"""
Seasonal Festivals System - Special holiday events and celebrations.
Features unique activities, decorations, and limited-time rewards.
"""
from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random


class FestivalType(Enum):
    """Types of seasonal festivals."""
    SPRING_BLOOM = "spring_bloom"
    SUMMER_SPLASH = "summer_splash"
    AUTUMN_HARVEST = "autumn_harvest"
    WINTER_WONDER = "winter_wonder"
    DUCK_DAY = "duck_day"
    LOVE_FESTIVAL = "love_festival"
    STARLIGHT = "starlight"
    HARVEST_MOON = "harvest_moon"


@dataclass
class FestivalReward:
    """A reward from participating in a festival."""
    name: str
    description: str
    item_type: str  # cosmetic, consumable, decoration, currency
    rarity: str
    xp_value: int = 0
    coin_value: int = 0


@dataclass
class FestivalActivity:
    """A festival-specific activity."""
    id: str
    name: str
    description: str
    participation_points: int
    cooldown_minutes: int
    max_daily: int
    rewards: List[FestivalReward]


@dataclass
class Festival:
    """A seasonal festival event."""
    id: str
    name: str
    description: str
    festival_type: FestivalType
    start_month: int
    start_day: int
    duration_days: int
    theme_color: str
    activities: List[FestivalActivity]
    exclusive_rewards: List[FestivalReward]
    decorations: List[str]
    special_npc: Optional[str] = None
    music_theme: Optional[str] = None


@dataclass
class FestivalProgress:
    """Player's progress in a festival."""
    festival_id: str
    year: int
    participation_points: int = 0
    activities_completed: Dict[str, int] = field(default_factory=dict)
    rewards_claimed: List[str] = field(default_factory=list)
    daily_activities: Dict[str, int] = field(default_factory=dict)
    last_activity_date: str = ""


