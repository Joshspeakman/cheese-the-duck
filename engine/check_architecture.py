"""Native structures, controls, ownership, weather, speech and full save/reload."""
import os,sys,tempfile,json,copy,subprocess
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-architecture-');os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,architecture as k
from engine.scene import snapshot
from world.habitat import PlacedItem
from world.atmosphere import Weather,WeatherType,Season
from audio.sound import sound_engine
sys.stdout=host.WIRE;checks=[];frames=[];weather_frames=[]
def check(ok,label):
    assert ok,label
    checks.append(label)
payload=[dict(id=id,elapsed=spec['duration']*i/100,start={key:.37 for key in k.CONTROLS}) for id,spec in k.ROUTINES.items() for i in range(101)]
script="import {architecturePose,ARCHITECTURE_CONTROLS} from './engine/client/architecture-routines.mjs';let s='';for await(const c of process.stdin)s+=c;console.log(JSON.stringify(JSON.parse(s).map(w=>Object.fromEntries(Object.keys(ARCHITECTURE_CONTROLS).map(k=>[k,architecturePose(w)[k]])))))"
samples=json.loads(subprocess.check_output(['node','--input-type=module','-e',script],input=json.dumps(payload).encode(),cwd=ROOT))
check(all(all(abs(a[key]-v)<1e-9 for key,v in k.controls(w).items()) for a,w in zip(samples,payload)),str(len(payload))+' native and renderer mechanism samples agree')
bad={'architecture':{'open':float('nan'),'phase':float('inf'),'brake':3,'studies':999999}};k.state('gate',bad);check(bad['architecture']['open']==0 and bad['architecture']['phase']==0 and bad['architecture']['brake']==1 and bad['architecture']['studies']==9999,'invalid optional saved values are bounded')
t=host.DesktopInput();g=host.DesktopGame(terminal=t,renderer_factory=host.CanvasRenderer);t.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
    g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.renderer._show_talk=False;sound_engine.enabled=False
    g.renderer._viewport_width=132;g.renderer._viewport_height=42;g.renderer._update_camera(132,42)
    p=g.living_pond;p.state['auto']=False;p.minds.model.state['next_social']=1e9
    g.duck.growth_stage='adult';g.duck.needs.energy=95;g.duck.needs.hunger=95;g.duck_store.sync_from_duck(g.duck)
    def weather(kind=WeatherType.SUNNY,hour=12,season=Season.SPRING):
        g.day_night.get_current_hour=lambda:hour;g.day_night.get_current_minute=lambda:0
        g.atmosphere.current_season=season;g.atmosphere.current_weather=Weather(kind,.5,1,datetime.now().isoformat());p.sync()
        p.state['ecology'].update(temperature=18,wind=.35)
    weather()
    def own(item,twins=False):
        p.cancel();g.duck.current_action=None;g.behavior_ai.clear_action();g.habitat.owned_items=[item];g.habitat.placed_items=[PlacedItem(item,6 if twins else 10,6)];g.habitat.stored_items=[];g.habitat.stored_placements=[];g.building.structures=[]
        for room in g.decorations.rooms.values():room.decorations=[]
        if twins:g.habitat.placed_items.append(PlacedItem(item,14,6))
        p.sync();p.state['cooldowns']={};p._cache=None
        for obj in [*p.state['instances'].values(),*p.state['objects'].values()]:obj['last_use']=-1000
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=15;pos.y=20
        iid=g.habitat.placed_items[0].instance_id;return iid,p.object_state(item,iid)
    def possessions():return copy.deepcopy((g.inventory.to_dict(),g.materials.get_all_materials(),g.habitat.currency,g.treasure.to_dict()))
    def step(capture=False):
        p.state['elapsed']+=.2;pos=g.renderer.duck_pos;pos._state_start_time-=.2;pos.update(.2);p._activity(.2)
        if capture:frames.append(snapshot(g,g.renderer))
    def finish(capture=False):
        for n in range(900):
            if not p.state['plan']:return
            step(capture and n%12==0)
        raise AssertionError('structure work did not finish')
    def arrived():
        for _ in range(900):
            step()
            if p.state['plan']['phase']=='act':return
        raise AssertionError('never arrived')
    def facts():
        p.minds.sync();return json.loads(p.minds.prompt('cheese','What are you working on?')[0]['content'].split('CHARACTER AND VERIFIED GAME STATE:\n',1)[1])
    def weather_frame(label,item,iid):
        p._cache=None
        weather_frames.append(dict(label=label,item=item,instance=iid,scene=snapshot(g,g.renderer)))
    for item in k.ITEMS:
        iid,obj=own(item);before=possessions();initial=copy.deepcopy(obj);ok,msg=p.start('item',item,instance=iid);check(ok,item+' starts: '+msg);plan=p.state['plan']
        p._activity(1);check(obj==initial and plan['architecture_work']['elapsed']==0,item+' cannot manipulate from a distance');finish(True)
        check(plan['architecture_work']['done'] and obj['uses']==initial['uses']+1,item+' earns one completed original use');check(possessions()==before,item+' invents no inventory, currency or treasure');saved=copy.deepcopy(obj);k.complete(p,plan);check(obj==saved,item+' cannot repeat a completion')
    for key,spec in k.ROUTINES.items():
        weather();item=next(i for i,s in k.ITEMS.items() if s['type'] in spec['types']);iid,obj=own(item)
        # Close, lower-flag and release tracks begin in the opposing physical state.
        if key in ('gate_close','mailbox_close','mailbox_lower_flag','windmill_release','well_raise'):
            for field in spec['controls']:obj['architecture'][field]=1.
        check(p.start('item',item,instance=iid)[0],key+' accepts its real object');plan=p.state['plan'];work=plan['architecture_work'];work.update(id=key,label=spec['label']);before=obj['uses'];finish(True)
        check(not work.get('interrupted') and obj['uses']==before+1 and obj.get('architecture_routines',{}).get(key),key+' finishes on the native clock')
    for item,choice,field in [('gate','gate_open','open'),('mailbox','mailbox_open','panel'),('mailbox','mailbox_flag','flag'),('wishing_well','well_lower','bucket'),('windmill','windmill_brake','brake')]:
        iid,obj=own(item,True);other=p.object_state(item,g.habitat.placed_items[1].instance_id);before=possessions();check(k.request(p,item,choice,iid)[0],choice+' accepts its explicit control');plan=p.state['plan'];uses=obj['uses'];arrived()
        while obj['architecture'][field]<.4:step(True)
        value=obj['architecture'][field];check(.4<=value<1 and other['architecture'][field]==0,choice+' moves continuously on the selected copy only')
        current=copy.deepcopy(obj);plan['paused']=True;p._activity(100);check(obj==current,choice+' pause holds the physical mechanism');p.cancel();check(obj['uses']==uses and obj['architecture'][field]==value,choice+' cancellation keeps only real movement');check(possessions()==before,choice+' grants no invented reward')
    weather();iid,obj=own('wishing_well');obj['architecture'].update(bucket=.4,crank=2.1)
    check(k.request(p,'wishing_well','well_raise',iid)[0],'partly lowered bucket can be raised');plan=p.state['plan'];arrived();step()
    check(abs(obj['architecture']['crank']-2.1)<1e-9,'new bucket work retains the saved handle orientation before contact')
    while obj['architecture']['bucket']>.2:step()
    expected=(2.1+(.4-obj['architecture']['bucket'])*k.math.pi*8)%(k.math.pi*2)
    check(abs(obj['architecture']['crank']-expected)<1e-9,'bucket crank continues from its saved angle during contact');p.cancel()
    weather();iid,obj=own('gate');k.request(p,'gate','gate_open',iid);plan=p.state['plan'];arrived()
    while obj['architecture']['open']<.5:step()
    plan['paused']=True;before=copy.deepcopy(obj);g._save_game();g._flush_pending_save();g._load_game();p=g.living_pond;p.sync();weather();loaded=p.object_state('gate',iid)
    check(p.state['plan']['paused'] and loaded['architecture']==before['architecture'],'full save reload retains the exact partially opened gate');p.state['plan']['paused']=False;finish(True);check(loaded['architecture']['open']==1,'resumed gate reaches its final physical position')
    for reason in ('move','replace','store','care','storm','displace'):
        weather();iid,obj=own('gate');k.request(p,'gate','gate_open',iid);arrived();plan=p.state['plan'];before=obj['uses']
        if reason=='move':g.habitat.placed_items[0].x+=2;p.sync()
        elif reason=='replace':g.habitat.placed_items=[PlacedItem('gate',10,6)];p.sync()
        elif reason=='store':g.habitat.store_item('gate',iid);p.sync()
        elif reason=='care':
            g.duck.current_action='feed';clock=plan['architecture_work']['elapsed'];p._activity(10);check(plan['architecture_work']['elapsed']==clock,'direct care holds architecture work');p.cancel();g.duck.current_action=None
        elif reason=='storm':weather(WeatherType.STORMY)
        else:g.renderer.duck_pos.x+=10
        finish();check(obj['uses']==before,reason+' cannot finish the abandoned session')
    weather();iid,obj=own('mailbox');p.start('item','mailbox',instance=iid);check('contents' not in facts()['garden_structure'],'Cheese cannot inspect the mailbox before arriving');arrived();check('Empty compartment' in facts()['garden_structure']['contents'],'conversation knows the real empty mailbox');p.cancel()
    for age in ('hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'):
        g.duck.growth_stage=age;weather(hour=23);expected='young_survey' if age in ('hatchling','duckling') else 'elder_survey' if age in ('elder','legendary') else 'night_survey';check(k.choose(p,'mailbox',iid)['id']==expected,age+' gets appropriate quiet inspection')
    g.duck.growth_stage='hatchling';check(not k.request(p,'mailbox','mailbox_open',iid)[0],'hatchlings cannot work heavy mechanisms');g.duck.growth_stage='egg';check(not p.start('item','mailbox',instance=iid)[0],'egg cannot operate architecture');g.duck.growth_stage='adult'
    weather(WeatherType.RAINY);check(k.choose(p,'mailbox',iid)['id']=='rain_drips' and not k.request(p,'mailbox','mailbox_open',iid)[0],'rain chooses observation instead of mechanism handling')
    weather();iid,obj=own('windmill');a=copy.deepcopy(obj);b=copy.deepcopy(obj);k.update(p,'windmill',a,50,True,.4)
    for _ in range(5):k.update(p,'windmill',b,10,True,.4)
    check(abs(a['architecture']['phase']-b['architecture']['phase'])<1e-9 and abs(a['architecture']['speed']-b['architecture']['speed'])<1e-9,'wind rotation has frame-rate-independent native integration')
    k.update(p,'windmill',obj,10,True,.5);check(obj['architecture']['speed']>.9,'wind drives the exposed sails');obj['architecture']['brake']=1;k.update(p,'windmill',obj,10,True,.5);check(obj['architecture']['speed']<.01,'brake actually stops rotation')
    obj['architecture']['brake']=0;k.update(p,'windmill',obj,10,True,.5,'stormy');check(obj['architecture']['speed']<.01,'storm feathers the sails');before=copy.deepcopy(obj);k.update(p,'windmill',obj,500,False,1);check(obj==before,'stored windmill never rotates')
    iid,obj=own('trellis');weather(season=Season.WINTER);p._environment(5,False);check(obj['architecture']['season']=='winter','actual pond season controls climbing foliage')
    # Landmark mechanisms use saved game weather/time, never renderer wall time.
    iid,obj=own('weather_vane');weather();p.state['weather']={};p._last_weather=None
    p._environment(1,False);heading=p.state['weather']['pond']['wind_heading'];check(0<=heading<1 and all('wind_heading' in f for f in p.state['weather']['pond']['forecast']),'weather fronts carry native directional wind')
    p.state['ecology']['wind_heading']=.99;p.state['weather']['pond']['wind_heading']=.01;p._environment(2,False)
    check(p.state['ecology']['wind_heading']>.99 or p.state['ecology']['wind_heading']<.01,'wind crosses northward wrap by the short route')
    a=copy.deepcopy(obj);b=copy.deepcopy(obj);a['architecture']['bearing']=b['architecture']['bearing']=6.2;k.update(p,'weather_vane',a,1,True,.4,'sunny',.02)
    for _ in range(10):k.update(p,'weather_vane',b,.1,True,.4,'sunny',.02)
    check(abs(a['architecture']['bearing']-b['architecture']['bearing'])<1e-9,'copper arrow follows native wind with frame-independent damping')
    saved=copy.deepcopy(a);k.update(p,'weather_vane',a,10,False,1,'stormy',.8);check(a==saved,'stored vane retains its last orientation')
    for heading,label in [(0,'East'),(.25,'South'),(.5,'West'),(.75,'North')]:
        p.state['ecology'].update(wind_heading=heading,wind=.4);k.update(p,'weather_vane',obj,30,True,.4,'sunny',heading)
        weather_frame('Vane / '+label+' wind','weather_vane',iid)
    for sky in ('rainy','snowy','windy'):
        weather(WeatherType(sky))
        for heading,label in [(0,'East'),(.5,'West')]:
            p.state['ecology'].update(wind_heading=heading,wind=.8);k.update(p,'weather_vane',obj,30,True,.8,sky,heading)
            weather_frame('Vane / '+sky+' / '+label+' wind','weather_vane',iid)
    iid,obj=own('sundial')
    for hour,sky,visible,side in [(8,'sunny',True,-1),(12,'sunny',True,0),(16,'sunny',True,1),(23,'sunny',False,0),(12,'overcast',False,0),(12,'rainy',False,0)]:
        weather(WeatherType(sky),hour=hour);k.update(p,'sundial',obj,1,True,.2,sky,.3);a=obj['architecture'];check((a['sun']>.1)==visible,'sundial sunlight at '+str(hour)+' '+sky)
        if visible:check(abs(k.math.sin(a['shadow_angle']))<1e-8 if not side else k.math.sin(a['shadow_angle'])*side>0,'sundial shadow follows the actual hour')
        weather_frame('Sundial / '+str(hour)+':00 '+sky,'sundial',iid)
    weather(season=Season.SUMMER);k.update(p,'sundial',obj,1,True,.2);summer=obj['architecture']['shadow_length'];weather_frame('Sundial / summer noon','sundial',iid)
    weather(season=Season.WINTER);k.update(p,'sundial',obj,1,True,.2);check(obj['architecture']['shadow_length']>summer,'winter makes the stylized solar shadow longer');weather_frame('Sundial / winter noon','sundial',iid)
    weather();iid,obj=own('flag_pole');obj['architecture']['flag']=1
    for heading,label in [(0,'East'),(.25,'South'),(.5,'West'),(.75,'North')]:
        p.state['ecology'].update(wind_heading=heading,wind=.65);k.update(p,'flag_pole',obj,30,True,.65,'sunny',heading)
        check(abs(k.math.sin(obj['architecture']['bearing']-heading*k.math.pi*2))<1e-8,'native pennant bearing follows '+label+' wind');weather_frame('Pennant / '+label+' wind','flag_pole',iid)
    weather();iid,obj=own('flag_pole',True);other=p.object_state('flag_pole',g.habitat.placed_items[1].instance_id);uses=obj['uses'];check(k.request(p,'flag_pole','flag_hoist',iid)[0],'explicit pennant command starts real halyard work');arrived()
    while obj['architecture']['flag']<.3:step(True)
    value=obj['architecture']['flag'];check(0<value<1 and other['architecture']['flag']==0,'halyard moves only the selected flag')
    plan=p.state['plan'];plan['paused']=True;before=copy.deepcopy(obj['architecture']);wind=copy.deepcopy(p.state['weather']);g._save_game();g._flush_pending_save();g._load_game();p=g.living_pond;p.sync();loaded=p.object_state('flag_pole',iid)
    check(loaded['architecture']==before and p.state['weather']==wind and p.state['plan']['paused'],'save/load retains partial hoist and directional weather fronts');p.cancel();check(loaded['uses']==uses,'cancelled flag work adds no completed use')
    weather();check(k.request(p,'flag_pole','flag_lower',iid)[0],'part-raised flag can be lowered from its saved height');finish(True);check(loaded['architecture']['flag']==0,'flag comes down through actual native contact')
    iid,obj=own('scarecrow');k.update(p,'scarecrow',obj,2,True,.8);check(obj['architecture']['phase']>0 and obj['architecture']['wind']==.8,'scarecrow scarf uses native breeze and time');saved=copy.deepcopy(obj);k.update(p,'scarecrow',obj,50,False,.9);check(obj==saved,'stored scarf has no autonomous animation clock')
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True);(out/'architecture-frames.json').write_text(json.dumps(frames));(out/'landmark-weather-frames.json').write_text(json.dumps(weather_frames));(out/'architecture-native.json').write_text(json.dumps(dict(result='PASS',checks=len(checks),assertions=checks,frames=len(frames),weatherFrames=len(weather_frames)),indent=2));print(json.dumps(dict(result='PASS',checks=len(checks),frames=len(frames),cores=len(k.ROUTINES),weatherFrames=len(weather_frames))))
    if '--serve' in sys.argv:
        weather();g.duck.growth_stage='adult';item='gate';iid,obj=own(item,True)
        def emit():
            p._cache=None;copies=[a.instance for a in p.placements if a.item_id==item]
            print(json.dumps(dict(type='physical_frame',frame=dict(scene=snapshot(g,g.renderer),copies=copies,item=item))),flush=True)
        emit()
        for line in sys.stdin:
            command=json.loads(line)
            if command.get('type')=='quit':break
            if command.get('type')=='test_fixture':
                item=command['item'];weather();iid,obj=own(item,True);obj['dirt']=0;obj['wetness']=0;obj['uses']=0
            elif command.get('type')=='test_advance':
                if command.get('until')=='contact':
                    for _ in range(900):
                        step();work=(p.state['plan'] or {}).get('architecture_work',{})
                        if work and work['elapsed']>k.ROUTINES[work['id']]['duration']*.425:break
                else:finish()
            elif command.get('type')=='test_ready':
                p.state['cooldowns']={}
                for state in p.state['instances'].values():state['last_use']=-1000
            elif command.get('type')=='pond':p.command(command);p.sync()
            emit()
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
