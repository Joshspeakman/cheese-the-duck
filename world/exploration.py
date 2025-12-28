"""
Exploration system - Different areas/biomes the duck can explore.
Each area has unique resources, encounters, and discovery chances.
"""
import random
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class BiomeType(Enum):
    """Different areas the duck can explore."""
    POND = "pond"           # Home base - water, reeds, fish
    FOREST = "forest"       # Trees, twigs, leaves, berries, mushrooms
    MEADOW = "meadow"       # Flowers, grass, seeds, insects
    RIVERSIDE = "riverside" # Pebbles, shells, clay, driftwood
    GARDEN = "garden"       # Vegetables, flowers, string, fabric scraps
    MOUNTAINS = "mountains" # Rocks, crystals, moss, pine needles (unlockable)
    BEACH = "beach"         # Sand, shells, seaweed, glass, treasures (unlockable)


@dataclass
class ResourceNode:
    """A gatherable resource in an area."""
    resource_id: str
    name: str
    quantity: int  # How many can be gathered
    regen_time: float  # Hours until it regenerates
    last_gathered: float = 0  # Timestamp of last gather
    skill_required: int = 0  # Minimum gathering skill needed
    
    def is_available(self) -> bool:
        """Check if resource can be gathered."""
        if self.quantity <= 0:
            # Check if regenerated
            hours_passed = (time.time() - self.last_gathered) / 3600
            return hours_passed >= self.regen_time
        return True
    
    def gather(self, amount: int = 1) -> int:
        """Gather resources. Returns amount actually gathered."""
        if not self.is_available():
            return 0
        
        # Regenerate if needed
        if self.quantity <= 0:
            self.quantity = random.randint(2, 5)
        
        gathered = min(amount, self.quantity)
        self.quantity -= gathered
        if self.quantity <= 0:
            self.last_gathered = time.time()
        return gathered


@dataclass
class BiomeArea:
    """A specific explorable area within a biome."""
    biome: BiomeType
    name: str
    description: str
    resources: List[ResourceNode] = field(default_factory=list)
    discovery_chance: float = 0.1  # Chance to find rare items while exploring
    danger_level: int = 0  # 0-5, affects encounter chances
    unlock_level: int = 1  # Player level required to access
    is_discovered: bool = False
    times_visited: int = 0
    special_events: List[str] = field(default_factory=list)


# Resource definitions by biome
BIOME_RESOURCES = {
    BiomeType.POND: [
        ("reed", "Reed", 5, 2.0, 0),
        ("pond_weed", "Pond Weed", 8, 1.0, 0),
        ("small_fish", "Small Fish", 2, 4.0, 2),
        ("frog_spawn", "Frog Spawn", 1, 24.0, 3),
        ("lily_pad", "Lily Pad", 3, 6.0, 1),
        ("pond_clay", "Pond Clay", 4, 3.0, 1),
    ],
    BiomeType.FOREST: [
        ("twig", "Twig", 10, 1.0, 0),
        ("leaf", "Leaf", 15, 0.5, 0),
        ("bark", "Bark", 6, 2.0, 1),
        ("acorn", "Acorn", 4, 3.0, 0),
        ("mushroom", "Mushroom", 3, 4.0, 1),
        ("berry", "Berry", 5, 2.0, 0),
        ("pine_cone", "Pine Cone", 4, 3.0, 0),
        ("feather", "Feather", 2, 6.0, 0),
        ("moss", "Moss", 6, 2.0, 1),
    ],
    BiomeType.MEADOW: [
        ("grass_blade", "Grass Blade", 20, 0.5, 0),
        ("wildflower", "Wildflower", 8, 2.0, 0),
        ("seed", "Seed", 10, 1.0, 0),
        ("clover", "Clover", 6, 1.5, 0),
        ("dandelion", "Dandelion", 5, 1.0, 0),
        ("butterfly_wing", "Butterfly Wing", 1, 12.0, 3),
        ("honeycomb", "Honeycomb", 1, 24.0, 4),
    ],
    BiomeType.RIVERSIDE: [
        ("pebble", "Pebble", 12, 1.0, 0),
        ("smooth_stone", "Smooth Stone", 6, 2.0, 1),
        ("shell", "Shell", 4, 3.0, 0),
        ("driftwood", "Driftwood", 3, 4.0, 1),
        ("clay", "Clay", 5, 2.0, 1),
        ("sand", "Sand", 15, 0.5, 0),
        ("river_pearl", "River Pearl", 1, 48.0, 5),
    ],
    BiomeType.GARDEN: [
        ("string", "String", 3, 4.0, 0),
        ("fabric_scrap", "Fabric Scrap", 2, 6.0, 0),
        ("vegetable_seed", "Vegetable Seed", 6, 2.0, 0),
        ("garden_flower", "Garden Flower", 5, 2.0, 0),
        ("worm", "Worm", 4, 1.0, 0),
        ("bread_crumb", "Bread Crumb", 8, 1.0, 0),
        ("shiny_button", "Shiny Button", 1, 12.0, 2),
    ],
    BiomeType.MOUNTAINS: [
        ("rock", "Rock", 10, 2.0, 0),
        ("iron_ore", "Iron Ore", 2, 8.0, 4),
        ("crystal", "Crystal", 1, 24.0, 5),
        ("pine_needle", "Pine Needle", 12, 1.0, 0),
        ("mountain_moss", "Mountain Moss", 5, 3.0, 2),
        ("eagle_feather", "Eagle Feather", 1, 48.0, 5),
    ],
    BiomeType.BEACH: [
        ("sea_shell", "Sea Shell", 8, 1.0, 0),
        ("sea_glass", "Sea Glass", 3, 4.0, 1),
        ("seaweed", "Seaweed", 10, 1.0, 0),
        ("driftwood_large", "Large Driftwood", 2, 6.0, 2),
        ("sand_dollar", "Sand Dollar", 2, 12.0, 2),
        ("message_bottle", "Message in Bottle", 1, 72.0, 4),
        ("treasure_chest", "Treasure Chest", 1, 168.0, 6),  # Weekly!
    ],
}


