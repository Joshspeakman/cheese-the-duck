"""Bounded shared castle controls: an exact visitor operates, Cheese observes.

One existing animator owns each root; one existing work clock owns all effects.
Proposals are pure. Live leases never survive reload or accept replacement guests.
"""
import copy,json,math,uuid
from pathlib import Path
from engine import castle_work as castle,castle_actors as actors,excursions,terrain
from engine.portable_ground import policy
from world.guest_cast import guest_profile

METRIC_DATA=json.loads((Path(__file__).parent/'client/animation/castle-guest-metrics.json').read_text())
METRICS=METRIC_DATA['casts']
IMMUTABLE=('operator','source_age','cheese_identity','instance','center','sites','operator_routes','operator_exit_route','cheese_route','cheese_exit_route','watch','operator_exit','cheese_exit')
RESERVED=('nest_helpers','playmates','structure_helpers','ground_helpers','textile_helpers','creators','readers','housing','furnishings','gardening','musicians')


def point(p):return isinstance(p,(tuple,list)) and len(p)==2 and all(type(n) in (int,float) and math.isfinite(n) for n in p)
def near(a,b,tolerance=1e-7):return point(a) and point(b) and max(abs(a[i]-b[i]) for i in (0,1))<=tolerance
def cheese_root(pond):return [float(pond.game.renderer.duck_pos.x),float(pond.game.renderer.duck_pos.y)]
def operator_metrics(cast,score):
    if score in castle.AIR_SCORES:
        from engine import castle_air
        return castle_air.DATA['casts'][cast]['routines'][score]
    return METRICS[cast]['routines'][score]

def operator_travel(cast,score):
    if score in castle.AIR_SCORES:
        from engine import castle_air
        return dict(castle_air.DATA['casts'][cast]['travel'],full_body=True)
    return METRICS[cast]['travel']
def cheese_metric(age,score=None):
    if score in castle.AIR_SCORES:
        from engine import castle_air
        return dict(castle_air.DATA['ages'][age]['travel'],full_body=True)
    return METRIC_DATA['observers'][age]['travel']


def envelope(metric):
    xs=[f[0] for f in metric['feet']];body=metric.get('body')
    if body:xs.extend([body['x'],body['x']+body['w']])
    return min(xs)-1,max(xs)+1


def support(pond,plan,root,metric,center):
    if not point(root):return False
    bx,by=castle.pitches(metric);left,right=envelope(metric)
    shape=dict(width=(right-left)*metric['scale'],height=4*metric['scale']/.675,floor=False)
    if not policy(pond).check('rock',(root[0]+(left+right)*bx/2)*20/132,root[1]*12/42,plan['instance'],shape)[0]:return False
    ground=castle.art_world(center,0,castle.GEOMETRY['ground_row'])[1]
    wall_left=castle.art_world(center,0,0)[0];wall_right=castle.art_world(center,castle.GEOMETRY['width'],0)[0]
    if root[1]<ground and wall_left-max(3,right)*bx<root[0]<wall_right+max(3,-left)*bx:return False
    return all(not terrain.water_at(pond.location,root[0]+f[0]*bx,root[1]+f[1]*by,pond.biome) for f in metric['feet'])


def samples(a,b):
    n=max(1,math.ceil(max(abs(a[i]-b[i]) for i in (0,1))/.2))
    return [[a[0]+(b[0]-a[0])*i/n,a[1]+(b[1]-a[1])*i/n] for i in range(n+1)]


def separated(a,am,b,bm):
    if am.get('full_body') or bm.get('full_body'):
        from engine import castle_air
        return not castle_air.overlap(castle_air.box(a,am),castle_air.box(b,bm),1.)
    ax=castle.pitches(am)[0];bx=castle.pitches(bm)[0];al,ar=envelope(am);bl,br=envelope(bm)
    return a[0]+ar*ax+1<b[0]+bl*bx or b[0]+br*bx+1<a[0]+al*ax or abs(a[1]-b[1])>3.5


