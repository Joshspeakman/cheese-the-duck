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
    "sunflower_seeds": Material("sunflower_seeds", "Sunflower Seeds", "Harvested sunflower seeds.", MaterialCategory.FOOD, 1, 99, 2, 0, 0, 1),
    "tulip_bulb": Material("tulip_bulb", "Tulip Bulb", "A garden tulip bulb.", MaterialCategory.PLANT, 2, 50, 4, 0, 0, 3),
    "rose_petal": Material("rose_petal", "Rose Petal", "A fragrant rose petal.", MaterialCategory.PLANT, 2, 50, 5, 0, 0, 4),
    "carrot": Material("carrot", "Carrot", "A crunchy garden carrot.", MaterialCategory.FOOD, 1, 50, 3, 0, 0, 0),
    "tomato": Material("tomato", "Tomato", "A juicy garden tomato.", MaterialCategory.FOOD, 1, 50, 3, 0, 0, 0),
    "pumpkin": Material("pumpkin", "Pumpkin", "A sturdy orange pumpkin.", MaterialCategory.FOOD, 2, 20, 8, 1, 0, 2),
    "strawberry": Material("strawberry", "Strawberry", "A sweet garden berry.", MaterialCategory.FOOD, 1, 50, 3, 0, 0, 1),
    "watermelon": Material("watermelon", "Watermelon", "A refreshing garden melon.", MaterialCategory.FOOD, 2, 10, 12, 0, 0, 1),
    "mint_leaves": Material("mint_leaves", "Mint Leaves", "Fresh mint leaves.", MaterialCategory.PLANT, 1, 99, 2, 0, 0, 1),
    "golden_petal": Material("golden_petal", "Golden Petal", "A rare glowing flower petal.", MaterialCategory.RARE, 5, 10, 75, 0, 0, 10),
    "crystal_shard": Material("crystal_shard", "Crystal Shard", "A shard from a crystal plant.", MaterialCategory.RARE, 5, 10, 100, 3, 0, 10),
    
    # RARE/SPECIAL materials
    "butterfly_wing": Material("butterfly_wing", "Butterfly Wing", "A delicate wing.", MaterialCategory.RARE, 3, 20, 8, 0, 0, 6),
    "flower_petal": Material("flower_petal", "Flower Petal", "A soft colorful petal.", MaterialCategory.PLANT, 1, 99, 2, 0, 0, 2),
    "juicy_worm": Material("juicy_worm", "Juicy Worm", "A premium worm.", MaterialCategory.FOOD, 2, 30, 5, 0, 0, 0),
    "giant_worm": Material("giant_worm", "Giant Worm", "A very large worm.", MaterialCategory.FOOD, 3, 10, 12, 0, 0, 0),
    "rainbow_feather": Material("rainbow_feather", "Rainbow Feather", "A shimmering rainbow feather.", MaterialCategory.RARE, 5, 5, 120, 0, 3, 10),
    "crystal_icicle": Material("crystal_icicle", "Crystal Icicle", "A clear frozen crystal.", MaterialCategory.RARE, 4, 10, 50, 2, 0, 8),
    "frozen_dewdrop": Material("frozen_dewdrop", "Frozen Dewdrop", "A tiny bead of frozen dew.", MaterialCategory.RARE, 3, 20, 15, 0, 0, 5),
    "static_feather": Material("static_feather", "Static Feather", "A feather that crackles softly.", MaterialCategory.RARE, 3, 20, 20, 0, 1, 5),
    "golden_leaf": Material("golden_leaf", "Golden Leaf", "A brilliant autumn leaf.", MaterialCategory.RARE, 4, 20, 30, 0, 0, 8),
    "red_maple_leaf": Material("red_maple_leaf", "Red Maple Leaf", "A vivid red maple leaf.", MaterialCategory.PLANT, 2, 50, 4, 0, 0, 3),
    "mist_crystal": Material("mist_crystal", "Mist Crystal", "A crystal condensed from fog.", MaterialCategory.RARE, 4, 10, 45, 1, 0, 7),
    "fog_essence": Material("fog_essence", "Fog Essence", "A vial of cool fog.", MaterialCategory.RARE, 4, 10, 35, 0, 0, 6),
    "dandelion_fluff": Material("dandelion_fluff", "Dandelion Fluff", "A tuft of floating fluff.", MaterialCategory.PLANT, 1, 99, 2, 0, 1, 1),
    "mud_sculpture": Material("mud_sculpture", "Mud Sculpture", "A tiny mud artwork.", MaterialCategory.EARTH, 2, 20, 8, 1, 0, 4, True),
    "snow_feather": Material("snow_feather", "Snow Feather", "A feather dusted with snow.", MaterialCategory.RARE, 3, 20, 20, 0, 2, 5),
    "storm_sketch": Material("storm_sketch", "Storm Sketch", "A dramatic weather sketch.", MaterialCategory.RARE, 3, 10, 25, 0, 0, 6),
    "paper_plane_design": Material("paper_plane_design", "Paper Plane Design", "A foldable flying design.", MaterialCategory.RARE, 2, 20, 10, 0, 0, 3),
    "fog_bell": Material("fog_bell", "Fog Bell", "A bell that sounds distant.", MaterialCategory.RARE, 4, 5, 60, 0, 0, 8),
    "mystery_sound": Material("mystery_sound", "Mystery Sound", "Somehow, a sound you can keep.", MaterialCategory.RARE, 4, 5, 50, 0, 0, 7),
    "rare_bug_jar": Material("rare_bug_jar", "Rare Bug Jar", "A jar containing a rare bug.", MaterialCategory.RARE, 3, 10, 30, 0, 0, 4),
    "memory_trophy": Material("memory_trophy", "Memory Trophy", "A trophy for sharp memory.", MaterialCategory.RARE, 3, 5, 35, 0, 0, 5),
    "racing_medal": Material("racing_medal", "Racing Medal", "A medal from a fast race.", MaterialCategory.RARE, 3, 5, 35, 0, 0, 5),
    "spring_petal": Material("spring_petal", "Spring Petal", "A delicate spring festival petal.", MaterialCategory.PLANT, 1, 99, 2, 0, 0, 3),
    "fresh_apple": Material("fresh_apple", "Fresh Apple", "A crisp autumn apple.", MaterialCategory.FOOD, 1, 50, 3, 0, 0, 1),
    "autumn_leaf": Material("autumn_leaf", "Autumn Leaf", "A colorful fallen leaf.", MaterialCategory.PLANT, 1, 99, 2, 0, 0, 2),
    "homemade_pie": Material("homemade_pie", "Homemade Pie", "A rare homemade festival pie.", MaterialCategory.FOOD, 3, 10, 25, 0, 0, 4),
    "snowball": Material("snowball", "Snowball", "A perfectly packed snowball.", MaterialCategory.WATER, 1, 20, 2, 0, 1, 0),
    "ice_crystal": Material("ice_crystal", "Ice Crystal", "A sparkling winter crystal.", MaterialCategory.RARE, 3, 20, 20, 2, 0, 6),
    "warmth": Material("warmth", "Warmth", "A cozy feeling saved for later.", MaterialCategory.RARE, 2, 10, 10, 0, 5, 3),
    "mystery_gift": Material("mystery_gift", "Mystery Gift", "A wrapped festival mystery.", MaterialCategory.RARE, 3, 10, 30, 0, 0, 5),
    "friendship_card": Material("friendship_card", "Friendship Card", "A handmade card full of love.", MaterialCategory.RARE, 2, 20, 12, 0, 0, 5),
    "heart_cookie": Material("heart_cookie", "Heart Cookie", "A heart-shaped cookie.", MaterialCategory.FOOD, 3, 10, 18, 0, 0, 4),
    "splash_trophy": Material("splash_trophy", "Splash Trophy", "Winner of the splash contest.", MaterialCategory.RARE, 3, 5, 35, 0, 0, 7),
    "sunset_photo": Material("sunset_photo", "Sunset Photo", "A keepsake from a perfect sunset.", MaterialCategory.RARE, 3, 10, 20, 0, 0, 6),
    "parade_flag": Material("parade_flag", "Parade Flag", "A Duck Day parade flag.", MaterialCategory.FIBER, 2, 20, 15, 1, 0, 4),
    "dance_medal": Material("dance_medal", "Dance Medal", "A medal for excellent dancing.", MaterialCategory.RARE, 3, 5, 35, 0, 0, 7),
    "spring_duck_costume": Material("spring_duck_costume", "Spring Duck Costume", "A flowery spring outfit token.", MaterialCategory.RARE, 4, 5, 70, 0, 0, 8),
    "cherry_blossom_hat": Material("cherry_blossom_hat", "Cherry Blossom Hat", "A hat with cherry blossoms.", MaterialCategory.RARE, 3, 5, 45, 0, 0, 7),
    "beach_duck_costume": Material("beach_duck_costume", "Beach Duck Costume", "A tropical summer outfit token.", MaterialCategory.RARE, 4, 5, 70, 0, 0, 8),
    "surfboard": Material("surfboard", "Surfboard", "A rad festival surfboard.", MaterialCategory.RARE, 3, 5, 50, 2, 0, 7, True),
    "scarecrow_costume": Material("scarecrow_costume", "Scarecrow Costume", "A festive scarecrow outfit token.", MaterialCategory.RARE, 4, 5, 70, 0, 0, 8),
    "autumn_wreath_hat": Material("autumn_wreath_hat", "Autumn Wreath Hat", "A hat with autumn leaves.", MaterialCategory.RARE, 3, 5, 45, 0, 0, 7),
    "winter_coat_costume": Material("winter_coat_costume", "Winter Coat Costume", "A warm festive winter outfit token.", MaterialCategory.RARE, 4, 5, 70, 0, 4, 8),
    "snowflake_crown": Material("snowflake_crown", "Snowflake Crown", "A crown of eternal snowflakes.", MaterialCategory.RARE, 4, 5, 60, 0, 0, 8),
    "duck_crown": Material("duck_crown", "Duck Crown", "A crown fit for the finest duck.", MaterialCategory.RARE, 5, 5, 100, 0, 0, 10),
    "heart_hat": Material("heart_hat", "Heart Hat", "A hat covered in hearts.", MaterialCategory.RARE, 3, 5, 55, 0, 0, 7),
    "golden_duck_trophy": Material("golden_duck_trophy", "Golden Duck Trophy", "The ultimate duck prize.", MaterialCategory.RARE, 5, 1, 200, 3, 0, 10),
    "spring_spirit_badge": Material("spring_spirit_badge", "Spring Spirit Badge", "Proof of spring celebration.", MaterialCategory.RARE, 4, 5, 80, 0, 0, 8),
    "summer_spirit_badge": Material("summer_spirit_badge", "Summer Spirit Badge", "Proof of summer fun.", MaterialCategory.RARE, 4, 5, 80, 0, 0, 8),
    "harvest_spirit_badge": Material("harvest_spirit_badge", "Harvest Spirit Badge", "Proof of autumn bounty.", MaterialCategory.RARE, 4, 5, 80, 0, 0, 8),
    "winter_spirit_badge": Material("winter_spirit_badge", "Winter Spirit Badge", "Proof of winter magic.", MaterialCategory.RARE, 4, 5, 80, 0, 0, 8),
    "duck_day_champion_badge": Material("duck_day_champion_badge", "Duck Day Champion Badge", "Champion of Duck Day.", MaterialCategory.RARE, 5, 5, 120, 0, 0, 10),
    "love_spirit_badge": Material("love_spirit_badge", "Love Spirit Badge", "Spreader of love and friendship.", MaterialCategory.RARE, 4, 5, 80, 0, 0, 8),
    "welcome_bread": Material("welcome_bread", "Welcome Bread", "A first-loaf keepsake for a new duck.", MaterialCategory.FOOD, 2, 10, 12, 0, 0, 2),
    "duck_toy": Material("duck_toy", "Duck Toy", "A simple toy earned from early care.", MaterialCategory.CRAFTED, 2, 10, 15, 0, 0, 3, True),
    "magpie_friendship_charm": Material("magpie_friendship_charm", "Magpie Friendship Charm", "A shiny charm from a completed quest chain.", MaterialCategory.RARE, 4, 5, 80, 0, 0, 9),
    "better_bait": Material("better_bait", "Better Bait", "Improved bait for serious fishing.", MaterialCategory.FOOD, 2, 20, 10, 0, 0, 0),
    "master_fishing_rod": Material("master_fishing_rod", "Master Fishing Rod", "A trophy-grade fishing rod.", MaterialCategory.CRAFTED, 4, 1, 120, 4, 0, 5, True),
    "fish_trophy": Material("fish_trophy", "Fish Trophy", "Proof of a great fish tale.", MaterialCategory.RARE, 3, 5, 50, 0, 0, 7),
    "dream_flower": Material("dream_flower", "Dream Flower", "A flower that smells like sleep.", MaterialCategory.RARE, 4, 10, 60, 0, 0, 9),
    "enchanted_seeds": Material("enchanted_seeds", "Enchanted Seeds", "Seeds that hum with garden magic.", MaterialCategory.RARE, 4, 10, 65, 0, 0, 8),
    "ancient_amulet": Material("ancient_amulet", "Ancient Amulet", "A strange amulet from an old mystery.", MaterialCategory.RARE, 5, 3, 150, 0, 0, 10),
    "guardian_blessing": Material("guardian_blessing", "Guardian Blessing", "A blessing carefully bottled as a keepsake.", MaterialCategory.RARE, 5, 5, 120, 0, 5, 10),
    "rare_treat": Material("rare_treat", "Rare Treat", "A premium reward treat.", MaterialCategory.FOOD, 3, 10, 30, 0, 0, 2),
    "weekly_chest": Material("weekly_chest", "Weekly Chest", "A reward chest for showing up all week.", MaterialCategory.RARE, 4, 5, 90, 2, 0, 8),
    "explorer_badge": Material("explorer_badge", "Explorer Badge", "A badge for serious wandering.", MaterialCategory.RARE, 3, 10, 45, 0, 0, 7),
    "master_trophy": Material("master_trophy", "Master Trophy", "A trophy for clearing the weekly board.", MaterialCategory.RARE, 5, 3, 160, 3, 0, 10),
    "rainbow_charm": Material("rainbow_charm", "Rainbow Charm", "A charm that caught a rainbow's edge.", MaterialCategory.RARE, 5, 5, 120, 0, 0, 10),
    "legendary_trophy": Material("legendary_trophy", "Legendary Trophy", "A trophy for catching a legendary fish.", MaterialCategory.RARE, 5, 3, 180, 3, 0, 10),
    "golden_badge": Material("golden_badge", "Golden Badge", "A badge for growing something impossible.", MaterialCategory.RARE, 5, 5, 130, 0, 0, 10),
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
