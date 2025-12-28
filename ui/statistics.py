"""
Statistics System - Comprehensive game statistics and analytics.
Tracks all player actions, achievements, and progress metrics.
"""
from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
import json


class StatCategory(Enum):
    """Categories of statistics."""
    GENERAL = "general"
    CARE = "care"
    ACTIVITIES = "activities"
    ECONOMY = "economy"
    SOCIAL = "social"
    EXPLORATION = "exploration"
    ACHIEVEMENTS = "achievements"
    TIME = "time"


@dataclass
class StatRecord:
    """A record of a stat with history."""
    current_value: int = 0
    all_time_total: int = 0
    daily_values: Dict[str, int] = field(default_factory=dict)  # date -> value
    weekly_values: Dict[str, int] = field(default_factory=dict)  # week -> value
    monthly_values: Dict[str, int] = field(default_factory=dict)  # month -> value
    peak_value: int = 0
    peak_date: str = ""
    last_updated: str = ""


class StatisticsSystem:
    """
    Comprehensive statistics tracking system.
    """
    
    def __init__(self):
        # General Stats
        self.total_playtime_minutes: int = 0
        self.session_count: int = 0
        self.current_session_start: Optional[str] = None
        self.longest_session_minutes: int = 0
        self.first_played: str = ""
        self.last_played: str = ""
        
        # Care Stats
        self.times_fed: StatRecord = StatRecord()
        self.times_played: StatRecord = StatRecord()
        self.times_petted: StatRecord = StatRecord()
        self.times_talked: StatRecord = StatRecord()
        self.times_cleaned: StatRecord = StatRecord()
        self.times_put_to_sleep: StatRecord = StatRecord()
        
        # Activity Stats
        self.minigames_played: StatRecord = StatRecord()
        self.minigames_won: StatRecord = StatRecord()
        self.fish_caught: StatRecord = StatRecord()
        self.rare_fish_caught: int = 0
        self.legendary_fish_caught: int = 0
        self.plants_grown: StatRecord = StatRecord()
        self.plants_harvested: StatRecord = StatRecord()
        self.treasures_found: StatRecord = StatRecord()
        self.tricks_performed: StatRecord = StatRecord()
        self.perfect_performances: int = 0
        
        # Economy Stats
        self.coins_earned: StatRecord = StatRecord()
        self.coins_spent: StatRecord = StatRecord()
        self.most_coins_held: int = 0
        self.items_bought: int = 0
        self.items_sold: int = 0
        
        # XP Stats
        self.xp_earned: StatRecord = StatRecord()
        self.levels_gained: int = 0
        self.current_level: int = 1
        self.highest_level: int = 1
        
        # Social Stats
        self.friends_made: int = 0
        self.gifts_given: int = 0
        self.gifts_received: int = 0
        self.visitors_hosted: int = 0
        self.best_friendship_level: int = 0
        
        # Exploration Stats
        self.areas_discovered: int = 0
        self.total_explorations: int = 0
        self.secrets_found: int = 0
        
        # Quest Stats
        self.quests_completed: int = 0
        self.quests_failed: int = 0
        self.quest_chains_completed: int = 0
        
        # Challenge Stats
        self.daily_challenges_completed: int = 0
        self.weekly_challenges_completed: int = 0
        self.challenge_streak_best: int = 0
        
        # Festival Stats
        self.festivals_participated: int = 0
        self.festival_rewards_earned: int = 0
        
        # Collection Stats
        self.collectibles_owned: int = 0
        self.sets_completed: int = 0
        self.shiny_collectibles: int = 0
        
        # Duck Stats
        self.duck_age_days: int = 0
        self.growth_stages_reached: int = 1
        self.mood_history: Dict[str, int] = {}  # mood -> times
        self.happiest_day: str = ""
        self.titles_earned: int = 0
        self.outfits_collected: int = 0
        self.decorations_placed: int = 0
        
        # Streak Stats
        self.current_login_streak: int = 0
        self.best_login_streak: int = 0
        self.last_login_date: str = ""
        
        # Milestones
        self.milestones_reached: List[str] = []
    
    def start_session(self):
        """Start a new play session."""
        now = datetime.now().isoformat()
        self.current_session_start = now
        self.session_count += 1
        self.last_played = now
        
        if not self.first_played:
            self.first_played = now
        
        # Update login streak
        today = date.today().isoformat()
        if self.last_login_date:
            yesterday = (date.today() - timedelta(days=1)).isoformat()
            if self.last_login_date == yesterday:
                self.current_login_streak += 1
            elif self.last_login_date != today:
                self.current_login_streak = 1
        else:
            self.current_login_streak = 1
        
        self.last_login_date = today
        
        if self.current_login_streak > self.best_login_streak:
            self.best_login_streak = self.current_login_streak
    
    def end_session(self):
        """End the current session and record playtime."""
        if not self.current_session_start:
            return
        
        start = datetime.fromisoformat(self.current_session_start)
        duration = int((datetime.now() - start).total_seconds() / 60)
        
        self.total_playtime_minutes += duration
        
        if duration > self.longest_session_minutes:
            self.longest_session_minutes = duration
        
        self.current_session_start = None
    
    def increment_stat(self, stat_name: str, amount: int = 1):
        """Increment a stat record."""
        stat = getattr(self, stat_name, None)
        if not isinstance(stat, StatRecord):
            return
        
        today = date.today().isoformat()
        week = f"{date.today().year}-W{date.today().isocalendar()[1]}"
        month = date.today().strftime("%Y-%m")
        
        stat.current_value += amount
        stat.all_time_total += amount
        stat.daily_values[today] = stat.daily_values.get(today, 0) + amount
        stat.weekly_values[week] = stat.weekly_values.get(week, 0) + amount
        stat.monthly_values[month] = stat.monthly_values.get(month, 0) + amount
        stat.last_updated = datetime.now().isoformat()
        
        if stat.current_value > stat.peak_value:
            stat.peak_value = stat.current_value
            stat.peak_date = today
    
    def get_stat_summary(self, stat_name: str) -> Dict:
        """Get summary of a stat."""
        stat = getattr(self, stat_name, None)
        if not isinstance(stat, StatRecord):
            return {}
        
        today = date.today().isoformat()
        week = f"{date.today().year}-W{date.today().isocalendar()[1]}"
        month = date.today().strftime("%Y-%m")
        
        return {
            "total": stat.all_time_total,
            "today": stat.daily_values.get(today, 0),
            "this_week": stat.weekly_values.get(week, 0),
            "this_month": stat.monthly_values.get(month, 0),
            "peak": stat.peak_value,
            "peak_date": stat.peak_date,
        }
    
    def get_overview_stats(self) -> Dict:
        """Get an overview of key statistics."""
        return {
            "total_playtime": self.format_playtime(self.total_playtime_minutes),
            "sessions": self.session_count,
            "login_streak": self.current_login_streak,
            "best_streak": self.best_login_streak,
            "level": self.current_level,
            "total_xp": self.xp_earned.all_time_total,
            "total_coins_earned": self.coins_earned.all_time_total,
            "coins_spent": self.coins_spent.all_time_total,
            "care_actions": (
                self.times_fed.all_time_total +
                self.times_played.all_time_total +
                self.times_petted.all_time_total +
                self.times_talked.all_time_total
            ),
            "minigames": self.minigames_played.all_time_total,
            "fish_caught": self.fish_caught.all_time_total,
            "plants_grown": self.plants_grown.all_time_total,
            "treasures": self.treasures_found.all_time_total,
            "quests": self.quests_completed,
            "achievements": len(self.milestones_reached),
        }
    
    def format_playtime(self, minutes: int) -> str:
        """Format playtime as human-readable string."""
        hours = minutes // 60
        mins = minutes % 60
        
        if hours > 24:
            days = hours // 24
            hours = hours % 24
            return f"{days}d {hours}h {mins}m"
        elif hours > 0:
            return f"{hours}h {mins}m"
        else:
            return f"{mins}m"
    
    def check_milestones(self) -> List[str]:
        """Check for new milestone achievements."""
        new_milestones = []
        
        # Playtime milestones
        playtime_milestones = [60, 300, 600, 1440, 4320, 10080]  # 1h, 5h, 10h, 1d, 3d, 1w
        for mins in playtime_milestones:
            milestone = f"playtime_{mins}"
            if self.total_playtime_minutes >= mins and milestone not in self.milestones_reached:
                self.milestones_reached.append(milestone)
                new_milestones.append(f"Played for {self.format_playtime(mins)}!")
        
        # Login streak milestones
        streak_milestones = [7, 30, 100, 365]
        for days in streak_milestones:
            milestone = f"streak_{days}"
            if self.current_login_streak >= days and milestone not in self.milestones_reached:
                self.milestones_reached.append(milestone)
                new_milestones.append(f"{days}-day login streak!")
        
        # Care milestones
        care_milestones = [10, 50, 100, 500, 1000]
        for count in care_milestones:
            if self.times_fed.all_time_total >= count:
                milestone = f"fed_{count}"
                if milestone not in self.milestones_reached:
                    self.milestones_reached.append(milestone)
                    new_milestones.append(f"Fed duck {count} times!")
        
        # Fish milestones
        fish_milestones = [10, 50, 100, 500]
        for count in fish_milestones:
            if self.fish_caught.all_time_total >= count:
                milestone = f"fish_{count}"
                if milestone not in self.milestones_reached:
                    self.milestones_reached.append(milestone)
                    new_milestones.append(f"Caught {count} fish!")
        
        # Coin milestones
        coin_milestones = [1000, 10000, 100000, 1000000]
        for amount in coin_milestones:
            if self.coins_earned.all_time_total >= amount:
                milestone = f"coins_{amount}"
                if milestone not in self.milestones_reached:
                    self.milestones_reached.append(milestone)
                    new_milestones.append(f"Earned {amount:,} coins!")
        
        return new_milestones
    
    def record_mood(self, mood: str):
        """Record current duck mood."""
        self.mood_history[mood] = self.mood_history.get(mood, 0) + 1
    
    def get_mood_distribution(self) -> Dict[str, float]:
        """Get percentage distribution of moods."""
        total = sum(self.mood_history.values())
        if total == 0:
            return {}
        
        return {
            mood: (count / total) * 100
            for mood, count in self.mood_history.items()
        }
    
    def render_stats_screen(self, page: int = 1) -> List[str]:
        """Render the statistics screen."""
        lines = [
            "╔═══════════════════════════════════════════════╗",
            "║             📊 STATISTICS 📊                  ║",
            "╠═══════════════════════════════════════════════╣",
        ]
        
        if page == 1:  # Overview
            lines.append("║  📋 OVERVIEW                                  ║")
            lines.append(f"║  Total Playtime: {self.format_playtime(self.total_playtime_minutes):^24}  ║")
            lines.append(f"║  Sessions: {self.session_count:^30}  ║")
            lines.append(f"║  Current Streak: {self.current_login_streak:^24} days ║")
            lines.append(f"║  Best Streak: {self.best_login_streak:^27} days ║")
            lines.append("╠═══════════════════════════════════════════════╣")
            lines.append("║  🎮 LEVEL & XP                                ║")
            lines.append(f"║  Level: {self.current_level:^33}  ║")
            lines.append(f"║  Total XP: {self.xp_earned.all_time_total:^30}  ║")
            lines.append(f"║  Levels Gained: {self.levels_gained:^25}  ║")
        
        elif page == 2:  # Care stats
            lines.append("║  💕 CARE ACTIONS                              ║")
            lines.append(f"║  Times Fed: {self.times_fed.all_time_total:^29}  ║")
            lines.append(f"║  Times Played: {self.times_played.all_time_total:^26}  ║")
            lines.append(f"║  Times Petted: {self.times_petted.all_time_total:^26}  ║")
            lines.append(f"║  Times Talked: {self.times_talked.all_time_total:^26}  ║")
            lines.append(f"║  Times Cleaned: {self.times_cleaned.all_time_total:^25}  ║")
            lines.append("╠═══════════════════════════════════════════════╣")
            lines.append("║  TODAY:                                       ║")
            today = date.today().isoformat()
            lines.append(f"║  Fed: {self.times_fed.daily_values.get(today, 0)}  Played: {self.times_played.daily_values.get(today, 0)}  Pet: {self.times_petted.daily_values.get(today, 0):^16}  ║")
        
        elif page == 3:  # Activities
            lines.append("║  🎯 ACTIVITIES                                ║")
            lines.append(f"║  Minigames Played: {self.minigames_played.all_time_total:^22}  ║")
            lines.append(f"║  Minigames Won: {self.minigames_won.all_time_total:^25}  ║")
            lines.append(f"║  Fish Caught: {self.fish_caught.all_time_total:^27}  ║")
            lines.append(f"║  Rare Fish: {self.rare_fish_caught:^29}  ║")
            lines.append(f"║  Legendary Fish: {self.legendary_fish_caught:^24}  ║")
            lines.append(f"║  Plants Grown: {self.plants_grown.all_time_total:^26}  ║")
            lines.append(f"║  Treasures Found: {self.treasures_found.all_time_total:^23}  ║")
            lines.append(f"║  Tricks Performed: {self.tricks_performed.all_time_total:^22}  ║")
        
        elif page == 4:  # Economy
            lines.append("║  💰 ECONOMY                                   ║")
            lines.append(f"║  Total Coins Earned: {self.coins_earned.all_time_total:^20}  ║")
            lines.append(f"║  Total Coins Spent: {self.coins_spent.all_time_total:^21}  ║")
            lines.append(f"║  Most Coins Held: {self.most_coins_held:^23}  ║")
            lines.append(f"║  Items Bought: {self.items_bought:^26}  ║")
            lines.append(f"║  Items Sold: {self.items_sold:^28}  ║")
            lines.append("╠═══════════════════════════════════════════════╣")
            today = date.today().isoformat()
            earned_today = self.coins_earned.daily_values.get(today, 0)
            spent_today = self.coins_spent.daily_values.get(today, 0)
            lines.append(f"║  Today: +{earned_today} / -{spent_today:^26}  ║")
        
        elif page == 5:  # Social & Quests
            lines.append("║  👥 SOCIAL                                    ║")
            lines.append(f"║  Friends Made: {self.friends_made:^26}  ║")
            lines.append(f"║  Gifts Given: {self.gifts_given:^27}  ║")
            lines.append(f"║  Gifts Received: {self.gifts_received:^24}  ║")
            lines.append(f"║  Visitors Hosted: {self.visitors_hosted:^23}  ║")
            lines.append("╠═══════════════════════════════════════════════╣")
            lines.append("║  📜 QUESTS                                    ║")
            lines.append(f"║  Quests Completed: {self.quests_completed:^22}  ║")
            lines.append(f"║  Daily Challenges: {self.daily_challenges_completed:^22}  ║")
            lines.append(f"║  Weekly Challenges: {self.weekly_challenges_completed:^21}  ║")
        
        lines.extend([
            "╠═══════════════════════════════════════════════╣",
            f"║  Page {page}/5  [←/→ to navigate]                  ║",
            "╚═══════════════════════════════════════════════╝",
        ])
        
        return lines
    
    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        def stat_to_dict(stat: StatRecord) -> dict:
            return {
                "current_value": stat.current_value,
                "all_time_total": stat.all_time_total,
                "daily_values": dict(list(stat.daily_values.items())[-30:]),  # Keep last 30 days
                "weekly_values": dict(list(stat.weekly_values.items())[-12:]),  # Keep last 12 weeks
                "monthly_values": dict(list(stat.monthly_values.items())[-12:]),  # Keep last 12 months
                "peak_value": stat.peak_value,
                "peak_date": stat.peak_date,
                "last_updated": stat.last_updated,
            }
        
        return {
            "total_playtime_minutes": self.total_playtime_minutes,
            "session_count": self.session_count,
            "longest_session_minutes": self.longest_session_minutes,
            "first_played": self.first_played,
            "last_played": self.last_played,
            
            "times_fed": stat_to_dict(self.times_fed),
            "times_played": stat_to_dict(self.times_played),
            "times_petted": stat_to_dict(self.times_petted),
            "times_talked": stat_to_dict(self.times_talked),
            "times_cleaned": stat_to_dict(self.times_cleaned),
            "times_put_to_sleep": stat_to_dict(self.times_put_to_sleep),
            
            "minigames_played": stat_to_dict(self.minigames_played),
            "minigames_won": stat_to_dict(self.minigames_won),
            "fish_caught": stat_to_dict(self.fish_caught),
            "rare_fish_caught": self.rare_fish_caught,
            "legendary_fish_caught": self.legendary_fish_caught,
            "plants_grown": stat_to_dict(self.plants_grown),
            "plants_harvested": stat_to_dict(self.plants_harvested),
            "treasures_found": stat_to_dict(self.treasures_found),
            "tricks_performed": stat_to_dict(self.tricks_performed),
            "perfect_performances": self.perfect_performances,
            
            "coins_earned": stat_to_dict(self.coins_earned),
            "coins_spent": stat_to_dict(self.coins_spent),
            "most_coins_held": self.most_coins_held,
            "items_bought": self.items_bought,
            "items_sold": self.items_sold,
            
            "xp_earned": stat_to_dict(self.xp_earned),
            "levels_gained": self.levels_gained,
            "current_level": self.current_level,
            "highest_level": self.highest_level,
            
            "friends_made": self.friends_made,
            "gifts_given": self.gifts_given,
            "gifts_received": self.gifts_received,
            "visitors_hosted": self.visitors_hosted,
            "best_friendship_level": self.best_friendship_level,
            
            "areas_discovered": self.areas_discovered,
            "total_explorations": self.total_explorations,
            "secrets_found": self.secrets_found,
            
            "quests_completed": self.quests_completed,
            "quests_failed": self.quests_failed,
            "quest_chains_completed": self.quest_chains_completed,
            
            "daily_challenges_completed": self.daily_challenges_completed,
            "weekly_challenges_completed": self.weekly_challenges_completed,
            "challenge_streak_best": self.challenge_streak_best,
            
            "festivals_participated": self.festivals_participated,
            "festival_rewards_earned": self.festival_rewards_earned,
            
            "collectibles_owned": self.collectibles_owned,
            "sets_completed": self.sets_completed,
            "shiny_collectibles": self.shiny_collectibles,
            
            "duck_age_days": self.duck_age_days,
            "growth_stages_reached": self.growth_stages_reached,
            "mood_history": self.mood_history,
            "happiest_day": self.happiest_day,
            "titles_earned": self.titles_earned,
            "outfits_collected": self.outfits_collected,
            "decorations_placed": self.decorations_placed,
            
            "current_login_streak": self.current_login_streak,
            "best_login_streak": self.best_login_streak,
            "last_login_date": self.last_login_date,
            
            "milestones_reached": self.milestones_reached,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "StatisticsSystem":
        """Create from dictionary."""
        def dict_to_stat(d: dict) -> StatRecord:
            return StatRecord(
                current_value=d.get("current_value", 0),
                all_time_total=d.get("all_time_total", 0),
                daily_values=d.get("daily_values", {}),
                weekly_values=d.get("weekly_values", {}),
                monthly_values=d.get("monthly_values", {}),
                peak_value=d.get("peak_value", 0),
                peak_date=d.get("peak_date", ""),
                last_updated=d.get("last_updated", ""),
            )
        
        system = cls()
        
        system.total_playtime_minutes = data.get("total_playtime_minutes", 0)
        system.session_count = data.get("session_count", 0)
        system.longest_session_minutes = data.get("longest_session_minutes", 0)
        system.first_played = data.get("first_played", "")
        system.last_played = data.get("last_played", "")
        
        if "times_fed" in data:
            system.times_fed = dict_to_stat(data["times_fed"])
        if "times_played" in data:
            system.times_played = dict_to_stat(data["times_played"])
        if "times_petted" in data:
            system.times_petted = dict_to_stat(data["times_petted"])
        if "times_talked" in data:
            system.times_talked = dict_to_stat(data["times_talked"])
        if "times_cleaned" in data:
            system.times_cleaned = dict_to_stat(data["times_cleaned"])
        
        if "minigames_played" in data:
            system.minigames_played = dict_to_stat(data["minigames_played"])
        if "minigames_won" in data:
            system.minigames_won = dict_to_stat(data["minigames_won"])
        if "fish_caught" in data:
            system.fish_caught = dict_to_stat(data["fish_caught"])
        system.rare_fish_caught = data.get("rare_fish_caught", 0)
        system.legendary_fish_caught = data.get("legendary_fish_caught", 0)
        if "plants_grown" in data:
            system.plants_grown = dict_to_stat(data["plants_grown"])
        if "treasures_found" in data:
            system.treasures_found = dict_to_stat(data["treasures_found"])
        if "tricks_performed" in data:
            system.tricks_performed = dict_to_stat(data["tricks_performed"])
        system.perfect_performances = data.get("perfect_performances", 0)
        
        if "coins_earned" in data:
            system.coins_earned = dict_to_stat(data["coins_earned"])
        if "coins_spent" in data:
            system.coins_spent = dict_to_stat(data["coins_spent"])
        system.most_coins_held = data.get("most_coins_held", 0)
        system.items_bought = data.get("items_bought", 0)
        system.items_sold = data.get("items_sold", 0)
        
        if "xp_earned" in data:
            system.xp_earned = dict_to_stat(data["xp_earned"])
        system.levels_gained = data.get("levels_gained", 0)
        system.current_level = data.get("current_level", 1)
        system.highest_level = data.get("highest_level", 1)
        
        system.friends_made = data.get("friends_made", 0)
        system.gifts_given = data.get("gifts_given", 0)
        system.gifts_received = data.get("gifts_received", 0)
        system.visitors_hosted = data.get("visitors_hosted", 0)
        system.best_friendship_level = data.get("best_friendship_level", 0)
        
        system.areas_discovered = data.get("areas_discovered", 0)
        system.total_explorations = data.get("total_explorations", 0)
        system.secrets_found = data.get("secrets_found", 0)
        
        system.quests_completed = data.get("quests_completed", 0)
        system.quests_failed = data.get("quests_failed", 0)
        system.quest_chains_completed = data.get("quest_chains_completed", 0)
        
        system.daily_challenges_completed = data.get("daily_challenges_completed", 0)
        system.weekly_challenges_completed = data.get("weekly_challenges_completed", 0)
        system.challenge_streak_best = data.get("challenge_streak_best", 0)
        
        system.festivals_participated = data.get("festivals_participated", 0)
        system.festival_rewards_earned = data.get("festival_rewards_earned", 0)
        
        system.collectibles_owned = data.get("collectibles_owned", 0)
        system.sets_completed = data.get("sets_completed", 0)
        system.shiny_collectibles = data.get("shiny_collectibles", 0)
        
        system.duck_age_days = data.get("duck_age_days", 0)
        system.growth_stages_reached = data.get("growth_stages_reached", 1)
        system.mood_history = data.get("mood_history", {})
        system.happiest_day = data.get("happiest_day", "")
        system.titles_earned = data.get("titles_earned", 0)
        system.outfits_collected = data.get("outfits_collected", 0)
        system.decorations_placed = data.get("decorations_placed", 0)
        
        system.current_login_streak = data.get("current_login_streak", 0)
        system.best_login_streak = data.get("best_login_streak", 0)
        system.last_login_date = data.get("last_login_date", "")
        
        system.milestones_reached = data.get("milestones_reached", [])
        
        return system


# Global statistics system instance
statistics_system = StatisticsSystem()
