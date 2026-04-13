"""
Location-specific ASCII art backgrounds for the playfield.
Each location has unique ground patterns, decorations, and scenery.
"""
import random
from typing import Dict, List, Tuple, Callable, Optional
from blessed import Terminal

_term = Terminal()


# ============================================================================
# GROUND CHARACTERS BY LOCATION
# ============================================================================

# Ground tiles - characters that make up the floor/base of each location
LOCATION_GROUND_CHARS: Dict[str, List[str]] = {
    # Home Pond - grassy shore meets calm pond water
    "Home Pond": [" ", "~", "~", "'", ".", " ", "~", "~", "~", ","],
    # Deep End - nothing but dark water and shadow
    "Deep End": ["~", "=", " ", "#", "~", "=", "~", " ", "=", "~"],

    # Forest - damp earth, leaf litter, twigs
    "Forest Edge": [" ", ".", ",", " ", ".", "'", " ", ",", ".", " "],
    "Ancient Oak": [".", ",", " ", ".", "o", " ", ",", ".", " ", "'"],
    "Mushroom Grove": [".", "~", " ", "*", ".", "~", " ", ".", "~", " "],

    # Meadow - wildflower meadow, breezy
    "Sunny Meadow": ["'", " ", "'", ".", " ", "'", ",", " ", "'", " "],
    "Butterfly Garden": ["'", " ", ".", "'", " ", "'", ".", " ", "'", ","],

    # Riverside - pebbles, fine sand, water edge
    "Pebble Beach": ["o", ".", " ", "o", ".", "O", " ", ".", "o", " "],
    "Waterfall": [".", "~", " ", ".", "=", " ", ".", "~", ".", " "],

    # Garden - tilled soil, organic
    "Vegetable Patch": [".", " ", ".", " ", ",", ".", " ", ".", ",", " "],
    "Tool Shed": [".", " ", ".", " ", ".", " ", " ", ".", " ", " "],

    # Mountains - alpine scree, rocky
    "Foothills": [" ", ".", ".", " ", ".", " ", ".", ",", " ", "."],
    "Crystal Cave": [".", " ", "*", ".", " ", ".", "*", " ", ".", " "],

    # Beach - fine sand, shell fragments
    "Sandy Shore": [" ", ".", " ", ".", " ", "o", " ", " ", ".", " "],
    "Shipwreck Cove": [".", "~", " ", ".", "=", " ", ".", " ", "o", " "],

    # Swamp - wet bog, murky
    "Misty Marsh": ["~", " ", "=", ".", "~", " ", ".", "~", " ", "="],
    "Cypress Hollow": [".", "~", " ", ".", "+", " ", "~", ".", " ", "+"],
    "Sunken Ruins": [".", "=", " ", "#", ".", "~", ".", " ", "=", "."],

    # Urban - cobblestone, concrete, gravel
    "Park Fountain": [".", " ", ".", " ", "'", ".", " ", ".", "'", " "],
    "Rooftop Garden": [".", " ", ".", "'", " ", ".", " ", ".", " ", "'"],
    "Storm Drain": [".", " ", ".", " ", ".", "#", " ", ".", " ", "."],
}

# Default ground for unknown locations
DEFAULT_GROUND_CHARS = [" ", " ", ".", " ", ".", " ", "'", " ", " ", " "]


# ============================================================================
# LOCATION-SPECIFIC DECORATIONS
# ============================================================================

# Each decoration: (art_chars, weight) - weight is how common it is
LOCATION_DECORATIONS: Dict[str, List[Tuple[str, int]]] = {
    "Home Pond": [
        # Mix of grass, shore, and water elements
        ("'", 8),        # Grass blades (land)
        (".", 6),        # Short grass (land)
        (",", 5),        # Pebbles on shore (transition)
        ("~", 8),        # Water ripples (water)
        ("O", 4),        # Lily pad (water)
        ("*", 2),        # Lily flower (water)
        ("|", 3),        # Reed stems
    ],
    "Deep End": [
        ("~", 8),        # Deep murky water
        ("=", 7),        # Dark ripples
        ("#", 3),        # Shadow shapes lurking
        ("%", 4),        # Murky patches
        (".", 5),        # Rising bubbles
        ("O", 2),        # Sunken object
        ("?", 2),        # Mystery shape
        ("<", 2),        # Fish silhouette
        (">", 2),        # Fish silhouette
    ],
    "Forest Edge": [
        # Dense forest feel with prominent river
        ("A", 10),       # Tree top (lots of trees!)
        ("|", 8),        # Tree trunk
        ("+", 7),        # Bush
        ("~", 6),        # River water
        ("=", 6),        # River flow
        (".", 5),        # Fallen leaves
        (",", 4),        # Twigs
        ("'", 3),        # Grass
        (".", 4),        # Forest floor
    ],
    "Ancient Oak": [
        ("A", 10),       # Massive tree canopy
        ("|", 6),        # Thick gnarled trunk
        ("O", 3),        # Owl knothole
        ("@", 2),        # Squirrel
        ("u", 3),        # Bird nest
        ("o", 4),        # Acorns
        ("+", 3),        # Moss
        ("^", 2),        # Shelf mushroom
        (".", 5),        # Fallen leaves
        ("'", 3),        # Woodpecker holes
    ],
    "Mushroom Grove": [
        ("^", 8),        # Small mushroom
        ("@", 5),        # Giant mushroom cap
        ("|", 3),        # Tall mushroom
        ("*", 6),        # Glowing spores floating
        (".", 5),        # Spore clouds
        ("*", 3),        # Bioluminescent spots
        ("+", 2),        # Moss clump
        ("~", 2),        # Mycelium trails
    ],
    "Sunny Meadow": [
        ("*", 6),        # Flower
        ("@", 5),        # Sunflower head
        ("+", 3),        # Beehive
        ("z", 4),        # Buzzing bee
        ("8", 3),        # Bee in flight
        ("+", 4),        # Clover patch
        ("'", 6),        # Tall grass
        (".", 3),        # Pollen float
    ],
    "Butterfly Garden": [
        ("*", 7),        # Nectar flower
        ("V", 5),        # Butterfly left wing
        ("W", 5),        # Butterfly right wing
        ("@", 3),        # Fluttering butterfly
        ("o", 3),        # Chrysalis
        ("||", 2),       # Trellis post
        ("A", 3),        # Flowering shrub
        ("~", 2),        # Flutter path
        (".", 4),        # Wing scale shimmer
    ],
    "Pebble Beach": [
        ("o", 6),        # Perfect skipping stone
        ("O", 4),        # Flat skipping stone
        ("@", 3),        # Large smooth rock
        ("~", 4),        # Skip ripples
        (".", 3),        # Skip splash point
        (".", 5),        # Tiny pebbles
        (".", 5),        # Wet sand
        ("-", 2),        # Driftwood piece
    ],
    "Waterfall": [
        ("|", 6),        # Cascading water
        ("=", 6),        # Pool swirl
        ("~", 5),        # Splash
        ("*", 5),        # Mist droplet
        (".", 4),        # Fine spray
        ("*", 3),        # Rainbow sparkle
        ("<>", 2),       # Hidden treasure glint
        ("#", 3),        # Cave shadow
    ],
    "Vegetable Patch": [
        ("@", 4),        # Cabbage head
        ("^", 5),        # Carrot top
        ("Y", 3),        # Tomato stake
        ("o", 4),        # Ripe tomato
        ("@", 3),        # Squash
        ("+", 4),        # Herb bush
        ("|", 2),        # Bean pole
        (".", 3),        # Tilled soil
        ("~", 2),        # Irrigation
    ],
    "Tool Shed": [
        ("#", 3),        # Wooden wall
        ("T", 3),        # Hanging rake
        ("/", 3),        # Shovel lean
        ("\\", 3),        # Hoe lean
        ("[", 2),        # Toolbox
        ("-", 4),        # Workbench
        ("O", 2),        # Watering can
        (".", 5),        # Sawdust
        ("=", 2),        # Cobweb
    ],
    "Foothills": [
        ("^", 6),        # Mountain peak
        ("/\\", 5),      # Distant peak
        ("=", 3),        # Snow line
        ("A", 4),        # Alpine pine
        ("O", 3),        # Boulder
        ("=", 3),        # Mountain stream
        ("*", 2),        # Eagle soar
        ("*", 2),        # Edelweiss
        (".", 4),        # Rocky scree
    ],
    "Crystal Cave": [
        ("<>", 6),       # Clear crystal
        ("*", 5),        # Amethyst cluster
        ("*", 5),        # Light refraction
        ("*", 4),        # Crystal glow
        ("~", 3),        # Underground pool
        ("V", 3),        # Stalactite
        ("A", 3),        # Stalagmite
        (".", 4),        # Cave sparkle
    ],
    "Sandy Shore": [
        ("*", 2),        # Sun glint
        ("Y", 3),        # Palm frond
        ("|", 2),        # Palm trunk
        ("@", 5),        # Spiral shell
        ("O", 3),        # Conch shell
        ("~", 4),        # Gentle wave
        ("*", 3),        # Starfish
        ("C", 2),        # Crab
        (".", 6),        # Warm sand
    ],
    "Shipwreck Cove": [
        ("#", 4),        # Rotting hull
        ("#", 2),        # Torn sail
        ("|", 3),        # Broken mast
        ("=", 3),        # Deck planks
        ("+", 1),        # Rusty anchor
        ("O", 3),        # Barrel
        ("~", 5),        # Lapping waves
        ("*", 1),        # Treasure glint (rare)
        (".", 4),        # Barnacles
    ],
    # Swamp decorations
    "Misty Marsh": [
        ("~", 7),        # Murky water
        ("=", 5),        # Ripples
        ("*", 6),        # Firefly glow
        (".", 4),        # Mist particle
        ("+", 3),        # Bog plant
        ("^", 2),        # Mushroom
    ],
    "Cypress Hollow": [
        ("|", 7),        # Tree trunk
        ("+", 5),        # Moss clump
        ("~", 4),        # Water
        ("*", 5),        # Firefly
        (".", 3),        # Spore
        ("=", 3),        # Spanish moss
    ],
    "Sunken Ruins": [
        (".", 5),        # Stone
        ("#", 3),        # Dark stone
        ("~", 6),        # Water
        ("=", 4),        # Murk
        ("O", 2),        # Ancient artifact
        (".", 3),        # Debris
    ],
    # Urban decorations
    "Park Fountain": [
        (".", 6),        # Cobblestone
        ("~", 5),        # Fountain spray
        ("+", 3),        # Trimmed hedge
        ("'", 4),        # Lawn grass
        ("o", 3),        # Wishing coin
        ("*", 3),        # Flower bed
        ("*", 1),        # Rare coin shimmer
        ("A", 2),        # Ornamental tree
    ],
    "Rooftop Garden": [
        ("+", 6),        # Potted vegetable
        ("*", 4),        # Rooftop flower
        ("^", 3),        # Carrot tops
        ("[]", 4),       # Raised bed
        ("o", 3),        # Tomato
        (".", 4),        # Gravel path
        ("O", 3),        # Clay pot
        ("z", 2),        # Urban bee
        ("|", 2),        # Bamboo stake
    ],
    "Storm Drain": [
        (".", 5),        # Damp concrete
        ("~", 4),        # Trickling water
        ("#", 4),        # Deep shadow
        ("O", 3),        # Lost treasure
        ("%", 4),        # Dim light
        ("=", 3),        # Water flow
        ("*", 2),        # Dripping stalactite
        ("*", 1),        # Glinting object (rare)
    ],
}

