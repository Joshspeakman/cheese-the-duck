"""
Expanded Personality Traits System - Deep personality mechanics with trait interactions.
Extends the base personality system with more traits, quirks, and behavioral modifiers.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random


class TraitCategory(Enum):
    """Categories of personality traits."""
    CORE = "core"           # Main personality axes
    QUIRK = "quirk"         # Unique behaviors
    PREFERENCE = "preference"  # Likes and dislikes
    HIDDEN = "hidden"       # Secret traits discovered over time


class QuirkType(Enum):
    """Types of unique quirks a duck can have."""
    # Movement quirks
    WADDLE_WIGGLE = "waddle_wiggle"
    TIPPY_TAPS = "tippy_taps"
    SPIN_BEFORE_SIT = "spin_before_sit"
    BACKWARDS_WALKER = "backwards_walker"
    
    # Sound quirks
    MELODIC_QUACK = "melodic_quack"
    WHISPER_QUACK = "whisper_quack"
    DOUBLE_QUACK = "double_quack"
    HONK_INSTEAD = "honk_instead"
    
    # Behavior quirks
    HEAD_TILT = "head_tilt"
    WING_STRETCH = "wing_stretch"
    TAIL_WAGGLE = "tail_waggle"
    BLINK_SLOWLY = "blink_slowly"
    
    # Food quirks
    FOOD_INSPECTOR = "food_inspector"
    CRUMB_COLLECTOR = "crumb_collector"
    NEAT_EATER = "neat_eater"
    FOOD_DANCER = "food_dancer"
    
    # Social quirks
    GIFT_GIVER = "gift_giver"
    PERSONAL_SPACE = "personal_space"
    CUDDLE_BUG = "cuddle_bug"
    SHOW_OFF = "show_off"
    
    # Special quirks
    NIGHT_OWL = "night_owl"
    EARLY_BIRD = "early_bird"
    RAIN_LOVER = "rain_lover"
    STAR_GAZER = "star_gazer"


class PreferenceType(Enum):
    """Types of preferences a duck can have."""
    # Food preferences
    FAVORITE_FOOD = "favorite_food"
    HATED_FOOD = "hated_food"
    
    # Weather preferences
    FAVORITE_WEATHER = "favorite_weather"
    HATED_WEATHER = "hated_weather"
    
    # Activity preferences
    FAVORITE_ACTIVITY = "favorite_activity"
    DISLIKED_ACTIVITY = "disliked_activity"
    
    # Time preferences
    PREFERRED_TIME = "preferred_time"
    
    # Color preferences
    FAVORITE_COLOR = "favorite_color"
    
    # Location preferences
    FAVORITE_SPOT = "favorite_spot"


@dataclass
class TraitInfo:
    """Information about a personality trait."""
    trait_id: str
    name: str
    category: TraitCategory
    description: str
    positive_effects: Dict[str, float]
    negative_effects: Dict[str, float]
    animation_modifiers: Dict[str, str]
    dialogue_modifiers: List[str]


@dataclass
class QuirkInfo:
    """Information about a quirk."""
    quirk_type: QuirkType
    name: str
    description: str
    trigger_chance: float  # 0.0 to 1.0
    trigger_conditions: List[str]
    animation: str
    sound: Optional[str]
    dialogue: List[str]


@dataclass
class Preference:
    """A duck's preference for something."""
    preference_type: PreferenceType
    value: str
    strength: int  # 1-10, how strong the preference is
    discovered: bool = False
    discovery_date: Optional[str] = None


@dataclass
class HiddenTrait:
    """A hidden trait that gets revealed over time."""
    trait_id: str
    name: str
    description: str
    discovery_condition: str
    discovery_progress: float = 0.0  # 0.0 to 1.0
    is_discovered: bool = False
    discovery_date: Optional[str] = None


