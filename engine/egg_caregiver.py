"""One arrived caregiver operates real controls beside an unchanged stationary egg."""
import copy,json,math,uuid
from pathlib import Path
from engine import castle_shared as shared,castle_work as castle,castle_actors as actors,terrain
from engine.portable_ground import policy
from engine.pond_layout import bounds,FOOTPRINTS
from world.guest_cast import guest_profile

EGG=json.loads((Path(__file__).parent/'client/animation/egg-caregiver-metrics.json').read_text())
IMMUTABLE=('destination','mode','score','source_age','operator','recipient','instance','center','sites','operator_routes','operator_exit_route','operator_exit','origin')


def available(pond):return bool(pond.game.duck and pond.game.duck.growth_stage=='egg' and pond.scene_available())


def recipient(pond):
    g=pond.game;p=g.renderer.duck_pos
    if not g.duck or g.duck.growth_stage!='egg' or type(p.facing_right) is not bool or not shared.point([p.x,p.y]):return None
    return dict(actor='cheese',stage='egg',token=str(g.duck.created_at),root=[p.x,p.y],facing=p.facing_right,phase='stationary')


def actual(pond,identity):
    try:
        a=actors.live(pond,identity)
        if not a or type(a.get('facing')) is not bool:return None
        if a['adapter']=='regular':
            from world.friends import visitor_animator
            raw=[visitor_animator._position_x,visitor_animator._position_y]
        else:
            mover=pond.game.guest_motion if a['adapter']=='rare' else pond.game.story_motion
            raw=[mover.actor['x'],mover.actor['y']]
        return a if shared.point(raw) and shared.point(a['root']) else None
    except (TypeError,ValueError,KeyError,AttributeError):return None


def weather_ok(pond,score):
    ecology=pond.state.get('ecology');wind=ecology.get('wind') if isinstance(ecology,dict) else None
    return bool(type(wind) in (int,float) and math.isfinite(wind) and wind>=0 and isinstance(pond.weather_type,str) and castle.allowed(pond,score))


def metric(r):return dict(EGG['facings']['right' if r['facing'] else 'left'],scale=EGG['scale'])


def box(root,m,key='body'):
    bx,by=castle.pitches(m);b=m[key]
    return [root[0]+b['x']*bx,root[1]+b['y']*by,b['w']*bx,b['h']*by]


def overlap(a,b,pad=.25):return a[0]<b[0]+b[2]+pad and a[0]+a[2]+pad>b[0] and a[1]<b[1]+b[3]+pad and a[1]+a[3]+pad>b[1]


def extra_actor(pond):return sum(bool(v) for v in (pond.game.friends.current_visit,pond.game.atmosphere.current_visitor,pond.state.get('story')))>1


def shell_safe(pond,plan,r,center):
    if not r or not shared.point(center):return False
    m=metric(r);shell=box(r['root'],m);base=box(r['root'],m,'shell_base')
    if shell[0]<2 or shell[0]+shell[2]>124 or shell[1]<2 or shell[1]+shell[3]>37:return False
    shape=dict(width=shell[2]*192/132,height=shell[3]*47/42,floor=False)
    if not policy(pond).check('rock',(shell[0]+shell[2]/2)*20/132,(base[1]+base[3])*12/42,plan['instance'],shape)[0]:return False
    for x,y in shared.samples([base[0],base[1]],[base[0]+base[2],base[1]] )+shared.samples([base[0],base[1]+base[3]],[base[0]+base[2],base[1]+base[3]]):
        if terrain.water_at(pond.location,x,y,pond.biome):return False
    left=castle.art_world(center,0,0);right=castle.art_world(center,castle.GEOMETRY['width'],castle.GEOMETRY['ground_row'])
    if overlap(shell,[left[0],left[1],right[0]-left[0],right[1]-left[1]]):return False
    grill=castle.control_world(center,'grill')
    if overlap(shell,[grill[0]-6,grill[1]-6,12,12]):return False
    # Full placed-object silhouettes, rather than only their ground footprint.
    for item,x,y,shape in policy(pond).occupied(instance=plan['instance']):
        if shape is None and item not in FOOTPRINTS:return False
        try:b=bounds(item,x,y,shape)
        except (ValueError,TypeError,KeyError):return False
        if not shared.point([b['x'],b['y']]) or not shared.point([b['w'],b['h']]):return False
        if not b['floor'] and overlap(shell,[b['x']*132/20,b['y']*42/12,b['w']*132/20,b['h']*42/12]):return False
    return True


