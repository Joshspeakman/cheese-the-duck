"""Per-physical-copy light controls. Rendering never operates a switch or timer."""
import json
import math
from pathlib import Path
from engine import shelters

DATA=Path(__file__).parent/'client/animation'
LIGHTS=json.loads((DATA/'lighting.json').read_text())
ROUTINES=json.loads((DATA/'lighting-routines.json').read_text())
MODES=('auto','on','off')

def dusk(hour):
    h=hour%24
    return 1. if h<5 else (7-h)/2 if h<7 else 0. if h<17 else (h-17)/2 if h<19 else 1.

def output(item,mode,hour=12,season='spring',wet=False,intensity=.7):
    p=LIGHTS[item]
    level=1. if p['style']=='eternal' else 1. if mode=='on' else 0. if mode=='off' else dusk(hour)
    if p['type']=='fireflies':level=dusk(hour)*(.12 if season=='winter' else 1.)
    if p.get('exposed') and wet:level*=max(.08,1-intensity*.92)
    return max(0.,min(1.,level))

def state(item,obj,hour=12,season='spring'):
    p=LIGHTS[item];s=obj.setdefault('lighting',{})
    mode=s.get('mode','on' if p['style']=='eternal' else 'auto')
    if mode not in MODES:mode='auto'
    if p['control']=='observe':mode='on' if p['style']=='eternal' else 'auto'
    s['mode']=mode
    for k,v in dict(level=output(item,mode,hour,season),heat=0.,switches=0,operating_seconds=0.).items():
        if not isinstance(s.get(k),(int,float)) or not math.isfinite(s[k]):s[k]=v
    s['level']=max(0.,min(1.,s['level']));s['heat']=max(0.,min(1.,s['heat']))
    return s

def update(pond,item,obj,dt,outdoors,wet=False,intensity=.7):
    if item not in LIGHTS:return
    s=state(item,obj,getattr(pond,'hour',12),getattr(pond,'season','spring'));p=LIGHTS[item]
    target=output(item,s['mode'],pond.hour,pond.season,wet,intensity) if outdoors else 0.
    # Stable exponential response is independent of frame rate. Stored items
    # retain their chosen mode without accumulating operation or lighting a room.
    s['level']+=(target-s['level'])*(1-math.exp(-dt/(3 if p['type'] in ('fire','torch','lava') else .7)))
    s['heat']+=((s['level'] if p['type'] in ('fire','torch','candles','lava') else 0.)-s['heat'])*(1-math.exp(-dt/20))
    if outdoors:s['operating_seconds']=min(1e9,s['operating_seconds']+dt*target)

def make_work(pond,item,ref,mode=None):
    p=LIGHTS[item];s=state(item,pond.object_state(item,ref),pond.hour,pond.season)
    young=pond.game.duck.growth_stage in ('egg','hatchling','duckling')
    if p['control']=='observe' or young and p.get('exposed'):
        key=('firefly_watch' if s['level']>.15 else 'firefly_rest') if p['type']=='fireflies' else ('warm_wings' if s['level']>.15 or s['heat']>.2 else 'unlit_inspect');mode=None
    else:
        mode=mode or ('off' if s['level']>.4 else 'on')
        key='pull_chain' if p['type']=='shade' and p['style']!='gooseneck' else 'shade_shutter' if p['control']=='shutter' else 'turn_wick' if p['control']=='wick' else 'switch_click'
        if p['type']=='fire':key='bank_coals' if mode=='off' else 'fan_embers'
    return dict(id=key,elapsed=0.,done=False,changed=False,mode=mode,label=ROUTINES[key]['label'])

def request(pond,item,mode,instance=None):
    if item not in LIGHTS or mode not in MODES:return False,'Choose an available light setting.'
    p=LIGHTS[item]
    if p['control']=='observe':return False,'Fireflies choose their own rhythm.' if p['type']=='fireflies' else 'The eternal flame keeps its own light.'
    if p.get('exposed') and pond.game.duck.growth_stage in ('egg','hatchling','duckling'):
        return False,'Little Cheese can watch this light, but leaves its controls alone.'
    ok,message=pond.start('item',item,instance=instance)
    if not ok:return ok,message
    plan=pond.state['plan'];plan['light_work']=make_work(pond,item,plan,mode);plan['label']=plan['light_work']['label']
    return True,plan['label']+'.'

def advance(pond,plan,dt):
    work=plan.get('light_work')
    if not work or work.get('done') or plan['phase']!='act':return False
    spec=ROUTINES.get(work.get('id'))
    if not spec or not shelters.still_placed(pond,dict(id=plan['target'],instance=plan.get('instance'),destination=plan.get('destination'))):
        work.update(done=True,interrupted=True);return False
    pos=pond.game.renderer.duck_pos;dest=plan['destination']
    if abs(pos.x-dest[0])+abs(pos.y-dest[1])>3:
        work.update(done=True,interrupted=True);return False
    work['elapsed']=min(spec['duration'],work['elapsed']+dt)
    if work.get('mode') in MODES and not work['changed'] and work['elapsed']>=spec['contact']:
        s=state(plan['target'],pond.object_state(plan['target'],plan),pond.hour,pond.season)
        if s['mode']!=work['mode']:s['mode']=work['mode'];s['switches']+=1
        work['changed']=True
    work['done']=work['elapsed']>=spec['duration'];pond._cache=None
    return not work['done']

def complete(pond,plan):
    work=plan.get('light_work')
    if not work or not work.get('done') or work.get('interrupted') or work.get('recorded'):return
    work['recorded']=True
    obj=pond.object_state(plan['target'],plan);history=obj.setdefault('light_routines',{})
    history[work['id']]=min(9999,history.get(work['id'],0)+1)
    pond.remember('light',work['label']+'.',.4,plan['target'])
