"""
Event system - random and scheduled events that happen to the duck.
Animal Crossing-style special days and seasonal events included.
"""
import random
import time
from typing import Dict, List, Optional, Callable, TYPE_CHECKING
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

if TYPE_CHECKING:
    from duck.duck import Duck

# Simple growth stages in order (matching config.py)
SIMPLE_GROWTH_STAGES = ["egg", "duckling", "teen", "adult", "elder"]


class EventType(Enum):
    """Types of events."""
    RANDOM = "random"       # Can happen anytime
    SCHEDULED = "scheduled" # Happens at specific times
    TRIGGERED = "triggered" # Happens based on conditions
    WEATHER = "weather"     # Weather changes
    VISITOR = "visitor"     # Someone visits
    SPECIAL_DAY = "special_day"  # Holiday/special occasion
    SOCIAL = "social"       # Social interactions with other animals
    SEASONAL = "seasonal"   # Season-specific events
    DISCOVERY = "discovery" # Rare discovery events


@dataclass
class Event:
    """An event that can occur."""
    id: str
    name: str
    description: str
    event_type: EventType
    probability: float  # 0.0 to 1.0 for random events
    effects: Dict[str, float]  # need changes
    mood_change: int  # temporary mood modifier
    message: str  # message to display
    duck_reaction: str  # how duck reacts
    sound: Optional[str] = None
    requires_stage: Optional[str] = None  # minimum growth stage
    cooldown: float = 300  # seconds before can happen again
    has_animation: bool = True  # whether this event has a visual animation
    weather_group: Optional[str] = None  # Required weather group (hot/cold/wet/harsh/pleasant/magical)
    chain_id: Optional[str] = None  # If set, this event starts an event chain
    encounter_id: Optional[str] = None  # If set, starts an encounter requiring player action


@dataclass
class Encounter:
    """A negative encounter the player can help resolve.
    
    When triggered, the duck is in trouble. If the player performs the
    required action within the time window, positive outcome. Otherwise,
    negative outcome persists. Gives the player meaningful agency.
    """
    id: str
    name: str
    trigger_message: str       # What the duck says when encounter starts
    help_action: str           # Action the player must do ("pet", "play", "feed", "clean")
    help_message: str          # What the duck says when helped
    ignore_message: str        # What the duck says if player doesn't help in time
    help_effects: Dict[str, float]  # Effects if player helps
    ignore_effects: Dict[str, float]  # Effects if player ignores
    help_trust_bonus: float = 1.0    # Trust bonus for helping
    time_window: float = 120.0       # Seconds player has to respond
    cooldown: float = 3600.0         # Seconds before this encounter can repeat


# ── Encounters (player choice matters) ──────────────────────────────────
ENCOUNTERS: Dict[str, Encounter] = {
    "predator_shadow": Encounter(
        id="predator_shadow",
        name="Shadow Overhead",
        trigger_message="*freezes* ...Something big just flew overhead. I'm fine. I'm definitely fine. "
                        "(Pet me. NOW. I mean... if you want.)",
        help_action="pet",
        help_message="*unclenches* ...You scared it off. Good. I wasn't scared. I was being TACTICAL. "
                     "But... thanks. Or whatever.",
        ignore_message="*slowly unfreezes* ...It's gone. No thanks to you. "
                       "I handled it. Alone. As USUAL.",
        help_effects={"fun": 5, "social": 10},
        ignore_effects={"fun": -10, "energy": -8, "social": -5},
        help_trust_bonus=2.0,
        time_window=90.0,
    ),
    "stuck_in_mud": Encounter(
        id="stuck_in_mud",
        name="Stuck!",
        trigger_message="*struggles* ...I appear to be... embedded. In mud. This is fine. "
                        "Everything is fine. (Clean me. Please. I said please.)",
        help_action="clean",
        help_message="*freed* ...Dignity: compromised. Feathers: disgusting. But at least I'm unstuck. "
                     "You saw nothing.",
        ignore_message="*eventually wiggles free* ...Took me twenty minutes. I counted. "
                       "You were RIGHT THERE.",
        help_effects={"cleanliness": 15, "fun": 5},
        ignore_effects={"cleanliness": -20, "energy": -15, "fun": -10},
        help_trust_bonus=1.5,
        time_window=120.0,
    ),
    "hungry_bully": Encounter(
        id="hungry_bully",
        name="Food Thief",
        trigger_message="*alarm* A pigeon is trying to steal my food stash! The AUDACITY! "
                        "(Feed me something. Quick. Before that feathered criminal takes everything.)",
        help_action="feed",
        help_message="*munches defiantly* HA! Shared my food? Never. This is MY food now. "
                     "The pigeon can have nothing. Thanks for the backup.",
        ignore_message="*watches food disappear* ...The pigeon took it. All of it. "
                       "While you watched. I'll remember this.",
        help_effects={"hunger": 20, "fun": 5},
        ignore_effects={"hunger": -15, "fun": -10},
        help_trust_bonus=1.5,
        time_window=90.0,
    ),
    "bored_crisis": Encounter(
        id="bored_crisis",
        name="Existential Boredom",
        trigger_message="*lies flat* ...I've run out of things to think about. All thoughts: exhausted. "
                        "I've thought every thought. Play with me before I start thinking about thinking.",
        help_action="play",
        help_message="*perks up* ...Okay. That was acceptable entertainment. The void has receded. "
                     "Temporarily. Don't let it happen again.",
        ignore_message="*remains flat* ...I waited. The void didn't recede. "
                       "It's fine. I've made friends with it now. The void and I have an understanding.",
        help_effects={"fun": 20, "energy": 5},
        ignore_effects={"fun": -15, "social": -10},
        help_trust_bonus=1.0,
        time_window=120.0,
    ),
}


@dataclass
class EventChain:
    """A multi-stage event that unfolds over time."""
    id: str
    stages: List[Event]
    min_seconds_between: float = 30.0  # Minimum seconds between stages
    cooldown: float = 7200.0  # 2 hours before chain can repeat
    requires_stage: Optional[str] = None


