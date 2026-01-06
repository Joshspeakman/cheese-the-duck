"""
Settings Menu UI - Renders and handles the settings menu.

Provides interface for all game settings with live preview where possible.
"""
from typing import Optional, List, Callable, Any, Tuple
from dataclasses import dataclass
from enum import Enum

from core.settings import (
    GameSettings, SettingsManager, settings_manager,
    AudioSettings, DisplaySettings, AccessibilitySettings, 
    GameplaySettings, KeyBindings
)
from core.menu_controller import MenuController, MenuConfig, MenuResult, MenuAction


class SettingsCategory(Enum):
    """Settings menu categories."""
    AUDIO = "audio"
    DISPLAY = "display"
    ACCESSIBILITY = "accessibility"
    GAMEPLAY = "gameplay"
    KEYBINDINGS = "keybindings"


@dataclass
class SettingItem:
    """A single setting item for display."""
    id: str
    label: str
    category: str
    value_type: str  # "toggle", "slider", "choice", "key"
    current_value: Any
    choices: Optional[List[Tuple[str, Any]]] = None  # For choice type: (display, value)
    min_value: float = 0.0  # For slider type
    max_value: float = 1.0  # For slider type
    step: float = 0.1       # For slider type
    description: str = ""
    enabled: bool = True


class SettingsMenu:
    """
    Settings menu with categories and editable options.
    
    Usage:
        menu = SettingsMenu(renderer)
        menu.open()
        
        # In input handler:
        if menu.is_open:
            result = menu.handle_input(key)
    """
    
    def __init__(self, show_message_callback: Callable[[str, float], None] = None):
        self._show_message = show_message_callback
        self._is_open = False
        self._current_category: SettingsCategory = SettingsCategory.AUDIO
        self._category_index = 0
        self._setting_index = 0
        self._editing_value = False  # True when adjusting a slider/choice
        self._editing_key = False    # True when capturing key binding
        self._pending_key_action = None  # Action waiting for new key
        
        # Category menu
        self._categories = list(SettingsCategory)
        
        # Current settings items
        self._items: List[SettingItem] = []
        
        # Sound engine reference for live preview
        self._sound_engine = None
    
    def set_sound_engine(self, sound_engine):
        """Set sound engine reference for live volume preview."""
        self._sound_engine = sound_engine
    
    @property
    def is_open(self) -> bool:
        return self._is_open
    
    def open(self):
        """Open the settings menu."""
        self._is_open = True
        self._category_index = 0
        self._setting_index = 0
        self._current_category = self._categories[0]
        self._editing_value = False
        self._editing_key = False
        self._load_category_items()
    
    def close(self):
        """Close the settings menu and save."""
        self._is_open = False
        self._editing_value = False
        self._editing_key = False
        settings_manager.save()
    
    def reset_selection(self):
        """Reset the menu selection to the beginning."""
        self._category_index = 0
        self._setting_index = 0
        self._current_category = self._categories[0]
        self._editing_value = False
        self._editing_key = False
        self._load_category_items()
    
    def discard_changes(self):
        """Discard any unsaved changes and reload settings."""
        settings_manager.load()  # Reload from file
        self._load_category_items()  # Refresh displayed items

    def _load_category_items(self):
        """Load setting items for current category."""
        settings = settings_manager.settings
        self._items = []
        
        if self._current_category == SettingsCategory.AUDIO:
            self._items = [
                SettingItem("master_volume", "Master Volume", "audio", "slider",
                           settings.audio.master_volume, min_value=0, max_value=1, step=0.1,
                           description="Overall game volume"),
                SettingItem("music_volume", "Music Volume", "audio", "slider",
                           settings.audio.music_volume, min_value=0, max_value=1, step=0.1,
                           description="Background music volume"),
                SettingItem("sfx_volume", "Sound Effects", "audio", "slider",
                           settings.audio.sfx_volume, min_value=0, max_value=1, step=0.1,
                           description="Sound effects volume"),
                SettingItem("ambient_volume", "Ambient Sounds", "audio", "slider",
                           settings.audio.ambient_volume, min_value=0, max_value=1, step=0.1,
                           description="Environmental ambient sounds"),
                SettingItem("music_enabled", "Music", "audio", "toggle",
                           settings.audio.music_enabled,
                           description="Enable/disable background music"),
                SettingItem("sfx_enabled", "Sound Effects", "audio", "toggle",
                           settings.audio.sfx_enabled,
                           description="Enable/disable sound effects"),
                SettingItem("duck_quacks_enabled", "Duck Quacks", "audio", "toggle",
                           settings.audio.duck_quacks_enabled,
                           description="Enable/disable duck quacking sounds"),
            ]
        
        elif self._current_category == SettingsCategory.DISPLAY:
            self._items = [
                SettingItem("text_speed", "Text Speed", "display", "choice",
                           settings.display.text_speed,
                           choices=[("Slow", "slow"), ("Normal", "normal"), 
                                   ("Fast", "fast"), ("Instant", "instant")],
                           description="Speed of text display"),
                SettingItem("show_particles", "Weather Particles", "display", "toggle",
                           settings.display.show_particles,
                           description="Show rain, snow, and other particles"),
                SettingItem("show_animations", "Animations", "display", "toggle",
                           settings.display.show_animations,
                           description="Show duck and item animations"),
                SettingItem("show_weather_effects", "Weather Effects", "display", "toggle",
                           settings.display.show_weather_effects,
                           description="Show weather visual effects"),
                SettingItem("show_clock", "Show Clock", "display", "toggle",
                           settings.display.show_clock,
                           description="Display time in header"),
                SettingItem("show_mood_bar", "Mood Bar", "display", "toggle",
                           settings.display.show_mood_bar,
                           description="Show mood indicator bar"),
                SettingItem("compact_ui", "Compact UI", "display", "toggle",
                           settings.display.compact_ui,
                           description="Reduced spacing for small terminals"),
            ]
        
        elif self._current_category == SettingsCategory.ACCESSIBILITY:
            self._items = [
                SettingItem("reduced_motion", "Reduced Motion", "accessibility", "toggle",
                           settings.accessibility.reduced_motion,
                           description="Disable animations for accessibility"),
                SettingItem("high_contrast", "High Contrast", "accessibility", "toggle",
                           settings.accessibility.high_contrast,
                           description="Use high contrast colors"),
                SettingItem("colorblind_mode", "Colorblind Mode", "accessibility", "choice",
                           settings.accessibility.colorblind_mode,
                           choices=[("None", "none"), 
                                   ("Deuteranopia", "deuteranopia"),
                                   ("Protanopia", "protanopia"),
                                   ("Tritanopia", "tritanopia")],
                           description="Color adjustments for color vision"),
                SettingItem("flash_warnings", "Flash Warnings", "accessibility", "toggle",
                           settings.accessibility.flash_warnings,
                           description="Warn before bright flashing effects"),
                SettingItem("screen_reader_hints", "Screen Reader", "accessibility", "toggle",
                           settings.accessibility.screen_reader_hints,
                           description="Add extra descriptions for screen readers"),
            ]
        
        elif self._current_category == SettingsCategory.GAMEPLAY:
            self._items = [
                SettingItem("difficulty", "Difficulty", "gameplay", "choice",
                           settings.gameplay.difficulty,
                           choices=[("Relaxed", "relaxed"), 
                                   ("Normal", "normal"),
                                   ("Challenging", "challenging")],
                           description="Affects need decay speed"),
                SettingItem("auto_save_interval", "Auto-Save", "gameplay", "choice",
                           settings.gameplay.auto_save_interval,
                           choices=[("Off", 0), ("30 sec", 30), 
                                   ("1 min", 60), ("2 min", 120), ("5 min", 300)],
                           description="Automatic save frequency"),
                SettingItem("auto_feed_warning", "Low Need Warnings", "gameplay", "toggle",
                           settings.gameplay.auto_feed_warning,
                           description="Warn when needs are critical"),
                SettingItem("confirm_expensive_purchases", "Confirm Purchases", "gameplay", "toggle",
                           settings.gameplay.confirm_expensive_purchases,
                           description="Confirm expensive purchases"),
                SettingItem("expensive_threshold", "Confirm Threshold", "gameplay", "choice",
                           settings.gameplay.expensive_threshold,
                           choices=[("100", 100), ("250", 250), 
                                   ("500", 500), ("1000", 1000)],
                           description="Coin amount that triggers confirmation"),
                SettingItem("confirm_rare_item_use", "Confirm Rare Items", "gameplay", "toggle",
                           settings.gameplay.confirm_rare_item_use,
                           description="Confirm using rare items"),
                SettingItem("show_tips", "Show Tips", "gameplay", "toggle",
                           settings.gameplay.show_tips,
                           description="Display contextual hints"),
            ]
        
        elif self._current_category == SettingsCategory.KEYBINDINGS:
            kb = settings.keybindings
            self._items = [
                SettingItem("feed", "Feed", "keybindings", "key", kb.feed),
                SettingItem("play", "Play", "keybindings", "key", kb.play),
                SettingItem("clean", "Clean", "keybindings", "key", kb.clean),
                SettingItem("pet", "Pet", "keybindings", "key", kb.pet),
                SettingItem("sleep", "Sleep", "keybindings", "key", kb.sleep),
                SettingItem("talk", "Talk", "keybindings", "key", kb.talk),
                SettingItem("shop", "Shop", "keybindings", "key", kb.shop),
                SettingItem("inventory", "Inventory", "keybindings", "key", kb.inventory),
                SettingItem("stats", "Stats", "keybindings", "key", kb.stats),
                SettingItem("help", "Help", "keybindings", "key", kb.help),
            ]
        
        self._setting_index = 0
    
    def handle_input(self, key) -> MenuResult:
        """Handle input for the settings menu."""
        if not self._is_open:
            return MenuResult.NONE
        
        key_str = str(key).lower() if not getattr(key, 'is_sequence', False) else ""
        key_name = getattr(key, 'name', "") or ""
        
        # Key binding capture mode
        if self._editing_key:
            return self._handle_key_capture(key, key_str, key_name)
        
        # Value editing mode (slider/choice)
        if self._editing_value:
            return self._handle_value_edit(key, key_str, key_name)
        
        # Close menu
        if key_name == "KEY_ESCAPE":
            self.close()
            return MenuResult.CANCELLED
        
        # Category navigation (left/right)
        if key_name == "KEY_LEFT":
            self._category_index = (self._category_index - 1) % len(self._categories)
            self._current_category = self._categories[self._category_index]
            self._load_category_items()
            return MenuResult.NAVIGATED
        
        if key_name == "KEY_RIGHT":
            self._category_index = (self._category_index + 1) % len(self._categories)
            self._current_category = self._categories[self._category_index]
            self._load_category_items()
            return MenuResult.NAVIGATED
        
        # Setting navigation (up/down)
        if key_name == "KEY_UP":
            if self._items:
                self._setting_index = (self._setting_index - 1) % len(self._items)
            return MenuResult.NAVIGATED
        
        if key_name == "KEY_DOWN":
            if self._items:
                self._setting_index = (self._setting_index + 1) % len(self._items)
            return MenuResult.NAVIGATED
        
        # Edit/toggle selected setting (Enter or Space)
        if key_name == "KEY_ENTER" or key_str == " ":
            return self._start_edit()
        
        # Quick adjust for sliders ([ and ])
        if key_str == "[" or key_str == "]":
            item = self._get_current_item()
            if item and item.value_type == "slider":
                direction = -1 if key_str == "[" else 1
                self._adjust_slider(item, direction)
                return MenuResult.SELECTED
        
        return MenuResult.NONE
    
    def _start_edit(self) -> MenuResult:
        """Start editing the current setting."""
        item = self._get_current_item()
        if not item or not item.enabled:
            return MenuResult.NONE
        
        if item.value_type == "toggle":
            # Toggle immediately
            new_value = not item.current_value
            self._apply_setting(item.category, item.id, new_value)
            item.current_value = new_value
            return MenuResult.SELECTED
        
        elif item.value_type == "slider":
            self._editing_value = True
            return MenuResult.SELECTED
        
        elif item.value_type == "choice":
            self._editing_value = True
            return MenuResult.SELECTED
        
        elif item.value_type == "key":
            self._editing_key = True
            self._pending_key_action = item.id
            return MenuResult.SELECTED
        
        return MenuResult.NONE
    
    def _handle_value_edit(self, key, key_str: str, key_name: str) -> MenuResult:
        """Handle input while editing a value."""
        item = self._get_current_item()
        if not item:
            self._editing_value = False
            return MenuResult.NONE
        
        # Confirm with Enter
        if key_name == "KEY_ENTER":
            self._editing_value = False
            return MenuResult.SELECTED
        
        # Cancel with Escape
        if key_name == "KEY_ESCAPE":
            self._editing_value = False
            self._load_category_items()  # Reload to reset
            return MenuResult.CANCELLED
        
        if item.value_type == "slider":
            if key_name == "KEY_LEFT" or key_str == "[":
                self._adjust_slider(item, -1)
                return MenuResult.NAVIGATED
            elif key_name == "KEY_RIGHT" or key_str == "]":
                self._adjust_slider(item, 1)
                return MenuResult.NAVIGATED
        
        elif item.value_type == "choice":
            if key_name == "KEY_LEFT" or key_name == "KEY_UP":
                self._cycle_choice(item, -1)
                return MenuResult.NAVIGATED
            elif key_name == "KEY_RIGHT" or key_name == "KEY_DOWN":
                self._cycle_choice(item, 1)
                return MenuResult.NAVIGATED
        
        return MenuResult.NONE
    
    def _handle_key_capture(self, key, key_str: str, key_name: str) -> MenuResult:
        """Handle key binding capture."""
        # Cancel with Escape
        if key_name == "KEY_ESCAPE":
            self._editing_key = False
            self._pending_key_action = None
            return MenuResult.CANCELLED
        
        # Capture the key
        new_key = key_name if key_name else key_str
        if new_key and self._pending_key_action:
            self._apply_setting("keybindings", self._pending_key_action, new_key)
            self._editing_key = False
            self._pending_key_action = None
            self._load_category_items()  # Reload to show new key
            return MenuResult.SELECTED
        
        return MenuResult.NONE
    
    def _adjust_slider(self, item: SettingItem, direction: int):
        """Adjust a slider value."""
        new_value = item.current_value + (item.step * direction)
        new_value = max(item.min_value, min(item.max_value, new_value))
        new_value = round(new_value, 2)  # Avoid float precision issues
        
        item.current_value = new_value
        self._apply_setting(item.category, item.id, new_value)
        
        # Live preview for volume settings
        if self._sound_engine and "volume" in item.id:
            self._preview_volume(item.id, new_value)
    
    def _cycle_choice(self, item: SettingItem, direction: int):
        """Cycle through choice options."""
        if not item.choices:
            return
        
        current_idx = 0
        for i, (_, value) in enumerate(item.choices):
            if value == item.current_value:
                current_idx = i
                break
        
        new_idx = (current_idx + direction) % len(item.choices)
        new_value = item.choices[new_idx][1]
        
        item.current_value = new_value
        self._apply_setting(item.category, item.id, new_value)
    
    def _apply_setting(self, category: str, key: str, value: Any):
        """Apply a setting change."""
        settings_manager.set_value(category, key, value)
    
    def _preview_volume(self, setting_id: str, value: float):
        """Preview volume change with a test sound."""
        if not self._sound_engine:
            return
        
        try:
            if setting_id == "master_volume":
                self._sound_engine.set_master_volume(value)
            elif setting_id == "music_volume":
                self._sound_engine.set_music_volume(value)
            elif setting_id == "sfx_volume":
                self._sound_engine.set_sfx_volume(value)
        except Exception:
            pass  # Sound engine might not support these methods
    
    def _get_current_item(self) -> Optional[SettingItem]:
        """Get the currently selected item."""
        if 0 <= self._setting_index < len(self._items):
            return self._items[self._setting_index]
        return None
    
    def get_display_lines(self, width: int = 60) -> List[str]:
        """Generate display lines for the settings menu."""
        lines = []
        
        # Title
        lines.append("╔" + "═" * (width - 2) + "╗")
        title = "SETTINGS"
        padding = (width - 2 - len(title)) // 2
        lines.append("║" + " " * padding + title + " " * (width - 2 - padding - len(title)) + "║")
        lines.append("╠" + "═" * (width - 2) + "╣")
        
        # Category tabs
        tab_line = "║ "
        for i, cat in enumerate(self._categories):
            name = cat.value.upper()
            if i == self._category_index:
                tab_line += f"[{name}] "
            else:
                tab_line += f" {name}  "
        tab_line = tab_line.ljust(width - 1) + "║"
        lines.append(tab_line)
        lines.append("║" + "─" * (width - 2) + "║")
        
        # Settings list
        for i, item in enumerate(self._items):
            is_selected = i == self._setting_index
            prefix = "→ " if is_selected else "  "
            
            # Format value display
            value_str = self._format_value(item)
            
            # Build line
            label = item.label
            if len(label) > 20:
                label = label[:17] + "..."
            
            line = f"{prefix}{label:<20} {value_str}"
            
            # Highlight if editing
            if is_selected and (self._editing_value or self._editing_key):
                line = f"{prefix}{label:<20} [{value_str}]"
            
            # Pad and border
            line = "║ " + line.ljust(width - 4) + " ║"
            lines.append(line)
        
        # Description of selected item
        item = self._get_current_item()
        if item and item.description:
            lines.append("║" + "─" * (width - 2) + "║")
            desc = item.description[:width - 6]
            lines.append("║ " + desc.ljust(width - 4) + " ║")
        
        # Controls hint
        lines.append("╠" + "═" * (width - 2) + "╣")
        if self._editing_key:
            hint = "Press any key to bind, ESC to cancel"
        elif self._editing_value:
            hint = "←/→ to adjust, ENTER to confirm"
        else:
            hint = "←/→ Category  ↑/↓ Navigate  ENTER Edit  ESC Close"
        hint_padding = (width - 2 - len(hint)) // 2
        lines.append("║" + " " * hint_padding + hint + " " * (width - 2 - hint_padding - len(hint)) + "║")
        lines.append("╚" + "═" * (width - 2) + "╝")
        
        return lines
    
    def _format_value(self, item: SettingItem) -> str:
        """Format a setting value for display."""
        if item.value_type == "toggle":
            return "ON" if item.current_value else "OFF"
        
        elif item.value_type == "slider":
            # Show as bar: [████░░░░░░] 40%
            percent = int((item.current_value - item.min_value) / 
                         (item.max_value - item.min_value) * 100)
            filled = percent // 10
            bar = "█" * filled + "░" * (10 - filled)
            return f"[{bar}] {percent}%"
        
        elif item.value_type == "choice":
            if item.choices:
                for display, value in item.choices:
                    if value == item.current_value:
                        return display
            return str(item.current_value)
        
        elif item.value_type == "key":
            key = item.current_value
            if key.startswith("KEY_"):
                return key[4:]  # Remove KEY_ prefix
            return key.upper()
        
        return str(item.current_value)

    def has_unsaved_changes(self) -> bool:
        """Check if there are unsaved changes."""
        # For now, assume changes are applied immediately
        # Could track dirty state if needed
        return False
    
    def navigate_category(self, direction: int):
        """Navigate between categories (left/right)."""
        self._category_index = (self._category_index + direction) % len(self._categories)
        self._current_category = self._categories[self._category_index]
        self._setting_index = 0
        self._editing_value = False
        self._load_category_items()
    
    def navigate_item(self, direction: int):
        """Navigate between items (up/down)."""
        if not self._items:
            return
        self._setting_index = (self._setting_index + direction) % len(self._items)
    
    def adjust_value(self, direction: int):
        """Adjust the current setting value (left/right while editing)."""
        if not self._items or self._setting_index >= len(self._items):
            return
        
        item = self._items[self._setting_index]
        
        if item.value_type == "slider":
            self._adjust_slider(item, direction)
        elif item.value_type == "choice":
            self._cycle_choice(item, direction)
        elif item.value_type == "toggle":
            # Toggle on any adjustment
            item.current_value = not item.current_value
            self._apply_setting(item.category, item.id, item.current_value)
    
    def select_current(self) -> 'MenuResult':
        """Select/activate the current item (Enter key)."""
        return self._start_edit()
    
    def render(self) -> List[str]:
        """Render the settings menu and return display lines."""
        return self.get_display_lines()
    
    def save_changes(self):
        """Save all current settings to file."""
        settings_manager.save()
    
    def reload_from_settings(self):
        """Reload items from current settings."""
        self._load_category_items()


# Global settings menu instance
settings_menu = SettingsMenu()
