"""
Tests for core.time_system — TimeOfDay, Season, and TimeManager.

Validates time-of-day resolution, season mapping, and backward-compatible
string key generation.
"""
from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock
from datetime import datetime

import pytest

# Ensure project root is on sys.path.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from core.time_system import (
    TimeOfDay,
    Season,
    TimeManager,
    _resolve_time_of_day,
    _resolve_season,
    TIME_PHASES,
    SEASON_PHASES,
)


# ── Helper: mock GameClock ───────────────────────────────────────────────────

def _make_clock(hour: int = 12, month: int = 6) -> MagicMock:
    """Create a mock GameClock whose ``.now`` returns a datetime with the
    given hour and month."""
    clock = MagicMock()
    clock.now = datetime(2026, month, 15, hour, 0, 0)
    return clock


# ═══════════════════════════════════════════════════════════════════════════
# Time of day resolution
# ═══════════════════════════════════════════════════════════════════════════

class TestTimeOfDay:
    """Tests for hour -> TimeOfDay mapping."""

    def test_time_of_day_dawn(self) -> None:
        """Hours 5-6 map to DAWN."""
        assert _resolve_time_of_day(5) == TimeOfDay.DAWN
        assert _resolve_time_of_day(6) == TimeOfDay.DAWN

    def test_time_of_day_morning(self) -> None:
        """Hours 7-10 map to MORNING."""
        assert _resolve_time_of_day(7) == TimeOfDay.MORNING
        assert _resolve_time_of_day(9) == TimeOfDay.MORNING
        assert _resolve_time_of_day(10) == TimeOfDay.MORNING

    def test_time_of_day_all_periods(self) -> None:
        """All 8 time periods are reachable and map correctly."""
        # Map of representative hours to expected TimeOfDay.
        expected = {
            0: TimeOfDay.LATE_NIGHT,
            2: TimeOfDay.LATE_NIGHT,
            4: TimeOfDay.LATE_NIGHT,
            5: TimeOfDay.DAWN,
            6: TimeOfDay.DAWN,
            7: TimeOfDay.MORNING,
            10: TimeOfDay.MORNING,
            11: TimeOfDay.MIDDAY,
            13: TimeOfDay.MIDDAY,
            14: TimeOfDay.AFTERNOON,
            16: TimeOfDay.AFTERNOON,
            17: TimeOfDay.EVENING,
            18: TimeOfDay.EVENING,
            19: TimeOfDay.DUSK,
            20: TimeOfDay.DUSK,
            21: TimeOfDay.NIGHT,
            23: TimeOfDay.NIGHT,
        }
        for hour, tod in expected.items():
            result = _resolve_time_of_day(hour)
            assert result == tod, (
                f"Hour {hour}: expected {tod.value}, got {result.value}"
            )

    def test_time_of_day_boundary_hours(self) -> None:
        """Boundary hours land in the correct phase."""
        # Dawn starts at 5, ends at 7 (exclusive).
        assert _resolve_time_of_day(4) == TimeOfDay.LATE_NIGHT
        assert _resolve_time_of_day(5) == TimeOfDay.DAWN
        assert _resolve_time_of_day(7) == TimeOfDay.MORNING


# ═══════════════════════════════════════════════════════════════════════════
# Season resolution
# ═══════════════════════════════════════════════════════════════════════════

class TestSeason:
    """Tests for month -> Season mapping."""

    def test_season_from_month(self) -> None:
        """Each month maps to the correct season."""
        expected = {
            1: Season.WINTER, 2: Season.WINTER,
            3: Season.SPRING, 4: Season.SPRING, 5: Season.SPRING,
            6: Season.SUMMER, 7: Season.SUMMER, 8: Season.SUMMER,
            9: Season.AUTUMN, 10: Season.AUTUMN, 11: Season.AUTUMN,
            12: Season.WINTER,
        }
        for month, season in expected.items():
            result = _resolve_season(month)
            assert result == season, (
                f"Month {month}: expected {season.value}, got {result.value}"
            )


# ═══════════════════════════════════════════════════════════════════════════
# TimeManager
# ═══════════════════════════════════════════════════════════════════════════

class TestTimeManager:
    """Tests for the TimeManager class."""

    def test_get_time_of_day(self) -> None:
        """TimeManager.get_time_of_day returns correct enum."""
        clock = _make_clock(hour=9)
        tm = TimeManager(clock)
        assert tm.get_time_of_day() == TimeOfDay.MORNING

    def test_get_season(self) -> None:
        """TimeManager.get_season returns correct enum."""
        clock = _make_clock(month=1)
        tm = TimeManager(clock)
        assert tm.get_season() == Season.WINTER

    def test_time_key_backward_compat(self) -> None:
        """get_time_key returns lowercase strings matching biome_visuals keys."""
        clock = _make_clock(hour=5)
        tm = TimeManager(clock)
        key = tm.get_time_key()
        assert isinstance(key, str)
        assert key == "dawn"
        assert key == key.lower()

    def test_season_key_backward_compat(self) -> None:
        """get_season_key returns lowercase strings."""
        clock = _make_clock(month=7)
        tm = TimeManager(clock)
        key = tm.get_season_key()
        assert isinstance(key, str)
        assert key == "summer"
        assert key == key.lower()

    def test_get_time_phase_returns_phase(self) -> None:
        """get_time_phase returns a TimePhase dataclass."""
        clock = _make_clock(hour=12)
        tm = TimeManager(clock)
        phase = tm.get_time_phase()
        assert phase.time_of_day == TimeOfDay.MIDDAY
        assert 0.0 <= phase.ambient_level <= 1.0

    def test_get_season_phase_returns_phase(self) -> None:
        """get_season_phase returns a SeasonPhase dataclass."""
        clock = _make_clock(month=10)
        tm = TimeManager(clock)
        phase = tm.get_season_phase()
        assert phase.season == Season.AUTUMN


# ═══════════════════════════════════════════════════════════════════════════
# Static data integrity
# ═══════════════════════════════════════════════════════════════════════════

class TestStaticData:
    """Tests that static phase data is well-formed."""

    def test_all_time_phases_present(self) -> None:
        """All 8 TimeOfDay enum members have a corresponding TimePhase."""
        for tod in TimeOfDay:
            assert tod in TIME_PHASES, f"Missing TimePhase for {tod.value}"

    def test_all_season_phases_present(self) -> None:
        """All 4 Season enum members have a corresponding SeasonPhase."""
        for season in Season:
            assert season in SEASON_PHASES, (
                f"Missing SeasonPhase for {season.value}"
            )

    def test_time_phase_values_lowercase(self) -> None:
        """All TimeOfDay enum values are lowercase strings."""
        for tod in TimeOfDay:
            assert tod.value == tod.value.lower()

    def test_season_values_lowercase(self) -> None:
        """All Season enum values are lowercase strings."""
        for s in Season:
            assert s.value == s.value.lower()