def separated(root,cast,r,score=None):
    m=EGG.get('caregivers',{}).get(cast)
    if score in castle.AIR_SCORES:m=shared.operator_travel(cast,score)
    return bool(m and not overlap(box(root,m),box(r['root'],metric(r))))


def segment(pond,plan,a,b,s):
    m=shared.operator_travel(s['operator']['cast'],s['score'])
    return all(shared.support(pond,plan,p,m,s['center']) and separated(p,s['operator']['cast'],s['recipient'],s['score']) for p in shared.samples(a,b))


def route(pond,plan,a,b,s):
    for corner in ([a[0],b[1]],[b[0],a[1]]):
        path=[corner,list(b)]
        if all(segment(pond,plan,x,y,s) for x,y in zip([a]+path,path)):return path
    return None


def proposal_clear(pond,plan,s):
    if not shell_safe(pond,plan,s['recipient'],s['center']):return False
    previous=s['origin']
    for path in s['operator_routes']+[s['operator_exit_route']]:
        for end in path:
            if not segment(pond,plan,previous,end,s):return False
            previous=end
    return True


def propose(pond,score,instance):
    r=recipient(pond)
    if not r or not available(pond) or pond.state.get('plan') or extra_actor(pond):return None,'The egg needs a free, quiet scene with one arrived caregiver.'
    if score not in castle.PHYSICAL_SCORES or not weather_ok(pond,score):return None,'That control work is not available in this weather.'
    plan=dict(target='bounce_house',instance=instance);center=castle.placement_center(pond,plan)
    if not shared.point(center) or 'bounce_house' not in pond.owned:return None,'That exact house is not placed here.'
    if not shell_safe(pond,plan,r,center) or math.hypot(r['root'][0]-center[0],r['root'][1]-center[1])>40:return None,'The egg must already rest safely beside this house; it cannot move into place.'
    reason='No arrived, willing caregiver has measured control anatomy.'
    try:candidates=actors.candidates(pond)
    except (TypeError,ValueError,KeyError,AttributeError):return None,'The actual caregiver position is invalid.'
    for candidate in candidates:
        a=actual(pond,actors.identity(candidate))
        if not a:continue
        if not shared.eligible(pond,a) or a['cast'] not in EGG.get('caregivers',{}):continue
        s=dict(destination=[round(v) for v in center],mode='egg-caregiver',score=score,source_age='egg',operator=actors.identity(a),recipient=r,instance=instance,center=center,origin=a['root'],operator_exit=a['root'])
        ground=math.ceil(castle.art_world(center,0,castle.GEOMETRY['ground_row'])[1]);rows=shared.operator_metrics(a['cast'],score);m=shared.operator_travel(a['cast'],score);sites=[]
        if score in castle.AIR_SCORES:
            from engine import castle_air
            sites,reason=castle_air.plan_sites(pond,plan,score,s['operator'],[box(r['root'],metric(r))])
            if sites is None:continue
        else:
            for _,name in castle.physical_stations(dict(id=score)):
                target=castle.control_world(center,name);contacts=[v for v in rows if v['station']==name];preferred=target[0]-(max(v['grip'][0] for v in contacts)+1)*castle.pitches(m)[0]
                points=sorted(([x,y] for x in range(math.floor(preferred)-4,math.ceil(preferred)+5) for y in range(ground,ground+4)),key=lambda p:(p[0]-preferred)**2+(p[1]-ground)**2)
                stance=next((p for p in points if shared.support(pond,plan,p,m,center) and separated(p,a['cast'],r) and all(castle.reach_distance(p,target,v['grip'],v['scale'])<=3 for v in contacts)),None)
                if stance is None:break
                sites.append(dict(station=name,target=target,stance=stance))
        if len(sites)!=len(castle.physical_stations(dict(id=score))):reason='A later control has no safe caregiver stance beside the egg.';continue
        s['sites']=sites;paths=[];previous=a['root']
        for site in sites:
            path=route(pond,plan,previous,site['stance'],s)
            if path is None:break
            paths.append(path);previous=site['stance']
        if len(paths)!=len(sites):reason='The caregiver cannot reach every control without crossing the egg.';continue
        exit_route=route(pond,plan,previous,a['root'],s)
        if exit_route is None:reason='The caregiver has no clear independent exit.';continue
        s.update(operator_routes=paths,operator_exit_route=exit_route)
        distance=sum(math.hypot(b[0]-a[0],2*(b[1]-a[1])) for a,b in zip([s['origin']]+[p for path in paths+[exit_route] for p in path],[p for path in paths+[exit_route] for p in path]))
        pace=3.5 if s['operator']['adapter']=='story' else guest_profile(s['operator']['cast'])['pace']*.72*.8
        s['required_seconds']=distance/pace+castle.ROUTINES[score]['duration']+12
        if a['adapter']=='rare' and a['remaining_seconds']<s['required_seconds']:reason='The caregiver cannot finish before departure.';continue
        return s,''
    return None,reason


