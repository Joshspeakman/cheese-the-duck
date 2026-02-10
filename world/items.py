"""
Items and inventory system.
"""
from typing import Dict, List, Optional, TYPE_CHECKING
from dataclasses import dataclass
from enum import Enum
import random

if TYPE_CHECKING:
    from duck.duck import Duck


class ItemType(Enum):
    """Types of items."""
    FOOD = "food"
    TOY = "toy"
    DECORATION = "decoration"
    SPECIAL = "special"


@dataclass
class Item:
    """An item definition."""
    id: str
    name: str
    description: str
    item_type: ItemType
    effects: Dict[str, float]  # need changes when used
    mood_bonus: int
    duck_reaction: str
    use_message: str
    rarity: str = "common"  # common, uncommon, rare, legendary
    consumable: bool = True  # disappears after use
    icon: str = "[?]"


# Item definitions
ITEMS = {
    # Foods
    "bread": Item(
        id="bread",
        name="Bread Crumbs",
        description="Delicious bread crumbs - a duck's favorite!",
        item_type=ItemType.FOOD,
        effects={"hunger": 30},
        mood_bonus=5,
        duck_reaction="excited",
        use_message="*CHOMP CHOMP* Bread!! The best!",
        icon="[B]",
    ),
    "seeds": Item(
        id="seeds",
        name="Sunflower Seeds",
        description="Tasty sunflower seeds.",
        item_type=ItemType.FOOD,
        effects={"hunger": 20},
        mood_bonus=3,
        duck_reaction="happy",
        use_message="*peck peck* Yummy seeds!",
        icon="[S]",
    ),
    "lettuce": Item(
        id="lettuce",
        name="Fresh Lettuce",
        description="Crisp, fresh lettuce leaf.",
        item_type=ItemType.FOOD,
        effects={"hunger": 25, "cleanliness": 5},
        mood_bonus=4,
        duck_reaction="happy",
        use_message="*cronch* Healthy greens!",
        icon="[L]",
    ),
    "worm": Item(
        id="worm",
        name="Wiggly Worm",
        description="A protein-rich wiggly worm!",
        item_type=ItemType.FOOD,
        effects={"hunger": 40},
        mood_bonus=8,
        duck_reaction="ecstatic",
        use_message="*SLURP* Worm!! Best food!!",
        rarity="uncommon",
        icon="[W]",
    ),
    "fancy_bread": Item(
        id="fancy_bread",
        name="Fancy Artisan Bread",
        description="Premium bread with seeds and grains.",
        item_type=ItemType.FOOD,
        effects={"hunger": 50, "fun": 10},
        mood_bonus=15,
        duck_reaction="ecstatic",
        use_message="*savors every bite* This is FANCY!!",
        rarity="rare",
        icon="[F]",
    ),
    "golden_crumb": Item(
        id="golden_crumb",
        name="Golden Crumb",
        description="A mysteriously glowing crumb...",
        item_type=ItemType.FOOD,
        effects={"hunger": 100, "energy": 50, "fun": 30},
        mood_bonus=50,
        duck_reaction="transcendent",
        use_message="*glows with joy* THE ULTIMATE CRUMB!",
        rarity="legendary",
        icon="[G]",
    ),

    # Toys
    "rubber_duck": Item(
        id="rubber_duck",
        name="Rubber Duck Friend",
        description="A squeaky rubber duck companion!",
        item_type=ItemType.TOY,
        effects={"fun": 25, "social": 15},
        mood_bonus=10,
        duck_reaction="delighted",
        use_message="*squeak squeak* My friend!!",
        consumable=False,
        icon="[R]",
    ),
    "ball": Item(
        id="ball",
        name="Bouncy Ball",
        description="A colorful bouncy ball to chase.",
        item_type=ItemType.TOY,
        effects={"fun": 30, "energy": -10},
        mood_bonus=8,
        duck_reaction="playful",
        use_message="*chases ball* Wheee!",
        consumable=False,
        icon="[O]",
    ),
    "feather": Item(
        id="feather",
        name="Pretty Feather",
        description="A colorful feather to play with.",
        item_type=ItemType.TOY,
        effects={"fun": 15},
        mood_bonus=5,
        duck_reaction="curious",
        use_message="*plays with feather* So pretty!",
        consumable=False,
        icon="[~]",
    ),
    "mirror": Item(
        id="mirror",
        name="Small Mirror",
        description="Who's that handsome duck?",
        item_type=ItemType.TOY,
        effects={"fun": 20, "social": 10},
        mood_bonus=7,
        duck_reaction="fascinated",
        use_message="*stares at reflection* ...friend?",
        consumable=False,
        rarity="uncommon",
        icon="[M]",
    ),

    # Decorations
    "flower": Item(
        id="flower",
        name="Pretty Flower",
        description="A lovely flower for decoration.",
        item_type=ItemType.DECORATION,
        effects={"fun": 10},
        mood_bonus=5,
        duck_reaction="happy",
        use_message="*sniffs flower* Smells nice!",
        consumable=False,
        icon="[*]",
    ),
    "shiny_pebble": Item(
        id="shiny_pebble",
        name="Shiny Pebble",
        description="A shiny pebble treasure!",
        item_type=ItemType.DECORATION,
        effects={"fun": 5},
        mood_bonus=3,
        duck_reaction="proud",
        use_message="*admires pebble* My treasure...",
        consumable=False,
        icon="[.]",
    ),

    # Special items
    "lucky_clover": Item(
        id="lucky_clover",
        name="Four-Leaf Clover",
        description="A lucky charm!",
        item_type=ItemType.SPECIAL,
        effects={},
        mood_bonus=20,
        duck_reaction="amazed",
        use_message="*feels lucky* Good things coming!",
        consumable=False,
        rarity="rare",
        icon="[4]",
    ),

    # === ADDITIONAL FOODS ===
    "corn": Item(
        id="corn",
        name="Corn Kernels",
        description="Plump yellow corn kernels.",
        item_type=ItemType.FOOD,
        effects={"hunger": 25},
        mood_bonus=5,
        duck_reaction="happy",
        use_message="*peck peck peck* Pop! Pop! Delicious!",
        icon="[Y]",
    ),
    "peas": Item(
        id="peas",
        name="Sweet Peas",
        description="Tiny green peas - a healthy snack!",
        item_type=ItemType.FOOD,
        effects={"hunger": 20, "energy": 5},
        mood_bonus=3,
        duck_reaction="content",
        use_message="*munch* Healthy AND tasty! ...Mostly tasty.",
        icon="[g]",  # Lowercase to differentiate from cosmic_crumb
    ),
    "grapes": Item(
        id="grapes",
        name="Grape Halves",
        description="Sweet, juicy grape halves.",
        item_type=ItemType.FOOD,
        effects={"hunger": 30, "fun": 5},
        mood_bonus=8,
        duck_reaction="delighted",
        use_message="*slurp* SO JUICY!! More!!",
        rarity="uncommon",
        icon="[P]",
    ),
    "oats": Item(
        id="oats",
        name="Rolled Oats",
        description="Hearty, filling oats.",
        item_type=ItemType.FOOD,
        effects={"hunger": 35, "energy": 10},
        mood_bonus=4,
        duck_reaction="content",
        use_message="*munch* Healthy... but BORING. Okay fine, it's good.",
        icon="[@]",  # Grain-like to differentiate from ball
    ),
    "fish_treat": Item(
        id="fish_treat",
        name="Tiny Dried Fish",
        description="A rare protein-packed delicacy!",
        item_type=ItemType.FOOD,
        effects={"hunger": 45, "energy": 15},
        mood_bonus=15,
        duck_reaction="ecstatic",
        use_message="*CRONCH* FISH!! I didn't know I liked fish! I LOVE fish!!",
        rarity="rare",
        icon="[><]",
    ),
    "mysterious_crumb": Item(
        id="mysterious_crumb",
        name="Mysterious Crumb",
        description="What even IS this? Only one way to find out...",
        item_type=ItemType.FOOD,
        effects={"hunger": 15},
        mood_bonus=10,
        duck_reaction="curious",
        use_message="*nibble* Hmm... I have no idea what that was. 10/10 would eat again.",
        rarity="uncommon",
        icon="[?]",
    ),
    "rainbow_crumb": Item(
        id="rainbow_crumb",
        name="Rainbow Crumb",
        description="A shimmering, multicolored crumb. Magical?",
        item_type=ItemType.FOOD,
        effects={"hunger": 50, "fun": 30, "energy": 20},
        mood_bonus=40,
        duck_reaction="transcendent",
        use_message="*SPARKLES* I CAN SEE FOREVER!! ...Is this what enlightenment feels like?!",
        rarity="legendary",
        icon="[+]",  # Rainbow sparkle to differentiate from flower
    ),

    # === ADDITIONAL TOYS ===
    "squeaky_toy": Item(
        id="squeaky_toy",
        name="Squeaky Toy",
        description="A toy that makes silly sounds when poked!",
        item_type=ItemType.TOY,
        effects={"fun": 25},
        mood_bonus=10,
        duck_reaction="amused",
        use_message="*SQUEAK SQUEAK* Hehehe! Again! *SQUEAK*",
        consumable=False,
        icon="[!]",
    ),
    "tiny_boat": Item(
        id="tiny_boat",
        name="Tiny Toy Boat",
        description="A little boat to push around!",
        item_type=ItemType.TOY,
        effects={"fun": 30, "cleanliness": 5},
        mood_bonus=12,
        duck_reaction="playful",
        use_message="*pushes boat* Toot toot! I'm the captain! Captain of ONE boat!",
        consumable=False,
        rarity="uncommon",
        icon="[>]",
    ),
    "wind_up_duck": Item(
        id="wind_up_duck",
        name="Wind-Up Duck",
        description="A mechanical duck that waddles on its own!",
        item_type=ItemType.TOY,
        effects={"fun": 35, "social": 15},
        mood_bonus=15,
        duck_reaction="fascinated",
        use_message="*watches intently* It's like... mini me? BUT WORSE?! ...I'm still the better duck.",
        consumable=False,
        rarity="rare",
        icon="[D]",
    ),
    "bubble_wand": Item(
        id="bubble_wand",
        name="Bubble Wand",
        description="Creates beautiful bubbles!",
        item_type=ItemType.TOY,
        effects={"fun": 40},
        mood_bonus=18,
        duck_reaction="mesmerized",
        use_message="*pops bubbles* So many! So floaty! So... POPPABLE!! *pop pop pop*",
        consumable=False,
        rarity="rare",
        icon="[o]",
    ),
    "disco_ball": Item(
        id="disco_ball",
        name="Tiny Disco Ball",
        description="It's always party time!",
        item_type=ItemType.TOY,
        effects={"fun": 50, "social": 20},
        mood_bonus=25,
        duck_reaction="party_mode",
        use_message="*DANCING INTENSIFIES* DISCO DUCK!! WOO!! *very embarrassing moves*",
        consumable=False,
        rarity="legendary",
        icon="[@]",
    ),

    # === ADDITIONAL DECORATIONS ===
    "seashell": Item(
        id="seashell",
        name="Pretty Seashell",
        description="You can hear the ocean... or maybe just your own breathing.",
        item_type=ItemType.DECORATION,
        effects={"fun": 8},
        mood_bonus=6,
        duck_reaction="nostalgic",
        use_message="*listens* I hear... the sea? Or my stomach? Hard to tell.",
        consumable=False,
        icon="[)]",
    ),
    "cool_stick": Item(
        id="cool_stick",
        name="Really Cool Stick",
        description="It's just a stick but it's REALLY cool, okay?",
        item_type=ItemType.DECORATION,
        effects={"fun": 5},
        mood_bonus=3,
        duck_reaction="proud",
        use_message="Look at this STICK. THE coolest stick. Don't question it.",
        consumable=False,
        icon="[/]",
    ),
    "bottle_cap": Item(
        id="bottle_cap",
        name="Shiny Bottle Cap",
        description="Trash to some, treasure to ducks.",
        item_type=ItemType.DECORATION,
        effects={},
        mood_bonus=4,
        duck_reaction="collector",
        use_message="*adds to hoard* My precious... I mean, my collection!",
        consumable=False,
        icon="[0]",
    ),
    "glitter_rock": Item(
        id="glitter_rock",
        name="Sparkly Rock",
        description="A rock with glitter embedded in it!",
        item_type=ItemType.DECORATION,
        effects={"fun": 10},
        mood_bonus=10,
        duck_reaction="enchanted",
        use_message="*gazes* It's like the stars... but smaller... and rock-ier...",
        consumable=False,
        rarity="uncommon",
        icon="[+]",
    ),
    "tiny_crown": Item(
        id="tiny_crown",
        name="Tiny Crown",
        description="A crown fit for a duck royalty!",
        item_type=ItemType.DECORATION,
        effects={"fun": 15, "social": 10},
        mood_bonus=20,
        duck_reaction="regal",
        use_message="*WEARING CROWN* I am ROYALTY now. Bow before me. Or don't. I'm chill.",
        consumable=False,
        rarity="rare",
        icon="[^]",
    ),
    "golden_feather": Item(
        id="golden_feather",
        name="Golden Feather",
        description="A mysteriously glowing golden feather...",
        item_type=ItemType.DECORATION,
        effects={"fun": 20},
        mood_bonus=30,
        duck_reaction="awestruck",
        use_message="*reverent quack* Is this... from the Legendary Golden Duck?! IT'S REAL?!",
        consumable=False,
        rarity="legendary",
        icon="[~]",
    ),

    # === SPECIAL/SECRET ITEMS ===
    "mystery_egg": Item(
        id="mystery_egg",
        name="Mystery Egg",
        description="What could be inside? Probably nothing. Maybe something?",
        item_type=ItemType.SPECIAL,
        effects={"fun": 30},
        mood_bonus=25,
        duck_reaction="confused",
        use_message="*stares at egg* Are we... related? This is awkward...",
        consumable=False,
        rarity="rare",
        icon="[E]",
    ),
    "ancient_bread": Item(
        id="ancient_bread",
        name="Ancient Bread",
        description="Bread from a time long forgotten. Still kinda edible?",
        item_type=ItemType.SPECIAL,
        effects={"hunger": 100},
        mood_bonus=50,
        duck_reaction="reverent",
        use_message="*whispers* The LEGENDARY bread... I thought it was just a myth... *takes smallest bite*",
        rarity="legendary",
        icon="[A]",
    ),
    "duck_photo": Item(
        id="duck_photo",
        name="Photo of You Two",
        description="A cherished photo of you and your duck.",
        item_type=ItemType.SPECIAL,
        effects={"social": 30},
        mood_bonus=35,
        duck_reaction="emotional",
        use_message="*looks at photo* We look so happy... Wait, is that crumb on my face?! DELETE THIS!",
        consumable=False,
        rarity="rare",
        icon="[#]",
    ),
    "void_crumb": Item(
        id="void_crumb",
        name="Void Crumb",
        description="A crumb that stares back. Where did this come from?",
        item_type=ItemType.SPECIAL,
        effects={"hunger": 1, "fun": -10, "energy": 50},
        mood_bonus=-5,
        duck_reaction="unsettled",
        use_message="*eats* That tasted like... nothing? And everything? I feel weird...",
        rarity="legendary",
        icon="[V]",
    ),
    "best_friend_badge": Item(
        id="best_friend_badge",
        name="Best Friend Badge",
        description="Proof of your unbreakable bond!",
        item_type=ItemType.SPECIAL,
        effects={"social": 50},
        mood_bonus=100,
        duck_reaction="crying_happy",
        use_message="*actual tears* You... you really care... I'M NOT CRYING YOU'RE CRYING!!",
        consumable=False,
        rarity="legendary",
        icon="[<3]",
    ),
    # ── Medicine (consequence engine) ──────────────────────────────
    "medicine": Item(
        id="medicine",
        name="Pond Medicine",
        description="Dubious herbal remedy. Smells like pond scum and regret.",
        item_type=ItemType.SPECIAL,
        effects={},  # Handled by consequence engine, not need effects
        mood_bonus=5,
        duck_reaction="grimace",
        use_message="*gulp* ...disgusting. absolutely vile. ...I feel better. don't tell anyone.",
        consumable=True,
        rarity="uncommon",
        icon="[+]",
    ),
}


