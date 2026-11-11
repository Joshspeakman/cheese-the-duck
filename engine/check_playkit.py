"""Real plaything ownership, native clocks, contacts, weather and save/reload."""
import os,sys,tempfile,json,copy,subprocess
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-playkit-');os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,playkit as k
from engine.scene import snapshot
from world.habitat import PlacedItem
from world.atmosphere import Weather,WeatherType,Season
from audio.sound import sound_engine
sys.stdout=host.WIRE;checks=[];frames=[]
def check(ok,label):
    assert ok,label
    checks.append(label)
payload=[dict(id=id,elapsed=s['duration']*i/100,start={key:.37 for key in k.CONTROLS}) for id,s in k.ROUTINES.items() for i in range(101)]
script="import {playkitPose,PLAYKIT_CONTROLS} from './engine/client/playkit-routines.mjs';let s='';for await(const c of process.stdin)s+=c;console.log(JSON.stringify(JSON.parse(s).map(w=>Object.fromEntries(Object.keys(PLAYKIT_CONTROLS).map(k=>[k,playkitPose(w)[k]])))))"
render=json.loads(subprocess.check_output(['node','--input-type=module','-e',script],input=json.dumps(payload).encode(),cwd=ROOT))
check(all(all(abs(a[key]-v)<1e-9 for key,v in k.controls(w).items()) for a,w in zip(render,payload)),str(len(payload))+' native/renderer control samples agree')
bad={'playkit':{'power':float('nan'),'phase':float('inf'),'bubbles':[None,{'age':-5,'size':100}], 'pushes':1e20}};k.state('bubble_machine',bad)
check(bad['playkit']['power']==0 and bad['playkit']['phase']==0 and bad['playkit']['pushes']==9999 and len(bad['playkit']['bubbles'])==1,'optional corrupt state stays bounded and finite')
t=host.DesktopInput();g=host.DesktopGame(terminal=t,renderer_factory=host.CanvasRenderer);t.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
    g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.renderer._show_talk=False;sound_engine.enabled=False
    g.renderer._viewport_width=132;g.renderer._viewport_height=42;g.renderer._update_camera(132,42)
    p=g.living_pond;p.state['auto']=False;p.minds.model.state['next_social']=1e9
    g.duck.growth_stage='adult';g.duck.needs.energy=95;g.duck.needs.hunger=95;g.duck_store.sync_from_duck(g.duck)
    def weather(kind=WeatherType.SUNNY,hour=12):
        g.day_night.get_current_hour=lambda:hour;g.day_night.get_current_minute=lambda:0;g.atmosphere.current_season=Season.SPRING;g.atmosphere.current_weather=Weather(kind,.5,1,datetime.now().isoformat());p.sync();p.state['ecology'].update(temperature=18,wind=.35)
    weather()
    def own(item,twins=False):
        p.cancel();g.duck.current_action=None;g.behavior_ai.clear_action();g.habitat.owned_items=[];g.habitat.placed_items=[];g.habitat.stored_items=[];g.habitat.stored_placements=[];g.building.structures=[];g.inventory.items=[]
        for room in g.decorations.rooms.values():room.decorations=[]
        if item in ('bubble_wand','tiny_boat'):check(g.inventory.add_item(item),item+' is a real inventory object')
        elif item=='surfboard':g.materials.add_material(item,1)
        else:
            g.habitat.owned_items=[item];g.habitat.placed_items=[PlacedItem(item,6 if twins else 10,6)]
            if twins:g.habitat.placed_items.append(PlacedItem(item,14,6))
        p.sync();p.state['cooldowns']={};p._cache=None
        for obj in [*p.state['instances'].values(),*p.state['objects'].values()]:obj['last_use']=-1000
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=24;pos.y=22
        placed=next((x for x in p.placements if x.item_id==item),None);iid=placed.instance if placed else None
        obj=p.object_state(item,iid);obj['playkit']={};k.state(item,obj);return iid,obj
    def possessions():return copy.deepcopy((g.inventory.to_dict(),g.materials.get_all_materials(),g.habitat.currency,g.treasure.to_dict()))
    def step(capture=False):
        p.state['elapsed']+=.2;pos=g.renderer.duck_pos;pos._state_start_time-=.2;pos.update(.2);p._activity(.2)
        for item,obj,outdoors in __import__('engine.object_history',fromlist=['records']).records(p):k.update(p,item,obj,.2,outdoors,.35)
        if capture:frames.append(snapshot(g,g.renderer))
    def finish(capture=False):
        for n in range(1000):
            if not p.state['plan']:return
            step(capture and n%12==0)
        raise AssertionError('plaything did not finish '+str(p.state['plan']))
    def arrived():
        for _ in range(900):
            step()
            if p.state['plan']['phase']=='act':return
        raise AssertionError('never arrived')
    for item in k.ITEMS:
        iid,obj=own(item);before=possessions();initial=copy.deepcopy(obj);ok,msg=p.start('item',item,instance=iid);check(ok,item+' starts through real ownership: '+msg);plan=p.state['plan']
        p._activity(.2);check(plan['playkit_work']['elapsed']==0,item+' waits for preparation/arrival');finish(True)
        check(plan['playkit_work']['done'] and obj['uses']==initial['uses']+1,item+' completes one original use');check(possessions()==before,item+' does not invent or consume inventory');saved=copy.deepcopy(obj);k.complete(p,plan);check(saved==obj,item+' completion cannot repeat')
    for id,s in k.ROUTINES.items():
        weather();item=next(i for i,b in k.ITEMS.items() if b['type']==s['type']);iid,obj=own(item);before=obj['uses'];check(k.request(p,item,id,iid)[0],id+' can be chosen explicitly');plan=p.state['plan'];finish(True)
        check(plan['playkit_work']['done'] and obj['uses']==before+1 and obj['playkit_routines'].get(id),id+' completes through the native clock')
    # Switch contact, separate copies, interruption and facts are actual gameplay.
    iid,obj=own('bubble_machine',True);other=p.object_state('bubble_machine',g.habitat.placed_items[1].instance_id);uses=obj['uses'];k.request(p,'bubble_machine','bubbler_start',iid);plan=p.state['plan'];arrived()
    while obj['playkit']['power']<.6:step()
    check(other['playkit']['power']==0 and obj['playkit']['power']>.5,'only selected machine powers up')
    frozen=copy.deepcopy(obj);plan['paused']=True;p._activity(30);check(obj==frozen,'pause freezes the contact work');p.cancel();check(obj['uses']==uses and obj['playkit']['power']>.5,'cancel keeps the switch position without an item-use reward')
    for _ in range(80):step()
    check(0<len(obj['playkit']['bubbles'])<=12 and obj['playkit']['bubbles_made']>0,'powered machine emits bounded native bubbles independently')
    k.request(p,'bubble_machine','bubbler_stop',iid);finish();count=obj['playkit']['bubbles_made']
    for _ in range(45):step()
    check(obj['playkit']['power']==0 and not obj['playkit']['bubbles'] and obj['playkit']['bubbles_made']==count,'switch off stops emission and remaining bubbles expire')
    weather();iid,obj=own('frisbee');k.request(p,'frisbee','disc_roll',iid);arrived();plan=p.state['plan']
    while obj['playkit']['travel']<.5:step()
    plan['paused']=True;before=copy.deepcopy(obj);g._save_game();g._flush_pending_save();g._load_game();p=g.living_pond;p.sync();weather();loaded=p.object_state('frisbee',iid)
    check(loaded['playkit']==before['playkit'] and p.state['plan']['paused'],'save/reload retains the real disc position and paused clock')
    p.cancel();check(loaded['uses']==before['uses'],'cancel after reload adds no completion reward')
    weather();iid,obj=own('bubble_wand');k.request(p,'bubble_wand','wand_breath');arrived();plan=p.state['plan']
    while obj['playkit']['bubbles_made']<1:step(True)
    facts=k.conversation(p,plan);check(facts['actual_contacts']==['dip','bubble'] and facts['bubbles_visible']==1,'conversation gets only contacts and bubbles that really happened')
    g.inventory.remove_item('bubble_wand');p.sync();p._activity(1);check(not p.state['plan'],'losing a portable toy cancels its use')
    weather();iid,obj=own('yo_yo');k.request(p,'yo_yo','yoyo_drop',iid);arrived();plan=p.state['plan'];uses=obj['uses'];weather(WeatherType.STORMY);step(True)
    check(plan['playkit_work']['id']=='yoyo_pack','storm starts a native wind-down');finish(True);check(obj['uses']==uses,'weather interruption earns no successful play reward')
    weather();iid,obj=own('pinwheel');a=copy.deepcopy(obj);b=copy.deepcopy(obj);k.update(p,'pinwheel',a,1,True,.5)
    for _ in range(10):k.update(p,'pinwheel',b,.1,True,.5)
    check(abs(a['playkit']['speed']-b['playkit']['speed'])<1e-9 and abs(a['playkit']['phase']-b['playkit']['phase'])<1e-9,'wind-driven vanes are invariant to frame size')
    k.update(p,'pinwheel',a,10,False,1);check(a['playkit']['speed']==0,'stored pinwheel never spins')
    for age in ('hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'):
        g.duck.growth_stage=age;weather();iid,obj=own('jump_rope');selected=k.choose(p,'jump_rope',iid)['id'];check(selected==('rope_gentle' if age in ('hatchling','duckling','elder','legendary') else 'rope_steps'),age+' chooses fitting rope play')
    g.duck.growth_stage='adult';weather(hour=23);iid,obj=own('frisbee');check(k.choose(p,'frisbee',iid)['id']=='disc_gentle','night favours quiet observation');weather(WeatherType.RAINY);check(k.choose(p,'frisbee',iid)['id']=='disc_pack','rain selects winding down')
    weather();g.duck.growth_stage='egg';iid,obj=own('jump_rope');check(not p.start('item','jump_rope',instance=iid)[0],'an unhatched egg cannot skip');g.duck.growth_stage='adult'
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
    (out/'playkit-frames.json').write_text(json.dumps(frames));(out/'playkit-native.json').write_text(json.dumps(dict(result='PASS',checks=checks,frames=len(frames),cores=len(k.ROUTINES)),indent=2));print(json.dumps(dict(result='PASS',checks=len(checks),frames=len(frames),cores=len(k.ROUTINES))))
    if '--serve' in sys.argv:
        weather();item='bubble_machine';iid,obj=own(item,True)
        def emit():
            p._cache=None;copies=[a.instance for a in p.placements if a.item_id==item]
            print(json.dumps(dict(type='physical_frame',frame=dict(scene=snapshot(g,g.renderer),copies=copies,item=item))),flush=True)
        emit()
        for line in sys.stdin:
            command=json.loads(line)
            if command.get('type')=='quit':break
            if command.get('type')=='test_fixture':item=command['item'];weather();iid,obj=own(item,True)
            elif command.get('type')=='test_advance':finish()
            elif command.get('type')=='pond':p.command(command);p.sync()
            emit()
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
