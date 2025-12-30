"""
Item Interaction System - Custom interactions with placed habitat items.
Each item type has unique animations, effects, and dialogue.
"""
import random
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from world.shop import ItemCategory, get_item


class InteractionType(Enum):
    """Types of interactions available."""
    PLAY = "play"           # Active play interaction
    USE = "use"             # General use
    SPLASH = "splash"       # Water-based
    RIDE = "ride"           # Rideable items
    SIT = "sit"             # Sittable items
    SLEEP = "sleep"         # Sleep on/in item
    EAT = "eat"             # Eat from item
    MUSIC = "music"         # Musical items
    CLIMB = "climb"         # Climbable items
    HIDE = "hide"           # Hideable items
    ADMIRE = "admire"       # Look at/appreciate


@dataclass
class InteractionResult:
    """Result of an item interaction."""
    success: bool
    message: str
    animation_frames: List[List[str]]  # ASCII art frames for animation
    duration: float  # How long the animation lasts
    effects: Dict[str, int]  # Need changes (hunger, fun, etc.)
    sound: Optional[str] = None  # Sound to play


# Animation frames for duck interacting with items
# Each animation is a list of frames, each frame is a list of strings

INTERACTION_ANIMATIONS = {
    # Ball - duck pushes ball, ball rolls, duck chases
    "toy_ball": {
        "play": [
            # Frame 1: Duck approaches ball
            [
                "        O  ",
                "   __  /   ",
                "  (o )>    ",
                "  /|\\|     ",
                " (_) (_)   ",
            ],
            # Frame 2: Duck kicks ball
            [
                "          O",
                "   __   / ",
                "  (o )>/  ",
                "  /|\\|    ",
                " (_)  (_) ",
            ],
            # Frame 3: Ball rolling away
            [
                "              O",
                "   __         ",
                "  (o )>  ->   ",
                "  /|\\|        ",
                " (_) (_)      ",
            ],
            # Frame 4: Duck chasing
            [
                "                O",
                "      __        ",
                "     (o )>  !!  ",
                "     /|\\|       ",
                "    (_) (_)     ",
            ],
            # Frame 5: Duck catches ball
            [
                "   __  O",
                "  (^o)>|",
                "  /|\\|  ",
                " (_)(_) ",
            ],
        ],
    },
    
    # Trampoline - duck bouncing
    "toy_trampoline": {
        "play": [
            # Frame 1: Duck on trampoline
            [
                "   __    ",
                "  (o )>  ",
                " /|\\|    ",
                " [====]  ",
                "  \\  /   ",
            ],
            # Frame 2: Duck in air
            [
                "   __    ",
                "  (^o)>  ",
                " /|\\| !! ",
                "         ",
                " [====]  ",
            ],
            # Frame 3: Duck high in air
            [
                "  (^o)>  ",
                " /|\\|    ",
                "  WHEEE! ",
                "         ",
                " [====]  ",
            ],
            # Frame 4: Duck coming down
            [
                "         ",
                "   __    ",
                "  (o )>  ",
                " /|\\|    ",
                " [====]  ",
            ],
            # Frame 5: Duck landing bounce
            [
                "         ",
                "   __    ",
                "  (oo)>  ",
                " [====]  ",
                "  \\  /   ",
            ],
        ],
    },
    
    # Pool - duck swimming
    "pool_kiddie": {
        "splash": [
            # Frame 1: Duck approaching
            [
                "   __      ",
                "  (o )>    ",
                " /|\\|      ",
                " (__)  [~] ",
            ],
            # Frame 2: Duck jumping in
            [
                "      __   ",
                "     (^o)> ",
                "      !!   ",
                "    [~~~~] ",
            ],
            # Frame 3: SPLASH!
            [
                "   SPLASH! ",
                "  * (oo) * ",
                " *  ~~   * ",
                "  [~~~~~~] ",
            ],
            # Frame 4: Duck swimming
            [
                "           ",
                "   __      ",
                " ~(^o)>~   ",
                "  [~~~~~~] ",
            ],
            # Frame 5: Happy duck paddling
            [
                "    !!     ",
                "   __      ",
                " ~~(^-)~~  ",
                "  [~~~~~~] ",
            ],
        ],
    },
    
    "pool_large": {
        "splash": [
            [
                "       __         ",
                "      (o )>       ",
                "      /|\\|        ",
                "   [~~~~~~~~~]    ",
            ],
            [
                "          CANNONBALL!",
                "        __    ",
                "       (^o)>  ",
                "         \\\\   ",
                "   [~~~~~~~~~]",
            ],
            [
                "    * * SPLASH! * *",
                "      * (OO) *    ",
                "   [~~~~~~~~~~]   ",
            ],
            [
                "                  ",
                "        __        ",
                "   ~~~(^o)>~~~    ",
                "   [~~~~~~~~~~]   ",
            ],
            [
                "       :)         ",
                "        __        ",
                "   ~~~~~(^-)~~~~  ",
                "   [~~~~~~~~~~~]  ",
            ],
        ],
    },
    
    # Swing set
    "toy_swing": {
        "play": [
            [
                "   |---|   ",
                "   | | |   ",
                "   |___|   ",
                "  (o_)     ",
                "    \\      ",
            ],
            [
                "   |---|   ",
                "   |   |   ",
                "     (o_)  ",
                "       \\   ",
                "   |___|   ",
            ],
            [
                "   |---|   ",
                "   |   |   ",
                "   |   |   ",
                "      (^o) ",
                "         \\ ",
            ],
            [
                "   |---|   ",
                "   |   |   ",
                "     (o_)  ",
                "       \\   ",
                "   |___|   ",
            ],
            [
                "   |---|   ",
                "   | | |   ",
                " (o_)      ",
                "   \\       ",
                "   |___|   ",
            ],
        ],
    },
    
    # Slide
    "toy_slide": {
        "play": [
            [
                "     /|    ",
                "    / |    ",
                "   /  |    ",
                "  /___|    ",
                "  (o_)     ",
            ],
            [
                "   (o_)/|  ",
                "    / |    ",
                "   /  |    ",
                "  /___|    ",
            ],
            [
                "     /|    ",
                " (^o)/ |   ",
                "   /  |    ",
                "  /___|    ",
            ],
            [
                "     /|    ",
                "    / |    ",
                "WHEE/(o_)  ",
                "  /___|    ",
            ],
            [
                "     /|    ",
                "    / |    ",
                "   /  |    ",
                "  /___ (^o)",
            ],
        ],
    },
    
    # Sandbox
    "toy_sandbox": {
        "play": [
            [
                "  [     ]  ",
                "  | . . |  ",
                "  [_____]  ",
                "   (o_)    ",
            ],
            [
                "  [     ]  ",
                "  | (o_)|  ",
                "  [_____]  ",
            ],
            [
                "  *dig dig*",
                "  [     ]  ",
                " (o_)...   ",
                "  [_____]  ",
            ],
            [
                "    ^      ",
                "  [/|\\   ] ",
                " (o_) SAND ",
                "  [_____]  ",
            ],
            [
                "  CASTLE!  ",
                "  [  ^  ]  ",
                "  [ /|\\ ]  ",
                "  [_____]  ",
                "   (^o)    ",
            ],
        ],
    },
    
    # Piano
    "toy_piano": {
        "music": [
            [
                " [|||||]   ",
                "  (o_)     ",
            ],
            [
                " [|||||]   ",
                "  (o_)*    ",
                "   plink!  ",
            ],
            [
                " [|||||]   ",
                "   *(o_)   ",
                " plink!    ",
            ],
            [
                " [|||||]   ",
                "  *(o_)*   ",
                " # # #     ",
            ],
            [
                " CONCERT!  ",
                " [|||||]   ",
                "  (^o)     ",
                " # # # #   ",
            ],
        ],
    },
    
    # Trumpet
    "toy_trumpet": {
        "music": [
            [
                "         ",
                "   (o_)  ",
                "   /|\\|  ",
            ],
            [
                "  ===|   ",
                "   (o_)> ",
            ],
            [
                " HONK!   ",
                "  ===|   ",
                "   (O_)> ",
            ],
            [
                "  HONK!  ",
                " ===|    ",
                "  (O_)>  ",
                "  HONK!  ",
            ],
            [
                " *jazz*  ",
                "  ===|   ",
                "   (^o)> ",
                "  # #    ",
            ],
        ],
    },
    
    # Chair - sit on it
    "chair_wood": {
        "sit": [
            [
                " [  ]    ",
                " |  |    ",
                " |__|    ",
                "  (o_)   ",
            ],
            [
                " [  ]    ",
                " |(o_)   ",
                " |__|    ",
            ],
            [
                " [  ]    ",
                " |(^o)   ",
                " |__|    ",
                " Ahh...  ",
            ],
        ],
    },
    
    # Bed - sleep on it
    "bed": {
        "sleep": [
            [
                " ______  ",
                " |    |  ",
                " |____|  ",
                "  (o_)   ",
            ],
            [
                " ______  ",
                " |(o_)|  ",
                " |____|  ",
            ],
            [
                " ______  ",
                " |(-_)|  ",
                " |____|  ",
                "   zzz   ",
            ],
            [
                " ______  ",
                " |(-_)|z ",
                " |____|Z ",
                "   ZZZ   ",
            ],
        ],
    },
    
    # Hot tub
    "hot_tub": {
        "splash": [
            [
                "  (o_)       ",
                " /|\\|        ",
                "[  steam  ]  ",
                "[~~~~~~~~~]  ",
            ],
            [
                "     Ahhh... ",
                "   ~ (o_) ~  ",
                "[~~~~~~~~~]  ",
                "   steam     ",
            ],
            [
                "   ~ ~ ~     ",
                "   ~ (^-) ~  ",
                "[~~~~~~~~~]  ",
                "  so warm... ",
            ],
        ],
    },
    
    # Sprinkler
    "sprinkler": {
        "splash": [
            [
                "    |    ",
                "   (o_)  ",
            ],
            [
                "  * | *  ",
                " * (o_)* ",
                "    !    ",
            ],
            [
                " *  |  * ",
                "* (OO) * ",
                "   !!!   ",
            ],
            [
                "  * | *  ",
                " * (^o)* ",
                "  Wheee! ",
            ],
        ],
    },
    
    # Skateboard
    "toy_skateboard": {
        "ride": [
            [
                "   (o_)  ",
                "  [====] ",
                "   O  O  ",
            ],
            [
                "    (o_) ",
                "   [====]",
                "    O  O ",
            ],
            [
                "      (o_)  ",
                "     [====] ",
                "      O  O  ",
            ],
            [
                "        (^o) ",
                "       [====]",
                "        O  O ",
                "  Radical!   ",
            ],
        ],
    },
    
    # Boombox
    "toy_boombox": {
        "music": [
            [
                " [|O|O|] ",
                "  (o_)   ",
            ],
            [
                " *click* ",
                " [|O|O|] ",
                "  (o_)   ",
            ],
            [
                " # # #   ",
                " [|O|O|] ",
                "  (^o)   ",
            ],
            [
                " # # #   ",
                " [|O|O|] ",
                "  \\(^o)/ ",
                "  dance! ",
            ],
        ],
    },
    
    # Fountain
    "fountain_small": {
        "splash": [
            [
                "    |    ",
                "   ~~~   ",
                "  (o_)   ",
            ],
            [
                "   *|*   ",
                "   ~~~   ",
                "   (o_)  ",
            ],
            [
                "  *sip*  ",
                "   ~~~   ",
                "  (o_)>| ",
            ],
            [
                "   Ahh!  ",
                "   ~~~   ",
                "  (^o)   ",
            ],
        ],
    },
    
    # Hammock
    "hammock": {
        "sleep": [
            [
                "  \\___/  ",
                "   (o_)  ",
            ],
            [
                "  \\(o_)/ ",
            ],
            [
                "  \\(-_)/ ",
                "   zzz   ",
            ],
        ],
    },
    
    # Tire swing
    "tire_swing": {
        "play": [
            [
                "    |    ",
                "    O    ",
                "   (o_)  ",
            ],
            [
                "   \\|    ",
                "    O    ",
                "     (o_)",
            ],
            [
                "    |/   ",
                "    O    ",
                "(o_)     ",
            ],
            [
                "    |    ",
                "  (^o)   ",
                "    O    ",
            ],
        ],
    },
    
    # Frisbee
    "frisbee": {
        "play": [
            [
                "         ====    ",
                "   __          ",
                "  (o )>  ->    ",
                "  /|\\|         ",
            ],
            [
                "              ====",
                "   __            ",
                "  (o )>    ->    ",
                "  /|\\|           ",
            ],
            [
                "                 ====",
                "      __          ",
                "     (o )>  !!    ",
                "     /|\\|         ",
            ],
            [
                "         __  ====",
                "        (^o)>|   ",
                "        /|\\|     ",
            ],
        ],
    },
    
    # Water slide
    "water_slide": {
        "splash": [
            [
                "      /|   ",
                "     / |   ",
                "    (o_)   ",
                "   /   |   ",
            ],
            [
                "          ",
                "      /|  ",
                "  (o_)/   ",
                " /    |   ",
            ],
            [
                "          ",
                "          ",
                "      /|  ",
                " (^o)~~ ! ",
            ],
            [
                "  SPLASH! ",
                "   ~~~    ",
                "  (^o)    ",
                "   ~~~    ",
            ],
        ],
    },
    
    # Kite
    "kite": {
        "play": [
            [
                "           <>  ",
                "          /    ",
                "   __    /     ",
                "  (o )> /      ",
            ],
            [
                "             <>",
                "            /  ",
                "   __      /   ",
                "  (^o)>   /    ",
            ],
            [
                "        <>     ",
                "       /       ",
                "   __ /        ",
                "  (o )>        ",
            ],
        ],
    },
    
    # Drums
    "drums": {
        "music": [
            [
                "   !  !   ",
                "   |  |   ",
                "  [====]  ",
                "  (o_)    ",
            ],
            [
                "  \\    /  ",
                "   |  |   ",
                "  [====]  ",
                "  (^o)    ",
            ],
            [
                "   !  !   ",
                "   |  |   ",
                "  [====]  ",
                "  (o_)    ",
            ],
        ],
    },
    
    # Telescope
    "telescope": {
        "use": [
            [
                "          * * ",
                "       ====>  ",
                "      /       ",
                "   (o_)       ",
            ],
            [
                "       * O *  ",
                "       ====>  ",
                "      /       ",
                "   (^o)       ",
            ],
            [
                "       *  *   ",
                "       ====>  ",
                "      /       ",
                "   (o_) wow!  ",
            ],
        ],
    },
    
    # Easel/painting
    "easel": {
        "use": [
            [
                "  [---]   ",
                "  |   | / ",
                "  |   |/  ",
                "   (o_)   ",
            ],
            [
                "  [~-~]   ",
                "  |   | / ",
                "  |   |/  ",
                "   (o_)   ",
            ],
            [
                "  [:D:]   ",
                "  |   | / ",
                "  |   |/  ",
                "   (^o)   ",
            ],
        ],
    },
    
    # Mirror
    "mirror": {
        "admire": [
            [
                "  [   ]   ",
                "  |(o_)|  ",
                "  [   ]   ",
            ],
            [
                "  [   ]   ",
                "  |(^o)|  ",
                "  [   ]   ",
            ],
            [
                "  [ * ]   ",
                "  |(o_)|  ",
                "  [   ]   ",
            ],
        ],
    },
    
    # Throne
    "chair_throne": {
        "sit": [
            [
                "   ___    ",
                "  |   |   ",
                "  |(o_)|  ",
                "  |___|   ",
            ],
            [
                "  ___     ",
                "  |   |   ",
                "  |(^o)|  ",
                "  |___|   ",
            ],
        ],
    },
}


