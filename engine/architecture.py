"""Native contact and weather for garden structures; no invented deliveries or loot."""
import json,math,copy
from pathlib import Path
from engine import shelters
DATA=Path(__file__).parent/'client/animation'
ITEMS=json.loads((DATA/'architecture.json').read_text())
ROUTINES=json.loads((DATA/'architecture-routines.json').read_text())
CONTROLS=dict(open=0.,panel=0.,flag=0.,bucket=0.,brake=0.,walk=0.)
def finite(n,default=0.):return n if isinstance(n,(int,float)) and math.isfinite(n) else default
def clamp(n):return max(0.,min(1.,finite(n)))
def state(item,obj):
    if not isinstance(obj.get('architecture'),dict):obj['architecture']={}
    s=obj['architecture']
    for key in CONTROLS:s[key]=clamp(s.get(key,0))
    for key in ('studies','adjustments','cleanings','taps'):s[key]=max(0,min(9999,int(finite(s.get(key)))))
    s['phase']=finite(s.get('phase'))%(math.pi*2);s['speed']=max(0.,min(2.,finite(s.get('speed'))));s['crank']=finite(s.get('crank'))%(math.pi*2)
    for key in ('wind','sun','shadow_length'):s[key]=clamp(s.get(key,0))
    for key in ('bearing','shadow_angle'):s[key]=finite(s.get(key))%(math.pi*2)
    if s.get('season') not in ('spring','summer','fall','winter'):s['season']='spring'
    return s
def gusty(weather):return any(word in weather for word in ('storm','blizzard','hurricane','tornado','gale','thunder'))
def update(pond,item,obj,dt,outdoors,wind=0.,weather='sunny',wind_heading=None):
    if item not in ITEMS or not outdoors:return
    s=state(item,obj);s['season']=pond.season;dt=max(0.,finite(dt))
    kind=ITEMS[item]['type'];s['wind']=clamp(wind)
    if kind in ('flag','scarecrow'):s['phase']=(s['phase']+dt*(.25+clamp(wind)*2))%(math.pi*2)
    if kind=='vane' and wind_heading is not None and wind>.01:
        target=(finite(wind_heading)*math.pi*2)%(math.pi*2);delta=(target-s['bearing']+math.pi)%(math.pi*2)-math.pi
        s['bearing']=(s['bearing']+delta*(1-math.exp(-dt*.8)))%(math.pi*2)
    if kind=='sundial':
        hour=finite(pond.hour,12);day=6<hour<18
        s['sun']=0. if not day or any(w in weather for w in ('rain','storm','snow','blizzard','fog','overcast')) else .35 if 'cloud' in weather else 1.
        s['shadow_angle']=((hour-12)*math.pi/12)%(math.pi*2)
        s['shadow_length']=clamp(.35+abs(hour-12)/9+(.15 if pond.season=='winter' else 0))
    if kind=='windmill':
        # Exposed sails slow under the brake; storms feather them automatically.
        target=0. if gusty(weather) else max(0.,min(1.2,finite(wind)*2))*(1-s['brake'])
        rate=1.4;decay=math.exp(-rate*dt);old=s['speed']
        s['speed']=target+(old-target)*decay
        travel=target*dt+(old-target)*(1-decay)/rate
        s['phase']=(s['phase']+travel)%(math.pi*2)
def sample(work,track,base):
    p=clamp(work['elapsed']/ROUTINES[work['id']]['duration']);a,b=track[0],track[-1]
    for i in range(1,len(track)):
        if p<=track[i][0]:a,b=track[i-1:i+1];break
    u=clamp((p-a[0])/max(.001,b[0]-a[0]));u=u*u*(3-2*u)
    return {k:a[1].get(k,value)+(b[1].get(k,value)-a[1].get(k,value))*u for k,value in base.items()}
def controls(work):
    return sample(work,ROUTINES[work['id']]['track'],{**CONTROLS,**work.get('start',{})})
