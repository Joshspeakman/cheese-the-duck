"""
Cosmetics system - renders hats and accessories on the duck.
Features mini-sized cosmetics with color support for the playfield duck.
"""
from typing import List, Dict, Optional, Callable
from blessed import Terminal

# Global terminal instance for colors
_term = Terminal()


# Color functions for cosmetic rendering
class CosmeticColors:
    """Color wrappers for cosmetic items."""
    RED = lambda s: _term.red(s)
    BRIGHT_RED = lambda s: _term.bright_red(s)
    BLUE = lambda s: _term.blue(s)
    BRIGHT_BLUE = lambda s: _term.bright_blue(s)
    YELLOW = lambda s: _term.yellow(s)
    BRIGHT_YELLOW = lambda s: _term.bright_yellow(s)
    GREEN = lambda s: _term.green(s)
    BRIGHT_GREEN = lambda s: _term.bright_green(s)
    MAGENTA = lambda s: _term.magenta(s)
    BRIGHT_MAGENTA = lambda s: _term.bright_magenta(s)
    CYAN = lambda s: _term.cyan(s)
    BRIGHT_CYAN = lambda s: _term.bright_cyan(s)
    WHITE = lambda s: _term.white(s)
    BRIGHT_WHITE = lambda s: _term.bright_white(s)
    ORANGE = lambda s: _term.color(208)(s)  # Orange via 256 color
    PINK = lambda s: _term.color(213)(s)  # Pink via 256 color
    GOLD = lambda s: _term.color(220)(s)  # Gold via 256 color
    PURPLE = lambda s: _term.color(135)(s)  # Purple via 256 color
    BROWN = lambda s: _term.color(130)(s)  # Brown via 256 color
    SILVER = lambda s: _term.color(250)(s)  # Silver/gray via 256 color
    BLACK = lambda s: _term.color(232)(s)  # Near-black via 256 color

C = CosmeticColors  # Shorthand