DEFAULT_DECORATIONS = [
    (".", 5),
    (".", 4),
    ("'", 3),
]


# ============================================================================
# SCENERY ELEMENTS - Large multi-line decorations
# ============================================================================

# Large scenery pieces that get placed in specific spots.
# Each piece is either List[str] (static) or List[List[str]] (animated frames,
# renderer picks frame = piece[_animation_frame % len(piece)]).
LOCATION_SCENERY: Dict[str, List] = {
    "Home Pond": [
        # === ANIMATED: Water surface sparkle - 3 frames ===
        [
            ["~~~~~~~~~~~", "~~~~~~~~~~~", "~~~~~~~~~~~"],
            ["~=~~~~~~~~~", "~~~~~~~~~~~", "~~~~~~~~~~~"],
            ["~~~~~~~~~~~", "~~~=~~~~~~~", "~~~~~~~~~~~"],
        ],
        # === ANIMATED: Reed sway in breeze - 4 frames ===
        [
            ["| | | | |", "| | | | |", "| | | | |", "Y Y Y Y Y"],
            ["/ / / / /", "| | | | |", "| | | | |", "Y Y Y Y Y"],
            ["| | | | |", "| | | | |", "| | | | |", "Y Y Y Y Y"],
            ["\\ \\ \\ \\ \\", "| | | | |", "| | | | |", "Y Y Y Y Y"],
        ],
        # Lily pad constellation centered on pond
        ["  ~  O  ~  O  ~  ", " ~ O ~ O ~ O ~ ", "  ~  O  *  O  ~  ",
         " ~ O ~ O ~ O ~ ", "  ~  O  ~  O  ~  "],
        # Duck's weathered dock
        ["=========", "|       |", "+=======+"],
        # Cattail border
        ["@ @ @ @ @ @", "| | | | | |", "| | | | | |"],
        # Pebble shore edge
        [". . . . . .", " . . . . . "],
    ],
    "Deep End": [
        # === ANIMATED: Shadow entity pulse - 2 frames ===
        [
            ["   ###    ", " #######  ", " ## ? ##  ", " #######  "],
            ["  ####    ", " ######## ", " ## ? ##  ", " ######## "],
        ],
        # === ANIMATED: Rising bubbles - 3 frames ===
        [
            ["  o     o  ", " o  o  o  ", "o    o   o "],
            ["o     o    ", "  o  o  o  ", " o    o   o"],
            ["   o     o ", "o  o  o    ", "  o    o   "],
        ],
        # Sunken log with glint inside
        ["  =========  ", " /%%%%%%%%%\\", "/%%%%%%%%%*%\\"],
        # Fish silhouettes lurking
        ["  ><((((o>   ", "    ><(o>    ", "  <>        "],
        # Deep pool bottom texture
        ["#=#=#=#=#=#=", "=#=#=#=#=#=#"],
        # Ancient sunken barrel
        ["  +===+  ", " |o o o| ", "  +=+=+  "],
    ],
    "Forest Edge": [
        # === ANIMATED: Treeline canopy sway - 2 frames ===
        [
            ["A   A   A   A   A", "AAA AAA AAA AAA ", " |   |   |   |  "],
            [" A   A   A   A  A", " AAA AAA AAA AAA", " |   |   |   |  "],
        ],
        # === ANIMATED: River ripple propagation - 3 frames ===
        [
            ["~~~================~~~"],
            [" ~~~==============~~~~"],
            ["~~~~==============~~~"],
        ],
        # Stone bridge over river
        ["o  o  o  o  o  o  o", " #================# ", "~~~~~~~~~~~~~~~~~~~"],
        # Dense tree cluster
        [" A A A A ", "+|+|+|++"],
        # Mossy fallen log
        ["+==========+", "|+++++####++|", "+==========+"],
        # Signpost at the forest boundary
        ["  /=======\\  ", " | FOREST |  ", "     |||     "],
    ],
    "Ancient Oak": [
        # === ANIMATED: Massive canopy sway - 2 frames ===
        [
            ["      AAAAAAAAAAAAAAAAA      ", "    AAAAAAAAAAAAAAAAAAAAA    ",
             "   AAAAAAAAAAAAAAAAAAAAAA    ", "         |||||||||           ",
             "         |||||||||           ", "         |||||||||           "],
            ["       AAAAAAAAAAAAAAAAA     ", "     AAAAAAAAAAAAAAAAAAAAA   ",
             "    AAAAAAAAAAAAAAAAAAAAAA   ", "         |||||||||           ",
             "         |||||||||           ", "         |||||||||           "],
        ],
        # === ANIMATED: Resident owl blink - 4 frames ===
        [
            ["  +------+  ", "  | O  O |  ", "  |  /\\  |  ", "  +------+  "],
            ["  +------+  ", "  | O  O |  ", "  |  /\\  |  ", "  +------+  "],
            ["  +------+  ", "  | -  - |  ", "  |  /\\  |  ", "  +------+  "],
            ["  +------+  ", "  | O  O |  ", "  |  /\\  |  ", "  +------+  "],
        ],
        # Ancient root tangle at the base
        ["/\\/\\/\\/\\/\\/\\/\\", "\\/\\/\\/\\/\\/\\/\\/", "/\\/\\    /\\/\\/\\"],
        # Bird nest in a crook
        ["  (u u u)  ", " (*o*o*o*) ", "  =======  "],
        # Squirrel hoarding an acorn
        ["  @@@  ", " @(@)@ ", "  | o  "],
        # Beehive hanging from a branch
        [" +=====+  ", "/zzzzzzz\\ ", "\\zzzzzzz/ ", "  +---+   ", "    |     "],
    ],
    "Mushroom Grove": [
        # === ANIMATED: Spore cloud drift - 3 frames ===
        [
            [" *  *  *  * ", "*  *  *  *  ", " *  *  *  * "],
            ["*  *  *  *  ", " *  *  *  * ", "  *  *  *  *"],
            ["  *  *  *  *", "*  *  *  *  ", " *  *  *  * "],
        ],
        # === ANIMATED: Mycelium network pulse - 2 frames ===
        [
            ["~+~+~+~+~+~+~", "+~+~+~+~+~+~+"],
            ["+~+~+~+~+~+~+", "~+~+~+~+~+~+~"],
        ],
        # Giant bioluminescent toadstool
        ["    /=========\\    ", "   /* * * * * *\\   ", "  |  *  *  *  * |  ",
         "      |||||||       ", "      |||||||       ", "      |||||||       "],
        # Tall thin mushroom cluster
        [" @    @    @  ", " |    |    |  ", " |    |    |  "],
        # Fairy ring of small mushrooms
        ["  ^ ^ ^ ^  ", " ^       ^ ", "  ^ ^ ^ ^  "],
        # Glowing underground pool
        ["  *~*~*~*~*  ", " *~*~*~*~*~* "],
    ],
    "Sunny Meadow": [
        # === ANIMATED: Wildflower sway - 2 frames ===
        [
            ["* * * * * * *", "| | | | | | |", "'''''''''''"],
            ["* * * * * * *", "/ / / / / / /", "'''''''''''"],
        ],
        # === ANIMATED: Bees buzzing - 2 frames ===
        [
            [" z 8 z 8 z ", "8 z 8 z 8  ", " z 8 z 8 z "],
            [" 8 z 8 z 8 ", "z 8 z 8 z  ", " 8 z 8 z 8 "],
        ],
        # Sunflower grove
        [" (*) (*) (*) ", " ||| ||| ||| ", " ||| ||| ||| ", "''|'''|'''|''"],
        # Picnic blanket
        ["+===========+", "|| [] [] [] ||", "||           ||", "+===========+"],
        # Wooden fence row
        ["|   |   |   |   |", "+---+   +---+   +"],
        # Beehive on a post
        ["  +---+  ", " /zzzzz\\ ", "|zzzzzz| ", " \\====/ ", "   ||   "],
    ],
    "Butterfly Garden": [
        # === ANIMATED: Butterfly wings flutter - 2 frames ===
        [
            ["V W  V W  V", " W V  W V ", "V W  V W  V"],
            ["W V  W V  W", " V W  V W ", "W V  W V  W"],
        ],
        # === ANIMATED: Chrysalis shudder - 3 frames ===
        [
            [" o   o   o ", " |   |   | ", " +   +   + "],
            ["(o)  o  (o)", " |   |   | ", " +   +   + "],
            [" o  (o)  o ", " |   |   | ", " +   +   + "],
        ],
        # Glass conservatory frame
        ["+==================+", "|* * V * W * V * * |", "|* W * * * V * W * |",
         "+==================+"],
        # Trellis arch with climbing roses
        [" /+++++++++++++\\ ", "|* * * * * * * |", "|  (*) (*) (*) |", "++           +++"],
        # Potted flowers on a shelf
        ["(*) (*) (*)", " |   |   | ", "[+] [+] [+]"],
    ],
    "Pebble Beach": [
        # === ANIMATED: Skip ripple rings expanding - 4 frames ===
        [
            ["    .    ", "   .o.   ", "    .    "],
            ["   . .   ", "  .~o~.  ", "   . .   "],
            ["  . ~ .  ", " .~.o.~. ", "  . ~ .  "],
            [" . ~ ~ . ", ".~. o .~.", " . ~ ~ . "],
        ],
        # === ANIMATED: Wave foam retreating - 3 frames ===
        [
            ["~~~~~===========~~~~~"],
            ["~~~~============~~~~~"],
            ["~~~~~===========~~~~~"],
        ],
        # Champion stone stacking tower
        ["     o     ", "    ooo    ", "   ooooo   ", "  ooooooo  ", " ooooooooo "],
        # Driftwood seat
        ["============", "/%%%%%XXX%%%\\"],
        # Curated shell collection
        ["(@) * (@) @ (@)", " @  (@)  *  @  "],
        # Local skip score board
        ["+===========+", "| BEST: 5sk |", "+===========+"],
    ],
    "Waterfall": [
        # === ANIMATED: Cascading waterfall - 4 frames ===
        [
            ["    +========+    ", "    |||||||||||||  ", "    |||||||||||||  ",
             "    |||||||||||||  ", "  ~~|||||||||||||~~", "  ~~~~~~~~~~~~~~~~~"],
            ["    +========+    ", "    |||||||||||||  ", "    |||||||||||||  ",
             "    |||||||||||||  ", " ~~~|||||||||||||~~", "  ~~~~~~~~~~~~~~~~~"],
            ["    +========+    ", "    |||||||||||||  ", "    |||||||||||||  ",
             "    |||||||||||||  ", "  ~~|||||||||||||~~", "  ~~~~~~~~~~~~~~~~~~"],
            ["    +========+    ", "    |||||||||||||  ", "    |||||||||||||  ",
             "    |||||||||||||  ", "~~~~|||||||||||||~~", "  ~~~~~~~~~~~~~~~~~"],
        ],
        # === ANIMATED: Mist slowly billowing - 3 frames ===
        [
            ["* * * * * * *", " * * * * * * ", "* * * * * * *"],
            [" * * * * * * ", "* * * * * * *", " * * * * * * "],
            ["* * * * * * *", " * * * * * * ", "* * * * * * *"],
        ],
        # Hidden cave entrance behind the falls
        [" [#######] ", " |       | ", " |  ???  | ", " [#######] "],
        # Wet rocks in the pool
        [" O  O  O  O ", "............"],
        # Rainbow in the mist spray
        ["   *  *  *   ", "  * * * * *  ", "   *  *  *   "],
    ],
    "Vegetable Patch": [
        # === ANIMATED: Scarecrow waving in wind - 2 frames ===
        [
            ["      +       ", "    / | \\     ", "   /  |  \\    ", "      |       ",
             "     /|\\      "],
            ["      +       ", "    \\ | /     ", "   \\  |  /    ", "      |       ",
             "     /|\\      "],
        ],
        # === ANIMATED: Irrigation channel trickle - 3 frames ===
        [
            [" ~~~~~~~~~ ", "[  ~~~~~  ]"],
            [" ~~~~~~~~~ ", "[  ~~~~   ]"],
            [" ~~~~~~~~~ ", "[  ~~~~~  ]"],
        ],
        # Cabbage row
        ["@ @ @ @ @ @ @", "+++++++++++++++"],
        # Tomato trellis stakes
        [" o   o   o   o ", " Y   Y   Y   Y ", " |   |   |   | "],
        # Bean poles with climbing vines
        ["  +   +   +  ", " /|  /|  /|  ", "+ |  + |  + |"],
        # Herb spiral garden feature
        ["    +++    ", "  +[*]*+   ", " +*[+]+*+  ", "  +[*]*+   ", "    +++    "],
    ],
    "Tool Shed": [
        # === ANIMATED: Corner cobweb swaying - 2 frames ===
        [
            ["=====  ", "  \\/   ", " \\ \\  ", "  = =  "],
            ["=====  ", "  \\/   ", " / /  ", "  = =  "],
        ],
        # Main shed building
        ["   /=========\\   ", "  |  +-----+  |  ", " |   |     |   | ",
         " |   +-----+   | ", " +===========+ "],
        # Pegboard tool wall
        ["T  /  \\  T  /  \\ ", "   |  |     |  |  ", "   |  |     |  |  "],
        # Cluttered workbench
        ["+==================+", "|| []=  # []  =  [] ||", "||  ||  =====  ||   ||",
         "+==================+"],
        # Loaded wheelbarrow
        ["  +========+  ", "  |@@^o^@@@|  ", " \\          // ", "  [O]====[O]  "],
        # Stacked clay pots
        ["    []    ", "   [][]   ", "  [][][]  "],
    ],
    "Foothills": [
        # === ANIMATED: Alpine pine sway - 2 frames ===
        [
            ["    A    ", "   AAA   ", "  AAAAA  ", "    |    "],
            ["   A     ", "   AAA   ", "  AAAAA  ", "    |    "],
        ],
        # === ANIMATED: Peak mist rolling - 3 frames ===
        [
            ["    ***    ", "   /^^^^\\  ", "  /      \\ "],
            ["    **+    ", "   /^^^^\\  ", "  /      \\ "],
            ["    ***    ", "   /^^^^\\  ", "  /      \\ "],
        ],
        # Mountain range backdrop
        ["       /\\  /\\     /\\     ", "      /  \\/  \\   /  \\    ",
         "     / ***  *.\\/***.*\\   ", "    /               \\    "],
        # Rocky outcrop with cave mouth
        [" O  O  O  O  O ", "OOOOOOOOOOOOOOO", "OOO [   ] OOOO"],
        # Alpine snowmelt stream
        ["=========~===~===", " =======~=~=====  "],
        # Edelweiss patch
        ["* * * * * *", "+ + + + + +"],
    ],
    "Crystal Cave": [
        # === ANIMATED: Crystal facet shimmer - 4 frames ===
        [
            ["  <><><>  ", " <><><><> ", "<><><><><>"],
            ["  <><><>  ", " <>*<><>  ", "<><><><><>"],
            ["  <>*<>   ", " <><><><> ", "<><><>*<><>"],
            ["  <><><>  ", " <><><><> ", "<>*<><><><>"],
        ],
        # === ANIMATED: Stalactite drip falling - 4 frames ===
        [
            ["V  V  V  V  V", "|  |  |  |  |", "             ",
             "|  |  |  |  |", "A  A  A  A  A"],
            ["V  V  V  V  V", "|  ;  |  |  |", "             ",
             "|  |  |  |  |", "A  A  A  A  A"],
            ["V  V  V  V  V", "|  .  |  |  |", "  .          ",
             "|  |  |  |  |", "A  A  A  A  A"],
            ["V  V  V  V  V", "|     |  |  |", "  *          ",
             "|  |  |  |  |", "A  A  A  A  A"],
        ],
        # Cathedral geode formation
        ["         /\\         ", "        /<>\\        ", "       /<><>\\       ",
         "      /<><><>\\      ", "     |<>*<>*<>|     ", "     |<><><><>|     ",
         "      \\______/      "],
        # Glowing underground lake
        ["~*~*~*~*~*~*~*~*~*~", "*~*~*~*~*~*~*~*~*~*", "~*~*~*~*~*~*~*~*~*~"],
        # Crystal column
        ["   /\\   ", "  /  \\  ", " |<><>| ", " |<><>| ", "  \\  /  ", "   \\/   "],
    ],
    "Sandy Shore": [
        # === ANIMATED: Palm tree fronds swaying - 3 frames ===
        [
            ["   \\|/   ", "    |    ", "    |    ", "    |    ", "   ===   "],
            ["    \\|   ", "    |    ", "    |    ", "    |    ", "   ===   "],
            ["   \\|/   ", "    |    ", "    |    ", "    |    ", "   ===   "],
        ],
        # === ANIMATED: Wave rolling in - 4 frames ===
        [
            ["~~~~~===========~~~~~"],
            [" ~~~~============~~~~"],
            ["  ~~~=============~~~"],
            [" ~~~~============~~~~"],
        ],
        # Sandcastle with flag
        ["  +--+--+--+  ", " /|  |[o]|  \\ ", "| |  |   |  | |", "++==========++",
         ".............."],
        # Rock pool with starfish inside
        ["  o  o  o ", " o ~~~~~~ o", "o ~*(*)~ o ", " o ~~~~~~ o", "  o  o  o "],
        # Resident crab
        ["  __C__  ", " / ||| \\ ", "(_/   \\_)"],
    ],
    "Shipwreck Cove": [
        # === ANIMATED: Jolly Roger flag fluttering - 4 frames ===
        [
            ["+--+", "|XX|", "|X  |", " || "],
            ["+--+", "| XX|", "| XX|", " || "],
            ["+--+", "|XX |", "|  X|", " || "],
            ["+--+", "|XX|", "| XX|", " || "],
        ],
        # === ANIMATED: Wave crash burst - 3 frames ===
        [
            ["~~~~~~~", " ~~~~~ ", "  ~~~  "],
            ["~~~*~~~", " ~~~~~ ", "  ~~~  "],
            ["~~~~~~~", " ~~~~~ ", "  ~~~  "],
        ],
        # Wrecked hull dominating the cove
        ["     /\\      ", "    /#\\      ", "   /###\\     ", "  /=====\\    ",
         " |#######|   ", " |#######|   ", "  \\=====/    "],
        # Half-buried treasure chest
        [" +======+ ", "|$<>*<>$| ", "+======+  ", ".......... "],
        # Scattered barrels
        ["(O)(O) (O) ", " (O) (O)   "],
        # Barnacle-covered rocks
        ["O.O.O.O.O  ", ".O.O.O.O.  "],
    ],
    "Misty Marsh": [
        # === ANIMATED: Firefly blink (independent) - 4 frames ===
        [
            [" *       *      ", "   *   *   *    ", "     *       *  "],
            ["   *   *        ", " *       *   *  ", "   *   *        "],
            ["*       *   *   ", "   *       *    ", " *   *       *  "],
            ["   *   *        ", "*       *   *   ", "   *       *    "],
        ],
        # === ANIMATED: Fog bank drifting - 2 frames ===
        [
            [". . . . . . . . .", " . . . . . . . . "],
            [" . . . . . . . . ", ". . . . . . . . ."],
        ],
        # Dead tree stark silhouette
        ["    /\\    ", "   /  \\   ", "  /    \\  ", "    ||    ", "    ||    ",
         "    ||    "],
        # Dark bog pool
        ["  ==========  ", " ~============ ", "~~============~~"],
        # Frog on floating log
        ["========", "|  (@)  |", "~~~~~~~~~"],
        # Will-o-wisp orb
        ["  (*)  ", " (*.*) ", "  (*)  "],
    ],
    "Cypress Hollow": [
        # === ANIMATED: Spanish moss curtain sway - 3 frames ===
        [
            ["= = = = = = = =", " = = = = = = = "],
            [" = = = = = = = ", "  = = = = = = ="],
            ["= = = = = = = =", " = = = = = = = "],
        ],
        # Wide ancient cypress trunk
        ["   /====\\   ", "  /||||||\\ ", " | |||||| | ", " | |||||| | ",
         " | |||||| | "],
        # Hollow log with fireflies inside
        ["+==========+", "|| * * * * ||", "+==========+"],
        # Dugout swamp boat
        ["  /========\\  ", " /          \\ ", "/============\\"],
        # Cypress knee cluster
        [" /\\ /\\ /\\ /\\ ", "/  \\/  \\/  \\ "],
        # Hunting heron silhouette
        ["  /  ", " /   ", " |   ", " |   ", "/ \\  "],
    ],
    "Sunken Ruins": [
        # === ANIMATED: Rune glow moving between columns - 3 frames ===
        [
            ["|     |     |     |", "|     |     |     |", "|     |     |     |",
             "+=====+=====+=====+"],
            ["|  .  |     |     |", "|     |     |     |", "|     |     |     |",
             "+=====+=====+=====+"],
            ["|     |  .  |     |", "|     |     |  .  |", "|     |     |     |",
             "+=====+=====+=====+"],
        ],
        # Submerged archway
        ["+=====+", "| ~~~ |", "+     +"],
        # Eroded ancient statue
        ["  +===+  ", " |(OO) | ", " | ||  | ", "  +===+  ", " . . . . "],
        # Ancient artifact pile glinting
        ["  O  <>  O  ", " <> * $ <> ", "  O  <>  O  "],
        # Broken toppled pillar
        [" +=+ ", " |.| ", " |.| ", "====="],
    ],
    "Park Fountain": [
        # === ANIMATED: Fountain water arc - 4 frames ===
        [
            ["       +===+       ", "      /~~~~~\\      ", "     |~~~~~~~|     ",
             "     | ~ ~ ~ |     ", "    +=========+    ", "   |  o  *  o  |   ",
             "    +=========+    "],
            ["       +===+       ", "      /~~~~~\\      ", "     |~~.~~~~|     ",
             "     | ~ ~ ~ |     ", "    +=========+    ", "   |  o  *  o  |   ",
             "    +=========+    "],
            ["       +===+       ", "      /~~~~~\\      ", "     |~~~~~~~|     ",
             "     | ~.~ ~ |     ", "    +=========+    ", "   |  *  o  *  |   ",
             "    +=========+    "],
            ["       +===+       ", "      /~~~~~\\      ", "     |~~~~~~~|     ",
             "     | ~ ~.~ |     ", "    +=========+    ", "   |  o  *  o  |   ",
             "    +=========+    "],
        ],
        # === ANIMATED: Pigeon flock shuffling - 2 frames ===
        [
            [" v  v     v ", "   v    v   "],
            [" v     v    ", "   v  v   v "],
        ],
        # Victorian lamp post
        ["  (O)  ", "   |   ", "   |   ", "   |   ", " +=|=+ "],
        # Ornamental park bench
        ["+===========+", "|           |", "|           |", "++=========++"],
        # Topiary duck (secret easter egg)
        ["  ++++  ", " +>++++", "  ++++  ", "  +  +  "],
    ],
    "Rooftop Garden": [
        # === ANIMATED: Solar panel sun track glint - 4 frames ===
        [
            ["/=========\\", "||[=][=][=]||", "||[=][=][=]||", "\\=========/"],
            ["/=========\\", "||[.][=][=]||", "||[=][=][=]||", "\\=========/"],
            ["/=========\\", "||[=][.][=]||", "||[=][=][=]||", "\\=========/"],
            ["/=========\\", "||[=][=][.]||", "||[=][=][=]||", "\\=========/"],
        ],
        # Raised vegetable beds (side by side)
        ["+------+  +------+", "| ++++ |  | ^^^^ |", "| ++++ |  | ^^^^ |",
         "+------+  +------+"],
        # Urban beehive
        ["  +---+  ", " /zzzzz\\ ", "|zzzBzzz| ", " \\=====/ "],
        # City skyline backdrop
        ["## ##   ### ##   ##", "## ## # ### ## # ##", "###########  ######"],
        # Rainwater collection barrel
        ["  +===+  ", " | ~ ~ | ", " | ~ ~ | ", "  +===+  "],
    ],
    "Storm Drain": [
        # === ANIMATED: Light shafts through grate shifting - 3 frames ===
        [
            ["+=+=+=+=+=+=+=+", "| | | | | | | |", "| | | | | | | |", "+=+=+=+=+=+=+=+"],
            ["+=+=+=+=+=+=+=+", "| |.| | | | | |", "| | | | |.| | |", "+=+=+=+=+=+=+=+"],
            ["+=+=+=+=+=+=+=+", "| | | |.| | | |", "| |.| | | | |. ", "+=+=+=+=+=+=+=+"],
        ],
        # === ANIMATED: Stalactite drip drops falling - 4 frames ===
        [
            ["V  V * V * V", "|  |   |   |", "             "],
            ["V  V * V * V", "|  ;   |   |", "             "],
            ["V  V * V * V", "|  .   |   |", "  .          "],
            ["V  V * V * V", "|      |   |", "  *          "],
        ],
        # Dark tunnel stretching back
        ["+===========+", "|##%###%###%#|", "|##%###%###%#|", "|##% . #%###%|",
         "+===========+"],
        # Lost treasure pile
        ["  O  *  <>  ", "<> * O * <> ", "  * <> *    "],
        # Glowing drain fungus
        ["*.*.*.*.  ", ".*.*.*.*  "],
        # Resident rat (not hostile, he lives here)
        ["  (@)~~  ", " / | \\   ", "   o     "],
    ],
}