# Event definitions
EVENTS = {
    # Random positive events
    "found_crumb": Event(
        id="found_crumb",
        name="Found a Crumb",
        description="The duck found a tasty crumb!",
        event_type=EventType.RANDOM,
        probability=0.05,
        effects={"hunger": 5},
        mood_change=5,
        message="*finds a crumb* MINE. Don't even look at it.",
        duck_reaction="excited",
        sound="eat",
        has_animation=True,
    ),
    "nice_breeze": Event(
        id="nice_breeze",
        name="Nice Breeze",
        description="A pleasant breeze ruffles the duck's feathers.",
        event_type=EventType.RANDOM,
        probability=0.03,
        effects={"fun": 5},
        mood_change=3,
        message="*feathers rustle* ...Okay, that's actually nice.",
        duck_reaction="content",
        has_animation=True,
    ),
    "butterfly": Event(
        id="butterfly",
        name="Butterfly Visit",
        description="A butterfly flutters by!",
        event_type=EventType.RANDOM,
        probability=0.02,
        effects={"fun": 10},
        mood_change=8,
        message="*watches butterfly* ...I could catch it. If I WANTED to.",
        duck_reaction="curious",
        has_animation=True,
    ),
    "found_shiny": Event(
        id="found_shiny",
        name="Found Something Shiny",
        description="The duck found something shiny!",
        event_type=EventType.RANDOM,
        probability=0.01,
        effects={"fun": 15},
        mood_change=10,
        message="*finds shiny thing* TREASURE! This is MINE now!",
        duck_reaction="ecstatic",
        sound="alert",
        has_animation=True,
    ),
    "shiny_pebble": Event(
        id="shiny_pebble",
        name="Smooth Pebble",
        description="The duck found a perfectly smooth pebble.",
        event_type=EventType.RANDOM,
        probability=0.03,
        effects={"fun": 8},
        mood_change=5,
        message="*picks up pebble* Smooth. Round. Perfect. This is the best rock I've ever met.",
        duck_reaction="pleased",
        has_animation=True,
    ),
    "lost_coin": Event(
        id="lost_coin",
        name="Lost Coin",
        description="A human dropped a coin nearby.",
        event_type=EventType.RANDOM,
        probability=0.02,
        effects={"fun": 12},
        mood_change=7,
        message="*finds coin* The humans dropped this. Their loss. My shiny circle now.",
        duck_reaction="excited",
        has_animation=True,
    ),
    "forgotten_bread": Event(
        id="forgotten_bread",
        name="Forgotten Bread",
        description="Someone left bread on a bench.",
        event_type=EventType.RANDOM,
        probability=0.015,
        effects={"hunger": 15, "fun": 10},
        mood_change=12,
        message="*vibrating* ...Bread. Unattended bread. On a BENCH. The universe provides. I am BLESSED.",
        duck_reaction="ecstatic",
        sound="eat",
        has_animation=True,
    ),
    "friendly_frog": Event(
        id="friendly_frog",
        name="Friendly Frog",
        description="A frog croaks a greeting from the pond edge.",
        event_type=EventType.RANDOM,
        probability=0.02,
        effects={"social": 8, "fun": 5},
        mood_change=5,
        message="*nods at frog* ...Sup. You're green. I respect that commitment.",
        duck_reaction="friendly",
        has_animation=True,
    ),
    "visiting_ladybug": Event(
        id="visiting_ladybug",
        name="Ladybug Landing",
        description="A ladybug lands on the duck's head.",
        event_type=EventType.RANDOM,
        probability=0.02,
        effects={"fun": 8, "social": 3},
        mood_change=6,
        message="*holds very still* There's a bug on my head. It has spots. We're friends now. It didn't agree to this.",
        duck_reaction="gentle",
        has_animation=True,
    ),
    "rainbow_sighting": Event(
        id="rainbow_sighting",
        name="Rainbow Sighting",
        description="A rainbow appears in the distance.",
        event_type=EventType.RANDOM,
        probability=0.01,
        effects={"fun": 12},
        mood_change=8,
        message="*looks up* ...Colors. In the sky. Unauthorized colors. I'll allow it this once.",
        duck_reaction="awed",
        has_animation=True,
    ),
    "perfect_puddle": Event(
        id="perfect_puddle",
        name="Perfect Puddle",
        description="A puddle of ideal depth and temperature.",
        event_type=EventType.RANDOM,
        probability=0.02,
        effects={"fun": 10, "cleanliness": 5},
        mood_change=8,
        message="*sits in puddle* ...This puddle understands me. The depth. The temperature. Flawless.",
        duck_reaction="content",
        sound="splash",
        has_animation=True,
    ),
    "warm_sunbeam": Event(
        id="warm_sunbeam",
        name="Warm Sunbeam",
        description="A warm sunbeam hits just right.",
        event_type=EventType.RANDOM,
        probability=0.03,
        effects={"energy": 5, "fun": 5},
        mood_change=6,
        message="*melts into sunbeam* ...The sun targeted me specifically. I'm the chosen one. Obviously.",
        duck_reaction="content",
        has_animation=True,
    ),
    "dandelion_fluff": Event(
        id="dandelion_fluff",
        name="Dandelion Fluff",
        description="Dandelion seeds float past on the breeze.",
        event_type=EventType.RANDOM,
        probability=0.03,
        effects={"fun": 6},
        mood_change=4,
        message="*watches seeds float* ...Free-range plant confetti. Didn't ask for a show. Not complaining.",
        duck_reaction="calm",
        has_animation=True,
    ),
    "lucky_clover": Event(
        id="lucky_clover",
        name="Four-Leaf Clover",
        description="The duck found a rare four-leaf clover!",
        event_type=EventType.RANDOM,
        probability=0.005,
        effects={"fun": 18},
        mood_change=12,
        message="*examines clover* Four leaves. The normal ones have three. I found the overachiever. MINE.",
        duck_reaction="excited",
        sound="alert",
        has_animation=True,
    ),

    # Random neutral events
    "random_quack": Event(
        id="random_quack",
        name="Random Quack",
        description="The duck quacks for no reason.",
        event_type=EventType.RANDOM,
        probability=0.08,
        effects={},
        mood_change=0,
        message="QUACK! ...That was on PURPOSE. Obviously.",
        duck_reaction="confused",
        sound="quack",
    ),
    "forgot_something": Event(
        id="forgot_something",
        name="Forgot Something",
        description="The duck forgot what it was doing.",
        event_type=EventType.RANDOM,
        probability=0.04,
        effects={},
        mood_change=0,
        message="*stops* ...I wasn't doing ANYTHING. Mind your business.",
        duck_reaction="confused",
    ),
    "stare_contest": Event(
        id="stare_contest",
        name="Staring Contest",
        description="The duck has a staring contest with nothing.",
        event_type=EventType.RANDOM,
        probability=0.03,
        effects={},
        mood_change=2,
        message="*intense staring at wall* ...The wall blinked. I WIN.",
        duck_reaction="proud",
    ),
    "leaf_falling": Event(
        id="leaf_falling",
        name="Falling Leaf",
        description="A single leaf drifts down from a tree.",
        event_type=EventType.RANDOM,
        probability=0.04,
        effects={},
        mood_change=1,
        message="*watches leaf fall* ...Took its time. Committed to the descent. I respect that.",
        duck_reaction="observant",
    ),
    "cloud_shapes": Event(
        id="cloud_shapes",
        name="Cloud Shapes",
        description="The duck stares at the clouds.",
        event_type=EventType.RANDOM,
        probability=0.04,
        effects={},
        mood_change=2,
        message="*looks up* That cloud looks like bread. That one too. They all look like bread. Might be hungry.",
        duck_reaction="thoughtful",
    ),
    "ant_parade": Event(
        id="ant_parade",
        name="Ant Parade",
        description="A line of ants marches past the duck.",
        event_type=EventType.RANDOM,
        probability=0.03,
        effects={},
        mood_change=1,
        message="*watches ants* ...They're organized. They have purpose. I have questions. They're ignoring me.",
        duck_reaction="curious",
    ),
    "feather_molt": Event(
        id="feather_molt",
        name="Feather Molt",
        description="The duck lost a feather.",
        event_type=EventType.RANDOM,
        probability=0.03,
        effects={"cleanliness": -3},
        mood_change=0,
        message="*feather falls off* ...Goodbye, feather. You served adequately. There are others.",
        duck_reaction="indifferent",
    ),
    "itchy_spot": Event(
        id="itchy_spot",
        name="Itchy Spot",
        description="The duck has an itch it can't quite reach.",
        event_type=EventType.RANDOM,
        probability=0.04,
        effects={},
        mood_change=-1,
        message="*contorts* There's an itch. Right THERE. No. There. No. THERE. ...It moved.",
        duck_reaction="frustrated",
    ),
    "deep_thought": Event(
        id="deep_thought",
        name="Deep Thought",
        description="The duck has a moment of philosophical reflection.",
        event_type=EventType.RANDOM,
        probability=0.03,
        effects={},
        mood_change=1,
        message="*stares into distance* ...If a duck quacks and no one is around, is it still annoying. Yes. The answer is yes.",
        duck_reaction="philosophical",
    ),
    "shadow_watching": Event(
        id="shadow_watching",
        name="Shadow Watching",
        description="The duck notices its own shadow.",
        event_type=EventType.RANDOM,
        probability=0.03,
        effects={},
        mood_change=0,
        message="*stares at shadow* ...It copies everything I do. Flattering but also creepy. I'm watching you, shadow.",
        duck_reaction="suspicious",
    ),

    # Random negative events
    "loud_noise": Event(
        id="loud_noise",
        name="Loud Noise",
        description="A loud noise startled the duck!",
        event_type=EventType.RANDOM,
        probability=0.02,
        effects={"fun": -5},
        mood_change=-5,
        message="*STARTLED* WHO DID THAT?! Show yourself, COWARD!",
        duck_reaction="scared",
        sound="alert",
        has_animation=True,
    ),
    "stubbed_toe": Event(
        id="stubbed_toe",
        name="Stubbed Toe",
        description="The duck stubbed its toe.",
        event_type=EventType.RANDOM,
        probability=0.02,
        effects={"fun": -3},
        mood_change=-3,
        message="*trips* ...That was the FLOOR'S fault!",
        duck_reaction="hurt",
    ),
    "bad_dream": Event(
        id="bad_dream",
        name="Bad Dream",
        description="The duck had a bad dream.",
        event_type=EventType.RANDOM,
        probability=0.01,
        effects={"energy": -5},
        mood_change=-8,
        message="*wakes up startled* ...Whatever. It wasn't scary.",
        duck_reaction="scared",
        has_animation=True,
    ),
    "stepped_in_gum": Event(
        id="stepped_in_gum",
        name="Stepped in Gum",
        description="The duck stepped in something sticky.",
        event_type=EventType.RANDOM,
        probability=0.02,
        effects={"fun": -5, "cleanliness": -8},
        mood_change=-5,
        message="*lifts foot* ...Sticky. My foot is HOSTAGE. Who leaves gum on the ground. CRIMINALS.",
        duck_reaction="disgusted",
    ),
    "startled_by_splash": Event(
        id="startled_by_splash",
        name="Unexpected Splash",
        description="Something splashed near the duck.",
        event_type=EventType.RANDOM,
        probability=0.02,
        effects={"fun": -3, "cleanliness": -5},
        mood_change=-4,
        message="*drenched* ...I'm wet now. I didn't authorize this. Someone WILL answer for this.",
        duck_reaction="annoyed",
    ),
    "too_warm": Event(
        id="too_warm",
        name="Too Warm",
        description="It's uncomfortably warm.",
        event_type=EventType.RANDOM,
        probability=0.02,
        effects={"energy": -5},
        mood_change=-4,
        message="*panting* I'm melting. Slowly. This is how it ends. By evaporation.",
        duck_reaction="miserable",
    ),
    "too_chilly": Event(
        id="too_chilly",
        name="Too Chilly",
        description="There's a chill in the air.",
        event_type=EventType.RANDOM,
        probability=0.02,
        effects={"energy": -4},
        mood_change=-3,
        message="*puffs up feathers* Cold. My feathers are doing their BEST. It's not enough.",
        duck_reaction="grumpy",
    ),
    "fish_stare_off": Event(
        id="fish_stare_off",
        name="Fish Standoff",
        description="A fish stares at the duck from the water.",
        event_type=EventType.RANDOM,
        probability=0.02,
        effects={"fun": -3},
        mood_change=-2,
        message="*locks eyes with fish* ...It's been four minutes. The fish won't blink. I can't blink. I'VE COMMITTED.",
        duck_reaction="tense",
    ),
    "pigeon_judgement": Event(
        id="pigeon_judgement",
        name="Pigeon Judgement",
        description="A pigeon gives the duck a judgemental look.",
        event_type=EventType.RANDOM,
        probability=0.02,
        effects={"social": -5},
        mood_change=-4,
        message="*bristles* That pigeon just LOOKED at me. With JUDGEMENT. I am being EVALUATED by a pigeon.",
        duck_reaction="offended",
        has_animation=True,
    ),
    "bug_in_face": Event(
        id="bug_in_face",
        name="Bug Collision",
        description="A bug flew right into the duck's face.",
        event_type=EventType.RANDOM,
        probability=0.03,
        effects={"fun": -4},
        mood_change=-3,
        message="*sputters* A BUG. In my FACE. It had the whole sky. THE WHOLE SKY. And it chose my face.",
        duck_reaction="shocked",
    ),

    # Weather events
    "sunny": Event(
        id="sunny",
        name="Sunny Day",
        description="It's a beautiful sunny day!",
        event_type=EventType.WEATHER,
        probability=0.01,
        effects={"fun": 5},
        mood_change=5,
        message="*basks in sunlight* Finally, some GOOD weather.",
        duck_reaction="happy",
        cooldown=1800,
    ),
    "rain": Event(
        id="rain",
        name="Rain",
        description="It's raining!",
        event_type=EventType.WEATHER,
        probability=0.01,
        effects={"cleanliness": 10, "fun": 5},
        mood_change=3,
        message="*plays in rain* FREE bath! Take THAT, hygiene police!",
        duck_reaction="playful",
        sound="splash",
        cooldown=1800,
    ),

    # Weather-conditional events (only fire when the matching weather group is active)
    "heat_nap": Event(
        id="heat_nap",
        name="Heat Nap",
        description="The heat makes the duck drowsy.",
        event_type=EventType.WEATHER,
        probability=0.03,
        effects={"energy": -8},
        mood_change=-3,
        message="*droops* It's too hot to exist. I'm going horizontal.",
        duck_reaction="sleepy",
        cooldown=1200,
        weather_group="hot",
    ),
    "cool_puddle": Event(
        id="cool_puddle",
        name="Cool Puddle",
        description="Found a refreshing puddle!",
        event_type=EventType.WEATHER,
        probability=0.03,
        effects={"energy": 8, "cleanliness": 5},
        mood_change=5,
        message="*sits in puddle* ...This is fine. This is my puddle now. No one else's.",
        duck_reaction="content",
        sound="splash",
        cooldown=1200,
        weather_group="hot",
    ),
    "frozen_beak": Event(
        id="frozen_beak",
        name="Frozen Beak",
        description="The cold nips at the duck's beak.",
        event_type=EventType.WEATHER,
        probability=0.03,
        effects={"hunger": -5, "energy": -3},
        mood_change=-4,
        message="*beak chattering* My beak just tried to leave my face. Rude.",
        duck_reaction="annoyed",
        cooldown=1200,
        weather_group="cold",
    ),
    "snow_discovery": Event(
        id="snow_discovery",
        name="Snow Discovery",
        description="The duck discovers something in the snow!",
        event_type=EventType.WEATHER,
        probability=0.02,
        effects={"fun": 10},
        mood_change=6,
        message="*digs in snow* Found something shiny! ...It's ice. But it's MY ice.",
        duck_reaction="excited",
        cooldown=1800,
        weather_group="cold",
    ),
    "mud_splash": Event(
        id="mud_splash",
        name="Mud Splash",
        description="The rain made a perfect mud puddle.",
        event_type=EventType.WEATHER,
        probability=0.03,
        effects={"fun": 8, "cleanliness": -15},
        mood_change=4,
        message="*cannon-ducks into mud* WORTH IT. Every. Single. Time.",
        duck_reaction="playful",
        sound="splash",
        cooldown=1200,
        weather_group="wet",
    ),
    "worm_surface": Event(
        id="worm_surface",
        name="Worm Surfacing",
        description="The rain brought worms to the surface!",
        event_type=EventType.WEATHER,
        probability=0.02,
        effects={"hunger": 12},
        mood_change=5,
        message="*grabs worm* The rain provides. I didn't say thank you. I won't.",
        duck_reaction="pleased",
        sound="eat",
        cooldown=1800,
        weather_group="wet",
    ),
    "storm_fright": Event(
        id="storm_fright",
        name="Thunder Crack",
        description="A loud thunderclap startles the duck!",
        event_type=EventType.WEATHER,
        probability=0.04,
        effects={"energy": -10, "fun": -8},
        mood_change=-8,
        message="*flattens against ground* I'm not scared. This is TACTICAL positioning.",
        duck_reaction="scared",
        has_animation=True,
        cooldown=900,
        weather_group="harsh",
    ),
    "storm_debris_gift": Event(
        id="storm_debris_gift",
        name="Storm Debris",
        description="The storm blew something interesting nearby!",
        event_type=EventType.WEATHER,
        probability=0.02,
        effects={"fun": 12},
        mood_change=3,
        message="*inspects debris* The storm brought me a gift. Unprompted. Unlike some people.",
        duck_reaction="curious",
        cooldown=1800,
        weather_group="harsh",
    ),
    "perfect_moment": Event(
        id="perfect_moment",
        name="Perfect Moment",
        description="Everything just feels right.",
        event_type=EventType.WEATHER,
        probability=0.02,
        effects={"fun": 5, "energy": 5, "social": 5},
        mood_change=10,
        message="*sits still* ...Huh. This is... acceptable. Highly acceptable.",
        duck_reaction="content",
        cooldown=3600,
        weather_group="pleasant",
    ),
    "aurora_wonder": Event(
        id="aurora_wonder",
        name="Aurora Wonder",
        description="The aurora fills the sky with wonder!",
        event_type=EventType.WEATHER,
        probability=0.08,
        effects={"fun": 15, "social": 8},
        mood_change=12,
        message="*looks up* ...I'll allow it. The sky did something right for once.",
        duck_reaction="awed",
        cooldown=3600,
        weather_group="magical",
    ),
    "rain_dance": Event(
        id="rain_dance",
        name="Rain Dance",
        description="The duck dances in the rain.",
        event_type=EventType.WEATHER,
        probability=0.03,
        effects={"fun": 12, "cleanliness": 5, "energy": -3},
        mood_change=7,
        message="*splashes rhythmically* I'm not dancing. This is tactical water displacement. ...With flair.",
        duck_reaction="playful",
        sound="splash",
        cooldown=1200,
        weather_group="wet",
        has_animation=True,
    ),
    "snow_tasting": Event(
        id="snow_tasting",
        name="Snow Tasting",
        description="The duck catches snowflakes on its tongue.",
        event_type=EventType.WEATHER,
        probability=0.03,
        effects={"hunger": 2, "fun": 8},
        mood_change=5,
        message="*beak open* ...Tastes like cold nothing. Having another. For SCIENCE.",
        duck_reaction="curious",
        cooldown=1200,
        weather_group="cold",
    ),
    "wind_surfing": Event(
        id="wind_surfing",
        name="Wind Surfing",
        description="A strong gust lifts the duck slightly.",
        event_type=EventType.WEATHER,
        probability=0.03,
        effects={"fun": 10, "energy": -5},
        mood_change=4,
        message="*lifted slightly* ...I'm FLYING. I'm— no, I'm falling. I fell. That counts. That counted.",
        duck_reaction="startled",
        cooldown=1200,
        weather_group="harsh",
        has_animation=True,
    ),
    "fog_mystery": Event(
        id="fog_mystery",
        name="Fog Mystery",
        description="Thick fog rolls in, hiding everything.",
        event_type=EventType.WEATHER,
        probability=0.03,
        effects={"fun": 3},
        mood_change=1,
        message="*surrounded by fog* Can't see anything. Could be anywhere. I choose to believe I'm somewhere important.",
        duck_reaction="mysterious",
        cooldown=1800,
        weather_group="wet",
    ),
    "sun_glare": Event(
        id="sun_glare",
        name="Sun Glare",
        description="The sun is blindingly bright.",
        event_type=EventType.WEATHER,
        probability=0.03,
        effects={"fun": -3, "energy": -3},
        mood_change=-3,
        message="*squints aggressively* The sun is ATTACKING me. Personally. I take this as a THREAT.",
        duck_reaction="annoyed",
        cooldown=1200,
        weather_group="hot",
    ),
    "frost_art": Event(
        id="frost_art",
        name="Frost Patterns",
        description="Delicate frost patterns form on nearby surfaces.",
        event_type=EventType.WEATHER,
        probability=0.02,
        effects={"fun": 7},
        mood_change=5,
        message="*examines frost* ...Nature drew on the ground. Without permission. It's pretty good though. Don't tell nature I said that.",
        duck_reaction="impressed",
        cooldown=1800,
        weather_group="cold",
        has_animation=True,
    ),
    "rainbow_after_rain": Event(
        id="rainbow_after_rain",
        name="Post-Rain Rainbow",
        description="A rainbow appears after the rain clears.",
        event_type=EventType.WEATHER,
        probability=0.02,
        effects={"fun": 10, "social": 5},
        mood_change=8,
        message="*stares* ...The sky is apologizing for the rain. With colors. Apology accepted. Barely.",
        duck_reaction="content",
        cooldown=3600,
        weather_group="pleasant",
        has_animation=True,
    ),

    # Visitor events
    "another_duck": Event(
        id="another_duck",
        name="Duck Visitor",
        description="Another duck waddles by!",
        event_type=EventType.VISITOR,
        probability=0.005,
        effects={"social": 20},
        mood_change=10,
        message="*excited quacking* Another duck! ...Act cool. Be cool.",
        duck_reaction="ecstatic",
        sound="quack_excited",
        cooldown=600,
        has_animation=True,
    ),
    "bird_friend": Event(
        id="bird_friend",
        name="Bird Friend",
        description="A small bird visits!",
        event_type=EventType.VISITOR,
        probability=0.01,
        effects={"social": 10},
        mood_change=5,
        message="*nods at bird* ...Sup. We're cool.",
        duck_reaction="friendly",
        cooldown=600,
        has_animation=True,
    ),

    # Growth triggered events
    "first_waddle": Event(
        id="first_waddle",
        name="First Waddle",
        description="The duckling takes its first steps!",
        event_type=EventType.TRIGGERED,
        probability=1.0,
        effects={"fun": 20},
        mood_change=15,
        message="*wobbles* I... Look, I MEANT to do that!",
        duck_reaction="proud",
        sound="level_up",
        requires_stage="duckling",
    ),
    "first_quack": Event(
        id="first_quack",
        name="First Quack",
        description="The duckling quacks for the first time!",
        event_type=EventType.TRIGGERED,
        probability=1.0,
        effects={"social": 15},
        mood_change=20,
        message="*opens beak* ...QUACK! Yeah, nailed it. Obviously.",
        duck_reaction="ecstatic",
        sound="quack_happy",
        requires_stage="duckling",
    ),

    # Chain-starting events (the first stage of multi-stage event chains)
    "mysterious_sound": Event(
        id="mysterious_sound",
        name="Mysterious Sound",
        description="A strange sound comes from the bushes...",
        event_type=EventType.RANDOM,
        probability=0.008,
        effects={},
        mood_change=0,
        message="*head tilt* ...Did you hear that? Something in the bushes. Probably nothing. Probably.",
        duck_reaction="curious",
        cooldown=7200,
        requires_stage="duckling",
        chain_id="mysterious_sound",
    ),
    "shiny_trail": Event(
        id="shiny_trail",
        name="Shiny Trail",
        description="Something glints in the distance...",
        event_type=EventType.RANDOM,
        probability=0.006,
        effects={},
        mood_change=0,
        message="*squints* ...Is that...? Something shiny. Over there. Don't get excited. I'm not excited.",
        duck_reaction="curious",
        cooldown=7200,
        requires_stage="teen",
        chain_id="shiny_trail",
    ),
    "strange_visitor": Event(
        id="strange_visitor",
        name="Strange Tracks",
        description="Unusual tracks appear nearby...",
        event_type=EventType.RANDOM,
        probability=0.005,
        effects={},
        mood_change=0,
        message="*sniffs ground* ...These tracks aren't mine. And they're not yours. So. That's concerning. Mildly.",
        duck_reaction="suspicious",
        cooldown=10800,
        requires_stage="teen",
        chain_id="strange_visitor",
    ),

    # ── Encounters (player agency — help the duck!) ─────────────────
    "enc_predator_shadow": Event(
        id="enc_predator_shadow",
        name="Shadow Overhead!",
        description="Something large passes over the duck.",
        event_type=EventType.RANDOM,
        probability=0.008,
        effects={},
        mood_change=-5,
        message="",  # Encounter trigger_message used instead
        duck_reaction="scared",
        cooldown=3600,
        encounter_id="predator_shadow",
    ),
    "enc_stuck_in_mud": Event(
        id="enc_stuck_in_mud",
        name="Stuck in Mud!",
        description="The duck got stuck in some mud.",
        event_type=EventType.RANDOM,
        probability=0.008,
        effects={},
        mood_change=-3,
        message="",
        duck_reaction="distressed",
        cooldown=3600,
        weather_group="wet",
        encounter_id="stuck_in_mud",
    ),
    "enc_hungry_bully": Event(
        id="enc_hungry_bully",
        name="Food Thief!",
        description="A pigeon is after the duck's food stash.",
        event_type=EventType.RANDOM,
        probability=0.008,
        effects={},
        mood_change=-3,
        message="",
        duck_reaction="alarmed",
        cooldown=3600,
        encounter_id="hungry_bully",
    ),
    "enc_bored_crisis": Event(
        id="enc_bored_crisis",
        name="Existential Boredom",
        description="The duck has run out of thoughts.",
        event_type=EventType.RANDOM,
        probability=0.01,
        effects={},
        mood_change=-2,
        message="",
        duck_reaction="bored",
        cooldown=2400,
        encounter_id="bored_crisis",
    ),

    # ── New seasonal & weather-conditional events ──────────────────────
    "autumn_mushroom": Event(
        id="autumn_mushroom",
        name="Mysterious Mushroom",
        description="A strange mushroom has appeared near the pond.",
        event_type=EventType.RANDOM,
        probability=0.02,
        effects={"fun": 10},
        mood_change=6,
        message="*inspects mushroom* ...It appeared overnight. Nobody planted it. It has its own agenda. I respect that.",
        duck_reaction="curious",
        has_animation=True,
        weather_group="wet",
    ),
    "spring_blossom": Event(
        id="spring_blossom",
        name="Blossom Shower",
        description="Petals drift down like pink snow.",
        event_type=EventType.RANDOM,
        probability=0.02,
        effects={"fun": 12, "energy": 3},
        mood_change=8,
        message="*covered in petals* ...The trees are shedding on me. Unprompted. I look fabulous though. Carry on.",
        duck_reaction="content",
        has_animation=True,
        weather_group="pleasant",
    ),
    "summer_fireflies": Event(
        id="summer_fireflies",
        name="Firefly Display",
        description="Fireflies light up the evening air.",
        event_type=EventType.RANDOM,
        probability=0.015,
        effects={"fun": 14, "social": 5},
        mood_change=10,
        message="*watches lights* ...Bugs with lanterns. They just do that. For free. The sky should be embarrassed.",
        duck_reaction="awed",
        has_animation=True,
        weather_group="pleasant",
    ),
    "winter_icicle": Event(
        id="winter_icicle",
        name="Icicle Discovery",
        description="A perfect icicle hangs from a branch overhead.",
        event_type=EventType.RANDOM,
        probability=0.02,
        effects={"fun": 8},
        mood_change=5,
        message="*stares up* ...The cold made a sword. Out of water. Nature is showing off again.",
        duck_reaction="impressed",
        has_animation=True,
        weather_group="cold",
    ),
    "heatwave_mirage": Event(
        id="heatwave_mirage",
        name="Mirage",
        description="The heat creates a shimmering mirage on the horizon.",
        event_type=EventType.RANDOM,
        probability=0.02,
        effects={"fun": 5},
        mood_change=2,
        message="*squints* ...Is that a bread truck? No. It's nothing. The heat is a liar and I fell for it.",
        duck_reaction="disappointed",
        weather_group="hot",
        cooldown=1800,
    ),

    # ── New social events ─────────────────────────────────────────────
    "visiting_heron": Event(
        id="visiting_heron",
        name="Heron Visit",
        description="A tall heron stands at the pond edge, watching.",
        event_type=EventType.VISITOR,
        probability=0.004,
        effects={"social": 10},
        mood_change=3,
        message="*looks up. keeps looking up.* ...You're tall. Unnecessarily tall. We get it. Congratulations.",
        duck_reaction="intimidated",
        cooldown=3600,
        has_animation=True,
    ),
    "curious_squirrel": Event(
        id="curious_squirrel",
        name="Squirrel Approach",
        description="A squirrel cautiously approaches the duck.",
        event_type=EventType.VISITOR,
        probability=0.008,
        effects={"social": 8, "fun": 5},
        mood_change=5,
        message="*suspicious eye contact* ...It's back. The nut hoarder. I don't have nuts. I have STANDARDS.",
        duck_reaction="wary",
        cooldown=1800,
        has_animation=True,
    ),
    "turtle_encounter": Event(
        id="turtle_encounter",
        name="Turtle at the Pond",
        description="A turtle slowly emerges from the water.",
        event_type=EventType.VISITOR,
        probability=0.005,
        effects={"social": 12, "fun": 8},
        mood_change=7,
        message="*watches turtle surface* ...You live in there? Full time? With that commute speed? Respect. Unironically.",
        duck_reaction="respectful",
        cooldown=3600,
        has_animation=True,
    ),
    "flock_overhead": Event(
        id="flock_overhead",
        name="Flock Overhead",
        description="A V-formation of ducks flies overhead.",
        event_type=EventType.VISITOR,
        probability=0.006,
        effects={"social": 15},
        mood_change=5,
        message="*looks up* ...There they go. The overachievers. With their formation and their PLANS. *stays put*",
        duck_reaction="conflicted",
        cooldown=3600,
        has_animation=True,
        requires_stage="teen",
    ),

    # ── New discovery events ──────────────────────────────────────────
    "old_bottle": Event(
        id="old_bottle",
        name="Message in a Bottle",
        description="An old bottle washes to the pond edge.",
        event_type=EventType.RANDOM,
        probability=0.008,
        effects={"fun": 15},
        mood_change=8,
        message="*inspects bottle* ...There's a note inside. It says 'help.' Bit dramatic. The bottle was in a POND.",
        duck_reaction="amused",
        has_animation=True,
        requires_stage="teen",
    ),
    "buried_crumb": Event(
        id="buried_crumb",
        name="Archaeological Discovery",
        description="The duck unearths an ancient bread crumb.",
        event_type=EventType.RANDOM,
        probability=0.01,
        effects={"hunger": 5, "fun": 12},
        mood_change=8,
        message="*digs* ...A crumb. Buried. Preserved. This is an artifact. Bread archaeology. *eats it immediately*",
        duck_reaction="thrilled",
        sound="eat",
        has_animation=True,
    ),
    "peculiar_stone": Event(
        id="peculiar_stone",
        name="Peculiar Stone",
        description="A stone with unusual markings sits by the water.",
        event_type=EventType.RANDOM,
        probability=0.01,
        effects={"fun": 10},
        mood_change=6,
        message="*examines stone* ...There are markings on this. Could be ancient. Could be a stain. Either way MINE.",
        duck_reaction="intrigued",
        has_animation=True,
    ),
    "forgotten_nest": Event(
        id="forgotten_nest",
        name="Old Nest",
        description="An abandoned nest from a long-gone bird.",
        event_type=EventType.RANDOM,
        probability=0.008,
        effects={"fun": 8, "social": 5},
        mood_change=4,
        message="*peers into nest* ...Someone lived here. Built this. Left. The real estate market is brutal even for birds.",
        duck_reaction="thoughtful",
        has_animation=True,
        requires_stage="teen",
    ),

    # ── Rare and legendary events ─────────────────────────────────────
    "golden_breadcrumb": Event(
        id="golden_breadcrumb",
        name="The Golden Crumb",
        description="A bread crumb that seems to glow in the light.",
        event_type=EventType.RANDOM,
        probability=0.002,
        effects={"hunger": 25, "fun": 30},
        mood_change=20,
        message="*trembling* ...It's GLOWING. The crumb is glowing. This is the bread prophecy. The one the ancients spoke of. *reverent nibble*",
        duck_reaction="ecstatic",
        sound="alert",
        has_animation=True,
        requires_stage="teen",
    ),
    "legendary_feather": Event(
        id="legendary_feather",
        name="The Iridescent Feather",
        description="A feather that shifts through every color.",
        event_type=EventType.RANDOM,
        probability=0.001,
        effects={"fun": 35, "social": 15},
        mood_change=25,
        message="*stares* ...This feather changes color. Every color. The single most beautiful object that has ever existed. After bread.",
        duck_reaction="awed",
        sound="alert",
        has_animation=True,
        requires_stage="adult",
    ),
    "ancient_coin": Event(
        id="ancient_coin",
        name="Ancient Coin",
        description="A very old coin, worn smooth by time.",
        event_type=EventType.RANDOM,
        probability=0.003,
        effects={"fun": 20},
        mood_change=12,
        message="*picks up coin* ...This is old. Really old. There's a face on it. The face looks tired. Same, coin. Same.",
        duck_reaction="impressed",
        sound="alert",
        has_animation=True,
        requires_stage="teen",
    ),

    # ── Chain-starting event ──────────────────────────────────────────
    "mysterious_map": Event(
        id="mysterious_map",
        name="A Soggy Map",
        description="Something that looks like a map floats to shore.",
        event_type=EventType.RANDOM,
        probability=0.005,
        effects={},
        mood_change=3,
        message="*picks up soggy paper* ...Lines. And an X. That's a map. I know what maps are. I'm not excited. ...Yes I am.",
        duck_reaction="curious",
        cooldown=10800,
        requires_stage="teen",
        chain_id="mysterious_map",
    ),

    # ── Additional seasonal discovery events ──────────────────────────
    "dewdrop_morning": Event(
        id="dewdrop_morning",
        name="Morning Dew",
        description="Everything is covered in perfect dewdrops.",
        event_type=EventType.RANDOM,
        probability=0.02,
        effects={"fun": 8, "cleanliness": 5},
        mood_change=6,
        message="*examines dewdrop* ...Each one is a tiny lens. Showing a tiny world. In which a tiny Cheese exists. Infinite Cheeses. You're welcome, universe.",
        duck_reaction="contemplative",
        has_animation=True,
        weather_group="pleasant",
    ),
    "autumn_leaf_pile": Event(
        id="autumn_leaf_pile",
        name="Leaf Pile",
        description="A pile of colorful autumn leaves has gathered.",
        event_type=EventType.RANDOM,
        probability=0.02,
        effects={"fun": 12},
        mood_change=8,
        message="*launches into leaf pile* ...I regret nothing. There might be bugs in here. I DO NOT CARE.",
        duck_reaction="playful",
        has_animation=True,
    ),
    "first_flower": Event(
        id="first_flower",
        name="First Flower",
        description="The very first flower of the season appears.",
        event_type=EventType.RANDOM,
        probability=0.01,
        effects={"fun": 10, "social": 5},
        mood_change=8,
        message="*stares at flower* ...You're early. Or I'm late. Either way you're the only one here. Brave. I respect brave things.",
        duck_reaction="gentle",
        has_animation=True,
        weather_group="pleasant",
    ),
    "frozen_puddle": Event(
        id="frozen_puddle",
        name="Frozen Puddle",
        description="A nearby puddle has frozen solid overnight.",
        event_type=EventType.WEATHER,
        probability=0.02,
        effects={"fun": 10},
        mood_change=5,
        message="*steps on ice* *slides* ...I meant to do that. This is skating. I'm skating now. *slides into bush*",
        duck_reaction="surprised",
        sound="splash",
        has_animation=True,
        weather_group="cold",
        cooldown=1800,
    ),

    # ── Additional social interaction events ──────────────────────────
    "duck_argument": Event(
        id="duck_argument",
        name="Distant Quacking",
        description="Two ducks are arguing in the distance.",
        event_type=EventType.RANDOM,
        probability=0.008,
        effects={"social": 5, "fun": 8},
        mood_change=4,
        message="*listens* ...Two ducks. Having words. About territory, probably. Or bread. Always bread. I'm staying out of it. *leans in to listen*",
        duck_reaction="nosy",
        cooldown=3600,
    ),
    "baby_ducks": Event(
        id="baby_ducks",
        name="Duckling Parade",
        description="A mother duck leads a line of tiny ducklings past.",
        event_type=EventType.VISITOR,
        probability=0.004,
        effects={"social": 20, "fun": 15},
        mood_change=12,
        message="*watches ducklings* ...Small. Very small. I was that small once. Hard to believe. They'll grow. They'll learn about bread. Everything is ahead of them.",
        duck_reaction="softened",
        cooldown=7200,
        has_animation=True,
        requires_stage="adult",
    ),
    "cat_staredown": Event(
        id="cat_staredown",
        name="Cat at the Pond",
        description="A cat sits at the pond edge, watching the duck.",
        event_type=EventType.VISITOR,
        probability=0.005,
        effects={"fun": 5},
        mood_change=0,
        message="*locks eyes with cat* ...We meet again. Neither of us blinks. The standoff continues. I'm in the water. I have the tactical advantage. And we both know it.",
        duck_reaction="defiant",
        cooldown=3600,
        has_animation=True,
    ),
    "crow_gift": Event(
        id="crow_gift",
        name="Crow's Gift",
        description="A crow drops something shiny near the duck.",
        event_type=EventType.VISITOR,
        probability=0.005,
        effects={"fun": 15, "social": 10},
        mood_change=10,
        message="*examines object* ...A crow dropped this. On purpose. It's shiny. And it's FOR ME. Crows understand gift-giving. Unlike some species. *looks at humans*",
        duck_reaction="touched",
        sound="alert",
        cooldown=7200,
        has_animation=True,
    ),

    # ── Additional rare and legendary events ──────────────────────────
    "perfect_reflection": Event(
        id="perfect_reflection",
        name="The Perfect Reflection",
        description="The pond is so still it creates a flawless mirror.",
        event_type=EventType.RANDOM,
        probability=0.003,
        effects={"fun": 20, "social": 10},
        mood_change=15,
        message="*looks down* ...The pond is a mirror. I see myself. Clearly. For once. And I look... good. I look really good. The pond knows the truth.",
        duck_reaction="moved",
        has_animation=True,
        cooldown=7200,
    ),
    "shooting_star": Event(
        id="shooting_star",
        name="Shooting Star",
        description="A shooting star streaks across the night sky.",
        event_type=EventType.RANDOM,
        probability=0.002,
        effects={"fun": 25},
        mood_change=18,
        message="*looks up* ...A star just fell. Moving. Fast. I made a wish. The wish is bread. But also something else. I won't say what. That's between me and the star.",
        duck_reaction="awed",
        sound="alert",
        has_animation=True,
        cooldown=14400,
    ),
    "double_yolk": Event(
        id="double_yolk",
        name="Double Yolk Day",
        description="Everything seems to come in twos today.",
        event_type=EventType.RANDOM,
        probability=0.002,
        effects={"fun": 25, "hunger": 15},
        mood_change=15,
        message="*blinks* ...Two crumbs where there should be one. Two butterflies. Two reflections? The world is being generous. I accept. Cautiously. But I accept.",
        duck_reaction="lucky",
        sound="alert",
        has_animation=True,
        cooldown=14400,
    ),

    # ── Round 3: More events ──────────────────────────────────────────────
    "old_tire_swing": Event(
        id="old_tire_swing",
        name="The Old Tire Swing",
        description="Someone hung a tire from the big tree. It swings over the water.",
        event_type=EventType.DISCOVERY,
        probability=0.012,
        effects={"fun": 20, "energy": -5},
        mood_change=12,
        message="There is a tire. Hanging from a rope. Over the water. *stares at it for eleven minutes* ...I am not getting on that. *gets on it* This was a mistake. *swings* This is the best mistake.",
        duck_reaction="happy",
        sound="splash",
        has_animation=True,
        cooldown=7200,
    ),
    "fog_morning": Event(
        id="fog_morning",
        name="The Fog",
        description="A thick fog rolls in, making the pond feel infinite.",
        event_type=EventType.WEATHER,
        probability=0.02,
        effects={"fun": 8, "energy": -3},
        mood_change=5,
        message="Can't see the edges of the pond. Can't see the far bank. For all I know the pond goes on forever now. *floats cautiously* This is either peaceful or the beginning of a horror story. I choose peaceful.",
        duck_reaction="curious",
        weather_group="fog",
        cooldown=3600,
    ),
    "paper_boat": Event(
        id="paper_boat",
        name="Paper Boat",
        description="A small paper boat drifts onto the pond.",
        event_type=EventType.DISCOVERY,
        probability=0.015,
        effects={"fun": 15, "social": 5},
        mood_change=10,
        message="A paper boat. Someone made it. Someone folded paper into a shape that means 'boat' and put it on the water and it came to me. *nudges it gently* It's not a REAL boat. But it's trying. I respect the effort.",
        duck_reaction="curious",
        sound="splash",
        cooldown=7200,
    ),
    "visiting_owl": Event(
        id="visiting_owl",
        name="The Owl's Visit",
        description="An owl perches nearby in the early evening.",
        event_type=EventType.SOCIAL,
        probability=0.01,
        effects={"social": 12, "energy": -5},
        mood_change=6,
        message="An owl. In the tree. Looking at me with those enormous eyes. *looks back* I feel judged but also educated. Like a very silent lecture. We maintain eye contact for an uncomfortable amount of time. The owl blinks first. I WIN.",
        duck_reaction="curious",
        sound="ambient",
        cooldown=14400,
    ),
    "lost_kite": Event(
        id="lost_kite",
        name="Lost Kite",
        description="A kite with a broken string tangles in a bush near the pond.",
        event_type=EventType.DISCOVERY,
        probability=0.01,
        effects={"fun": 10, "energy": -3},
        mood_change=7,
        message="A kite. In a bush. Its string goes nowhere. Someone was flying it and then they weren't. *studies the diamond shape and the tail* It's a bird that needs a person to fly. Tragic when you think about it. I don't think about it. I peck the tail.",
        duck_reaction="curious",
        cooldown=7200,
    ),
    "morning_cobwebs": Event(
        id="morning_cobwebs",
        name="Dew-Covered Cobwebs",
        description="Morning dew decorates the cobwebs around the pond like tiny jewels.",
        event_type=EventType.WEATHER,
        probability=0.025,
        effects={"fun": 8},
        mood_change=8,
        message="The spiders have been decorating. Every web has a thousand little water diamonds. *waddles closer* Impressive craftsmanship. I couldn't make this. I make ripples. Ripples are good but they don't stay. These stay. Until the sun eats them.",
        duck_reaction="curious",
        weather_group="clear",
        cooldown=3600,
    ),
    "frog_chorus": Event(
        id="frog_chorus",
        name="Frog Chorus",
        description="The frogs start an evening concert near the pond.",
        event_type=EventType.SOCIAL,
        probability=0.03,
        effects={"fun": 12, "social": 8},
        mood_change=9,
        message="The frogs are singing. All of them. At once. Different songs. *listens* This is not coordinated. This is a hundred tiny egos competing for volume. I relate to this energy. *quacks along* We sound terrible together. This is community.",
        duck_reaction="happy",
        sound="ambient",
        cooldown=3600,
    ),
    "old_fishing_line": Event(
        id="old_fishing_line",
        name="Tangled Fishing Line",
        description="An old fishing line is caught on a rock. No hook, thankfully.",
        event_type=EventType.DISCOVERY,
        probability=0.01,
        effects={"energy": -5},
        mood_change=-3,
        message="Fishing line. Old. Tangled on a rock. *gives it a wide berth* Someone was trying to catch something. Not me. I hope. I am NOT a fish. I want that on the record. I am a DUCK. Very different. Fundamentally.",
        duck_reaction="nervous",
        cooldown=14400,
    ),
    "butterfly_migration": Event(
        id="butterfly_migration",
        name="Butterfly Migration",
        description="Hundreds of butterflies pass over the pond.",
        event_type=EventType.SEASONAL,
        probability=0.005,
        effects={"fun": 25, "energy": 5},
        mood_change=15,
        message="Butterflies. Not one. Not ten. HUNDREDS. The sky is moving with them. *watches with beak slightly open* They're going somewhere important. They all agreed on a direction. Nobody asked me. I would have said south. Because that's the direction I know.",
        duck_reaction="amazed",
        sound="alert",
        has_animation=True,
        cooldown=86400,
    ),
    "dragonfly_landing": Event(
        id="dragonfly_landing",
        name="Dragonfly Landing Pad",
        description="A dragonfly lands directly on Cheese's head.",
        event_type=EventType.RANDOM,
        probability=0.02,
        effects={"fun": 15},
        mood_change=10,
        message="Something landed on my head. *freezes* I can't see it. But I can feel tiny feet. Six of them. On my HEAD. *holds extremely still* I am a landing pad now. This is my new identity. I will not move until it leaves. I have been chosen.",
        duck_reaction="happy",
        has_animation=True,
        cooldown=3600,
    ),
    "mud_puddle_spa": Event(
        id="mud_puddle_spa",
        name="Mud Puddle Spa",
        description="A particularly nice mud puddle appears after light rain.",
        event_type=EventType.WEATHER,
        probability=0.02,
        effects={"fun": 15, "hygiene": -10, "energy": 10},
        mood_change=12,
        message="A mud puddle. Warm. The perfect consistency. *settles in* I know what you're thinking. 'Cheese, you live in water.' Yes. But this is DIFFERENT water. This is water that chose to be mud. Aspirational. *sinks lower* This is a spa day.",
        duck_reaction="happy",
        weather_group="rain",
        cooldown=7200,
    ),
    "echo_discovery": Event(
        id="echo_discovery",
        name="Echo Discovery",
        description="Cheese discovers that quacking under the bridge creates an echo.",
        event_type=EventType.DISCOVERY,
        probability=0.008,
        effects={"fun": 20},
        mood_change=14,
        message="*quacks under bridge* QUACK. ...quack. *freezes* There is another duck. Under the bridge. Copying me. *quacks again* QUACK. ...quack. *narrows eyes* Clever. Very clever. ...Wait. Is that me? That's me. I'm incredible. *quacks seventeen more times*",
        duck_reaction="happy",
        sound="quack",
        has_animation=True,
        cooldown=14400,
    ),
    "night_fishing_lights": Event(
        id="night_fishing_lights",
        name="Lights on the Water",
        description="Someone's distant flashlight reflects off the water at night.",
        event_type=EventType.RANDOM,
        probability=0.015,
        effects={"fun": 10, "energy": -5},
        mood_change=5,
        message="A light. On the water. Moving slowly. *watches from nest* It's probably a human with a flashlight. Probably. Could also be a ghost. Or an anglerfish. Or my imagination. I choose to believe it's a firefly with ambition.",
        duck_reaction="curious",
        cooldown=7200,
    ),
}


