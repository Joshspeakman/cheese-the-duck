"""Cheese operates real controls while an independently arriving Flutter observes.

No flight feet or grip exist. Full airborne ink bounds reserve the observer's
corridor; the existing native Cheese scheduler alone consumes mechanical effects.
"""
import copy,json,math,uuid
from pathlib import Path
from engine import castle_work as castle,castle_shared as shared,castle_actors as actors
from engine.portable_ground import policy
from engine.pond_layout import bounds,FOOTPRINTS
from world.guest_cast import guest_profile

METRIC=json.loads((Path(__file__).parent/'client/animation/castle-flight-metrics.json').read_text())
SCENERY=json.loads((Path(__file__).parent/'client/animation/castle-scenery-metrics.json').read_text())
IMMUTABLE=('score','mode','operator','observer','source_age','cheese_identity','instance','center','sites','cheese_route','cheese_exit','roots','hover','flight_route','flight_exit_route','flight_exit')


def live(pond,s):
    a=actors.flight(pond)
    return a if a and actors.identity(a)==s.get('observer') else None


def box(root,metric):
    bx,by=castle.pitches(metric);b=metric['body']
    return [root[0]+b['x']*bx,root[1]+b['y']*by,b['w']*bx,b['h']*by]


def overlap(a,b,pad=.25):
    return a[0]<b[0]+b[2]+pad and a[0]+a[2]+pad>b[0] and a[1]<b[1]+b[3]+pad and a[1]+a[3]+pad>b[1]


def cheese_root(pond):
    try:
        root=shared.cheese_root(pond)
        return root if shared.point(root) else None
    except (TypeError,ValueError,AttributeError):return None


def body(pond,root,age,score=None):
    from engine import castle_air
    return box(root,castle_air.DATA['ages'][age]['travel'] if score in castle.AIR_SCORES else METRIC['operators'][age])


def outfitted(pond):
    from engine.scene import equipped_wearables
    return any(equipped_wearables(pond.game).values())


def third_actor(pond):return bool(pond.game.friends.current_visit or pond.state.get('story'))


def weather_ok(pond):
    ecology=pond.state.get('ecology');wind=ecology.get('wind') if isinstance(ecology,dict) else None
    return (type(wind) in (int,float) and math.isfinite(wind) and 0<=wind<.5 and isinstance(pond.weather_type,str)
            and not any(w in pond.weather_type for w in ('rain','storm','snow','blizzard','gale','tornado','hurricane')))


def flight_clear(pond,plan,root,center,cheese=None):
    if not shared.point(root):return False
    b=box(root,METRIC);pos=pond.game.renderer.duck_pos
    if b[0]<2 or b[1]<2 or b[0]+b[2]>pos._play_width-8 or b[1]+b[3]>pos._play_height-5:return False
    top=castle.art_world(center,0,0);bottom=castle.art_world(center,castle.GEOMETRY['width'],castle.GEOMETRY['ground_row'])
    if overlap(b,[top[0],top[1],bottom[0]-top[0],bottom[1]-top[1]]):return False
    # Reserve the blower's approach and exhaust even before start turns it on.
    grill=castle.control_world(center,'grill')
    if overlap(b,[grill[0]-6,grill[1]-6,12,12]):return False
    layout=policy(pond)
    for item,x,y,shape in layout.occupied(instance=plan['instance']):
        if shape is None and item not in FOOTPRINTS:return False
        try:obstacle=bounds(item,x,y,shape)
        except (TypeError,ValueError,KeyError):return False
        if not shared.point([obstacle['x'],obstacle['y']]) or not shared.point([obstacle['w'],obstacle['h']]) or min(obstacle['w'],obstacle['h'])<=0:return False
        if not obstacle['floor'] and overlap(b,[obstacle['x']*132/20,obstacle['y']*42/12,obstacle['w']*132/20,obstacle['h']*42/12]):return False
    if pond.location!=SCENERY['location']:return False
    for feature in SCENERY['features']:
        obstacle=feature['bounds']
        if overlap(b,[obstacle['x'],obstacle['y'],obstacle['w'],obstacle['h']]):return False
    return cheese is None or not overlap(b,body(pond,cheese,plan['carnival_work']['source_age'],plan['carnival_work']['id']))


def flight_segment(pond,plan,a,b,center,cheese):
    return all(flight_clear(pond,plan,r,center,cheese) for r in shared.samples(a,b))


