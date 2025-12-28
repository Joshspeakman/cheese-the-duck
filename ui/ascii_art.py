"""
ASCII art for the duck in various states, moods, and growth stages.
Large detailed version with emotion close-ups.
"""
from typing import Dict, List, Optional
from duck.mood import MoodState


# =============================================================================
# LARGE DETAILED DUCK ART
# =============================================================================

DUCK_ART = {
    # ===================
    # DUCKLING STAGE
    # ===================
    "duckling": {
        "normal": [
            "                              ",
            "            .---.             ",
            "           / o   \\            ",
            "          |   __  |           ",
            "           \\  \\_) |>          ",
            "            `---|--'          ",
            "              _|  \\           ",
            "             (_)  (_)         ",
            "                              ",
        ],
        "happy": [
            "                              ",
            "            .---.             ",
            "           / ^   \\    !       ",
            "          |   __  |           ",
            "           \\  \\_) |>          ",
            "            `---|--'          ",
            "              _|  \\           ",
            "             (_)  (_)         ",
            "                              ",
        ],
        "sad": [
            "                              ",
            "            .---.             ",
            "           / ;   \\            ",
            "          |   __  |           ",
            "           \\  \\_) |>          ",
            "            `---|--'    .     ",
            "              _|  \\    '      ",
            "             (_)  (_)         ",
            "                              ",
        ],
        "sleeping": [
            "                              ",
            "            .---.       z     ",
            "           / -   \\      Z     ",
            "          |   __  |    z      ",
            "           \\  \\_) |>          ",
            "            `---|--'          ",
            "              _|  \\           ",
            "             (_)  (_)         ",
            "                              ",
        ],
        "eating": [
            "                              ",
            "            .---.             ",
            "           / o   \\            ",
            "          |   __  |           ",
            "           \\  \\_) |> om nom   ",
            "            `---|--'          ",
            "         .,.,_|  \\.,.,        ",
            "             (_)  (_)         ",
            "                              ",
        ],
    },

    # ===================
    # TEEN STAGE
    # ===================
    "teen": {
        "normal": [
            "                                  ",
            "              __                  ",
            "           __(  )_                ",
            "          /  o    \\               ",
            "         |    ___  |              ",
            "          \\   \\_/  )_             ",
            "           \\__    _/ |>           ",
            "              |  |--'             ",
            "            __|  |__              ",
            "           (__)  (__)             ",
            "                                  ",
        ],
        "happy": [
            "              !!                  ",
            "              __                  ",
            "           __(  )_                ",
            "          /  ^    \\               ",
            "         |    ___  |              ",
            "          \\   \\_/  )_             ",
            "           \\__    _/ |>           ",
            "              |  |--'             ",
            "            __|  |__              ",
            "           (__)  (__)             ",
            "                                  ",
        ],
        "sad": [
            "                                  ",
            "              __                  ",
            "           __(  )_                ",
            "          /  ;    \\               ",
            "         |    ___  |              ",
            "          \\   \\_/  )_             ",
            "           \\__    _/ |>           ",
            "              |  |--'      .      ",
            "            __|  |__      '       ",
            "           (__)  (__)             ",
            "                                  ",
        ],
        "sleeping": [
            "                           z Z    ",
            "              __          z       ",
            "           __(  )_       Z        ",
            "          /  -    \\               ",
            "         |    ___  |              ",
            "          \\   \\_/  )_             ",
            "           \\__    _/ |>           ",
            "              |  |--'             ",
            "            __|  |__              ",
            "           (__)  (__)             ",
            "                                  ",
        ],
        "eating": [
            "                                  ",
            "              __                  ",
            "           __(  )_                ",
            "          /  o    \\               ",
            "         |    ___  |   *chomp*    ",
            "          \\   \\_/  )_             ",
            "           \\__    _/ |>           ",
            "              |  |--'             ",
            "         .,.__|  |__.,.,          ",
            "           (__)  (__)             ",
            "                                  ",
        ],
        "grumpy": [
            "                                  ",
            "              __                  ",
            "           __(  )_                ",
            "          /  >    \\    hmph       ",
            "         |    ___  |              ",
            "          \\   \\_/  )_             ",
            "           \\__    _/ |>           ",
            "              |  |--'             ",
            "            __|  |__              ",
            "           (__)  (__)             ",
            "                                  ",
        ],
    },

    # ===================
    # ADULT STAGE (Main)
    # ===================
    "adult": {
        "normal": [
            "                                        ",
            "                  ___                   ",
            "               __(   )__                ",
            "              /    o    \\               ",
            "             |           |              ",
            "             |    ____   |              ",
            "              \\   \\__/   /_             ",
            "               \\___     _/  |>          ",
            "                   |   |---'            ",
            "                 __|   |__              ",
            "                /   \\ /   \\             ",
            "               (___) (___)              ",
            "                                        ",
        ],
        "happy": [
            "                   !                    ",
            "                  ___                   ",
            "               __(   )__                ",
            "              /    ^    \\               ",
            "             |           |              ",
            "             |    ____   |              ",
            "              \\   \\__/   /_             ",
            "               \\___     _/  |>          ",
            "                   |   |---'            ",
            "                 __|   |__              ",
            "                /   \\ /   \\             ",
            "               (___) (___)              ",
            "                                        ",
        ],
        "ecstatic": [
            "              \\   !   /                 ",
            "                  ___                   ",
            "               __(   )__                ",
            "              /    O    \\      !!       ",
            "             |    \\./   |               ",
            "             |    ____   |              ",
            "              \\   \\__/   /_             ",
            "               \\___     _/  |>          ",
            "                   |   |---'            ",
            "                 __|   |__              ",
            "                / | \\ / | \\             ",
            "               (___) (___)              ",
            "                                        ",
        ],
        "sad": [
            "                                        ",
            "                  ___                   ",
            "               __(   )__                ",
            "              /    ;    \\               ",
            "             |     .    |               ",
            "             |    ____   |              ",
            "              \\   \\__/   /_             ",
            "               \\___     _/  |>          ",
            "                   |   |---'            ",
            "                 __|   |__       .      ",
            "                /   \\ /   \\     '       ",
            "               (___) (___)              ",
            "                                        ",
        ],
        "miserable": [
            "                                        ",
            "                  ___                   ",
            "               __(   )__                ",
            "              /    T    \\               ",
            "             |     _    |               ",
            "             |    ____   |              ",
            "              \\   \\__/   /_             ",
            "               \\___     _/  |>          ",
            "                   |   |---'            ",
            "                 __|   |__    '. .'     ",
            "                /   \\ /   \\             ",
            "               (___) (___)              ",
            "                                        ",
        ],
        "sleeping": [
            "                               z Z z    ",
            "                  ___         Z   z     ",
            "               __(   )__     z          ",
            "              /    -    \\               ",
            "             |     _    |               ",
            "             |    ____   |              ",
            "              \\   \\__/   /_             ",
            "               \\___     _/  |>          ",
            "                   |   |---'            ",
            "                 __|   |__              ",
            "                /   \\ /   \\             ",
            "               (___) (___)              ",
            "                                        ",
        ],
        "eating": [
            "                                        ",
            "                  ___                   ",
            "               __(   )__                ",
            "              /    o    \\               ",
            "             |     U    |   *NOM NOM*   ",
            "             |    ____   |              ",
            "              \\   \\__/   /_             ",
            "               \\___     _/  '>          ",
            "                   |   |---'            ",
            "            .,.,__|   |__.,.,.,         ",
            "                /   \\ /   \\             ",
            "               (___) (___)              ",
            "                                        ",
        ],
        "grumpy": [
            "                                        ",
            "                  ___                   ",
            "               __(   )__                ",
            "              /    >    \\     hmph      ",
            "             |     _    |               ",
            "             |    ____   |              ",
            "              \\   \\__/   /_             ",
            "               \\___     _/  |>          ",
            "                   |   |---'            ",
            "                 __|   |__              ",
            "                /   \\ /   \\             ",
            "               (___) (___)              ",
            "                                        ",
        ],
        "quack": [
            "                                        ",
            "                  ___                   ",
            "               __(   )__                ",
            "              /    O    \\               ",
            "             |           |   QUACK!!    ",
            "             |    ____   |              ",
            "              \\   \\__/   /_             ",
            "               \\___     _/  O>          ",
            "                   |   |---'            ",
            "                 __|   |__              ",
            "                /   \\ /   \\             ",
            "               (___) (___)              ",
            "                                        ",
        ],
        "splash": [
            "             ~         ~                ",
            "                  ___       ~           ",
            "          ~   __(   )__                 ",
            "              /    ^    \\       ~       ",
            "        ~    |    \\.    |               ",
            "             |    ____   |    ~         ",
            "         ~    \\   \\__/   /_             ",
            "               \\___     _/  |>   ~      ",
            "          ~        |   |---'            ",
            "        ~  ~  ~  __|   |__ ~  ~  ~      ",
            "           ~    /   \\ /   \\    ~        ",
            "               (___) (___)              ",
            "                                        ",
        ],
        "preen": [
            "                                        ",
            "                  ___                   ",
            "               __(   )__                ",
            "              /    -    \\               ",
            "             |     .    |               ",
            "             |    ____   |              ",
            "              \\   \\__/   /              ",
            "               \\___     _\\              ",
            "                   |   |  \\  *fluff*    ",
            "                 __|   |   \\            ",
            "                /   \\ /   \\ |           ",
            "               (___) (___)              ",
            "                                        ",
        ],
        "stare": [
            "                                        ",
            "                  ___                   ",
            "               __(   )__                ",
            "              /    .    \\               ",
            "             |           |              ",
            "             |    ____   |              ",
            "              \\   \\__/   /_             ",
            "               \\___     _/  |>          ",
            "                   |   |---'            ",
            "                 __|   |__              ",
            "                /   \\ /   \\    . . .    ",
            "               (___) (___)              ",
            "                                        ",
        ],
        "trip": [
            "                                        ",
            "                       ___              ",
            "                    __(   )__           ",
            "                   /    @    \\          ",
            "          WHOA!   |           |         ",
            "                  |    ____   |         ",
            "                   \\   \\__/   \\         ",
            "            ___     \\___   ___/         ",
            "           <|  ------|   |              ",
            "                   __|   |__            ",
            "                  /   \\ /   \\           ",
            "                 (___) (___)   *thud*   ",
            "                                        ",
        ],
        "flap": [
            "              \\         /               ",
            "               \\  ___  /                ",
            "               __(   )__                ",
            "              /    O    \\               ",
            "             |     !    |   *FLAP*      ",
            "             |    ____   |              ",
            "              \\   \\__/   /_             ",
            "               \\___     _/  |>          ",
            "                   |   |---'            ",
            "                 __|   |__              ",
            "                /   \\ /   \\             ",
            "               (___) (___)              ",
            "                                        ",
        ],
        "waddle_left": [
            "                                        ",
            "                  ___                   ",
            "               __(   )__                ",
            "              /    o    \\               ",
            "             |           |              ",
            "             |    ____   |              ",
            "              \\   \\__/   /_             ",
            "               \\___     _/  |>          ",
            "                   |   |---'            ",
            "                 __|   |__              ",
            "               _/   \\ /   \\             ",
            "              (___) (___)               ",
            "                                        ",
        ],
        "waddle_right": [
            "                                        ",
            "                  ___                   ",
            "               __(   )__                ",
            "              /    o    \\               ",
            "             |           |              ",
            "             |    ____   |              ",
            "              \\   \\__/   /_             ",
            "               \\___     _/  |>          ",
            "                   |   |---'            ",
            "                 __|   |__              ",
            "                /   \\ /   \\_            ",
            "               (___) (___)              ",
            "                                        ",
        ],
    },

    # ===================
    # ELDER STAGE
    # ===================
    "elder": {
        "normal": [
            "                                        ",
            "                  ___                   ",
            "           ~  __(   )__ ~               ",
            "              /    o    \\               ",
            "             |   ~   ~  |               ",
            "             |    ____   |              ",
            "              \\   \\__/   /_             ",
            "               \\___     _/  |>          ",
            "                   |   |---'            ",
            "                 __|   |__    *wise*    ",
            "                /   \\ /   \\             ",
            "               (___) (___)              ",
            "                                        ",
        ],
        "happy": [
            "                                        ",
            "                  ___                   ",
            "           ~  __(   )__ ~               ",
            "              /    ^    \\               ",
            "             |   ~   ~  |               ",
            "             |    ____   |              ",
            "              \\   \\__/   /_             ",
            "               \\___     _/  |>          ",
            "                   |   |---'            ",
            "                 __|   |__              ",
            "                /   \\ /   \\             ",
            "               (___) (___)              ",
            "                                        ",
        ],
        "sleeping": [
            "                              z Z z Z   ",
            "                  ___                   ",
            "           ~  __(   )__ ~    Z   z      ",
            "              /    -    \\               ",
            "             |   ~   ~  |               ",
            "             |    ____   |              ",
            "              \\   \\__/   /_             ",
            "               \\___     _/  |>          ",
            "                   |   |---'            ",
            "                 __|   |__              ",
            "                /   \\ /   \\             ",
            "               (___) (___)              ",
            "                                        ",
        ],
        "sad": [
            "                                        ",
            "                  ___                   ",
            "           ~  __(   )__ ~               ",
            "              /    ;    \\               ",
            "             |   ~   ~  |               ",
            "             |    ____   |   *sigh*     ",
            "              \\   \\__/   /_             ",
            "               \\___     _/  |>          ",
            "                   |   |---'            ",
            "                 __|   |__              ",
            "                /   \\ /   \\             ",
            "               (___) (___)              ",
            "                                        ",
        ],
    },
}