# ============================================================================
# COLORS BY LOCATION
# ============================================================================

def _get_location_colors(location: str) -> Dict[str, Callable]:
    """Get color functions for a location's elements."""
    colors = {
        "Home Pond": {
            "ground": lambda s: _term.green(s),      # Grassy land
            "water": lambda s: _term.bright_cyan(s), # Pond water
            "plant": lambda s: _term.bright_green(s),# Grass and plants
            "accent": lambda s: _term.bright_yellow(s),
            "scenery": lambda s: _term.green(s),     # Shore elements
            "shore": lambda s: _term.color(229)(s),  # Sandy shore edge
        },
        "Deep End": {
            "ground": lambda s: _term.color(24)(s),  # Dark blue
            "water": lambda s: _term.blue(s),
            "plant": lambda s: _term.green(s),
            "accent": lambda s: _term.cyan(s),
            "scenery": lambda s: _term.color(24)(s),
        },
        "Forest Edge": {
            "ground": lambda s: _term.color(130)(s),  # Brown
            "water": lambda s: _term.bright_cyan(s),
            "plant": lambda s: _term.bright_green(s),
            "tree": lambda s: _term.green(s),
            "accent": lambda s: _term.yellow(s),
            "scenery": lambda s: _term.green(s),
        },
        "Ancient Oak": {
            "ground": lambda s: _term.color(130)(s),  # Brown
            "plant": lambda s: _term.green(s),
            "tree": lambda s: _term.color(22)(s),  # Dark green
            "accent": lambda s: _term.color(130)(s),
            "scenery": lambda s: _term.color(22)(s),
        },
        "Mushroom Grove": {
            "ground": lambda s: _term.color(130)(s),
            "plant": lambda s: _term.magenta(s),
            "accent": lambda s: _term.bright_magenta(s),
            "scenery": lambda s: _term.magenta(s),
        },
        "Sunny Meadow": {
            "ground": lambda s: _term.green(s),
            "plant": lambda s: _term.bright_green(s),
            "flower": lambda s: _term.bright_yellow(s),
            "accent": lambda s: _term.bright_magenta(s),
            "scenery": lambda s: _term.bright_yellow(s),
        },
        "Butterfly Garden": {
            "ground": lambda s: _term.green(s),
            "plant": lambda s: _term.bright_green(s),
            "flower": lambda s: _term.bright_magenta(s),
            "accent": lambda s: _term.bright_cyan(s),
            "scenery": lambda s: _term.bright_magenta(s),
        },
        "Pebble Beach": {
            "ground": lambda s: _term.color(250)(s),  # Gray
            "water": lambda s: _term.bright_cyan(s),
            "accent": lambda s: _term.white(s),
            "scenery": lambda s: _term.color(250)(s),
        },
        "Waterfall": {
            "ground": lambda s: _term.color(250)(s),
            "water": lambda s: _term.bright_cyan(s),
            "accent": lambda s: _term.bright_white(s),
            "scenery": lambda s: _term.bright_cyan(s),
        },
        "Vegetable Patch": {
            "ground": lambda s: _term.color(94)(s),  # Soil brown
            "plant": lambda s: _term.bright_green(s),
            "accent": lambda s: _term.red(s),
            "scenery": lambda s: _term.color(94)(s),
        },
        "Tool Shed": {
            "ground": lambda s: _term.color(240)(s),  # Gray floor
            "wood": lambda s: _term.color(130)(s),
            "accent": lambda s: _term.color(250)(s),
            "scenery": lambda s: _term.color(130)(s),
        },
        "Foothills": {
            "ground": lambda s: _term.color(250)(s),  # Rocky gray
            "rock": lambda s: _term.color(240)(s),
            "plant": lambda s: _term.green(s),
            "accent": lambda s: _term.white(s),
            "scenery": lambda s: _term.color(240)(s),
        },
        "Crystal Cave": {
            "ground": lambda s: _term.color(236)(s),  # Dark
            "crystal": lambda s: _term.bright_cyan(s),
            "accent": lambda s: _term.bright_magenta(s),
            "scenery": lambda s: _term.bright_cyan(s),
        },
        "Sandy Shore": {
            "ground": lambda s: _term.color(229)(s),  # Sandy yellow
            "water": lambda s: _term.bright_cyan(s),
            "accent": lambda s: _term.bright_white(s),
            "scenery": lambda s: _term.bright_cyan(s),
        },
        "Shipwreck Cove": {
            "ground": lambda s: _term.color(229)(s),
            "water": lambda s: _term.cyan(s),
            "wood": lambda s: _term.color(130)(s),
            "accent": lambda s: _term.color(220)(s),  # Gold
            "scenery": lambda s: _term.color(130)(s),
        },
        # Swamp colors - murky greens and mysterious glows
        "Misty Marsh": {
            "ground": lambda s: _term.color(22)(s),   # Dark green
            "water": lambda s: _term.color(23)(s),    # Murky teal
            "plant": lambda s: _term.color(28)(s),    # Swamp green
            "accent": lambda s: _term.bright_yellow(s),  # Firefly glow
            "scenery": lambda s: _term.color(22)(s),
        },
        "Cypress Hollow": {
            "ground": lambda s: _term.color(58)(s),   # Brown-green
            "water": lambda s: _term.color(23)(s),    # Dark teal
            "plant": lambda s: _term.color(28)(s),    # Moss green
            "accent": lambda s: _term.bright_yellow(s),  # Firefly
            "scenery": lambda s: _term.color(65)(s),  # Muted green
        },
        "Sunken Ruins": {
            "ground": lambda s: _term.color(236)(s),  # Dark stone
            "water": lambda s: _term.color(23)(s),    # Murky
            "stone": lambda s: _term.color(244)(s),   # Gray stone
            "accent": lambda s: _term.cyan(s),        # Ancient glow
            "scenery": lambda s: _term.color(244)(s),
        },
        # Urban colors - grays and city tones
        "Park Fountain": {
            "ground": lambda s: _term.color(250)(s),  # Pavement gray
            "water": lambda s: _term.bright_cyan(s),  # Clean water
            "plant": lambda s: _term.bright_green(s), # Maintained plants
            "accent": lambda s: _term.bright_yellow(s),  # Coins
            "scenery": lambda s: _term.color(250)(s),
        },
        "Rooftop Garden": {
            "ground": lambda s: _term.color(240)(s),  # Concrete
            "plant": lambda s: _term.bright_green(s), # Healthy plants
            "flower": lambda s: _term.bright_magenta(s),
            "accent": lambda s: _term.bright_yellow(s),
            "scenery": lambda s: _term.green(s),
        },
        "Storm Drain": {
            "ground": lambda s: _term.color(236)(s),  # Dark concrete
            "water": lambda s: _term.color(24)(s),    # Dim water
            "accent": lambda s: _term.bright_yellow(s),  # Lost treasures
            "scenery": lambda s: _term.color(240)(s),
        },
    }
    return colors.get(location, {
        "ground": lambda s: s,
        "accent": lambda s: _term.white(s),
        "scenery": lambda s: s,
    })


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_ground_chars(location: str) -> List[str]:
    """Get ground pattern characters for a location."""
    return LOCATION_GROUND_CHARS.get(location, DEFAULT_GROUND_CHARS)


