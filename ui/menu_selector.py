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
    Handles arrow-key navigation for menus with pagination support.

    Usage:
        menu = MenuSelector("Crafting Menu", items_per_page=8)
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

    def __init__(self, title: str = "Menu", close_keys: List[str] = None, items_per_page: int = 8):
        """
        Initialize the menu selector.

        Args:
            title: Display title for the menu
            close_keys: Keys that close the menu (lowercase)
            items_per_page: Max items to show per page (0 = no pagination)
        """
        self.title = title
        self.close_keys = close_keys or ['KEY_ESCAPE']
        self.items_per_page = items_per_page
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

    @property
    def current_page(self) -> int:
        """Get current page number (0-indexed)."""
        if self.items_per_page <= 0 or not self._items:
            return 0
        return self._selected_index // self.items_per_page

    @property
    def total_pages(self) -> int:
        """Get total number of pages."""
        if self.items_per_page <= 0 or not self._items:
            return 1
        return max(1, (len(self._items) + self.items_per_page - 1) // self.items_per_page)

    @property
    def page_start_index(self) -> int:
        """Get the index of the first item on current page."""
        if self.items_per_page <= 0:
            return 0
        return self.current_page * self.items_per_page

    @property
    def page_end_index(self) -> int:
        """Get the index after the last item on current page."""
        if self.items_per_page <= 0:
            return len(self._items)
        return min(self.page_start_index + self.items_per_page, len(self._items))

    def get_display_lines(self,
                          width: int = 40,
                          show_numbers: bool = True,
                          selected_prefix: str = "> ",
                          unselected_prefix: str = "  ",
                          disabled_suffix: str = " (locked)",
                          max_items: int = 0) -> List[str]:
        """
        Get formatted display lines for the menu with pagination.

        Args:
            width: Maximum width of lines
            show_numbers: Show number prefixes for items
            selected_prefix: Prefix for selected item
            unselected_prefix: Prefix for unselected items
            disabled_suffix: Suffix for disabled items
            max_items: Override items_per_page (0 = use default)

        Returns:
            List of formatted strings for display
        """
        lines = []
        lines.append(f"=== {self.title} ===")
        
        # Determine pagination
        items_limit = max_items if max_items > 0 else self.items_per_page
        use_pagination = items_limit > 0 and len(self._items) > items_limit
        
        if use_pagination:
            # Show page info
            page = self.current_page + 1
            total = self.total_pages
            lines.append(f"Page {page}/{total}")
            start_idx = self.page_start_index
            end_idx = self.page_end_index
        else:
            lines.append("")
            start_idx = 0
            end_idx = len(self._items)

        for i in range(start_idx, end_idx):
            item = self._items[i]
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
        if use_pagination:
            lines.append("[^v] Navigate  [Enter] Select  [ESC] Close")
        else:
            lines.append("[^v] Navigate  [Enter] Select  [ESC] Close")

        return lines


# ==================== HIERARCHICAL MENU ====================

@dataclass
class MenuCategory:
    """A category containing menu items or subcategories."""
    id: str
    label: str
    items: List[MenuItem] = None
    icon: str = ""  # Optional ASCII icon


class HierarchicalMenuSelector:
    """
    A hierarchical menu system with categories and sub-items.
    Supports arrow-key navigation with breadcrumb trail.
    
    Usage:
        menu = HierarchicalMenuSelector("Main Menu")
        menu.set_categories([
            MenuCategory("care", "Duck Care", [
                MenuItem("feed", "Feed", "Give your duck some food"),
                MenuItem("play", "Play", "Have fun with your duck"),
            ]),
            MenuCategory("world", "World & Building", [...]),
        ])
        
        # In input handler:
        if menu.handle_key(key_str, key_name):
            if menu.was_action_selected():
                action = menu.get_selected_action()
                # Execute action
    """
    
    def __init__(self, title: str = "Main Menu"):
        self.title = title
        self._categories: List[MenuCategory] = []
        self._is_open = False
        
        # Navigation state
        self._current_level = 0  # 0 = categories, 1 = items
        self._category_index = 0
        self._item_index = 0
        
        # Action state
        self._selected_action: Optional[str] = None
        self._was_cancelled = False
    
    def set_categories(self, categories: List[MenuCategory]):
        """Set the menu categories."""
        self._categories = categories
        self._category_index = 0
        self._item_index = 0
        self._current_level = 0
    
    def open(self):
        """Open the menu at the top level."""
        self._is_open = True
        self._current_level = 0
        self._category_index = 0
        self._item_index = 0
        self._selected_action = None
        self._was_cancelled = False
    
    def close(self):
        """Close the menu."""
        self._is_open = False
        self._selected_action = None
    
    def is_open(self) -> bool:
        """Check if menu is open."""
        return self._is_open
    
    def handle_key(self, key_str: str, key_name: str = "") -> bool:
        """
        Handle a key press.
        
        Returns True if the key was handled.
        """
        if not self._is_open:
            return False
        
        self._selected_action = None
        self._was_cancelled = False
        
        # Escape: go back one level or close
        if key_name == 'KEY_ESCAPE' or key_str == '\x1b':
            if self._current_level > 0:
                self._current_level -= 1
                self._item_index = 0
            else:
                self._was_cancelled = True
                self._is_open = False
            return True
        
        # Tab: close menu
        if key_str == '\t':
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
        
        # Navigate left: go back
        if key_name == 'KEY_LEFT':
            if self._current_level > 0:
                self._current_level -= 1
                self._item_index = 0
            return True
        
        # Navigate right or Enter: drill down or select
        if key_name in ('KEY_RIGHT', 'KEY_ENTER'):
            return self._select_current()
        
        return False
    
    def _move_selection(self, direction: int):
        """Move selection up or down."""
        if self._current_level == 0:
            # Navigating categories
            if not self._categories:
                return
            self._category_index = (self._category_index + direction) % len(self._categories)
        else:
            # Navigating items within category
            category = self._get_current_category()
            if category and category.items:
                # Skip disabled items
                original = self._item_index
                for _ in range(len(category.items)):
                    self._item_index = (self._item_index + direction) % len(category.items)
                    if category.items[self._item_index].enabled:
                        return
                self._item_index = original
    
    def _select_current(self) -> bool:
        """Select current item - drill down or trigger action."""
        if self._current_level == 0:
            # Drill into category
            category = self._get_current_category()
            if category and category.items:
                self._current_level = 1
                self._item_index = 0
                # Find first enabled item
                for i, item in enumerate(category.items):
                    if item.enabled:
                        self._item_index = i
                        break
        else:
            # Select item - trigger action
            category = self._get_current_category()
            if category and category.items:
                item = category.items[self._item_index]
                if item.enabled:
                    self._selected_action = item.id
                    self._is_open = False
        return True
    
    def _get_current_category(self) -> Optional[MenuCategory]:
        """Get the currently selected category."""
        if self._categories and 0 <= self._category_index < len(self._categories):
            return self._categories[self._category_index]
        return None
    
    def was_action_selected(self) -> bool:
        """Check if an action was selected."""
        return self._selected_action is not None
    
    def was_cancelled(self) -> bool:
        """Check if menu was cancelled."""
        return self._was_cancelled
    
    def get_selected_action(self) -> Optional[str]:
        """Get the ID of the selected action."""
        return self._selected_action
    
    def get_breadcrumb(self) -> str:
        """Get breadcrumb trail for current location."""
        parts = [self.title]
        if self._current_level > 0:
            category = self._get_current_category()
            if category:
                parts.append(category.label)
        return " > ".join(parts)
    
    def get_display_lines(self, width: int = 50) -> List[str]:
        """Get formatted display lines for the menu."""
        lines = []
        
        # Header with breadcrumb
        breadcrumb = self.get_breadcrumb()
        lines.append("+" + "=" * (width - 2) + "+")
        lines.append(f"| {breadcrumb:<{width-4}} |")
        lines.append("+" + "-" * (width - 2) + "+")
        lines.append("")
        
        if self._current_level == 0:
            # Show categories
            for i, cat in enumerate(self._categories):
                is_selected = (i == self._category_index)
                prefix = ">" if is_selected else " "
                icon = f"{cat.icon} " if cat.icon else ""
                arrow = "  ->" if is_selected else ""
                lines.append(f"  {prefix} {icon}{cat.label}{arrow}")
        else:
            # Show items in current category
            category = self._get_current_category()
            if category and category.items:
                for i, item in enumerate(category.items):
                    is_selected = (i == self._item_index)
                    prefix = ">" if is_selected else " "
                    status = "" if item.enabled else " (locked)"
                    lines.append(f"  {prefix} {item.label}{status}")
                    
                    # Show description for selected item
                    if is_selected and item.description:
                        lines.append(f"      {item.description}")
        
        lines.append("")
        
        # Navigation hints
        if self._current_level == 0:
            lines.append("  [^v] Navigate  [Enter/->] Open  [TAB] Close")
        else:
            lines.append("  [^v] Navigate  [Enter] Select  [<-/ESC] Back")
        
        lines.append("+" + "=" * (width - 2) + "+")
        
        return lines


@dataclass
class MasterMenuItem:
    """Item in the master menu tree."""
    id: str
    label: str
    action: str = None  # Action ID to execute, or None if has children
    children: list = None  # List of MasterMenuItem or callable that returns list
    completed: bool = False  # Whether item shows * indicator
    enabled: bool = True  # Whether item can be selected


class MasterMenuPanel:
    """
    Persistent hierarchical menu panel for the side panel.
    
    Supports unlimited depth via navigation stack, scroll-follow behavior,
    and visual indicators (> selected, -> has submenu, * completed).
    """
    
    def __init__(self, game=None):
        """Initialize the master menu panel."""
        self.game = game
        self._menu_tree = []  # Root menu items (set by set_menu_tree)
        self._navigation_stack = []  # List of (menu_items, selected_index) for each level
        self._current_items = []  # Current level's items
        self._selected_index = 0
        self._scroll_offset = 0
        self._parent_label = None  # Label to show as header when in submenu
        
    def set_menu_tree(self, tree: list):
        """Set the root menu tree."""
        self._menu_tree = tree
        self._current_items = tree
        self._selected_index = 0
        self._scroll_offset = 0
        self._navigation_stack = []
        self._parent_label = None
        
    def _get_current_items(self) -> list:
        """Get current menu items, resolving dynamic children if needed."""
        items = []
        for item in self._current_items:
            if callable(item):
                # Dynamic item generator
                items.extend(item(self.game) if self.game else item(None))
            elif isinstance(item, MasterMenuItem):
                items.append(item)
            elif isinstance(item, dict):
                # Convert dict to MasterMenuItem
                children = item.get('children')
                if callable(children):
                    children = children(self.game) if self.game else children(None)
                items.append(MasterMenuItem(
                    id=item.get('id', ''),
                    label=item.get('label', ''),
                    action=item.get('action'),
                    children=children,
                    completed=item.get('completed', False),
                    enabled=item.get('enabled', True)
                ))
        return items
    
    def navigate(self, direction: int):
        """Navigate up (direction=-1) or down (direction=1)."""
        items = self._get_current_items()
        if not items:
            return
            
        new_index = self._selected_index + direction
        if 0 <= new_index < len(items):
            self._selected_index = new_index
            
    def select(self) -> str:
        """
        Select current item. Returns action ID if leaf, or None if expanded submenu.
        """
        items = self._get_current_items()
        if not items or self._selected_index >= len(items):
            return None
            
        item = items[self._selected_index]
        if not item.enabled:
            return None
            
        # Check if item has children (submenu)
        children = item.children
        if callable(children):
            children = children(self.game) if self.game else children(None)
            
        if children:
            # Push current state to stack and navigate into submenu
            self._navigation_stack.append((self._current_items, self._selected_index, self._parent_label))
            self._current_items = children
            self._parent_label = item.label
            self._selected_index = 0
            self._scroll_offset = 0
            return None
        else:
            # Leaf item - return action
            return item.action or item.id
            
    def back(self) -> bool:
        """Go back one level. Returns True if went back, False if at root."""
        if self._navigation_stack:
            self._current_items, self._selected_index, self._parent_label = self._navigation_stack.pop()
            self._scroll_offset = 0
            return True
        return False

    def navigate_to_item(self, *path: str) -> bool:
        """
        Navigate to a specific menu item by ID path.

        Args:
            *path: Variable number of item IDs forming the path (e.g., "social", "inventory")

        Returns:
            True if navigation succeeded, False otherwise
        """
        # Reset to root first
        self._current_items = self._menu_tree
        self._selected_index = 0
        self._scroll_offset = 0
        self._navigation_stack = []
        self._parent_label = None

        for item_id in path:
            items = self._get_current_items()
            found = False
            for i, item in enumerate(items):
                if item.id == item_id:
                    self._selected_index = i
                    # If this is not the last item in path, drill into it
                    if item_id != path[-1]:
                        children = item.children
                        if callable(children):
                            children = children(self.game) if self.game else children(None)
                        if children:
                            self._navigation_stack.append((self._current_items, self._selected_index, self._parent_label))
                            self._current_items = children
                            self._parent_label = item.label
                            self._selected_index = 0
                            self._scroll_offset = 0
                    found = True
                    break
            if not found:
                return False
        return True

    def is_at_root(self) -> bool:
        """Check if at root level."""
        return len(self._navigation_stack) == 0
        
    def get_depth(self) -> int:
        """Get current navigation depth (0 = root)."""
        return len(self._navigation_stack)
        
    def get_render_lines(self, width: int, max_lines: int) -> list:
        """
        Render the menu to a list of strings (Pixel Art / 8-bit style).
        
        Args:
            width: Available width for each line
            max_lines: Maximum number of lines to return
            
        Returns:
            List of strings, each exactly 'width' characters
        """
        lines = []
        items = self._get_current_items()
        
        if not items:
            empty_msg = "No items"
            lines.append(empty_msg.center(width))
            return lines
            
        # Pixel art style header
        header_lines = 0
        if self._parent_label:
            # 8-bit style header: ▄▀▄ LABEL ▄▀▄
            header_text = self._parent_label.upper()
            if len(header_text) > width - 8:
                header_text = header_text[:width-11] + "..."
            header = f"▄▀▄ {header_text} ▄▀▄"
            lines.append(header.center(width))
            header_lines = 1
        else:
            # Root level - show MENU title in same style
            header = "▄▀▄ MENU ▄▀▄"
            lines.append(header.center(width))
            header_lines = 1
            
        # Calculate visible items with scroll-follow
        # For selected items, we need 3 lines (top bar, content, bottom bar)
        # But we'll simplify: selected gets highlight bar above
        visible_lines = max_lines - header_lines - 2  # Reserve for scroll indicators
        if visible_lines < 1:
            visible_lines = 1
            
        # Ensure selected item is visible (scroll-follow)
        if self._selected_index < self._scroll_offset:
            self._scroll_offset = self._selected_index
        elif self._selected_index >= self._scroll_offset + visible_lines:
            self._scroll_offset = self._selected_index - visible_lines + 1
            
        # Clamp scroll offset
        max_scroll = max(0, len(items) - visible_lines)
        self._scroll_offset = max(0, min(self._scroll_offset, max_scroll))
        
        # Show "^ more" indicator (pixel style)
        if self._scroll_offset > 0:
            indicator = "▲▲▲ MORE ▲▲▲"
            lines.append(indicator.center(width))
        else:
            lines.append(" " * width)
            
        # Render visible items
        end_index = min(self._scroll_offset + visible_lines, len(items))
        for i in range(self._scroll_offset, end_index):
            item = items[i]
            is_selected = (i == self._selected_index)
            
            # Check for submenu indicator
            children = item.children
            if callable(children):
                has_submenu = True
            else:
                has_submenu = bool(children)
            
            # Completion indicator
            completed = item.completed
            if callable(completed):
                completed = completed(self.game) if self.game else False
            
            # Enabled indicator
            if not item.enabled:
                label = f"[{item.label}]"  # Brackets for locked
            else:
                label = item.label
            
            if is_selected:
                # Selected: ▓ ► Label       → ▓  (pixel block style)
                submenu_arrow = "→" if has_submenu else " "
                completion_mark = "♦" if completed else " "
                
                # Calculate inner content width (▓ + space + ► + content + ▓)
                inner_width = width - 4  # "▓ " and " ▓"
                content = f"► {label}"
                suffix = f"{submenu_arrow}{completion_mark}"
                
                # Pad content
                content_space = inner_width - len(suffix)
                if len(content) > content_space:
                    content = content[:content_space-2] + ".."
                content = content.ljust(content_space)
                
                line = f"▓ {content}{suffix} ▓"
            else:
                # Non-selected: regular with symbols
                submenu_arrow = "→" if has_submenu else " "
                if completed:
                    prefix = "♦"  # Diamond for completed
                else:
                    prefix = " "
                
                # Calculate available space for label
                # Format: "  ♦ Label        → "
                overhead = 6  # prefix(1) + spaces + arrow(1) + padding
                max_label_len = width - overhead
                if len(label) > max_label_len:
                    label = label[:max_label_len-2] + ".."
                label = label.ljust(max_label_len)
                
                line = f"  {prefix} {label}{submenu_arrow} "
            
            # Ensure exact width
            if len(line) < width:
                line = line + " " * (width - len(line))
            elif len(line) > width:
                line = line[:width]
                
            lines.append(line)
            
        # Fill remaining visible lines if needed
        rendered_items = end_index - self._scroll_offset
        for _ in range(rendered_items, visible_lines):
            lines.append(" " * width)
            
        # Show "v more" indicator (pixel style)
        if end_index < len(items):
            indicator = "▼▼▼ MORE ▼▼▼"
            lines.append(indicator.center(width))
        else:
            lines.append(" " * width)
            
        return lines
        
    def handle_key(self, key) -> str:
        """
        Handle a keypress. Returns action ID if action triggered, None otherwise.
        
        Args:
            key: Key object from blessed terminal
            
        Returns:
            Action ID string if action should execute, None otherwise
        """
        key_name = getattr(key, 'name', '') or ''
        
        if key_name == 'KEY_UP':
            self.navigate(-1)
            return None
        elif key_name == 'KEY_DOWN':
            self.navigate(1)
            return None
        elif key_name == 'KEY_RIGHT' or key_name == 'KEY_ENTER':
            return self.select()
        elif key_name == 'KEY_LEFT' or key_name == 'KEY_BACKSPACE':
            self.back()
            return None
            
        return None