# Extended trait definitions
EXTENDED_TRAITS = {
    # Emotional traits
    "emotional_depth": TraitInfo(
        trait_id="emotional_depth",
        name="Emotional Depth",
        category=TraitCategory.CORE,
        description="How deeply the duck feels emotions",
        positive_effects={"mood_intensity": 0.5, "bond_growth": 0.3},
        negative_effects={"mood_swing_chance": 0.4},
        animation_modifiers={"emotional": "exaggerated"},
        dialogue_modifiers=["more emotional words", "deeper reactions"],
    ),
    "optimism": TraitInfo(
        trait_id="optimism",
        name="Optimism",
        category=TraitCategory.CORE,
        description="Tendency to see the bright side",
        positive_effects={"mood_recovery": 0.4, "happy_event_bonus": 0.3},
        negative_effects={"ignores_problems": 0.2},
        animation_modifiers={"idle": "bouncy"},
        dialogue_modifiers=["positive spin", "hopeful outlook"],
    ),
    "curiosity": TraitInfo(
        trait_id="curiosity",
        name="Curiosity",
        category=TraitCategory.CORE,
        description="Interest in exploring and discovering",
        positive_effects={"discovery_chance": 0.5, "learning_speed": 0.3},
        negative_effects={"restlessness": 0.3},
        animation_modifiers={"look": "inquisitive"},
        dialogue_modifiers=["asks questions", "wonders aloud"],
    ),
    "stubbornness": TraitInfo(
        trait_id="stubbornness",
        name="Stubbornness",
        category=TraitCategory.CORE,
        description="Resistance to change and persistence",
        positive_effects={"focus_duration": 0.4, "goal_commitment": 0.5},
        negative_effects={"flexibility": -0.4},
        animation_modifiers={"refuse": "firm"},
        dialogue_modifiers=["insistent", "won't budge"],
    ),
    "playfulness": TraitInfo(
        trait_id="playfulness",
        name="Playfulness",
        category=TraitCategory.CORE,
        description="Love of games and fun",
        positive_effects={"fun_gain": 0.5, "trick_learning": 0.3},
        negative_effects={"seriousness": -0.3},
        animation_modifiers={"idle": "playful"},
        dialogue_modifiers=["jokes", "playful teasing"],
    ),
    "empathy": TraitInfo(
        trait_id="empathy",
        name="Empathy",
        category=TraitCategory.CORE,
        description="Sensitivity to others' feelings",
        positive_effects={"bond_strength": 0.4, "visitor_rapport": 0.5},
        negative_effects={"takes_on_others_moods": 0.3},
        animation_modifiers={"comfort": "gentle"},
        dialogue_modifiers=["understanding", "supportive"],
    ),
    "independence": TraitInfo(
        trait_id="independence",
        name="Independence",
        category=TraitCategory.CORE,
        description="Self-reliance and autonomy",
        positive_effects={"solo_activities": 0.4, "self_care": 0.3},
        negative_effects={"social_need_decay": 0.2},
        animation_modifiers={"alone": "content"},
        dialogue_modifiers=["self-sufficient", "doesn't need help"],
    ),
    "mischief": TraitInfo(
        trait_id="mischief",
        name="Mischief",
        category=TraitCategory.CORE,
        description="Love of pranks and trouble",
        positive_effects={"random_events": 0.5, "surprise_finds": 0.3},
        negative_effects={"mess_creation": 0.4},
        animation_modifiers={"scheme": "sneaky"},
        dialogue_modifiers=["plotting", "innocent act"],
    ),
}

