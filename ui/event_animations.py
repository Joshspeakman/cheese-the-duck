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
# Generic animator imports
# ---------------------------------------------------------------------------
from ui.generic_animators import (
    GenericParticleAnimator,
    GenericSpriteAnimator,
    GenericDuckReactionAnimator,
    GenericAmbientAnimator,
    GenericWeatherAnimator,
    GenericCreatureAnimator,
    GenericFoodAnimator,
    GenericSkyAnimator,
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
        "forgotten_bread": ("[=]", "yellow", "drop"),
        "breadcrumb_trail": ("...", "yellow", "discover"),
        "soggy_bread": ("[~]", "cyan", "drop"),
        "crouton_discovery": ("[#]", "yellow", "discover"),
        "human_eating_bread": ("[=]", "white", "throw"),
        "pizza_crust": ("(>)", "yellow", "discover"),
        "seed_jackpot": (".:.", "yellow", "discover"),
        "stolen_chip": ("/\\", "yellow", "throw"),
        "mystery_food": ("[?]", "magenta", "discover"),
        "pea_discovery": ("o", "green", "discover"),
        "corn_kernel": ("o", "yellow", "discover"),
        "lettuce_confusion": ("{~}", "green", "discover"),
        "grape_chase": ("o", "magenta", "throw"),
        "toast_fragment": ("[=]", "yellow", "drop"),
        "worm_surprise": ("~", "green", "discover"),
        "bird_feeder_raid": ("[=]", "yellow", "throw"),
        "underwater_snack": ("[~]", "cyan", "discover"),
        "bread_dream": ("[=]", "yellow", "discover"),
        "food_sharing_refusal": ("[=]", "red", "throw"),
        "acorn_toy": ("@", "yellow", "discover"),
        "gourmet_weed": ("{}", "green", "discover"),
        "pretzel_find": ("&", "yellow", "discover"),
        "cheese_cracker": ("[#]", "yellow", "discover"),
        "popcorn_windfall": ("*", "white", "drop"),
        "sandwich_nearby": ("[==]", "yellow", "discover"),
        "apple_encounter": ("@", "red", "discover"),
        "fish_food_theft": (".:.", "cyan", "throw"),
        "donut_fragment": ("(O)", "yellow", "discover"),
        "rice_scattered": ("...", "white", "drop"),
        "muffin_top": ("(^)", "yellow", "discover"),
        "noodle_strand": ("~", "yellow", "discover"),
        "waffle_piece": ("[#]", "yellow", "discover"),
        "cereal_spill": ("o.o", "yellow", "drop"),
        "bread_in_eye": ("[=]", "yellow", "throw"),
        "bread_thrown_far": ("[=]", "yellow", "throw"),
        "bread_share_stranger": ("[=]", "yellow", "throw"),
        "bread_museum_fantasy": ("[=]", "magenta", "discover"),
        "bread_fossils": ("[=]", "yellow", "discover"),
        "bread_satellite": ("[=]", "cyan", "throw"),
        "bread_mirage": ("[=]", "magenta", "discover"),
        "golden_breadcrumb": ("*", "yellow", "discover"),
        "ancient_bread": ("[=]", "yellow", "discover"),
    }
    if event_id in food_events:
        char, color, style = food_events[event_id]
        return GenericFoodAnimator(event_id, w, h, food_char=char, color=color, appear_style=style)

    # --- CREATURE EVENTS -----------------------------------------------
    creature_events = {
        "friendly_frog": ("medium", "green"),
        "visiting_ladybug": ("small", "red"),
        "ant_parade": ("small", "green"),
        "fish_stare_off": ("swimming", "cyan"),
        "pigeon_judgement": ("flying", "white"),
        "bug_in_face": ("small", "yellow"),
        "worm_surface": ("small", "green"),
        "catfish_surface": ("swimming", "cyan"),
        "curious_squirrel": ("medium", "yellow"),
        "turtle_encounter": ("medium", "green"),
        "flock_overhead": ("flying", "white"),
        "visiting_heron": ("large", "blue"),
        "crow_gift": ("flying", "white"),
        "baby_ducks": ("medium", "yellow"),
        "baby_ducks_passing": ("medium", "yellow"),
        "visiting_owl": ("large", "white"),
        "dragonfly_landing": ("small", "cyan"),
        "dragonfly_chase_exp": ("small", "cyan"),
        "frog_chorus": ("medium", "green"),
        "frog_duet": ("medium", "green"),
        "caterpillar_watch": ("small", "green"),
        "spider_architect": ("small", "white"),
        "robin_argument": ("flying", "red"),
        "crow_watching": ("flying", "white"),
        "snail_race": ("small", "green"),
        "bee_flower_show": ("small", "yellow"),
        "moth_confusion": ("small", "white"),
        "heron_encounter": ("large", "blue"),
        "goose_intimidation": ("large", "white"),
        "pelican_stare": ("large", "white"),
        "kingfisher_dive": ("flying", "cyan"),
        "crab_encounter": ("small", "red"),
        "hedgehog_visit": ("medium", "yellow"),
        "swan_in_distance": ("large", "white"),
        "deer_sighting": ("large", "yellow"),
        "fox_distant": ("medium", "red"),
        "bat_swoops": ("flying", "white"),
        "peacock_jealousy": ("large", "magenta"),
        "squirrel_staredown": ("medium", "yellow"),
        "cat_staredown": ("medium", "white"),
        "sleeping_cat": ("medium", "white"),
        "hawk_shadow_pass": ("flying", "white"),
        "rabbit_sprint": ("medium", "white"),
        "raccoon_night": ("medium", "white"),
        "dog_encounter_exp": ("large", "yellow"),
        "mole_hill_exp": ("small", "green"),
        "earthworm_rain": ("small", "green"),
        "worm_standoff": ("small", "green"),
        "worm_escape": ("small", "green"),
        "caterpillar_on_nose": ("small", "green"),
        "singing_frog_choir": ("medium", "green"),
        "fish_smile": ("swimming", "cyan"),
        "fish_splashing_fight": ("swimming", "cyan"),
        "fish_tornado": ("swimming", "cyan"),
        "butterfly_migration": ("flying", "magenta"),
        "butterfly_migration_solo": ("flying", "magenta"),
        "dragonfly_escort": ("small", "cyan"),
        "heron_flyover": ("flying", "blue"),
        "owl_stare": ("large", "white"),
        "owl_conversation": ("large", "white"),
        "owl_eyes": ("large", "yellow"),
        "owl_pellet_find": ("medium", "white"),
        "fox_trot_past": ("medium", "red"),
        "barn_owl_face": ("large", "white"),
        "spider_balloon": ("small", "white"),
        "spider_web_hammock": ("small", "white"),
        "walking_stick_insect": ("small", "green"),
        "water_strider_walk": ("small", "cyan"),
        "iridescent_beetle": ("small", "magenta"),
        "coyote_howl": ("large", "yellow"),
        "tree_frog_call": ("small", "green"),
        "upside_down_beetle": ("small", "green"),
        "woodpecker_percussion": ("flying", "red"),
        "woodpecker_rhythm": ("flying", "red"),
        "flash_mob_birds": ("flying", "white"),
        "ladybug_landing": ("small", "red"),
        "ant_carrying_food": ("small", "green"),
        "witch_cat": ("medium", "magenta"),
        "hiccup_scare_fish": ("swimming", "cyan"),
        "wrong_end_fish": ("swimming", "cyan"),
        "fish_splash": ("swimming", "cyan"),
        "mosquito_assault": ("small", "red"),
        "bigfoot_glimpse": ("large", "green"),
        "venus_flytrap": ("small", "green"),
        "sunflower_turning": ("medium", "yellow"),
        "toad_wisdom": ("medium", "green"),
        "bird_v_formation": ("flying", "white"),
    }
    if event_id in creature_events:
        ctype, color = creature_events[event_id]
        return GenericCreatureAnimator(event_id, w, h, creature_type=ctype, color=color)

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
        return GenericWeatherAnimator(event_id, w, h, weather_type=wtype, color=color)

    # --- DUCK REACTION / BODY EVENTS -----------------------------------
    reaction_events = {
        # (emote, color, style)
        "random_quack": ("!", "yellow", "pop"),
        "forgot_something": ("?", "yellow", "shake"),
        "stare_contest": ("o_o", "white", "pop"),
        "feather_molt": ("~", "white", "float"),
        "itchy_spot": ("!", "red", "shake"),
        "deep_thought": ("...", "cyan", "float"),
        "shadow_watching": ("?", "white", "pop"),
        "stubbed_toe": ("!!", "red", "shake"),
        "stepped_in_gum": ("~", "green", "shake"),
        "startled_by_splash": ("!!", "cyan", "bounce"),
        "too_warm": ("~", "red", "float"),
        "too_chilly": ("*", "cyan", "shake"),
        "persistent_itch": ("!", "red", "shake"),
        "own_reflection": ("?", "cyan", "pop"),
        "stepping_on_twig": ("!", "yellow", "bounce"),
        "morning_stretch": ("~", "yellow", "float"),
        "sunset_contemplation": ("...", "red", "float"),
        "forgot_what_doing": ("?", "yellow", "shake"),
        "satisfying_quack": ("~", "yellow", "pop"),
        "accidental_bug_catch": ("!", "green", "bounce"),
        "dewdrop_on_beak": (".", "cyan", "pop"),
        "loose_feather": ("~", "white", "float"),
        "tail_waggle": ("~", "yellow", "bounce"),
        "good_waddle_rhythm": ("~", "yellow", "bounce"),
        "eye_contact_stranger": ("!", "white", "pop"),
        "random_hiccup": ("!", "yellow", "bounce"),
        "sitting_on_foot": ("?", "yellow", "shake"),
        "bill_click": ("*", "yellow", "pop"),
        "preen_perfection": ("*", "yellow", "pop"),
        "puddle_splash_exp": ("~", "cyan", "bounce"),
        "wing_flap_breeze": ("~", "cyan", "float"),
        "head_tuck_nap": ("z", "white", "float"),
        "webbed_foot_inspection": ("?", "yellow", "pop"),
        "comfortable_bob": ("~", "cyan", "bounce"),
        "dramatic_yawn": ("O", "yellow", "pop"),
        "shadow_investigation": ("?", "white", "pop"),
        "rock_appreciation": ("*", "white", "pop"),
        "grass_nest_attempt": ("~", "green", "shake"),
        "mud_squelch": ("~", "green", "bounce"),
        "tail_chase": ("!", "yellow", "bounce"),
        "underwater_eyes": ("o", "cyan", "pop"),
        "perfect_landing": ("*", "yellow", "pop"),
        "preening_knot": ("!", "yellow", "shake"),
        "comfortable_rock": ("~", "white", "float"),
        "feather_ruffle": ("~", "white", "shake"),
        "water_droplet_race": (".", "cyan", "bounce"),
        "accidental_dive": ("!!", "cyan", "bounce"),
        "symmetrical_ripple": ("o", "cyan", "pop"),
        "warm_breeze_face": ("~", "yellow", "float"),
        "one_legged_stand": ("!", "yellow", "pop"),
        "found_own_footprints": ("?", "yellow", "pop"),
        "feather_dance": ("~", "white", "float"),
        "yawn_contagion": ("O", "yellow", "pop"),
        "belly_rub_ground": ("~", "yellow", "bounce"),
        "bubble_blowing": ("o", "cyan", "float"),
        "stumble_recovery": ("!", "yellow", "bounce"),
        "first_swim_today": ("~", "cyan", "bounce"),
        "counting_feathers": ("...", "white", "pop"),
        "warmth_appreciation": ("*", "yellow", "float"),
        "missed_bug": ("!", "red", "shake"),
        "nice_dirt_bath": ("~", "yellow", "bounce"),
        "interesting_stick": ("?", "yellow", "pop"),
        "leaf_on_head": ("~", "green", "float"),
        "swimming_circles": ("~", "cyan", "bounce"),
        "splash_face": ("!", "cyan", "bounce"),
        "belly_flop": ("!!", "cyan", "bounce"),
        "fell_asleep_swimming": ("z", "cyan", "float"),
        "slippery_rock": ("!", "yellow", "shake"),
        "stuck_in_mud_exp": ("!", "green", "shake"),
        "dramatic_fall": ("!!", "red", "bounce"),
        "poop_on_head": ("!!", "green", "bounce"),
        "misjudged_jump": ("!", "yellow", "bounce"),
        "walked_into_post": ("*", "red", "shake"),
        "wing_stuck_pose": ("?", "yellow", "shake"),
        "choked_on_air": ("!", "red", "shake"),
        "tangled_in_seaweed": ("~", "green", "shake"),
        "water_up_nose": ("!", "cyan", "shake"),
        "spider_web_face": ("!!", "white", "shake"),
        "feather_mouth": ("~", "white", "shake"),
        "sneeze_too_loud": ("!!", "yellow", "bounce"),
        "eye_twitch": (".", "yellow", "shake"),
        "quack_voice_crack": ("?", "yellow", "bounce"),
        "upside_down": ("!", "yellow", "shake"),
        "double_quack": ("!!", "yellow", "pop"),
        "snoring_self": ("z", "white", "float"),
        "invisible_wall": ("!", "white", "shake"),
        "wing_hug_self": ("*", "yellow", "pop"),
        "backwards_waddle": ("?", "yellow", "shake"),
        "drool_nap": ("z", "cyan", "float"),
        "belly_rumble_loud": ("~", "yellow", "shake"),
        "wing_pit_check": ("?", "yellow", "pop"),
        "head_shake_infinite": ("~", "cyan", "shake"),
        "accidental_moonwalk": ("*", "yellow", "bounce"),
        "perfect_scratch": ("*", "yellow", "pop"),
        "tail_feather_loose": ("~", "white", "float"),
        "impressive_splash": ("!!", "cyan", "bounce"),
        "cold_feet_literal": ("*", "cyan", "shake"),
        "splinter_bill": ("!", "red", "shake"),
        "quicksand_scare": ("!!", "green", "shake"),
        "static_shock_exp": ("*", "yellow", "bounce"),
        "sleeptalk_quack": ("z", "white", "float"),
        "sleepwalking_exp": ("z", "white", "shake"),
        # Existential / thought events
        "consciousness_moment": ("...", "cyan", "float"),
        "meaning_of_quack": ("?", "cyan", "float"),
        "identity_crisis_exp": ("?!", "magenta", "shake"),
        "parallel_cheese": ("?", "magenta", "float"),
        "what_is_water": ("?", "cyan", "float"),
        "nature_of_bread": ("?", "yellow", "float"),
        "fourth_wall_glance": ("!", "magenta", "pop"),
        "circular_thoughts": ("~", "cyan", "shake"),
        "gravity_appreciation": (".", "white", "float"),
        "memory_of_egg": ("...", "yellow", "float"),
        "purpose_question": ("?", "cyan", "float"),
        "dream_vs_reality": ("?", "magenta", "shake"),
        "language_thoughts": ("...", "cyan", "float"),
        "quantum_duck": ("?", "magenta", "shake"),
        "time_perception": ("...", "cyan", "float"),
        "mortality_awareness": ("...", "white", "float"),
        "pond_infinity": ("~", "cyan", "float"),
        "deja_vu_paddle": ("?!", "magenta", "shake"),
        "time_loop": ("~", "magenta", "shake"),
        "3am_existential": ("...", "white", "float"),
        "2am_bread_craving": ("!", "yellow", "shake"),
        # Human / social events
        "child_feeding_attempt": ("!", "yellow", "pop"),
        "old_person_bench": ("~", "white", "float"),
        "jogger_splash_exp": ("!!", "cyan", "bounce"),
        "kid_pointing": ("!", "yellow", "pop"),
        "human_sneeze": ("!!", "white", "bounce"),
        "hat_blew_off": ("?", "yellow", "pop"),
        "photographer_exp": ("!", "white", "pop"),
        "person_talking_to_cheese": ("?", "yellow", "pop"),
        "someone_whistling": ("~", "yellow", "float"),
        "human_phone_stare": ("?", "white", "pop"),
        "romantic_couple": ("~", "red", "float"),
        "couple_arguing": ("!", "red", "pop"),
        "baby_laughing": ("~", "yellow", "bounce"),
        "park_ranger_shoo": ("!!", "red", "bounce"),
        "picnic_nearby": ("!", "yellow", "pop"),
        "market_day": ("!", "yellow", "pop"),
        "duck_argument": ("!", "yellow", "shake"),
        "friendly_wave": ("~", "yellow", "pop"),
        "old_tire_swing": ("~", "yellow", "bounce"),
        "helicopter_visit": ("!", "white", "bounce"),
        "boat_wake": ("~", "cyan", "bounce"),
        "train_distant": ("~", "white", "float"),
        "train_distant_horn": ("~", "white", "float"),
        "kite_flying": ("~", "magenta", "float"),
        "circus_parade": ("!!", "magenta", "bounce"),
        "wrong_flock": ("?", "yellow", "shake"),
        "paper_boat": ("~", "white", "float"),
        # Encounter events
        "enc_predator_shadow": ("!!", "red", "shake"),
        "enc_stuck_in_mud": ("!", "green", "shake"),
        "enc_hungry_bully": ("!!", "red", "shake"),
        "enc_bored_crisis": ("...", "white", "float"),
        # Triggered events
        "first_waddle": ("!", "yellow", "bounce"),
        "first_quack": ("!", "yellow", "pop"),
        # Remaining misc reactions
        "earthquake_tiny": ("!!", "red", "shake"),
        "underground_rumble": ("!!", "yellow", "shake"),
        "magnetic_north_feeling": ("?", "cyan", "shake"),
        "doppelganger_duck": ("?!", "magenta", "shake"),
        "toe_curl": ("~", "yellow", "bounce"),
        "pinecone_investigation": ("?", "yellow", "pop"),
        "mud_art_prints": ("*", "yellow", "pop"),
        "tail_dip_painting": ("*", "yellow", "pop"),
    }
    if event_id in reaction_events:
        emote, color, style = reaction_events[event_id]
        return GenericDuckReactionAnimator(event_id, w, h, emote=emote, color=color, style=style)

    # --- SKY / CELESTIAL EVENTS ----------------------------------------
    sky_events = {
        "shooting_star": ("celestial", "white"),
        "moon_reflection": ("stars", "cyan"),
        "constellation_duck": ("stars", "white"),
        "stars_contemplate": ("stars", "white"),
        "midnight_quack": ("stars", "white"),
        "moonlight_swim": ("stars", "cyan"),
        "first_light": ("celestial", "yellow"),
        "night_fishing_lights": ("stars", "yellow"),
        "night_pond_sounds": ("stars", "cyan"),
        "night_fog_shapes": ("stars", "white"),
        "dusk_silence": ("stars", "white"),
        "dawn_chorus_exp": ("celestial", "yellow"),
        "bread_constellation": ("stars", "yellow"),
        "northern_lights_false_alarm": ("aurora", "green"),
        "venus_bright": ("celestial", "white"),
        "shadow_duck": ("stars", "white"),
        "moth_to_moon": ("celestial", "white"),
        "moonbeam_path": ("stars", "cyan"),
        "venus_visible": ("celestial", "white"),
        "halo_around_moon": ("celestial", "white"),
        "cloud_mammoth": ("clouds", "white"),
        # Weather events that are sky-based
        "aurora_wonder": ("aurora", "green"),
        "cloud_shaped_bread": ("clouds", "white"),
        "cloud_racing": ("clouds", "white"),
        "cloud_spotlight": ("clouds", "yellow"),
        "nacreous_clouds": ("aurora", "magenta"),
        "mammatus_clouds": ("clouds", "white"),
        "lenticular_cloud": ("clouds", "white"),
        # Seasonal sky events
        "summer_long_day": ("celestial", "yellow"),
        "summer_solstice_glow": ("celestial", "yellow"),
        "winter_short_day": ("stars", "white"),
        "spring_equinox": ("celestial", "yellow"),
        "winter_solstice_peace": ("stars", "white"),
        # Remaining misc sky
        "rainbow_sighting": ("celestial", "magenta"),
        "double_rainbow_end": ("celestial", "magenta"),
        "cloud_shadow_race": ("clouds", "white"),
        "perfectly_round_cloud": ("clouds", "white"),
    }
    if event_id in sky_events:
        stype, color = sky_events[event_id]
        return GenericSkyAnimator(event_id, w, h, sky_type=stype, color=color)

    # --- AMBIENT / DISCOVERY EVENTS ------------------------------------
    ambient_events = {
        # (pattern, color)
        "shiny_pebble": ("sparkle", "yellow"),
        "lost_coin": ("sparkle", "yellow"),
        "perfect_puddle": ("sparkle", "cyan"),
        "lucky_clover": ("sparkle", "green"),
        "shiny_trail": ("sparkle", "yellow"),
        "strange_visitor": ("sparkle", "white"),
        "autumn_mushroom": ("sparkle", "green"),
        "peculiar_stone": ("sparkle", "white"),
        "forgotten_nest": ("sparkle", "yellow"),
        "legendary_feather": ("sparkle", "magenta"),
        "ancient_coin": ("sparkle", "yellow"),
        "mysterious_map": ("sparkle", "yellow"),
        "old_bottle": ("sparkle", "cyan"),
        "buried_crumb": ("sparkle", "yellow"),
        "perfect_reflection": ("sparkle", "cyan"),
        "double_yolk": ("sparkle", "yellow"),
        "lost_kite": ("sparkle", "cyan"),
        "morning_cobwebs": ("sparkle", "white"),
        "old_fishing_line": ("sparkle", "white"),
        "echo_discovery": ("pulse", "cyan"),
        "crystal_clear_water": ("sparkle", "cyan"),
        "feather_collection": ("sparkle", "white"),
        "four_leaf_clover": ("sparkle", "green"),
        "perfect_stone": ("sparkle", "white"),
        "rainbow_puddle": ("sparkle", "magenta"),
        "old_coin": ("sparkle", "yellow"),
        "compass_found": ("sparkle", "yellow"),
        "singing_stones": ("pulse", "cyan"),
        "message_bottle": ("sparkle", "cyan"),
        "cave_entrance": ("pulse", "white"),
        "hidden_path": ("sparkle", "green"),
        "buried_treasure": ("sparkle", "yellow"),
        "locked_box": ("sparkle", "yellow"),
        "pirate_flag": ("sparkle", "red"),
        "rope_bridge": ("sparkle", "yellow"),
        "secret_garden": ("sparkle", "green"),
        "underground_spring": ("sparkle", "cyan"),
        "wishing_well_exp": ("sparkle", "cyan"),
        "painted_rock": ("sparkle", "magenta"),
        "natural_hot_tub": ("pulse", "yellow"),
        "mystery_tunnel": ("pulse", "white"),
        "hollow_tree": ("pulse", "green"),
        "echo_cave": ("pulse", "cyan"),
        "bell_sound": ("pulse", "yellow"),
        "footprints_unknown": ("sparkle", "white"),
        "ancient_tree": ("sparkle", "green"),
        "cosmic_duck_awareness": ("pulse", "magenta"),
        "sundial": ("sparkle", "yellow"),
        "mushroom_fairy_ring": ("sparkle", "green"),
        "rock_stack": ("sparkle", "white"),
        "beaver_dam_sighting": ("sparkle", "yellow"),
        "old_bottle_message": ("sparkle", "cyan"),
        "found_glass": ("sparkle", "cyan"),
        "found_marble": ("sparkle", "yellow"),
        "found_snail_shell": ("sparkle", "white"),
        "pebble_collection": ("sparkle", "white"),
        "new_spot_discovery": ("sparkle", "yellow"),
        # Ambiance / misc
        "dandelion_fluff": ("sparkle", "white"),
        "cloud_shapes": ("sparkle", "white"),
        "dandelion_puff": ("sparkle", "white"),
        "mysterious_sound": ("pulse", "white"),
        "mysterious_music": ("pulse", "cyan"),
        "perfect_nap_spot": ("sparkle", "yellow"),
        "water_perfect_temp": ("sparkle", "cyan"),
        "perfect_day_exp": ("sparkle", "yellow"),
        "zen_moment": ("sparkle", "cyan"),
        "water_whisper": ("sparkle", "cyan"),
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
        "giant_dandelion": ("sparkle", "white"),
        "twig_snap_investigation": ("pulse", "white"),
        "talking_fish": ("pulse", "cyan"),
        "voice_in_reeds": ("pulse", "green"),
        "disappearing_island": ("pulse", "white"),
        "bright_colors": ("sparkle", "magenta"),
        "night_jasmine": ("sparkle", "magenta"),
        "fire_rainbow": ("sparkle", "magenta"),
        # Seasonal ambient
        "first_flower": ("sparkle", "magenta"),
        "dewdrop_morning": ("sparkle", "cyan"),
        "frozen_puddle": ("sparkle", "cyan"),
        "first_flower_spring": ("sparkle", "magenta"),
        "spring_rain_smell": ("sparkle", "cyan"),
        "autumn_harvest_smell": ("sparkle", "yellow"),
        "winter_silence": ("sparkle", "white"),
        "first_spring_flower": ("sparkle", "magenta"),
        "morning_frost_sparkle": ("sparkle", "white"),
        # Remaining misc ambient
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
        "warm_egg_shaped_stone": ("sparkle", "yellow"),
        "dandelion_clock_exp": ("scatter", "white"),
    }
    if event_id in ambient_events:
        pattern, color = ambient_events[event_id]
        return GenericAmbientAnimator(event_id, w, h, pattern=pattern, color=color)

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
        return GenericParticleAnimator(event_id, w, h, particles=chars, color=color, fall_speed=fspeed)

    # --- SEASONAL (reaction-style) ------------------------------------
    seasonal_reaction = {
        "spring_nest_building": ("~", "green", "pop"),
        "summer_lazy": ("z", "yellow", "float"),
    }
    if event_id in seasonal_reaction:
        emote, color, style = seasonal_reaction[event_id]
        return GenericDuckReactionAnimator(event_id, w, h, emote=emote, color=color, style=style)

    # ------------------------------------------------------------------
    # 3. Fallback — any unmapped event gets a subtle sparkle
    # ------------------------------------------------------------------
    return GenericAmbientAnimator(event_id, w, h, pattern="sparkle", color="white", duration=4.0, intensity=4)


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
