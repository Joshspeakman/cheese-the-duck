"""
Duck Aging System - Growth stages and age-related content.
Tracks duck age and changes behavior/appearance over time.
"""
from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum


class GrowthStage(Enum):
    """Growth stages of the duck."""
    EGG = "egg"
    HATCHLING = "hatchling"
    DUCKLING = "duckling"
    JUVENILE = "juvenile"
    YOUNG_ADULT = "young_adult"
    ADULT = "adult"
    MATURE = "mature"
    ELDER = "elder"
    LEGENDARY = "legendary"


@dataclass
class StageInfo:
    """Information about a growth stage."""
    stage: GrowthStage
    name: str
    min_days: int
    max_days: int  # -1 for no upper limit
    description: str
    size_multiplier: float  # Affects size in ASCII art
    stat_modifiers: Dict[str, float]  # Modifiers to various stats
    unlocks: List[str]  # Features unlocked at this stage
    ascii_art: List[str]
    special_abilities: List[str]


# Growth stage definitions
GROWTH_STAGES: Dict[GrowthStage, StageInfo] = {
    GrowthStage.EGG: StageInfo(
        stage=GrowthStage.EGG,
        name="Egg",
        min_days=0,
        max_days=0,  # Only exists at creation
        description="A mysterious egg, waiting to hatch...",
        size_multiplier=0.5,
        stat_modifiers={},
        unlocks=[],
        ascii_art=[
            "    ___    ",
            "   /   \\   ",
            "  |  ?  |  ",
            "   \\___/   ",
        ],
        special_abilities=[]
    ),
    
    GrowthStage.HATCHLING: StageInfo(
        stage=GrowthStage.HATCHLING,
        name="Hatchling",
        min_days=0,
        max_days=3,
        description="A tiny, adorable freshly-hatched duck!",
        size_multiplier=0.6,
        stat_modifiers={
            "hunger_rate": 1.5,  # Gets hungry faster
            "energy_rate": 1.3,  # Gets tired faster
            "happiness_gain": 1.5,  # Easier to make happy
        },
        unlocks=["basic_care", "feeding", "petting"],
        ascii_art=[
            "   (\\./)   ",
            "   (o.o)   ",
            "    ('>)   ",
            "   *tiny*  ",
        ],
        special_abilities=["extra_cute"]
    ),
    
    GrowthStage.DUCKLING: StageInfo(
        stage=GrowthStage.DUCKLING,
        name="Duckling",
        min_days=3,
        max_days=14,
        description="A fluffy duckling learning about the world!",
        size_multiplier=0.7,
        stat_modifiers={
            "hunger_rate": 1.3,
            "energy_rate": 1.2,
            "xp_gain": 1.2,  # Learns faster
        },
        unlocks=["minigames", "exploring"],
        ascii_art=[
            "    __     ",
            "  >(o )__  ",
            "   ( ._>   ",
            "  *fluffy* ",
        ],
        special_abilities=["quick_learner"]
    ),
    
    GrowthStage.JUVENILE: StageInfo(
        stage=GrowthStage.JUVENILE,
        name="Juvenile",
        min_days=14,
        max_days=30,
        description="A growing duck, full of energy!",
        size_multiplier=0.85,
        stat_modifiers={
            "energy_rate": 0.9,  # More stamina
            "xp_gain": 1.1,
        },
        unlocks=["fishing", "basic_tricks"],
        ascii_art=[
            "     __    ",
            "  __( o)>  ",
            " \\_ \\__/   ",
            "  *growing*",
        ],
        special_abilities=["energetic"]
    ),
    
    GrowthStage.YOUNG_ADULT: StageInfo(
        stage=GrowthStage.YOUNG_ADULT,
        name="Young Adult",
        min_days=30,
        max_days=90,
        description="A young adult duck, becoming independent!",
        size_multiplier=0.95,
        stat_modifiers={
            "coin_gain": 1.1,
        },
        unlocks=["garden", "treasure_hunting", "intermediate_tricks"],
        ascii_art=[
            "      _    ",
            "   __( o)> ",
            "  \\___\\_/  ",
            "   *young* ",
        ],
        special_abilities=["social_butterfly"]
    ),
    
    GrowthStage.ADULT: StageInfo(
        stage=GrowthStage.ADULT,
        name="Adult",
        min_days=90,
        max_days=365,
        description="A fully grown adult duck in their prime!",
        size_multiplier=1.0,
        stat_modifiers={},  # Baseline
        unlocks=["advanced_tricks", "trading", "all_locations"],
        ascii_art=[
            "      __   ",
            "   __(o )> ",
            "  \\_____/  ",
            "   *prime* ",
        ],
        special_abilities=["balanced"]
    ),
    
    GrowthStage.MATURE: StageInfo(
        stage=GrowthStage.MATURE,
        name="Mature",
        min_days=365,
        max_days=730,  # 2 years
        description="A wise and experienced duck!",
        size_multiplier=1.0,
        stat_modifiers={
            "coin_gain": 1.15,
            "xp_gain": 0.9,
        },
        unlocks=["master_tricks", "mentoring"],
        ascii_art=[
            "      __   ",
            "   __(• )> ",
            "  \\_____/  ",
            "   *wise*  ",
        ],
        special_abilities=["wise", "mentor"]
    ),
    
    GrowthStage.ELDER: StageInfo(
        stage=GrowthStage.ELDER,
        name="Elder",
        min_days=730,
        max_days=1095,  # 3 years
        description="A venerable elder duck, respected by all!",
        size_multiplier=1.0,
        stat_modifiers={
            "coin_gain": 1.25,
            "energy_rate": 1.2,  # Tires faster
            "happiness_gain": 1.2,
        },
        unlocks=["elder_wisdom", "legacy_items"],
        ascii_art=[
            "    o     ",
            "   __(◕ )> ",
            "  \\_____/  ",
            "  *elder*  ",
        ],
        special_abilities=["respected", "storyteller"]
    ),
    
    GrowthStage.LEGENDARY: StageInfo(
        stage=GrowthStage.LEGENDARY,
        name="Legendary",
        min_days=1095,  # 3+ years
        max_days=-1,
        description="A legendary duck that has transcended time!",
        size_multiplier=1.1,
        stat_modifiers={
            "coin_gain": 1.5,
            "xp_gain": 1.5,
            "happiness_gain": 1.5,
        },
        unlocks=["legendary_status", "all_abilities"],
        ascii_art=[
            "    *^    ",
            "   __(* )> ",
            "  \\_____/  ",
            " *LEGEND*  ",
        ],
        special_abilities=["legendary_aura", "time_transcendent"]
    ),
}


