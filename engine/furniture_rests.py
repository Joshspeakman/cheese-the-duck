"""Independent seat reservations and completed, remembered shared rests."""
import copy
import json
from pathlib import Path
from engine import shelters
from engine.visitor_shelters import distance, departing, profile

DATA=Path(__file__).parent/'client/animation'
BLUEPRINTS=json.loads((DATA/'furniture.json').read_text())
SEATS={key:value for key,value in BLUEPRINTS.items() if value.get('seat')}
ROUTINES=json.loads((DATA/'seating-routines.json').read_text())

def flags(pond,item,actor='cheese'):
    p=SEATS[item];m=pond.minds
    stage=pond.game.duck.growth_stage if actor=='cheese' else profile(m,actor)[0]
    energy=pond.game.duck.needs.energy/100 if actor=='cheese' else m.model.residents[actor]['energy']
    return dict(soft=p['type'] in ('sofa','cushion','hammock'),tired=energy<.55,
                royal=p['style'] in ('gold','velvet') and p['type']=='chair',
                quilt=p['style'] in ('quilt','patchwork'),hammock=p['type']=='hammock',
                bench=p['type']=='bench',autumn=pond.season=='fall',
                night=pond.hour<6 or pond.hour>=19,day=6<=pond.hour<19,
                hot=pond.state['ecology']['temperature']>=25,
                elder=stage in ('elder','legendary'),young=stage in ('hatchling','duckling'))

def choose(pond,item,actor='cheese',shared=False,ref=None):
    f=flags(pond,item,actor);obj=pond.object_state(item,ref)
    history=obj.get('seat_routines',{})
    options=[key for key,spec in ROUTINES.items() if bool(spec.get('shared'))==shared
             and all(f.get(k)==v for k,v in spec['when'].items())]
    if shared:
        # Context chooses a first moment; completed history then gives quieter,
        # less specific moments a turn instead of repeating the same daylight
        # observation forever.
        weights={'tired':3,'night':2,'day':1}
        return max(options,key=lambda key:(-history.get(key,0),key!=obj.get('last_seat_routine'),
                   sum(weights.get(k,0) for k in ROUTINES[key]['when'])))
    return max(options,key=lambda key:(bool(ROUTINES[key]['when']),
               key!=obj.get('last_seat_routine'),-history.get(key,0)))

def candidates(pond,target='',actor='cheese'):
    if pond.location!='Home Pond' or shelters.adverse(pond.weather_type):return []
    m=pond.minds
    stage=pond.game.duck.growth_stage if actor=='cheese' else profile(m,actor)[0]
    if stage=='egg':return []
    pos=m.present.get(actor,(pond.game.renderer.duck_pos.x,pond.game.renderer.duck_pos.y))
    result=[]
    for placed in pond.placements:
        item=placed.item_id
        if item not in SEATS or item not in pond.owned or target and item!=target:continue
        dest=shelters.position(placed)
        if not (2<=dest[0]<=124 and 2<=dest[1]<=37):continue
        used=[r['slot'] for key,r in m.furnishings.items() if key!=actor and r['id']==item and r['destination']==dest]
        plan=pond.state.get('plan')
        if actor!='cheese' and plan and plan.get('seating'):
            r=plan['seating']
            if r['id']==item and r['destination']==dest:used.append(r['slot'])
        slots=[n for n in range(SEATS[item]['capacity']) if n not in used]
        if not slots:continue
        # The reservation belongs to this physical copy and never follows Cheese.
        result.append(dict(id=item,instance=placed.instance,destination=dest,slot=slots[0],capacity=SEATS[item]['capacity'],
                           distance=distance(pos,dest)))
    return sorted(result,key=lambda r:r['distance'])

def valid(pond,r):
    return pond.location=='Home Pond' and not shelters.adverse(pond.weather_type) and shelters.still_placed(pond,r)

def company_for(minds,actor):
    return next((s for s in minds.seat_scenes.values() if actor in (s['a'],s['b'])),None)

