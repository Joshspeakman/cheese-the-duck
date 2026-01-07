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
    SWAMP = "swamp"         # Murky water, fireflies, bog plants, mysterious finds
    URBAN = "urban"         # City park, bread crumbs, lost coins, human treasures


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
    unlock_level: int = 1  # Player level required to access
    is_discovered: bool = False
    times_visited: int = 0
    special_events: List[str] = field(default_factory=list)
    art: List[str] = field(default_factory=list)  # ASCII art for this area


# Unique ASCII art for each area
AREA_ART = {
    "Home Pond": [
        "    .  *  .    *       .   *",
        "  *    ~~~~~~~~~~~    .     ",
        "    . ~~~~~~~~~~~~~ *   .   ",
        " .   ~~~~~~~~~~~~~~~     *  ",
        "    ~~~~~~~~~~~~~~~~   .    ",
        "  *  ~~~~~~~~~~~~~~~  *     ",
        "   . ~~~~~~~~~~~~~~~ .      ",
        r" ,,  \water water/  ,,   . ",
        r",,,\\  ~~~~~~~~~~~  //,,,  ",
        r",,,,,\  ~~~~~~~~~  /,,,,,  ",
    ],
    "Deep End": [
        "  %%%%%%%%%%%%%%%%%%%%%%   ",
        " %####################%   ",
        "%#~~~~~~~~~~~~~~~~~~~~~~#% ",
        "%#~~~<%>~~~~<%>~~~~<%>~~#% ",
        "%#~~~~~~~~~~~~~~~~~~~~~~#% ",
        "%#~~~===___===___===~~~~#% ",
        "%#~~|   ???   |~~~~~~~~#%  ",
        " %#~|_________|~~~~~~~#%   ",
        "  %#####################%  ",
        "   %%%%%%%%%%%%%%%%%%%%%%  ",
    ],
    "Forest Edge": [
        "   AAA   AAA   AAA   AAA   ",
        "  AAAAA AAAAA AAAAA AAAAA  ",
        "    |     |     |     |    ",
        " ,,,|,,,,,|,,,,,|,,,,,|,,, ",
        "====+=====+=====+=====+====",
        "~~~~|~~~~~|~~~~~|~~~~~|~~~~",
        "~~~~+=====+=====+=====+~~~~",
        " ~~~~~~~~~~~~~~~~~~~~~~    ",
        "  ~~~~<%>~~~~~~<%>~~~~     ",
        "   ~~~~~~~~~~~~~~~~~~~~    ",
    ],
    "Ancient Oak": [
        "     .AAAAAAAAAAAAAAAA.     ",
        "   .AAAAAAAAAAAAAAAAAAAA.   ",
        "  AAAAAAAAAAAAAAAAAAAAAAA   ",
        "   AAAAAAAAAAAAAAAAAAAAA    ",
        "     AAAAAAA|||AAAAAAA      ",
        "          |||||||           ",
        "      [O O]|||||[O O]       ",
        "          |||||    (@)      ",
        "    ======+++++======       ",
        " ,,,,,,,,,|||||,,,,,,,,,,   ",
    ],
    "Mushroom Grove": [
        "  *  .  *  .  *  .  *  .   ",
        "   ,---, . ,-----, ,---,   ",
        "  / * * \\  / * * * \\ / * \\ ",
        " +--###--++---###---++###+ ",
        "    |||       |||     |||  ",
        "  ,-----, . ,---, . ,----, ",
        " / o o o \\  / o o\\ / o o o\\",
        "+----###--++--###-++--###--+",
        "     |||     |||     |||   ",
        ",,,,,,,,,,,,,,,,,,,,,,,,,,  ",
    ],
    "Sunny Meadow": [
        "  *  .  *  .  *  .  *  .   ",
        " (*) .  (*) .  (*) .  (*)  ",
        " /|\\ .  /|\\ .  /|\\ .  /|\\  ",
        "  |  .   |  .   |  .   |   ",
        "  z  8  z  8  z  8  z  8   ",
        " (*) .  (*) .  (*) .  (*)  ",
        " /|\\ .  /|\\ .  /|\\ .  /|\\  ",
        "  |  .   |  .   |  .   |   ",
        "''''''''''''''''''''''''''",
        ",,,,,,,,,,,,,,,,,,,,,,,,,,",
    ],
    "Butterfly Garden": [
        "  V V   V V   V V   V V    ",
        "   W     W     W     W     ",
        " +=====================+   ",
        " |  *  *  *  *  *  *  |    ",
        " | (*)(*)(*)(*)(*)(*)(*)|  ",
        " | /|/|/|/|/|/|/|/|/|/||   ",
        " |  | | | | | | | | | |    ",
        " +=====================+   ",
        "   V V   V V   V V   V V   ",
        "''''''''''''''''''''''''''",
    ],
    "Pebble Beach": [
        "  .  *  .  *  .  *  .  *   ",
        "  ~~~~~~~~~~~~~~~~~~~~~~   ",
        " ~~~~~~~~~~~~~~~~~~~~~~~~  ",
        "~~~~========================",
        " ~~~=======================",
        "============================",
        " oOo oOo oOo oOo oOo oOo   ",
        "o Oo OoO oO OoO oOo OoO o  ",
        "oOo oOo (@) oOo (@) oOo oO ",
        " o  o  o  o  o  o  o  o    ",
    ],
    "Waterfall": [
        "  ################         ",
        " #||||||||||||||||||#      ",
        " #||||||||||||||||||#      ",
        "  #||||||||||||||||#       ",
        "   #+====++====++===+      ",
        "    |~~~~||~~~~||~~~|      ",
        "    +====++====++===+      ",
        " ~~~~====================  ",
        "~~~~======================",
        " ,,,,,,,,,,,,,,,,,,,,,,    ",
    ],
    "Vegetable Patch": [
        "  *  .  *  .  *  .  *  .   ",
        " +--+--+--+--+--+--+--+    ",
        " |@@|^^|()|()|@@|^^|()|    ",
        " +--+--+--+--+--+--+--+    ",
        " |^^|()|@@|^^|()|@@|^^|    ",
        " +--+--+--+--+--+--+--+    ",
        " |()|@@|^^|()|^^|()|@@|    ",
        " +--+--+--+--+--+--+--+    ",
        " ,,,,,,,,,,,,,,,,,,,,,,    ",
        "  . . . . . . . . . . .    ",
    ],
    "Tool Shed": [
        "     +================+    ",
        "    /##################\\   ",
        "   /################### \\  ",
        "  +======================+ ",
        " |  +----+  +====+       | ",
        " |  |T /\\|  | [] |  [++] | ",
        " |  |/ \\||  +====+       | ",
        " |  +----+      (O)      | ",
        " +========[    ]=======+ ",
        " ,,,,,,,,, door ,,,,,,,   ",
    ],
    "Foothills": [
        "          /\\               ",
        "         /  \\    /\\        ",
        "    /\\  /    \\  /  \\   /\\  ",
        "   /  \\/======\\/====\\ /  \\ ",
        "  /    \\  /\\  /\\     \\/   \\",
        " /  AAA \\/  \\/  \\ AAA \\    ",
        "/  AAAAA\\    /   AAAAA \\   ",
        "====++===\\  /=====++=====  ",
        " AAA||AAA \\/  AAA||AAA     ",
        ",,,,,,,,,,,,,,,,,,,,,,,,   ",
    ],
    "Crystal Cave": [
        " ####+==============+###   ",
        "##   | <>  *  <>  * |  ##  ",
        "#    |  \\  /  \\  /  |   #  ",
        "#    | * ><  * >< * |   #  ",
        "#    |  /  \\  /  \\  |   #  ",
        "#    | *  <>  *  <> |   #  ",
        "#    |   [*]  [*]   |   #  ",
        "##   +==============+  ##  ",
        " ### |~~~~~~~~~~~~~~| ##   ",
        "  ###+==============+##    ",
    ],
    "Sandy Shore": [
        "  *  .  .  *  .  .  *      ",
        "   \\|/       \\|/          ",
        "    |   /\\    |    /\\     ",
        "    |   \\/    |    \\/     ",
        "~~~~~~~~~~~~~~~~~~~~~~     ",
        " ~~~~===================   ",
        "  ~~~====================  ",
        "============================",
        ".:.:(@).:.:.:.:(@).:.:.:.: ",
        "...........................",
    ],
    "Shipwreck Cove": [
        "  *  .  *  .  *  .  *      ",
        " ~~~~~~~~~~~~~~~~~~~~~~    ",
        "~~=======================  ",
        "~===+====+===============  ",
        "~~==| XX |=====+====+=~~   ",
        "~===+====+=====|XXXX|===   ",
        "====|    |=====+====+===   ",
        " ===+/\\\\/\\+=============== ",
        "===/______\\=============== ",
        " (@) [$] [*]  (@) [<>] (@) ",
    ],
    "Misty Marsh": [
        "  o  .  o  .  o  .  o  .   ",
        " ########################  ",
        "##~~~~~~~~~~~~~~~~~~~~~~~~#",
        "#~~~~~~~~~~~~~~~~~~~~~~~~~#",
        "#~~||~~||~~||~~||~~||~~||~#",
        "#~~||~~||~~||~~||~~||~~||~#",
        "#~~~~~~~~~~~~~~~~~~~~~~~~~#",
        " ########################  ",
        "  (@)    (@)      (@)      ",
        ",,,,,,,,,,,,,,,,,,,,,,,,   ",
    ],
    "Cypress Hollow": [
        "  *  .  *  .  *  .  *      ",
        "  /\\   /\\   /\\   /\\       ",
        " /##\\ /##\\ /##\\ /##\\      ",
        "/####X####X####X####\\     ",
        " ||||  ||||  ||||  ||||    ",
        " ||||  ||||  ||||  ||||    ",
        "~||||~~||||~~||||~~||||~~  ",
        "~~======================== ",
        "  (@)       (@)       (@)  ",
        ",,,,,,,,,,,,,,,,,,,,,,,    ",
    ],
    "Sunken Ruins": [
        "  *  .  *  .  *  .  *      ",
        " ========================  ",
        "==+==+====+======+====+==  ",
        "==|##|====| @@ @ |====|==  ",
        "==+==+====+======+====+==  ",
        "==|  |====|      |====|==  ",
        "==+==+====+======+====+==  ",
        "=====<%>=========<%>=====  ",
        "  (*)    [<>]   [*]   (*) ",
        "=========================  ",
    ],
    "Park Fountain": [
        "  *  .  .  *  .  .  *      ",
        "      +======+             ",
        "     +| ~~~  |+            ",
        "     ||  |   ||            ",
        "   +=+|  |   |+=+          ",
        "  +|~~~| |   |~~~|+        ",
        " +|~~~~+-+-+-+~~~~|+       ",
        " ||~~~~~~~|~~~~~~~||       ",
        " ++===============++       ",
        "  AAA  [==]  [==]  AAA     ",
    ],
    "Rooftop Garden": [
        "  .  *  .  *  .  *  .      ",
        " +====================+    ",
        " | ++ ++ ++ ++ ++ ++ +|    ",
        " | @@ @@ @@ @@ @@ @@ @|    ",
        " +====================+    ",
        " |  [==]    [==]    []|    ",
        " |       @@       @@  |    ",
        " +====================+    ",
        " | -- | -- | -- | -- |     ",
        " |    |    |    |    |     ",
    ],
    "Storm Drain": [
        " ######################    ",
        " #||##||##||##||##||##|    ",
        " #||##||##||##||##||##|    ",
        " ######################    ",
        " |                    |    ",
        " | ================== |    ",
        " | ================== |    ",
        " | ====(@)======(@)=== |   ",
        " | ================== |    ",
        " +====================+    ",
    ],
}