# =============================================================================
# EMOTION CLOSE-UP FACES (Compact versions for side panel)
# =============================================================================

EMOTION_CLOSEUPS = {
    "normal": [
        "              ",
        "  (o      o)  ",
        "              ",
        "      >       ",
        "              ",
    ],
    "happy": [
        "              ",
        "  (^      ^)  ",
        "              ",
        "      >       ",
        "              ",
    ],
    "ecstatic": [
        "           !! ",
        "  (★      ★)  ",
        "              ",
        "      >       ",
        "              ",
    ],
    "sad": [
        "            · ",
        "  (;      ;)  ",
        "              ",
        "      >       ",
        "              ",
    ],
    "miserable": [
        "          · · ",
        "  (T      T)  ",
        "              ",
        "      >       ",
        "              ",
    ],
    "grumpy": [
        "         hmph ",
        "  (>      <)  ",
        "              ",
        "      >       ",
        "              ",
    ],
    "content": [
        "            ~ ",
        "  (-      -)  ",
        "              ",
        "      >       ",
        "              ",
    ],
    "eating": [
        "              ",
        "  (o      o)  ",
        "              ",
        "    nom>      ",
        "              ",
    ],
    "sleeping": [
        "          zzZ ",
        "  (-      -)  ",
        "              ",
        "      >       ",
        "              ",
    ],
    "excited": [
        "           !! ",
        "  (O      O)  ",
        "              ",
        "      O       ",
        "              ",
    ],
    "confused": [
        "          ??? ",
        "  (o      ?)  ",
        "              ",
        "      >       ",
        "              ",
    ],
    "love": [
        "           <3 ",
        "  (♡      ♡)  ",
        "              ",
        "      >       ",
        "              ",
    ],
    "derpy": [
        "          ... ",
        "  (o      .)  ",
        "              ",
        "      >       ",
        "              ",
    ],
}


