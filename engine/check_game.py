"""Exercise the real game against the canvas backend, with a disposable save.
Run from the repository root: .venv/bin/python engine/check_game.py
"""
import os
import sys
import tempfile
import json
from pathlib import Path
root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
os.environ['CHEESE_SAVE_DIR'] = tempfile.mkdtemp(prefix='cheese-parity-')
os.environ['SDL_AUDIODRIVER'] = 'dummy'
from engine import host
from ui.menu_structure import MENU_ACTIONS
from world.exploration import AREAS
from engine.frame import line_runs
from engine.scene import snapshot
from audio.sound import sound_engine
sys.stdout = host.WIRE

frames = []
def submit(lines):
    frames.append([line_runs(line) for line in lines])

terminal = host.DesktopInput()
game = host.DesktopGame(terminal=terminal, renderer_factory=host.CanvasRenderer)
terminal.game = game
game.renderer.game = game
game.renderer.present = submit
game._running = True
game._start_new_game()
game.duck.growth_stage = 'adult'
for name in ('hunger', 'energy', 'fun', 'cleanliness', 'social'):
    setattr(game.duck.needs, name, 90)
checks = []
try:
    # Every non-destructive static menu route uses the real handler and compositor.
    for action in MENU_ACTIONS:
        if action in ('reset_game', 'quit', 'nook_radio_toggle', 'sleep'):
            continue
        game._close_all_menus()
        game.renderer.hide_overlays()
        game.renderer.dismiss_celebration()
        game._execute_menu_action(action)
        game._render()
        assert frames, action
        text = '\n'.join(''.join(r[0] for r in row) for row in frames[-1])
        assert 'Action not implemented:' not in text, action
        assert 'Game loop error' not in text, action
        checks.append('menu:' + action)
    game._close_all_menus()
    game.renderer.hide_overlays()
    for tab in ('overview','journal','emotions','photos','dreams','life'):
        game._enhanced_diary_tab = tab
        game._render_enhanced_diary()
        checks.append('diary:' + tab)
    game._close_all_menus()
    # Mouse toolbar commands route through the same action handlers on the game thread.
    terminal.commands.put({'action':'inventory'}); game._process_input()
    assert game.renderer.is_inventory_open()
    terminal.commands.put({'action':'talk'}); game._process_input()
    assert game.renderer.is_talking()
    assert not game.renderer.is_inventory_open()
    game._close_all_menus(); game.renderer.hide_overlays()
    checks.append('input:mouse-action-routing')
    # Every authored location, including gated areas, is rendered without altering unlock rules.
    for biome, areas in AREAS.items():
        for area in areas:
            game.exploration.current_area = area
            game.renderer.render_frame(game)
            assert len(frames[-1]) > 20
            scene = snapshot(game, game.renderer)
            assert scene['location'] == area.name
            assert scene['biome'] == area.biome.value
            assert scene['duck']['name'] == 'Cheese'
            json.dumps(scene)  # scene transport must remain JSON serializable
            checks.append('location:' + area.name)
    game.exploration.current_area = AREAS[next(iter(AREAS))][0]
    # Exercise the actual four minigame update/render/input lifecycles.
    for name in ('bread_catch','bug_chase','memory_match','duck_race'):
        game._start_minigame(name)
        assert game._active_minigame is not None, name
        game._update_minigame()
        game.renderer.render_frame(game)
        game._end_minigame(abandoned=True)
        checks.append('minigame:' + name)
    # Real desktop queue routes speech, editing and submission without censorship.
    game._close_all_menus(); game.renderer.hide_overlays()
    game._execute_menu_action('talk')
    for c in 'What the fuck, Cheese?':
        terminal.commands.put(host.Key(c)); game._process_input()
    assert game.renderer.get_talk_buffer() == 'What the fuck, Cheese?'
    terminal.commands.put(host.Key(*host.KEYS['Backspace'])); game._process_input()
    assert game.renderer.get_talk_buffer() == 'What the fuck, Cheese'
    terminal.commands.put(host.Key(*host.KEYS['Escape'])); game._process_input()
    checks.append('input:uncensored-talk-and-edit')
    # Save and reload the complete game through its normal serializer.
    game.habitat.currency = 1234
    game._save_game()
    game._flush_pending_save()
    save = json.loads(Path(os.environ['CHEESE_SAVE_DIR'], 'save.json').read_text())
    assert len(save) > 20
    game.habitat.currency = 0
    game._load_game()
    assert game.habitat.currency == 1234
    assert game.duck.name == 'Cheese'
    checks.append('persistence:full-save-reload')
    report = {'passed': len(checks), 'checks': checks, 'save_keys': sorted(save), 'frames': len(frames)}
    out = root / 'engine/artifacts/parity.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2))
    print(json.dumps({'passed':len(checks),'frames':len(frames),'report':str(out)}))
finally:
    if hasattr(game, '_save_executor'): game._save_executor.shutdown(wait=True)
    if hasattr(game, '_talk_executor'): game._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
