"""
Tick / update timing scheduler.

Replaces the sprawling ``if time.time() - self._last_*_check > INTERVAL``
pattern found throughout ``Game._update()`` with a declarative registry of
periodic callbacks.

Usage from game.py::

    self.update_scheduler = UpdateScheduler()
    self.update_scheduler.register("atmosphere", self._check_atmosphere, 30.0)
    self.update_scheduler.register("events",     self._check_events,     30.0)
    self.update_scheduler.register("auto_save",  self._save_game,        60.0)

    # In _update():
    self.update_scheduler.update(time.time())
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional


# ── Common interval constants (seconds) ──────────────────────────────
# Gathered from game.py and config.py defaults.

TICK_INTERVAL = 1.0              # Core game tick (need decay, mood, etc.)
SAVE_INTERVAL = 60.0             # Auto-save
EVENT_CHECK_INTERVAL = 30.0      # Random event rolls
ATMOSPHERE_CHECK_INTERVAL = 30.0 # Weather / visitor updates
AREA_EVENT_INTERVAL = 45.0       # Area-specific events
SPONTANEOUS_TRAVEL_INTERVAL = 30.0  # Duck decides to wander
RANDOM_COMMENT_INTERVAL = 45.0   # Idle contextual quips
CRAFT_CHECK_INTERVAL = 2.0       # Crafting progress poll
BUILD_CHECK_INTERVAL = 5.0       # Building progress poll
WEATHER_DAMAGE_INTERVAL = 60.0   # Structure weather damage
DIARY_FLUSH_INTERVAL = 30.0      # Flush pending diary entries


@dataclass
class SystemUpdate:
    """A single registered periodic callback."""
    system_name: str
    callback: Callable[[], Any]
    interval: float                   # seconds between runs
    last_update: float = 0.0         # epoch timestamp of last execution
    enabled: bool = True
    # Bookkeeping for get_stats()
    run_count: int = field(default=0, repr=False)
    total_duration: float = field(default=0.0, repr=False)


class UpdateScheduler:
    """
    Registry of named periodic callbacks.

    Each registered system has an *interval*; on every ``update()`` call the
    scheduler checks which systems are due and fires their callbacks.
    """

    def __init__(self) -> None:
        self._systems: Dict[str, SystemUpdate] = {}

    # ── Registration ──────────────────────────────────────────────────

    def register(
        self,
        name: str,
        callback: Callable[[], Any],
        interval: float,
        enabled: bool = True,
    ) -> None:
        """
        Register (or re-register) a periodic system.

        Args:
            name:     Unique identifier for the system.
            callback: Zero-arg callable invoked when the system is due.
            interval: Minimum seconds between successive invocations.
            enabled:  Whether the system starts enabled.
        """
        self._systems[name] = SystemUpdate(
            system_name=name,
            callback=callback,
            interval=interval,
            last_update=0.0,
            enabled=enabled,
        )

    def unregister(self, name: str) -> None:
        """Remove a system by name.  No-op if the name is unknown."""
        self._systems.pop(name, None)

    # ── Enable / disable ──────────────────────────────────────────────

    def enable(self, name: str) -> None:
        """Enable a registered system.  Raises ``KeyError`` if unknown."""
        self._systems[name].enabled = True

    def disable(self, name: str) -> None:
        """Disable a registered system.  Raises ``KeyError`` if unknown."""
        self._systems[name].enabled = False

    def is_enabled(self, name: str) -> bool:
        """Check whether a system is enabled.  Raises ``KeyError`` if unknown."""
        return self._systems[name].enabled

    # ── Core loop ─────────────────────────────────────────────────────

    def update(self, current_time: Optional[float] = None) -> None:
        """
        Run all enabled systems whose interval has elapsed.

        Args:
            current_time: Epoch timestamp (defaults to ``time.time()``).
        """
        if current_time is None:
            current_time = time.time()

        for sys in self._systems.values():
            if not sys.enabled:
                continue
            if current_time - sys.last_update < sys.interval:
                continue

            t0 = time.monotonic()
            try:
                sys.callback()
            except Exception:
                # Subsystems must not crash the game loop.
                # In a production game you'd log this; for now swallow silently
                # just as the existing ``try/except: pass`` blocks do in game.py.
                pass
            elapsed = time.monotonic() - t0

            sys.last_update = current_time
            sys.run_count += 1
            sys.total_duration += elapsed

    # ── Immediate execution ───────────────────────────────────────────

    def force_run(self, name: str) -> None:
        """
        Execute a system immediately, regardless of its interval timer.

        Raises ``KeyError`` if the name is unknown.
        """
        sys = self._systems[name]
        t0 = time.monotonic()
        sys.callback()
        elapsed = time.monotonic() - t0
        sys.last_update = time.time()
        sys.run_count += 1
        sys.total_duration += elapsed

    # ── Diagnostics ───────────────────────────────────────────────────

    def get_stats(self) -> Dict[str, Dict[str, Any]]:
        """
        Return debugging statistics for every registered system.

        Returns:
            Mapping of ``system_name`` to a dict with keys:
            ``interval``, ``enabled``, ``last_update``, ``run_count``,
            ``avg_duration_ms``.
        """
        stats: Dict[str, Dict[str, Any]] = {}
        for name, sys in self._systems.items():
            avg_ms = (sys.total_duration / sys.run_count * 1000) if sys.run_count else 0.0
            stats[name] = {
                "interval": sys.interval,
                "enabled": sys.enabled,
                "last_update": sys.last_update,
                "run_count": sys.run_count,
                "avg_duration_ms": round(avg_ms, 3),
            }
        return stats

    def get_registered_names(self) -> list[str]:
        """Return a sorted list of all registered system names."""
        return sorted(self._systems.keys())

    # ── Dunder ────────────────────────────────────────────────────────

    def __len__(self) -> int:
        return len(self._systems)

    def __contains__(self, name: str) -> bool:
        return name in self._systems

    def __repr__(self) -> str:
        enabled = sum(1 for s in self._systems.values() if s.enabled)
        return f"UpdateScheduler({len(self._systems)} systems, {enabled} enabled)"