# ── Multi-stage event chains ────────────────────────────────────────────

EVENT_CHAINS: Dict[str, EventChain] = {
    "mysterious_sound": EventChain(
        id="mysterious_sound",
        stages=[
            # Stage 0 is the starter event above
            Event(
                id="mysterious_sound_2",
                name="Investigation",
                description="Getting closer to the sound...",
                event_type=EventType.RANDOM,
                probability=1.0,
                effects={"fun": 5},
                mood_change=3,
                message="*creeps forward* ...It's getting louder. I'm not scared. This is scientific curiosity.",
                duck_reaction="cautious",
            ),
            Event(
                id="mysterious_sound_3",
                name="Discovery!",
                description="Found the source!",
                event_type=EventType.RANDOM,
                probability=1.0,
                effects={"fun": 15, "social": 10},
                mood_change=10,
                message="*parts bushes* ...It's a cricket. A CRICKET. All that buildup for a cricket. "
                        "...Fine, it's kind of cute. Don't tell anyone I said that.",
                duck_reaction="amused",
                sound="discovery",
            ),
        ],
        min_seconds_between=45.0,
        cooldown=7200.0,
        requires_stage="duckling",
    ),
    "shiny_trail": EventChain(
        id="shiny_trail",
        stages=[
            Event(
                id="shiny_trail_2",
                name="Following the Trail",
                description="The trail continues...",
                event_type=EventType.RANDOM,
                probability=1.0,
                effects={"energy": -3},
                mood_change=2,
                message="*waddles determinedly* ...The trail goes this way. I'm committed now. No turning back.",
                duck_reaction="focused",
            ),
            Event(
                id="shiny_trail_3",
                name="Shiny Treasure",
                description="Found something!",
                event_type=EventType.RANDOM,
                probability=1.0,
                effects={"fun": 20, "hunger": 5},
                mood_change=12,
                message="*gasp* ...A bottle cap. THE bottle cap. The shiniest one I've ever— "
                        "I mean. It's adequate. I'll keep it. For research.",
                duck_reaction="thrilled",
                sound="discovery",
            ),
        ],
        min_seconds_between=60.0,
        cooldown=7200.0,
        requires_stage="teen",
    ),
    "strange_visitor": EventChain(
        id="strange_visitor",
        stages=[
            Event(
                id="strange_visitor_2",
                name="More Evidence",
                description="More signs of the visitor...",
                event_type=EventType.RANDOM,
                probability=1.0,
                effects={},
                mood_change=-2,
                message="*finds feather* ...Not my feather. Different color. Someone was HERE. In MY territory.",
                duck_reaction="suspicious",
            ),
            Event(
                id="strange_visitor_3",
                name="The Encounter",
                description="Face to face with the visitor!",
                event_type=EventType.RANDOM,
                probability=1.0,
                effects={"social": 25, "fun": 10},
                mood_change=8,
                message="*stares* ...It's another duck. Just standing there. Staring back. "
                        "We had a moment. We nodded. They left. I didn't ask them to stay. "
                        "I didn't want them to stay. ...Did they have to leave so fast though?",
                duck_reaction="conflicted",
                sound="quack",
            ),
        ],
        min_seconds_between=90.0,
        cooldown=10800.0,
        requires_stage="teen",
    ),
    "mysterious_map": EventChain(
        id="mysterious_map",
        stages=[
            Event(
                id="mysterious_map_2",
                name="Following the Map",
                description="The map leads somewhere specific...",
                event_type=EventType.RANDOM,
                probability=1.0,
                effects={"energy": -5},
                mood_change=5,
                message="*waddling with purpose* ...The map says go this way. I trust the map. "
                        "I've had it for two minutes. That's long enough to build trust.",
                duck_reaction="determined",
            ),
            Event(
                id="mysterious_map_3",
                name="X Marks the Spot",
                description="Arrived at the marked location!",
                event_type=EventType.RANDOM,
                probability=1.0,
                effects={"fun": 25, "hunger": 10},
                mood_change=15,
                message="*digs* ...A tin box. Inside: three very old bread crumbs and a smooth pebble. "
                        "This is the greatest treasure ever found. By anyone. I am a professional explorer now.",
                duck_reaction="ecstatic",
                sound="discovery",
            ),
        ],
        min_seconds_between=60.0,
        cooldown=10800.0,
        requires_stage="teen",
    ),
}