def cheese_segment(pond,plan,a,b,center,hover):
    if not castle.segment_clear(pond,plan,a,b,center):return False
    # Union of continuous sweep plus native diagonal unit positions.
    points=shared.samples(a,b);p=list(a)
    for _ in range(180):
        points.append(p)
        if shared.near(p,b,.51):break
        p=[p[i]+(1 if p[i]<b[i] else -1 if p[i]>b[i] else 0) for i in (0,1)]
    return all(not overlap(box(hover,METRIC),body(pond,r,plan['carnival_work']['source_age'],plan['carnival_work']['id'])) for r in points)


def willing(pond,a):
    if not a:return False
    m=pond.minds;key=a['actor'];resident=m.model.residents.get(key)
    if not resident or resident['energy']<.4 or key in m.carnival_guests or m.encounter_for(key):return False
    from engine import playdates
    return (not any(key in getattr(m,n) for n in shared.RESERVED) and not playdates.active(m,key)
            and m.tasks.get(key,{}).get('action') in ('observe','share','restore','practice') and m.now>=m.carnival_retry.get(key,0))


def proposal_clear(pond,plan,s):
    previous=s['roots']['observer']
    for end in s['flight_route']:
        if not flight_segment(pond,plan,previous,end,s['center'],s['roots']['cheese']):return False
        previous=end
    previous=s['roots']['cheese']
    for end in s['cheese_route']+[v['stance'] for v in s['sites'][1:]]+[s['cheese_exit']]:
        if not cheese_segment(pond,plan,previous,end,s['center'],s['hover']):return False
        previous=end
    previous=s['hover']
    for end in s['flight_exit_route']:
        if not flight_segment(pond,plan,previous,end,s['center'],s['cheese_exit']):return False
        previous=end
    return True


def propose(pond,score,instance):
    age=castle.canonical_age(pond.game.duck.growth_stage);a=actors.flight(pond)
    if pond.location!=SCENERY['location']:return None,'Flutter needs an authored flight corridor in this location.'
    if outfitted(pond):return None,'Flutter needs more clearance around that outfit; try these controls solo for now.'
    if cheese_root(pond) is None:return None,'Cheese needs a valid actual ground position.'
    if age is None or score not in castle.PHYSICAL_SCORES:return None,'Flutter needs a hatched control operator.'
    if pond.state.get('plan') or third_actor(pond) or not willing(pond,a):return None,'No free, arrived Flutter can join this work.'
    if not weather_ok(pond) or not castle.allowed(pond,score):return None,'Flutter needs calm, dry flying weather.'
    plan=dict(target='bounce_house',instance=instance);plan['carnival_work']=castle.make(pond,plan,score)
    center=castle.placement_center(pond,plan)
    if not shared.point(center) or 'bounce_house' not in pond.owned:return None,'That exact house is not placed here.'
    sites,missing=castle.physical_sites(pond,plan,center)
    if not sites:return None,'Cheese cannot reach every '+str(missing)+' contact.'
    cr=cheese_root(pond);ground=castle.art_world(center,0,castle.GEOMETRY['ground_row'])[1]
    entry=castle.art_world(center,castle.GEOMETRY['entry']['x'],castle.GEOMETRY['ground_row']);exit_point=[round(entry[0]),math.ceil(ground)]
    route=castle.physical_route(cr,sites[0]['stance'],exit_point,ground,'initial')
    left=castle.art_world(center,0,0)[0]
    candidates=sorted(([x,y] for x in range(8,max(9,math.floor(left)-3)) for y in range(10,35)),key=lambda r:(r[0]-left+8)**2+(r[1]-ground-3)**2)
    for hover in candidates:
        if not flight_clear(pond,plan,hover,center,cr):continue
        for corner in ([a['root'][0],hover[1]],[hover[0],a['root'][1]]):
            s=dict(score=score,mode='flight-observer',operator=dict(actor='cheese',adapter='cheese',source_age=age),observer=actors.identity(a),source_age=age,cheese_identity=str(pond.game.duck.created_at),instance=instance,center=center,sites=sites,cheese_route=route,cheese_exit=exit_point,roots=dict(cheese=cr,observer=a['root']),hover=hover,flight_route=[corner,hover],flight_exit_route=[corner,a['root']],flight_exit=a['root'])
            if not proposal_clear(pond,plan,s):continue
            def length(start,points):return sum(math.hypot(b[0]-a[0],2*(b[1]-a[1])) for a,b in zip([start]+points,points))
            s['required_seconds']=(length(a['root'],s['flight_route'])+length(hover,s['flight_exit_route']))/(guest_profile('butterfly_fairy')['pace']*.72*.8)+length(cr,route+[v['stance'] for v in sites[1:]]+[exit_point])+castle.ROUTINES[score]['duration']+12
            s['remaining_seconds']=a['remaining_seconds']
            if a['remaining_seconds']<s['required_seconds']:return None,'Flutter cannot finish both flights before departure.'
            return s,''
    return None,'Flutter has no clear independent flight corridor and hover space.'


