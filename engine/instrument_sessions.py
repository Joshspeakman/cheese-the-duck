"""Arrived musicians, a shared beat and notes emitted exactly once from native time."""
import copy
import json
from pathlib import Path
from engine import shelters
from engine.visitor_shelters import distance,departing,profile

DATA=Path(__file__).parent/'client/animation'
INSTRUMENTS=json.loads((DATA/'instruments.json').read_text())
SCORES=json.loads((DATA/'music-scores.json').read_text())
WHITE=(0,2,4,5,7,9,11,12)

def flags(pond,item,actor):
    p=INSTRUMENTS[item];m=pond.minds
    stage=pond.game.duck.growth_stage if actor=='cheese' else profile(m,actor)[0]
    resident=m.model.residents[actor]
    return dict(young=stage in ('hatchling','duckling'),elder=stage in ('elder','legendary'),
        night=pond.hour<6 or pond.hour>=19,day=6<=pond.hour<19,rain='rain' in pond.weather_type,
        autumn=pond.season=='fall',grumpy=resident['mood']<.35,bold=resident['traits']['confidence']>.65,
        cassette=p['style']=='cassette',wooden=p['style']=='wood',tubes=p['style']=='tubes',shells=p['style']=='shells',bell=p['style']=='bell')

def choose(pond,item,actor='cheese',shared=False,ref=None):
    p=INSTRUMENTS[item];f=flags(pond,item,actor);history=pond.object_state(item,ref).get('music_scores',{})
    options=[k for k,s in SCORES.items() if p['type'] in s['types'] and s['shared']==shared and all(f.get(k)==v for k,v in s['when'].items())]
    if not options:return None
    weights={'young':10,'elder':8,'night':7,'rain':6,'grumpy':6,'autumn':4,'bold':4,'day':1}
    return max(options,key=lambda k:sum(weights.get(flag,3) for flag in SCORES[k]['when'])-min(5,history.get(k,0))*.4)

def make_score(pond,item,actor='cheese',shared=False,ref=None):
    key=choose(pond,item,actor,shared,ref)
    return dict(id=key,elapsed=0.,cursor=0,done=False,label=SCORES[key]['label']) if key else None

def valid(pond,r):
    return pond.location=='Home Pond' and not any(w in pond.weather_type for w in ('storm','blizzard')) and shelters.still_placed(pond,r)

def note_events(item,score):
    spec=SCORES[score['id']];p=INSTRUMENTS[item];beat=60/spec['tempo']
    result=[]
    for i,n in enumerate(spec['notes']):
        pitch=n[1];voice=p['voice'];midi=60+WHITE[pitch%8]
        if voice=='gong':midi=43
        elif voice=='drum':
            head=pitch%6;voice=('tom','tom','snare','cymbal','tom','kick')[head];midi=(48,53,36,84,41,33)[head]
        elif voice in ('bell','shell','tines'):midi+=12
        result.append(dict(index=i,at=2+n[0]*beat,key=pitch,hand=n[2],hold=(n[3] if len(n)>3 else .7)*beat,
                           velocity=n[4] if len(n)>4 else .6,midi=midi,voice=voice))
    return result

def clock(minds,item,routine,dt,session):
    if routine.get('done'):return
    spec=SCORES[routine['id']];routine['elapsed']=min(spec['duration'],routine['elapsed']+dt)
    events=note_events(item,routine)
    while routine['cursor']<len(events) and events[routine['cursor']]['at']<=routine['elapsed']:
        event=events[routine['cursor']];routine['cursor']+=1
        # A late update consumes old beats, but does not burst a whole missed
        # bar through the speakers when a window resumes.
        if routine['elapsed']-event['at']<=.35:
            minds.instrument_audio.play(session,event['voice'],event['midi'],event['hold'],event['velocity'])
    routine['done']=routine['elapsed']>=spec['duration']
    minds.pond._cache=None

def company_for(minds,key):return next((s for s in minds.music_scenes.values() if key in (s['a'],s['b'])),None)

