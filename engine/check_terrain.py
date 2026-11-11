"""Real portable activities stay on suitable ground, through travel and saves."""
import os,sys,tempfile,json,copy
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-terrain-')
os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,portable_ground as pg,terrain,object_history
from engine.pond_layout import bounds,overlaps
from engine.scene import snapshot
from world.exploration import AREAS
from world.atmosphere import Weather,WeatherType,Season
from audio.sound import sound_engine
sys.stdout=host.WIRE
checks=[];reviews=[]
def check(ok,label):
    assert ok,label
    checks.append(label)
t=host.DesktopInput();g=host.DesktopGame(terminal=t,renderer_factory=host.CanvasRenderer)
t.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
    g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.renderer._show_talk=False;sound_engine.enabled=False
    g.renderer._viewport_width=132;g.renderer._viewport_height=42;g.renderer._update_camera(132,42)
    g.duck.growth_stage='adult';g.duck.needs.energy=95;g.duck.needs.hunger=95;g.duck_store.sync_from_duck(g.duck)
    g.day_night.get_current_hour=lambda:12;g.day_night.get_current_minute=lambda:0
    g.atmosphere.current_season=Season.SPRING;g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.3,1,datetime.now().isoformat())
    p=g.living_pond;p.state['auto']=False;p.minds.model.state['next_social']=1e9
    g.habitat.owned_items=[];g.habitat.placed_items=[];g.habitat.stored_placements=[];g.habitat.stored_items=[];g.building.structures=[]
    for room in g.decorations.rooms.values():room.decorations=[]
    areas={a.name:a for group in AREAS.values() for a in group}
    check(set(areas)==set(terrain.REGIONS),'terrain covers every original area')
    pos=g.renderer.duck_pos
    for name,area in areas.items():
        g.exploration.current_area=area;p.sync();pos.cancel_movement();pos.x=65;pos.y=35
        items=[]
        for item in ('toy_ball','couch','bubble_wand','tiny_boat','lily_pad','bridge','jump_rope','picture_frame'):
            site=pg.choose(p,item);layout=pg.policy(p)
            if site:
                point=site['object'];box=bounds(item,point[0]*20/132,point[1]*12/42)['ground']
                check(pg.point_ok(layout,item,point),name+': '+item+' has clear ground and approach')
                check(terrain.surface_fits(item,box,name,area.biome.value),name+': '+item+' support matches terrain')
                check(all(not overlaps(box,f['box']) for f in layout.features),name+': '+item+' clears fixed scenery')
                items.append(dict(id=item,x=point[0],y=point[1]))
            else:
                check(not any(pg.point_ok(layout,item,[x/2*132/20,y/4*42/12]) for x in range(1,40) for y in range(4,43)),name+': unavailable '+item+' has no false fallback')
        # The review deliberately shows separate items in separate frames, so
        # identical nearest sites never create fake overlapping belongings.
        frame=snapshot(g,g.renderer);frame['items']=[];frame['structures']=[]
        reviews.append(dict(scene=frame,placements=items))
    g.exploration.current_area=areas['Home Pond'];p.sync()
    def ready(item):
        p.cancel();g.duck.current_action=None;g.behavior_ai.clear_action();pos.cancel_movement();pos.x=65;pos.y=35
        if item not in g.inventory.items:check(g.inventory.add_item(item),item+' is owned through the real inventory')
        p.sync();p.state['cooldowns']={};p.object_state(item)['last_use']=-1000
        p.state['ecology'].update(temperature=18,wind=.2)
    def step():
        p.state['elapsed']+=.2;pos._state_start_time-=.2;pos.update(.2);p._activity(.2)
    ready('bubble_wand');before=p.object_state('bubble_wand')['uses'];ok,msg=p.start('item','bubble_wand');check(ok,msg)
    plan=p.state['plan'];site=copy.deepcopy(plan['portable']);work=plan['playkit_work']
    check(not terrain.water_at('Home Pond',*site['object']),'portable dry toy leaves the water for dry ground')
    p._activity(1);check(work['elapsed']==0 and p.object_state('bubble_wand')['uses']==before,'no work or reward before arrival')
    p.sync();check(p.state['plan'] is plan and p.object_state('bubble_wand',plan) is p.object_state('bubble_wand'),'walking destination does not turn a portable item into a placed copy')
    for _ in range(900):
        step()
        if work['elapsed']>1:break
    check(work['elapsed']>1,'Cheese actually walks to the site and starts work')
    check(plan['portable']['deployed'],'arrival puts the real prop down')
    site=copy.deepcopy(plan['portable'])
    check(pg.reservation(p) is not None,'active temporary object reserves its ground')
    x,y=site['object'];check(not p.layout.check('toy_ball',x*20/132,y*12/42)[0],'permanent placement cannot land on a portable activity')
    plan['paused']=True;saved_clock=work['elapsed'];p._activity(10)
    check(work['elapsed']==saved_clock,'paused work clock stays still')
    g.exploration.current_area=areas['Sunny Meadow'];p.sync();p.command({'action':'resume'})
    check(plan['paused'] and plan['portable']==site,'travel leaves the unfinished object at its original location')
    g.exploration.current_area=areas['Home Pond'];p.sync()
    g._save_game();g._flush_pending_save();g._load_game();p=g.living_pond;p.sync();pos=g.renderer.duck_pos
    plan=p.state['plan'];check(plan and plan['paused'] and plan['portable']==site and plan['playkit_work']['elapsed']==saved_clock,'save/reload preserves the portable reservation and exact routine clock')
    pos.cancel_movement();pos.x=65;pos.y=35;p.command({'action':'resume'});p._activity(.2)
    check(plan['phase']=='approach' and plan['playkit_work']['elapsed']==saved_clock,'resuming walks back before further contacts')
    for _ in range(1200):
        step()
        if not p.state['plan']:break
    check(not p.state['plan'] and plan['playkit_work']['done'] and p.object_state('bubble_wand')['uses']==before+1,'resumed portable routine completes exactly once')
    check(pg.reservation(p) is None,'completion releases temporary ground')
    ready('bubble_wand');check(p.start('item','bubble_wand')[0],'portable routine starts again after cooldown fixture reset')
    p.state['plan']['paused']=True;before=p.object_state('bubble_wand')['uses'];g.inventory.remove_item('bubble_wand');p.sync()
    check(not p.state['plan'] and pg.reservation(p) is None and p.object_state('bubble_wand')['uses']==before,'losing a paused item releases its prop without reward')
    ready('tiny_boat');check(p.start('item','tiny_boat')[0],'toy boat starts at a suitable water spot')
    plan=p.state['plan'];check(terrain.water_at('Home Pond',*plan['portable']['object']),'toy boat is put on water')
    p.cancel();g.exploration.current_area=areas['Sunny Meadow'];p.sync()
    before=copy.deepcopy((g.inventory.to_dict(),p.state['objects'],g.habitat.currency))
    check(not p.start('item','tiny_boat')[0],'dry meadow refuses a water-only toy instead of drawing fake water')
    check(before==(g.inventory.to_dict(),p.state['objects'],g.habitat.currency),'failed placement costs no object, condition or currency')
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
    (out/'terrain-native.json').write_text(json.dumps(dict(result='PASS',checks=checks),indent=2))
    (out/'terrain-review-frames.json').write_text(json.dumps(reviews))
    print(json.dumps(dict(result='PASS',checks=len(checks),areas=len(reviews))))
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
