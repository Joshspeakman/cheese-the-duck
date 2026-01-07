"""
Habitat system - manages owned items and their placement in the duck's home.
"""
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import json
from pathlib import Path

from world.shop import ShopItem, get_item, ItemCategory


# Fixed positions for items - ensures consistent placement
# Grid is 20x12, organized by category:
# - Toys: left side (x: 2-7)
# - Water features: center-right (x: 10-15)
# - Furniture: right side (x: 15-18)
# - Decorations/Plants: scattered around edges
ITEM_FIXED_POSITIONS: Dict[str, Tuple[int, int]] = {
    # === TOYS (left side) ===
    "toy_ball": (3, 3),
    "toy_blocks": (5, 2),
    "toy_trumpet": (2, 5),
    "toy_skateboard": (4, 7),
    "toy_piano": (6, 4),
    "toy_trampoline": (3, 9),
    "toy_slide": (5, 6),
    "toy_swing": (2, 8),
    "toy_seesaw": (6, 10),
    "toy_sandbox": (4, 10),
    "toy_boombox": (7, 3),
    "toy_car": (3, 6),
    "rubber_duck": (5, 5),
    "frisbee": (2, 2),
    "squeaky_toy": (6, 8),
    "trampoline": (4, 4),

    # === WATER FEATURES (center-right) ===
    "pool_kiddie": (11, 5),
    "pool_large": (12, 7),
    "fountain_small": (10, 3),
    "fountain_grand": (13, 4),
    "sprinkler": (11, 9),
    "hot_tub": (14, 6),
    "birdbath": (10, 8),
    "pond": (12, 2),
    "water_slide": (13, 9),
    "waterfall": (14, 3),
    "fountain_statue": (11, 2),
    "birdbath_garden": (10, 10),
    "fountain_decorative": (13, 2),

    # === FURNITURE (right side) ===
    "chair_wood": (16, 4),
    "chair_throne": (17, 3),
    "table_small": (15, 5),
    "bed_small": (18, 6),
    "bed_king": (17, 8),
    "couch": (16, 7),
    "hammock": (18, 4),
    "bookshelf": (15, 3),
    "lamp": (18, 2),
    "fireplace": (16, 2),
    "piano": (15, 9),

    # === PLANTS (scattered around edges) ===
    "flower_rose": (1, 1),
    "flower_tulip": (19, 1),
    "flower_sunflower": (1, 10),
    "tree_oak": (19, 10),
    "tree_pine": (1, 6),
    "cactus": (19, 6),
    "bamboo": (8, 1),
    "bonsai": (8, 10),

    # === DECORATIONS ===
    "rock_pile": (9, 2),
    "garden_gnome": (9, 9),
    "wind_chime": (8, 5),
    "bird_feeder": (9, 7),
}


@dataclass
class PlacedItem:
    """An item that has been placed in the habitat."""
    item_id: str
    x: int  # Position in habitat grid
    y: int
    last_interaction: float = 0  # Timestamp of last duck interaction
    # Animation state
    anim_offset_x: float = 0.0  # Temporary x offset for animation
    anim_offset_y: float = 0.0  # Temporary y offset for animation
    anim_start: float = 0.0  # When animation started
    is_animating: bool = False

    def to_dict(self) -> dict:
        return {
            "item_id": self.item_id,
            "x": self.x,
            "y": self.y,
            "last_interaction": self.last_interaction
            # Don't save animation state
        }

    @staticmethod
    def from_dict(data: dict) -> "PlacedItem":
        return PlacedItem(
            item_id=data.get("item_id", ""),
            x=data.get("x", 0),
            y=data.get("y", 0),
            last_interaction=data.get("last_interaction", 0)
        )

    def start_animation(self, anim_type: str = "bounce"):
        """Start an interaction animation."""
        import time
        self.is_animating = True
        self.anim_start = time.time()
        # Different animation types
        if anim_type == "bounce":
            self.anim_offset_y = -1  # Jump up
        elif anim_type == "shake":
            self.anim_offset_x = 1  # Shake right first
        elif anim_type == "roll":
            self.anim_offset_x = 2  # Roll to the side

    def update_animation(self) -> bool:
        """Update animation state. Returns True if still animating."""
        import time
        if not self.is_animating:
            return False

        elapsed = time.time() - self.anim_start
        duration = 0.5  # Animation duration in seconds

        if elapsed >= duration:
            # Animation complete
            self.is_animating = False
            self.anim_offset_x = 0.0
            self.anim_offset_y = 0.0
            return False

        # Decay animation offset back to 0
        progress = elapsed / duration
        decay = 1.0 - progress
        self.anim_offset_x *= decay * 0.9
        self.anim_offset_y *= decay * 0.9

        # Add bounce effect
        if abs(self.anim_offset_y) > 0.1:
            import math
            # Bounce effect
            bounce = math.sin(progress * math.pi * 3) * decay
            self.anim_offset_y = bounce * -1

        return True

    def get_display_position(self) -> Tuple[int, int]:
        """Get position with animation offset applied."""
        return (
            self.x + int(round(self.anim_offset_x)),
            self.y + int(round(self.anim_offset_y))
        )