# =============================================================================
# SPECIAL DAY EVENTS (Animal Crossing style)
# =============================================================================

SPECIAL_DAY_EVENTS = {
    # Monthly events
    "new_years": Event(
        id="new_years",
        name="New Year's Day",
        description="Happy New Year! Time for new beginnings.",
        event_type=EventType.SPECIAL_DAY,
        probability=1.0,
        effects={"fun": 30, "social": 20},
        mood_change=25,
        message="HAPPY NEW YEAR! *celebratory quacking* This is MY year. Watch me.",
        duck_reaction="ecstatic",
        sound="celebrate",
        cooldown=86400,  # Once per day
    ),
    "valentines": Event(
        id="valentines",
        name="Valentine's Day",
        description="A day for love and friendship!",
        event_type=EventType.SPECIAL_DAY,
        probability=1.0,
        effects={"social": 40},
        mood_change=30,
        message="*blushes* Valentine's Day... You remembered? ...I mean, obviously you did. I'm unforgettable. <3",
        duck_reaction="love",
        sound="happy",
        cooldown=86400,
    ),
    "spring_equinox": Event(
        id="spring_equinox",
        name="First Day of Spring",
        description="Spring has sprung! New life emerges.",
        event_type=EventType.SPECIAL_DAY,
        probability=1.0,
        effects={"fun": 20, "energy": 15},
        mood_change=20,
        message="*sniffs air* Spring! Bugs to hunt, flowers to ignore, villains to defeat. Let's GO.",
        duck_reaction="happy",
        cooldown=86400,
    ),
    "april_fools": Event(
        id="april_fools",
        name="April Fools Day",
        description="Prepare for pranks!",
        event_type=EventType.SPECIAL_DAY,
        probability=1.0,
        effects={"fun": 25},
        mood_change=15,
        message="*suspicious glare* I trust NOTHING today. Everyone's a suspect. Especially you.",
        duck_reaction="suspicious",
        cooldown=86400,
    ),
    "summer_solstice": Event(
        id="summer_solstice",
        name="Summer Solstice",
        description="The longest day of the year!",
        event_type=EventType.SPECIAL_DAY,
        probability=1.0,
        effects={"energy": 30, "fun": 20},
        mood_change=20,
        message="*basking* MAXIMUM SUN! Peak power! I am UNSTOPPABLE! ...Right after this nap.",
        duck_reaction="happy",
        cooldown=86400,
    ),
    "halloween": Event(
        id="halloween",
        name="Halloween",
        description="Spooky season is here!",
        event_type=EventType.SPECIAL_DAY,
        probability=1.0,
        effects={"fun": 30},
        mood_change=20,
        message="*wearing tiny pumpkin* FEAR ME! I am the NIGHT DUCK! ...Was that scary? Be honest.",
        duck_reaction="playful",
        sound="spooky",
        cooldown=86400,
    ),
    "thanksgiving": Event(
        id="thanksgiving",
        name="Thanksgiving",
        description="A day to be grateful!",
        event_type=EventType.SPECIAL_DAY,
        probability=1.0,
        effects={"hunger": 50, "social": 30},
        mood_change=25,
        message="*content sigh* I'm thankful for bread, vengeance, and you. ...In that order. Don't overthink it.",
        duck_reaction="content",
        cooldown=86400,
    ),
    "winter_solstice": Event(
        id="winter_solstice",
        name="Winter Solstice",
        description="The shortest day of the year.",
        event_type=EventType.SPECIAL_DAY,
        probability=1.0,
        effects={"energy": -10},
        mood_change=10,
        message="*shivers* It's cold and dark. The world conspires against me. More naps required.",
        duck_reaction="sleepy",
        cooldown=86400,
    ),
    "christmas": Event(
        id="christmas",
        name="Christmas Day",
        description="Merry Christmas! A magical time.",
        event_type=EventType.SPECIAL_DAY,
        probability=1.0,
        effects={"fun": 40, "social": 30, "hunger": 20},
        mood_change=35,
        message="MERRY QUACKMAS! *tiny santa hat* I got you a shiny rock. YOU'RE WELCOME. Where's my bread?",
        duck_reaction="ecstatic",
        sound="celebrate",
        cooldown=86400,
    ),
    "new_years_eve": Event(
        id="new_years_eve",
        name="New Year's Eve",
        description="The last day of the year!",
        event_type=EventType.SPECIAL_DAY,
        probability=1.0,
        effects={"fun": 25, "social": 25},
        mood_change=20,
        message="*excited* Almost a new year! New chances to find crumbs! New puddles to splash in! I can't wait!!",
        duck_reaction="excited",
        sound="celebrate",
        cooldown=86400,
    ),

    # Weekly events
    "lazy_sunday": Event(
        id="lazy_sunday",
        name="Lazy Sunday",
        description="A perfect day for doing nothing.",
        event_type=EventType.SPECIAL_DAY,
        probability=0.5,
        effects={"energy": 20},
        mood_change=15,
        message="*yawns* It's Sunday... Perfect day to just... exist. *flops over* Wake me up when there's food.",
        duck_reaction="sleepy",
        cooldown=86400,
    ),
    "monday_blues": Event(
        id="monday_blues",
        name="Case of the Mondays",
        description="Ugh, Monday.",
        event_type=EventType.SPECIAL_DAY,
        probability=0.3,
        effects={"fun": -10},
        mood_change=-5,
        message="*grumbles* It's Monday... Even though every day is basically the same for me, it just FEELS worse somehow.",
        duck_reaction="grumpy",
        cooldown=86400,
    ),
    "taco_tuesday": Event(
        id="taco_tuesday",
        name="Tasty Tuesday",
        description="Food tastes extra good today!",
        event_type=EventType.SPECIAL_DAY,
        probability=0.4,
        effects={"hunger": 15},
        mood_change=10,
        message="*sniffs* Is it just me or does everything smell more delicious today?? *drools*",
        duck_reaction="hungry",
        cooldown=86400,
    ),
    "hump_day": Event(
        id="hump_day",
        name="Hump Day",
        description="We're halfway through the week!",
        event_type=EventType.SPECIAL_DAY,
        probability=0.3,
        effects={"fun": 10},
        mood_change=5,
        message="*waddles determinedly* Wednesday! Halfway there! Halfway to... wait, what are we working towards again?",
        duck_reaction="confused",
        cooldown=86400,
    ),
    "friday_vibes": Event(
        id="friday_vibes",
        name="Friday Feeling",
        description="The weekend is almost here!",
        event_type=EventType.SPECIAL_DAY,
        probability=0.5,
        effects={"fun": 20, "energy": 10},
        mood_change=15,
        message="*dances* It's FRIDAY!! Time to party!! *realizes ducks party every day* Wait, what's special about- PARTY ANYWAY!!",
        duck_reaction="happy",
        cooldown=86400,
    ),

    # Time of day events
    "golden_hour": Event(
        id="golden_hour",
        name="Golden Hour",
        description="The light is beautiful right now.",
        event_type=EventType.SPECIAL_DAY,
        probability=0.6,
        effects={"fun": 15},
        mood_change=10,
        message="*stares at sunset* Pretty... So pretty... *forgets what they were doing*",
        duck_reaction="content",
        cooldown=3600,  # Once per hour
    ),
    "midnight_snack": Event(
        id="midnight_snack",
        name="Midnight Munchies",
        description="Late night cravings hit different.",
        event_type=EventType.SPECIAL_DAY,
        probability=0.4,
        effects={"hunger": -10},
        mood_change=0,
        message="*stomach growls* Why am I awake?? And why do I suddenly want bread SO badly??",
        duck_reaction="hungry",
        cooldown=3600,
    ),

    # Weather/Seasonal mood
    "rainy_day": Event(
        id="rainy_day",
        name="Rainy Day",
        description="Perfect weather for ducks!",
        event_type=EventType.SPECIAL_DAY,
        probability=0.3,
        effects={"cleanliness": 20, "fun": 25},
        mood_change=20,
        message="*splashes joyfully* RAIN!! The sky is giving me a BATH!! Best! Day! EVER!!",
        duck_reaction="ecstatic",
        sound="splash",
        cooldown=7200,
    ),
}


