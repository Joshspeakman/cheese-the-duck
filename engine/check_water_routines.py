"""Real water use, changing conditions, placement, interruption and persistence."""
import os,sys,tempfile,json,copy,random
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-water-');os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,water_routines
from engine.living_world import LivingPond
from engine.scene import snapshot
from world.habitat import PlacedItem
from world.atmosphere import Weather,WeatherType
sys.stdout=host.WIRE;random.seed(74)
checks=[];frames=[]
def check(ok,label):
    assert ok,label
    checks.append(label)
t=host.DesktopInput();g=host.DesktopGame(terminal=t,renderer_factory=host.CanvasRenderer)
t.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
    g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.renderer._show_talk=False
    p=g.living_pond;p.state['auto']=False;b=p.minds;b.model.state['next_social']=10**9
    g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.5,1,datetime.now().isoformat())
    g.habitat.owned_items.extend(water_routines.WATER);g.habitat.placed_items=[];p.sync();clock=0
    def advance(n):
        global clock
        for _ in range(n):
            clock+=.2;p.state['elapsed']+=.2
            pos=g.renderer.duck_pos;pos._state_start_time-=.2;pos.update(.2);p._activity(.2)
            plan=p.state['plan']
            if plan and plan.get('water_routine') and int(clock*5)%5==0:
                frames.append(snapshot(g,g.renderer))
    def begin(item,stage='adult',temperature=22,ice=0,energy=90,weather='sunny',hour=15,desired=None):
        p.cancel();g.duck.growth_stage=stage;g.duck.needs.energy=energy;g.duck.needs.hunger=90
        g.duck.needs.cleanliness=40;g.duck.needs.fun=40
        g.duck_store.sync_from_duck(g.duck)
        g.day_night.get_current_hour=lambda:int(hour);g.day_night.get_current_minute=lambda:0
        g.atmosphere.current_weather=Weather(WeatherType(weather),.5,1,datetime.now().isoformat())
        g.habitat.placed_items=[PlacedItem(item,10,6)];p.sync();p.weather_type=weather;p.hour=hour
        p.state['ecology'].update(temperature=temperature,ice=ice);p.state['cooldowns']={}
        obj=p.state['objects'][item];obj.update(last_use=-1000,dirt=.1,wetness=0,last_water_routine=None)
        obj['water_routines']={key:(0 if key==desired else 10) for key in water_routines.ROUTINES} if desired else {}
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=46;pos.y=21
        ok,msg=p.start('item',item);check(ok,'start real placed '+item+': '+msg)
        # start() refreshes the actual game hour/weather; fixtures set the
        # environment again before the simulation chooses its arrived activity.
        p.weather_type=weather;p.hour=hour
        for _ in range(500):
            advance(1)
            if p.state['plan'] and p.state['plan'].get('water_routine'):break
        check(bool(p.state['plan'] and p.state['plan'].get('water_routine')),item+' reaches its water activity')
        return p.state['plan'],p.state['plan']['water_routine']
    cases=[('shallow_steps','pool_kiddie',{}),('paddle_loop','pool_large',{}),('lazy_drift','pool_large',{'energy':40}),
           ('wing_rinse','bird_bath',{}),('bubble_soak','hot_tub',{}),('steam_stretch','hot_tub_deluxe',{'temperature':5}),
           ('watch_koi','koi_pond',{}),('small_sips','water_bowl',{}),('fountain_rings','fountain_small',{}),
           ('catch_spray','sprinkler',{}),('spray_dash','sprinkler_system',{'temperature':30}),('cascade_listen','waterfall',{}),
           ('rain_rings','pond',{'weather':'drizzle'}),('moon_reflection','pond',{'hour':22}),('ripple_watch','birdbath',{'temperature':5}),
           ('ice_inspect','pond',{'temperature':-5,'ice':.7})]
    for expected,item,kwargs in cases:
        plan,routine=begin(item,desired=expected,**kwargs);old=p.state['objects'][item]['uses']
        check(routine['id']==expected,'conditions select '+expected+', got '+routine['id'])
        check(routine['label'] in json.dumps(b.prompt('cheese','What are you doing?')),'chat knows the actual '+expected+' activity')
        check(abs(g.renderer.duck_pos.x-plan['destination'][0])+abs(g.renderer.duck_pos.y-plan['destination'][1])<=3.001,'arrive before '+expected)
        for _ in range(500):
            advance(1)
            if p.state['plan'] is None:break
        check(routine['done'] and not routine.get('interrupted') and p.state['plan'] is None,expected+' finishes and releases Cheese')
        check(p.state['objects'][item]['uses']==old+1,expected+' grants one actual item use')
        check(p.state['objects'][item]['water_routines'][expected]==1,expected+' records a single completed memory')
        if water_routines.ROUTINES[expected]['mode'] in ('edge','sip'):
            check(g.duck.needs.cleanliness==40 and p.state['objects'][item]['wetness']==0,expected+' does not pretend observation or drinking was a bath: '+repr((g.duck.needs.cleanliness,p.state['objects'][item]['wetness'])))
        else:
            check(g.duck.needs.cleanliness>40 and p.state['objects'][item]['wetness']==1,expected+' records actual bathing effects')
        advance(50);check(p.state['objects'][item]['uses']==old+1,expected+' never repeats its reward')
    plan,routine=begin('pool_large',stage='hatchling');check(water_routines.ROUTINES[routine['id']]['mode']=='edge','a hatchling watches a deep pool from the bank')
    plan,routine=begin('pool_kiddie',stage='hatchling');check(water_routines.ROUTINES[routine['id']]['mode']=='wade','a hatchling can use shallow water')
    elapsed=routine['elapsed'];plan['paused']=True;advance(30);check(routine['elapsed']==elapsed,'pause freezes water acting')
    saved=LivingPond(p.save());check(saved.state['plan']['paused'],'load holds the plan until the player resumes')
    plan['paused']=False;uses=p.state['objects']['pool_kiddie']['uses'];g.habitat.placed_items=[];p.sync();advance(60)
    check(p.state['plan'] is None and p.state['objects']['pool_kiddie']['uses']==uses,'putting the pool away cancels without a reward')
    plan,routine=begin('pool_large');uses=p.state['objects']['pool_large']['uses'];p.weather_type='thunderstorm';advance(60)
    check(routine.get('interrupted') and p.state['plan'] is None,'a storm ends outdoor swimming immediately')
    check(p.state['objects']['pool_large']['uses']==uses,'weather interruption grants no use or memory')
    plan,routine=begin('pond');p.state['ecology']['ice']=.7;advance(1)
    check(routine.get('interrupted') and p.state['plan'] is None,'forming ice cancels an existing swim')
    plan,routine=begin('hot_tub');p.cancel();check(g.renderer.duck_pos._state_str=='idle','player cancellation releases the held bathing pose')
    p.sync();g.habitat.placed_items=[];p.sync();p.state['objects']['pool_large']['last_use']=-1000
    check(not p.start('item','pool_large')[0],'an owned but unplaced pool cannot be used')
    g.habitat.placed_items=[PlacedItem('pool_large',10,6)];p.sync();g.duck.growth_stage='egg'
    check(not p.start('item','pool_large')[0],'an egg cannot swim itself into a pool')
    restored=LivingPond(p.save());check(restored.state['objects']['pond']['water_routines']==p.state['objects']['pond']['water_routines'],'completed water memories survive serialization')
    from engine.item_profiles import ITEMS
    check(ITEMS['pond_mat']['kind']=='comfort' and ITEMS['pond_mat']['material']=='fabric','the pond mat is fabric, not a usable pool')
    out=ROOT/'engine/artifacts/animation-milestone';result={'result':'PASS','checks':len(checks),'details':checks,'nativeFrames':len(frames),'scores':len(cases)}
    (out/'water-simulation.json').write_text(json.dumps(result,indent=2));(out/'water-frames.json').write_text(json.dumps(frames));print(json.dumps({k:v for k,v in result.items() if k!='details'}))
finally:
    b.close()
    if hasattr(g,'_save_executor'):g._save_executor.shutdown(wait=True)
    if hasattr(g,'_talk_executor'):g._talk_executor.shutdown(wait=False)
    from audio.sound import sound_engine
    sound_engine.shutdown()
