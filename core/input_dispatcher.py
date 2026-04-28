"""
Input routing / dispatch extracted from the massive ``Game._process_input()``
if/elif chain.

The dispatcher maintains a registry of overlay-specific and global input
handlers, ordered by priority.  When a key is received, global handlers fire
first (quit, help, music toggle, ...), then the handler for the active
overlay (if any).

Usage from game.py::

    self.input_dispatcher = InputDispatcher()

    # Register global shortcuts (always active)
    self.input_dispatcher.register_global_handler(
        GlobalInputHandler(game=self), priority=0
    )

    # Register per-overlay handlers
    self.input_dispatcher.register_handler(
        "crafting", crafting_handler, priority=0
    )

    # In _process_input():
    handled = self.input_dispatcher.dispatch(key, active_overlay="crafting")
"""
from __future__ import annotations

import abc
from dataclasses import dataclass, field
import logging
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable

logger = logging.getLogger(__name__)


# ── InputAction dataclass ─────────────────────────────────────────────

@dataclass
class InputAction:
    """Describes a key-press in context."""
    key: Any               # The raw blessed key object
    action_name: str = ""  # Optional semantic name (e.g. "quit", "feed")
    overlay: str = ""      # Active overlay when the key was pressed


# ── InputHandler protocol ─────────────────────────────────────────────

@runtime_checkable
class InputHandlerProtocol(Protocol):
    """
    Any object that can consume a key press.

    Return ``True`` if the input was handled (stop further dispatch),
    ``False`` to let the next handler in the chain try.
    """
    def handle(self, key: Any, context: InputAction) -> bool: ...


class InputHandlerBase(abc.ABC):
    """
    Abstract base class alternative to the protocol.

    Subclass this when you want explicit abstract enforcement.
    """
    @abc.abstractmethod
    def handle(self, key: Any, context: InputAction) -> bool:
        """Process *key* in *context*.  Return True if consumed."""
        ...


# ── InputDispatcher ───────────────────────────────────────────────────

@dataclass(order=True)
class _HandlerEntry:
    """Internal wrapper that sorts handlers by ascending priority number."""
    priority: int
    handler: Any = field(compare=False)  # InputHandlerProtocol


class InputDispatcher:
    """
    Routes key-presses to the correct handler based on the active overlay.

    Dispatch order:
    1. Global handlers (sorted by priority, lowest first).
    2. Overlay-specific handlers (sorted by priority, lowest first).

    The first handler that returns ``True`` stops the chain.
    """

    def __init__(self) -> None:
        self._global_handlers: List[_HandlerEntry] = []
        self._overlay_handlers: Dict[str, List[_HandlerEntry]] = {}

    # ── Registration ──────────────────────────────────────────────────

    def register_handler(
        self,
        overlay: str,
        handler: InputHandlerProtocol,
        priority: int = 0,
    ) -> None:
        """
        Register *handler* for a specific overlay name.

        Lower *priority* values fire first.

        Args:
            overlay:  Overlay identifier string (e.g. ``"crafting"``).
            handler:  Object implementing ``handle(key, context) -> bool``.
            priority: Execution order (lower = earlier).
        """
        entry = _HandlerEntry(priority=priority, handler=handler)
        self._overlay_handlers.setdefault(overlay, []).append(entry)
        self._overlay_handlers[overlay].sort()

    def register_global_handler(
        self,
        handler: InputHandlerProtocol,
        priority: int = 0,
    ) -> None:
        """
        Register a handler that fires for **every** key press regardless
        of the active overlay.

        Args:
            handler:  Object implementing ``handle(key, context) -> bool``.
            priority: Execution order (lower = earlier).
        """
        self._global_handlers.append(_HandlerEntry(priority=priority, handler=handler))
        self._global_handlers.sort()

    # ── Dispatch ──────────────────────────────────────────────────────

    def dispatch(self, key: Any, active_overlay: str = "") -> bool:
        """
        Route *key* through the handler chain.

        Args:
            key:            The raw blessed key object.
            active_overlay: Current overlay identifier (empty string for none).

        Returns:
            ``True`` if any handler consumed the input.
        """
        context = InputAction(key=key, overlay=active_overlay)

        # 1. Global handlers
        for entry in self._global_handlers:
            try:
                if entry.handler.handle(key, context):
                    return True
            except Exception:
                # Never let a broken handler crash the game loop.
                logger.debug("Global input handler failed", exc_info=True)

        # 2. Overlay-specific handlers
        if active_overlay and active_overlay in self._overlay_handlers:
            for entry in self._overlay_handlers[active_overlay]:
                try:
                    if entry.handler.handle(key, context):
                        return True
                except Exception:
                    logger.debug("Handler overlay check failed", exc_info=True)

        return False


