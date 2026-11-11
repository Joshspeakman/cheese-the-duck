"""Real ownership, independent mechanisms, home weather and save boundaries."""
import os,sys,tempfile,json,copy,math
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-excursions-')
os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,excursions as e
from engine.scene import snapshot
from engine import object_history
from world.habitat import PlacedItem
from world.atmosphere import Weather,WeatherType,Season
from audio.sound import sound_engine
sys.stdout=host.WIRE
checks=[];frames=[]
def numbers(value):
    return [n for v in value.values() for n in numbers(v)] if isinstance(value,dict) else [value]
def check(ok,label):
    assert ok,label
    checks.append(label)

for item in e.ITEMS:
    bad={'excursion':{'phase':float('nan'),'wind_phase':float('inf'),'inflation':-20,'speed':'bad','cover':None,'wind':True,'lights':1000,'running':'yes'}}
    e.state(item,bad)
    check(all(isinstance(v,(int,float)) and math.isfinite(v) for v in numbers(bad['excursion'])),item+' corrupt optional state becomes finite')
    a={'condition':1};b=copy.deepcopy(a)
    e.update(item,a,37,True,'sunny',.3,12)
    for _ in range(370):e.update(item,b,.1,True,'sunny',.3,12)
    check(all(abs(x-y)<1e-9 for x,y in zip(numbers(a['excursion']),numbers(b['excursion']))),item+' mechanism is independent of timestep')
    before=copy.deepcopy(a);e.update(item,a,0,True,'sunny',.3,12)
    check(before==a,item+' zero time adds no movement')
    e.update(item,a,100,True,'stormy',.9,12)
    check(a['excursion']['speed']<1e-9 and not a['excursion']['running'] and a['excursion']['lights']==0,item+' storms stop empty motors and lamps')
    if e.ITEMS[item]['motion'] in ('envelope','inflation'):
        check(abs(a['excursion']['inflation']-.35)<.001,item+' bad weather lowers fabric pressure')
    e.update(item,a,100,True,'sunny',.1,23)
    check(a['excursion']['lights']==1 and not a['excursion']['running'],item+' quiet night lights without running rides')
    frozen=copy.deepcopy(a['excursion']);e.update(item,a,86400,False,'sunny',1,12)
    check(a['excursion']['phase']==frozen['phase'] and a['excursion']['wind_phase']==frozen['wind_phase'] and a['excursion']['inflation']==frozen['inflation'],item+' storage freezes moving parts')
    e.update(item,a,172800,True,'rainbow',.1,12)
    check(0<=a['excursion']['phase']<e.TAU,item+' offline advance remains bounded')
    if e.ITEMS[item]['motion'] in ('motor','scanner'):check(a['excursion']['running'],item+' rainbow is dry weather')

from engine import castle_work
for reason,change in [('switched off',{'motor':'off'}),('coiled hose',{'hose':1}),('damaged house',{})]:
    obj={'condition':.1 if reason=='damaged house' else 1};s=castle_work.state(obj);s.update(change)
    if 'hose' in change:s['targets']['hose']=change['hose']
    e.update('bounce_house',obj,100,True,'sunny',.1,12)
    check(not s['powered'] and obj['excursion']['inflation']<.16,reason+' cannot keep an empty house inflated')

