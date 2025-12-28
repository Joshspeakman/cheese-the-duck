"""
Terminal UI renderer using blessed library - Enhanced version with side panel layout.
Features a main playfield with moving duck and side panel with close-up, stats, etc.
"""
import time
import math
import random
import re
from typing import Optional, List, Dict, Tuple, TYPE_CHECKING
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
    Handles ANSI escape sequences correctly.
    """
    result = []
    visible_pos = 0
    i = 0
    
    while i < len(s):
        # Check for ANSI escape sequence
        match = _ANSI_ESCAPE.match(s, i)
        if match:
            # Always include ANSI codes in output (they're invisible)
            if visible_pos >= start and visible_pos < end:
                result.append(match.group())
            elif visible_pos < start:
                # Include opening codes before slice to maintain formatting
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

    def update(self, delta_time: float):
        """Update duck position and movement."""
        self._move_timer += delta_time
        self._idle_timer += delta_time
        self._state_animation_timer += delta_time

        # Cycle animation frames for non-idle states (every 0.4 seconds)
        if self._state in ["sleeping", "eating", "playing", "cleaning", "petting"]:
            if self._state_animation_timer > 0.4:
                self._animation_frame = (self._animation_frame + 1) % 2
                self._state_animation_timer = 0
            
            # Check if state duration has expired (return to idle)
            if self._state_duration > 0:
                import time
                if time.time() - self._state_start_time > self._state_duration:
                    self._state = "idle"
                    self._state_duration = 0
            return  # Don't wander while in interaction state

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
        self.target_x = random.randint(margin, self.field_width - margin - 6)
        self.target_y = random.randint(margin, self.field_height - margin - 3)

    def set_state(self, state: str, duration: float = 3.0):
        """Set duck state (idle, sleeping, eating, playing, cleaning, petting)."""
        import time
        self._state = state
        self._animation_frame = 0
        self._state_animation_timer = 0
        self._state_duration = duration
        self._state_start_time = time.time()
        
        # Stop moving during interaction states
        if state in ["sleeping", "eating", "playing", "cleaning", "petting"]:
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
        self._generate_ground_pattern()

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

    def _generate_ground_pattern(self):
        """Generate static ground pattern."""
        self._ground_pattern = []
        for y in range(self.duck_pos.field_height):
            row = ""
            for x in range(self.duck_pos.field_width):
                row += random.choice(GROUND_CHARS)
            self._ground_pattern.append(row)

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

        # Update duck position
        delta = time.time() - self._last_render_time if self._last_render_time else 0.033
        self.duck_pos.update(delta)
        self._last_render_time = time.time()

        # Get terminal size - fully responsive
        width = max(self.term.width, 60)  # Minimum 60 chars
        height = max(self.term.height, 20)  # Minimum 20 rows

        # Dynamic layout based on terminal width
        # Side panel needs at least 25 chars, playfield gets the rest
        side_panel_width = max(25, min(35, width // 3))
        playfield_width = width - side_panel_width

        # Update playfield dimensions for duck movement
        field_inner_width = playfield_width - 2
        field_height = max(8, height - 15)  # Leave room for header, messages, controls
        self.duck_pos.field_width = field_inner_width
        self.duck_pos.field_height = field_height

        # Regenerate ground pattern if size changed
        if len(self._ground_pattern) != field_height or (self._ground_pattern and len(self._ground_pattern[0]) != field_inner_width):
            self._generate_ground_pattern()

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
        placed_items = game.habitat.placed_items if hasattr(game, 'habitat') else []

        # Main area: playfield on left, side panel on right
        playfield_lines = self._render_playfield(duck, playfield_width, field_height, equipped_cosmetics, placed_items)
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

        # Overlays (help, stats, inventory, celebration)
        if self._show_celebration:
            output = self._overlay_celebration(output, width)
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

        # Print frame - fill terminal (no clear to prevent flashing)
        print(self.term.home, end="")
        for i, line in enumerate(output):
            if i < height - 1:  # Leave one line at bottom
                # Use move to ensure proper positioning and overwrite
                # Use ANSI-aware functions for lines that may contain color codes
                truncated = _visible_truncate(line, width)
                padded = _visible_ljust(truncated, width)
                print(self.term.move(i, 0) + padded, end="")

    def _render_header_bar(self, duck: "Duck", width: int, currency: int = 0, weather=None) -> List[str]:
        """Render the top header bar with weather info."""
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

        # Weather icons
        weather_icons = {
            "sunny": "☀",
            "cloudy": "☁",
            "rainy": "🌧",
            "stormy": "⛈",
            "snowy": "❄",
            "foggy": "🌫",
            "windy": "💨",
            "rainbow": "🌈",
        }
        weather_part = ""
        if weather:
            weather_icon = weather_icons.get(weather.weather_type.value, "?")
            weather_part = f" {weather_icon} "

        # Build header
        name_part = f" {duck.name} the {duck.get_growth_stage_display()} "
        mood_part = f" {mood_ind} {mood.description.title()} "
        age_part = f" Age: {age_str} "
        coin_part = f" ${currency} "

        # Create bordered header
        inner_width = width - 2
        # Arrange: name ... weather ... mood ... age ... coins
        spacer_len = inner_width - len(name_part) - len(weather_part) - len(mood_part) - len(age_part) - len(coin_part)
        spacer = " " * max(0, spacer_len)
        header_content = f"{name_part}{weather_part}{spacer}{mood_part}{age_part}{coin_part}"

        lines = [
            BOX_DOUBLE["tl"] + BOX_DOUBLE["h"] * inner_width + BOX_DOUBLE["tr"],
            BOX_DOUBLE["v"] + header_content[:inner_width].ljust(inner_width) + BOX_DOUBLE["v"],
            BOX_DOUBLE["bl"] + BOX_DOUBLE["h"] * inner_width + BOX_DOUBLE["br"],
        ]
        return lines

    def _render_playfield(self, duck: "Duck", width: int, height: int = None, 
                          equipped_cosmetics: Dict[str, str] = None,
                          placed_items: List = None) -> List[str]:
        """Render the main playfield where duck moves around."""
        inner_width = width - 2
        lines = []

        # Title bar
        title = " DUCK HABITAT "
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

        # Pre-calculate all item placements with multi-line art
        # Each entry: (x, y, art_lines, color_func)
        from ui.habitat_art import get_item_art, get_item_color
        
        item_placements = []
        if placed_items:
            for placed_item in placed_items:
                art = get_item_art(placed_item.item_id)
                color_func = get_item_color(placed_item.item_id)
                # Scale item position to playfield coordinates
                item_x = int(placed_item.x * inner_width / 20)
                item_y = int(placed_item.y * field_height / 12)
                item_placements.append((item_x, item_y, art, color_func))

        # Build each row of the playfield
        # Use a grid of (char, color_func) tuples to handle colors properly
        for y in range(field_height):
            # Initialize row with (char, None) tuples for ground pattern
            row = [(c, None) for c in self._ground_pattern[y][:inner_width]]
            # Pad to inner_width
            while len(row) < inner_width:
                row.append((' ', None))

            # Add decorations (built-in playfield objects)
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
                        # No cosmetics, use plain duck art
                        duck_line = duck_art[dy] if dy < len(duck_art) else ""
                        for dx, char in enumerate(duck_line):
                            if char != ' ' and 0 <= duck_x + dx < inner_width:
                                row[duck_x + dx] = (char, None)

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

            # Convert row to string, applying colors
            row_chars = []
            for char, color_func in row:
                if color_func:
                    row_chars.append(color_func(char))
                else:
                    row_chars.append(char)
            row_str = "".join(row_chars)
            
            # Pad to inner_width (but length() counts ANSI codes, so we track visible chars)
            visible_len = len(row)  # We know we have exactly inner_width visible chars
            lines.append(BOX["v"] + row_str + BOX["v"])

        # Bottom of playfield
        lines.append(BOX["bl"] + BOX["h"] * inner_width + BOX["br"])

        return lines

    def _render_side_panel(self, duck: "Duck", game: "Game", width: int) -> List[str]:
        """Render the side panel with close-up, stats, and info."""
        inner_width = width - 2
        lines = []

        # Panel header
        lines.append(BOX["tl"] + BOX["h"] * inner_width + BOX["tr"])

        # Close-up face section (compact)
        mood = duck.get_mood()
        closeup = get_emotion_closeup(mood.state, self._closeup_action if self._show_closeup else None)

        if closeup:
            # Show compact close-up
            for closeup_line in closeup:
                truncated = closeup_line[:inner_width].center(inner_width)
                lines.append(BOX["v"] + truncated + BOX["v"])
        else:
            # Show mood status (compact)
            mood_text = f"{mood.description}".center(inner_width)
            lines.append(BOX["v"] + mood_text + BOX["v"])

        # Divider
        lines.append(BOX["t_right"] + BOX["h"] * inner_width + BOX["t_left"])

        # Needs bars
        needs_data = [
            ("HUN", duck.needs.hunger, self._get_need_indicator(duck.needs.hunger)),
            ("ENG", duck.needs.energy, self._get_need_indicator(duck.needs.energy)),
            ("FUN", duck.needs.fun, self._get_need_indicator(duck.needs.fun)),
            ("CLN", duck.needs.cleanliness, self._get_need_indicator(duck.needs.cleanliness)),
            ("SOC", duck.needs.social, self._get_need_indicator(duck.needs.social)),
        ]

        for name, value, indicator in needs_data:
            bar = self._make_progress_bar(value, 10)
            line = f"{name}{bar}{indicator}".ljust(inner_width)
            lines.append(BOX["v"] + line[:inner_width] + BOX["v"])

        # Divider
        lines.append(BOX["t_right"] + BOX["h"] * inner_width + BOX["t_left"])

        # Activity/Status
        activity = self._get_activity_text(duck)
        lines.append(BOX["v"] + f"{activity}".center(inner_width)[:inner_width] + BOX["v"])

        # Current action message (truncate if needed)
        action_msg = duck.get_action_message() or "Just vibing..."
        if len(action_msg) > inner_width - 2:
            action_msg = action_msg[:inner_width - 5] + "..."
        lines.append(BOX["v"] + action_msg.center(inner_width)[:inner_width] + BOX["v"])

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
        state = self.duck_pos.get_state()
        if state == "sleeping":
            return "Sleeping Zzz"
        elif state == "eating":
            return "Eating nom"
        elif state == "playing":
            return "Playing!"
        elif state == "walking":
            return "Wandering"
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

    def _make_progress_bar(self, value: float, width: int) -> str:
        """Create a fancy progress bar."""
        filled = int((value / 100) * width)

        # Color coding based on value
        if value >= 70:
            char = BAR_STYLES["full"]
        elif value >= 40:
            char = BAR_STYLES["high"]
        elif value >= 20:
            char = BAR_STYLES["med"]
        else:
            char = BAR_STYLES["low"]

        bar = char * filled + BAR_STYLES["empty"] * (width - filled)
        return f"[{bar}]"

    def _render_messages(self, width: int) -> List[str]:
        """Render the message area."""
        inner_width = width - 2

        lines = [
            BOX["tl"] + BOX["h"] * inner_width + BOX["tr"],
        ]

        if self._message_queue and time.time() < self._message_expire:
            for msg in self._message_queue[-2:]:
                msg_line = f" {msg} ".center(inner_width)
                lines.append(BOX["v"] + msg_line[:inner_width] + BOX["v"])
        else:
            lines.append(BOX["v"] + " " * inner_width + BOX["v"])
            lines.append(BOX["v"] + " " * inner_width + BOX["v"])

        lines.append(BOX["bl"] + BOX["h"] * inner_width + BOX["br"])

        return lines

    def _render_controls_bar(self, width: int) -> List[str]:
        """Render the bottom controls bar."""
        inner_width = width - 2

        # Two rows of controls for clarity
        controls1 = " [F]eed [P]lay [C]lean p[E]t [Z]leep "
        controls2 = " [T]alk [B]uy [S]tats [I]nv [G]oals [H]elp [Q]uit "

        lines = [
            BOX["tl"] + BOX["h"] * inner_width + BOX["tr"],
            BOX["v"] + controls1.center(inner_width)[:inner_width] + BOX["v"],
            BOX["v"] + controls2.center(inner_width)[:inner_width] + BOX["v"],
            BOX["bl"] + BOX["h"] * inner_width + BOX["br"],
        ]
        return lines

    def _render_title_screen(self):
        """Render the title/new game screen with dancing duck animation."""
        self._title_frame = (self._title_frame + 1) % 120

        # Dancing duck animation frames
        duck_frames = [
            # Frame 1 - Idle happy
            [
                "        ★  ✦  ★                       ",
                "           \\|/                        ",
                "        __(^.^)__                     ",
                "       /  (  >)  \\                    ",
                "      |  __\\/__   |                   ",
                "       \\ \\____/ /     ♪              ",
                "        \\_____/|>                    ",
                "          |   |                       ",
                "         _|   |_                      ",
                "        (•)   (•)                     ",
                "       ~~~~~~~~~~~                    ",
            ],
            # Frame 2 - Dance pose up
            [
                "           ✦  ★  ✦                    ",
                "              \\|/                     ",
                "           __(^ ^)__                  ",
                "          /  (  >)  \\                 ",
                "         |  __\\/__   |                ",
                "        / \\ \\____/ \\   ♫             ",
                "       <|  \\_____/                   ",
                "             |   |                    ",
                "            /     \\                   ",
                "          (•)     (•)                 ",
                "         ~~~~~~~~~~~                  ",
            ],
            # Frame 3 - Look right
            [
                "              ★  ✦  ★                 ",
                "                 \\|/                  ",
                "              __(O O)__               ",
                "             /  ( o )  \\              ",
                "            |  __\\/__   |  ♪         ",
                "             \\ \\____/ /              ",
                "              \\_____/|>              ",
                "                |   |                 ",
                "               _|   |_                ",
                "              (•)   (•)               ",
                "             ~~~~~~~~~~~              ",
            ],
            # Frame 4 - Arms up!
            [
                "         \\\\  ★ ✦ ★  //               ",
                "          \\\\  \\|/  //                ",
                "           __(O O)__     QUACK!       ",
                "          /  ( ◡ )  \\                 ",
                "       \\\\|  __\\/__   |//             ",
                "        \\\\  \\____/  //    ♫ ♪       ",
                "          \\_____/|>                  ",
                "            |   |                     ",
                "           _|   |_                    ",
                "          (•)   (•)                   ",
                "         ~~~~~~~~~~~                  ",
            ],
            # Frame 5 - Lean left
            [
                "      ♪  ★  ✦                         ",
                "         \\|                           ",
                "       __(~ ~)__                      ",
                "      /  (  >)  \\                     ",
                "     |  __\\/__   \\                    ",
                "      \\ \\____/  /                     ",
                "       \\_____/|>                     ",
                "         |   |                        ",
                "        /     \\_                      ",
                "      (•)    (•)                      ",
                "     ~~~~~~~~~~~                      ",
            ],
            # Frame 6 - Lean right
            [
                "                  ✦  ★  ♫             ",
                "                   |/                 ",
                "              __(~ ~)__               ",
                "             /  (  >)  \\              ",
                "            /   __\\/__  |             ",
                "             \\  \\____/ /              ",
                "              \\_____/|>              ",
                "                |   |                 ",
                "              _/     \\                ",
                "             (•)    (•)               ",
                "            ~~~~~~~~~~~               ",
            ],
            # Frame 7 - Spin!
            [
                "           ✧ SPIN ✧                   ",
                "              ★                       ",
                "           __(@ @)__                  ",
                "          /  (  >)  \\                 ",
                "         |  __\\/__   |  ♫            ",
                "          \\ \\____/ /                 ",
                "           \\_____/>                  ",
                "             \\   |                    ",
                "              \\  |_                   ",
                "              (•)(•)                  ",
                "            ~~~~~~~~~~                ",
            ],
            # Frame 8 - Point!
            [
                "             ★  ✦  ★                  ",
                "           ♫  \\|/  ♪                 ",
                "           __(^ ^)__                  ",
                "          /  (  ᴗ)  \\=====>>         ",
                "         |  __\\/__   |                ",
                "          \\ \\____/ /                 ",
                "           \\_____/|>                 ",
                "             |   |                    ",
                "            _|   |_                   ",
                "           (•)   (•)                  ",
                "          ~~~~~~~~~~~                 ",
            ],
            # Frame 9 - Happy blink
            [
                "                                      ",
                "            *  .  *                   ",
                "               __                     ",
                "            __(-.-)>                  ",
                "           /  (   )                   ",
                "          |   \\  /                    ",
                "           \\___\\/|>                   ",
                "             |  |                     ",
                "            _|  |_                    ",
                "           (•)  (•)                   ",
                "          ~~~~~~~~~~                  ",
            ],
            # Frame 10 - Look at you!
            [
                "                                      ",
                "            ★  .  ★                   ",
                "               __                     ",
                "            __(o_o)>    Hi there!     ",
                "           /  (   )                   ",
                "          |   \\  /                    ",
                "           \\___\\/|>                   ",
                "             |  |                     ",
                "            _|  |_                    ",
                "           (•)  (•)                   ",
                "          ~~~~~~~~~~                  ",
            ],
        ]

        frame_idx = (self._title_frame // 10) % len(duck_frames)
        duck_art = duck_frames[frame_idx]

        # Sparkle effects that rotate
        sparkle_chars = ["✦", "✧", "★", "☆", "◆", "◇", "●", "○"]
        sparkle1 = sparkle_chars[self._title_frame % len(sparkle_chars)]
        sparkle2 = sparkle_chars[(self._title_frame + 4) % len(sparkle_chars)]

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

        # Add the dancing duck
        for line in duck_art:
            padded_line = line + " " * (54 - len(line)) if len(line) < 54 else line[:54]
            title_art.append(f"    ║{padded_line}║    ")

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

        print(self.term.home + self.term.clear)
        for line in title_art:
            print(self.term.center(line))

    def _overlay_help(self, base_output: List[str], width: int) -> List[str]:
        """Overlay the help screen."""
        help_text = [
            "CONTROLS",
            "--------",
            "[F] / [1] - Feed duck      [T] - Talk to duck",
            "[P] / [2] - Play with duck [I] - Open inventory",
            "[C] / [3] - Clean duck     [G] - View goals",
            "[E] / [4] - Pet duck       [S] - View statistics",
            "[Z] / [5] - Let duck sleep [B] - Open shop",
            "",
            "AUDIO",
            "[M] - Toggle sound on/off",
            "[N] - Toggle music on/off",
            "[+] - Volume up  [-] - Volume down",
            "",
            "GAME",
            "[R] - Return to title  [Q] - Save and quit",
            "[X] - Reset game (start over)",
            "",
            "The duck will wander around on its own!",
            "Keep its needs up to keep it happy.",
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
            f"╔══════════════ LIFETIME ══════════════╗",
            f"  Days Played: {prog.days_played}",
            f"  Total Care: {total_care_actions} actions",
            f"    🍞 Fed: {total_stats.get('total_feeds', 0)}",
            f"    🎮 Played: {total_stats.get('total_plays', 0)}",
            f"    🧼 Cleaned: {total_stats.get('total_cleans', 0)}",
            f"    💕 Petted: {total_stats.get('total_pets', 0)}",
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
            # Use ANSI-aware padding and truncation for colored content
            padded = _visible_ljust(f" {line} ", box_width)
            padded = _visible_truncate(padded, box_width)
            box_lines.append(BOX_DOUBLE["v"] + padded + BOX_DOUBLE["v"])

        box_lines.append(BOX_DOUBLE["bl"] + BOX_DOUBLE["h"] * box_width + BOX_DOUBLE["br"])

        # Overlay on base output
        result = base_output.copy()
        start_row = 4
        start_col = (width - box_width - 2) // 2

        for i, line in enumerate(box_lines):
            if start_row + i < len(result):
                row = result[start_row + i]
                # Use ANSI-aware slicing for rows that may contain colored text
                box_visible_width = _visible_len(line)
                left_part = _visible_slice(row, 0, start_col)
                left_part = _visible_ljust(left_part, start_col)  # Ensure proper width
                right_part = _visible_slice(row, start_col + box_visible_width, width)
                new_row = left_part + line + right_part
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
            # Use ANSI-aware centering and truncation for colored art
            centered = _visible_center(line, box_width)
            centered = _visible_truncate(centered, box_width)
            box_lines.append(centered)

        # Overlay on base output
        result = base_output.copy()
        start_row = max(2, (len(result) - box_height) // 2 - 2)
        start_col = (width - box_width) // 2

        for i, line in enumerate(box_lines):
            if start_row + i < len(result):
                row = result[start_row + i]
                # Use ANSI-aware slicing for rows that may contain colored text
                box_visible_width = _visible_len(line)
                left_part = _visible_slice(row, 0, start_col)
                left_part = _visible_ljust(left_part, start_col)
                right_part = _visible_slice(row, start_col + box_visible_width, width)
                new_row = left_part + line + right_part
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
        """Show a message to the player (default 5 seconds)."""
        self._message_queue.append(message)
        if len(self._message_queue) > 5:
            self._message_queue.pop(0)
        self._message_expire = time.time() + duration

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

        lines = [
            "",
            "  " + BOX_DOUBLE["tl"] + BOX_DOUBLE["h"] * 44 + BOX_DOUBLE["tr"],
            "  " + BOX_DOUBLE["v"] + " " * 44 + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + f"  Welcome back!                            " + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + f"  {duck_name} missed you!                  "[:44] + " " + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + " " * 44 + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + f"  You were away for {time_str}            "[:44] + " " + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + " " * 44 + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + "  While you were gone:                      " + BOX_DOUBLE["v"],
        ]

        for need, change in changes.items():
            if change != 0:
                direction = "decreased" if change < 0 else "recovered"
                line = f"   - {need}: {direction}"
                lines.append("  " + BOX_DOUBLE["v"] + f"  {line}                        "[:44] + BOX_DOUBLE["v"])

        lines.extend([
            "  " + BOX_DOUBLE["v"] + " " * 44 + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + "  Press any key to continue...              " + BOX_DOUBLE["v"],
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
