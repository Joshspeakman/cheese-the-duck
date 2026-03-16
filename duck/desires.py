"""
Duck Desires — Daily agenda, motivation, and interaction resistance.

Cheese generates 3 hidden daily goals based on personality, mood, needs,
and growth stage. Goals are invisible to the player — discovered only
through body language and behavior. Mood-driven motivation scales from
full responsiveness down to complete nest-refusal shutdown.

Works identically with and without LLM — LLM enriches flavor text only.
"""
import random
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from duck.duck import Duck
    from duck.mood import MoodState


# ── Goal types ────────────────────────────────────────────────────────
class GoalType(Enum):
    EXPLORE = "explore"          # Visit a specific location/biome
    SOCIALIZE = "socialize"      # Interact with player or visitor
    PLAY = "play"                # Have fun — toys, splashing, chasing
    REST = "rest"                # Nap, sleep, float, do nothing
    FORAGE = "forage"            # Get fed / find food
    GROOM = "groom"              # Preen, bathe, get clean
    ADVENTURE = "adventure"      # Perform biome action at specific location
    CREATIVE = "creative"        # Learn trick, inspect workbench, discover


class TimeSlot(Enum):
    MORNING = "morning"    # First third of session
    MIDDAY = "midday"      # Middle third
    EVENING = "evening"    # Last third


# ── Motivation tiers ──────────────────────────────────────────────────
class MotivationTier(Enum):
    NORMAL = "normal"        # > 0.6  — full responsiveness
    SLUGGISH = "sluggish"    # 0.4-0.6 — slower, occasional refusal
    RESISTANT = "resistant"  # 0.2-0.4 — frequent refusal, gravitates to nest
    SHUTDOWN = "shutdown"    # < 0.2  — stays in nest, refuses nearly everything