t=host.DesktopInput();g=host.DesktopGame(terminal=t,renderer_factory=host.CanvasRenderer)
t.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
    g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.renderer._show_talk=False;sound_engine.enabled=False
    g.renderer._viewport_width=132;g.renderer._viewport_height=42;g.renderer._update_camera(132,42)
    p=g.living_pond;p.state['auto']=False;p.minds.model.state['next_social']=1e9
    g.duck.growth_stage='hatchling'
    for k in ('energy','hunger','fun','cleanliness','social'):setattr(g.duck.needs,k,90)
    g.duck_store.sync_from_duck(g.duck)
    def weather(kind=WeatherType.SUNNY,hour=12):
        g.day_night.get_current_hour=lambda:hour;g.day_night.get_current_minute=lambda:0
        g.atmosphere.set_current_biome('pond');g.atmosphere.current_season=Season.SPRING
        g.atmosphere.current_weather=Weather(kind,.7,1,datetime.now().isoformat())
        p.sync();front=p.state['weather'].setdefault('pond',{})
        front.update(type=kind.value,until=p.state['elapsed']+1e6,intensity=.7,forecast=[],front=0)
        p._last_weather=('pond',kind.value,0)
    def own(item):
        p.cancel();g.duck.current_action=None;g.behavior_ai.clear_action()
        g.habitat.owned_items=[];g.habitat.placed_items=[];g.habitat.stored_items=[];g.habitat.stored_placements=[]
        g.building.structures=[];g.decorations.stored_placements=[]
        for room in g.decorations.rooms.values():room.decorations=[]
        p.sync() # Clear previous obstacles before the real placement policy runs.
        g.habitat.owned_items=[item];g.habitat.stored_items=[item]
        check(g.habitat.show_item(item),item+' fits through original placement policy')
        p.sync();p.state['cooldowns'].clear()
        placed=next(a for a in g.habitat.placed_items if a.item_id==item)
        obj=p.object_state(item,placed.instance_id);obj['excursion']={};e.state(item,obj)
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=28;pos.y=23
        return placed.instance_id,obj
    def possessions():
        return copy.deepcopy((g.inventory.to_dict(),g.materials.get_all_materials(),g.habitat.currency,g.habitat.owned_items,g.treasure.to_dict()))
    def capture():
        p._cache=None;frames.append(snapshot(g,g.renderer))
    def tick(dt=1):p.advance(dt,offline=True)
    for item,spec in e.ITEMS.items():
        weather();iid,obj=own(item);before=possessions();uses=obj['uses']
        start=obj['excursion']['phase'];tick(10)
        check((obj['excursion']['phase']!=start)==(spec['motion'] in ('motor','scanner')),item+' native environment drives only actual motors')
        check(obj['uses']==uses and possessions()==before,item+' passive mechanisms add no item rewards')
        for _ in range(5):tick(.4);capture()
        weather(WeatherType.STORMY);tick(120);capture()
        check(not obj['excursion']['running'],item+' actual storm stops operation')
        weather(hour=23);tick(100);capture()
        check(obj['excursion']['lights']==1,item+' actual home nighttime reaches object')
        saved=copy.deepcopy(obj['excursion']);g._save_game();g._flush_pending_save();g._load_game();p=g.living_pond;p.state['auto']=False;p.sync()
        obj=p.object_state(item,iid)
        check(obj['excursion']==saved,item+' save/load retains exact mechanism phase and fabric')
        check(g.habitat.store_item(item,instance=iid),item+' can be stored through original handler');p.sync()
        saved=copy.deepcopy(obj['excursion']);weather();tick(90)
        check(obj['excursion']['phase']==saved['phase'] and obj['excursion']['wind_phase']==saved['wind_phase'],item+' original storage stops native clocks')
        check(g.habitat.show_item(item),item+' original placement restores stored copy');p.sync()
        check(g.habitat.placed_items[0].instance_id==iid,item+' replacement is the same physical copy')
        # Original use/cooldowns stay authoritative; no new trip or passenger reward.
        g.duck.growth_stage='adult';g.duck_store.sync_from_duck(g.duck);p.state['cooldowns'].clear();obj['last_use']=-1000
        ok,message=p.start('item',item,instance=iid);check(ok,item+' keeps original activity: '+message);plan=p.state['plan'];uses=obj['uses'];before=possessions()
        for _ in range(1000):
            if not p.state['plan']:break
            p.state['elapsed']+=.2;pos=g.renderer.duck_pos;pos._state_start_time-=.2;pos.update(.2);p._activity(.2)
        check(not p.state['plan'] and obj['uses']==uses+1,item+' completes exactly one original use')
        check(possessions()==before,item+' original activity preserves inventory and currency')
        g.duck.growth_stage='hatchling';g.duck_store.sync_from_duck(g.duck)
    # Real duplicate identities: storage pauses one wheel independently.
    weather();iid,obj=own('ferris_wheel');twin=PlacedItem('ferris_wheel',1,1)
    g.habitat.stored_placements.append(twin);p.sync();second=p.object_state('ferris_wheel',twin.instance_id)
    second['excursion']['phase']=2.3;tick(20)
    check(second['excursion']['phase']==2.3 and second['excursion']['speed']==0 and obj['excursion']['running'],'stored duplicate remains independent of the outdoor wheel')
    # Objects at home use home weather while Cheese visits another biome.
    g.atmosphere._biome_weather['pond']=Weather(WeatherType.STORMY,.8,1,datetime.now().isoformat())
    p.biome='forest';p.weather_type='sunny';p.state['weather']['forest']={'type':'sunny','until':p.state['elapsed']+1e6,'intensity':.1,'front':0,'forecast':[]}
    tick(60);check(not obj['excursion']['running'] and obj['excursion']['speed']<1e-9,'home storm stops the wheel while Cheese is elsewhere')
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
    (out/'excursions-frames.json').write_text(json.dumps(frames))
    result=dict(result='PASS',checks=checks,frames=len(frames),objects=len(e.ITEMS))
    (out/'excursions-native.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(dict(result='PASS',checks=len(checks),frames=len(frames),objects=len(e.ITEMS))))
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