def segment(pond,plan,a,b,metric,center,other=None):
    return all(support(pond,plan,p,metric,center) and (other is None or separated(p,metric,*other)) for p in samples(a,b))


def route(pond,plan,start,end,metric,center,other=None):
    for corner in ([start[0],end[1]],[end[0],start[1]]):
        path=[corner,list(end)];previous=start
        if all(segment(pond,plan,a,b,metric,center,other) for a,b in zip([previous]+path,path)):
            return [p for i,p in enumerate(path) if i==0 or p!=path[i-1]]
    return None


def route_ok(pond,plan,start,path,metric,center,other=None):
    return bool(path) and all(point(b) and segment(pond,plan,a,b,metric,center,other) for a,b in zip([start]+path,path))


def eligible(pond,live):
    if not live or live['cast'] not in METRICS:return False
    m=pond.minds;key=live['actor'];resident=m.model.residents.get(key)
    if not resident or resident['energy']<.4 or key in m.carnival_guests or m.encounter_for(key):return False
    if any(key in getattr(m,name) for name in RESERVED):return False
    from engine import playdates
    return (not playdates.active(m,key) and m.tasks.get(key,{}).get('action') in ('observe','share','restore','practice')
            and m.now>=m.carnival_retry.get(key,0))


def propose(pond,score,instance):
    """Pure all-role proposal; no task, target, lease, material or brain writes."""
    age=castle.canonical_age(pond.game.duck.growth_stage)
    if score not in castle.PHYSICAL_SCORES or age is None:return None,'This shared control needs a hatched observer and an authored score.'
    if pond.state.get('plan'):return None,'Finish the current activity before inviting an operator.'
    reason='No arrived, willing visitor can operate this control.'
    for live in actors.candidates(pond):
        if eligible(pond,live):
            proposal,reason=_propose_for(pond,score,instance,age,live)
            if proposal:return proposal,''
    return None,reason


def _propose_for(pond,score,instance,age,live):
    plan=dict(target='bounce_house',instance=instance);center=castle.placement_center(pond,plan)
    if center is None or 'bounce_house' not in pond.owned:return None,'That exact house is not placed here.'
    if not castle.allowed(pond,score):return None,'The weather does not allow this control work.'
    op=operator_travel(live['cast'],score);watch=cheese_metric(age,score);ground=math.ceil(castle.art_world(center,0,castle.GEOMETRY['ground_row'])[1])
    rows=operator_metrics(live['cast'],score);steps=castle.physical_stations(dict(id=score));sites=[]
    if score in castle.AIR_SCORES:
        from engine import castle_air
        sites,reason=castle_air.plan_sites(pond,plan,score,actors.identity(live))
        if sites is None:return None,reason
    else:
        for _,name in steps:
            target=castle.control_world(center,name);contacts=[m for m in rows if m['station']==name];bx=castle.pitches(op)[0]
            preferred=target[0]-(max(m['grip'][0] for m in contacts)+1)*bx
            candidates=sorted(([x,y] for x in range(math.floor(preferred)-4,math.ceil(preferred)+5) for y in range(ground,ground+4)),key=lambda r:(r[0]-preferred)**2+(r[1]-ground)**2)
            stance=next((r for r in candidates if support(pond,plan,r,op,center) and all(castle.reach_distance(r,target,m['grip'],m['scale'])<=3 for m in contacts)),None)
            if stance is None:return None,'The visitor cannot reach every '+name+' contact from dry ground.'
            sites.append(dict(station=name,target=target,stance=stance))
    oroot=live['root'];croot=cheese_root(pond)
    if not support(pond,plan,oroot,op,center) or not support(pond,plan,croot,watch,center):return None,'Both actors must start on supported exterior ground.'
    # Cheese arrives first; the held visitor cannot be crossed. Its later entire
    # itinerary must remain clear of the stationary observer's actual envelope.
    preferred=min(s['stance'][0] for s in sites)-14
    watches=sorted(([x,y] for x in range(max(8,int(preferred)-5),int(preferred)+6) for y in range(ground,ground+4)),key=lambda r:(r[0]-preferred)**2+(r[1]-ground-2)**2)
    # Preserve established proposals; farther-left observers are a fallback for
    # larger bodies whose approach cannot pass the initially held operator.
    watches+=sorted(([x,y] for x in range(8,max(8,int(preferred)-5)) for y in range(ground,ground+4)),key=lambda r:(r[0]-preferred)**2+(r[1]-ground-2)**2)
    for spot in watches:
        if not support(pond,plan,spot,watch,center):continue
        cr=route(pond,plan,croot,spot,watch,center,(oroot,op))
        if cr is None:continue
        paths=[];previous=oroot
        for site in sites:
            leg=route(pond,plan,previous,site['stance'],op,center,(spot,watch))
            if leg is None:break
            paths.append(leg);previous=site['stance']
        if len(paths)!=len(sites):continue
        oe=list(oroot)
        ox=route(pond,plan,previous,oe,op,center,(spot,watch))
        ce=[spot[0]-4,spot[1]+2];cx=route(pond,plan,spot,ce,watch,center,(oe,op))
        if ox is None or cx is None:continue
        operator=actors.identity(live)
        proposal=dict(operator=operator,source_age=age,cheese_identity=str(pond.game.duck.created_at),instance=instance,center=center,
                    roots=dict(operator=oroot,cheese=croot),sites=sites,operator_routes=paths,operator_exit_route=ox,
                    cheese_route=cr,cheese_exit_route=cx,watch=spot,operator_exit=oe,cheese_exit=ce)
        proposal['required_seconds']=required_seconds(proposal,score)
        if live['adapter']=='rare':
            proposal['remaining_seconds']=live['remaining_seconds']
            if live['remaining_seconds']<proposal['required_seconds']:return None,'The visitor cannot finish both routes before departure.'
        return proposal,''
    return None,'The operator and observer have no separate safe approach, working corridor and exits.'


