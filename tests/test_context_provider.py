"""Tests for dialogue/context_provider.py — ContextProvider ABC and GameContextProvider."""
from __future__ import annotations

import sys
import gc
import weakref
from pathlib import Path
from typing import List, Optional

import pytest

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from dialogue.context_provider import ContextProvider, GameContextProvider
from dialogue.dialogue_core import DialogueContext


# ═══════════════════════════════════════════════════════════════════════════
# Stub / mock helpers
# ═══════════════════════════════════════════════════════════════════════════

class StubContextProvider(ContextProvider):
    """Minimal concrete implementation of the ContextProvider ABC."""

    def build_context(self, player_message=None, triggers=None):
        return DialogueContext(
            timestamp=0.0,
            player_message=player_message,
            triggers=triggers or [],
        )

    def get_duck_mood(self) -> str:
        return "happy"

    def get_duck_trust(self) -> float:
        return 75.0

    def get_weather(self) -> str:
        return "rain"

    def get_time_of_day(self) -> str:
        return "evening"

    def get_season(self) -> str:
        return "autumn"

    def get_current_biome(self) -> str:
        return "forest"

    def get_current_location(self) -> str:
        return "clearing"

    def get_active_visitor(self) -> Optional[str]:
        return None

    def get_active_event(self) -> Optional[str]:
        return None


class FakeGame:
    """Lightweight stand-in for a Game object."""

    def __init__(self):
        self.duck = FakeDuck()
        self.atmosphere = FakeAtmosphere()

    # attributes that GameContextProvider reads optionally
    world = None
    visitor_manager = None
    event_manager = None


class FakeDuck:
    def __init__(self):
        self.trust = 42.0
        self.current_location = "pond_edge"

    def get_mood(self):
        return FakeMood()


class FakeMoodState:
    value = "curious"


class FakeMood:
    state = FakeMoodState()


class FakeAtmosphere:
    current_weather = "clear"
    time_of_day = "morning"
    current_season = "summer"


# ═══════════════════════════════════════════════════════════════════════════
# ContextProvider ABC
# ═══════════════════════════════════════════════════════════════════════════

class TestContextProviderABC:
    """Tests for the abstract ContextProvider interface."""

    def test_cannot_instantiate_abc(self) -> None:
        """ContextProvider itself cannot be instantiated directly."""
        with pytest.raises(TypeError):
            ContextProvider()

    def test_stub_implements_interface(self) -> None:
        """A complete stub satisfies the ABC contract."""
        provider = StubContextProvider()
        ctx = provider.build_context(player_message="hi")
        assert isinstance(ctx, DialogueContext)
        assert ctx.player_message == "hi"

    def test_stub_accessors(self) -> None:
        """Individual accessors return the stub values."""
        p = StubContextProvider()
        assert p.get_duck_mood() == "happy"
        assert p.get_duck_trust() == 75.0
        assert p.get_weather() == "rain"
        assert p.get_time_of_day() == "evening"
        assert p.get_season() == "autumn"
        assert p.get_current_biome() == "forest"
        assert p.get_current_location() == "clearing"
        assert p.get_active_visitor() is None
        assert p.get_active_event() is None


# ═══════════════════════════════════════════════════════════════════════════
# GameContextProvider
# ═══════════════════════════════════════════════════════════════════════════

class TestGameContextProvider:
    """Tests for the concrete GameContextProvider."""

    def test_reads_duck_mood(self) -> None:
        """get_duck_mood returns the duck's mood state value."""
        game = FakeGame()
        provider = GameContextProvider(game)
        assert provider.get_duck_mood() == "curious"

    def test_reads_duck_trust(self) -> None:
        """get_duck_trust returns the duck's trust attribute."""
        game = FakeGame()
        provider = GameContextProvider(game)
        assert provider.get_duck_trust() == 42.0

    def test_reads_weather(self) -> None:
        """get_weather returns the atmosphere's current weather."""
        game = FakeGame()
        provider = GameContextProvider(game)
        assert provider.get_weather() == "clear"

    def test_reads_time_of_day(self) -> None:
        """get_time_of_day returns the atmosphere's time_of_day."""
        game = FakeGame()
        provider = GameContextProvider(game)
        assert provider.get_time_of_day() == "morning"

    def test_reads_season(self) -> None:
        """get_season returns the atmosphere's current season."""
        game = FakeGame()
        provider = GameContextProvider(game)
        assert provider.get_season() == "summer"

    def test_fallback_when_game_collected(self) -> None:
        """When the game ref is garbage-collected, accessors return defaults."""
        game = FakeGame()
        provider = GameContextProvider(game)
        # Drop all strong references to game
        del game
        gc.collect()

        assert provider.get_duck_mood() == "content"
        assert provider.get_duck_trust() == 20.0
        assert provider.get_weather() == "clear"
        assert provider.get_time_of_day() == "day"
        assert provider.get_season() == "spring"
        assert provider.get_current_biome() == "pond"
        assert provider.get_current_location() == "home"
        assert provider.get_active_visitor() is None
        assert provider.get_active_event() is None

    def test_build_context_returns_dialogue_context(self) -> None:
        """build_context assembles a complete DialogueContext."""
        game = FakeGame()
        provider = GameContextProvider(game)
        ctx = provider.build_context(player_message="hello", triggers=["player_input"])

        assert isinstance(ctx, DialogueContext)
        assert ctx.player_message == "hello"
        assert "player_input" in ctx.triggers
        assert ctx.duck_mood == "curious"
        assert ctx.duck_trust == 42.0
        assert ctx.weather == "clear"
        assert ctx.time_of_day == "morning"
        assert ctx.season == "summer"

    def test_build_context_fallback_when_collected(self) -> None:
        """build_context returns a minimal context if the game is gone."""
        game = FakeGame()
        provider = GameContextProvider(game)
        del game
        gc.collect()

        ctx = provider.build_context(player_message="hey", triggers=["idle_timer"])
        assert isinstance(ctx, DialogueContext)
        assert ctx.player_message == "hey"
        assert ctx.triggers == ["idle_timer"]

    def test_current_location_from_duck(self) -> None:
        """get_current_location reads from game.duck.current_location."""
        game = FakeGame()
        provider = GameContextProvider(game)
        assert provider.get_current_location() == "pond_edge"

    def test_active_visitor_none_by_default(self) -> None:
        """get_active_visitor returns None when no visitor manager exists."""
        game = FakeGame()
        provider = GameContextProvider(game)
        assert provider.get_active_visitor() is None

    def test_active_event_none_by_default(self) -> None:
        """get_active_event returns None when no event manager exists."""
        game = FakeGame()
        provider = GameContextProvider(game)
        assert provider.get_active_event() is None
