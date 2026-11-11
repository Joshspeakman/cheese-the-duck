"""An independently arriving neighbour helps from outside an occupied nest.

The nest's native routine remains the single owner of material contacts. The
companion holds its edge, counts steps or observes; it never consumes a second
nest place or duplicates a completion reward.
"""
import copy
import json
from pathlib import Path
from engine import nest_routines, shelters
from engine.visitor_shelters import distance, departing, profile

SCORES=json.loads((Path(__file__).parent/'client/animation/nest-company.json').read_text())

def active(minds,key='cheese'):
    return next(iter(minds.nest_helpers.values()),None) if key=='cheese' else minds.nest_helpers.get(key)

def ready(minds):
    return minds.pond.available() and minds.game.duck.current_action not in ('feed','play','clean','pet','sleep')

def valid(minds,r):
    p=minds.pond;plan=p.state.get('plan');pos=minds.game.renderer.duck_pos
    return bool(plan and plan.get('residence',{}).get('routine') is r['work']
        and not r['work'].get('interrupted') and shelters.still_placed(p,r)
        and abs(pos.x-r['destination'][0])+abs(pos.y-r['destination'][1])<=3
        and r['actor'] in minds.present and minds.presence_tokens.get(r['actor'])==r['token']
        and (r['phase']=='approach' or distance(minds.present[r['actor']],r['spot'])<=3)
        and p.location==r['location'] and not departing(minds,r['actor'])
        and r['actor'] not in minds.housing and not shelters.adverse(p.weather_type))

def choose(minds,plan,key):
    core=plan['residence']['routine']['id'];age=minds.game.duck.growth_stage
    stage,species=profile(minds,key)
    # A hovering insect observes without suddenly growing a bill or fingers.
    if species=='butterfly':return 'hover_observer'
    if age in ('mature','elder','legendary') or minds.model.residents[key]['energy']<.45 or minds.model.residents[key]['mood']<.3:return 'patient_company'
    if age in ('hatchling','duckling') and stage!='duckling' and species!='toad' and core in SCORES['young_support']['cores']:return 'young_support'
    selected=next((name for name,s in SCORES.items() if name!='young_support' and core in s['cores']),None)
    if selected and (stage=='duckling' or species=='toad') and selected in ('left_rim','right_rim','weave_tension','lining_fan','summer_fan'):
        return 'lining_inspect'  # Watch the joinery instead of overreaching it.
    return selected

def release(minds,key):
    if minds.nest_helpers.pop(key,None):
        minds.nest_retry[key]=minds.now+60;minds.pond._cache=None

def invite(minds,plan):
    work=plan['residence']['routine']
    if work.get('invitation_checked'):return
    work['invitation_checked']=True
    if minds.nest_helpers or plan.get('paused') or not ready(minds) or shelters.adverse(minds.pond.weather_type):return
    from engine import playdates
    origin=list(plan['destination']);options=[]
    for key in minds.present:
        if key=='cheese' or departing(minds,key) or minds.now<minds.nest_retry.get(key,0):continue
        if any(key in getattr(minds,name,{}) for name in ('carnival_guests','playmates','structure_helpers','ground_helpers','textile_helpers','creators','readers','housing','gardening','furnishings','musicians')) or minds.encounter_for(key) or playdates.active(minds,key):continue
        resident=minds.model.residents[key]
        if resident['energy']<.25 or minds.tasks.get(key,{}).get('action') not in ('observe','share','restore'):continue
        selected=choose(minds,plan,key)
        if not selected:continue
        side=-1 if SCORES[selected]['anchor']=='left' else 1
        spot=[origin[0]+side*10,origin[1]+1]
        if not (6<=spot[0]<=122 and 3<=spot[1]<=36):continue
        d=distance(minds.present[key],spot)
        if d>24:continue
        options.append((d-resident['traits']['care']*4,key,selected,spot))
    if not options:return
    _,key,selected,spot=min(options);minds.tasks.pop(key,None)
    minds.nest_helpers[key]=dict(actor=key,id=plan['target'],instance=plan.get('instance'),destination=origin,spot=spot,
        location=minds.pond.location,token=minds.presence_tokens[key],phase='approach',elapsed=0.,started=minds.now,
        score=selected,work=work,overlap=0.,last_clock=0.,contexts={a:minds.context(a) for a in ('cheese',key)})
    minds.pond._cache=None

