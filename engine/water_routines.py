"""Water activities follow real placement, arrival, weather and completion."""
import json
from pathlib import Path
from engine import shelters
from engine.visitor_shelters import distance

DATA=Path(__file__).parent/'client/animation'
BLUEPRINTS=json.loads((DATA/'waterworks.json').read_text())
WATER={key:spec for key,spec in BLUEPRINTS.items() if spec['type']!='mat'}
ROUTINES=json.loads((DATA/'water-routines.json').read_text())

def eligible(pond,item,spec,ref=None):
    p=WATER[item];e=pond.state['ecology'];n=pond.game.duck.needs
    stage=pond.game.duck.growth_stage
    if stage=='egg' or any(word in pond.weather_type for word in ('storm','blizzard')):return False
    frozen=not p.get('heated') and e.get('ice',0)>.3
    gate=spec['when'];wet=spec['mode'] in ('swim','soak','wade','spray','sip')
    if frozen and not gate.get('frozen'):return False
    if wet and not p.get('heated') and e['temperature']<8:return False
    flags=dict(shallow=p.get('shallow',False) and p['type']!='bowl',swim=p.get('swim',False),
               grown=stage not in ('egg','hatchling','duckling','elder','legendary'),
               tired=n.energy<55,bathing=p.get('shallow',False) and p['type']!='bowl' or p.get('swim',False) and stage not in ('hatchling','duckling'),
               heated=p.get('heated',False),cold=e['temperature']<12,observe=p.get('observe',False),
               bowl=p['type']=='bowl' and pond.object_state(item,ref).get('dirt',0)<.3,
               fountain=p['type']=='fountain',spray=p['type']=='spray',cascade=p['type']=='cascade',
               hot=e['temperature']>=25,rain=any(w in pond.weather_type for w in ('rain','drizzle','shower')),
               night=pond.hour<6 or pond.hour>=19,still=p['type']!='spray',frozen=frozen)
    return all(flags.get(key)==value for key,value in gate.items())

def choose(pond,item,ref=None):
    obj=pond.object_state(item,ref);history=obj.get('water_routines',{});last=obj.get('last_water_routine')
    choices=[key for key,s in ROUTINES.items() if eligible(pond,item,s,ref)]
    if not choices:return None
    # Specific conditions and neglected motions take precedence over repeats.
    def rank(key):
        spec=ROUTINES[key]
        specific=any(k in spec['when'] for k in ('cold','hot','night','rain','frozen','tired','observe','bowl'))
        return (specific, key!=last, -history.get(key,0), spec['mode']!='edge')
    return max(choices,key=rank)

def advance(pond,plan,dt):
    if plan['kind']!='item' or plan['target'] not in WATER or plan['phase']!='act':return False
    item=plan['target'];routine=plan.get('water_routine')
    if routine and routine.get('done'):return False
    if routine and routine.get('id') not in ROUTINES:
        routine.update(done=True,interrupted=True);return False
    if not routine:
        key=choose(pond,item,plan)
        if not key:plan['water_routine']={'done':True,'interrupted':True};return False
        routine={'id':key,'elapsed':0.,'done':False,'label':ROUTINES[key]['label']};plan['water_routine']=routine
    if not eligible(pond,item,ROUTINES[routine['id']],plan) or not shelters.still_placed(pond,{'id':item,'instance':plan.get('instance'),'destination':plan['destination']}) or distance((pond.game.renderer.duck_pos.x,pond.game.renderer.duck_pos.y),plan['destination'])>3:
        routine.update(done=True,interrupted=True);return False
    routine['elapsed']=min(ROUTINES[routine['id']]['duration'],routine['elapsed']+dt)
    pond._cache=None
    if routine['elapsed']>=ROUTINES[routine['id']]['duration']:routine['done']=True;return False
    return True

def complete(pond,plan):
    routine=plan.get('water_routine')
    if not routine or not routine.get('done') or routine.get('interrupted'):return
    obj=pond.object_state(plan['target'],plan);history=obj.setdefault('water_routines',{})
    history[routine['id']]=min(9999,history.get(routine['id'],0)+1)
    obj['last_water_routine']=routine['id']
    pond.remember('item',routine['label']+'.',.35,plan['target'])
    mode=ROUTINES[routine['id']]['mode']
    effects={'edge':{'fun':1.2},'sip':{'energy':.5},'swim':{'cleanliness':1.5,'fun':2,'energy':-.7},
             'wade':{'cleanliness':2,'fun':1},'soak':{'cleanliness':1,'energy':2},
             'spray':{'cleanliness':1,'fun':2.5,'energy':-.3}}[mode]
    for need,amount in effects.items():pond.change_need(need,amount)
    if mode not in ('edge','sip'):obj['wetness']=1
    return mode
