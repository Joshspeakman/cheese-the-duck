"""
Duck Reaction Controller - Manages visual reactions to weather, events, and friends.

This module handles automatic duck animation state changes based on:
- Weather conditions (persistent reactions)
- Events (temporary reactions)
- Friend arrivals/departures (social reactions)
"""
from dataclasses import dataclass
from typing import Optional, Dict, List, TYPE_CHECKING
import time

if TYPE_CHECKING:
    from ui.renderer import Renderer


# Weather-to-animation state mapping
# Each weather type maps to a list of states to cycle through and optional effect
# Note: Use states that exist for all growth stages (duckling, teen, adult, elder)
WEATHER_DUCK_STATES: Dict[str, Dict] = {
    "sunny": {
        "states": ["idle", "excited"],  # excited exists for all stages
        "effect": None,
        "priority": 1,
    },
    "cloudy": {
        "states": ["idle"],
        "effect": None,
        "priority": 1,
    },
    "rainy": {
        "states": ["shaking", "splashing"],
        "effect": "splash",
        "effect_chance": 0.3,  # 30% chance to show effect on state change
        "priority": 2,
    },
    "stormy": {
        "states": ["scared", "shaking"],
        "effect": "exclaim",
        "effect_chance": 0.5,
        "priority": 4,
    },
    "snowy": {
        "states": ["cold"],
        "effect": None,
        "priority": 3,
    },
    "foggy": {
        "states": ["curious", "idle"],
        "effect": "question",
        "effect_chance": 0.2,
        "priority": 2,
    },
    "windy": {
        "states": ["flapping", "shaking"],
        "effect": None,
        "priority": 2,
    },
    "rainbow": {
        "states": ["excited", "dancing"],
        "effect": "sparkle",
        "effect_chance": 0.6,
        "priority": 5,
    },
}


@dataclass
class EventReaction:
    """Defines how the duck reacts to an event."""
    state: str
    effect: Optional[str] = None
    duration: float = 2.0
    sound: Optional[str] = None


# Event-to-reaction mapping
EVENT_DUCK_REACTIONS: Dict[str, EventReaction] = {
    # Friend/social events
    "friend_arrival": EventReaction(
        state="excited",
        effect="hearts",
        duration=3.0,
        sound="happy",
    ),
    "friend_departure": EventReaction(
        state="waving",
        effect=None,
        duration=2.0,
    ),
    "visitor_arrival": EventReaction(
        state="curious",
        effect="hearts",
        duration=3.0,
        sound="happy",
    ),

    # Random events
    "butterfly": EventReaction(
        state="curious",
        effect="sparkle",
        duration=2.0,
    ),
    "bird_friend": EventReaction(
        state="excited",
        effect=None,
        duration=2.0,
    ),
    "found_shiny": EventReaction(
        state="proud",
        effect="sparkle",
        duration=2.5,
    ),
    "found_crumb": EventReaction(
        state="excited",
        effect=None,
        duration=2.0,
    ),
    "nice_breeze": EventReaction(
        state="happy",
        effect=None,
        duration=2.0,
    ),
    "loud_noise": EventReaction(
        state="scared",
        effect="exclaim",
        duration=2.0,
    ),
    "bad_dream": EventReaction(
        state="scared",
        effect=None,
        duration=3.0,
    ),

    # Achievement/progression events
    "level_up": EventReaction(
        state="dancing",
        effect="sparkle",
        duration=4.0,
        sound="happy",
    ),
    "achievement": EventReaction(
        state="proud",
        effect="sparkle",
        duration=3.0,
    ),
    "new_item": EventReaction(
        state="excited",
        effect="sparkle",
        duration=2.0,
    ),

    # Weather change reactions (one-time when weather changes)
    "weather_stormy": EventReaction(
        state="scared",
        effect="exclaim",
        duration=2.0,
    ),
    "weather_rainbow": EventReaction(
        state="excited",
        effect="sparkle",
        duration=3.0,
    ),
}


