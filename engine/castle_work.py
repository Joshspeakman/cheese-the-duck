"""Physical controls and fabric care for the actual placed bounce house."""
import copy,json,math
from pathlib import Path
from engine import excursions
ROUTINES=json.loads((Path(__file__).parent/'client/animation/castle-care.json').read_text())
DEFAULTS=dict(vent=0.,door=0.,latch=0.,tie_left=.8,tie_right=.8,apron=0.,flag=1.,hose=0.,kink=0.,dust=0.,mesh_wet=0.,roof_water=0.,prints=0.)
MOVING=('vent','door','tie_left','tie_right','apron','flag','hose','kink')

# These controls use explicit age geometry; no unknown-age adult fallback.
CONTACT_METRICS=json.loads((Path(__file__).parent/'client/animation/castle-contact-metrics.json').read_text())['ages']
AIR_SCORES={'castle_start','castle_stop','castle_vent_open','castle_vent_close','castle_hose_straight','castle_hose_stow','castle_grill_clean','castle_gauge_check'}
PHYSICAL_SCORES=AIR_SCORES|{'castle_door_open'}

def canonical_age(age):
    age='juvenile' if age=='teen' else age
    return age if isinstance(age,str) and age in CONTACT_METRICS else None

def physical_age_ok(pond,plan):
    if not isinstance(plan,dict):return False
    w=plan.get('carnival_work');p=w.get('physical') if isinstance(w,dict) else None
    age=canonical_age(pond.game.duck.growth_stage)
    return bool(age and isinstance(p,dict) and p.get('source_age')==age and w.get('source_age')==age)

def effect_metrics(work):
    if work['id'] in AIR_SCORES:
        from engine import castle_air
        return castle_air.DATA['ages'][work['source_age']]['routines'][work['id']]
    return CONTACT_METRICS[work['source_age']]['routines'][work['id']]

def rig_metric(work):return effect_metrics(work)[0]

def pitches(metric):return metric['scale']*132/192,metric['scale']*42/47

