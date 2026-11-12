"""Real Cheese operation and independent Flutter flight observation, disposable saves only."""
import os,sys,tempfile,json,copy,random
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-castle-shared-');os.environ['SDL_AUDIODRIVER']='dummy';os.environ['SDL_VIDEODRIVER']='dummy'
from engine import host,carnival,castle_work as castle,castle_shared as shared,castle_flight as flight,excursions
from engine.scene import snapshot
from engine.living_world import LivingPond
from world.habitat import PlacedItem
from world.friends import visitor_animator,DuckPersonalityType
from world.guest_cast import PROFILES
from world.atmosphere import Weather,WeatherType,Season,VISITORS
from audio.sound import sound_engine
sys.stdout=host.WIRE;random.seed(57);checks=[];frames=[];trace=[];pending=[];moving_seen=set();clock=0.;observer_age='adult'
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
    original=None
    def reset(cast,score,start=True):
        moving_seen.clear();p.cancel();g.duck.current_action=None;g.behavior_ai.clear_action();g.duck.growth_stage=observer_age
        for k in ('energy','hunger','fun','cleanliness','social'):setattr(g.duck.needs,k,80)
        g.duck_store.sync_from_duck(g.duck);g.atmosphere.current_visitor=None;p.state['story']=None
        for name in shared.RESERVED:getattr(p.minds,name).clear()
        p.minds.carnival_guests.clear();p.minds.carnival_retry.clear()
        g.habitat.owned_items=['bounce_house'];g.habitat.placed_items=[PlacedItem('bounce_house',9,5)];g.habitat.stored_items=[];g.habitat.stored_placements=[];g.building.structures=[]
        for room in g.decorations.rooms.values():room.decorations=[]
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=44 if '--all-ages' in sys.argv else 48;pos.y=26
        g.friends.current_visit=None
        if adapter=='rare':
            g.atmosphere.current_visitor=(VISITORS[cast],datetime.now().isoformat());g.guest_motion.token=None;g.guest_motion.tick(g,clock);mover=g.guest_motion;actor=cast
        else:
            p.state['story']=dict(id='lost_duckling',step=0,x=64,y=24);g.story_motion.token=None;g.story_motion.tick(g,clock);mover=g.story_motion;actor='story:pip'
        mover.actor.update(x=26.,y=28.);mover.target=(26.,28.);mover.last=clock
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
        s['_sharedCast']=p.state['plan']['carnival_work']['shared']['observer']['cast'];s['_physicalAge']=observer_age;frames.append(s)
    def step(dt=.2,move=True):
        global clock
        active=p.state.get('plan')
        if active and active.get('phase')=='act':
            work=active.get('carnival_work',{});elapsed=work.get('clock',0)
            future=[e[0]*castle.ROUTINES[work['id']]['duration']-elapsed for i,e in enumerate(castle.ROUTINES[work['id']]['effects']) if i not in work['events'] and e[0]*castle.ROUTINES[work['id']]['duration']>elapsed]
            if future:dt=min(dt,min(future))
        previous_cheese=shared.cheese_root(p);previous_flutter=list(flight.actors.flight(p)['root'])
        clock+=dt;p.state['elapsed']+=dt;flight.refresh(p)
        pos=g.renderer.duck_pos
        if move:
            pos._state_start_time-=dt;pos.update(dt)
            (g.guest_motion if adapter=='rare' else g.story_motion).tick(g,clock)
        if p.state['plan']:
            plan=p.state['plan'];obj=p.object_state('bounce_house',plan);excursions.update('bounce_house',obj,dt,True,p.weather_type,.2,p.hour,reserved=carnival.owns(p,'bounce_house',obj))
            p._activity(dt)
        p.minds.sync();flight.refresh(p)
        current=p.state.get('plan')
        if current and (shared.cheese_root(p)!=previous_cheese or flight.actors.flight(p)['root']!=previous_flutter):
            work=current['carnival_work'];s=work['shared'];ph=work['physical'];key=(s['phase'],ph['phase'],ph['station'],s['observer_physical']['phase'])
            if key not in moving_seen:moving_seen.add(key);capture('actual motion '+str(key))
        for event in pending[:]:
            capture(event[0],event[1]);pending.remove(event)
    def until(predicate,label,limit=5000):
        for _ in range(limit):
            if predicate():return
            if not p.state['plan']:raise AssertionError(label+' lost plan: '+str(w.get('physical_error')))
            step()
        raise AssertionError(label+': '+str(p.state['plan']))
    adapter='rare'
    from engine import castle_air as air
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
    for score in sorted(castle.AIR_SCORES):
        plan,w,obj,f=reset('butterfly_fairy',score)
        before_counts=copy.deepcopy({key:p.minds.model.residents[key]['counts'] for key in ('cheese',f.id)})
        before_egg=copy.deepcopy((g.duck.needs.__dict__,p.state.get('skills'),p.state.get('preferences')))
        until(lambda:p.state['plan'] is None,score+' completion')
        check(w.get('recorded') and not w.get('interrupted'),score+' receipt')
        reader='cheese' if 'flight'=='flight' else f.id
        if score=='castle_gauge_check':
            check(obj['uses']==0,'gauge observation earns no item use')
            for key in ('cheese',f.id):check(p.minds.model.residents[key]['counts'].get('practice',0)==before_counts[key].get('practice',0),'gauge never earns mechanical practice')
            check(p.minds.model.residents[reader]['counts'].get('observe',0)==before_counts[reader].get('observe',0)+1,'actual reader learns observation exactly once')
        if 'flight'=='egg':
            check(p.minds.model.residents['cheese']['counts']==before_counts['cheese'],'egg receives no actor learning')
            check((g.duck.needs.__dict__,p.state.get('skills'),p.state.get('preferences'))==before_egg,'egg receives no item need skill or preference reward')
        before_duplicate=copy.deepcopy((obj,p.minds.model.state,g.duck.needs.__dict__,p.state.get('skills')))
        p._complete(plan)
        check((obj,p.minds.model.state,g.duck.needs.__dict__,p.state.get('skills'))==before_duplicate,'duplicate callback awards nothing')

    castle.apply=original_apply
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
    (out/'castle-air-flight-frames.json').write_text(json.dumps(frames))
    result=dict(result='PASS',checks=len(checks),frames=len(frames),mode='flight')
    (out/'castle-air-flight-native.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