# Action to art state mapping
ACTION_TO_STATE = {
    "idle": "normal",
    "waddle": "waddle_left",
    "quack": "quack",
    "preen": "preen",
    "nap": "sleeping",
    "look_around": "normal",
    "splash": "splash",
    "stare_blankly": "stare",
    "chase_bug": "waddle_right",
    "flap_wings": "flap",
    "wiggle": "happy",
    "trip": "trip",
    "feed": "eating",
    "play": "happy",
    "clean": "splash",
    "pet": "ecstatic",
    "sleep": "sleeping",
}

# Mood to default state mapping
MOOD_TO_STATE = {
    MoodState.ECSTATIC: "ecstatic",
    MoodState.HAPPY: "happy",
    MoodState.CONTENT: "normal",
    MoodState.GRUMPY: "grumpy",
    MoodState.SAD: "sad",
    MoodState.MISERABLE: "miserable",
}

# Mood to close-up mapping
MOOD_TO_CLOSEUP = {
    MoodState.ECSTATIC: "ecstatic",
    MoodState.HAPPY: "happy",
    MoodState.CONTENT: "content",
    MoodState.GRUMPY: "grumpy",
    MoodState.SAD: "sad",
    MoodState.MISERABLE: "miserable",
}

# Action to close-up mapping
ACTION_TO_CLOSEUP = {
    "feed": "eating",
    "eat": "eating",
    "sleep": "sleeping",
    "nap": "sleeping",
    "pet": "love",
    "play": "excited",
    "stare_blankly": "derpy",
    "trip": "confused",
    "forgot_something": "confused",
    "quack": "happy",
    "wiggle": "ecstatic",
    "flap_wings": "excited",
    "clean": "content",
    "splash": "happy",
}


