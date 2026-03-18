"""
Unified particle system for weather effects and biome ambient particles.

Replaces both ``Renderer._generate_weather_decorations()`` and
``Renderer._update_ambient_particles()`` with a single, composable system.
All particle configs, movement, spawning, and despawning are handled here
with no Terminal/UI dependency -- callers receive integer positions and RGB
colours ready for rendering.

Performance note: this system is designed for 60 fps.  Weather and ambient
particles internally skip every other update (effective 30 fps) to match the
original renderer behaviour and keep motion natural.
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple


# ── Enums ─────────────────────────────────────────────────────────────────────

class ParticleDirection(Enum):
    """Movement direction for particles."""
    FALL = "fall"
    FLOAT_UP = "float_up"
    DRIFT_RIGHT = "drift_right"
    DRIFT_LEFT = "drift_left"
    STATIC = "static"
    SWIRL = "swirl"


# ── Data classes ──────────────────────────────────────────────────────────────

@dataclass
class ParticleConfig:
    """Template for spawning a category of particles.

    Attributes:
        chars: Characters randomly chosen when spawning.
        color_rgb: (R, G, B) colour for rendering.
        direction: How the particle moves each tick.
        speed: Movement magnitude (cells per second at 30 effective fps).
        density: Spawn probability factor (0.0 -- 1.0).
        lifetime: Seconds before automatic despawn.  ``None`` = permanent
                  (removed only when leaving bounds).
        time_filter: If set, particle only spawns during these time periods.
        season_filter: If set, particle only spawns during these seasons.
        weather_suppression: If current weather intensity exceeds this value
                            the config is skipped (default 0.7).
    """
    chars: List[str]
    color_rgb: Tuple[int, int, int]
    direction: ParticleDirection
    speed: float
    density: float
    lifetime: Optional[float] = None
    time_filter: Optional[List[str]] = None
    season_filter: Optional[List[str]] = None
    weather_suppression: float = 0.7


@dataclass
class Particle:
    """A single live particle instance.

    Attributes:
        x: Current x position (float for sub-cell precision).
        y: Current y position.
        char: Character to render.
        color_rgb: RGB colour tuple.
        direction: Movement direction.
        speed: Movement speed.
        age: Seconds since spawn.
        lifetime: Maximum lifetime or ``None``.
    """
    x: float
    y: float
    char: str
    color_rgb: Tuple[int, int, int]
    direction: ParticleDirection
    speed: float
    age: float = 0.0
    lifetime: Optional[float] = None


# ── Main particle system ─────────────────────────────────────────────────────

class ParticleSystem:
    """Manages weather and ambient particles within a bounded region.

    Usage:
        system = ParticleSystem(width=44, height=14)
        system.configure_weather("rainy", 0.5)
        system.configure_biome("forest", "night", "fall")

        # Each frame:
        system.update(delta_time)
        for ix, iy, ch, rgb in system.get_particles():
            render(ix, iy, ch, rgb)
    """

    def __init__(self, width: int, height: int, max_particles: int = 50) -> None:
        self._width: int = width
        self._height: int = height
        self._max_particles: int = max_particles

        self._weather_particles: List[Particle] = []
        self._ambient_particles: List[Particle] = []

        self._weather_configs: List[ParticleConfig] = []
        self._ambient_configs: List[ParticleConfig] = []

        self._weather_type: Optional[str] = None
        self._weather_intensity: float = 0.0

        # Frame counter for 30-fps skip logic (matches original renderer)
        self._frame: int = 0

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """Remove all particles and configs."""
        self._weather_particles.clear()
        self._ambient_particles.clear()
        self._weather_configs.clear()
        self._ambient_configs.clear()
        self._weather_type = None
        self._weather_intensity = 0.0
        self._frame = 0

    def set_bounds(self, width: int, height: int) -> None:
        """Update playfield dimensions (e.g. after terminal resize)."""
        self._width = width
        self._height = height

    def configure_weather(self, weather_type: Optional[str], intensity: float) -> None:
        """Set up weather particle configs.

        If the weather type changed, existing weather particles are flushed
        and new configs are loaded from :class:`WeatherParticles`.
        """
        if weather_type == self._weather_type and abs(intensity - self._weather_intensity) < 0.01:
            return

        self._weather_type = weather_type
        self._weather_intensity = intensity
        self._weather_particles.clear()

        if not weather_type:
            self._weather_configs = []
            return

        self._weather_configs = WeatherParticles.get_config(weather_type, intensity)

    def configure_biome(self, biome: str, time_of_day: str, season: str) -> None:
        """Set up biome-specific ambient particle configs.

        Loads from :class:`BiomeParticles` and filters by time/season.
        """
        all_configs = BiomeParticles.get_config(biome)
        active: List[ParticleConfig] = []
        for cfg in all_configs:
            if cfg.time_filter is not None and time_of_day not in cfg.time_filter:
                continue
            if cfg.season_filter is not None and season not in cfg.season_filter:
                continue
            active.append(cfg)

        self._ambient_configs = active
        # Don't clear existing ambient particles -- they age out naturally

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def update(self, delta_time: float) -> None:
        """Move all particles, spawn new ones, despawn expired ones.

        Should be called once per render frame.  Internally skips every other
        frame to match the 30-fps effective rate of the original renderer.
        """
        self._frame += 1

        # Skip every other frame (effective 30 fps at 60 fps render rate)
        if self._frame % 2 == 0:
            return

        self._update_weather(delta_time)
        self._update_ambient(delta_time)

    def get_particles(self) -> List[Tuple[int, int, str, Tuple[int, int, int]]]:
        """Return all live particles as ``(x, y, char, rgb)`` with integer positions."""
        result: List[Tuple[int, int, str, Tuple[int, int, int]]] = []
        for p in self._weather_particles:
            ix, iy = int(p.x), int(p.y)
            if 0 <= ix < self._width and 0 <= iy < self._height:
                result.append((ix, iy, p.char, p.color_rgb))
        for p in self._ambient_particles:
            ix, iy = int(p.x), int(p.y)
            if 0 <= ix < self._width and 0 <= iy < self._height:
                result.append((ix, iy, p.char, p.color_rgb))
        return result

    # ------------------------------------------------------------------
    # Weather particle update (ported from _update_weather_particles)
    # ------------------------------------------------------------------

    def _update_weather(self, delta_time: float) -> None:
        """Move and spawn weather particles."""
        if not self._weather_configs:
            self._weather_particles.clear()
            return

        wtype = self._weather_type or ""

        # --- Move existing ---
        alive: List[Particle] = []
        for p in self._weather_particles:
            p.age += delta_time
            if p.lifetime is not None and p.age >= p.lifetime:
                continue

            ny = p.y + p.speed
            nx = p.x

            # Horizontal drift per weather type (ported from original)
            if wtype in ("windy", "wind", "blizzard", "leaf_storm"):
                nx += 0.8
            elif wtype in ("autumn_wind", "gentle_wind", "breezy"):
                nx += 0.5
            elif wtype in ("snowy", "snow", "light_snow", "heavy_snow", "flurries"):
                nx += random.uniform(-0.3, 0.3)
            elif wtype == "falling_leaves":
                nx += random.uniform(-0.4, 0.4)
            elif wtype in ("stormy", "storm", "thunderstorm", "summer_storm"):
                nx += random.uniform(-0.5, 0.5)
            elif wtype == "aurora":
                nx += math.sin(self._frame * 0.1 + p.y) * 0.3
            elif wtype == "meteors":
                nx += 1.5
            elif wtype == "pollen":
                nx += random.uniform(-0.2, 0.4)
            elif wtype == "heat_shimmer":
                nx += math.sin(self._frame * 0.2 + p.x) * 0.2

            if 0 <= nx < self._width and ny < self._height:
                p.x = nx
                p.y = ny
                alive.append(p)

        # --- Spawn new particles at edge ---
        for cfg in self._weather_configs:
            spawn_y = float(self._height - 1) if cfg.direction == ParticleDirection.FLOAT_UP else 0.0
            for col in range(self._width):
                if random.random() < cfg.density:
                    alive.append(Particle(
                        x=float(col),
                        y=spawn_y,
                        char=random.choice(cfg.chars),
                        color_rgb=cfg.color_rgb,
                        direction=cfg.direction,
                        speed=cfg.speed,
                        lifetime=cfg.lifetime,
                    ))

        # --- Lightning for storm types (every ~1.5 s at 60 fps) ---
        if wtype in ("stormy", "storm", "thunderstorm", "summer_storm", "ice_storm"):
            if self._frame % 90 == 0 and random.random() < 0.25:
                bolt_x = random.randint(3, max(3, self._width - 3))
                bolt_y = random.randint(0, min(3, self._height - 1))
                alive.append(Particle(
                    x=float(bolt_x), y=float(bolt_y),
                    char="!", color_rgb=(255, 255, 150),
                    direction=ParticleDirection.STATIC, speed=0.0,
                    lifetime=0.1,
                ))
                if wtype == "thunderstorm" and random.random() < 0.5:
                    alive.append(Particle(
                        x=float(random.randint(3, max(3, self._width - 3))),
                        y=float(bolt_y + 1),
                        char="!", color_rgb=(255, 255, 150),
                        direction=ParticleDirection.STATIC, speed=0.0,
                        lifetime=0.1,
                    ))

        # --- Aurora wave lines ---
        if wtype == "aurora":
            if self._frame % 20 == 0:
                wave_y = random.randint(0, min(5, self._height - 1))
                for wx in range(0, self._width, random.randint(3, 6)):
                    alive.append(Particle(
                        x=float(wx), y=float(wave_y),
                        char=random.choice(["|", "~", "/", "\\"]),
                        color_rgb=(100, 255, 200),
                        direction=ParticleDirection.STATIC, speed=0.0,
                        lifetime=0.35,
                    ))

        self._weather_particles = alive

    # ------------------------------------------------------------------
    # Ambient particle update (ported from _update_ambient_particles)
    # ------------------------------------------------------------------

    def _update_ambient(self, delta_time: float) -> None:
        """Move and spawn biome ambient particles."""
        # Suppress during heavy weather
        if self._weather_intensity > 0.7 or not self._ambient_configs:
            self._ambient_particles.clear()
            return

        alive: List[Particle] = []

        for p in self._ambient_particles:
            p.age += delta_time
            if p.lifetime is not None and p.age >= p.lifetime:
                continue

            nx, ny = p.x, p.y

            if p.direction == ParticleDirection.FALL:
                ny += p.speed
                nx += random.uniform(-0.15, 0.15)
            elif p.direction == ParticleDirection.FLOAT_UP:
                ny += random.uniform(-p.speed, p.speed)
                nx += random.uniform(-p.speed, p.speed)
            elif p.direction == ParticleDirection.DRIFT_RIGHT:
                ny += random.uniform(-0.05, 0.05)
                nx += p.speed
            elif p.direction == ParticleDirection.DRIFT_LEFT:
                ny += random.uniform(-0.05, 0.05)
                nx -= p.speed
            elif p.direction == ParticleDirection.STATIC:
                # Static particles fade out randomly
                if random.random() < 0.03:
                    continue
            elif p.direction == ParticleDirection.SWIRL:
                angle = p.age * 2.0
                nx += math.sin(angle) * p.speed
                ny += math.cos(angle) * p.speed * 0.5

            if 0 <= nx < self._width and 0 <= ny < self._height:
                p.x = nx
                p.y = ny
                alive.append(p)

        # Spawn new particles from active configs
        for cfg in self._ambient_configs:
            spawn_count = cfg.density * self._width * self._height * 0.02
            if random.random() < spawn_count:
                char = random.choice(cfg.chars)

                if cfg.direction == ParticleDirection.FALL:
                    sx = random.uniform(0, self._width - 1)
                    sy = 0.0
                elif cfg.direction == ParticleDirection.FLOAT_UP:
                    sx = random.uniform(0, self._width - 1)
                    sy = random.uniform(0, self._height - 1)
                elif cfg.direction == ParticleDirection.DRIFT_RIGHT:
                    sx = 0.0
                    sy = random.uniform(0, self._height - 1)
                elif cfg.direction == ParticleDirection.DRIFT_LEFT:
                    sx = float(self._width - 1)
                    sy = random.uniform(0, self._height - 1)
                elif cfg.direction == ParticleDirection.STATIC:
                    sx = random.uniform(0, self._width - 1)
                    sy = random.uniform(0, self._height * 0.4)
                else:
                    sx = random.uniform(0, self._width - 1)
                    sy = random.uniform(0, self._height - 1)

                alive.append(Particle(
                    x=sx, y=sy,
                    char=char,
                    color_rgb=cfg.color_rgb,
                    direction=cfg.direction,
                    speed=cfg.speed,
                    lifetime=cfg.lifetime,
                ))

        # Cap particle count
        max_ambient = 20
        if len(alive) > max_ambient:
            alive = alive[-max_ambient:]

        self._ambient_particles = alive


# ── WeatherParticles config factory ───────────────────────────────────────────

class WeatherParticles:
    """Static factory returning :class:`ParticleConfig` lists for weather types.

    All character sets, densities, and speeds are ported directly from the
    original ``Renderer._update_weather_particles`` dictionaries.
    """

    # Chars per weather type
    _CHARS: Dict[str, List[str]] = {
        # Rain variants
        "drizzle": ["'", ",", "'", "."],
        "rain": ["|", "|", "'", ",", ":", "'"],
        "rainy": ["|", "|", "'", ",", ":", "'"],
        "heavy_rain": ["|", "|", "|", "'", ",", "|", ":"],
        "spring_rain": ["|", "'", ",", "~"],
        "storm": ["|", "|", "'", ",", ":"],
        "stormy": ["|", "|", "'", ",", ":"],
        "thunderstorm": ["|", "|", "!", "|", ",", "!", ":"],
        "summer_storm": ["|", "|", "|", "'", "!", "|"],
        # Snow variants
        "light_snow": ["*", ".", "*", "."],
        "snow": ["*", "*", "*", "*", ".", "o", "*"],
        "snowy": ["*", "*", "*", "*", ".", "o", "*"],
        "heavy_snow": ["*", "*", "o", "*", "*", "O", "*"],
        "flurries": ["*", ".", "*", ".", "*"],
        "blizzard": ["*", "*", "*", "/", "\\", "*", "O"],
        # Ice variants
        "sleet": ["'", "|", "'", ",", "|", "."],
        "hail": ["o", "o", "O", "o", "."],
        "ice_storm": ["|", "'", "o", "|", "'"],
        # Fog/mist
        "fog": [".", "~", "~", "~", " ", "#"],
        "foggy": [".", "~", "~", "~", " ", "#"],
        "mist": [".", "~", " ", "~", "."],
        # Wind variants
        "wind": [">", ">", "~", ">", "~", "-", "~"],
        "windy": [">", ">", "~", ">", "~", "-", "~"],
        "gentle_wind": ["~", "-", "~", " ", "~"],
        "autumn_wind": [">", "}", "{", ">", "~"],
        # Leaf particles
        "falling_leaves": ["{", "}", "(", ")", "~"],
        "leaf_storm": ["{", "}", "{", ">", "}", ">", "{"],
        # Special effects
        "pollen": [".", "\u00b0", ".", "\u00b0", "."],
        "heat_shimmer": ["~", "~", "^", "~"],
        "moonlight": ["*", ".", "*", "."],
        "golden_sparkles": ["*", "+", "*", "."],
        "sparkles": ["*", "+", "*", ".", "+"],
        # Rare/magical
        "rainbow": ["*", "*", "*", "*", "*"],
        "aurora": ["|", "/", "\\", "|", "~"],
        "meteors": ["\\", "/", "*", "."],
    }

    _DENSITY: Dict[str, float] = {
        "drizzle": 0.08, "rain": 0.20, "rainy": 0.20, "heavy_rain": 0.30,
        "spring_rain": 0.15, "storm": 0.25, "stormy": 0.25,
        "thunderstorm": 0.28, "summer_storm": 0.30,
        "light_snow": 0.06, "snow": 0.12, "snowy": 0.12,
        "heavy_snow": 0.20, "flurries": 0.08, "blizzard": 0.35,
        "sleet": 0.18, "hail": 0.15, "ice_storm": 0.22,
        "fog": 0.15, "foggy": 0.15, "mist": 0.08,
        "wind": 0.10, "windy": 0.10, "gentle_wind": 0.05, "autumn_wind": 0.12,
        "falling_leaves": 0.08, "leaf_storm": 0.18,
        "pollen": 0.06, "heat_shimmer": 0.04, "moonlight": 0.03,
        "golden_sparkles": 0.05, "sparkles": 0.06,
        "rainbow": 0.08, "aurora": 0.10, "meteors": 0.02,
    }

    _SPEED: Dict[str, float] = {
        "drizzle": 1.2, "rain": 2.0, "rainy": 2.0, "heavy_rain": 2.5,
        "spring_rain": 1.5, "storm": 2.5, "stormy": 2.5,
        "thunderstorm": 2.8, "summer_storm": 3.0,
        "light_snow": 0.3, "snow": 0.4, "snowy": 0.4,
        "heavy_snow": 0.5, "flurries": 0.35, "blizzard": 0.8,
        "sleet": 1.8, "hail": 2.2, "ice_storm": 2.0,
        "fog": 0.15, "foggy": 0.15, "mist": 0.1,
        "wind": 1.5, "windy": 1.5, "gentle_wind": 0.8, "autumn_wind": 1.2,
        "falling_leaves": 0.6, "leaf_storm": 1.0,
        "pollen": 0.2, "heat_shimmer": -0.3,
        "moonlight": 0.4, "golden_sparkles": 0.3, "sparkles": 0.4,
        "rainbow": 0.5, "aurora": 0.2, "meteors": 3.5,
    }

    # Default RGB colours per weather category
    _COLORS: Dict[str, Tuple[int, int, int]] = {
        "drizzle": (100, 180, 255), "rain": (100, 180, 255),
        "rainy": (100, 180, 255), "heavy_rain": (80, 150, 220),
        "spring_rain": (120, 190, 255), "storm": (80, 150, 220),
        "stormy": (80, 150, 220), "thunderstorm": (80, 150, 220),
        "summer_storm": (80, 150, 220),
        "light_snow": (240, 240, 255), "snow": (240, 240, 255),
        "snowy": (240, 240, 255), "heavy_snow": (240, 240, 255),
        "flurries": (240, 240, 255), "blizzard": (240, 240, 255),
        "sleet": (200, 220, 240), "hail": (220, 220, 230),
        "ice_storm": (200, 220, 240),
        "fog": (200, 200, 210), "foggy": (200, 200, 210),
        "mist": (210, 210, 220),
        "wind": (180, 200, 180), "windy": (180, 200, 180),
        "gentle_wind": (200, 210, 200), "autumn_wind": (200, 150, 80),
        "falling_leaves": (200, 120, 40), "leaf_storm": (200, 120, 40),
        "pollen": (220, 210, 100), "heat_shimmer": (255, 200, 100),
        "moonlight": (200, 200, 240), "golden_sparkles": (255, 230, 100),
        "sparkles": (255, 255, 200),
        "rainbow": (255, 200, 200), "aurora": (100, 255, 200),
        "meteors": (255, 255, 200),
    }

    @classmethod
    def get_config(cls, weather_type: str, intensity: float = 1.0) -> List[ParticleConfig]:
        """Return particle configs for the given weather type.

        Args:
            weather_type: Weather particle type string (e.g. ``"rainy"``).
            intensity: Weather intensity (0.0 -- 1.0), currently stored but
                       not used to modify density (matches original behaviour).
        """
        chars = cls._CHARS.get(weather_type)
        if not chars:
            return []

        density = cls._DENSITY.get(weather_type, 0.0)
        speed = cls._SPEED.get(weather_type, 1.0)
        rgb = cls._COLORS.get(weather_type, (200, 200, 200))

        direction = ParticleDirection.FALL
        if speed < 0:
            direction = ParticleDirection.FLOAT_UP
            speed = abs(speed)

        return [ParticleConfig(
            chars=chars,
            color_rgb=rgb,
            direction=direction,
            speed=speed,
            density=density,
        )]

    # Convenience methods for specific weather categories

    @classmethod
    def get_rain_config(cls, intensity: float = 1.0) -> List[ParticleConfig]:
        """Return configs for rain at given intensity."""
        if intensity > 0.7:
            return cls.get_config("heavy_rain", intensity)
        elif intensity > 0.3:
            return cls.get_config("rainy", intensity)
        else:
            return cls.get_config("drizzle", intensity)

    @classmethod
    def get_snow_config(cls, intensity: float = 1.0) -> List[ParticleConfig]:
        """Return configs for snow at given intensity."""
        if intensity > 0.7:
            return cls.get_config("heavy_snow", intensity)
        elif intensity > 0.3:
            return cls.get_config("snowy", intensity)
        else:
            return cls.get_config("light_snow", intensity)

    @classmethod
    def get_leaves_config(cls, season: str = "fall") -> List[ParticleConfig]:
        """Return configs for falling leaves."""
        if season == "fall":
            return cls.get_config("falling_leaves")
        return []

    @classmethod
    def get_mist_config(cls) -> List[ParticleConfig]:
        """Return configs for mist particles."""
        return cls.get_config("mist")

    @classmethod
    def get_sandstorm_config(cls, intensity: float = 1.0) -> List[ParticleConfig]:
        """Return configs for sandstorm-like wind with sand particles."""
        return [ParticleConfig(
            chars=[".", ",", "\u00b7", "'"],
            color_rgb=(210, 195, 150),
            direction=ParticleDirection.DRIFT_RIGHT,
            speed=1.5 * intensity,
            density=0.15 * intensity,
        )]


# ── BiomeParticles config factory ─────────────────────────────────────────────

class BiomeParticles:
    """Static factory returning :class:`ParticleConfig` lists from biome data.

    Data is ported from ``BIOME_AMBIENT_PARTICLES`` in ``ui/biome_visuals.py``.
    """

    # Direction string -> enum mapping
    _DIR_MAP: Dict[str, ParticleDirection] = {
        "fall": ParticleDirection.FALL,
        "float": ParticleDirection.FLOAT_UP,
        "drift_right": ParticleDirection.DRIFT_RIGHT,
        "drift_left": ParticleDirection.DRIFT_LEFT,
        "static": ParticleDirection.STATIC,
        "swirl": ParticleDirection.SWIRL,
    }

    # Complete biome ambient data (ported from biome_visuals.BIOME_AMBIENT_PARTICLES)
    _DATA: Dict[str, List[dict]] = {
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

    @classmethod
    def get_config(cls, biome: str) -> List[ParticleConfig]:
        """Return all ambient particle configs for *biome* (unfiltered by time/season).

        Time and season filtering is handled by
        :meth:`ParticleSystem.configure_biome`.
        """
        raw = cls._DATA.get(biome, [])
        configs: List[ParticleConfig] = []
        for entry in raw:
            direction = cls._DIR_MAP.get(entry["direction"], ParticleDirection.FALL)
            configs.append(ParticleConfig(
                chars=entry["chars"],
                color_rgb=entry["color_rgb"],
                direction=direction,
                speed=entry["speed"],
                density=entry["density"],
                time_filter=entry.get("time"),
                season_filter=entry.get("season"),
            ))
        return configs