# ============================================================================
# LOCATION-SPECIFIC EVENTS AND DISCOVERIES
# ============================================================================

# Each location has unique events that can only happen there
LOCATION_EVENTS = {
    "Home Pond": {
        "events": [
            {"name": "Familiar Ripple", "message": "*sees ripple* That's MY ripple spot. Marked it myself.", "chance": 0.08},
            {"name": "Cozy Spot Found", "message": "*settles into favorite spot* ...This is acceptable.", "chance": 0.05},
            {"name": "Reed Serenade", "message": "*listens to wind through reeds* ...It's singing to ME. Obviously.", "chance": 0.04},
        ],
        "discoveries": ["perfect_lily_pad", "home_feather", "lucky_pebble"],
    },
    "Deep End": {
        "events": [
            {"name": "Shadow Below", "message": "*peers into depths* Something's down there... It BETTER not be judging me.", "chance": 0.10},
            {"name": "Mysterious Bubble", "message": "*watches bubble rise* ...That wasn't me. WHO WAS THAT?!", "chance": 0.08},
            {"name": "Deep Glow", "message": "*notices faint glow below* Treasure? Or a trap? ...Still going.", "chance": 0.05},
            {"name": "Sunken Treasure", "message": "*finds old object* This was down here the WHOLE TIME?!", "chance": 0.03},
        ],
        "discoveries": ["ancient_coin", "sunken_toy", "mysterious_pearl", "deep_crystal"],
    },
    "Forest Edge": {
        "events": [
            {"name": "Rustling Leaves", "message": "*hears rustle* Show yourself! I'm not scared. I'm DANGEROUS.", "chance": 0.08},
            {"name": "Acorn Drop", "message": "*acorn bonks head* OW! ...I'll allow it. This time.", "chance": 0.06},
            {"name": "River Song", "message": "*listens to river* It's telling me where the fish are. I speak river.", "chance": 0.04},
        ],
        "discoveries": ["perfect_twig", "forest_gem", "ancient_acorn"],
    },
    "Ancient Oak": {
        "events": [
            {"name": "Owl Stare", "message": "*meets owl's gaze* ...I'm the scarier one here. I am.", "chance": 0.10},
            {"name": "Squirrel Chatter", "message": "*squirrel scolds* Yeah? YEAH?! Come down here and say that!", "chance": 0.08},
            {"name": "Old Wisdom", "message": "*touches ancient bark* This tree knows things. I can TELL.", "chance": 0.04},
            {"name": "Nest Discovery", "message": "*finds abandoned nest* FREE REAL ESTATE. ...Too small though.", "chance": 0.05},
        ],
        "discoveries": ["owl_feather", "acorn_collection", "ancient_bark", "tree_sap_amber"],
    },
    "Mushroom Grove": {
        "events": [
            {"name": "Spore Cloud", "message": "*walks through spores* ACHOO! ...That never happened.", "chance": 0.10},
            {"name": "Glow Pulse", "message": "*mushrooms pulse* They're COMMUNICATING. About me. Definitely about me.", "chance": 0.06},
            {"name": "Fairy Ring", "message": "*finds perfect circle* ...I'm not dancing in it. You can't make me.", "chance": 0.03},
        ],
        "discoveries": ["glowing_cap", "spore_dust", "fairy_truffle", "luminescent_moss"],
    },
    "Sunny Meadow": {
        "events": [
            {"name": "Bee Inspection", "message": "*bee hovers close* I'm not a flower! ...Unless you have honey.", "chance": 0.08},
            {"name": "Sunbeam Nap", "message": "*finds perfect sunbeam* This spot... is mine now. Forever.", "chance": 0.05},
            {"name": "Flower Crown", "message": "*flower falls on head* I AM ROYALTY NOW. It was always true.", "chance": 0.04},
            {"name": "Lucky Clover", "message": "*finds four-leaf clover* DESTINY. I was MEANT to find this.", "chance": 0.02},
        ],
        "discoveries": ["honeycomb_piece", "four_leaf_clover", "bee_amber", "sunflower_seed"],
    },
    "Butterfly Garden": {
        "events": [
            {"name": "Butterfly Landing", "message": "*butterfly lands on beak* I am CHOSEN. Bow before me.", "chance": 0.08},
            {"name": "Wing Shimmer", "message": "*watches shimmer* ...I could have wings if I WANTED.", "chance": 0.06},
            {"name": "Chrysalis Found", "message": "*finds chrysalis* A waiting butterfly. I understand waiting.", "chance": 0.04},
        ],
        "discoveries": ["butterfly_wing", "chrysalis_shell", "nectar_drop", "iridescent_scale"],
    },
    "Pebble Beach": {
        "events": [
            {"name": "Perfect Skip", "message": "*skips stone 12 times* WORLD RECORD. You saw it. You're my witness.", "chance": 0.06},
            {"name": "Wave Splash", "message": "*wave splashes* HEY! I wasn't READY! Best of three!", "chance": 0.08},
            {"name": "Smooth Find", "message": "*finds incredibly smooth stone* ...This one is special. Don't touch it.", "chance": 0.04},
        ],
        "discoveries": ["perfect_skipper", "wave_glass", "river_opal", "ancient_fossil"],
    },
    "Waterfall": {
        "events": [
            {"name": "Rainbow Sighting", "message": "*sees rainbow in mist* At the end is treasure. I WILL find it.", "chance": 0.06},
            {"name": "Mist Baptism", "message": "*walks through mist* I am REFRESHED. And slightly damp.", "chance": 0.08},
            {"name": "Hidden Cave Glimpse", "message": "*glimpses cave behind falls* There's something IN there...", "chance": 0.04},
            {"name": "Treasure Washes Up", "message": "*finds washed-up treasure* The waterfall PROVIDES.", "chance": 0.03},
        ],
        "discoveries": ["waterfall_crystal", "mist_pearl", "rainbow_scale", "cave_gem"],
    },
    "Vegetable Patch": {
        "events": [
            {"name": "Worm Friend", "message": "*worm appears* Hello, long pink duck. ...Wait.", "chance": 0.08},
            {"name": "Ripe Discovery", "message": "*finds fallen vegetable* The humans DON'T NEED THIS. It's mine now.", "chance": 0.06},
            {"name": "Scarecrow Staredown", "message": "*stares at scarecrow* ...I blinked first. BUT I'LL WIN NEXT TIME.", "chance": 0.05},
        ],
        "discoveries": ["perfect_seed", "garden_snail_shell", "lucky_worm", "heirloom_seed"],
    },
    "Tool Shed": {
        "events": [
            {"name": "Dusty Sneeze", "message": "*inhales dust* ACHOO! ...There's HISTORY in here.", "chance": 0.10},
            {"name": "Shiny Tool Spot", "message": "*sees gleaming tool* TREASURE CAVE. Everything is treasure.", "chance": 0.06},
            {"name": "Cobweb Encounter", "message": "*walks into web* AAAAH! ...I meant to do that.", "chance": 0.08},
        ],
        "discoveries": ["shiny_nail", "brass_button", "twine_ball", "old_key"],
    },
    "Foothills": {
        "events": [
            {"name": "Echo Call", "message": "*QUACKS at mountain* ...It quacked BACK. We're friends now.", "chance": 0.08},
            {"name": "Eagle Shadow", "message": "*sees shadow pass* ...I'm the apex predator here. I AM.", "chance": 0.06},
            {"name": "Alpine Wind", "message": "*strong gust* ...The mountain is TESTING me. I pass.", "chance": 0.05},
        ],
        "discoveries": ["eagle_feather", "mountain_crystal", "alpine_flower", "fossil_fragment"],
    },
    "Crystal Cave": {
        "events": [
            {"name": "Light Refraction", "message": "*sees light dance* I'm covered in RAINBOW. This is my destiny.", "chance": 0.08},
            {"name": "Crystal Hum", "message": "*crystals hum* They're SINGING to me. I'm honored.", "chance": 0.06},
            {"name": "Echo Wonder", "message": "*quacks softly* ...It echoes forever. I am ETERNAL.", "chance": 0.04},
        ],
        "discoveries": ["amethyst_shard", "crystal_cluster", "geode_piece", "cave_pearl"],
    },
    "Sandy Shore": {
        "events": [
            {"name": "Wave Dance", "message": "*dodges waves* Too slow! I'm TOO FAST FOR YOU, OCEAN!", "chance": 0.08},
            {"name": "Shell Discovery", "message": "*holds shell to ear* ...It's whispering secrets. Duck secrets.", "chance": 0.06},
            {"name": "Crab Challenge", "message": "*crab waves claw* BRING IT! I have a BEAK!", "chance": 0.05},
            {"name": "Coconut Roll", "message": "*coconut rolls past* ...I'll deal with you LATER.", "chance": 0.04},
        ],
        "discoveries": ["conch_shell", "sea_glass", "starfish", "palm_pearl"],
    },
    "Shipwreck Cove": {
        "events": [
            {"name": "Pirate Fancy", "message": "*imagines being pirate* Captain Duck! Terror of the seas! QUARK!", "chance": 0.08},
            {"name": "Treasure Glint", "message": "*sees something shine* GOLD?! ...or a button. STILL MINE.", "chance": 0.06},
            {"name": "Ship Creak", "message": "*ship creaks* ...It's just settling. I'm not scared. YOU'RE scared.", "chance": 0.05},
        ],
        "discoveries": ["doubloon", "treasure_map_piece", "captain_button", "ancient_compass"],
    },
    "Park Fountain": {
        "events": [
            {"name": "Coin Wish", "message": "*human throws coin* ...That WISH was for ME. I'm keeping it.", "chance": 0.08},
            {"name": "Pigeon Standoff", "message": "*pigeon approaches* This is MY fountain. Find your own.", "chance": 0.06},
            {"name": "Water Dance", "message": "*fountain jets change* It's performing FOR ME. Obviously.", "chance": 0.05},
        ],
        "discoveries": ["wishing_coin", "fountain_penny", "lost_ring", "city_gem"],
    },
    "Rooftop Garden": {
        "events": [
            {"name": "City View", "message": "*surveys city below* All of this... could be MINE someday.", "chance": 0.06},
            {"name": "Urban Bee Friend", "message": "*bee visits* Even city bees know greatness. That's me.", "chance": 0.05},
            {"name": "Wind Garden", "message": "*wind chimes ring* They're announcing my ARRIVAL.", "chance": 0.04},
        ],
        "discoveries": ["rooftop_herb", "city_honey", "wind_chime_piece", "urban_flower"],
    },
    "Storm Drain": {
        "events": [
            {"name": "Echo Explorer", "message": "*quack echoes endlessly* I have CONQUERED the underground!", "chance": 0.08},
            {"name": "Treasure Current", "message": "*sees something float by* The drain PROVIDES tribute.", "chance": 0.06},
            {"name": "Grate Light", "message": "*light streams through grate* A spotlight! For ME!", "chance": 0.05},
            {"name": "Underground Discovery", "message": "*finds hidden corner* Secret BASE. This is my secret BASE now.", "chance": 0.04},
        ],
        "discoveries": ["lost_marble", "subway_token", "drain_treasure", "mystery_key"],
    },
    "Misty Marsh": {
        "events": [
            {"name": "Firefly Welcome", "message": "*fireflies surround* They RECOGNIZE royalty. As they should.", "chance": 0.08},
            {"name": "Mist Whisper", "message": "*mist swirls* ...The marsh is SPEAKING. I listen.", "chance": 0.05},
            {"name": "Mystery Sound", "message": "*strange noise* ...I'm investigating. I'm BRAVE.", "chance": 0.06},
        ],
        "discoveries": ["firefly_lantern", "marsh_pearl", "bog_amber", "mist_crystal"],
    },
    "Cypress Hollow": {
        "events": [
            {"name": "Moss Drape", "message": "*moss brushes face* The trees are PETTING me. Acceptable.", "chance": 0.06},
            {"name": "Ancient Feeling", "message": "*senses age of trees* ...I belong here. The hollow KNOWS.", "chance": 0.04},
            {"name": "Hidden Path", "message": "*finds hidden way* Secret passage! For DUCKS ONLY.", "chance": 0.03},
        ],
        "discoveries": ["cypress_cone", "moss_bundle", "hollow_gem", "ancient_bark"],
    },
    "Sunken Ruins": {
        "events": [
            {"name": "Ancient Echo", "message": "*explores ruins* Someone IMPORTANT lived here. Like me.", "chance": 0.06},
            {"name": "Relic Gleam", "message": "*sees underwater glint* History and TREASURE! My favorites!", "chance": 0.05},
            {"name": "Pillar Perch", "message": "*sits on pillar* I am KING of these ruins now.", "chance": 0.04},
        ],
        "discoveries": ["ancient_tile", "ruin_gem", "forgotten_coin", "mystery_artifact"],
    },
}

