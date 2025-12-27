"""
Utility-based behavior AI for autonomous duck actions.
"""
import random
import time
from typing import List, Tuple, Optional, TYPE_CHECKING
from dataclasses import dataclass
from enum import Enum

from config import AI_IDLE_INTERVAL, AI_RANDOMNESS, DERPY_RANDOMNESS_BONUS

if TYPE_CHECKING:
    from duck.duck import Duck


class AutonomousAction(Enum):
    """Actions the duck can perform autonomously."""
    IDLE = "idle"
    WADDLE = "waddle"
    QUACK = "quack"
    PREEN = "preen"
    NAP = "nap"
    LOOK_AROUND = "look_around"
    SPLASH = "splash"
    STARE_BLANKLY = "stare_blankly"
    CHASE_BUG = "chase_bug"
    FLAP_WINGS = "flap_wings"
    WIGGLE = "wiggle"
    TRIP = "trip"


# Action data: base utility, need it helps with, personality affinity
ACTION_DATA = {
    AutonomousAction.IDLE: {
        "messages": [
            "*stands there*",
            "*blinks*",
            "*exists quietly*",
        ],
        "base_utility": 0.1,
        "need_bonus": None,
        "personality_bonus": None,
        "duration": 2.0,
    },
    AutonomousAction.WADDLE: {
        "messages": [
            "*waddle waddle*",
            "*waddles around happily*",
            "*waddles in a circle*",
            "*waddles to nowhere in particular*",
        ],
        "base_utility": 0.3,
        "need_bonus": ("fun", 0.3),
        "personality_bonus": ("active_lazy", 0.2),
        "duration": 3.0,
    },
    AutonomousAction.QUACK: {
        "messages": [
            "QUACK!",
            "Quack quack!",
            "quack?",
            "*enthusiastic quacking*",
            "QUAAAACK!",
        ],
        "base_utility": 0.25,
        "need_bonus": ("social", 0.4),
        "personality_bonus": ("social_shy", 0.3),
        "duration": 1.5,
    },
    AutonomousAction.PREEN: {
        "messages": [
            "*preens feathers*",
            "*carefully arranges feathers*",
            "*fluffs up*",
        ],
        "base_utility": 0.2,
        "need_bonus": ("cleanliness", 0.5),
        "personality_bonus": ("neat_messy", -0.3),  # Neat ducks preen more
        "duration": 4.0,
        "effect": {"cleanliness": 3},
    },
    AutonomousAction.NAP: {
        "messages": [
            "*takes a little nap*",
            "zzZ...",
            "*dozes off briefly*",
            "*sleepy duck noises*",
        ],
        "base_utility": 0.15,
        "need_bonus": ("energy", 0.6),
        "personality_bonus": ("active_lazy", -0.4),  # Lazy ducks nap more
        "duration": 5.0,
        "effect": {"energy": 5},
    },
    AutonomousAction.LOOK_AROUND: {
        "messages": [
            "*looks around curiously*",
            "*tilts head*",
            "*scans the area*",
            "*notices something interesting*",
        ],
        "base_utility": 0.2,
        "need_bonus": ("fun", 0.2),
        "personality_bonus": ("brave_timid", 0.2),
        "duration": 2.5,
    },
    AutonomousAction.SPLASH: {
        "messages": [
            "*splashes in puddle*",
            "*SPLASH SPLASH*",
            "*happy water noises*",
            "*gets a bit wet*",
        ],
        "base_utility": 0.25,
        "need_bonus": ("fun", 0.5),
        "personality_bonus": ("active_lazy", 0.3),
        "duration": 3.0,
        "effect": {"fun": 5, "cleanliness": -2},
    },
    AutonomousAction.STARE_BLANKLY: {
        "messages": [
            "*stares at nothing*",
            "*vacant expression*",
            "...",
            "*thinking about... wait what*",
            "*forgot what it was doing*",
            "*stares at wall*",
        ],
        "base_utility": 0.15,
        "need_bonus": None,
        "personality_bonus": ("clever_derpy", -0.5),  # Derpy ducks do this more
        "duration": 3.0,
    },
    AutonomousAction.CHASE_BUG: {
        "messages": [
            "*chases imaginary bug*",
            "*THERE'S A BUG wait no*",
            "*pounces on nothing*",
            "*very focused on... something*",
        ],
        "base_utility": 0.2,
        "need_bonus": ("fun", 0.4),
        "personality_bonus": ("clever_derpy", -0.3),
        "duration": 3.5,
        "effect": {"fun": 3, "energy": -2},
    },
    AutonomousAction.FLAP_WINGS: {
        "messages": [
            "*flap flap flap*",
            "*flaps excitedly*",
            "*attempts to fly* ...nope",
            "*dramatic wing flapping*",
        ],
        "base_utility": 0.2,
        "need_bonus": ("energy", 0.3),
        "personality_bonus": ("active_lazy", 0.3),
        "duration": 2.0,
        "effect": {"energy": -1},
    },
    AutonomousAction.WIGGLE: {
        "messages": [
            "*wiggles happily*",
            "*excited wiggling*",
            "*tail waggle*",
            "*whole body wiggle*",
        ],
        "base_utility": 0.25,
        "need_bonus": ("fun", 0.3),
        "personality_bonus": ("social_shy", 0.2),
        "duration": 1.5,
    },
    AutonomousAction.TRIP: {
        "messages": [
            "*trips over nothing*",
            "*stumbles* I meant to do that!",
            "*faceplants* ...quack",
            "*falls over own feet*",
        ],
        "base_utility": 0.05,
        "need_bonus": None,
        "personality_bonus": ("clever_derpy", -0.6),  # Very derpy behavior
        "duration": 2.0,
    },
}


