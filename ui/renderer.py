"""
Terminal UI renderer using blessed library - Enhanced version with side panel layout.
Features a main playfield with moving duck and side panel with close-up, stats, etc.
"""
import time
import math
import random
import re
from typing import Optional, List, Dict, Tuple, Any, TYPE_CHECKING
from blessed import Terminal


# Regex to strip ANSI escape sequences for visible length calculation
_ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;]*m|\033\[[0-9;]*m|\x1b\([0-9;]*[a-zA-Z]')

def _visible_len(s: str) -> int:
    """Get visible length of string, ignoring ANSI escape codes."""
    return len(_ANSI_ESCAPE.sub('', s))


def _visible_ljust(s: str, width: int) -> str:
    """Left-justify string to visible width, accounting for ANSI codes."""
    visible = _visible_len(s)
    if visible >= width:
        return s
    return s + ' ' * (width - visible)


def _visible_center(s: str, width: int) -> str:
    """Center string to visible width, accounting for ANSI codes."""
    visible = _visible_len(s)
    if visible >= width:
        return s
    pad_total = width - visible
    pad_left = pad_total // 2
    pad_right = pad_total - pad_left
    return ' ' * pad_left + s + ' ' * pad_right


def _visible_rjust(s: str, width: int) -> str:
    """Right-justify string to visible width, accounting for ANSI codes."""
    visible = _visible_len(s)
    if visible >= width:
        return s
    return ' ' * (width - visible) + s


def _visible_slice(s: str, start: int, end: int) -> str:
    """Slice string by visible character positions, preserving ANSI codes.
    
    Returns substring from visible position start to end (exclusive).
    Handles ANSI escape sequences correctly - only includes ANSI codes
    that appear within the sliced range to prevent color bleeding.
    """
    result = []
    visible_pos = 0
    i = 0
    
    while i < len(s):
        # Check for ANSI escape sequence
        match = _ANSI_ESCAPE.match(s, i)
        if match:
            # Only include ANSI codes that appear within the sliced range
            # Don't include codes from before the slice to prevent color bleeding
            if visible_pos >= start and visible_pos < end:
                result.append(match.group())
            i = match.end()
        else:
            # Regular character
            if start <= visible_pos < end:
                result.append(s[i])
            visible_pos += 1
            i += 1
    
    return ''.join(result)


def _visible_truncate(s: str, width: int) -> str:
    """Truncate string to visible width, preserving ANSI codes."""
    return _visible_slice(s, 0, width)


from config import COLORS
from ui.ascii_art import get_duck_art, get_emotion_closeup, create_box, BORDER, get_mini_duck, PLAYFIELD_OBJECTS
from ui.input_handler import get_help_text
from ui.animations import animation_controller, EFFECTS
from ui.habitat_icons import get_habitat_icon, HABITAT_ICONS
from ui.location_art import (
    generate_location_ground, generate_location_decorations, 
    generate_location_scenery, get_decoration_color, get_location_colors,
    get_ground_color
)
from duck.mood import MoodState
from duck.cosmetics import CosmeticsRenderer, COSMETIC_ART

if TYPE_CHECKING:
    from duck.duck import Duck
    from core.game import Game


# Box drawing characters (Unicode)
BOX = {
    "tl": "\u250c",  # Top left
    "tr": "\u2510",  # Top right
    "bl": "\u2514",  # Bottom left
    "br": "\u2518",  # Bottom right
    "h": "\u2500",   # Horizontal
    "v": "\u2502",   # Vertical
    "cross": "\u253c",
    "t_down": "\u252c",
    "t_up": "\u2534",
    "t_right": "\u251c",
    "t_left": "\u2524",
}

# Double line box for emphasis
BOX_DOUBLE = {
    "tl": "\u2554",
    "tr": "\u2557",
    "bl": "\u255a",
    "br": "\u255d",
    "h": "\u2550",
    "v": "\u2551",
}

# Progress bar styles
BAR_STYLES = {
    "full": "\u2588",      # Full block
    "high": "\u2593",      # Dark shade
    "med": "\u2592",       # Medium shade
    "low": "\u2591",       # Light shade
    "empty": " ",
}

# Ground patterns for playfield
GROUND_CHARS = [".", ",", "'", "`", " ", " ", " "]


class DuckPosition:
    """Tracks duck position and movement in the playfield."""

    def __init__(self, field_width: int = 40, field_height: int = 12):
        self.field_width = field_width
        self.field_height = field_height
        self.x = field_width // 2
        self.y = field_height // 2
        self.target_x = self.x
        self.target_y = self.y
        self.facing_right = True
        self.is_moving = False
        self._move_timer = 0.0
        self._idle_timer = 0.0
        self._state = "idle"  # idle, walking, sleeping, eating, playing, cleaning, petting
        self._animation_frame = 0
        self._state_animation_timer = 0.0  # Timer for state-specific animations
        self._state_duration = 0.0  # How long to stay in this state
        self._state_start_time = 0.0  # When the state started
        
        # Movement callback support for animated interactions
        self._movement_callback = None  # Called when duck reaches target
        self._movement_callback_data = None  # Data to pass to callback
        self._is_directed_movement = False  # True if moving to specific target (not wandering)
        self._original_position = None  # For returning after interaction

    # All states that support animation frame cycling
    # Only includes states that exist for all growth stages
    ANIMATABLE_STATES = {
        # User interaction states
        "sleeping", "eating", "playing", "cleaning", "petting",
        # Weather reaction states
        "cold", "hot", "shaking", "scared", "excited", "curious", "hiding",
        # Extended animation states
        "swimming", "diving", "stretching", "yawning", "jumping",
        "thinking", "dancing", "singing", "pecking", "flapping",
        "preening", "napping", "waddle_fast", "dizzy", "proud",
        "sneaking", "splashing", "floating", "hungry", "love",
        "angry", "bored", "waving", "tail_wag", "reminiscing", "wise"
    }

    def update(self, delta_time: float):
        """Update duck position and movement."""
        self._move_timer += delta_time
        self._idle_timer += delta_time
        self._state_animation_timer += delta_time

        # ALWAYS process directed movement first, regardless of animation state
        # This ensures duck walks to nest/structures before performing actions
        if self._is_directed_movement:
            if self.x != self.target_x or self.y != self.target_y:
                self.is_moving = True
                if self._move_timer > 0.15:  # Move every 0.15 seconds
                    self._move_timer = 0
                    self._animation_frame = (self._animation_frame + 1) % 4

                    # Move one step towards target
                    if self.x < self.target_x:
                        self.x += 1
                        self.facing_right = True
                    elif self.x > self.target_x:
                        self.x -= 1
                        self.facing_right = False

                    if self.y < self.target_y:
                        self.y += 1
                    elif self.y > self.target_y:
                        self.y -= 1
            else:
                # Reached target during directed movement
                self.is_moving = False
                if self._movement_callback:
                    callback = self._movement_callback
                    callback_data = self._movement_callback_data
                    # Clear callback before calling to prevent re-triggering
                    self._movement_callback = None
                    self._movement_callback_data = None
                    self._is_directed_movement = False
                    # Execute callback (this will set the sleeping/action state)
                    callback(callback_data)
                else:
                    self._is_directed_movement = False
            return  # Don't do other movement while directed movement is active

        # Cycle animation frames for all animatable states (every 0.4 seconds)
        if self._state in self.ANIMATABLE_STATES:
            if self._state_animation_timer > 0.4:
                self._animation_frame = (self._animation_frame + 1) % 2
                self._state_animation_timer = 0

            # Check if state duration has expired (return to idle)
            if self._state_duration > 0:
                import time
                if time.time() - self._state_start_time > self._state_duration:
                    self._state = "idle"
                    self._state_duration = 0
            return  # Don't wander while in special state

        # Randomly pick new target when idle (but not during directed movement)
        if self._state == "idle" and not self._is_directed_movement and self._idle_timer > random.uniform(3, 8):
            if random.random() < 0.6:  # 60% chance to wander
                self._pick_new_target()
                self._idle_timer = 0

        # Move towards target (normal wandering, not directed)
        if self.x != self.target_x or self.y != self.target_y:
            self.is_moving = True
            self._state = "walking"

            if self._move_timer > 0.15:  # Move every 0.15 seconds
                self._move_timer = 0
                self._animation_frame = (self._animation_frame + 1) % 4

                # Move one step towards target
                if self.x < self.target_x:
                    self.x += 1
                    self.facing_right = True
                elif self.x > self.target_x:
                    self.x -= 1
                    self.facing_right = False

                if self.y < self.target_y:
                    self.y += 1
                elif self.y > self.target_y:
                    self.y -= 1
        else:
            # Reached target
            self.is_moving = False
            if self._state == "walking":
                self._state = "idle"
                self._idle_timer = 0

    def _pick_new_target(self):
        """Pick a random target position."""
        margin = 3
        # Ensure valid ranges even for small fields
        max_x = max(margin, self.field_width - margin - 6)
        max_y = max(margin, self.field_height - margin - 3)
        self.target_x = random.randint(margin, max_x)
        self.target_y = random.randint(margin, max_y)

    def move_to(self, target_x: int, target_y: int, callback=None, callback_data=None, save_original: bool = True):
        """
        Move duck to specific target position with optional callback when reached.
        
        Args:
            target_x: Target x position in playfield coordinates
            target_y: Target y position in playfield coordinates  
            callback: Function to call when duck reaches target (receives callback_data)
            callback_data: Data to pass to callback function
            save_original: If True, save current position to return to later
        """
        # Clamp to field bounds
        margin = 2
        max_x = max(margin, self.field_width - margin - 6)
        max_y = max(margin, self.field_height - margin - 3)
        target_x = max(margin, min(target_x, max_x))
        target_y = max(margin, min(target_y, max_y))
        
        # Save original position for potential return
        if save_original and self._original_position is None:
            self._original_position = (self.x, self.y)
        
        self.target_x = target_x
        self.target_y = target_y
        self._movement_callback = callback
        self._movement_callback_data = callback_data
        self._is_directed_movement = True
        self._state = "walking"
        self.is_moving = True
        
        # Face the right direction
        self.facing_right = target_x >= self.x

    def return_to_original(self, callback=None, callback_data=None):
        """Move duck back to its original position before directed movement."""
        if self._original_position:
            orig_x, orig_y = self._original_position
            self._original_position = None  # Clear so we don't save new position
            self.move_to(orig_x, orig_y, callback, callback_data, save_original=False)
        else:
            # No original position, just stay put
            if callback:
                callback(callback_data)

    def cancel_movement(self):
        """Cancel any pending directed movement and callbacks."""
        self._movement_callback = None
        self._movement_callback_data = None
        self._is_directed_movement = False
        self._original_position = None
        self.target_x = self.x
        self.target_y = self.y
        self.is_moving = False
        self._state = "idle"

    def set_state(self, state: str, duration: float = 3.0):
        """Set duck state for animation."""
        import time
        self._state = state
        self._animation_frame = 0
        self._state_animation_timer = 0
        self._state_duration = duration
        self._state_start_time = time.time()

        # Stop moving during all animatable states
        if state in self.ANIMATABLE_STATES:
            self.target_x = self.x
            self.target_y = self.y
            self.is_moving = False
            # Clear directed movement and callbacks if we're entering a special state
            self._is_directed_movement = False
            self._movement_callback = None
            self._movement_callback_data = None

    def get_state(self) -> str:
        return self._state

    def get_animation_frame(self) -> int:
        return self._animation_frame


class Renderer:
    """
    Renders the game UI to the terminal using blessed.
    Enhanced version with side panel layout and animated playfield.
    """

    def __init__(self, terminal: Terminal):
        self.term = terminal
        self._last_render_time = 0
        self._message_queue: List[str] = []
        self._message_expire = 0
        self._show_message_overlay = False  # Show messages as overlay instead of bottom bar
        self._message_rendered_inline = False  # Track if message was rendered in playfield
        
        # Persistent chat log (WoW-style, newest at bottom)
        self._chat_log: List[tuple] = []  # List of (timestamp, message, category)
        self._chat_log_max_size = 30  # Keep last 30 messages
        self._chat_log_visible_lines = 5  # Show 5 lines in the UI
        self._chat_scroll_offset = 0  # Scroll offset (0 = newest at bottom)
        
        # Menu overlay (separate from chat messages)
        self._menu_overlay_content: List[str] = []  # Menu overlay content
        self._menu_overlay_active = False  # Whether a menu overlay is shown
        
        self._show_help = False
        self._show_inventory = False
        self._show_stats = False
        self._show_talk = False
        self._show_closeup = False
        self._closeup_expire = 0
        self._closeup_action: Optional[str] = None
        self._talk_buffer = ""
        self._animation_frame = 0
        self._animation_time = 0
        self._title_frame = 0
        self._effect_overlay: Optional[str] = None
        self._effect_expire = 0

        # Celebration overlay
        self._show_celebration = False
        self._celebration_type: Optional[str] = None
        self._celebration_message: str = ""
        self._celebration_expire = 0
        self._celebration_frame = 0
        self._celebration_frame_time = 0

        # Duck position tracking
        self.duck_pos = DuckPosition(field_width=44, field_height=14)

        # Cosmetics renderer for showing equipped items
        self._cosmetics_renderer = CosmeticsRenderer()

        # Interaction animation overlay system
        from ui.interaction_animations import InteractionAnimator
        self.interaction_animator = InteractionAnimator()

        # Playfield decorations (static objects)
        self._playfield_objects: List[Tuple[int, int, str]] = []
        self._generate_playfield_decorations()

        # Inventory items list for key selection
        self._inventory_items: List[str] = []

        # Shop system
        self._show_shop = False
        self._shop_category_index = 0
        self._shop_item_index = 0
        self._shop_categories = ["COSMETIC", "TOY", "FURNITURE", "WATER", "PLANT"]
        self._shop_items_per_page = 8  # Items per page in shop

        # Stats window pagination
        self._stats_scroll_offset = 0
        self._stats_page_size = 15  # Lines visible per page

        # Ground pattern cache
        self._ground_pattern: List[str] = []
        self._current_location: Optional[str] = None
        self._location_decorations: List[Tuple[int, int, str]] = []
        self._location_scenery: List[Tuple[int, int, List[str]]] = []
        self._first_render = True  # Force regeneration on first render
        # Don't generate pattern here - wait for first render with correct dimensions

        # Weather effects
        self._weather_particles: List[Tuple[float, float, str]] = []  # (x, y, char)
        self._weather_frame = 0
        self._current_weather_type: Optional[str] = None
        
        # Cached terminal dimensions for stability (prevent micro-jitter)
        self._cached_width: Optional[int] = None
        self._cached_height: Optional[int] = None
        
        # Environmental weather decorations (puddles, snow piles, leaves, etc.)
        self._weather_decorations: List[Tuple[int, int, str, Any]] = []  # (x, y, char, color_func)
        self._weather_decoration_weather: Optional[str] = None  # Weather when decorations were generated

    def _generate_weather_decorations(self, weather_type: Optional[str], env_effects: List[str], width: int, height: int):
        """Generate environmental decorations based on current weather."""
        if weather_type == self._weather_decoration_weather:
            return  # Already generated for this weather
        
        self._weather_decoration_weather = weather_type
        self._weather_decorations = []
        
        if not env_effects or not weather_type:
            return
        
        # Define decoration patterns for each environmental effect
        effect_decorations = {
            # Puddles and water effects
            "small_puddles": [("~", self.term.bright_cyan), (".", self.term.cyan)],
            "puddles": [("~", self.term.cyan), ("~", self.term.bright_cyan), ("o", self.term.blue)],
            "large_puddles": [("~~~", self.term.blue), ("~o~", self.term.cyan), ("~~", self.term.bright_blue)],
            "rippling_water": [("~", self.term.cyan), ("o", self.term.bright_cyan)],
            "icy_puddles": [("#", self.term.bright_white), ("~", self.term.bright_cyan)],
            
            # Snow and ice effects
            "light_snow_cover": [(".", self.term.white), (",", self.term.bright_white)],
            "snow_cover": [("*", self.term.bright_white), (".", self.term.white)],
            "snow_piles": [("***", self.term.bright_white), ("**", self.term.white), ("*#*", self.term.bright_white)],
            "snow_drifts": [("~~~~", self.term.bright_white), ("***", self.term.white)],
            "deep_snow": [("###", self.term.bright_white), ("***", self.term.white)],
            "frost_crystals": [("*", self.term.bright_cyan), ("+", self.term.cyan)],
            "icicles": [("|", self.term.bright_cyan), ("'", self.term.cyan)],
            "ice_coating": [("#", self.term.bright_white), ("=", self.term.bright_cyan)],
            "frost_sparkles": [("*", self.term.bright_white), ("+", self.term.cyan)],
            
            # Leaf effects
            "falling_leaves": [("{", self.term.yellow), ("}", self.term.bright_red), ("(", self.term.bright_yellow)],
            "leaf_piles": [("{}", self.term.yellow), ("()", self.term.bright_red), ("{{}}", self.term.bright_yellow)],
            "swirling_leaves": [("{", self.term.yellow), ("}", self.term.red)],
            "colorful_leaves": [("{", self.term.bright_yellow), ("}", self.term.red), ("(", self.term.yellow)],
            
            # Nature effects  
            "swaying_reeds": [("|", self.term.green), ("/", self.term.green), ("\\", self.term.green)],
            "blowing_leaves": [("~", self.term.green), ("{", self.term.yellow)],
            "swaying_flowers": [("*", self.term.magenta), ("@", self.term.bright_magenta)],
            "dancing_petals": [(".", self.term.magenta), ("*", self.term.bright_red)],
            "blooming_flowers": [("*", self.term.magenta), ("@", self.term.bright_yellow), ("o", self.term.red)],
            "blooming_trees": [("Y", self.term.green), ("*", self.term.magenta)],
            "bending_trees": [("/", self.term.green), ("\\", self.term.green)],
            
            # Atmospheric effects
            "dew_drops": [(".", self.term.bright_cyan), ("o", self.term.cyan)],
            "thick_fog": [(".", self.term.white), ("~", self.term.white)],
            "soft_haze": [(".", self.term.white)],
            "cloud_shadows": [(".", self.term.white)],
            "dim_lighting": [],
            
            # Heat effects
            "heat_waves": [("~", self.term.yellow), ("^", self.term.bright_yellow)],
            "extreme_heat_waves": [("~", self.term.bright_red), ("^", self.term.yellow)],
            "wilting_plants": [(",", self.term.yellow), (".", self.term.green)],
            "cracked_ground": [("#", self.term.yellow), ("=", self.term.bright_yellow)],
            
            # Special effects
            "fireflies": [("*", self.term.bright_yellow), (".", self.term.yellow)],
            "sparkles": [("*", self.term.bright_white), ("+", self.term.bright_cyan)],
            "sun_sparkles": [("*", self.term.bright_yellow)],
            "golden_light": [("*", self.term.bright_yellow), (".", self.term.yellow)],
            "warm_glow": [(".", self.term.yellow)],
            "mystical_glow": [("*", self.term.bright_magenta), (".", self.term.magenta)],
            "rainbow_arc": [("=", self.term.bright_red), ("=", self.term.bright_yellow), ("=", self.term.bright_green), ("=", self.term.bright_cyan)],
            "aurora_glow": [("|", self.term.green), ("/", self.term.cyan), ("\\", self.term.magenta)],
            "color_waves": [("~", self.term.green), ("~", self.term.cyan), ("~", self.term.magenta)],
            "lightning_flashes": [("!", self.term.bright_yellow)],
            "streaking_lights": [("\\", self.term.bright_white), ("/", self.term.white)],
        }
        
        # Generate decorations based on active effects
        for effect in env_effects:
            decorations = effect_decorations.get(effect, [])
            if not decorations:
                continue
            
            # Determine density based on effect type
            density = 3  # Default number of decorations per effect
            if "pile" in effect or "cover" in effect:
                density = 5
            elif "heavy" in effect or "deep" in effect:
                density = 6
            elif "light" in effect or "small" in effect:
                density = 2
            
            for _ in range(density):
                char, color = random.choice(decorations)
                x = random.randint(1, width - len(char) - 1)
                y = random.randint(height // 2, height - 2)  # Bottom half of screen
                self._weather_decorations.append((x, y, char, color))

    def _generate_playfield_decorations(self):
        """Generate random decorations for the playfield."""
        self._playfield_objects = []

        # Add some flowers, rocks, grass tufts
        decorations = [
            ("flower", 3),
            ("grass", 5),
            ("rock", 2),
            ("mushroom", 1),
        ]

        for obj_type, count in decorations:
            for _ in range(count):
                x = random.randint(2, self.duck_pos.field_width - 5)
                y = random.randint(2, self.duck_pos.field_height - 3)
                self._playfield_objects.append((x, y, obj_type))
    
    def add_nest_to_playfield(self, x: int = 3, y: int = 8):
        """Add a nest at the specified position for the duck to use."""
        # Remove any existing nest first
        self._playfield_objects = [(ox, oy, ot) for ox, oy, ot in self._playfield_objects if ot != "nest"]
        # Add the nest at the specified position
        self._playfield_objects.append((x, y, "nest"))

    def _generate_ground_pattern(self, location: Optional[str] = None):
        """Generate static ground pattern based on current location."""
        if location:
            # Use location-specific ground pattern
            self._ground_pattern = generate_location_ground(
                location, 
                self.duck_pos.field_width, 
                self.duck_pos.field_height
            )
            # Generate location-specific decorations
            self._location_decorations = generate_location_decorations(
                location,
                self.duck_pos.field_width,
                self.duck_pos.field_height,
                count=15  # More decorations for visual interest
            )
            # Generate large scenery elements
            self._location_scenery = generate_location_scenery(
                location,
                self.duck_pos.field_width,
                self.duck_pos.field_height
            )
        else:
            # Default pattern
            self._ground_pattern = []
            for y in range(self.duck_pos.field_height):
                row = ""
                for x in range(self.duck_pos.field_width):
                    row += random.choice(GROUND_CHARS)
                self._ground_pattern.append(row)
            self._location_decorations = []
            self._location_scenery = []

    def _update_weather_particles(self, width: int, height: int, weather_type: Optional[str]):
        """Update animated weather particles."""
        # Reset particles if weather changed
        if weather_type != self._current_weather_type:
            self._weather_particles = []
            self._current_weather_type = weather_type
            self._weather_frame = 0

        if not weather_type:
            self._weather_particles = []
            return

        self._weather_frame += 1

        # Weather particle settings - Enhanced for many weather types
        # Note: sunny/clear weather has no particles (just a nice day)
        weather_chars = {
            # Rain variants
            "drizzle": ["'", ",", "'", "."],  # Light rain
            "rain": ["|", "|", "'", ",", ":", "'"],  # Rain streaks (alias for rainy)
            "rainy": ["|", "|", "'", ",", ":", "'"],  # Rain streaks
            "heavy_rain": ["|", "|", "|", "'", ",", "|", ":"],  # Heavy rain
            "spring_rain": ["|", "'", ",", "~"],  # Gentle spring rain
            "storm": ["|", "|", "'", ",", ":"],  # Storm rain
            "stormy": ["|", "|", "'", ",", ":"],  # Storm rain (alias)
            "thunderstorm": ["|", "|", "!", "|", ",", "!", ":"],  # Thunder + rain
            "summer_storm": ["|", "|", "|", "'", "!", "|"],  # Heavy summer storm
            
            # Snow variants  
            "light_snow": ["*", ".", "*", "."],  # Light snowflakes
            "snow": ["*", "*", "*", "*", ".", "o", "*"],  # Normal snow
            "snowy": ["*", "*", "*", "*", ".", "o", "*"],  # Normal snow (alias)
            "heavy_snow": ["*", "*", "o", "*", "*", "O", "*"],  # Heavy snowfall
            "flurries": ["*", ".", "*", ".", "*"],  # Dancing flurries
            "blizzard": ["*", "*", "*", "/", "\\", "*", "O"],  # Blowing blizzard
            
            # Ice variants
            "sleet": ["'", "|", "'", ",", "|", "."],  # Mixed ice/rain
            "hail": ["o", "o", "O", "o", "."],  # Ice balls
            "ice_storm": ["|", "'", "o", "|", "'"],  # Freezing rain
            
            # Fog/mist
            "fog": [".", "~", "~", "~", " ", "#"],  # Thick fog
            "foggy": [".", "~", "~", "~", " ", "#"],  # Thick fog (alias)
            "mist": [".", "~", " ", "~", "."],  # Light mist
            
            # Wind variants
            "wind": [">", ">", "~", ">", "~", "-", "~"],  # Standard wind
            "windy": [">", ">", "~", ">", "~", "-", "~"],  # Standard wind (alias)
            "gentle_wind": ["~", "-", "~", " ", "~"],  # Gentle breeze
            "autumn_wind": [">", "}", "{", ">", "~"],  # Fall wind with leaves
            
            # Leaf particles
            "falling_leaves": ["{", "}", "(", ")", "~"],  # Drifting leaves
            "leaf_storm": ["{", "}", "{", ">", "}", ">", "{"],  # Swirling leaves
            
            # Special effects
            "pollen": [".", "°", ".", "°", "."],  # Floating pollen
            "heat_shimmer": ["~", "~", "^", "~"],  # Heat waves rising
            "moonlight": ["*", ".", "*", "."],  # Moonlit sparkles
            "golden_sparkles": ["*", "+", "*", "."],  # Golden hour magic
            "sparkles": ["*", "+", "*", ".", "+"],  # Generic sparkles
            
            # Rare/magical
            "rainbow": ["*", "*", "*", "*", "*"],  # Rainbow sparkles
            "aurora": ["|", "/", "\\", "|", "~"],  # Northern lights
            "meteors": ["\\", "/", "*", "."],  # Shooting stars
        }

        particle_density = {
            # Rain variants
            "drizzle": 0.08,
            "rain": 0.20,
            "rainy": 0.20,
            "heavy_rain": 0.30,
            "spring_rain": 0.15,
            "storm": 0.25,
            "stormy": 0.25,
            "thunderstorm": 0.28,
            "summer_storm": 0.30,
            
            # Snow variants
            "light_snow": 0.06,
            "snow": 0.12,
            "snowy": 0.12,
            "heavy_snow": 0.20,
            "flurries": 0.08,
            "blizzard": 0.35,
            
            # Ice variants
            "sleet": 0.18,
            "hail": 0.15,
            "ice_storm": 0.22,
            
            # Fog/mist
            "fog": 0.15,
            "foggy": 0.15,
            "mist": 0.08,
            
            # Wind variants
            "wind": 0.10,
            "windy": 0.10,
            "gentle_wind": 0.05,
            "autumn_wind": 0.12,
            
            # Leaf particles
            "falling_leaves": 0.08,
            "leaf_storm": 0.18,
            
            # Special effects
            "pollen": 0.06,
            "heat_shimmer": 0.04,
            "moonlight": 0.03,
            "golden_sparkles": 0.05,
            "sparkles": 0.06,
            
            # Rare/magical
            "rainbow": 0.08,
            "aurora": 0.10,
            "meteors": 0.02,
        }

        particle_speed = {
            # Rain variants (fast, downward)
            "drizzle": 1.2,
            "rain": 2.0,
            "rainy": 2.0,
            "heavy_rain": 2.5,
            "spring_rain": 1.5,
            "storm": 2.5,
            "stormy": 2.5,
            "thunderstorm": 2.8,
            "summer_storm": 3.0,
            
            # Snow variants (slow, gentle)
            "light_snow": 0.3,
            "snow": 0.4,
            "snowy": 0.4,
            "heavy_snow": 0.5,
            "flurries": 0.35,
            "blizzard": 0.8,
            
            # Ice variants
            "sleet": 1.8,
            "hail": 2.2,
            "ice_storm": 2.0,
            
            # Fog/mist (very slow drift)
            "fog": 0.15,
            "foggy": 0.15,
            "mist": 0.1,
            
            # Wind variants (fast horizontal)
            "wind": 1.5,
            "windy": 1.5,
            "gentle_wind": 0.8,
            "autumn_wind": 1.2,
            
            # Leaf particles (medium, drifting)
            "falling_leaves": 0.6,
            "leaf_storm": 1.0,
            
            # Special effects
            "pollen": 0.2,
            "heat_shimmer": -0.3,  # Rises up
            "moonlight": 0.4,
            "golden_sparkles": 0.3,
            "sparkles": 0.4,
            
            # Rare/magical
            "rainbow": 0.5,
            "aurora": 0.2,
            "meteors": 3.5,
        }

        chars = weather_chars.get(weather_type, [])
        density = particle_density.get(weather_type, 0)
        speed = particle_speed.get(weather_type, 1.0)

        if not chars:
            return

        # Move existing particles
        new_particles = []
        for x, y, char in self._weather_particles:
            new_y = y + speed

            # Horizontal drift for different weather types
            # Wind types - strong rightward movement
            if weather_type in ("windy", "wind", "blizzard", "leaf_storm"):
                new_x = x + 0.8
            # Autumn/gentle wind - moderate rightward
            elif weather_type in ("autumn_wind", "gentle_wind", "breezy"):
                new_x = x + 0.5
            # Snow types - gentle random drift
            elif weather_type in ("snowy", "snow", "light_snow", "heavy_snow", "flurries"):
                new_x = x + random.uniform(-0.3, 0.3)
            # Leaves - swaying drift
            elif weather_type == "falling_leaves":
                new_x = x + random.uniform(-0.4, 0.4)
            # Storm types - chaotic
            elif weather_type in ("stormy", "storm", "thunderstorm", "summer_storm"):
                new_x = x + random.uniform(-0.5, 0.5)
            # Aurora - gentle wave motion
            elif weather_type == "aurora":
                import math
                new_x = x + math.sin(self._weather_frame * 0.1 + y) * 0.3
            # Meteors - diagonal streak
            elif weather_type == "meteors":
                new_x = x + 1.5  # Fast diagonal
            # Pollen - floating drift
            elif weather_type == "pollen":
                new_x = x + random.uniform(-0.2, 0.4)
            # Heat shimmer - slight wave
            elif weather_type == "heat_shimmer":
                import math
                new_x = x + math.sin(self._weather_frame * 0.2 + x) * 0.2
            else:
                new_x = x

            if new_y < height and 0 <= new_x < width:
                new_particles.append((new_x, new_y, char))

        # Spawn new particles at top (or bottom for heat shimmer)
        spawn_y = height - 1 if weather_type == "heat_shimmer" else 0.0
        for x in range(width):
            if random.random() < density:
                char = random.choice(chars)
                new_particles.append((float(x), spawn_y, char))

        # Lightning flash for storms (rare and brief)
        if weather_type in ("stormy", "storm", "thunderstorm", "summer_storm", "ice_storm"):
            if self._weather_frame % 45 == 0 and random.random() < 0.25:
                bolt_x = random.randint(3, width - 3)
                bolt_y = random.randint(0, min(3, height - 1))
                new_particles.append((float(bolt_x), float(bolt_y), "!"))
                # Double flash for thunderstorms
                if weather_type == "thunderstorm" and random.random() < 0.5:
                    bolt_x2 = random.randint(3, width - 3)
                    new_particles.append((float(bolt_x2), float(bolt_y + 1), "!"))

        # Aurora color waves effect
        if weather_type == "aurora":
            # Add horizontal lines that drift
            if self._weather_frame % 10 == 0:
                wave_y = random.randint(0, min(5, height - 1))
                for wx in range(0, width, random.randint(3, 6)):
                    char = random.choice(["|", "~", "/", "\\"])
                    new_particles.append((float(wx), float(wave_y), char))

        self._weather_particles = new_particles

    def _get_time_of_day_elements(self, width: int) -> Tuple[str, Optional[Any], List[Tuple[int, str]]]:
        """
        Get time-of-day visual elements.
        Returns (sky_char, bg_color_func, celestial_objects)
        celestial_objects is a list of (x_position, character) for sun/moon/stars
        """
        from datetime import datetime
        hour = datetime.now().hour

        # Define time periods with visual elements
        if 5 <= hour < 7:  # Dawn
            sky_char = "."
            bg_color = self.term.on_color_rgb(255, 200, 150)  # Warm orange-pink
            celestials = [(width - 5, "-*-"), (3, "*"), (width - 10, "*")]
        elif 7 <= hour < 11:  # Morning
            sky_char = " "
            bg_color = None  # Clear sky
            celestials = [(width // 4, "*"), (5, "*"), (width - 8, "*")]
        elif 11 <= hour < 14:  # Midday
            sky_char = " "
            bg_color = None
            celestials = [(width // 2, "*")]
        elif 14 <= hour < 17:  # Afternoon
            sky_char = " "
            bg_color = None
            celestials = [(3 * width // 4, "*"), (width // 4, "*")]
        elif 17 <= hour < 19:  # Evening
            sky_char = "."
            bg_color = self.term.on_color_rgb(255, 180, 100)  # Golden hour
            celestials = [(width - 3, "-*-"), (width // 2, "*")]
        elif 19 <= hour < 21:  # Dusk
            sky_char = "▒"
            bg_color = self.term.on_color_rgb(100, 80, 120)  # Purple dusk
            celestials = [(width - 4, "-*-"), (5, "*"), (width // 2, "*")]
        elif 21 <= hour or hour < 0:  # Night
            sky_char = " "
            bg_color = self.term.on_color_rgb(20, 20, 40)  # Dark blue
            celestials = [
                (width - 5, ")"),
                (3, "*"), (8, "*"), (15, "*"), (width - 12, "*"),
                (width // 2 - 3, "*"), (width // 2 + 5, "*")
            ]
        else:  # Late night (0-5)
            sky_char = " "
            bg_color = self.term.on_color_rgb(10, 10, 25)  # Very dark
            celestials = [
                (width - 6, "o"),
                (4, "*"), (10, "*"), (18, "*"), (width - 15, "*"),
                (width // 3, "*"), (2 * width // 3, "*")
            ]

        return sky_char, bg_color, celestials

    def _get_weather_ambient_effects(self, weather_type: Optional[str], width: int) -> List[str]:
        """Get ambient text effects for weather displayed at top of playfield."""
        if not weather_type:
            return []

        effects = {
            # Common weather
            "sunny": ["~ warm sunbeams ~", "* bright and cheerful *"],
            "partly_cloudy": ["(*) clouds drift by (*)", "~ bits of blue sky ~"],
            "cloudy": ["(*) clouds gather (*)", "~ overcast skies ~"],
            "overcast": ["... grey blanket above ...", "~ dim and cozy ~"],
            "windy": ["~~ whoooosh! ~~", "~ leaves swirl ~", ">> breezy day >>"],
            "foggy": ["... mist swirls ...", "~ mysterious fog ~", "o.o visibility low o.o"],
            "misty": ["~ soft haze ~", "... gentle mist ..."],
            
            # Rain variants
            "drizzle": ["' light drops '", "~ gentle drizzle ~"],
            "rainy": ["' pitter patter '", "~ splish splash ~", "',' rain falls ','"],
            "heavy_rain": ["''' POURING '''", "~~ splashing puddles ~~"],
            "spring_rain": ["'~' April showers '~'", "~ flowers love this ~"],
            "stormy": ["! THUNDER RUMBLES !", "~~ wind howls ~~"],
            "thunderstorm": ["!! CRACK BOOM !!", "~~ lightning flashes ~~"],
            "summer_storm": ["!! dramatic storm !!", "~~ rolling thunder ~~"],
            
            # Snow/ice variants
            "frost": ["*.: frost crystals :.*", "~ delicate ice ~"],
            "light_snow": ["* gentle flakes *", "~ peaceful snow ~"],
            "snowy": ["* snowflakes drift *", "~ winter wonderland ~"],
            "heavy_snow": ["** HEAVY SNOW **", "~~ blanketed white ~~"],
            "blizzard": ["*** BLIZZARD ***", "~~ can't see! ~~"],
            "sleet": ["'o icy rain o'", "~ frozen drops ~"],
            "hail": ["O HAIL O", "~~ duck and cover! ~~"],
            "ice_storm": ["**. ICE STORM .**", "~~ everything frozen ~~"],
            
            # Spring specific
            "spring_showers": ["'~' refreshing rain '~'", "~ growth coming ~"],
            "rainbow": ["(=) magical colors! (=)", "* make a wish! *"],
            "pollen_drift": [".o pollen floats o.", "~ *ACHOO!* ~"],
            "warm_breeze": ["~ gentle warmth ~", "~ perfect day ~"],
            "dewy_morning": ["o.o morning dew o.o", "~ sparkly grass ~"],
            
            # Summer specific  
            "scorching": ["^^ SO HOT ^^", "~~ need shade! ~~"],
            "humid": ["... sticky air ...", "~ muggy weather ~"],
            "heat_wave": ["^^^ HEAT WAVE ^^^", "~~ drink water! ~~"],
            "balmy_evening": ["~ warm and lovely ~", "* fireflies appear *"],
            "golden_hour": ["*+* golden light *+*", "~ magical hour ~"],
            "muggy": ["... thick air ...", "~ so humid ~"],
            
            # Fall specific
            "crisp": ["~ cool and fresh ~", "* autumn air *"],
            "breezy": ["~> autumn breeze <~", "~ leaves dancing ~"],
            "leaf_storm": ["{}{ LEAVES SWIRL }{}}", "~ colorful chaos ~"],
            "harvest_moon": ["O big orange moon O", "~ mystical night ~"],
            "first_frost": ["*.: first frost :.*", "~ winter approaches ~"],
            "autumnal": ["{} colorful leaves {}", "~ perfect fall day ~"],
            
            # Winter specific
            "bitter_cold": ["!!! FREEZING !!!", "~~ brrrrr! ~~"],
            "freezing": ["** everything frozen **", "~ ice crystals ~"],
            "clear_cold": ["* cold but bright *", "~ crisp winter day ~"],
            "snow_flurries": ["* dancing flakes *", "~ playful snow ~"],
            "winter_sun": ["*o bright but cold o*", "~ sparkly snow ~"],
            
            # Rare/special
            "aurora": ["|/| NORTHERN LIGHTS |\\|", "~ magical sky ~"],
            "meteor_shower": ["\\*/ SHOOTING STARS \\*/", "~ make wishes! ~"],
            "double_rainbow": ["=== DOUBLE RAINBOW ===", "** WHAT DOES IT MEAN **"],
            "perfect_day": ["*** PERFECT DAY ***", "~ everything is magical ~"],
        }

        return effects.get(weather_type, [])

    def clear(self):
        """Clear the terminal."""
        print(self.term.home + self.term.clear)

    def render_frame(self, game: "Game"):
        """
        Render a complete frame with side panel layout.
        Responsive to terminal size.

        Args:
            game: Game instance with current state
        """
        duck = game.duck
        if duck is None:
            self._render_title_screen()
            return

        # Check for active minigame - render minigame instead of normal frame
        if hasattr(game, '_active_minigame') and game._active_minigame:
            self._render_minigame_frame(game)
            return

        # Update duck position
        delta = time.time() - self._last_render_time if self._last_render_time else 0.033
        self.duck_pos.update(delta)
        self._last_render_time = time.time()

        # Get terminal size - cap to reasonable maximum for consistent gameplay
        MAX_WIDTH = 116   # Maximum game width
        MAX_HEIGHT = 35   # Maximum game height
        
        term_width = max(self.term.width, 60)
        term_height = max(self.term.height, 20)
        
        new_width = min(term_width, MAX_WIDTH)
        new_height = min(term_height, MAX_HEIGHT)
        
        # Use cached dimensions to prevent micro-jitter from terminal size fluctuations
        # Only update if dimensions changed by more than 2 chars, or if not yet cached
        if (self._cached_width is None or self._cached_height is None or
            abs(new_width - self._cached_width) > 2 or 
            abs(new_height - self._cached_height) > 2):
            self._cached_width = new_width
            self._cached_height = new_height
        
        width = self._cached_width
        height = self._cached_height

        # Dynamic layout based on terminal width
        # Side panel needs at least 25 chars, playfield gets the rest
        side_panel_width = max(25, min(35, width // 3))
        playfield_width = width - side_panel_width

        # Update playfield dimensions for duck movement
        field_inner_width = playfield_width - 2
        field_height = max(8, height - 10)  # Leave room for header, controls, messages
        self.duck_pos.field_width = field_inner_width
        self.duck_pos.field_height = field_height

        # Get current location from exploration system
        current_location = None
        if hasattr(game, 'exploration') and game.exploration and game.exploration.current_area:
            current_location = game.exploration.current_area.name

        # Regenerate ground pattern if size or location changed, or on first render
        size_changed = len(self._ground_pattern) != field_height or (self._ground_pattern and len(self._ground_pattern[0]) != field_inner_width)
        location_changed = current_location != self._current_location
        
        # Track if this is first render for screen clear later
        is_first_render = self._first_render

        if size_changed or location_changed or self._first_render:
            self._current_location = current_location
            self._generate_ground_pattern(current_location)
            self._first_render = False

        # Build the frame
        output = []

        # Header spanning full width - include currency, weather, and season if available
        currency = game.habitat.currency if hasattr(game, 'habitat') else 0
        weather_info = None
        season_info = None
        if hasattr(game, 'atmosphere') and game.atmosphere:
            weather_info = game.atmosphere.current_weather
            season_info = game.atmosphere.current_season
        output.extend(self._render_header_bar(duck, width, currency, weather_info, season_info=season_info))

        # Get equipped cosmetics and placed items from habitat
        equipped_cosmetics = game.habitat.equipped_cosmetics if hasattr(game, 'habitat') else {}
        # Placed items (ball, etc.) only appear at Home Pond - use get_visible_placed_items to respect stored status
        if current_location == "Home Pond" or current_location is None:
            placed_items = game.habitat.get_visible_placed_items() if hasattr(game, 'habitat') else []
        else:
            placed_items = []

        # Get built structures from building system (only show at Home Pond)
        built_structures = []
        if (current_location == "Home Pond" or current_location is None) and hasattr(game, 'building') and game.building:
            built_structures = [s for s in game.building.structures if s.status.value == "complete"]

        # Get current visitor info from friends system
        current_visitor = None
        if hasattr(game, 'friends') and game.friends and game.friends.current_visit:
            visitor_id = game.friends.current_visit.friend_id
            current_visitor = game.friends.get_friend_by_id(visitor_id)

        # Get active event animators from game
        event_animators = getattr(game, '_event_animators', [])

        # Main area: playfield on left, side panel on right
        playfield_lines = self._render_playfield(duck, playfield_width, field_height, 
                                                   equipped_cosmetics, placed_items, weather_info,
                                                   built_structures, current_visitor, event_animators)
        sidepanel_lines = self._render_side_panel(duck, game, side_panel_width)

        # Combine playfield and side panel
        max_lines = max(len(playfield_lines), len(sidepanel_lines))
        for i in range(max_lines):
            pf_line = playfield_lines[i] if i < len(playfield_lines) else " " * playfield_width
            sp_line = sidepanel_lines[i] if i < len(sidepanel_lines) else " " * side_panel_width
            # Pad lines to exact visible width (accounting for ANSI escape codes)
            pf_line = _visible_ljust(pf_line, playfield_width)
            sp_line = _visible_ljust(sp_line, side_panel_width)
            output.append(pf_line + sp_line)

        # Progress bars (Level/XP and Growth)
        output.extend(self._render_progress_bars(width, game))

        # Controls bar
        output.extend(self._render_controls_bar(width))

        # Check for expired closeup
        self._check_closeup_expired()

        # Check for expired celebration
        self._check_celebration_expired()

        # Overlays (help, stats, inventory, celebration, item interaction, fishing)
        if self._show_celebration:
            output = self._overlay_celebration(output, width)
        elif hasattr(game, '_item_interaction_active') and game._item_interaction_active:
            output = self._overlay_item_interaction(output, game, width)
        elif hasattr(game, 'fishing') and game.fishing.is_fishing:
            output = self._overlay_fishing(output, game, width)
        elif self._show_help:
            output = self._overlay_help(output, width)
        elif self._show_stats:
            output = self._overlay_stats(output, duck, game, width)
        elif self._show_talk:
            output = self._overlay_talk(output, width)
        elif self._show_inventory:
            output = self._overlay_inventory(output, game, width)
        elif self._show_shop:
            output = self._overlay_shop(output, game.habitat, width)
        elif self._menu_overlay_active:
            # Menu overlays (debug menu, settings, etc.) - always show
            output = self._overlay_menu(output, width)
        elif self._show_message_overlay and not getattr(self, '_message_rendered_inline', False):
            output = self._overlay_message(output, width)

        # Print frame - clear on first render to remove title screen remnants
        if is_first_render:
            print(self.term.home + self.term.clear, end="")
        else:
            print(self.term.home, end="")
            
        # Print all output lines, not limited by height
        max_lines = min(len(output), self.term.height - 1)
        for i in range(max_lines):
            line = output[i]
            # Use move to ensure proper positioning and overwrite
            # Use ANSI-aware functions for lines that may contain color codes
            truncated = _visible_truncate(line, width)
            padded = _visible_ljust(truncated, width)
            # End each line with terminal reset to prevent color bleeding
            print(self.term.move(i, 0) + padded + self.term.normal, end="")

    def _render_header_bar(self, duck: "Duck", width: int, currency: int = 0, weather=None, time_info=None, season_info=None) -> List[str]:
        """Render the top header bar with weather, season, and time info."""
        from datetime import datetime

        mood = duck.get_mood()
        age_days = duck.get_age_days()

        if age_days < 1:
            age_str = f"{int(age_days * 24)}h"
        else:
            age_str = f"{int(age_days)}d"

        # Mood emoji/indicator
        mood_indicators = {
            "ecstatic": "[*o*]",
            "happy": "[^-^]",
            "content": "[-.-]",
            "grumpy": "[>_<]",
            "sad": "[;_;]",
            "miserable": "[T_T]",
        }
        mood_ind = mood_indicators.get(mood.state.value, "[...]")

        # Season icons and names
        season_data = {
            "spring": ("~*~", "Spring"),
            "summer": ("-*-", "Summer"),
            "fall": ("{~}", "Fall"),
            "winter": ("*.*", "Winter"),
        }

        # Weather icons and names
        weather_data = {
            # Common (all seasons)
            "sunny": ("*", "Sunny"),
            "partly_cloudy": ("*~", "Partly Cloudy"),
            "cloudy": ("(*)", "Cloudy"),
            "overcast": ("(~)", "Overcast"),
            "windy": ("~~", "Windy"),
            "foggy": ("...", "Foggy"),
            "misty": ("...", "Misty"),
            # Rain variations
            "drizzle": ("'", "Drizzle"),
            "rainy": ("','", "Rainy"),
            "heavy_rain": ("'''", "Heavy Rain"),
            "stormy": ("!!!", "Stormy"),
            "thunderstorm": ("!*!", "Thunderstorm"),
            # Snow/ice variations
            "light_snow": ("*", "Light Snow"),
            "snowy": ("*", "Snowy"),
            "heavy_snow": ("***", "Heavy Snow"),
            "blizzard": ("***", "Blizzard"),
            "sleet": ("'*", "Sleet"),
            "hail": ("o'o", "Hail"),
            "frost": ("*.*", "Frost"),
            "ice_storm": ("*!*", "Ice Storm"),
            # Spring specific
            "spring_showers": ("'~'", "Spring Showers"),
            "rainbow": ("(=)", "Rainbow"),
            "pollen_drift": ("o~o", "Pollen"),
            "warm_breeze": ("~*~", "Warm Breeze"),
            "dewy_morning": ("'*'", "Dewy"),
            # Summer specific
            "scorching": ("**", "Scorching"),
            "humid": ("~'~", "Humid"),
            "heat_wave": ("***", "Heat Wave"),
            "summer_storm": ("!'!", "Summer Storm"),
            "balmy_evening": ("~*", "Balmy"),
            "golden_hour": ("*-*", "Golden Hour"),
            "muggy": ("~'", "Muggy"),
            # Fall specific
            "crisp": ("*~", "Crisp"),
            "breezy": ("~~", "Breezy"),
            "leaf_storm": ("{~}", "Leaf Storm"),
            "harvest_moon": ("O", "Harvest Moon"),
            "first_frost": ("*.", "First Frost"),
            "autumnal": ("{*}", "Autumnal"),
            # Winter specific
            "bitter_cold": ("***", "Bitter Cold"),
            "freezing": ("*!*", "Freezing"),
            "clear_cold": ("*.", "Clear Cold"),
            "snow_flurries": ("*~*", "Flurries"),
            "winter_sun": ("*o*", "Winter Sun"),
            # Rare/special
            "aurora": ("~*~", "Aurora"),
            "meteor_shower": ("*!*", "Meteors"),
            "double_rainbow": ("(==)", "Double Rainbow"),
            "perfect_day": ("*O*", "Perfect Day"),
        }

        # Time of day icons and names
        time_data = {
            "dawn": ("-*-", "Dawn"),
            "morning": ("*", "Morning"),
            "midday": ("*", "Midday"),
            "afternoon": ("*", "Afternoon"),
            "evening": ("-*-", "Evening"),
            "dusk": ("-*-", "Dusk"),
            "night": (")", "Night"),
            "late_night": ("o", "Late Night"),
        }

        # Build season string with icon and label
        season_part = ""
        if season_info:
            s_icon, s_name = season_data.get(season_info.value, ("", ""))
            season_part = f"{s_icon} {s_name}"

        # Build weather string with icon and label
        weather_part = ""
        if weather:
            w_icon, w_name = weather_data.get(weather.weather_type.value, ("?", "Unknown"))
            weather_part = f"{w_icon} {w_name}"

        # Build time string with icon, time, and period
        now = datetime.now()
        time_str = now.strftime("%H:%M")
        hour = now.hour

        # Determine time of day
        if 5 <= hour < 7:
            tod = "dawn"
        elif 7 <= hour < 11:
            tod = "morning"
        elif 11 <= hour < 14:
            tod = "midday"
        elif 14 <= hour < 17:
            tod = "afternoon"
        elif 17 <= hour < 19:
            tod = "evening"
        elif 19 <= hour < 21:
            tod = "dusk"
        elif 21 <= hour or hour < 0:
            tod = "night"
        else:
            tod = "late_night"

        t_icon, t_name = time_data.get(tod, ("⏰", ""))
        time_part = f" {t_icon} {time_str} {t_name} "

        # Build header parts - use simpler format to avoid cutoff
        name_part = duck.name
        mood_desc = mood.description  # "tolerating existence quite well", etc.
        mood_part = f"{mood_desc} {mood_ind}"
        age_part = age_str
        coin_part = f"${currency}"

        # Create bordered header
        inner_width = width - 2

        # Simplified format: Name | Season Weather | Time | Mood Age $Money
        left_side = f" {name_part} "
        if season_part or weather_part:
            left_side += "|"
            if season_part:
                left_side += f" {season_part}"
            if weather_part:
                left_side += f" {weather_part}"
        left_side += f" | {time_part.strip()}"

        right_side = f"{mood_part} {age_part} {coin_part} "

        # Calculate padding
        left_len = _visible_len(left_side)
        right_len = _visible_len(right_side)
        pad_len = max(0, inner_width - left_len - right_len)

        line1 = left_side + " " * pad_len + right_side

        # Ensure line fits
        line1 = _visible_ljust(line1, inner_width)
        line1 = _visible_truncate(line1, inner_width)

        lines = [
            BOX_DOUBLE["tl"] + BOX_DOUBLE["h"] * inner_width + BOX_DOUBLE["tr"],
            BOX_DOUBLE["v"] + line1 + BOX_DOUBLE["v"],
            BOX_DOUBLE["bl"] + BOX_DOUBLE["h"] * inner_width + BOX_DOUBLE["br"],
        ]
        return lines

    def _render_playfield(self, duck: "Duck", width: int, height: int = None,
                          equipped_cosmetics: Dict[str, str] = None,
                          placed_items: List = None,
                          weather_info = None,
                          built_structures: List = None,
                          current_visitor = None,
                          event_animators: List = None) -> List[str]:
        """Render the main playfield where duck moves around with time/weather visuals."""
        inner_width = width - 2
        lines = []

        # Get particle type from weather data for more specific particle rendering
        field_height = height if height else self.duck_pos.field_height
        weather_type = weather_info.weather_type.value if weather_info else None
        particle_type = None
        env_effects = []
        
        if weather_info and hasattr(weather_info, 'weather_type'):
            from world.atmosphere import WEATHER_DATA
            weather_data = WEATHER_DATA.get(weather_info.weather_type, {})
            env_effects = weather_data.get("env_effects", [])
            particle_type = weather_data.get("particle_type")
        
        # Update weather particles (use particle_type for specific effects, fallback to weather_type)
        self._update_weather_particles(inner_width, field_height, particle_type or weather_type)
        
        # Generate environmental weather decorations (puddles, snow piles, etc.)
        self._generate_weather_decorations(
            weather_type,  # Use weather_type for decoration context
            env_effects, 
            inner_width, 
            field_height
        )

        # Get time-of-day visual elements
        sky_char, time_bg_color, celestials = self._get_time_of_day_elements(inner_width)

        # Title bar with weather/time flavor text
        title = " DUCK HABITAT "
        weather_effects = self._get_weather_ambient_effects(weather_type, inner_width)
        if weather_effects and self._weather_frame % 60 < 30:
            # Show rotating weather flavor text
            effect_text = weather_effects[(self._weather_frame // 60) % len(weather_effects)]
            if len(effect_text) < inner_width - 4:
                title = f" {effect_text} "
        pad = (inner_width - len(title)) // 2
        lines.append(BOX["tl"] + BOX["h"] * pad + title + BOX["h"] * (inner_width - pad - len(title)) + BOX["tr"])

        # Create the playfield grid - use passed height or fall back to duck_pos
        field_height = height if height is not None else self.duck_pos.field_height

        # Get mini duck art for playfield
        duck_art = get_mini_duck(
            duck.growth_stage,
            self.duck_pos.get_state(),
            self.duck_pos.facing_right,
            self.duck_pos.get_animation_frame()
        )
        
        # Get cosmetics overlay as a grid of (char, color_func) tuples
        duck_grid = None
        if equipped_cosmetics:
            duck_grid = self._cosmetics_renderer.render_duck_with_cosmetics(duck_art, equipped_cosmetics)
        
        duck_height = len(duck_art)
        duck_width = max(len(line) for line in duck_art) if duck_art else 0

        # Handle visitor NPC animation
        visitor_art = None
        visitor_x = 0
        visitor_y = 0
        if current_visitor:
            from world.friends import visitor_animator
            personality = current_visitor.personality.value if hasattr(current_visitor.personality, 'value') else str(current_visitor.personality)
            # Don't re-set the visitor if already active (preserves state)
            if visitor_animator._personality != personality.lower():
                # Get friendship level info
                friendship_level = current_visitor.friendship_level.value if hasattr(current_visitor.friendship_level, 'value') else str(current_visitor.friendship_level)
                visit_number = current_visitor.times_visited if hasattr(current_visitor, 'times_visited') else 1
                unlocked_topics = set(current_visitor.unlocked_dialogue) if hasattr(current_visitor, 'unlocked_dialogue') else set()
                # Get shared experiences for LLM context
                shared_experiences = getattr(current_visitor, 'shared_experiences', [])
                shared_memories = list(shared_experiences)[:5] if shared_experiences else []
                visitor_animator.set_visitor(
                    personality, 
                    current_visitor.name,
                    friendship_level,
                    visit_number,
                    unlocked_topics,
                    duck_ref=duck,
                    shared_memories=shared_memories
                )
            # Update visitor with duck's actual screen position
            duck_screen_x = self.duck_pos.x
            duck_screen_y = self.duck_pos.y
            visitor_animator.update(time.time(), duck_screen_x, duck_screen_y)
            # Get absolute position from animator
            visitor_x, visitor_y = visitor_animator.get_position()
            # Keep in screen bounds
            visitor_x = max(0, min(visitor_x, inner_width - 10))
            visitor_y = max(0, min(visitor_y, field_height - 4))
            visitor_art = visitor_animator.get_current_art()

        # Pre-calculate all item placements with multi-line art
        # Each entry: (x, y, art_lines, color_func)
        from ui.habitat_art import get_item_art, get_item_color, get_structure_art, get_structure_color
        
        # Get the item being animated (if any) to hide it from the playfield
        animating_item_id = self.interaction_animator.get_animating_item_id()
        
        item_placements = []
        if placed_items:
            for placed_item in placed_items:
                # Skip the item being animated - it's shown in the animation instead
                if animating_item_id and placed_item.item_id == animating_item_id:
                    continue
                art = get_item_art(placed_item.item_id)
                color_func = get_item_color(placed_item.item_id)
                # Use display position which includes animation offset
                display_x, display_y = placed_item.get_display_position()
                # Scale item position to playfield coordinates
                item_x = int(display_x * inner_width / 20)
                item_y = int(display_y * field_height / 12)
                item_placements.append((item_x, item_y, art, color_func))
        
        # Add built structures to item placements
        if built_structures:
            for i, structure in enumerate(built_structures):
                art = get_structure_art(structure.blueprint_id)
                color_name = get_structure_color(structure.blueprint_id)
                # Convert color name to terminal color function
                color_func = None
                if color_name:
                    color_map = {
                        "yellow": self.term.yellow,
                        "bright_yellow": self.term.bright_yellow,
                        "red": self.term.red,
                        "white": self.term.white,
                        "cyan": self.term.cyan,
                        "bright_cyan": self.term.bright_cyan,
                        "green": self.term.green,
                        "magenta": self.term.magenta,
                    }
                    color_func = color_map.get(color_name)
                # Position structures at their grid position, or space them out if position not set
                if hasattr(structure, 'position') and structure.position:
                    struct_x = int(structure.position[0] * inner_width / 10)
                    struct_y = int(structure.position[1] * field_height / 8)
                else:
                    # Default spacing if no position
                    struct_x = 2 + (i * 8) % (inner_width - 10)
                    struct_y = field_height - len(art) - 1
                item_placements.append((struct_x, struct_y, art, color_func))

        # Build each row of the playfield
        # Use a grid of (char, color_func) tuples to handle colors properly
        # Get ground color for current location
        ground_color = get_ground_color(self._current_location) if self._current_location else None
        
        for y in range(field_height):
            # Initialize row with (char, ground_color) tuples for ground pattern
            row = [(c, ground_color if c != ' ' else None) for c in self._ground_pattern[y][:inner_width]]
            # Pad to inner_width
            while len(row) < inner_width:
                row.append((' ', None))

            # Add location-specific scenery (large multi-line elements) - render first (background)
            for scene_x, scene_y, scene_art in self._location_scenery:
                scene_row_index = y - scene_y
                if 0 <= scene_row_index < len(scene_art):
                    scene_line = scene_art[scene_row_index]
                    for dx, char in enumerate(scene_line):
                        px = scene_x + dx
                        if char != ' ' and 0 <= px < inner_width:
                            color_func = get_decoration_color(self._current_location or "", char)
                            row[px] = (char, color_func)

            # Add location-specific decorations
            for dec_x, dec_y, dec_char in self._location_decorations:
                if dec_y == y and 0 <= dec_x < inner_width:
                    color_func = get_decoration_color(self._current_location or "", dec_char)
                    row[dec_x] = (dec_char, color_func)

            # Add legacy decorations (built-in playfield objects) only if no location set
            if not self._current_location:
                for obj_x, obj_y, obj_type in self._playfield_objects:
                    if obj_y == y and 0 <= obj_x < inner_width:
                        obj_chars = PLAYFIELD_OBJECTS.get(obj_type, "*")
                        for i, char in enumerate(obj_chars):
                            if obj_x + i < inner_width:
                                row[obj_x + i] = (char, None)

            # Add weather-based environmental decorations (puddles, snow piles, leaves, etc.)
            for wx, wy, wchar, wcolor in self._weather_decorations:
                if wy == y:
                    for i, char in enumerate(wchar):
                        px = wx + i
                        if 0 <= px < inner_width:
                            existing_char, _ = row[px]
                            # Only place on empty ground, not over other objects
                            if existing_char == ' ' or existing_char in GROUND_CHARS:
                                row[px] = (char, wcolor)

            # Add placed habitat items (multi-line art)
            for item_x, item_y, art, color_func in item_placements:
                # Check if this row intersects with this item
                art_row_index = y - item_y
                if 0 <= art_row_index < len(art):
                    art_line = art[art_row_index]
                    for dx, char in enumerate(art_line):
                        px = item_x + dx
                        if char != ' ' and 0 <= px < inner_width:
                            row[px] = (char, color_func)

            # Add event animations (butterfly, bird, etc.) - render before duck so duck is on top
            if event_animators:
                for animator in event_animators:
                    from ui.event_animations import EventAnimationState, BreezeAnimator
                    
                    if animator.state == EventAnimationState.FINISHED:
                        continue
                    
                    # Handle particle-based animations (breeze)
                    if hasattr(animator, 'get_particles'):
                        # Color map for event animation colors
                        anim_color_map = {
                            "cyan": self.term.cyan,
                            "magenta": self.term.magenta,
                            "yellow": self.term.yellow,
                            "white": self.term.white,
                            "red": self.term.red,
                            "green": self.term.green,
                            "blue": self.term.blue,
                            "bright_yellow": self.term.bright_yellow,
                            "bright_cyan": self.term.bright_cyan,
                            "bright_magenta": self.term.bright_magenta,
                        }
                        particles = animator.get_particles()
                        particle_color = anim_color_map.get(animator.get_color(), self.term.cyan)
                        for px, py, char in particles:
                            if py == y and 0 <= px < inner_width:
                                existing_char, _ = row[px]
                                if existing_char == ' ' or existing_char in GROUND_CHARS:
                                    row[px] = (char, particle_color)
                    else:
                        # Sprite-based animations
                        anim_sprite = animator.get_sprite()
                        anim_x, anim_y = animator.get_position()
                        
                        # Color map for event animation colors
                        anim_color_map = {
                            "cyan": self.term.cyan,
                            "magenta": self.term.magenta,
                            "yellow": self.term.yellow,
                            "white": self.term.white,
                            "red": self.term.red,
                            "green": self.term.green,
                            "blue": self.term.blue,
                            "bright_yellow": self.term.bright_yellow,
                            "bright_cyan": self.term.bright_cyan,
                            "bright_magenta": self.term.bright_magenta,
                        }
                        anim_color = anim_color_map.get(animator.get_color(), self.term.cyan)
                        
                        # Check if this row intersects with this animation
                        anim_row_index = y - anim_y
                        if 0 <= anim_row_index < len(anim_sprite):
                            anim_line = anim_sprite[anim_row_index]
                            for dx, char in enumerate(anim_line):
                                px = anim_x + dx
                                if char != ' ' and 0 <= px < inner_width:
                                    row[px] = (char, anim_color)

            # Add visitor NPC if visiting (render before duck so duck is on top)
            if visitor_art and current_visitor:
                personality = current_visitor.personality.value if hasattr(current_visitor.personality, 'value') else str(current_visitor.personality)
                
                # Multi-color schemes for visitors (body, accessory, detail)
                visitor_color_schemes = {
                    "adventurous": {
                        "body": self.term.bright_yellow,
                        "accessory": self.term.green,  # Explorer hat
                        "detail": self.term.white,  # Eyes
                        "accent": self.term.brown if hasattr(self.term, 'brown') else self.term.yellow,
                    },
                    "scholarly": {
                        "body": self.term.bright_white,
                        "accessory": self.term.bright_blue,  # Glasses
                        "detail": self.term.blue,
                        "accent": self.term.cyan,
                    },
                    "artistic": {
                        "body": self.term.bright_white,
                        "accessory": self.term.bright_magenta,  # Beret
                        "detail": self.term.magenta,
                        "accent": self.term.bright_cyan,
                    },
                    "playful": {
                        "body": self.term.bright_yellow,
                        "accessory": self.term.bright_red,  # Propeller hat
                        "detail": self.term.bright_green,
                        "accent": self.term.cyan,
                    },
                    "mysterious": {
                        "body": self.term.white,
                        "accessory": self.term.magenta,  # Mask
                        "detail": self.term.bright_magenta,
                        "accent": self.term.blue,
                    },
                    "generous": {
                        "body": self.term.bright_yellow,
                        "accessory": self.term.bright_red,  # Bow tie
                        "detail": self.term.white,
                        "accent": self.term.magenta,
                    },
                    "foodie": {
                        "body": self.term.yellow,
                        "accessory": self.term.bright_white,  # Chef hat
                        "detail": self.term.red,
                        "accent": self.term.green,
                    },
                    "athletic": {
                        "body": self.term.bright_yellow,
                        "accessory": self.term.bright_red,  # Headband
                        "detail": self.term.cyan,
                        "accent": self.term.white,
                    },
                }
                
                colors = visitor_color_schemes.get(personality, {
                    "body": self.term.bright_cyan,
                    "accessory": self.term.white,
                    "detail": self.term.yellow,
                    "accent": self.term.cyan,
                })
                
                visitor_height = len(visitor_art)
                for dy in range(visitor_height):
                    if y == visitor_y + dy:
                        visitor_line = visitor_art[dy] if dy < len(visitor_art) else ""
                        for dx, char in enumerate(visitor_line):
                            px = visitor_x + dx
                            if char != ' ' and 0 <= px < inner_width:
                                # Color different parts differently
                                if char in ('o', 'O', '.', '^', '*', '0'):  # Eyes and expressions
                                    color = colors["detail"]
                                elif char in ('/', '\\', '^', '-', '_', '|') and dy == 0:  # Hat/accessory (first line)
                                    color = colors["accessory"]
                                elif char in ('#', '[', ']', '!', '?', '~', '>'):  # Special items/gifts
                                    color = colors["accent"]
                                elif char in (')', '(', '{', '}'):  # Body shape
                                    color = colors["body"]
                                else:
                                    color = colors["body"]
                                row[px] = (char, color)

            # Check if there's an interaction animation playing
            anim_render_data = self.interaction_animator.get_render_data()
            if anim_render_data:
                anim_lines, anim_pos, show_duck, item_color = anim_render_data
                anim_x, anim_y = anim_pos
                # Use item color if available, otherwise default to bright yellow
                anim_color = item_color if item_color else self.term.bright_yellow
                
                # Duck characters should stay yellow, item characters get item color
                # Duck parts: face, beak, body, wings, expressions
                duck_chars = set("()o>^v-_/\\'|~*")

                # Render animation frame
                for dy, anim_line in enumerate(anim_lines):
                    if y == anim_y + dy:
                        for dx, char in enumerate(anim_line):
                            px = anim_x + dx
                            if char != ' ' and 0 <= px < inner_width:
                                # Duck characters stay yellow, items get item color
                                if char in duck_chars:
                                    row[px] = (char, self.term.yellow)
                                else:
                                    row[px] = (char, anim_color)

            # Add duck if on this row (duck renders ON TOP of items)
            # Skip if animation is hiding the duck
            duck_y = self.duck_pos.y
            duck_x = self.duck_pos.x
            should_render_duck = not self.interaction_animator.should_hide_duck()

            if should_render_duck:
                for dy in range(duck_height):
                    if y == duck_y + dy:
                        if duck_grid:
                            # Use the cosmetics grid (has color info)
                            duck_row = duck_grid[dy] if dy < len(duck_grid) else []
                            for dx, (char, color_func) in enumerate(duck_row):
                                if char != ' ' and 0 <= duck_x + dx < inner_width:
                                    row[duck_x + dx] = (char, color_func)
                        else:
                            # No cosmetics, use plain duck art with yellow color
                            duck_line = duck_art[dy] if dy < len(duck_art) else ""
                            for dx, char in enumerate(duck_line):
                                if char != ' ' and 0 <= duck_x + dx < inner_width:
                                    row[duck_x + dx] = (char, self.term.yellow)

            # Add effect overlay above duck if any
            effect_overlay = animation_controller.get_effect_overlay()
            if effect_overlay:
                effect_offset_y = duck_y - len(effect_overlay)  # Render above duck
                effect_row_idx = y - effect_offset_y
                if 0 <= effect_row_idx < len(effect_overlay):
                    effect_line = effect_overlay[effect_row_idx]
                    effect_x = duck_x + (duck_width - len(effect_line)) // 2  # Center above duck
                    for dx, char in enumerate(effect_line):
                        px = effect_x + dx
                        if char != ' ' and 0 <= px < inner_width:
                            # Use bright yellow for effects
                            row[px] = (char, self.term.bright_yellow)

            # Add weather particles (rendered on top of everything except text)
            # Enhanced colors for more dramatic weather effects
            # Note: sunny weather has no particles, just clear sky
            weather_colors = {
                "rainy": self.term.cyan,           # Cool rain color
                "stormy": self.term.bright_white,  # Bright storm
                "snowy": self.term.bright_white,   # White snow
                "foggy": self.term.white,          # Misty fog
                "windy": self.term.bright_cyan,    # Wind streaks
                "rainbow": self.term.bright_magenta,  # Magic rainbow
            }
            weather_color = weather_colors.get(self._current_weather_type)
            for px, py, char in self._weather_particles:
                if int(py) == y and 0 <= int(px) < inner_width:
                    # Don't overwrite duck or effect characters
                    existing_char, existing_color = row[int(px)]
                    if existing_char in GROUND_CHARS or existing_char == ' ':
                        # Only use first character if multi-char to prevent overflow
                        display_char = char[0] if len(char) > 1 else char
                        row[int(px)] = (display_char, weather_color)

            # Convert row to string, applying colors
            row_chars = []
            for char, color_func in row:
                if color_func:
                    # Apply color and reset after each colored character
                    row_chars.append(color_func(char) + self.term.normal)
                else:
                    row_chars.append(char)
            row_str = "".join(row_chars)
            
            # Pad to inner_width (but length() counts ANSI codes, so we track visible chars)
            visible_len = len(row)  # We know we have exactly inner_width visible chars
            lines.append(BOX["v"] + row_str + self.term.normal + BOX["v"])

        # Persistent chat log at bottom of playfield (WoW-style, newest at bottom)
        # Show scroll indicator if scrolled
        if self._chat_scroll_offset > 0:
            scroll_indicator = f" [PgUp/Dn] {self._chat_scroll_offset}+ more "
            header_pad = inner_width - len(scroll_indicator)
            lines.append(BOX["t_right"] + BOX["h"] * (header_pad // 2) + scroll_indicator + BOX["h"] * (header_pad - header_pad // 2) + BOX["t_left"])
        else:
            lines.append(BOX["t_right"] + BOX["h"] * inner_width + BOX["t_left"])
        
        # Build wrapped chat lines for display
        # Each message can wrap to multiple lines
        import textwrap
        wrap_width = inner_width - 9  # 9 = "[HH:MM] " + margin
        
        all_chat_lines = []  # List of (line_text, category, is_continuation)
        for timestamp, msg, category in self._chat_log:
            # Wrap long messages
            wrapped = textwrap.wrap(msg, width=wrap_width) if msg else ['']
            for j, line in enumerate(wrapped):
                prefix = f"[{timestamp}] " if j == 0 else "        "  # 8 spaces for continuation
                all_chat_lines.append((prefix + line, category, j > 0))
        
        # Calculate which lines to show based on scroll offset
        total_lines = len(all_chat_lines)
        if total_lines <= self._chat_log_visible_lines:
            # Not enough to scroll
            visible_start = 0
            visible_end = total_lines
        else:
            # Show lines based on scroll offset (0 = newest at bottom)
            visible_end = total_lines - self._chat_scroll_offset
            visible_start = max(0, visible_end - self._chat_log_visible_lines)
            visible_end = min(total_lines, visible_start + self._chat_log_visible_lines)
        
        visible_lines = all_chat_lines[visible_start:visible_end]
        
        # Pad with empty lines if not enough messages
        while len(visible_lines) < self._chat_log_visible_lines:
            visible_lines.insert(0, None)
        
        # Render each line with fading effect (oldest = dimmest)
        for i, entry in enumerate(visible_lines):
            if entry is None:
                # Empty line
                lines.append(BOX["v"] + " " * inner_width + BOX["v"])
            else:
                line_text, category, is_continuation = entry
                
                # Calculate fade level (0 = oldest/dimmest, visible_lines-1 = newest/brightest)
                fade_level = i / max(1, self._chat_log_visible_lines - 1)
                
                # Color based on category and fade
                if fade_level < 0.3:
                    # Very dim for oldest
                    color = self.term.dim
                elif fade_level < 0.6:
                    # Medium brightness
                    color = self.term.normal
                else:
                    # Full brightness for newest
                    if category == "duck":
                        color = self.term.bright_yellow
                    elif category == "event":
                        color = self.term.bright_cyan
                    elif category == "action":
                        color = self.term.bright_green
                    elif category == "discovery":
                        color = self.term.bright_magenta
                    else:
                        color = self.term.bright_white
                
                # Format line (already has timestamp prefix from wrapping)
                msg_truncated = _visible_truncate(line_text, inner_width - 1)
                
                line_content = color + msg_truncated + self.term.normal
                # Pad to width
                line_padded = _visible_ljust(line_content, inner_width)
                lines.append(BOX["v"] + line_padded + BOX["v"])
        
        # Bottom of playfield
        lines.append(BOX["bl"] + BOX["h"] * inner_width + BOX["br"])
        
        # Mark message as rendered so overlay doesn't show
        self._message_rendered_inline = True

        return lines

    def _render_side_panel(self, duck: "Duck", game: "Game", width: int) -> List[str]:
        """Render the side panel with close-up, stats, shortcuts, and info."""
        inner_width = width - 2
        lines = []

        # Panel header
        lines.append(BOX["tl"] + BOX["h"] * inner_width + BOX["tr"])

        # Close-up face section (compact)
        mood = duck.get_mood()
        
        # Determine which action to show for closeup
        # Priority: 1) Temporary closeup action, 2) Duck's current action, 3) Mood-based
        if self._show_closeup and self._closeup_action:
            closeup_action = self._closeup_action
        elif duck.current_action:
            closeup_action = duck.current_action
        else:
            closeup_action = None
        
        closeup = get_emotion_closeup(mood.state, closeup_action)

        if closeup:
            # Show compact close-up with yellow duck color
            for closeup_line in closeup:
                # Center the line properly
                centered = _visible_center(closeup_line, inner_width)
                # Apply yellow color to the duck ASCII
                yellow_line = self.term.yellow + centered + self.term.normal
                lines.append(BOX["v"] + yellow_line + BOX["v"])
        else:
            # Show mood status (compact)
            mood_text = _visible_center(mood.description, inner_width)
            lines.append(BOX["v"] + mood_text + BOX["v"])

        # Divider
        lines.append(BOX["t_right"] + BOX["h"] * inner_width + BOX["t_left"])

        # Needs bars (fill the width properly)
        needs_data = [
            ("HUN", duck.needs.hunger),
            ("ENG", duck.needs.energy),
            ("FUN", duck.needs.fun),
            ("CLN", duck.needs.cleanliness),
            ("SOC", duck.needs.social),
        ]

        for name, value in needs_data:
            # Calculate bar width to fill the space
            # Format: "HUN[████████] 83%"
            # Name=3, []=2 (in bar), space=1, pct=4-5 chars
            pct_str = f"{int(value):>3}%"
            bar_width = inner_width - len(name) - len(pct_str) - 3  # -3 for [] and space
            if bar_width < 5:
                bar_width = 5
            bar = self._make_progress_bar(value, bar_width)
            line_content = f"{name}{bar} {pct_str}"
            # Pad to exact width
            line_content = _visible_ljust(line_content, inner_width)
            lines.append(BOX["v"] + line_content + BOX["v"])

        # Divider - Master Menu Section
        lines.append(BOX["t_right"] + BOX["h"] * inner_width + BOX["t_left"])
        
        # Render master menu if available
        if hasattr(game, 'master_menu') and game.master_menu:
            # Calculate available lines for menu (target ~12 lines for menu content)
            menu_max_lines = 14
            menu_lines = game.master_menu.get_render_lines(inner_width, menu_max_lines)
            for menu_line in menu_lines:
                lines.append(BOX["v"] + menu_line + BOX["v"])
        else:
            # Fallback if master menu not initialized
            fallback_title = _visible_center("--- MENU ---", inner_width)
            lines.append(BOX["v"] + fallback_title + BOX["v"])
            fallback_msg = _visible_center("Loading...", inner_width)
            lines.append(BOX["v"] + fallback_msg + BOX["v"])

        # Divider
        lines.append(BOX["t_right"] + BOX["h"] * inner_width + BOX["t_left"])

        # Top padding for vertical centering (aligns with 5-line chat)
        lines.append(BOX["v"] + " " * inner_width + BOX["v"])

        # Activity/Status
        activity = self._get_activity_text(duck)
        activity_centered = _visible_center(activity, inner_width)
        lines.append(BOX["v"] + activity_centered + BOX["v"])

        # Current action message (truncate if needed)
        action_msg = duck.get_action_message() or "Just vibing..."
        action_msg = _visible_truncate(action_msg, inner_width - 2)
        action_centered = _visible_center(action_msg, inner_width)
        lines.append(BOX["v"] + action_centered + BOX["v"])
        
        # Current location (from exploration system) - always show line for consistent height
        if hasattr(game, 'exploration') and game.exploration and game.exploration.current_area:
            area_name = game.exploration.current_area.name
            location = f"@ {area_name}"  # Use @ instead of emoji for consistent width
        else:
            location = "@ Home Pond"  # Default location
        location = _visible_truncate(location, inner_width)
        location_centered = _visible_center(location, inner_width)
        lines.append(BOX["v"] + location_centered + BOX["v"])

        # Bottom padding for vertical centering
        lines.append(BOX["v"] + " " * inner_width + BOX["v"])

        # Bottom
        lines.append(BOX["bl"] + BOX["h"] * inner_width + BOX["br"])

        return lines

    def _get_need_indicator(self, value: float) -> str:
        """Get a text indicator for need level."""
        if value >= 80:
            return "OK!"
        elif value >= 50:
            return "..."
        elif value >= 30:
            return "low"
        else:
            return "!!!"

    def _get_activity_text(self, duck: "Duck") -> str:
        """Get text describing current activity."""
        import time as _time
        
        # Auto-clear expired current_action to prevent stale status display
        if hasattr(duck, 'current_action') and duck.current_action:
            if hasattr(duck, '_action_end_time') and _time.time() > duck._action_end_time:
                duck.current_action = None
        
        # Check for special activities first (based on duck.current_action if available)
        if hasattr(duck, 'current_action') and duck.current_action:
            action = duck.current_action
            if action == "traveling":
                return "Traveling..."
            elif action == "exploring":
                return "Exploring!"
            elif action == "building":
                return "Building..."
            elif action == "nap_in_nest":
                return "Napping in nest"
            elif action == "hide_in_shelter":
                return "Taking shelter"
            elif action == "use_bird_bath":
                return "Bathing"
        
        state = self.duck_pos.get_state()
        if state == "sleeping":
            return "Sleeping Zzz"
        elif state == "eating":
            return "Eating nom"
        elif state == "playing":
            return "Playing!"
        elif state == "walking":
            return "Wandering"
        elif state == "hiding":
            return "Hiding"
        else:
            return "Chilling"

    def _render_status(self, duck: "Duck", width: int) -> List[str]:
        """Render the needs status bars with fancy graphics."""
        inner_width = width - 2

        lines = [
            BOX["t_right"] + BOX["h"] * inner_width + BOX["t_left"],
        ]

        # Need display with progress bars
        needs_data = [
            ("Hunger", duck.needs.hunger, "H"),
            ("Energy", duck.needs.energy, "E"),
            ("Fun", duck.needs.fun, "F"),
            ("Clean", duck.needs.cleanliness, "C"),
            ("Social", duck.needs.social, "S"),
        ]

        # Two rows of needs
        row1 = needs_data[:3]
        row2 = needs_data[3:]

        for row in [row1, row2]:
            row_content = ""
            for name, value, key in row:
                bar = self._make_progress_bar(value, 10)
                row_content += f" [{key}]{name}: {bar} {value:5.1f} "

            row_content = row_content.center(inner_width)
            lines.append(BOX["v"] + row_content[:inner_width] + BOX["v"])

        return lines

    def _make_progress_bar(self, value: float, width: int, use_color: bool = True) -> str:
        """Create a fancy progress bar with optional color."""
        filled = int((value / 100) * width)

        # Color coding based on value
        if value >= 70:
            char = BAR_STYLES["full"]
            color = self.term.green if use_color else None
        elif value >= 40:
            char = BAR_STYLES["high"]
            color = self.term.yellow if use_color else None
        elif value >= 20:
            char = BAR_STYLES["med"]
            color = self.term.bright_red if use_color else None
        else:
            char = BAR_STYLES["low"]
            color = self.term.red if use_color else None

        bar_content = char * filled + BAR_STYLES["empty"] * (width - filled)
        if color and use_color:
            return f"[{color(bar_content)}]"
        return f"[{bar_content}]"

    def _render_messages(self, width: int) -> List[str]:
        """Render the message area (shows hints when no overlay message active)."""
        inner_width = width - 2

        lines = [
            BOX["tl"] + BOX["h"] * inner_width + BOX["tr"],
        ]

        # Show duck's current action/thought (not overlay messages)
        if hasattr(self, '_duck_thought') and self._duck_thought:
            thought_line = f" {self._duck_thought} ".center(inner_width)
            lines.append(BOX["v"] + thought_line[:inner_width] + BOX["v"])
            lines.append(BOX["v"] + " " * inner_width + BOX["v"])
        else:
            # Default hint text
            hint = " [TAB] Menu | [H] Help | [Q] Quit "
            lines.append(BOX["v"] + hint.center(inner_width)[:inner_width] + BOX["v"])
            lines.append(BOX["v"] + " " * inner_width + BOX["v"])

        lines.append(BOX["bl"] + BOX["h"] * inner_width + BOX["br"])

        return lines

    def _render_progress_bars(self, width: int, game) -> List[str]:
        """Render a single-line progress status bar above controls."""
        # Simple non-colored progress bar
        def make_bar(pct: float, bar_width: int) -> str:
            filled = int((pct / 100) * bar_width)
            return "=" * filled + "-" * (bar_width - filled)

        # Get data
        progression = game.progression
        xp_in_level, xp_needed, xp_pct = progression.get_xp_progress()
        level = progression.level

        duck = game.duck
        stage_name = duck.get_growth_stage_display()
        growth_pct = duck.growth_progress * 100
        
        # Get goal progress
        goals_completed = game.goals.get_completed_count()
        goals_total = max(game.goals.get_total_count(), 1)  # Avoid div by zero
        goals_pct = (goals_completed / goals_total) * 100 if goals_total > 0 else 0

        # Build compact format: "Lv.5 [====----] 50% | Juvenile [====----] 25% | Goals 3/10"
        bar_width = 10
        left_bar = make_bar(xp_pct, bar_width)

        if duck.growth_stage in ("elder", "legendary"):
            age_days = duck.age_days
            years = age_days // 365
            days = age_days % 365
            age_str = f"{years}y {days}d" if years > 0 else f"{days}d"
            age_part = f"{stage_name} {age_str}"
        else:
            right_bar = make_bar(growth_pct, bar_width)
            age_part = f"{stage_name} [{right_bar}] {int(growth_pct)}%"
        
        # Goal part
        goal_part = f"Goals {goals_completed}/{goals_total}"

        content = f" Lv.{level} [{left_bar}] {int(xp_pct)}% | {age_part} | {goal_part} "

        # Calculate inner width (excluding borders)
        inner_width = width - 2
        
        # Pad or truncate content to fit
        if len(content) < inner_width:
            content = content + " " * (inner_width - len(content))
        else:
            content = content[:inner_width]

        # Return with full box borders (top, content with sides, bottom)
        return [
            BOX["tl"] + BOX["h"] * inner_width + BOX["tr"],
            BOX["v"] + content + BOX["v"],
            BOX["bl"] + BOX["h"] * inner_width + BOX["br"],
        ]

    def _render_controls_bar(self, width: int) -> List[str]:
        """Render the bottom controls bar."""
        inner_width = max(width - 2, 20)  # Ensure minimum width

        # Compact controls hint - updated for master menu navigation
        controls = "[Arrows] Nav | [Enter] Select | [Bksp] Back | [M]usic [N]oise | [H]elp [Q]uit"

        # Pad or truncate to exact width
        if len(controls) < inner_width:
            content = controls.center(inner_width)
        else:
            content = controls[:inner_width]

        lines = [
            BOX["tl"] + BOX["h"] * inner_width + BOX["tr"],
            BOX["v"] + content + BOX["v"],
            BOX["bl"] + BOX["h"] * inner_width + BOX["br"],
        ]
        return lines

    def _render_minigame_frame(self, game: "Game"):
        """Render a minigame frame."""
        width = max(self.term.width, 60)
        height = max(self.term.height, 20)

        output = []

        # Get minigame render lines
        minigame_lines = game._render_minigame()

        # Calculate centering
        game_height = len(minigame_lines)
        top_padding = max(0, (height - game_height - 2) // 2)

        # Add top padding
        for _ in range(top_padding):
            output.append("")

        # Add minigame title bar
        game_names = {
            "bread_catch": "BREAD CATCH",
            "bug_chase": "BUG CHASE",
            "memory_match": "MEMORY MATCH",
            "duck_race": "DUCK RACE",
        }
        game_name = game_names.get(game._minigame_type, "MINI-GAME")
        title = f"=== {game_name} ==="
        output.append(title.center(width))
        output.append("")

        # Add minigame content, centered
        for line in minigame_lines:
            centered_line = line.center(width)
            output.append(centered_line)

        # Add bottom padding/instructions
        output.append("")
        output.append("[Q] Quit Game".center(width))

        # Print everything
        print(self.term.home + self.term.clear, end="")
        for line in output:
            print(line)

    def _render_title_screen(self, menu_index: int = 0, has_save: bool = False, 
                                update_status: str = "", version: str = "1.0.0"):
        """Render the title/new game screen with dancing duck animation and menu.
        
        Args:
            menu_index: Currently selected menu option (0-3)
            has_save: Whether a save file exists (enables Continue option)
            update_status: Status message for updates (e.g., "Update available!")
            version: Current game version to display
        """
        self._title_frame = (self._title_frame + 1) % 120

        # Dancing duck animation frames - Teen duck style
        duck_frames = [
            # Frame 1 - Idle happy
            [
                "              ,~~.                     ",
                "         ,   (  ^ )>        *          ",
                "         )`~~'    (                    ",
                "        (    .__)  )                   ",
                "         `-.____.,'                    ",
                "             ||          #             ",
                "           ~~~~~                       ",
            ],
            # Frame 2 - Dance left
            [
                "           ,~~.                        ",
                "      ,   (  o )>    #                 ",
                "      )`~~'    (                       ",
                "     (    .~.)  )                      ",
                "      `-.____.,'                       ",
                "        //  ||                         ",
                "       ~~~~~~~                         ",
            ],
            # Frame 3 - Dance right
            [
                "                ,~~.                   ",
                "           ,   (  o )>                 ",
                "           )`~~'    (      #           ",
                "          (    (._)  )                 ",
                "           `-.____.,'                  ",
                "               ||  \\\\                  ",
                "              ~~~~~~~                  ",
            ],
            # Frame 4 - QUACK pose!
            [
                "     \\\\    ,~~.    //                 ",
                "      \\\\  ( O O )> //    QUACK!       ",
                "       )`~~'    (                      ",
                "      (    .◡.)  )        # #         ",
                "       `-.____.,'                      ",
                "          \\    /                       ",
                "         ~~~~~~~                       ",
            ],
            # Frame 5 - Lean left
            [
                "         ,~~.      #                   ",
                "    ,   (  ~ )>                        ",
                "    )`~~'    (                         ",
                "   (    .__)  )                        ",
                "    `-.____.,'                         ",
                "       //   |                          ",
                "     ~~~~~~~                           ",
            ],
            # Frame 6 - Lean right
            [
                "                  ,~~.                 ",
                "             ,   (  ~ )>      #        ",
                "             )`~~'    (                ",
                "            (    .__)  )               ",
                "             `-.____.,'                ",
                "                 |   \\\\                ",
                "               ~~~~~~~                 ",
            ],
            # Frame 7 - Spin!
            [
                "           * SPIN *                    ",
                "              ,~~.                     ",
                "         ,   ( @ @ )>                  ",
                "         )`~~'    (       #            ",
                "        (    .~~)  )                   ",
                "         `-.____.,'                    ",
                "            ~~~~~~~                    ",
            ],
            # Frame 8 - Point!
            [
                "              ,~~.                     ",
                "         ,   (  ^ )>======>>           ",
                "         )`~~'    (                    ",
                "        (    .ᴗ.)  )       #           ",
                "         `-.____.,'                    ",
                "             ||                        ",
                "           ~~~~~                       ",
            ],
            # Frame 9 - Happy blink
            [
                "              ,~~.                     ",
                "         ,   ( -.- )>      *  .  *     ",
                "         )`~~'    (                    ",
                "        (    .__)  )                   ",
                "         `-.____.,'                    ",
                "             ||                        ",
                "           ~~~~~                       ",
            ],
            # Frame 10 - Look at you!
            [
                "              ,~~.                     ",
                "         ,   ( o_o )>    Hi there!     ",
                "         )`~~'    (                    ",
                "        (    .__)  )      *            ",
                "         `-.____.,'                    ",
                "             ||                        ",
                "           ~~~~~                       ",
            ],
        ]

        # Slow down animation - change frame every 12 ticks instead of 10
        frame_idx = (self._title_frame // 12) % len(duck_frames)
        duck_art = duck_frames[frame_idx]

        # Sparkle effects that rotate slowly (change every 15 ticks)
        sparkle_chars = ["*", "*", "*", "*"]
        sparkle_idx = (self._title_frame // 15) % len(sparkle_chars)
        sparkle1 = sparkle_chars[sparkle_idx]
        sparkle2 = sparkle_chars[(sparkle_idx + 2) % len(sparkle_chars)]

        # Build title screen
        title_art = [
            f"    {sparkle1}                                                    {sparkle2}",
            "    +======================================================+    ",
            "    |                                                      |    ",
            "    |      ██████+██+  ██+███████+███████+███████+███████+ |    ",
            "    |     ██+====+██|  ██|██+====+██+====+██+====+██+====+ |    ",
            "    |     ██|     ███████|█████+  █████+  ███████+█████+   |    ",
            "    |     ██|     ██+==██|██+==+  ██+==+  +====██|██+==+   |    ",
            "    |     +██████+██|  ██|███████+███████+███████|███████+ |    ",
            "    |      +=====++=+  +=++======++======++======++======+ |    ",
            "    |                                                      |    ",
            "    |            === THE DUCK ===                          |    ",
            "    |                                                      |    ",
            "    +======================================================+    ",
        ]

        # Add the dancing duck with yellow color
        for line in duck_art:
            padded_line = line + " " * (54 - len(line)) if len(line) < 54 else line[:54]
            yellow_duck = self.term.yellow + padded_line + self.term.normal
            title_art.append(f"    |{yellow_duck}|    ")

        # Build menu options
        menu_options = []
        if has_save:
            menu_options.append(("Continue", 0))
        menu_options.append(("New Game", 1 if has_save else 0))
        menu_options.append(("Check for Updates", 2 if has_save else 1))
        menu_options.append(("Quit", 3 if has_save else 2))
        
        # Build menu lines with selection indicator
        def format_menu_item(text: str, idx: int, selected: bool) -> str:
            if selected:
                return self.term.bold + self.term.cyan + f"  > {text} <  " + self.term.normal
            else:
                return f"    {text}    "
        
        # Calculate menu display with proper spacing
        menu_lines = []
        for label, idx in menu_options:
            is_selected = (idx == menu_index) if has_save else (idx == menu_index)
            # Adjust index check based on whether save exists
            actual_idx = menu_options.index((label, idx))
            is_selected = (actual_idx == menu_index)
            formatted = format_menu_item(label, idx, is_selected)
            # Pad to fit the box width (54 chars inside)
            visible_len = len(label) + (10 if is_selected else 8)
            padding = (54 - visible_len) // 2
            line_content = " " * padding + formatted + " " * padding
            # Trim or pad to exactly 54 chars
            if _visible_len(line_content) < 54:
                line_content = line_content + " " * (54 - _visible_len(line_content))
            elif _visible_len(line_content) > 54:
                line_content = _visible_slice(line_content, 0, 54)
            menu_lines.append(f"    |{line_content}|    ")

        # Add footer with menu
        title_art.extend([
            "    +======================================================+    ",
            "    |                                                      |    ",
            "    |         Your virtual pet duck awaits!                |    ",
            "    |                                                      |    ",
            "    +------------------------------------------------------+    ",
        ])
        
        # Add menu items
        title_art.extend(menu_lines)
        
        # Add navigation hint and update status
        title_art.extend([
            "    +------------------------------------------------------+    ",
            "    |         Use UP/DOWN to select, ENTER to confirm      |    ",
        ])
        
        # Add update status if available
        if update_status:
            # Color the update status based on content
            if "available" in update_status.lower():
                status_colored = self.term.green + update_status + self.term.normal
            elif "failed" in update_status.lower() or "error" in update_status.lower():
                status_colored = self.term.red + update_status + self.term.normal
            else:
                status_colored = update_status
            status_line = _visible_center(status_colored, 54)
            title_art.append(f"    |{status_line}|    ")
        
        # Add version footer
        version_str = f"v{version}"
        version_line = _visible_center(version_str, 54)
        title_art.extend([
            f"    |{version_line}|    ",
            "    +======================================================+    ",
            "",
        ])

        # Use home only (no clear) to prevent flicker - overwrite in place
        print(self.term.home)
        for line in title_art:
            # Clear to end of line to handle any leftover characters
            print(self.term.center(line) + self.term.clear_eol)

    def _overlay_help(self, base_output: List[str], width: int) -> List[str]:
        """Overlay the help screen."""
        help_text = [
            "=== DUCK CARE ===",
            "[F]/[1] Feed    [P]/[2] Play    [L]/[3] Clean",
            "[D]/[4] Pet     [Z]/[5] Sleep   [T] Talk",
            "",
            "=== MENUS ===",
            "[I] Inventory   [G] Goals    [S] Stats",
            "[B] Shop        [U] Use Item [O] Quests",
            "",
            "=== ACTIVITIES ===",
            "[E] Explore     [A] Areas    [C] Craft",
            "[R] Build       [J] Minigames",
            "[K] Duck Fact   [W] Weather Activities",
            "",
            "=== SPECIAL ===",
            "[V] Trading     [Y] Scrapbook",
            "[6] Treasure    [7] Secrets",
            "",
            "=== AUDIO ===",
            "[M] Sound  [N] Music  [+]/[-] Volume",
            "",
            "=== SYSTEM ===",
            "[Q] Save & Quit  [X] Reset Game",
            "",
            "Press [H] to close",
        ]

        return self._overlay_box(base_output, help_text, "HELP", width)

    def _overlay_stats(self, base_output: List[str], duck: "Duck", game: "Game", width: int) -> List[str]:
        """Overlay statistics screen with pagination."""
        stats = game._statistics
        memory = duck.memory
        prog = game.progression

        # XP progress bar
        xp_in_level, xp_needed, xp_pct = prog.get_xp_progress()
        xp_bar_width = 15
        xp_filled = int((xp_pct / 100) * xp_bar_width)
        xp_bar = "[" + "#" * xp_filled + "-" * (xp_bar_width - xp_filled) + "]"

        # Collectibles progress
        coll_owned, coll_total = prog.get_total_collection_progress()

        # Streak multiplier display
        streak_mult = prog.get_streak_multiplier_display()
        streak_line = f"Streak: {prog.current_streak} days"
        if streak_mult:
            streak_line += f" {streak_mult}"

        # Fun stats calculations
        total_stats = prog.stats
        total_care_actions = (
            total_stats.get("total_feeds", 0) +
            total_stats.get("total_plays", 0) +
            total_stats.get("total_cleans", 0) +
            total_stats.get("total_pets", 0)
        )

        # Calculate "love score" - a fun aggregate metric
        relationship_pct = memory.total_interactions // 10  # Approximate relationship level
        love_score = min(100, (
            (prog.current_streak * 2) +
            (relationship_pct) +
            (prog.level * 3) +
            min(30, coll_owned * 2)
        ))

        # Exploration stats
        exploration = game.exploration
        area_count = len(exploration.discovered_areas)
        current_biome = exploration._current_biome
        biome_name = current_biome.value.replace("_", " ").title() if current_biome else "Unknown"

        # Materials count
        materials = game.materials
        mat_count = len(materials.get_all_materials())
        mat_total = sum(materials.get_all_materials().values())

        # Building count
        building = game.building
        struct_count = len([s for s in building._structures if s.status.value == "complete"])

        # All stats content
        all_stats = [
            f"[d] {duck.name} - {duck.get_growth_stage_display()}",
            "",
            f"+============== PROGRESS ==============+",
            f"  Level {prog.level}: {prog.title}",
            f"  XP: {xp_bar} {int(xp_pct)}%",
            f"  Total XP: {prog.xp}",
            f"  {streak_line}",
            f"  Best Streak: {prog.longest_streak} days",
            f"+======================================+",
            "",
            f"+============== BONDING ===============+",
            f"  Relationship: {memory.get_relationship_description()}",
            f"  Total Interactions: {memory.total_interactions}",
            f"  Mood Trend: {memory.get_recent_mood_trend()}",
            f"  Love Score: {'<3' * (love_score // 20)} {love_score}%",
            f"+======================================+",
            "",
            f"+============== WORLD =================+",
            f"  Location: {biome_name}",
            f"  Areas Discovered: {area_count}",
            f"  Materials: {mat_count} types ({mat_total} total)",
            f"  Structures Built: {struct_count}",
            f"+======================================+",
            "",
            f"+============== LIFETIME ==============+",
            f"  Days Played: {prog.days_played}",
            f"  Total Care Actions: {total_care_actions}",
            f"  - Feeds: {total_stats.get('total_feeds', 0)}",
            f"  - Plays: {total_stats.get('total_plays', 0)}",
            f"  - Cleans: {total_stats.get('total_cleans', 0)}",
            f"  - Pets: {total_stats.get('total_pets', 0)}",
            f"  Collectibles: {coll_owned}/{coll_total}",
            f"+======================================+",
        ]
        
        # Pagination logic
        total_lines = len(all_stats)
        max_scroll = max(0, total_lines - self._stats_page_size)
        self._stats_scroll_offset = max(0, min(self._stats_scroll_offset, max_scroll))
        
        # Get visible portion
        start_idx = self._stats_scroll_offset
        end_idx = start_idx + self._stats_page_size
        visible_stats = all_stats[start_idx:end_idx]
        
        # Add navigation hint
        nav_hints = []
        if self._stats_scroll_offset > 0:
            nav_hints.append("[^] Up")
        if self._stats_scroll_offset < max_scroll:
            nav_hints.append("[v] Down")
        nav_hints.append("[ESC] Close")
        
        visible_stats.append("")
        visible_stats.append("  " + " | ".join(nav_hints))

        return self._overlay_box(base_output, visible_stats, "[=] STATISTICS", width)

    def _overlay_talk(self, base_output: List[str], width: int) -> List[str]:
        """Overlay talk/chat interface."""
        talk_text = [
            "Talk to your duck!",
            "",
            f"> {self._talk_buffer}_",
            "",
            "Type a message and press ENTER",
            "Press ESC to cancel",
        ]

        return self._overlay_box(base_output, talk_text, "TALK", width)

    def _overlay_fishing(self, base_output: List[str], game: "Game", width: int) -> List[str]:
        """Overlay fishing minigame status."""
        fishing = game.fishing
        
        # ASCII fishing animation
        fishing_art = [
            "         \\  |  /",
            "          \\ | /",
            "     ~~~~~~\\|/~~~~~~",
            "    ~~~~~~~~~~~~~~~~~",
            "   ~~~~~~~~~~~~~~~~~~~",
        ]
        
        fish_text = []
        fish_text.append("-o FISHING -o")
        fish_text.append("")
        
        # Add fishing art
        for line in fishing_art:
            fish_text.append(line)
        
        fish_text.append("")
        
        # Status based on fishing state
        if fishing.hooked_fish:
            fish_text.append("  !! FISH ON THE LINE !!")
            fish_text.append("")
            fish_text.append("  Press [SPACE] to REEL IN!")
        else:
            fish_text.append("  Waiting for a bite...")
            fish_text.append("")
            fish_text.append("  [SPACE] Reel in when hooked")
        
        fish_text.append("")
        fish_text.append("-" * 28)
        fish_text.append(f"  Spot: {fishing.current_spot.value if fishing.current_spot else 'Unknown'}")
        fish_text.append(f"  Fish Caught: {fishing.total_catches}")
        fish_text.append("")
        fish_text.append("  [Q] or [ESC] to stop fishing")
        
        return self._overlay_box(base_output, fish_text, "FISHING", width)

    def _overlay_message(self, base_output: List[str], width: int) -> List[str]:
        """Overlay message box."""
        # Check if message expired
        if time.time() > self._message_expire:
            self._show_message_overlay = False
            self._message_queue.clear()
            return base_output

        if not self._message_queue:
            return base_output

        # Build message content
        msg_text = []
        for line in self._message_queue:
            msg_text.append(line)

        return self._overlay_box(base_output, msg_text, "MESSAGE", width)

    def _overlay_inventory(self, base_output: List[str], game: "Game", width: int) -> List[str]:
        """Overlay inventory screen with pagination."""
        inv = game.inventory

        # Group items by count and create numbered list
        item_counts: Dict[str, int] = {}
        unique_items: List[str] = []
        for item_id in inv.items:
            if item_id not in item_counts:
                unique_items.append(item_id)
            item_counts[item_id] = item_counts.get(item_id, 0) + 1

        # Pagination settings
        items_per_page = 9  # Matches [1-9] keys
        total_items = len(unique_items)
        total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)
        
        # Get current page from state (add if not exists)
        if not hasattr(self, '_inventory_page'):
            self._inventory_page = 0
        current_page = self._inventory_page
        start_idx = current_page * items_per_page
        end_idx = min(start_idx + items_per_page, total_items)

        inv_text = [
            f"Items: {len(inv.items)}/{inv.max_size}",
        ]
        
        if total_pages > 1:
            inv_text.append(f"Page {current_page + 1}/{total_pages} (</> to change)")
        inv_text.append("-" * 30)

        from world.items import get_item_info
        display_num = 1
        for idx in range(start_idx, end_idx):
            item_id = unique_items[idx]
            item = get_item_info(item_id)
            if item:
                count_str = f"x{item_counts[item_id]}" if item_counts[item_id] > 1 else ""
                line = f"[{display_num}] {item.icon} {item.name} {count_str}"
                inv_text.append(line)
                display_num += 1

        if not item_counts:
            inv_text.append("(Empty)")
            inv_text.append("")
            inv_text.append("Find items by exploring!")

        inv_text.extend([
            "",
            "[1-9] Use item | [</>] Page | [I] Close",
        ])

        # Store unique items list for key handling (current page only) and total count for pagination
        self._inventory_items = unique_items[start_idx:end_idx]
        self._inventory_total_items = len(unique_items)

        return self._overlay_box(base_output, inv_text, "INVENTORY", width)

    def inventory_change_page(self, delta: int):
        """Change inventory page."""
        if not hasattr(self, '_inventory_page'):
            self._inventory_page = 0
        
        # Calculate total pages based on total unique items
        items_per_page = 9
        total_items = getattr(self, '_inventory_total_items', 0)
        total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)
        
        self._inventory_page = max(0, min(total_pages - 1, self._inventory_page + delta))

    def _overlay_box(self, base_output: List[str], content: List[str], title: str, width: int) -> List[str]:
        """Generic overlay box with height limiting."""
        box_width = min(50, width - 4)
        
        # Limit height to fit on screen (leave room for top/bottom margins)
        max_content_height = len(base_output) - 6  # Leave small margins, allow more content
        if max_content_height < 15:
            max_content_height = 15
        
        # Truncate content if too tall
        if len(content) > max_content_height:
            visible_content = content[:max_content_height - 1]
            visible_content.append(f"... ({len(content) - max_content_height + 1} more lines)")
        else:
            visible_content = content
        
        box_height = len(visible_content) + 4

        # Create box - the interior is box_width wide
        # Total line width = tl(1) + interior(box_width) + tr(1) = box_width + 2
        title_visible_len = _visible_len(title)
        title_with_spaces = f" {title} "
        title_total_len = title_visible_len + 2  # Including spaces
        
        # Top line: tl + h + " title " + remaining h's + tr
        # Interior width for h's = box_width - len(" title ")
        remaining_h = box_width - title_total_len - 1  # -1 for the initial h before title
        if remaining_h < 0:
            remaining_h = 0
        
        box_lines = [
            BOX_DOUBLE["tl"] + BOX_DOUBLE["h"] + title_with_spaces + BOX_DOUBLE["h"] * remaining_h + BOX_DOUBLE["tr"],
        ]

        for line in visible_content:
            # Ensure content fills exactly box_width chars with spaces (solid background)
            # First truncate if too long, then pad with spaces to fill
            content_area = _visible_truncate(f" {line}", box_width)
            content_area = _visible_ljust(content_area, box_width)
            box_lines.append(BOX_DOUBLE["v"] + content_area + BOX_DOUBLE["v"])

        box_lines.append(BOX_DOUBLE["bl"] + BOX_DOUBLE["h"] * box_width + BOX_DOUBLE["br"])

        # Overlay on base output
        result = base_output.copy()
        start_row = 4
        start_col = (width - box_width - 2) // 2
        
        # Get blessed terminal for color reset
        from blessed import Terminal
        _term = Terminal()

        for i, line in enumerate(box_lines):
            if start_row + i < len(result):
                row = result[start_row + i]
                # Use ANSI-aware slicing for rows that may contain colored text
                box_visible_width = _visible_len(line)
                left_part = _visible_slice(row, 0, start_col)
                left_part = _visible_ljust(left_part, start_col)  # Ensure proper width
                right_part = _visible_slice(row, start_col + box_visible_width, width)
                # Add terminal reset after left_part to prevent color bleeding into overlay
                new_row = left_part + _term.normal + line + right_part
                result[start_row + i] = _visible_truncate(new_row, width)

        return result

    def _overlay_celebration(self, base_output: List[str], width: int) -> List[str]:
        """Overlay celebration screen with ASCII art."""
        from ui.ascii_art import get_celebration_art, get_celebration_frame_count

        # Update animation frame (every 0.2 seconds)
        current_time = time.time()
        if current_time - self._celebration_frame_time >= 0.2:
            self._celebration_frame += 1
            self._celebration_frame_time = current_time

        # Get the current frame of animation
        art = get_celebration_art(self._celebration_type, self._celebration_frame)
        if not art:
            art = get_celebration_art("level_up", self._celebration_frame)  # Default

        content = art.copy() if art else []
        if self._celebration_message:
            content.append("")
            # Use ANSI-aware centering for colored messages
            content.append(_visible_center(self._celebration_message, 30))
        content.append("")
        content.append(_visible_center("Press any key to continue...", 30))

        # Create a larger box for celebrations
        box_width = min(60, width - 4)
        box_height = len(content) + 2

        box_lines = []
        for line in content:
            # Center and ensure full width with spaces (solid background)
            centered = _visible_center(line, box_width)
            centered = _visible_ljust(_visible_truncate(centered, box_width), box_width)
            box_lines.append(centered)

        # Overlay on base output
        result = base_output.copy()
        start_row = max(2, (len(result) - box_height) // 2 - 2)
        start_col = (width - box_width) // 2
        
        # Get blessed terminal for color reset
        from blessed import Terminal
        _term = Terminal()

        for i, line in enumerate(box_lines):
            if start_row + i < len(result):
                row = result[start_row + i]
                # Use ANSI-aware slicing for rows that may contain colored text
                box_visible_width = _visible_len(line)
                left_part = _visible_slice(row, 0, start_col)
                left_part = _visible_ljust(left_part, start_col)
                right_part = _visible_slice(row, start_col + box_visible_width, width)
                # Add terminal reset after left_part to prevent color bleeding into overlay
                new_row = left_part + _term.normal + line + right_part
                result[start_row + i] = _visible_truncate(new_row, width)

        return result

    def show_celebration(self, celebration_type: str, message: str = "", duration: float = 4.0):
        """Show a celebration overlay."""
        self._show_celebration = True
        self._celebration_type = celebration_type
        self._celebration_message = message
        self._celebration_expire = time.time() + duration
        self._celebration_frame = 0
        self._celebration_frame_time = time.time()

    def _check_celebration_expired(self):
        """Check and clear expired celebration."""
        if self._show_celebration and time.time() > self._celebration_expire:
            self._show_celebration = False
            self._celebration_type = None
            self._celebration_message = ""

    def dismiss_celebration(self):
        """Dismiss celebration overlay early (on key press)."""
        self._show_celebration = False
        self._celebration_type = None
        self._celebration_message = ""

    def _overlay_item_interaction(self, base_output: List[str], game: "Game", width: int) -> List[str]:
        """Overlay item interaction animation."""
        # Get current animation frame from game
        frame = game.get_current_interaction_frame()
        if not frame:
            return base_output
        
        # Build content box
        content = []
        content.append("")  # Top padding
        content.append(_visible_center("~~ INTERACTING ~~", 40))
        content.append("")
        
        # Add animation frame
        for line in frame:
            content.append(_visible_center(line, 40))
        
        content.append("")
        
        # Add message if available
        if hasattr(game, '_item_interaction_message') and game._item_interaction_message:
            msg = game._item_interaction_message
            # Wrap long messages
            if len(msg) > 36:
                words = msg.split()
                line = ""
                for word in words:
                    if len(line) + len(word) + 1 <= 36:
                        line += (" " if line else "") + word
                    else:
                        content.append(_visible_center(line, 40))
                        line = word
                if line:
                    content.append(_visible_center(line, 40))
            else:
                content.append(_visible_center(msg, 40))
        
        content.append("")

        # Create box
        box_width = min(44, width - 4)
        box_height = len(content) + 2

        box_lines = []
        # Top border
        box_lines.append(self.term.cyan("+" + "=" * (box_width - 2) + "+"))
        
        for line in content:
            # Truncate and pad to box width
            centered = _visible_center(line, box_width - 4)
            centered = _visible_truncate(centered, box_width - 4)
            centered = _visible_ljust(centered, box_width - 4)
            box_lines.append(self.term.cyan("| ") + centered + self.term.cyan(" |"))
        
        # Bottom border
        box_lines.append(self.term.cyan("+" + "=" * (box_width - 2) + "+"))

        # Overlay on base output
        result = base_output.copy()
        start_row = max(2, (len(result) - box_height) // 2 - 2)
        start_col = (width - box_width) // 2
        
        # Get blessed terminal for color reset
        from blessed import Terminal
        _term = Terminal()

        for i, line in enumerate(box_lines):
            if start_row + i < len(result):
                row = result[start_row + i]
                # Use ANSI-aware slicing
                box_visible_width = _visible_len(line)
                left_part = _visible_slice(row, 0, start_col)
                left_part = _visible_ljust(left_part, start_col)
                right_part = _visible_slice(row, start_col + box_visible_width, width)
                # Add terminal reset after left_part to prevent color bleeding into overlay
                new_row = left_part + _term.normal + line + right_part
                result[start_row + i] = _visible_truncate(new_row, width)

        return result

    def _overlay_shop(self, base_output: List[str], habitat, width: int) -> List[str]:
        """Overlay shop interface with pagination."""
        from world.shop import get_items_by_category, ItemCategory
        from ui.habitat_art import render_item_preview
        
        # Get items in current category
        category = ItemCategory(self._shop_categories[self._shop_category_index].lower())
        items = get_items_by_category(category)
        
        # Calculate pagination
        total_items = len(items)
        items_per_page = self._shop_items_per_page
        current_page = self._shop_item_index // items_per_page if items_per_page > 0 else 0
        total_pages = max(1, (total_items + items_per_page - 1) // items_per_page) if items_per_page > 0 else 1
        start_idx = current_page * items_per_page
        end_idx = min(start_idx + items_per_page, total_items)
        
        # Build shop display
        content = []
        content.append(f"$ Currency: ${habitat.currency}")
        content.append("")
        content.append("Categories: " + " ".join(
            f"[{cat}]" if i == self._shop_category_index else cat 
            for i, cat in enumerate(self._shop_categories)
        ))
        
        # Show page info if paginated
        if total_pages > 1:
            content.append(f"Page {current_page + 1}/{total_pages}")
        else:
            content.append("")
        
        # Show items for current page
        for i in range(start_idx, end_idx):
            item = items[i]
            prefix = "-> " if i == self._shop_item_index else "   "
            
            # Show ownership and visibility status
            if habitat.owns_item(item.id):
                # Owned item - show placed/stored status
                if item.category == ItemCategory.COSMETIC:
                    # Cosmetics show equipped status
                    is_equipped = item.id in habitat.equipped_cosmetics.values()
                    status = "[WORN]  " if is_equipped else "[OWNED] "
                elif habitat.is_item_stored(item.id):
                    status = "[STORED]"
                else:
                    status = "[PLACED]"
                content.append(f"{prefix}{status} {item.name}")
            else:
                # Not owned - show price and affordability
                affordable = "$" if habitat.can_afford(item.cost) else "X"
                content.append(f"{prefix}[NEW]    {item.name} ${item.cost} {affordable} Lv{item.unlock_level}")
        
        # Show selected item description and actions
        if self._shop_item_index < len(items):
            item = items[self._shop_item_index]
            content.append("")
            content.append(item.description)
            
            # Show available action for this item
            if habitat.owns_item(item.id):
                if item.category == ItemCategory.COSMETIC:
                    is_equipped = item.id in habitat.equipped_cosmetics.values()
                    action_hint = "[E] Unequip" if is_equipped else "[E] Equip"
                elif habitat.is_item_stored(item.id):
                    action_hint = "[T] Show (free)"
                else:
                    action_hint = "[T] Hide (free)"
                content.append(action_hint)
        
        content.append("")
        content.append("<- -> : Category | ^ v : Select | [B]uy | [T]oggle | [ESC]")
        
        return self._overlay_box(base_output, content, "[SHOP]", width)

    def shop_navigate_category(self, delta: int):
        """Navigate shop categories."""
        self._shop_category_index = (self._shop_category_index + delta) % len(self._shop_categories)
        self._shop_item_index = 0

    def shop_navigate_item(self, delta: int):
        """Navigate shop items."""
        from world.shop import get_items_by_category, ItemCategory
        category = ItemCategory(self._shop_categories[self._shop_category_index].lower())
        items = get_items_by_category(category)
        if items:
            self._shop_item_index = (self._shop_item_index + delta) % len(items)

    def get_selected_shop_item(self):
        """Get currently selected shop item."""
        from world.shop import get_items_by_category, ItemCategory
        category = ItemCategory(self._shop_categories[self._shop_category_index].lower())
        items = get_items_by_category(category)
        if self._shop_item_index < len(items):
            return items[self._shop_item_index]
        return None

    def show_message(self, message: str, duration: float = 5.0, category: str = "system"):
        """Show a message to the player and add to chat log. 
        Categories: system, action, duck, event, discovery"""
        import textwrap
        from datetime import datetime
        
        # Add to persistent chat log with timestamp
        timestamp = datetime.now().strftime("%H:%M")
        # Split multi-line messages into separate log entries
        for line in message.split('\n'):
            if line.strip():
                self._chat_log.append((timestamp, line.strip(), category))
        
        # Trim chat log to max size
        if len(self._chat_log) > self._chat_log_max_size:
            self._chat_log = self._chat_log[-self._chat_log_max_size:]
        
        # Box width is min(50, width - 4), so content width is about 46 chars
        wrap_width = 44
        
        # Split message by newlines first, then wrap each line
        wrapped_lines = []
        for line in message.split('\n'):
            if line.strip():
                # Wrap long lines
                wrapped = textwrap.wrap(line, width=wrap_width)
                wrapped_lines.extend(wrapped if wrapped else [''])
            else:
                wrapped_lines.append('')
        
        self._message_queue = wrapped_lines
        self._show_message_overlay = True
        if duration > 0:
            self._message_expire = time.time() + duration
        else:
            self._message_expire = float('inf')  # Never expire automatically
    
    def add_chat_message(self, message: str, category: str = "system"):
        """Add a message to the chat log without showing overlay."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M")
        for line in message.split('\n'):
            if line.strip():
                self._chat_log.append((timestamp, line.strip(), category))
        # Trim chat log to max size
        if len(self._chat_log) > self._chat_log_max_size:
            self._chat_log = self._chat_log[-self._chat_log_max_size:]
    
    def show_overlay(self, message: str, duration: float = 0):
        """Show a menu overlay WITHOUT adding to chat log (for menus/debug)."""
        # Store content directly - don't wrap, the menu formats itself
        self._menu_overlay_content = message.split('\n')
        self._menu_overlay_active = True

    def dismiss_overlay(self):
        """Dismiss the menu overlay."""
        self._menu_overlay_content = []
        self._menu_overlay_active = False

    def _overlay_menu(self, base_output: List[str], width: int) -> List[str]:
        """Overlay menu content (debug menu, settings, etc.)."""
        if not self._menu_overlay_content:
            return base_output
        
        return self._overlay_box(base_output, self._menu_overlay_content, "MENU", width)

    def dismiss_message(self):
        """Dismiss the current message overlay."""
        if self._message_queue:
            self._message_queue.clear()
        self._message_expire = 0
        self._show_message_overlay = False

    def scroll_chat_up(self):
        """Scroll chat log up (show older messages)."""
        import textwrap
        wrap_width = 60  # Approximate
        
        # Calculate total wrapped lines
        total_lines = 0
        for _, msg, _ in self._chat_log:
            wrapped = textwrap.wrap(msg, width=wrap_width) if msg else ['']
            total_lines += len(wrapped)
        
        max_scroll = max(0, total_lines - self._chat_log_visible_lines)
        self._chat_scroll_offset = min(self._chat_scroll_offset + self._chat_log_visible_lines, max_scroll)

    def scroll_chat_down(self):
        """Scroll chat log down (show newer messages)."""
        self._chat_scroll_offset = max(0, self._chat_scroll_offset - self._chat_log_visible_lines)

    def show_menu(self, title: str, items: List[Dict], selected_index: int = 0,
                  show_numbers: bool = True, footer: str = "[^v] Navigate  [Enter] Select  [ESC] Close",
                  max_visible: int = 12):
        """
        Show a menu with arrow-key selection highlighting and pagination.

        Args:
            title: Menu title
            items: List of dicts with 'label', optional 'description', 'enabled'
            selected_index: Currently selected item index
            show_numbers: Show number prefixes
            footer: Footer text with controls hint
            max_visible: Maximum visible items before scrolling
        """
        lines = []
        lines.append(f"=== {title} ===")
        lines.append("")

        if not items:
            lines.append("  (no items)")
        else:
            # Calculate visible window for scrolling
            total_items = len(items)
            
            if total_items <= max_visible:
                # No scrolling needed
                start_idx = 0
                end_idx = total_items
            else:
                # Calculate scroll window to keep selected item visible
                half_window = max_visible // 2
                if selected_index < half_window:
                    start_idx = 0
                elif selected_index >= total_items - half_window:
                    start_idx = total_items - max_visible
                else:
                    start_idx = selected_index - half_window
                end_idx = start_idx + max_visible
            
            # Show scroll indicator at top if not at beginning
            if start_idx > 0:
                lines.append(f"   [...{start_idx} more above...]")
            
            for i in range(start_idx, end_idx):
                item = items[i]
                is_selected = (i == selected_index)
                enabled = item.get('enabled', True)
                label = item.get('label', f'Item {i+1}')
                desc = item.get('description', '')

                # Build prefix - use >> for selected
                if is_selected:
                    prefix = ">> "
                else:
                    prefix = "   "

                # Build number
                if show_numbers:
                    num = f"[{i+1}] "
                else:
                    num = ""

                # Build label with enabled state
                if not enabled:
                    label_text = f"{num}{label} (locked)"
                else:
                    label_text = f"{num}{label}"

                lines.append(f"{prefix}{label_text}")

                # Show description for selected item
                if is_selected and desc:
                    lines.append(f"       {desc}")
            
            # Show scroll indicator at bottom if not at end
            if end_idx < total_items:
                lines.append(f"   [...{total_items - end_idx} more below...]")

        lines.append("")
        lines.append(footer)

        self.show_message("\n".join(lines), duration=0)

    def show_effect(self, effect_name: str, duration: float = 1.0):
        """Show a visual effect."""
        animation_controller.play_effect(effect_name, duration)

    def show_closeup(self, action: Optional[str] = None, duration: float = 2.0):
        """Show an emotion close-up in the side panel."""
        self._show_closeup = True
        self._closeup_expire = time.time() + duration
        self._closeup_action = action

    def _check_closeup_expired(self):
        """Check and clear expired closeup."""
        if self._show_closeup and time.time() > self._closeup_expire:
            self._show_closeup = False
            self._closeup_action = None

    def set_duck_state(self, state: str, duration: float = 3.0):
        """Set the duck's visual state in the playfield."""
        self.duck_pos.set_state(state, duration)

    def toggle_help(self):
        """Toggle the help overlay."""
        self._show_help = not self._show_help
        self._show_stats = False
        self._show_talk = False
        self._show_inventory = False
        self.dismiss_message()  # Close any menu overlays

    def toggle_stats(self):
        """Toggle the stats overlay."""
        self._show_stats = not self._show_stats
        self._show_help = False
        self._show_talk = False
        self._show_inventory = False
        self.dismiss_message()  # Close any menu overlays

    def toggle_talk(self):
        """Toggle the talk overlay."""
        was_talking = self._show_talk
        self._show_talk = not self._show_talk
        self._show_help = False
        self._show_stats = False
        self._show_inventory = False
        self._talk_buffer = ""
        # Only dismiss messages when OPENING talk mode, not when closing
        # (closing talk mode should preserve the response message)
        if not was_talking:
            self.dismiss_message()  # Close any menu overlays when opening talk

    def toggle_inventory(self):
        """Toggle the inventory overlay."""
        self._show_inventory = not self._show_inventory
        if self._show_inventory:
            self._inventory_page = 0  # Reset to first page when opening
        self._show_help = False
        self._show_stats = False
        self._show_talk = False
        self._show_shop = False
        self.dismiss_message()  # Close any menu overlays

    def toggle_shop(self):
        """Toggle the shop overlay."""
        self._show_shop = not self._show_shop
        self._show_help = False
        self._show_stats = False
        self._show_talk = False
        self._show_inventory = False
        self.dismiss_message()  # Close any menu overlays

    def hide_overlays(self):
        """Hide all overlays."""
        self._show_help = False
        self._show_stats = False
        self._show_talk = False
        self._show_inventory = False
        self._show_shop = False
        self.dismiss_message()  # Close any menu overlays

    def is_talking(self) -> bool:
        """Check if talk mode is active."""
        return self._show_talk

    def is_inventory_open(self) -> bool:
        """Check if inventory is open."""
        return self._show_inventory

    def is_shop_open(self) -> bool:
        """Check if shop is open."""
        return self._show_shop

    def get_inventory_item(self, index: int) -> Optional[str]:
        """Get item ID at inventory index (0-based)."""
        if 0 <= index < len(self._inventory_items):
            return self._inventory_items[index]
        return None

    def add_talk_char(self, char: str):
        """Add a character to talk buffer."""
        if len(self._talk_buffer) < 50:
            self._talk_buffer += char

    def backspace_talk(self):
        """Remove last character from talk buffer."""
        self._talk_buffer = self._talk_buffer[:-1]

    def get_talk_buffer(self) -> str:
        """Get current talk buffer."""
        return self._talk_buffer

    def clear_talk_buffer(self):
        """Clear talk buffer."""
        self._talk_buffer = ""

    def render_offline_summary(self, duck_name: str, hours: float, changes: dict):
        """Render a summary of what happened while offline."""
        if hours < 0.016:
            return

        from core.clock import GameClock
        clock = GameClock()
        time_str = clock.format_duration(hours)

        # Helper to pad content to exactly 44 chars
        def pad_line(content: str) -> str:
            return (content + " " * 44)[:44]

        lines = [
            "",
            "  " + BOX_DOUBLE["tl"] + BOX_DOUBLE["h"] * 44 + BOX_DOUBLE["tr"],
            "  " + BOX_DOUBLE["v"] + " " * 44 + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + pad_line("  Welcome back!") + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + pad_line(f"  {duck_name} missed you!") + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + " " * 44 + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + pad_line(f"  You were away for {time_str}") + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + " " * 44 + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + pad_line("  While you were gone:") + BOX_DOUBLE["v"],
        ]

        for need, change in changes.items():
            if change != 0:
                direction = "decreased" if change < 0 else "recovered"
                line = f"   - {need}: {direction}"
                lines.append("  " + BOX_DOUBLE["v"] + pad_line(f"  {line}") + BOX_DOUBLE["v"])

        lines.extend([
            "  " + BOX_DOUBLE["v"] + " " * 44 + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + pad_line("  Press any key to continue...") + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + " " * 44 + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["bl"] + BOX_DOUBLE["h"] * 44 + BOX_DOUBLE["br"],
            "",
        ])

        print(self.term.home + self.term.clear)
        print("\n".join(lines))

    def update_animation(self):
        """Update animation frame counter."""
        current = time.time()
        if current - self._animation_time > 0.3:
            self._animation_frame = (self._animation_frame + 1) % 4
            self._animation_time = current
            animation_controller.update()
