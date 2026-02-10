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
        "Interesting. Same time again.",
        "Is this going to be a thing. The {time_of_day} {action}.",
        "Two could be a coincidence. This is starting to not be that.",
        "Oh look. {Action}. At this hour. What are the odds.",
        "I'm noticing a {time_of_day} trend here. Just so you know.",
        "You and {time_of_day}s. There's something there.",
        "Are we doing this every {time_of_day} now. Because I can prepare.",
        "Another {time_of_day} {action}. *files that away*",
        "Hm. {Action} again. Around now. Noted.",
        "If I didn't know better I'd say you had a schedule.",
        "This {time_of_day} {action} thing is becoming suspiciously regular.",
    ],
    # Medium confidence (established)
    "established": [
        "Right on schedule.",
        "{Hour_ampm}. {Action} time. I know the drill.",
        "There it is. The {hour_ampm} {action}. Reliable.",
        "You're consistent. I'll give you that.",
        "Ah. The {hour_ampm} {action}. We meet again.",
        "Called it. {Action}. Right now.",
        "Some ducks get fed randomly. I get a SCHEDULE.",
        "Every {time_of_day}. Like the tide. But with more {action}ing.",
        "I could set a sundial by you. If I had a sundial. Or thumbs.",
        "You know what. The predictability is growing on me. *slightly*",
        "The {hour_ampm} {action}. My body knew before my brain did.",
        "There's that {time_of_day} {action} energy. I felt it coming.",
        "{Action} o'clock. Population: me.",
        "Day {streak} of the {hour_ampm} {action}. This is our life now.",
        "You again. At {hour_ampm}. With the {action}. Shocker.",
    ],
    # High confidence (deeply routine)
    "deep": [
        "I had this penciled in.",
        "{Action} at {hour_ampm}. Day {streak}. Not that I'm counting.",
        "If I had a watch, I wouldn't need one. I've got you.",
        "My internal clock is just you, at this point.",
        "{Hour_ampm}. Like clockwork. I'd set my feathers by it.",
        "Day {streak}. Same time. Same {action}. same duck. This is fine.",
        "We've been doing this so long I think it's legally a tradition.",
        "The {hour_ampm} {action}. Older than some civilizations. Probably.",
        "I don't even get excited anymore. It's just... part of me now.",
        "{Action}. {Hour_ampm}. Day {streak}. The universe is in order.",
        "Some things are constant. Gravity. Entropy. The {hour_ampm} {action}.",
        "I knew you were coming before you did. That's not creepy. that's DEVOTION.",
        "My feathers pre-adjusted. That's how deep this goes.",
        "{Hour_ampm}. *already in position*",
        "We don't even need words at this point. {Action}. Go.",
        "The {hour_ampm} {action}. I'd write it in stone but I don't have a chisel.",
        "Day {streak}. This ritual has outlasted some of my feathers.",
        "At this point the {action} is load-bearing. Don't test that.",
        "They say ducks don't understand time. They haven't met me at {hour_ampm}.",
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
        "Oh. There you are. I was NOT staring at where you usually appear.",
        "Bold of you to reschedule without consulting me.",
        "The schedule said {hour_ampm}. You said {actual_ampm}. We'll discuss this later.",
        "Fashionably late. Emphasis on late.",
        "I had already mentally moved on. *hadn't moved on*",
        "You know the {action} window. You chose to ignore it. That's fine. FINE.",
        "I reorganized my entire afternoon. Because of you. Not that you'd know.",
        "The {hour_ampm} {action} sends its regards from {actual_ampm}.",
    ],
    # Missed entirely yesterday
    "missed": [
        "No {action} yesterday. I survived. Obviously.",
        "We skipped the {action} routine yesterday. Change of plans?",
        "Yesterday came and went without the usual {action}. I adapted. Ducks adapt.",
        "So yesterday. The {action}. We're just not talking about it?",
        "I waited at {hour_ampm} yesterday. Just kidding. I DIDN'T.",
        "The {hour_ampm} slot was empty yesterday. I filled it with dignity.",
        "Yesterday's missing {action} has been noted in the record. My record. The one I keep.",
        "One day without the {action}. I barely noticed. I mean I noticed. But barely.",
        "Funny thing about yesterday. Actually no. It wasn't funny.",
        "The streak was nice while it lasted. That's all I'll say about yesterday.",
    ],
    # Multi-day break
    "forgotten": [
        "Remember when you used to {action} me at {hour_ampm}? Me neither. Wait, yes I do.",
        "The {action} schedule has been... flexible lately.",
        "I had a whole routine built around the {hour_ampm} {action}. Had.",
        "I've stopped expecting the {hour_ampm} {action}. Self-preservation.",
        "The {action} routine walked out and didn't leave a note.",
        "*stares at the spot where the routine used to be*",
        "I've rearranged my whole day. Since the {action} apparently isn't in it anymore.",
        "Some ducks have routines. I have memories of routines. It's different.",
        "The {hour_ampm} {action}. A thing that happened once. For a while. Then didn't.",
        "I'm not bitter about the {action} schedule. I'm a duck. Ducks don't do bitter.",
    ],
}

