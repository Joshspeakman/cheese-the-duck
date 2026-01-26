"""
Animation system for duck movements and effects.
"""
import time
import threading
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import random


class AnimationType(Enum):
    """Types of animations."""
    IDLE = "idle"
    WADDLE = "waddle"
    BOUNCE = "bounce"
    FLAP = "flap"
    SHAKE = "shake"
    SLEEP_BREATHE = "sleep_breathe"
    EAT = "eat"
    SPLASH = "splash"
    SPIN = "spin"
    JUMP = "jump"
    TRIP = "trip"
    WIGGLE = "wiggle"
    QUACK = "quack"
    HEART = "heart"
    SPARKLE = "sparkle"
    EXCLAIM = "exclaim"
    QUESTION = "question"
    ANGRY = "angry"
    CRY = "cry"
    ZZZ = "zzz"


@dataclass
class AnimationFrame:
    """A single frame of animation."""
    art: List[str]         # ASCII art lines
    duration: float        # How long to show (seconds)
    offset_x: int = 0      # Horizontal offset
    offset_y: int = 0      # Vertical offset
    effect: Optional[str] = None  # Optional effect text


@dataclass
class Animation:
    """A complete animation sequence."""
    name: str
    frames: List[AnimationFrame]
    loop: bool = False
    on_complete: Optional[Callable] = None


# Effect overlays (can be drawn on top of duck)
EFFECTS = {
    "heart": [
        "  <3   ",
        " <3 <3 ",
        "  <3   ",
    ],
    "hearts": [
        " <3 <3 <3 ",
        "  <3 <3   ",
        "    <3    ",
    ],
    "sparkle": [
        " *  +  * ",
        "  *  *   ",
        " +  *  + ",
    ],
    "exclaim": [
        "  !!!  ",
        "  !!!  ",
        "   !   ",
    ],
    "question": [
        "  ???  ",
        "  ???  ",
        "   ?   ",
    ],
    "angry": [
        " #@$%! ",
        "  >:( ",
    ],
    "zzz": [
        "     z  ",
        "    z Z ",
        "   Z  z ",
    ],
    "music": [
        " ~  ~ ",
        "  ~~  ",
        " ~  ~ ",
    ],
    "sweat": [
        "   '  ",
        "  ' ' ",
    ],
    "happy": [
        " ^-^ ",
    ],
    "sad": [
        " ;-; ",
    ],
    # Item interaction effects
    "splash": [
        " ~ ~ ~ ",
        "~ o ~ o",
        " ~   ~ ",
        "  ~~~  ",
    ],
    "bounce": [
        "  ^  ",
        " ^ ^ ",
        "  ^  ",
    ],
    "play": [
        " * ! * ",
        "  FUN  ",
        " * ! * ",
    ],
    "comfy": [
        " ~ ~ ~ ",
        " zzz.. ",
        " ~ ~ ~ ",
    ],
    "sniff": [
        " ?   ? ",
        "  *~*  ",
        "   ?   ",
    ],
    "admire": [
        " o   o ",
        "  ooo  ",
        " o   o ",
    ],
}


# Particle effects for ambient animation
PARTICLES = {
    "dust": [".", ",", "'"],
    "water": ["~", "o", "*"],
    "sparkle": ["*", "+", "."],
    "leaves": ["~", "^", "v"],
    "crumbs": [".", ",", "o"],
}


