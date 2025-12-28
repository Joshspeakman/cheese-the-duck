"""
Materials system - Collectible resources and material inventory.
Used for crafting tools and building structures.
"""
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class MaterialCategory(Enum):
    """Categories of materials."""
    PLANT = "plant"         # Leaves, grass, flowers, seeds
    WOOD = "wood"           # Twigs, bark, branches, driftwood
    STONE = "stone"         # Pebbles, rocks, crystals
    EARTH = "earth"         # Clay, sand, mud
    WATER = "water"         # Shells, pearls, seaweed
    FIBER = "fiber"         # String, fabric, reeds
    FOOD = "food"           # Berries, seeds, fish
    RARE = "rare"           # Special/magical items
    CRAFTED = "crafted"     # Items made from other materials


@dataclass
class Material:
    """Definition of a gatherable/craftable material."""
    id: str
    name: str
    description: str
    category: MaterialCategory
    rarity: int = 1  # 1-5, higher = rarer
    stack_size: int = 99  # Max per stack
    value: int = 1  # Base value for trading
    
    # Crafting properties
    strength: int = 1  # For building durability
    warmth: int = 0    # For insulation
    beauty: int = 0    # For decoration
    waterproof: bool = False


# All material definitions
MATERIALS: Dict[str, Material] = {
    # PLANT materials
    "leaf": Material("leaf", "Leaf", "A fallen leaf. Useful for bedding.", MaterialCategory.PLANT, 1, 99, 1, 1, 1, 1),
    "grass_blade": Material("grass_blade", "Grass Blade", "Long blade of grass.", MaterialCategory.PLANT, 1, 99, 1, 1, 1, 0),
    "wildflower": Material("wildflower", "Wildflower", "A pretty flower.", MaterialCategory.PLANT, 1, 50, 2, 0, 0, 3),
    "clover": Material("clover", "Clover", "A lucky clover.", MaterialCategory.PLANT, 1, 99, 1, 1, 0, 1),
    "dandelion": Material("dandelion", "Dandelion", "Fluffy dandelion.", MaterialCategory.PLANT, 1, 99, 1, 0, 0, 1),
    "moss": Material("moss", "Moss", "Soft green moss.", MaterialCategory.PLANT, 2, 50, 3, 2, 3, 2),
    "pine_needle": Material("pine_needle", "Pine Needle", "Fragrant pine needle.", MaterialCategory.PLANT, 1, 99, 1, 1, 1, 1),
    "mushroom": Material("mushroom", "Mushroom", "A forest mushroom.", MaterialCategory.PLANT, 2, 30, 3, 0, 0, 1),
    "pond_weed": Material("pond_weed", "Pond Weed", "Aquatic plant.", MaterialCategory.PLANT, 1, 99, 1, 1, 0, 0),
    "lily_pad": Material("lily_pad", "Lily Pad", "Floating lily pad.", MaterialCategory.PLANT, 2, 30, 3, 1, 0, 2, True),
    "garden_flower": Material("garden_flower", "Garden Flower", "Cultivated flower.", MaterialCategory.PLANT, 2, 50, 4, 0, 0, 4),
    "rainbow_flower": Material("rainbow_flower", "Rainbow Flower", "Magical rainbow-colored flower!", MaterialCategory.RARE, 5, 10, 50, 0, 0, 10),
    
    # WOOD materials
    "twig": Material("twig", "Twig", "A small twig.", MaterialCategory.WOOD, 1, 99, 1, 2, 0, 0),
    "bark": Material("bark", "Bark", "Tree bark.", MaterialCategory.WOOD, 2, 50, 2, 3, 1, 0),
    "acorn": Material("acorn", "Acorn", "A small acorn.", MaterialCategory.WOOD, 1, 99, 2, 1, 0, 0),
    "pine_cone": Material("pine_cone", "Pine Cone", "A pine cone.", MaterialCategory.WOOD, 1, 50, 2, 2, 0, 1),
    "driftwood": Material("driftwood", "Driftwood", "Weathered driftwood.", MaterialCategory.WOOD, 2, 30, 4, 4, 0, 2, True),
    "driftwood_large": Material("driftwood_large", "Large Driftwood", "Big piece of driftwood.", MaterialCategory.WOOD, 3, 10, 10, 6, 0, 3, True),
    
    # STONE materials
    "pebble": Material("pebble", "Pebble", "A small pebble.", MaterialCategory.STONE, 1, 99, 1, 3, 0, 0),
    "smooth_stone": Material("smooth_stone", "Smooth Stone", "Polished by water.", MaterialCategory.STONE, 2, 50, 3, 4, 0, 1),
    "rock": Material("rock", "Rock", "A solid rock.", MaterialCategory.STONE, 2, 30, 4, 5, 0, 0),
    "crystal": Material("crystal", "Crystal", "A sparkling crystal!", MaterialCategory.RARE, 4, 20, 25, 3, 0, 8),
    "iron_ore": Material("iron_ore", "Iron Ore", "Raw iron ore.", MaterialCategory.STONE, 3, 30, 10, 8, 0, 0),
    
    # EARTH materials
    "clay": Material("clay", "Clay", "Moldable clay.", MaterialCategory.EARTH, 1, 50, 2, 2, 0, 0, True),
    "pond_clay": Material("pond_clay", "Pond Clay", "Clay from the pond.", MaterialCategory.EARTH, 1, 50, 2, 2, 0, 0, True),
    "sand": Material("sand", "Sand", "Fine sand.", MaterialCategory.EARTH, 1, 99, 1, 1, 0, 0),
    
    # WATER/SHELL materials
    "shell": Material("shell", "Shell", "A pretty shell.", MaterialCategory.WATER, 1, 50, 2, 2, 0, 2),
    "sea_shell": Material("sea_shell", "Sea Shell", "Ocean shell.", MaterialCategory.WATER, 1, 50, 3, 3, 0, 3),
    "sea_glass": Material("sea_glass", "Sea Glass", "Smooth sea glass.", MaterialCategory.WATER, 2, 30, 5, 2, 0, 5),
    "seaweed": Material("seaweed", "Seaweed", "Ocean seaweed.", MaterialCategory.WATER, 1, 99, 1, 1, 0, 0, True),
    "river_pearl": Material("river_pearl", "River Pearl", "A rare pearl!", MaterialCategory.RARE, 4, 10, 30, 1, 0, 10),
    "sand_dollar": Material("sand_dollar", "Sand Dollar", "Ocean treasure.", MaterialCategory.WATER, 2, 20, 8, 0, 0, 5),
    
    # FIBER materials
    "reed": Material("reed", "Reed", "A sturdy reed.", MaterialCategory.FIBER, 1, 99, 2, 2, 0, 0, True),
    "string": Material("string", "String", "A length of string.", MaterialCategory.FIBER, 2, 50, 4, 1, 0, 0),
    "fabric_scrap": Material("fabric_scrap", "Fabric Scrap", "Piece of fabric.", MaterialCategory.FIBER, 2, 30, 5, 1, 3, 1),
    "feather": Material("feather", "Feather", "A soft feather.", MaterialCategory.FIBER, 2, 50, 3, 0, 2, 2),
    "eagle_feather": Material("eagle_feather", "Eagle Feather", "A majestic eagle feather!", MaterialCategory.RARE, 4, 10, 20, 0, 1, 8),
    
    # FOOD materials
    "berry": Material("berry", "Berry", "A tasty berry.", MaterialCategory.FOOD, 1, 50, 2, 0, 0, 1),
    "seed": Material("seed", "Seed", "A plantable seed.", MaterialCategory.FOOD, 1, 99, 1, 0, 0, 0),
    "vegetable_seed": Material("vegetable_seed", "Vegetable Seed", "Garden vegetable seed.", MaterialCategory.FOOD, 2, 50, 3, 0, 0, 0),
    "worm": Material("worm", "Worm", "A wiggly worm.", MaterialCategory.FOOD, 1, 30, 2, 0, 0, 0),
    "small_fish": Material("small_fish", "Small Fish", "A tiny fish.", MaterialCategory.FOOD, 2, 20, 5, 0, 0, 0),
    "bread_crumb": Material("bread_crumb", "Bread Crumb", "Precious bread!", MaterialCategory.FOOD, 1, 99, 2, 0, 0, 0),
    "honeycomb": Material("honeycomb", "Honeycomb", "Sweet honeycomb.", MaterialCategory.FOOD, 3, 20, 10, 0, 0, 2),
    
    # RARE/SPECIAL materials
    "butterfly_wing": Material("butterfly_wing", "Butterfly Wing", "A delicate wing.", MaterialCategory.RARE, 3, 20, 8, 0, 0, 6),
    "frog_spawn": Material("frog_spawn", "Frog Spawn", "Baby frogs!", MaterialCategory.RARE, 3, 10, 5, 0, 0, 0),
    "fairy_dust": Material("fairy_dust", "Fairy Dust", "Magical sparkling dust!", MaterialCategory.RARE, 5, 10, 100, 0, 0, 10),
    "dragon_scale": Material("dragon_scale", "Dragon Scale", "Is this real?!", MaterialCategory.RARE, 5, 5, 200, 10, 5, 10),
    "mermaid_scale": Material("mermaid_scale", "Mermaid Scale", "Iridescent scale.", MaterialCategory.RARE, 5, 5, 150, 5, 3, 10, True),
    "magic_acorn": Material("magic_acorn", "Magic Acorn", "Glows softly...", MaterialCategory.RARE, 4, 10, 50, 3, 2, 5),
    "lucky_clover": Material("lucky_clover", "Lucky Clover", "Four-leaf clover!", MaterialCategory.RARE, 3, 20, 25, 0, 0, 3),
    "shiny_button": Material("shiny_button", "Shiny Button", "A shiny button.", MaterialCategory.RARE, 2, 30, 5, 0, 0, 3),
    "ancient_coin": Material("ancient_coin", "Ancient Coin", "Very old coin.", MaterialCategory.RARE, 4, 20, 40, 0, 0, 5),
    "message_bottle": Material("message_bottle", "Message in Bottle", "What does it say?", MaterialCategory.RARE, 3, 10, 15, 0, 0, 4),
    "treasure_chest": Material("treasure_chest", "Treasure Chest", "TREASURE!", MaterialCategory.RARE, 5, 1, 500, 5, 0, 10),
    "pirate_map": Material("pirate_map", "Pirate Map", "X marks the spot!", MaterialCategory.RARE, 5, 1, 100, 0, 0, 5),
    "treasure_key": Material("treasure_key", "Treasure Key", "Opens something special...", MaterialCategory.RARE, 5, 1, 75, 0, 0, 3),
    
    # CRAFTED materials (made from other materials)
    "woven_grass": Material("woven_grass", "Woven Grass", "Grass woven into a mat.", MaterialCategory.CRAFTED, 2, 30, 5, 3, 2, 1, True),
    "rope": Material("rope", "Rope", "Strong woven rope.", MaterialCategory.CRAFTED, 2, 30, 8, 4, 0, 0),
    "clay_brick": Material("clay_brick", "Clay Brick", "Hardened clay brick.", MaterialCategory.CRAFTED, 2, 50, 6, 6, 1, 0, True),
    "wooden_plank": Material("wooden_plank", "Wooden Plank", "Carved wooden plank.", MaterialCategory.CRAFTED, 2, 30, 10, 5, 1, 1),
    "stone_block": Material("stone_block", "Stone Block", "Carved stone block.", MaterialCategory.CRAFTED, 3, 20, 15, 8, 0, 1),
    "insulation": Material("insulation", "Insulation", "Keeps warmth in.", MaterialCategory.CRAFTED, 2, 30, 8, 2, 5, 0),
    "thatch": Material("thatch", "Thatch", "Woven roof material.", MaterialCategory.CRAFTED, 2, 30, 7, 4, 2, 1, True),
}