def prepare(pond,plan,proposal=None):
    if cheese_root(pond) is None:return False,'Cheese needs a valid actual ground position.'
    if outfitted(pond):return False,'Flutter needs more clearance around that outfit.'
    if not isinstance(proposal,dict):return False,'A flight companion needs an atomic proposal.'
    a=live(pond,proposal);w=plan['carnival_work']
    if (w.get('id')!=proposal.get('score') or w.get('source_age')!=proposal.get('source_age') or plan.get('instance')!=proposal.get('instance') or pond.state.get('plan') or third_actor(pond) or not a or not willing(pond,a) or a['remaining_seconds']<proposal['required_seconds'] or a['root']!=proposal['roots']['observer'] or cheese_root(pond)!=proposal['roots']['cheese']
        or castle.canonical_age(pond.game.duck.growth_stage)!=proposal['source_age'] or castle.placement_center(pond,plan)!=proposal['center'] or not weather_ok(pond) or not proposal_clear(pond,plan,proposal)):return False,'The flight proposal changed before acquisition.'
    if castle.physical_sites(pond,plan,proposal['center'])[0]!=proposal['sites']:return False,'The required control stances changed.'
    # Install the already validated native reservation directly. Calling the
    # standalone prepare here would cancel an unrelated roaming target on its
    # failure path; no live movement changes until every pure check succeeds.
    site=proposal['sites'][0]
    w['physical']=dict(version=1,actor='cheese',source_age=proposal['source_age'],center=proposal['center'],root=list(proposal['roots']['cheese']),target=site['target'],stance=site['stance'],phase='approach',station=site['station'],station_index=0,contact_ready=False,route=proposal['cheese_route'],waypoint=0,route_origin=list(proposal['roots']['cheese']),route_kind='initial',exit=proposal['cheese_exit'],travel_time=0.)
    if 'observation_target' in site:w['physical']['observation_target']=site['observation_target']
    plan['approach_destination']=list(site['stance'])
    s=copy.deepcopy(proposal);s.update(version=1,attempt=uuid.uuid4().hex,phase='waiting')
    s['observer_physical']=dict(root=list(a['root']),stance=list(s['hover']),exit=list(s['flight_exit']),phase='approach',route=s['flight_route'],waypoint=0,ready=False)
    w.update(shared=s,flight_observer=True,shared_physical=True,physical_pilot=True,paired=True,invitation_checked=True,companion=dict(actor=a['actor'],mode='observer',ready=False))
    m=pond.minds;key=a['actor'];m.carnival_guests[key]=dict(actor=key,work=w,attempt=s['attempt'],shared=True,flight=True,contract={k:copy.deepcopy(s[k]) for k in IMMUTABLE},target=list(a['root']),phase='approach',token=a['token'],contexts={k:m.context(k) for k in ('cheese',key)})
    m.tasks.pop(key,None);castle.physical_pause(pond,plan);pond._cache=None
    return True,''


def validate(pond,plan):
    try:
        w=plan['carnival_work'];s=w['shared'];a=live(pond,s);o=s['observer_physical'];lease=pond.minds.carnival_guests.get('butterfly_fairy')
        if w.get('flight_observer') is not True or w.get('shared_physical') is not True or w.get('physical_pilot') is not True or s['version']!=1 or s['mode']!='flight-observer':return False
        if cheese_root(pond) is None or outfitted(pond) or third_actor(pond) or not a or not isinstance(lease,dict) or lease.get('work') is not w or lease.get('attempt')!=s['attempt'] or any(s.get(k)!=lease['contract'].get(k) for k in IMMUTABLE):return False
        if not castle.physical_geometry_ok(pond,plan) or str(pond.game.duck.created_at)!=s['cheese_identity'] or s['source_age']!=w['source_age'] or w.get('interrupted'):return False
        if s['phase'] not in ('waiting','operate','exit','done') or o['phase'] not in ('approach','hold','exit') or not all(shared.point(o[k]) for k in ('root','stance','exit')):return False
        expected=s['flight_exit_route'] if o['phase']=='exit' else s['flight_route']
        if o['route']!=expected or not all(shared.point(p) for p in o['route']) or type(o['waypoint']) is not int or not 0<=o['waypoint']<len(o['route']) or o['stance']!=s['hover'] or o['exit']!=s['flight_exit']:return False
        if w['physical']['stance']!=s['sites'][w['physical']['station_index']]['stance']:return False
        if s['phase']=='waiting':return o['phase']=='approach' and not o['ready'] and w['stage']=='queue' and w['clock']==0 and w['physical']['phase']=='approach'
        if s['phase']=='operate':return o['phase']=='hold' and o['ready'] is True and not w['done']
        return w['done'] is True and o['phase']=='exit' and (s['phase']!='done' or o.get('exited') is True)
    except (KeyError,ValueError,TypeError,IndexError,AttributeError):return False