def wet(pond):return pond.weather_type!='rainbow' and any(w in pond.weather_type for w in ('rain','storm','shower','drizzle','sleet','snow','blizzard','hail'))
def choose(pond,item,ref):
    obj=pond.object_state(item,ref);s=state(item,obj);kind=ITEMS[item]['type'];age=pond.game.duck.growth_stage;n=obj.get('uses',0)
    options={'picket':['picket_knots','picket_brush'],'wall':['wall_layers','wall_moss'],'arch':['arch_trace','arch_shadow'],'bridge':['bridge_cross','bridge_listen'],'watchtower':['watchtower_braces','watchtower_roof'],'windmill':['windmill_turn','windmill_brake' if s['brake']<.5 else 'windmill_release'],'gate':['gate_open' if s['open']<.5 else 'gate_close','gate_hinge'],'pergola':['pergola_shade','pergola_beams'],'mailbox':['mailbox_open' if s['panel']<.5 else 'mailbox_close','mailbox_flag' if s['flag']<.5 else 'mailbox_lower_flag'],'well':['well_lower' if s['bucket']<.5 else 'well_raise','well_echo'],'trellis':['trellis_flowers','trellis_ties'],'castle':['castle_arrowloop','castle_stones'],'ironfence':['iron_scroll','iron_brush'],'gnome':['gnome_greet','gnome_boots'],'statue':['statue_inscription','statue_polish'],'scarecrow':['scarecrow_straw','scarecrow_scarf'],'totem':['totem_faces','totem_grooves'],'sundial':['sundial_shadow' if s['sun']>.1 else 'sundial_cloud','sundial_marks'],'vane':['vane_direction','vane_foot'],'compass':['compass_points','compass_grout'],'flag':['flag_hoist' if s['flag']<.5 else 'flag_salute','flag_lower']}[kind]
    key=options[n%len(options)]
    if gusty(pond.weather_type):key='storm_stepback'
    elif wet(pond):key='rain_drips'
    elif age in ('hatchling','duckling'):key='young_survey'
    elif age in ('elder','legendary') or pond.game.duck.needs.energy<35:key='elder_survey'
    elif pond.hour<6 or pond.hour>=19:key='night_survey'
    pos=pond.game.renderer.duck_pos
    return dict(id=key,elapsed=0.,done=False,events=[],origin=[pos.x,pos.y],start={k:s[k] for k in CONTROLS},start_crank=s['crank'],label=ROUTINES[key]['label'])
def valid(pond,plan):
    item=plan['target'];work=plan.get('architecture_work',{});obj=pond.object_state(item,plan)
    return bool(item in ITEMS and item in pond.owned and obj is not None and work.get('id') in ROUTINES and ITEMS[item]['type'] in ROUTINES[work['id']]['types'] and plan.get('instance') and shelters.still_placed(pond,dict(id=item,instance=plan['instance'],destination=plan.get('destination'))))
def advance(pond,plan,dt):
    work=plan.get('architecture_work')
    if not work or work.get('done') or plan['phase']!='act':return False
    pos=pond.game.renderer.duck_pos;dest=plan['destination']
    if not valid(pond,plan) or abs(pos.x-dest[0])+abs(pos.y-dest[1])>3:work.update(done=True,interrupted=True);return False
    obj=pond.object_state(plan['target'],plan);s=state(plan['target'],obj)
    retreat='storm_stepback' if gusty(pond.weather_type) else 'rain_drips' if wet(pond) else None
    if retreat and work['id'] not in ('storm_stepback','rain_drips'):
        work.update(id=retreat,elapsed=0.,events=[],start=controls(work),withdrawal=True,label=ROUTINES[retreat]['label']);plan['label']=work['label']
    from engine import architecture_company
    if not work.get('withdrawal') and architecture_company.waiting(pond.minds):return True
    spec=ROUTINES[work['id']];old=work['elapsed'];work['elapsed']=min(spec['duration'],old+max(0.,dt));v=controls(work)
    for field in spec['controls']:
        if field!='walk':s[field]=clamp(v[field])
    if 'bucket' in spec['controls']:s['crank']=(work.get('start_crank',0.)+(work['start']['bucket']-v['bucket'])*math.pi*8)%(math.pi*2)
    for i,(at,event) in enumerate(spec['events']):
        if i in work['events'] or work['elapsed']<at*spec['duration']:continue
        work['events'].append(i)
        if event=='clean':obj['dirt']=max(0.,obj.get('dirt',0)-.2);s['cleanings']=min(9999,s['cleanings']+1)
    work['done']=work['elapsed']>=spec['duration']
    if work['done'] and work.get('withdrawal'):work['interrupted']=True
    pond._cache=None;return not work['done']
