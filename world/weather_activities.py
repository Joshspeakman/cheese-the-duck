"""
Weather Activities System - Weather-specific interactions and events.
Different activities available based on current weather conditions.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random


class WeatherType(Enum):
    """Types of weather."""
    SUNNY = "sunny"
    CLOUDY = "cloudy"
    RAINY = "rainy"
    STORMY = "stormy"
    SNOWY = "snowy"
    FOGGY = "foggy"
    WINDY = "windy"
    HOT = "hot"
    COLD = "cold"


class ActivityType(Enum):
    """Types of weather activities."""
    PLAY = "play"
    EXPLORE = "explore"
    COLLECT = "collect"
    SPECIAL = "special"


@dataclass
class WeatherActivity:
    """A weather-specific activity."""
    id: str
    name: str
    description: str
    weather_types: List[WeatherType]
    activity_type: ActivityType
    duration_seconds: int = 30
    cooldown_minutes: int = 15
    coins_reward: Tuple[int, int] = (10, 30)
    xp_reward: Tuple[int, int] = (5, 15)
    special_drops: List[str] = field(default_factory=list)
    drop_chance: float = 0.1
    mood_bonus: int = 10
    ascii_animation: List[str] = field(default_factory=list)
    success_messages: List[str] = field(default_factory=list)


# Define weather activities
WEATHER_ACTIVITIES: Dict[str, WeatherActivity] = {
    # Sunny activities
    "sunbathing": WeatherActivity(
        id="sunbathing",
        name="Sunbathing",
        description="Cheese relaxes in the warm sunshine!",
        weather_types=[WeatherType.SUNNY, WeatherType.HOT],
        activity_type=ActivityType.PLAY,
        duration_seconds=20,
        cooldown_minutes=30,
        coins_reward=(15, 25),
        xp_reward=(10, 20),
        mood_bonus=20,
        ascii_animation=[
            "  * * *   ",
            "   \\|/   ",
            "  --d--   ",
            "   ~~~~   ",
            "  Ahhh... ",
        ],
        success_messages=[
            "Cheese soaks up the vitamin D!",
            "What a beautiful day for a duck!",
            "Cheese feels warm and happy!",
        ]
    ),
    
    "butterfly_chase": WeatherActivity(
        id="butterfly_chase",
        name="Chase Butterflies",
        description="Chase beautiful butterflies through the meadow!",
        weather_types=[WeatherType.SUNNY],
        activity_type=ActivityType.PLAY,
        duration_seconds=25,
        cooldown_minutes=20,
        coins_reward=(20, 40),
        xp_reward=(15, 25),
        special_drops=["butterfly_wing", "flower_petal"],
        drop_chance=0.3,
        mood_bonus=15,
        ascii_animation=[
            "  ~.  .~  ",
            "    d     ",
            "   ~~>    ",
            " *waddle* ",
        ],
        success_messages=[
            "Cheese chased 5 butterflies!",
            "Almost caught one!",
            "So many pretty colors!",
        ]
    ),
    
    # Rainy activities
    "puddle_splash": WeatherActivity(
        id="puddle_splash",
        name="Puddle Splashing",
        description="Jump and splash in rain puddles!",
        weather_types=[WeatherType.RAINY],
        activity_type=ActivityType.PLAY,
        duration_seconds=20,
        cooldown_minutes=15,
        coins_reward=(15, 30),
        xp_reward=(10, 20),
        mood_bonus=25,
        ascii_animation=[
            "   ','    ",
            "   ~d~    ",
            "  *SPLASH* ",
            "   ~~~~    ",
        ],
        success_messages=[
            "SPLASH! Water everywhere!",
            "Puddles are the best!",
            "Cheese is soaking wet and happy!",
        ]
    ),
    
    "worm_hunting": WeatherActivity(
        id="worm_hunting",
        name="Worm Hunting",
        description="Rain brings worms to the surface!",
        weather_types=[WeatherType.RAINY],
        activity_type=ActivityType.COLLECT,
        duration_seconds=30,
        cooldown_minutes=25,
        coins_reward=(25, 50),
        xp_reward=(20, 35),
        special_drops=["juicy_worm", "giant_worm"],
        drop_chance=0.5,
        mood_bonus=10,
        ascii_animation=[
            "  ','     ",
            "  d  ?    ",
            " ~~S~~    ",
            "  Found!  ",
        ],
        success_messages=[
            "Cheese found 3 juicy worms!",
            "Protein snack time!",
            "The early duck gets the worm!",
        ]
    ),
    
    "rainbow_watch": WeatherActivity(
        id="rainbow_watch",
        name="Rainbow Watching",
        description="Wait for a rainbow after the rain!",
        weather_types=[WeatherType.RAINY, WeatherType.CLOUDY],
        activity_type=ActivityType.SPECIAL,
        duration_seconds=45,
        cooldown_minutes=60,
        coins_reward=(50, 100),
        xp_reward=(30, 50),
        special_drops=["rainbow_feather"],
        drop_chance=0.2,
        mood_bonus=30,
        ascii_animation=[
            "      (=)        ",
            "  (*)     (*)   ",
            "      d         ",
            "   *amazed*     ",
        ],
        success_messages=[
            "A beautiful rainbow appeared!",
            "Cheese made a rainbow wish!",
            "Seven colors of joy!",
        ]
    ),
    
    # Snowy activities
    "snowball_play": WeatherActivity(
        id="snowball_play",
        name="Snowball Fun",
        description="Roll around and play in the snow!",
        weather_types=[WeatherType.SNOWY],
        activity_type=ActivityType.PLAY,
        duration_seconds=25,
        cooldown_minutes=20,
        coins_reward=(20, 40),
        xp_reward=(15, 30),
        mood_bonus=20,
        ascii_animation=[
            "  * * *   ",
            "    o d   ",
            "   *roll*  ",
            "  * * *   ",
        ],
        success_messages=[
            "Cheese made a snowball!",
            "Brrr but fun!",
            "Snow duck mode activated!",
        ]
    ),
    
    "snow_angel": WeatherActivity(
        id="snow_angel",
        name="Snow Duck Angel",
        description="Make a duck-shaped angel in the snow!",
        weather_types=[WeatherType.SNOWY],
        activity_type=ActivityType.SPECIAL,
        duration_seconds=15,
        cooldown_minutes=30,
        coins_reward=(30, 50),
        xp_reward=(20, 35),
        mood_bonus=25,
        ascii_animation=[
            "  *     *  ",
            "    \\d/   ",
            "    /  \\   ",
            "  *flap*   ",
        ],
        success_messages=[
            "Perfect snow duck angel!",
            "It looks just like Cheese!",
            "Art in the snow!",
        ]
    ),
    
    "icicle_collect": WeatherActivity(
        id="icicle_collect",
        name="Icicle Collection",
        description="Carefully collect pretty icicles!",
        weather_types=[WeatherType.SNOWY, WeatherType.COLD],
        activity_type=ActivityType.COLLECT,
        duration_seconds=30,
        cooldown_minutes=25,
        coins_reward=(25, 45),
        xp_reward=(15, 30),
        special_drops=["crystal_icicle", "frozen_dewdrop"],
        drop_chance=0.35,
        ascii_animation=[
            "   |||    ",
            "     |     ",
            "    d      ",
            "  *clink*  ",
        ],
        success_messages=[
            "Found some beautiful icicles!",
            "So cold and sparkly!",
            "Nature's crystals!",
        ]
    ),
    
    # Stormy activities
    "storm_watch": WeatherActivity(
        id="storm_watch",
        name="Storm Watching",
        description="Watch the dramatic storm from safety!",
        weather_types=[WeatherType.STORMY],
        activity_type=ActivityType.SPECIAL,
        duration_seconds=40,
        cooldown_minutes=45,
        coins_reward=(40, 80),
        xp_reward=(25, 45),
        mood_bonus=10,
        ascii_animation=[
            "  ! (*) !   ",
            "   ','      ",
            "  [d]       ",
            " *window*   ",
        ],
        success_messages=[
            "The storm is intense!",
            "Cheese watches from inside, cozy and dry.",
            "Nature's power is amazing!",
        ]
    ),
    
    "thunder_count": WeatherActivity(
        id="thunder_count",
        name="Count Thunder",
        description="Count the seconds between lightning and thunder!",
        weather_types=[WeatherType.STORMY],
        activity_type=ActivityType.PLAY,
        duration_seconds=30,
        cooldown_minutes=30,
        coins_reward=(30, 60),
        xp_reward=(20, 40),
        special_drops=["static_feather"],
        drop_chance=0.15,
        ascii_animation=[
            "   !      ",
            "  1...2...3",
            "   BOOM!  ",
            "   d !    ",
        ],
        success_messages=[
            "That was close! Only 3 seconds!",
            "The storm is far away now.",
            "Cheese is getting good at counting!",
        ]
    ),
    
    # Windy activities
    "kite_flying": WeatherActivity(
        id="kite_flying",
        name="Fly a Kite",
        description="The wind is perfect for kite flying!",
        weather_types=[WeatherType.WINDY],
        activity_type=ActivityType.PLAY,
        duration_seconds=35,
        cooldown_minutes=25,
        coins_reward=(25, 50),
        xp_reward=(20, 35),
        mood_bonus=20,
        ascii_animation=[
            "      <>   ",
            "     /     ",
            "    /      ",
            "   d       ",
        ],
        success_messages=[
            "The kite soars high!",
            "Look at it dance in the wind!",
            "Cheese is a master kite flyer!",
        ]
    ),
    
    "leaf_catch": WeatherActivity(
        id="leaf_catch",
        name="Catch Leaves",
        description="Catch swirling autumn leaves in the wind!",
        weather_types=[WeatherType.WINDY],
        activity_type=ActivityType.COLLECT,
        duration_seconds=25,
        cooldown_minutes=20,
        coins_reward=(20, 40),
        xp_reward=(15, 30),
        special_drops=["golden_leaf", "red_maple_leaf"],
        drop_chance=0.4,
        ascii_animation=[
            "  ~ ~ ~    ",
            "    ~~     ",
            "    d      ",
            "  *catch*  ",
        ],
        success_messages=[
            "Caught 5 colorful leaves!",
            "They're so pretty!",
            "A perfect collection!",
        ]
    ),
    
    # Foggy activities
    "fog_explore": WeatherActivity(
        id="fog_explore",
        name="Mysterious Fog Walk",
        description="Explore the mysterious foggy landscape!",
        weather_types=[WeatherType.FOGGY],
        activity_type=ActivityType.EXPLORE,
        duration_seconds=40,
        cooldown_minutes=35,
        coins_reward=(35, 70),
        xp_reward=(25, 45),
        special_drops=["mist_crystal", "fog_essence"],
        drop_chance=0.25,
        mood_bonus=5,
        ascii_animation=[
            "  ......  ",
            "  .d....  ",
            "  ...?..  ",
            " *spooky* ",
        ],
        success_messages=[
            "What was that shadow?",
            "Cheese found something in the mist!",
            "Mysterious and exciting!",
        ]
    ),
    
    # Cloudy activities
    "cloud_shapes": WeatherActivity(
        id="cloud_shapes",
        name="Cloud Watching",
        description="Find fun shapes in the clouds!",
        weather_types=[WeatherType.CLOUDY],
        activity_type=ActivityType.PLAY,
        duration_seconds=30,
        cooldown_minutes=20,
        coins_reward=(15, 30),
        xp_reward=(10, 25),
        mood_bonus=15,
        ascii_animation=[
            "  (*)(*)  ",
            "   (o o)  ",
            "    d     ",
            "  *dream* ",
        ],
        success_messages=[
            "That cloud looks like a duck!",
            "Cheese sees a giant bread loaf!",
            "So peaceful and relaxing.",
        ]
    ),
    
    # Hot weather activities
    "pond_swim": WeatherActivity(
        id="pond_swim",
        name="Cool Swim",
        description="Take a refreshing swim in the pond!",
        weather_types=[WeatherType.HOT, WeatherType.SUNNY],
        activity_type=ActivityType.PLAY,
        duration_seconds=25,
        cooldown_minutes=20,
        coins_reward=(20, 40),
        xp_reward=(15, 30),
        mood_bonus=25,
        ascii_animation=[
            "   * *    ",
            "   d~     ",
            "  ~~~~    ",
            " *splash* ",
        ],
        success_messages=[
            "So refreshing!",
            "Perfect temperature!",
            "Cheese is a natural swimmer!",
        ]
    ),
}


@dataclass
class ActivityProgress:
    """Progress for an in-progress activity."""
    activity_id: str
    started_at: str
    duration_seconds: int
    completed: bool = False


class WeatherActivitiesSystem:
    """
    System for weather-specific activities.
    """
    
    def __init__(self):
        self.activity_cooldowns: Dict[str, str] = {}  # activity_id -> last_completed
        self.current_activity: Optional[ActivityProgress] = None
        self.completed_activities: Dict[str, int] = {}  # activity_id -> times completed
        self.total_activities_done: int = 0
        self.items_collected: List[str] = []
    
    def get_available_activities(self, weather: str) -> List[WeatherActivity]:
        """Get activities available for current weather."""
        try:
            weather_type = WeatherType(weather.lower())
        except ValueError:
            weather_type = WeatherType.CLOUDY  # Default
        
        now = datetime.now()
        available = []
        
        for activity in WEATHER_ACTIVITIES.values():
            if weather_type not in activity.weather_types:
                continue
            
            # Check cooldown
            if activity.id in self.activity_cooldowns:
                last_done = datetime.fromisoformat(self.activity_cooldowns[activity.id])
                cooldown_seconds = activity.cooldown_minutes * 60
                if (now - last_done).total_seconds() < cooldown_seconds:
                    continue
            
            available.append(activity)
        
        return available
    
    def start_activity(self, activity_id: str, weather: str) -> Optional[WeatherActivity]:
        """Start a weather activity."""
        if self.current_activity:
            return None  # Already doing something
        
        available = self.get_available_activities(weather)
        activity = next((a for a in available if a.id == activity_id), None)
        
        if not activity:
            return None
        
        self.current_activity = ActivityProgress(
            activity_id=activity_id,
            started_at=datetime.now().isoformat(),
            duration_seconds=activity.duration_seconds
        )
        
        return activity
    
    def check_activity_complete(self) -> Optional[Tuple[WeatherActivity, Dict]]:
        """Check if current activity is complete and return results."""
        if not self.current_activity:
            return None
        
        started = datetime.fromisoformat(self.current_activity.started_at)
        elapsed = (datetime.now() - started).total_seconds()
        
        if elapsed < self.current_activity.duration_seconds:
            return None  # Not done yet
        
        # Complete the activity
        activity = WEATHER_ACTIVITIES.get(self.current_activity.activity_id)
        if not activity:
            self.current_activity = None
            return None
        
        # Calculate rewards
        coins = random.randint(*activity.coins_reward)
        xp = random.randint(*activity.xp_reward)
        
        # Check for special drops
        special_drop = None
        if activity.special_drops and random.random() < activity.drop_chance:
            special_drop = random.choice(activity.special_drops)
            self.items_collected.append(special_drop)
        
        message = random.choice(activity.success_messages) if activity.success_messages else f"Completed {activity.name}!"
        
        # Update tracking
        self.activity_cooldowns[activity.id] = datetime.now().isoformat()
        self.completed_activities[activity.id] = self.completed_activities.get(activity.id, 0) + 1
        self.total_activities_done += 1
        self.current_activity = None
        
        results = {
            "coins": coins,
            "xp": xp,
            "mood_bonus": activity.mood_bonus,
            "special_drop": special_drop,
            "message": message,
        }
        
        return activity, results
    
    def get_activity_progress(self) -> Optional[Tuple[float, WeatherActivity]]:
        """Get progress of current activity (0.0 to 1.0)."""
        if not self.current_activity:
            return None
        
        activity = WEATHER_ACTIVITIES.get(self.current_activity.activity_id)
        if not activity:
            return None
        
        started = datetime.fromisoformat(self.current_activity.started_at)
        elapsed = (datetime.now() - started).total_seconds()
        progress = min(1.0, elapsed / self.current_activity.duration_seconds)
        
        return progress, activity
    
    def render_activity_selection(self, weather: str) -> List[str]:
        """Render available activities for selection."""
        lines = [
            "+===============================================+",
            f"|      *️ WEATHER ACTIVITIES ({weather.upper()})        |",
            "+===============================================+",
        ]
        
        activities = self.get_available_activities(weather)
        
        if not activities:
            lines.append("|  No activities available right now!           |")
            lines.append("|  Check back when the weather changes,         |")
            lines.append("|  or wait for cooldowns to reset.              |")
        else:
            for i, activity in enumerate(activities, 1):
                lines.append(f"|  [{i}] {activity.name:<35}  |")
                desc = activity.description[:40]
                lines.append(f"|      {desc:<40}  |")
                lines.append(f"|      (t) {activity.duration_seconds}s  $ {activity.coins_reward[0]}-{activity.coins_reward[1]}  * {activity.xp_reward[0]}-{activity.xp_reward[1]} XP |")
                lines.append("|                                               |")
        
        lines.extend([
            "+===============================================+",
            "|  Select an activity number or [B] to go back  |",
            "+===============================================+",
        ])
        
        return lines
    
    def render_activity_progress(self) -> List[str]:
        """Render current activity in progress."""
        progress_data = self.get_activity_progress()
        if not progress_data:
            return []
        
        progress, activity = progress_data
        
        # Progress bar
        bar_width = 30
        filled = int(progress * bar_width)
        bar = "#" * filled + "." * (bar_width - filled)
        
        lines = [
            "+===============================================+",
            f"|      (o) {activity.name.upper():<30}  |",
            "+===============================================+",
        ]
        
        # Add animation
        if activity.ascii_animation:
            for anim_line in activity.ascii_animation:
                lines.append(f"|  {anim_line:^43}  |")
        
        lines.extend([
            "|                                               |",
            f"|  [{bar}]  |",
            f"|  {int(progress * 100):>42}%  |",
            "+===============================================+",
        ])
        
        return lines
    
    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "activity_cooldowns": self.activity_cooldowns,
            "completed_activities": self.completed_activities,
            "total_activities_done": self.total_activities_done,
            "items_collected": self.items_collected[-50:],  # Keep last 50
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "WeatherActivitiesSystem":
        """Create from dictionary."""
        system = cls()
        system.activity_cooldowns = data.get("activity_cooldowns", {})
        system.completed_activities = data.get("completed_activities", {})
        system.total_activities_done = data.get("total_activities_done", 0)
        system.items_collected = data.get("items_collected", [])
        return system


# Global instance
weather_activities_system = WeatherActivitiesSystem()
