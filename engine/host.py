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
                    if self.game._state == 'playing' and not (self.game._confirmation_dialog and self.game._confirmation_dialog.is_open):
                        self.game._close_all_menus()
                        self.game.renderer.hide_overlays()
                        self.game._execute_menu_action(key['action'])
                    return Key()
            return key
        except queue.Empty: return Key()
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
                    elif kind == 'action' and command.get('action') in ACTIONS:
                        self.commands.put_nowait({'action': command['action']})
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
        self.landscape = Landscape(terminal)
        self.last_sent = 0
        self.game = None
        self.sequence = 0
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
        send({'type': 'frame', 'seq': self.sequence, 'cols': COLS, 'rows': rows,
              'lines': [line_runs(line) for line in lines], 'meta': metadata})

class DesktopGame(Game):
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
