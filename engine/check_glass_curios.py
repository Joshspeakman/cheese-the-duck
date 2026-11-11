"""Exercise actual placed curios, contact, forecast truth and save lifecycle."""
import os,sys,json,tempfile,copy,math
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-glass-curios-');os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,keepsakes as k,glass_curios as glass
from engine.scene import snapshot
from world.habitat import PlacedItem
from world.decorations import PlacedDecoration,RoomType
from world.atmosphere import Weather,WeatherType,Season
from audio.sound import sound_engine
sys.stdout=host.WIRE;checks=[];frames=[]
def check(ok,label):
    assert ok,label
    checks.append(label)
t=host.DesktopInput();g=host.DesktopGame(terminal=t,renderer_factory=host.CanvasRenderer);t.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
    g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.renderer._show_talk=False;sound_engine.enabled=False
    g.renderer._viewport_width=132;g.renderer._viewport_height=42;g.renderer._update_camera(132,42)
    p=g.living_pond;p.state['auto']=False;p.minds.model.state['next_social']=1e9
    def reset(item='snow_globe',stage='adult',twins=False):
        p.cancel();g.duck.current_action=None;g.behavior_ai.clear_action();g.duck.growth_stage=stage;g.duck.needs.energy=95;g.duck.needs.hunger=95;g.duck_store.sync_from_duck(g.duck)
        g.day_night.get_current_hour=lambda:12;g.day_night.get_current_minute=lambda:0
        g.atmosphere.current_season=Season.SPRING;g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.5,1,datetime.now().isoformat())
        g.habitat.owned_items=[];g.habitat.placed_items=[];g.habitat.stored_items=[];g.habitat.stored_placements=[]
        for room in g.decorations.rooms.values():room.decorations=[]
        if item=='snowglobe':
            g.decorations.owned_decorations[item]=1;g.decorations.rooms['garden'].unlocked=True
            g.decorations.rooms['garden'].decorations=[PlacedDecoration(item,RoomType.GARDEN,(6,5),datetime.now().isoformat())]
        else:
            g.habitat.owned_items=[item]*(2 if twins else 1);g.habitat.placed_items=[PlacedItem(item,10,6)]
            if twins:g.habitat.placed_items.append(PlacedItem(item,17,6))
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=35;pos.y=21
        p.sync();p.weather_type='sunny';p.season='spring';p.hour=12;p.state['cooldowns']={};p.state['ecology'].update(temperature=18,wind=.2)
        p.state['weather'].pop(p.biome,None);p._weather_front(False)
        placement=next(a for a in p.placements if a.item_id==item);obj=p.object_state(item,placement.instance);obj['last_use']=-1000
        obj['keepsake'].pop('glass',None);k.state(item,obj);obj['keepsake'].update(studies=0,open=0)
        return placement.instance,obj
    def step(capture=False):
        p.state['elapsed']+=.2;pos=g.renderer.duck_pos;pos._state_start_time-=.2;pos.update(.2);p._activity(.2)
        for placement in p.placements:
            if placement.item_id in ('snow_globe','snowglobe','crystal_ball'):k.update(p,placement.item_id,p.object_state(placement.item_id,placement.instance),.2,True)
        if capture:
            frame=snapshot(g,g.renderer);work=(p.state['plan'] or {}).get('keepsake_work')
            if work and .4<work['elapsed']/k.ROUTINES[work['id']]['duration']<.5:frame['review']='glass-'+p.state['plan']['target']+'-'+work['id']
            frames.append(frame)
    def finish(capture=False):
        for i in range(1000):
            if not p.state['plan']:return
            step(capture and i%5==0)
        raise AssertionError('curio interaction did not finish')
    for item in ('snow_globe','snowglobe','crystal_ball'):
        for core,spec in k.ROUTINES.items():
            if k.ITEMS[item]['type'] not in spec.get('types',[]):continue
            iid,obj=reset(item);before_uses=obj['uses'];possessions=copy.deepcopy((g.inventory.to_dict(),g.materials.get_all_materials(),g.habitat.currency,g.treasure.to_dict()))
            check(k.request(p,item,core,iid)[0],item+' accepts '+core)
            plan=p.state['plan'];initial=copy.deepcopy(obj);p._activity(1)
            check(obj==initial and plan['keepsake_work']['elapsed']==0,core+' no remote touch during approach')
            facts=k.conversation(p,plan);check('miniature' not in facts and 'weather_reading' not in facts,core+' no observation before arrival')
            finish(True)
            check(plan['keepsake_work']['done'] and obj['uses']==before_uses+1,core+' finishes once')
            check(possessions==(g.inventory.to_dict(),g.materials.get_all_materials(),g.habitat.currency,g.treasure.to_dict()),core+' preserves original possessions')
            seen=copy.deepcopy(obj);k.complete(p,plan);check(obj==seen,core+' repeated completion changes nothing')
            if core=='globe_pump':check(obj['keepsake']['glass']['pumps']==3 and obj['keepsake']['glass']['energy']>0, item+' all three physical strokes circulate snow')
            if core=='oracle_focus':check(obj['keepsake']['glass']['readings']==1 and obj['keepsake']['glass']['vision']['weather']==p.state['weather'][p.biome]['forecast'][0]['type'],'oracle reads the actual next front exactly once')
    # Native circulation integrates identically at different frame rates.
    a={'glass':dict(energy=1,phase=2,focus=.8)};b=copy.deepcopy(a);glass.update(a,12)
    for _ in range(120):glass.update(b,.1)
    check(all(abs(a['glass'][key]-b['glass'][key])<1e-10 for key in ('energy','phase','focus')),'snow circulation and focus decay are frame-rate independent')
    iid,obj=reset(twins=True);other=p.object_state('snow_globe',g.habitat.placed_items[1].instance_id)
    initial_other=copy.deepcopy(other);uses=obj['uses'];k.request(p,'snow_globe','globe_pump',iid);p.cancel()
    check(obj['uses']==uses and obj['keepsake']['glass']['pumps']==0,'cancel before touching a globe has no physical result')
    k.request(p,'snow_globe','globe_pump',iid);plan=p.state['plan']
    for _ in range(1000):
        step(True)
        if obj['keepsake']['glass']['pumps']:break
    check(obj['keepsake']['glass']['pumps']==1 and not plan['keepsake_work']['done'],'snow begins at the first pump contact')
    p.cancel();check(obj['uses']==uses and other==initial_other,'cancelling after a stroke preserves it without rewards or touching a twin')
    check(obj['keepsake']['open']==0,'spring-loaded pump releases when Cheese takes his wing away')
    state=copy.deepcopy(obj['keepsake']);k.update(p,'snow_globe',obj,200,False)
    check(obj['keepsake']==state,'stored curios do not advance through the outdoor clock')
    k.update(p,'snow_globe',obj,120,True)
    check(obj['keepsake']['glass']['energy']<.001,'snow settles naturally without another interaction')
    check(not k.request(p,'snow_globe','oracle_focus',iid)[0],'a globe cannot run crystal controls')
    check(not k.request(p,'snow_globe',[],iid)[0],'malformed requested action is rejected')
    # Context selection changes the actual choreography, not just its title.
    for age in ('egg','hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'):
        for item in ('snow_globe','snowglobe','crystal_ball'):
            iid,obj=reset(item,age);obj['uses']=0;selected=k.choose(p,item,dict(instance=iid))['id']
            if age=='egg':check(not k.request(p,item,'globe_scene' if item!='crystal_ball' else 'oracle_young',iid)[0],'egg never leaves its shell to operate '+item)
            elif age in ('hatchling','duckling'):
                check(selected==('oracle_young' if item=='crystal_ball' else 'globe_low'),age+' looks from below '+item)
                for core,spec in k.ROUTINES.items():
                    if k.ITEMS[item]['type'] in spec.get('types',[]) and spec.get('tool')!='none':check(not k.request(p,item,core,iid)[0],age+' cannot overreach '+core)
            elif item!='crystal_ball' and age in ('mature','elder','legendary'):check(selected=='globe_slow',age+' watches the snow settle')
            else:check(selected in ('globe_pump','oracle_focus'),age+' uses reachable controls '+item)
    iid,obj=reset();obj['uses']=0;p.hour=23;check(k.choose(p,'snow_globe',dict(instance=iid))['id']=='globe_night','darkness chooses cottage-window watching')
    p.hour=12;g.duck.needs.energy=25;check(k.choose(p,'snow_globe',dict(instance=iid))['id']=='globe_slow','tired Cheese watches quietly');g.duck.needs.energy=95
    for weather in ('rainy','stormy','drizzle','sleet','hail'):
        p.weather_type=weather;check(k.choose(p,'snow_globe',dict(instance=iid))['id']=='glass_raindrops',weather+' selects sealed-glass observation')
        check(not k.request(p,'snow_globe','globe_pump',iid)[0],weather+' keeps wet wings off the control')
    for weather in ('rainbow','double_rainbow','meteor_shower'):
        p.weather_type=weather;check(not glass.wet(p) and k.choose(p,'snow_globe',dict(instance=iid))['id']!='glass_raindrops',weather+' does not invent rain on the glass')
    for reason in ('rain','storm','move','replace','store'):
        iid,obj=reset();uses=obj['uses'];k.request(p,'snow_globe','globe_pump',iid);plan=p.state['plan']
        for _ in range(1000):
            step()
            if obj['keepsake']['glass']['pumps']:break
        strokes=obj['keepsake']['glass']['pumps']
        if reason in ('rain','storm'):p.weather_type='rainy' if reason=='rain' else 'stormy'
        elif reason=='move':g.habitat.placed_items[0].x+=3;p.sync()
        elif reason=='replace':g.habitat.placed_items=[PlacedItem('snow_globe',10,6)];p.sync()
        else:g.habitat.store_item('snow_globe',iid);p.sync()
        p._activity(.2)
        check(not p.state['plan'] and obj['uses']==uses and obj['keepsake']['glass']['pumps']==strokes and obj['keepsake']['open']==0,reason+' releases partial pumping without extra contact or completion')
    # A prophecy is a saved observation, never a promise or rewritten forecast.
    iid,obj=reset('crystal_ball');k.request(p,'crystal_ball','oracle_focus',iid);plan=p.state['plan'];front_before=copy.deepcopy(p.state['weather'])
    for _ in range(1000):
        step(True)
        if obj['keepsake']['glass']['vision']:break
    v=copy.deepcopy(obj['keepsake']['glass']['vision']);before=copy.deepcopy(obj);facts=k.conversation(p,plan)
    check(facts['weather_reading']['status']=='currently expected next front' and v['weather']==p.state['weather'][p.biome]['forecast'][0]['type'],'a fresh reading describes the actual queue')
    check(obj==before and p.state['weather']==front_before,'consulting and describing never changes the weather or the object again')
    facts['weather_reading']['weather']='imaginary';check(obj['keepsake']['glass']['vision']==v,'speech context cannot alter the saved reading')
    front=p.state['weather'][p.biome];front['forecast'][0]['type']='snowy' if v['weather']!='snowy' else 'sunny'
    check(k.conversation(p,plan)['weather_reading']['status']=='forecast changed since reading','a changed forecast never masquerades as the old certainty')
    p.state['elapsed']=v['at']+1;check(k.conversation(p,plan)['weather_reading']['status']=='past reading','an elapsed prediction remains a past reading')
    before_clock=plan['keepsake_work']['elapsed'];plan['paused']=True;p._activity(20)
    check(plan['keepsake_work']['elapsed']==before_clock and obj['keepsake']['glass']['readings']==1,'pause never repeats consultation contact')
    saved=copy.deepcopy(obj['keepsake']['glass']);g._save_game();g._flush_pending_save();g._load_game();p=g.living_pond;p.sync()
    check(p.object_state('crystal_ball',iid)['keepsake']['glass']==saved and p.state['plan']['paused'],'full save/reload preserves the actual crystal reading and paused control')
    p.cancel();g.habitat.store_item('crystal_ball',iid);p.sync();check(not k.request(p,'crystal_ball','oracle_focus',iid)[0],'stored crystal cannot be consulted through stale UI')
    damaged={'glass':{'energy':float('nan'),'phase':float('inf'),'readings':-99,'vision':{'weather':'fake'}}};glass.state(damaged)
    check(damaged['glass']['energy']==0 and damaged['glass']['phase']==0 and damaged['glass']['readings']==0 and damaged['glass']['vision'] is None,'damaged optional glass state normalizes safely')
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
    (out/'glass-curios-frames.json').write_text(json.dumps(frames))
    (out/'glass-curios-weathers.json').write_text(json.dumps(sorted(glass.WEATHER)))
    result=dict(result='PASS',checks=len(checks),frames=len(frames));(out/'glass-curios-native.json').write_text(json.dumps(dict(**result,assertions=checks),indent=2));print(json.dumps(result))
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
