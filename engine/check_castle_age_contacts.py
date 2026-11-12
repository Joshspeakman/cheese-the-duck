"""Age-specific native contacts for three controls; no egg or assistance adoption.

Disposable saves only; real production snapshots and an observed contact trace.
"""
import os,sys,tempfile,json,copy,random
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-castle-age-')
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
    def reset(score='castle_door_open',age='adult',root=(48,26),start=True,placement=(9,7),expect=True):
        p.cancel();g.duck.current_action=None;g.behavior_ai.clear_action();g.duck.growth_stage=age
        for k in ('energy','hunger','fun','cleanliness','social'):setattr(g.duck.needs,k,95)
        g.duck_store.sync_from_duck(g.duck);g.friends.current_visit=None;g.atmosphere.current_visitor=None;p.state['story']=None
        g.habitat.owned_items=['bounce_house'];g.habitat.placed_items=[PlacedItem('bounce_house',*placement)];g.habitat.stored_items=[];g.habitat.stored_placements=[];g.building.structures=[]
        for room in g.decorations.rooms.values():room.decorations=[]
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x,pos.y=root
        p.sync();p.weather_type='sunny';p.season='spring';p.hour=12;p.state['ecology'].update(wind=.2,temperature=18);p.state['cooldowns']={}
        iid=next(a.instance for a in p.placements if a.item_id=='bounce_house');obj=p.object_state('bounce_house',iid)
        obj.update(last_use=-1000,uses=0,dirt=0,wetness=0,condition=1,excursion={},castle={},carnival_routines={},carnival_company={});excursions.state('bounce_house',obj);castle.state(obj).update(motor='on',power_hold=False,latch=1,door=0,hose=0)
        if not start:return iid,obj
        if not frames:capture('before')
        ok,message=carnival.request(p,'bounce_house',score,iid)
        check(ok==expect,'production request '+str(age)+' '+score+': '+message)
        if not ok:return None,None,obj
        plan=p.state['plan'];return plan,plan['carnival_work'],obj
    def capture(case,event=None):
        p._cache=None;s=snapshot(g,g.renderer);s['_physicalCase']=case;s['_physicalAge']=castle.canonical_age(g.duck.growth_stage) or g.duck.growth_stage
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
        physical=w['physical'];metric=castle.effect_metrics(w)[index];pos=g.renderer.duck_pos;root=[pos.x,pos.y]
        capture(w['source_age']+' '+w['id']+' event '+str(index),index)
        check(physical['source_age']==castle.canonical_age(g.duck.growth_stage),w['source_age']+' actual source age owns contact')
        check(w['clock']==effect[0]*castle.ROUTINES[w['id']]['duration'] and physical['station']==metric['station'],w['id']+' exact effect time and station')
        check(castle.reach_distance(root,physical['target'],metric['grip'],metric['scale'])<=3,w['source_age']+' age-specific grip bounded at '+str(index))
        check(castle.supported(p,p.state['plan'],root,physical['center']),w['source_age']+' actual age feet supported at contact')
        trace.append(dict(age=w['source_age'],score=w['id'],event=index,clock=w['clock'],root=root,station=physical['station'],target=physical['target'],grip=metric['grip'],scale=metric['scale'],feet=metric['feet'],events=list(w['events'])))
    castle.apply=observe_apply
    outcomes=[]
    for age in castle.CONTACT_METRICS:
        for score in sorted(castle.PHYSICAL_SCORES):
            placement=(9,6) if age=='hatchling' else (9,7)
            plan,w,obj=reset(score,age,placement=placement)
            check(w['physical']['source_age']==age and not w['paired'],age+' '+score+' explicitly solo native binding')
            capture(age+' '+score+' approach')
            for _ in range(5):step(move=False)
            check(not w['events'] and w['clock']==0,age+' no walking grants no contact')
            until(lambda:w['physical']['phase']=='exit',age+' '+score+' exit');capture(age+' '+score+' exit');finish()
            check(w['events']==list(range(len(castle.ROUTINES[score]['effects']))) and obj['uses']==1 and not obj['carnival_company'],age+' '+score+' completes once without invented assistant')
            outcomes.append(dict(age=age,score=score,placement=placement,result='direct',events=w['events']))
    # Geometric failure of a future station must preserve the first mechanical state.
    for score in ('castle_door_open','castle_hose_stow'):
        plan,w,obj=reset(score,'hatchling',placement=(9,7),expect=False)
        check(plan is None and p.state['plan'] is None and obj['castle']['latch']==1 and obj['castle']['motor']=='on' and obj['castle']['targets']['door']==0 and obj['castle']['targets']['hose']==0 and obj['uses']==0 and not obj['carnival_routines'],'hatchling '+score+' unreachable site defers before any unlatch/shutdown/contact')
        outcomes.append(dict(age='hatchling',score=score,placement=[9,7],result='deferred',events=[]))
    for age in ('egg','unknown_age',None):
        plan,w,obj=reset('castle_start',age,expect=False)
        check(p.state['plan'] is None and obj['uses']==0 and not obj['carnival_routines'],str(age)+' cannot silently inherit an adult operator')
    plan,w,obj=reset('castle_start','teen');check(w['source_age']=='juvenile' and w['physical']['source_age']=='juvenile','teen explicitly canonicalizes to juvenile');finish()
    # Growth after a consumed effect retains materials, but never earns completion.
    plan,w,obj=reset('castle_hose_stow','duckling');until(lambda:w['events']==[0],'growth after shutdown')
    g.duck.growth_stage='juvenile';step()
    check(p.state['plan'] is None and obj['castle']['motor']=='off' and w['events']==[0] and obj['uses']==0,'growth interrupts old geometry and preserves actual shutdown without credit')
    # Restoring a valid saved reservation against another actual age must fail closed.
    plan,w,obj=reset('castle_door_open','elder');until(lambda:w['events']==[0],'save before growth');saved=json.loads(json.dumps(p.save()));old=p
    g.duck.growth_stage='adult';p=LivingPond(saved);g.living_pond=p;p.attach(g,offline=False)
    check(p.state['plan']['carnival_work'].get('interrupted'),'restore refuses saved source age mismatch');old.minds.close()
    castle.apply=original_apply
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
    (out/'castle-age-frames.json').write_text(json.dumps(frames))
    result=dict(result='PASS',checks=len(checks),frames=len(frames),trace=trace,outcomes=outcomes,limitations=['egg caregiver scene not adopted','no assistance or alternative contact poses','three controls only'])
    (out/'castle-age-native.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ('trace','outcomes','limitations')}))
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
