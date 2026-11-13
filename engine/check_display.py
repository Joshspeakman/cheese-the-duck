"""Display spots: show only owned collectibles, one place at a time, capacity,
auto-removal when no longer owned, save/reload. Disposable saves only."""
import os, sys, tempfile, json, copy
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ['CHEESE_SAVE_DIR'] = tempfile.mkdtemp(prefix='cheese-display-')
os.environ['SDL_AUDIODRIVER'] = 'dummy'
from engine import host, display as D, repertoire as R
from world.habitat import PlacedItem
from audio.sound import sound_engine
sys.stdout = host.WIRE
checks = []
def check(ok, label):
    assert ok, label
    checks.append(label)
t = host.DesktopInput(); g = host.DesktopGame(terminal=t, renderer_factory=host.CanvasRenderer); t.game = g; g.renderer.game = g; g.renderer.present = lambda l: None
try:
    g._running = True; g._start_new_game(); g._flush_pending_save(); g._state = 'playing'; sound_engine.enabled = False
    p = g.living_pond; p.state['auto'] = False
    g.habitat.owned_items = ['trophy_case', 'cabinet']; g.habitat.placed_items = [PlacedItem('trophy_case', 10, 6), PlacedItem('cabinet', 3, 2)]
    check(g.collectibles.collect('portrait_cheese', 'test'), 'a real collectible card is collected')
    g.materials.add_material('golden_badge', 1)
    p.sync()
    case = next(x.instance for x in p.placements if x.item_id == 'trophy_case'); cab = next(x.instance for x in p.placements if x.item_id == 'cabinet')
    check('portrait_cheese' in p.owned, 'owned collectible cards now count as owned at the pond')
    before = copy.deepcopy((g.inventory.to_dict(), g.materials.get_all_materials(), g.habitat.currency, dict(g.collectibles.owned)))
    def cmd(target, inst, text):
        p.command({'action': 'display_action', 'target': target, 'instance': inst, 'text': text}); return D.state(p.object_state(target, inst))
    d = cmd('trophy_case', case, 'show:portrait_cheese')
    check(d['items'] == ['portrait_cheese'], 'the card goes on the trophy case')
    d2 = cmd('cabinet', cab, 'show:portrait_cheese')
    check(d2['items'] == [], 'one thing is displayed in one place at a time')
    d = cmd('trophy_case', case, 'show:legend_dragon')
    check('legend_dragon' not in d['items'], 'something not owned cannot be displayed')
    d = cmd('trophy_case', case, 'show:golden_badge')
    check(d['items'] == ['portrait_cheese', 'golden_badge'], 'an owned badge joins it')
    check(copy.deepcopy((g.inventory.to_dict(), g.materials.get_all_materials(), g.habitat.currency, dict(g.collectibles.owned))) == before, 'displaying consumes and creates nothing')
    g.materials.materials.pop('golden_badge', None) if hasattr(g.materials, 'materials') else None
    if 'golden_badge' in g.materials.get_all_materials():
        g.materials.remove_material('golden_badge', 1)
    p.sync()
    check(D.state(p.object_state('trophy_case', case))['items'] == ['portrait_cheese'], 'a badge no longer owned leaves the shelf')
    for x in sorted(R.displayable())[:12]:
        if not g.collectibles.collect(x, 'test'):
            g.materials.add_material(x, 1)
    p.sync()
    for x in sorted(R.displayable()):
        cmd('trophy_case', case, 'show:' + x)
    check(len(D.state(p.object_state('trophy_case', case))['items']) == 8, 'the trophy case holds eight')
    saved = copy.deepcopy(D.state(p.object_state('trophy_case', case)))
    g._save_game(); g._flush_pending_save(); g._load_game(); p = g.living_pond; p.sync()
    check(D.state(p.object_state('trophy_case', case)) == saved, 'the display survives save and reload')
    print(json.dumps(dict(result='PASS', checks=len(checks))))
finally:
    g.living_pond.minds.close(); g._save_executor.shutdown(wait=True); sound_engine.shutdown()
