"""Native reading/sorting actions; never redeem rewards or fabricate inventory."""
import json,math
from pathlib import Path
from engine import shelters,glass_curios
DATA=Path(__file__).parent/'client/animation'
ITEMS=json.loads((DATA/'keepsakes.json').read_text())
ROUTINES=json.loads((DATA/'keepsake-routines.json').read_text())

def state(item,obj):
    p=ITEMS[item];s=obj.setdefault('keepsake',{})
    defaults=dict(open=1. if p['style']=='charcoal' else 0.,page=0,bookmark=0,studies=0,sorted=0)
    if p['type']=='barrel':defaults['litres']=0.
    for k,v in defaults.items():
        if not isinstance(s.get(k),(int,float)) or not math.isfinite(s[k]):s[k]=v
    s['open']=max(0.,min(1.,s['open']));s['page']=int(s['page'])%p.get('pages',8);s['bookmark']=int(s['bookmark'])%p.get('pages',8)
    for key in ('studies','sorted'):s[key]=max(0,min(9999,int(s[key])))
    if 'litres' in defaults:s['litres']=max(0.,min(p['capacity'],s['litres']))
    if p['type'] in glass_curios.TYPES:glass_curios.state(s)
    return s

def update(pond,item,obj,dt,outdoors,wet=False,intensity=.7,temperature=15):
    if item not in ITEMS:return
    s=state(item,obj)
    if ITEMS[item]['type'] in glass_curios.TYPES and outdoors:glass_curios.update(s,dt)
    if ITEMS[item]['type']=='barrel':s['frozen']=bool(outdoors and temperature<=0)
    if ITEMS[item]['type']=='barrel' and outdoors and temperature>0:
        # The screened collector catches rain even with the wooden cover down.
        s['litres']=max(0.,min(ITEMS[item]['capacity'],s['litres']+dt*(intensity*.025 if wet else -.00003*max(1,temperature/15))))

def choose(pond,item,ref):
    p=ITEMS[item];obj=pond.object_state(item,ref);s=state(item,obj);age=pond.game.duck.growth_stage
    if p['type'] in glass_curios.TYPES:key=glass_curios.choose(pond,p,obj)
    elif p['type'] in ('paper','map','book') and any(w in pond.weather_type for w in ('rain','storm','shower','drizzle','sleet','snow','blizzard')):key='paper_shelter'
    elif p['type'] in ('paper','map') and pond.state['ecology'].get('wind',0)>.55:key='paper_wind'
    elif p['type']=='barrel':key='barrel_frost' if pond.state['ecology'].get('temperature',15)<=0 else 'barrel_empty' if s['litres']<1 else 'barrel_measure'
    elif p['type']=='chest':key={'pirate':'coin_inspection','joinery':'compartment_sort','weekly':'ribbon_unfold'}[p['style']]
    elif p['type']=='basket':key='basket_sort'
    elif p['type']=='frame':key='glass_polish' if obj.get('dirt',0)>.3 else {'friends':'photo_remember','sunset':'sunset_remember','empty':'frame_corner'}[p['style']]
    elif p['type']=='paper':key='card_read' if p['style']=='card' else 'charcoal_study'
    elif p['type']=='map':key='map_route'
    else:key='book_pictures' if age in ('hatchling','duckling') else 'book_bookmark' if age in ('mature','elder','legendary') else 'book_leaf'
    pos=pond.game.renderer.duck_pos
    return dict(id=key,elapsed=0.,done=False,events=[],start_open=s['open'],origin=[pos.x,pos.y],label=ROUTINES[key]['label'])

def valid(pond,plan):
    item=plan['target'];work=plan.get('keepsake_work',{});obj=pond.object_state(item,plan)
    if item not in ITEMS or item not in pond.owned or obj is None or work.get('id') not in ROUTINES:return False
    if ROUTINES[work['id']].get('types') and ITEMS[item]['type'] not in ROUTINES[work['id']]['types']:return False
    if ITEMS[item]['type'] in glass_curios.TYPES:
        if any(w in pond.weather_type for w in ('storm','blizzard')):return False
        if glass_curios.wet(pond) and ROUTINES[work['id']].get('tool') not in (None,'none'):return False
    if plan.get('instance'):return shelters.still_placed(pond,dict(id=item,instance=plan['instance'],destination=plan.get('destination')))
    return ITEMS[item]['portable'] and not obj.get('_source')

