"""Standalone simulation host. JSON commands in, structured glyph frames out."""
import os
import sys
from pathlib import Path

if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()

ROOT = Path(__file__).resolve().parent.parent
if not getattr(sys, 'frozen', False):
    sys.path.insert(0, str(ROOT))
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
os.environ['TERM'] = 'xterm-256color'
os.environ.pop('NO_COLOR', None)
os.environ['COLORTERM'] = 'truecolor'
os.environ.setdefault('CHEESE_SAVE_DIR', str(ROOT / 'engine' / '.runtime' / 'saves'))

import json
import queue
import threading
import time
import traceback
from contextlib import nullcontext

WIRE = sys.stdout
sys.stdout = sys.stderr  # Libraries/logs never share the frame protocol.
from blessed import Terminal
from engine.frame import line_runs
from engine.scenery import Landscape
from engine.scene import snapshot, overlay_bounds
from engine.interface import snapshot as interface_snapshot, composed_modal
from ui.renderer import Renderer
from core.game import Game

COLS, ROWS = 144, 52
ACTIONS = {'feed','play','clean','pet','sleep','talk','explore','shop','craft','build','inventory','help'}

class Key(str):
    def __new__(cls, value='', name=None):
        obj = super().__new__(cls, value)
        obj.name = name
        obj.is_sequence = name is not None
        obj.code = None
        return obj

KEYS = {'ArrowUp': ('\x1b[A', 'KEY_UP'), 'ArrowDown': ('\x1b[B', 'KEY_DOWN'),
        'ArrowRight': ('\x1b[C', 'KEY_RIGHT'), 'ArrowLeft': ('\x1b[D', 'KEY_LEFT'),
        'Enter': ('\r', 'KEY_ENTER'), 'Escape': ('\x1b', 'KEY_ESCAPE'),
        'Backspace': ('\x7f', 'KEY_BACKSPACE'), 'Tab': ('\t', 'KEY_TAB'),
        'PageUp': ('\x1b[5~', 'KEY_PPAGE'), 'PageDown': ('\x1b[6~', 'KEY_NPAGE'),
        'Home': ('\x1b[H', 'KEY_HOME'), 'End': ('\x1b[F', 'KEY_END'),
        'Delete': ('\x1b[3~', 'KEY_DELETE')}

class DesktopInput(Terminal):
    """Style vocabulary plus a command queue; never opens a terminal or PTY."""
    def __init__(self):
        super().__init__(kind='xterm-256color', force_styling=True, stream=sys.stderr)
        self.commands = queue.Queue(maxsize=4096)
        self.stopping = False
        self.game = None
    @property
    def width(self): return COLS
    @property
    def height(self): return ROWS
    def fullscreen(self): return nullcontext()
    def cbreak(self): return nullcontext()
    def hidden_cursor(self): return nullcontext()
    def inkey(self, timeout=None, **kwargs):
        if self.stopping:
            if self.game and self.game._running:
                self.game._quit('desktop window closed')
            return Key()
        try:
            key = self.commands.get(timeout=min(timeout or 0, .01))
            if self.game:
                self.game.renderer.dismiss_celebration()
                if isinstance(key, dict):
                    if key.get('type') == 'pond':
                        if self.game._state == 'playing' and self.game.living_pond and not (self.game._confirmation_dialog and self.game._confirmation_dialog.is_open):
                            self.game.living_pond.command(key)
                        return Key()
                    if key.get('type') == 'choose':
                        return self.choose(key)
                    if self.game._state == 'playing' and not (self.game._confirmation_dialog and self.game._confirmation_dialog.is_open):
                        self.game._close_all_menus()
                        self.game.renderer.hide_overlays()
                        self.game._execute_menu_action(key['action'])
                    return Key()
            return key
        except queue.Empty: return Key()
    def choose(self, command):
        """Resolve clicks against the current menu on the game thread, then use Enter."""
        game = self.game
        if command.get('target') == 'title' and game._state == 'title':
            title = game.renderer.interface_title
            if not title or getattr(game, '_title_confirm_new_game', False): return Key()
            index = command.get('index')
            if command.get('context') == '|'.join(title['options']) and type(index) is int and 0 <= index < len(title['options']):
                game._title_menu_index = index
                return Key(*KEYS['Enter'])
        elif command.get('target') == 'menu' and game._state == 'playing':
            renderer = game.renderer
            if (renderer.interface_modal or game._active_minigame or
                    (game._confirmation_dialog and game._confirmation_dialog.is_open)):
                return Key()
            items = game.master_menu._get_current_items()
            if command.get('context') != '|'.join(item.id for item in items): return Key()
            for index, item in enumerate(items):
                if item.id == command.get('id') and item.enabled:
                    game.master_menu._selected_index = index
                    return Key(*KEYS['Enter'])
        return Key()
    def read_commands(self):
        try:
            for raw in sys.stdin:
                try:
                    command = json.loads(raw)
                    kind = command.get('type')
                    if kind == 'shutdown': break
                    if kind == 'key':
                        key = command.get('key', '')
                        if key in KEYS: self.commands.put_nowait(Key(*KEYS[key]))
                        elif isinstance(key, str) and len(key) == 1: self.commands.put_nowait(Key(key))
                    elif kind == 'pond' and isinstance(command.get('action'), str):
                        self.commands.put_nowait(command)
                    elif kind == 'action' and command.get('action') in ACTIONS:
                        self.commands.put_nowait({'action': command['action']})
                    elif kind == 'choose' and command.get('target') in ('title', 'menu'):
                        self.commands.put_nowait(command)
                    elif kind == 'text':
                        for char in str(command.get('text', ''))[:1000]:
                            if char.isprintable(): self.commands.put_nowait(Key(char))
                except (ValueError, TypeError, queue.Full):
                    continue
        finally:
            self.stopping = True