# ── GlobalInputHandler ────────────────────────────────────────────────

class OverlayInputHandler(InputHandlerBase):
    """Concrete handler that delegates to a callable for a specific overlay."""

    def __init__(self, name: str, callback) -> None:
        self._name = name
        self._callback = callback

    @property
    def name(self) -> str:
        return self._name

    def handle(self, key: Any, context: InputAction) -> bool:
        self._callback(key)
        return True  # overlay always consumes input


class GlobalInputHandler(InputHandlerBase):
    """
    Handles keys that work regardless of which overlay is active.

    Mirrors the top-level key checks in ``Game._handle_action``:

    * ``q``  -> quit (save & exit)
    * ``h``  -> toggle help overlay
    * ``m``  -> toggle music mute
    * ``n``  -> toggle sound effects
    * ``+``/``=`` -> volume up
    * ``-``/``_`` -> volume down

    The *game* reference is stored but only used when ``handle()`` is
    actually called, so there are no import-time circular dependencies.
    """

    def __init__(self, game: Any) -> None:
        """
        Args:
            game: Reference to the ``Game`` instance.  Only the following
                  attributes are accessed:
                  ``_quit``, ``renderer``, ``_close_all_menus``,
                  ``_sound_enabled``, ``sound_engine`` (via import).
        """
        self._game = game

    def handle(self, key: Any, context: InputAction) -> bool:
        """
        Process global shortcuts.

        Returns ``True`` if the key was consumed.
        """
        # Normalise key to a lowercase string (ignoring special/sequence keys)
        is_sequence = getattr(key, 'is_sequence', False)
        key_str = str(key).lower() if not is_sequence else ""
        key_name = getattr(key, 'name', "") or ""

        # Check if any overlay or text-input mode is active.
        # When an overlay is open, only ESC/arrow/Enter should work — not
        # letter shortcuts like m/n/q/h which conflict with typing.
        _overlay_active = bool(context.overlay) and context.overlay != "NONE"
        if not _overlay_active:
            try:
                r = self._game.renderer
                _overlay_active = (
                    r.is_talking() or r.is_shop_open()
                    or r._show_stats or r._show_inventory or r._show_help
                )
            except Exception:
                pass

        # Quit [Q] — only when no overlay is active
        if key_str == 'q' and not _overlay_active:
            self._game._quit()
            return True

        # Help toggle [H] — only when no overlay is active
        if key_str == 'h' and not _overlay_active:
            self._game._close_all_menus()
            self._game.renderer.toggle_help()
            return True

        # Music mute toggle [M] — only when no overlay/text input is active
        if key_str == 'm' and not _overlay_active:
            from audio.sound import sound_engine
            sound_engine.toggle_music_mute()
            if sound_engine.music_muted:
                self._game.renderer.show_message("Music: OFF")
            elif sound_engine.is_radio_playing():
                station = sound_engine.get_radio().current_station
                name = station.name if station else "Radio"
                self._game.renderer.show_message(f"♪ {name} ♪")
            else:
                self._game.renderer.show_message("Music: ON")
            return True

        # Sound toggle [N] — only when no overlay/text input is active
        if key_str == 'n' and not _overlay_active:
            from audio.sound import sound_engine
            self._game._sound_enabled = sound_engine.toggle()
            status = "ON" if self._game._sound_enabled else "OFF"
            self._game.renderer.show_message(f"Sound: {status}")
            return True

        # Volume up [+] or [=] — only when no overlay/text input is active
        if key_str in ('+', '=') and not _overlay_active:
            from audio.sound import sound_engine
            new_vol = sound_engine.volume_up()
            vol_bar = sound_engine.get_volume_display()
            self._game.renderer.show_message(
                f"Volume: {vol_bar} {int(new_vol * 100)}%"
            )
            return True

        # Volume down [-] or [_] — only when no overlay/text input is active
        if key_str in ('-', '_') and not _overlay_active:
            from audio.sound import sound_engine
            new_vol = sound_engine.volume_down()
            vol_bar = sound_engine.get_volume_display()
            self._game.renderer.show_message(
                f"Volume: {vol_bar} {int(new_vol * 100)}%"
            )
            return True

        return False
