"""
Treasure Hunting System - Hidden treasures and exploration rewards.
Features maps, digging, and rare collectible treasures.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random


class TreasureRarity(Enum):
    """Rarity of treasures."""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    MYTHICAL = "mythical"


class TreasureLocation(Enum):
    """Types of treasure locations."""
    BEACH = "beach"
    FOREST = "forest"
    GARDEN = "garden"
    POND = "pond"
    CAVE = "cave"
    MOUNTAIN = "mountain"
    SECRET = "secret"


@dataclass
class Treasure:
    """A treasure that can be found."""
    id: str
    name: str
    description: str
    rarity: TreasureRarity
    locations: List[TreasureLocation]
    xp_value: int
    coin_value: int
    ascii_art: str
    lore: str  # Story/background
    is_collectible: bool = True


@dataclass
class TreasureMap:
    """A map that reveals treasure location."""
    map_id: str
    treasure_id: str
    location: TreasureLocation
    hint: str
    found: bool = False
    created_at: str = ""


@dataclass
class FoundTreasure:
    """A treasure that was found."""
    treasure_id: str
    found_at: str
    location: TreasureLocation
    was_mapped: bool = False


# Treasure Database
TREASURES: Dict[str, Treasure] = {
    # Common treasures
    "old_coin": Treasure(
        id="old_coin",
        name="Old Coin",
        description="A worn, old coin. Someone lost this long ago.",
        rarity=TreasureRarity.COMMON,
        locations=[TreasureLocation.BEACH, TreasureLocation.GARDEN],
        xp_value=10,
        coin_value=5,
        ascii_art="[◎]",
        lore="This coin bears the image of a duck king from centuries past.",
    ),
    "pretty_shell": Treasure(
        id="pretty_shell",
        name="Pretty Shell",
        description="A beautiful seashell with a pearly interior.",
        rarity=TreasureRarity.COMMON,
        locations=[TreasureLocation.BEACH, TreasureLocation.POND],
        xp_value=8,
        coin_value=3,
        ascii_art="🐚",
        lore="Hold it to your ear - you can hear the ocean!",
    ),
    "smooth_stone": Treasure(
        id="smooth_stone",
        name="Smooth Stone",
        description="A perfectly smooth, palm-sized stone.",
        rarity=TreasureRarity.COMMON,
        locations=[TreasureLocation.FOREST, TreasureLocation.POND],
        xp_value=5,
        coin_value=2,
        ascii_art="◐",
        lore="Polished by centuries of flowing water.",
    ),
    
    # Uncommon treasures
    "ancient_feather": Treasure(
        id="ancient_feather",
        name="Ancient Feather",
        description="A preserved feather from an ancient duck.",
        rarity=TreasureRarity.UNCOMMON,
        locations=[TreasureLocation.CAVE, TreasureLocation.FOREST],
        xp_value=25,
        coin_value=20,
        ascii_art="🪶",
        lore="Legend says this belonged to the First Duck.",
    ),
    "glass_bottle": Treasure(
        id="glass_bottle",
        name="Message in a Bottle",
        description="An old bottle with a mysterious message inside!",
        rarity=TreasureRarity.UNCOMMON,
        locations=[TreasureLocation.BEACH, TreasureLocation.POND],
        xp_value=30,
        coin_value=25,
        ascii_art="🍾",
        lore="The message reads: 'Bread is the answer to everything.'",
    ),
    "fossil": Treasure(
        id="fossil",
        name="Duck Fossil",
        description="A fossilized duck footprint from prehistoric times!",
        rarity=TreasureRarity.UNCOMMON,
        locations=[TreasureLocation.MOUNTAIN, TreasureLocation.CAVE],
        xp_value=35,
        coin_value=30,
        ascii_art="🦶",
        lore="Evidence that ducks have been awesome for millions of years.",
    ),
    
    # Rare treasures
    "ruby_gem": Treasure(
        id="ruby_gem",
        name="Ruby Gem",
        description="A beautiful red gemstone that catches the light!",
        rarity=TreasureRarity.RARE,
        locations=[TreasureLocation.CAVE, TreasureLocation.MOUNTAIN],
        xp_value=75,
        coin_value=100,
        ascii_art="💎",
        lore="Some say this gem was formed from crystallized duck joy.",
    ),
    "golden_acorn": Treasure(
        id="golden_acorn",
        name="Golden Acorn",
        description="A perfectly preserved golden acorn!",
        rarity=TreasureRarity.RARE,
        locations=[TreasureLocation.FOREST],
        xp_value=60,
        coin_value=75,
        ascii_art="🌰",
        lore="Grown from the legendary Golden Oak Tree.",
    ),
    "pirate_compass": Treasure(
        id="pirate_compass",
        name="Pirate Compass",
        description="An old compass that always points to treasure!",
        rarity=TreasureRarity.RARE,
        locations=[TreasureLocation.BEACH, TreasureLocation.CAVE],
        xp_value=80,
        coin_value=90,
        ascii_art="🧭",
        lore="Once belonged to Captain Quackbeard himself.",
    ),
    
    # Epic treasures
    "ancient_crown": Treasure(
        id="ancient_crown",
        name="Ancient Duck Crown",
        description="A crown worn by duck royalty of old!",
        rarity=TreasureRarity.EPIC,
        locations=[TreasureLocation.CAVE, TreasureLocation.SECRET],
        xp_value=200,
        coin_value=300,
        ascii_art="👑",
        lore="This crown has been passed down through 100 duck generations.",
    ),
    "mystic_egg": Treasure(
        id="mystic_egg",
        name="Mystic Egg",
        description="A mysterious glowing egg with ancient symbols.",
        rarity=TreasureRarity.EPIC,
        locations=[TreasureLocation.SECRET, TreasureLocation.MOUNTAIN],
        xp_value=250,
        coin_value=350,
        ascii_art="🥚✨",
        lore="What could hatch from this egg? Nobody knows...",
    ),
    
    # Legendary treasures
    "star_fragment": Treasure(
        id="star_fragment",
        name="Star Fragment",
        description="A piece of a fallen star! Incredibly rare!",
        rarity=TreasureRarity.LEGENDARY,
        locations=[TreasureLocation.SECRET, TreasureLocation.MOUNTAIN],
        xp_value=500,
        coin_value=750,
        ascii_art="⭐",
        lore="Whispered wishes to this fragment are said to come true.",
    ),
    "ancient_tome": Treasure(
        id="ancient_tome",
        name="Ancient Tome of Quacks",
        description="An ancient book of duck wisdom!",
        rarity=TreasureRarity.LEGENDARY,
        locations=[TreasureLocation.CAVE, TreasureLocation.SECRET],
        xp_value=600,
        coin_value=800,
        ascii_art="📖",
        lore="Contains the sacred knowledge of the Duck Elders.",
    ),
    
    # Mythical treasures
    "heart_of_pond": Treasure(
        id="heart_of_pond",
        name="Heart of the Pond",
        description="THE legendary treasure. The soul of all ponds!",
        rarity=TreasureRarity.MYTHICAL,
        locations=[TreasureLocation.SECRET],
        xp_value=2000,
        coin_value=2500,
        ascii_art="💙✨",
        lore="Only the most dedicated treasure hunter will ever find this.",
    ),
}

# Treasure hunt hints for each location
LOCATION_HINTS = {
    TreasureLocation.BEACH: [
        "Where the waves kiss the sand...",
        "Near the driftwood at low tide...",
        "Beneath the seagull's watchful gaze...",
    ],
    TreasureLocation.FOREST: [
        "Under the ancient oak...",
        "Where sunlight filters through leaves...",
        "Near the mushroom circle...",
    ],
    TreasureLocation.GARDEN: [
        "Beside the old sundial...",
        "Where the roses bloom...",
        "Under the bird bath...",
    ],
    TreasureLocation.POND: [
        "At the water's edge...",
        "Near the lily pads...",
        "Where the ducks gather...",
    ],
    TreasureLocation.CAVE: [
        "In the deepest shadows...",
        "Behind the crystal formations...",
        "Where echoes fade to silence...",
    ],
    TreasureLocation.MOUNTAIN: [
        "At the summit's peak...",
        "Near the ancient stones...",
        "Where eagles dare not go...",
    ],
    TreasureLocation.SECRET: [
        "Where dreams meet reality...",
        "In the place between places...",
        "Follow the golden light...",
    ],
}


class TreasureHunter:
    """
    Treasure hunting system.
    """
    
    def __init__(self):
        self.found_treasures: Dict[str, List[FoundTreasure]] = {}
        self.treasure_maps: List[TreasureMap] = []
        self.total_treasures_found: int = 0
        self.total_value_found: int = 0
        self.unlocked_locations: List[TreasureLocation] = [
            TreasureLocation.BEACH,
            TreasureLocation.GARDEN,
        ]
        self.dig_attempts_today: int = 0
        self.max_digs_per_day: int = 10
        self.last_dig_date: str = ""
        self.current_hunt_location: Optional[TreasureLocation] = None
        self.hunt_progress: int = 0  # 0-100
        self.active_map: Optional[TreasureMap] = None
    
    def start_hunt(self, location: TreasureLocation) -> Tuple[bool, str]:
        """Start hunting at a location."""
        if location not in self.unlocked_locations:
            return False, f"You haven't unlocked {location.value} yet!"
        
        # Check daily dig limit
        today = datetime.now().strftime("%Y-%m-%d")
        if self.last_dig_date != today:
            self.dig_attempts_today = 0
            self.last_dig_date = today
        
        if self.dig_attempts_today >= self.max_digs_per_day:
            return False, "You're tired from digging! Try again tomorrow."
        
        self.current_hunt_location = location
        self.hunt_progress = 0
        return True, f"Started searching at {location.value}... 🔍"
    
    def dig(self) -> Tuple[bool, str, Optional[FoundTreasure]]:
        """Attempt to dig for treasure."""
        if not self.current_hunt_location:
            return False, "Start a treasure hunt first!", None
        
        self.dig_attempts_today += 1
        self.hunt_progress += random.randint(15, 35)
        
        # Check if using a map
        if self.active_map:
            if self.hunt_progress >= 50:
                # Guaranteed find with map
                return self._find_treasure(self.active_map.treasure_id, was_mapped=True)
        
        # Random find chance
        find_chance = 0.1 + (self.hunt_progress / 500)  # Base 10%, increases with progress
        
        if random.random() < find_chance:
            treasure = self._select_treasure()
            if treasure:
                return self._find_treasure(treasure.id)
        
        # Progression messages
        if self.hunt_progress >= 100:
            self.hunt_progress = 0
            return False, "Nothing here... Try a different spot? 🤔", None
        
        messages = [
            "Digging... Nothing yet. 🕳️",
            "Keep searching... 🔍",
            "You found a rock! ...Just a rock. 🪨",
            "Something rustles nearby... 🌿",
            "The duck instincts say you're getting closer! 🦆",
        ]
        return False, random.choice(messages), None
    
    def _select_treasure(self) -> Optional[Treasure]:
        """Select a random treasure based on location and rarity."""
        if not self.current_hunt_location:
            return None
        
        available = [
            t for t in TREASURES.values()
            if self.current_hunt_location in t.locations
        ]
        
        if not available:
            return None
        
        # Weight by rarity (rarer = less likely)
        weights = {
            TreasureRarity.COMMON: 50,
            TreasureRarity.UNCOMMON: 25,
            TreasureRarity.RARE: 10,
            TreasureRarity.EPIC: 4,
            TreasureRarity.LEGENDARY: 1,
            TreasureRarity.MYTHICAL: 0.1,
        }
        
        weighted = []
        for t in available:
            weight = weights.get(t.rarity, 1)
            weighted.extend([t] * int(weight * 10))
        
        if weighted:
            return random.choice(weighted)
        return random.choice(available)
    
    def _find_treasure(self, treasure_id: str, was_mapped: bool = False) -> Tuple[bool, str, Optional[FoundTreasure]]:
        """Record finding a treasure."""
        treasure = TREASURES.get(treasure_id)
        if not treasure:
            return False, "Error: Unknown treasure!", None
        
        found = FoundTreasure(
            treasure_id=treasure_id,
            found_at=datetime.now().isoformat(),
            location=self.current_hunt_location,
            was_mapped=was_mapped,
        )
        
        if treasure_id not in self.found_treasures:
            self.found_treasures[treasure_id] = []
        self.found_treasures[treasure_id].append(found)
        
        self.total_treasures_found += 1
        self.total_value_found += treasure.coin_value
        
        # Clear map if used
        if was_mapped and self.active_map:
            self.active_map.found = True
            self.active_map = None
        
        # Reset hunt
        self.current_hunt_location = None
        self.hunt_progress = 0
        
        rarity_emoji = {
            TreasureRarity.COMMON: "✓",
            TreasureRarity.UNCOMMON: "✦",
            TreasureRarity.RARE: "★",
            TreasureRarity.EPIC: "✮",
            TreasureRarity.LEGENDARY: "⭐",
            TreasureRarity.MYTHICAL: "🌟",
        }
        
        emoji = rarity_emoji.get(treasure.rarity, "✓")
        first_find = len(self.found_treasures[treasure_id]) == 1
        new_badge = " 🆕 First Find!" if first_find else ""
        
        return True, f"{emoji} TREASURE FOUND! {emoji}\n{treasure.name} {treasure.ascii_art}{new_badge}", found
    
    def use_map(self, map_id: str) -> Tuple[bool, str]:
        """Use a treasure map."""
        map_obj = next((m for m in self.treasure_maps if m.map_id == map_id and not m.found), None)
        if not map_obj:
            return False, "Map not found or already used!"
        
        if map_obj.location not in self.unlocked_locations:
            return False, f"You need to unlock {map_obj.location.value} first!"
        
        self.active_map = map_obj
        self.current_hunt_location = map_obj.location
        self.hunt_progress = 0
        
        return True, f"Following the map... Hint: {map_obj.hint}"
    
    def add_map(self, treasure_id: str) -> TreasureMap:
        """Generate a new treasure map."""
        treasure = TREASURES.get(treasure_id)
        if not treasure:
            treasure = random.choice(list(TREASURES.values()))
        
        location = random.choice(treasure.locations)
        hints = LOCATION_HINTS.get(location, ["Look carefully..."])
        
        new_map = TreasureMap(
            map_id=f"map_{len(self.treasure_maps) + 1}",
            treasure_id=treasure.id,
            location=location,
            hint=random.choice(hints),
            created_at=datetime.now().isoformat(),
        )
        self.treasure_maps.append(new_map)
        return new_map
    
    def unlock_location(self, location: TreasureLocation) -> Tuple[bool, str]:
        """Unlock a new treasure hunting location."""
        if location in self.unlocked_locations:
            return False, "Location already unlocked!"
        
        self.unlocked_locations.append(location)
        return True, f"Unlocked {location.value} for treasure hunting! 🗺️"
    
    def get_collection_stats(self) -> Dict:
        """Get treasure collection statistics."""
        total = len(TREASURES)
        found = len(self.found_treasures)
        
        by_rarity = {}
        for tid in self.found_treasures:
            treasure = TREASURES.get(tid)
            if treasure:
                rarity = treasure.rarity.value
                by_rarity[rarity] = by_rarity.get(rarity, 0) + 1
        
        return {
            "total_types": total,
            "found_types": found,
            "completion": round(found / total * 100, 1),
            "total_found": self.total_treasures_found,
            "total_value": self.total_value_found,
            "by_rarity": by_rarity,
            "unlocked_locations": len(self.unlocked_locations),
            "maps_available": len([m for m in self.treasure_maps if not m.found]),
        }
    
    def render_collection(self) -> List[str]:
        """Render treasure collection display."""
        stats = self.get_collection_stats()
        
        lines = [
            "╔════════════════════════════════════════╗",
            "║       💎 TREASURE COLLECTION 💎        ║",
            f"║ Found: {stats['found_types']}/{stats['total_types']} ({stats['completion']}%)            ║",
            f"║ Total Value: {stats['total_value']:,} coins            ║",
            "╠════════════════════════════════════════╣",
        ]
        
        for tid, treasure in TREASURES.items():
            if tid in self.found_treasures:
                count = len(self.found_treasures[tid])
                lines.append(f"║ {treasure.ascii_art} {treasure.name:20} x{count} ║")
            else:
                lines.append(f"║ ??? {'Unknown Treasure':20}    ║")
        
        lines.append("╚════════════════════════════════════════╝")
        return lines
    
    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "found_treasures": {
                tid: [
                    {
                        "treasure_id": f.treasure_id,
                        "found_at": f.found_at,
                        "location": f.location.value,
                        "was_mapped": f.was_mapped,
                    }
                    for f in finds
                ]
                for tid, finds in self.found_treasures.items()
            },
            "treasure_maps": [
                {
                    "map_id": m.map_id,
                    "treasure_id": m.treasure_id,
                    "location": m.location.value,
                    "hint": m.hint,
                    "found": m.found,
                    "created_at": m.created_at,
                }
                for m in self.treasure_maps
            ],
            "total_treasures_found": self.total_treasures_found,
            "total_value_found": self.total_value_found,
            "unlocked_locations": [l.value for l in self.unlocked_locations],
            "dig_attempts_today": self.dig_attempts_today,
            "last_dig_date": self.last_dig_date,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "TreasureHunter":
        """Create from dictionary."""
        hunter = cls()
        
        for tid, finds in data.get("found_treasures", {}).items():
            hunter.found_treasures[tid] = [
                FoundTreasure(
                    treasure_id=f["treasure_id"],
                    found_at=f["found_at"],
                    location=TreasureLocation(f["location"]),
                    was_mapped=f.get("was_mapped", False),
                )
                for f in finds
            ]
        
        hunter.treasure_maps = [
            TreasureMap(
                map_id=m["map_id"],
                treasure_id=m["treasure_id"],
                location=TreasureLocation(m["location"]),
                hint=m["hint"],
                found=m.get("found", False),
                created_at=m.get("created_at", ""),
            )
            for m in data.get("treasure_maps", [])
        ]
        
        hunter.total_treasures_found = data.get("total_treasures_found", 0)
        hunter.total_value_found = data.get("total_value_found", 0)
        hunter.unlocked_locations = [TreasureLocation(l) for l in data.get("unlocked_locations", ["beach", "garden"])]
        hunter.dig_attempts_today = data.get("dig_attempts_today", 0)
        hunter.last_dig_date = data.get("last_dig_date", "")
        
        return hunter


# Global treasure hunter instance
treasure_hunter = TreasureHunter()
