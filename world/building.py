"""
Building system - Construct nests, houses, and other structures.
Structures provide bonuses and can be upgraded over time.
"""
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from world.materials import MaterialInventory, MATERIALS


class StructureType(Enum):
    """Types of buildable structures."""
    NEST = "nest"           # Basic shelter
    HOUSE = "house"         # Upgraded shelter
    WORKSHOP = "workshop"   # Crafting bonus
    GARDEN = "garden"       # Grow plants
    POND = "pond"          # Water source
    DECORATION = "decoration"  # Aesthetic only
    STORAGE = "storage"     # Extra inventory
    WATCHTOWER = "watchtower"  # See dangers earlier


class StructureStatus(Enum):
    """Status of a structure."""
    PLANNING = "planning"   # Blueprint placed
    BUILDING = "building"   # Under construction
    COMPLETE = "complete"   # Finished
    DAMAGED = "damaged"     # Needs repair
    DESTROYED = "destroyed" # Must rebuild


@dataclass
class StructureBlueprint:
    """Blueprint for building a structure."""
    id: str
    name: str
    description: str
    structure_type: StructureType
    size: Tuple[int, int]  # Width x Height in grid
    
    # Requirements
    required_materials: Dict[str, int]
    build_time: float  # Seconds to complete each stage
    stages: int = 3    # Number of build stages
    unlock_level: int = 1
    
    # Benefits when complete
    energy_regen_bonus: float = 0.0
    happiness_bonus: int = 0
    storage_slots: int = 0
    crafting_bonus: float = 0.0
    protection: int = 0  # Weather/predator protection
    beauty: int = 0  # Aesthetic value
    
    # Durability
    max_durability: int = 100
    weather_resistance: int = 50  # Resistance to weather damage