def required_seconds(proposal,score):
    def length(start,paths):
        total=0
        for path in paths:
            for end in path:
                total+=math.hypot(end[0]-start[0],2*(end[1]-start[1]));start=end
        return total
    operator=proposal['operator'];pace=3.5 if operator['adapter']=='story' else guest_profile(operator['cast'])['pace']*.72*.8
    travel=length(proposal['roots']['operator'],proposal['operator_routes']+[proposal['operator_exit_route']])/pace
    watch=length(proposal['roots']['cheese'],[proposal['cheese_route'],proposal['cheese_exit_route']])
    return travel+watch+castle.ROUTINES[score]['duration']+12


def prepare(pond,plan,proposal=None):
    w=plan['carnival_work']
    # Parent preflights before installing plan. Revalidate that immutable proposal
    # against actual roots without clearing/replacing any prior ownership.
    if proposal is None:return False,'A shared activity needs an atomic preflight proposal.'
    live=actors.live(pond,proposal['operator']);age=castle.canonical_age(pond.game.duck.growth_stage)
    if (not live or not eligible(pond,live) or proposal['instance']!=plan.get('instance') or age!=proposal['source_age']
        or any(live[k]!=v for k,v in proposal['operator'].items()) or live['root']!=proposal['roots']['operator']
        or cheese_root(pond)!=proposal['roots']['cheese'] or castle.placement_center(pond,plan)!=proposal['center']):return False,'The shared proposal changed before acquisition.'
    if live['adapter']=='rare' and live['remaining_seconds']<required_seconds(proposal,w['id']):return False,'The visitor no longer has enough time.'
    s=copy.deepcopy(proposal);s.update(version=1,attempt=uuid.uuid4().hex,phase='waiting')
    s['cheese']=dict(root=cheese_root(pond),stance=s['watch'],exit=s['cheese_exit'],phase='approach',ready=False,route=s['cheese_route'],waypoint=0)
    site=s['sites'][0];ph=dict(version=1,actor=live['actor'],root=list(live['root']),target=site['target'],stance=site['stance'],center=s['center'],station=site['station'],station_index=0,phase='approach',route=s['operator_routes'][0],waypoint=0,exit=s['operator_exit'],contact_ready=False)
    if 'observation_target' in site:ph['observation_target']=site['observation_target']
    # Recheck all preflight legs before acquiring either actor.
    if not proposal_clear(pond,plan,s):return False,'The shared routes changed before acquisition.'
    w.update(shared=s,physical=ph,shared_physical=True,physical_pilot=False,source_age=age,paired=True,invitation_checked=True)
    m=pond.minds;key=live['actor'];m.carnival_guests[key]=dict(actor=key,work=w,attempt=s['attempt'],shared=True,contract={k:copy.deepcopy(s[k]) for k in IMMUTABLE},finished=False,phase='approach',spot=list(live['root']),target=list(live['root']),token=live['token'],location=pond.location,mode='operator',overlap=0.,contexts={k:m.context(k) for k in ('cheese',key)})
    m.tasks.pop(key,None);w['companion']=dict(actor=key,mode='operator',ready=False);plan['approach_destination']=list(s['watch']);pond._cache=None
    return True,''


