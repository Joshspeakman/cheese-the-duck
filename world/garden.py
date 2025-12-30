"""
Garden/Planting System - Plant seeds, grow plants, and harvest produce.
Features seasonal plants, growth stages, and special rare plants.
"""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random


class PlantType(Enum):
    """Types of plants."""
    FLOWER = "flower"
    VEGETABLE = "vegetable"
    FRUIT = "fruit"
    HERB = "herb"
    SPECIAL = "special"


class GrowthStage(Enum):
    """Growth stages of plants."""
    SEED = "seed"
    SPROUT = "sprout"
    GROWING = "growing"
    MATURE = "mature"
    FLOWERING = "flowering"
    HARVESTABLE = "harvestable"
    WITHERED = "withered"


@dataclass
class PlantDefinition:
    """Definition of a plant type."""
    id: str
    name: str
    description: str
    plant_type: PlantType
    growth_time_hours: float  # Hours to fully grow
    water_needs: int  # 1-5, how often it needs water
    seasons: List[str]  # Which seasons it can grow in
    harvest_amount: Tuple[int, int]  # Min, max harvest
    harvest_item: str  # What item it produces
    xp_value: int
    coin_value: int
    rarity: str  # common, uncommon, rare, legendary
    ascii_stages: Dict[GrowthStage, List[str]]
    fun_fact: str


@dataclass
class PlantedPlant:
    """A plant that has been planted."""
    plant_id: str
    plot_id: int
    planted_at: str  # ISO datetime
    last_watered: str  # ISO datetime
    growth_stage: GrowthStage = GrowthStage.SEED
    water_level: int = 100  # 0-100
    health: int = 100  # 0-100
    times_watered: int = 0
    is_withered: bool = False


