"""Physical controls and fabric care for the actual placed bounce house."""
import copy,json,math
from pathlib import Path
from engine import excursions
ROUTINES=json.loads((Path(__file__).parent/'client/animation/castle-care.json').read_text())
DEFAULTS=dict(vent=0.,door=0.,latch=0.,tie_left=.8,tie_right=.8,apron=0.,flag=1.,hose=0.,kink=0.,dust=0.,mesh_wet=0.,roof_water=0.,prints=0.)
MOVING=('vent','door','tie_left','tie_right','apron','flag','hose','kink')

# Only the first explicitly adopted solo control uses native physical ownership.
PHYSICAL_SCORES={'castle_start'}

def physical_active(plan):
    if not isinstance(plan,dict) or plan.get('target')!='bounce_house':return False
    w=plan.get('carnival_work')
    if not isinstance(w,dict) or not isinstance(w.get('id'),str) or w.get('id') not in PHYSICAL_SCORES or w.get('castle_care') is not True or w.get('physical_pilot') is not True:return False
    p=w.get('physical')
    def point(v):
        return isinstance(v,(list,tuple)) and len(v)==2 and all(isinstance(n,(int,float)) and not isinstance(n,bool) and math.isfinite(n) for n in v)
    return bool(w.get('id') in PHYSICAL_SCORES and isinstance(p,dict) and p.get('version')==1
                and p.get('actor')=='cheese' and p.get('phase') in ('approach','hold','exit')
                and p.get('station')=='switch' and point(p.get('root')) and point(p.get('target'))
                and point(p.get('stance')) and point(p.get('center')) and point(p.get('exit'))
                and isinstance(p.get('route'),list) and bool(p['route']) and all(point(v) for v in p['route'])
                and type(p.get('waypoint')) is int and 0<=p['waypoint']<len(p['route'])
                and isinstance(p.get('travel_time'),(int,float)) and math.isfinite(p['travel_time']) and p['travel_time']>=0
                and isinstance(p.get('contact_ready'),bool))

def physical_pause(pond,plan,preserve_state=False):
    if not physical_active(plan):return
    pos=pond.game.renderer.duck_pos
    state=pos._state_str if preserve_state and pos._state_str in pos.ANIMATABLE_STATES else 'thinking'
    pos.cancel_movement()
    # Stopping a route alone enters idle, which can immediately choose a wander
    # target. Hold a non-expiring stationary state until explicit resume/care end.
    pos.set_state_by_name(state,0)
    plan['carnival_work']['physical']['contact_ready']=False

def physical_lifecycle_ok(plan):
    if not physical_active(plan):return False
    w=plan['carnival_work'];p=w['physical'];duration=ROUTINES[w['id']]['duration']
    clock=w.get('clock');elapsed=w.get('ride_elapsed');events=w.get('events');stage=w.get('stage')
    if any(type(v) not in (int,float) or not math.isfinite(v) or v<0 for v in (clock,elapsed)):return False
    if elapsed>duration or not isinstance(events,list) or any(type(v) is not int for v in events):return False
    expected=[i for i,effect in enumerate(ROUTINES[w['id']]['effects']) if effect[0]*duration<=elapsed]
    if events!=expected:return False
    if stage=='queue':return clock==0 and elapsed==0 and p['phase'] in ('approach','hold') and not w.get('done')
    if stage=='service':return clock==elapsed and p['phase'] in ('approach','hold') and not w.get('done')
    if stage in ('service_exit','done'):
        return (elapsed==duration and clock==0 and p['phase']=='exit'
                and p['route'][-1]==p['exit'] and bool(w.get('done'))==(stage=='done'))
    return False

# The first pilot is adult Cheese, solo, at the low blower switch. Rig offsets
# below come from its authored contact pose, not a renderer-generated body shift.
GEOMETRY=json.loads((Path(__file__).parent/'client/animation/castle-geometry.json').read_text())
Q=.66*GEOMETRY['detail_scale']
BX=.675*132/192
BY=.675*42/47
STANCE=dict(width=6,height=4,floor=False)

def art_world(center,x,y):
    return [center[0]+(x-GEOMETRY['width']/2)*Q*132/192,
            center[1]+(y-GEOMETRY['height'])*Q*42/47]

def control_world(center,name='switch'):
    point=GEOMETRY['controls'][name]
    return art_world(center,point['x']+.5,point['y']+.5)

def placement_center(pond,plan):
    place=next((p for p in pond.placements if p.instance==plan.get('instance') and p.item_id=='bounce_house'),None)
    if place is None:return None
    x,y=place.get_display_position()
    return [x*132/20,y*42/12]

