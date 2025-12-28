"""
Seasonal Clothing System - Season-specific outfits and accessories.
Extends the outfit system with weather-appropriate and holiday-themed clothing.
"""
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random


class Season(Enum):
    """The four seasons."""
    SPRING = "spring"
    SUMMER = "summer"
    AUTUMN = "autumn"
    WINTER = "winter"


class ClothingSlot(Enum):
    """Slots for seasonal clothing."""
    HEAD = "head"
    BODY = "body"
    FEET = "feet"
    ACCESSORY = "accessory"
    SPECIAL = "special"


class SeasonalRarity(Enum):
    """Rarity of seasonal items."""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    LEGENDARY = "legendary"
    EVENT = "event"  # Special event items


class HolidayType(Enum):
    """Holiday themes for special clothing."""
    NEW_YEAR = "new_year"
    VALENTINES = "valentines"
    EASTER = "easter"
    SUMMER_FEST = "summer_fest"
    HALLOWEEN = "halloween"
    THANKSGIVING = "thanksgiving"
    WINTER_HOLIDAY = "winter_holiday"
    BIRTHDAY = "birthday"


@dataclass
class SeasonalItem:
    """A seasonal clothing item."""
    item_id: str
    name: str
    description: str
    slot: ClothingSlot
    season: Optional[Season]  # None = all seasons
    holiday: Optional[HolidayType]  # None = not holiday-specific
    rarity: SeasonalRarity
    ascii_art: List[str]
    weather_bonus: Dict[str, float]  # Bonuses in certain weather
    mood_effect: int  # Mood bonus when worn
    unlock_condition: Optional[str]
    is_obtainable: bool = True


@dataclass
class SeasonalWardrobe:
    """A player's collection of seasonal items."""
    owned_items: List[str] = field(default_factory=list)
    equipped: Dict[str, str] = field(default_factory=dict)  # slot -> item_id
    favorites: List[str] = field(default_factory=list)
    last_outfit_change: Optional[str] = None


# Spring items
SPRING_ITEMS = {
    "spring_flower_crown": SeasonalItem(
        item_id="spring_flower_crown",
        name="Flower Crown",
        description="A beautiful crown of spring flowers",
        slot=ClothingSlot.HEAD,
        season=Season.SPRING,
        holiday=None,
        rarity=SeasonalRarity.COMMON,
        ascii_art=[
            "  🌸🌼🌸  ",
            " 🌷    🌷 ",
        ],
        weather_bonus={"sunny": 0.1, "rainy": 0.05},
        mood_effect=5,
        unlock_condition=None,
    ),
    "spring_rain_boots": SeasonalItem(
        item_id="spring_rain_boots",
        name="Yellow Rain Boots",
        description="Splish splash in style!",
        slot=ClothingSlot.FEET,
        season=Season.SPRING,
        holiday=None,
        rarity=SeasonalRarity.COMMON,
        ascii_art=[
            " |  | |  |",
            " |__| |__|",
        ],
        weather_bonus={"rainy": 0.2, "stormy": 0.1},
        mood_effect=3,
        unlock_condition=None,
    ),
    "spring_raincoat": SeasonalItem(
        item_id="spring_raincoat",
        name="Pastel Raincoat",
        description="Stay dry in this cute raincoat",
        slot=ClothingSlot.BODY,
        season=Season.SPRING,
        holiday=None,
        rarity=SeasonalRarity.UNCOMMON,
        ascii_art=[
            " /------\\ ",
            "/   🦆   \\",
            "\\________/",
        ],
        weather_bonus={"rainy": 0.25, "stormy": 0.15},
        mood_effect=4,
        unlock_condition=None,
    ),
    "spring_butterfly_bow": SeasonalItem(
        item_id="spring_butterfly_bow",
        name="Butterfly Bow",
        description="A bow with butterfly decorations",
        slot=ClothingSlot.ACCESSORY,
        season=Season.SPRING,
        holiday=None,
        rarity=SeasonalRarity.UNCOMMON,
        ascii_art=[
            " 🦋~∞~🦋 ",
        ],
        weather_bonus={"sunny": 0.1},
        mood_effect=6,
        unlock_condition=None,
    ),
    "spring_gardener_hat": SeasonalItem(
        item_id="spring_gardener_hat",
        name="Gardener's Hat",
        description="Perfect for tending the garden",
        slot=ClothingSlot.HEAD,
        season=Season.SPRING,
        holiday=None,
        rarity=SeasonalRarity.RARE,
        ascii_art=[
            "  _____  ",
            " /     \\ ",
            "(  🌱   )",
        ],
        weather_bonus={"sunny": 0.15},
        mood_effect=5,
        unlock_condition="Plant 10 seeds",
    ),
}

