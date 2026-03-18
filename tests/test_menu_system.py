"""Tests for core/menu_system.py — MenuSystem, MenuItem, MenuDefinition."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from core.menu_system import MenuSystem, MenuItem, MenuDefinition
from core.ui_state import UIStateManager, UIOverlay


# ═══════════════════════════════════════════════════════════════════════════
# MenuItem
# ═══════════════════════════════════════════════════════════════════════════

class TestMenuItem:
    """Tests for the MenuItem dataclass."""

    def test_default_values(self) -> None:
        """MenuItem has sensible defaults for optional fields."""
        item = MenuItem(label="Sword")
        assert item.label == "Sword"
        assert item.enabled is True
        assert item.visible is True
        assert item.action is None
        assert item.submenu is None
        assert item.icon == ""
        assert item.data is None
        assert item.id == ""

    def test_str_without_icon(self) -> None:
        """__str__ returns the label when there is no icon."""
        item = MenuItem(label="Shield")
        assert str(item) == "Shield"

    def test_str_with_icon(self) -> None:
        """__str__ prepends the icon to the label."""
        item = MenuItem(label="Potion", icon="*")
        assert str(item) == "* Potion"

    def test_action_callback(self) -> None:
        """MenuItem stores and exposes an action callback."""
        called = []
        item = MenuItem(label="Go", action=lambda: called.append(True))
        item.action()
        assert called == [True]


# ═══════════════════════════════════════════════════════════════════════════
# MenuDefinition
# ═══════════════════════════════════════════════════════════════════════════

class TestMenuDefinition:
    """Tests for the MenuDefinition dataclass."""

    def test_defaults(self) -> None:
        """Default definition has reasonable values."""
        defn = MenuDefinition(title="Test")
        assert defn.title == "Test"
        assert defn.items == []
        assert defn.columns == 1
        assert defn.show_back is True
        assert defn.page_size == 0
        assert defn.wrap_navigation is True
        assert "KEY_ESCAPE" in defn.close_keys

    def test_items_list(self) -> None:
        """Items passed at construction are stored correctly."""
        items = [MenuItem(label="A"), MenuItem(label="B")]
        defn = MenuDefinition(title="AB", items=items)
        assert len(defn.items) == 2
        assert defn.items[0].label == "A"


# ═══════════════════════════════════════════════════════════════════════════
# MenuSystem — standalone (no UIStateManager)
# ═══════════════════════════════════════════════════════════════════════════

class TestMenuSystemStandalone:
    """Tests for MenuSystem used without a UIStateManager."""

    def test_register_and_has_menu(self) -> None:
        """Registered menus are discoverable via has_menu."""
        ms = MenuSystem()
        assert ms.has_menu("crafting") is False

        ms.register_menu("crafting", MenuDefinition(
            title="Crafting",
            items=[MenuItem(label="Wooden Sword")],
        ))
        assert ms.has_menu("crafting") is True

    def test_open_and_close(self) -> None:
        """Opening a menu sets it active; closing resets to None."""
        ms = MenuSystem()
        ms.register_menu("shop", MenuDefinition(
            title="Shop",
            items=[MenuItem(label="Hat"), MenuItem(label="Scarf")],
        ))

        ms.open_menu("shop")
        assert ms.get_active_menu() == "shop"
        assert len(ms.get_items()) == 2

        ms.close_menu()
        assert ms.get_active_menu() is None
        assert ms.get_items() == []

    def test_open_unregistered_raises(self) -> None:
        """Opening a menu that was never registered raises KeyError."""
        ms = MenuSystem()
        with pytest.raises(KeyError):
            ms.open_menu("does_not_exist")

    def test_select_item_returns_action(self) -> None:
        """select_item returns the action callback of the chosen item."""
        called = []
        action = lambda: called.append("ok")
        ms = MenuSystem()
        ms.register_menu("test", MenuDefinition(
            title="Test",
            items=[MenuItem(label="Go", action=action)],
        ))
        ms.open_menu("test")

        cb = ms.select_item(0)
        assert cb is not None
        cb()
        assert called == ["ok"]

    def test_select_item_disabled(self) -> None:
        """select_item returns None for a disabled item."""
        ms = MenuSystem()
        ms.register_menu("test", MenuDefinition(
            title="Test",
            items=[MenuItem(label="Locked", enabled=False, action=lambda: None)],
        ))
        ms.open_menu("test")
        assert ms.select_item(0) is None

    def test_select_item_out_of_range(self) -> None:
        """select_item returns None for indices outside the item list."""
        ms = MenuSystem()
        ms.register_menu("t", MenuDefinition(title="T", items=[MenuItem(label="A")]))
        ms.open_menu("t")
        assert ms.select_item(99) is None
        assert ms.select_item(-1) is None

    def test_select_item_no_menu_open(self) -> None:
        """select_item returns None when no menu is open."""
        ms = MenuSystem()
        assert ms.select_item(0) is None

    def test_navigate_changes_selected(self) -> None:
        """navigate() moves the selection cursor."""
        ms = MenuSystem()
        ms.register_menu("nav", MenuDefinition(
            title="Nav",
            items=[MenuItem(label="A"), MenuItem(label="B"), MenuItem(label="C")],
        ))
        ms.open_menu("nav")
        assert ms.get_selected() == 0

        ms.navigate(1)
        assert ms.get_selected() == 1

        ms.navigate(1)
        assert ms.get_selected() == 2

    def test_get_definition(self) -> None:
        """get_definition returns the stored definition (or None)."""
        ms = MenuSystem()
        defn = MenuDefinition(title="X")
        ms.register_menu("x", defn)
        assert ms.get_definition("x") is defn
        assert ms.get_definition("nope") is None

    def test_update_items_live(self) -> None:
        """update_items replaces items on a currently active menu."""
        ms = MenuSystem()
        ms.register_menu("dyn", MenuDefinition(
            title="Dynamic",
            items=[MenuItem(label="Old")],
        ))
        ms.open_menu("dyn")
        assert ms.get_items()[0].label == "Old"

        ms.update_items("dyn", [MenuItem(label="New1"), MenuItem(label="New2")])
        assert len(ms.get_items()) == 2
        assert ms.get_items()[0].label == "New1"

    def test_invisible_items_filtered(self) -> None:
        """Items with visible=False are excluded when the menu opens."""
        ms = MenuSystem()
        ms.register_menu("vis", MenuDefinition(
            title="Vis",
            items=[
                MenuItem(label="Shown", visible=True),
                MenuItem(label="Hidden", visible=False),
            ],
        ))
        ms.open_menu("vis")
        labels = [i.label for i in ms.get_items()]
        assert "Shown" in labels
        assert "Hidden" not in labels

    def test_repr(self) -> None:
        """__repr__ includes registered menu ids and active state."""
        ms = MenuSystem()
        ms.register_menu("a", MenuDefinition(title="A"))
        r = repr(ms)
        assert "a" in r
        assert "active=None" in r


# ═══════════════════════════════════════════════════════════════════════════
# MenuSystem — with UIStateManager
# ═══════════════════════════════════════════════════════════════════════════

class TestMenuSystemWithUI:
    """Tests for MenuSystem + UIStateManager integration."""

    def test_open_sets_overlay(self) -> None:
        """Opening a well-known menu opens the corresponding UIOverlay."""
        ui = UIStateManager()
        ms = MenuSystem(ui)
        ms.register_menu("crafting", MenuDefinition(
            title="Crafting",
            items=[MenuItem(label="Sword")],
        ))
        ms.open_menu("crafting")
        assert ui.is_open(UIOverlay.CRAFTING)

    def test_close_clears_overlay(self) -> None:
        """Closing the menu pops the overlay from the UIStateManager."""
        ui = UIStateManager()
        ms = MenuSystem(ui)
        ms.register_menu("shop", MenuDefinition(
            title="Shop",
            items=[MenuItem(label="Hat")],
        ))
        ms.open_menu("shop")
        ms.close_menu()
        assert ui.get_active() == UIOverlay.NONE

    def test_unknown_menu_id_uses_custom_overlay(self) -> None:
        """A menu_id not in _MENU_TO_OVERLAY maps to UIOverlay.CUSTOM."""
        ui = UIStateManager()
        ms = MenuSystem(ui)
        ms.register_menu("my_custom", MenuDefinition(
            title="Custom",
            items=[MenuItem(label="Stuff")],
        ))
        ms.open_menu("my_custom")
        assert ui.is_open(UIOverlay.CUSTOM)
