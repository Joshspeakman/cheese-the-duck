"""Ground material contact, interruption, inventory, context and full-save checks."""
import os,sys,tempfile,json,copy,subprocess
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-ground-');os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,groundworks as k
from engine.scene import snapshot
from world.habitat import PlacedItem
from world.building import Structure,StructureStatus
from world.atmosphere import Weather,WeatherType,Season
from audio.sound import sound_engine
sys.stdout=host.WIRE;checks=[];frames=[]
def check(ok,label):
    assert ok,label
    checks.append(label)
payload=[dict(id=id,elapsed=spec['duration']*i/100,start={**k.CONTROLS,'u':.37}) for id,spec in k.ROUTINES.items() for i in range(101)]
script="import {groundPose,GROUND_CONTROLS} from './engine/client/ground-routines.mjs';let s='';for await(const c of process.stdin)s+=c;console.log(JSON.stringify(JSON.parse(s).map(w=>Object.fromEntries(Object.keys(GROUND_CONTROLS).map(k=>[k,groundPose(w)[k]])))))"
render=json.loads(subprocess.check_output(['node','--input-type=module','-e',script],input=json.dumps(payload).encode(),cwd=ROOT))
check(all(all(abs(a[key]-v)<1e-9 for key,v in k.controls(w).items()) for a,w in zip(render,payload)),str(len(payload))+' native and renderer mechanical samples agree')
bad={'ground':{'powder':float('nan'),'phase':float('inf'),'frost':-1,'studies':999999,'tracks':[{},dict(u=.5,v=.3)]}}
check(k.state('sand_floor',bad)['powder']==.75 and bad['ground']['frost']==0 and bad['ground']['studies']==9999 and len(bad['ground']['tracks'])==1,'corrupt optional ground state is bounded')
t=host.DesktopInput();g=host.DesktopGame(terminal=t,renderer_factory=host.CanvasRenderer);t.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
    g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.renderer._show_talk=False;sound_engine.enabled=False
    g.renderer._viewport_width=132;g.renderer._viewport_height=42;g.renderer._update_camera(132,42)
    p=g.living_pond;p.state['auto']=False;p.minds.model.state['next_social']=1e9
    g.duck.growth_stage='adult';g.duck.needs.energy=95;g.duck.needs.hunger=95;g.duck_store.sync_from_duck(g.duck)
    def weather(kind=WeatherType.SUNNY,hour=12,wind=.35,season=Season.SPRING):
        g.day_night.get_current_hour=lambda:hour;g.day_night.get_current_minute=lambda:0
        g.atmosphere.current_season=season;g.atmosphere.current_weather=Weather(kind,.5,1,datetime.now().isoformat());p.sync()
        p.state['ecology'].update(temperature=18,wind=wind)
    weather()
    def own(item,twins=False):
        p.cancel();g.duck.current_action=None;g.behavior_ai.clear_action();g.habitat.owned_items=[];g.habitat.placed_items=[];g.habitat.stored_items=[];g.habitat.stored_placements=[];g.building.structures=[]
        for room in g.decorations.rooms.values():room.decorations=[]
        if item=='stone_path':g.building.structures=[Structure(item,(8,6),status=StructureStatus.COMPLETE)]
        elif k.ITEMS[item]['portable']:g.materials.add_material(item,1)
        else:
            g.habitat.owned_items=[item];g.habitat.placed_items=[PlacedItem(item,6 if twins else 10,6)]
            if twins:g.habitat.placed_items.append(PlacedItem(item,14,6))
        p.sync();p.state['cooldowns']={};p._cache=None
        for obj in [*p.state['instances'].values(),*p.state['objects'].values()]:obj['last_use']=-1000
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=15;pos.y=20
        placed=next((x for x in p.placements if x.item_id==item),None);iid=placed.instance if placed else None
        return iid,p.object_state(item,iid)
    def possessions():return copy.deepcopy((g.inventory.to_dict(),g.materials.get_all_materials(),g.habitat.currency,g.treasure.to_dict()))
    def step(capture=False):
        p.state['elapsed']+=.2;pos=g.renderer.duck_pos;pos._state_start_time-=.2;pos.update(.2);p._activity(.2)
        if capture:frames.append(snapshot(g,g.renderer))
    def finish(capture=False):
        for n in range(900):
            if not p.state['plan']:return
            step(capture and n%15==0)
        raise AssertionError('ground action did not finish '+str(p.state['plan']))
    def arrived():
        for _ in range(900):
            step()
            if p.state['plan']['phase']=='act':return
        raise AssertionError('never arrived')
    def facts():
        p.minds.sync();messages=p.minds.prompt('cheese','What are you working on?')
        return json.loads(messages[0]['content'].split('CHARACTER AND VERIFIED GAME STATE:\n',1)[1])
    for item in k.ITEMS:
        iid,obj=own(item);before=possessions();initial=copy.deepcopy(obj);ok,msg=p.start('item',item,instance=iid)
        check(ok,item+' starts through real ownership: '+msg);plan=p.state['plan']
        if iid:p._activity(1);check(obj==initial and plan['ground_work']['elapsed']==0,item+' contact waits for actual arrival')
        finish(True)
        check(plan['ground_work']['done'] and obj['uses']==initial['uses']+1,item+' completes exactly one use')
        check(possessions()==before,item+' never consumes or fabricates inventory')
        saved=copy.deepcopy(obj);k.complete(p,plan);check(saved==obj,item+' repeated completion cannot duplicate credit')
    for key,spec in k.ROUTINES.items():
        weather();item=next(i for i,s in k.ITEMS.items() if s['type'] in spec['types']);iid,obj=own(item)
        check(p.start('item',item,instance=iid)[0],key+' accepts the owned item');plan=p.state['plan'];work=plan['ground_work'];work.update(id=key,label=spec['label'])
        before=obj['uses'];finish(True)
        check(not work.get('interrupted') and obj['uses']==before+1 and obj.get('ground_routines',{}).get(key),key+' completes through the actual native clock')
    weather();iid,obj=own('marble_tiles');obj['dirt']=0;obj['ground']['frost']=0
    for age in ('hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'):
        g.duck.growth_stage=age;weather(hour=23)
        expected='young_footing' if age in ('hatchling','duckling') else 'elder_footing' if age in ('elder','legendary') else 'night_surface'
        check(k.choose(p,'marble_tiles',iid)['id']==expected,age+' chooses age-appropriate night footing')
    g.duck.growth_stage='egg';check(not p.start('item','marble_tiles',instance=iid)[0],'egg cannot walk or operate a surface');g.duck.growth_stage='adult';weather()
    for item,expected in [('stepping_stones','stone_cross'),('stone_path','winding_walk')]:
        iid,obj=own(item);g.duck.growth_stage='hatchling';check(k.choose(p,item,iid)['id']==expected,'young duck uses the actual '+item+' footholds')
    g.duck.growth_stage='adult';iid,obj=own('marble_tiles',True);obj['dirt']=.8;obj['ground']['frost']=0
    other=p.object_state('marble_tiles',g.habitat.placed_items[1].instance_id);other['dirt']=.8
    check(p.start('item','marble_tiles',instance=iid)[0],'choose dirty copy');plan=p.state['plan'];uses=obj['uses'];arrived()
    while not plan['ground_work']['events']:step()
    check(abs(obj['dirt']-.62)<1e-9 and other['dirt']==.8,'contact cleans only the selected marble copy')
    current=copy.deepcopy(obj);f=facts();check(f['ground_work']['material']=='marble' and obj==current,'speech receives actual nearby material without changing it')
    plan['paused']=True;clock=plan['ground_work']['elapsed'];p._activity(30);check(obj==current and plan['ground_work']['elapsed']==clock,'paused contact cannot advance')
    g._save_game();g._flush_pending_save();g._load_game();p=g.living_pond;p.sync();weather();obj=p.object_state('marble_tiles',iid)
    check(p.state['plan']['paused'] and obj['ground']==current['ground'] and obj['dirt']==current['dirt'],'full save reload keeps physical state and pauses work')
    p.cancel();check(obj['uses']==uses and obj['dirt']==current['dirt'],'cancel preserves real contact without completion credit')
    iid,obj=own('sand_floor');obj['ground'].update(tracks=[],furrows=[],frost=0);obj['uses']=0
    p.start('item','sand_floor',instance=iid);plan=p.state['plan'];arrived()
    while not plan['ground_work']['events']:step()
    check(len(obj['ground']['furrows'])==1,'first rake stroke creates exactly one saved furrow')
    p.cancel();check(len(obj['ground']['furrows'])==1,'cancel retains the line already drawn')
    p.state['cooldowns']={};obj['last_use']=-1000;obj['uses']=1;p.start('item','sand_floor',instance=iid);finish(True)
    check(len(obj['ground']['tracks'])==4,'four steps create four physical sand footprints')
    obj['last_use']=-1000;p.state['cooldowns']={};obj['uses']=2;p.start('item','sand_floor',instance=iid);finish()
    check(not obj['ground']['tracks'] and not obj['ground']['furrows'],'smoothing actually removes the old marks')
    obj['ground']['tracks']=[dict(u=.5,v=.5,life=1)];obj['ground']['furrows']=[dict(v=.6,life=1)]
    current=copy.deepcopy(obj);k.update(p,'sand_floor',obj,300,False,True);check(obj==current,'stored floor does not weather outdoors')
    k.update(p,'sand_floor',obj,300,True,True);check(not obj['ground']['tracks'] and not obj['ground']['furrows'],'rain washes old sand marks away')
    iid,obj=own('snow_floor');obj['ground'].update(powder=.4,tracks=[],frost=0)
    k.update(p,'snow_floor',obj,400,True,False,.7,-3,True);check(obj['ground']['powder']>.8 and obj['ground']['frost']>.5,'actual snowfall accumulates powder and frost even without liquid rain')
    depth=obj['ground']['powder'];k.update(p,'snow_floor',obj,2000,True,False,.7,15,False);check(obj['ground']['powder']<depth and obj['ground']['frost']<.1,'warm weather thins powder and melts frost')
    obj['ground'].update(frost=0,powder=.8);obj['uses']=0;p.start('item','snow_floor',instance=iid);finish(True)
    check(len(obj['ground']['tracks'])==4 and abs(obj['ground']['powder']-.7)<1e-9,'four snow steps compact real powder')
    # Verify the actual environmental update routes pond snowfall to the copy.
    iid,obj=own('snow_floor');obj['ground'].update(powder=.2,frost=0);weather(WeatherType.SNOWY,season=Season.WINTER)
    p._environment(300,False)
    check(obj['ground']['powder']>.6 and obj['ground']['frost']>.5,'global pond weather drives the placed snow floor state')
    state_before=copy.deepcopy(obj['ground']);g.habitat.store_item('snow_floor',iid);p.sync();p._environment(300,False)
    check(p.object_state('snow_floor',iid)['ground']==state_before,'global environment leaves the stored snow copy alone')
    weather();iid,obj=own('checkered_floor');obj['ground']['frost']=0;obj['dirt']=0;p.start('item','checkered_floor',instance=iid);plan=p.state['plan'];arrived()
    for _ in range(50):step()
    before=k.controls(plan['ground_work']);uses=obj['uses'];weather(WeatherType.RAINY);step(True);after=k.controls(plan['ground_work'])
    check(plan['ground_work']['id']=='wet_footing' and abs(after['u']-before['u'])<.01 and abs(after['v']-before['v'])<.01,'wet-weather retreat begins at the actual current footing')
    finish(True);check(obj['uses']==uses and plan['ground_work']['interrupted'] and k.controls(plan['ground_work'])['v']>=1.1,'withdrawal ends outside without completed-session credit')
    weather()
    for reason in ('store','move','replace'):
        iid,obj=own('stone_tiles');p.start('item','stone_tiles',instance=iid)
        if reason=='store':g.habitat.store_item('stone_tiles',iid)
        elif reason=='move':g.habitat.placed_items[0].x+=3
        else:g.habitat.placed_items=[PlacedItem('stone_tiles',10,6)]
        p.sync();p._activity(1);check(p.state['plan'] is None,reason+' cancels the exact-copy work')
    iid,obj=own('wooden_plank');p.start('item','wooden_plank');g.materials.remove_material('wooden_plank',g.materials.get_all_materials()['wooden_plank']);p.sync();p._activity(1)
    check(p.state['plan'] is None,'consuming the last crafting plank elsewhere cancels handling')
    for item,key,stage in [('stepping_stones','stone_cross','hatchling'),('sand_floor','sand_rake','adult'),('snow_floor','snow_crunch','duckling'),('wooden_plank','wood_grain','elder'),('lava_floor','lava_edge','hatchling'),('galaxy_floor','galaxy_orbit','adult')]:
        weather();g.duck.growth_stage=stage;iid,obj=own(item);obj['ground']['frost']=0;p.start('item',item,instance=iid);arrived();plan=p.state['plan'];plan['ground_work'].update(id=key,elapsed=k.ROUTINES[key]['duration']*.6)
        p._cache=None;s=snapshot(g,g.renderer);s['review']=item+'-'+stage;frames.append(s)
        if item=='lava_floor':check('not touched' in facts()['ground_work']['position'],'speech knows Cheese is outside the molten surface')
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
    (out/'ground-frames.json').write_text(json.dumps(frames));(out/'ground-native.json').write_text(json.dumps(dict(result='PASS',checks=checks,frames=len(frames),scores=len(k.ROUTINES)),indent=2))
    print(json.dumps(dict(result='PASS',checks=len(checks),frames=len(frames),scores=len(k.ROUTINES))))
    if '--serve' in sys.argv:
        weather();g.duck.growth_stage='adult';item='marble_tiles';iid,obj=own(item,True)
        for placed in p.placements:
            target=p.object_state(item,placed.instance);target['dirt']=.8;target['ground'].update(frost=0,tracks=[])
        def emit():
            p._cache=None;copies=[a.instance for a in p.placements if a.item_id==item]
            print(json.dumps(dict(type='physical_frame',frame=dict(scene=snapshot(g,g.renderer),copies=copies,item=item))),flush=True)
        emit()
        for line in sys.stdin:
            command=json.loads(line)
            if command.get('type')=='quit':break
            if command.get('type')=='test_fixture':
                item=command['item'];weather();iid,obj=own(item);obj['dirt']=0;obj['wetness']=0;obj['uses']=0;obj['ground'].update(frost=0,tracks=[],furrows=[])
            elif command.get('type')=='test_weather':
                weather(WeatherType.RAINY if command['wet'] else WeatherType.SUNNY);obj['last_use']=-1000;p.state['cooldowns']={}
            elif command.get('type')=='test_advance':
                if command.get('until')=='contact':
                    for _ in range(900):
                        step();work=(p.state['plan'] or {}).get('ground_work',{})
                        if work.get('events'):break
                else:finish()
            elif command.get('type')=='pond':p.command(command);p.sync()
            emit()
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