# Summer items
SUMMER_ITEMS = {
    "summer_sunglasses": SeasonalItem(
        item_id="summer_sunglasses",
        name="Cool Shades",
        description="Looking cool in the summer sun",
        slot=ClothingSlot.ACCESSORY,
        season=Season.SUMMER,
        holiday=None,
        rarity=SeasonalRarity.COMMON,
        ascii_art=[
            " ⊙─⊙ ",
        ],
        weather_bonus={"sunny": 0.2, "hot": 0.15},
        mood_effect=5,
        unlock_condition=None,
    ),
    "summer_sun_hat": SeasonalItem(
        item_id="summer_sun_hat",
        name="Straw Sun Hat",
        description="A wide-brimmed hat for hot days",
        slot=ClothingSlot.HEAD,
        season=Season.SUMMER,
        holiday=None,
        rarity=SeasonalRarity.COMMON,
        ascii_art=[
            " ╭━━━━━━╮",
            "  \\____/ ",
        ],
        weather_bonus={"sunny": 0.25, "hot": 0.2},
        mood_effect=4,
        unlock_condition=None,
    ),
    "summer_swim_ring": SeasonalItem(
        item_id="summer_swim_ring",
        name="Duck Floatie Ring",
        description="A ring for swimming adventures",
        slot=ClothingSlot.SPECIAL,
        season=Season.SUMMER,
        holiday=None,
        rarity=SeasonalRarity.UNCOMMON,
        ascii_art=[
            " ╭╭────╮╮",
            " ││🦆 ││",
            " ╰╰────╯╯",
        ],
        weather_bonus={"sunny": 0.1},
        mood_effect=8,
        unlock_condition=None,
    ),
    "summer_hawaiian_shirt": SeasonalItem(
        item_id="summer_hawaiian_shirt",
        name="Hawaiian Shirt",
        description="Tropical vibes all day",
        slot=ClothingSlot.BODY,
        season=Season.SUMMER,
        holiday=None,
        rarity=SeasonalRarity.UNCOMMON,
        ascii_art=[
            " ┌🌺🌴🌺┐",
            " │     │",
            " └─────┘",
        ],
        weather_bonus={"hot": 0.1},
        mood_effect=7,
        unlock_condition=None,
    ),
    "summer_flip_flops": SeasonalItem(
        item_id="summer_flip_flops",
        name="Tiny Flip Flops",
        description="Flap flap on duck feet",
        slot=ClothingSlot.FEET,
        season=Season.SUMMER,
        holiday=None,
        rarity=SeasonalRarity.COMMON,
        ascii_art=[
            " Y   Y ",
            " │ ∩ │ ",
        ],
        weather_bonus={"sunny": 0.05},
        mood_effect=3,
        unlock_condition=None,
    ),
    "summer_ice_cream_cone": SeasonalItem(
        item_id="summer_ice_cream_cone",
        name="Ice Cream Cone Hat",
        description="A deliciously silly hat",
        slot=ClothingSlot.HEAD,
        season=Season.SUMMER,
        holiday=None,
        rarity=SeasonalRarity.RARE,
        ascii_art=[
            "   🍦   ",
            "  \\  /  ",
            "   \\/   ",
        ],
        weather_bonus={"hot": 0.3},
        mood_effect=10,
        unlock_condition="Eat 20 treats",
    ),
}