# Festival Definitions
FESTIVALS: Dict[str, Festival] = {
    "spring_bloom": Festival(
        id="spring_bloom",
        name="* Spring Bloom Festival",
        description="Celebrate the return of spring with flowers, butterflies, and new beginnings!",
        festival_type=FestivalType.SPRING_BLOOM,
        start_month=3,
        start_day=20,
        duration_days=14,
        theme_color="pink",
        activities=[
            FestivalActivity(
                id="plant_flower",
                name="Plant a Festival Flower",
                description="Plant special spring flowers in the festival garden",
                participation_points=15,
                cooldown_minutes=30,
                max_daily=5,
                rewards=[
                    FestivalReward("Spring Petal", "A delicate spring petal", "consumable", "common", xp_value=10),
                ],
            ),
            FestivalActivity(
                id="catch_butterfly",
                name="Butterfly Catching",
                description="Catch beautiful spring butterflies",
                participation_points=20,
                cooldown_minutes=45,
                max_daily=3,
                rewards=[
                    FestivalReward("Butterfly Wing", "A shimmering butterfly wing", "material", "uncommon", xp_value=20),
                ],
            ),
            FestivalActivity(
                id="flower_crown",
                name="Make a Flower Crown",
                description="Craft a beautiful flower crown",
                participation_points=30,
                cooldown_minutes=60,
                max_daily=2,
                rewards=[
                    FestivalReward("Flower Crown", "A wearable flower crown", "cosmetic", "rare", xp_value=35),
                ],
            ),
        ],
        exclusive_rewards=[
            FestivalReward("Spring Duck Costume", "A flowery spring outfit", "cosmetic", "epic", xp_value=100),
            FestivalReward("Cherry Blossom Hat", "A hat with cherry blossoms", "cosmetic", "rare", xp_value=50),
            FestivalReward("Spring Spirit Badge", "Proof of spring celebration", "achievement", "legendary", xp_value=150),
        ],
        decorations=["cherry_blossoms", "flower_garlands", "butterfly_lights", "spring_banners"],
        special_npc="Blossom the Spring Fairy Duck",
    ),
    
    "summer_splash": Festival(
        id="summer_splash",
        name="- Summer Splash Festival",
        description="Dive into summer fun with beach activities and water games!",
        festival_type=FestivalType.SUMMER_SPLASH,
        start_month=6,
        start_day=21,
        duration_days=14,
        theme_color="cyan",
        activities=[
            FestivalActivity(
                id="build_sandcastle",
                name="Build a Sandcastle",
                description="Create an epic sandcastle on the beach",
                participation_points=20,
                cooldown_minutes=45,
                max_daily=4,
                rewards=[
                    FestivalReward("Seashell", "A beautiful seashell", "material", "common", xp_value=10),
                ],
            ),
            FestivalActivity(
                id="splash_contest",
                name="Splash Contest",
                description="Compete to make the biggest splash!",
                participation_points=25,
                cooldown_minutes=60,
                max_daily=3,
                rewards=[
                    FestivalReward("Splash Trophy", "Winner of the splash contest", "decoration", "uncommon", xp_value=25),
                ],
            ),
            FestivalActivity(
                id="sunset_watch",
                name="Watch the Sunset",
                description="Enjoy a beautiful summer sunset",
                participation_points=15,
                cooldown_minutes=120,
                max_daily=1,
                rewards=[
                    FestivalReward("Sunset Photo", "A gorgeous sunset photo", "keepsake", "rare", xp_value=40),
                ],
            ),
        ],
        exclusive_rewards=[
            FestivalReward("Beach Duck Costume", "Tropical summer outfit", "cosmetic", "epic", xp_value=100),
            FestivalReward("Surfboard", "A rad surfboard", "cosmetic", "rare", xp_value=60),
            FestivalReward("Summer Spirit Badge", "Proof of summer fun", "achievement", "legendary", xp_value=150),
        ],
        decorations=["palm_trees", "beach_umbrellas", "sand_dunes", "wave_decorations"],
        special_npc="Sunny the Lifeguard Duck",
    ),
    
    "autumn_harvest": Festival(
        id="autumn_harvest",
        name="f Autumn Harvest Festival",
        description="Gather the bounty of fall with harvesting, cooking, and cozy activities!",
        festival_type=FestivalType.AUTUMN_HARVEST,
        start_month=9,
        start_day=22,
        duration_days=14,
        theme_color="orange",
        activities=[
            FestivalActivity(
                id="harvest_pumpkin",
                name="Harvest Pumpkins",
                description="Pick the perfect pumpkin from the patch",
                participation_points=20,
                cooldown_minutes=40,
                max_daily=4,
                rewards=[
                    FestivalReward("Pumpkin", "A round orange pumpkin", "material", "common", xp_value=15),
                ],
            ),
            FestivalActivity(
                id="apple_picking",
                name="Apple Picking",
                description="Pick fresh apples from the orchard",
                participation_points=15,
                cooldown_minutes=30,
                max_daily=5,
                rewards=[
                    FestivalReward("Fresh Apple", "A crisp autumn apple", "consumable", "common", xp_value=10),
                ],
            ),
            FestivalActivity(
                id="leaf_pile",
                name="Jump in Leaf Pile",
                description="Jump into a colorful pile of autumn leaves!",
                participation_points=10,
                cooldown_minutes=20,
                max_daily=6,
                rewards=[
                    FestivalReward("Autumn Leaf", "A colorful fall leaf", "material", "common", xp_value=5),
                ],
            ),
            FestivalActivity(
                id="bake_pie",
                name="Bake a Pie",
                description="Bake a delicious autumn pie",
                participation_points=35,
                cooldown_minutes=90,
                max_daily=2,
                rewards=[
                    FestivalReward("Homemade Pie", "A delicious homemade pie", "consumable", "rare", xp_value=45),
                ],
            ),
        ],
        exclusive_rewards=[
            FestivalReward("Scarecrow Costume", "A festive scarecrow outfit", "cosmetic", "epic", xp_value=100),
            FestivalReward("Autumn Wreath Hat", "A hat with autumn leaves", "cosmetic", "rare", xp_value=55),
            FestivalReward("Harvest Spirit Badge", "Proof of autumn bounty", "achievement", "legendary", xp_value=150),
        ],
        decorations=["hay_bales", "pumpkin_stacks", "corn_stalks", "autumn_garlands"],
        special_npc="Maple the Farmer Duck",
    ),
    
    "winter_wonder": Festival(
        id="winter_wonder",
        name="* Winter Wonderland Festival",
        description="Experience the magic of winter with snow, gifts, and warm gatherings!",
        festival_type=FestivalType.WINTER_WONDER,
        start_month=12,
        start_day=21,
        duration_days=14,
        theme_color="white",
        activities=[
            FestivalActivity(
                id="build_snowduck",
                name="Build a Snow Duck",
                description="Build a duck-shaped snowman",
                participation_points=25,
                cooldown_minutes=45,
                max_daily=3,
                rewards=[
                    FestivalReward("Snowball", "A perfectly packed snowball", "material", "common", xp_value=10),
                ],
            ),
            FestivalActivity(
                id="ice_skating",
                name="Ice Skating",
                description="Glide across the frozen pond",
                participation_points=20,
                cooldown_minutes=40,
                max_daily=4,
                rewards=[
                    FestivalReward("Ice Crystal", "A sparkling ice crystal", "material", "uncommon", xp_value=20),
                ],
            ),
            FestivalActivity(
                id="hot_cocoa",
                name="Sip Hot Cocoa",
                description="Warm up with delicious hot cocoa",
                participation_points=15,
                cooldown_minutes=30,
                max_daily=5,
                rewards=[
                    FestivalReward("Warmth", "A cozy feeling inside", "buff", "common", xp_value=10),
                ],
            ),
            FestivalActivity(
                id="gift_exchange",
                name="Gift Exchange",
                description="Exchange presents with friends",
                participation_points=40,
                cooldown_minutes=120,
                max_daily=1,
                rewards=[
                    FestivalReward("Mystery Gift", "A wrapped mystery present", "mystery", "rare", xp_value=50),
                ],
            ),
        ],
        exclusive_rewards=[
            FestivalReward("Winter Coat Costume", "A warm festive winter outfit", "cosmetic", "epic", xp_value=100),
            FestivalReward("Snowflake Crown", "A crown of eternal snowflakes", "cosmetic", "rare", xp_value=65),
            FestivalReward("Winter Spirit Badge", "Proof of winter magic", "achievement", "legendary", xp_value=150),
        ],
        decorations=["snowflakes", "ice_sculptures", "winter_lights", "evergreen_garlands"],
        special_npc="Frost the Holiday Duck",
    ),
    
    "duck_day": Festival(
        id="duck_day",
        name="[d] International Duck Day",
        description="Celebrate all things duck! The most special day of the year for Cheese!",
        festival_type=FestivalType.DUCK_DAY,
        start_month=1,
        start_day=13,
        duration_days=3,
        theme_color="yellow",
        activities=[
            FestivalActivity(
                id="quack_parade",
                name="Quack Parade",
                description="Join the grand quacking parade!",
                participation_points=50,
                cooldown_minutes=180,
                max_daily=1,
                rewards=[
                    FestivalReward("Parade Flag", "A Duck Day parade flag", "decoration", "uncommon", xp_value=30),
                ],
            ),
            FestivalActivity(
                id="duck_dance",
                name="Duck Dance Contest",
                description="Show off your best duck dance moves!",
                participation_points=35,
                cooldown_minutes=60,
                max_daily=3,
                rewards=[
                    FestivalReward("Dance Medal", "For excellent dancing", "achievement", "rare", xp_value=40),
                ],
            ),
        ],
        exclusive_rewards=[
            FestivalReward("Golden Duck Trophy", "The ultimate duck prize", "decoration", "legendary", xp_value=200),
            FestivalReward("Duck Crown", "A crown fit for the finest duck", "cosmetic", "legendary", xp_value=175),
            FestivalReward("Duck Day Champion Badge", "Champion of Duck Day", "achievement", "legendary", xp_value=250),
        ],
        decorations=["duck_balloons", "golden_streamers", "duck_banners", "confetti"],
        special_npc="The Grand Quackmaster",
    ),
    
    "love_festival": Festival(
        id="love_festival",
        name="<3 Festival of Love",
        description="Celebrate friendship, love, and the bonds we share!",
        festival_type=FestivalType.LOVE_FESTIVAL,
        start_month=2,
        start_day=14,
        duration_days=3,
        theme_color="pink",
        activities=[
            FestivalActivity(
                id="make_card",
                name="Make a Friendship Card",
                description="Create a card for someone special",
                participation_points=20,
                cooldown_minutes=45,
                max_daily=3,
                rewards=[
                    FestivalReward("Friendship Card", "A handmade card full of love", "gift", "uncommon", xp_value=20),
                ],
            ),
            FestivalActivity(
                id="share_treat",
                name="Share a Treat",
                description="Share something sweet with a friend",
                participation_points=25,
                cooldown_minutes=60,
                max_daily=2,
                rewards=[
                    FestivalReward("Heart Cookie", "A heart-shaped cookie", "consumable", "rare", xp_value=30),
                ],
            ),
        ],
        exclusive_rewards=[
            FestivalReward("Heart Hat", "A hat covered in hearts", "cosmetic", "rare", xp_value=75),
            FestivalReward("Love Spirit Badge", "Spreader of love and friendship", "achievement", "legendary", xp_value=125),
        ],
        decorations=["heart_garlands", "pink_ribbons", "rose_petals", "love_lanterns"],
        special_npc="Cupid the Love Duck",
    ),
}


