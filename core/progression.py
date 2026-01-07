"""
Progression and addiction systems - The Sims/Animal Crossing style engagement mechanics.
Implements: XP, levels, streaks, daily rewards, collectibles, milestones, FOMO events.
Enhanced with psychological engagement patterns from Tamagotchi/Animal Crossing research.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import random
import math


# =============================================================================
# STREAK MULTIPLIER SYSTEM
# =============================================================================

# XP multiplier based on current streak
STREAK_XP_MULTIPLIERS = {
    1: 1.0,     # Day 1: Normal XP
    3: 1.1,     # 3+ days: 10% bonus
    7: 1.25,    # Week+: 25% bonus
    14: 1.5,    # 2 weeks+: 50% bonus
    30: 2.0,    # Month+: Double XP!
    60: 2.5,    # 2 months+: 2.5x
    100: 3.0,   # 100+ days: Triple XP!
}

# Streak loss messages (emotional engagement)
STREAK_LOSS_MESSAGES = [
    "Oh no! Cheese missed you... Your {n}-day streak ended. :(",
    "Cheese waited all day yesterday... The {n}-day streak is broken.",
    "The {n}-day streak has ended, but Cheese is happy you're back!",
    "Your {n}-day streak ended... but every journey starts fresh!",
    "Cheese: 'I counted {n} days... where did you go?' :(",
]

# Streak recovery bonuses (incentive to return after losing streak)
STREAK_RECOVERY_DAYS = 3  # Days to earn a "recovery bonus"

# Messages for streak milestones (celebratory)
STREAK_CELEBRATION_MESSAGES = {
    3: "3 days! Cheese is starting to recognize you! *",
    7: "* ONE WEEK STREAK! Cheese does a happy dance! d*",
    14: "* TWO WEEKS! You and Cheese are becoming best friends!",
    21: "~ THREE WEEKS! Cheese gave you a special feather!",
    30: "* ONE MONTH! WOW! Cheese is SO HAPPY! d<3 DOUBLE XP UNLOCKED!",
    50: "* FIFTY DAYS! Cheese made you a tiny crown! ^",
    100: "[#] ONE HUNDRED DAYS! LEGENDARY! Cheese will remember this forever! *",
    365: "* ONE YEAR WITH CHEESE! Eternal bond formed! d<3",
}


# =============================================================================
# SURPRISE REWARDS SYSTEM (Variable ratio reinforcement)
# =============================================================================

# Random gift announcements (builds excitement)
SURPRISE_GIFT_MESSAGES = [
    "* Cheese found something for you! *",
    "[+] Look what Cheese discovered! [+]",
    "* A lucky find! *",
    "* Something special appeared! *",
    "* Cheese wants to share this with you! *",
]

# Lucky events that can trigger randomly
LUCKY_EVENTS = [
    {"name": "Lucky Crumb", "chance": 0.05, "reward_type": "xp", "value": "15", "message": "Found a lucky crumb! +15 XP"},
    {"name": "Shiny Discovery", "chance": 0.03, "reward_type": "xp", "value": "25", "message": "Cheese found something shiny! +25 XP"},
    {"name": "Secret Stash", "chance": 0.01, "reward_type": "item", "value": "bread", "message": "A secret bread stash! B"},
    {"name": "Hidden Treasure", "chance": 0.005, "reward_type": "item", "value": "fancy_bread", "message": "Hidden treasure! Fancy bread! o"},
    {"name": "Magic Moment", "chance": 0.002, "reward_type": "collectible", "value": "treasures:crystal_shard", "message": "* A magical crystal appeared! *"},
]

# Time-based bonus multipliers (engagement hooks)
TIME_BONUSES = {
    "morning": {"hours": (6, 9), "xp_mult": 1.2, "message": "-*- Early bird bonus! +20% XP"},
    "lunch": {"hours": (12, 13), "xp_mult": 1.15, "message": "* Lunch break bonus! +15% XP"},
    "evening": {"hours": (18, 21), "xp_mult": 1.25, "message": "-*- Evening chill bonus! +25% XP"},
    "night_owl": {"hours": (23, 24), "xp_mult": 1.3, "message": "O Night owl bonus! +30% XP"},
    "midnight": {"hours": (0, 2), "xp_mult": 1.5, "message": ") Midnight dedication! +50% XP"},
}

# =============================================================================
# TIME-BASED GREETINGS (Daily rituals)
# =============================================================================

TIME_GREETINGS = {
    "early_morning": {
        "hours": (5, 7),
        "greetings": [
            "-*- *yawns* Oh! You're up early! Cheese is still sleepy...",
            "* The early bird gets the worm... but ducks get bread!",
            "* *stretches wings* Good morning, friend! Let's make today great!",
        ]
    },
    "morning": {
        "hours": (7, 12),
        "greetings": [
            "* Good morning! Cheese is ready for adventure!",
            "* *happy quack* A new day! What will we do today?",
            "B Morning! Is it breakfast time? It's always breakfast time!",
        ]
    },
    "afternoon": {
        "hours": (12, 17),
        "greetings": [
            "* Good afternoon! Perfect time for a snack!",
            "*️ *waddles over* Hey! I was just thinking about you!",
            "o The day is going great! How about you?",
        ]
    },
    "evening": {
        "hours": (17, 21),
        "greetings": [
            "-*- Good evening! Time to wind down together.",
            "-*- *content sigh* Nothing like a relaxing evening with a friend.",
            "* The sunset is beautiful... almost as beautiful as bread!",
        ]
    },
    "night": {
        "hours": (21, 24),
        "greetings": [
            ") *sleepy quack* It's getting late... but I'm glad you're here.",
            "* The stars are out! Make a wish for more crumbs!",
            "* A night owl, huh? Cheese approves.",
        ]
    },
    "late_night": {
        "hours": (0, 5),
        "greetings": [
            ") *whispers* It's very late... but Cheese is always here for you.",
            "z Couldn't sleep? Me neither. Let's hang out.",
            "* The world is quiet, but our friendship is loud! ...that sounded cooler in my head.",
        ]
    },
}

# =============================================================================
# COMFORT MESSAGES (Reduce anxiety, encourage return)
# =============================================================================

COMFORT_MESSAGES = {
    "time_away_short": [  # 1-3 days away
        "You were gone! But Cheese is just happy you're back! <3",
        "I missed you! But I found some good crumbs while you were away.",
        "Welcome back, friend! Everything is better now!",
    ],
    "time_away_medium": [  # 4-7 days away
        "It's been a while! Cheese thought about you every day. :(",
        "You came back! I knew you would! *happy waddle*",
        "Life was quiet without you... but now it's good again! <3",
    ],
    "time_away_long": [  # 8+ days away
        "You're back!! Cheese never gave up hope! <3<3<3",
        "*runs over* I MISSED YOU SO MUCH! Don't worry, I was okay!",
        "No matter how long you're gone, Cheese will always be here waiting. d<3",
    ],
    "encouragement": [
        "You're doing great! Cheese is proud of you! *",
        "Every moment with you is special! *",
        "Just being here makes Cheese happy! <3",
        "You're Cheese's favorite human! ...Don't tell the others.",
        "Thanks for taking care of me! You're the best! d",
    ],
    "gentle_reminder": [
        "Cheese will always be here when you need a break! ~",
        "Take your time! No rush! Cheese is very patient. <3",
        "Remember: there's no wrong way to be a duck friend!",
    ],
}

# =============================================================================
# AMBIENT EVENTS (Peaceful background happenings)
# =============================================================================

AMBIENT_EVENTS = [
    "*A gentle breeze ruffles Cheese's feathers*",
    "*Sunlight sparkles on the pond*",
    "*A butterfly floats by peacefully*",
    "*Cheese finds a comfy spot and settles in*",
    "*The world feels calm and safe*",
    "*Birds sing softly in the distance*",
    "*A leaf drifts down gently*",
    "*Cheese takes a deep, contented breath*",
]


class RewardType(Enum):
    """Types of rewards players can earn."""
    ITEM = "item"
    XP = "xp"
    CURRENCY = "currency"
    COLLECTIBLE = "collectible"
    COSMETIC = "cosmetic"
    TITLE = "title"
    UNLOCK = "unlock"


@dataclass
class Reward:
    """A reward that can be earned."""
    reward_type: RewardType
    value: str  # item_id, amount, or unlock_id
    amount: int = 1
    description: str = ""
    rare: bool = False


@dataclass
class DailyChallenge:
    """A daily challenge/task."""
    id: str
    name: str
    description: str
    target: int
    progress: int = 0
    reward: Optional[Reward] = None
    expires: Optional[str] = None  # ISO datetime


# XP required per level (exponential curve)
def xp_for_level(level: int) -> int:
    """Calculate XP needed to reach a level.
    
    Level 1 requires 0 XP (starting level).
    Higher levels use exponential curve.
    """
    if level <= 1:
        return 0
    return int(100 * (level ** 1.5))


# Level titles/ranks
LEVEL_TITLES = {
    1: "Duckling Watcher",
    5: "Duck Friend",
    10: "Duck Buddy",
    15: "Duck Companion",
    20: "Duck Guardian",
    25: "Duck Whisperer",
    30: "Duck Master",
    40: "Duck Sage",
    50: "Legendary Duck Keeper",
    75: "Eternal Duck Bond",
    100: "One With The Duck",
}


# Collectible categories
COLLECTIBLES = {
    "feathers": {
        "name": "Feather Collection",
        "description": "Rare feathers shed by Cheese",
        "items": {
            "white_feather": {"name": "White Feather", "rarity": "common", "description": "A soft white feather"},
            "golden_feather": {"name": "Golden Feather", "rarity": "legendary", "description": "Shimmers with mysterious light"},
            "rainbow_feather": {"name": "Rainbow Feather", "rarity": "legendary", "description": "Changes color in the light"},
            "fluffy_down": {"name": "Fluffy Down", "rarity": "common", "description": "Extra soft and warm"},
            "spotted_feather": {"name": "Spotted Feather", "rarity": "uncommon", "description": "Unique spotted pattern"},
            "iridescent_feather": {"name": "Iridescent Feather", "rarity": "rare", "description": "Gleams with oil-slick colors"},
            "ancient_feather": {"name": "Ancient Feather", "rarity": "legendary", "description": "From the First Duck..."},
        }
    },
    "badges": {
        "name": "Badge Collection",
        "description": "Achievements and honors",
        "items": {
            "first_friend": {"name": "First Friend Badge", "rarity": "common", "description": "Made a friend!"},
            "best_buddy": {"name": "Best Buddy Badge", "rarity": "rare", "description": "Reached max friendship"},
            "bread_master": {"name": "Bread Master Badge", "rarity": "uncommon", "description": "Fed 100 pieces of bread"},
            "early_bird": {"name": "Early Bird Badge", "rarity": "uncommon", "description": "Played at dawn"},
            "night_owl": {"name": "Night Owl Badge", "rarity": "uncommon", "description": "Played at midnight"},
            "dedication": {"name": "Dedication Badge", "rarity": "rare", "description": "30 day streak"},
            "legendary_keeper": {"name": "Legendary Keeper", "rarity": "legendary", "description": "100% completion"},
        }
    },
    "photos": {
        "name": "Photo Album",
        "description": "Memorable moments captured",
        "items": {
            "first_meeting": {"name": "First Meeting", "rarity": "common", "description": "The day we met"},
            "first_bath": {"name": "Splish Splash", "rarity": "common", "description": "First bath time"},
            "sleeping_duck": {"name": "Sleepy Time", "rarity": "common", "description": "Peaceful napping"},
            "happy_dance": {"name": "Happy Dance", "rarity": "uncommon", "description": "Pure joy captured"},
            "holiday_photo": {"name": "Holiday Memory", "rarity": "rare", "description": "Special holiday moment"},
            "evolution": {"name": "Growing Up", "rarity": "rare", "description": "Growth milestone"},
            "best_friends": {"name": "Best Friends Forever", "rarity": "legendary", "description": "Maximum bond achieved"},
        }
    },
    "treasures": {
        "name": "Duck Treasures",
        "description": "Shiny things Cheese found",
        "items": {
            "shiny_coin": {"name": "Shiny Coin", "rarity": "common", "description": "Ooh, shiny!"},
            "pretty_rock": {"name": "Pretty Rock", "rarity": "common", "description": "It's a really nice rock"},
            "lost_button": {"name": "Lost Button", "rarity": "common", "description": "Someone's missing this"},
            "glass_marble": {"name": "Glass Marble", "rarity": "uncommon", "description": "Swirly colors inside"},
            "old_key": {"name": "Mysterious Key", "rarity": "rare", "description": "What does it unlock?"},
            "crystal_shard": {"name": "Crystal Shard", "rarity": "rare", "description": "Sparkles in sunlight"},
            "ancient_artifact": {"name": "Ancient Artifact", "rarity": "legendary", "description": "From a forgotten time"},
        }
    }
}


# Milestone rewards
MILESTONES = {
    "interactions": [
        (10, Reward(RewardType.XP, "50", description="First 10 interactions!")),
        (50, Reward(RewardType.ITEM, "fancy_bread", description="50 interactions!")),
        (100, Reward(RewardType.COLLECTIBLE, "badges:first_friend", description="100 interactions!")),
        (500, Reward(RewardType.COLLECTIBLE, "badges:dedication", description="500 interactions!")),
        (1000, Reward(RewardType.TITLE, "Dedicated Keeper", description="1000 interactions!")),
    ],
    "days_played": [
        (1, Reward(RewardType.XP, "25", description="First day!")),
        (7, Reward(RewardType.ITEM, "rubber_duck", description="One week!")),
        (30, Reward(RewardType.COLLECTIBLE, "badges:dedication", description="One month!")),
        (100, Reward(RewardType.TITLE, "Centurion", description="100 days!")),
        (365, Reward(RewardType.COLLECTIBLE, "badges:legendary_keeper", description="One year!")),
    ],
    "streak": [
        (3, Reward(RewardType.XP, "30", description="3 day streak!")),
        (7, Reward(RewardType.ITEM, "seeds", 3, description="Week streak!")),
        (14, Reward(RewardType.COLLECTIBLE, "feathers:spotted_feather", description="2 week streak!")),
        (30, Reward(RewardType.COLLECTIBLE, "badges:dedication", description="Month streak!")),
        (100, Reward(RewardType.COLLECTIBLE, "feathers:golden_feather", description="100 day streak!")),
    ],
    "relationship": [
        (20, Reward(RewardType.COLLECTIBLE, "photos:first_meeting", description="Acquaintance!")),
        (40, Reward(RewardType.TITLE, "Duck Friend", description="Friends!")),
        (60, Reward(RewardType.COLLECTIBLE, "photos:happy_dance", description="Good Friends!")),
        (80, Reward(RewardType.ITEM, "duck_photo", description="Best Friends!")),
        (100, Reward(RewardType.COLLECTIBLE, "photos:best_friends", description="Bonded Forever!")),
    ],
}


# Daily reward tiers (based on streak)
DAILY_REWARDS = [
    # Day 1
    [Reward(RewardType.ITEM, "bread", 2), Reward(RewardType.XP, "10")],
    # Day 2
    [Reward(RewardType.ITEM, "seeds", 2), Reward(RewardType.XP, "15")],
    # Day 3
    [Reward(RewardType.ITEM, "lettuce"), Reward(RewardType.XP, "20")],
    # Day 4
    [Reward(RewardType.ITEM, "corn", 2), Reward(RewardType.XP, "25")],
    # Day 5
    [Reward(RewardType.ITEM, "worm"), Reward(RewardType.XP, "30")],
    # Day 6
    [Reward(RewardType.ITEM, "grapes"), Reward(RewardType.XP, "35")],
    # Day 7 (weekly bonus!)
    [Reward(RewardType.ITEM, "fancy_bread"), Reward(RewardType.XP, "100"),
     Reward(RewardType.COLLECTIBLE, "treasures:shiny_coin")],
]


class ProgressionSystem:
    """
    Manages player progression, rewards, and engagement mechanics.
    """

    def __init__(self):
        # XP and Level
        self.xp: int = 0
        self.level: int = 1
        self.title: str = "Duckling Watcher"

        # Streaks and daily
        self.current_streak: int = 0
        self.longest_streak: int = 0
        self.last_login_date: Optional[str] = None
        self.daily_reward_claimed: bool = False
        self.days_played: int = 0

        # Enhanced streak tracking
        self.streak_lost_today: bool = False  # Did we lose a streak today?
        self.previous_streak: int = 0  # Streak before it was lost (for emotional messaging)
        self.days_since_streak_loss: int = 0  # Track recovery period
        self.streak_celebration_shown: Dict[int, bool] = {}  # Track which celebrations shown

        # Collectibles: category -> item_id -> owned
        self.collectibles: Dict[str, Dict[str, bool]] = {}
        for category in COLLECTIBLES:
            self.collectibles[category] = {}

        # Milestone tracking
        self.milestone_progress: Dict[str, int] = {
            "interactions": 0,
            "days_played": 0,
            "streak": 0,
            "relationship": 0,
        }
        self.claimed_milestones: Dict[str, List[int]] = {
            "interactions": [],
            "days_played": [],
            "streak": [],
            "relationship": [],
        }

        # Daily challenges
        self.daily_challenges: List[DailyChallenge] = []
        self.last_challenge_refresh: Optional[str] = None

        # Unlocked titles
        self.unlocked_titles: List[str] = ["Duckling Watcher"]

        # Statistics for achievements
        self.stats: Dict[str, int] = {
            "total_feeds": 0,
            "total_plays": 0,
            "total_cleans": 0,
            "total_pets": 0,
            "total_talks": 0,
            "items_used": 0,
            "collectibles_found": 0,
        }

        # Pending rewards to show player
        self.pending_rewards: List[Tuple[str, Reward]] = []

    def add_xp(self, amount: int, source: str = "") -> Optional[int]:
        """
        Add XP and check for level up.
        Returns new level if leveled up, None otherwise.
        XP is multiplied based on current streak.
        """
        # Apply streak multiplier
        multiplier = self.get_streak_multiplier()
        boosted_amount = int(amount * multiplier)
        self.xp += boosted_amount
        old_level = self.level

        # Check for level up
        while self.xp >= xp_for_level(self.level + 1):
            self.level += 1

            # Check for new title
            if self.level in LEVEL_TITLES:
                new_title = LEVEL_TITLES[self.level]
                self.title = new_title
                self.unlocked_titles.append(new_title)

        if self.level > old_level:
            return self.level
        return None

    def get_streak_multiplier(self) -> float:
        """Get the current XP multiplier based on streak."""
        multiplier = 1.0
        for threshold, mult in sorted(STREAK_XP_MULTIPLIERS.items()):
            if self.current_streak >= threshold:
                multiplier = mult
        return multiplier

    def get_streak_multiplier_display(self) -> str:
        """Get a display string for current streak bonus."""
        mult = self.get_streak_multiplier()
        if mult > 1.0:
            return f"^ {mult}x XP"
        return ""

    def get_xp_progress(self) -> Tuple[int, int, float]:
        """Get current XP, XP needed for next level, and percentage."""
        current_level_xp = xp_for_level(self.level)
        next_level_xp = xp_for_level(self.level + 1)
        xp_in_level = self.xp - current_level_xp
        xp_needed = next_level_xp - current_level_xp
        percentage = (xp_in_level / xp_needed) * 100 if xp_needed > 0 else 100
        return xp_in_level, xp_needed, percentage

    def check_login(self) -> Tuple[bool, List[Reward], Optional[str]]:
        """
        Check daily login, update streak, return daily rewards if applicable.
        Returns (is_new_day, rewards_list, special_message)
        Special message can be streak loss, streak celebration, or None.
        """
        today = datetime.now().strftime("%Y-%m-%d")

        if self.last_login_date == today:
            return False, [], None

        # It's a new day!
        is_first_login = self.last_login_date is None
        rewards = []
        special_message = None
        self.streak_lost_today = False

        if not is_first_login:
            # Check if streak continues
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            if self.last_login_date == yesterday:
                self.current_streak += 1
                self.days_since_streak_loss = 0
            else:
                # Streak broken! Track for emotional messaging
                if self.current_streak > 1:
                    self.streak_lost_today = True
                    self.previous_streak = self.current_streak
                    # Generate emotional loss message
                    msg_template = random.choice(STREAK_LOSS_MESSAGES)
                    special_message = msg_template.format(n=self.previous_streak)
                self.current_streak = 1
                self.days_since_streak_loss += 1
        else:
            self.current_streak = 1

        # Update longest streak
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak

        # Check for streak celebration milestone
        if self.current_streak in STREAK_CELEBRATION_MESSAGES:
            if not self.streak_celebration_shown.get(self.current_streak, False):
                special_message = STREAK_CELEBRATION_MESSAGES[self.current_streak]
                self.streak_celebration_shown[self.current_streak] = True

        # Increment days played
        self.days_played += 1

        # Get daily rewards based on streak (cycles through week)
        reward_day = (self.current_streak - 1) % 7
        rewards = DAILY_REWARDS[reward_day].copy()

        # Bonus for long streaks
        if self.current_streak >= 30 and self.current_streak % 30 == 0:
            rewards.append(Reward(RewardType.COLLECTIBLE, "feathers:iridescent_feather",
                                  description="30 day streak bonus!"))
        elif self.current_streak >= 7 and self.current_streak % 7 == 0:
            rewards.append(Reward(RewardType.XP, "50", description="Weekly streak bonus!"))

        # Recovery bonus - after losing a streak, if you come back within 3 days
        if 0 < self.days_since_streak_loss <= STREAK_RECOVERY_DAYS and not self.streak_lost_today:
            rewards.append(Reward(RewardType.XP, "25", description="Welcome back bonus!"))

        self.last_login_date = today
        self.daily_reward_claimed = False

        # Update milestone progress
        self.milestone_progress["streak"] = self.current_streak
        self.milestone_progress["days_played"] = self.days_played

        return True, rewards, special_message

    def claim_daily_rewards(self) -> List[Reward]:
        """Claim daily rewards. Returns list of rewards or empty if already claimed."""
        if self.daily_reward_claimed:
            return []

        self.daily_reward_claimed = True
        _, rewards = self.check_login()

        for reward in rewards:
            self.pending_rewards.append(("Daily Reward", reward))

        return rewards

    def record_interaction(self, interaction_type: str):
        """Record an interaction for milestone tracking."""
        self.milestone_progress["interactions"] += 1

        # Track specific stats
        stat_map = {
            "feed": "total_feeds",
            "play": "total_plays",
            "clean": "total_cleans",
            "pet": "total_pets",
            "talk": "total_talks",
        }
        if interaction_type in stat_map:
            self.stats[stat_map[interaction_type]] += 1

        # Small XP for interactions
        self.add_xp(2, interaction_type)

    def update_relationship(self, level: int):
        """Update relationship level for milestones."""
        self.milestone_progress["relationship"] = level

    def check_milestones(self) -> List[Tuple[str, int, Reward]]:
        """
        Check for newly achieved milestones.
        Returns list of (category, threshold, reward) tuples.
        """
        achieved = []

        for category, thresholds in MILESTONES.items():
            current = self.milestone_progress.get(category, 0)
            claimed = self.claimed_milestones.get(category, [])

            for threshold, reward in thresholds:
                if current >= threshold and threshold not in claimed:
                    achieved.append((category, threshold, reward))
                    claimed.append(threshold)
                    self.pending_rewards.append((f"Milestone: {category}", reward))

        return achieved

    def add_collectible(self, collectible_id: str) -> bool:
        """
        Add a collectible. ID format: "category:item_id"
        Returns True if new, False if already owned.
        """
        if ":" not in collectible_id:
            return False

        category, item_id = collectible_id.split(":", 1)

        if category not in self.collectibles:
            return False

        if self.collectibles[category].get(item_id, False):
            return False  # Already owned

        self.collectibles[category][item_id] = True
        self.stats["collectibles_found"] += 1
        return True

    def has_collectible(self, collectible_id: str) -> bool:
        """Check if player has a collectible."""
        if ":" not in collectible_id:
            return False
        category, item_id = collectible_id.split(":", 1)
        return self.collectibles.get(category, {}).get(item_id, False)

    def get_collection_progress(self, category: str) -> Tuple[int, int]:
        """Get (owned, total) for a collection category."""
        if category not in COLLECTIBLES:
            return 0, 0

        total = len(COLLECTIBLES[category]["items"])
        owned = sum(1 for v in self.collectibles.get(category, {}).values() if v)
        return owned, total

    def get_total_collection_progress(self) -> Tuple[int, int]:
        """Get total collectibles (owned, total)."""
        owned = 0
        total = 0
        for category in COLLECTIBLES:
            o, t = self.get_collection_progress(category)
            owned += o
            total += t
        return owned, total

    def generate_daily_challenges(self) -> List[DailyChallenge]:
        """Generate new daily challenges."""
        today = datetime.now().strftime("%Y-%m-%d")

        if self.last_challenge_refresh == today and self.daily_challenges:
            return self.daily_challenges

        # Generate 3 random challenges
        challenge_templates = [
            ("feed_duck", "Feed Cheese", "Feed Cheese {n} times", 3,
             Reward(RewardType.XP, "25")),
            ("play_duck", "Playtime!", "Play with Cheese {n} times", 3,
             Reward(RewardType.XP, "25")),
            ("talk_duck", "Conversation", "Talk to Cheese {n} times", 2,
             Reward(RewardType.XP, "30")),
            ("pet_duck", "Affection", "Pet Cheese {n} times", 5,
             Reward(RewardType.ITEM, "bread", 2)),
            ("use_items", "Item User", "Use {n} items from inventory", 2,
             Reward(RewardType.XP, "20")),
            ("happy_duck", "Keep Happy", "Keep Cheese happy for {n} interactions", 5,
             Reward(RewardType.ITEM, "seeds", 3)),
        ]

        selected = random.sample(challenge_templates, min(3, len(challenge_templates)))
        tomorrow = (datetime.now() + timedelta(days=1)).replace(
            hour=0, minute=0, second=0
        ).isoformat()

        self.daily_challenges = []
        for id_prefix, name, desc_template, target, reward in selected:
            challenge = DailyChallenge(
                id=f"{id_prefix}_{today}",
                name=name,
                description=desc_template.format(n=target),
                target=target,
                progress=0,
                reward=reward,
                expires=tomorrow,
            )
            self.daily_challenges.append(challenge)

        self.last_challenge_refresh = today
        return self.daily_challenges

    def update_challenge_progress(self, challenge_type: str, amount: int = 1):
        """Update progress on daily challenges."""
        type_mapping = {
            "feed": "feed_duck",
            "play": "play_duck",
            "talk": "talk_duck",
            "pet": "pet_duck",
            "use_item": "use_items",
            "happy": "happy_duck",
        }

        prefix = type_mapping.get(challenge_type, challenge_type)

        for challenge in self.daily_challenges:
            if challenge.id.startswith(prefix) and challenge.progress < challenge.target:
                challenge.progress = min(challenge.progress + amount, challenge.target)

                # Check if completed
                if challenge.progress >= challenge.target and challenge.reward:
                    self.pending_rewards.append(
                        (f"Challenge: {challenge.name}", challenge.reward)
                    )
                    challenge.reward = None  # Don't reward again

    def get_pending_rewards(self) -> List[Tuple[str, Reward]]:
        """Get and clear pending rewards."""
        rewards = self.pending_rewards.copy()
        self.pending_rewards = []
        return rewards

    def random_collectible_drop(self, base_chance: float = 0.02) -> Optional[str]:
        """
        Random chance to find a collectible.
        Returns collectible_id if found, None otherwise.
        """
        if random.random() > base_chance:
            return None

        # Weight by rarity
        all_collectibles = []
        for category, data in COLLECTIBLES.items():
            for item_id, item_data in data["items"].items():
                if not self.has_collectible(f"{category}:{item_id}"):
                    rarity = item_data.get("rarity", "common")
                    weight = {"common": 60, "uncommon": 25, "rare": 10, "legendary": 1}.get(rarity, 10)
                    all_collectibles.extend([(category, item_id)] * weight)

        if not all_collectibles:
            return None

        category, item_id = random.choice(all_collectibles)
        collectible_id = f"{category}:{item_id}"
        self.add_collectible(collectible_id)
        return collectible_id

    def check_lucky_event(self) -> Optional[Tuple[str, Reward]]:
        """
        Check for random lucky events (variable ratio reinforcement).
        Returns (message, reward) if lucky event triggers, None otherwise.
        """
        for event in LUCKY_EVENTS:
            if random.random() < event["chance"]:
                reward = Reward(
                    reward_type=RewardType(event["reward_type"]),
                    value=event["value"],
                    description=event["name"],
                    rare=event["chance"] < 0.01,
                )
                return (event["message"], reward)
        return None

    def check_time_bonus(self) -> Optional[Tuple[str, float]]:
        """
        Check if current time qualifies for a time bonus.
        Returns (message, multiplier) if in bonus window, None otherwise.
        """
        current_hour = datetime.now().hour
        for bonus_name, bonus_data in TIME_BONUSES.items():
            start_hour, end_hour = bonus_data["hours"]
            if start_hour <= current_hour < end_hour:
                return (bonus_data["message"], bonus_data["xp_mult"])
        return None

    def get_surprise_gift(self) -> Optional[Tuple[str, Reward]]:
        """
        Random surprise gift (used for dopamine hits during play).
        Lower chance than lucky events but better rewards.
        """
        if random.random() > 0.008:  # 0.8% chance
            return None

        gift_message = random.choice(SURPRISE_GIFT_MESSAGES)

        # Pick a random reward type with weighted probabilities
        roll = random.random()
        if roll < 0.4:
            # XP bonus
            xp_amount = random.choice([20, 30, 50, 75])
            reward = Reward(RewardType.XP, str(xp_amount), description="Surprise XP!")
        elif roll < 0.7:
            # Item
            items = ["bread", "seeds", "lettuce", "corn", "grapes"]
            item = random.choice(items)
            reward = Reward(RewardType.ITEM, item, description="Surprise gift!")
        elif roll < 0.9:
            # Better item
            items = ["worm", "fancy_bread", "rubber_duck"]
            item = random.choice(items)
            reward = Reward(RewardType.ITEM, item, description="Special gift!", rare=True)
        else:
            # Random collectible chance
            collectible = self.random_collectible_drop(base_chance=1.0)
            if collectible:
                reward = Reward(RewardType.COLLECTIBLE, collectible, description="Rare find!", rare=True)
            else:
                reward = Reward(RewardType.XP, "100", description="Bonus XP!", rare=True)

        return (gift_message, reward)

    def roll_interaction_bonus(self) -> Optional[Tuple[str, int]]:
        """
        Chance for bonus XP on interactions (slot machine psychology).
        Returns (message, bonus_xp) or None.
        """
        roll = random.random()
        if roll < 0.1:  # 10% chance for small bonus
            return ("Nice! +5 bonus XP!", 5)
        elif roll < 0.03:  # 3% chance for medium bonus
            return ("Great! +15 bonus XP!", 15)
        elif roll < 0.005:  # 0.5% chance for jackpot
            return ("[#] JACKPOT! +50 bonus XP! [#]", 50)
        return None

    def get_time_greeting(self) -> str:
        """Get a greeting appropriate for the current time of day."""
        current_hour = datetime.now().hour
        for period, data in TIME_GREETINGS.items():
            start_hour, end_hour = data["hours"]
            if start_hour <= current_hour < end_hour:
                return random.choice(data["greetings"])
            elif period == "late_night" and (current_hour >= start_hour or current_hour < end_hour):
                return random.choice(data["greetings"])
        return random.choice(TIME_GREETINGS["morning"]["greetings"])

    def get_time_away_message(self, days_away: int) -> Optional[str]:
        """Get a comfort message based on how long the player was away."""
        if days_away <= 0:
            return None
        elif days_away <= 3:
            return random.choice(COMFORT_MESSAGES["time_away_short"])
        elif days_away <= 7:
            return random.choice(COMFORT_MESSAGES["time_away_medium"])
        else:
            return random.choice(COMFORT_MESSAGES["time_away_long"])

    def get_encouragement(self) -> str:
        """Get a random encouragement message."""
        return random.choice(COMFORT_MESSAGES["encouragement"])

    def get_gentle_reminder(self) -> str:
        """Get a gentle reminder message."""
        return random.choice(COMFORT_MESSAGES["gentle_reminder"])

    def get_ambient_event(self, chance: float = 0.05) -> Optional[str]:
        """
        Get a random ambient event description.
        Low chance to trigger for peaceful atmosphere.
        """
        if random.random() < chance:
            return random.choice(AMBIENT_EVENTS)
        return None

    def calculate_days_away(self) -> int:
        """Calculate how many days since last login."""
        if not self.last_login_date:
            return 0
        try:
            last = datetime.strptime(self.last_login_date, "%Y-%m-%d")
            today = datetime.now()
            return (today - last).days
        except (ValueError, TypeError):
            return 0

    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "xp": self.xp,
            "level": self.level,
            "title": self.title,
            "current_streak": self.current_streak,
            "longest_streak": self.longest_streak,
            "last_login_date": self.last_login_date,
            "daily_reward_claimed": self.daily_reward_claimed,
            "days_played": self.days_played,
            # Enhanced streak tracking
            "previous_streak": self.previous_streak,
            "days_since_streak_loss": self.days_since_streak_loss,
            "streak_celebration_shown": self.streak_celebration_shown,
            # Collections and milestones
            "collectibles": self.collectibles,
            "milestone_progress": self.milestone_progress,
            "claimed_milestones": self.claimed_milestones,
            "daily_challenges": [
                {
                    "id": c.id,
                    "name": c.name,
                    "description": c.description,
                    "target": c.target,
                    "progress": c.progress,
                    "expires": c.expires,
                }
                for c in self.daily_challenges
            ],
            "last_challenge_refresh": self.last_challenge_refresh,
            "unlocked_titles": self.unlocked_titles,
            "stats": self.stats,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ProgressionSystem":
        """Create from dictionary."""
        prog = cls()
        prog.xp = data.get("xp", 0)
        prog.level = data.get("level", 1)
        prog.title = data.get("title", "Duckling Watcher")
        prog.current_streak = data.get("current_streak", 0)
        prog.longest_streak = data.get("longest_streak", 0)
        prog.last_login_date = data.get("last_login_date")
        prog.daily_reward_claimed = data.get("daily_reward_claimed", False)
        prog.days_played = data.get("days_played", 0)
        # Enhanced streak tracking
        prog.previous_streak = data.get("previous_streak", 0)
        prog.days_since_streak_loss = data.get("days_since_streak_loss", 0)
        prog.streak_celebration_shown = data.get("streak_celebration_shown", {})
        # Convert string keys to int (JSON serialization converts int keys to strings)
        prog.streak_celebration_shown = {int(k): v for k, v in prog.streak_celebration_shown.items()}
        # Collections and milestones
        prog.collectibles = data.get("collectibles", {})
        prog.milestone_progress = data.get("milestone_progress", {})
        prog.claimed_milestones = data.get("claimed_milestones", {})
        prog.unlocked_titles = data.get("unlocked_titles", ["Duckling Watcher"])
        prog.stats = data.get("stats", {})
        prog.last_challenge_refresh = data.get("last_challenge_refresh")

        # Restore daily challenges
        for c_data in data.get("daily_challenges", []):
            challenge = DailyChallenge(
                id=c_data["id"],
                name=c_data["name"],
                description=c_data["description"],
                target=c_data["target"],
                progress=c_data.get("progress", 0),
                expires=c_data.get("expires"),
            )
            prog.daily_challenges.append(challenge)

        return prog


# Global instance
progression_system = ProgressionSystem()
