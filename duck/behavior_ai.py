"""
Utility-based behavior AI for autonomous duck actions.
Integrates with LLM for dynamic commentary when available.
"""
import random
import time
from typing import List, Tuple, Optional, TYPE_CHECKING
from dataclasses import dataclass
from enum import Enum

from config import AI_IDLE_INTERVAL, AI_RANDOMNESS, DERPY_RANDOMNESS_BONUS

if TYPE_CHECKING:
    from duck.duck import Duck

# Lazy import for LLM behavior controller
_llm_controller = None

def _get_llm_controller():
    """Lazy load LLM controller to avoid circular imports."""
    global _llm_controller
    if _llm_controller is None:
        try:
            from dialogue.llm_behavior import get_behavior_controller
            _llm_controller = get_behavior_controller()
        except ImportError:
            pass
    return _llm_controller


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
    # Structure-related actions
    NAP_IN_NEST = "nap_in_nest"
    HIDE_IN_SHELTER = "hide_in_shelter"
    USE_BIRD_BATH = "use_bird_bath"
    ADMIRE_GARDEN = "admire_garden"
    INSPECT_WORKBENCH = "inspect_workbench"


# Action data: base utility, need it helps with, personality affinity
ACTION_DATA = {
    AutonomousAction.IDLE: {
        "messages": [
            "*stands still*",
            "*blinks*",
            "*exists*",
            "*stares*",
        ],
        "base_utility": 0.1,
        "need_bonus": None,
        "personality_bonus": None,
        "duration": 8.0,
    },
    AutonomousAction.WADDLE: {
        "messages": [
            "*waddles*",
            "*waddle waddle*",
            "*waddles around*",
            "*waddles about*",
        ],
        "base_utility": 0.3,
        "need_bonus": ("fun", 0.3),
        "personality_bonus": ("active_lazy", 0.2),
        "duration": 10.0,
    },
    AutonomousAction.QUACK: {
        "messages": [
            "*QUACK!*",
            "*quack quack*",
            "*quack?*",
            "*quacks*",
            "*QUAAAACK!*",
        ],
        "base_utility": 0.25,
        "need_bonus": ("social", 0.4),
        "personality_bonus": ("social_shy", 0.3),
        "duration": 5.0,
    },
    AutonomousAction.PREEN: {
        "messages": [
            "*preens*",
            "*preens feathers*",
            "*fluffs up*",
        ],
        "base_utility": 0.2,
        "need_bonus": ("cleanliness", 0.5),
        "personality_bonus": ("neat_messy", -0.3),  # Neat ducks preen more
        "duration": 15.0,
        "effect": {"cleanliness": 0.3},  # Small boost, doesn't prevent decay
    },
    AutonomousAction.NAP: {
        "messages": [
            "*naps*",
            "*zzZ...*",
            "*dozes off*",
            "*snoozes*",
        ],
        "base_utility": 0.15,
        "need_bonus": ("energy", 0.6),
        "personality_bonus": ("active_lazy", -0.4),  # Lazy ducks nap more
        "duration": 25.0,
        "effect": {"energy": 0.5},  # Small boost, doesn't prevent decay
    },
    AutonomousAction.LOOK_AROUND: {
        "messages": [
            "*looks around*",
            "*tilts head*",
            "*scans around*",
            "*peeks*",
        ],
        "base_utility": 0.2,
        "need_bonus": ("fun", 0.2),
        "personality_bonus": ("brave_timid", 0.2),
        "duration": 8.0,
    },
    AutonomousAction.SPLASH: {
        "messages": [
            "*splashes*",
            "*SPLASH SPLASH*",
            "*splashes about*",
            "*splish splash*",
        ],
        "base_utility": 0.25,
        "need_bonus": ("fun", 0.5),
        "personality_bonus": ("active_lazy", 0.3),
        "duration": 12.0,
        "effect": {"fun": 0.4, "cleanliness": -0.2},  # Small effects
    },
    AutonomousAction.STARE_BLANKLY: {
        "messages": [
            "*stares blankly*",
            "*zones out*",
            "*...*",
            "*stares*",
        ],
        "base_utility": 0.15,
        "need_bonus": None,
        "personality_bonus": ("clever_derpy", -0.5),  # Derpy ducks do this more
        "duration": 12.0,
    },
    AutonomousAction.CHASE_BUG: {
        "messages": [
            "*chases bug*",
            "*spots a bug!*",
            "*pounces*",
            "*chases*",
        ],
        "base_utility": 0.2,
        "need_bonus": ("fun", 0.4),
        "personality_bonus": ("clever_derpy", -0.3),
        "duration": 10.0,
        "effect": {"fun": 0.3, "energy": -0.2},  # Small effects
    },
    AutonomousAction.FLAP_WINGS: {
        "messages": [
            "*flaps wings*",
            "*flap flap flap*",
            "*flaps*",
            "*flapping*",
        ],
        "base_utility": 0.2,
        "need_bonus": ("energy", 0.3),
        "personality_bonus": ("active_lazy", 0.3),
        "duration": 6.0,
        "effect": {"energy": -0.1},  # Small energy cost
    },
    AutonomousAction.WIGGLE: {
        "messages": [
            "*wiggles*",
            "*wiggle wiggle*",
            "*tail waggle*",
            "*wiggles about*",
        ],
        "base_utility": 0.25,
        "need_bonus": ("fun", 0.3),
        "personality_bonus": ("social_shy", 0.2),
        "duration": 5.0,
    },
    AutonomousAction.TRIP: {
        "messages": [
            "*trips*",
            "*stumbles*",
            "*faceplants*",
            "*falls over*",
        ],
        "base_utility": 0.05,
        "need_bonus": None,
        "personality_bonus": ("clever_derpy", -0.6),  # Very derpy behavior
        "duration": 4.0,
    },
    # Structure-related actions (these require structures to be available)
    AutonomousAction.NAP_IN_NEST: {
        "messages": [
            "*curls up in nest*",
            "*nestles in*",
            "*snuggles in nest*",
            "*settles into nest*",
        ],
        "base_utility": 0.0,  # Only available when nest exists
        "need_bonus": ("energy", 0.8),
        "personality_bonus": ("active_lazy", -0.3),
        "duration": 30.0,
        "effect": {"energy": 1.0},  # Better than regular nap but still small
        "requires_structure": "nest",
    },
    AutonomousAction.HIDE_IN_SHELTER: {
        "messages": [
            "*hides*",
            "*shelters inside*",
            "*takes cover*",
            "*peeks out*",
        ],
        "base_utility": 0.0,  # Only used during bad weather
        "need_bonus": None,
        "personality_bonus": ("brave_timid", -0.4),
        "duration": 20.0,
        "effect": {"energy": 0.2},  # Small energy conservation
        "requires_structure": "shelter",
    },
    AutonomousAction.USE_BIRD_BATH: {
        "messages": [
            "*splashes in bath*",
            "*bathes*",
            "*soaks in bath*",
            "*bath time*",
        ],
        "base_utility": 0.0,  # Only when bird bath exists
        "need_bonus": ("cleanliness", 0.7),
        "personality_bonus": ("neat_messy", -0.2),
        "duration": 18.0,
        "effect": {"cleanliness": 0.8, "fun": 0.3},  # Better than preening but still small
        "requires_structure": "bird_bath",
    },
    AutonomousAction.ADMIRE_GARDEN: {
        "messages": [
            "*sniffs flowers*",
            "*inspects garden*",
            "*admires plants*",
            "*watches garden*",
        ],
        "base_utility": 0.0,  # Only when garden exists
        "need_bonus": ("fun", 0.3),
        "personality_bonus": None,
        "duration": 12.0,
        "effect": {"fun": 0.2},  # Small entertainment
        "requires_structure": "garden_plot",
    },
    AutonomousAction.INSPECT_WORKBENCH: {
        "messages": [
            "*inspects workbench*",
            "*examines tools*",
            "*pokes around*",
            "*reorganizes*",
        ],
        "base_utility": 0.0,  # Only when workbench exists
        "need_bonus": None,
        "personality_bonus": ("clever_derpy", 0.3),
        "duration": 10.0,
        "requires_structure": "workbench",
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
        
        # Context for structure-aware behavior
        self._available_structures: set = set()  # Set of available structure types
        self._is_bad_weather: bool = False  # Whether to seek shelter
        self._weather_type: Optional[str] = None  # Current weather type
        
        # Structure positions for duck movement (structure_id -> (x, y) playfield coords)
        self._structure_positions: dict = {}
        
        # Movement callback support
        self._pending_action: Optional[ActionResult] = None  # Action to perform after reaching target
        self._movement_requested: bool = False  # Whether we're waiting for duck to move

    def set_context(self, available_structures: set = None, 
                    is_bad_weather: bool = False, weather_type: str = None,
                    structure_positions: dict = None):
        """Set context for structure-aware behavior decisions."""
        if available_structures is not None:
            self._available_structures = available_structures
        self._is_bad_weather = is_bad_weather
        self._weather_type = weather_type
        if structure_positions is not None:
            self._structure_positions = structure_positions

    def get_structure_position(self, structure_type: str) -> Optional[Tuple[int, int]]:
        """Get playfield position for a structure the duck should walk to."""
        # Map abstract structure types to actual structure IDs
        struct_mapping = {
            "nest": ["basic_nest", "cozy_nest", "deluxe_nest"],
            "shelter": ["basic_nest", "cozy_nest", "deluxe_nest", 
                       "mud_hut", "wooden_cottage", "stone_house"],
            "bird_bath": ["bird_bath"],
            "garden_plot": ["garden_plot"],
            "workbench": ["workbench"],
        }
        
        # Check if we have a specific position for this type
        if structure_type in self._structure_positions:
            return self._structure_positions[structure_type]
        
        # Check if this is an abstract type that maps to actual structures
        if structure_type in struct_mapping:
            for actual_struct in struct_mapping[structure_type]:
                if actual_struct in self._structure_positions:
                    return self._structure_positions[actual_struct]
        
        # Check variations (e.g., "nest" matches "basic_nest")
        for struct_id, pos in self._structure_positions.items():
            if structure_type in struct_id or struct_id in structure_type:
                return pos
        
        return None

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
        Uses LLM for dynamic commentary when available.

        Args:
            duck: The duck entity
            current_time: Current time in seconds

        Returns:
            ActionResult if action performed, None otherwise
        """
        if not self.should_act(current_time):
            return None

        result = self.select_action(duck)
        
        # Check if this action requires walking to a structure
        data = ACTION_DATA.get(result.action, {})
        required_struct = data.get("requires_structure")
        
        if required_struct:
            # Get the position of the structure
            struct_pos = self.get_structure_position(required_struct)
            if struct_pos:
                # Store the pending action and request movement
                self._pending_action = result
                self._movement_requested = True
                
                # Return a "walking to" message instead
                walk_messages = {
                    "nest": "*waddles toward nest*",
                    "shelter": "*waddles toward shelter*",
                    "bird_bath": "*waddles toward bird bath*",
                    "garden_plot": "*waddles toward garden*",
                    "workbench": "*waddles toward workbench*",
                }
                walk_msg = walk_messages.get(required_struct, f"*waddles toward {required_struct}*")
                
                # Update timing for the walk
                self._last_action_time = current_time
                duck.set_action_message(walk_msg, duration=5.0)
                
                # Return info about needing to move (caller should handle movement)
                return ActionResult(
                    action=result.action,
                    message=walk_msg,
                    duration=result.duration,
                    effects={},  # No effects during walking
                )

        # Try to get LLM-generated commentary (seamlessly falls back to template)
        controller = _get_llm_controller()
        if controller:
            controller.set_duck(duck)
            
            # Register fallback templates for this action
            data = ACTION_DATA.get(result.action, {})
            controller.register_fallback_templates(
                result.action.value, 
                data.get("messages", [result.message])
            )
            
            # Capture duration for callback closure
            action_duration = result.duration
            
            # Create callback to update duck message when LLM response is ready
            def on_llm_response(response: Optional[str]):
                if response and duck:
                    duck.set_action_message(response, duration=action_duration)
            
            # Request LLM commentary with template fallback and callback
            llm_message = controller.request_action_commentary(
                duck=duck,
                action=result.action.value,
                weather=self._weather_type or "clear",
                time_of_day="day",  # Could be enhanced with actual time
                fallback=result.message,
                callback=on_llm_response
            )
            
            if llm_message:
                result = ActionResult(
                    action=result.action,
                    message=llm_message,
                    duration=result.duration,
                    effects=result.effects
                )

        # Apply effects
        for need, change in result.effects.items():
            if hasattr(duck.needs, need):
                current = getattr(duck.needs, need)
                setattr(duck.needs, need, max(0, min(100, current + change)))

        # Update timing
        self._last_action_time = current_time
        self._current_action = result
        self._action_end_time = current_time + result.duration

        # Set action on duck for display (message lasts for the action duration)
        duck.current_action = result.action.value
        duck.set_action_message(result.message, duration=result.duration)

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
            # Skip structure-dependent actions if structure not available
            required_struct = data.get("requires_structure")
            if required_struct:
                # Map structure types to what we track
                struct_mapping = {
                    "nest": ["basic_nest", "cozy_nest", "deluxe_nest"],
                    "shelter": ["basic_nest", "cozy_nest", "deluxe_nest", 
                               "mud_hut", "wooden_cottage", "stone_house"],
                    "bird_bath": ["bird_bath"],
                    "garden_plot": ["garden_plot"],
                    "workbench": ["workbench"],
                }
                required_ids = struct_mapping.get(required_struct, [required_struct])
                has_structure = any(s in self._available_structures for s in required_ids)
                
                if not has_structure:
                    continue  # Skip this action entirely
            
            score = data["base_utility"]
            
            # Structure-based actions get bonus utility when available
            if required_struct:
                score = 0.25  # Base utility when structure exists
                
                # HIDE_IN_SHELTER gets massive bonus during bad weather
                if action == AutonomousAction.HIDE_IN_SHELTER and self._is_bad_weather:
                    score = 0.8  # Very high utility during storms
                
                # NAP_IN_NEST preferred over regular NAP
                if action == AutonomousAction.NAP_IN_NEST:
                    need_value = getattr(duck.needs, "energy", 50)
                    if need_value < 40:  # Tired duck prefers nest
                        score = 0.6

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
            
            # Weather influences for non-structure actions
            if self._is_bad_weather:
                # Reduce outdoor activity scores during bad weather
                outdoor_actions = [AutonomousAction.WADDLE, AutonomousAction.SPLASH,
                                   AutonomousAction.CHASE_BUG, AutonomousAction.LOOK_AROUND]
                if action in outdoor_actions:
                    score *= 0.5

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
    
    def has_pending_movement(self) -> bool:
        """Check if there's a pending action that requires duck movement."""
        return self._movement_requested and self._pending_action is not None
    
    def get_pending_movement_target(self) -> Optional[Tuple[int, int]]:
        """Get the target position for pending movement."""
        if not self._pending_action:
            return None
        
        data = ACTION_DATA.get(self._pending_action.action, {})
        required_struct = data.get("requires_structure")
        if required_struct:
            return self.get_structure_position(required_struct)
        return None
    
    def complete_movement(self, duck: "Duck", current_time: float) -> Optional[ActionResult]:
        """
        Called when duck reaches the target structure.
        Performs the actual action that was pending.
        """
        if not self._pending_action:
            return None
        
        result = self._pending_action
        self._pending_action = None
        self._movement_requested = False
        
        # Apply effects now that we're at the structure
        for need, change in result.effects.items():
            if hasattr(duck.needs, need):
                current = getattr(duck.needs, need)
                setattr(duck.needs, need, max(0, min(100, current + change)))
        
        # Update timing
        self._current_action = result
        self._action_end_time = current_time + result.duration
        
        # Set action on duck
        duck.current_action = result.action.value
        duck.set_action_message(result.message, duration=result.duration)
        
        return result
    
    def cancel_pending_movement(self):
        """Cancel any pending movement/action."""
        self._pending_action = None
        self._movement_requested = False
