"""
Atmosphere system - Weather, Seasons, Lucky Days, and Rare Visitors.
Creates dynamic, engaging world that changes over time (Animal Crossing style).
"""
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


# =============================================================================
# WEATHER SYSTEM
# =============================================================================

class WeatherType(Enum):
    """Types of weather that affect gameplay."""
    SUNNY = "sunny"
    CLOUDY = "cloudy"
    RAINY = "rainy"
    STORMY = "stormy"
    FOGGY = "foggy"
    SNOWY = "snowy"
    WINDY = "windy"
    RAINBOW = "rainbow"  # Rare, after rain


@dataclass
class Weather:
    """Current weather state."""
    weather_type: WeatherType
    intensity: float  # 0.0 to 1.0
    duration_hours: float
    start_time: str  # ISO datetime

    # Gameplay effects
    mood_modifier: int = 0
    xp_multiplier: float = 1.0
    special_message: str = ""

    def is_active(self) -> bool:
        """Check if weather is still active."""
        try:
            start = datetime.fromisoformat(self.start_time)
            elapsed = (datetime.now() - start).total_seconds() / 3600
            return elapsed < self.duration_hours
        except:
            return False


# Weather definitions with probabilities by season
WEATHER_DATA = {
    WeatherType.SUNNY: {
        "name": "Sunny",
        "message": "The sun is shining! Perfect day!",
        "mood_modifier": 5,
        "xp_multiplier": 1.1,
        "ascii": ["  \\  |  /", "   \\ | /", " -- \u2299 --", "   / | \\", "  /  |  \\"],
        "spring_prob": 0.35, "summer_prob": 0.50, "fall_prob": 0.25, "winter_prob": 0.15,
    },
    WeatherType.CLOUDY: {
        "name": "Cloudy",
        "message": "Clouds drift overhead...",
        "mood_modifier": 0,
        "xp_multiplier": 1.0,
        "ascii": ["   .-~~~-.", " .-~       ~-.", "{    CLOUD   }", " `-._______.-'"],
        "spring_prob": 0.25, "summer_prob": 0.15, "fall_prob": 0.30, "winter_prob": 0.30,
    },
    WeatherType.RAINY: {
        "name": "Rainy",
        "message": "*pitter patter* Cheese loves splashing in puddles!",
        "mood_modifier": -2,
        "xp_multiplier": 1.15,  # Bonus for playing in rain
        "ascii": [" , , , , ,", ", , , , , ,", " , , , , ,", "  ~ puddles ~"],
        "spring_prob": 0.25, "summer_prob": 0.15, "fall_prob": 0.25, "winter_prob": 0.10,
        "triggers_rainbow": True,
    },
    WeatherType.STORMY: {
        "name": "Stormy",
        "message": "*BOOM* Thunder! Cheese hides under a wing...",
        "mood_modifier": -5,
        "xp_multiplier": 1.25,  # Big bonus for braving the storm
        "ascii": [" \\\\\\|///", "  STORM!!", " ///|\\\\\\", "  * zap *"],
        "spring_prob": 0.05, "summer_prob": 0.10, "fall_prob": 0.10, "winter_prob": 0.05,
    },
    WeatherType.FOGGY: {
        "name": "Foggy",
        "message": "Mysterious fog rolls in... spooky!",
        "mood_modifier": 0,
        "xp_multiplier": 1.2,  # Mystery bonus
        "ascii": ["~ ~ ~ ~ ~ ~", " ~ ~ ~ ~ ~", "~ ~ ~ ~ ~ ~", " ~ fog ~ ~"],
        "spring_prob": 0.05, "summer_prob": 0.02, "fall_prob": 0.08, "winter_prob": 0.15,
        "rare_drops_bonus": 0.5,  # 50% more rare drops
    },
    WeatherType.SNOWY: {
        "name": "Snowy",
        "message": "*catches snowflake* So pretty! So cold!",
        "mood_modifier": 3,
        "xp_multiplier": 1.2,
        "ascii": ["  *  *  *  ", " *  *  *  *", "  *  *  *  ", "~~~~~~~~~~~~"],
        "spring_prob": 0.02, "summer_prob": 0.0, "fall_prob": 0.05, "winter_prob": 0.30,
    },
    WeatherType.WINDY: {
        "name": "Windy",
        "message": "*feathers ruffled* Woooosh!",
        "mood_modifier": 2,
        "xp_multiplier": 1.0,
        "ascii": ["  ~~ >>> ~~", " ~~ >>> ~~", "~~ >>> ~~", "  whoooosh"],
        "spring_prob": 0.08, "summer_prob": 0.05, "fall_prob": 0.12, "winter_prob": 0.10,
    },
    WeatherType.RAINBOW: {
        "name": "Rainbow",
        "message": "A RAINBOW! Make a wish! This is MAGICAL!",
        "mood_modifier": 15,
        "xp_multiplier": 2.0,  # Double XP during rainbows!
        "ascii": ["   .--.", " .'    `.", "/  RAINBOW\\", "  colors! "],
        "spring_prob": 0.0, "summer_prob": 0.0, "fall_prob": 0.0, "winter_prob": 0.0,
        "special": True,
    },
}


