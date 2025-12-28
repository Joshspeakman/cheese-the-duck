"""
Fortune & Horoscope System - Daily fortunes, zodiac signs, and mystical predictions.
Includes duck zodiac signs, daily horoscopes, lucky items, and fortune cookies.
"""
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random
import hashlib


class DuckZodiacSign(Enum):
    """Duck zodiac signs based on birthday."""
    MALLARD = "mallard"           # Jan 20 - Feb 18 (Aquarius)
    PEKIN = "pekin"               # Feb 19 - Mar 20 (Pisces)
    MUSCOVY = "muscovy"           # Mar 21 - Apr 19 (Aries)
    RUNNER = "runner"             # Apr 20 - May 20 (Taurus)
    CAYUGA = "cayuga"             # May 21 - Jun 20 (Gemini)
    ROUEN = "rouen"               # Jun 21 - Jul 22 (Cancer)
    KHAKI_CAMPBELL = "khaki_campbell"  # Jul 23 - Aug 22 (Leo)
    SWEDISH = "swedish"           # Aug 23 - Sep 22 (Virgo)
    BUFF = "buff"                 # Sep 23 - Oct 22 (Libra)
    MAGPIE = "magpie"             # Oct 23 - Nov 21 (Scorpio)
    CALL = "call"                 # Nov 22 - Dec 21 (Sagittarius)
    WELSH_HARLEQUIN = "welsh_harlequin"  # Dec 22 - Jan 19 (Capricorn)


class FortuneCategory(Enum):
    """Categories of fortune predictions."""
    GENERAL = "general"
    LOVE = "love"
    LUCK = "luck"
    ADVENTURE = "adventure"
    WEALTH = "wealth"
    FRIENDSHIP = "friendship"
    HEALTH = "health"
    WISDOM = "wisdom"


class FortuneRarity(Enum):
    """Rarity of fortune cookies."""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    LEGENDARY = "legendary"


@dataclass
class ZodiacInfo:
    """Information about a duck zodiac sign."""
    sign: DuckZodiacSign
    name: str
    symbol: str
    element: str  # Water, Earth, Fire, Air
    traits: List[str]
    compatible_signs: List[DuckZodiacSign]
    lucky_items: List[str]
    lucky_colors: List[str]
    lucky_numbers: List[int]
    description: str


@dataclass
class DailyHoroscope:
    """A daily horoscope reading."""
    date: str
    sign: DuckZodiacSign
    general_fortune: str
    lucky_item: str
    lucky_color: str
    lucky_number: int
    mood_prediction: str
    activity_suggestion: str
    fortune_level: int  # 1-5 stars
    special_message: Optional[str] = None


@dataclass
class FortuneCookie:
    """A fortune cookie with a message."""
    cookie_id: str
    message: str
    category: FortuneCategory
    rarity: FortuneRarity
    lucky_numbers: List[int]
    date_received: str
    is_revealed: bool = False


@dataclass
class FortuneState:
    """Persistent fortune state."""
    duck_birthday: str  # ISO date string
    zodiac_sign: DuckZodiacSign
    last_horoscope_date: str
    fortune_cookies_collected: List[Dict]
    favorite_fortunes: List[str]
    daily_luck_streak: int
    total_cookies_opened: int
    rare_cookies_found: int
    lucky_events_triggered: int


