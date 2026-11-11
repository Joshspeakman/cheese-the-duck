"""Native creative work: physical controls, progressive painting and wind handling.

The paper-plane design remains a material. Practising its folds never consumes
it or manufactures a second inventory object. Each placed copy keeps its state.
"""
import json, math
from pathlib import Path
from engine import shelters
DATA=Path(__file__).parent/'client/animation'
ITEMS=json.loads((DATA/'creative-props.json').read_text())
ROUTINES=json.loads((DATA/'creative-routines.json').read_text())
CONTROLS=dict(aim=.35,focus=.5,cap=1.,fold=0.,cover=0.,flight=0.,stroke=0.)

def clamp(n):return max(0.,min(1.,n))

def state(item,obj):
    if not isinstance(obj.get('creative'),dict):obj['creative']={}
    s=obj['creative']
    for key,default in CONTROLS.items():
        if key in ('flight','stroke'):continue  # These exist only during work.
        v=s.get(key,default)
        s[key]=clamp(v) if isinstance(v,(int,float)) and math.isfinite(v) else default
    for key,limit in [('strokes',12),('observations',9999),('flights',9999),('folds',9999)]:
        n=s.get(key,0);s[key]=max(0,min(limit,int(n))) if isinstance(n,(int,float)) and math.isfinite(n) else 0
    if s.get('motif') not in ('pond','night','autumn','winter'):s['motif']='pond'
    return s

def wet(pond):return pond.weather_type not in ('rainbow','leaf_storm') and any(w in pond.weather_type for w in ('rain','storm','shower','drizzle','sleet','snow','blizzard','hail'))

def wind(pond):return clamp(pond.state['ecology'].get('wind',0))