class Habitat:
    """Manages the duck's habitat with owned and placed items."""
    
    def __init__(self):
        self.owned_items: List[str] = []  # Item IDs owned
        self.placed_items: List[PlacedItem] = []  # Items placed in habitat
        self.stored_items: List[str] = []  # Item IDs that are hidden/stored (not visible)
        self.equipped_cosmetics: Dict[str, str] = {}  # slot -> item_id
        self.currency: int = 100  # Starting currency
        
        # Habitat grid size (for placement)
        self.width = 20
        self.height = 12
    
    def add_currency(self, amount: int):
        """Add currency."""
        self.currency += amount
    
    def can_afford(self, cost: int) -> bool:
        """Check if player can afford an item."""
        return self.currency >= cost
    
    def purchase_item(self, item_id: str) -> bool:
        """Purchase an item if affordable."""
        item = get_item(item_id)
        if not item:
            return False
        
        if not self.can_afford(item.cost):
            return False
        
        if item_id in self.owned_items:
            return False  # Already owned
        
        self.currency -= item.cost
        self.owned_items.append(item_id)
        
        # Auto-equip cosmetics
        if item.category == ItemCategory.COSMETIC:
            self.equip_cosmetic(item_id)
        else:
            # Auto-place non-cosmetic items in the habitat
            self._auto_place_item(item_id)
        
        return True
    
    def _auto_place_item(self, item_id: str):
        """Place an item at its designated fixed position, or use deterministic fallback."""
        # First, check for a fixed position
        if item_id in ITEM_FIXED_POSITIONS:
            x, y = ITEM_FIXED_POSITIONS[item_id]
            if not self.get_item_at(x, y):
                self.place_item(item_id, x, y)
                return
            # Fixed position occupied, try nearby positions
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1)]:
                nx, ny = x + dx, y + dy
                if 1 <= nx < self.width - 1 and 1 <= ny < self.height - 1:
                    if not self.get_item_at(nx, ny):
                        self.place_item(item_id, nx, ny)
                        return

        # Fallback: hash-based deterministic placement (same item always tries same spot)
        hash_val = hash(item_id)
        base_x = (abs(hash_val) % 16) + 2  # Range 2-17
        base_y = (abs(hash_val >> 8) % 8) + 2  # Range 2-9

        # Avoid the center area where duck spawns
        if 7 <= base_x <= 12 and 4 <= base_y <= 8:
            base_x = (base_x + 8) % 16 + 2

        # Try the deterministic position first
        if not self.get_item_at(base_x, base_y):
            self.place_item(item_id, base_x, base_y)
            return

        # If occupied, spiral outward from the deterministic position
        for radius in range(1, max(self.width, self.height)):
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    if abs(dx) != radius and abs(dy) != radius:
                        continue  # Only check perimeter
                    nx, ny = base_x + dx, base_y + dy
                    if 1 <= nx < self.width - 1 and 1 <= ny < self.height - 1:
                        # Avoid center duck spawn area
                        if 7 <= nx <= 12 and 4 <= ny <= 8:
                            continue
                        if not self.get_item_at(nx, ny):
                            self.place_item(item_id, nx, ny)
                            return
    
    def owns_item(self, item_id: str) -> bool:
        """Check if player owns an item."""
        return item_id in self.owned_items
    
    def place_item(self, item_id: str, x: int, y: int) -> bool:
        """Place an owned item in the habitat."""
        if not self.owns_item(item_id):
            return False
        
        # Check if position is valid
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        
        # Check if something is already there
        if self.get_item_at(x, y):
            return False
        
        placed = PlacedItem(item_id=item_id, x=x, y=y)
        self.placed_items.append(placed)
        return True
    
    def remove_item_at(self, x: int, y: int) -> bool:
        """Remove an item from a position."""
        item = self.get_item_at(x, y)
        if item:
            self.placed_items.remove(item)
            return True
        return False
    
    def get_item_at(self, x: int, y: int) -> Optional[PlacedItem]:
        """Get the item at a position."""
        for item in self.placed_items:
            if item.x == x and item.y == y:
                return item
        return None

    def update_animations(self):
        """Update all item animations."""
        for item in self.placed_items:
            item.update_animation()

    def animate_item(self, placed_item: PlacedItem, anim_type: str = "bounce"):
        """Start an animation on a placed item."""
        placed_item.start_animation(anim_type)

    def get_items_near(self, x: int, y: int, radius: int = 3) -> List[PlacedItem]:
        """Get visible items near a position (excludes stored items)."""
        nearby = []
        for item in self.placed_items:
            # Skip stored (hidden) items
            if item.item_id in self.stored_items:
                continue
            dx = abs(item.x - x)
            dy = abs(item.y - y)
            if dx <= radius and dy <= radius:
                nearby.append(item)
        return nearby

    def get_placed_items_by_category(self, category: ItemCategory) -> List[PlacedItem]:
        """Get all visible placed items of a category (excludes stored items)."""
        result = []
        for placed in self.placed_items:
            # Skip stored (hidden) items
            if placed.item_id in self.stored_items:
                continue
            item = get_item(placed.item_id)
            if item and item.category == category:
                result.append(placed)
        return result
    
    def equip_cosmetic(self, item_id: str):
        """Equip a cosmetic item."""
        item = get_item(item_id)
        if not item or item.category != ItemCategory.COSMETIC:
            return
        
        # Determine slot based on item name
        slot = self._get_cosmetic_slot(item_id)
        self.equipped_cosmetics[slot] = item_id
    
    def unequip_cosmetic(self, slot: str):
        """Remove a cosmetic from a slot."""
        if slot in self.equipped_cosmetics:
            del self.equipped_cosmetics[slot]
    
    def _get_cosmetic_slot(self, item_id: str) -> str:
        """Determine which slot a cosmetic goes in."""
        # Hats and head items
        head_items = ["hat_", "cap_", "beanie", "crown", "helmet", "wizard", "pirate", "viking", 
                      "party_hat", "flower_crown", "tiara", "graduation", "nurse", "pilot", 
                      "detective", "cat_ears", "bunny_ears", "antenna", "propeller", "jester"]
        for h in head_items:
            if h in item_id:
                return "head"
        
        # Glasses and face items  
        if "glasses_" in item_id or "sunglasses" in item_id or "monocle" in item_id:
            return "eyes"
        
        # Neck accessories
        if "bowtie" in item_id or "bow_tie" in item_id or "scarf_" in item_id or "bandana" in item_id:
            return "neck"
        
        # Back items
        if "cape" in item_id or "wings_" in item_id or "backpack" in item_id:
            return "back"
        
        # Above head (floating)
        if "halo" in item_id or "devil_horns" in item_id or "headphones" in item_id:
            return "above"
        
        return "head"  # Default to head slot
    
    def get_nearby_items(self, x: int, y: int, radius: int = 2) -> List[PlacedItem]:
        """Get visible items near a position for duck interaction (excludes stored items)."""
        nearby = []
        for item in self.placed_items:
            # Skip stored (hidden) items
            if item.item_id in self.stored_items:
                continue
            dx = abs(item.x - x)
            dy = abs(item.y - y)
            if dx <= radius and dy <= radius:
                nearby.append(item)
        return nearby
    
    def mark_interaction(self, placed_item: PlacedItem, timestamp: float):
        """Mark that the duck interacted with an item."""
        placed_item.last_interaction = timestamp
    
    def save(self, filepath: Path):
        """Save habitat data to file."""
        data = {
            "owned_items": self.owned_items,
            "placed_items": [item.to_dict() for item in self.placed_items],
            "equipped_cosmetics": self.equipped_cosmetics,
            "currency": self.currency
        }
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load(self, filepath: Path):
        """Load habitat data from file."""
        if not filepath.exists():
            return
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            self.owned_items = data.get("owned_items", [])
            self.placed_items = [PlacedItem.from_dict(item) for item in data.get("placed_items", [])]
            self.equipped_cosmetics = data.get("equipped_cosmetics", {})
            self.currency = data.get("currency", 100)
        except Exception as e:
            print(f"Error loading habitat: {e}")
    
    def to_dict(self) -> dict:
        """Convert habitat to dictionary for saving."""
        return {
            "owned_items": self.owned_items,
            "placed_items": [item.to_dict() for item in self.placed_items],
            "stored_items": self.stored_items,
            "equipped_cosmetics": self.equipped_cosmetics,
            "currency": self.currency
        }
    
    def from_dict(self, data: dict):
        """Load habitat from dictionary."""
        self.owned_items = data.get("owned_items", [])
        self.placed_items = [PlacedItem.from_dict(item) for item in data.get("placed_items", [])]
        self.stored_items = data.get("stored_items", [])
        self.equipped_cosmetics = data.get("equipped_cosmetics", {})
        self.currency = data.get("currency", 100)
    
    def get_stats(self) -> Dict[str, int]:
        """Get habitat statistics."""
        return {
            "owned_items": len(self.owned_items),
            "placed_items": len(self.placed_items),
            "stored_items": len(self.stored_items),
            "currency": self.currency,
            "cosmetics_equipped": len(self.equipped_cosmetics)
        }
    
    def is_item_stored(self, item_id: str) -> bool:
        """Check if an owned item is currently stored (hidden)."""
        return item_id in self.stored_items
    
    def is_item_placed(self, item_id: str) -> bool:
        """Check if an owned item is currently placed (visible)."""
        return any(p.item_id == item_id for p in self.placed_items)
    
    def toggle_item_visibility(self, item_id: str) -> str:
        """Toggle an owned item between placed and stored states.
        
        Returns:
            'placed' - item is now visible in habitat
            'stored' - item is now hidden
            'not_owned' - item is not owned
            'cosmetic' - cosmetics can't be toggled this way
        """
        if item_id not in self.owned_items:
            return 'not_owned'
        
        # Cosmetics are handled separately via equip/unequip
        item = get_item(item_id)
        if item and item.category == ItemCategory.COSMETIC:
            return 'cosmetic'
        
        if item_id in self.stored_items:
            # Currently stored -> place it
            self.stored_items.remove(item_id)
            self._auto_place_item(item_id)
            return 'placed'
        else:
            # Currently placed -> store it
            # Remove from placed_items
            self.placed_items = [p for p in self.placed_items if p.item_id != item_id]
            self.stored_items.append(item_id)
            return 'stored'
    
    def store_item(self, item_id: str) -> bool:
        """Store (hide) an item from the habitat. Returns True if successful."""
        if item_id not in self.owned_items:
            return False
        
        item = get_item(item_id)
        if item and item.category == ItemCategory.COSMETIC:
            return False
        
        if item_id in self.stored_items:
            return True  # Already stored
        
        # Remove from placed_items
        self.placed_items = [p for p in self.placed_items if p.item_id != item_id]
        self.stored_items.append(item_id)
        return True
    
    def show_item(self, item_id: str) -> bool:
        """Show (place) an item in the habitat. Returns True if successful."""
        if item_id not in self.owned_items:
            return False
        
        item = get_item(item_id)
        if item and item.category == ItemCategory.COSMETIC:
            return False
        
        if item_id in self.stored_items:
            self.stored_items.remove(item_id)
        
        # Only place if not already placed
        if not any(p.item_id == item_id for p in self.placed_items):
            self._auto_place_item(item_id)
        
        return True
    
    def get_visible_placed_items(self) -> List[PlacedItem]:
        """Get only the placed items that are visible (not stored)."""
        return [p for p in self.placed_items if p.item_id not in self.stored_items]
