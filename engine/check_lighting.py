"""Real light controls, copy identity, weather, native arrival and save lifecycle."""
import os,sys,tempfile,json,copy,subprocess,math
from pathlib import Path
from types import SimpleNamespace
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-lighting-')
os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,pond_lighting as lights
from engine.item_profiles import ITEMS
from engine.scene import snapshot
from world.habitat import PlacedItem
from world.atmosphere import Weather,WeatherType,Season
from audio.sound import sound_engine
sys.stdout=host.WIRE;checks=[];frames=[]
def check(ok,label):
    assert ok,label
    checks.append(label)
contexts=[(h,s,w,m) for h in (3,6,12,18,22) for s in ('spring','winter') for w in (False,True) for m in lights.MODES]
payload=[dict(id=k,hour=h,season=s,weather='rain' if w else 'sunny',intensity=.7,mode=m) for k in lights.LIGHTS for h,s,w,m in contexts]
script="import {lightOutput} from './engine/client/lighting-state.mjs';let s='';for await(const c of process.stdin)s+=c;console.log(JSON.stringify(JSON.parse(s).map(c=>lightOutput(c.id,{lighting:{mode:c.mode}},c))))"
render=json.loads(subprocess.check_output(['node','--input-type=module','-e',script],input=json.dumps(payload).encode(),cwd=ROOT))
native=[lights.output(c['id'],c['mode'],c['hour'],c['season'],c['weather']=='rain',.7) for c in payload]
check(all(abs(a-b)<1e-9 for a,b in zip(render,native)),'1620 native/preview dusk weather season and mode cases agree')
for item in lights.LIGHTS:
    obj={};p=SimpleNamespace(hour=22,season='summer');s=lights.state(item,obj,22,'summer')
    lights.update(p,item,obj,30,True,False,.7);check(0<=s['level']<=1 and s['operating_seconds']>0,item+' operates outdoors at night')
    mode=s['mode'];hours=s['operating_seconds'];lights.update(p,item,obj,300,False)
    check(s['level']<1e-6 and s['mode']==mode and s['operating_seconds']==hours,item+' storage retains mode without accumulating operation')
    check(ITEMS[item]['kind']=='light' and ITEMS[item]['skill']=='observation',item+' native profile uses light behavior')

