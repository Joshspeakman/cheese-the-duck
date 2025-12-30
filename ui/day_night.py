"""
Day/Night Cycle System - Time-based visual changes and events.
Includes sunrise, day, sunset, night phases with visual effects.
"""
from dataclasses import dataclass, field
from datetime import datetime, time, date
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random


class TimeOfDay(Enum):
    """Times of day."""
    DAWN = "dawn"
    MORNING = "morning"
    MIDDAY = "midday"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    DUSK = "dusk"
    NIGHT = "night"
    LATE_NIGHT = "late_night"


class MoonPhase(Enum):
    """Moon phases."""
    NEW_MOON = "new_moon"
    WAXING_CRESCENT = "waxing_crescent"
    FIRST_QUARTER = "first_quarter"
    WAXING_GIBBOUS = "waxing_gibbous"
    FULL_MOON = "full_moon"
    WANING_GIBBOUS = "waning_gibbous"
    LAST_QUARTER = "last_quarter"
    WANING_CRESCENT = "waning_crescent"


@dataclass
class TimePhase:
    """Definition of a time phase."""
    time_of_day: TimeOfDay
    name: str
    start_hour: int
    end_hour: int
    sky_color: str
    ambient_level: float  # 0.0 (dark) to 1.0 (bright)
    description: str
    duck_activity: str  # What duck typically does
    special_events: List[str] = field(default_factory=list)


# Time phase definitions
TIME_PHASES: Dict[TimeOfDay, TimePhase] = {
    TimeOfDay.DAWN: TimePhase(
        time_of_day=TimeOfDay.DAWN,
        name="Dawn",
        start_hour=5,
        end_hour=7,
        sky_color="pink-orange",
        ambient_level=0.4,
        description="The sky turns pink and orange as the sun rises.",
        duck_activity="waking up",
        special_events=["sunrise_bonus", "early_bird_reward"]
    ),
    TimeOfDay.MORNING: TimePhase(
        time_of_day=TimeOfDay.MORNING,
        name="Morning",
        start_hour=7,
        end_hour=11,
        sky_color="light-blue",
        ambient_level=0.8,
        description="Fresh morning air and bright skies.",
        duck_activity="active and energetic",
        special_events=["morning_stretch", "breakfast_time"]
    ),
    TimeOfDay.MIDDAY: TimePhase(
        time_of_day=TimeOfDay.MIDDAY,
        name="Midday",
        start_hour=11,
        end_hour=14,
        sky_color="bright-blue",
        ambient_level=1.0,
        description="The sun is at its highest point.",
        duck_activity="taking a siesta",
        special_events=["sunbathing", "lunch_time"]
    ),
    TimeOfDay.AFTERNOON: TimePhase(
        time_of_day=TimeOfDay.AFTERNOON,
        name="Afternoon",
        start_hour=14,
        end_hour=17,
        sky_color="blue",
        ambient_level=0.9,
        description="Warm afternoon hours.",
        duck_activity="playing",
        special_events=["playtime", "snack_time"]
    ),
    TimeOfDay.EVENING: TimePhase(
        time_of_day=TimeOfDay.EVENING,
        name="Evening",
        start_hour=17,
        end_hour=19,
        sky_color="golden",
        ambient_level=0.6,
        description="Golden hour as the sun starts to set.",
        duck_activity="winding down",
        special_events=["dinner_time", "sunset_watching"]
    ),
    TimeOfDay.DUSK: TimePhase(
        time_of_day=TimeOfDay.DUSK,
        name="Dusk",
        start_hour=19,
        end_hour=21,
        sky_color="purple-orange",
        ambient_level=0.3,
        description="The sky turns purple and orange as night approaches.",
        duck_activity="getting sleepy",
        special_events=["sunset_bonus", "firefly_watching"]
    ),
    TimeOfDay.NIGHT: TimePhase(
        time_of_day=TimeOfDay.NIGHT,
        name="Night",
        start_hour=21,
        end_hour=0,
        sky_color="dark-blue",
        ambient_level=0.15,
        description="Stars twinkle in the dark sky.",
        duck_activity="sleeping",
        special_events=["stargazing", "night_sounds"]
    ),
    TimeOfDay.LATE_NIGHT: TimePhase(
        time_of_day=TimeOfDay.LATE_NIGHT,
        name="Late Night",
        start_hour=0,
        end_hour=5,
        sky_color="black",
        ambient_level=0.1,
        description="Deep night, the world is quiet.",
        duck_activity="deep sleep",
        special_events=["midnight_secret", "shooting_star"]
    ),
}

