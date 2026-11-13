"""Native air controls with actual movement, mechanism response and gauge sightlines.

Disposable saves only; real production snapshots and an observed contact trace.
"""
import os,sys,tempfile,json,copy,random,hashlib
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
    metrics_sha=hashlib.sha256((ROOT/'engine/client/animation/castle-air-metrics.json').read_bytes()).hexdigest()
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
    cases=[];case_id=None
    old_capture=capture
    def capture(case,event=None):
        old_capture(case,event)
        frames[-1]['_airMatrixCase']=case_id
    for age in castle.CONTACT_METRICS:
        for score in sorted(set(sys.argv[sys.argv.index('--scores')+1].split(',')) if '--scores' in sys.argv else castle.AIR_SCORES):
            case_id='solo/'+age+'/cheese/cheese/'+score
            case=dict(geometry_sha256=hashlib.sha256(json.dumps(dict(events=air.DATA['ages'][age]['routines'][score],travel=air.DATA['ages'][age]['travel']),sort_keys=True,separators=(',',':')).encode()).hexdigest(),id=case_id,mode='solo',age=age,cast='cheese',adapter='cheese',score=score,attempts=[])
            for placement in ((9,6),(9,5),(8,5),(10,5)):
                iid,obj=reset(score,age,root=(44,26),start=False,placement=placement)
                before=copy.deepcopy(obj['castle'])
                ok,reason=carnival.request(p,'bounce_house',score,iid)
                case['attempts'].append(dict(placement=list(placement),accepted=ok,reason=reason))
                if not ok:
                    check(obj['castle']==before and not obj['carnival_routines'] and obj['uses']==0,'refused acquisition has no material event or reward')
                    continue
                plan=p.state['plan'];w=plan['carnival_work'];case['placement']=list(placement);case['center']=list(w['physical']['center']);case['status']='supported'
                capture('accepted approach')
                until(lambda:w['physical']['phase']=='exit','matrix exit '+case_id,3000)
                capture('actual exit route')
                until(lambda:p.state['plan'] is None,'matrix completion '+case_id,3000)
                check(w.get('recorded') and not w.get('interrupted'),'actual matrix completion '+case_id+' '+str(w.get('physical_error')))
                check(w['events']==list(range(len(castle.ROUTINES[score]['effects']))),'all authored matrix effects')
                case['events']=list(w['events']);case['inspection']=w.get('inspection');case['material']=copy.deepcopy(obj['castle'])
                break
            else:case.update(status='refused',reason=case['attempts'][-1]['reason'])
            cases.append(case)
        print(json.dumps(dict(progress=age,cases=len(cases),supported=sum(c['status']=='supported' for c in cases))),flush=True)
    castle.apply=original_apply
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
    prefix='castle-air-ages-matrix'+('-'+sys.argv[sys.argv.index('--scores')+1].replace(',','-') if '--scores' in sys.argv else '')
    payload=json.dumps(frames);(out/(prefix+'-frames.json')).write_text(payload)
    result=dict(schema_version=1,result='PASS',scope='Eight Cheese ages, eight air atomics; actual native solo movers and effects',checks=len(checks),frames=len(frames),frames_file=prefix+'-frames.json',metrics_sha256=metrics_sha,frames_sha256=hashlib.sha256(payload.encode()).hexdigest(),cases=cases)
    (out/(prefix+'-manifest.json')).write_text(json.dumps(result,indent=2))
    print(json.dumps(dict(result='PASS',checks=len(checks),frames=len(frames),cases=len(cases),supported=sum(c['status']=='supported' for c in cases),refused=sum(c['status']=='refused' for c in cases))))
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
