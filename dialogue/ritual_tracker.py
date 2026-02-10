"""
Ritual Tracker — detects player habits and lets the duck comment on them.

If you feed the duck at 8am every day, Cheese will notice. And if you're
late one morning, Cheese will notice that too. Not that he was waiting.

Detection: Rolling window of last 30 timestamps per action. If the median
hour has a tight spread (IQR < 2h), it's a ritual. Confidence grows over
a week of consistency.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple


# ── Constants ───────────────────────────────────────────────────────────
HISTORY_WINDOW = 30        # Max timestamps to keep per action
MIN_ENTRIES_FOR_RITUAL = 5  # Need 5+ entries in rolling window
IQR_THRESHOLD_HOURS = 2.0  # Max inter-quartile range for "consistent"
MAX_CONFIDENCE = 1.0
CONFIDENCE_PER_DAY = 1.0 / 7.0  # ~1 week to full confidence
COMMENT_COOLDOWN_HOURS = 20  # Don't comment on same ritual twice in 20h
BROKEN_GRACE_MINUTES = 90   # How late before "broken" kicks in


# ── Data structures ─────────────────────────────────────────────────────
@dataclass
class ActionTimestamp:
    """A single recorded interaction with wall-clock time."""
    action: str       # "feed", "play", "clean", "pet", "sleep"
    hour: int         # 0-23
    minute: int       # 0-59
    weekday: int      # 0=Monday, 6=Sunday
    timestamp: float  # time.time() epoch

    def to_dict(self) -> dict:
        return {
            "action": self.action,
            "hour": self.hour,
            "minute": self.minute,
            "weekday": self.weekday,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ActionTimestamp":
        return cls(
            action=data.get("action", ""),
            hour=data.get("hour", 0),
            minute=data.get("minute", 0),
            weekday=data.get("weekday", 0),
            timestamp=data.get("timestamp", 0.0),
        )


@dataclass
class RitualPattern:
    """A detected routine for a specific action."""
    action: str                    # Which action
    typical_hour: int              # Most common hour (0-23)
    typical_minute: int            # Median minute within that hour
    confidence: float              # 0.0-1.0
    streak: int                    # Consecutive days the ritual was matched
    last_matched: float            # Epoch of last match
    last_commented: float          # Epoch of last duck comment about this
    times_acknowledged: int        # Total times duck mentioned it
    broken_days: int               # Consecutive days missed

    def to_dict(self) -> dict:
        return {
            "action": self.action,
            "typical_hour": self.typical_hour,
            "typical_minute": self.typical_minute,
            "confidence": self.confidence,
            "streak": self.streak,
            "last_matched": self.last_matched,
            "last_commented": self.last_commented,
            "times_acknowledged": self.times_acknowledged,
            "broken_days": self.broken_days,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "RitualPattern":
        return cls(
            action=data.get("action", ""),
            typical_hour=data.get("typical_hour", 12),
            typical_minute=data.get("typical_minute", 0),
            confidence=data.get("confidence", 0.0),
            streak=data.get("streak", 0),
            last_matched=data.get("last_matched", 0.0),
            last_commented=data.get("last_commented", 0.0),
            times_acknowledged=data.get("times_acknowledged", 0),
            broken_days=data.get("broken_days", 0),
        )

    @property
    def is_established(self) -> bool:
        """Ritual is established enough to comment on."""
        return self.confidence >= 0.4

    @property
    def window_start_minutes(self) -> int:
        """Start of the expected window (minutes from midnight)."""
        return self.typical_hour * 60 + self.typical_minute - BROKEN_GRACE_MINUTES // 2

    @property
    def window_end_minutes(self) -> int:
        """End of the expected window (minutes from midnight)."""
        return self.typical_hour * 60 + self.typical_minute + BROKEN_GRACE_MINUTES // 2


# ── Ritual observation lines (deadpan voice) ────────────────────────────

# When player matches a ritual — keyed by confidence tier
_RITUAL_MATCH_LINES = {
    # Low confidence (just emerging pattern)
    "emerging": [
        "You like {time_of_day}s for {action}ing, huh.",
        "This is becoming a pattern. The {action}ing. Around now.",
        "Let me guess. {Action} time.",
    ],
    # Medium confidence (established)
    "established": [
        "Right on schedule.",
        "{Hour_ampm}. {Action} time. I know the drill.",
        "There it is. The {hour_ampm} {action}. Reliable.",
        "You're consistent. I'll give you that.",
    ],
    # High confidence (deeply routine)
    "deep": [
        "I had this penciled in.",
        "{Action} at {hour_ampm}. Day {streak}. Not that I'm counting.",
        "If I had a watch, I wouldn't need one. I've got you.",
        "My internal clock is just you, at this point.",
        "{Hour_ampm}. Like clockwork. I'd set my feathers by it.",
    ],
}

# When player is late / breaks a ritual
_RITUAL_BROKEN_LINES = {
    # Just slightly late
    "late": [
        "You're late. Not that I noticed.",
        "Running behind today? I barely registered it.",
        "The {hour_ampm} {action} was more of a {actual_ampm} {action} today.",
        "I wasn't waiting. I was just... here. At the usual time.",
    ],
    # Missed entirely yesterday
    "missed": [
        "No {action} yesterday. I survived. Obviously.",
        "We skipped the {action} routine yesterday. Change of plans?",
        "Yesterday came and went without the usual {action}. I adapted. Ducks adapt.",
    ],
    # Multi-day break
    "forgotten": [
        "Remember when you used to {action} me at {hour_ampm}? Me neither. Wait, yes I do.",
        "The {action} schedule has been... flexible lately.",
        "I had a whole routine built around the {hour_ampm} {action}. Had.",
    ],
}

# When player resumes a broken ritual
_RITUAL_RESUMED_LINES = [
    "Oh. We're doing this again. Fine by me. Not that I missed it.",
    "The prodigal {action} returns.",
    "Back to the old routine? I never left.",
    "Welcome back to the {hour_ampm} {action}. Your usual spot is still warm.",
]


def _format_hour_ampm(hour: int) -> str:
    """Format hour as '8am', '2pm', etc."""
    if hour == 0:
        return "12am"
    elif hour < 12:
        return f"{hour}am"
    elif hour == 12:
        return "12pm"
    else:
        return f"{hour - 12}pm"


def _format_time_of_day(hour: int) -> str:
    """Format hour as 'morning', 'afternoon', 'evening', 'night'."""
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "evening"
    else:
        return "night"


def _format_line(template: str, action: str, ritual: Optional[RitualPattern] = None,
                 actual_hour: Optional[int] = None) -> str:
    """Fill in template placeholders."""
    hour_ampm = _format_hour_ampm(ritual.typical_hour) if ritual else ""
    actual_ampm = _format_hour_ampm(actual_hour) if actual_hour is not None else ""
    time_of_day = _format_time_of_day(ritual.typical_hour) if ritual else ""
    streak = ritual.streak if ritual else 0
    
    return template.format(
        action=action,
        Action=action.capitalize(),
        hour_ampm=hour_ampm,
        Hour_ampm=hour_ampm[:1].upper() + hour_ampm[1:] if hour_ampm else "",
        actual_ampm=actual_ampm,
        time_of_day=time_of_day,
        streak=streak,
    )


# ── The tracker ─────────────────────────────────────────────────────────
import random
import statistics


class RitualTracker:
    """
    Detects and tracks player interaction rituals.
    
    Watches for patterns in when the player performs actions, builds
    confidence over time, and provides observations for the duck to
    comment on.
    """

    def __init__(self):
        self.action_history: Dict[str, List[ActionTimestamp]] = {}
        self.detected_rituals: Dict[str, RitualPattern] = {}
        self._last_ritual_check: float = 0.0

    def record_interaction(self, action: str) -> Optional[str]:
        """
        Record an interaction and return a ritual observation if relevant.
        
        Args:
            action: The action type ("feed", "play", "clean", "pet", "sleep")
            
        Returns:
            A deadpan observation string if a ritual was matched/broken, else None
        """
        now = time.time()
        dt = datetime.now()
        
        ts = ActionTimestamp(
            action=action,
            hour=dt.hour,
            minute=dt.minute,
            weekday=dt.weekday(),
            timestamp=now,
        )
        
        # Store in rolling window
        if action not in self.action_history:
            self.action_history[action] = []
        history = self.action_history[action]
        history.append(ts)
        
        # Trim to window size
        if len(history) > HISTORY_WINDOW:
            self.action_history[action] = history[-HISTORY_WINDOW:]
        
        # Re-detect rituals
        self._detect_rituals()
        
        # Check if this matches an existing ritual
        ritual = self.detected_rituals.get(action)
        if ritual is None or not ritual.is_established:
            return None
        
        # Is this within the expected window?
        current_minutes = dt.hour * 60 + dt.minute
        expected_minutes = ritual.typical_hour * 60 + ritual.typical_minute
        diff = abs(current_minutes - expected_minutes)
        # Handle midnight wraparound
        diff = min(diff, 1440 - diff)
        
        in_window = diff <= BROKEN_GRACE_MINUTES
        
        if in_window:
            return self._on_ritual_matched(ritual, now, dt.hour)
        else:
            return self._on_ritual_late(ritual, now, dt.hour)

    def check_missed_rituals(self) -> List[str]:
        """
        Check for rituals that should have happened by now but haven't.
        Call this periodically from the game tick.
        
        Returns:
            List of deadpan observations about broken routines.
        """
        now = time.time()
        
        # Only check every 30 minutes (real time)
        if now - self._last_ritual_check < 1800:
            return []
        self._last_ritual_check = now
        
        dt = datetime.now()
        current_minutes = dt.hour * 60 + dt.minute
        observations = []
        
        for action, ritual in self.detected_rituals.items():
            if not ritual.is_established:
                continue
            
            # Has this ritual's window passed today?
            window_end = ritual.window_end_minutes
            if current_minutes <= window_end:
                continue  # Window hasn't closed yet
            
            # Was it already matched today?
            history = self.action_history.get(action, [])
            today_start = datetime.now().replace(hour=0, minute=0, second=0).timestamp()
            matched_today = any(
                ts.timestamp >= today_start and
                abs((ts.hour * 60 + ts.minute) - (ritual.typical_hour * 60 + ritual.typical_minute)) <= BROKEN_GRACE_MINUTES
                for ts in history
            )
            
            if matched_today:
                continue
            
            # Comment cooldown
            if now - ritual.last_commented < COMMENT_COOLDOWN_HOURS * 3600:
                continue
            
            # Broken!
            ritual.broken_days += 1
            
            if ritual.broken_days == 1:
                tier = "late"
            elif ritual.broken_days <= 3:
                tier = "missed"
            else:
                tier = "forgotten"
            
            lines = _RITUAL_BROKEN_LINES.get(tier, _RITUAL_BROKEN_LINES["late"])
            template = random.choice(lines)
            obs = _format_line(template, action, ritual)
            
            ritual.last_commented = now
            ritual.times_acknowledged += 1
            observations.append(obs)
        
        return observations

    def _on_ritual_matched(self, ritual: RitualPattern, now: float, 
                           actual_hour: int) -> Optional[str]:
        """Handle a ritual being matched on time."""
        was_broken = ritual.broken_days > 0
        ritual.streak += 1
        ritual.broken_days = 0
        ritual.last_matched = now
        
        # Boost confidence
        ritual.confidence = min(MAX_CONFIDENCE, 
                               ritual.confidence + CONFIDENCE_PER_DAY)
        
        # Resuming a broken ritual?
        if was_broken:
            # Comment cooldown still applies
            if now - ritual.last_commented < COMMENT_COOLDOWN_HOURS * 3600:
                return None
            ritual.last_commented = now
            ritual.times_acknowledged += 1
            template = random.choice(_RITUAL_RESUMED_LINES)
            return _format_line(template, ritual.action, ritual)
        
        # Comment cooldown
        if now - ritual.last_commented < COMMENT_COOLDOWN_HOURS * 3600:
            return None
        
        # Determine confidence tier
        if ritual.confidence < 0.5:
            tier = "emerging"
        elif ritual.confidence < 0.8:
            tier = "established"
        else:
            tier = "deep"
        
        lines = _RITUAL_MATCH_LINES[tier]
        template = random.choice(lines)
        obs = _format_line(template, ritual.action, ritual, actual_hour)
        
        ritual.last_commented = now
        ritual.times_acknowledged += 1
        return obs

    def _on_ritual_late(self, ritual: RitualPattern, now: float,
                        actual_hour: int) -> Optional[str]:
        """Handle an action done outside the ritual window."""
        # Comment cooldown
        if now - ritual.last_commented < COMMENT_COOLDOWN_HOURS * 3600:
            return None
        
        # Only comment if confidence is decent — don't nag about emerging patterns
        if ritual.confidence < 0.5:
            return None
        
        ritual.last_commented = now
        ritual.times_acknowledged += 1
        
        lines = _RITUAL_BROKEN_LINES["late"]
        template = random.choice(lines)
        return _format_line(template, ritual.action, ritual, actual_hour)

    def _detect_rituals(self):
        """Analyze action history to detect/update ritual patterns."""
        for action, history in self.action_history.items():
            if len(history) < MIN_ENTRIES_FOR_RITUAL:
                continue
            
            # Only consider recent entries (last 14 days)
            cutoff = time.time() - (14 * 24 * 3600)
            recent = [ts for ts in history if ts.timestamp > cutoff]
            
            if len(recent) < MIN_ENTRIES_FOR_RITUAL:
                # Pattern decayed — remove ritual
                if action in self.detected_rituals:
                    self.detected_rituals[action].confidence *= 0.9
                    if self.detected_rituals[action].confidence < 0.1:
                        del self.detected_rituals[action]
                continue
            
            # Convert to minutes-from-midnight for analysis
            minutes = [ts.hour * 60 + ts.minute for ts in recent]
            
            # Handle midnight wraparound: if actions span midnight,
            # shift everything by 12 hours for analysis
            has_early = any(m < 180 for m in minutes)  # Before 3am
            has_late = any(m > 1260 for m in minutes)   # After 9pm
            shifted = False
            if has_early and has_late:
                minutes = [(m + 720) % 1440 for m in minutes]
                shifted = True
            
            # Calculate median and IQR
            minutes.sort()
            median_min = statistics.median(minutes)
            
            q1 = statistics.median(minutes[:len(minutes) // 2]) if len(minutes) >= 4 else minutes[0]
            q3 = statistics.median(minutes[len(minutes) // 2 + (1 if len(minutes) % 2 else 0):]) if len(minutes) >= 4 else minutes[-1]
            iqr_hours = (q3 - q1) / 60.0
            
            if iqr_hours > IQR_THRESHOLD_HOURS:
                # Too scattered — not a ritual
                if action in self.detected_rituals:
                    self.detected_rituals[action].confidence *= 0.95
                continue
            
            # Unshift if needed
            if shifted:
                median_min = (median_min - 720) % 1440
            
            typical_hour = int(median_min) // 60
            typical_minute = int(median_min) % 60
            
            # Update or create ritual
            if action in self.detected_rituals:
                ritual = self.detected_rituals[action]
                ritual.typical_hour = typical_hour
                ritual.typical_minute = typical_minute
                # Don't reset confidence — it grows via matches
            else:
                self.detected_rituals[action] = RitualPattern(
                    action=action,
                    typical_hour=typical_hour,
                    typical_minute=typical_minute,
                    confidence=CONFIDENCE_PER_DAY * len(recent),
                    streak=0,
                    last_matched=0.0,
                    last_commented=0.0,
                    times_acknowledged=0,
                    broken_days=0,
                )

    def get_ritual_summary(self) -> Dict[str, str]:
        """Get a summary of detected rituals for UI/debug."""
        result = {}
        for action, ritual in self.detected_rituals.items():
            if ritual.is_established:
                hour_str = _format_hour_ampm(ritual.typical_hour)
                result[action] = (
                    f"{hour_str} (confidence: {ritual.confidence:.0%}, "
                    f"streak: {ritual.streak})"
                )
        return result

    def to_dict(self) -> dict:
        """Serialize for persistence."""
        return {
            "action_history": {
                action: [ts.to_dict() for ts in timestamps]
                for action, timestamps in self.action_history.items()
            },
            "detected_rituals": {
                action: ritual.to_dict()
                for action, ritual in self.detected_rituals.items()
            },
            "last_ritual_check": self._last_ritual_check,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "RitualTracker":
        """Deserialize from save data."""
        tracker = cls()
        
        for action, timestamps in data.get("action_history", {}).items():
            tracker.action_history[action] = [
                ActionTimestamp.from_dict(ts) for ts in timestamps
            ]
        
        for action, ritual_data in data.get("detected_rituals", {}).items():
            tracker.detected_rituals[action] = RitualPattern.from_dict(ritual_data)
        
        tracker._last_ritual_check = data.get("last_ritual_check", 0.0)
        return tracker
