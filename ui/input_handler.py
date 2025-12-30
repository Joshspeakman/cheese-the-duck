"""
Keyboard input handling for the game.
"""
from typing import Optional, Callable, Dict, Any
from enum import Enum, auto


class GameAction(Enum):
    """Actions that can be triggered by input."""
    NONE = auto()
    QUIT = auto()
    RETURN_TO_TITLE = auto()
    FEED = auto()
    PLAY = auto()
    CLEAN = auto()
    PET = auto()
    SLEEP = auto()
    TALK = auto()
    MENU = auto()
    HELP = auto()
    SAVE = auto()
    DEBUG = auto()
    CONFIRM = auto()
    CANCEL = auto()


# Key mappings - Organized to avoid conflicts
# NOTE: Many keys are now handled directly in game.py for flexibility
KEY_BINDINGS = {
    # Quit
    "q": GameAction.QUIT,
    "Q": GameAction.QUIT,

    # Interactions (F, P, L, D, Z + number keys)
    "f": GameAction.FEED,
    "F": GameAction.FEED,
    "1": GameAction.FEED,

    "p": GameAction.PLAY,
    "P": GameAction.PLAY,
    "2": GameAction.PLAY,

    "l": GameAction.CLEAN,  # L for cLean
    "L": GameAction.CLEAN,
    "3": GameAction.CLEAN,

    "d": GameAction.PET,    # D for pet/aDorable
    "D": GameAction.PET,
    "4": GameAction.PET,

    "z": GameAction.SLEEP,
    "Z": GameAction.SLEEP,
    "5": GameAction.SLEEP,

    # Help
    "h": GameAction.HELP,
    "H": GameAction.HELP,
    "?": GameAction.HELP,

    # NOTE: These keys are handled directly in game.py to avoid conflicts:
    # T = Talk, S = Stats, I = Inventory, G = Goals, M = Sound toggle
    # E = Explore, C = Craft, R = Build, A = Areas, B = Shop
}


class InputHandler:
    """Handles keyboard input and maps to game actions."""

    def __init__(self, terminal):
        """
        Initialize with blessed terminal.

        Args:
            terminal: blessed Terminal instance
        """
        self.terminal = terminal
        self._callbacks: Dict[GameAction, Callable] = {}
        self._input_mode = "normal"  # normal, text, menu
        self._text_buffer = ""
        self._text_callback: Optional[Callable[[str], None]] = None

    def register_callback(self, action: GameAction, callback: Callable):
        """Register a callback for an action."""
        self._callbacks[action] = callback

    def process_key(self, key) -> GameAction:
        """
        Process a key press and return the action.

        Args:
            key: Key from terminal.inkey()

        Returns:
            GameAction triggered by the key
        """
        if key is None or key == "":
            return GameAction.NONE

        # Handle text input mode
        if self._input_mode == "text":
            return self._handle_text_input(key)

        # Handle escape key
        if key.name == "KEY_ESCAPE":
            return GameAction.CANCEL

        # Handle enter key
        if key.name == "KEY_ENTER":
            return GameAction.CONFIRM

        # Look up key binding
        key_str = str(key) if not key.name else key.name
        action = KEY_BINDINGS.get(key_str, GameAction.NONE)

        # Execute callback if registered
        if action != GameAction.NONE and action in self._callbacks:
            self._callbacks[action]()

        return action

    def _handle_text_input(self, key) -> GameAction:
        """Handle input in text entry mode."""
        if key.name == "KEY_ESCAPE":
            self._input_mode = "normal"
            self._text_buffer = ""
            return GameAction.CANCEL

        if key.name == "KEY_ENTER":
            # Submit text
            if self._text_callback:
                self._text_callback(self._text_buffer)
            self._input_mode = "normal"
            result = self._text_buffer
            self._text_buffer = ""
            return GameAction.CONFIRM

        if key.name == "KEY_BACKSPACE":
            self._text_buffer = self._text_buffer[:-1]
            return GameAction.NONE

        # Add printable characters
        if key.is_sequence is False and len(str(key)) == 1:
            self._text_buffer += str(key)

        return GameAction.NONE

    def start_text_input(self, callback: Callable[[str], None]):
        """
        Switch to text input mode.

        Args:
            callback: Function to call with the entered text
        """
        self._input_mode = "text"
        self._text_buffer = ""
        self._text_callback = callback

    def get_text_buffer(self) -> str:
        """Get current text buffer contents."""
        return self._text_buffer

    def is_text_mode(self) -> bool:
        """Check if in text input mode."""
        return self._input_mode == "text"

    def cancel_text_input(self):
        """Cancel text input and return to normal mode."""
        self._input_mode = "normal"
        self._text_buffer = ""
        self._text_callback = None


def get_help_text() -> str:
    """Get the help text for controls."""
    return """
DUCK CARE
---------
[F]/[1] Feed    [P]/[2] Play
[L]/[3] Clean   [D]/[4] Pet
[Z]/[5] Sleep

MENUS
-----
[S] Stats       [I] Inventory
[G] Goals       [T] Talk
[B] Shop        [U] Use Items

WORLD
-----
[E] Explore     [A] Areas
[C] Craft       [R] Build
[V] Decorate    [<] Trading

ACTIVITIES
----------
[J] Mini-games  [7] Tricks
[9] Garden      [0] Festivals
[=] Diary       [;] Photo

COLLECTIONS
-----------
['] Collectibles [8] Prestige
[~] Titles       [Y] Scrapbook
[\\] Secrets

OTHER
-----
[K] Duck Fact  [/] Save Slots
[M] Sound  [N] Music  [+/-] Vol
[H] Help   [Q] Quit

MENU NAVIGATION
---------------
[TAB] Main Menu
[Arrow Keys] Navigate menus
[Enter] Select/Confirm
[ESC] Close menu
"""


def get_interaction_name(action: GameAction) -> str:
    """Get display name for an interaction action."""
    names = {
        GameAction.FEED: "Feed",
        GameAction.PLAY: "Play",
        GameAction.CLEAN: "Clean",
        GameAction.PET: "Pet",
        GameAction.SLEEP: "Sleep",
        GameAction.TALK: "Talk",
    }
    return names.get(action, "Unknown")
