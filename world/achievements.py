"""
Achievements system - hidden and visible achievements to unlock.
"""
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Achievement:
    """An achievement that can be unlocked."""
    id: str
    name: str
    description: str
    secret_description: str  # Shown before unlock for secret achievements
    category: str  # interaction, growth, time, secret, legendary
    icon: str
    rarity: str  # common, uncommon, rare, legendary, secret
    hidden: bool = False


# All achievements
ACHIEVEMENTS = {
    # Interaction achievements
    "first_feed": Achievement(
        id="first_feed",
        name="First Meal",
        description="Fed your duck for the first time",
        secret_description="",
        category="interaction",
        icon="[F]",
        rarity="common",
    ),
    "10_feeds": Achievement(
        id="10_feeds",
        name="Feeder I",
        description="Fed your duck 10 times",
        secret_description="",
        category="interaction",
        icon="[F]",
        rarity="common",
    ),
    "50_feeds": Achievement(
        id="50_feeds",
        name="Feeder II",
        description="Fed your duck 50 times",
        secret_description="",
        category="interaction",
        icon="[F]",
        rarity="uncommon",
    ),
    "100_feeds": Achievement(
        id="100_feeds",
        name="Master Feeder",
        description="Fed your duck 100 times",
        secret_description="",
        category="interaction",
        icon="[F]",
        rarity="rare",
    ),
    "10_plays": Achievement(
        id="10_plays",
        name="Playmate I",
        description="Played with your duck 10 times",
        secret_description="",
        category="interaction",
        icon="[P]",
        rarity="common",
    ),
    "50_plays": Achievement(
        id="50_plays",
        name="Playmate II",
        description="Played with your duck 50 times",
        secret_description="",
        category="interaction",
        icon="[P]",
        rarity="uncommon",
    ),
    "100_plays": Achievement(
        id="100_plays",
        name="Best Playmate",
        description="Played with your duck 100 times",
        secret_description="",
        category="interaction",
        icon="[P]",
        rarity="rare",
    ),
    "10_pets": Achievement(
        id="10_pets",
        name="Affectionate I",
        description="Petted your duck 10 times",
        secret_description="",
        category="interaction",
        icon="[E]",
        rarity="common",
    ),
    "50_pets": Achievement(
        id="50_pets",
        name="Affectionate II",
        description="Petted your duck 50 times",
        secret_description="",
        category="interaction",
        icon="[E]",
        rarity="uncommon",
    ),
    "100_pets": Achievement(
        id="100_pets",
        name="Cuddle Expert",
        description="Petted your duck 100 times",
        secret_description="",
        category="interaction",
        icon="[E]",
        rarity="rare",
    ),

    # Growth achievements
    "reach_duckling": Achievement(
        id="reach_duckling",
        name="Born!",
        description="Your duck hatched from an egg",
        secret_description="",
        category="growth",
        icon="[D]",
        rarity="common",
    ),
    "reach_teen": Achievement(
        id="reach_teen",
        name="Growing Up",
        description="Your duck became a teenager",
        secret_description="",
        category="growth",
        icon="[T]",
        rarity="uncommon",
    ),
    "reach_adult": Achievement(
        id="reach_adult",
        name="All Grown Up",
        description="Your duck became an adult",
        secret_description="",
        category="growth",
        icon="[A]",
        rarity="rare",
    ),
    "reach_elder": Achievement(
        id="reach_elder",
        name="Wise One",
        description="Your duck became an elder",
        secret_description="",
        category="growth",
        icon="[E]",
        rarity="legendary",
    ),

    # Mood achievements
    "first_ecstatic": Achievement(
        id="first_ecstatic",
        name="Pure Joy",
        description="Made your duck ecstatic for the first time",
        secret_description="",
        category="mood",
        icon="[!]",
        rarity="uncommon",
    ),
    "keep_happy_day": Achievement(
        id="keep_happy_day",
        name="Good Day",
        description="Kept your duck happy for a full day",
        secret_description="",
        category="mood",
        icon="[^]",
        rarity="rare",
    ),

    # Relationship achievements
    "best_friends": Achievement(
        id="best_friends",
        name="Best Friends Forever",
        description="Reached 'bonded' relationship with your duck",
        secret_description="",
        category="relationship",
        icon="[<3]",
        rarity="legendary",
    ),

    # Time achievements
    "week_played": Achievement(
        id="week_played",
        name="Dedicated",
        description="Played for a week",
        secret_description="",
        category="time",
        icon="[7]",
        rarity="uncommon",
    ),
    "month_played": Achievement(
        id="month_played",
        name="Committed",
        description="Played for a month",
        secret_description="",
        category="time",
        icon="[30]",
        rarity="rare",
    ),

    # Secret achievements
    "midnight_duck": Achievement(
        id="midnight_duck",
        name="Night Owl",
        description="Played with your duck at midnight",
        secret_description="???",
        category="secret",
        icon="[?]",
        rarity="secret",
        hidden=True,
    ),
    "early_bird": Achievement(
        id="early_bird",
        name="Early Bird",
        description="Played with your duck at 5 AM",
        secret_description="???",
        category="secret",
        icon="[?]",
        rarity="secret",
        hidden=True,
    ),
    "derp_master": Achievement(
        id="derp_master",
        name="Derp Master",
        description="Witnessed your duck trip over nothing 10 times",
        secret_description="???",
        category="secret",
        icon="[?]",
        rarity="secret",
        hidden=True,
    ),
    "golden_discovery": Achievement(
        id="golden_discovery",
        name="Legendary Find",
        description="Found the Golden Crumb",
        secret_description="???",
        category="secret",
        icon="[G]",
        rarity="legendary",
        hidden=True,
    ),
    "patient_one": Achievement(
        id="patient_one",
        name="The Patient One",
        description="Waited 5 minutes without doing anything",
        secret_description="???",
        category="secret",
        icon="[.]",
        rarity="secret",
        hidden=True,
    ),
    "quack_master": Achievement(
        id="quack_master",
        name="Quack Master",
        description="Heard your duck quack 50 times",
        secret_description="???",
        category="secret",
        icon="[Q]",
        rarity="secret",
        hidden=True,
    ),
    "holiday_spirit": Achievement(
        id="holiday_spirit",
        name="Holiday Spirit",
        description="Played during a special holiday event",
        secret_description="???",
        category="secret",
        icon="[*]",
        rarity="secret",
        hidden=True,
    ),
}