@dataclass
class MaterialStack:
    """A stack of materials in inventory."""
    material_id: str
    quantity: int
    
    @property
    def material(self) -> Optional[Material]:
        return MATERIALS.get(self.material_id)
    
    def can_add(self, amount: int) -> bool:
        mat = self.material
        if not mat:
            return False
        return self.quantity + amount <= mat.stack_size
    
    def add(self, amount: int) -> int:
        """Add to stack, returns overflow."""
        mat = self.material
        if not mat:
            return amount
        
        can_add = mat.stack_size - self.quantity
        actual = min(amount, can_add)
        self.quantity += actual
        return amount - actual
    
    def remove(self, amount: int) -> int:
        """Remove from stack, returns actual removed."""
        actual = min(amount, self.quantity)
        self.quantity -= actual
        return actual


class MaterialInventory:
    """Manages the duck's material inventory."""
    
    def __init__(self, max_slots: int = 50):
        self.max_slots = max_slots
        self.stacks: List[MaterialStack] = []
        self.total_weight: int = 0  # For potential carry limit
    
    def add_material(self, material_id: str, amount: int = 1) -> Tuple[int, str]:
        """
        Add materials to inventory.
        Returns (amount_added, message).
        """
        if material_id not in MATERIALS:
            return 0, f"Unknown material: {material_id}"
        
        material = MATERIALS[material_id]
        remaining = amount
        
        # Try to add to existing stacks first
        for stack in self.stacks:
            if stack.material_id == material_id and stack.can_add(1):
                overflow = stack.add(remaining)
                remaining = overflow
                if remaining == 0:
                    break
        
        # Create new stacks if needed
        while remaining > 0 and len(self.stacks) < self.max_slots:
            new_stack = MaterialStack(material_id, 0)
            overflow = new_stack.add(remaining)
            self.stacks.append(new_stack)
            remaining = overflow
        
        added = amount - remaining
        if added > 0:
            return added, f"Added {added}x {material.name}"
        else:
            return 0, "Inventory full!"
    
    def remove_material(self, material_id: str, amount: int = 1) -> Tuple[int, str]:
        """
        Remove materials from inventory.
        Returns (amount_removed, message).
        """
        if material_id not in MATERIALS:
            return 0, f"Unknown material: {material_id}"
        
        material = MATERIALS[material_id]
        current = self.get_count(material_id)
        
        if current < amount:
            return 0, f"Not enough {material.name} (have {current}, need {amount})"
        
        remaining = amount
        stacks_to_remove = []
        
        for stack in self.stacks:
            if stack.material_id == material_id:
                removed = stack.remove(remaining)
                remaining -= removed
                if stack.quantity == 0:
                    stacks_to_remove.append(stack)
                if remaining == 0:
                    break
        
        # Clean up empty stacks
        for stack in stacks_to_remove:
            self.stacks.remove(stack)
        
        return amount, f"Used {amount}x {material.name}"
    
    def get_count(self, material_id: str) -> int:
        """Get total count of a material."""
        return sum(s.quantity for s in self.stacks if s.material_id == material_id)
    
    def has_materials(self, requirements: Dict[str, int]) -> bool:
        """Check if inventory has all required materials."""
        for mat_id, amount in requirements.items():
            if self.get_count(mat_id) < amount:
                return False
        return True
    
    def get_all_materials(self) -> Dict[str, int]:
        """Get dict of all materials and counts."""
        result = {}
        for stack in self.stacks:
            if stack.material_id in result:
                result[stack.material_id] += stack.quantity
            else:
                result[stack.material_id] = stack.quantity
        return result
    
    def get_by_category(self, category: MaterialCategory) -> Dict[str, int]:
        """Get all materials of a specific category."""
        result = {}
        for mat_id, count in self.get_all_materials().items():
            mat = MATERIALS.get(mat_id)
            if mat and mat.category == category:
                result[mat_id] = count
        return result
    
    def get_slots_used(self) -> int:
        """Get number of inventory slots used."""
        return len(self.stacks)
    
    def get_slots_free(self) -> int:
        """Get number of free inventory slots."""
        return self.max_slots - len(self.stacks)
    
    def get_total_value(self) -> int:
        """Get total value of all materials."""
        total = 0
        for mat_id, count in self.get_all_materials().items():
            mat = MATERIALS.get(mat_id)
            if mat:
                total += mat.value * count
        return total
    
    def get_display_list(self) -> List[Tuple[str, str, int]]:
        """Get formatted list for display: [(id, name, count), ...]"""
        result = []
        for mat_id, count in sorted(self.get_all_materials().items()):
            mat = MATERIALS.get(mat_id)
            if mat:
                result.append((mat_id, mat.name, count))
        return result
    
    def to_dict(self) -> Dict:
        """Serialize for saving."""
        return {
            "max_slots": self.max_slots,
            "materials": self.get_all_materials(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "MaterialInventory":
        """Deserialize from save data."""
        inv = cls(max_slots=data.get("max_slots", 50))
        for mat_id, count in data.get("materials", {}).items():
            inv.add_material(mat_id, count)
        return inv


# Global instance
material_inventory = MaterialInventory()