def prepare(pond,plan,proposal=None):
    if not isinstance(proposal,dict):return False,'Caregiving needs a complete preflight.'
    s=copy.deepcopy(proposal);a=actual(pond,s['operator']);w=plan['carnival_work']
    if (pond.state.get('plan') or not available(pond) or not weather_ok(pond,w['id']) or extra_actor(pond) or recipient(pond)!=s['recipient'] or not a or not shared.eligible(pond,a) or a['root']!=s['origin'] or w['id']!=s['score'] or plan['instance']!=s['instance'] or plan.get('destination')!=s['destination'] or s['destination']!=[round(v) for v in s['center']] or castle.placement_center(pond,plan)!=s['center'] or not proposal_clear(pond,plan,s)
        or a['adapter']=='rare' and a['remaining_seconds']<s['required_seconds']):return False,'The caregiver preflight changed before acquisition.'
    s.update(version=1,attempt=uuid.uuid4().hex,phase='approach');site=s['sites'][0]
    ph=dict(version=1,actor=a['actor'],root=list(a['root']),center=s['center'],station_index=0,station=site['station'],target=site['target'],stance=site['stance'],phase='approach',route=s['operator_routes'][0],waypoint=0,exit=s['operator_exit'],contact_ready=False)
    if 'observation_target' in site:ph['observation_target']=site['observation_target']
    w.update(egg_caregiver=True,shared_physical=True,physical_pilot=False,source_age='egg',shared=s,physical=ph,paired=True,invitation_checked=True,companion=dict(actor=a['actor'],mode='caregiver',ready=False))
    m=pond.minds;key=a['actor'];m.carnival_guests[key]=dict(actor=key,work=w,attempt=s['attempt'],shared=True,egg_caregiver=True,contract={k:copy.deepcopy(s[k]) for k in IMMUTABLE},target=list(a['root']),phase='approach',token=a['token'],context=m.context(key))
    m.tasks.pop(key,None);pond.game.renderer.duck_pos.frozen=True;pond._cache=None
    return True,''


