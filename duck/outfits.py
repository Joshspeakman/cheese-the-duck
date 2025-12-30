"""
Outfit System - Full outfit management beyond just hats.
Includes tops, accessories, costumes, and seasonal clothing.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class OutfitSlot(Enum):
    """Slots where items can be equipped."""
    HAT = "hat"
    FACE = "face"  # Glasses, masks
    NECK = "neck"  # Scarves, necklaces, bowties
    BODY = "body"  # Shirts, capes, costumes
    WINGS = "wings"  # Wing decorations
    FEET = "feet"  # Shoes, booties
    HELD = "held"  # Items held in wing
    SPECIAL = "special"  # Auras, effects


class Season(Enum):
    """Seasons for seasonal clothing."""
    SPRING = "spring"
    SUMMER = "summer"
    FALL = "fall"
    WINTER = "winter"
    ANY = "any"
    HOLIDAY = "holiday"


@dataclass
class OutfitItem:
    """An equippable outfit item."""
    id: str
    name: str
    description: str
    slot: OutfitSlot
    rarity: str  # common, uncommon, rare, epic, legendary
    cost: int
    unlock_level: int
    seasons: List[Season]
    ascii_art: Dict[str, str]  # Position hints for rendering
    color_code: str  # Color for rendering
    animation: Optional[str] = None  # Optional animation type
    mood_bonus: int = 0
    special_effect: Optional[str] = None


# Complete outfit database
OUTFIT_ITEMS: Dict[str, OutfitItem] = {
    # ===== HATS (already exist, but adding more) =====
    "santa_hat": OutfitItem(
        id="santa_hat",
        name="Santa Hat",
        description="Ho ho ho! A festive red hat with white trim!",
        slot=OutfitSlot.HAT,
        rarity="rare",
        cost=200,
        unlock_level=5,
        seasons=[Season.WINTER, Season.HOLIDAY],
        ascii_art={"symbol": "S", "offset": (-1, 0)},
        color_code="red",
        mood_bonus=10,
    ),
    "witch_hat": OutfitItem(
        id="witch_hat",
        name="Witch Hat",
        description="Spooky and magical! Perfect for Halloween!",
        slot=OutfitSlot.HAT,
        rarity="uncommon",
        cost=150,
        unlock_level=4,
        seasons=[Season.FALL, Season.HOLIDAY],
        ascii_art={"symbol": "W", "offset": (-1, 0)},
        color_code="purple",
        mood_bonus=5,
    ),
    "bunny_ears": OutfitItem(
        id="bunny_ears",
        name="Bunny Ears",
        description="Hippity hoppity! Spring-themed bunny ears!",
        slot=OutfitSlot.HAT,
        rarity="uncommon",
        cost=120,
        unlock_level=3,
        seasons=[Season.SPRING, Season.HOLIDAY],
        ascii_art={"symbol": "b", "offset": (-1, 0)},
        color_code="pink",
        mood_bonus=5,
    ),
    "sun_hat": OutfitItem(
        id="sun_hat",
        name="Sun Hat",
        description="A wide-brimmed hat for sunny days!",
        slot=OutfitSlot.HAT,
        rarity="common",
        cost=80,
        unlock_level=2,
        seasons=[Season.SUMMER],
        ascii_art={"symbol": "^", "offset": (-1, 0)},
        color_code="yellow",
        mood_bonus=3,
    ),
    
    # ===== FACE ACCESSORIES =====
    "sunglasses_cool": OutfitItem(
        id="sunglasses_cool",
        name="Cool Sunglasses",
        description="Deal with it. B)",
        slot=OutfitSlot.FACE,
        rarity="common",
        cost=100,
        unlock_level=2,
        seasons=[Season.ANY],
        ascii_art={"symbol": "o", "offset": (0, 0)},
        color_code="black",
        mood_bonus=5,
    ),
    "monocle": OutfitItem(
        id="monocle",
        name="Distinguished Monocle",
        description="Hmm, yes, quite distinguished indeed!",
        slot=OutfitSlot.FACE,
        rarity="uncommon",
        cost=200,
        unlock_level=4,
        seasons=[Season.ANY],
        ascii_art={"symbol": "o", "offset": (0, 0)},
        color_code="gold",
        mood_bonus=5,
    ),
    "heart_glasses": OutfitItem(
        id="heart_glasses",
        name="Heart Glasses",
        description="Everything looks lovely through these!",
        slot=OutfitSlot.FACE,
        rarity="uncommon",
        cost=150,
        unlock_level=3,
        seasons=[Season.ANY, Season.HOLIDAY],
        ascii_art={"symbol": "<3", "offset": (0, 0)},
        color_code="pink",
        mood_bonus=8,
    ),
    "masquerade_mask": OutfitItem(
        id="masquerade_mask",
        name="Masquerade Mask",
        description="Mysterious and elegant!",
        slot=OutfitSlot.FACE,
        rarity="rare",
        cost=300,
        unlock_level=6,
        seasons=[Season.ANY],
        ascii_art={"symbol": "*", "offset": (0, 0)},
        color_code="purple",
        mood_bonus=10,
    ),
    
    # ===== NECK ACCESSORIES =====
    "bowtie_red": OutfitItem(
        id="bowtie_red",
        name="Red Bowtie",
        description="Dapper and distinguished!",
        slot=OutfitSlot.NECK,
        rarity="common",
        cost=80,
        unlock_level=2,
        seasons=[Season.ANY],
        ascii_art={"symbol": "*", "offset": (1, 0)},
        color_code="red",
        mood_bonus=3,
    ),
    "scarf_striped": OutfitItem(
        id="scarf_striped",
        name="Striped Scarf",
        description="Warm and cozy for cold days!",
        slot=OutfitSlot.NECK,
        rarity="common",
        cost=90,
        unlock_level=2,
        seasons=[Season.WINTER, Season.FALL],
        ascii_art={"symbol": "S", "offset": (1, 0)},
        color_code="blue",
        mood_bonus=5,
    ),
    "pearl_necklace": OutfitItem(
        id="pearl_necklace",
        name="Pearl Necklace",
        description="Elegant pearls for a fancy duck!",
        slot=OutfitSlot.NECK,
        rarity="rare",
        cost=400,
        unlock_level=7,
        seasons=[Season.ANY],
        ascii_art={"symbol": "o", "offset": (1, 0)},
        color_code="white",
        mood_bonus=10,
    ),
    "flower_lei": OutfitItem(
        id="flower_lei",
        name="Flower Lei",
        description="Aloha! A tropical flower necklace!",
        slot=OutfitSlot.NECK,
        rarity="uncommon",
        cost=120,
        unlock_level=3,
        seasons=[Season.SUMMER],
        ascii_art={"symbol": "*", "offset": (1, 0)},
        color_code="pink",
        mood_bonus=8,
    ),
    "bell_collar": OutfitItem(
        id="bell_collar",
        name="Bell Collar",
        description="Jingle jingle! A festive collar with a bell!",
        slot=OutfitSlot.NECK,
        rarity="uncommon",
        cost=150,
        unlock_level=4,
        seasons=[Season.WINTER, Season.HOLIDAY],
        ascii_art={"symbol": "o", "offset": (1, 0)},
        color_code="gold",
        mood_bonus=7,
        special_effect="jingle",
    ),
    
    # ===== BODY/COSTUMES =====
    "superhero_cape": OutfitItem(
        id="superhero_cape",
        name="Superhero Cape",
        description="Up, up, and away! A flowing red cape!",
        slot=OutfitSlot.BODY,
        rarity="rare",
        cost=500,
        unlock_level=6,
        seasons=[Season.ANY],
        ascii_art={"symbol": "S", "offset": (0, 1)},
        color_code="red",
        mood_bonus=15,
        animation="flutter",
    ),
    "sweater_cozy": OutfitItem(
        id="sweater_cozy",
        name="Cozy Sweater",
        description="An adorable knitted sweater!",
        slot=OutfitSlot.BODY,
        rarity="common",
        cost=100,
        unlock_level=2,
        seasons=[Season.WINTER, Season.FALL],
        ascii_art={"symbol": "C", "offset": (0, 0)},
        color_code="blue",
        mood_bonus=5,
    ),
    "hawaiian_shirt": OutfitItem(
        id="hawaiian_shirt",
        name="Hawaiian Shirt",
        description="Tropical vibes! Vacation mode activated!",
        slot=OutfitSlot.BODY,
        rarity="uncommon",
        cost=150,
        unlock_level=3,
        seasons=[Season.SUMMER],
        ascii_art={"symbol": "T", "offset": (0, 0)},
        color_code="cyan",
        mood_bonus=8,
    ),
    "tuxedo": OutfitItem(
        id="tuxedo",
        name="Tuxedo",
        description="Black tie affair! Very distinguished!",
        slot=OutfitSlot.BODY,
        rarity="epic",
        cost=800,
        unlock_level=8,
        seasons=[Season.ANY],
        ascii_art={"symbol": "T", "offset": (0, 0)},
        color_code="black",
        mood_bonus=15,
    ),
    "wizard_robe": OutfitItem(
        id="wizard_robe",
        name="Wizard Robe",
        description="Mystical robes for a magical duck!",
        slot=OutfitSlot.BODY,
        rarity="rare",
        cost=400,
        unlock_level=6,
        seasons=[Season.ANY],
        ascii_art={"symbol": "W", "offset": (0, 0)},
        color_code="purple",
        mood_bonus=12,
        special_effect="sparkle",
    ),
    "santa_suit": OutfitItem(
        id="santa_suit",
        name="Santa Suit",
        description="Full Santa costume! Ho ho ho!",
        slot=OutfitSlot.BODY,
        rarity="epic",
        cost=600,
        unlock_level=7,
        seasons=[Season.WINTER, Season.HOLIDAY],
        ascii_art={"symbol": "S", "offset": (0, 0)},
        color_code="red",
        mood_bonus=20,
    ),
    "raincoat": OutfitItem(
        id="raincoat",
        name="Yellow Raincoat",
        description="Splash splash! Stay dry in the rain!",
        slot=OutfitSlot.BODY,
        rarity="common",
        cost=80,
        unlock_level=2,
        seasons=[Season.SPRING, Season.FALL],
        ascii_art={"symbol": "C", "offset": (0, 0)},
        color_code="yellow",
        mood_bonus=5,
    ),
    
    # ===== WING DECORATIONS =====
    "fairy_wings": OutfitItem(
        id="fairy_wings",
        name="Fairy Wings",
        description="Sparkly magical wings!",
        slot=OutfitSlot.WINGS,
        rarity="epic",
        cost=700,
        unlock_level=8,
        seasons=[Season.ANY],
        ascii_art={"symbol": "f", "offset": (0, 0)},
        color_code="pink",
        mood_bonus=15,
        animation="shimmer",
        special_effect="sparkle",
    ),
    "angel_wings": OutfitItem(
        id="angel_wings",
        name="Angel Wings",
        description="Pure white angelic wings!",
        slot=OutfitSlot.WINGS,
        rarity="legendary",
        cost=1500,
        unlock_level=12,
        seasons=[Season.ANY],
        ascii_art={"symbol": ":)", "offset": (0, 0)},
        color_code="white",
        mood_bonus=25,
        animation="glow",
        special_effect="halo",
    ),
    "bat_wings": OutfitItem(
        id="bat_wings",
        name="Bat Wings",
        description="Spooky bat wings for Halloween!",
        slot=OutfitSlot.WINGS,
        rarity="rare",
        cost=350,
        unlock_level=5,
        seasons=[Season.FALL, Season.HOLIDAY],
        ascii_art={"symbol": "V", "offset": (0, 0)},
        color_code="black",
        mood_bonus=10,
    ),
    
    # ===== FEET =====
    "rain_boots": OutfitItem(
        id="rain_boots",
        name="Rain Boots",
        description="Yellow rubber boots for puddle jumping!",
        slot=OutfitSlot.FEET,
        rarity="common",
        cost=60,
        unlock_level=1,
        seasons=[Season.SPRING, Season.ANY],
        ascii_art={"symbol": "b", "offset": (2, 0)},
        color_code="yellow",
        mood_bonus=5,
    ),
    "bunny_slippers": OutfitItem(
        id="bunny_slippers",
        name="Bunny Slippers",
        description="Comfy bunny slippers!",
        slot=OutfitSlot.FEET,
        rarity="uncommon",
        cost=120,
        unlock_level=3,
        seasons=[Season.ANY],
        ascii_art={"symbol": "b", "offset": (2, 0)},
        color_code="pink",
        mood_bonus=8,
    ),
    "ice_skates": OutfitItem(
        id="ice_skates",
        name="Ice Skates",
        description="Glide on ice! Winter fun!",
        slot=OutfitSlot.FEET,
        rarity="uncommon",
        cost=150,
        unlock_level=4,
        seasons=[Season.WINTER],
        ascii_art={"symbol": "x", "offset": (2, 0)},
        color_code="silver",
        mood_bonus=10,
    ),
    
    # ===== HELD ITEMS =====
    "umbrella": OutfitItem(
        id="umbrella",
        name="Umbrella",
        description="A colorful umbrella!",
        slot=OutfitSlot.HELD,
        rarity="common",
        cost=70,
        unlock_level=2,
        seasons=[Season.SPRING, Season.FALL],
        ascii_art={"symbol": "Y", "offset": (0, 1)},
        color_code="red",
        mood_bonus=3,
    ),
    "magic_wand": OutfitItem(
        id="magic_wand",
        name="Magic Wand",
        description="Sparkly magic wand!",
        slot=OutfitSlot.HELD,
        rarity="rare",
        cost=300,
        unlock_level=5,
        seasons=[Season.ANY],
        ascii_art={"symbol": "*", "offset": (0, 1)},
        color_code="gold",
        mood_bonus=12,
        animation="sparkle",
    ),
    "fishing_rod": OutfitItem(
        id="fishing_rod",
        name="Fishing Rod",
        description="Gone fishin'!",
        slot=OutfitSlot.HELD,
        rarity="common",
        cost=80,
        unlock_level=3,
        seasons=[Season.ANY],
        ascii_art={"symbol": "-o", "offset": (0, 1)},
        color_code="brown",
        mood_bonus=5,
    ),
    "bouquet": OutfitItem(
        id="bouquet",
        name="Flower Bouquet",
        description="A beautiful bouquet of flowers!",
        slot=OutfitSlot.HELD,
        rarity="uncommon",
        cost=100,
        unlock_level=2,
        seasons=[Season.SPRING, Season.SUMMER],
        ascii_art={"symbol": "*", "offset": (0, 1)},
        color_code="pink",
        mood_bonus=10,
    ),
    
    # ===== SPECIAL EFFECTS =====
    "sparkle_aura": OutfitItem(
        id="sparkle_aura",
        name="Sparkle Aura",
        description="Magical sparkles surround you!",
        slot=OutfitSlot.SPECIAL,
        rarity="epic",
        cost=1000,
        unlock_level=10,
        seasons=[Season.ANY],
        ascii_art={"symbol": "*", "offset": (0, 0)},
        color_code="gold",
        mood_bonus=20,
        animation="sparkle",
        special_effect="particle_sparkle",
    ),
    "rainbow_trail": OutfitItem(
        id="rainbow_trail",
        name="Rainbow Trail",
        description="Leave rainbows wherever you go!",
        slot=OutfitSlot.SPECIAL,
        rarity="legendary",
        cost=2000,
        unlock_level=15,
        seasons=[Season.ANY],
        ascii_art={"symbol": "~", "offset": (0, 0)},
        color_code="rainbow",
        mood_bonus=30,
        animation="trail",
        special_effect="rainbow_trail",
    ),
    "heart_bubbles": OutfitItem(
        id="heart_bubbles",
        name="Heart Bubbles",
        description="Float in a cloud of heart bubbles!",
        slot=OutfitSlot.SPECIAL,
        rarity="rare",
        cost=500,
        unlock_level=7,
        seasons=[Season.ANY],
        ascii_art={"symbol": "<3", "offset": (0, 0)},
        color_code="pink",
        mood_bonus=15,
        animation="float",
        special_effect="heart_particles",
    ),
}


@dataclass
class EquippedOutfit:
    """Currently equipped outfit."""
    hat: Optional[str] = None
    face: Optional[str] = None
    neck: Optional[str] = None
    body: Optional[str] = None
    wings: Optional[str] = None
    feet: Optional[str] = None
    held: Optional[str] = None
    special: Optional[str] = None


@dataclass
class SavedOutfit:
    """A saved outfit combination."""
    name: str
    outfit: EquippedOutfit
    created_at: str


class OutfitManager:
    """
    Manages the full outfit system.
    """
    
    def __init__(self):
        self.owned_items: List[str] = []
        self.current_outfit: EquippedOutfit = EquippedOutfit()
        self.saved_outfits: Dict[str, SavedOutfit] = {}
        self.favorite_items: List[str] = []
    
    def purchase_item(self, item_id: str, currency: int, level: int) -> Tuple[bool, str, int]:
        """Purchase an outfit item."""
        if item_id not in OUTFIT_ITEMS:
            return False, "Item not found!", 0
        
        item = OUTFIT_ITEMS[item_id]
        
        if item_id in self.owned_items:
            return False, "You already own this!", 0
        
        if level < item.unlock_level:
            return False, f"Reach level {item.unlock_level} to unlock!", 0
        
        if currency < item.cost:
            return False, f"Need {item.cost - currency} more coins!", 0
        
        self.owned_items.append(item_id)
        return True, f"Purchased {item.name}! *", item.cost
    
    def equip_item(self, item_id: str) -> Tuple[bool, str]:
        """Equip an item."""
        if item_id not in self.owned_items:
            return False, "You don't own this item!"
        
        item = OUTFIT_ITEMS.get(item_id)
        if not item:
            return False, "Item not found!"
        
        # Equip to appropriate slot
        slot_map = {
            OutfitSlot.HAT: "hat",
            OutfitSlot.FACE: "face",
            OutfitSlot.NECK: "neck",
            OutfitSlot.BODY: "body",
            OutfitSlot.WINGS: "wings",
            OutfitSlot.FEET: "feet",
            OutfitSlot.HELD: "held",
            OutfitSlot.SPECIAL: "special",
        }
        
        slot_attr = slot_map.get(item.slot)
        if slot_attr:
            setattr(self.current_outfit, slot_attr, item_id)
            return True, f"Equipped {item.name}!"
        
        return False, "Invalid slot!"
    
    def unequip_slot(self, slot: OutfitSlot) -> Tuple[bool, str]:
        """Unequip an item from a slot."""
        slot_map = {
            OutfitSlot.HAT: "hat",
            OutfitSlot.FACE: "face",
            OutfitSlot.NECK: "neck",
            OutfitSlot.BODY: "body",
            OutfitSlot.WINGS: "wings",
            OutfitSlot.FEET: "feet",
            OutfitSlot.HELD: "held",
            OutfitSlot.SPECIAL: "special",
        }
        
        slot_attr = slot_map.get(slot)
        if slot_attr:
            current = getattr(self.current_outfit, slot_attr)
            if current:
                setattr(self.current_outfit, slot_attr, None)
                item = OUTFIT_ITEMS.get(current)
                return True, f"Unequipped {item.name if item else 'item'}!"
            return False, "Nothing equipped in that slot!"
        
        return False, "Invalid slot!"
    
    def save_outfit(self, name: str) -> Tuple[bool, str]:
        """Save current outfit combination."""
        from datetime import datetime
        
        saved = SavedOutfit(
            name=name,
            outfit=EquippedOutfit(
                hat=self.current_outfit.hat,
                face=self.current_outfit.face,
                neck=self.current_outfit.neck,
                body=self.current_outfit.body,
                wings=self.current_outfit.wings,
                feet=self.current_outfit.feet,
                held=self.current_outfit.held,
                special=self.current_outfit.special,
            ),
            created_at=datetime.now().isoformat(),
        )
        self.saved_outfits[name] = saved
        return True, f"Saved outfit '{name}'!"
    
    def load_outfit(self, name: str) -> Tuple[bool, str]:
        """Load a saved outfit."""
        if name not in self.saved_outfits:
            return False, "Outfit not found!"
        
        saved = self.saved_outfits[name]
        self.current_outfit = EquippedOutfit(
            hat=saved.outfit.hat,
            face=saved.outfit.face,
            neck=saved.outfit.neck,
            body=saved.outfit.body,
            wings=saved.outfit.wings,
            feet=saved.outfit.feet,
            held=saved.outfit.held,
            special=saved.outfit.special,
        )
        return True, f"Loaded outfit '{name}'!"
    
    def get_total_mood_bonus(self) -> int:
        """Calculate total mood bonus from equipped items."""
        total = 0
        for slot in [self.current_outfit.hat, self.current_outfit.face,
                     self.current_outfit.neck, self.current_outfit.body,
                     self.current_outfit.wings, self.current_outfit.feet,
                     self.current_outfit.held, self.current_outfit.special]:
            if slot:
                item = OUTFIT_ITEMS.get(slot)
                if item:
                    total += item.mood_bonus
        return total
    
    def get_equipped_items(self) -> List[OutfitItem]:
        """Get list of all equipped items."""
        items = []
        for slot in [self.current_outfit.hat, self.current_outfit.face,
                     self.current_outfit.neck, self.current_outfit.body,
                     self.current_outfit.wings, self.current_outfit.feet,
                     self.current_outfit.held, self.current_outfit.special]:
            if slot:
                item = OUTFIT_ITEMS.get(slot)
                if item:
                    items.append(item)
        return items
    
    def get_seasonal_items(self, season: Season) -> List[OutfitItem]:
        """Get items appropriate for current season."""
        return [
            item for item in OUTFIT_ITEMS.values()
            if season in item.seasons or Season.ANY in item.seasons
        ]
    
    def render_wardrobe(self) -> List[str]:
        """Render the wardrobe display."""
        lines = [
            "+===========================================+",
            "|           * YOUR WARDROBE *             |",
            "+===========================================+",
            "| Currently Wearing:                        |",
        ]
        
        slot_names = ["Hat", "Face", "Neck", "Body", "Wings", "Feet", "Held", "Special"]
        slot_attrs = ["hat", "face", "neck", "body", "wings", "feet", "held", "special"]
        
        for name, attr in zip(slot_names, slot_attrs):
            item_id = getattr(self.current_outfit, attr)
            if item_id:
                item = OUTFIT_ITEMS.get(item_id)
                if item:
                    lines.append(f"|  {name:8}: {item.name[:20]:20}    |")
                else:
                    lines.append(f"|  {name:8}: (Unknown)                  |")
            else:
                lines.append(f"|  {name:8}: [Empty]                    |")
        
        lines.append("+===========================================+")
        lines.append(f"| Mood Bonus: +{self.get_total_mood_bonus():2}                          |")
        lines.append(f"| Owned Items: {len(self.owned_items):3}                           |")
        lines.append("+===========================================+")
        
        return lines
    
    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "owned_items": self.owned_items,
            "current_outfit": {
                "hat": self.current_outfit.hat,
                "face": self.current_outfit.face,
                "neck": self.current_outfit.neck,
                "body": self.current_outfit.body,
                "wings": self.current_outfit.wings,
                "feet": self.current_outfit.feet,
                "held": self.current_outfit.held,
                "special": self.current_outfit.special,
            },
            "saved_outfits": {
                name: {
                    "name": s.name,
                    "outfit": {
                        "hat": s.outfit.hat,
                        "face": s.outfit.face,
                        "neck": s.outfit.neck,
                        "body": s.outfit.body,
                        "wings": s.outfit.wings,
                        "feet": s.outfit.feet,
                        "held": s.outfit.held,
                        "special": s.outfit.special,
                    },
                    "created_at": s.created_at,
                }
                for name, s in self.saved_outfits.items()
            },
            "favorite_items": self.favorite_items,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "OutfitManager":
        """Create from dictionary."""
        manager = cls()
        manager.owned_items = data.get("owned_items", [])
        
        outfit_data = data.get("current_outfit", {})
        manager.current_outfit = EquippedOutfit(
            hat=outfit_data.get("hat"),
            face=outfit_data.get("face"),
            neck=outfit_data.get("neck"),
            body=outfit_data.get("body"),
            wings=outfit_data.get("wings"),
            feet=outfit_data.get("feet"),
            held=outfit_data.get("held"),
            special=outfit_data.get("special"),
        )
        
        for name, sdata in data.get("saved_outfits", {}).items():
            outfit = EquippedOutfit(
                hat=sdata["outfit"].get("hat"),
                face=sdata["outfit"].get("face"),
                neck=sdata["outfit"].get("neck"),
                body=sdata["outfit"].get("body"),
                wings=sdata["outfit"].get("wings"),
                feet=sdata["outfit"].get("feet"),
                held=sdata["outfit"].get("held"),
                special=sdata["outfit"].get("special"),
            )
            manager.saved_outfits[name] = SavedOutfit(
                name=sdata["name"],
                outfit=outfit,
                created_at=sdata.get("created_at", ""),
            )
        
        manager.favorite_items = data.get("favorite_items", [])
        
        return manager


# Global outfit manager instance
outfit_manager = OutfitManager()