def reach_distance(root,target):
    hand=[root[0]+15.5*BX,root[1]-4*BY]
    return math.hypot((target[0]-hand[0])/BX,(target[1]-hand[1])/BY)

def supported(pond,plan,root,center):
    from engine import terrain
    from engine.portable_ground import policy
    if not policy(pond).check('rock',root[0]*20/132,root[1]*12/42,plan.get('instance'),STANCE)[0]:return False
    # Excluding this copy's layout collision does not permit walking through it.
    # The entire front corridor is at/south of its real ground row. A root may
    # approach that corridor from outside either outer wall, never through fabric.
    ground=art_world(center,0,GEOMETRY['ground_row'])[1]
    left=art_world(center,0,0)[0];right=art_world(center,GEOMETRY['width'],0)[0]
    if root[1]<ground and left-3*BX<root[0]<right+3*BX:return False
    for dx in (-3.5*BX,2.5*BX):
        if terrain.water_at(pond.location,root[0]+dx,root[1],pond.biome):return False
    return True

def segment_clear(pond,plan,start,end,center):
    # Match the existing animator's diagonal unit steps, including fractional
    # starting positions. Arrival is observed within .51, never teleported.
    point=list(start)
    for _ in range(180):
        if not supported(pond,plan,point,center):return False
        if max(abs(point[i]-end[i]) for i in (0,1))<=.51:return True
        point=[point[i]+(1 if point[i]<end[i] else -1 if point[i]>end[i] else 0) for i in (0,1)]
    return False

def physical_prepare(pond,plan):
    w=plan['carnival_work'];pos=pond.game.renderer.duck_pos;center=placement_center(pond,plan)
    if center is None:return physical_interrupt(pond,plan,'The placed house is no longer here.')
    target=control_world(center);ground=art_world(center,0,GEOMETRY['ground_row'])[1]
    preferred=[target[0]-16.5*BX,ground]
    candidates=sorted(([x,y] for x in range(math.floor(preferred[0])-3,math.ceil(preferred[0])+4)
                       for y in range(math.ceil(ground),math.ceil(ground)+4)),key=lambda v:(v[0]-preferred[0])**2+(v[1]-preferred[1])**2)
    stance=next((v for v in candidates if supported(pond,plan,v,center) and reach_distance(v,target)<=3),None)
    entry=art_world(center,GEOMETRY['entry']['x'],GEOMETRY['ground_row'])
    exit_point=[round(entry[0]),math.ceil(ground)]
    route=[];root=[pos.x,pos.y]
    if root[1]<ground:route.append([round(root[0]),math.ceil(ground)])
    route.append(exit_point)
    if stance is not None:route.append(stance)
    previous=root
    if stance is None:return physical_interrupt(pond,plan,'The blower switch has no dry reachable stance.')
    for point in route:
        if not segment_clear(pond,plan,previous,point,center):return physical_interrupt(pond,plan,'The exterior route to the blower is blocked.')
        previous=point
    w['physical']=dict(version=1,actor='cheese',center=center,root=root,target=target,stance=stance,
                       phase='approach',station='switch',contact_ready=False,route=route,waypoint=0,
                       exit=exit_point,travel_time=0.)
    w['invitation_checked']=True;w['paired']=False
    plan['approach_destination']=list(stance)
    pos.move_to(*route[0])
    return True

def physical_interrupt(pond,plan,reason):
    w=plan['carnival_work'];w.update(done=True,interrupted=True,physical_error=reason)
    if isinstance(w.get('physical'),dict):w['physical']['contact_ready']=False
    pond.game.renderer.duck_pos.cancel_movement();clear(pond,plan)
    return False

def physical_geometry_ok(pond,plan):
    if not physical_lifecycle_ok(plan):return False
    p=plan['carnival_work']['physical'];center=placement_center(pond,plan)
    if center!=p['center'] or p['target']!=control_world(center):return False
    ground=art_world(center,0,GEOMETRY['ground_row'])[1]
    entry=art_world(center,GEOMETRY['entry']['x'],GEOMETRY['ground_row'])
    return (p['exit']==[round(entry[0]),math.ceil(ground)] and p['stance'][1]>=ground
            and all(n==round(n) for n in p['stance']) and reach_distance(p['stance'],p['target'])<=3
            and supported(pond,plan,p['stance'],center))

