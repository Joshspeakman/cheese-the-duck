"""Exact47guest/48adapter air-control matrix with actual movers and finite visits."""
import os,sys,tempfile,json,copy,random,hashlib
from pathlib import Path
from datetime import datetime,timedelta
from unittest.mock import patch
from contextlib import ExitStack
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-castle-shared-');os.environ['SDL_AUDIODRIVER']='dummy';os.environ['SDL_VIDEODRIVER']='dummy'
from engine import host,carnival,castle_work as castle,castle_shared as shared,egg_caregiver as egg,excursions
from engine.scene import snapshot
from engine.living_world import LivingPond
from world.habitat import PlacedItem
from world.friends import visitor_animator,DuckPersonalityType
from world.guest_cast import PROFILES
from world.atmosphere import Weather,WeatherType,Season,VISITORS
from audio.sound import sound_engine
sys.stdout=host.WIRE;random.seed(57);checks=[];frames=[];trace=[];pending=[];clock=0.;observer_age='adult';placement=(9,5);guest_root=tuple(map(float,sys.argv[sys.argv.index('--root')+1:sys.argv.index('--root')+3])) if '--root' in sys.argv else (72.,25.);case_id=None;simulation_base=datetime.now();patches=ExitStack()
def check(ok,label):
    assert ok,label
    checks.append(label)