# Plant Database
PLANTS: Dict[str, PlantDefinition] = {
    # Flowers
    "sunflower": PlantDefinition(
        id="sunflower",
        name="Sunflower",
        description="A tall, cheerful flower that follows the sun!",
        plant_type=PlantType.FLOWER,
        growth_time_hours=24.0,
        water_needs=2,
        seasons=["spring", "summer"],
        harvest_amount=(1, 3),
        harvest_item="sunflower_seeds",
        xp_value=15,
        coin_value=10,
        rarity="common",
        ascii_stages={
            GrowthStage.SEED: ["."],
            GrowthStage.SPROUT: ["v"],
            GrowthStage.GROWING: ["|", "v"],
            GrowthStage.MATURE: ["|", "Y"],
            GrowthStage.FLOWERING: ["|", "o"],
            GrowthStage.HARVESTABLE: ["|", "o*"],
        },
        fun_fact="Sunflowers can grow up to 12 feet tall!",
    ),
    "tulip": PlantDefinition(
        id="tulip",
        name="Tulip",
        description="A beautiful spring flower in many colors!",
        plant_type=PlantType.FLOWER,
        growth_time_hours=18.0,
        water_needs=2,
        seasons=["spring"],
        harvest_amount=(1, 2),
        harvest_item="tulip_bulb",
        xp_value=12,
        coin_value=8,
        rarity="common",
        ascii_stages={
            GrowthStage.SEED: ["."],
            GrowthStage.SPROUT: ["|"],
            GrowthStage.GROWING: ["|", "|"],
            GrowthStage.MATURE: ["|", "Y"],
            GrowthStage.FLOWERING: ["|", "T"],
            GrowthStage.HARVESTABLE: ["|", "T*"],
        },
        fun_fact="Tulip bulbs were once more valuable than gold!",
    ),
    "rose": PlantDefinition(
        id="rose",
        name="Rose",
        description="The classic flower of love and beauty.",
        plant_type=PlantType.FLOWER,
        growth_time_hours=36.0,
        water_needs=3,
        seasons=["spring", "summer"],
        harvest_amount=(1, 2),
        harvest_item="rose_petal",
        xp_value=25,
        coin_value=20,
        rarity="uncommon",
        ascii_stages={
            GrowthStage.SEED: ["."],
            GrowthStage.SPROUT: ["+"],
            GrowthStage.GROWING: ["|", "+"],
            GrowthStage.MATURE: ["|", "Y"],
            GrowthStage.FLOWERING: ["|", "@"],
            GrowthStage.HARVESTABLE: ["|", "@*"],
        },
        fun_fact="Roses are related to apples, cherries, and almonds!",
    ),
    
    # Vegetables
    "carrot": PlantDefinition(
        id="carrot",
        name="Carrot",
        description="A crunchy orange root vegetable!",
        plant_type=PlantType.VEGETABLE,
        growth_time_hours=20.0,
        water_needs=2,
        seasons=["spring", "fall"],
        harvest_amount=(2, 5),
        harvest_item="carrot",
        xp_value=10,
        coin_value=6,
        rarity="common",
        ascii_stages={
            GrowthStage.SEED: ["."],
            GrowthStage.SPROUT: ["~"],
            GrowthStage.GROWING: ["~", "~~"],
            GrowthStage.MATURE: ["~~~"],
            GrowthStage.HARVESTABLE: ["|~~"],
        },
        fun_fact="Carrots were originally purple, not orange!",
    ),
    "tomato": PlantDefinition(
        id="tomato",
        name="Tomato",
        description="A juicy red fruit (yes, fruit!) for salads!",
        plant_type=PlantType.VEGETABLE,
        growth_time_hours=30.0,
        water_needs=3,
        seasons=["summer"],
        harvest_amount=(3, 8),
        harvest_item="tomato",
        xp_value=15,
        coin_value=10,
        rarity="common",
        ascii_stages={
            GrowthStage.SEED: ["."],
            GrowthStage.SPROUT: ["v"],
            GrowthStage.GROWING: ["|", "v"],
            GrowthStage.MATURE: ["|", "Y"],
            GrowthStage.FLOWERING: ["|", "*"],
            GrowthStage.HARVESTABLE: ["|", "o"],
        },
        fun_fact="Tomatoes were once thought to be poisonous!",
    ),
    "pumpkin": PlantDefinition(
        id="pumpkin",
        name="Pumpkin",
        description="A big orange squash, perfect for fall!",
        plant_type=PlantType.VEGETABLE,
        growth_time_hours=48.0,
        water_needs=3,
        seasons=["fall"],
        harvest_amount=(1, 3),
        harvest_item="pumpkin",
        xp_value=30,
        coin_value=25,
        rarity="uncommon",
        ascii_stages={
            GrowthStage.SEED: ["."],
            GrowthStage.SPROUT: ["v"],
            GrowthStage.GROWING: ["~~"],
            GrowthStage.MATURE: ["~~o"],
            GrowthStage.HARVESTABLE: ["~O"],
        },
        fun_fact="The largest pumpkin ever weighed over 2,700 pounds!",
    ),
    
    # Fruits
    "strawberry": PlantDefinition(
        id="strawberry",
        name="Strawberry",
        description="Sweet, red, heart-shaped berries!",
        plant_type=PlantType.FRUIT,
        growth_time_hours=24.0,
        water_needs=3,
        seasons=["spring", "summer"],
        harvest_amount=(3, 8),
        harvest_item="strawberry",
        xp_value=12,
        coin_value=8,
        rarity="common",
        ascii_stages={
            GrowthStage.SEED: ["."],
            GrowthStage.SPROUT: ["v"],
            GrowthStage.GROWING: ["vv"],
            GrowthStage.FLOWERING: ["*"],
            GrowthStage.HARVESTABLE: ["oo"],
        },
        fun_fact="Strawberries are the only fruit with seeds on the outside!",
    ),
    "watermelon": PlantDefinition(
        id="watermelon",
        name="Watermelon",
        description="Big, refreshing summer fruit!",
        plant_type=PlantType.FRUIT,
        growth_time_hours=72.0,
        water_needs=4,
        seasons=["summer"],
        harvest_amount=(1, 2),
        harvest_item="watermelon",
        xp_value=40,
        coin_value=35,
        rarity="uncommon",
        ascii_stages={
            GrowthStage.SEED: ["."],
            GrowthStage.SPROUT: ["v"],
            GrowthStage.GROWING: ["~~"],
            GrowthStage.MATURE: ["~~O"],
            GrowthStage.HARVESTABLE: ["~O"],
        },
        fun_fact="Watermelon is 92% water!",
    ),
    
    # Herbs
    "mint": PlantDefinition(
        id="mint",
        name="Mint",
        description="Fresh, aromatic herb that spreads quickly!",
        plant_type=PlantType.HERB,
        growth_time_hours=16.0,
        water_needs=2,
        seasons=["spring", "summer", "fall"],
        harvest_amount=(5, 10),
        harvest_item="mint_leaves",
        xp_value=8,
        coin_value=5,
        rarity="common",
        ascii_stages={
            GrowthStage.SEED: ["."],
            GrowthStage.SPROUT: ["v"],
            GrowthStage.GROWING: ["vv"],
            GrowthStage.HARVESTABLE: ["~~"],
        },
        fun_fact="Mint can help soothe an upset stomach!",
    ),
    
    # Special plants
    "golden_flower": PlantDefinition(
        id="golden_flower",
        name="Golden Flower",
        description="A rare, magical flower that glows at night!",
        plant_type=PlantType.SPECIAL,
        growth_time_hours=96.0,
        water_needs=4,
        seasons=["any"],
        harvest_amount=(1, 1),
        harvest_item="golden_petal",
        xp_value=100,
        coin_value=100,
        rarity="legendary",
        ascii_stages={
            GrowthStage.SEED: ["*"],
            GrowthStage.SPROUT: ["|", "*"],
            GrowthStage.GROWING: ["|", "*"],
            GrowthStage.MATURE: ["|", "*"],
            GrowthStage.FLOWERING: ["|", "*"],
            GrowthStage.HARVESTABLE: ["|", "*"],
        },
        fun_fact="Legend says this flower only blooms once every century!",
    ),
    "crystal_plant": PlantDefinition(
        id="crystal_plant",
        name="Crystal Plant",
        description="A mysterious plant made of pure crystal!",
        plant_type=PlantType.SPECIAL,
        growth_time_hours=120.0,
        water_needs=5,
        seasons=["winter"],
        harvest_amount=(1, 2),
        harvest_item="crystal_shard",
        xp_value=150,
        coin_value=150,
        rarity="legendary",
        ascii_stages={
            GrowthStage.SEED: ["◇"],
            GrowthStage.SPROUT: ["◇", "◇"],
            GrowthStage.GROWING: ["◇", "◆"],
            GrowthStage.MATURE: ["◆", "◆"],
            GrowthStage.HARVESTABLE: ["[D]", "*"],
        },
        fun_fact="Crystal plants only grow in the coldest conditions!",
    ),
}