def proposal_clear(pond,plan,s):
    op=operator_travel(s['operator']['cast'],plan['carnival_work']['id']);watch=cheese_metric(s['source_age'],plan['carnival_work']['id']);center=s['center'];spot=s['watch']
    if not route_ok(pond,plan,s['roots']['cheese'],s['cheese_route'],watch,center,(s['roots']['operator'],op)):return False
    previous=s['roots']['operator']
    for leg in s['operator_routes']:
        if not route_ok(pond,plan,previous,leg,op,center,(spot,watch)):return False
        previous=leg[-1]
    return (route_ok(pond,plan,previous,s['operator_exit_route'],op,center,(spot,watch))
            and route_ok(pond,plan,spot,s['cheese_exit_route'],watch,center,(s['operator_exit'],op)))


def validate(pond,plan):
    try:
        w=plan['carnival_work'];s=w['shared'];ph=w['physical'];live=actors.live(pond,s.get('operator') if isinstance(s,dict) else None)
        if not isinstance(s,dict) or not isinstance(ph,dict) or not isinstance(s.get('operator'),dict) or not isinstance(s.get('cheese'),dict):return False
        if any(not isinstance(v,str) for v in s['operator'].values()):return False
        if w.get('shared_physical') is not True or w.get('physical_pilot') is not False or s['version']!=1 or w['id'] not in castle.PHYSICAL_SCORES:return False
        if not live or any(live[k]!=v for k,v in s['operator'].items()) or ph['actor']!=live['actor']:return False
        if str(pond.game.duck.created_at)!=s['cheese_identity'] or castle.canonical_age(pond.game.duck.growth_stage)!=s['source_age']:return False
        if plan['instance']!=s['instance'] or castle.placement_center(pond,plan)!=s['center'] or pond.location!=s['operator']['location']:return False
        lease=pond.minds.carnival_guests.get(live['actor'])
        if not lease or lease['work'] is not w or lease.get('attempt')!=s['attempt']:return False
        if any(s.get(k)!=lease['contract'].get(k) for k in IMMUTABLE):return False
        if w.get('source_age')!=s['source_age'] or w.get('interrupted') or s['phase'] not in ('waiting','operate','exit','done'):return False
        duration=castle.ROUTINES[w['id']]['duration'];elapsed=w['ride_elapsed']
        if type(elapsed) not in (int,float) or not math.isfinite(elapsed) or not 0<=elapsed<=duration:return False
        if not isinstance(w.get('events'),list) or any(type(i) is not int for i in w['events']):return False
        if w['events']!=[i for i,e in enumerate(castle.ROUTINES[w['id']]['effects']) if e[0]*duration<=elapsed]:return False
        cursor=max(i for i,(at,_) in enumerate(castle.physical_stations(w)) if at*duration<=elapsed)
        if ph['station_index']!=cursor or ph['station']!=s['sites'][cursor]['station'] or ph['target']!=castle.control_world(s['center'],ph['station']) or ph['stance']!=s['sites'][cursor]['stance']:return False
        if w['id']=='castle_gauge_check':
            from engine import castle_air
            if ph.get('observation_target')!=castle_air.observation_target(s['center']):return False
        if ph['center']!=s['center'] or ph['phase'] not in ('approach','hold','exit') or s['cheese']['phase'] not in ('approach','hold','exit'):return False
        expected_route=s['operator_exit_route'] if ph['phase']=='exit' else s['operator_routes'][cursor]
        if ph['route']!=expected_route or ph['exit']!=s['operator_exit']:return False
        if s['cheese']['route']!=(s['cheese_exit_route'] if s['cheese']['phase']=='exit' else s['cheese_route']) or s['cheese']['stance']!=s['watch'] or s['cheese']['exit']!=s['cheese_exit']:return False
        for record in (ph,s['cheese']):
            if not isinstance(record['route'],list) or not record['route'] or not all(point(p) for p in record['route']):return False
            if not point(record['root']) or not point(record['stance']) or not point(record['exit']) or type(record['waypoint']) is not int or not 0<=record['waypoint']<len(record['route']):return False
        if s['phase'] in ('exit','done') and (ph['phase']!='exit' or s['cheese']['phase']!='exit'):return False
        if s['phase']=='waiting' and (w['stage']!='queue' or elapsed!=0 or ph['phase']!='approach'):return False
        if s['phase']=='operate' and (w['stage'] not in ('queue','service') or s['cheese']['phase']!='hold' or not s['cheese']['ready']):return False
        if s['phase']=='done':return lease.get('finished') is True and w.get('done') is True and w['stage']=='done' and elapsed==duration and w['clock']==0
        if s['phase']=='exit':return not w.get('done') and w['stage']=='service_exit' and elapsed==duration and w['clock']==0
        return not w.get('done') and w['clock']==elapsed
    except (KeyError,TypeError,ValueError,IndexError,AttributeError):return False