# When player resumes a broken ritual
_RITUAL_RESUMED_LINES = [
    "Oh. We're doing this again. Fine by me. Not that I missed it.",
    "The prodigal {action} returns.",
    "Back to the old routine? I never left.",
    "Welcome back to the {hour_ampm} {action}. Your usual spot is still warm.",
    "Look who remembered. *was absolutely not waiting*",
    "The {action}. It's back. I'm not emotional about it. these are REGULAR tears.",
    "Act natural. Act like the {action} never left. *acts natural*",
    "Oh the {hour_ampm} {action} is back on the menu? Just like that?",
    "You. {Action}. {Hour_ampm}. Like nothing happened. Bold.",
    "I didn't keep the {action} slot open for you. It just... stayed open. On its own.",
    "The routine resumes. I'm not relieved. I'm INDIFFERENT. Different thing.",
    "Interesting. The {hour_ampm} {action}. Returning from its sabbatical.",
]

# When a specific action ritual is observed — keyed by action type
_RITUAL_ACTION_SPECIFIC = {
    "feed": [
        "The bread arrives on schedule. This is the most important schedule.",
        "Feeding time. My SACRED hour. You know what you're doing.",
        "{Hour_ampm} bread. The cornerstone of my entire existence.",
        "The {hour_ampm} feeding. Without this nothing else matters and I mean that.",
        "You bring bread. I am here. The ancient pact holds.",
        "Bread at {hour_ampm}. Some things are too important to be casual about.",
        "The feeding ritual. The one that actually keeps me alive. No pressure.",
    ],
    "play": [
        "Ah. Scheduled fun. The best kind of fun.",
        "Play time at {hour_ampm}. Penciled in. In ink. On my soul.",
        "The {hour_ampm} play session. I've been conserving energy for this.",
        "Time to pretend I'm not excited. *is clearly excited*",
        "The play hour. Where I tolerate being entertained.",
        "Recreation at {hour_ampm}. I've been standing here. Recreationally.",
    ],
    "clean": [
        "Grooming hour. I was already pristine but go ahead.",
        "The {hour_ampm} clean. Making the immaculate slightly more immaculate.",
        "Right on time with the cleaning. My feathers were counting on you.",
        "Clean at {hour_ampm}. Not that I was dirty. Ducks are never dirty.",
        "The grooming schedule. The one thing between me and chaos.",
        "Ah. Maintenance hour. Please proceed. I'll supervise.",
    ],
    "pet": [
        "The {hour_ampm} pet. I allow it. On schedule.",
        "Affection hour. I tolerate this one. Specifically this one.",
        "Right on time with the pets. I had my feathers pre-fluffed.",
        "The petting schedule holds. My dignity takes its scheduled hit.",
        "Touching the duck. At the appointed time. As is tradition.",
        "*allows the {hour_ampm} pet* This means nothing.",
        "Pet time. I have arranged my face into an expression of indifference.",
    ],
    "sleep": [
        "Bedtime. Right on cue. My eyelids were already heavy. Strategically.",
        "The {hour_ampm} sleep. You tuck, I tolerate. The system works.",
        "Ah. Sleep o'clock. My favorite appointment.",
        "lights out at {hour_ampm}. I was already half asleep. Probably.",
        "The sleep ritual. Where you pretend I need help sleeping.",
        "Bedtime at {hour_ampm}. I'll allow it. *already yawning*",
    ],
}

# Milestone observations for streak achievements
_RITUAL_MILESTONE_LINES = {
    7: [
        "One week of the {hour_ampm} {action}. I'd bake a cake but. You know. Duck.",
        "Seven days straight. The {action} has graduated from habit to lifestyle.",
        "A full week. The {hour_ampm} {action} can now legally call itself a routine.",
    ],
    14: [
        "Two weeks of {action} at {hour_ampm}. This is longer than most of my relationships. With bread.",
        "Fourteen days. The {action} routine has entered its awkward teen phase.",
        "Two weeks. At this point the {hour_ampm} {action} has its own chair here.",
        "Half a month. The {action} schedule is no longer a phase.",
    ],
    30: [
        "One month. Thirty days of the {hour_ampm} {action}. I don't know what to say. so I'll say nothing.",
        "A whole month of this. The {action} routine is now older than some cheeses. Speaking of which.",
        "Thirty days. The {hour_ampm} {action} is now a INSTITUTION.",
        "Month one of the {action} era. I've stopped imagining life without it.",
    ],
    100: [
        "One hundred days. The {hour_ampm} {action}. I'm not crying. Ducks don't cry. This is pond water.",
        "Day 100. The {action} streak has outlived empires. Small empires. But still.",
        "Triple digits. The {hour_ampm} {action} is now basically a law of nature.",
        "A hundred days of this. We should get a plaque. I'd settle for bread.",
    ],
    365: [
        "One year. Three hundred and sixty-five days of {action} at {hour_ampm}. I have nothing to add. *has everything to add*",
        "A full orbit around the sun. And every single day. The {action}. I need a moment.",
        "365 days. The {hour_ampm} {action} is now older than most things I care about. Which is two things.",
        "One year. I am... not going to say what I am. But I am it. About the {action}.",
    ],
}


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
