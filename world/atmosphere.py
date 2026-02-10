"""
Atmosphere system - Weather, Seasons, Lucky Days, and Rare Visitors.
Creates dynamic, engaging world that changes over time (Animal Crossing style).
"""
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


# =============================================================================
# WEATHER SYSTEM
# =============================================================================

class WeatherType(Enum):
    """Types of weather that affect gameplay."""
    # === COMMON (all seasons) ===
    SUNNY = "sunny"
    PARTLY_CLOUDY = "partly_cloudy"
    CLOUDY = "cloudy"
    OVERCAST = "overcast"
    WINDY = "windy"
    FOGGY = "foggy"
    MISTY = "misty"
    
    # === RAIN VARIATIONS ===
    DRIZZLE = "drizzle"
    RAINY = "rainy"
    HEAVY_RAIN = "heavy_rain"
    STORMY = "stormy"
    THUNDERSTORM = "thunderstorm"
    
    # === SNOW/ICE VARIATIONS ===
    LIGHT_SNOW = "light_snow"
    SNOWY = "snowy"
    HEAVY_SNOW = "heavy_snow"
    BLIZZARD = "blizzard"
    SLEET = "sleet"
    HAIL = "hail"
    FROST = "frost"
    ICE_STORM = "ice_storm"
    
    # === SPRING SPECIFIC ===
    SPRING_SHOWERS = "spring_showers"
    RAINBOW = "rainbow"
    POLLEN_DRIFT = "pollen_drift"
    WARM_BREEZE = "warm_breeze"
    DEWY_MORNING = "dewy_morning"
    
    # === SUMMER SPECIFIC ===
    SCORCHING = "scorching"
    HUMID = "humid"
    HEAT_WAVE = "heat_wave"
    SUMMER_STORM = "summer_storm"
    BALMY_EVENING = "balmy_evening"
    GOLDEN_HOUR = "golden_hour"
    MUGGY = "muggy"
    
    # === FALL SPECIFIC ===
    CRISP = "crisp"
    BREEZY = "breezy"
    LEAF_STORM = "leaf_storm"
    HARVEST_MOON = "harvest_moon"
    FIRST_FROST = "first_frost"
    AUTUMNAL = "autumnal"
    
    # === WINTER SPECIFIC ===
    BITTER_COLD = "bitter_cold"
    FREEZING = "freezing"
    CLEAR_COLD = "clear_cold"
    SNOW_FLURRIES = "snow_flurries"
    WINTER_SUN = "winter_sun"
    
    # === RARE/SPECIAL ===
    AURORA = "aurora"
    METEOR_SHOWER = "meteor_shower"
    DOUBLE_RAINBOW = "double_rainbow"
    PERFECT_DAY = "perfect_day"


@dataclass
class Weather:
    """Current weather state."""
    weather_type: WeatherType
    intensity: float  # 0.0 to 1.0
    duration_hours: float
    start_time: str  # ISO datetime

    # Gameplay effects
    mood_modifier: int = 0
    xp_multiplier: float = 1.0
    special_message: str = ""

    def is_active(self) -> bool:
        """Check if weather is still active."""
        try:
            start = datetime.fromisoformat(self.start_time)
            elapsed = (datetime.now() - start).total_seconds() / 3600
            return elapsed < self.duration_hours
        except (ValueError, TypeError, AttributeError):
            return False


# ── Weather → need decay modifiers ──────────────────────────────────────
# Maps weather categories to multipliers on each need's decay rate.
# Values > 1.0 = need decays faster; < 1.0 = need decays slower.
# None/missing entries default to 1.0 (no effect).
# Grouped by weather "feel" for maintainability.

_WEATHER_NEED_GROUPS = {
    # Hot weather: energy drains faster, hunger too (sweating), cleanliness slower (dry)
    "hot": {"energy": 1.3, "hunger": 1.2, "cleanliness": 0.8},
    # Cold weather: hunger drains faster (body heat), energy slightly faster
    "cold": {"hunger": 1.3, "energy": 1.15},
    # Wet weather: cleanliness drains faster (mud/puddles), fun slightly faster (bored indoors)
    "wet": {"cleanliness": 1.4, "fun": 1.1},
    # Harsh weather: energy drains fast, fun drains (scary/stressful), social need rises (huddle)
    "harsh": {"energy": 1.4, "fun": 1.3, "social": 1.2},
    # Pleasant weather: everything a bit slower (nice day!)
    "pleasant": {"hunger": 0.9, "energy": 0.9, "fun": 0.8, "social": 0.9},
    # Boring weather: fun drains faster
    "boring": {"fun": 1.2},
    # Magical weather: everything slows down (wonder!)
    "magical": {"fun": 0.6, "social": 0.8, "energy": 0.9},
}

_WEATHER_TYPE_TO_GROUP = {
    # Hot
    WeatherType.SCORCHING: "hot", WeatherType.HEAT_WAVE: "hot",
    WeatherType.HUMID: "hot", WeatherType.MUGGY: "hot",
    WeatherType.BALMY_EVENING: "hot",
    # Cold
    WeatherType.BITTER_COLD: "cold", WeatherType.FREEZING: "cold",
    WeatherType.CLEAR_COLD: "cold", WeatherType.FROST: "cold",
    WeatherType.FIRST_FROST: "cold", WeatherType.SNOW_FLURRIES: "cold",
    WeatherType.LIGHT_SNOW: "cold", WeatherType.SNOWY: "cold",
    # Wet
    WeatherType.RAINY: "wet", WeatherType.HEAVY_RAIN: "wet",
    WeatherType.DRIZZLE: "wet", WeatherType.SPRING_SHOWERS: "wet",
    WeatherType.SLEET: "wet", WeatherType.POLLEN_DRIFT: "wet",
    # Harsh
    WeatherType.STORMY: "harsh", WeatherType.THUNDERSTORM: "harsh",
    WeatherType.BLIZZARD: "harsh", WeatherType.HEAVY_SNOW: "harsh",
    WeatherType.ICE_STORM: "harsh", WeatherType.SUMMER_STORM: "harsh",
    WeatherType.HAIL: "harsh", WeatherType.LEAF_STORM: "harsh",
    # Pleasant
    WeatherType.SUNNY: "pleasant", WeatherType.WARM_BREEZE: "pleasant",
    WeatherType.GOLDEN_HOUR: "pleasant", WeatherType.DEWY_MORNING: "pleasant",
    WeatherType.RAINBOW: "pleasant", WeatherType.CRISP: "pleasant",
    WeatherType.WINTER_SUN: "pleasant", WeatherType.PERFECT_DAY: "pleasant",
    WeatherType.HARVEST_MOON: "pleasant", WeatherType.AUTUMNAL: "pleasant",
    # Boring
    WeatherType.OVERCAST: "boring", WeatherType.CLOUDY: "boring",
    WeatherType.FOGGY: "boring", WeatherType.MISTY: "boring",
    WeatherType.PARTLY_CLOUDY: "boring", WeatherType.WINDY: "boring",
    WeatherType.BREEZY: "boring",
    # Magical
    WeatherType.AURORA: "magical", WeatherType.METEOR_SHOWER: "magical",
    WeatherType.DOUBLE_RAINBOW: "magical",
}


def get_weather_need_modifiers(weather) -> Dict[str, float]:
    """Get need decay multipliers for the current weather.
    
    Args:
        weather: A Weather instance or None
        
    Returns:
        Dict mapping need names to decay multipliers (1.0 = normal).
        Hot weather drains energy/hunger faster. Rain dirties the duck.
        Pleasant days slow everything down. Harsh storms are stressful.
    """
    default = {"hunger": 1.0, "energy": 1.0, "fun": 1.0, "cleanliness": 1.0, "social": 1.0}
    if weather is None:
        return default
    
    group = _WEATHER_TYPE_TO_GROUP.get(weather.weather_type)
    if group is None:
        return default
    
    mods = _WEATHER_NEED_GROUPS.get(group, {})
    result = default.copy()
    
    # Scale effect by weather intensity (0.3-1.0)
    intensity = getattr(weather, 'intensity', 0.7)
    for need, mult in mods.items():
        # Lerp between 1.0 and mult based on intensity
        result[need] = 1.0 + (mult - 1.0) * intensity
    
    return result


# =============================================================================
# BIOME-SPECIFIC WEATHER MODIFIERS
# =============================================================================
# Multiplies the base seasonal probability for each weather type per biome.
# Values > 1.0 = more likely in this biome; < 1.0 = less likely.
# Missing entries default to 1.0 (no modification).

_ALL_BIOMES = ["pond", "forest", "meadow", "riverside", "garden", "mountains", "beach", "swamp", "urban"]

BIOME_WEATHER_MODIFIERS: Dict[str, Dict] = {
    "pond": {},  # Home base — default season probabilities
    "forest": {
        WeatherType.FOGGY: 2.0, WeatherType.MISTY: 2.0, WeatherType.OVERCAST: 1.5,
        WeatherType.DEWY_MORNING: 2.0, WeatherType.DRIZZLE: 1.5,
        WeatherType.SCORCHING: 0.3, WeatherType.HEAT_WAVE: 0.3,
    },
    "meadow": {
        WeatherType.SUNNY: 1.5, WeatherType.WARM_BREEZE: 2.0, WeatherType.POLLEN_DRIFT: 2.5,
        WeatherType.GOLDEN_HOUR: 1.5, WeatherType.BALMY_EVENING: 1.5,
        WeatherType.FOGGY: 0.5, WeatherType.MISTY: 0.5,
    },
    "riverside": {
        WeatherType.MISTY: 2.0, WeatherType.FOGGY: 1.8, WeatherType.DEWY_MORNING: 2.0,
        WeatherType.DRIZZLE: 1.5, WeatherType.HUMID: 1.5,
    },
    "garden": {
        WeatherType.SUNNY: 1.3, WeatherType.WARM_BREEZE: 1.5, WeatherType.SPRING_SHOWERS: 1.5,
        WeatherType.BLIZZARD: 0.3, WeatherType.STORMY: 0.5, WeatherType.THUNDERSTORM: 0.5,
    },
    "mountains": {
        WeatherType.WINDY: 2.5, WeatherType.BITTER_COLD: 2.0, WeatherType.FROST: 2.0,
        WeatherType.CLEAR_COLD: 1.8, WeatherType.SNOW_FLURRIES: 2.0,
        WeatherType.LIGHT_SNOW: 1.8, WeatherType.BLIZZARD: 1.5, WeatherType.AURORA: 2.0,
        WeatherType.HUMID: 0.2, WeatherType.MUGGY: 0.1,
        WeatherType.SCORCHING: 0.2, WeatherType.HEAT_WAVE: 0.1,
    },
    "beach": {
        WeatherType.SUNNY: 1.8, WeatherType.WINDY: 1.8, WeatherType.BALMY_EVENING: 2.0,
        WeatherType.GOLDEN_HOUR: 2.0, WeatherType.SUMMER_STORM: 1.5,
        WeatherType.FOGGY: 0.5, WeatherType.SNOWY: 0.3,
        WeatherType.HEAVY_SNOW: 0.1, WeatherType.BLIZZARD: 0.1,
    },
    "swamp": {
        WeatherType.FOGGY: 3.0, WeatherType.MISTY: 2.5, WeatherType.HUMID: 2.5,
        WeatherType.MUGGY: 2.5, WeatherType.DRIZZLE: 2.0, WeatherType.RAINY: 1.5,
        WeatherType.OVERCAST: 1.5, WeatherType.SUNNY: 0.5, WeatherType.SCORCHING: 0.3,
    },
    "urban": {
        WeatherType.CLOUDY: 1.5, WeatherType.OVERCAST: 1.5, WeatherType.PARTLY_CLOUDY: 1.3,
        WeatherType.FOGGY: 1.3, WeatherType.BLIZZARD: 0.5, WeatherType.HEAVY_SNOW: 0.7,
    },
}


