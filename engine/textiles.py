"""Physical mats, living ground patches and stored fibre materials.

The native clock owns folding, impressions, cleaning and weather response.
Handling crafting materials never consumes them, repairs a building or invents
an inventory item. Placed copies retain their own weave and weather history.
"""
import json,math
from pathlib import Path
from engine import shelters
DATA=Path(__file__).parent/'client/animation'
ITEMS=json.loads((DATA/'textiles.json').read_text())
ROUTINES=json.loads((DATA/'textile-routines.json').read_text())
CONTROLS=dict(roll=0.,lift=0.,press=0.,comb=0.,spread=.2,tie=1.,loft=.6,u=.5,v=1.08)
PERSIST=('roll','spread','tie','loft')
def clamp(n):return max(0.,min(1.,n))
def state(item,obj):
    if not isinstance(obj.get('textile'),dict):obj['textile']={}
    s=obj['textile']
    for key,value in dict(roll=0.,spread=.2,tie=1.,loft=.6,fringe=.5,nap=.5,frost=0.).items():
        n=s.get(key,value);s[key]=clamp(n) if isinstance(n,(int,float)) and math.isfinite(n) else value
    for key in ('care','studies','sorts'):
        n=s.get(key,0);s[key]=max(0,min(9999,int(n))) if isinstance(n,(int,float)) and math.isfinite(n) else 0
    tracks=s.get('tracks',[])
    s['tracks']=[{k:clamp(t[k]) for k in ('u','v')} for t in tracks[-8:] if isinstance(t,dict) and all(isinstance(t.get(k),(int,float)) and math.isfinite(t[k]) for k in ('u','v'))] if isinstance(tracks,list) else []
    return s

def wet(pond):return pond.weather_type not in ('rainbow','leaf_storm') and any(w in pond.weather_type for w in ('rain','storm','shower','drizzle','sleet','snow','blizzard','hail'))
def update(pond,item,obj,dt,outdoors,wet=False,intensity=.7,temperature=15):
    if item not in ITEMS or not outdoors:return
    s=state(item,obj)
    target=1. if temperature<=0 and wet else 0.
    s['frost']+=(target-s['frost'])*(1-math.exp(-max(0,dt)/(180 if target else 500)))
    if ITEMS[item]['type'] in ('turf','moss'):s['nap']+=(.65-s['nap'])*(1-math.exp(-max(0,dt)/1200))

def choose(pond,item,ref):
    p=ITEMS[item];obj=pond.object_state(item,ref);s=state(item,obj);age=pond.game.duck.growth_stage;small=age in ('hatchling','duckling')
    kind=p['type'];n=obj.get('uses',0)
    if s['frost']>.35:key='frost_sweep' if kind in ('turf','moss','mat','rubber') else 'rolled_inspect'
    elif wet(pond) and kind in ('mat','scrap','bundle'):key='mat_roll' if kind in ('mat','scrap') and s['roll']<.9 else 'rolled_inspect'
    elif kind in ('mat','scrap') and s['roll']>.05:key='mat_unroll'
    elif kind=='scrap':key='lint_brush' if obj.get('dirt',0)>.25 else 'scrap_fold'
    elif kind=='bundle':key='batting_fluff' if p['style']=='batting' else 'reed_sort' if n%2==0 or s['tie']<.7 else 'binding_check'
    elif kind=='rubber':key='rubber_drain' if obj.get('wetness',0)>.3 else 'welcome_wipe' if pond.game.duck.needs.cleanliness<70 else 'young_steps' if small else ('rubber_press','rubber_bounce')[n%2]
    elif kind=='turf':key='grass_dew' if obj.get('wetness',0)>.2 else 'young_steps' if small else 'elder_settle' if age in ('elder','legendary') else 'soft_loaf' if pond.state['ecology']['temperature']>24 else ('grass_tracks','night_listen' if pond.hour<6 or pond.hour>=19 else 'soft_loaf')[n%2]
    elif kind=='moss':key='moss_probe' if obj.get('wetness',0)>.5 else 'young_steps' if small else ('moss_pat','soft_loaf')[n%2]
    elif obj.get('dirt',0)>.25:key='lint_brush'
    elif small:key='young_steps'
    elif age in ('elder','legendary'):key='elder_settle'
    elif pond.hour<6 or pond.hour>=19:key='night_listen'
    else:
        own={'runner':'runner_parade','tatami':'tatami_grain','medallion':'medallion_trace','coir':'welcome_wipe','patchwork':'soft_loaf','braid':'weave_tighten'}[p['style']]
        key=(own,'corner_smooth','fringe_comb' if p['style'] in ('runner','medallion','patchwork','braid') else 'edge_shake')[n%3]
    pos=pond.game.renderer.duck_pos
    return dict(id=key,elapsed=0.,done=False,events=[],start={k:s.get(k,v) for k,v in CONTROLS.items()},origin=[pos.x,pos.y],label=ROUTINES[key]['label'])

def valid(pond,plan):
    item=plan['target'];work=plan.get('textile_work',{});obj=pond.object_state(item,plan)
    if item not in ITEMS or item not in pond.owned or obj is None or work.get('id') not in ROUTINES or ITEMS[item]['type'] not in ROUTINES[work['id']]['types']:return False
    if plan.get('instance'):return shelters.still_placed(pond,dict(id=item,instance=plan['instance'],destination=plan.get('destination')))
    return ITEMS[item]['portable'] and not obj.get('_source')

