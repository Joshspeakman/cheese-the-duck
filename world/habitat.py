"""
Habitat system - manages owned items and their placement in the duck's home.
"""
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import json
from pathlib import Path

from world.shop import ShopItem, get_item, ItemCategory


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
        """Find a random empty spot and place an item."""
        import random
        
        # Try to find an empty spot (avoid edges and center where duck spawns)
        max_attempts = 50
        for _ in range(max_attempts):
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            
            # Avoid the center area where duck typically is
            if 7 <= x <= 12 and 4 <= y <= 8:
                continue
            
            # Check if spot is empty
            if not self.get_item_at(x, y):
                self.place_item(item_id, x, y)
                return
        
        # If all attempts failed, place at first available spot
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if not self.get_item_at(x, y):
                    self.place_item(item_id, x, y)
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
        """Get items near a position."""
        nearby = []
        for item in self.placed_items:
            dx = abs(item.x - x)
            dy = abs(item.y - y)
            if dx <= radius and dy <= radius:
                nearby.append(item)
        return nearby

    def get_placed_items_by_category(self, category: ItemCategory) -> List[PlacedItem]:
        """Get all placed items of a category."""
        result = []
        for placed in self.placed_items:
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
        """Get items near a position (for duck interaction)."""
        nearby = []
        for item in self.placed_items:
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
            "equipped_cosmetics": self.equipped_cosmetics,
            "currency": self.currency
        }
    
    def from_dict(self, data: dict):
        """Load habitat from dictionary."""
        self.owned_items = data.get("owned_items", [])
        self.placed_items = [PlacedItem.from_dict(item) for item in data.get("placed_items", [])]
        self.equipped_cosmetics = data.get("equipped_cosmetics", {})
        self.currency = data.get("currency", 100)
    
    def get_stats(self) -> Dict[str, int]:
        """Get habitat statistics."""
        return {
            "owned_items": len(self.owned_items),
            "placed_items": len(self.placed_items),
            "currency": self.currency,
            "cosmetics_equipped": len(self.equipped_cosmetics)
        }
