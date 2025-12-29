"""
Home Decorations System - Decorate and customize the duck's living space.
Features furniture, decorations, themes, and room layouts.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Set
from enum import Enum
import random


class DecorationCategory(Enum):
    """Categories of decorations."""
    FURNITURE = "furniture"
    WALL = "wall"
    FLOOR = "floor"
    LIGHTING = "lighting"
    PLANT = "plant"
    TOY = "toy"
    SEASONAL = "seasonal"
    SPECIAL = "special"


class DecorationRarity(Enum):
    """Rarity of decorations."""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class RoomType(Enum):
    """Types of rooms/areas."""
    BEDROOM = "bedroom"
    LIVING = "living"
    GARDEN = "garden"
    POND = "pond"
    KITCHEN = "kitchen"
    PLAY = "play"


@dataclass
class Decoration:
    """A decoration item."""
    id: str
    name: str
    description: str
    category: DecorationCategory
    rarity: DecorationRarity
    price: int
    size: Tuple[int, int]  # width, height in grid
    ascii_art: List[str]
    mood_bonus: int = 0
    comfort_bonus: int = 0
    beauty_bonus: int = 0
    allowed_rooms: List[RoomType] = field(default_factory=list)
    special_effect: Optional[str] = None
    seasonal: Optional[str] = None  # season when available


@dataclass
class PlacedDecoration:
    """A decoration placed in a room."""
    decoration_id: str
    room: RoomType
    position: Tuple[int, int]  # grid position
    placed_at: str
    rotation: int = 0  # 0, 90, 180, 270


@dataclass
class Room:
    """A room/area that can be decorated."""
    room_type: RoomType
    name: str
    size: Tuple[int, int]  # grid size
    unlocked: bool = True
    decorations: List[PlacedDecoration] = field(default_factory=list)
    theme: Optional[str] = None
    mood_modifier: int = 0
    comfort_level: int = 0


# Decoration Definitions
DECORATIONS: Dict[str, Decoration] = {
    # Furniture
    "cozy_bed": Decoration(
        id="cozy_bed",
        name="Cozy Duck Bed",
        description="A soft, comfortable bed for resting",
        category=DecorationCategory.FURNITURE,
        rarity=DecorationRarity.COMMON,
        price=50,
        size=(2, 2),
        ascii_art=[
            "╔════╗",
            "║~~~~║",
            "╚════╝",
        ],
        comfort_bonus=15,
        mood_bonus=5,
        allowed_rooms=[RoomType.BEDROOM],
    ),
    "nest_premium": Decoration(
        id="nest_premium",
        name="Premium Nest",
        description="A luxury nest with extra padding",
        category=DecorationCategory.FURNITURE,
        rarity=DecorationRarity.RARE,
        price=200,
        size=(2, 2),
        ascii_art=[
            " ╭──╮ ",
            "╭┤~~├╮",
            "╰────╯",
        ],
        comfort_bonus=30,
        mood_bonus=15,
        beauty_bonus=10,
        allowed_rooms=[RoomType.BEDROOM],
    ),
    "tiny_table": Decoration(
        id="tiny_table",
        name="Tiny Table",
        description="A small table for snacks",
        category=DecorationCategory.FURNITURE,
        rarity=DecorationRarity.COMMON,
        price=30,
        size=(1, 1),
        ascii_art=[
            "┌─┐",
            "│ │",
        ],
        allowed_rooms=[RoomType.LIVING, RoomType.KITCHEN],
    ),
    "cushion": Decoration(
        id="cushion",
        name="Soft Cushion",
        description="A comfy cushion to sit on",
        category=DecorationCategory.FURNITURE,
        rarity=DecorationRarity.COMMON,
        price=25,
        size=(1, 1),
        ascii_art=[
            "╭──╮",
            "╰──╯",
        ],
        comfort_bonus=10,
        allowed_rooms=[RoomType.BEDROOM, RoomType.LIVING],
    ),
    "bookshelf": Decoration(
        id="bookshelf",
        name="Mini Bookshelf",
        description="Store your favorite duck tales",
        category=DecorationCategory.FURNITURE,
        rarity=DecorationRarity.UNCOMMON,
        price=75,
        size=(2, 3),
        ascii_art=[
            "╔════╗",
            "║||||║",
            "║||||║",
            "╚════╝",
        ],
        beauty_bonus=10,
        allowed_rooms=[RoomType.LIVING, RoomType.BEDROOM],
    ),
    
    # Wall Decorations
    "picture_frame": Decoration(
        id="picture_frame",
        name="Picture Frame",
        description="Display your favorite memories",
        category=DecorationCategory.WALL,
        rarity=DecorationRarity.COMMON,
        price=20,
        size=(1, 1),
        ascii_art=[
            "┌──┐",
            "│🖼️│",
            "└──┘",
        ],
        beauty_bonus=5,
        mood_bonus=3,
        allowed_rooms=[RoomType.BEDROOM, RoomType.LIVING],
    ),
    "clock": Decoration(
        id="clock",
        name="Duck Clock",
        description="A clock with duck hands",
        category=DecorationCategory.WALL,
        rarity=DecorationRarity.UNCOMMON,
        price=40,
        size=(1, 1),
        ascii_art=[
            "╭─╮",
            "│○│",
            "╰─╯",
        ],
        allowed_rooms=[RoomType.LIVING, RoomType.KITCHEN],
    ),
    "mirror": Decoration(
        id="mirror",
        name="Pretty Mirror",
        description="Admire your beautiful feathers",
        category=DecorationCategory.WALL,
        rarity=DecorationRarity.UNCOMMON,
        price=60,
        size=(1, 2),
        ascii_art=[
            "╭──╮",
            "│◇◇│",
            "│◇◇│",
            "╰──╯",
        ],
        beauty_bonus=15,
        mood_bonus=5,
        allowed_rooms=[RoomType.BEDROOM, RoomType.LIVING],
    ),
    
    # Plants
    "potted_plant": Decoration(
        id="potted_plant",
        name="Potted Plant",
        description="A green friend to keep you company",
        category=DecorationCategory.PLANT,
        rarity=DecorationRarity.COMMON,
        price=25,
        size=(1, 1),
        ascii_art=[
            " 🌱 ",
            "╰┴╯",
        ],
        mood_bonus=5,
        beauty_bonus=5,
    ),
    "flower_pot": Decoration(
        id="flower_pot",
        name="Flower Pot",
        description="Pretty flowers to brighten the room",
        category=DecorationCategory.PLANT,
        rarity=DecorationRarity.COMMON,
        price=30,
        size=(1, 1),
        ascii_art=[
            " 🌸 ",
            "╰┴╯",
        ],
        mood_bonus=10,
        beauty_bonus=10,
    ),
    "bonsai": Decoration(
        id="bonsai",
        name="Bonsai Tree",
        description="A miniature tree, carefully cultivated",
        category=DecorationCategory.PLANT,
        rarity=DecorationRarity.RARE,
        price=150,
        size=(1, 2),
        ascii_art=[
            " 🌳 ",
            " │  ",
            "╰┴╯",
        ],
        mood_bonus=15,
        beauty_bonus=20,
        comfort_bonus=5,
    ),
    
    # Lighting
    "lamp": Decoration(
        id="lamp",
        name="Cozy Lamp",
        description="Warm lighting for dark nights",
        category=DecorationCategory.LIGHTING,
        rarity=DecorationRarity.COMMON,
        price=35,
        size=(1, 1),
        ascii_art=[
            "╱─╲",
            " │ ",
        ],
        comfort_bonus=10,
        mood_bonus=5,
    ),
    "fairy_lights": Decoration(
        id="fairy_lights",
        name="Fairy Lights",
        description="Magical twinkling lights",
        category=DecorationCategory.LIGHTING,
        rarity=DecorationRarity.RARE,
        price=100,
        size=(3, 1),
        ascii_art=[
            "✨~✨~✨~✨",
        ],
        mood_bonus=20,
        beauty_bonus=15,
        special_effect="sparkle_animation",
    ),
    "lantern": Decoration(
        id="lantern",
        name="Paper Lantern",
        description="A soft glowing lantern",
        category=DecorationCategory.LIGHTING,
        rarity=DecorationRarity.UNCOMMON,
        price=45,
        size=(1, 1),
        ascii_art=[
            "╭─╮",
            "│●│",
            "╰─╯",
        ],
        mood_bonus=10,
        beauty_bonus=10,
    ),
    
    # Toys
    "rubber_duck": Decoration(
        id="rubber_duck",
        name="Rubber Ducky Friend",
        description="A squeaky companion",
        category=DecorationCategory.TOY,
        rarity=DecorationRarity.COMMON,
        price=15,
        size=(1, 1),
        ascii_art=[
            "🦆",
        ],
        mood_bonus=10,
        allowed_rooms=[RoomType.PLAY, RoomType.POND],
    ),
    "ball": Decoration(
        id="ball",
        name="Bouncy Ball",
        description="For endless fun!",
        category=DecorationCategory.TOY,
        rarity=DecorationRarity.COMMON,
        price=10,
        size=(1, 1),
        ascii_art=[
            "⚽",
        ],
        mood_bonus=8,
        allowed_rooms=[RoomType.PLAY],
    ),
    "plushie": Decoration(
        id="plushie",
        name="Plush Friend",
        description="A cuddly plush toy",
        category=DecorationCategory.TOY,
        rarity=DecorationRarity.UNCOMMON,
        price=40,
        size=(1, 1),
        ascii_art=[
            "🧸",
        ],
        mood_bonus=15,
        comfort_bonus=10,
        allowed_rooms=[RoomType.BEDROOM, RoomType.PLAY],
    ),
    
    # Floor
    "rug": Decoration(
        id="rug",
        name="Soft Rug",
        description="A comfortable area rug",
        category=DecorationCategory.FLOOR,
        rarity=DecorationRarity.COMMON,
        price=45,
        size=(2, 2),
        ascii_art=[
            "╔════╗",
            "║░░░░║",
            "╚════╝",
        ],
        comfort_bonus=15,
    ),
    "pond_mat": Decoration(
        id="pond_mat",
        name="Pond Mat",
        description="A mat that looks like a pond",
        category=DecorationCategory.FLOOR,
        rarity=DecorationRarity.UNCOMMON,
        price=65,
        size=(2, 2),
        ascii_art=[
            "~~~~~~~~",
            "~🐟~~🐟~",
            "~~~~~~~~",
        ],
        mood_bonus=10,
        beauty_bonus=10,
    ),
    
    # Seasonal
    "spring_wreath": Decoration(
        id="spring_wreath",
        name="Spring Wreath",
        description="A wreath of spring flowers",
        category=DecorationCategory.SEASONAL,
        rarity=DecorationRarity.RARE,
        price=80,
        size=(1, 1),
        ascii_art=[
            "🌸🌷🌸",
        ],
        mood_bonus=15,
        beauty_bonus=20,
        seasonal="spring",
    ),
    "snowglobe": Decoration(
        id="snowglobe",
        name="Snow Globe",
        description="A magical winter snow globe",
        category=DecorationCategory.SEASONAL,
        rarity=DecorationRarity.RARE,
        price=90,
        size=(1, 1),
        ascii_art=[
            "╭──╮",
            "│❄️│",
            "╰──╯",
        ],
        mood_bonus=20,
        beauty_bonus=15,
        seasonal="winter",
        special_effect="snow_particles",
    ),
    
    # Special/Legendary
    "fountain": Decoration(
        id="fountain",
        name="Duck Fountain",
        description="A beautiful fountain with a duck statue",
        category=DecorationCategory.SPECIAL,
        rarity=DecorationRarity.LEGENDARY,
        price=500,
        size=(3, 3),
        ascii_art=[
            "  🦆  ",
            " ╭┴╮ ",
            "╭┴──┴╮",
            "~~~~~~",
        ],
        mood_bonus=30,
        beauty_bonus=40,
        comfort_bonus=20,
        allowed_rooms=[RoomType.GARDEN, RoomType.POND],
        special_effect="water_animation",
    ),
    "golden_nest": Decoration(
        id="golden_nest",
        name="Golden Nest",
        description="The most luxurious nest ever made",
        category=DecorationCategory.SPECIAL,
        rarity=DecorationRarity.LEGENDARY,
        price=1000,
        size=(2, 2),
        ascii_art=[
            " ✨✨ ",
            "╭┤★★├╮",
            "╰────╯",
        ],
        comfort_bonus=50,
        mood_bonus=40,
        beauty_bonus=30,
        allowed_rooms=[RoomType.BEDROOM],
        special_effect="golden_sparkle",
    ),
}


class DecorationsSystem:
    """
    Manages home decorations and room customization.
    """
    
    def __init__(self):
        self.owned_decorations: Dict[str, int] = {}  # decoration_id -> count
        self.rooms: Dict[str, Room] = {
            "bedroom": Room(RoomType.BEDROOM, "Cozy Bedroom", (8, 6)),
            "living": Room(RoomType.LIVING, "Living Room", (10, 8)),
            "garden": Room(RoomType.GARDEN, "Garden", (12, 10)),
            "pond": Room(RoomType.POND, "Duck Pond", (10, 8)),
        }
        self.total_beauty: int = 0
        self.total_comfort: int = 0
        self.favorite_room: Optional[str] = None
        self.themes_unlocked: List[str] = ["default"]
        self.decorating_history: List[Dict] = []
    
    def buy_decoration(self, decoration_id: str, coins: int) -> Tuple[bool, str, int]:
        """Purchase a decoration."""
        decoration = DECORATIONS.get(decoration_id)
        if not decoration:
            return False, "Decoration not found!", coins
        
        if coins < decoration.price:
            return False, f"Not enough coins! Need {decoration.price}.", coins
        
        self.owned_decorations[decoration_id] = self.owned_decorations.get(decoration_id, 0) + 1
        new_coins = coins - decoration.price
        
        return True, f"🛒 Purchased {decoration.name}!", new_coins
    
    def place_decoration(
        self,
        decoration_id: str,
        room_type: str,
        position: Tuple[int, int]
    ) -> Tuple[bool, str]:
        """Place a decoration in a room."""
        decoration = DECORATIONS.get(decoration_id)
        if not decoration:
            return False, "Decoration not found!"
        
        if self.owned_decorations.get(decoration_id, 0) <= 0:
            return False, "You don't own this decoration!"
        
        room = self.rooms.get(room_type)
        if not room:
            return False, "Room not found!"
        
        # Check if decoration can go in this room
        if decoration.allowed_rooms and room.room_type not in decoration.allowed_rooms:
            return False, f"Can't place {decoration.name} in {room.name}!"
        
        # Check if position is valid
        if position[0] < 0 or position[1] < 0:
            return False, "Invalid position!"
        
        if position[0] + decoration.size[0] > room.size[0]:
            return False, "Doesn't fit horizontally!"
        
        if position[1] + decoration.size[1] > room.size[1]:
            return False, "Doesn't fit vertically!"
        
        # Check for overlap with existing decorations
        for placed in room.decorations:
            existing = DECORATIONS.get(placed.decoration_id)
            if not existing:
                continue
            
            # Simple overlap check
            if self._check_overlap(position, decoration.size,
                                    placed.position, existing.size):
                return False, "Space already occupied!"
        
        # Place the decoration
        placed = PlacedDecoration(
            decoration_id=decoration_id,
            room=room.room_type,
            position=position,
            placed_at=datetime.now().isoformat(),
        )
        
        room.decorations.append(placed)
        self.owned_decorations[decoration_id] -= 1
        
        # Update room stats
        room.mood_modifier += decoration.mood_bonus
        room.comfort_level += decoration.comfort_bonus
        self.total_beauty += decoration.beauty_bonus
        self.total_comfort += decoration.comfort_bonus
        
        # Record history
        self.decorating_history.append({
            "action": "place",
            "decoration": decoration_id,
            "room": room_type,
            "position": position,
            "timestamp": datetime.now().isoformat(),
        })

        # Keep history manageable to prevent memory leak
        if len(self.decorating_history) > 100:
            self.decorating_history = self.decorating_history[-100:]

        return True, f"🏠 Placed {decoration.name} in {room.name}!"
    
    def remove_decoration(
        self,
        room_type: str,
        position: Tuple[int, int]
    ) -> Tuple[bool, str]:
        """Remove a decoration from a room."""
        room = self.rooms.get(room_type)
        if not room:
            return False, "Room not found!"
        
        # Find decoration at position
        for i, placed in enumerate(room.decorations):
            if placed.position == position:
                decoration = DECORATIONS.get(placed.decoration_id)
                
                # Remove and return to inventory
                room.decorations.pop(i)
                self.owned_decorations[placed.decoration_id] = \
                    self.owned_decorations.get(placed.decoration_id, 0) + 1
                
                # Update stats
                if decoration:
                    room.mood_modifier -= decoration.mood_bonus
                    room.comfort_level -= decoration.comfort_bonus
                    self.total_beauty -= decoration.beauty_bonus
                    self.total_comfort -= decoration.comfort_bonus
                
                name = decoration.name if decoration else "decoration"
                return True, f"📦 Removed {name} from {room.name}!"
        
        return False, "No decoration at that position!"
    
    def _check_overlap(
        self,
        pos1: Tuple[int, int],
        size1: Tuple[int, int],
        pos2: Tuple[int, int],
        size2: Tuple[int, int]
    ) -> bool:
        """Check if two rectangles overlap."""
        return not (
            pos1[0] + size1[0] <= pos2[0] or
            pos2[0] + size2[0] <= pos1[0] or
            pos1[1] + size1[1] <= pos2[1] or
            pos2[1] + size2[1] <= pos1[1]
        )
    
    def get_room_bonuses(self, room_type: str) -> Dict[str, int]:
        """Get total bonuses from a room's decorations."""
        room = self.rooms.get(room_type)
        if not room:
            return {}
        
        return {
            "mood": room.mood_modifier,
            "comfort": room.comfort_level,
        }
    
    def get_shop_items(self, category: Optional[str] = None) -> List[Decoration]:
        """Get decorations available in the shop."""
        items = list(DECORATIONS.values())
        
        if category:
            try:
                cat = DecorationCategory(category)
                items = [d for d in items if d.category == cat]
            except ValueError:
                pass
        
        return sorted(items, key=lambda x: x.price)
    
    def render_room(self, room_type: str) -> List[str]:
        """Render a room with its decorations."""
        room = self.rooms.get(room_type)
        if not room:
            return ["Room not found!"]
        
        lines = [
            "╔═══════════════════════════════════════════════╗",
            f"║  🏠 {room.name:^37} 🏠  ║",
            "╠═══════════════════════════════════════════════╣",
        ]
        
        # Create room grid
        grid_width = min(room.size[0] * 4, 40)
        grid_height = min(room.size[1], 8)
        
        # Simple room floor
        floor = "░" * grid_width
        for _ in range(grid_height):
            lines.append(f"║  {floor:40}   ║")
        
        lines.append("╠═══════════════════════════════════════════════╣")
        lines.append(f"║  Decorations: {len(room.decorations):3}  |  Mood: +{room.mood_modifier:3}       ║")
        lines.append(f"║  Comfort: +{room.comfort_level:3}                               ║")
        
        # List placed decorations
        if room.decorations:
            lines.append("╠═══════════════════════════════════════════════╣")
            for placed in room.decorations[:3]:
                decoration = DECORATIONS.get(placed.decoration_id)
                if decoration:
                    lines.append(f"║   • {decoration.name:^35}   ║")
        
        lines.append("╚═══════════════════════════════════════════════╝")
        
        return lines
    
    def render_decoration_shop(self) -> List[str]:
        """Render the decoration shop."""
        lines = [
            "╔═══════════════════════════════════════════════╗",
            "║         🛋️ DECORATION SHOP 🛋️                ║",
            "╠═══════════════════════════════════════════════╣",
        ]
        
        categories = list(DecorationCategory)
        for cat in categories[:4]:
            items = [d for d in DECORATIONS.values() if d.category == cat]
            lines.append(f"║  {cat.value.upper():^41}  ║")
            for item in items[:2]:
                owned = self.owned_decorations.get(item.id, 0)
                owned_str = f"[{owned}]" if owned > 0 else ""
                lines.append(f"║    {item.name[:20]:20} {item.price:5}🪙 {owned_str:4} ║")
            lines.append("║                                               ║")
        
        lines.extend([
            "╠═══════════════════════════════════════════════╣",
            f"║  Total Beauty: {self.total_beauty:4}  |  Comfort: {self.total_comfort:4}     ║",
            "╚═══════════════════════════════════════════════╝",
        ])
        
        return lines
    
    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "owned_decorations": self.owned_decorations,
            "rooms": {
                rtype: {
                    "room_type": room.room_type.value,
                    "name": room.name,
                    "size": room.size,
                    "unlocked": room.unlocked,
                    "decorations": [
                        {
                            "decoration_id": d.decoration_id,
                            "room": d.room.value,
                            "position": d.position,
                            "placed_at": d.placed_at,
                            "rotation": d.rotation,
                        }
                        for d in room.decorations
                    ],
                    "theme": room.theme,
                    "mood_modifier": room.mood_modifier,
                    "comfort_level": room.comfort_level,
                }
                for rtype, room in self.rooms.items()
            },
            "total_beauty": self.total_beauty,
            "total_comfort": self.total_comfort,
            "favorite_room": self.favorite_room,
            "themes_unlocked": self.themes_unlocked,
            "decorating_history": self.decorating_history[-50:],  # Keep last 50
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "DecorationsSystem":
        """Create from dictionary."""
        system = cls()
        
        system.owned_decorations = data.get("owned_decorations", {})
        
        for rtype, rdata in data.get("rooms", {}).items():
            room = Room(
                room_type=RoomType(rdata["room_type"]),
                name=rdata["name"],
                size=tuple(rdata["size"]),
                unlocked=rdata.get("unlocked", True),
                decorations=[
                    PlacedDecoration(
                        decoration_id=d["decoration_id"],
                        room=RoomType(d["room"]),
                        position=tuple(d["position"]),
                        placed_at=d["placed_at"],
                        rotation=d.get("rotation", 0),
                    )
                    for d in rdata.get("decorations", [])
                ],
                theme=rdata.get("theme"),
                mood_modifier=rdata.get("mood_modifier", 0),
                comfort_level=rdata.get("comfort_level", 0),
            )
            system.rooms[rtype] = room
        
        system.total_beauty = data.get("total_beauty", 0)
        system.total_comfort = data.get("total_comfort", 0)
        system.favorite_room = data.get("favorite_room")
        system.themes_unlocked = data.get("themes_unlocked", ["default"])
        system.decorating_history = data.get("decorating_history", [])
        
        return system


# Global decorations system instance
decorations_system = DecorationsSystem()
