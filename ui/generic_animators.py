"""
Scene-based event animators for Cheese the Duck.

Every event gets a full visual scene: detailed ASCII art sprites that enter,
interact with the environment near Cheese, and leave.  No mere emotion
bubbles -- the actual event content plays out on screen.

Animator types
--------------
- CreatureSceneAnimator  : animals/insects approach and interact
- FoodSceneAnimator      : food items appear / fall / are discovered
- ObjectSceneAnimator    : objects shimmer into view on the ground
- HumanSceneAnimator     : people walk past / interact
- CelestialSceneAnimator : sky objects drift across the upper area
- PropSceneAnimator      : props appear near Cheese for reaction events
- VehicleSceneAnimator   : vehicles pass through the scene
- WeatherSceneAnimator   : particle-based weather effects
- ParticleSceneAnimator  : generic falling/drifting particle effects
- AmbientSceneAnimator   : sparkle/pulse/wave/scatter patterns
"""

import random
import math
import time
from typing import List, Tuple, Dict, Optional

from ui.event_animations import EventAnimator, EventAnimationState
from ui.sprite_library import (
    CREATURES, FOOD, OBJECTS, HUMANS, CELESTIAL, PROPS, VEHICLES,
)


# ===================================================================
# 1. CreatureSceneAnimator
# ===================================================================

