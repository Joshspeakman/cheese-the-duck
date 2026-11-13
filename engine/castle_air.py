"""Measured air-control geometry and a reusable, reward-free atomic executor.

The caller owns leases, real movers, occurrence selection and final exits. This
module never replaces the outer plan or simulates a pending physical response.
"""
import copy,json,math
from pathlib import Path
from engine import castle_work as castle,castle_actors as actors,castle_shared as shared,terrain,excursions
from engine.portable_ground import policy
from engine.pond_layout import bounds,FOOTPRINTS

DATA=json.loads((Path(__file__).parent/'client/animation/castle-air-metrics.json').read_text())
SCENERY=json.loads((Path(__file__).parent/'client/animation/castle-scenery-metrics.json').read_text())
ATOMIC_IDS=frozenset(('castle_start','castle_stop','castle_vent_open','castle_vent_close','castle_hose_straight','castle_hose_stow','castle_grill_clean','castle_gauge_check'))
READ_DISTANCE=12.


def operator_state(pond,operator):
    try:
        if operator.get('adapter')=='cheese':
            g=pond.game;p=g.renderer.duck_pos;age=castle.canonical_age(g.duck.growth_stage)
            if operator.get('actor')!='cheese' or age!=operator.get('source_age') or not age or not shared.point([p.x,p.y]) or type(p.facing_right) is not bool:return None
            if 'token' in operator and operator['token']!=str(g.duck.created_at):return None
            return dict(operator,root=[p.x,p.y],facing=p.facing_right)
        live=actors.live(pond,operator)
        if not live or not shared.point(live['root']) or type(live.get('facing')) is not bool:return None
        if live['adapter']=='regular':
            from world.friends import visitor_animator
            raw=[visitor_animator._position_x,visitor_animator._position_y]
        else:
            mover=pond.game.guest_motion if live['adapter']=='rare' else pond.game.story_motion
            raw=[mover.actor['x'],mover.actor['y']]
        return live if shared.point(raw) else None
    except (KeyError,TypeError,ValueError,AttributeError):return None


def entry(operator):
    return DATA['ages'][operator['source_age']] if operator['adapter']=='cheese' else DATA['casts'][operator['cast']]


def metrics(operator,atomic_id):return entry(operator)['routines'][atomic_id]
def travel_metric(operator):return entry(operator)['travel']
def event_metric(operator,atomic_id,index):return metrics(operator,atomic_id)[index]


def box(root,metric):
    bx,by=castle.pitches(metric);b=metric['body']
    return [root[0]+b['x']*bx,root[1]+b['y']*by,b['w']*bx,b['h']*by]


def overlap(a,b,pad=.25):return a[0]<b[0]+b[2]+pad and a[0]+a[2]+pad>b[0] and a[1]<b[1]+b[3]+pad and a[1]+a[3]+pad>b[1]


def obstacles_of(context):
    value=context.get('obstacles',())
    return value() if callable(value) else value


def supported(pond,plan,atomic_id,operator,root,obstacles=()):
    if atomic_id not in ATOMIC_IDS or not shared.point(root):return False
    center=castle.placement_center(pond,plan)
    if not shared.point(center):return False
    m=travel_metric(operator)
    if not shared.support(pond,plan,root,m,center):return False
    body=box(root,m)
    return all(isinstance(b,(list,tuple)) and len(b)==4 and all(type(v) in (int,float) and math.isfinite(v) for v in b) and not overlap(body,b) for b in obstacles)


def segment_clear(pond,plan,atomic_id,operator,start,end,obstacles=()):
    if not shared.point(start) or not shared.point(end):return False
    return all(supported(pond,plan,atomic_id,operator,p,obstacles) for p in shared.samples(start,end))


def plan_route(pond,plan,atomic_id,operator,start,end,obstacles=()):
    for corner in ([start[0],end[1]],[end[0],start[1]]):
        path=[corner,list(end)]
        if all(segment_clear(pond,plan,atomic_id,operator,a,b,obstacles) for a,b in zip([start]+path,path)):return path
    return None