def get_duck_art(
    growth_stage: str,
    mood_state: Optional[MoodState] = None,
    action: Optional[str] = None,
) -> List[str]:
    """
    Get the appropriate duck ASCII art.

    Args:
        growth_stage: Current growth stage (egg, duckling, teen, adult, elder)
        mood_state: Current mood (optional)
        action: Current action being performed (optional)

    Returns:
        List of strings representing the ASCII art lines
    """
    # Default to adult if stage not found
    stage_art = DUCK_ART.get(growth_stage, DUCK_ART["adult"])

    # Determine which state to show
    state = "normal"

    # Action takes priority
    if action:
        state = ACTION_TO_STATE.get(action, "normal")

    # Fall back to mood-based state
    elif mood_state:
        state = MOOD_TO_STATE.get(mood_state, "normal")

    # Get the art, falling back to normal if state not found
    art = stage_art.get(state, stage_art.get("normal", ["(duck)"]))

    return art


def get_emotion_closeup(
    mood_state: Optional[MoodState] = None,
    action: Optional[str] = None,
) -> Optional[List[str]]:
    """
    Get a close-up face for an emotion/action.

    Args:
        mood_state: Current mood (optional)
        action: Current action (optional)

    Returns:
        Close-up art or None
    """
    # Action takes priority for close-ups
    if action and action in ACTION_TO_CLOSEUP:
        closeup_key = ACTION_TO_CLOSEUP[action]
        return EMOTION_CLOSEUPS.get(closeup_key)

    # Fall back to mood
    if mood_state:
        closeup_key = MOOD_TO_CLOSEUP.get(mood_state)
        if closeup_key:
            return EMOTION_CLOSEUPS.get(closeup_key)

    return None


def get_animation_frames(
    growth_stage: str,
    animation: str,
) -> List[List[str]]:
    """
    Get animation frames for a specific animation.
    """
    stage_art = DUCK_ART.get(growth_stage, DUCK_ART["adult"])

    if animation == "waddle":
        return [
            stage_art.get("waddle_left", stage_art.get("normal")),
            stage_art.get("normal", ["(duck)"]),
            stage_art.get("waddle_right", stage_art.get("normal")),
            stage_art.get("normal", ["(duck)"]),
        ]
    else:
        return [stage_art.get("normal", ["(duck)"])]


# Border characters for UI
BORDER = {
    "tl": "+",
    "tr": "+",
    "bl": "+",
    "br": "+",
    "h": "-",
    "v": "|",
}

