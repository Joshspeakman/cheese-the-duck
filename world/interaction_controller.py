"""
Unified Interaction Controller - Ensures duck always walks to items before interacting.
Handles player commands, AI behaviors, and proximity triggers through a single pathway.
"""
from typing import Optional, Callable, Dict, Any, Tuple, List, TYPE_CHECKING
from dataclasses import dataclass
from enum import Enum, auto
import time

if TYPE_CHECKING:
    from world.habitat import Habitat, PlacedItem
    from ui.renderer import Renderer


class InteractionSource(Enum):
    """What triggered the interaction."""
    PLAYER_COMMAND = auto()  # Player typed command or used menu
    AI_AUTONOMOUS = auto()   # AI behavior system chose to interact
    PROXIMITY = auto()       # Duck wandered near item (random chance)


class InteractionState(Enum):
    """Current state of an interaction."""
    IDLE = auto()           # No interaction in progress
    MOVING = auto()         # Duck is walking to item
    ARRIVED = auto()        # Duck arrived, item animation starting
    ANIMATING = auto()      # Full interaction animation playing
    COMPLETING = auto()     # Applying effects and cleaning up


@dataclass
class PendingInteraction:
    """An interaction waiting to be executed or in progress."""
    item_id: str
    source: InteractionSource
    start_time: float
    target_position: Tuple[int, int]  # Playfield coordinates
    interaction_result: Any  # InteractionResult from item_interactions
    state: InteractionState = InteractionState.MOVING
    animation_start_time: float = 0.0
    on_complete: Optional[Callable] = None


