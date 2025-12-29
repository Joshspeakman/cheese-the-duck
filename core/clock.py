"""
Game clock and time management for real-time and offline progression.
"""
import time
from datetime import datetime, timedelta
from typing import Optional

from config import TIME_MULTIPLIER, MAX_OFFLINE_HOURS, OFFLINE_DECAY_MULTIPLIER


class GameClock:
    """Manages game time, ticks, and offline progression calculations."""

    def __init__(self):
        self._last_tick = time.time()
        self._last_save_time: Optional[datetime] = None
        self._accumulated_delta = 0.0
        self._time_multiplier = TIME_MULTIPLIER

    @property
    def now(self) -> datetime:
        """Current datetime."""
        return datetime.now()

    @property
    def timestamp(self) -> str:
        """ISO format timestamp for saving."""
        return self.now.isoformat()

    def tick(self) -> float:
        """
        Calculate delta time since last tick.
        Returns the time delta in seconds, adjusted by time multiplier.
        """
        current = time.time()
        delta = current - self._last_tick
        self._last_tick = current
        return delta * self._time_multiplier

    def get_delta_minutes(self, delta_seconds: float) -> float:
        """Convert delta seconds to minutes for need calculations."""
        return delta_seconds / 60.0

    def calculate_offline_time(self, last_played_iso: str) -> dict:
        """
        Calculate how much time passed while offline.

        Returns dict with:
            - hours: float, hours offline (capped)
            - minutes: float, minutes offline (capped)
            - raw_hours: float, actual hours offline
            - capped: bool, whether time was capped
            - decay_multiplier: float, how much to reduce decay
        """
        try:
            last_played = datetime.fromisoformat(last_played_iso.replace('Z', '+00:00'))
            # Handle timezone mismatch - make both naive for comparison
            if last_played.tzinfo is not None:
                last_played = last_played.replace(tzinfo=None)
        except (ValueError, TypeError):
            return {
                "hours": 0,
                "minutes": 0,
                "raw_hours": 0,
                "capped": False,
                "decay_multiplier": 1.0,
            }

        # Ensure self.now is also naive
        now = self.now
        if hasattr(now, 'tzinfo') and now.tzinfo is not None:
            now = now.replace(tzinfo=None)

        delta = now - last_played
        raw_hours = delta.total_seconds() / 3600

        # Cap offline time for fairness
        capped = raw_hours > MAX_OFFLINE_HOURS
        hours = min(raw_hours, MAX_OFFLINE_HOURS)

        return {
            "hours": hours,
            "minutes": hours * 60,
            "raw_hours": raw_hours,
            "capped": capped,
            "decay_multiplier": OFFLINE_DECAY_MULTIPLIER,
        }

    def format_duration(self, hours: float) -> str:
        """Format a duration in hours as a human-readable string."""
        if hours < 1/60:  # Less than a minute
            return "just now"
        elif hours < 1:
            minutes = int(hours * 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''}"
        elif hours < 24:
            h = int(hours)
            m = int((hours - h) * 60)
            if m > 0:
                return f"{h} hour{'s' if h != 1 else ''}, {m} min"
            return f"{h} hour{'s' if h != 1 else ''}"
        else:
            days = int(hours / 24)
            remaining_hours = int(hours % 24)
            if remaining_hours > 0:
                return f"{days} day{'s' if days != 1 else ''}, {remaining_hours} hr"
            return f"{days} day{'s' if days != 1 else ''}"

    def set_time_multiplier(self, multiplier: float):
        """Set time speed multiplier (for testing)."""
        self._time_multiplier = max(0.1, min(100.0, multiplier))

    def get_time_of_day(self) -> str:
        """Get current time of day period."""
        hour = self.now.hour
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 21:
            return "evening"
        else:
            return "night"


# Global clock instance
game_clock = GameClock()
