"""
Context Provider - Bridge between game state and dialogue system.

Provides a clean abstraction for building DialogueContext objects
from live game state without the dialogue system needing to know
about the internal structure of Game, Duck, AtmosphereManager, etc.

Uses ``weakref.ref`` to hold the game object, preventing circular
reference cycles between the dialogue pipeline and the game loop.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Any
import logging
import time
import weakref

from dialogue.dialogue_core import DialogueContext

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# ContextProvider ABC
# ---------------------------------------------------------------------------

class ContextProvider(ABC):
    """
    Abstract interface for anything that can supply a DialogueContext.

    The dialogue pipeline only depends on this interface, so unit tests
    can inject a stub provider without a full game instance.
    """

    @abstractmethod
    def build_context(
        self,
        player_message: Optional[str] = None,
        triggers: Optional[List[str]] = None,
    ) -> DialogueContext:
        """
        Assemble a complete DialogueContext from current game state.

        Args:
            player_message: The text the player typed, if any.
            triggers: What caused this dialogue turn (e.g.
                ``["player_input"]``, ``["idle_timer"]``).

        Returns:
            A fully populated DialogueContext.
        """
        ...

    @abstractmethod
    def get_duck_mood(self) -> str:
        """Return the duck's current mood as a string."""
        ...

    @abstractmethod
    def get_duck_trust(self) -> float:
        """Return the duck's current trust level."""
        ...

    @abstractmethod
    def get_weather(self) -> str:
        """Return the current weather type."""
        ...

    @abstractmethod
    def get_time_of_day(self) -> str:
        """Return the current time-of-day period."""
        ...

    @abstractmethod
    def get_season(self) -> str:
        """Return the current season."""
        ...

    @abstractmethod
    def get_current_biome(self) -> str:
        """Return the current biome name."""
        ...

    @abstractmethod
    def get_current_location(self) -> str:
        """Return the current location name."""
        ...

    @abstractmethod
    def get_active_visitor(self) -> Optional[str]:
        """Return the name of the visiting duck, or None."""
        ...

    @abstractmethod
    def get_active_event(self) -> Optional[str]:
        """Return the active event name, or None."""
        ...


# ---------------------------------------------------------------------------
# GameContextProvider - reads from a live Game instance
# ---------------------------------------------------------------------------