def get_decorations(location: str) -> List[Tuple[str, int]]:
    """Get decorations for a location with weights."""
    return LOCATION_DECORATIONS.get(location, DEFAULT_DECORATIONS)


def get_scenery(location: str) -> List[List[str]]:
    """Get large scenery elements for a location."""
    return LOCATION_SCENERY.get(location, [])


def get_location_colors(location: str) -> Dict[str, Callable]:
    """Get color functions for a location."""
    return _get_location_colors(location)


def generate_location_ground(location: str, width: int, height: int) -> List[str]:
    """Generate ground pattern for a specific location."""
    chars = get_ground_chars(location)
    pattern = []
    for y in range(height):
        row = ""
        for x in range(width):
            row += random.choice(chars)
        pattern.append(row)
    return pattern


def generate_location_decorations(location: str, width: int, height: int, 
                                   count: int = 10) -> List[Tuple[int, int, str]]:
    """Generate random decoration placements for a location.
    
    Returns: List of (x, y, char) tuples
    """
    decorations = get_decorations(location)
    if not decorations:
        return []
    
    # Build weighted list
    weighted_chars = []
    for char, weight in decorations:
        weighted_chars.extend([char] * weight)
    
    placements = []
    for _ in range(count):
        x = random.randint(2, width - 3)
        y = random.randint(2, height - 3)
        char = random.choice(weighted_chars)
        placements.append((x, y, char))
    
    return placements


