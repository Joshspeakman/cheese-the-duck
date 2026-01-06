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
    # Home Pond - 70% grassy shore, 30% calm pond water with reeds
    "Home Pond": [" ", "'", ".", ",", " ", "~", "~", "~", " ", "|"],
    "Deep End": [" ", "~", "~", "=", ".", " ", "~", "=", " ", "."],
    
    # Forest - earthy with fallen leaves and twigs
    "Forest Edge": [" ", " ", ".", ",", "'", ".", " ", ".", " ", " "],
    "Ancient Oak": [" ", ".", ".", ",", "'", ".", ".", " ", " ", "."],
    "Mushroom Grove": [" ", ".", ".", "o", " ", ".", ",", " ", " ", "."],
    
    # Meadow - grassy and flowery
    "Sunny Meadow": [" ", " ", "'", ".", ".", ",", " ", "'", " ", " "],
    "Butterfly Garden": [" ", "'", ".", ",", ".", "'", ".", " ", ",", " "],
    
    # Riverside - sandy with pebbles
    "Pebble Beach": [" ", ".", ".", "o", " ", ".", ".", " ", ".", " "],
    "Waterfall": [" ", "~", ".", "=", "~", " ", ".", "~", " ", "="],
    
    # Garden - organized, clean
    "Vegetable Patch": [" ", " ", ".", ".", " ", "'", " ", ".", " ", " "],
    "Tool Shed": [" ", " ", ".", " ", ".", " ", " ", ".", " ", " "],
    
    # Mountains - rocky
    "Foothills": [" ", ".", ".", ".", " ", ".", ".", " ", " ", "."],
    "Crystal Cave": [" ", ".", "*", " ", ".", ".", "*", " ", " ", "."],
    
    # Beach - sandy with shells
    "Sandy Shore": [" ", " ", ".", ".", " ", "o", " ", ".", " ", " "],
    "Shipwreck Cove": [" ", ".", "~", ".", " ", "~", ".", " ", "=", " "],
    
    # Swamp - murky and mysterious
    "Misty Marsh": [" ", "~", ".", "=", " ", "~", ".", " ", "*", " "],
    "Cypress Hollow": [" ", ".", ".", "~", " ", ".", ".", "*", " ", " "],
    "Sunken Ruins": [" ", ".", "=", ".", " ", "~", ".", ".", " ", "."],
    
    # Urban - concrete and parks
    "Park Fountain": [" ", " ", ".", ".", " ", "'", " ", ".", " ", " "],
    "Rooftop Garden": [" ", "'", ".", ".", " ", "'", ".", " ", ".", " "],
    "Storm Drain": [" ", ".", ".", " ", ".", " ", ".", ".", " ", "."],
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