class AchievementSystem:
    """Manages player achievements."""

    def __init__(self):
        self._unlocked: Set[str] = set()
        self._unlock_times: Dict[str, str] = {}
        self._progress: Dict[str, int] = {}  # For progress-based achievements
        self._pending_notifications: List[Achievement] = []

    def unlock(self, achievement_id: str) -> Optional[Achievement]:
        """
        Unlock an achievement.

        Returns the achievement if newly unlocked, None if already unlocked.
        """
        if achievement_id in self._unlocked:
            return None

        achievement = ACHIEVEMENTS.get(achievement_id)
        if not achievement:
            return None

        self._unlocked.add(achievement_id)
        self._unlock_times[achievement_id] = datetime.now().isoformat()
        self._pending_notifications.append(achievement)

        return achievement

    def is_unlocked(self, achievement_id: str) -> bool:
        """Check if an achievement is unlocked."""
        return achievement_id in self._unlocked

    def get_unlocked(self) -> List[Achievement]:
        """Get all unlocked achievements."""
        return [ACHIEVEMENTS[aid] for aid in self._unlocked if aid in ACHIEVEMENTS]

    def get_locked(self) -> List[Achievement]:
        """Get all locked achievements (non-hidden ones)."""
        locked = []
        for aid, ach in ACHIEVEMENTS.items():
            if aid not in self._unlocked and not ach.hidden:
                locked.append(ach)
        return locked

    def get_unlocked_count(self) -> int:
        """Get number of unlocked achievements."""
        return len(self._unlocked)

    def get_total_count(self) -> int:
        """Get total number of achievements (excluding hidden)."""
        return len([a for a in ACHIEVEMENTS.values() if not a.hidden])

    def get_pending_notifications(self) -> List[Achievement]:
        """Get and clear pending achievement notifications."""
        pending = self._pending_notifications.copy()
        self._pending_notifications.clear()
        return pending

    def increment_progress(self, achievement_id: str, amount: int = 1) -> Optional[Achievement]:
        """
        Increment progress on a progress-based achievement.

        Returns the achievement if it triggers unlock.
        """
        self._progress[achievement_id] = self._progress.get(achievement_id, 0) + amount
        return None  # Would need targets defined to auto-unlock

    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "unlocked": list(self._unlocked),
            "unlock_times": self._unlock_times,
            "progress": self._progress,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AchievementSystem":
        """Create from dictionary."""
        system = cls()
        system._unlocked = set(data.get("unlocked", []))
        system._unlock_times = data.get("unlock_times", {})
        system._progress = data.get("progress", {})
        return system


# Global instance
achievement_system = AchievementSystem()