def generate_location_scenery(location: str, width: int, height: int) -> List[Tuple[int, int, List]]:
    """Generate large scenery placements for a location.

    Returns: List of (x, y, piece) tuples where piece is either List[str]
    (static) or List[List[str]] (animated frames).
    """
    scenery_pieces = get_scenery(location)
    if not scenery_pieces:
        return []

    # Special layout generators
    if location == "Forest Edge":
        return _generate_forest_edge_scenery(scenery_pieces, width, height)
    elif location == "Home Pond":
        return _generate_home_pond_scenery(scenery_pieces, width, height)
    elif location == "Ancient Oak":
        return _generate_ancient_oak_scenery(scenery_pieces, width, height)
    elif location == "Crystal Cave":
        return _generate_crystal_cave_scenery(scenery_pieces, width, height)
    elif location == "Misty Marsh":
        return _generate_misty_marsh_scenery(scenery_pieces, width, height)
    elif location == "Shipwreck Cove":
        return _generate_shipwreck_cove_scenery(scenery_pieces, width, height)

    # Default: place 2-4 pieces spread across the world
    num_pieces = random.randint(2, min(4, len(scenery_pieces)))
    used_positions = set()
    placements = []

    for piece in random.sample(scenery_pieces, num_pieces):
        frame0 = _first_frame(piece)
        piece_width = max(len(line) for line in frame0) if frame0 else 4
        piece_height = len(frame0) if frame0 else 2

        for _ in range(12):
            x = random.randint(1, max(1, width - piece_width - 2))
            y = random.randint(1, max(1, height - piece_height - 2))
            overlap = any(
                abs(x - px) < piece_width + 3 and abs(y - py) < piece_height + 2
                for px, py in used_positions
            )
            if not overlap:
                placements.append((x, y, piece))
                used_positions.add((x, y))
                break

    return placements