# Quirk definitions
QUIRK_DEFINITIONS = {
    QuirkType.WADDLE_WIGGLE: QuirkInfo(
        quirk_type=QuirkType.WADDLE_WIGGLE,
        name="Waddle Wiggle",
        description="Does a little wiggle while waddling",
        trigger_chance=0.3,
        trigger_conditions=["moving", "happy"],
        animation="wiggle_walk",
        sound="happy_quack",
        dialogue=["*wiggle wiggle*", "*happy waddle noises*"],
    ),
    QuirkType.TIPPY_TAPS: QuirkInfo(
        quirk_type=QuirkType.TIPPY_TAPS,
        name="Tippy Taps",
        description="Does excited tippy taps when happy",
        trigger_chance=0.4,
        trigger_conditions=["excited", "receiving_food"],
        animation="tippy_tap",
        sound="tap_tap",
        dialogue=["*tap tap tap tap*", "*excited feet noises*"],
    ),
    QuirkType.SPIN_BEFORE_SIT: QuirkInfo(
        quirk_type=QuirkType.SPIN_BEFORE_SIT,
        name="Spin Before Sitting",
        description="Spins in a circle before settling down",
        trigger_chance=0.6,
        trigger_conditions=["resting", "sleeping"],
        animation="spin_sit",
        sound=None,
        dialogue=["*spin spin plop*", "*finds the perfect spot*"],
    ),
    QuirkType.BACKWARDS_WALKER: QuirkInfo(
        quirk_type=QuirkType.BACKWARDS_WALKER,
        name="Backwards Walker",
        description="Sometimes walks backwards for no reason",
        trigger_chance=0.1,
        trigger_conditions=["random", "confused"],
        animation="walk_backwards",
        sound=None,
        dialogue=["*walks backwards mysteriously*", "*reverse!*"],
    ),
    QuirkType.MELODIC_QUACK: QuirkInfo(
        quirk_type=QuirkType.MELODIC_QUACK,
        name="Melodic Quacker",
        description="Quacks in musical patterns",
        trigger_chance=0.5,
        trigger_conditions=["quacking", "happy"],
        animation="musical_quack",
        sound="melodic_quack",
        dialogue=["*quack quack quaaa~ck*", "♪ Quack quack ♪"],
    ),
    QuirkType.WHISPER_QUACK: QuirkInfo(
        quirk_type=QuirkType.WHISPER_QUACK,
        name="Whisper Quacker",
        description="Sometimes quacks very quietly",
        trigger_chance=0.3,
        trigger_conditions=["shy", "secretive"],
        animation="soft_quack",
        sound="whisper_quack",
        dialogue=["*quiet quack*", "...quack..."],
    ),
    QuirkType.DOUBLE_QUACK: QuirkInfo(
        quirk_type=QuirkType.DOUBLE_QUACK,
        name="Double Quacker",
        description="Always quacks twice in a row",
        trigger_chance=0.7,
        trigger_conditions=["quacking"],
        animation="double_quack",
        sound="double_quack",
        dialogue=["Quack quack!", "QUACK QUACK!"],
    ),
    QuirkType.HONK_INSTEAD: QuirkInfo(
        quirk_type=QuirkType.HONK_INSTEAD,
        name="Honker",
        description="Occasionally honks instead of quacking",
        trigger_chance=0.15,
        trigger_conditions=["quacking", "surprised"],
        animation="honk",
        sound="honk",
        dialogue=["HONK!", "*surprised honk*"],
    ),
    QuirkType.HEAD_TILT: QuirkInfo(
        quirk_type=QuirkType.HEAD_TILT,
        name="Head Tilter",
        description="Tilts head adorably when curious",
        trigger_chance=0.5,
        trigger_conditions=["curious", "listening"],
        animation="head_tilt",
        sound=None,
        dialogue=["*tilts head*", "*curious tilt*"],
    ),
    QuirkType.WING_STRETCH: QuirkInfo(
        quirk_type=QuirkType.WING_STRETCH,
        name="Wing Stretcher",
        description="Stretches wings frequently",
        trigger_chance=0.3,
        trigger_conditions=["idle", "waking"],
        animation="wing_stretch",
        sound=None,
        dialogue=["*big stretch*", "*wing flap stretch*"],
    ),
    QuirkType.TAIL_WAGGLE: QuirkInfo(
        quirk_type=QuirkType.TAIL_WAGGLE,
        name="Tail Waggler",
        description="Waggles tail feathers when happy",
        trigger_chance=0.4,
        trigger_conditions=["happy", "excited"],
        animation="tail_waggle",
        sound=None,
        dialogue=["*waggle waggle*", "*happy tail*"],
    ),
    QuirkType.BLINK_SLOWLY: QuirkInfo(
        quirk_type=QuirkType.BLINK_SLOWLY,
        name="Slow Blinker",
        description="Does slow, affectionate blinks",
        trigger_chance=0.3,
        trigger_conditions=["relaxed", "affectionate"],
        animation="slow_blink",
        sound=None,
        dialogue=["*slow blink of love*", "*affectionate blink*"],
    ),
    QuirkType.FOOD_INSPECTOR: QuirkInfo(
        quirk_type=QuirkType.FOOD_INSPECTOR,
        name="Food Inspector",
        description="Carefully inspects all food before eating",
        trigger_chance=0.6,
        trigger_conditions=["receiving_food"],
        animation="inspect_food",
        sound=None,
        dialogue=["*inspects carefully*", "Hmm, is this fresh?"],
    ),
    QuirkType.CRUMB_COLLECTOR: QuirkInfo(
        quirk_type=QuirkType.CRUMB_COLLECTOR,
        name="Crumb Collector",
        description="Always searches for leftover crumbs",
        trigger_chance=0.4,
        trigger_conditions=["after_eating", "exploring"],
        animation="search_crumbs",
        sound=None,
        dialogue=["*searching for crumbs*", "Any more? Any more?"],
    ),
    QuirkType.NEAT_EATER: QuirkInfo(
        quirk_type=QuirkType.NEAT_EATER,
        name="Neat Eater",
        description="Eats very carefully and tidily",
        trigger_chance=0.7,
        trigger_conditions=["eating"],
        animation="neat_eat",
        sound=None,
        dialogue=["*eats delicately*", "*no mess!*"],
    ),
    QuirkType.FOOD_DANCER: QuirkInfo(
        quirk_type=QuirkType.FOOD_DANCER,
        name="Food Dancer",
        description="Does a happy dance when given food",
        trigger_chance=0.5,
        trigger_conditions=["receiving_food"],
        animation="food_dance",
        sound="excited_quack",
        dialogue=["*food dance!*", "*happy food wiggles*"],
    ),
    QuirkType.GIFT_GIVER: QuirkInfo(
        quirk_type=QuirkType.GIFT_GIVER,
        name="Gift Giver",
        description="Likes to bring small gifts",
        trigger_chance=0.2,
        trigger_conditions=["happy", "bonded"],
        animation="offer_gift",
        sound="proud_quack",
        dialogue=["*brings you a gift*", "I found this for you!"],
    ),
    QuirkType.PERSONAL_SPACE: QuirkInfo(
        quirk_type=QuirkType.PERSONAL_SPACE,
        name="Personal Space Respecter",
        description="Maintains polite distance",
        trigger_chance=0.5,
        trigger_conditions=["social"],
        animation="step_back",
        sound=None,
        dialogue=["*keeps respectful distance*", "*gives you space*"],
    ),
    QuirkType.CUDDLE_BUG: QuirkInfo(
        quirk_type=QuirkType.CUDDLE_BUG,
        name="Cuddle Bug",
        description="Loves to snuggle up close",
        trigger_chance=0.5,
        trigger_conditions=["relaxed", "affectionate"],
        animation="snuggle",
        sound="content_quack",
        dialogue=["*snuggles close*", "*cuddle time!*"],
    ),
    QuirkType.SHOW_OFF: QuirkInfo(
        quirk_type=QuirkType.SHOW_OFF,
        name="Show Off",
        description="Likes to display feathers and skills",
        trigger_chance=0.4,
        trigger_conditions=["proud", "social"],
        animation="strut",
        sound="proud_quack",
        dialogue=["*struts proudly*", "Look at me!"],
    ),
    QuirkType.NIGHT_OWL: QuirkInfo(
        quirk_type=QuirkType.NIGHT_OWL,
        name="Night Owl",
        description="More active at night",
        trigger_chance=0.6,
        trigger_conditions=["night_time"],
        animation="alert_night",
        sound=None,
        dialogue=["*perks up at night*", "Night time is the best time!"],
    ),
    QuirkType.EARLY_BIRD: QuirkInfo(
        quirk_type=QuirkType.EARLY_BIRD,
        name="Early Bird",
        description="Very energetic in the morning",
        trigger_chance=0.6,
        trigger_conditions=["morning"],
        animation="sunrise_stretch",
        sound="morning_quack",
        dialogue=["*bright and early!*", "Good morning world!"],
    ),
    QuirkType.RAIN_LOVER: QuirkInfo(
        quirk_type=QuirkType.RAIN_LOVER,
        name="Rain Lover",
        description="Extra happy when it rains",
        trigger_chance=0.7,
        trigger_conditions=["rainy"],
        animation="rain_dance",
        sound="happy_quack",
        dialogue=["*splashes happily*", "I love the rain!"],
    ),
    QuirkType.STAR_GAZER: QuirkInfo(
        quirk_type=QuirkType.STAR_GAZER,
        name="Star Gazer",
        description="Loves watching the night sky",
        trigger_chance=0.5,
        trigger_conditions=["night_time", "clear_sky"],
        animation="look_up",
        sound=None,
        dialogue=["*gazes at stars*", "So many stars..."],
    ),
}

