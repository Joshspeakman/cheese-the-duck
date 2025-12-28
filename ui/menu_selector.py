"""
Reusable arrow-key menu selection system.
"""
from typing import List, Optional, Callable, Any, Dict
from dataclasses import dataclass


@dataclass
class MenuItem:
    """A single menu item."""
    id: str
    label: str
    description: str = ""
    enabled: bool = True
    data: Any = None


class MenuSelector:
    """
    Handles arrow-key navigation for menus.

    Usage:
        menu = MenuSelector("Crafting Menu")
        menu.set_items([
            MenuItem("1", "Wooden Sword", "Attack +5"),
            MenuItem("2", "Iron Shield", "Defense +3"),
        ])

        # In input handler:
        if menu.handle_key(key_name):
            if menu.was_confirmed():
                selected = menu.get_selected_item()
                # Do something with selected item
    """

    def __init__(self, title: str = "Menu", close_keys: List[str] = None):
        """
        Initialize the menu selector.

        Args:
            title: Display title for the menu
            close_keys: Keys that close the menu (lowercase)
        """
        self.title = title
        self.close_keys = close_keys or ['KEY_ESCAPE']
        self._items: List[MenuItem] = []
        self._selected_index = 0
        self._is_open = False
        self._was_confirmed = False
        self._was_cancelled = False

    def set_items(self, items: List[MenuItem]):
        """Set the menu items."""
        self._items = items
        self._selected_index = 0
        # Find first enabled item
        for i, item in enumerate(items):
            if item.enabled:
                self._selected_index = i
                break

    def add_item(self, item: MenuItem):
        """Add a single item to the menu."""
        self._items.append(item)

    def clear_items(self):
        """Clear all items."""
        self._items = []
        self._selected_index = 0

    def open(self):
        """Open the menu."""
        self._is_open = True
        self._was_confirmed = False
        self._was_cancelled = False
        self._selected_index = 0
        # Find first enabled item
        for i, item in enumerate(self._items):
            if item.enabled:
                self._selected_index = i
                break

    def close(self):
        """Close the menu."""
        self._is_open = False

    def is_open(self) -> bool:
        """Check if menu is open."""
        return self._is_open

    def handle_key(self, key_str: str, key_name: str = "") -> bool:
        """
        Handle a key press.

        Args:
            key_str: The string value of the key
            key_name: The name of special keys (KEY_UP, KEY_DOWN, etc.)

        Returns:
            True if the key was handled, False otherwise
        """
        if not self._is_open:
            return False

        self._was_confirmed = False
        self._was_cancelled = False

        # Check close keys
        if key_name in self.close_keys or key_str in self.close_keys:
            self._was_cancelled = True
            self._is_open = False
            return True

        # Navigate up
        if key_name == 'KEY_UP':
            self._move_selection(-1)
            return True

        # Navigate down
        if key_name == 'KEY_DOWN':
            self._move_selection(1)
            return True

        # Confirm selection
        if key_name == 'KEY_ENTER':
            if self._items and 0 <= self._selected_index < len(self._items):
                if self._items[self._selected_index].enabled:
                    self._was_confirmed = True
                    self._is_open = False
            return True

        return False

    def _move_selection(self, direction: int):
        """Move selection up (-1) or down (+1), skipping disabled items."""
        if not self._items:
            return

        original = self._selected_index
        new_index = self._selected_index

        # Try to find next enabled item in direction
        for _ in range(len(self._items)):
            new_index = (new_index + direction) % len(self._items)
            if self._items[new_index].enabled:
                self._selected_index = new_index
                return

        # No enabled items found, stay at original
        self._selected_index = original

    def get_selected_index(self) -> int:
        """Get the currently selected index."""
        return self._selected_index

    def set_selected_index(self, index: int):
        """Set the selected index."""
        if 0 <= index < len(self._items):
            self._selected_index = index

    def get_selected_item(self) -> Optional[MenuItem]:
        """Get the currently selected item."""
        if self._items and 0 <= self._selected_index < len(self._items):
            return self._items[self._selected_index]
        return None

    def get_items(self) -> List[MenuItem]:
        """Get all menu items."""
        return self._items

    def was_confirmed(self) -> bool:
        """Check if last action was a confirmation."""
        return self._was_confirmed

    def was_cancelled(self) -> bool:
        """Check if last action was a cancellation."""
        return self._was_cancelled

    def get_display_lines(self,
                          width: int = 40,
                          show_numbers: bool = True,
                          selected_prefix: str = "> ",
                          unselected_prefix: str = "  ",
                          disabled_suffix: str = " (locked)") -> List[str]:
        """
        Get formatted display lines for the menu.

        Args:
            width: Maximum width of lines
            show_numbers: Show number prefixes for items
            selected_prefix: Prefix for selected item
            unselected_prefix: Prefix for unselected items
            disabled_suffix: Suffix for disabled items

        Returns:
            List of formatted strings for display
        """
        lines = []
        lines.append(f"=== {self.title} ===")
        lines.append("")

        for i, item in enumerate(self._items):
            is_selected = (i == self._selected_index)
            prefix = selected_prefix if is_selected else unselected_prefix

            # Build the line
            if show_numbers:
                num = f"[{i+1}] "
            else:
                num = ""

            label = item.label
            if not item.enabled:
                label += disabled_suffix

            line = f"{prefix}{num}{label}"

            # Add description if selected and has one
            if is_selected and item.description:
                lines.append(line)
                lines.append(f"    {item.description}")
            else:
                lines.append(line)

        lines.append("")
        lines.append("[↑↓] Navigate  [Enter] Select  [ESC] Close")

        return lines
