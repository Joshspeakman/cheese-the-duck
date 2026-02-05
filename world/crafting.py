"""
Crafting system - Combine materials into tools, building materials, and items.
Unlocks new recipes as the duck gains experience.
"""
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from world.materials import MaterialInventory, MATERIALS, MaterialCategory


class CraftingCategory(Enum):
    """Categories of craftable items."""
    TOOL = "tool"           # Hammers, fishing rods, etc.
    BUILDING = "building"   # Planks, bricks, thatch
    DECORATION = "decoration"  # Pretty things for the nest/house
    UTILITY = "utility"     # Rope, containers, etc.
    FOOD = "food"           # Prepared food items
    SPECIAL = "special"     # Rare/magical items


@dataclass
class CraftingRecipe:
    """A recipe for crafting an item."""
    id: str
    name: str
    description: str
    category: CraftingCategory
    ingredients: Dict[str, int]  # material_id -> amount needed
    result_id: str  # What it creates
    result_amount: int = 1
    crafting_time: float = 1.0  # Seconds to craft
    skill_required: int = 1  # Crafting skill level needed
    unlock_level: int = 1  # Player level to unlock
    xp_reward: int = 10  # XP gained for crafting
    
    # Requirements
    requires_tool: Optional[str] = None  # Tool needed to craft
    requires_workbench: bool = False  # Needs a workbench structure
    
    @property
    def result_item(self) -> str:
        """Alias for result_id for compatibility."""
        return self.result_id
    
    def can_craft(self, inventory: MaterialInventory, skill: int, level: int, 
                  has_tool: bool = True, has_workbench: bool = True) -> Tuple[bool, str]:
        """Check if recipe can be crafted."""
        if skill < self.skill_required:
            return False, f"Need crafting skill {self.skill_required} (have {skill})"
        
        if level < self.unlock_level:
            return False, f"Unlock at level {self.unlock_level}"
        
        if self.requires_workbench and not has_workbench:
            return False, "Need a workbench to craft this"
        
        if self.requires_tool and not has_tool:
            return False, f"Need {self.requires_tool} to craft this"
        
        # Check materials
        for mat_id, amount in self.ingredients.items():
            if inventory.get_count(mat_id) < amount:
                mat = MATERIALS.get(mat_id)
                mat_name = mat.name if mat else mat_id
                have = inventory.get_count(mat_id)
                return False, f"Need {amount}x {mat_name} (have {have})"
        
        return True, "Ready to craft!"