# Mini cosmetics designed to fit 3-4 line duck sprites
# Each entry has: char(s), y_offset (from top of duck), x_offset (from center), color_func
MINI_COSMETIC_ART = {
    # ============ HATS (displayed above head) ============
    "hat_red": {
        "position": "above",
        "lines": [("^", C.RED)],
        "y_offset": -1, "x_offset": 0
    },
    "hat_blue": {
        "position": "above",
        "lines": [("^", C.BLUE)],
        "y_offset": -1, "x_offset": 0
    },
    "hat_party": {
        "position": "above",
        "lines": [("*", C.BRIGHT_YELLOW), ("△", C.BRIGHT_MAGENTA)],
        "y_offset": -2, "x_offset": 0
    },
    "hat_chef": {
        "position": "above",
        "lines": [("#", C.BRIGHT_WHITE)],
        "y_offset": -1, "x_offset": 0
    },
    "hat_wizard": {
        "position": "above",
        "lines": [("*", C.BRIGHT_YELLOW), ("◢", C.PURPLE)],
        "y_offset": -2, "x_offset": 0
    },
    "hat_crown": {
        "position": "above",
        "lines": [("^", C.GOLD)],
        "y_offset": -1, "x_offset": 0
    },
    "hat_viking": {
        "position": "above",
        "lines": [("⌐■", C.SILVER)],
        "y_offset": -1, "x_offset": -1
    },
    "hat_pirate": {
        "position": "above",
        "lines": [("X", C.WHITE)],
        "y_offset": -1, "x_offset": 0
    },
    "hat_cowboy": {
        "position": "above",
        "lines": [("◠", C.BROWN)],
        "y_offset": -1, "x_offset": 0
    },
    "hat_tophat": {
        "position": "above",
        "lines": [("▀", C.BLACK), ("█", C.BLACK)],
        "y_offset": -2, "x_offset": 0
    },
    "hat_beret": {
        "position": "above",
        "lines": [("◖", C.RED)],
        "y_offset": -1, "x_offset": 0
    },
    "hat_beanie": {
        "position": "above",
        "lines": [("◕", C.BLUE)],
        "y_offset": -1, "x_offset": 0
    },
    "hat_sombrero": {
        "position": "above",
        "lines": [("◠◠", C.ORANGE)],
        "y_offset": -1, "x_offset": -1
    },
    "party_hat": {
        "position": "above",
        "lines": [("*", C.BRIGHT_CYAN), ("^", C.BRIGHT_MAGENTA)],
        "y_offset": -2, "x_offset": 0
    },
    "cap_sports": {
        "position": "above",
        "lines": [("⌐", C.BRIGHT_RED)],
        "y_offset": -1, "x_offset": 0
    },
    "beanie_striped": {
        "position": "above",
        "lines": [("≋", C.BRIGHT_GREEN)],
        "y_offset": -1, "x_offset": 0
    },
    "crown_golden": {
        "position": "above",
        "lines": [("^", C.GOLD)],
        "y_offset": -1, "x_offset": 0
    },
    "viking_helmet": {
        "position": "above",
        "lines": [("⋀", C.SILVER)],
        "y_offset": -1, "x_offset": 0
    },
    "wizard_hat": {
        "position": "above",
        "lines": [("*", C.BRIGHT_YELLOW), ("^", C.PURPLE)],
        "y_offset": -2, "x_offset": 0
    },
    "pirate_hat": {
        "position": "above",
        "lines": [("#", C.WHITE)],
        "y_offset": -1, "x_offset": 0
    },
    "flower_crown": {
        "position": "above",
        "lines": [("*", C.PINK)],
        "y_offset": -1, "x_offset": 0
    },
    "space_helmet": {
        "position": "above",
        "lines": [("◯", C.BRIGHT_CYAN)],
        "y_offset": -1, "x_offset": 0
    },
    "hat_jester": {
        "position": "above",
        "lines": [("**", C.BRIGHT_MAGENTA)],
        "y_offset": -1, "x_offset": -1
    },
    "propeller_hat": {
        "position": "above",
        "lines": [("⌘", C.BRIGHT_RED)],
        "y_offset": -1, "x_offset": 0
    },
    "graduation_cap": {
        "position": "above",
        "lines": [("▬", C.BLACK)],
        "y_offset": -1, "x_offset": 0
    },
    "tiara": {
        "position": "above",
        "lines": [("*", C.PINK)],
        "y_offset": -1, "x_offset": 0
    },
    "antenna": {
        "position": "above",
        "lines": [("•", C.BRIGHT_GREEN), ("|", C.GREEN)],
        "y_offset": -2, "x_offset": 0
    },
    "nurse_cap": {
        "position": "above",
        "lines": [("+", C.BRIGHT_RED)],
        "y_offset": -1, "x_offset": 0
    },
    "pilot_cap": {
        "position": "above",
        "lines": [(">", C.BRIGHT_BLUE)],
        "y_offset": -1, "x_offset": 0
    },
    "detective_hat": {
        "position": "above",
        "lines": [("◢", C.BROWN)],
        "y_offset": -1, "x_offset": 0
    },
    "cat_ears": {
        "position": "above",
        "lines": [("∧∧", C.ORANGE)],
        "y_offset": -1, "x_offset": -1
    },
    "bunny_ears": {
        "position": "above",
        "lines": [("())", C.PINK)],
        "y_offset": -1, "x_offset": -1
    },
    
    # ============ GLASSES (overlay on face line) ============
    "glasses_cool": {
        "position": "face",
        "lines": [("■■", C.BLACK)],
        "y_offset": 0, "x_offset": -1
    },
    "glasses_nerd": {
        "position": "face",
        "lines": [("◎◎", C.BLACK)],
        "y_offset": 0, "x_offset": -1
    },
    "sunglasses": {
        "position": "face",
        "lines": [("▀▀", C.BLACK)],
        "y_offset": 0, "x_offset": -1
    },
    "sunglasses_aviator": {
        "position": "face",
        "lines": [("◢◣", C.GOLD)],
        "y_offset": 0, "x_offset": -1
    },
    "monocle": {
        "position": "face",
        "lines": [("⧫", C.GOLD)],
        "y_offset": 0, "x_offset": 0
    },
    
    # ============ NECK ACCESSORIES ============
    "bowtie": {
        "position": "neck",
        "lines": [("<>", C.RED)],
        "y_offset": 1, "x_offset": -1
    },
    "bowtie_red": {
        "position": "neck",
        "lines": [("*", C.BRIGHT_RED)],
        "y_offset": 1, "x_offset": 0
    },
    "bowtie_fancy": {
        "position": "neck",
        "lines": [("◇", C.GOLD)],
        "y_offset": 1, "x_offset": 0
    },
    "bow_tie_blue": {
        "position": "neck",
        "lines": [("*", C.BRIGHT_BLUE)],
        "y_offset": 1, "x_offset": 0
    },
    "bow_tie_pink": {
        "position": "neck",
        "lines": [("<3", C.PINK)],
        "y_offset": 1, "x_offset": 0
    },
    "scarf_red": {
        "position": "neck",
        "lines": [("~≈", C.BRIGHT_RED)],
        "y_offset": 1, "x_offset": -1
    },
    "scarf_winter": {
        "position": "neck",
        "lines": [("≈≈", C.BRIGHT_CYAN)],
        "y_offset": 1, "x_offset": -1
    },
    "bandana": {
        "position": "neck",
        "lines": [("▼", C.BRIGHT_RED)],
        "y_offset": 1, "x_offset": 0
    },
    
    # ============ BACK/CAPE ACCESSORIES ============
    "cape": {
        "position": "back",
        "lines": [("\\", C.RED)],
        "y_offset": 1, "x_offset": 2
    },
    "cape_superhero": {
        "position": "back",
        "lines": [("\\", C.BRIGHT_RED)],
        "y_offset": 1, "x_offset": 2
    },
    "wings_fairy": {
        "position": "back",
        "lines": [("*)", C.BRIGHT_MAGENTA)],
        "y_offset": 0, "x_offset": 2
    },
    "backpack_tiny": {
        "position": "back",
        "lines": [("#", C.BROWN)],
        "y_offset": 1, "x_offset": 2
    },
    
    # ============ FLOATING ABOVE ============
    "halo_angel": {
        "position": "floating",
        "lines": [("o", C.BRIGHT_YELLOW)],
        "y_offset": -2, "x_offset": 0
    },
    "devil_horns": {
        "position": "above",
        "lines": [("}{", C.BRIGHT_RED)],
        "y_offset": -1, "x_offset": -1
    },
    "headphones": {
        "position": "above",
        "lines": [("#", C.BRIGHT_CYAN)],
        "y_offset": -1, "x_offset": 0
    },
}