def paused(pond,plan):return bool(plan.get('paused') or not pond.available() or pond.game.duck.current_action in ('feed','play','clean','pet','sleep'))


def interrupt(pond,plan,reason):
    w=plan.get('carnival_work') if isinstance(plan,dict) else None
    if not isinstance(w,dict):return False
    w.update(done=True,interrupted=True,physical_error=reason)
    s=w.get('shared')
    if isinstance(s,dict):s['phase']='interrupted'
    if isinstance(w.get('physical'),dict):w['physical']['contact_ready']=False
    # Rejected wire data is untrusted. Release only actual leases bound by work
    # identity, never a forged actor field or a replacement visitor's token.
    for key,lease in list(pond.minds.carnival_guests.items()):
        if not isinstance(lease,dict):
            pond.minds.carnival_guests.pop(key,None);continue
        if lease.get('work') is w:
            pond.minds.carnival_guests.pop(key,None)
            if isinstance(key,str):actors.release_owned(pond,key,lease)
    w.pop('companion',None)
    try:castle.clear(pond,plan)
    except (KeyError,TypeError,ValueError,AttributeError):pass
    pos=pond.game.renderer.duck_pos;pos.cancel_movement();pos.set_state_by_name('thinking',0);pond._cache=None
    return False


def cancel(pond,plan):return interrupt(pond,plan,'Shared work was set aside.')


