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
    "happy": [
        "  (^)  (^)  ",
        "   \\____/   ",
        "    \\__/    ",
        "     |>     ",
        "  * HAPPY *  ",
    ],
    "ecstatic": [
        " *(*) (*)* ",
        "   \\____/   ",
        "    \\O/     ",
        "     O>  !! ",
        " ECSTATIC!! ",
    ],
    "sad": [
        "  (;)  (;)  ",
        "   \\____/   ",
        "    \\__/    ",
        "     |>  '  ",
        "  * sad *   ",
    ],
    "miserable": [
        "  (T)  (T)  ",
        " ' \\____/ ' ",
        "    \\__/    ",
        "  '  |>  '  ",
        " *miserable*",
    ],
    "grumpy": [
        " >(>)  (>)< ",
        "   ______   ",
        "    \\__/    ",
        "     |> hmph",
        "  *GRUMPY*  ",
    ],
    "content": [
        "  (-)  (-)  ",
        "   \\____/   ",
        "    \\__/    ",
        "     |>     ",
        " ~ content ~",
    ],
    "eating": [
        "  (o)  (o)  ",
        "   \\____/   ",
        " nom\\O/nom  ",
        "   .,.,.,   ",
        " *NOM NOM!* ",
    ],
    "sleeping": [
        "  (-)  (-) z",
        "   \\____/ Z ",
        "    \\__/  z ",
        "     |>     ",
        "  z z z z   ",
    ],
    "excited": [
        " !(O)  (O)! ",
        "   \\____/   ",
        "    \\__/    ",
        "     O> !!! ",
        " *EXCITED!* ",
    ],
    "confused": [
        "  (o)  (.)? ",
        "   \\____/   ",
        "    \\__/  ? ",
        "     |> ??? ",
        " *confused* ",
    ],
    "love": [
        " <3(^)(^)<3 ",
        "   \\____/   ",
        "  <3\\__/<3  ",
        "     |> <3  ",
        " ** LOVE ** ",
    ],
    "derpy": [
        "  (o)  ( .) ",
        "   \\____/   ",
        "    \\__/    ",
        "     |> ... ",
        "  *derp...*  ",
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
            " __ z",
            "(-~)",
            "/'\\)",
        ],
        "eating": [
            " __ ",
            "(o>.",
            "/'\\)",
        ],
        "playing": [
            "\\ __",
            "(O>)",
            " '\\)",
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
            " (-~) ",
            "  /_|>",
            " (_)  ",
        ],
        "eating": [
            "  __  ",
            " (o_)>",
            "  /_| ",
            " (_)  ",
        ],
        "playing": [
            " \\__/ ",
            " (O_) ",
            "  /_|>",
            " (_)  ",
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
            "  (-_~) Z",
            " _/   \\_ ",
            "   |_|>  ",
            "  (___)  ",
        ],
        "eating": [
            "   ___   ",
            "  (o__) ~",
            " _/   \\_.",
            "   |_|>  ",
            "  (___)  ",
        ],
        "playing": [
            " \\ ___ / ",
            "  (O__)  ",
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
            "  (-_~) Z",
            " _/   \\_ ",
            "   |_|>  ",
            "  (___)  ",
        ],
        "eating": [
            "  ~___~  ",
            "  (o__) ~",
            " _/   \\_.",
            "   |_|>  ",
            "  (___)  ",
        ],
        "playing": [
            "  ~___~  ",
            "  (^__)  ",
            " _/   \\_ ",
            "   |_|>  ",
            "  (___)  ",
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
        state: Current state (idle, walking, sleeping, eating, playing)
        facing_right: True if facing right
        animation_frame: Animation frame number (0-3)

    Returns:
        List of strings representing the mini duck sprite
    """
    stage_sprites = MINI_DUCK.get(growth_stage, MINI_DUCK["adult"])

    # Determine which sprite to use
    if state == "sleeping":
        return stage_sprites.get("sleeping", stage_sprites.get("idle_right", ["?"]))
    elif state == "eating":
        return stage_sprites.get("eating", stage_sprites.get("idle_right", ["?"]))
    elif state == "playing":
        return stage_sprites.get("playing", stage_sprites.get("idle_right", ["?"]))
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
