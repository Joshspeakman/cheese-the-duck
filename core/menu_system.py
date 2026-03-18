"""
Unified menu state management.

Builds on the patterns established in ``core.menu_controller`` (MenuController,
MenuConfig, MenuResult) and adds a higher-level registry so that game.py can
define menus declaratively and open/close them by ID.

Usage from game.py::

    self.menu_system = MenuSystem(self.ui_state)

    self.menu_system.register_menu("crafting", MenuDefinition(
        title="Crafting",
        items=[MenuItem(label="Wooden Sword", action=craft_sword)],
    ))

    self.menu_system.open_menu("crafting")
    items = self.menu_system.get_items()
    selected_callback = self.menu_system.select_item(0)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from core.menu_controller import MenuController, MenuConfig, MenuResult
from core.ui_state import UIOverlay, UIStateManager


# ── Data classes ──────────────────────────────────────────────────────

@dataclass
class MenuItem:
    """A single item inside a menu."""
    label: str
    action: Optional[Callable[[], Any]] = None
    enabled: bool = True
    visible: bool = True
    submenu: Optional[str] = None       # menu_id of a nested sub-menu
    icon: str = ""                       # optional icon / emoji
    data: Any = None                     # arbitrary payload
    id: str = ""                         # optional unique identifier

    def __str__(self) -> str:
        prefix = f"{self.icon} " if self.icon else ""
        return f"{prefix}{self.label}"


@dataclass
class MenuDefinition:
    """
    Blueprint for a menu.

    Holds the *template* from which a live MenuController is created
    when the menu is opened.
    """
    title: str
    items: List[MenuItem] = field(default_factory=list)
    columns: int = 1                    # future: multi-column layout
    show_back: bool = True              # show a "Back" entry at the bottom
    page_size: int = 0                  # 0 = no pagination
    close_keys: List[str] = field(default_factory=lambda: ["KEY_ESCAPE"])
    select_keys: List[str] = field(default_factory=lambda: ["KEY_ENTER", " "])
    wrap_navigation: bool = True


# ── MenuSystem ────────────────────────────────────────────────────────

class MenuSystem:
    """
    High-level menu registry that works alongside :class:`UIStateManager`.

    * ``register_menu`` stores a :class:`MenuDefinition` by id.
    * ``open_menu`` activates the corresponding :class:`MenuController` and
      opens the ``UIOverlay.MAIN_MENU`` (or a custom overlay) in
      the :class:`UIStateManager`.
    * ``close_menu`` tears down the active controller and pops the overlay.
    * Navigation and selection are forwarded to the underlying controller.
    """

    # Map well-known menu ids to overlay enum values.
    _MENU_TO_OVERLAY: Dict[str, UIOverlay] = {
        "crafting":     UIOverlay.CRAFTING,
        "building":     UIOverlay.BUILDING,
        "areas":        UIOverlay.AREAS,
        "use_item":     UIOverlay.USE_ITEM,
        "minigames":    UIOverlay.MINIGAME,
        "quests":       UIOverlay.QUESTS,
        "weather":      UIOverlay.WEATHER,
        "treasure":     UIOverlay.TREASURE,
        "scrapbook":    UIOverlay.SCRAPBOOK,
        "tricks":       UIOverlay.TRICKS,
        "titles":       UIOverlay.TITLES,
        "decorations":  UIOverlay.DECORATIONS,
        "collectibles": UIOverlay.COLLECTIBLES,
        "badges":       UIOverlay.BADGES,
        "secrets":      UIOverlay.SECRETS,
        "garden":       UIOverlay.GARDEN,
        "prestige":     UIOverlay.PRESTIGE,
        "save_slots":   UIOverlay.SAVE_SLOTS,
        "trading":      UIOverlay.TRADING,
        "diary":        UIOverlay.DIARY,
        "enhanced_diary": UIOverlay.ENHANCED_DIARY,
        "festival":     UIOverlay.FESTIVAL,
        "inventory":    UIOverlay.INVENTORY,
        "shop":         UIOverlay.SHOP,
        "settings":     UIOverlay.SETTINGS,
        "debug":        UIOverlay.DEBUG_MENU,
        "help":         UIOverlay.HELP,
        "talk":         UIOverlay.TALK,
        "main_menu":    UIOverlay.MAIN_MENU,
    }

    def __init__(self, ui_state: Optional[UIStateManager] = None) -> None:
        """
        Args:
            ui_state: Optional :class:`UIStateManager` to keep in sync.
                      Pass ``None`` to use the MenuSystem standalone.
        """
        self._ui_state = ui_state
        self._definitions: Dict[str, MenuDefinition] = {}
        self._active_menu_id: Optional[str] = None
        self._controller: Optional[MenuController] = None

    # ── Registration ──────────────────────────────────────────────────

    def register_menu(self, menu_id: str, definition: MenuDefinition) -> None:
        """
        Register (or replace) a menu definition.

        Args:
            menu_id:    Unique string identifier (e.g. ``"crafting"``).
            definition: The :class:`MenuDefinition` blueprint.
        """
        self._definitions[menu_id] = definition

    def has_menu(self, menu_id: str) -> bool:
        """Check whether *menu_id* is registered."""
        return menu_id in self._definitions

    # ── Lifecycle ─────────────────────────────────────────────────────

    def open_menu(self, menu_id: str) -> None:
        """
        Activate the menu identified by *menu_id*.

        Creates a :class:`MenuController` from the stored definition and,
        if a :class:`UIStateManager` is attached, opens the corresponding
        overlay.

        Raises:
            KeyError: If *menu_id* has not been registered.
        """
        defn = self._definitions[menu_id]

        # Build a MenuController from the definition
        config = MenuConfig(
            title=defn.title,
            close_keys=list(defn.close_keys),
            select_keys=list(defn.select_keys),
            wrap_navigation=defn.wrap_navigation,
            page_size=defn.page_size,
        )
        controller = MenuController(config)

        # Only include visible items
        visible_items = [item for item in defn.items if item.visible]
        controller.set_items(visible_items)
        controller.is_open = True

        self._controller = controller
        self._active_menu_id = menu_id

        # Sync with UIStateManager
        if self._ui_state is not None:
            overlay = self._MENU_TO_OVERLAY.get(menu_id, UIOverlay.CUSTOM)
            self._ui_state.open_overlay(overlay, {"menu_id": menu_id})

    def close_menu(self) -> None:
        """Close the active menu (if any) and pop the overlay."""
        if self._controller is not None:
            self._controller.is_open = False
        self._controller = None
        self._active_menu_id = None

        if self._ui_state is not None:
            self._ui_state.close_overlay()

    # ── Queries ───────────────────────────────────────────────────────

    def get_active_menu(self) -> Optional[str]:
        """Return the id of the active menu, or ``None``."""
        return self._active_menu_id

    def get_items(self) -> List[MenuItem]:
        """
        Return the visible items of the active menu.

        Returns an empty list if no menu is open.
        """
        if self._controller is None:
            return []
        return self._controller.items

    def get_definition(self, menu_id: str) -> Optional[MenuDefinition]:
        """Return the stored definition for *menu_id*, or ``None``."""
        return self._definitions.get(menu_id)

    # ── Navigation ────────────────────────────────────────────────────

    def navigate(self, direction: int) -> None:
        """
        Move the selection cursor by *direction* (``+1`` = down, ``-1`` = up).
        """
        if self._controller is not None:
            self._controller._navigate(direction)

    def get_selected(self) -> int:
        """Return the selected index of the active menu (or ``0``)."""
        if self._controller is not None:
            return self._controller.selected_index
        return 0

    def select_item(self, index: int) -> Optional[Callable[[], Any]]:
        """
        Select item at *index* and return its action callback (if any).

        Returns ``None`` if the index is out of range, the item is disabled,
        or no menu is open.
        """
        if self._controller is None:
            return None
        items = self._controller.items
        if index < 0 or index >= len(items):
            return None
        item = items[index]
        if not getattr(item, 'enabled', True):
            return None
        return getattr(item, 'action', None)

    def handle_input(self, key: Any) -> MenuResult:
        """
        Forward a raw key press to the active :class:`MenuController`.

        Returns ``MenuResult.NONE`` if no menu is open.
        """
        if self._controller is None:
            return MenuResult.NONE
        result = self._controller.handle_input(key)
        return result.result

    # ── Convenience: update items dynamically ─────────────────────────

    def update_items(self, menu_id: str, items: List[MenuItem]) -> None:
        """
        Replace the item list of a registered definition *and* the live
        controller (if that menu is currently active).

        Useful for menus whose contents change at runtime (crafting recipes
        filtered by owned materials, etc.).
        """
        if menu_id in self._definitions:
            self._definitions[menu_id].items = items

        # If this menu is currently active, hot-swap items
        if self._active_menu_id == menu_id and self._controller is not None:
            visible = [i for i in items if i.visible]
            self._controller.set_items(visible)

    # ── Dunder ────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return (
            f"MenuSystem(registered={list(self._definitions.keys())}, "
            f"active={self._active_menu_id!r})"
        )