# Location-specific duck dialogue when entering or exploring
LOCATION_DIALOGUE = {
    "Home Pond": [
        "Home sweet pond. MINE.",
        "Ah, familiar waters. The BEST waters.",
        "*happy paddle* Nobody makes ripples like me.",
        "Every lily pad knows my name here.",
    ],
    "Deep End": [
        "Into the DEPTHS. The brave go here. That's me.",
        "*peers down* What secrets are you hiding, pond?",
        "The deep end respects me. I can tell.",
        "Somewhere down there... MYSTERIES.",
    ],
    "Forest Edge": [
        "Where water meets wood. BOTH are mine.",
        "*listens to river* Yes, I understand. Secrets.",
        "The forest doesn't scare me. I scare IT.",
        "Twigs. Leaves. Acorns. TREASURE everywhere.",
    ],
    "Ancient Oak": [
        "This tree has seen THINGS. Like me. We're alike.",
        "*looks up* You and me, Oak. Legends.",
        "The squirrels fear my name here.",
        "Ancient wisdom flows from this bark. I absorb it.",
    ],
    "Mushroom Grove": [
        "*sniffs* Smells like MAGIC in here.",
        "The mushrooms GLOW for me. It's an honor.",
        "Spores know duck greatness when they see it.",
        "This place understands the weird and wonderful.",
    ],
    "Sunny Meadow": [
        "*stretches in sun* Yes. This is PERFECT.",
        "Bees recognize royalty. That's why they bow.",
        "Every flower here blooms for ME.",
        "The meadow and I have an understanding.",
    ],
    "Butterfly Garden": [
        "Flutter all you want. I'm still PRETTIER.",
        "*watches butterflies* We're both magnificent.",
        "A garden of wings. And ONE duck. The best one.",
        "The butterflies whisper my legend.",
    ],
    "Pebble Beach": [
        "Time to show these stones who's BOSS.",
        "*examines pebbles* These will skip PERFECTLY.",
        "The beach surrenders its smoothest stones to me.",
        "Champion skipper. That's what they'll call me.",
    ],
    "Waterfall": [
        "*stands in mist* MAJESTIC. Like me.",
        "The waterfall ROARS my arrival!",
        "Somewhere behind that water... TREASURE.",
        "Rainbows exist because of ducks like me.",
    ],
    "Vegetable Patch": [
        "The BOUNTY. All of it could be mine.",
        "*inspects vegetables* The scarecrow knows to fear me.",
        "Human gardens grow tribute for ducks.",
        "So many seeds... so many POSSIBILITIES.",
    ],
    "Tool Shed": [
        "Dusty mysteries await! I LOVE dusty mysteries.",
        "*sneeze* There's HISTORY here. I can taste it.",
        "Every cobweb hides a secret. Every corner, a treasure.",
        "The shed whispers its secrets only to ducks.",
    ],
    "Foothills": [
        "*looks up at peaks* I WILL conquer you, mountains.",
        "The wind up here knows my name.",
        "Eagles? Pfft. DUCKS rule these heights.",
        "The mountains bow before duck determination.",
    ],
    "Crystal Cave": [
        "*eyes sparkle* MORE shine than even I expected!",
        "The crystals SING. For me. Obviously.",
        "Underground rainbows! I have found PARADISE.",
        "These gems recognize duck magnificence.",
    ],
    "Sandy Shore": [
        "*wiggles toes in sand* Ocean duck MODE ACTIVATED.",
        "The waves retreat from my power!",
        "Shells, sand, treasure! The shore PROVIDES.",
        "I could rule this beach. I WILL rule this beach.",
    ],
    "Shipwreck Cove": [
        "ARR! ...I mean QUARK! Captain Duck arrives!",
        "*explores wreck* This is MY ship now.",
        "Pirates WISHED they were as fierce as me.",
        "Doubloons... treasure... MINE, all mine!",
    ],
    "Park Fountain": [
        "Urban territory! The fountain is MINE now.",
        "*splash splash* City ducks bow to country legends!",
        "So many coins... so many WISHES for me.",
        "The fountain dances for its new ruler.",
    ],
    "Rooftop Garden": [
        "*surveys city* All of this could be MINE.",
        "High above the peasants. Where I BELONG.",
        "Even city bees recognize duck greatness.",
        "The rooftop garden: MY sky kingdom.",
    ],
    "Storm Drain": [
        "Into the UNDERGROUND. Only the brave explore here.",
        "*echo QUACK* Magnificent acoustics for my calls.",
        "The drain hides TREASURES. I will find them ALL.",
        "This is my secret lair now. VILLAIN DUCK!",
    ],
    "Misty Marsh": [
        "*peers through mist* What secrets do you hide?",
        "Fireflies light my path. As they SHOULD.",
        "The marsh knows ancient duck wisdom.",
        "Murky waters can't hide treasure from ME.",
    ],
    "Cypress Hollow": [
        "The old trees remember duck legends. They remember ME.",
        "*brushes moss aside* I walk where few dare.",
        "Spanish moss = tree beard = WISE. Like me.",
        "This hollow was waiting for a duck. Here I AM.",
    ],
    "Sunken Ruins": [
        "Ancient duck civilizations once RULED here!",
        "*explores carefully* History respects the curious.",
        "Every stone has a story. I will KNOW them all.",
        "Ruins = treasure = MINE. Simple math.",
    ],
}


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
    BiomeType.SWAMP: [
        ("swamp_reed", "Swamp Reed", 8, 1.5, 0),
        ("bog_moss", "Bog Moss", 10, 1.0, 0),
        ("firefly_jar", "Firefly Jar", 1, 8.0, 2),
        ("murky_pearl", "Murky Pearl", 1, 24.0, 4),
        ("ancient_bone", "Ancient Bone", 1, 48.0, 3),
        ("glowing_mushroom", "Glowing Mushroom", 3, 6.0, 2),
        ("cypress_bark", "Cypress Bark", 5, 3.0, 1),
    ],
    BiomeType.URBAN: [
        ("bread_crumb", "Bread Crumb", 10, 0.5, 0),
        ("lost_coin", "Lost Coin", 3, 4.0, 0),
        ("shiny_wrapper", "Shiny Wrapper", 6, 1.0, 0),
        ("park_flower", "Park Flower", 4, 2.0, 0),
        ("dropped_fry", "Dropped Fry", 2, 2.0, 0),
        ("fancy_button", "Fancy Button", 1, 12.0, 2),
        ("lost_earring", "Lost Earring", 1, 48.0, 4),
    ],
}