# Weather definitions with probabilities by season
# Each weather type has: name, message, mood_modifier, xp_multiplier, and season probabilities
# Probabilities for each season should sum to approximately 1.0

WEATHER_DATA = {
    # ==========================================================================
    # COMMON WEATHER (appears in multiple seasons)
    # ==========================================================================
    WeatherType.SUNNY: {
        "name": "Sunny",
        "message": "The sun is shining! Perfect day!",
        "mood_modifier": 5,
        "xp_multiplier": 1.1,
        "particle_type": None,  # No particles
        "env_effects": ["sun_sparkles"],
        "spring_prob": 0.15, "summer_prob": 0.20, "fall_prob": 0.12, "winter_prob": 0.08,
    },
    WeatherType.PARTLY_CLOUDY: {
        "name": "Partly Cloudy",
        "message": "Fluffy clouds drift across a blue sky.",
        "mood_modifier": 3,
        "xp_multiplier": 1.05,
        "particle_type": None,
        "env_effects": ["cloud_shadows"],
        "spring_prob": 0.12, "summer_prob": 0.15, "fall_prob": 0.10, "winter_prob": 0.08,
    },
    WeatherType.CLOUDY: {
        "name": "Cloudy",
        "message": "Grey clouds blanket the sky...",
        "mood_modifier": 0,
        "xp_multiplier": 1.0,
        "particle_type": None,
        "env_effects": [],
        "spring_prob": 0.10, "summer_prob": 0.08, "fall_prob": 0.12, "winter_prob": 0.12,
    },
    WeatherType.OVERCAST: {
        "name": "Overcast",
        "message": "A thick layer of clouds covers everything.",
        "mood_modifier": -1,
        "xp_multiplier": 1.0,
        "particle_type": None,
        "env_effects": ["dim_lighting"],
        "spring_prob": 0.06, "summer_prob": 0.04, "fall_prob": 0.08, "winter_prob": 0.10,
    },
    WeatherType.WINDY: {
        "name": "Windy",
        "message": "*feathers ruffled* Woooosh!",
        "mood_modifier": 2,
        "xp_multiplier": 1.0,
        "particle_type": "wind",
        "env_effects": ["swaying_reeds", "blowing_leaves"],
        "spring_prob": 0.06, "summer_prob": 0.04, "fall_prob": 0.06, "winter_prob": 0.05,
    },
    WeatherType.FOGGY: {
        "name": "Foggy",
        "message": "Mysterious fog rolls in... spooky!",
        "mood_modifier": 0,
        "xp_multiplier": 1.2,
        "particle_type": "fog",
        "env_effects": ["thick_fog", "hidden_shapes"],
        "rare_drops_bonus": 0.5,
        "spring_prob": 0.03, "summer_prob": 0.01, "fall_prob": 0.04, "winter_prob": 0.05,
    },
    WeatherType.MISTY: {
        "name": "Misty",
        "message": "A light mist hangs in the air...",
        "mood_modifier": 1,
        "xp_multiplier": 1.1,
        "particle_type": "mist",
        "env_effects": ["dew_drops", "soft_haze"],
        "spring_prob": 0.04, "summer_prob": 0.02, "fall_prob": 0.05, "winter_prob": 0.04,
    },
    
    # ==========================================================================
    # RAIN VARIATIONS
    # ==========================================================================
    WeatherType.DRIZZLE: {
        "name": "Drizzle",
        "message": "*light pitter-patter* A gentle drizzle falls.",
        "mood_modifier": 0,
        "xp_multiplier": 1.05,
        "particle_type": "drizzle",
        "env_effects": ["small_puddles", "damp_ground"],
        "spring_prob": 0.06, "summer_prob": 0.03, "fall_prob": 0.06, "winter_prob": 0.02,
    },
    WeatherType.RAINY: {
        "name": "Rainy",
        "message": "*pitter patter* Perfect puddle splashing weather!",
        "mood_modifier": -2,
        "xp_multiplier": 1.15,
        "particle_type": "rain",
        "env_effects": ["puddles", "rippling_water", "wet_vegetation"],
        "triggers_rainbow": True,
        "spring_prob": 0.08, "summer_prob": 0.05, "fall_prob": 0.08, "winter_prob": 0.03,
    },
    WeatherType.HEAVY_RAIN: {
        "name": "Heavy Rain",
        "message": "*SPLASH SPLASH* It's POURING! Quick, find shelter!",
        "mood_modifier": -4,
        "xp_multiplier": 1.2,
        "particle_type": "heavy_rain",
        "env_effects": ["large_puddles", "splashing", "overflowing_pond"],
        "triggers_rainbow": True,
        "spring_prob": 0.04, "summer_prob": 0.03, "fall_prob": 0.05, "winter_prob": 0.01,
    },
    WeatherType.STORMY: {
        "name": "Stormy",
        "message": "*rumble* Storm clouds gather ominously...",
        "mood_modifier": -5,
        "xp_multiplier": 1.25,
        "particle_type": "storm",
        "env_effects": ["large_puddles", "dark_sky", "bending_trees"],
        "spring_prob": 0.02, "summer_prob": 0.03, "fall_prob": 0.03, "winter_prob": 0.01,
    },
    WeatherType.THUNDERSTORM: {
        "name": "Thunderstorm",
        "message": "*CRACK-BOOM* Lightning flashes across the sky!",
        "mood_modifier": -8,
        "xp_multiplier": 1.35,
        "particle_type": "thunderstorm",
        "env_effects": ["lightning_flashes", "large_puddles", "dark_sky", "frightened_animals"],
        "spring_prob": 0.02, "summer_prob": 0.04, "fall_prob": 0.02, "winter_prob": 0.01,
    },
    
    # ==========================================================================
    # SNOW/ICE VARIATIONS
    # ==========================================================================
    WeatherType.FROST: {
        "name": "Frost",
        "message": "*shivers* Everything's covered in delicate frost crystals!",
        "mood_modifier": 1,
        "xp_multiplier": 1.1,
        "particle_type": None,
        "env_effects": ["frost_crystals", "frozen_edges", "icy_sparkles"],
        "spring_prob": 0.01, "summer_prob": 0.0, "fall_prob": 0.03, "winter_prob": 0.08,
    },
    WeatherType.LIGHT_SNOW: {
        "name": "Light Snow",
        "message": "*catches snowflake* How pretty!",
        "mood_modifier": 3,
        "xp_multiplier": 1.15,
        "particle_type": "light_snow",
        "env_effects": ["light_snow_cover", "snowflakes"],
        "spring_prob": 0.01, "summer_prob": 0.0, "fall_prob": 0.01, "winter_prob": 0.10,
    },
    WeatherType.SNOWY: {
        "name": "Snowy",
        "message": "*waddles through snow* So fluffy!",
        "mood_modifier": 4,
        "xp_multiplier": 1.2,
        "particle_type": "snow",
        "env_effects": ["snow_cover", "snow_piles", "icicles"],
        "spring_prob": 0.0, "summer_prob": 0.0, "fall_prob": 0.01, "winter_prob": 0.08,
    },
    WeatherType.HEAVY_SNOW: {
        "name": "Heavy Snow",
        "message": "*BRRR* It's a winter wonderland out here!",
        "mood_modifier": 2,
        "xp_multiplier": 1.25,
        "particle_type": "heavy_snow",
        "env_effects": ["deep_snow", "snow_drifts", "covered_vegetation"],
        "spring_prob": 0.0, "summer_prob": 0.0, "fall_prob": 0.0, "winter_prob": 0.05,
    },
    WeatherType.BLIZZARD: {
        "name": "Blizzard",
        "message": "*WHOOSH* Can barely see through the blowing snow!",
        "mood_modifier": -6,
        "xp_multiplier": 1.4,
        "particle_type": "blizzard",
        "env_effects": ["deep_snow", "blowing_snow", "zero_visibility", "snow_drifts"],
        "spring_prob": 0.0, "summer_prob": 0.0, "fall_prob": 0.0, "winter_prob": 0.02,
    },
    WeatherType.SLEET: {
        "name": "Sleet",
        "message": "*tap tap tap* Icy rain bounces off everything!",
        "mood_modifier": -4,
        "xp_multiplier": 1.15,
        "particle_type": "sleet",
        "env_effects": ["icy_puddles", "frozen_ground"],
        "spring_prob": 0.01, "summer_prob": 0.0, "fall_prob": 0.02, "winter_prob": 0.04,
    },
    WeatherType.HAIL: {
        "name": "Hail",
        "message": "*BONK* OW! Ice balls falling from the sky!",
        "mood_modifier": -7,
        "xp_multiplier": 1.3,
        "particle_type": "hail",
        "env_effects": ["hail_stones", "dented_ground"],
        "spring_prob": 0.01, "summer_prob": 0.02, "fall_prob": 0.01, "winter_prob": 0.02,
    },
    WeatherType.ICE_STORM: {
        "name": "Ice Storm",
        "message": "*crackle* Everything's coated in ice!",
        "mood_modifier": -8,
        "xp_multiplier": 1.35,
        "particle_type": "ice_storm",
        "env_effects": ["ice_coating", "frozen_everything", "icicles", "cracking_branches"],
        "spring_prob": 0.0, "summer_prob": 0.0, "fall_prob": 0.0, "winter_prob": 0.02,
    },
    
    # ==========================================================================
    # SPRING SPECIFIC
    # ==========================================================================
    WeatherType.SPRING_SHOWERS: {
        "name": "Spring Showers",
        "message": "April showers bring May flowers! 🌷",
        "mood_modifier": 2,
        "xp_multiplier": 1.15,
        "particle_type": "spring_rain",
        "env_effects": ["puddles", "blooming_flowers", "fresh_growth"],
        "triggers_rainbow": True,
        "spring_prob": 0.10, "summer_prob": 0.0, "fall_prob": 0.0, "winter_prob": 0.0,
    },
    WeatherType.RAINBOW: {
        "name": "Rainbow",
        "message": "A RAINBOW! Make a wish! ✨",
        "mood_modifier": 15,
        "xp_multiplier": 2.0,
        "particle_type": "rainbow",
        "env_effects": ["rainbow_arc", "sparkles", "puddles"],
        "special": True,
        "spring_prob": 0.0, "summer_prob": 0.0, "fall_prob": 0.0, "winter_prob": 0.0,
    },
    WeatherType.POLLEN_DRIFT: {
        "name": "Pollen Drift",
        "message": "*ACHOO* The air is full of golden pollen!",
        "mood_modifier": -1,
        "xp_multiplier": 1.05,
        "particle_type": "pollen",
        "env_effects": ["pollen_clouds", "blooming_trees", "yellow_dust"],
        "spring_prob": 0.06, "summer_prob": 0.0, "fall_prob": 0.0, "winter_prob": 0.0,
    },
    WeatherType.WARM_BREEZE: {
        "name": "Warm Breeze",
        "message": "*aaahh* A gentle warm breeze ruffles your feathers.",
        "mood_modifier": 6,
        "xp_multiplier": 1.15,
        "particle_type": "gentle_wind",
        "env_effects": ["swaying_flowers", "dancing_petals"],
        "spring_prob": 0.08, "summer_prob": 0.0, "fall_prob": 0.0, "winter_prob": 0.0,
    },
    WeatherType.DEWY_MORNING: {
        "name": "Dewy Morning",
        "message": "*sparkle sparkle* Morning dew glistens everywhere!",
        "mood_modifier": 4,
        "xp_multiplier": 1.1,
        "particle_type": None,
        "env_effects": ["dew_drops", "glistening_grass", "spider_webs"],
        "spring_prob": 0.05, "summer_prob": 0.0, "fall_prob": 0.0, "winter_prob": 0.0,
    },
    
    # ==========================================================================
    # SUMMER SPECIFIC
    # ==========================================================================
    WeatherType.SCORCHING: {
        "name": "Scorching",
        "message": "*pants* It's SO hot! Need water!",
        "mood_modifier": -3,
        "xp_multiplier": 1.1,
        "particle_type": "heat_shimmer",
        "env_effects": ["heat_waves", "wilting_plants", "cracked_ground"],
        "spring_prob": 0.0, "summer_prob": 0.08, "fall_prob": 0.0, "winter_prob": 0.0,
    },
    WeatherType.HUMID: {
        "name": "Humid",
        "message": "*sticky feathers* The air is thick and muggy.",
        "mood_modifier": -2,
        "xp_multiplier": 1.0,
        "particle_type": None,
        "env_effects": ["moist_air", "sweating_plants"],
        "spring_prob": 0.0, "summer_prob": 0.10, "fall_prob": 0.0, "winter_prob": 0.0,
    },
    WeatherType.HEAT_WAVE: {
        "name": "Heat Wave",
        "message": "*gasp* It's a HEAT WAVE! Find shade!",
        "mood_modifier": -6,
        "xp_multiplier": 1.2,
        "particle_type": "heat_shimmer",
        "env_effects": ["extreme_heat_waves", "wilting_plants", "dry_ground"],
        "spring_prob": 0.0, "summer_prob": 0.05, "fall_prob": 0.0, "winter_prob": 0.0,
    },
    WeatherType.SUMMER_STORM: {
        "name": "Summer Storm",
        "message": "*CRACK-BOOM* A dramatic summer storm!",
        "mood_modifier": -4,
        "xp_multiplier": 1.3,
        "particle_type": "summer_storm",
        "env_effects": ["lightning_flashes", "large_puddles", "dramatic_sky"],
        "triggers_rainbow": True,
        "spring_prob": 0.0, "summer_prob": 0.06, "fall_prob": 0.0, "winter_prob": 0.0,
    },
    WeatherType.BALMY_EVENING: {
        "name": "Balmy Evening",
        "message": "*content sigh* What a perfect warm evening.",
        "mood_modifier": 7,
        "xp_multiplier": 1.2,
        "particle_type": None,
        "env_effects": ["fireflies", "warm_glow", "gentle_breeze"],
        "spring_prob": 0.0, "summer_prob": 0.06, "fall_prob": 0.0, "winter_prob": 0.0,
    },
    WeatherType.GOLDEN_HOUR: {
        "name": "Golden Hour",
        "message": "*basks* Everything is bathed in golden light!",
        "mood_modifier": 10,
        "xp_multiplier": 1.5,
        "particle_type": "golden_sparkles",
        "env_effects": ["golden_light", "long_shadows", "warm_glow"],
        "spring_prob": 0.0, "summer_prob": 0.04, "fall_prob": 0.0, "winter_prob": 0.0,
    },
    WeatherType.MUGGY: {
        "name": "Muggy",
        "message": "*fans self with wing* So hot and sticky!",
        "mood_modifier": -3,
        "xp_multiplier": 1.05,
        "particle_type": None,
        "env_effects": ["humid_haze", "drooping_plants"],
        "spring_prob": 0.0, "summer_prob": 0.08, "fall_prob": 0.0, "winter_prob": 0.0,
    },
    
    # ==========================================================================
    # FALL SPECIFIC
    # ==========================================================================
    WeatherType.CRISP: {
        "name": "Crisp",
        "message": "*deep breath* The air is cool and refreshing!",
        "mood_modifier": 5,
        "xp_multiplier": 1.15,
        "particle_type": None,
        "env_effects": ["colorful_leaves", "clear_air"],
        "spring_prob": 0.0, "summer_prob": 0.0, "fall_prob": 0.12, "winter_prob": 0.0,
    },
    WeatherType.BREEZY: {
        "name": "Breezy",
        "message": "*feathers flutter* A playful autumn breeze!",
        "mood_modifier": 4,
        "xp_multiplier": 1.1,
        "particle_type": "autumn_wind",
        "env_effects": ["falling_leaves", "swaying_trees"],
        "spring_prob": 0.0, "summer_prob": 0.0, "fall_prob": 0.10, "winter_prob": 0.0,
    },
    WeatherType.LEAF_STORM: {
        "name": "Leaf Storm",
        "message": "*wheee* Leaves swirling EVERYWHERE!",
        "mood_modifier": 6,
        "xp_multiplier": 1.2,
        "particle_type": "leaf_storm",
        "env_effects": ["leaf_piles", "swirling_leaves", "bare_trees"],
        "spring_prob": 0.0, "summer_prob": 0.0, "fall_prob": 0.08, "winter_prob": 0.0,
    },
    WeatherType.HARVEST_MOON: {
        "name": "Harvest Moon",
        "message": "*gazes up* The huge orange moon is beautiful!",
        "mood_modifier": 8,
        "xp_multiplier": 1.25,
        "particle_type": "moonlight",
        "env_effects": ["orange_moon", "long_shadows", "mystical_glow"],
        "spring_prob": 0.0, "summer_prob": 0.0, "fall_prob": 0.04, "winter_prob": 0.0,
    },
    WeatherType.FIRST_FROST: {
        "name": "First Frost",
        "message": "*shivers* Winter is coming... first frost!",
        "mood_modifier": 2,
        "xp_multiplier": 1.15,
        "particle_type": None,
        "env_effects": ["frost_crystals", "frozen_puddles", "cold_breath"],
        "spring_prob": 0.0, "summer_prob": 0.0, "fall_prob": 0.05, "winter_prob": 0.0,
    },
    WeatherType.AUTUMNAL: {
        "name": "Autumnal",
        "message": "A perfect autumn day with colorful leaves!",
        "mood_modifier": 6,
        "xp_multiplier": 1.2,
        "particle_type": "falling_leaves",
        "env_effects": ["colorful_leaves", "leaf_piles", "warm_colors"],
        "spring_prob": 0.0, "summer_prob": 0.0, "fall_prob": 0.10, "winter_prob": 0.0,
    },
    
    # ==========================================================================
    # WINTER SPECIFIC
    # ==========================================================================
    WeatherType.BITTER_COLD: {
        "name": "Bitter Cold",
        "message": "*BRRRRR* It's FREEZING out here!",
        "mood_modifier": -5,
        "xp_multiplier": 1.2,
        "particle_type": None,
        "env_effects": ["frost_everywhere", "frozen_pond", "cold_breath"],
        "spring_prob": 0.0, "summer_prob": 0.0, "fall_prob": 0.0, "winter_prob": 0.06,
    },
    WeatherType.FREEZING: {
        "name": "Freezing",
        "message": "*teeth chattering* Everything's frozen solid!",
        "mood_modifier": -4,
        "xp_multiplier": 1.15,
        "particle_type": None,
        "env_effects": ["ice_coating", "frozen_water", "frost_crystals"],
        "spring_prob": 0.0, "summer_prob": 0.0, "fall_prob": 0.0, "winter_prob": 0.08,
    },
    WeatherType.CLEAR_COLD: {
        "name": "Clear Cold",
        "message": "*crisp!* Cold but sunny - beautiful winter day!",
        "mood_modifier": 4,
        "xp_multiplier": 1.15,
        "particle_type": None,
        "env_effects": ["frost_sparkles", "blue_sky", "sharp_shadows"],
        "spring_prob": 0.0, "summer_prob": 0.0, "fall_prob": 0.0, "winter_prob": 0.10,
    },
    WeatherType.SNOW_FLURRIES: {
        "name": "Snow Flurries",
        "message": "*catches flakes* Little snowflakes dancing in the air!",
        "mood_modifier": 5,
        "xp_multiplier": 1.15,
        "particle_type": "flurries",
        "env_effects": ["light_snow_cover", "dancing_flakes"],
        "spring_prob": 0.0, "summer_prob": 0.0, "fall_prob": 0.0, "winter_prob": 0.08,
    },
    WeatherType.WINTER_SUN: {
        "name": "Winter Sun",
        "message": "*soaks up rays* Bright winter sunshine!",
        "mood_modifier": 6,
        "xp_multiplier": 1.2,
        "particle_type": None,
        "env_effects": ["bright_glare", "snow_sparkles", "warm_patches"],
        "spring_prob": 0.0, "summer_prob": 0.0, "fall_prob": 0.0, "winter_prob": 0.06,
    },
    
    # ==========================================================================
    # RARE/SPECIAL WEATHER
    # ==========================================================================
    WeatherType.AURORA: {
        "name": "Aurora Borealis",
        "message": "*mesmerized* The northern lights dance across the sky!",
        "mood_modifier": 20,
        "xp_multiplier": 2.5,
        "particle_type": "aurora",
        "env_effects": ["aurora_glow", "mystical_light", "color_waves"],
        "special": True,
        "spring_prob": 0.0, "summer_prob": 0.0, "fall_prob": 0.005, "winter_prob": 0.01,
    },
    WeatherType.METEOR_SHOWER: {
        "name": "Meteor Shower",
        "message": "*gasp* Shooting stars! Make a wish!",
        "mood_modifier": 18,
        "xp_multiplier": 2.0,
        "particle_type": "meteors",
        "env_effects": ["streaking_lights", "night_magic"],
        "special": True,
        "spring_prob": 0.005, "summer_prob": 0.01, "fall_prob": 0.005, "winter_prob": 0.005,
    },
    WeatherType.DOUBLE_RAINBOW: {
        "name": "Double Rainbow",
        "message": "*GASP* DOUBLE RAINBOW! What does it MEAN?!",
        "mood_modifier": 25,
        "xp_multiplier": 3.0,
        "particle_type": "rainbow",
        "env_effects": ["double_rainbow_arc", "sparkles", "magical_glow"],
        "special": True,
        "spring_prob": 0.0, "summer_prob": 0.0, "fall_prob": 0.0, "winter_prob": 0.0,
    },
    WeatherType.PERFECT_DAY: {
        "name": "Perfect Day",
        "message": "Everything is PERFECT. Temperature, sky, breeze... magical!",
        "mood_modifier": 15,
        "xp_multiplier": 2.0,
        "particle_type": "sparkles",
        "env_effects": ["perfect_lighting", "happy_animals", "blooming_nature"],
        "special": True,
        "spring_prob": 0.01, "summer_prob": 0.01, "fall_prob": 0.01, "winter_prob": 0.005,
    },
}


