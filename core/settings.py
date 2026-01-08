"""
Game Settings System - User-configurable options with persistence.

Handles audio, display, accessibility, gameplay, and keybinding settings.
"""
import json
from pathlib import Path
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass, field, asdict
from enum import Enum

from config import SAVE_DIR


class TextSpeed(Enum):
    """Text display speed options."""
    SLOW = "slow"
    NORMAL = "normal"
    FAST = "fast"
    INSTANT = "instant"


class Difficulty(Enum):
    """Difficulty presets affecting need decay rates."""
    RELAXED = "relaxed"      # 50% decay rate, forgiving
    NORMAL = "normal"        # 100% decay rate, balanced
    CHALLENGING = "challenging"  # 150% decay rate, demanding


class ColorTheme(Enum):
    """Color theme options for accessibility."""
    DEFAULT = "default"
    HIGH_CONTRAST = "high_contrast"
    COLORBLIND_DEUTERANOPIA = "deuteranopia"  # Red-green (most common)
    COLORBLIND_PROTANOPIA = "protanopia"      # Red-green variant
    COLORBLIND_TRITANOPIA = "tritanopia"      # Blue-yellow


@dataclass
class AudioSettings:
    """Audio-related settings."""
    master_volume: float = 0.8          # 0.0 - 1.0
    music_volume: float = 0.7           # 0.0 - 1.0
    sfx_volume: float = 0.8             # 0.0 - 1.0
    ambient_volume: float = 0.5         # 0.0 - 1.0
    music_enabled: bool = True
    sfx_enabled: bool = True
    ambient_enabled: bool = True
    duck_quacks_enabled: bool = True    # Some might find frequent quacks annoying


@dataclass
class DisplaySettings:
    """Display and visual settings."""
    text_speed: str = "normal"          # slow, normal, fast, instant
    show_particles: bool = True         # Weather particles, effects
    show_animations: bool = True        # Duck animations, item bounces
    show_weather_effects: bool = True   # Rain, snow visual effects
    color_theme: str = "default"        # Color theme name
    show_clock: bool = True             # Show time in header
    show_mood_bar: bool = True          # Show mood indicator
    compact_ui: bool = False            # Reduced spacing for small terminals


@dataclass
class AccessibilitySettings:
    """Accessibility options."""
    reduced_motion: bool = False        # Disable/reduce animations
    high_contrast: bool = False         # Use high contrast colors
    screen_reader_hints: bool = False   # Add extra text descriptions
    flash_warnings: bool = True         # Warn before flashing effects
    large_text: bool = False            # Use larger ASCII art where possible
    colorblind_mode: str = "none"       # none, deuteranopia, protanopia, tritanopia


@dataclass  
class GameplaySettings:
    """Gameplay balance settings."""
    difficulty: str = "normal"          # relaxed, normal, challenging
    auto_save_interval: int = 60        # Seconds between auto-saves (0 = disabled)
    auto_feed_warning: bool = True      # Show warnings when needs are critical
    pause_when_unfocused: bool = False  # Pause game when terminal loses focus
    confirm_expensive_purchases: bool = True  # Confirm purchases over threshold
    expensive_threshold: int = 500      # Coins threshold for confirmation
    confirm_rare_item_use: bool = True  # Confirm using rare/legendary items
    show_tips: bool = True              # Show contextual tips
    tutorial_completed: bool = False    # Has player completed tutorial


@dataclass
class KeyBinding:
    """A single key binding."""
    action: str
    key: str
    display_name: str
    category: str = "general"


@dataclass
class SystemSettings:
    """System-level settings."""
    preferred_terminal: str = "auto"    # auto, gnome-terminal, konsole, xterm, etc.
    
    @staticmethod
    def detect_available_terminals() -> list:
        """Detect available terminal emulators on the system."""
        import shutil
        
        terminals = [
            ("auto", "Auto-detect"),
            ("gnome-terminal", "GNOME Terminal"),
            ("konsole", "Konsole (KDE)"),
            ("xfce4-terminal", "XFCE Terminal"),
            ("xterm", "XTerm"),
            ("tilix", "Tilix"),
            ("terminator", "Terminator"),
            ("mate-terminal", "MATE Terminal"),
            ("lxterminal", "LXTerminal"),
            ("alacritty", "Alacritty"),
            ("kitty", "Kitty"),
            ("wezterm", "WezTerm"),
            ("foot", "Foot"),
            ("x-terminal-emulator", "System Default"),
        ]
        
        available = [("auto", "Auto-detect")]  # Always include auto
        for cmd, name in terminals[1:]:  # Skip auto, check rest
            if shutil.which(cmd):
                available.append((cmd, name))
        
        return available


