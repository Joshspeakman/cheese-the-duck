"""
Duck Home/Nest customization system.
Allows players to decorate and upgrade the duck's living space.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random


class DecorationSlot(Enum):
    """Slots where decorations can be placed."""
    NEST = "nest"
    FLOOR_LEFT = "floor_left"
    FLOOR_RIGHT = "floor_right"
    WALL_LEFT = "wall_left"
    WALL_RIGHT = "wall_right"
    CEILING = "ceiling"
    WATER = "water"


@dataclass
class Decoration:
    """A decoration item for the home."""
    id: str
    name: str
    description: str
    slot: DecorationSlot
    ascii_art: List[str]  # Small ASCII representation
    mood_bonus: int = 0
    rarity: str = "common"
    unlocked: bool = False
    unlock_condition: str = ""


# Available decorations
DECORATIONS = {
    # Nest upgrades
    "basic_nest": Decoration(
        id="basic_nest",
        name="Basic Nest",
        description="A simple but cozy nest",
        slot=DecorationSlot.NEST,
        ascii_art=["\\___/"],
        mood_bonus=0,
        unlocked=True,
    ),
    "cozy_nest": Decoration(
        id="cozy_nest",
        name="Cozy Nest",
        description="Extra soft with feather lining",
        slot=DecorationSlot.NEST,
        ascii_art=["\\~*~/"],
        mood_bonus=5,
        rarity="uncommon",
        unlock_condition="Reach level 5",
    ),
    "luxury_nest": Decoration(
        id="luxury_nest",
        name="Luxury Nest",
        description="Fit for duck royalty",
        slot=DecorationSlot.NEST,
        ascii_art=["\\***/ "],
        mood_bonus=15,
        rarity="rare",
        unlock_condition="Reach level 15",
    ),
    "golden_nest": Decoration(
        id="golden_nest",
        name="Golden Nest",
        description="Made of dreams and sparkles",
        slot=DecorationSlot.NEST,
        ascii_art=["\\@#@/"],
        mood_bonus=30,
        rarity="legendary",
        unlock_condition="Reach level 30",
    ),

    # Floor decorations
    "small_pond": Decoration(
        id="small_pond",
        name="Mini Pond",
        description="A tiny splash zone",
        slot=DecorationSlot.WATER,
        ascii_art=["~~~~~", " ~~~ "],
        mood_bonus=10,
        rarity="uncommon",
        unlock_condition="Play 50 times",
    ),
    "flower_patch": Decoration(
        id="flower_patch",
        name="Flower Patch",
        description="Pretty flowers!",
        slot=DecorationSlot.FLOOR_LEFT,
        ascii_art=["*,*,*"],
        mood_bonus=5,
        unlock_condition="Feed 20 times",
    ),
    "pebble_collection": Decoration(
        id="pebble_collection",
        name="Pebble Collection",
        description="Shiny rocks arranged nicely",
        slot=DecorationSlot.FLOOR_RIGHT,
        ascii_art=["o.o.o"],
        mood_bonus=3,
        unlocked=True,
    ),
    "food_bowl": Decoration(
        id="food_bowl",
        name="Fancy Food Bowl",
        description="Always has snacks nearby",
        slot=DecorationSlot.FLOOR_LEFT,
        ascii_art=["(===)"],
        mood_bonus=8,
        rarity="uncommon",
        unlock_condition="Feed 100 times",
    ),
    "toy_box": Decoration(
        id="toy_box",
        name="Toy Box",
        description="Full of fun things!",
        slot=DecorationSlot.FLOOR_RIGHT,
        ascii_art=["[TOY]"],
        mood_bonus=10,
        rarity="uncommon",
        unlock_condition="Collect 5 toys",
    ),

    # Wall decorations
    "family_photo": Decoration(
        id="family_photo",
        name="Family Photo",
        description="A photo of you and Cheese",
        slot=DecorationSlot.WALL_LEFT,
        ascii_art=["[^^]"],
        mood_bonus=15,
        rarity="rare",
        unlock_condition="30 day streak",
    ),
    "duck_poster": Decoration(
        id="duck_poster",
        name="Duck Poster",
        description="'Believe in yourself' - Duck",
        slot=DecorationSlot.WALL_RIGHT,
        ascii_art=["[DK]"],
        mood_bonus=5,
        unlocked=True,
    ),
    "achievement_wall": Decoration(
        id="achievement_wall",
        name="Achievement Wall",
        description="Shows off your badges",
        slot=DecorationSlot.WALL_LEFT,
        ascii_art=["[!!]"],
        mood_bonus=10,
        rarity="uncommon",
        unlock_condition="Earn 10 achievements",
    ),
    "window": Decoration(
        id="window",
        name="Sunny Window",
        description="Lets in natural light",
        slot=DecorationSlot.WALL_RIGHT,
        ascii_art=["[##]"],
        mood_bonus=8,
        rarity="uncommon",
        unlock_condition="Reach level 10",
    ),

    # Ceiling decorations
    "fairy_lights": Decoration(
        id="fairy_lights",
        name="Fairy Lights",
        description="Sparkly and magical",
        slot=DecorationSlot.CEILING,
        ascii_art=["*-*-*-*"],
        mood_bonus=12,
        rarity="rare",
        unlock_condition="Find Golden Feather",
    ),
    "mobile": Decoration(
        id="mobile",
        name="Duck Mobile",
        description="Little ducks spinning around",
        slot=DecorationSlot.CEILING,
        ascii_art=["o-O-o"],
        mood_bonus=7,
        rarity="uncommon",
        unlock_condition="Reach level 7",
    ),
    "chandelier": Decoration(
        id="chandelier",
        name="Mini Chandelier",
        description="Fancy lighting!",
        slot=DecorationSlot.CEILING,
        ascii_art=["\\|/"],
        mood_bonus=20,
        rarity="legendary",
        unlock_condition="Reach level 40",
    ),
}


# Home themes that change the overall look
HOME_THEMES = {
    "default": {
        "name": "Classic Pond",
        "description": "A simple, cozy pond home",
        "border_char": "~",
        "floor_char": ".",
        "unlocked": True,
    },
    "forest": {
        "name": "Forest Hideaway",
        "description": "Surrounded by trees",
        "border_char": "|",
        "floor_char": ",",
        "unlock_condition": "Reach level 10",
    },
    "beach": {
        "name": "Beach Paradise",
        "description": "Sandy and sunny",
        "border_char": "~",
        "floor_char": ":",
        "unlock_condition": "7 day streak",
    },
    "space": {
        "name": "Space Station",
        "description": "Duck in spaaaaace!",
        "border_char": "*",
        "floor_char": " ",
        "unlock_condition": "Reach level 25",
    },
    "castle": {
        "name": "Duck Castle",
        "description": "Royal accommodations",
        "border_char": "#",
        "floor_char": "_",
        "unlock_condition": "Reach level 50",
    },
}


class DuckHome:
    """
    Manages the duck's home/living space customization.
    """

    def __init__(self):
        self.theme: str = "default"
        self.decorations: Dict[str, str] = {
            # slot -> decoration_id
            DecorationSlot.NEST.value: "basic_nest",
        }
        self.unlocked_decorations: List[str] = ["basic_nest", "pebble_collection", "duck_poster"]
        self.unlocked_themes: List[str] = ["default"]

        # Home stats
        self.total_mood_bonus: int = 0
        self._calculate_mood_bonus()

    def _calculate_mood_bonus(self):
        """Calculate total mood bonus from decorations."""
        self.total_mood_bonus = 0
        for dec_id in self.decorations.values():
            if dec_id in DECORATIONS:
                self.total_mood_bonus += DECORATIONS[dec_id].mood_bonus

    def place_decoration(self, decoration_id: str) -> bool:
        """
        Place a decoration in its designated slot.
        Returns True if successful.
        """
        if decoration_id not in self.unlocked_decorations:
            return False

        if decoration_id not in DECORATIONS:
            return False

        dec = DECORATIONS[decoration_id]
        self.decorations[dec.slot.value] = decoration_id
        self._calculate_mood_bonus()
        return True

    def remove_decoration(self, slot: str) -> bool:
        """Remove decoration from a slot."""
        if slot in self.decorations:
            del self.decorations[slot]
            self._calculate_mood_bonus()
            return True
        return False

    def unlock_decoration(self, decoration_id: str) -> bool:
        """Unlock a decoration."""
        if decoration_id in self.unlocked_decorations:
            return False
        if decoration_id not in DECORATIONS:
            return False

        self.unlocked_decorations.append(decoration_id)
        return True

    def set_theme(self, theme_id: str) -> bool:
        """Set the home theme."""
        if theme_id not in self.unlocked_themes:
            return False
        if theme_id not in HOME_THEMES:
            return False

        self.theme = theme_id
        return True

    def unlock_theme(self, theme_id: str) -> bool:
        """Unlock a theme."""
        if theme_id in self.unlocked_themes:
            return False
        if theme_id not in HOME_THEMES:
            return False

        self.unlocked_themes.append(theme_id)
        return True

    def get_decoration_at(self, slot: str) -> Optional[Decoration]:
        """Get the decoration at a slot."""
        dec_id = self.decorations.get(slot)
        if dec_id:
            return DECORATIONS.get(dec_id)
        return None

    def get_available_decorations(self, slot: DecorationSlot) -> List[Decoration]:
        """Get all unlocked decorations for a slot."""
        return [
            DECORATIONS[dec_id]
            for dec_id in self.unlocked_decorations
            if dec_id in DECORATIONS and DECORATIONS[dec_id].slot == slot
        ]

    def render_home_preview(self, width: int = 30) -> List[str]:
        """Render a preview of the current home setup."""
        theme = HOME_THEMES.get(self.theme, HOME_THEMES["default"])
        border = theme["border_char"]
        floor = theme["floor_char"]

        lines = []

        # Ceiling
        ceiling_dec = self.get_decoration_at(DecorationSlot.CEILING.value)
        ceiling_art = ceiling_dec.ascii_art[0] if ceiling_dec else ""
        ceiling_line = ceiling_art.center(width - 2)
        lines.append(border + ceiling_line + border)

        # Walls
        wall_left = self.get_decoration_at(DecorationSlot.WALL_LEFT.value)
        wall_right = self.get_decoration_at(DecorationSlot.WALL_RIGHT.value)
        left_art = wall_left.ascii_art[0] if wall_left else "    "
        right_art = wall_right.ascii_art[0] if wall_right else "    "

        wall_line = left_art + " " * (width - 2 - len(left_art) - len(right_art)) + right_art
        lines.append(border + wall_line + border)

        # Middle area (where duck goes)
        lines.append(border + " " * (width - 2) + border)
        lines.append(border + " " * (width - 2) + border)

        # Nest area
        nest = self.get_decoration_at(DecorationSlot.NEST.value)
        nest_art = nest.ascii_art[0] if nest else "\\___/"
        nest_line = nest_art.center(width - 2)
        lines.append(border + nest_line + border)

        # Floor
        floor_left = self.get_decoration_at(DecorationSlot.FLOOR_LEFT.value)
        floor_right = self.get_decoration_at(DecorationSlot.FLOOR_RIGHT.value)
        left_art = floor_left.ascii_art[0] if floor_left else floor * 5
        right_art = floor_right.ascii_art[0] if floor_right else floor * 5

        floor_fill = floor * (width - 2 - len(left_art) - len(right_art))
        lines.append(border + left_art + floor_fill + right_art + border)

        # Water area
        water = self.get_decoration_at(DecorationSlot.WATER.value)
        if water:
            water_art = water.ascii_art[0] if water.ascii_art else "~~~~~"
            water_line = water_art.center(width - 2)
            lines.append(border + water_line + border)

        # Bottom border
        lines.append(border * width)

        return lines

    def check_unlocks(self, level: int, stats: dict, streak: int, collectibles: dict) -> List[str]:
        """
        Check what can be unlocked based on progress.
        Returns list of newly unlockable decoration/theme IDs.
        """
        newly_unlockable = []

        # Check decorations
        for dec_id, dec in DECORATIONS.items():
            if dec_id in self.unlocked_decorations:
                continue
            if not dec.unlock_condition:
                continue

            condition = dec.unlock_condition.lower()

            # Level-based
            if "level" in condition:
                import re
                match = re.search(r"level\s*(\d+)", condition)
                if match and level >= int(match.group(1)):
                    newly_unlockable.append(dec_id)

            # Streak-based
            elif "streak" in condition:
                import re
                match = re.search(r"(\d+)\s*day", condition)
                if match and streak >= int(match.group(1)):
                    newly_unlockable.append(dec_id)

            # Stat-based
            elif "feed" in condition:
                import re
                match = re.search(r"(\d+)", condition)
                if match and stats.get("total_feeds", 0) >= int(match.group(1)):
                    newly_unlockable.append(dec_id)
            elif "play" in condition:
                import re
                match = re.search(r"(\d+)", condition)
                if match and stats.get("total_plays", 0) >= int(match.group(1)):
                    newly_unlockable.append(dec_id)

        # Check themes
        for theme_id, theme in HOME_THEMES.items():
            if theme_id in self.unlocked_themes:
                continue
            condition = theme.get("unlock_condition", "").lower()
            if not condition:
                continue

            if "level" in condition:
                import re
                match = re.search(r"level\s*(\d+)", condition)
                if match and level >= int(match.group(1)):
                    newly_unlockable.append(f"theme:{theme_id}")

            elif "streak" in condition:
                import re
                match = re.search(r"(\d+)\s*day", condition)
                if match and streak >= int(match.group(1)):
                    newly_unlockable.append(f"theme:{theme_id}")

        return newly_unlockable

    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "theme": self.theme,
            "decorations": self.decorations,
            "unlocked_decorations": self.unlocked_decorations,
            "unlocked_themes": self.unlocked_themes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DuckHome":
        """Create from dictionary."""
        home = cls()
        home.theme = data.get("theme", "default")
        home.decorations = data.get("decorations", {})
        home.unlocked_decorations = data.get("unlocked_decorations", ["basic_nest", "pebble_collection", "duck_poster"])
        home.unlocked_themes = data.get("unlocked_themes", ["default"])
        home._calculate_mood_bonus()
        return home


# Global instance
duck_home = DuckHome()