# All structure blueprints
BLUEPRINTS: Dict[str, StructureBlueprint] = {
    # === NESTS (Tier 1) ===
    "basic_nest": StructureBlueprint(
        id="basic_nest",
        name="Basic Nest",
        description="A simple nest of grass and twigs. Home sweet home!",
        structure_type=StructureType.NEST,
        size=(2, 2),
        required_materials={
            "twig": 8,
            "grass_blade": 10,
            "leaf": 5,
        },
        build_time=3.0,
        stages=2,
        unlock_level=1,
        energy_regen_bonus=0.1,
        happiness_bonus=5,
        protection=20,
        max_durability=50,
        weather_resistance=30,
    ),
    "cozy_nest": StructureBlueprint(
        id="cozy_nest",
        name="Cozy Nest",
        description="A padded nest with soft moss lining.",
        structure_type=StructureType.NEST,
        size=(3, 2),
        required_materials={
            "twig": 10,
            "grass_blade": 8,
            "moss": 4,
            "feather": 3,
            "woven_grass": 1,
        },
        build_time=5.0,
        stages=3,
        unlock_level=4,
        energy_regen_bonus=0.2,
        happiness_bonus=10,
        protection=35,
        beauty=5,
        max_durability=80,
        weather_resistance=50,
    ),
    "deluxe_nest": StructureBlueprint(
        id="deluxe_nest",
        name="Deluxe Nest",
        description="A luxurious nest fit for royalty!",
        structure_type=StructureType.NEST,
        size=(3, 3),
        required_materials={
            "twig": 15,
            "moss": 6,
            "feather": 5,
            "woven_grass": 2,
            "insulation": 1,
            "shell": 3,
        },
        build_time=10.0,
        stages=4,
        unlock_level=10,
        energy_regen_bonus=0.35,
        happiness_bonus=20,
        protection=60,
        beauty=15,
        max_durability=120,
        weather_resistance=70,
    ),
    
    # === HOUSES (Tier 2) ===
    "mud_hut": StructureBlueprint(
        id="mud_hut",
        name="Mud Hut",
        description="A simple hut with clay walls.",
        structure_type=StructureType.HOUSE,
        size=(3, 3),
        required_materials={
            "clay_brick": 4,
            "twig": 10,
            "thatch": 2,
            "woven_grass": 1,
        },
        build_time=12.0,
        stages=4,
        unlock_level=8,
        energy_regen_bonus=0.3,
        happiness_bonus=15,
        protection=50,
        storage_slots=5,
        max_durability=150,
        weather_resistance=60,
    ),
    "wooden_cottage": StructureBlueprint(
        id="wooden_cottage",
        name="Wooden Cottage",
        description="A charming wooden cottage.",
        structure_type=StructureType.HOUSE,
        size=(4, 3),
        required_materials={
            "wooden_plank": 5,
            "clay_brick": 3,
            "thatch": 3,
            "rope": 2,
            "shell": 2,  # Windows
        },
        build_time=18.0,
        stages=5,
        unlock_level=12,
        energy_regen_bonus=0.4,
        happiness_bonus=25,
        protection=70,
        storage_slots=10,
        beauty=10,
        max_durability=200,
        weather_resistance=80,
    ),
    "stone_house": StructureBlueprint(
        id="stone_house",
        name="Stone House",
        description="A sturdy stone house. Built to last!",
        structure_type=StructureType.HOUSE,
        size=(4, 4),
        required_materials={
            "stone_block": 8,
            "wooden_plank": 3,
            "thatch": 4,
            "rope": 3,
            "insulation": 2,
            "sea_glass": 2,  # Windows
        },
        build_time=25.0,
        stages=6,
        unlock_level=18,
        energy_regen_bonus=0.5,
        happiness_bonus=35,
        protection=90,
        storage_slots=15,
        beauty=15,
        max_durability=300,
        weather_resistance=95,
    ),
    
    # === UTILITY STRUCTURES ===
    "workbench": StructureBlueprint(
        id="workbench",
        name="Workbench",
        description="A crafting station for advanced recipes.",
        structure_type=StructureType.WORKSHOP,
        size=(2, 1),
        required_materials={
            "wooden_plank": 2,
            "stone_block": 1,
            "rope": 1,
        },
        build_time=6.0,
        stages=2,
        unlock_level=6,
        crafting_bonus=0.2,
        max_durability=80,
        weather_resistance=40,
    ),
    "storage_chest": StructureBlueprint(
        id="storage_chest",
        name="Storage Chest",
        description="Extra space for your treasures!",
        structure_type=StructureType.STORAGE,
        size=(1, 1),
        required_materials={
            "wooden_plank": 2,
        },
        build_time=3.0,
        stages=1,
        unlock_level=5,
        storage_slots=20,
        max_durability=60,
        weather_resistance=50,
    ),
    "garden_plot": StructureBlueprint(
        id="garden_plot",
        name="Garden Plot",
        description="Grow your own food and flowers!",
        structure_type=StructureType.GARDEN,
        size=(3, 2),
        required_materials={
            "woven_grass": 2,
            "pebble": 5,
            "sand": 3,
            "seed": 3,
        },
        build_time=5.0,
        stages=2,
        unlock_level=7,
        happiness_bonus=10,
        beauty=10,
        max_durability=40,
        weather_resistance=20,
    ),
    "bird_bath": StructureBlueprint(
        id="bird_bath",
        name="Bird Bath",
        description="A refreshing pool for bathing!",
        structure_type=StructureType.POND,
        size=(2, 2),
        required_materials={
            "stone_block": 2,
            "clay_brick": 2,
            "shell": 2,
        },
        build_time=6.0,
        stages=2,
        unlock_level=9,
        energy_regen_bonus=0.1,
        happiness_bonus=15,
        beauty=12,
        max_durability=100,
        weather_resistance=90,  # Water-proof!
    ),
    "watchtower": StructureBlueprint(
        id="watchtower",
        name="Watchtower",
        description="Spot dangers from afar!",
        structure_type=StructureType.WATCHTOWER,
        size=(2, 3),
        required_materials={
            "wooden_plank": 4,
            "rope": 2,
            "twig": 8,
        },
        build_time=10.0,
        stages=3,
        unlock_level=14,
        protection=10,  # Early warning
        max_durability=90,
        weather_resistance=45,
    ),
    
    # === DECORATIONS ===
    "flower_bed": StructureBlueprint(
        id="flower_bed",
        name="Flower Bed",
        description="A pretty arrangement of flowers.",
        structure_type=StructureType.DECORATION,
        size=(2, 1),
        required_materials={
            "wildflower": 5,
            "garden_flower": 3,
            "pebble": 3,
        },
        build_time=2.0,
        stages=1,
        unlock_level=3,
        happiness_bonus=8,
        beauty=15,
        max_durability=30,
        weather_resistance=25,
    ),
    "stone_path": StructureBlueprint(
        id="stone_path",
        name="Stone Path",
        description="A winding path of smooth stones.",
        structure_type=StructureType.DECORATION,
        size=(4, 1),
        required_materials={
            "smooth_stone": 6,
            "pebble": 10,
            "sand": 4,
        },
        build_time=5.0,
        stages=2,
        unlock_level=6,
        beauty=10,
        max_durability=150,
        weather_resistance=90,
    ),
    "pond_fountain": StructureBlueprint(
        id="pond_fountain",
        name="Pond Fountain",
        description="A beautiful fountain!",
        structure_type=StructureType.DECORATION,
        size=(3, 3),
        required_materials={
            "stone_block": 3,
            "sea_glass": 2,
            "shell": 4,
            "crystal": 1,
        },
        build_time=12.0,
        stages=4,
        unlock_level=16,
        happiness_bonus=25,
        beauty=30,
        max_durability=120,
        weather_resistance=95,
    ),
}