@dataclass
class KeyBindings:
    """All customizable key bindings."""
    # Core interactions
    feed: str = "f"
    play: str = "p"
    clean: str = "c"
    pet: str = "e"
    sleep: str = "z"
    talk: str = "t"
    
    # Menus
    shop: str = "b"
    inventory: str = "i"
    stats: str = "s"
    help: str = "?"
    main_menu: str = "KEY_TAB"
    
    # Activities
    explore: str = "a"
    craft: str = "c"
    build: str = "r"
    fish: str = "4"
    garden: str = "9"
    minigames: str = "j"
    
    # System
    quit: str = "q"
    save: str = "KEY_F5"
    
    def get_all_bindings(self) -> List[KeyBinding]:
        """Get all bindings as a list for display."""
        return [
            KeyBinding("feed", self.feed, "Feed Duck", "interactions"),
            KeyBinding("play", self.play, "Play with Duck", "interactions"),
            KeyBinding("clean", self.clean, "Clean Duck", "interactions"),
            KeyBinding("pet", self.pet, "Pet Duck", "interactions"),
            KeyBinding("sleep", self.sleep, "Put to Sleep", "interactions"),
            KeyBinding("talk", self.talk, "Talk to Duck", "interactions"),
            KeyBinding("shop", self.shop, "Open Shop", "menus"),
            KeyBinding("inventory", self.inventory, "Open Inventory", "menus"),
            KeyBinding("stats", self.stats, "View Stats", "menus"),
            KeyBinding("help", self.help, "Show Help", "menus"),
            KeyBinding("main_menu", self.main_menu, "Main Menu", "menus"),
            KeyBinding("explore", self.explore, "Explore Areas", "activities"),
            KeyBinding("craft", self.craft, "Crafting Menu", "activities"),
            KeyBinding("build", self.build, "Building Menu", "activities"),
            KeyBinding("fish", self.fish, "Go Fishing", "activities"),
            KeyBinding("garden", self.garden, "Garden Menu", "activities"),
            KeyBinding("minigames", self.minigames, "Mini-games", "activities"),
            KeyBinding("quit", self.quit, "Quit Game", "system"),
            KeyBinding("save", self.save, "Quick Save", "system"),
        ]