# ── Daily goal dataclass ──────────────────────────────────────────────
@dataclass
class DailyGoal:
    goal_type: GoalType
    description: str                    # Internal description (not shown to player)
    priority: float                     # 0.0–1.0
    time_slot: TimeSlot
    target_location: Optional[str] = None   # Location name for EXPLORE/ADVENTURE
    target_action: Optional[str] = None     # Specific action for tracking
    progress: float = 0.0              # 0.0–1.0
    satisfied: bool = False

    def to_dict(self) -> dict:
        return {
            "goal_type": self.goal_type.value,
            "description": self.description,
            "priority": self.priority,
            "time_slot": self.time_slot.value,
            "target_location": self.target_location,
            "target_action": self.target_action,
            "progress": round(self.progress, 3),
            "satisfied": self.satisfied,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DailyGoal":
        return cls(
            goal_type=GoalType(data.get("goal_type", "rest")),
            description=data.get("description", ""),
            priority=data.get("priority", 0.5),
            time_slot=TimeSlot(data.get("time_slot", "morning")),
            target_location=data.get("target_location"),
            target_action=data.get("target_action"),
            progress=data.get("progress", 0.0),
            satisfied=data.get("satisfied", False),
        )


# ── Personality → GoalType mapping ────────────────────────────────────
# Maps personality trait extremes to preferred goal types.
# (trait, threshold, goal_type_if_above, goal_type_if_below)
PERSONALITY_GOAL_MAP = [
    ("active_lazy",  20, GoalType.EXPLORE,    GoalType.REST),
    ("social_shy",   20, GoalType.SOCIALIZE,  GoalType.REST),
    ("neat_messy",  -20, GoalType.GROOM,      GoalType.PLAY),
    ("brave_timid",  20, GoalType.ADVENTURE,  GoalType.REST),
    ("clever_derpy",  0, GoalType.CREATIVE,   GoalType.PLAY),
]

# Need → GoalType mapping for secondary goals
NEED_GOAL_MAP = {
    "hunger": GoalType.FORAGE,
    "energy": GoalType.REST,
    "fun": GoalType.PLAY,
    "cleanliness": GoalType.GROOM,
    "social": GoalType.SOCIALIZE,
}

# Mood → goal bias overrides
MOOD_GOAL_BIAS: Dict[str, List[GoalType]] = {
    "sad": [GoalType.REST, GoalType.REST, GoalType.GROOM],
    "miserable": [GoalType.REST, GoalType.REST, GoalType.REST],
    "ecstatic": [GoalType.ADVENTURE, GoalType.PLAY, GoalType.EXPLORE],
    "happy": [GoalType.PLAY, GoalType.EXPLORE, GoalType.SOCIALIZE],
    "dramatic": [GoalType.ADVENTURE, GoalType.CREATIVE, GoalType.SOCIALIZE],
    "petty": [GoalType.REST, GoalType.GROOM, GoalType.REST],
}

# Goal descriptions per type (internal, hidden from player)
GOAL_DESCRIPTIONS: Dict[GoalType, List[str]] = {
    GoalType.EXPLORE: [
        "wants to visit {location}",
        "feels like exploring {location}",
        "has an itch to waddle toward {location}",
    ],
    GoalType.SOCIALIZE: [
        "wants attention from the human",
        "craving some social interaction",
        "needs someone to talk at",
    ],
    GoalType.PLAY: [
        "wants to play with something",
        "feeling restless and playful",
        "needs to chase or splash",
    ],
    GoalType.REST: [
        "just wants to nap in the nest",
        "needs to do absolutely nothing",
        "wants a long peaceful rest",
    ],
    GoalType.FORAGE: [
        "hungry and wants food",
        "thinking about bread again",
        "stomach is making demands",
    ],
    GoalType.GROOM: [
        "wants to get clean",
        "feathers need attention",
        "craving a good bath",
    ],
    GoalType.ADVENTURE: [
        "wants to do something exciting at {location}",
        "feels adventurous about {location}",
        "drawn toward something at {location}",
    ],
    GoalType.CREATIVE: [
        "wants to learn something new",
        "feeling curious and inventive",
        "itching to tinker or discover",
    ],
}

# Locations for explore/adventure goals (subset of world/exploration.py locations)
EXPLORABLE_LOCATIONS = [
    "Home Pond", "Deep End", "Forest Edge", "Ancient Oak",
    "Mushroom Grove", "Sunny Meadow", "Butterfly Garden",
    "Pebble Beach", "Waterfall", "Vegetable Patch", "Tool Shed",
    "Foothills", "Crystal Cave", "Sandy Shore", "Shipwreck Cove",
    "Misty Marsh", "Cypress Hollow", "Sunken Ruins",
    "Park Fountain", "Rooftop Garden", "Storm Drain",
]


# ── Refusal messages ─────────────────────────────────────────────────
REFUSAL_MESSAGES: Dict[str, List[str]] = {
    "sluggish": [
        "*half-heartedly bats at the toy*",
        "*yawns mid-play*",
        "*moves at the speed of apathy*",
        "*starts, then gives up immediately*",
        "*blinks slowly in your direction*",
    ],
    "resistant": [
        "*turns away*",
        "*stares at the wall instead*",
        "*deliberately sits down*",
        "*sigh*... no.",
        "*pretends not to hear you*",
        "*pointedly looks at the nest instead*",
    ],
    "shutdown": [
        "*...*",
        "*doesn't move*",
        "*pretends to be asleep*",
        "",  # Empty — silence
        "*buried in the nest, unresponsive*",
        "*completely still*",
    ],
}


# ── Motivation mood multipliers ──────────────────────────────────────
MOOD_MOTIVATION_MULT: Dict[str, float] = {
    "ecstatic": 1.3,
    "happy": 1.1,
    "content": 1.0,
    "grumpy": 0.7,
    "sad": 0.5,
    "miserable": 0.2,
    "dramatic": 0.8,
    "petty": 0.6,
}


# ── GoalType → AutonomousAction mapping ──────────────────────────────
# Maps each goal type to the behavior_ai action enum value strings
# that advance the goal when performed.
GOAL_ACTION_MAP: Dict[GoalType, List[str]] = {
    GoalType.EXPLORE: ["biome_action", "waddle", "look_around"],
    GoalType.SOCIALIZE: ["quack", "look_around"],
    GoalType.PLAY: ["splash", "chase_bug", "wiggle", "flap_wings",
                     "play_with_toy", "splash_in_water"],
    GoalType.REST: ["nap", "nap_in_nest", "rest_on_furniture", "idle"],
    GoalType.FORAGE: ["look_around"],
    GoalType.GROOM: ["preen", "use_bird_bath"],
    GoalType.ADVENTURE: ["biome_action"],
    GoalType.CREATIVE: ["look_around", "inspect_workbench"],
}


class DuckDesires:
    """
    Generates and tracks daily goals. Computes motivation from mood.
    Handles interaction resistance when motivation is low.
    """

    def __init__(self):
        self.goals: List[DailyGoal] = []
        self._last_generated_date: str = ""         # ISO date of last generation
        self._session_start: float = time.time()     # When current session began
        self._goals_satisfied_today: int = 0
        self._all_satisfied_triggered: bool = False  # Bonus already given this cycle

    # ── Motivation calculation ────────────────────────────────────────

    @staticmethod
    def calculate_motivation(duck: "Duck") -> float:
        """
        Derive motivation (0.0–1.0) live from mood, needs, and personality.
        Not stored — always computed fresh.
        """
        mood_info = duck.get_mood()
        base = mood_info.score / 100.0

        # Mood multiplier
        mood_mult = MOOD_MOTIVATION_MULT.get(mood_info.state.value, 1.0)
        motivation = base * mood_mult

        # Low energy penalty
        if duck.needs.energy < 20:
            motivation *= 0.5

        # Sickness penalty
        if getattr(duck, 'is_sick', False):
            motivation *= 0.3

        # Personality overrides
        personality = duck.personality
        # Independent ducks don't let social need tank motivation
        independence = 0
        if hasattr(duck, '_personality_system') and duck._personality_system:
            ext = getattr(duck._personality_system, '_extended_traits', {})
            independence = ext.get('independence', 0)
        if independence > 30 and duck.needs.social < 20:
            motivation = max(motivation, 0.35)

        # Optimistic ducks recover motivation faster (floor is higher)
        optimism = 0
        if hasattr(duck, '_personality_system') and duck._personality_system:
            ext = getattr(duck._personality_system, '_extended_traits', {})
            optimism = ext.get('optimism', 0)
        if optimism > 30:
            motivation = max(motivation, 0.25)

        # Stubborn ducks maintain minimum motivation for their own goals
        stubbornness = 0
        if hasattr(duck, '_personality_system') and duck._personality_system:
            ext = getattr(duck._personality_system, '_extended_traits', {})
            stubbornness = ext.get('stubbornness', 0)
        if stubbornness > 40:
            motivation = max(motivation, 0.2)

        return max(0.0, min(1.0, motivation))

    @staticmethod
    def get_motivation_tier(motivation: float) -> MotivationTier:
        """Map motivation value to a tier."""
        if motivation > 0.6:
            return MotivationTier.NORMAL
        elif motivation > 0.4:
            return MotivationTier.SLUGGISH
        elif motivation > 0.2:
            return MotivationTier.RESISTANT
        return MotivationTier.SHUTDOWN

    # ── Interaction resistance ────────────────────────────────────────

    @staticmethod
    def check_interaction_refusal(duck: "Duck", interaction: str) -> Tuple[bool, str]:
        """
        Roll against motivation to see if the duck refuses a player command.

        Returns:
            (refused: bool, message: str)  — if refused is True, message
            contains the refusal text to display.
        """
        motivation = DuckDesires.calculate_motivation(duck)
        tier = DuckDesires.get_motivation_tier(motivation)

        if tier == MotivationTier.NORMAL:
            return False, ""

        # Feeding always has reduced refusal (even miserable ducks eat sometimes)
        if interaction == "feed":
            if tier == MotivationTier.SLUGGISH:
                return False, ""  # Always accepts food when sluggish
            elif tier == MotivationTier.RESISTANT:
                if random.random() < 0.2:  # 20% refuse
                    return True, random.choice(REFUSAL_MESSAGES["resistant"])
                return False, ""
            elif tier == MotivationTier.SHUTDOWN:
                if random.random() < 0.6:  # 60% refuse even food
                    return True, random.choice(REFUSAL_MESSAGES["shutdown"])
                return False, ""

        # Petting has chance to break through at low motivation
        if interaction == "pet":
            if tier == MotivationTier.RESISTANT:
                if random.random() < 0.3:  # 30% refuse (less than other actions)
                    return True, random.choice(REFUSAL_MESSAGES["resistant"])
                return False, ""
            elif tier == MotivationTier.SHUTDOWN:
                if random.random() < 0.7:  # 70% refuse
                    msg = random.choice(REFUSAL_MESSAGES["shutdown"])
                    return True, msg
                # Break through! Small mood boost handled by caller
                return False, "*reluctantly accepts*"

        # All other interactions
        refusal_chances = {
            MotivationTier.SLUGGISH: 0.2,
            MotivationTier.RESISTANT: 0.5,
            MotivationTier.SHUTDOWN: 0.9,
        }
        chance = refusal_chances.get(tier, 0.0)
        if random.random() < chance:
            tier_key = tier.value
            return True, random.choice(REFUSAL_MESSAGES.get(tier_key, [""]))

        return False, ""

    # ── Goal generation ───────────────────────────────────────────────

    def generate_daily_agenda(self, duck: "Duck",
                              unlocked_locations: Optional[List[str]] = None):
        """
        Generate 3 goals: primary (personality), secondary (needs),
        tertiary (random/aspirational). Mood filters the pool.
        """
        self.goals.clear()
        self._all_satisfied_triggered = False
        self._goals_satisfied_today = 0
        self._last_generated_date = datetime.now().strftime("%Y-%m-%d")

        mood_info = duck.get_mood()
        mood_key = mood_info.state.value
        locations = unlocked_locations or EXPLORABLE_LOCATIONS[:5]

        # ── Primary: personality-driven ───────────────────────────
        primary_type = self._pick_personality_goal(duck, mood_key)
        primary_loc = random.choice(locations) if primary_type in (
            GoalType.EXPLORE, GoalType.ADVENTURE) else None
        desc = self._make_description(primary_type, primary_loc)
        self.goals.append(DailyGoal(
            goal_type=primary_type,
            description=desc,
            priority=1.0,
            time_slot=TimeSlot.MORNING,
            target_location=primary_loc,
        ))

        # ── Secondary: need-driven ────────────────────────────────
        secondary_type = self._pick_need_goal(duck, mood_key)
        # Avoid duplicate type
        if secondary_type == primary_type:
            secondary_type = GoalType.PLAY if secondary_type != GoalType.PLAY else GoalType.REST
        secondary_loc = random.choice(locations) if secondary_type in (
            GoalType.EXPLORE, GoalType.ADVENTURE) else None
        desc = self._make_description(secondary_type, secondary_loc)
        self.goals.append(DailyGoal(
            goal_type=secondary_type,
            description=desc,
            priority=0.7,
            time_slot=TimeSlot.MIDDAY,
            target_location=secondary_loc,
        ))

        # ── Tertiary: random / aspirational ───────────────────────
        tertiary_type = self._pick_aspirational_goal(duck, mood_key)
        used = {primary_type, secondary_type}
        if tertiary_type in used:
            # Pick from remaining types
            remaining = [g for g in GoalType if g not in used]
            tertiary_type = random.choice(remaining) if remaining else GoalType.REST
        tertiary_loc = random.choice(locations) if tertiary_type in (
            GoalType.EXPLORE, GoalType.ADVENTURE) else None
        desc = self._make_description(tertiary_type, tertiary_loc)
        self.goals.append(DailyGoal(
            goal_type=tertiary_type,
            description=desc,
            priority=0.4,
            time_slot=TimeSlot.EVENING,
            target_location=tertiary_loc,
        ))

    def _pick_personality_goal(self, duck: "Duck", mood_key: str) -> GoalType:
        """Select a goal type weighted by personality traits."""
        # Check mood bias first
        if mood_key in MOOD_GOAL_BIAS:
            if random.random() < 0.5:  # 50% mood override
                return random.choice(MOOD_GOAL_BIAS[mood_key])

        # Score each goal type by personality
        scores: Dict[GoalType, float] = {}
        for trait, threshold, goal_above, goal_below in PERSONALITY_GOAL_MAP:
            val = duck.get_personality_trait(trait)
            if val > threshold:
                scores[goal_above] = scores.get(goal_above, 0) + abs(val) / 100
            else:
                scores[goal_below] = scores.get(goal_below, 0) + abs(val) / 100

        if not scores:
            return GoalType.PLAY

        # Weighted random selection
        types = list(scores.keys())
        weights = [scores[t] for t in types]
        return random.choices(types, weights=weights, k=1)[0]

    def _pick_need_goal(self, duck: "Duck", mood_key: str) -> GoalType:
        """Select a goal based on lowest need."""
        if mood_key in MOOD_GOAL_BIAS and random.random() < 0.3:
            return random.choice(MOOD_GOAL_BIAS[mood_key])

        needs_values = {
            "hunger": duck.needs.hunger,
            "energy": duck.needs.energy,
            "fun": duck.needs.fun,
            "cleanliness": duck.needs.cleanliness,
            "social": duck.needs.social,
        }
        lowest_need = min(needs_values, key=needs_values.get)
        return NEED_GOAL_MAP.get(lowest_need, GoalType.PLAY)

    def _pick_aspirational_goal(self, duck: "Duck", mood_key: str) -> GoalType:
        """Pick a random goal influenced by age."""
        age_days = duck.get_age_days()
        if age_days < 7:
            # Young ducks want to explore
            pool = [GoalType.EXPLORE, GoalType.PLAY, GoalType.EXPLORE,
                    GoalType.CREATIVE, GoalType.SOCIALIZE]
        elif age_days > 60:
            # Elder ducks favor rest and socializing
            pool = [GoalType.REST, GoalType.SOCIALIZE, GoalType.GROOM,
                    GoalType.REST, GoalType.CREATIVE]
        else:
            pool = list(GoalType)

        if mood_key in MOOD_GOAL_BIAS and random.random() < 0.3:
            return random.choice(MOOD_GOAL_BIAS[mood_key])

        return random.choice(pool)

    def _make_description(self, goal_type: GoalType,
                          location: Optional[str] = None) -> str:
        templates = GOAL_DESCRIPTIONS.get(goal_type, ["wants something"])
        desc = random.choice(templates)
        if location and "{location}" in desc:
            desc = desc.replace("{location}", location)
        elif "{location}" in desc:
            desc = desc.replace("{location}", "somewhere new")
        return desc

    # ── Goal progress tracking ────────────────────────────────────────

    def get_active_goal(self) -> Optional[DailyGoal]:
        """
        Get the current priority goal based on session elapsed time.
        Falls back to highest-priority unsatisfied goal.
        """
        elapsed = time.time() - self._session_start
        # Divide session into thirds for time slots
        # Use ~40 min per third (2 hour nominal session)
        slot_duration = 40 * 60  # 40 minutes per slot
        if elapsed < slot_duration:
            target_slot = TimeSlot.MORNING
        elif elapsed < slot_duration * 2:
            target_slot = TimeSlot.MIDDAY
        else:
            target_slot = TimeSlot.EVENING

        # Find matching unsatisfied goal for this slot
        for goal in self.goals:
            if goal.time_slot == target_slot and not goal.satisfied:
                return goal

        # Fall back to any unsatisfied goal, highest priority first
        unsatisfied = [g for g in self.goals if not g.satisfied]
        if unsatisfied:
            return max(unsatisfied, key=lambda g: g.priority)
        return None

    def on_action_performed(self, action_value: str,
                            current_location: Optional[str] = None) -> bool:
        """
        Called when the duck performs an autonomous action.
        Increments progress on matching goals.

        Returns True if a goal was just satisfied.
        """
        active = self.get_active_goal()
        if not active or active.satisfied:
            return False

        aligned_actions = GOAL_ACTION_MAP.get(active.goal_type, [])
        if action_value not in aligned_actions:
            return False

        # Location check for explore/adventure goals
        if active.goal_type in (GoalType.EXPLORE, GoalType.ADVENTURE):
            if active.target_location and current_location:
                if active.target_location.lower() != current_location.lower():
                    # Still give tiny progress for exploring generally
                    active.progress = min(1.0, active.progress + 0.05)
                    return False
            # At the right location — big progress
            active.progress = min(1.0, active.progress + 0.35)
        else:
            # Non-location goals: moderate progress per aligned action
            active.progress = min(1.0, active.progress + 0.25)

        if active.progress >= 1.0:
            active.satisfied = True
            self._goals_satisfied_today += 1
            return True

        return False

    def on_need_satisfied(self, need_name: str, new_value: float):
        """
        Called when a need crosses a satisfaction threshold via interaction.
        Checks if it satisfies a FORAGE/REST/GROOM goal.
        """
        for goal in self.goals:
            if goal.satisfied:
                continue
            if goal.goal_type == GoalType.FORAGE and need_name == "hunger" and new_value > 60:
                goal.progress = 1.0
                goal.satisfied = True
                self._goals_satisfied_today += 1
            elif goal.goal_type == GoalType.REST and need_name == "energy" and new_value > 70:
                goal.progress = 1.0
                goal.satisfied = True
                self._goals_satisfied_today += 1
            elif goal.goal_type == GoalType.GROOM and need_name == "cleanliness" and new_value > 70:
                goal.progress = 1.0
                goal.satisfied = True
                self._goals_satisfied_today += 1

    def on_player_interaction(self, interaction: str):
        """
        Called when the player does an interaction (feed/play/pet/clean).
        Checks SOCIALIZE goal progress.
        """
        for goal in self.goals:
            if goal.satisfied:
                continue
            if goal.goal_type == GoalType.SOCIALIZE:
                goal.progress = min(1.0, goal.progress + 0.35)
                if goal.progress >= 1.0:
                    goal.satisfied = True
                    self._goals_satisfied_today += 1

    def all_goals_satisfied(self) -> bool:
        return len(self.goals) > 0 and all(g.satisfied for g in self.goals)

    def check_all_satisfied_bonus(self) -> bool:
        """Returns True once when all 3 goals are satisfied (for trust/diary bonus)."""
        if self.all_goals_satisfied() and not self._all_satisfied_triggered:
            self._all_satisfied_triggered = True
            return True
        return False

    # ── Regeneration checks ───────────────────────────────────────────

    def should_regenerate(self) -> bool:
        """Check if goals should be regenerated."""
        today = datetime.now().strftime("%Y-%m-%d")
        # New real calendar day
        if today != self._last_generated_date:
            return True
        # All goals satisfied
        if self.all_goals_satisfied():
            return True
        # No goals generated yet
        if not self.goals:
            return True
        return False

    def on_sleep_recovery(self, energy_before: float, energy_after: float):
        """Called when energy crosses 80 from below (duck slept well)."""
        if energy_before < 80 and energy_after >= 80:
            # Mark for regeneration by clearing date
            self._last_generated_date = ""

    def reset_session_timer(self):
        """Reset session start for time slot calculations."""
        self._session_start = time.time()

    # ── Utility boost for behavior AI ─────────────────────────────────

    def get_goal_utility_boost(self, action_value: str,
                                current_location: Optional[str] = None) -> float:
        """
        Returns a utility bonus (0.0–0.6) for actions aligned with the
        active goal. Used by behavior_ai._calculate_utilities().
        """
        active = self.get_active_goal()
        if not active:
            return 0.0

        aligned_actions = GOAL_ACTION_MAP.get(active.goal_type, [])
        if action_value not in aligned_actions:
            # Penalize actions that contradict the active goal
            return -0.1

        boost = 0.4 * active.priority

        # Extra boost if at the target location
        if active.target_location and current_location:
            if active.target_location.lower() == current_location.lower():
                boost += 0.2

        return boost

    def get_goal_suppression(self, action_value: str,
                              motivation: float) -> float:
        """
        Returns a penalty for actions that contradict the active goal.
        Reduced penalty when motivation is low (duck stops caring).
        """
        active = self.get_active_goal()
        if not active:
            return 0.0

        aligned = GOAL_ACTION_MAP.get(active.goal_type, [])
        if action_value in aligned:
            return 0.0  # No suppression for aligned actions

        # Low motivation = duck doesn't care about goals either
        if motivation < 0.4:
            return 0.0

        return -0.1

    # ── Serialization ─────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "goals": [g.to_dict() for g in self.goals],
            "last_generated_date": self._last_generated_date,
            "goals_satisfied_today": self._goals_satisfied_today,
            "all_satisfied_triggered": self._all_satisfied_triggered,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DuckDesires":
        desires = cls()
        desires.goals = [DailyGoal.from_dict(g) for g in data.get("goals", [])]
        desires._last_generated_date = data.get("last_generated_date", "")
        desires._goals_satisfied_today = data.get("goals_satisfied_today", 0)
        desires._all_satisfied_triggered = data.get("all_satisfied_triggered", False)
        return desires