# All crafting recipes
RECIPES: Dict[str, CraftingRecipe] = {
    # === BUILDING MATERIALS ===
    "woven_grass": CraftingRecipe(
        id="woven_grass",
        name="Woven Grass Mat",
        description="Weave grass into a useful mat.",
        category=CraftingCategory.BUILDING,
        ingredients={"grass_blade": 10},
        result_id="woven_grass",
        result_amount=1,
        crafting_time=2.0,
        skill_required=1,
        unlock_level=1,
        xp_reward=5,
    ),
    "rope": CraftingRecipe(
        id="rope",
        name="Rope",
        description="Twist fibers into strong rope.",
        category=CraftingCategory.UTILITY,
        ingredients={"reed": 5, "grass_blade": 5},
        result_id="rope",
        result_amount=1,
        crafting_time=3.0,
        skill_required=2,
        unlock_level=2,
        xp_reward=10,
    ),
    "thatch": CraftingRecipe(
        id="thatch",
        name="Thatch Bundle",
        description="Bundle reeds into roofing material.",
        category=CraftingCategory.BUILDING,
        ingredients={"reed": 8, "grass_blade": 4},
        result_id="thatch",
        result_amount=1,
        crafting_time=2.5,
        skill_required=2,
        unlock_level=3,
        xp_reward=10,
    ),
    "clay_brick": CraftingRecipe(
        id="clay_brick",
        name="Clay Brick",
        description="Shape and dry clay into a brick.",
        category=CraftingCategory.BUILDING,
        ingredients={"clay": 3, "sand": 1},
        result_id="clay_brick",
        result_amount=1,
        crafting_time=4.0,
        skill_required=3,
        unlock_level=5,
        xp_reward=15,
    ),
    "wooden_plank": CraftingRecipe(
        id="wooden_plank",
        name="Wooden Plank",
        description="Carve driftwood into a plank.",
        category=CraftingCategory.BUILDING,
        ingredients={"driftwood": 2, "twig": 4},
        result_id="wooden_plank",
        result_amount=1,
        crafting_time=5.0,
        skill_required=3,
        unlock_level=6,
        xp_reward=20,
        requires_tool="stone_hammer",
    ),
    "stone_block": CraftingRecipe(
        id="stone_block",
        name="Stone Block",
        description="Shape rocks into a building block.",
        category=CraftingCategory.BUILDING,
        ingredients={"rock": 4, "pebble": 6},
        result_id="stone_block",
        result_amount=1,
        crafting_time=6.0,
        skill_required=4,
        unlock_level=8,
        xp_reward=25,
        requires_tool="stone_hammer",
    ),
    "insulation": CraftingRecipe(
        id="insulation",
        name="Insulation",
        description="Soft materials for warmth.",
        category=CraftingCategory.BUILDING,
        ingredients={"feather": 5, "moss": 3, "leaf": 8},
        result_id="insulation",
        result_amount=1,
        crafting_time=3.0,
        skill_required=2,
        unlock_level=4,
        xp_reward=10,
    ),
    
    # === TOOLS ===
    "stone_hammer": CraftingRecipe(
        id="stone_hammer",
        name="Stone Hammer",
        description="A basic hammer for building.",
        category=CraftingCategory.TOOL,
        ingredients={"rock": 2, "twig": 3, "reed": 2},
        result_id="stone_hammer",
        result_amount=1,
        crafting_time=4.0,
        skill_required=2,
        unlock_level=3,
        xp_reward=20,
    ),
    "fishing_rod": CraftingRecipe(
        id="fishing_rod",
        name="Fishing Rod",
        description="A simple rod for catching fish.",
        category=CraftingCategory.TOOL,
        ingredients={"twig": 5, "string": 2, "worm": 1},
        result_id="fishing_rod",
        result_amount=1,
        crafting_time=5.0,
        skill_required=3,
        unlock_level=5,
        xp_reward=25,
    ),
    "gathering_bag": CraftingRecipe(
        id="gathering_bag",
        name="Gathering Bag",
        description="Carry more materials!",
        category=CraftingCategory.TOOL,
        ingredients={"fabric_scrap": 3, "string": 2, "leaf": 5},
        result_id="gathering_bag",
        result_amount=1,
        crafting_time=4.0,
        skill_required=2,
        unlock_level=4,
        xp_reward=20,
    ),
    "digging_stick": CraftingRecipe(
        id="digging_stick",
        name="Digging Stick",
        description="For digging up treasures.",
        category=CraftingCategory.TOOL,
        ingredients={"twig": 4, "smooth_stone": 1},
        result_id="digging_stick",
        result_amount=1,
        crafting_time=3.0,
        skill_required=2,
        unlock_level=3,
        xp_reward=15,
    ),
    
    # === DECORATIONS ===
    "flower_wreath": CraftingRecipe(
        id="flower_wreath",
        name="Flower Wreath",
        description="A pretty wreath of flowers.",
        category=CraftingCategory.DECORATION,
        ingredients={"wildflower": 6, "grass_blade": 4},
        result_id="flower_wreath",
        result_amount=1,
        crafting_time=2.0,
        skill_required=1,
        unlock_level=2,
        xp_reward=10,
    ),
    "shell_mobile": CraftingRecipe(
        id="shell_mobile",
        name="Shell Mobile",
        description="Shells that clink in the wind.",
        category=CraftingCategory.DECORATION,
        ingredients={"shell": 5, "string": 1, "twig": 2},
        result_id="shell_mobile",
        result_amount=1,
        crafting_time=3.0,
        skill_required=2,
        unlock_level=4,
        xp_reward=15,
    ),
    "pebble_path": CraftingRecipe(
        id="pebble_path",
        name="Pebble Path",
        description="A decorative path of pebbles.",
        category=CraftingCategory.DECORATION,
        ingredients={"pebble": 10, "sand": 5},
        result_id="pebble_path",
        result_amount=1,
        crafting_time=4.0,
        skill_required=2,
        unlock_level=5,
        xp_reward=15,
    ),
    "moss_carpet": CraftingRecipe(
        id="moss_carpet",
        name="Moss Carpet",
        description="Soft, cozy floor covering.",
        category=CraftingCategory.DECORATION,
        ingredients={"moss": 8, "woven_grass": 2},
        result_id="moss_carpet",
        result_amount=1,
        crafting_time=3.5,
        skill_required=3,
        unlock_level=6,
        xp_reward=20,
    ),
    "crystal_lamp": CraftingRecipe(
        id="crystal_lamp",
        name="Crystal Lamp",
        description="A magical glowing lamp!",
        category=CraftingCategory.DECORATION,
        ingredients={"crystal": 1, "shell": 2, "fairy_dust": 1},
        result_id="crystal_lamp",
        result_amount=1,
        crafting_time=8.0,
        skill_required=5,
        unlock_level=15,
        xp_reward=100,
    ),
    
    # === UTILITY ===
    "storage_basket": CraftingRecipe(
        id="storage_basket",
        name="Storage Basket",
        description="A woven basket for storage.",
        category=CraftingCategory.UTILITY,
        ingredients={"reed": 10, "grass_blade": 6},
        result_id="storage_basket",
        result_amount=1,
        crafting_time=4.0,
        skill_required=2,
        unlock_level=3,
        xp_reward=15,
    ),
    "water_bowl": CraftingRecipe(
        id="water_bowl",
        name="Water Bowl",
        description="A clay bowl for water.",
        category=CraftingCategory.UTILITY,
        ingredients={"clay": 5, "pebble": 2},
        result_id="water_bowl",
        result_amount=1,
        crafting_time=3.5,
        skill_required=2,
        unlock_level=4,
        xp_reward=15,
    ),
    "torch": CraftingRecipe(
        id="torch",
        name="Torch",
        description="Light the way!",
        category=CraftingCategory.UTILITY,
        ingredients={"twig": 3, "bark": 2, "fabric_scrap": 1},
        result_id="torch",
        result_amount=1,
        crafting_time=2.0,
        skill_required=2,
        unlock_level=5,
        xp_reward=10,
    ),
    
    # === FOOD ===
    "berry_salad": CraftingRecipe(
        id="berry_salad",
        name="Berry Salad",
        description="A healthy mix of berries.",
        category=CraftingCategory.FOOD,
        ingredients={"berry": 5, "clover": 2},
        result_id="berry_salad",
        result_amount=1,
        crafting_time=1.0,
        skill_required=1,
        unlock_level=2,
        xp_reward=5,
    ),
    "honey_bread": CraftingRecipe(
        id="honey_bread",
        name="Honey Bread",
        description="Sweet honey on bread crumbs!",
        category=CraftingCategory.FOOD,
        ingredients={"bread_crumb": 5, "honeycomb": 1, "seed": 3},
        result_id="honey_bread",
        result_amount=1,
        crafting_time=3.0,
        skill_required=3,
        unlock_level=7,
        xp_reward=20,
    ),
    
    # === SPECIAL ===
    "lucky_charm": CraftingRecipe(
        id="lucky_charm",
        name="Lucky Charm",
        description="Increases rare find chance!",
        category=CraftingCategory.SPECIAL,
        ingredients={"lucky_clover": 1, "butterfly_wing": 1, "river_pearl": 1},
        result_id="lucky_charm",
        result_amount=1,
        crafting_time=10.0,
        skill_required=5,
        unlock_level=12,
        xp_reward=75,
    ),
    "magic_wand": CraftingRecipe(
        id="magic_wand",
        name="Magic Wand",
        description="Channel magical energy!",
        category=CraftingCategory.SPECIAL,
        ingredients={"magic_acorn": 1, "fairy_dust": 2, "crystal": 1, "eagle_feather": 1},
        result_id="magic_wand",
        result_amount=1,
        crafting_time=15.0,
        skill_required=6,
        unlock_level=20,
        xp_reward=200,
    ),
}


