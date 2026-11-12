"""Adult solo blower pilot: actual native arrival before mechanical contact.

This is a bounded implementation regression, not 48-sequence certification.
Only disposable saves are used. Frames are actual scene.snapshot output.
"""
import os,sys,tempfile,json,copy,random
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-castle-physical-')
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
    def reset(age='adult',root=(48,24),start=True):
        p.cancel();g.duck.current_action=None;g.behavior_ai.clear_action();g.duck.growth_stage=age
        for k in ('energy','hunger','fun','cleanliness','social'):setattr(g.duck.needs,k,95)
        g.duck_store.sync_from_duck(g.duck);g.friends.current_visit=None;g.atmosphere.current_visitor=None;p.state['story']=None
        g.habitat.owned_items=['bounce_house'];g.habitat.placed_items=[PlacedItem('bounce_house',9,7)];g.habitat.stored_items=[];g.habitat.stored_placements=[];g.building.structures=[]
        for room in g.decorations.rooms.values():room.decorations=[]
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x,pos.y=root
        p.sync();p.weather_type='sunny';p.season='spring';p.hour=12;p.state['ecology'].update(wind=.2,temperature=18);p.state['cooldowns']={}
        iid=next(a.instance for a in p.placements if a.item_id=='bounce_house');obj=p.object_state('bounce_house',iid)
        obj.update(last_use=-1000,uses=0,dirt=0,wetness=0,condition=1,excursion={},castle={},carnival_routines={},carnival_company={});excursions.state('bounce_house',obj);castle.state(obj).update(motor='off',power_hold=True)
        if not start:return iid,obj
        if not frames:capture('before')
        ok,message=carnival.request(p,'bounce_house','castle_start',iid);check(ok,'production carnival.request starts '+age+' pilot: '+message)
        plan=p.state['plan'];return plan,plan['carnival_work'],obj
    def capture(case):
        s=snapshot(g,g.renderer);s['_physicalCase']=case;frames.append(s)
    def step(move=True,capture_case=None,dt=.2):
        p.state['elapsed']+=dt;pos=g.renderer.duck_pos
        if move:pos._state_start_time-=dt;pos.update(dt)
        p._activity(dt)
        if p.state['plan']:
            plan=p.state['plan'];w=plan['carnival_work'];obj=p.object_state('bounce_house',plan)
            excursions.update('bounce_house',obj,dt,True,p.weather_type,.2,p.hour,reserved=carnival.owns(p,'bounce_house',obj))
            if capture_case:
                capture(capture_case);trace.append(dict(case=capture_case,objectInstance=plan['instance'],actor='cheese',sequenceId=w['id'],root=[pos.x,pos.y],physical=carnival.view(p,plan).get('physical'),events=list(w['events']),clock=w['clock'],motor=obj['castle']['motor']))
    plan,w,obj=reset();check(castle.physical_active(plan),'adult pilot has a validated physical reservation: '+str(w))
    check(w['physical']['center']==[59.4,24.5],'physical control uses exact placement center, not rounded navigation identity')
    expected=castle.control_world(w['physical']['center']);check(w['physical']['target']==expected,'control target comes from shared geometry cell center')
    check(w['physical']['stance']==list(map(round,w['physical']['stance'])),'walking stance uses reachable integer coordinates')
    initial=[g.renderer.duck_pos.x,g.renderer.duck_pos.y];capture('approach')
    for _ in range(50):step(move=False)
    check(w['clock']==0 and not w['events'] and obj['castle']['motor']=='off','no walking means no service clock or motor contact')
    positions=set();seen=set()
    for i in range(800):
        if not p.state['plan']:break
        step(capture_case='successful' if i%3==0 else None);positions.add((g.renderer.duck_pos.x,g.renderer.duck_pos.y))
        if w.get('physical'):seen.add(w['physical']['phase'])
        if w['events'] and 'contact' not in seen:capture('contact');seen.add('contact')
    capture('after')
    check(w.get('done') and not w.get('interrupted') and p.state['plan'] is None,'pilot finishes only after actual exterior exit: '+str(w))
    check(len(positions)>8 and {'approach','hold','exit','contact'}<=seen,'real intermediate native roots cover approach, hold, contact and exit')
    check(w['events']==[0] and obj['castle']['motor']=='on' and obj['uses']==1,'exactly one reached press turns on the real motor and completes one use')
    check(obj['carnival_routines'].get('castle_start')==1,'completed physical work records one original routine')
    for row in trace:
        ph=row['physical'];check(ph['root']==row['root'],'snapshot record equals actual native root')
        if row['events']:check(castle.reach_distance(ph['stance'],ph['target'])<=3,'consumed contact has a bounded validated stance')
    # Rendering may update the actor between native work ticks. Snapshot reads
    # that actual root, and never advances work or overwrites saved controller data.
    plan,w,obj=reset();before=copy.deepcopy(w);g.renderer.duck_pos.update(.3)
    view=carnival.view(p,plan);native=[g.renderer.duck_pos.x,g.renderer.duck_pos.y]
    check(view['physical']['root']==native and w==before,'read-only view exposes actual animator root between work ticks')
    p._cache=None;frame=snapshot(g,g.renderer)
    check(frame['living']['plan']['carnival_work']['physical']['root']==[frame['duck']['x'],frame['duck']['y']],'whole scene snapshot has one native root')
    for reason in ('paused','direct_care','unavailable'):
        plan,w,obj=reset();pos=g.renderer.duck_pos
        if reason=='paused':plan['paused']=True
        elif reason=='direct_care':g.duck.current_action='feed'
        else:g.renderer._show_talk=True
        p._activity(.2);root=[pos.x,pos.y];pos.update(.2)
        check(not pos._is_directed_movement and [pos.x,pos.y]==root and w['clock']==0,reason+' stops actual travel as well as work clock')
        plan['paused']=False;g.duck.current_action=None;g.renderer._show_talk=False;p._activity(.2)
        check(pos._is_directed_movement,reason+' resume reissues native route without teleport')
    plan,w,obj=reset()
    for _ in range(470):
        step(move=False)
        if p.state['plan'] is None:break
    check(w.get('interrupted') and p.state['plan'] is None and not w['events'],'unmoving actor times out without contact')
    # A request with no exterior dry route fails before leaving an active plan.
    iid,obj=reset(root=(48,18),start=False);ok,message=carnival.request(p,'bounce_house','castle_start',iid)
    check(not ok and p.state['plan'] is None and obj['castle']['motor']=='off','initial route through own castle body is refused')
    iid,obj=reset(start=False);g.habitat.placed_items[0].y=10;p.sync()
    ok,message=carnival.request(p,'bounce_house','castle_start',iid)
    check(not ok and p.state['plan'] is None and obj['castle']['motor']=='off','water-supported blower stance is refused')
    # Deliberate input cancels before contact, retaining off state and no credit.
    plan,w,obj=reset()
    for _ in range(8):step()
    p.cancel();check(obj['castle']['motor']=='off' and not w['events'] and obj['uses']==0,'pre-contact cancellation has no motor or use reward')
    # Complete only the press, then cancel; physical work persists without credit.
    plan,w,obj=reset()
    for _ in range(600):
        step()
        if w['events']:break
    check(w['events']==[0],'post-contact fixture reaches native press')
    p.cancel();check(obj['castle']['motor']=='on' and obj['uses']==0,'post-contact cancellation preserves real motor effect without completion credit')
    # Block the approved future stance with another physical copy after request.
    plan,w,obj=reset();stance=w['physical']['stance'];g.habitat.owned_items.append('rock');g.habitat.placed_items.append(PlacedItem('rock',stance[0]*20/132,stance[1]*12/42))
    for _ in range(500):
        step()
        if p.state['plan'] is None:break
    check(w.get('interrupted') and not w['events'] and obj['uses']==0 and obj['castle']['motor']=='off','new obstacle prevents contact and shared completion')
    # Malformed physical state is cancelled, never routed to elapsed-only work.
    plan,w,obj=reset();w['physical']['target']=[float('nan'),0];step()
    check(p.state['plan'] is None and not w['events'] and obj['castle']['motor']=='off','malformed physical reservation fails closed')
    # Saved contact remains consumed; actual loaded root is re-approached.
    plan,w,obj=reset()
    for _ in range(600):
        step()
        if w['events']:break
    saved=json.loads(json.dumps(p.save()));saved_pos=[g.renderer.duck_pos.x,g.renderer.duck_pos.y]
    restored=LivingPond(saved)
    try:
        restored.attach(g,offline=False);rw=restored.state['plan']['carnival_work'];ro=restored.object_state('bounce_house',restored.state['plan'])
        check([g.renderer.duck_pos.x,g.renderer.duck_pos.y]==saved_pos and restored.state['plan']['paused'],'reload pauses without teleporting native actor')
        check(rw['events']==[0] and ro['castle']['motor']=='on' and ro['uses']==0,'reload preserves consumed physical effect without completed credit')
        check(rw['physical']['contact_ready'] is False and rw['physical']['phase']=='approach','restored work must reacquire actual arrival and support')
        original=p;p=restored;g.living_pond=restored
        p.command({'action':'resume'})
        for _ in range(900):
            step()
            if p.state['plan'] is None:break
        check(p.state['plan'] is None and rw['events']==[0] and ro['uses']==1 and ro['carnival_routines'].get('castle_start')==1,'resumed native work reacquires stance and completes once without replaying consumed contact')
        p=original;g.living_pond=original
    finally:restored.minds.close();p.attach(g,offline=False)
    forged=copy.deepcopy(saved);forged['plan']['carnival_work']['physical']['target'][0]+=.1
    restored=LivingPond(forged)
    try:
        restored.attach(g,offline=False)
        check(restored.state['plan']['carnival_work'].get('interrupted'),'finite forged saved target cannot invent a switch contact')
    finally:restored.minds.close();p.attach(g,offline=False)
    plan,w,obj=reset(age='duckling');check(not w.get('physical_pilot') and not castle.physical_active(plan),'unsupported age is explicitly legacy and receives no native-pilot claim')
    for bad in (None,{},dict(target='bounce_house',carnival_work=None),dict(target='bounce_house',carnival_work=[]),dict(target='bounce_house',carnival_work={'id':[]})):
        check(not castle.physical_active(bad),'malformed or unrelated plan is safe for generic hook')
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
    (out/'castle-physical-frames.json').write_text(json.dumps(frames))
    result=dict(result='PASS',checks=len(checks),frames=len(frames),pilot='adult-solo-castle_start',trace=trace,limitations=['other ages and controls remain legacy','three-cell bounded pilot reach is not anatomical certification','save restores paused re-approach, not exact pose'])
    (out/'castle-physical-native.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ('trace','limitations')}))
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