@dataclass
class Structure:
    """An instance of a built structure."""
    blueprint_id: str
    position: Tuple[int, int]  # Grid position
    status: StructureStatus = StructureStatus.PLANNING
    current_stage: int = 0
    stage_progress: float = 0.0  # 0.0-1.0 progress in current stage
    durability: int = 100
    last_update: float = field(default_factory=time.time)
    placed_decorations: List[str] = field(default_factory=list)
    
    @property
    def blueprint(self) -> Optional[StructureBlueprint]:
        return BLUEPRINTS.get(self.blueprint_id)
    
    def is_complete(self) -> bool:
        return self.status == StructureStatus.COMPLETE
    
    def needs_repair(self) -> bool:
        if not self.blueprint:
            return False
        return self.durability < self.blueprint.max_durability * 0.5
    
    def get_build_progress(self) -> float:
        """Get overall build progress 0.0-1.0."""
        if not self.blueprint:
            return 0.0
        
        if self.is_complete():
            return 1.0
        
        stage_value = 1.0 / self.blueprint.stages
        return (self.current_stage * stage_value) + (self.stage_progress * stage_value)
    
    def take_damage(self, amount: int) -> str:
        """Apply damage to structure."""
        self.durability = max(0, self.durability - amount)
        
        if self.durability <= 0:
            self.status = StructureStatus.DESTROYED
            return f"{self.blueprint.name if self.blueprint else 'Structure'} was destroyed!"
        elif self.durability < 30:
            self.status = StructureStatus.DAMAGED
            return f"{self.blueprint.name if self.blueprint else 'Structure'} is badly damaged!"
        elif self.durability < 50:
            self.status = StructureStatus.DAMAGED
            return f"{self.blueprint.name if self.blueprint else 'Structure'} is damaged."
        
        return ""


@dataclass
class BuildProgress:
    """Tracks active building progress."""
    structure: Structure
    workers: int = 1  # Could have helpers later
    start_time: float = field(default_factory=time.time)