# =============================================================================
# SEASONS
# =============================================================================

class Season(Enum):
    """Seasons that affect gameplay."""
    SPRING = "spring"
    SUMMER = "summer"
    FALL = "fall"
    WINTER = "winter"


@dataclass
class SeasonalContent:
    """Content specific to a season."""
    items_available: List[str]  # Special items only available this season
    events: List[str]  # Special events
    decorations: List[str]  # Seasonal decorations
    mood_theme: str  # General mood of the season
    xp_bonus: float  # Season-wide XP modifier


SEASONAL_CONTENT = {
    Season.SPRING: SeasonalContent(
        items_available=["spring_flower", "easter_egg", "cherry_blossom"],
        events=["cherry_blossom_festival", "spring_cleaning", "egg_hunt"],
        decorations=["flower_wreath", "pastel_banner", "bunny_statue"],
        mood_theme="renewal",
        xp_bonus=1.1,
    ),
    Season.SUMMER: SeasonalContent(
        items_available=["watermelon", "sunscreen", "beach_ball", "ice_cream"],
        events=["beach_day", "fireworks_show", "summer_festival"],
        decorations=["beach_umbrella", "sandcastle", "tiki_torch"],
        mood_theme="adventure",
        xp_bonus=1.0,
    ),
    Season.FALL: SeasonalContent(
        items_available=["pumpkin", "autumn_leaf", "candy_corn", "apple_cider"],
        events=["harvest_festival", "spooky_night", "thanksgiving_feast"],
        decorations=["scarecrow", "hay_bale", "pumpkin_lantern"],
        mood_theme="cozy",
        xp_bonus=1.15,
    ),
    Season.WINTER: SeasonalContent(
        items_available=["hot_cocoa", "snowball", "candy_cane", "wrapped_gift"],
        events=["first_snow", "winter_festival", "new_year_countdown"],
        decorations=["snow_duck", "string_lights", "wreath"],
        mood_theme="warmth",
        xp_bonus=1.2,
    ),
}


# =============================================================================
# LUCKY / UNLUCKY DAYS
# =============================================================================

@dataclass
class DayFortune:
    """Fortune for a specific day (lucky/unlucky)."""
    fortune_type: str  # "lucky", "normal", "unlucky", "super_lucky"
    xp_multiplier: float
    drop_rate_modifier: float  # Multiplier for rare drops
    special_message: str
    horoscope: str  # Fun daily fortune message


