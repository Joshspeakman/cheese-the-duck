"""
Shop system - 255 items to unlock and place in the habitat.
Items range from cosmetics to furniture with visual impact and interactions.
"""
from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass


class ItemCategory(Enum):
    """Categories of shop items."""
    COSMETIC = "cosmetic"  # Hats, accessories worn by duck
    TOY = "toy"  # Interactive toys
    FURNITURE = "furniture"  # Chairs, tables, etc.
    WATER = "water"  # Pools, fountains, ponds
    PLANT = "plant"  # Trees, flowers, bushes
    STRUCTURE = "structure"  # Houses, walls, fences
    DECORATION = "decoration"  # Statues, signs, misc
    LIGHTING = "lighting"  # Lamps, candles
    FLOORING = "flooring"  # Rugs, tiles, patterns
    SPECIAL = "special"  # Unique animated items


class ItemRarity(Enum):
    """Item rarity tiers affecting cost and unlock requirements."""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


@dataclass
class ShopItem:
    """A purchasable item for the habitat."""
    id: str
    name: str
    description: str
    category: ItemCategory
    rarity: ItemRarity
    cost: int  # In-game currency
    unlock_level: int  # Player level required
    unlock_xp: int  # Total XP required
    size: str  # "small", "medium", "large"
    animated: bool = False
    interaction_text: List[str] = None  # What duck says when interacting
    
    def __post_init__(self):
        if self.interaction_text is None:
            self.interaction_text = []


# Shop items database - 255 total items
SHOP_ITEMS: Dict[str, ShopItem] = {}


def register_item(item: ShopItem):
    """Register an item in the shop."""
    SHOP_ITEMS[item.id] = item


# ========================================
# COSMETICS (IDs 1-50) - Hats & Accessories
# ========================================

# Common cosmetics (Level 1-5, 50-200 coins)
register_item(ShopItem(
    id="hat_red", name="Red Cap", description="A classic red baseball cap. Very dapper!",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.COMMON,
    cost=50, unlock_level=1, unlock_xp=0, size="small",
    interaction_text=["*adjusts cap* How do I look? *quack*", "*tips cap* M'human."]
))

register_item(ShopItem(
    id="hat_blue", name="Blue Cap", description="A cool blue cap for a cool duck.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.COMMON,
    cost=50, unlock_level=1, unlock_xp=0, size="small",
    interaction_text=["*straightens cap* Blue is SO my color!", "*quack* Stylin'!"]
))

register_item(ShopItem(
    id="hat_party", name="Party Hat", description="Pointy, colorful, and festive!",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.COMMON,
    cost=75, unlock_level=1, unlock_xp=0, size="small",
    interaction_text=["*PARTY QUACK!*", "Every day is a party! *dances*"]
))

register_item(ShopItem(
    id="hat_chef", name="Chef's Hat", description="For the sophisticated culinary duck.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.COMMON,
    cost=100, unlock_level=2, unlock_xp=50, size="small",
    interaction_text=["*chef's kiss* Quack!", "Bread is art. I am artist. *nods*"]
))

register_item(ShopItem(
    id="hat_wizard", name="Wizard Hat", description="Mystical pointy hat with stars.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.UNCOMMON,
    cost=200, unlock_level=3, unlock_xp=150, size="small",
    interaction_text=["*waves wing* Abra-qua-dabra!", "*mystical quacking*"]
))

register_item(ShopItem(
    id="hat_crown", name="Golden Crown", description="For royalty. You're looking at them.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.RARE,
    cost=500, unlock_level=5, unlock_xp=500, size="small",
    interaction_text=["*regal quack* KNEEL.", "Being royalty is exhausting. *sigh*"]
))

register_item(ShopItem(
    id="hat_viking", name="Viking Helmet", description="With horns! Historically inaccurate but awesome.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.UNCOMMON,
    cost=250, unlock_level=4, unlock_xp=300, size="small",
    interaction_text=["*warrior quack* FOR VALHALLA!", "*pillages bread basket*"]
))

register_item(ShopItem(
    id="hat_pirate", name="Pirate Hat", description="Arr! A tricorn for swashbuckling ducks.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.UNCOMMON,
    cost=250, unlock_level=4, unlock_xp=300, size="small",
    interaction_text=["Arr! *pirate quack*", "Where's me treasure? Oh wait, it's bread."]
))

register_item(ShopItem(
    id="hat_cowboy", name="Cowboy Hat", description="Yeehaw! Partner.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.UNCOMMON,
    cost=200, unlock_level=3, unlock_xp=150, size="small",
    interaction_text=["*tips hat* Howdy, partner!", "This pond ain't big enough for both of us. Wait, yes it is."]
))

register_item(ShopItem(
    id="hat_tophat", name="Top Hat", description="Classy and sophisticated. Very fancy.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.RARE,
    cost=400, unlock_level=5, unlock_xp=500, size="small",
    interaction_text=["*sophisticated quack*", "Indeed. Quite. *adjusts monocle that doesn't exist*"]
))

# More cosmetics continuing...
register_item(ShopItem(
    id="hat_beret", name="Beret", description="Très chic! For the artistic duck.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.COMMON,
    cost=150, unlock_level=2, unlock_xp=50, size="small",
    interaction_text=["*artistic quack* C'est magnifique!", "I don't speak French but I feel fancy."]
))

register_item(ShopItem(
    id="hat_beanie", name="Beanie", description="Warm and cozy winter hat.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.COMMON,
    cost=100, unlock_level=2, unlock_xp=50, size="small",
    interaction_text=["*cozy quack*", "So warm! So comfy!"]
))

register_item(ShopItem(
    id="hat_sombrero", name="Sombrero", description="Large, festive, and provides excellent shade.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.UNCOMMON,
    cost=300, unlock_level=4, unlock_xp=300, size="small",
    interaction_text=["*festive quacking*", "This is VERY big. I love it."]
))

register_item(ShopItem(
    id="glasses_cool", name="Sunglasses", description="Deal with it. B) (but in text form)",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.COMMON,
    cost=150, unlock_level=2, unlock_xp=50, size="small",
    interaction_text=["*cool quack*", "Can't see anything but I LOOK GOOD."]
))

register_item(ShopItem(
    id="glasses_nerd", name="Nerd Glasses", description="Smart duck energy.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.COMMON,
    cost=100, unlock_level=2, unlock_xp=50, size="small",
    interaction_text=["*pushes up glasses* Actually...", "*intelligent quacking*"]
))

register_item(ShopItem(
    id="bowtie", name="Bow Tie", description="Fancy neckwear for formal occasions.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.COMMON,
    cost=120, unlock_level=2, unlock_xp=50, size="small",
    interaction_text=["*adjusts bow tie* Dapper!", "Bow ties are cool. *quack*"]
))

register_item(ShopItem(
    id="scarf_red", name="Red Scarf", description="Cozy and stylish.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.COMMON,
    cost=100, unlock_level=1, unlock_xp=0, size="small",
    interaction_text=["*wrapped in warmth*", "*muffled quacking through scarf*"]
))

register_item(ShopItem(
    id="cape", name="Superhero Cape", description="For when you need to save the day!",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.RARE,
    cost=600, unlock_level=6, unlock_xp=800, size="small",
    interaction_text=["*heroic pose* SUPER DUCK!", "*attempts to fly, waddles instead*"]
))

register_item(ShopItem(
    id="wings_fairy", name="Fairy Wings", description="Sparkly, magical wings.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.EPIC,
    cost=1000, unlock_level=8, unlock_xp=1500, size="small", animated=True,
    interaction_text=["*sparkles*", "*magical quacking*"]
))

register_item(ShopItem(
    id="halo", name="Halo", description="Angelic duck mode activated.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.RARE,
    cost=500, unlock_level=6, unlock_xp=800, size="small", animated=True,
    interaction_text=["*angelic quack*", "I'm basically a saint. Of bread."]
))

# ========================================
# TOYS (IDs 51-80) - Interactive items
# ========================================

register_item(ShopItem(
    id="toy_ball", name="Rubber Ball", description="A bouncy ball to play with!",
    category=ItemCategory.TOY, rarity=ItemRarity.COMMON,
    cost=80, unlock_level=1, unlock_xp=0, size="small",
    interaction_text=["*pushes ball* Wheee!", "*chases ball* Come back here!"]
))

register_item(ShopItem(
    id="toy_blocks", name="Building Blocks", description="Colorful blocks to stack and knock over.",
    category=ItemCategory.TOY, rarity=ItemRarity.COMMON,
    cost=100, unlock_level=1, unlock_xp=0, size="small",
    interaction_text=["*stacks blocks carefully*", "*KNOCKS OVER BLOCKS* Oops!"]
))

register_item(ShopItem(
    id="toy_trumpet", name="Toy Trumpet", description="For making noise! So much noise!",
    category=ItemCategory.TOY, rarity=ItemRarity.COMMON,
    cost=150, unlock_level=2, unlock_xp=50, size="small",
    interaction_text=["*HONK HONK* This is AMAZING!", "*jazz quacking*"]
))

register_item(ShopItem(
    id="toy_skateboard", name="Skateboard", description="Radical! Cowabunga!",
    category=ItemCategory.TOY, rarity=ItemRarity.UNCOMMON,
    cost=300, unlock_level=3, unlock_xp=150, size="medium",
    interaction_text=["*kickflips* ...almost!", "*rolls around* Quack yeah!"]
))

register_item(ShopItem(
    id="toy_piano", name="Toy Piano", description="A small piano for musical ducks.",
    category=ItemCategory.TOY, rarity=ItemRarity.UNCOMMON,
    cost=400, unlock_level=4, unlock_xp=300, size="medium",
    interaction_text=["*pecks keys* ##", "*composes masterpiece* This is called 'Bread in D Minor'"]
))

register_item(ShopItem(
    id="toy_trampoline", name="Trampoline", description="Bounceounce bounce!",
    category=ItemCategory.TOY, rarity=ItemRarity.UNCOMMON,
    cost=500, unlock_level=5, unlock_xp=500, size="medium", animated=True,
    interaction_text=["*BOING BOING* THIS IS THE BEST!", "*bouncing intensifies*"]
))

register_item(ShopItem(
    id="toy_slide", name="Playground Slide", description="Whee! Down we go!",
    category=ItemCategory.TOY, rarity=ItemRarity.RARE,
    cost=800, unlock_level=6, unlock_xp=800, size="large",
    interaction_text=["*slides down* WHEEEEE!", "*climbs up for another turn*"]
))

register_item(ShopItem(
    id="toy_swing", name="Swing Set", description="Swing high into the sky!",
    category=ItemCategory.TOY, rarity=ItemRarity.RARE,
    cost=800, unlock_level=6, unlock_xp=800, size="large", animated=True,
    interaction_text=["*swinging* Higher! HIGHER!", "*pumps legs* I can touch the clouds! (No I can't)"]
))