def start(pond,score,instance=None):
    s,reason=propose(pond,score,instance)
    if not s:return False,reason
    if pond.state['elapsed']<pond.state['cooldowns'].get('item:'+str(instance),-1):return False,'Give this house a little time before another caregiver visit.'
    plan=dict(kind='item',target='bounce_house',instance=instance,location=pond.location,destination=list(s['destination']),phase='act',elapsed=0.,duration=castle.ROUTINES[score]['duration'],automatic=False,paused=False)
    plan['carnival_work']=castle.make(pond,plan,score);plan['label']='Caregiver: '+plan['carnival_work']['label']
    ok,reason=prepare(pond,plan,s)
    if not ok:return False,reason
    pond.state['plan']=plan;pond._cache=None
    return True,plan['label']+'.'


def validate(pond,plan):
    try:
        w=plan['carnival_work'];s=w['shared'];ph=w['physical'];a=actual(pond,s['operator']);lease=pond.minds.carnival_guests.get(s['operator']['actor'])
        if plan.get('kind')!='item' or plan.get('target')!='bounce_house' or plan.get('location')!=pond.location:return False
        if w.get('egg_caregiver') is not True or w.get('shared_physical') is not True or w.get('physical_pilot') is not False or s['version']!=1 or s['mode']!='egg-caregiver' or w['source_age']!='egg' or w.get('interrupted'):return False
        if recipient(pond)!=s['recipient'] or extra_actor(pond) or not a or not isinstance(lease,dict) or lease.get('work') is not w or lease.get('attempt')!=s['attempt']:return False
        if any(s.get(k)!=lease['contract'].get(k) for k in IMMUTABLE) or w['id']!=s['score'] or plan['instance']!=s['instance'] or plan.get('destination')!=s['destination'] or s['destination']!=[round(v) for v in s['center']] or castle.placement_center(pond,plan)!=s['center']:return False
        duration=castle.ROUTINES[w['id']]['duration'];elapsed=w['ride_elapsed']
        if type(elapsed) not in (int,float) or not math.isfinite(elapsed) or not 0<=elapsed<=duration or type(w['clock']) not in (int,float) or not math.isfinite(w['clock']):return False
        if not isinstance(w['events'],list) or any(type(i) is not int for i in w['events']) or w['events']!=[i for i,e in enumerate(castle.ROUTINES[w['id']]['effects']) if e[0]*duration<=elapsed]:return False
        cursor=max(i for i,(at,_) in enumerate(castle.physical_stations(w)) if at*duration<=elapsed);site=s['sites'][cursor]
        if w['id']=='castle_gauge_check':
            from engine import castle_air
            if ph.get('observation_target')!=castle_air.observation_target(s['center']):return False
        if ph.get('version')!=1 or type(ph.get('contact_ready')) is not bool or ph['actor']!=a['actor'] or ph['station_index']!=cursor or any(ph[k]!=site[k] for k in ('station','target','stance')) or ph['center']!=s['center'] or ph['exit']!=s['operator_exit']:return False
        if ph['phase'] not in ('approach','hold','exit') or not shared.point(ph['root']) or type(ph['waypoint']) is not int:return False
        expected=s['operator_exit_route'] if ph['phase']=='exit' else s['operator_routes'][cursor]
        if ph['route']!=expected or not all(shared.point(p) for p in ph['route']) or not 0<=ph['waypoint']<len(expected):return False
        if s['phase']=='done':return w['done'] is True and ph.get('exited') is True and ph['phase']=='exit' and w['stage']=='done' and elapsed==duration and w['clock']==0
        if s['phase']=='exit':return not w['done'] and ph['phase']=='exit' and w['stage']=='service_exit' and elapsed==duration and w['clock']==0
        return s['phase'] in ('approach','operate') and not w['done'] and ph['phase'] in ('approach','hold') and w['stage'] in ('queue','service') and w['clock']==elapsed
    except (TypeError,ValueError,KeyError,IndexError,AttributeError):return False


