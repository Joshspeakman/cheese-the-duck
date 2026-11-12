"""Native air controls with actual movement, mechanism response and gauge sightlines.

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
        obj.update(last_use=-1000,uses=0,dirt=0,wetness=0,condition=1,excursion={},castle={},carnival_routines={},carnival_company={});excursions.state('bounce_house',obj);castle.state(obj).update(motor='off' if score=='castle_start' else 'on',power_hold=False,latch=1,door=0,hose=1 if score=='castle_hose_straight' else 0,kink=.7 if score=='castle_hose_straight' else 0,vent=1 if score=='castle_vent_close' else 0,dust=.8 if score=='castle_grill_clean' else 0)
        for field in ('vent','hose','kink'):obj['castle']['targets'][field]=obj['castle'][field]
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
        if p.state['plan']:
            plan=p.state['plan'];w=plan['carnival_work'];obj=p.object_state('bounce_house',plan)
            excursions.update('bounce_house',obj,dt,True,p.weather_type,.2,p.hour,reserved=carnival.owns(p,'bounce_house',obj))
            p._activity(dt)
            if capture_case:
                capture(capture_case);trace.append(dict(case=capture_case,objectInstance=plan['instance'],actor='cheese',sequenceId=w['id'],root=[pos.x,pos.y],physical=carnival.view(p,plan).get('physical'),events=list(w['events']),clock=w['clock'],motor=obj['castle']['motor']))
    def until(predicate,label,limit=1600):
        for _ in range(limit):
            if predicate():return
            step()
        raise AssertionError(label+': '+str(p.state.get('plan')))
    def finish():until(lambda:p.state['plan'] is None,'completion')
    from engine import castle_air as air
    original_apply=castle.apply
    def observed_apply(obj,w,index,effect):
        original_apply(obj,w,index,effect)
        ph=w['physical'];metric=castle.effect_metrics(w)[index]
        check(w['clock']==effect[0]*castle.ROUTINES[w['id']]['duration'],'effect uses exact authored pose clock')
        if metric['kind']=='observation':
            check(ph.get('observation_ready') and not ph['contact_ready'],'reading has eye authority without mechanical contact')
            check(air.sightline(p,p.state['plan'],[g.renderer.duck_pos.x,g.renderer.duck_pos.y],g.renderer.duck_pos.facing_right,metric,ph['center']),'actual eyes see actual needle')
        else:
            check(ph['contact_ready'] and castle.reach_distance([g.renderer.duck_pos.x,g.renderer.duck_pos.y],ph['target'],metric['grip'],metric['scale'])<=3,'real authored grip is bounded')
        capture(w['id']+' effect '+str(index),index)
    castle.apply=observed_apply
    outcomes=[]
    for score in sorted(set(os.environ.get('AIR_SCORES',','.join(castle.AIR_SCORES)).split(','))):
        plan,w,obj=reset(score,placement=(9,6))
        until(lambda:p.state['plan'] is None,'air completion '+score,2600)
        check(not w.get('interrupted'),score+' no interruption '+str(w.get('physical_error')))
        check(w['events']==list(range(len(castle.ROUTINES[score]['effects']))),score+' every actual event')
        check(w.get('recorded'),score+' completed receipt')
        outcomes.append(dict(id=score,events=w['events'],inspection=w.get('inspection'),material=obj['castle']))
    castle.apply=original_apply
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
    (out/'castle-air-frames.json').write_text(json.dumps(frames))
    (out/'castle-air-native.json').write_text(json.dumps(dict(result='PASS',checks=len(checks),outcomes=outcomes),indent=2))
    print(json.dumps(dict(result='PASS',checks=len(checks),frames=len(frames),scores=len(outcomes))))
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