def interrupt(pond,plan,reason):
    w=plan.get('carnival_work') if isinstance(plan,dict) else None
    if not isinstance(w,dict):return False
    w.update(done=True,interrupted=True,physical_error=reason)
    s=w.get('shared')
    if isinstance(s,dict):s['phase']='interrupted'
    if isinstance(w.get('physical'),dict):w['physical']['contact_ready']=False
    for key,lease in list(pond.minds.carnival_guests.items()):
        if not isinstance(lease,dict):
            pond.minds.carnival_guests.pop(key,None);continue
        if lease.get('work') is w:
            pond.minds.carnival_guests.pop(key,None);pond.game.guest_motion.release_meeting(lease.get('attempt'))
    w.pop('companion',None)
    try:castle.clear(pond,plan)
    except (KeyError,TypeError,ValueError,AttributeError):pass
    pos=pond.game.renderer.duck_pos;pos.cancel_movement();pos.set_state_by_name('thinking',0);pond._cache=None
    return False


def refresh(pond):
    plan=pond.state.get('plan');w=plan.get('carnival_work',{}) if plan else {}
    from engine import carnival
    if not carnival.is_flight(plan):return
    if outfitted(pond):interrupt(pond,plan,'Flutter needs more clearance around that outfit.');return
    if not validate(pond,plan):interrupt(pond,plan,'The flight reservation changed.');return
    if not weather_ok(pond) or not castle.allowed(pond,w['id']) or pond.game.duck.needs.energy<10 or pond.game.duck.needs.hunger<15:interrupt(pond,plan,'Weather or urgent care interrupted the flight.');return
    s=w['shared'];o=s['observer_physical'];a=live(pond,s);cr=cheese_root(pond);ph=w['physical'];lease=pond.minds.carnival_guests[a['actor']]
    if not flight_segment(pond,plan,o['root'],a['root'],s['center'],cr) or not cheese_segment(pond,plan,ph['root'],cr,s['center'],a['root']):interrupt(pond,plan,'An actual flight or walking segment lost clearance.');return
    o['root']=list(a['root']);ph['root']=list(cr);stop=shared.paused(pond,plan)
    target=a['root'] if stop or o['phase']=='hold' or s['phase']=='done' else o['route'][o['waypoint']]
    if not flight_segment(pond,plan,a['root'],target,s['center'],cr):interrupt(pond,plan,'The next flight segment is blocked.');return
    lease['target']=list(target)
    if stop or s['phase'] in ('waiting','exit','done'):castle.physical_pause(pond,plan,preserve_state=stop and pond.game.duck.current_action in ('feed','play','clean','pet','sleep'))
    else:
        target=ph['route'][ph['waypoint']]
        if not cheese_segment(pond,plan,cr,target,s['center'],a['root']):interrupt(pond,plan,'The control route is blocked by the flight corridor.');return
        if w['id'] in castle.AIR_SCORES:
            from engine import castle_air
            ph['contact_ready']=ph['observation_ready']=False
            if o['ready'] and shared.near(a['root'],s['hover']) and a['facing']==(cr[0]>=a['root'][0]):
                castle_air.station_ready(pond,plan,s['operator'],ph,w['id'],[box(a['root'],METRIC)])
        else:
            ph['contact_ready']=bool(ph['phase']=='hold' and o['ready'] and shared.near(a['root'],s['hover']) and a['facing']==(cr[0]>=a['root'][0]) and shared.near(cr,ph['stance'],.51) and all(castle.reach_distance(cr,ph['target'],g,castle.rig_metric(w)['scale'])<=3 for g in castle.station_grips(w,ph['station'])))