register_item(ShopItem(
    id="toy_seesaw", name="Seesaw", description="Up and down! (Works better with two ducks)",
    category=ItemCategory.TOY, rarity=ItemRarity.UNCOMMON,
    cost=400, unlock_level=4, unlock_xp=300, size="medium",
    interaction_text=["*sits on one end* ...I need a friend.", "*bounces slightly* This is fun? I guess?"]
))

register_item(ShopItem(
    id="toy_sandbox", name="Sandbox", description="Dig, build, play! (Gets everywhere)",
    category=ItemCategory.TOY, rarity=ItemRarity.COMMON,
    cost=250, unlock_level=3, unlock_xp=150, size="medium",
    interaction_text=["*digs furiously*", "*makes sand castle* Architectural genius!"]
))

register_item(ShopItem(
    id="toy_boombox", name="Boombox", description="A retro boombox! Turn it on for some tunes!",
    category=ItemCategory.TOY, rarity=ItemRarity.RARE,
    cost=350, unlock_level=3, unlock_xp=150, size="medium", animated=True,
    interaction_text=["*turns on boombox* ## MUSIC TIME! ##", "*dances to the beat* This is my JAM!"]
))

# ========================================
# FURNITURE (IDs 81-110)
# ========================================

register_item(ShopItem(
    id="chair_wood", name="Wooden Chair", description="Simple, sturdy, sittable.",
    category=ItemCategory.FURNITURE, rarity=ItemRarity.COMMON,
    cost=100, unlock_level=1, unlock_xp=0, size="small",
    interaction_text=["*sits* Ahh, perfect.", "*lounges* This is the life."]
))

register_item(ShopItem(
    id="chair_throne", name="Royal Throne", description="For sitting like the royalty you are.",
    category=ItemCategory.FURNITURE, rarity=ItemRarity.EPIC,
    cost=2000, unlock_level=10, unlock_xp=3000, size="large",
    interaction_text=["*sits majestically* BEHOLD.", "*waves wing dismissively* Peasants."]
))

register_item(ShopItem(
    id="table_small", name="Small Table", description="Perfect for snacks!",
    category=ItemCategory.FURNITURE, rarity=ItemRarity.COMMON,
    cost=150, unlock_level=1, unlock_xp=0, size="medium",
    interaction_text=["*hops on table* Great view!", "*places bread here* My shrine."]
))

register_item(ShopItem(
    id="bed_small", name="Cozy Bed", description="For naps. So many naps.",
    category=ItemCategory.FURNITURE, rarity=ItemRarity.COMMON,
    cost=200, unlock_level=2, unlock_xp=50, size="medium",
    interaction_text=["*flops into bed* zzz", "*makes nest* Perfect!"]
))

register_item(ShopItem(
    id="bed_king", name="King Size Bed", description="Ridiculously large for one duck.",
    category=ItemCategory.FURNITURE, rarity=ItemRarity.RARE,
    cost=1000, unlock_level=7, unlock_xp=1000, size="large",
    interaction_text=["*spreads out* SO MUCH ROOM!", "*gets lost in bed*"]
))

register_item(ShopItem(
    id="couch", name="Comfy Couch", description="For lounging like a boss.",
    category=ItemCategory.FURNITURE, rarity=ItemRarity.UNCOMMON,
    cost=500, unlock_level=5, unlock_xp=500, size="large",
    interaction_text=["*sprawls* Don't wanna move. Ever.", "*cushion quack*"]
))

register_item(ShopItem(
    id="bookshelf", name="Bookshelf", description="For books you pretend to read.",
    category=ItemCategory.FURNITURE, rarity=ItemRarity.UNCOMMON,
    cost=300, unlock_level=3, unlock_xp=150, size="medium",
    interaction_text=["*looks at books* I can't read. But it looks SMART!", "*pulls out book* Is this about bread?"]
))

register_item(ShopItem(
    id="desk", name="Writing Desk", description="For important duck business.",
    category=ItemCategory.FURNITURE, rarity=ItemRarity.UNCOMMON,
    cost=400, unlock_level=4, unlock_xp=300, size="medium",
    interaction_text=["*sits at desk importantly*", "*scribbles* Dear diary: BREAD."]
))

register_item(ShopItem(
    id="lamp_floor", name="Floor Lamp", description="Provides ambiance and light!",
    category=ItemCategory.FURNITURE, rarity=ItemRarity.COMMON,
    cost=200, unlock_level=2, unlock_xp=50, size="small",
    interaction_text=["*flicks lamp on and off* MAGIC!", "*basks in the glow*"]
))

register_item(ShopItem(
    id="mirror", name="Full Length Mirror", description="For admiring yourself. A lot.",
    category=ItemCategory.FURNITURE, rarity=ItemRarity.UNCOMMON,
    cost=300, unlock_level=3, unlock_xp=150, size="medium",
    interaction_text=["*stares* Who's that handsome duck? Oh, it's me!", "*poses*"]
))

# ========================================
# WATER FEATURES (IDs 111-130)
# ========================================

register_item(ShopItem(
    id="pool_kiddie", name="Kiddie Pool", description="A small inflatable pool. Splish splash!",
    category=ItemCategory.WATER, rarity=ItemRarity.COMMON,
    cost=300, unlock_level=2, unlock_xp=50, size="medium", animated=True,
    interaction_text=["*splashes* WATER!", "*paddles around*"]
))

register_item(ShopItem(
    id="pool_large", name="Swimming Pool", description="A proper pool for swimming!",
    category=ItemCategory.WATER, rarity=ItemRarity.RARE,
    cost=1500, unlock_level=8, unlock_xp=1500, size="large", animated=True,
    interaction_text=["*dives in* CANNONBALL!", "*swims laps* I'm an athlete!"]
))

register_item(ShopItem(
    id="fountain_small", name="Garden Fountain", description="Peaceful bubbling water.",
    category=ItemCategory.WATER, rarity=ItemRarity.UNCOMMON,
    cost=600, unlock_level=5, unlock_xp=500, size="medium", animated=True,
    interaction_text=["*drinks from fountain*", "*splashes face* Refreshing!"]
))

register_item(ShopItem(
    id="fountain_grand", name="Grand Fountain", description="Majestic, tall, impressive!",
    category=ItemCategory.WATER, rarity=ItemRarity.EPIC,
    cost=2500, unlock_level=12, unlock_xp=4000, size="large", animated=True,
    interaction_text=["*stares in awe*", "*feels fancy*"]
))

register_item(ShopItem(
    id="pond", name="Duck Pond", description="A natural pond. Your ancestral home!",
    category=ItemCategory.WATER, rarity=ItemRarity.RARE,
    cost=1200, unlock_level=7, unlock_xp=1000, size="large", animated=True,
    interaction_text=["*happy duck noises* HOME!", "*floats peacefully*"]
))

register_item(ShopItem(
    id="sprinkler", name="Lawn Sprinkler", description="Run through it! Get wet!",
    category=ItemCategory.WATER, rarity=ItemRarity.COMMON,
    cost=200, unlock_level=2, unlock_xp=50, size="small", animated=True,
    interaction_text=["*runs through sprinkler* WHEEE!", "*gets soaked* Worth it!"]
))

register_item(ShopItem(
    id="waterfall", name="Waterfall", description="Cascading water. Very zen.",
    category=ItemCategory.WATER, rarity=ItemRarity.EPIC,
    cost=3000, unlock_level=13, unlock_xp=5000, size="large", animated=True,
    interaction_text=["*listens to water* So peaceful...", "*stands under waterfall* COLD!"]
))

register_item(ShopItem(
    id="hot_tub", name="Hot Tub", description="Luxury! Bubbles! Warmth!",
    category=ItemCategory.WATER, rarity=ItemRarity.RARE,
    cost=2000, unlock_level=10, unlock_xp=3000, size="large", animated=True,
    interaction_text=["*relaxes* Ahhhh...", "*bubbles* This is AMAZING!"]
))

register_item(ShopItem(
    id="birdbath", name="Bird Bath", description="Ironically, perfect for ducks too.",
    category=ItemCategory.WATER, rarity=ItemRarity.COMMON,
    cost=150, unlock_level=1, unlock_xp=0, size="small",
    interaction_text=["*splashes* Bath time!", "*preens feathers*"]
))

register_item(ShopItem(
    id="water_slide", name="Water Slide", description="Slide into the pool! Wheee!",
    category=ItemCategory.WATER, rarity=ItemRarity.EPIC,
    cost=2500, unlock_level=11, unlock_xp=3500, size="large", animated=True,
    interaction_text=["*slides down* WHEEEEE SPLASH!", "*climbs up again* AGAIN!"]
))

# ========================================
# PLANTS (IDs 131-160)
# ========================================

register_item(ShopItem(
    id="flower_rose", name="Rose Bush", description="Beautiful red roses.",
    category=ItemCategory.PLANT, rarity=ItemRarity.COMMON,
    cost=100, unlock_level=1, unlock_xp=0, size="small",
    interaction_text=["*smells roses* Quack!", "*tries to eat* ...not bread."]
))

register_item(ShopItem(
    id="flower_tulip", name="Tulips", description="Colorful spring flowers!",
    category=ItemCategory.PLANT, rarity=ItemRarity.COMMON,
    cost=80, unlock_level=1, unlock_xp=0, size="small",
    interaction_text=["*appreciates beauty*", "*waddles through tulips*"]
))

register_item(ShopItem(
    id="flower_sunflower", name="Sunflower", description="Tall, bright, happy!",
    category=ItemCategory.PLANT, rarity=ItemRarity.COMMON,
    cost=120, unlock_level=1, unlock_xp=0, size="medium",
    interaction_text=["*stands next to sunflower* I'm taller! Wait...", "*pecks seeds* SNACK!"]
))

register_item(ShopItem(
    id="tree_small", name="Small Tree", description="A cute little tree for shade.",
    category=ItemCategory.PLANT, rarity=ItemRarity.UNCOMMON,
    cost=300, unlock_level=3, unlock_xp=150, size="medium",
    interaction_text=["*sits under tree* Shady!", "*pecks bark* Knock knock!"]
))

register_item(ShopItem(
    id="tree_oak", name="Oak Tree", description="Large, majestic, ancient.",
    category=ItemCategory.PLANT, rarity=ItemRarity.RARE,
    cost=800, unlock_level=6, unlock_xp=800, size="large",
    interaction_text=["*looks up* So tall!", "*naps under tree*"]
))

register_item(ShopItem(
    id="tree_cherry", name="Cherry Blossom Tree", description="Pink petals drift down beautifully.",
    category=ItemCategory.PLANT, rarity=ItemRarity.EPIC,
    cost=1500, unlock_level=9, unlock_xp=2000, size="large", animated=True,
    interaction_text=["*catches petal* Magical!", "*photo op quack*"]
))

register_item(ShopItem(
    id="bush_hedge", name="Hedge Bush", description="Perfect for privacy!",
    category=ItemCategory.PLANT, rarity=ItemRarity.COMMON,
    cost=150, unlock_level=2, unlock_xp=50, size="medium",
    interaction_text=["*hides behind bush*", "*peeks out* Can't see me!"]
))

