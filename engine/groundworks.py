"""Native material contact for paths, floor panels and a crafting plank.

Handling changes only the selected physical copy. Snow, frost, footprints and
sand furrows are saved state; rendering never advances them or crafts a reward.
"""
import json,math
from pathlib import Path
from engine import shelters
DATA=Path(__file__).parent/'client/animation'
ITEMS=json.loads((DATA/'groundworks.json').read_text())
ROUTINES=json.loads((DATA/'ground-routines.json').read_text())
COMPANY=json.loads((DATA/'ground-company.json').read_text())
CONTROLS=dict(u=.5,v=1.1,press=0.,sweep=0.)
def finite(n,default=0.):return n if isinstance(n,(int,float)) and math.isfinite(n) else default
def clamp(n):return max(0.,min(1.,finite(n)))
def state(item,obj):
    if not isinstance(obj.get('ground'),dict):obj['ground']={}
    s=obj['ground']
    for key,default in dict(frost=0.,powder=.75,phase=0.).items():
        s[key]=clamp(finite(s.get(key),default)) if key!='phase' else finite(s.get(key))%(math.pi*20)
    for key in ('studies','taps','care'):
        s[key]=max(0,min(9999,int(finite(s.get(key)))))
    for key,limit,fields in [('tracks',12,('u','v','life')),('furrows',6,('v','life'))]:
        data=s.get(key,[])
        entries=[d for d in data[-limit:] if isinstance(d,dict) and all(isinstance(d.get(k,1.),(int,float)) and math.isfinite(d.get(k,1.)) for k in fields) and 'v' in d and (key!='tracks' or 'u' in d)] if isinstance(data,list) else []
        s[key]=[]
        for d in entries:
            mark={k:clamp(d.get(k,1.)) for k in fields};mark['by']=str(d.get('by','cheese'))[:80]
            if key=='furrows':mark.update(u0=clamp(d.get('u0',.31)),u1=clamp(d.get('u1',.79)))
            else:mark['shape']=d.get('shape') if d.get('shape') in ('webbed','small','talon','toad') else 'webbed'
            s[key].append(mark)
    return s
def footprint(item,obj,u,v,actor='cheese',species='duck',young=False):
    kind=ITEMS[item]['type'];s=state(item,obj)
    if species=='butterfly':return
    shape='small' if young else 'talon' if species in ('crow','owl') else 'toad' if species=='toad' else 'webbed'
    if kind in ('sand','snow') or obj.get('wetness',0)>.15:s['tracks']=(s['tracks']+[dict(u=clamp(u),v=clamp(v),life=1.,by=actor,shape=shape)])[-12:]
    if kind=='snow':s['powder']=max(0.,s['powder']-(.015 if young else .035 if species=='toad' else .03 if species=='goose' else .025))
def wet(pond):return pond.weather_type not in ('rainbow','leaf_storm') and any(w in pond.weather_type for w in ('rain','storm','shower','drizzle','sleet','snow','blizzard','hail'))
def update(pond,item,obj,dt,outdoors,wet=False,intensity=.7,temperature=15,snow=False):
    if item not in ITEMS or not outdoors:return
    s=state(item,obj);dt=max(0.,finite(dt));kind=ITEMS[item]['type']
    if kind in ('cloud','lava','galaxy'):s['phase']=(s['phase']+dt*.12)%(math.pi*20)
    if kind not in ('lava','cloud','rainbow','galaxy','plank'):
        target=1. if temperature<=0 and (wet or snow) else 0.
        s['frost']+=(target-s['frost'])*(1-math.exp(-dt/(240 if target else 650)))
    if kind=='snow':
        target=1. if snow and temperature<=2 else .05 if temperature>2 else s['powder']
        s['powder']+=(target-s['powder'])*(1-math.exp(-dt/(300 if target==1 else 1800)))
    # Rain washes the actual trail away; fresh snow fills old impressions.
    rate=(1/240 if wet and kind=='sand' else 1/180 if snow and kind=='snow' else 1/900 if wet else 1/1800)
    for key in ('tracks','furrows'):
        for mark in s[key]:mark['life']=max(0.,mark['life']-dt*rate)
        s[key]=[mark for mark in s[key] if mark['life']>0]