def tick(minds,dt):
    for key,r in list(minds.nest_helpers.items()):
        if not valid(minds,r) or not ready(minds):release(minds,key);continue
        if minds.pond.state['plan'].get('paused'):
            r['started']+=dt;continue
        if r['phase']=='approach':
            if minds.now-r['started']>25:release(minds,key);continue
            if distance(minds.present[key],r['spot'])<=.8:r.update(phase='enter',elapsed=0.)
        elif distance(minds.present[key],r['spot'])>3:release(minds,key);continue
        elif r['phase']=='enter':
            r['elapsed']+=dt
            if r['elapsed']>=2:r.update(phase='inside',elapsed=0.,last_clock=r['work']['elapsed'])
        elif r['phase']=='inside':
            r['overlap']+=max(0,r['work']['elapsed']-r['last_clock']);r['last_clock']=r['work']['elapsed']
        if r['work'].get('done'):r['phase']='finished'

def waiting(minds):
    r=active(minds)
    return bool(r and valid(minds,r) and (r['phase']=='enter' or r['phase']=='approach' and minds.now-r['started']<=25))

def complete(minds,plan):
    r=active(minds)
    if not r or not valid(minds,r) or r.get('recorded') or r['phase'] not in ('inside','finished'):return
    work=r['work'];duration=nest_routines.ROUTINES[work['id']]['duration']
    if not work.get('done') or work.get('interrupted') or r['overlap']<duration*.5 or distance(minds.present[r['actor']],r['spot'])>3:return
    r['recorded']=True;key=r['actor'];note=SCORES[r['score']]['label']+'.'
    for actor,other in (('cheese',key),(key,'cheese')):
        minds.model.learn(actor,'share',r['contexts'][actor],.23,minds.now,note,other)
        minds.model.bond(actor,other,.16,minds.now,note)
    obj=minds.pond.object_state(plan['target'],plan);history=obj.setdefault('nest_company',{})
    history[r['score']]=min(9999,history.get(r['score'],0)+1)
    minds.pond.remember('neighbors',minds.model.residents[key]['name']+' and Cheese: '+note,.55,key)

def work_view(minds,work,role='a'):
    out=copy.deepcopy(work);r=active(minds)
    if r and r['work'] is work and valid(minds,r) and (role=='b' or r['phase'] in ('inside','finished')):
        out['company']=dict(id=r['score'],role=role)
        if role=='b' and r['phase']=='enter':out['transition']=dict(phase='enter',elapsed=r['elapsed'])
    return out

def snapshot(minds):
    return [dict(**{k:copy.deepcopy(r[k]) for k in ('actor','id','instance','destination','spot','phase','elapsed')},
                 routine=work_view(minds,r['work'],'b')) for r in minds.nest_helpers.values() if valid(minds,r)]

def motion(minds,key):
    r=minds.nest_helpers.get(key)
    return dict(target=list(r['spot']),facing=SCORES[r['score']]['anchor']=='left',phase=r['phase'],gesture='idle') if r else None

def conversation(minds,key):
    r=active(minds,key)
    if not r or not valid(minds,r):return None
    partner=r['actor'] if key=='cheese' else 'cheese'
    return dict(with_name=minds.model.residents[partner]['name'],activity=SCORES[r['score']]['label'],
        status='paused' if minds.pond.state['plan'].get('paused') else 'walking over' if r['phase']=='approach' else
        'getting into position' if r['phase']=='enter' else 'finished together' if r['phase']=='finished' else 'helping beside the nest now')