def observation_target(center):return castle.art_world(center,*DATA['observation']['dial']['needle_center'])


def ray_boxes(pond,plan,center,obstacles=()):
    result=list(obstacles)
    if pond.location!=SCENERY['location']:return None
    for b in DATA['observation']['occluders']:
        a=castle.art_world(center,b['x'],b['y']);z=castle.art_world(center,b['x']+b['w'],b['y']+b['h'])
        result.append([a[0],a[1],z[0]-a[0],z[1]-a[1]])
    for feature in SCENERY['features']:
        b=feature['bounds'];result.append([b['x'],b['y'],b['w'],b['h']])
    for item,x,y,shape in policy(pond).occupied(instance=plan.get('instance')):
        if shape is None and item not in FOOTPRINTS:return None
        try:b=bounds(item,x,y,shape)
        except (ValueError,TypeError,KeyError):return None
        if not shared.point([b['x'],b['y']]) or not shared.point([b['w'],b['h']]):return None
        result.append([b['x']*132/20,b['y']*42/12,b['w']*132/20,b['h']*42/12])
    return result


def ray_clear(a,b,boxes):
    if boxes is None:return False
    # Analytic closed segment/AABB intersection catches arbitrarily thin or
    # grazing obstructions; no sample spacing can certify an eye ray.
    for q in boxes:
        enter,leave=0.,1.
        for axis in (0,1):
            lo=q[axis]-.05;hi=q[axis]+q[axis+2]+.05;delta=b[axis]-a[axis]
            if delta==0:
                if not lo<=a[axis]<=hi:enter,leave=1.,0.;break
            else:
                x,y=(lo-a[axis])/delta,(hi-a[axis])/delta
                enter=max(enter,min(x,y));leave=min(leave,max(x,y))
        if enter<=leave:return False
    return True


def sightline(pond,plan,root,facing,metric,center,obstacles=()):
    if facing is not True:return False
    target=observation_target(center);bx,by=castle.pitches(metric);boxes=ray_boxes(pond,plan,center,obstacles)
    for mode in ('normal','reduced'):
        eyes=[[root[0]+x*bx,root[1]+y*by] for x,y in metric['eyes'][mode]]
        if not any(target[0]>p[0] and .25<=math.hypot(target[0]-p[0],target[1]-p[1])<=READ_DISTANCE and ray_clear(p,target,boxes) for p in eyes):return False
    return True


def plan_sites(pond,plan,atomic_id,operator,obstacles=()):
    live=operator_state(pond,operator);center=castle.placement_center(pond,plan)
    if atomic_id not in ATOMIC_IDS or not live or not shared.point(center):return None,'This atomic control lacks a valid measured operator.'
    ground=math.ceil(castle.art_world(center,0,castle.GEOMETRY['ground_row'])[1]);rows=metrics(operator,atomic_id);sites=[]
    for index,(_,name) in enumerate(castle.physical_stations(dict(id=atomic_id))):
        local=[m for m in rows if m['station_index']==index];target=castle.control_world(center,name)
        if not local:return None,'This station occurrence has no authored effect geometry.'
        if local[0]['kind']=='observation':
            read=observation_target(center);m=local[0];bx,by=castle.pitches(m);eyes=[p for mode in m['eyes'].values() for p in mode]
            preferred=[read[0]-max(e[0] for e in eyes)*bx-4,read[1]-sum(e[1] for e in eyes)/len(eyes)*by]
            ys=range(max(ground,math.floor(preferred[1])-5),min(37,math.ceil(preferred[1])+6))
        else:
            bx=castle.pitches(local[0])[0];preferred=[target[0]-(max(m['grip'][0] for m in local)+1)*bx,ground];ys=range(ground,ground+4)
        points=sorted(([x,y] for x in range(math.floor(preferred[0])-(12 if local[0]['kind']=='observation' else 5),math.ceil(preferred[0])+6) for y in ys),key=lambda r:(r[0]-preferred[0])**2+(r[1]-preferred[1])**2)
        if operator['adapter']=='cheese':points=[[live['root'][i]+round(p[i]-live['root'][i]) for i in (0,1)] for p in points]
        def fits(root):
            if not supported(pond,plan,atomic_id,operator,root,obstacles):return False
            return all(sightline(pond,plan,root,True,m,center,obstacles) if m['kind']=='observation' else castle.reach_distance(root,target,m['grip'],m['scale'])<=3 for m in local)
        stance=next((p for p in points if fits(p)),None)
        if stance is None:return None,'The '+name+' occurrence has no supported, reachable viewing or contact stance.'
        site=dict(station_index=index,station=name,stance=stance,target=target)
        if local[0]['kind']=='observation':site['observation_target']=observation_target(center)
        sites.append(site)
    return sites,''


