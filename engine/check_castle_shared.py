"""Real regular-visitor operation and Cheese observation, disposable saves only."""
import os,sys,tempfile,json,copy,random
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-castle-shared-');os.environ['SDL_AUDIODRIVER']='dummy';os.environ['SDL_VIDEODRIVER']='dummy'
from engine import host,carnival,castle_work as castle,castle_shared as shared,excursions
from engine.scene import snapshot
from engine.living_world import LivingPond
from world.habitat import PlacedItem
from world.friends import visitor_animator,DuckPersonalityType
from world.guest_cast import PROFILES
from world.atmosphere import Weather,WeatherType,Season
from audio.sound import sound_engine
sys.stdout=host.WIRE;random.seed(57);checks=[];frames=[];trace=[];clock=0.;observer_age='adult'
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
        g.habitat.owned_items=['bounce_house'];g.habitat.placed_items=[PlacedItem('bounce_house',9,6)];g.habitat.stored_items=[];g.habitat.stored_placements=[];g.building.structures=[]
        for room in g.decorations.rooms.values():room.decorations=[]
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=44 if '--all-ages' in sys.argv else 48;pos.y=26
        f=copy.deepcopy(original);f.id='shared-test:'+cast;f.name=PROFILES[cast]['name'];f.personality=DuckPersonalityType(PROFILES[cast]['archetype']);g.friends.friends[f.id]=f;g.friends.current_visit=None;g.friends.start_visit(f.id)
        personality=f.personality.value if hasattr(f.personality,'value') else str(f.personality)
        visitor_animator.set_visitor(personality,f.name);visitor_animator._is_leaving=False
        visitor_animator._position_x=64-g.renderer._camera_x;visitor_animator._position_y=24-g.renderer._camera_y;visitor_animator._target_x=visitor_animator._position_x;visitor_animator._target_y=visitor_animator._position_y;visitor_animator._last_move_time=clock;visitor_animator._rest_until=clock+100
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
        s['_sharedCast']=p.state['plan']['carnival_work']['shared']['operator']['cast'];s['_physicalAge']=observer_age;frames.append(s)
    def step(dt=.2,move=True):
        global clock
        clock+=dt;p.state['elapsed']+=dt;shared.refresh(p)
        if g.friends.current_visit:
            meeting=shared.motion(p.minds,g.friends.current_visit.friend_id)
            visitor_animator._mind_motion={'meeting':dict(meeting,target=[meeting['target'][0]-g.renderer._camera_x,meeting['target'][1]-g.renderer._camera_y])} if meeting else {}
        pos=g.renderer.duck_pos
        if move:pos._state_start_time-=dt;pos.update(dt);visitor_animator.update(clock,pos.x-g.renderer._camera_x,pos.y-g.renderer._camera_y)
        p._activity(dt)
        if p.state['plan']:
            plan=p.state['plan'];obj=p.object_state('bounce_house',plan);excursions.update('bounce_house',obj,dt,True,p.weather_type,.2,p.hour,reserved=carnival.owns(p,'bounce_house',obj))
        p.minds.sync()
    def until(predicate,label,limit=5000):
        for _ in range(limit):
            if predicate():return
            if not p.state['plan']:raise AssertionError(label+' lost plan: '+str(w.get('physical_error')))
            step()
        raise AssertionError(label+': '+str(p.state['plan']))
    original_apply=castle.apply
    def observed_apply(obj,w,index,effect):
        original_apply(obj,w,index,effect)
        if not w.get('shared_physical'):return
        s=w['shared'];ph=w['physical'];live=shared.actors.regular(p);metric=shared.operator_metrics(s['operator']['cast'],w['id'])[index]
        check(ph['actor']==live['actor'] and ph['actor']!='cheese' and ph['contact_ready'],'only actual leased visitor owns mechanical contact')
        check(w['clock']==effect[0]*castle.ROUTINES[w['id']]['duration'] and castle.reach_distance(live['root'],ph['target'],metric['grip'],metric['scale'])<=3,'exact event time and real profile grip')
        check(shared.near(shared.cheese_root(p),s['cheese']['stance'],.51) and g.renderer.duck_pos.facing_right==(live['root'][0]>=shared.cheese_root(p)[0]),'Cheese observes from actual distinct stance facing the real operator')
        capture(s['operator']['cast']+' '+w['id']+' contact '+str(index),index)
        trace.append(dict(age=observer_age,cast=s['operator']['cast'],score=w['id'],event=index,operator=live['actor'],operatorRoot=live['root'],cheeseRoot=shared.cheese_root(p),target=ph['target'],station=ph['station'],clock=w['clock'],events=list(w['events'])))
    castle.apply=observed_apply
    casts=list(shared.METRIC_DATA['adapters']['regular'])
    if '--one' in sys.argv:casts=casts[:1]
    if '--cast' in sys.argv:casts=[sys.argv[sys.argv.index('--cast')+1]]
    bindings=[(cast,'adult') for cast in casts]
    if '--all-ages' in sys.argv:bindings=[(casts[0],age) for age in shared.METRIC_DATA['observers']]
    for cast,observer_age in bindings:
        for score in sorted(castle.PHYSICAL_SCORES):
            plan,w,obj,f=reset(cast,score);capture(cast+' '+score+' waiting')
            before={key:copy.deepcopy(p.minds.model.residents[key]['counts']) for key in ('cheese',f.id)}
            until(lambda:w['shared']['phase']=='exit',cast+' '+score+' exit');capture(cast+' '+score+' exits')
            until(lambda:p.state['plan'] is None,cast+' '+score+' completion')
            check(w.get('recorded') and obj['uses']==1 and obj['carnival_routines'].get(score)==1 and obj['carnival_company'].get(f.id)==1,cast+' '+score+' one use and shared receipt')
            for key in ('cheese',f.id):check(p.minds.model.residents[key]['counts']['share']==before[key].get('share',0)+1,'completed sharing learns once')
            check(p.minds.model.residents['cheese']['counts']['observe']==before['cheese'].get('observe',0)+1,'Cheese learns observation once')
            check(p.minds.model.residents[f.id]['counts']['practice']==before[f.id].get('practice',0)+1,'operator learns actual work once')
            snapshot_reward=copy.deepcopy((obj,p.minds.model.state,g.duck.needs.__dict__,p.state['skills']))
            p._complete(plan)
            check((obj,p.minds.model.state,g.duck.needs.__dict__,p.state['skills'])==snapshot_reward,'duplicate callback earns no additional rewards')
    castle.apply=original_apply
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
    prefix='castle-shared-ages' if '--all-ages' in sys.argv else 'castle-shared'
    (out/(prefix+'-frames.json')).write_text(json.dumps(frames));result=dict(result='PASS',checks=len(checks),frames=len(frames),casts=len(set(c for c,a in bindings)),observer_ages=sorted(set(a for c,a in bindings)),trace=trace)
    (out/(prefix+'-native.json')).write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='trace'}))
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