def choose(pond,item,ref):
    obj=pond.object_state(item,ref);s=state(item,obj);kind=ITEMS[item]['type']
    age=pond.game.duck.growth_stage;small=age in ('hatchling','duckling');w=wind(pond)
    history=obj.get('creative_routines',{})
    if kind=='scope':
        if wet(pond):key='scope_cover'
        elif obj.get('dirt',0)>.3:key='scope_polish'
        elif any(v in pond.weather_type for v in ('cloud','fog','mist','overcast')):key='scope_clouds'
        elif small:key='scope_first_peek'
        else:key='scope_stars' if pond.hour<6 or pond.hour>=19 else 'scope_focus'
    elif kind=='easel':
        if wet(pond) or w>.75:key='paint_cover'
        elif s['cover']>.05:key='paint_uncover'
        elif obj.get('dirt',0)>.3:key='paint_rinse'
        elif s['strokes']>=12:key='paint_study'
        else:key=('paint_sky','paint_bank','paint_ducks','paint_finish')[s['strokes']//3]
    elif kind=='kite':
        if wet(pond) or w>.8:key='kite_tail'
        elif w<.15:key='kite_calm'
        elif obj.get('dirt',0)>.3 or not history.get('kite_tail'):key='kite_tail'
        elif small or age in ('elder','legendary'):key='kite_low_arc'
        else:key='kite_gust' if w>.55 else 'kite_launch'
    else:
        if wet(pond):key='fold_cover'
        elif s['cover']>.05:key='fold_unwrap'
        elif w>.5:key='fold_pin'
        elif small and not history.get('fold_first'):key='fold_first'
        elif s['fold']<.4:key='fold_nose'
        elif s['fold']<.95:key='fold_wings'
        else:key='fold_unfold'
    pos=pond.game.renderer.duck_pos
    motif='night' if pond.hour<6 or pond.hour>=19 else 'autumn' if pond.season in ('fall','autumn') else 'winter' if pond.season=='winter' else 'pond'
    return dict(id=key,elapsed=0.,events=[],done=False,start={k:s.get(k,v) for k,v in CONTROLS.items()},
                origin=[pos.x,pos.y],wind=w,label=ROUTINES[key]['label'],motif=motif)

def valid(pond,plan):
    item=plan['target'];work=plan.get('creative_work',{});obj=pond.object_state(item,plan)
    if item not in ITEMS or item not in pond.owned or obj is None or work.get('id') not in ROUTINES:return False
    if ROUTINES[work['id']]['type']!=ITEMS[item]['type']:return False
    if plan.get('instance'):return shelters.still_placed(pond,dict(id=item,instance=plan['instance'],destination=plan.get('destination')))
    return ITEMS[item]['portable'] and not obj.get('_source')

def controls(work):
    spec=ROUTINES[work['id']];progress=clamp(work['elapsed']/spec['duration']);track=spec['track']
    a,b=track[0],track[-1]
    for i in range(1,len(track)):
        if progress<=track[i][0]:a,b=track[i-1:i+1];break
    u=clamp((progress-a[0])/max(.001,b[0]-a[0]));u=u*u*(3-2*u)
    start={**CONTROLS,**work.get('start',{})}
    result={k:a[1].get(k,start[k])+(b[1].get(k,start[k])-a[1].get(k,start[k]))*u for k in CONTROLS}
    if work['id']=='kite_reel':result['flight']*=start['flight']
    return result

def advance(pond,plan,dt):
    work=plan.get('creative_work')
    if not work or work.get('done') or plan['phase']!='act':return False
    pos=pond.game.renderer.duck_pos;dest=plan.get('destination',work['origin'])
    if not valid(pond,plan) or abs(pos.x-dest[0])+abs(pos.y-dest[1])>3:
        work.update(done=True,interrupted=True);return False
    kind=ITEMS[plan['target']]['type'];w=wind(pond)
    protect={'scope':'scope_cover','easel':'paint_cover','kite':'kite_reel','fold':'fold_cover'}[kind]
    unsafe=wet(pond) or (kind in ('easel','kite') and w>.8) or (kind=='kite' and w<.12 and controls(work)['flight']>.1)
    # A change in weather drives a bounded physical wind-down, not an airborne
    # kite teleport or a successful-use reward for an abandoned painting.
    if unsafe and not work.get('withdrawal') and work['id'] not in ('scope_cover','paint_cover','kite_tail','kite_calm','fold_cover'):
        initial=controls(work)
        work.update(id=protect,start=initial,elapsed=0.,events=[],withdrawal=True,label=ROUTINES[protect]['label'])
        plan['label']=work['label']
    spec=ROUTINES[work['id']];work['wind']=w
    work['elapsed']=min(spec['duration'],work['elapsed']+max(0.,dt))
    obj=pond.object_state(plan['target'],plan);s=state(plan['target'],obj);v=controls(work)
    for key in ('aim','focus','cap','fold','cover'):s[key]=v[key]
    for i,(at,event) in enumerate(spec.get('events',[])):
        if i in work['events'] or work['elapsed']<at*spec['duration']:continue
        work['events'].append(i)
        if event=='stroke':
            if s['strokes']==0:s['motif']=work['motif']
            s['strokes']=min(12,s['strokes']+1)
        elif event=='clean':obj['dirt']=max(0.,obj.get('dirt',0)-.2)
    work['done']=work['elapsed']>=spec['duration']
    if work['done'] and work.get('withdrawal'):work['interrupted']=True
    pond._cache=None
    return not work['done']

def complete(pond,plan):
    work=plan.get('creative_work')
    if not work or not work.get('done') or work.get('interrupted') or work.get('recorded') or not valid(pond,plan):return
    work['recorded']=True;obj=pond.object_state(plan['target'],plan);s=state(plan['target'],obj)
    events=[e for _,e in ROUTINES[work['id']].get('events',[])]
    for event,key in [('observe','observations'),('fly','flights'),('fold','folds')]:
        if event in events:s[key]=min(9999,s[key]+1)
    history=obj.setdefault('creative_routines',{});history[work['id']]=min(9999,history.get(work['id'],0)+1)
    pond.remember('creative',work['label']+'.',.5,plan['target'])

def conversation(pond,plan):
    if not plan or not plan.get('creative_work') or not valid(pond,plan):return None
    item=plan['target'];work=plan['creative_work'];pos=pond.game.renderer.duck_pos;dest=plan.get('destination',work['origin'])
    facts=dict(object=item.replace('_',' '),activity=work['label'],phase=plan['phase'],paused=bool(plan.get('paused')))
    if plan['phase']=='approach' or abs(pos.x-dest[0])+abs(pos.y-dest[1])>3:return facts
    s=pond.object_state(item,plan)['creative'];kind=ITEMS[item]['type']
    if kind=='scope':facts.update(lens_capped=s['cap']>.5,focus=round(s['focus'],2),observations=s['observations'],view='No specific astronomical discovery is established by this interaction.')
    elif kind=='easel':facts.update(painted_layers=s['strokes'],total_layers=12,painting=s['motif'],covered=s['cover']>.5,finished=s['strokes']==12)
    elif kind=='kite':facts.update(airborne=controls(work)['flight']>.15,wind=round(work['wind'],2),completed_flights=s['flights'])
    else:facts.update(folded=s['fold']>.95,fold_progress=round(s['fold'],2),practice_sessions=s['folds'],inventory='Practising with the existing paper-plane design; no new item was made.')
    return facts