def make_execution(atomic_id,occurrence_id,power_authority='manual'):
    if atomic_id not in ATOMIC_IDS or power_authority not in ('manual','procedure'):raise ValueError('Unknown atomic control or power authority')
    return dict(id=atomic_id,occurrence_id=occurrence_id,label=castle.ROUTINES[atomic_id]['label'],clock=0.,ride_elapsed=0.,elapsed=0.,events=[],fractions={},stage='queue',done=False,power_authority=power_authority,automatic=False)


def result(status,reason='',**extra):return dict(status=status,reason=reason,**extra)


def _response_ready(obj,execution,index):
    state=castle.state(obj);_,field,value=castle.ROUTINES[execution['id']]['effects'][index]
    if field=='dust_fraction':
        if state['motor']!='off':return result('blocked','Stop the motor before sweeping the actual grille.')
        if state['powered'] or state['rotor_speed']>0:return result('wait','Wait for the real rotor to stop before the wing sweep.')
    if field=='hose' and execution['id']=='castle_hose_stow' and (0 not in execution['events'] or state['motor']!='off'):return result('blocked','Stop the blower before coiling its hose.')
    if field=='motor' and value=='on' and excursions.finite(obj.get('condition'),1.)<=.2:return result('blocked','Repair the house before starting its air supply.')
    if field=='motor' and value=='on' and execution.get('power_authority')=='procedure' and state['power_hold']:return result('blocked','The user has explicitly left this blower switched off.')
    return result('ready')


def effect_ready(pond,plan,execution,context,index):
    try:
        operator=context['operator'];p=context['physical'];live=operator_state(pond,operator);m=event_metric(operator,execution['id'],index);center=castle.placement_center(pond,plan);obstacles=obstacles_of(context)
        if not live or p['station_index']!=m['station_index'] or p['station']!=m['station'] or p['target']!=castle.control_world(center,m['station']):return result('blocked','The actual operator or station occurrence changed.')
        tolerance=.51 if operator['adapter']=='cheese' else 1e-7
        if p['phase']!='hold' or not shared.near(live['root'],p['stance'],tolerance) or not supported(pond,plan,execution['id'],operator,live['root'],obstacles):return result('blocked','The operator lost its actual supported stance.')
        if m['kind']=='observation':
            if p.get('observation_target')!=observation_target(center) or not sightline(pond,plan,live['root'],live['facing'],m,center,obstacles):return result('blocked','The actual open eyes cannot see the real pressure needle.')
        elif live['facing'] is not True or castle.reach_distance(live['root'],p['target'],m['grip'],m['scale'])>3:return result('blocked','The actual authored grip cannot reach the control.')
        response=_response_ready(pond.object_state('bounce_house',plan),execution,index)
        return dict(response,kind=m['kind'])
    except (TypeError,ValueError,KeyError,IndexError,AttributeError):return result('blocked','The atomic geometry record is malformed.')


