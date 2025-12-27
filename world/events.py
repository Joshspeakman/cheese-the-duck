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
        message="*finds a crumb* Ooh!",
        duck_reaction="excited",
        sound="eat",
    ),
    "nice_breeze": Event(
        id="nice_breeze",
        name="Nice Breeze",
        description="A pleasant breeze ruffles the duck's feathers.",
        event_type=EventType.RANDOM,
        probability=0.03,
        effects={"fun": 5},
        mood_change=3,
        message="*feathers rustle* Ahh, nice...",
        duck_reaction="content",
    ),
    "butterfly": Event(
        id="butterfly",
        name="Butterfly Visit",
        description="A butterfly flutters by!",
        event_type=EventType.RANDOM,
        probability=0.02,
        effects={"fun": 10},
        mood_change=8,
        message="*watches butterfly* Ooooh pretty!",
        duck_reaction="curious",
    ),
    "found_shiny": Event(
        id="found_shiny",
        name="Found Something Shiny",
        description="The duck found something shiny!",
        event_type=EventType.RANDOM,
        probability=0.01,
        effects={"fun": 15},
        mood_change=10,
        message="*finds shiny thing* MINE!",
        duck_reaction="ecstatic",
        sound="alert",
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
        message="QUACK! ...wait why did I do that",
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
        message="*stops* ...what was I doing?",
        duck_reaction="confused",
        requires_stage="duckling",
    ),
    "stare_contest": Event(
        id="stare_contest",
        name="Staring Contest",
        description="The duck has a staring contest with nothing.",
        event_type=EventType.RANDOM,
        probability=0.03,
        effects={},
        mood_change=2,
        message="*intense staring at wall* ...I win!",
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
        message="*STARTLED* QUACK?!",
        duck_reaction="scared",
        sound="alert",
    ),
    "stubbed_toe": Event(
        id="stubbed_toe",
        name="Stubbed Toe",
        description="The duck stubbed its toe.",
        event_type=EventType.RANDOM,
        probability=0.02,
        effects={"fun": -3},
        mood_change=-3,
        message="*trips* Ow ow ow!",
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
        message="*wakes up startled* ...bad dream...",
        duck_reaction="scared",
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
        message="*basks in sunlight* So warm...",
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
        message="*plays in rain* Splish splash!",
        duck_reaction="playful",
        sound="splash",
        cooldown=1800,
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
        message="*excited quacking* Another duck!!",
        duck_reaction="ecstatic",
        sound="quack_excited",
        cooldown=600,
    ),
    "bird_friend": Event(
        id="bird_friend",
        name="Bird Friend",
        description="A small bird visits!",
        event_type=EventType.VISITOR,
        probability=0.01,
        effects={"social": 10},
        mood_change=5,
        message="*chirps at bird* Tweet tweet?",
        duck_reaction="friendly",
        cooldown=600,
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
        message="*wobbles* I... I'm walking!!",
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
        message="*opens beak* ...QUACK! I did it!",
        duck_reaction="ecstatic",
        sound="quack_happy",
        requires_stage="duckling",
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
        message="HAPPY NEW YEAR!! *celebratory quacking* May this year bring many crumbs!",
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
        message="*blushes* It's Valentine's Day! You... you remembered me? Quack! <3",
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
        message="*sniffs air* Ahh, spring! Everything smells so... alive! And full of bugs to eat!",
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
        message="*suspicious look* I don't trust ANYTHING today... Is that bread real? *pokes it*",
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
        message="*basking* Maximum sun! Maximum warmth! I could stay outside FOREVER! ...Is it naptime yet?",
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
        message="*wearing tiny pumpkin* BOO! Did I scare you?? ...No? *tries again* QUACK!! How about now?",
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
        message="*content sigh* I'm thankful for bread, for ponds, and for you. Mostly for bread though. ...Mostly.",
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
        message="*shivers* It's so dark... and cold... But that means more nap time, right? *hopeful look*",
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
        message="MERRY QUACKMAS!! *wearing tiny santa hat* Did you get me bread?? I got you a... *shows pebble* ...it's shiny!",
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

            # Check stage requirement
            if event.requires_stage:
                stages = ["egg", "duckling", "teen", "adult", "elder"]
                required_idx = stages.index(event.requires_stage) if event.requires_stage in stages else 0
                current_idx = stages.index(duck.growth_stage) if duck.growth_stage in stages else 0
                if current_idx < required_idx:
                    continue

            # Roll for event
            if random.random() < event.probability:
                self._last_event_times[event_id] = current_time
                return event

        return None

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
                    elif event_id == "first_quack" and trigger == "first_quack":
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

        # Random chance for rainy day
        if random.random() < 0.05:
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