# Seeds available in the shop
SEEDS = {
    "sunflower_seeds": {"plant": "sunflower", "cost": 5},
    "tulip_seeds": {"plant": "tulip", "cost": 5},
    "rose_seeds": {"plant": "rose", "cost": 15},
    "carrot_seeds": {"plant": "carrot", "cost": 3},
    "tomato_seeds": {"plant": "tomato", "cost": 5},
    "pumpkin_seeds": {"plant": "pumpkin", "cost": 10},
    "strawberry_seeds": {"plant": "strawberry", "cost": 8},
    "watermelon_seeds": {"plant": "watermelon", "cost": 15},
    "mint_seeds": {"plant": "mint", "cost": 4},
    "golden_seeds": {"plant": "golden_flower", "cost": 200},
    "crystal_seeds": {"plant": "crystal_plant", "cost": 250},
}


@dataclass
class GardenPlot:
    """A single plot in the garden."""
    plot_id: int
    plant: Optional[PlantedPlant] = None
    is_unlocked: bool = True
    soil_quality: int = 100  # Affects growth speed
    decorations: List[str] = field(default_factory=list)


class Garden:
    """
    Garden system for planting and growing.
    """
    
    def __init__(self):
        self.plots: Dict[int, GardenPlot] = {}
        self.max_plots: int = 4
        self.unlocked_plots: int = 2
        self.seed_inventory: Dict[str, int] = {
            "sunflower_seeds": 3,
            "carrot_seeds": 3,
        }
        self.harvest_inventory: Dict[str, int] = {}
        self.total_harvests: int = 0
        self.plants_grown: Dict[str, int] = {}  # Track how many of each plant grown
        
        # Initialize plots
        for i in range(self.max_plots):
            self.plots[i] = GardenPlot(
                plot_id=i,
                is_unlocked=i < self.unlocked_plots,
            )
    
    def get_current_season(self) -> str:
        """Get current season based on date."""
        month = datetime.now().month
        if month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        elif month in [9, 10, 11]:
            return "fall"
        else:
            return "winter"
    
    def plant_seed(self, plot_id: int, seed_id: str) -> Tuple[bool, str]:
        """Plant a seed in a plot."""
        if plot_id not in self.plots:
            return False, "Invalid plot!"
        
        plot = self.plots[plot_id]
        if not plot.is_unlocked:
            return False, "This plot is locked!"
        
        if plot.plant is not None:
            return False, "This plot already has a plant!"
        
        if seed_id not in self.seed_inventory or self.seed_inventory[seed_id] <= 0:
            return False, f"You don't have any {seed_id}!"
        
        seed_info = SEEDS.get(seed_id)
        if not seed_info:
            return False, "Invalid seed!"
        
        plant_def = PLANTS.get(seed_info["plant"])
        if not plant_def:
            return False, "Unknown plant!"
        
        # Check season
        season = self.get_current_season()
        if "any" not in plant_def.seasons and season not in plant_def.seasons:
            return False, f"{plant_def.name} doesn't grow in {season}!"
        
        # Plant the seed
        self.seed_inventory[seed_id] -= 1
        now = datetime.now().isoformat()
        
        plot.plant = PlantedPlant(
            plant_id=plant_def.id,
            plot_id=plot_id,
            planted_at=now,
            last_watered=now,
            growth_stage=GrowthStage.SEED,
        )
        
        return True, f"Planted {plant_def.name}! i"
    
    def water_plant(self, plot_id: int) -> Tuple[bool, str]:
        """Water a plant."""
        if plot_id not in self.plots:
            return False, "Invalid plot!"
        
        plot = self.plots[plot_id]
        if plot.plant is None:
            return False, "No plant to water!"
        
        plant = plot.plant
        if plant.is_withered:
            return False, "This plant has withered... :("
        
        plant.water_level = min(100, plant.water_level + 50)
        plant.last_watered = datetime.now().isoformat()
        plant.times_watered += 1
        
        return True, "Watered the plant! ~"
    
    def update_plants(self, delta_hours: float):
        """Update all plants based on time passed."""
        for plot in self.plots.values():
            if plot.plant is None:
                continue
            
            plant = plot.plant
            plant_def = PLANTS.get(plant.plant_id)
            if not plant_def:
                continue
            
            # Decrease water level
            water_decrease = plant_def.water_needs * delta_hours * 5
            plant.water_level = max(0, plant.water_level - water_decrease)
            
            # Check for withering
            if plant.water_level <= 0:
                plant.health -= delta_hours * 10
                if plant.health <= 0:
                    plant.is_withered = True
                    plant.growth_stage = GrowthStage.WITHERED
            else:
                plant.health = min(100, plant.health + delta_hours * 2)
            
            # Growth progress
            if not plant.is_withered and plant.water_level > 20:
                planted_time = datetime.fromisoformat(plant.planted_at)
                hours_since_planting = (datetime.now() - planted_time).total_seconds() / 3600
                growth_percent = hours_since_planting / plant_def.growth_time_hours
                
                # Determine growth stage
                if growth_percent >= 1.0:
                    plant.growth_stage = GrowthStage.HARVESTABLE
                elif growth_percent >= 0.8:
                    plant.growth_stage = GrowthStage.FLOWERING if PlantType.FLOWER == plant_def.plant_type else GrowthStage.MATURE
                elif growth_percent >= 0.5:
                    plant.growth_stage = GrowthStage.MATURE
                elif growth_percent >= 0.3:
                    plant.growth_stage = GrowthStage.GROWING
                elif growth_percent >= 0.1:
                    plant.growth_stage = GrowthStage.SPROUT
    
    def harvest_plant(self, plot_id: int) -> Tuple[bool, str, Dict[str, int]]:
        """Harvest a mature plant."""
        if plot_id not in self.plots:
            return False, "Invalid plot!", {}
        
        plot = self.plots[plot_id]
        if plot.plant is None:
            return False, "No plant to harvest!", {}
        
        plant = plot.plant
        if plant.growth_stage != GrowthStage.HARVESTABLE:
            return False, "Plant is not ready to harvest!", {}
        
        plant_def = PLANTS.get(plant.plant_id)
        if not plant_def:
            return False, "Unknown plant!", {}
        
        # Calculate harvest amount
        min_amt, max_amt = plant_def.harvest_amount
        amount = random.randint(min_amt, max_amt)
        
        # Bonus for well-watered plants
        if plant.times_watered >= plant_def.water_needs * 2:
            amount += 1
        
        harvest_item = plant_def.harvest_item
        self.harvest_inventory[harvest_item] = self.harvest_inventory.get(harvest_item, 0) + amount
        self.total_harvests += 1
        self.plants_grown[plant.plant_id] = self.plants_grown.get(plant.plant_id, 0) + 1
        
        # Clear the plot
        plot.plant = None
        
        return True, f"Harvested {amount} {plant_def.name}! W", {
            "item": harvest_item,
            "amount": amount,
            "xp": plant_def.xp_value,
            "coins": plant_def.coin_value * amount,
        }
    
    def remove_plant(self, plot_id: int) -> Tuple[bool, str]:
        """Remove a plant (including withered ones)."""
        if plot_id not in self.plots:
            return False, "Invalid plot!"
        
        plot = self.plots[plot_id]
        if plot.plant is None:
            return False, "No plant to remove!"
        
        plot.plant = None
        return True, "Removed the plant."
    
    def unlock_plot(self, plot_id: int) -> Tuple[bool, str]:
        """Unlock a new garden plot."""
        if plot_id not in self.plots:
            return False, "Invalid plot!"
        
        plot = self.plots[plot_id]
        if plot.is_unlocked:
            return False, "Plot already unlocked!"
        
        plot.is_unlocked = True
        self.unlocked_plots += 1
        return True, "Unlocked new garden plot! i"
    
    def add_seeds(self, seed_id: str, amount: int):
        """Add seeds to inventory."""
        self.seed_inventory[seed_id] = self.seed_inventory.get(seed_id, 0) + amount
    
    def render_garden(self) -> List[str]:
        """Render the garden display."""
        lines = [
            "+=======================================+",
            "|         o YOUR GARDEN o              |",
            f"|  Season: {self.get_current_season().capitalize():12}              |",
            "+=======================================+",
        ]
        
        for plot_id, plot in self.plots.items():
            if not plot.is_unlocked:
                lines.append(f"| Plot {plot_id + 1}: [LOCKED] X              |")
                continue
            
            if plot.plant is None:
                lines.append(f"| Plot {plot_id + 1}: [Empty] - Ready to plant  |")
            else:
                plant = plot.plant
                plant_def = PLANTS.get(plant.plant_id)
                if plant_def:
                    stage = plant.growth_stage.value
                    water = "~" * (plant.water_level // 25) if plant.water_level > 0 else "X"
                    art = plant_def.ascii_stages.get(plant.growth_stage, ["?"])[-1]
                    lines.append(f"| Plot {plot_id + 1}: {art} {plant_def.name[:10]:10} {water:4} |")
                    lines.append(f"|         Stage: {stage:15}       |")
        
        lines.append("+=======================================+")
        lines.append("| [P]lant [W]ater [H]arvest [R]emove    |")
        lines.append("+=======================================+")
        
        return lines
    
    def get_garden_stats(self) -> Dict:
        """Get garden statistics."""
        return {
            "total_harvests": self.total_harvests,
            "plants_grown": self.plants_grown,
            "unlocked_plots": self.unlocked_plots,
            "active_plants": sum(1 for p in self.plots.values() if p.plant is not None),
        }
    
    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "plots": {
                str(pid): {
                    "plot_id": p.plot_id,
                    "is_unlocked": p.is_unlocked,
                    "soil_quality": p.soil_quality,
                    "plant": {
                        "plant_id": p.plant.plant_id,
                        "plot_id": p.plant.plot_id,
                        "planted_at": p.plant.planted_at,
                        "last_watered": p.plant.last_watered,
                        "growth_stage": p.plant.growth_stage.value,
                        "water_level": p.plant.water_level,
                        "health": p.plant.health,
                        "times_watered": p.plant.times_watered,
                        "is_withered": p.plant.is_withered,
                    } if p.plant else None,
                }
                for pid, p in self.plots.items()
            },
            "seed_inventory": self.seed_inventory,
            "harvest_inventory": self.harvest_inventory,
            "total_harvests": self.total_harvests,
            "plants_grown": self.plants_grown,
            "unlocked_plots": self.unlocked_plots,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Garden":
        """Create from dictionary."""
        garden = cls()
        
        for pid_str, pdata in data.get("plots", {}).items():
            pid = int(pid_str)
            if pid in garden.plots:
                plot = garden.plots[pid]
                plot.is_unlocked = pdata.get("is_unlocked", False)
                plot.soil_quality = pdata.get("soil_quality", 100)
                
                if pdata.get("plant"):
                    plant_data = pdata["plant"]
                    plot.plant = PlantedPlant(
                        plant_id=plant_data["plant_id"],
                        plot_id=plant_data["plot_id"],
                        planted_at=plant_data["planted_at"],
                        last_watered=plant_data["last_watered"],
                        growth_stage=GrowthStage(plant_data["growth_stage"]),
                        water_level=plant_data.get("water_level", 100),
                        health=plant_data.get("health", 100),
                        times_watered=plant_data.get("times_watered", 0),
                        is_withered=plant_data.get("is_withered", False),
                    )
        
        garden.seed_inventory = data.get("seed_inventory", {})
        garden.harvest_inventory = data.get("harvest_inventory", {})
        garden.total_harvests = data.get("total_harvests", 0)
        garden.plants_grown = data.get("plants_grown", {})
        garden.unlocked_plots = data.get("unlocked_plots", 2)
        
        return garden


# Global garden instance
garden = Garden()