# =============================================================================
# PLAYFIELD OBJECTS (decorations for the habitat)
# =============================================================================

PLAYFIELD_OBJECTS = {
    "flower": "*,",
    "grass": "\"\"",
    "rock": "@@",
    "mushroom": "&",
    "puddle": "~~",
    "leaf": "^",
    "acorn": "o",
    "stick": "_/",
    "butterfly": "%",
    "worm": "~",
}

# =============================================================================
# MINI DUCK SPRITES FOR PLAYFIELD (smaller, for movement)
# =============================================================================

MINI_DUCK = {
    "duckling": {
        "idle_right": [
            " __ ",
            "(o>)",
            "/'\\)",
        ],
        "idle_left": [
            " __ ",
            "(<o)",
            "(/'\\"
        ],
        "walk_right_1": [
            " __ ",
            "(o>)",
            " /')",
        ],
        "walk_right_2": [
            " __ ",
            "(o>)",
            "(/' ",
        ],
        "walk_left_1": [
            " __ ",
            "(<o)",
            "(\\' ",
        ],
        "walk_left_2": [
            " __ ",
            "(<o)",
            " '\\_)",
        ],
        "sleeping": [
            " __z",
            "(-~)",
            "~~~)",
        ],
        "sleeping_2": [
            " __Z",
            "(~-)",
            "~~~)",
        ],
        "eating": [
            " __°",
            "(o>)",
            "°'\\)",
        ],
        "eating_2": [
            " __ ",
            "(o>°",
            "/'\\)",
        ],
        "playing": [
            "\\__/",
            "(^>)",
            " '\\)",
        ],
        "playing_2": [
            " __ ",
            "(^>)!",
            " /')",
        ],
        "cleaning": [
            "~__~",
            "(o>)",
            "~~~)",
        ],
        "cleaning_2": [
            " __~",
            "~o>)",
            "~'\\)",
        ],
        "petting": [
            " __♥",
            "(^>)",
            "/'\\)",
        ],
        "petting_2": [
            "♥__ ",
            "(^>)",
            "~'\\)",
        ],
    },
    "teen": {
        "idle_right": [
            "  __  ",
            " (o_) ",
            "  /_|>",
            " (_)  ",
        ],
        "idle_left": [
            "  __  ",
            " (_o) ",
            "<|_\\  ",
            "  (_) ",
        ],
        "walk_right_1": [
            "  __  ",
            " (o_) ",
            "  /_|>",
            "  (_) ",
        ],
        "walk_right_2": [
            "  __  ",
            " (o_) ",
            "  /_|>",
            " (_)  ",
        ],
        "walk_left_1": [
            "  __  ",
            " (_o) ",
            "<|_\\  ",
            " (_)  ",
        ],
        "walk_left_2": [
            "  __  ",
            " (_o) ",
            "<|_\\  ",
            "  (_) ",
        ],
        "sleeping": [
            "  __ z",
            " (-_) Z",
            "  /~~>",
            " ~~~  ",
        ],
        "sleeping_2": [
            "  __  Z",
            " (_-) z",
            "  /~~>",
            " ~~~  ",
        ],
        "eating": [
            "  __  ",
            " (o_)°",
            "  /_|>",
            " (_)° ",
        ],
        "eating_2": [
            "  __ °",
            " (o>) ",
            " °/_|>",
            " (_)  ",
        ],
        "playing": [
            " \\__/ ",
            " (^_)!",
            "  /_|>",
            " ~ ~  ",
        ],
        "playing_2": [
            "  __! ",
            " (^_) ",
            "  \\O|>",
            "  ~ ~ ",
        ],
        "cleaning": [
            " ~~~ ",
            "~(o_)~",
            " ~/_|>",
            " ~~~  ",
        ],
        "cleaning_2": [
            "  ~~  ",
            " (o_)~",
            "~~/_|>",
            " ~~~  ",
        ],
        "petting": [
            "  __♥ ",
            " (^_) ",
            "  /_|>",
            " (_)  ",
        ],
        "petting_2": [
            " ♥__  ",
            " (^_) ",
            "  /~|>",
            " (~)  ",
        ],
    },
    "adult": {
        "idle_right": [
            "   ___   ",
            "  (o__)  ",
            " _/   \\_ ",
            "   |_|>  ",
            "  (___)  ",
        ],
        "idle_left": [
            "   ___   ",
            "  (__o)  ",
            " _/   \\_ ",
            "  <|_|   ",
            "  (___)  ",
        ],
        "walk_right_1": [
            "   ___   ",
            "  (o__)  ",
            " _/   \\_ ",
            "   |_|>  ",
            "   (__) )",
        ],
        "walk_right_2": [
            "   ___   ",
            "  (o__)  ",
            " _/   \\_ ",
            "   |_|>  ",
            "( (__)   ",
        ],
        "walk_left_1": [
            "   ___   ",
            "  (__o)  ",
            " _/   \\_ ",
            "  <|_|   ",
            "( (__)   ",
        ],
        "walk_left_2": [
            "   ___   ",
            "  (__o)  ",
            " _/   \\_ ",
            "  <|_|   ",
            "   (__) )",
        ],
        "sleeping": [
            "   ___  z",
            "  (-_-)  Z",
            " _/~~~\\_ ",
            "   ~~~   ",
            "  (___)  ",
        ],
        "sleeping_2": [
            "   ___   Z",
            "  (-.-)  z",
            " _/~~~\\_ ",
            "   ~~~   ",
            "  (___)  ",
        ],
        "eating": [
            "   ___   ",
            "  (o>_) °",
            " _/   \\_°",
            "  °|_|>  ",
            "  (___)  ",
        ],
        "eating_2": [
            "   ___  °",
            "  (o__)  ",
            " _/°  \\_°",
            "  °|_|>  ",
            "  (___)  ",
        ],
        "playing": [
            " \\ ___ /!",
            "  (^O^)  ",
            " _/   \\_ ",
            "   \\O/>  ",
            "  ~ ~ ~  ",
        ],
        "playing_2": [
            "  \\___ / ",
            "  (^o^) !",
            " _/ ! \\_ ",
            "   |_|>  ",
            "  (___)  ",
        ],
        "quack": [
            "   ___   ",
            "  (O__)!!",
            " _/   \\_ ",
            "   |_O>  ",
            "  (___)  ",
        ],
        "happy": [
            "   ___  !",
            "  (^__)  ",
            " _/   \\_ ",
            "   |_|>  ",
            "  (___)  ",
        ],
        "sad": [
            "   ___   ",
            "  (;__)  ",
            " _/   \\_ ",
            "   |_|>  ",
            "  (___) .",
        ],
        "cleaning": [
            " ~~___~~ ",
            " ~(o__)~ ",
            "~_/   \\_~",
            " ~~|_|>~~",
            " ~(~~~)~ ",
        ],
        "cleaning_2": [
            "  ~___~  ",
            " ~(^__)~ ",
            "~~/   \\~~",
            "  ~|_|>~ ",
            "  (~_~)  ",
        ],
        "petting": [
            "  ♥___♥  ",
            "  (^_^)  ",
            " _/   \\_ ",
            "   |_|>  ",
            "  (___)  ",
        ],
        "petting_2": [
            "   ___ ♥ ",
            "  (^o^)  ",
            " _/ ~ \\_ ",
            "   |~|>  ",
            "  (~_~)  ",
        ],
    },
    "elder": {
        "idle_right": [
            "  ~___~  ",
            "  (o__)  ",
            " _/   \\_ ",
            "   |_|>  ",
            "  (___)  ",
        ],
        "idle_left": [
            "  ~___~  ",
            "  (__o)  ",
            " _/   \\_ ",
            "  <|_|   ",
            "  (___)  ",
        ],
        "walk_right_1": [
            "  ~___~  ",
            "  (o__)  ",
            " _/   \\_ ",
            "   |_|>  ",
            "   (__) )",
        ],
        "walk_right_2": [
            "  ~___~  ",
            "  (o__)  ",
            " _/   \\_ ",
            "   |_|>  ",
            "( (__)   ",
        ],
        "sleeping": [
            "  ~___~ z",
            "  (-_-)  Z",
            " _/~~~\\_ ",
            "   ~~~   ",
            "  (___)  ",
        ],
        "sleeping_2": [
            "  ~___~  Z",
            "  (-.-)  z",
            " _/~~~\\_ ",
            "   ~~~   ",
            "  (___)  ",
        ],
        "eating": [
            "  ~___~  ",
            "  (o>_) °",
            " _/   \\_°",
            "  °|_|>  ",
            "  (___)  ",
        ],
        "eating_2": [
            "  ~___~ °",
            "  (o__)  ",
            " _/°  \\_°",
            "  °|_|>  ",
            "  (___)  ",
        ],
        "playing": [
            "  ~___~  ",
            "  (^__)  ",
            " _/   \\_ ",
            "   |_|>  ",
            "  (___)  ",
        ],
        "playing_2": [
            "  ~___~ !",
            "  (^__)  ",
            " _/ ~ \\_ ",
            "   |_|>  ",
            "  (~_~)  ",
        ],
        "cleaning": [
            " ~~___~~ ",
            " ~(o__)~ ",
            "~_/   \\_~",
            " ~~|_|>~~",
            " ~(~~~)~ ",
        ],
        "cleaning_2": [
            "  ~___~  ",
            " ~(^__)~ ",
            "~~/   \\~~",
            "  ~|_|>~ ",
            "  (~_~)  ",
        ],
        "petting": [
            "  ~___~♥ ",
            "  (^_^)  ",
            " _/   \\_ ",
            "   |_|>  ",
            "  (___)  ",
        ],
        "petting_2": [
            " ♥~___~  ",
            "  (^o^)  ",
            " _/ ~ \\_ ",
            "   |~|>  ",
            "  (~_~)  ",
        ],
    },
}