# Duck zodiac definitions
ZODIAC_INFO = {
    DuckZodiacSign.MALLARD: ZodiacInfo(
        sign=DuckZodiacSign.MALLARD,
        name="The Mallard",
        symbol="🦆",
        element="Air",
        traits=["Free-spirited", "Social", "Adaptable", "Innovative"],
        compatible_signs=[DuckZodiacSign.CAYUGA, DuckZodiacSign.CALL, DuckZodiacSign.BUFF],
        lucky_items=["Feather", "Blue ribbon", "Wind chime"],
        lucky_colors=["Iridescent green", "Sky blue"],
        lucky_numbers=[7, 11, 22],
        description="Mallards are natural leaders with a flair for the unconventional. They swim against the current and inspire others to do the same.",
    ),
    DuckZodiacSign.PEKIN: ZodiacInfo(
        sign=DuckZodiacSign.PEKIN,
        name="The Pekin",
        symbol="🐤",
        element="Water",
        traits=["Dreamy", "Gentle", "Intuitive", "Artistic"],
        compatible_signs=[DuckZodiacSign.ROUEN, DuckZodiacSign.CAYUGA, DuckZodiacSign.SWEDISH],
        lucky_items=["Pearl", "Lily pad", "Moon pendant"],
        lucky_colors=["Pure white", "Pearl pink"],
        lucky_numbers=[3, 9, 12],
        description="Pekins are the dreamers of the duck world. They have deep emotional intelligence and a natural artistic flair.",
    ),
    DuckZodiacSign.MUSCOVY: ZodiacInfo(
        sign=DuckZodiacSign.MUSCOVY,
        name="The Muscovy",
        symbol="💪",
        element="Fire",
        traits=["Bold", "Independent", "Courageous", "Pioneering"],
        compatible_signs=[DuckZodiacSign.KHAKI_CAMPBELL, DuckZodiacSign.CALL, DuckZodiacSign.RUNNER],
        lucky_items=["Red stone", "Sun medal", "Courage token"],
        lucky_colors=["Crimson", "Orange"],
        lucky_numbers=[1, 9, 19],
        description="Muscovys charge ahead where others fear to waddle. Natural pioneers who blaze new trails.",
    ),
    DuckZodiacSign.RUNNER: ZodiacInfo(
        sign=DuckZodiacSign.RUNNER,
        name="The Runner",
        symbol="🏃",
        element="Earth",
        traits=["Determined", "Patient", "Reliable", "Luxurious"],
        compatible_signs=[DuckZodiacSign.SWEDISH, DuckZodiacSign.WELSH_HARLEQUIN, DuckZodiacSign.PEKIN],
        lucky_items=["Garden stone", "Copper coin", "Rose petal"],
        lucky_colors=["Emerald", "Earthy brown"],
        lucky_numbers=[2, 6, 15],
        description="Runners are steady and dependable. They appreciate the finer things and work hard to achieve comfort.",
    ),
    DuckZodiacSign.CAYUGA: ZodiacInfo(
        sign=DuckZodiacSign.CAYUGA,
        name="The Cayuga",
        symbol="🌟",
        element="Air",
        traits=["Curious", "Witty", "Versatile", "Communicative"],
        compatible_signs=[DuckZodiacSign.MALLARD, DuckZodiacSign.BUFF, DuckZodiacSign.CALL],
        lucky_items=["Twin feathers", "Journal", "Lucky dice"],
        lucky_colors=["Beetle green", "Yellow"],
        lucky_numbers=[5, 14, 23],
        description="Cayugas are quick-witted and love to learn. They have beautiful iridescent feathers that shift like their moods.",
    ),
    DuckZodiacSign.ROUEN: ZodiacInfo(
        sign=DuckZodiacSign.ROUEN,
        name="The Rouen",
        symbol="🏠",
        element="Water",
        traits=["Nurturing", "Protective", "Emotional", "Home-loving"],
        compatible_signs=[DuckZodiacSign.PEKIN, DuckZodiacSign.MAGPIE, DuckZodiacSign.SWEDISH],
        lucky_items=["Shell", "Family photo", "Nest material"],
        lucky_colors=["Silver", "Cream"],
        lucky_numbers=[2, 7, 11],
        description="Rouens are the nurturers. They create warm, welcoming spaces and protect those they love fiercely.",
    ),
    DuckZodiacSign.KHAKI_CAMPBELL: ZodiacInfo(
        sign=DuckZodiacSign.KHAKI_CAMPBELL,
        name="The Khaki Campbell",
        symbol="👑",
        element="Fire",
        traits=["Confident", "Generous", "Dramatic", "Warm-hearted"],
        compatible_signs=[DuckZodiacSign.MUSCOVY, DuckZodiacSign.CALL, DuckZodiacSign.BUFF],
        lucky_items=["Gold coin", "Crown charm", "Sunflower"],
        lucky_colors=["Gold", "Khaki"],
        lucky_numbers=[1, 10, 19],
        description="Khaki Campbells are born performers who love the spotlight. They're generous and warm but demand recognition.",
    ),
    DuckZodiacSign.SWEDISH: ZodiacInfo(
        sign=DuckZodiacSign.SWEDISH,
        name="The Swedish",
        symbol="📋",
        element="Earth",
        traits=["Analytical", "Practical", "Helpful", "Detail-oriented"],
        compatible_signs=[DuckZodiacSign.RUNNER, DuckZodiacSign.ROUEN, DuckZodiacSign.WELSH_HARLEQUIN],
        lucky_items=["Checklist", "Blue flower", "Perfect pebble"],
        lucky_colors=["Blue", "Slate grey"],
        lucky_numbers=[3, 6, 27],
        description="Swedish ducks are the organizers. They notice every detail and strive for perfection in all they do.",
    ),
    DuckZodiacSign.BUFF: ZodiacInfo(
        sign=DuckZodiacSign.BUFF,
        name="The Buff",
        symbol="⚖️",
        element="Air",
        traits=["Diplomatic", "Charming", "Fair", "Artistic"],
        compatible_signs=[DuckZodiacSign.CAYUGA, DuckZodiacSign.MALLARD, DuckZodiacSign.KHAKI_CAMPBELL],
        lucky_items=["Balance scale", "Rose quartz", "Art brush"],
        lucky_colors=["Buff", "Pastel pink"],
        lucky_numbers=[4, 13, 22],
        description="Buffs seek harmony in all things. They're natural diplomats with excellent taste and charming personalities.",
    ),
    DuckZodiacSign.MAGPIE: ZodiacInfo(
        sign=DuckZodiacSign.MAGPIE,
        name="The Magpie",
        symbol="🔮",
        element="Water",
        traits=["Mysterious", "Intense", "Passionate", "Perceptive"],
        compatible_signs=[DuckZodiacSign.ROUEN, DuckZodiacSign.PEKIN, DuckZodiacSign.WELSH_HARLEQUIN],
        lucky_items=["Black pearl", "Mystery box", "Obsidian"],
        lucky_colors=["Black", "Deep purple"],
        lucky_numbers=[8, 11, 18],
        description="Magpies are drawn to mystery and secrets. They have intense emotions and see through pretense.",
    ),
    DuckZodiacSign.CALL: ZodiacInfo(
        sign=DuckZodiacSign.CALL,
        name="The Call",
        symbol="🏹",
        element="Fire",
        traits=["Adventurous", "Optimistic", "Philosophical", "Honest"],
        compatible_signs=[DuckZodiacSign.MALLARD, DuckZodiacSign.MUSCOVY, DuckZodiacSign.CAYUGA],
        lucky_items=["Map", "Arrow charm", "Lucky horseshoe"],
        lucky_colors=["Purple", "Turquoise"],
        lucky_numbers=[3, 9, 12],
        description="Calls are the philosophers and adventurers. Their loud voice matches their big dreams and bigger heart.",
    ),
    DuckZodiacSign.WELSH_HARLEQUIN: ZodiacInfo(
        sign=DuckZodiacSign.WELSH_HARLEQUIN,
        name="The Welsh Harlequin",
        symbol="🏔️",
        element="Earth",
        traits=["Ambitious", "Disciplined", "Patient", "Responsible"],
        compatible_signs=[DuckZodiacSign.RUNNER, DuckZodiacSign.SWEDISH, DuckZodiacSign.MAGPIE],
        lucky_items=["Mountain crystal", "Clock charm", "Building block"],
        lucky_colors=["Dark brown", "Forest green"],
        lucky_numbers=[4, 8, 17],
        description="Welsh Harlequins are the builders. Patient and ambitious, they work steadily toward their lofty goals.",
    ),
}