t=host.DesktopInput();g=host.DesktopGame(terminal=t,renderer_factory=host.CanvasRenderer)
t.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
    g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.renderer._show_talk=False
    g.renderer._viewport_width=132;g.renderer._viewport_height=42;g.renderer._update_camera(132,42);sound_engine.enabled=False
    p=g.living_pond;p.state['auto']=False;p.minds.model.state['next_social']=1e9
    g.building.structures=[]
    for room in g.decorations.rooms.values():room.decorations=[]
    g.duck.growth_stage='adult';g.duck.needs.energy=95;g.duck.needs.hunger=95;g.duck_store.sync_from_duck(g.duck)
    g.day_night.get_current_hour=lambda:12;g.day_night.get_current_minute=lambda:0
    g.atmosphere.current_season=Season.SPRING;g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.5,1,datetime.now().isoformat())
    def place(item,twins=False):
        p.cancel();g.duck.current_action=None;g.behavior_ai.clear_action();g.habitat.owned_items=[item]
        g.habitat.stored_items=[];g.habitat.stored_placements=[];g.habitat.placed_items=[PlacedItem(item,10,6)]
        if twins:g.habitat.placed_items.append(PlacedItem(item,17,6))
        p.sync();p.state['cooldowns']={};p._cache=None
        for obj in p.state['instances'].values():obj['last_use']=-1000
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=36;pos.y=21
        a=g.habitat.placed_items[0];return a,p.object_state(item,a.instance_id)
    def step(capture=False):
        p.state['elapsed']+=.2;pos=g.renderer.duck_pos;pos._state_start_time-=.2;pos.update(.2);p._activity(.2)
        for placed in p.placements:lights.update(p,placed.item_id,p.object_state(placed.item_id,placed.instance),.2,True)
        if capture and len(frames)<200:frames.append(snapshot(g,g.renderer))
    def finish(capture=False):
        for n in range(900):
            if not p.state['plan']:return
            step(capture and n%5==0)
        raise AssertionError('light action did not finish')
    for item,spec in lights.LIGHTS.items():
        a,obj=place(item)
        if spec['control']=='observe':
            check(not lights.request(p,item,'off',a.instance_id)[0],item+' cannot be switched against its nature')
            ok,msg=p.start('item',item,instance=a.instance_id)
        else:ok,msg=lights.request(p,item,'on',a.instance_id)
        check(ok,item+' starts a real activity: '+msg);plan=p.state['plan'];original=copy.deepcopy(obj)
        p._activity(1);check(obj==original and plan['light_work']['elapsed']==0,item+' cannot operate before reaching it')
        finish(item in ('table_lamp','tiki_torch','campfire'))
        check(plan.get('arrived') and plan['light_work']['done'] and obj['uses']==1,item+' arrives acts and completes once')
        if spec['control']!='observe':check(obj['lighting']['mode']=='on' and obj['lighting']['switches']==1,item+' changes the requested switch once')
        old=copy.deepcopy(obj);lights.complete(p,plan);check(obj==old,item+' repeated completion cannot duplicate history')
    a,obj=place('table_lamp',True);b=g.habitat.placed_items[1];other=p.object_state('table_lamp',b.instance_id)
    command=dict(type='pond',action='lighting_mode',target='table_lamp',instance=a.instance_id,text='on')
    bridge="const {pondCommand}=require('./engine/pond-command.cjs');let s='';process.stdin.on('data',c=>s+=c);process.stdin.on('end',()=>console.log(JSON.stringify(pondCommand(JSON.parse(s)))));"
    forwarded=json.loads(subprocess.check_output(['node','-e',bridge],input=json.dumps(command).encode(),cwd=ROOT));p.command(forwarded)
    check(p.state['plan']['instance']==a.instance_id,'production command validator reaches the selected physical copy')
    finish();check(obj['lighting']['mode']=='on' and other['lighting']['mode']=='auto' and other['uses']==0,'changing one light does not operate its twin')
    obj['last_use']=-1000;p.state['cooldowns']={};check(lights.request(p,'table_lamp','off',a.instance_id)[0],'second setting starts')
    p.cancel();check(obj['lighting']['mode']=='on' and obj['uses']==1,'cancelling before contact leaves switch and rewards unchanged')
    check(lights.request(p,'table_lamp','off',a.instance_id)[0],'restart after cancellation')
    plan=p.state['plan']
    for _ in range(700):
        step()
        if plan['light_work']['changed']:break
    check(plan['light_work']['changed'] and not plan['light_work']['done'],'native contact precedes completion')
    before=plan['light_work']['elapsed'];plan['paused']=True;p._activity(10)
    check(plan['light_work']['elapsed']==before,'paused acting clock does not progress')
    p.cancel();check(obj['lighting']['mode']=='off' and obj['uses']==1,'cancelling after real contact keeps the changed switch without completion rewards')
    obj['last_use']=-1000;p.state['cooldowns']={};check(lights.request(p,'table_lamp','on',a.instance_id)[0],'stale-copy test starts')
    g.habitat.placed_items[0]=PlacedItem('table_lamp',a.x,a.y);p.sync();p._activity(.2)
    check(p.state['plan'] is None and obj['lighting']['mode']=='off','replacement at the same coordinates cannot receive the old switch action')
    a,obj=place('table_lamp');lights.request(p,'table_lamp','on',a.instance_id);finish()
    check(g.habitat.store_item('table_lamp',a.instance_id),'operated lamp can be stored');p.sync();p._environment(300,True)
    check(obj['lighting']['mode']=='on' and obj['lighting']['level']<1e-6,'normal environment update powers stored copy down')
    saved=copy.deepcopy(obj['lighting']);g._save_game();g._flush_pending_save();g._load_game();p=g.living_pond;p.sync()
    check(p.object_state('table_lamp',a.instance_id)['lighting']['mode']==saved['mode'],'full game save reload preserves physical light setting')
    # Loading reconstructs the clock; keep this cold/daytime fixture explicit.
    g.day_night.get_current_hour=lambda:12;g.day_night.get_current_minute=lambda:0;p.sync()
    g.duck.growth_stage='egg';a,obj=place('table_lamp');check(not lights.request(p,'table_lamp','on',a.instance_id)[0],'an egg cannot operate controls')
    g.duck.growth_stage='hatchling';a,obj=place('tiki_torch');obj['lighting'].update(mode='auto',level=0,heat=0)
    check(not lights.request(p,'tiki_torch','on',a.instance_id)[0],'hatchling enjoys an open flame without operating it')
    check(p.start('item','tiki_torch',instance=a.instance_id)[0] and p.state['plan']['light_work']['id']=='unlit_inspect','young Cheese inspects a cold torch without pretending it is warm');p.cancel()
    obj['lighting'].update(level=1,heat=.8)
    check(p.start('item','tiki_torch',instance=a.instance_id)[0] and p.state['plan']['light_work']['id']=='warm_wings','young Cheese enjoys warmth when a flame is actually burning');p.cancel()
    g.duck.growth_stage='adult';a,obj=place('table_lamp');lights.request(p,'table_lamp','on',a.instance_id);finish()
    for hour,label in [(12,'day'),(22,'night')]:
        g.day_night.get_current_hour=lambda h=hour:h;p.sync();lights.update(p,'table_lamp',obj,30,True);s=snapshot(g,g.renderer);s['review']=label;frames.append(s)
    p.state['cooldowns']={};obj['last_use']=-1000;lights.request(p,'table_lamp','off',a.instance_id)
    for _ in range(700):
        step()
        if p.state['plan'] and p.state['plan']['light_work']['elapsed']>=4.6:
            s=snapshot(g,g.renderer);s['review']='control';frames.append(s);break
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(exist_ok=True,parents=True)
    (out/'lighting-frames.json').write_text(json.dumps(frames))
    (out/'lighting-native.json').write_text(json.dumps(dict(result='PASS',checks=checks,frames=len(frames)),indent=2))
    print(json.dumps(dict(result='PASS',checks=len(checks),frames=len(frames))))
    if '--serve' in sys.argv:
        g.duck.growth_stage='adult';g.day_night.get_current_hour=lambda:12
        a,obj=place('table_lamp',True);copies=[x.instance_id for x in g.habitat.placed_items]
        for iid in copies:p.object_state('table_lamp',iid)['lighting'].update(mode='auto',level=0,heat=0)
        def emit():
            p._cache=None
            print(json.dumps(dict(type='physical_frame',frame=dict(scene=snapshot(g,g.renderer),copies=copies,item='table_lamp'))),flush=True)
        emit()
        for line in sys.stdin:
            command=json.loads(line)
            if command.get('type')=='quit':break
            if command.get('type')=='test_advance':
                if command.get('until')=='contact':
                    for _ in range(800):
                        step()
                        if p.state['plan'] and p.state['plan']['light_work']['elapsed']>=5.4:break
                else:finish()
            elif command.get('type')=='pond':
                p.state['cooldowns']={}
                for iid in copies:p.object_state('table_lamp',iid)['last_use']=-1000
                p.command(command);p.sync()
            emit()
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