def controls(work):
    spec=ROUTINES[work['id']];p=clamp(work['elapsed']/spec['duration']);a,b=spec['track'][0],spec['track'][-1]
    for i in range(1,len(spec['track'])):
        if p<=spec['track'][i][0]:a,b=spec['track'][i-1:i+1];break
    u=clamp((p-a[0])/max(.001,b[0]-a[0]));u=u*u*(3-2*u);start={**CONTROLS,**work.get('start',{})}
    initial_roll=start['roll']
    if work['id'] in ('mat_roll','mat_unroll'):start['roll']=0. if work['id']=='mat_roll' else 1.
    values={k:a[1].get(k,start[k])+(b[1].get(k,start[k])-a[1].get(k,start[k]))*u for k in CONTROLS}
    if work['id']=='mat_roll':values['roll']=initial_roll+(1-initial_roll)*values['roll']
    if work['id']=='mat_unroll':values['roll']*=initial_roll
    return values

def advance(pond,plan,dt):
    work=plan.get('textile_work')
    if not work or work.get('done') or plan['phase']!='act':return False
    pos=pond.game.renderer.duck_pos;dest=plan.get('destination',work['origin'])
    if not valid(pond,plan) or abs(pos.x-dest[0])+abs(pos.y-dest[1])>3:work.update(done=True,interrupted=True);return False
    item=plan['target'];kind=ITEMS[item]['type'];obj=pond.object_state(item,plan);s=state(item,obj)
    if wet(pond) and kind in ('mat','scrap','bundle') and work['id'] not in ('mat_roll','rolled_inspect') and not work.get('withdrawal'):
        if kind=='bundle':work.update(done=True,interrupted=True);return False
        work.update(id='mat_roll',elapsed=0.,events=[],start=controls(work),withdrawal=True,label=ROUTINES['mat_roll']['label']);plan['label']=work['label']
    from engine import textile_company
    if not work.get('withdrawal') and textile_company.waiting(pond.minds):return True
    spec=ROUTINES[work['id']];before=work['elapsed'];work['elapsed']=min(spec['duration'],before+max(0.,dt));values=controls(work)
    for key in PERSIST:s[key]=values[key]
    for i,(at,event) in enumerate(spec['events']):
        if i in work['events'] or work['elapsed']<at*spec['duration']:continue
        work['events'].append(i)
        if event=='smooth':s['nap']=min(1.,s['nap']+.2);s['care']=min(9999,s['care']+1)
        elif event=='comb':s['fringe']=min(1.,s['fringe']+.2)
        elif event=='clean':obj['dirt']=max(0.,obj.get('dirt',0)-.2)
        elif event=='drain':obj['wetness']=max(0.,obj.get('wetness',0)-.25)
        elif event=='frost':s['frost']=max(0.,s['frost']-.4)
        elif event=='wipe':
            amount=min(.4,max(0,100-pond.game.duck.needs.cleanliness));pond.change_need('cleanliness',amount);obj['dirt']=min(1.,obj.get('dirt',0)+amount*.04)
        if event in ('track','wipe'):
            at_work={**work,'elapsed':at*spec['duration']};foot=controls(at_work)
            s['tracks']=(s['tracks']+[dict(u=clamp(foot['u']),v=clamp(foot['v']))])[-8:];s['nap']=max(0.,s['nap']-.04)
    work['done']=work['elapsed']>=spec['duration']
    if work['done'] and work.get('withdrawal'):work['interrupted']=True
    pond._cache=None
    return not work['done']

def complete(pond,plan):
    work=plan.get('textile_work')
    if not work or not work.get('done') or work.get('interrupted') or work.get('recorded') or not valid(pond,plan):return
    work['recorded']=True;obj=pond.object_state(plan['target'],plan);s=state(plan['target'],obj);events={e for _,e in ROUTINES[work['id']]['events']}
    for event,key in [('study','studies'),('sort','sorts')]:
        if event in events:s[key]=min(9999,s[key]+1)
    if 'rest' in events and obj.get('wetness',0)<.35 and s['frost']<.2:pond.change_need('energy',2)
    history=obj.setdefault('textile_routines',{});history[work['id']]=min(9999,history.get(work['id'],0)+1)
    pond.remember('belongings',work['label']+'.',.45,plan['target'])

def conversation(pond,plan):
    if not plan or not plan.get('textile_work') or not valid(pond,plan):return None
    item=plan['target'];obj=pond.object_state(item,plan);s=obj['textile'];p=ITEMS[item]
    result=dict(object=item.replace('_',' '),activity=plan['textile_work']['label'],phase=plan['phase'],paused=bool(plan.get('paused')),material=p['material'])
    pos=pond.game.renderer.duck_pos;dest=plan.get('destination',plan['textile_work']['origin'])
    if plan['phase']=='approach' or abs(pos.x-dest[0])+abs(pos.y-dest[1])>3:return result
    result.update(rolled=round(s['roll'],2),dampness=round(obj.get('wetness',0),2),frost=round(s['frost'],2),footprints=len(s['tracks']),completed_studies=s['studies'])
    if p['type'] in ('bundle','scrap'):result['materials']='Handling the existing material; no crafting, consumption or repair has occurred.'
    if p['style']=='coir':result['visible_words']='QUACK-OME!'
    return result
