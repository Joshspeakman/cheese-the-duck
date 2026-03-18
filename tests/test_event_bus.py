"""
Tests for core.event_bus.EventBus.

Validates the publish/subscribe system, priority ordering, async queue,
recursion guards, and event history.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Ensure project root is on sys.path.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from core.event_bus import (
    EventBus,
    GameEvent,
    NeedChangedEvent,
    MoodChangedEvent,
    TrustChangedEvent,
)
from core.exceptions import EventError


@pytest.fixture
def bus() -> EventBus:
    """A fresh EventBus instance for each test."""
    return EventBus(history_size=50)


# ═══════════════════════════════════════════════════════════════════════════
# Basic pub/sub
# ═══════════════════════════════════════════════════════════════════════════

class TestSubscribeAndEmit:
    """Tests for basic subscribe/emit flow."""

    def test_subscribe_and_emit(self, bus: EventBus) -> None:
        """A subscribed handler receives emitted events."""
        received = []
        bus.subscribe(NeedChangedEvent, lambda e: received.append(e))

        event = NeedChangedEvent(
            source="test", need="hunger", old_value=80.0, new_value=75.0
        )
        bus.emit(event)

        assert len(received) == 1
        assert received[0].need == "hunger"
        assert received[0].old_value == 80.0

    def test_unsubscribe(self, bus: EventBus) -> None:
        """After unsubscribing, the handler is no longer called."""
        received = []
        unsub = bus.subscribe(NeedChangedEvent, lambda e: received.append(e))

        bus.emit(NeedChangedEvent(source="test", need="hunger"))
        assert len(received) == 1

        unsub()
        bus.emit(NeedChangedEvent(source="test", need="energy"))
        assert len(received) == 1  # No new event received.

    def test_multiple_subscribers(self, bus: EventBus) -> None:
        """Multiple handlers for the same event type all receive the event."""
        results_a = []
        results_b = []
        bus.subscribe(MoodChangedEvent, lambda e: results_a.append(e))
        bus.subscribe(MoodChangedEvent, lambda e: results_b.append(e))

        bus.emit(MoodChangedEvent(source="test", old_mood="content", new_mood="happy"))

        assert len(results_a) == 1
        assert len(results_b) == 1

    def test_no_subscribers(self, bus: EventBus) -> None:
        """Emitting with no subscribers does not raise an error."""
        # This should complete without any exception.
        bus.emit(TrustChangedEvent(
            source="test", old_value=20.0, new_value=25.0
        ))


# ═══════════════════════════════════════════════════════════════════════════
# Priority ordering
# ═══════════════════════════════════════════════════════════════════════════

class TestPriorityOrdering:
    """Tests for handler priority."""

    def test_priority_ordering(self, bus: EventBus) -> None:
        """Higher-priority handlers are called before lower-priority ones."""
        call_order = []

        bus.subscribe(
            NeedChangedEvent,
            lambda e: call_order.append("low"),
            priority=0,
        )
        bus.subscribe(
            NeedChangedEvent,
            lambda e: call_order.append("high"),
            priority=10,
        )
        bus.subscribe(
            NeedChangedEvent,
            lambda e: call_order.append("mid"),
            priority=5,
        )

        bus.emit(NeedChangedEvent(source="test", need="hunger"))

        assert call_order == ["high", "mid", "low"]


# ═══════════════════════════════════════════════════════════════════════════
# Async queue
# ═══════════════════════════════════════════════════════════════════════════

class TestAsyncQueue:
    """Tests for emit_async and process_queued."""

    def test_emit_async_and_process(self, bus: EventBus) -> None:
        """Events queued via emit_async are delivered by process_queued."""
        received = []
        bus.subscribe(NeedChangedEvent, lambda e: received.append(e))

        bus.emit_async(NeedChangedEvent(
            source="test", need="fun", old_value=50.0, new_value=45.0
        ))

        # Not yet delivered.
        assert len(received) == 0

        count = bus.process_queued()
        assert count == 1
        assert len(received) == 1
        assert received[0].need == "fun"


# ═══════════════════════════════════════════════════════════════════════════
# Recursion guard
# ═══════════════════════════════════════════════════════════════════════════

class TestRecursionGuard:
    """Tests for the recursion depth limit."""

    def test_recursion_guard(self, bus: EventBus) -> None:
        """Emitting from within a handler is allowed up to the depth limit.

        Beyond the limit, an EventError is raised, preventing infinite
        loops.
        """
        depth_reached = []

        def recursive_handler(event: NeedChangedEvent) -> None:
            depth_reached.append(1)
            # Re-emit the same event type, which would cause infinite
            # recursion without the guard.
            bus.emit(NeedChangedEvent(source="recursive", need="hunger"))

        bus.subscribe(NeedChangedEvent, recursive_handler)

        # The bus should raise EventError when recursion is too deep,
        # but the outer emit swallows handler exceptions.  So we expect
        # the depth counter to stop at the max recursion limit.
        bus.emit(NeedChangedEvent(source="test", need="hunger"))

        # Should have recursed up to the limit (default 5).
        assert len(depth_reached) <= 6  # 5 recursive + 1 original at most


# ═══════════════════════════════════════════════════════════════════════════
# Event history
# ═══════════════════════════════════════════════════════════════════════════

class TestEventHistory:
    """Tests for the get_history method."""

    def test_event_history(self, bus: EventBus) -> None:
        """get_history returns recent events of the requested type."""
        for i in range(5):
            bus.emit(NeedChangedEvent(
                source="test",
                need="hunger",
                old_value=float(50 - i),
                new_value=float(50 - i - 1),
            ))

        history = bus.get_history(NeedChangedEvent, limit=3)
        assert len(history) == 3
        # Newest should be last.
        assert history[-1].old_value == 46.0

    def test_history_only_returns_matching_type(self, bus: EventBus) -> None:
        """History for one event type does not include other types."""
        bus.emit(NeedChangedEvent(source="test", need="hunger"))
        bus.emit(MoodChangedEvent(source="test", old_mood="content", new_mood="happy"))

        need_history = bus.get_history(NeedChangedEvent)
        assert len(need_history) == 1
        assert all(isinstance(e, NeedChangedEvent) for e in need_history)

    def test_clear_resets_everything(self, bus: EventBus) -> None:
        """bus.clear() removes all subscribers, queue, and history."""
        received = []
        bus.subscribe(NeedChangedEvent, lambda e: received.append(e))
        bus.emit(NeedChangedEvent(source="test", need="hunger"))

        bus.clear()

        # History was wiped by clear.
        assert bus.get_history(NeedChangedEvent) == []

        bus.emit(NeedChangedEvent(source="test", need="hunger"))
        # Handler was removed by clear, so received should still be 1.
        assert len(received) == 1