# Moon phase icons and bonuses
MOON_ICONS: Dict[MoonPhase, str] = {
    MoonPhase.NEW_MOON: "( )",
    MoonPhase.WAXING_CRESCENT: "()",
    MoonPhase.FIRST_QUARTER: "D",
    MoonPhase.WAXING_GIBBOUS: "O",
    MoonPhase.FULL_MOON: "O",
    MoonPhase.WANING_GIBBOUS: "O",
    MoonPhase.LAST_QUARTER: "C",
    MoonPhase.WANING_CRESCENT: "()",
}

# Time-based duck visuals
DUCK_VISUALS: Dict[TimeOfDay, List[str]] = {
    TimeOfDay.DAWN: [
        "    *yawn*    ",
        "      d       ",
        "    z..z..    ",
        "   (waking)   ",
    ],
    TimeOfDay.MORNING: [
        "      *       ",
        "    \\d/      ",
        "   stretch!   ",
        "   *quack!*   ",
    ],
    TimeOfDay.MIDDAY: [
        "   * * *     ",
        "     d       ",
        "    ~~~~     ",
        "   relaxing   ",
    ],
    TimeOfDay.AFTERNOON: [
        "     *        ",
        "    d>>      ",
        "   *waddle*   ",
        "   playful!   ",
    ],
    TimeOfDay.EVENING: [
        "    ~~       ",
        "     d       ",
        "    yum~     ",
        "   dinner    ",
    ],
    TimeOfDay.DUSK: [
        "   ~~         ",
        "    d  *     ",
        "   *yawn*    ",
        "   sleepy..   ",
    ],
    TimeOfDay.NIGHT: [
        "   *  )  *   ",
        "    zzZd     ",
        "   sleeping   ",
        "    ...      ",
    ],
    TimeOfDay.LATE_NIGHT: [
        "     )       ",
        "   zzZdzzZ   ",
        "   *snore*   ",
        "   deep zzz   ",
    ],
}