def physical_restore(pond,plan):
    w=plan['carnival_work']
    # Material contacts and event indices remain consumed. Reacquire support
    # from the loaded actor's actual root; never teleport to a saved picture.
    if not physical_geometry_ok(pond,plan):return physical_interrupt(pond,plan,'Invalid saved control reservation.')
    if w.get('done'):
        pond.game.renderer.duck_pos.cancel_movement();return True
    was_exit=w['physical']['phase']=='exit'
    if not physical_prepare(pond,plan):return False
    if was_exit:
        p=w['physical'];p.update(phase='exit',route=[p['exit']],waypoint=0)
    physical_pause(pond,plan)
    return True

def physical_advance(pond,plan,dt):
    from engine import carnival
    w=plan['carnival_work'];pos=pond.game.renderer.duck_pos
    if not physical_geometry_ok(pond,plan):return physical_interrupt(pond,plan,'Invalid native control reservation.')
    p=w['physical'];root=[pos.x,pos.y];previous=p['root'];p['root']=root;p['contact_ready']=False
    center=placement_center(pond,plan)
    if center!=p['center'] or pond.game.duck.growth_stage!='adult':return physical_interrupt(pond,plan,'The control reservation changed.')
    if not allowed(pond,w['id']) or pond.game.duck.needs.energy<10 or pond.game.duck.needs.hunger<15:return physical_interrupt(pond,plan,'Control work interrupted by weather or urgent care.')
    if not segment_clear(pond,plan,previous,root,center):return physical_interrupt(pond,plan,'The actual walking segment is blocked.')
    if p['phase'] in ('approach','exit'):
        p['travel_time']+=max(0,excursions.finite(dt))
        if p['travel_time']>90:return physical_interrupt(pond,plan,'The control stance was not reached.')
        route=p['route'];index=p['waypoint'];destination=route[index]
        if not segment_clear(pond,plan,root,destination,center):return physical_interrupt(pond,plan,'The remaining exterior route is blocked.')
        if max(abs(root[i]-destination[i]) for i in (0,1))<=.51:
            pos.cancel_movement();p['waypoint']+=1
            if p['waypoint']<len(route):pos.move_to(*route[p['waypoint']]);return True
            p['waypoint']=len(route)-1
            if p['phase']=='exit':w.update(stage='done',done=True);clear(pond,plan);return False
            p['phase']='hold';pos.set_state_by_name('thinking',0)
        else:
            if not pos._is_directed_movement or [pos.target_x,pos.target_y]!=destination:pos.move_to(*destination)
            return True
    if not supported(pond,plan,root,center) or reach_distance(root,p['target'])>3 or max(abs(root[i]-p['stance'][i]) for i in (0,1))>.51:
        return physical_interrupt(pond,plan,'The actual feet and grip cannot reach the switch.')
    p['contact_ready']=True
    if plan['phase']!='act':return True
    obj=pond.object_state('bounce_house',plan);s=state(obj);s['active']=True
    if w['stage']=='queue':
        w['start']=copy.deepcopy(s);carnival.stage(w,'service',ROUTINES[w['id']]['duration'])
    if w['stage']=='service':
        duration=ROUTINES[w['id']]['duration'];old=w['clock'];step=min(max(0,excursions.finite(dt)),duration-old)
        w['clock']+=step;w['elapsed']+=step;w['ride_elapsed']=w['clock'];s['stroke']=max(0,math.sin(w['clock']*4))
        for i,effect in enumerate(ROUTINES[w['id']]['effects']):
            if old<effect[0]*duration<=w['clock']:apply(obj,w,i,effect)
        if w['clock']>=duration:
            p.update(phase='exit',contact_ready=False,route=[p['exit']],waypoint=0,travel_time=0.)
            carnival.stage(w,'service_exit',0);pos.move_to(*p['exit'])
    return True


def state(obj):
    if not isinstance(obj.get('castle'),dict):obj['castle']={}
    s=obj['castle'];s['motor']=s.get('motor') if s.get('motor') in ('auto','on','off') else 'auto'
    s['power_hold']=s.get('power_hold',s['motor']=='off') is True
    for key,value in DEFAULTS.items():s[key]=excursions.clamp(s.get(key,value))
    if not isinstance(s.get('targets'),dict):s['targets']={}
    for key in MOVING:s['targets'][key]=excursions.clamp(s['targets'].get(key,s[key]))
    s['fan']=excursions.finite(s.get('fan'))%math.tau;s['powered']=s.get('powered') is True
    s['spray']=excursions.clamp(s.get('spray'));s['stroke']=excursions.clamp(s.get('stroke'));s['active']=s.get('active') is True
    return s

