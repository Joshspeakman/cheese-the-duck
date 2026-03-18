"""
Lightweight event bus for decoupled inter-system communication.

The bus is the central nervous system of the refactored architecture.  Any
system can *emit* a typed event and any number of listeners can *subscribe*
to it — without the emitter knowing who (or whether) anyone is listening.

Design constraints
------------------
* **60 fps budget** — emit/subscribe must be O(1) amortised; no allocations
  on the hot path beyond the event dataclass itself.
* **Thread-safe** — a background audio or LLM worker can emit events without
  corrupting listener lists.
* **Recursion-safe** — guards against emit-inside-emit spirals (max depth 5).
* **Debuggable** — recent event history is retained for inspection.

Usage
-----
>>> from core.event_bus import event_bus, NeedChangedEvent
>>> unsub = event_bus.subscribe(NeedChangedEvent, lambda e: print(e))
>>> event_bus.emit(NeedChangedEvent(
...     source="needs", need="hunger",
...     old_value=80.0, new_value=75.0, reason="decay"))
>>> unsub()                   # unsubscribe when done
"""
from __future__ import annotations

import threading
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import (
    Any,
    Callable,
    Deque,
    Dict,
    List,
    Optional,
    Type,
)

from core.exceptions import EventError


# ── Event Dataclasses ───────────────────────────────────────────────────────

@dataclass
class GameEvent:
    """Base class for every event that flows through the bus.

    Attributes
    ----------
    source : str
        Identifier of the system that emitted the event (e.g. ``"needs"``,
        ``"weather"``).  Useful for debugging and filtering.
    timestamp : float
        ``time.time()`` when the event was created.  Auto-populated.
    """
    source: str = ""
    timestamp: float = field(default_factory=time.time)


# ── Need / Duck State ───────────────────────────────────────────────────────

@dataclass
class NeedChangedEvent(GameEvent):
    """Fired whenever a duck need value changes."""
    need: str = ""
    old_value: float = 0.0
    new_value: float = 0.0
    reason: str = ""


@dataclass
class MoodChangedEvent(GameEvent):
    """Fired when the duck's mood label transitions."""
    old_mood: str = ""
    new_mood: str = ""


@dataclass
class TrustChangedEvent(GameEvent):
    """Fired when the duck's trust in the player changes."""
    old_value: float = 0.0
    new_value: float = 0.0
    reason: str = ""


@dataclass
class ActionPerformedEvent(GameEvent):
    """Fired after the player or AI performs an action."""
    action: str = ""
    item: Optional[str] = None
    result: str = ""


# ── World / Environment ─────────────────────────────────────────────────────

@dataclass
class WeatherChangedEvent(GameEvent):
    """Fired when the weather type transitions."""
    old_weather: str = ""
    new_weather: str = ""
    intensity: float = 0.0


@dataclass
class TimeChangedEvent(GameEvent):
    """Fired when the time-of-day phase transitions (e.g. morning -> midday)."""
    old_time: str = ""
    new_time: str = ""
    hour: int = 0


@dataclass
class SeasonChangedEvent(GameEvent):
    """Fired when the season transitions."""
    old_season: str = ""
    new_season: str = ""


@dataclass
class BiomeChangedEvent(GameEvent):
    """Fired when the duck moves to a different biome."""
    old_biome: str = ""
    new_biome: str = ""


# ── Social / Visitors ───────────────────────────────────────────────────────

@dataclass
class VisitorArrivedEvent(GameEvent):
    """Fired when a visitor duck arrives."""
    visitor_name: str = ""


@dataclass
class VisitorDepartedEvent(GameEvent):
    """Fired when a visitor duck leaves."""
    visitor_name: str = ""


@dataclass
class ConversationEvent(GameEvent):
    """Fired when a conversation line is spoken."""
    speaker: str = ""
    message: str = ""
    response_source: str = ""


# ── Items / Progression ─────────────────────────────────────────────────────

@dataclass
class ItemUsedEvent(GameEvent):
    """Fired when an inventory item is used."""
    item_name: str = ""
    target: str = ""


@dataclass
class AchievementUnlockedEvent(GameEvent):
    """Fired when a new achievement is unlocked."""
    achievement_id: str = ""
    name: str = ""


# ── Status Effects ──────────────────────────────────────────────────────────

@dataclass
class SicknessEvent(GameEvent):
    """Fired when sickness starts or ends."""
    started: bool = True
    cause: str = ""


@dataclass
class HidingEvent(GameEvent):
    """Fired when the duck starts or stops hiding."""
    started: bool = True


# ── Event Bus ───────────────────────────────────────────────────────────────

_MAX_RECURSION_DEPTH: int = 5
_DEFAULT_HISTORY_SIZE: int = 50