# Interaction definitions for each item type
ITEM_INTERACTIONS: Dict[str, Dict] = {
    # ===== TOYS =====
    "toy_ball": {
        "commands": ["play with ball", "kick ball", "chase ball"],
        "type": InteractionType.PLAY,
        "messages": [
            "*pushes ball* Wheee!",
            "*chases ball around* Come back here!",
            "*kicks ball* GOAL! Wait, there's no goal...",
            "*nudges ball with beak* Roll roll roll!",
            "*accidentally sits on ball* ...oops",
        ],
        "effects": {"fun": 15, "energy": -5},
        "sound": "play",
        "edge_cases": {
            "tired": "*yawn* Too tired to chase ball... *pushes weakly*",
            "hungry": "*stomach growls* Ball... looks... round like bread?",
            "sad": "*pushes ball* ...it keeps rolling away. Like my happiness.",
        },
    },
    
    "toy_blocks": {
        "commands": ["play with blocks", "stack blocks", "build blocks"],
        "type": InteractionType.PLAY,
        "messages": [
            "*stacks blocks carefully* Tower time!",
            "*KNOCKS OVER BLOCKS* Oops! ...that was on purpose.",
            "*builds elaborate structure* Architectural genius!",
            "*places block* One more... *falls* NOOO!",
        ],
        "effects": {"fun": 12},
        "sound": "play",
        "edge_cases": {
            "clumsy": "*knocks over immediately* I meant to do that!",
        },
    },
    
    "toy_trumpet": {
        "commands": ["play trumpet", "honk trumpet", "make noise"],
        "type": InteractionType.MUSIC,
        "messages": [
            "*HONK HONK* This is AMAZING!",
            "*jazz quacking intensifies*",
            "*plays a tune* I'm basically Mozart!",
            "*HONNNNNK* ...sorry neighbors!",
        ],
        "effects": {"fun": 10, "social": 5},
        "sound": "quack",
        "edge_cases": {
            "night": "*quiet toot* Gotta be quiet... *HONK* oops",
        },
    },
    
    "toy_skateboard": {
        "commands": ["ride skateboard", "skate", "do tricks"],
        "type": InteractionType.RIDE,
        "messages": [
            "*kickflips* ...almost!",
            "*rolls around* Quack yeah! Radical!",
            "*attempts ollie* *falls off* That was... intentional.",
            "*cruises by* I'm a skating legend!",
        ],
        "effects": {"fun": 18, "energy": -8},
        "sound": "play",
        "edge_cases": {
            "clumsy": "*immediately faceplants* I'm okay!",
            "tired": "*sits on skateboard* This counts as skating, right?",
        },
    },
    
    "toy_piano": {
        "commands": ["play piano", "make music", "compose"],
        "type": InteractionType.MUSIC,
        "messages": [
            "*pecks keys* ## Masterpiece!",
            "*composes* This is called 'Bread in D Minor'",
            "*plays dramatic chord* DUN DUN DUNNN",
            "*gentle melody* So soothing...",
        ],
        "effects": {"fun": 12, "social": 3},
        "sound": "play",
    },
    
    "toy_trampoline": {
        "commands": ["jump on trampoline", "bounce", "trampoline"],
        "type": InteractionType.PLAY,
        "messages": [
            "*BOING BOING* THIS IS THE BEST!",
            "*bouncing intensifies* HIGHER!",
            "*does flip* ...nailed it? Sort of?",
            "*bounces* I CAN TOUCH THE CLOUDS!",
        ],
        "effects": {"fun": 20, "energy": -10},
        "sound": "play",
        "edge_cases": {
            "tired": "*weak bounce* *flops* I'll just... lie here.",
            "full_stomach": "*bounces* Oh no my bread! *urp*",
        },
    },
    
    "toy_slide": {
        "commands": ["go down slide", "slide", "climb slide"],
        "type": InteractionType.CLIMB,
        "messages": [
            "*slides down* WHEEEEE!",
            "*climbs up for another turn* Again! Again!",
            "*goes down backwards* I'm an innovator!",
            "*zooms down* That was SO FAST!",
        ],
        "effects": {"fun": 15, "energy": -5},
        "sound": "play",
        "edge_cases": {
            "scared": "*looks down* That's... high. *carefully slides* okay that was fun",
        },
    },
    
    "toy_swing": {
        "commands": ["swing", "use swing", "swing set"],
        "type": InteractionType.PLAY,
        "messages": [
            "*swinging* Higher! HIGHER!",
            "*pumps legs* I can touch the clouds!",
            "*swings peacefully* So relaxing...",
            "*swings wildly* MAXIMUM VELOCITY!",
        ],
        "effects": {"fun": 15, "energy": -3},
        "sound": "play",
    },
    
    "toy_seesaw": {
        "commands": ["use seesaw", "play seesaw"],
        "type": InteractionType.PLAY,
        "messages": [
            "*sits on one end* ...I need a friend.",
            "*bounces slightly* This is fun? I guess?",
            "*imagines friend on other end* Up! Down! Up!",
            "*waddles back and forth* Multi-tasking!",
        ],
        "effects": {"fun": 5, "social": -2},
        "edge_cases": {
            "lonely": "*sits alone* This would be better with a friend... *sigh*",
        },
    },
    
    "toy_sandbox": {
        "commands": ["play in sandbox", "dig sand", "build sandcastle"],
        "type": InteractionType.PLAY,
        "messages": [
            "*digs furiously* TREASURE! ...nope, just more sand.",
            "*makes sand castle* Architectural genius!",
            "*buries self* I am one with the sand.",
            "*digs hole* It's getting deeper! And deeper!",
        ],
        "effects": {"fun": 12, "cleanliness": -8},
        "sound": "play",
        "edge_cases": {
            "clean": "*looks at sand* But I JUST got clean... *dives in anyway*",
        },
    },
    
    "toy_boombox": {
        "commands": ["play boombox", "turn on music", "dance"],
        "type": InteractionType.MUSIC,
        "messages": [
            "*turns on boombox* ## MUSIC TIME! ##",
            "*dances to the beat* This is my JAM!",
            "*breakdances* ...sort of. Duck-style!",
            "*vibes* This beat is FIRE!",
        ],
        "effects": {"fun": 15, "social": 5},
        "sound": "play",
    },
    
    # ===== WATER FEATURES =====
    "pool_kiddie": {
        "commands": ["swim in pool", "splash in pool", "go swimming"],
        "type": InteractionType.SPLASH,
        "messages": [
            "*splashes* WATER! GLORIOUS WATER!",
            "*paddles around* I'm a natural!",
            "*floats on back* This is the life...",
            "*dives under* Blub blub!",
        ],
        "effects": {"fun": 20, "cleanliness": 10, "energy": -5},
        "sound": "splash",
        "edge_cases": {
            "cold": "*tests water with foot* Cold cold cold! *jumps in anyway*",
        },
    },
    
    "pool_large": {
        "commands": ["swim in pool", "dive in pool", "go swimming", "cannonball"],
        "type": InteractionType.SPLASH,
        "messages": [
            "*dives in* CANNONBALL!",
            "*swims laps* I'm an athlete!",
            "*floats majestically* Born for this!",
            "*does synchronized swimming alone* TA-DA!",
        ],
        "effects": {"fun": 25, "cleanliness": 15, "energy": -8},
        "sound": "splash",
        "edge_cases": {
            "showing_off": "*does elaborate dive* 10 out of 10! ...right?",
        },
    },
    
    "fountain_small": {
        "commands": ["drink from fountain", "splash in fountain", "use fountain"],
        "type": InteractionType.SPLASH,
        "messages": [
            "*drinks from fountain* Refreshing!",
            "*splashes face* Ahh, so nice!",
            "*watches water* So peaceful...",
            "*sticks head in* BLOOOP!",
        ],
        "effects": {"fun": 8, "hunger": 5},
        "sound": "splash",
    },
    
    "fountain_grand": {
        "commands": ["admire fountain", "splash in fountain"],
        "type": InteractionType.ADMIRE,
        "messages": [
            "*stares in awe* So... beautiful...",
            "*feels fancy* I'm high class now!",
            "*makes a wish* I wish for more bread!",
            "*splashes grandly* I AM ROYALTY!",
        ],
        "effects": {"fun": 12, "social": 5},
    },
    
    "pond": {
        "commands": ["swim in pond", "float in pond", "go to pond"],
        "type": InteractionType.SPLASH,
        "messages": [
            "*happy duck noises* HOME!",
            "*floats peacefully* This is where I belong...",
            "*dives for imaginary fish* Gotcha! ...nothing.",
            "*paddles in circles* Round and round!",
        ],
        "effects": {"fun": 20, "cleanliness": 10, "energy": 5},
        "sound": "splash",
    },
    
    "sprinkler": {
        "commands": ["run through sprinkler", "play in sprinkler", "get wet"],
        "type": InteractionType.SPLASH,
        "messages": [
            "*runs through sprinkler* WHEEE!",
            "*gets soaked* Worth it!",
            "*dances in water* LA LA LA!",
            "*jumps through repeatedly* AGAIN!",
        ],
        "effects": {"fun": 15, "cleanliness": 8, "energy": -5},
        "sound": "splash",
    },
    
    "hot_tub": {
        "commands": ["get in hot tub", "relax in hot tub", "soak"],
        "type": InteractionType.SPLASH,
        "messages": [
            "*relaxes* Ahhhh... this is AMAZING!",
            "*bubbles* The bubbles! SO MANY BUBBLES!",
            "*soaks* I could stay here forever...",
            "*steam rises* I'm like a soup... wait, that's concerning.",
        ],
        "effects": {"fun": 15, "energy": 10, "cleanliness": 5},
        "sound": "splash",
        "edge_cases": {
            "cold_weather": "*sinks deeper* Never leaving. NEVER.",
        },
    },
    
    "waterfall": {
        "commands": ["stand under waterfall", "use waterfall", "meditate"],
        "type": InteractionType.SPLASH,
        "messages": [
            "*stands under waterfall* COLD! But cool!",
            "*meditates* I am one with the water...",
            "*gets pummeled by water* SO INTENSE!",
            "*listens to water* So zen...",
        ],
        "effects": {"fun": 12, "cleanliness": 15, "energy": -3},
        "sound": "splash",
    },
    
    "birdbath": {
        "commands": ["bathe in birdbath", "splash in birdbath", "use birdbath"],
        "type": InteractionType.SPLASH,
        "messages": [
            "*splashes* Bath time!",
            "*preens feathers* Looking GOOD!",
            "*shakes off water* Sparkly clean!",
            "*sits in water* Ahh, perfect fit!",
        ],
        "effects": {"fun": 8, "cleanliness": 12},
        "sound": "splash",
    },
    
    # ===== FURNITURE =====
    "chair_wood": {
        "commands": ["sit on chair", "rest on chair", "sit down"],
        "type": InteractionType.SIT,
        "messages": [
            "*sits* Ahh, perfect.",
            "*lounges* This is the life.",
            "*swings legs* La la la~",
            "*sits regally* Throne acquired.",
        ],
        "effects": {"energy": 5},
    },
    
    "chair_fancy": {
        "commands": ["sit on chair", "sit down"],
        "type": InteractionType.SIT,
        "messages": [
            "*sits elegantly* I feel FANCY.",
            "*poses* Paint me like one of your French ducks.",
            "*lounges luxuriously* This is living!",
        ],
        "effects": {"energy": 8, "fun": 3},
    },
    
    "bed": {
        "commands": ["sleep in bed", "rest in bed", "take a nap", "lie down"],
        "type": InteractionType.SLEEP,
        "messages": [
            "*flops on bed* SO COMFY!",
            "*snuggles in* zzz...",
            "*starfishes* Maximum comfort achieved.",
            "*burrows under covers* Goodnight world!",
        ],
        "effects": {"energy": 20},
        "sound": "sleep",
    },
    
    "hammock": {
        "commands": ["rest in hammock", "swing in hammock", "nap in hammock"],
        "type": InteractionType.SLEEP,
        "messages": [
            "*sways gently* This is paradise...",
            "*falls asleep* zzz... *almost falls out* GAH!",
            "*relaxes* Nothing to do... nowhere to be...",
        ],
        "effects": {"energy": 15, "fun": 5},
    },
    
    "tire_swing": {
        "commands": ["swing on tire", "play with tire swing"],
        "type": InteractionType.PLAY,
        "messages": [
            "*swings in tire* WHEEE!",
            "*spins around* Dizzy... but FUN!",
            "*hangs upside down* I can see the WORLD!",
        ],
        "effects": {"fun": 12, "energy": -3},
    },
    
    # ===== SPECIAL/DECORATION =====
    "disco_ball": {
        "commands": ["dance under disco ball", "party time"],
        "type": InteractionType.PLAY,
        "messages": [
            "*disco dancing* SATURDAY NIGHT FEVER!",
            "*struts* I'm a dancing MACHINE!",
            "*sparkles* Look at those lights!",
        ],
        "effects": {"fun": 15, "social": 5},
    },
    
    "campfire": {
        "commands": ["sit by campfire", "warm up", "roast marshmallows"],
        "type": InteractionType.SIT,
        "messages": [
            "*warms wings* Cozy~",
            "*stares at flames* So mesmerizing...",
            "*pretends to roast marshmallow* S'mores time!",
        ],
        "effects": {"energy": 5, "fun": 8},
        "edge_cases": {
            "cold": "*hugs fire* WARMTH! PRECIOUS WARMTH!",
        },
    },
    
    # Additional items
    "frisbee": {
        "commands": ["throw frisbee", "play frisbee", "catch frisbee"],
        "type": InteractionType.PLAY,
        "messages": [
            "*throws frisbee* ...and catches it! Wait, how?",
            "*chases frisbee* Got it! Got it! Almost!",
            "*frisbee bonks head* Ow! Worth it!",
            "*does trick throw* I'm a frisbee LEGEND!",
        ],
        "effects": {"fun": 15, "energy": -8},
    },
    
    "toy_car": {
        "commands": ["play with car", "drive car", "vroom"],
        "type": InteractionType.PLAY,
        "messages": [
            "*pushes car* Vroom vroom!",
            "*makes engine noises* BRRRRRM!",
            "*races car around* Fastest duck in town!",
            "*car does loop* Stunt driver mode!",
        ],
        "effects": {"fun": 12},
    },
    
    "kite": {
        "commands": ["fly kite", "play with kite"],
        "type": InteractionType.PLAY,
        "messages": [
            "*runs with kite* FLY! FLY!",
            "*kite soars* I made it FLY!",
            "*kite crashes* ...gravity wins again.",
            "*watches kite dance* So pretty up there!",
        ],
        "effects": {"fun": 15, "energy": -5},
        "edge_cases": {
            "no_wind": "*waves kite sadly* Need more wind...",
        },
    },
    
    "yo_yo": {
        "commands": ["play with yo-yo", "yo-yo tricks"],
        "type": InteractionType.PLAY,
        "messages": [
            "*yo-yo goes down* ...and up! ...and tangled.",
            "*attempts walk the dog* More like 'tangle the string'!",
            "*yo-yo trick* I MEANT to do that!",
            "*spins yo-yo* Round and round~",
        ],
        "effects": {"fun": 10},
    },
    
    "jump_rope": {
        "commands": ["jump rope", "skip rope"],
        "type": InteractionType.PLAY,
        "messages": [
            "*jump jump jump* One, two, skip a few!",
            "*trips on rope* Style points!",
            "*speed jumping* I'm unstoppable!",
            "*double dutch attempt* ...okay single rope it is.",
        ],
        "effects": {"fun": 12, "energy": -8},
    },
    
    "drums": {
        "commands": ["play drums", "drum solo"],
        "type": InteractionType.MUSIC,
        "messages": [
            "*BANG BANG BANG* ROCK AND ROLL!",
            "*epic drum solo* FEEL THE RHYTHM!",
            "*tap tap tap* Subtle. Artistic.",
            "*crashes cymbals* WHAT A FINALE!",
        ],
        "effects": {"fun": 15, "social": 5},
    },
    
    "telescope": {
        "commands": ["look through telescope", "stargaze", "use telescope"],
        "type": InteractionType.USE,
        "messages": [
            "*peers through telescope* I can see the MOON!",
            "*searches sky* Looking for the Bread Galaxy...",
            "*spots star* I'm naming that one 'Quacky'!",
            "*gazes at stars* So many worlds out there...",
        ],
        "effects": {"fun": 10},
        "edge_cases": {
            "day": "*looks at sun* OW! Okay don't do that.",
        },
    },
    
    "easel": {
        "commands": ["paint", "draw", "use easel"],
        "type": InteractionType.USE,
        "messages": [
            "*paints masterpiece* Art! ART!",
            "*draws self-portrait* Stunning. Magnificent.",
            "*splashes colors* Abstract expressionism!",
            "*careful brushstrokes* My magnum opus!",
        ],
        "effects": {"fun": 12},
    },
    
    "water_slide": {
        "commands": ["go down water slide", "slide", "whoosh"],
        "type": InteractionType.SPLASH,
        "messages": [
            "*WHOOOOSH* AMAZING!",
            "*zooms down* FASTER! FASTER!",
            "*splashes at bottom* Perfect landing!",
            "*slides again* One more time! And again!",
        ],
        "effects": {"fun": 25, "cleanliness": 5, "energy": -8},
    },
    
    "couch": {
        "commands": ["sit on couch", "relax on couch", "lounge"],
        "type": InteractionType.SIT,
        "messages": [
            "*sinks into cushions* Ahhhhh...",
            "*sprawls out* Maximum comfort!",
            "*watches imaginary TV* Peak entertainment.",
            "*snuggles in* Never leaving.",
        ],
        "effects": {"energy": 10},
    },
    
    "bed_small": {
        "commands": ["sleep in bed", "nap", "rest"],
        "type": InteractionType.SLEEP,
        "messages": [
            "*curls up* Perfect size!",
            "*snuggles blanket* So cozy~",
            "*yawns* Naptime...",
        ],
        "effects": {"energy": 15},
    },
    
    "bed_king": {
        "commands": ["sleep in bed", "sprawl", "king size nap"],
        "type": InteractionType.SLEEP,
        "messages": [
            "*starfishes across entire bed* ALL MINE!",
            "*rolls around* So much ROOM!",
            "*builds pillow fort* Duck palace!",
            "*sinks into luxury* I am ROYALTY!",
        ],
        "effects": {"energy": 25, "fun": 5},
    },
    
    "bookshelf": {
        "commands": ["read book", "look at books"],
        "type": InteractionType.USE,
        "messages": [
            "*picks out book* '101 Bread Recipes'!",
            "*pretends to read* Very intellectual.",
            "*flips pages* Ooh, pictures!",
            "*organizes books* By tastiness of cover color.",
        ],
        "effects": {"fun": 5},
    },
    
    "mirror": {
        "commands": ["look in mirror", "admire self"],
        "type": InteractionType.ADMIRE,
        "messages": [
            "*poses* Looking GOOD!",
            "*makes faces* Majestic. Stunning.",
            "*preens feathers* Photo ready!",
            "*winks at reflection* Hey good looking!",
        ],
        "effects": {"fun": 8},
    },
    
    "lamp_floor": {
        "commands": ["turn on lamp", "sit by lamp"],
        "type": InteractionType.USE,
        "messages": [
            "*clicks lamp* Let there be LIGHT!",
            "*basks in warm glow* Cozy~",
            "*stares at light* Moth mode activated.",
        ],
        "effects": {"fun": 3},
    },
    
    "table_small": {
        "commands": ["sit at table", "use table"],
        "type": InteractionType.SIT,
        "messages": [
            "*sits at table* Very proper.",
            "*taps table* Waiting for bread service...",
            "*pretends to have tea* Fancy!",
        ],
        "effects": {"energy": 3},
    },
    
    "desk": {
        "commands": ["work at desk", "sit at desk"],
        "type": InteractionType.SIT,
        "messages": [
            "*sits professionally* Time to work!",
            "*organizes nothing* Very productive.",
            "*doodles* This is working, right?",
        ],
        "effects": {"energy": 3},
    },
    
    "chair_throne": {
        "commands": ["sit on throne", "be king"],
        "type": InteractionType.SIT,
        "messages": [
            "*sits majestically* BOW TO ME!",
            "*adjusts crown* King of the ducks!",
            "*waves regally* Hello, subjects!",
            "*decrees* More bread for everyone!",
        ],
        "effects": {"energy": 8, "fun": 10},
    },
}


