"""Native outdoor playthings: saved controls, contact events and finite soap bubbles."""
import copy,json,math
from pathlib import Path
from engine import shelters
DATA=Path(__file__).parent/'client/animation'
ITEMS=json.loads((DATA/'playkit.json').read_text())
ROUTINES=json.loads((DATA/'playkit-routines.json').read_text())
CONTROLS=dict(travel=0.,lift=0.,turn=0.,coil=0.,power=0.,dip=0.,blow=0.,walk=0.,tilt=0.,jump=0.,drop=1.,held=0.,wide=0.,sail=0.)
def finite(v,d=0.):return float(v) if isinstance(v,(int,float)) and math.isfinite(v) else d
def clamp(v,a=0.,b=1.):return max(a,min(b,finite(v)))
def state(item,obj):
    if not isinstance(obj.get('playkit'),dict):obj['playkit']={}
    s=obj['playkit']
    for k,d in CONTROLS.items():s[k]=clamp(s.get(k,d),-1 if k=='tilt' else 0,100 if k=='turn' else 1)
    for k in ('pushes','retrievals','hops','turns','bubbles_made','cleanings','balances','steps','folds','riggings','waxes','studies'):
        s[k]=int(clamp(s.get(k),0,9999))
    s['phase']=finite(s.get('phase'))%(math.pi*2);s['speed']=clamp(s.get('speed'),0,3);s['bubble_clock']=clamp(s.get('bubble_clock'),0,1.2)
    s['bubbles']=[dict(age=clamp(v.get('age'),0,8),size=clamp(v.get('size',1),.5,2),lane=int(clamp(v.get('lane'),0,4))) for v in s.get('bubbles',[]) if isinstance(v,dict)][-12:] if isinstance(s.get('bubbles'),list) else []
    return s

def wet(pond):return pond.weather_type!='rainbow' and any(w in pond.weather_type for w in ('rain','storm','snow','blizzard','drizzle','shower','hail','sleet'))
def gusty(pond):return any(w in pond.weather_type for w in ('storm','gale','tornado','hurricane','blizzard'))
def bubble(s,size=1.):
    s['bubbles_made']=min(9999,s['bubbles_made']+1)
    s['bubbles'].append(dict(age=0.,size=size,lane=s['bubbles_made']%5));s['bubbles']=s['bubbles'][-12:]
def update(pond,item,obj,dt,outdoors,wind=0.,weather=None):
    if item not in ITEMS:return
    s=state(item,obj);dt=max(0,finite(dt));plan=pond.state.get('plan')
    portable=bool(plan and not plan.get('instance') and plan.get('playkit_work') and plan['target']==item and pond.object_state(item,plan) is obj)
    outdoors=outdoors or portable
    actual=pond.weather_type if portable or weather is None else weather
    adverse=actual!='rainbow' and any(w in actual for w in ('rain','storm','snow','blizzard','drizzle','shower','hail','sleet','gale','tornado','hurricane'))
    if not outdoors:
        s['power']=0;s['speed']=0;s['bubbles']=[];return
    for b in s['bubbles']:b['age']+=dt
    s['bubbles']=[b for b in s['bubbles'] if b['age']<8]
    kind=ITEMS[item]['type']
    if kind=='bubbler':
        if adverse:s['power']=0
        if s['power']>.5:
            s['phase']=(s['phase']+dt*1.7)%(math.pi*2)
            s['bubble_clock']+=dt
            # Long frames age old bubbles; they do not dump a backlog of particles.
            if s['bubble_clock']>=1.2:bubble(s);s['bubble_clock']%=1.2
    elif kind=='pinwheel':
        target=0. if adverse else clamp(wind)*2.4
        decay=math.exp(-2*dt);old=s['speed'];s['speed']=target+(old-target)*decay
        s['phase']=(s['phase']+target*dt+(old-target)*(1-decay)/2)%(math.pi*2)
    if not obj.get('active'):
        s['lift']=max(0,s['lift']-dt*.5)
        if kind=='yoyo':s['drop']=min(1,s['drop']+dt*.6)

def controls(work):
    spec=ROUTINES[work['id']];p=clamp(work['elapsed']/spec['duration']);track=spec['track'];a,b=track[0],track[-1]
    for i in range(1,len(track)):
        if p<=track[i][0]:a,b=track[i-1:i+1];break
    u=clamp((p-a[0])/max(.001,b[0]-a[0]));u=u*u*(3-2*u)
    start={**CONTROLS,**work.get('start',{})}
    return {k:a[1].get(k,v)+(b[1].get(k,v)-a[1].get(k,v))*u for k,v in start.items() if k in CONTROLS}

def choose(pond,item,ref):
    obj=pond.object_state(item,ref);s=state(item,obj);kind=ITEMS[item]['type'];age=pond.game.duck.growth_stage
    pool=[k for k in ROUTINES if ROUTINES[k]['type']==kind and not k.endswith(('_gentle','_pack'))]
    key=pool[obj.get('uses',0)%len(pool)]
    if kind=='bubbler':key='bubbler_stop' if s['power']>.5 else 'bubbler_start'
    if kind=='rope' and s['coil']>.5:key='rope_uncoil'
    quiet=pond.game.duck.needs.energy<35 or age in ('hatchling','duckling','elder','legendary') or pond.hour<6 or pond.hour>=20
    if quiet:key=kind+'_gentle'
    if wet(pond) or gusty(pond):key=kind+'_pack'
    pos=pond.game.renderer.duck_pos
    # Transient movement is a path relative to the current resting location.
    start={**CONTROLS,'power':s['power'],'coil':s['coil'],'sail':s['sail'],'travel':s['travel'],'turn':s['turn']}
    return dict(id=key,label=ROUTINES[key]['label'],elapsed=0.,events=[],done=False,origin=[pos.x,pos.y],start=start)