register_item(ShopItem(
    id="grass_patch", name="Grass Patch", description="Soft green grass. Nice!",
    category=ItemCategory.PLANT, rarity=ItemRarity.COMMON,
    cost=50, unlock_level=1, unlock_xp=0, size="small",
    interaction_text=["*rolls in grass*", "*munches grass* Tastes green."]
))

register_item(ShopItem(
    id="cactus", name="Cactus", description="Spiky! Do not hug!",
    category=ItemCategory.PLANT, rarity=ItemRarity.UNCOMMON,
    cost=200, unlock_level=3, unlock_xp=150, size="small",
    interaction_text=["*stares* Why would anyone... okay.", "*gets too close* OW!"]
))

register_item(ShopItem(
    id="bamboo", name="Bamboo Grove", description="Peaceful bamboo stalks.",
    category=ItemCategory.PLANT, rarity=ItemRarity.RARE,
    cost=700, unlock_level=6, unlock_xp=800, size="medium",
    interaction_text=["*zen quack*", "*hides in bamboo*"]
))

# ============ MORE COSMETICS (20 more) ============
register_item(ShopItem(
    id="bow_tie_blue", name="Blue Bow Tie", description="Classy blue bow tie.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.COMMON,
    cost=50, unlock_level=1, unlock_xp=0, size="small",
    interaction_text=["Looking sharp!", "*adjusts tie*"]
))

register_item(ShopItem(
    id="bow_tie_pink", name="Pink Bow Tie", description="Fabulous pink bow tie.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.COMMON,
    cost=50, unlock_level=1, unlock_xp=0, size="small",
    interaction_text=["Feeling fancy!", "*struts*"]
))

register_item(ShopItem(
    id="cap_sports", name="Sports Cap", description="For the athletic duck.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.COMMON,
    cost=75, unlock_level=1, unlock_xp=0, size="small",
    interaction_text=["Ready to play!", "*does warm-up stretches*"]
))

register_item(ShopItem(
    id="beanie_striped", name="Striped Beanie", description="Hip striped beanie.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.COMMON,
    cost=75, unlock_level=2, unlock_xp=50, size="small",
    interaction_text=["*hipster quack*", "Too cool for school!"]
))

register_item(ShopItem(
    id="bandana", name="Bandana", description="Cool bandana accessory.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.COMMON,
    cost=60, unlock_level=2, unlock_xp=50, size="small",
    interaction_text=["*rebel quack*", "Born to waddle!"]
))

register_item(ShopItem(
    id="headphones", name="Headphones", description="Listening to duck jams.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.UNCOMMON,
    cost=150, unlock_level=3, unlock_xp=150, size="small", animated=True,
    interaction_text=["*vibing to music*", "Can't hear you, jamming!"]
))

register_item(ShopItem(
    id="sunglasses_aviator", name="Aviator Sunglasses", description="Top Gun duck.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.UNCOMMON,
    cost=180, unlock_level=3, unlock_xp=150, size="small",
    interaction_text=["*cool quack*", "Highway to the quack zone!"]
))

register_item(ShopItem(
    id="scarf_winter", name="Winter Scarf", description="Cozy knitted scarf.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.UNCOMMON,
    cost=120, unlock_level=4, unlock_xp=300, size="small",
    interaction_text=["So warm!", "*snuggles into scarf*"]
))

register_item(ShopItem(
    id="crown_golden", name="Golden Crown", description="Royalty among ducks.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.EPIC,
    cost=800, unlock_level=8, unlock_xp=1500, size="small",
    interaction_text=["*royal quack*", "Bow before your duck overlord!"]
))

register_item(ShopItem(
    id="viking_helmet", name="Viking Helmet", description="Raid and pillage!",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.RARE,
    cost=400, unlock_level=6, unlock_xp=800, size="small",
    interaction_text=["*QUAAACK!*", "To Valhalla!"]
))

register_item(ShopItem(
    id="wizard_hat", name="Wizard Hat", description="You're a wizard, ducky!",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.EPIC,
    cost=900, unlock_level=9, unlock_xp=2000, size="small",
    interaction_text=["*casts spell*", "Quackus Wingardium!"]
))

register_item(ShopItem(
    id="pirate_hat", name="Pirate Hat", description="Yarr, matey duck!",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.RARE,
    cost=450, unlock_level=7, unlock_xp=1200, size="small",
    interaction_text=["Shiver me feathers!", "*pirate quack*"]
))

register_item(ShopItem(
    id="flower_crown", name="Flower Crown", description="Pretty flower crown.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.UNCOMMON,
    cost=200, unlock_level=4, unlock_xp=300, size="small",
    interaction_text=["*flower power*", "Nature duck!"]
))

register_item(ShopItem(
    id="cape_superhero", name="Superhero Cape", description="Not all heroes wear capes. Oh wait.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.RARE,
    cost=500, unlock_level=7, unlock_xp=1200, size="small", animated=True,
    interaction_text=["*heroic pose*", "Up, up, and a-QUACK!"]
))

register_item(ShopItem(
    id="backpack_tiny", name="Tiny Backpack", description="For duck adventures.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.UNCOMMON,
    cost=180, unlock_level=5, unlock_xp=500, size="small",
    interaction_text=["Ready for adventure!", "*checks map*"]
))

register_item(ShopItem(
    id="monocle", name="Monocle", description="Distinguished and refined.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.RARE,
    cost=350, unlock_level=6, unlock_xp=800, size="small",
    interaction_text=["*posh quack*", "Indeed, quite!"]
))

register_item(ShopItem(
    id="halo_angel", name="Angel Halo", description="Angelic duck halo.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.LEGENDARY,
    cost=1500, unlock_level=12, unlock_xp=5000, size="small", animated=True,
    interaction_text=["*innocent quack*", "I'm an angel, I swear!"]
))

register_item(ShopItem(
    id="devil_horns", name="Devil Horns", description="Mischievous devil horns.",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.LEGENDARY,
    cost=1500, unlock_level=12, unlock_xp=5000, size="small", animated=True,
    interaction_text=["*evil quack*", "Let's cause some chaos!"]
))

register_item(ShopItem(
    id="party_hat", name="Party Hat", description="It's party time!",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.COMMON,
    cost=80, unlock_level=2, unlock_xp=50, size="small",
    interaction_text=["*party quack*", "Let's celebrate!"]
))

register_item(ShopItem(
    id="space_helmet", name="Space Helmet", description="Astronaut duck reporting!",
    category=ItemCategory.COSMETIC, rarity=ItemRarity.EPIC,
    cost=1000, unlock_level=10, unlock_xp=3000, size="small",
    interaction_text=["Houston, we have a quack!", "*floats weightlessly*"]
))

# ============ MORE TOYS (10 more) ============
register_item(ShopItem(
    id="frisbee", name="Flying Frisbee", description="Catch me if you can!",
    category=ItemCategory.TOY, rarity=ItemRarity.COMMON,
    cost=100, unlock_level=2, unlock_xp=50, size="small", animated=True,
    interaction_text=["*zooom*", "*catches in beak*"]
))

register_item(ShopItem(
    id="toy_car", name="Toy Car", description="Vroom vroom!",
    category=ItemCategory.TOY, rarity=ItemRarity.COMMON,
    cost=120, unlock_level=2, unlock_xp=50, size="small",
    interaction_text=["*beep beep*", "*pushes with beak*"]
))

register_item(ShopItem(
    id="jump_rope", name="Jump Rope", description="Skip! Skip! Skip!",
    category=ItemCategory.TOY, rarity=ItemRarity.UNCOMMON,
    cost=150, unlock_level=3, unlock_xp=150, size="small", animated=True,
    interaction_text=["*huff puff*", "*jumps awkwardly*"]
))

register_item(ShopItem(
    id="yo_yo", name="Yo-Yo", description="Walk the duck!",
    category=ItemCategory.TOY, rarity=ItemRarity.UNCOMMON,
    cost=180, unlock_level=4, unlock_xp=300, size="small", animated=True,
    interaction_text=["*concentrates*", "Around the world!"]
))

register_item(ShopItem(
    id="kite", name="Colorful Kite", description="Flies high in the sky!",
    category=ItemCategory.TOY, rarity=ItemRarity.RARE,
    cost=400, unlock_level=5, unlock_xp=500, size="medium", animated=True,
    interaction_text=["*watches kite soar*", "It's so pretty up there!"]
))

register_item(ShopItem(
    id="skateboard", name="Skateboard", description="Radical duck!",
    category=ItemCategory.TOY, rarity=ItemRarity.RARE,
    cost=450, unlock_level=6, unlock_xp=800, size="small", animated=True,
    interaction_text=["*kickflip attempt*", "That hurt..."]
))

register_item(ShopItem(
    id="trampoline", name="Mini Trampoline", description="Bounce bounce bounce!",
    category=ItemCategory.TOY, rarity=ItemRarity.RARE,
    cost=550, unlock_level=7, unlock_xp=1200, size="medium", animated=True,
    interaction_text=["WHEEE!", "*bounces wildly*"]
))

register_item(ShopItem(
    id="telescope", name="Telescope", description="Star gazing duck.",
    category=ItemCategory.TOY, rarity=ItemRarity.EPIC,
    cost=800, unlock_level=8, unlock_xp=1500, size="medium",
    interaction_text=["*gazes at stars*", "Is that... Pluto?"]
))

register_item(ShopItem(
    id="easel", name="Art Easel", description="For the artistic duck.",
    category=ItemCategory.TOY, rarity=ItemRarity.EPIC,
    cost=700, unlock_level=8, unlock_xp=1500, size="medium",
    interaction_text=["*paints masterpiece*", "I call it 'Quack Abstract'"]
))

register_item(ShopItem(
    id="drums", name="Drum Set", description="Rock out!",
    category=ItemCategory.TOY, rarity=ItemRarity.EPIC,
    cost=900, unlock_level=9, unlock_xp=2000, size="large", animated=True,
    interaction_text=["*BANG CRASH*", "*epic drum solo*"]
))

# ============ MORE FURNITURE (15 more) ============
register_item(ShopItem(
    id="bookshelf_wood", name="Bookshelf", description="Full of duck literature.",
    category=ItemCategory.FURNITURE, rarity=ItemRarity.UNCOMMON,
    cost=250, unlock_level=3, unlock_xp=150, size="medium",
    interaction_text=["*reads 'War and Quack'*", "Hmm, fascinating!"]
))

register_item(ShopItem(
    id="dresser", name="Wooden Dresser", description="Storage for duck things.",
    category=ItemCategory.FURNITURE, rarity=ItemRarity.UNCOMMON,
    cost=300, unlock_level=4, unlock_xp=300, size="medium",
    interaction_text=["*opens drawer*", "Where did I put that..."]
))