def get_mini_duck(
    growth_stage: str,
    state: str,
    facing_right: bool,
    animation_frame: int
) -> List[str]:
    """
    Get mini duck sprite for playfield.

    Args:
        growth_stage: Current growth stage
        state: Current state (idle, walking, sleeping, eating, playing, cleaning, petting)
        facing_right: True if facing right
        animation_frame: Animation frame number (0-3)

    Returns:
        List of strings representing the mini duck sprite
    """
    stage_sprites = MINI_DUCK.get(growth_stage, MINI_DUCK["adult"])

    # Determine which sprite to use - with animation frame alternation
    if state == "sleeping":
        # Alternate between sleeping frames
        if animation_frame % 2 == 0:
            return stage_sprites.get("sleeping", stage_sprites.get("idle_right", ["?"]))
        else:
            return stage_sprites.get("sleeping_2", stage_sprites.get("sleeping", stage_sprites.get("idle_right", ["?"])))
    elif state == "eating":
        # Alternate between eating frames
        if animation_frame % 2 == 0:
            return stage_sprites.get("eating", stage_sprites.get("idle_right", ["?"]))
        else:
            return stage_sprites.get("eating_2", stage_sprites.get("eating", stage_sprites.get("idle_right", ["?"])))
    elif state == "playing":
        # Alternate between playing frames
        if animation_frame % 2 == 0:
            return stage_sprites.get("playing", stage_sprites.get("idle_right", ["?"]))
        else:
            return stage_sprites.get("playing_2", stage_sprites.get("playing", stage_sprites.get("idle_right", ["?"])))
    elif state == "cleaning":
        # Alternate between cleaning frames
        if animation_frame % 2 == 0:
            return stage_sprites.get("cleaning", stage_sprites.get("idle_right", ["?"]))
        else:
            return stage_sprites.get("cleaning_2", stage_sprites.get("cleaning", stage_sprites.get("idle_right", ["?"])))
    elif state == "petting":
        # Alternate between petting frames
        if animation_frame % 2 == 0:
            return stage_sprites.get("petting", stage_sprites.get("happy", stage_sprites.get("idle_right", ["?"])))
        else:
            return stage_sprites.get("petting_2", stage_sprites.get("petting", stage_sprites.get("idle_right", ["?"])))
    elif state == "walking":
        # Alternate between walk frames
        direction = "right" if facing_right else "left"
        frame = (animation_frame % 2) + 1
        key = f"walk_{direction}_{frame}"
        return stage_sprites.get(key, stage_sprites.get(f"idle_{direction}", ["?"]))
    else:
        # Idle
        direction = "right" if facing_right else "left"
        return stage_sprites.get(f"idle_{direction}", stage_sprites.get("idle_right", ["?"]))


