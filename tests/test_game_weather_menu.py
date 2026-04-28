"""Tests for weather activities menu input handling."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.game import Game
from core.ui_state import UIOverlay, UIStateManager
from ui.menu_selector import MenuItem, MenuSelector


class _FakeKey:
    def __init__(self, text: str, name: str = "", is_sequence: bool = True):
        self._text = text
        self.name = name
        self.is_sequence = is_sequence

    def __str__(self) -> str:
        return self._text


class _FakeWeatherMenu:
    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True


class _FakeRenderer:
    def __init__(self):
        self.message_dismissed = False
        self.overlay_dismissed = False

    def dismiss_message(self):
        self.message_dismissed = True

    def dismiss_overlay(self):
        self.overlay_dismissed = True


def _make_weather_game():
    game = Game.__new__(Game)
    game.ui_state = UIStateManager()
    game.ui_state.open_overlay(UIOverlay.WEATHER)
    game._weather_menu = _FakeWeatherMenu()
    game.renderer = _FakeRenderer()
    return game


def _make_garden_game():
    game = Game.__new__(Game)
    game.ui_state = UIStateManager()
    game.ui_state.open_overlay(UIOverlay.GARDEN)
    game.renderer = _FakeRenderer()
    return game


def test_weather_menu_closes_on_raw_escape_sequence():
    game = _make_weather_game()

    game._handle_weather_input_direct(_FakeKey("\x1b", name=""))

    assert game.ui_state.get_active() == UIOverlay.NONE
    assert game._weather_menu.closed
    assert game.renderer.message_dismissed
    assert game.renderer.overlay_dismissed


def test_weather_menu_closes_on_raw_backspace_sequence():
    game = _make_weather_game()

    game._handle_weather_input_direct(_FakeKey("\x7f", name=""))

    assert game.ui_state.get_active() == UIOverlay.NONE
    assert game._weather_menu.closed
    assert game.renderer.message_dismissed
    assert game.renderer.overlay_dismissed


def test_garden_menu_closes_on_raw_backspace_sequence():
    game = _make_garden_game()

    game._handle_garden_input(_FakeKey("\x7f", name=""))

    assert game.ui_state.get_active() == UIOverlay.NONE
    assert game.renderer.message_dismissed
    assert game.renderer.overlay_dismissed


def test_menu_selector_closes_on_raw_backspace_sequence():
    menu = MenuSelector("Test")
    menu.set_items([MenuItem("one", "One")])
    menu.open()

    handled = menu.handle_key("\x7f", "")

    assert handled
    assert menu.was_cancelled()
    assert not menu.is_open()