# =============================================================================
# SEASONS
# =============================================================================

class Season(Enum):
    """Seasons that affect gameplay."""
    SPRING = "spring"
    SUMMER = "summer"
    FALL = "fall"
    WINTER = "winter"


@dataclass
class SeasonalContent:
    """Content specific to a season."""
    items_available: List[str]  # Special items only available this season
    events: List[str]  # Special events
    decorations: List[str]  # Seasonal decorations
    mood_theme: str  # General mood of the season
    xp_bonus: float  # Season-wide XP modifier
    color_palette: List[str] = field(default_factory=list)  # Colors for the season
    special_activities: List[str] = field(default_factory=list)  # Seasonal activities
    ambient_effects: List[str] = field(default_factory=list)  # Visual effects
    greeting_messages: List[str] = field(default_factory=list)  # Seasonal greetings


@dataclass
class SeasonalEvent:
    """A special seasonal event."""
    id: str
    name: str
    description: str
    season: Season
    start_day: int  # Day of month to start (0 = season start)
    duration_days: int
    xp_bonus: float
    special_drops: List[str]
    activities: List[str]
    messages: List[str]


SEASONAL_EVENTS = {
    # Spring Events
    "cherry_blossom_festival": SeasonalEvent(
        id="cherry_blossom_festival",
        name="Cherry Blossom Festival",
        description="Pink petals drift through the air!",
        season=Season.SPRING,
        start_day=1,
        duration_days=14,
        xp_bonus=1.3,
        special_drops=["cherry_blossom", "pink_petal", "blossom_crown"],
        activities=["petal_catching", "blossom_viewing", "picnic"],
        messages=[
            "The cherry blossoms are in full bloom!",
            "*catches a falling petal* So pretty!",
            "Spring renewal fills the air with magic!",
        ],
    ),
    "egg_hunt": SeasonalEvent(
        id="egg_hunt",
        name="Egg Hunt Festival",
        description="Colorful eggs are hidden everywhere!",
        season=Season.SPRING,
        start_day=15,
        duration_days=7,
        xp_bonus=1.5,
        special_drops=["golden_egg", "rainbow_egg", "lucky_egg"],
        activities=["egg_hunting", "egg_decorating", "egg_rolling"],
        messages=[
            "Eggs are hidden everywhere! Time to hunt!",
            "*finds an egg* Ooh, this one sparkles!",
            "The Egg Hunt is on! Happy searching!",
        ],
    ),
    # Summer Events
    "beach_day": SeasonalEvent(
        id="beach_day",
        name="Beach Day Celebration",
        description="Sun, sand, and splashing fun!",
        season=Season.SUMMER,
        start_day=1,
        duration_days=21,
        xp_bonus=1.2,
        special_drops=["seashell", "sand_dollar", "starfish"],
        activities=["swimming", "sandcastle_building", "shell_collecting"],
        messages=[
            "Beach Day! Time for sun and splashing!",
            "*splashes in the waves* Summer fun!",
            "The water is perfect today!",
        ],
    ),
    "fireworks_show": SeasonalEvent(
        id="fireworks_show",
        name="Fireworks Festival",
        description="The night sky lights up with colors!",
        season=Season.SUMMER,
        start_day=20,
        duration_days=3,
        xp_bonus=2.0,
        special_drops=["sparkler", "firework_fragment", "star_piece"],
        activities=["firework_watching", "sparkler_waving", "night_picnic"],
        messages=[
            "*BOOM* The fireworks are starting!",
            "Ooooh! Aaaaah! *watches in awe*",
            "The night sky is so colorful!",
        ],
    ),
    # Fall Events
    "harvest_festival": SeasonalEvent(
        id="harvest_festival",
        name="Harvest Festival",
        description="Celebrate the autumn bounty!",
        season=Season.FALL,
        start_day=1,
        duration_days=14,
        xp_bonus=1.3,
        special_drops=["golden_wheat", "harvest_corn", "autumn_apple"],
        activities=["apple_picking", "pie_baking", "hayride"],
        messages=[
            "The Harvest Festival begins! So much good food!",
            "*munches on apple* Autumn treats are the best!",
            "Time to gather the harvest!",
        ],
    ),
    "spooky_night": SeasonalEvent(
        id="spooky_night",
        name="Spooky Night",
        description="Things go bump in the night!",
        season=Season.FALL,
        start_day=24,
        duration_days=7,
        xp_bonus=1.5,
        special_drops=["candy_corn", "ghost_feather", "pumpkin_piece"],
        activities=["trick_or_treating", "costume_wearing", "spooky_stories"],
        messages=[
            "*spooky quack* BOO! Happy Spooky Night!",
            "Is that a ghost?! Oh wait, it's just fog...",
            "Time for tricks and treats!",
        ],
    ),
    # Winter Events
    "first_snow": SeasonalEvent(
        id="first_snow",
        name="First Snow Day",
        description="The first magical snowfall of winter!",
        season=Season.WINTER,
        start_day=1,
        duration_days=7,
        xp_bonus=1.4,
        special_drops=["snowflake", "icicle", "snow_globe_shard"],
        activities=["snowball_making", "snow_angel", "sledding"],
        messages=[
            "It's snowing! The first snow of winter!",
            "*catches snowflake on tongue* Magical!",
            "Everything is covered in white!",
        ],
    ),
    "winter_festival": SeasonalEvent(
        id="winter_festival",
        name="Winter Festival",
        description="A celebration of warmth and giving!",
        season=Season.WINTER,
        start_day=20,
        duration_days=5,
        xp_bonus=2.0,
        special_drops=["wrapped_gift", "candy_cane", "holiday_cookie"],
        activities=["gift_giving", "carol_singing", "cocoa_drinking"],
        messages=[
            "Happy Winter Festival! Time for warmth and joy!",
            "*sips hot cocoa* So cozy!",
            "The spirit of giving fills the air!",
        ],
    ),
    "new_year_countdown": SeasonalEvent(
        id="new_year_countdown",
        name="New Year Countdown",
        description="Ring in the new year!",
        season=Season.WINTER,
        start_day=28,
        duration_days=4,
        xp_bonus=1.5,
        special_drops=["confetti", "party_hat", "lucky_charm"],
        activities=["countdown", "resolution_making", "celebration"],
        messages=[
            "The new year approaches! Time to celebrate!",
            "3... 2... 1... HAPPY NEW YEAR!",
            "New year, new adventures!",
        ],
    ),
}


