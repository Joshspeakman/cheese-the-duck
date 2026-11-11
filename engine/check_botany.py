"""Real rooted plant lifecycle, care arrivals, interruption and persistence."""
import os,sys,tempfile,json,copy,random,subprocess
from pathlib import Path
from types import SimpleNamespace
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-botany-')
os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,botany
from engine.living_world import LivingPond
from engine.item_profiles import ITEMS
from engine.scene import snapshot
from world.habitat import PlacedItem
from world.atmosphere import Weather,WeatherType,Season
from world.garden import PlantedPlant,GrowthStage
sys.stdout=host.WIRE;random.seed(34)
checks=[];frames=[]
def check(ok,label):
    assert ok,label
    checks.append(label)

# Definitions used by the UI and simulation must agree, including all foods.
script="import {catalog,itemProfile,itemFamily} from './engine/client/ultra-items.mjs';console.log(JSON.stringify(Object.fromEntries(catalog.map(i=>[i.id,itemProfile(i,itemFamily(i.id))]))));"
profiles=json.loads(subprocess.check_output(['node','--input-type=module','-e',script],cwd=str(ROOT)))
for key,profile in profiles.items():
    assert all(ITEMS[key][k]==v for k,v in profile.items()),(key,profile,ITEMS[key])
check(len(profiles)==542,'all 542 simulation and renderer use profiles agree')
def seed(item,moisture=.55):
    obj=dict(growth=.35,dirt=0.,botany=dict(moisture=moisture,health=.9,bloom=.65,care_count=0,last_care=None))
    p=SimpleNamespace(placed={item:True},season='spring',state={'ecology':dict(soil=.7,water=.8,wind=.2,temperature=20.),'objects':{item:obj}})
    return p,obj
for item in botany.ROOTED:
    p,obj=seed(item);before=copy.deepcopy(obj)
    botany.update(p,item,obj,10,False,.5,20)
    check(obj['growth']>before['growth'] and obj['botany']['moisture']<.55,item+' grows in suitable soil and uses moisture')
    p.placed={};before=copy.deepcopy(obj);botany.update(p,item,obj,120,True,1,20)
    check(obj==before,item+' in storage keeps its biological state')
    p.placed={item:True};p.season='winter';before=obj['growth'];botany.update(p,item,obj,10,False,.5,-4)
    check(obj['growth']==before,item+' winter dormancy')
    p.season='spring';obj['botany']['moisture']=.1;before=.1;botany.update(p,item,obj,10,True,1,20)
    check(obj['botany']['moisture']>before,item+' absorbs rain')
for item,pref in botany.BLUEPRINTS.items():
    if pref['rooted']:continue
    p,obj=seed(item);before=copy.deepcopy(obj);botany.update(p,item,obj,120,True,1,20)
    check(obj==before,item+' harvested specimen is not a growing plant')
p,cactus=seed('cactus');q,fern=seed('fern');botany.update(p,'cactus',cactus,60,False,.5,28);botany.update(q,'fern',fern,60,False,.5,28)
check(cactus['botany']['moisture']>fern['botany']['moisture'],'succulents retain more water than potted ferns')
p,obj=seed('fern',0);before=obj['growth'];botany.update(p,'fern',obj,60,False,.5,28)
check(obj['growth']==before and obj['botany']['health']<.9,'drought pauses growth and reduces health')
p,obj=seed('fern',.1);plan={'kind':'item','target':'fern','plant_care':'water'}
botany.complete(p,plan);before=copy.deepcopy(p.state);botany.complete(p,plan)
check(before==p.state and obj['botany']['moisture']==.72 and p.state['ecology']['water']<.8,'water is transferred once, capped at soil capacity')
p,obj=seed('fern',.1);p.state['ecology']['water']=.1
check(botany.care_mode(p,'fern')=='inspect','low pond water prevents a watering plan')
botany.complete(p,{'kind':'item','target':'fern','plant_care':'water'})
check(obj['botany']['moisture']==.1 and obj['botany']['care_count']==0,'water becoming unavailable cannot be conjured')
p,obj=seed('fern',.1);p.state['ecology']['temperature']=-3
check(botany.care_mode(p,'fern')=='inspect','freezing conditions prevent watering')
p,obj=seed('fern');p.placed={};before=copy.deepcopy(obj);botany.complete(p,{'kind':'item','target':'fern','plant_care':'water'})
check(before==obj,'stored plants cannot be watered by a stale completion')
p,obj=seed('fern');obj['dirt']=.7
check(botany.care_mode(p,'fern')=='brush','dirty leaves select debris care')
botany.complete(p,{'kind':'item','target':'fern','plant_care':'brush'})
check(abs(obj['dirt']-.4)<1e-8 and obj['botany']['last_care']=='brush','brushing removes actual dirt')