class Inventory:
    """
    Manages the duck's item inventory.
    """

    def __init__(self, max_size: int = 20):
        self.items: List[str] = []  # List of item IDs
        self.max_size = max_size
        self.equipped: Dict[str, str] = {}  # slot -> item_id

    def add_item(self, item_id: str) -> bool:
        """
        Add an item to inventory.

        Returns:
            True if added successfully, False if full
        """
        if item_id not in ITEMS:
            return False

        if len(self.items) >= self.max_size:
            return False

        self.items.append(item_id)
        return True

    def remove_item(self, item_id: str) -> bool:
        """Remove an item from inventory."""
        if item_id in self.items:
            self.items.remove(item_id)
            return True
        return False

    def has_item(self, item_id: str) -> bool:
        """Check if inventory contains an item."""
        return item_id in self.items

    def get_item_count(self, item_id: str) -> int:
        """Get count of a specific item."""
        return self.items.count(item_id)

    def use_item(self, item_id: str, duck: "Duck") -> Optional[Dict]:
        """
        Use an item on the duck.

        Args:
            item_id: Item to use
            duck: Duck to use item on

        Returns:
            Dict with results, or None if item not found/usable
        """
        if item_id not in self.items:
            return None

        item = ITEMS.get(item_id)
        if not item:
            return None

        # Apply effects
        changes = {}
        for need, change in item.effects.items():
            if hasattr(duck.needs, need):
                old_value = getattr(duck.needs, need)
                new_value = max(0, min(100, old_value + change))
                setattr(duck.needs, need, new_value)
                changes[need] = new_value - old_value

        # Remove if consumable
        if item.consumable:
            self.items.remove(item_id)

        return {
            "item": item,
            "changes": changes,
            "message": item.use_message,
            "reaction": item.duck_reaction,
        }

    def get_items_by_type(self, item_type: ItemType) -> List[str]:
        """Get all items of a specific type."""
        return [
            item_id for item_id in self.items
            if ITEMS.get(item_id) and ITEMS[item_id].item_type == item_type
        ]

    def get_food_items(self) -> List[str]:
        """Get all food items."""
        return self.get_items_by_type(ItemType.FOOD)

    def get_toy_items(self) -> List[str]:
        """Get all toy items."""
        return self.get_items_by_type(ItemType.TOY)

    def is_full(self) -> bool:
        """Check if inventory is full."""
        return len(self.items) >= self.max_size

    def is_empty(self) -> bool:
        """Check if inventory is empty."""
        return len(self.items) == 0

    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "items": self.items.copy(),
            "max_size": self.max_size,
            "equipped": self.equipped.copy(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Inventory":
        """Create from dictionary."""
        inv = cls(max_size=data.get("max_size", 20))
        inv.items = data.get("items", [])
        inv.equipped = data.get("equipped", {})
        return inv


def get_random_item(rarity: str = None) -> Optional[str]:
    """
    Get a random item ID, optionally filtered by rarity.

    Args:
        rarity: Optional rarity filter

    Returns:
        Item ID or None
    """
    if rarity:
        candidates = [
            item_id for item_id, item in ITEMS.items()
            if item.rarity == rarity
        ]
    else:
        # Weight by rarity
        candidates = []
        weights = {"common": 60, "uncommon": 25, "rare": 10, "legendary": 1}
        for item_id, item in ITEMS.items():
            weight = weights.get(item.rarity, 10)
            candidates.extend([item_id] * weight)

    if candidates:
        return random.choice(candidates)
    return None


def get_item_info(item_id: str) -> Optional[Item]:
    """Get item definition by ID."""
    return ITEMS.get(item_id)