def create_box(content: List[str], width: int, title: str = "") -> List[str]:
    """Create a box around content."""
    inner_width = width - 2

    if title:
        title_part = f" {title} "
        padding = inner_width - len(title_part)
        left_pad = padding // 2
        right_pad = padding - left_pad
        top = BORDER["tl"] + BORDER["h"] * left_pad + title_part + BORDER["h"] * right_pad + BORDER["tr"]
    else:
        top = BORDER["tl"] + BORDER["h"] * inner_width + BORDER["tr"]

    bottom = BORDER["bl"] + BORDER["h"] * inner_width + BORDER["br"]

    lines = [top]
    for line in content:
        padded = line[:inner_width].ljust(inner_width)
        lines.append(BORDER["v"] + padded + BORDER["v"])
    lines.append(bottom)

    return lines


# =============================================================================
# CELEBRATION ASCII ART
# =============================================================================

# Animated celebration frames (for celebrations that animate)
CELEBRATION_FRAMES = {
    "level_up": [
        # Frame 1: Duck on ground
        [
            "    ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★    ",
            "  ╔═════════════════════╗  ",
            "  ║    LEVEL UP!!! 🎉   ║  ",
            "  ║                     ║  ",
            "  ║                     ║  ",
            "  ║       (^o^)         ║  ",
            "  ║     <(     )>       ║  ",
            "  ║        ~~~          ║  ",
            "  ║                     ║  ",
            "  ╚═════════════════════╝  ",
            "    ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★    ",
        ],
        # Frame 2: Duck jumping up
        [
            "    ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦    ",
            "  ╔═════════════════════╗  ",
            "  ║    LEVEL UP!!! 🎉   ║  ",
            "  ║      \\   ★   /      ║  ",
            "  ║       (^O^)         ║  ",
            "  ║     \\(     )/       ║  ",
            "  ║                     ║  ",
            "  ║        ~~~          ║  ",
            "  ║                     ║  ",
            "  ╚═════════════════════╝  ",
            "    ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦    ",
        ],
        # Frame 3: Duck at peak
        [
            "    ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★    ",
            "  ╔═════════════════════╗  ",
            "  ║    LEVEL UP!!! 🎉   ║  ",
            "  ║     \\  ★ ★  /       ║  ",
            "  ║       (^O^)  !!     ║  ",
            "  ║     \\(     )/       ║  ",
            "  ║                     ║  ",
            "  ║                     ║  ",
            "  ║        ~~~          ║  ",
            "  ╚═════════════════════╝  ",
            "    ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★    ",
        ],
        # Frame 4: Duck coming down
        [
            "    ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦    ",
            "  ╔═════════════════════╗  ",
            "  ║    LEVEL UP!!! 🎉   ║  ",
            "  ║        ★ ★          ║  ",
            "  ║       (^o^)         ║  ",
            "  ║     <(     )>       ║  ",
            "  ║                     ║  ",
            "  ║        ~~~          ║  ",
            "  ║                     ║  ",
            "  ╚═════════════════════╝  ",
            "    ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦    ",
        ],
    ],
}