def choose(pond,item,ref):
    p=ITEMS[item];obj=pond.object_state(item,ref);s=state(item,obj);age=pond.game.duck.growth_stage;kind=p['type'];n=obj.get('uses',0)
    own={'stepping':('stone_cross','stone_trace'),'winding':('winding_walk','stone_trace'),'cobbles':('cobble_seams','stone_trace'),'pebbles':('pebble_listen','stone_trace'),'slate':('slate_layers','seam_brush'),'marble':('marble_vein','marble_buff'),'checker':('checker_steps','seam_brush'),'mosaic':('mosaic_spiral','seam_brush'),'ice':('ice_test','ice_bubbles'),'glass':('glass_reflection','glass_wipe'),'deck':('board_knock','nail_inspect','wood_grain'),'plank':('wood_grain','board_knock'),'sand':('sand_rake','sand_tracks','sand_smooth'),'snow':('snow_crunch','snow_crystal'),'cloud':('cloud_watch',),'rainbow':('rainbow_trace',),'lava':('lava_edge',),'galaxy':('galaxy_orbit',)}[p['style']]
    key=own[n%len(own)]
    # Narrow stones have their own exact footholds; don't replace them with a
    # generic floor walk that would put a duck into a gap between the stones.
    narrow=p['style'] in ('stepping','winding')
    if kind in ('lava','cloud','rainbow','galaxy','plank'):pass
    elif s['frost']>.35:key='frost_edge'
    elif (wet(pond) or obj.get('wetness',0)>.5) and kind in ('stones','tiles','wood','glass','sand'):key='wet_footing'
    elif narrow:key=own[0]
    elif obj.get('dirt',0)>.45 and kind in ('stones','tiles','wood','glass'):key='seam_brush'
    elif age in ('hatchling','duckling') and kind!='ice':key='young_footing'
    elif age in ('elder','legendary') and kind!='ice':key='elder_footing'
    elif pond.hour<6 or pond.hour>=19:key='night_surface'
    elif kind=='snow' and s['powder']<.2:key='snow_crystal'
    elif kind=='sand' and len(s['tracks'])>=8:key='sand_smooth'
    pos=pond.game.renderer.duck_pos
    return dict(id=key,elapsed=0.,done=False,events=[],origin=[pos.x,pos.y],label=ROUTINES[key]['label'])
def valid(pond,plan):
    item=plan['target'];work=plan.get('ground_work',{});obj=pond.object_state(item,plan)
    if item not in ITEMS or item not in pond.owned or obj is None or work.get('id') not in ROUTINES or ITEMS[item]['type'] not in ROUTINES[work['id']]['types']:return False
    if plan.get('instance'):return shelters.still_placed(pond,dict(id=item,instance=plan['instance'],destination=plan.get('destination')))
    return ITEMS[item]['portable'] and not obj.get('_source')
def sample(work,track,base):
    p=clamp(work['elapsed']/ROUTINES[work['id']]['duration']);a,b=track[0],track[-1]
    for i in range(1,len(track)):
        if p<=track[i][0]:a,b=track[i-1:i+1];break
    u=clamp((p-a[0])/max(.001,b[0]-a[0]));u=u*u*(3-2*u)
    return {k:a[1].get(k,value)+(b[1].get(k,value)-a[1].get(k,value))*u for k,value in base.items()}
def controls(work):
    duet=COMPANY.get(work.get('duet'),{});track=duet.get('lead',ROUTINES[work['id']]['track'])
    pose=sample(work,track,{**CONTROLS,**work.get('start',{})})
    if duet.get('layout')=='lanes':pose['u']=.08+.4*pose['u']
    return pose