def _first_frame(piece) -> List[str]:
    """Return the first frame lines for filtering/sizing animated or static pieces."""
    if piece and isinstance(piece[0], list):
        return piece[0]  # animated: first frame is List[str]
    return piece          # static: piece itself is List[str]


def _generate_forest_edge_scenery(scenery_pieces, width: int, height: int):
    """Forest Edge: animated treeline top, animated river across the floor, landmarks."""
    placements = []

    def has_char(piece, ch):
        return any(ch in line for line in _first_frame(piece))

    animated_river = [p for p in scenery_pieces if isinstance(p[0], list) and
                      any('=' in line or '~' in line for line in p[0])]
    animated_trees = [p for p in scenery_pieces if isinstance(p[0], list) and
                      any('A' in line for line in p[0])]
    static_river   = [p for p in scenery_pieces if not isinstance(p[0], list) and
                      any('=' in line or '~' in line for line in p)]
    static_trees   = [p for p in scenery_pieces if not isinstance(p[0], list) and
                      any('A' in line for line in p)]
    static_other   = [p for p in scenery_pieces if not isinstance(p[0], list) and
                      not any('A' in line for line in p) and
                      not any('=' in line or '~' in line for line in p)]

    # Place animated treeline across the top
    if animated_trees:
        tree = animated_trees[0]
        frame0 = _first_frame(tree)
        tw = max(len(l) for l in frame0)
        placements.append((random.randint(0, max(0, width - tw)), 0, tree))

    # Place animated river near the bottom
    if animated_river:
        river = animated_river[0]
        frame0 = _first_frame(river)
        rw = max(len(l) for l in frame0)
        rh = len(frame0)
        placements.append((random.randint(0, max(0, width - rw)), height - rh - 2, river))

    # Add 2-3 static pieces (bridge, log, signpost)
    for piece in random.sample(static_other + static_river, min(3, len(static_other + static_river))):
        frame0 = _first_frame(piece)
        pw = max(len(l) for l in frame0)
        ph = len(frame0)
        x = random.randint(1, max(1, width - pw - 2))
        y = random.randint(2, max(2, height - ph - 3))
        placements.append((x, y, piece))

    return placements