def refresh(pond):
    plan=pond.state.get('plan');w=plan.get('carnival_work',{}) if plan else {}
    if not isinstance(w,dict) or not ('shared_physical' in w or 'shared' in w):return
    if not validate(pond,plan):interrupt(pond,plan,'The shared actor, visit, age or placement changed.');return
    if not castle.allowed(pond,w['id']) or pond.game.duck.needs.energy<10 or pond.game.duck.needs.hunger<15:
        interrupt(pond,plan,'Weather or urgent care interrupted shared work.');return
    s=w['shared'];ph=w['physical'];live=actors.live(pond,s.get('operator') if isinstance(s,dict) else None);op=operator_travel(live['cast'],w['id']);watch=cheese_metric(s['source_age'],plan['carnival_work']['id']);cr=cheese_root(pond);orr=live['root'];lease=pond.minds.carnival_guests[live['actor']]
    if not segment(pond,plan,ph['root'],orr,op,s['center'],(cr,watch)) or not segment(pond,plan,s['cheese']['root'],cr,watch,s['center'],(orr,op)):
        interrupt(pond,plan,'An actual actor segment lost support or crossed the other actor.');return
    ph['root']=list(orr);s['cheese']['root']=list(cr);ph['contact_ready']=False
    stop=paused(pond,plan) or s['phase']=='done'
    operator_wait=stop or (s['phase']=='waiting' and not s['cheese']['ready']) or ph['phase']=='hold' or (s['phase']=='exit' and ph.get('exited'))
    ot=orr if operator_wait else ph['route'][ph['waypoint']]
    cheese_wait=stop or s['cheese']['phase']=='hold' or (s['phase']=='exit' and not ph.get('exited')) or s['cheese'].get('exited')
    ct=cr if cheese_wait else s['cheese']['route'][s['cheese']['waypoint']]
    if not segment(pond,plan,orr,ot,op,s['center'],(cr,watch)) or not segment(pond,plan,cr,ct,watch,s['center'],(orr,op)):
        interrupt(pond,plan,'The next shared route segment is blocked.');return
    lease['target']=list(ot);lease['spot']=list(ot)
    pos=pond.game.renderer.duck_pos
    if cheese_wait:
        current=pos._state_str;pos.cancel_movement();pos.set_state_by_name(current if pond.game.duck.current_action in ('feed','play','clean','pet','sleep') and current in pos.ANIMATABLE_STATES else 'thinking',0)
    elif not pos._is_directed_movement or [pos.target_x,pos.target_y]!=ct:pos.move_to(*ct)
    if not stop and (s['cheese']['phase']=='hold' or s['cheese'].get('exited')):
        pos.facing_right=orr[0]>=cr[0]
    if s['phase']=='done':pos.facing_right=orr[0]>=cr[0]
    if not stop and s['phase']=='operate' and ph['phase']=='hold':
        if w['id'] in castle.AIR_SCORES:
            from engine import castle_air
            if near(cr,s['cheese']['stance'],.51) and pos.facing_right==(orr[0]>=cr[0]):
                castle_air.station_ready(pond,plan,s['operator'],ph,w['id'],[castle_air.box(cr,watch)])
        else:
            contacts=[m for m in operator_metrics(live['cast'],w['id']) if m['station']==ph['station']]
            ph['contact_ready']=bool(live['facing'] and near(orr,ph['stance']) and near(cr,s['cheese']['stance'],.51)
                and pos.facing_right==(orr[0]>=cr[0]) and all(castle.reach_distance(orr,ph['target'],m['grip'],m['scale'])<=3 for m in contacts))


def motion(minds,key):
    lease=minds.carnival_guests.get(key)
    if not lease or not lease.get('shared'):return None
    return dict(target=list(lease['target']),phase=lease['phase'],facing=True,gesture='idle',owner=lease['attempt'])


def arrived(record,root,tolerance=1e-7):
    if not near(root,record['route'][record['waypoint']],tolerance):return False
    if record['waypoint']+1<len(record['route']):record['waypoint']+=1;return False
    return True