def physical_active(plan):
    if not isinstance(plan,dict) or plan.get('target')!='bounce_house':return False
    w=plan.get('carnival_work')
    if not isinstance(w,dict) or not isinstance(w.get('id'),str) or w.get('id') not in PHYSICAL_SCORES or w.get('castle_care') is not True or w.get('physical_pilot') is not True:return False
    p=w.get('physical')
    def point(v):
        return isinstance(v,(list,tuple)) and len(v)==2 and all(isinstance(n,(int,float)) and not isinstance(n,bool) and math.isfinite(n) for n in v)
    return bool(w.get('id') in PHYSICAL_SCORES and isinstance(p,dict) and p.get('version')==1
                and canonical_age(p.get('source_age'))==p.get('source_age') and p.get('source_age') is not None
                and w.get('source_age')==p.get('source_age')
                and p.get('actor')=='cheese' and p.get('phase') in ('approach','hold','exit')
                and type(p.get('station_index')) is int and 0<=p['station_index']<len(physical_stations(w))
                and p.get('station')==physical_stations(w)[p['station_index']][1]
                and p.get('route_kind') in ('initial','transfer','exit') and point(p.get('route_origin')) and point(p.get('root')) and point(p.get('target'))
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
    steps=physical_stations(w)
    cursor=max(i for i,(at,_) in enumerate(steps) if at*duration<=elapsed)
    if p['station_index']!=cursor:return False
    if p['phase']=='exit':
        if p['route_kind']!='exit' or p['route']!=[p['exit']]:return False
    else:
        if p['route_kind']=='exit' or p['route'][-1]!=p['stance']:return False
        if p['phase']=='hold' and p['waypoint']!=len(p['route'])-1:return False
        if p['route_kind']=='transfer' and (cursor==0 or p['route']!=[p['stance']]):return False
    if stage=='queue':return clock==0 and elapsed==0 and p['phase'] in ('approach','hold') and not w.get('done')
    if stage=='service':return clock==elapsed and p['phase'] in ('approach','hold') and not w.get('done')
    if stage in ('service_exit','done'):
        return (elapsed==duration and clock==0 and p['phase']=='exit'
                and p['route'][-1]==p['exit'] and bool(w.get('done'))==(stage=='done'))
    return False

# Contact and support use each reserved age's actual authored rig geometry.
GEOMETRY=json.loads((Path(__file__).parent/'client/animation/castle-geometry.json').read_text())
Q=.66*GEOMETRY['detail_scale']

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

def reach_distance(root,target,grip=(15.5,-4),scale=.675):
    bx,by=scale*132/192,scale*42/47
    hand=[root[0]+grip[0]*bx,root[1]+grip[1]*by]
    return math.hypot((target[0]-hand[0])/bx,(target[1]-hand[1])/by)

def supported(pond,plan,root,center):
    from engine import terrain
    from engine.portable_ground import policy
    if plan['carnival_work']['id'] in AIR_SCORES:
        from engine import castle_air
        return castle_air.supported(pond,plan,plan['carnival_work']['id'],dict(actor='cheese',adapter='cheese',source_age=plan['carnival_work']['source_age']),root)
    metric=rig_metric(plan['carnival_work']);bx,by=pitches(metric)
    feet=list({tuple(f) for m in effect_metrics(plan['carnival_work']) for f in m['feet']})
    # Retain the conservative four-cell adult depth, scaled to this age's pitch;
    # width spans its actual feet. Each foot is also tested individually below.
    width=(max(f[0] for f in feet)-min(f[0] for f in feet))*metric['scale']/.675
    stance=dict(width=width,height=4*metric['scale']/.675,floor=False)
    if not policy(pond).check('rock',root[0]*20/132,root[1]*12/42,plan.get('instance'),stance)[0]:return False
    # Excluding this copy's layout collision does not permit walking through it.
    # The entire front corridor is at/south of its real ground row. A root may
    # approach that corridor from outside either outer wall, never through fabric.
    ground=art_world(center,0,GEOMETRY['ground_row'])[1]
    left=art_world(center,0,0)[0];right=art_world(center,GEOMETRY['width'],0)[0]
    # Outside the front corridor, neither actual foot may enter this copy's
    # fabric; large-age feet can extend beyond the retained body margin.
    right_reach=max(3,max(f[0] for f in feet))*bx
    left_reach=max(3,-min(f[0] for f in feet))*bx
    if root[1]<ground and left-right_reach<root[0]<right+left_reach:return False
    for fx,fy in feet:
        if terrain.water_at(pond.location,root[0]+fx*bx,root[1]+fy*by,pond.biome):return False
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

def physical_stations(work):
    spec=ROUTINES[work['id']]
    return spec.get('stations',[[0,spec['station']]])

def station_grips(work,name):
    return [e['grip'] for e in effect_metrics(work) if e['station']==name and 'grip' in e]

def physical_route(root,stance,exit_point,ground,kind):
    if kind=='exit':return [exit_point]
    if kind=='transfer':return [stance]
    route=[]
    if root[1]<ground:route.append([round(root[0]),math.ceil(ground)])
    return route+[exit_point,stance]

def physical_sites(pond,plan,center):
    w=plan['carnival_work']
    if w['id'] in AIR_SCORES:
        from engine import castle_air
        return castle_air.plan_sites(pond,plan,w['id'],dict(actor='cheese',adapter='cheese',source_age=w['source_age']))
    metric=rig_metric(w);bx,by=pitches(metric)
    ground=art_world(center,0,GEOMETRY['ground_row'])[1];sites=[]
    for _,name in physical_stations(w):
        target=control_world(center,name);grips=station_grips(w,name)
        preferred=[target[0]-(max(g[0] for g in grips)+1)*bx,ground]
        candidates=sorted(([x,y] for x in range(math.floor(preferred[0])-3,math.ceil(preferred[0])+4)
                           for y in range(math.ceil(ground),math.ceil(ground)+4)),key=lambda v:(v[0]-preferred[0])**2+(v[1]-preferred[1])**2)
        stance=next((v for v in candidates if supported(pond,plan,v,center) and all(reach_distance(v,target,g,metric['scale'])<=3 for g in grips)),None)
        if stance is None:return None,name
        sites.append(dict(station=name,target=target,stance=stance))
    return sites,None

def physical_prepare(pond,plan,cursor=0,kind='initial'):
    w=plan['carnival_work'];pos=pond.game.renderer.duck_pos;center=placement_center(pond,plan)
    age=canonical_age(pond.game.duck.growth_stage)
    if age is None or w.get('source_age')!=age:return physical_interrupt(pond,plan,'This age has no valid control reservation.')
    if center is None:return physical_interrupt(pond,plan,'The placed house is no longer here.')
    # Reserve a complete feasible itinerary before even starting the walk. An
    # unreachable later cord must not first consume an unlatch/shutdown effect.
    sites,missing=physical_sites(pond,plan,center)
    if sites is None:return physical_interrupt(pond,plan,'The '+missing+' has no dry reachable stance for this age.')
    ground=art_world(center,0,GEOMETRY['ground_row'])[1]
    entry=art_world(center,GEOMETRY['entry']['x'],GEOMETRY['ground_row'])
    exit_point=[round(entry[0]),math.ceil(ground)];root=[pos.x,pos.y]
    site=sites[cursor];name=site['station'];stance=site['stance'];target=site['target']
    route=physical_route(root,stance,exit_point,ground,kind)
    itinerary=route if kind=='exit' else route+[v['stance'] for v in sites[cursor+1:]]+[exit_point]
    previous=root
    for point in itinerary:
        if not segment_clear(pond,plan,previous,point,center):return physical_interrupt(pond,plan,'The exterior route to the '+name+' is blocked.')
        previous=point
    w['physical']=dict(version=1,actor='cheese',source_age=age,center=center,root=root,target=target,stance=stance,
                       phase='approach',station=name,station_index=cursor,contact_ready=False,route=route,waypoint=0,
                       route_origin=list(root),route_kind=kind,exit=exit_point,travel_time=0.)
    if 'observation_target' in site:w['physical']['observation_target']=site['observation_target']
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
    if not physical_age_ok(pond,plan) or not physical_lifecycle_ok(plan):return False
    w=plan['carnival_work'];p=w['physical'];center=placement_center(pond,plan)
    if center!=p['center'] or p['target']!=control_world(center,p['station']):return False
    if w['id'] in AIR_SCORES:
        from engine import castle_air
        if w['id']=='castle_gauge_check' and p.get('observation_target')!=castle_air.observation_target(center):return False
    ground=art_world(center,0,GEOMETRY['ground_row'])[1]
    entry=art_world(center,GEOMETRY['entry']['x'],GEOMETRY['ground_row'])
    return (p['exit']==[round(entry[0]),math.ceil(ground)] and p['stance'][1]>=ground
            and p['route']==physical_route(p['route_origin'],p['stance'],p['exit'],ground,p['route_kind'])
            and (w['id'] in AIR_SCORES or all(n==round(n) for n in p['stance']))
            and all(reach_distance(p['stance'],p['target'],g,rig_metric(w)['scale'])<=3 for g in station_grips(w,p['station']))
            and supported(pond,plan,p['stance'],center))

def physical_restore(pond,plan):
    w=plan['carnival_work']
    # Material contacts and event indices remain consumed. Reacquire support
    # from the loaded actor's actual root; never teleport to a saved picture.
    if not physical_geometry_ok(pond,plan):return physical_interrupt(pond,plan,'Invalid saved control reservation.')
    if w.get('done'):
        pond.game.renderer.duck_pos.cancel_movement();return True
    old=w['physical'];was_exit=old['phase']=='exit'
    if not physical_prepare(pond,plan,old['station_index'],kind='exit' if was_exit else 'initial'):return False
    if was_exit:w['physical']['phase']='exit'
    physical_pause(pond,plan)
    return True

def physical_advance(pond,plan,dt):
    from engine import carnival
    w=plan['carnival_work'];pos=pond.game.renderer.duck_pos
    if not physical_geometry_ok(pond,plan):return physical_interrupt(pond,plan,'Invalid native control reservation.')
    p=w['physical'];root=[pos.x,pos.y];previous=p['root'];p['root']=root;p['contact_ready']=False
    center=placement_center(pond,plan)
    if center!=p['center'] or not physical_age_ok(pond,plan):return physical_interrupt(pond,plan,'The control reservation changed.')
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
            if p['phase']=='exit':
                # The outer plan may still settle before consuming completion.
                # Keep the reached exit instead of allowing idle to wander away.
                pos.set_state_by_name('thinking',0)
                w.update(stage='done',done=True);clear(pond,plan);return False
            p['phase']='hold';pos.set_state_by_name('thinking',0)
        else:
            if not pos._is_directed_movement or [pos.target_x,pos.target_y]!=destination:pos.move_to(*destination)
            return True
    if not supported(pond,plan,root,center) or not all(reach_distance(root,p['target'],g,rig_metric(w)['scale'])<=3 for g in station_grips(w,p['station'])) or max(abs(root[i]-p['stance'][i]) for i in (0,1))>.51:
        return physical_interrupt(pond,plan,'The actual feet and grip cannot reach the '+p['station']+'.')
    p['contact_ready']=w['id']!='castle_gauge_check'
    p['observation_ready']=False
    if plan['phase']!='act':return True
    obj=pond.object_state('bounce_house',plan);s=state(obj);s['active']=True
    if w['stage']=='queue':
        w['start']=copy.deepcopy(s);carnival.stage(w,'service',ROUTINES[w['id']]['duration'])
    if w['stage']=='service' and w['id'] in AIR_SCORES:
        from engine import castle_air
        def preflight():
            sites,_=physical_sites(pond,plan,center)
            if not sites:return False
            points=[root]+[v['stance'] for v in sites[p['station_index']:]]+[p['exit']]
            return all(segment_clear(pond,plan,a,b,center) for a,b in zip(points,points[1:]))
        context=dict(operator=dict(actor='cheese',adapter='cheese',source_age=w['source_age']),physical=p,preflight=preflight)
        answer=castle_air.advance_atomic(pond,plan,w,context,dt)
        w['done']=False
        if answer['status']=='blocked':return physical_interrupt(pond,plan,answer['reason'])
        if answer['status']=='transfer':return physical_prepare(pond,plan,p['station_index']+1,kind='transfer')
        if answer['status']=='finished':
            p.update(phase='exit',contact_ready=False,observation_ready=False,route=[p['exit']],waypoint=0,travel_time=0.,route_kind='exit',route_origin=list(root))
            carnival.stage(w,'service_exit',0);pos.move_to(*p['exit'])
        return True
    if w['stage']=='service':
        spec=ROUTINES[w['id']];duration=spec['duration'];remaining=max(0,excursions.finite(dt))
        steps=physical_stations(w);cursor=p['station_index']
        boundary=steps[cursor+1][0]*duration if cursor+1<len(steps) else duration
        # Split at each authored effect and station boundary. No score time is
        # spent walking; an arbitrarily large dt cannot operate the next station.
        while remaining>0 and w['clock']<boundary:
            old=w['clock']
            upcoming=[e[0]*duration for i,e in enumerate(spec['effects']) if i not in w['events'] and e[0]*duration>old]
            stop=min([old+remaining,boundary]+upcoming)
            if stop<=old:break  # Sub-ULP remainder cannot advance this score clock.
            step=stop-old;w['clock']=stop;w['elapsed']+=step;w['ride_elapsed']=stop;remaining-=step
            s['stroke']=max(0,math.sin(stop*4))
            for i,effect in enumerate(spec['effects']):
                if old<effect[0]*duration<=stop:
                    if i==0:
                        sites,missing=physical_sites(pond,plan,center)
                        if sites is None:return physical_interrupt(pond,plan,'A required later stance is no longer reachable.')
                        previous=root
                        for point in [v['stance'] for v in sites[1:]]+[p['exit']]:
                            if not segment_clear(pond,plan,previous,point,center):return physical_interrupt(pond,plan,'A required later route is blocked before the first contact.')
                            previous=point
                    metric=effect_metrics(w)[i]
                    if metric['station']!=p['station'] or reach_distance(root,p['target'],metric['grip'],metric['scale'])>3:
                        return physical_interrupt(pond,plan,'The authored contact cannot reach its control.')
                    if w['id']=='castle_hose_stow' and effect[1]=='hose' and (0 not in w['events'] or s['motor']!='off'):
                        return physical_interrupt(pond,plan,'Stop the blower before coiling its hose.')
                    apply(obj,w,i,effect)
        if w['clock']>=boundary and cursor+1<len(steps):
            return physical_prepare(pond,plan,cursor+1,kind='transfer')
        if w['clock']>=duration:
            p.update(phase='exit',contact_ready=False,route=[p['exit']],waypoint=0,travel_time=0.,route_kind='exit',route_origin=list(root))
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
    # Old saves had only an energized flag and a visible fabric volume. Do not
    # turn passive/night fabric inflation into a fabricated pressure reading.
    s['rotor_speed']=excursions.clamp(s.get('rotor_speed',float(s['powered'])))
    old_inflation=obj.get('excursion',{}).get('inflation',1.) if isinstance(obj.get('excursion'),dict) else 1.
    s['pressure']=excursions.clamp(s.get('pressure',old_inflation if s['powered'] else 0.))
    s['airflow']=excursions.clamp(s.get('airflow',s['rotor_speed']*(1-.65*s['dust'])*(1-s['hose'])*(1-.6*s['kink'])))
    s['power_revision']=s.get('power_revision',0) if type(s.get('power_revision',0)) is int and s.get('power_revision',0)>=0 else 0
    s['spray']=excursions.clamp(s.get('spray'));s['stroke']=excursions.clamp(s.get('stroke'));s['active']=s.get('active') is True
    return s

# Authored gameplay response rates, in inverse seconds. Pressure is actual
# normalized supplied air; excursion.inflation remains a downstream art volume.
ROTOR_UP=2.4
ROTOR_COAST=1.6
ROTOR_STOP=.01
PRESSURE_RATE=.08
TRANSIENT_SECONDS=20.
MECHANISM_STEP=1/60


def airflow(s):return s['rotor_speed']*(1-.65*s['dust'])*(1-s['hose'])*(1-.6*s['kink'])


def _rotor(s,dt):
    old=s['rotor_speed']
    if s['powered']:
        decay=math.exp(-ROTOR_UP*dt)
        integral=dt+(old-1)*(1-decay)/ROTOR_UP
        s['rotor_speed']=1+(old-1)*decay
    else:
        stop_at=math.log(old/ROTOR_STOP)/ROTOR_COAST if old>ROTOR_STOP else 0.
        elapsed=min(dt,stop_at);decay=math.exp(-ROTOR_COAST*elapsed)
        integral=old*(1-decay)/ROTOR_COAST
        s['rotor_speed']=0. if dt>=stop_at else old*decay
    s['fan']=(s['fan']+12*integral)%math.tau


def _linear_pressure(value,a,b,dt):
    # Exact solution of P'=rate*(a+b*t-P), including constant supply.
    decay=math.exp(-PRESSURE_RATE*dt)
    return a+b*(dt-1/PRESSURE_RATE)+(value-a+b/PRESSURE_RATE)*decay


def update(obj,dt,outdoors,wet,wind,hour,reserved):
    s=state(obj);dt=max(0,excursions.finite(dt))
    if reserved=='hold':return s['pressure']
    night=hour<7 or hour>=20
    s['powered']=bool(outdoors and not wet and wind<.8 and excursions.finite(obj.get('condition'),1.)>.2 and s['motor']!='off' and (s['motor']=='on' or not night or reserved=='active'))
    if not outdoors:
        _rotor(s,dt);s['airflow']=0.;s['pressure']*=math.exp(-PRESSURE_RATE*dt)
        return s['pressure']
    dust_rate=.000015*(1+wind)
    def material_step(h):
        for key in MOVING:
            s[key]+=(s['targets'][key]-s[key])*(1-math.exp(-h*1.6))
            if abs(s[key]-s['targets'][key])<.001:s[key]=s['targets'][key]
        s['dust']=excursions.clamp(s['dust']+h*dust_rate)
        for key,rate in (('mesh_wet',.0012),('roof_water',.0007)):
            s[key]=excursions.clamp(s[key]+h*(rate if wet else -.0002))
        s['spray']*=math.exp(-h*2)
        _rotor(s,h)
    # Midpoint forcing with exact material/rotor substeps. At most 1200 steps,
    # independent of offline duration; after 20s every eased control is snapped
    # to its target and the rotor residual is below floating-point resolution.
    transient=min(dt,TRANSIENT_SECONDS);steps=max(1,math.ceil(transient/MECHANISM_STEP));h=transient/steps
    for _ in range(steps):
        material_step(h/2)
        target=airflow(s)*(1-s['vent']*.85)
        s['pressure']=target+(s['pressure']-target)*math.exp(-PRESSURE_RATE*h)
        material_step(h/2)
    tail=dt-transient
    if tail>0:
        coefficient=s['rotor_speed']*(1-s['hose'])*(1-.6*s['kink'])*(1-.85*s['vent'])
        to_clamp=(1-s['dust'])/dust_rate if dust_rate>0 else tail
        linear=min(tail,max(0,to_clamp))
        s['pressure']=_linear_pressure(s['pressure'],coefficient*(1-.65*s['dust']),-.65*coefficient*dust_rate,linear)
        s['dust']=excursions.clamp(s['dust']+linear*dust_rate)
        if tail>linear:s['pressure']=_linear_pressure(s['pressure'],coefficient*.35,0.,tail-linear)
        s['dust']=excursions.clamp(s['dust']+(tail-linear)*dust_rate)
        for key,rate in (('mesh_wet',.0012),('roof_water',.0007)):
            s[key]=excursions.clamp(s[key]+tail*(rate if wet else -.0002))
        s['spray']*=math.exp(-tail*2);_rotor(s,tail)
    s['pressure']=excursions.clamp(s['pressure']);s['airflow']=excursions.clamp(airflow(s))
    if not reserved:s['active']=False;s['stroke']=0.
    return s['pressure']


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
    work=dict(id=choice,label=s['label'],stage='queue',clock=0.,elapsed=0.,ride_elapsed=0.,done=False,invitation_checked=False,castle_care=True,events=[],fractions={},automatic=bool(plan.get('automatic')),physical_pilot=choice in PHYSICAL_SCORES,source_age=canonical_age(pond.game.duck.growth_stage))
    if choice in AIR_SCORES:work['expected_power_revision']=state(pond.object_state('bounce_house',plan))['power_revision']
    return work

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
        w['inspection']=dict(kind=value,pressure=round(s['pressure'],3),condition=round(obj['condition'],3))
        w.setdefault('inspections',[]).append(copy.deepcopy(w['inspection']))
    elif key=='motor':
        if w.get('power_authority')=='procedure' and w.get('id')=='castle_start' and value=='on':
            value=w.get('restore_motor','on')
            if value not in ('on','auto'):raise ValueError('Invalid restored motor policy')
        s['motor']=value
        if not w.get('automatic') and w.get('power_authority','manual')!='procedure':
            s['power_hold']=value=='off';s['power_revision']+=1
    elif key in MOVING:s['targets'][key]=value
    else:s[key]=value
    w['events'].append(index)
    if w.get('id') in AIR_SCORES:w['expected_power_revision']=s['power_revision']

def advance(pond,plan,dt,r):
    from engine import carnival
    w=plan['carnival_work']
    if carnival.is_air_procedure(plan):
        w.update(interrupted=True,done=True,physical_error='This procedure has no live native session.')
        return False
    spec=ROUTINES[w['id']];obj=pond.object_state('bounce_house',plan);s=state(obj);s['active']=True
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
      motor=s['motor'],player_left_switched_off=s['power_hold'],fan_turning=s['rotor_speed']>0,pressure=round(s['pressure'],2),
      door_open=round(s['door'],2),door_buckled=s['latch']>.5,completed_contacts=len(w['events']),inspection=w.get('inspection'),
      company=pond.minds.model.residents[r['actor']]['name'] if r else None,setting='Both residents stay outside the empty house. Controls and cleaning act only on this placed copy.')