# Area definitions
AREAS = {
    BiomeType.POND: [
        BiomeArea(
            biome=BiomeType.POND,
            name="Home Pond",
            description="Your cozy home pond with reeds and lily pads.",
            discovery_chance=0.05,
            danger_level=0,
            unlock_level=1,
            is_discovered=True,
        ),
        BiomeArea(
            biome=BiomeType.POND,
            name="Deep End",
            description="The mysterious deep part of the pond. What lurks below?",
            discovery_chance=0.15,
            danger_level=1,
            unlock_level=3,
        ),
    ],
    BiomeType.FOREST: [
        BiomeArea(
            biome=BiomeType.FOREST,
            name="Forest Edge",
            description="Where the pond meets the forest. Lots of fallen twigs.",
            discovery_chance=0.10,
            danger_level=1,
            unlock_level=1,
            is_discovered=True,
        ),
        BiomeArea(
            biome=BiomeType.FOREST,
            name="Ancient Oak",
            description="A massive old oak tree. Home to many creatures.",
            discovery_chance=0.20,
            danger_level=2,
            unlock_level=5,
        ),
        BiomeArea(
            biome=BiomeType.FOREST,
            name="Mushroom Grove",
            description="A damp, shady area full of interesting fungi.",
            discovery_chance=0.25,
            danger_level=2,
            unlock_level=7,
        ),
    ],
    BiomeType.MEADOW: [
        BiomeArea(
            biome=BiomeType.MEADOW,
            name="Sunny Meadow",
            description="A bright, flower-filled meadow buzzing with bees.",
            discovery_chance=0.10,
            danger_level=0,
            unlock_level=2,
        ),
        BiomeArea(
            biome=BiomeType.MEADOW,
            name="Butterfly Garden",
            description="Rare butterflies dance among exotic flowers.",
            discovery_chance=0.30,
            danger_level=1,
            unlock_level=8,
        ),
    ],
    BiomeType.RIVERSIDE: [
        BiomeArea(
            biome=BiomeType.RIVERSIDE,
            name="Pebble Beach",
            description="A calm section of river with smooth stones.",
            discovery_chance=0.15,
            danger_level=1,
            unlock_level=3,
        ),
        BiomeArea(
            biome=BiomeType.RIVERSIDE,
            name="Waterfall",
            description="A beautiful waterfall! Treasures wash up here.",
            discovery_chance=0.35,
            danger_level=3,
            unlock_level=10,
        ),
    ],
    BiomeType.GARDEN: [
        BiomeArea(
            biome=BiomeType.GARDEN,
            name="Vegetable Patch",
            description="A human's garden. Full of useful scraps!",
            discovery_chance=0.20,
            danger_level=2,
            unlock_level=4,
        ),
        BiomeArea(
            biome=BiomeType.GARDEN,
            name="Tool Shed",
            description="The humans keep interesting things here...",
            discovery_chance=0.40,
            danger_level=3,
            unlock_level=12,
        ),
    ],
    BiomeType.MOUNTAINS: [
        BiomeArea(
            biome=BiomeType.MOUNTAINS,
            name="Foothills",
            description="The base of the mountains. Rocky and wild.",
            discovery_chance=0.20,
            danger_level=3,
            unlock_level=15,
        ),
        BiomeArea(
            biome=BiomeType.MOUNTAINS,
            name="Crystal Cave",
            description="A hidden cave sparkling with crystals!",
            discovery_chance=0.50,
            danger_level=4,
            unlock_level=20,
        ),
    ],
    BiomeType.BEACH: [
        BiomeArea(
            biome=BiomeType.BEACH,
            name="Sandy Shore",
            description="The ocean! So many shells and treasures.",
            discovery_chance=0.25,
            danger_level=2,
            unlock_level=18,
        ),
        BiomeArea(
            biome=BiomeType.BEACH,
            name="Shipwreck Cove",
            description="An old shipwreck! Who knows what's inside?",
            discovery_chance=0.60,
            danger_level=5,
            unlock_level=25,
        ),
    ],
}