def advance(pond,plan,dt):
    r=plan.get('instrument')
    if not r or plan['phase'] not in ('prepare','act'):return False
    score=plan.get('music_score')
    if not valid(pond,r) or distance((pond.game.renderer.duck_pos.x,pond.game.renderer.duck_pos.y),r['destination'])>3:
        plan['music_score']={'done':True,'interrupted':True};return False
    if not score:
        score=make_score(pond,r['id'],ref=r);plan['music_score']=score;plan['music_session']='cheese:'+str(pond.state['elapsed'])
    if score.get('id') not in SCORES:score.update(done=True,interrupted=True);return False
    if plan['phase']!='act' or score['done']:return False
    if company_for(pond.minds,'cheese'):return True
    clock(pond.minds,r['id'],score,dt,plan['music_session'])
    return not score['done']

def record(pond,item,score,ref=None):
    obj=pond.object_state(item,ref);history=obj.setdefault('music_scores',{})
    history[score['id']]=min(9999,history.get(score['id'],0)+1);obj['last_music_score']=score['id']

def complete(pond,plan):
    s=plan.get('music_score')
    if not s or not s.get('done') or s.get('interrupted') or plan.get('music_recorded'):return
    plan['music_recorded']=True;record(pond,plan['target'],s,plan)
    pond.remember('music',s['label']+'.',.45,plan['target'])

def candidates(minds,actor,target=''):
    p=minds.pond
    if p.location!='Home Pond' or any(w in p.weather_type for w in ('storm','blizzard')):return []
    stage,species=(p.game.duck.growth_stage,'duck') if actor=='cheese' else profile(minds,actor)
    if stage=='egg':return []
    out=[]
    for placed in p.placements:
        item=placed.item_id
        if item not in INSTRUMENTS or item not in p.owned or target and item!=target:continue
        spec=INSTRUMENTS[item]
        if species=='butterfly' and spec['type']!='chimes':continue
        dest=shelters.position(placed)
        if not(6<=dest[0]<=122 and 3<=dest[1]<=36):continue
        used=[r['slot'] for k,r in minds.musicians.items() if k!=actor and r['id']==item and r['destination']==dest]
        plan=p.state.get('plan')
        if actor!='cheese' and plan and plan.get('instrument') and plan['target']==item and plan.get('destination')==dest:used.append(plan['instrument']['slot'])
        slots=[s for s in range(spec['capacity']) if s not in used]
        if not slots:continue
        slot=slots[0];spot=list(dest) if actor=='cheese' else [dest[0]+(-3 if slot==0 else 3),dest[1]]
        out.append(dict(id=item,instance=placed.instance,destination=dest,spot=spot,slot=slot,capacity=spec['capacity'],distance=distance(minds.present.get(actor,dest),spot)))
    return sorted(out,key=lambda r:r['distance'])

def cheese_ready(minds):
    return minds.pond.available() and minds.game.duck.current_action not in ('feed','play','clean','pet','sleep')

def occupants(minds):
    out={k:r for k,r in minds.musicians.items() if r['phase']=='inside'}
    p=minds.pond.state.get('plan')
    if p and p.get('instrument') and p.get('music_score') and p['phase']=='act' and not p.get('paused') and not p['music_score']['done'] and cheese_ready(minds):
        out['cheese']={**p['instrument'],'score':p['music_score'],'owner':p['instrument']}
    return out

def company_tick(minds,dt):
    active=occupants(minds)
    for key,s in list(minds.music_scenes.items()):
        if any(k not in active or active[k]['id']!=s['item'] or active[k].get('instance')!=s.get('instance') or active[k]['destination']!=s['destination'] or minds.presence_tokens.get(k)!=s['tokens'][k] for k in (s['a'],s['b'])):
            minds.music_scenes.pop(key);continue
        clock(minds,s['item'],s['score'],dt,s['session'])
        if s['score']['done']:
            note=s['score']['label']+' on the '+s['item'].replace('_',' ')+'.'
            for k,other in ((s['a'],s['b']),(s['b'],s['a'])):
                minds.model.learn(k,'practice',s['contexts'][k],.25,minds.now,note,other);minds.model.bond(k,other,.17,minds.now,note)
            record(minds.pond,s['item'],s['score'],s);minds.pond.remember('neighbors',note,.5,s['b']);minds.music_scenes.pop(key)
    keys=sorted(active)
    for i,a in enumerate(keys):
        ra=active[a];owner=ra.get('owner',ra)
        if owner.get('duet_done') or company_for(minds,a):continue
        for b in keys[i+1:]:
            rb=active[b];other=rb.get('owner',rb)
            if other.get('duet_done') or company_for(minds,b) or ra['id']!=rb['id'] or ra.get('instance')!=rb.get('instance') or ra['destination']!=rb['destination'] or ra['slot']==rb['slot']:continue
            score=make_score(minds.pond,ra['id'],a,True,ra)
            if not score:continue
            owner['duet_done']=other['duet_done']=True
            first,second=sorted((a,b),key=lambda k:active[k]['slot'])
            pair='|'.join(sorted((a,b)))
            minds.music_scenes[pair]=dict(a=first,b=second,item=ra['id'],instance=ra.get('instance'),destination=list(ra['destination']),score=score,session='duet:'+pair+':'+str(minds.now),tokens={k:minds.presence_tokens[k] for k in (a,b)},contexts={k:minds.context(k) for k in (a,b)})
            break