def terminal_ready(pond,plan,execution,context):
    try:
        obj=pond.object_state('bounce_house',plan);s=castle.state(obj);id=execution['id'];spec=castle.ROUTINES[id]
        if id=='castle_start' and excursions.finite(obj.get('condition'),1.)<=.2:return result('blocked','The damaged house cannot start its air supply.')
        if execution['events']!=list(range(len(spec['effects']))) or execution['clock']<spec['duration']:return result('wait','The authored atomic contacts are not complete.')
        if id in ('castle_stop','castle_hose_stow','castle_grill_clean') and (s['motor']!='off' or s['powered'] or s['rotor_speed']!=0):return result('wait','The rotor is still moving.')
        if id=='castle_start':
            policy=execution.get('restore_motor','on') if execution.get('power_authority')=='procedure' else 'on'
            if s['motor']!=policy:return result('blocked','The actual motor policy differs from its operated switch.')
            standby=policy=='auto' and (pond.hour<7 or pond.hour>=20)
            if standby:
                if s['powered'] or s['rotor_speed']!=0:return result('wait','The automatic supply must settle into night standby.')
            elif not s['powered'] or s['rotor_speed']<.98:return result('wait','The actual blower is still spinning up.')
        for key in ('vent','hose','kink'):
            values=[e[2] for e in spec['effects'] if e[1]==key]
            if values and abs(s[key]-values[-1])>.001:return result('wait','The actual '+key+' has not reached its commanded position.')
        return result('ready')
    except (TypeError,ValueError,KeyError,IndexError):return result('blocked','The atomic material record is invalid.')


def advance_atomic(pond,plan,execution,context,dt):
    """Advance the supplied child record, never the outer lease/route/receipt."""
    try:
        id=execution['id'];p=context['physical'];spec=castle.ROUTINES[id];duration=spec['duration'];operator=context['operator']
        if id not in ATOMIC_IDS or type(execution['clock']) not in (int,float) or not math.isfinite(execution['clock']) or not 0<=execution['clock']<=duration:return result('blocked','Invalid atomic clock.')
        if execution.get('power_authority','manual') not in ('manual','procedure'):return result('blocked','Invalid power authority.')
        if 'restore_motor' in execution and (id!='castle_start' or execution.get('power_authority')!='procedure' or execution['restore_motor'] not in ('auto','on')):return result('blocked','Invalid restored motor policy.')
        stage=execution.get('stage')
        if stage not in ('queue','service') or type(execution.get('done')) is not bool:return result('blocked','Invalid atomic stage.')
        if stage=='queue' and (execution['clock']!=0 or execution.get('events') or execution.get('done')):return result('blocked','A queued atomic cannot contain prior progress.')
        if execution.get('done'):
            if stage=='service' and execution['clock']==duration and execution.get('events')==list(range(len(spec['effects']))) and terminal_ready(pond,plan,execution,context)['status']=='ready':return result('finished',station_index=p['station_index'],new_events=[])
            return result('blocked','Invalid completed atomic record.')
        expected=[i for i,e in enumerate(spec['effects']) if e[0]*duration<=execution['clock']]
        if execution.get('ride_elapsed')!=execution['clock'] or execution['events']!=expected or any(type(i) is not int for i in execution['events']):return result('blocked','Invalid atomic effect prefix.')
        live=operator_state(pond,operator)
        if not live:return result('blocked','The atomic operator is no longer present.')
        tolerance=.51 if operator['adapter']=='cheese' else 1e-7
        if p.get('phase')!='hold':return result('hold','The actual operator is still travelling.')
        if not shared.near(live['root'],p.get('stance'),tolerance) or not supported(pond,plan,id,operator,live['root'],obstacles_of(context)):
            return result('blocked','The actual operator lost its held support.')
        cursor=p['station_index'];steps=castle.physical_stations(execution)
        if cursor!=max(i for i,(at,_) in enumerate(steps) if at*duration<=execution['clock']):return result('blocked','The atomic station cursor changed.')
        old_events=len(execution['events']);obj=pond.object_state('bounce_house',plan)
        revision=castle.state(obj)['power_revision']
        if 'expected_power_revision' not in execution and execution['clock']==0 and not execution['events']:execution['expected_power_revision']=revision
        if type(execution.get('expected_power_revision')) is not int or execution['expected_power_revision']!=revision:return result('blocked','External power intent changed during this atomic attempt.')
        if execution['stage']=='queue':execution['start']=copy.deepcopy(castle.state(obj));execution['stage']='service'
        boundary=steps[cursor+1][0]*duration if cursor+1<len(steps) else duration
        remaining=max(0,excursions.finite(dt));p['contact_ready']=False;p['observation_ready']=False
        while remaining>0 and execution['clock']<boundary:
            old=execution['clock'];upcoming=[(i,e[0]*duration) for i,e in enumerate(spec['effects']) if i not in execution['events']]
            stop=min([old+remaining,boundary]+[at for _,at in upcoming]);due=[i for i,at in upcoming if at==stop]
            for index in due:
                gate=_response_ready(obj,execution,index)
                if gate['status']=='wait':return result('hold',gate['reason'],station_index=cursor,new_events=execution['events'][old_events:])
                if gate['status']=='blocked':return result('blocked',gate['reason'],station_index=cursor,new_events=execution['events'][old_events:])
                if index==0 and not context['preflight']():return result('blocked','A required future route or role is no longer safe.')
            if stop<=old:break
            step=stop-old;execution['clock']=execution['ride_elapsed']=stop;execution['elapsed']+=step;remaining-=step
            for index in due:
                # Publish the exact authored pose clock before validating its
                # eye/grip geometry. World response was gated before this beat.
                gate=effect_ready(pond,plan,execution,context,index)
                if gate['status']!='ready':return result('blocked',gate['reason'],station_index=cursor,new_events=execution['events'][old_events:])
                kind=event_metric(operator,id,index)['kind'];p['contact_ready']=kind=='contact';p['observation_ready']=kind=='observation'
                castle.apply(obj,execution,index,spec['effects'][index])
            castle.state(obj)['active']=True
        extra=dict(station_index=cursor,new_events=execution['events'][old_events:])
        if execution['clock']>=boundary and cursor+1<len(steps):return result('transfer',**extra)
        if execution['clock']>=duration:
            gate=terminal_ready(pond,plan,execution,context)
            if gate['status']=='ready':execution['done']=True;return result('finished',observation=copy.deepcopy(execution.get('inspection')),**extra)
            return result('hold' if gate['status']=='wait' else 'blocked',gate['reason'],**extra)
        return result('hold',**extra)
    except (TypeError,ValueError,KeyError,IndexError,AttributeError):return result('blocked','The atomic execution or physical context is malformed.')


