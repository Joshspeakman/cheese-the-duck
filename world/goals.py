"""
Goals/Quests system - gives players objectives to complete.
"""
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import random


@dataclass
class Goal:
    """A goal/quest the player can complete."""
    id: str
    name: str
    description: str
    goal_type: str  # daily, weekly, achievement, secret
    action: str  # What action progresses this goal
    target: int  # How many times to complete
    progress: int = 0
    completed: bool = False
    reward_item: Optional[str] = None
    reward_message: str = ""
    hidden: bool = False  # Secret goals don't show until unlocked


# Goal templates
DAILY_GOALS = [
    Goal(
        id="feed_duck_daily",
        name="Breakfast Time",
        description="Feed your duck 3 times today",
        goal_type="daily",
        action="feed",
        target=3,
        reward_message="Your duck had a filling day!",
    ),
    Goal(
        id="play_duck_daily",
        name="Playtime!",
        description="Play with your duck 2 times",
        goal_type="daily",
        action="play",
        target=2,
        reward_message="Fun was had by all!",
    ),
    Goal(
        id="pet_duck_daily",
        name="Affection",
        description="Pet your duck 3 times",
        goal_type="daily",
        action="pet",
        target=3,
        reward_message="Your duck feels loved!",
    ),
    Goal(
        id="talk_duck_daily",
        name="Chit Chat",
        description="Have 2 conversations with your duck",
        goal_type="daily",
        action="talk",
        target=2,
        reward_message="Communication is key!",
    ),
    Goal(
        id="clean_duck_daily",
        name="Squeaky Clean",
        description="Clean your duck today",
        goal_type="daily",
        action="clean",
        target=1,
        reward_message="Fresh as a daisy!",
    ),
]

WEEKLY_GOALS = [
    Goal(
        id="feed_duck_weekly",
        name="Well Fed",
        description="Feed your duck 20 times this week",
        goal_type="weekly",
        action="feed",
        target=20,
        reward_item="fancy_bread",
        reward_message="Earned: Fancy Artisan Bread!",
    ),
    Goal(
        id="play_duck_weekly",
        name="Party Duck",
        description="Play with your duck 15 times this week",
        goal_type="weekly",
        action="play",
        target=15,
        reward_item="ball",
        reward_message="Earned: Bouncy Ball!",
    ),
    Goal(
        id="talk_duck_weekly",
        name="Best Friends",
        description="Have 10 conversations this week",
        goal_type="weekly",
        action="talk",
        target=10,
        reward_item="mirror",
        reward_message="Earned: Small Mirror!",
    ),
]

ACHIEVEMENT_GOALS = [
    Goal(
        id="first_feed",
        name="First Meal",
        description="Feed your duck for the first time",
        goal_type="achievement",
        action="feed",
        target=1,
        reward_message="Your journey begins!",
    ),
    Goal(
        id="hundred_feeds",
        name="Master Chef",
        description="Feed your duck 100 times",
        goal_type="achievement",
        action="feed",
        target=100,
        reward_item="golden_crumb",
        reward_message="LEGENDARY: Golden Crumb!",
    ),
    Goal(
        id="hundred_pets",
        name="Cuddle Master",
        description="Pet your duck 100 times",
        goal_type="achievement",
        action="pet",
        target=100,
        reward_item="lucky_clover",
        reward_message="RARE: Four-Leaf Clover!",
    ),
    Goal(
        id="first_trade",
        name="Open for Business",
        description="Complete your first trade with a trader",
        goal_type="achievement",
        action="trade",
        target=1,
        reward_message="You struck your first deal!",
    ),
    Goal(
        id="ten_trades",
        name="Seasoned Trader",
        description="Complete 10 trades with traders",
        goal_type="achievement",
        action="trade",
        target=10,
        reward_item="coin_pouch",
        reward_message="UNCOMMON: Coin Pouch!",
    ),
]

