"""Serve native frames for journal UI checks (disposable saves). stdin JSON lines:
{type:'test_fixture', item}, {type:'test_advance', until:'finish'|n}, pond commands, {type:'quit'}."""
import os, sys, tempfile, json
from pathlib import Path
from datetime import datetime
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ['CHEESE_SAVE_DIR'] = tempfile.mkdtemp(prefix='cheese-ui-fixture-')
os.environ['SDL_AUDIODRIVER'] = 'dummy'
from engine import host, keeping as K, display as D, repertoire as R
from engine.scene import snapshot
from world.habitat import PlacedItem
from world.fishing import CaughtFish, FishingSpot, BaitType
from world.atmosphere import Weather, WeatherType, Season
from audio.sound import sound_engine
sys.stdout = host.WIRE
t = host.DesktopInput(); g = host.DesktopGame(terminal=t, renderer_factory=host.CanvasRenderer); t.game = g; g.renderer.game = g; g.renderer.present = lambda l: None
g._running = True; g._start_new_game(); g._flush_pending_save(); g._state = 'playing'; sound_engine.enabled = False
g.renderer._viewport_width = 132; g.renderer._viewport_height = 42; g.renderer._update_camera(132, 42)
p = g.living_pond; p.state['auto'] = False; p.minds.model.state['next_social'] = 1e9
g.duck.growth_stage = 'adult'; g.duck.needs.energy = g.duck.needs.hunger = g.duck.needs.fun = 95; g.duck_store.sync_from_duck(g.duck)
g.day_night.get_current_hour = lambda: 12; g.day_night.get_current_minute = lambda: 0
g.atmosphere.current_season = Season.SPRING; g.atmosphere.current_weather = Weather(WeatherType.SUNNY, .5, 1, datetime.now().isoformat())
item = None
_notice = p.notice
def _echo(text):
    sys.stderr.write('NOTICE ' + str(text) + '\n'); return _notice(text)
p.notice = _echo
def emit():
    p._cache = None
    copies = [a.instance for a in p.placements if a.item_id == item]
    sys.__stdout__.write(json.dumps(dict(type='physical_frame', frame=dict(scene=snapshot(g, g.renderer), copies=copies, item=item))) + '\n'); sys.__stdout__.flush()
def fixture(name):
    global item
    p.cancel(); item = name
    g.habitat.stored_items, g.habitat.stored_placements = [], []
    if name == 'koi_pond':
        c = CaughtFish('koi', 42., '2026-05-01T10:00:00', FishingSpot.POND, BaitType.BREAD, False)
        g.fishing.fish_caught['koi'] = [c]; g.habitat.owned_items = ['koi_pond']; g.habitat.placed_items = [PlacedItem('koi_pond', 10, 6)]; p.sync()
    elif name == 'trophy_case':
        g.collectibles.collect('portrait_cheese', 'test'); g.habitat.owned_items = ['trophy_case']; g.habitat.placed_items = [PlacedItem('trophy_case', 10, 6)]; p.sync()
    elif name == 'scarf_red':
        g.habitat.owned_items, g.habitat.placed_items = [], []
        if 'scarf_red' not in g.outfits.owned_items: g.outfits.owned_items.append('scarf_red')
        p.sync()
    else:
        g.habitat.owned_items = [name]; g.habitat.placed_items = [PlacedItem(name, 10, 6)]; p.sync()
    pos = g.renderer.duck_pos; pos.cancel_movement(); pos.x, pos.y = 36, 21
    for o in [*p.state['instances'].values(), *p.state['objects'].values()]: o['last_use'] = -1000
def step(n=1):
    for _ in range(n):
        p.state['elapsed'] += .2; pos = g.renderer.duck_pos; pos._state_start_time -= .2; pos.update(.2); p._activity(.2)
try:
    fixture('gong'); emit()
    for line in sys.stdin:
        c = json.loads(line)
        if c.get('type') == 'quit': break
        if c.get('type') == 'test_fixture': fixture(c['item'])
        elif c.get('type') == 'test_advance':
            if c.get('until') == 'finish':
                for _ in range(3000):
                    if not p.state['plan']: break
                    step()
            else: step(int(c.get('until') or 1))
        elif c.get('type') == 'pond': p.command(c); p.sync()
        emit()
finally:
    g.living_pond.minds.close(); g._save_executor.shutdown(wait=True); sound_engine.shutdown()
