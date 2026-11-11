"""Reachability, weather waiting, interruption and persistence in a disposable game."""
import os
import sys
import tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ['CHEESE_SAVE_DIR'] = tempfile.mkdtemp(prefix='cheese-shelters-')
os.environ['SDL_AUDIODRIVER'] = 'dummy'
import copy
import json
from engine import host, shelters
from engine.living_world import LivingPond
from world.habitat import PlacedItem
sys.stdout = host.WIRE
checks = []
def check(ok, message):
    assert ok, message
    checks.append(message)
t = host.DesktopInput()
g = host.DesktopGame(terminal=t, renderer_factory=host.CanvasRenderer)
t.game = g; g.renderer.game = g; g.renderer.present = lambda lines: None
try:
    g._running=True; g._start_new_game(); g._flush_pending_save()
    g._state='playing'; g.renderer._show_talk=False
    g.duck.growth_stage='adult'; g.duck.current_action=None
    p=g.living_pond; p.state['auto']=False
    for need in ('hunger','energy','fun','cleanliness','social'):
        g.duck_store.set_need(need,65)
    g.duck_store.sync_to_duck(g.duck)
    g.duck.growth_stage='adult'
    g.habitat.owned_items.extend(list(shelters.HOMES)+['birdhouse'])
    g.habitat.placed_items=[PlacedItem('cozy_nest',4,5),PlacedItem('wooden_cottage',10,5),PlacedItem('treehouse',15,5),PlacedItem('birdhouse',3,5)]
    p.sync(); pos=g.renderer.duck_pos; pos.x=8;pos.y=20
    p.weather_type='rainy'
    check([c['id'] for c in shelters.candidates(p)]==['wooden_cottage','treehouse'],'rain excludes uncovered nests and wildlife birdhouses: '+str((p.location,g.duck.growth_stage,shelters.candidates(p))))
    g.duck.growth_stage='hatchling'
    check([c['id'] for c in shelters.candidates(p)]==['wooden_cottage'],'hatchlings use ground-level roofed shelters')
    for stage in shelters.AGES:
        g.duck.growth_stage=stage
        choices=shelters.candidates(p)
        check(not choices if stage=='egg' else bool(choices),'shelter suitability '+stage)
    g.duck.growth_stage='adult'
    # start() synchronizes from the live weather, just as real input does.
    from world.atmosphere import WeatherType, Weather
    from datetime import datetime
    g.atmosphere.current_weather=Weather(WeatherType.RAINY,.7,1,datetime.now().isoformat())
    check(p.start('rest')[0],'a real roofed resting plan starts')
    plan=p.state['plan']; check(plan['target']=='wooden_cottage','nearest reachable roof selected')
    p._activity(5)
    check(plan['elapsed']==0 and not plan['residence'].get('inside'),'distant Cheese cannot appear inside a house')
    # Walk using the actual directed animator rather than teleporting the fixture.
    travelled=[]
    for _ in range(600):
        pos.update(.2);p._activity(.2);travelled.append((pos.x,pos.y))
        if plan['phase']=='act':break
    check(len(set(travelled))>10,'shelter arrival walks through intermediate positions')
    check(plan['phase']=='act' and plan['residence']['inside'],'actual arrival enters the resting place')
    before=p.state['objects']['wooden_cottage']['uses']
    for _ in range(60):p._activity(5)
    check(p.state['plan'] is plan and plan['residence']['holding'],'Cheese stays under cover while it rains')
    check(plan['residence']['restored']<=10,'long storm rest has bounded actual need recovery')
    check(p.state['objects']['wooden_cottage']['uses']==before,'waiting does not repeatedly award completion')
    saved=p.save(); reloaded=LivingPond(saved); reloaded.attach(g,offline=False)
    check(reloaded.state['plan']['paused'],'saved occupancy pauses until deliberately resumed')
    p.weather_type='sunny';p._activity(10)
    check(p.state['plan'] is None,'clear weather releases the rest once')
    check(p.state['objects']['wooden_cottage']['uses']==before+1,'one shelter visit records one use')
    p.state['cooldowns'].clear();p.weather_type='rainy'
    check(p.start('rest','wooden_cottage')[0],'explicit shelter visit starts')
    pos.x,pos.y=p.state['plan']['destination'];p._activity(9)
    g.habitat.placed_items=[i for i in g.habitat.placed_items if i.item_id!='wooden_cottage'];p.sync();p._activity(1)
    check(p.state['plan'] is None,'removing a shelter releases its occupant without completion')
    check(p.state['objects']['wooden_cottage']['uses']==before+1,'removed shelter earns no extra use')
    check(not p.start('rest','birdhouse')[0],'a wildlife birdhouse cannot imprison Cheese')
    check(not p.start('rest','cozy_nest')[0],'explicit open nest does not pretend to be rain cover')
    g.habitat.placed_items.append(PlacedItem('wooden_cottage',10,5));p.sync();p.state['cooldowns'].clear()
    p.decide()
    check(p.state['plan']['residence']['roof'],'autonomous bad-weather choice seeks a real roof')
    p.cancel();check(p.state['plan'] is None and not pos._is_directed_movement,'user cancellation clears travel and occupancy')
    # Both copies must remain distinguishable by destination.
    g.habitat.placed_items.append(PlacedItem('wooden_cottage',2,5));p.sync();pos.x=10;pos.y=18
    check(shelters.candidates(p,'wooden_cottage')[0]['destination'][0]==13,'duplicate homes choose the nearest actual placement')
    result={'result':'PASS','checks':len(checks),'details':checks}
    (ROOT/'engine/artifacts/animation-milestone/shelter-simulation.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({'result':'PASS','checks':len(checks)}))
finally:
    if hasattr(g,'_save_executor'):g._save_executor.shutdown(wait=True)
    from audio.sound import sound_engine
    sound_engine.shutdown()
    if hasattr(g,'_talk_executor'):g._talk_executor.shutdown(wait=False)