def advance(pond,plan,dt):
    seat=plan.get('seating')
    if not seat or plan['phase']!='act':return False
    routine=plan.get('seat_routine')
    if not valid(pond,seat) or distance((pond.game.renderer.duck_pos.x,pond.game.renderer.duck_pos.y),seat['destination'])>3:
        plan['seat_routine']={'done':True,'interrupted':True};return False
    if not routine:
        key=choose(pond,seat['id'],ref=seat)
        routine={'id':key,'elapsed':0.,'done':False,'label':ROUTINES[key]['label']}
        plan['seat_routine']=routine
    if routine.get('done'):return False
    if routine['id'] not in ROUTINES:
        routine.update(done=True,interrupted=True);return False
    if company_for(pond.minds,'cheese'):return True
    routine['elapsed']=min(ROUTINES[routine['id']]['duration'],routine['elapsed']+dt)
    routine['done']=routine['elapsed']>=ROUTINES[routine['id']]['duration']
    pond._cache=None
    return not routine['done']

def record(pond,item,key,ref=None):
    obj=pond.object_state(item,ref);history=obj.setdefault('seat_routines',{})
    history[key]=min(9999,history.get(key,0)+1);obj['last_seat_routine']=key

def complete(pond,plan):
    r=plan.get('seat_routine')
    if not r or not r.get('done') or r.get('interrupted'):return
    record(pond,plan['target'],r['id'],plan)
    pond.remember('item',r['label']+'.',.35,plan['target'])

def release(minds,key,completed=False):
    r=minds.furnishings.pop(key,None)
    if not r:return
    if completed:
        note=ROUTINES[r['routine']['id']]['label']+' on the '+r['id'].replace('_',' ')+'.'
        resident=minds.model.residents[key]
        resident['energy']=min(1.,resident['energy']+.045)
        minds.model.learn(key,'rest',r['context'],.3,minds.now,note)
        minds.model.remember(key,'seat',note,minds.now,.4)
        record(minds.pond,r['id'],r['routine']['id'],r)
    minds.seat_retry[key]=minds.now+(300 if completed else 20)
    minds.pond._cache=None

def inside(minds):
    result={key:r for key,r in minds.furnishings.items() if r['phase']=='inside'}
    plan=minds.pond.state.get('plan')
    if plan and not plan.get('paused') and plan['phase']=='act' and plan.get('seating') and not plan.get('seat_routine',{}).get('done'):
        result['cheese']={**plan['seating'],'routine':plan.get('seat_routine',{}),'owner':plan['seating']}
    return result

def company_tick(minds,dt):
    seated=inside(minds)
    for pair,s in list(minds.seat_scenes.items()):
        a,b=s['a'],s['b']
        if any(key not in seated or minds.presence_tokens.get(key)!=s['tokens'][key]
               or seated[key]['id']!=s['item'] or seated[key].get('instance')!=s.get('instance') or seated[key]['destination']!=s['destination']
               for key in (a,b)):
            minds.seat_scenes.pop(pair);continue
        s['elapsed']+=dt
        if s['elapsed']>=ROUTINES[s['id']]['duration']:
            note=ROUTINES[s['id']]['label']+' on the '+s['item'].replace('_',' ')+'.'
            for key,other in ((a,b),(b,a)):
                minds.model.learn(key,'share',s['contexts'][key],.2,minds.now,note,other)
                minds.model.bond(key,other,.15,minds.now,note)
            record(minds.pond,s['item'],s['id'],s)
            minds.pond.remember('neighbors',note,.45,b)
            minds.seat_scenes.pop(pair)
    keys=sorted(seated)
    for i,a in enumerate(keys):
        ra=seated[a];owner_a=ra.get('owner',ra)
        if owner_a.get('company_done') or company_for(minds,a):continue
        for b in keys[i+1:]:
            rb=seated[b];owner_b=rb.get('owner',rb)
            if owner_b.get('company_done') or company_for(minds,b):continue
            if ra['id']!=rb['id'] or ra.get('instance')!=rb.get('instance') or ra['destination']!=rb['destination'] or ra['slot']==rb['slot']:continue
            if any(r.get('routine',{}).get('done') for r in (ra,rb)):continue
            owner_a['company_done']=owner_b['company_done']=True
            # A shared clock holds both individual rests. No independent visitor
            # task can expire or reward itself during this actual shared pause.
            key=choose(minds.pond,ra['id'],a,True,ra)
            left,right=sorted((a,b),key=lambda k:seated[k]['slot'])
            minds.seat_scenes['|'.join(sorted((a,b)))]=dict(id=key,a=left,b=right,elapsed=0.,
                item=ra['id'],instance=ra.get('instance'),destination=list(ra['destination']),
                tokens={k:minds.presence_tokens[k] for k in (a,b)},
                contexts={k:minds.context(k) for k in (a,b)})
            break

