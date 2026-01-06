"""
Generic Menu Controller - Handles common menu navigation patterns.

Eliminates duplicated menu handling code across the game.
"""
from typing import Optional, Callable, Any, List, Dict
from dataclasses import dataclass, field
from enum import Enum, auto


class MenuResult(Enum):
    """Result of menu input handling."""
    NONE = auto()           # No action taken
    NAVIGATED = auto()      # Selection changed
    SELECTED = auto()       # Item was selected
    CANCELLED = auto()      # Menu was closed
    PAGE_CHANGED = auto()   # Page navigation occurred


@dataclass
class MenuAction:
    """Result of a menu action."""
    result: MenuResult
    selected_item: Optional[Any] = None
    selected_index: int = -1
    data: Optional[Any] = None


@dataclass
class MenuConfig:
    """Configuration for a menu."""
    title: str
    close_keys: List[str] = field(default_factory=lambda: ["KEY_ESCAPE"])
    select_keys: List[str] = field(default_factory=lambda: ["KEY_ENTER", " "])
    wrap_navigation: bool = True      # Wrap around at ends
    page_size: int = 0                # 0 = no pagination
    show_index: bool = False          # Show item numbers
    allow_disabled_select: bool = False  # Allow selecting disabled items


class MenuController:
    """
    Generic menu controller that handles navigation, selection, and rendering.
    
    Eliminates the need for separate _handle_X_input_direct methods for each menu.
    
    Usage:
        controller = MenuController(MenuConfig(title="My Menu"))
        controller.set_items([MenuItem(...), MenuItem(...)])
        
        # In input handler:
        result = controller.handle_input(key)
        if result.result == MenuResult.SELECTED:
            do_something(result.selected_item)
        elif result.result == MenuResult.CANCELLED:
            close_menu()
    """
    
    def __init__(self, config: MenuConfig):
        self.config = config
        self._items: List[Any] = []
        self._selected_index: int = 0
        self._current_page: int = 0
        self._is_open: bool = False
        
        # Callbacks
        self._on_select: Optional[Callable[[Any, int], None]] = None
        self._on_cancel: Optional[Callable[[], None]] = None
        self._on_navigate: Optional[Callable[[int], None]] = None
    
    @property
    def is_open(self) -> bool:
        return self._is_open
    
    @is_open.setter
    def is_open(self, value: bool):
        self._is_open = value
        if value and self._items:
            # Reset to first enabled item when opening
            self._select_first_enabled()
    
    @property
    def selected_index(self) -> int:
        return self._selected_index
    
    @property
    def selected_item(self) -> Optional[Any]:
        if 0 <= self._selected_index < len(self._items):
            return self._items[self._selected_index]
        return None
    
    @property
    def items(self) -> List[Any]:
        return self._items
    
    @property
    def visible_items(self) -> List[Any]:
        """Get items for current page (or all if no pagination)."""
        if self.config.page_size <= 0:
            return self._items
        
        start = self._current_page * self.config.page_size
        end = start + self.config.page_size
        return self._items[start:end]
    
    @property
    def total_pages(self) -> int:
        if self.config.page_size <= 0:
            return 1
        return max(1, (len(self._items) + self.config.page_size - 1) // self.config.page_size)
    
    @property
    def current_page(self) -> int:
        return self._current_page
    
    def set_items(self, items: List[Any]):
        """Set the menu items."""
        self._items = items
        self._selected_index = 0
        self._current_page = 0
        if items:
            self._select_first_enabled()
    
    def add_item(self, item: Any):
        """Add a single item."""
        self._items.append(item)
    
    def clear_items(self):
        """Clear all items."""
        self._items = []
        self._selected_index = 0
        self._current_page = 0
    
    def set_callbacks(self, 
                      on_select: Optional[Callable[[Any, int], None]] = None,
                      on_cancel: Optional[Callable[[], None]] = None,
                      on_navigate: Optional[Callable[[int], None]] = None):
        """Set callback functions."""
        self._on_select = on_select
        self._on_cancel = on_cancel
        self._on_navigate = on_navigate
    
    def handle_input(self, key) -> MenuAction:
        """
        Handle keyboard input for menu navigation.
        
        Args:
            key: Key object from blessed terminal (has .name for special keys)
        
        Returns:
            MenuAction with result and any selected data
        """
        if not self._is_open or not self._items:
            return MenuAction(MenuResult.NONE)
        
        key_str = str(key).lower() if not getattr(key, 'is_sequence', False) else ""
        key_name = getattr(key, 'name', "") or ""
        
        # Check for close/cancel
        for close_key in self.config.close_keys:
            if key_name == close_key or key_str == close_key.lower():
                self._is_open = False
                if self._on_cancel:
                    self._on_cancel()
                return MenuAction(MenuResult.CANCELLED)
        
        # Check for selection
        for select_key in self.config.select_keys:
            if key_name == select_key or key_str == select_key:
                item = self.selected_item
                if item is not None:
                    # Check if item is enabled (if it has that attribute)
                    is_enabled = getattr(item, 'enabled', True)
                    if is_enabled or self.config.allow_disabled_select:
                        if self._on_select:
                            self._on_select(item, self._selected_index)
                        return MenuAction(
                            MenuResult.SELECTED, 
                            selected_item=item,
                            selected_index=self._selected_index,
                            data=getattr(item, 'data', None)
                        )
                return MenuAction(MenuResult.NONE)
        
        # Navigation
        if key_name == "KEY_UP":
            return self._navigate(-1)
        elif key_name == "KEY_DOWN":
            return self._navigate(1)
        elif key_name == "KEY_PGUP" or key_name == "KEY_LEFT":
            return self._change_page(-1)
        elif key_name == "KEY_PGDN" or key_name == "KEY_RIGHT":
            return self._change_page(1)
        elif key_name == "KEY_HOME":
            return self._navigate_to(0)
        elif key_name == "KEY_END":
            return self._navigate_to(len(self._items) - 1)
        
        return MenuAction(MenuResult.NONE)
    
    def _navigate(self, direction: int) -> MenuAction:
        """Navigate up or down in the menu."""
        if not self._items:
            return MenuAction(MenuResult.NONE)
        
        old_index = self._selected_index
        new_index = self._selected_index + direction
        
        if self.config.wrap_navigation:
            new_index = new_index % len(self._items)
        else:
            new_index = max(0, min(len(self._items) - 1, new_index))
        
        if new_index != old_index:
            self._selected_index = new_index
            self._ensure_visible()
            if self._on_navigate:
                self._on_navigate(new_index)
            return MenuAction(MenuResult.NAVIGATED, selected_index=new_index)
        
        return MenuAction(MenuResult.NONE)
    
    def _navigate_to(self, index: int) -> MenuAction:
        """Navigate to a specific index."""
        if not self._items:
            return MenuAction(MenuResult.NONE)
        
        new_index = max(0, min(len(self._items) - 1, index))
        if new_index != self._selected_index:
            self._selected_index = new_index
            self._ensure_visible()
            if self._on_navigate:
                self._on_navigate(new_index)
            return MenuAction(MenuResult.NAVIGATED, selected_index=new_index)
        
        return MenuAction(MenuResult.NONE)
    
    def _change_page(self, direction: int) -> MenuAction:
        """Change page in paginated menus."""
        if self.config.page_size <= 0:
            return MenuAction(MenuResult.NONE)
        
        old_page = self._current_page
        new_page = self._current_page + direction
        
        if self.config.wrap_navigation:
            new_page = new_page % self.total_pages
        else:
            new_page = max(0, min(self.total_pages - 1, new_page))
        
        if new_page != old_page:
            self._current_page = new_page
            # Move selection to first item on new page
            self._selected_index = new_page * self.config.page_size
            return MenuAction(MenuResult.PAGE_CHANGED)
        
        return MenuAction(MenuResult.NONE)
    
    def _ensure_visible(self):
        """Ensure selected item is on current page."""
        if self.config.page_size <= 0:
            return
        
        target_page = self._selected_index // self.config.page_size
        if target_page != self._current_page:
            self._current_page = target_page
    
    def _select_first_enabled(self):
        """Select the first enabled item."""
        for i, item in enumerate(self._items):
            if getattr(item, 'enabled', True):
                self._selected_index = i
                return
        # If no enabled items, select first anyway
        self._selected_index = 0
    
    def select_by_id(self, item_id: str) -> bool:
        """Select item by its ID (if items have .id attribute)."""
        for i, item in enumerate(self._items):
            if getattr(item, 'id', None) == item_id:
                self._selected_index = i
                self._ensure_visible()
                return True
        return False
    
    def get_display_lines(self, width: int = 40, include_header: bool = True) -> List[str]:
        """
        Generate display lines for the menu.
        
        Args:
            width: Width of the menu display
            include_header: Whether to include title header
        
        Returns:
            List of formatted strings for display
        """
        lines = []
        
        if include_header:
            lines.append(f"═══ {self.config.title} ═══")
            lines.append("")
        
        visible = self.visible_items
        page_offset = self._current_page * self.config.page_size if self.config.page_size > 0 else 0
        
        for i, item in enumerate(visible):
            actual_index = page_offset + i
            is_selected = actual_index == self._selected_index
            is_enabled = getattr(item, 'enabled', True)
            
            # Get display text
            label = getattr(item, 'label', str(item))
            
            # Build line
            prefix = "→ " if is_selected else "  "
            if self.config.show_index:
                prefix = f"{actual_index + 1}. " + prefix
            
            line = f"{prefix}{label}"
            
            # Truncate if needed
            if len(line) > width:
                line = line[:width-3] + "..."
            
            # Style for disabled
            if not is_enabled:
                line = f"({line.strip()})"
            
            lines.append(line)
        
        # Pagination info
        if self.total_pages > 1:
            lines.append("")
            lines.append(f"Page {self._current_page + 1}/{self.total_pages} (←/→)")
        
        return lines


class ConfirmationDialog:
    """
    Simple yes/no confirmation dialog.
    
    Usage:
        dialog = ConfirmationDialog(
            title="Confirm Purchase",
            message="Buy Golden Hat for 1000 coins?",
            on_confirm=lambda: buy_item(),
            on_cancel=lambda: close_dialog()
        )
        
        # In input handler:
        result = dialog.handle_input(key)
    """
    
    def __init__(self, 
                 title: str,
                 message: str,
                 on_confirm: Optional[Callable[[], None]] = None,
                 on_cancel: Optional[Callable[[], None]] = None,
                 confirm_key: str = "y",
                 cancel_key: str = "n",
                 dangerous: bool = False):
        self.title = title
        self.message = message
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        self.confirm_key = confirm_key.lower()
        self.cancel_key = cancel_key.lower()
        self.dangerous = dangerous  # If true, require typing "yes"
        self._is_open = False
        self._confirmed = False
        self._cancelled = False
        self._input_buffer = ""  # For dangerous confirmations
    
    @property
    def is_open(self) -> bool:
        return self._is_open
    
    @is_open.setter
    def is_open(self, value: bool):
        self._is_open = value
        self._confirmed = False
        self._cancelled = False
        self._input_buffer = ""
    
    @property
    def was_confirmed(self) -> bool:
        return self._confirmed
    
    @property
    def was_cancelled(self) -> bool:
        return self._cancelled
    
    def handle_input(self, key) -> MenuResult:
        """Handle input for the confirmation dialog."""
        if not self._is_open:
            return MenuResult.NONE
        
        key_str = str(key).lower() if not getattr(key, 'is_sequence', False) else ""
        key_name = getattr(key, 'name', "") or ""
        
        # Always allow escape to cancel
        if key_name == "KEY_ESCAPE":
            self._is_open = False
            self._cancelled = True
            if self.on_cancel:
                self.on_cancel()
            return MenuResult.CANCELLED
        
        if self.dangerous:
            # Require typing "yes" for dangerous actions
            if key_name == "KEY_BACKSPACE":
                self._input_buffer = self._input_buffer[:-1]
                return MenuResult.NONE
            elif key_name == "KEY_ENTER":
                if self._input_buffer.lower() == "yes":
                    self._is_open = False
                    self._confirmed = True
                    if self.on_confirm:
                        self.on_confirm()
                    return MenuResult.SELECTED
                return MenuResult.NONE
            elif len(key_str) == 1 and key_str.isalpha():
                self._input_buffer += key_str
                return MenuResult.NONE
        else:
            # Simple Y/N
            if key_str == self.confirm_key:
                self._is_open = False
                self._confirmed = True
                if self.on_confirm:
                    self.on_confirm()
                return MenuResult.SELECTED
            elif key_str == self.cancel_key:
                self._is_open = False
                self._cancelled = True
                if self.on_cancel:
                    self.on_cancel()
                return MenuResult.CANCELLED
        
        return MenuResult.NONE
    
    def get_display_lines(self, width: int = 50) -> List[str]:
        """Generate display lines for the dialog."""
        lines = []
        lines.append("═" * width)
        lines.append(f"  {self.title}")
        lines.append("═" * width)
        lines.append("")
        
        # Word wrap message
        words = self.message.split()
        current_line = "  "
        for word in words:
            if len(current_line) + len(word) + 1 > width - 2:
                lines.append(current_line)
                current_line = "  " + word
            else:
                current_line += " " + word if current_line.strip() else "  " + word
        if current_line.strip():
            lines.append(current_line)
        
        lines.append("")
        
        if self.dangerous:
            lines.append(f"  Type 'yes' to confirm: {self._input_buffer}_")
        else:
            lines.append(f"  [{self.confirm_key.upper()}] Yes   [{self.cancel_key.upper()}] No")
        
        lines.append("")
        lines.append("═" * width)
        
        return lines


class NotificationManager:
    """
    Manages on-screen notifications with different types.
    
    Provides visual feedback with appropriate styling.
    """
    
    class NotificationType(Enum):
        INFO = "info"
        SUCCESS = "success"
        WARNING = "warning"
        ERROR = "error"
    
    @dataclass
    class Notification:
        message: str
        type: "NotificationManager.NotificationType"
        duration: float
        created_at: float
    
    def __init__(self):
        self._notifications: List[NotificationManager.Notification] = []
        self._max_notifications = 3
    
    def add(self, message: str, 
            notification_type: "NotificationType" = None,
            duration: float = 3.0):
        """Add a notification."""
        import time
        
        if notification_type is None:
            notification_type = self.NotificationType.INFO
        
        notification = self.Notification(
            message=message,
            type=notification_type,
            duration=duration,
            created_at=time.time()
        )
        
        self._notifications.append(notification)
        
        # Keep only most recent
        if len(self._notifications) > self._max_notifications:
            self._notifications = self._notifications[-self._max_notifications:]

    def show(self, message: str, 
             notification_type: str = "info",
             duration: float = 3.0):
        """
        Show a notification (convenience method).
        
        Args:
            message: The notification text
            notification_type: One of "info", "success", "warning", "error"
            duration: How long to show (seconds)
        """
        type_map = {
            "info": self.NotificationType.INFO,
            "success": self.NotificationType.SUCCESS,
            "warning": self.NotificationType.WARNING,
            "error": self.NotificationType.ERROR,
        }
        ntype = type_map.get(notification_type, self.NotificationType.INFO)
        self.add(message, ntype, duration)

    def info(self, message: str, duration: float = 3.0):
        """Add an info notification."""
        self.add(message, self.NotificationType.INFO, duration)
    
    def success(self, message: str, duration: float = 3.0):
        """Add a success notification."""
        self.add(message, self.NotificationType.SUCCESS, duration)
    
    def warning(self, message: str, duration: float = 4.0):
        """Add a warning notification."""
        self.add(message, self.NotificationType.WARNING, duration)
    
    def error(self, message: str, duration: float = 5.0):
        """Add an error notification."""
        self.add(message, self.NotificationType.ERROR, duration)
    
    def update(self):
        """Remove expired notifications."""
        import time
        current_time = time.time()
        self._notifications = [
            n for n in self._notifications
            if current_time - n.created_at < n.duration
        ]
    
    def get_active(self) -> List["Notification"]:
        """Get all active notifications."""
        self.update()
        return self._notifications
    
    def get_prefix(self, notification_type: "NotificationType") -> str:
        """Get display prefix for notification type."""
        prefixes = {
            self.NotificationType.INFO: "ℹ️ ",
            self.NotificationType.SUCCESS: "✓ ",
            self.NotificationType.WARNING: "⚠ ",
            self.NotificationType.ERROR: "✗ ",
        }
        return prefixes.get(notification_type, "")
    
    def clear(self):
        """Clear all notifications."""
        self._notifications = []


# Global notification manager
notification_manager = NotificationManager()
