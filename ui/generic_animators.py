"""
Generic, reusable event animators for Cheese the Duck.

These configurable animator classes can be parameterized to cover hundreds
of different events without writing unique code for each one. They rely on
the EventAnimator base class and EventAnimationState enum provided by
ui.event_animations.

Rendering modes:
  - Sprite-based: get_sprite() -> List[str], get_position() -> (x, y)
  - Particle-based: get_particles() -> List[(x, y, char)]
"""

import random
import math
import time
from typing import List, Tuple, Dict, Optional

from ui.event_animations import EventAnimator, EventAnimationState


# ---------------------------------------------------------------------------
# 1. GenericParticleAnimator
# ---------------------------------------------------------------------------

class GenericParticleAnimator(EventAnimator):
    """
    Particle-based animator that spawns configurable ASCII particles across
    the screen.  Perfect for weather, ambiance, and environmental effects.
    """

    def __init__(
        self,
        event_id: str,
        playfield_width: int = 60,
        playfield_height: int = 15,
        particles: str = ".*+~",
        color: str = "white",
        density: int = 8,
        fall_speed: float = 0.3,
        drift_speed: float = 0.1,
        duration: float = 6.0,
        spread: str = "full",
    ):
        super().__init__(
            event_id=event_id,
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            duration=duration,
        )
        self.particle_chars = list(particles)
        self._color = color
        self.density = density
        self.fall_speed = fall_speed
        self.drift_speed = drift_speed
        self.spread = spread

        # Active particle list: dicts with x, y, char, age
        self._particles: List[Dict] = []

    # -- helpers ----------------------------------------------------------

    def _random_spawn_pos(self) -> Tuple[float, float]:
        """Return a random (x, y) based on the spread mode."""
        x = random.uniform(0, self.playfield_width - 1)
        if self.spread == "top":
            y = random.uniform(0, self.playfield_height * 0.4)
        elif self.spread == "bottom":
            y = random.uniform(self.playfield_height * 0.6, self.playfield_height - 1)
        elif self.spread == "center":
            cx = self.playfield_width / 2
            cy = self.playfield_height / 2
            x = cx + random.uniform(-self.playfield_width * 0.25, self.playfield_width * 0.25)
            y = cy + random.uniform(-self.playfield_height * 0.25, self.playfield_height * 0.25)
        else:  # "full"
            y = random.uniform(0, self.playfield_height - 1)
        return (x, y)

    def _spawn_particle(self) -> Dict:
        x, y = self._random_spawn_pos()
        return {
            "x": x,
            "y": y,
            "char": random.choice(self.particle_chars),
            "age": 0.0,
        }

    def _move_particle(self, p: Dict, dt: float) -> None:
        p["y"] += self.fall_speed
        p["x"] += self.drift_speed + random.uniform(-0.15, 0.15)
        p["age"] += dt

    def _in_bounds(self, p: Dict) -> bool:
        return (
            -1 <= p["x"] <= self.playfield_width
            and -1 <= p["y"] <= self.playfield_height
        )

    def _respawn(self, p: Dict) -> None:
        """Wrap / respawn a particle that left the screen."""
        x, y = self._random_spawn_pos()
        p["x"] = x
        # Reset to an edge appropriate for the fall direction
        if self.fall_speed >= 0:
            p["y"] = random.uniform(-1, 0)
        else:
            p["y"] = random.uniform(self.playfield_height - 1, self.playfield_height)
        p["char"] = random.choice(self.particle_chars)
        p["age"] = 0.0

    # -- overrides --------------------------------------------------------

    def start(self):
        self.state = EventAnimationState.ARRIVING
        self.start_time = time.time()
        self.state_start_time = time.time()
        self._particles = []

    def update(self, duck_x: int = 30, duck_y: int = 8) -> bool:
        if self.state == EventAnimationState.FINISHED:
            return False

        now = time.time()
        dt = 0.1  # nominal tick
        elapsed = now - self.start_time

        # --- state transitions ---
        arrive_dur = min(1.0, self.total_duration * 0.15)
        leave_start = self.total_duration - min(1.5, self.total_duration * 0.2)

        if self.state == EventAnimationState.ARRIVING:
            # Gradually add particles
            target = int(self.density * min(1.0, (elapsed / arrive_dur)))
            while len(self._particles) < target:
                self._particles.append(self._spawn_particle())
            if elapsed >= arrive_dur:
                self.state = EventAnimationState.INTERACTING
                self.state_start_time = now

        elif self.state == EventAnimationState.INTERACTING:
            # Maintain particle count
            while len(self._particles) < self.density:
                self._particles.append(self._spawn_particle())
            if elapsed >= leave_start:
                self.state = EventAnimationState.LEAVING
                self.state_start_time = now

        elif self.state == EventAnimationState.LEAVING:
            # Fade out — stop spawning, let existing ones leave
            if not self._particles or elapsed >= self.total_duration + 2.0:
                self.state = EventAnimationState.FINISHED
                self._particles = []
                return False

        # --- move existing particles ---
        survivors: List[Dict] = []
        for p in self._particles:
            self._move_particle(p, dt)
            if self._in_bounds(p):
                survivors.append(p)
            elif self.state == EventAnimationState.INTERACTING:
                self._respawn(p)
                survivors.append(p)
            # else: particle drifts away during LEAVING
        self._particles = survivors

        return True

    def get_particles(self) -> List[Tuple[int, int, str]]:
        return [(int(p["x"]), int(p["y"]), p["char"]) for p in self._particles]

    def get_sprite(self) -> List[str]:
        return []

    def get_color(self) -> str:
        return self._color


