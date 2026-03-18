"""
pytest configuration and shared fixtures for Cheese the Duck tests.

Provides reusable fixtures for DuckStore, DuckState, Duck objects,
event bus mocking, and temporary save directories.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple
from dataclasses import dataclass, field

import pytest

# Ensure the project root is on sys.path so that ``import config`` etc. work
# regardless of how pytest is invoked.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from core.duck_store import DuckState, DuckStore


# ── Mock Event Bus ───────────────────────────────────────────────────────────

@dataclass
class RecordedEvent:
    """A single event captured by the mock event bus."""

    event_type: str
    event: Any


class MockEventBus:
    """Lightweight stand-in for ``core.event_bus.EventBus``.

    Records every emitted event so that tests can assert on what was
    emitted without needing the full threading-capable bus.
    """

    def __init__(self) -> None:
        self.events: List[RecordedEvent] = []
        self._subscribers: Dict[type, List[Any]] = {}

    def emit(self, event: Any) -> None:
        """Record *event* and call any subscribed handlers."""
        self.events.append(RecordedEvent(
            event_type=type(event).__name__,
            event=event,
        ))
        for handler in self._subscribers.get(type(event), []):
            handler(event)

    def emit_async(self, event: Any) -> None:
        """Queue is not implemented — just emit synchronously."""
        self.emit(event)

    def subscribe(self, event_type: type, handler: Any, priority: int = 0) -> Any:
        """Register a handler and return an unsubscribe callable."""
        self._subscribers.setdefault(event_type, []).append(handler)

        def _unsub() -> None:
            try:
                self._subscribers[event_type].remove(handler)
            except (ValueError, KeyError):
                pass

        return _unsub

    def get_events_of_type(self, type_name: str) -> List[RecordedEvent]:
        """Return all recorded events whose type name matches *type_name*."""
        return [e for e in self.events if e.event_type == type_name]

    def clear(self) -> None:
        """Discard all recorded events and subscribers."""
        self.events.clear()
        self._subscribers.clear()


# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def duck_store() -> DuckStore:
    """A fresh DuckStore with default state (needs at 50, trust at 20)."""
    return DuckStore()


@pytest.fixture
def duck_state() -> DuckState:
    """A DuckState snapshot with sensible defaults (all needs 50, trust 50)."""
    return DuckState(
        name="Cheese",
        created_at=0.0,
        growth_stage="hatchling",
        growth_progress=0.0,
        needs={
            "hunger": 50.0,
            "energy": 50.0,
            "fun": 50.0,
            "cleanliness": 50.0,
            "social": 50.0,
        },
        trust=50.0,
        personality={
            "clever_derpy": -30,
            "brave_timid": 0,
            "active_lazy": 20,
            "social_shy": 30,
            "neat_messy": -20,
        },
        mood="content",
        mood_score=50.0,
        motivation=0.5,
        is_sick=False,
        sick_since=None,
        is_hiding=False,
        hiding_coax_visits=0,
        cooldown_until=None,
        current_action=None,
        action_start_time=None,
    )


@pytest.fixture
def mock_event_bus() -> MockEventBus:
    """A MockEventBus that records all emitted events for assertion."""
    return MockEventBus()


@pytest.fixture
def sample_duck():
    """A fully configured Duck object for integration tests.

    Returns a real Duck instance with randomized personality and
    default needs, ready to be wrapped by DuckStore.
    """
    from duck.duck import Duck
    return Duck.create_new(name="TestCheese")


@pytest.fixture
def temp_save_dir(tmp_path: Path) -> Path:
    """A temporary directory for save file tests.

    Returns a Path to a clean temporary directory that is automatically
    cleaned up by pytest's ``tmp_path`` fixture.
    """
    save_dir = tmp_path / "saves"
    save_dir.mkdir()
    return save_dir
