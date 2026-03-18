"""Tests for ui/biome_config.py — BiomeVisualConfig, lookups, and blending."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from ui.biome_config import (
    ALL_TIME_PERIODS,
    BiomeVisualConfig,
    BIOME_CONFIGS,
    validate_biome_configs,
    get_biome_tint,
    get_biome_particles,
    blend_tint,
)


# ═══════════════════════════════════════════════════════════════════════════
# BiomeVisualConfig dataclass
# ═══════════════════════════════════════════════════════════════════════════

class TestBiomeVisualConfig:
    """Tests for the BiomeVisualConfig dataclass."""

    def test_default_construction(self) -> None:
        """A config can be constructed with just a biome_id."""
        cfg = BiomeVisualConfig(biome_id="test")
        assert cfg.biome_id == "test"
        assert cfg.time_tints == {}
        assert cfg.ambient_particles == []
        assert isinstance(cfg.ground_chars, str)
        assert cfg.description == ""

    def test_custom_fields(self) -> None:
        """All fields can be set at construction time."""
        tints = {"dawn": (200, 150, 100)}
        cfg = BiomeVisualConfig(
            biome_id="custom",
            time_tints=tints,
            ambient_particles=[{"type": "leaf"}],
            ground_chars="~.",
            description="A custom biome.",
        )
        assert cfg.time_tints == tints
        assert len(cfg.ambient_particles) == 1
        assert cfg.ground_chars == "~."
        assert cfg.description == "A custom biome."


# ═══════════════════════════════════════════════════════════════════════════
# Module-level BIOME_CONFIGS
# ═══════════════════════════════════════════════════════════════════════════

class TestBiomeConfigs:
    """Tests for the auto-built BIOME_CONFIGS mapping."""

    def test_biome_configs_is_dict(self) -> None:
        """BIOME_CONFIGS is a non-empty dict."""
        assert isinstance(BIOME_CONFIGS, dict)
        assert len(BIOME_CONFIGS) > 0

    def test_pond_exists(self) -> None:
        """The 'pond' biome (duck's home) is always present."""
        assert "pond" in BIOME_CONFIGS
        cfg = BIOME_CONFIGS["pond"]
        assert cfg.biome_id == "pond"

    def test_all_configs_have_biome_id(self) -> None:
        """Every config's biome_id matches its dict key."""
        for key, cfg in BIOME_CONFIGS.items():
            assert cfg.biome_id == key


# ═══════════════════════════════════════════════════════════════════════════
# Validation
# ═══════════════════════════════════════════════════════════════════════════

class TestValidation:
    """Tests for validate_biome_configs."""

    def test_validate_complete_config(self) -> None:
        """A config with all 8 time periods produces no warnings."""
        full_tints = {period: (100, 100, 100) for period in ALL_TIME_PERIODS}
        configs = {
            "complete": BiomeVisualConfig(biome_id="complete", time_tints=full_tints)
        }
        warnings = validate_biome_configs(configs)
        assert warnings == []

    def test_validate_missing_period(self) -> None:
        """A config missing a time period produces a warning."""
        partial_tints = {period: (100, 100, 100) for period in ALL_TIME_PERIODS[:5]}
        configs = {
            "partial": BiomeVisualConfig(biome_id="partial", time_tints=partial_tints)
        }
        warnings = validate_biome_configs(configs)
        assert len(warnings) > 0
        assert any("partial" in w for w in warnings)

    def test_validate_empty_config(self) -> None:
        """A config with no tints at all produces 8 warnings."""
        configs = {
            "empty": BiomeVisualConfig(biome_id="empty", time_tints={})
        }
        warnings = validate_biome_configs(configs)
        assert len(warnings) == len(ALL_TIME_PERIODS)


# ═══════════════════════════════════════════════════════════════════════════
# Lookup helpers
# ═══════════════════════════════════════════════════════════════════════════

class TestLookupHelpers:
    """Tests for get_biome_tint and get_biome_particles."""

    def test_get_biome_tint_valid(self) -> None:
        """Looking up a valid biome+time returns an RGB tuple."""
        # pond should have at least some time periods defined
        tint = get_biome_tint("pond", "midday")
        if tint is not None:
            assert isinstance(tint, tuple)
            assert len(tint) == 3
            assert all(isinstance(c, int) for c in tint)

    def test_get_biome_tint_unknown_biome(self) -> None:
        """An unknown biome returns None."""
        assert get_biome_tint("atlantis", "dawn") is None

    def test_get_biome_tint_unknown_time(self) -> None:
        """An unknown time period returns None."""
        assert get_biome_tint("pond", "nonexistent_time") is None

    def test_get_biome_particles_valid(self) -> None:
        """get_biome_particles returns a list for a known biome."""
        particles = get_biome_particles("pond")
        assert isinstance(particles, list)

    def test_get_biome_particles_unknown(self) -> None:
        """An unknown biome returns an empty list."""
        assert get_biome_particles("atlantis") == []


# ═══════════════════════════════════════════════════════════════════════════
# blend_tint
# ═══════════════════════════════════════════════════════════════════════════

class TestBlendTint:
    """Tests for the blend_tint colour interpolation utility."""

    def test_factor_zero_returns_base(self) -> None:
        """factor=0.0 returns the base colour unchanged."""
        result = blend_tint((100, 150, 200), (0, 0, 0), factor=0.0)
        assert result == (100, 150, 200)

    def test_factor_one_returns_biome(self) -> None:
        """factor=1.0 returns the biome colour unchanged."""
        result = blend_tint((0, 0, 0), (100, 150, 200), factor=1.0)
        assert result == (100, 150, 200)

    def test_factor_half_blends(self) -> None:
        """factor=0.5 blends evenly between base and biome."""
        result = blend_tint((0, 0, 0), (200, 100, 50), factor=0.5)
        assert result == (100, 50, 25)

    def test_clamping_high(self) -> None:
        """Values above 255 are clamped."""
        result = blend_tint((250, 250, 250), (255, 255, 255), factor=0.5)
        assert all(0 <= c <= 255 for c in result)

    def test_clamping_low(self) -> None:
        """Values below 0 are clamped."""
        result = blend_tint((10, 10, 10), (0, 0, 0), factor=2.0)
        assert all(0 <= c <= 255 for c in result)