@dataclass
class ExplorationResult:
    """Result of an exploration action."""
    success: bool
    message: str
    resources_found: Dict[str, int] = field(default_factory=dict)
    rare_item: Optional[str] = None
    encounter: Optional[str] = None
    xp_gained: int = 0
    new_area_discovered: Optional[str] = None


class ExplorationSystem:
    """Manages duck exploration and resource gathering."""
    
    def __init__(self):
        self.current_area: Optional[BiomeArea] = None
        self.discovered_areas: Dict[str, BiomeArea] = {}
        self.gathering_skill: int = 1
        self.exploration_xp: int = 0
        self.total_resources_gathered: int = 0
        self.rare_items_found: List[str] = []
        self._last_exploration: float = 0
        self._exploration_cooldown: float = 30  # 30 seconds between explorations
        self._player_level: int = 1  # Track player level for unlocks
        
        # Aliases for compatibility
        self._gathering_skill = self.gathering_skill
        
        # Initialize starting areas
        self._initialize_areas()
    
    @property
    def _current_biome(self):
        """Get current biome type (alias for compatibility)."""
        if self.current_area:
            return self.current_area.biome
        return BiomeType.POND
    
    @property  
    def _biome_danger(self):
        """Get danger levels for discovered biomes."""
        return {area.biome: area.danger_level / 5.0 for area in self.discovered_areas.values()}

    def _initialize_areas(self):
        """Set up initial discovered areas."""
        for biome, areas in AREAS.items():
            for area in areas:
                if area.is_discovered:
                    self.discovered_areas[area.name] = area
                    # Initialize resources for discovered areas
                    self._populate_area_resources(area)
    
    def _populate_area_resources(self, area: BiomeArea):
        """Add resources to an area based on its biome."""
        if area.resources:
            return  # Already populated
        
        resource_defs = BIOME_RESOURCES.get(area.biome, [])
        for res_id, name, qty, regen, skill in resource_defs:
            # Randomize starting quantity
            starting_qty = random.randint(qty // 2, qty)
            area.resources.append(ResourceNode(
                resource_id=res_id,
                name=name,
                quantity=starting_qty,
                regen_time=regen,
                skill_required=skill,
            ))
    
    def get_available_areas(self, player_level: int = None) -> List[BiomeArea]:
        """Get all areas the player can currently access."""
        level = player_level if player_level is not None else self._player_level
        return [
            area for area in self.discovered_areas.values()
            if area.unlock_level <= level
        ]
    
    def get_undiscovered_areas(self, player_level: int) -> List[BiomeArea]:
        """Get areas that could be discovered at current level."""
        undiscovered = []
        for biome, areas in AREAS.items():
            for area in areas:
                if area.name not in self.discovered_areas and area.unlock_level <= player_level:
                    undiscovered.append(area)
        return undiscovered
    
    def travel_to(self, area) -> Dict:
        """Travel to a specific area. Accepts area name (str) or BiomeArea object."""
        # Handle both string names and BiomeArea objects
        if isinstance(area, BiomeArea):
            area_name = area.name
        else:
            area_name = str(area)
        
        if area_name not in self.discovered_areas:
            return {"success": False, "message": f"You haven't discovered {area_name} yet!"}
        
        self.current_area = self.discovered_areas[area_name]
        self.current_area.times_visited += 1
        
        return {"success": True, "message": f"Traveled to {area_name}. {self.current_area.description}"}
    
    def explore(self, duck, player_level: int = None) -> Dict:
        """Explore the current area to find resources and discoveries."""
        current_time = time.time()
        
        # Update player level if provided
        if player_level is not None:
            self._player_level = player_level
        
        # Check cooldown
        if current_time - self._last_exploration < self._exploration_cooldown:
            remaining = int(self._exploration_cooldown - (current_time - self._last_exploration))
            return {
                "success": False,
                "message": f"Still tired from exploring... Wait {remaining}s",
            }
        
        if not self.current_area:
            # Default to home pond
            self.travel_to("Home Pond")
        
        self._last_exploration = current_time
        result = {"success": True, "message": "", "xp_gained": 5, "resources": {}}
        
        area = self.current_area
        messages = []
        
        # Gather some resources automatically
        gatherable = [r for r in area.resources if r.is_available() and r.skill_required <= self.gathering_skill]
        if gatherable:
            # Pick 1-3 random resources
            to_gather = random.sample(gatherable, min(len(gatherable), random.randint(1, 3)))
            for resource in to_gather:
                amount = resource.gather(random.randint(1, 2))
                if amount > 0:
                    result["resources"][resource.resource_id] = amount
                    self.total_resources_gathered += amount
                    messages.append(f"Found {amount}x {resource.name}!")
        
        # Check for rare discovery
        discovery_roll = random.random()
        if discovery_roll < area.discovery_chance:
            rare_items = self._get_rare_items(area.biome)
            if rare_items:
                rare_item = random.choice(rare_items)
                result["rare_discovery"] = rare_item
                self.rare_items_found.append(rare_item)
                result["xp_gained"] += 20
                messages.append(f"✨ RARE FIND: {rare_item}!")
        
        # Check for new area discovery
        if random.random() < 0.1:  # 10% chance per exploration
            undiscovered = self.get_undiscovered_areas(self._player_level)
            if undiscovered:
                new_area = random.choice(undiscovered)
                self._discover_area(new_area)
                result["new_area_discovered"] = new_area.name
                result["xp_gained"] += 50
                messages.append(f"🗺️ Discovered new area: {new_area.name}!")
        
        # Random encounter (danger)
        if area.danger_level > 0 and random.random() < area.danger_level * 0.1:
            encounter = self._generate_encounter(area)
            result["danger"] = {"message": encounter}
            messages.append(encounter)
        
        # Build final message
        if not messages:
            messages.append(f"Explored {area.name} but didn't find much this time.")
        
        result["message"] = " ".join(messages)
        result["biome"] = area.biome.value
        
        # Check for skill up
        old_skill = self.gathering_skill
        self.exploration_xp += result["xp_gained"]
        self._check_skill_up()
        if self.gathering_skill > old_skill:
            result["skill_up"] = True
            self._gathering_skill = self.gathering_skill  # Update alias
        
        return result
    
    def gather(self, resource_id: str, amount: int = 1) -> Tuple[int, str]:
        """Attempt to gather a specific resource from current area."""
        if not self.current_area:
            return 0, "You're not exploring any area!"
        
        for resource in self.current_area.resources:
            if resource.resource_id == resource_id:
                if resource.skill_required > self.gathering_skill:
                    return 0, f"Need gathering skill {resource.skill_required} for {resource.name}!"
                
                if not resource.is_available():
                    hours_left = resource.regen_time - ((time.time() - resource.last_gathered) / 3600)
                    return 0, f"{resource.name} is depleted. Regenerates in {hours_left:.1f}h"
                
                gathered = resource.gather(amount)
                if gathered > 0:
                    self.total_resources_gathered += gathered
                    return gathered, f"Gathered {gathered}x {resource.name}!"
                return 0, f"Couldn't gather any {resource.name}"
        
        return 0, f"No {resource_id} found in this area"
    
    def _discover_area(self, area: BiomeArea):
        """Discover a new area."""
        area.is_discovered = True
        self._populate_area_resources(area)
        self.discovered_areas[area.name] = area
    
    def _get_rare_items(self, biome: BiomeType) -> List[str]:
        """Get possible rare items for a biome."""
        rare_items = {
            BiomeType.POND: ["Golden Scale", "Ancient Coin", "Frog Prince"],
            BiomeType.FOREST: ["Fairy Dust", "Owl Pellet", "Magic Acorn"],
            BiomeType.MEADOW: ["Rainbow Flower", "Bee Crown", "Lucky Clover"],
            BiomeType.RIVERSIDE: ["River Pearl", "Message Bottle", "Fish Bone"],
            BiomeType.GARDEN: ["Garden Gnome", "Lost Ring", "Magic Bean"],
            BiomeType.MOUNTAINS: ["Dragon Scale", "Star Crystal", "Thunder Stone"],
            BiomeType.BEACH: ["Pirate Map", "Mermaid Scale", "Treasure Key"],
        }
        return rare_items.get(biome, [])
    
    def _generate_encounter(self, area: BiomeArea) -> str:
        """Generate a random encounter based on area."""
        encounters = {
            0: [],
            1: [
                "A curious squirrel watches you gather.",
                "A butterfly lands on your head briefly.",
                "You hear rustling in the bushes... just the wind.",
            ],
            2: [
                "A grumpy goose honks at you! Best move on.",
                "A snake slithers by. You freeze until it passes.",
                "A territorial robin dive-bombs you!",
            ],
            3: [
                "A fox eyes you hungrily... but you're too fast!",
                "A hawk circles overhead. Stay near cover!",
                "You stumble into a wasp nest! RUN!",
            ],
            4: [
                "A wild cat stalks you through the undergrowth!",
                "You narrowly avoid a hunter's trap!",
                "Thunder rumbles - a storm is coming!",
            ],
            5: [
                "An eagle swoops down! You barely escape!",
                "You find yourself in predator territory...",
                "The ground shakes - what was that?!",
            ],
        }
        
        level_encounters = encounters.get(min(area.danger_level, 5), [])
        if level_encounters:
            return random.choice(level_encounters)
        return ""
    
    def _check_skill_up(self):
        """Check if gathering skill should increase."""
        xp_thresholds = [0, 50, 150, 300, 500, 800, 1200, 1800, 2500, 3500]
        for level, threshold in enumerate(xp_thresholds):
            if self.exploration_xp >= threshold:
                self.gathering_skill = max(self.gathering_skill, level + 1)
    
    def get_current_area_info(self) -> str:
        """Get info about current area."""
        if not self.current_area:
            return "Not currently exploring"
        
        area = self.current_area
        available = [r for r in area.resources if r.is_available()]
        
        lines = [
            f"📍 {area.name} ({area.biome.value.title()})",
            f"   {area.description}",
            f"   Available resources: {len(available)}/{len(area.resources)}",
            f"   Danger: {'⚠️' * area.danger_level if area.danger_level else 'Safe'}",
            f"   Visited: {area.times_visited} times",
        ]
        return "\n".join(lines)
    
    def to_dict(self) -> Dict:
        """Serialize for saving."""
        return {
            "current_area": self.current_area.name if self.current_area else None,
            "discovered_areas": list(self.discovered_areas.keys()),
            "gathering_skill": self.gathering_skill,
            "exploration_xp": self.exploration_xp,
            "total_gathered": self.total_resources_gathered,
            "rare_items": self.rare_items_found,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "ExplorationSystem":
        """Deserialize from save data."""
        system = cls()
        system.gathering_skill = data.get("gathering_skill", 1)
        system.exploration_xp = data.get("exploration_xp", 0)
        system.total_resources_gathered = data.get("total_gathered", 0)
        system.rare_items_found = data.get("rare_items", [])
        
        # Restore discovered areas
        for area_name in data.get("discovered_areas", []):
            for biome, areas in AREAS.items():
                for area in areas:
                    if area.name == area_name:
                        system._discover_area(area)
        
        # Restore current area
        if data.get("current_area"):
            system.travel_to(data["current_area"])
        
        return system


# Global instance
exploration = ExplorationSystem()
