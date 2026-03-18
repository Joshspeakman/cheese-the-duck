"""Tests for ui/render_context.py — RenderContext dataclass construction."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from ui.render_context import RenderContext


# ═══════════════════════════════════════════════════════════════════════════
# Default construction
# ═══════════════════════════════════════════════════════════════════════════

class TestRenderContextDefaults:
    """Tests for RenderContext default values."""

    def test_default_duck_position(self) -> None:
        """Default duck position is (0, 0)."""
        ctx = RenderContext()
        assert ctx.duck_x == 0
        assert ctx.duck_y == 0

    def test_default_duck_state(self) -> None:
        """Default duck state fields have sensible values."""
        ctx = RenderContext()
        assert ctx.duck_state == "idle"
        assert ctx.duck_animation_frame == 0
        assert ctx.duck_facing_right is True
        assert ctx.duck_growth_stage == "duckling"
        assert ctx.duck_name == "Cheese"
        assert ctx.duck_mood == "content"
        assert ctx.duck_trust == 0.5

    def test_default_needs(self) -> None:
        """Default needs are all 1.0 (fully satisfied)."""
        ctx = RenderContext()
        assert ctx.duck_needs == {
            "hunger": 1.0,
            "energy": 1.0,
            "fun": 1.0,
            "cleanliness": 1.0,
            "social": 1.0,
        }

    def test_default_world_state(self) -> None:
        """Default world-state fields."""
        ctx = RenderContext()
        assert ctx.time_of_day == "midday"
        assert ctx.season == "spring"
        assert ctx.weather_type is None
        assert ctx.weather_intensity == 0.0
        assert ctx.current_biome == "pond"
        assert ctx.current_location is None

    def test_default_progression(self) -> None:
        """Default progression fields."""
        ctx = RenderContext()
        assert ctx.level == 1
        assert ctx.xp_progress == 0.0
        assert ctx.growth_progress == 0.0
        assert ctx.goals_completed == 0
        assert ctx.goals_total == 0
        assert ctx.coins == 0

    def test_default_terminal(self) -> None:
        """Default terminal size is 80x24."""
        ctx = RenderContext()
        assert ctx.terminal_width == 80
        assert ctx.terminal_height == 24

    def test_default_collections_empty(self) -> None:
        """Default collection fields are empty."""
        ctx = RenderContext()
        assert ctx.chat_messages == []
        assert ctx.particles == []
        assert ctx.visitors == []
        assert ctx.habitat_items == []
        assert ctx.duck_cosmetics == []

    def test_default_overlay(self) -> None:
        """Default overlay state is inactive."""
        ctx = RenderContext()
        assert ctx.active_overlay == ""
        assert ctx.menu_items is None
        assert ctx.menu_selected == 0


# ═══════════════════════════════════════════════════════════════════════════
# Custom construction
# ═══════════════════════════════════════════════════════════════════════════

class TestRenderContextCustom:
    """Tests for constructing RenderContext with custom values."""

    def test_custom_duck_position(self) -> None:
        """Custom duck position is stored correctly."""
        ctx = RenderContext(duck_x=42, duck_y=17)
        assert ctx.duck_x == 42
        assert ctx.duck_y == 17

    def test_custom_world_state(self) -> None:
        """Custom world state values are stored correctly."""
        ctx = RenderContext(
            time_of_day="night",
            season="winter",
            weather_type="snow",
            weather_intensity=0.8,
            current_biome="mountains",
            current_location="Summit",
        )
        assert ctx.time_of_day == "night"
        assert ctx.season == "winter"
        assert ctx.weather_type == "snow"
        assert ctx.weather_intensity == 0.8
        assert ctx.current_biome == "mountains"
        assert ctx.current_location == "Summit"

    def test_custom_chat_messages(self) -> None:
        """Chat messages store (role, text) tuples."""
        msgs = [("user", "Hello"), ("assistant", "Quack!")]
        ctx = RenderContext(chat_messages=msgs)
        assert len(ctx.chat_messages) == 2
        assert ctx.chat_messages[0] == ("user", "Hello")
        assert ctx.chat_messages[1] == ("assistant", "Quack!")

    def test_custom_overlay_and_menu(self) -> None:
        """Menu/overlay state can be set at construction."""
        ctx = RenderContext(
            active_overlay="shop",
            menu_items=["Hat", "Scarf", "Boots"],
            menu_selected=1,
        )
        assert ctx.active_overlay == "shop"
        assert ctx.menu_items == ["Hat", "Scarf", "Boots"]
        assert ctx.menu_selected == 1


# ═══════════════════════════════════════════════════════════════════════════
# Isolation between instances
# ═══════════════════════════════════════════════════════════════════════════

class TestRenderContextIsolation:
    """Ensure mutable default fields are not shared between instances."""

    def test_needs_are_independent(self) -> None:
        """Mutating needs on one context does not affect another."""
        a = RenderContext()
        b = RenderContext()
        a.duck_needs["hunger"] = 0.0
        assert b.duck_needs["hunger"] == 1.0

    def test_chat_messages_are_independent(self) -> None:
        """Mutating chat_messages on one context does not affect another."""
        a = RenderContext()
        b = RenderContext()
        a.chat_messages.append(("user", "test"))
        assert b.chat_messages == []

    def test_particles_are_independent(self) -> None:
        """Mutating particles on one context does not affect another."""
        a = RenderContext()
        b = RenderContext()
        a.particles.append((1, 2, "*", (255, 255, 255)))
        assert b.particles == []