class BuildingSystem:
    """Manages structure building and maintenance."""
    
    def __init__(self):
        self.structures: List[Structure] = []
        self.current_build: Optional[BuildProgress] = None
        self.building_skill: int = 1
        self.building_xp: int = 0
        self.structures_built: int = 0
        self.total_beauty: int = 0
        self._player_level: int = 1  # Track player level
        self._default_position: Tuple[int, int] = (5, 5)  # Default build position
        
        # Grid for placement (20x15)
        self.grid_width = 20
        self.grid_height = 15
        self.occupied_cells: set = set()
    
    @property
    def _current_build(self):
        """Alias for current_build for game.py compatibility."""
        return self.current_build
    
    @property
    def _structures(self):
        """Alias for structures for game.py compatibility."""
        return self.structures

    def get_buildable_structures(self, inventory: MaterialInventory, player_level: int = None) -> List[str]:
        """Get blueprint IDs that can currently be built."""
        level = player_level if player_level is not None else self._player_level
        buildable = []
        for bp_id, bp in BLUEPRINTS.items():
            if bp.unlock_level <= level:
                # Check if we have materials
                can_build = True
                for mat_id, amount in bp.required_materials.items():
                    if inventory.get_count(mat_id) < amount:
                        can_build = False
                        break
                if can_build:
                    buildable.append(bp_id)
        return buildable

    def get_available_blueprints(self, player_level: int = None) -> List[StructureBlueprint]:
        """Get blueprints available at current level."""
        level = player_level if player_level is not None else self._player_level
        return [bp for bp in BLUEPRINTS.values() if bp.unlock_level <= level]
    
    def can_build(self, blueprint_id: str, position: Tuple[int, int], 
                  inventory: MaterialInventory, player_level: int) -> Tuple[bool, str]:
        """Check if a structure can be built at a position."""
        if blueprint_id not in BLUEPRINTS:
            return False, "Unknown blueprint"
        
        blueprint = BLUEPRINTS[blueprint_id]
        
        # Check level
        if blueprint.unlock_level > player_level:
            return False, f"Unlock at level {blueprint.unlock_level}"
        
        # Check position bounds
        x, y = position
        if x < 0 or y < 0:
            return False, "Invalid position"
        if x + blueprint.size[0] > self.grid_width:
            return False, "Structure doesn't fit (too wide)"
        if y + blueprint.size[1] > self.grid_height:
            return False, "Structure doesn't fit (too tall)"
        
        # Check for overlapping structures
        for dx in range(blueprint.size[0]):
            for dy in range(blueprint.size[1]):
                cell = (x + dx, y + dy)
                if cell in self.occupied_cells:
                    return False, "Space is already occupied"
        
        # Check materials
        for mat_id, amount in blueprint.required_materials.items():
            if inventory.get_count(mat_id) < amount:
                mat = MATERIALS.get(mat_id)
                mat_name = mat.name if mat else mat_id
                have = inventory.get_count(mat_id)
                return False, f"Need {amount}x {mat_name} (have {have})"
        
        return True, "Ready to build!"
    
    def start_building(self, blueprint_id: str, inventory: MaterialInventory,
                       position: Tuple[int, int] = None, player_level: int = None) -> Dict:
        """Start building a structure."""
        level = player_level if player_level is not None else self._player_level
        pos = position if position is not None else self._find_free_position(blueprint_id)
        
        if self.current_build:
            return {"success": False, "message": "Already building something!"}
        
        can, reason = self.can_build(blueprint_id, pos, inventory, level)
        if not can:
            return {"success": False, "message": reason}
        
        blueprint = BLUEPRINTS[blueprint_id]
        
        # Consume materials
        for mat_id, amount in blueprint.required_materials.items():
            inventory.remove_material(mat_id, amount)
        
        # Create structure
        structure = Structure(
            blueprint_id=blueprint_id,
            position=pos,
            status=StructureStatus.BUILDING,
            durability=blueprint.max_durability,
        )
        
        # Mark cells as occupied
        x, y = pos
        for dx in range(blueprint.size[0]):
            for dy in range(blueprint.size[1]):
                self.occupied_cells.add((x + dx, y + dy))
        
        self.structures.append(structure)
        self.current_build = BuildProgress(structure=structure)
        
        return {"success": True, "message": f"Started building {blueprint.name}!"}
    
    def _find_free_position(self, blueprint_id: str) -> Tuple[int, int]:
        """Find a free position for a structure."""
        bp = BLUEPRINTS.get(blueprint_id)
        if not bp:
            return self._default_position
        
        # Try positions starting from top-left
        for y in range(self.grid_height - bp.size[1] + 1):
            for x in range(self.grid_width - bp.size[0] + 1):
                free = True
                for dx in range(bp.size[0]):
                    for dy in range(bp.size[1]):
                        if (x + dx, y + dy) in self.occupied_cells:
                            free = False
                            break
                    if not free:
                        break
                if free:
                    return (x, y)
        
        return self._default_position
    
    def update_building(self, inventory: MaterialInventory = None, delta_time: float = 1.0) -> Dict:
        """Update current building progress. Returns dict with status info."""
        if not self.current_build:
            return {"in_progress": False}
        
        structure = self.current_build.structure
        blueprint = structure.blueprint
        
        if not blueprint:
            self.current_build = None
            return {"in_progress": False, "message": "Error: Blueprint not found"}
        
        # Calculate progress per second
        progress_per_second = 1.0 / blueprint.build_time
        # Skill bonus
        progress_per_second *= (1.0 + (self.building_skill - 1) * 0.1)
        
        structure.stage_progress += progress_per_second * delta_time
        
        if structure.stage_progress >= 1.0:
            structure.stage_progress = 0.0
            structure.current_stage += 1
            
            if structure.current_stage >= blueprint.stages:
                # Building complete!
                structure.status = StructureStatus.COMPLETE
                structure.current_stage = blueprint.stages
                
                # Update stats
                self.structures_built += 1
                self.total_beauty += blueprint.beauty
                self.building_xp += 20 * blueprint.stages
                self._check_skill_up()
                
                self.current_build = None
                return {
                    "completed": True,
                    "blueprint_id": blueprint.id,
                    "message": f"[=] {blueprint.name} complete! {blueprint.description}"
                }
            else:
                return {
                    "in_progress": True,
                    "stage_completed": True,
                    "current_stage": structure.current_stage,
                    "total_stages": blueprint.stages,
                    "message": f"Stage {structure.current_stage}/{blueprint.stages} complete!"
                }
        
        return {
            "in_progress": True,
            "current_stage": structure.current_stage,
            "progress": structure.stage_progress
        }
    
    def repair_structure(self, structure: Structure, inventory: MaterialInventory) -> Tuple[bool, str]:
        """Repair a damaged structure."""
        if not structure.blueprint:
            return False, "Unknown structure"
        
        if structure.status == StructureStatus.DESTROYED:
            return False, "Structure is destroyed. Must rebuild."
        
        if structure.durability >= structure.blueprint.max_durability:
            return False, "Structure is already in perfect condition"
        
        # Calculate repair cost (25% of build cost per 50 durability)
        repair_amount = min(50, structure.blueprint.max_durability - structure.durability)
        cost_multiplier = repair_amount / 200.0
        
        repair_cost = {}
        for mat_id, amount in structure.blueprint.required_materials.items():
            needed = max(1, int(amount * cost_multiplier))
            repair_cost[mat_id] = needed
        
        # Check materials
        for mat_id, amount in repair_cost.items():
            if inventory.get_count(mat_id) < amount:
                mat = MATERIALS.get(mat_id)
                mat_name = mat.name if mat else mat_id
                return False, f"Need {amount}x {mat_name} for repairs"
        
        # Consume materials
        for mat_id, amount in repair_cost.items():
            inventory.remove_material(mat_id, amount)
        
        # Repair
        structure.durability = min(structure.blueprint.max_durability, 
                                   structure.durability + repair_amount)
        
        if structure.durability >= structure.blueprint.max_durability * 0.5:
            structure.status = StructureStatus.COMPLETE
        
        return True, f"Repaired {structure.blueprint.name}! (+{repair_amount} durability)"
    
    def apply_weather_damage(self, weather_type, intensity: float = 1.0) -> List["Structure"]:
        """Apply weather damage to structures. Returns list of damaged structures."""
        damaged = []
        
        # Handle WeatherType enum or string
        if hasattr(weather_type, 'value'):
            weather_str = weather_type.value
        else:
            weather_str = str(weather_type)
        
        weather_damage = {
            "stormy": 15,
            "rainy": 5,
            "windy": 3,
            "snowy": 8,
        }
        
        base_damage = weather_damage.get(weather_str, 0)
        if base_damage == 0:
            return []
        
        for structure in self.structures:
            if structure.status not in [StructureStatus.COMPLETE, StructureStatus.DAMAGED]:
                continue
            
            blueprint = structure.blueprint
            if not blueprint:
                continue
            
            # Calculate damage after resistance
            resistance = blueprint.weather_resistance / 100.0
            actual_damage = int(base_damage * intensity * (1 - resistance))
            
            if actual_damage > 0:
                structure.take_damage(actual_damage)
                damaged.append(structure)
        
        return damaged
    
    def get_total_bonuses(self) -> Dict[str, float]:
        """Get combined bonuses from all complete structures."""
        bonuses = {
            "energy_regen": 0.0,
            "happiness": 0,
            "storage": 0,
            "crafting": 0.0,
            "protection": 0,
            "beauty": 0,
        }
        
        for structure in self.structures:
            if structure.status != StructureStatus.COMPLETE:
                continue
            
            blueprint = structure.blueprint
            if not blueprint:
                continue
            
            bonuses["energy_regen"] += blueprint.energy_regen_bonus
            bonuses["happiness"] += blueprint.happiness_bonus
            bonuses["storage"] += blueprint.storage_slots
            bonuses["crafting"] += blueprint.crafting_bonus
            bonuses["protection"] += blueprint.protection
            bonuses["beauty"] += blueprint.beauty
        
        return bonuses
    
    def has_workbench(self) -> bool:
        """Check if player has a complete workbench."""
        for structure in self.structures:
            if structure.blueprint_id == "workbench" and structure.is_complete():
                return True
        return False
    
    def get_home(self) -> Optional[Structure]:
        """Get the best nest/house for sleeping."""
        best = None
        best_bonus = 0
        
        for structure in self.structures:
            if structure.status != StructureStatus.COMPLETE:
                continue
            
            blueprint = structure.blueprint
            if not blueprint:
                continue
            
            if blueprint.structure_type in [StructureType.NEST, StructureType.HOUSE]:
                if blueprint.energy_regen_bonus > best_bonus:
                    best = structure
                    best_bonus = blueprint.energy_regen_bonus
        
        return best
    
    def _check_skill_up(self):
        """Check if building skill should increase."""
        xp_thresholds = [0, 40, 120, 280, 500, 800, 1200, 1700, 2400, 3200]
        for level, threshold in enumerate(xp_thresholds):
            if self.building_xp >= threshold:
                self.building_skill = max(self.building_skill, level + 1)
    
    def get_structures_summary(self) -> str:
        """Get a summary of all structures."""
        if not self.structures:
            return "No structures built yet"
        
        lines = []
        for structure in self.structures:
            bp = structure.blueprint
            if not bp:
                continue
            
            status_icon = {
                StructureStatus.PLANNING: "[=]",
                StructureStatus.BUILDING: "#",
                StructureStatus.COMPLETE: "x",
                StructureStatus.DAMAGED: "!",
                StructureStatus.DESTROYED: "*",
            }.get(structure.status, "?")
            
            if structure.status == StructureStatus.BUILDING:
                progress = int(structure.get_build_progress() * 100)
                lines.append(f"{status_icon} {bp.name} ({progress}%)")
            else:
                dur = f" [{structure.durability}/{bp.max_durability}]" if structure.status != StructureStatus.DESTROYED else ""
                lines.append(f"{status_icon} {bp.name}{dur}")
        
        return "\n".join(lines)
    
    def to_dict(self) -> Dict:
        """Serialize for saving."""
        return {
            "skill": self.building_skill,
            "xp": self.building_xp,
            "built_count": self.structures_built,
            "structures": [
                {
                    "blueprint_id": s.blueprint_id,
                    "position": s.position,
                    "status": s.status.value,
                    "stage": s.current_stage,
                    "progress": s.stage_progress,
                    "durability": s.durability,
                }
                for s in self.structures
            ],
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "BuildingSystem":
        """Deserialize from save data."""
        system = cls()
        system.building_skill = data.get("skill", 1)
        system.building_xp = data.get("xp", 0)
        system.structures_built = data.get("built_count", 0)
        
        for s_data in data.get("structures", []):
            structure = Structure(
                blueprint_id=s_data["blueprint_id"],
                position=tuple(s_data["position"]),
                status=StructureStatus(s_data.get("status", "planning")),
                current_stage=s_data.get("stage", 0),
                stage_progress=s_data.get("progress", 0.0),
                durability=s_data.get("durability", 100),
            )
            system.structures.append(structure)
            
            # Mark cells as occupied
            bp = structure.blueprint
            if bp:
                x, y = structure.position
                for dx in range(bp.size[0]):
                    for dy in range(bp.size[1]):
                        system.occupied_cells.add((x + dx, y + dy))
        
        # Recalculate beauty
        system.total_beauty = sum(
            s.blueprint.beauty for s in system.structures 
            if s.is_complete() and s.blueprint
        )
        
        return system


# Global instance
building = BuildingSystem()