# Fortune cookie messages by category and rarity
FORTUNE_MESSAGES = {
    FortuneCategory.GENERAL: {
        FortuneRarity.COMMON: [
            "Today will be a good day for quacking.",
            "The pond awaits your presence.",
            "A feather in the wind leads to adventure.",
            "Sometimes the best path is the one with the most puddles.",
            "Bread crumbs are a duck's best friend.",
        ],
        FortuneRarity.UNCOMMON: [
            "An unexpected visitor brings good tidings.",
            "The next sunset will bring clarity to your thoughts.",
            "Trust your waddle - it knows the way.",
            "A shiny object will catch your attention soon.",
            "The universe quacks in mysterious ways.",
        ],
        FortuneRarity.RARE: [
            "A golden opportunity lies beneath the surface.",
            "Your feathers will shine with destiny's light.",
            "The stars align in favor of your next adventure.",
            "Something lost shall be found by week's end.",
        ],
        FortuneRarity.LEGENDARY: [
            "You are destined for greatness, little duck.",
            "The legendary Golden Bread awaits those who seek it.",
            "Your quack echoes through the halls of eternity.",
        ],
    },
    FortuneCategory.LOVE: {
        FortuneRarity.COMMON: [
            "Your human thinks of you fondly right now.",
            "Love is found in simple moments of care.",
            "A pet on the head brings joy to the heart.",
        ],
        FortuneRarity.UNCOMMON: [
            "A deep bond will grow stronger this week.",
            "Your affection will be returned tenfold.",
            "The heart knows what the beak cannot say.",
        ],
        FortuneRarity.RARE: [
            "A soulmate watches over you from afar.",
            "Your love creates ripples across the universe.",
        ],
        FortuneRarity.LEGENDARY: [
            "You are loved beyond measure - eternally.",
        ],
    },
    FortuneCategory.LUCK: {
        FortuneRarity.COMMON: [
            "Good luck flows like water today.",
            "Fortune favors the bold duck.",
            "A lucky number will appear soon.",
        ],
        FortuneRarity.UNCOMMON: [
            "Unexpected fortune comes your way.",
            "The odds are ever in your favor.",
            "Lucky finds await the patient seeker.",
        ],
        FortuneRarity.RARE: [
            "A four-leaf clover blooms in your path.",
            "Lady Luck has taken notice of you.",
        ],
        FortuneRarity.LEGENDARY: [
            "You ARE luck incarnate.",
        ],
    },
    FortuneCategory.ADVENTURE: {
        FortuneRarity.COMMON: [
            "A new path opens before you.",
            "Adventure is just a waddle away.",
            "The world is your pond.",
        ],
        FortuneRarity.UNCOMMON: [
            "An exciting journey awaits beyond the familiar.",
            "Discovery comes to those who explore.",
            "Uncharted waters call your name.",
        ],
        FortuneRarity.RARE: [
            "A legendary quest shall present itself.",
            "The greatest adventure of your life approaches.",
        ],
        FortuneRarity.LEGENDARY: [
            "You shall explore realms yet undreamed of.",
        ],
    },
    FortuneCategory.WEALTH: {
        FortuneRarity.COMMON: [
            "A small treasure hides nearby.",
            "Wealth comes in many forms - including bread.",
            "Your collection grows steadily.",
        ],
        FortuneRarity.UNCOMMON: [
            "A generous gift approaches.",
            "Investment in friendship pays the highest dividends.",
            "Abundance flows to the grateful duck.",
        ],
        FortuneRarity.RARE: [
            "Riches beyond bread await your discovery.",
            "A fortune in coins shall be yours.",
        ],
        FortuneRarity.LEGENDARY: [
            "You shall want for nothing, ever.",
        ],
    },
    FortuneCategory.FRIENDSHIP: {
        FortuneRarity.COMMON: [
            "A friend thinks of you today.",
            "Friendship makes the pond brighter.",
            "Share your bread, share your joy.",
        ],
        FortuneRarity.UNCOMMON: [
            "A new friend awaits introduction.",
            "Old friends return with happy news.",
            "Your flock grows stronger together.",
        ],
        FortuneRarity.RARE: [
            "A friendship forged now shall last forever.",
            "You are the friend everyone hopes to find.",
        ],
        FortuneRarity.LEGENDARY: [
            "Your friendships shape the very stars.",
        ],
    },
    FortuneCategory.HEALTH: {
        FortuneRarity.COMMON: [
            "Healthy feathers, happy duck.",
            "A good preen keeps problems at bay.",
            "Rest well to waddle far.",
        ],
        FortuneRarity.UNCOMMON: [
            "Vitality surges through your wings.",
            "Your energy shall know no bounds today.",
            "Balance in all things brings wellness.",
        ],
        FortuneRarity.RARE: [
            "Peak condition is your natural state.",
            "You radiate with vibrant health.",
        ],
        FortuneRarity.LEGENDARY: [
            "You are blessed with eternal vigor.",
        ],
    },
    FortuneCategory.WISDOM: {
        FortuneRarity.COMMON: [
            "The wise duck listens before quacking.",
            "Patience is a virtue, even for ducks.",
            "Learn from yesterday, hope for tomorrow.",
        ],
        FortuneRarity.UNCOMMON: [
            "Deep thoughts lead to greater understanding.",
            "The answer you seek lies within.",
            "Wisdom comes to those who observe.",
        ],
        FortuneRarity.RARE: [
            "You carry knowledge beyond your years.",
            "Others seek your counsel for good reason.",
        ],
        FortuneRarity.LEGENDARY: [
            "You are a sage among ducks.",
        ],
    },
}