class CreatureSceneAnimator(EventAnimator):
    """
    Full scene animation for creature/animal events.
    A detailed ASCII creature enters from the side, approaches Cheese's area,
    performs an interaction (hops around, chirps, splashes, etc.), then leaves.
    """

    BEHAVIORS = {
        "hop":    {"speed": 0.45, "wobble_amp": 1.8, "wobble_freq": 5.0, "interact_time": 3.0},
        "walk":   {"speed": 0.3,  "wobble_amp": 0.3, "wobble_freq": 2.0, "interact_time": 3.5},
        "fly":    {"speed": 0.6,  "wobble_amp": 2.0, "wobble_freq": 3.0, "interact_time": 2.5},
        "swim":   {"speed": 0.35, "wobble_amp": 0.8, "wobble_freq": 2.5, "interact_time": 3.0},
        "crawl":  {"speed": 0.2,  "wobble_amp": 0.2, "wobble_freq": 1.5, "interact_time": 4.0},
        "sneak":  {"speed": 0.25, "wobble_amp": 0.0, "wobble_freq": 0.0, "interact_time": 3.0},
        "swoop":  {"speed": 0.7,  "wobble_amp": 3.0, "wobble_freq": 4.0, "interact_time": 2.0},
        "float":  {"speed": 0.2,  "wobble_amp": 1.0, "wobble_freq": 1.0, "interact_time": 4.0},
    }

    def __init__(
        self,
        event_id: str,
        playfield_width: int = 60,
        playfield_height: int = 15,
        creature_name: str = "frog",
        color: str = "green",
        behavior: str = "hop",
        enter_from: str = "right",
        y_zone: str = "ground",
        duration: float = 7.0,
    ):
        if y_zone == "ground":
            start_y = float(playfield_height - 5)
        elif y_zone == "water":
            start_y = float(playfield_height - 3)
        elif y_zone == "sky":
            start_y = float(random.randint(1, 4))
        elif y_zone == "mid":
            start_y = float(playfield_height // 2)
        else:
            start_y = float(playfield_height - 5)

        if enter_from == "random":
            enter_from = random.choice(["left", "right"])
        coming_from_right = enter_from == "right"
        start_x = float(playfield_width + 6) if coming_from_right else -10.0

        super().__init__(
            event_id=event_id,
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=start_x,
            start_y=start_y,
            duration=duration,
        )

        self._sprites = CREATURES.get(creature_name, CREATURES.get("frog", {}))
        self._sprite_keys = list(self._sprites.keys())
        self._color = color
        self._behavior_name = behavior
        self._coming_from_right = coming_from_right
        self._y_zone = y_zone

        beh = self.BEHAVIORS.get(behavior, self.BEHAVIORS["walk"])
        self.speed = beh["speed"]
        self.wobble_amplitude = beh["wobble_amp"]
        self.wobble_frequency = beh["wobble_freq"]
        self._interact_time = beh["interact_time"]
        self.frame_duration = 0.2
        self._orbit_angle = 0.0
        self._hop_timer = 0.0

    # -- arrival -------------------------------------------------------

    def _setup_arrival_path(self):
        mid_x = self.playfield_width // 2
        target_x = mid_x + random.randint(-8, 8)
        target_y = self.y

        if self._behavior_name in ("fly", "swoop"):
            mid_point_y = self.y - random.uniform(2, 5)
            self.path_points = [
                (self.x, self.y),
                ((self.x + target_x) / 2, mid_point_y),
                (target_x, target_y),
            ]
        elif self._behavior_name == "hop":
            steps = 4
            pts = [(self.x, self.y)]
            for i in range(1, steps + 1):
                t = i / steps
                px = self.x + (target_x - self.x) * t
                py = self.y - abs(math.sin(t * math.pi * 2)) * 2
                pts.append((px, py))
            self.path_points = pts
        else:
            self.path_points = [(self.x, self.y), (target_x, target_y)]
        self.path_index = 0

    # -- interaction ---------------------------------------------------

    def _setup_interaction(self):
        super()._setup_interaction()
        self._orbit_angle = 0.0
        self._hop_timer = 0.0
        self._interact_base_x = self.x
        self._interact_base_y = self.y

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time

        if self._behavior_name in ("hop", "crawl"):
            self._hop_timer += 0.1
            self.x = self._interact_base_x + math.sin(self._hop_timer * 2) * 3
            self.y = self._interact_base_y - abs(math.sin(self._hop_timer * 3)) * 1.5
        elif self._behavior_name in ("fly", "swoop"):
            self._orbit_angle += 0.12
            radius = 8 + math.sin(elapsed * 1.5) * 2
            self.x = duck_x + math.cos(self._orbit_angle) * radius
            self.y = duck_y + math.sin(self._orbit_angle) * radius * 0.4
        elif self._behavior_name == "swim":
            self.x = self._interact_base_x + math.sin(elapsed * 1.5) * 4
            self.y = self._interact_base_y + math.sin(elapsed * 0.8) * 0.5
        elif self._behavior_name == "sneak":
            if abs(self.x - duck_x) > 5:
                self.x += 0.1 if duck_x > self.x else -0.1
        else:
            self.y = self._interact_base_y + math.sin(elapsed * 2) * 1.0

        self.x = max(0, min(self.playfield_width - 8, self.x))
        self.y = max(1, min(self.playfield_height - 3, self.y))

        if elapsed >= self._interact_time:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    # -- leaving -------------------------------------------------------

    def _setup_leaving_path(self):
        exit_x = -12.0 if self._coming_from_right else self.playfield_width + 12
        exit_y = self.y if self._behavior_name not in ("fly", "swoop") else random.uniform(0, 4)

        if self._behavior_name in ("fly", "swoop"):
            mid_y = min(self.y, exit_y) - 3
            self.path_points = [
                (self.x, self.y),
                ((self.x + exit_x) / 2, mid_y),
                (exit_x, exit_y),
            ]
        else:
            self.path_points = [(self.x, self.y), (exit_x, exit_y)]
        self.path_index = 0

    # -- sprite --------------------------------------------------------

    def _update_sprite_frame(self):
        if self._sprite_keys:
            self.frame_index = (self.frame_index + 1) % len(self._sprite_keys)
            self.current_sprite_key = self._sprite_keys[self.frame_index]

    def get_sprite(self) -> List[str]:
        if not self._sprites:
            return ["?"]
        key = self.current_sprite_key if self.current_sprite_key in self._sprites else self._sprite_keys[0]
        return self._sprites.get(key, ["?"])

    def get_color(self) -> str:
        return self._color


# ===================================================================
# 2. FoodSceneAnimator
# ===================================================================

class FoodSceneAnimator(EventAnimator):
    """
    Full scene animation for food-related events.
    A food item drops from above, is thrown in, or is discovered on the ground,
    with sparkle/shimmer frame alternation.
    """

    def __init__(
        self,
        event_id: str,
        playfield_width: int = 60,
        playfield_height: int = 15,
        food_name: str = "bread_loaf",
        color: str = "yellow",
        appear_style: str = "drop",
        duration: float = 6.0,
    ):
        ground_y = float(playfield_height - 4)
        if appear_style == "drop":
            sx = float(playfield_width // 2 + random.randint(-10, 10))
            sy = -3.0
        elif appear_style == "throw":
            sx = float(playfield_width + 6)
            sy = float(random.randint(2, playfield_height // 2))
        else:
            sx = float(playfield_width // 2 + random.randint(-10, 10))
            sy = ground_y

        super().__init__(
            event_id=event_id,
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=sx,
            start_y=sy,
            duration=duration,
        )

        self._sprites = FOOD.get(food_name, FOOD.get("bread_loaf", {}))
        self._color = color
        self._appear_style = appear_style
        self._ground_y = ground_y
        self._current_frame = "appear"
        self.frame_duration = 0.25
        self._shimmer = 0.0

    def _setup_arrival_path(self):
        if self._appear_style == "drop":
            land_x = self.x + random.uniform(-3, 3)
            self.path_points = [(self.x, self.y), (land_x, self._ground_y)]
        elif self._appear_style == "throw":
            land_x = self.playfield_width // 2 + random.randint(-8, 8)
            mid_y = min(self.y, self._ground_y) - 4
            self.path_points = [(self.x, self.y), ((self.x + land_x) / 2, mid_y), (land_x, self._ground_y)]
        else:
            self.path_points = [(self.x, self.y)]
        self.path_index = 0
        self.speed = 0.8 if self._appear_style == "drop" else 0.6

    def _update_arriving(self, duck_x: int, duck_y: int):
        if self._appear_style == "discover":
            self.state = EventAnimationState.INTERACTING
            self._setup_interaction()
            return
        reached = self._move_along_path()
        if reached:
            self.state = EventAnimationState.INTERACTING
            self._setup_interaction()

    def _setup_interaction(self):
        super()._setup_interaction()
        self._current_frame = "idle"

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        self._shimmer += 0.1
        self._current_frame = "sparkle" if int(self._shimmer * 3) % 3 == 0 else "idle"
        if elapsed >= max(2.0, self.total_duration - 3.0):
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    def _setup_leaving_path(self):
        self.path_points = [(self.x, self.y), (self.x, self.y - 8)]
        self.path_index = 0
        self.speed = 0.3

    def _update_leaving(self):
        reached = self._move_along_path()
        if reached or self.y < -5:
            self.state = EventAnimationState.FINISHED

    def get_sprite(self) -> List[str]:
        f = self._sprites.get(self._current_frame)
        if f is None:
            keys = list(self._sprites.keys())
            f = self._sprites[keys[0]] if keys else ["[?]"]
        return f

    def get_color(self) -> str:
        return random.choice([self._color, "white", "bright_yellow"]) if self._current_frame == "sparkle" else self._color


# ===================================================================
# 3. ObjectSceneAnimator
# ===================================================================

class ObjectSceneAnimator(EventAnimator):
    """
    Full scene animation for discovering objects.
    An object shimmers into view on the ground, glows, then fades or is
    picked up.
    """

    def __init__(
        self,
        event_id: str,
        playfield_width: int = 60,
        playfield_height: int = 15,
        object_name: str = "pebble",
        color: str = "yellow",
        duration: float = 6.0,
    ):
        ground_y = float(playfield_height - 4)
        sx = float(playfield_width // 2 + random.randint(-12, 12))

        super().__init__(
            event_id=event_id,
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=sx,
            start_y=ground_y,
            duration=duration,
        )

        self._sprites = OBJECTS.get(object_name, OBJECTS.get("pebble", {}))
        self._color = color
        self._current_frame = "idle"
        self._shine = 0.0
        self.frame_duration = 0.3

    def start(self):
        self.state = EventAnimationState.INTERACTING
        self.start_time = time.time()
        self.state_start_time = time.time()

    def update(self, duck_x: int = 30, duck_y: int = 8) -> bool:
        if self.state == EventAnimationState.FINISHED:
            return False
        elapsed = time.time() - self.start_time
        self._shine += 0.1
        self._current_frame = "shine" if int(self._shine * 2) % 3 == 0 else "idle"
        if elapsed >= self.total_duration:
            self.state = EventAnimationState.FINISHED
            return False
        self.y = float(self.playfield_height - 4) + math.sin(elapsed * 1.5) * 0.5
        return True

    def get_sprite(self) -> List[str]:
        f = self._sprites.get(self._current_frame)
        if f is None:
            keys = list(self._sprites.keys())
            f = self._sprites[keys[0]] if keys else ["(?)"]
        return f

    def get_color(self) -> str:
        return random.choice([self._color, "white", "bright_yellow"]) if self._current_frame == "shine" else self._color


# ===================================================================
# 4. HumanSceneAnimator
# ===================================================================

class HumanSceneAnimator(EventAnimator):
    """
    Full scene animation for events involving humans/people.
    A person walks across the scene, pauses near the duck, then continues.
    """

    def __init__(
        self,
        event_id: str,
        playfield_width: int = 60,
        playfield_height: int = 15,
        human_name: str = "child",
        color: str = "white",
        duration: float = 7.0,
        enter_from: str = "right",
    ):
        if enter_from == "random":
            enter_from = random.choice(["left", "right"])
        coming_from_right = enter_from == "right"
        sx = float(playfield_width + 8) if coming_from_right else -10.0
        gy = float(playfield_height - 5)

        super().__init__(
            event_id=event_id,
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=sx,
            start_y=gy,
            duration=duration,
        )

        self._sprites = HUMANS.get(human_name, HUMANS.get("child", {}))
        self._sprite_keys = list(self._sprites.keys())
        self._color = color
        self._coming_from_right = coming_from_right
        self.speed = 0.35
        self.frame_duration = 0.25

    def _setup_arrival_path(self):
        stop_x = self.playfield_width // 2 + random.randint(-5, 5)
        self.path_points = [(self.x, self.y), (stop_x, self.y)]
        self.path_index = 0

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        if elapsed >= 2.5:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    def _setup_leaving_path(self):
        exit_x = -12.0 if not self._coming_from_right else self.playfield_width + 12
        self.path_points = [(self.x, self.y), (exit_x, self.y)]
        self.path_index = 0

    def _update_sprite_frame(self):
        if self._sprite_keys:
            if self.state == EventAnimationState.INTERACTING:
                idx = min(2, len(self._sprite_keys) - 1)
            else:
                idx = (self.frame_index + 1) % min(2, len(self._sprite_keys))
            self.frame_index = idx

    def get_sprite(self) -> List[str]:
        if not self._sprite_keys:
            return ["?"]
        idx = self.frame_index % len(self._sprite_keys)
        return self._sprites.get(self._sprite_keys[idx], ["?"])

    def get_color(self) -> str:
        return self._color


# ===================================================================
# 5. CelestialSceneAnimator
# ===================================================================

class CelestialSceneAnimator(EventAnimator):
    """
    Full scene animation for sky/celestial events.
    Objects appear in the upper portion of the screen, drift slowly, and fade.
    """

    def __init__(
        self,
        event_id: str,
        playfield_width: int = 60,
        playfield_height: int = 15,
        celestial_name: str = "shooting_star",
        color: str = "white",
        duration: float = 7.0,
        drift_direction: str = "left",
    ):
        sky_y = float(random.randint(1, max(2, playfield_height // 3)))
        if drift_direction == "left":
            sx = float(playfield_width + 5)
        elif drift_direction == "right":
            sx = -10.0
        else:
            sx = float(random.randint(5, playfield_width - 10))

        super().__init__(
            event_id=event_id,
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=sx,
            start_y=sky_y,
            duration=duration,
        )

        self._sprites = CELESTIAL.get(celestial_name, CELESTIAL.get("shooting_star", {}))
        self._sprite_keys = list(self._sprites.keys())
        self._color = color
        self._drift_dir = drift_direction
        self.speed = 0.25
        self.frame_duration = 0.35

    def _setup_arrival_path(self):
        target_x = self.playfield_width // 2
        if self._drift_dir == "none":
            target_x = self.x
        self.path_points = [(self.x, self.y), (target_x, self.y)]
        self.path_index = 0

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        self.y += math.sin(elapsed * 0.8) * 0.05
        if elapsed >= max(2.0, self.total_duration - 3.0):
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    def _setup_leaving_path(self):
        if self._drift_dir == "left":
            ex = -15.0
        elif self._drift_dir == "right":
            ex = self.playfield_width + 15
        else:
            ex = self.x
        self.path_points = [(self.x, self.y), (ex, self.y - 2)]
        self.path_index = 0

    def _update_sprite_frame(self):
        if self._sprite_keys:
            self.frame_index = (self.frame_index + 1) % len(self._sprite_keys)

    def get_sprite(self) -> List[str]:
        if not self._sprite_keys:
            return ["*"]
        idx = self.frame_index % len(self._sprite_keys)
        return self._sprites.get(self._sprite_keys[idx], ["*"])

    def get_color(self) -> str:
        return self._color


# ===================================================================
# 6. PropSceneAnimator
# ===================================================================

class PropSceneAnimator(EventAnimator):
    """
    Full scene animation for duck reaction / internal events.
    Instead of a boring emotion bubble a relevant PROP appears nearby --
    a rock for stubbed_toe, musical notes for singing, impact stars for
    a collision, etc.
    """

    def __init__(
        self,
        event_id: str,
        playfield_width: int = 60,
        playfield_height: int = 15,
        prop_name: str = "exclamation",
        color: str = "yellow",
        appear_style: str = "pop",
        duration: float = 5.0,
        offset_x: int = 0,
        offset_y: int = -3,
    ):
        duck_cx = playfield_width // 2
        duck_cy = playfield_height // 2

        if appear_style == "drop":
            sx, sy = float(duck_cx + offset_x), -3.0
        elif appear_style == "slide":
            sx, sy = float(playfield_width + 5), float(duck_cy + offset_y)
        elif appear_style == "rise":
            sx, sy = float(duck_cx + offset_x), float(playfield_height + 3)
        else:
            sx, sy = float(duck_cx + offset_x), float(duck_cy + offset_y)

        super().__init__(
            event_id=event_id,
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=sx,
            start_y=sy,
            duration=duration,
        )

        self._sprites = PROPS.get(prop_name, PROPS.get("exclamation", {}))
        self._color = color
        self._appear_style = appear_style
        self._current_frame = "appear"
        self._target_x = float(duck_cx + offset_x)
        self._target_y = float(duck_cy + offset_y)
        self.frame_duration = 0.25
        self._anim_timer = 0.0

    # -- arrival -------------------------------------------------------

    def _setup_arrival_path(self):
        if self._appear_style in ("drop", "slide", "rise"):
            self.path_points = [(self.x, self.y), (self._target_x, self._target_y)]
            self.speed = 0.5
        else:
            self.path_points = [(self.x, self.y)]
        self.path_index = 0

    def _update_arriving(self, duck_x: int, duck_y: int):
        if self._appear_style == "pop":
            self.state = EventAnimationState.INTERACTING
            self._setup_interaction()
            return
        reached = self._move_along_path()
        if reached:
            self.state = EventAnimationState.INTERACTING
            self._setup_interaction()

    # -- interaction ---------------------------------------------------

    def _setup_interaction(self):
        super()._setup_interaction()
        self._current_frame = "idle"

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        self._anim_timer += 0.1

        phase = int(self._anim_timer * 2) % 3
        self._current_frame = "appear" if phase == 1 else "idle"

        if self._appear_style in ("pop", "drop"):
            self.y = self._target_y + math.sin(elapsed * 2.5) * 0.8
            self.x = self._target_x
        elif self._appear_style == "slide":
            self.x = self._target_x + math.sin(elapsed * 1.5) * 1.5
            self.y = self._target_y
        elif self._appear_style == "rise":
            self.y = self._target_y - elapsed * 0.3
            self.x = self._target_x + math.sin(elapsed * 2) * 0.5

        if elapsed >= max(1.5, self.total_duration - 2.0):
            self.state = EventAnimationState.LEAVING
            self._current_frame = "fade"
            self._setup_leaving_path()

    # -- leaving -------------------------------------------------------

    def _setup_leaving_path(self):
        self.path_points = [(self.x, self.y), (self.x + random.uniform(-3, 3), self.y - 6)]
        self.path_index = 0
        self.speed = 0.25

    def _update_leaving(self):
        reached = self._move_along_path()
        self._current_frame = "fade"
        if reached or self.y < -5:
            self.state = EventAnimationState.FINISHED

    # -- sprite --------------------------------------------------------

    def get_sprite(self) -> List[str]:
        f = self._sprites.get(self._current_frame)
        if f is None:
            keys = list(self._sprites.keys())
            f = self._sprites[keys[0]] if keys else ["?"]
        return f

    def get_color(self) -> str:
        return self._color


# ===================================================================
# 7. VehicleSceneAnimator
# ===================================================================

class VehicleSceneAnimator(EventAnimator):
    """
    Scene animation for vehicles (boats, helicopters, etc.)
    that pass through the scene.
    """

    def __init__(
        self,
        event_id: str,
        playfield_width: int = 60,
        playfield_height: int = 15,
        vehicle_name: str = "boat",
        color: str = "white",
        y_zone: str = "water",
        duration: float = 7.0,
    ):
        if y_zone == "sky":
            sy = float(random.randint(1, 4))
        elif y_zone == "water":
            sy = float(playfield_height - 4)
        else:
            sy = float(playfield_height // 2)

        super().__init__(
            event_id=event_id,
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=float(playfield_width + 8),
            start_y=sy,
            duration=duration,
        )

        self._sprites = VEHICLES.get(vehicle_name, VEHICLES.get("boat", {}))
        self._sprite_keys = list(self._sprites.keys())
        self._color = color
        self.speed = 0.3
        self.frame_duration = 0.3

    def _setup_arrival_path(self):
        self.path_points = [(self.x, self.y), (self.playfield_width // 2, self.y)]
        self.path_index = 0

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        self.y += math.sin(elapsed * 1.5) * 0.05
        if elapsed >= 2.5:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    def _setup_leaving_path(self):
        self.path_points = [(self.x, self.y), (-15.0, self.y)]
        self.path_index = 0

    def _update_sprite_frame(self):
        if self._sprite_keys:
            self.frame_index = (self.frame_index + 1) % len(self._sprite_keys)

    def get_sprite(self) -> List[str]:
        if not self._sprite_keys:
            return ["?"]
        idx = self.frame_index % len(self._sprite_keys)
        return self._sprites.get(self._sprite_keys[idx], ["?"])

    def get_color(self) -> str:
        return self._color


# ===================================================================
# 8. WeatherSceneAnimator  (particle-based)
# ===================================================================

class WeatherSceneAnimator(EventAnimator):
    """
    Particle-based weather animation covering the whole playfield.
    """

    _PRESETS = {
        "rain":  {"chars": "|,",   "fall": 1.0,  "drift": 0.0,   "dens": 1.0},
        "snow":  {"chars": "*.+",  "fall": 0.25, "drift": 0.15,  "dens": 0.8},
        "wind":  {"chars": "~-=",  "fall": 0.0,  "drift": 1.2,   "dens": 0.7},
        "fog":   {"chars": ".:'",  "fall": 0.0,  "drift": 0.05,  "dens": 0.5},
        "sun":   {"chars": "*.+",  "fall": 0.3,  "drift": 0.05,  "dens": 0.6},
        "hail":  {"chars": "oO",   "fall": 1.2,  "drift": 0.0,   "dens": 0.9},
        "mist":  {"chars": ".'",   "fall": 0.0,  "drift": 0.04,  "dens": 0.4},
    }

    def __init__(
        self,
        event_id: str,
        playfield_width: int = 60,
        playfield_height: int = 15,
        weather_type: str = "rain",
        color: str = "cyan",
        intensity: int = 14,
        duration: float = 7.0,
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
        self._fall = preset["fall"]
        self._drift = preset["drift"]
        self._density = max(1, int(intensity * preset["dens"]))
        self._particles: List[Dict] = []

    def _spawn(self) -> Dict:
        pw, ph = self.playfield_width, self.playfield_height
        wt = self.weather_type
        if wt in ("rain", "hail", "snow"):
            x, y = random.uniform(0, pw - 1), random.uniform(-2, 0)
        elif wt == "wind":
            x, y = random.uniform(pw, pw + 5), random.uniform(0, ph - 1)
        elif wt in ("fog", "mist"):
            x, y = random.uniform(0, pw - 1), random.uniform(ph * 0.4, ph - 1)
        elif wt == "sun":
            x, y = pw / 2 + random.uniform(-5, 5), random.uniform(-1, 1)
        else:
            x, y = random.uniform(0, pw - 1), random.uniform(-2, 0)
        return {"x": x, "y": y, "char": random.choice(self._chars),
                "vy": self._fall + random.uniform(-0.05, 0.05),
                "vx": self._drift + random.uniform(-0.03, 0.03)}

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
        arrive = min(1.0, self.total_duration * 0.15)
        leave_start = self.total_duration - min(1.5, self.total_duration * 0.2)

        if self.state == EventAnimationState.ARRIVING:
            while len(self._particles) < int(self._density * min(1.0, elapsed / arrive)):
                self._particles.append(self._spawn())
            if elapsed >= arrive:
                self.state = EventAnimationState.INTERACTING
                self.state_start_time = now
        elif self.state == EventAnimationState.INTERACTING:
            while len(self._particles) < self._density:
                self._particles.append(self._spawn())
            if elapsed >= leave_start:
                self.state = EventAnimationState.LEAVING
                self.state_start_time = now
        elif self.state == EventAnimationState.LEAVING:
            if not self._particles or elapsed >= self.total_duration + 2:
                self.state = EventAnimationState.FINISHED
                return False

        survivors: List[Dict] = []
        pw, ph = self.playfield_width, self.playfield_height
        for p in self._particles:
            p["y"] += p["vy"]
            p["x"] -= p["vx"]
            if self.weather_type == "hail" and p["y"] >= ph - 1:
                p["vy"] = -abs(p["vy"]) * 0.4
                p["y"] = float(ph - 1)
            if -2 <= p["x"] <= pw + 2 and -2 <= p["y"] <= ph + 2:
                survivors.append(p)
            elif self.state == EventAnimationState.INTERACTING:
                survivors.append(self._spawn())
        self._particles = survivors
        return True

    def get_particles(self) -> List[Tuple[int, int, str]]:
        pw, ph = self.playfield_width, self.playfield_height
        return [(int(p["x"]), int(p["y"]), p["char"]) for p in self._particles
                if 0 <= int(p["x"]) < pw and 0 <= int(p["y"]) < ph]

    def get_sprite(self) -> List[str]:
        return []

    def get_color(self) -> str:
        return self._color


# ===================================================================
# 9. ParticleSceneAnimator
# ===================================================================

class ParticleSceneAnimator(EventAnimator):
    """
    Generic particle animator for falling/drifting effects (leaves, petals,
    pollen, embers, etc.).
    """

    def __init__(
        self,
        event_id: str,
        playfield_width: int = 60,
        playfield_height: int = 15,
        particles: str = ".*+~",
        color: str = "white",
        density: int = 10,
        fall_speed: float = 0.3,
        drift_speed: float = 0.1,
        duration: float = 6.0,
        spread: str = "full",
    ):
        super().__init__(event_id=event_id, playfield_width=playfield_width,
                         playfield_height=playfield_height, duration=duration)
        self._chars = list(particles)
        self._color = color
        self._density = density
        self._fall = fall_speed
        self._drift = drift_speed
        self._spread = spread
        self._particles: List[Dict] = []

    def _spawn(self) -> Dict:
        pw, ph = self.playfield_width, self.playfield_height
        if self._spread == "top":
            x, y = random.uniform(0, pw - 1), random.uniform(-2, 0)
        elif self._spread == "bottom":
            x, y = random.uniform(0, pw - 1), random.uniform(ph - 2, ph)
        elif self._spread == "center":
            x = pw / 2 + random.uniform(-pw / 4, pw / 4)
            y = ph / 2 + random.uniform(-ph / 4, ph / 4)
        else:
            x = random.uniform(0, pw - 1)
            y = random.uniform(-2, 0) if self._fall > 0 else random.uniform(0, ph - 1)
        return {"x": x, "y": y, "char": random.choice(self._chars)}

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
        arrive = min(1.0, self.total_duration * 0.15)
        leave = self.total_duration - min(1.5, self.total_duration * 0.2)

        if self.state == EventAnimationState.ARRIVING:
            while len(self._particles) < int(self._density * min(1.0, elapsed / arrive)):
                self._particles.append(self._spawn())
            if elapsed >= arrive:
                self.state = EventAnimationState.INTERACTING
                self.state_start_time = now
        elif self.state == EventAnimationState.INTERACTING:
            while len(self._particles) < self._density:
                self._particles.append(self._spawn())
            if elapsed >= leave:
                self.state = EventAnimationState.LEAVING
                self.state_start_time = now
        elif self.state == EventAnimationState.LEAVING:
            if not self._particles or elapsed >= self.total_duration + 2:
                self.state = EventAnimationState.FINISHED
                return False

        pw, ph = self.playfield_width, self.playfield_height
        survivors: List[Dict] = []
        for p in self._particles:
            p["y"] += self._fall
            p["x"] += self._drift + random.uniform(-0.15, 0.15)
            if -1 <= p["x"] <= pw and -1 <= p["y"] <= ph:
                survivors.append(p)
            elif self.state == EventAnimationState.INTERACTING:
                survivors.append(self._spawn())
        self._particles = survivors
        return True

    def get_particles(self) -> List[Tuple[int, int, str]]:
        pw, ph = self.playfield_width, self.playfield_height
        return [(int(p["x"]), int(p["y"]), p["char"]) for p in self._particles
                if 0 <= int(p["x"]) < pw and 0 <= int(p["y"]) < ph]

    def get_sprite(self) -> List[str]:
        return []

    def get_color(self) -> str:
        return self._color


# ===================================================================
# 10. AmbientSceneAnimator  (sparkle/pulse/wave)
# ===================================================================

class AmbientSceneAnimator(EventAnimator):
    """
    Particle-based ambient animator for discovery, mood, and atmosphere events.
    Creates sparkle / pulse / wave / scatter patterns across the scene.
    """

    def __init__(
        self,
        event_id: str,
        playfield_width: int = 60,
        playfield_height: int = 15,
        pattern: str = "sparkle",
        chars: str = "*.+",
        color: str = "cyan",
        duration: float = 5.0,
        intensity: int = 8,
    ):
        super().__init__(event_id=event_id, playfield_width=playfield_width,
                         playfield_height=playfield_height, duration=duration)
        self.pattern = pattern
        self._chars = list(chars)
        self._color = color
        self._intensity = intensity
        self._particles: List[Dict] = []
        self._cx = playfield_width / 2.0
        self._cy = playfield_height / 2.0

    def _make(self, x: float, y: float, vx: float = 0, vy: float = 0) -> Dict:
        return {"x": x, "y": y, "char": random.choice(self._chars),
                "born": time.time(), "life": random.uniform(0.4, 1.0),
                "vx": vx, "vy": vy}

    def _spawn_one(self, elapsed: float = 0) -> Dict:
        pw, ph = self.playfield_width, self.playfield_height
        if self.pattern == "sparkle":
            return self._make(random.uniform(0, pw - 1), random.uniform(0, ph - 1))
        elif self.pattern == "wave":
            off = elapsed * 4
            side = random.choice([-1, 1])
            return self._make(self._cx + side * off, self._cy + random.uniform(-0.5, 0.5))
        elif self.pattern == "pulse":
            r = elapsed * 3
            a = random.uniform(0, 2 * math.pi)
            return self._make(self._cx + math.cos(a) * r, self._cy + math.sin(a) * r * 0.5)
        elif self.pattern == "scatter":
            a = random.uniform(0, 2 * math.pi)
            sp = random.uniform(0.5, 2)
            return self._make(self._cx, self._cy, math.cos(a) * sp, math.sin(a) * sp * 0.5)
        return self._make(random.uniform(0, pw - 1), random.uniform(0, ph - 1))

    def start(self):
        self.state = EventAnimationState.INTERACTING
        self.start_time = time.time()
        self.state_start_time = time.time()
        self._particles = []

    def update(self, duck_x: int = 30, duck_y: int = 8) -> bool:
        if self.state == EventAnimationState.FINISHED:
            return False
        now = time.time()
        if (now - self.start_time) >= self.total_duration:
            self.state = EventAnimationState.FINISHED
            return False
        self._particles = [p for p in self._particles if (now - p["born"]) < p["life"]]
        for p in self._particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vx"] *= 0.92
            p["vy"] *= 0.92
        se = now - self.state_start_time
        while len(self._particles) < self._intensity:
            self._particles.append(self._spawn_one(se))
        return True

    def get_particles(self) -> List[Tuple[int, int, str]]:
        pw, ph = self.playfield_width, self.playfield_height
        return [(int(p["x"]), int(p["y"]), p["char"]) for p in self._particles
                if 0 <= p["x"] < pw and 0 <= p["y"] < ph]

    def get_sprite(self) -> List[str]:
        return []

    def get_color(self) -> str:
        return self._color