def tick(minds,dt):
    p=minds.pond
    for key,r in list(minds.furnishings.items()):
        if key not in minds.present or minds.presence_tokens.get(key)!=r['token'] or departing(minds,key) or key in minds.housing or not valid(p,r):
            release(minds,key);continue
        at=distance(minds.present[key],r['destination'])
        if r['phase']=='approach':
            if minds.now-r['started']>90:release(minds,key);continue
            if at<=.8:r.update(phase='enter',elapsed=0.)
        elif at>3:release(minds,key);continue
        elif r['phase']=='enter':
            r['elapsed']+=dt
            if r['elapsed']>=3:r.update(phase='inside',elapsed=0.)
        elif r['phase']=='inside':
            if not company_for(minds,key):
                routine=r['routine'];routine['elapsed']+=dt
                if routine['elapsed']>=ROUTINES[routine['id']]['duration']:
                    routine['done']=True;r.update(phase='exit',elapsed=0.)
        elif r['phase']=='exit':
            r['elapsed']+=dt
            if r['elapsed']>=3:release(minds,key,True)
    if not shelters.adverse(p.weather_type) and p.location=='Home Pond':
        from engine import playdates
        for key in sorted(minds.present):
            if key=='cheese' or key in minds.nest_helpers or key in minds.playmates or key in minds.structure_helpers or key in minds.ground_helpers or key in minds.textile_helpers or key in minds.creators or key in minds.readers or key in minds.furnishings or key in minds.gardening or key in minds.musicians or key in minds.housing or departing(minds,key) or minds.now<minds.seat_retry.get(key,0) or playdates.active(minds,key) or minds.encounter_for(key):continue
            if minds.model.residents[key]['energy']>=.62 and minds.tasks.get(key,{}).get('action')!='rest':continue
            choices=candidates(p,actor=key)
            if not choices or choices[0]['distance']>55:
                minds.seat_retry[key]=minds.now+15;continue
            r=choices[0];routine=choose(p,r['id'],key,ref=r)
            # A genuine furniture rest replaces the abstract rest task; it must
            # not wake later and grant an extra, unearned recovery.
            minds.tasks.pop(key,None)
            minds.furnishings[key]={**r,'actor':key,'token':minds.presence_tokens[key],
                'phase':'approach','elapsed':0.,'started':minds.now,'context':minds.context(key),
                'routine':{'id':routine,'elapsed':0.,'done':False,'label':ROUTINES[routine]['label']}}
            p._cache=None
    company_tick(minds,dt)
    for key in list(minds.seat_retry):
        if key not in minds.present:minds.seat_retry.pop(key)

def routine_view(minds,key,routine):
    scene=company_for(minds,key)
    if scene:return dict(id=scene['id'],elapsed=scene['elapsed'],role='a' if scene['a']==key else 'b',
                         label=ROUTINES[scene['id']]['label'],done=False)
    return copy.deepcopy(routine)

def snapshot(minds):
    return [{**{k:copy.deepcopy(r.get(k)) for k in ('actor','id','instance','destination','slot','capacity','phase','elapsed')},
             'routine':routine_view(minds,key,r['routine'])} for key,r in minds.furnishings.items()]

def motion(minds,key):
    r=minds.furnishings.get(key)
    if not r:return None
    return dict(target=list(r['destination']),facing=r['slot']==0,phase=r['phase'],
                gesture='walking' if r['phase'] in ('enter','exit') else 'idle')
