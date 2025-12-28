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
    
    # Exploration achievements
    "first_explore": Achievement(
        id="first_explore",
        name="Explorer",
        description="Explored your first area",
        secret_description="",
        category="exploration",
        icon="[E]",
        rarity="common",
    ),
    "discover_5_areas": Achievement(
        id="discover_5_areas",
        name="Adventurer",
        description="Discovered 5 different areas",
        secret_description="",
        category="exploration",
        icon="[E]",
        rarity="uncommon",
    ),
    "discover_10_areas": Achievement(
        id="discover_10_areas",
        name="World Explorer",
        description="Discovered 10 different areas",
        secret_description="",
        category="exploration",
        icon="[E]",
        rarity="rare",
    ),
    "gathering_master": Achievement(
        id="gathering_master",
        name="Gathering Master",
        description="Reached gathering skill level 5",
        secret_description="",
        category="exploration",
        icon="[G]",
        rarity="rare",
    ),
    "rare_find": Achievement(
        id="rare_find",
        name="Rare Find",
        description="Found a rare item while exploring",
        secret_description="",
        category="exploration",
        icon="[R]",
        rarity="uncommon",
    ),
    
    # Crafting achievements
    "first_craft": Achievement(
        id="first_craft",
        name="Crafter",
        description="Crafted your first item",
        secret_description="",
        category="crafting",
        icon="[C]",
        rarity="common",
    ),
    "craft_10": Achievement(
        id="craft_10",
        name="Artisan",
        description="Crafted 10 items",
        secret_description="",
        category="crafting",
        icon="[C]",
        rarity="uncommon",
    ),
    "craft_tool": Achievement(
        id="craft_tool",
        name="Tool Maker",
        description="Crafted your first tool",
        secret_description="",
        category="crafting",
        icon="[T]",
        rarity="uncommon",
    ),
    "crafting_master": Achievement(
        id="crafting_master",
        name="Crafting Master",
        description="Reached crafting skill level 5",
        secret_description="",
        category="crafting",
        icon="[C]",
        rarity="rare",
    ),
    
    # Building achievements
    "first_build": Achievement(
        id="first_build",
        name="Builder",
        description="Built your first structure",
        secret_description="",
        category="building",
        icon="[B]",
        rarity="common",
    ),
    "build_nest": Achievement(
        id="build_nest",
        name="Homemaker",
        description="Built a cozy nest",
        secret_description="",
        category="building",
        icon="[N]",
        rarity="common",
    ),
    "build_house": Achievement(
        id="build_house",
        name="Architect",
        description="Built a proper house",
        secret_description="",
        category="building",
        icon="[H]",
        rarity="rare",
    ),
    "build_5": Achievement(
        id="build_5",
        name="Construction Duck",
        description="Built 5 structures",
        secret_description="",
        category="building",
        icon="[B]",
        rarity="uncommon",
    ),
    "building_master": Achievement(
        id="building_master",
        name="Master Builder",
        description="Reached building skill level 5",
        secret_description="",
        category="building",
        icon="[B]",
        rarity="rare",
    ),

    # ==================== MINIGAME ACHIEVEMENTS ====================
    "first_minigame": Achievement(
        id="first_minigame",
        name="Game On!",
        description="Played your first mini-game",
        secret_description="",
        category="minigame",
        icon="[J]",
        rarity="common",
    ),
    "minigame_fan": Achievement(
        id="minigame_fan",
        name="Game Fan",
        description="Played 10 mini-games",
        secret_description="",
        category="minigame",
        icon="[J]",
        rarity="uncommon",
    ),
    "minigame_master": Achievement(
        id="minigame_master",
        name="Game Master",
        description="Played 50 mini-games",
        secret_description="",
        category="minigame",
        icon="[J]",
        rarity="rare",
    ),
    "high_scorer": Achievement(
        id="high_scorer",
        name="High Scorer",
        description="Set a new high score in any mini-game",
        secret_description="",
        category="minigame",
        icon="[H]",
        rarity="uncommon",
    ),
    "bread_master": Achievement(
        id="bread_master",
        name="Bread Catcher",
        description="Scored 500+ in Bread Catch",
        secret_description="???",
        category="minigame",
        icon="[B]",
        rarity="rare",
        hidden=True,
    ),
    "bug_hunter": Achievement(
        id="bug_hunter",
        name="Bug Hunter",
        description="Scored 1000+ in Bug Chase",
        secret_description="???",
        category="minigame",
        icon="[B]",
        rarity="rare",
        hidden=True,
    ),
    "perfect_memory": Achievement(
        id="perfect_memory",
        name="Perfect Memory",
        description="Won Memory Match in 16 moves or less",
        secret_description="???",
        category="minigame",
        icon="[M]",
        rarity="legendary",
        hidden=True,
    ),
    "speed_demon": Achievement(
        id="speed_demon",
        name="Speed Demon",
        description="Won Duck Race in under 10 seconds",
        secret_description="???",
        category="minigame",
        icon="[R]",
        rarity="legendary",
        hidden=True,
    ),

    # ==================== DREAM ACHIEVEMENTS ====================
    "first_dream": Achievement(
        id="first_dream",
        name="Sweet Dreams",
        description="Had your first dream",
        secret_description="",
        category="dreams",
        icon="[Z]",
        rarity="common",
    ),
    "dreamer": Achievement(
        id="dreamer",
        name="Dreamer",
        description="Had 10 dreams",
        secret_description="",
        category="dreams",
        icon="[Z]",
        rarity="uncommon",
    ),
    "dream_master": Achievement(
        id="dream_master",
        name="Dream Walker",
        description="Had 50 dreams",
        secret_description="",
        category="dreams",
        icon="[Z]",
        rarity="rare",
    ),
    "dream_treasure": Achievement(
        id="dream_treasure",
        name="Dream Treasure",
        description="Found an item in a dream",
        secret_description="???",
        category="dreams",
        icon="[D]",
        rarity="uncommon",
        hidden=True,
    ),
    "dream_collector": Achievement(
        id="dream_collector",
        name="Dream Collector",
        description="Found 5 items in dreams",
        secret_description="???",
        category="dreams",
        icon="[D]",
        rarity="rare",
        hidden=True,
    ),
    "dream_explorer": Achievement(
        id="dream_explorer",
        name="Dream Explorer",
        description="Experienced all types of dreams",
        secret_description="???",
        category="dreams",
        icon="[*]",
        rarity="legendary",
        hidden=True,
    ),

    # ==================== VISITOR ACHIEVEMENTS ====================
    "first_visitor": Achievement(
        id="first_visitor",
        name="Host",
        description="Had your first visitor",
        secret_description="",
        category="visitors",
        icon="[V]",
        rarity="common",
    ),
    "social_butterfly": Achievement(
        id="social_butterfly",
        name="Social Butterfly",
        description="Met 5 different visitors",
        secret_description="",
        category="visitors",
        icon="[V]",
        rarity="uncommon",
    ),
    "popular_duck": Achievement(
        id="popular_duck",
        name="Popular Duck",
        description="Had 20 total visitor visits",
        secret_description="",
        category="visitors",
        icon="[V]",
        rarity="rare",
    ),
    "best_friend_visitor": Achievement(
        id="best_friend_visitor",
        name="Best Friends",
        description="Reached best friend status with a visitor",
        secret_description="???",
        category="visitors",
        icon="[<3]",
        rarity="legendary",
        hidden=True,
    ),
    "met_gerald": Achievement(
        id="met_gerald",
        name="Goose Friend",
        description="Met Gerald the Goose",
        secret_description="???",
        category="visitors",
        icon="[G]",
        rarity="secret",
        hidden=True,
    ),
    "met_professor": Achievement(
        id="met_professor",
        name="Wise Student",
        description="Met Professor Hoot",
        secret_description="???",
        category="visitors",
        icon="[O]",
        rarity="secret",
        hidden=True,
    ),
    "met_all_visitors": Achievement(
        id="met_all_visitors",
        name="Social Legend",
        description="Met all possible visitors",
        secret_description="???",
        category="visitors",
        icon="[*]",
        rarity="legendary",
        hidden=True,
    ),

    # ==================== SEASONAL ACHIEVEMENTS ====================
    "spring_celebration": Achievement(
        id="spring_celebration",
        name="Spring Has Sprung",
        description="Played during a Spring event",
        secret_description="",
        category="seasonal",
        icon="[S]",
        rarity="uncommon",
    ),
    "summer_fun": Achievement(
        id="summer_fun",
        name="Summer Vibes",
        description="Played during a Summer event",
        secret_description="",
        category="seasonal",
        icon="[S]",
        rarity="uncommon",
    ),
    "fall_harvest": Achievement(
        id="fall_harvest",
        name="Harvest Time",
        description="Played during a Fall event",
        secret_description="",
        category="seasonal",
        icon="[S]",
        rarity="uncommon",
    ),
    "winter_wonderland": Achievement(
        id="winter_wonderland",
        name="Winter Wonderland",
        description="Played during a Winter event",
        secret_description="",
        category="seasonal",
        icon="[S]",
        rarity="uncommon",
    ),
    "all_seasons": Achievement(
        id="all_seasons",
        name="Season Master",
        description="Experienced all four seasons",
        secret_description="",
        category="seasonal",
        icon="[*]",
        rarity="rare",
    ),

    # ==================== BIRTHDAY/MILESTONE ACHIEVEMENTS ====================
    "happy_birthday": Achievement(
        id="happy_birthday",
        name="Happy Hatch Day!",
        description="Celebrated your duck's birthday",
        secret_description="",
        category="milestone",
        icon="[B]",
        rarity="rare",
    ),
    "week_together": Achievement(
        id="week_together",
        name="One Week Friend",
        description="Been together for one week",
        secret_description="",
        category="milestone",
        icon="[7]",
        rarity="common",
    ),
    "month_together": Achievement(
        id="month_together",
        name="Monthly Bond",
        description="Been together for one month",
        secret_description="",
        category="milestone",
        icon="[30]",
        rarity="uncommon",
    ),
    "century_of_love": Achievement(
        id="century_of_love",
        name="Century of Love",
        description="Been together for 100 days",
        secret_description="",
        category="milestone",
        icon="[100]",
        rarity="rare",
    ),
    "year_together": Achievement(
        id="year_together",
        name="Forever Friends",
        description="Been together for one whole year!",
        secret_description="",
        category="milestone",
        icon="[365]",
        rarity="legendary",
    ),

    # ==================== DUCK FACTS ACHIEVEMENTS ====================
    "duck_scholar": Achievement(
        id="duck_scholar",
        name="Duck Scholar",
        description="Learned 10 duck facts",
        secret_description="",
        category="knowledge",
        icon="[F]",
        rarity="uncommon",
    ),
    "duck_professor": Achievement(
        id="duck_professor",
        name="Duck Professor",
        description="Learned 50 duck facts",
        secret_description="",
        category="knowledge",
        icon="[F]",
        rarity="rare",
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