def get_item_interaction(item_id: str) -> Optional[Dict]:
    """Get interaction data for an item."""
    return ITEM_INTERACTIONS.get(item_id)


def get_interaction_commands(item_id: str) -> List[str]:
    """Get list of command strings for an item."""
    interaction = ITEM_INTERACTIONS.get(item_id)
    if interaction:
        return interaction.get("commands", [])
    return []


def get_all_interaction_commands() -> Dict[str, List[str]]:
    """Get all items and their commands."""
    return {
        item_id: data.get("commands", [])
        for item_id, data in ITEM_INTERACTIONS.items()
    }


def execute_interaction(item_id: str, duck_state: Dict = None) -> Optional[InteractionResult]:
    """
    Execute an interaction with an item.
    
    Args:
        item_id: The item to interact with
        duck_state: Optional dict with keys like 'energy', 'hunger', 'fun', 'mood'
                   to check for edge cases
    
    Returns:
        InteractionResult with message, animation, and effects
    """
    interaction = ITEM_INTERACTIONS.get(item_id)
    if not interaction:
        return None
    
    duck_state = duck_state or {}
    
    # Check for edge cases based on duck state
    message = None
    edge_cases = interaction.get("edge_cases", {})
    
    # Check various edge cases
    if duck_state.get("energy", 100) < 20 and "tired" in edge_cases:
        message = edge_cases["tired"]
    elif duck_state.get("hunger", 100) < 20 and "hungry" in edge_cases:
        message = edge_cases["hungry"]
    elif duck_state.get("fun", 100) < 20 and "sad" in edge_cases:
        message = edge_cases["sad"]
    elif duck_state.get("cleanliness", 100) > 90 and "clean" in edge_cases:
        message = edge_cases["clean"]
    elif duck_state.get("social", 100) < 20 and "lonely" in edge_cases:
        message = edge_cases["lonely"]
    
    # Default to random message
    if not message:
        messages = interaction.get("messages", ["*interacts*"])
        message = random.choice(messages)
    
    # Get animation frames
    animation_data = INTERACTION_ANIMATIONS.get(item_id, {})
    interaction_type = interaction.get("type", InteractionType.USE)
    animation_key = interaction_type.value
    animation_frames = animation_data.get(animation_key, [])
    
    # Default animation if none defined
    if not animation_frames:
        animation_frames = [
            ["   (o_)  ", "   /|\\|  "],
            ["   (^o)  ", "   /|\\|  "],
        ]
    
    return InteractionResult(
        success=True,
        message=message,
        animation_frames=animation_frames,
        duration=len(animation_frames) * 0.5,  # 0.5 seconds per frame
        effects=interaction.get("effects", {}),
        sound=interaction.get("sound"),
    )


def find_matching_item(command: str, owned_items: List[str]) -> Optional[str]:
    """
    Find an item that matches the given command.
    
    Args:
        command: The command string (e.g., "play with ball")
        owned_items: List of item IDs the player owns
    
    Returns:
        The matching item_id, or None
    """
    command_lower = command.lower().strip()
    
    for item_id in owned_items:
        interaction = ITEM_INTERACTIONS.get(item_id)
        if not interaction:
            continue
        
        commands = interaction.get("commands", [])
        for cmd in commands:
            if cmd.lower() in command_lower or command_lower in cmd.lower():
                return item_id
    
    # Also try partial matching on item names
    for item_id in owned_items:
        item = get_item(item_id)
        if item and item.name.lower() in command_lower:
            if item_id in ITEM_INTERACTIONS:
                return item_id
    
    return None
