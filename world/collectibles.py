"""
Collectibles System - Collectible cards, stickers, and trading.
Features albums, rarity tiers, and set bonuses.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Set
from enum import Enum
import random


class CollectibleRarity(Enum):
    """Rarity tiers for collectibles."""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    MYTHIC = "mythic"


class CollectibleType(Enum):
    """Types of collectibles."""
    CARD = "card"
    STICKER = "sticker"
    STAMP = "stamp"
    BADGE = "badge"


@dataclass
class Collectible:
    """A collectible item."""
    id: str
    name: str
    collectible_type: CollectibleType
    rarity: CollectibleRarity
    set_id: str
    set_position: int
    description: str
    image_art: List[str]  # ASCII art lines
    flavor_text: str = ""
    special_effect: Optional[str] = None


@dataclass
class CollectibleSet:
    """A set/album of collectibles."""
    id: str
    name: str
    description: str
    theme: str
    total_items: int
    set_bonus: str
    bonus_reward: Dict[str, int]  # xp, coins, etc


@dataclass
class OwnedCollectible:
    """A collectible owned by the player."""
    collectible_id: str
    obtained_at: str
    obtained_from: str  # how they got it
    is_shiny: bool = False
    duplicate_count: int = 0


# Collectible Sets
SETS: Dict[str, CollectibleSet] = {
    "duck_portraits": CollectibleSet(
        id="duck_portraits",
        name="Duck Portraits Collection",
        description="Famous ducks throughout history",
        theme="historical",
        total_items=8,
        set_bonus="Historical Duck Title",
        bonus_reward={"xp": 500, "coins": 300},
    ),
    "pond_life": CollectibleSet(
        id="pond_life",
        name="Life at the Pond",
        description="Creatures and plants from the pond",
        theme="nature",
        total_items=10,
        set_bonus="Pond Master Badge",
        bonus_reward={"xp": 400, "coins": 250},
    ),
    "weather_wonders": CollectibleSet(
        id="weather_wonders",
        name="Weather Wonders",
        description="Weather phenomena and conditions",
        theme="weather",
        total_items=6,
        set_bonus="Weather Wizard Hat",
        bonus_reward={"xp": 350, "coins": 200},
    ),
    "food_feast": CollectibleSet(
        id="food_feast",
        name="Duck's Feast",
        description="Delicious foods for ducks",
        theme="food",
        total_items=8,
        set_bonus="Gourmet Chef Apron",
        bonus_reward={"xp": 300, "coins": 200},
    ),
    "emotions": CollectibleSet(
        id="emotions",
        name="Quack Expressions",
        description="Different duck moods and emotions",
        theme="emotions",
        total_items=6,
        set_bonus="Emotion Reader Title",
        bonus_reward={"xp": 250, "coins": 150},
    ),
    "seasons": CollectibleSet(
        id="seasons",
        name="Four Seasons",
        description="The beauty of each season",
        theme="seasons",
        total_items=4,
        set_bonus="Seasonal Spirit",
        bonus_reward={"xp": 600, "coins": 400},
    ),
    "legendary_ducks": CollectibleSet(
        id="legendary_ducks",
        name="Legendary Ducks",
        description="Mythical and legendary duck beings",
        theme="mythology",
        total_items=5,
        set_bonus="Legendary Status",
        bonus_reward={"xp": 1000, "coins": 750},
    ),
}

# Individual Collectibles
COLLECTIBLES: Dict[str, Collectible] = {
    # Duck Portraits Set
    "portrait_cheese": Collectible(
        id="portrait_cheese",
        name="Cheese Portrait",
        collectible_type=CollectibleType.CARD,
        rarity=CollectibleRarity.RARE,
        set_id="duck_portraits",
        set_position=1,
        description="An elegant portrait of Cheese the Duck",
        image_art=[
            "╔══════════╗",
            "║  .--.    ║",
            "║ (_ ^ _)  ║",
            "║  (__)    ║",
            "╚══════════╝",
        ],
        flavor_text="The one and only!",
    ),
    "portrait_emperor": Collectible(
        id="portrait_emperor",
        name="Emperor Duck",
        collectible_type=CollectibleType.CARD,
        rarity=CollectibleRarity.EPIC,
        set_id="duck_portraits",
        set_position=2,
        description="The legendary Emperor Duck",
        image_art=[
            "╔══════════╗",
            "║  👑      ║",
            "║ (_ ^ _)  ║",
            "║  (__)    ║",
            "╚══════════╝",
        ],
        flavor_text="Ruler of the Great Pond",
    ),
    "portrait_scholar": Collectible(
        id="portrait_scholar",
        name="Scholar Duck",
        collectible_type=CollectibleType.CARD,
        rarity=CollectibleRarity.UNCOMMON,
        set_id="duck_portraits",
        set_position=3,
        description="A wise scholar duck with glasses",
        image_art=[
            "╔══════════╗",
            "║  .--.    ║",
            "║ (o o)    ║",
            "║  (__)    ║",
            "╚══════════╝",
        ],
        flavor_text="Knowledge is power!",
    ),
    "portrait_artist": Collectible(
        id="portrait_artist",
        name="Artist Duck",
        collectible_type=CollectibleType.CARD,
        rarity=CollectibleRarity.UNCOMMON,
        set_id="duck_portraits",
        set_position=4,
        description="A creative artist duck",
        image_art=[
            "╔══════════╗",
            "║  🎨      ║",
            "║ (_ ^ _)  ║",
            "║  (__)    ║",
            "╚══════════╝",
        ],
        flavor_text="Every quack is a masterpiece",
    ),
    "portrait_explorer": Collectible(
        id="portrait_explorer",
        name="Explorer Duck",
        collectible_type=CollectibleType.CARD,
        rarity=CollectibleRarity.RARE,
        set_id="duck_portraits",
        set_position=5,
        description="An adventurous explorer",
        image_art=[
            "╔══════════╗",
            "║  ⛏️      ║",
            "║ (_ ^ _)  ║",
            "║  (__)    ║",
            "╚══════════╝",
        ],
        flavor_text="Adventure awaits!",
    ),
    
    # Pond Life Set
    "pond_frog": Collectible(
        id="pond_frog",
        name="Friendly Frog",
        collectible_type=CollectibleType.STICKER,
        rarity=CollectibleRarity.COMMON,
        set_id="pond_life",
        set_position=1,
        description="A friendly frog from the pond",
        image_art=[
            "  @..@  ",
            " (----)  ",
            "( >  < ) ",
            " ^    ^  ",
        ],
        flavor_text="Ribbit!",
    ),
    "pond_lily": Collectible(
        id="pond_lily",
        name="Water Lily",
        collectible_type=CollectibleType.STICKER,
        rarity=CollectibleRarity.COMMON,
        set_id="pond_life",
        set_position=2,
        description="A beautiful water lily",
        image_art=[
            "  _/\\_  ",
            " (____)  ",
            "~~~~~~~",
        ],
        flavor_text="Peaceful and serene",
    ),
    "pond_dragonfly": Collectible(
        id="pond_dragonfly",
        name="Dragonfly",
        collectible_type=CollectibleType.STICKER,
        rarity=CollectibleRarity.UNCOMMON,
        set_id="pond_life",
        set_position=3,
        description="A shimmering dragonfly",
        image_art=[
            " \\|/  ",
            " -o-  ",
            " /|\\  ",
        ],
        flavor_text="Swift and beautiful",
    ),
    "pond_fish": Collectible(
        id="pond_fish",
        name="Golden Fish",
        collectible_type=CollectibleType.STICKER,
        rarity=CollectibleRarity.RARE,
        set_id="pond_life",
        set_position=4,
        description="A rare golden fish",
        image_art=[
            "  ><>  ",
        ],
        flavor_text="Lucky find!",
    ),
    
    # Weather Wonders Set
    "weather_sun": Collectible(
        id="weather_sun",
        name="Sunny Day",
        collectible_type=CollectibleType.STAMP,
        rarity=CollectibleRarity.COMMON,
        set_id="weather_wonders",
        set_position=1,
        description="A bright sunny day",
        image_art=[
            " \\|/  ",
            "-- ☀ --",
            " /|\\  ",
        ],
        flavor_text="Perfect weather!",
    ),
    "weather_rain": Collectible(
        id="weather_rain",
        name="Rainy Day",
        collectible_type=CollectibleType.STAMP,
        rarity=CollectibleRarity.COMMON,
        set_id="weather_wonders",
        set_position=2,
        description="A cozy rainy day",
        image_art=[
            "  ☁️   ",
            " , , , ",
            "' ' ' '",
        ],
        flavor_text="Splish splash!",
    ),
    "weather_rainbow": Collectible(
        id="weather_rainbow",
        name="Rainbow",
        collectible_type=CollectibleType.STAMP,
        rarity=CollectibleRarity.EPIC,
        set_id="weather_wonders",
        set_position=3,
        description="A magical rainbow",
        image_art=[
            "  🌈   ",
        ],
        flavor_text="Double rainbow!",
    ),
    "weather_snow": Collectible(
        id="weather_snow",
        name="Snowy Day",
        collectible_type=CollectibleType.STAMP,
        rarity=CollectibleRarity.UNCOMMON,
        set_id="weather_wonders",
        set_position=4,
        description="A beautiful snowy day",
        image_art=[
            " ❄️ ❄️ ❄️ ",
            "  ❄️ ❄️  ",
        ],
        flavor_text="Let it snow!",
    ),
    
    # Legendary Ducks Set
    "legend_phoenix": Collectible(
        id="legend_phoenix",
        name="Phoenix Duck",
        collectible_type=CollectibleType.CARD,
        rarity=CollectibleRarity.MYTHIC,
        set_id="legendary_ducks",
        set_position=1,
        description="The immortal Phoenix Duck",
        image_art=[
            "  🔥🔥🔥  ",
            " (_ ^ _) ",
            "  🔥🔥   ",
        ],
        flavor_text="Rises from the ashes",
        special_effect="Grants rebirth protection once",
    ),
    "legend_dragon": Collectible(
        id="legend_dragon",
        name="Dragon Duck",
        collectible_type=CollectibleType.CARD,
        rarity=CollectibleRarity.MYTHIC,
        set_id="legendary_ducks",
        set_position=2,
        description="The mighty Dragon Duck",
        image_art=[
            "  🐉     ",
            " (_ ^ _) ",
            "  ~~~~   ",
        ],
        flavor_text="Breathes fire and wisdom",
        special_effect="Doubles XP for one hour",
    ),
}

# Rarity drop weights
RARITY_WEIGHTS = {
    CollectibleRarity.COMMON: 45,
    CollectibleRarity.UNCOMMON: 30,
    CollectibleRarity.RARE: 15,
    CollectibleRarity.EPIC: 7,
    CollectibleRarity.LEGENDARY: 2.5,
    CollectibleRarity.MYTHIC: 0.5,
}


class CollectiblesSystem:
    """
    Manages collectibles, albums, and trading.
    """
    
    def __init__(self):
        self.owned: Dict[str, OwnedCollectible] = {}  # collectible_id -> owned
        self.completed_sets: List[str] = []
        self.total_collected: int = 0
        self.shiny_count: int = 0
        self.favorite_collectible: Optional[str] = None
        self.packs_opened: int = 0
        self.trade_history: List[Dict] = []
    
    def open_pack(self, pack_type: str = "standard") -> Tuple[bool, str, List[Collectible]]:
        """Open a collectible pack."""
        pack_sizes = {
            "standard": 3,
            "premium": 5,
            "mega": 8,
        }
        
        count = pack_sizes.get(pack_type, 3)
        
        # Determine rarities
        results = []
        for _ in range(count):
            # Weighted random rarity
            roll = random.uniform(0, 100)
            cumulative = 0
            selected_rarity = CollectibleRarity.COMMON
            
            for rarity, weight in RARITY_WEIGHTS.items():
                cumulative += weight
                if roll <= cumulative:
                    selected_rarity = rarity
                    break
            
            # Find collectibles of that rarity
            matching = [
                c for c in COLLECTIBLES.values()
                if c.rarity == selected_rarity
            ]
            
            if not matching:
                matching = list(COLLECTIBLES.values())
            
            collectible = random.choice(matching)
            results.append(collectible)
            
            # Add to collection
            self._add_collectible(collectible)
        
        self.packs_opened += 1
        
        names = ", ".join(c.name for c in results)
        return True, f"🎴 Pack opened! Got: {names}", results
    
    def _add_collectible(self, collectible: Collectible):
        """Add a collectible to the collection."""
        # 5% chance of shiny
        is_shiny = random.random() < 0.05
        
        if collectible.id in self.owned:
            self.owned[collectible.id].duplicate_count += 1
        else:
            self.owned[collectible.id] = OwnedCollectible(
                collectible_id=collectible.id,
                obtained_at=datetime.now().isoformat(),
                obtained_from="pack",
                is_shiny=is_shiny,
            )
            self.total_collected += 1
            
            if is_shiny:
                self.shiny_count += 1
        
        # Check for set completion
        self._check_set_completion(collectible.set_id)
    
    def _check_set_completion(self, set_id: str) -> bool:
        """Check if a set is complete."""
        if set_id in self.completed_sets:
            return True
        
        set_def = SETS.get(set_id)
        if not set_def:
            return False
        
        # Count owned from this set
        owned_in_set = sum(
            1 for cid, _ in self.owned.items()
            if COLLECTIBLES.get(cid, Collectible("", "", CollectibleType.CARD, CollectibleRarity.COMMON, "", 0, "", [])).set_id == set_id
        )
        
        if owned_in_set >= set_def.total_items:
            self.completed_sets.append(set_id)
            return True
        
        return False
    
    def get_set_progress(self, set_id: str) -> Tuple[int, int, List[str]]:
        """Get progress on a specific set."""
        set_def = SETS.get(set_id)
        if not set_def:
            return 0, 0, []
        
        owned_ids = []
        for cid in self.owned.keys():
            collectible = COLLECTIBLES.get(cid)
            if collectible and collectible.set_id == set_id:
                owned_ids.append(cid)
        
        return len(owned_ids), set_def.total_items, owned_ids
    
    def get_collection_stats(self) -> Dict:
        """Get overall collection statistics."""
        total_possible = len(COLLECTIBLES)
        unique_owned = len(self.owned)
        
        duplicates = sum(c.duplicate_count for c in self.owned.values())
        
        by_rarity = {}
        for cid in self.owned.keys():
            collectible = COLLECTIBLES.get(cid)
            if collectible:
                rarity = collectible.rarity.value
                by_rarity[rarity] = by_rarity.get(rarity, 0) + 1
        
        return {
            "unique_owned": unique_owned,
            "total_possible": total_possible,
            "completion_percent": (unique_owned / total_possible * 100) if total_possible > 0 else 0,
            "duplicates": duplicates,
            "shiny_count": self.shiny_count,
            "sets_completed": len(self.completed_sets),
            "total_sets": len(SETS),
            "by_rarity": by_rarity,
        }
    
    def trade_duplicates(self, collectible_ids: List[str]) -> Tuple[bool, str, Optional[Collectible]]:
        """Trade duplicate collectibles for a random new one."""
        if len(collectible_ids) < 3:
            return False, "Need at least 3 duplicates to trade!", None
        
        # Verify all are duplicates
        for cid in collectible_ids:
            owned = self.owned.get(cid)
            if not owned or owned.duplicate_count < 1:
                return False, f"Not enough duplicates of {cid}!", None
        
        # Remove duplicates
        for cid in collectible_ids:
            self.owned[cid].duplicate_count -= 1
        
        # Calculate trade value for rarity
        avg_rarity_value = 0
        for cid in collectible_ids:
            collectible = COLLECTIBLES.get(cid)
            if collectible:
                rarity_values = {
                    CollectibleRarity.COMMON: 1,
                    CollectibleRarity.UNCOMMON: 2,
                    CollectibleRarity.RARE: 4,
                    CollectibleRarity.EPIC: 8,
                    CollectibleRarity.LEGENDARY: 16,
                    CollectibleRarity.MYTHIC: 32,
                }
                avg_rarity_value += rarity_values.get(collectible.rarity, 1)
        
        avg_rarity_value /= len(collectible_ids)
        
        # Better chance of higher rarity based on trade value
        target_rarity = CollectibleRarity.COMMON
        if avg_rarity_value >= 8:
            target_rarity = CollectibleRarity.EPIC
        elif avg_rarity_value >= 4:
            target_rarity = CollectibleRarity.RARE
        elif avg_rarity_value >= 2:
            target_rarity = CollectibleRarity.UNCOMMON
        
        # Get collectible of appropriate rarity
        candidates = [
            c for c in COLLECTIBLES.values()
            if c.rarity == target_rarity
        ]
        
        if not candidates:
            candidates = list(COLLECTIBLES.values())
        
        new_collectible = random.choice(candidates)
        self._add_collectible(new_collectible)
        
        # Record trade
        self.trade_history.append({
            "traded": collectible_ids,
            "received": new_collectible.id,
            "timestamp": datetime.now().isoformat(),
        })

        # Keep history manageable to prevent memory leak
        if len(self.trade_history) > 100:
            self.trade_history = self.trade_history[-100:]

        return True, f"🔄 Trade successful! Got: {new_collectible.name}!", new_collectible
    
    def render_collection_album(self) -> List[str]:
        """Render the collection album view."""
        stats = self.get_collection_stats()
        
        lines = [
            "╔═══════════════════════════════════════════════╗",
            "║           🎴 COLLECTION ALBUM 🎴              ║",
            "╠═══════════════════════════════════════════════╣",
            f"║  Collected: {stats['unique_owned']:3}/{stats['total_possible']:<3} ({stats['completion_percent']:.1f}%)               ║",
            f"║  Shiny: {stats['shiny_count']:3}  |  Sets: {stats['sets_completed']}/{stats['total_sets']}                ║",
            "╠═══════════════════════════════════════════════╣",
            "║  SETS:                                        ║",
        ]
        
        for set_id, set_def in list(SETS.items())[:5]:
            owned, total, _ = self.get_set_progress(set_id)
            completed = "✓" if set_id in self.completed_sets else " "
            progress = f"{owned}/{total}"
            lines.append(f"║  [{completed}] {set_def.name[:25]:25} {progress:5}   ║")
        
        lines.extend([
            "╠═══════════════════════════════════════════════╣",
            "║  RARITY:                                      ║",
        ])
        
        for rarity in CollectibleRarity:
            count = stats['by_rarity'].get(rarity.value, 0)
            icon = {"common": "⚪", "uncommon": "🟢", "rare": "🔵", "epic": "🟣", "legendary": "🟡", "mythic": "🔴"}.get(rarity.value, "⚪")
            lines.append(f"║    {icon} {rarity.value.title():12}: {count:3}                    ║")
        
        lines.append("╚═══════════════════════════════════════════════╝")
        
        return lines
    
    def render_collectible_card(self, collectible_id: str) -> List[str]:
        """Render a single collectible card."""
        collectible = COLLECTIBLES.get(collectible_id)
        if not collectible:
            return ["Collectible not found!"]
        
        owned = self.owned.get(collectible_id)
        
        rarity_colors = {
            CollectibleRarity.COMMON: "⚪",
            CollectibleRarity.UNCOMMON: "🟢",
            CollectibleRarity.RARE: "🔵",
            CollectibleRarity.EPIC: "🟣",
            CollectibleRarity.LEGENDARY: "🟡",
            CollectibleRarity.MYTHIC: "🔴",
        }
        
        rarity_icon = rarity_colors.get(collectible.rarity, "⚪")
        shiny = "✨" if owned and owned.is_shiny else ""
        
        lines = [
            "╔════════════════════════════════════╗",
            f"║ {shiny}{collectible.name:^32}{shiny} ║",
            f"║  {rarity_icon} {collectible.rarity.value.title():^29}  ║",
            "╠════════════════════════════════════╣",
        ]
        
        # Add art
        for art_line in collectible.image_art:
            lines.append(f"║  {art_line:^32}  ║")
        
        lines.append("╠════════════════════════════════════╣")
        
        # Description (word wrap)
        desc = collectible.description
        while desc:
            lines.append(f"║  {desc[:32]:32}  ║")
            desc = desc[32:]
        
        if collectible.flavor_text:
            lines.append(f"║  \"{collectible.flavor_text[:28]:28}\"  ║")
        
        if owned:
            dupe = f"+{owned.duplicate_count}" if owned.duplicate_count > 0 else ""
            lines.append(f"║  Owned {dupe:^27}  ║")
        else:
            lines.append("║  ??? Not Owned ???                 ║")
        
        lines.append("╚════════════════════════════════════╝")
        
        return lines
    
    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "owned": {
                cid: {
                    "collectible_id": c.collectible_id,
                    "obtained_at": c.obtained_at,
                    "obtained_from": c.obtained_from,
                    "is_shiny": c.is_shiny,
                    "duplicate_count": c.duplicate_count,
                }
                for cid, c in self.owned.items()
            },
            "completed_sets": self.completed_sets,
            "total_collected": self.total_collected,
            "shiny_count": self.shiny_count,
            "favorite_collectible": self.favorite_collectible,
            "packs_opened": self.packs_opened,
            "trade_history": self.trade_history,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "CollectiblesSystem":
        """Create from dictionary."""
        system = cls()
        
        for cid, cdata in data.get("owned", {}).items():
            system.owned[cid] = OwnedCollectible(
                collectible_id=cdata["collectible_id"],
                obtained_at=cdata["obtained_at"],
                obtained_from=cdata.get("obtained_from", "unknown"),
                is_shiny=cdata.get("is_shiny", False),
                duplicate_count=cdata.get("duplicate_count", 0),
            )
        
        system.completed_sets = data.get("completed_sets", [])
        system.total_collected = data.get("total_collected", 0)
        system.shiny_count = data.get("shiny_count", 0)
        system.favorite_collectible = data.get("favorite_collectible")
        system.packs_opened = data.get("packs_opened", 0)
        system.trade_history = data.get("trade_history", [])
        
        return system


# Global collectibles system instance
collectibles_system = CollectiblesSystem()