def motion(minds,key):
    lease=minds.carnival_guests.get(key)
    if not isinstance(lease,dict) or not lease.get('flight') or not validate(minds.pond,minds.pond.state.get('plan')):return None
    w=lease['work'];s=w['shared'];a=live(minds.pond,s);cr=shared.cheese_root(minds.pond)
    return dict(target=list(lease['target']),phase=lease['phase'],facing=cr[0]>=a['root'][0] if a else True,gesture='idle',owner=lease['attempt'])


def advance(pond,plan,dt):
    if outfitted(pond):return interrupt(pond,plan,'Flutter needs more clearance around that outfit.')
    if not validate(pond,plan):return interrupt(pond,plan,'The flight reservation is invalid.')
    refresh(pond);w=plan['carnival_work']
    if w.get('interrupted'):return False
    if shared.paused(pond,plan):return True
    s=w['shared'];o=s['observer_physical'];a=live(pond,s)
    if s['phase']=='waiting':
        if not shared.arrived(o,a['root']):return True
        o.update(phase='hold',ready=True);s['phase']='operate'
    if s['phase']=='operate':
        if not flight_clear(pond,plan,a['root'],s['center'],cheese_root(pond)) or not shared.near(a['root'],s['hover']):return interrupt(pond,plan,'Flutter lost the reserved hover point.')
        if a['facing']!=(cheese_root(pond)[0]>=a['root'][0]):castle.physical_pause(pond,plan);return True
        if not w['events'] and not proposal_clear(pond,plan,s):return interrupt(pond,plan,'A future flight or control leg is blocked.')
        castle.physical_advance(pond,plan,dt)
        if w.get('interrupted'):return interrupt(pond,plan,w.get('physical_error','Native controls interrupted.'))
        if w['done']:
            s['phase']='exit';o.update(phase='exit',ready=False,route=s['flight_exit_route'],waypoint=0)
        return True
    if s['phase']=='exit' and shared.arrived(o,a['root']):o['exited']=True;s['phase']='done';refresh(pond);return False
    return s['phase']!='done'


def completion_ready(pond,plan):
    from engine import castle_air
    if not castle_air.receipt_ready(pond,plan):return False
    if not validate(pond,plan):return False
    w=plan['carnival_work'];s=w['shared'];a=live(pond,s)
    return bool(weather_ok(pond) and castle.allowed(pond,w['id']) and castle.supported(pond,plan,cheese_root(pond),s['center']) and not w.get('recorded') and s['phase']=='done' and shared.near(cheese_root(pond),w['physical']['exit'],.51) and shared.near(a['root'],s['flight_exit']) and flight_clear(pond,plan,a['root'],s['center'],cheese_root(pond)))


def complete(pond,plan):
    if plan.get('carnival_work',{}).get('id')=='castle_gauge_check':
        from engine import castle_air
        return castle_air.complete_observation(pond,plan)
    if not completion_ready(pond,plan):return False
    w=plan['carnival_work'];s=w['shared'];m=pond.minds;key=s['observer']['actor'];lease=m.carnival_guests[key];w['recorded']=True
    obj=pond.object_state('bounce_house',plan);history=obj.setdefault('carnival_routines',{});history[w['id']]=min(9999,history.get(w['id'],0)+1);company=obj.setdefault('carnival_company',{});company[key]=min(9999,company.get(key,0)+1)
    note='Cheese operated '+w['label']+' while Flutter watched from her own clear flight space.'
    m.model.learn('cheese','practice',lease['contexts']['cheese'],.25,m.now,note,key);m.model.learn(key,'observe',lease['contexts'][key],.25,m.now,note,'cheese')
    for actor,other in (('cheese',key),(key,'cheese')):m.model.learn(actor,'share',lease['contexts'][actor],.25,m.now,note,other);m.model.bond(actor,other,.18,m.now,note)
    m.carnival_guests.pop(key,None);pond.game.guest_motion.release_meeting(s['attempt']);pond.remember('neighbors',note,.6,key);pond._cache=None;return True


def view(pond,plan):
    w=copy.deepcopy(plan.get('carnival_work',{}))
    if not validate(pond,plan):w.update(flight_observer=True,shared_physical=True,shared={},physical={});return w
    cr=cheese_root(pond);s=w['shared'];a=live(pond,s);o=s['observer_physical']
    if w['physical']['root']!=cr or o['root']!=a['root'] or not shared.near(a['root'],s['hover']) or a['facing']!=(cr[0]>=a['root'][0]):w['physical']['contact_ready']=False
    w['physical']['root']=cr;o['root']=list(a['root']);return w
