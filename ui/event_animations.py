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
            " .#",
            "<O)",
            "/L ",
        ],
        "chirp_2": [
            "#. ",
            "<O)#",
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
    
    # New adult-style 3-line sprites
    SPRITES = {
        "waddle_right_1": [" ___ ", "(o__)>", "/'__\\"],
        "waddle_right_2": [" ___ ", "(o__)>", " '__\\"],
        "waddle_right_3": [" ___ ", "(o__)>", "/'__ "],
        "idle_1": [" ___ ", "(o__)>", "/'__\\"],
        "idle_2": [" ___ ", "(-_-)>", "/'__\\"],
        "quack_1": [" ___!!", "(O__)>", "/'__\\"],
        "quack_2": ["!! __ ", "(O__)>", "/'__\\"],
        "happy_1": [" ___ +", "(^__)>", "/'__\\"],
        "happy_2": ["+ ___ ", "(^__)>", "/'__\\"],
        "gift_1": [" ___ ", "(^__)>", "/'*_\\"],
        "gift_2": [" ___ *", "(^__)>", "/'__\\"],
        "wave_1": [" ___/ ", "(^__)>", "/'__\\"],
        "wave_2": ["\\ ___ ", "(^__)>", "/'__\\"],
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
        ground_y = playfield_height - 4  # 3-line sprite
        
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
        ground_y = self.playfield_height - 4  # 3-line sprite
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
            " * ",
            "***",
            " * ",
        ],
        "shine_2": [
            "  *  ",
            " *** ",
            "  *  ",
        ],
        "shine_3": [
            " *** ",
            "* * *",
            " *** ",
        ],
        "pickup_1": [
            " ^ ",
            " * ",
        ],
        "pickup_2": [
            "^",
            "*",
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
    """Animation for nice breeze - leaves and particles floating across entire habitat."""

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

        # Spawn initial particles across ENTIRE habitat area (not just waiting off-screen)
        # Distribute evenly across height with multiple columns
        for col in range(8):  # 8 columns of particles
            x_offset = col * (playfield_width // 6)
            for row in range(playfield_height - 1):  # Cover full height
                if random.random() < 0.4:  # 40% chance per cell
                    self.particles.append((
                        float(x_offset + random.uniform(-3, 3)),
                        float(row + random.uniform(0, 1)),
                        random.choice(self.particle_chars)
                    ))

        # Also add particles coming from off-screen
        for _ in range(10):
            self.particles.append((
                random.uniform(playfield_width + 1, playfield_width + 20),
                random.uniform(0, playfield_height - 1),
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
            # Move left with slight wave - gentler movement
            new_x = x - 1.0 - random.uniform(0, 0.3)
            new_y = y + math.sin(x * 0.2) * 0.15  # Gentler vertical wave

            # Keep Y within bounds
            new_y = max(0, min(self.playfield_height - 1, new_y))

            if new_x > -5:
                new_particles.append((new_x, new_y, char))

        # Only spawn new particles if we're still within duration
        if elapsed < self.total_duration:
            if len(new_particles) < 50 and random.random() < 0.6:
                # Spawn at different heights, favoring even distribution
                spawn_y = random.uniform(0, self.playfield_height - 1)
                new_particles.append((
                    self.playfield_width + random.uniform(1, 5),
                    spawn_y,
                    random.choice(self.particle_chars)
                ))

        self.particles = new_particles

        # End when time is up OR all particles have left the screen
        if elapsed >= self.total_duration + 2.0 or len(self.particles) == 0:
            self.state = EventAnimationState.FINISHED
            self.particles = []  # Clear any remaining particles
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


# ═══════════════════════════════════════════════════════════════════════════
# AREA-SPECIFIC ANIMATORS — used by the 150+ location events
# ═══════════════════════════════════════════════════════════════════════════


class LilyPadAnimator(EventAnimator):
    """Animation for lily pad events — a pad bobs on water."""

    SPRITES = {
        "pad_1": [
            " ~~~~ ",
            "(____)",
            " ~~~~ ",
        ],
        "pad_2": [
            "  ~~~ ",
            " (___)",
            "  ~~~ ",
        ],
        "pad_3": [
            " @~~~ ",
            "(_*__)",
            " ~~~~ ",
        ],
        "pad_4": [
            "  @~~ ",
            " (_*_)",
            "  ~~~ ",
        ],
    }

    def __init__(self, playfield_width: int = 60, playfield_height: int = 15):
        super().__init__(
            event_id="lily_pad",
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            duration=5.0,
        )
        self.x = float(playfield_width // 2 + random.randint(-8, 8))
        self.y = float(playfield_height - 4)
        self.frame_duration = 0.4
        self.bob_phase = 0.0

    def start(self):
        self.state = EventAnimationState.INTERACTING
        self.start_time = time.time()
        self.state_start_time = time.time()

    def update(self, duck_x: int = 30, duck_y: int = 8) -> bool:
        if self.state == EventAnimationState.FINISHED:
            return False
        now = time.time()
        elapsed = now - self.start_time
        if now - self.last_frame_time >= self.frame_duration:
            self._update_sprite_frame()
            self.last_frame_time = now
        self.bob_phase += 0.05
        self.y = float(self.playfield_height - 4) + math.sin(self.bob_phase) * 0.3
        if elapsed >= self.total_duration:
            self.state = EventAnimationState.FINISHED
            return False
        return True

    def _update_sprite_frame(self):
        self.frame_index = (self.frame_index + 1) % 4
        self.current_sprite_key = f"pad_{self.frame_index + 1}"

    def get_sprite(self) -> List[str]:
        return self.SPRITES.get(self.current_sprite_key, self.SPRITES["pad_1"])

    def get_color(self) -> str:
        return "green"


class RippleAnimator(EventAnimator):
    """Expanding ripple circles on water."""

    SPRITES = {
        "ripple_1": [" . "],
        "ripple_2": [" o "],
        "ripple_3": [" O "],
        "ripple_4": ["( )"],
        "ripple_5": ["(   )"],
        "ripple_6": ["(     )"],
        "ripple_7": [" (       ) "],
    }

    def __init__(self, playfield_width: int = 60, playfield_height: int = 15):
        super().__init__(
            event_id="ripple",
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            duration=4.0,
        )
        self.x = float(playfield_width // 2 + random.randint(-10, 10))
        self.y = float(playfield_height - 3)
        self.frame_duration = 0.3

    def start(self):
        self.state = EventAnimationState.INTERACTING
        self.start_time = time.time()
        self.state_start_time = time.time()

    def update(self, duck_x: int = 30, duck_y: int = 8) -> bool:
        if self.state == EventAnimationState.FINISHED:
            return False
        now = time.time()
        if now - self.last_frame_time >= self.frame_duration:
            self._update_sprite_frame()
            self.last_frame_time = now
        if now - self.start_time >= self.total_duration:
            self.state = EventAnimationState.FINISHED
            return False
        return True

    def _update_sprite_frame(self):
        self.frame_index = (self.frame_index + 1) % 7
        self.current_sprite_key = f"ripple_{self.frame_index + 1}"

    def get_sprite(self) -> List[str]:
        return self.SPRITES.get(self.current_sprite_key, self.SPRITES["ripple_1"])

    def get_color(self) -> str:
        return "cyan"


class FrogAnimator(EventAnimator):
    """A frog hops in, croaks, hops away."""

    SPRITES = {
        "hop_1": [
            " @..@ ",
            "(----)>",
            " /  \\ ",
        ],
        "hop_2": [
            "  @..@",
            " (----)>",
            "  ^^  ",
        ],
        "sit_1": [
            " @..@ ",
            "(----)>",
            " \\__/ ",
        ],
        "sit_2": [
            " @oo@ ",
            "(----)>",
            " \\__/ ",
        ],
        "croak_1": [
            " @OO@ ",
            "(OOOO)>",
            " \\__/ ",
        ],
        "croak_2": [
            " @oo@ ",
            "(-OO-)>",
            " \\__/ ",
        ],
    }

    def __init__(self, playfield_width: int = 60, playfield_height: int = 15):
        super().__init__(
            event_id="frog_hop",
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            duration=6.0,
        )
        self.coming_from_right = random.random() < 0.5
        ground = playfield_height - 4
        self.x = float(playfield_width + 5) if self.coming_from_right else -5.0
        self.y = float(ground)
        self.speed = 0.7
        self.frame_duration = 0.2

    def _setup_arrival_path(self):
        ground = self.playfield_height - 4
        mid = self.playfield_width // 2
        self.path_points = [(self.x, self.y), (mid + random.randint(-5, 5), ground)]
        self.path_index = 0

    def _setup_interaction(self):
        super()._setup_interaction()

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        if elapsed >= 2.5:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    def _setup_leaving_path(self):
        exit_x = -10.0 if not self.coming_from_right else self.playfield_width + 10
        # Frog hops upward then away
        self.path_points = [
            (self.x, self.y),
            (self.x + (5 if exit_x > self.x else -5), self.y - 3),
            (exit_x, self.y),
        ]
        self.path_index = 0

    def _update_sprite_frame(self):
        self.frame_index = (self.frame_index + 1) % 2
        if self.state == EventAnimationState.ARRIVING:
            self.current_sprite_key = f"hop_{self.frame_index + 1}"
        elif self.state == EventAnimationState.INTERACTING:
            elapsed = time.time() - self.state_start_time
            if int(elapsed * 2) % 3 == 0:
                self.current_sprite_key = f"croak_{self.frame_index + 1}"
            else:
                self.current_sprite_key = f"sit_{self.frame_index + 1}"
        elif self.state == EventAnimationState.LEAVING:
            self.current_sprite_key = f"hop_{self.frame_index + 1}"

    def get_sprite(self) -> List[str]:
        return self.SPRITES.get(self.current_sprite_key, self.SPRITES["sit_1"])

    def get_color(self) -> str:
        return "green"


class DragonflyAnimator(EventAnimator):
    """A dragonfly zips erratically around the screen."""

    SPRITES = {
        "fly_1": ["--O--"],
        "fly_2": [" =O= "],
        "fly_3": ["--o--"],
        "hover_1": ["==O=="],
        "hover_2": [" =o= "],
    }

    def __init__(self, playfield_width: int = 60, playfield_height: int = 15):
        super().__init__(
            event_id="dragonfly",
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            duration=5.0,
        )
        self.x = float(playfield_width + 3)
        self.y = random.uniform(2, playfield_height - 3)
        self.speed = 1.2
        self.frame_duration = 0.1
        self._zip_target_x = 0.0
        self._zip_target_y = 0.0
        self._zip_timer = 0.0

    def _setup_arrival_path(self):
        mid_x = self.playfield_width // 2
        mid_y = self.playfield_height // 2
        self.path_points = [(self.x, self.y), (mid_x, mid_y)]
        self.path_index = 0

    def _setup_interaction(self):
        super()._setup_interaction()
        self._pick_zip_target()

    def _pick_zip_target(self):
        self._zip_target_x = random.uniform(5, self.playfield_width - 5)
        self._zip_target_y = random.uniform(2, self.playfield_height - 3)
        self._zip_timer = time.time()

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        # Zip to random points
        dx = self._zip_target_x - self.x
        dy = self._zip_target_y - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist < 2 or time.time() - self._zip_timer > 0.8:
            self._pick_zip_target()
        else:
            self.x += (dx / max(dist, 0.1)) * self.speed
            self.y += (dy / max(dist, 0.1)) * self.speed * 0.5
        if elapsed >= 3.0:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    def _setup_leaving_path(self):
        self.path_points = [(self.x, self.y), (self.playfield_width + 10, -3)]
        self.path_index = 0

    def _update_sprite_frame(self):
        self.frame_index = (self.frame_index + 1) % 3
        if self.state == EventAnimationState.INTERACTING:
            self.current_sprite_key = f"hover_{(self.frame_index % 2) + 1}"
        else:
            self.current_sprite_key = f"fly_{self.frame_index + 1}"

    def get_sprite(self) -> List[str]:
        return self.SPRITES.get(self.current_sprite_key, self.SPRITES["fly_1"])

    def get_color(self) -> str:
        return "blue"


class BubblesAnimator(EventAnimator):
    """Bubbles rising from underwater — particle-based like BreezeAnimator."""

    def __init__(self, playfield_width: int = 60, playfield_height: int = 15):
        super().__init__(
            event_id="bubbles",
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            duration=4.0,
        )
        self.particles: List[Tuple[float, float, str]] = []
        bubble_chars = ["o", "O", ".", "0", "°"]
        # Spawn bubbles from bottom
        spawn_x = playfield_width // 2 + random.randint(-10, 10)
        for _ in range(15):
            self.particles.append((
                spawn_x + random.uniform(-4, 4),
                float(playfield_height - 2 + random.uniform(0, 3)),
                random.choice(bubble_chars),
            ))
        self.frame_duration = 0.1

    def start(self):
        self.state = EventAnimationState.INTERACTING
        self.start_time = time.time()
        self.state_start_time = time.time()

    def update(self, duck_x: int = 30, duck_y: int = 8) -> bool:
        if self.state == EventAnimationState.FINISHED:
            return False
        elapsed = time.time() - self.start_time
        new_particles = []
        for x, y, char in self.particles:
            ny = y - random.uniform(0.2, 0.6)
            nx = x + random.uniform(-0.3, 0.3)
            if ny > 0:
                new_particles.append((nx, ny, char))
        # Spawn new bubbles from bottom
        if elapsed < self.total_duration and random.random() < 0.4:
            spawn_x = self.playfield_width // 2 + random.randint(-8, 8)
            new_particles.append((
                spawn_x + random.uniform(-2, 2),
                float(self.playfield_height - 2),
                random.choice(["o", "O", ".", "0", "°"]),
            ))
        self.particles = new_particles
        if elapsed >= self.total_duration + 1.0 or not self.particles:
            self.state = EventAnimationState.FINISHED
            self.particles = []
            return False
        return True

    def get_sprite(self) -> List[str]:
        return []

    def get_particles(self) -> List[Tuple[int, int, str]]:
        return [(int(x), int(y), c) for x, y, c in self.particles]

    def get_color(self) -> str:
        return "cyan"


class FallingObjectAnimator(EventAnimator):
    """Something falls from above — acorns, pinecones, tomatoes."""

    SPRITES = {
        "fall_1": ["*"],
        "fall_2": ["+"],
        "fall_3": ["o"],
        "impact_1": [
            " * ",
            "*+*",
            " * ",
        ],
        "impact_2": [
            "  .  ",
            ". + .",
            "  .  ",
        ],
    }

    def __init__(self, playfield_width: int = 60, playfield_height: int = 15):
        super().__init__(
            event_id="falling_object",
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            duration=3.0,
        )
        self.x = float(playfield_width // 2 + random.randint(-10, 10))
        self.y = 0.0
        self.target_y = float(playfield_height - 3)
        self.speed = 0.8
        self.frame_duration = 0.12
        self._hit_ground = False

    def start(self):
        self.state = EventAnimationState.ARRIVING
        self.start_time = time.time()
        self.state_start_time = time.time()

    def _setup_arrival_path(self):
        self.path_points = [(self.x, 0), (self.x + random.uniform(-2, 2), self.target_y)]
        self.path_index = 0

    def _update_arriving(self, duck_x: int, duck_y: int):
        self.y += self.speed
        self.x += random.uniform(-0.1, 0.1)
        if self.y >= self.target_y:
            self._hit_ground = True
            self.state = EventAnimationState.INTERACTING
            self._setup_interaction()

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        if elapsed >= 1.0:
            self.state = EventAnimationState.FINISHED

    def _update_sprite_frame(self):
        self.frame_index = (self.frame_index + 1) % 3
        if self._hit_ground:
            self.current_sprite_key = f"impact_{(self.frame_index % 2) + 1}"
        else:
            self.current_sprite_key = f"fall_{self.frame_index + 1}"

    def get_sprite(self) -> List[str]:
        return self.SPRITES.get(self.current_sprite_key, self.SPRITES["fall_1"])

    def get_color(self) -> str:
        return "red" if self._hit_ground else "yellow"


class SquirrelAnimator(EventAnimator):
    """A squirrel dashes across the screen, pauses, then bolts."""

    SPRITES = {
        "run_right_1": [
            " /\\ ",
            "('v')",
            " /|~",
        ],
        "run_right_2": [
            "  /\\",
            "('v')",
            "~|\\ ",
        ],
        "sit_1": [
            " /\\  ",
            "('.')>",
            " /|  ",
        ],
        "sit_2": [
            " /\\  ",
            "(o.o)>",
            " /|  ",
        ],
        "panic_1": [
            "  /\\!",
            "('O')",
            " /|\\ ",
        ],
        "panic_2": [
            "!/\\  ",
            "('O')",
            " /|\\ ",
        ],
    }

    def __init__(self, playfield_width: int = 60, playfield_height: int = 15):
        super().__init__(
            event_id="squirrel",
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            duration=5.0,
        )
        ground = playfield_height - 4
        self.coming_from_right = random.random() < 0.5
        self.x = float(playfield_width + 5) if self.coming_from_right else -5.0
        self.y = float(ground)
        self.speed = 1.0
        self.frame_duration = 0.15

    def _setup_arrival_path(self):
        ground = self.playfield_height - 4
        mid = self.playfield_width // 2 + random.randint(-8, 8)
        self.path_points = [(self.x, self.y), (mid, ground)]
        self.path_index = 0

    def _setup_interaction(self):
        super()._setup_interaction()

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        if elapsed >= 1.5:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    def _setup_leaving_path(self):
        # Squirrel bolts in the opposite direction at high speed
        exit_x = -10.0 if self.coming_from_right else self.playfield_width + 10
        self.path_points = [
            (self.x, self.y),
            (exit_x, self.y - 2),
        ]
        self.path_index = 0
        self.speed = 2.0  # Panic speed!

    def _update_sprite_frame(self):
        self.frame_index = (self.frame_index + 1) % 2
        if self.state == EventAnimationState.ARRIVING:
            self.current_sprite_key = f"run_right_{self.frame_index + 1}"
        elif self.state == EventAnimationState.INTERACTING:
            self.current_sprite_key = f"sit_{self.frame_index + 1}"
        elif self.state == EventAnimationState.LEAVING:
            self.current_sprite_key = f"panic_{self.frame_index + 1}"

    def get_sprite(self) -> List[str]:
        return self.SPRITES.get(self.current_sprite_key, self.SPRITES["sit_1"])

    def get_color(self) -> str:
        if self.state == EventAnimationState.LEAVING:
            return "red"
        return "yellow"


# ---------------------------------------------------------------------------
# New animator classes for extended events
# ---------------------------------------------------------------------------

class FoodAnimator(EventAnimator):
    """Animator for sacred/special food items: the_holy_loaf, baguette_find."""

    SPRITES_MAP = {
        "the_holy_loaf": {
            "idle_1": [
                "  .***. ",
                " * ~~~ *",
                "  '***' ",
            ],
            "idle_2": [
                " .****.  ",
                "* ~~~~ * ",
                " '****'  ",
            ],
        },
        "baguette_find": {
            "idle_1": [
                " ______ ",
                "/      \\",
                "\\______/",
            ],
            "idle_2": [
                "  ______  ",
                " / ~~ ~ \\",
                " \\______/ ",
            ],
        },
    }

    COLORS_MAP = {
        "the_holy_loaf": "yellow",
        "baguette_find": "yellow",
    }

    def __init__(self, playfield_width: int = 60, playfield_height: int = 15,
                 event_id: str = "the_holy_loaf"):
        super().__init__(
            event_id=event_id,
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=float(playfield_width // 2),
            start_y=-3.0,
            duration=7.0,
        )
        self.speed = 0.3
        self.wobble_amplitude = 0.5
        self.wobble_frequency = 2.0
        self.sprites = self.SPRITES_MAP.get(event_id, self.SPRITES_MAP["the_holy_loaf"])
        self._color = self.COLORS_MAP.get(event_id, "yellow")

    def _setup_arrival_path(self):
        cx = self.playfield_width // 2
        cy = self.playfield_height // 2
        self.path_points = [(self.x, self.y), (float(cx), float(cy))]
        self.path_index = 0

    def _setup_interaction(self):
        super()._setup_interaction()

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        # gentle hover
        self.y += math.sin(elapsed * 3) * 0.05
        if elapsed >= 3.0:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    def _setup_leaving_path(self):
        self.path_points = [(self.x, self.y), (self.x, -5.0)]
        self.path_index = 0
        self.speed = 0.5

    def _update_sprite_frame(self):
        self.frame_index = (self.frame_index + 1) % 2

    def get_sprite(self) -> List[str]:
        key = f"idle_{self.frame_index + 1}"
        return self.sprites.get(key, list(self.sprites.values())[0])

    def get_color(self) -> str:
        return self._color


class FallingThingsAnimator(EventAnimator):
    """Animator for things falling from the sky: bread_rain, cherry_blossom."""

    SPRITES_MAP = {
        "bread_rain": {
            "fall_1": [
                " o  o ",
                "  o   ",
                " o  o ",
            ],
            "fall_2": [
                "  o  o",
                " o    ",
                "  o o ",
            ],
        },
        "cherry_blossom": {
            "fall_1": [
                " *  * ",
                "  *   ",
                " *  * ",
            ],
            "fall_2": [
                "  * * ",
                " *    ",
                "  * * ",
            ],
        },
    }

    COLORS_MAP = {
        "bread_rain": "yellow",
        "cherry_blossom": "magenta",
    }

    def __init__(self, playfield_width: int = 60, playfield_height: int = 15,
                 event_id: str = "bread_rain"):
        super().__init__(
            event_id=event_id,
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=float(playfield_width // 2),
            start_y=-2.0,
            duration=6.0,
        )
        self.speed = 0.4
        self.wobble_amplitude = 1.0
        self.wobble_frequency = 3.0
        self.sprites = self.SPRITES_MAP.get(event_id, self.SPRITES_MAP["bread_rain"])
        self._color = self.COLORS_MAP.get(event_id, "yellow")

    def _setup_arrival_path(self):
        cx = self.playfield_width // 2
        self.path_points = [(self.x, self.y), (float(cx), float(self.playfield_height - 2))]
        self.path_index = 0

    def _setup_interaction(self):
        super()._setup_interaction()

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        self.y = max(0.0, self.y + math.sin(elapsed * 4) * 0.1)
        if elapsed >= 3.0:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    def _setup_leaving_path(self):
        self.path_points = [(self.x, self.y), (self.x, float(self.playfield_height + 5))]
        self.path_index = 0

    def _update_sprite_frame(self):
        self.frame_index = (self.frame_index + 1) % 2

    def get_sprite(self) -> List[str]:
        key = f"fall_{self.frame_index + 1}"
        return self.sprites.get(key, list(self.sprites.values())[0])

    def get_color(self) -> str:
        return self._color


class SkyLightAnimator(EventAnimator):
    """Animator for lights/streaks in the sky: aurora_borealis, ball_lightning,
    sun_pillar, shooting_star_wish, meteor_shower."""

    SPRITES_MAP = {
        "aurora_borealis": {
            "glow_1": [
                "~*~*~*~*~",
                " ~*~*~*~ ",
                "  ~*~*~  ",
            ],
            "glow_2": [
                " *~*~*~* ",
                "~*~*~*~*~",
                "  *~*~*  ",
            ],
        },
        "ball_lightning": {
            "glow_1": [
                " .**. ",
                "* ** *",
                " '**' ",
            ],
            "glow_2": [
                " .++. ",
                "+ ++ +",
                " '++' ",
            ],
        },
        "sun_pillar": {
            "glow_1": [
                "  ||  ",
                "  ||  ",
                "  ||  ",
                "  ||  ",
            ],
            "glow_2": [
                "  ||  ",
                " :|:  ",
                "  ||  ",
                "  ||  ",
            ],
        },
        "shooting_star_wish": {
            "glow_1": [
                "        *",
                "      ** ",
                "    **   ",
            ],
            "glow_2": [
                "       * ",
                "     **  ",
                "   **    ",
            ],
        },
        "meteor_shower": {
            "glow_1": [
                " *  *  * ",
                "  \\  \\ \\",
                "   *  *  ",
            ],
            "glow_2": [
                "  *  * * ",
                " \\  \\ \\ ",
                "  *  *   ",
            ],
        },
    }

    COLORS_MAP = {
        "aurora_borealis": "green",
        "ball_lightning": "cyan",
        "sun_pillar": "yellow",
        "shooting_star_wish": "white",
        "meteor_shower": "cyan",
    }

    def __init__(self, playfield_width: int = 60, playfield_height: int = 15,
                 event_id: str = "aurora_borealis"):
        start_x = float(playfield_width + 5)
        start_y = random.uniform(1, 4)
        super().__init__(
            event_id=event_id,
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=start_x,
            start_y=start_y,
            duration=7.0,
        )
        self.speed = 0.7
        self.sprites = self.SPRITES_MAP.get(event_id, self.SPRITES_MAP["aurora_borealis"])
        self._color = self.COLORS_MAP.get(event_id, "white")

    def _setup_arrival_path(self):
        mid_x = self.playfield_width // 2
        self.path_points = [
            (self.x, self.y),
            (float(mid_x), self.y),
        ]
        self.path_index = 0

    def _setup_interaction(self):
        super()._setup_interaction()

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        self.x += math.sin(elapsed * 2) * 0.1
        if elapsed >= 3.0:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    def _setup_leaving_path(self):
        self.path_points = [(self.x, self.y), (-10.0, self.y)]
        self.path_index = 0
        self.speed = 1.0

    def _update_sprite_frame(self):
        self.frame_index = (self.frame_index + 1) % 2

    def get_sprite(self) -> List[str]:
        key = f"glow_{self.frame_index + 1}"
        return self.sprites.get(key, list(self.sprites.values())[0])

    def get_color(self) -> str:
        return self._color


class RainbowAnimator(EventAnimator):
    """Animator for rainbow events: rainbow_double, rainbow_complete, night_rainbow."""

    SPRITES_MAP = {
        "rainbow_double": {
            "arc_1": [
                "  .~~~.  ",
                " /     \\ ",
                " .~~~.   ",
                "/     \\  ",
            ],
            "arc_2": [
                " .~~~.   ",
                "/     \\  ",
                "  .~~~.  ",
                " /     \\ ",
            ],
        },
        "rainbow_complete": {
            "arc_1": [
                "  .=====. ",
                " / r o y \\",
                "|  g b v  |",
            ],
            "arc_2": [
                "  .=====.  ",
                " / R O Y \\ ",
                "|  G B V  | ",
            ],
        },
        "night_rainbow": {
            "arc_1": [
                "  .-----.  ",
                " / . . . \\",
                "|  . . .  |",
            ],
            "arc_2": [
                "  .-----.  ",
                " /  . .  \\ ",
                "|  . . .  | ",
            ],
        },
    }

    COLORS_MAP = {
        "rainbow_double": "cyan",
        "rainbow_complete": "magenta",
        "night_rainbow": "blue",
    }

    def __init__(self, playfield_width: int = 60, playfield_height: int = 15,
                 event_id: str = "rainbow_double"):
        super().__init__(
            event_id=event_id,
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=float(playfield_width + 10),
            start_y=2.0,
            duration=8.0,
        )
        self.speed = 0.4
        self.sprites = self.SPRITES_MAP.get(event_id, self.SPRITES_MAP["rainbow_double"])
        self._color = self.COLORS_MAP.get(event_id, "cyan")

    def _setup_arrival_path(self):
        cx = self.playfield_width // 2
        self.path_points = [(self.x, self.y), (float(cx), 1.0)]
        self.path_index = 0

    def _setup_interaction(self):
        super()._setup_interaction()

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        if elapsed >= 4.0:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    def _setup_leaving_path(self):
        self.path_points = [(self.x, self.y), (self.x, -6.0)]
        self.path_index = 0
        self.speed = 0.3

    def _update_sprite_frame(self):
        self.frame_index = (self.frame_index + 1) % 2

    def get_sprite(self) -> List[str]:
        key = f"arc_{self.frame_index + 1}"
        return self.sprites.get(key, list(self.sprites.values())[0])

    def get_color(self) -> str:
        return self._color


class MoonAnimator(EventAnimator):
    """Animator for moon/celestial body events: full_moon_exp, moonrise_massive,
    eclipse_event, blood_moon_exp, milky_way_visible."""

    SPRITES_MAP = {
        "full_moon_exp": {
            "rise_1": [
                "  ___  ",
                " /   \\ ",
                "|  O  |",
                " \\___/ ",
            ],
            "rise_2": [
                "  ___  ",
                " / * \\ ",
                "|  O  |",
                " \\___/ ",
            ],
        },
        "moonrise_massive": {
            "rise_1": [
                " .----. ",
                "/      \\",
                "|  ()  |",
                "\\      /",
                " '----' ",
            ],
            "rise_2": [
                " .----. ",
                "/ *  * \\",
                "|  ()  |",
                "\\      /",
                " '----' ",
            ],
        },
        "eclipse_event": {
            "rise_1": [
                "  ___  ",
                " /###\\ ",
                "|#####|",
                " \\###/ ",
            ],
            "rise_2": [
                "  ___  ",
                " /## \\ ",
                "|#### |",
                " \\###/ ",
            ],
        },
        "blood_moon_exp": {
            "rise_1": [
                "  ___  ",
                " /ooo\\ ",
                "|ooooo|",
                " \\ooo/ ",
            ],
            "rise_2": [
                "  ___  ",
                " /OOO\\ ",
                "|OOOOO|",
                " \\OOO/ ",
            ],
        },
        "milky_way_visible": {
            "rise_1": [
                " . * . * . ",
                "* . * . * .",
                " . * . * . ",
            ],
            "rise_2": [
                "* . * . * .",
                " . * . * . ",
                "* . * . * .",
            ],
        },
    }

    COLORS_MAP = {
        "full_moon_exp": "white",
        "moonrise_massive": "yellow",
        "eclipse_event": "white",
        "blood_moon_exp": "red",
        "milky_way_visible": "cyan",
    }

    def __init__(self, playfield_width: int = 60, playfield_height: int = 15,
                 event_id: str = "full_moon_exp"):
        super().__init__(
            event_id=event_id,
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=float(playfield_width // 2),
            start_y=float(playfield_height + 3),
            duration=8.0,
        )
        self.speed = 0.25
        self.sprites = self.SPRITES_MAP.get(event_id, self.SPRITES_MAP["full_moon_exp"])
        self._color = self.COLORS_MAP.get(event_id, "white")

    def _setup_arrival_path(self):
        cx = self.playfield_width // 2
        self.path_points = [(self.x, self.y), (float(cx), 2.0)]
        self.path_index = 0

    def _setup_interaction(self):
        super()._setup_interaction()

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        self.x += math.sin(elapsed) * 0.02
        if elapsed >= 4.0:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    def _setup_leaving_path(self):
        self.path_points = [(self.x, self.y), (self.x, -6.0)]
        self.path_index = 0
        self.speed = 0.2

    def _update_sprite_frame(self):
        self.frame_index = (self.frame_index + 1) % 2

    def get_sprite(self) -> List[str]:
        key = f"rise_{self.frame_index + 1}"
        return self.sprites.get(key, list(self.sprites.values())[0])

    def get_color(self) -> str:
        return self._color


class GlowAnimator(EventAnimator):
    """Animator for glowing objects: pond_glow, golden_egg_shimmer,
    glowing_mushroom, will_o_wisp, bioluminescent_insects, algae_bloom_glow,
    bioluminescent_fish."""

    SPRITES_MAP = {
        "pond_glow": {
            "glow_1": [
                " ~.~.~ ",
                "~.~.~.~",
                " ~.~.~ ",
            ],
            "glow_2": [
                ".~.~.~.",
                " ~.~.~ ",
                ".~.~.~.",
            ],
        },
        "golden_egg_shimmer": {
            "glow_1": [
                "  .-.  ",
                " /   \\ ",
                " \\___/ ",
            ],
            "glow_2": [
                "  .*.  ",
                " / * \\ ",
                " \\___/ ",
            ],
        },
        "glowing_mushroom": {
            "glow_1": [
                "  .--.  ",
                " / ** \\ ",
                "   ||   ",
            ],
            "glow_2": [
                "  .--. ",
                " / oo \\",
                "   ||  ",
            ],
        },
        "will_o_wisp": {
            "glow_1": [
                " o ",
                "( )",
                " o ",
            ],
            "glow_2": [
                "  o",
                " ( )",
                "  o",
            ],
        },
        "bioluminescent_insects": {
            "glow_1": [
                " *  .  * ",
                "  .  *   ",
                " *  .  * ",
            ],
            "glow_2": [
                "  .  *  .",
                " *  .  * ",
                "  .  *   ",
            ],
        },
        "algae_bloom_glow": {
            "glow_1": [
                "~*~*~*~",
                "*~*~*~*",
                "~*~*~*~",
            ],
            "glow_2": [
                "*~*~*~*",
                "~*~*~*~",
                "*~*~*~*",
            ],
        },
        "bioluminescent_fish": {
            "glow_1": [
                " ><((*> ",
            ],
            "glow_2": [
                " ><((o> ",
            ],
        },
    }

    COLORS_MAP = {
        "pond_glow": "cyan",
        "golden_egg_shimmer": "yellow",
        "glowing_mushroom": "green",
        "will_o_wisp": "green",
        "bioluminescent_insects": "cyan",
        "algae_bloom_glow": "green",
        "bioluminescent_fish": "cyan",
    }

    def __init__(self, playfield_width: int = 60, playfield_height: int = 15,
                 event_id: str = "pond_glow"):
        pos_y = float(playfield_height - 3) if event_id in (
            "pond_glow", "algae_bloom_glow", "bioluminescent_fish"
        ) else float(playfield_height // 2)
        super().__init__(
            event_id=event_id,
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=float(playfield_width // 2),
            start_y=pos_y,
            duration=7.0,
        )
        self.speed = 0.0  # mostly stationary
        self.sprites = self.SPRITES_MAP.get(event_id, self.SPRITES_MAP["pond_glow"])
        self._color = self.COLORS_MAP.get(event_id, "cyan")
        self._appeared = False

    def _setup_arrival_path(self):
        # appear in-place
        self.path_points = [(self.x, self.y)]
        self.path_index = 0

    def _setup_interaction(self):
        super()._setup_interaction()

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        # gentle pulse movement
        self.y += math.sin(elapsed * 3) * 0.03
        if elapsed >= 3.5:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    def _setup_leaving_path(self):
        self.path_points = [(self.x, self.y)]
        self.path_index = 0

    def _update_leaving(self):
        # fade-out simulated by finishing immediately
        self.state = EventAnimationState.FINISHED

    def _update_sprite_frame(self):
        self.frame_index = (self.frame_index + 1) % 2

    def get_sprite(self) -> List[str]:
        key = f"glow_{self.frame_index + 1}"
        return self.sprites.get(key, list(self.sprites.values())[0])

    def get_color(self) -> str:
        return self._color


class GreenFlashAnimator(EventAnimator):
    """Animator for sunset_green_flash."""

    def __init__(self, playfield_width: int = 60, playfield_height: int = 15):
        super().__init__(
            event_id="sunset_green_flash",
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=float(playfield_width // 2),
            start_y=float(playfield_height - 2),
            duration=4.0,
        )
        self.speed = 0.0

    def _setup_arrival_path(self):
        self.path_points = [(self.x, self.y)]
        self.path_index = 0

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        if elapsed >= 1.5:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    def _setup_leaving_path(self):
        self.path_points = [(self.x, self.y)]
        self.path_index = 0

    def _update_leaving(self):
        self.state = EventAnimationState.FINISHED

    def _update_sprite_frame(self):
        self.frame_index = (self.frame_index + 1) % 2

    def get_sprite(self) -> List[str]:
        if self.frame_index == 0:
            return [
                "          ",
                "=*=*=*=*=*",
                "          ",
            ]
        return [
            "          ",
            "*=*=*=*=*=",
            "          ",
        ]

    def get_color(self) -> str:
        return "green"


class PuffUpAnimator(EventAnimator):
    """Animator for thunder_puffup - feathers puff up from thunder."""

    def __init__(self, playfield_width: int = 60, playfield_height: int = 15):
        super().__init__(
            event_id="thunder_puffup",
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=float(playfield_width // 2),
            start_y=1.0,
            duration=5.0,
        )
        self.speed = 0.0

    def _setup_arrival_path(self):
        self.path_points = [(self.x, self.y)]
        self.path_index = 0

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        if elapsed >= 2.0:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    def _setup_leaving_path(self):
        self.path_points = [(self.x, self.y)]
        self.path_index = 0

    def _update_leaving(self):
        self.state = EventAnimationState.FINISHED

    def _update_sprite_frame(self):
        self.frame_index = (self.frame_index + 1) % 2

    def get_sprite(self) -> List[str]:
        if self.frame_index == 0:
            return [
                " _/\\/\\_ ",
                "| BOOM! |",
                " \\/\\/\\/ ",
            ]
        return [
            " \\/\\/\\/ ",
            "| KRAK! |",
            " _/\\/\\_ ",
        ]

    def get_color(self) -> str:
        return "yellow"


class UFOAnimator(EventAnimator):
    """Animator for ufo_landing."""

    def __init__(self, playfield_width: int = 60, playfield_height: int = 15):
        super().__init__(
            event_id="ufo_landing",
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=float(playfield_width // 2),
            start_y=-4.0,
            duration=8.0,
        )
        self.speed = 0.3
        self.wobble_amplitude = 0.8
        self.wobble_frequency = 2.0

    def _setup_arrival_path(self):
        cx = self.playfield_width // 2
        cy = self.playfield_height // 2
        self.path_points = [
            (self.x, self.y),
            (float(cx) + 5, float(cy) - 2),
            (float(cx), float(cy)),
        ]
        self.path_index = 0

    def _setup_interaction(self):
        super()._setup_interaction()

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        self.x += math.sin(elapsed * 2) * 0.15
        if elapsed >= 3.5:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    def _setup_leaving_path(self):
        self.path_points = [(self.x, self.y), (self.x + 10, -6.0)]
        self.path_index = 0
        self.speed = 0.8

    def _update_sprite_frame(self):
        self.frame_index = (self.frame_index + 1) % 2

    def get_sprite(self) -> List[str]:
        if self.frame_index == 0:
            return [
                "   ___   ",
                " _/   \\_ ",
                "|__-o-__|",
                "   |||   ",
            ]
        return [
            "   ___   ",
            " _/ * \\_ ",
            "|__-O-__|",
            "   |!|   ",
        ]

    def get_color(self) -> str:
        return "green"


class GhostDuckAnimator(EventAnimator):
    """Animator for ghost_duck - a translucent ghost duck drifts through."""

    def __init__(self, playfield_width: int = 60, playfield_height: int = 15):
        side = random.choice(["left", "right"])
        sx = -5.0 if side == "left" else float(playfield_width + 5)
        super().__init__(
            event_id="ghost_duck",
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=sx,
            start_y=float(playfield_height // 2),
            duration=7.0,
        )
        self.speed = 0.35
        self.wobble_amplitude = 1.0
        self.wobble_frequency = 1.5
        self._from_left = (side == "left")

    def _setup_arrival_path(self):
        cx = self.playfield_width // 2
        cy = self.playfield_height // 2
        self.path_points = [(self.x, self.y), (float(cx), float(cy))]
        self.path_index = 0

    def _setup_interaction(self):
        super()._setup_interaction()

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        self.y += math.sin(elapsed * 2) * 0.08
        if elapsed >= 3.0:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    def _setup_leaving_path(self):
        exit_x = float(self.playfield_width + 10) if self._from_left else -10.0
        self.path_points = [(self.x, self.y), (exit_x, self.y - 2)]
        self.path_index = 0
        self.speed = 0.4

    def _update_sprite_frame(self):
        self.frame_index = (self.frame_index + 1) % 2

    def get_sprite(self) -> List[str]:
        if self.frame_index == 0:
            return [
                " .--. ",
                "(o  o)",
                " \\~~/ ",
                "  \\/  ",
            ]
        return [
            " .--. ",
            "(o  o)",
            " /~~\\ ",
            "  /\\  ",
        ]

    def get_color(self) -> str:
        return "white"


class PortalAnimator(EventAnimator):
    """Animator for pond_portal - a swirling portal opens on the pond."""

    def __init__(self, playfield_width: int = 60, playfield_height: int = 15):
        super().__init__(
            event_id="pond_portal",
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=float(playfield_width // 2),
            start_y=float(playfield_height - 3),
            duration=7.0,
        )
        self.speed = 0.0

    def _setup_arrival_path(self):
        self.path_points = [(self.x, self.y)]
        self.path_index = 0

    def _setup_interaction(self):
        super()._setup_interaction()

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        if elapsed >= 3.5:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    def _setup_leaving_path(self):
        self.path_points = [(self.x, self.y)]
        self.path_index = 0

    def _update_leaving(self):
        self.state = EventAnimationState.FINISHED

    def _update_sprite_frame(self):
        self.frame_index = (self.frame_index + 1) % 2

    def get_sprite(self) -> List[str]:
        if self.frame_index == 0:
            return [
                " .oOo. ",
                "( @  @ )",
                " 'oOo' ",
            ]
        return [
            " .OoO. ",
            "( @  @ )",
            " 'OoO' ",
        ]

    def get_color(self) -> str:
        return "magenta"


class FloatingAnimator(EventAnimator):
    """Animator for objects floating in the sky: hot_air_balloon, frozen_bubble."""

    SPRITES_MAP = {
        "hot_air_balloon": {
            "float_1": [
                " .--. ",
                "/    \\",
                "\\    /",
                " |__|",
            ],
            "float_2": [
                " .--. ",
                "/ ** \\",
                "\\    /",
                " |__|",
            ],
        },
        "frozen_bubble": {
            "float_1": [
                " .-. ",
                "( * )",
                " '-' ",
            ],
            "float_2": [
                " .-. ",
                "(  *)",
                " '-' ",
            ],
        },
    }

    COLORS_MAP = {
        "hot_air_balloon": "red",
        "frozen_bubble": "cyan",
    }

    def __init__(self, playfield_width: int = 60, playfield_height: int = 15,
                 event_id: str = "hot_air_balloon"):
        side = random.choice(["left", "right"])
        sx = -5.0 if side == "left" else float(playfield_width + 5)
        super().__init__(
            event_id=event_id,
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=sx,
            start_y=random.uniform(1, 4),
            duration=8.0,
        )
        self.speed = 0.3
        self.wobble_amplitude = 0.5
        self.wobble_frequency = 1.5
        self._from_left = (side == "left")
        self.sprites = self.SPRITES_MAP.get(event_id, self.SPRITES_MAP["hot_air_balloon"])
        self._color = self.COLORS_MAP.get(event_id, "white")

    def _setup_arrival_path(self):
        cx = self.playfield_width // 2
        self.path_points = [(self.x, self.y), (float(cx), self.y)]
        self.path_index = 0

    def _setup_interaction(self):
        super()._setup_interaction()

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        self.y += math.sin(elapsed * 1.5) * 0.04
        if elapsed >= 3.0:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    def _setup_leaving_path(self):
        exit_x = float(self.playfield_width + 10) if self._from_left else -10.0
        self.path_points = [(self.x, self.y), (exit_x, self.y - 1)]
        self.path_index = 0
        self.speed = 0.3

    def _update_sprite_frame(self):
        self.frame_index = (self.frame_index + 1) % 2

    def get_sprite(self) -> List[str]:
        key = f"float_{self.frame_index + 1}"
        return self.sprites.get(key, list(self.sprites.values())[0])

    def get_color(self) -> str:
        return self._color


class FireflyAnimator(EventAnimator):
    """Animator for firefly events: firefly_show, fireflies_sync."""

    SPRITES_MAP = {
        "firefly_show": {
            "blink_1": [
                " *  .  * ",
                ".  *  .  ",
                " *  .  * ",
            ],
            "blink_2": [
                ".  *  .  ",
                " *  .  * ",
                ".  *  .  ",
            ],
        },
        "fireflies_sync": {
            "blink_1": [
                " *  *  * ",
                " *  *  * ",
                " *  *  * ",
            ],
            "blink_2": [
                "         ",
                "         ",
                "         ",
            ],
        },
    }

    COLORS_MAP = {
        "firefly_show": "yellow",
        "fireflies_sync": "yellow",
    }

    def __init__(self, playfield_width: int = 60, playfield_height: int = 15,
                 event_id: str = "firefly_show"):
        super().__init__(
            event_id=event_id,
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=float(playfield_width // 2),
            start_y=float(playfield_height // 2),
            duration=7.0,
        )
        self.speed = 0.0
        self.sprites = self.SPRITES_MAP.get(event_id, self.SPRITES_MAP["firefly_show"])
        self._color = self.COLORS_MAP.get(event_id, "yellow")

    def _setup_arrival_path(self):
        self.path_points = [(self.x, self.y)]
        self.path_index = 0

    def _setup_interaction(self):
        super()._setup_interaction()

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        if elapsed >= 3.5:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    def _setup_leaving_path(self):
        self.path_points = [(self.x, self.y)]
        self.path_index = 0

    def _update_leaving(self):
        self.state = EventAnimationState.FINISHED

    def _update_sprite_frame(self):
        self.frame_index = (self.frame_index + 1) % 2

    def get_sprite(self) -> List[str]:
        key = f"blink_{self.frame_index + 1}"
        return self.sprites.get(key, list(self.sprites.values())[0])

    def get_color(self) -> str:
        return self._color


class ButterflySwarmAnimator(EventAnimator):
    """Animator for butterfly_migration_exp and butterfly_mistake."""

    SPRITES_MAP = {
        "butterfly_migration_exp": {
            "fly_1": [
                "\\/ \\/ \\/",
                " /\\ /\\ ",
                "\\/ \\/ \\/",
            ],
            "fly_2": [
                " /\\ /\\ ",
                "\\/ \\/ \\/",
                " /\\ /\\ ",
            ],
        },
        "butterfly_mistake": {
            "fly_1": [
                " \\/ ",
                " /\\ ",
            ],
            "fly_2": [
                " -- ",
                " -- ",
            ],
        },
    }

    COLORS_MAP = {
        "butterfly_migration_exp": "magenta",
        "butterfly_mistake": "cyan",
    }

    def __init__(self, playfield_width: int = 60, playfield_height: int = 15,
                 event_id: str = "butterfly_migration_exp"):
        side = random.choice(["left", "right"])
        sx = -8.0 if side == "left" else float(playfield_width + 8)
        super().__init__(
            event_id=event_id,
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=sx,
            start_y=random.uniform(2, playfield_height - 3),
            duration=7.0,
        )
        self.speed = 0.5
        self.wobble_amplitude = 1.2
        self.wobble_frequency = 3.0
        self._from_left = (side == "left")
        self.sprites = self.SPRITES_MAP.get(event_id, self.SPRITES_MAP["butterfly_migration_exp"])
        self._color = self.COLORS_MAP.get(event_id, "magenta")

    def _setup_arrival_path(self):
        cx = self.playfield_width // 2
        cy = self.playfield_height // 2
        self.path_points = [(self.x, self.y), (float(cx), float(cy))]
        self.path_index = 0

    def _setup_interaction(self):
        super()._setup_interaction()

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        self.x += math.sin(elapsed * 3) * 0.1
        self.y += math.cos(elapsed * 2) * 0.08
        if elapsed >= 2.5:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    def _setup_leaving_path(self):
        exit_x = float(self.playfield_width + 10) if self._from_left else -10.0
        self.path_points = [(self.x, self.y), (exit_x, self.y - 2)]
        self.path_index = 0
        self.speed = 0.6

    def _update_sprite_frame(self):
        self.frame_index = (self.frame_index + 1) % 2

    def get_sprite(self) -> List[str]:
        key = f"fly_{self.frame_index + 1}"
        return self.sprites.get(key, list(self.sprites.values())[0])

    def get_color(self) -> str:
        return self._color


class TurtleAnimator(EventAnimator):
    """Animator for turtle_encounter_exp - a slow turtle passing through."""

    def __init__(self, playfield_width: int = 60, playfield_height: int = 15):
        super().__init__(
            event_id="turtle_encounter_exp",
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=-5.0,
            start_y=float(playfield_height - 2),
            duration=10.0,
        )
        self.speed = 0.15

    def _setup_arrival_path(self):
        cx = self.playfield_width // 2
        self.path_points = [(self.x, self.y), (float(cx), self.y)]
        self.path_index = 0

    def _setup_interaction(self):
        super()._setup_interaction()

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        if elapsed >= 2.5:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    def _setup_leaving_path(self):
        self.path_points = [(self.x, self.y), (float(self.playfield_width + 10), self.y)]
        self.path_index = 0
        self.speed = 0.15

    def _update_sprite_frame(self):
        self.frame_index = (self.frame_index + 1) % 2

    def get_sprite(self) -> List[str]:
        if self.frame_index == 0:
            return [
                "  ___  ",
                "/(o.o)\\",
                "  ^^^  ",
            ]
        return [
            "  ___  ",
            "/(o_o)\\",
            "  ^^^  ",
        ]

    def get_color(self) -> str:
        return "green"


class FireworksAnimator(EventAnimator):
    """Animator for fireworks_distant - fireworks bursting in the sky."""

    def __init__(self, playfield_width: int = 60, playfield_height: int = 15):
        super().__init__(
            event_id="fireworks_distant",
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=float(playfield_width // 2),
            start_y=float(playfield_height),
            duration=6.0,
        )
        self.speed = 0.6
        self._burst = False

    def _setup_arrival_path(self):
        cx = self.playfield_width // 2
        self.path_points = [(self.x, self.y), (float(cx), 2.0)]
        self.path_index = 0

    def _setup_interaction(self):
        super()._setup_interaction()
        self._burst = True

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        if elapsed >= 2.5:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    def _setup_leaving_path(self):
        self.path_points = [(self.x, self.y)]
        self.path_index = 0

    def _update_leaving(self):
        self.state = EventAnimationState.FINISHED

    def _update_sprite_frame(self):
        self.frame_index = (self.frame_index + 1) % 2

    def get_sprite(self) -> List[str]:
        if not self._burst:
            return [
                " | ",
                " | ",
            ]
        if self.frame_index == 0:
            return [
                " \\|/ ",
                "-- --",
                " /|\\ ",
            ]
        return [
            " * * ",
            "*   *",
            " * * ",
        ]

    def get_color(self) -> str:
        colors = ["red", "yellow", "magenta", "cyan"]
        return colors[self.frame_index % len(colors)]


class IcePalaceAnimator(EventAnimator):
    """Animator for ice_palace - ice forms into castle shapes."""

    def __init__(self, playfield_width: int = 60, playfield_height: int = 15):
        super().__init__(
            event_id="ice_palace",
            playfield_width=playfield_width,
            playfield_height=playfield_height,
            start_x=float(playfield_width // 2),
            start_y=float(playfield_height - 3),
            duration=7.0,
        )
        self.speed = 0.0
        self._stage = 0

    def _setup_arrival_path(self):
        self.path_points = [(self.x, self.y)]
        self.path_index = 0

    def _setup_interaction(self):
        super()._setup_interaction()

    def _update_interacting(self, duck_x: int, duck_y: int):
        elapsed = time.time() - self.state_start_time
        self._stage = min(2, int(elapsed))
        if elapsed >= 3.5:
            self.state = EventAnimationState.LEAVING
            self._setup_leaving_path()

    def _setup_leaving_path(self):
        self.path_points = [(self.x, self.y)]
        self.path_index = 0

    def _update_leaving(self):
        self.state = EventAnimationState.FINISHED

    def _update_sprite_frame(self):
        self.frame_index = (self.frame_index + 1) % 2

    def get_sprite(self) -> List[str]:
        if self._stage == 0:
            return [
                "  /\\  ",
                " /  \\ ",
            ]
        if self._stage == 1:
            return [
                "  /\\  ",
                " /  \\ ",
                "|    |",
                "|    |",
            ]
        return [
            " /\\/\\ ",
            "/    \\",
            "| [] |",
            "|____|",
        ]

    def get_color(self) -> str:
        return "cyan"


# ---------------------------------------------------------------------------
# Scene-based animator imports
# ---------------------------------------------------------------------------
from ui.generic_animators import (
    CreatureSceneAnimator,
    FoodSceneAnimator,
    ObjectSceneAnimator,
    HumanSceneAnimator,
    CelestialSceneAnimator,
    PropSceneAnimator,
    VehicleSceneAnimator,
    WeatherSceneAnimator,
    ParticleSceneAnimator,
    AmbientSceneAnimator,
)


# ---------------------------------------------------------------------------
# Factory function — every event gets an animation
# ---------------------------------------------------------------------------
def create_event_animator(event_id, playfield_width=60, playfield_height=15):
    """Create the appropriate animator for an event.

    First checks for hand-crafted specific animators, then falls back to
    generic animators organised by category.  If the event is completely
    unknown a subtle sparkle is returned so *nothing* is ever without
    animation.
    """
    w, h = playfield_width, playfield_height

    # ------------------------------------------------------------------
    # 1. Specific / hand-crafted animators (original mappings preserved)
    # ------------------------------------------------------------------
    specific = {
        "butterfly": ButterflyAnimator,
        "bird_friend": BirdAnimator,
        "another_duck": DuckVisitorAnimator,
        "found_shiny": ShinyObjectAnimator,
        "nice_breeze": BreezeAnimator,
        "found_crumb": CrumbAnimator,
        "loud_noise": LoudNoiseAnimator,
        "bad_dream": lambda w, h: DreamCloudAnimator(w, h, is_bad=True),
        # Area-specific
        "lily_pad": LilyPadAnimator,
        "ripple": RippleAnimator,
        "frog_hop": FrogAnimator,
        "dragonfly": DragonflyAnimator,
        "bubbles": BubblesAnimator,
        "falling_object": FallingObjectAnimator,
        "squirrel": SquirrelAnimator,
        # Food / Bread themed
        "the_holy_loaf": lambda w, h: FoodAnimator(w, h, event_id="the_holy_loaf"),
        "baguette_find": lambda w, h: FoodAnimator(w, h, event_id="baguette_find"),
        "bread_rain": lambda w, h: FallingThingsAnimator(w, h, event_id="bread_rain"),
        # Weather / Sky
        "thunder_puffup": PuffUpAnimator,
        "rainbow_double": lambda w, h: RainbowAnimator(w, h, event_id="rainbow_double"),
        "aurora_borealis": lambda w, h: SkyLightAnimator(w, h, event_id="aurora_borealis"),
        "ball_lightning": lambda w, h: SkyLightAnimator(w, h, event_id="ball_lightning"),
        "sun_pillar": lambda w, h: SkyLightAnimator(w, h, event_id="sun_pillar"),
        "rainbow_complete": lambda w, h: RainbowAnimator(w, h, event_id="rainbow_complete"),
        "night_rainbow": lambda w, h: RainbowAnimator(w, h, event_id="night_rainbow"),
        # Creatures
        "turtle_encounter_exp": TurtleAnimator,
        "butterfly_mistake": lambda w, h: ButterflySwarmAnimator(w, h, event_id="butterfly_mistake"),
        "firefly_show": lambda w, h: FireflyAnimator(w, h, event_id="firefly_show"),
        "butterfly_migration_exp": lambda w, h: ButterflySwarmAnimator(w, h, event_id="butterfly_migration_exp"),
        "bioluminescent_insects": lambda w, h: GlowAnimator(w, h, event_id="bioluminescent_insects"),
        "bioluminescent_fish": lambda w, h: GlowAnimator(w, h, event_id="bioluminescent_fish"),
        # Celestial
        "shooting_star_wish": lambda w, h: SkyLightAnimator(w, h, event_id="shooting_star_wish"),
        "full_moon_exp": lambda w, h: MoonAnimator(w, h, event_id="full_moon_exp"),
        "eclipse_event": lambda w, h: MoonAnimator(w, h, event_id="eclipse_event"),
        "sunset_green_flash": GreenFlashAnimator,
        "moonrise_massive": lambda w, h: MoonAnimator(w, h, event_id="moonrise_massive"),
        "milky_way_visible": lambda w, h: MoonAnimator(w, h, event_id="milky_way_visible"),
        "blood_moon_exp": lambda w, h: MoonAnimator(w, h, event_id="blood_moon_exp"),
        # Supernatural / Rare
        "ufo_landing": UFOAnimator,
        "ghost_duck": GhostDuckAnimator,
        "meteor_shower": lambda w, h: SkyLightAnimator(w, h, event_id="meteor_shower"),
        "will_o_wisp": lambda w, h: GlowAnimator(w, h, event_id="will_o_wisp"),
        "pond_glow": lambda w, h: GlowAnimator(w, h, event_id="pond_glow"),
        "golden_egg_shimmer": lambda w, h: GlowAnimator(w, h, event_id="golden_egg_shimmer"),
        "pond_portal": PortalAnimator,
        "glowing_mushroom": lambda w, h: GlowAnimator(w, h, event_id="glowing_mushroom"),
        # Nature
        "cherry_blossom": lambda w, h: FallingThingsAnimator(w, h, event_id="cherry_blossom"),
        "hot_air_balloon": lambda w, h: FloatingAnimator(w, h, event_id="hot_air_balloon"),
        "fireworks_distant": FireworksAnimator,
        # Ice / Weather Special
        "frozen_bubble": lambda w, h: FloatingAnimator(w, h, event_id="frozen_bubble"),
        "ice_palace": IcePalaceAnimator,
        "algae_bloom_glow": lambda w, h: GlowAnimator(w, h, event_id="algae_bloom_glow"),
        "fireflies_sync": lambda w, h: FireflyAnimator(w, h, event_id="fireflies_sync"),
    }

    if event_id in specific:
        creator = specific[event_id]
        return creator(w, h)

    # ------------------------------------------------------------------
    # 2. Generic animators — organised by category
    # ------------------------------------------------------------------

    # --- FOOD EVENTS ---------------------------------------------------
    food_events = {
        # event_id: (food_sprite, color, appear_style)
        "forgotten_bread": ("bread_loaf", "yellow", "discover"),
        "breadcrumb_trail": ("breadcrumbs", "yellow", "discover"),
        "soggy_bread": ("bread_loaf", "cyan", "drop"),
        "crouton_discovery": ("crouton", "yellow", "discover"),
        "human_eating_bread": ("bread_loaf", "white", "throw"),
        "pizza_crust": ("pizza_crust", "yellow", "discover"),
        "seed_jackpot": ("seed_pile", "yellow", "discover"),
        "stolen_chip": ("chip", "yellow", "throw"),
        "mystery_food": ("cookie", "magenta", "discover"),
        "pea_discovery": ("seed_pile", "green", "discover"),
        "corn_kernel": ("corn", "yellow", "discover"),
        "lettuce_confusion": ("seed_pile", "green", "discover"),
        "grape_chase": ("grape", "magenta", "throw"),
        "toast_fragment": ("bread_loaf", "yellow", "drop"),
        "worm_surprise": ("noodle", "green", "discover"),
        "bird_feeder_raid": ("seed_pile", "yellow", "throw"),
        "underwater_snack": ("breadcrumbs", "cyan", "discover"),
        "bread_dream": ("golden_bread", "yellow", "discover"),
        "food_sharing_refusal": ("bread_loaf", "red", "throw"),
        "acorn_toy": ("acorn", "yellow", "discover"),
        "gourmet_weed": ("seed_pile", "green", "discover"),
        "pretzel_find": ("pretzel", "yellow", "discover"),
        "cheese_cracker": ("crouton", "yellow", "discover"),
        "popcorn_windfall": ("popcorn", "white", "drop"),
        "sandwich_nearby": ("sandwich", "yellow", "discover"),
        "apple_encounter": ("apple", "red", "discover"),
        "fish_food_theft": ("seed_pile", "cyan", "throw"),
        "donut_fragment": ("donut", "yellow", "discover"),
        "rice_scattered": ("breadcrumbs", "white", "drop"),
        "muffin_top": ("muffin", "yellow", "discover"),
        "noodle_strand": ("noodle", "yellow", "discover"),
        "waffle_piece": ("waffle", "yellow", "discover"),
        "cereal_spill": ("breadcrumbs", "yellow", "drop"),
        "bread_in_eye": ("bread_loaf", "yellow", "throw"),
        "bread_thrown_far": ("bread_loaf", "yellow", "throw"),
        "bread_share_stranger": ("bread_loaf", "yellow", "throw"),
        "bread_museum_fantasy": ("golden_bread", "magenta", "discover"),
        "bread_fossils": ("bread_loaf", "yellow", "discover"),
        "bread_satellite": ("bread_loaf", "cyan", "throw"),
        "bread_mirage": ("golden_bread", "magenta", "discover"),
        "golden_breadcrumb": ("golden_bread", "yellow", "discover"),
        "ancient_bread": ("baguette", "yellow", "discover"),
    }
    if event_id in food_events:
        food_name, color, style = food_events[event_id]
        return FoodSceneAnimator(event_id, w, h, food_name=food_name, color=color, appear_style=style)

    # --- CREATURE EVENTS -----------------------------------------------
    creature_events = {
        # event_id: (creature_sprite, color, behavior, enter_from, y_zone)
        "friendly_frog": ("frog", "green", "hop", "random", "ground"),
        "visiting_ladybug": ("ladybug", "red", "fly", "random", "mid"),
        "ant_parade": ("ant", "green", "crawl", "left", "ground"),
        "fish_stare_off": ("fish", "cyan", "swim", "right", "water"),
        "pigeon_judgement": ("bird_flying", "white", "fly", "right", "sky"),
        "bug_in_face": ("beetle", "yellow", "fly", "right", "mid"),
        "worm_surface": ("worm", "green", "crawl", "left", "ground"),
        "catfish_surface": ("fish", "cyan", "swim", "right", "water"),
        "curious_squirrel": ("squirrel", "yellow", "hop", "right", "ground"),
        "turtle_encounter": ("turtle", "green", "walk", "left", "ground"),
        "flock_overhead": ("bird_flying", "white", "fly", "right", "sky"),
        "visiting_heron": ("heron", "blue", "fly", "right", "ground"),
        "crow_gift": ("crow", "white", "fly", "left", "sky"),
        "baby_ducks": ("baby_duck", "yellow", "walk", "left", "ground"),
        "baby_ducks_passing": ("baby_duck", "yellow", "walk", "right", "ground"),
        "visiting_owl": ("owl", "white", "fly", "right", "sky"),
        "dragonfly_landing": ("dragonfly", "cyan", "fly", "random", "mid"),
        "dragonfly_chase_exp": ("dragonfly", "cyan", "swoop", "random", "mid"),
        "frog_chorus": ("frog", "green", "hop", "left", "ground"),
        "frog_duet": ("frog", "green", "hop", "right", "ground"),
        "caterpillar_watch": ("caterpillar", "green", "crawl", "left", "ground"),
        "spider_architect": ("spider", "white", "crawl", "right", "mid"),
        "robin_argument": ("robin", "red", "fly", "random", "sky"),
        "crow_watching": ("crow", "white", "fly", "left", "sky"),
        "snail_race": ("snail", "green", "crawl", "left", "ground"),
        "bee_flower_show": ("bee", "yellow", "fly", "random", "mid"),
        "moth_confusion": ("moth", "white", "fly", "random", "mid"),
        "heron_encounter": ("heron", "blue", "walk", "right", "ground"),
        "goose_intimidation": ("goose", "white", "walk", "left", "ground"),
        "pelican_stare": ("pelican", "white", "fly", "right", "ground"),
        "kingfisher_dive": ("kingfisher", "cyan", "swoop", "right", "sky"),
        "crab_encounter": ("crab", "red", "crawl", "left", "ground"),
        "hedgehog_visit": ("hedgehog", "yellow", "walk", "right", "ground"),
        "swan_in_distance": ("swan", "white", "swim", "left", "water"),
        "deer_sighting": ("deer", "yellow", "walk", "right", "ground"),
        "fox_distant": ("fox", "red", "sneak", "right", "ground"),
        "bat_swoops": ("bat", "white", "swoop", "random", "sky"),
        "peacock_jealousy": ("peacock", "magenta", "walk", "left", "ground"),
        "squirrel_staredown": ("squirrel", "yellow", "hop", "right", "ground"),
        "cat_staredown": ("cat", "white", "sneak", "right", "ground"),
        "sleeping_cat": ("cat", "white", "walk", "left", "ground"),
        "hawk_shadow_pass": ("hawk", "white", "swoop", "right", "sky"),
        "rabbit_sprint": ("rabbit", "white", "hop", "left", "ground"),
        "raccoon_night": ("raccoon", "white", "sneak", "right", "ground"),
        "dog_encounter_exp": ("dog", "yellow", "walk", "right", "ground"),
        "mole_hill_exp": ("mole", "green", "crawl", "left", "ground"),
        "earthworm_rain": ("earthworm", "green", "crawl", "left", "ground"),
        "worm_standoff": ("worm", "green", "crawl", "right", "ground"),
        "worm_escape": ("worm", "green", "crawl", "left", "ground"),
        "caterpillar_on_nose": ("caterpillar", "green", "crawl", "right", "mid"),
        "singing_frog_choir": ("frog", "green", "hop", "left", "ground"),
        "fish_smile": ("fish", "cyan", "swim", "right", "water"),
        "fish_splashing_fight": ("fish", "cyan", "swim", "left", "water"),
        "fish_tornado": ("fish", "cyan", "swim", "random", "water"),
        "butterfly_migration": ("ladybug", "magenta", "fly", "right", "sky"),
        "butterfly_migration_solo": ("moth", "magenta", "fly", "left", "sky"),
        "dragonfly_escort": ("dragonfly", "cyan", "fly", "random", "mid"),
        "heron_flyover": ("heron", "blue", "fly", "right", "sky"),
        "owl_stare": ("owl", "white", "fly", "left", "sky"),
        "owl_conversation": ("owl", "white", "fly", "right", "sky"),
        "owl_eyes": ("owl", "yellow", "fly", "left", "sky"),
        "owl_pellet_find": ("owl", "white", "fly", "right", "sky"),
        "fox_trot_past": ("fox", "red", "walk", "right", "ground"),
        "barn_owl_face": ("owl", "white", "fly", "left", "sky"),
        "spider_balloon": ("spider", "white", "float", "random", "sky"),
        "spider_web_hammock": ("spider", "white", "crawl", "left", "mid"),
        "walking_stick_insect": ("stick_insect", "green", "crawl", "left", "ground"),
        "water_strider_walk": ("water_strider", "cyan", "crawl", "right", "water"),
        "iridescent_beetle": ("beetle", "magenta", "crawl", "right", "ground"),
        "coyote_howl": ("fox", "yellow", "walk", "right", "ground"),
        "tree_frog_call": ("frog", "green", "hop", "left", "ground"),
        "upside_down_beetle": ("beetle", "green", "crawl", "left", "ground"),
        "woodpecker_percussion": ("woodpecker", "red", "fly", "right", "sky"),
        "woodpecker_rhythm": ("woodpecker", "red", "fly", "left", "sky"),
        "flash_mob_birds": ("bird_flying", "white", "fly", "random", "sky"),
        "ladybug_landing": ("ladybug", "red", "fly", "random", "mid"),
        "ant_carrying_food": ("ant", "green", "crawl", "left", "ground"),
        "witch_cat": ("cat", "magenta", "sneak", "right", "ground"),
        "hiccup_scare_fish": ("fish", "cyan", "swim", "right", "water"),
        "wrong_end_fish": ("fish", "cyan", "swim", "left", "water"),
        "fish_splash": ("fish", "cyan", "swim", "random", "water"),
        "mosquito_assault": ("mosquito", "red", "fly", "random", "mid"),
        "bigfoot_glimpse": ("deer", "green", "walk", "right", "ground"),
        "venus_flytrap": ("frog", "green", "crawl", "left", "ground"),
        "sunflower_turning": ("ladybug", "yellow", "float", "right", "mid"),
        "toad_wisdom": ("toad", "green", "hop", "left", "ground"),
        "bird_v_formation": ("bird_flying", "white", "fly", "right", "sky"),
    }
    if event_id in creature_events:
        creature_name, color, behavior, enter_from, y_zone = creature_events[event_id]
        return CreatureSceneAnimator(event_id, w, h, creature_name=creature_name,
                                     color=color, behavior=behavior,
                                     enter_from=enter_from, y_zone=y_zone)

    # --- WEATHER EVENTS ------------------------------------------------
    weather_events = {
        "sunny": ("sun", "yellow"),
        "rain": ("rain", "cyan"),
        "heat_nap": ("sun", "yellow"),
        "cool_puddle": ("rain", "cyan"),
        "frozen_beak": ("snow", "cyan"),
        "snow_discovery": ("snow", "white"),
        "mud_splash": ("rain", "green"),
        "storm_fright": ("rain", "white"),
        "storm_debris_gift": ("wind", "white"),
        "perfect_moment": ("sun", "yellow"),
        "rain_dance": ("rain", "cyan"),
        "snow_tasting": ("snow", "white"),
        "wind_surfing": ("wind", "cyan"),
        "fog_mystery": ("fog", "white"),
        "sun_glare": ("sun", "yellow"),
        "frost_art": ("snow", "cyan"),
        "rainbow_after_rain": ("sun", "yellow"),
        "first_snowflake_beak": ("snow", "white"),
        "rain_puddle_music": ("rain", "cyan"),
        "wind_sideways": ("wind", "cyan"),
        "sun_too_bright": ("sun", "yellow"),
        "fog_mystery_exp": ("fog", "white"),
        "tiny_hail": ("hail", "white"),
        "sundog_sighting": ("sun", "yellow"),
        "frost_on_bill": ("snow", "cyan"),
        "gentle_drizzle": ("rain", "cyan"),
        "wind_feather_art": ("wind", "white"),
        "morning_mist": ("mist", "white"),
        "perfect_breeze": ("wind", "cyan"),
        "lightning_flash": ("rain", "white"),
        "snow_angel_attempt": ("snow", "white"),
        "dew_bath": ("mist", "cyan"),
        "rain_beak_drum": ("rain", "cyan"),
        "warm_rain": ("rain", "yellow"),
        "warm_rock_sun": ("sun", "yellow"),
        "hail_bounce": ("hail", "white"),
        "freezing_rain": ("rain", "cyan"),
        "ice_singing": ("snow", "cyan"),
        "icicle_boop": ("snow", "cyan"),
        "mud_puddle_spa": ("rain", "green"),
        "snowflake_unique": ("snow", "white"),
        "golden_hour": ("sun", "yellow"),
        "static_feathers": ("wind", "yellow"),
        "rainbow_spider_web": ("rain", "magenta"),
        "humidity_complaint": ("mist", "cyan"),
        "wind_tunnel_exp": ("wind", "cyan"),
        "wind_whistle": ("wind", "cyan"),
        "sunset_colors": ("sun", "red"),
        "fog_morning": ("fog", "white"),
        "pond_overflow": ("rain", "cyan"),
        "rain_crown": ("rain", "cyan"),
        "first_rain_drop": ("rain", "cyan"),
        "rain_on_leaf_xylophone": ("rain", "cyan"),
        "steam_breath": ("mist", "white"),
        "ice_cracking_sound": ("snow", "cyan"),
        "sunset_green_sky": ("sun", "green"),
        "frost_art_window": ("snow", "cyan"),
        "warm_wind_arrive": ("wind", "yellow"),
        "dust_devil_mini": ("wind", "yellow"),
        "ice_crystal_on_feather": ("snow", "cyan"),
        "worm_rain": ("rain", "green"),
        "solar_halo": ("sun", "yellow"),
        "circumhorizontal_arc": ("sun", "magenta"),
        "heat_shimmer": ("sun", "yellow"),
        "fogbow": ("fog", "white"),
        "mud_season": ("rain", "green"),
        "summer_thunderstorm": ("rain", "white"),
        "fog_bow": ("fog", "white"),
        "warm_sunbeam": ("sun", "yellow"),
    }
    if event_id in weather_events:
        wtype, color = weather_events[event_id]
        return WeatherSceneAnimator(event_id, w, h, weather_type=wtype, color=color)

    # --- DUCK REACTION / BODY EVENTS -----------------------------------
    reaction_events = {
        # event_id: (prop_sprite, color, appear_style, offset_x, offset_y)
        # Physical reactions
        "random_quack": ("music_notes", "yellow", "pop", 4, -3),
        "forgot_something": ("question", "yellow", "pop", 3, -4),
        "stare_contest": ("exclamation", "white", "pop", 5, -2),
        "feather_molt": ("leaf", "white", "drop", 0, -5),
        "itchy_spot": ("sweat_drops", "red", "pop", 3, -2),
        "deep_thought": ("thought_cloud", "cyan", "pop", 4, -4),
        "shadow_watching": ("shadow", "white", "slide", -5, 2),
        "stubbed_toe": ("rock", "red", "pop", -2, 3),
        "stepped_in_gum": ("mud_splat", "green", "pop", -1, 3),
        "startled_by_splash": ("splash", "cyan", "rise", 0, 3),
        "too_warm": ("steam", "red", "rise", 2, -3),
        "too_chilly": ("ice_crystal", "cyan", "pop", 3, -2),
        "persistent_itch": ("sweat_drops", "red", "pop", 4, -2),
        "own_reflection": ("mirror", "cyan", "pop", 5, 0),
        "stepping_on_twig": ("twig_snap", "yellow", "pop", -2, 3),
        "morning_stretch": ("spark", "yellow", "pop", 4, -3),
        "sunset_contemplation": ("thought_cloud", "red", "pop", 4, -4),
        "forgot_what_doing": ("question", "yellow", "pop", 4, -3),
        "satisfying_quack": ("music_notes", "yellow", "pop", 4, -3),
        "accidental_bug_catch": ("exclamation", "green", "pop", 3, -2),
        "dewdrop_on_beak": ("bubble", "cyan", "drop", 2, -2),
        "loose_feather": ("leaf", "white", "drop", 0, -5),
        "tail_waggle": ("ripple", "yellow", "pop", -2, 2),
        "good_waddle_rhythm": ("music_notes", "yellow", "pop", 4, -3),
        "eye_contact_stranger": ("exclamation", "white", "pop", 4, -3),
        "random_hiccup": ("exclamation", "yellow", "pop", 4, -2),
        "sitting_on_foot": ("question", "yellow", "pop", 3, -3),
        "bill_click": ("spark", "yellow", "pop", 2, -1),
        "preen_perfection": ("spark", "yellow", "pop", 3, -2),
        "puddle_splash_exp": ("splash", "cyan", "rise", 0, 3),
        "wing_flap_breeze": ("leaf", "cyan", "pop", 5, -2),
        "head_tuck_nap": ("sleep_zzz", "white", "pop", 4, -4),
        "webbed_foot_inspection": ("question", "yellow", "pop", -2, 3),
        "comfortable_bob": ("ripple", "cyan", "rise", 0, 3),
        "dramatic_yawn": ("steam", "yellow", "pop", 3, -2),
        "shadow_investigation": ("shadow", "white", "slide", -5, 2),
        "rock_appreciation": ("rock", "white", "pop", -3, 2),
        "grass_nest_attempt": ("leaf", "green", "pop", -2, 2),
        "mud_squelch": ("mud_splat", "green", "rise", 0, 3),
        "tail_chase": ("dizzy_spiral", "yellow", "pop", 0, -2),
        "underwater_eyes": ("bubble", "cyan", "rise", 0, 3),
        "perfect_landing": ("impact_stars", "yellow", "pop", 0, 2),
        "preening_knot": ("sweat_drops", "yellow", "pop", 3, -2),
        "comfortable_rock": ("rock", "white", "pop", -3, 2),
        "feather_ruffle": ("leaf", "white", "pop", 4, -2),
        "water_droplet_race": ("splash", "cyan", "rise", 0, 3),
        "accidental_dive": ("splash", "cyan", "rise", 0, 3),
        "symmetrical_ripple": ("ripple", "cyan", "rise", 0, 3),
        "warm_breeze_face": ("leaf", "yellow", "slide", -5, -2),
        "one_legged_stand": ("exclamation", "yellow", "pop", 4, -3),
        "found_own_footprints": ("footprints", "yellow", "pop", -3, 3),
        "feather_dance": ("leaf", "white", "drop", 0, -5),
        "yawn_contagion": ("steam", "yellow", "pop", 4, -2),
        "belly_rub_ground": ("ripple", "yellow", "pop", 0, 3),
        "bubble_blowing": ("bubble", "cyan", "pop", 4, -3),
        "stumble_recovery": ("impact_stars", "yellow", "pop", -1, 2),
        "first_swim_today": ("splash", "cyan", "rise", 0, 3),
        "counting_feathers": ("thought_cloud", "white", "pop", 4, -4),
        "warmth_appreciation": ("spark", "yellow", "pop", 4, -2),
        "missed_bug": ("exclamation", "red", "pop", 4, -2),
        "nice_dirt_bath": ("mud_splat", "yellow", "rise", 0, 2),
        "interesting_stick": ("twig_snap", "yellow", "pop", -3, 2),
        "leaf_on_head": ("leaf", "green", "drop", 1, -4),
        "swimming_circles": ("ripple", "cyan", "rise", 0, 3),
        "splash_face": ("splash", "cyan", "pop", 2, -1),
        "belly_flop": ("splash", "cyan", "rise", 0, 3),
        "fell_asleep_swimming": ("sleep_zzz", "cyan", "pop", 4, -4),
        "slippery_rock": ("rock", "yellow", "pop", -2, 3),
        "stuck_in_mud_exp": ("mud_splat", "green", "rise", 0, 3),
        "dramatic_fall": ("impact_stars", "red", "pop", 0, 2),
        "poop_on_head": ("mud_splat", "green", "drop", 1, -4),
        "misjudged_jump": ("impact_stars", "yellow", "pop", 0, 2),
        "walked_into_post": ("impact_stars", "red", "pop", -3, 0),
        "wing_stuck_pose": ("sweat_drops", "yellow", "pop", 4, -2),
        "choked_on_air": ("exclamation", "red", "pop", 4, -2),
        "tangled_in_seaweed": ("seaweed", "green", "rise", -2, 2),
        "water_up_nose": ("splash", "cyan", "pop", 2, -1),
        "spider_web_face": ("cobweb", "white", "pop", 2, -1),
        "feather_mouth": ("leaf", "white", "pop", 2, -1),
        "sneeze_too_loud": ("impact_stars", "yellow", "pop", 3, -2),
        "eye_twitch": ("spark", "yellow", "pop", 3, -1),
        "quack_voice_crack": ("music_notes", "yellow", "pop", 4, -3),
        "upside_down": ("dizzy_spiral", "yellow", "pop", 3, -3),
        "double_quack": ("music_notes", "yellow", "pop", 4, -3),
        "snoring_self": ("sleep_zzz", "white", "pop", 4, -4),
        "invisible_wall": ("impact_stars", "white", "pop", -3, 0),
        "wing_hug_self": ("heart", "yellow", "pop", 4, -3),
        "backwards_waddle": ("footprints", "yellow", "pop", -3, 3),
        "drool_nap": ("sleep_zzz", "cyan", "pop", 4, -4),
        "belly_rumble_loud": ("exclamation", "yellow", "pop", 3, -2),
        "wing_pit_check": ("question", "yellow", "pop", 4, -2),
        "head_shake_infinite": ("dizzy_spiral", "cyan", "pop", 3, -3),
        "accidental_moonwalk": ("footprints", "yellow", "pop", -3, 3),
        "perfect_scratch": ("spark", "yellow", "pop", 3, -1),
        "tail_feather_loose": ("leaf", "white", "drop", 0, -4),
        "impressive_splash": ("splash", "cyan", "rise", 0, 3),
        "cold_feet_literal": ("ice_crystal", "cyan", "pop", -2, 3),
        "splinter_bill": ("twig_snap", "red", "pop", 2, -1),
        "quicksand_scare": ("mud_splat", "green", "rise", 0, 3),
        "static_shock_exp": ("spark", "yellow", "pop", 3, -1),
        "sleeptalk_quack": ("sleep_zzz", "white", "pop", 4, -4),
        "sleepwalking_exp": ("sleep_zzz", "white", "pop", 4, -4),
        # Existential / thought events
        "consciousness_moment": ("thought_cloud", "cyan", "pop", 4, -4),
        "meaning_of_quack": ("question", "cyan", "pop", 4, -4),
        "identity_crisis_exp": ("dizzy_spiral", "magenta", "pop", 3, -3),
        "parallel_cheese": ("mirror", "magenta", "slide", 6, 0),
        "what_is_water": ("question", "cyan", "pop", 4, -4),
        "nature_of_bread": ("thought_cloud", "yellow", "pop", 4, -4),
        "fourth_wall_glance": ("exclamation", "magenta", "pop", 5, -2),
        "circular_thoughts": ("dizzy_spiral", "cyan", "pop", 3, -3),
        "gravity_appreciation": ("thought_cloud", "white", "pop", 4, -4),
        "memory_of_egg": ("thought_cloud", "yellow", "pop", 4, -4),
        "purpose_question": ("question", "cyan", "pop", 4, -4),
        "dream_vs_reality": ("thought_cloud", "magenta", "pop", 4, -4),
        "language_thoughts": ("thought_cloud", "cyan", "pop", 4, -4),
        "quantum_duck": ("dizzy_spiral", "magenta", "pop", 3, -3),
        "time_perception": ("thought_cloud", "cyan", "pop", 4, -4),
        "mortality_awareness": ("thought_cloud", "white", "pop", 4, -4),
        "pond_infinity": ("ripple", "cyan", "rise", 0, 3),
        "deja_vu_paddle": ("dizzy_spiral", "magenta", "pop", 3, -3),
        "time_loop": ("dizzy_spiral", "magenta", "pop", 3, -3),
        "3am_existential": ("thought_cloud", "white", "pop", 4, -4),
        "2am_bread_craving": ("thought_cloud", "yellow", "pop", 4, -4),
        # Human / social events
        "child_feeding_attempt": ("exclamation", "yellow", "pop", 4, -3),
        "old_person_bench": ("thought_cloud", "white", "pop", 4, -4),
        "jogger_splash_exp": ("splash", "cyan", "rise", 0, 3),
        "kid_pointing": ("exclamation", "yellow", "pop", 5, -2),
        "human_sneeze": ("impact_stars", "white", "pop", -4, -1),
        "hat_blew_off": ("leaf", "yellow", "drop", 0, -5),
        "photographer_exp": ("spark", "white", "pop", 5, -2),
        "person_talking_to_cheese": ("music_notes", "yellow", "pop", -5, -3),
        "someone_whistling": ("music_notes", "yellow", "slide", -6, -3),
        "human_phone_stare": ("question", "white", "pop", 5, -2),
        "romantic_couple": ("heart", "red", "pop", 5, -3),
        "couple_arguing": ("exclamation", "red", "pop", -5, -2),
        "baby_laughing": ("music_notes", "yellow", "pop", 5, -3),
        "park_ranger_shoo": ("exclamation", "red", "slide", -5, -1),
        "picnic_nearby": ("bread_loaf", "yellow", "pop", -6, 2),
        "market_day": ("exclamation", "yellow", "pop", 5, -2),
        "duck_argument": ("exclamation", "yellow", "pop", 4, -2),
        "friendly_wave": ("heart", "yellow", "pop", 5, -3),
        "old_tire_swing": ("ripple", "yellow", "pop", -5, 2),
        "helicopter_visit": ("exclamation", "white", "drop", 0, -5),
        "boat_wake": ("ripple", "cyan", "rise", 0, 3),
        "train_distant": ("music_notes", "white", "slide", -8, -3),
        "train_distant_horn": ("music_notes", "white", "slide", -8, -3),
        "kite_flying": ("leaf", "magenta", "drop", 0, -5),
        "circus_parade": ("music_notes", "magenta", "slide", -6, -2),
        "wrong_flock": ("question", "yellow", "pop", 4, -3),
        "paper_boat": ("ripple", "white", "rise", 0, 3),
        # Encounter events
        "enc_predator_shadow": ("shadow", "red", "slide", -6, 2),
        "enc_stuck_in_mud": ("mud_splat", "green", "rise", 0, 3),
        "enc_hungry_bully": ("exclamation", "red", "slide", -5, -1),
        "enc_bored_crisis": ("thought_cloud", "white", "pop", 4, -4),
        # Triggered events
        "first_waddle": ("footprints", "yellow", "pop", -3, 3),
        "first_quack": ("music_notes", "yellow", "pop", 4, -3),
        # Remaining misc reactions
        "earthquake_tiny": ("impact_stars", "red", "pop", 0, 2),
        "underground_rumble": ("impact_stars", "yellow", "rise", 0, 3),
        "magnetic_north_feeling": ("spark", "cyan", "pop", 4, -2),
        "doppelganger_duck": ("mirror", "magenta", "slide", 6, 0),
        "toe_curl": ("ripple", "yellow", "pop", -1, 3),
        "pinecone_investigation": ("rock", "yellow", "pop", -3, 2),
        "mud_art_prints": ("footprints", "yellow", "pop", -3, 3),
        "tail_dip_painting": ("splash", "yellow", "rise", 0, 3),
    }
    if event_id in reaction_events:
        prop_name, color, style, ox, oy = reaction_events[event_id]
        # Map some reaction props to food sprites via FoodSceneAnimator
        if prop_name == "bread_loaf":
            return FoodSceneAnimator(event_id, w, h, food_name="bread_loaf",
                                     color=color, appear_style="discover")
        return PropSceneAnimator(event_id, w, h, prop_name=prop_name, color=color,
                                 appear_style=style, offset_x=ox, offset_y=oy)

    # --- SKY / CELESTIAL EVENTS ----------------------------------------
    sky_events = {
        # event_id: (celestial_sprite, color, drift_direction)
        "shooting_star": ("shooting_star", "white", "left"),
        "moon_reflection": ("moon", "cyan", "none"),
        "constellation_duck": ("constellation", "white", "none"),
        "stars_contemplate": ("constellation", "white", "none"),
        "midnight_quack": ("moon", "white", "none"),
        "moonlight_swim": ("moon", "cyan", "none"),
        "first_light": ("sun_rays", "yellow", "right"),
        "night_fishing_lights": ("constellation", "yellow", "none"),
        "night_pond_sounds": ("moon", "cyan", "none"),
        "night_fog_shapes": ("cloud", "white", "left"),
        "dusk_silence": ("moon", "white", "none"),
        "dawn_chorus_exp": ("sun_rays", "yellow", "right"),
        "bread_constellation": ("constellation", "yellow", "none"),
        "northern_lights_false_alarm": ("aurora", "green", "left"),
        "venus_bright": ("shooting_star", "white", "none"),
        "shadow_duck": ("moon", "white", "none"),
        "moth_to_moon": ("moon", "white", "none"),
        "moonbeam_path": ("moon", "cyan", "none"),
        "venus_visible": ("shooting_star", "white", "none"),
        "halo_around_moon": ("moon", "white", "none"),
        "cloud_mammoth": ("cloud", "white", "left"),
        "aurora_wonder": ("aurora", "green", "left"),
        "cloud_shaped_bread": ("cloud", "white", "left"),
        "cloud_racing": ("cloud", "white", "left"),
        "cloud_spotlight": ("cloud", "yellow", "left"),
        "nacreous_clouds": ("aurora", "magenta", "left"),
        "mammatus_clouds": ("cloud", "white", "left"),
        "lenticular_cloud": ("cloud", "white", "left"),
        "summer_long_day": ("sun_rays", "yellow", "none"),
        "summer_solstice_glow": ("sun_rays", "yellow", "none"),
        "winter_short_day": ("moon", "white", "none"),
        "spring_equinox": ("sun_rays", "yellow", "right"),
        "winter_solstice_peace": ("moon", "white", "none"),
        "rainbow_sighting": ("rainbow", "magenta", "none"),
        "double_rainbow_end": ("rainbow", "magenta", "none"),
        "cloud_shadow_race": ("cloud", "white", "left"),
        "perfectly_round_cloud": ("cloud", "white", "none"),
    }
    if event_id in sky_events:
        celestial_name, color, drift = sky_events[event_id]
        return CelestialSceneAnimator(event_id, w, h, celestial_name=celestial_name,
                                       color=color, drift_direction=drift)

    # --- AMBIENT / DISCOVERY EVENTS ------------------------------------
    # Object discoveries get a shimmering object on the ground
    object_events = {
        # event_id: (object_sprite, color)
        "shiny_pebble": ("pebble", "yellow"),
        "lost_coin": ("coin", "yellow"),
        "lucky_clover": ("clover", "green"),
        "shiny_trail": ("coin", "yellow"),
        "autumn_mushroom": ("mushroom", "green"),
        "peculiar_stone": ("pebble", "white"),
        "forgotten_nest": ("nest", "yellow"),
        "legendary_feather": ("feather_obj", "magenta"),
        "ancient_coin": ("coin", "yellow"),
        "mysterious_map": ("old_map", "yellow"),
        "old_bottle": ("bottle", "cyan"),
        "buried_crumb": ("pebble", "yellow"),
        "lost_kite": ("kite", "cyan"),
        "old_fishing_line": ("fishing_line", "white"),
        "crystal_clear_water": ("crystal", "cyan"),
        "feather_collection": ("feather_obj", "white"),
        "four_leaf_clover": ("clover", "green"),
        "perfect_stone": ("pebble", "white"),
        "old_coin": ("coin", "yellow"),
        "compass_found": ("compass", "yellow"),
        "message_bottle": ("bottle", "cyan"),
        "buried_treasure": ("treasure_chest", "yellow"),
        "locked_box": ("treasure_chest", "yellow"),
        "painted_rock": ("painted_rock", "magenta"),
        "footprints_unknown": ("pebble", "white"),
        "sundial": ("sundial", "yellow"),
        "mushroom_fairy_ring": ("mushroom", "green"),
        "rock_stack": ("pebble", "white"),
        "old_bottle_message": ("bottle", "cyan"),
        "found_glass": ("crystal", "cyan"),
        "found_marble": ("marble", "yellow"),
        "found_snail_shell": ("snail_shell", "white"),
        "pebble_collection": ("pebble", "white"),
        "warm_egg_shaped_stone": ("pebble", "yellow"),
    }
    if event_id in object_events:
        obj_name, color = object_events[event_id]
        return ObjectSceneAnimator(event_id, w, h, object_name=obj_name, color=color)

    # The rest are atmospheric/ambient particle effects
    ambient_events = {
        # event_id: (pattern, color)
        "perfect_puddle": ("sparkle", "cyan"),
        "strange_visitor": ("sparkle", "white"),
        "perfect_reflection": ("sparkle", "cyan"),
        "double_yolk": ("sparkle", "yellow"),
        "morning_cobwebs": ("sparkle", "white"),
        "echo_discovery": ("pulse", "cyan"),
        "rainbow_puddle": ("sparkle", "magenta"),
        "singing_stones": ("pulse", "cyan"),
        "cave_entrance": ("pulse", "white"),
        "hidden_path": ("sparkle", "green"),
        "pirate_flag": ("sparkle", "red"),
        "rope_bridge": ("sparkle", "yellow"),
        "secret_garden": ("sparkle", "green"),
        "underground_spring": ("sparkle", "cyan"),
        "wishing_well_exp": ("sparkle", "cyan"),
        "natural_hot_tub": ("pulse", "yellow"),
        "mystery_tunnel": ("pulse", "white"),
        "hollow_tree": ("pulse", "green"),
        "echo_cave": ("pulse", "cyan"),
        "bell_sound": ("pulse", "yellow"),
        "ancient_tree": ("sparkle", "green"),
        "cosmic_duck_awareness": ("pulse", "magenta"),
        "beaver_dam_sighting": ("sparkle", "yellow"),
        "new_spot_discovery": ("sparkle", "yellow"),
        "dandelion_fluff": ("scatter", "white"),
        "cloud_shapes": ("sparkle", "white"),
        "dandelion_puff": ("scatter", "white"),
        "mysterious_sound": ("pulse", "white"),
        "mysterious_music": ("pulse", "cyan"),
        "perfect_nap_spot": ("sparkle", "yellow"),
        "water_perfect_temp": ("sparkle", "cyan"),
        "perfect_day_exp": ("sparkle", "yellow"),
        "zen_moment": ("sparkle", "cyan"),
        "water_whisper": ("wave", "cyan"),
        "perfect_temperature": ("sparkle", "yellow"),
        "ripple_symphony": ("wave", "cyan"),
        "wind_chimes_distant": ("sparkle", "cyan"),
        "sunbeam_spotlight": ("sparkle", "yellow"),
        "pond_scum_art": ("sparkle", "green"),
        "cloud_pillow": ("sparkle", "white"),
        "pine_needle_spa": ("sparkle", "green"),
        "moss_carpet": ("sparkle", "green"),
        "bubble_ride": ("sparkle", "cyan"),
        "sand_bath": ("sparkle", "yellow"),
        "flower_crown": ("sparkle", "magenta"),
        "puddle_mirror": ("sparkle", "cyan"),
        "rainbow_oil_slick": ("sparkle", "magenta"),
        "morning_cobweb_jewels": ("sparkle", "white"),
        "pond_singing_bowls": ("pulse", "cyan"),
        "perfectly_clear_water": ("sparkle", "cyan"),
        "sound_of_nothing": ("sparkle", "white"),
        "perfectly_still_day": ("sparkle", "white"),
        "giant_dandelion": ("scatter", "white"),
        "twig_snap_investigation": ("pulse", "white"),
        "talking_fish": ("pulse", "cyan"),
        "voice_in_reeds": ("pulse", "green"),
        "disappearing_island": ("pulse", "white"),
        "bright_colors": ("sparkle", "magenta"),
        "night_jasmine": ("sparkle", "magenta"),
        "fire_rainbow": ("sparkle", "magenta"),
        "first_flower": ("sparkle", "magenta"),
        "dewdrop_morning": ("sparkle", "cyan"),
        "frozen_puddle": ("sparkle", "cyan"),
        "first_flower_spring": ("sparkle", "magenta"),
        "spring_rain_smell": ("sparkle", "cyan"),
        "autumn_harvest_smell": ("sparkle", "yellow"),
        "winter_silence": ("sparkle", "white"),
        "first_spring_flower": ("sparkle", "magenta"),
        "morning_frost_sparkle": ("sparkle", "white"),
        "heatwave_mirage": ("wave", "yellow"),
        "duck_crop_circle": ("pulse", "green"),
        "sunset_waddle": ("sparkle", "red"),
        "whirlpool_tiny": ("wave", "cyan"),
        "human_playing_guitar": ("sparkle", "yellow"),
        "firefly_one": ("sparkle", "yellow"),
        "rainbow_in_spray": ("sparkle", "magenta"),
        "water_lens": ("sparkle", "cyan"),
        "fish_bubble_message": ("sparkle", "cyan"),
        "tree_face": ("pulse", "green"),
        "backward_waterfall": ("wave", "cyan"),
        "lotus_bloom": ("sparkle", "magenta"),
        "rain_smell_before": ("sparkle", "cyan"),
        "slug_trail_art": ("sparkle", "white"),
        "mushroom_overnight": ("sparkle", "green"),
        "echo_across_lake": ("pulse", "cyan"),
        "water_running_uphill": ("wave", "cyan"),
        "cricket_song": ("sparkle", "green"),
        "cricket_song_change": ("sparkle", "green"),
        "dandelion_clock_exp": ("scatter", "white"),
    }
    if event_id in ambient_events:
        pattern, color = ambient_events[event_id]
        return AmbientSceneAnimator(event_id, w, h, pattern=pattern, color=color)

    # --- PARTICLE EVENTS (falling / drifting things) -------------------
    particle_events = {
        # (particles, color, fall_speed)
        "leaf_falling": ("~.", "yellow", 0.2),
        "spring_blossom": ("*.'", "magenta", 0.2),
        "summer_fireflies": ("*.", "yellow", -0.1),
        "winter_icicle": ("| !", "cyan", 0.3),
        "autumn_leaf_pile": ("~*", "yellow", 0.2),
        "autumn_colors": ("*~", "red", 0.2),
        "spring_melt": (".,~", "cyan", 0.3),
        "autumn_leaf_fall": ("~*.", "yellow", 0.2),
        "seed_helicopter": ("~*", "green", 0.2),
    }
    if event_id in particle_events:
        chars, color, fspeed = particle_events[event_id]
        return ParticleSceneAnimator(event_id, w, h, particles=chars, color=color, fall_speed=fspeed)

    # --- SEASONAL (prop-style) ----------------------------------------
    seasonal_reaction = {
        # event_id: (prop_sprite, color, appear_style, offset_x, offset_y)
        "spring_nest_building": ("leaf", "green", "pop", -3, 2),
        "summer_lazy": ("sleep_zzz", "yellow", "pop", 4, -4),
    }
    if event_id in seasonal_reaction:
        prop_name, color, style, ox, oy = seasonal_reaction[event_id]
        return PropSceneAnimator(event_id, w, h, prop_name=prop_name, color=color,
                                 appear_style=style, offset_x=ox, offset_y=oy)

    # ------------------------------------------------------------------
    # 3. Fallback — any unmapped event gets a subtle sparkle
    # ------------------------------------------------------------------
    return AmbientSceneAnimator(event_id, w, h, pattern="sparkle", color="white", duration=4.0, intensity=4)


# ---------------------------------------------------------------------------
# Sentinel: every event now has an animation
# ---------------------------------------------------------------------------
class _AllEvents:
    """Sentinel: every event has animation."""
    def __contains__(self, item):
        return True
    def __iter__(self):
        return iter([])
    def __len__(self):
        return 999

ANIMATED_EVENTS = _AllEvents()
