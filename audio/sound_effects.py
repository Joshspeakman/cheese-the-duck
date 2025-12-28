"""
Sound Effects System - Expanded duck sounds and game audio.
Text-based sound representations with timing and context awareness.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Callable
from enum import Enum
import random


class SoundCategory(Enum):
    """Categories of sounds."""
    DUCK_VOICE = "duck_voice"
    DUCK_MOVEMENT = "duck_movement"
    DUCK_ACTION = "duck_action"
    ENVIRONMENT = "environment"
    UI = "ui"
    NOTIFICATION = "notification"
    MUSIC = "music"
    SPECIAL = "special"


class SoundPriority(Enum):
    """Priority levels for sounds."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class MoodModifier(Enum):
    """How mood affects sounds."""
    NONE = "none"
    PITCH_UP = "pitch_up"      # Happy = higher pitch
    PITCH_DOWN = "pitch_down"  # Sad = lower pitch
    LOUDER = "louder"
    SOFTER = "softer"
    FASTER = "faster"
    SLOWER = "slower"


@dataclass
class SoundEffect:
    """A sound effect definition."""
    sound_id: str
    name: str
    category: SoundCategory
    text_representation: List[str]  # ASCII/text representations
    priority: SoundPriority
    duration_ms: int  # How long the sound "lasts"
    mood_modifier: MoodModifier
    can_overlap: bool = True
    cooldown_ms: int = 0
    variations: int = 1  # Number of text variations


@dataclass
class ActiveSound:
    """A currently playing sound."""
    sound: SoundEffect
    start_time: float
    display_text: str
    intensity: float = 1.0
    is_looping: bool = False


