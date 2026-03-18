"""
Validated biome visual configuration.

Consolidates biome time-tints and ambient particle data from
``ui/biome_visuals.py`` into validated :class:`BiomeVisualConfig` dataclass
instances.  Provides lookup helpers and colour blending utilities.

At import time, :func:`validate_biome_configs` checks that every known biome
has tints for all 8 time periods and logs warnings for any gaps.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# The 8 canonical time-period keys used throughout the game.
ALL_TIME_PERIODS = (
    "dawn", "morning", "midday", "afternoon",
    "evening", "dusk", "night", "late_night",
)


@dataclass
class BiomeVisualConfig:
    """Complete visual configuration for a single biome.

    Attributes:
        biome_id: Biome identifier (e.g. ``"pond"``, ``"forest"``).
        time_tints: Mapping of time-period key to ``(R, G, B)`` background tint.
            Must have entries for all 8 time periods to be fully valid.
        ambient_particles: Particle config dicts for this biome (same schema as
            ``BIOME_AMBIENT_PARTICLES`` entries in ``biome_visuals.py``).
        ground_chars: Default ground characters for the playfield.
        description: Human-readable biome description.
    """
    biome_id: str
    time_tints: Dict[str, Tuple[int, int, int]] = field(default_factory=dict)
    ambient_particles: List[dict] = field(default_factory=list)
    ground_chars: str = ".,'\u00b7 "
    description: str = ""


# ── Build validated configs from existing data ────────────────────────────────

def _build_biome_configs() -> Dict[str, BiomeVisualConfig]:
    """Construct ``BIOME_CONFIGS`` from the raw dicts in ``biome_visuals``."""
    from ui.biome_visuals import BIOME_TIME_TINTS, BIOME_AMBIENT_PARTICLES

    _DESCRIPTIONS: Dict[str, str] = {
        "pond": "A quiet pond surrounded by reeds -- the duck's home base.",
        "forest": "A dense canopy filters the light through green leaves.",
        "meadow": "Wide open grasslands under big skies.",
        "riverside": "A babbling river with misty banks.",
        "garden": "A lovingly tended garden with flowers and paths.",
        "mountains": "High altitude with crisp air and wind-swept ridges.",
        "beach": "Sun, sand, and the sound of waves.",
        "swamp": "Murky waters and eerie fog among twisted trees.",
        "urban": "A city park with streetlights and pigeons.",
    }

    _GROUND_CHARS: Dict[str, str] = {
        "pond": "~.,\u00b7 ",
        "forest": ".,'\u00b7#",
        "meadow": ".,'\u00b7 ",
        "riverside": "~.,\u00b7 ",
        "garden": ".,*\u00b7 ",
        "mountains": ".^,\u00b7#",
        "beach": ".,~\u00b7 ",
        "swamp": "~.,\u00b7#",
        "urban": ".,_\u00b7 ",
    }

    configs: Dict[str, BiomeVisualConfig] = {}

    # Start from the set of all biomes that appear in either data source
    all_biomes = set(BIOME_TIME_TINTS.keys()) | set(BIOME_AMBIENT_PARTICLES.keys())

    for biome_id in sorted(all_biomes):
        tints = BIOME_TIME_TINTS.get(biome_id, {})
        particles = BIOME_AMBIENT_PARTICLES.get(biome_id, [])
        configs[biome_id] = BiomeVisualConfig(
            biome_id=biome_id,
            time_tints=dict(tints),  # defensive copy
            ambient_particles=[dict(p) for p in particles],
            ground_chars=_GROUND_CHARS.get(biome_id, ".,'\u00b7 "),
            description=_DESCRIPTIONS.get(biome_id, ""),
        )

    return configs


def validate_biome_configs(configs: Optional[Dict[str, BiomeVisualConfig]] = None) -> List[str]:
    """Validate that every biome has tints for all 8 time periods.

    Returns a list of warning strings (empty means all valid).  Also logs
    each warning via the ``logging`` module at WARNING level.
    """
    if configs is None:
        configs = BIOME_CONFIGS

    warnings: List[str] = []
    for biome_id, cfg in configs.items():
        for period in ALL_TIME_PERIODS:
            if period not in cfg.time_tints:
                msg = f"Biome '{biome_id}' missing time-tint for '{period}'"
                warnings.append(msg)
                logger.warning(msg)
    return warnings


# ── Module-level validated config ─────────────────────────────────────────────

BIOME_CONFIGS: Dict[str, BiomeVisualConfig] = _build_biome_configs()

# Run validation at import time (logs warnings but does not raise)
_validation_warnings = validate_biome_configs(BIOME_CONFIGS)


# ── Public lookup helpers ─────────────────────────────────────────────────────

def get_biome_tint(biome: str, time_key: str) -> Optional[Tuple[int, int, int]]:
    """Look up the RGB background tint for *biome* at *time_key*.

    Returns ``None`` if the biome or time key is unknown.
    """
    cfg = BIOME_CONFIGS.get(biome)
    if cfg:
        return cfg.time_tints.get(time_key)
    return None


def get_biome_particles(biome: str) -> List[dict]:
    """Return the raw ambient particle config dicts for *biome*.

    Returns an empty list for unknown biomes.
    """
    cfg = BIOME_CONFIGS.get(biome)
    if cfg:
        return cfg.ambient_particles
    return []


def blend_tint(
    base: Tuple[int, int, int],
    biome: Tuple[int, int, int],
    factor: float = 0.6,
) -> Tuple[int, int, int]:
    """Linearly interpolate between *base* and *biome* RGB colours.

    This is the same blend used in ``biome_visuals.blend_tint`` and
    ``renderer._get_time_of_day_elements``.

    Args:
        base: Base RGB colour (e.g. global time-of-day tint).
        biome: Biome-specific RGB colour.
        factor: Blend factor where 0.0 = pure *base* and 1.0 = pure *biome*.

    Returns:
        Blended ``(R, G, B)`` tuple with values clamped to 0 -- 255.
    """
    r = int(base[0] + (biome[0] - base[0]) * factor)
    g = int(base[1] + (biome[1] - base[1]) * factor)
    b = int(base[2] + (biome[2] - base[2]) * factor)
    return (
        max(0, min(255, r)),
        max(0, min(255, g)),
        max(0, min(255, b)),
    )
