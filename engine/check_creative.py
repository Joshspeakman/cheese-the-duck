"""Creative prop contact, interruption, inventory, context and full-save checks."""
import os,sys,tempfile,json,copy,subprocess
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-creative-');os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,creative_props as k
from engine.scene import snapshot
from world.habitat import PlacedItem
from world.atmosphere import Weather,WeatherType,Season
from audio.sound import sound_engine
sys.stdout=host.WIRE;checks=[];frames=[]
def check(ok,label):
    assert ok,label
    checks.append(label)
payload=[dict(id=id,elapsed=spec['duration']*i/100,start={**k.CONTROLS, 'flight':.74,'fold':.4,'cap':.7}) for id,spec in k.ROUTINES.items() for i in range(101)]
script="import {creativePose,CREATIVE_CONTROLS} from './engine/client/creative-routines.mjs';let s='';for await(const c of process.stdin)s+=c;console.log(JSON.stringify(JSON.parse(s).map(w=>Object.fromEntries(Object.keys(CREATIVE_CONTROLS).map(k=>[k,creativePose(w)[k]])))))"
render=json.loads(subprocess.check_output(['node','--input-type=module','-e',script],input=json.dumps(payload).encode(),cwd=ROOT))
check(all(all(abs(a[key]-v)<1e-9 for key,v in k.controls(w).items()) for a,w in zip(render,payload)),str(len(payload))+' native and renderer mechanical samples agree')
bad={'creative':{'aim':float('nan'),'focus':float('inf'),'strokes':999,'fold':-1,'motif':'invented'}}
check(k.state('easel',bad)['strokes']==12 and bad['creative']['aim']==.35 and bad['creative']['fold']==0 and bad['creative']['motif']=='pond','corrupt optional controls are finite and bounded')
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
        if item!='paper_plane_design':
            g.habitat.owned_items=[item];g.habitat.placed_items=[PlacedItem(item,10,6)]
            if twins:g.habitat.placed_items.append(PlacedItem(item,17,6))
        else:g.materials.add_material(item,1)
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
        raise AssertionError('creative action did not finish '+str(p.state['plan']))
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
        if iid:p._activity(1);check(obj==initial and plan['creative_work']['elapsed']==0,item+' controls wait for actual arrival')
        finish(True)
        check(plan['creative_work']['done'] and obj['uses']==initial['uses']+1,item+' completes exactly one use')
        check(possessions()==before,item+' does not consume or manufacture inventory')
        saved=copy.deepcopy(obj);k.complete(p,plan);check(saved==obj,item+' repeated callback cannot duplicate credit')
    # All authored action cores pass through the actual native planner/clock.
    for key,spec in k.ROUTINES.items():
        weather();item=next(i for i,s in k.ITEMS.items() if s['type']==spec['type']);iid,obj=own(item)
        obj['creative'].update(strokes=0,fold=0,cap=1,cover=0)
        check(p.start('item',item,instance=iid)[0],key+' accepts the actual item');plan=p.state['plan'];work=plan['creative_work'];work.update(id=key,label=spec['label'],start={**k.CONTROLS,'flight':.75 if key=='kite_reel' else 0})
        initial=obj['uses'];finish(True)
        check(not work.get('interrupted') and obj['uses']==initial+1 and obj.get('creative_routines',{}).get(key),key+' completes with physical event history')
    # Context selection from real day/weather/age and object history.
    iid,obj=own('telescope')
    for age in ('hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'):
        g.duck.growth_stage=age;weather(hour=23)
        check(k.choose(p,'telescope',iid)['id']==('scope_first_peek' if age in ('hatchling','duckling') else 'scope_stars'),age+' receives a fitting night observation')
    g.duck.growth_stage='egg';check(not p.start('item','telescope',instance=iid)[0],'an egg cannot climb or focus a telescope');g.duck.growth_stage='adult'
    for condition,expected in [(WeatherType.RAINY,'scope_cover'),(WeatherType.FOGGY,'scope_clouds'),(WeatherType.SUNNY,'scope_focus')]:
        weather(condition);check(k.choose(p,'telescope',iid)['id']==expected,'scope responds to '+condition.value)
    # Four painting sessions build one saved painting, not twelve looped effects.
    weather(hour=23);iid,obj=own('easel');obj['creative'].update(strokes=0,cover=0)
    for n,key in enumerate(('paint_sky','paint_bank','paint_ducks','paint_finish')):
        p.state['cooldowns']={};obj['last_use']=-1000
        check(p.start('item','easel',instance=iid)[0],'next painting phase starts')
        check(p.state['plan']['creative_work']['id']==key,'saved layers select '+key)
        finish(True);check(obj['creative']['strokes']==(n+1)*3,key+' adds three real paint layers')
    weather(hour=12);check(obj['creative']['motif']=='night' and k.choose(p,'easel',iid)['id']=='paint_study','finished night painting survives daytime and is admired instead of overwritten')
    # Independent copies, live contact and cancellation preserve only real work.
    weather();iid,obj=own('easel',True);other=p.object_state('easel',g.habitat.placed_items[1].instance_id);obj['creative']['strokes']=0
    p.start('item','easel',instance=iid);plan=p.state['plan'];before=obj['uses'];arrived()
    while not plan['creative_work']['events']:step()
    check(obj['creative']['strokes']==1 and other['creative']['strokes']==0,'first brush contact marks only the selected canvas')
    now=copy.deepcopy(obj);f=facts();check(f['creative_work']['painted_layers']==1 and obj==now,'natural speech gets true painting progress without changing it')
    f['creative_work']['painted_layers']=999;check(obj['creative']['strokes']==1,'conversation facts are detached')
    plan['paused']=True;clock=plan['creative_work']['elapsed'];p._activity(30);check(plan['creative_work']['elapsed']==clock and obj==now,'pause freezes brush and canvas')
    g._save_game();g._flush_pending_save();g._load_game();p=g.living_pond;p.sync();weather();obj=p.object_state('easel',iid)
    check(p.state['plan']['paused'] and obj['creative']==now['creative'],'full save reload retains unfinished canvas and paused clock')
    p.cancel();check(obj['uses']==before and obj['creative']['strokes']==1,'cancellation retains contact marks without completion rewards')
    # Wind and rain cause a real reel-in instead of a disappearing airborne kite.
    iid,obj=own('kite');obj.setdefault('creative_routines',{})['kite_tail']=1;weather(wind=.4)
    p.start('item','kite',instance=iid);plan=p.state['plan'];arrived()
    while k.controls(plan['creative_work'])['flight']<.6:step()
    height=k.controls(plan['creative_work'])['flight'];uses=obj['uses'];weather(WeatherType.STORMY,wind=.95);step(True)
    check(plan['creative_work']['id']=='kite_reel' and k.controls(plan['creative_work'])['flight']<=height,'storm starts reeling from actual flight height')
    prev=height
    while p.state['plan']:
        step(True);value=k.controls(plan['creative_work'])['flight'];check(value<=prev+1e-9,'reel-in never jumps upward');prev=value
    check(prev==0 and obj['uses']==uses and plan['creative_work']['interrupted'],'weather cancellation grounds the kite without completed-use credit')
    weather();iid,obj=own('telescope');p.start('item','telescope',instance=iid);g.habitat.store_item('telescope',iid);p.sync();p._activity(1)
    check(p.state['plan'] is None and obj['uses']==0,'storing an active telescope cancels its controls')
    iid,obj=own('paper_plane_design');p.start('item','paper_plane_design');g.materials.remove_material('paper_plane_design',g.materials.get_all_materials()['paper_plane_design']);p.sync();p._activity(1)
    check(p.state['plan'] is None,'losing the last paper design cancels folding')
    # Representative real scenes, including a young character at the eyepiece.
    for item,key,stage,at in [('telescope','scope_first_peek','hatchling',.62),('telescope','scope_stars','adult',.7),('easel','paint_ducks','adult',.6),('kite','kite_gust','juvenile',.55),('paper_plane_design','fold_wings','hatchling',.75)]:
        weather();g.duck.growth_stage=stage;iid,obj=own(item);p.start('item',item,instance=iid);arrived();plan=p.state['plan'];work=plan['creative_work'];work.update(id=key,elapsed=k.ROUTINES[key]['duration']*at,label=k.ROUTINES[key]['label'])
        if item=='easel':obj['creative']['strokes']=8
        p._cache=None;s=snapshot(g,g.renderer);s['review']=item+'-'+stage;frames.append(s)
    # Covers are removed by a physical action once the real weather clears.
    for item,key in [('easel','paint_uncover'),('paper_plane_design','fold_unwrap')]:
        weather();iid,obj=own(item);obj['creative']['cover']=1;obj['creative']['fold']=1;obj['last_use']=-1000
        check(p.start('item',item,instance=iid)[0] and p.state['plan']['creative_work']['id']==key,item+' uncovers after rain');finish();check(obj['creative']['cover']==0,item+' cover comes off at native contact')
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
    (out/'creative-frames.json').write_text(json.dumps(frames));(out/'creative-native.json').write_text(json.dumps(dict(result='PASS',checks=checks,frames=len(frames),scores=len(k.ROUTINES)),indent=2))
    print(json.dumps(dict(result='PASS',checks=len(checks),frames=len(frames),scores=len(k.ROUTINES))))
    if '--serve' in sys.argv:
        weather();g.duck.growth_stage='adult';item='easel';iid,obj=own(item,True);obj['creative'].update(strokes=0,cover=0)
        def emit():
            p._cache=None;copies=[a.instance for a in p.placements if a.item_id==item]
            print(json.dumps(dict(type='physical_frame',frame=dict(scene=snapshot(g,g.renderer),copies=copies,item=item))),flush=True)
        emit()
        for line in sys.stdin:
            command=json.loads(line)
            if command.get('type')=='quit':break
            if command.get('type')=='test_fixture':
                item=command['item'];weather();iid,obj=own(item);obj['creative'].update(strokes=0,cover=0,fold=0,folds=0)
            elif command.get('type')=='test_weather':weather(WeatherType.RAINY if command['wet'] else WeatherType.SUNNY)
            elif command.get('type')=='test_advance':
                if command.get('until')=='contact':
                    for _ in range(900):
                        step();work=(p.state['plan'] or {}).get('creative_work',{})
                        if work.get('events'):break
                else:finish()
            elif command.get('type')=='pond':p.command(command);p.sync()
            emit()
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
