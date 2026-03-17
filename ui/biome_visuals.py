"""
Biome-specific visual atmosphere data.

Provides per-biome lighting tints (varying by time of day), seasonal color
overrides for ground and decorations, and ambient particle configurations
(fireflies, falling leaves, mist, etc.).

All data is pure dicts/tuples — no classes, no heavy logic.
"""
import random
from typing import Dict, List, Optional, Tuple


# ── Biome × Time-of-Day Background Tints ────────────────────────────────────
# Each biome has an RGB tint for each time period.  These are blended with the
# global time-of-day base colour in renderer._get_time_of_day_elements().
#
# Keys: biome enum .value strings   ×   time period strings
# Values: (R, G, B) absolute background colour for that combo.

BIOME_TIME_TINTS: Dict[str, Dict[str, Tuple[int, int, int]]] = {
    "pond": {
        "dawn":       (220, 200, 160),
        "morning":    (180, 210, 200),
        "midday":     (200, 220, 210),
        "afternoon":  (190, 210, 200),
        "evening":    (210, 180, 120),
        "dusk":       (90, 85, 110),
        "night":      (15, 20, 35),
        "late_night": (8, 10, 22),
    },
    "forest": {
        "dawn":       (180, 200, 140),
        "morning":    (140, 185, 130),
        "midday":     (120, 170, 110),
        "afternoon":  (135, 175, 120),
        "evening":    (160, 150, 80),
        "dusk":       (60, 70, 50),
        "night":      (8, 16, 10),
        "late_night": (4, 10, 6),
    },
    "meadow": {
        "dawn":       (240, 210, 170),
        "morning":    (210, 220, 180),
        "midday":     (230, 235, 200),
        "afternoon":  (220, 215, 175),
        "evening":    (230, 190, 110),
        "dusk":       (110, 90, 100),
        "night":      (18, 18, 35),
        "late_night": (10, 10, 20),
    },
    "riverside": {
        "dawn":       (210, 200, 170),
        "morning":    (180, 210, 215),
        "midday":     (200, 225, 230),
        "afternoon":  (190, 215, 210),
        "evening":    (200, 175, 120),
        "dusk":       (85, 80, 110),
        "night":      (12, 18, 30),
        "late_night": (6, 10, 20),
    },
    "garden": {
        "dawn":       (225, 210, 165),
        "morning":    (195, 215, 180),
        "midday":     (215, 225, 200),
        "afternoon":  (205, 215, 185),
        "evening":    (220, 185, 115),
        "dusk":       (100, 88, 105),
        "night":      (15, 18, 30),
        "late_night": (8, 10, 20),
    },
    "mountains": {
        "dawn":       (210, 195, 185),
        "morning":    (190, 210, 230),
        "midday":     (210, 225, 245),
        "afternoon":  (200, 215, 235),
        "evening":    (195, 170, 140),
        "dusk":       (80, 75, 110),
        "night":      (10, 12, 30),
        "late_night": (5, 6, 18),
    },
    "beach": {
        "dawn":       (245, 210, 175),
        "morning":    (210, 230, 245),
        "midday":     (230, 240, 250),
        "afternoon":  (220, 235, 245),
        "evening":    (240, 185, 120),
        "dusk":       (110, 85, 105),
        "night":      (15, 18, 35),
        "late_night": (8, 10, 22),
    },
    "swamp": {
        "dawn":       (170, 180, 120),
        "morning":    (140, 160, 110),
        "midday":     (150, 165, 115),
        "afternoon":  (145, 160, 110),
        "evening":    (140, 140, 80),
        "dusk":       (60, 65, 45),
        "night":      (10, 18, 8),
        "late_night": (5, 12, 5),
    },
    "urban": {
        "dawn":       (200, 190, 175),
        "morning":    (195, 200, 205),
        "midday":     (210, 215, 215),
        "afternoon":  (205, 208, 210),
        "evening":    (200, 175, 130),
        "dusk":       (100, 90, 85),
        "night":      (25, 20, 15),
        "late_night": (18, 14, 10),
    },
}


# ── Seasonal Ground Colour Overrides ─────────────────────────────────────────
# Terminal colour index overrides per location per season.
# Only locations/seasons that DIFFER from the static default need entries.