class AnimationController:
    """
    Controls and plays animations.
    """

    def __init__(self):
        self._current_animation: Optional[Animation] = None
        self._frame_index = 0
        self._frame_start_time = 0.0
        self._particles: List[Dict] = []
        self._effect_overlay: Optional[str] = None
        self._effect_expire = 0.0
        self._ambient_frame = 0
        self._ambient_time = 0.0

    def play(self, animation: Animation):
        """Start playing an animation."""
        self._current_animation = animation
        self._frame_index = 0
        self._frame_start_time = time.time()

    def play_effect(self, effect_name: str, duration: float = 1.0):
        """Show an effect overlay."""
        if effect_name in EFFECTS:
            self._effect_overlay = effect_name
            self._effect_expire = time.time() + duration

    def update(self) -> Optional[AnimationFrame]:
        """
        Update animation state and return current frame if any.
        """
        current_time = time.time()

        # Update particles
        self._update_particles(current_time)

        # Update ambient animation
        if current_time - self._ambient_time > 0.5:
            self._ambient_frame = (self._ambient_frame + 1) % 4
            self._ambient_time = current_time

        # Clear expired effects
        if self._effect_overlay and current_time > self._effect_expire:
            self._effect_overlay = None

        # No animation playing
        if not self._current_animation:
            return None

        # Get current frame
        frames = self._current_animation.frames
        if not frames:
            return None

        current_frame = frames[self._frame_index]

        # Check if frame duration elapsed
        if current_time - self._frame_start_time >= current_frame.duration:
            self._frame_index += 1
            self._frame_start_time = current_time

            # Animation complete
            if self._frame_index >= len(frames):
                if self._current_animation.loop:
                    self._frame_index = 0
                else:
                    if self._current_animation.on_complete:
                        self._current_animation.on_complete()
                    self._current_animation = None
                    return None

            if self._frame_index < len(frames):
                current_frame = frames[self._frame_index]

        return current_frame

    def spawn_particles(self, particle_type: str, count: int = 5):
        """Spawn ambient particles."""
        chars = PARTICLES.get(particle_type, ["."])
        for _ in range(count):
            self._particles.append({
                "char": random.choice(chars),
                "x": random.randint(-5, 5),
                "y": random.randint(-3, 3),
                "vx": random.uniform(-0.5, 0.5),
                "vy": random.uniform(-0.3, 0.1),
                "life": random.uniform(1.0, 2.0),
                "spawn_time": time.time(),
            })

    def _update_particles(self, current_time: float):
        """Update particle positions and remove expired ones."""
        alive = []
        for p in self._particles:
            age = current_time - p["spawn_time"]
            if age < p["life"]:
                p["x"] += p["vx"]
                p["y"] += p["vy"]
                alive.append(p)
        self._particles = alive

    def get_particles(self) -> List[Dict]:
        """Get current particles."""
        return self._particles.copy()

    def get_effect_overlay(self) -> Optional[List[str]]:
        """Get current effect overlay if any."""
        if self._effect_overlay:
            return EFFECTS.get(self._effect_overlay)
        return None

    def get_ambient_offset(self) -> tuple:
        """Get ambient animation offset for subtle movement."""
        # Subtle breathing/idle motion
        offsets = [(0, 0), (0, 0), (0, -1), (0, 0)]
        return offsets[self._ambient_frame]

    def is_animating(self) -> bool:
        """Check if an animation is playing."""
        return self._current_animation is not None

    def stop(self):
        """Stop current animation."""
        self._current_animation = None


def create_waddle_animation(duck_art: List[str]) -> Animation:
    """Create a waddle animation from base duck art."""
    # Create frames with slight horizontal offset
    frames = [
        AnimationFrame(duck_art, 0.15, offset_x=-1),
        AnimationFrame(duck_art, 0.15, offset_x=0),
        AnimationFrame(duck_art, 0.15, offset_x=1),
        AnimationFrame(duck_art, 0.15, offset_x=0),
    ]
    return Animation("waddle", frames, loop=True)


def create_bounce_animation(duck_art: List[str]) -> Animation:
    """Create a bouncing animation."""
    frames = [
        AnimationFrame(duck_art, 0.1, offset_y=0),
        AnimationFrame(duck_art, 0.1, offset_y=-1),
        AnimationFrame(duck_art, 0.1, offset_y=-1),
        AnimationFrame(duck_art, 0.1, offset_y=0),
    ]
    return Animation("bounce", frames, loop=True)


def create_shake_animation(duck_art: List[str]) -> Animation:
    """Create a shaking animation (for being cold/scared)."""
    frames = [
        AnimationFrame(duck_art, 0.05, offset_x=-1),
        AnimationFrame(duck_art, 0.05, offset_x=1),
        AnimationFrame(duck_art, 0.05, offset_x=-1),
        AnimationFrame(duck_art, 0.05, offset_x=1),
        AnimationFrame(duck_art, 0.05, offset_x=0),
    ]
    return Animation("shake", frames, loop=False)


def create_spin_animation(duck_art_states: Dict[str, List[str]]) -> Animation:
    """Create a spinning animation (needs multiple duck orientations)."""
    # For now just use the normal art with rotation effect
    art = duck_art_states.get("normal", ["(duck)"])
    frames = [
        AnimationFrame(art, 0.1, offset_x=0, effect="*spin*"),
        AnimationFrame(art, 0.1, offset_x=1),
        AnimationFrame(art, 0.1, offset_x=0),
        AnimationFrame(art, 0.1, offset_x=-1),
    ]
    return Animation("spin", frames, loop=False)


# Lazy singleton pattern with thread-safe initialization
_animation_controller: Optional[AnimationController] = None
_animation_controller_lock = threading.Lock()


def get_animation_controller() -> AnimationController:
    """Get the global animation controller instance (lazy initialization). Thread-safe."""
    global _animation_controller
    if _animation_controller is None:
        with _animation_controller_lock:
            if _animation_controller is None:
                _animation_controller = AnimationController()
    return _animation_controller


# Direct instance for backwards compatibility - uses the singleton
animation_controller = get_animation_controller()
