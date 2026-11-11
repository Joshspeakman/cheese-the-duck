"""Textile prop contact, interruption, inventory, context and full-save checks."""
import os,sys,tempfile,json,copy,subprocess
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-textile-');os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,textiles as k
from engine.scene import snapshot
from world.habitat import PlacedItem
from world.atmosphere import Weather,WeatherType,Season
from audio.sound import sound_engine
sys.stdout=host.WIRE;checks=[];frames=[]
def check(ok,label):
    assert ok,label
    checks.append(label)
payload=[dict(id=id,elapsed=spec['duration']*i/100,start={**k.CONTROLS,'roll':.37}) for id,spec in k.ROUTINES.items() for i in range(101)]
script="import {textilePose,TEXTILE_CONTROLS} from './engine/client/textile-routines.mjs';let s='';for await(const c of process.stdin)s+=c;console.log(JSON.stringify(JSON.parse(s).map(w=>Object.fromEntries(Object.keys(TEXTILE_CONTROLS).map(k=>[k,textilePose(w)[k]])))))"
render=json.loads(subprocess.check_output(['node','--input-type=module','-e',script],input=json.dumps(payload).encode(),cwd=ROOT))
check(all(all(abs(a[key]-v)<1e-9 for key,v in k.controls(w).items()) for a,w in zip(render,payload)),str(len(payload))+' native and renderer mechanical samples agree')
bad={'textile':{'roll':float('nan'),'loft':float('inf'),'nap':-1,'care':999999,'tracks':[{},dict(u=.5,v=.3)]}}
check(k.state('carpet_red',bad)['roll']==0 and bad['textile']['nap']==0 and bad['textile']['care']==9999 and len(bad['textile']['tracks'])==1,'corrupt optional material state is bounded')
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
        if item=='rug':
            g.decorations.owned_decorations[item]=1;g.decorations.place_decoration(item,'garden',(5,3))
        elif item=='moss_carpet':g.inventory.add_item(item)
        elif k.ITEMS[item]['portable']:g.materials.add_material(item,1)
        else:
            g.habitat.owned_items=[item];g.habitat.placed_items=[PlacedItem(item,10,6)]
            if twins:g.habitat.placed_items.append(PlacedItem(item,17,6))
        p.sync();p.state['cooldowns']={};p._cache=None
        for obj in [*p.state['instances'].values(),*p.state['objects'].values()]:obj['last_use']=-1000
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=36;pos.y=21
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
        raise AssertionError('textile action did not finish '+str(p.state['plan']))
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
        check(ok,item+' starts through actual ownership: '+msg);plan=p.state['plan']
        if iid:p._activity(1);check(obj==initial and plan['textile_work']['elapsed']==0,item+' controls wait for actual arrival')
        finish(True)
        check(plan['textile_work']['done'] and obj['uses']==initial['uses']+1,item+' completes exactly one use')
        check(possessions()==before,item+' does not consume or manufacture inventory')
        saved=copy.deepcopy(obj);k.complete(p,plan);check(saved==obj,item+' repeated callback cannot duplicate credit')
    # All authored action cores pass through the actual native planner/clock.
    for key,spec in k.ROUTINES.items():
        weather();item=next(i for i,s in k.ITEMS.items() if s['type'] in spec['types']);iid,obj=own(item)
        obj['textile'].update(roll=1 if key=='mat_unroll' else 0,fringe=.3,nap=.4,frost=.7 if key=='frost_sweep' else 0,tracks=[])
        check(p.start('item',item,instance=iid)[0],key+' accepts the actual item');plan=p.state['plan'];work=plan['textile_work'];work.update(id=key,label=spec['label'],start={**k.CONTROLS,'roll':1 if key=='mat_unroll' else 0})
        initial=obj['uses'];finish(True)
        check(not work.get('interrupted') and obj['uses']==initial+1 and obj.get('textile_routines',{}).get(key),key+' completes with physical event history')
    # Actual age, material, dirt, weather and time select different uses.
    weather();iid,obj=own('carpet_red');obj['textile'].update(roll=0,frost=0);obj['dirt']=0
    for age in ('hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'):
        g.duck.growth_stage=age;weather(hour=23)
        expected='young_steps' if age in ('hatchling','duckling') else 'elder_settle' if age in ('elder','legendary') else 'night_listen'
        check(k.choose(p,'carpet_red',iid)['id']==expected,age+' selects age-appropriate night use')
    g.duck.growth_stage='egg';check(not p.start('item','carpet_red',instance=iid)[0],'an egg cannot operate a rug');g.duck.growth_stage='adult'
    weather(WeatherType.RAINY);check(k.choose(p,'carpet_red',iid)['id']=='mat_roll','rain rolls exposed cloth instead of encouraging a wet nap')
    obj['textile']['roll']=1;check(k.choose(p,'carpet_red',iid)['id']=='rolled_inspect','rolled cloth waits for dry conditions without claiming it is dry')
    weather();check(k.choose(p,'carpet_red',iid)['id']=='mat_unroll','dry weather allows the real roll to be opened again')
    # The first contact changes only this physical copy; cancellation keeps it.
    iid,obj=own('persian_rug',True);obj['dirt']=.8;obj['textile'].update(roll=0,frost=0);other=p.object_state('persian_rug',g.habitat.placed_items[1].instance_id);other['dirt']=.8
    p.start('item','persian_rug',instance=iid);plan=p.state['plan'];uses=obj['uses'];arrived()
    while not plan['textile_work']['events']:step()
    check(abs(obj['dirt']-.6)<1e-9 and other['dirt']==.8,'brush contact cleans only the selected copy')
    current=copy.deepcopy(obj);f=facts();check(f['textile_work']['material']=='wool' and f['textile_work']['rolled']==0 and obj==current,'speech receives actual material and current state without operating it')
    plan['paused']=True;clock=plan['textile_work']['elapsed'];p._activity(30);check(obj==current and plan['textile_work']['elapsed']==clock,'pause freezes handling and the textile')
    g._save_game();g._flush_pending_save();g._load_game();p=g.living_pond;p.sync();weather();obj=p.object_state('persian_rug',iid)
    check(p.state['plan']['paused'] and obj['textile']==current['textile'] and obj['dirt']==current['dirt'],'full save reload retains actual material state and paused work')
    p.cancel();check(obj['uses']==uses and obj['dirt']==current['dirt'],'cancellation retains only the cleaning that already occurred')
    # Rolling on a weather change starts from the actual partially rolled state.
    iid,obj=own('carpet_red');obj['textile'].update(roll=.65,frost=0);p.start('item','carpet_red',instance=iid);plan=p.state['plan'];arrived()
    for _ in range(20):step()
    before=obj['textile']['roll'];uses=obj['uses'];weather(WeatherType.STORMY);step(True)
    check(plan['textile_work']['id']=='mat_roll' and abs(obj['textile']['roll']-before)<.01,'rain withdrawal starts from the real rolled edge')
    last=before
    while p.state['plan']:
        step(True);value=obj['textile']['roll'];check(value>=last-1e-9,'weather roll never reverses or jumps open');last=value
    check(last==1 and obj['uses']==uses and plan['textile_work']['interrupted'],'wet withdrawal finishes rolling without successful-session credit')
    weather();iid,obj=own('rubber_mat');obj['wetness']=.8;obj['textile']['frost']=0;p.start('item','rubber_mat',instance=iid);finish()
    check(abs(obj['wetness']-.55)<1e-8,'tilting the rubber mat drains actual retained moisture')
    iid,obj=own('welcome_mat');obj['uses']=0;obj['textile'].update(roll=0,frost=0);obj['dirt']=0;g.duck.needs.cleanliness=50;g.duck_store.sync_from_duck(g.duck)
    p.start('item','welcome_mat',instance=iid);plan=p.state['plan'];finish(True)
    check(g.duck.needs.cleanliness>50 and obj['dirt']>0 and len(obj['textile']['tracks'])==2,'wiping transfers dirt to the real mat and leaves two impressions')
    iid,obj=own('grass_patch');obj['textile']['frost']=0;k.update(p,'grass_patch',obj,300,True,True,.8,-3)
    check(obj['textile']['frost']>.5,'cold precipitation accumulates native frost')
    before=obj['textile']['frost'];k.update(p,'grass_patch',obj,300,False,True,.8,-3);check(obj['textile']['frost']==before,'stored materials do not accrue outdoor frost')
    k.update(p,'grass_patch',obj,500,True,False,.8,12);check(obj['textile']['frost']<before,'actual warmth melts the frost')
    for reason in ('store','move','replace'):
        iid,obj=own('tatami_mat');p.start('item','tatami_mat',instance=iid)
        if reason=='store':g.habitat.store_item('tatami_mat',iid)
        elif reason=='move':g.habitat.placed_items[0].x+=3
        else:g.habitat.placed_items=[PlacedItem('tatami_mat',10,6)]
        p.sync();p._activity(1);check(p.state['plan'] is None,reason+' cancels exact-copy handling')
    iid,obj=own('fabric_scrap');p.start('item','fabric_scrap');g.materials.remove_material('fabric_scrap',g.materials.get_all_materials()['fabric_scrap']);p.sync();p._activity(1)
    check(p.state['plan'] is None,'consuming the last crafting material elsewhere cancels handling')
    for item,key,stage in [('persian_rug','fringe_comb','hatchling'),('tatami_mat','tatami_grain','adult'),('welcome_mat','welcome_wipe','elder'),('moss_carpet','moss_pat','duckling'),('thatch','reed_sort','adult')]:
        weather();g.duck.growth_stage=stage;iid,obj=own(item);obj['textile'].update(roll=0,frost=0);p.start('item',item,instance=iid);arrived();plan=p.state['plan'];plan['textile_work'].update(id=key,elapsed=k.ROUTINES[key]['duration']*.6,start=k.CONTROLS.copy())
        p._cache=None;s=snapshot(g,g.renderer);s['review']=item+'-'+stage;frames.append(s)
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
    (out/'textile-frames.json').write_text(json.dumps(frames));(out/'textile-native.json').write_text(json.dumps(dict(result='PASS',checks=checks,frames=len(frames),scores=len(k.ROUTINES)),indent=2))
    print(json.dumps(dict(result='PASS',checks=len(checks),frames=len(frames),scores=len(k.ROUTINES))))
    if '--serve' in sys.argv:
        weather();g.duck.growth_stage='adult';item='persian_rug';iid,obj=own(item,True)
        for placed in p.placements:
            target=p.object_state(item,placed.instance);target['dirt']=.8;target['textile'].update(roll=0,frost=0,tracks=[])
        def emit():
            p._cache=None;copies=[a.instance for a in p.placements if a.item_id==item]
            print(json.dumps(dict(type='physical_frame',frame=dict(scene=snapshot(g,g.renderer),copies=copies,item=item))),flush=True)
        emit()
        for line in sys.stdin:
            command=json.loads(line)
            if command.get('type')=='quit':break
            if command.get('type')=='test_fixture':
                item=command['item'];weather();iid,obj=own(item);obj['dirt']=0;obj['wetness']=0;obj['textile'].update(roll=0,frost=0,tracks=[])
            elif command.get('type')=='test_weather':
                weather(WeatherType.RAINY if command['wet'] else WeatherType.SUNNY);obj['last_use']=-1000;p.state['cooldowns']={}
            elif command.get('type')=='test_advance':
                if command.get('until')=='contact':
                    for _ in range(900):
                        step();work=(p.state['plan'] or {}).get('textile_work',{})
                        if work.get('events'):break
                else:finish()
            elif command.get('type')=='pond':p.command(command);p.sync()
            emit()
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