SEASONAL_GROUND_COLORS: Dict[str, Dict[str, int]] = {
    # Forest locations
    "Forest Edge": {
        "spring": 28,    # Bright fresh green
        "fall":   130,   # Orange-brown
        "winter": 94,    # Dark bare brown
    },
    "Ancient Oak": {
        "spring": 28,
        "fall":   130,
        "winter": 236,   # Dark gray-brown
    },
    "Mushroom Grove": {
        "spring": 22,    # Dark green (more alive)
        "fall":   95,    # Muted purple-brown
        "winter": 236,
    },
    # Meadow locations
    "Sunny Meadow": {
        "spring": 40,    # Vivid green with growth
        "fall":   178,   # Golden yellow
        "winter": 250,   # Frost white-gray
    },
    "Butterfly Garden": {
        "spring": 40,
        "fall":   178,
        "winter": 250,
    },
    # Pond locations
    "Home Pond": {
        "spring": 28,    # Lush green shore
        "fall":   58,    # Olive-brown
        "winter": 240,   # Gray frost
    },
    "Deep End": {
        "winter": 60,    # Icy blue
    },
    # Riverside
    "Pebble Beach": {
        "winter": 255,   # Frosted white-gray
    },
    "Waterfall": {
        "winter": 60,    # Icy blue
    },
    # Garden
    "Vegetable Patch": {
        "spring": 28,    # Freshly tilled green
        "fall":   130,   # Harvest brown
        "winter": 240,   # Dormant gray
    },
    # Swamp — always murky, subtle seasonal shift
    "Misty Marsh": {
        "fall":   58,    # Brown-green decay
        "winter": 236,   # Dark frozen murk
    },
    "Cypress Hollow": {
        "fall":   94,    # Brown
        "winter": 236,
    },
    # Mountains — snow in winter
    "Foothills": {
        "winter": 255,   # Snow-covered
    },
    "Crystal Cave": {},  # Underground — no change
    # Beach — minimal change
    "Sandy Shore": {
        "winter": 253,   # Slightly paler sand
    },
}


# ── Seasonal Decoration Colour Overrides ─────────────────────────────────────
# Per-season colour overrides for specific decoration characters.
# Values are lists of (R, G, B) tuples — one is picked at random for variety.
# Only chars that actually change appearance need entries.

SEASONAL_DECORATION_OVERRIDES: Dict[str, Dict[str, List[Tuple[int, int, int]]]] = {
    "spring": {
        "A": [(80, 210, 70), (100, 230, 90), (60, 200, 80)],     # Fresh bright greens
        "+": [(70, 190, 60), (90, 210, 80)],                       # Fresh bushes
        "*": [(255, 150, 200), (255, 200, 100), (200, 150, 255),
               (255, 180, 180), (180, 220, 255)],                  # Colourful spring flowers
    },
    "summer": {
        "A": [(40, 160, 40), (50, 180, 50), (30, 150, 30)],       # Deep lush greens
        "+": [(45, 160, 45), (35, 150, 35)],                       # Full bushes
    },
    "fall": {
        "A": [(200, 100, 30), (220, 80, 40), (180, 120, 20),
               (210, 140, 40), (190, 60, 30)],                     # Orange/red/gold foliage
        "+": [(160, 130, 40), (170, 110, 30)],                     # Brownish bushes
        "'": [(180, 160, 80), (170, 150, 70)],                     # Dry golden grass
    },
    "winter": {
        "A": [(180, 180, 190), (170, 175, 185), (190, 190, 200)], # Gray-white bare branches
        "+": [(200, 200, 210), (190, 195, 205)],                   # Snow-dusted bushes
        "'": [(220, 220, 235), (210, 215, 230)],                   # Frost-covered grass
        "*": [(230, 230, 240), (220, 225, 235)],                   # Frost-tipped flowers (dormant)
    },
}

# Locations where seasonal decoration overrides should NOT apply
# (underground, indoor, or environments that don't change with seasons)
_NO_SEASONAL_DECORATION_LOCATIONS = frozenset({
    "Crystal Cave", "Tool Shed", "Storm Drain",
})


# ── Biome Ambient Particles ──────────────────────────────────────────────────
# Per-biome ambient particle configs.  Each entry is a dict:
#   chars:     list of character options for the particle
#   color_rgb: (R, G, B) colour
#   density:   spawn probability per cell per update (keep low!)
#   speed:     cells per update tick
#   direction: "fall" | "float" | "drift_right" | "drift_left" | "static"
#   time:      list of time periods when active, or None for always
#   season:    list of seasons when active, or None for always

