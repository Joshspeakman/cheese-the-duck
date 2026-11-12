"""Adult solo door and hose controls: native two-station movement and exact contacts.

Disposable saves only; real production snapshots and an observed contact trace.
"""
import os,sys,tempfile,json,copy,random
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-castle-multistation-')
os.environ['SDL_AUDIODRIVER']='dummy';os.environ['SDL_VIDEODRIVER']='dummy'
from engine import host,carnival,castle_work as castle,excursions
from engine.scene import snapshot
from engine.living_world import LivingPond
from world.habitat import PlacedItem
from world.atmosphere import Weather,WeatherType,Season
from audio.sound import sound_engine
sys.stdout=host.WIRE;random.seed(47);checks=[];frames=[];trace=[]
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
    def reset(score='castle_door_open',age='adult',root=(48,26),start=True):
        p.cancel();g.duck.current_action=None;g.behavior_ai.clear_action();g.duck.growth_stage=age
        for k in ('energy','hunger','fun','cleanliness','social'):setattr(g.duck.needs,k,95)
        g.duck_store.sync_from_duck(g.duck);g.friends.current_visit=None;g.atmosphere.current_visitor=None;p.state['story']=None
        g.habitat.owned_items=['bounce_house'];g.habitat.placed_items=[PlacedItem('bounce_house',9,7)];g.habitat.stored_items=[];g.habitat.stored_placements=[];g.building.structures=[]
        for room in g.decorations.rooms.values():room.decorations=[]
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x,pos.y=root
        p.sync();p.weather_type='sunny';p.season='spring';p.hour=12;p.state['ecology'].update(wind=.2,temperature=18);p.state['cooldowns']={}
        iid=next(a.instance for a in p.placements if a.item_id=='bounce_house');obj=p.object_state('bounce_house',iid)
        obj.update(last_use=-1000,uses=0,dirt=0,wetness=0,condition=1,excursion={},castle={},carnival_routines={},carnival_company={});excursions.state('bounce_house',obj);castle.state(obj).update(motor='on',power_hold=False,latch=1,door=0,hose=0)
        if not start:return iid,obj
        if not frames:capture('before')
        ok,message=carnival.request(p,'bounce_house',score,iid);check(ok,'production carnival.request starts '+age+' pilot: '+message)
        plan=p.state['plan'];return plan,plan['carnival_work'],obj
    def capture(case,event=None):
        p._cache=None;s=snapshot(g,g.renderer);s['_physicalCase']=case
        if event is not None:s['_physicalEvent']=event
        frames.append(s)
    def step(move=True,capture_case=None,dt=.2):
        p.state['elapsed']+=dt;pos=g.renderer.duck_pos
        if move:pos._state_start_time-=dt;pos.update(dt)
        p._activity(dt)
        if p.state['plan']:
            plan=p.state['plan'];w=plan['carnival_work'];obj=p.object_state('bounce_house',plan)
            excursions.update('bounce_house',obj,dt,True,p.weather_type,.2,p.hour,reserved=carnival.owns(p,'bounce_house',obj))
            if capture_case:
                capture(capture_case);trace.append(dict(case=capture_case,objectInstance=plan['instance'],actor='cheese',sequenceId=w['id'],root=[pos.x,pos.y],physical=carnival.view(p,plan).get('physical'),events=list(w['events']),clock=w['clock'],motor=obj['castle']['motor']))
    def until(predicate,label,limit=1600):
        for _ in range(limit):
            if predicate():return
            step()
        raise AssertionError(label+': '+str(p.state.get('plan')))
    def finish():until(lambda:p.state['plan'] is None,'completion')
    original_apply=castle.apply
    def observe_apply(obj,w,index,effect):
        original_apply(obj,w,index,effect)
        if w['id'] in ('castle_door_open','castle_hose_stow'):
            capture(w['id']+' contact '+str(index),index)
            physical=w['physical'];metric=castle.effect_metrics(w)[index]
            trace.append(dict(score=w['id'],event=index,clock=w['clock'],station=physical['station'],root=list(physical['root']),target=list(physical['target']),grip=metric['grip'],events=list(w['events']),motor=obj['castle']['motor']))
            check(w['clock']==effect[0]*castle.ROUTINES[w['id']]['duration'],w['id']+' effect occurs at exact authored time '+str(index))
            check(physical['station']==metric['station'] and physical['phase']=='hold' and physical['contact_ready'],w['id']+' effect owns reached station '+str(index))
            check(castle.reach_distance(physical['root'],physical['target'],metric['grip'])<=3,w['id']+' exact authored grip reaches '+str(index))
    castle.apply=observe_apply
    for score in ('castle_door_open','castle_hose_stow'):
        plan,w,obj=reset(score);duration=castle.ROUTINES[score]['duration'];boundary=castle.physical_stations(w)[1][0]*duration
        check(castle.physical_active(plan) and not w['paired'],score+' native adult solo reservation')
        root=[g.renderer.duck_pos.x,g.renderer.duck_pos.y]
        for _ in range(20):step(move=False)
        check(w['clock']==0 and not w['events'],score+' no initial arrival means no score or contact')
        until(lambda:w['stage']=='service',score+' first arrival');capture(score+' first arrival')
        # A huge tick stops exactly at the real second-leg departure.
        step(dt=100)
        check(w['clock']==boundary and w['events']==[0] and w['physical']['phase']=='approach',score+' large dt cannot skip second station travel')
        capture(score+' departure')
        check(not w['physical']['contact_ready'],score+' departure releases grip')
        if score=='castle_hose_stow':check(obj['castle']['motor']=='off' and obj['castle']['power_hold'] and obj['castle']['targets']['hose']==0,'hose shuts down before moving or coiling')
        for _ in range(20):step(move=False)
        check(w['clock']==boundary and w['events']==[0],score+' frozen actor cannot accrue second station work')
        # Explicit paused fixture and direct care exercise native stepping and production resume.
        plan['paused']=True;pos=g.renderer.duck_pos;frozen=[pos.x,pos.y];step();frozen=[pos.x,pos.y]
        for _ in range(8):step()
        check([pos.x,pos.y]==frozen and w['clock']==boundary,score+' pause holds root and service clock')
        p.command(dict(action='resume'));g.duck.current_action='feed';step();frozen=[pos.x,pos.y]
        for _ in range(8):step()
        check([pos.x,pos.y]==frozen and w['clock']==boundary,score+' direct care holds root and service clock')
        g.duck.current_action=None
        step();capture(score+' transfer walking')
        until(lambda:w['physical']['phase']=='hold',score+' second arrival');capture(score+' second arrival')
        check(w['physical']['station_index']==1 and w['events']==[0],score+' real second stance acquired before its first effect')
        until(lambda:w['physical']['phase']=='exit',score+' actual exit');capture(score+' exit')
        finish()
        check(w['events']==[0,1,2,3] and obj['uses']==1 and obj['carnival_routines'].get(score)==1 and not obj['carnival_company'],score+' exactly four contacts and one solo completion')
        field='door' if score=='castle_door_open' else 'hose'
        check(obj['castle']['targets'][field]==1 and obj['castle'][field]>.99,score+' actual material reaches final endpoint')
        # Cancellation after first effect preserves the actual unlatch/shutdown.
        plan,w,obj=reset(score);until(lambda:w['events']==[0],score+' first effect for cancellation');p.cancel()
        check(obj['uses']==0 and not obj['carnival_routines'] and not obj['carnival_company'],score+' cancellation earns no completion')
        check(obj['castle']['latch']==0 if score=='castle_door_open' else obj['castle']['motor']=='off',score+' cancellation preserves consumed first effect')
        # Save in second-leg transit; restore through production attach.
        plan,w,obj=reset(score);until(lambda:w['physical']['station_index']==1,score+' save second leg')
        saved=json.loads(json.dumps(p.save()));saved_root=[g.renderer.duck_pos.x,g.renderer.duck_pos.y]
        old=p;restored=LivingPond(saved);g.living_pond=restored;p=restored;restored.attach(g,offline=False);p.state['auto']=False;p.minds.model.state['next_social']=1e9
        loaded=p.state['plan'];rw=loaded['carnival_work'];ro=p.object_state('bounce_house',loaded)
        check(loaded['paused'] and rw['events']==[0] and rw['physical']['station_index']==1 and [g.renderer.duck_pos.x,g.renderer.duck_pos.y]==saved_root,score+' restore retains consumed contact and current station without teleport')
        p.command(dict(action='resume'));finish();check(ro['uses']==1 and rw['events']==[0,1,2,3],score+' restored second leg completes once')
        old.minds.close()
        plan,w,obj=reset(score);until(lambda:w['events']==[0,1],score+' second contact save')
        partial=json.loads(json.dumps(p.save()));old=p;restored=LivingPond(partial);g.living_pond=restored;p=restored;restored.attach(g,offline=False);p.state['auto']=False;p.minds.model.state['next_social']=1e9
        loaded=p.state['plan'];rw=loaded['carnival_work'];ro=p.object_state('bounce_house',loaded)
        check(rw['events']==[0,1] and rw['physical']['station_index']==1 and ro['castle']['targets'][field]==.35,score+' restore preserves second contact and its material target')
        p.command(dict(action='resume'));finish();check(ro['uses']==1 and rw['events']==[0,1,2,3],score+' partial second-station restore never replays earlier effects')
        old.minds.close()
        saved=partial
        # Cursor, target, route and event forgeries must all fail closed.
        for field,value in [('station_index',0),('station','switch'),('target',[0,0]),('route',[[0,0]]),('waypoint',999)]:
            forged=copy.deepcopy(saved);fw=forged['plan']['carnival_work'];fw['physical'][field]=value
            prior=p;restored=LivingPond(forged);g.living_pond=restored;p=restored;restored.attach(g,offline=False)
            check(p.state['plan']['carnival_work'].get('interrupted'),score+' rejects forged '+field)
            prior.minds.close()
        plan,w,obj=reset(score);until(lambda:w['events']==[0],score+' first effect before obstacle')
        target=castle.control_world(w['physical']['center'],castle.physical_stations(w)[1][1])
        # A real rock blocks the second stance without covering the first.
        g.habitat.owned_items.append('rock');g.habitat.placed_items.append(PlacedItem('rock',(target[0]-1)*20/132,26*12/42));p.sync()
        until(lambda:p.state['plan'] is None,score+' blocked second station')
        check(w.get('interrupted') and obj['uses']==0 and w['events']==[0],score+' actual second-station obstacle prevents later contacts and completion: '+str((w.get('interrupted'),obj['uses'],w['events'],w.get('physical_error'))))
        check(obj['castle']['latch']==0 if score=='castle_door_open' else obj['castle']['motor']=='off',score+' blocked second leg preserves consumed first effect')
        plan,w,obj=reset(score);g.habitat.placed_items=[];p.sync();step()
        check(p.state['plan'] is None and obj['uses']==0,score+' removing the actual copy cancels without credit')
    castle.apply=original_apply
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
    (out/'castle-multistation-frames.json').write_text(json.dumps(frames))
    result=dict(result='PASS',checks=len(checks),frames=len(frames),trace=trace,routines=['castle_door_open','castle_hose_stow'])
    (out/'castle-multistation-native.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='trace'}))
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
