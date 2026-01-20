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
        "   o     o    ",
        "      >       ",
        "     ===      ",
        "              ",
    ],
    "happy": [
        "              ",
        "   ^     ^    ",
        "      >       ",
        "     ===      ",
        "              ",
    ],
    "ecstatic": [
        "            !!",
        "   *     *    ",
        "      >       ",
        "     ===      ",
        "              ",
    ],
    "sad": [
        "             .",
        "   ;     ;    ",
        "      >       ",
        "     ===      ",
        "              ",
    ],
    "miserable": [
        "           . .",
        "   T     T    ",
        "      >       ",
        "     ===      ",
        "              ",
    ],
    "grumpy": [
        "              ",
        "   >     <    ",
        "      >       ",
        "     ===      ",
        "              ",
    ],
    "content": [
        "             ~",
        "   -     -    ",
        "      >       ",
        "     ===      ",
        "              ",
    ],
    "eating": [
        "              ",
        "   o     o    ",
        "    nom>      ",
        "     ===      ",
        "              ",
    ],
    "sleeping": [
        "          zzZ ",
        "   -     -    ",
        "      >       ",
        "     ===      ",
        "              ",
    ],
    "excited": [
        "            !!",
        "   O     O    ",
        "      O       ",
        "     ===      ",
        "              ",
    ],
    "confused": [
        "           ?? ",
        "   o     ?    ",
        "      >       ",
        "     ===      ",
        "              ",
    ],
    "love": [
        "            <3",
        "   +     +    ",
        "      >       ",
        "     ===      ",
        "              ",
    ],
    "derpy": [
        "           ...",
        "   o     .    ",
        "      >       ",
        "     ===      ",
        "              ",
    ],
    "playing": [
        "            **",
        "   ^     ^    ",
        "      >       ",
        "     ===      ",
        "              ",
    ],
    "cleaning": [
        "            ~~",
        "   o     o    ",
        "      >       ",
        "    ~===~     ",
        "              ",
    ],
    "petting": [
        "            ++",
        "   ^     ^    ",
        "      >       ",
        "     ===      ",
        "              ",
    ],
    "thinking": [
        "            ??",
        "   .     _    ",
        "      >       ",
        "     ===      ",
        "              ",
    ],
    "singing": [
        "           ~~~",
        "   ^     ^    ",
        "      O       ",
        "     ===      ",
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
    # Player actions
    "feed": "eating",
    "eat": "eating",
    "sleep": "sleeping",
    "nap": "sleeping",
    "pet": "petting",
    "play": "playing",
    "clean": "cleaning",
    
    # Autonomous actions
    "idle": "content",
    "waddle": "happy",
    "quack": "happy",
    "preen": "content",
    "look_around": "thinking",
    "splash": "happy",
    "stare_blankly": "derpy",
    "chase_bug": "excited",
    "flap_wings": "excited",
    "wiggle": "ecstatic",
    "trip": "confused",
    "forgot_something": "confused",
    "singing": "singing",
    "sing": "singing",
    
    # Structure actions
    "nap_in_nest": "sleeping",
    "hide_in_shelter": "grumpy",
    "use_bird_bath": "cleaning",
    "admire_garden": "content",
    "inspect_workbench": "thinking",
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
    "nest": "(@@)",  # Cozy nest for duck to sleep in
}

# =============================================================================
# MINI DUCK SPRITES FOR PLAYFIELD (smaller, for movement)
# =============================================================================

