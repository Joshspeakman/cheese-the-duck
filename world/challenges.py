"""
Challenges System - Daily and weekly challenges with bonus rewards.
Features streak bonuses, special challenges, and achievement tracking.
"""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random


class ChallengeType(Enum):
    """Types of challenges."""
    DAILY = "daily"
    WEEKLY = "weekly"
    SPECIAL = "special"
    SEASONAL = "seasonal"


class ChallengeDifficulty(Enum):
    """Challenge difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXTREME = "extreme"


@dataclass
class ChallengeDefinition:
    """A challenge definition template."""
    id: str
    name: str
    description: str
    challenge_type: ChallengeType
    difficulty: ChallengeDifficulty
    goal_type: str  # feed, play, talk, explore, etc.
    goal_amount: int
    xp_reward: int
    coin_reward: int
    bonus_item: Optional[str] = None
    time_limit_hours: Optional[int] = None


@dataclass
class ActiveChallenge:
    """An active challenge being tracked."""
    challenge_id: str
    started_at: str
    expires_at: str
    current_progress: int
    goal_amount: int
    completed: bool = False
    claimed: bool = False


# Challenge definitions
DAILY_CHALLENGES: Dict[str, ChallengeDefinition] = {
    # Easy challenges
    "feed_5": ChallengeDefinition(
        id="feed_5", name="Snack Time",
        description="Feed your duck 5 times",
        challenge_type=ChallengeType.DAILY,
        difficulty=ChallengeDifficulty.EASY,
        goal_type="feed", goal_amount=5,
        xp_reward=25, coin_reward=15,
    ),
    "play_3": ChallengeDefinition(
        id="play_3", name="Playtime!",
        description="Play with your duck 3 times",
        challenge_type=ChallengeType.DAILY,
        difficulty=ChallengeDifficulty.EASY,
        goal_type="play", goal_amount=3,
        xp_reward=20, coin_reward=10,
    ),
    "pet_5": ChallengeDefinition(
        id="pet_5", name="Cuddle Time",
        description="Pet your duck 5 times",
        challenge_type=ChallengeType.DAILY,
        difficulty=ChallengeDifficulty.EASY,
        goal_type="pet", goal_amount=5,
        xp_reward=20, coin_reward=10,
    ),
    "talk_3": ChallengeDefinition(
        id="talk_3", name="Chit Chat",
        description="Talk to your duck 3 times",
        challenge_type=ChallengeType.DAILY,
        difficulty=ChallengeDifficulty.EASY,
        goal_type="talk", goal_amount=3,
        xp_reward=15, coin_reward=10,
    ),
    
    # Medium challenges
    "feed_10": ChallengeDefinition(
        id="feed_10", name="Feast Day",
        description="Feed your duck 10 times",
        challenge_type=ChallengeType.DAILY,
        difficulty=ChallengeDifficulty.MEDIUM,
        goal_type="feed", goal_amount=10,
        xp_reward=50, coin_reward=30,
    ),
    "explore_2": ChallengeDefinition(
        id="explore_2", name="Explorer",
        description="Explore 2 different areas",
        challenge_type=ChallengeType.DAILY,
        difficulty=ChallengeDifficulty.MEDIUM,
        goal_type="explore", goal_amount=2,
        xp_reward=40, coin_reward=25,
    ),
    "minigame_3": ChallengeDefinition(
        id="minigame_3", name="Gamer Duck",
        description="Play 3 mini-games",
        challenge_type=ChallengeType.DAILY,
        difficulty=ChallengeDifficulty.MEDIUM,
        goal_type="minigame", goal_amount=3,
        xp_reward=45, coin_reward=30,
    ),
    "happy_mood": ChallengeDefinition(
        id="happy_mood", name="Keep Smiling",
        description="Keep duck happy for 30 minutes",
        challenge_type=ChallengeType.DAILY,
        difficulty=ChallengeDifficulty.MEDIUM,
        goal_type="happy_time", goal_amount=30,
        xp_reward=60, coin_reward=40,
    ),
    
    # Hard challenges
    "perfect_care": ChallengeDefinition(
        id="perfect_care", name="Perfect Caretaker",
        description="Keep all needs above 80% for 1 hour",
        challenge_type=ChallengeType.DAILY,
        difficulty=ChallengeDifficulty.HARD,
        goal_type="perfect_care", goal_amount=60,
        xp_reward=100, coin_reward=75,
        bonus_item="rare_treat",
    ),
    "all_activities": ChallengeDefinition(
        id="all_activities", name="Variety Day",
        description="Do all 5 activity types today",
        challenge_type=ChallengeType.DAILY,
        difficulty=ChallengeDifficulty.HARD,
        goal_type="activity_variety", goal_amount=5,
        xp_reward=80, coin_reward=60,
    ),
}

WEEKLY_CHALLENGES: Dict[str, ChallengeDefinition] = {
    # Medium weekly challenges
    "weekly_feed_50": ChallengeDefinition(
        id="weekly_feed_50", name="Weekly Feast",
        description="Feed your duck 50 times this week",
        challenge_type=ChallengeType.WEEKLY,
        difficulty=ChallengeDifficulty.MEDIUM,
        goal_type="feed", goal_amount=50,
        xp_reward=200, coin_reward=150,
    ),
    "weekly_play_25": ChallengeDefinition(
        id="weekly_play_25", name="Playful Week",
        description="Play 25 times this week",
        challenge_type=ChallengeType.WEEKLY,
        difficulty=ChallengeDifficulty.MEDIUM,
        goal_type="play", goal_amount=25,
        xp_reward=175, coin_reward=125,
    ),
    "weekly_login_7": ChallengeDefinition(
        id="weekly_login_7", name="Dedicated",
        description="Log in every day this week",
        challenge_type=ChallengeType.WEEKLY,
        difficulty=ChallengeDifficulty.MEDIUM,
        goal_type="login", goal_amount=7,
        xp_reward=250, coin_reward=200,
        bonus_item="weekly_chest",
    ),
    
    # Hard weekly challenges
    "weekly_explore_10": ChallengeDefinition(
        id="weekly_explore_10", name="Grand Explorer",
        description="Complete 10 explorations this week",
        challenge_type=ChallengeType.WEEKLY,
        difficulty=ChallengeDifficulty.HARD,
        goal_type="explore", goal_amount=10,
        xp_reward=300, coin_reward=250,
        bonus_item="explorer_badge",
    ),
    "weekly_minigame_20": ChallengeDefinition(
        id="weekly_minigame_20", name="Mini-Game Master",
        description="Play 20 mini-games this week",
        challenge_type=ChallengeType.WEEKLY,
        difficulty=ChallengeDifficulty.HARD,
        goal_type="minigame", goal_amount=20,
        xp_reward=350, coin_reward=275,
    ),
    
    # Extreme weekly challenge
    "weekly_master": ChallengeDefinition(
        id="weekly_master", name="Master Caretaker",
        description="Complete all other weekly challenges",
        challenge_type=ChallengeType.WEEKLY,
        difficulty=ChallengeDifficulty.EXTREME,
        goal_type="complete_weekly", goal_amount=4,
        xp_reward=500, coin_reward=400,
        bonus_item="master_trophy",
    ),
}

SPECIAL_CHALLENGES: Dict[str, ChallengeDefinition] = {
    "first_rainbow": ChallengeDefinition(
        id="first_rainbow", name="Rainbow Hunter",
        description="Experience a rainbow event",
        challenge_type=ChallengeType.SPECIAL,
        difficulty=ChallengeDifficulty.MEDIUM,
        goal_type="see_rainbow", goal_amount=1,
        xp_reward=100, coin_reward=100,
        bonus_item="rainbow_charm",
    ),
    "catch_legendary": ChallengeDefinition(
        id="catch_legendary", name="Legend Fisher",
        description="Catch a legendary fish",
        challenge_type=ChallengeType.SPECIAL,
        difficulty=ChallengeDifficulty.EXTREME,
        goal_type="catch_legendary_fish", goal_amount=1,
        xp_reward=500, coin_reward=500,
        bonus_item="legendary_trophy",
    ),
    "grow_golden": ChallengeDefinition(
        id="grow_golden", name="Golden Gardener",
        description="Grow a golden flower",
        challenge_type=ChallengeType.SPECIAL,
        difficulty=ChallengeDifficulty.HARD,
        goal_type="grow_golden_flower", goal_amount=1,
        xp_reward=300, coin_reward=300,
        bonus_item="golden_badge",
    ),
}


class ChallengeSystem:
    """
    Manages daily and weekly challenges.
    """
    
    def __init__(self):
        self.active_daily: List[ActiveChallenge] = []
        self.active_weekly: List[ActiveChallenge] = []
        self.active_special: List[ActiveChallenge] = []
        self.completed_challenges: Dict[str, int] = {}  # challenge_id -> times completed
        self.daily_refresh_date: str = ""
        self.weekly_refresh_date: str = ""
        self.challenge_streak: int = 0
        self.last_complete_date: str = ""
        self.total_challenges_completed: int = 0
        self.total_rewards_earned: Dict[str, int] = {"xp": 0, "coins": 0}
    
    def refresh_daily_challenges(self, force: bool = False) -> bool:
        """Refresh daily challenges if needed."""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if self.daily_refresh_date == today and not force:
            return False
        
        # Select 3 random daily challenges
        challenge_pool = list(DAILY_CHALLENGES.values())
        selected = random.sample(challenge_pool, min(3, len(challenge_pool)))
        
        now = datetime.now()
        tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0)
        
        self.active_daily = [
            ActiveChallenge(
                challenge_id=c.id,
                started_at=now.isoformat(),
                expires_at=tomorrow.isoformat(),
                current_progress=0,
                goal_amount=c.goal_amount,
            )
            for c in selected
        ]
        
        self.daily_refresh_date = today
        return True
    
    def refresh_weekly_challenges(self, force: bool = False) -> bool:
        """Refresh weekly challenges if needed."""
        today = datetime.now()
        week_num = today.isocalendar()[1]
        year = today.year
        week_key = f"{year}-W{week_num}"
        
        if self.weekly_refresh_date == week_key and not force:
            return False
        
        # Select 4 weekly challenges
        challenge_pool = list(WEEKLY_CHALLENGES.values())
        selected = random.sample(challenge_pool, min(4, len(challenge_pool)))
        
        # Calculate end of week
        days_until_monday = (7 - today.weekday()) % 7
        if days_until_monday == 0:
            days_until_monday = 7
        next_monday = (today + timedelta(days=days_until_monday)).replace(hour=0, minute=0, second=0)
        
        self.active_weekly = [
            ActiveChallenge(
                challenge_id=c.id,
                started_at=today.isoformat(),
                expires_at=next_monday.isoformat(),
                current_progress=0,
                goal_amount=c.goal_amount,
            )
            for c in selected
        ]
        
        self.weekly_refresh_date = week_key
        return True
    
    def update_progress(self, goal_type: str, amount: int = 1) -> List[Tuple[str, bool]]:
        """Update progress on challenges matching the goal type."""
        updates = []
        
        all_challenges = self.active_daily + self.active_weekly + self.active_special
        
        for challenge in all_challenges:
            if challenge.completed:
                continue
            
            definition = self._get_definition(challenge.challenge_id)
            if not definition:
                continue
            
            if definition.goal_type == goal_type:
                challenge.current_progress = min(
                    challenge.current_progress + amount,
                    challenge.goal_amount
                )
                
                # Check for completion
                if challenge.current_progress >= challenge.goal_amount:
                    challenge.completed = True
                    updates.append((challenge.challenge_id, True))
                else:
                    updates.append((challenge.challenge_id, False))
        
        return updates
    
    def claim_reward(self, challenge_id: str) -> Tuple[bool, str, Dict]:
        """Claim reward for a completed challenge."""
        challenge = self._find_challenge(challenge_id)
        if not challenge:
            return False, "Challenge not found!", {}
        
        if not challenge.completed:
            return False, "Challenge not completed yet!", {}
        
        if challenge.claimed:
            return False, "Reward already claimed!", {}
        
        definition = self._get_definition(challenge_id)
        if not definition:
            return False, "Challenge definition not found!", {}
        
        # Mark as claimed
        challenge.claimed = True
        
        # Update stats
        self.total_challenges_completed += 1
        self.completed_challenges[challenge_id] = self.completed_challenges.get(challenge_id, 0) + 1
        self.total_rewards_earned["xp"] += definition.xp_reward
        self.total_rewards_earned["coins"] += definition.coin_reward
        
        # Update streak
        today = datetime.now().strftime("%Y-%m-%d")
        if self.last_complete_date != today:
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            if self.last_complete_date == yesterday:
                self.challenge_streak += 1
            else:
                self.challenge_streak = 1
            self.last_complete_date = today
        
        # Calculate streak bonus
        streak_bonus = min(self.challenge_streak * 0.1, 0.5)  # Up to 50% bonus
        bonus_xp = int(definition.xp_reward * streak_bonus)
        bonus_coins = int(definition.coin_reward * streak_bonus)
        
        rewards = {
            "xp": definition.xp_reward + bonus_xp,
            "coins": definition.coin_reward + bonus_coins,
            "streak_bonus": streak_bonus,
            "item": definition.bonus_item,
        }
        
        return True, f"* Challenge Complete! +{rewards['xp']} XP, +{rewards['coins']} coins!", rewards
    
    def _find_challenge(self, challenge_id: str) -> Optional[ActiveChallenge]:
        """Find an active challenge by ID."""
        for challenge in self.active_daily + self.active_weekly + self.active_special:
            if challenge.challenge_id == challenge_id:
                return challenge
        return None
    
    def _get_definition(self, challenge_id: str) -> Optional[ChallengeDefinition]:
        """Get challenge definition by ID."""
        if challenge_id in DAILY_CHALLENGES:
            return DAILY_CHALLENGES[challenge_id]
        if challenge_id in WEEKLY_CHALLENGES:
            return WEEKLY_CHALLENGES[challenge_id]
        if challenge_id in SPECIAL_CHALLENGES:
            return SPECIAL_CHALLENGES[challenge_id]
        return None
    
    def add_special_challenge(self, challenge_id: str, duration_hours: int = 24):
        """Add a special/seasonal challenge."""
        definition = SPECIAL_CHALLENGES.get(challenge_id)
        if not definition:
            return
        
        now = datetime.now()
        expires = now + timedelta(hours=duration_hours)
        
        challenge = ActiveChallenge(
            challenge_id=challenge_id,
            started_at=now.isoformat(),
            expires_at=expires.isoformat(),
            current_progress=0,
            goal_amount=definition.goal_amount,
        )
        self.active_special.append(challenge)
    
    def get_daily_progress(self) -> Dict:
        """Get summary of daily challenge progress."""
        completed = sum(1 for c in self.active_daily if c.completed)
        total = len(self.active_daily)
        
        return {
            "completed": completed,
            "total": total,
            "challenges": [
                {
                    "id": c.challenge_id,
                    "progress": c.current_progress,
                    "goal": c.goal_amount,
                    "completed": c.completed,
                    "claimed": c.claimed,
                }
                for c in self.active_daily
            ],
        }
    
    def get_weekly_progress(self) -> Dict:
        """Get summary of weekly challenge progress."""
        completed = sum(1 for c in self.active_weekly if c.completed)
        total = len(self.active_weekly)
        
        return {
            "completed": completed,
            "total": total,
            "challenges": [
                {
                    "id": c.challenge_id,
                    "progress": c.current_progress,
                    "goal": c.goal_amount,
                    "completed": c.completed,
                    "claimed": c.claimed,
                }
                for c in self.active_weekly
            ],
        }
    
    def render_challenges(self) -> List[str]:
        """Render the challenges display."""
        lines = [
            "+===============================================+",
            "|          [=] CHALLENGES [=]                     |",
            f"|  Streak: {self.challenge_streak} days ^                          |",
            "+===============================================+",
            "|  [=] DAILY CHALLENGES:                         |",
        ]
        
        for challenge in self.active_daily:
            definition = self._get_definition(challenge.challenge_id)
            if definition:
                status = "[x]" if challenge.completed else f"{challenge.current_progress}/{challenge.goal_amount}"
                claimed = " [+]" if challenge.claimed else ""
                lines.append(f"|   {status} {definition.name[:20]:20}{claimed}    |")
        
        lines.append("+===============================================+")
        lines.append("|  [=] WEEKLY CHALLENGES:                        |")
        
        for challenge in self.active_weekly:
            definition = self._get_definition(challenge.challenge_id)
            if definition:
                status = "[x]" if challenge.completed else f"{challenge.current_progress}/{challenge.goal_amount}"
                claimed = " [+]" if challenge.claimed else ""
                lines.append(f"|   {status} {definition.name[:20]:20}{claimed}    |")
        
        if self.active_special:
            lines.append("+===============================================+")
            lines.append("|  * SPECIAL CHALLENGES:                       |")
            for challenge in self.active_special:
                definition = self._get_definition(challenge.challenge_id)
                if definition:
                    status = "[x]" if challenge.completed else f"{challenge.current_progress}/{challenge.goal_amount}"
                    lines.append(f"|   {status} {definition.name[:20]:20}        |")
        
        lines.append("+===============================================+")
        lines.append(f"|  Total Completed: {self.total_challenges_completed:5}                      |")
        lines.append("+===============================================+")
        
        return lines
    
    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "active_daily": [
                {
                    "challenge_id": c.challenge_id,
                    "started_at": c.started_at,
                    "expires_at": c.expires_at,
                    "current_progress": c.current_progress,
                    "goal_amount": c.goal_amount,
                    "completed": c.completed,
                    "claimed": c.claimed,
                }
                for c in self.active_daily
            ],
            "active_weekly": [
                {
                    "challenge_id": c.challenge_id,
                    "started_at": c.started_at,
                    "expires_at": c.expires_at,
                    "current_progress": c.current_progress,
                    "goal_amount": c.goal_amount,
                    "completed": c.completed,
                    "claimed": c.claimed,
                }
                for c in self.active_weekly
            ],
            "active_special": [
                {
                    "challenge_id": c.challenge_id,
                    "started_at": c.started_at,
                    "expires_at": c.expires_at,
                    "current_progress": c.current_progress,
                    "goal_amount": c.goal_amount,
                    "completed": c.completed,
                    "claimed": c.claimed,
                }
                for c in self.active_special
            ],
            "completed_challenges": self.completed_challenges,
            "daily_refresh_date": self.daily_refresh_date,
            "weekly_refresh_date": self.weekly_refresh_date,
            "challenge_streak": self.challenge_streak,
            "last_complete_date": self.last_complete_date,
            "total_challenges_completed": self.total_challenges_completed,
            "total_rewards_earned": self.total_rewards_earned,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ChallengeSystem":
        """Create from dictionary."""
        system = cls()
        
        system.active_daily = [
            ActiveChallenge(
                challenge_id=c["challenge_id"],
                started_at=c["started_at"],
                expires_at=c["expires_at"],
                current_progress=c["current_progress"],
                goal_amount=c["goal_amount"],
                completed=c.get("completed", False),
                claimed=c.get("claimed", False),
            )
            for c in data.get("active_daily", [])
        ]
        
        system.active_weekly = [
            ActiveChallenge(
                challenge_id=c["challenge_id"],
                started_at=c["started_at"],
                expires_at=c["expires_at"],
                current_progress=c["current_progress"],
                goal_amount=c["goal_amount"],
                completed=c.get("completed", False),
                claimed=c.get("claimed", False),
            )
            for c in data.get("active_weekly", [])
        ]
        
        system.active_special = [
            ActiveChallenge(
                challenge_id=c["challenge_id"],
                started_at=c["started_at"],
                expires_at=c["expires_at"],
                current_progress=c["current_progress"],
                goal_amount=c["goal_amount"],
                completed=c.get("completed", False),
                claimed=c.get("claimed", False),
            )
            for c in data.get("active_special", [])
        ]
        
        system.completed_challenges = data.get("completed_challenges", {})
        system.daily_refresh_date = data.get("daily_refresh_date", "")
        system.weekly_refresh_date = data.get("weekly_refresh_date", "")
        system.challenge_streak = data.get("challenge_streak", 0)
        system.last_complete_date = data.get("last_complete_date", "")
        system.total_challenges_completed = data.get("total_challenges_completed", 0)
        system.total_rewards_earned = data.get("total_rewards_earned", {"xp": 0, "coins": 0})
        
        return system


# Global challenge system instance
challenge_system = ChallengeSystem()
