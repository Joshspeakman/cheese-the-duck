from __future__ import annotations

import time
from types import SimpleNamespace

import pytest

from core.duck_store import DuckStore
from core.game import Game
from duck.duck import Duck


class _FakeBehaviorAI:
    def __init__(self, action_value: str):
        self._action_value = action_value

    def get_current_action(self):
        return SimpleNamespace(action=SimpleNamespace(value=self._action_value))


def _bare_game() -> Game:
    game = object.__new__(Game)
    game.duck = Duck.create_new(name="Cheese")
    game.behavior_ai = None
    game.duck_store = DuckStore()
    game._dream_active = False
    return game


def test_active_sleep_action_uses_behavior_ai_when_duck_action_is_stale():
    game = _bare_game()
    game.behavior_ai = _FakeBehaviorAI("nap_in_nest")
    game.duck.current_action = None

    assert game._get_active_sleep_action(time.time()) == "nap_in_nest"


def test_sleep_regen_preserves_autonomous_action_in_duck_store():
    game = _bare_game()
    game.duck.needs.energy = 10.0
    game.duck.current_action = "nap"
    game.duck.action_start_time = time.time()
    game.duck._action_end_time = time.time() + 30.0

    # Reproduce the stale-store state from autonomous actions: BehaviorAI set
    # Duck.current_action, but DuckStore has not seen it yet.
    assert game.duck_store.get_state().current_action is None

    game._apply_sleep_energy_regen("nap", delta_seconds=5.0, energy_before=10.0)

    assert game.duck.needs.energy == pytest.approx(20.0)
    assert game.duck.current_action == "nap"
    assert game.duck_store.get_state().current_action == "nap"


def test_duck_clears_expired_autonomous_action():
    duck = Duck.create_new(name="Cheese")
    duck.current_action = "nap"
    duck.action_start_time = time.time() - 60.0
    duck._action_end_time = time.time() - 1.0

    duck.update(0.0)

    assert duck.current_action is None
    assert duck.action_start_time is None