MINI_DUCK = {
    # ===================
    # DUCKLING - tiny baby duck (3 lines)
    # ===================
    "duckling": {
        "idle_right": [" __ ", "(o>)", "/'\\)"],
        "idle_left": [" __ ", "(<o)", "(/'/"],
        "walk_right_1": [" __ ", "(o>)", " /')"],
        "walk_right_2": [" __ ", "(o>)", "(/' "],
        "walk_left_1": [" __ ", "(<o)", "(\\' "],
        "walk_left_2": [" __ ", "(<o)", " '/)"],
        "sleeping": [" __z", "(-~)", "/'/)"],
        "sleeping_2": [" __Z", "(~-)", "/'/)"],
        "eating": [" __ ", "(o>.", "/'/)"],
        "eating_2": [" __ ", "(o>)", ".'/)"],
        "playing": ["\\__/", "(^>)", " '/)"],
        "playing_2": [" __!", "(^>)", " /')"],
        "cleaning": ["~__~", "(o>)", "/'/)"],
        "cleaning_2": [" __~", "(o>)", "~'/)"],
        "petting": [" __+", "(^>)", "/'/)"],
        "petting_2": ["+__ ", "(^>)", "/'/)"],
        "swimming": [" __ ", "(o>)", "~~~)"],
        "swimming_2": [" __ ", "(o>)", "~~~)"],
        "diving": ["    ", "~~~~", "\\o>/"],
        "diving_2": [" '' ", "~~~~", "    "],
        "stretching": [" __~", "(o>)", "/'/_"],
        "stretching_2": ["\\__ ", "(^>)", " ' /"],
        "yawning": [" __o", "(O>)", "/'/)"],
        "yawning_2": [" __ ", "(O-)", "/'/)"],
        "jumping": ["\\__/", "(^>)", "    "],
        "jumping_2": [" !! ", "(^>)", "/'/)"],
        "scared": [" !! ", "(°>)", "/!/)"],
        "scared_2": [" __ ", "(°>)", " '/)"],
        "thinking": [" __?", "(._)", "/'/)"],
        "thinking_2": ["?__ ", "(.>)", "/'/)"],
        "dancing": [" ~_ ", "(^>)", " //)"],
        "dancing_2": [" _~ ", "(^>)", "(// "],
        "singing": [" ~_ ", "(O>)", "/'/)"],
        "singing_2": [" _~ ", "(O>)", "/'/)"],
        "pecking": [" __ ", "(o>.", "/'/)"],
        "pecking_2": [" __ ", "(o>)", ".'/)"],
        "flapping": ["\\__/", "(o>)", " ' )"],
        "flapping_2": [" __ ", "\\o>/", " ' )"],
        "preening": [" _~ ", "(o<)", "/'/)"],
        "preening_2": [" ~_ ", "(>o)", "/'/)"],
        "napping": [" __ ", "(-~)", "/'/)"],
        "napping_2": [" __ ", "(~-)", "/'/)"],
        "curious": [" __?", "(o>)", " '/)"],
        "curious_2": ["?__ ", "(<o)", "/'/)"],
        "waddle_fast": [" __ ", "(o>)", " /')"],
        "waddle_fast_2": [" __ ", "(o>)", "(/' "],
        "dizzy": [" __ ", "(@>)", " x/)"],
        "dizzy_2": [" __ ", "(<@)", " x/)"],
        "proud": [" _+ ", "(^>)", "/'/)"],
        "proud_2": ["+__ ", "(^>)", "/'/)"],
        "sneaking": [" .. ", "(o>)", "._/)"],
        "sneaking_2": ["... ", "(o>)", " ./)"],
        "splashing": ["'__'", "(^>)", "~~~)"],
        "splashing_2": [" '' ", "(^>)", "~~~)"],
        "floating": [" __ ", "(~>)", "~~~~"],
        "floating_2": [" ~~ ", "(->)", "~~~~"],
        "shaking": ["~__~", "(o>)", "/'/)"],
        "shaking_2": [" __'", "(o>)", "/'/)"],
        "hungry": [" __ ", "(o>)", ".'/)"],
        "hungry_2": [" __ ", "(o>)", "''/)"],
        "cold": ["*__*", "(;>)", "/'/)"],
        "cold_2": [" __ ", "(;>)", "/'/)"],
        "hot": ["~__~", "('>)", "/'/)"],
        "hot_2": [" __ ", "('>)", "/'/)"],
        "love": ["+__+", "(^>)", "/'/)"],
        "love_2": [" __ ", "(^>)", "+'/)"],
        "angry": [" _x ", "(>>)", "/'/)"],
        "angry_2": ["x__ ", "(>>)", " '/)"],
        "bored": [" __ ", "(-_)", " ./)"],
        "bored_2": [" .. ", "(_-)", " '/)"],
        "excited": ["\\!!/", "(^>)", "/'/)"],
        "excited_2": [" !! ", "(^>)", "/'/)"],
        "waving": [" __/", "(o>)", " '/)"],
        "waving_2": ["\\__ ", "(<o)", " '/)"],
        "tail_wag": [" __~", "(^>)", "/'~)"],
        "tail_wag_2": [" ~~_", "(^>)", "~'/)"],
        "happy": [" __ ", "(^>)", "/'/)"],
        "happy_2": [" __!", "(^>)", "/'/)"],
        "sad": [" __ ", "(;>)", "/'/)"],
        "sad_2": [" __ ", "(;>)", " '/)"],
        "quack": [" __ ", "(O>)", "/'/)"],
        "quack_2": [" __ ", "(O>)", "/'/)"],
    },
    # ===================
    # TEEN - slightly bigger, has attitude (3 lines)
    # ===================
    "teen": {
        "idle_right": [" _~_ ", "(o_>)", "/''\\_"],
        "idle_left": [" _~_ ", "(<_o)", "_/''\\"],
        "walk_right_1": [" _~_ ", "(o_>)", " ''\\_"],
        "walk_right_2": [" _~_ ", "(o_>)", "/''\\ "],
        "walk_left_1": [" _~_ ", "(<_o)", "_/'' "],
        "walk_left_2": [" _~_ ", "(<_o)", " /''\\"],
        "sleeping": [" _~_z", "(-_-)", "/''/"],
        "sleeping_2": [" _~_Z", "(-_-)", "/''/"],
        "eating": [" _~_ ", "(o_>.", "/''/"],
        "eating_2": [" _~_ ", "(o_>)", ".''/ "],
        "playing": ["\\_~_/", "(^_>)", " ''/"],
        "playing_2": [" _~_!", "(^_>)", " ''\\_"],
        "cleaning": ["~_~_~", "(o_>)", "/''/"],
        "cleaning_2": [" _~_~", "(o_>)", "~''/"],
        "petting": [" _~_+", "(^_>)", "/''/"],
        "petting_2": ["+_~_ ", "(^_>)", "/''/"],
        "swimming": [" _~_ ", "(o_>)", "~~~\\_"],
        "swimming_2": [" _~_ ", "(o_>)", "~~~\\_"],
        "diving": ["     ", "~~~~~", "\\o_>/"],
        "diving_2": [" ''  ", "~~~~~", "     "],
        "stretching": [" _~_~", "(o_>)", "/''/"],
        "stretching_2": ["\\_~_/", "(^_>)", " ''/"],
        "yawning": [" _~_o", "(O_>)", "/''/"],
        "yawning_2": [" _~_ ", "(O_-)", "/''/"],
        "jumping": ["\\_~_/", "(^_>)", "     "],
        "jumping_2": [" !!  ", "(^_>)", "/''/"],
        "scared": [" !!  ", "(°_>)", "/!!/"],
        "scared_2": [" _~_ ", "(°_>)", " '!/"],
        "thinking": [" _~_?", "(._>)", "/''/"],
        "thinking_2": ["?_~_ ", "(._>)", "/''/"],
        "dancing": [" ~_~ ", "(^_>)", " //\\"],
        "dancing_2": [" _~_~", "(^_>)", "/\\/ "],
        "singing": [" ~_~ ", "(O_>)", "/''/"],
        "singing_2": [" _~_~", "(O_>)", "/''/"],
        "pecking": [" _~_ ", "(o_>.", "/''/"],
        "pecking_2": [" _~_ ", "(o_>)", ".''/ "],
        "flapping": ["\\_~_/", "(o_>)", " ' /"],
        "flapping_2": [" _~_ ", "\\o_>/", " ' /"],
        "preening": [" _~_ ", "(o<_)", "/''/"],
        "preening_2": [" _~_ ", "(_>o)", "/''/"],
        "napping": [" _~_ ", "(-_-)", "/''/"],
        "curious": [" _~_?", "(o_>)", " ''/"],
        "curious_2": ["?_~_ ", "(<_o)", "/''/"],
        "waddle_fast": [" _~_ ", "(o_>)", " ''/"],
        "waddle_fast_2": [" _~_ ", "(o_>)", "/''\\ "],
        "dizzy": [" _~_ ", "(@_>)", " x'/"],
        "dizzy_2": [" _~_ ", "(<_@)", " x'/"],
        "proud": [" _+_ ", "(^_>)", "/''/"],
        "proud_2": ["+_~_ ", "(^_>)", "/''/"],
        "sneaking": [" ... ", "(o_>)", "._'/"],
        "sneaking_2": [".... ", "(o_>)", " .'/"],
        "splashing": ["'_~_'", "(^_>)", "~~~\\_"],
        "splashing_2": [" ''  ", "(^_>)", "~~~\\_"],
        "floating": [" _~_ ", "(~_>)", "~~~~~"],
        "floating_2": [" ~~~ ", "(-_>)", "~~~~~"],
        "shaking": ["~_~_~", "(o_>)", "/''/"],
        "shaking_2": [" _~_'", "(o_>)", "/''/"],
        "hungry": [" _~_ ", "(o_>)", ".''/ "],
        "hungry_2": [" _~_ ", "(o_>)", "'''/ "],
        "cold": ["*_~_*", "(;_>)", "/''/"],
        "cold_2": [" _~_ ", "(;_>)", "/''/"],
        "hot": ["~_~_~", "(>_>)", "/''/"],
        "hot_2": [" _~_ ", "(>_<)", "/''/"],
        "love": ["+_~_+", "(^_>)", "/''/"],
        "love_2": [" _~_ ", "(^_>)", "+''/"],
        "angry": [" _x_ ", "(>_<)", "/''/"],
        "angry_2": ["x_~_ ", "(>_>)", " ''/"],
        "bored": [" _~_ ", "(-_-)", " .'/"],
        "bored_2": [" ... ", "(-_-)", " ''/"],
        "excited": ["\\!!/", "(^_>)", "/''/"],
        "excited_2": [" !!  ", "(^_>)", "/''/"],
        "tail_wag": [" _~_~", "(^_>)", "/'~\\_"],
        "tail_wag_2": [" ~~_ ", "(^_>)", "~''/"],
        "happy": [" _~_!", "(^_>)", "/''/"],
        "happy_2": [" _~_ ", "(^_>)", "/''/"],
        "sad": [" _~_ ", "(;_>)", "/''/"],
        "sad_2": [" _~_ ", "(;_>)", " ''/"],
        "quack": [" _~_ ", "(O_>)", "/''/"],
        "quack_2": [" _~_ ", "(O_>)", "/''/"],
    },
    # ===================
    # ADULT - full grown duck (3 lines)
    # ===================
    "adult": {
        "idle_right": [" ___ ", "(o__)>", "/'__\\"],
        "idle_left": [" ___ ", "<(__o)", "/__'\\"],
        "walk_right_1": [" ___ ", "(o__)>", " '__\\"],
        "walk_right_2": [" ___ ", "(o__)>", "/'__ "],
        "walk_left_1": [" ___ ", "<(__o)", "__' \\"],
        "walk_left_2": [" ___ ", "<(__o)", " /__'"],
        "sleeping": [" ___z", "(-_-)>", "/'__\\"],
        "sleeping_2": [" ___Z", "(-_-)>", "/'__\\"],
        "eating": [" ___ ", "(o__>.", "/'__\\"],
        "eating_2": [" ___ ", "(o__)>", ".'__\\"],
        "playing": ["\\___ ", "(^__)>", " '__\\"],
        "playing_2": [" ___!", "(^__)>", " '__\\"],
        "quack": [" ___ ", "(O__)>", "/'__\\"],
        "quack_2": [" ___ ", "(O__)>", "/'__\\"],
        "happy": [" ___!", "(^__)>", "/'__\\"],
        "happy_2": [" ___ ", "(^__)>", "/'__\\"],
        "sad": [" ___ ", "(;__)>", "/'__\\"],
        "sad_2": [" ___ ", "(;__)>", " '__\\"],
        "cleaning": ["~___~", "(o__)>", "/'__\\"],
        "cleaning_2": [" ___~", "(o__)>", "~'__\\"],
        "petting": [" ___+", "(^__)>", "/'__\\"],
        "petting_2": ["+___ ", "(^__)>", "/'__\\"],
        "swimming": [" ___ ", "(o__)>", "~~~__"],
        "swimming_2": [" ___ ", "(o__)>", "~~~__"],
        "diving": ["     ", "~~~~~", "\\o__>"],
        "diving_2": [" ''  ", "~~~~~", "     "],
        "stretching": [" ___~", "(o__)>", "/'__/"],
        "stretching_2": ["\\___ ", "(^__)>", " '__\\"],
        "yawning": [" ___o", "(O__)>", "/'__\\"],
        "yawning_2": [" ___ ", "(O_-)>", "/'__\\"],
        "jumping": ["\\___ ", "(^__)>", "     "],
        "jumping_2": [" !!! ", "(^__)>", "/'__\\"],
        "scared": [" !!! ", "(°__)>", "/!__\\"],
        "scared_2": [" ___ ", "(°__)>", " '!_\\"],
        "thinking": [" ___?", "(.__)>", "/'__\\"],
        "thinking_2": ["?___ ", "(.__)>", "/'__\\"],
        "dancing": [" ~_~ ", "(^__)>", " //__"],
        "dancing_2": [" _~_~", "(^__)>", "__// "],
        "singing": [" ~__ ", "(O__)>", "/'__\\"],
        "singing_2": [" __~ ", "(O__)>", "/'__\\"],
        "pecking": [" ___ ", "(o__>.", "/'__\\"],
        "pecking_2": [" ___ ", "(o__)>", ".'__\\"],
        "flapping": ["\\___ ", "(o__)>", " ' _\\"],
        "flapping_2": [" ___ ", "\\o__/>", " ' _\\"],
        "preening": [" ___ ", "(o<_)>", "/'__\\"],
        "preening_2": [" ___ ", "(_>o)>", "/'__\\"],
        "napping": [" ___ ", "(-_-)>", "/'__\\"],
        "napping_2": [" ___ ", "(-_-)>", "/'__\\"],
        "curious": [" ___?", "(o__)>", " '__\\"],
        "curious_2": ["?___ ", "<(__o)", "/'__\\"],
        "waddle_fast": [" ___ ", "(o__)>", " '__\\"],
        "waddle_fast_2": [" ___ ", "(o__)>", "/'__ "],
        "dizzy": [" ___ ", "(@__)>", " x'_\\"],
        "dizzy_2": [" ___ ", "<(__@)", " x'_\\"],
        "proud": [" _+_ ", "(^__)>", "/'__\\"],
        "proud_2": ["+___ ", "(^__)>", "/'__\\"],
        "sneaking": [" ... ", "(o__)>", "._'_\\"],
        "sneaking_2": [".... ", "(o__)>", " .'_\\"],
        "splashing": ["'___'", "(^__)>", "~~~__"],
        "splashing_2": [" ''  ", "(^__)>", "~~~__"],
        "floating": [" ___ ", "(~__)>", "~~~~~"],
        "floating_2": [" ~~~ ", "(-__)>", "~~~~~"],
        "shaking": ["~___~", "(o__)>", "/'__\\"],
        "shaking_2": [" ___'", "(o__)>", "/'__\\"],
        "hungry": [" ___ ", "(o__)>", ".'__\\"],
        "hungry_2": [" ___ ", "(o__)>", "''__\\"],
        "cold": ["*___*", "(;__)>", "/'__\\"],
        "cold_2": [" ___ ", "(;__)>", "/'__\\"],
        "hot": ["~___~", "(>__)>", "/'__\\"],
        "hot_2": [" ___ ", "(>_<)>", "/'__\\"],
        "love": ["+___+", "(^__)>", "/'__\\"],
        "love_2": [" ___ ", "(^__)>", "+'__\\"],
        "angry": [" _x_ ", "(>_<)>", "/'__\\"],
        "angry_2": ["x___ ", "(>__)>", " '__\\"],
        "bored": [" ___ ", "(-_-)>", " .'_\\"],
        "bored_2": [" ... ", "(-_-)>", " '__\\"],
        "excited": ["\\!!!/", "(^__)>", "/'__\\"],
        "excited_2": [" !!! ", "(^__)>", "/'__\\"],
        "waving": [" ___/", "(o__)>", " '__\\"],
        "waving_2": ["\\___ ", "<(__o)", " '__\\"],
        "tail_wag": [" ___~", "(^__)>", "/'~_\\"],
        "tail_wag_2": [" ~~_ ", "(^__)>", "~'__\\"],
    },
    # ===================
    # ELDER - wise old duck with tufts (3 lines)
    # ===================
    "elder": {
        "idle_right": ["~___~", "(o__)>", "/'__\\"],
        "idle_left": ["~___~", "<(__o)", "/__'\\"],
        "walk_right_1": ["~___~", "(o__)>", " '__\\"],
        "walk_right_2": ["~___~", "(o__)>", "/'__ "],
        "walk_left_1": ["~___~", "<(__o)", "__' \\"],
        "walk_left_2": ["~___~", "<(__o)", " /__'"],
        "sleeping": ["~___~z", "(-_-)>", "/'__\\"],
        "sleeping_2": ["~___~Z", "(-_-)>", "/'__\\"],
        "eating": ["~___~", "(o__>.", "/'__\\"],
        "eating_2": ["~___~", "(o__)>", ".'__\\"],
        "playing": ["~___~", "(^__)>", " '__\\"],
        "playing_2": ["~___~!", "(^__)>", " '__\\"],
        "cleaning": ["~___~", "(o__)>", "/'__\\"],
        "cleaning_2": ["~___~", "(o__)>", "~'__\\"],
        "petting": ["~___~+", "(^__)>", "/'__\\"],
        "petting_2": ["+~___~", "(^__)>", "/'__\\"],
        "swimming": ["~___~", "(o__)>", "~~~__"],
        "swimming_2": ["~___~", "(o__)>", "~~~__"],
        "diving": ["     ", "~~~~~", "\\o__>"],
        "diving_2": [" ''  ", "~~~~~", "     "],
        "stretching": ["~___~~", "(o__)>", "/'__/"],
        "stretching_2": ["\\~___~", "(^__)>", " '__\\"],
        "yawning": ["~___~o", "(O__)>", "/'__\\"],
        "yawning_2": ["~___~", "(O_-)>", "/'__\\"],
        "jumping": ["\\~___~", "(^__)>", "     "],
        "jumping_2": ["~!!!~", "(^__)>", "/'__\\"],
        "scared": ["~!!!~", "(°__)>", "/!__\\"],
        "scared_2": ["~___~", "(°__)>", " '!_\\"],
        "thinking": ["~___~?", "(.__)>", "/'__\\"],
        "thinking_2": ["?~___~", "(.__)>", "/'__\\"],
        "dancing": ["~~_~~", "(^__)>", " //__"],
        "dancing_2": ["~_~_~", "(^__)>", "__// "],
        "singing": ["~~__~", "(O__)>", "/'__\\"],
        "singing_2": ["~__~~", "(O__)>", "/'__\\"],
        "pecking": ["~___~", "(o__>.", "/'__\\"],
        "pecking_2": ["~___~", "(o__)>", ".'__\\"],
        "flapping": ["\\~___~", "(o__)>", " ' _\\"],
        "flapping_2": ["~___~", "\\o__/>", " ' _\\"],
        "preening": ["~___~", "(o<_)>", "/'__\\"],
        "preening_2": ["~___~", "(_>o)>", "/'__\\"],
        "napping": ["~___~", "(-_-)>", "/'__\\"],
        "napping_2": ["~___~", "(-_-)>", "/'__\\"],
        "curious": ["~___~?", "(o__)>", " '__\\"],
        "curious_2": ["?~___~", "<(__o)", "/'__\\"],
        "waddle_fast": ["~___~", "(o__)>", " '__\\"],
        "waddle_fast_2": ["~___~", "(o__)>", "/'__ "],
        "dizzy": ["~___~", "(@__)>", " x'_\\"],
        "dizzy_2": ["~___~", "<(__@)", " x'_\\"],
        "proud": ["~_+_~", "(^__)>", "/'__\\"],
        "proud_2": ["+~___~", "(^__)>", "/'__\\"],
        "sneaking": ["~...~", "(o__)>", "._'_\\"],
        "sneaking_2": ["~....~", "(o__)>", " .'_\\"],
        "splashing": ["'~___~'", "(^__)>", "~~~__"],
        "splashing_2": [" ''  ", "(^__)>", "~~~__"],
        "floating": ["~___~", "(~__)>", "~~~~~"],
        "floating_2": ["~~~~~", "(-__)>", "~~~~~"],
        "shaking": ["~~___~~", "(o__)>", "/'__\\"],
        "shaking_2": ["~___~'", "(o__)>", "/'__\\"],
        "hungry": ["~___~", "(o__)>", ".'__\\"],
        "hungry_2": ["~___~", "(o__)>", "''__\\"],
        "cold": ["*~___~*", "(;__)>", "/'__\\"],
        "cold_2": ["~___~", "(;__)>", "/'__\\"],
        "hot": ["~~___~~", "(>__)>", "/'__\\"],
        "hot_2": ["~___~", "(>_<)>", "/'__\\"],
        "love": ["+~___~+", "(^__)>", "/'__\\"],
        "love_2": ["~___~", "(^__)>", "+'__\\"],
        "angry": ["~_x_~", "(>_<)>", "/'__\\"],
        "angry_2": ["x~___~", "(>__)>", " '__\\"],
        "bored": ["~___~", "(-_-)>", " .'_\\"],
        "bored_2": ["~...~", "(-_-)>", " '__\\"],
        "excited": ["\\~!!!~/", "(^__)>", "/'__\\"],
        "excited_2": ["~!!!~", "(^__)>", "/'__\\"],
        "waving": ["~___~/", "(o__)>", " '__\\"],
        "waving_2": ["\\~___~", "<(__o)", " '__\\"],
        "tail_wag": ["~___~~", "(^__)>", "/'~_\\"],
        "tail_wag_2": ["~~_~", "(^__)>", "~'__\\"],
        "happy": ["~___~!", "(^__)>", "/'__\\"],
        "happy_2": ["~___~", "(^__)>", "/'__\\"],
        "sad": ["~___~", "(;__)>", "/'__\\"],
        "sad_2": ["~___~", "(;__)>", " '__\\"],
        "quack": ["~___~", "(O__)>", "/'__\\"],
        "quack_2": ["~___~", "(O__)>", "/'__\\"],
        "reminiscing": ["~___~", "(.__)>", "/'__\\"],
        "reminiscing_2": ["~___~.", "(.__)>", "/'__\\"],
        "wise": ["~___~+", "(^__)>", "/'__\\"],
        "wise_2": ["+~___~", "(^__)>", "/'__\\"],
    },
    # ===================
    # EGG - before hatching (3 lines)
    # ===================
    "egg": {
        "idle_right": ["  __  ", " /  \\ ", " \\__/ "],
        "idle_left": ["  __  ", " /  \\ ", " \\__/ "],
        "walk_right_1": ["  __  ", " /  \\ ", " \\__/ "],
        "walk_right_2": ["  __  ", " /  \\ ", " \\__/ "],
        "walk_left_1": ["  __  ", " /  \\ ", " \\__/ "],
        "walk_left_2": ["  __  ", " /  \\ ", " \\__/ "],
        "sleeping": ["  __z ", " /  \\ ", " \\__/ "],
        "sleeping_2": ["  __Z ", " /  \\ ", " \\__/ "],
        "eating": ["  __  ", " /  \\ ", " \\__/ "],
        "eating_2": ["  __  ", " /  \\ ", " \\__/ "],
        "playing": ["  __  ", " /  \\ ", " \\__/ "],
        "playing_2": [" ~__~ ", " /  \\ ", " \\__/ "],
    },
    # ===================
    # HATCHLING - tiny freshly-hatched (3 lines)
    # ===================
    "hatchling": {
        "idle_right": [" ,, ", "(o>)", " /)"],
        "idle_left": [" ,, ", "(<o)", "(\\ "],
        "walk_right_1": [" ,, ", "(o>)", "  )"],
        "walk_right_2": [" ,, ", "(o>)", " /) "],
        "walk_left_1": [" ,, ", "(<o)", "(  "],
        "walk_left_2": [" ,, ", "(<o)", " (\\ "],
        "sleeping": [" ,,z", "(-~)", " /)"],
        "sleeping_2": [" ,,Z", "(~-)", " /)"],
        "eating": [" ,, ", "(o>.", " /)"],
        "eating_2": [" ,, ", "(o>)", "' )"],
        "playing": ["\\,,/", "(^>)", " /)"],
        "playing_2": [" ,,!", "(^>)", " /)"],
        "cleaning": ["~,,~", "(o>)", " /)"],
        "cleaning_2": [" ,,~", "(o>)", "~/)"],
        "petting": [" ,,+", "(^>)", " /)"],
        "petting_2": ["+,, ", "(^>)", " /)"],
        "swimming": [" ,, ", "(o>)", "~~~"],
        "swimming_2": [" ,, ", "(o>)", "~~~"],
        "hungry": [" ,, ", "(o>)", "' )"],
        "hungry_2": [" ,, ", "(o>)", "  )"],
        "cold": ["*,,*", "(;>)", " /)"],
        "cold_2": [" ,, ", "(;>)", " /)"],
        "hot": ["~,,~", "('>)", " /)"],
        "hot_2": [" ,, ", "('>)", " /)"],
        "love": ["+,,+", "(^>)", " /)"],
        "love_2": [" ,, ", "(^>)", "+/)"],
        "scared": [" !! ", "(°>)", "/!)"],
        "scared_2": [" ,, ", "(°>)", " /)"],
        "happy": [" ,, ", "(^>)", " /)"],
        "happy_2": [" ,,!", "(^>)", " /)"],
        "sad": [" ,, ", "(;>)", " /)"],
        "sad_2": [" ,, ", "(;>)", "  )"],
    },
    # ===================
    # LEGENDARY - ancient, mystical duck (3 lines)
    # ===================
    "legendary": {
        "idle_right": ["*~___~*", "(^_^)>", "/'=='\\_"],
        "idle_left": ["*~___~*", "<(^_^)", "_/'=='\\"],
        "walk_right_1": ["*~___~*", "(^_^)>", " '=='\\_"],
        "walk_right_2": ["*~___~*", "(^_^)>", "/'=='\\ "],
        "walk_left_1": ["*~___~*", "<(^_^)", "_/'==' "],
        "walk_left_2": ["*~___~*", "<(^_^)", " /'=='\\"],
        "sleeping": ["*~___~z", "(-_-)>", "/'=='/"],
        "sleeping_2": ["z~___~*", "(-_-)>", "/'=='/"],
        "eating": ["*~___~*", "(^_^)>.", "/'=='/ "],
        "eating_2": ["*~___~*", "(^_^)>", ".=='/ "],
        "playing": ["\\~___~/", "(^_^)>", " '=='/"],
        "playing_2": ["*~___~!", "(^_^)>", " '=='\\_"],
        "cleaning": ["~~___~~", "(^_^)>", "/'=='/ "],
        "cleaning_2": ["*~___~*", "(^_^)>", "~~=='/"],
        "petting": ["*~___~+", "(^_^)>", "/'=='/"],
        "petting_2": ["+~___~*", "(^_^)>", "/'=='/"],
        "wise": ["*~___~*", "(^_^)>", "/'=='/"],
        "wise_2": ["**___**", "(^_^)>", "/'=='/"],
        "reminiscing": ["*~___~*", "(._.)>", "/'=='/"],
        "reminiscing_2": [".~___~*", "(._.)>", "/'=='/"],
        "happy": ["*~___~*!", "(^_^)>", "/'=='/"],
        "happy_2": ["*~___~*", "(^_^)>", "/'=='/"],
        "sad": ["*~___~*", "(;_;)>", "/'=='/"],
        "sad_2": ["*~___~*", "(;_;)>", " '=='/"],
    },
}