SEASONAL_CONTENT = {
    Season.SPRING: SeasonalContent(
        items_available=["spring_flower", "easter_egg", "cherry_blossom", "butterfly_net", "flower_seeds"],
        events=["cherry_blossom_festival", "egg_hunt"],
        decorations=["flower_wreath", "pastel_banner", "bunny_statue", "blossom_tree", "butterfly_garden"],
        mood_theme="renewal",
        xp_bonus=1.1,
        color_palette=["pink", "light_green", "yellow", "lavender"],
        special_activities=["flower_picking", "butterfly_watching", "spring_cleaning"],
        ambient_effects=["petals_falling", "birds_singing", "gentle_breeze"],
        greeting_messages=[
            "Spring has sprung! New beginnings await!",
            "The flowers are blooming just for you!",
            "Spring energy fills the air!",
        ],
    ),
    Season.SUMMER: SeasonalContent(
        items_available=["watermelon", "sunscreen", "beach_ball", "ice_cream", "sunglasses", "seashell"],
        events=["beach_day", "fireworks_show"],
        decorations=["beach_umbrella", "sandcastle", "tiki_torch", "palm_tree", "hammock"],
        mood_theme="adventure",
        xp_bonus=1.0,
        color_palette=["bright_blue", "yellow", "orange", "coral"],
        special_activities=["swimming", "sunbathing", "beach_exploring"],
        ambient_effects=["sun_rays", "heat_shimmer", "waves"],
        greeting_messages=[
            "Summer vibes! Time for adventure!",
            "The sun is shining just for you!",
            "Hot summer days call for cool fun!",
        ],
    ),
    Season.FALL: SeasonalContent(
        items_available=["pumpkin", "autumn_leaf", "candy_corn", "apple_cider", "acorn", "warm_scarf"],
        events=["harvest_festival", "spooky_night"],
        decorations=["scarecrow", "hay_bale", "pumpkin_lantern", "leaf_pile", "harvest_basket"],
        mood_theme="cozy",
        xp_bonus=1.15,
        color_palette=["orange", "red", "brown", "gold"],
        special_activities=["leaf_jumping", "apple_picking", "cozy_napping"],
        ambient_effects=["leaves_falling", "crisp_air", "warm_glow"],
        greeting_messages=[
            "Cozy autumn days are here!",
            "The leaves are changing colors!",
            "Fall brings warmth to the heart!",
        ],
    ),
    Season.WINTER: SeasonalContent(
        items_available=["hot_cocoa", "snowball", "candy_cane", "wrapped_gift", "mittens", "warm_blanket"],
        events=["first_snow", "winter_festival", "new_year_countdown"],
        decorations=["snow_duck", "string_lights", "wreath", "snowman", "ice_sculpture"],
        mood_theme="warmth",
        xp_bonus=1.2,
        color_palette=["white", "blue", "silver", "red", "green"],
        special_activities=["snowball_fights", "ice_skating", "cozy_cuddling"],
        ambient_effects=["snowfall", "frost", "twinkling_lights"],
        greeting_messages=[
            "Winter wonderland! Stay warm and cozy!",
            "The snow makes everything magical!",
            "Warm hearts in cold weather!",
        ],
    ),
}