@dataclass
class CraftingProgress:
    """Tracks an in-progress crafting operation."""
    recipe_id: str
    start_time: float
    duration: float
    
    def get_progress(self) -> float:
        """Get progress as 0.0-1.0."""
        elapsed = time.time() - self.start_time
        return min(1.0, elapsed / self.duration)
    
    def is_complete(self) -> bool:
        return self.get_progress() >= 1.0


@dataclass
class Tool:
    """A crafted tool with durability."""
    id: str
    name: str
    durability: int = 100  # Uses remaining
    max_durability: int = 100
    bonus_type: str = ""  # What it helps with
    bonus_amount: float = 0.0


class CraftingSystem:
    """Manages crafting operations and skill progression."""
    
    def __init__(self, building_system=None):
        self.crafting_skill: int = 1
        self.crafting_xp: int = 0
        self.recipes_unlocked: List[str] = []
        self.current_craft: Optional[CraftingProgress] = None
        self.crafted_count: Dict[str, int] = {}  # recipe_id -> times crafted
        self.tools: Dict[str, Tool] = {}  # tool_id -> Tool instance
        self._player_level: int = 1  # Track player level
        self._building_system = building_system  # Reference for workbench check
        
        # Unlock starting recipes
        self._unlock_starting_recipes()
    
    @property
    def _current_craft(self):
        """Alias for current_craft for game.py compatibility."""
        return self.current_craft

    def _unlock_starting_recipes(self):
        """Unlock recipes available from the start."""
        for recipe_id, recipe in RECIPES.items():
            if recipe.unlock_level <= 1 and recipe.skill_required <= 1:
                self.recipes_unlocked.append(recipe_id)
    
    def get_available_recipes(self, inventory: MaterialInventory, player_level: int = None) -> List[str]:
        """Get all recipe IDs that can currently be crafted. Returns result item IDs."""
        level = player_level if player_level is not None else self._player_level
        available = []
        for recipe_id in self.recipes_unlocked:
            recipe = RECIPES.get(recipe_id)
            if recipe:
                can, _ = recipe.can_craft(
                    inventory, 
                    self.crafting_skill, 
                    level,
                    has_tool=self._has_tool(recipe.requires_tool),
                    has_workbench=self._has_workbench(),
                )
                if can:
                    available.append(recipe.result_id)  # Return result_id for matching
        return available
    
    def get_all_known_recipes(self) -> List[CraftingRecipe]:
        """Get all unlocked recipes."""
        return [RECIPES[r] for r in self.recipes_unlocked if r in RECIPES]
    
    def _has_tool(self, tool_id: Optional[str]) -> bool:
        """Check if player has a tool."""
        if not tool_id:
            return True
        return tool_id in self.tools and self.tools[tool_id].durability > 0
    
    def _has_workbench(self) -> bool:
        """Check if player has a workbench structure built."""
        if self._building_system is None:
            return True  # Default to True if no building system linked
        # Check if any workbench-type structure exists
        return self._building_system.has_structure("workbench")
    
    def set_building_system(self, building_system):
        """Link the building system for workbench checks."""
        self._building_system = building_system
    
    def start_crafting(self, recipe_id: str, inventory: MaterialInventory, 
                       player_level: int = None) -> Dict:
        """Start crafting a recipe."""
        level = player_level if player_level is not None else self._player_level
        
        if self.current_craft:
            return {"success": False, "message": "Already crafting something!"}
        
        if recipe_id not in RECIPES:
            return {"success": False, "message": f"Unknown recipe: {recipe_id}"}
        
        recipe = RECIPES[recipe_id]
        
        # Check if unlocked
        if recipe_id not in self.recipes_unlocked:
            return {"success": False, "message": f"Recipe not unlocked yet"}
        
        # Check requirements
        can, reason = recipe.can_craft(
            inventory,
            self.crafting_skill,
            level,
            has_tool=self._has_tool(recipe.requires_tool),
            has_workbench=self._has_workbench(),
        )
        
        if not can:
            return {"success": False, "message": reason}
        
        # Consume materials
        for mat_id, amount in recipe.ingredients.items():
            inventory.remove_material(mat_id, amount)
        
        # Start crafting
        self.current_craft = CraftingProgress(
            recipe_id=recipe_id,
            start_time=time.time(),
            duration=recipe.crafting_time,
        )
        
        # Use tool durability if required
        if recipe.requires_tool and recipe.requires_tool in self.tools:
            self.tools[recipe.requires_tool].durability -= 1
        
        return {"success": True, "message": f"Started crafting {recipe.name}..."}
    
    def check_crafting(self, inventory: MaterialInventory = None) -> Dict:
        """
        Check if current crafting is complete.
        Returns dict with 'completed' bool and other info.
        """
        if not self.current_craft:
            return {"completed": False}
        
        if not self.current_craft.is_complete():
            progress = int(self.current_craft.get_progress() * 100)
            return {"completed": False, "progress": progress, "message": f"Crafting... {progress}%"}
        
        # Complete the craft
        recipe = RECIPES.get(self.current_craft.recipe_id)
        if not recipe:
            self.current_craft = None
            return {"completed": False, "message": "Error: Recipe not found"}
        
        # Track stats
        self.crafted_count[recipe.id] = self.crafted_count.get(recipe.id, 0) + 1
        
        # Award XP
        self.crafting_xp += recipe.xp_reward
        self._check_skill_up()
        
        # Check for new recipe unlocks
        new_unlocks = self._check_recipe_unlocks()
        
        # If it's a tool, add to tools
        if recipe.category == CraftingCategory.TOOL:
            self._add_tool(recipe.result_id, recipe.name)
        
        result_item = recipe.result_id
        quantity = recipe.result_amount
        
        self.current_craft = None
        
        return {
            "completed": True,
            "result_item": result_item,
            "quantity": quantity,
            "xp_gained": recipe.xp_reward,
            "message": f"Crafted {quantity}x {recipe.name}! (+{recipe.xp_reward} XP)",
            "new_unlocks": new_unlocks,
        }
    
    def cancel_crafting(self, inventory: MaterialInventory) -> str:
        """Cancel current crafting, refunding 50% of materials."""
        if not self.current_craft:
            return "Not crafting anything"
        
        recipe = RECIPES.get(self.current_craft.recipe_id)
        if recipe:
            # Refund 50% of materials
            for mat_id, amount in recipe.ingredients.items():
                refund = max(1, amount // 2)
                inventory.add_material(mat_id, refund)
        
        self.current_craft = None
        return "Crafting cancelled. 50% materials refunded."
    
    def _add_tool(self, tool_id: str, name: str):
        """Add a crafted tool to inventory."""
        # Define tool properties
        tool_props = {
            "stone_hammer": ("building", 0.2),
            "fishing_rod": ("fishing", 0.5),
            "gathering_bag": ("gathering", 0.3),
            "digging_stick": ("digging", 0.4),
        }
        
        bonus_type, bonus_amount = tool_props.get(tool_id, ("", 0.0))
        
        self.tools[tool_id] = Tool(
            id=tool_id,
            name=name,
            durability=100,
            max_durability=100,
            bonus_type=bonus_type,
            bonus_amount=bonus_amount,
        )
    
    def _check_skill_up(self):
        """Check if crafting skill should increase."""
        xp_thresholds = [0, 50, 150, 350, 600, 1000, 1500, 2200, 3000, 4000]
        for level, threshold in enumerate(xp_thresholds):
            if self.crafting_xp >= threshold:
                self.crafting_skill = max(self.crafting_skill, level + 1)
    
    def _check_recipe_unlocks(self) -> List[str]:
        """Check for new recipe unlocks based on skill level."""
        new_unlocks = []
        for recipe_id, recipe in RECIPES.items():
            if recipe_id not in self.recipes_unlocked:
                if recipe.skill_required <= self.crafting_skill:
                    self.recipes_unlocked.append(recipe_id)
                    new_unlocks.append(recipe.name)
        return new_unlocks
    
    def get_crafting_status(self) -> str:
        """Get current crafting status."""
        if not self.current_craft:
            return "Not crafting"
        
        recipe = RECIPES.get(self.current_craft.recipe_id)
        if not recipe:
            return "Unknown craft"
        
        progress = int(self.current_craft.get_progress() * 100)
        return f"Crafting {recipe.name}... {progress}%"
    
    def to_dict(self) -> Dict:
        """Serialize for saving."""
        return {
            "skill": self.crafting_skill,
            "xp": self.crafting_xp,
            "unlocked": self.recipes_unlocked,
            "crafted_count": self.crafted_count,
            "tools": {
                tid: {
                    "durability": t.durability,
                    "max_durability": t.max_durability,
                    "name": t.name,
                    "bonus_type": t.bonus_type,
                    "bonus_amount": t.bonus_amount,
                }
                for tid, t in self.tools.items()
            },
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "CraftingSystem":
        """Deserialize from save data."""
        system = cls()
        system.crafting_skill = data.get("skill", 1)
        system.crafting_xp = data.get("xp", 0)
        system.recipes_unlocked = data.get("unlocked", [])
        system.crafted_count = data.get("crafted_count", {})
        
        # Restore tools with all fields
        for tool_id, tool_data in data.get("tools", {}).items():
            system.tools[tool_id] = Tool(
                id=tool_id,
                name=tool_data.get("name", tool_id),
                durability=tool_data.get("durability", 100),
                max_durability=tool_data.get("max_durability", 100),
                bonus_type=tool_data.get("bonus_type", ""),
                bonus_amount=tool_data.get("bonus_amount", 0.0),
            )
        
        # Ensure starting recipes are unlocked
        system._unlock_starting_recipes()
        
        return system


# Global instance
crafting = CraftingSystem()
