"""
Fishing Mini-System - A relaxing fishing minigame with various fish types.
Features different fishing spots, bait types, and collectible fish.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random
import time


class FishRarity(Enum):
    """Rarity tiers for fish."""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    MYTHICAL = "mythical"


class FishingSpot(Enum):
    """Different locations to fish."""
    POND = "pond"
    RIVER = "river"
    LAKE = "lake"
    OCEAN = "ocean"
    SECRET_COVE = "secret_cove"


class BaitType(Enum):
    """Types of bait that affect catch rates."""
    BREAD = "bread"
    WORMS = "worms"
    SEEDS = "seeds"
    SPECIAL = "special"
    GOLDEN = "golden"


@dataclass
class Fish:
    """A type of fish that can be caught."""
    id: str
    name: str
    description: str
    rarity: FishRarity
    min_size: float  # in cm
    max_size: float
    base_catch_rate: float  # 0.0 to 1.0
    spots: List[FishingSpot]  # Where it can be found
    preferred_bait: List[BaitType]
    time_of_day: List[str]  # morning, afternoon, evening, night, any
    season: List[str]  # spring, summer, fall, winter, any
    ascii_art: List[str]
    xp_value: int
    coin_value: int
    fun_fact: str


@dataclass
class CaughtFish:
    """A specific fish that was caught."""
    fish_id: str
    size: float
    caught_at: str  # ISO datetime
    spot: FishingSpot
    bait_used: BaitType
    is_record: bool = False


# Fish Database
FISH_DATABASE: Dict[str, Fish] = {
    # Common fish
    "minnow": Fish(
        id="minnow",
        name="Minnow",
        description="A tiny, quick little fish. Good for beginners!",
        rarity=FishRarity.COMMON,
        min_size=2.0, max_size=5.0,
        base_catch_rate=0.8,
        spots=[FishingSpot.POND, FishingSpot.RIVER, FishingSpot.LAKE],
        preferred_bait=[BaitType.BREAD],
        time_of_day=["any"],
        season=["any"],
        ascii_art=["><>"],
        xp_value=5, coin_value=2,
        fun_fact="Minnows travel in schools for protection!",
    ),
    "goldfish": Fish(
        id="goldfish",
        name="Goldfish",
        description="A pretty golden fish that sparkles in the sun!",
        rarity=FishRarity.COMMON,
        min_size=5.0, max_size=15.0,
        base_catch_rate=0.7,
        spots=[FishingSpot.POND, FishingSpot.LAKE],
        preferred_bait=[BaitType.BREAD, BaitType.SEEDS],
        time_of_day=["morning", "afternoon"],
        season=["any"],
        ascii_art=["<º)))><"],
        xp_value=8, coin_value=5,
        fun_fact="Goldfish can recognize their owners!",
    ),
    "carp": Fish(
        id="carp",
        name="Carp",
        description="A chunky, reliable fish. Great for learning!",
        rarity=FishRarity.COMMON,
        min_size=20.0, max_size=50.0,
        base_catch_rate=0.6,
        spots=[FishingSpot.RIVER, FishingSpot.LAKE],
        preferred_bait=[BaitType.WORMS],
        time_of_day=["any"],
        season=["any"],
        ascii_art=["><(((('>"],
        xp_value=10, coin_value=8,
        fun_fact="Carp can live for over 20 years!",
    ),
    
    # Uncommon fish
    "bass": Fish(
        id="bass",
        name="Bass",
        description="A feisty fish that puts up a good fight!",
        rarity=FishRarity.UNCOMMON,
        min_size=25.0, max_size=60.0,
        base_catch_rate=0.5,
        spots=[FishingSpot.LAKE, FishingSpot.RIVER],
        preferred_bait=[BaitType.WORMS],
        time_of_day=["morning", "evening"],
        season=["spring", "summer", "fall"],
        ascii_art=["><(((º>"],
        xp_value=20, coin_value=15,
        fun_fact="Bass are ambush predators!",
    ),
    "catfish": Fish(
        id="catfish",
        name="Catfish",
        description="A whiskered bottom-dweller. Very chill!",
        rarity=FishRarity.UNCOMMON,
        min_size=30.0, max_size=80.0,
        base_catch_rate=0.45,
        spots=[FishingSpot.RIVER, FishingSpot.LAKE],
        preferred_bait=[BaitType.WORMS, BaitType.SPECIAL],
        time_of_day=["night", "evening"],
        season=["any"],
        ascii_art=["=<º))))><"],
        xp_value=25, coin_value=20,
        fun_fact="Catfish can taste with their entire body!",
    ),
    "trout": Fish(
        id="trout",
        name="Rainbow Trout",
        description="Beautiful and colorful! A prized catch!",
        rarity=FishRarity.UNCOMMON,
        min_size=20.0, max_size=50.0,
        base_catch_rate=0.4,
        spots=[FishingSpot.RIVER],
        preferred_bait=[BaitType.WORMS, BaitType.SPECIAL],
        time_of_day=["morning"],
        season=["spring", "summer"],
        ascii_art=["🌈><º>"],
        xp_value=30, coin_value=25,
        fun_fact="Rainbow trout can leap 3 feet out of water!",
    ),
    
    # Rare fish
    "koi": Fish(
        id="koi",
        name="Koi Fish",
        description="An elegant, colorful fish. Symbol of luck!",
        rarity=FishRarity.RARE,
        min_size=30.0, max_size=70.0,
        base_catch_rate=0.25,
        spots=[FishingSpot.POND, FishingSpot.SECRET_COVE],
        preferred_bait=[BaitType.SPECIAL],
        time_of_day=["morning", "evening"],
        season=["spring", "summer"],
        ascii_art=["🎏><º)))><"],
        xp_value=50, coin_value=50,
        fun_fact="Koi can live for over 200 years!",
    ),
    "salmon": Fish(
        id="salmon",
        name="Salmon",
        description="A powerful swimmer! Swims upstream!",
        rarity=FishRarity.RARE,
        min_size=50.0, max_size=100.0,
        base_catch_rate=0.3,
        spots=[FishingSpot.RIVER, FishingSpot.OCEAN],
        preferred_bait=[BaitType.WORMS, BaitType.SPECIAL],
        time_of_day=["morning", "evening"],
        season=["fall"],
        ascii_art=["<º)))>><"],
        xp_value=60, coin_value=60,
        fun_fact="Salmon return to where they were born to spawn!",
    ),
    "pufferfish": Fish(
        id="pufferfish",
        name="Pufferfish",
        description="Round and spiky! Puffs up when scared!",
        rarity=FishRarity.RARE,
        min_size=10.0, max_size=30.0,
        base_catch_rate=0.2,
        spots=[FishingSpot.OCEAN, FishingSpot.SECRET_COVE],
        preferred_bait=[BaitType.SPECIAL],
        time_of_day=["any"],
        season=["summer"],
        ascii_art=["<(°o°)>"],
        xp_value=70, coin_value=70,
        fun_fact="Pufferfish are one of the most poisonous vertebrates!",
    ),
    
    # Epic fish
    "swordfish": Fish(
        id="swordfish",
        name="Swordfish",
        description="A majestic fish with a sword-like snout!",
        rarity=FishRarity.EPIC,
        min_size=100.0, max_size=300.0,
        base_catch_rate=0.1,
        spots=[FishingSpot.OCEAN],
        preferred_bait=[BaitType.SPECIAL, BaitType.GOLDEN],
        time_of_day=["morning", "evening"],
        season=["summer", "fall"],
        ascii_art=["=======>°>"],
        xp_value=150, coin_value=150,
        fun_fact="Swordfish can swim up to 60 mph!",
    ),
    "sturgeon": Fish(
        id="sturgeon",
        name="Sturgeon",
        description="An ancient fish, living fossil!",
        rarity=FishRarity.EPIC,
        min_size=100.0, max_size=400.0,
        base_catch_rate=0.08,
        spots=[FishingSpot.RIVER, FishingSpot.LAKE],
        preferred_bait=[BaitType.SPECIAL, BaitType.GOLDEN],
        time_of_day=["night"],
        season=["any"],
        ascii_art=["<º≈≈≈≈))))><"],
        xp_value=200, coin_value=200,
        fun_fact="Sturgeon can live for over 100 years!",
    ),
    
    # Legendary fish
    "golden_koi": Fish(
        id="golden_koi",
        name="Golden Koi",
        description="A mythical golden koi! Extremely rare!",
        rarity=FishRarity.LEGENDARY,
        min_size=50.0, max_size=100.0,
        base_catch_rate=0.03,
        spots=[FishingSpot.SECRET_COVE],
        preferred_bait=[BaitType.GOLDEN],
        time_of_day=["morning"],
        season=["spring"],
        ascii_art=["✨><(((°>✨"],
        xp_value=500, coin_value=500,
        fun_fact="Legend says seeing a golden koi brings 100 years of luck!",
    ),
    "ghost_fish": Fish(
        id="ghost_fish",
        name="Ghost Fish",
        description="A translucent, ethereal fish from the deep!",
        rarity=FishRarity.LEGENDARY,
        min_size=20.0, max_size=50.0,
        base_catch_rate=0.02,
        spots=[FishingSpot.SECRET_COVE, FishingSpot.LAKE],
        preferred_bait=[BaitType.GOLDEN],
        time_of_day=["night"],
        season=["winter"],
        ascii_art=["👻><°>👻"],
        xp_value=600, coin_value=600,
        fun_fact="Ghost fish can only be seen under moonlight!",
    ),
    
    # Mythical fish
    "ancient_dragon_fish": Fish(
        id="ancient_dragon_fish",
        name="Ancient Dragon Fish",
        description="THE legendary fish of myth! Said to grant wishes!",
        rarity=FishRarity.MYTHICAL,
        min_size=200.0, max_size=500.0,
        base_catch_rate=0.005,
        spots=[FishingSpot.SECRET_COVE],
        preferred_bait=[BaitType.GOLDEN],
        time_of_day=["night"],
        season=["any"],
        ascii_art=["🐉><(((((º>🐉"],
        xp_value=2000, coin_value=2000,
        fun_fact="Only the most patient and skilled fishers ever see this fish!",
    ),
}

# Fishing spot descriptions and unlock requirements
FISHING_SPOTS = {
    FishingSpot.POND: {
        "name": "Peaceful Pond",
        "description": "A quiet, serene pond perfect for beginners.",
        "unlock_level": 1,
        "difficulty": 1,
        "ascii": [
            "  ~~~~~~~~~~~  ",
            " ~~~~~~~~~~~~~ ",
            "~~~~~~~~~~~~~~~",
            " ~~~~~~~~~~~~~ ",
            "  ~~~~~~~~~~~  ",
        ],
    },
    FishingSpot.RIVER: {
        "name": "Rushing River",
        "description": "A flowing river with diverse fish!",
        "unlock_level": 3,
        "difficulty": 2,
        "ascii": [
            "≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈",
            "≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈",
            "≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈",
        ],
    },
    FishingSpot.LAKE: {
        "name": "Crystal Lake",
        "description": "A large, clear lake with big fish!",
        "unlock_level": 5,
        "difficulty": 3,
        "ascii": [
            "   ~~~~~~~~~~   ",
            "  ~~~~~~~~~~~~  ",
            " ~~~~~~~~~~~~~~ ",
            "~~~~~~~~~~~~~~~~",
            " ~~~~~~~~~~~~~~ ",
            "  ~~~~~~~~~~~~  ",
        ],
    },
    FishingSpot.OCEAN: {
        "name": "Deep Ocean",
        "description": "The vast ocean. Who knows what lurks below?",
        "unlock_level": 8,
        "difficulty": 4,
        "ascii": [
            "≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋",
            "≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋",
            "≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋",
            "≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋",
        ],
    },
    FishingSpot.SECRET_COVE: {
        "name": "Secret Cove",
        "description": "A hidden spot with legendary fish...",
        "unlock_level": 12,
        "difficulty": 5,
        "ascii": [
            "  ✨~~~~~✨  ",
            " ~~~~~~~~~~~ ",
            "~~~~~~~~~~~~~",
            " ~~~~~~~~~~~ ",
            "  ✨~~~~~✨  ",
        ],
    },
}


class FishingMinigame:
    """
    Fishing minigame state and logic.
    The duck casts a line and waits for fish to bite!
    """
    
    def __init__(self):
        self.current_spot: Optional[FishingSpot] = None
        self.current_bait: BaitType = BaitType.BREAD
        self.is_fishing: bool = False
        self.waiting_for_bite: bool = False
        self.bite_timer: float = 0.0
        self.reaction_window: float = 0.0
        self.hooked_fish: Optional[str] = None
        self.animation_frame: int = 0
        self.cast_time: float = 0.0
        
        # Player stats
        self.fish_caught: Dict[str, List[CaughtFish]] = {}
        self.total_catches: int = 0
        self.biggest_catch: Optional[CaughtFish] = None
        self.fish_records: Dict[str, float] = {}  # fish_id -> biggest size
        self.unlocked_spots: List[FishingSpot] = [FishingSpot.POND]
        self.bait_inventory: Dict[BaitType, int] = {
            BaitType.BREAD: 10,
            BaitType.WORMS: 0,
            BaitType.SEEDS: 5,
            BaitType.SPECIAL: 0,
            BaitType.GOLDEN: 0,
        }
    
    def start_fishing(self, spot: FishingSpot) -> Tuple[bool, str]:
        """Start fishing at a spot."""
        if spot not in self.unlocked_spots:
            return False, f"You haven't unlocked {FISHING_SPOTS[spot]['name']} yet!"
        
        if self.bait_inventory.get(self.current_bait, 0) <= 0:
            return False, f"You're out of {self.current_bait.value}!"
        
        self.current_spot = spot
        self.is_fishing = True
        self.waiting_for_bite = True
        self.bite_timer = random.uniform(3.0, 10.0)  # Random wait time
        self.cast_time = time.time()
        self.hooked_fish = None
        
        # Use bait
        self.bait_inventory[self.current_bait] -= 1
        
        return True, f"Casting line at {FISHING_SPOTS[spot]['name']}... 🎣"
    
    def update(self, delta_time: float) -> Optional[str]:
        """Update fishing state. Returns message if something happens."""
        if not self.is_fishing:
            return None
        
        self.animation_frame = (self.animation_frame + 1) % 4
        
        if self.waiting_for_bite:
            self.bite_timer -= delta_time
            
            if self.bite_timer <= 0:
                # A fish bites!
                fish = self._select_fish()
                if fish:
                    self.hooked_fish = fish.id
                    self.waiting_for_bite = False
                    self.reaction_window = 2.0  # 2 seconds to react
                    return f"❗ BITE! Press SPACE to reel in! ❗"
                else:
                    # No fish, try again
                    self.bite_timer = random.uniform(3.0, 8.0)
        else:
            # Reaction window
            self.reaction_window -= delta_time
            if self.reaction_window <= 0:
                # Missed!
                self.hooked_fish = None
                self.is_fishing = False
                return "The fish got away! 😢"
        
        return None
    
    def reel_in(self) -> Tuple[bool, str, Optional[CaughtFish]]:
        """Try to reel in the fish."""
        if not self.hooked_fish:
            return False, "No fish on the line!", None
        
        fish = FISH_DATABASE.get(self.hooked_fish)
        if not fish:
            self.is_fishing = False
            return False, "The fish escaped!", None
        
        # Calculate catch success based on reaction time and difficulty
        difficulty = FISHING_SPOTS.get(self.current_spot, {}).get("difficulty", 1)
        base_success = fish.base_catch_rate
        
        # Bait bonus
        if self.current_bait in fish.preferred_bait:
            base_success *= 1.5
        
        # Difficulty modifier
        base_success /= (difficulty * 0.5)
        
        # Roll for success
        if random.random() < min(0.95, base_success):
            # Caught it!
            size = round(random.uniform(fish.min_size, fish.max_size), 1)
            is_record = size > self.fish_records.get(fish.id, 0)
            
            if is_record:
                self.fish_records[fish.id] = size
            
            caught = CaughtFish(
                fish_id=fish.id,
                size=size,
                caught_at=datetime.now().isoformat(),
                spot=self.current_spot,
                bait_used=self.current_bait,
                is_record=is_record,
            )
            
            if fish.id not in self.fish_caught:
                self.fish_caught[fish.id] = []
            self.fish_caught[fish.id].append(caught)
            self.total_catches += 1
            
            if not self.biggest_catch or size > self.biggest_catch.size:
                self.biggest_catch = caught
            
            self.is_fishing = False
            self.hooked_fish = None
            
            record_text = " 🏆 NEW RECORD!" if is_record else ""
            return True, f"Caught a {fish.name}! {size}cm!{record_text} {fish.ascii_art[0]}", caught
        else:
            self.is_fishing = False
            self.hooked_fish = None
            return False, f"The {fish.name} got away... 😢", None
    
    def _select_fish(self) -> Optional[Fish]:
        """Select which fish bit based on conditions."""
        if not self.current_spot:
            return None
        
        # Get current time of day
        hour = datetime.now().hour
        if 5 <= hour < 12:
            time_of_day = "morning"
        elif 12 <= hour < 17:
            time_of_day = "afternoon"
        elif 17 <= hour < 21:
            time_of_day = "evening"
        else:
            time_of_day = "night"
        
        # Get current season
        month = datetime.now().month
        if month in [3, 4, 5]:
            season = "spring"
        elif month in [6, 7, 8]:
            season = "summer"
        elif month in [9, 10, 11]:
            season = "fall"
        else:
            season = "winter"
        
        # Filter available fish
        available = []
        for fish in FISH_DATABASE.values():
            if self.current_spot not in fish.spots:
                continue
            if "any" not in fish.time_of_day and time_of_day not in fish.time_of_day:
                continue
            if "any" not in fish.season and season not in fish.season:
                continue
            
            # Weight by catch rate
            weight = fish.base_catch_rate
            if self.current_bait in fish.preferred_bait:
                weight *= 2
            
            available.extend([fish] * int(weight * 100))
        
        if not available:
            return random.choice(list(FISH_DATABASE.values()))  # Fallback
        
        return random.choice(available)
    
    def cancel_fishing(self):
        """Cancel current fishing session."""
        self.is_fishing = False
        self.waiting_for_bite = False
        self.hooked_fish = None
    
    def get_fishing_animation(self) -> List[str]:
        """Get current fishing animation frame."""
        frames = [
            [
                "     🎣",
                "    ╱",
                "   ╱",
                "  ○",
                "~~~~~",
            ],
            [
                "    🎣",
                "    │",
                "    │",
                "    ○",
                "~~~~~",
            ],
            [
                "   🎣",
                "    ╲",
                "     ╲",
                "      ○",
                "  ~~~~~",
            ],
            [
                "    🎣",
                "    │",
                "    │",
                "    ○",
                " ~~~~~",
            ],
        ]
        
        if self.hooked_fish:
            # Excited animation when fish is hooked
            return [
                "    🎣❗",
                "    │",
                "   ~~~",
                "  🐟!!!",
                "~~~~~~",
            ]
        
        return frames[self.animation_frame % len(frames)]
    
    def unlock_spot(self, spot: FishingSpot):
        """Unlock a fishing spot."""
        if spot not in self.unlocked_spots:
            self.unlocked_spots.append(spot)
    
    def add_bait(self, bait_type: BaitType, amount: int):
        """Add bait to inventory."""
        self.bait_inventory[bait_type] = self.bait_inventory.get(bait_type, 0) + amount
    
    def get_fish_collection_stats(self) -> Dict[str, any]:
        """Get collection statistics."""
        total_species = len(FISH_DATABASE)
        caught_species = len(self.fish_caught)
        
        by_rarity = {}
        for fish_id in self.fish_caught:
            fish = FISH_DATABASE.get(fish_id)
            if fish:
                rarity = fish.rarity.value
                by_rarity[rarity] = by_rarity.get(rarity, 0) + 1
        
        return {
            "total_species": total_species,
            "caught_species": caught_species,
            "completion_percent": round(caught_species / total_species * 100, 1),
            "total_catches": self.total_catches,
            "by_rarity": by_rarity,
            "biggest_catch": self.biggest_catch,
        }
    
    def render_collection(self) -> List[str]:
        """Render fish collection display."""
        stats = self.get_fish_collection_stats()
        
        lines = [
            "╔══════════════════════════════════════════╗",
            "║          🐟 FISH COLLECTION 🐟           ║",
            f"║  Caught: {stats['caught_species']}/{stats['total_species']} ({stats['completion_percent']}%)              ║",
            "╠══════════════════════════════════════════╣",
        ]
        
        for fish_id, fish in FISH_DATABASE.items():
            if fish_id in self.fish_caught:
                catches = self.fish_caught[fish_id]
                record = self.fish_records.get(fish_id, 0)
                symbol = "✓"
                lines.append(f"║ {symbol} {fish.name:20} Best: {record}cm  ║")
            else:
                lines.append(f"║ ? {'???':20}              ║")
        
        lines.append("╚══════════════════════════════════════════╝")
        return lines
    
    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "fish_caught": {
                fid: [
                    {
                        "fish_id": c.fish_id,
                        "size": c.size,
                        "caught_at": c.caught_at,
                        "spot": c.spot.value,
                        "bait_used": c.bait_used.value,
                        "is_record": c.is_record,
                    }
                    for c in catches
                ]
                for fid, catches in self.fish_caught.items()
            },
            "total_catches": self.total_catches,
            "fish_records": self.fish_records,
            "unlocked_spots": [s.value for s in self.unlocked_spots],
            "bait_inventory": {k.value: v for k, v in self.bait_inventory.items()},
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "FishingMinigame":
        """Create from dictionary."""
        fishing = cls()
        
        for fid, catches in data.get("fish_caught", {}).items():
            fishing.fish_caught[fid] = [
                CaughtFish(
                    fish_id=c["fish_id"],
                    size=c["size"],
                    caught_at=c["caught_at"],
                    spot=FishingSpot(c["spot"]),
                    bait_used=BaitType(c["bait_used"]),
                    is_record=c.get("is_record", False),
                )
                for c in catches
            ]
        
        fishing.total_catches = data.get("total_catches", 0)
        fishing.fish_records = data.get("fish_records", {})
        fishing.unlocked_spots = [FishingSpot(s) for s in data.get("unlocked_spots", ["pond"])]
        fishing.bait_inventory = {BaitType(k): v for k, v in data.get("bait_inventory", {}).items()}
        
        return fishing


# Global fishing system instance
fishing_system = FishingMinigame()
