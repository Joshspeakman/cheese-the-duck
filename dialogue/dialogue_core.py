"""
Dialogue Core - Unified data types for the dialogue pipeline.

Replaces the scattered state across ConversationSystem, DuckBrain,
ConversationMemory, and LLMChat with a single coherent set of types:

- DialogueContext: everything the duck needs to know to speak
- DialogueResponse: what the duck said and metadata about it
- DialogueMemory: unified conversation history (replaces 3 systems)
- DialogueState: single source of truth for session/relationship state
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict
from datetime import datetime
import difflib
import time


# ---------------------------------------------------------------------------
# DialogueContext - snapshot of the world at dialogue time
# ---------------------------------------------------------------------------

@dataclass
class DialogueContext:
    """
    Everything the duck needs to know when generating a response.

    Built once per dialogue turn by a ContextProvider, then passed
    through the entire ResponsePipeline unchanged.
    """
    timestamp: float
    player_message: Optional[str] = None
    conversation_state: str = "active"  # greeting, active, idle, farewell
    duck_mood: str = "content"
    duck_trust: float = 20.0
    time_of_day: str = "day"
    season: str = "spring"
    weather: str = "clear"
    current_biome: str = "pond"
    current_location: str = "home"
    active_visitor: Optional[str] = None
    active_event: Optional[str] = None
    recent_topics: List[str] = field(default_factory=list)
    session_message_count: int = 0
    triggers: List[str] = field(default_factory=list)
    # "player_input", "idle_timer", "action", "callback"


# ---------------------------------------------------------------------------
# DialogueResponse - what the duck said
# ---------------------------------------------------------------------------

@dataclass
class DialogueResponse:
    """
    A response produced by the pipeline, with metadata about its origin.

    Actions are parsed from ``[ACTION:xxx]`` tags embedded in the text
    by the LLM source. ``should_record`` is False for Markov voice-gen
    gibberish so it does not pollute persistent memory.
    """
    text: str
    source: str = "template"  # llm, keyword, learning, voice, seaman, template, idle
    confidence: float = 0.5   # 0.0-1.0
    actions: List[str] = field(default_factory=list)
    mood_hint: Optional[str] = None
    should_record: bool = True


# ---------------------------------------------------------------------------
# DialogueMemory - unified conversation history
# ---------------------------------------------------------------------------

class DialogueMemory:
    """
    Unified conversation history replacing the scattered triple of
    ``ConversationSystem._conversation_history``,
    ``ConversationMemory``, and ``LLMChat._conversation_history``.

    Keeps a bounded ring of exchanges with rich metadata, provides
    formatted views for display, LLM context, topic extraction, and
    fuzzy search.  Serialisable to/from dict for persistence.
    """

    def __init__(self, max_history: int = 200):
        self._max_history: int = max_history
        self._exchanges: List[Dict] = []
        # Aggregated topic counts across all exchanges
        self._topic_counts: Dict[str, int] = defaultdict(int)
        # Notable / high-sentiment exchanges worth recalling
        self._notable: List[Dict] = []
        # Running counters
        self._total_messages: int = 0
        self._session_count: int = 0
        self._current_session_start: Optional[float] = None

    # -- recording --------------------------------------------------------

    def record_exchange(
        self,
        player_msg: str,
        duck_msg: str,
        context: DialogueContext,
        response: DialogueResponse,
    ) -> None:
        """
        Record a single player/duck exchange.

        Args:
            player_msg: What the player said.
            duck_msg: What the duck responded.
            context: The DialogueContext at the time of the exchange.
            response: The DialogueResponse metadata.
        """
        topics = self._detect_topics(player_msg)
        for topic in topics:
            self._topic_counts[topic] += 1

        entry: Dict = {
            "player": player_msg,
            "duck": duck_msg,
            "timestamp": context.timestamp,
            "iso_time": datetime.fromtimestamp(context.timestamp).isoformat(),
            "source": response.source,
            "confidence": response.confidence,
            "topics": topics,
            "mood": context.duck_mood,
            "should_record": response.should_record,
        }

        self._exchanges.append(entry)
        self._total_messages += 2  # one player + one duck

        # Trim to max
        if len(self._exchanges) > self._max_history:
            self._exchanges = self._exchanges[-self._max_history:]

        # Track notable exchanges (strong sentiment / personal content)
        if response.should_record and self._is_notable(player_msg):
            self._notable.append(entry)
            # Keep notable list bounded too
            if len(self._notable) > 100:
                self._notable = self._notable[-100:]

    # -- querying ---------------------------------------------------------

    def get_recent(self, limit: int = 10) -> List[Dict]:
        """
        Return the most recent exchanges for display.

        Each dict has keys: player, duck, timestamp, iso_time, source,
        confidence, topics, mood.
        """
        return self._exchanges[-limit:]

    def get_llm_context(self, limit: int = 20) -> List[Dict]:
        """
        Return recent exchanges formatted for LLM consumption.

        Returns a list of ``{"role": "user"/"assistant", "content": ...}``
        dicts suitable for chat-completion APIs.
        """
        messages: List[Dict] = []
        for ex in self._exchanges[-limit:]:
            messages.append({"role": "user", "content": ex["player"]})
            messages.append({"role": "assistant", "content": ex["duck"]})
        return messages

    def get_topics(self, limit: int = 20) -> List[str]:
        """
        Return the most frequently discussed topics, most common first.
        """
        sorted_topics = sorted(
            self._topic_counts.items(), key=lambda kv: kv[1], reverse=True
        )
        return [topic for topic, _count in sorted_topics[:limit]]

    def get_notable_quotes(self) -> List[Dict]:
        """
        Return memorable exchanges (personal statements, strong feelings).
        """
        return list(self._notable)

    def search(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Fuzzy-search through history for exchanges matching *query*.

        Uses ``difflib.SequenceMatcher`` on the player message for
        ranking, then returns the top *limit* results.
        """
        query_lower = query.lower()
        scored: List[Tuple[float, Dict]] = []

        for ex in self._exchanges:
            player_lower = ex["player"].lower()
            # Fast keyword pre-check
            if query_lower in player_lower:
                scored.append((1.0, ex))
                continue
            ratio = difflib.SequenceMatcher(
                None, query_lower, player_lower
            ).ratio()
            if ratio > 0.35:
                scored.append((ratio, ex))

        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [ex for _score, ex in scored[:limit]]

    # -- session tracking -------------------------------------------------

    def start_session(self) -> None:
        """Mark the beginning of a play session."""
        self._session_count += 1
        self._current_session_start = time.time()

    def end_session(self) -> None:
        """Mark the end of a play session."""
        self._current_session_start = None

    def get_message_count(self) -> int:
        """Total number of individual messages (player + duck) ever recorded."""
        return self._total_messages

    def get_session_count(self) -> int:
        """Number of play sessions tracked."""
        return self._session_count

    # -- persistence ------------------------------------------------------

    def to_dict(self) -> dict:
        """Serialise to a plain dict for JSON persistence."""
        return {
            "max_history": self._max_history,
            "exchanges": self._exchanges,
            "topic_counts": dict(self._topic_counts),
            "notable": self._notable,
            "total_messages": self._total_messages,
            "session_count": self._session_count,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DialogueMemory":
        """Deserialise from a plain dict."""
        mem = cls(max_history=data.get("max_history", 200))
        mem._exchanges = data.get("exchanges", [])
        mem._topic_counts = defaultdict(int, data.get("topic_counts", {}))
        mem._notable = data.get("notable", [])
        mem._total_messages = data.get("total_messages", 0)
        mem._session_count = data.get("session_count", 0)
        return mem

    # -- internals --------------------------------------------------------

    @staticmethod
    def _detect_topics(text: str) -> List[str]:
        """
        Lightweight topic detection mirroring ConversationMemory._detect_topics.
        """
        text_lower = text.lower()
        topics: List[str] = []

        topic_keywords: Dict[str, List[str]] = {
            "greeting": ["hello", "hi ", "hey", "good morning", "good evening"],
            "farewell": ["bye", "goodbye", "see you", "later", "goodnight"],
            "food": ["food", "eat", "hungry", "bread", "feed", "meal", "snack"],
            "weather": ["weather", "rain", "sun", "snow", "cold", "hot", "storm"],
            "feelings": ["feel", "sad", "happy", "angry", "love", "hate", "scared"],
            "personal": ["my life", "my job", "my family", "my friend", "i work"],
            "games": ["play", "game", "fun", "boring"],
            "philosophy": ["meaning", "life", "death", "purpose", "existence"],
            "dreams": ["dream", "hope", "wish", "someday"],
            "past": ["remember", "used to", "when i was", "back then"],
            "secrets": ["secret", "don't tell", "between us", "private"],
            "praise": ["good duck", "love you", "best", "amazing", "awesome"],
            "complaints": ["annoying", "stop", "don't like", "hate when"],
            "existential": ["exist", "real", "consciousness", "what am i"],
        }

        for topic, keywords in topic_keywords.items():
            if any(kw in text_lower for kw in keywords):
                topics.append(topic)

        return topics or ["random"]

    @staticmethod
    def _is_notable(text: str) -> bool:
        """Determine if a player message is worth bookmarking."""
        if len(text) < 10 or len(text) > 200:
            return False
        text_lower = text.lower()
        markers = [
            "i think", "i believe", "i feel", "i love", "i hate",
            "my favorite", "i always", "i never", "i wish", "i hope",
            "i'm afraid", "i'm happy", "i'm sad", "i want",
        ]
        if any(m in text_lower for m in markers):
            return True
        strong = ["always", "never", "best", "worst", "love", "hate"]
        return any(w in text_lower for w in strong)


# ---------------------------------------------------------------------------
# DialogueState - single source of truth
# ---------------------------------------------------------------------------

class DialogueState:
    """
    Unified dialogue state that replaces scattered sync between
    DuckBrain, ConversationSystem, and game loop variables.

    Holds references to the existing PlayerModel and the new
    DialogueMemory, plus session bookkeeping and cooldowns.
    """

    def __init__(self) -> None:
        # External reference (set via sync_from_duck or directly)
        self.player_model: Any = None
        self.memory: DialogueMemory = DialogueMemory()

        # Duck state
        self.duck_mood: str = "content"
        self.duck_trust: float = 20.0
        self.personality_scores: Dict[str, float] = {}

        # Session bookkeeping
        self.session_start: float = time.time()
        self.messages_this_session: int = 0

        # Cooldowns: category -> next-allowed timestamp
        self.cooldowns: Dict[str, float] = {
            "observation": 0.0,
            "callback": 0.0,
            "question": 0.0,
            "idle": 0.0,
            "genuine_moment": 0.0,
        }

    # -- sync helpers -----------------------------------------------------

    def sync_from_duck(self, duck_obj: Any) -> None:
        """
        Pull all relevant state from a Duck object in one call.

        Args:
            duck_obj: The ``duck.duck.Duck`` instance.
        """
        try:
            mood = duck_obj.get_mood()
            self.duck_mood = mood.state.value
        except Exception:
            self.duck_mood = "content"

        self.duck_trust = getattr(duck_obj, "trust", 20.0)
        self.personality_scores = dict(getattr(duck_obj, "personality", {}))

    def sync_from_game(self, context_dict: dict) -> None:
        """
        Pull game-level context that does not live on the Duck.

        Expected keys (all optional):
            weather, time_of_day, season, current_biome,
            current_location, active_visitor, active_event.
        """
        # Just stash the raw dict for ContextProvider to use;
        # this method exists so callers have ONE place to push state.
        self._game_context = context_dict

    def check_cooldown(self, category: str) -> bool:
        """Return True if the cooldown for *category* has expired."""
        return time.time() >= self.cooldowns.get(category, 0.0)

    def set_cooldown(self, category: str, seconds: float) -> None:
        """Set a cooldown for *category* starting now."""
        self.cooldowns[category] = time.time() + seconds