# Global minimum gap between ANY random event firing (seconds).
# Prevents the huge pool of 590+ events from overwhelming the player.
GLOBAL_EVENT_MIN_GAP = 120  # 2 minutes between events


class EventSystem:
    """
    Manages game events including special day events.
    """

    def __init__(self):
        self._last_event_times: Dict[str, float] = {}
        self._last_any_event_time: float = 0.0  # global cooldown tracker
        self._triggered_events: set = set()
        self._current_weather: Optional[str] = None
        self._pending_events: List[Event] = []
        self._last_special_check: Optional[str] = None
        # Event chain tracking
        self._active_chains: Dict[str, Dict] = {}  # chain_id → {stage, started_at, last_stage_at}
        self._completed_chains: set = set()  # chain_ids that completed (for cooldown)
        # Encounter tracking (negative events with player agency)
        self._active_encounter: Optional[Dict] = None  # {encounter_id, started_at}

    def set_current_weather(self, weather: str):
        """Set the current weather for weather-based events."""
        self._current_weather = weather

    def _weather_group_matches(self, required_group: str) -> bool:
        """Check if the current weather matches a required weather group."""
        if not self._current_weather:
            return False
        try:
            from world.atmosphere import WeatherType, _WEATHER_TYPE_TO_GROUP
            # _current_weather may be a string value or a WeatherType
            if isinstance(self._current_weather, str):
                weather_type = WeatherType(self._current_weather)
            else:
                weather_type = self._current_weather
            return _WEATHER_TYPE_TO_GROUP.get(weather_type) == required_group
        except (ValueError, KeyError):
            return False

    def check_random_events(self, duck: "Duck") -> Optional[Event]:
        """
        Check if a random event should occur.

        Args:
            duck: The duck entity

        Returns:
            Event if one occurred, None otherwise
        """
        current_time = time.time()

        # Global cooldown — don't fire anything if an event happened recently
        if current_time - self._last_any_event_time < GLOBAL_EVENT_MIN_GAP:
            return None

        for event_id, event in EVENTS.items():
            if event.event_type not in [EventType.RANDOM, EventType.WEATHER, EventType.VISITOR, EventType.SEASONAL, EventType.DISCOVERY]:
                continue

            # Check cooldown
            last_time = self._last_event_times.get(event_id, 0)
            if current_time - last_time < event.cooldown:
                continue

            # Check weather group requirement
            if event.weather_group:
                if not self._weather_group_matches(event.weather_group):
                    continue

            # Check stage requirement
            if event.requires_stage:
                required_idx = SIMPLE_GROWTH_STAGES.index(event.requires_stage) if event.requires_stage in SIMPLE_GROWTH_STAGES else 0
                current_idx = SIMPLE_GROWTH_STAGES.index(duck.growth_stage) if duck.growth_stage in SIMPLE_GROWTH_STAGES else 0
                if current_idx < required_idx:
                    continue

            # Roll for event
            if random.random() < event.probability:
                self._last_event_times[event_id] = current_time
                self._last_any_event_time = current_time  # global cooldown
                
                # If this event starts an encounter, activate the encounter
                if event.encounter_id and event.encounter_id in ENCOUNTERS:
                    # Don't start if an encounter is already active
                    if self._active_encounter:
                        continue
                    self.start_encounter(event.encounter_id)
                
                # If this event starts a chain, activate the chain
                elif event.chain_id and event.chain_id in EVENT_CHAINS:
                    chain = EVENT_CHAINS[event.chain_id]
                    self._active_chains[event.chain_id] = {
                        "stage": 0,
                        "started_at": current_time,
                        "last_stage_at": current_time,
                    }
                
                return event

        return None

    def check_chain_progress(self, duck: "Duck") -> Optional[Event]:
        """
        Check if any active event chains should advance to their next stage.
        
        Returns:
            The next stage Event if one is ready, else None.
        """
        current_time = time.time()
        chains_to_remove = []
        
        for chain_id, state in self._active_chains.items():
            chain = EVENT_CHAINS.get(chain_id)
            if not chain:
                chains_to_remove.append(chain_id)
                continue
            
            current_stage = state["stage"]
            next_stage = current_stage + 1
            
            # All stages done?
            if next_stage >= len(chain.stages):
                chains_to_remove.append(chain_id)
                self._completed_chains.add(chain_id)
                self._last_event_times[chain_id] = current_time
                continue
            
            # Wait between stages
            elapsed = current_time - state["last_stage_at"]
            if elapsed < chain.min_seconds_between:
                continue
            
            # Advance!
            state["stage"] = next_stage
            state["last_stage_at"] = current_time
            
            stage_event = chain.stages[next_stage]
            
            # Final stage → complete the chain
            if next_stage >= len(chain.stages) - 1:
                chains_to_remove.append(chain_id)
                self._completed_chains.add(chain_id)
                self._last_event_times[chain_id] = current_time
            
            return stage_event
        
        for cid in chains_to_remove:
            self._active_chains.pop(cid, None)
        
        return None

    # ── Encounter management (negative events with player agency) ────
    
    def start_encounter(self, encounter_id: str) -> Optional[str]:
        """
        Start an encounter. Returns the trigger_message to display, or None.
        Only one encounter can be active at a time.
        """
        if self._active_encounter:
            return None
        encounter = ENCOUNTERS.get(encounter_id)
        if not encounter:
            return None
        self._active_encounter = {
            "encounter_id": encounter_id,
            "started_at": time.time(),
        }
        return encounter.trigger_message

    def has_active_encounter(self) -> bool:
        """Check if there's an active encounter."""
        return self._active_encounter is not None

    def get_active_encounter(self) -> Optional["Encounter"]:
        """Get the active encounter object, or None."""
        if not self._active_encounter:
            return None
        return ENCOUNTERS.get(self._active_encounter["encounter_id"])

    def try_resolve_encounter(self, action: str) -> Optional[Dict]:
        """
        Called when the player performs an interaction. If it matches the
        active encounter's help_action, the encounter resolves positively.
        
        Returns a dict with resolution info, or None if no encounter or wrong action.
        """
        if not self._active_encounter:
            return None
        encounter = ENCOUNTERS.get(self._active_encounter["encounter_id"])
        if not encounter:
            self._active_encounter = None
            return None
        
        if action != encounter.help_action:
            return None
        
        # Player helped!
        self._active_encounter = None
        self._last_event_times[encounter.id] = time.time()
        return {
            "resolved": True,
            "message": encounter.help_message,
            "effects": encounter.help_effects,
            "trust_bonus": encounter.help_trust_bonus,
        }

    def check_encounter_timeout(self) -> Optional[Dict]:
        """
        Check if the active encounter has timed out (player didn't help).
        Called from the game tick. Returns resolution dict or None.
        """
        if not self._active_encounter:
            return None
        encounter = ENCOUNTERS.get(self._active_encounter["encounter_id"])
        if not encounter:
            self._active_encounter = None
            return None
        
        elapsed = time.time() - self._active_encounter["started_at"]
        if elapsed < encounter.time_window:
            return None
        
        # Timed out — negative outcome
        self._active_encounter = None
        self._last_event_times[encounter.id] = time.time()
        return {
            "resolved": False,
            "message": encounter.ignore_message,
            "effects": encounter.ignore_effects,
            "trust_bonus": -0.5,
        }

    def check_triggered_events(self, duck: "Duck", trigger: str) -> Optional[Event]:
        """
        Check for triggered events based on game state.

        Args:
            duck: The duck entity
            trigger: What triggered the check (e.g., "stage_change")

        Returns:
            Event if one triggered, None otherwise
        """
        for event_id, event in EVENTS.items():
            if event.event_type != EventType.TRIGGERED:
                continue

            # Already triggered
            if event_id in self._triggered_events:
                continue

            # Check stage requirement
            if event.requires_stage:
                if event.requires_stage == duck.growth_stage:
                    if event_id == "first_waddle" and trigger == "stage_change":
                        self._triggered_events.add(event_id)
                        return event
                    elif event_id == "first_quack" and trigger == "stage_change":
                        self._triggered_events.add(event_id)
                        return event

        return None

    def apply_event(self, duck: "Duck", event: Event) -> Dict:
        """
        Apply an event's effects to the duck.

        Args:
            duck: The duck entity
            event: The event to apply

        Returns:
            Dict with changes made
        """
        changes = {}

        # Apply need effects
        for need, change in event.effects.items():
            if hasattr(duck.needs, need):
                old_value = getattr(duck.needs, need)
                new_value = max(0, min(100, old_value + change))
                setattr(duck.needs, need, new_value)
                changes[need] = new_value - old_value

        return changes

    def get_time_of_day_events(self) -> List[Event]:
        """Get events that should happen based on time of day."""
        hour = datetime.now().hour
        events = []

        # Morning (6-9)
        if 6 <= hour < 9:
            events.append(EVENTS.get("sunny"))

        # Night (22-6)
        if hour >= 22 or hour < 6:
            if random.random() < 0.1:
                events.append(EVENTS.get("bad_dream"))

        return [e for e in events if e is not None]

    def check_special_day_events(self) -> Optional[Event]:
        """
        Check for special day events (holidays, days of week, time of day).

        Returns event if one should trigger, None otherwise.
        """
        now = datetime.now()
        current_time = time.time()

        # Create a unique key for this check period
        check_key = now.strftime("%Y-%m-%d-%H")

        # Don't spam check
        if check_key == self._last_special_check:
            return None

        self._last_special_check = check_key

        month = now.month
        day = now.day
        weekday = now.weekday()  # 0=Monday, 6=Sunday
        hour = now.hour

        events_to_check = []

        # Check holidays by date
        if month == 1 and day == 1:
            events_to_check.append("new_years")
        elif month == 2 and day == 14:
            events_to_check.append("valentines")
        elif month == 3 and 19 <= day <= 21:
            events_to_check.append("spring_equinox")
        elif month == 4 and day == 1:
            events_to_check.append("april_fools")
        elif month == 6 and 20 <= day <= 22:
            events_to_check.append("summer_solstice")
        elif month == 10 and day == 31:
            events_to_check.append("halloween")
        elif month == 11 and 22 <= day <= 28 and weekday == 3:  # 4th Thursday
            events_to_check.append("thanksgiving")
        elif month == 12 and 20 <= day <= 22:
            events_to_check.append("winter_solstice")
        elif month == 12 and day == 25:
            events_to_check.append("christmas")
        elif month == 12 and day == 31:
            events_to_check.append("new_years_eve")

        # Check day of week events
        if weekday == 6:  # Sunday
            events_to_check.append("lazy_sunday")
        elif weekday == 0:  # Monday
            events_to_check.append("monday_blues")
        elif weekday == 1:  # Tuesday
            events_to_check.append("taco_tuesday")
        elif weekday == 2:  # Wednesday
            events_to_check.append("hump_day")
        elif weekday == 4:  # Friday
            events_to_check.append("friday_vibes")

        # Check time of day events
        if 17 <= hour <= 19:  # Golden hour (5-7pm)
            events_to_check.append("golden_hour")
        elif 23 <= hour or hour <= 1:  # Midnight
            events_to_check.append("midnight_snack")

        # Check for rainy day based on actual weather
        rainy_weather_types = ["rainy", "heavy_rain", "drizzle", "spring_showers", "thunderstorm", "stormy"]
        if self._current_weather:
            # Handle both string and enum weather types
            weather_str = (
                self._current_weather.value 
                if hasattr(self._current_weather, 'value') 
                else str(self._current_weather)
            ).lower()
            if weather_str in rainy_weather_types:
                events_to_check.append("rainy_day")

        # Check which events can actually trigger
        for event_id in events_to_check:
            event = SPECIAL_DAY_EVENTS.get(event_id)
            if not event:
                continue

            # Check cooldown
            last_time = self._last_event_times.get(event_id, 0)
            if current_time - last_time < event.cooldown:
                continue

            # Roll probability
            if random.random() < event.probability:
                self._last_event_times[event_id] = current_time
                return event

        return None

    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "last_event_times": self._last_event_times,
            "last_any_event_time": self._last_any_event_time,
            "triggered_events": list(self._triggered_events),
            "current_weather": self._current_weather,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "EventSystem":
        """Create from dictionary."""
        system = cls()
        system._last_event_times = data.get("last_event_times", {})
        system._last_any_event_time = data.get("last_any_event_time", 0.0)
        system._triggered_events = set(data.get("triggered_events", []))
        system._current_weather = data.get("current_weather")
        return system


# ═══════════════════════════════════════════════════════════════════
#  Merge expanded events into main dictionaries
# ═══════════════════════════════════════════════════════════════════
try:
    from world.expanded_events import (
        EXPANDED_EVENTS,
        EXPANDED_ENCOUNTERS,
        EXPANDED_CHAINS,
    )
    EVENTS.update(EXPANDED_EVENTS)
    ENCOUNTERS.update(EXPANDED_ENCOUNTERS)
    EVENT_CHAINS.update(EXPANDED_CHAINS)
except ImportError:
    pass  # expanded_events module not available

# Global event system
event_system = EventSystem()
