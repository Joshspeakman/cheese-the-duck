"""Arrived gardeners, authored care clocks and memories of completed work."""
import copy
import json
from pathlib import Path
from engine import botany, shelters
from engine.visitor_shelters import distance, departing, profile

ROUTINES=json.loads((Path(__file__).parent/'client/animation/botanical-routines.json').read_text())

def flags(pond,item,actor):
    p=botany.ROOTED[item]
    stage,species=(pond.game.duck.growth_stage,'duck') if actor=='cheese' else profile(pond.minds,actor)
    return dict(pot=p['container'] in ('pot','dish'),succulent=p['type']=='succulent',
        fungus=p['type']=='fungus',tree=p['type']=='tree',garden=p['type']=='garden',flower=p['type']=='flower',trap=p['type']=='trap',
        winter=pond.season=='winter',night=pond.hour<6 or pond.hour>=19,
        young=stage in ('hatchling','duckling'),elder=stage in ('elder','legendary'),butterfly=species=='butterfly')

def choose(pond,item,actor='cheese',mode=None,ref=None):
    f=flags(pond,item,actor);mode='inspect' if f['butterfly'] else mode or botany.care_mode(pond,item,ref)
    history=pond.object_state(item,ref).get('care_routines',{})
    choices=[k for k,s in ROUTINES.items() if s['mode']==mode and all(f.get(k)==v for k,v in s['when'].items())
             and (not f['butterfly'] or s['tool']=='none')]
    weights={'fungus':8,'succulent':8,'butterfly':12,'young':6,'elder':6,'winter':5,'night':4,'garden':3,'tree':3,'trap':3,'pot':2,'flower':2}
    key=max(choices,key=lambda k:(sum(weights.get(flag,1) for flag in ROUTINES[k]['when']),-history.get(k,0)))
    return dict(id=key,elapsed=0.,done=False,label=ROUTINES[key]['label'],mode=mode)

def valid(pond,r):
    return pond.location=='Home Pond' and not any(w in pond.weather_type for w in ('storm','blizzard')) and shelters.still_placed(pond,r)

def resources_available(pond,routine):
    e=pond.state['ecology']
    return routine.get('mode')!='water' or e['water']>.15 and e['temperature']>3

def advance(pond,plan,dt):
    if not plan.get('plant_care') or plan['phase'] not in ('prepare','act'):return False
    routine=plan.get('care_routine')
    r={'id':plan['target'],'instance':plan.get('instance'),'destination':plan.get('destination')}
    if not r['destination'] or not valid(pond,r) or distance((pond.game.renderer.duck_pos.x,pond.game.renderer.duck_pos.y),r['destination'])>3:
        plan['care_routine']={'done':True,'interrupted':True};return False
    if not routine:
        routine=choose(pond,plan['target'],mode=plan['plant_care'],ref=plan);plan['care_routine']=routine
        plan['care_session']='cheese:'+str(pond.state['elapsed'])
    if not resources_available(pond,routine):
        routine.update(done=True,interrupted=True);return False
    if plan['phase']!='act' or routine.get('done'):return False
    if routine['id'] not in ROUTINES:
        routine.update(done=True,interrupted=True);return False
    routine['elapsed']=min(ROUTINES[routine['id']]['duration'],routine['elapsed']+dt)
    routine['done']=routine['elapsed']>=ROUTINES[routine['id']]['duration']
    pond._cache=None
    return not routine['done']

def record(pond,item,routine,ref=None):
    obj=pond.object_state(item,ref);h=obj.setdefault('care_routines',{})
    h[routine['id']]=min(9999,h.get(routine['id'],0)+1);obj['last_care_routine']=routine['id']

def completed(minds,key,session):
    for pair in minds.garden_scenes.values():
        if pair['sessions'].get(key)==session:pair['completed'][key]=True

def complete(pond,plan):
    r=plan.get('care_routine')
    if not r or not r.get('done') or r.get('interrupted') or plan.get('care_recorded'):return
    plan['care_recorded']=True
    record(pond,plan['target'],r,plan);botany.complete(pond,plan)
    completed(pond.minds,'cheese',plan.get('care_session'))
    pond.remember('garden',r['label']+'.',.4,plan['target'])

def workers(minds):
    result={k:r for k,r in minds.gardening.items() if r['phase'] in ('inside','exit')}
    p=minds.pond.state.get('plan')
    if p and p.get('care_routine') and not p.get('paused') and p['phase'] in ('act','settle'):
        result['cheese']=dict(id=p['target'],instance=p.get('instance'),destination=p['destination'],slot=0,session=p['care_session'],routine=p['care_routine'])
    return result

def company_tick(minds,dt):
    active=workers(minds)
    for pair,s in list(minds.garden_scenes.items()):
        if not valid(minds.pond,dict(id=s['item'],instance=s.get('instance'),destination=s['destination'])) or any(
            minds.presence_tokens.get(k)!=s['tokens'][k] or (not s['completed'][k] and
            (k not in active or active[k]['session']!=s['sessions'][k])) for k in s['sessions']):
            minds.garden_scenes.pop(pair);continue
        if all(not active.get(k,{}).get('routine',{}).get('done',True) for k in s['sessions']):s['overlap']+=dt
        if all(s['completed'].values()):
            if s['overlap']>=5:
                a,b=s['sessions'];note='Tended the '+s['item'].replace('_',' ')+' together, each finishing their part.'
                for key,other in ((a,b),(b,a)):
                    minds.model.learn(key,'share',s['contexts'][key],.24,minds.now,note,other)
                    minds.model.bond(key,other,.18,minds.now,note)
                minds.pond.remember('neighbors',note,.5,b)
            minds.garden_scenes.pop(pair)
    keys=sorted(active)
    for i,a in enumerate(keys):
        ra=active[a]
        for b in keys[i+1:]:
            rb=active[b];pair='|'.join((a,b))
            if pair in minds.garden_scenes or ra['routine']['done'] or rb['routine']['done']:continue
            if ra['id']!=rb['id'] or ra.get('instance')!=rb.get('instance') or ra['destination']!=rb['destination'] or ra['slot']==rb['slot']:continue
            minds.garden_scenes[pair]=dict(item=ra['id'],instance=ra.get('instance'),destination=list(ra['destination']),overlap=0.,
                sessions={a:ra['session'],b:rb['session']},completed={a:False,b:False},
                tokens={k:minds.presence_tokens[k] for k in (a,b)},contexts={k:minds.context(k) for k in (a,b)})