def complete(pond,plan):
    work=plan.get('architecture_work')
    if not work or not work.get('done') or work.get('interrupted') or work.get('recorded') or not valid(pond,plan):return
    work['recorded']=True;obj=pond.object_state(plan['target'],plan);s=state(plan['target'],obj)
    for key,event in [('studies','study'),('adjustments','adjust')]:
        if any(e==event for _,e in ROUTINES[work['id']]['events']):s[key]=min(9999,s[key]+1)
    history=obj.setdefault('architecture_routines',{});history[work['id']]=min(9999,history.get(work['id'],0)+1)
    pond.remember('belongings',work['label']+'.',.45,plan['target'])
def view(pond,plan):
    work=copy.deepcopy(plan['architecture_work']);progress=plan['elapsed']/plan['duration']
    if plan['phase']=='prepare':work['transition']=dict(phase='enter',elapsed=max(0,min(2,(progress-.15)/.13*2)))
    elif plan['phase']=='settle':work['transition']=dict(phase='exit',elapsed=max(0,min(2,(progress-.9)/.1*2)))
    return work
def conversation(pond,plan):
    if not plan or not plan.get('architecture_work') or not valid(pond,plan):return None
    item=plan['target'];obj=pond.object_state(item,plan);s=obj['architecture'];kind=ITEMS[item]['type']
    result=dict(object=item.replace('_',' '),activity=plan['architecture_work']['label'],phase=plan['phase'],paused=bool(plan.get('paused')),material=ITEMS[item]['material'])
    pos=pond.game.renderer.duck_pos;dest=plan['destination']
    if plan['phase']=='approach' or abs(pos.x-dest[0])+abs(pos.y-dest[1])>3:return result
    if kind=='gate':result['gate_open_fraction']=round(s['open'],2)
    if kind=='mailbox':result.update(door_open_fraction=round(s['panel'],2),flag_raised=s['flag']>.5,contents='Empty compartment. Raising the flag does not send or receive mail.')
    if kind=='well':result.update(bucket='lowered into the shaft' if s['bucket']>.6 else 'partway down' if s['bucket']>.2 else 'at the rim',water='No water or treasure has been collected.')
    if kind=='windmill':result.update(sail_speed=round(s['speed'],2),brake_applied=s['brake']>.5)
    if kind in ('trellis','pergola','arch'):result['vines']='bare winter stems' if s['season']=='winter' else 'autumn leaves' if s['season']=='fall' else 'climbing leaves and roses'
    if kind in ('watchtower','castle'):result['position']='Inspecting from the ground; no climb has occurred.'
    if kind in ('castle','statue','totem'):result['inscription']=ITEMS[item]['inscription']
    if kind=='sundial':result.update(shadow_visible=s['sun']>.1,shadow_direction='left' if math.sin(s['shadow_angle'])<-.1 else 'right' if math.sin(s['shadow_angle'])>.1 else 'near the middle',clock='A decorative solar shadow; not an exact civil clock.')
    if kind=='vane':result.update(wind_direction=['east','southeast','south','southwest','west','northwest','north','northeast'][round(s['bearing']/(math.pi/4))%8],wind_strength=round(s['wind'],2))
    if kind=='flag':result['flag_height']=round(s['flag'],2)
    if kind=='gnome':result['appearance']='Painted ceramic gnome, curled boots, red cap and a carved beard; not a living visitor.'
    return result

CONTROL_CHOICES={'flag':('flag_hoist','flag_lower'),'gate':('gate_open','gate_close'),'mailbox':('mailbox_open','mailbox_close','mailbox_flag','mailbox_lower_flag'),'well':('well_lower','well_raise'),'windmill':('windmill_brake','windmill_release')}
def request(pond,item,choice,instance=None):
    if item not in ITEMS or not isinstance(choice,str) or choice not in CONTROL_CHOICES.get(ITEMS[item]['type'],()):return False,'Choose a control on this structure.'
    if pond.game.duck.growth_stage in ('egg','hatchling','duckling'):return False,'Little Cheese studies the low details and leaves the heavy controls alone.'
    if wet(pond) or gusty(pond.weather_type):return False,'Cheese waits for dry, calmer weather before working the mechanism.'
    ok,message=pond.start('item',item,instance=instance)
    if not ok:return ok,message
    plan=pond.state['plan'];work=plan['architecture_work'];work.update(id=choice,label=ROUTINES[choice]['label']);plan['label']=work['label']
    return True,work['label']+'.'