# Daily horoscope templates
HOROSCOPE_TEMPLATES = {
    1: [  # Very poor fortune
        "The stars suggest a day of rest. Stay close to home and avoid unnecessary risks.",
        "A challenging day lies ahead. Find comfort in familiar routines.",
        "The cosmic energies are scrambled. Best to keep expectations low today.",
    ],
    2: [  # Below average
        "A slightly bumpy day ahead. Patience will be your greatest ally.",
        "Minor obstacles may appear. Face them with resilience.",
        "The universe tests your resolve today. Stay strong, little duck.",
    ],
    3: [  # Average
        "A balanced day awaits. Neither great nor poor - embrace the ordinary.",
        "The stars shine neutrally. Make of today what you will.",
        "Average energies surround you. A good day for steady progress.",
    ],
    4: [  # Above average
        "Good fortune flows your way! Seize opportunities as they appear.",
        "The stars smile upon you today. Take confident action.",
        "Positive energy surrounds you. A wonderful day for new beginnings.",
    ],
    5: [  # Excellent fortune
        "AMAZING! The stars align perfectly! Today is YOUR day!",
        "Cosmic forces conspire in your favor! Embrace every moment!",
        "A legendary day awaits! Nothing can stop you now!",
    ],
}

MOOD_PREDICTIONS = [
    "cheerful and energetic",
    "calm and contemplative",
    "playful and mischievous",
    "cuddly and affectionate",
    "adventurous and bold",
    "peaceful and serene",
    "curious and explorative",
    "cozy and content",
]

