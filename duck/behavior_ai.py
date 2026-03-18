"""
Utility-based behavior AI for autonomous duck actions.
Integrates with LLM for dynamic commentary when available.
"""
import random
import time
from collections import deque
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
    # Item-based actions (shop items in habitat)
    PLAY_WITH_TOY = "play_with_toy"
    SPLASH_IN_WATER = "splash_in_water"
    REST_ON_FURNITURE = "rest_on_furniture"
    ADMIRE_DECORATION = "admire_decoration"
    # Radio action (requires nook_radio item)
    LISTEN_TO_RADIO = "listen_to_radio"
    # Biome-specific action (message chosen from biome_behaviors data)
    BIOME_ACTION = "biome_action"


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
        "effect": {"cleanliness": 1},  # Tiny self-care nudge
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
        "effect": {},  # Energy regen handled by game tick while napping
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
        "effect": {"fun": 1, "cleanliness": -1},  # Tiny nudge
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
        "effect": {"fun": 1, "energy": -1},  # Tiny nudge
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
        "effect": {"energy": -1},  # Small energy cost
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
        "effect": {},  # Energy regen handled by game tick while napping (nest is comfier)
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
        "effect": {"energy": 1},  # Small energy conservation
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
        "effect": {"cleanliness": 3, "fun": 1},  # Better than preening
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
        "effect": {"fun": 1},  # Small entertainment
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
    # === ITEM-BASED ACTIONS (shop items in habitat) ===
    AutonomousAction.PLAY_WITH_TOY: {
        "messages": [
            "*plays with toy*",
            "*bounces around happily*",
            "*has fun with toy*",
            "*entertains self*",
        ],
        "base_utility": 0.0,  # Only when toy items exist
        "need_bonus": ("fun", 0.6),
        "personality_bonus": ("active_lazy", 0.3),
        "duration": 15.0,
        "effect": {"fun": 4, "energy": -2},
        "requires_item_category": "toy",
    },
    AutonomousAction.SPLASH_IN_WATER: {
        "messages": [
            "*splashes in water*",
            "*makes little waves*",
            "*enjoys the water*",
            "*paddles around*",
        ],
        "base_utility": 0.0,  # Only when water items exist
        "need_bonus": ("cleanliness", 0.7),
        "personality_bonus": None,
        "duration": 18.0,
        "effect": {"cleanliness": 3, "fun": 2},
        "requires_item_category": "water",
    },
    AutonomousAction.REST_ON_FURNITURE: {
        "messages": [
            "*settles onto furniture*",
            "*relaxes comfortably*",
            "*takes a rest*",
            "*lounges contentedly*",
        ],
        "base_utility": 0.0,  # Only when furniture items exist
        "need_bonus": ("energy", 0.5),
        "personality_bonus": ("active_lazy", -0.3),
        "duration": 20.0,
        "effect": {"energy": 3},
        "requires_item_category": "furniture",
    },
    AutonomousAction.ADMIRE_DECORATION: {
        "messages": [
            "*admires decoration*",
            "*gazes at pretty thing*",
            "*appreciates surroundings*",
            "*looks around happily*",
        ],
        "base_utility": 0.0,  # Only when decoration/plant items exist
        "need_bonus": ("fun", 0.2),
        "personality_bonus": None,
        "duration": 8.0,
        "effect": {"fun": 1},
        "requires_item_category": "decoration",
    },
    # === RADIO ACTION (requires nook_radio ownership) ===
    AutonomousAction.LISTEN_TO_RADIO: {
        "messages": [
            "*bobs head to the music*",
            "*listens intently*",
            "*taps foot to the beat*",
            "*vibes quietly*",
            "*sways gently*",
            "*closes eyes and listens*",
        ],
        "base_utility": 0.0,  # Only when duck owns nook_radio
        "need_bonus": ("fun", 0.4),
        "personality_bonus": None,
        "duration": 25.0,
        "effect": {"fun": 3, "social": 1},
        "requires_radio": True,
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
        self._action_history: deque = deque(maxlen=10)
        self._current_action: Optional[ActionResult] = None
        self._action_end_time: float = 0.0
        
        # Context for structure-aware behavior
        self._available_structures: set = set()  # Set of available structure types
        self._is_bad_weather: bool = False  # Whether to seek shelter
        self._weather_type: Optional[str] = None  # Current weather type

        # Radio context
        self._has_radio: bool = False  # Whether duck owns nook_radio
        self._radio_playing: bool = False  # Whether radio is currently on

        # Structure positions for duck movement (structure_id -> (x, y) playfield coords)
        self._structure_positions: dict = {}

        # Item-based action context (shop items in habitat)
        self._available_items: dict = {}  # category -> list of item_ids
        self._selected_item: Optional[str] = None  # Item selected for current action
        
        # Biome context for location-specific behaviors
        self._current_biome: Optional[str] = None  # Current biome name (e.g. "pond", "forest")
        self._current_location: Optional[str] = None  # Location name (e.g. "Home Pond", "Forest Edge")
        self._field_width: int = 79   # Playfield width for zone coordinate conversion
        self._field_height: int = 25  # Playfield height for zone coordinate conversion
        self._biome_target_position: Optional[Tuple[int, int]] = None  # Target for biome movement
        self._biome_feature_tag: Optional[str] = None  # Feature tag for current biome action (water/vegetation/etc.)
        
        # Cooldown for item interactions (prevents constant item-to-item behavior)
        self._last_item_interaction_time: float = 0.0
        self._item_interaction_cooldown: float = 120.0  # Seconds between item interactions

        # Per-category satiation: tracks how many times duck has used each
        # category recently.  Each use adds 1; decays by 1 every 180s.
        # Higher satiation → lower utility for that category.
        self._item_satiation: dict = {}  # category -> (count, last_use_time)

        # Movement callback support
        self._pending_action: Optional[ActionResult] = None  # Action to perform after reaching target
        self._movement_requested: bool = False  # Whether we're waiting for duck to move

        # Desires/motivation context (set each tick from game loop)
        self._active_goal = None       # DailyGoal or None
        self._motivation: float = 1.0  # 0.0-1.0, from DuckDesires.calculate_motivation
        self._desires = None           # DuckDesires reference

    def record_item_interaction(self, category: str = None):
        """Record that an item interaction just occurred (for cooldown and satiation)."""
        self._last_item_interaction_time = time.time()
        if category:
            count, _ = self._item_satiation.get(category, (0, 0.0))
            self._item_satiation[category] = (count + 1, time.time())

    def _get_item_satiation(self, category: str) -> float:
        """Get satiation multiplier for a category (0.0 = fully bored, 1.0 = fresh).
        
        Each use adds 1 to counter; counter decays by 1 every 180s of non-use.
        Multiplier: 1.0 at 0, 0.5 at 1, 0.25 at 2, etc.
        """
        if category not in self._item_satiation:
            return 1.0
        count, last_time = self._item_satiation[category]
        # Decay: remove 1 count per 180s since last use
        elapsed = time.time() - last_time
        decayed_count = max(0, count - int(elapsed / 180.0))
        if decayed_count <= 0:
            del self._item_satiation[category]
            return 1.0
        self._item_satiation[category] = (decayed_count, last_time)
        # Halve utility for each stacked use
        return 0.5 ** decayed_count

    def is_item_interaction_on_cooldown(self) -> bool:
        """Check if item interactions are still on cooldown."""
        return time.time() - self._last_item_interaction_time < self._item_interaction_cooldown

    def get_item_cooldown_remaining(self) -> float:
        """Get seconds remaining on item interaction cooldown."""
        remaining = self._item_interaction_cooldown - (time.time() - self._last_item_interaction_time)
        return max(0.0, remaining)

    def _has_nest_available(self) -> bool:
        """Check if any nest structure is available for sleeping."""
        nest_structures = ["basic_nest", "cozy_nest", "deluxe_nest"]
        return any(s in self._available_structures for s in nest_structures)

    def set_context(self, available_structures: set = None,
                    is_bad_weather: bool = False, weather_type: str = None,
                    structure_positions: dict = None, placed_items: list = None,
                    current_biome: str = None, current_location: str = None,
                    field_width: int = None, field_height: int = None,
                    desires=None, motivation: float = None,
                    has_radio: bool = None, radio_playing: bool = None):
        """Set context for structure-aware and item-aware behavior decisions."""
        if available_structures is not None:
            self._available_structures = available_structures
        self._is_bad_weather = is_bad_weather
        self._weather_type = weather_type
        if structure_positions is not None:
            self._structure_positions = structure_positions
        if placed_items is not None:
            self._available_items = self._categorize_items(placed_items)
        if current_biome is not None:
            self._current_biome = current_biome
        if current_location is not None:
            self._current_location = current_location
        if field_width is not None:
            self._field_width = field_width
        if field_height is not None:
            self._field_height = field_height
        if desires is not None:
            self._desires = desires
            self._active_goal = desires.get_active_goal()
        if motivation is not None:
            self._motivation = motivation
        if has_radio is not None:
            self._has_radio = has_radio
        if radio_playing is not None:
            self._radio_playing = radio_playing

    def _categorize_items(self, placed_items: list) -> dict:
        """Categorize placed items by their shop category for AI decisions."""
        try:
            from world.shop import get_item, ItemCategory
        except ImportError:
            return {}

        categories = {
            "toy": [],
            "water": [],
            "furniture": [],
            "decoration": [],
            "plant": [],
        }

        for placed in placed_items:
            item = get_item(placed.item_id)
            if item:
                cat_name = item.category.value.lower()
                if cat_name in categories:
                    categories[cat_name].append(placed.item_id)
                # Plants and decorations both count as decoration for AI
                if cat_name == "plant":
                    categories["decoration"].append(placed.item_id)

        return categories

    def get_items_by_category(self, category: str) -> List[str]:
        """Get list of available item IDs for a category."""
        return self._available_items.get(category.lower(), [])

    def get_selected_item(self) -> Optional[str]:
        """Get the item selected for the current action (if item-based)."""
        return self._selected_item

    def clear_selected_item(self):
        """Clear the selected item after the action is handled."""
        self._selected_item = None

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
        """Check if it's time for a new autonomous action.
        
        Idle interval scales with motivation: low motivation → longer idle.
        """
        # Don't act if action end time is still in the future
        # (this handles both AI actions and user-initiated actions like sleep)
        if current_time < self._action_end_time:
            return False
        # Clear the current action when it has expired
        if self._current_action and current_time >= self._action_end_time:
            self._current_action = None
        # Scale idle interval: normal at 1.0, 3× at 0.2, 6× at <0.2
        mot = max(0.1, self._motivation)
        idle_scale = 1.0 + (1.0 - mot) * 5.0  # 1× at 1.0 → 6× at 0.0
        effective_interval = AI_IDLE_INTERVAL * idle_scale
        return current_time - self._last_action_time >= effective_interval

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
        item_actions = {AutonomousAction.PLAY_WITH_TOY, AutonomousAction.SPLASH_IN_WATER,
                        AutonomousAction.REST_ON_FURNITURE, AutonomousAction.ADMIRE_DECORATION}
        recent_had_item = any(a in item_actions for a in list(self._action_history)[-3:])

        for i, (action, score) in enumerate(noisy_scores):
            if action == self._last_action:
                noisy_scores[i] = (action, score * 0.3)
            elif action in list(self._action_history)[-3:]:
                noisy_scores[i] = (action, score * 0.6)
            # If ANY item action was recent, suppress ALL item actions
            elif recent_had_item and action in item_actions:
                noisy_scores[i] = (action, score * 0.4)

        # Sort by score and pick the best
        noisy_scores.sort(key=lambda x: x[1], reverse=True)
        chosen_action = noisy_scores[0][0]

        # Get action data — biome actions use special handling
        if chosen_action == AutonomousAction.BIOME_ACTION:
            message, duration, feature_tag = self._pick_biome_behavior()
            self._selected_item = None
            self._last_action = chosen_action
            self._action_history.append(chosen_action)
            # Compute target position from feature zone
            from duck.biome_behaviors import get_biome_target
            target = get_biome_target(
                self._current_location or "",
                feature_tag,
                self._field_width,
                self._field_height,
            )
            self._biome_target_position = target
            self._biome_feature_tag = feature_tag
            # Scale duration by motivation: low motivation = lingering
            scaled_duration = duration * (2.0 - self._motivation)
            return ActionResult(
                action=chosen_action,
                message=message,
                duration=scaled_duration,
                effects={"fun": 1},
            )

        # Get action data
        data = ACTION_DATA[chosen_action]
        message = random.choice(data["messages"])

        # If this is an item-based action, select a specific item
        required_item_cat = data.get("requires_item_category")
        if required_item_cat:
            available_items = self.get_items_by_category(required_item_cat)
            if available_items:
                self._selected_item = random.choice(available_items)
            else:
                # No items available for this action — pick next best action that doesn't need items
                for fallback_action, fallback_score in noisy_scores[1:]:
                    fb_data = ACTION_DATA.get(fallback_action, {})
                    if not fb_data.get("requires_item_category"):
                        chosen_action = fallback_action
                        data = fb_data
                        message = random.choice(data["messages"])
                        self._selected_item = None
                        break
                else:
                    # All candidates need items — force idle
                    self._selected_item = None
                    chosen_action = AutonomousAction.IDLE
                    data = ACTION_DATA[chosen_action]
                    message = random.choice(data["messages"])
        else:
            self._selected_item = None

        # Record this action
        self._last_action = chosen_action
        self._action_history.append(chosen_action)

        # Scale duration by motivation: low motivation = lingering on actions longer
        scaled_duration = data["duration"] * (2.0 - self._motivation)

        return ActionResult(
            action=chosen_action,
            message=message,
            duration=scaled_duration,
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
        
        # Check if biome action needs positional movement
        if result.action == AutonomousAction.BIOME_ACTION and self._biome_target_position:
            self._pending_action = result
            self._movement_requested = True
            walk_msg = "*waddles toward something interesting*"
            self._last_action_time = current_time
            duck.set_action_message(walk_msg, duration=5.0)
            return ActionResult(
                action=result.action,
                message=walk_msg,
                duration=result.duration,
                effects={},
            )

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

                # Update timing for the walk — block new actions while walking
                self._last_action_time = current_time
                self._action_end_time = current_time + result.duration
                duck.set_action_message(walk_msg, duration=5.0)

                # Return info about needing to move (caller should handle movement)
                return ActionResult(
                    action=result.action,
                    message=walk_msg,
                    duration=result.duration,
                    effects={},  # No effects during walking
                )

        # Check if this action requires an item (handled by game's interaction controller)
        required_item_cat = data.get("requires_item_category")
        if required_item_cat and self._selected_item:
            # Store the pending action and request item interaction
            self._pending_action = result
            self._movement_requested = True  # Signal to game that duck needs to move

            # Return a "walking to" message
            walk_messages = {
                "toy": "*notices a toy and waddles over*",
                "water": "*sees water and waddles over to splash*",
                "furniture": "*spots a comfy spot and waddles over*",
                "decoration": "*admires something pretty and waddles closer*",
            }
            walk_msg = walk_messages.get(required_item_cat, f"*waddles toward item*")

            # Update timing for the walk — block new actions while walking
            self._last_action_time = current_time
            self._action_end_time = current_time + result.duration

            # Return info - game will use _selected_item to trigger interaction controller
            return ActionResult(
                action=result.action,
                message=walk_msg,
                duration=result.duration,
                effects={},  # Effects applied by interaction controller
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
        # Store action end time on duck so it can auto-clear
        duck.current_action = result.action.value
        duck._action_end_time = self._action_end_time
        duck.set_action_message(result.message, duration=result.duration)

        return result

    def _pick_biome_behavior(self) -> Tuple[str, float, str]:
        """Pick a random biome-specific behavior message, duration, and feature tag."""
        from duck.biome_behaviors import BIOME_BEHAVIORS
        biome_key = self._current_biome or "pond"
        behaviors = BIOME_BEHAVIORS.get(biome_key, BIOME_BEHAVIORS["pond"])
        message, duration, feature_tag = random.choice(behaviors)
        return message, duration, feature_tag

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

            # Skip item-based actions if no items of that category available
            required_item_cat = data.get("requires_item_category")
            if required_item_cat:
                available_items = self.get_items_by_category(required_item_cat)
                if not available_items:
                    continue  # Skip this action - no items of this category

            # Skip radio action if duck doesn't own the radio
            if data.get("requires_radio") and not self._has_radio:
                continue

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

            # Item-based actions get bonus utility when items are available
            if required_item_cat:
                # Check cooldown - if on cooldown, skip item actions entirely
                if self.is_item_interaction_on_cooldown():
                    continue  # Skip item actions during cooldown, let duck vibe/idle
                
                # Base utility for item interactions (low - duck needs a reason)
                score = 0.05
                
                # PLAY_WITH_TOY - bonus when duck needs fun (capped to compete, not dominate)
                if action == AutonomousAction.PLAY_WITH_TOY:
                    need_value = getattr(duck.needs, "fun", 50)
                    energy_value = getattr(duck.needs, "energy", 50)
                    
                    if energy_value < 25:
                        score = 0.05  # Too tired to play
                    elif need_value < 30:  # Very bored
                        score = 0.45
                    elif need_value < 50:  # Somewhat bored
                        score = 0.3
                    elif need_value < 70:  # Slight interest
                        score = 0.15
                    else:
                        score = 0.05  # Not interested when fun is high

                # SPLASH_IN_WATER - bonus when duck needs cleaning
                elif action == AutonomousAction.SPLASH_IN_WATER:
                    need_value = getattr(duck.needs, "cleanliness", 50)
                    energy_value = getattr(duck.needs, "energy", 50)
                    
                    if energy_value < 20:
                        score = 0.05  # Too tired for splashing
                    elif need_value < 30:  # Very dirty
                        score = 0.5
                    elif need_value < 50:  # Dirty
                        score = 0.3
                    elif need_value < 70:  # Slightly dirty
                        score = 0.15
                    else:
                        score = 0.05

                # REST_ON_FURNITURE - bonus when duck is tired
                elif action == AutonomousAction.REST_ON_FURNITURE:
                    need_value = getattr(duck.needs, "energy", 50)
                    if need_value < 30:  # Very tired
                        score = 0.45
                    elif need_value < 50:  # Tired
                        score = 0.3
                    elif need_value < 70:  # Slightly tired
                        score = 0.15
                    else:
                        score = 0.05

                # Apply satiation decay — repeated use of same category is boring
                satiation = self._get_item_satiation(required_item_cat)
                score *= satiation

            # Radio action scoring — duck occasionally wants to toggle radio
            if data.get("requires_radio") and self._has_radio:
                fun_value = getattr(duck.needs, "fun", 50)
                energy_value = getattr(duck.needs, "energy", 50)
                if energy_value < 20:
                    score = 0.02  # Too tired
                elif self._radio_playing:
                    # Radio already on — low chance to toggle off (duck enjoys it)
                    score = 0.05
                elif fun_value < 40:
                    score = 0.35  # Bored — wants music
                elif fun_value < 60:
                    score = 0.2   # Slightly bored
                else:
                    score = 0.08  # Content — might still want tunes

            # Add bonus based on relevant need (lower need = higher bonus)
            # Skip for item-based actions - they have custom need handling above
            if data["need_bonus"] and not required_item_cat and not data.get("requires_radio"):
                need_name, bonus_weight = data["need_bonus"]
                need_value = getattr(duck.needs, need_name, 50)
                # Invert: low need value = high bonus
                need_urgency = (100 - need_value) / 100
                
                # Special case: If duck wants to NAP and a nest is available,
                # strongly prefer NAP_IN_NEST over regular NAP
                if action == AutonomousAction.NAP and self._has_nest_available():
                    # Reduce NAP utility significantly when nest exists
                    # Duck should go to nest instead of napping on the ground
                    score += need_urgency * bonus_weight * 0.2  # Only 20% of normal bonus
                else:
                    score += need_urgency * bonus_weight

            # Add bonus based on personality alignment
            # Skip for item-based actions - keep scores predictable
            if data["personality_bonus"] and not required_item_cat:
                trait_name, trait_weight = data["personality_bonus"]
                trait_value = duck.get_personality_trait(trait_name)
                # Positive trait_weight means high trait = more likely
                # Negative trait_weight means low trait = more likely
                trait_influence = (trait_value / 100) * trait_weight
                score += trait_influence

            # Mood influences
            mood = duck.get_mood()
            if mood.state.value in ["happy", "ecstatic"]:
                # Happy ducks are more active and enjoy music
                if action in [AutonomousAction.WADDLE, AutonomousAction.WIGGLE,
                              AutonomousAction.SPLASH, AutonomousAction.FLAP_WINGS,
                              AutonomousAction.LISTEN_TO_RADIO]:
                    score += 0.1
            elif mood.state.value in ["sad", "miserable"]:
                # Sad ducks prefer calmer actions — but music might comfort them
                if action in [AutonomousAction.IDLE, AutonomousAction.NAP,
                              AutonomousAction.STARE_BLANKLY,
                              AutonomousAction.LISTEN_TO_RADIO]:
                    score += 0.15
            elif mood.state.value == "dramatic":
                # Dramatic ducks favour performative actions
                if action in [AutonomousAction.WIGGLE, AutonomousAction.FLAP_WINGS,
                              AutonomousAction.SPLASH]:
                    score += 0.2
            elif mood.state.value == "petty":
                # Petty ducks favour passive-aggressive idling
                if action in [AutonomousAction.IDLE, AutonomousAction.STARE_BLANKLY,
                              AutonomousAction.LOOK_AROUND]:
                    score += 0.15
            
            # Weather influences for non-structure actions
            if self._is_bad_weather:
                # Reduce outdoor activity scores during bad weather
                outdoor_actions = [AutonomousAction.WADDLE, AutonomousAction.SPLASH,
                                   AutonomousAction.CHASE_BUG, AutonomousAction.LOOK_AROUND]
                if action in outdoor_actions:
                    score *= 0.5

            # ── Goal-driven utility boost ─────────────────────────
            if self._desires and self._active_goal:
                goal_boost = self._desires.get_goal_utility_boost(
                    action.value, self._current_location)
                score += goal_boost * self._motivation
                # Suppression for contradicting actions
                score += self._desires.get_goal_suppression(
                    action.value, self._motivation)

            # ── Motivation-driven REST bias ────────────────────────
            # Low motivation → duck gravitates to passive actions
            if self._motivation < 0.4:
                if action in (AutonomousAction.NAP, AutonomousAction.NAP_IN_NEST,
                              AutonomousAction.IDLE, AutonomousAction.STARE_BLANKLY,
                              AutonomousAction.REST_ON_FURNITURE):
                    score += 0.3 * (1.0 - self._motivation)

            # ── Energy exhaustion gate ───────────────────────────
            # When energy is very low, suppress physical actions and strongly
            # prefer rest.  A duck with no energy should nap, not play.
            energy = getattr(duck.needs, "energy", 50)
            rest_actions = (AutonomousAction.NAP, AutonomousAction.NAP_IN_NEST,
                            AutonomousAction.REST_ON_FURNITURE, AutonomousAction.IDLE,
                            AutonomousAction.STARE_BLANKLY, AutonomousAction.HIDE_IN_SHELTER)
            if energy < 15:
                # Exhausted: almost nothing except rest
                if action not in rest_actions:
                    score *= 0.05
                else:
                    score += 0.6
            elif energy < 30:
                # Very tired: strongly discourage physical actions
                if action not in rest_actions:
                    score *= 0.3
                else:
                    score += 0.3

            scores.append((action, max(0, score)))

        # Add biome-specific action if duck is in a known biome
        if self._current_biome:
            from duck.biome_behaviors import BIOME_BEHAVIORS
            if self._current_biome in BIOME_BEHAVIORS:
                biome_score = 0.35  # Moderate base — competes with waddle/splash
                mood = duck.get_mood()
                if mood.state.value in ["happy", "ecstatic"]:
                    biome_score += 0.1  # Happy ducks explore more
                if self._is_bad_weather:
                    biome_score *= 0.5  # Less exploring in bad weather
                scores.append((AutonomousAction.BIOME_ACTION, biome_score))

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
        
        # Biome actions have their own target position
        if self._pending_action.action == AutonomousAction.BIOME_ACTION:
            return self._biome_target_position
        
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
        self._biome_target_position = None
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
        self._biome_target_position = None
        self._biome_feature_tag = None