register_item(ShopItem(
    id="mirror_standing", name="Standing Mirror", description="Looking good!",
    category=ItemCategory.FURNITURE, rarity=ItemRarity.UNCOMMON,
    cost=200, unlock_level=3, unlock_xp=150, size="medium",
    interaction_text=["*admires self*", "Who's a handsome duck?"]
))

register_item(ShopItem(
    id="desk_writing", name="Writing Desk", description="For important duck work.",
    category=ItemCategory.FURNITURE, rarity=ItemRarity.RARE,
    cost=400, unlock_level=5, unlock_xp=500, size="medium",
    interaction_text=["*scribbles notes*", "*quill scratching sounds*"]
))

register_item(ShopItem(
    id="piano", name="Grand Piano", description="Tickle those ivories!",
    category=ItemCategory.FURNITURE, rarity=ItemRarity.EPIC,
    cost=1200, unlock_level=10, unlock_xp=3000, size="large", animated=True,
    interaction_text=["*plays Moonlight Quackata*", "*dramatic musical flourish*"]
))

register_item(ShopItem(
    id="wardrobe", name="Wardrobe", description="Narnia might be in there.",
    category=ItemCategory.FURNITURE, rarity=ItemRarity.RARE,
    cost=500, unlock_level=6, unlock_xp=800, size="large",
    interaction_text=["*checks for Narnia*", "Just coats..."]
))

register_item(ShopItem(
    id="sofa_fancy", name="Fancy Sofa", description="Luxurious velvet sofa.",
    category=ItemCategory.FURNITURE, rarity=ItemRarity.EPIC,
    cost=800, unlock_level=8, unlock_xp=1500, size="large",
    interaction_text=["*lounges dramatically*", "This is the life!"]
))

register_item(ShopItem(
    id="coffee_table", name="Coffee Table", description="Perfect for magazines.",
    category=ItemCategory.FURNITURE, rarity=ItemRarity.COMMON,
    cost=150, unlock_level=2, unlock_xp=50, size="medium",
    interaction_text=["*puts feet up*", "*reads Duck Weekly*"]
))

register_item(ShopItem(
    id="bar_cart", name="Bar Cart", description="For sophisticated gatherings.",
    category=ItemCategory.FURNITURE, rarity=ItemRarity.RARE,
    cost=450, unlock_level=7, unlock_xp=1200, size="medium",
    interaction_text=["*mixes drink*", "Shaken, not quacked!"]
))

register_item(ShopItem(
    id="grandfather_clock", name="Grandfather Clock", description="Tick tock, duck o'clock.",
    category=ItemCategory.FURNITURE, rarity=ItemRarity.EPIC,
    cost=1000, unlock_level=9, unlock_xp=2000, size="large", animated=True,
    interaction_text=["*BONG BONG*", "What time is it? Quack-thirty!"]
))

register_item(ShopItem(
    id="rocking_horse", name="Rocking Horse", description="Giddyup!",
    category=ItemCategory.FURNITURE, rarity=ItemRarity.UNCOMMON,
    cost=220, unlock_level=4, unlock_xp=300, size="medium", animated=True,
    interaction_text=["*rocks back and forth*", "YEE-HAW!"]
))

register_item(ShopItem(
    id="cabinet", name="Display Cabinet", description="Show off treasures.",
    category=ItemCategory.FURNITURE, rarity=ItemRarity.UNCOMMON,
    cost=280, unlock_level=5, unlock_xp=500, size="medium",
    interaction_text=["*polishes glass*", "My precious collectibles!"]
))

register_item(ShopItem(
    id="fireplace", name="Stone Fireplace", description="Cozy warmth.",
    category=ItemCategory.FURNITURE, rarity=ItemRarity.LEGENDARY,
    cost=2000, unlock_level=12, unlock_xp=5000, size="large", animated=True,
    interaction_text=["*warms by fire*", "*crackle crackle*"]
))

register_item(ShopItem(
    id="tv_stand", name="TV Stand", description="For entertainment center.",
    category=ItemCategory.FURNITURE, rarity=ItemRarity.UNCOMMON,
    cost=250, unlock_level=4, unlock_xp=300, size="medium",
    interaction_text=["*channel surfing*", "Duck Dynasty is on!"]
))

register_item(ShopItem(
    id="bean_bag", name="Giant Bean Bag", description="Ultimate comfort.",
    category=ItemCategory.FURNITURE, rarity=ItemRarity.RARE,
    cost=350, unlock_level=5, unlock_xp=500, size="large",
    interaction_text=["*sinks in*", "*contented sigh*"]
))

# ============ MORE WATER FEATURES (5 more) ============
register_item(ShopItem(
    id="koi_pond", name="Koi Pond", description="Beautiful fish friends!",
    category=ItemCategory.WATER, rarity=ItemRarity.EPIC,
    cost=1100, unlock_level=10, unlock_xp=3000, size="large", animated=True,
    interaction_text=["*watches fish*", "Hello, fishy friends!"]
))

register_item(ShopItem(
    id="waterfall_mini", name="Mini Waterfall", description="Soothing water sounds.",
    category=ItemCategory.WATER, rarity=ItemRarity.LEGENDARY,
    cost=2500, unlock_level=13, unlock_xp=7000, size="large", animated=True,
    interaction_text=["*splish splash*", "So peaceful..."]
))

register_item(ShopItem(
    id="hot_tub_deluxe", name="Hot Tub", description="Relaxation station!",
    category=ItemCategory.WATER, rarity=ItemRarity.EPIC,
    cost=1500, unlock_level=11, unlock_xp=4000, size="large", animated=True,
    interaction_text=["*bubbles everywhere*", "Ahhhhh, this is nice!"]
))

register_item(ShopItem(
    id="water_slide_mega", name="Water Slide", description="WHEEE down the slide!",
    category=ItemCategory.WATER, rarity=ItemRarity.LEGENDARY,
    cost=3000, unlock_level=15, unlock_xp=10000, size="large", animated=True,
    interaction_text=["WHEEEEE!", "*splash at bottom*"]
))

register_item(ShopItem(
    id="sprinkler_system", name="Sprinkler System", description="Cool off in summer!",
    category=ItemCategory.WATER, rarity=ItemRarity.UNCOMMON,
    cost=200, unlock_level=3, unlock_xp=150, size="small", animated=True,
    interaction_text=["*runs through spray*", "*refreshing quack*"]
))

# ============ MORE PLANTS (10 more) ============
register_item(ShopItem(
    id="bonsai", name="Bonsai Tree", description="Miniature zen tree.",
    category=ItemCategory.PLANT, rarity=ItemRarity.UNCOMMON,
    cost=180, unlock_level=3, unlock_xp=150, size="small",
    interaction_text=["*trims carefully*", "The art of patience..."]
))

register_item(ShopItem(
    id="venus_flytrap", name="Venus Flytrap", description="Don't stick your beak in!",
    category=ItemCategory.PLANT, rarity=ItemRarity.RARE,
    cost=350, unlock_level=6, unlock_xp=800, size="small", animated=True,
    interaction_text=["*CHOMP*", "Hey! That almost got me!"]
))

register_item(ShopItem(
    id="herb_garden", name="Herb Garden", description="Fresh herbs for cooking.",
    category=ItemCategory.PLANT, rarity=ItemRarity.UNCOMMON,
    cost=200, unlock_level=4, unlock_xp=300, size="medium",
    interaction_text=["*sniffs basil*", "Smells delicious!"]
))

register_item(ShopItem(
    id="cherry_tree", name="Cherry Blossom Tree", description="Beautiful pink blossoms.",
    category=ItemCategory.PLANT, rarity=ItemRarity.EPIC,
    cost=1000, unlock_level=9, unlock_xp=2000, size="large", animated=True,
    interaction_text=["*petals fall*", "So beautiful!"]
))

register_item(ShopItem(
    id="willow_tree", name="Weeping Willow", description="Graceful drooping branches.",
    category=ItemCategory.PLANT, rarity=ItemRarity.EPIC,
    cost=900, unlock_level=8, unlock_xp=1500, size="large",
    interaction_text=["*hides under branches*", "My secret spot!"]
))

register_item(ShopItem(
    id="mushroom_patch", name="Mushroom Patch", description="Cute toadstools.",
    category=ItemCategory.PLANT, rarity=ItemRarity.UNCOMMON,
    cost=150, unlock_level=3, unlock_xp=150, size="small",
    interaction_text=["*examines mushrooms*", "Are these edible?"]
))

register_item(ShopItem(
    id="topiary_duck", name="Duck Topiary", description="A bush shaped like... you!",
    category=ItemCategory.PLANT, rarity=ItemRarity.RARE,
    cost=600, unlock_level=7, unlock_xp=1200, size="medium",
    interaction_text=["*stares at bush-self*", "Looking good, other me!"]
))

register_item(ShopItem(
    id="fern", name="Potted Fern", description="Lush green fern.",
    category=ItemCategory.PLANT, rarity=ItemRarity.COMMON,
    cost=80, unlock_level=1, unlock_xp=0, size="small",
    interaction_text=["*rustles leaves*", "Nature is neat!"]
))

register_item(ShopItem(
    id="lavender", name="Lavender Bush", description="Calming purple flowers.",
    category=ItemCategory.PLANT, rarity=ItemRarity.UNCOMMON,
    cost=120, unlock_level=2, unlock_xp=50, size="small",
    interaction_text=["*deep breath*", "So relaxing..."]
))

register_item(ShopItem(
    id="hedge_maze", name="Hedge Maze", description="Get lost in the maze!",
    category=ItemCategory.PLANT, rarity=ItemRarity.LEGENDARY,
    cost=2000, unlock_level=13, unlock_xp=7000, size="large",
    interaction_text=["*wanders around*", "I'm lost... again!"]
))

# ============ STRUCTURE ITEMS (20 items) ============
register_item(ShopItem(
    id="dog_house", name="Duck House", description="A cozy little house.",
    category=ItemCategory.STRUCTURE, rarity=ItemRarity.UNCOMMON,
    cost=300, unlock_level=3, unlock_xp=150, size="large",
    interaction_text=["*enters house*", "Home sweet home!"]
))

register_item(ShopItem(
    id="picket_fence", name="Picket Fence", description="White picket fence section.",
    category=ItemCategory.STRUCTURE, rarity=ItemRarity.COMMON,
    cost=100, unlock_level=2, unlock_xp=50, size="medium",
    interaction_text=["*hops over fence*", "Can't contain me!"]
))

register_item(ShopItem(
    id="stone_wall", name="Stone Wall", description="Sturdy stone wall section.",
    category=ItemCategory.STRUCTURE, rarity=ItemRarity.UNCOMMON,
    cost=200, unlock_level=3, unlock_xp=150, size="medium",
    interaction_text=["*taps wall*", "Solid construction!"]
))

register_item(ShopItem(
    id="archway", name="Garden Archway", description="Elegant garden arch.",
    category=ItemCategory.STRUCTURE, rarity=ItemRarity.RARE,
    cost=450, unlock_level=5, unlock_xp=500, size="large",
    interaction_text=["*walks through*", "So fancy!"]
))