def send(payload):
    WIRE.write(json.dumps(payload, ensure_ascii=False, separators=(',', ':')) + '\n')
    WIRE.flush()

class CanvasRenderer(Renderer):
    max_width, max_height = COLS, ROWS - 4
    def __init__(self, terminal):
        super().__init__(terminal)
        # The legacy renderer hard-coded six tabs, hiding four live registries.
        # Navigation and buying still use the original shop handlers.
        from world.shop import ItemCategory
        self._shop_categories = [category.name for category in ItemCategory]
        self.landscape = Landscape(terminal)
        self.last_sent = 0
        self.game = None
        self.sequence = 0
        self.scene_base = None
        self.scene_rect = None
        self.header_rows = 3
        self.interface_modal = None
        self.interface_title = None
        self.interface_chat = []
    def render_frame(self, game):
        self.interface_modal = None
        # Persistent menus refresh each tick; keep their confirmation in front.
        for dialog in (game._confirmation_dialog, game._error_dialog):
            if dialog and dialog.is_open:
                self.show_overlay('\n'.join(dialog.get_display_lines()))
                break
        return super().render_frame(game)
    def _render_title_screen(self, menu_index=0, has_save=False, **kwargs):
        self.interface_modal = None
        self.interface_title = {'selected': menu_index, 'hasSave': has_save,
                                'options': (['Continue'] if has_save else []) + ['New Game', 'Check for Updates', 'Quit'],
                                'status': kwargs.get('update_status', '')}
        return super()._render_title_screen(menu_index=menu_index, has_save=has_save, **kwargs)
    def _overlay_box(self, base_output, content, title, width):
        # Capture before the terminal compositor's 60-column/height truncation.
        self.interface_modal = {'title': title, 'lines': [line_runs(line) for line in content]}
        return super()._overlay_box(base_output, content, title, width)
    def _render_header_bar(self, *args, **kwargs):
        lines = super()._render_header_bar(*args, **kwargs)
        self.header_rows = len(lines)
        return lines
    def _render_playfield(self, duck, width, height=None, *args, **kwargs):
        lines = super()._render_playfield(duck, width, height, *args, **kwargs)
        self.scene_rect = {'x': 1, 'y': self.header_rows + 1, 'w': width - 2,
                           'h': height or self._viewport_height}
        self.interface_chat = lines[1 + self.scene_rect['h']:]
        return lines
    def capture_scene_base(self, lines):
        self.scene_base = list(lines)
    def _generate_ground_pattern(self, location=None):
        super()._generate_ground_pattern(location)
        # The new terrain layer owns ground detail. Preserve original landmarks.
        self._ground_pattern = [' ' * self.duck_pos.field_width for _ in range(self.duck_pos.field_height)]
    def detail_row(self, row, x, y, biome, season):
        seconds = time.monotonic() if self._show_animations else 0
        self.landscape.row(row, x, y, biome, season, seconds)
    def present(self, lines):
        now = time.monotonic()
        if now - self.last_sent < 1 / 30: return
        self.last_sent = now
        self.sequence += 1
        game = self.game
        state = game._state if game else 'loading'
        metadata = {'state': state, 'talking': self._show_talk}
        if game and game.duck:
            metadata.update(name=game.duck.name, stage=game.duck.growth_stage,
                            location=game.exploration.current_area.name if game.exploration.current_area else 'Home Pond')
        # Grow the frame when a tall original menu needs more rows; never cut off actions.
        rows = max(ROWS, len(lines))
        scene = None
        if state == 'playing' and game.duck and not game._active_minigame and self.scene_rect:
            scene = snapshot(game, self)
            scene['rect'] = self.scene_rect
            scene['overlay'] = overlay_bounds(self.scene_base or lines, lines)
            if scene['overlay'] and not self.interface_modal:
                self.interface_modal = composed_modal(lines, scene['overlay'])
        send({'type': 'frame', 'seq': self.sequence, 'cols': COLS, 'rows': rows,
              'lines': [line_runs(line) for line in lines], 'meta': metadata, 'scene': scene,
              'ui': interface_snapshot(game, self) if game else None})