def interrupt(pond,plan,reason):
    w=plan.get('carnival_work') if isinstance(plan,dict) else None
    if not isinstance(w,dict):return False
    w.update(done=True,interrupted=True,physical_error=reason)
    if isinstance(w.get('shared'),dict):w['shared']['phase']='interrupted'
    if isinstance(w.get('physical'),dict):w['physical']['contact_ready']=False
    for key,lease in list(pond.minds.carnival_guests.items()):
        if not isinstance(lease,dict):pond.minds.carnival_guests.pop(key,None);continue
        if lease.get('work') is w:
            pond.minds.carnival_guests.pop(key,None)
            try:actors.release_owned(pond,key,lease)
            except (TypeError,ValueError,KeyError,AttributeError):pass
    w.pop('companion',None)
    try:
        if pond.state.get('plan') is None or pond.state.get('plan') is plan:
            castle.clear(pond,plan);pond.object_state('bounce_house',plan)['active']=False
    except (TypeError,ValueError,KeyError,AttributeError):pass
    pond._cache=None;return False


def paused(pond,plan):return bool(plan.get('paused') or not available(pond) or pond.game.duck.current_action in ('feed','play','clean','pet','sleep'))


def refresh(pond):
    plan=pond.state.get('plan')
    if not plan:return
    if not validate(pond,plan):interrupt(pond,plan,'The egg or caregiver reservation changed.');return
    w=plan['carnival_work'];s=w['shared'];ph=w['physical'];a=actual(pond,s['operator'])
    if not weather_ok(pond,w['id']) or not shell_safe(pond,plan,s['recipient'],s['center']) or not segment(pond,plan,ph['root'],a['root'],s):interrupt(pond,plan,'The shell or caregiver corridor is no longer safe.');return
    ph['root']=list(a['root']);stop=paused(pond,plan) or s['phase']=='done';target=a['root'] if stop or ph['phase']=='hold' else ph['route'][ph['waypoint']]
    if not segment(pond,plan,a['root'],target,s):interrupt(pond,plan,'The remaining caregiver route is blocked.');return
    lease=pond.minds.carnival_guests[a['actor']];lease['target']=list(target)
    if w['id'] in castle.AIR_SCORES:
        from engine import castle_air
        ph['contact_ready']=ph['observation_ready']=False
        if not stop:castle_air.station_ready(pond,plan,s['operator'],ph,w['id'],[box(s['recipient']['root'],metric(s['recipient']))])
    else:
        contacts=[m for m in shared.operator_metrics(a['cast'],w['id']) if m['station']==ph['station']]
        ph['contact_ready']=bool(not stop and ph['phase']=='hold' and a['facing'] and shared.near(a['root'],ph['stance']) and all(castle.reach_distance(a['root'],ph['target'],m['grip'],m['scale'])<=3 for m in contacts))


def motion(minds,key):
    lease=minds.carnival_guests.get(key)
    if not isinstance(lease,dict) or not lease.get('egg_caregiver') or not validate(minds.pond,minds.pond.state.get('plan')):return None
    return dict(target=list(lease['target']),phase=lease['phase'],facing=True,gesture='idle',owner=lease['attempt'])


def advance(pond,plan,dt):
    if not validate(pond,plan):return interrupt(pond,plan,'The egg caregiver reservation is invalid.')
    refresh(pond);w=plan['carnival_work']
    if w.get('interrupted'):return False
    if paused(pond,plan):return True
    s=w['shared'];ph=w['physical'];a=actual(pond,s['operator'])
    if s['phase']=='done':return False
    if ph['phase'] in ('approach','exit'):
        if not shared.arrived(ph,a['root']):return True
        if ph['phase']=='exit':
            ph['exited']=True;s['phase']='done';w.update(stage='done',done=True);castle.clear(pond,plan);refresh(pond);return False
        ph['phase']='hold';s['phase']='operate'
    refresh(pond)
    if w.get('interrupted') or (w['id'] not in castle.AIR_SCORES and not ph['contact_ready']):return not w.get('interrupted')
    status,reason=shared.advance_control_clock(pond,plan,dt,lambda:actual(pond,s['operator']),lambda:proposal_clear(pond,plan,s))
    if status=='blocked':return interrupt(pond,plan,reason)
    from engine import carnival
    if status=='transfer':
        i=ph['station_index']+1;site=s['sites'][i]
        if 'observation_target' in site:ph['observation_target']=site['observation_target']
        ph.update(station_index=i,station=site['station'],target=site['target'],stance=site['stance'],phase='approach',route=s['operator_routes'][i],waypoint=0,contact_ready=False)
    elif status=='exit':s['phase']='exit';ph.update(phase='exit',route=s['operator_exit_route'],waypoint=0,contact_ready=False);carnival.stage(w,'service_exit',0)
    return True