FORTUNE_TYPES = {
    "super_lucky": {
        "probability": 0.02,  # 2% chance
        "xp_multiplier": 2.0,
        "drop_rate_modifier": 3.0,
        "messages": [
            "The stars align! SUPER LUCKY DAY! Everything sparkles!",
            "Cheese found a four-leaf clover! MAXIMUM LUCK activated!",
            "The universe smiles upon you today! Triple rare drops!",
        ],
        "horoscopes": [
            "Today, even the bread crumbs lead to treasure!",
            "Lucky streams flow through your feathers today!",
            "The duck spirits have blessed this day abundantly!",
        ],
    },
    "lucky": {
        "probability": 0.15,  # 15% chance
        "xp_multiplier": 1.3,
        "drop_rate_modifier": 1.5,
        "messages": [
            "Feeling lucky today! Good things are coming!",
            "Cheese's lucky feather is tingling!",
            "The vibes are immaculate today!",
        ],
        "horoscopes": [
            "Fortune favors the bold duck today!",
            "Small surprises await around every corner!",
            "Your quacks carry extra weight today!",
        ],
    },
    "normal": {
        "probability": 0.70,  # 70% chance
        "xp_multiplier": 1.0,
        "drop_rate_modifier": 1.0,
        "messages": [
            "A pleasant, ordinary day!",
            "Just right for duck activities!",
        ],
        "horoscopes": [
            "Balance in all things today!",
            "A day like any other, yet full of potential!",
        ],
    },
    "unlucky": {
        "probability": 0.13,  # 13% chance (but we make it feel ok)
        "xp_multiplier": 0.9,
        "drop_rate_modifier": 0.7,
        "messages": [
            "Feeling a bit off today... but Cheese is still here for you!",
            "Not the luckiest day, but that makes the good days better!",
            "Mercury might be in retrograde, but ducks don't care!",
        ],
        "horoscopes": [
            "Even unlucky days teach valuable lessons!",
            "Tomorrow will be better! Today, just cozy up!",
            "Bad luck? Psh. Cheese makes their own luck!",
        ],
        # Compensations for unlucky days (so it doesn't feel bad)
        "compensations": [
            "Extra cuddles from Cheese today! +social bonus",
            "Cheese found a comfort snack for you!",
            "At least the company is good!",
        ],
    },
}


# =============================================================================
# RARE VISITORS
# =============================================================================

@dataclass
class Visitor:
    """A rare visitor that can appear."""
    id: str
    name: str
    description: str
    ascii_art: List[str]
    greeting: str
    farewell: str
    gift_chance: float  # Chance to leave a gift
    possible_gifts: List[str]
    appearance_chance: float
    stay_duration_hours: float
    special_interaction: str  # What you can do with them
    mood_boost: int


VISITORS = {
    "friendly_goose": Visitor(
        id="friendly_goose",
        name="Gerald the Goose",
        description="A surprisingly friendly goose waddles by!",
        ascii_art=[
            "   __",
            " >(o )___",
            "  ( ._> /",
            "   `---'",
        ],
        greeting="*HONK* Oh, a fellow waterfowl! Gerald has arrived!",
        farewell="*HONK* Gerald must go. Keep being awesome, friend!",
        gift_chance=0.7,
        possible_gifts=["bread", "shiny_pebble", "feather"],
        appearance_chance=0.008,
        stay_duration_hours=2,
        special_interaction="chat",
        mood_boost=15,
    ),
    "wise_owl": Visitor(
        id="wise_owl",
        name="Professor Hoot",
        description="A wise owl visits under moonlight!",
        ascii_art=[
            "  ,___,",
            "  (O,O)",
            "  /)_)",
            "   \" \"",
        ],
        greeting="*hoo hoo* Greetings, young duck. I bring wisdom!",
        farewell="*hoo* Remember: knowledge is the greatest treasure. Farewell!",
        gift_chance=0.9,
        possible_gifts=["mysterious_crumb", "old_key", "crystal_shard"],
        appearance_chance=0.005,
        stay_duration_hours=1,
        special_interaction="learn",
        mood_boost=20,
    ),
    "lost_duckling": Visitor(
        id="lost_duckling",
        name="Pip the Duckling",
        description="A tiny lost duckling needs help!",
        ascii_art=[
            " __",
            "(o>",
            " V",
        ],
        greeting="*peep peep* I'm lost! Can I stay here for a bit?",
        farewell="*happy peep* Thank you for helping me! You're the best!",
        gift_chance=1.0,
        possible_gifts=["fluffy_down", "lucky_clover"],
        appearance_chance=0.01,
        stay_duration_hours=3,
        special_interaction="comfort",
        mood_boost=25,
    ),
    "traveling_merchant": Visitor(
        id="traveling_merchant",
        name="Marco the Merchant Duck",
        description="A traveling merchant duck appears with wares!",
        ascii_art=[
            "   ,__,",
            "  (o.o)",
            " /|##|\\",
            "  d  b",
        ],
        greeting="*quack* Greetings! Marco has exotic items from far lands!",
        farewell="*quack* Marco must continue the journey. Until next time!",
        gift_chance=0.5,
        possible_gifts=["fancy_bread", "glass_marble", "rainbow_crumb"],
        appearance_chance=0.004,
        stay_duration_hours=1.5,
        special_interaction="trade",
        mood_boost=10,
    ),
    "celebrity_duck": Visitor(
        id="celebrity_duck",
        name="Sir Quackington III",
        description="A famous noble duck graces you with their presence!",
        ascii_art=[
            "  /\\  ",
            " (@@)",
            " /||\\",
            "  ''",
        ],
        greeting="*regal quack* One has heard of your establishment. Impressive!",
        farewell="*noble nod* One shall speak well of this place. Farewell!",
        gift_chance=0.8,
        possible_gifts=["golden_crumb", "crown", "ancient_artifact"],
        appearance_chance=0.002,
        stay_duration_hours=0.5,
        special_interaction="impress",
        mood_boost=30,
    ),
    "mysterious_crow": Visitor(
        id="mysterious_crow",
        name="The Mysterious Crow",
        description="A cryptic crow appears with secrets...",
        ascii_art=[
            "   ___",
            " /'o o'\\",
            " \\ V  /",
            "  ^^^",
        ],
        greeting="*caw* I know things... secret things...",
        farewell="*caw* We will meet again when the stars align...",
        gift_chance=0.6,
        possible_gifts=["old_key", "crystal_shard", "ancient_artifact"],
        appearance_chance=0.003,
        stay_duration_hours=1,
        special_interaction="mystery",
        mood_boost=5,
    ),
}