class EventBus:
    """Central publish/subscribe event dispatcher.

    Thread-safe.  Subscribers are called synchronously on ``emit()`` and
    asynchronously (batched) when using ``emit_async()`` + ``process_queued()``.

    Parameters
    ----------
    history_size : int
        Maximum number of past events to retain per event type for debugging.
    """

    def __init__(self, history_size: int = _DEFAULT_HISTORY_SIZE) -> None:
        self._lock = threading.Lock()
        self._subscribers: Dict[
            Type[GameEvent],
            List[tuple[int, int, Callable[[Any], None]]],
        ] = defaultdict(list)
        # _next_id provides a stable insertion order so that subscribers with
        # equal priority are called in subscription order.
        self._next_id: int = 0
        self._queue: Deque[GameEvent] = deque()
        self._history: Dict[Type[GameEvent], Deque[GameEvent]] = defaultdict(
            lambda: deque(maxlen=history_size)
        )
        self._history_size = history_size
        self._depth: int = 0

    # ── subscribe / unsubscribe ─────────────────────────────────────────

    def subscribe(
        self,
        event_type: Type[GameEvent],
        handler: Callable[[Any], None],
        priority: int = 0,
    ) -> Callable[[], None]:
        """Register *handler* for events of *event_type*.

        Parameters
        ----------
        event_type : Type[GameEvent]
            The concrete event class to listen for.
        handler : callable
            ``handler(event)`` will be called on each matching emit.
        priority : int
            Higher priority handlers are called first.  Default ``0``.

        Returns
        -------
        callable
            A zero-argument callable that removes this subscription.
        """
        with self._lock:
            sub_id = self._next_id
            self._next_id += 1
            entry = (priority, sub_id, handler)
            subs = self._subscribers[event_type]
            subs.append(entry)
            # Sort: highest priority first; within same priority, earliest first.
            subs.sort(key=lambda e: (-e[0], e[1]))

        def _unsubscribe() -> None:
            with self._lock:
                try:
                    self._subscribers[event_type].remove(entry)
                except ValueError:
                    pass  # already removed

        return _unsubscribe

    # ── emit (synchronous) ──────────────────────────────────────────────

    def emit(self, event: GameEvent) -> None:
        """Emit *event* synchronously, calling all subscribers immediately.

        Raises
        ------
        EventError
            If recursion depth exceeds the safety limit.
        """
        if self._depth >= _MAX_RECURSION_DEPTH:
            raise EventError(
                f"Event recursion limit ({_MAX_RECURSION_DEPTH}) exceeded",
                details={
                    "event_type": type(event).__name__,
                    "source": event.source,
                },
            )

        # Snapshot the subscriber list under the lock so that handlers can
        # safely subscribe/unsubscribe without iterator invalidation.
        with self._lock:
            handlers = list(self._subscribers.get(type(event), []))
            self._history[type(event)].append(event)

        self._depth += 1
        try:
            for _priority, _sid, handler in handlers:
                try:
                    handler(event)
                except Exception:
                    # Swallow handler exceptions so one broken listener cannot
                    # break the emitter.  In a production build this would go
                    # through the game logger.
                    pass
        finally:
            self._depth -= 1

    # ── emit_async (queued) ─────────────────────────────────────────────

    def emit_async(self, event: GameEvent) -> None:
        """Queue *event* for deferred processing on the next tick.

        Use this from background threads or when you want to avoid deep
        call stacks during a single frame.
        """
        with self._lock:
            self._queue.append(event)

    def process_queued(self) -> int:
        """Process all queued async events.  Call once per game tick.

        Returns
        -------
        int
            Number of events processed.
        """
        # Drain the queue under the lock, then process outside of it.
        with self._lock:
            batch = list(self._queue)
            self._queue.clear()

        for event in batch:
            self.emit(event)

        return len(batch)

    # ── history ─────────────────────────────────────────────────────────

    def get_history(
        self,
        event_type: Type[GameEvent],
        limit: int = 10,
    ) -> List[GameEvent]:
        """Return the most recent events of *event_type* (newest last).

        Parameters
        ----------
        event_type : Type[GameEvent]
            The event class to query.
        limit : int
            Maximum number of events to return.  Default ``10``.
        """
        with self._lock:
            history = self._history.get(event_type, deque())
            # deque is oldest-first; slice from the end for the most recent.
            items = list(history)
            return items[-limit:]

    # ── housekeeping ────────────────────────────────────────────────────

    def clear(self) -> None:
        """Remove all subscribers, queued events, and history.

        Intended for tests and full-game resets.
        """
        with self._lock:
            self._subscribers.clear()
            self._queue.clear()
            self._history.clear()
            self._next_id = 0
            self._depth = 0


# ── Module-level singleton ──────────────────────────────────────────────────

event_bus: EventBus = EventBus()