t=host.DesktopInput();g=host.DesktopGame(terminal=t,renderer_factory=host.CanvasRenderer);t.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
    g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.renderer._show_talk=False;sound_engine.enabled=False
    g.renderer._viewport_width=132;g.renderer._viewport_height=42;g.renderer._update_camera(132,42)
    p=g.living_pond;p.state['auto']=False;p.minds.model.state['next_social']=1e9
    g.day_night.get_current_hour=lambda:12;g.day_night.get_current_minute=lambda:0
    g.atmosphere.current_season=Season.SPRING;g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.5,1,datetime.now().isoformat())
    original=g.friends.generate_new_friend()
    def reset(cast,score,start=True):
        p.cancel();g.duck.current_action=None;g.behavior_ai.clear_action();g.duck.growth_stage=observer_age
        for k in ('energy','hunger','fun','cleanliness','social'):setattr(g.duck.needs,k,80)
        g.duck_store.sync_from_duck(g.duck);g.atmosphere.current_visitor=None;p.state['story']=None
        for name in shared.RESERVED:getattr(p.minds,name).clear()
        p.minds.carnival_guests.clear();p.minds.carnival_retry.clear()
        g.habitat.owned_items=['bounce_house'];g.habitat.placed_items=[PlacedItem('bounce_house',*placement)];g.habitat.stored_items=[];g.habitat.stored_placements=[];g.building.structures=[]
        for room in g.decorations.rooms.values():room.decorations=[]
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=44;pos.y=26;pos.facing_right=False;pos.frozen=False
        if adapter=='regular':
            f=copy.deepcopy(original);f.id='shared-test:'+cast;f.name=PROFILES[cast]['name'];f.personality=DuckPersonalityType(PROFILES[cast]['archetype']);g.friends.friends[f.id]=f;g.friends.current_visit=None;g.friends.start_visit(f.id)
            personality=f.personality.value if hasattr(f.personality,'value') else str(f.personality)
            visitor_animator.set_visitor(personality,f.name);visitor_animator._is_leaving=False
            visitor_animator._position_x=guest_root[0]-g.renderer._camera_x;visitor_animator._position_y=guest_root[1]-g.renderer._camera_y;visitor_animator._target_x=visitor_animator._position_x;visitor_animator._target_y=visitor_animator._position_y;visitor_animator._last_move_time=clock;visitor_animator._rest_until=clock+100
        else:
            g.friends.current_visit=None
            if adapter=='rare':
                g.atmosphere.current_visitor=(VISITORS[cast],datetime.now().isoformat());g.guest_motion.token=None;g.guest_motion.tick(g,clock);mover=g.guest_motion;actor=cast
            else:
                p.state['story']=dict(id='lost_duckling',step=0,x=64,y=24);g.story_motion.token=None;g.story_motion.tick(g,clock);mover=g.story_motion;actor='story:pip'
            mover.actor.update(x=guest_root[0],y=guest_root[1]);mover.target=guest_root;mover.last=clock
            from types import SimpleNamespace
            f=SimpleNamespace(id=actor)
        p.sync();p.weather_type='sunny';p.season='spring';p.hour=12;p.state['ecology'].update(wind=.2,temperature=18);p.state['cooldowns']={};p.minds.sync()
        p.minds.model.residents[f.id]['energy']=.9;p.minds.tasks[f.id]=dict(action='observe',until=p.minds.now+1000,context=p.minds.context(f.id))
        iid=next(a.instance for a in p.placements if a.item_id=='bounce_house');obj=p.object_state('bounce_house',iid)
        obj.update(last_use=-1000,uses=0,dirt=0,wetness=0,condition=1,excursion={},castle={},carnival_routines={},carnival_company={});excursions.state('bounce_house',obj);castle.state(obj).update(motor='off' if score=='castle_start' else 'on',latch=1)
        if not start:return iid,obj,f
        ok,msg=carnival.request(p,'bounce_house',score,iid,together=True);check(ok,cast+' '+observer_age+' '+score+' starts: '+msg)
        plan=p.state['plan'];return plan,plan['carnival_work'],obj,f
    def capture(label,event=None):
        p._cache=None;s=snapshot(g,g.renderer);s['_physicalCase']=label
        if event is not None:s['_physicalEvent']=event
        s['_sharedCast']=p.state['plan']['carnival_work']['shared']['operator']['cast'];s['_physicalAge']=observer_age;s['_airMatrixCase']=case_id;frames.append(s)
    def step(dt=.2,move=True):
        global clock
        active=p.state.get('plan')
        if active:
            work=active['carnival_work'];elapsed=work['clock'];future=[e[0]*castle.ROUTINES[work['id']]['duration']-elapsed for i,e in enumerate(castle.ROUTINES[work['id']]['effects']) if i not in work['events'] and e[0]*castle.ROUTINES[work['id']]['duration']>elapsed]
            if future:dt=min(dt,min(future))
        clock+=dt;p.state['elapsed']+=dt;shared.refresh(p)
        if g.friends.current_visit:
            meeting=shared.motion(p.minds,g.friends.current_visit.friend_id)
            visitor_animator._mind_motion={'meeting':dict(meeting,target=[meeting['target'][0]-g.renderer._camera_x,meeting['target'][1]-g.renderer._camera_y])} if meeting else {}
        pos=g.renderer.duck_pos
        if move:
            pos._state_start_time-=dt;pos.update(dt)
            if adapter=='regular':visitor_animator.update(clock,pos.x-g.renderer._camera_x,pos.y-g.renderer._camera_y)
            else:(g.guest_motion if adapter=='rare' else g.story_motion).tick(g,clock)
        if p.state['plan']:
            plan=p.state['plan'];obj=p.object_state('bounce_house',plan);excursions.update('bounce_house',obj,dt,True,p.weather_type,.2,p.hour,reserved=carnival.owns(p,'bounce_house',obj))
            p._activity(dt)
        p.minds.sync();shared.refresh(p)
        for event in pending[:]:capture(event[0],event[1]);pending.remove(event)
    def until(predicate,label,limit=5000):
        for _ in range(limit):
            if predicate():return
            if not p.state['plan']:raise AssertionError(label+' lost plan: '+str(w.get('physical_error')))
            step()
        raise AssertionError(label+': '+str(p.state['plan']))
    class SimDatetime(datetime):
        @classmethod
        def now(cls,tz=None):return simulation_base+timedelta(seconds=clock)
    from engine import guest_motion,visitor_shelters
    import world.friends as friends_module
    patches.enter_context(patch('datetime.datetime',SimDatetime))
    patches.enter_context(patch.object(guest_motion,'datetime',SimDatetime))
    patches.enter_context(patch.object(visitor_shelters,'datetime',SimDatetime))
    patches.enter_context(patch.object(friends_module,'datetime',SimDatetime))
    patches.enter_context(patch('engine.guest_motion.time.monotonic',lambda:clock))
    datetime=SimDatetime
    adapter='regular' 
    from engine import castle_air as air
    metrics_sha=hashlib.sha256((ROOT/'engine/client/animation/castle-air-metrics.json').read_bytes()).hexdigest()
    original_apply=castle.apply
    def observe_apply(obj,w,index,effect):
        original_apply(obj,w,index,effect)
        ph=w['physical'];operator=w['shared']['operator'];metric=air.event_metric(operator,w['id'],index)
        check(w['clock']==effect[0]*castle.ROUTINES[w['id']]['duration'],'exact authored event clock')
        live=air.operator_state(p,operator)
        if metric['kind']=='observation':
            check(ph.get('observation_ready') and not ph['contact_ready'],'actual reading never mechanical contact')
            check(air.sightline(p,p.state['plan'],live['root'],live['facing'],metric,ph['center']),'actual eyes and clear needle ray')
        else:check(ph['contact_ready'] and castle.reach_distance(live['root'],ph['target'],metric['grip'],metric['scale'])<=3,'actual operator grip bounded')
        capture(w['id']+' effect '+str(index),index)
    castle.apply=observe_apply
    cases=[]
    bindings=[('regular',c) for c in shared.METRIC_DATA['adapters']['regular']]+[('rare',c) for c in shared.actors.SPECIAL+shared.actors.SPECIES]+[('story','lost_duckling')]
    if '--cast' in sys.argv:bindings=[v for v in bindings if v[1]==sys.argv[sys.argv.index('--cast')+1]]
    for adapter,cast in bindings:
        if '--safe-roots' in sys.argv:guest_root=(64.,24.) if cast in ('friend:georgia','friend:raven','friend:biscuit','friendly_goose') else (72.,25.)
        for score in sorted(set(sys.argv[sys.argv.index('--scores')+1].split(',')) if '--scores' in sys.argv else castle.AIR_SCORES):
            case_id='shared/adult/'+cast+'/'+adapter+'/'+score
            case=dict(geometry_sha256=hashlib.sha256(json.dumps(dict(events=air.DATA['casts'][cast]['routines'][score],travel=air.DATA['casts'][cast]['travel']),sort_keys=True,separators=(',',':')).encode()).hexdigest(),id=case_id,mode='shared',age='adult',cast=cast,adapter=adapter,score=score,attempts=[])
            for placement in ((9,5),(9,6),(8,5),(10,5)):
                iid,obj,f=reset(cast,score,start=False)
                before=copy.deepcopy(obj['castle']);tasks=copy.deepcopy(p.minds.tasks)
                actual=shared.actors.live(p,next(shared.actors.identity(v) for v in shared.actors.candidates(p) if v['cast']==cast and v['adapter']==adapter))
                before_root=list(actual['root']);before_cheese=shared.cheese_root(p)
                ok,reason=carnival.request(p,'bounce_house',score,iid,together=True)
                case['attempts'].append(dict(placement=list(placement),operator_root=list(before_root),cheese_root=list(before_cheese),accepted=ok,reason=reason))
                if not ok:
                    check(obj['castle']==before and not obj['carnival_routines'] and obj['uses']==0 and not p.minds.carnival_guests,'refused invitation has no material effect reward or lease')
                    check(p.minds.tasks==tasks and shared.cheese_root(p)==before_cheese,'refused invitation preserves actor tasks and roots')
                    continue
                plan=p.state['plan'];w=plan['carnival_work'];case.update(status='supported',operator_root=list(before_root),cheese_root=list(before_cheese),placement=list(placement),center=list(w['physical']['center']),required_seconds=w['shared'].get('required_seconds'),remaining_seconds=w['shared'].get('remaining_seconds'),visit_duration_seconds=g.friends.current_visit.duration_minutes*60 if adapter=='regular' else None)
                start_clock=clock;capture('accepted approach')
                before_counts=copy.deepcopy({key:p.minds.model.residents[key]['counts'] for key in ('cheese',f.id)})
                until(lambda:w['shared']['phase']=='exit',case_id+' exit');capture('actual independent exits')
                until(lambda:p.state['plan'] is None,case_id+' completion')
                check(w.get('recorded') and not w.get('interrupted'),case_id+' completed receipt '+str(w.get('physical_error')))
                check(w['events']==list(range(len(castle.ROUTINES[score]['effects']))),'all authored matrix events')
                if score=='castle_gauge_check':
                    check(obj['uses']==0 and p.minds.model.residents[f.id]['counts'].get('observe',0)==before_counts[f.id].get('observe',0)+1,'actual reader observation without item use')
                    for key in ('cheese',f.id):check(p.minds.model.residents[key]['counts'].get('practice',0)==before_counts[key].get('practice',0),'gauge earns no mechanical practice')
                case.update(events=list(w['events']),seconds=clock-start_clock,inspection=w.get('inspection'),material=copy.deepcopy(obj['castle']))
                if adapter=='rare':check(case['seconds']<case['remaining_seconds']-6,'real rare duration retains departure reserve')
                if adapter=='regular':check(case['seconds']<case['visit_duration_seconds'],'real regular visit does not expire during the attempt')
                break
            else:case.update(status='refused',reason=case['attempts'][-1]['reason'])
            cases.append(case)
        print(json.dumps(dict(progress=cast,adapter=adapter,cases=len(cases),supported=sum(c['status']=='supported' for c in cases))),flush=True)
    castle.apply=original_apply
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
    suffix='-'+sys.argv[sys.argv.index('--cast')+1].replace(':','-') if '--cast' in sys.argv else ''
    if '--root' in sys.argv:suffix+='-root-'+str(guest_root[0])+'-'+str(guest_root[1])
    if '--safe-roots' in sys.argv:suffix+='-safe-roots'
    if '--scores' in sys.argv:suffix+='-'+sys.argv[sys.argv.index('--scores')+1].replace(',','-')
    frames_file='castle-air-guests-matrix'+suffix+'-frames.json';payload=json.dumps(frames);(out/frames_file).write_text(payload)
    result=dict(schema_version=1,result='PASS',scope='Selected exact guest adapter/control cases with adult observer; no unstated cross-age coverage',checks=len(checks),frames=len(frames),frames_file=frames_file,metrics_sha256=metrics_sha,frames_sha256=hashlib.sha256(payload.encode()).hexdigest(),cases=cases)
    (out/('castle-air-guests-matrix'+suffix+'-manifest.json')).write_text(json.dumps(result,indent=2))
    print(json.dumps(dict(result='PASS',checks=len(checks),frames=len(frames),cases=len(cases),supported=sum(c['status']=='supported' for c in cases),refused=sum(c['status']=='refused' for c in cases))))
finally:
    patches.close()
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
