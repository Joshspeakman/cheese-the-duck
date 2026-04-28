"""Tests for core.ui_state — UIStateManager overlay lifecycle and navigation."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.ui_state import UIOverlay, UIStateManager


def test_initial_state():
    mgr = UIStateManager()
    assert mgr.get_active() == UIOverlay.NONE
    assert not mgr.is_any_open()


def test_open_overlay():
    mgr = UIStateManager()
    mgr.open_overlay(UIOverlay.CRAFTING)
    assert mgr.get_active() == UIOverlay.CRAFTING
    assert mgr.is_any_open()


def test_close_overlay():
    mgr = UIStateManager()
    mgr.open_overlay(UIOverlay.INVENTORY)
    mgr.close_overlay()
    assert mgr.get_active() == UIOverlay.NONE
    assert not mgr.is_any_open()


def test_close_all():
    mgr = UIStateManager()
    mgr.open_overlay(UIOverlay.CRAFTING)
    mgr.open_overlay(UIOverlay.INVENTORY)
    mgr.close_all()
    assert mgr.get_active() == UIOverlay.NONE
    assert not mgr.is_any_open()


def test_overlay_stack():
    mgr = UIStateManager()
    mgr.open_overlay(UIOverlay.CRAFTING)
    mgr.open_overlay(UIOverlay.INVENTORY)
    assert mgr.get_active() == UIOverlay.INVENTORY
    mgr.close_overlay()
    assert mgr.get_active() == UIOverlay.CRAFTING
    mgr.close_overlay()
    assert mgr.get_active() == UIOverlay.NONE


def test_open_same_overlay_is_idempotent():
    mgr = UIStateManager()
    mgr.open_overlay(UIOverlay.CRAFTING)
    mgr.open_overlay(UIOverlay.CRAFTING)
    assert mgr.get_active() == UIOverlay.CRAFTING

    mgr.close_overlay()
    assert mgr.get_active() == UIOverlay.NONE


def test_navigate():
    mgr = UIStateManager()
    mgr.open_overlay(UIOverlay.INVENTORY)
    mgr.navigate(3)
    assert mgr.get_selected_index() == 3
    mgr.navigate(-1)
    assert mgr.get_selected_index() == 2
    mgr.navigate(-10)
    assert mgr.get_selected_index() == 0