# Large scenery pieces that get placed in specific spots
LOCATION_SCENERY: Dict[str, List[List[str]]] = {
    "Home Pond": [
        # Large pond water area (central feature)
        ["~~~~~~~~~~~", "~~~~~~~~~~~", "~~~~~~~~~~~"],
        # Lily pad clusters floating on pond
        ["  ~  O  ~  O  ~  ", " ~ O ~ O ~ O ~ ", "  ~  O  ~  O  ~  "],
        # More lily pads with flowers
        [" O ~ O ~ O ", "~ O * O ~ ", " O ~ O ~ O "],
        # Reed cluster at water's edge (tall)
        ["| | | | |", "| | | | |", "| | | | |", "Y Y Y Y Y"],
        # Another reed cluster
        ["| | |", "| | |", "Y Y Y"],
        # Cattails along shore
        ["| | | | | |", "| | | | | |", "Y Y Y Y Y Y"],
        # Water edge with ripples
        ["~=~=~=~=~=~", " ~~~~~~~~~ "],
        # Small grassy shore patch
        ["' ' ' ' '", ".,.,.,.,.'"],
        # Cozy dock extending into water
        ["=======", "|     |", "+-----+"],
        # Pebble shore edge
        [". . . . . .", " . . . . . "],
    ],
    "Deep End": [
        # Murky deep waters with mysterious shapes
        ["#######~~~~~~~#######", " ###~~~~~~~~~### ", "  ~~~~~~~~~~~  "],
        # Sunken log with shadows
        ["   =====   ", "  /%%%%%\\  ", " /%%%%%%\\ "],
        # Fish silhouettes lurking
        ["  <><    ", "    <>< ", " <><   <><"],
        # Rising bubble columns
        ["  o     o  ", " o  o  o ", "o   o   o", "  o   o  "],
        # Shadow shapes in the deep
        [" ###%### ", "  #%#%#  ", "   %#%   "],
        # Mysterious treasure glint
        ["    *    ", "  . * .  ", " <>  *  <> "],
        # Deep underwater plants swaying
        [" Y  Y  Y ", "| || || |", "| || || |"],
        # Old sunken barrel
        ["  +===+  ", " |o o o| ", "  +=+=+  "],
        # Mystery creature shape
        ["   ???   ", "  ?????  ", " ??????? "],
        # Sunken treasure chest
        [" +====+ ", " |$$$$$| ", " +====+ "],
    ],
    "Forest Edge": [
        # Large tree left side
        ["    AAAAA    ", "   AAAAAAA   ", "      |      ", "      |      "],
        # Tree row (forest background)
        ["  A   A   A   A  ", "  |   |   |   |  "],
        # Long winding river across playfield
        ["~================~", " ~==============~ "],
        # River bend going down
        ["      ====~", "    ====~  ", "  ====~    ", "====~      "],
        # River bend going up
        ["===~        ", "  ===~      ", "    ===~    ", "      ====~~"],
        # Dense tree cluster
        [" A A A A ", "+|+|+|++"],
        # Bush row
        ["+ + + + +"],
        # Fallen log
        ["=======", "  ###  "],
        # Another tree
        ["   AAA   ", "  AAAAA  ", "    |    ", "    |    "],
        # Bridge over river
        ["+=========+", "||~~~~~~~||", "+=========+"],
    ],
    "Ancient Oak": [
        # Massive ancient oak tree with full canopy
        ["      AAAAAAAAAAA      ", "    AAAAAAAAAAAAAAA    ", "   AAAAAAAAAAAAAAAA   ", "         ||||         ", "         ||||         ", "         ||||         "],
        # Owl knothole with watching eyes
        ["  +---+  ", "  |O O|  ", "  | ^ |  ", "  +---+  "],
        # Squirrel on branch
        ["   ===@@   ", "  /    \\  ", " +      + "],
        # Bird nest with eggs
        ["  u u u  ", " (ooo) ", "  ===  "],
        # Acorns scattered on ground
        [" o  o  o ", "o  o  o  "],
        # Shelf mushrooms on trunk
        ["  |^|  ", " |^^| ", "  |||  "],
        # Woodpecker holes
        ["  |.|  ", " |. .| ", "  |.|  "],
        # Hanging vines
        ["~ ~ ~ ~", " ~ ~ ~ ", "~ ~ ~ ~"],
        # Root system
        ["/\\/\\/\\/\\", " \\/\\/\\/ "],
    ],
    "Mushroom Grove": [
        # Giant bioluminescent toadstool
        ["   +-----+   ", "  /  * *  \\  ", " |  *   *  | ", "     |||     ", "     |||     "],
        # Mushroom cluster (various sizes)
        ["  ^   @   ^  ", " |   |||   | ", " |   |||   | "],
        # Floating spore clouds
        [" *  *  * ", "*  *  *  ", "  *  *  *"],
        # Mycelium network on ground
        [" ~~+~~+~~+~~ ", "+~~+~~+~~+~~+"],
        # Shelf mushroom stairs
        ["      ^", "    ^^ ", "  ^^^  ", "^^^^   "],
        # Glowing moss patches
        [" *...* ", "...*..*"],
        # Tall thin mushrooms
        [" @  @  @ ", " |  |  | ", " |  |  | "],
        # Ring of small mushrooms
        ["  ^ ^ ^  ", " ^     ^ ", "  ^ ^ ^  "],
        # Puffball cluster
        [" (o) (o) (o) ", "  @   @   @  "],
    ],
    "Sunny Meadow": [
        # Large sunflower
        ["   (*)   ", "   |||   ", "   |||   ", "  ''|''  "],
        # Beehive on post
        ["  +---+  ", " /zzzzz\\ ", "|zzzzzz| ", " \\====/ ", "   ||   "],
        # Buzzing bees
        [" z 8 z ", "8 z 8 z", " z 8 z "],
        # Clover patch with lucky clover
        [" + + + + ", "+ + ++ + +", " + + + + "],
        # Tall wildflower row
        ["* * * * *", "| | | | |", "''''''''"],
        # Winding bee path
        ["  8   8  ", "   8z8   ", " 8   8   "],
        # Flower garden
        ["(*)(*)(*)", " | | | | ", "''''''''"],
        # Picnic blanket
        ["+-------+", "|[][][]|", "+-------+"],
    ],
    "Butterfly Garden": [
        # Glass conservatory frame
        ["+==============+", "|  *  *  *  * |", "|  +  +  +  + |", "+==============+"],
        # Trellis archway with vines
        [" /+++++++\\ ", "|* * * * *|", "|  A A A  |", "++       ++"],
        # Flutter of butterflies (V W shapes)
        ["V W  V W  ", " W V  W V ", "V W  V W  "],
        # Chrysalis row
        [" o   o   o ", " |   |   | ", " +   +   + "],
        # Nectar flower bed
        ["* * * * * *", " + + + + + ", "-----------"],
        # Resting platform
        ["+-------+", "| V W  |", "+-------+"],
        # Potted flowers
        ["(*)  (*)", " |    | ", "[+]  [+]"],
    ],
    "Pebble Beach": [
        # Skip ripples across water
        ["    . ~ . ~ .    ", "   ~ . ~ . ~    ", "  . ~ . ~ . ~   "],
        # Collection of skipping stones
        [" o O o O o ", "O o O o O  ", " o O o O   "],
        # Champion's flat stone
        ["   +===+   ", " /BEST \\  ", "+========+ "],
        # Driftwood log
        ["  ========  ", " /%%%%%%%\\ "],
        # Water's edge
        ["~~~~~~~~~~~~~", "  ~~~~~~~~   ", "    ~~~~     "],
        # Stone stack tower
        ["    o    ", "   oo   ", "  ooo  ", " OOOO "],
        # Shell collection
        ["(@) (@) (@)", " @   @   @ "],
        # Beach umbrella
        ["   /====\\   ", "  /======\\  ", "     ||     "],
    ],
    "Waterfall": [
        # Grand waterfall with hidden cave
        ["    +===+    ", "   /|||||\\   ", "  / ||||| \\  ", " /  |||||  \\ ", "[#] ||||| [#]", " ~~|||||~~  ", "  ~~~~~~~   "],
        # Rainbow in mist
        ["   *  *  *   ", "  *  *  *  * ", "   *  *  *   "],
        # Mist cloud
        ["* * * * * *", " * * * * * ", "* * * * * *"],
        # Treasure glint behind falls
        ["  [<><>]  ", "   <*>   "],
        # Wet rocks
        [" O  O  O ", "........."],
        # Deep pool
        ["~========~", " ======== "],
        # Cliff face
        ["###|||||###", "##|||||||##", "#|||||||||#"],
    ],
    "Vegetable Patch": [
        # Cabbage row
        [" @  @  @  @  @ ", "++++++++++++++++"],
        # Tomato stakes with ripe tomatoes
        [" o   o   o   o ", " Y   Y   Y   Y ", " |   |   |   | "],
        # Carrot tops peeking out
        [" ^^ ^^ ^^ ^^ ", "............."],
        # Bean poles with climbing vines
        ["  +   +   +  ", " /|  /|  /|  ", "+ |  + |  + | "],
        # Squash patch
        [" @  @  @ ", "~~~~~~~~~"],
        # Irrigation channel
        [" ~~~~~~~~~ ", "[  ~~~  ]"],
        # Herb spiral
        ["  +++  ", " +++++ ", "+++++++", " +++++ "],
        # Scarecrow
        ["   +   ", "  /|\\  ", "   |   ", "  / \\  "],
        # Garden plot grid
        ["+--+--+--+", "|^^|@@|()|", "+--+--+--+"],
    ],
    "Tool Shed": [
        # Main shed building
        ["   /========\\   ", "  |   +==+   |  ", " |    |  |    | ", " |    +==+    | ", " +============+ "],
        # Wall of hanging tools
        [" T / \\ T / ", " | | | | | ", " | | | | | "],
        # Cluttered workbench
        ["+----------+", "| []= # [] |", "|  ||  ||  |", "+----------+"],
        # Watering can collection
        [" O   O   O ", " |   |   | "],
        # Cobwebby corner
        ["=====  ", "  \\/   ", " \\ \\  ", "  = =  "],
        # Stacked pots
        ["  []  ", " [][] ", "[][][]"],
        # Seed packets on shelf
        ["+------+", "|*+*+*+|", "+------+"],
        # Wheelbarrow
        ["  +===+  ", " /     \\ ", " \\O===O/ "],
    ],
    "Foothills": [
        # Majestic mountain range
        ["       /\\       ", "      /  \\      ", "     /    \\     ", "    /      \\    ", "   /        \\   "],
        # Snow-capped peaks
        ["    ***    ", "   /^^^^\\   ", "  /      \\  "],
        # Alpine pines
        ["    A    ", "   AAA   ", "  AAAAA  ", "    |    "],
        # Soaring eagle
        ["  \\   /  ", "   ***   "],
        # Mountain stream
        ["=========", " ======= "],
        # Rocky outcrop
        [" O O O ", "OOOOOO"],
        # Edelweiss flowers
        [" * * * ", " + + + "],
        # Trail markers
        [" | ", " |^|", " | "],
        # Goat silhouette
        ["  /\\ ", " |==|", " || ||"],
    ],
    "Crystal Cave": [
        # Massive geode formation
        ["    /\\    ", "   /<>\\   ", "  /<><>\\  ", " |<>*<>| ", " |<><><>| ", "  \\____/  "],
        # Stalactite and stalagmite
        ["  V  V  V  ", "  |  |  |  ", "         ", "  |  |  |  ", "  A  A  A  "],
        # Light refraction rainbows
        ["  * * * *  ", " * * * * * ", "  * * * *  "],
        # Underground crystal pool
        ["~*~*~*~*~", "*~*~*~*~*", "~~~~~~~~"],
        # Amethyst cluster
        ["  <><>  ", " <><><> ", "<><><><>"],
        # Cave entrance
        ["  +===+  ", " /.....\\", "/.......\\ "],
        # Glowing moss patches
        [" *.*.* ", ".*.*.*." ],
        # Crystal column
        ["  /\\  ", " /  \\ ", "|<><>|", " \\  / ", "  \\/  "],
    ],
    "Sandy Shore": [
        # Palm tree
        ["   \\|/   ", "    |    ", "    |    ", "    |    ", "   ===   "],
        # Gentle tropical waves
        ["~~~~~======~~~~~", " ~~~========~~~ ", "  ~~========~~  "],
        # Shell collection
        [" @ (@) * @ (@) ", "(@) @ * (@) @  "],
        # Crab with claw
        ["  __C__  ", " /|||||\\  "],
        # Starfish
        ["   *   ", "  *+*  ", "   *   "],
        # Sandy castle
        [" +---+ ", " |[o]| ", "+-----+", "......."],
        # Coconut
        [" (...) "],
        # Sun reflection on water
        ["*   *   *"],
        # Beach chair
        [" /===\\ ", "/     \\", "+-----+"],
    ],
    "Shipwreck Cove": [
        # Wrecked pirate ship
        ["       /\\      ", "      /# \\     ", "     /====\\    ", "   /========\\  ", "  /##########\\  ", " |############| ", " +============+ "],
        # Broken mast with torn sail
        ["   #   ", "  /|\\  ", " / | \\ ", "   |   ", "   |   "],
        # Treasure chest (half buried)
        ["  +===+  ", " |$<>$| ", " +===+  ", "...... "],
        # Rusty anchor
        ["   [+]   ", "  /|\\ ", " / | \\", "   |   "],
        # Scattered cargo
        [" O  O  O ", "  ==== "],
        # Barnacle-covered rocks
        [" O.O.O ", ".O.O.O"],
        # Wave crash
        ["~~~~~~~", " ~~~~~ ", "  ~~~  "],
        # Pirate flag
        ["  +--+  ", "  |XX|  ", "  +--+  ", "   ||   "],
    ],
    # Swamp scenery
    "Misty Marsh": [
        # Fog bank
        ["  . . . .  ", " . . . . . "],
        # Firefly cluster
        [" * . * ", ". * . *"],
        # Murky pool
        ["  =====  ", " ~=====~ "],
        # Dead tree
        ["   /\\   ", "  /  \\  ", "    |    "],
        # Cattail cluster
        ["Y Y Y Y", "| | | |", "| | | |"],
        # Frog on lily pad
        ["  (@)  ", " ~O O~ "],
        # Gnarled roots
        ["/\\/\\/\\", "\\/\\/\\/"],
    ],
    "Cypress Hollow": [
        # Twisted cypress tree
        ["  ====  ", " /|||\\", "  |||  ", "  |||  "],
        # Spanish moss
        ["= = = =", " = = = "],
        # Hollow log
        ["+=====+", "| *** |", "+=====+"],
        # Firefly lanterns
        ["  *   *  ", " * * * * "],
        # Swamp boat
        ["  +===+  ", " /     \\ ", " \\=====/ "],
        # Cypress knees
        ["  /\\  /\\  /\\  ", " /  \\/  \\/  \\ "],
    ],
    "Sunken Ruins": [
        # Broken column
        ["  +=+  ", "  |.|  ", "  +=+  ", " . . . "],
        # Submerged arch
        ["+=====+", "| ~~~ |", "+     +"],
        # Ancient stones
        [" . # . ", "# . # ."],
        # Sunken statue
        ["  +==+  ", " |(OO)|", " | || |", "  +==+  "],
        # Treasure pile
        [" $ <> $ ", "  $$$  "],
        # Ancient pillar row
        ["|   |   |", "|   |   |", "+===+===+"],
    ],
    # Urban scenery
    "Park Fountain": [
        # Grand city fountain
        ["    +===+    ", "   /~~~~~\\   ", "  |~~~~~~~|  ", "  | ~ ~ ~ |  ", " +=========+ ", " |  o o o  | ", " +=========+ "],
        # Ornamental park bench
        ["+=========+", "|         |", "|         |", "++-------++"],
        # Wishing coins at bottom
        [" o <> o <> o ", "<> o * o <> "],
        # Flower bed with tulips
        ["* * * * * *", "| | | | | |", "==========="],
        # Victorian lamp post
        ["  [O]  ", "   |   ", "   |   ", " +=|=+ "],
        # Hedge sculpture (duck shape!)
        ["  ++++  ", " ++>+++", "  ++++  "],
        # Pigeon flock
        [" v v v ", "  v v  "],
    ],
    "Rooftop Garden": [
        # Raised vegetable beds
        ["+------+  +------+", "| ++++ |  | ^^^^ |", "| ++++ |  | ^^^^ |", "+------+  +------+"],
        # Tomato trellis
        [" o  o  o ", " Y  Y  Y ", " |  |  | ", "+------+"],
        # Beehive for urban bees
        ["  +---+  ", " /zzz\\ ", "|zzzzz| ", " \\===/ "],
        # Potted herb collection
        [" [+] [+] [+] ", "  |   |   |  "],
        # City skyline view
        ["##  ###  ##", " ##   ##  ", "  # # #  "],
        # Rainwater barrel
        ["  +===+  ", " | == | ", " | == | ", "  +===+  "],
        # Compost bin
        ["+---+", "|+++|", "+---+"],
        # Solar panel
        ["/=======\\", "|[=][=][=]|", "\\=======/"],
    ],
    "Storm Drain": [
        # Iron grate entrance with light
        [" +=+=+=+=+ ", " | | | | | ", " | | | | | ", " +=+=+=+=+ "],
        # Dark tunnel stretching back
        ["+=========+", "|##%###%##|", "|##%###%##|", "+=========+"],
        # Underground waterfall
        ["    |||    ", "   ~|||~   ", "  ~~~~~  "],
        # Lost treasure pile
        [" O  <>  O ", "  *  *  ", " . . . "],
        # Dripping stalactites
        [" V * V * V ", "  .   .   "],
        # Mysterious glowing
        ["  [###]  ", "   [#]   "],
        # Echoing puddle
        [" ~~~~~~~~ ", "  ~~~~~~  "],
        # Rat silhouette
        ["  (@)~~ ", " /|\\    "],
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


def generate_location_scenery(location: str, width: int, height: int) -> List[Tuple[int, int, List[str]]]:
    """Generate large scenery placements for a location.
    
    Returns: List of (x, y, art_lines) tuples
    """
    scenery_pieces = get_scenery(location)
    if not scenery_pieces:
        return []
    
    placements = []
    
    # Special handling for specific locations
    if location == "Forest Edge":
        # Always place a winding river and multiple trees
        return _generate_forest_edge_scenery(scenery_pieces, width, height)
    elif location == "Home Pond":
        # Cozy arrangement with lily pads center, reeds on sides
        return _generate_home_pond_scenery(scenery_pieces, width, height)
    
    # Default: Place 1-3 scenery pieces
    num_pieces = random.randint(1, min(3, len(scenery_pieces)))
    used_positions = set()
    
    for piece in random.sample(scenery_pieces, num_pieces):
        piece_width = max(len(line) for line in piece)
        piece_height = len(piece)
        
        # Find a position that doesn't overlap
        attempts = 0
        while attempts < 10:
            x = random.randint(1, max(1, width - piece_width - 2))
            y = random.randint(1, max(1, height - piece_height - 2))
            
            # Check for overlap
            overlap = False
            for px, py in used_positions:
                if abs(x - px) < piece_width + 2 and abs(y - py) < piece_height + 2:
                    overlap = True
                    break
            
            if not overlap:
                placements.append((x, y, piece))
                used_positions.add((x, y))
                break
            
            attempts += 1
    
    return placements


def _generate_forest_edge_scenery(scenery_pieces: List[List[str]], 
                                   width: int, height: int) -> List[Tuple[int, int, List[str]]]:
    """Generate Forest Edge with lots of trees and a winding river."""
    placements = []
    
    # Find river pieces
    river_pieces = [p for p in scenery_pieces if any('=' in line or '~' in line for line in p)]
    tree_pieces = [p for p in scenery_pieces if any('A' in line for line in p)]
    bush_pieces = [p for p in scenery_pieces if any('+' in line for line in p) and not any('A' in line for line in p)]
    
    # Place a long river across the middle-bottom area
    if river_pieces:
        # Find the longest river piece
        long_rivers = [p for p in river_pieces if max(len(line) for line in p) > 10]
        if long_rivers:
            river = random.choice(long_rivers)
            river_y = height - len(river) - 2  # Near bottom
            river_x = random.randint(0, max(0, width - max(len(line) for line in river)))
            placements.append((river_x, river_y, river))
        
        # Add a river bend
        bends = [p for p in river_pieces if len(p) > 2]  # Multi-line river bends
        if bends:
            bend = random.choice(bends)
            bend_x = random.randint(0, max(0, width // 2))
            bend_y = max(0, height - len(bend) - 4)
            placements.append((bend_x, bend_y, bend))
    
    # Place multiple trees along the top area (forest edge)
    if tree_pieces:
        # Place 3-5 tree clusters
        for i in range(random.randint(3, 5)):
            tree = random.choice(tree_pieces)
            tree_width = max(len(line) for line in tree)
            tree_x = random.randint(0, max(0, width - tree_width - 1))
            tree_y = random.randint(0, max(0, min(3, height // 3)))  # Upper area
            placements.append((tree_x, tree_y, tree))
    
    # Add some bushes scattered around
    if bush_pieces:
        for i in range(random.randint(1, 3)):
            bush = random.choice(bush_pieces)
            bush_width = max(len(line) for line in bush)
            bush_x = random.randint(0, max(0, width - bush_width))
            bush_y = random.randint(height // 3, max(height // 3, height - 3))
            placements.append((bush_x, bush_y, bush))
    
    return placements


def _generate_home_pond_scenery(scenery_pieces: List[List[str]],
                                 width: int, height: int) -> List[Tuple[int, int, List[str]]]:
    """Generate Home Pond with cozy pond-focused arrangement."""
    placements = []

    # Categorize scenery pieces by content (using ASCII chars)
    water_pieces = [p for p in scenery_pieces if any('~' in line and len(line) > 8 for line in p)]
    lily_pieces = [p for p in scenery_pieces if any('O' in line and '~' in line for line in p)]
    reed_pieces = [p for p in scenery_pieces if any('|' in line or 'Y' in line for line in p) and not any('O' in line for line in p) and not any('+' in line for line in p)]
    # Dock: has = on one line and + on another
    dock_pieces = [p for p in scenery_pieces if any('=' in line for line in p) and any('+' in line for line in p)]
    shore_pieces = [p for p in scenery_pieces if any("'" in line or ('.' in line and ' ' in line) for line in p) and not any('~' in line for line in p)]

    # Always place main water area in center (this is the pond!)
    if water_pieces:
        water = water_pieces[0]  # Use the big water block
        water_width = max(len(line) for line in water)
        water_x = (width - water_width) // 2
        water_y = (height - len(water)) // 2
        placements.append((water_x, water_y, water))

    # Place lily pads on the water
    if lily_pieces:
        lily = lily_pieces[0]
        lily_width = max(len(line) for line in lily)
        lily_x = (width - lily_width) // 2
        lily_y = (height - len(lily)) // 2 - 1  # Slightly above center
        placements.append((lily_x, lily_y, lily))

    # Reeds on the left edge
    if reed_pieces:
        reed = reed_pieces[0]
        placements.append((1, height - len(reed) - 1, reed))

    # Reeds on the right edge too
    if len(reed_pieces) > 1:
        reed = reed_pieces[1]
        reed_width = max(len(line) for line in reed)
        placements.append((width - reed_width - 2, height - len(reed) - 1, reed))
    elif reed_pieces:
        reed = reed_pieces[0]
        reed_width = max(len(line) for line in reed)
        placements.append((width - reed_width - 2, height - len(reed), reed))

    # Dock in corner
    if dock_pieces:
        dock = dock_pieces[0]
        dock_width = max(len(line) for line in dock)
        placements.append((width - dock_width - 1, 0, dock))

    # Shore/pebbles at bottom
    if shore_pieces:
        shore = shore_pieces[0]
        shore_width = max(len(line) for line in shore)
        placements.append(((width - shore_width) // 2, height - len(shore), shore))

    return placements


# ============================================================================
# DECORATION CHARACTER COLORS
# ============================================================================

def get_decoration_color(location: str, char: str) -> Optional[Callable]:
    """Get the color function for a specific decoration character."""
    # Water characters
    if char in "~=":
        return _term.bright_cyan

    # Lily pads (O) - bright green
    if char == "O":
        return _term.bright_green

    # Lily flowers (*) - bright magenta when near water
    if char == "*" and location in ("Home Pond", "Deep End"):
        return _term.bright_magenta

    # Reeds and cattails (| and Y)
    if char == "|":
        return _term.green
    if char == "Y":
        return _term.color(130)  # Brown cattail tops

    # Dock elements (= and +)
    if char in "=+-":
        return _term.color(130)  # Brown wood

    # Plants/trees
    if char in "A+":
        return _term.green

    # Tree trunks
    if char in "||":
        return _term.color(130)  # Brown

    # Cozy elements - firefly/glow
    if char == "*":
        return _term.bright_yellow  # Firefly/glow
    
    # Flowers - stable colors (no flashing)
    if char == "*":
        return _term.bright_magenta
    if char == "*":
        return _term.bright_yellow
    if char == "*":
        return _term.bright_red
    
    # Crystals - stable colors
    if char == "<" or char == ">":
        return _term.bright_cyan
    if char == "*":
        return _term.bright_white
    if char == "*":
        return _term.bright_magenta
    
    # Rocks/pebbles
    if char in "oO":
        return _term.color(250)  # Gray
    
    # Mushrooms
    if char in "^@":
        colors = [_term.red, _term.bright_red, _term.bright_magenta]
        return random.choice(colors)
    
    # Mountains
    if char in "^/\\":
        return _term.color(240)  # Dark gray
    
    # Wood/structures (not tree trunks)
    if char in "#.=":
        return _term.color(130)  # Brown
    
    # Dock elements
    if char == "=":
        return _term.color(130)  # Brown dock
    
    # Default - no color
    return None


def get_ground_color(location: str) -> Optional[Callable]:
    """Get the ground/background color for a location."""
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