t=host.DesktopInput();g=host.DesktopGame(terminal=t,renderer_factory=host.CanvasRenderer)
t.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
    g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.renderer._show_talk=False
    g.renderer._viewport_width=132;g.renderer._viewport_height=42;g.renderer._update_camera(132,42)
    p=g.living_pond;p.state['auto']=False;p.minds.model.state['next_social']=10**9
    g.habitat.owned_items.extend(botany.ROOTED);g.duck.growth_stage='hatchling'
    g.duck.needs.energy=90;g.duck_store.sync_from_duck(g.duck)
    g.day_night.get_current_hour=lambda:12;g.day_night.get_current_minute=lambda:0
    g.atmosphere.current_season=Season.SPRING
    def weather():
        g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.5,1,datetime.now().isoformat())
    weather();p.sync();clock=0.
    def begin(mode='water',item='fern'):
        p.cancel();weather();g.habitat.placed_items=[PlacedItem(item,10,6)];p.sync()
        p.state['cooldowns']={};p.state['objects'][item].update(last_use=-1000,dirt=.7 if mode=='brush' else 0.)
        botany.state(p.state['objects'][item]).update(moisture=.1 if mode=='water' else .65,health=.9)
        p.state['ecology'].update(water=.8,temperature=20)
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=35;pos.y=21
        ok,msg=p.start('item',item);check(ok,'start '+item+' '+mode+': '+msg)
        check(p.state['plan']['plant_care']==mode,'actual state selects '+mode)
        return p.state['plan']
    def advance(n,capture=False):
        global clock
        for _ in range(n):
            clock+=.2;p.state['elapsed']+=.2
            pos=g.renderer.duck_pos;pos._state_start_time-=.2;pos.update(.2);p._activity(.2)
            if capture and int(clock*5)%5==0:frames.append(snapshot(g,g.renderer))
    for mode in ('water','brush','inspect'):
        plan=begin(mode);before=copy.deepcopy(p.state['objects']['fern']);water=p.state['ecology']['water']
        p._activity(1)
        check(p.state['objects']['fern']==before,'no '+mode+' reward before physical arrival')
        for _ in range(600):
            advance(1,True)
            if not p.state['plan']:break
        after=p.state['objects']['fern']
        check(plan.get('arrived') and not p.state['plan'],'Cheese arrives and finishes '+mode)
        check(after['uses']==before['uses']+1 and after['botany']['care_count']==before['botany']['care_count']+1,'one completed '+mode+' memory')
        check((p.state['ecology']['water']<water)==(mode=='water'),'only actual watering takes pond water')
        old=copy.deepcopy(after);advance(20);check(after==old,'no duplicate care after '+mode)
    plan=begin();before=copy.deepcopy(p.state['objects']['fern']);plan['paused']=True;advance(30)
    check(p.state['objects']['fern']==before and plan['elapsed']==0,'pausing freezes care without rewards')
    saved=p.save();loaded=LivingPond(saved)
    check(loaded.state['objects']['fern']['botany']==before['botany'] and loaded.state['plan']['paused'],'care state and unfinished paused plan survive save/load')
    plan['paused']=False;g.habitat.placed_items=[];p.sync();advance(2)
    check(not p.state['plan'] and p.state['objects']['fern']['uses']==before['uses'],'storage cancels care without reward')
    plan=begin();before=p.state['objects']['fern']['uses'];g.habitat.placed_items[0].x=5;p.sync();advance(2)
    check(not p.state['plan'] and p.state['objects']['fern']['uses']==before,'moving the plant cancels care')
    plan=begin();p.weather_type='stormy';advance(2)
    check(not p.state['plan'],'storm interrupts outdoor plant care')
    plan=begin();plan.pop('destination');advance(1)
    check(not p.state['plan'],'legacy malformed plant plan cancels safely')
    p.state['cooldowns']={};g.duck.growth_stage='egg'
    check(not p.start('item','fern')[0],'an egg cannot tend plants')
    g.duck.growth_stage='hatchling';p.state['cooldowns']={};g.habitat.placed_items=[];p.sync()
    check(not p.start('item','fern')[0],'stored plants cannot be started')
    plot=next(plot for plot in g.garden.plots.values() if plot.is_unlocked)
    plot.plant=PlantedPlant('mint',plot.plot_id,datetime.now().isoformat(),datetime.now().isoformat(),water_level=20)
    plan=begin('water','garden_plot');p.state['objects']['garden_plot']['botany']['moisture']=.7
    check(botany.care_mode(p,'garden_plot')=='water','thirsty actual crops choose watering even when bed soil is moist')
    stocks=copy.deepcopy(g.garden.harvest_inventory);materials=copy.deepcopy(g.materials.get_all_materials())
    for _ in range(600):
        advance(1,True)
        if not p.state['plan']:break
    check(plot.plant.water_level==70 and plot.plant.times_watered==1,'garden bed care waters the real garden crop once')
    check(g.garden.harvest_inventory==stocks and g.materials.get_all_materials()==materials,'garden care never grants harvested ingredients')
    previous=p.state['ecology']['water'];advance(20)
    check(plot.plant.times_watered==1 and p.state['ecology']['water']==previous,'finished garden care cannot replay watering')
    plot.plant.is_withered=True;plot.plant.growth_stage=GrowthStage.WITHERED;plot.plant.water_level=0
    p.state['objects']['garden_plot']['botany']['moisture']=.7
    check(botany.care_mode(p,'garden_plot')=='inspect','withering is not undone by decorative bed care')
    # Actual multi-object daytime snapshot for reviewing young Cheese readability.
    g.habitat.placed_items=[]
    for item,x,y in [('tree_cherry',3.5,6),('fern',10,6),('flower_rose',16,6)]:
        g.habitat.placed_items.append(PlacedItem(item,x,y))
    p.sync();g.renderer.duck_pos.x=68;g.renderer.duck_pos.y=24;weather();p.sync()
    frames.append(snapshot(g,g.renderer))
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
    (out/'botanical-frames.json').write_text(json.dumps(frames))
    result={'result':'PASS','checks':len(checks),'rootedPlants':len(botany.ROOTED),'drawings':len(botany.BLUEPRINTS),'frames':len(frames)}
    (out/'botanical-simulation.json').write_text(json.dumps(dict(result,details=checks),indent=2))
    print(json.dumps(result))
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    from audio.sound import sound_engine
    sound_engine.shutdown()