register_item(ShopItem(
    id="gazebo", name="Wooden Gazebo", description="Peaceful garden gazebo.",
    category=ItemCategory.STRUCTURE, rarity=ItemRarity.EPIC,
    cost=1200, unlock_level=10, unlock_xp=3000, size="large",
    interaction_text=["*sits in gazebo*", "What a view!"]
))

register_item(ShopItem(
    id="bridge", name="Wooden Bridge", description="Crosses over water.",
    category=ItemCategory.STRUCTURE, rarity=ItemRarity.RARE,
    cost=600, unlock_level=7, unlock_xp=1200, size="large",
    interaction_text=["*crosses bridge*", "*clack clack clack*"]
))

register_item(ShopItem(
    id="tower", name="Watch Tower", description="Survey your domain!",
    category=ItemCategory.STRUCTURE, rarity=ItemRarity.EPIC,
    cost=1500, unlock_level=11, unlock_xp=4000, size="large",
    interaction_text=["*climbs to top*", "I can see everything!"]
))

register_item(ShopItem(
    id="windmill", name="Windmill", description="Classic spinning windmill.",
    category=ItemCategory.STRUCTURE, rarity=ItemRarity.LEGENDARY,
    cost=2500, unlock_level=13, unlock_xp=7000, size="large", animated=True,
    interaction_text=["*blades spin*", "*whoosh whoosh*"]
))

register_item(ShopItem(
    id="gate", name="Garden Gate", description="Ornate iron gate.",
    category=ItemCategory.STRUCTURE, rarity=ItemRarity.UNCOMMON,
    cost=180, unlock_level=3, unlock_xp=150, size="medium",
    interaction_text=["*creaky sounds*", "*waddles through*"]
))

register_item(ShopItem(
    id="pergola", name="Pergola", description="Vine-covered pergola.",
    category=ItemCategory.STRUCTURE, rarity=ItemRarity.RARE,
    cost=700, unlock_level=8, unlock_xp=1500, size="large",
    interaction_text=["*relaxes underneath*", "Perfect shade!"]
))

register_item(ShopItem(
    id="shed", name="Garden Shed", description="For storage and tools.",
    category=ItemCategory.STRUCTURE, rarity=ItemRarity.UNCOMMON,
    cost=350, unlock_level=4, unlock_xp=300, size="large",
    interaction_text=["*rummages inside*", "Where's my shovel?"]
))

register_item(ShopItem(
    id="treehouse", name="Treehouse", description="Duck fortress in the trees!",
    category=ItemCategory.STRUCTURE, rarity=ItemRarity.EPIC,
    cost=1800, unlock_level=12, unlock_xp=5000, size="large",
    interaction_text=["*climbs up*", "No grown-ups allowed!"]
))

register_item(ShopItem(
    id="birdhouse", name="Fancy Birdhouse", description="Ironic housing for birds.",
    category=ItemCategory.STRUCTURE, rarity=ItemRarity.COMMON,
    cost=120, unlock_level=2, unlock_xp=50, size="small",
    interaction_text=["*peers inside*", "Anyone home?"]
))

register_item(ShopItem(
    id="mailbox", name="Mailbox", description="You've got quail mail!",
    category=ItemCategory.STRUCTURE, rarity=ItemRarity.COMMON,
    cost=80, unlock_level=1, unlock_xp=0, size="small",
    interaction_text=["*checks mail*", "Bills, bills, bills..."]
))

register_item(ShopItem(
    id="wishing_well", name="Wishing Well", description="Make a wish!",
    category=ItemCategory.STRUCTURE, rarity=ItemRarity.RARE,
    cost=800, unlock_level=8, unlock_xp=1500, size="medium",
    interaction_text=["*tosses coin*", "I wish for more bread!"]
))

register_item(ShopItem(
    id="trellis", name="Rose Trellis", description="Climbing roses on lattice.",
    category=ItemCategory.STRUCTURE, rarity=ItemRarity.UNCOMMON,
    cost=220, unlock_level=4, unlock_xp=300, size="medium",
    interaction_text=["*smells roses*", "Watch the thorns!"]
))

register_item(ShopItem(
    id="greenhouse", name="Greenhouse", description="Grow plants year-round.",
    category=ItemCategory.STRUCTURE, rarity=ItemRarity.EPIC,
    cost=1400, unlock_level=11, unlock_xp=4000, size="large",
    interaction_text=["*waters plants*", "Look at them grow!"]
))

register_item(ShopItem(
    id="castle_tower", name="Castle Tower", description="Medieval stone tower.",
    category=ItemCategory.STRUCTURE, rarity=ItemRarity.LEGENDARY,
    cost=3000, unlock_level=15, unlock_xp=10000, size="large",
    interaction_text=["*feels majestic*", "My castle!"]
))

register_item(ShopItem(
    id="barn", name="Red Barn", description="Classic red barn.",
    category=ItemCategory.STRUCTURE, rarity=ItemRarity.RARE,
    cost=900, unlock_level=9, unlock_xp=2000, size="large",
    interaction_text=["*explores barn*", "E-I-E-I-QUACK!"]
))

register_item(ShopItem(
    id="fence_section", name="Iron Fence", description="Decorative iron fence.",
    category=ItemCategory.STRUCTURE, rarity=ItemRarity.UNCOMMON,
    cost=150, unlock_level=2, unlock_xp=50, size="medium",
    interaction_text=["*rattles bars*", "Nice and secure!"]
))

# ============ DECORATION ITEMS (30 items) ============
register_item(ShopItem(
    id="garden_gnome", name="Garden Gnome", description="Creepy little guy.",
    category=ItemCategory.DECORATION, rarity=ItemRarity.COMMON,
    cost=100, unlock_level=1, unlock_xp=0, size="small",
    interaction_text=["*stares at gnome*", "Is it... watching me?"]
))

register_item(ShopItem(
    id="duck_statue", name="Duck Statue", description="A statue of... you!",
    category=ItemCategory.DECORATION, rarity=ItemRarity.RARE,
    cost=500, unlock_level=6, unlock_xp=800, size="medium",
    interaction_text=["*strikes same pose*", "Nailed it!"]
))

register_item(ShopItem(
    id="fountain_statue", name="Fountain Statue", description="Classical marble statue.",
    category=ItemCategory.DECORATION, rarity=ItemRarity.EPIC,
    cost=1000, unlock_level=9, unlock_xp=2000, size="large",
    interaction_text=["*admires art*", "Such culture!"]
))

register_item(ShopItem(
    id="wind_chimes", name="Wind Chimes", description="Tinkle in the breeze.",
    category=ItemCategory.DECORATION, rarity=ItemRarity.COMMON,
    cost=80, unlock_level=1, unlock_xp=0, size="small", animated=True,
    interaction_text=["*ting ting ting*", "Peaceful sounds..."]
))

register_item(ShopItem(
    id="birdbath_garden", name="Birdbath", description="For your bird friends.",
    category=ItemCategory.DECORATION, rarity=ItemRarity.COMMON,
    cost=120, unlock_level=2, unlock_xp=50, size="small",
    interaction_text=["*splashes*", "Also a duckbath!"]
))

register_item(ShopItem(
    id="sundial", name="Sundial", description="Tell time by the sun.",
    category=ItemCategory.DECORATION, rarity=ItemRarity.UNCOMMON,
    cost=200, unlock_level=3, unlock_xp=150, size="small",
    interaction_text=["*checks time*", "It's... daytime!"]
))

register_item(ShopItem(
    id="weather_vane", name="Weather Vane", description="Shows wind direction.",
    category=ItemCategory.DECORATION, rarity=ItemRarity.UNCOMMON,
    cost=180, unlock_level=3, unlock_xp=150, size="medium", animated=True,
    interaction_text=["*spins around*", "Windy today!"]
))

register_item(ShopItem(
    id="flag_pole", name="Flag Pole", description="Fly your colors!",
    category=ItemCategory.DECORATION, rarity=ItemRarity.UNCOMMON,
    cost=220, unlock_level=4, unlock_xp=300, size="medium", animated=True,
    interaction_text=["*salutes*", "*flag flaps*"]
))

register_item(ShopItem(
    id="tire_swing", name="Tire Swing", description="Classic backyard fun!",
    category=ItemCategory.DECORATION, rarity=ItemRarity.UNCOMMON,
    cost=150, unlock_level=3, unlock_xp=150, size="medium", animated=True,
    interaction_text=["*swings back and forth*", "WHEEE!"]
))

register_item(ShopItem(
    id="hammock", name="Hammock", description="Perfect for napping.",
    category=ItemCategory.DECORATION, rarity=ItemRarity.RARE,
    cost=350, unlock_level=5, unlock_xp=500, size="medium",
    interaction_text=["*sways gently*", "*snooze*"]
))

register_item(ShopItem(
    id="scarecrow", name="Scarecrow", description="Keeps the... other birds away?",
    category=ItemCategory.DECORATION, rarity=ItemRarity.UNCOMMON,
    cost=180, unlock_level=3, unlock_xp=150, size="medium",
    interaction_text=["*befriends scarecrow*", "You're not so scary!"]
))

register_item(ShopItem(
    id="totem_pole", name="Totem Pole", description="Carved wooden totem.",
    category=ItemCategory.DECORATION, rarity=ItemRarity.RARE,
    cost=600, unlock_level=7, unlock_xp=1200, size="large",
    interaction_text=["*studies carvings*", "Ancient duck wisdom!"]
))

register_item(ShopItem(
    id="welcome_mat", name="Welcome Mat", description="Says 'QUACK-ome!'",
    category=ItemCategory.DECORATION, rarity=ItemRarity.COMMON,
    cost=60, unlock_level=1, unlock_xp=0, size="small",
    interaction_text=["*wipes feet*", "So polite!"]
))

register_item(ShopItem(
    id="potted_cactus", name="Decorative Cactus", description="Don't hug!",
    category=ItemCategory.DECORATION, rarity=ItemRarity.COMMON,
    cost=90, unlock_level=1, unlock_xp=0, size="small",
    interaction_text=["*pokes*", "OW!"]
))

register_item(ShopItem(
    id="stepping_stones", name="Stepping Stones", description="Path across the grass.",
    category=ItemCategory.DECORATION, rarity=ItemRarity.UNCOMMON,
    cost=150, unlock_level=2, unlock_xp=50, size="medium",
    interaction_text=["*hops along*", "Step step step!"]
))

register_item(ShopItem(
    id="garden_bench", name="Park Bench", description="Sit and relax.",
    category=ItemCategory.DECORATION, rarity=ItemRarity.UNCOMMON,
    cost=200, unlock_level=3, unlock_xp=150, size="medium",
    interaction_text=["*sits down*", "Nice day for it!"]
))

