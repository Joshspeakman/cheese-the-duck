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


# Upgrade paths: Maps structure ID to its upgrade
# When upgrading, the new structure replaces the old one at the same position
UPGRADE_PATHS: Dict[str, str] = {
    # Nest tier upgrades
    "basic_nest": "cozy_nest",
    "cozy_nest": "deluxe_nest",
    # House tier upgrades  
    "mud_hut": "wooden_cottage",
    "wooden_cottage": "stone_house",
}

# Reverse lookup: What structure does this upgrade FROM?
UPGRADE_FROM: Dict[str, str] = {v: k for k, v in UPGRADE_PATHS.items()}

# Material recovery rate when upgrading (50% of old structure materials returned)
UPGRADE_MATERIAL_RECOVERY = 0.5


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
        
        # Structure positions in playfield coordinates (for duck movement)
        self.structure_positions: Dict[str, Tuple[int, int]] = {}
    
    def add_starter_nest(self):
        """Add a pre-built starter nest at the Home Pond."""
        # Check if already has a nest
        for s in self.structures:
            if s.blueprint_id == "starter_nest" or (s.blueprint and s.blueprint.structure_type == StructureType.NEST):
                return  # Already has a nest
        
        # Create a simple starter nest (already complete, no materials needed)
        structure = Structure(
            blueprint_id="basic_nest",
            position=(2, 2),  # Corner of building grid
            status=StructureStatus.COMPLETE,
            current_stage=2,  # Fully built
            stage_progress=1.0,
            durability=50,
        )
        self.structures.append(structure)
        
        # Mark cells as occupied
        bp = structure.blueprint
        if bp:
            x, y = structure.position
            for dx in range(bp.size[0]):
                for dy in range(bp.size[1]):
                    self.occupied_cells.add((x + dx, y + dy))
        
        # Set playfield position for duck to walk to
        # Match the rendering calculation: struct_x = int(pos[0] * 44 / 10), struct_y = int(pos[1] * 14 / 8)
        # With position=(2,2): struct_x = 8, struct_y = 3
        # Nest art is 12 chars wide, 5 lines tall. Interior is around center
        # Duck should be positioned at center of nest interior: x = 20, y = 6
        self.structure_positions["basic_nest"] = (20, 6)  # Playfield coords (centered in nest interior)
    
    def cleanup_duplicate_shelters(self) -> List[str]:
        """Remove duplicate nest/house structures, keeping only the best one.
        Returns list of removed structure names."""
        removed = []
        
        # Find all shelter structures (nests and houses)
        shelters = [s for s in self.structures 
                    if s.blueprint and s.blueprint.structure_type in [StructureType.NEST, StructureType.HOUSE]]
        
        if len(shelters) <= 1:
            return removed  # No duplicates
        
        # Sort by priority: complete > building, then by bonus (higher is better)
        def shelter_priority(s):
            bp = s.blueprint
            is_complete = 1 if s.is_complete() else 0
            bonus = bp.energy_regen_bonus if bp else 0
            return (is_complete, bonus)
        
        shelters.sort(key=shelter_priority, reverse=True)
        
        # Keep the best one, remove the rest
        best = shelters[0]
        for s in shelters[1:]:
            # Free up cells
            bp = s.blueprint
            if bp:
                x, y = s.position
                for dx in range(bp.size[0]):
                    for dy in range(bp.size[1]):
                        self.occupied_cells.discard((x + dx, y + dy))
                removed.append(bp.name)
            self.structures.remove(s)
        
        return removed
    
    def get_structure_position(self, structure_type: str) -> Optional[Tuple[int, int]]:
        """Get the playfield position for a structure type (for duck movement)."""
        # Check specific structure positions first
        if structure_type in self.structure_positions:
            return self.structure_positions[structure_type]
        
        # Default positions based on structure type (calculated from render positions)
        # These are centered in the interior of each structure type
        default_positions = {
            "nest": (20, 6),
            "basic_nest": (20, 6),
            "cozy_nest": (20, 7),
            "shelter": (20, 6),
            "bird_bath": (35, 8),
            "garden_plot": (30, 10),
            "workbench": (38, 6),
        }
        return default_positions.get(structure_type)
    
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
    
    def get_structure_to_upgrade(self, blueprint_id: str) -> Optional[Structure]:
        """Check if this blueprint is an upgrade of an existing structure.
        Returns the structure that would be upgraded, or None."""
        if blueprint_id not in UPGRADE_FROM:
            return None
        
        required_structure_id = UPGRADE_FROM[blueprint_id]
        
        # Find a complete structure of the required type
        for structure in self.structures:
            if structure.blueprint_id == required_structure_id and structure.is_complete():
                return structure
        
        return None
    
    def get_upgrade_info(self, blueprint_id: str, inventory: MaterialInventory) -> Dict:
        """Get info about upgrading to this blueprint.
        Returns dict with 'is_upgrade', 'from_structure', 'reduced_materials', 'recovered_materials'."""
        result = {
            "is_upgrade": False,
            "from_structure": None,
            "reduced_materials": {},
            "recovered_materials": {},
        }
        
        structure_to_upgrade = self.get_structure_to_upgrade(blueprint_id)
        if not structure_to_upgrade:
            return result
        
        result["is_upgrade"] = True
        result["from_structure"] = structure_to_upgrade
        
        old_bp = structure_to_upgrade.blueprint
        new_bp = BLUEPRINTS.get(blueprint_id)
        
        if not old_bp or not new_bp:
            return result
        
        # Calculate materials recovered from old structure (50%)
        for mat_id, amount in old_bp.required_materials.items():
            recovered = int(amount * UPGRADE_MATERIAL_RECOVERY)
            if recovered > 0:
                result["recovered_materials"][mat_id] = recovered
        
        # Calculate reduced material cost (new cost - recovered)
        for mat_id, amount in new_bp.required_materials.items():
            recovered = result["recovered_materials"].get(mat_id, 0)
            reduced = max(0, amount - recovered)
            result["reduced_materials"][mat_id] = reduced
        
        return result
    
    def can_upgrade(self, blueprint_id: str, inventory: MaterialInventory, 
                    player_level: int) -> Tuple[bool, str]:
        """Check if player can upgrade to this blueprint."""
        if blueprint_id not in BLUEPRINTS:
            return False, "Unknown blueprint"
        
        blueprint = BLUEPRINTS[blueprint_id]
        
        # Check level
        if blueprint.unlock_level > player_level:
            return False, f"Unlock at level {blueprint.unlock_level}"
        
        # Check if this is an upgrade
        upgrade_info = self.get_upgrade_info(blueprint_id, inventory)
        if not upgrade_info["is_upgrade"]:
            return False, "Not an upgrade"
        
        # Check reduced materials
        for mat_id, amount in upgrade_info["reduced_materials"].items():
            if amount > 0 and inventory.get_count(mat_id) < amount:
                mat = MATERIALS.get(mat_id)
                mat_name = mat.name if mat else mat_id
                have = inventory.get_count(mat_id)
                return False, f"Need {amount}x {mat_name} (have {have})"
        
        return True, "Ready to upgrade!"
    
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
    
    def has_nest(self) -> bool:
        """Check if player has any nest structure (building or complete)."""
        for s in self.structures:
            if s.blueprint and s.blueprint.structure_type == StructureType.NEST:
                return True
        return False
    
    def has_house(self) -> bool:
        """Check if player has any house structure (building or complete)."""
        for s in self.structures:
            if s.blueprint and s.blueprint.structure_type == StructureType.HOUSE:
                return True
        return False
    
    def start_building(self, blueprint_id: str, inventory: MaterialInventory,
                       position: Tuple[int, int] = None, player_level: int = None) -> Dict:
        """Start building a structure. Handles upgrades automatically."""
        level = player_level if player_level is not None else self._player_level
        
        if self.current_build:
            return {"success": False, "message": "Already building something!"}
        
        blueprint = BLUEPRINTS.get(blueprint_id)
        if not blueprint:
            return {"success": False, "message": "Unknown blueprint"}
        
        # Check if this is an upgrade
        upgrade_info = self.get_upgrade_info(blueprint_id, inventory)
        is_upgrade = upgrade_info["is_upgrade"]
        old_structure = upgrade_info.get("from_structure")
        
        # Prevent building duplicate shelter structures (nests/houses)
        # You can only have ONE nest OR house - upgrade instead of building new
        if blueprint.structure_type in [StructureType.NEST, StructureType.HOUSE]:
            if not is_upgrade:
                # Not an upgrade - check if we already have a shelter
                for s in self.structures:
                    if s.blueprint and s.blueprint.structure_type in [StructureType.NEST, StructureType.HOUSE]:
                        return {
                            "success": False, 
                            "message": f"You already have a {s.blueprint.name}! Upgrade it instead."
                        }
        
        if is_upgrade and old_structure:
            # Use the old structure's position for the upgrade
            pos = old_structure.position
            
            # Check if we can upgrade
            can, reason = self.can_upgrade(blueprint_id, inventory, level)
            if not can:
                return {"success": False, "message": reason}
            
            blueprint = BLUEPRINTS[blueprint_id]
            
            # Remove old structure and free its cells
            old_bp = old_structure.blueprint
            if old_bp:
                old_x, old_y = old_structure.position
                for dx in range(old_bp.size[0]):
                    for dy in range(old_bp.size[1]):
                        self.occupied_cells.discard((old_x + dx, old_y + dy))
            
            self.structures.remove(old_structure)
            
            # Update structure positions dict
            if old_structure.blueprint_id in self.structure_positions:
                # Move the position to the new structure type
                old_pos = self.structure_positions.pop(old_structure.blueprint_id)
                self.structure_positions[blueprint_id] = old_pos
            
            # Consume only the reduced materials
            for mat_id, amount in upgrade_info["reduced_materials"].items():
                if amount > 0:
                    inventory.remove_material(mat_id, amount)
            
            # Create upgraded structure at same position
            structure = Structure(
                blueprint_id=blueprint_id,
                position=pos,
                status=StructureStatus.BUILDING,
                durability=blueprint.max_durability,
            )
            
            # Mark new cells as occupied
            x, y = pos
            for dx in range(blueprint.size[0]):
                for dy in range(blueprint.size[1]):
                    self.occupied_cells.add((x + dx, y + dy))
            
            self.structures.append(structure)
            self.current_build = BuildProgress(structure=structure)
            
            old_name = old_bp.name if old_bp else "structure"
            return {
                "success": True, 
                "message": f"Upgrading {old_name} to {blueprint.name}!",
                "is_upgrade": True
            }
        
        # Standard build (not an upgrade)
        pos = position if position is not None else self._find_free_position(blueprint_id)
        
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