# Autumn items
AUTUMN_ITEMS = {
    "autumn_leaf_crown": SeasonalItem(
        item_id="autumn_leaf_crown",
        name="Autumn Leaf Crown",
        description="A crown of colorful fall leaves",
        slot=ClothingSlot.HEAD,
        season=Season.AUTUMN,
        holiday=None,
        rarity=SeasonalRarity.COMMON,
        ascii_art=[
            " 🍂🍁🍂 ",
            "  \\ | / ",
        ],
        weather_bonus={"cool": 0.1, "windy": 0.1},
        mood_effect=5,
        unlock_condition=None,
    ),
    "autumn_cozy_sweater": SeasonalItem(
        item_id="autumn_cozy_sweater",
        name="Cozy Knit Sweater",
        description="Perfect for chilly autumn days",
        slot=ClothingSlot.BODY,
        season=Season.AUTUMN,
        holiday=None,
        rarity=SeasonalRarity.UNCOMMON,
        ascii_art=[
            " ╭─────╮",
            " │~~~~~│",
            " │~~~~~│",
            " ╰─────╯",
        ],
        weather_bonus={"cool": 0.2, "cold": 0.1},
        mood_effect=6,
        unlock_condition=None,
    ),
    "autumn_scarf": SeasonalItem(
        item_id="autumn_scarf",
        name="Plaid Scarf",
        description="A warm and stylish scarf",
        slot=ClothingSlot.ACCESSORY,
        season=Season.AUTUMN,
        holiday=None,
        rarity=SeasonalRarity.COMMON,
        ascii_art=[
            " ░█░█░ ",
            "  ~~~  ",
        ],
        weather_bonus={"cool": 0.15, "windy": 0.1},
        mood_effect=4,
        unlock_condition=None,
    ),
    "autumn_boots": SeasonalItem(
        item_id="autumn_boots",
        name="Leather Boots",
        description="Sturdy boots for leaf-crunching",
        slot=ClothingSlot.FEET,
        season=Season.AUTUMN,
        holiday=None,
        rarity=SeasonalRarity.COMMON,
        ascii_art=[
            " ┌──┐┌──┐",
            " │  ││  │",
        ],
        weather_bonus={"cool": 0.1, "rainy": 0.1},
        mood_effect=3,
        unlock_condition=None,
    ),
    "autumn_acorn_charm": SeasonalItem(
        item_id="autumn_acorn_charm",
        name="Lucky Acorn Charm",
        description="Brings good fortune",
        slot=ClothingSlot.ACCESSORY,
        season=Season.AUTUMN,
        holiday=None,
        rarity=SeasonalRarity.RARE,
        ascii_art=[
            "   ∩   ",
            "  (🌰)  ",
        ],
        weather_bonus={},
        mood_effect=5,
        unlock_condition="Collect 30 items",
    ),
}

# Winter items
WINTER_ITEMS = {
    "winter_earmuffs": SeasonalItem(
        item_id="winter_earmuffs",
        name="Fluffy Earmuffs",
        description="Keep those ears toasty",
        slot=ClothingSlot.HEAD,
        season=Season.WINTER,
        holiday=None,
        rarity=SeasonalRarity.COMMON,
        ascii_art=[
            " (◯)─(◯)",
        ],
        weather_bonus={"cold": 0.15, "snowy": 0.1},
        mood_effect=4,
        unlock_condition=None,
    ),
    "winter_puffy_coat": SeasonalItem(
        item_id="winter_puffy_coat",
        name="Puffy Winter Coat",
        description="So warm and puffy!",
        slot=ClothingSlot.BODY,
        season=Season.WINTER,
        holiday=None,
        rarity=SeasonalRarity.UNCOMMON,
        ascii_art=[
            " ╭═════╮",
            " ║░░░░░║",
            " ║░░░░░║",
            " ╰═════╯",
        ],
        weather_bonus={"cold": 0.3, "snowy": 0.25, "freezing": 0.2},
        mood_effect=6,
        unlock_condition=None,
    ),
    "winter_snow_boots": SeasonalItem(
        item_id="winter_snow_boots",
        name="Warm Snow Boots",
        description="Perfect for snow adventures",
        slot=ClothingSlot.FEET,
        season=Season.WINTER,
        holiday=None,
        rarity=SeasonalRarity.COMMON,
        ascii_art=[
            " ╔══╗╔══╗",
            " ║⚪║║⚪║",
            " ╚══╝╚══╝",
        ],
        weather_bonus={"snowy": 0.2, "cold": 0.15},
        mood_effect=4,
        unlock_condition=None,
    ),
    "winter_cozy_scarf": SeasonalItem(
        item_id="winter_cozy_scarf",
        name="Knitted Winter Scarf",
        description="Long and super warm",
        slot=ClothingSlot.ACCESSORY,
        season=Season.WINTER,
        holiday=None,
        rarity=SeasonalRarity.COMMON,
        ascii_art=[
            " ≈≈≈≈≈≈ ",
            "  ~~~~  ",
        ],
        weather_bonus={"cold": 0.2, "freezing": 0.15},
        mood_effect=5,
        unlock_condition=None,
    ),
    "winter_mittens": SeasonalItem(
        item_id="winter_mittens",
        name="Fuzzy Mittens",
        description="Warm little wing-warmers",
        slot=ClothingSlot.ACCESSORY,
        season=Season.WINTER,
        holiday=None,
        rarity=SeasonalRarity.UNCOMMON,
        ascii_art=[
            " ╭─╮ ╭─╮",
            " │♥│ │♥│",
            " ╰─╯ ╰─╯",
        ],
        weather_bonus={"cold": 0.15, "snowy": 0.1},
        mood_effect=6,
        unlock_condition=None,
    ),
    "winter_snowflake_crown": SeasonalItem(
        item_id="winter_snowflake_crown",
        name="Snowflake Crown",
        description="A crown of crystalline snowflakes",
        slot=ClothingSlot.HEAD,
        season=Season.WINTER,
        holiday=None,
        rarity=SeasonalRarity.RARE,
        ascii_art=[
            " ❄️✨❄️ ",
            "  \\|/  ",
        ],
        weather_bonus={"snowy": 0.3},
        mood_effect=8,
        unlock_condition="Play 30 snow days",
    ),
}