register_item(ShopItem(
    id="fountain_decorative", name="Small Fountain", description="Trickling water feature.",
    category=ItemCategory.DECORATION, rarity=ItemRarity.RARE,
    cost=400, unlock_level=5, unlock_xp=500, size="medium", animated=True,
    interaction_text=["*splish splash*", "So soothing!"]
))

register_item(ShopItem(
    id="zen_garden", name="Zen Garden", description="Rake the sand, find peace.",
    category=ItemCategory.DECORATION, rarity=ItemRarity.RARE,
    cost=550, unlock_level=7, unlock_xp=1200, size="medium",
    interaction_text=["*rakes patterns*", "*inner peace*"]
))

register_item(ShopItem(
    id="fairy_lights", name="String Lights", description="Twinkly lights on string.",
    category=ItemCategory.DECORATION, rarity=ItemRarity.UNCOMMON,
    cost=180, unlock_level=3, unlock_xp=150, size="medium", animated=True,
    interaction_text=["*twinkle twinkle*", "So pretty!"]
))

register_item(ShopItem(
    id="pinwheel", name="Pinwheel", description="Spins in the wind!",
    category=ItemCategory.DECORATION, rarity=ItemRarity.COMMON,
    cost=70, unlock_level=1, unlock_xp=0, size="small", animated=True,
    interaction_text=["*spins rapidly*", "*mesmerized*"]
))

register_item(ShopItem(
    id="rain_barrel", name="Rain Barrel", description="Collects rainwater.",
    category=ItemCategory.DECORATION, rarity=ItemRarity.COMMON,
    cost=100, unlock_level=2, unlock_xp=50, size="small",
    interaction_text=["*checks water level*", "Almost full!"]
))

register_item(ShopItem(
    id="wheelbarrow", name="Wheelbarrow", description="For garden work.",
    category=ItemCategory.DECORATION, rarity=ItemRarity.COMMON,
    cost=110, unlock_level=2, unlock_xp=50, size="small",
    interaction_text=["*pushes around*", "*squeaky wheel*"]
))

register_item(ShopItem(
    id="tiki_torch", name="Tiki Torch", description="Island vibes!",
    category=ItemCategory.DECORATION, rarity=ItemRarity.UNCOMMON,
    cost=150, unlock_level=3, unlock_xp=150, size="small", animated=True,
    interaction_text=["*flame flickers*", "Aloha!"]
))

register_item(ShopItem(
    id="ice_sculpture", name="Ice Sculpture", description="Beautiful but melting!",
    category=ItemCategory.DECORATION, rarity=ItemRarity.EPIC,
    cost=800, unlock_level=8, unlock_xp=1500, size="medium", animated=True,
    interaction_text=["*drip drip*", "Enjoy it while it lasts!"]
))

register_item(ShopItem(
    id="trophy_case", name="Trophy Case", description="Display your achievements!",
    category=ItemCategory.DECORATION, rarity=ItemRarity.RARE,
    cost=450, unlock_level=6, unlock_xp=800, size="medium",
    interaction_text=["*polishes trophies*", "Look at all I've done!"]
))

register_item(ShopItem(
    id="compass_rose", name="Compass Rose", description="Decorative floor compass.",
    category=ItemCategory.DECORATION, rarity=ItemRarity.UNCOMMON,
    cost=200, unlock_level=4, unlock_xp=300, size="small",
    interaction_text=["*spins around*", "North! South! East! West!"]
))

register_item(ShopItem(
    id="sand_castle", name="Sand Castle", description="Beach vibes!",
    category=ItemCategory.DECORATION, rarity=ItemRarity.UNCOMMON,
    cost=180, unlock_level=3, unlock_xp=150, size="medium",
    interaction_text=["*adds flag*", "My sandy kingdom!"]
))

register_item(ShopItem(
    id="gong", name="Meditation Gong", description="BONG!",
    category=ItemCategory.DECORATION, rarity=ItemRarity.RARE,
    cost=500, unlock_level=6, unlock_xp=800, size="medium", animated=True,
    interaction_text=["*strikes gong*", "BONNNNNG!"]
))

register_item(ShopItem(
    id="bubble_machine", name="Bubble Machine", description="Bubbles everywhere!",
    category=ItemCategory.DECORATION, rarity=ItemRarity.RARE,
    cost=400, unlock_level=5, unlock_xp=500, size="small", animated=True,
    interaction_text=["*pop pop pop*", "Catch the bubbles!"]
))

register_item(ShopItem(
    id="snow_globe", name="Giant Snow Globe", description="Winter wonderland inside!",
    category=ItemCategory.DECORATION, rarity=ItemRarity.EPIC,
    cost=900, unlock_level=9, unlock_xp=2000, size="medium", animated=True,
    interaction_text=["*shakes globe*", "It's snowing!"]
))

# ============ LIGHTING ITEMS (20 items) ============
register_item(ShopItem(
    id="table_lamp", name="Table Lamp", description="Classic table lamp.",
    category=ItemCategory.LIGHTING, rarity=ItemRarity.COMMON,
    cost=80, unlock_level=1, unlock_xp=0, size="small", animated=True,
    interaction_text=["*flicks switch*", "Let there be light!"]
))

register_item(ShopItem(
    id="floor_lamp", name="Floor Lamp", description="Tall standing lamp.",
    category=ItemCategory.LIGHTING, rarity=ItemRarity.COMMON,
    cost=120, unlock_level=2, unlock_xp=50, size="small", animated=True,
    interaction_text=["*adjusts shade*", "Perfect lighting!"]
))

register_item(ShopItem(
    id="chandelier", name="Crystal Chandelier", description="Fancy hanging chandelier.",
    category=ItemCategory.LIGHTING, rarity=ItemRarity.EPIC,
    cost=1200, unlock_level=10, unlock_xp=3000, size="large", animated=True,
    interaction_text=["*sparkle sparkle*", "So glamorous!"]
))

register_item(ShopItem(
    id="paper_lantern", name="Paper Lantern", description="Soft glowing lantern.",
    category=ItemCategory.LIGHTING, rarity=ItemRarity.UNCOMMON,
    cost=100, unlock_level=2, unlock_xp=50, size="small", animated=True,
    interaction_text=["*gentle glow*", "Peaceful ambiance!"]
))

register_item(ShopItem(
    id="lava_lamp", name="Lava Lamp", description="Groovy! Retro vibes!",
    category=ItemCategory.LIGHTING, rarity=ItemRarity.RARE,
    cost=350, unlock_level=5, unlock_xp=500, size="small", animated=True,
    interaction_text=["*blobs float*", "*mesmerized*"]
))

register_item(ShopItem(
    id="neon_sign", name="Neon Sign", description="Custom neon QUACK sign!",
    category=ItemCategory.LIGHTING, rarity=ItemRarity.EPIC,
    cost=800, unlock_level=8, unlock_xp=1500, size="medium", animated=True,
    interaction_text=["*buzzing sound*", "So bright!"]
))

register_item(ShopItem(
    id="disco_ball", name="Disco Ball", description="Party time!",
    category=ItemCategory.LIGHTING, rarity=ItemRarity.RARE,
    cost=500, unlock_level=6, unlock_xp=800, size="small", animated=True,
    interaction_text=["*spins and sparkles*", "*dance dance*"]
))

register_item(ShopItem(
    id="candelabra", name="Silver Candelabra", description="Elegant candle holder.",
    category=ItemCategory.LIGHTING, rarity=ItemRarity.UNCOMMON,
    cost=200, unlock_level=3, unlock_xp=150, size="small", animated=True,
    interaction_text=["*flames flicker*", "So fancy!"]
))

register_item(ShopItem(
    id="fairy_lamp", name="Fairy Light Jar", description="Captured fireflies! (fake)",
    category=ItemCategory.LIGHTING, rarity=ItemRarity.UNCOMMON,
    cost=150, unlock_level=3, unlock_xp=150, size="small", animated=True,
    interaction_text=["*twinkles*", "Magical!"]
))

register_item(ShopItem(
    id="spotlight", name="Stage Spotlight", description="You're in the spotlight!",
    category=ItemCategory.LIGHTING, rarity=ItemRarity.RARE,
    cost=450, unlock_level=6, unlock_xp=800, size="medium", animated=True,
    interaction_text=["*dramatic pose*", "All eyes on me!"]
))

register_item(ShopItem(
    id="street_lamp", name="Street Lamp", description="Old-fashioned lamp post.",
    category=ItemCategory.LIGHTING, rarity=ItemRarity.UNCOMMON,
    cost=250, unlock_level=4, unlock_xp=300, size="medium", animated=True,
    interaction_text=["*warm glow*", "Feels like home!"]
))

register_item(ShopItem(
    id="campfire", name="Campfire", description="Cozy crackling fire.",
    category=ItemCategory.LIGHTING, rarity=ItemRarity.UNCOMMON,
    cost=180, unlock_level=3, unlock_xp=150, size="small", animated=True,
    interaction_text=["*crackle pop*", "Time for s'mores!"]
))

register_item(ShopItem(
    id="lighthouse", name="Miniature Lighthouse", description="Guide the way!",
    category=ItemCategory.LIGHTING, rarity=ItemRarity.EPIC,
    cost=1100, unlock_level=10, unlock_xp=3000, size="large", animated=True,
    interaction_text=["*beacon spins*", "Don't crash into the rocks!"]
))

register_item(ShopItem(
    id="firefly_swarm", name="Firefly Swarm", description="Real fireflies!",
    category=ItemCategory.LIGHTING, rarity=ItemRarity.RARE,
    cost=600, unlock_level=7, unlock_xp=1200, size="medium", animated=True,
    interaction_text=["*blink blink*", "Catch them gently!"]
))

register_item(ShopItem(
    id="moon_lamp", name="Moon Lamp", description="Glowing moon replica.",
    category=ItemCategory.LIGHTING, rarity=ItemRarity.RARE,
    cost=400, unlock_level=5, unlock_xp=500, size="small", animated=True,
    interaction_text=["*lunar glow*", "My own moon!"]
))

register_item(ShopItem(
    id="star_projector", name="Star Projector", description="Projects night sky!",
    category=ItemCategory.LIGHTING, rarity=ItemRarity.EPIC,
    cost=900, unlock_level=9, unlock_xp=2000, size="small", animated=True,
    interaction_text=["*stars everywhere*", "It's beautiful!"]
))

register_item(ShopItem(
    id="torches", name="Wall Torches", description="Medieval torches.",
    category=ItemCategory.LIGHTING, rarity=ItemRarity.UNCOMMON,
    cost=150, unlock_level=3, unlock_xp=150, size="small", animated=True,
    interaction_text=["*flames dance*", "Dungeon vibes!"]
))

register_item(ShopItem(
    id="glowsticks", name="Glowstick Bundle", description="Rave duck!",
    category=ItemCategory.LIGHTING, rarity=ItemRarity.COMMON,
    cost=90, unlock_level=2, unlock_xp=50, size="small", animated=True,
    interaction_text=["*waves glowsticks*", "Untz untz untz!"]
))