@dataclass
class ActionResult:
    """Result of an autonomous action."""
    action: AutonomousAction
    message: str
    duration: float
    effects: dict


class BehaviorAI:
    """
    Utility-based AI that selects autonomous actions for the duck.
    """

    def __init__(self):
        self._last_action_time = 0.0
        self._last_action: Optional[AutonomousAction] = None
        self._action_history: List[AutonomousAction] = []
        self._current_action: Optional[ActionResult] = None
        self._action_end_time: float = 0.0

    def should_act(self, current_time: float) -> bool:
        """Check if it's time for a new autonomous action."""
        if self._current_action and current_time < self._action_end_time:
            return False
        return current_time - self._last_action_time >= AI_IDLE_INTERVAL

    def select_action(self, duck: "Duck") -> ActionResult:
        """
        Select the best action based on utility scoring.

        Args:
            duck: The duck entity

        Returns:
            ActionResult with chosen action and message
        """
        scores = self._calculate_utilities(duck)

        # Add randomness based on personality
        derpy_level = -duck.get_personality_trait("clever_derpy")  # Negative = derpy
        randomness = AI_RANDOMNESS + (derpy_level / 100) * DERPY_RANDOMNESS_BONUS

        # Add random noise to scores
        noisy_scores = [
            (action, score + random.uniform(0, randomness))
            for action, score in scores
        ]

        # Reduce score for recently performed actions
        for i, (action, score) in enumerate(noisy_scores):
            if action == self._last_action:
                noisy_scores[i] = (action, score * 0.3)
            elif action in self._action_history[-3:]:
                noisy_scores[i] = (action, score * 0.6)

        # Sort by score and pick the best
        noisy_scores.sort(key=lambda x: x[1], reverse=True)
        chosen_action = noisy_scores[0][0]

        # Get action data
        data = ACTION_DATA[chosen_action]
        message = random.choice(data["messages"])

        # Record this action
        self._last_action = chosen_action
        self._action_history.append(chosen_action)
        if len(self._action_history) > 10:
            self._action_history.pop(0)

        return ActionResult(
            action=chosen_action,
            message=message,
            duration=data["duration"],
            effects=data.get("effect", {}),
        )

    def perform_action(self, duck: "Duck", current_time: float) -> Optional[ActionResult]:
        """
        Perform an autonomous action if appropriate.

        Args:
            duck: The duck entity
            current_time: Current time in seconds

        Returns:
            ActionResult if action performed, None otherwise
        """
        if not self.should_act(current_time):
            return None

        result = self.select_action(duck)

        # Apply effects
        for need, change in result.effects.items():
            if hasattr(duck.needs, need):
                current = getattr(duck.needs, need)
                setattr(duck.needs, need, max(0, min(100, current + change)))

        # Update timing
        self._last_action_time = current_time
        self._current_action = result
        self._action_end_time = current_time + result.duration

        # Set action on duck for display
        duck.current_action = result.action.value
        duck.set_action_message(result.message)

        return result

    def _calculate_utilities(self, duck: "Duck") -> List[Tuple[AutonomousAction, float]]:
        """
        Calculate utility scores for all possible actions.

        Args:
            duck: The duck entity

        Returns:
            List of (action, score) tuples
        """
        scores = []

        for action, data in ACTION_DATA.items():
            score = data["base_utility"]

            # Add bonus based on relevant need (lower need = higher bonus)
            if data["need_bonus"]:
                need_name, bonus_weight = data["need_bonus"]
                need_value = getattr(duck.needs, need_name, 50)
                # Invert: low need value = high bonus
                need_urgency = (100 - need_value) / 100
                score += need_urgency * bonus_weight

            # Add bonus based on personality alignment
            if data["personality_bonus"]:
                trait_name, trait_weight = data["personality_bonus"]
                trait_value = duck.get_personality_trait(trait_name)
                # Positive trait_weight means high trait = more likely
                # Negative trait_weight means low trait = more likely
                trait_influence = (trait_value / 100) * trait_weight
                score += trait_influence

            # Mood influences
            mood = duck.get_mood()
            if mood.state.value in ["happy", "ecstatic"]:
                # Happy ducks are more active
                if action in [AutonomousAction.WADDLE, AutonomousAction.WIGGLE,
                              AutonomousAction.SPLASH, AutonomousAction.FLAP_WINGS]:
                    score += 0.1
            elif mood.state.value in ["sad", "miserable"]:
                # Sad ducks prefer calmer actions
                if action in [AutonomousAction.IDLE, AutonomousAction.NAP,
                              AutonomousAction.STARE_BLANKLY]:
                    score += 0.15

            scores.append((action, max(0, score)))

        return scores

    def get_current_action(self) -> Optional[ActionResult]:
        """Get the currently executing action, if any."""
        if time.time() < self._action_end_time:
            return self._current_action
        return None

    def is_busy(self) -> bool:
        """Check if duck is currently performing an action."""
        return time.time() < self._action_end_time

    def clear_action(self):
        """Clear the current action."""
        self._current_action = None
        self._action_end_time = 0