def valid(pond,plan):
    item=plan['target'];work=plan.get('playkit_work',{});obj=pond.object_state(item,plan)
    if item not in ITEMS or item not in pond.owned or obj is None or work.get('id') not in ROUTINES:return False
    if ROUTINES[work['id']]['type']!=ITEMS[item]['type']:return False
    if plan.get('instance'):return shelters.still_placed(pond,dict(id=item,instance=plan['instance'],destination=plan.get('destination')))
    return ITEMS[item]['portable'] and not obj.get('_source')
def advance(pond,plan,dt):
    work=plan.get('playkit_work')
    if not work or work.get('done') or plan['phase']!='act':return False
    dest=plan.get('destination',work['origin']);pos=pond.game.renderer.duck_pos
    if not valid(pond,plan) or abs(pos.x-dest[0])+abs(pos.y-dest[1])>3:work.update(done=True,interrupted=True);return False
    item=plan['target'];s=state(item,pond.object_state(item,plan));kind=ITEMS[item]['type']
    if (wet(pond) or gusty(pond)) and not work['id'].endswith('_pack'):
        start=controls(work);work.update(id=kind+'_pack',label=ROUTINES[kind+'_pack']['label'],elapsed=0.,events=[],start=start,withdrawal=True);plan['label']=work['label']
    spec=ROUTINES[work['id']];old=work['elapsed'];work['elapsed']=min(spec['duration'],old+max(0,finite(dt)));v=controls(work)
    for k in CONTROLS:s[k]=v[k]
    for i,(at,event) in enumerate(spec['events']):
        if i in work['events'] or work['elapsed']<at*spec['duration']:continue
        work['events'].append(i)
        counter={'push':'pushes','roll':'pushes','retrieve':'retrievals','hop':'hops','step':'steps','spin':'turns','return':'retrievals','fold':'folds','unfold':'folds','rig':'riggings','balance':'balances','watch':'studies','wax':'waxes','clean':'cleanings'}.get(event)
        if counter:s[counter]=min(9999,s[counter]+1)
        if event in ('clean','wax'):obj=pond.object_state(item,plan);obj['dirt']=max(0,obj.get('dirt',0)-.12)
        if event in ('bubble','wide_bubble'):bubble(s,1.7 if event=='wide_bubble' else 1.)
        if event=='nudge':s['phase']=(s['phase']+.9)%(math.pi*2)
    work['done']=work['elapsed']>=spec['duration']
    if work['done'] and work.get('withdrawal'):work['interrupted']=True
    pond._cache=None;return not work['done']
def complete(pond,plan):
    work=plan.get('playkit_work')
    if not work or not work.get('done') or work.get('interrupted') or work.get('recorded') or not valid(pond,plan):return
    work['recorded']=True;obj=pond.object_state(plan['target'],plan);history=obj.setdefault('playkit_routines',{})
    history[work['id']]=min(9999,history.get(work['id'],0)+1)
    pond.remember('belongings',work['label']+'.',.45,plan['target'])
def view(pond,plan):
    work=copy.deepcopy(plan['playkit_work']);p=plan['elapsed']/plan['duration']
    if plan['phase']=='prepare':work['transition']=dict(phase='enter',elapsed=clamp((p-.15)/.13)*2)
    elif plan['phase']=='settle':work['transition']=dict(phase='exit',elapsed=clamp((p-.9)/.1)*2)
    return work
def conversation(pond,plan):
    if not plan or not plan.get('playkit_work') or not valid(pond,plan):return None
    item=plan['target'];work=plan['playkit_work'];result=dict(object=item.replace('_',' '),activity=work['label'],phase=plan['phase'],paused=bool(plan.get('paused')))
    pos=pond.game.renderer.duck_pos;dest=plan.get('destination',work['origin'])
    if plan['phase']=='approach' or abs(pos.x-dest[0])+abs(pos.y-dest[1])>3:return result
    s=pond.object_state(item,plan)['playkit'];result['actual_contacts']=[ROUTINES[work['id']]['events'][i][1] for i in work['events']]
    if ITEMS[item]['type'] in ('bubbler','wand'):result.update(bubbles_visible=len(s['bubbles']),machine_running=s['power']>.5)
    if ITEMS[item]['type']=='pinwheel':result['wind_driven_speed']=round(s['speed'],2)
    if ITEMS[item]['type'] in ('boat','board'):result['setting']='On the bank, not a voyage or surf trip. No fish, water or travel reward.'
    return result


def request(pond,item,choice,instance=None):
    if item not in ITEMS or not isinstance(choice,str) or choice not in ROUTINES or ROUTINES[choice]['type']!=ITEMS[item]['type']:return False,'Choose a game for this plaything.'
    if pond.game.duck.growth_stage in ('egg','hatchling','duckling') and not choice.endswith('_gentle'):return False,'Little Cheese explores this toy gently for now.'
    if (wet(pond) or gusty(pond)) and not choice.endswith('_pack'):return False,'Cheese waits for drier, calmer weather before playing.'
    ok,message=pond.start('item',item,instance=instance)
    if not ok:return ok,message
    plan=pond.state['plan'];work=plan['playkit_work'];work.update(id=choice,label=ROUTINES[choice]['label']);plan['label']=work['label']
    return True,work['label']+'.'