# =============================================================================
# LUCKY / UNLUCKY DAYS
# =============================================================================

@dataclass
class DayFortune:
    """Fortune for a specific day (lucky/unlucky)."""
    fortune_type: str  # "lucky", "normal", "unlucky", "super_lucky"
    xp_multiplier: float
    drop_rate_modifier: float  # Multiplier for rare drops
    special_message: str
    horoscope: str  # Fun daily fortune message


FORTUNE_TYPES = {
    "super_lucky": {
        "probability": 0.02,  # 2% chance
        "xp_multiplier": 2.0,
        "drop_rate_modifier": 3.0,
        "messages": [
            "The stars align! SUPER LUCKY DAY! Everything sparkles!",
            "Cheese found a four-leaf clover! MAXIMUM LUCK activated!",
            "The universe smiles upon you today! Triple rare drops!",
        ],
        "horoscopes": [
            "Today, even the bread crumbs lead to treasure!",
            "Lucky streams flow through your feathers today!",
            "The duck spirits have blessed this day abundantly!",
        ],
    },
    "lucky": {
        "probability": 0.15,  # 15% chance
        "xp_multiplier": 1.3,
        "drop_rate_modifier": 1.5,
        "messages": [
            "Feeling lucky today! Good things are coming!",
            "Cheese's lucky feather is tingling!",
            "The vibes are immaculate today!",
        ],
        "horoscopes": [
            "Fortune favors the bold duck today!",
            "Small surprises await around every corner!",
            "Your quacks carry extra weight today!",
        ],
    },
    "normal": {
        "probability": 0.70,  # 70% chance
        "xp_multiplier": 1.0,
        "drop_rate_modifier": 1.0,
        "messages": [
            "A pleasant, ordinary day!",
            "Just right for duck activities!",
        ],
        "horoscopes": [
            "Balance in all things today!",
            "A day like any other, yet full of potential!",
        ],
    },
    "unlucky": {
        "probability": 0.13,  # 13% chance (but we make it feel ok)
        "xp_multiplier": 0.9,
        "drop_rate_modifier": 0.7,
        "messages": [
            "Feeling a bit off today... but Cheese is still here for you!",
            "Not the luckiest day, but that makes the good days better!",
            "Mercury might be in retrograde, but ducks don't care!",
        ],
        "horoscopes": [
            "Even unlucky days teach valuable lessons!",
            "Tomorrow will be better! Today, just cozy up!",
            "Bad luck? Psh. Cheese makes their own luck!",
        ],
        # Compensations for unlucky days (so it doesn't feel bad)
        "compensations": [
            "Extra cuddles from Cheese today! +social bonus",
            "Cheese found a comfort snack for you!",
            "At least the company is good!",
        ],
    },
}


# =============================================================================
# RARE VISITORS & RECURRING FRIENDS
# =============================================================================

class FriendshipLevel(Enum):
    """Friendship levels with recurring visitors."""
    STRANGER = "stranger"
    ACQUAINTANCE = "acquaintance"
    FRIEND = "friend"
    GOOD_FRIEND = "good_friend"
    BEST_FRIEND = "best_friend"


FRIENDSHIP_THRESHOLDS = {
    FriendshipLevel.STRANGER: 0,
    FriendshipLevel.ACQUAINTANCE: 3,
    FriendshipLevel.FRIEND: 8,
    FriendshipLevel.GOOD_FRIEND: 15,
    FriendshipLevel.BEST_FRIEND: 25,
}


@dataclass
class VisitorFriendship:
    """Tracks friendship with a recurring visitor."""
    visitor_id: str
    visit_count: int = 0
    friendship_points: int = 0
    last_visit: Optional[str] = None
    gifts_received: List[str] = field(default_factory=list)
    special_moments: List[str] = field(default_factory=list)

    @property
    def level(self) -> FriendshipLevel:
        """Get current friendship level."""
        for level in reversed(list(FriendshipLevel)):
            if self.friendship_points >= FRIENDSHIP_THRESHOLDS[level]:
                return level
        return FriendshipLevel.STRANGER

    def add_visit(self):
        """Record a visit."""
        self.visit_count += 1
        self.friendship_points += 2
        self.last_visit = datetime.now().isoformat()

    def add_interaction(self, points: int = 1):
        """Add points from interaction."""
        self.friendship_points += points


@dataclass
class Visitor:
    """A rare visitor that can appear."""
    id: str
    name: str
    description: str
    ascii_art: List[str]
    greeting: str
    farewell: str
    gift_chance: float  # Chance to leave a gift
    possible_gifts: List[str]
    appearance_chance: float
    stay_duration_hours: float
    special_interaction: str  # What you can do with them
    mood_boost: int
    # New fields for recurring visitors
    is_recurring: bool = True
    personality: str = "friendly"
    favorite_weather: Optional[str] = None
    favorite_season: Optional[str] = None
    return_greetings: List[str] = field(default_factory=list)
    friend_greetings: List[str] = field(default_factory=list)
    best_friend_greetings: List[str] = field(default_factory=list)
    special_gifts: List[str] = field(default_factory=list)  # Rare gifts at higher friendship
    conversations: List[str] = field(default_factory=list)
    secrets: List[str] = field(default_factory=list)  # Unlocked at best friend level


