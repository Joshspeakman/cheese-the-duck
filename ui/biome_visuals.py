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
# IMPORTANT: Values must be VERY DARK (0-45 range) to keep foreground elements
# visible.  These are subtle colour casts, not solid fills.  Daytime periods
# (morning, midday, afternoon) should be the subtlest since they previously
# had no background at all.
#
# Keys: biome enum .value strings   ×   time period strings
# Values: (R, G, B) — dark ambient background colour hint.

BIOME_TIME_TINTS: Dict[str, Dict[str, Tuple[int, int, int]]] = {
    "pond": {
        "dawn":       (35, 28, 18),   # Warm hint
        "morning":    (8, 14, 12),    # Very subtle teal
        "midday":     (6, 10, 8),     # Barely there
        "afternoon":  (8, 12, 10),
        "evening":    (30, 22, 10),   # Golden warmth
        "dusk":       (18, 16, 28),   # Purple tinge
        "night":      (6, 10, 22),    # Dark blue
        "late_night": (3, 5, 14),
    },
    "forest": {
        "dawn":       (22, 30, 12),   # Green-tinged dawn
        "morning":    (6, 16, 8),     # Dark green filter
        "midday":     (5, 14, 6),     # Canopy-filtered light
        "afternoon":  (6, 14, 7),
        "evening":    (24, 20, 8),    # Orange through trees
        "dusk":       (12, 18, 10),   # Dark forest dusk
        "night":      (3, 10, 5),     # Very dark green
        "late_night": (2, 6, 3),
    },
    "meadow": {
        "dawn":       (38, 30, 16),   # Warm golden dawn
        "morning":    (12, 14, 8),    # Light warm hint
        "midday":     (10, 12, 6),    # Subtle warmth
        "afternoon":  (12, 12, 7),
        "evening":    (35, 25, 10),   # Rich golden hour
        "dusk":       (22, 16, 20),   # Soft purple
        "night":      (8, 8, 18),     # Open sky dark blue
        "late_night": (4, 4, 12),
    },
    "riverside": {
        "dawn":       (30, 26, 18),
        "morning":    (8, 14, 16),    # Cool blue hint
        "midday":     (6, 12, 14),
        "afternoon":  (8, 12, 14),
        "evening":    (28, 22, 12),
        "dusk":       (16, 14, 24),
        "night":      (5, 8, 18),
        "late_night": (3, 5, 12),
    },
    "garden": {
        "dawn":       (32, 28, 16),
        "morning":    (10, 14, 8),
        "midday":     (8, 12, 6),
        "afternoon":  (10, 12, 7),
        "evening":    (30, 24, 10),
        "dusk":       (20, 16, 22),
        "night":      (6, 8, 16),
        "late_night": (3, 5, 10),
    },
    "mountains": {
        "dawn":       (28, 24, 22),   # Cool crisp dawn
        "morning":    (8, 12, 18),    # Clear blue hint
        "midday":     (6, 10, 16),    # Alpine clarity
        "afternoon":  (8, 10, 16),
        "evening":    (26, 20, 14),
        "dusk":       (14, 12, 24),   # Deep purple twilight
        "night":      (4, 5, 18),     # Clear dark sky
        "late_night": (2, 3, 12),
    },
    "beach": {
        "dawn":       (38, 28, 18),   # Warm sunrise
        "morning":    (10, 16, 20),   # Bright cyan hint
        "midday":     (8, 14, 18),    # Bright open sky
        "afternoon":  (10, 14, 18),
        "evening":    (36, 24, 12),   # Sunset warmth
        "dusk":       (22, 14, 20),
        "night":      (6, 8, 20),
        "late_night": (3, 5, 14),
    },
    "swamp": {
        "dawn":       (22, 28, 10),   # Murky green dawn
        "morning":    (8, 16, 6),     # Green murk
        "midday":     (6, 14, 5),     # Hazy green
        "afternoon":  (7, 14, 5),
        "evening":    (18, 20, 6),    # Sickly golden
        "dusk":       (10, 16, 8),    # Dark murk
        "night":      (4, 12, 3),     # Eerie dark green
        "late_night": (2, 8, 2),
    },
    "urban": {
        "dawn":       (28, 24, 20),   # Gray-warm
        "morning":    (12, 12, 14),   # Gray cast
        "midday":     (10, 10, 12),   # Neutral gray
        "afternoon":  (12, 12, 12),
        "evening":    (28, 22, 12),   # Streetlight warmth
        "dusk":       (20, 16, 14),   # Orange-gray
        "night":      (16, 12, 8),    # Streetlight amber glow
        "late_night": (10, 7, 4),     # Dim amber
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