# Keep COSMETIC_ART as an alias pointing to mini art for compatibility
COSMETIC_ART = MINI_COSMETIC_ART


class CosmeticsRenderer:
    """
    Renders cosmetic items on the mini duck in the playfield.
    Uses compact colored symbols that fit the small duck sprites.
    
    IMPORTANT: This renderer returns a grid of (char, color_func) tuples
    that can be used by the playfield renderer to apply colors correctly.
    """
    
    def __init__(self, terminal: Terminal = None):
        self.term = terminal or _term
    
    def render_duck_with_cosmetics(self, duck_art: List[str], equipped: Dict[str, str], duck_color: Callable = None) -> List[List[tuple]]:
        """
        Overlay cosmetics onto duck ASCII art.

        Returns a 2D grid of (char, color_func) tuples where color_func is None
        for normal duck characters and a color function for cosmetic characters.

        Args:
            duck_art: Base duck ASCII art lines
            equipped: Dict of slot -> item_id (e.g. {"head": "hat_red", "eyes": "sunglasses"})
            duck_color: Color function for duck body (defaults to terminal yellow)

        Returns:
            2D list of (char, color_func) tuples with same dimensions as duck_art
        """
        if not duck_art:
            return []

        # Use provided duck color or fall back to terminal yellow
        body_color = duck_color if duck_color is not None else self.term.yellow

        # Find duck dimensions - we will NOT change these
        duck_height = len(duck_art)
        duck_width = max(len(line) for line in duck_art) if duck_art else 0

        # Pad all lines to same width
        padded_art = [line.ljust(duck_width) for line in duck_art]

        # Convert to a grid of (char, color_func) tuples
        # Base duck characters get the duck's body color, spaces get None
        grid = [[(c, body_color if c != ' ' else None) for c in line] for line in padded_art]
        
        if not equipped:
            return grid
        
        # Find the duck's "head" position (where eyes are - usually line 1)
        # For mini ducks: line 0 is top of head, line 1 is face with eyes
        face_line = 1 if duck_height > 1 else 0
        
        # Find horizontal center of duck (where to place cosmetics)
        center_x = duck_width // 2
        
        # Apply each equipped cosmetic
        for slot, item_id in equipped.items():
            if item_id not in MINI_COSMETIC_ART:
                continue
            
            cosmetic = MINI_COSMETIC_ART[item_id]
            lines = cosmetic.get("lines", [])
            position = cosmetic.get("position", "above")
            x_off = cosmetic.get("x_offset", 0)
            
            # Determine target row based on position type
            if position in ("above", "floating"):
                # Place on top line of duck (row 0)
                target_y = 0
            elif position == "face":
                # Place on face line (row 1)
                target_y = face_line
            elif position == "neck":
                # Place below face (row 2 or bottom-1)
                target_y = min(2, duck_height - 1)
            elif position == "back":
                # Place on body (row 1-2, to the right side)
                target_y = face_line
            else:
                target_y = 0
            
            # For multi-line cosmetics, only use the first line (mini format)
            if lines:
                text, color_func = lines[0]
                base_x = center_x + x_off
                
                # Place characters on the grid
                for char_idx, char in enumerate(text):
                    col_x = base_x + char_idx
                    if 0 <= target_y < duck_height and 0 <= col_x < duck_width and char != ' ':
                        grid[target_y][col_x] = (char, color_func)
        
        return grid
    
    def grid_to_strings(self, grid: List[List[tuple]]) -> List[str]:
        """Convert a grid of (char, color_func) tuples to colored strings."""
        result = []
        for row in grid:
            line_chars = []
            for char, color_func in row:
                if color_func:
                    line_chars.append(color_func(char))
                else:
                    line_chars.append(char)
            result.append(''.join(line_chars))
        return result
    
    def get_cosmetic_preview(self, item_id: str) -> str:
        """Get a small preview of a cosmetic item for display in menus."""
        if item_id not in MINI_COSMETIC_ART:
            return "?"
        
        cosmetic = MINI_COSMETIC_ART[item_id]
        lines = cosmetic.get("lines", [])
        if lines:
            text, color_func = lines[0]
            if color_func:
                return color_func(text)
            return text
        return "?"
    
    def get_cosmetic_description(self, item_id: str) -> str:
        """Get a description of the cosmetic for display."""
        from world.shop import get_item
        item = get_item(item_id)
        if item:
            preview = self.get_cosmetic_preview(item_id)
            return f"{preview} {item.name}"
        return ""