# Holiday items
HOLIDAY_ITEMS = {
    # Valentine's Day
    "valentine_heart_headband": SeasonalItem(
        item_id="valentine_heart_headband",
        name="Heart Headband",
        description="Love is in the air!",
        slot=ClothingSlot.HEAD,
        season=None,
        holiday=HolidayType.VALENTINES,
        rarity=SeasonalRarity.EVENT,
        ascii_art=[
            " ♥️ ♥️ ♥️ ",
        ],
        weather_bonus={},
        mood_effect=10,
        unlock_condition="Valentine's Day event",
    ),
    "valentine_cupid_wings": SeasonalItem(
        item_id="valentine_cupid_wings",
        name="Cupid Wings",
        description="Tiny wings of love",
        slot=ClothingSlot.SPECIAL,
        season=None,
        holiday=HolidayType.VALENTINES,
        rarity=SeasonalRarity.EVENT,
        ascii_art=[
            " ⟨💕⟩ ",
            "  \\^/ ",
        ],
        weather_bonus={},
        mood_effect=12,
        unlock_condition="Valentine's Day event",
    ),
    
    # Easter
    "easter_bunny_ears": SeasonalItem(
        item_id="easter_bunny_ears",
        name="Bunny Ears",
        description="A duck-bunny crossover!",
        slot=ClothingSlot.HEAD,
        season=None,
        holiday=HolidayType.EASTER,
        rarity=SeasonalRarity.EVENT,
        ascii_art=[
            " (\\  /)",
            "  \\\\// ",
        ],
        weather_bonus={},
        mood_effect=8,
        unlock_condition="Easter event",
    ),
    "easter_egg_basket": SeasonalItem(
        item_id="easter_egg_basket",
        name="Easter Basket",
        description="Filled with colorful eggs",
        slot=ClothingSlot.ACCESSORY,
        season=None,
        holiday=HolidayType.EASTER,
        rarity=SeasonalRarity.EVENT,
        ascii_art=[
            " ╭─🥚🥚─╮",
            "  \\____/ ",
        ],
        weather_bonus={},
        mood_effect=7,
        unlock_condition="Easter event",
    ),
    
    # Halloween
    "halloween_witch_hat": SeasonalItem(
        item_id="halloween_witch_hat",
        name="Witch Hat",
        description="Spooky duck vibes",
        slot=ClothingSlot.HEAD,
        season=None,
        holiday=HolidayType.HALLOWEEN,
        rarity=SeasonalRarity.EVENT,
        ascii_art=[
            "   /\\   ",
            "  /  \\  ",
            " /____\\ ",
        ],
        weather_bonus={"foggy": 0.2},
        mood_effect=9,
        unlock_condition="Halloween event",
    ),
    "halloween_pumpkin_costume": SeasonalItem(
        item_id="halloween_pumpkin_costume",
        name="Pumpkin Costume",
        description="Round and orange!",
        slot=ClothingSlot.BODY,
        season=None,
        holiday=HolidayType.HALLOWEEN,
        rarity=SeasonalRarity.EVENT,
        ascii_art=[
            " ╭─────╮",
            " │ 🎃  │",
            " ╰─────╯",
        ],
        weather_bonus={},
        mood_effect=10,
        unlock_condition="Halloween event",
    ),
    "halloween_ghost_sheet": SeasonalItem(
        item_id="halloween_ghost_sheet",
        name="Ghost Sheet",
        description="Boo! It's a ghost duck!",
        slot=ClothingSlot.BODY,
        season=None,
        holiday=HolidayType.HALLOWEEN,
        rarity=SeasonalRarity.EVENT,
        ascii_art=[
            " ╭─────╮",
            " │ ◉ ◉ │",
            " ╰~~~~~╯",
        ],
        weather_bonus={"foggy": 0.25},
        mood_effect=8,
        unlock_condition="Halloween event",
    ),
    
    # Thanksgiving
    "thanksgiving_pilgrim_hat": SeasonalItem(
        item_id="thanksgiving_pilgrim_hat",
        name="Pilgrim Hat",
        description="Thankful duck!",
        slot=ClothingSlot.HEAD,
        season=None,
        holiday=HolidayType.THANKSGIVING,
        rarity=SeasonalRarity.EVENT,
        ascii_art=[
            "   ___   ",
            "  |   |  ",
            " /-----\\ ",
        ],
        weather_bonus={},
        mood_effect=7,
        unlock_condition="Thanksgiving event",
    ),
    
    # Winter holidays
    "winter_santa_hat": SeasonalItem(
        item_id="winter_santa_hat",
        name="Santa Hat",
        description="Ho ho ho!",
        slot=ClothingSlot.HEAD,
        season=None,
        holiday=HolidayType.WINTER_HOLIDAY,
        rarity=SeasonalRarity.EVENT,
        ascii_art=[
            "    ◯  ",
            "  /   \\ ",
            " (____) ",
        ],
        weather_bonus={"snowy": 0.2},
        mood_effect=12,
        unlock_condition="Winter holiday event",
    ),
    "winter_elf_costume": SeasonalItem(
        item_id="winter_elf_costume",
        name="Elf Costume",
        description="Santa's little helper",
        slot=ClothingSlot.BODY,
        season=None,
        holiday=HolidayType.WINTER_HOLIDAY,
        rarity=SeasonalRarity.EVENT,
        ascii_art=[
            " ╭─🎄─╮",
            " │    │",
            " ╰────╯",
        ],
        weather_bonus={"snowy": 0.15},
        mood_effect=10,
        unlock_condition="Winter holiday event",
    ),
    "winter_reindeer_antlers": SeasonalItem(
        item_id="winter_reindeer_antlers",
        name="Reindeer Antlers",
        description="Ready to fly!",
        slot=ClothingSlot.HEAD,
        season=None,
        holiday=HolidayType.WINTER_HOLIDAY,
        rarity=SeasonalRarity.EVENT,
        ascii_art=[
            "  ∿  ∿  ",
            "  │  │  ",
        ],
        weather_bonus={"snowy": 0.1},
        mood_effect=8,
        unlock_condition="Winter holiday event",
    ),
    
    # New Year
    "newyear_party_hat": SeasonalItem(
        item_id="newyear_party_hat",
        name="Party Hat",
        description="Happy New Year!",
        slot=ClothingSlot.HEAD,
        season=None,
        holiday=HolidayType.NEW_YEAR,
        rarity=SeasonalRarity.EVENT,
        ascii_art=[
            "   ★   ",
            "  /🎊\\  ",
            " /    \\ ",
        ],
        weather_bonus={},
        mood_effect=15,
        unlock_condition="New Year event",
    ),
    "newyear_fancy_glasses": SeasonalItem(
        item_id="newyear_fancy_glasses",
        name="2024 Glasses",
        description="See the new year clearly!",
        slot=ClothingSlot.ACCESSORY,
        season=None,
        holiday=HolidayType.NEW_YEAR,
        rarity=SeasonalRarity.EVENT,
        ascii_art=[
            " [2024] ",
        ],
        weather_bonus={},
        mood_effect=10,
        unlock_condition="New Year event",
    ),
    
    # Birthday
    "birthday_crown": SeasonalItem(
        item_id="birthday_crown",
        name="Birthday Crown",
        description="It's YOUR special day!",
        slot=ClothingSlot.HEAD,
        season=None,
        holiday=HolidayType.BIRTHDAY,
        rarity=SeasonalRarity.EVENT,
        ascii_art=[
            " ★ ♔ ★ ",
        ],
        weather_bonus={},
        mood_effect=20,
        unlock_condition="Duck's birthday",
    ),
    "birthday_sash": SeasonalItem(
        item_id="birthday_sash",
        name="Birthday Sash",
        description="Birthday duck coming through!",
        slot=ClothingSlot.ACCESSORY,
        season=None,
        holiday=HolidayType.BIRTHDAY,
        rarity=SeasonalRarity.EVENT,
        ascii_art=[
            " ╲🎂╱ ",
        ],
        weather_bonus={},
        mood_effect=15,
        unlock_condition="Duck's birthday",
    ),
}