def update(obj,dt,outdoors,wet,wind,hour,reserved):
    s=state(obj);dt=max(0,excursions.finite(dt))
    if not outdoors:s['powered']=False;return
    if reserved=='hold':return
    for key in MOVING:
        s[key]+=(s['targets'][key]-s[key])*(1-math.exp(-dt*1.6))
        if abs(s[key]-s['targets'][key])<.001:s[key]=s['targets'][key]
    night=hour<7 or hour>=20
    s['powered']=bool(not wet and wind<.8 and excursions.finite(obj.get('condition'),1.)>.2 and s['motor']!='off' and (s['motor']=='on' or not night or reserved=='active') and s['hose']<.15)
    if s['powered']:s['fan']=(s['fan']+dt*12)%math.tau
    s['spray']*=math.exp(-dt*2)
    if not reserved:s['active']=False;s['stroke']=0.
    # Moisture is material state, not an emitted effect pretending to be rain.
    for key,rate in (('mesh_wet',.0012),('roof_water',.0007)):
        s[key]=excursions.clamp(s[key]+dt*(rate if wet else -.0002))
    s['dust']=excursions.clamp(s['dust']+dt*.000015*(1+wind))

def ready(obj):
    s=state(obj)
    if s['motor']=='off' or s['hose']>.15 or s['kink']>.6:return False,'Start the blower and straighten its hose before bouncing.'
    if s['vent']>.2:return False,'Close the air valve before bouncing.'
    if min(s['tie_left'],s['tie_right'])<.45:return False,'Snug both guy ropes before bouncing.'
    if s['latch']>.5 or s['apron']>.3:return False,'Unbuckle the mesh and flatten the landing apron first.'
    return True,''

def allowed(pond,choice):
    from engine import carnival
    return not carnival.blocked(pond) or ROUTINES[choice]['weatherSafe']

def starts_blower(choice):
    return any(key=='motor' and value=='on' for _,key,value in ROUTINES[choice]['effects'])

def next_work(pond,obj):
    """A useful job on this copy, with an explainable reason; never a random chore."""
    s=state(obj);weather=pond.weather_type
    if any(word in weather for word in ('storm','blizzard','gale','tornado','hurricane')) or pond.state['ecology']['wind']>=.8:return None
    if excursions.adverse(weather):
        if s['motor']!='off' or s['latch']<.5 or s['apron']<.8 or s['flag']>.2:
            return 'castle_rain_cover','rain is reaching the open fabric',24
        return None
    if pond.hour>=20 or pond.hour<7:
        if s['motor']!='off' or s['latch']<.5 or s['flag']>.2:
            return 'castle_close_night','the empty house is still open for the night',18
        return None
    if s['roof_water']>.45 or s['mesh_wet']>.45:return 'castle_after_rain','water is still caught in the roof and mesh',24
    if s['dust']>.55:return ('castle_grill_clean' if s['power_hold'] or obj.get('condition',1)<=.2 else 'castle_dust_service'),'dust has collected on the blower grille',24
    # An explicit player shutdown remains off. Autonomous closing can be undone
    # next morning, but residents do not undo a manually requested shutdown.
    if s['power_hold'] or obj.get('condition',1)<=.2:return None
    if min(s['tie_left'],s['tie_right'])<.45:return 'castle_spring_retension','the side ropes have slackened',22
    if s['vent']>.2 or s['kink']>.6:return 'castle_pressure_check','air is escaping or the supply hose is bent',22
    if s['motor']=='off' or s['hose']>.15 or s['latch']>.5 or s['apron']>.3:return 'castle_open_day','the weather has cleared but the house is still closed',16
    if s['prints']>.5:return 'castle_apron_clean','footprints cover the landing apron',18
    return None

def make(pond,plan,choice):
    s=ROUTINES[choice]
    return dict(id=choice,label=s['label'],stage='queue',clock=0.,elapsed=0.,ride_elapsed=0.,done=False,invitation_checked=False,castle_care=True,events=[],fractions={},automatic=bool(plan.get('automatic')),physical_pilot=choice in PHYSICAL_SCORES and pond.game.duck.growth_stage=='adult')

def clear(pond,plan):
    if plan and plan.get('target')=='bounce_house':
        s=state(pond.object_state('bounce_house',plan));s.update(active=False,stroke=0.)