# =============================================================================
# ATMOSPHERE MANAGER
# =============================================================================

class AtmosphereManager:
    """
    Manages weather, seasons, luck, and visitors.
    Creates dynamic world that changes over time.
    """

    def __init__(self):
        self.current_weather: Optional[Weather] = None
        self.current_season: Season = self._calculate_season()
        self.day_fortune: Optional[DayFortune] = None
        self.current_visitor: Optional[Tuple[Visitor, str]] = None  # (visitor, arrival_time)
        self.last_fortune_date: Optional[str] = None
        self.last_weather_check: Optional[str] = None
        self.visitor_history: List[str] = []  # Track who has visited
        self.weather_history: List[str] = []  # Recent weather

        # Generate initial states
        self._generate_weather()
        self._generate_fortune()

    def _calculate_season(self) -> Season:
        """Determine current season based on date."""
        month = datetime.now().month
        if month in [3, 4, 5]:
            return Season.SPRING
        elif month in [6, 7, 8]:
            return Season.SUMMER
        elif month in [9, 10, 11]:
            return Season.FALL
        else:
            return Season.WINTER

    def _generate_weather(self):
        """Generate new weather based on season."""
        season = self.current_season
        season_key = f"{season.value}_prob"

        # Build weighted list
        weather_options = []
        for weather_type, data in WEATHER_DATA.items():
            if data.get("special"):
                continue  # Skip special weather like rainbow
            prob = data.get(season_key, 0.1)
            weight = int(prob * 100)
            weather_options.extend([weather_type] * max(1, weight))

        chosen_type = random.choice(weather_options)
        data = WEATHER_DATA[chosen_type]

        # Determine duration (1-6 hours)
        duration = random.uniform(1, 6)

        self.current_weather = Weather(
            weather_type=chosen_type,
            intensity=random.uniform(0.3, 1.0),
            duration_hours=duration,
            start_time=datetime.now().isoformat(),
            mood_modifier=data.get("mood_modifier", 0),
            xp_multiplier=data.get("xp_multiplier", 1.0),
            special_message=data.get("message", ""),
        )

        self.weather_history.append(chosen_type.value)
        if len(self.weather_history) > 10:
            self.weather_history = self.weather_history[-10:]

        self.last_weather_check = datetime.now().strftime("%Y-%m-%d %H")

    def _maybe_rainbow(self):
        """Check if rainbow should appear after rain."""
        if not self.current_weather:
            return

        # Rainbow can appear after rain (20% chance)
        if (self.current_weather.weather_type == WeatherType.RAINY and
            not self.current_weather.is_active() and
            random.random() < 0.2):

            data = WEATHER_DATA[WeatherType.RAINBOW]
            self.current_weather = Weather(
                weather_type=WeatherType.RAINBOW,
                intensity=1.0,
                duration_hours=0.5,  # Short but magical
                start_time=datetime.now().isoformat(),
                mood_modifier=data.get("mood_modifier", 0),
                xp_multiplier=data.get("xp_multiplier", 1.0),
                special_message=data.get("message", ""),
            )

    def _generate_fortune(self):
        """Generate fortune for the day."""
        today = datetime.now().strftime("%Y-%m-%d")

        if self.last_fortune_date == today and self.day_fortune:
            return

        # Roll for fortune type
        roll = random.random()
        cumulative = 0
        chosen_type = "normal"

        for fortune_type, data in FORTUNE_TYPES.items():
            cumulative += data["probability"]
            if roll < cumulative:
                chosen_type = fortune_type
                break

        data = FORTUNE_TYPES[chosen_type]

        self.day_fortune = DayFortune(
            fortune_type=chosen_type,
            xp_multiplier=data["xp_multiplier"],
            drop_rate_modifier=data["drop_rate_modifier"],
            special_message=random.choice(data["messages"]),
            horoscope=random.choice(data["horoscopes"]),
        )

        self.last_fortune_date = today

    def update(self) -> List[str]:
        """
        Update atmosphere state. Call periodically.
        Returns list of messages about changes.
        """
        messages = []

        # Update season if needed
        new_season = self._calculate_season()
        if new_season != self.current_season:
            self.current_season = new_season
            content = SEASONAL_CONTENT[new_season]
            messages.append(f"Season changed to {new_season.value}! {content.mood_theme.title()} vibes!")

        # Check weather
        current_hour = datetime.now().strftime("%Y-%m-%d %H")
        if self.last_weather_check != current_hour:
            if self.current_weather and not self.current_weather.is_active():
                self._maybe_rainbow()
                if self.current_weather.weather_type != WeatherType.RAINBOW:
                    self._generate_weather()
                    messages.append(f"Weather changed: {self.current_weather.special_message}")
            elif not self.current_weather:
                self._generate_weather()
            self.last_weather_check = current_hour

        # Check fortune
        today = datetime.now().strftime("%Y-%m-%d")
        if self.last_fortune_date != today:
            self._generate_fortune()
            messages.append(f"Today's fortune: {self.day_fortune.horoscope}")

        # Check for visitor
        visitor_msg = self._check_visitor()
        if visitor_msg:
            messages.append(visitor_msg)

        return messages

    def _check_visitor(self) -> Optional[str]:
        """Check if a visitor should appear or leave."""
        # Check if current visitor should leave
        if self.current_visitor:
            visitor, arrival = self.current_visitor
            try:
                arrival_time = datetime.fromisoformat(arrival)
                elapsed = (datetime.now() - arrival_time).total_seconds() / 3600
                if elapsed >= visitor.stay_duration_hours:
                    self.current_visitor = None
                    return visitor.farewell
            except:
                self.current_visitor = None

        # Maybe spawn new visitor
        if not self.current_visitor and random.random() < 0.01:  # Check every update
            for visitor_id, visitor in VISITORS.items():
                if random.random() < visitor.appearance_chance:
                    self.current_visitor = (visitor, datetime.now().isoformat())
                    self.visitor_history.append(visitor_id)
                    return visitor.greeting

        return None

    def get_weather_display(self) -> List[str]:
        """Get ASCII art for current weather."""
        if not self.current_weather:
            return []
        data = WEATHER_DATA.get(self.current_weather.weather_type, {})
        return data.get("ascii", [])

    def get_total_xp_multiplier(self) -> float:
        """Get combined XP multiplier from all sources."""
        multiplier = 1.0

        # Season bonus
        season_content = SEASONAL_CONTENT.get(self.current_season)
        if season_content:
            multiplier *= season_content.xp_bonus

        # Weather bonus
        if self.current_weather:
            multiplier *= self.current_weather.xp_multiplier

        # Fortune bonus
        if self.day_fortune:
            multiplier *= self.day_fortune.xp_multiplier

        return multiplier

    def get_drop_rate_modifier(self) -> float:
        """Get combined drop rate modifier."""
        modifier = 1.0

        # Fortune modifier
        if self.day_fortune:
            modifier *= self.day_fortune.drop_rate_modifier

        # Foggy weather bonus
        if self.current_weather and self.current_weather.weather_type == WeatherType.FOGGY:
            modifier *= 1.5

        return modifier

    def get_mood_modifier(self) -> int:
        """Get combined mood modifier."""
        mood = 0

        if self.current_weather:
            mood += self.current_weather.mood_modifier

        if self.current_visitor:
            mood += self.current_visitor[0].mood_boost

        return mood

    def interact_with_visitor(self) -> Optional[Tuple[str, Optional[str]]]:
        """
        Interact with current visitor.
        Returns (message, gift_item_id) or None if no visitor.
        """
        if not self.current_visitor:
            return None

        visitor, _ = self.current_visitor

        # Check for gift
        gift = None
        if random.random() < visitor.gift_chance and visitor.possible_gifts:
            gift = random.choice(visitor.possible_gifts)
            message = f"{visitor.name}: *gives you something* Here, take this!"
        else:
            responses = [
                f"{visitor.name}: *quacks happily* Nice to meet you!",
                f"{visitor.name}: This is a lovely place you have here!",
                f"{visitor.name}: *nods approvingly* You take good care of Cheese!",
            ]
            message = random.choice(responses)

        return (message, gift)

    def get_seasonal_items(self) -> List[str]:
        """Get items available this season."""
        content = SEASONAL_CONTENT.get(self.current_season)
        return content.items_available if content else []

    def get_status_display(self) -> Dict[str, str]:
        """Get current atmosphere status for display."""
        status = {
            "season": self.current_season.value.title(),
            "weather": "Unknown",
            "fortune": "Normal",
            "visitor": "None",
        }

        if self.current_weather:
            data = WEATHER_DATA.get(self.current_weather.weather_type, {})
            status["weather"] = data.get("name", self.current_weather.weather_type.value)

        if self.day_fortune:
            status["fortune"] = self.day_fortune.fortune_type.replace("_", " ").title()

        if self.current_visitor:
            status["visitor"] = self.current_visitor[0].name

        return status

    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "current_season": self.current_season.value,
            "current_weather": {
                "type": self.current_weather.weather_type.value,
                "intensity": self.current_weather.intensity,
                "duration": self.current_weather.duration_hours,
                "start": self.current_weather.start_time,
            } if self.current_weather else None,
            "day_fortune": {
                "type": self.day_fortune.fortune_type,
                "xp_mult": self.day_fortune.xp_multiplier,
                "drop_mult": self.day_fortune.drop_rate_modifier,
                "message": self.day_fortune.special_message,
                "horoscope": self.day_fortune.horoscope,
            } if self.day_fortune else None,
            "last_fortune_date": self.last_fortune_date,
            "visitor_history": self.visitor_history[-20:],  # Keep last 20
            "weather_history": self.weather_history,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AtmosphereManager":
        """Create from dictionary."""
        atm = cls()

        if data.get("current_season"):
            try:
                atm.current_season = Season(data["current_season"])
            except:
                pass

        if data.get("current_weather"):
            w = data["current_weather"]
            try:
                weather_type = WeatherType(w["type"])
                weather_data = WEATHER_DATA.get(weather_type, {})
                atm.current_weather = Weather(
                    weather_type=weather_type,
                    intensity=w.get("intensity", 0.5),
                    duration_hours=w.get("duration", 3),
                    start_time=w.get("start", datetime.now().isoformat()),
                    mood_modifier=weather_data.get("mood_modifier", 0),
                    xp_multiplier=weather_data.get("xp_multiplier", 1.0),
                    special_message=weather_data.get("message", ""),
                )
            except:
                pass

        if data.get("day_fortune"):
            f = data["day_fortune"]
            atm.day_fortune = DayFortune(
                fortune_type=f.get("type", "normal"),
                xp_multiplier=f.get("xp_mult", 1.0),
                drop_rate_modifier=f.get("drop_mult", 1.0),
                special_message=f.get("message", ""),
                horoscope=f.get("horoscope", ""),
            )

        atm.last_fortune_date = data.get("last_fortune_date")
        atm.visitor_history = data.get("visitor_history", [])
        atm.weather_history = data.get("weather_history", [])

        return atm


# Global instance
atmosphere = AtmosphereManager()