def candidates(minds,key):
    p=minds.pond;choices=[]
    if p.location!='Home Pond' or shelters.adverse(p.weather_type):return choices
    for placed in p.placements:
        item=placed.item_id
        if item not in botany.ROOTED or item not in p.owned:continue
        dest=shelters.position(placed)
        if not(7<=dest[0]<=120 and 3<=dest[1]<=35):continue
        capacity=2 if botany.ROOTED[item]['type'] in ('tree','garden','hedge','bamboo') else 1
        used=[r['slot'] for r in minds.gardening.values() if r['id']==item and r['destination']==dest]
        plan=p.state.get('plan')
        if plan and plan.get('plant_care') and plan['target']==item and plan.get('destination')==dest:used.append(0)
        slots=[s for s in range(capacity) if s not in used]
        if not slots:continue
        slot=slots[0];spot=[dest[0]+(-3 if slot==0 else 3),dest[1]]
        choices.append(dict(id=item,instance=placed.instance,destination=dest,slot=slot,spot=spot,distance=distance(minds.present[key],spot),
                            observer=bool(used)))
    return sorted(choices,key=lambda r:r['distance'])

def release(minds,key,finished=False):
    r=minds.gardening.pop(key,None)
    if not r:return
    if finished:
        p=minds.pond;routine=r['routine'];item=r['id']
        # Resource effects use the same idempotent transfer as Cheese. An
        # observing partner never repeats the other resident's watering.
        botany.complete(p,dict(kind='item',target=item,instance=r.get('instance'),destination=r['destination'],plant_care=routine['mode']))
        record(p,item,routine,r)
        note=routine['label']+' at the '+item.replace('_',' ')+'.'
        minds.model.learn(key,'garden',r['context'],.28,minds.now,note)
        minds.model.remember(key,'garden',note,minds.now,.4)
        completed(minds,key,r['session'])
    minds.garden_retry[key]=minds.now+(210 if finished else 20)
    minds.pond._cache=None

def tick(minds,dt):
    p=minds.pond
    for key,r in list(minds.gardening.items()):
        if key not in minds.present or minds.presence_tokens.get(key)!=r['token'] or departing(minds,key) or key in minds.housing or not valid(p,r) or shelters.adverse(p.weather_type) or not resources_available(p,r['routine']):
            release(minds,key);continue
        at=distance(minds.present[key],r['spot'])
        if r['phase']=='approach':
            if minds.now-r['started']>90:release(minds,key);continue
            if at<=.8:r.update(phase='enter',elapsed=0.)
        elif at>3:release(minds,key);continue
        elif r['phase']=='enter':
            r['elapsed']+=dt
            if r['elapsed']>=3:r.update(phase='inside',elapsed=0.)
        elif r['phase']=='inside':
            routine=r['routine'];routine['elapsed']=min(ROUTINES[routine['id']]['duration'],routine['elapsed']+dt)
            if routine['elapsed']>=ROUTINES[routine['id']]['duration']:
                routine['done']=True;r.update(phase='exit',elapsed=0.)
        elif r['phase']=='exit':
            r['elapsed']+=dt
            if r['elapsed']>=3:release(minds,key,True)
    from engine import playdates
    for key in sorted(minds.present):
        if key=='cheese' or key in minds.carnival_guests or key in minds.nest_helpers or key in minds.playmates or key in minds.structure_helpers or key in minds.ground_helpers or key in minds.textile_helpers or key in minds.creators or key in minds.readers or key in minds.wonder_guests or key in minds.gardening or key in minds.musicians or key in minds.housing or key in minds.furnishings or departing(minds,key) or minds.now<minds.garden_retry.get(key,0) or playdates.active(minds,key) or minds.encounter_for(key):continue
        if minds.tasks.get(key,{}).get('action')!='garden' or minds.model.residents[key]['energy']<.3:continue
        choices=candidates(minds,key)
        if not choices or choices[0]['distance']>55:
            minds.garden_retry[key]=minds.now+15;continue
        r=choices[0];routine=choose(p,r['id'],key,'inspect' if r['observer'] else None,ref=r)
        minds.tasks.pop(key,None)
        minds.gardening[key]={**r,'actor':key,'token':minds.presence_tokens[key],
            'phase':'approach','elapsed':0.,'started':minds.now,'session':key+':'+str(minds.now),
            'context':minds.context(key),'routine':routine}
        p._cache=None
    company_tick(minds,dt)
    for key in list(minds.garden_retry):
        if key not in minds.present:minds.garden_retry.pop(key)

def snapshot(minds):
    return [{k:copy.deepcopy(r.get(k)) for k in ('actor','id','instance','destination','slot','spot','phase','elapsed','routine')} for r in minds.gardening.values()]

def motion(minds,key):
    r=minds.gardening.get(key)
    return dict(target=list(r['spot']),facing=r['slot']==0,phase=r['phase'],gesture='idle') if r else None