def completion_ready(pond,plan):
    from engine import castle_air
    if not castle_air.receipt_ready(pond,plan):return False
    if not validate(pond,plan):return False
    w=plan['carnival_work'];s=w['shared'];a=actual(pond,s['operator'])
    return bool(not w.get('recorded') and s['phase']=='done' and weather_ok(pond,w['id']) and shell_safe(pond,plan,s['recipient'],s['center']) and shared.near(a['root'],s['operator_exit']) and segment(pond,plan,a['root'],a['root'],s))


def complete(pond,plan):
    if plan.get('carnival_work',{}).get('id')=='castle_gauge_check':
        from engine import castle_air
        return castle_air.complete_observation(pond,plan)
    if not completion_ready(pond,plan):
        w=plan.get('carnival_work') if isinstance(plan,dict) else None
        if isinstance(w,dict) and not w.get('recorded'):
            interrupt(pond,plan,'The caregiver callback arrived before a valid completed exit.')
        return False
    w=plan['carnival_work'];s=w['shared'];key=s['operator']['actor'];m=pond.minds;lease=m.carnival_guests[key];w['recorded']=True
    obj=pond.object_state('bounce_house',plan);obj['active']=False;castle.clear(pond,plan)
    for field,index in (('carnival_routines',w['id']),('carnival_company',key),('egg_caregiving',key)):
        ledger=obj.setdefault(field,{});ledger[index]=min(9999,ledger.get(index,0)+1)
    note=m.model.residents[key]['name']+' completed '+w['label']+' beside the resting egg.'
    m.model.learn(key,'practice',lease['context'],.25,m.now,note,'cheese');m.model.learn(key,'share',lease['context'],.25,m.now,note,'cheese')
    m.carnival_guests.pop(key,None);actors.release_owned(pond,key,lease);pond._cache=None
    return True


def tick(pond,dt):
    plan=pond.state.get('plan')
    if not plan:return
    advance(pond,plan,dt);w=plan['carnival_work']
    if w.get('interrupted'):pond.state['plan']=None;pond._cache=None;return
    done=completion_ready(pond,plan)
    plan['elapsed']=plan['duration']*(1 if done else .9*min(1,w.get('ride_elapsed',0)/castle.ROUTINES[w['id']]['duration']))
    obj=pond.object_state('bounce_house',plan);obj['active']=bool(not w.get('interrupted') and w['shared']['phase']=='operate' and not paused(pond,plan))
    if w.get('interrupted'):pond.state['plan']=None;pond._cache=None;return
    if done:
        obj['active']=False;pond.state['plan']=None;pond._complete(plan);pond.state['cooldowns']['item:'+str(plan['instance'])]=pond.state['elapsed']+30;pond._cache=None


def view(pond,plan):
    w=copy.deepcopy(plan.get('carnival_work',{}))
    if not validate(pond,plan):w.update(egg_caregiver=True,shared_physical=True,shared={},physical={});return w
    a=actual(pond,w['shared']['operator'])
    if w['physical']['root']!=a['root']:w['physical']['contact_ready']=False
    w['physical']['root']=list(a['root']);return w


def conversation(pond,plan,key):
    if not validate(pond,plan) or key!=plan['carnival_work']['shared']['operator']['actor']:return None
    w=plan['carnival_work']
    return dict(object='bounce house',activity=w['label'],stage=w['stage'],paused=paused(pond,plan),company='the resting egg',company_status='stationary recipient')