# Preference options
PREFERENCE_OPTIONS = {
    PreferenceType.FAVORITE_FOOD: [
        "bread", "seeds", "peas", "corn", "lettuce", "oats",
        "worms", "bugs", "berries", "crackers", "rice", "pasta",
    ],
    PreferenceType.HATED_FOOD: [
        "spicy things", "sour things", "onions", "citrus",
        "moldy bread", "dry crackers",
    ],
    PreferenceType.FAVORITE_WEATHER: [
        "rainy", "sunny", "cloudy", "snowy", "foggy", "stormy",
    ],
    PreferenceType.HATED_WEATHER: [
        "too hot", "too cold", "very windy", "hail",
    ],
    PreferenceType.FAVORITE_ACTIVITY: [
        "swimming", "preening", "exploring", "napping", "eating",
        "playing", "watching clouds", "collecting shiny things",
    ],
    PreferenceType.DISLIKED_ACTIVITY: [
        "baths", "loud noises", "being alone", "exercise",
    ],
    PreferenceType.PREFERRED_TIME: [
        "morning", "afternoon", "evening", "night",
    ],
    PreferenceType.FAVORITE_COLOR: [
        "blue", "green", "yellow", "orange", "purple", "pink",
        "gold", "silver", "rainbow",
    ],
    PreferenceType.FAVORITE_SPOT: [
        "by the window", "in the corner", "near you", "in the middle",
        "somewhere cozy", "up high", "hidden spot",
    ],
}

