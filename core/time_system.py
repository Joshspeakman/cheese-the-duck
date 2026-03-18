"""
Unified Time & Season System.

Consolidates the four inconsistent time-of-day calculations that previously
lived in ``core/clock.py``, ``ui/day_night.py``, ``ui/renderer.py``, and
``duck/seasonal_clothing.py`` into a single authoritative source.

Every subsystem that needs to know "what time is it?" or "what season?" should
import from here instead of computing it independently.

Backward-compatibility helpers (``get_current_time_of_day()``,
``get_current_season()``) and string-key accessors (``get_time_key()``,
``get_season_key()``) are provided so that existing code (biome_visuals,
renderer, etc.) can migrate incrementally.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, TYPE_CHECKING

from core.event_bus import (
    event_bus,
    SeasonChangedEvent,
    TimeChangedEvent,
)

if TYPE_CHECKING:
    from core.clock import GameClock


# ── Enums ───────────────────────────────────────────────────────────────────

class TimeOfDay(Enum):
    """Eight fine-grained time-of-day phases.

    Values are lowercase strings matching the keys used by
    ``ui.biome_visuals.BIOME_TIME_TINTS`` and ``ui.renderer`` so that
    ``phase.value`` can be used directly as a dict key for backward compat.
    """
    DAWN = "dawn"
    MORNING = "morning"
    MIDDAY = "midday"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    DUSK = "dusk"
    NIGHT = "night"
    LATE_NIGHT = "late_night"


class Season(Enum):
    """The four calendar seasons.

    Values are lowercase strings matching existing dict keys throughout
    the codebase (biome_visuals, seasonal_clothing, etc.).
    """
    SPRING = "spring"
    SUMMER = "summer"
    AUTUMN = "autumn"
    WINTER = "winter"


# ── Phase Dataclasses ───────────────────────────────────────────────────────

@dataclass(frozen=True)
class TimePhase:
    """Static definition of a time-of-day phase.

    Attributes
    ----------
    time_of_day : TimeOfDay
        Which phase this describes.
    start_hour : int
        Inclusive start hour (0-23).
    end_hour : int
        Exclusive end hour (0-23).  Wraps around midnight when
        ``start_hour > end_hour`` (e.g. NIGHT: 21 -> 0).
    ambient_level : float
        Normalised light level, 0.0 (pitch dark) to 1.0 (full sun).
    description : str
        Short flavour text for UI display.
    mood_modifier : float
        Additive mood-score modifier applied while this phase is active.
        Positive = mood boost, negative = mood drain.
    """
    time_of_day: TimeOfDay
    start_hour: int
    end_hour: int
    ambient_level: float
    description: str
    mood_modifier: float = 0.0


@dataclass(frozen=True)
class SeasonPhase:
    """Static definition of a calendar season.

    Attributes
    ----------
    season : Season
        Which season this describes.
    months : tuple[int, ...]
        Calendar months (1-12) that belong to this season.
    temperature_base : float
        Baseline temperature for weather calculations (arbitrary units).
    description : str
        Short flavour text for UI display.
    """
    season: Season
    months: tuple
    temperature_base: float
    description: str


# ── Static Phase Data ───────────────────────────────────────────────────────
# Hour ranges match ui/day_night.py's DayNightSystem.get_time_of_day() and
# the renderer's _get_time_of_day_elements().

TIME_PHASES: Dict[TimeOfDay, TimePhase] = {
    TimeOfDay.DAWN: TimePhase(
        time_of_day=TimeOfDay.DAWN,
        start_hour=5,
        end_hour=7,
        ambient_level=0.4,
        description="The sky turns pink and orange as the sun rises.",
        mood_modifier=2.0,
    ),
    TimeOfDay.MORNING: TimePhase(
        time_of_day=TimeOfDay.MORNING,
        start_hour=7,
        end_hour=11,
        ambient_level=0.8,
        description="Fresh morning air and bright skies.",
        mood_modifier=3.0,
    ),
    TimeOfDay.MIDDAY: TimePhase(
        time_of_day=TimeOfDay.MIDDAY,
        start_hour=11,
        end_hour=14,
        ambient_level=1.0,
        description="The sun is at its highest point.",
        mood_modifier=1.0,
    ),
    TimeOfDay.AFTERNOON: TimePhase(
        time_of_day=TimeOfDay.AFTERNOON,
        start_hour=14,
        end_hour=17,
        ambient_level=0.9,
        description="Warm afternoon hours.",
        mood_modifier=1.0,
    ),
    TimeOfDay.EVENING: TimePhase(
        time_of_day=TimeOfDay.EVENING,
        start_hour=17,
        end_hour=19,
        ambient_level=0.6,
        description="Golden hour as the sun starts to set.",
        mood_modifier=0.0,
    ),
    TimeOfDay.DUSK: TimePhase(
        time_of_day=TimeOfDay.DUSK,
        start_hour=19,
        end_hour=21,
        ambient_level=0.3,
        description="The sky turns purple and orange as night approaches.",
        mood_modifier=-1.0,
    ),
    TimeOfDay.NIGHT: TimePhase(
        time_of_day=TimeOfDay.NIGHT,
        start_hour=21,
        end_hour=0,
        ambient_level=0.15,
        description="Stars twinkle in the dark sky.",
        mood_modifier=-2.0,
    ),
    TimeOfDay.LATE_NIGHT: TimePhase(
        time_of_day=TimeOfDay.LATE_NIGHT,
        start_hour=0,
        end_hour=5,
        ambient_level=0.1,
        description="Deep night, the world is quiet.",
        mood_modifier=-3.0,
    ),
}

SEASON_PHASES: Dict[Season, SeasonPhase] = {
    Season.SPRING: SeasonPhase(
        season=Season.SPRING,
        months=(3, 4, 5),
        temperature_base=15.0,
        description="Flowers bloom and rain showers bring new life.",
    ),
    Season.SUMMER: SeasonPhase(
        season=Season.SUMMER,
        months=(6, 7, 8),
        temperature_base=28.0,
        description="Long sunny days and warm nights.",
    ),
    Season.AUTUMN: SeasonPhase(
        season=Season.AUTUMN,
        months=(9, 10, 11),
        temperature_base=12.0,
        description="Leaves turn golden and the air grows crisp.",
    ),
    Season.WINTER: SeasonPhase(
        season=Season.WINTER,
        months=(12, 1, 2),
        temperature_base=2.0,
        description="Snow falls and the world sleeps under a white blanket.",
    ),
}


# ── Lookup helpers (O(1) via pre-built tables) ──────────────────────────────

# Build a month -> Season lookup for fast season resolution.
_MONTH_TO_SEASON: Dict[int, Season] = {}
for _sp in SEASON_PHASES.values():
    for _m in _sp.months:
        _MONTH_TO_SEASON[_m] = _sp.season

# Build an ordered list of (start_hour, TimeOfDay) for hour -> phase lookup.
# Sorted so that a simple linear scan from the end finds the right bracket.
_HOUR_BRACKETS: List[tuple] = sorted(
    [(phase.start_hour, phase.time_of_day) for phase in TIME_PHASES.values()],
    key=lambda t: t[0],
)


def _resolve_time_of_day(hour: int) -> TimeOfDay:
    """Return the ``TimeOfDay`` for a given hour (0-23).

    Uses the same boundary logic as ``ui/day_night.py`` and ``ui/renderer.py``:
    LATE_NIGHT 0-4, DAWN 5-6, MORNING 7-10, MIDDAY 11-13, AFTERNOON 14-16,
    EVENING 17-18, DUSK 19-20, NIGHT 21-23.
    """
    # Walk the brackets in reverse; the first one whose start_hour <= hour wins.
    # Because LATE_NIGHT starts at 0 and NIGHT starts at 21, hours 21-23 land
    # on NIGHT and hours 0-4 land on LATE_NIGHT — matching existing behaviour.
    for start, tod in reversed(_HOUR_BRACKETS):
        if hour >= start:
            return tod
    # Fallback (should not be reachable for hours 0-23).
    return TimeOfDay.LATE_NIGHT


def _resolve_season(month: int) -> Season:
    """Return the ``Season`` for a given month (1-12)."""
    return _MONTH_TO_SEASON.get(month, Season.SPRING)


# ── TimeManager ─────────────────────────────────────────────────────────────

class TimeManager:
    """Single authoritative source for current time-of-day and season.

    Wraps an existing ``GameClock`` (for its ``now`` property) and adds
    phase/season tracking with automatic event emission on transitions.

    Parameters
    ----------
    clock : GameClock
        The game clock instance to read the current time from.
    """

    def __init__(self, clock: "GameClock") -> None:
        self._clock = clock
        # Seed previous values so the first ``update()`` does not emit a
        # spurious change event unless the time genuinely differs.
        self._prev_time: Optional[TimeOfDay] = None
        self._prev_season: Optional[Season] = None

    # ── Core queries ────────────────────────────────────────────────────

    def get_hour(self) -> int:
        """Return the current real-world hour (0-23)."""
        return self._clock.now.hour

    def get_time_of_day(self) -> TimeOfDay:
        """Return the current ``TimeOfDay`` enum value."""
        return _resolve_time_of_day(self.get_hour())

    def get_season(self) -> Season:
        """Return the current ``Season`` enum value."""
        return _resolve_season(self._clock.now.month)

    def get_time_phase(self) -> TimePhase:
        """Return the full ``TimePhase`` dataclass for the current time."""
        return TIME_PHASES[self.get_time_of_day()]

    def get_season_phase(self) -> SeasonPhase:
        """Return the full ``SeasonPhase`` dataclass for the current season."""
        return SEASON_PHASES[self.get_season()]

    # ── Backward-compatibility string keys ──────────────────────────────

    def get_time_key(self) -> str:
        """Return a lowercase string key (e.g. ``"dawn"``, ``"late_night"``).

        Matches the dict keys used by ``ui.biome_visuals.BIOME_TIME_TINTS``
        and ``ui.renderer._get_time_of_day_elements()``.
        """
        return self.get_time_of_day().value

    def get_season_key(self) -> str:
        """Return a lowercase string key (e.g. ``"spring"``, ``"winter"``).

        Matches the dict keys used by ``ui.biome_visuals`` and
        ``duck.seasonal_clothing``.
        """
        return self.get_season().value

    # ── Tick / update ───────────────────────────────────────────────────

    def update(self) -> None:
        """Check for time/season transitions and emit events if needed.

        Should be called once per game tick (typically once per second).
        """
        current_time = self.get_time_of_day()
        current_season = self.get_season()

        if self._prev_time is not None and current_time != self._prev_time:
            event_bus.emit(TimeChangedEvent(
                source="time_system",
                old_time=self._prev_time.value,
                new_time=current_time.value,
                hour=self.get_hour(),
            ))

        if self._prev_season is not None and current_season != self._prev_season:
            event_bus.emit(SeasonChangedEvent(
                source="time_system",
                old_season=self._prev_season.value,
                new_season=current_season.value,
            ))

        self._prev_time = current_time
        self._prev_season = current_season


# ── Module-level convenience ────────────────────────────────────────────────
# These free functions let existing code migrate with minimal churn.  They
# read directly from ``datetime.now()`` (matching the old behaviour) so they
# work even before a ``TimeManager`` is instantiated.

def get_current_time_of_day() -> TimeOfDay:
    """Return the current ``TimeOfDay`` based on the system clock.

    Drop-in replacement for the scattered ``get_time_of_day()`` helpers in
    ``core.clock``, ``ui.day_night``, and ``ui.renderer``.
    """
    return _resolve_time_of_day(datetime.now().hour)


def get_current_season() -> Season:
    """Return the current ``Season`` based on the system clock.

    Drop-in replacement for ``duck.seasonal_clothing.get_current_season()``.
    """
    return _resolve_season(datetime.now().month)