class FestivalSystem:
    """
    Manages seasonal festivals and celebrations.
    """
    
    def __init__(self):
        self.festival_history: Dict[str, List[FestivalProgress]] = {}  # festival_id -> yearly progress
        self.current_festival_progress: Optional[FestivalProgress] = None
        self.total_festivals_participated: int = 0
        self.festival_rewards_collected: List[str] = []
        self.favorite_festival: Optional[str] = None
        self.last_festival_check: str = ""
    
    def check_active_festival(self) -> Optional[Festival]:
        """Check if there's an active festival right now."""
        today = date.today()
        
        for festival in FESTIVALS.values():
            start = date(today.year, festival.start_month, festival.start_day)
            end_date = start + timedelta(days=festival.duration_days)
            
            if start <= today <= end_date:
                return festival
            
            # Check previous year for festivals that span year boundary
            start_prev = date(today.year - 1, festival.start_month, festival.start_day)
            end_prev = start_prev + timedelta(days=festival.duration_days)
            if start_prev <= today <= end_prev:
                return festival
        
        return None
    
    def start_festival_participation(self, festival: Festival) -> Tuple[bool, str]:
        """Start participating in an active festival."""
        current_year = date.today().year
        
        # Check if already participating this year
        if self.current_festival_progress:
            if (self.current_festival_progress.festival_id == festival.id and
                    self.current_festival_progress.year == current_year):
                return False, "Already participating in this festival!"
        
        # Create new progress
        self.current_festival_progress = FestivalProgress(
            festival_id=festival.id,
            year=current_year,
        )
        
        self.total_festivals_participated += 1
        
        return True, f"(!) Welcome to the {festival.name}!"
    
    def do_festival_activity(self, activity_id: str) -> Tuple[bool, str, Optional[FestivalReward]]:
        """Perform a festival activity."""
        if not self.current_festival_progress:
            return False, "Not participating in a festival!", None
        
        festival = FESTIVALS.get(self.current_festival_progress.festival_id)
        if not festival:
            return False, "Festival not found!", None
        
        # Find the activity
        activity = next((a for a in festival.activities if a.id == activity_id), None)
        if not activity:
            return False, "Activity not found!", None
        
        # Check daily limit
        today = date.today().isoformat()
        if self.current_festival_progress.last_activity_date != today:
            # Reset daily counts
            self.current_festival_progress.daily_activities = {}
            self.current_festival_progress.last_activity_date = today
        
        daily_count = self.current_festival_progress.daily_activities.get(activity_id, 0)
        if daily_count >= activity.max_daily:
            return False, f"You've done this activity {activity.max_daily} times today!", None
        
        # Perform activity
        self.current_festival_progress.daily_activities[activity_id] = daily_count + 1
        self.current_festival_progress.participation_points += activity.participation_points
        
        # Track completion
        total_completions = self.current_festival_progress.activities_completed.get(activity_id, 0)
        self.current_festival_progress.activities_completed[activity_id] = total_completions + 1
        
        # Get reward
        reward = random.choice(activity.rewards) if activity.rewards else None
        
        if reward:
            self.festival_rewards_collected.append(reward.name)
            return True, f"(!) {activity.name} complete! +{activity.participation_points} points! Got: {reward.name}", reward
        
        return True, f"(!) {activity.name} complete! +{activity.participation_points} points!", None
    
    def claim_festival_reward(self, reward_index: int) -> Tuple[bool, str, Optional[FestivalReward]]:
        """Claim an exclusive festival reward based on participation points."""
        if not self.current_festival_progress:
            return False, "Not participating in a festival!", None
        
        festival = FESTIVALS.get(self.current_festival_progress.festival_id)
        if not festival:
            return False, "Festival not found!", None
        
        if reward_index >= len(festival.exclusive_rewards):
            return False, "Invalid reward!", None
        
        reward = festival.exclusive_rewards[reward_index]
        
        # Check if already claimed
        if reward.name in self.current_festival_progress.rewards_claimed:
            return False, "Already claimed this reward!", None
        
        # Check point requirements (based on position)
        required_points = (reward_index + 1) * 100
        if self.current_festival_progress.participation_points < required_points:
            return False, f"Need {required_points} points! (Have: {self.current_festival_progress.participation_points})", None
        
        # Claim reward
        self.current_festival_progress.rewards_claimed.append(reward.name)
        self.festival_rewards_collected.append(reward.name)
        
        return True, f"[#] Claimed: {reward.name}!", reward
    
    def end_festival(self) -> Tuple[bool, str, Dict]:
        """End participation in the current festival."""
        if not self.current_festival_progress:
            return False, "Not participating in a festival!", {}
        
        # Store in history
        festival_id = self.current_festival_progress.festival_id
        if festival_id not in self.festival_history:
            self.festival_history[festival_id] = []

        self.festival_history[festival_id].append(self.current_festival_progress)

        # Keep history manageable to prevent memory leak
        if len(self.festival_history[festival_id]) > 20:
            self.festival_history[festival_id] = self.festival_history[festival_id][-20:]
        
        summary = {
            "festival_id": festival_id,
            "points": self.current_festival_progress.participation_points,
            "activities": sum(self.current_festival_progress.activities_completed.values()),
            "rewards": len(self.current_festival_progress.rewards_claimed),
        }
        
        self.current_festival_progress = None
        
        return True, "(!) Festival participation ended! See you next year!", summary
    
    def get_festival_status(self) -> Optional[Dict]:
        """Get current festival participation status."""
        if not self.current_festival_progress:
            return None
        
        festival = FESTIVALS.get(self.current_festival_progress.festival_id)
        if not festival:
            return None
        
        return {
            "festival_name": festival.name,
            "points": self.current_festival_progress.participation_points,
            "activities_done": self.current_festival_progress.activities_completed,
            "rewards_claimed": self.current_festival_progress.rewards_claimed,
            "available_rewards": [
                {
                    "name": r.name,
                    "required_points": (i + 1) * 100,
                    "claimed": r.name in self.current_festival_progress.rewards_claimed,
                }
                for i, r in enumerate(festival.exclusive_rewards)
            ],
        }
    
    def render_festival_screen(self) -> List[str]:
        """Render the festival interface."""
        active = self.check_active_festival()
        
        if not active:
            return [
                "+===============================================+",
                "|            [#] FESTIVALS [#]                    |",
                "+===============================================+",
                "|                                               |",
                "|       No festival is currently active.        |",
                "|                                               |",
                "|    Check back during seasonal celebrations!   |",
                "|                                               |",
                f"|    Festivals participated: {self.total_festivals_participated:3}               |",
                "|                                               |",
                "+===============================================+",
            ]
        
        lines = [
            "+===============================================+",
            f"|  {active.name:^41}  |",
            "+===============================================+",
        ]
        
        # Description
        desc = active.description[:40]
        lines.append(f"|  {desc:^41}  |")
        lines.append("|                                               |")
        
        if self.current_festival_progress:
            points = self.current_festival_progress.participation_points
            lines.append(f"|  * Participation Points: {points:5}              |")
            lines.append("+===============================================+")
            lines.append("|  ACTIVITIES:                                  |")
            
            # Show more activities with scroll hint
            show_count = min(6, len(active.activities))
            for activity in active.activities[:show_count]:
                done = self.current_festival_progress.activities_completed.get(activity.id, 0)
                daily = self.current_festival_progress.daily_activities.get(activity.id, 0)
                lines.append(f"|   - {activity.name[:25]:25} [{daily}/{activity.max_daily}]   |")
            if len(active.activities) > show_count:
                lines.append(f"|   ... and {len(active.activities) - show_count} more activities              |")
            
            lines.append("+===============================================+")
            lines.append("|  REWARDS:                                     |")
            
            # Show more rewards
            show_rewards = min(5, len(active.exclusive_rewards))
            for i, reward in enumerate(active.exclusive_rewards[:show_rewards]):
                req = (i + 1) * 100
                claimed = "[x]" if reward.name in self.current_festival_progress.rewards_claimed else "[ ]"
                lines.append(f"|   {claimed} {reward.name[:25]:25} ({req}pts)  |")
            if len(active.exclusive_rewards) > show_rewards:
                lines.append(f"|   ... and {len(active.exclusive_rewards) - show_rewards} more rewards                |")
        else:
            lines.append("|                                               |")
            lines.append("|     Press [J]oin to participate!              |")
            lines.append("|                                               |")
        
        lines.append("+===============================================+")
        
        return lines
    
    def get_upcoming_festivals(self) -> List[Tuple[str, int]]:
        """Get list of upcoming festivals and days until they start."""
        today = date.today()
        upcoming = []
        
        for festival in FESTIVALS.values():
            start = date(today.year, festival.start_month, festival.start_day)
            
            # If already passed this year, use next year
            if start < today:
                start = start.replace(year=today.year + 1)
            
            days_until = (start - today).days
            upcoming.append((festival.name, days_until))
        
        return sorted(upcoming, key=lambda x: x[1])
    
    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "festival_history": {
                fid: [
                    {
                        "festival_id": p.festival_id,
                        "year": p.year,
                        "participation_points": p.participation_points,
                        "activities_completed": p.activities_completed,
                        "rewards_claimed": p.rewards_claimed,
                        "daily_activities": p.daily_activities,
                        "last_activity_date": p.last_activity_date,
                    }
                    for p in progress_list
                ]
                for fid, progress_list in self.festival_history.items()
            },
            "current_festival_progress": {
                "festival_id": self.current_festival_progress.festival_id,
                "year": self.current_festival_progress.year,
                "participation_points": self.current_festival_progress.participation_points,
                "activities_completed": self.current_festival_progress.activities_completed,
                "rewards_claimed": self.current_festival_progress.rewards_claimed,
                "daily_activities": self.current_festival_progress.daily_activities,
                "last_activity_date": self.current_festival_progress.last_activity_date,
            } if self.current_festival_progress else None,
            "total_festivals_participated": self.total_festivals_participated,
            "festival_rewards_collected": self.festival_rewards_collected,
            "favorite_festival": self.favorite_festival,
            "last_festival_check": self.last_festival_check,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "FestivalSystem":
        """Create from dictionary."""
        system = cls()
        
        for fid, progress_list in data.get("festival_history", {}).items():
            system.festival_history[fid] = [
                FestivalProgress(
                    festival_id=p["festival_id"],
                    year=p["year"],
                    participation_points=p.get("participation_points", 0),
                    activities_completed=p.get("activities_completed", {}),
                    rewards_claimed=p.get("rewards_claimed", []),
                    daily_activities=p.get("daily_activities", {}),
                    last_activity_date=p.get("last_activity_date", ""),
                )
                for p in progress_list
            ]
        
        current = data.get("current_festival_progress")
        if current:
            system.current_festival_progress = FestivalProgress(
                festival_id=current["festival_id"],
                year=current["year"],
                participation_points=current.get("participation_points", 0),
                activities_completed=current.get("activities_completed", {}),
                rewards_claimed=current.get("rewards_claimed", []),
                daily_activities=current.get("daily_activities", {}),
                last_activity_date=current.get("last_activity_date", ""),
            )
        
        system.total_festivals_participated = data.get("total_festivals_participated", 0)
        system.festival_rewards_collected = data.get("festival_rewards_collected", [])
        system.favorite_festival = data.get("favorite_festival")
        system.last_festival_check = data.get("last_festival_check", "")
        
        return system


# Global festival system instance
festival_system = FestivalSystem()