# Hidden traits
HIDDEN_TRAITS = {
    "secret_genius": HiddenTrait(
        trait_id="secret_genius",
        name="Secret Genius",
        description="Actually incredibly smart, just hides it",
        discovery_condition="Complete 10 puzzles or tricks perfectly",
    ),
    "hidden_bravery": HiddenTrait(
        trait_id="hidden_bravery",
        name="Hidden Bravery",
        description="Brave when it truly matters",
        discovery_condition="Face 5 scary events without hiding",
    ),
    "gentle_soul": HiddenTrait(
        trait_id="gentle_soul",
        name="Gentle Soul",
        description="Exceptionally caring and nurturing",
        discovery_condition="Take care of duck at low health 3 times",
    ),
    "old_soul": HiddenTrait(
        trait_id="old_soul",
        name="Old Soul",
        description="Wise beyond their apparent years",
        discovery_condition="Reach 100 days of age",
    ),
    "lucky_duck": HiddenTrait(
        trait_id="lucky_duck",
        name="Lucky Duck",
        description="Blessed with extraordinary luck",
        discovery_condition="Find 5 legendary items",
    ),
    "dreamer": HiddenTrait(
        trait_id="dreamer",
        name="Dreamer",
        description="Has vivid and prophetic dreams",
        discovery_condition="Observe 20 dream sequences",
    ),
    "guardian": HiddenTrait(
        trait_id="guardian",
        name="Guardian Spirit",
        description="Protects and watches over you",
        discovery_condition="Maintain max bond for 30 days",
    ),
    "adventurer": HiddenTrait(
        trait_id="adventurer",
        name="Born Adventurer",
        description="Has an insatiable wanderlust",
        discovery_condition="Complete 20 exploration events",
    ),
}