# Duck voice sounds
DUCK_VOICE_SOUNDS = {
    "quack": SoundEffect(
        sound_id="quack",
        name="Basic Quack",
        category=SoundCategory.DUCK_VOICE,
        text_representation=[
            "Quack!",
            "QUACK!",
            "quack~",
            "Quaaack!",
        ],
        priority=SoundPriority.MEDIUM,
        duration_ms=500,
        mood_modifier=MoodModifier.PITCH_UP,
        variations=4,
    ),
    "happy_quack": SoundEffect(
        sound_id="happy_quack",
        name="Happy Quack",
        category=SoundCategory.DUCK_VOICE,
        text_representation=[
            "QUACK QUACK! ♪",
            "Quaaack~! 💕",
            "QUA~ACK! ✨",
            "Quack quack quack! 🎵",
        ],
        priority=SoundPriority.MEDIUM,
        duration_ms=700,
        mood_modifier=MoodModifier.PITCH_UP,
        variations=4,
    ),
    "sad_quack": SoundEffect(
        sound_id="sad_quack",
        name="Sad Quack",
        category=SoundCategory.DUCK_VOICE,
        text_representation=[
            "...quack...",
            "qua...ck...",
            "*sad quack*",
            "quack... 😢",
        ],
        priority=SoundPriority.MEDIUM,
        duration_ms=800,
        mood_modifier=MoodModifier.PITCH_DOWN,
        variations=4,
    ),
    "excited_quack": SoundEffect(
        sound_id="excited_quack",
        name="Excited Quack",
        category=SoundCategory.DUCK_VOICE,
        text_representation=[
            "QUACK QUACK QUACK!!!",
            "QuAcK qUaCk!!!",
            "QUAAAAAACK! 🎉",
            "!!QUACK QUACK!!",
        ],
        priority=SoundPriority.HIGH,
        duration_ms=600,
        mood_modifier=MoodModifier.FASTER,
        variations=4,
    ),
    "sleepy_quack": SoundEffect(
        sound_id="sleepy_quack",
        name="Sleepy Quack",
        category=SoundCategory.DUCK_VOICE,
        text_representation=[
            "...quaaaack... 💤",
            "qua...zzzz...",
            "*yawn* quack...",
            "mmm...quack... 😴",
        ],
        priority=SoundPriority.LOW,
        duration_ms=1000,
        mood_modifier=MoodModifier.SLOWER,
        variations=4,
    ),
    "angry_quack": SoundEffect(
        sound_id="angry_quack",
        name="Angry Quack",
        category=SoundCategory.DUCK_VOICE,
        text_representation=[
            "QUACK! 😠",
            "QUACK QUACK!! >:[",
            "*aggressive quack*",
            "QUAAACK!!! 💢",
        ],
        priority=SoundPriority.HIGH,
        duration_ms=500,
        mood_modifier=MoodModifier.LOUDER,
        variations=4,
    ),
    "questioning_quack": SoundEffect(
        sound_id="questioning_quack",
        name="Questioning Quack",
        category=SoundCategory.DUCK_VOICE,
        text_representation=[
            "Quack?",
            "Quack...?",
            "*confused quack*",
            "Qua...ck? 🤔",
        ],
        priority=SoundPriority.MEDIUM,
        duration_ms=600,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
    "honk": SoundEffect(
        sound_id="honk",
        name="Honk",
        category=SoundCategory.DUCK_VOICE,
        text_representation=[
            "HONK!",
            "HONK HONK!",
            "*loud honk*",
            "HOOOOONK!",
        ],
        priority=SoundPriority.HIGH,
        duration_ms=700,
        mood_modifier=MoodModifier.LOUDER,
        variations=4,
    ),
    "whisper_quack": SoundEffect(
        sound_id="whisper_quack",
        name="Whisper Quack",
        category=SoundCategory.DUCK_VOICE,
        text_representation=[
            "...quack...",
            "*quiet quack*",
            "ᵠᵘᵃᶜᵏ",
            "(quack)",
        ],
        priority=SoundPriority.LOW,
        duration_ms=400,
        mood_modifier=MoodModifier.SOFTER,
        variations=4,
    ),
    "chirp": SoundEffect(
        sound_id="chirp",
        name="Baby Chirp",
        category=SoundCategory.DUCK_VOICE,
        text_representation=[
            "Peep!",
            "Cheep cheep!",
            "*tiny peep*",
            "Pip pip! 🐣",
        ],
        priority=SoundPriority.MEDIUM,
        duration_ms=300,
        mood_modifier=MoodModifier.PITCH_UP,
        variations=4,
    ),
    "singing": SoundEffect(
        sound_id="singing",
        name="Duck Singing",
        category=SoundCategory.DUCK_VOICE,
        text_representation=[
            "♪ Quack quack quack ♪",
            "🎵 La la quack~ 🎵",
            "♫ Quaaack~ ♫",
            "🎶 Qua~ck qua~ck 🎶",
        ],
        priority=SoundPriority.MEDIUM,
        duration_ms=1500,
        mood_modifier=MoodModifier.PITCH_UP,
        variations=4,
    ),
}

# Duck movement sounds
DUCK_MOVEMENT_SOUNDS = {
    "waddle": SoundEffect(
        sound_id="waddle",
        name="Waddling",
        category=SoundCategory.DUCK_MOVEMENT,
        text_representation=[
            "*waddle waddle*",
            "*pitter patter*",
            "*tap tap tap*",
            "*waddle walk*",
        ],
        priority=SoundPriority.LOW,
        duration_ms=400,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
    "splash": SoundEffect(
        sound_id="splash",
        name="Splash",
        category=SoundCategory.DUCK_MOVEMENT,
        text_representation=[
            "*SPLASH!*",
            "*splish splash*",
            "*sploosh!*",
            "💦 SPLASH! 💦",
        ],
        priority=SoundPriority.MEDIUM,
        duration_ms=600,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
    "flap": SoundEffect(
        sound_id="flap",
        name="Wing Flap",
        category=SoundCategory.DUCK_MOVEMENT,
        text_representation=[
            "*flap flap*",
            "*flutter flutter*",
            "*whoosh!*",
            "*wings flapping*",
        ],
        priority=SoundPriority.LOW,
        duration_ms=500,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
    "hop": SoundEffect(
        sound_id="hop",
        name="Little Hop",
        category=SoundCategory.DUCK_MOVEMENT,
        text_representation=[
            "*hop!*",
            "*boing!*",
            "*little jump*",
            "*hop hop!*",
        ],
        priority=SoundPriority.LOW,
        duration_ms=300,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
    "slide": SoundEffect(
        sound_id="slide",
        name="Sliding",
        category=SoundCategory.DUCK_MOVEMENT,
        text_representation=[
            "*sliiide*",
            "*wheee~*",
            "*swoosh*",
            "*sliding noises*",
        ],
        priority=SoundPriority.LOW,
        duration_ms=800,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
    "plop": SoundEffect(
        sound_id="plop",
        name="Sit Down Plop",
        category=SoundCategory.DUCK_MOVEMENT,
        text_representation=[
            "*plop*",
            "*flump*",
            "*sits down*",
            "*plop!* 🦆",
        ],
        priority=SoundPriority.LOW,
        duration_ms=300,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
    "tippy_tap": SoundEffect(
        sound_id="tippy_tap",
        name="Tippy Taps",
        category=SoundCategory.DUCK_MOVEMENT,
        text_representation=[
            "*tap tap tap tap*",
            "*tippy tap tippy tap*",
            "*excited feet noises*",
            "*rapid tapping* 🦶",
        ],
        priority=SoundPriority.LOW,
        duration_ms=700,
        mood_modifier=MoodModifier.FASTER,
        variations=4,
    ),
    "stumble": SoundEffect(
        sound_id="stumble",
        name="Stumble",
        category=SoundCategory.DUCK_MOVEMENT,
        text_representation=[
            "*wobble wobble*",
            "*trips* Oops!",
            "*stumbles*",
            "*bonk!*",
        ],
        priority=SoundPriority.MEDIUM,
        duration_ms=500,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
}

# Duck action sounds
DUCK_ACTION_SOUNDS = {
    "eat": SoundEffect(
        sound_id="eat",
        name="Eating",
        category=SoundCategory.DUCK_ACTION,
        text_representation=[
            "*nom nom*",
            "*munch munch*",
            "*gobble gobble*",
            "*chomp chomp*",
        ],
        priority=SoundPriority.MEDIUM,
        duration_ms=600,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
    "drink": SoundEffect(
        sound_id="drink",
        name="Drinking",
        category=SoundCategory.DUCK_ACTION,
        text_representation=[
            "*sip sip*",
            "*gulp gulp*",
            "*slurp*",
            "*drinking noises*",
        ],
        priority=SoundPriority.LOW,
        duration_ms=500,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
    "preen": SoundEffect(
        sound_id="preen",
        name="Preening",
        category=SoundCategory.DUCK_ACTION,
        text_representation=[
            "*preen preen*",
            "*fluff fluff*",
            "*ruffling feathers*",
            "*self-care sounds*",
        ],
        priority=SoundPriority.LOW,
        duration_ms=800,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
    "shake": SoundEffect(
        sound_id="shake",
        name="Shake Off Water",
        category=SoundCategory.DUCK_ACTION,
        text_representation=[
            "*shake shake shake*",
            "*fluff!* 💦",
            "*vigorous shaking*",
            "*water everywhere!*",
        ],
        priority=SoundPriority.MEDIUM,
        duration_ms=600,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
    "nap_start": SoundEffect(
        sound_id="nap_start",
        name="Starting Nap",
        category=SoundCategory.DUCK_ACTION,
        text_representation=[
            "*yaaawn*",
            "*settles down* 💤",
            "*getting cozy*",
            "*sleepy eyes*",
        ],
        priority=SoundPriority.LOW,
        duration_ms=1000,
        mood_modifier=MoodModifier.SLOWER,
        variations=4,
    ),
    "snoring": SoundEffect(
        sound_id="snoring",
        name="Snoring",
        category=SoundCategory.DUCK_ACTION,
        text_representation=[
            "zzz... zzz...",
            "*tiny snores* 💤",
            "ZZzzZZzz...",
            "*peaceful sleeping*",
        ],
        priority=SoundPriority.LOW,
        duration_ms=2000,
        mood_modifier=MoodModifier.SLOWER,
        can_overlap=False,
        variations=4,
    ),
    "wake_up": SoundEffect(
        sound_id="wake_up",
        name="Waking Up",
        category=SoundCategory.DUCK_ACTION,
        text_representation=[
            "*stretch* Good morning!",
            "*blinks awake*",
            "*yawn* ...quack?",
            "*rises and shines*",
        ],
        priority=SoundPriority.MEDIUM,
        duration_ms=800,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
    "find_item": SoundEffect(
        sound_id="find_item",
        name="Found Something",
        category=SoundCategory.DUCK_ACTION,
        text_representation=[
            "*gasp!* ✨",
            "Ooh! What's this?",
            "*discovery sounds*",
            "*excited find!* 🎁",
        ],
        priority=SoundPriority.HIGH,
        duration_ms=600,
        mood_modifier=MoodModifier.PITCH_UP,
        variations=4,
    ),
    "craft": SoundEffect(
        sound_id="craft",
        name="Crafting",
        category=SoundCategory.DUCK_ACTION,
        text_representation=[
            "*tink tink*",
            "*busy crafting*",
            "*making something*",
            "*creative noises* 🔨",
        ],
        priority=SoundPriority.MEDIUM,
        duration_ms=1000,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
    "dig": SoundEffect(
        sound_id="dig",
        name="Digging",
        category=SoundCategory.DUCK_ACTION,
        text_representation=[
            "*dig dig dig*",
            "*scrape scrape*",
            "*digging sounds*",
            "*excavating* 🕳️",
        ],
        priority=SoundPriority.LOW,
        duration_ms=700,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
}

# Environment sounds
ENVIRONMENT_SOUNDS = {
    "rain": SoundEffect(
        sound_id="rain",
        name="Rain",
        category=SoundCategory.ENVIRONMENT,
        text_representation=[
            "☔ *pitter patter*",
            "*rain falling*",
            "🌧️ *gentle rain*",
            "*raindrops*",
        ],
        priority=SoundPriority.LOW,
        duration_ms=5000,
        mood_modifier=MoodModifier.NONE,
        can_overlap=False,
        variations=4,
    ),
    "thunder": SoundEffect(
        sound_id="thunder",
        name="Thunder",
        category=SoundCategory.ENVIRONMENT,
        text_representation=[
            "⚡ RUMBLE! ⚡",
            "*BOOM!*",
            "⛈️ *thunder crashes*",
            "*loud thunder!*",
        ],
        priority=SoundPriority.HIGH,
        duration_ms=1500,
        mood_modifier=MoodModifier.LOUDER,
        cooldown_ms=5000,
        variations=4,
    ),
    "wind": SoundEffect(
        sound_id="wind",
        name="Wind",
        category=SoundCategory.ENVIRONMENT,
        text_representation=[
            "*whoooosh*",
            "💨 *wind blowing*",
            "*rustling leaves*",
            "*breezy sounds*",
        ],
        priority=SoundPriority.LOW,
        duration_ms=3000,
        mood_modifier=MoodModifier.NONE,
        can_overlap=False,
        variations=4,
    ),
    "birds_chirping": SoundEffect(
        sound_id="birds_chirping",
        name="Birds Chirping",
        category=SoundCategory.ENVIRONMENT,
        text_representation=[
            "🐦 *tweet tweet*",
            "*birdsong*",
            "*chirp chirp*",
            "*morning birds*",
        ],
        priority=SoundPriority.LOW,
        duration_ms=2000,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
    "crickets": SoundEffect(
        sound_id="crickets",
        name="Crickets",
        category=SoundCategory.ENVIRONMENT,
        text_representation=[
            "*chirp chirp*",
            "🦗 *cricket sounds*",
            "*night insects*",
            "*evening crickets*",
        ],
        priority=SoundPriority.LOW,
        duration_ms=3000,
        mood_modifier=MoodModifier.NONE,
        can_overlap=False,
        variations=4,
    ),
    "water_flowing": SoundEffect(
        sound_id="water_flowing",
        name="Flowing Water",
        category=SoundCategory.ENVIRONMENT,
        text_representation=[
            "*gentle stream*",
            "💧 *water flowing*",
            "*babbling brook*",
            "*peaceful water*",
        ],
        priority=SoundPriority.LOW,
        duration_ms=4000,
        mood_modifier=MoodModifier.NONE,
        can_overlap=False,
        variations=4,
    ),
}

# UI sounds
UI_SOUNDS = {
    "menu_open": SoundEffect(
        sound_id="menu_open",
        name="Menu Open",
        category=SoundCategory.UI,
        text_representation=[
            "*swish*",
            "*pop*",
            "[MENU]",
            "*click*",
        ],
        priority=SoundPriority.LOW,
        duration_ms=200,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
    "menu_close": SoundEffect(
        sound_id="menu_close",
        name="Menu Close",
        category=SoundCategory.UI,
        text_representation=[
            "*whoosh*",
            "*closed*",
            "[CLOSE]",
            "*click*",
        ],
        priority=SoundPriority.LOW,
        duration_ms=200,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
    "select": SoundEffect(
        sound_id="select",
        name="Selection",
        category=SoundCategory.UI,
        text_representation=[
            "*bloop*",
            "*ding*",
            "[SELECT]",
            "*pip*",
        ],
        priority=SoundPriority.LOW,
        duration_ms=150,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
    "confirm": SoundEffect(
        sound_id="confirm",
        name="Confirm",
        category=SoundCategory.UI,
        text_representation=[
            "*ding!* ✓",
            "*confirmed*",
            "[OK!]",
            "*success*",
        ],
        priority=SoundPriority.MEDIUM,
        duration_ms=300,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
    "error": SoundEffect(
        sound_id="error",
        name="Error",
        category=SoundCategory.UI,
        text_representation=[
            "*buzz* ✗",
            "*error*",
            "[NOPE]",
            "*denied*",
        ],
        priority=SoundPriority.MEDIUM,
        duration_ms=300,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
    "coins": SoundEffect(
        sound_id="coins",
        name="Coins",
        category=SoundCategory.UI,
        text_representation=[
            "*clink clink* 💰",
            "*cha-ching!*",
            "[COINS!]",
            "*money sounds*",
        ],
        priority=SoundPriority.MEDIUM,
        duration_ms=400,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
    "level_up": SoundEffect(
        sound_id="level_up",
        name="Level Up",
        category=SoundCategory.UI,
        text_representation=[
            "⬆️ LEVEL UP! ⬆️",
            "✨ *fanfare* ✨",
            "[LEVEL UP!]",
            "🎉 *celebration* 🎉",
        ],
        priority=SoundPriority.HIGH,
        duration_ms=1500,
        mood_modifier=MoodModifier.PITCH_UP,
        variations=4,
    ),
    "achievement": SoundEffect(
        sound_id="achievement",
        name="Achievement",
        category=SoundCategory.UI,
        text_representation=[
            "🏆 ACHIEVEMENT! 🏆",
            "✨ *unlock sound* ✨",
            "[UNLOCKED!]",
            "🌟 *special sound* 🌟",
        ],
        priority=SoundPriority.HIGH,
        duration_ms=1200,
        mood_modifier=MoodModifier.PITCH_UP,
        variations=4,
    ),
}

# Notification sounds
NOTIFICATION_SOUNDS = {
    "alert": SoundEffect(
        sound_id="alert",
        name="Alert",
        category=SoundCategory.NOTIFICATION,
        text_representation=[
            "❗ *ding!*",
            "*alert sound*",
            "[ALERT!]",
            "⚠️ *notification*",
        ],
        priority=SoundPriority.HIGH,
        duration_ms=400,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
    "visitor": SoundEffect(
        sound_id="visitor",
        name="Visitor Arrived",
        category=SoundCategory.NOTIFICATION,
        text_representation=[
            "🚪 *knock knock*",
            "*doorbell*",
            "[VISITOR!]",
            "👋 *someone's here!*",
        ],
        priority=SoundPriority.HIGH,
        duration_ms=800,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
    "new_day": SoundEffect(
        sound_id="new_day",
        name="New Day",
        category=SoundCategory.NOTIFICATION,
        text_representation=[
            "🌅 *rooster crow*",
            "*new day dawns*",
            "[NEW DAY!]",
            "☀️ *morning chime*",
        ],
        priority=SoundPriority.MEDIUM,
        duration_ms=1000,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
    "gift": SoundEffect(
        sound_id="gift",
        name="Received Gift",
        category=SoundCategory.NOTIFICATION,
        text_representation=[
            "🎁 *sparkle*",
            "*gift received!*",
            "[GIFT!]",
            "✨ *present sounds*",
        ],
        priority=SoundPriority.HIGH,
        duration_ms=700,
        mood_modifier=MoodModifier.PITCH_UP,
        variations=4,
    ),
}

# Special sounds
SPECIAL_SOUNDS = {
    "rare_find": SoundEffect(
        sound_id="rare_find",
        name="Rare Discovery",
        category=SoundCategory.SPECIAL,
        text_representation=[
            "⭐ *AMAZING FIND!* ⭐",
            "🌟 *legendary sound* 🌟",
            "[INCREDIBLE!]",
            "✨ *magical chime* ✨",
        ],
        priority=SoundPriority.CRITICAL,
        duration_ms=1500,
        mood_modifier=MoodModifier.PITCH_UP,
        variations=4,
    ),
    "birthday": SoundEffect(
        sound_id="birthday",
        name="Birthday",
        category=SoundCategory.SPECIAL,
        text_representation=[
            "🎂 *Happy Birthday!* 🎂",
            "🎉 *party sounds* 🎉",
            "[BIRTHDAY!]",
            "🎈 *celebration* 🎈",
        ],
        priority=SoundPriority.CRITICAL,
        duration_ms=2000,
        mood_modifier=MoodModifier.LOUDER,
        variations=4,
    ),
    "secret_found": SoundEffect(
        sound_id="secret_found",
        name="Secret Found",
        category=SoundCategory.SPECIAL,
        text_representation=[
            "🔮 *SECRET!* 🔮",
            "*mysterious sound*",
            "[SECRET UNLOCKED!]",
            "🗝️ *hidden discovery* 🗝️",
        ],
        priority=SoundPriority.CRITICAL,
        duration_ms=1200,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
    "magic": SoundEffect(
        sound_id="magic",
        name="Magic",
        category=SoundCategory.SPECIAL,
        text_representation=[
            "✨ *sparkle sparkle* ✨",
            "*magical sounds*",
            "[MAGIC!]",
            "💫 *enchanting* 💫",
        ],
        priority=SoundPriority.HIGH,
        duration_ms=1000,
        mood_modifier=MoodModifier.PITCH_UP,
        variations=4,
    ),
    "heartbeat": SoundEffect(
        sound_id="heartbeat",
        name="Heartbeat",
        category=SoundCategory.SPECIAL,
        text_representation=[
            "💓 *thump thump*",
            "*heartbeat*",
            "❤️ *ba-dum*",
            "*beating heart*",
        ],
        priority=SoundPriority.LOW,
        duration_ms=1000,
        mood_modifier=MoodModifier.NONE,
        variations=4,
    ),
}

# Combine all sounds
ALL_SOUND_EFFECTS = {
    **DUCK_VOICE_SOUNDS,
    **DUCK_MOVEMENT_SOUNDS,
    **DUCK_ACTION_SOUNDS,
    **ENVIRONMENT_SOUNDS,
    **UI_SOUNDS,
    **NOTIFICATION_SOUNDS,
    **SPECIAL_SOUNDS,
}


class SoundEffectSystem:
    """Manages sound effects playback (text-based)."""
    
    def __init__(self):
        self.active_sounds: List[ActiveSound] = []
        self.sound_history: List[Dict] = []
        self.last_played: Dict[str, float] = {}  # sound_id -> timestamp
        self.volume_master: float = 1.0
        self.volume_categories: Dict[SoundCategory, float] = {
            cat: 1.0 for cat in SoundCategory
        }
        self.muted: bool = False
        self.sound_enabled: Dict[str, bool] = {}  # Per-sound enable/disable
        
    def get_sound(self, sound_id: str) -> Optional[SoundEffect]:
        """Get a sound effect by ID."""
        return ALL_SOUND_EFFECTS.get(sound_id)
        
    def can_play(self, sound_id: str, current_time: float) -> bool:
        """Check if a sound can be played."""
        if self.muted:
            return False
            
        if sound_id in self.sound_enabled and not self.sound_enabled[sound_id]:
            return False
            
        sound = self.get_sound(sound_id)
        if not sound:
            return False
            
        # Check cooldown
        if sound.cooldown_ms > 0:
            last = self.last_played.get(sound_id, 0)
            if current_time - last < sound.cooldown_ms / 1000:
                return False
                
        # Check overlap
        if not sound.can_overlap:
            for active in self.active_sounds:
                if active.sound.sound_id == sound_id:
                    return False
                    
        return True
        
    def play(self, sound_id: str, intensity: float = 1.0, mood: Optional[str] = None) -> Optional[str]:
        """Play a sound effect and return its text representation."""
        import time
        current_time = time.time()
        
        if not self.can_play(sound_id, current_time):
            return None
            
        sound = self.get_sound(sound_id)
        if not sound:
            return None
            
        # Select variation
        variation_idx = random.randint(0, sound.variations - 1)
        text = sound.text_representation[variation_idx]
        
        # Apply mood modifier to text if applicable
        if mood and sound.mood_modifier != MoodModifier.NONE:
            text = self._apply_mood_modifier(text, mood, sound.mood_modifier)
            
        # Create active sound
        active = ActiveSound(
            sound=sound,
            start_time=current_time,
            display_text=text,
            intensity=intensity,
        )
        
        self.active_sounds.append(active)
        self.last_played[sound_id] = current_time
        
        # Record in history
        self.sound_history.append({
            "sound_id": sound_id,
            "text": text,
            "time": datetime.now().isoformat(),
            "intensity": intensity,
        })
        
        # Keep history limited
        if len(self.sound_history) > 100:
            self.sound_history = self.sound_history[-100:]
            
        return text
        
    def _apply_mood_modifier(self, text: str, mood: str, modifier: MoodModifier) -> str:
        """Apply mood-based modifications to sound text."""
        if modifier == MoodModifier.PITCH_UP and mood == "happy":
            text = text.replace("!", "! ♪")
        elif modifier == MoodModifier.PITCH_DOWN and mood == "sad":
            text = text.replace("!", "...")
        elif modifier == MoodModifier.LOUDER:
            text = text.upper()
        elif modifier == MoodModifier.SOFTER:
            text = text.lower()
        elif modifier == MoodModifier.FASTER:
            text = text.replace(" ", "")
        elif modifier == MoodModifier.SLOWER:
            text = text.replace(" ", "... ")
        return text
        
    def update(self, current_time: float):
        """Update active sounds, removing expired ones."""
        self.active_sounds = [
            s for s in self.active_sounds
            if current_time - s.start_time < s.sound.duration_ms / 1000
            or s.is_looping
        ]
        
    def get_active_display(self) -> List[str]:
        """Get text displays for all active sounds."""
        return [s.display_text for s in self.active_sounds]
        
    def get_sounds_by_category(self, category: SoundCategory) -> List[SoundEffect]:
        """Get all sounds in a category."""
        return [s for s in ALL_SOUND_EFFECTS.values() if s.category == category]
        
    def set_volume(self, volume: float):
        """Set master volume (0.0 to 1.0)."""
        self.volume_master = max(0.0, min(1.0, volume))
        
    def set_category_volume(self, category: SoundCategory, volume: float):
        """Set volume for a category."""
        self.volume_categories[category] = max(0.0, min(1.0, volume))
        
    def toggle_mute(self):
        """Toggle mute."""
        self.muted = not self.muted
        
    def enable_sound(self, sound_id: str, enabled: bool = True):
        """Enable or disable a specific sound."""
        self.sound_enabled[sound_id] = enabled
        
    def play_random_from_category(self, category: SoundCategory, intensity: float = 1.0) -> Optional[str]:
        """Play a random sound from a category."""
        sounds = self.get_sounds_by_category(category)
        if sounds:
            sound = random.choice(sounds)
            return self.play(sound.sound_id, intensity)
        return None
        
    def get_sound_statistics(self) -> Dict:
        """Get sound usage statistics."""
        stats = {
            "total_sounds": len(ALL_SOUND_EFFECTS),
            "total_played": len(self.sound_history),
            "by_category": {},
        }
        
        for cat in SoundCategory:
            cat_sounds = self.get_sounds_by_category(cat)
            stats["by_category"][cat.value] = {
                "total": len(cat_sounds),
                "played": sum(1 for h in self.sound_history 
                             if self.get_sound(h["sound_id"]) and 
                             self.get_sound(h["sound_id"]).category == cat),
            }
            
        return stats
        
    def render_sound_mixer(self, width: int = 50) -> List[str]:
        """Render a sound mixer display."""
        lines = []
        
        lines.append("╔" + "═" * (width - 2) + "╗")
        lines.append("║" + " 🔊 Sound Mixer 🔊 ".center(width - 2) + "║")
        lines.append("╠" + "═" * (width - 2) + "╣")
        
        # Master volume
        mute_str = " 🔇 MUTED" if self.muted else ""
        bar_width = 20
        bar_filled = int(self.volume_master * bar_width)
        bar = "█" * bar_filled + "░" * (bar_width - bar_filled)
        
        lines.append("║" + f" Master: [{bar}] {int(self.volume_master * 100)}%{mute_str}"[:width-3].ljust(width - 2) + "║")
        
        lines.append("╠" + "─" * (width - 2) + "╣")
        
        # Category volumes
        for cat in SoundCategory:
            vol = self.volume_categories.get(cat, 1.0)
            bar_filled = int(vol * 15)
            bar = "▓" * bar_filled + "░" * (15 - bar_filled)
            cat_name = cat.value.replace("_", " ").title()
            lines.append("║" + f" {cat_name}: [{bar}]"[:width-3].ljust(width - 2) + "║")
            
        lines.append("╠" + "─" * (width - 2) + "╣")
        
        # Currently playing
        lines.append("║" + " Now Playing: ".ljust(width - 2) + "║")
        
        if self.active_sounds:
            for sound in self.active_sounds[:3]:
                lines.append("║" + f"  • {sound.display_text}"[:width-3].ljust(width - 2) + "║")
        else:
            lines.append("║" + "  (silence)".ljust(width - 2) + "║")
            
        lines.append("╚" + "═" * (width - 2) + "╝")
        
        return lines
        
    def to_dict(self) -> Dict:
        """Serialize settings to dictionary."""
        return {
            "volume_master": self.volume_master,
            "volume_categories": {c.value: v for c, v in self.volume_categories.items()},
            "muted": self.muted,
            "sound_enabled": self.sound_enabled,
            "sound_history": self.sound_history[-50:],  # Keep last 50
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "SoundEffectSystem":
        """Deserialize from dictionary."""
        system = cls()
        system.volume_master = data.get("volume_master", 1.0)
        
        for cat_str, vol in data.get("volume_categories", {}).items():
            try:
                cat = SoundCategory(cat_str)
                system.volume_categories[cat] = vol
            except ValueError:
                pass
                
        system.muted = data.get("muted", False)
        system.sound_enabled = data.get("sound_enabled", {})
        system.sound_history = data.get("sound_history", [])
        return system


# Global instance
sound_effects = SoundEffectSystem()