class DayNightSystem:
    """
    System for day/night cycle and time-based visuals.
    """
    
    def __init__(self):
        self.use_real_time: bool = True
        self.game_hour: int = 12  # Used when not using real time
        self.time_speed: float = 1.0  # 1.0 = real time
        self.sunrises_watched: int = 0
        self.sunsets_watched: int = 0
        self.full_moons_experienced: int = 0
        self.shooting_stars_seen: int = 0
        self.time_bonuses_claimed: Dict[str, str] = {}  # bonus_id -> claimed_date
    
    def get_current_hour(self) -> int:
        """Get current hour (0-23)."""
        if self.use_real_time:
            return datetime.now().hour
        return self.game_hour
    
    def get_current_minute(self) -> int:
        """Get current minute (0-59)."""
        if self.use_real_time:
            return datetime.now().minute
        return 0
    
    def get_time_of_day(self) -> TimeOfDay:
        """Get current time of day phase."""
        hour = self.get_current_hour()
        
        if 5 <= hour < 7:
            return TimeOfDay.DAWN
        elif 7 <= hour < 11:
            return TimeOfDay.MORNING
        elif 11 <= hour < 14:
            return TimeOfDay.MIDDAY
        elif 14 <= hour < 17:
            return TimeOfDay.AFTERNOON
        elif 17 <= hour < 19:
            return TimeOfDay.EVENING
        elif 19 <= hour < 21:
            return TimeOfDay.DUSK
        elif 21 <= hour or hour < 0:
            return TimeOfDay.NIGHT
        else:
            return TimeOfDay.LATE_NIGHT
    
    def get_current_phase(self) -> TimePhase:
        """Get current time phase details."""
        return TIME_PHASES[self.get_time_of_day()]
    
    def get_moon_phase(self) -> MoonPhase:
        """Calculate current moon phase based on date."""
        # Simple moon phase calculation
        # Full lunar cycle is ~29.53 days
        today = date.today()
        # Known full moon date for reference
        known_full = date(2024, 1, 25)
        days_since = (today - known_full).days
        lunar_cycle = 29.53
        phase_progress = (days_since % lunar_cycle) / lunar_cycle
        
        if phase_progress < 0.125:
            return MoonPhase.FULL_MOON
        elif phase_progress < 0.25:
            return MoonPhase.WANING_GIBBOUS
        elif phase_progress < 0.375:
            return MoonPhase.LAST_QUARTER
        elif phase_progress < 0.5:
            return MoonPhase.WANING_CRESCENT
        elif phase_progress < 0.625:
            return MoonPhase.NEW_MOON
        elif phase_progress < 0.75:
            return MoonPhase.WAXING_CRESCENT
        elif phase_progress < 0.875:
            return MoonPhase.FIRST_QUARTER
        else:
            return MoonPhase.WAXING_GIBBOUS
    
    def get_sky_gradient(self) -> List[str]:
        """Get ASCII art representation of the sky."""
        tod = self.get_time_of_day()
        phase = TIME_PHASES[tod]
        
        if tod == TimeOfDay.DAWN:
            return [
                "...,,,###########,,,..:",
                "  * rising from the east  ",
            ]
        elif tod == TimeOfDay.MORNING:
            return [
                "            *               ",
                "  (*)   clear skies   (*)   ",
            ]
        elif tod == TimeOfDay.MIDDAY:
            return [
                "          *                ",
                "      bright and warm       ",
            ]
        elif tod == TimeOfDay.AFTERNOON:
            return [
                "              *             ",
                "    (*)  pleasant  (*)      ",
            ]
        elif tod == TimeOfDay.EVENING:
            return [
                "                  ~~       ",
                "     golden hour glow      ",
            ]
        elif tod == TimeOfDay.DUSK:
            return [
                "###,,,:::......:::,,,###",
                "          ~~               ",
            ]
        elif tod == TimeOfDay.NIGHT:
            moon = MOON_ICONS[self.get_moon_phase()]
            return [
                f"   *    {moon}    *   *   ",
                "         dark sky          ",
            ]
        else:  # Late night
            moon = MOON_ICONS[self.get_moon_phase()]
            return [
                f"  *  *   {moon}     *    ",
                "      deep night           ",
            ]
    
    def get_ambient_modifier(self) -> float:
        """Get current ambient light level modifier."""
        return TIME_PHASES[self.get_time_of_day()].ambient_level
    
    def check_time_bonus(self) -> Optional[Tuple[str, int, int]]:
        """Check for time-based bonuses. Returns (message, coins, xp) or None."""
        tod = self.get_time_of_day()
        today = date.today().isoformat()
        
        # Early bird bonus (dawn, first time today)
        if tod == TimeOfDay.DAWN:
            bonus_id = f"early_bird_{today}"
            if bonus_id not in self.time_bonuses_claimed:
                self.time_bonuses_claimed[bonus_id] = today
                self.sunrises_watched += 1
                return ("~~ Early Bird Bonus! You caught the sunrise!", 50, 25)
        
        # Night owl bonus (late night)
        if tod == TimeOfDay.LATE_NIGHT:
            bonus_id = f"night_owl_{today}"
            if bonus_id not in self.time_bonuses_claimed:
                self.time_bonuses_claimed[bonus_id] = today
                return ("(o,o) Night Owl Bonus! Still awake?", 40, 20)
        
        # Golden hour bonus (dusk)
        if tod == TimeOfDay.DUSK:
            bonus_id = f"sunset_{today}"
            if bonus_id not in self.time_bonuses_claimed:
                self.time_bonuses_claimed[bonus_id] = today
                self.sunsets_watched += 1
                return ("~~ Golden Hour Bonus! Beautiful sunset!", 45, 22)
        
        # Full moon bonus
        if self.get_moon_phase() == MoonPhase.FULL_MOON and tod in [TimeOfDay.NIGHT, TimeOfDay.LATE_NIGHT]:
            bonus_id = f"full_moon_{today}"
            if bonus_id not in self.time_bonuses_claimed:
                self.time_bonuses_claimed[bonus_id] = today
                self.full_moons_experienced += 1
                return ("O Full Moon Bonus! Mystical energy!", 75, 35)
        
        return None
    
    def check_shooting_star(self) -> bool:
        """Random chance for a shooting star at night. Returns True if one appears."""
        tod = self.get_time_of_day()
        if tod not in [TimeOfDay.NIGHT, TimeOfDay.LATE_NIGHT]:
            return False
        
        # 2% chance per check
        if random.random() < 0.02:
            self.shooting_stars_seen += 1
            return True
        return False
    
    def get_duck_energy_modifier(self) -> float:
        """Get energy modifier based on time of day."""
        tod = self.get_time_of_day()
        
        modifiers = {
            TimeOfDay.DAWN: 0.7,
            TimeOfDay.MORNING: 1.2,
            TimeOfDay.MIDDAY: 0.8,
            TimeOfDay.AFTERNOON: 1.0,
            TimeOfDay.EVENING: 0.9,
            TimeOfDay.DUSK: 0.7,
            TimeOfDay.NIGHT: 0.5,
            TimeOfDay.LATE_NIGHT: 0.3,
        }
        
        return modifiers.get(tod, 1.0)
    
    def get_time_string(self) -> str:
        """Get formatted time string."""
        hour = self.get_current_hour()
        minute = self.get_current_minute()
        return f"{hour:02d}:{minute:02d}"
    
    def render_time_display(self) -> List[str]:
        """Render the time of day display."""
        phase = self.get_current_phase()
        time_str = self.get_time_string()
        moon = MOON_ICONS[self.get_moon_phase()]
        
        # Time icon based on day/night
        if phase.ambient_level > 0.5:
            time_icon = "*"
        else:
            time_icon = moon
        
        lines = [
            "+===============================================+",
            f"|    {time_icon} {time_str} - {phase.name:<25}     |",
            "+===============================================+",
        ]
        
        # Sky gradient
        for sky_line in self.get_sky_gradient():
            lines.append(f"|  {sky_line:^43}  |")
        
        lines.append("|                                               |")
        lines.append(f"|  {phase.description:<43}  |")
        lines.append(f"|  Cheese is {phase.duck_activity:<33}  |")
        
        # Duck visual
        duck_visual = DUCK_VISUALS.get(phase.time_of_day, [])
        for dv_line in duck_visual:
            lines.append(f"|  {dv_line:^43}  |")
        
        lines.append("+===============================================+")
        
        return lines
    
    def render_mini_time_widget(self) -> str:
        """Render a compact time widget for the HUD."""
        phase = self.get_current_phase()
        time_str = self.get_time_string()
        
        if phase.ambient_level > 0.5:
            icon = "*"
        elif phase.ambient_level > 0.2:
            icon = ")"
        else:
            icon = "o"
        
        return f"{icon} {time_str}"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "use_real_time": self.use_real_time,
            "game_hour": self.game_hour,
            "time_speed": self.time_speed,
            "sunrises_watched": self.sunrises_watched,
            "sunsets_watched": self.sunsets_watched,
            "full_moons_experienced": self.full_moons_experienced,
            "shooting_stars_seen": self.shooting_stars_seen,
            "time_bonuses_claimed": dict(list(self.time_bonuses_claimed.items())[-30:]),  # Keep last 30
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "DayNightSystem":
        """Create from dictionary."""
        system = cls()
        system.use_real_time = data.get("use_real_time", True)
        system.game_hour = data.get("game_hour", 12)
        system.time_speed = data.get("time_speed", 1.0)
        system.sunrises_watched = data.get("sunrises_watched", 0)
        system.sunsets_watched = data.get("sunsets_watched", 0)
        system.full_moons_experienced = data.get("full_moons_experienced", 0)
        system.shooting_stars_seen = data.get("shooting_stars_seen", 0)
        system.time_bonuses_claimed = data.get("time_bonuses_claimed", {})
        return system


# Global instance
day_night_system = DayNightSystem()