SECRET_GOALS = [
    Goal(
        id="midnight_quack",
        name="???",
        description="Play at midnight",
        goal_type="secret",
        action="midnight_play",
        target=1,
        hidden=True,
        reward_item="shiny_pebble",
        reward_message="SECRET: Night Owl achievement!",
    ),
    Goal(
        id="triple_play",
        name="???",
        description="Play 3 times in a row",
        goal_type="secret",
        action="triple_play",
        target=1,
        hidden=True,
        reward_message="SECRET: Triple Threat!",
    ),
    Goal(
        id="patient_one",
        name="???",
        description="Wait for 5 minutes without doing anything",
        goal_type="secret",
        action="idle_wait",
        target=1,
        hidden=True,
        reward_message="SECRET: The Patient One",
    ),
    # New secret goals
    Goal(
        id="early_bird",
        name="???",
        description="Play before 6 AM",
        goal_type="secret",
        action="early_bird",
        target=1,
        hidden=True,
        reward_item="seeds",
        reward_message="SECRET: Early Bird! The duck that gets the worm!",
    ),
    Goal(
        id="bread_obsessed",
        name="???",
        description="Feed bread 10 times in one session",
        goal_type="secret",
        action="bread_feast",
        target=1,
        hidden=True,
        reward_item="fancy_bread",
        reward_message="SECRET: Bread Obsessed! Carb loading complete!",
    ),
    Goal(
        id="rainbow_witness",
        name="???",
        description="See a rainbow",
        goal_type="secret",
        action="saw_rainbow",
        target=1,
        hidden=True,
        reward_item="rainbow_crumb",
        reward_message="SECRET: Rainbow Witness! Magical!",
    ),
    Goal(
        id="visitor_friend",
        name="???",
        description="Meet 5 different visitors",
        goal_type="secret",
        action="met_visitors",
        target=5,
        hidden=True,
        reward_item="glass_marble",
        reward_message="SECRET: Social Butterfly! So many friends!",
    ),
    Goal(
        id="weather_watcher",
        name="???",
        description="Experience all weather types",
        goal_type="secret",
        action="all_weather",
        target=1,
        hidden=True,
        reward_message="SECRET: Weather Watcher! Meteorologist duck!",
    ),
    Goal(
        id="marathon_session",
        name="???",
        description="Play for 30 minutes straight",
        goal_type="secret",
        action="marathon",
        target=1,
        hidden=True,
        reward_item="worm",
        reward_message="SECRET: Marathon Duck! Such dedication!",
    ),
    Goal(
        id="perfectionist",
        name="???",
        description="Keep all needs above 80 for 10 minutes",
        goal_type="secret",
        action="perfect_care",
        target=1,
        hidden=True,
        reward_item="golden_crumb",
        reward_message="SECRET: Perfectionist! Optimal duck care achieved!",
    ),
    Goal(
        id="chatterbox",
        name="???",
        description="Talk to duck 20 times",
        goal_type="secret",
        action="talk",
        target=20,
        hidden=True,
        reward_message="SECRET: Chatterbox! Quack quack indeed!",
    ),
    Goal(
        id="collector",
        name="???",
        description="Find 10 collectibles",
        goal_type="secret",
        action="collect_item",
        target=10,
        hidden=True,
        reward_item="crystal_shard",
        reward_message="SECRET: Collector! Shiny hoarder!",
    ),
    Goal(
        id="super_lucky",
        name="???",
        description="Play on a super lucky day",
        goal_type="secret",
        action="super_lucky_day",
        target=1,
        hidden=True,
        reward_message="SECRET: Fortune's Favorite! The stars aligned!",
    ),
    Goal(
        id="storm_chaser",
        name="???",
        description="Play during a storm",
        goal_type="secret",
        action="storm_play",
        target=1,
        hidden=True,
        reward_message="SECRET: Storm Chaser! Brave duck!",
    ),
    Goal(
        id="zen_master",
        name="???",
        description="Keep duck at ecstatic mood for 5 minutes",
        goal_type="secret",
        action="zen_master",
        target=1,
        hidden=True,
        reward_item="lucky_clover",
        reward_message="SECRET: Zen Master! Maximum happiness achieved!",
    ),
    Goal(
        id="holiday_spirit",
        name="???",
        description="Play on a special holiday",
        goal_type="secret",
        action="holiday_play",
        target=1,
        hidden=True,
        reward_message="SECRET: Holiday Spirit! Festive duck!",
    ),
    Goal(
        id="week_warrior",
        name="???",
        description="Maintain a 7-day streak",
        goal_type="secret",
        action="week_streak",
        target=1,
        hidden=True,
        reward_item="feather",
        reward_message="SECRET: Week Warrior! Consistent friend!",
    ),
    Goal(
        id="month_master",
        name="???",
        description="Maintain a 30-day streak",
        goal_type="secret",
        action="month_streak",
        target=1,
        hidden=True,
        reward_item="ancient_artifact",
        reward_message="SECRET: Month Master! Legendary dedication!",
    ),
]