# Area definitions
AREAS = {
    BiomeType.POND: [
        BiomeArea(
            biome=BiomeType.POND,
            name="Home Pond",
            description="Your cozy home pond with grassy shores and calm waters.",
            discovery_chance=0.05,
            unlock_level=1,
            is_discovered=True,
        ),
        BiomeArea(
            biome=BiomeType.POND,
            name="Deep End",
            description="The mysterious deep part of the pond. What lurks below?",
            discovery_chance=0.15,
            unlock_level=3,
            is_discovered=True,
        ),
    ],
    BiomeType.FOREST: [
        BiomeArea(
            biome=BiomeType.FOREST,
            name="Forest Edge",
            description="Where the pond meets the forest. Lots of fallen twigs.",
            discovery_chance=0.10,
            unlock_level=1,
            is_discovered=True,
        ),
        BiomeArea(
            biome=BiomeType.FOREST,
            name="Ancient Oak",
            description="A massive old oak tree. Home to many creatures.",
            discovery_chance=0.20,
            unlock_level=5,
            is_discovered=True,
        ),
        BiomeArea(
            biome=BiomeType.FOREST,
            name="Mushroom Grove",
            description="A damp, shady area full of interesting fungi.",
            discovery_chance=0.25,
            unlock_level=7,
        ),
    ],
    BiomeType.MEADOW: [
        BiomeArea(
            biome=BiomeType.MEADOW,
            name="Sunny Meadow",
            description="A bright, flower-filled meadow buzzing with bees.",
            discovery_chance=0.10,
            unlock_level=2,
            is_discovered=True,
        ),
        BiomeArea(
            biome=BiomeType.MEADOW,
            name="Butterfly Garden",
            description="Rare butterflies dance among exotic flowers.",
            discovery_chance=0.30,
            unlock_level=8,
        ),
    ],
    BiomeType.RIVERSIDE: [
        BiomeArea(
            biome=BiomeType.RIVERSIDE,
            name="Pebble Beach",
            description="A calm section of river with smooth stones.",
            discovery_chance=0.15,
            unlock_level=3,
            is_discovered=True,
        ),
        BiomeArea(
            biome=BiomeType.RIVERSIDE,
            name="Waterfall",
            description="A beautiful waterfall! Treasures wash up here.",
            discovery_chance=0.35,
            unlock_level=10,
        ),
    ],
    BiomeType.GARDEN: [
        BiomeArea(
            biome=BiomeType.GARDEN,
            name="Vegetable Patch",
            description="A human's garden. Full of useful scraps!",
            discovery_chance=0.20,
            unlock_level=4,
            is_discovered=True,
        ),
        BiomeArea(
            biome=BiomeType.GARDEN,
            name="Tool Shed",
            description="The humans keep interesting things here...",
            discovery_chance=0.40,
            unlock_level=12,
        ),
    ],
    BiomeType.MOUNTAINS: [
        BiomeArea(
            biome=BiomeType.MOUNTAINS,
            name="Foothills",
            description="The base of the mountains. Rocky and wild.",
            discovery_chance=0.20,
            unlock_level=15,
        ),
        BiomeArea(
            biome=BiomeType.MOUNTAINS,
            name="Crystal Cave",
            description="A hidden cave sparkling with crystals!",
            discovery_chance=0.50,
            unlock_level=20,
        ),
    ],
    BiomeType.BEACH: [
        BiomeArea(
            biome=BiomeType.BEACH,
            name="Sandy Shore",
            description="The ocean! So many shells and treasures.",
            discovery_chance=0.25,
            unlock_level=18,
        ),
        BiomeArea(
            biome=BiomeType.BEACH,
            name="Shipwreck Cove",
            description="An old shipwreck! Who knows what's inside?",
            discovery_chance=0.60,
            unlock_level=25,
        ),
    ],
    BiomeType.SWAMP: [
        BiomeArea(
            biome=BiomeType.SWAMP,
            name="Misty Marsh",
            description="Thick fog hangs over murky waters. Fireflies glow in the mist.",
            discovery_chance=0.20,
            unlock_level=9,
        ),
        BiomeArea(
            biome=BiomeType.SWAMP,
            name="Cypress Hollow",
            description="Ancient twisted trees draped in moss. Secrets hide here.",
            discovery_chance=0.35,
            unlock_level=16,
        ),
        BiomeArea(
            biome=BiomeType.SWAMP,
            name="Sunken Ruins",
            description="Mysterious old structures half-submerged in the bog.",
            discovery_chance=0.55,
            unlock_level=24,
        ),
    ],
    BiomeType.URBAN: [
        BiomeArea(
            biome=BiomeType.URBAN,
            name="Park Fountain",
            description="A busy city park! Humans drop all sorts of treasures.",
            discovery_chance=0.15,
            unlock_level=6,
            is_discovered=True,
        ),
        BiomeArea(
            biome=BiomeType.URBAN,
            name="Rooftop Garden",
            description="A hidden garden high above the city streets.",
            discovery_chance=0.30,
            unlock_level=14,
        ),
        BiomeArea(
            biome=BiomeType.URBAN,
            name="Storm Drain",
            description="Underground tunnels where lost things wash up.",
            discovery_chance=0.50,
            unlock_level=22,
        ),
    ],
}


