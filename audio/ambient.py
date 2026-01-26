"""
Ambient Sound System - Environmental audio for atmosphere.
Plays background sounds based on weather, time, and location.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum
import threading


class AmbientCategory(Enum):
    """Categories of ambient sounds."""
    WEATHER = "weather"
    TIME_OF_DAY = "time_of_day"
    LOCATION = "location"
    SEASONAL = "seasonal"
    SPECIAL = "special"


class SoundMood(Enum):
    """Mood of the sound."""
    CALM = "calm"
    ENERGETIC = "energetic"
    MYSTERIOUS = "mysterious"
    COZY = "cozy"
    PEACEFUL = "peaceful"
    DRAMATIC = "dramatic"


@dataclass
class AmbientSound:
    """Definition of an ambient sound."""
    id: str
    name: str
    description: str
    category: AmbientCategory
    mood: SoundMood
    triggers: List[str]  # Weather, time, location, etc.
    volume_default: float = 0.5  # 0.0 to 1.0
    loop: bool = True
    ascii_visualization: List[str] = field(default_factory=list)
    text_representation: str = ""  # For text-based "sound"


# Define ambient sounds
AMBIENT_SOUNDS: Dict[str, AmbientSound] = {
    # Weather sounds
    "light_rain": AmbientSound(
        id="light_rain",
        name="Light Rain",
        description="Gentle raindrops pattering softly",
        category=AmbientCategory.WEATHER,
        mood=SoundMood.CALM,
        triggers=["rain", "light_rain", "drizzle"],
        ascii_visualization=[
            "  .  '  .  '  .  ",
            " '  .  '  .  '   ",
            "  .  '  .  '  .  ",
        ],
        text_representation="# pitter... patter... pitter... #"
    ),
    
    "heavy_rain": AmbientSound(
        id="heavy_rain",
        name="Heavy Rain",
        description="Intense rainfall drumming down",
        category=AmbientCategory.WEATHER,
        mood=SoundMood.DRAMATIC,
        triggers=["heavy_rain", "storm", "downpour"],
        ascii_visualization=[
            " |||  |||  |||   ",
            "  |||  |||  |||  ",
            " |||  |||  |||   ",
        ],
        text_representation="# SHHHHHHH... DRUMMMM... #"
    ),
    
    "thunder": AmbientSound(
        id="thunder",
        name="Thunder",
        description="Rolling thunder in the distance",
        category=AmbientCategory.WEATHER,
        mood=SoundMood.DRAMATIC,
        triggers=["thunderstorm", "storm"],
        loop=False,
        ascii_visualization=[
            "    !  BOOM  !   ",
            "  ~~~RUMBLE~~~   ",
        ],
        text_representation="# ...BOOM... rumble rumble... #"
    ),
    
    "wind": AmbientSound(
        id="wind",
        name="Wind",
        description="Breeze rustling through leaves",
        category=AmbientCategory.WEATHER,
        mood=SoundMood.PEACEFUL,
        triggers=["windy", "breezy"],
        ascii_visualization=[
            "  ~~~  ~~~  ~~~  ",
            "    ~~~  ~~~     ",
        ],
        text_representation="# whoooosh... shhhhh... #"
    ),
    
    "snow_falling": AmbientSound(
        id="snow_falling",
        name="Snow Falling",
        description="Soft silence of falling snow",
        category=AmbientCategory.WEATHER,
        mood=SoundMood.PEACEFUL,
        triggers=["snow", "snowy", "blizzard"],
        ascii_visualization=[
            "  *   *   *     ",
            "    *   *   *   ",
            "  *   *   *     ",
        ],
        text_representation="# ... ... (peaceful silence) ... #"
    ),
    
    # Time of day sounds
    "morning_birds": AmbientSound(
        id="morning_birds",
        name="Morning Birdsong",
        description="Birds greeting the new day",
        category=AmbientCategory.TIME_OF_DAY,
        mood=SoundMood.ENERGETIC,
        triggers=["dawn", "morning"],
        ascii_visualization=[
            "  b tweet tweet  ",
            "    chirp chirp   ",
        ],
        text_representation="# tweet-tweet! chirp-chirp! #"
    ),
    
    "afternoon_buzz": AmbientSound(
        id="afternoon_buzz",
        name="Afternoon Buzz",
        description="Bees and insects in the warm sun",
        category=AmbientCategory.TIME_OF_DAY,
        mood=SoundMood.PEACEFUL,
        triggers=["afternoon", "midday"],
        ascii_visualization=[
            "  b bzzzz b    ",
            "    flutter...    ",
        ],
        text_representation="# bzzzzz... flutter flutter... #"
    ),
    
    "evening_crickets": AmbientSound(
        id="evening_crickets",
        name="Evening Crickets",
        description="Crickets chirping as dusk falls",
        category=AmbientCategory.TIME_OF_DAY,
        mood=SoundMood.CALM,
        triggers=["evening", "dusk"],
        ascii_visualization=[
            "  c chirp chirp  ",
            "    ...chirp...   ",
        ],
        text_representation="# chirp... chirp... chirp... #"
    ),
    
    "night_silence": AmbientSound(
        id="night_silence",
        name="Night Silence",
        description="Peaceful quiet of the night",
        category=AmbientCategory.TIME_OF_DAY,
        mood=SoundMood.PEACEFUL,
        triggers=["night", "late_night"],
        ascii_visualization=[
            "  * ... ) ...   ",
            "    (silence)     ",
        ],
        text_representation="# ... (peaceful night) ... #"
    ),
    
    "owl_hoot": AmbientSound(
        id="owl_hoot",
        name="Owl Hooting",
        description="A distant owl hoots",
        category=AmbientCategory.TIME_OF_DAY,
        mood=SoundMood.MYSTERIOUS,
        triggers=["night", "late_night"],
        loop=False,
        ascii_visualization=[
            "    O hoo-hoo    ",
        ],
        text_representation="# hoo... hoo-hoo... #"
    ),
    
    # Location sounds
    "pond_water": AmbientSound(
        id="pond_water",
        name="Pond Water",
        description="Gentle water lapping",
        category=AmbientCategory.LOCATION,
        mood=SoundMood.CALM,
        triggers=["pond", "lake", "water"],
        ascii_visualization=[
            "  ~~~~ ~~~~ ~~~   ",
            "    plop... plop  ",
        ],
        text_representation="# lap... lap... splash... #"
    ),
    
    "forest_rustle": AmbientSound(
        id="forest_rustle",
        name="Forest Rustling",
        description="Leaves and branches stirring",
        category=AmbientCategory.LOCATION,
        mood=SoundMood.PEACEFUL,
        triggers=["forest", "woods", "garden"],
        ascii_visualization=[
            "  ~ rustle ~    ",
            "    shh... shh... ",
        ],
        text_representation="# rustle... shh... rustle... #"
    ),
    
    "home_cozy": AmbientSound(
        id="home_cozy",
        name="Cozy Home",
        description="Warm crackling and soft sounds",
        category=AmbientCategory.LOCATION,
        mood=SoundMood.COZY,
        triggers=["home", "nest", "indoor"],
        ascii_visualization=[
            "  [=] crackle...   ",
            "    (cozy warm)   ",
        ],
        text_representation="# crackle... pop... warm... #"
    ),
    
    # Seasonal sounds
    "spring_bloom": AmbientSound(
        id="spring_bloom",
        name="Spring Awakening",
        description="Nature coming alive",
        category=AmbientCategory.SEASONAL,
        mood=SoundMood.ENERGETIC,
        triggers=["spring"],
        ascii_visualization=[
            "  * bloom *     ",
            "    nature sings  ",
        ],
        text_representation="# chirp! buzz! bloom! #"
    ),
    
    "summer_heat": AmbientSound(
        id="summer_heat",
        name="Summer Heat",
        description="Hot summer day sounds",
        category=AmbientCategory.SEASONAL,
        mood=SoundMood.PEACEFUL,
        triggers=["summer"],
        ascii_visualization=[
            "  * sizzle...    ",
            "    heat waves... ",
        ],
        text_representation="# bzzz... shimmer... hot... #"
    ),
    
    "autumn_leaves": AmbientSound(
        id="autumn_leaves",
        name="Autumn Leaves",
        description="Leaves crunching and falling",
        category=AmbientCategory.SEASONAL,
        mood=SoundMood.CALM,
        triggers=["autumn", "fall"],
        ascii_visualization=[
            "  f crunch f    ",
            "    scatter...    ",
        ],
        text_representation="# crunch... rustle... fall... #"
    ),
    
    "winter_chill": AmbientSound(
        id="winter_chill",
        name="Winter Chill",
        description="Cold winter atmosphere",
        category=AmbientCategory.SEASONAL,
        mood=SoundMood.PEACEFUL,
        triggers=["winter"],
        ascii_visualization=[
            "  * crisp...     ",
            "    chill air...  ",
        ],
        text_representation="# crunch... silence... cold... #"
    ),
    
    # Special sounds
    "festival_music": AmbientSound(
        id="festival_music",
        name="Festival Music",
        description="Joyful celebration music",
        category=AmbientCategory.SPECIAL,
        mood=SoundMood.ENERGETIC,
        triggers=["festival", "celebration"],
        ascii_visualization=[
            "  # # # #    ",
            "    party time!   ",
        ],
        text_representation="# la la la! celebrate! #"
    ),
    
    "sleeping_duck": AmbientSound(
        id="sleeping_duck",
        name="Sleeping Duck",
        description="Peaceful duck snoring",
        category=AmbientCategory.SPECIAL,
        mood=SoundMood.COZY,
        triggers=["sleeping", "napping"],
        ascii_visualization=[
            "  z zzz... z    ",
            "    (soft snore)  ",
        ],
        text_representation="# zzz... quack... zzz... #"
    ),
}


class AmbientSoundSystem:
    """
    System for managing ambient sounds.
    Uses text representations since this is a terminal game.
    """
    
    def __init__(self):
        self.enabled: bool = True
        self.master_volume: float = 0.7
        self.sound_volumes: Dict[str, float] = {}  # Individual sound volumes
        self.currently_playing: List[str] = []
        self.sound_preferences: Dict[str, bool] = {}  # Sound enabled/disabled
        self.last_update: str = ""
    
    def set_enabled(self, enabled: bool):
        """Enable or disable ambient sounds."""
        self.enabled = enabled
    
    def set_master_volume(self, volume: float):
        """Set master volume (0.0 to 1.0)."""
        self.master_volume = max(0.0, min(1.0, volume))
    
    def set_sound_volume(self, sound_id: str, volume: float):
        """Set volume for a specific sound."""
        self.sound_volumes[sound_id] = max(0.0, min(1.0, volume))
    
    def toggle_sound(self, sound_id: str) -> bool:
        """Toggle a specific sound on/off."""
        current = self.sound_preferences.get(sound_id, True)
        self.sound_preferences[sound_id] = not current
        return self.sound_preferences[sound_id]
    
    def update_ambient(self, weather: str, time_of_day: str, 
                       season: str, location: str, 
                       duck_state: str = "") -> List[AmbientSound]:
        """Update which ambient sounds should be playing based on context."""
        if not self.enabled:
            self.currently_playing = []
            return []
        
        # Collect all matching sounds
        matching = []
        triggers = [
            weather.lower(), 
            time_of_day.lower(), 
            season.lower(), 
            location.lower(),
            duck_state.lower()
        ]
        
        for sound in AMBIENT_SOUNDS.values():
            # Check if sound is enabled
            if not self.sound_preferences.get(sound.id, True):
                continue
            
            # Check if any trigger matches
            for trigger in triggers:
                if trigger and trigger in sound.triggers:
                    matching.append(sound)
                    break
        
        # Update currently playing
        self.currently_playing = [s.id for s in matching]
        self.last_update = datetime.now().isoformat()
        
        return matching
    
    def get_current_visualization(self) -> List[str]:
        """Get ASCII visualization of current ambient sounds."""
        if not self.enabled or not self.currently_playing:
            return ["  (ambient sounds off)  "]
        
        lines = []
        for sound_id in self.currently_playing[:3]:  # Show max 3
            sound = AMBIENT_SOUNDS.get(sound_id)
            if sound:
                lines.extend(sound.ascii_visualization)
        
        return lines if lines else ["  (quiet)  "]
    
    def get_text_representation(self) -> str:
        """Get text 'sound' representation for terminal output."""
        if not self.enabled or not self.currently_playing:
            return ""
        
        # Combine text representations
        sounds = []
        for sound_id in self.currently_playing[:2]:  # Max 2 sounds
            sound = AMBIENT_SOUNDS.get(sound_id)
            if sound and sound.text_representation:
                sounds.append(sound.text_representation)
        
        if not sounds:
            return ""
        
        return " | ".join(sounds)
    
    def get_mood(self) -> Optional[SoundMood]:
        """Get the overall mood based on current sounds."""
        if not self.currently_playing:
            return None
        
        mood_counts: Dict[SoundMood, int] = {}
        for sound_id in self.currently_playing:
            sound = AMBIENT_SOUNDS.get(sound_id)
            if sound:
                mood_counts[sound.mood] = mood_counts.get(sound.mood, 0) + 1
        
        if not mood_counts:
            return None
        
        return max(mood_counts, key=mood_counts.get)
    
    def render_sound_settings(self) -> List[str]:
        """Render the ambient sound settings screen."""
        lines = [
            "+===============================================+",
            "|          [=] AMBIENT SOUNDS [=]                 |",
            "+===============================================+",
        ]
        
        # Master settings
        enabled_str = "ON" if self.enabled else "OFF"
        volume_bar = "█" * int(self.master_volume * 10) + "." * (10 - int(self.master_volume * 10))
        
        lines.append(f"|  Ambient Sounds: {enabled_str:<26}  |")
        lines.append(f"|  Master Volume: [{volume_bar}] {int(self.master_volume * 100):>3}%  |")
        lines.append("+===============================================+")
        
        # Current sounds
        lines.append("|  Currently Playing:                           |")
        if self.currently_playing:
            for sound_id in self.currently_playing:
                sound = AMBIENT_SOUNDS.get(sound_id)
                if sound:
                    lines.append(f"|  • {sound.name:<40}  |")
        else:
            lines.append("|  (none)                                       |")
        
        lines.append("+===============================================+")
        
        # Sound categories
        lines.append("|  Sound Categories:                            |")
        for category in AmbientCategory:
            sounds_in_cat = [s for s in AMBIENT_SOUNDS.values() if s.category == category]
            enabled_count = sum(1 for s in sounds_in_cat if self.sound_preferences.get(s.id, True))
            lines.append(f"|  {category.value.upper()}: {enabled_count}/{len(sounds_in_cat)} enabled         |")
        
        lines.extend([
            "+===============================================+",
            "|  [T] Toggle  [+/-] Volume  [B] Back           |",
            "+===============================================+",
        ])
        
        return lines
    
    def render_sound_list(self, category: Optional[AmbientCategory] = None) -> List[str]:
        """Render list of all sounds for configuration."""
        lines = [
            "+===============================================+",
            "|          # SOUND LIST #                     |",
            "+===============================================+",
        ]
        
        sounds = list(AMBIENT_SOUNDS.values())
        if category:
            sounds = [s for s in sounds if s.category == category]
        
        for sound in sounds:
            enabled = self.sound_preferences.get(sound.id, True)
            status = "x" if enabled else " "
            volume = self.sound_volumes.get(sound.id, sound.volume_default)
            vol_str = f"{int(volume * 100)}%"
            
            lines.append(f"|  [{status}] {sound.name:<25} {vol_str:>5}  |")
            lines.append(f"|      {sound.description[:38]:<38}  |")
        
        lines.extend([
            "+===============================================+",
            "|  [#] Toggle  [B] Back                         |",
            "+===============================================+",
        ])
        
        return lines
    
    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "enabled": self.enabled,
            "master_volume": self.master_volume,
            "sound_volumes": self.sound_volumes,
            "sound_preferences": self.sound_preferences,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "AmbientSoundSystem":
        """Create from dictionary."""
        system = cls()
        system.enabled = data.get("enabled", True)
        system.master_volume = data.get("master_volume", 0.7)
        system.sound_volumes = data.get("sound_volumes", {})
        system.sound_preferences = data.get("sound_preferences", {})
        return system


# Lazy singleton pattern - initialized on first access with thread safety
_ambient_sound_system: Optional[AmbientSoundSystem] = None
_ambient_sound_lock = threading.Lock()


def get_ambient_sound_system() -> AmbientSoundSystem:
    """Get the global ambient sound system instance (lazy initialization). Thread-safe.

    This pattern defers initialization until the system is actually needed,
    improving startup time and avoiding circular import issues.
    """
    global _ambient_sound_system
    if _ambient_sound_system is None:
        with _ambient_sound_lock:
            # Double-check after acquiring lock
            if _ambient_sound_system is None:
                _ambient_sound_system = AmbientSoundSystem()
    return _ambient_sound_system


# Direct instance for backwards compatibility - uses the singleton
ambient_sound_system = get_ambient_sound_system()
