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
                    if key.get('type') == 'chat':
                        self.game._submit_chat(key)
                        return Key()
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
                    elif kind == 'chat':
                        self.commands.put_nowait(command)
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
    def _update_camera(self, viewport_w, viewport_h):
        old_x,old_y=self._camera_x,self._camera_y
        super()._update_camera(viewport_w,viewport_h)
        # The original visitor animator stores screen coordinates. Preserve its
        # world position and destination when this viewport scrolls.
        from world.friends import visitor_animator
        visitor_animator.shift_camera(self._camera_x-old_x,self._camera_y-old_y)

    max_width, max_height = COLS, ROWS - 4
    def __init__(self, terminal):
        super().__init__(terminal)
        from engine.chat_stream import ChatStream, ChatMirror
        self.chat = ChatStream()
        self._chat_log = ChatMirror(self.chat.raw, self._chat_log)
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
        from engine.guest_motion import GuestMotion, StoryMotion
        self.guest_motion = GuestMotion()
        self.story_motion = StoryMotion()
        self.living_pond = None
        self._pond_duck = None
        super().__init__(*args, **kwargs)

    def _restore_living_pond(self, data):
        from engine.living_world import LivingPond
        if self.living_pond:self.living_pond.minds.close()
        self._pending_talk_future = None
        self.living_pond = LivingPond(data)
        self.renderer.chat.restore(self.living_pond.minds.model.state['exchanges'])
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
        self._reconcile_visitor_presence()

    def _reconcile_visitor_presence(self):
        from engine import visitor_presence
        if visitor_presence.reconcile(self):
            # Other company routines also consult this presence cache before
            # the usual end-of-frame mind update. Do not retain the absent body.
            self.living_pond.minds.sync()
            # Release a rare-Pip lease before GuestMotion can consume its target.
            # Its actual actor remains available for owner-specific cleanup.
            self._refresh_shared_motion()

    def _start_new_game(self):
        self.renderer.chat.reset()
        if self.living_pond:self.living_pond.minds.close()
        self._pending_talk_future = None
        self.living_pond = None
        self._pond_duck = None
        super()._start_new_game()
        self._ensure_living_pond()
        self._save_game()

    def _load_game(self):
        self.renderer.chat.reset()
        super()._load_game()
        self._ensure_living_pond(offline=True)

    def _refresh_friend_motion(self):
        from world.friends import visitor_animator
        from engine import carnival
        shared=bool(self.living_pond and carnival.is_shared(self.living_pond.state.get('plan')))
        if self.living_pond and (self._state=='playing' or shared) and self.duck and self.friends.current_visit:
            motion=self.living_pond.minds.motion(self.friends.current_visit.friend_id)
            # Meeting providers publish world points. Convert a fresh descriptor
            # once here, without mutating a retained reservation or its target.
            motion=dict(motion)
            for kind in ('meeting','shelter'):
                if motion.get(kind):
                    meeting=dict(motion[kind]);target=meeting['target']
                    meeting['target']=[target[0]-self.renderer._camera_x,target[1]-self.renderer._camera_y]
                    motion[kind]=meeting
            visitor_animator._mind_motion=motion
        else:visitor_animator._mind_motion={}

    def _refresh_shared_motion(self):
        if self.living_pond:
            from engine import carnival
            if carnival.is_shared(self.living_pond.state.get('plan')):
                from engine import castle_shared
                castle_shared.refresh(self.living_pond)

    def _update(self):
        self._ensure_living_pond()
        self._refresh_shared_motion()
        self._refresh_friend_motion()
        from world.friends import visitor_animator
        visitor_animator._roam_bounds = (2, max(12, self.renderer._viewport_width - 12),
                                         1, max(5, self.renderer._viewport_height - 6))
        super()._update()
        if self.living_pond:
            self.living_pond.tick()
        self._reconcile_visitor_presence()
        # Base/pond callbacks may change a visit, story step or age. Revalidate
        # motion ownership before the rare/story movers consume a destination.
        self._refresh_shared_motion()
        if self.duck:
            self.guest_motion.tick(self)
        self.story_motion.tick(self)
        if self.living_pond and self._state == 'playing' and self.duck:
            self.living_pond.minds.tick()
            self._refresh_friend_motion()

    def _perform_interaction(self, interaction):
        if self.living_pond and self.living_pond.busy:
            self.living_pond.cancel()
        before = self.living_pond.minds.before(interaction) if self.living_pond and self.duck else None
        accepted_at = self._last_interaction_time.get(interaction, 0)
        super()._perform_interaction(interaction)
        if before and self._last_interaction_time.get(interaction, 0) != accepted_at:
            self.living_pond.minds.completed(interaction, 'You made time to '+interaction+' with Cheese.', before)
        if self.living_pond and self.duck and self.duck.growth_stage != 'egg':
            self.living_pond.remember('care', 'You made time to '+interaction+' with Cheese.', .55)

    def _on_interaction_effects_applied(self, item_id, result):
        super()._on_interaction_effects_applied(item_id, result)
        if self.living_pond and result:
            self.living_pond.sync()
            pending = getattr(self.interaction_controller,'_pending',None)
            obj = self.living_pond.object_state(item_id,getattr(pending,'instance',None))
            if obj:
                obj['uses'] += 1
                obj['bond'] = min(1, obj['bond'] + .02)
                obj['last_use'] = self.living_pond.state['elapsed']

    def _generate_talk_response(self, message):
        from engine.local_speech import speak
        messages, fallback = self._pond_speech_request
        result = speak(messages, fallback)
        class SpeechLine(str):
            pass
        line = SpeechLine(result['text'])
        line.speech_result = result
        return line

    def _process_talk(self, message, allow_item_commands=True):
        if not self.duck or not self.living_pond:return
        minds=self.living_pond.minds
        if minds.pending or getattr(self, '_pending_talk_future', None):
            self.renderer.show_message('One thought at a time. This beak has a queue.', duration=3, category='duck')
            return
        minds.sync()
        self._pond_speech_request=(minds.prompt('cheese',message),minds.fallback('cheese',message))
        super()._process_talk(message, allow_item_commands=allow_item_commands)
        if getattr(self, '_pending_talk_future', None):
            minds.model.heard_player('cheese',message,minds.context(),minds.now)
            channel=getattr(minds,'_requested_channel','say')
            minds.reply_channels['cheese']=channel
            self.renderer.chat.player(message,'cheese',channel)

    def _submit_chat(self, command):
        stream=self.renderer.chat
        request=command.get('id');text=command.get('text');target=command.get('target','cheese')
        if not isinstance(request,str) or not 1<=len(request)<=80:return
        if request in stream.receipts:return
        if command.get('session')!=stream.session:
            return stream.receipt(request,False,'The pond changed. Send your message again.')
        if not isinstance(text,str) or not text.strip() or len(text)>1000:
            return stream.receipt(request,False,'Write a message of up to 1,000 characters.')
        if not isinstance(target,str) or len(target)>128 or command.get('channel') not in ('say','whisper'):
            return stream.receipt(request,False,'Choose Cheese or a friend who is here.')
        if (self._state!='playing' or not self.duck or not self.living_pond or
                self.renderer.interface_modal or self._active_minigame or
                (self._confirmation_dialog and self._confirmation_dialog.is_open)):
            return stream.receipt(request,False,'Finish the current screen before chatting.')
        minds=self.living_pond.minds
        minds._requested_channel=command['channel']
        try:accepted,message=minds.ask(target,text)
        finally:
            if hasattr(minds,'_requested_channel'):del minds._requested_channel
        stream.receipt(request,accepted,message)

    def _check_pending_talk(self):
        future=getattr(self, '_pending_talk_future', None)
        if future and future.done() and self.living_pond:
            try:
                line=future.result()
                result=getattr(line, 'speech_result', {'text':str(line),'source':'authored','detail':'Learning is active.'})
                self.living_pond.minds.exchange('cheese','player',getattr(self,'_pending_talk_message',''),result)
            except Exception:
                pass
        return super()._check_pending_talk()

    def _parse_llm_actions(self, response):
        # Local speech is expressive, never an inventory/action authority.
        from engine.local_speech import clean_speech
        return [], clean_speech(response)

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
        if game and game.living_pond:game.living_pond.minds.close()
        if game and hasattr(game, '_save_executor'):
            game._save_executor.shutdown(wait=True)
        from audio.sound import sound_engine
        sound_engine.shutdown()
        if game and hasattr(game, '_talk_executor'):
            game._talk_executor.shutdown(wait=False)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