BIOME_AMBIENT_PARTICLES: Dict[str, List[dict]] = {
    "swamp": [
        {
            "chars": ["*", ".", "\u00b7"],
            "color_rgb": (160, 240, 80),
            "density": 0.012,
            "speed": 0.08,
            "direction": "float",
            "time": ["night", "late_night", "dusk", "evening"],
            "season": None,
        },
        {
            "chars": [".", "~", "\u00b7"],
            "color_rgb": (140, 150, 120),
            "density": 0.008,
            "speed": 0.04,
            "direction": "drift_right",
            "time": None,
            "season": None,
        },
    ],
    "forest": [
        {
            "chars": ["{", "}", ",", "'"],
            "color_rgb": (200, 120, 40),
            "density": 0.015,
            "speed": 0.25,
            "direction": "fall",
            "time": None,
            "season": ["fall"],
        },
        {
            "chars": [".", "\u00b7", "o"],
            "color_rgb": (220, 240, 120),
            "density": 0.006,
            "speed": 0.03,
            "direction": "float",
            "time": None,
            "season": ["spring"],
        },
        {
            "chars": ["*", "\u00b7"],
            "color_rgb": (255, 255, 190),
            "density": 0.004,
            "speed": 0.0,
            "direction": "static",
            "time": ["midday", "afternoon"],
            "season": ["summer"],
        },
    ],
    "beach": [
        {
            "chars": [".", ",", "\u00b7"],
            "color_rgb": (210, 195, 150),
            "density": 0.008,
            "speed": 0.35,
            "direction": "drift_right",
            "time": None,
            "season": None,
        },
    ],
    "mountains": [
        {
            "chars": ["-", "~", ">"],
            "color_rgb": (195, 205, 215),
            "density": 0.010,
            "speed": 0.45,
            "direction": "drift_right",
            "time": None,
            "season": None,
        },
        {
            "chars": ["*", ".", "\u00b7"],
            "color_rgb": (235, 235, 250),
            "density": 0.010,
            "speed": 0.18,
            "direction": "fall",
            "time": None,
            "season": ["winter"],
        },
    ],
    "meadow": [
        {
            "chars": ["~", "'", "."],
            "color_rgb": (255, 255, 200),
            "density": 0.005,
            "speed": 0.12,
            "direction": "float",
            "time": ["morning", "midday", "afternoon"],
            "season": ["spring", "summer"],
        },
        {
            "chars": ["o", "\u00b7"],
            "color_rgb": (240, 240, 220),
            "density": 0.006,
            "speed": 0.10,
            "direction": "drift_right",
            "time": None,
            "season": ["fall"],
        },
    ],
    "riverside": [
        {
            "chars": [".", "\u00b7", "'"],
            "color_rgb": (180, 210, 230),
            "density": 0.005,
            "speed": 0.06,
            "direction": "float",
            "time": None,
            "season": None,
        },
    ],
    "garden": [
        {
            "chars": ["\u00b7", "*"],
            "color_rgb": (255, 200, 150),
            "density": 0.004,
            "speed": 0.05,
            "direction": "float",
            "time": ["morning", "midday", "afternoon"],
            "season": ["spring", "summer"],
        },
    ],
    "urban": [
        {
            "chars": ["\u00b7", "."],
            "color_rgb": (200, 190, 170),
            "density": 0.003,
            "speed": 0.15,
            "direction": "drift_right",
            "time": None,
            "season": None,
        },
    ],
    "pond": [
        {
            "chars": ["*", "\u00b7"],
            "color_rgb": (140, 220, 80),
            "density": 0.008,
            "speed": 0.06,
            "direction": "float",
            "time": ["night", "late_night", "dusk"],
            "season": ["summer"],
        },
    ],
}


# ── Helper Functions ─────────────────────────────────────────────────────────

def blend_tint(
    base_rgb: Tuple[int, int, int],
    biome_rgb: Tuple[int, int, int],
    factor: float = 0.5,
) -> Tuple[int, int, int]:
    """Linearly interpolate between two RGB colours."""
    return (
        int(base_rgb[0] + (biome_rgb[0] - base_rgb[0]) * factor),
        int(base_rgb[1] + (biome_rgb[1] - base_rgb[1]) * factor),
        int(base_rgb[2] + (biome_rgb[2] - base_rgb[2]) * factor),
    )


def get_biome_time_tint(
    biome: str, time_of_day: str
) -> Optional[Tuple[int, int, int]]:
    """Look up the RGB tint for a biome at a given time of day."""
    biome_tints = BIOME_TIME_TINTS.get(biome)
    if biome_tints:
        return biome_tints.get(time_of_day)
    return None


def get_seasonal_ground_color(location: str, season: str) -> Optional[int]:
    """Get seasonal terminal colour index override for a location's ground."""
    loc_seasons = SEASONAL_GROUND_COLORS.get(location)
    if loc_seasons:
        return loc_seasons.get(season)
    return None


def get_seasonal_decoration_color(
    char: str, season: str, location: str = ""
) -> Optional[Tuple[int, int, int]]:
    """Get seasonal RGB override for a decoration character.

    Returns a randomly chosen colour from the override list for variety,
    or None if no override applies.
    """
    if location in _NO_SEASONAL_DECORATION_LOCATIONS:
        return None

    season_overrides = SEASONAL_DECORATION_OVERRIDES.get(season)
    if season_overrides:
        options = season_overrides.get(char)
        if options:
            return random.choice(options)
    return None


def get_ambient_particles(
    biome: str, time_of_day: str, season: str
) -> List[dict]:
    """Return the list of active ambient particle configs for the current state."""
    configs = BIOME_AMBIENT_PARTICLES.get(biome, [])
    active = []
    for cfg in configs:
        # Filter by time of day
        if cfg["time"] is not None and time_of_day not in cfg["time"]:
            continue
        # Filter by season
        if cfg.get("season") is not None and season not in cfg["season"]:
            continue
        active.append(cfg)
    return active