class ExtendedPersonalitySystem:
    """Manages the extended personality system."""
    
    def __init__(self):
        # Extended trait values (-100 to +100)
        self.extended_traits: Dict[str, int] = {}
        for trait_id in EXTENDED_TRAITS:
            self.extended_traits[trait_id] = 0
            
        # Quirks (randomly assigned, can discover more)
        self.quirks: List[QuirkType] = []
        
        # Preferences
        self.preferences: Dict[PreferenceType, Preference] = {}
        
        # Hidden traits
        self.hidden_traits: Dict[str, HiddenTrait] = {}
        for trait_id, trait_info in HIDDEN_TRAITS.items():
            self.hidden_traits[trait_id] = HiddenTrait(
                trait_id=trait_info.trait_id,
                name=trait_info.name,
                description=trait_info.description,
                discovery_condition=trait_info.discovery_condition,
            )
            
        # Personality evolution tracking
        self.trait_history: List[Dict] = []
        self.personality_age_days: int = 0
        
    def generate_random(self):
        """Generate a random personality."""
        # Randomize extended traits
        for trait_id in EXTENDED_TRAITS:
            # Normal-ish distribution around 0
            self.extended_traits[trait_id] = random.randint(-60, 60)
            
        # Assign 2-4 random quirks
        num_quirks = random.randint(2, 4)
        all_quirks = list(QuirkType)
        self.quirks = random.sample(all_quirks, num_quirks)
        
        # Generate preferences
        for pref_type in PreferenceType:
            if pref_type in PREFERENCE_OPTIONS:
                options = PREFERENCE_OPTIONS[pref_type]
                value = random.choice(options)
                strength = random.randint(3, 10)
                # Some preferences start discovered, others hidden
                discovered = random.random() < 0.3
                self.preferences[pref_type] = Preference(
                    preference_type=pref_type,
                    value=value,
                    strength=strength,
                    discovered=discovered,
                    discovery_date=datetime.now().isoformat() if discovered else None,
                )
                
    def get_trait_value(self, trait_id: str) -> int:
        """Get an extended trait's value."""
        return self.extended_traits.get(trait_id, 0)
        
    def set_trait_value(self, trait_id: str, value: int):
        """Set an extended trait's value (clamped)."""
        if trait_id in self.extended_traits:
            self.extended_traits[trait_id] = max(-100, min(100, value))
            
    def adjust_trait(self, trait_id: str, delta: int, reason: str = ""):
        """Adjust a trait and record the change."""
        if trait_id not in self.extended_traits:
            return
            
        old_value = self.extended_traits[trait_id]
        self.set_trait_value(trait_id, old_value + delta)
        new_value = self.extended_traits[trait_id]
        
        if old_value != new_value:
            self.trait_history.append({
                "trait": trait_id,
                "old_value": old_value,
                "new_value": new_value,
                "delta": new_value - old_value,
                "reason": reason,
                "date": datetime.now().isoformat(),
            })
            
    def has_quirk(self, quirk: QuirkType) -> bool:
        """Check if duck has a quirk."""
        return quirk in self.quirks
        
    def add_quirk(self, quirk: QuirkType):
        """Add a quirk if not already present."""
        if quirk not in self.quirks:
            self.quirks.append(quirk)
            
    def get_quirk_info(self, quirk: QuirkType) -> Optional[QuirkInfo]:
        """Get information about a quirk."""
        return QUIRK_DEFINITIONS.get(quirk)
        
    def check_quirk_trigger(self, condition: str) -> List[Tuple[QuirkType, QuirkInfo]]:
        """Check which quirks should trigger for a condition."""
        triggered = []
        for quirk in self.quirks:
            info = QUIRK_DEFINITIONS.get(quirk)
            if info and condition in info.trigger_conditions:
                if random.random() < info.trigger_chance:
                    triggered.append((quirk, info))
        return triggered
        
    def get_preference(self, pref_type: PreferenceType) -> Optional[Preference]:
        """Get a preference value."""
        return self.preferences.get(pref_type)
        
    def discover_preference(self, pref_type: PreferenceType):
        """Mark a preference as discovered."""
        if pref_type in self.preferences:
            pref = self.preferences[pref_type]
            if not pref.discovered:
                pref.discovered = True
                pref.discovery_date = datetime.now().isoformat()
                
    def get_discovered_preferences(self) -> List[Preference]:
        """Get all discovered preferences."""
        return [p for p in self.preferences.values() if p.discovered]
        
    def update_hidden_trait_progress(self, trait_id: str, progress: float):
        """Update progress toward discovering a hidden trait."""
        if trait_id not in self.hidden_traits:
            return
            
        trait = self.hidden_traits[trait_id]
        if trait.is_discovered:
            return
            
        trait.discovery_progress = min(1.0, trait.discovery_progress + progress)
        
        if trait.discovery_progress >= 1.0:
            trait.is_discovered = True
            trait.discovery_date = datetime.now().isoformat()
            
    def get_discovered_hidden_traits(self) -> List[HiddenTrait]:
        """Get all discovered hidden traits."""
        return [t for t in self.hidden_traits.values() if t.is_discovered]
        
    def get_personality_summary(self) -> str:
        """Get a text summary of the personality."""
        lines = []
        
        # Dominant traits
        dominant = []
        for trait_id, value in self.extended_traits.items():
            if abs(value) >= 40:
                info = EXTENDED_TRAITS[trait_id]
                if value > 0:
                    dominant.append(f"Very {info.name.lower()}")
                else:
                    dominant.append(f"Low {info.name.lower()}")
                    
        if dominant:
            lines.append("Dominant traits: " + ", ".join(dominant))
            
        # Quirks
        if self.quirks:
            quirk_names = [QUIRK_DEFINITIONS[q].name for q in self.quirks]
            lines.append("Quirks: " + ", ".join(quirk_names))
            
        # Discovered preferences
        discovered_prefs = self.get_discovered_preferences()
        if discovered_prefs:
            pref_strs = []
            for pref in discovered_prefs:
                pref_strs.append(f"{pref.preference_type.value}: {pref.value}")
            lines.append("Known preferences: " + ", ".join(pref_strs[:3]))
            
        return "\n".join(lines) if lines else "A mysterious duck..."
        
    def get_behavior_modifiers(self) -> Dict[str, float]:
        """Get all behavior modifiers from traits and quirks."""
        modifiers = {}
        
        # Apply trait effects
        for trait_id, value in self.extended_traits.items():
            if trait_id not in EXTENDED_TRAITS:
                continue
                
            info = EXTENDED_TRAITS[trait_id]
            multiplier = value / 100.0  # -1.0 to +1.0
            
            if value > 0:
                for effect, strength in info.positive_effects.items():
                    modifiers[effect] = modifiers.get(effect, 0) + (strength * multiplier)
            else:
                for effect, strength in info.negative_effects.items():
                    modifiers[effect] = modifiers.get(effect, 0) + (strength * abs(multiplier))
                    
        return modifiers
        
    def age_personality(self, days: int = 1):
        """Age the personality, potentially shifting traits."""
        self.personality_age_days += days
        
        # Traits can slowly drift over time
        for trait_id in self.extended_traits:
            # Small random drift toward center (stability)
            current = self.extended_traits[trait_id]
            if abs(current) > 20:
                drift = -1 if current > 0 else 1
                if random.random() < 0.1:  # 10% chance per day
                    self.extended_traits[trait_id] += drift
                    
    def render_personality_card(self, width: int = 60) -> List[str]:
        """Render a personality card display."""
        lines = []
        
        lines.append("╔" + "═" * (width - 2) + "╗")
        lines.append("║" + " 🦆 Personality Profile 🦆 ".center(width - 2) + "║")
        lines.append("╠" + "═" * (width - 2) + "╣")
        
        # Extended traits
        lines.append("║" + " Core Traits: ".ljust(width - 2) + "║")
        
        for trait_id, value in self.extended_traits.items():
            if trait_id not in EXTENDED_TRAITS:
                continue
                
            info = EXTENDED_TRAITS[trait_id]
            bar_width = 20
            bar_pos = int((value + 100) / 200 * bar_width)
            bar = "─" * bar_pos + "●" + "─" * (bar_width - bar_pos - 1)
            
            trait_line = f"  {info.name}: [{bar}]"
            lines.append("║" + trait_line[:width-3].ljust(width - 2) + "║")
            
        lines.append("╠" + "─" * (width - 2) + "╣")
        
        # Quirks
        lines.append("║" + " Quirks: ".ljust(width - 2) + "║")
        for quirk in self.quirks[:4]:  # Show up to 4
            info = QUIRK_DEFINITIONS.get(quirk)
            if info:
                lines.append("║" + f"  • {info.name}: {info.description}"[:width-3].ljust(width - 2) + "║")
                
        lines.append("╠" + "─" * (width - 2) + "╣")
        
        # Discovered preferences
        discovered = self.get_discovered_preferences()
        if discovered:
            lines.append("║" + " Known Preferences: ".ljust(width - 2) + "║")
            for pref in discovered[:4]:
                pref_name = pref.preference_type.value.replace("_", " ").title()
                lines.append("║" + f"  • {pref_name}: {pref.value}"[:width-3].ljust(width - 2) + "║")
        else:
            lines.append("║" + " Preferences: (Not yet discovered) ".ljust(width - 2) + "║")
            
        lines.append("╠" + "─" * (width - 2) + "╣")
        
        # Hidden traits
        discovered_hidden = self.get_discovered_hidden_traits()
        in_progress = [t for t in self.hidden_traits.values() 
                       if not t.is_discovered and t.discovery_progress > 0]
        
        lines.append("║" + " Hidden Traits: ".ljust(width - 2) + "║")
        if discovered_hidden:
            for trait in discovered_hidden:
                lines.append("║" + f"  ✨ {trait.name}"[:width-3].ljust(width - 2) + "║")
        if in_progress:
            lines.append("║" + f"  (+ {len(in_progress)} being discovered...)"[:width-3].ljust(width - 2) + "║")
        if not discovered_hidden and not in_progress:
            lines.append("║" + "  (Discover through gameplay)"[:width-3].ljust(width - 2) + "║")
            
        lines.append("╚" + "═" * (width - 2) + "╝")
        
        return lines
        
    def to_dict(self) -> Dict:
        """Serialize to dictionary."""
        return {
            "extended_traits": self.extended_traits,
            "quirks": [q.value for q in self.quirks],
            "preferences": {
                pt.value: {
                    "value": p.value,
                    "strength": p.strength,
                    "discovered": p.discovered,
                    "discovery_date": p.discovery_date,
                }
                for pt, p in self.preferences.items()
            },
            "hidden_traits": {
                tid: {
                    "discovery_progress": t.discovery_progress,
                    "is_discovered": t.is_discovered,
                    "discovery_date": t.discovery_date,
                }
                for tid, t in self.hidden_traits.items()
            },
            "trait_history": self.trait_history[-100:],  # Keep last 100
            "personality_age_days": self.personality_age_days,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "ExtendedPersonalitySystem":
        """Deserialize from dictionary."""
        system = cls()
        system.extended_traits = data.get("extended_traits", {})
        
        # Ensure all traits exist
        for trait_id in EXTENDED_TRAITS:
            if trait_id not in system.extended_traits:
                system.extended_traits[trait_id] = 0
                
        system.quirks = [QuirkType(q) for q in data.get("quirks", [])]
        
        system.preferences = {}
        for pt_str, p_data in data.get("preferences", {}).items():
            try:
                pt = PreferenceType(pt_str)
                system.preferences[pt] = Preference(
                    preference_type=pt,
                    value=p_data["value"],
                    strength=p_data["strength"],
                    discovered=p_data["discovered"],
                    discovery_date=p_data.get("discovery_date"),
                )
            except ValueError:
                pass
                
        for tid, t_data in data.get("hidden_traits", {}).items():
            if tid in system.hidden_traits:
                system.hidden_traits[tid].discovery_progress = t_data.get("discovery_progress", 0)
                system.hidden_traits[tid].is_discovered = t_data.get("is_discovered", False)
                system.hidden_traits[tid].discovery_date = t_data.get("discovery_date")
                
        system.trait_history = data.get("trait_history", [])
        system.personality_age_days = data.get("personality_age_days", 0)
        return system


# Global instance
extended_personality = ExtendedPersonalitySystem()