class InteractionController:
    """
    Manages all duck-to-item interactions with proper movement.

    This controller ensures that:
    1. Duck ALWAYS walks to items before interacting
    2. Both player commands and AI behaviors use the same flow
    3. Only one interaction can happen at a time
    4. Animations are properly sequenced
    """

    def __init__(self):
        self._pending: Optional[PendingInteraction] = None
        self._cooldown_end: float = 0.0  # Prevent rapid re-interactions
        self._interaction_cooldown: float = 2.0  # Seconds between interactions

        # References set by game
        self._habitat: Optional['Habitat'] = None
        self._renderer: Optional['Renderer'] = None
        self._duck: Any = None
        self._on_effects_applied: Optional[Callable] = None  # Callback to apply effects

    def set_references(self, habitat: 'Habitat', renderer: 'Renderer', duck: Any,
                       on_effects_applied: Optional[Callable] = None):
        """Set references to game objects needed for interactions."""
        self._habitat = habitat
        self._renderer = renderer
        self._duck = duck
        self._on_effects_applied = on_effects_applied

    def can_start_interaction(self) -> bool:
        """Check if a new interaction can be started."""
        if self._pending is not None:
            return False
        if time.time() < self._cooldown_end:
            return False
        return True

    def is_interacting(self) -> bool:
        """Check if an interaction is currently in progress."""
        return self._pending is not None

    def get_current_state(self) -> InteractionState:
        """Get the current interaction state."""
        if self._pending:
            return self._pending.state
        return InteractionState.IDLE

    def request_interaction(self, item_id: str, source: InteractionSource,
                           duck_state: Optional[Dict] = None) -> Tuple[bool, str]:
        """
        Request an interaction with an item.

        Args:
            item_id: The item to interact with
            source: What triggered the interaction (player, AI, proximity)
            duck_state: Current duck state for contextual messages

        Returns:
            Tuple of (success, message)
        """
        if not self.can_start_interaction():
            return False, "*quack* I'm busy right now!"

        if not self._habitat or not self._renderer or not self._duck:
            return False, "*confused quack*"

        # Check if item exists in habitat
        placed_item = self._get_placed_item(item_id)
        if not placed_item:
            return False, f"*looks around* Where is that?"

        # Get item's playfield position
        target_pos = self._get_item_playfield_position(placed_item)
        if not target_pos:
            return False, "*confused quack*"

        # Get interaction result
        from world.item_interactions import execute_interaction
        if duck_state is None:
            duck_state = self._build_duck_state()

        result = execute_interaction(item_id, duck_state)
        if not result or not result.success:
            return False, "*confused quack* I don't know how to do that..."

        # Create pending interaction
        self._pending = PendingInteraction(
            item_id=item_id,
            source=source,
            start_time=time.time(),
            target_position=target_pos,
            interaction_result=result,
            state=InteractionState.MOVING
        )

        # Get item name for message
        from world.shop import get_item as get_shop_item
        item = get_shop_item(item_id)
        item_name = item.name if item else item_id

        # Show anticipation message
        if source == InteractionSource.AI_AUTONOMOUS:
            message = f"*notices {item_name} and waddles over*"
        else:
            message = f"*waddles excitedly toward {item_name}*"
        self._renderer.show_message(message, duration=2.0)

        # Start movement
        self._renderer.duck_pos.move_to(
            target_pos[0], target_pos[1],
            callback=self._on_arrived_at_item,
            callback_data={"item_id": item_id}
        )

        return True, message

    def _get_placed_item(self, item_id: str) -> Optional['PlacedItem']:
        """Get a placed item by ID."""
        if not self._habitat:
            return None
        for placed in self._habitat.placed_items:
            if placed.item_id == item_id:
                return placed
        return None

    def _get_item_playfield_position(self, placed_item: 'PlacedItem') -> Optional[Tuple[int, int]]:
        """Convert item's habitat grid position to playfield coordinates."""
        if not self._renderer:
            return None

        # Habitat grid: 20x12, Playfield: field_width x field_height
        field_width = self._renderer.duck_pos.field_width
        field_height = self._renderer.duck_pos.field_height

        # Scale coordinates
        item_x = int(placed_item.x * field_width / 20)
        item_y = int(placed_item.y * field_height / 12)

        return (item_x, item_y)

    def _build_duck_state(self) -> Dict[str, Any]:
        """Build duck state dictionary for interaction context."""
        if not self._duck:
            return {}

        # Get growth stage value
        growth_stage = "adult"
        if hasattr(self._duck, 'growth_stage'):
            if hasattr(self._duck.growth_stage, 'value'):
                growth_stage = self._duck.growth_stage.value
            else:
                growth_stage = str(self._duck.growth_stage)

        return {
            "energy": getattr(self._duck.needs, "energy", 100),
            "hunger": getattr(self._duck.needs, "hunger", 100),
            "fun": getattr(self._duck.needs, "fun", 100),
            "cleanliness": getattr(self._duck.needs, "cleanliness", 100),
            "social": getattr(self._duck.needs, "social", 100),
            "mood": self._duck.get_mood().state.value if hasattr(self._duck, 'get_mood') else "neutral",
            "growth_stage": growth_stage,
        }

    def _on_arrived_at_item(self, data: Dict):
        """Callback when duck reaches the item."""
        if not self._pending:
            return

        item_id = data.get("item_id")
        if item_id != self._pending.item_id:
            return  # Wrong callback (shouldn't happen)

        # Update state
        self._pending.state = InteractionState.ARRIVED

        # Trigger item's bounce/shake animation
        self._trigger_item_animation()

        # Start the animation overlay in the renderer
        self._start_animation_overlay()

        # Transition to animating state
        self._pending.state = InteractionState.ANIMATING
        self._pending.animation_start_time = time.time()

        # Show interaction message
        result = self._pending.interaction_result
        if result and result.message:
            self._renderer.show_message(result.message, duration=result.duration + 1.0)

        # Set duck animation state based on item type (only if no overlay animation)
        if not self._renderer.interaction_animator.is_animating():
            duck_state = self._get_duck_animation_state()
            if duck_state:
                self._renderer.duck_pos.set_state(duck_state, duration=result.duration if result else 3.0)

    def _start_animation_overlay(self):
        """Start the animation overlay in the renderer if available."""
        if not self._pending or not self._renderer:
            return

        # Get the duck's current position as the animation position
        position = (self._renderer.duck_pos.x, self._renderer.duck_pos.y)

        # Get duck's growth stage for stage-specific animations
        growth_stage = "adult"
        if self._duck and hasattr(self._duck, 'growth_stage'):
            if hasattr(self._duck.growth_stage, 'value'):
                growth_stage = self._duck.growth_stage.value
            else:
                growth_stage = str(self._duck.growth_stage)

        # Try to start an animation overlay with stage-specific animations
        self._renderer.interaction_animator.start_animation(
            item_id=self._pending.item_id,
            position=position,
            on_complete=None,  # Animation completion handled by update() timeout
            growth_stage=growth_stage
        )

    def _trigger_item_animation(self):
        """Trigger the placed item's animation when duck arrives."""
        if not self._pending or not self._habitat:
            return

        for placed_item in self._habitat.placed_items:
            if placed_item.item_id == self._pending.item_id:
                # Choose animation type based on item
                item_id = self._pending.item_id
                if "ball" in item_id or "toy" in item_id or "trampoline" in item_id:
                    placed_item.start_animation("bounce")
                elif "pool" in item_id or "water" in item_id or "bath" in item_id or "fountain" in item_id:
                    placed_item.start_animation("shake")
                elif "swing" in item_id or "hammock" in item_id:
                    placed_item.start_animation("shake")
                else:
                    placed_item.start_animation("bounce")
                break

    def _get_duck_animation_state(self) -> Optional[str]:
        """Get the appropriate duck animation state for the current interaction."""
        if not self._pending:
            return None

        item_id = self._pending.item_id

        # Map item types to duck animation states
        if "pool" in item_id or "bath" in item_id or "fountain" in item_id or "water" in item_id:
            return "splashing"
        elif "ball" in item_id or "toy" in item_id or "trampoline" in item_id:
            return "playing"
        elif "bed" in item_id or "hammock" in item_id or "couch" in item_id:
            return "napping"
        elif "chair" in item_id:
            return "sitting"
        elif "piano" in item_id or "boombox" in item_id or "trumpet" in item_id:
            return "playing"
        else:
            return "playing"

    def update(self, delta_time: float):
        """
        Update the interaction state.
        Call this every frame to progress animations.
        """
        if not self._pending:
            return

        # Safety timeout - if stuck in MOVING state for too long, cancel
        # This prevents blocking all interactions if duck can't reach item
        if self._pending.state == InteractionState.MOVING:
            elapsed = time.time() - self._pending.start_time
            if elapsed > 15.0:  # 15 seconds max to reach item
                self.cancel_interaction()
                if self._renderer:
                    self._renderer.show_message("*gives up and waddles away*", duration=2.0)
                return

        # Handle animation completion
        if self._pending.state == InteractionState.ANIMATING:
            result = self._pending.interaction_result
            duration = result.duration if result else 3.0
            elapsed = time.time() - self._pending.animation_start_time

            if elapsed >= duration:
                self._complete_interaction()

    def _complete_interaction(self):
        """Complete the interaction and apply effects."""
        if not self._pending:
            return

        result = self._pending.interaction_result
        item_id = self._pending.item_id

        # Apply effects to duck needs
        if result and result.effects and self._duck:
            for need, change in result.effects.items():
                if hasattr(self._duck.needs, need):
                    current = getattr(self._duck.needs, need)
                    new_value = min(100, max(0, current + change))
                    setattr(self._duck.needs, need, new_value)

        # Notify callback if set
        if self._on_effects_applied:
            self._on_effects_applied(item_id, result)

        # Set cooldown
        self._cooldown_end = time.time() + self._interaction_cooldown

        # Clear pending interaction
        self._pending = None

    def cancel_interaction(self):
        """Cancel the current interaction."""
        if self._pending:
            # Cancel duck movement
            if self._renderer:
                self._renderer.duck_pos.cancel_movement()
            self._pending = None

    def get_interactable_items(self) -> List[str]:
        """Get list of item IDs that can currently be interacted with."""
        if not self._habitat:
            return []
        return [placed.item_id for placed in self._habitat.placed_items]

    def get_items_by_category(self, category: str) -> List[str]:
        """Get item IDs filtered by category (for AI to choose from)."""
        if not self._habitat:
            return []

        from world.shop import get_item, ItemCategory

        # Map string category to enum
        category_map = {
            "toy": ItemCategory.TOY,
            "water": ItemCategory.WATER,
            "furniture": ItemCategory.FURNITURE,
            "plant": ItemCategory.PLANT,
            "decoration": ItemCategory.DECORATION,
        }

        target_category = category_map.get(category.lower())
        if not target_category:
            return []

        result = []
        for placed in self._habitat.placed_items:
            item = get_item(placed.item_id)
            if item and item.category == target_category:
                result.append(placed.item_id)
        return result

    def get_random_item_for_need(self, need: str) -> Optional[str]:
        """
        Get a random item that helps with a specific need.
        Used by AI to choose items intelligently.

        Args:
            need: The need to address ("fun", "cleanliness", "energy", etc.)

        Returns:
            Item ID or None if no suitable item found
        """
        import random

        # Map needs to item categories
        need_category_map = {
            "fun": ["toy", "water"],
            "cleanliness": ["water"],
            "energy": ["furniture"],  # Beds, couches for resting
            "social": ["toy"],  # Playing is social
        }

        categories = need_category_map.get(need, [])
        candidates = []

        for category in categories:
            candidates.extend(self.get_items_by_category(category))

        if candidates:
            return random.choice(candidates)
        return None
