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

    # All states that support animation frame cycling
    # Only includes states that exist for all growth stages
    ANIMATABLE_STATES = {
        # User interaction states
        "sleeping", "eating", "playing", "cleaning", "petting",
        # Weather reaction states
        "cold", "hot", "shaking", "scared", "excited", "curious",
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

        # Randomly pick new target when idle
        if self._state == "idle" and self._idle_timer > random.uniform(3, 8):
            if random.random() < 0.6:  # 60% chance to wander
                self._pick_new_target()
                self._idle_timer = 0

        # Move towards target
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

        # Weather particle settings - Enhanced for more dramatic visuals
        # Note: sunny/clear weather has no particles (just a nice day)
        weather_chars = {
            "rainy": ["│", "╎", "┆", "╏", "|", "'", ","],  # Rain streaks
            "stormy": ["│", "|", "'", ",", ":"],  # Heavy rain drops (cleaner look)
            "snowy": ["❄", "*", "✦", "❅", "·", "°", "✧"],  # Snowflakes
            "foggy": ["░", "▒", "~", "≈", " ", "▓"],  # Thick fog
            "windy": ["→", "⟹", "~", "≫", "»", "›", "~"],  # Wind direction
            "rainbow": ["♦", "★", "✦", "◊", "*"],  # Sparkles for rainbow
        }

        particle_density = {
            "rainy": 0.20,      # More rain
            "stormy": 0.25,     # Heavy storm rain (was 0.35)
            "snowy": 0.12,      # More snow
            "foggy": 0.15,      # Thicker fog
            "windy": 0.10,      # More wind particles
            "rainbow": 0.08,    # Magic sparkles
        }

        particle_speed = {
            "rainy": 2.0,       # Faster rain
            "stormy": 2.5,      # Fast storm rain (was 3.0)
            "snowy": 0.4,       # Slow gentle snow
            "foggy": 0.15,      # Very slow fog drift
            "windy": 1.5,       # Fast wind
            "rainbow": 0.5,     # Gentle rainbow sparkle
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
            if weather_type == "windy":
                new_x = x + 0.8  # Move right
            elif weather_type == "snowy":
                new_x = x + random.uniform(-0.3, 0.3)  # Gentle drift
            elif weather_type == "stormy":
                new_x = x + random.uniform(-0.5, 0.5)  # Chaotic
            else:
                new_x = x

            if new_y < height and 0 <= new_x < width:
                new_particles.append((new_x, new_y, char))

        # Spawn new particles at top
        for x in range(width):
            if random.random() < density:
                char = random.choice(chars)
                new_particles.append((float(x), 0.0, char))

        # Lightning flash for storms (rare and brief)
        if weather_type == "stormy" and self._weather_frame % 45 == 0 and random.random() < 0.25:
            # Add single lightning bolt character
            bolt_x = random.randint(3, width - 3)
            bolt_y = random.randint(0, min(3, height - 1))
            new_particles.append((float(bolt_x), float(bolt_y), "⚡"))

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
            sky_char = "░"
            bg_color = self.term.on_color_rgb(255, 200, 150)  # Warm orange-pink
            celestials = [(width - 5, "🌅"), (3, "☆"), (width - 10, "✦")]
        elif 7 <= hour < 11:  # Morning
            sky_char = " "
            bg_color = None  # Clear sky
            celestials = [(width // 4, "☀"), (5, "☁"), (width - 8, "☁")]
        elif 11 <= hour < 14:  # Midday
            sky_char = " "
            bg_color = None
            celestials = [(width // 2, "☀")]
        elif 14 <= hour < 17:  # Afternoon
            sky_char = " "
            bg_color = None
            celestials = [(3 * width // 4, "☀"), (width // 4, "☁")]
        elif 17 <= hour < 19:  # Evening
            sky_char = "░"
            bg_color = self.term.on_color_rgb(255, 180, 100)  # Golden hour
            celestials = [(width - 3, "🌅"), (width // 2, "☁")]
        elif 19 <= hour < 21:  # Dusk
            sky_char = "▒"
            bg_color = self.term.on_color_rgb(100, 80, 120)  # Purple dusk
            celestials = [(width - 4, "🌆"), (5, "★"), (width // 2, "☆")]
        elif 21 <= hour or hour < 0:  # Night
            sky_char = " "
            bg_color = self.term.on_color_rgb(20, 20, 40)  # Dark blue
            celestials = [
                (width - 5, "🌙"),
                (3, "★"), (8, "☆"), (15, "✦"), (width - 12, "★"),
                (width // 2 - 3, "☆"), (width // 2 + 5, "✦")
            ]
        else:  # Late night (0-5)
            sky_char = " "
            bg_color = self.term.on_color_rgb(10, 10, 25)  # Very dark
            celestials = [
                (width - 6, "🌑"),
                (4, "★"), (10, "☆"), (18, "★"), (width - 15, "✦"),
                (width // 3, "☆"), (2 * width // 3, "★")
            ]

        return sky_char, bg_color, celestials

    def _get_weather_ambient_effects(self, weather_type: Optional[str], width: int) -> List[str]:
        """Get ambient text effects for weather displayed at top of playfield."""
        if not weather_type:
            return []

        effects = {
            "sunny": ["~ warm sunbeams ~", "☀ bright and cheerful ☀"],
            "cloudy": ["☁ clouds drift by ☁", "~ overcast skies ~"],
            "rainy": ["💧 pitter patter 💧", "~ splish splash ~", "🌧 rain falls gently 🌧"],
            "stormy": ["⚡ THUNDER RUMBLES ⚡", "💨 wind howls 💨", "🌩 lightning flashes 🌩"],
            "snowy": ["❄ snowflakes drift ❄", "~ winter wonderland ~", "☃ frosty and cold ☃"],
            "foggy": ["🌫 mist swirls 🌫", "~ mysterious fog ~", "👀 visibility low 👀"],
            "windy": ["💨 whoooosh! 💨", "~ leaves swirl ~", "🍃 breezy day 🍃"],
            "rainbow": ["🌈 magical colors! 🌈", "✨ make a wish! ✨", "🦄 rare and beautiful 🦄"],
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
        MAX_WIDTH = 120   # Maximum game width
        MAX_HEIGHT = 40   # Maximum game height
        
        term_width = max(self.term.width, 60)
        term_height = max(self.term.height, 20)
        
        width = min(term_width, MAX_WIDTH)
        height = min(term_height, MAX_HEIGHT)

        # Dynamic layout based on terminal width
        # Side panel needs at least 25 chars, playfield gets the rest
        side_panel_width = max(25, min(35, width // 3))
        playfield_width = width - side_panel_width

        # Update playfield dimensions for duck movement
        field_inner_width = playfield_width - 2
        field_height = max(8, height - 10)  # Reduced from 15 to 10 for taller playfield
        self.duck_pos.field_width = field_inner_width
        self.duck_pos.field_height = field_height

        # Get current location from exploration system
        current_location = None
        if hasattr(game, 'exploration') and game.exploration and game.exploration.current_area:
            current_location = game.exploration.current_area.name

        # Regenerate ground pattern if size or location changed, or on first render
        size_changed = len(self._ground_pattern) != field_height or (self._ground_pattern and len(self._ground_pattern[0]) != field_inner_width)
        location_changed = current_location != self._current_location

        if size_changed or location_changed or self._first_render:
            self._current_location = current_location
            self._generate_ground_pattern(current_location)
            self._first_render = False

        # Build the frame
        output = []

        # Header spanning full width - include currency and weather if available
        currency = game.habitat.currency if hasattr(game, 'habitat') else 0
        weather_info = None
        if hasattr(game, 'atmosphere') and game.atmosphere:
            weather_info = game.atmosphere.current_weather
        output.extend(self._render_header_bar(duck, width, currency, weather_info))

        # Get equipped cosmetics and placed items from habitat
        equipped_cosmetics = game.habitat.equipped_cosmetics if hasattr(game, 'habitat') else {}
        # Placed items (ball, etc.) only appear at Home Pond
        if current_location == "Home Pond" or current_location is None:
            placed_items = game.habitat.placed_items if hasattr(game, 'habitat') else []
        else:
            placed_items = []

        # Get built structures from building system
        built_structures = []
        if hasattr(game, 'building') and game.building:
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

        # Message area
        output.extend(self._render_messages(width))

        # Controls bar
        output.extend(self._render_controls_bar(width))

        # Check for expired closeup
        self._check_closeup_expired()

        # Check for expired celebration
        self._check_celebration_expired()

        # Overlays (help, stats, inventory, celebration, item interaction)
        if self._show_celebration:
            output = self._overlay_celebration(output, width)
        elif hasattr(game, '_item_interaction_active') and game._item_interaction_active:
            output = self._overlay_item_interaction(output, game, width)
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
        elif self._show_message_overlay:
            output = self._overlay_message(output, width)

        # Print frame - fill terminal (no clear to prevent flashing)
        print(self.term.home, end="")
        for i, line in enumerate(output):
            if i < height - 1:  # Leave one line at bottom
                # Use move to ensure proper positioning and overwrite
                # Use ANSI-aware functions for lines that may contain color codes
                truncated = _visible_truncate(line, width)
                padded = _visible_ljust(truncated, width)
                # End each line with terminal reset to prevent color bleeding
                print(self.term.move(i, 0) + padded + self.term.normal, end="")

    def _render_header_bar(self, duck: "Duck", width: int, currency: int = 0, weather=None, time_info=None) -> List[str]:
        """Render the top header bar with weather and time info."""
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

        # Weather icons and names
        weather_data = {
            "sunny": ("☀", "Sunny"),
            "cloudy": ("☁", "Cloudy"),
            "rainy": ("🌧", "Rainy"),
            "stormy": ("⛈", "Stormy"),
            "snowy": ("❄", "Snowy"),
            "foggy": ("🌫", "Foggy"),
            "windy": ("💨", "Windy"),
            "rainbow": ("🌈", "Rainbow"),
        }

        # Time of day icons and names
        time_data = {
            "dawn": ("🌅", "Dawn"),
            "morning": ("🌤", "Morning"),
            "midday": ("☀", "Midday"),
            "afternoon": ("🌤", "Afternoon"),
            "evening": ("🌆", "Evening"),
            "dusk": ("🌇", "Dusk"),
            "night": ("🌙", "Night"),
            "late_night": ("🌑", "Late Night"),
        }

        # Build weather string with icon and label
        weather_part = ""
        if weather:
            w_icon, w_name = weather_data.get(weather.weather_type.value, ("?", "Unknown"))
            weather_part = f" {w_icon} {w_name} "

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
        mood_part = mood_ind
        age_part = age_str
        coin_part = f"${currency}"

        # Create bordered header
        inner_width = width - 2

        # Simplified format: Name | Weather Time | Mood Age $Money
        left_side = f" {name_part} "
        if weather_part:
            left_side += f"| {weather_part.strip()}"
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

        # Update weather particles
        weather_type = weather_info.weather_type.value if weather_info else None
        self._update_weather_particles(inner_width, height if height else self.duck_pos.field_height, weather_type)

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
                visitor_animator.set_visitor(
                    personality, 
                    current_visitor.name,
                    friendship_level,
                    visit_number,
                    unlocked_topics
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
        
        item_placements = []
        if placed_items:
            for placed_item in placed_items:
                art = get_item_art(placed_item.item_id)
                color_func = get_item_color(placed_item.item_id)
                # Scale item position to playfield coordinates
                item_x = int(placed_item.x * inner_width / 20)
                item_y = int(placed_item.y * field_height / 12)
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

            # Add duck if on this row (duck renders ON TOP of items)
            duck_y = self.duck_pos.y
            duck_x = self.duck_pos.x

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
                        row[int(px)] = (char, weather_color)

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

        # Bottom of playfield
        lines.append(BOX["bl"] + BOX["h"] * inner_width + BOX["br"])

        return lines

    def _render_side_panel(self, duck: "Duck", game: "Game", width: int) -> List[str]:
        """Render the side panel with close-up, stats, shortcuts, and info."""
        inner_width = width - 2
        lines = []

        # Panel header
        lines.append(BOX["tl"] + BOX["h"] * inner_width + BOX["tr"])

        # Close-up face section (compact)
        mood = duck.get_mood()
        closeup = get_emotion_closeup(mood.state, self._closeup_action if self._show_closeup else None)

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

        # Needs bars (compact)
        needs_data = [
            ("HUN", duck.needs.hunger, self._get_need_indicator(duck.needs.hunger)),
            ("ENG", duck.needs.energy, self._get_need_indicator(duck.needs.energy)),
            ("FUN", duck.needs.fun, self._get_need_indicator(duck.needs.fun)),
            ("CLN", duck.needs.cleanliness, self._get_need_indicator(duck.needs.cleanliness)),
            ("SOC", duck.needs.social, self._get_need_indicator(duck.needs.social)),
        ]

        for name, value, indicator in needs_data:
            bar = self._make_progress_bar(value, 8)
            pct = f"{int(value)}%"
            # Build line: NAME[bar] ##%
            line_content = f"{name}{bar} {pct}"
            # Truncate and pad to exact width
            line_content = _visible_truncate(line_content, inner_width)
            line_content = _visible_ljust(line_content, inner_width)
            lines.append(BOX["v"] + line_content + BOX["v"])

        # Divider - Shortcuts Section
        lines.append(BOX["t_right"] + BOX["h"] * inner_width + BOX["t_left"])
        shortcut_title = _visible_center("─── SHORTCUTS ───", inner_width)
        lines.append(BOX["v"] + shortcut_title + BOX["v"])

        # Actions column - organized by function
        shortcuts = [
            "[F] Feed    [P] Play",
            "[L] Clean  [D] Pet  ",
            "[Z] Sleep   [T] Talk",
            "",
            "[E] Explore [A] Areas",
            "[C] Craft   [R] Build",
            "",
            "[I] Items   [B] Shop",
            "[G] Goals   [S] Stats",
            "[H] Help    [Q] Quit",
        ]

        for shortcut in shortcuts:
            if shortcut:
                centered = _visible_center(shortcut, inner_width)
                lines.append(BOX["v"] + centered + BOX["v"])

        # Divider
        lines.append(BOX["t_right"] + BOX["h"] * inner_width + BOX["t_left"])

        # Activity/Status
        activity = self._get_activity_text(duck)
        activity_centered = _visible_center(activity, inner_width)
        lines.append(BOX["v"] + activity_centered + BOX["v"])

        # Current action message (truncate if needed)
        action_msg = duck.get_action_message() or "Just vibing..."
        action_msg = _visible_truncate(action_msg, inner_width - 2)
        action_centered = _visible_center(action_msg, inner_width)
        lines.append(BOX["v"] + action_centered + BOX["v"])
        
        # Current location (from exploration system)
        if hasattr(game, 'exploration') and game.exploration and game.exploration.current_area:
            area_name = game.exploration.current_area.name
            location = f"@ {area_name}"  # Use @ instead of emoji for consistent width
            location = _visible_truncate(location, inner_width)
            location_centered = _visible_center(location, inner_width)
            lines.append(BOX["v"] + location_centered + BOX["v"])

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
            hint = " Press [H] for help "
            lines.append(BOX["v"] + hint.center(inner_width)[:inner_width] + BOX["v"])
            lines.append(BOX["v"] + " " * inner_width + BOX["v"])

        lines.append(BOX["bl"] + BOX["h"] * inner_width + BOX["br"])

        return lines

    def _render_controls_bar(self, width: int) -> List[str]:
        """Render the bottom controls bar."""
        inner_width = width - 2

        # Compact controls hint
        controls = " [H]elp for shortcuts • [M]ute • [+/-] Volume • [Q]uit "

        lines = [
            BOX["tl"] + BOX["h"] * inner_width + BOX["tr"],
            BOX["v"] + controls.center(inner_width)[:inner_width] + BOX["v"],
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
        title = f"═══ {game_name} ═══"
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

    def _render_title_screen(self):
        """Render the title/new game screen with dancing duck animation."""
        self._title_frame = (self._title_frame + 1) % 120

        # Dancing duck animation frames - Teen duck style
        duck_frames = [
            # Frame 1 - Idle happy
            [
                "              ,~~.                     ",
                "         ,   (  ^ )>        ★          ",
                "         )`~~'    (                    ",
                "        (    .__)  )                   ",
                "         `-.____.,'                    ",
                "             ||          ♪             ",
                "           ~~~~~                       ",
            ],
            # Frame 2 - Dance left
            [
                "           ,~~.                        ",
                "      ,   (  o )>    ♫                 ",
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
                "           )`~~'    (      ♪           ",
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
                "      (    .◡.)  )        ♫ ♪         ",
                "       `-.____.,'                      ",
                "          \\    /                       ",
                "         ~~~~~~~                       ",
            ],
            # Frame 5 - Lean left
            [
                "         ,~~.      ♪                   ",
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
                "             ,   (  ~ )>      ♫        ",
                "             )`~~'    (                ",
                "            (    .__)  )               ",
                "             `-.____.,'                ",
                "                 |   \\\\                ",
                "               ~~~~~~~                 ",
            ],
            # Frame 7 - Spin!
            [
                "           ✧ SPIN ✧                    ",
                "              ,~~.                     ",
                "         ,   ( @ @ )>                  ",
                "         )`~~'    (       ♫            ",
                "        (    .~~)  )                   ",
                "         `-.____.,'                    ",
                "            ~~~~~~~                    ",
            ],
            # Frame 8 - Point!
            [
                "              ,~~.                     ",
                "         ,   (  ^ )>======>>           ",
                "         )`~~'    (                    ",
                "        (    .ᴗ.)  )       ♪           ",
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
                "        (    .__)  )      ★            ",
                "         `-.____.,'                    ",
                "             ||                        ",
                "           ~~~~~                       ",
            ],
        ]

        # Slow down animation - change frame every 12 ticks instead of 10
        frame_idx = (self._title_frame // 12) % len(duck_frames)
        duck_art = duck_frames[frame_idx]

        # Sparkle effects that rotate slowly (change every 15 ticks)
        sparkle_chars = ["✦", "★", "✧", "☆"]
        sparkle_idx = (self._title_frame // 15) % len(sparkle_chars)
        sparkle1 = sparkle_chars[sparkle_idx]
        sparkle2 = sparkle_chars[(sparkle_idx + 2) % len(sparkle_chars)]

        # Build title screen
        title_art = [
            f"    {sparkle1}                                                    {sparkle2}",
            "    ╔══════════════════════════════════════════════════════╗    ",
            "    ║                                                      ║    ",
            "    ║      ██████╗██╗  ██╗███████╗███████╗███████╗███████╗ ║    ",
            "    ║     ██╔════╝██║  ██║██╔════╝██╔════╝██╔════╝██╔════╝ ║    ",
            "    ║     ██║     ███████║█████╗  █████╗  ███████╗█████╗   ║    ",
            "    ║     ██║     ██╔══██║██╔══╝  ██╔══╝  ╚════██║██╔══╝   ║    ",
            "    ║     ╚██████╗██║  ██║███████╗███████╗███████║███████╗ ║    ",
            "    ║      ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚══════╝ ║    ",
            "    ║                                                      ║    ",
            "    ║            ═══ THE DUCK ═══                          ║    ",
            "    ║                                                      ║    ",
            "    ╠══════════════════════════════════════════════════════╣    ",
        ]

        # Add the dancing duck with yellow color
        for line in duck_art:
            padded_line = line + " " * (54 - len(line)) if len(line) < 54 else line[:54]
            yellow_duck = self.term.yellow + padded_line + self.term.normal
            title_art.append(f"    ║{yellow_duck}║    ")

        # Add footer
        title_art.extend([
            "    ╠══════════════════════════════════════════════════════╣    ",
            "    ║                                                      ║    ",
            "    ║         Your virtual pet duck awaits!                ║    ",
            "    ║                                                      ║    ",
            "    ╠══════════════════════════════════════════════════════╣    ",
            "    ║                                                      ║    ",
            "    ║            Press [ENTER] to start                    ║    ",
            "    ║            Press [Q] to quit                         ║    ",
            "    ║                                                      ║    ",
            "    ╚══════════════════════════════════════════════════════╝    ",
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
            "═══ DUCK CARE ═══",
            "[F]/[1] Feed    [P]/[2] Play    [L]/[3] Clean",
            "[D]/[4] Pet     [Z]/[5] Sleep   [T] Talk",
            "",
            "═══ MENUS ═══",
            "[I] Inventory   [G] Goals    [S] Stats",
            "[B] Shop        [U] Use Item [O] Quests",
            "",
            "═══ ACTIVITIES ═══",
            "[E] Explore     [A] Areas    [C] Craft",
            "[R] Build       [J] Minigames",
            "[K] Duck Fact   [W] Weather Activities",
            "",
            "═══ SPECIAL ═══",
            "[V] Trading     [Y] Scrapbook",
            "[6] Treasure    [7] Secrets",
            "",
            "═══ AUDIO ═══",
            "[M] Sound  [N] Music  [+]/[-] Volume",
            "",
            "═══ SYSTEM ═══",
            "[Q] Save & Quit  [X] Reset Game",
            "",
            "Press [H] to close",
        ]

        return self._overlay_box(base_output, help_text, "HELP", width)

    def _overlay_stats(self, base_output: List[str], duck: "Duck", game: "Game", width: int) -> List[str]:
        """Overlay statistics screen."""
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

        stats_text = [
            f"🦆 {duck.name} - {duck.get_growth_stage_display()}",
            "",
            f"╔══════════════ PROGRESS ══════════════╗",
            f"  Level {prog.level}: {prog.title}",
            f"  XP: {xp_bar} {int(xp_pct)}%",
            f"  {streak_line}",
            f"  Best Streak: {prog.longest_streak} days",
            f"╚══════════════════════════════════════╝",
            "",
            f"╔══════════════ BONDING ═══════════════╗",
            f"  Relationship: {memory.get_relationship_description()}",
            f"  Mood Trend: {memory.get_recent_mood_trend()}",
            f"  Love Score: {'💕' * (love_score // 20)}{'💔' * (5 - love_score // 20)} {love_score}%",
            f"╚══════════════════════════════════════╝",
            "",
            f"╔══════════════ WORLD ═════════════════╗",
            f"  🗺️  Location: {biome_name}",
            f"  🌲 Areas: {area_count} discovered",
            f"  📦 Materials: {mat_count} types ({mat_total} total)",
            f"  🏠 Structures: {struct_count} built",
            f"╚══════════════════════════════════════╝",
            "",
            f"╔══════════════ LIFETIME ══════════════╗",
            f"  Days Played: {prog.days_played}",
            f"  Total Care: {total_care_actions} actions",
            f"  Collectibles: {coll_owned}/{coll_total} 🏆",
            f"╚══════════════════════════════════════╝",
            "",
            "       Press [S] to close",
        ]

        return self._overlay_box(base_output, stats_text, "📊 STATISTICS", width)

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
        """Overlay inventory screen."""
        inv = game.inventory

        inv_text = [
            f"Items: {len(inv.items)}/{inv.max_size}",
            "-" * 30,
        ]

        # Group items by count and create numbered list
        item_counts: Dict[str, int] = {}
        unique_items: List[str] = []
        for item_id in inv.items:
            if item_id not in item_counts:
                unique_items.append(item_id)
            item_counts[item_id] = item_counts.get(item_id, 0) + 1

        from world.items import get_item_info
        for idx, item_id in enumerate(unique_items[:9], start=1):  # Max 9 items shown
            item = get_item_info(item_id)
            if item:
                count_str = f"x{item_counts[item_id]}" if item_counts[item_id] > 1 else ""
                type_tag = item.item_type.value[:4].upper()
                line = f"[{idx}] {item.icon} {item.name} {count_str}"
                inv_text.append(line)

        if not item_counts:
            inv_text.append("(Empty)")
            inv_text.append("")
            inv_text.append("Find items by exploring!")

        inv_text.extend([
            "",
            "Press [1-9] to use item",
            "Press [I] to close",
        ])

        # Store unique items list for key handling
        self._inventory_items = unique_items

        return self._overlay_box(base_output, inv_text, "INVENTORY", width)

    def _overlay_box(self, base_output: List[str], content: List[str], title: str, width: int) -> List[str]:
        """Generic overlay box."""
        box_width = min(50, width - 4)
        box_height = len(content) + 4

        # Create box - use _visible_len for title to handle colored titles
        title_visible_len = _visible_len(title)
        box_lines = [
            BOX_DOUBLE["tl"] + BOX_DOUBLE["h"] + f" {title} " + BOX_DOUBLE["h"] * (box_width - title_visible_len - 4) + BOX_DOUBLE["tr"],
        ]

        for line in content:
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
        box_lines.append(self.term.cyan("╔" + "═" * (box_width - 2) + "╗"))
        
        for line in content:
            # Truncate and pad to box width
            centered = _visible_center(line, box_width - 4)
            centered = _visible_truncate(centered, box_width - 4)
            centered = _visible_ljust(centered, box_width - 4)
            box_lines.append(self.term.cyan("║ ") + centered + self.term.cyan(" ║"))
        
        # Bottom border
        box_lines.append(self.term.cyan("╚" + "═" * (box_width - 2) + "╝"))

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
        """Overlay shop interface."""
        from world.shop import get_items_by_category, ItemCategory
        from ui.habitat_art import render_item_preview
        
        # Get items in current category
        category = ItemCategory(self._shop_categories[self._shop_category_index].lower())
        items = get_items_by_category(category)
        
        # Build shop display
        content = []
        content.append(f"💰 Currency: ${habitat.currency}")
        content.append("")
        content.append("Categories: " + " ".join(
            f"[{cat}]" if i == self._shop_category_index else cat 
            for i, cat in enumerate(self._shop_categories)
        ))
        content.append("")
        
        # Show items (max 10)
        for i, item in enumerate(items[:10]):
            prefix = "→ " if i == self._shop_item_index else "  "
            owned = "✓" if habitat.owns_item(item.id) else " "
            affordable = "💰" if habitat.can_afford(item.cost) else "🔒"
            content.append(f"{prefix}{owned} {item.name} ${item.cost} {affordable} (Lv{item.unlock_level})")
        
        if self._shop_item_index < len(items):
            item = items[self._shop_item_index]
            content.append("")
            content.append(item.description)
        
        content.append("")
        content.append("← → : Change category | ↑ ↓ : Select item | [B]uy | [ESC]: Close")
        
        return self._overlay_box(base_output, content, "🏪 SHOP", width)

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

    def show_message(self, message: str, duration: float = 5.0):
        """Show a message to the player as an overlay (default 5 seconds). If duration is 0, message persists until dismissed."""
        import textwrap
        
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

    def dismiss_message(self):
        """Dismiss the current message overlay."""
        if self._message_queue:
            self._message_queue.clear()
        self._message_expire = 0
        self._show_message_overlay = False

    def show_menu(self, title: str, items: List[Dict], selected_index: int = 0,
                  show_numbers: bool = True, footer: str = "[↑↓] Navigate  [Enter] Select  [ESC] Close"):
        """
        Show a menu with arrow-key selection highlighting.

        Args:
            title: Menu title
            items: List of dicts with 'label', optional 'description', 'enabled'
            selected_index: Currently selected item index
            show_numbers: Show number prefixes
            footer: Footer text with controls hint
        """
        lines = []
        lines.append(f"═══ {title} ═══")
        lines.append("")

        if not items:
            lines.append("  (no items)")
        else:
            for i, item in enumerate(items):
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

    def toggle_stats(self):
        """Toggle the stats overlay."""
        self._show_stats = not self._show_stats
        self._show_help = False
        self._show_talk = False
        self._show_inventory = False

    def toggle_talk(self):
        """Toggle the talk overlay."""
        self._show_talk = not self._show_talk
        self._show_help = False
        self._show_stats = False
        self._show_inventory = False
        self._talk_buffer = ""

    def toggle_inventory(self):
        """Toggle the inventory overlay."""
        self._show_inventory = not self._show_inventory
        self._show_help = False
        self._show_stats = False
        self._show_talk = False
        self._show_shop = False

    def toggle_shop(self):
        """Toggle the shop overlay."""
        self._show_shop = not self._show_shop
        self._show_help = False
        self._show_stats = False
        self._show_talk = False
        self._show_inventory = False

    def hide_overlays(self):
        """Hide all overlays."""
        self._show_help = False
        self._show_stats = False
        self._show_talk = False
        self._show_inventory = False
        self._show_shop = False

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
