"""Capture real menu routes for desktop UI verification, using disposable saves."""
import os
import sys
import tempfile
import json
from types import SimpleNamespace
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ['CHEESE_SAVE_DIR'] = tempfile.mkdtemp(prefix='cheese-interface-')
os.environ['SDL_AUDIODRIVER'] = 'dummy'
from engine import host
from ui.menu_structure import MENU_ACTIONS
from audio.sound import sound_engine

frames = {}
latest = None
def submit(frame):
    global latest
    latest = frame
host.send = submit
terminal = host.DesktopInput()
game = host.DesktopGame(terminal=terminal, renderer_factory=host.CanvasRenderer)
terminal.game = game
game.renderer.game = game
game._running = True
game._state = 'title'
game._terminal_options = []

def capture(name):
    # Persistent menu routes compose their content after the first frame.
    for _ in range(2):
        game.renderer.last_sent = 0
        game._render()
    assert latest and latest['type'] == 'frame', name
    frames[name] = latest

def close():
    game._confirmation_dialog = None
    game._close_all_menus()
    game.renderer.hide_overlays()
    game.renderer.dismiss_celebration()

try:
    capture('title')
    game._start_new_game()
    game.duck.growth_stage = 'adult'
    game.habitat.currency = 1234
    for name in ('hunger', 'energy', 'fun', 'cleanliness', 'social'):
        setattr(game.duck.needs, name, 82)
    close()
    capture('pond')
    game.renderer.show_celebration('level_up', 'Cheese reached level 2!', duration=60)
    capture('celebration')
    close()
    from ui.ascii_art import get_mini_duck
    game._start_item_interaction_animation('test_bread', SimpleNamespace(
        animation_frames=[get_mini_duck('adult', 'eating', True, 0)], duration=5,
        message='Cheese is enjoying the bread.'))
    capture('item-interaction')
    game._item_interaction_active = False
    close()
    for action in MENU_ACTIONS:
        if action in ('reset_game', 'quit', 'nook_radio_toggle', 'sleep'):
            continue
        close()
        game._execute_menu_action(action)
        capture(action)
    close()
    game._execute_menu_action('settings')
    for category in game._settings_menu._categories:
        game._settings_menu._current_category = category
        game._settings_menu._load_category_items()
        game._settings_menu._category_index = game._settings_menu._categories.index(category)
        game._render_settings_menu()
        capture('settings-' + category.value)
    game._show_reset_settings_prompt()
    capture('confirmation')
    close()
    for tab in ('overview', 'journal', 'emotions', 'photos', 'dreams', 'life'):
        game._enhanced_diary_tab = tab
        game._render_enhanced_diary()
        capture('diary-' + tab)
    close()
    for name in ('bread_catch', 'bug_chase', 'memory_match', 'duck_race'):
        game._start_minigame(name)
        game._update_minigame()
        capture(name)
        game._end_minigame(abandoned=True)
        close()
    game._execute_menu_action('talk')
    game.renderer._talk_buffer = 'What the fuck, Cheese? ' + 'Keep every character. ' * 9
    capture('long-talk')
    close()
    game._state = 'offline_summary'
    game.renderer.last_sent = 0
    game.renderer.render_offline_summary('Cheese', 3, {'hunger': -12, 'energy': 15}, ['Cheese watched the clouds.'])
    frames['offline'] = latest
    game._state = 'ai_loading'
    game.renderer.last_sent = 0
    game.renderer.render_loading_screen('Waking up the pond...', 'Getting Cheese ready')
    frames['loading'] = latest
    game._state = 'title'
    game.renderer.last_sent = 0
    game.renderer._render_title_screen(menu_index=1, has_save=True, update_status='Start new game? This will ERASE your save! [Y/N]')
    frames['title-confirmation'] = latest
    out = ROOT / 'engine/artifacts/interface-frames.json'
    out.write_text(json.dumps(frames))
    print(json.dumps({'frames': len(frames), 'out': str(out)}), file=host.WIRE)
finally:
    if hasattr(game, '_save_executor'): game._save_executor.shutdown(wait=True)
    if hasattr(game, '_talk_executor'): game._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