@dataclass
class AgeEvent:
    """A special event that occurred during the duck's life."""
    event_type: str
    description: str
    occurred_at: str
    age_days: int


class AgingSystem:
    """
    System for tracking duck age and growth.
    """
    
    def __init__(self):
        self.birth_date: Optional[str] = None  # ISO format
        self.current_stage: GrowthStage = GrowthStage.HATCHLING
        self.days_in_current_stage: int = 0
        self.life_events: List[AgeEvent] = []
        self.growth_milestones: Dict[str, str] = {}  # stage -> date reached
        self.birthday_celebrated: Dict[int, bool] = {}  # year -> celebrated
        self.aging_paused: bool = False  # For prestige or special modes
    
    def initialize(self, birth_date: Optional[str] = None):
        """Initialize the aging system for a new duck."""
        if birth_date:
            self.birth_date = birth_date
        else:
            self.birth_date = date.today().isoformat()
        
        self.current_stage = GrowthStage.HATCHLING
        self.growth_milestones[GrowthStage.HATCHLING.value] = datetime.now().isoformat()
        
        self.life_events.append(AgeEvent(
            event_type="birth",
            description="A new duck was born!",
            occurred_at=datetime.now().isoformat(),
            age_days=0
        ))
    
    def get_age_days(self) -> int:
        """Get the duck's age in days."""
        if not self.birth_date:
            return 0
        
        birth = date.fromisoformat(self.birth_date)
        return (date.today() - birth).days
    
    def get_age_string(self) -> str:
        """Get a human-readable age string."""
        days = self.get_age_days()
        
        if days < 7:
            return f"{days} days old"
        elif days < 30:
            weeks = days // 7
            return f"{weeks} week{'s' if weeks > 1 else ''} old"
        elif days < 365:
            months = days // 30
            return f"{months} month{'s' if months > 1 else ''} old"
        else:
            years = days // 365
            months = (days % 365) // 30
            if months > 0:
                return f"{years} year{'s' if years > 1 else ''}, {months} month{'s' if months > 1 else ''} old"
            return f"{years} year{'s' if years > 1 else ''} old"
    
    def update_stage(self) -> Optional[GrowthStage]:
        """Update growth stage based on age. Returns new stage if changed."""
        if self.aging_paused:
            return None
        
        days = self.get_age_days()
        
        # Find appropriate stage
        new_stage = None
        for stage in GrowthStage:
            stage_info = GROWTH_STAGES[stage]
            if days >= stage_info.min_days:
                if stage_info.max_days == -1 or days <= stage_info.max_days:
                    new_stage = stage
        
        if new_stage and new_stage != self.current_stage:
            old_stage = self.current_stage
            self.current_stage = new_stage
            self.days_in_current_stage = 0
            self.growth_milestones[new_stage.value] = datetime.now().isoformat()
            
            self.life_events.append(AgeEvent(
                event_type="growth",
                description=f"Grew from {old_stage.value} to {new_stage.value}!",
                occurred_at=datetime.now().isoformat(),
                age_days=days
            ))
            
            return new_stage
        
        return None
    
    def get_current_stage_info(self) -> StageInfo:
        """Get information about the current growth stage."""
        return GROWTH_STAGES[self.current_stage]
    
    def get_stat_modifier(self, stat: str) -> float:
        """Get the modifier for a specific stat based on current stage."""
        stage_info = GROWTH_STAGES[self.current_stage]
        return stage_info.stat_modifiers.get(stat, 1.0)
    
    def is_birthday(self) -> Tuple[bool, int]:
        """Check if today is the duck's birthday. Returns (is_birthday, years)."""
        if not self.birth_date:
            return False, 0
        
        birth = date.fromisoformat(self.birth_date)
        today = date.today()
        
        if birth.month == today.month and birth.day == today.day:
            years = today.year - birth.year
            if years > 0 and not self.birthday_celebrated.get(years, False):
                return True, years
        
        return False, 0
    
    def celebrate_birthday(self, years: int):
        """Mark a birthday as celebrated."""
        self.birthday_celebrated[years] = True
        
        self.life_events.append(AgeEvent(
            event_type="birthday",
            description=f"Celebrated {years} year{'s' if years > 1 else ''} birthday!",
            occurred_at=datetime.now().isoformat(),
            age_days=self.get_age_days()
        ))
    
    def add_life_event(self, event_type: str, description: str):
        """Add a custom life event."""
        self.life_events.append(AgeEvent(
            event_type=event_type,
            description=description,
            occurred_at=datetime.now().isoformat(),
            age_days=self.get_age_days()
        ))
    
    def get_unlocked_features(self) -> List[str]:
        """Get all features unlocked up to current stage."""
        unlocked = []
        stage_order = list(GrowthStage)
        current_index = stage_order.index(self.current_stage)
        
        for i in range(current_index + 1):
            stage_info = GROWTH_STAGES[stage_order[i]]
            unlocked.extend(stage_info.unlocks)
        
        return unlocked
    
    def render_age_display(self) -> List[str]:
        """Render the age and growth display."""
        stage_info = self.get_current_stage_info()
        age_str = self.get_age_string()
        
        lines = [
            "+===============================================+",
            "|            d DUCK GROWTH d                  |",
            "+===============================================+",
        ]
        
        # ASCII art
        for art_line in stage_info.ascii_art:
            lines.append(f"|  {art_line:^43}  |")
        
        lines.append("|                                               |")
        lines.append(f"|  Stage: {stage_info.name:<35}  |")
        lines.append(f"|  Age: {age_str:<37}  |")
        lines.append(f"|  {stage_info.description[:43]:<43}  |")
        
        # Progress to next stage
        lines.append("+===============================================+")
        
        days = self.get_age_days()
        stage_order = list(GrowthStage)
        current_index = stage_order.index(self.current_stage)
        
        if current_index < len(stage_order) - 1:
            next_stage = stage_order[current_index + 1]
            next_info = GROWTH_STAGES[next_stage]
            days_until = next_info.min_days - days
            
            if days_until > 0:
                lines.append(f"|  Next: {next_info.name} in {days_until} days           |")
            else:
                lines.append(f"|  Ready to grow to: {next_info.name}!             |")
        else:
            lines.append("|  Maximum growth achieved! *                  |")
        
        # Special abilities
        if stage_info.special_abilities:
            lines.append("+===============================================+")
            lines.append("|  Special Abilities:                           |")
            for ability in stage_info.special_abilities:
                lines.append(f"|  • {ability:<41}  |")
        
        # Stat modifiers
        if stage_info.stat_modifiers:
            lines.append("+===============================================+")
            lines.append("|  Stage Bonuses:                               |")
            for stat, modifier in stage_info.stat_modifiers.items():
                mod_str = f"+{int((modifier - 1) * 100)}%" if modifier > 1 else f"{int((modifier - 1) * 100)}%"
                stat_name = stat.replace("_", " ").title()
                lines.append(f"|  • {stat_name}: {mod_str:<30}  |")
        
        lines.append("+===============================================+")
        
        return lines
    
    def render_life_timeline(self, page: int = 1) -> List[str]:
        """Render the duck's life timeline."""
        lines = [
            "+===============================================+",
            "|           [=] LIFE TIMELINE [=]                 |",
            "+===============================================+",
        ]
        
        if not self.life_events:
            lines.append("|  No events recorded yet!                      |")
        else:
            # Reverse chronological
            events = list(reversed(self.life_events))
            per_page = 6
            start = (page - 1) * per_page
            end = start + per_page
            page_events = events[start:end]
            
            for event in page_events:
                icon = {
                    "birth": "o",
                    "growth": "^",
                    "birthday": "#",
                    "achievement": "[#]",
                    "milestone": "*",
                }.get(event.event_type, "[=]")
                
                lines.append(f"|  {icon} Day {event.age_days}: {event.description[:30]:<30}  |")
            
            total_pages = (len(events) + per_page - 1) // per_page
            lines.append("+===============================================+")
            lines.append(f"|  Page {page}/{total_pages}  [<-/-> to navigate]                |")
        
        lines.append("+===============================================+")
        
        return lines
    
    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "birth_date": self.birth_date,
            "current_stage": self.current_stage.value,
            "days_in_current_stage": self.days_in_current_stage,
            "life_events": [
                {
                    "event_type": e.event_type,
                    "description": e.description,
                    "occurred_at": e.occurred_at,
                    "age_days": e.age_days,
                }
                for e in self.life_events[-100:]  # Keep last 100
            ],
            "growth_milestones": self.growth_milestones,
            "birthday_celebrated": {str(k): v for k, v in self.birthday_celebrated.items()},
            "aging_paused": self.aging_paused,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "AgingSystem":
        """Create from dictionary."""
        system = cls()
        system.birth_date = data.get("birth_date")
        
        stage_str = data.get("current_stage", "hatchling")
        try:
            system.current_stage = GrowthStage(stage_str)
        except ValueError:
            system.current_stage = GrowthStage.HATCHLING
        
        system.days_in_current_stage = data.get("days_in_current_stage", 0)
        
        events = data.get("life_events", [])
        system.life_events = [
            AgeEvent(
                event_type=e["event_type"],
                description=e["description"],
                occurred_at=e["occurred_at"],
                age_days=e["age_days"],
            )
            for e in events
        ]
        
        system.growth_milestones = data.get("growth_milestones", {})
        system.birthday_celebrated = {int(k): v for k, v in data.get("birthday_celebrated", {}).items()}
        system.aging_paused = data.get("aging_paused", False)
        
        return system


# Global instance
aging_system = AgingSystem()