# Stage mapping: maps new aging system stages to existing sprite sets
STAGE_SPRITE_MAP = {
    "egg": "egg",
    "hatchling": "hatchling",
    "duckling": "duckling",
    "juvenile": "teen",
    "young_adult": "adult",
    "adult": "adult",
    "mature": "elder",
    "elder": "elder",
    "legendary": "legendary",
    # Keep old names working too
    "teen": "teen",
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
        state: Current state (idle, walking, sleeping, eating, playing, cleaning, petting,
               swimming, diving, stretching, yawning, jumping, scared, thinking, dancing,
               singing, pecking, flapping, preening, napping, curious, waddle_fast, dizzy,
               proud, sneaking, splashing, floating, shaking, hungry, cold, hot, love,
               angry, bored, excited, waving, tail_wag, reminiscing, wise, hiding)
        facing_right: True if facing right
        animation_frame: Animation frame number (0-3)

    Returns:
        List of strings representing the mini duck sprite
    """
    # Map new stage names to sprite sets
    mapped_stage = STAGE_SPRITE_MAP.get(growth_stage, growth_stage)
    stage_sprites = MINI_DUCK.get(mapped_stage, MINI_DUCK["adult"])

    # Map some states to their sprite equivalents
    state_sprite_map = {
        "hiding": "scared",  # Use scared sprite for hiding
    }
    sprite_state = state_sprite_map.get(state, state)

    # List of all animatable states with frame alternation
    animatable_states = [
        "sleeping", "eating", "playing", "cleaning", "petting",
        "swimming", "diving", "stretching", "yawning", "jumping",
        "scared", "thinking", "dancing", "singing", "pecking",
        "flapping", "preening", "napping", "curious", "waddle_fast",
        "dizzy", "proud", "sneaking", "splashing", "floating",
        "shaking", "hungry", "cold", "hot", "love", "angry",
        "bored", "excited", "waving", "tail_wag", "reminiscing", "wise"
    ]

    if sprite_state in animatable_states:
        # Alternate between frames for animated states
        if animation_frame % 2 == 0:
            sprite = stage_sprites.get(sprite_state, stage_sprites.get("idle_right", ["?"]))
        else:
            sprite = stage_sprites.get(f"{sprite_state}_2", stage_sprites.get(sprite_state, stage_sprites.get("idle_right", ["?"])))
        return sprite
    elif state == "walking":
        # Alternate between walk frames
        direction = "right" if facing_right else "left"
        frame = (animation_frame % 2) + 1
        key = f"walk_{direction}_{frame}"
        return stage_sprites.get(key, stage_sprites.get(f"idle_{direction}", ["?"]))
    else:
        # Idle or unknown state - fallback to idle
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
            "    * + * + * + * + *    ",
            "  +=====================+  ",
            "  |    LEVEL UP!!! !   |  ",
            "  |                     |  ",
            "  |                     |  ",
            "  |       (^o^)         |  ",
            "  |     <(     )>       |  ",
            "  |        ~~~          |  ",
            "  |                     |  ",
            "  +=====================+  ",
            "    * + * + * + * + *    ",
        ],
        # Frame 2: Duck jumping up
        [
            "    + * + * + * + * +    ",
            "  +=====================+  ",
            "  |    LEVEL UP!!! !   |  ",
            "  |      \\   *   /      |  ",
            "  |       (^O^)         |  ",
            "  |     \\(     )/       |  ",
            "  |                     |  ",
            "  |        ~~~          |  ",
            "  |                     |  ",
            "  +=====================+  ",
            "    + * + * + * + * +    ",
        ],
        # Frame 3: Duck at peak
        [
            "    * + * + * + * + *    ",
            "  +=====================+  ",
            "  |    LEVEL UP!!! !   |  ",
            "  |     \\  * *  /       |  ",
            "  |       (^O^)  !!     |  ",
            "  |     \\(     )/       |  ",
            "  |                     |  ",
            "  |                     |  ",
            "  |        ~~~          |  ",
            "  +=====================+  ",
            "    * + * + * + * + *    ",
        ],
        # Frame 4: Duck coming down
        [
            "    + * + * + * + * +    ",
            "  +=====================+  ",
            "  |    LEVEL UP!!! !   |  ",
            "  |        * *          |  ",
            "  |       (^o^)         |  ",
            "  |     <(     )>       |  ",
            "  |                     |  ",
            "  |        ~~~          |  ",
            "  |                     |  ",
            "  +=====================+  ",
            "    + * + * + * + * +    ",
        ],
    ],
}

# Static celebration art (non-animated, used as fallback)
CELEBRATION_ART = {
    "level_up": [
        "    * + * + * + * + *    ",
        "  +=====================+  ",
        "  |    LEVEL UP!!! !   |  ",
        "  |      \\   *   /      |  ",
        "  |       (^O^)         |  ",
        "  |     \\(     )/       |  ",
        "  |        ~~~          |  ",
        "  |                     |  ",
        "  +=====================+  ",
        "    * + * + * + * + *    ",
    ],
    "streak_milestone": [
        "  * * * * * * * * *  ",
        " +=======================+ ",
        " |   STREAK MILESTONE!   | ",
        " |                       | ",
        " |      \\o/  @  \\o/     | ",
        " |       |      |        | ",
        " |      / \\    / \\       | ",
        " |                       | ",
        " +=======================+ ",
        "  * * * * * * * * *  ",
    ],
    "collectible_found": [
        "   * * * * * * *   ",
        " +=====================+ ",
        " |  RARE FIND!  *     | ",
        " |                     | ",
        " |   [  ?  ?  ?  ]     | ",
        " |                     | ",
        " +=====================+ ",
        "   * * * * * * *   ",
    ],
    "achievement": [
        "  # # # # # # # #  ",
        " +=======================+ ",
        " |   ACHIEVEMENT GET!    | ",
        " |                       | ",
        " |        \\(^o^)/        | ",
        " |                       | ",
        " +=======================+ ",
        "  # # # # # # # #  ",
    ],
    "surprise_gift": [
        "   = = = = = = =   ",
        " +=====================+ ",
        " |   SURPRISE GIFT!    | ",
        " |                     | ",
        " |      .------.       | ",
        " |     |  X   |       | ",
        " |     |______|        | ",
        " |                     | ",
        " +=====================+ ",
        "   = = = = = = =   ",
    ],
    "jackpot": [
        " $ $ $ $ $ $ $ $ $ ",
        "+===========================+",
        "|      * JACKPOT! *       |",
        "|                           |",
        "|    +===+ +===+ +===+     |",
        "|    | 7 | | 7 | | 7 |     |",
        "|    +===+ +===+ +===+     |",
        "|                           |",
        "+===========================+",
        " $ $ $ $ $ $ $ $ $ ",
    ],
    "new_record": [
        "  * * * * * * * *  ",
        " +=======================+ ",
        " |    NEW RECORD!!!      | ",
        " |                       | ",
        " |       @ #1 @        | ",
        " |                       | ",
        " +=======================+ ",
        "  * * * * * * * *  ",
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