def _generate_home_pond_scenery(scenery_pieces, width: int, height: int):
    """Home Pond: animated water center, animated reeds flanking, dock top-right."""
    placements = []

    animated_water = [p for p in scenery_pieces if isinstance(p[0], list) and
                      any('~' in line for line in p[0])]
    animated_reeds = [p for p in scenery_pieces if isinstance(p[0], list) and
                      any('|' in line or 'Y' in line for line in p[0])]
    static_lily    = [p for p in scenery_pieces if not isinstance(p[0], list) and
                      any('O' in line and '~' in line for line in p)]
    static_dock    = [p for p in scenery_pieces if not isinstance(p[0], list) and
                      any('=' in line for line in p) and any('+' in line for line in p)]
    static_shore   = [p for p in scenery_pieces if not isinstance(p[0], list) and
                      any('.' in line for line in p) and
                      not any('~' in line or 'O' in line for line in p)]

    # Animated water surface - centered
    if animated_water:
        w = animated_water[0]
        f = _first_frame(w)
        ww = max(len(l) for l in f)
        wh = len(f)
        placements.append(((width - ww) // 2, (height - wh) // 2, w))

    # Animated reed sway - left edge
    if animated_reeds:
        r = animated_reeds[0]
        f = _first_frame(r)
        rh = len(f)
        placements.append((1, height - rh - 1, r))

    # Animated reed sway - right edge
    if len(animated_reeds) > 0:
        r = animated_reeds[0]
        f = _first_frame(r)
        rw = max(len(l) for l in f)
        rh = len(f)
        placements.append((width - rw - 2, height - rh - 1, r))

    # Lily pads on water
    if static_lily:
        lily = static_lily[0]
        lw = max(len(l) for l in lily)
        lh = len(lily)
        placements.append(((width - lw) // 2, (height - lh) // 2 - 1, lily))

    # Dock - top right corner
    if static_dock:
        dock = static_dock[0]
        dw = max(len(l) for l in dock)
        placements.append((width - dw - 1, 0, dock))

    # Shore pebbles - bottom center
    if static_shore:
        shore = static_shore[0]
        sw = max(len(l) for l in shore)
        sh = len(shore)
        placements.append(((width - sw) // 2, height - sh, shore))

    return placements


def _generate_ancient_oak_scenery(scenery_pieces, width: int, height: int):
    """Ancient Oak: animated canopy dominates top-center, creatures scattered below."""
    placements = []

    animated_canopy  = [p for p in scenery_pieces if isinstance(p[0], list) and
                        any('A' in line for line in p[0])]
    animated_owl     = [p for p in scenery_pieces if isinstance(p[0], list) and
                        any('O' in line and '+' in line for line in p[0])]
    static_roots     = [p for p in scenery_pieces if not isinstance(p[0], list) and
                        any('\\/' in line or '/\\' in line for line in p)]
    static_rest      = [p for p in scenery_pieces if not isinstance(p[0], list) and
                        not any('A' in line for line in p)]

    # Animated canopy - centered top
    if animated_canopy:
        c = animated_canopy[0]
        f = _first_frame(c)
        cw = max(len(l) for l in f)
        placements.append(((width - cw) // 2, 0, c))

    # Animated owl knothole - slightly left of center, mid-height
    if animated_owl:
        o = animated_owl[0]
        f = _first_frame(o)
        ow = max(len(l) for l in f)
        oh = len(f)
        placements.append(((width - ow) // 2 - 4, height // 2 - oh // 2, o))

    # Roots at ground level
    if static_roots:
        r = static_roots[0]
        rw = max(len(l) for l in r)
        rh = len(r)
        placements.append(((width - rw) // 2, height - rh, r))

    # Scatter remaining static pieces
    for piece in random.sample(static_rest, min(3, len(static_rest))):
        f = _first_frame(piece)
        pw = max(len(l) for l in f)
        ph = len(f)
        x = random.randint(2, max(2, width - pw - 2))
        y = random.randint(height // 3, max(height // 3, height - ph - 1))
        placements.append((x, y, piece))

    return placements


def _generate_crystal_cave_scenery(scenery_pieces, width: int, height: int):
    """Crystal Cave: animated crystals and drips flanking a central geode."""
    placements = []

    animated_shimmer = [p for p in scenery_pieces if isinstance(p[0], list) and
                        any('<' in line for line in p[0])]
    animated_drip    = [p for p in scenery_pieces if isinstance(p[0], list) and
                        any('V' in line for line in p[0])]
    static_geode     = [p for p in scenery_pieces if not isinstance(p[0], list) and
                        any('/' in line and '\\' in line for line in p)]
    static_lake      = [p for p in scenery_pieces if not isinstance(p[0], list) and
                        any('*' in line and '~' in line for line in p)]
    static_rest      = [p for p in scenery_pieces if not isinstance(p[0], list) and
                        p not in static_geode and p not in static_lake]

    # Central geode
    if static_geode:
        g = static_geode[0]
        gw = max(len(l) for l in g)
        gh = len(g)
        placements.append(((width - gw) // 2, (height - gh) // 2, g))

    # Animated crystal shimmer - left cluster
    if animated_shimmer:
        s = animated_shimmer[0]
        f = _first_frame(s)
        sw = max(len(l) for l in f)
        placements.append((2, height // 3, s))
        placements.append((width - sw - 3, height // 3, s))

    # Animated stalactite drip - top area
    if animated_drip:
        d = animated_drip[0]
        f = _first_frame(d)
        dw = max(len(l) for l in f)
        placements.append(((width - dw) // 2, 0, d))

    # Glowing lake near bottom
    if static_lake:
        lake = static_lake[0]
        lw = max(len(l) for l in lake)
        lh = len(lake)
        placements.append(((width - lw) // 2, height - lh - 1, lake))

    return placements


def _generate_misty_marsh_scenery(scenery_pieces, width: int, height: int):
    """Misty Marsh: animated fireflies fill the space, fog at top, landmarks scattered."""
    placements = []

    animated_firefly = [p for p in scenery_pieces if isinstance(p[0], list) and
                        any('*' in line for line in p[0])]
    animated_fog     = [p for p in scenery_pieces if isinstance(p[0], list) and
                        any('.' in line for line in p[0])]
    static_pieces    = [p for p in scenery_pieces if not isinstance(p[0], list)]

    # Fog drifting at the top
    if animated_fog:
        placements.append((0, 0, animated_fog[0]))

    # Fireflies clustered in two patches
    if animated_firefly:
        ff = animated_firefly[0]
        f = _first_frame(ff)
        fw = max(len(l) for l in f)
        fh = len(f)
        placements.append((width // 5, height // 3, ff))
        placements.append((width * 3 // 5, height // 2, ff))

    # Scatter static landmarks
    for piece in random.sample(static_pieces, min(4, len(static_pieces))):
        f = _first_frame(piece)
        pw = max(len(l) for l in f)
        ph = len(f)
        x = random.randint(2, max(2, width - pw - 2))
        y = random.randint(2, max(2, height - ph - 2))
        placements.append((x, y, piece))

    return placements


def _generate_shipwreck_cove_scenery(scenery_pieces, width: int, height: int):
    """Shipwreck Cove: hull dominates right side, flag flies above, waves and debris left."""
    placements = []

    animated_flag  = [p for p in scenery_pieces if isinstance(p[0], list) and
                      any('X' in line for line in p[0])]
    animated_wave  = [p for p in scenery_pieces if isinstance(p[0], list) and
                      any('~' in line for line in p[0])]
    static_hull    = [p for p in scenery_pieces if not isinstance(p[0], list) and
                      any('#' in line for line in p) and len(p) > 4]
    static_rest    = [p for p in scenery_pieces if not isinstance(p[0], list) and
                      p not in static_hull]

    # Hull - right-center
    if static_hull:
        h = static_hull[0]
        hw = max(len(l) for l in h)
        hh = len(h)
        hx = width - hw - 3
        hy = (height - hh) // 2
        placements.append((hx, hy, h))

        # Flag above the hull mast
        if animated_flag:
            ff = animated_flag[0]
            f = _first_frame(ff)
            fw = max(len(l) for l in f)
            placements.append((hx + hw // 2 - fw // 2, max(0, hy - len(f)), ff))

    # Animated waves - left side
    if animated_wave:
        wv = animated_wave[0]
        f = _first_frame(wv)
        wh = len(f)
        placements.append((2, height - wh - 2, wv))
        placements.append((width // 3, height - wh - 2, wv))

    # Scatter debris
    for piece in random.sample(static_rest, min(3, len(static_rest))):
        f = _first_frame(piece)
        pw = max(len(l) for l in f)
        ph = len(f)
        x = random.randint(2, max(2, width // 2 - pw))
        y = random.randint(2, max(2, height - ph - 2))
        placements.append((x, y, piece))

    return placements


# ============================================================================
# DECORATION CHARACTER COLORS
# ============================================================================

def get_decoration_color(location: str, char: str, season: str = None) -> Optional[Callable]:
    """Get the color function for a specific decoration character.

    If *season* is provided, seasonal colour overrides are checked first for
    characters that change with the seasons (trees, bushes, grass, flowers).
    """
    # Check seasonal override first (only for chars that change: A, +, ', *)
    if season and char in ("A", "+", "'", "*"):
        from ui.biome_visuals import get_seasonal_decoration_color
        override = get_seasonal_decoration_color(char, season, location)
        if override:
            r, g, b = override
            return _term.color_rgb(r, g, b)

    # Water characters
    if char == "~":
        return _term.bright_cyan

    # = is context-dependent: water vs wood/dock
    if char == "=":
        if location in ("Home Pond", "Deep End", "Forest Edge", "Waterfall",
                        "Misty Marsh", "Cypress Hollow", "Sunken Ruins",
                        "Storm Drain", "Shipwreck Cove"):
            return _term.bright_cyan  # Water
        return _term.color(130)  # Brown wood/dock/structures

    # O is context-dependent by location
    if char == "O":
        if location in ("Home Pond",):
            return _term.bright_green  # Lily pad
        return _term.color(250)  # Gray - rocks, barrels, shells, artifacts

    # * is context-dependent by location
    if char == "*":
        if location in ("Home Pond", "Deep End"):
            return _term.bright_magenta  # Lily flowers
        if location in ("Crystal Cave",):
            return random.choice([_term.bright_white, _term.bright_cyan, _term.bright_magenta])
        if location in ("Sunny Meadow", "Butterfly Garden", "Park Fountain", "Rooftop Garden"):
            return random.choice([_term.bright_magenta, _term.bright_yellow, _term.bright_red])
        if location in ("Foothills", "Sandy Shore", "Waterfall"):
            return _term.bright_white  # Eagle, edelweiss, mist, starfish
        # Default for Misty Marsh, Cypress Hollow, Mushroom Grove, etc.
        return _term.bright_yellow  # Firefly/glow

    # Reeds and cattails
    if char == "|":
        return _term.green
    if char == "Y":
        return _term.color(130)  # Brown cattail tops

    # + and - are wood/dock
    if char in "+-":
        return _term.color(130)  # Brown wood

    # Plants/trees
    if char == "A":
        return _term.green

    # Crystals
    if char in "<>":
        return _term.bright_cyan

    # Rocks/pebbles
    if char == "o":
        return _term.color(250)  # Gray

    # ^ is context-dependent: mushroom vs mountain vs carrot
    if char == "^":
        if location in ("Foothills",):
            return _term.color(240)  # Dark gray mountain
        if location in ("Vegetable Patch", "Rooftop Garden"):
            return _term.green  # Carrot tops
        # Default: mushroom (Mushroom Grove, Ancient Oak, Misty Marsh)
        return random.choice([_term.red, _term.bright_red, _term.bright_magenta])

    # @ - mushrooms/round objects
    if char == "@":
        if location in ("Mushroom Grove", "Ancient Oak"):
            return random.choice([_term.red, _term.bright_red, _term.bright_magenta])
        return _term.green  # Sunflower/cabbage/squash/shell

    # / and \ - mountains/tools
    if char in "/\\":
        return _term.color(240)  # Dark gray

    # # and . - structures
    if char in "#.":
        return _term.color(130)  # Brown

    # Default - no color
    return None


def get_ground_color(location: str, season: str = None) -> Optional[Callable]:
    """Get the ground/background color for a location.

    If *season* is provided, a seasonal override is checked first.
    """
    if season:
        from ui.biome_visuals import get_seasonal_ground_color
        seasonal_idx = get_seasonal_ground_color(location, season)
        if seasonal_idx is not None:
            return _term.color(seasonal_idx)

    ground_colors = {
        "Home Pond": _term.color(22),       # Green-blue (grassy shore with pond)
        "Deep End": _term.color(17),        # Darker blue
        "Forest Edge": _term.color(22),     # Dark green (forest floor)
        "Ancient Oak": _term.color(94),     # Brown earth
        "Mushroom Grove": _term.color(53),  # Dark purple
        "Sunny Meadow": _term.color(28),    # Grass green
        "Butterfly Garden": _term.color(28), # Grass green
        "Pebble Beach": _term.color(250),   # Light gray
        "Waterfall": _term.color(24),       # Blue
        "Vegetable Patch": _term.color(94), # Soil brown
        "Tool Shed": _term.color(240),      # Gray floor
        "Foothills": _term.color(242),      # Rocky gray
        "Crystal Cave": _term.color(234),   # Very dark
        "Sandy Shore": _term.color(229),    # Sandy yellow
        "Shipwreck Cove": _term.color(180), # Sandy
        # Swamp locations
        "Misty Marsh": _term.color(22),     # Dark murky green
        "Cypress Hollow": _term.color(58),  # Brown-green swamp
        "Sunken Ruins": _term.color(236),   # Dark stone
        # Urban locations
        "Park Fountain": _term.color(250),  # Light gray pavement
        "Rooftop Garden": _term.color(240), # Concrete gray
        "Storm Drain": _term.color(234),    # Very dark
    }
    return ground_colors.get(location)