register_item(ShopItem(
    id="aurora", name="Aurora Projector", description="Northern lights indoors!",
    category=ItemCategory.LIGHTING, rarity=ItemRarity.LEGENDARY,
    cost=2000, unlock_level=13, unlock_xp=7000, size="medium", animated=True,
    interaction_text=["*colors dance*", "So mesmerizing!"]
))

register_item(ShopItem(
    id="laser_lights", name="Laser Light Show", description="Pew pew lights!",
    category=ItemCategory.LIGHTING, rarity=ItemRarity.EPIC,
    cost=1000, unlock_level=9, unlock_xp=2000, size="medium", animated=True,
    interaction_text=["*pew pew pew*", "Light show!"]
))

# ============ FLOORING ITEMS (20 items) ============
register_item(ShopItem(
    id="grass_floor", name="Grass Patch", description="Soft green grass.",
    category=ItemCategory.FLOORING, rarity=ItemRarity.COMMON,
    cost=50, unlock_level=1, unlock_xp=0, size="medium",
    interaction_text=["*lies on grass*", "So comfy!"]
))

register_item(ShopItem(
    id="wooden_planks", name="Wooden Planks", description="Rustic wood flooring.",
    category=ItemCategory.FLOORING, rarity=ItemRarity.COMMON,
    cost=80, unlock_level=1, unlock_xp=0, size="medium",
    interaction_text=["*tap tap*", "Nice and sturdy!"]
))

register_item(ShopItem(
    id="marble_tiles", name="Marble Tiles", description="Elegant marble flooring.",
    category=ItemCategory.FLOORING, rarity=ItemRarity.EPIC,
    cost=1000, unlock_level=9, unlock_xp=2000, size="medium",
    interaction_text=["*slides across*", "So smooth!"]
))

register_item(ShopItem(
    id="carpet_red", name="Red Carpet", description="VIP treatment!",
    category=ItemCategory.FLOORING, rarity=ItemRarity.UNCOMMON,
    cost=200, unlock_level=3, unlock_xp=150, size="medium",
    interaction_text=["*struts down carpet*", "Celebrity duck!"]
))

register_item(ShopItem(
    id="tatami_mat", name="Tatami Mat", description="Traditional Japanese mat.",
    category=ItemCategory.FLOORING, rarity=ItemRarity.UNCOMMON,
    cost=180, unlock_level=3, unlock_xp=150, size="medium",
    interaction_text=["*bows*", "Very zen!"]
))

register_item(ShopItem(
    id="sand_floor", name="Sand Floor", description="Beach vibes!",
    category=ItemCategory.FLOORING, rarity=ItemRarity.COMMON,
    cost=70, unlock_level=1, unlock_xp=0, size="medium",
    interaction_text=["*digs in sand*", "Where's my bucket?"]
))

register_item(ShopItem(
    id="stone_tiles", name="Stone Tiles", description="Cold stone flooring.",
    category=ItemCategory.FLOORING, rarity=ItemRarity.UNCOMMON,
    cost=150, unlock_level=2, unlock_xp=50, size="medium",
    interaction_text=["*feet get cold*", "Brr!"]
))

register_item(ShopItem(
    id="checkered_floor", name="Checkered Floor", description="Black and white pattern.",
    category=ItemCategory.FLOORING, rarity=ItemRarity.UNCOMMON,
    cost=200, unlock_level=3, unlock_xp=150, size="medium",
    interaction_text=["*hops on squares*", "Don't step on the cracks!"]
))

register_item(ShopItem(
    id="mosaic_tiles", name="Mosaic Tiles", description="Colorful mosaic pattern.",
    category=ItemCategory.FLOORING, rarity=ItemRarity.RARE,
    cost=500, unlock_level=6, unlock_xp=800, size="medium",
    interaction_text=["*admires pattern*", "So artistic!"]
))

register_item(ShopItem(
    id="ice_floor", name="Ice Floor", description="Super slippery!",
    category=ItemCategory.FLOORING, rarity=ItemRarity.RARE,
    cost=450, unlock_level=6, unlock_xp=800, size="medium", animated=True,
    interaction_text=["*slip slip*", "WHOA!"]
))

register_item(ShopItem(
    id="cobblestone", name="Cobblestone Path", description="Medieval cobblestone.",
    category=ItemCategory.FLOORING, rarity=ItemRarity.UNCOMMON,
    cost=180, unlock_level=3, unlock_xp=150, size="medium",
    interaction_text=["*waddles on stones*", "Bumpy!"]
))

register_item(ShopItem(
    id="lava_floor", name="Lava Floor", description="HOT! Don't actually touch!",
    category=ItemCategory.FLOORING, rarity=ItemRarity.LEGENDARY,
    cost=2500, unlock_level=14, unlock_xp=8000, size="medium", animated=True,
    interaction_text=["*hovers nervously*", "THE FLOOR IS LAVA!"]
))

register_item(ShopItem(
    id="cloud_floor", name="Cloud Floor", description="Walk on clouds!",
    category=ItemCategory.FLOORING, rarity=ItemRarity.LEGENDARY,
    cost=2000, unlock_level=13, unlock_xp=7000, size="medium", animated=True,
    interaction_text=["*bounces softly*", "Heaven!"]
))

register_item(ShopItem(
    id="persian_rug", name="Persian Rug", description="Luxurious antique rug.",
    category=ItemCategory.FLOORING, rarity=ItemRarity.EPIC,
    cost=900, unlock_level=8, unlock_xp=1500, size="medium",
    interaction_text=["*appreciates craftsmanship*", "Exquisite!"]
))

register_item(ShopItem(
    id="rainbow_path", name="Rainbow Path", description="Colorful rainbow walkway.",
    category=ItemCategory.FLOORING, rarity=ItemRarity.RARE,
    cost=600, unlock_level=7, unlock_xp=1200, size="medium", animated=True,
    interaction_text=["*prances on rainbow*", "Taste the rainbow!"]
))

register_item(ShopItem(
    id="glass_floor", name="Glass Floor", description="See-through floor!",
    category=ItemCategory.FLOORING, rarity=ItemRarity.EPIC,
    cost=1100, unlock_level=10, unlock_xp=3000, size="medium",
    interaction_text=["*looks down*", "Don't look down!"]
))

register_item(ShopItem(
    id="rubber_mat", name="Rubber Mat", description="Bouncy safety mat.",
    category=ItemCategory.FLOORING, rarity=ItemRarity.COMMON,
    cost=100, unlock_level=2, unlock_xp=50, size="medium",
    interaction_text=["*bounce bounce*", "Wheee!"]
))

register_item(ShopItem(
    id="autumn_leaves", name="Autumn Leaf Pile", description="Crunchy leaves!",
    category=ItemCategory.FLOORING, rarity=ItemRarity.UNCOMMON,
    cost=120, unlock_level=2, unlock_xp=50, size="medium",
    interaction_text=["*crunch crunch*", "*jumps in pile*"]
))

register_item(ShopItem(
    id="snow_floor", name="Snow Floor", description="Fresh white snow.",
    category=ItemCategory.FLOORING, rarity=ItemRarity.UNCOMMON,
    cost=150, unlock_level=3, unlock_xp=150, size="medium",
    interaction_text=["*makes snow angels*", "Cold but fun!"]
))

register_item(ShopItem(
    id="galaxy_floor", name="Galaxy Floor", description="Stars beneath your feet!",
    category=ItemCategory.FLOORING, rarity=ItemRarity.LEGENDARY,
    cost=3000, unlock_level=15, unlock_xp=10000, size="medium", animated=True,
    interaction_text=["*walks on stars*", "I'm in space!"]
))

# ============ SPECIAL ITEMS (40 items) ============
register_item(ShopItem(
    id="portal", name="Magic Portal", description="Where does it lead?",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.LEGENDARY,
    cost=3000, unlock_level=15, unlock_xp=10000, size="large", animated=True,
    interaction_text=["*steps through portal*", "WOAH! Different dimension!"]
))

register_item(ShopItem(
    id="time_machine", name="Time Machine", description="Travel through time!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.LEGENDARY,
    cost=5000, unlock_level=20, unlock_xp=20000, size="large", animated=True,
    interaction_text=["*whirring sounds*", "To the future!"]
))

register_item(ShopItem(
    id="rainbow_generator", name="Rainbow Generator", description="Makes rainbows appear!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.EPIC,
    cost=1500, unlock_level=11, unlock_xp=4000, size="medium", animated=True,
    interaction_text=["*rainbow appears*", "Double rainbow!"]
))

register_item(ShopItem(
    id="weather_machine", name="Weather Machine", description="Control the weather!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.LEGENDARY,
    cost=4000, unlock_level=18, unlock_xp=15000, size="large", animated=True,
    interaction_text=["*dials to sunny*", "Perfect weather!"]
))

register_item(ShopItem(
    id="black_hole", name="Mini Black Hole", description="Totally safe! Probably.",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.LEGENDARY,
    cost=4500, unlock_level=19, unlock_xp=18000, size="medium", animated=True,
    interaction_text=["*gravity intensifies*", "Don't get too close!"]
))

register_item(ShopItem(
    id="volcano", name="Mini Volcano", description="It erupts sometimes!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.EPIC,
    cost=1800, unlock_level=12, unlock_xp=5000, size="large", animated=True,
    interaction_text=["*rumble rumble*", "Stand back!"]
))

register_item(ShopItem(
    id="antigravity", name="Anti-Gravity Zone", description="Float around!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.LEGENDARY,
    cost=3500, unlock_level=17, unlock_xp=12000, size="large", animated=True,
    interaction_text=["*floats upward*", "I can fly!"]
))

register_item(ShopItem(
    id="tornado", name="Pet Tornado", description="Tiny tornado friend!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.EPIC,
    cost=1600, unlock_level=11, unlock_xp=4000, size="medium", animated=True,
    interaction_text=["*whoooosh*", "Hold onto your feathers!"]
))

register_item(ShopItem(
    id="dragon_egg", name="Dragon Egg", description="Will it hatch?",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.LEGENDARY,
    cost=5000, unlock_level=20, unlock_xp=20000, size="medium", animated=True,
    interaction_text=["*egg wiggles*", "Something's in there!"]
))

register_item(ShopItem(
    id="treasure_chest", name="Treasure Chest", description="Full of gold!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.EPIC,
    cost=1200, unlock_level=10, unlock_xp=3000, size="medium", animated=True,
    interaction_text=["*opens chest*", "TREASURE!"]
))

register_item(ShopItem(
    id="magic_carpet", name="Flying Carpet", description="Aladdin style!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.EPIC,
    cost=1400, unlock_level=11, unlock_xp=4000, size="medium", animated=True,
    interaction_text=["*rides carpet*", "A whole new world!"]
))

register_item(ShopItem(
    id="crystal_ball", name="Crystal Ball", description="See the future!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.RARE,
    cost=800, unlock_level=8, unlock_xp=1500, size="small", animated=True,
    interaction_text=["*gazes into ball*", "I see... more bread!"]
))