# Combine all items
ALL_SEASONAL_ITEMS = {
    **SPRING_ITEMS,
    **SUMMER_ITEMS,
    **AUTUMN_ITEMS,
    **WINTER_ITEMS,
    **HOLIDAY_ITEMS,
}


def get_current_season() -> Season:
    """Get the current season based on date."""
    month = datetime.now().month
    if month in [3, 4, 5]:
        return Season.SPRING
    elif month in [6, 7, 8]:
        return Season.SUMMER
    elif month in [9, 10, 11]:
        return Season.AUTUMN
    else:
        return Season.WINTER


def get_season_emoji(season: Season) -> str:
    """Get emoji for a season."""
    return {
        Season.SPRING: "🌸",
        Season.SUMMER: "☀️",
        Season.AUTUMN: "🍂",
        Season.WINTER: "❄️",
    }.get(season, "🌍")


class SeasonalClothingSystem:
    """Manages seasonal clothing and outfits."""
    
    def __init__(self):
        self.wardrobe = SeasonalWardrobe()
        self.unlocked_holidays: List[HolidayType] = []
        self.seasonal_shop_refreshed: Optional[str] = None
        self.current_shop_items: List[str] = []
        
    def get_item(self, item_id: str) -> Optional[SeasonalItem]:
        """Get a seasonal item by ID."""
        return ALL_SEASONAL_ITEMS.get(item_id)
        
    def owns_item(self, item_id: str) -> bool:
        """Check if player owns an item."""
        return item_id in self.wardrobe.owned_items
        
    def add_item(self, item_id: str) -> bool:
        """Add an item to the wardrobe."""
        if item_id not in ALL_SEASONAL_ITEMS:
            return False
        if item_id in self.wardrobe.owned_items:
            return False
        self.wardrobe.owned_items.append(item_id)
        return True
        
    def equip_item(self, item_id: str) -> bool:
        """Equip an item."""
        if not self.owns_item(item_id):
            return False
            
        item = self.get_item(item_id)
        if not item:
            return False
            
        self.wardrobe.equipped[item.slot.value] = item_id
        self.wardrobe.last_outfit_change = datetime.now().isoformat()
        return True
        
    def unequip_slot(self, slot: ClothingSlot):
        """Unequip an item from a slot."""
        if slot.value in self.wardrobe.equipped:
            del self.wardrobe.equipped[slot.value]
            
    def get_equipped(self, slot: ClothingSlot) -> Optional[SeasonalItem]:
        """Get the equipped item in a slot."""
        item_id = self.wardrobe.equipped.get(slot.value)
        if item_id:
            return self.get_item(item_id)
        return None
        
    def toggle_favorite(self, item_id: str):
        """Toggle an item as favorite."""
        if item_id in self.wardrobe.favorites:
            self.wardrobe.favorites.remove(item_id)
        else:
            self.wardrobe.favorites.append(item_id)
            
    def get_items_by_season(self, season: Season) -> List[SeasonalItem]:
        """Get all items for a season."""
        return [item for item in ALL_SEASONAL_ITEMS.values() 
                if item.season == season or item.season is None]
        
    def get_items_by_holiday(self, holiday: HolidayType) -> List[SeasonalItem]:
        """Get all items for a holiday."""
        return [item for item in ALL_SEASONAL_ITEMS.values() 
                if item.holiday == holiday]
        
    def get_owned_items(self) -> List[SeasonalItem]:
        """Get all owned items."""
        return [self.get_item(item_id) for item_id in self.wardrobe.owned_items 
                if self.get_item(item_id)]
        
    def get_season_bonus(self, weather: str = "") -> float:
        """Get total bonus from equipped seasonal items."""
        bonus = 0.0
        for item_id in self.wardrobe.equipped.values():
            item = self.get_item(item_id)
            if item and weather in item.weather_bonus:
                bonus += item.weather_bonus[weather]
        return bonus
        
    def get_mood_bonus(self) -> int:
        """Get total mood bonus from equipped items."""
        bonus = 0
        for item_id in self.wardrobe.equipped.values():
            item = self.get_item(item_id)
            if item:
                bonus += item.mood_effect
        return bonus
        
    def get_appropriate_items(self) -> List[SeasonalItem]:
        """Get items appropriate for current season."""
        current = get_current_season()
        appropriate = []
        
        for item_id in self.wardrobe.owned_items:
            item = self.get_item(item_id)
            if not item:
                continue
            if item.season is None or item.season == current:
                appropriate.append(item)
                
        return appropriate
        
    def auto_equip_for_season(self):
        """Auto-equip best items for current season."""
        current = get_current_season()
        appropriate = self.get_appropriate_items()
        
        # Group by slot
        by_slot: Dict[ClothingSlot, List[SeasonalItem]] = {}
        for item in appropriate:
            if item.slot not in by_slot:
                by_slot[item.slot] = []
            by_slot[item.slot].append(item)
            
        # Equip best item in each slot (by mood effect)
        for slot, items in by_slot.items():
            items.sort(key=lambda x: x.mood_effect, reverse=True)
            self.equip_item(items[0].item_id)
            
    def refresh_seasonal_shop(self):
        """Refresh the seasonal shop with new items."""
        current = get_current_season()
        available = [
            item_id for item_id, item in ALL_SEASONAL_ITEMS.items()
            if item.season == current or item.season is None
            and item.holiday is None
            and item.is_obtainable
            and item_id not in self.wardrobe.owned_items
        ]
        
        # Pick 4-6 random items
        num_items = min(len(available), random.randint(4, 6))
        self.current_shop_items = random.sample(available, num_items)
        self.seasonal_shop_refreshed = datetime.now().isoformat()
        
    def unlock_holiday(self, holiday: HolidayType):
        """Unlock holiday items for obtaining."""
        if holiday not in self.unlocked_holidays:
            self.unlocked_holidays.append(holiday)
            
    def get_holiday_items_available(self) -> List[SeasonalItem]:
        """Get holiday items that can currently be obtained."""
        items = []
        for holiday in self.unlocked_holidays:
            items.extend(self.get_items_by_holiday(holiday))
        return items
        
    def render_wardrobe_display(self, width: int = 60) -> List[str]:
        """Render the wardrobe display."""
        lines = []
        current = get_current_season()
        emoji = get_season_emoji(current)
        
        lines.append("╔" + "═" * (width - 2) + "╗")
        lines.append("║" + f" {emoji} Seasonal Wardrobe {emoji} ".center(width - 2) + "║")
        lines.append("║" + f" Current Season: {current.value.title()} ".center(width - 2) + "║")
        lines.append("╠" + "═" * (width - 2) + "╣")
        
        # Currently equipped
        lines.append("║" + " Currently Wearing: ".ljust(width - 2) + "║")
        
        for slot in ClothingSlot:
            equipped = self.get_equipped(slot)
            if equipped:
                lines.append("║" + f"  {slot.value.title()}: {equipped.name}"[:width-3].ljust(width - 2) + "║")
            else:
                lines.append("║" + f"  {slot.value.title()}: (empty)"[:width-3].ljust(width - 2) + "║")
                
        lines.append("╠" + "─" * (width - 2) + "╣")
        
        # Stats
        mood_bonus = self.get_mood_bonus()
        lines.append("║" + f" Outfit Mood Bonus: +{mood_bonus} ".ljust(width - 2) + "║")
        
        lines.append("╠" + "─" * (width - 2) + "╣")
        
        # Collection summary
        total_items = len(ALL_SEASONAL_ITEMS)
        owned = len(self.wardrobe.owned_items)
        
        lines.append("║" + f" Collection: {owned}/{total_items} items ".ljust(width - 2) + "║")
        
        # Season breakdown
        for season in Season:
            s_emoji = get_season_emoji(season)
            season_items = [i for i in ALL_SEASONAL_ITEMS.values() if i.season == season]
            owned_season = [i for i in season_items if i.item_id in self.wardrobe.owned_items]
            lines.append("║" + f"  {s_emoji} {season.value.title()}: {len(owned_season)}/{len(season_items)}"[:width-3].ljust(width - 2) + "║")
            
        # Holiday items
        holiday_items = [i for i in ALL_SEASONAL_ITEMS.values() if i.holiday is not None]
        owned_holiday = [i for i in holiday_items if i.item_id in self.wardrobe.owned_items]
        lines.append("║" + f"  🎉 Holiday: {len(owned_holiday)}/{len(holiday_items)}"[:width-3].ljust(width - 2) + "║")
        
        lines.append("╚" + "═" * (width - 2) + "╝")
        
        return lines
        
    def render_item_card(self, item: SeasonalItem, width: int = 40) -> List[str]:
        """Render a single item card."""
        lines = []
        
        owned = "✓ Owned" if item.item_id in self.wardrobe.owned_items else "✗ Not Owned"
        equipped = "★ Equipped" if item.item_id in self.wardrobe.equipped.values() else ""
        
        lines.append("┌" + "─" * (width - 2) + "┐")
        lines.append("│" + f" {item.name} ".center(width - 2) + "│")
        lines.append("│" + f" [{item.rarity.value.upper()}] ".center(width - 2) + "│")
        lines.append("├" + "─" * (width - 2) + "┤")
        
        # ASCII art
        for art_line in item.ascii_art:
            lines.append("│" + art_line.center(width - 2) + "│")
            
        lines.append("├" + "─" * (width - 2) + "┤")
        
        # Description
        lines.append("│" + item.description[:width-4].center(width - 2) + "│")
        
        lines.append("├" + "─" * (width - 2) + "┤")
        
        # Stats
        lines.append("│" + f" Slot: {item.slot.value.title()} ".ljust(width - 2) + "│")
        lines.append("│" + f" Mood: +{item.mood_effect} ".ljust(width - 2) + "│")
        
        if item.weather_bonus:
            bonuses = ", ".join([f"{k}: +{int(v*100)}%" for k, v in item.weather_bonus.items()])
            lines.append("│" + f" Weather: {bonuses}"[:width-3].ljust(width - 2) + "│")
            
        lines.append("├" + "─" * (width - 2) + "┤")
        lines.append("│" + f" {owned} {equipped} ".center(width - 2) + "│")
        lines.append("└" + "─" * (width - 2) + "┘")
        
        return lines
        
    def to_dict(self) -> Dict:
        """Serialize to dictionary."""
        return {
            "owned_items": self.wardrobe.owned_items,
            "equipped": self.wardrobe.equipped,
            "favorites": self.wardrobe.favorites,
            "last_outfit_change": self.wardrobe.last_outfit_change,
            "unlocked_holidays": [h.value for h in self.unlocked_holidays],
            "seasonal_shop_refreshed": self.seasonal_shop_refreshed,
            "current_shop_items": self.current_shop_items,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "SeasonalClothingSystem":
        """Deserialize from dictionary."""
        system = cls()
        system.wardrobe = SeasonalWardrobe(
            owned_items=data.get("owned_items", []),
            equipped=data.get("equipped", {}),
            favorites=data.get("favorites", []),
            last_outfit_change=data.get("last_outfit_change"),
        )
        system.unlocked_holidays = [HolidayType(h) for h in data.get("unlocked_holidays", [])]
        system.seasonal_shop_refreshed = data.get("seasonal_shop_refreshed")
        system.current_shop_items = data.get("current_shop_items", [])
        return system


# Global instance
seasonal_clothing = SeasonalClothingSystem()
