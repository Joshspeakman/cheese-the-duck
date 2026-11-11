"""A creative companion walks to a fixed prop and joins its native activity clock.

Reservations are transient. Actual arrival, shared native time and completed work
are required for learning. The partner never duplicates an item use or reward.
"""
import copy
import json
from pathlib import Path
from engine import creative_props, shelters
from engine.visitor_shelters import distance, departing, profile

SCORES=json.loads((Path(__file__).parent/'client/animation/creative-company.json').read_text())

def active(minds,key='cheese'):
    return next(iter(minds.creators.values()),None) if key=='cheese' else minds.creators.get(key)

def ready(minds):
    return minds.pond.available() and minds.game.duck.current_action not in ('feed','play','clean','pet','sleep')

def valid(minds,r,plan=None):
    p=minds.pond;plan=plan or p.state.get('plan')
    pos=minds.game.renderer.duck_pos
    return bool(plan and plan.get('creative_work') is r['work'] and creative_props.valid(p,plan)
                and abs(pos.x-r['destination'][0])+abs(pos.y-r['destination'][1])<=3
                and r['actor'] in minds.present and minds.presence_tokens.get(r['actor'])==r['token']
                and r['location']==p.location and not departing(minds,r['actor'])
                and r['actor'] not in minds.housing and not r['work'].get('withdrawal') and not r['work'].get('interrupted') and not shelters.adverse(p.weather_type))

def choose(minds,plan,key):
    kind=creative_props.ITEMS[plan['target']]['type'];work=plan['creative_work']
    if work['id'] in ('scope_cover','scope_polish','paint_cover','paint_uncover','paint_rinse','paint_study','kite_reel','fold_cover','fold_unwrap'):return None
    age=minds.game.duck.growth_stage;stage,species=profile(minds,key)
    if species=='butterfly':return 'hover_observer'
    young=age in ('hatchling','duckling') or stage=='duckling'
    if kind=='scope':return 'scope_first' if young else 'scope_stars' if minds.pond.hour<6 or minds.pond.hour>=19 else 'scope_bank'
    if kind=='easel':
        if age in ('elder','legendary'):return 'paint_patient'
        return 'paint_proud' if minds.model.residents[key]['traits']['confidence']>=.55 else 'paint_shy'
    if kind=='kite':return 'kite_tail_partner' if work['id']=='kite_tail' else 'kite_low_companion' if young or work['id']=='kite_calm' else 'kite_bridle'
    return 'fold_pin_partner' if creative_props.wind(minds.pond)>.5 else 'fold_wing_partner' if work['id']=='fold_wings' else 'fold_nose_partner'

def release(minds,key):
    if minds.creators.pop(key,None):
        minds.creative_retry[key]=minds.now+100
        minds.pond._cache=None

def tick(minds,dt):
    p=minds.pond;plan=p.state.get('plan')
    for key,r in list(minds.creators.items()):
        if not valid(minds,r) or not ready(minds):release(minds,key);continue
        if plan.get('paused'):
            r['started']+=dt
            continue
        if r['phase']=='approach':
            if minds.now-r['started']>25:release(minds,key);continue
            if distance(minds.present[key],r['spot'])<=.8:r.update(phase='enter',elapsed=0.)
        elif distance(minds.present[key],r['spot'])>3:release(minds,key);continue
        elif r['phase']=='enter':
            r['elapsed']+=dt
            if r['elapsed']>=2:r.update(phase='inside',elapsed=0.,last_clock=r['work']['elapsed'])
        elif r['phase']=='inside':
            elapsed=r['work']['elapsed'];shared_dt=max(0,elapsed-r['last_clock']);r['overlap']+=shared_dt;r['last_clock']=elapsed
            # Remember only things observed while both actors were actually here.
            visible=creative_props.conversation(p,plan) or {}
            observations=[]
            if visible.get('airborne'):observations.append('Watched the kite lift in the actual wind')
            if visible.get('painted_layers',0)>r['initial_layers']:observations.append('Watched new brush marks appear on the '+visible.get('painting','pond')+' painting')
            if visible.get('fold_progress',0)>.5:observations.append('Watched the paper take its folded shape')
            if visible.get('lens_capped') is False:observations.append('Kept Cheese company while the telescope lens was uncovered')
            for text in observations:
                noticed=r.setdefault('noticed',{});noticed[text]=noticed.get(text,0)+shared_dt
            if r['work'].get('done'):r['phase']='finished'
        # Stay through Cheese's settling phase so actual completion, not an
        # optimistic preview, decides whether the pair remembers this creative session.
    if not plan or not plan.get('creative_work') or plan.get('paused') or not ready(minds) or shelters.adverse(p.weather_type):return
    work=plan['creative_work'];spec=creative_props.ROUTINES.get(work.get('id'))
    if not spec or work.get('invitation_checked') or work.get('done') or work['elapsed']>0 or plan['phase'] not in ('prepare','act'):return
    work['invitation_checked']=True
    if minds.creators:return
    origin=list(plan.get('destination',work['origin']))
    # A portable prop is laid down seven native cells beside Cheese. Its companion
    # reserves the far edge, never a destination relative to Cheese's next move.
    center=[origin[0]+(0 if plan.get('instance') else 7),origin[1]]
    spot=[center[0]+9,center[1]]
    if not (6<=spot[0]<=122 and 3<=spot[1]<=36):return
    from engine import playdates
    options=[]
    for key in minds.present:
        if key=='cheese' or departing(minds,key) or minds.now<minds.creative_retry.get(key,0):continue
        if key in minds.ground_helpers or key in minds.textile_helpers or key in minds.readers or key in minds.housing or key in minds.gardening or key in minds.furnishings or key in minds.musicians or minds.encounter_for(key) or playdates.active(minds,key):continue
        resident=minds.model.residents[key]
        if resident['energy']<.25 or minds.tasks.get(key,{}).get('action') not in ('observe','share','restore','practice'):continue
        d=distance(minds.present[key],spot)
        if d>24:continue
        score=choose(minds,plan,key)
        if score:options.append((d-5*resident['traits']['sociability'],key,score))
    if not options:return
    _,key,score=min(options);minds.tasks.pop(key,None)
    minds.creators[key]=dict(actor=key,id=plan['target'],instance=plan.get('instance'),destination=origin,spot=spot,
        location=p.location,token=minds.presence_tokens[key],phase='approach',elapsed=0.,started=minds.now,
        score=score,work=work,initial_layers=p.object_state(plan['target'],plan)['creative']['strokes'],overlap=0.,last_clock=work['elapsed'],contexts={k:minds.context(k) for k in ('cheese',key)})
    p._cache=None