VISITORS = {
    "friendly_goose": Visitor(
        id="friendly_goose",
        name="Gerald the Goose",
        description="A surprisingly friendly goose waddles by!",
        ascii_art=[
            "   __",
            " >(o )___",
            "  ( ._> /",
            "   `---'",
        ],
        greeting="*HONK* Oh, a fellow waterfowl! Gerald has arrived!",
        farewell="*HONK* Gerald must go. Keep being awesome, friend!",
        gift_chance=0.7,
        possible_gifts=["bread", "shiny_pebble", "feather"],
        appearance_chance=0.25,
        stay_duration_hours=0.05,  # 3 minutes
        special_interaction="chat",
        mood_boost=15,
        personality="boisterous",
        favorite_weather="sunny",
        favorite_season="summer",
        return_greetings=[
            "*HONK* Gerald is back! Did you miss the honks?",
            "*happy honk* Cheese! My favorite duck!",
            "*HONK HONK* The pond wasn't the same without you!",
        ],
        friend_greetings=[
            "*affectionate honk* Cheese, my dear friend!",
            "*HONK* Gerald brought you something special today!",
        ],
        best_friend_greetings=[
            "*gentle honk* Best friend Cheese! Gerald missed you so much!",
            "*HONK* Gerald considers you family now!",
        ],
        special_gifts=["golden_feather", "goose_down_pillow", "honorary_goose_badge"],
        conversations=[
            "Gerald once flew across three lakes in one day! *proud honk*",
            "Did you know geese can remember faces? Gerald remembers yours!",
            "The secret to a good honk is confidence! HONK!",
            "Gerald's grandmother was a legendary honker. True story!",
        ],
        secrets=["Gerald is actually afraid of butterflies... don't tell anyone!"],
    ),
    "wise_owl": Visitor(
        id="wise_owl",
        name="Professor Hoot",
        description="A wise owl visits under moonlight!",
        ascii_art=[
            "  ,___,",
            "  (O,O)",
            "  /)_)",
            "   \" \"",
        ],
        greeting="*hoo hoo* Greetings, young duck. I bring wisdom!",
        farewell="*hoo* Remember: knowledge is the greatest treasure. Farewell!",
        gift_chance=0.9,
        possible_gifts=["mysterious_crumb", "old_key", "crystal_shard"],
        appearance_chance=0.20,
        stay_duration_hours=0.035,  # ~2 minutes
        special_interaction="learn",
        mood_boost=20,
        personality="scholarly",
        favorite_weather="foggy",
        favorite_season="fall",
        return_greetings=[
            "*hoo* We meet again, studious one!",
            "*wise nod* The Professor has returned with more knowledge!",
            "*hoo hoo* Your quest for wisdom brings me back!",
        ],
        friend_greetings=[
            "*hoo* My friend! I've discovered fascinating new facts!",
            "*warm hoo* It gladdens me to see you again, fellow seeker!",
        ],
        best_friend_greetings=[
            "*affectionate hoo* My dearest pupil! I have much to share!",
            "*hoo* You've grown so wise! I'm proud of you!",
        ],
        special_gifts=["ancient_tome", "wisdom_crystal", "star_chart"],
        conversations=[
            "Did you know owls can rotate their heads 270 degrees?",
            "The stars tell stories if you know how to read them...",
            "In my 200 years, I've learned that kindness is true wisdom.",
            "The oldest tree in this forest holds many secrets...",
        ],
        secrets=["I once failed a flying test. Even professors make mistakes!"],
    ),
    "lost_duckling": Visitor(
        id="lost_duckling",
        name="Pip the Duckling",
        description="A tiny lost duckling needs help!",
        ascii_art=[
            " __",
            "(o>",
            " V",
        ],
        greeting="*peep peep* I'm lost! Can I stay here for a bit?",
        farewell="*happy peep* Thank you for helping me! You're the best!",
        gift_chance=1.0,
        possible_gifts=["fluffy_down", "lucky_clover"],
        appearance_chance=0.15,
        stay_duration_hours=0.08,  # ~5 minutes
        special_interaction="comfort",
        mood_boost=25,
        personality="shy",
        favorite_weather="sunny",
        favorite_season="spring",
        return_greetings=[
            "*excited peep* It's me, Pip! I came back to visit!",
            "*peep peep* I found my way here on purpose this time!",
            "*happy peep* I missed you, big duck friend!",
        ],
        friend_greetings=[
            "*confident peep* Cheese! My best big friend!",
            "*peep* I practiced flying just to see you!",
        ],
        best_friend_greetings=[
            "*peep* You're like a sibling to me, Cheese!",
            "*loving peep* I tell all my friends about you!",
        ],
        special_gifts=["friendship_bracelet", "tiny_flower_crown", "drawn_picture"],
        conversations=[
            "I'm getting better at swimming! Watch! *splash*",
            "My mom says I'll be big like you someday!",
            "Do you think I'll learn to fly soon?",
            "I made you a drawing! It's... um... abstract!",
        ],
        secrets=["I'm not really lost anymore. I just like visiting you!"],
    ),
    "traveling_merchant": Visitor(
        id="traveling_merchant",
        name="Marco the Merchant",
        description="A traveling merchant duck appears with wares!",
        ascii_art=[
            "   ,__,",
            "  (o.o)",
            " /|##|\\",
            "  d  b",
        ],
        greeting="*quack* Greetings! Marco has exotic items from far lands!",
        farewell="*quack* Marco must continue the journey. Until next time!",
        gift_chance=0.5,
        possible_gifts=["fancy_bread", "glass_marble", "rainbow_crumb"],
        appearance_chance=0.12,
        stay_duration_hours=0.05,  # 3 minutes
        special_interaction="trade",
        mood_boost=10,
        personality="entrepreneurial",
        favorite_weather="windy",
        favorite_season="fall",
        return_greetings=[
            "*quack* Marco returns with new treasures!",
            "*merchant quack* The trading routes led me back!",
            "*happy quack* My favorite customer! More exotic goods!",
        ],
        friend_greetings=[
            "*friendly quack* For you, friend, the best prices!",
            "*quack* Marco saved something special just for you!",
        ],
        best_friend_greetings=[
            "*warm quack* My dearest business partner and friend!",
            "*quack* For you, priceless friendship! (Also good deals)",
        ],
        special_gifts=["exotic_spices", "treasure_map", "enchanted_compass"],
        conversations=[
            "I once traded a single crumb for a whole loaf in the south!",
            "The markets in the Eastern Ponds are incredible!",
            "Marco's secret: always smile while negotiating!",
            "I've traveled to 47 different ponds! This is number 48!",
        ],
        secrets=["I keep the best items for my friends. Don't tell!"],
    ),
    "celebrity_duck": Visitor(
        id="celebrity_duck",
        name="Sir Quackington III",
        description="A famous noble duck graces you with their presence!",
        ascii_art=[
            "  /\\  ",
            " (@@)",
            " /||\\",
            "  ''",
        ],
        greeting="*regal quack* One has heard of your establishment. Impressive!",
        farewell="*noble nod* One shall speak well of this place. Farewell!",
        gift_chance=0.8,
        possible_gifts=["golden_crumb", "crown", "ancient_artifact"],
        appearance_chance=0.08,
        stay_duration_hours=0.035,  # ~2 minutes
        special_interaction="impress",
        mood_boost=30,
        personality="regal",
        favorite_weather="sunny",
        favorite_season="spring",
        return_greetings=[
            "*pleased quack* One simply had to return!",
            "*regal nod* The Queen's Court pales in comparison!",
            "*dignified quack* One has spoken highly of you at court!",
        ],
        friend_greetings=[
            "*warm royal quack* Ah, my dear friend! How delightful!",
            "*drops formality* It's good to see you again, truly!",
        ],
        best_friend_greetings=[
            "*genuine smile* You know, you can call me just Quacks!",
            "*royal embrace* The crown means nothing next to true friendship!",
        ],
        special_gifts=["royal_decree", "diamond_crumb", "noble_title"],
        conversations=[
            "Being royalty is lonely. One appreciates genuine company.",
            "The crown is surprisingly heavy! Both literally and figuratively.",
            "Between us, the royal bread is actually quite stale.",
            "My great-great-grandfather invented the formal waddle!",
        ],
        secrets=["I actually prefer common bread over fancy crumpets!"],
    ),
    "mysterious_crow": Visitor(
        id="mysterious_crow",
        name="Corvus the Crow",
        description="A cryptic crow appears with secrets...",
        ascii_art=[
            "   ___",
            " /'o o'\\",
            " \\ V  /",
            "  ^^^",
        ],
        greeting="*caw* I know things... secret things...",
        farewell="*caw* We will meet again when the stars align...",
        gift_chance=0.6,
        possible_gifts=["old_key", "crystal_shard", "ancient_artifact"],
        appearance_chance=0.10,
        stay_duration_hours=0.035,  # ~2 minutes
        special_interaction="mystery",
        mood_boost=5,
        personality="mysterious",
        favorite_weather="foggy",
        favorite_season="winter",
        return_greetings=[
            "*knowing caw* The shadows whispered of our reunion...",
            "*cryptic caw* I foresaw this meeting in the darkness...",
            "*mysterious caw* The threads of fate intertwine again...",
        ],
        friend_greetings=[
            "*warmer caw* You... are different. I trust you.",
            "*caw* The secrets I share with you... are real.",
        ],
        best_friend_greetings=[
            "*genuine caw* You see past the mystery. I appreciate that.",
            "*soft caw* Few earn Corvus's true friendship. You have.",
        ],
        special_gifts=["shadow_feather", "prophecy_scroll", "void_crystal"],
        conversations=[
            "The old oak tree... it remembers everything...",
            "I collect shiny things. Not because I must... because I can.",
            "There are 7 secret passages in this area. I've found 6.",
            "The moon tells me stories. They're usually sad.",
        ],
        secrets=["I'm not actually mysterious. I just have social anxiety."],
    ),
    "butterfly_fairy": Visitor(
        id="butterfly_fairy",
        name="Flutter",
        description="A magical butterfly with gossamer wings appears!",
        ascii_art=[
            "  \\  /",
            "  (oo)",
            "  /  \\",
            "  ~~~~",
        ],
        greeting="*sparkle* Hello little duck! I'm Flutter! *twirl*",
        farewell="*shimmer* May flowers bloom wherever you waddle!",
        gift_chance=0.9,
        possible_gifts=["flower_petal", "fairy_dust", "rainbow_scale"],
        appearance_chance=0.12,
        stay_duration_hours=0.05,  # 3 minutes
        special_interaction="wish",
        mood_boost=20,
        personality="whimsical",
        favorite_weather="sunny",
        favorite_season="spring",
        return_greetings=[
            "*happy flutter* I followed the flowers back to you!",
            "*twirl* The spring breeze carried me here!",
            "*sparkle* You're like a flower I keep coming back to!",
        ],
        friend_greetings=[
            "*affectionate flutter* My flower friend!",
            "*sparkle* I dreamed of visiting you!",
        ],
        best_friend_greetings=[
            "*gentle landing* You're my favorite duck in all the meadows!",
            "*shimmer* Our friendship is like the prettiest flower!",
        ],
        special_gifts=["enchanted_pollen", "rainbow_wing_scale", "eternal_bloom"],
        conversations=[
            "I've visited 10,000 flowers! You're the only duck!",
            "The roses told me you're very kind!",
            "I can taste colors! Purple is the yummiest!",
            "My wings have stories written in them!",
        ],
        secrets=["I'm 300 years old! Butterflies live long in the magic meadows!"],
    ),
    "grumpy_toad": Visitor(
        id="grumpy_toad",
        name="Grumble the Toad",
        description="A grumpy toad hops by, looking annoyed!",
        ascii_art=[
            "  @..@",
            " (---)",
            " (---)",
            "  \\_/",
        ],
        greeting="*ribbit* What? I'm just passing through. Don't get excited.",
        farewell="*grumble* Fine, this was... acceptable. Don't expect me back.",
        gift_chance=0.4,
        possible_gifts=["pond_lily", "lucky_stone", "mud_cake"],
        appearance_chance=0.15,
        stay_duration_hours=0.035,  # ~2 minutes
        special_interaction="listen",
        mood_boost=5,
        personality="grumpy",
        favorite_weather="rainy",
        favorite_season="fall",
        return_greetings=[
            "*annoyed ribbit* Ugh, I'm here again. Don't read into it.",
            "*grumble* My other ponds were worse. That's the only reason.",
            "*ribbit* Stop smiling. This isn't a friendship thing.",
        ],
        friend_greetings=[
            "*embarrassed ribbit* I... might have missed you. A little.",
            "*softer grumble* You're tolerable, I suppose.",
        ],
        best_friend_greetings=[
            "*quiet ribbit* You're the only one who gets me, duck.",
            "*almost smiling* I come here because I like you. There. I said it.",
        ],
        special_gifts=["rare_swamp_crystal", "ancient_tadpole_fossil", "grumble_cookie"],
        conversations=[
            "Everyone thinks toads are grumpy. It's a defense mechanism.",
            "I had a friend once. A dragonfly. Good times.",
            "Rain is the only weather that makes sense.",
            "My swamp is actually very cozy. Not that I'm inviting you.",
        ],
        secrets=["I write poetry. It's all about friendship. Tell no one."],
    ),
}


# =============================================================================
# ATMOSPHERE MANAGER
# =============================================================================