# Static celebration art (non-animated, used as fallback)
CELEBRATION_ART = {
    "level_up": [
        "    ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★    ",
        "  ╔═════════════════════╗  ",
        "  ║    LEVEL UP!!! 🎉   ║  ",
        "  ║      \\   ★   /      ║  ",
        "  ║       (^O^)         ║  ",
        "  ║     \\(     )/       ║  ",
        "  ║        ~~~          ║  ",
        "  ║                     ║  ",
        "  ╚═════════════════════╝  ",
        "    ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★    ",
    ],
    "streak_milestone": [
        "  🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥  ",
        " ╔═══════════════════════╗ ",
        " ║   STREAK MILESTONE!   ║ ",
        " ║                       ║ ",
        " ║      \\o/  🦆  \\o/     ║ ",
        " ║       |      |        ║ ",
        " ║      / \\    / \\       ║ ",
        " ║                       ║ ",
        " ╚═══════════════════════╝ ",
        "  🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥  ",
    ],
    "collectible_found": [
        "   ✨ ✨ ✨ ✨ ✨ ✨ ✨   ",
        " ╔═════════════════════╗ ",
        " ║  RARE FIND!  ⭐     ║ ",
        " ║                     ║ ",
        " ║   [  ?  ?  ?  ]     ║ ",
        " ║                     ║ ",
        " ╚═════════════════════╝ ",
        "   ✨ ✨ ✨ ✨ ✨ ✨ ✨   ",
    ],
    "achievement": [
        "  🏆 🏆 🏆 🏆 🏆 🏆 🏆 🏆  ",
        " ╔═══════════════════════╗ ",
        " ║   ACHIEVEMENT GET!    ║ ",
        " ║                       ║ ",
        " ║        \\(^o^)/        ║ ",
        " ║                       ║ ",
        " ╚═══════════════════════╝ ",
        "  🏆 🏆 🏆 🏆 🏆 🏆 🏆 🏆  ",
    ],
    "surprise_gift": [
        "   🎁 🎁 🎁 🎁 🎁 🎁 🎁   ",
        " ╔═════════════════════╗ ",
        " ║   SURPRISE GIFT!    ║ ",
        " ║                     ║ ",
        " ║      .------.       ║ ",
        " ║     |  🎀   |       ║ ",
        " ║     |______|        ║ ",
        " ║                     ║ ",
        " ╚═════════════════════╝ ",
        "   🎁 🎁 🎁 🎁 🎁 🎁 🎁   ",
    ],
    "jackpot": [
        " 💰 💰 💰 💰 💰 💰 💰 💰 💰 ",
        "╔═══════════════════════════╗",
        "║      🎰 JACKPOT! 🎰       ║",
        "║                           ║",
        "║    ╔═══╗ ╔═══╗ ╔═══╗     ║",
        "║    ║ 7 ║ ║ 7 ║ ║ 7 ║     ║",
        "║    ╚═══╝ ╚═══╝ ╚═══╝     ║",
        "║                           ║",
        "╚═══════════════════════════╝",
        " 💰 💰 💰 💰 💰 💰 💰 💰 💰 ",
    ],
    "new_record": [
        "  🌟 🌟 🌟 🌟 🌟 🌟 🌟 🌟  ",
        " ╔═══════════════════════╗ ",
        " ║    NEW RECORD!!!      ║ ",
        " ║                       ║ ",
        " ║       🏅 #1 🏅        ║ ",
        " ║                       ║ ",
        " ╚═══════════════════════╝ ",
        "  🌟 🌟 🌟 🌟 🌟 🌟 🌟 🌟  ",
    ],
}


def get_celebration_art(celebration_type: str, frame: int = 0) -> Optional[List[str]]:
    """Get celebration ASCII art by type. Supports animation frames."""
    # Check for animated celebration
    if celebration_type in CELEBRATION_FRAMES:
        frames = CELEBRATION_FRAMES[celebration_type]
        return frames[frame % len(frames)]
    # Fallback to static art
    return CELEBRATION_ART.get(celebration_type)


def get_celebration_frame_count(celebration_type: str) -> int:
    """Get the number of animation frames for a celebration type."""
    if celebration_type in CELEBRATION_FRAMES:
        return len(CELEBRATION_FRAMES[celebration_type])
    return 1