def waiting(minds):
    r=active(minds)
    return bool(r and valid(minds,r) and (r['phase']=='enter' or r['phase']=='approach' and minds.now-r['started']<=25))

def complete(minds,plan):
    r=active(minds)
    if not r or not valid(minds,r,plan) or r.get('recorded') or r['phase'] not in ('inside','finished'):return
    work=r['work'];duration=creative_props.ROUTINES[work['id']]['duration']
    if not work.get('done') or work.get('interrupted') or r['overlap']<max(5,duration*.45) or distance(minds.present[r['actor']],r['spot'])>3:return
    r['recorded']=True;key=r['actor'];note=SCORES[r['score']]['label']+'.'
    noticed=[text for text,seconds in r.get('noticed',{}).items() if seconds>=2]
    if noticed:note+=' Together: '+ ' / '.join(noticed[-2:])+'.'
    for actor,other in (('cheese',key),(key,'cheese')):
        minds.model.learn(actor,'share',r['contexts'][actor],.25,minds.now,note,other)
        minds.model.bond(actor,other,.18,minds.now,note)
    obj=minds.pond.object_state(plan['target'],plan);history=obj.setdefault('creative_company',{})
    history[r['score']]=min(9999,history.get(r['score'],0)+1)
    minds.pond.remember('neighbors',minds.model.residents[key]['name']+' and Cheese: '+note,.55,key)

def work_view(minds,work,role='a'):
    out=copy.deepcopy(work);r=active(minds)
    if r and r['work'] is work and valid(minds,r) and (role=='b' or r['phase'] in ('inside','finished')):
        out['company']=dict(id=r['score'],role=role)
    plan=minds.pond.state.get('plan')
    if plan and plan.get('creative_work') is work:
        progress=plan['elapsed']/plan['duration']
        if role=='a' and plan['phase']=='prepare':out['transition']=dict(phase='enter',elapsed=max(0,min(2,(progress-.15)/.13*2)))
        elif plan['phase']=='settle':out['transition']=dict(phase='exit',elapsed=max(0,min(2,(progress-.9)/.1*2)))
        elif role=='b' and r and r['phase']=='enter':out['transition']=dict(phase='enter',elapsed=r['elapsed'])
    return out

def snapshot(minds):
    result=[]
    for r in minds.creators.values():
        if not valid(minds,r):continue
        work=work_view(minds,r['work'],'b')
        record={k:copy.deepcopy(r[k]) for k in ('actor','id','instance','destination','spot','phase','elapsed')}
        if work.get('transition',{}).get('phase')=='exit':record.update(phase='exit',elapsed=work['transition']['elapsed'])
        result.append(dict(**record,routine=work))
    return result

def motion(minds,key):
    r=minds.creators.get(key)
    return dict(target=list(r['spot']),facing=False,phase=r['phase'],gesture='idle') if r else None

def conversation(minds,key):
    r=active(minds,key)
    if not r or not valid(minds,r):return None
    partner=r['actor'] if key=='cheese' else 'cheese';plan=minds.pond.state['plan']
    return dict(with_name=minds.model.residents[partner]['name'],activity=SCORES[r['score']]['label'],
                status='paused' if plan.get('paused') else 'walking over' if r['phase']=='approach' else 'settling in' if r['phase']=='enter' else 'finished the session' if r['phase']=='finished' else 'making and observing together now')
