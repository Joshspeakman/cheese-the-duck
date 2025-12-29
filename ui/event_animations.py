"""
Event animation system for Cheese the Duck.

This module provides animated visual sequences for random events like
butterfly visits, bird friends, and other creatures that appear and interact.
"""

import random
import time
import math
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Tuple, Optional, Dict, Any


class EventAnimationState(Enum):
    """States for event animations."""
    WAITING = auto()       # Not started yet
    ARRIVING = auto()      # Moving into view
    INTERACTING = auto()   # Doing the main action
    LEAVING = auto()       # Moving out of view
    FINISHED = auto()      # Animation complete


@dataclass
class AnimationKeyframe:
    """Single keyframe in an animation sequence."""
    x: float              # Position x
    y: float              # Position y
    sprite_key: str       # Which sprite frame to show
    duration: float       # How long this keyframe lasts
    sound: Optional[str] = None  # Optional sound to play


class EventAnimator:
    """
    Base class for event animations.
    
    Handles position interpolation, sprite frame selection, and state management.
    Subclasses define specific movement patterns and sprite sequences.
    """
    
    def __init__(
        self,
        event_id: str,
        playfield_width: int = 60,
        playfield_height: int = 15,
        start_x: Optional[float] = None,
        start_y: Optional[float] = None,
        duration: float = 6.0
    ):
        self.event_id = event_id
        self.playfield_width = playfield_width
        self.playfield_height = playfield_height
        
        # Position (can be float for smooth movement)
        self.x = start_x if start_x is not None else float(playfield_width + 5)
        self.y = start_y if start_y is not None else float(playfield_height // 2)
        
        # Target for movement
        self.target_x = float(playfield_width // 2)
        self.target_y = float(playfield_height // 2)
        
        # Animation state
        self.state = EventAnimationState.WAITING
        self.start_time = 0.0
        self.state_start_time = 0.0
        self.total_duration = duration
        
        # Current sprite
        self.current_sprite_key = "idle_1"
        self.frame_index = 0
        self.last_frame_time = 0.0
        self.frame_duration = 0.2  # Seconds per frame
        
        # Movement parameters
        self.speed = 0.5  # Units per update
        self.wobble_amplitude = 0.0
        self.wobble_frequency = 0.0
        
        # For curved paths
        self.path_points: List[Tuple[float, float]] = []
        self.path_index = 0
        
    def start(self):
        """Begin the animation."""
        self.state = EventAnimationState.ARRIVING
        self.start_time = time.time()
        self.state_start_time = time.time()
        self._setup_arrival_path()
        
    def _setup_arrival_path(self):
        """Setup the path for arriving. Override in subclasses."""
        # Default: straight line from right side to center
        self.path_points = [
            (self.x, self.y),
            (self.target_x, self.target_y)
        ]
        self.path_index = 0
        
    def _setup_interaction(self):
        """Setup the interaction phase. Override in subclasses."""
        self.state_start_time = time.time()
        
    def _setup_leaving_path(self):
        """Setup the path for leaving. Override in subclasses."""
        # Default: straight line to left side
        self.path_points = [
            (self.x, self.y),
            (-5.0, self.y)
        ]
        self.path_index = 0
        
    def update(self, duck_x: int = 30, duck_y: int = 8) -> bool:
        """
        Update the animation state.
        
        Args:
            duck_x: Player duck's x position for interaction targeting
            duck_y: Player duck's y position for interaction targeting
            
        Returns:
            True if animation is still running, False if finished
        """
        if self.state == EventAnimationState.WAITING:
            return True
            
        if self.state == EventAnimationState.FINISHED:
            return False
            
        current_time = time.time()
        elapsed = current_time - self.start_time
        
        # Update sprite frame
        if current_time - self.last_frame_time >= self.frame_duration:
            self._update_sprite_frame()
            self.last_frame_time = current_time
        
        # State-specific updates
        if self.state == EventAnimationState.ARRIVING:
            self._update_arriving(duck_x, duck_y)
        elif self.state == EventAnimationState.INTERACTING:
            self._update_interacting(duck_x, duck_y)
        elif self.state == EventAnimationState.LEAVING:
            self._update_leaving()
            
        return self.state != EventAnimationState.FINISHED
        
    def _update_arriving(self, duck_x: int, duck_y: int):
        """Update arrival movement."""
        # Move toward target
        reached = self._move_along_path()
        
        if reached:
            self.state = EventAnimationState.INTERACTING
            self._setup_interaction()
            
    def _update_interacting(self, duck_x: int, duck_y: int):
        """Update interaction phase."""
        # Default: stay for 2 seconds then leave
        elapsed = time.time() - self.state_start_time
        if elapsed >= 2.0:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()
            
    def _update_leaving(self):
        """Update leaving movement."""
        reached = self._move_along_path()
        
        if reached or self.x < -10 or self.x > self.playfield_width + 10:
            self.state = EventAnimationState.FINISHED
            
    def _move_along_path(self) -> bool:
        """
        Move along the path toward current target.
        
        Returns:
            True if reached destination
        """
        if not self.path_points or self.path_index >= len(self.path_points):
            return True
            
        target_x, target_y = self.path_points[self.path_index]
        
        # Calculate direction
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance < self.speed:
            # Reached this waypoint
            self.x = target_x
            self.y = target_y
            self.path_index += 1
            return self.path_index >= len(self.path_points)
        else:
            # Move toward target
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
            
            # Add wobble
            if self.wobble_amplitude > 0:
                wobble = math.sin(time.time() * self.wobble_frequency) * self.wobble_amplitude
                self.y += wobble
                
            return False
            
    def _update_sprite_frame(self):
        """Update the current sprite frame. Override for custom behavior."""
        self.frame_index = (self.frame_index + 1) % 2
        
        if self.state == EventAnimationState.ARRIVING:
            self.current_sprite_key = f"fly_{self.frame_index + 1}"
        elif self.state == EventAnimationState.INTERACTING:
            self.current_sprite_key = f"idle_{self.frame_index + 1}"
        elif self.state == EventAnimationState.LEAVING:
            self.current_sprite_key = f"fly_{self.frame_index + 1}"
            
    def get_sprite(self) -> List[str]:
        """Get the current sprite ASCII art. Override in subclasses."""
        return ["?"]
        
    def get_position(self) -> Tuple[int, int]:
        """Get current integer position for rendering."""
        return (int(self.x), int(self.y))
        
    def get_color(self) -> str:
        """Get the color for this animation. Override in subclasses."""
        return "white"


class ButterflyAnimator(EventAnimator):
    """
    Animated butterfly that flutters in, circles around the duck, and leaves.
    """
    
    # Butterfly ASCII art frames
    SPRITES = {
        "fly_1": [
            " \\ /",
            "  O ",
            " / \\",
        ],
        "fly_2": [
            "  |",
            " \\O/",
            "  |",
        ],
        "fly_3": [
            "   ",
            "--O--",
            "   ",
        ],
        "idle_1": [
            "\\   /",
            " \\ / ",
            "  O  ",
            " / \\ ",
            "/   \\",
        ],
        "idle_2": [
            " \\ / ",
            "  O  ",
            " / \\ ",
        ],
        "land_1": [
            "\\./",
            " O ",
        ],
        "land_2": [
            "_O_",
        ],
    }
    
    # Color cycles for magical butterfly
    COLORS = ["magenta", "cyan", "yellow", "magenta", "blue"]
    
    def __init__(self, playfield_width: int = 60, playfield_height: int = 15):
        super().__init__(
            event_id="butterfly",
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            duration=8.0
        )
        
        # Start from random edge
        if random.random() < 0.5:
            self.x = float(playfield_width + 5)
        else:
            self.x = -5.0
        self.y = random.uniform(2, playfield_height - 3)
        
        # Butterfly-specific movement
        self.wobble_amplitude = 1.5
        self.wobble_frequency = 4.0
        self.speed = 0.6
        self.frame_duration = 0.15
        
        self.color_index = 0
        self.interaction_orbit_angle = 0.0
        
    def _setup_arrival_path(self):
        """Create a wavy path toward duck."""
        # Target near center
        mid_x = self.playfield_width // 2
        mid_y = self.playfield_height // 2
        
        # Create waypoints with some randomness
        self.path_points = []
        steps = 5
        start_x = self.x
        start_y = self.y
        
        for i in range(steps + 1):
            t = i / steps
            x = start_x + (mid_x - start_x) * t
            y = start_y + (mid_y - start_y) * t
            # Add some wave
            y += math.sin(t * math.pi * 2) * 2
            self.path_points.append((x, y))
            
        self.path_index = 0
        
    def _setup_interaction(self):
        """Orbit around where the duck would be."""
        super()._setup_interaction()
        self.interaction_orbit_angle = 0.0
        
    def _update_interacting(self, duck_x: int, duck_y: int):
        """Circle around the duck position."""
        elapsed = time.time() - self.state_start_time
        
        # Orbit around duck position
        self.interaction_orbit_angle += 0.15
        orbit_radius = 8 + math.sin(elapsed * 2) * 2
        
        self.x = duck_x + math.cos(self.interaction_orbit_angle) * orbit_radius
        self.y = duck_y + math.sin(self.interaction_orbit_angle) * orbit_radius * 0.5
        
        # Keep in bounds
        self.x = max(0, min(self.playfield_width - 5, self.x))
        self.y = max(1, min(self.playfield_height - 2, self.y))
        
        # After orbiting, land briefly then leave
        if elapsed >= 3.5:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()
            
    def _setup_leaving_path(self):
        """Flutter away in a wavy path."""
        exit_x = -10.0 if self.x < self.playfield_width / 2 else self.playfield_width + 10
        exit_y = random.uniform(0, self.playfield_height)
        
        self.path_points = []
        steps = 4
        for i in range(steps + 1):
            t = i / steps
            x = self.x + (exit_x - self.x) * t
            y = self.y + (exit_y - self.y) * t
            y += math.sin(t * math.pi * 3) * 1.5
            self.path_points.append((x, y))
        self.path_index = 0
        
    def _update_sprite_frame(self):
        """Update butterfly sprite and color."""
        self.frame_index = (self.frame_index + 1) % 3
        self.color_index = (self.color_index + 1) % len(self.COLORS)
        
        if self.state == EventAnimationState.ARRIVING:
            self.current_sprite_key = f"fly_{(self.frame_index % 3) + 1}"
        elif self.state == EventAnimationState.INTERACTING:
            if self.frame_index % 4 == 0:
                self.current_sprite_key = "idle_1"
            else:
                self.current_sprite_key = "idle_2"
        elif self.state == EventAnimationState.LEAVING:
            self.current_sprite_key = f"fly_{(self.frame_index % 3) + 1}"
            
    def get_sprite(self) -> List[str]:
        """Get current butterfly sprite."""
        return self.SPRITES.get(self.current_sprite_key, self.SPRITES["fly_1"])
        
    def get_color(self) -> str:
        """Get current butterfly color (cycles through magical colors)."""
        return self.COLORS[self.color_index]


class BirdAnimator(EventAnimator):
    """
    Animated bird that hops in, chirps at the duck, and flies away.
    """
    
    SPRITES = {
        "fly_right_1": [
            "   __",
            "__(o>",
            "\\____)",
        ],
        "fly_right_2": [
            " __  ",
            "(o>__",
            "(__//",
        ],
        "fly_left_1": [
            "__   ",
            "<o)__",
            "(____/",
        ],
        "fly_left_2": [
            "  __ ",
            "__<o)",
            "\\\\__)",
        ],
        "hop_right_1": [
            " .",
            "<o)",
            "/|\\",
            " | ",
        ],
        "hop_right_2": [
            " . ",
            "<o)",
            "\\|/",
            "   ",
        ],
        "idle_right_1": [
            " .",
            "<o)",
            "/L ",
        ],
        "idle_right_2": [
            " .'",
            "<o)",
            " L\\",
        ],
        "chirp_1": [
            " .♪",
            "<O)",
            "/L ",
        ],
        "chirp_2": [
            "♪. ",
            "<O)♪",
            " L\\",
        ],
        "peck_1": [
            "   ",
            " o)",
            "/|°",
        ],
        "peck_2": [
            " . ",
            "<o)",
            "/| ",
        ],
    }
    
    def __init__(self, playfield_width: int = 60, playfield_height: int = 15):
        super().__init__(
            event_id="bird_friend",
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            duration=7.0
        )
        
        # Birds come from the sides at ground level
        self.coming_from_right = random.random() < 0.5
        if self.coming_from_right:
            self.x = float(playfield_width + 5)
        else:
            self.x = -5.0
            
        # Birds fly in at top, then descend
        self.y = 2.0
        
        # Bird-specific movement
        self.speed = 0.8
        self.frame_duration = 0.18
        self.is_hopping = False
        self.hop_count = 0
        
    def _setup_arrival_path(self):
        """Bird flies in from side, descends to ground."""
        ground_y = self.playfield_height - 4
        mid_x = self.playfield_width // 2
        
        # Flight path: come in high, descend
        if self.coming_from_right:
            self.path_points = [
                (self.x, self.y),
                (self.playfield_width * 0.7, 3),
                (mid_x + 5, ground_y - 2),
                (mid_x, ground_y),
            ]
        else:
            self.path_points = [
                (self.x, self.y),
                (self.playfield_width * 0.3, 3),
                (mid_x - 5, ground_y - 2),
                (mid_x, ground_y),
            ]
        self.path_index = 0
        
    def _setup_interaction(self):
        """Bird will hop and chirp."""
        super()._setup_interaction()
        self.is_hopping = True
        self.hop_count = 0
        
    def _update_interacting(self, duck_x: int, duck_y: int):
        """Hop around and chirp."""
        elapsed = time.time() - self.state_start_time
        
        # Occasional hop toward duck
        if int(elapsed * 2) != int((elapsed - 0.5) * 2):
            self.hop_count += 1
            # Small hop toward duck
            if self.x < duck_x:
                self.x += random.uniform(0.5, 1.5)
            elif self.x > duck_x:
                self.x -= random.uniform(0.5, 1.5)
                
        # Chirp and leave after interaction
        if elapsed >= 3.0:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()
            
    def _setup_leaving_path(self):
        """Fly away upward."""
        exit_x = -10.0 if not self.coming_from_right else self.playfield_width + 10
        
        self.path_points = [
            (self.x, self.y),
            (self.x + (5 if exit_x > self.x else -5), self.y - 3),
            (exit_x * 0.5 + self.x * 0.5, 2),
            (exit_x, -5),
        ]
        self.path_index = 0
        self.is_hopping = False
        
    def _update_sprite_frame(self):
        """Update bird sprite based on state."""
        self.frame_index = (self.frame_index + 1) % 2
        direction = "right"  # Birds face toward center
        
        if self.state == EventAnimationState.ARRIVING:
            self.current_sprite_key = f"fly_{direction}_{self.frame_index + 1}"
        elif self.state == EventAnimationState.INTERACTING:
            elapsed = time.time() - self.state_start_time
            if int(elapsed * 3) % 4 == 0:
                self.current_sprite_key = f"chirp_{self.frame_index + 1}"
            elif int(elapsed * 3) % 4 == 1:
                self.current_sprite_key = f"peck_{self.frame_index + 1}"
            else:
                self.current_sprite_key = f"hop_{direction}_{self.frame_index + 1}"
        elif self.state == EventAnimationState.LEAVING:
            self.current_sprite_key = f"fly_{direction}_{self.frame_index + 1}"
            
    def get_sprite(self) -> List[str]:
        """Get current bird sprite."""
        return self.SPRITES.get(self.current_sprite_key, self.SPRITES["idle_right_1"])
        
    def get_color(self) -> str:
        """Birds are brown/orange."""
        return "yellow"


class DuckVisitorAnimator(EventAnimator):
    """
    Another duck that waddles in to visit!
    More elaborate animation than regular visitors.
    """
    
    SPRITES = {
        "waddle_right_1": [
            "  __  ",
            " (o_) ",
            "<|  |>",
            " (__) ",
        ],
        "waddle_right_2": [
            "  __  ",
            " (o_) ",
            "<|  |>",
            "(__) )",
        ],
        "waddle_right_3": [
            "  __  ",
            " (o_) ",
            "<|  |>",
            "( (__)",
        ],
        "idle_1": [
            "  __  ",
            " (o_) ",
            "<|  |>",
            " (__) ",
        ],
        "idle_2": [
            "  __  ",
            " (-_) ",
            "<|  |>",
            " (__) ",
        ],
        "quack_1": [
            "  __  !!",
            " (O_)  ",
            "<|  |> ",
            " (__) ",
        ],
        "quack_2": [
            " !! __ ",
            "  (O>) ",
            " <|  |>",
            "  (__) ",
        ],
        "happy_1": [
            "  __  ♥",
            " (^_) ",
            "<|  |>",
            " (__) ",
        ],
        "happy_2": [
            " ♥__  ",
            " (^_) ",
            "<|  |>",
            "~(__)~",
        ],
        "gift_1": [
            "  __  ",
            " (^_) ",
            "<| ♦|>",
            " (__) ",
        ],
        "gift_2": [
            "  __  ",
            " (^_)♦",
            "<|  |>",
            " (__) ",
        ],
        "wave_1": [
            "  __/ ",
            " (^_) ",
            "<|  |>",
            " (__) ",
        ],
        "wave_2": [
            " \\__  ",
            " (^_) ",
            "<|  |>",
            " (__) ",
        ],
    }
    
    def __init__(self, playfield_width: int = 60, playfield_height: int = 15):
        super().__init__(
            event_id="another_duck",
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            duration=10.0
        )
        
        # Ducks waddle in from sides
        self.coming_from_right = random.random() < 0.5
        ground_y = playfield_height - 5
        
        if self.coming_from_right:
            self.x = float(playfield_width + 8)
        else:
            self.x = -8.0
        self.y = float(ground_y)
        
        # Duck movement
        self.speed = 0.3  # Slow waddle
        self.frame_duration = 0.25
        self.waddle_phase = 0
        
    def _setup_arrival_path(self):
        """Waddle in to meet player duck."""
        ground_y = self.playfield_height - 5
        # Stop a bit away from center to face player's duck
        if self.coming_from_right:
            target_x = self.playfield_width * 0.6
        else:
            target_x = self.playfield_width * 0.4
            
        self.path_points = [
            (self.x, self.y),
            (target_x, ground_y),
        ]
        self.path_index = 0
        
    def _setup_interaction(self):
        """Interact with player's duck."""
        super()._setup_interaction()
        self.interaction_phase = 0  # 0=quack, 1=happy, 2=gift
        
    def _update_interacting(self, duck_x: int, duck_y: int):
        """Cycle through interactions."""
        elapsed = time.time() - self.state_start_time
        
        if elapsed < 1.5:
            self.interaction_phase = 0  # Quacking
        elif elapsed < 3.0:
            self.interaction_phase = 1  # Happy
        elif elapsed < 4.0:
            self.interaction_phase = 2  # Gift giving
        else:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()
            
    def _setup_leaving_path(self):
        """Waddle away waving."""
        exit_x = -10.0 if not self.coming_from_right else self.playfield_width + 10
        
        self.path_points = [
            (self.x, self.y),
            (exit_x, self.y),
        ]
        self.path_index = 0
        
    def _update_sprite_frame(self):
        """Update duck visitor sprite."""
        self.frame_index = (self.frame_index + 1) % 3
        
        if self.state == EventAnimationState.ARRIVING:
            self.current_sprite_key = f"waddle_right_{self.frame_index + 1}"
        elif self.state == EventAnimationState.INTERACTING:
            if self.interaction_phase == 0:
                self.current_sprite_key = f"quack_{(self.frame_index % 2) + 1}"
            elif self.interaction_phase == 1:
                self.current_sprite_key = f"happy_{(self.frame_index % 2) + 1}"
            else:
                self.current_sprite_key = f"gift_{(self.frame_index % 2) + 1}"
        elif self.state == EventAnimationState.LEAVING:
            if self.frame_index % 3 == 0:
                self.current_sprite_key = f"wave_{(self.frame_index // 3 % 2) + 1}"
            else:
                self.current_sprite_key = f"waddle_right_{self.frame_index + 1}"
                
    def get_sprite(self) -> List[str]:
        """Get current duck visitor sprite."""
        return self.SPRITES.get(self.current_sprite_key, self.SPRITES["idle_1"])
        
    def get_color(self) -> str:
        """Visitor ducks are orange."""
        return "yellow"


class ShinyObjectAnimator(EventAnimator):
    """Animation for finding shiny objects."""
    
    SPRITES = {
        "appear_1": [
            " ",
        ],
        "appear_2": [
            ".",
        ],
        "appear_3": [
            "*",
        ],
        "shine_1": [
            " ✦ ",
            "✦*✦",
            " ✦ ",
        ],
        "shine_2": [
            "  *  ",
            " *✦* ",
            "  *  ",
        ],
        "shine_3": [
            " ✧✦✧ ",
            "✦ * ✦",
            " ✧✦✧ ",
        ],
        "pickup_1": [
            " ↑ ",
            " ✦ ",
        ],
        "pickup_2": [
            "↑",
            "✦",
        ],
    }
    
    def __init__(self, playfield_width: int = 60, playfield_height: int = 15):
        super().__init__(
            event_id="found_shiny",
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            duration=5.0
        )
        
        # Shiny appears on ground near center
        self.x = float(playfield_width // 2 + random.randint(-10, 10))
        self.y = float(playfield_height - 4)
        
        self.frame_duration = 0.2
        self.shine_cycle = 0
        
    def _setup_arrival_path(self):
        """No movement - just appears."""
        self.path_points = [(self.x, self.y)]
        self.path_index = 0
        
    def _update_arriving(self, duck_x: int, duck_y: int):
        """Quick appear animation."""
        elapsed = time.time() - self.state_start_time
        if elapsed >= 0.5:
            self.state = EventAnimationState.INTERACTING
            self._setup_interaction()
            
    def _update_interacting(self, duck_x: int, duck_y: int):
        """Shine brightly."""
        elapsed = time.time() - self.state_start_time
        if elapsed >= 2.5:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()
            
    def _setup_leaving_path(self):
        """Float up as duck picks it up."""
        self.path_points = [
            (self.x, self.y),
            (self.x, self.y - 5),
        ]
        self.path_index = 0
        
    def _update_leaving(self):
        """Float up and fade."""
        self._move_along_path()
        if self.y < self.playfield_height - 8:
            self.state = EventAnimationState.FINISHED
            
    def _update_sprite_frame(self):
        """Cycle through shine frames."""
        self.shine_cycle = (self.shine_cycle + 1) % 6
        
        if self.state == EventAnimationState.ARRIVING:
            self.current_sprite_key = f"appear_{min(self.shine_cycle + 1, 3)}"
        elif self.state == EventAnimationState.INTERACTING:
            self.current_sprite_key = f"shine_{(self.shine_cycle % 3) + 1}"
        elif self.state == EventAnimationState.LEAVING:
            self.current_sprite_key = f"pickup_{(self.shine_cycle % 2) + 1}"
            
    def get_sprite(self) -> List[str]:
        return self.SPRITES.get(self.current_sprite_key, self.SPRITES["shine_1"])
        
    def get_color(self) -> str:
        colors = ["yellow", "white", "cyan", "yellow"]
        return colors[self.shine_cycle % len(colors)]


class BreezeAnimator(EventAnimator):
    """Animation for nice breeze - leaves and particles floating by."""
    
    def __init__(self, playfield_width: int = 60, playfield_height: int = 15):
        super().__init__(
            event_id="nice_breeze",
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            duration=4.0
        )
        
        # Breeze particles - ASCII-safe characters for consistent width
        self.particles: List[Tuple[float, float, str]] = []
        self.particle_chars = ["~", "-", "=", "'", ".", "*", "+"]
        
        # Spawn initial particles
        for _ in range(15):
            self.particles.append((
                random.uniform(playfield_width + 1, playfield_width + 20),
                random.uniform(0, playfield_height),
                random.choice(self.particle_chars)
            ))
            
        self.frame_duration = 0.1
        
    def start(self):
        """Begin breeze animation."""
        self.state = EventAnimationState.INTERACTING
        self.start_time = time.time()
        self.state_start_time = time.time()
        
    def update(self, duck_x: int = 30, duck_y: int = 8) -> bool:
        """Update breeze particles."""
        if self.state == EventAnimationState.FINISHED:
            return False
            
        elapsed = time.time() - self.start_time
        
        # Move particles
        new_particles = []
        for x, y, char in self.particles:
            # Move left with slight wave
            new_x = x - 1.2 - random.uniform(0, 0.5)
            new_y = y + math.sin(x * 0.3) * 0.3
            
            if new_x > -5:
                new_particles.append((new_x, new_y, char))
                
        # Spawn new particles from right
        if len(new_particles) < 20 and random.random() < 0.4:
            new_particles.append((
                self.playfield_width + random.uniform(1, 5),
                random.uniform(0, self.playfield_height),
                random.choice(self.particle_chars)
            ))
            
        self.particles = new_particles
        
        # End when time is up and particles are gone
        if elapsed >= self.total_duration and len(self.particles) < 3:
            self.state = EventAnimationState.FINISHED
            return False
            
        return True
        
    def get_sprite(self) -> List[str]:
        """Breeze doesn't have a single sprite - uses particles."""
        return []
        
    def get_particles(self) -> List[Tuple[int, int, str]]:
        """Get all particles for rendering."""
        return [(int(x), int(y), char) for x, y, char in self.particles]
        
    def get_color(self) -> str:
        return "cyan"


class CrumbAnimator(EventAnimator):
    """Animation for finding crumbs - crumbs appear and duck eats them."""
    
    SPRITES = {
        "crumbs_1": [
            " °.°",
            "°  .",
        ],
        "crumbs_2": [
            ".° °",
            " . °",
        ],
        "crumbs_3": [
            "° .°",
            ".  .",
        ],
        "eating_1": [
            "°  ",
            "   ",
        ],
        "eating_2": [
            " ° ",
            "   ",
        ],
        "gone": [
            "   ",
        ],
    }
    
    def __init__(self, playfield_width: int = 60, playfield_height: int = 15):
        super().__init__(
            event_id="found_crumb",
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            duration=4.0
        )
        
        # Crumbs appear on ground
        self.x = float(playfield_width // 2 + random.randint(-5, 5))
        self.y = float(playfield_height - 3)
        
        self.frame_duration = 0.3
        
    def start(self):
        """Begin crumb animation."""
        self.state = EventAnimationState.INTERACTING
        self.start_time = time.time()
        self.state_start_time = time.time()
        
    def update(self, duck_x: int = 30, duck_y: int = 8) -> bool:
        """Update crumb animation."""
        if self.state == EventAnimationState.FINISHED:
            return False
            
        current_time = time.time()
        elapsed = current_time - self.start_time
        
        if current_time - self.last_frame_time >= self.frame_duration:
            self._update_sprite_frame()
            self.last_frame_time = current_time
            
        # Crumbs get eaten over time
        if elapsed >= self.total_duration:
            self.state = EventAnimationState.FINISHED
            return False
            
        return True
        
    def _update_sprite_frame(self):
        elapsed = time.time() - self.start_time
        
        if elapsed < 2.0:
            self.current_sprite_key = f"crumbs_{(self.frame_index % 3) + 1}"
        elif elapsed < 3.0:
            self.current_sprite_key = f"eating_{(self.frame_index % 2) + 1}"
        else:
            self.current_sprite_key = "gone"
            
        self.frame_index += 1
        
    def get_sprite(self) -> List[str]:
        return self.SPRITES.get(self.current_sprite_key, self.SPRITES["crumbs_1"])
        
    def get_color(self) -> str:
        return "yellow"


class LoudNoiseAnimator(EventAnimator):
    """Animation for loud noise - startled effect."""
    
    SPRITES = {
        "bang_1": [
            " !! ",
            "!##!",
            " !! ",
        ],
        "bang_2": [
            "!  !",
            " ## ",
            "!  !",
        ],
        "bang_3": [
            "\\!!/",
            " ## ",
            "/!!\\",
        ],
        "shake_1": [
            "~  ~",
            " ~~ ",
            "~  ~",
        ],
        "shake_2": [
            " ~~ ",
            "~  ~",
            " ~~ ",
        ],
    }
    
    def __init__(self, playfield_width: int = 60, playfield_height: int = 15):
        super().__init__(
            event_id="loud_noise",
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            duration=2.0
        )
        
        # Appears near center
        self.x = float(playfield_width // 2)
        self.y = float(playfield_height // 2 - 2)
        
        self.frame_duration = 0.1
        
    def start(self):
        self.state = EventAnimationState.INTERACTING
        self.start_time = time.time()
        self.state_start_time = time.time()
        
    def update(self, duck_x: int = 30, duck_y: int = 8) -> bool:
        if self.state == EventAnimationState.FINISHED:
            return False
            
        current_time = time.time()
        elapsed = current_time - self.start_time
        
        if current_time - self.last_frame_time >= self.frame_duration:
            self._update_sprite_frame()
            self.last_frame_time = current_time
            
        if elapsed >= self.total_duration:
            self.state = EventAnimationState.FINISHED
            return False
            
        return True
        
    def _update_sprite_frame(self):
        elapsed = time.time() - self.start_time
        
        if elapsed < 0.5:
            self.current_sprite_key = f"bang_{(self.frame_index % 3) + 1}"
        else:
            self.current_sprite_key = f"shake_{(self.frame_index % 2) + 1}"
            
        self.frame_index += 1
        
    def get_sprite(self) -> List[str]:
        return self.SPRITES.get(self.current_sprite_key, self.SPRITES["bang_1"])
        
    def get_color(self) -> str:
        return "red" if time.time() - self.start_time < 0.5 else "yellow"


class DreamCloudAnimator(EventAnimator):
    """Animation for bad dream/good dream - thought bubble."""
    
    SPRITES = {
        "cloud_1": [
            "  .-~~~-. ",
            " /       \\",
            "(  ?   ?  )",
            " \\       /",
            "  '-...-' ",
            "     o    ",
            "    o     ",
        ],
        "cloud_2": [
            "  .-~~~-. ",
            " /  ???  \\",
            "(         )",
            " \\       /",
            "  '-...-' ",
            "    o     ",
            "     o    ",
        ],
        "bad_1": [
            "  .-~~~-. ",
            " / x   x \\",
            "(  ~~~    )",
            " \\       /",
            "  '-...-' ",
            "     o    ",
        ],
        "bad_2": [
            "  .-~~~-. ",
            " /  x x  \\",
            "(   ~~~   )",
            " \\       /",
            "  '-...-' ",
            "    o     ",
        ],
    }
    
    def __init__(self, playfield_width: int = 60, playfield_height: int = 15, is_bad: bool = True):
        super().__init__(
            event_id="bad_dream" if is_bad else "dream",
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            duration=3.5
        )
        
        self.is_bad = is_bad
        self.x = float(playfield_width // 2 - 5)
        self.y = 2.0
        self.frame_duration = 0.4
        
    def start(self):
        self.state = EventAnimationState.INTERACTING
        self.start_time = time.time()
        self.state_start_time = time.time()
        
    def update(self, duck_x: int = 30, duck_y: int = 8) -> bool:
        if self.state == EventAnimationState.FINISHED:
            return False
            
        current_time = time.time()
        elapsed = current_time - self.start_time
        
        if current_time - self.last_frame_time >= self.frame_duration:
            self._update_sprite_frame()
            self.last_frame_time = current_time
            
        if elapsed >= self.total_duration:
            self.state = EventAnimationState.FINISHED
            return False
            
        return True
        
    def _update_sprite_frame(self):
        self.frame_index += 1
        if self.is_bad:
            self.current_sprite_key = f"bad_{(self.frame_index % 2) + 1}"
        else:
            self.current_sprite_key = f"cloud_{(self.frame_index % 2) + 1}"
            
    def get_sprite(self) -> List[str]:
        return self.SPRITES.get(self.current_sprite_key, self.SPRITES["cloud_1"])
        
    def get_color(self) -> str:
        return "red" if self.is_bad else "cyan"


# Factory function to create appropriate animator for an event
def create_event_animator(
    event_id: str,
    playfield_width: int = 60,
    playfield_height: int = 15
) -> Optional[EventAnimator]:
    """
    Create the appropriate animator for an event.
    
    Args:
        event_id: The event identifier
        playfield_width: Width of the playfield
        playfield_height: Height of the playfield
        
    Returns:
        EventAnimator instance or None if no animation exists for this event
    """
    animators = {
        "butterfly": ButterflyAnimator,
        "bird_friend": BirdAnimator,
        "another_duck": DuckVisitorAnimator,
        "found_shiny": ShinyObjectAnimator,
        "nice_breeze": BreezeAnimator,
        "found_crumb": CrumbAnimator,
        "loud_noise": LoudNoiseAnimator,
        "bad_dream": lambda w, h: DreamCloudAnimator(w, h, is_bad=True),
    }
    
    animator_class = animators.get(event_id)
    if animator_class:
        return animator_class(playfield_width, playfield_height)
    return None


# List of all events that have animations
ANIMATED_EVENTS = [
    "butterfly",
    "bird_friend", 
    "another_duck",
    "found_shiny",
    "nice_breeze",
    "found_crumb",
    "loud_noise",
    "bad_dream",
]