register_item(ShopItem(
    id="wormhole", name="Wormhole", description="Shortcut through space!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.LEGENDARY,
    cost=4000, unlock_level=18, unlock_xp=15000, size="large", animated=True,
    interaction_text=["*swoooosh*", "Instant travel!"]
))

register_item(ShopItem(
    id="force_field", name="Force Field", description="Protected zone!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.EPIC,
    cost=1300, unlock_level=10, unlock_xp=3000, size="large", animated=True,
    interaction_text=["*shield activates*", "Nothing can hurt me!"]
))

register_item(ShopItem(
    id="teleporter", name="Teleporter Pad", description="Beam me up!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.LEGENDARY,
    cost=3500, unlock_level=16, unlock_xp=12000, size="medium", animated=True,
    interaction_text=["*sparkles*", "*materializes elsewhere*"]
))

register_item(ShopItem(
    id="robot_butler", name="Robot Butler", description="At your service!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.EPIC,
    cost=2000, unlock_level=13, unlock_xp=7000, size="medium", animated=True,
    interaction_text=["*beep boop*", "Tea is served, sir!"]
))

register_item(ShopItem(
    id="hologram", name="Hologram Projector", description="3D holographic images!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.EPIC,
    cost=1500, unlock_level=11, unlock_xp=4000, size="small", animated=True,
    interaction_text=["*projects hologram*", "Help me, Obi-Wan!"]
))

register_item(ShopItem(
    id="shrink_ray", name="Shrink Ray", description="Make things tiny!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.LEGENDARY,
    cost=3000, unlock_level=15, unlock_xp=10000, size="small", animated=True,
    interaction_text=["*zap*", "Everything's so big now!"]
))

register_item(ShopItem(
    id="growth_ray", name="Growth Ray", description="Make things HUGE!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.LEGENDARY,
    cost=3000, unlock_level=15, unlock_xp=10000, size="small", animated=True,
    interaction_text=["*ZAP*", "I'M ENORMOUS!"]
))

register_item(ShopItem(
    id="cloning_machine", name="Cloning Machine", description="Two ducks are better than one!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.LEGENDARY,
    cost=5000, unlock_level=20, unlock_xp=20000, size="large", animated=True,
    interaction_text=["*creates clone*", "There's two of me!"]
))

register_item(ShopItem(
    id="ufo", name="UFO", description="Alien spacecraft!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.LEGENDARY,
    cost=4500, unlock_level=19, unlock_xp=18000, size="large", animated=True,
    interaction_text=["*beams up*", "Take me to your leader!"]
))

register_item(ShopItem(
    id="rainbow_slide", name="Rainbow Slide", description="Slide down a rainbow!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.EPIC,
    cost=1800, unlock_level=12, unlock_xp=5000, size="large", animated=True,
    interaction_text=["*wheee down slide*", "WHEEEEE!"]
))

register_item(ShopItem(
    id="genie_lamp", name="Genie Lamp", description="Three wishes!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.LEGENDARY,
    cost=5000, unlock_level=20, unlock_xp=20000, size="small", animated=True,
    interaction_text=["*rubs lamp*", "Your wish is my command!"]
))

register_item(ShopItem(
    id="infinity_pool", name="Infinity Pool", description="Never-ending pool!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.LEGENDARY,
    cost=4000, unlock_level=18, unlock_xp=15000, size="large", animated=True,
    interaction_text=["*swims forever*", "No edges!"]
))

register_item(ShopItem(
    id="bounce_house", name="Bounce House", description="Inflatable bouncing fun!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.RARE,
    cost=700, unlock_level=7, unlock_xp=1200, size="large", animated=True,
    interaction_text=["*bounce bounce BOUNCE*", "WHEEE!"]
))

register_item(ShopItem(
    id="ferris_wheel", name="Ferris Wheel", description="Carnival ride!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.LEGENDARY,
    cost=3500, unlock_level=16, unlock_xp=12000, size="large", animated=True,
    interaction_text=["*spins slowly*", "What a view from up here!"]
))

register_item(ShopItem(
    id="carousel", name="Carousel", description="Merry-go-round!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.EPIC,
    cost=2000, unlock_level=13, unlock_xp=7000, size="large", animated=True,
    interaction_text=["*rides horse*", "*carousel music plays*"]
))

register_item(ShopItem(
    id="jetpack", name="Jetpack", description="FLY DUCK FLY!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.EPIC,
    cost=1800, unlock_level=12, unlock_xp=5000, size="small", animated=True,
    interaction_text=["*BLAST OFF*", "I'M FLYING!"]
))

register_item(ShopItem(
    id="submarine", name="Submarine", description="Underwater exploration!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.EPIC,
    cost=2200, unlock_level=14, unlock_xp=8000, size="large", animated=True,
    interaction_text=["*dive dive dive*", "20,000 leagues under!"]
))

register_item(ShopItem(
    id="hot_air_balloon", name="Hot Air Balloon", description="Float in the sky!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.EPIC,
    cost=1600, unlock_level=11, unlock_xp=4000, size="large", animated=True,
    interaction_text=["*floats upward*", "So peaceful up here!"]
))

register_item(ShopItem(
    id="rocket_ship", name="Rocket Ship", description="To the moon!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.LEGENDARY,
    cost=5000, unlock_level=20, unlock_xp=20000, size="large", animated=True,
    interaction_text=["*countdown 3...2...1*", "BLAST OFF!"]
))

register_item(ShopItem(
    id="tardis", name="Blue Police Box", description="Bigger on the inside!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.LEGENDARY,
    cost=4500, unlock_level=19, unlock_xp=18000, size="medium", animated=True,
    interaction_text=["*whoosh whoosh*", "Allons-y!"]
))

register_item(ShopItem(
    id="invisible_cloak", name="Invisibility Cloak", description="Can't see me!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.LEGENDARY,
    cost=3500, unlock_level=17, unlock_xp=12000, size="small", animated=True,
    interaction_text=["*disappears*", "Where did I go?"]
))

register_item(ShopItem(
    id="transmogrifier", name="Transmogrifier", description="Turn into anything!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.LEGENDARY,
    cost=4500, unlock_level=19, unlock_xp=18000, size="large", animated=True,
    interaction_text=["*ZAP*", "I'm a... toaster?"]
))

register_item(ShopItem(
    id="money_printer", name="Money Printer", description="Infinite coins! (balanced)",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.LEGENDARY,
    cost=10000, unlock_level=25, unlock_xp=50000, size="medium", animated=True,
    interaction_text=["*printing sounds*", "Cha-ching!"]
))

register_item(ShopItem(
    id="perpetual_motion", name="Perpetual Motion Machine", description="Never stops!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.LEGENDARY,
    cost=3500, unlock_level=17, unlock_xp=12000, size="medium", animated=True,
    interaction_text=["*spins endlessly*", "*mesmerized*"]
))

register_item(ShopItem(
    id="DNA_mixer", name="DNA Mixer", description="Combine DNA! Science!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.LEGENDARY,
    cost=4000, unlock_level=18, unlock_xp=15000, size="medium", animated=True,
    interaction_text=["*bubbles*", "What am I now?!"]
))

register_item(ShopItem(
    id="dream_catcher", name="Dream Catcher", description="Shows your dreams!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.EPIC,
    cost=1200, unlock_level=10, unlock_xp=3000, size="small", animated=True,
    interaction_text=["*dreams visualize*", "I dreamed of bread!"]
))

register_item(ShopItem(
    id="wish_fountain", name="Wishing Fountain", description="Every wish comes true!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.LEGENDARY,
    cost=5000, unlock_level=20, unlock_xp=20000, size="large", animated=True,
    interaction_text=["*tosses coin*", "*magic sparkles*"]
))

register_item(ShopItem(
    id="dimensional_door", name="Dimensional Door", description="Leads to another dimension!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.LEGENDARY,
    cost=4500, unlock_level=19, unlock_xp=18000, size="large", animated=True,
    interaction_text=["*opens door*", "What's on the other side?"]
))

# ============ BONUS LEGENDARY ITEMS (5 more to reach 255!) ============
register_item(ShopItem(
    id="golden_throne", name="Golden Throne", description="For the ultimate duck emperor!",
    category=ItemCategory.FURNITURE, rarity=ItemRarity.LEGENDARY,
    cost=5000, unlock_level=20, unlock_xp=20000, size="large",
    interaction_text=["*sits majestically*", "Bow before me!"]
))

register_item(ShopItem(
    id="world_tree", name="World Tree Yggdrasil", description="The tree that holds the universe!",
    category=ItemCategory.PLANT, rarity=ItemRarity.LEGENDARY,
    cost=5000, unlock_level=20, unlock_xp=20000, size="large", animated=True,
    interaction_text=["*touches trunk*", "I can feel the cosmos!"]
))

register_item(ShopItem(
    id="cosmic_arch", name="Cosmic Archway", description="Gateway to the stars!",
    category=ItemCategory.STRUCTURE, rarity=ItemRarity.LEGENDARY,
    cost=5000, unlock_level=20, unlock_xp=20000, size="large", animated=True,
    interaction_text=["*walks through*", "The universe awaits!"]
))

register_item(ShopItem(
    id="eternal_flame", name="Eternal Flame", description="Never goes out!",
    category=ItemCategory.LIGHTING, rarity=ItemRarity.LEGENDARY,
    cost=3500, unlock_level=17, unlock_xp=12000, size="small", animated=True,
    interaction_text=["*flames dance*", "It burns forever!"]
))

register_item(ShopItem(
    id="philosophers_stone", name="Philosopher's Stone", description="Legendary alchemical treasure!",
    category=ItemCategory.SPECIAL, rarity=ItemRarity.LEGENDARY,
    cost=10000, unlock_level=25, unlock_xp=50000, size="small", animated=True,
    interaction_text=["*glows mysteriously*", "The secret of immortality!"]
))


def get_items_by_category(category: ItemCategory) -> List[ShopItem]:
    """Get all items in a category, sorted by level requirement then price."""
    items = [item for item in SHOP_ITEMS.values() if item.category == category]
    # Sort by level requirement (ascending), then by price (ascending)
    return sorted(items, key=lambda x: (x.unlock_level, x.cost))


def get_items_by_rarity(rarity: ItemRarity) -> List[ShopItem]:
    """Get all items of a rarity tier, sorted by level requirement then price."""
    items = [item for item in SHOP_ITEMS.values() if item.rarity == rarity]
    return sorted(items, key=lambda x: (x.unlock_level, x.cost))


def get_affordable_items(currency: int, level: int) -> List[ShopItem]:
    """Get items the player can afford and has unlocked, sorted by price."""
    items = [item for item in SHOP_ITEMS.values() 
            if item.cost <= currency and item.unlock_level <= level]
    return sorted(items, key=lambda x: (x.unlock_level, x.cost))


def get_item(item_id: str) -> Optional[ShopItem]:
    """Get an item by ID."""
    return SHOP_ITEMS.get(item_id)