ACTIVITY_SUGGESTIONS = [
    "take a relaxing swim",
    "explore somewhere new",
    "spend quality time with your human",
    "practice your favorite trick",
    "hunt for hidden treasures",
    "make a new friend",
    "rest and recharge",
    "enjoy a delicious meal",
    "splash in puddles",
    "collect shiny things",
    "preen your feathers extra thoroughly",
    "try something you've never done before",
]


def get_zodiac_sign(birthday: date) -> DuckZodiacSign:
    """Determine zodiac sign from birthday."""
    month, day = birthday.month, birthday.day
    
    if (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return DuckZodiacSign.MALLARD
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return DuckZodiacSign.PEKIN
    elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return DuckZodiacSign.MUSCOVY
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return DuckZodiacSign.RUNNER
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return DuckZodiacSign.CAYUGA
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return DuckZodiacSign.ROUEN
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return DuckZodiacSign.KHAKI_CAMPBELL
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return DuckZodiacSign.SWEDISH
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return DuckZodiacSign.BUFF
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return DuckZodiacSign.MAGPIE
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return DuckZodiacSign.CALL
    else:
        return DuckZodiacSign.WELSH_HARLEQUIN


def generate_daily_seed(date_obj: date, sign: DuckZodiacSign) -> int:
    """Generate a deterministic seed for daily fortune based on date and sign."""
    seed_string = f"{date_obj.isoformat()}-{sign.value}"
    return int(hashlib.md5(seed_string.encode()).hexdigest()[:8], 16)


class FortuneSystem:
    """Manages fortunes, horoscopes, and predictions."""
    
    def __init__(self):
        self.duck_birthday: Optional[date] = None
        self.zodiac_sign: Optional[DuckZodiacSign] = None
        self.last_horoscope_date: Optional[date] = None
        self.fortune_cookies: List[FortuneCookie] = []
        self.favorite_fortunes: List[str] = []
        self.daily_luck_streak: int = 0
        self.total_cookies_opened: int = 0
        self.rare_cookies_found: int = 0
        self.lucky_events_triggered: int = 0
        
    def set_duck_birthday(self, birthday: date):
        """Set the duck's birthday and determine zodiac sign."""
        self.duck_birthday = birthday
        self.zodiac_sign = get_zodiac_sign(birthday)
        
    def get_zodiac_info(self) -> Optional[ZodiacInfo]:
        """Get the duck's zodiac information."""
        if self.zodiac_sign:
            return ZODIAC_INFO.get(self.zodiac_sign)
        return None
        
    def generate_daily_horoscope(self, for_date: Optional[date] = None) -> Optional[DailyHoroscope]:
        """Generate a daily horoscope for the duck."""
        if not self.zodiac_sign:
            return None
            
        target_date = for_date or date.today()
        
        # Use deterministic seed for consistent daily fortune
        seed = generate_daily_seed(target_date, self.zodiac_sign)
        rng = random.Random(seed)
        
        zodiac_info = ZODIAC_INFO[self.zodiac_sign]
        
        # Determine fortune level (1-5 stars)
        # Slightly biased toward positive fortunes
        fortune_weights = [0.1, 0.2, 0.3, 0.25, 0.15]
        fortune_level = rng.choices([1, 2, 3, 4, 5], weights=fortune_weights)[0]
        
        # Generate horoscope content
        general_fortune = rng.choice(HOROSCOPE_TEMPLATES[fortune_level])
        lucky_item = rng.choice(zodiac_info.lucky_items)
        lucky_color = rng.choice(zodiac_info.lucky_colors)
        lucky_number = rng.choice(zodiac_info.lucky_numbers)
        mood_prediction = rng.choice(MOOD_PREDICTIONS)
        activity_suggestion = rng.choice(ACTIVITY_SUGGESTIONS)
        
        # Special message on certain days
        special_message = None
        day_of_year = target_date.timetuple().tm_yday
        
        if target_date.month == self.duck_birthday.month and target_date.day == self.duck_birthday.day:
            special_message = "🎂 HAPPY BIRTHDAY! The stars shower you with extra blessings today! 🎂"
            fortune_level = 5  # Birthday is always max fortune!
        elif day_of_year % 7 == 0:
            special_message = "✨ Weekly fortune boost! Something special may happen! ✨"
        elif fortune_level == 5:
            special_message = "🌟 A truly LEGENDARY day! Make it count! 🌟"
            
        horoscope = DailyHoroscope(
            date=target_date.isoformat(),
            sign=self.zodiac_sign,
            general_fortune=general_fortune,
            lucky_item=lucky_item,
            lucky_color=lucky_color,
            lucky_number=lucky_number,
            mood_prediction=mood_prediction,
            activity_suggestion=activity_suggestion,
            fortune_level=fortune_level,
            special_message=special_message,
        )
        
        self.last_horoscope_date = target_date
        
        # Track luck streak
        if fortune_level >= 4:
            self.daily_luck_streak += 1
        else:
            self.daily_luck_streak = 0
            
        return horoscope
        
    def get_fortune_cookie(self) -> FortuneCookie:
        """Open a fortune cookie and get a message."""
        # Determine rarity
        rarity_roll = random.random()
        if rarity_roll < 0.02:  # 2% legendary
            rarity = FortuneRarity.LEGENDARY
            self.rare_cookies_found += 1
        elif rarity_roll < 0.12:  # 10% rare
            rarity = FortuneRarity.RARE
            self.rare_cookies_found += 1
        elif rarity_roll < 0.37:  # 25% uncommon
            rarity = FortuneRarity.UNCOMMON
        else:  # 63% common
            rarity = FortuneRarity.COMMON
            
        # Pick random category
        category = random.choice(list(FortuneCategory))
        
        # Get message
        messages = FORTUNE_MESSAGES[category][rarity]
        message = random.choice(messages)
        
        # Generate lucky numbers
        lucky_numbers = sorted(random.sample(range(1, 50), 3))
        
        cookie = FortuneCookie(
            cookie_id=f"cookie_{self.total_cookies_opened + 1}",
            message=message,
            category=category,
            rarity=rarity,
            lucky_numbers=lucky_numbers,
            date_received=datetime.now().isoformat(),
            is_revealed=True,
        )
        
        self.fortune_cookies.append(cookie)
        self.total_cookies_opened += 1
        
        return cookie
        
    def add_favorite_fortune(self, cookie_id: str):
        """Mark a fortune as favorite."""
        if cookie_id not in self.favorite_fortunes:
            self.favorite_fortunes.append(cookie_id)
            
    def remove_favorite_fortune(self, cookie_id: str):
        """Remove a fortune from favorites."""
        if cookie_id in self.favorite_fortunes:
            self.favorite_fortunes.remove(cookie_id)
            
    def get_compatibility(self, other_sign: DuckZodiacSign) -> Tuple[int, str]:
        """Check compatibility with another zodiac sign."""
        if not self.zodiac_sign:
            return (0, "Unknown")
            
        my_info = ZODIAC_INFO[self.zodiac_sign]
        
        if other_sign in my_info.compatible_signs:
            return (100, "Perfect Match! 💕")
        
        # Check if signs share element
        other_info = ZODIAC_INFO[other_sign]
        if my_info.element == other_info.element:
            return (75, "Great compatibility! 🌟")
            
        # Check element compatibility
        compatible_elements = {
            "Fire": ["Air"],
            "Air": ["Fire"],
            "Water": ["Earth"],
            "Earth": ["Water"],
        }
        
        if other_info.element in compatible_elements.get(my_info.element, []):
            return (60, "Good potential! ✨")
            
        return (40, "Challenging but possible 🤔")
        
    def get_daily_bonus(self) -> Dict[str, float]:
        """Get today's horoscope-based bonuses."""
        if not self.zodiac_sign:
            return {}
            
        today_horoscope = self.generate_daily_horoscope()
        if not today_horoscope:
            return {}
            
        fortune_level = today_horoscope.fortune_level
        
        bonuses = {
            "luck_multiplier": 0.8 + (fortune_level * 0.1),  # 0.9 to 1.3
            "coin_bonus": (fortune_level - 3) * 0.05,  # -0.1 to +0.1
            "xp_bonus": (fortune_level - 3) * 0.05,
            "find_chance_bonus": (fortune_level - 3) * 0.02,
        }
        
        # Streak bonus
        if self.daily_luck_streak >= 3:
            bonuses["luck_multiplier"] += 0.05
        if self.daily_luck_streak >= 7:
            bonuses["coin_bonus"] += 0.05
            
        return bonuses
        
    def render_zodiac_display(self, width: int = 60) -> List[str]:
        """Render the zodiac sign information display."""
        lines = []
        
        if not self.zodiac_sign:
            lines.append("╔" + "═" * (width - 2) + "╗")
            lines.append("║" + " No birthday set! ".center(width - 2) + "║")
            lines.append("╚" + "═" * (width - 2) + "╝")
            return lines
            
        info = ZODIAC_INFO[self.zodiac_sign]
        
        lines.append("╔" + "═" * (width - 2) + "╗")
        lines.append("║" + f" {info.symbol} {info.name} {info.symbol} ".center(width - 2) + "║")
        lines.append("║" + f" Element: {info.element} ".center(width - 2) + "║")
        lines.append("╠" + "═" * (width - 2) + "╣")
        
        lines.append("║" + " Traits: ".ljust(width - 2) + "║")
        traits_str = ", ".join(info.traits)
        lines.append("║" + f"  {traits_str}"[:width-3].ljust(width - 2) + "║")
        
        lines.append("╠" + "─" * (width - 2) + "╣")
        
        lines.append("║" + " Lucky Items: ".ljust(width - 2) + "║")
        for item in info.lucky_items:
            lines.append("║" + f"  • {item}"[:width-3].ljust(width - 2) + "║")
            
        lines.append("╠" + "─" * (width - 2) + "╣")
        
        colors_str = ", ".join(info.lucky_colors)
        lines.append("║" + f" Lucky Colors: {colors_str}"[:width-3].ljust(width - 2) + "║")
        
        numbers_str = ", ".join(str(n) for n in info.lucky_numbers)
        lines.append("║" + f" Lucky Numbers: {numbers_str}"[:width-3].ljust(width - 2) + "║")
        
        lines.append("╠" + "─" * (width - 2) + "╣")
        
        lines.append("║" + " Compatible Signs: ".ljust(width - 2) + "║")
        for sign in info.compatible_signs:
            compat_info = ZODIAC_INFO[sign]
            lines.append("║" + f"  {compat_info.symbol} {compat_info.name}"[:width-3].ljust(width - 2) + "║")
            
        lines.append("╠" + "─" * (width - 2) + "╣")
        
        # Wrap description
        desc = info.description
        while desc:
            lines.append("║ " + desc[:width-4].ljust(width - 3) + "║")
            desc = desc[width-4:]
            
        lines.append("╚" + "═" * (width - 2) + "╝")
        
        return lines
        
    def render_horoscope_display(self, horoscope: DailyHoroscope, width: int = 60) -> List[str]:
        """Render a daily horoscope display."""
        lines = []
        
        info = ZODIAC_INFO[horoscope.sign]
        stars = "⭐" * horoscope.fortune_level + "☆" * (5 - horoscope.fortune_level)
        
        lines.append("╔" + "═" * (width - 2) + "╗")
        lines.append("║" + f" {info.symbol} Daily Horoscope {info.symbol} ".center(width - 2) + "║")
        lines.append("║" + f" {horoscope.date} ".center(width - 2) + "║")
        lines.append("╠" + "═" * (width - 2) + "╣")
        
        lines.append("║" + f" Fortune: {stars} ".center(width - 2) + "║")
        
        if horoscope.special_message:
            lines.append("╠" + "─" * (width - 2) + "╣")
            lines.append("║" + horoscope.special_message[:width-4].center(width - 2) + "║")
            
        lines.append("╠" + "─" * (width - 2) + "╣")
        
        # Wrap general fortune
        fortune = horoscope.general_fortune
        while fortune:
            lines.append("║ " + fortune[:width-4].ljust(width - 3) + "║")
            fortune = fortune[width-4:]
            
        lines.append("╠" + "─" * (width - 2) + "╣")
        
        lines.append("║" + f" 🎨 Lucky Color: {horoscope.lucky_color}"[:width-3].ljust(width - 2) + "║")
        lines.append("║" + f" 🎁 Lucky Item: {horoscope.lucky_item}"[:width-3].ljust(width - 2) + "║")
        lines.append("║" + f" 🔢 Lucky Number: {horoscope.lucky_number}"[:width-3].ljust(width - 2) + "║")
        
        lines.append("╠" + "─" * (width - 2) + "╣")
        
        lines.append("║" + f" Mood: {horoscope.mood_prediction}"[:width-3].ljust(width - 2) + "║")
        lines.append("║" + f" Suggestion: {horoscope.activity_suggestion}"[:width-3].ljust(width - 2) + "║")
        
        lines.append("╚" + "═" * (width - 2) + "╝")
        
        return lines
        
    def render_fortune_cookie_display(self, cookie: FortuneCookie, width: int = 50) -> List[str]:
        """Render a fortune cookie display."""
        lines = []
        
        rarity_symbols = {
            FortuneRarity.COMMON: "🥠",
            FortuneRarity.UNCOMMON: "🥠✨",
            FortuneRarity.RARE: "🥠🌟",
            FortuneRarity.LEGENDARY: "🥠👑",
        }
        
        rarity_str = rarity_symbols.get(cookie.rarity, "🥠")
        
        lines.append("╔" + "═" * (width - 2) + "╗")
        lines.append("║" + f" {rarity_str} Fortune Cookie {rarity_str} ".center(width - 2) + "║")
        lines.append("║" + f" [{cookie.rarity.value.upper()}] ".center(width - 2) + "║")
        lines.append("╠" + "═" * (width - 2) + "╣")
        
        # Wrap message
        message = cookie.message
        while message:
            lines.append("║ " + message[:width-4].ljust(width - 3) + "║")
            message = message[width-4:]
            
        lines.append("╠" + "─" * (width - 2) + "╣")
        
        numbers_str = " - ".join(str(n) for n in cookie.lucky_numbers)
        lines.append("║" + f" Lucky Numbers: {numbers_str} ".center(width - 2) + "║")
        
        lines.append("╚" + "═" * (width - 2) + "╝")
        
        return lines
        
    def to_dict(self) -> Dict:
        """Serialize to dictionary for saving."""
        return {
            "duck_birthday": self.duck_birthday.isoformat() if self.duck_birthday else None,
            "zodiac_sign": self.zodiac_sign.value if self.zodiac_sign else None,
            "last_horoscope_date": self.last_horoscope_date.isoformat() if self.last_horoscope_date else None,
            "fortune_cookies": [
                {
                    "cookie_id": c.cookie_id,
                    "message": c.message,
                    "category": c.category.value,
                    "rarity": c.rarity.value,
                    "lucky_numbers": c.lucky_numbers,
                    "date_received": c.date_received,
                    "is_revealed": c.is_revealed,
                }
                for c in self.fortune_cookies[-50:]  # Keep last 50 cookies
            ],
            "favorite_fortunes": self.favorite_fortunes,
            "daily_luck_streak": self.daily_luck_streak,
            "total_cookies_opened": self.total_cookies_opened,
            "rare_cookies_found": self.rare_cookies_found,
            "lucky_events_triggered": self.lucky_events_triggered,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "FortuneSystem":
        """Deserialize from dictionary."""
        system = cls()
        if data.get("duck_birthday"):
            system.duck_birthday = date.fromisoformat(data["duck_birthday"])
        if data.get("zodiac_sign"):
            system.zodiac_sign = DuckZodiacSign(data["zodiac_sign"])
        if data.get("last_horoscope_date"):
            system.last_horoscope_date = date.fromisoformat(data["last_horoscope_date"])
            
        system.fortune_cookies = []
        for c_data in data.get("fortune_cookies", []):
            system.fortune_cookies.append(FortuneCookie(
                cookie_id=c_data["cookie_id"],
                message=c_data["message"],
                category=FortuneCategory(c_data["category"]),
                rarity=FortuneRarity(c_data["rarity"]),
                lucky_numbers=c_data["lucky_numbers"],
                date_received=c_data["date_received"],
                is_revealed=c_data.get("is_revealed", True),
            ))
            
        system.favorite_fortunes = data.get("favorite_fortunes", [])
        system.daily_luck_streak = data.get("daily_luck_streak", 0)
        system.total_cookies_opened = data.get("total_cookies_opened", 0)
        system.rare_cookies_found = data.get("rare_cookies_found", 0)
        system.lucky_events_triggered = data.get("lucky_events_triggered", 0)
        return system


# Global instance
fortune_system = FortuneSystem()