class GameContextProvider(ContextProvider):
    """
    Concrete provider that reads live state from the Game object.

    Holds only a ``weakref.ref`` to the game to avoid preventing
    garbage collection and to break circular reference chains.
    """

    def __init__(self, game_ref: Any) -> None:
        """
        Args:
            game_ref: The live Game instance.  A weak reference is
                stored internally.
        """
        self._game_ref = weakref.ref(game_ref)

    def _game(self) -> Any:
        """Dereference the weak ref, returning None if collected."""
        return self._game_ref()

    # -- full context build -----------------------------------------------

    def build_context(
        self,
        player_message: Optional[str] = None,
        triggers: Optional[List[str]] = None,
    ) -> DialogueContext:
        """
        Assemble a DialogueContext by reading every relevant piece
        of game state in one pass.
        """
        game = self._game()

        # Fallback context if game has been collected
        if game is None:
            return DialogueContext(
                timestamp=time.time(),
                player_message=player_message,
                triggers=triggers or [],
            )

        # Pull recent topics from duck brain if available
        recent_topics: List[str] = []
        duck_brain = getattr(game, "duck_brain", None)
        if duck_brain is not None:
            try:
                conv_mem = duck_brain.conversation_memory
                # Get topics from the last few messages
                if conv_mem.current_conversation:
                    for msg in conv_mem.current_conversation.messages[-10:]:
                        recent_topics.extend(msg.topics)
                recent_topics = list(dict.fromkeys(recent_topics))[:20]
            except Exception:
                logger.debug("Failed to extract recent topics from duck brain", exc_info=True)

        # Session message count
        session_count = 0
        if duck_brain is not None:
            session_count = getattr(duck_brain, "_session_messages", 0)

        # Determine conversation state
        conv_state = "active"
        if triggers and "idle_timer" in triggers:
            conv_state = "idle"
        elif session_count == 0:
            conv_state = "greeting"

        return DialogueContext(
            timestamp=time.time(),
            player_message=player_message,
            conversation_state=conv_state,
            duck_mood=self.get_duck_mood(),
            duck_trust=self.get_duck_trust(),
            time_of_day=self.get_time_of_day(),
            season=self.get_season(),
            weather=self.get_weather(),
            current_biome=self.get_current_biome(),
            current_location=self.get_current_location(),
            active_visitor=self.get_active_visitor(),
            active_event=self.get_active_event(),
            recent_topics=recent_topics,
            session_message_count=session_count,
            triggers=triggers or [],
        )

    # -- individual accessors ---------------------------------------------

    def get_duck_mood(self) -> str:
        game = self._game()
        if game is None:
            return "content"
        duck = getattr(game, "duck", None)
        if duck is None:
            return "content"
        try:
            mood = duck.get_mood()
            return mood.state.value
        except Exception:
            return "content"

    def get_duck_trust(self) -> float:
        game = self._game()
        if game is None:
            return 20.0
        duck = getattr(game, "duck", None)
        if duck is None:
            return 20.0
        return getattr(duck, "trust", 20.0)

    def get_weather(self) -> str:
        game = self._game()
        if game is None:
            return "clear"
        atmo = getattr(game, "atmosphere", None)
        if atmo is None:
            return "clear"
        try:
            weather_type = atmo.current_weather
            # weather_type may be an enum; get its value
            return getattr(weather_type, "value", str(weather_type))
        except Exception:
            return "clear"

    def get_time_of_day(self) -> str:
        game = self._game()
        if game is None:
            return "day"
        atmo = getattr(game, "atmosphere", None)
        if atmo is None:
            return "day"
        try:
            return getattr(atmo, "time_of_day", "day")
        except Exception:
            return "day"

    def get_season(self) -> str:
        game = self._game()
        if game is None:
            return "spring"
        atmo = getattr(game, "atmosphere", None)
        if atmo is None:
            return "spring"
        try:
            season = getattr(atmo, "current_season", "spring")
            return getattr(season, "value", str(season))
        except Exception:
            return "spring"

    def get_current_biome(self) -> str:
        game = self._game()
        if game is None:
            return "pond"
        try:
            world = getattr(game, "world", None)
            if world is not None:
                biome = getattr(world, "current_biome", None)
                if biome is not None:
                    return getattr(biome, "name", str(biome))
        except Exception:
            logger.debug("Failed to read current biome", exc_info=True)
        return "pond"

    def get_current_location(self) -> str:
        game = self._game()
        if game is None:
            return "home"
        try:
            duck = getattr(game, "duck", None)
            if duck is not None:
                loc = getattr(duck, "current_location", None)
                if loc is not None:
                    return str(loc)
        except Exception:
            logger.debug("Failed to read current location", exc_info=True)
        return "home"

    def get_active_visitor(self) -> Optional[str]:
        game = self._game()
        if game is None:
            return None
        try:
            visitor_mgr = getattr(game, "visitor_manager", None)
            if visitor_mgr is not None:
                visitor = getattr(visitor_mgr, "current_visitor", None)
                if visitor is not None:
                    return getattr(visitor, "name", str(visitor))
        except Exception:
            logger.debug("Failed to read active visitor", exc_info=True)
        return None

    def get_active_event(self) -> Optional[str]:
        game = self._game()
        if game is None:
            return None
        try:
            event_mgr = getattr(game, "event_manager", None)
            if event_mgr is not None:
                event = getattr(event_mgr, "current_event", None)
                if event is not None:
                    return getattr(event, "name", str(event))
        except Exception:
            logger.debug("Failed to read active event", exc_info=True)
        return None