def station(work,role='a'):
    spec=ROUTINES[work['id']]
    steps=spec.get('partnerStations',[[0,spec['partner']]]) if role=='b' else spec.get('stations',[[0,spec['station']]])
    name=previous=steps[0][1];travel=1.
    for at,target in steps[1:]:
        if work['ride_elapsed']<at*spec['duration']:break
        previous,name=name,target;travel=excursions.clamp((work['ride_elapsed']-at*spec['duration'])/2)
    return dict(name=name,previous=previous,travel=travel)

def apply(obj,w,index,effect):
    if index in w['events']:return
    at,key,value=effect;s=state(obj)
    if key.endswith('_fraction'):
        field={'dust_fraction':'dust','mesh_fraction':'mesh_wet','roof_fraction':'roof_water','prints_fraction':'prints'}[key]
        before=s[field];amount=w['start'][field]*(w['fractions'].get(field,1)-value);s[field]=max(0,s[field]-amount);w['fractions'][field]=value
        if field in ('mesh_wet','roof_water'):s['spray']=min(1,s['spray']+(before-s[field])*4)
    elif key=='inspection':
        history=obj.setdefault('castle_inspections',{});history[value]=min(9999,history.get(value,0)+1)
        w['inspection']=dict(kind=value,pressure=round(obj['excursion']['inflation'],3),condition=round(obj['condition'],3))
        w.setdefault('inspections',[]).append(copy.deepcopy(w['inspection']))
    elif key=='motor':
        s['motor']=value
        if not w.get('automatic'):s['power_hold']=value=='off'
    elif key in MOVING:s['targets'][key]=value
    else:s[key]=value
    w['events'].append(index)

def advance(pond,plan,dt,r):
    from engine import carnival
    w=plan['carnival_work'];spec=ROUTINES[w['id']];obj=pond.object_state('bounce_house',plan);s=state(obj);s['active']=True
    needs=pond.game.duck.needs
    bad=not allowed(pond,w['id']) or needs.energy<10 or needs.hunger<15
    if bad and not w.get('withdrawal'):
        w['withdrawal']=True;w['withdrawal_at']=w['elapsed']
        if w['stage']=='queue':w.update(done=True,interrupted=True);clear(pond,plan);return False
        if w['stage']=='service':carnival.stage(w,'service_exit',4)
    remaining=min(300,max(0,excursions.finite(dt)))
    for _ in range(8):
        if remaining<=0 or w['done']:break
        if w['stage']=='queue':
            w['clock']+=remaining;w['elapsed']+=remaining;remaining=0
            if r and r['phase']=='approach' and w['clock']<26:return True
            if r and r['phase']=='approach':carnival.release(pond.minds,r['actor']);r=None
            w['start']=copy.deepcopy(s);w['paired']=bool(r and r['phase']=='ready');carnival.stage(w,'service',spec['duration']);break
        name=w['stage'];step=min(remaining,max(0,w['stage_duration']-w['clock']));old=w['clock'];w['clock']+=step;w['elapsed']+=step;remaining-=step
        if name=='service':
            w['ride_elapsed']=w['clock'];s['stroke']=max(0,math.sin(w['clock']*4))
            for i,effect in enumerate(spec['effects']):
                if old<effect[0]*spec['duration']<=w['clock']:apply(obj,w,i,effect)
            if r and r['phase']=='ready':r['overlap']+=step
        if w['clock']<w['stage_duration']:break
        if name=='service':carnival.stage(w,'service_exit',4)
        else:w.update(stage='done',done=True,interrupted=bool(w.get('withdrawal')));clear(pond,plan)
    pond._cache=None
    return not w['done']

def conversation(pond,plan,key,r):
    w=plan['carnival_work'];s=state(pond.object_state('bounce_house',plan));spec=ROUTINES[w['id']]
    where=station(w,'a' if key=='cheese' else 'b')
    return dict(object='bounce house',activity=spec['label'],stage=w['stage'],paused=bool(plan.get('paused')),
      body_status='watching from outside' if key!='cheese' and r and r['mode']=='watch' else 'walking between the '+where['previous'].replace('_',' ')+' and '+where['name'].replace('_',' ') if where['travel']<1 else 'working at the low '+where['name'].replace('_',' '),
      motor=s['motor'],player_left_switched_off=s['power_hold'],fan_turning=s['powered'],pressure=round(pond.object_state('bounce_house',plan)['excursion']['inflation'],2),
      door_open=round(s['door'],2),door_buckled=s['latch']>.5,completed_contacts=len(w['events']),inspection=w.get('inspection'),
      company=pond.minds.model.residents[r['actor']]['name'] if r else None,setting='Both residents stay outside the empty house. Controls and cleaning act only on this placed copy.')
