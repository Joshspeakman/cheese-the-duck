"""
Terminal UI renderer using blessed library - Enhanced version with side panel layout.
Features a main playfield with moving duck and side panel with close-up, stats, etc.
"""
import time
import math
import random
from typing import Optional, List, Dict, Tuple, TYPE_CHECKING
from blessed import Terminal

from config import COLORS
from ui.ascii_art import get_duck_art, get_emotion_closeup, create_box, BORDER, get_mini_duck, PLAYFIELD_OBJECTS
from ui.input_handler import get_help_text
from ui.animations import animation_controller, EFFECTS
from duck.mood import MoodState

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
        self._state = "idle"  # idle, walking, sleeping, eating, playing
        self._animation_frame = 0

    def update(self, delta_time: float):
        """Update duck position and movement."""
        self._move_timer += delta_time
        self._idle_timer += delta_time

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

    def set_state(self, state: str):
        """Set duck state (idle, sleeping, eating, playing)."""
        self._state = state
        self._animation_frame = 0
        if state == "sleeping":
            # Move to a corner-ish spot to sleep
            self.target_x = random.choice([3, self.field_width - 10])
            self.target_y = self.field_height - 4

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

        # Duck position tracking
        self.duck_pos = DuckPosition(field_width=44, field_height=14)

        # Playfield decorations (static objects)
        self._playfield_objects: List[Tuple[int, int, str]] = []
        self._generate_playfield_decorations()

        # Inventory items list for key selection
        self._inventory_items: List[str] = []

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

        # Header spanning full width
        output.extend(self._render_header_bar(duck, width))

        # Main area: playfield on left, side panel on right
        playfield_lines = self._render_playfield(duck, playfield_width, field_height)
        sidepanel_lines = self._render_side_panel(duck, game, side_panel_width)

        # Combine playfield and side panel
        max_lines = max(len(playfield_lines), len(sidepanel_lines))
        for i in range(max_lines):
            pf_line = playfield_lines[i] if i < len(playfield_lines) else " " * playfield_width
            sp_line = sidepanel_lines[i] if i < len(sidepanel_lines) else " " * side_panel_width
            # Pad lines to exact width
            pf_line = pf_line.ljust(playfield_width)[:playfield_width]
            sp_line = sp_line.ljust(side_panel_width)[:side_panel_width]
            output.append(pf_line + sp_line)

        # Message area
        output.extend(self._render_messages(width))

        # Controls bar
        output.extend(self._render_controls_bar(width))

        # Check for expired closeup
        self._check_closeup_expired()

        # Overlays (help, stats, inventory)
        if self._show_help:
            output = self._overlay_help(output, width)
        elif self._show_stats:
            output = self._overlay_stats(output, duck, game, width)
        elif self._show_talk:
            output = self._overlay_talk(output, width)
        elif self._show_inventory:
            output = self._overlay_inventory(output, game, width)

        # Print frame - fill terminal (no clear to prevent flashing)
        print(self.term.home, end="")
        for i, line in enumerate(output):
            if i < height - 1:  # Leave one line at bottom
                # Use move to ensure proper positioning and overwrite
                print(self.term.move(i, 0) + line[:width].ljust(width), end="")

    def _render_header_bar(self, duck: "Duck", width: int) -> List[str]:
        """Render the top header bar."""
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

        # Build header
        name_part = f" {duck.name} the {duck.get_growth_stage_display()} "
        mood_part = f" {mood_ind} {mood.description.title()} "
        age_part = f" Age: {age_str} "

        # Create bordered header
        inner_width = width - 2
        header_content = f"{name_part}{' ' * (inner_width - len(name_part) - len(mood_part) - len(age_part))}{mood_part}{age_part}"

        lines = [
            BOX_DOUBLE["tl"] + BOX_DOUBLE["h"] * inner_width + BOX_DOUBLE["tr"],
            BOX_DOUBLE["v"] + header_content[:inner_width].ljust(inner_width) + BOX_DOUBLE["v"],
            BOX_DOUBLE["bl"] + BOX_DOUBLE["h"] * inner_width + BOX_DOUBLE["br"],
        ]
        return lines

    def _render_playfield(self, duck: "Duck", width: int, height: int = None) -> List[str]:
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
        duck_height = len(duck_art)
        duck_width = max(len(line) for line in duck_art) if duck_art else 0

        # Build each row of the playfield
        for y in range(field_height):
            row = list(self._ground_pattern[y][:inner_width])

            # Add decorations
            for obj_x, obj_y, obj_type in self._playfield_objects:
                if obj_y == y and 0 <= obj_x < inner_width:
                    obj_chars = PLAYFIELD_OBJECTS.get(obj_type, "*")
                    for i, char in enumerate(obj_chars):
                        if obj_x + i < inner_width:
                            row[obj_x + i] = char

            # Add duck if on this row
            duck_y = self.duck_pos.y
            duck_x = self.duck_pos.x

            for dy, duck_line in enumerate(duck_art):
                if y == duck_y + dy:
                    for dx, char in enumerate(duck_line):
                        if char != ' ' and 0 <= duck_x + dx < inner_width:
                            row[duck_x + dx] = char

            row_str = "".join(row)
            lines.append(BOX["v"] + row_str.ljust(inner_width)[:inner_width] + BOX["v"])

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
        controls2 = " [T]alk [S]tats [I]nv [G]oals [H]elp [Q]uit "

        lines = [
            BOX["tl"] + BOX["h"] * inner_width + BOX["tr"],
            BOX["v"] + controls1.center(inner_width)[:inner_width] + BOX["v"],
            BOX["v"] + controls2.center(inner_width)[:inner_width] + BOX["v"],
            BOX["bl"] + BOX["h"] * inner_width + BOX["br"],
        ]
        return lines

    def _render_title_screen(self):
        """Render the title/new game screen with animation."""
        self._title_frame = (self._title_frame + 1) % 60

        # Animated duck with more frames
        duck_frames = [
            [
                "        __        ",
                "      >(o )___    ",
                "       ( ._> /    ",
                "        `---'     ",
            ],
            [
                "        __        ",
                "      >(o )___    ",
                "       ( ._> /    ",
                "       /`---'     ",
            ],
            [
                "        __        ",
                "      >(- )___    ",
                "       ( ._> /    ",
                "        `---'\\    ",
            ],
            [
                "        __        ",
                "      >(o )___    ",
                "       ( ._> /    ",
                "        `---'     ",
            ],
        ]

        frame_idx = (self._title_frame // 15) % len(duck_frames)
        duck_art = duck_frames[frame_idx]

        # Build title screen with more flair
        title = [
            "",
            "  " + BOX_DOUBLE["tl"] + BOX_DOUBLE["h"] * 44 + BOX_DOUBLE["tr"],
            "  " + BOX_DOUBLE["v"] + " " * 44 + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + "    ____ _                            " + "     " + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + "   / ___| |__   ___  ___  ___  ___    " + "     " + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + "  | |   | '_ \\ / _ \\/ _ \\/ __|/ _ \\   " + "     " + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + "  | |___| | | |  __/  __/\\__ \\  __/   " + "     " + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + "   \\____|_| |_|\\___|\\___|_|___/\\___|   " + "     " + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + "                                      " + "     " + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + "           THE DUCK                   " + "     " + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + " " * 44 + BOX_DOUBLE["v"],
        ]

        for line in duck_art:
            title.append("  " + BOX_DOUBLE["v"] + "       " + line + " " * (44 - 7 - len(line)) + BOX_DOUBLE["v"])

        # Add some flair based on animation frame
        flair = ["~", "*", ".", " "][self._title_frame % 4]

        title.extend([
            "  " + BOX_DOUBLE["v"] + " " * 44 + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + f"   {flair} A Virtual Pet Simulation {flair}            " + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + "   with a very cheesy duck named Cheese   " + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + " " * 44 + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + "     Press [ENTER] to start a new game    " + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + "     Press [Q] to quit                    " + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["v"] + " " * 44 + BOX_DOUBLE["v"],
            "  " + BOX_DOUBLE["bl"] + BOX_DOUBLE["h"] * 44 + BOX_DOUBLE["br"],
            "",
        ])

        print(self.term.home + self.term.clear)
        print("\n".join(title))

    def _overlay_help(self, base_output: List[str], width: int) -> List[str]:
        """Overlay the help screen."""
        help_text = [
            "CONTROLS",
            "--------",
            "[F] / [1] - Feed duck      [T] - Talk to duck",
            "[P] / [2] - Play with duck [I] - Open inventory",
            "[C] / [3] - Clean duck     [G] - View goals",
            "[E] / [4] - Pet duck       [S] - View statistics",
            "[Z] / [5] - Let duck sleep [M] - Toggle sound",
            "",
            "[H] - Toggle this help",
            "[Q] - Save and quit",
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

        stats_text = [
            f"Name: {duck.name}",
            f"Stage: {duck.get_growth_stage_display()}",
            "",
            f"Level {prog.level}: {prog.title}",
            f"XP: {xp_bar} {int(xp_pct)}%",
            f"Streak: {prog.current_streak} days (best: {prog.longest_streak})",
            "",
            f"Relationship: {memory.get_relationship_description()}",
            f"Mood: {memory.get_recent_mood_trend()}",
            "",
            f"Collectibles: {coll_owned}/{coll_total}",
            f"Interactions: {memory.total_interactions}",
            "",
            "Press [S] to close",
        ]

        return self._overlay_box(base_output, stats_text, "STATISTICS", width)

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

        # Create box
        box_lines = [
            BOX_DOUBLE["tl"] + BOX_DOUBLE["h"] + f" {title} " + BOX_DOUBLE["h"] * (box_width - len(title) - 4) + BOX_DOUBLE["tr"],
        ]

        for line in content:
            padded = f" {line} ".ljust(box_width)[:box_width]
            box_lines.append(BOX_DOUBLE["v"] + padded + BOX_DOUBLE["v"])

        box_lines.append(BOX_DOUBLE["bl"] + BOX_DOUBLE["h"] * box_width + BOX_DOUBLE["br"])

        # Overlay on base output
        result = base_output.copy()
        start_row = 4
        start_col = (width - box_width - 2) // 2

        for i, line in enumerate(box_lines):
            if start_row + i < len(result):
                row = result[start_row + i]
                # Insert box into row
                new_row = row[:start_col] + line + row[start_col + len(line):]
                result[start_row + i] = new_row[:width]

        return result

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

    def set_duck_state(self, state: str):
        """Set the duck's visual state in the playfield."""
        self.duck_pos.set_state(state)

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

    def hide_overlays(self):
        """Hide all overlays."""
        self._show_help = False
        self._show_stats = False
        self._show_talk = False
        self._show_inventory = False

    def is_talking(self) -> bool:
        """Check if talk mode is active."""
        return self._show_talk

    def is_inventory_open(self) -> bool:
        """Check if inventory is open."""
        return self._show_inventory

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