def advance(pond,plan,dt):
    w=plan['carnival_work']
    if not validate(pond,plan):return interrupt(pond,plan,'The shared reservation is invalid.')
    refresh(pond)
    if w.get('interrupted'):return False
    if paused(pond,plan):return True
    s=w['shared'];ph=w['physical'];ch=s['cheese'];live=actors.live(pond,s.get('operator') if isinstance(s,dict) else None);orr=live['root'];cr=cheese_root(pond);lease=pond.minds.carnival_guests[live['actor']]
    s['waited']=s.get('waited',0)+max(0,excursions.finite(dt))
    if s['waited']>600:return interrupt(pond,plan,'The shared route could not be completed.')
    if s['phase']=='done':return False
    if s['phase']=='waiting':
        if not ch['ready']:
            if arrived(ch,cr,.51):ch.update(phase='hold',ready=True)
            return True
        if arrived(ph,orr):ph['phase']='hold';s['phase']='operate';lease['phase']='ready'
        else:return True
    if s['phase']=='exit':
        if not ph.get('exited'):
            if arrived(ph,orr):ph['exited']=True
            return True
        if arrived(ch,cr,.51):
            ch['exited']=True;s['phase']='done';lease['finished']=True;w.update(stage='done',done=True);castle.clear(pond,plan);refresh(pond);return False
        return True
    if ph['phase']=='approach':
        if not arrived(ph,orr):return True
        ph['phase']='hold'
    if not near(cr,ch['stance'],.51) or not live['facing'] or pond.game.renderer.duck_pos.facing_right!=(orr[0]>=cr[0]):return True
    metricrows=operator_metrics(live['cast'],w['id']);current=[m for m in metricrows if m['station']==ph['station'] and 'grip' in m]
    if not near(orr,ph['stance']) or not all(castle.reach_distance(orr,ph['target'],m['grip'],m['scale'])<=3 for m in current):return interrupt(pond,plan,'The real operator cannot reach this control.')
    ph['contact_ready']=w['id']!='castle_gauge_check'
    ph['observation_ready']=False
    if plan['phase']!='act':return True
    from engine import carnival
    cursor=ph['station_index'];steps=castle.physical_stations(w)
    status,reason=advance_control_clock(pond,plan,dt,lambda:actors.live(pond,s['operator']),lambda:proposal_clear(pond,plan,s))
    if w['events']:s['cheese']['reaction_event']=w['events'][-1]
    if status=='blocked':return interrupt(pond,plan,reason)
    if status=='transfer':
        site=s['sites'][cursor+1]
        if 'observation_target' in site:ph['observation_target']=site['observation_target']
        ph.update(station_index=cursor+1,station=site['station'],target=site['target'],stance=site['stance'],phase='approach',route=s['operator_routes'][cursor+1],waypoint=0,contact_ready=False)
    elif status=='exit':
        s['phase']='exit';ph.update(phase='exit',route=s['operator_exit_route'],waypoint=0,contact_ready=False);ch.update(phase='exit',route=s['cheese_exit_route'],waypoint=0,ready=False);carnival.stage(w,'service_exit',0)
    pond._cache=None
    return True


def advance_control_clock(pond,plan,dt,resolve_actor,preflight):
    """Consume only the existing bounded control clock; no movement or rewards."""
    from engine import carnival
    w=plan['carnival_work'];s=w['shared'];ph=w['physical']
    if w['id'] in castle.AIR_SCORES:
        from engine import castle_air
        obstacles=[]
        if 'cheese' in s:obstacles=[castle_air.box(cheese_root(pond),cheese_metric(s['source_age'],w['id']))]
        elif 'recipient' in s:
            from engine import egg_caregiver
            obstacles=[egg_caregiver.box(s['recipient']['root'],egg_caregiver.metric(s['recipient']))]
        answer=castle_air.advance_atomic(pond,plan,w,dict(operator=s['operator'],physical=ph,preflight=preflight,obstacles=obstacles),dt)
        w['done']=False
        return ('exit' if answer['status']=='finished' else answer['status']),answer['reason']
    metricrows=operator_metrics(s['operator']['cast'],w['id'])
    obj=pond.object_state('bounce_house',plan)
    if w['stage']=='queue':w['start']=copy.deepcopy(castle.state(obj));carnival.stage(w,'service',castle.ROUTINES[w['id']]['duration'])
    spec=castle.ROUTINES[w['id']];duration=spec['duration'];cursor=ph['station_index'];steps=castle.physical_stations(w);boundary=steps[cursor+1][0]*duration if cursor+1<len(steps) else duration
    remaining=max(0,excursions.finite(dt));castle.state(obj)['active']=True
    while remaining>0 and w['clock']<boundary:
        old=w['clock'];upcoming=[e[0]*duration for i,e in enumerate(spec['effects']) if i not in w['events'] and e[0]*duration>old];stop=min([old+remaining,boundary]+upcoming)
        if stop<=old:break
        step=stop-old;w['clock']=stop;w['ride_elapsed']=stop;w['elapsed']+=step;remaining-=step
        for i,e in enumerate(spec['effects']):
            if old<e[0]*duration<=stop:
                if i==0 and not preflight():return 'blocked','A future shared route is no longer safe.'
                metric=metricrows[i];actual=resolve_actor()
                if not actual or not near(actual['root'],ph['stance']) or castle.reach_distance(actual['root'],ph['target'],metric['grip'],metric['scale'])>3:return 'blocked','The operator lost its actual contact stance.'
                if w['id']=='castle_hose_stow' and e[1]=='hose' and (0 not in w['events'] or obj['castle']['motor']!='off'):return 'blocked','The blower must stop before the hose is coiled.'
                castle.apply(obj,w,i,e)
    if w['clock']>=boundary and cursor+1<len(steps):return 'transfer',''
    if w['clock']>=duration:return 'exit',''
    return 'hold',''