class AtmosphereManager:
    """
    Manages weather, seasons, luck, and visitors.
    Creates dynamic world that changes over time.
    """

    def __init__(self):
        # Per-biome persistent weather storage
        self._biome_weather: Dict[str, Weather] = {}
        self._current_biome: str = "pond"  # Active biome for weather resolution

        self.current_season: Season = self._calculate_season()
        self.day_fortune: Optional[DayFortune] = None
        self.current_visitor: Optional[Tuple[Visitor, str]] = None  # (visitor, arrival_time)
        self.last_fortune_date: Optional[str] = None
        self.last_weather_check: Optional[str] = None
        self.visitor_history: List[str] = []  # Track who has visited
        self.weather_history: List[str] = []  # Recent weather
        self.visitor_friendships: Dict[str, VisitorFriendship] = {}  # Track friendships

        # Generate initial weather for every known biome
        for biome in _ALL_BIOMES:
            self._generate_weather(biome)
        self._generate_fortune()

    # ── Per-biome weather property (backward-compatible) ────────────────

    @property
    def current_weather(self) -> Optional[Weather]:
        """Get weather for the current biome."""
        return self._biome_weather.get(self._current_biome)

    @current_weather.setter
    def current_weather(self, value: Optional[Weather]):
        """Set weather for the current biome."""
        if value is None:
            self._biome_weather.pop(self._current_biome, None)
        else:
            self._biome_weather[self._current_biome] = value

    def set_current_biome(self, biome: str):
        """Switch the active biome for weather resolution.

        Called when the duck travels to a new area.  Ensures the
        destination biome already has weather generated.
        """
        self._current_biome = biome
        if biome not in self._biome_weather:
            self._generate_weather(biome)

    def get_biome_weather(self, biome: str) -> Optional[Weather]:
        """Get weather for a specific biome without changing the active one."""
        return self._biome_weather.get(biome)

    def get_all_biome_weather(self) -> Dict[str, Optional[Weather]]:
        """Get weather dict for all biomes (useful for map overview)."""
        return dict(self._biome_weather)

    def _calculate_season(self) -> Season:
        """Determine current season based on date."""
        month = datetime.now().month
        if month in [3, 4, 5]:
            return Season.SPRING
        elif month in [6, 7, 8]:
            return Season.SUMMER
        elif month in [9, 10, 11]:
            return Season.FALL
        else:
            return Season.WINTER

    def _generate_weather(self, biome: Optional[str] = None):
        """Generate new weather based on season and biome.

        Each biome has its own probability modifiers that make certain
        weather types more or less likely (e.g. swamps are foggier,
        mountains are windier, beaches are sunnier).
        """
        if biome is None:
            biome = self._current_biome

        season = self.current_season
        season_key = f"{season.value}_prob"

        # Get biome-specific probability modifiers
        biome_mods = BIOME_WEATHER_MODIFIERS.get(biome, {})

        # Build weighted list with biome modifiers applied
        weather_options = []
        for weather_type, data in WEATHER_DATA.items():
            if data.get("special"):
                continue  # Skip special weather like rainbow
            prob = data.get(season_key, 0.0)
            if prob > 0:
                modifier = biome_mods.get(weather_type, 1.0)
                weight = int(prob * modifier * 100)
                weather_options.extend([weather_type] * max(1, weight))

        # Fallback to sunny if no options (shouldn't happen)
        if not weather_options:
            weather_options = [WeatherType.SUNNY]

        chosen_type = random.choice(weather_options)
        data = WEATHER_DATA[chosen_type]

        # Determine duration (3-12 hours) - weather changes less frequently
        duration = random.uniform(3, 12)

        self._biome_weather[biome] = Weather(
            weather_type=chosen_type,
            intensity=random.uniform(0.3, 1.0),
            duration_hours=duration,
            start_time=datetime.now().isoformat(),
            mood_modifier=data.get("mood_modifier", 0),
            xp_multiplier=data.get("xp_multiplier", 1.0),
            special_message=data.get("message", ""),
        )

        self.weather_history.append(chosen_type.value)
        if len(self.weather_history) > 10:
            self.weather_history = self.weather_history[-10:]

        self.last_weather_check = datetime.now().strftime("%Y-%m-%d %H")

    def _maybe_rainbow(self, biome: Optional[str] = None):
        """Check if rainbow should appear after rain in a specific biome."""
        if biome is None:
            biome = self._current_biome

        weather = self._biome_weather.get(biome)
        if not weather:
            return

        # Check if this weather type can trigger a rainbow
        weather_data = WEATHER_DATA.get(weather.weather_type, {})
        if not weather_data.get("triggers_rainbow", False):
            return

        # Rainbow can appear after rain ends (20% chance, 5% for double rainbow!)
        if not weather.is_active():
            if random.random() < 0.05:
                # Ultra rare double rainbow!
                data = WEATHER_DATA[WeatherType.DOUBLE_RAINBOW]
                self._biome_weather[biome] = Weather(
                    weather_type=WeatherType.DOUBLE_RAINBOW,
                    intensity=1.0,
                    duration_hours=0.3,  # Very short but AMAZING
                    start_time=datetime.now().isoformat(),
                    mood_modifier=data.get("mood_modifier", 0),
                    xp_multiplier=data.get("xp_multiplier", 1.0),
                    special_message=data.get("message", ""),
                )
            elif random.random() < 0.2:
                data = WEATHER_DATA[WeatherType.RAINBOW]
                self._biome_weather[biome] = Weather(
                    weather_type=WeatherType.RAINBOW,
                    intensity=1.0,
                    duration_hours=0.5,  # Short but magical
                    start_time=datetime.now().isoformat(),
                    mood_modifier=data.get("mood_modifier", 0),
                    xp_multiplier=data.get("xp_multiplier", 1.0),
                    special_message=data.get("message", ""),
                )

    def _generate_fortune(self):
        """Generate fortune for the day."""
        today = datetime.now().strftime("%Y-%m-%d")

        if self.last_fortune_date == today and self.day_fortune:
            return

        # Roll for fortune type
        roll = random.random()
        cumulative = 0
        chosen_type = "normal"

        for fortune_type, data in FORTUNE_TYPES.items():
            cumulative += data["probability"]
            if roll < cumulative:
                chosen_type = fortune_type
                break

        data = FORTUNE_TYPES[chosen_type]

        self.day_fortune = DayFortune(
            fortune_type=chosen_type,
            xp_multiplier=data["xp_multiplier"],
            drop_rate_modifier=data["drop_rate_modifier"],
            special_message=random.choice(data["messages"]),
            horoscope=random.choice(data["horoscopes"]),
        )

        self.last_fortune_date = today

    def update(self) -> List[str]:
        """
        Update atmosphere state. Call periodically.
        Returns list of messages about changes.
        """
        messages = []

        # Update season if needed
        new_season = self._calculate_season()
        if new_season != self.current_season:
            self.current_season = new_season
            content = SEASONAL_CONTENT[new_season]
            messages.append(f"Season changed to {new_season.value}! {content.mood_theme.title()} vibes!")

        # Update weather for ALL biomes (per-biome persistent weather)
        for biome in list(self._biome_weather.keys()):
            weather = self._biome_weather.get(biome)
            if weather and not weather.is_active():
                # Try rainbow after rain
                self._maybe_rainbow(biome)
                # Check if a rainbow was placed (it would be freshly active)
                weather = self._biome_weather.get(biome)
                if not weather or not weather.is_active():
                    # No rainbow — generate fresh weather for this biome
                    self._generate_weather(biome)
                    # Only report weather changes in the duck's current biome
                    if biome == self._current_biome:
                        new_w = self._biome_weather.get(biome)
                        if new_w:
                            messages.append(f"Weather changed: {new_w.special_message}")

        # Ensure current biome always has weather
        if self._current_biome not in self._biome_weather:
            self._generate_weather(self._current_biome)
            weather = self._biome_weather.get(self._current_biome)
            if weather:
                messages.append(f"Weather: {weather.special_message}")

        # Check fortune
        today = datetime.now().strftime("%Y-%m-%d")
        if self.last_fortune_date != today:
            self._generate_fortune()
            messages.append(f"Today's fortune: {self.day_fortune.horoscope}")

        # Check for visitor
        visitor_msg = self._check_visitor()
        if visitor_msg:
            messages.append(visitor_msg)

        return messages

    def _check_visitor(self) -> Optional[str]:
        """Check if a visitor should appear or leave."""
        # Check if current visitor should leave
        if self.current_visitor:
            visitor, arrival = self.current_visitor
            try:
                arrival_time = datetime.fromisoformat(arrival)
                elapsed = (datetime.now() - arrival_time).total_seconds() / 3600
                if elapsed >= visitor.stay_duration_hours:
                    self.current_visitor = None
                    return visitor.farewell
            except (ValueError, TypeError, AttributeError):
                self.current_visitor = None

        # Maybe spawn new visitor (higher chance for friends)
        # Base 1% chance per check (every 30 seconds) for visitors - kept rare
        if not self.current_visitor and random.random() < 0.01:
            # Build weighted visitor list (friends visit more often)
            candidates = []
            for visitor_id, visitor in VISITORS.items():
                base_chance = visitor.appearance_chance

                # Increase chance for visitors with higher friendship
                if visitor_id in self.visitor_friendships:
                    friendship = self.visitor_friendships[visitor_id]
                    if friendship.level == FriendshipLevel.BEST_FRIEND:
                        base_chance *= 3.0
                    elif friendship.level == FriendshipLevel.GOOD_FRIEND:
                        base_chance *= 2.5
                    elif friendship.level == FriendshipLevel.FRIEND:
                        base_chance *= 2.0
                    elif friendship.level == FriendshipLevel.ACQUAINTANCE:
                        base_chance *= 1.5

                # Increase chance if weather/season matches preference
                if self.current_weather and visitor.favorite_weather:
                    if self.current_weather.weather_type.value == visitor.favorite_weather:
                        base_chance *= 1.5

                if visitor.favorite_season and self.current_season.value == visitor.favorite_season:
                    base_chance *= 1.3

                # Cap probability at 1.0 to prevent guaranteed appearances
                base_chance = min(base_chance, 1.0)

                if random.random() < base_chance:
                    candidates.append(visitor_id)

            if candidates:
                visitor_id = random.choice(candidates)
                visitor = VISITORS[visitor_id]
                self.current_visitor = (visitor, datetime.now().isoformat())
                self.visitor_history.append(visitor_id)

                # Keep history manageable to prevent memory leak
                if len(self.visitor_history) > 50:
                    self.visitor_history = self.visitor_history[-50:]

                # Track friendship
                if visitor_id not in self.visitor_friendships:
                    self.visitor_friendships[visitor_id] = VisitorFriendship(visitor_id=visitor_id)
                self.visitor_friendships[visitor_id].add_visit()

                return self._get_visitor_greeting(visitor, visitor_id)

        return None

    def _get_visitor_greeting(self, visitor: Visitor, visitor_id: str) -> str:
        """Get appropriate greeting based on friendship level."""
        if visitor_id not in self.visitor_friendships:
            return visitor.greeting

        friendship = self.visitor_friendships[visitor_id]
        visit_count = friendship.visit_count

        # First visit
        if visit_count <= 1:
            return visitor.greeting

        # Get greeting based on friendship level
        level = friendship.level
        if level == FriendshipLevel.BEST_FRIEND and visitor.best_friend_greetings:
            return random.choice(visitor.best_friend_greetings)
        elif level in [FriendshipLevel.GOOD_FRIEND, FriendshipLevel.FRIEND] and visitor.friend_greetings:
            return random.choice(visitor.friend_greetings)
        elif visitor.return_greetings:
            return random.choice(visitor.return_greetings)

        return visitor.greeting

    def get_visitor_friendship(self, visitor_id: str) -> Optional[VisitorFriendship]:
        """Get friendship data for a visitor."""
        return self.visitor_friendships.get(visitor_id)

    def get_weather_display(self) -> List[str]:
        """Get ASCII art for current weather."""
        if not self.current_weather:
            return []
        data = WEATHER_DATA.get(self.current_weather.weather_type, {})
        return data.get("ascii", [])

    def get_total_xp_multiplier(self) -> float:
        """Get combined XP multiplier from all sources."""
        multiplier = 1.0

        # Season bonus
        season_content = SEASONAL_CONTENT.get(self.current_season)
        if season_content:
            multiplier *= season_content.xp_bonus

        # Weather bonus
        if self.current_weather:
            multiplier *= self.current_weather.xp_multiplier

        # Fortune bonus
        if self.day_fortune:
            multiplier *= self.day_fortune.xp_multiplier

        return multiplier

    def get_drop_rate_modifier(self) -> float:
        """Get combined drop rate modifier."""
        modifier = 1.0

        # Fortune modifier
        if self.day_fortune:
            modifier *= self.day_fortune.drop_rate_modifier

        # Foggy weather bonus
        if self.current_weather and self.current_weather.weather_type == WeatherType.FOGGY:
            modifier *= 1.5

        return modifier

    def get_mood_modifier(self) -> int:
        """Get combined mood modifier."""
        mood = 0

        if self.current_weather:
            mood += self.current_weather.mood_modifier

        if self.current_visitor:
            mood += self.current_visitor[0].mood_boost

        return mood

    def interact_with_visitor(self) -> Optional[Tuple[str, Optional[str]]]:
        """
        Interact with current visitor.
        Returns (message, gift_item_id) or None if no visitor.
        """
        if not self.current_visitor:
            return None

        visitor, _ = self.current_visitor
        visitor_id = visitor.id

        # Add friendship points for interaction
        if visitor_id in self.visitor_friendships:
            self.visitor_friendships[visitor_id].add_interaction(1)

        friendship = self.visitor_friendships.get(visitor_id)
        level = friendship.level if friendship else FriendshipLevel.STRANGER

        # Check for gift (better gifts at higher friendship)
        gift = None
        gift_chance = visitor.gift_chance

        # Higher friendship = better gift chance
        if level == FriendshipLevel.BEST_FRIEND:
            gift_chance = min(1.0, gift_chance + 0.3)
        elif level == FriendshipLevel.GOOD_FRIEND:
            gift_chance = min(1.0, gift_chance + 0.2)
        elif level == FriendshipLevel.FRIEND:
            gift_chance = min(1.0, gift_chance + 0.1)

        if random.random() < gift_chance:
            # Best friends get special gifts
            if level == FriendshipLevel.BEST_FRIEND and visitor.special_gifts:
                gift = random.choice(visitor.special_gifts)
                message = f"{visitor.name}: *gives you something special* For my best friend!"
            elif visitor.possible_gifts:
                gift = random.choice(visitor.possible_gifts)
                message = f"{visitor.name}: *gives you something* Here, take this!"
            else:
                gift = None
                message = f"{visitor.name}: I wish I had something to give you!"
        else:
            # Get conversation based on friendship level
            if level == FriendshipLevel.BEST_FRIEND and visitor.secrets:
                # Chance to share a secret
                if random.random() < 0.3:
                    secret = random.choice(visitor.secrets)
                    message = f"{visitor.name}: *whispers* Can I tell you a secret? {secret}"
                elif visitor.conversations:
                    message = f"{visitor.name}: {random.choice(visitor.conversations)}"
                else:
                    message = f"{visitor.name}: *happy* It's always so nice to see you!"
            elif visitor.conversations and random.random() < 0.5:
                message = f"{visitor.name}: {random.choice(visitor.conversations)}"
            else:
                responses = [
                    f"{visitor.name}: *quacks happily* Nice to meet you!",
                    f"{visitor.name}: This is a lovely place you have here!",
                    f"{visitor.name}: *nods approvingly* You take good care of Cheese!",
                ]
                message = random.choice(responses)

        # Track gift if received
        if gift and friendship:
            friendship.gifts_received.append(gift)

        return (message, gift)

    def get_all_friendships(self) -> List[Tuple[Visitor, VisitorFriendship]]:
        """Get all visitor friendships for display."""
        result = []
        for visitor_id, friendship in self.visitor_friendships.items():
            if visitor_id in VISITORS:
                result.append((VISITORS[visitor_id], friendship))
        return sorted(result, key=lambda x: x[1].friendship_points, reverse=True)

    def get_seasonal_items(self) -> List[str]:
        """Get items available this season."""
        content = SEASONAL_CONTENT.get(self.current_season)
        return content.items_available if content else []

    def get_active_seasonal_event(self) -> Optional[SeasonalEvent]:
        """Check if there's an active seasonal event."""
        now = datetime.now()
        day_of_month = now.day

        for event_id, event in SEASONAL_EVENTS.items():
            if event.season != self.current_season:
                continue

            # Check if event is active
            start = event.start_day
            end = start + event.duration_days

            if start <= day_of_month < end:
                return event

        return None

    def get_seasonal_greeting(self) -> str:
        """Get a seasonal greeting message."""
        content = SEASONAL_CONTENT.get(self.current_season)
        if content and content.greeting_messages:
            return random.choice(content.greeting_messages)
        return "Welcome back!"

    def get_seasonal_activity_bonus(self, activity: str) -> float:
        """Get bonus multiplier for seasonal activities."""
        content = SEASONAL_CONTENT.get(self.current_season)
        if content and activity in content.special_activities:
            return 1.5  # 50% bonus for in-season activities

        # Check active events
        event = self.get_active_seasonal_event()
        if event and activity in event.activities:
            return event.xp_bonus

        return 1.0

    def get_seasonal_drop_bonus(self) -> Tuple[float, List[str]]:
        """Get drop rate bonus and special drops for current season/event."""
        bonus = 1.0
        special_drops = []

        # Check active event
        event = self.get_active_seasonal_event()
        if event:
            bonus = event.xp_bonus
            special_drops = event.special_drops

        return bonus, special_drops

    def get_seasonal_ambient_effects(self) -> List[str]:
        """Get ambient visual effects for current season."""
        content = SEASONAL_CONTENT.get(self.current_season)
        return content.ambient_effects if content else []

    def get_seasonal_decorations(self) -> List[str]:
        """Get available seasonal decorations."""
        content = SEASONAL_CONTENT.get(self.current_season)
        return content.decorations if content else []

    def get_event_message(self) -> Optional[str]:
        """Get a message about the current event if active."""
        event = self.get_active_seasonal_event()
        if event and event.messages:
            return random.choice(event.messages)
        return None

    def get_weather_remaining_hours(self) -> float:
        """Get how many hours the current weather has left."""
        if not self.current_weather:
            return 0.0
        try:
            start = datetime.fromisoformat(self.current_weather.start_time)
            elapsed = (datetime.now() - start).total_seconds() / 3600
            return max(0.0, self.current_weather.duration_hours - elapsed)
        except (ValueError, TypeError):
            return 0.0

    def forecast_next_weather(self) -> Tuple[WeatherType, float]:
        """Predict the most likely next weather based on season probabilities.
        
        Returns:
            (weather_type, confidence) where confidence is 0.0-1.0
        """
        season_key = f"{self.current_season.value}_prob"
        weights: Dict[WeatherType, float] = {}
        
        for weather_type, data in WEATHER_DATA.items():
            if data.get("special"):
                continue
            prob = data.get(season_key, 0.0)
            if prob > 0:
                weights[weather_type] = prob
        
        if not weights:
            return WeatherType.SUNNY, 1.0
        
        total = sum(weights.values())
        top = max(weights, key=weights.get)
        return top, weights[top] / total if total > 0 else 0.0

    def get_status_display(self) -> Dict[str, str]:
        """Get current atmosphere status for display."""
        status = {
            "season": self.current_season.value.title(),
            "weather": "Unknown",
            "fortune": "Normal",
            "visitor": "None",
        }

        if self.current_weather:
            data = WEATHER_DATA.get(self.current_weather.weather_type, {})
            status["weather"] = data.get("name", self.current_weather.weather_type.value)

        if self.day_fortune:
            status["fortune"] = self.day_fortune.fortune_type.replace("_", " ").title()

        if self.current_visitor:
            status["visitor"] = self.current_visitor[0].name

        return status

    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        # Save visitor friendships
        friendships_data = {}
        for visitor_id, friendship in self.visitor_friendships.items():
            friendships_data[visitor_id] = {
                "visit_count": friendship.visit_count,
                "friendship_points": friendship.friendship_points,
                "last_visit": friendship.last_visit,
                "gifts_received": friendship.gifts_received[-20:],  # Keep last 20
                "special_moments": friendship.special_moments[-10:],  # Keep last 10
            }

        return {
            "current_season": self.current_season.value,
            "current_biome": self._current_biome,
            "biome_weather": {
                biome: {
                    "type": w.weather_type.value,
                    "intensity": w.intensity,
                    "duration": w.duration_hours,
                    "start": w.start_time,
                } for biome, w in self._biome_weather.items() if w
            },
            # Legacy key kept for backward compatibility
            "current_weather": {
                "type": self.current_weather.weather_type.value,
                "intensity": self.current_weather.intensity,
                "duration": self.current_weather.duration_hours,
                "start": self.current_weather.start_time,
            } if self.current_weather else None,
            "day_fortune": {
                "type": self.day_fortune.fortune_type,
                "xp_mult": self.day_fortune.xp_multiplier,
                "drop_mult": self.day_fortune.drop_rate_modifier,
                "message": self.day_fortune.special_message,
                "horoscope": self.day_fortune.horoscope,
            } if self.day_fortune else None,
            "last_fortune_date": self.last_fortune_date,
            "visitor_history": self.visitor_history[-20:],  # Keep last 20
            "weather_history": self.weather_history,
            "visitor_friendships": friendships_data,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AtmosphereManager":
        """Create from dictionary."""
        atm = cls()

        # Restore current biome
        atm._current_biome = data.get("current_biome", "pond")

        if data.get("current_season"):
            try:
                atm.current_season = Season(data["current_season"])
            except (ValueError, KeyError):
                pass

        # Restore per-biome weather (new format)
        if data.get("biome_weather"):
            for biome, w in data["biome_weather"].items():
                try:
                    weather_type = WeatherType(w["type"])
                    weather_data = WEATHER_DATA.get(weather_type, {})
                    atm._biome_weather[biome] = Weather(
                        weather_type=weather_type,
                        intensity=w.get("intensity", 0.5),
                        duration_hours=w.get("duration", 3),
                        start_time=w.get("start", datetime.now().isoformat()),
                        mood_modifier=weather_data.get("mood_modifier", 0),
                        xp_multiplier=weather_data.get("xp_multiplier", 1.0),
                        special_message=weather_data.get("message", ""),
                    )
                except (ValueError, KeyError, TypeError):
                    pass
        elif data.get("current_weather"):
            # Backward compat: old save with single weather → assign to current biome
            w = data["current_weather"]
            try:
                weather_type = WeatherType(w["type"])
                weather_data = WEATHER_DATA.get(weather_type, {})
                atm._biome_weather[atm._current_biome] = Weather(
                    weather_type=weather_type,
                    intensity=w.get("intensity", 0.5),
                    duration_hours=w.get("duration", 3),
                    start_time=w.get("start", datetime.now().isoformat()),
                    mood_modifier=weather_data.get("mood_modifier", 0),
                    xp_multiplier=weather_data.get("xp_multiplier", 1.0),
                    special_message=weather_data.get("message", ""),
                )
            except (ValueError, KeyError, TypeError):
                pass

        if data.get("day_fortune"):
            f = data["day_fortune"]
            atm.day_fortune = DayFortune(
                fortune_type=f.get("type", "normal"),
                xp_multiplier=f.get("xp_mult", 1.0),
                drop_rate_modifier=f.get("drop_mult", 1.0),
                special_message=f.get("message", ""),
                horoscope=f.get("horoscope", ""),
            )

        atm.last_fortune_date = data.get("last_fortune_date")
        atm.visitor_history = data.get("visitor_history", [])
        atm.weather_history = data.get("weather_history", [])

        # Load visitor friendships
        if data.get("visitor_friendships"):
            for visitor_id, f_data in data["visitor_friendships"].items():
                atm.visitor_friendships[visitor_id] = VisitorFriendship(
                    visitor_id=visitor_id,
                    visit_count=f_data.get("visit_count", 0),
                    friendship_points=f_data.get("friendship_points", 0),
                    last_visit=f_data.get("last_visit"),
                    gifts_received=f_data.get("gifts_received", []),
                    special_moments=f_data.get("special_moments", []),
                )

        return atm


# Global instance
atmosphere = AtmosphereManager()
