"""
Centralized UI state management.

Extracts all overlay/menu open-state tracking from the Game god object
into a single source of truth.  Game.py can progressively migrate its
boolean flags (``_crafting_menu_open``, ``_scrapbook_menu_open``, etc.)
to use this manager instead.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional


class UIOverlay(Enum):
    """Every distinct overlay/menu that can be open in the game."""
    NONE = auto()
    MAIN_MENU = auto()
    INVENTORY = auto()
    SHOP = auto()
    CRAFTING = auto()
    BUILDING = auto()
    EXPLORATION = auto()
    SETTINGS = auto()
    ACHIEVEMENTS = auto()
    QUESTS = auto()
    CHALLENGES = auto()
    DIARY = auto()
    STATISTICS = auto()
    SCRAPBOOK = auto()
    FRIENDS = auto()
    FISHING = auto()
    GARDEN = auto()
    MINIGAME = auto()
    HELP = auto()
    TUTORIAL = auto()
    TALK = auto()
    DEBUG_MENU = auto()
    DREAM = auto()
    FESTIVAL = auto()
    CUSTOM = auto()
    # Additional overlays present in game.py
    AREAS = auto()
    USE_ITEM = auto()
    WEATHER = auto()
    TREASURE = auto()
    TRICKS = auto()
    TITLES = auto()
    DECORATIONS = auto()
    DECORATION_ROOM = auto()
    COLLECTIBLES = auto()
    BADGES = auto()
    SECRETS = auto()
    PRESTIGE = auto()
    SAVE_SLOTS = auto()
    TRADING = auto()
    ENHANCED_DIARY = auto()
    GOALS = auto()
    CONFIRMATION = auto()


@dataclass
class UIState:
    """Snapshot of the current UI state."""
    active_overlay: UIOverlay = UIOverlay.NONE
    overlay_stack: List[UIOverlay] = field(default_factory=list)
    selected_index: int = 0
    current_page: int = 0
    scroll_offset: int = 0
    is_transitioning: bool = False
    overlay_data: Dict[str, Any] = field(default_factory=dict)


class UIStateManager:
    """
    Manages which UI overlay is active, supports a stack for nesting,
    and holds per-overlay selection / pagination state.

    Usage from game.py::

        self.ui_state = UIStateManager()

        # Open crafting overlay
        self.ui_state.open_overlay(UIOverlay.CRAFTING)

        # Query
        if self.ui_state.is_open(UIOverlay.CRAFTING):
            ...

        # Close (returns to previous overlay or NONE)
        self.ui_state.close_overlay()
    """

    def __init__(self) -> None:
        self._state = UIState()

    # ── Properties ────────────────────────────────────────────────────

    @property
    def state(self) -> UIState:
        """Direct read access to the current state (prefer helper methods)."""
        return self._state

    # ── Overlay lifecycle ─────────────────────────────────────────────

    def open_overlay(self, overlay: UIOverlay, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Open *overlay*, pushing the current one onto the stack.

        Args:
            overlay: The overlay to activate.
            data:    Arbitrary data dict attached to this overlay session.
        """
        if (
            self._state.active_overlay != UIOverlay.NONE
            and self._state.active_overlay != overlay
        ):
            self._state.overlay_stack.append(self._state.active_overlay)
        self._state.active_overlay = overlay
        self._state.selected_index = 0
        self._state.current_page = 0
        self._state.scroll_offset = 0
        self._state.is_transitioning = False
        self._state.overlay_data = data if data is not None else {}

    def close_overlay(self) -> Optional[UIOverlay]:
        """
        Close the active overlay and return to the previous one (or NONE).

        Returns:
            The overlay that was just closed, or ``None`` if nothing was open.
        """
        closed = self._state.active_overlay
        if closed == UIOverlay.NONE:
            return None

        if self._state.overlay_stack:
            self._state.active_overlay = self._state.overlay_stack.pop()
        else:
            self._state.active_overlay = UIOverlay.NONE

        # Reset per-overlay transient state
        self._state.selected_index = 0
        self._state.current_page = 0
        self._state.scroll_offset = 0
        self._state.overlay_data = {}
        return closed

    def close_all(self) -> None:
        """Close every overlay and clear the stack."""
        self._state.active_overlay = UIOverlay.NONE
        self._state.overlay_stack.clear()
        self._state.selected_index = 0
        self._state.current_page = 0
        self._state.scroll_offset = 0
        self._state.overlay_data = {}
        self._state.is_transitioning = False

    # ── Queries ───────────────────────────────────────────────────────

    def get_active(self) -> UIOverlay:
        """Return the currently active overlay."""
        return self._state.active_overlay

    def is_any_open(self) -> bool:
        """True if *any* overlay is active (not NONE)."""
        return self._state.active_overlay != UIOverlay.NONE

    def is_open(self, overlay: UIOverlay) -> bool:
        """True if *overlay* is the currently active overlay."""
        return self._state.active_overlay == overlay

    # ── Per-overlay data ──────────────────────────────────────────────

    def get_data(self, key: str, default: Any = None) -> Any:
        """Read an arbitrary value from the active overlay's data bag."""
        return self._state.overlay_data.get(key, default)

    def set_data(self, key: str, value: Any) -> None:
        """Write an arbitrary value into the active overlay's data bag."""
        self._state.overlay_data[key] = value

    # ── Selection / navigation helpers ────────────────────────────────

    def get_selected_index(self) -> int:
        """Return the current selected-item index."""
        return self._state.selected_index

    def set_selected_index(self, index: int) -> None:
        """Set the current selected-item index (clamped to >= 0)."""
        self._state.selected_index = max(0, index)

    def navigate(self, direction: int) -> None:
        """
        Adjust the selected index by *direction* (positive = down, negative = up).

        The index is clamped at 0 on the low end; callers should clamp the
        upper bound against the actual item count.
        """
        self._state.selected_index = max(0, self._state.selected_index + direction)

    def get_page(self) -> int:
        """Return the current page number."""
        return self._state.current_page

    def set_page(self, page: int) -> None:
        """Set the current page number (clamped to >= 0)."""
        self._state.current_page = max(0, page)

    # ── Convenience ───────────────────────────────────────────────────

    def __repr__(self) -> str:
        stack_names = [o.name for o in self._state.overlay_stack]
        return (
            f"UIStateManager(active={self._state.active_overlay.name}, "
            f"stack={stack_names}, idx={self._state.selected_index}, "
            f"page={self._state.current_page})"
        )