def station_ready(pond,plan,operator,physical,atomic_id,obstacles=()):
    """Truthful motion-only readiness; never consumes an effect or a reading."""
    physical['contact_ready']=physical['observation_ready']=False
    live=operator_state(pond,operator)
    if not live or physical.get('phase')!='hold':return False
    rows=[(i,m) for i,m in enumerate(metrics(operator,atomic_id)) if m['station_index']==physical['station_index']]
    if not rows:return False
    # Reuse geometry/real-response predicates with an already-consumed prefix;
    # the current work supplies the actual shutdown prerequisite for hose work.
    work=plan['carnival_work'];execution=work.get('atomic',work)
    context=dict(operator=operator,physical=physical,obstacles=obstacles)
    gates=[effect_ready(pond,plan,execution,context,i) for i,_ in rows]
    ready=all(g['status']=='ready' for g in gates)
    kind=rows[0][1]['kind']
    if kind=='observation' and not any(execution.get('clock')==m['at']*castle.ROUTINES[atomic_id]['duration'] for _,m in rows):ready=False
    physical['contact_ready']=ready and kind=='contact';physical['observation_ready']=ready and kind=='observation'
    return ready


def complete_observation(pond,plan):
    """A gauge read earns a reader observation receipt, never item operation."""
    from engine import carnival
    w=plan.get('carnival_work',{}) if isinstance(plan,dict) else {}
    if not isinstance(w,dict) or w.get('id')!='castle_gauge_check' or w.get('recorded'):return False
    def reject():
        reason='The reading callback lacks a valid actual reading and exit.'
        if pond.state.get('plan') is plan:
            if carnival.is_shared(plan):carnival.shared_controller(plan).interrupt(pond,plan,reason)
            else:castle.physical_interrupt(pond,plan,reason)
        else:
            # A late callback no longer owns Cheese's current movement or pose.
            # Release only leases still referring to this exact work record.
            w.update(done=True,interrupted=True,physical_error=reason)
            if isinstance(w.get('physical'),dict):
                w['physical'].update(contact_ready=False,observation_ready=False)
            for key,lease in list(pond.minds.carnival_guests.items()):
                if isinstance(lease,dict) and lease.get('work') is w:
                    pond.minds.carnival_guests.pop(key,None)
                    actors.release_owned(pond,key,lease)
            if pond.state.get('plan') is None:castle.clear(pond,plan)
            pond._cache=None
        return False
    try:
        if not carnival.completion_ready(pond,plan):return reject()
        inspection=w.get('inspection');archive=w.get('inspections')
        if (not isinstance(inspection,dict) or inspection.get('kind')!='pressure' or type(inspection.get('pressure')) not in (int,float) or not math.isfinite(inspection['pressure']) or not 0<=inspection['pressure']<=1 or not isinstance(archive,list) or inspection not in archive):return reject()
        m=pond.minds;s=w.get('shared',{});reader=s.get('operator',{}).get('actor','cheese');other=None
        if s.get('mode')=='flight-observer':other=s['observer']['actor']
        elif s.get('mode')!='egg-caregiver' and s.get('operator'):other='cheese'
        leasekey=s.get('observer',{}).get('actor') if s.get('mode')=='flight-observer' else s.get('operator',{}).get('actor')
        lease=m.carnival_guests.get(leasekey) if leasekey else None
        if leasekey and (not isinstance(lease,dict) or lease.get('work') is not w):return reject()
        if not isinstance(reader,str) or reader not in m.model.residents or other is not None and other not in m.model.residents:return reject()
        context=(lease['context'] if s.get('mode')=='egg-caregiver' else lease['contexts'][reader]) if lease else m.context(reader)
        if not isinstance(context,dict):return reject()
        if other and any(not isinstance(lease['contexts'].get(actor),dict) for actor in (reader,other)):return reject()
    except (KeyError,TypeError,ValueError,AttributeError):return reject()
    note=m.model.residents[reader]['name']+' read the actual pressure dial at '+str(inspection['pressure'])+'.'
    m.model.learn(reader,'observe',context,.25,m.now,note,other)
    if s.get('mode')=='egg-caregiver':m.model.learn(reader,'share',context,.25,m.now,note,'cheese')
    if other:
        for actor,partner in ((reader,other),(other,reader)):
            m.model.learn(actor,'share',lease['contexts'][actor],.25,m.now,note,partner)
    w['recorded']=True
    obj=pond.object_state('bounce_house',plan);history=obj.setdefault('carnival_routines',{});history[w['id']]=min(9999,history.get(w['id'],0)+1)
    if lease:
        company=obj.setdefault('carnival_company',{});company[leasekey]=min(9999,company.get(leasekey,0)+1)
        if s.get('mode')=='egg-caregiver':
            care=obj.setdefault('egg_caregiving',{});care[reader]=min(9999,care.get(reader,0)+1)
        m.carnival_guests.pop(leasekey,None);actors.release_owned(pond,leasekey,lease)
    castle.clear(pond,plan);pond._cache=None
    return True


def receipt_ready(pond,plan):
    """Recheck the actual material response immediately before final credit."""
    try:
        work=plan['carnival_work']
        if work['id'] not in ATOMIC_IDS:return True
        if type(work.get('expected_power_revision')) is not int or work['expected_power_revision']!=castle.state(pond.object_state('bounce_house',plan))['power_revision']:return False
        execution=dict(work,clock=work['ride_elapsed'])
        return terminal_ready(pond,plan,execution,{})['status']=='ready'
    except (TypeError,KeyError,ValueError,AttributeError):return False