# ---------------------------------------------------------------------------
# 2. GenericSpriteAnimator
# ---------------------------------------------------------------------------

class GenericSpriteAnimator(EventAnimator):
    """
    Sprite-based animator where you pass in sprites directly.
    Good for specific objects and creatures.
    """

    def __init__(
        self,
        event_id: str,
        playfield_width: int = 60,
        playfield_height: int = 15,
        sprites: Optional[Dict[str, List[str]]] = None,
        color: str = "white",
        duration: float = 6.0,
        enter_from: str = "right",
        interaction_behavior: str = "hover",
        frame_speed: float = 0.3,
    ):
        # Determine start position from entry direction
        direction = enter_from
        if direction == "random":
            direction = random.choice(["right", "left", "top", "bottom"])
        self._enter_dir = direction

        start_x, start_y = self._edge_position(
            direction, playfield_width, playfield_height, entering=True
        )

        super().__init__(
            event_id=event_id,
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=start_x,
            start_y=start_y,
            duration=duration,
        )

        self.sprites = sprites or {"frame_1": ["?"]}
        self._sprite_keys = sorted(self.sprites.keys())
        self._color = color
        self.interaction_behavior = interaction_behavior
        self.frame_duration = frame_speed
        self.speed = 0.4
        self._orbit_angle = 0.0
        self._hover_base_y = float(playfield_height // 2)

    @staticmethod
    def _edge_position(
        direction: str, pw: int, ph: int, entering: bool
    ) -> Tuple[float, float]:
        margin = 6
        if entering:
            if direction == "right":
                return (float(pw + margin), float(ph // 2))
            elif direction == "left":
                return (float(-margin), float(ph // 2))
            elif direction == "top":
                return (float(pw // 2), float(-margin))
            else:  # bottom
                return (float(pw // 2), float(ph + margin))
        else:
            # Leave in opposite direction
            if direction == "right":
                return (float(-margin), float(ph // 2))
            elif direction == "left":
                return (float(pw + margin), float(ph // 2))
            elif direction == "top":
                return (float(pw // 2), float(ph + margin))
            else:
                return (float(pw // 2), float(-margin))

    def _setup_arrival_path(self):
        mid_x = self.playfield_width / 2
        mid_y = self.playfield_height / 2
        self.path_points = [(self.x, self.y), (mid_x, mid_y)]
        self.path_index = 0

    def _setup_interaction(self):
        super()._setup_interaction()
        self._hover_base_y = self.y
        self._orbit_angle = 0.0

    def _setup_leaving_path(self):
        ex, ey = self._edge_position(
            self._enter_dir, self.playfield_width, self.playfield_height,
            entering=False,
        )
        self.path_points = [(self.x, self.y), (ex, ey)]
        self.path_index = 0

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        interact_dur = max(1.0, self.total_duration - 3.0)

        if self.interaction_behavior == "hover":
            self.y = self._hover_base_y + math.sin(elapsed * 2.0) * 1.5
        elif self.interaction_behavior == "orbit":
            self._orbit_angle += 0.12
            radius = 8 + math.sin(elapsed * 1.5) * 2
            self.x = duck_x + math.cos(self._orbit_angle) * radius
            self.y = duck_y + math.sin(self._orbit_angle) * radius * 0.5
            self.x = max(0, min(self.playfield_width - 5, self.x))
            self.y = max(1, min(self.playfield_height - 2, self.y))
        # "static": no movement — just animate frames

        if elapsed >= interact_dur:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    def _update_sprite_frame(self):
        self.frame_index = (self.frame_index + 1) % max(1, len(self._sprite_keys))
        self.current_sprite_key = self._sprite_keys[self.frame_index]

    def get_sprite(self) -> List[str]:
        return self.sprites.get(self.current_sprite_key, next(iter(self.sprites.values())))

    def get_color(self) -> str:
        return self._color


# ---------------------------------------------------------------------------
# 3. GenericDuckReactionAnimator
# ---------------------------------------------------------------------------

class GenericDuckReactionAnimator(EventAnimator):
    """
    Shows a reaction / emote above or near the duck.
    For internal events (thoughts, emotions, body reactions, self-awareness).
    """

    def __init__(
        self,
        event_id: str,
        playfield_width: int = 60,
        playfield_height: int = 15,
        emote: str = "!",
        color: str = "yellow",
        duration: float = 4.0,
        style: str = "pop",
    ):
        super().__init__(
            event_id=event_id,
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            duration=duration,
        )
        self.emote = emote
        self._color = color
        self.style = style

        # Build emote bubble frames (small → large → small for "pop")
        self._frames = self._build_frames(emote)
        self._duck_x = float(playfield_width // 2)
        self._duck_y = float(playfield_height // 2)
        self._base_y = self._duck_y - 3
        self._shake_offset = 0.0
        self._bounce_vel = -1.2  # initial upward velocity for bounce

    @staticmethod
    def _build_frames(emote: str) -> Dict[str, List[str]]:
        """Build bubble frames that adapt to emote length."""
        elen = len(emote)
        if elen <= 1:
            inner = f" {emote} "
            width = 5
        elif elen <= 3:
            inner = f" {emote} "
            width = elen + 4
        else:
            inner = f" {emote} "
            width = elen + 4

        top = "╭" + "─" * (width - 2) + "╮"
        mid = "│" + inner.center(width - 2) + "│"
        bot_half = (width - 2) // 2
        bot = "╰" + "─" * bot_half + "┬" + "─" * (width - 3 - bot_half) + "╯"

        full = [top, mid, bot]
        small = [f"({emote})"]
        tiny = [emote]
        return {"tiny": tiny, "small": small, "full": full}

    def start(self):
        self.state = EventAnimationState.INTERACTING
        self.start_time = time.time()
        self.state_start_time = time.time()

    def update(self, duck_x: int = 30, duck_y: int = 8) -> bool:
        if self.state == EventAnimationState.FINISHED:
            return False

        self._duck_x = float(duck_x)
        self._duck_y = float(duck_y)
        self._base_y = self._duck_y - 3

        elapsed = time.time() - self.start_time

        if elapsed >= self.total_duration:
            self.state = EventAnimationState.FINISHED
            return False

        # Style-specific position updates
        if self.style == "float":
            # Float upward over time
            self.x = self._duck_x
            self.y = self._base_y - elapsed * 0.6
        elif self.style == "shake":
            self.x = self._duck_x + random.choice([-1, 0, 1])
            self.y = self._base_y
        elif self.style == "bounce":
            # Damped spring
            t = elapsed
            amp = max(0, 2.0 - t * 0.5)
            self.y = self._base_y + math.sin(t * 5) * amp
            self.x = self._duck_x
        else:  # "pop"
            self.x = self._duck_x
            self.y = self._base_y

        return True

    def _current_frame_key(self) -> str:
        elapsed = time.time() - self.start_time
        frac = elapsed / self.total_duration if self.total_duration > 0 else 1.0

        if self.style == "pop":
            if frac < 0.15:
                return "tiny"
            elif frac < 0.3:
                return "small"
            elif frac < 0.8:
                return "full"
            elif frac < 0.9:
                return "small"
            else:
                return "tiny"
        elif self.style == "float":
            if frac < 0.7:
                return "full"
            elif frac < 0.85:
                return "small"
            else:
                return "tiny"
        else:
            return "full"

    def get_sprite(self) -> List[str]:
        key = self._current_frame_key()
        return self._frames.get(key, self._frames["full"])

    def get_position(self) -> Tuple[int, int]:
        return (int(self.x), int(self.y))

    def get_color(self) -> str:
        return self._color


# ---------------------------------------------------------------------------
# 4. GenericAmbientAnimator
# ---------------------------------------------------------------------------

class GenericAmbientAnimator(EventAnimator):
    """
    Particle-based ambient effect that creates atmosphere without a central
    sprite.  Ideal for sound-events, temperature changes, moods.
    """

    def __init__(
        self,
        event_id: str,
        playfield_width: int = 60,
        playfield_height: int = 15,
        pattern: str = "sparkle",
        chars: str = "·✧*˚",
        color: str = "cyan",
        duration: float = 5.0,
        intensity: int = 6,
    ):
        super().__init__(
            event_id=event_id,
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            duration=duration,
        )
        self.pattern = pattern
        self.char_list = list(chars)
        self._color = color
        self.intensity = intensity

        # Each particle: {x, y, char, born, lifetime, vx, vy}
        self._particles: List[Dict] = []
        self._center_x = playfield_width / 2.0
        self._center_y = playfield_height / 2.0

    def _make_particle(self, x: float, y: float, vx: float = 0.0, vy: float = 0.0) -> Dict:
        return {
            "x": x, "y": y,
            "char": random.choice(self.char_list),
            "born": time.time(),
            "lifetime": random.uniform(0.3, 0.8),
            "vx": vx, "vy": vy,
        }

    # -- spawners for each pattern ----------------------------------------

    def _spawn_sparkle(self) -> Dict:
        return self._make_particle(
            random.uniform(0, self.playfield_width - 1),
            random.uniform(0, self.playfield_height - 1),
        )

    def _spawn_wave(self, elapsed: float) -> Dict:
        """Horizontal line expanding from center."""
        offset = elapsed * 4.0  # expansion speed
        side = random.choice([-1, 1])
        x = self._center_x + side * offset + random.uniform(-1, 1)
        y = self._center_y + random.uniform(-0.5, 0.5)
        return self._make_particle(x, y)

    def _spawn_pulse(self, elapsed: float) -> Dict:
        """Expanding ring from center."""
        radius = elapsed * 3.0
        angle = random.uniform(0, 2 * math.pi)
        x = self._center_x + math.cos(angle) * radius
        y = self._center_y + math.sin(angle) * radius * 0.5
        return self._make_particle(x, y)

    def _spawn_scatter(self) -> Dict:
        """Burst outward from center, decelerating."""
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.5, 2.0)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed * 0.5
        return self._make_particle(self._center_x, self._center_y, vx, vy)

    # -- overrides --------------------------------------------------------

    def start(self):
        self.state = EventAnimationState.INTERACTING
        self.start_time = time.time()
        self.state_start_time = time.time()
        self._particles = []

    def update(self, duck_x: int = 30, duck_y: int = 8) -> bool:
        if self.state == EventAnimationState.FINISHED:
            return False

        now = time.time()
        elapsed = now - self.start_time

        if elapsed >= self.total_duration:
            self.state = EventAnimationState.FINISHED
            self._particles = []
            return False

        # Remove expired particles
        self._particles = [
            p for p in self._particles if (now - p["born"]) < p["lifetime"]
        ]

        # Move particles with velocity (scatter mostly)
        for p in self._particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            # Decelerate scatter particles
            p["vx"] *= 0.92
            p["vy"] *= 0.92

        # Spawn new particles to maintain intensity
        state_elapsed = now - self.state_start_time
        while len(self._particles) < self.intensity:
            if self.pattern == "sparkle":
                self._particles.append(self._spawn_sparkle())
            elif self.pattern == "wave":
                self._particles.append(self._spawn_wave(state_elapsed))
            elif self.pattern == "pulse":
                self._particles.append(self._spawn_pulse(state_elapsed))
            elif self.pattern == "scatter":
                self._particles.append(self._spawn_scatter())
            else:
                self._particles.append(self._spawn_sparkle())

        return True

    def get_particles(self) -> List[Tuple[int, int, str]]:
        return [
            (int(p["x"]), int(p["y"]), p["char"])
            for p in self._particles
            if 0 <= p["x"] < self.playfield_width and 0 <= p["y"] < self.playfield_height
        ]

    def get_sprite(self) -> List[str]:
        return []

    def get_color(self) -> str:
        return self._color


# ---------------------------------------------------------------------------
# 5. GenericWeatherAnimator
# ---------------------------------------------------------------------------

class GenericWeatherAnimator(EventAnimator):
    """
    Particle-based animator specifically for weather events.
    Supports rain, snow, wind, fog, sun, hail, and mist.
    """

    _PRESETS = {
        "rain":  {"chars": "|,",  "fall": 1.0,  "drift": 0.0,  "density_mult": 1.0},
        "snow":  {"chars": "*.·", "fall": 0.25, "drift": 0.15, "density_mult": 0.8},
        "wind":  {"chars": "~-",  "fall": 0.0,  "drift": 1.2,  "density_mult": 0.7},
        "fog":   {"chars": "░▒",  "fall": 0.0,  "drift": 0.05, "density_mult": 0.4},
        "sun":   {"chars": "*.·", "fall": 0.3,  "drift": 0.05, "density_mult": 0.6},
        "hail":  {"chars": "o°",  "fall": 1.2,  "drift": 0.0,  "density_mult": 1.0},
        "mist":  {"chars": ".'",  "fall": 0.0,  "drift": 0.04, "density_mult": 0.5},
    }

    def __init__(
        self,
        event_id: str,
        playfield_width: int = 60,
        playfield_height: int = 15,
        weather_type: str = "rain",
        color: str = "cyan",
        intensity: int = 12,
        duration: float = 6.0,
    ):
        super().__init__(
            event_id=event_id,
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            duration=duration,
        )
        self.weather_type = weather_type
        self._color = color
        self.intensity = intensity

        preset = self._PRESETS.get(weather_type, self._PRESETS["rain"])
        self._chars = list(preset["chars"])
        self._fall_speed = preset["fall"]
        self._drift_speed = preset["drift"]
        self._density = max(1, int(intensity * preset["density_mult"]))

        self._particles: List[Dict] = []

    # -- spawn helpers ----------------------------------------------------

    def _spawn(self) -> Dict:
        wt = self.weather_type
        pw, ph = self.playfield_width, self.playfield_height

        if wt == "rain" or wt == "hail":
            x = random.uniform(0, pw - 1)
            y = random.uniform(-2, 0)
        elif wt == "snow":
            x = random.uniform(0, pw - 1)
            y = random.uniform(-2, 0)
        elif wt == "wind":
            x = random.uniform(pw, pw + 5)
            y = random.uniform(0, ph - 1)
        elif wt == "fog":
            x = random.uniform(0, pw - 1)
            y = random.uniform(ph * 0.4, ph - 1)
        elif wt == "sun":
            # Emanate from top-center
            cx = pw / 2
            x = cx + random.uniform(-4, 4)
            y = random.uniform(-1, 1)
        elif wt == "mist":
            x = random.uniform(0, pw - 1)
            y = random.uniform(ph * 0.5, ph - 1)
        else:
            x = random.uniform(0, pw - 1)
            y = random.uniform(-2, 0)

        return {
            "x": x, "y": y,
            "char": random.choice(self._chars),
            "age": 0.0,
            "vy": self._fall_speed + random.uniform(-0.05, 0.05),
            "vx": self._drift_speed + random.uniform(-0.03, 0.03),
        }

    def _in_bounds(self, p: Dict) -> bool:
        return -2 <= p["x"] <= self.playfield_width + 2 and -2 <= p["y"] <= self.playfield_height + 2

    # -- overrides --------------------------------------------------------

    def start(self):
        self.state = EventAnimationState.ARRIVING
        self.start_time = time.time()
        self.state_start_time = time.time()
        self._particles = []

    def update(self, duck_x: int = 30, duck_y: int = 8) -> bool:
        if self.state == EventAnimationState.FINISHED:
            return False

        now = time.time()
        elapsed = now - self.start_time
        arrive_dur = min(1.0, self.total_duration * 0.15)
        leave_start = self.total_duration - min(1.5, self.total_duration * 0.2)

        # State transitions
        if self.state == EventAnimationState.ARRIVING:
            target_count = int(self._density * min(1.0, elapsed / arrive_dur))
            while len(self._particles) < target_count:
                self._particles.append(self._spawn())
            if elapsed >= arrive_dur:
                self.state = EventAnimationState.INTERACTING
                self.state_start_time = now

        elif self.state == EventAnimationState.INTERACTING:
            while len(self._particles) < self._density:
                self._particles.append(self._spawn())
            if elapsed >= leave_start:
                self.state = EventAnimationState.LEAVING
                self.state_start_time = now

        elif self.state == EventAnimationState.LEAVING:
            if not self._particles or elapsed >= self.total_duration + 2.0:
                self.state = EventAnimationState.FINISHED
                self._particles = []
                return False

        # Move particles
        survivors: List[Dict] = []
        for p in self._particles:
            p["y"] += p["vy"]
            p["x"] -= p["vx"]  # wind / drift moves left
            p["age"] += 0.1

            # Hail: bounce near bottom
            if self.weather_type == "hail" and p["y"] >= self.playfield_height - 1:
                p["vy"] = -abs(p["vy"]) * 0.4
                p["y"] = self.playfield_height - 1.0

            if self._in_bounds(p):
                survivors.append(p)
            elif self.state == EventAnimationState.INTERACTING:
                survivors.append(self._spawn())
        self._particles = survivors

        return True

    def get_particles(self) -> List[Tuple[int, int, str]]:
        return [
            (int(p["x"]), int(p["y"]), p["char"])
            for p in self._particles
            if 0 <= int(p["x"]) < self.playfield_width and 0 <= int(p["y"]) < self.playfield_height
        ]

    def get_sprite(self) -> List[str]:
        return []

    def get_color(self) -> str:
        return self._color


# ---------------------------------------------------------------------------
# 6. GenericCreatureAnimator
# ---------------------------------------------------------------------------

class GenericCreatureAnimator(EventAnimator):
    """
    Sprite-based animator for animal/creature events.
    A simple creature walks or flies in and out.
    """

    _CREATURE_DATA = {
        "small": {
            "frames": {
                "frame_1": ["\\o/"],
                "frame_2": ["-o-"],
            },
            "enter": "side",
            "speed": 0.5,
            "y_zone": "middle",
        },
        "medium": {
            "frames": {
                "frame_1": [" _  ", "(o )"],
                "frame_2": [" _  ", "( o)"],
            },
            "enter": "side",
            "speed": 0.35,
            "y_zone": "bottom",
        },
        "large": {
            "frames": {
                "frame_1": ["  /\\  ", " /  \\ ", "/____\\"],
                "frame_2": ["  /\\  ", " /  \\ ", "\\____/"],
            },
            "enter": "side",
            "speed": 0.25,
            "y_zone": "bottom",
        },
        "flying": {
            "frames": {
                "frame_1": [" \\  ", "  >->"],
                "frame_2": [" /  ", "  >->"],
            },
            "enter": "top_side",
            "speed": 0.5,
            "y_zone": "top",
        },
        "swimming": {
            "frames": {
                "frame_1": ["><>"],
                "frame_2": ["><>>"],
            },
            "enter": "side",
            "speed": 0.3,
            "y_zone": "very_bottom",
        },
    }

    def __init__(
        self,
        event_id: str,
        playfield_width: int = 60,
        playfield_height: int = 15,
        creature_type: str = "small",
        color: str = "green",
        duration: float = 6.0,
    ):
        data = self._CREATURE_DATA.get(creature_type, self._CREATURE_DATA["small"])
        self._creature_type = creature_type
        self._frames_dict = data["frames"]
        self._sprite_keys = sorted(self._frames_dict.keys())
        self._enter_mode = data["enter"]
        self._y_zone = data["y_zone"]

        # Determine start Y based on zone
        if self._y_zone == "top":
            start_y = random.uniform(1, playfield_height * 0.3)
        elif self._y_zone == "bottom":
            start_y = random.uniform(playfield_height * 0.6, playfield_height - 2)
        elif self._y_zone == "very_bottom":
            start_y = float(playfield_height - 2)
        else:
            start_y = random.uniform(playfield_height * 0.3, playfield_height * 0.7)

        # Enter from right by default
        enter_left = random.random() < 0.5
        start_x = float(-6) if enter_left else float(playfield_width + 6)
        self._from_left = enter_left

        if self._enter_mode == "top_side":
            start_y = random.uniform(-3, 2)

        super().__init__(
            event_id=event_id,
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=start_x,
            start_y=start_y,
            duration=duration,
        )
        self.speed = data["speed"]
        self._color = color
        self._interact_start_y = start_y

    def _setup_arrival_path(self):
        mid_x = self.playfield_width / 2 + random.uniform(-8, 8)
        if self._y_zone == "top":
            mid_y = random.uniform(2, self.playfield_height * 0.35)
        elif self._y_zone in ("bottom", "very_bottom"):
            mid_y = self._interact_start_y
        else:
            mid_y = self.playfield_height / 2

        self.path_points = [(self.x, self.y), (mid_x, mid_y)]
        self.path_index = 0
        self._interact_start_y = mid_y

    def _setup_interaction(self):
        super()._setup_interaction()

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        interact_dur = max(1.0, self.total_duration - 3.0)

        # Medium creatures: gentle hop
        if self._creature_type == "medium":
            self.y = self._interact_start_y + math.sin(elapsed * 3) * 0.8

        if elapsed >= interact_dur:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    def _setup_leaving_path(self):
        exit_x = float(-8) if not self._from_left else float(self.playfield_width + 8)
        exit_y = self.y
        if self._enter_mode == "top_side":
            exit_y = random.uniform(-3, 2)
        self.path_points = [(self.x, self.y), (exit_x, exit_y)]
        self.path_index = 0

    def _update_sprite_frame(self):
        self.frame_index = (self.frame_index + 1) % max(1, len(self._sprite_keys))
        self.current_sprite_key = self._sprite_keys[self.frame_index]

    def get_sprite(self) -> List[str]:
        return self._frames_dict.get(
            self.current_sprite_key, next(iter(self._frames_dict.values()))
        )

    def get_color(self) -> str:
        return self._color


# ---------------------------------------------------------------------------
# 7. GenericFoodAnimator
# ---------------------------------------------------------------------------

class GenericFoodAnimator(EventAnimator):
    """
    Sprite-based animator for food discovery/encounter events.
    Shows a food item appearing via drop, discovery, or throw.
    """

    def __init__(
        self,
        event_id: str,
        playfield_width: int = 60,
        playfield_height: int = 15,
        food_char: str = "[=]",
        color: str = "yellow",
        duration: float = 5.0,
        appear_style: str = "drop",
    ):
        self.appear_style = appear_style
        self._food_char = food_char
        self._color = color
        self._ground_y = float(playfield_height - 3)
        self._sparkle_particles: List[Dict] = []
        self._bounce_vel = 0.0
        self._landed = False

        # Start position depends on style
        cx = float(playfield_width // 2 + random.randint(-6, 6))
        if appear_style == "drop":
            start_x, start_y = cx, -2.0
        elif appear_style == "throw":
            start_x = float(-5)
            start_y = float(playfield_height // 2)
        else:  # "discover"
            start_x = cx
            start_y = self._ground_y

        super().__init__(
            event_id=event_id,
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=start_x,
            start_y=start_y,
            duration=duration,
        )
        self.speed = 0.6
        self._arc_t = 0.0  # parametric time for throw arc

    def start(self):
        self.state = EventAnimationState.ARRIVING
        self.start_time = time.time()
        self.state_start_time = time.time()
        self._landed = False
        self._bounce_vel = 0.0
        self._arc_t = 0.0
        if self.appear_style == "discover":
            # Skip arrival, go straight to interaction with sparkles
            self.state = EventAnimationState.INTERACTING
            self._spawn_discovery_sparkles()

    def _spawn_discovery_sparkles(self):
        for _ in range(6):
            angle = random.uniform(0, 2 * math.pi)
            self._sparkle_particles.append({
                "x": self.x + math.cos(angle) * 2,
                "y": self.y + math.sin(angle) * 1,
                "char": random.choice(["*", "+", ".", "·"]),
                "born": time.time(),
                "lifetime": random.uniform(0.4, 1.0),
            })

    def update(self, duck_x: int = 30, duck_y: int = 8) -> bool:
        if self.state == EventAnimationState.FINISHED:
            return False

        now = time.time()
        elapsed = now - self.start_time

        # Update sparkle particles
        self._sparkle_particles = [
            p for p in self._sparkle_particles if (now - p["born"]) < p["lifetime"]
        ]

        if self.state == EventAnimationState.ARRIVING:
            if self.appear_style == "drop":
                # Fall with gravity + bounce
                self._bounce_vel += 0.15  # gravity
                self.y += self._bounce_vel
                if self.y >= self._ground_y:
                    self.y = self._ground_y
                    if abs(self._bounce_vel) < 0.3:
                        self._landed = True
                    else:
                        self._bounce_vel = -abs(self._bounce_vel) * 0.4
                if self._landed:
                    self.state = EventAnimationState.INTERACTING
                    self.state_start_time = now

            elif self.appear_style == "throw":
                # Parabolic arc toward center
                self._arc_t += 0.04
                t = min(self._arc_t, 1.0)
                target_x = float(self.playfield_width // 2)
                self.x = -5 + (target_x - (-5)) * t
                # Arc: y = start + (ground-start)*t - height*sin(pi*t)
                arc_height = 6.0
                start_y = float(self.playfield_height // 2)
                self.y = start_y + (self._ground_y - start_y) * t - arc_height * math.sin(math.pi * t)
                if t >= 1.0:
                    self.y = self._ground_y
                    self.state = EventAnimationState.INTERACTING
                    self.state_start_time = now

        elif self.state == EventAnimationState.INTERACTING:
            interact_dur = max(1.0, self.total_duration - 2.5)
            if elapsed - (now - self.state_start_time - elapsed + (now - self.start_time)) >= 0:
                state_elapsed = now - self.state_start_time
                if state_elapsed >= interact_dur:
                    self.state = EventAnimationState.LEAVING
                    self.state_start_time = now

        elif self.state == EventAnimationState.LEAVING:
            leave_elapsed = now - self.state_start_time
            if leave_elapsed >= 1.5:
                self.state = EventAnimationState.FINISHED
                return False

        if elapsed >= self.total_duration + 2.0:
            self.state = EventAnimationState.FINISHED
            return False

        return True

    def get_sprite(self) -> List[str]:
        if self.state == EventAnimationState.LEAVING:
            # Fade out: shrink
            leave_frac = (time.time() - self.state_start_time) / 1.5
            if leave_frac > 0.7:
                return ["."]
            elif leave_frac > 0.4:
                return [self._food_char[len(self._food_char) // 2]] if self._food_char else ["."]
        return [self._food_char]

    def get_position(self) -> Tuple[int, int]:
        return (int(self.x), int(self.y))

    def get_color(self) -> str:
        return self._color


# ---------------------------------------------------------------------------
# 8. GenericSkyAnimator
# ---------------------------------------------------------------------------

class GenericSkyAnimator(EventAnimator):
    """
    Particle-based animator for sky/celestial events.
    Supports stars, clouds, aurora, and celestial patterns.
    """

    _PRESETS = {
        "stars":     {"chars": "*.+",    "density": 10, "drift": 0.0,  "zone_top": 0.0, "zone_bot": 0.33},
        "clouds":    {"chars": "~",      "density": 5,  "drift": 0.08, "zone_top": 0.0, "zone_bot": 0.33},
        "aurora":    {"chars": "░║",     "density": 8,  "drift": 0.0,  "zone_top": 0.0, "zone_bot": 0.50},
        "celestial": {"chars": "*.·○",   "density": 7,  "drift": 0.02, "zone_top": 0.0, "zone_bot": 0.25},
    }

    def __init__(
        self,
        event_id: str,
        playfield_width: int = 60,
        playfield_height: int = 15,
        sky_type: str = "stars",
        color: str = "white",
        duration: float = 7.0,
    ):
        super().__init__(
            event_id=event_id,
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            duration=duration,
        )
        self.sky_type = sky_type
        self._color = color

        preset = self._PRESETS.get(sky_type, self._PRESETS["stars"])
        self._chars = list(preset["chars"])
        self._density = preset["density"]
        self._drift = preset["drift"]
        self._zone_top = preset["zone_top"]
        self._zone_bot = preset["zone_bot"]

        self._particles: List[Dict] = []

    def _zone_y_range(self) -> Tuple[float, float]:
        top = self.playfield_height * self._zone_top
        bot = self.playfield_height * self._zone_bot
        return (top, max(top + 1, bot))

    def _spawn(self) -> Dict:
        y_lo, y_hi = self._zone_y_range()
        return {
            "x": random.uniform(0, self.playfield_width - 1),
            "y": random.uniform(y_lo, y_hi),
            "char": random.choice(self._chars),
            "born": time.time(),
            "lifetime": random.uniform(0.5, 1.5),
            "visible": True,
        }

    def start(self):
        self.state = EventAnimationState.ARRIVING
        self.start_time = time.time()
        self.state_start_time = time.time()
        self._particles = []

    def update(self, duck_x: int = 30, duck_y: int = 8) -> bool:
        if self.state == EventAnimationState.FINISHED:
            return False

        now = time.time()
        elapsed = now - self.start_time
        arrive_dur = min(1.5, self.total_duration * 0.15)
        leave_start = self.total_duration - min(2.0, self.total_duration * 0.2)

        # State machine
        if self.state == EventAnimationState.ARRIVING:
            target = int(self._density * min(1.0, elapsed / arrive_dur))
            while len(self._particles) < target:
                self._particles.append(self._spawn())
            if elapsed >= arrive_dur:
                self.state = EventAnimationState.INTERACTING
                self.state_start_time = now

        elif self.state == EventAnimationState.INTERACTING:
            if elapsed >= leave_start:
                self.state = EventAnimationState.LEAVING
                self.state_start_time = now

        elif self.state == EventAnimationState.LEAVING:
            if not self._particles or elapsed >= self.total_duration + 2.0:
                self.state = EventAnimationState.FINISHED
                self._particles = []
                return False

        # Update particles
        survivors: List[Dict] = []
        for p in self._particles:
            age = now - p["born"]

            # Stars: blink on/off randomly
            if self.sky_type == "stars":
                p["visible"] = random.random() > 0.15  # 15% chance to blink off

            # Clouds: drift horizontally
            if self._drift != 0:
                p["x"] += self._drift

            # Aurora: shimmer vertically
            if self.sky_type == "aurora":
                p["y"] += math.sin(now * 3 + p["x"] * 0.5) * 0.2
                p["char"] = random.choice(self._chars)

            # Expire and respawn
            if age >= p["lifetime"]:
                if self.state != EventAnimationState.LEAVING:
                    survivors.append(self._spawn())
                # else: don't respawn — let them fade
            else:
                # Wrap x for drifting
                if p["x"] > self.playfield_width:
                    p["x"] = 0.0
                elif p["x"] < 0:
                    p["x"] = float(self.playfield_width - 1)
                survivors.append(p)

        self._particles = survivors
        return True

    def get_particles(self) -> List[Tuple[int, int, str]]:
        return [
            (int(p["x"]), int(p["y"]), p["char"])
            for p in self._particles
            if p.get("visible", True)
            and 0 <= int(p["x"]) < self.playfield_width
            and 0 <= int(p["y"]) < self.playfield_height
        ]

    def get_sprite(self) -> List[str]:
        return []

    def get_color(self) -> str:
        return self._color