class GoalSystem:
    """Manages player goals and quests."""

    def __init__(self):
        self._active_goals: List[Goal] = []
        self._completed_goals: List[str] = []
        self._last_daily_reset: Optional[str] = None
        self._last_weekly_reset: Optional[str] = None
        self._last_action: str = ""
        self._action_streak: int = 0
        self._idle_time: float = 0

    def add_daily_goals(self):
        """Add random daily goals."""
        # Clear old daily goals
        self._active_goals = [g for g in self._active_goals if g.goal_type != "daily"]

        # Add 3 random daily goals
        selected = random.sample(DAILY_GOALS, min(3, len(DAILY_GOALS)))
        for template in selected:
            goal = Goal(
                id=template.id,
                name=template.name,
                description=template.description,
                goal_type=template.goal_type,
                action=template.action,
                target=template.target,
                reward_item=template.reward_item,
                reward_message=template.reward_message,
            )
            self._active_goals.append(goal)

        self._last_daily_reset = datetime.now().strftime("%Y-%m-%d")

    def add_weekly_goals(self):
        """Add weekly goals."""
        self._active_goals = [g for g in self._active_goals if g.goal_type != "weekly"]

        for template in WEEKLY_GOALS:
            goal = Goal(
                id=template.id,
                name=template.name,
                description=template.description,
                goal_type=template.goal_type,
                action=template.action,
                target=template.target,
                reward_item=template.reward_item,
                reward_message=template.reward_message,
            )
            self._active_goals.append(goal)

        self._last_weekly_reset = datetime.now().strftime("%Y-%W")

    def add_achievement_goals(self):
        """Add achievement goals that weren't completed yet."""
        for template in ACHIEVEMENT_GOALS:
            if template.id not in self._completed_goals:
                exists = any(g.id == template.id for g in self._active_goals)
                if not exists:
                    goal = Goal(
                        id=template.id,
                        name=template.name,
                        description=template.description,
                        goal_type=template.goal_type,
                        action=template.action,
                        target=template.target,
                        reward_item=template.reward_item,
                        reward_message=template.reward_message,
                    )
                    self._active_goals.append(goal)

    def update_progress(self, action: str, amount: int = 1) -> List[Goal]:
        """
        Update progress on goals that match the action.

        Returns list of newly completed goals.
        """
        completed = []

        # Track action streak for secret goals
        if action == self._last_action:
            self._action_streak += 1
        else:
            self._action_streak = 1
            self._last_action = action

        # Reset idle timer on action
        self._idle_time = 0

        # Check for triple action secret
        if self._action_streak >= 3 and action == "play":
            self._check_secret_goal("triple_play")

        # Check midnight play secret
        if action == "play":
            hour = datetime.now().hour
            if hour == 0 or hour == 23:
                self._check_secret_goal("midnight_play")

        for goal in self._active_goals:
            if goal.completed:
                continue

            if goal.action == action:
                goal.progress += amount
                if goal.progress >= goal.target:
                    goal.completed = True
                    self._completed_goals.append(goal.id)
                    completed.append(goal)

        return completed

    def update_time(self, delta_minutes: float):
        """Update time-based goals."""
        self._idle_time += delta_minutes

        # Check for patient one secret (5 minutes idle)
        if self._idle_time >= 5:
            self._check_secret_goal("idle_wait")

        # Check for daily/weekly resets
        today = datetime.now().strftime("%Y-%m-%d")
        week = datetime.now().strftime("%Y-%W")

        if self._last_daily_reset != today:
            self.add_daily_goals()

        if self._last_weekly_reset != week:
            self.add_weekly_goals()

    def _check_secret_goal(self, action: str):
        """Check and potentially unlock a secret goal."""
        for template in SECRET_GOALS:
            if template.action == action and template.id not in self._completed_goals:
                # Add and complete the secret goal
                goal = Goal(
                    id=template.id,
                    name=template.name.replace("???", template.description),
                    description=template.description,
                    goal_type=template.goal_type,
                    action=template.action,
                    target=template.target,
                    progress=template.target,
                    completed=True,
                    hidden=False,
                    reward_item=template.reward_item,
                    reward_message=template.reward_message,
                )
                self._active_goals.append(goal)
                self._completed_goals.append(goal.id)
                return goal
        return None

    def get_active_goals(self) -> List[Goal]:
        """Get all active, non-completed goals."""
        return [g for g in self._active_goals if not g.completed and not g.hidden]

    def get_completed_count(self) -> int:
        """Get number of completed goals."""
        return len(self._completed_goals)

    def get_total_count(self) -> int:
        """Get total number of goals (including hidden ones once discovered)."""
        return len(self._active_goals)

    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "active_goals": [
                {
                    "id": g.id,
                    "name": g.name,
                    "description": g.description,
                    "goal_type": g.goal_type,
                    "action": g.action,
                    "target": g.target,
                    "progress": g.progress,
                    "completed": g.completed,
                    "reward_item": g.reward_item,
                    "reward_message": g.reward_message,
                    "hidden": g.hidden,
                }
                for g in self._active_goals
            ],
            "completed_goals": self._completed_goals,
            "last_daily_reset": self._last_daily_reset,
            "last_weekly_reset": self._last_weekly_reset,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "GoalSystem":
        """Create from dictionary."""
        system = cls()
        system._completed_goals = data.get("completed_goals", [])
        system._last_daily_reset = data.get("last_daily_reset")
        system._last_weekly_reset = data.get("last_weekly_reset")

        for g_data in data.get("active_goals", []):
            goal = Goal(
                id=g_data.get("id", "unknown"),
                name=g_data.get("name", "Unknown"),
                description=g_data.get("description", ""),
                goal_type=g_data.get("goal_type", "daily"),
                action=g_data.get("action", ""),
                target=g_data.get("target", 1),
                progress=g_data.get("progress", 0),
                completed=g_data.get("completed", False),
                reward_item=g_data.get("reward_item"),
                reward_message=g_data.get("reward_message", ""),
                hidden=g_data.get("hidden", False),
            )
            system._active_goals.append(goal)

        return system


# Global instance
goal_system = GoalSystem()