def conversation(pond,plan):
    """Detached, read-only facts about the exact object Cheese has reached.

    Drawings and readable text share a definition with the renderer. Decorative
    coins, maps and chests are never evidence of inventory, gifts or discoveries.
    """
    if not plan or not plan.get('keepsake_work') or not valid(pond,plan):return None
    item=plan['target'];p=ITEMS[item];s=pond.object_state(item,plan).get('keepsake',{})
    result=dict(object=item.replace('_',' '),phase=plan['phase'],paused=bool(plan.get('paused')))
    if plan['phase']=='approach':return result
    pos=pond.game.renderer.duck_pos;dest=plan.get('destination',plan['keepsake_work']['origin'])
    if abs(pos.x-dest[0])+abs(pos.y-dest[1])>3:return result
    opened=s.get('open',0)
    result['completed_readings']=s.get('studies',0)
    if p['type'] in glass_curios.TYPES:
        import copy
        result.update(glass_curios.facts(pond,p,copy.deepcopy(s)))
    elif p['type']=='book':
        result.update(open=opened>.5,page=s.get('page',0)+1,bookmark=s.get('bookmark',0)+1)
        if opened>.5:
            chapter=p['chapters'][s.get('page',0)%p['pages']]
            result.update(chapter=chapter[0],visible_words=' '.join(chapter[1:]))
    elif p['type']=='barrel':
        result.update(litres_collected=round(s.get('litres',0),1),capacity_litres=p['capacity'],frozen=bool(s.get('frozen')))
    elif p['type'] in ('chest','basket'):
        result.update(open=opened>.1,completed_sorts=s.get('sorted',0),contents='Decorative artwork only; inspecting does not grant or reveal inventory.')
    elif p['style']=='card':
        result['open']=opened>.75
        text=p['reading']
        result['visible_words']=' '.join(text['greeting']+[line for line in text['message'] if line]+[text['signature']]) if result['open'] else text['cover']
    elif p['type']=='frame':
        caption=p['caption'];result['visible_words']=' '.join(caption) if isinstance(caption,list) else caption
        result['depicts']={'friends':'A duck and a person; their identities and the occasion are unspecified.',
                           'sunset':'A sun setting over water and reeds.',
                           'empty':'An empty picture frame with corner mounts; no photograph has been inserted.'}[p['style']]
    elif opened>.5:
        result['visible_words']=p['caption']+(' / '+p['question'] if p['type']=='map' else '')
        result['depicts']='An illustrated coast with a compass and dotted route; this is not a discovered treasure or an active quest.' if p['type']=='map' else 'A charcoal drawing of storm clouds, lightning, rain and water.'
    return result

def openness(work,spec):
    progress=min(1.,work['elapsed']/spec['duration']);track=spec['track']
    a,b=track[0],track[-1]
    for i in range(1,len(track)):
        if progress<=track[i][0]:a,b=track[i-1:i+1];break
    u=max(0.,min(1.,(progress-a[0])/max(.001,b[0]-a[0])));u=u*u*(3-2*u)
    start=work['start_open'];return a[1].get('open',start)+(b[1].get('open',start)-a[1].get('open',start))*u

def advance(pond,plan,dt):
    work=plan.get('keepsake_work')
    if not work or work.get('done') or plan['phase']!='act':return False
    if not valid(pond,plan):work.update(interrupted=True,done=True);return False
    pos=pond.game.renderer.duck_pos;destination=plan.get('destination',work['origin'])
    if abs(pos.x-destination[0])+abs(pos.y-destination[1])>3:work.update(interrupted=True,done=True);return False
    from engine import keepsake_company
    if keepsake_company.waiting(pond.minds):return True
    spec=ROUTINES[work['id']];work['elapsed']=min(spec['duration'],work['elapsed']+dt)
    obj=pond.object_state(plan['target'],plan);s=state(plan['target'],obj);s['open']=openness(work,spec)
    for i,(at,event) in enumerate(spec.get('events',[])):
        if work['elapsed']<at*spec['duration'] or i in work['events']:continue
        work['events'].append(i)
        if event=='page':s['page']=(s['page']+1)%ITEMS[plan['target']].get('pages',8)
        elif event=='bookmark':s['bookmark']=s['page']
        elif event=='polish':obj['dirt']=max(0.,obj['dirt']-.2)
        elif ITEMS[plan['target']]['type'] in glass_curios.TYPES:glass_curios.contact(pond,s,event)
        # Practice counts are awarded only on full completion below.
    work['done']=work['elapsed']>=spec['duration'];pond._cache=None
    return not work['done']

def complete(pond,plan):
    work=plan.get('keepsake_work')
    if not work or not work.get('done') or work.get('interrupted') or work.get('recorded') or not valid(pond,plan):return
    work['recorded']=True;obj=pond.object_state(plan['target'],plan);s=state(plan['target'],obj)
    events=[e for _,e in ROUTINES[work['id']].get('events',[])]
    for event,key in [('study','studies'),('tidy','sorted')]:
        if event in events:s[key]=min(9999,s[key]+1)
    history=obj.setdefault('keepsake_routines',{});history[work['id']]=min(9999,history.get(work['id'],0)+1)
    pond.remember('keepsake',work['label']+'.',.5,plan['target'])
    from engine import keepsake_company
    keepsake_company.complete(pond.minds,plan)

def request(pond,item,choice,instance=None):
    if not isinstance(item,str) or not isinstance(choice,str):return False,'Choose an action on this glass keepsake.'
    p=ITEMS.get(item,{});spec=ROUTINES.get(choice,{})
    if p.get('type') not in glass_curios.TYPES or p.get('type') not in spec.get('types',()):return False,'Choose an action on this glass keepsake.'
    if pond.game.duck.growth_stage in ('egg','hatchling','duckling') and spec.get('tool') not in (None,'none'):return False,'Little Cheese watches the tiny details and leaves the controls for later.'
    if any(w in pond.weather_type for w in ('storm','blizzard')):return False,'Cheese leaves the glass keepsakes alone while the storm passes.'
    if glass_curios.wet(pond) and spec.get('tool') not in (None,'none'):return False,'Cheese waits for dry weather before handling the controls.'
    ok,message=pond.start('item',item,instance=instance)
    if not ok:return ok,message
    plan=pond.state['plan'];plan['keepsake_work'].update(id=choice,label=spec['label']);plan['label']=spec['label'];pond._cache=None
    return True,spec['label']

def release(item,obj):
    """Spring-loaded pads release when the wing leaves; circulation remains."""
    if obj is not None and ITEMS.get(item,{}).get('type') in glass_curios.TYPES:
        state(item,obj)['open']=0.