class DesktopGame(Game):
    def __init__(self, *args, **kwargs):
        self.living_pond = None
        self._pond_duck = None
        super().__init__(*args, **kwargs)

    def _restore_living_pond(self, data):
        from engine.living_world import LivingPond
        self.living_pond = LivingPond(data)
        self._pond_duck = None

    def _ensure_living_pond(self, offline=False):
        if not self.duck:
            return
        if self.living_pond is None:
            from engine.living_world import LivingPond, stable
            self.living_pond = LivingPond(seed=stable(self.duck.created_at))
        if self._pond_duck is not self.duck:
            self.living_pond.attach(self, offline=offline)
            self._pond_duck = self.duck

    def _start_new_game(self):
        self.living_pond = None
        self._pond_duck = None
        super()._start_new_game()
        self._ensure_living_pond()
        self._save_game()

    def _load_game(self):
        super()._load_game()
        self._ensure_living_pond(offline=True)

    def _update(self):
        self._ensure_living_pond()
        super()._update()
        if self.living_pond:
            self.living_pond.tick()

    def _perform_interaction(self, interaction):
        if self.living_pond and self.living_pond.busy:
            self.living_pond.cancel()
        super()._perform_interaction(interaction)
        if self.living_pond and self.duck and self.duck.growth_stage != 'egg':
            self.living_pond.remember('care', 'You made time to '+interaction+' with Cheese.', .55)

    def _on_interaction_effects_applied(self, item_id, result):
        super()._on_interaction_effects_applied(item_id, result)
        if self.living_pond and result:
            self.living_pond.sync()
            obj = self.living_pond.state['objects'].get(item_id)
            if obj:
                obj['uses'] += 1
                obj['bond'] = min(1, obj['bond'] + .02)
                obj['last_use'] = self.living_pond.state['elapsed']

    def _generate_talk_response(self, message):
        # Snapshot context on the simulation thread before the asynchronous chat
        # request; the response worker never reads or mutates pond state.
        memory = getattr(self, '_pond_chat_context', '')
        if self.conversation and self.conversation.needs_memory_context():
            memory = self._get_memory_context_for_dialogue() + memory
        return self.conversation.process_player_input(self.duck, message, True, memory)

    def _process_talk(self, *args, **kwargs):
        self._pond_chat_context = self.living_pond.dialogue_context() if self.living_pond else ''
        return super()._process_talk(*args, **kwargs)

    def _check_for_updates_async(self):
        # A source updater must not replace this separate engine branch.
        self._title_update_status = 'ASCII Engine edition - updates stay on this branch.'
    def _download_and_apply_update(self):
        self._check_for_updates_async()
    def _cleanup_pycache(self):
        pass  # No recursive source-tree scan during desktop shutdown.


def main():
    game = None
    try:
        terminal = DesktopInput()
        game = DesktopGame(terminal=terminal, renderer_factory=CanvasRenderer)
        terminal.game = game
        game.renderer.game = game
        game._terminal_options = []
        threading.Thread(target=terminal.read_commands, daemon=True).start()
        game.start()
        send({'type': 'exit', 'saved': bool(game.duck)})
    except Exception:
        traceback.print_exc()
        send({'type': 'error', 'message': traceback.format_exc()})
        return 1
    finally:
        if game and hasattr(game, '_save_executor'):
            game._save_executor.shutdown(wait=True)
        from audio.sound import sound_engine
        sound_engine.shutdown()
        if game and hasattr(game, '_talk_executor'):
            game._talk_executor.shutdown(wait=False)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