def completion_ready(pond,plan):
    from engine import castle_air
    if not castle_air.receipt_ready(pond,plan):return False
    if not validate(pond,plan):return False
    w=plan['carnival_work'];s=w['shared'];ph=w['physical'];live=actors.live(pond,s.get('operator') if isinstance(s,dict) else None)
    return bool(not w.get('recorded') and s['phase']=='done' and ph.get('exited') and s['cheese'].get('exited') and near(live['root'],ph['exit']) and near(cheese_root(pond),s['cheese']['exit'],.51) and pond.game.renderer.duck_pos.facing_right==(live['root'][0]>=cheese_root(pond)[0])
                and support(pond,plan,live['root'],operator_travel(live['cast'],w['id']),s['center']) and support(pond,plan,cheese_root(pond),cheese_metric(s['source_age'],w['id']),s['center']))


def complete(pond,plan):
    if plan.get('carnival_work',{}).get('id')=='castle_gauge_check':
        from engine import castle_air
        return castle_air.complete_observation(pond,plan)
    if not completion_ready(pond,plan):return False
    w=plan['carnival_work'];s=w['shared'];m=pond.minds;key=s['operator']['actor'];lease=m.carnival_guests[key];w['recorded']=True
    obj=pond.object_state('bounce_house',plan);history=obj.setdefault('carnival_routines',{});history[w['id']]=min(9999,history.get(w['id'],0)+1);company=obj.setdefault('carnival_company',{});company[key]=min(9999,company.get(key,0)+1)
    note=m.model.residents[key]['name']+' operated '+w['label']+' while Cheese watched the real controls.'
    m.model.learn(key,'practice',lease['contexts'][key],.25,m.now,note,'cheese');m.model.learn('cheese','observe',lease['contexts']['cheese'],.25,m.now,note,key)
    for actor,other in ((key,'cheese'),('cheese',key)):
        m.model.learn(actor,'share',lease['contexts'][actor],.25,m.now,note,other);m.model.bond(actor,other,.18,m.now,note)
    pond.remember('belongings',w['label']+'.',.5,plan['target']);pond.remember('neighbors',note,.6,key)
    m.carnival_guests.pop(key,None);actors.release_owned(pond,key,lease);pond._cache=None;return True


def view(pond,plan):
    raw=plan.get('carnival_work') if isinstance(plan,dict) else None
    if not isinstance(raw,dict):return {}
    w=copy.deepcopy(raw)
    if not validate(pond,plan):
        # Snapshots can run before the next host validation. Keep shared intent
        # explicit but remove invalid geometry rather than falling back to legacy.
        w.update(shared_physical=True,physical={},shared={})
        return w
    s=w['shared'];ph=w['physical'];live=actors.live(pond,s.get('operator') if isinstance(s,dict) else None)
    root=live['root']
    if ph.get('root')!=root:ph['contact_ready']=False
    ph['root']=list(root);s['cheese']['root']=cheese_root(pond)
    return w
