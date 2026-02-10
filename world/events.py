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
    has_animation: bool = False  # whether this event has a visual animation
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


class EventSystem:
    """
    Manages game events including special day events.
    """

    def __init__(self):
        self._last_event_times: Dict[str, float] = {}
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

        for event_id, event in EVENTS.items():
            if event.event_type not in [EventType.RANDOM, EventType.WEATHER, EventType.VISITOR]:
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
            "triggered_events": list(self._triggered_events),
            "current_weather": self._current_weather,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "EventSystem":
        """Create from dictionary."""
        system = cls()
        system._last_event_times = data.get("last_event_times", {})
        system._triggered_events = set(data.get("triggered_events", []))
        system._current_weather = data.get("current_weather")
        return system


# Global event system
event_system = EventSystem()