def get_area_art(area_name: str) -> List[str]:
    """Get ASCII art for a specific area."""
    return AREA_ART.get(area_name, [
        "  .  *  .  *  .  *  .  *  . ",
        "    Unknown Location        ",
        "  .  *  .  *  .  *  .  *  . ",
    ])


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
    
    def _initialize_areas(self):
        """Set up initial discovered areas."""
        for biome, areas in AREAS.items():
            for area in areas:
                if area.is_discovered:
                    self.discovered_areas[area.name] = area
                    # Initialize resources for discovered areas
                    self._populate_area_resources(area)

        # Set default starting location to Home Pond
        if "Home Pond" in self.discovered_areas and not self.current_area:
            self.current_area = self.discovered_areas["Home Pond"]
    
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
        
        # Validate player level meets area requirements
        if self.current_area and self.current_area.unlock_level > self._player_level:
            return {
                "success": False,
                "message": f"You need to be level {self.current_area.unlock_level} to explore {self.current_area.name}!",
            }
        
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
                messages.append(f"* RARE FIND: {rare_item}!")
        
        # Check for new area discovery
        if random.random() < 0.1:  # 10% chance per exploration
            undiscovered = self.get_undiscovered_areas(self._player_level)
            if undiscovered:
                new_area = random.choice(undiscovered)
                self._discover_area(new_area)
                result["new_area_discovered"] = new_area.name
                result["xp_gained"] += 50
                messages.append(f"[?] Discovered new area: {new_area.name}!")
        
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
            BiomeType.SWAMP: ["Will-o-Wisp", "Bog Amber", "Swamp Witch Charm"],
            BiomeType.URBAN: ["Lucky Penny", "Diamond Ring", "Love Letter"],
        }
        return rare_items.get(biome, [])
    
    def _check_skill_up(self):
        """Check if gathering skill should increase."""
        xp_thresholds = [0, 50, 150, 300, 500, 800, 1200, 1800, 2500, 3500]
        for level, threshold in enumerate(xp_thresholds):
            if self.exploration_xp >= threshold:
                self.gathering_skill = max(self.gathering_skill, level + 1)
    
    def get_location_dialogue(self, location: str = None) -> Optional[str]:
        """Get a random location-specific duck dialogue line."""
        area_name = location or (self.current_area.name if self.current_area else None)
        if area_name and area_name in LOCATION_DIALOGUE:
            return random.choice(LOCATION_DIALOGUE[area_name])
        return None
    
    def check_location_event(self, location: str = None) -> Optional[Dict]:
        """Check if a location-specific event occurs. Returns event data or None."""
        area_name = location or (self.current_area.name if self.current_area else None)
        if not area_name or area_name not in LOCATION_EVENTS:
            return None
        
        location_data = LOCATION_EVENTS[area_name]
        events = location_data.get("events", [])
        
        # Check each event's chance
        for event in events:
            if random.random() < event.get("chance", 0.05):
                return {
                    "name": event.get("name", "Unknown Event"),
                    "message": event.get("message", "Something happened!"),
                    "location": area_name,
                }
        return None
    
    def get_location_discovery(self, location: str = None) -> Optional[str]:
        """Get a random possible discovery item for this location."""
        area_name = location or (self.current_area.name if self.current_area else None)
        if not area_name or area_name not in LOCATION_EVENTS:
            return None
        
        discoveries = LOCATION_EVENTS[area_name].get("discoveries", [])
        if discoveries:
            return random.choice(discoveries)
        return None
    
    def get_current_area_info(self) -> str:
        """Get info about current area."""
        if not self.current_area:
            return "Not currently exploring"
        
        area = self.current_area
        available = [r for r in area.resources if r.is_available()]
        
        lines = [
            f"* {area.name} ({area.biome.value.title()})",
            f"   {area.description}",
            f"   Available resources: {len(available)}/{len(area.resources)}",
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