class DuckReactionController:
    """
    Manages duck visual reactions to environmental and social changes.

    This controller coordinates animation state changes based on:
    - Weather (persistent, updates randomly every 5-30 seconds)
    - Events (immediate, temporary override)
    - Friend visits (social interactions)

    Priority system ensures important reactions aren't overridden:
    - User actions (feed, play, etc.) always take highest priority
    - Event reactions temporarily override weather
    - Weather reactions persist during calm periods
    """

    # Weather update interval range (seconds) - random between min and max
    WEATHER_UPDATE_MIN = 5.0
    WEATHER_UPDATE_MAX = 30.0

    def __init__(self, renderer: 'Renderer'):
        self.renderer = renderer

        # Weather reaction state
        self._last_weather_update: float = 0
        self._next_weather_interval: float = 15.0  # Start with middle value
        self._weather_state_index: int = 0
        self._current_weather: Optional[str] = None

        # Event reaction state
        self._event_end_time: float = 0
        self._active_event: Optional[str] = None

        # Track if user action is in progress (don't override)
        self._user_action_until: float = 0

    def update(self, current_time: float, weather_type: str):
        """
        Main update method - call every frame from game loop.

        Handles weather reactions when no event is active.
        """
        # Don't override user actions
        if current_time < self._user_action_until:
            return

        # Check if event reaction is still active
        if current_time < self._event_end_time:
            return  # Let event reaction play out

        # Clear event state when done
        if self._active_event:
            self._active_event = None

        # Update weather reaction
        self.update_weather_reaction(weather_type, current_time)

    def update_weather_reaction(self, weather_type: str, current_time: float):
        """
        Update duck animation based on current weather.

        Called with random intervals (5-30 seconds) to avoid gridlocking the duck.
        Cycles through available states for the current weather type.
        """
        import random

        # Throttle updates using random interval
        if current_time - self._last_weather_update < self._next_weather_interval:
            return

        self._last_weather_update = current_time
        # Set next random interval
        self._next_weather_interval = random.uniform(
            self.WEATHER_UPDATE_MIN,
            self.WEATHER_UPDATE_MAX
        )

        # Get weather data
        weather_data = WEATHER_DUCK_STATES.get(weather_type.lower())
        if not weather_data:
            return

        # Check if weather changed
        if weather_type != self._current_weather:
            self._current_weather = weather_type
            self._weather_state_index = 0  # Reset cycle on weather change

        # Get available states for this weather
        states = weather_data["states"]
        if not states:
            return

        # Cycle through states
        state = states[self._weather_state_index % len(states)]
        self._weather_state_index += 1

        # Set duck state - duration matches next interval so it persists until next update
        self.renderer.duck_pos.set_state(state, duration=self._next_weather_interval)

        # Optionally show effect
        effect = weather_data.get("effect")
        effect_chance = weather_data.get("effect_chance", 0.3)
        if effect and self._should_show_effect(effect_chance):
            self.renderer.show_effect(effect, duration=2.0)

    def trigger_event_reaction(self, event_type: str, current_time: float):
        """
        Trigger an immediate reaction to an event.

        Event reactions temporarily override weather reactions.
        """
        reaction = EVENT_DUCK_REACTIONS.get(event_type)
        if not reaction:
            return

        # Set active event
        self._active_event = event_type
        self._event_end_time = current_time + reaction.duration

        # Set duck state
        self.renderer.duck_pos.set_state(reaction.state, duration=reaction.duration)

        # Show effect if applicable
        if reaction.effect:
            self.renderer.show_effect(reaction.effect, duration=reaction.duration)

        # Play sound if applicable
        if reaction.sound:
            try:
                from audio.sound import duck_sounds
                duck_sounds.quack(reaction.sound)
            except Exception:
                pass  # Audio is optional

    def trigger_friend_reaction(self, event_type: str, current_time: float):
        """
        Handle friend arrival/departure reactions.

        Args:
            event_type: "arrival" or "departure"
            current_time: Current game time
        """
        if event_type == "arrival":
            self.trigger_event_reaction("friend_arrival", current_time)
        elif event_type == "departure":
            self.trigger_event_reaction("friend_departure", current_time)

    def trigger_visitor_reaction(self, event_type: str, current_time: float):
        """
        Handle rare visitor arrival/departure reactions.

        Args:
            event_type: "arrival" or "departure"
            current_time: Current game time
        """
        if event_type == "arrival":
            self.trigger_event_reaction("visitor_arrival", current_time)
        elif event_type == "departure":
            self.trigger_event_reaction("friend_departure", current_time)

    def notify_user_action(self, duration: float, current_time: float):
        """
        Notify that a user action is in progress.

        This prevents weather/event reactions from overriding
        user-initiated animations (feeding, playing, etc.).

        Args:
            duration: How long the user action lasts
            current_time: Current game time
        """
        self._user_action_until = current_time + duration

    def _should_show_effect(self, chance: float) -> bool:
        """Randomly decide whether to show an effect based on chance."""
        import random
        return random.random() < chance

    def is_event_active(self) -> bool:
        """Check if an event reaction is currently playing."""
        return self._active_event is not None

    def get_current_weather(self) -> Optional[str]:
        """Get the current weather type being reacted to."""
        return self._current_weather


# Global instance for easy access
reaction_controller: Optional[DuckReactionController] = None


def init_reaction_controller(renderer: 'Renderer') -> DuckReactionController:
    """Initialize the global reaction controller."""
    global reaction_controller
    reaction_controller = DuckReactionController(renderer)
    return reaction_controller


def get_reaction_controller() -> Optional[DuckReactionController]:
    """Get the global reaction controller instance."""
    return reaction_controller
