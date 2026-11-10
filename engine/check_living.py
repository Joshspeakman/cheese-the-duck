"""Integration checks against the real game, isolated from all player saves."""
import os
import sys
import tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-living-check-')
os.environ['SDL_AUDIODRIVER']='dummy'
import copy
import json
import math
import time
from engine import host
from engine.living_world import LivingPond, PROJECTS, ITEMS, STORIES
from world.habitat import PlacedItem
from world.crafting import Tool
from world.exploration import AREAS
from engine.scene import snapshot
sys.stdout=host.WIRE
checks=[]
def check(value,name):
    assert value,name
    checks.append(name)
terminal=host.DesktopInput()
g=host.DesktopGame(terminal=terminal,renderer_factory=host.CanvasRenderer)
terminal.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
    g._running=True;g._start_new_game();g._flush_pending_save()
    g.duck.growth_stage='adult';g.duck.current_action=None;g.renderer._show_talk=False;g._state='playing'
    p=g.living_pond;p.state['auto']=False
    for need in ('hunger','energy','fun','cleanliness','social'):g.duck_store.set_need(need,65)
    g.duck_store.sync_to_duck(g.duck)
    check(len(ITEMS)==542,'all item profiles exported')
    for item in ITEMS.values():check(item['kind'] and item['skill'],'profile '+item['id'])
    g.habitat.owned_items.extend(['toy_ball','fountain_grand','hat_chef','nook_radio'])
    g.habitat.placed_items.append(PlacedItem('toy_ball',3,4))
    g.outfits.owned_items.append('wizard_hat')
    g.seasonal_clothing.wardrobe.owned_items.append('winter_earmuffs')
    g.decorations.owned_decorations['fountain']=1
    g.decorations.place_decoration('fountain','pond',(0,0))
    p.sync()
    check('wizard_hat' in p.owned and 'winter_earmuffs' in p.owned,'all wardrobe registries retained in belongings')
    check('fountain' in p.placed and 'fountain' in p.owned,'outdoor room decorations retain ownership and world position')
    before=copy.deepcopy(p.state)
    check(not p.start('item','robot_butler')[0],'unowned item rejected')
    check(p.state==before,'invalid command causes no state changes')
    check(p.start('item','toy_ball')[0],'owned object usable')
    check(not p.start('forage')[0],'concurrent activities rejected')
    p.advance(4)
    check(p.state['objects']['toy_ball']['uses']==0,'cannot operate distant items before arriving')
    destination=p.state['plan'].get('destination')
    if destination:g.renderer.duck_pos.x,g.renderer.duck_pos.y=map(round,destination)
    before=copy.deepcopy(p.state)
    for _ in range(40):json.dumps(p.snapshot())
    check(p.state==before,'snapshots do not advance or mutate world')
    p.advance(30)
    check(p.state['objects']['toy_ball']['uses']==1,'item use completes once')
    p.advance(30)
    check(p.state['objects']['toy_ball']['uses']==1,'completion not replayed')
    check(p.state['objects']['toy_ball']['condition']<1,'use changes physical condition')
    check(not p.start('item','hat_chef')[0],'wearables use authoritative wardrobe')
    check(p.start('observe')[0],'observation starts')
    p.advance(6);saved=p.save();reloaded=LivingPond(saved);reloaded.attach(g,offline=False)
    check(reloaded.state['plan']['paused'],'in-flight action pauses on reload')
    knowledge=copy.deepcopy(reloaded.state['knowledge']);reloaded.advance(200,offline=True)
    check(reloaded.state['knowledge']==knowledge,'offline time never completes player rewards')
    check(reloaded.state['plan']['paused'],'offline plan stays paused')
    p.cancel();check(p.state['plan'] is None,'activity cancels')
    for key in PROJECTS:
        cost=PROJECTS[key]['stages'][0][1]
        check(not p.start('project',key)[0],'project requires materials '+key)
        for material,amount in cost.items():g.materials.add_material(material,amount)
        before=g.materials.get_all_materials().copy()
        check(p.start('project',key)[0],'project starts '+key)
        p.advance(100)
        check(p.state['projects'][key]['stage']==1,'project stage completes '+key)
        for material,amount in cost.items():check(g.materials.get_count(material)==before[material]-amount,'project consumes exact cost '+key+material)
    # Repair works on the original crafted tool, not just a decorative meter.
    g.crafting.tools['stone_hammer']=Tool('stone_hammer','Stone Hammer',durability=30)
    g.materials.add_material('twig',1);p.sync();p._legacy_links(1)
    check(p.start('repair_item','stone_hammer')[0],'damaged tool repair starts')
    p.advance(30)
    check(g.crafting.tools['stone_hammer'].durability==55,'repair restores actual crafted tool durability')
    # Real gardens share rainfall and the journal uses actual seed ownership.
    ok,_=g.garden.plant_seed(0,'carrot_seeds');check(ok,'original garden accepts starting seed')
    plant=g.garden.plots[0].plant;plant.water_level=20
    p.state['weather'][p.biome]={'type':'rainy','until':p.state['elapsed']+1000,'forecast':[{'type':'sunny','duration':300,'intensity':.4}],'front':99,'intensity':1}
    p.advance(60);check(plant.water_level>20,'rain waters actual garden')
    check(p.state['objects']['toy_ball']['wetness']>0,'rain wets placed items')
    check(p.state['objects']['hat_chef']['wetness']==0,'stored wardrobe remains dry')
    check(g.fishing.habitat_activity>.65,'fish habitat affects bite timing')
    # Original visitors retain their established friendship ledger.
    friend=g.friends.generate_new_friend();p.sync();g.friends.start_visit(friend.id)
    p.command({'action':'promise','target':friend.id})
    prior=friend.friendship_points
    check(p.start('share',friend.id)[0],'shared activity validates present visitor')
    p.advance(35)
    check(friend.friendship_points>prior,'shared activity uses original friendship progression')
    check(p.state['promises'][-1]['status']=='kept','shared activity fulfils promise')
    check(p.state['friends'][friend.id]['memories'],'friend retains specific shared memories')
    check(not p.start('share',friend.id)[0],'friendship cannot be click-farmed')
    # Every branching scene can complete and stale commands never apply twice.
    for story_id,story in STORIES.items():
        p.state['story']={'id':story_id,'step':0,'choices':[]}
        for step,scene in enumerate(story['scenes']):
            choice=scene['choices'][0]
            for material,amount in choice.get('cost',{}).items():g.materials.add_material(material,amount)
            token=f'{story_id}:{step}:{choice["id"]}'
            p.choose_story(token);before=json.dumps(p.state,sort_keys=True)
            p.choose_story(token);check(json.dumps(p.state,sort_keys=True)==before,'stale choice rejected '+token)
        check(story_id in p.state['stories'],'story completes '+story_id)
    # Forced event transport includes the original event animator and camera.
    g._start_event_animation('butterfly');g.renderer.render_frame(g)
    frame=snapshot(g,g.renderer)
    check(any(e['id']=='butterfly' for e in frame['events']),'Ultra receives original animated events')
    check(frame['living']['garden'][0]['plant']=='carrot','garden snapshot shows actual plant')
    # Saving preserves all original systems plus the extension in one atomic file.
    g._save_game();g._flush_pending_save();path=g.save_manager.save_path
    data=json.loads(path.read_text());check('living_pond' in data and len(data)>=60,'full atomic save retains original sections')
    g._load_game();check(g.living_pond.state['stories']==p.state['stories'],'stories survive real save/load')
    check(g.living_pond.state['objects']['toy_ball']['uses']==1,'object history survives real save/load')
    # Simulate migration by removing only the optional extension.
    data.pop('living_pond');g.save_manager.save(data);g._load_game()
    check(g.living_pond and not g.living_pond.state['stories'],'old saves gain fresh optional state')
    check('toy_ball' in g.habitat.owned_items,'migration preserves original ownership')
    # Deterministic long-running ecology: bounded values, stocks, histories and no rewards.
    g.living_pond.state['auto']=False;g.living_pond.sync();base=g.living_pond.save()
    a=LivingPond(base);b=LivingPond(base)
    for sim in (a,b):
        sim.attach(g,offline=False)
        for i in range(864):
            sim.hour=(i/36)%24
            sim.advance(300,offline=True)
    ea,eb=a.state['ecology'],b.state['ecology']
    check(ea==eb,'72-hour ecology is deterministic')
    check(all(math.isfinite(v) and (0<=v<=1 if k!='temperature' else -40<=v<=50) for k,v in ea.items()),'72-hour climate stays finite and bounded')
    check(all(0<=v<=12 for v in a.state['stocks'].values()),'forage patches remain bounded')
    check(a.state['skills']==base['skills'],'offline simulation awards no unearned skill')
    check(len(a.state['journal'])<=120 and len(a.state['promises'])<=24,'histories bounded during long run')
    # Export a populated fixture for UI/art verification only.
    g.living_pond=p;p.game=g;p.sync();p.state['story']={'id':'lost_duckling','step':0,'choices':[]};p._cache=None
    for key in p.state['projects']:p.state['projects'][key]['stage']=2
    g.renderer.render_frame(g)
    fixture=snapshot(g,g.renderer)
    fixture['duck']['stage']='adult';fixture['duck']['hidden']=False
    out=ROOT/'engine/artifacts/overhaul';out.mkdir(exist_ok=True)
    (out/'scene.json').write_text(json.dumps(fixture))
    report={'result':'PASS','checks':len(checks),'long_run_hours':72,'save_sections':len(data)+1,'stories':len(STORIES),'item_profiles':len(ITEMS),'details':checks}
    (out/'simulation-checks.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k!='details'}))
finally:
    if hasattr(g,'_save_executor'):g._save_executor.shutdown(wait=True)
    from audio.sound import sound_engine
    sound_engine.shutdown()
    if hasattr(g,'_talk_executor'):g._talk_executor.shutdown(wait=False)
