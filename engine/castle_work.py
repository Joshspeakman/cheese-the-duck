"""Physical controls and fabric care for the actual placed bounce house."""
import copy,json,math
from pathlib import Path
from engine import excursions
ROUTINES=json.loads((Path(__file__).parent/'client/animation/castle-care.json').read_text())
DEFAULTS=dict(vent=0.,door=0.,latch=0.,tie_left=.8,tie_right=.8,apron=0.,flag=1.,hose=0.,kink=0.,dust=0.,mesh_wet=0.,roof_water=0.,prints=0.)
MOVING=('vent','door','tie_left','tie_right','apron','flag','hose','kink')

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
    return dict(id=choice,label=s['label'],stage='queue',clock=0.,elapsed=0.,ride_elapsed=0.,done=False,invitation_checked=False,castle_care=True,events=[],fractions={},automatic=bool(plan.get('automatic')))

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