@dataclass
class GameSettings:
    """
    Complete game settings container.
    
    All user-configurable options in one place with save/load support.
    """
    audio: AudioSettings = field(default_factory=AudioSettings)
    display: DisplaySettings = field(default_factory=DisplaySettings)
    accessibility: AccessibilitySettings = field(default_factory=AccessibilitySettings)
    gameplay: GameplaySettings = field(default_factory=GameplaySettings)
    keybindings: KeyBindings = field(default_factory=KeyBindings)
    system: SystemSettings = field(default_factory=SystemSettings)
    
    # Metadata
    version: str = "1.0"
    first_launch: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize settings to dictionary."""
        return {
            "version": self.version,
            "first_launch": self.first_launch,
            "audio": asdict(self.audio),
            "display": asdict(self.display),
            "accessibility": asdict(self.accessibility),
            "gameplay": asdict(self.gameplay),
            "keybindings": asdict(self.keybindings),
            "system": asdict(self.system),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GameSettings":
        """Deserialize settings from dictionary."""
        settings = cls()
        
        if "audio" in data:
            settings.audio = AudioSettings(**data["audio"])
        if "display" in data:
            settings.display = DisplaySettings(**data["display"])
        if "accessibility" in data:
            settings.accessibility = AccessibilitySettings(**data["accessibility"])
        if "gameplay" in data:
            settings.gameplay = GameplaySettings(**data["gameplay"])
        if "keybindings" in data:
            settings.keybindings = KeyBindings(**data["keybindings"])
        if "system" in data:
            settings.system = SystemSettings(**data["system"])
        
        settings.version = data.get("version", "1.0")
        settings.first_launch = data.get("first_launch", True)
        
        return settings
    
    def get_difficulty_multiplier(self) -> float:
        """Get need decay multiplier based on difficulty."""
        multipliers = {
            "relaxed": 0.5,
            "normal": 1.0,
            "challenging": 1.5,
        }
        return multipliers.get(self.gameplay.difficulty, 1.0)
    
    def get_text_speed_delay(self) -> float:
        """Get delay between characters for text display."""
        delays = {
            "slow": 0.05,
            "normal": 0.02,
            "fast": 0.005,
            "instant": 0.0,
        }
        return delays.get(self.display.text_speed, 0.02)
    
    def should_show_animations(self) -> bool:
        """Check if animations should be shown (respects accessibility)."""
        if self.accessibility.reduced_motion:
            return False
        return self.display.show_animations
    
    def should_show_particles(self) -> bool:
        """Check if particles should be shown (respects accessibility)."""
        if self.accessibility.reduced_motion:
            return False
        return self.display.show_particles


class SettingsManager:
    """
    Manages loading, saving, and applying game settings.
    """
    
    SETTINGS_FILE = SAVE_DIR / "settings.json"
    
    def __init__(self):
        self._settings: GameSettings = GameSettings()
        self._change_callbacks: List[Callable[[str, Any], None]] = []
        self._ensure_save_dir()
    
    def _ensure_save_dir(self):
        """Create save directory if it doesn't exist."""
        SAVE_DIR.mkdir(parents=True, exist_ok=True)
    
    @property
    def settings(self) -> GameSettings:
        """Get current settings."""
        return self._settings
    
    def load(self) -> bool:
        """
        Load settings from file.
        
        Returns:
            True if loaded successfully, False if using defaults
        """
        if not self.SETTINGS_FILE.exists():
            return False
        
        try:
            with open(self.SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._settings = GameSettings.from_dict(data)
            return True
        except (IOError, json.JSONDecodeError, TypeError) as e:
            print(f"Warning: Could not load settings: {e}")
            return False
    
    def save(self) -> bool:
        """
        Save settings to file.
        
        Returns:
            True if saved successfully
        """
        try:
            self._ensure_save_dir()
            
            # Write atomically using temp file
            temp_path = self.SETTINGS_FILE.with_suffix(".tmp")
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(self._settings.to_dict(), f, indent=2)
            
            temp_path.replace(self.SETTINGS_FILE)
            return True
        except (IOError, OSError) as e:
            print(f"Warning: Could not save settings: {e}")
            return False
    
    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        self._settings = GameSettings()
        self._settings.first_launch = False  # Keep this as not first launch
        self._notify_change("all", None)
    
    def reset_category(self, category: str):
        """Reset a specific category to defaults."""
        if category == "audio":
            self._settings.audio = AudioSettings()
        elif category == "display":
            self._settings.display = DisplaySettings()
        elif category == "accessibility":
            self._settings.accessibility = AccessibilitySettings()
        elif category == "gameplay":
            self._settings.gameplay = GameplaySettings()
        elif category == "keybindings":
            self._settings.keybindings = KeyBindings()
        self._notify_change(category, None)
    
    def set_value(self, category: str, key: str, value: Any):
        """Set a specific setting value."""
        target = getattr(self._settings, category, None)
        if target and hasattr(target, key):
            setattr(target, key, value)
            self._notify_change(f"{category}.{key}", value)
    
    def get_value(self, category: str, key: str) -> Any:
        """Get a specific setting value."""
        target = getattr(self._settings, category, None)
        if target:
            return getattr(target, key, None)
        return None
    
    def register_change_callback(self, callback: Callable[[str, Any], None]):
        """Register a callback to be notified of setting changes."""
        self._change_callbacks.append(callback)
    
    def _notify_change(self, key: str, value: Any):
        """Notify all callbacks of a setting change."""
        for callback in self._change_callbacks:
            try:
                callback(key, value)
            except Exception:
                pass  # Don't let callback errors break settings
    
    def mark_tutorial_complete(self):
        """Mark the tutorial as completed."""
        self._settings.gameplay.tutorial_completed = True
        self._settings.first_launch = False
        self.save()
    
    def is_first_launch(self) -> bool:
        """Check if this is the first launch."""
        return self._settings.first_launch
    
    def mark_launched(self):
        """Mark that the game has been launched (no longer first launch)."""
        self._settings.first_launch = False
        self.save()


# Global settings manager instance
settings_manager = SettingsManager()


def get_settings() -> GameSettings:
    """Get the current game settings."""
    return settings_manager.settings


def load_settings() -> bool:
    """Load settings from file."""
    return settings_manager.load()


def save_settings() -> bool:
    """Save settings to file."""
    return settings_manager.save()