def release(minds,key,finished=False):
    r=minds.musicians.pop(key,None)
    if not r:return
    if finished:
        note=r['score']['label']+' on the '+r['id'].replace('_',' ')+'.'
        minds.model.learn(key,'practice',r['context'],.25,minds.now,note);record(minds.pond,r['id'],r['score'],r)
    minds.music_retry[key]=minds.now+(200 if finished else 20);minds.pond._cache=None

def tick(minds,dt):
    p=minds.pond
    for key,r in list(minds.musicians.items()):
        if key not in minds.present or minds.presence_tokens.get(key)!=r['token'] or departing(minds,key) or key in minds.housing or not valid(p,r):release(minds,key);continue
        at=distance(minds.present[key],r['spot'])
        if r['phase']=='approach':
            if minds.now-r['started']>90:release(minds,key);continue
            if at<=.8:r.update(phase='enter',elapsed=0.)
        elif at>3:release(minds,key);continue
        elif r['phase']=='enter':
            r['elapsed']+=dt
            if r['elapsed']>=3:r.update(phase='inside',elapsed=0.)
        elif r['phase']=='inside':
            if not company_for(minds,key):clock(minds,r['id'],r['score'],dt,r['session'])
            if r['score']['done']:r.update(phase='exit',elapsed=0.)
        elif r['phase']=='exit':
            r['elapsed']+=dt
            if r['elapsed']>=3:release(minds,key,True)
    from engine import playdates
    for key in sorted(minds.present):
        if key=='cheese' or key in minds.carnival_guests or key in minds.nest_helpers or key in minds.playmates or key in minds.structure_helpers or key in minds.ground_helpers or key in minds.textile_helpers or key in minds.creators or key in minds.readers or key in minds.musicians or key in minds.housing or key in minds.furnishings or key in minds.gardening or departing(minds,key) or minds.now<minds.music_retry.get(key,0) or minds.encounter_for(key) or playdates.active(minds,key):continue
        if minds.tasks.get(key,{}).get('action')!='practice' or minds.model.residents[key]['energy']<.25:continue
        choices=candidates(minds,key)
        if not choices or choices[0]['distance']>55:minds.music_retry[key]=minds.now+15;continue
        r=choices[0];score=make_score(p,r['id'],key,ref=r);minds.tasks.pop(key,None)
        minds.musicians[key]={**r,'actor':key,'token':minds.presence_tokens[key],'started':minds.now,'session':key+':'+str(minds.now),'score':score,'phase':'approach','elapsed':0.,'context':minds.context(key)}
    company_tick(minds,dt)
    sessions={r['session'] for r in minds.musicians.values() if r['phase']=='inside' and not company_for(minds,r['actor'])}
    plan=p.state.get('plan')
    if plan and plan.get('music_session') and not plan.get('paused') and cheese_ready(minds) and not company_for(minds,'cheese'):sessions.add(plan['music_session'])
    sessions.update(s['session'] for s in minds.music_scenes.values());minds.instrument_audio.stop_except(sessions)
    for key in list(minds.music_retry):
        if key not in minds.present:minds.music_retry.pop(key)

def score_view(minds,key,score):
    duet=company_for(minds,key)
    return {**copy.deepcopy(duet['score']),'role':'a' if duet['a']==key else 'b'} if duet else copy.deepcopy(score)

def snapshot(minds):
    return [{**{k:copy.deepcopy(r.get(k)) for k in ('actor','id','instance','destination','slot','phase','elapsed')},'score':score_view(minds,key,r['score'])} for key,r in minds.musicians.items()]

def motion(minds,key):
    r=minds.musicians.get(key)
    return dict(target=list(r['spot']),facing=r['slot']==0,phase=r['phase'],gesture='idle') if r else None