def advance(pond,plan,dt):
    work=plan.get('ground_work')
    if not work or work.get('done') or plan['phase']!='act':return False
    pos=pond.game.renderer.duck_pos;dest=plan.get('destination',work['origin'])
    if not valid(pond,plan) or abs(pos.x-dest[0])+abs(pos.y-dest[1])>3:work.update(done=True,interrupted=True);return False
    item=plan['target'];kind=ITEMS[item]['type'];obj=pond.object_state(item,plan);s=state(item,obj)
    if wet(pond) and kind in ('stones','tiles','wood','glass','sand') and work['id'] not in ('wet_footing','frost_edge'):
        start=controls(work);work.update(id='wet_footing',elapsed=0.,events=[],start=start,duet=None,withdrawal=True,label=ROUTINES['wet_footing']['label']);plan['label']=work['label']
    from engine import ground_company
    if not work.get('withdrawal') and ground_company.waiting(pond.minds):return True
    spec=ROUTINES[work['id']];work['elapsed']=min(spec['duration'],work['elapsed']+max(0.,dt))
    for i,(at,event) in enumerate(spec['events']):
        if i in work['events'] or work['elapsed']<at*spec['duration']:continue
        work['events'].append(i)
        if event=='clean':obj['dirt']=max(0.,obj.get('dirt',0)-.18);s['care']=min(9999,s['care']+1)
        elif event=='smooth':
            lanes=COMPANY.get(work.get('duet'),{}).get('layout')=='lanes'
            s['tracks']=[t for t in s['tracks'] if lanes and t['u']>=.6];s['furrows']=[t for t in s['furrows'] if lanes and t['u0']>=.6];s['care']=min(9999,s['care']+1)
        elif event=='tap':s['taps']=min(9999,s['taps']+1)
        elif event in ('track','furrow'):
            foot=controls({**work,'elapsed':at*spec['duration']})
            if event=='furrow':
                lanes=COMPANY.get(work.get('duet'),{}).get('layout')=='lanes'
                s['furrows']=(s['furrows']+[dict(u0=.258 if lanes else .31,u1=.45 if lanes else .79,v=clamp(foot['v']-.12),life=1.,by='cheese')])[-6:]
            else:
                # Impressions on snow/sand, wet footprints on a hard surface.
                footprint(item,obj,foot['u'],foot['v'],young=pond.game.duck.growth_stage in ('hatchling','duckling'))
    work['done']=work['elapsed']>=spec['duration']
    if work['done'] and work.get('withdrawal'):work['interrupted']=True
    pond._cache=None
    return not work['done']
def complete(pond,plan):
    work=plan.get('ground_work')
    if not work or not work.get('done') or work.get('interrupted') or work.get('recorded') or not valid(pond,plan):return
    work['recorded']=True;obj=pond.object_state(plan['target'],plan);s=state(plan['target'],obj)
    if any(e=='study' for _,e in ROUTINES[work['id']]['events']):s['studies']=min(9999,s['studies']+1)
    history=obj.setdefault('ground_routines',{});history[work['id']]=min(9999,history.get(work['id'],0)+1)
    pond.remember('belongings',work['label']+'.',.45,plan['target'])
def conversation(pond,plan):
    if not plan or not plan.get('ground_work') or not valid(pond,plan):return None
    item=plan['target'];obj=pond.object_state(item,plan);s=obj['ground'];p=ITEMS[item]
    result=dict(object=item.replace('_',' '),activity=plan['ground_work']['label'],phase=plan['phase'],paused=bool(plan.get('paused')),material=p['material'])
    pos=pond.game.renderer.duck_pos;dest=plan.get('destination',plan['ground_work']['origin'])
    if plan['phase']=='approach' or abs(pos.x-dest[0])+abs(pos.y-dest[1])>3:return result
    result.update(dampness=round(obj.get('wetness',0),2),frost=round(s['frost'],2),footprints=len(s['tracks']),completed_studies=s['studies'])
    trails={}
    for mark in s['tracks']:
        author=mark.get('by','cheese');entry=trails.setdefault(author,dict(name=pond.minds.model.residents.get(author,{}).get('name','Cheese' if author=='cheese' else 'a previous visitor'),shape=mark.get('shape','webbed'),prints=0));entry['prints']+=1
    if trails:result['footprint_trails']=list(trails.values())
    if p['type']=='sand':result['raked_lines']=len(s['furrows'])
    if p['type']=='snow':result['powder']=round(s['powder'],2)
    if p['type']=='lava':result['position']='Outside the stone lip, watching. Cheese has not touched the molten surface.'
    if p['portable']:result['materials']='Inspecting the existing plank; no crafting, consumption or repair has occurred.'
    return result
