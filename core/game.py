"""
Main game controller - manages game loop and state.
Enhanced with progression, daily rewards, collectibles, and addiction mechanics.
"""
import time
import random
from typing import Optional, List, Tuple, Dict
from datetime import datetime

from blessed import Terminal

from config import FPS, TICK_RATE
from core.clock import GameClock, game_clock
from core.persistence import SaveManager, save_manager, create_new_save
from core.progression import ProgressionSystem, Reward, RewardType, COLLECTIBLES
from duck.duck import Duck
from duck.behavior_ai import BehaviorAI
from dialogue.conversation import ConversationSystem, conversation
from world.events import EventSystem, event_system
from world.items import Inventory, get_random_item, get_item_info
from world.goals import GoalSystem, goal_system
from world.achievements import AchievementSystem, achievement_system
from world.home import DuckHome, duck_home
from world.atmosphere import AtmosphereManager, atmosphere, WeatherType
from world.exploration import ExplorationSystem, exploration, BiomeType
from world.materials import MaterialInventory, material_inventory, MATERIALS
from world.crafting import CraftingSystem, crafting, RECIPES
from world.building import BuildingSystem, building, BLUEPRINTS
from world.shop import get_item as get_shop_item
from world.minigames import (
    MiniGameSystem, BreadCatchGame, BugChaseGame, MemoryMatchGame, DuckRaceGame,
    MiniGameType, MiniGameResult
)
from world.dreams import DreamSystem, dreams
from world.facts import get_random_fact, get_birthday_info, get_birthday_message, get_mood_response
from world.item_interactions import (
    execute_interaction, find_matching_item, get_item_interaction,
    ITEM_INTERACTIONS, InteractionResult
)
from world.interaction_controller import InteractionController, InteractionSource
from dialogue.diary import DuckDiary, duck_diary, DiaryEntryType
from audio.sound import sound_engine, duck_sounds, get_music_context, MusicContext
from ui.renderer import Renderer
from ui.animations import animation_controller
from ui.input_handler import InputHandler, GameAction
from ui.menu_selector import MenuSelector, MenuItem

# New feature imports - Phase 2 systems
from world.scrapbook import Scrapbook, scrapbook
from world.fishing import FishingMinigame, fishing_system, FishingSpot
from world.garden import Garden, garden
from world.treasure import TreasureHunter, treasure_hunter
from world.challenges import ChallengeSystem, challenge_system
from world.friends import FriendsSystem, friends_system
from world.quests import QuestSystem, quest_system, QUESTS
from world.festivals import FestivalSystem, festival_system
from world.collectibles import CollectiblesSystem, collectibles_system
from world.decorations import DecorationsSystem, decorations_system
from world.secrets import SecretsSystem, secrets_system
from world.weather_activities import WeatherActivitiesSystem, weather_activities_system
from world.trading import TradingSystem, trading_system
from world.fortune import FortuneSystem, fortune_system

from duck.outfits import OutfitManager, outfit_manager
from duck.tricks import TricksSystem, tricks_system
from duck.titles import TitlesSystem, titles_system
from duck.aging import AgingSystem, aging_system
from duck.personality_extended import ExtendedPersonalitySystem, extended_personality
from duck.seasonal_clothing import SeasonalClothingSystem, seasonal_clothing

from core.prestige import PrestigeSystem, prestige_system
from core.save_slots import SaveSlotsSystem, save_slots_system

from dialogue.mood_dialogue import MoodDialogueSystem, mood_dialogue_system
from dialogue.diary_enhanced import EnhancedDiarySystem, enhanced_diary
from dialogue.contextual_dialogue import ContextualDialogueSystem, contextual_dialogue

from audio.ambient import AmbientSoundSystem, ambient_sound_system
from audio.sound_effects import SoundEffectSystem, sound_effects

# DuckBrain - Seaman-style memory and personality system
from dialogue.duck_brain import DuckBrain

from ui.statistics import StatisticsSystem, statistics_system
from ui.day_night import DayNightSystem, day_night_system
from ui.event_animations import (
    EventAnimator, create_event_animator, ANIMATED_EVENTS,
    EventAnimationState, BreezeAnimator
)
from ui.badges import BadgesSystem, badges_system
from ui.mood_visuals import MoodVisualEffects, mood_visual_effects
from ui.reactions import DuckReactionController, init_reaction_controller
from ui.menu_selector import HierarchicalMenuSelector, MasterMenuPanel
from ui.menu_structure import build_main_menu_categories, build_master_menu_tree, MENU_ACTIONS

# Settings and menu systems
from core.settings import settings_manager, get_settings, load_settings, save_settings
from core.menu_controller import MenuController, ConfirmationDialog, notification_manager
from ui.settings_menu import SettingsMenu, settings_menu

from enum import Enum, auto


class InteractionPhase(Enum):
    """Phases for animated duck-to-target interactions."""
    IDLE = auto()           # No interaction in progress
    MOVING_TO_TARGET = auto()  # Duck is waddling to item/friend/location
    INTERACTING = auto()    # Duck has arrived and is playing interaction animation
    RETURNING = auto()      # Duck is returning to original position (optional)


class Game:
    """
    Main game controller.

    Manages the game loop, state transitions, and coordinates
    between duck, UI, and persistence systems.
    """

    def __init__(self):
        self.terminal = Terminal()
        self.renderer = Renderer(self.terminal)
        self.input_handler = InputHandler(self.terminal)
        self.reaction_controller = init_reaction_controller(self.renderer)
        self.clock = game_clock
        self.save_manager = save_manager

        self.duck: Optional[Duck] = None
        self.behavior_ai: Optional[BehaviorAI] = None
        self.conversation: ConversationSystem = conversation
        self.events: EventSystem = event_system
        self.inventory: Inventory = Inventory()
        self.goals: GoalSystem = goal_system
        self.achievements: AchievementSystem = achievement_system
        self.progression: ProgressionSystem = ProgressionSystem()
        self.home: DuckHome = DuckHome()

        # Shop and habitat system
        from world.habitat import Habitat
        self.habitat: Habitat = Habitat()

        # Unified interaction controller - handles all duck-to-item interactions
        self.interaction_controller: InteractionController = InteractionController()

        # Atmosphere and diary systems (Animal Crossing style)
        self.atmosphere: AtmosphereManager = atmosphere
        self.diary: DuckDiary = duck_diary

        # Exploration, crafting, and building systems
        self.exploration: ExplorationSystem = exploration
        self.materials: MaterialInventory = material_inventory
        self.crafting: CraftingSystem = crafting
        self.building: BuildingSystem = building

        self._running = False
        self._state = "init"  # init, title, playing, paused, daily_rewards
        self._last_tick = 0.0
        self._last_save = 0.0
        self._last_event_check = 0.0
        self._last_progression_check = 0.0
        self._last_atmosphere_check = 0.0
        self._last_craft_check = 0.0
        self._last_build_check = 0.0
        self._session_start = time.time()
        self._session_feeds = 0  # Track for bread_obsessed secret
        self._ecstatic_start = None  # Track for zen_master secret
        self._perfect_care_start = None  # Track for perfectionist secret
        self._weather_seen = set()  # Track for weather_watcher secret
        self._statistics = {}
        self._pending_offline_summary = None
        self._pending_daily_rewards = []
        self._pending_messages = []  # Messages to show after load (e.g., cleanup notifications)
        self._sound_enabled = True
        self._show_goals = False
        self._reset_confirmation = False  # Flag for reset game confirmation

        # Arrow-key menu selectors with pagination
        self._crafting_menu = MenuSelector("CRAFTING", close_keys=['KEY_ESCAPE', 'c'], items_per_page=8)
        self._building_menu = MenuSelector("BUILDING", close_keys=['KEY_ESCAPE', 'r'], items_per_page=8)
        self._areas_menu = MenuSelector("AREAS", close_keys=['KEY_ESCAPE', 'a'], items_per_page=8)
        self._use_menu = MenuSelector("USE ITEM", close_keys=['KEY_ESCAPE', 'u'], items_per_page=8)
        self._minigames_menu = MenuSelector("MINI-GAMES", close_keys=['KEY_ESCAPE', 'j'], items_per_page=8)
        self._quests_menu = MenuSelector("QUESTS", close_keys=['KEY_ESCAPE', 'o'], items_per_page=8)
        self._weather_menu = MenuSelector("WEATHER ACTIVITIES", close_keys=['KEY_ESCAPE', 'w'], items_per_page=8)

        # Main hierarchical menu (TAB to open) - DEPRECATED, replaced by master_menu
        self._main_menu = HierarchicalMenuSelector("Main Menu")
        self._main_menu.set_categories(build_main_menu_categories())
        self._main_menu_open = False
        
        # NEW: Master menu panel (always visible in side panel)
        self.master_menu = MasterMenuPanel(self)
        self.master_menu.set_menu_tree(build_master_menu_tree())

        # Backwards compatibility flags (computed from menu state)
        self._crafting_menu_open = False  # Flag for crafting menu
        self._building_menu_open = False  # Flag for building menu
        self._areas_menu_open = False     # Flag for areas menu
        self._use_menu_open = False       # Flag for use/interact menu
        self._use_menu_items = []         # List of items with interactions
        self._use_menu_selected = 0       # Currently selected item in use menu
        self._minigames_menu_open = False # Flag for minigames menu
        self._minigames_menu_selected = 0 # Currently selected minigame
        self._quests_menu_open = False    # Flag for quests menu
        self._weather_menu_open = False   # Flag for weather activities menu
        
        # Treasure hunting menu
        self._treasure_menu_open = False  # Flag for treasure hunting menu
        self._treasure_menu_selected = 0  # Currently selected location/action
        self._treasure_menu_items = []    # Menu items for treasure hunting
        self._treasure_digging = False    # Currently digging for treasure
        self._treasure_dig_progress = 0   # Dig animation progress
        
        # Scrapbook menu
        self._scrapbook_menu_open = False  # Flag for scrapbook menu
        self._scrapbook_page = 0           # Current scrapbook page
        self._scrapbook_selected = 0       # Currently selected photo on page
        
        # Tricks menu pagination
        self._tricks_menu_open = False     # Flag for tricks menu
        self._tricks_menu_page = 0         # Current page of tricks
        
        # Titles menu pagination  
        self._titles_menu_open = False     # Flag for titles menu
        self._titles_menu_page = 0         # Current page of titles
        
        # Decorations menu pagination
        self._decorations_menu_open = False  # Flag for decorations menu
        self._decorations_menu_page = 0      # Current page of decorations
        
        # Collectibles menu pagination
        self._collectibles_menu_open = False  # Flag for collectibles menu
        self._collectibles_menu_page = 0      # Current page of collectibles
        
        # Secrets book menu
        self._secrets_menu_open = False       # Flag for secrets book menu
        self._secrets_menu_page = 0           # Current page of secrets
        
        # Garden menu
        self._garden_menu_open = False        # Flag for garden menu
        self._garden_selected_plot = 0        # Currently selected garden plot
        
        # Prestige menu
        self._prestige_menu_open = False      # Flag for prestige menu
        
        # Save slots menu  
        self._save_slots_menu_open = False    # Flag for save slots menu
        self._save_slots_selected = 0         # Currently selected slot
        
        # Trading menu
        self._trading_menu_open = False       # Flag for trading menu
        self._trading_selected = 0            # Currently selected trader
        
        # Enhanced diary menu
        self._enhanced_diary_open = False       # Flag for enhanced diary menu
        self._enhanced_diary_tab = "overview"   # Current tab: overview, emotions, photos, dreams, life
        self._enhanced_diary_page = 0           # Current page within tab
        
        # Title screen menu state
        self._title_menu_index = 0        # Currently selected title menu option
        self._title_update_status = ""    # Update status message for title screen
        self._title_checking_updates = False  # Currently checking for updates
        self._title_confirm_new_game = False  # Confirming new game over existing save
        
        # Game updater
        from core.updater import game_updater, GAME_VERSION, UpdateStatus
        self._game_updater = game_updater
        self._game_version = GAME_VERSION
        self._update_available_info = None  # Stores UpdateInfo when update is found
        self._update_in_progress = False    # Currently downloading/applying update
        
        # Festival activities menu
        self._festival_menu_open = False   # Flag for festival menu
        self._festival_menu_selected = 0   # Currently selected activity
        self._festival_menu_items = []     # Menu items for festivals
        self._festival_doing_activity = False  # Currently doing festival activity
        self._festival_activity_progress = 0   # Activity progress
        
        # Settings menu
        self._settings_menu_open = False  # Flag for settings menu
        self._settings_menu = settings_menu
        self._settings_menu.set_sound_engine(sound_engine)
        
        # Terminal selector (title screen inline)
        from core.settings import SystemSettings, settings_manager
        self._terminal_options = SystemSettings.detect_available_terminals()
        # Find current selection index from saved preference
        current_pref = settings_manager.settings.system.preferred_terminal
        self._terminal_selection_index = 0
        for i, (cmd, name) in enumerate(self._terminal_options):
            if cmd == current_pref:
                self._terminal_selection_index = i
                break
        
        # Confirmation dialog
        self._confirmation_dialog = None  # Active confirmation dialog
        
        # Hidden debug menu (accessed with backtick `)
        self._debug_menu_open = False
        self._debug_menu_selected = 0
        self._debug_submenu = None  # Current debug submenu (weather, events, etc.)
        self._debug_submenu_selected = 0
        self._debug_submenu_page = 0  # Current page for paginated submenus
        self._debug_items_per_page = 10  # Items per page in debug submenu

        # Mini-games system
        self.minigames: MiniGameSystem = MiniGameSystem()
        self._active_minigame = None      # Currently playing minigame instance
        self._minigame_type = None        # Type of current minigame
        self._minigame_last_update = 0.0  # Last update time for minigames
        self._boombox_playing = False     # Track if boombox music is playing

        # Dreams system
        self.dreams: DreamSystem = DreamSystem()
        self._dream_active = False        # Currently showing a dream
        self._dream_result = None         # Current dream result
        self._dream_scene_index = 0       # Current scene in dream
        self._dream_scene_timer = 0.0     # Timer for scene transitions
        
        # ============== NEW FEATURE SYSTEMS ==============
        # Scrapbook & Memory System
        self.scrapbook: Scrapbook = scrapbook
        
        # Activity Systems
        self.fishing: FishingMinigame = fishing_system
        self.garden: Garden = garden
        self.treasure: TreasureHunter = treasure_hunter
        
        # Social & Progression Systems
        self.challenges: ChallengeSystem = challenge_system
        self.friends: FriendsSystem = friends_system
        self.quests: QuestSystem = quest_system
        self.festivals: FestivalSystem = festival_system
        self.prestige: PrestigeSystem = prestige_system
        
        # Collection & Customization Systems
        self.collectibles: CollectiblesSystem = collectibles_system
        self.tricks: TricksSystem = tricks_system
        self.decorations: DecorationsSystem = decorations_system
        self.titles: TitlesSystem = titles_system
        self.outfits: OutfitManager = outfit_manager
        self.seasonal_clothing: SeasonalClothingSystem = seasonal_clothing
        
        # World & Environment Systems
        self.secrets: SecretsSystem = secrets_system
        self.weather_activities: WeatherActivitiesSystem = weather_activities_system
        self.trading: TradingSystem = trading_system
        self.fortune: FortuneSystem = fortune_system
        
        # Duck Extended Systems
        self.aging: AgingSystem = aging_system
        self.extended_personality: ExtendedPersonalitySystem = extended_personality
        
        # UI & Display Systems
        self.statistics: StatisticsSystem = statistics_system
        self.day_night: DayNightSystem = day_night_system
        self.badges: BadgesSystem = badges_system
        self.mood_visuals: MoodVisualEffects = mood_visual_effects
        
        # Audio Systems
        self.ambient: AmbientSoundSystem = ambient_sound_system
        self.sound_effects: SoundEffectSystem = sound_effects
        
        # Enhanced Dialogue Systems
        self.mood_dialogue: MoodDialogueSystem = mood_dialogue_system
        self.enhanced_diary: EnhancedDiarySystem = enhanced_diary
        self.contextual_dialogue: ContextualDialogueSystem = contextual_dialogue
        
        # DuckBrain - Seaman-style memory and personality system
        self.duck_brain: Optional[DuckBrain] = None
        
        # Random comment tracking
        self._last_random_comment_time = 0.0
        self._random_comment_interval = 45.0  # Seconds between random comments
        self._pending_visitor_comment = None
        self._pending_visitor_comment_time = 0.0
        self._pending_weather_comment = None
        self._pending_weather_comment_time = 0.0
        self._last_known_weather = None  # Track weather changes
        
        # Save Management
        self.save_slots: SaveSlotsSystem = save_slots_system
        # ============== END NEW FEATURE SYSTEMS ==============
        
        # Animated interaction state machine
        self._interaction_phase = InteractionPhase.IDLE
        self._interaction_target_item = None  # Item being interacted with
        self._interaction_target_friend = None  # Friend being visited
        self._interaction_target_pos = None  # Target position (x, y) in playfield coords
        self._interaction_pending_result = None  # InteractionResult waiting for duck arrival
        
        # Item interaction animation state
        self._item_interaction_active = False
        self._item_interaction_item = None
        self._item_interaction_frames = []
        self._item_interaction_frame_idx = 0
        self._item_interaction_start = 0.0
        self._item_interaction_duration = 0.0
        self._item_interaction_message = ""
        self._item_interaction_frame_time = 0.5
        
        # Event animation state - for animated random events
        self._event_animators: List[EventAnimator] = []  # Active event animations
        self._event_animation_last_update = 0.0  # Last update time
        
        # Exploration and building activity states
        self._duck_exploring = False      # Duck is actively exploring an area
        self._exploring_start_time = 0.0  # When exploring started
        self._exploring_duration = 5.0    # How long the duck explores (seconds)
        self._duck_building = False       # Duck is actively building
        self._building_start_time = 0.0   # When building started
        self._duck_traveling = False      # Duck is traveling to new area
        self._travel_start_time = 0.0     # When travel started
        self._travel_duration = 2.0       # How long to travel (seconds)
        self._travel_destination = None   # Where duck is traveling to

        # Interaction cooldowns (in seconds)
        self._interaction_cooldowns = {
            "feed": 30,      # Can feed every 30 seconds
            "play": 20,      # Can play every 20 seconds
            "clean": 45,     # Can clean every 45 seconds
            "pet": 10,       # Can pet every 10 seconds
            "sleep": 60,     # Can sleep every 60 seconds
        }
        self._last_interaction_time = {}  # Tracks when each interaction was last used

    def start(self):
        """Start the game."""
        self._running = True

        # Load user settings first
        load_settings()
        self._apply_settings()

        # Always show title screen first with music
        self._state = "title"
        self._start_title_music()

        self._game_loop()

    def _apply_settings(self):
        """Apply current settings to game systems."""
        settings = get_settings()
        
        # Apply audio settings
        if hasattr(sound_engine, 'set_master_volume'):
            sound_engine.set_master_volume(settings.audio.master_volume)
        sound_engine.set_enabled(settings.audio.sfx_enabled)
        if hasattr(sound_engine, 'set_music_enabled'):
            sound_engine.set_music_enabled(settings.audio.music_enabled)
        
        # Apply display settings to renderer (if available)
        if hasattr(self.renderer, 'set_show_particles'):
            self.renderer.set_show_particles(settings.display.show_particles)
        
        # Register callback for live setting changes
        settings_manager.register_change_callback(self._on_setting_changed)

    def _on_setting_changed(self, key: str, value):
        """Handle real-time setting changes."""
        if key.startswith("audio."):
            self._apply_settings()

    def _start_title_music(self):
        """Start playing title screen music."""
        sound_engine.set_enabled(True)
        # Try to play WAV file first
        if 'title' in sound_engine._available_wavs:
            sound_engine.play_wav_music('title', loop=True)
        # If no title WAV, just stay silent (no beeping fallback)

    def _game_loop(self):
        """Main game loop."""
        frame_time = 1.0 / FPS

        with self.terminal.fullscreen(), self.terminal.cbreak(), self.terminal.hidden_cursor():
            while self._running:
                loop_start = time.time()

                # Process input
                self._process_input()

                # Update game state
                if self._state == "playing" and self.duck:
                    self._update()

                # Render
                self._render()

                # Cap frame rate with adaptive sleep for CachyOS/Arch compatibility
                elapsed = time.time() - loop_start
                remaining = frame_time - elapsed
                if remaining > 0.002:  # Only sleep if >2ms remaining
                    # Sleep slightly less to avoid overshooting on systems with coarse timers
                    time.sleep(remaining * 0.9)
                # Spin-wait for the final milliseconds for precise timing
                while time.time() - loop_start < frame_time:
                    pass

    def _process_input(self):
        """Process keyboard input."""
        # Reduced timeout from 50ms to 10ms for more responsive input on Arch/CachyOS
        key = self.terminal.inkey(timeout=0.01)

        if not key:
            return

        # Handle talk mode specially
        if self.renderer.is_talking():
            self._handle_talk_input(key)
            return

        # Handle shop navigation
        if self.renderer.is_shop_open():
            self._handle_shop_input(key)
            return

        # Handle menu navigation (same priority as shop)
        if self._crafting_menu_open:
            self._handle_crafting_input_direct(key)
            return
        if self._building_menu_open:
            self._handle_building_input_direct(key)
            return
        if self._areas_menu_open:
            self._handle_areas_input_direct(key)
            return
        if self._use_menu_open:
            self._handle_use_input_direct(key)
            return
        if self._minigames_menu_open:
            self._handle_minigames_input_direct(key)
            return
        if self._quests_menu_open:
            self._handle_quests_input_direct(key)
            return
        if self._weather_menu_open:
            self._handle_weather_input_direct(key)
            return
        if self._treasure_menu_open:
            self._handle_treasure_input(key)
            return
        if self._scrapbook_menu_open:
            self._handle_scrapbook_input(key)
            return
        if self._tricks_menu_open:
            self._handle_tricks_input(key)
            return
        if self._titles_menu_open:
            self._handle_titles_input(key)
            return
        if self._decorations_menu_open:
            self._handle_decorations_input(key)
            return
        if self._collectibles_menu_open:
            self._handle_collectibles_input(key)
            return
        if self._secrets_menu_open:
            self._handle_secrets_input(key)
            return
        if self._garden_menu_open:
            self._handle_garden_input(key)
            return
        if self._prestige_menu_open:
            self._handle_prestige_input(key)
            return
        if self._save_slots_menu_open:
            self._handle_save_slots_input(key)
            return
        if self._trading_menu_open:
            self._handle_trading_input(key)
            return
        if self._enhanced_diary_open:
            self._handle_enhanced_diary_input(key)
            return
        if self._festival_menu_open:
            self._handle_festival_input(key)
            return
        if self._main_menu_open:
            self._handle_main_menu_input(key)
            return
        if self._debug_menu_open:
            self._handle_debug_input(key)
            return
        if self._settings_menu_open:
            self._handle_settings_input(key)
            return
        if self._confirmation_dialog and self._confirmation_dialog.is_open:
            self._handle_confirmation_input(key)
            return

        # Handle inventory item selection and pagination
        if self.renderer.is_inventory_open() and self.duck:
            key_str = str(key)
            key_name = getattr(key, 'name', '') or ''
            # Close inventory with backspace or ESC
            if key_name == 'KEY_BACKSPACE' or key_name == 'KEY_ESCAPE':
                self.renderer.toggle_inventory()
                return
            # Page navigation with < and >
            if key_str == ',' or key_str == '<':
                self.renderer.inventory_change_page(-1)
                return
            if key_str == '.' or key_str == '>':
                self.renderer.inventory_change_page(1)
                return
            if key_str.isdigit() and key_str != '0':
                self._use_inventory_item(int(key_str) - 1)  # Convert to 0-based index
                return
        
        # Handle master menu navigation (arrow keys, enter, backspace)
        # Only when no other overlay/menu is open
        if self._state == "playing" and not self._has_open_overlay():
            key_name = getattr(key, 'name', '') or ''
            if key_name in ('KEY_UP', 'KEY_DOWN', 'KEY_LEFT', 'KEY_RIGHT', 'KEY_ENTER', 'KEY_BACKSPACE'):
                action_id = self.master_menu.handle_key(key)
                if action_id:
                    self._execute_menu_action(action_id)
                return

        action = self.input_handler.process_key(key)
        self._handle_action(action, key)

    def _handle_talk_input(self, key):
        """Handle input while in talk mode."""
        # ESC closes talk mode (Backspace is used for text editing)
        if key.name == "KEY_ESCAPE":
            self.renderer.toggle_talk()
            return

        if key.name == "KEY_ENTER":
            # Submit message
            message = self.renderer.get_talk_buffer()
            self.renderer.toggle_talk()  # Close talk overlay first
            if message.strip():
                self._process_talk(message)
            else:
                # Empty message - duck responds to silence
                self.renderer.show_message("*stares expectantly* ...Well? I'm listening.", duration=3.0, category="duck")
            return

        if key.name == "KEY_BACKSPACE":
            self.renderer.backspace_talk()
            return

        # Add printable character
        if key and not key.is_sequence and len(str(key)) == 1:
            self.renderer.add_talk_char(str(key))

    def _handle_shop_input(self, key):
        """Handle input while in shop mode."""
        key_str = str(key).lower()

        # Close shop with ESC, Backspace, or B
        if key.name == "KEY_ESCAPE" or key.name == "KEY_BACKSPACE" or key_str == 'b':
            self.renderer.toggle_shop()
            return

        # Navigate categories
        if key.name == "KEY_LEFT":
            self.renderer.shop_navigate_category(-1)
            return
        if key.name == "KEY_RIGHT":
            self.renderer.shop_navigate_category(1)
            return

        # Navigate items
        if key.name == "KEY_UP":
            self.renderer.shop_navigate_item(-1)
            return
        if key.name == "KEY_DOWN":
            self.renderer.shop_navigate_item(1)
            return

        # Purchase item with ENTER or SPACE
        if key.name == "KEY_ENTER" or key_str == ' ':
            self._purchase_selected_item()
            return
        
        # Toggle item visibility with T
        if key_str == 't':
            self._toggle_selected_item_visibility()
            return

        # Equip/Unequip cosmetic with E
        if key_str == 'e':
            self._toggle_cosmetic_equip()
            return

    def _handle_crafting_input_direct(self, key):
        """Handle crafting menu input directly (like shop)."""
        key_str = str(key).lower() if not key.is_sequence else str(key)

        # Navigate up
        if key.name == "KEY_UP":
            idx = self._crafting_menu.get_selected_index()
            if idx > 0:
                self._crafting_menu.set_selected_index(idx - 1)
                self._update_crafting_menu_display()
            return
        # Navigate down
        if key.name == "KEY_DOWN":
            idx = self._crafting_menu.get_selected_index()
            items = self._crafting_menu.get_items()
            if idx < len(items) - 1:
                self._crafting_menu.set_selected_index(idx + 1)
                self._update_crafting_menu_display()
            return
        # Select with Enter or Space (like shop)
        if key.name == "KEY_ENTER" or key_str == ' ':
            selected = self._crafting_menu.get_selected_item()
            if selected and selected.data and selected.enabled:
                recipe = selected.data
                result = self.crafting.start_crafting(recipe.id, self.materials)
                self._crafting_menu_open = False
                self.renderer.show_message(result["message"], duration=3.0, category="action")
            return
        # Close with ESC, Backspace, or C
        if key.name == "KEY_ESCAPE" or key.name == "KEY_BACKSPACE" or key_str == 'c':
            self._crafting_menu_open = False
            self.renderer.dismiss_message()
            return

    def _handle_building_input_direct(self, key):
        """Handle building menu input directly (like shop)."""
        key_str = str(key).lower() if not key.is_sequence else str(key)

        if key.name == "KEY_UP":
            idx = self._building_menu.get_selected_index()
            if idx > 0:
                self._building_menu.set_selected_index(idx - 1)
                self._update_building_menu_display()
            return
        if key.name == "KEY_DOWN":
            idx = self._building_menu.get_selected_index()
            items = self._building_menu.get_items()
            if idx < len(items) - 1:
                self._building_menu.set_selected_index(idx + 1)
                self._update_building_menu_display()
            return
        if key.name == "KEY_ENTER" or key_str == ' ':
            selected = self._building_menu.get_selected_item()
            if selected and selected.data and selected.enabled:
                bp = selected.data
                result = self.building.start_building(bp.id, self.materials, player_level=self.progression.level)
                self._building_menu_open = False
                if result.get("success"):
                    self._start_building_animation(bp)
                else:
                    self.renderer.show_message(result["message"], duration=3.0, category="action")
            return
        if key.name == "KEY_ESCAPE" or key.name == "KEY_BACKSPACE" or key_str == 'r':
            self._building_menu_open = False
            self.renderer.dismiss_message()
            return

    def _handle_areas_input_direct(self, key):
        """Handle areas menu input directly (like shop)."""
        key_str = str(key).lower() if not key.is_sequence else str(key)

        if key.name == "KEY_UP":
            idx = self._areas_menu.get_selected_index()
            if idx > 0:
                self._areas_menu.set_selected_index(idx - 1)
                self._update_areas_menu_display()
            return
        if key.name == "KEY_DOWN":
            idx = self._areas_menu.get_selected_index()
            items = self._areas_menu.get_items()
            if idx < len(items) - 1:
                self._areas_menu.set_selected_index(idx + 1)
                self._update_areas_menu_display()
            return
        if key.name == "KEY_ENTER" or key_str == ' ':
            selected = self._areas_menu.get_selected_item()
            if selected and selected.data:
                area = selected.data
                self._areas_menu_open = False
                self.renderer.dismiss_message()
                self._start_travel_to_area(area)
            return
        if key.name == "KEY_ESCAPE" or key.name == "KEY_BACKSPACE" or key_str == 'a':
            self._areas_menu_open = False
            self.renderer.dismiss_message()
            return

    def _handle_use_input_direct(self, key):
        """Handle use menu input directly (like shop)."""
        key_str = str(key).lower() if not key.is_sequence else str(key)

        if key.name == "KEY_UP":
            idx = self._use_menu.get_selected_index()
            if idx > 0:
                self._use_menu.set_selected_index(idx - 1)
                self._update_use_menu_display()
            return
        if key.name == "KEY_DOWN":
            idx = self._use_menu.get_selected_index()
            items = self._use_menu.get_items()
            if idx < len(items) - 1:
                self._use_menu.set_selected_index(idx + 1)
                self._update_use_menu_display()
            return
        if key.name == "KEY_ENTER" or key_str == ' ':
            selected = self._use_menu.get_selected_item()
            if selected and selected.data:
                item_id, item = selected.data
                self._use_menu_open = False
                self.renderer.dismiss_message()
                self._execute_item_interaction(item_id)
            return
        if key.name == "KEY_ESCAPE" or key.name == "KEY_BACKSPACE" or key_str == 'u':
            self._use_menu_open = False
            self.renderer.dismiss_message()
            return

    def _handle_minigames_input_direct(self, key):
        """Handle minigames menu input directly (like shop)."""
        key_str = str(key).lower() if not key.is_sequence else str(key)

        if key.name == "KEY_UP":
            idx = self._minigames_menu.get_selected_index()
            if idx > 0:
                self._minigames_menu.set_selected_index(idx - 1)
                self._update_minigames_menu_display()
            return
        if key.name == "KEY_DOWN":
            idx = self._minigames_menu.get_selected_index()
            items = self._minigames_menu.get_items()
            if idx < len(items) - 1:
                self._minigames_menu.set_selected_index(idx + 1)
                self._update_minigames_menu_display()
            return
        if key.name == "KEY_ENTER" or key_str == ' ':
            selected = self._minigames_menu.get_selected_item()
            if selected and selected.data and selected.enabled:
                self._minigames_menu_open = False
                self.renderer.dismiss_message()
                self._start_minigame(selected.data["id"])
            return
        if key.name == "KEY_ESCAPE" or key.name == "KEY_BACKSPACE" or key_str == 'j':
            self._minigames_menu_open = False
            self.renderer.dismiss_message()
            return

    def _handle_quests_input_direct(self, key):
        """Handle quests menu input directly (like shop)."""
        key_str = str(key).lower() if not key.is_sequence else str(key)

        if key.name == "KEY_UP":
            idx = self._quests_menu.get_selected_index()
            if idx > 0:
                self._quests_menu.set_selected_index(idx - 1)
                self._update_quests_menu_display()
            return
        if key.name == "KEY_DOWN":
            idx = self._quests_menu.get_selected_index()
            items = self._quests_menu.get_items()
            if idx < len(items) - 1:
                self._quests_menu.set_selected_index(idx + 1)
                self._update_quests_menu_display()
            return
        if key.name == "KEY_ENTER" or key_str == ' ':
            selected = self._quests_menu.get_selected_item()
            if selected and selected.data and selected.enabled:
                quest_id = selected.data.get("quest_id")
                if quest_id:
                    self._quests_menu_open = False
                    self.renderer.dismiss_message()
                    self._start_selected_quest(quest_id)
            return
        if key.name == "KEY_ESCAPE" or key.name == "KEY_BACKSPACE" or key_str == 'o':
            self._quests_menu_open = False
            self.renderer.dismiss_message()
            return

    def _handle_main_menu_input(self, key):
        """Handle input while main menu is open."""
        key_str = str(key).lower() if not key.is_sequence else str(key)
        key_name = key.name if hasattr(key, 'name') else ""

        # Let the hierarchical menu handle the key
        handled = self._main_menu.handle_key(key_str, key_name)

        if self._main_menu.was_action_selected():
            # An action was selected - execute it
            action_id = self._main_menu.get_selected_action()
            self._main_menu_open = False
            self.renderer.dismiss_message()
            self._execute_menu_action(action_id)
            return

        if self._main_menu.was_cancelled():
            # Menu was closed
            self._main_menu_open = False
            self.renderer.dismiss_message()
            return

        if handled:
            # Navigation occurred - update display
            self._update_main_menu_display()

    def _update_main_menu_display(self):
        """Update the main menu display."""
        lines = self._main_menu.get_display_lines(width=50)
        self.renderer.show_overlay("\n".join(lines), duration=0)

    def _execute_menu_action(self, action_id: str):
        """Execute a menu action by its ID."""
        # Handle dynamic minigame actions (minigame_bread_catch, etc.)
        if action_id.startswith("minigame_"):
            game_id = action_id.replace("minigame_", "")
            self._start_minigame(game_id)
            return

        # Handle dynamic travel actions (travel_Home Pond, etc.)
        if action_id.startswith("travel_"):
            area_name = action_id.replace("travel_", "")
            self._travel_to_area(area_name)
            return

        # Handle dynamic craft actions (craft_recipe_id, etc.)
        if action_id.startswith("craft_"):
            recipe_id = action_id.replace("craft_", "")
            self._craft_item(recipe_id)
            return

        # Handle dynamic build actions (build_structure_id, etc.)
        if action_id.startswith("build_"):
            blueprint_id = action_id.replace("build_", "")
            self._start_building(blueprint_id)
            return

        # Handle dynamic trick actions (trick_trick_id, etc.)
        if action_id.startswith("trick_"):
            trick_id = action_id.replace("trick_", "")
            self._perform_trick(trick_id)
            return

        # Handle dynamic garden plant actions (garden_plant_seed_id, etc.)
        if action_id.startswith("garden_plant_"):
            seed_id = action_id.replace("garden_plant_", "")
            self._plant_seed(seed_id)
            return

        # Handle dynamic decoration actions (decor_decoration_id, etc.)
        if action_id.startswith("decor_"):
            decor_id = action_id.replace("decor_", "")
            self._place_decoration(decor_id)
            return

        # Handle dynamic collectible actions (col_collectible_id, etc.)
        if action_id.startswith("col_"):
            col_id = action_id.replace("col_", "")
            self._view_collectible(col_id)
            return

        # Handle dynamic title actions (title_title_id, etc.)
        if action_id.startswith("title_"):
            title_id = action_id.replace("title_", "")
            self._equip_title(title_id)
            return

        # Handle radio actions (radio_quack_fm, radio_stop, etc.)
        if action_id.startswith("radio_"):
            radio_action = action_id.replace("radio_", "")
            self._handle_radio_action(radio_action)
            return

        if action_id not in MENU_ACTIONS:
            self.renderer.show_message(f"Unknown action: {action_id}")
            return

        method_name = MENU_ACTIONS[action_id]

        # Special handling for interaction actions
        if method_name.startswith("_perform_interaction_"):
            interaction_type = method_name.replace("_perform_interaction_", "")
            self._close_all_overlays()
            self._perform_interaction(interaction_type)
            return

        # Special handling for toggle methods
        if method_name == "_toggle_stats":
            self._close_all_menus()
            self.renderer.toggle_stats()
            return
        if method_name == "_toggle_inventory":
            self._close_all_menus()
            self.renderer.toggle_inventory()
            return
        if method_name == "_toggle_goals":
            self._close_all_menus()
            self._show_goals = not self._show_goals
            if self._show_goals:
                self._goals_page = 0  # Reset to first page
                self._show_goals_overlay()
            else:
                self.renderer.dismiss_overlay()
            return
        if method_name == "_toggle_shop":
            self._close_all_menus()
            self.renderer.toggle_shop()
            return
        if method_name == "_toggle_help":
            self._close_all_menus()
            self.renderer.toggle_help()
            return
        if method_name == "_toggle_sound":
            self._toggle_sound_action()
            return
        if method_name == "_toggle_music":
            self._toggle_music_action()
            return
        if method_name == "_start_talk_mode":
            self._close_all_menus()
            self.renderer.toggle_talk()
            return
        if method_name == "_return_to_title":
            self._return_to_title()
            return
        if method_name == "_show_terminal_selector":
            self._close_all_menus()
            self._show_terminal_selector()
            return
        if method_name == "_open_settings_menu":
            self._close_all_menus()
            self._open_settings_menu()
            return

        # Standard method call
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            method()
        else:
            self.renderer.show_message(f"Action not implemented: {method_name}")

    def _toggle_sound_action(self):
        """Toggle sound effects."""
        from audio.sound import sound_engine
        sound_engine.toggle()  # toggle() returns new enabled state
        status = "ON" if sound_engine.enabled else "OFF"
        self.renderer.show_message(f"Sound: {status}")

    def _toggle_music_action(self):
        """Toggle music."""
        from audio.sound import sound_engine
        sound_engine.toggle_music_mute()  # toggle_music_mute() returns new muted state
        status = "OFF" if sound_engine.music_muted else "ON"
        self.renderer.show_message(f"Music: {status}")

    def _handle_radio_action(self, action: str):
        """Handle radio menu actions."""
        import threading
        from audio.sound import sound_engine
        from audio.radio import StationID
        
        if action == "stop":
            # Run in thread to avoid blocking
            threading.Thread(target=sound_engine.stop_radio, daemon=True).start()
            self.renderer.show_message("Radio stopped")
            return
        
        # Try to play the station
        try:
            station_id = StationID(action)
            radio = sound_engine.get_radio()
            
            # Check if DJ Duck is available
            if station_id == StationID.DJ_DUCK_LIVE and not radio.is_dj_duck_live():
                self.renderer.show_message(f"DJ Duck: {radio.get_dj_duck_status()}")
                return
            
            # Get station name before async call
            from audio.radio import STATIONS
            station = STATIONS.get(station_id)
            station_name = station.name if station else "Radio"
            
            # Change station in background thread to avoid blocking
            def change_async():
                sound_engine.change_radio_station(station_id)
            
            threading.Thread(target=change_async, daemon=True).start()
            self.renderer.show_message(f"Tuning to {station_name}...")
            
        except ValueError:
            self.renderer.show_message(f"Unknown station: {action}")

    def _show_radio_menu(self):
        """Show the radio station selection menu."""
        # Radio is accessed via the master menu submenu, 
        # this is just a fallback for direct access
        self._close_all_menus()
        self.renderer.show_message("Use TAB menu > Other > Radio")

    def _purchase_selected_item(self):
        """Purchase the currently selected shop item."""
        item = self.renderer.get_selected_shop_item()
        if not item:
            return

        # Check level requirement
        if self.progression.level < item.unlock_level:
            self.renderer.show_message(f"Unlock at level {item.unlock_level}!")
            return

        # Try to purchase
        if self.habitat.purchase_item(item.id):
            self.renderer.show_message(f"Purchased {item.name}! x")
            # Award XP for shopping
            new_level = self.progression.add_xp(5)
            if new_level:
                self._on_level_up(new_level)
        else:
            if self.habitat.owns_item(item.id):
                self.renderer.show_message("Already owned!")
            else:
                self.renderer.show_message(f"Need ${item.cost - self.habitat.currency} more!")

    def _toggle_selected_item_visibility(self):
        """Toggle the visibility of the currently selected shop item."""
        item = self.renderer.get_selected_shop_item()
        if not item:
            return
        
        # Can only toggle owned items
        if not self.habitat.owns_item(item.id):
            self.renderer.show_message("Buy the item first!")
            return
        
        # Toggle the item
        result = self.habitat.toggle_item_visibility(item.id)
        
        if result == 'placed':
            self.renderer.show_message(f"{item.name} is now visible!")
        elif result == 'stored':
            self.renderer.show_message(f"{item.name} is now hidden!")
        elif result == 'cosmetic':
            self.renderer.show_message("Use [E] to equip/unequip cosmetics!")
        else:
            self.renderer.show_message("Can't toggle this item!")

    def _toggle_cosmetic_equip(self):
        """Toggle equip/unequip of the currently selected cosmetic item."""
        item = self.renderer.get_selected_shop_item()
        if not item:
            return
        
        # Can only equip owned cosmetics
        if not self.habitat.owns_item(item.id):
            self.renderer.show_message("Buy the item first!")
            return
        
        # Check if it's a cosmetic
        from world.shop import ItemCategory
        if item.category != ItemCategory.COSMETIC:
            self.renderer.show_message("Not a cosmetic item!")
            return
        
        # Check if currently equipped
        is_equipped = item.id in self.habitat.equipped_cosmetics.values()
        
        if is_equipped:
            # Find the slot and unequip
            slot_to_remove = None
            for slot, item_id in self.habitat.equipped_cosmetics.items():
                if item_id == item.id:
                    slot_to_remove = slot
                    break
            if slot_to_remove:
                self.habitat.unequip_cosmetic(slot_to_remove)
                self.renderer.show_message(f"Unequipped {item.name}!")
        else:
            # Equip the cosmetic
            self.habitat.equip_cosmetic(item.id)
            self.renderer.show_message(f"Equipped {item.name}!")

    def _use_inventory_item(self, index: int):
        """Use an inventory item by index."""
        if not self.duck:
            return

        item_id = self.renderer.get_inventory_item(index)
        if not item_id:
            self.renderer.show_message("No item at that slot!")
            return

        # Use the item
        result = self.inventory.use_item(item_id, self.duck)
        if result:
            item = result["item"]

            # Show item use message
            self.renderer.show_message(result["message"], duration=4.0, category="duck")

            # Play appropriate sound
            if item.item_type.value == "food":
                duck_sounds.eat()
            elif item.item_type.value == "toy":
                duck_sounds.play()
            else:
                duck_sounds.quack("happy")

            # Show closeup based on reaction
            reaction = result.get("reaction", "happy")
            if reaction in ["ecstatic", "transcendent", "crying_happy"]:
                self.renderer.show_effect("sparkle", 2.0)
            self.renderer.show_closeup(reaction, 2.5)

            # Record in memory
            self.duck.memory.add_interaction(
                f"used_{item.item_type.value}",
                item.name,
                emotional_value=item.mood_bonus
            )

            # Update goals
            self.goals.update_progress("use_item", 1)
            if item.item_type.value == "food":
                self.goals.update_progress("feed", 1)

            # Check for item-related achievements
            if item.rarity == "legendary":
                self._unlock_achievement("used_legendary")
        else:
            self.renderer.show_message("Can't use that item!")

    def _process_talk(self, message: str):
        """Process a talk message and get duck response."""
        if not self.duck:
            return

        # Check for item interaction commands first
        owned_items = self.habitat.owned_items
        matching_item = find_matching_item(message, owned_items)
        
        if matching_item:
            # This is an item interaction command!
            self._execute_item_interaction(matching_item)
            return

        # Get memory context for enhanced dialogue
        memory_context = self._get_memory_context_for_dialogue()
        
        # Get response from conversation system (with memory context if LLM available)
        response = self.conversation.process_player_input(
            self.duck, 
            message,
            memory_context=memory_context
        )

        # Record in memory
        self.duck.memory.add_interaction("talk", message, emotional_value=5)
        self.duck.memory.total_interactions += 1

        # Update statistics
        self._statistics["conversations"] = self._statistics.get("conversations", 0) + 1

        # Show response (longer duration for conversations)
        self.renderer.show_message(response, duration=8.0, category="duck")

        # Play quacks for each syllable in the duck's response
        mood = self.duck.get_mood().state.value
        duck_sounds.quack_for_text(response, mood)

        # Check goals
        self.goals.update_progress("talk", 1)

    def _get_item_playfield_position(self, item_id: str) -> Optional[Tuple[int, int]]:
        """Get the playfield position of a placed item."""
        if not hasattr(self, 'habitat') or not self.habitat:
            return None
        
        for placed_item in self.habitat.placed_items:
            if placed_item.item_id == item_id:
                # Convert habitat grid coords (0-20, 0-12) to playfield coords
                # The playfield uses the duck_pos field dimensions
                field_width = self.renderer.duck_pos.field_width
                field_height = self.renderer.duck_pos.field_height
                item_x = int(placed_item.x * field_width / 20)
                item_y = int(placed_item.y * field_height / 12)
                return (item_x, item_y)
        return None

    def _execute_item_interaction(self, item_id: str, source: InteractionSource = InteractionSource.PLAYER_COMMAND):
        """Execute an interaction with a placed item using the unified controller."""
        if not self.duck:
            return

        # Items only exist at Home Pond - check current location
        current_location = None
        if hasattr(self, 'exploration') and self.exploration and self.exploration.current_area:
            current_location = self.exploration.current_area.name

        if current_location is not None and current_location != "Home Pond":
            self.renderer.show_message("*quack* My stuff is back at home!", duration=2.0, category="duck")
            return

        # Check if controller is busy
        if self.interaction_controller.is_interacting():
            return

        # For AI/proximity sources, don't interrupt ongoing AI actions (like sleeping)
        if source != InteractionSource.PLAYER_COMMAND:
            current_time = time.time()
            if hasattr(self, 'behavior_ai') and self.behavior_ai._current_action:
                if current_time < self.behavior_ai._action_end_time:
                    return  # Don't interrupt ongoing AI action
            # Also check duck's current_action
            if self.duck.current_action:
                if hasattr(self.duck, '_action_end_time') and current_time < self.duck._action_end_time:
                    return  # Duck still busy

        # Check legacy interaction phase (for visitor/event interactions that still use it)
        # Reset if stuck for too long (safety measure)
        if self._interaction_phase != InteractionPhase.IDLE:
            # Allow item interactions to proceed anyway since unified controller handles them
            # Only block if we're in MOVING_TO_TARGET for a friend/visitor
            if self._interaction_target_friend is not None:
                return

        # Build duck state for contextual messages
        duck_state = {
            "energy": getattr(self.duck.needs, "energy", 100),
            "hunger": getattr(self.duck.needs, "hunger", 100),
            "fun": getattr(self.duck.needs, "fun", 100),
            "cleanliness": getattr(self.duck.needs, "cleanliness", 100),
            "social": getattr(self.duck.needs, "social", 100),
            "mood": self.duck.get_mood().state.value,
        }

        # Use the unified controller - it handles movement, animation, and effects
        success, message = self.interaction_controller.request_interaction(
            item_id=item_id,
            source=source,
            duck_state=duck_state
        )

        # Only show error messages for player-initiated interactions, not AI
        # This prevents immersion-breaking "I'm busy" spam from autonomous behavior
        if not success and source == InteractionSource.PLAYER_COMMAND:
            self.renderer.show_message(message, category="duck")

    def _on_interaction_effects_applied(self, item_id: str, result: InteractionResult):
        """Callback when interaction controller finishes and applies effects."""
        # Always record interaction for behavior AI cooldown, even if result is missing
        if self.behavior_ai:
            self.behavior_ai.record_item_interaction()

        if not self.duck or not result:
            return

        # Get item info
        item = get_shop_item(item_id)
        item_name = item.name if item else item_id

        # Record in memory
        self.duck.memory.add_interaction(f"interacted_{item_id}", item_name, emotional_value=10)

        # Play sound effect
        if result.sound:
            if result.sound == "splash":
                duck_sounds.eat()  # Use eat sound for now
            elif result.sound == "bounce":
                duck_sounds.play()
            elif result.sound == "music":
                duck_sounds.quack("happy")
            else:
                duck_sounds.play()
        else:
            duck_sounds.play()

        # Update goals
        self.goals.update_progress("interact_item", 1)

        # Check achievements
        self._statistics["item_interactions"] = self._statistics.get("item_interactions", 0) + 1
        if self._statistics["item_interactions"] >= 10:
            self._unlock_achievement("playful_duck")
        if self._statistics["item_interactions"] >= 50:
            self._unlock_achievement("item_master")

    def _on_arrived_at_item(self, data: dict):
        """Callback when duck arrives at item position."""
        item_id = data.get("item_id")
        result = data.get("result")
        
        if not item_id or not result:
            self._interaction_phase = InteractionPhase.IDLE
            return
        
        # Trigger item's animation (bounce/shake)
        self._trigger_item_animation(item_id)
        
        # Now play the interaction animation
        self._interaction_phase = InteractionPhase.INTERACTING
        self._complete_item_interaction(item_id, result)

    def _trigger_item_animation(self, item_id: str):
        """Trigger the placed item's animation when duck arrives."""
        if not hasattr(self, 'habitat') or not self.habitat:
            return
        
        for placed_item in self.habitat.placed_items:
            if placed_item.item_id == item_id:
                # Choose animation type based on item
                if "ball" in item_id or "toy" in item_id:
                    placed_item.start_animation("bounce")
                elif "pool" in item_id or "water" in item_id:
                    placed_item.start_animation("shake")
                else:
                    placed_item.start_animation("bounce")
                break

    def _complete_item_interaction(self, item_id: str, result: InteractionResult):
        """Complete the item interaction after duck arrives."""
        # Get item info for the message
        item = get_shop_item(item_id)
        item_name = item.name if item else item_id
        
        # Start the interaction animation
        self._start_item_interaction_animation(item_id, result)
        
        # Apply effects to duck needs
        for need, change in result.effects.items():
            if hasattr(self.duck.needs, need):
                current = getattr(self.duck.needs, need)
                setattr(self.duck.needs, need, min(100, max(0, current + change)))
        
        # Record in memory
        self.duck.memory.add_interaction(f"interacted_{item_id}", item_name, emotional_value=10)
        
        # Play sound effect
        if result.sound:
            if result.sound == "splash":
                duck_sounds.eat()  # Use eat sound for now
            elif result.sound == "bounce":
                duck_sounds.play()
            elif result.sound == "music":
                duck_sounds.quack("happy")
            else:
                duck_sounds.play()
        else:
            duck_sounds.play()
        
        # Update goals
        self.goals.update_progress("interact_item", 1)
        
        # Check achievements
        self._statistics["item_interactions"] = self._statistics.get("item_interactions", 0) + 1
        if self._statistics["item_interactions"] >= 10:
            self._unlock_achievement("playful_duck")
        if self._statistics["item_interactions"] >= 50:
            self._unlock_achievement("item_master")
        
        # Reset interaction phase (animation system handles the rest)
        self._interaction_target_item = None
        self._interaction_target_pos = None
        self._interaction_pending_result = None

    def _execute_item_interaction_immediate(self, item_id: str):
        """Execute item interaction without movement animation (for backward compatibility)."""
        if not self.duck:
            return
        
        # Build duck state for edge case detection
        needs = self.duck.get_needs()
        duck_state = {
            "energy": needs.get("energy", 100),
            "hunger": needs.get("hunger", 100),
            "fun": needs.get("fun", 100),
            "cleanliness": needs.get("cleanliness", 100),
            "social": needs.get("social", 100),
            "mood": self.duck.get_mood().state.value,
            "growth_stage": self.duck.growth_stage.value if hasattr(self.duck.growth_stage, 'value') else str(self.duck.growth_stage),
        }
        
        result = execute_interaction(item_id, duck_state)
        
        if not result or not result.success:
            self.renderer.show_message("*confused quack* I don't know how to do that...", category="duck")
            return
        
        self._complete_item_interaction(item_id, result)
    
    def _start_item_interaction_animation(self, item_id: str, result: InteractionResult):
        """Start the animation for an item interaction."""
        # Store the animation state
        self._item_interaction_active = True
        self._item_interaction_item = item_id
        self._item_interaction_frames = result.animation_frames
        self._item_interaction_frame_idx = 0
        self._item_interaction_start = time.time()
        self._item_interaction_duration = result.duration
        self._item_interaction_message = result.message
        self._item_interaction_frame_time = 0.5  # seconds per frame
        
        # Show the message
        self.renderer.show_message(result.message, duration=result.duration + 1.0, category="duck")
    
    def _update_item_interaction_animation(self):
        """Update the item interaction animation."""
        if not hasattr(self, '_item_interaction_active') or not self._item_interaction_active:
            return
        
        elapsed = time.time() - self._item_interaction_start
        
        # Update frame
        frame_idx = int(elapsed / self._item_interaction_frame_time)
        if frame_idx >= len(self._item_interaction_frames):
            # Animation complete
            self._item_interaction_active = False
            self._interaction_phase = InteractionPhase.IDLE
            return
        
        self._item_interaction_frame_idx = frame_idx
    
    def get_current_interaction_frame(self) -> Optional[List[str]]:
        """Get the current animation frame for item interaction."""
        if not hasattr(self, '_item_interaction_active') or not self._item_interaction_active:
            return None
        
        if self._item_interaction_frame_idx < len(self._item_interaction_frames):
            return self._item_interaction_frames[self._item_interaction_frame_idx]
        return None

    def _handle_action(self, action: GameAction, key=None):
        """Handle a game action."""
        # Priority: Handle active minigame input FIRST (before anything else)
        if self._active_minigame and key:
            key_str = str(key).lower() if key else ""
            key_name = key.name if hasattr(key, 'name') else ""
            if self._handle_minigame_input(key_str, key_name):
                return

        # Handle reset confirmation dialog
        if self._reset_confirmation and key:
            key_str = str(key).lower()
            if key_str == 'y':
                self._confirm_reset()
                return
            elif key_str == 'n' or action == GameAction.CANCEL:
                self._cancel_reset()
                return
            return  # Ignore other keys during confirmation

        # Check for direct key actions first - includes UI keys and interaction keys
        if self._state == "playing" and self.duck and key:
            key_raw = str(key)  # Raw key for shift detection
            key_str = key_raw.lower()
            key_name = getattr(key, 'name', '') or ''

            # Handle ESC to close any overlay
            if key_name == 'KEY_ESCAPE':
                self._close_all_overlays()
                return

            # Reset game confirmation (Shift+X) - requires uppercase X
            if key_raw == 'X':
                self._start_reset_confirmation()
                return

            # Hidden debug menu (backtick key)
            if key_str == '`' or key_str == '~':
                self._debug_menu_open = not self._debug_menu_open
                self._debug_submenu = None
                self._debug_menu_selected = 0
                if self._debug_menu_open:
                    self._show_debug_menu()
                else:
                    self.renderer.dismiss_overlay()
                return

            # Page Up/Down for chat log scrolling
            if key_name == 'KEY_PGUP':
                self.renderer.scroll_chat_up()
                return
            if key_name == 'KEY_PGDOWN':
                self.renderer.scroll_chat_down()
                return

            # TAB key - no longer opens menu (master menu is always visible)
            # Keep for backwards compatibility - just ignore
            if key_str == '\t' or key_name == 'KEY_TAB':
                return

            # UI keys and interaction keys
            if key_str in ['s', 't', 'i', 'g', 'm', 'b', 'n', 'x', '+', '=', '-', '_', 'e', 'a', 'c', 'r', 'u', 'j', 'k', 'f', 'p', 'l', 'd', 'z', 'h', 'o', 'v', 'w', 'y', 'q', '1', '2', '3', '4', '5', '6', '7']:
                self._handle_playing_action(action, key)
                return

        # Handle title screen input BEFORE checking for NONE action
        # This allows arrow keys to work on title screen
        if self._state == "title":
            self._handle_title_input(action, key)
            return

        if action == GameAction.NONE:
            return

        # Global actions
        if action == GameAction.QUIT:
            self._quit()
            return

        if action == GameAction.RETURN_TO_TITLE:
            self._return_to_title()
            return

        if action == GameAction.HELP:
            self._close_all_menus()  # Close any open menus first
            self.renderer.toggle_help()
            return

        if action == GameAction.CANCEL:
            self.renderer.hide_overlays()
            self._close_all_menus()  # Also close any open menus
            self._show_goals = False
            return

        # State-specific actions
        if self._state == "offline_summary":
            self._state = "playing"
            self._pending_offline_summary = None
            # Start game music after dismissing offline summary
            sound_engine.stop_music()
            sound_engine.stop_background_music()
            weather_str = self.atmosphere.current_weather.weather_type.value if self.atmosphere.current_weather else "sunny"
            duck_mood = self.duck.get_mood().state.value if self.duck else "content"
            music_context = get_music_context(weather=weather_str, duck_mood=duck_mood)
            sound_engine.update_music(music_context, force=True)
            return

        if self._state == "playing" and self.duck:
            self._handle_playing_action(action, key)

    def _handle_playing_action(self, action: GameAction, key=None):
        """Handle actions while playing."""
        # Check if any menu/overlay is open that uses number keys
        # Define this early so it can be used for both direct key handling and fallback
        has_number_key_menu = (
            self._crafting_menu_open or
            self._building_menu_open or
            self._areas_menu_open or
            self._use_menu_open or
            self._minigames_menu_open or
            self._quests_menu_open or
            self.renderer._show_message_overlay or
            self.renderer._show_inventory
        )

        # Handle menu inputs first (if any menu is open)
        if key:
            key_str = str(key).lower() if not key.is_sequence else ''
            key_name = key.name if key.name else ''

            # Check for open menus and handle their input
            if self._crafting_menu_open:
                if self._handle_crafting_input(key_str, key_name, key):
                    return

            if self._building_menu_open:
                if self._handle_building_input(key_str, key_name, key):
                    return

            if self._areas_menu_open:
                if self._handle_areas_input(key_str, key_name, key):
                    return

            if self._use_menu_open:
                if self._handle_use_input(key_str, key_name, key):
                    return

            if self._minigames_menu_open:
                if self._handle_minigames_menu_input(key_str, key_name, key):
                    return

            # Check if a minigame is active
            if self._active_minigame:
                if self._handle_minigame_input(key_str, key_name):
                    return

            # Handle fishing input when actively fishing
            if self.fishing.is_fishing:
                if self._handle_fishing_input(key_str, key_name, key):
                    return

            # Quit [Q] - Close menus first, then quit if nothing is open
            if key_str == 'q':
                # Check if any menu or overlay is open
                has_overlay = (
                    self._crafting_menu_open or
                    self._building_menu_open or
                    self._areas_menu_open or
                    self._use_menu_open or
                    self._minigames_menu_open or
                    self._show_goals or
                    self.renderer._show_stats or
                    self.renderer._show_inventory or
                    self.renderer._show_shop or
                    self.renderer._show_help or
                    self.renderer._show_talk or
                    self.renderer._show_message_overlay
                )
                if has_overlay:
                    self._close_all_overlays()
                    return
                else:
                    self._quit()
                    return

            # Universal ESC and Backspace to close any overlay
            if key.name == "KEY_ESCAPE" or key.name == "KEY_BACKSPACE":
                # Check if any overlay is open and close it
                if self.renderer._show_stats:
                    self.renderer._stats_scroll_offset = 0
                    self.renderer.toggle_stats()
                    return
                if self.renderer._show_inventory:
                    self.renderer.toggle_inventory()
                    return
                if self.renderer._show_help:
                    self.renderer.toggle_help()
                    return
                if self._show_goals:
                    self._show_goals = False
                    self.renderer.dismiss_message()
                    return
                # If no overlay open, do nothing (or could close message overlay)
                if self.renderer._show_message_overlay:
                    self.renderer._show_message_overlay = False
                    return

            # Stats overlay - arrow key navigation when open
            if self.renderer._show_stats:
                if key.name == "KEY_UP":
                    self.renderer._stats_scroll_offset = max(0, self.renderer._stats_scroll_offset - 1)
                    return
                if key.name == "KEY_DOWN":
                    self.renderer._stats_scroll_offset += 1
                    return
                # S closes stats
                if key_str == 's':
                    self.renderer._stats_scroll_offset = 0
                    self.renderer.toggle_stats()
                    return
                # Consume other keys when stats is open
                return

            # Stats toggle [S]
            if key_str == 's':
                self._close_all_menus()  # Close any open menus first
                self.renderer.toggle_stats()
                return

            # Talk toggle [T]
            if key_str == 't':
                self._close_all_menus()  # Close any open menus first
                self.renderer.toggle_talk()
                return

            # Inventory toggle [I]
            if key_str == 'i':
                self._close_all_menus()  # Close any open menus first
                self.renderer.toggle_inventory()
                return

            # Goals toggle [G] - handle pagination when open
            if key_str == 'g':
                if self._show_goals:
                    self._show_goals = False
                    self.renderer.dismiss_message()
                else:
                    self._show_goals = True
                    self._goals_page = 0  # Reset to first page
                    self._show_goals_overlay()
                return
            
            # Handle goals pagination when goals overlay is open
            if self._show_goals:
                if key_str == ',' or key_str == '<':
                    if not hasattr(self, '_goals_page'):
                        self._goals_page = 0
                    self._goals_page = max(0, self._goals_page - 1)
                    self._show_goals_overlay()
                    return
                if key_str == '.' or key_str == '>':
                    if not hasattr(self, '_goals_page'):
                        self._goals_page = 0
                    self._goals_page += 1
                    self._show_goals_overlay()
                    return

            # Shop toggle [B] (for Buy)
            if key_str == 'b':
                self._close_all_menus()  # Close any open menus first
                self.renderer.toggle_shop()
                return

            # Use/Interact toggle [U] - Show interaction menu for owned items
            if key_str == 'u':
                self._show_use_menu()
                return

            # Music mute toggle [M]
            if key_str == 'm':
                muted = sound_engine.toggle_music_mute()
                status = "OFF" if muted else "ON"
                self.renderer.show_message(f"Music: {status}")
                return

            # Sound toggle [N]
            if key_str == 'n':
                self._sound_enabled = sound_engine.toggle()
                status = "ON" if self._sound_enabled else "OFF"
                self.renderer.show_message(f"Sound: {status}")
                return

            # Volume up [+] or [=]
            if key_str in ['+', '=']:
                new_vol = sound_engine.volume_up()
                vol_bar = sound_engine.get_volume_display()
                self.renderer.show_message(f"Volume: {vol_bar} {int(new_vol * 100)}%")
                return

            # Volume down [-] or [_]
            if key_str in ['-', '_']:
                new_vol = sound_engine.volume_down()
                vol_bar = sound_engine.get_volume_display()
                self.renderer.show_message(f"Volume: {vol_bar} {int(new_vol * 100)}%")
                return

            # Explore [E] - Explore current area for resources
            if key_str == 'e':
                self._do_explore()
                return

            # Craft [C] - Open crafting menu
            if key_str == 'c':
                self._show_crafting_menu()
                return

            # Build [R] - Open building menu (R for conStRuct)
            if key_str == 'r':
                self._show_building_menu()
                return

            # Decorations [V] - Decorate rooms
            if key_str == 'v':
                self._show_decorations_menu()
                return

            # Areas [A] - Show available areas to explore
            if key_str == 'a':
                self._show_areas_menu()
                return

            # Mini-games [J] - Play mini-games for rewards
            if key_str == 'j':
                self._show_minigames_menu()
                return

            # Duck Facts [K] - Show a random duck fact (K for Knowledge)
            if key_str == 'k':
                self._show_duck_fact()
                return

            # Quests/Objectives [O]
            if key_str == 'o':
                self._show_quests_menu()
                return

            # Trading Post [<] (Visiting merchants)
            if key_str == '<' or key_str == ',':
                self._show_trading_menu()
                return

            # Weather Activities [W]
            if key_str == 'w':
                self._show_weather_activities()
                return

            # Scrapbook/Memory Album [Y]
            if key_str == 'y':
                self._show_scrapbook()
                return

            # Treasure Hunting [6]
            if key_str == '6':
                self._show_treasure_hunt()
                return

            # Secrets Book [\]
            if key_str == '\\':
                self._show_secrets_book()
                return

            # Prestige/Legacy System [8]
            if key_str == '8':
                self._show_prestige_menu()
                return

            # Save Slots [/]
            if key_str == '/':
                self._show_save_slots_menu()
                return

            # Garden System [9]
            if key_str == '9':
                self._show_garden_menu()
                return

            # Festivals [0]
            if key_str == '0':
                self._show_festival_menu()
                return

            # Tricks Menu [7]
            if key_str == '7':
                self._show_tricks_menu()
                return

            # Titles Menu [`] (backtick - quick access since it's a prestige feature)
            if key_str == '~' or key_str == '`':
                # If not in debug menu, show titles
                if not self._debug_menu_open:
                    self._show_titles_menu()
                    return

            # Enhanced Diary [=]
            if key_str == '=':
                self._show_enhanced_diary()
                return

            # Collectibles Album [']
            if key_str == "'":
                self._show_collectibles_album()
                return

            # Take Photo [;] (quick diary photo)
            if key_str == ';':
                self._take_diary_photo()
                return

            # Help toggle [H]
            if key_str == 'h':
                self._close_all_menus()  # Close any open menus first
                self.renderer.toggle_help()
                return

            # Duck interaction keys - close any overlays first and perform action
            # Note: has_number_key_menu is defined at the start of this method
            # Feed [F] - always works; [1] only when no menu open
            if key_str == 'f' or (key_str == '1' and not has_number_key_menu):
                self._close_all_overlays()
                self._perform_interaction("feed")
                return

            # Play [P] - always works; [2] only when no menu open
            if key_str == 'p' or (key_str == '2' and not has_number_key_menu):
                self._close_all_overlays()
                self._perform_interaction("play")
                return

            # Clean [L] - always works; [3] only when no menu open
            if key_str == 'l' or (key_str == '3' and not has_number_key_menu):
                self._close_all_overlays()
                self._perform_interaction("clean")
                return

            # Pet [D] - always works; [4] only when no menu open
            if key_str == 'd' or (key_str == '4' and not has_number_key_menu):
                self._close_all_overlays()
                self._perform_interaction("pet")
                return

            # Sleep [Z] - always works; [5] only when no menu open
            if key_str == 'z' or (key_str == '5' and not has_number_key_menu):
                self._close_all_overlays()
                self._perform_interaction("sleep")
                return

        # Interaction actions (from GameAction enum) - fallback for any missed cases
        # Only process if no menu is open (same check as above for number keys)
        if not has_number_key_menu:
            interaction_map = {
                GameAction.FEED: "feed",
                GameAction.PLAY: "play",
                GameAction.CLEAN: "clean",
                GameAction.PET: "pet",
                GameAction.SLEEP: "sleep",
            }

            if action in interaction_map:
                interaction = interaction_map[action]
                self._perform_interaction(interaction)

    def _show_goals_overlay(self):
        """Show the goals overlay with pagination."""
        active_goals = self.goals.get_active_goals()
        completed = self.goals.get_completed_count()
        total = self.goals.get_total_count()

        # Pagination settings
        items_per_page = 5
        if not hasattr(self, '_goals_page'):
            self._goals_page = 0
        total_pages = max(1, (len(active_goals) + items_per_page - 1) // items_per_page)
        current_page = min(self._goals_page, total_pages - 1)
        start_idx = current_page * items_per_page
        end_idx = min(start_idx + items_per_page, len(active_goals))

        # Build goals text
        lines = [
            f"Goals Completed: {completed}/{total}",
        ]
        
        if total_pages > 1:
            lines.append(f"Page {current_page + 1}/{total_pages} (</> to change)")
        lines.append("-" * 30)

        for goal in active_goals[start_idx:end_idx]:
            progress = f"[{goal.progress}/{goal.target}]" if goal.target > 1 else ""
            status = "!" if goal.progress >= goal.target else " "
            lines.append(f"{status} {goal.name} {progress}")
            lines.append(f"   {goal.description}")

        if not active_goals:
            lines.append("All current goals complete!")
            lines.append("Check back later for more...")

        # Add achievements hint
        unlocked = self.achievements.get_unlocked_count()
        total_ach = self.achievements.get_total_count()
        lines.extend([
            "",
            f"Achievements: {unlocked}/{total_ach} unlocked",
            "",
            "[G] Close" + (" | [</>] Page" if total_pages > 1 else ""),
        ])

        self.renderer.show_overlay("\n".join(lines), duration=0)

    def _perform_interaction(self, interaction: str):
        """Perform an interaction with the duck."""
        if not self.duck:
            return

        # Check cooldown
        current_time = time.time()
        cooldown = self._interaction_cooldowns.get(interaction, 15)
        last_time = self._last_interaction_time.get(interaction, 0)
        time_since = current_time - last_time

        if time_since < cooldown:
            remaining = int(cooldown - time_since)
            # Show cooldown message with duck reaction
            cooldown_messages = {
                "feed": f"Cheese is still digesting! Wait {remaining}s",
                "play": f"Cheese needs a breather! Wait {remaining}s",
                "clean": f"Already squeaky clean! Wait {remaining}s",
                "pet": f"Give Cheese some space! Wait {remaining}s",
                "sleep": f"Cheese isn't tired yet! Wait {remaining}s",
            }
            msg = cooldown_messages.get(interaction, f"Wait {remaining}s...")
            self.renderer.show_message(msg, duration=1.5)
            duck_sounds.quack("grumpy")
            return

        # Record this interaction time
        self._last_interaction_time[interaction] = current_time

        # Clear any autonomous action (skip for sleep - _start_dream will set proper timing)
        if self.behavior_ai and interaction != "sleep":
            self.behavior_ai.clear_action()

        # Set duck visual state with appropriate duration
        state_durations = {
            "feed": 4.0,    # Eating animation for 4 seconds
            "play": 3.0,    # Playing animation for 3 seconds
            "sleep": 20.0,  # Sleeping animation - will be extended by dream if needed
            "clean": 3.5,   # Cleaning animation for 3.5 seconds
            "pet": 2.5,     # Petting animation for 2.5 seconds
        }
        duration = state_durations.get(interaction, 3.0)
        
        if interaction == "feed":
            self.renderer.set_duck_state("eating", duration)
        elif interaction == "play":
            self.renderer.set_duck_state("playing", duration)
        elif interaction == "sleep":
            # Start dream - this sets the sleeping state with proper duration
            self._start_dream()
        elif interaction == "clean":
            self.renderer.set_duck_state("cleaning", duration)
        elif interaction == "pet":
            self.renderer.set_duck_state("petting", duration)
        else:
            self.renderer.set_duck_state("idle", 1.0)

        # Notify reaction controller that user action is in progress
        # This prevents weather reactions from overriding user-initiated animations
        # Skip for sleep - it notifies with the correct dream duration in _start_dream()
        if interaction != "sleep":
            self.reaction_controller.notify_user_action(duration, time.time())

        # Perform the interaction
        result = self.duck.interact(interaction)

        # Record in memory
        mood = self.duck.get_mood()
        emotional_value = 10 if mood.score > 50 else 5
        self.duck.memory.add_interaction(interaction, "", emotional_value)
        self.duck.memory.total_interactions += 1
        self.duck.memory.record_mood(mood.score)
        
        # Record action in DuckBrain for Seaman-style callbacks
        if self.duck_brain:
            # Build context string
            context_parts = []
            if mood:
                context_parts.append(f"mood: {mood.state.value}")
            time_of_day = self.clock.get_time_of_day()
            context_parts.append(f"time: {time_of_day}")
            weather = self.atmosphere.current_weather
            if weather:
                context_parts.append(f"weather: {weather.weather_type.value}")
            context = ", ".join(context_parts)
            self.duck_brain.process_action(interaction, context)
        
        # Log emotion to enhanced diary
        from dialogue.diary_enhanced import EmotionCategory
        emotion_map = {
            "feed": (EmotionCategory.CONTENTMENT, "eating"),
            "play": (EmotionCategory.JOY, "playing"),
            "clean": (EmotionCategory.CALM, "bath time"),
            "pet": (EmotionCategory.LOVE, "being petted"),
            "sleep": (EmotionCategory.CALM, "resting"),
        }
        if interaction in emotion_map:
            emotion, trigger = emotion_map[interaction]
            intensity = min(10, max(1, mood.score // 10))
            self.enhanced_diary.log_emotion(emotion, intensity, trigger=trigger)

        # Update statistics
        stat_keys = {
            "feed": "times_fed",
            "play": "times_played",
            "clean": "times_cleaned",
            "pet": "times_petted",
            "sleep": "times_slept",
        }
        stat_key = stat_keys.get(interaction, f"times_{interaction}")
        self._statistics[stat_key] = self._statistics.get(stat_key, 0) + 1

        # Track for bread_obsessed secret (10 feeds in one session)
        if interaction == "feed":
            self._session_feeds += 1
            if self._session_feeds >= 10:
                self.goals._check_secret_goal("bread_feast")

        # Update diary relationship (builds emotional connection)
        level_change = self.diary.increase_relationship(1)
        if level_change:
            level, level_name = level_change
            self.renderer.show_celebration(
                "relationship",
                f"Relationship Level Up! You're now: {level_name}!",
                duration=4.0
            )
            duck_sounds.level_up()
            
            # Log relationship milestone to scrapbook
            from world.scrapbook import PhotoCategory
            duck_age = self.duck.get_age_days() if self.duck else 1
            location = self.exploration.current_area.name if self.exploration.current_area else "Home Pond"
            weather = self.atmosphere.current_weather.weather_type.value if self.atmosphere.current_weather else "sunny"
            mood_val = self.duck.get_mood().state.value if self.duck else "happy"
            self.scrapbook.take_photo(
                title=f"{level_name}!",
                description=f"Our relationship grew to {level_name}!",
                category=PhotoCategory.MILESTONE,
                art_key="duck_happy",
                mood=mood_val,
                duck_age=duck_age,
                location=location,
                weather=weather,
                tags=["relationship", level_name.lower().replace(" ", "_")]
            )
            self.enhanced_diary.add_chapter_event(f"Relationship grew to {level_name}!")

        # Record first interactions in diary
        if self._statistics[stat_key] == 1:
            if interaction == "pet":
                self.diary.record_relationship_change("first_pet")

        # Chance to record a random memory (builds narrative)
        self.diary.record_random_memory()

        # Update goals
        self.goals.update_progress(interaction, 1)

        # Update progression system
        self.progression.record_interaction(interaction)
        self.progression.update_challenge_progress(interaction, 1)

        # Check for happy interactions (for challenges)
        if mood.score > 60:
            self.progression.update_challenge_progress("happy", 1)

        # Award currency for interaction
        currency_reward = 5
        self.habitat.add_currency(currency_reward)

        # Random collectible chance on interactions
        collectible = self.progression.random_collectible_drop(0.03)
        if collectible:
            self._show_collectible_found(collectible)

        # Check for lucky events (variable ratio reinforcement - dopamine!)
        lucky_event = self.progression.check_lucky_event()
        if lucky_event:
            message, reward = lucky_event
            self.renderer.show_message(message, duration=3.0)
            self._apply_reward(reward)

        # Check for surprise gifts (rare dopamine hits)
        surprise = self.progression.get_surprise_gift()
        if surprise:
            gift_message, reward = surprise
            if reward.rare:
                self.renderer.show_celebration("surprise_gift", gift_message, duration=3.5)
            else:
                self.renderer.show_message(gift_message, duration=4.0)
            self._apply_reward(reward)

        # Roll for interaction bonus XP (slot machine psychology)
        bonus = self.progression.roll_interaction_bonus()
        if bonus:
            bonus_msg, bonus_xp = bonus
            self.progression.add_xp(bonus_xp, "bonus")
            # Jackpot gets celebration
            if bonus_xp >= 50:
                self.renderer.show_celebration("jackpot", bonus_msg, duration=3.0)
                duck_sounds.level_up()
            else:
                self.renderer.show_message(bonus_msg, duration=2.0)

        # Check for level up
        new_level = self.progression.add_xp(5, interaction)
        if new_level:
            self._on_level_up(new_level)

        # Check milestones
        milestones = self.progression.check_milestones()
        for category, threshold, reward in milestones:
            self._show_milestone_achieved(category, threshold, reward)

        # Check achievements
        self._check_achievements(interaction)

        # Update challenge progress for this interaction type
        challenge_updates = self.challenges.update_progress(interaction, 1)
        for challenge_id, completed in challenge_updates:
            if completed:
                self.renderer.show_message(f"[#] Challenge Complete: {challenge_id}!", duration=3.0)

        # Update quest progress for this interaction type
        self._process_quest_updates("interact", interaction, 1)

        # Update personality traits based on interaction
        personality_trait_map = {
            "feed": ("optimism", 1, "Being fed"),
            "pet": ("emotional_depth", 1, "Being petted"),
            "play": ("curiosity", 1, "Playing"),
            "clean": ("vanity", 1, "Being cleaned"),
        }
        if interaction in personality_trait_map:
            trait_id, delta, reason = personality_trait_map[interaction]
            self.extended_personality.adjust_trait(trait_id, delta, reason)

        # Update hidden trait discovery progress based on consistent actions
        hidden_trait_map = {
            "feed": ("gentle_soul", 0.01),  # Caring actions
            "pet": ("gentle_soul", 0.02),   # Affectionate actions
            "play": ("adventurer", 0.01),   # Active actions
        }
        if interaction in hidden_trait_map:
            trait_id, progress = hidden_trait_map[interaction]
            self.extended_personality.update_hidden_trait_progress(trait_id, progress)

        # Play sound
        sound_map = {
            "feed": duck_sounds.eat,
            "play": duck_sounds.play,
            "clean": duck_sounds.splash,
            "pet": duck_sounds.pet,
            "sleep": duck_sounds.sleep,
        }
        if interaction in sound_map:
            sound_map[interaction]()

        # Get dialogue response
        response = self.conversation.get_interaction_response(self.duck, interaction)
        self.renderer.show_message(response)

        # Show effect and closeup
        if interaction == "pet":
            self.renderer.show_effect("heart", 1.5)
            self.renderer.show_closeup("pet", 2.5)
            duck_sounds.quack("happy")
        elif interaction == "play":
            self.renderer.show_effect("sparkle", 1.0)
            self.renderer.show_closeup("play", 2.0)
            duck_sounds.quack("happy")
        elif interaction == "feed":
            self.renderer.show_closeup("feed", 2.0)
            duck_sounds.quack("content")
        elif interaction == "sleep":
            self.renderer.show_closeup("sleep", 2.5)
            # Chance to record a dream when sleeping
            if random.random() < 0.4:  # 40% chance of dream
                self._record_random_dream()
        elif interaction == "clean":
            self.renderer.show_closeup(None, 1.5)
            duck_sounds.quack("normal")

    def _check_achievements(self, interaction: str):
        """Check for achievement unlocks."""
        if not self.duck:
            return

        # Check interaction count achievements
        count = self._statistics.get(f"times_{interaction}ed" if interaction == "play" else f"times_{interaction}", 0)

        if count == 10:
            self._unlock_achievement(f"10_{interaction}s")
        elif count == 50:
            self._unlock_achievement(f"50_{interaction}s")
        elif count == 100:
            self._unlock_achievement(f"100_{interaction}s")

        # Check mood-based achievements
        mood = self.duck.get_mood()
        if mood.state.value == "ecstatic":
            self._unlock_achievement("first_ecstatic")

        # Check relationship achievements
        if self.duck.memory.get_relationship_level() == "bonded":
            self._unlock_achievement("best_friends")


    def _on_level_up(self, new_level: int):
        """Handle level up notification."""
        duck_sounds.level_up()
        self.renderer.show_effect("sparkle", 2.0)
        self.renderer.show_celebration(
            "level_up",
            f"Level {new_level}! {self.progression.title}",
            duration=4.0
        )
        # Trigger duck reaction animation
        self.reaction_controller.trigger_event_reaction("level_up", time.time())
        # Play celebration music temporarily
        sound_engine.play_event_music(MusicContext.CELEBRATION, duration=5.0)
        
        # Log to scrapbook
        from world.scrapbook import PhotoCategory
        duck_age = self.duck.get_age_days() if self.duck else 1
        location = self.exploration.current_area.name if self.exploration.current_area else "Home Pond"
        weather = self.atmosphere.current_weather.weather_type.value if self.atmosphere.current_weather else "sunny"
        mood = self.duck.get_mood().state.value if self.duck else "happy"
        self.scrapbook.take_photo(
            title=f"Level {new_level}!",
            description=f"{self.duck.name if self.duck else 'Duck'} reached level {new_level}!",
            category=PhotoCategory.MILESTONE,
            art_key="duck_celebration",
            mood=mood,
            duck_age=duck_age,
            location=location,
            weather=weather,
            tags=["level_up", f"level_{new_level}"]
        )
        
        # Log to enhanced diary life chapter
        self.enhanced_diary.add_chapter_event(f"Reached level {new_level}!")

        # Check for new title
        if self.progression.title:
            self.renderer.show_message(f"New title: {self.progression.title}", duration=3.0)

        # Check for home unlocks
        unlocks = self.home.check_unlocks(
            new_level,
            self.progression.stats,
            self.progression.current_streak,
            self.progression.collectibles
        )
        for unlock_id in unlocks:
            if unlock_id.startswith("theme:"):
                theme_id = unlock_id[6:]
                self.home.unlock_theme(theme_id)
                self.renderer.show_message(f"Unlocked home theme: {theme_id}!", duration=3.0)
            else:
                self.home.unlock_decoration(unlock_id)
                self.renderer.show_message(f"Unlocked decoration: {unlock_id}!", duration=3.0)

    def _on_friendship_level_up(self, friend, old_level, new_level):
        """Handle when friendship with a duck friend increases."""
        from world.scrapbook import PhotoCategory
        from world.friends import FriendshipLevel
        
        duck_age = self.duck.get_age_days() if self.duck else 1
        location = self.exploration.current_area.name if self.exploration.current_area else "Home Pond"
        weather = self.atmosphere.current_weather.weather_type.value if self.atmosphere.current_weather else "sunny"
        mood_val = self.duck.get_mood().state.value if self.duck else "happy"
        level_name = new_level.value.replace('_', ' ') if hasattr(new_level, 'value') else str(new_level)
        
        self.scrapbook.take_photo(
            title=f"{friend.name}: {level_name}!",
            description=f"Friendship with {friend.name} grew to {level_name}!",
            category=PhotoCategory.FRIENDSHIP,
            art_key="duck_friends",
            mood=mood_val,
            duck_age=duck_age,
            location=location,
            weather=weather,
            tags=["friendship", friend.name.lower(), level_name.lower().replace(" ", "_")]
        )
        self.enhanced_diary.add_chapter_event(f"Became {level_name} with {friend.name}!")

    def _process_quest_updates(self, objective_type: str, target: str, amount: int = 1):
        """Process quest objective updates and apply any earned rewards."""
        objective_updates, completed_quests = self.quests.update_progress(objective_type, target, amount)
        
        # Show objective completion messages
        for quest_id, objective, completed in objective_updates:
            if completed:
                self.renderer.show_message(f"[=] Quest objective complete!", duration=2.0)
        
        # Apply rewards for completed quests
        for quest_id, reward in completed_quests:
            quest = QUESTS.get(quest_id)
            quest_name = quest.name if quest else quest_id.replace("_", " ").title()
            
            # Apply coin reward
            if reward.coins > 0:
                self.habitat.add_currency(reward.coins)
            
            # Apply XP reward
            if reward.xp > 0:
                new_level = self.progression.add_xp(reward.xp, "quest")
                if new_level:
                    self._on_level_up(new_level)
            
            # Apply item rewards
            for item_id in reward.items:
                self.inventory.add_item(item_id)
            
            # Apply unlocks (achievements, features, etc.)
            for unlock in reward.unlocks:
                if unlock.startswith("achievement:"):
                    self._unlock_achievement(unlock[12:])
            
            # Show completion celebration
            duck_sounds.level_up()
            self.renderer.show_effect("sparkle", 2.0)
            
            # Build reward message
            reward_lines = []
            if reward.coins > 0:
                reward_lines.append(f"+{reward.coins} Coins")
            if reward.xp > 0:
                reward_lines.append(f"+{reward.xp} XP")
            if reward.items:
                reward_lines.append(f"Items: {', '.join(reward.items)}")
            if reward.title:
                reward_lines.append(f"Title: {reward.title}")
            
            reward_text = " | ".join(reward_lines) if reward_lines else "Quest Complete!"
            self.renderer.show_celebration(
                "quest_complete",
                f"Quest Complete: {quest_name}!\n{reward_text}",
                duration=5.0
            )
            
            # Update statistics
            self.progression.stats["quests_completed"] = self.progression.stats.get("quests_completed", 0) + 1

    def _show_collectible_found(self, collectible_id: str):
        """Show notification for finding a collectible."""
        if ":" not in collectible_id:
            return

        category, item_id = collectible_id.split(":", 1)
        if category in COLLECTIBLES and item_id in COLLECTIBLES[category]["items"]:
            item_data = COLLECTIBLES[category]["items"][item_id]
            name = item_data["name"]
            rarity = item_data.get("rarity", "common")

            duck_sounds.level_up()
            self.renderer.show_effect("sparkle", 1.5)

            rarity_prefix = ""
            if rarity == "legendary":
                rarity_prefix = "LEGENDARY "
            elif rarity == "rare":
                rarity_prefix = "Rare "

            # Use celebration for legendary items
            if rarity == "legendary":
                self.renderer.show_celebration(
                    "collectible_found",
                    f"LEGENDARY: {name}!",
                    duration=4.0
                )
            else:
                self.renderer.show_message(f"Found {rarity_prefix}collectible: {name}!", duration=4.0)

    def _show_milestone_achieved(self, category: str, threshold: int, reward: Reward):
        """Show notification for milestone achievement."""
        duck_sounds.level_up()
        self.renderer.show_effect("sparkle", 1.5)

        # Big milestones get celebration overlay
        if threshold >= 100 or category == "streak":
            self.renderer.show_celebration(
                "streak_milestone" if category == "streak" else "achievement",
                f"{category.title()} x{threshold}!",
                duration=3.5
            )
        else:
            self.renderer.show_message(f"Milestone! {category.title()} x{threshold}!", duration=3.0)

        # Apply reward
        self._apply_reward(reward)

    def _apply_reward(self, reward: Reward):
        """Apply a reward to the player."""
        if reward.reward_type == RewardType.ITEM:
            for _ in range(reward.amount):
                self.inventory.add_item(reward.value)
            item = get_item_info(reward.value)
            name = item.name if item else reward.value
            self.renderer.show_message(f"Received: {name} x{reward.amount}!", duration=2.0, category="action")

        elif reward.reward_type == RewardType.XP:
            xp = int(reward.value)
            new_level = self.progression.add_xp(xp, "reward")
            self.renderer.show_message(f"+{xp} XP!", duration=2.0, category="action")
            if new_level:
                self._on_level_up(new_level)

        elif reward.reward_type == RewardType.COLLECTIBLE:
            if self.progression.add_collectible(reward.value):
                self._show_collectible_found(reward.value)

        elif reward.reward_type == RewardType.TITLE:
            if reward.value not in self.progression.unlocked_titles:
                self.progression.unlocked_titles.append(reward.value)
                self.renderer.show_message(f"Unlocked title: {reward.value}!", duration=3.0, category="discovery")

    def _check_daily_login(self):
        """Check for daily login rewards."""
        # Check how long player was away (before updating login date)
        days_away = self.progression.calculate_days_away()

        is_new_day, rewards, special_message = self.progression.check_login()

        if is_new_day and rewards:
            # Generate daily challenges
            self.progression.generate_daily_challenges()

            # Show time-based greeting first
            greeting = self.progression.get_time_greeting()
            self.renderer.show_message(greeting, duration=4.0)

            # Show comfort message if player was away
            if days_away > 1:
                comfort_msg = self.progression.get_time_away_message(days_away)
                if comfort_msg:
                    self.renderer.show_message(comfort_msg, duration=4.0)

            # Show special message (streak loss or celebration)
            if special_message:
                self.renderer.show_message(special_message, duration=5.0)

            # Show streak info and multiplier
            streak = self.progression.current_streak
            multiplier_display = self.progression.get_streak_multiplier_display()

            if streak > 1:
                streak_msg = f"Day {streak} streak! {multiplier_display}".strip()
                self.renderer.show_message(streak_msg, duration=3.0)

            # Store pending rewards for display
            self._pending_daily_rewards = rewards

            # Auto-claim rewards
            for reward in rewards:
                self._apply_reward(reward)

    def _update(self):
        """Update game state."""
        current_time = time.time()

        # Update item interaction animation
        self._update_item_interaction_animation()

        # Update unified interaction controller
        self.interaction_controller.update(0.016)  # ~60fps delta

        # Update interaction animation overlay
        self.renderer.interaction_animator.update()

        # Update active minigame
        self._update_minigame()

        # Update dream sequence
        self._update_dream()

        # Update event animations (butterfly, bird, etc.)
        self._update_event_animations()

        # Update mood visual effects (every frame for smooth animations)
        if self.duck:
            self.mood_visuals.update(0.016)  # ~60fps delta

        # Update sound effects (cleanup expired sounds)
        self.sound_effects.update(current_time)

        # Update fishing system when actively fishing
        if self.fishing.is_fishing:
            fish_msg = self.fishing.update(0.016)
            if fish_msg:
                self._show_message_if_no_menu(fish_msg, duration=2.0, category="duck")

        # Update weather activities (check for completion)
        self._update_weather_activity()

        # Check for travel completion
        if self._duck_traveling:
            if current_time - self._travel_start_time >= self._travel_duration:
                self._complete_travel()

        # Check for exploration completion
        if self._duck_exploring:
            if current_time - self._exploring_start_time >= self._exploring_duration:
                self._complete_exploring()

        # Check for building completion (real-time progress)
        if self._duck_building and self.building.current_build:
            build_result = self.building.update_building(self.materials, 0.1)
            if build_result.get("completed"):
                self._complete_building(build_result)
            elif build_result.get("stage_completed"):
                self._show_message_if_no_menu(build_result.get("message", "Stage complete!"), duration=2.0, category="action")
                duck_sounds.play()  # Hammering sound

        # Update at tick rate
        if current_time - self._last_tick >= TICK_RATE:
            delta_seconds = current_time - self._last_tick
            delta_minutes = self.clock.get_delta_minutes(delta_seconds)

            # Store old stage for growth detection
            old_stage = self.duck.growth_stage

            # Update duck
            self.duck.update(delta_minutes)

            # Check for growth stage change
            if self.duck.growth_stage != old_stage:
                self._on_growth_stage_change(old_stage, self.duck.growth_stage)

            # Record mood
            self.duck.memory.record_mood(self.duck.get_mood().score)

            # Update animation
            self.renderer.update_animation()

            # Update habitat item animations
            if hasattr(self, 'habitat'):
                self.habitat.update_animations()

            # Update goals (time-based)
            self.goals.update_time(delta_minutes)

            # Update garden plants (convert minutes to hours)
            delta_hours = delta_minutes / 60.0
            self.garden.update_plants(delta_hours)

            # Update duck aging system
            new_stage = self.aging.update_stage()
            if new_stage:
                self._show_message_if_no_menu(f"# Your duck has grown to {new_stage.value}!", duration=5.0, category="event")

            # Check secret goals for session/mood-based achievements
            self._check_secret_achievements()

            self._last_tick = current_time

        # Update atmosphere (weather, visitors) every 30 seconds
        if current_time - self._last_atmosphere_check >= 30:
            messages = self.atmosphere.update()
            for msg in messages:
                self._show_message_if_no_menu(msg, duration=4.0, category="event")

            # Check for active festivals
            self._check_festival_events()

            # Track weather for secret goal and duck reactions
            if self.atmosphere.current_weather:
                current_weather = self.atmosphere.current_weather.weather_type.value
                self._weather_seen.add(current_weather)

                # Duck comments on weather changes
                if self._last_known_weather and self._last_known_weather != current_weather:
                    weather_comment = self._get_duck_weather_reaction(current_weather)
                    if weather_comment:
                        # Schedule weather comment after atmosphere message
                        self._pending_weather_comment = weather_comment
                        self._pending_weather_comment_time = current_time + 3.0
                    
                    # Animate duck reacting to weather change
                    self._animate_weather_reaction(current_weather)
                
                self._last_known_weather = current_weather

                # Check for rainbow secret
                if self.atmosphere.current_weather.weather_type == WeatherType.RAINBOW:
                    self.goals._check_secret_goal("saw_rainbow")
                    self.diary.record_adventure("rainbow")

                # Check for storm secret
                if self.atmosphere.current_weather.weather_type == WeatherType.STORMY:
                    self.goals._check_secret_goal("storm_play")

            # Check for super lucky day secret
            if self.atmosphere.day_fortune and self.atmosphere.day_fortune.fortune_type == "super_lucky":
                self.goals._check_secret_goal("super_lucky_day")

            # Check for all weather types seen
            all_basic_weather = {"sunny", "cloudy", "rainy", "stormy", "foggy", "snowy", "windy"}
            if all_basic_weather.issubset(self._weather_seen):
                self.goals._check_secret_goal("all_weather")

            # Check for duck friend visits (only at Home Pond)
            if self.exploration.current_area and self.exploration.current_area.name == "Home Pond":
                from datetime import datetime
                current_hour = datetime.now().hour
                visitor_arrived, visitor_msg = self.friends.check_for_random_visitor(current_hour)
                if visitor_arrived and visitor_msg:
                    # Get the visitor's greeting
                    from world.friends import visitor_animator
                    if self.friends.current_visit:
                        friend = self.friends.get_friend_by_id(self.friends.current_visit.friend_id)
                        if friend:
                            personality = friend.personality.value if hasattr(friend.personality, 'value') else str(friend.personality)
                            friendship_level = friend.friendship_level.value if hasattr(friend.friendship_level, 'value') else str(friend.friendship_level)
                            unlocked_topics = set(friend.unlocked_dialogue) if hasattr(friend, 'unlocked_dialogue') else set()
                            # Pass memory data for context-aware greetings
                            conversation_topics = getattr(friend, 'conversation_topics', [])
                            shared_experiences = getattr(friend, 'shared_experiences', [])
                            last_summary = getattr(friend, 'last_conversation_summary', "")
                            # Build shared memories list for LLM context
                            shared_memories = list(shared_experiences)[:5] if shared_experiences else []
                            if last_summary:
                                shared_memories.append(f"Last time: {last_summary}")
                            visitor_animator.set_visitor(
                                personality, 
                                friend.name,
                                friendship_level,
                                friend.times_visited,
                                unlocked_topics,
                                conversation_topics=conversation_topics,
                                shared_experiences=shared_experiences,
                                last_conversation_summary=last_summary,
                                duck_ref=self.duck,
                                shared_memories=shared_memories,
                            )
                            greeting = visitor_animator.get_greeting(self.duck.name)
                            if greeting:
                                self._show_message_if_no_menu(greeting, duration=6.0, category="friend")
                            duck_sounds.quack("happy")
                            # Trigger friend arrival reaction animation
                            self.reaction_controller.trigger_friend_reaction("arrival", current_time)
                            # Play happy music for the visit
                            sound_engine.play_event_music(MusicContext.HAPPY, duration=10.0)
                            
                            # Log friend visit to scrapbook
                            from world.scrapbook import PhotoCategory
                            duck_age = self.duck.get_age_days() if self.duck else 1
                            location_name = self.exploration.current_area.name if self.exploration.current_area else "Home Pond"
                            weather_val = self.atmosphere.current_weather.weather_type.value if self.atmosphere.current_weather else "sunny"
                            mood_val = self.duck.get_mood().state.value if self.duck else "happy"
                            visit_num = friend.times_visited
                            if visit_num <= 1:
                                # First meeting - extra special!
                                self.scrapbook.take_photo(
                                    title=f"Met {friend.name}!",
                                    description=f"First time meeting {friend.name}!",
                                    category=PhotoCategory.FRIENDSHIP,
                                    art_key="duck_friends",
                                    mood=mood_val,
                                    duck_age=duck_age,
                                    location=location_name,
                                    weather=weather_val,
                                    tags=["friend", "first_meeting", friend.name.lower()]
                                )
                                self.enhanced_diary.add_chapter_event(f"Met {friend.name} for the first time!")
                            
                            # Duck waddles toward the visitor (animated approach)
                            self._duck_approach_visitor()
                            
                            # Schedule duck's reaction comment after greeting
                            duck_reaction = self._get_duck_visitor_reaction(personality)
                            if duck_reaction:
                                # Show duck's comment after a short delay (using a simpler approach)
                                self._pending_visitor_comment = duck_reaction
                                self._pending_visitor_comment_time = current_time + 4.0

            # Update ambient sounds based on current conditions
            weather_str = self.atmosphere.current_weather.weather_type.value if self.atmosphere.current_weather else "clear"
            time_of_day_obj = self.day_night.get_time_of_day() if hasattr(self.day_night, 'get_time_of_day') else None
            time_of_day = time_of_day_obj.value if time_of_day_obj and hasattr(time_of_day_obj, 'value') else "day"
            season = self.atmosphere.current_season.value if hasattr(self.atmosphere, 'current_season') and self.atmosphere.current_season else "spring"
            location = self.exploration.current_area.name if self.exploration.current_area else "pond"
            duck_state = self.duck.get_mood().state.value if self.duck else "neutral"
            self.ambient.update_ambient(weather_str, time_of_day, season, location, duck_state)

            self._last_atmosphere_check = current_time

        # Update duck reactions and dynamic music more frequently (every frame, with internal throttling)
        # Get current context for reactions and music
        weather_str = self.atmosphere.current_weather.weather_type.value if self.atmosphere.current_weather else "sunny"
        time_of_day_obj = self.day_night.get_time_of_day() if hasattr(self.day_night, 'get_time_of_day') else None
        time_of_day = time_of_day_obj.value if time_of_day_obj and hasattr(time_of_day_obj, 'value') else "day"
        duck_state = self.duck.get_mood().state.value if self.duck else "neutral"

        # Update duck reactions based on weather (has internal 5-second throttle)
        self.reaction_controller.update(current_time, weather_str)

        # Update dynamic background music based on context
        music_context = get_music_context(
            weather=weather_str,
            time_of_day=time_of_day,
            duck_mood=duck_state
        )
        sound_engine.update_music(music_context)

        # Update active visitor interactions (every frame when there's a visitor)
        self._update_visitor_interactions(current_time)

        # Check for random events (every 10 seconds)
        if current_time - self._last_event_check >= 10:
            self._check_events()

            # Chance for ambient event (peaceful atmosphere)
            ambient = self.progression.get_ambient_event(chance=0.02)
            if ambient:
                self._show_message_if_no_menu(ambient, duration=3.0, category="event")

            self._last_event_check = current_time

        # Random contextual duck comments (every ~45 seconds when idle)
        if current_time - self._last_random_comment_time >= self._random_comment_interval:
            if not self._duck_traveling and not self._duck_exploring and not self._duck_building:
                # 25% chance to make a contextual comment
                if random.random() < 0.25:
                    self._make_contextual_comment()
            self._last_random_comment_time = current_time

        # Check for pending visitor reaction comment (Cheese responding to friend)
        if self._pending_visitor_comment and current_time >= self._pending_visitor_comment_time:
            self._show_message_if_no_menu(self._pending_visitor_comment, duration=4.0, category="duck")
            duck_sounds.quack("content")
            self._pending_visitor_comment = None

        # Check for pending weather reaction comment (Cheese reacting to weather)
        if self._pending_weather_comment and current_time >= self._pending_weather_comment_time:
            self._show_message_if_no_menu(self._pending_weather_comment, duration=4.0, category="duck")
            duck_sounds.quack("content")
            self._pending_weather_comment = None

        # Autonomous behavior (skip if duck is busy traveling/exploring/building/dreaming)
        if self.behavior_ai and not self._duck_traveling and not self._duck_exploring and not self._duck_building and not self._dream_active:
            # Check current location - structures and items only exist at Home Pond
            current_location = None
            if hasattr(self, 'exploration') and self.exploration and self.exploration.current_area:
                current_location = self.exploration.current_area.name
            is_at_home = current_location is None or current_location == "Home Pond"

            # Update behavior AI context with available structures and weather
            available_structures = set()
            structure_positions = {}
            placed_items = []

            # Only provide structures and items when at Home Pond
            if is_at_home:
                for structure in self.building.structures:
                    if structure.status.value == "complete":
                        available_structures.add(structure.blueprint_id)
                        # Get playfield position for this structure
                        pos = self.building.get_structure_position(structure.blueprint_id)
                        if pos:
                            structure_positions[structure.blueprint_id] = pos
                placed_items = self.habitat.placed_items

            # Check for bad weather
            is_bad_weather = False
            weather_type = None
            if self.atmosphere.current_weather:
                weather_type = self.atmosphere.current_weather.weather_type.value
                is_bad_weather = weather_type in ["rainy", "stormy", "snowy"]

            self.behavior_ai.set_context(
                available_structures=available_structures,
                is_bad_weather=is_bad_weather,
                weather_type=weather_type,
                structure_positions=structure_positions,
                placed_items=placed_items  # Only pass items when at Home Pond
            )

            # Check if there's a pending item interaction from AI
            selected_item = self.behavior_ai.get_selected_item()
            if selected_item and self.behavior_ai.has_pending_movement():
                # Don't interrupt if duck is currently doing another AI action
                # (e.g., don't interrupt sleeping to play with a toy)
                if self.behavior_ai._current_action and current_time < self.behavior_ai._action_end_time:
                    # Cancel the pending item selection, let current action finish
                    self.behavior_ai.clear_selected_item()
                    self.behavior_ai._movement_requested = False
                else:
                    # AI selected an item-based action - use the interaction controller
                    self._execute_item_interaction(selected_item, source=InteractionSource.AI_AUTONOMOUS)
                    self.behavior_ai.clear_selected_item()
                    self.behavior_ai._movement_requested = False
                    return  # Skip other AI processing for this tick

            # Check if there's a pending movement we need to handle
            if self.behavior_ai.has_pending_movement():
                target = self.behavior_ai.get_pending_movement_target()
                if target:
                    # Request duck to move to the structure
                    def on_reach_structure(data):
                        # Duck reached the structure, perform the action
                        result = self.behavior_ai.complete_movement(self.duck, time.time())
                        if result:
                            # Update visual state based on action
                            if result.action.value in ["nap", "sleep", "nap_in_nest"]:
                                self.renderer.set_duck_state("sleeping", duration=result.duration)
                            elif result.action.value in ["use_bird_bath", "splash"]:
                                self.renderer.set_duck_state("playing", duration=result.duration)
                            elif result.action.value in ["hide_in_shelter"]:
                                self.renderer.set_duck_state("scared", duration=result.duration)
                            elif result.action.value in ["preen", "admire_garden"]:
                                self.renderer.set_duck_state("preening", duration=result.duration)
                    
                    self.renderer.duck_pos.move_to(
                        target[0], target[1],
                        callback=on_reach_structure,
                        callback_data=None
                    )
                    # Clear the pending flag so we don't trigger again
                    self.behavior_ai._movement_requested = False
            else:
                result = self.behavior_ai.perform_action(self.duck, current_time)
                if result:
                    # Check if this action needs movement (behavior_ai will set pending)
                    if self.behavior_ai.has_pending_movement():
                        # Movement will be handled on next update
                        pass
                    else:
                        self.duck.set_action_message(result.message, duration=result.duration)

                        # Update visual state based on action
                        if result.action.value in ["nap", "sleep", "nap_in_nest"]:
                            self.renderer.set_duck_state("sleeping", duration=result.duration)
                        elif result.action.value in ["waddle", "look_around", "chase_bug"]:
                            self.renderer.set_duck_state("walking")
                        elif result.action.value in ["splash", "wiggle", "flap_wings", "use_bird_bath"]:
                            self.renderer.set_duck_state("playing", duration=result.duration)
                        elif result.action.value in ["hide_in_shelter"]:
                            self.renderer.set_duck_state("scared", duration=result.duration)

                        # Show closeup for emotive actions
                        emotive_actions = ["stare_blankly", "trip", "quack", "wiggle", "flap_wings",
                                           "nap_in_nest", "hide_in_shelter", "use_bird_bath",
                                           "play_with_toy", "splash_in_water", "rest_on_furniture"]
                        if result.action.value in emotive_actions:
                            self.renderer.show_closeup(result.action.value, 1.5)

                        # Play quack sound when duck talks to itself or does vocal actions
                        vocal_actions = ["quack", "look_around", "chase_bug", "trip", "wiggle", "splash",
                                         "play_with_toy", "splash_in_water"]
                        if result.action.value in vocal_actions:
                            mood = self.duck.get_mood().state.value
                            duck_sounds.quack(mood)

        # Duck interacts with nearby habitat items (10% chance per update)
        self._check_item_interaction(current_time)

        # Check crafting progress (every 2 seconds)
        if current_time - self._last_craft_check >= 2:
            self._update_crafting_progress()
            self._last_craft_check = current_time

        # Check building progress (every 5 seconds)
        if current_time - self._last_build_check >= 5:
            self._update_building_progress()
            self._last_build_check = current_time

        # Apply weather damage to structures (every 60 seconds during bad weather)
        if current_time - self._last_build_check >= 60:
            self._apply_weather_damage_to_structures()

        # Auto-save every 60 seconds
        if current_time - self._last_save >= 60:
            self._save_game()
            self._last_save = current_time

    def _update_visitor_interactions(self, current_time: float):
        """Update visitor movement, dialogue, and interactions."""
        if not self.friends.current_visit or not self.duck:
            return
        
        from world.friends import visitor_animator
        from datetime import datetime
        
        friend = self.friends.get_friend_by_id(self.friends.current_visit.friend_id)
        if not friend:
            return
        
        # Ensure visitor animator has the correct friend name set
        # This guards against race conditions where visit starts before set_visitor is called
        personality = friend.personality.value if hasattr(friend.personality, 'value') else str(friend.personality)
        if visitor_animator._friend_name != friend.name or visitor_animator._personality != personality.lower():
            friendship_level = friend.friendship_level.value if hasattr(friend.friendship_level, 'value') else str(friend.friendship_level)
            unlocked_topics = set(friend.unlocked_dialogue) if hasattr(friend, 'unlocked_dialogue') else set()
            shared_experiences = getattr(friend, 'shared_experiences', [])
            shared_memories = list(shared_experiences)[:5] if shared_experiences else []
            visitor_animator.set_visitor(
                personality, 
                friend.name,
                friendship_level,
                friend.times_visited,
                unlocked_topics,
                duck_ref=self.duck,
                shared_memories=shared_memories,
            )
        
        # Get duck's position for visitor to follow/approach
        duck_x = self.renderer.duck_pos.x
        duck_y = self.renderer.duck_pos.y
        
        # Update visitor animation and movement
        frame_changed, _ = visitor_animator.update(current_time, duck_x, duck_y)
        
        # Check for random dialogue from visitor
        dialogue = visitor_animator.get_random_dialogue(self.duck.name, current_time)
        if dialogue:
            self._show_message_if_no_menu(dialogue, duration=5.0, category="friend")
            
            # Schedule Cheese's response to the visitor's dialogue
            # friend.personality may be an enum, so convert to string
            personality = friend.personality if hasattr(friend, 'personality') else "playful"
            if hasattr(personality, 'value'):
                personality = personality.value  # Convert enum to string
            elif not isinstance(personality, str):
                personality = str(personality)
            duck_response = self.contextual_dialogue.get_conversation_response(personality)
            if duck_response:
                # Schedule response after visitor finishes talking
                self._pending_visitor_comment = f"{self.duck.name}: {duck_response}"
                self._pending_visitor_comment_time = current_time + 5.5  # After visitor's message duration
        
        # Comment on items/structures the visitor sees (only once per item)
        if visitor_animator.is_near_duck():
            # Comment on placed items
            for item in self.habitat.placed_items:
                item_id = item.item_id if hasattr(item, 'item_id') else str(item)
                item_name = item.name if hasattr(item, 'name') else item_id
                comment = visitor_animator.get_item_comment(item_id, item_name)
                if comment:
                    self._show_message_if_no_menu(comment, duration=4.0, category="friend")
                    break  # Only one comment at a time
            
            # Comment on cosmetics
            for slot, cosmetic_id in self.habitat.equipped_cosmetics.items():
                if cosmetic_id:
                    comment = visitor_animator.get_cosmetic_comment(self.duck.name, cosmetic_id)
                    if comment:
                        self._show_message_if_no_menu(comment, duration=4.0, category="friend")
                        break
            
            # Comment on built structures
            for structure in self.building.structures:
                if structure.status.value == "complete":
                    comment = visitor_animator.get_item_comment(structure.blueprint_id, structure.blueprint_id)
                    if comment:
                        self._show_message_if_no_menu(comment, duration=4.0, category="friend")
                        break
        
        # Check if visit should end (time-based or conversation complete)
        visit_start = datetime.fromisoformat(self.friends.current_visit.started_at)
        elapsed_minutes = (datetime.now() - visit_start).total_seconds() / 60
        
        # Visitor leaves when: time is up OR conversation is complete (whichever comes first)
        conversation_done = visitor_animator.is_conversation_complete()
        time_up = elapsed_minutes >= self.friends.current_visit.duration_minutes
        
        if time_up or conversation_done:
            # Visitor is leaving
            if not visitor_animator._is_leaving:
                # Save unlocked topics before leaving
                new_topics = visitor_animator.get_unlocked_topics()
                if new_topics and friend:
                    for topic in new_topics:
                        if topic not in friend.unlocked_dialogue:
                            friend.unlocked_dialogue.append(topic)
                
                visitor_animator.start_leaving()
                farewell = visitor_animator.get_farewell(self.duck.name)
                self._show_message_if_no_menu(farewell, duration=5.0, category="friend")
                duck_sounds.quack("happy")
                # Trigger friend departure reaction animation
                self.reaction_controller.trigger_friend_reaction("departure", time.time())
            
            # Check if off screen (visitor moves right toward x=70)
            pos_x, _ = visitor_animator.get_position()
            if pos_x >= 65:
                # End the visit
                self.friends.end_visit()
                self._show_message_if_no_menu(f"*{friend.name} waddles away happily*", duration=3.0, category="friend")

    def _update_crafting_progress(self):
        """Update crafting progress and complete if ready."""
        if not self.crafting._current_craft:
            return

        result = self.crafting.check_crafting()

        if result.get("completed"):
            item_id = result.get("result_item")
            quantity = result.get("quantity", 1)

            # Add crafted item to materials inventory
            if item_id in MATERIALS:
                self.materials.add_material(item_id, quantity)
            else:
                # It's a tool or other item - add to tool list
                pass

            self.renderer.show_message(
                f"* Crafting Complete! *\n\n"
                f"Created: {item_id.replace('_', ' ').title()} x{quantity}",
                duration=4.0
            )
            sound_engine.play_sound("craft_complete")
            new_level = self.progression.add_xp(15, "crafting")
            if new_level:
                self._on_level_up(new_level)

            # Crafting achievements
            self._unlock_achievement("first_craft")
            
            # Check for tool crafting
            from world.crafting import RECIPES, CraftingCategory
            recipe = RECIPES.get(item_id)
            if recipe and recipe.category == CraftingCategory.TOOL:
                self._unlock_achievement("craft_tool")
            
            # Check for crafting milestones
            total_crafted = sum(self.crafting.crafted_count.values())
            if total_crafted >= 10:
                self._unlock_achievement("craft_10")
            
            # Check for crafting master
            if self.crafting.crafting_skill >= 5:
                self._unlock_achievement("crafting_master")


            # Update challenge and quest progress for crafting
            self.challenges.update_progress("craft", 1)
            self._process_quest_updates("craft", item_id, 1)

    def _update_building_progress(self):
        """Update building progress if actively building."""
        if not self.building._current_build:
            return

        result = self.building.update_building(self.materials)

        if result.get("completed"):
            bp_id = result.get("blueprint_id")
            bp = BLUEPRINTS.get(bp_id)
            name = bp.name if bp else bp_id.replace("_", " ").title()

            self.renderer.show_message(
                f"[=] Building Complete! [=]\n\n"
                f"Built: {name}\n"
                f"Check [R] menu to see your structures!",
                duration=5.0
            )
            sound_engine.play_sound("build_complete")
            new_level = self.progression.add_xp(50, "building")
            if new_level:
                self._on_level_up(new_level)

            # Building achievements
            self._unlock_achievement("first_build")
            
            # Check structure type
            from world.building import StructureType
            if bp:
                if bp.structure_type == StructureType.NEST:
                    self._unlock_achievement("build_nest")
                elif bp.structure_type == StructureType.HOUSE:
                    self._unlock_achievement("build_house")
            
            # Check building milestones
            if self.building.structures_built >= 5:
                self._unlock_achievement("build_5")
            
            # Check for building master
            if self.building.building_skill >= 5:
                self._unlock_achievement("building_master")


            # Update challenge and quest progress for building
            self.challenges.update_progress("build", 1)
            self._process_quest_updates("build", bp_id, 1)

        elif result.get("stage_completed"):
            stage = result.get("current_stage", 0)
            stage_names = ["Foundation", "Frame", "Walls", "Roof", "Finishing"]
            name = stage_names[min(stage, 4)]
            self.renderer.show_message(f"# {name} complete! Continue building...", duration=2.0)

    def _apply_weather_damage_to_structures(self):
        """Apply weather damage to structures during bad weather."""
        if not self.atmosphere.current_weather:
            return

        weather_type = self.atmosphere.current_weather.weather_type
        damaged = self.building.apply_weather_damage(weather_type)

        for structure in damaged:
            bp = BLUEPRINTS.get(structure.blueprint_id)
            name = bp.name if bp else "Structure"
            health = int((structure.durability / structure.max_durability) * 100)

            if structure.status.value == "damaged":
                self.renderer.show_message(
                    f"! {name} damaged by weather! ({health}%)\n"
                    f"Repair with [R] menu.",
                    duration=3.0
                )
            elif structure.status.value == "destroyed":
                self.renderer.show_message(
                    f"</3 {name} destroyed by weather!",
                    duration=4.0
                )

    def _check_item_interaction(self, current_time: float):
        """Check if duck should interact with nearby placed items (proximity trigger)."""
        import random

        # Only trigger proximity interactions at Home Pond
        current_location = None
        if hasattr(self, 'exploration') and self.exploration and self.exploration.current_area:
            current_location = self.exploration.current_area.name
        if current_location is not None and current_location != "Home Pond":
            return

        # 3% chance per tick, and only if not already interacting
        if not self.duck or not hasattr(self, 'habitat') or random.random() > 0.03:
            return

        # Don't trigger if already interacting
        if self.interaction_controller.is_interacting():
            return

        # Don't interrupt ongoing AI actions (like sleeping, napping, etc.)
        # Check if behavior_ai has a current action in progress
        if hasattr(self, 'behavior_ai') and self.behavior_ai._current_action:
            if current_time < self.behavior_ai._action_end_time:
                return  # AI action still in progress, don't interrupt

        # Also check duck's current_action (backup check)
        if self.duck.current_action:
            if hasattr(self.duck, '_action_end_time') and current_time < self.duck._action_end_time:
                return  # Duck still busy with an action

        # Get duck position in habitat coordinates
        field_width = self.renderer.duck_pos.field_width
        field_height = self.renderer.duck_pos.field_height
        duck_x = int(self.renderer.duck_pos.x * 20 / field_width)
        duck_y = int(self.renderer.duck_pos.y * 12 / field_height)

        # Find nearby items
        nearby = self.habitat.get_nearby_items(duck_x, duck_y, radius=3)
        if not nearby:
            return

        # Pick a random nearby item to interact with
        item = random.choice(nearby)

        # Check cooldown (don't interact with same item too often)
        if current_time - item.last_interaction < 30:  # 30 second cooldown
            return

        # Special handling for boombox - toggle music directly (no walk needed)
        if item.item_id == "toy_boombox":
            self._toggle_boombox_music()
            self.habitat.mark_interaction(item, current_time)
            return

        # Use the unified interaction controller - duck will walk to item first
        # This ensures animation only plays AFTER duck reaches the item
        from world.interaction_controller import InteractionSource
        self._execute_item_interaction(item.item_id, source=InteractionSource.PROXIMITY)

    def _check_secret_achievements(self):
        """Check for session-based and mood-based secret achievements."""
        if not self.duck:
            return

        current_time = time.time()
        mood = self.duck.get_mood()
        needs = self.duck.needs

        # Check early bird (playing before 6 AM)
        hour = datetime.now().hour
        if hour < 6:
            self.goals._check_secret_goal("early_bird")

        # Check marathon session (30 minutes)
        session_minutes = (current_time - self._session_start) / 60
        if session_minutes >= 30:
            self.goals._check_secret_goal("marathon")

        # Check zen master (ecstatic mood for 5 minutes)
        if mood.state.value == "ecstatic":
            if self._ecstatic_start is None:
                self._ecstatic_start = current_time
            elif current_time - self._ecstatic_start >= 300:  # 5 minutes
                self.goals._check_secret_goal("zen_master")
        else:
            self._ecstatic_start = None

        # Check perfectionist (all needs above 80 for 10 minutes)
        all_high = (needs.hunger >= 80 and needs.energy >= 80 and
                   needs.fun >= 80 and needs.cleanliness >= 80 and
                   needs.social >= 80)
        if all_high:
            if self._perfect_care_start is None:
                self._perfect_care_start = current_time
            elif current_time - self._perfect_care_start >= 600:  # 10 minutes
                self.goals._check_secret_goal("perfect_care")
        else:
            self._perfect_care_start = None

        # Check streak milestones
        if self.progression.current_streak >= 7:
            self.goals._check_secret_goal("week_streak")
        if self.progression.current_streak >= 30:
            self.goals._check_secret_goal("month_streak")

        # Check holiday spirit
        special_event = self.events.check_special_day_events()
        if special_event:
            self.goals._check_secret_goal("holiday_play")

    def _check_events(self):
        """Check for random events."""
        if not self.duck:
            return

        # Check special day events first
        special_event = self.events.check_special_day_events()
        if special_event:
            self.renderer.show_message(special_event.message, duration=5.0, category="event")
            self.events.apply_event(self.duck, special_event)
            return

        event = self.events.check_random_events(self.duck)
        if event:
            # Apply event effects
            changes = self.events.apply_event(self.duck, event)

            # Trigger duck reaction animation for this event
            self.reaction_controller.trigger_event_reaction(event.id, time.time())

            # Start event animation if available
            if event.has_animation and event.id in ANIMATED_EVENTS:
                self._start_event_animation(event.id)
                # Show message after a short delay for animated events
                self.renderer.show_message(event.message, duration=5.0, category="duck")
            else:
                # Show event message immediately for non-animated events
                self.renderer.show_message(event.message, duration=4.0, category="duck")

            # Record in memory
            self.duck.memory.add_event(
                event.name,
                event.description,
                importance=5,
                emotional_value=event.mood_change
            )

            # Play sound if specified
            if event.sound:
                if event.sound == "quack":
                    duck_sounds.quack()
                elif event.sound == "alert":
                    duck_sounds.alert()
                elif event.sound == "eat":
                    duck_sounds.eat()

            # Play quack when duck finds something
            if "found" in event.name.lower() or "find" in event.name.lower():
                duck_sounds.quack("happy")

            # Random chance to get an item
            if event.mood_change > 0 and "found" in event.name.lower():
                item_id = get_random_item("common")
                if item_id and self.inventory.add_item(item_id):
                    item = get_item_info(item_id)
                    self.renderer.show_message(f"Found: {item.name}!", duration=3.0)

    def _start_event_animation(self, event_id: str):
        """Start an event animation."""
        # Get playfield dimensions from renderer
        playfield_width = 60  # Default, will be updated
        playfield_height = 15
        
        # Create the animator
        animator = create_event_animator(event_id, playfield_width, playfield_height)
        if animator:
            animator.start()
            self._event_animators.append(animator)

    def _make_contextual_comment(self):
        """Make a random contextual comment based on current game state.
        
        Uses DuckBrain for Seaman-style observations and callbacks when available,
        falling back to the contextual dialogue system otherwise.
        """
        if not self.duck:
            return
        
        # Don't interrupt open menus or overlays
        if self._is_any_menu_open():
            return
        
        comment = None
        
        # Try to get a DuckBrain comment first (Seaman-style)
        if self.duck_brain:
            # Decide what type of comment to make
            roll = random.random()
            
            if roll < 0.25:
                # 25% chance: Callback to a past event or conversation
                comment = self.duck_brain.get_callback()
            elif roll < 0.50:
                # 25% chance: Idle philosophical thought
                comment = self.duck_brain.get_idle_thought()
            elif roll < 0.70:
                # 20% chance: Observation about current situation
                # Build context
                context = {}
                if self.atmosphere.current_weather:
                    context["weather"] = self.atmosphere.current_weather.weather_type.value
                if self.exploration.current_area:
                    context["location"] = self.exploration.current_area.name
                context["time_of_day"] = self.clock.get_time_of_day()
                context["mood"] = self.duck.get_mood().state.value if self.duck else "content"
                comment = self.duck_brain.get_observation(context)
            elif roll < 0.85:
                # 15% chance: Maybe ask a question (to learn about player)
                question_result = self.duck_brain.get_question()
                if question_result:
                    # get_question returns (question_id, question_text) tuple
                    comment = question_result[1]
            # 15% chance: No comment (silence is golden)
        
        # Fallback to original contextual dialogue system
        if not comment:
            # Get current context
            weather = None
            if self.atmosphere.current_weather:
                weather = self.atmosphere.current_weather.weather_type.value
            
            # Check for visitor
            visitor_personality = None
            if self.friends.current_visit:
                friend = self.friends.get_friend_by_id(self.friends.current_visit.friend_id)
                if friend:
                    visitor_personality = friend.personality.value if hasattr(friend.personality, 'value') else str(friend.personality)
            
            # Get time of day
            time_of_day = None
            time_obj = self.day_night.get_time_of_day() if hasattr(self.day_night, 'get_time_of_day') else None
            if time_obj and hasattr(time_obj, 'value'):
                time_of_day = time_obj.value
            
            # Get a contextual comment
            comment = self.contextual_dialogue.get_contextual_comment(
                weather=weather,
                visitor_personality=visitor_personality,
                time_of_day=time_of_day
            )
        
        if comment:
            self.renderer.show_message(comment, duration=4.0, category="duck")
            # Play a soft quack
            duck_sounds.quack("content")

    def _get_duck_weather_reaction(self, weather_type: str) -> Optional[str]:
        """Get duck's reaction to weather change."""
        return self.contextual_dialogue.get_weather_comment(weather_type)

    def _animate_weather_reaction(self, weather_type: str):
        """Animate duck reacting to weather change with movement."""
        if self._interaction_phase != InteractionPhase.IDLE:
            return
        
        field_width = self.renderer.duck_pos.field_width
        field_height = self.renderer.duck_pos.field_height
        
        # Different movement patterns for different weather
        if weather_type == "rainy":
            # Waddle to a "puddle" (random low spot on playfield)
            puddle_x = random.randint(5, field_width - 8)
            puddle_y = field_height - random.randint(2, 4)  # Near bottom
            self.renderer.duck_pos.move_to(puddle_x, puddle_y, 
                callback=self._on_reached_puddle, callback_data=None, save_original=False)
        elif weather_type == "snowy":
            # Waddle around excitedly looking at snow
            snow_x = random.randint(4, field_width - 6)
            snow_y = random.randint(2, field_height - 3)
            self.renderer.duck_pos.move_to(snow_x, snow_y, save_original=False)
        elif weather_type == "sunny":
            # Find a sunny spot to bask
            sun_x = field_width // 2 + random.randint(-5, 5)
            sun_y = random.randint(2, 5)  # Upper part of screen (toward sun)
            self.renderer.duck_pos.move_to(sun_x, sun_y, save_original=False)
        elif weather_type == "windy":
            # Duck gets pushed by wind (move in wind direction)
            self.renderer.duck_pos.move_to(
                min(field_width - 6, self.renderer.duck_pos.x + 8),  # Wind pushes right
                self.renderer.duck_pos.y,
                save_original=False
            )
        elif weather_type == "rainbow":
            # Duck looks up and moves to center to admire
            self.renderer.duck_pos.move_to(field_width // 2, field_height // 2, save_original=False)

    def _on_reached_puddle(self, data):
        """Callback when duck reaches a puddle in the rain."""
        # Set duck to splashing state
        self.renderer.duck_pos.set_state("splashing", duration=3.0)
        self.renderer.show_message("*splish splash splosh!*", duration=2.5, category="duck")
        duck_sounds.play()  # Splash sound

    def _get_duck_visitor_reaction(self, personality: str) -> Optional[str]:
        """Get duck's reaction to a visitor."""
        return self.contextual_dialogue.get_visitor_comment(personality)

    def _duck_approach_visitor(self):
        """Make duck waddle toward the arriving visitor (with InteractionPhase tracking)."""
        # Check if we're already in an interaction
        if self._interaction_phase != InteractionPhase.IDLE:
            return
        
        from world.friends import visitor_animator
        
        # Get the current friend being visited
        if not self.friends.current_visit:
            return
        
        friend = self.friends.get_friend_by_id(self.friends.current_visit.friend_id)
        if not friend:
            return
        
        # Get visitor's current position
        visitor_x, visitor_y = visitor_animator.get_position()
        
        # Move duck toward visitor (but not all the way - leave some space)
        field_width = self.renderer.duck_pos.field_width
        field_height = self.renderer.duck_pos.field_height
        
        # Clamp visitor position to field bounds
        target_x = max(4, min(visitor_x - 4, field_width - 8))  # Stop a bit before visitor
        target_y = max(2, min(visitor_y, field_height - 4))
        
        # Set interaction state
        self._interaction_phase = InteractionPhase.MOVING_TO_TARGET
        self._interaction_target_friend = friend.id
        self._interaction_target_pos = (target_x, target_y)
        
        # Start the approach with callback
        self.renderer.duck_pos.move_to(
            target_x, target_y,
            callback=self._on_arrived_at_friend,
            callback_data={"friend_id": friend.id, "friend_name": friend.name},
            save_original=False
        )

    def _on_arrived_at_friend(self, data: dict):
        """Callback when duck arrives at friend's position."""
        friend_name = data.get("friend_name", "friend")
        
        # Set duck to excited/social state
        self._interaction_phase = InteractionPhase.INTERACTING
        self.renderer.duck_pos.set_state("excited", duration=2.0)
        
        # Show greeting reaction
        self.renderer.show_message(f"*happy quack* Hi {friend_name}!", duration=2.5, category="duck")
        duck_sounds.quack("happy")
        
        # Reset interaction phase after a short delay (state duration handles this)
        self._interaction_target_friend = None
        self._interaction_target_pos = None
        self._interaction_phase = InteractionPhase.IDLE

    def _update_event_animations(self):
        """Update all active event animations."""
        if not self._event_animators:
            return
            
        # Get duck position for interaction targeting
        duck_x = self.renderer.duck_pos.x
        duck_y = self.renderer.duck_pos.y
        
        # Update each animator and remove finished ones
        still_running = []
        for animator in self._event_animators:
            if animator.update(duck_x, duck_y):
                still_running.append(animator)
                
                # Check if duck should approach this event (butterflies, curious events)
                if (hasattr(animator, 'event_id') and 
                    animator.event_id in ["butterfly", "found_shiny", "rainbow"] and
                    self._interaction_phase == InteractionPhase.IDLE and
                    not self.renderer.duck_pos._is_directed_movement):
                    # Get animator's position
                    if hasattr(animator, 'x') and hasattr(animator, 'y'):
                        event_x = int(animator.x)
                        event_y = int(animator.y)
                        # Only approach if event is reasonably close
                        distance = abs(duck_x - event_x) + abs(duck_y - event_y)
                        if distance > 5 and distance < 20:
                            # ~0.1% per frame at 60 FPS = ~6% chance per second
                            if random.random() < 0.001:
                                self._duck_approach_event(event_x, event_y, animator.event_id)
                
        self._event_animators = still_running

    def _duck_approach_event(self, event_x: int, event_y: int, event_id: str):
        """Make duck curiously approach an environmental event."""
        field_width = self.renderer.duck_pos.field_width
        field_height = self.renderer.duck_pos.field_height
        
        # Approach to near the event (not right on top)
        target_x = max(3, min(event_x - 2, field_width - 6))
        target_y = max(2, min(event_y, field_height - 4))
        
        # Show curious message
        event_messages = {
            "butterfly": "*notices something fluttering* Ooh!",
            "found_shiny": "*spots something glittering* What's that?!",
            "rainbow": "*looks up in wonder* So pretty!",
            "breeze": "*feels the wind* Wheee!",
        }
        msg = event_messages.get(event_id, "*curious quack*")
        self.renderer.show_message(msg, duration=2.0)
        
        # Move toward event (no callback needed)
        self.renderer.duck_pos.move_to(target_x, target_y, save_original=False)

    def _on_growth_stage_change(self, old_stage: str, new_stage: str):
        """Handle growth stage transition."""
        if not self.duck:
            return

        # Play level up sound
        duck_sounds.level_up()

        # Show effect
        self.renderer.show_effect("sparkle", 2.0)

        # Get growth reaction
        reaction = self.conversation.get_growth_reaction(self.duck, new_stage)
        self.renderer.show_message(f"Evolved to {self.duck.get_growth_stage_display()}!", duration=3.0)
        self.renderer.show_message(reaction, duration=4.0)

        # Record milestone
        self.duck.memory.add_milestone(
            f"growth_{new_stage}",
            f"Grew from {old_stage} to {new_stage}!"
        )

        # Record in diary (narrative storytelling)
        milestone_map = {
            "duckling": "first_steps",
            "teen": "became_teen",
            "adult": "became_adult",
            "elder": "became_elder",
        }
        if new_stage in milestone_map:
            self.diary.record_milestone(milestone_map[new_stage])

        # Unlock achievement
        self._unlock_achievement(f"reach_{new_stage}")


        # Trigger growth events
        self.events.check_triggered_events(self.duck, "stage_change")

    def _render(self):
        """Render the current state."""
        if self._state == "title":
            has_save = self.save_manager.save_exists()
            self.renderer._render_title_screen(
                menu_index=self._title_menu_index,
                has_save=has_save,
                update_status=self._title_update_status,
                version=self._game_version,
                terminal_options=self._terminal_options,
                terminal_index=self._terminal_selection_index
            )
        elif self._state == "offline_summary" and self._pending_offline_summary:
            summary = self._pending_offline_summary
            self.renderer.render_offline_summary(
                summary["name"],
                summary["hours"],
                summary["changes"],
            )
        elif self._state == "playing":
            self.renderer.render_frame(self)
            # Keep menus persistent - re-render if a menu is open
            self._maintain_open_menus()

    def _maintain_open_menus(self):
        """Re-render any open menu to keep it visible. Prevents softlock from message overlay changes."""
        if self._tricks_menu_open:
            self._render_tricks_menu()
        elif self._titles_menu_open:
            self._render_titles_menu()
        elif self._collectibles_menu_open:
            self._render_collectibles_menu()
        elif self._secrets_menu_open:
            self._render_secrets_menu()
        elif self._garden_menu_open:
            self._render_garden_menu()
        elif self._prestige_menu_open:
            self._render_prestige_menu()
        elif self._save_slots_menu_open:
            self._render_save_slots_menu()
        elif self._trading_menu_open:
            self._render_trading_menu()
        elif self._decorations_menu_open:
            self._render_decorations_menu()
        elif self._scrapbook_menu_open:
            self._render_scrapbook()
        elif self._enhanced_diary_open:
            self._render_enhanced_diary()
        elif self._crafting_menu_open:
            self._update_crafting_menu_display()
        elif self._building_menu_open:
            self._update_building_menu_display()
        elif self._areas_menu_open:
            self._update_areas_menu_display()
        elif self._use_menu_open:
            self._update_use_menu_display()
        elif self._minigames_menu_open:
            self._update_minigames_menu_display()
        elif self._quests_menu_open:
            self._update_quests_menu_display()
        elif self._weather_menu_open:
            self._update_weather_menu_display()
        elif self._treasure_menu_open:
            self._update_treasure_menu_display()
        elif self._festival_menu_open:
            self._update_festival_menu_display()
        elif self._settings_menu_open:
            self._render_settings_menu()
        elif self._main_menu_open:
            self._update_main_menu_display()
        elif self._debug_menu_open:
            self._show_debug_menu()

    def _handle_title_input(self, action: GameAction, key=None):
        """Handle input on the title screen menu."""
        has_save = self.save_manager.save_exists()
        
        # Handle new game confirmation dialog
        if self._title_confirm_new_game:
            if key:
                key_str = str(key).lower()
                if key_str == 'y':
                    # Confirmed - delete save and start new game
                    self.save_manager.delete_save()
                    self._title_confirm_new_game = False
                    self._title_update_status = ""
                    self._start_new_game()
                elif key_str == 'n' or (key.name and key.name == 'KEY_ESCAPE'):
                    # Cancelled
                    self._title_confirm_new_game = False
                    self._title_update_status = ""
            return
        
        # Calculate max menu index based on whether save exists
        # Menu: Continue (if save), New Game, Check for Updates, Quit
        max_index = 3 if has_save else 2
        
        # Handle navigation
        if key and key.name == "KEY_UP":
            self._title_menu_index = max(0, self._title_menu_index - 1)
            sound_engine.play_sound("menu_move")
            return
            
        if key and key.name == "KEY_DOWN":
            self._title_menu_index = min(max_index, self._title_menu_index + 1)
            sound_engine.play_sound("menu_move")
            return
        
        # Handle terminal selector with LEFT/RIGHT arrows
        if key and key.name == "KEY_LEFT" and len(self._terminal_options) > 0:
            self._terminal_selection_index = (self._terminal_selection_index - 1) % len(self._terminal_options)
            sound_engine.play_sound("menu_move")
            # Auto-save terminal preference
            from core.settings import settings_manager
            selected_cmd = self._terminal_options[self._terminal_selection_index][0]
            settings_manager.set_value("system", "preferred_terminal", selected_cmd)
            settings_manager.save()
            return
        
        if key and key.name == "KEY_RIGHT" and len(self._terminal_options) > 0:
            self._terminal_selection_index = (self._terminal_selection_index + 1) % len(self._terminal_options)
            sound_engine.play_sound("menu_move")
            # Auto-save terminal preference
            from core.settings import settings_manager
            selected_cmd = self._terminal_options[self._terminal_selection_index][0]
            settings_manager.set_value("system", "preferred_terminal", selected_cmd)
            settings_manager.save()
            return
        
        # Handle selection
        if action == GameAction.CONFIRM or (key and key.name == "KEY_ENTER"):
            sound_engine.play_sound("menu_select")
            
            if has_save:
                # Menu: Continue, New Game, Check for Updates, Quit
                if self._title_menu_index == 0:
                    # Continue - load existing save
                    self._load_game()
                elif self._title_menu_index == 1:
                    # New Game - warn about overwriting save
                    self._title_confirm_new_game = True
                    self._title_update_status = "Start new game? This will ERASE your save! [Y/N]"
                elif self._title_menu_index == 2:
                    # Check for Updates
                    self._check_for_updates_async()
                elif self._title_menu_index == 3:
                    # Quit
                    self._running = False
            else:
                # Menu: New Game, Check for Updates, Quit
                if self._title_menu_index == 0:
                    # New Game
                    self._start_new_game()
                elif self._title_menu_index == 1:
                    # Check for Updates
                    self._check_for_updates_async()
                elif self._title_menu_index == 2:
                    # Quit
                    self._running = False
            return
        
        # Handle [U] key to download/install update
        if key:
            key_str = str(key).lower()
            if key_str == 'u' and self._update_available_info and not self._update_in_progress:
                sound_engine.play_sound("menu_select")
                self._download_and_apply_update()
                return
            
            # Handle [R] key to restart game after update
            if key_str == 'r' and "restart" in self._title_update_status.lower():
                self._restart_game()
                return
    
    def _check_for_updates_async(self):
        """Check for updates in background and update status message."""
        self._title_update_status = "Checking for updates..."
        try:
            update_info = self._game_updater.check_for_updates()
            self._title_update_status = self._game_updater.get_status_message(update_info.status)
            if update_info.status.value == "update_available":
                self._update_available_info = update_info
                # All installs can now be updated with [U]
                self._title_update_status = f"Update v{update_info.latest_version} available! Press [U] to install"
            else:
                self._update_available_info = None
        except Exception:
            self._title_update_status = "Could not check for updates"
            self._update_available_info = None
        self._title_checking_updates = False

    def _download_and_apply_update(self):
        """Download and apply the available update."""
        if not self._update_available_info:
            self._title_update_status = "No update available to install"
            return
        
        if self._update_in_progress:
            return
        
        self._update_in_progress = True
        
        try:
            from core.updater import UpdateStatus
            
            # Use different update method for system installs (apt/deb)
            if self._game_updater.is_system_install():
                self._title_update_status = "Building update package... Please wait..."
                result = self._game_updater.download_and_install_deb(self._update_available_info)
            else:
                self._title_update_status = "Downloading update... Please wait..."
                result = self._game_updater.download_and_apply_update(self._update_available_info)
            
            if result == UpdateStatus.UPDATE_COMPLETE:
                self._title_update_status = "Update complete! Press [R] to restart the game"
                self._update_available_info = None
            else:
                error = self._game_updater.get_last_error() or "Unknown error"
                self._title_update_status = f"Update failed: {error[:40]}"
        except Exception as e:
            self._title_update_status = f"Update failed: {str(e)[:40]}"
        finally:
            self._update_in_progress = False

    def _restart_game(self):
        """Restart the game after an update."""
        import sys
        import os
        # Re-execute the current Python script
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def _start_new_game(self):
        """Start a new game with a new duck."""
        # Stop title music (both methods to ensure it stops)
        sound_engine.stop_music()
        sound_engine.stop_background_music()
        
        self.duck = Duck.create_new()
        self.behavior_ai = BehaviorAI()
        self.inventory = Inventory()

        # Set up interaction controller references
        self.interaction_controller.set_references(
            habitat=self.habitat,
            renderer=self.renderer,
            duck=self.duck,
            on_effects_applied=self._on_interaction_effects_applied
        )
        self.goals = GoalSystem()
        self.achievements = AchievementSystem()
        self.progression = ProgressionSystem()
        self.home = DuckHome()
        
        # Reset building and add starter nest
        self.building = BuildingSystem()
        self.building.add_starter_nest()
        
        # Note: We don't add nest to playfield objects anymore since 
        # the building system structures are rendered directly

        # Give starting items
        self.inventory.add_item("bread")
        self.inventory.add_item("bread")
        self.inventory.add_item("rubber_duck")

        self._statistics = {
            "days_alive": 0,
            "times_fed": 0,
            "times_played": 0,
            "times_cleaned": 0,
            "times_petted": 0,
            "times_slept": 0,
            "conversations": 0,
        }
        self._state = "playing"
        self._last_tick = time.time()
        self._last_save = time.time()
        self._last_event_check = time.time()
        self._last_progression_check = time.time()

        # Check daily login for streak/rewards
        self._check_daily_login()

        # Welcome message - use DuckBrain greeting if available
        greeting = None
        if self.duck_brain:
            greeting = self.duck_brain.get_greeting()
        if not greeting:
            greeting = self.conversation.get_greeting(self.duck)
        self.renderer.show_message(f"Welcome, {self.duck.name}!", category="event")
        self.renderer.show_message(greeting, duration=4.0, category="duck")

        # Play welcome sound
        duck_sounds.quack("happy")

        # Start main game background music using dynamic system
        music_context = get_music_context(weather="sunny", duck_mood="content")
        sound_engine.update_music(music_context, force=True)

        # First goal
        self.goals.add_daily_goals()

        # Generate daily challenges
        self.progression.generate_daily_challenges()
        
        # Start first life chapter in enhanced diary
        self.enhanced_diary.start_life_chapter(
            title="The Beginning",
            summary=f"{self.duck.name} hatched into the world!"
        )
        self.enhanced_diary.add_chapter_event("First hatched!")
        
        # Log initial excitement emotion
        from dialogue.diary_enhanced import EmotionCategory
        self.enhanced_diary.log_emotion(EmotionCategory.EXCITEMENT, 8, trigger="hatching")

        # Initialize DuckBrain - Seaman-style persistent memory
        self.duck_brain = DuckBrain(duck_name=self.duck.name)
        self._connect_duck_brain_to_llm()
        self.duck_brain.start_session()
        
        # Record the hatching as a significant event
        self.duck_brain.process_action("hatched", "just hatched into the world")

        self._save_game()

    def _load_game(self):
        """Load an existing save."""
        data = self.save_manager.load()
        if not data:
            self._state = "title"
            self._start_title_music()
            return

        # Load duck
        duck_data = data.get("duck", {})
        self.duck = Duck.from_dict(duck_data)
        self.behavior_ai = BehaviorAI()
        self._statistics = data.get("statistics", {})

        # Load inventory
        if "inventory" in data:
            self.inventory = Inventory.from_dict(data["inventory"])
        else:
            self.inventory = Inventory()

        # Load events state
        if "events" in data:
            self.events = EventSystem.from_dict(data["events"])

        # Load goals
        if "goals" in data:
            self.goals = GoalSystem.from_dict(data["goals"])
        else:
            self.goals = GoalSystem()
            self.goals.add_daily_goals()

        # Load achievements
        if "achievements" in data:
            self.achievements = AchievementSystem.from_dict(data["achievements"])
        else:
            self.achievements = AchievementSystem()

        # Load progression system
        if "progression" in data:
            self.progression = ProgressionSystem.from_dict(data["progression"])
        else:
            self.progression = ProgressionSystem()

        # Load home customization
        if "home" in data:
            self.home = DuckHome.from_dict(data["home"])
        else:
            self.home = DuckHome()

        # Load habitat (shop items, placed items, cosmetics)
        if "habitat" in data:
            self.habitat.from_dict(data["habitat"])

        # Set up interaction controller references
        self.interaction_controller.set_references(
            habitat=self.habitat,
            renderer=self.renderer,
            duck=self.duck,
            on_effects_applied=self._on_interaction_effects_applied
        )

        # Load atmosphere (weather, visitors, fortune)
        if "atmosphere" in data:
            self.atmosphere = AtmosphereManager.from_dict(data["atmosphere"])
        else:
            self.atmosphere = AtmosphereManager()

        # Load diary (narrative journal)
        if "diary" in data:
            self.diary = DuckDiary.from_dict(data["diary"])
        else:
            self.diary = DuckDiary()
            # Record hatching for new diary
            self.diary.record_milestone("hatched")

        # Load exploration system
        if "exploration" in data:
            self.exploration = ExplorationSystem.from_dict(data["exploration"])
        else:
            self.exploration = ExplorationSystem()

        # Load materials inventory
        if "materials" in data:
            self.materials = MaterialInventory.from_dict(data["materials"])
        else:
            self.materials = MaterialInventory()

        # Load crafting system
        if "crafting" in data:
            self.crafting = CraftingSystem.from_dict(data["crafting"])
        else:
            self.crafting = CraftingSystem()

        # Load building system
        if "building" in data:
            self.building = BuildingSystem.from_dict(data["building"])
        else:
            self.building = BuildingSystem()
        
        # Cleanup any duplicate shelters from old saves
        removed = self.building.cleanup_duplicate_shelters()
        if removed:
            self._pending_messages.append(f"Cleaned up duplicate structures: {', '.join(removed)}")
        
        # Ensure there's always a starter nest
        self.building.add_starter_nest()
        
        # Note: We don't add nest to playfield objects anymore since 
        # the building system structures are rendered directly

        # Load minigames system
        if "minigames" in data:
            self.minigames = MiniGameSystem.from_dict(data["minigames"])
        else:
            self.minigames = MiniGameSystem()

        # Load dreams system
        if "dreams" in data:
            self.dreams = DreamSystem.from_dict(data["dreams"])
        else:
            self.dreams = DreamSystem()

        # ============== LOAD NEW FEATURE SYSTEMS ==============
        # Load scrapbook system
        if "scrapbook" in data:
            self.scrapbook = Scrapbook.from_dict(data["scrapbook"])
        else:
            self.scrapbook = Scrapbook()

        # Load fishing system
        if "fishing" in data:
            self.fishing = FishingMinigame.from_dict(data["fishing"])
        else:
            self.fishing = FishingMinigame()

        # Load garden system
        if "garden" in data:
            self.garden = Garden.from_dict(data["garden"])
        else:
            self.garden = Garden()

        # Load treasure system
        if "treasure" in data:
            self.treasure = TreasureHunter.from_dict(data["treasure"])
        else:
            self.treasure = TreasureHunter()

        # Load challenge system
        if "challenges" in data:
            self.challenges = ChallengeSystem.from_dict(data["challenges"])
        else:
            self.challenges = ChallengeSystem()

        # Load friendship system
        if "friends" in data:
            self.friends = FriendsSystem.from_dict(data["friends"])
        else:
            self.friends = FriendsSystem()
        self.friends.on_friendship_level_up = self._on_friendship_level_up

        # Load quest system
        if "quests" in data:
            self.quests = QuestSystem.from_dict(data["quests"])
        else:
            self.quests = QuestSystem()

        # Load festival system
        if "festivals" in data:
            self.festivals = FestivalSystem.from_dict(data["festivals"])
        else:
            self.festivals = FestivalSystem()

        # Load prestige system
        if "prestige" in data:
            self.prestige = PrestigeSystem.from_dict(data["prestige"])
        else:
            self.prestige = PrestigeSystem()

        # Load collectibles system
        if "collectibles" in data:
            self.collectibles = CollectiblesSystem.from_dict(data["collectibles"])
        else:
            self.collectibles = CollectiblesSystem()

        # Load tricks system
        if "tricks" in data:
            self.tricks = TricksSystem.from_dict(data["tricks"])
        else:
            self.tricks = TricksSystem()

        # Load decorations system
        if "decorations" in data:
            self.decorations = DecorationsSystem.from_dict(data["decorations"])
        else:
            self.decorations = DecorationsSystem()

        # Load titles system
        if "titles" in data:
            self.titles = TitlesSystem.from_dict(data["titles"])
        else:
            self.titles = TitlesSystem()

        # Load outfit system
        if "outfits" in data:
            self.outfits = OutfitManager.from_dict(data["outfits"])
        else:
            self.outfits = OutfitManager()

        # Load seasonal clothing system
        if "seasonal_clothing" in data:
            self.seasonal_clothing = SeasonalClothingSystem.from_dict(data["seasonal_clothing"])
        else:
            self.seasonal_clothing = SeasonalClothingSystem()

        # Load secrets system
        if "secrets" in data:
            self.secrets = SecretsSystem.from_dict(data["secrets"])
        else:
            self.secrets = SecretsSystem()

        # Load weather activities system
        if "weather_activities" in data:
            self.weather_activities = WeatherActivitiesSystem.from_dict(data["weather_activities"])
        else:
            self.weather_activities = WeatherActivitiesSystem()

        # Load trading system
        if "trading" in data:
            self.trading = TradingSystem.from_dict(data["trading"])
        else:
            self.trading = TradingSystem()

        # Load fortune system
        if "fortune" in data:
            self.fortune = FortuneSystem.from_dict(data["fortune"])
        else:
            self.fortune = FortuneSystem()

        # Load aging system
        if "aging" in data:
            self.aging = AgingSystem.from_dict(data["aging"])
        else:
            self.aging = AgingSystem()

        # Load extended personality system
        if "extended_personality" in data:
            self.extended_personality = ExtendedPersonalitySystem.from_dict(data["extended_personality"])
        else:
            self.extended_personality = ExtendedPersonalitySystem()

        # Load statistics system
        if "statistics_system" in data:
            self.statistics = StatisticsSystem.from_dict(data["statistics_system"])
        else:
            self.statistics = StatisticsSystem()

        # Load day/night system
        if "day_night" in data:
            self.day_night = DayNightSystem.from_dict(data["day_night"])
        else:
            self.day_night = DayNightSystem()

        # Load badges system
        if "badges" in data:
            self.badges = BadgesSystem.from_dict(data["badges"])
        else:
            self.badges = BadgesSystem()

        # Load mood visuals (stateless, no save needed)
        self.mood_visuals = MoodVisualEffects()

        # Load ambient sound system (mostly stateless)
        self.ambient = AmbientSoundSystem()

        # Load sound effects system (stateless)
        self.sound_effects = SoundEffectSystem()

        # Load mood dialogue system (stateless)
        self.mood_dialogue = MoodDialogueSystem()

        # Load enhanced diary system
        if "enhanced_diary" in data:
            self.enhanced_diary = EnhancedDiarySystem.from_dict(data["enhanced_diary"])
        else:
            self.enhanced_diary = EnhancedDiarySystem()

        # Load save slots system
        if "save_slots" in data:
            self.save_slots = SaveSlotsSystem.from_dict(data["save_slots"])
        else:
            self.save_slots = SaveSlotsSystem()
        
        # Load DuckBrain - Seaman-style persistent memory system
        if "duck_brain" in data and data["duck_brain"]:
            self.duck_brain = DuckBrain.from_dict(data["duck_brain"])
        else:
            # Create new DuckBrain with duck's name
            duck_name = self.duck.name if self.duck else "Cheese"
            self.duck_brain = DuckBrain(duck_name=duck_name)
        
        # Connect DuckBrain to LLM chat if available
        self._connect_duck_brain_to_llm()
        
        # Start a new session in DuckBrain
        self.duck_brain.start_session()
        # ============== END LOAD NEW FEATURE SYSTEMS ==============

        # Load weather history for secret goal
        self._weather_seen = set(data.get("weather_seen", []))

        # Check daily login and streak
        self._check_daily_login()

        # Check for birthday/milestone
        self._check_birthday_milestone()

        # Calculate offline progression
        last_played = data.get("last_played", datetime.now().isoformat())
        offline = self.clock.calculate_offline_time(last_played)

        if offline["hours"] > 0.016:  # More than 1 minute
            # Apply offline decay
            old_needs = self.duck.needs.to_dict()

            offline_minutes = offline["minutes"] * offline["decay_multiplier"]
            self.duck.update(offline_minutes)

            new_needs = self.duck.needs.to_dict()

            # Calculate changes for summary
            changes = {}
            for need in old_needs:
                diff = new_needs[need] - old_needs[need]
                if abs(diff) > 1:
                    changes[need] = diff

            # Show offline summary
            self._pending_offline_summary = {
                "name": self.duck.name,
                "hours": offline["hours"],
                "changes": changes,
            }
            self._state = "offline_summary"
        else:
            self._state = "playing"

        # Stop title music and start game music
        sound_engine.stop_music()
        sound_engine.stop_background_music()
        weather_str = self.atmosphere.current_weather.weather_type.value if self.atmosphere.current_weather else "sunny"
        duck_mood = self.duck.get_mood().state.value if self.duck else "content"
        music_context = get_music_context(weather=weather_str, duck_mood=duck_mood)
        sound_engine.update_music(music_context, force=True)

        self._last_tick = time.time()
        self._last_save = time.time()
        self._last_event_check = time.time()
        
        # Show welcome back - use DuckBrain greeting if available
        welcome_msg = None
        if self.duck_brain:
            welcome_msg = self.duck_brain.get_greeting()
        if welcome_msg:
            notification_manager.show(welcome_msg, "success", 3.5)
        else:
            notification_manager.show(f"Welcome back to care for {self.duck.name}!", "success", 2.5)

    def _connect_duck_brain_to_llm(self):
        """Connect DuckBrain to the LLM chat system for enhanced context."""
        try:
            from dialogue.llm_chat import get_llm_chat
            llm_chat = get_llm_chat()
            if llm_chat and self.duck_brain:
                llm_chat.set_duck_brain(self.duck_brain)
                # Also sync conversation history from DuckBrain
                recent_messages = self.duck_brain.conversation_memory.get_recent_context(20)
                history = []
                for msg in recent_messages:
                    role = "user" if msg.get("role") == "player" else "assistant"
                    history.append({"role": role, "content": msg.get("content", "")})
                llm_chat.set_conversation_history(history)
        except Exception as e:
            # Log but don't crash if LLM chat isn't available
            from game_logger import get_logger
            get_logger().debug(f"Could not connect DuckBrain to LLM: {e}")

    def _save_game(self):
        """Save the current game state."""
        if not self.duck:
            return

        save_data = {
            "duck": self.duck.to_dict(),
            "last_played": self.clock.timestamp,
            "inventory": self.inventory.to_dict(),
            "events": self.events.to_dict(),
            "goals": self.goals.to_dict(),
            "achievements": self.achievements.to_dict(),
            "progression": self.progression.to_dict(),
            "home": self.home.to_dict(),
            "habitat": self.habitat.to_dict(),
            "atmosphere": self.atmosphere.to_dict(),
            "diary": self.diary.to_dict(),
            "exploration": self.exploration.to_dict(),
            "materials": self.materials.to_dict(),
            "crafting": self.crafting.to_dict(),
            "building": self.building.to_dict(),
            "minigames": self.minigames.to_dict(),
            "dreams": self.dreams.to_dict(),
            "statistics": self._statistics,
            "weather_seen": list(self._weather_seen),
            # ============== NEW FEATURE SYSTEMS ==============
            "scrapbook": self.scrapbook.to_dict(),
            "fishing": self.fishing.to_dict(),
            "garden": self.garden.to_dict(),
            "treasure": self.treasure.to_dict(),
            "challenges": self.challenges.to_dict(),
            "friends": self.friends.to_dict(),
            "quests": self.quests.to_dict(),
            "festivals": self.festivals.to_dict(),
            "prestige": self.prestige.to_dict(),
            "collectibles": self.collectibles.to_dict(),
            "tricks": self.tricks.to_dict(),
            "decorations": self.decorations.to_dict(),
            "titles": self.titles.to_dict(),
            "outfits": self.outfits.to_dict(),
            "seasonal_clothing": self.seasonal_clothing.to_dict(),
            "secrets": self.secrets.to_dict(),
            "weather_activities": self.weather_activities.to_dict(),
            "trading": self.trading.to_dict(),
            "fortune": self.fortune.to_dict(),
            "aging": self.aging.to_dict(),
            "extended_personality": self.extended_personality.to_dict(),
            "statistics_system": self.statistics.to_dict(),
            "day_night": self.day_night.to_dict(),
            "badges": self.badges.to_dict(),
            "enhanced_diary": self.enhanced_diary.to_dict(),
            "save_slots": self.save_slots.to_dict(),
            # DuckBrain - Seaman-style persistent memory
            "duck_brain": self.duck_brain.to_dict() if self.duck_brain else None,
            # ============== END NEW FEATURE SYSTEMS ==============
        }

        self.save_manager.save(save_data)
        notification_manager.show("Game saved!", "success", 1.5)

    def _return_to_title(self):
        """Save the game and return to title screen."""
        if self.duck:
            # End DuckBrain session before saving
            if self.duck_brain:
                self.duck_brain.end_session()
            
            self._save_game()
            notification_manager.show("Saving...", "info", 0.5)
            time.sleep(0.5)
        
        # Reset game state
        self.duck = None
        self.behavior_ai = None
        self.duck_brain = None
        self._state = "title"
        
        # Start title music
        self._start_title_music()
        
        self.renderer.show_message("Returning to title...")
        time.sleep(0.3)

    def _is_any_menu_open(self) -> bool:
        """Check if any menu or overlay is currently open."""
        return (
            self._crafting_menu_open or
            self._building_menu_open or
            self._areas_menu_open or
            self._use_menu_open or
            self._minigames_menu_open or
            self._quests_menu_open or
            self._weather_menu_open or
            self._treasure_menu_open or
            self._scrapbook_menu_open or
            self._tricks_menu_open or
            self._titles_menu_open or
            self._decorations_menu_open or
            self._collectibles_menu_open or
            self._secrets_menu_open or
            self._garden_menu_open or
            self._prestige_menu_open or
            self._save_slots_menu_open or
            self._trading_menu_open or
            self._enhanced_diary_open or
            self._festival_menu_open or
            self._settings_menu_open or
            self._main_menu_open or
            self._debug_menu_open or
            self.renderer.is_shop_open() or
            self.renderer.is_talking() or
            self.renderer._show_stats or
            self.renderer._show_inventory or
            self.renderer._show_help
        )

    def _show_message_if_no_menu(self, message: str, duration: float = 5.0, category: str = "system"):
        """Show a message only if no menu is currently open. Used for non-critical duck messages."""
        if not self._is_any_menu_open():
            self.renderer.show_message(message, duration, category)

    def _close_all_menus(self):
        """Close all open game menus (crafting, building, etc.) and dismiss message overlay."""
        self.renderer.dismiss_message()
        self._crafting_menu_open = False
        self._building_menu_open = False
        self._areas_menu_open = False
        self._use_menu_open = False
        self._minigames_menu_open = False
        self._quests_menu_open = False
        self._weather_menu_open = False
        self._treasure_menu_open = False
        self._scrapbook_menu_open = False
        self._tricks_menu_open = False
        self._titles_menu_open = False
        self._decorations_menu_open = False
        self._collectibles_menu_open = False
        self._secrets_menu_open = False
        self._garden_menu_open = False
        self._prestige_menu_open = False
        self._save_slots_menu_open = False
        self._trading_menu_open = False
        self._enhanced_diary_open = False
        self._festival_menu_open = False
        self._settings_menu_open = False
        self._main_menu_open = False
        self._show_goals = False
        self._debug_menu_open = False
        self.renderer.dismiss_overlay()
        self._debug_submenu = None

    def _has_open_overlay(self) -> bool:
        """Check if any overlay or menu is currently open that should block master menu."""
        # Check renderer overlays (but NOT message overlay - that's just informational)
        if self.renderer.is_talking():
            return True
        if self.renderer.is_shop_open():
            return True
        if self.renderer._show_stats:
            return True
        if self.renderer._show_inventory:
            return True
        if self.renderer._show_help:
            return True
        # Note: _show_message_overlay is NOT blocking - messages are informational
            
        # Check game menus
        return (
            self._crafting_menu_open or
            self._building_menu_open or
            self._areas_menu_open or
            self._use_menu_open or
            self._minigames_menu_open or
            self._quests_menu_open or
            self._weather_menu_open or
            self._treasure_menu_open or
            self._scrapbook_menu_open or
            self._tricks_menu_open or
            self._titles_menu_open or
            self._decorations_menu_open or
            self._collectibles_menu_open or
            self._secrets_menu_open or
            self._garden_menu_open or
            self._prestige_menu_open or
            self._save_slots_menu_open or
            self._trading_menu_open or
            self._enhanced_diary_open or
            self._festival_menu_open or
            self._settings_menu_open or
            self._main_menu_open or
            self._show_goals or
            self._debug_menu_open or
            (self._confirmation_dialog and self._confirmation_dialog.is_open) or
            self._active_minigame is not None
        )

    def _close_all_overlays(self):
        """Close all open overlays and menus."""
        # Close renderer overlays
        self.renderer.hide_overlays()
        self.renderer.dismiss_message()

        # Close game menus
        self._crafting_menu_open = False
        self._building_menu_open = False
        self._areas_menu_open = False
        self._use_menu_open = False
        self._minigames_menu_open = False
        self._quests_menu_open = False
        self._weather_menu_open = False
        self._treasure_menu_open = False
        self._scrapbook_menu_open = False
        self._tricks_menu_open = False
        self._titles_menu_open = False
        self._decorations_menu_open = False
        self._collectibles_menu_open = False
        self._secrets_menu_open = False
        self._garden_menu_open = False
        self._prestige_menu_open = False
        self._save_slots_menu_open = False
        self._trading_menu_open = False
        self._enhanced_diary_open = False
        self._festival_menu_open = False
        self._settings_menu_open = False
        self._main_menu_open = False
        self._show_goals = False
        self._debug_menu_open = False
        self.renderer.dismiss_overlay()
        self._debug_submenu = None

    def _quit(self):
        """Quit the game."""
        if self.duck:
            # End DuckBrain session before saving
            if self.duck_brain:
                self.duck_brain.end_session()
            
            self._save_game()
            self.renderer.show_message("Saving and quitting...")
            time.sleep(0.5)

        # Stop any playing music
        sound_engine.stop_music()
        sound_engine.stop_background_music()

        # Clean up Python cache directories
        self._cleanup_pycache()

        self._running = False

    def _cleanup_pycache(self):
        """Remove __pycache__ directories to keep install clean."""
        import shutil
        from pathlib import Path
        
        try:
            # Get the game's root directory
            game_dir = Path(__file__).parent.parent
            
            # Find and remove all __pycache__ directories
            for cache_dir in game_dir.rglob("__pycache__"):
                if cache_dir.is_dir():
                    shutil.rmtree(cache_dir, ignore_errors=True)
        except Exception:
            pass  # Silently ignore cleanup errors

    def _start_reset_confirmation(self):
        """Start the reset game confirmation dialog using the new system."""
        self._confirmation_dialog = ConfirmationDialog(
            title="RESET GAME?",
            message="This will DELETE all progress!\n"
                    "Your duck, items, and achievements\n"
                    "will be PERMANENTLY lost!",
            dangerous=True,  # Requires typing "yes"
            on_confirm=self._confirm_reset,
            on_cancel=lambda: self.renderer.show_message("Reset cancelled.", duration=2.0)
        )
        self._confirmation_dialog.is_open = True
        self._render_confirmation_dialog()

    def _confirm_reset(self):
        """Confirm and execute game reset."""
        self._reset_confirmation = False
        # Note: _confirmation_dialog is cleared by _handle_confirmation_input
        
        notification_manager.show("Resetting game...", "warning", 2.0)

        # Clear Python cache to ensure fresh state
        self._clear_pycache()

        # Delete save file
        if self.save_manager.save_exists():
            self.save_manager.delete_save()

        # Reset all state
        self.duck = None
        self.behavior_ai = None
        self.inventory = Inventory()
        self.goals = GoalSystem()
        self.achievements = AchievementSystem()
        self.progression = ProgressionSystem()
        self.home = DuckHome()

        from world.habitat import Habitat
        self.habitat = Habitat()

        # Update interaction controller with new habitat reference
        # (duck may be None at this point, will be set properly in _start_new_game)
        self.interaction_controller.set_references(
            habitat=self.habitat,
            renderer=self.renderer,
            duck=self.duck,
            on_effects_applied=self._on_interaction_effects_applied
        )

        self.atmosphere = AtmosphereManager()
        self.diary = DuckDiary()
        self.exploration = ExplorationSystem()
        self.materials = MaterialInventory()
        self.crafting = CraftingSystem()
        self.building = BuildingSystem()
        
        # Reset new feature systems
        self.scrapbook = Scrapbook()
        self.fishing = FishingMinigame()
        self.garden = Garden()
        self.treasure = TreasureHunter()
        self.challenges = ChallengeSystem()
        self.friends = FriendsSystem()
        self.friends.on_friendship_level_up = self._on_friendship_level_up
        self.quests = QuestSystem()
        self.festivals = FestivalSystem()
        self.prestige = PrestigeSystem()
        self.collectibles = CollectiblesSystem()
        self.tricks = TricksSystem()
        self.decorations = DecorationsSystem()
        self.titles = TitlesSystem()
        self.outfits = OutfitManager()
        self.seasonal_clothing = SeasonalClothingSystem()
        self.secrets = SecretsSystem()
        self.weather_activities = WeatherActivitiesSystem()
        self.trading = TradingSystem()
        self.fortune = FortuneSystem()
        self.aging = AgingSystem()
        self.extended_personality = ExtendedPersonalitySystem()
        self.statistics = StatisticsSystem()
        self.day_night = DayNightSystem()
        self.badges = BadgesSystem()
        self.mood_visuals = MoodVisualEffects()
        self.ambient = AmbientSoundSystem()
        self.sound_effects = SoundEffectSystem()
        self.mood_dialogue = MoodDialogueSystem()
        self.enhanced_diary = EnhancedDiarySystem()
        self.save_slots = SaveSlotsSystem()

        self._statistics = {}
        self._weather_seen = set()
        self._session_feeds = 0

        # Stop music and return to title
        sound_engine.stop_music()
        sound_engine.stop_background_music()

        self._state = "title"
        self._start_title_music()

        self.renderer.show_message("Game reset! Starting fresh...", duration=3.0)

    def _clear_pycache(self):
        """Clear Python cache directories to ensure fresh state."""
        import shutil
        from pathlib import Path
        
        base_dir = Path(__file__).parent.parent
        cleared = 0
        
        for pycache_dir in base_dir.rglob("__pycache__"):
            try:
                shutil.rmtree(pycache_dir)
                cleared += 1
            except Exception:
                pass  # Ignore errors, some caches may be in use
        
        # Also clear any .pyc files in the root
        for pyc_file in base_dir.rglob("*.pyc"):
            try:
                pyc_file.unlink()
            except Exception:
                pass

    def _cancel_reset(self):
        """Cancel the reset confirmation."""
        self._reset_confirmation = False
        self.renderer.show_message("Reset cancelled.", duration=2.0)

    # ==================== EXPLORATION SYSTEM ====================

    def _do_explore(self):
        """Explore the current area for resources."""
        if not self.duck:
            return

        # Try to explore
        result = self.exploration.explore(self.duck)

        if not result["success"]:
            self.renderer.show_message(result["message"], duration=3.0)
            return

        # Add found resources to inventory
        resources_found = []
        for material_id, quantity in result.get("resources", {}).items():
            if material_id in MATERIALS:
                if self.materials.add_material(material_id, quantity):
                    mat = MATERIALS[material_id]
                    resources_found.append(f"{mat.name} x{quantity}")

        # Handle rare discoveries
        if result.get("rare_discovery"):
            item_id = result["rare_discovery"]
            self.inventory.add_item(item_id)
            sound_engine.play_sound("discovery")
            # Rare discoveries give bonus coins
            coins_earned = 25
            self.habitat.add_currency(coins_earned)
            self.renderer.show_message(
                f"* RARE DISCOVERY! *\n\n"
                f"You found: {item_id.replace('_', ' ').title()}!\n"
                f"Resources: {', '.join(resources_found) if resources_found else 'None'}\n"
                f"+{coins_earned} Coins",
                duration=5.0
            )
            # Achievement for rare finds
            self._unlock_achievement("rare_find")
            return

        # Handle danger encounters
        if result.get("danger"):
            danger = result["danger"]
            self.renderer.show_message(
                f"! DANGER! !\n\n"
                f"{danger['message']}\n"
                f"You escaped but dropped some items!",
                duration=4.0
            )
            return

        # Normal exploration result - award coins based on resources found
        coins_earned = 5 if resources_found else 2  # Base coins for exploring
        coins_earned += len(resources_found) * 3  # Bonus per resource type found
        self.habitat.add_currency(coins_earned)
        
        biome_name = result.get("biome", "area").replace("_", " ").title()
        if resources_found:
            msg = f"~ Explored {biome_name} ~\n\nFound: {', '.join(resources_found)}\n+{coins_earned} Coins"
            if result.get("skill_up"):
                msg += f"\n\n* Gathering skill improved!"
                # Check for gathering master achievement
                if self.exploration.gathering_skill >= 5:
                    self._unlock_achievement("gathering_master")
        else:
            msg = f"~ Explored {biome_name} ~\n\nNothing found this time.\n+{coins_earned} Coins"

        self.renderer.show_message(msg, duration=3.0)

        # Award some XP for exploring
        new_level = self.progression.add_xp(5, "exploration")
        if new_level:
            self._on_level_up(new_level)

        # First exploration achievement
        self._unlock_achievement("first_explore")

        # Check for area discovery achievements
        area_count = len(self.exploration.discovered_areas)
        if area_count >= 5:
            self._unlock_achievement("discover_5_areas")
        if area_count >= 10:
            self._unlock_achievement("discover_10_areas")


    def _show_crafting_menu(self):
        """Show the crafting menu overlay."""
        if not self.duck:
            return

        # Get available recipes
        available = self.crafting.get_available_recipes(self.materials)
        all_recipes = list(RECIPES.values())

        if self.crafting._current_craft:
            # Show crafting in progress as simple message
            progress = self.crafting._current_craft
            recipe = RECIPES.get(progress.recipe_id)
            if recipe:
                pct = int(progress.get_progress() * 100)
                self.renderer.show_message(
                    f"# Crafting: {recipe.name} ({pct}%)\n\n[Press ESC or C to close]",
                    duration=0
                )
            else:
                self.renderer.show_message("Crafting in progress...", duration=0)
            self._crafting_menu_open = True
            return

        # Build menu items - show all recipes, let MenuSelector handle pagination
        items = []
        for recipe in all_recipes:
            can_craft = recipe.result_item in available
            items.append({
                'id': recipe.id,
                'label': f"{'x' if can_craft else ' '} {recipe.name}",
                'description': f"Needs: {', '.join(f'{v} {k}' for k, v in recipe.ingredients.items())}",
                'enabled': can_craft,
                'data': recipe
            })

        self._crafting_menu.set_items([
            MenuItem(id=item['id'], label=item['label'], description=item['description'],
                     enabled=item['enabled'], data=item.get('data'))
            for item in items
        ])
        self._crafting_menu.open()
        self._crafting_menu_open = True
        self._update_crafting_menu_display()

    def _craft_item(self, recipe_id: str):
        """Craft an item by recipe ID (from menu action)."""
        if not self.duck:
            return

        recipe = RECIPES.get(recipe_id)
        if not recipe:
            self.renderer.show_message(f"Unknown recipe: {recipe_id}", duration=2.0)
            return

        result = self.crafting.start_crafting(recipe_id, self.materials)
        self.renderer.show_message(result["message"], duration=3.0, category="action")

    def _show_building_menu(self):
        """Show the building menu overlay."""
        if not self.duck:
            return

        # Get buildable structures
        buildable = self.building.get_buildable_structures(self.materials)
        all_blueprints = list(BLUEPRINTS.values())

        if self.building._current_build:
            # Show building in progress as simple message
            build_progress = self.building._current_build
            structure = build_progress.structure
            bp = BLUEPRINTS.get(structure.blueprint_id)
            if bp:
                stage_names = ["Foundation", "Frame", "Walls", "Roof", "Finishing"]
                current_stage = stage_names[min(structure.current_stage, 4)]
                pct = int((structure.current_stage / bp.stages) * 100)
                self.renderer.show_message(
                    f"# Building: {bp.name}\nStage: {current_stage} ({pct}%)\n\n[Press ESC or R to close]",
                    duration=0
                )
            else:
                self.renderer.show_message("Building in progress...", duration=0)
            self._building_menu_open = True
            return

        # Build menu items - show all blueprints with upgrade info
        items = []
        for bp in all_blueprints:
            can_build = bp.id in buildable
            
            # Check if this is an upgrade
            upgrade_info = self.building.get_upgrade_info(bp.id, self.materials)
            is_upgrade = upgrade_info["is_upgrade"]
            
            if is_upgrade:
                # Show reduced material cost for upgrades
                can_upgrade, _ = self.building.can_upgrade(bp.id, self.materials, self.progression.level)
                can_build = can_upgrade
                mat_desc = ', '.join(f'{v} {k}' for k, v in upgrade_info["reduced_materials"].items() if v > 0)
                if not mat_desc:
                    mat_desc = "No extra materials needed!"
                label = f"{'x' if can_build else ' '} ^ {bp.name}"  # ^ indicates upgrade
                desc = f"UPGRADE - Needs: {mat_desc}"
            else:
                mat_desc = ', '.join(f'{v} {k}' for k, v in bp.required_materials.items())
                label = f"{'x' if can_build else ' '} {bp.name}"
                desc = f"Needs: {mat_desc}"
            
            items.append({
                'id': bp.id,
                'label': label,
                'description': desc,
                'enabled': can_build,
                'data': bp
            })

        self._building_menu.set_items([
            MenuItem(id=item['id'], label=item['label'], description=item['description'],
                     enabled=item['enabled'], data=item.get('data'))
            for item in items
        ])
        self._building_menu.open()
        self._building_menu_open = True
        self._update_building_menu_display()

    def _start_building(self, blueprint_id: str):
        """Start building a structure by blueprint ID (from menu action)."""
        if not self.duck:
            return

        bp = BLUEPRINTS.get(blueprint_id)
        if not bp:
            self.renderer.show_message(f"Unknown blueprint: {blueprint_id}", duration=2.0)
            return

        result = self.building.start_building(bp.id, self.materials, player_level=self.progression.level)
        if result.get("success"):
            self._start_building_animation(bp)
        else:
            self.renderer.show_message(result["message"], duration=3.0, category="action")

    def _show_areas_menu(self):
        """Show discovered areas and allow travel."""
        if not self.duck:
            return

        # Pass actual player level to get correct available areas
        available = self.exploration.get_available_areas(self.progression.level)
        current_biome = self.exploration._current_biome
        current_name = current_biome.value.replace("_", " ").title() if current_biome else "Unknown"

        if not available:
            self.renderer.show_message(
                f"=== AREAS ===\n\nCurrent: {current_name}\n\n"
                "No other areas discovered yet.\nKeep exploring [E] to find new biomes!\n\n"
                f"Gathering skill: Lv.{self.exploration.gathering_skill}\n\n[ESC or A] Close",
                duration=0
            )
            self._areas_menu_open = True
            return

        # Build menu items
        items = []
        for area in available:
            # Show biome type as description
            biome_name = area.biome.value.replace("_", " ").title() if hasattr(area, 'biome') else "Unknown"
            items.append({
                'id': area.biome.value if hasattr(area, 'biome') else area.name,
                'label': f"  {area.name}",
                'description': f"{biome_name}",
                'enabled': True,
                'data': area
            })

        self._areas_menu.set_items([
            MenuItem(id=item['id'], label=item['label'], description=item['description'],
                     enabled=item['enabled'], data=item.get('data'))
            for item in items
        ])
        self._areas_menu.open()
        self._areas_menu_open = True
        self._update_areas_menu_display()

    def _handle_crafting_input(self, key_str: str, key_name: str = "", key=None) -> bool:
        """Handle input while crafting menu is open. Returns True if handled."""
        if not self._crafting_menu_open:
            return False

        # If crafting in progress, just handle close
        if self.crafting._current_craft:
            if key.name == 'KEY_ESCAPE' or key_str == 'c':
                self._crafting_menu_open = False
                self._crafting_menu.close()
                self.renderer.dismiss_message()
            return True

        # Handle arrow keys and enter directly (same as shop)
        if key.name == "KEY_UP":
            idx = self._crafting_menu.get_selected_index()
            if idx > 0:
                self._crafting_menu.set_selected_index(idx - 1)
                self._update_crafting_menu_display()
            return True
        if key.name == "KEY_DOWN":
            idx = self._crafting_menu.get_selected_index()
            items = self._crafting_menu.get_items()
            if idx < len(items) - 1:
                self._crafting_menu.set_selected_index(idx + 1)
                self._update_crafting_menu_display()
            return True
        if key.name == "KEY_ENTER":
            selected = self._crafting_menu.get_selected_item()
            if selected and selected.data and selected.enabled:
                recipe = selected.data
                result = self.crafting.start_crafting(recipe.id, self.materials)
                self._crafting_menu_open = False
                self.renderer.show_message(result["message"], duration=3.0)
            return True

        # Close on ESC or C
        if key.name == 'KEY_ESCAPE' or key_str == 'c':
            self._crafting_menu_open = False
            self.renderer.dismiss_message()
            return True

        return True  # Consume all keys while menu is open

    def _update_crafting_menu_display(self):
        """Update the crafting menu display with current selection."""
        items = [{'label': item.label, 'description': item.description, 'enabled': item.enabled}
                 for item in self._crafting_menu.get_items()]
        self.renderer.show_menu(
            "CRAFTING",
            items,
            self._crafting_menu.get_selected_index(),
            footer="[^v] Navigate  [Enter] Craft  [C/ESC] Close"
        )

    def _handle_building_input(self, key_str: str, key_name: str = "", key=None) -> bool:
        """Handle input while building menu is open. Returns True if handled."""
        if not self._building_menu_open:
            return False

        # If building in progress, just handle close
        if self.building._current_build:
            if key.name == 'KEY_ESCAPE' or key_str == 'r':
                self._building_menu_open = False
                self._building_menu.close()
                self.renderer.dismiss_message()
            return True

        # Handle arrow keys and enter directly (same as shop)
        if key.name == "KEY_UP":
            idx = self._building_menu.get_selected_index()
            if idx > 0:
                self._building_menu.set_selected_index(idx - 1)
                self._update_building_menu_display()
            return True
        if key.name == "KEY_DOWN":
            idx = self._building_menu.get_selected_index()
            items = self._building_menu.get_items()
            if idx < len(items) - 1:
                self._building_menu.set_selected_index(idx + 1)
                self._update_building_menu_display()
            return True
        if key.name == "KEY_ENTER":
            selected = self._building_menu.get_selected_item()
            if selected and selected.data and selected.enabled:
                bp = selected.data
                result = self.building.start_building(bp.id, self.materials, player_level=self.progression.level)
                self._building_menu_open = False
                if result.get("success"):
                    self._start_building_animation(bp)
                else:
                    self.renderer.show_message(result["message"], duration=3.0)
            return True

        # Close on ESC or R
        if key.name == 'KEY_ESCAPE' or key_str == 'r':
            self._building_menu_open = False
            self.renderer.dismiss_message()
            return True

        return True  # Consume all keys while menu is open

    def _update_building_menu_display(self):
        """Update the building menu display with current selection."""
        items = [{'label': item.label, 'description': item.description, 'enabled': item.enabled}
                 for item in self._building_menu.get_items()]
        self.renderer.show_menu(
            "BUILDING",
            items,
            self._building_menu.get_selected_index(),
            footer="[^v] Navigate  [Enter] Build  [R/ESC] Close"
        )

    def _start_building_animation(self, blueprint):
        """Start the duck building animation."""
        self._duck_building = True
        self._building_start_time = time.time()
        
        if self.duck:
            self.duck.current_action = "building"
            self.duck.set_action_message(f"*builds {blueprint.name}* #")
        
        self.renderer.show_message(f"# Building {blueprint.name}...", duration=blueprint.build_time)
        duck_sounds.play()  # Building sound

    def _complete_building(self, build_result):
        """Complete the building and show celebration."""
        self._duck_building = False
        
        if self.duck:
            self.duck.current_action = "idle"
            self.duck.set_action_message("")
        
        blueprint_id = build_result.get("blueprint_id")
        if blueprint_id and blueprint_id in BLUEPRINTS:
            bp = BLUEPRINTS[blueprint_id]
            self.renderer.show_celebration(
                "building_complete",
                f"[=] {bp.name} Complete!",
                duration=4.0
            )
            duck_sounds.level_up()
            
            # Check building achievements
            self._check_building_achievements()
        else:
            self.renderer.show_message(build_result.get("message", "Building complete!"), duration=3.0)

    def _check_building_achievements(self):
        """Check for building-related achievements."""
        if self.building.structures_built >= 1:
            self.achievements.unlock("first_builder")
        if self.building.structures_built >= 5:
            self.achievements.unlock("builder_5")
        if self.building.structures_built >= 15:
            self.achievements.unlock("master_builder")
        
        # Check for nest/house construction
        for structure in self.building.structures:
            if structure.blueprint_id in ["basic_nest", "cozy_nest", "deluxe_nest"]:
                self.achievements.unlock("nest_builder")
            if structure.blueprint_id in ["mud_hut", "wooden_cottage", "stone_house"]:
                self.achievements.unlock("house_builder")

    def _handle_areas_input(self, key_str: str, key_name: str = "", key=None) -> bool:
        """Handle input while areas menu is open. Returns True if handled."""
        if not self._areas_menu_open:
            return False

        # If no areas available, just handle close
        available = self.exploration.get_available_areas()
        if not available:
            if key.name == 'KEY_ESCAPE' or key_str == 'a':
                self._areas_menu_open = False
                self._areas_menu.close()
                self.renderer.dismiss_message()
            return True

        # Handle arrow keys and enter directly (same as shop)
        if key.name == "KEY_UP":
            idx = self._areas_menu.get_selected_index()
            if idx > 0:
                self._areas_menu.set_selected_index(idx - 1)
                self._update_areas_menu_display()
            return True
        if key.name == "KEY_DOWN":
            idx = self._areas_menu.get_selected_index()
            items = self._areas_menu.get_items()
            if idx < len(items) - 1:
                self._areas_menu.set_selected_index(idx + 1)
                self._update_areas_menu_display()
            return True
        if key.name == "KEY_ENTER":
            selected = self._areas_menu.get_selected_item()
            if selected and selected.data:
                area = selected.data
                self._areas_menu_open = False
                self.renderer.dismiss_message()
                self._start_travel_to_area(area)
            return True

        # Close on ESC or A
        if key.name == 'KEY_ESCAPE' or key_str == 'a':
            self._areas_menu_open = False
            self.renderer.dismiss_message()
            return True

        return True  # Consume all keys while menu is open

    def _update_areas_menu_display(self):
        """Update the areas menu display with current selection and area preview."""
        current_area = self.exploration.current_area
        current_name = current_area.name if current_area else "Unknown"

        # Get selected area for preview
        selected_item = self._areas_menu.get_selected_item()
        preview_lines = []
        if selected_item and selected_item.data:
            from world.exploration import get_area_art
            preview_area = selected_item.data
            art = get_area_art(preview_area.name)
            # Show first 5 lines of art as preview
            preview_lines = art[:5] if art else []

        items = [{'label': item.label, 'description': item.description, 'enabled': item.enabled}
                 for item in self._areas_menu.get_items()]

        # Build header with preview
        header = f"AREAS (Current: {current_name})"
        if preview_lines:
            preview_text = "\n".join(preview_lines)
            header = f"{header}\n\n{preview_text}"

        self.renderer.show_menu(
            header,
            items,
            self._areas_menu.get_selected_index(),
            show_numbers=False,
            footer="[^v] Navigate  [Enter] Travel  [A/ESC] Close"
        )

    def _travel_to_area(self, area_name: str):
        """Travel to an area by name (from menu action)."""
        if not self.duck:
            return

        # Look up area by name
        available = self.exploration.get_available_areas(self.progression.level)
        target_area = None
        for area in available:
            if area.name == area_name:
                target_area = area
                break

        if not target_area:
            self.renderer.show_message(f"Cannot travel to {area_name}", duration=2.0)
            return

        self._start_travel_to_area(target_area)

    def _start_travel_to_area(self, area):
        """Start duck traveling to a new area."""
        self._duck_traveling = True
        self._travel_start_time = time.time()
        self._travel_destination = area
        
        # Set duck action message for traveling animation
        if self.duck:
            self.duck.current_action = "traveling"
            self.duck.set_action_message(f"*waddles towards {area.name}*")
        
        self.renderer.show_message(f"d Traveling to {area.name}...", duration=self._travel_duration)
        duck_sounds.play()  # Travel sound

    def _complete_travel(self):
        """Complete the travel and start exploring."""
        if not self._travel_destination:
            self._duck_traveling = False
            return

        area = self._travel_destination
        result = self.exploration.travel_to(area)

        if result.get("success"):
            # Show area art and description
            from world.exploration import get_area_art
            art_lines = get_area_art(area.name)
            art_display = "\n".join(art_lines)

            arrival_msg = (
                f"=== {area.name} ===\n\n"
                f"{art_display}\n\n"
                f"{area.description}\n\n"
                f"[Press any key to explore]"
            )
            self.renderer.show_message(arrival_msg, duration=0)

            # Start exploring after showing the art
            self._start_exploring()
        else:
            self.renderer.show_message(result.get("message", "Couldn't reach destination"), duration=3.0)

        self._duck_traveling = False
        self._travel_destination = None

    def _start_exploring(self):
        """Start the duck exploring current area."""
        self._duck_exploring = True
        self._exploring_start_time = time.time()
        
        # Set duck to exploring animation
        if self.duck:
            current_area = self.exploration.current_area
            area_name = current_area.name if current_area else "the area"
            self.duck.current_action = "exploring"
            self.duck.set_action_message(f"*searches around {area_name}*")
        
        duck_sounds.quack("curious" if hasattr(duck_sounds, "quack") else "happy")

    def _complete_exploring(self):
        """Complete the exploration and show results."""
        self._duck_exploring = False
        
        if self.duck:
            self.duck.current_action = "idle"
            self.duck.set_action_message("")
        
        # Do the actual exploration
        result = self.exploration.explore(self.duck, self.progression.level)
        
        # Add resources to material inventory
        if result.get("resources"):
            for resource_id, amount in result["resources"].items():
                self.materials.add_material(resource_id, amount)
        
        # Award XP
        if result.get("xp_gained"):
            new_level = self.progression.add_xp(result["xp_gained"])
            if new_level:
                self._on_level_up(new_level)
        
        # Show results
        message = result.get("message", "Exploration complete!")
        if result.get("new_area_discovered"):
            self.renderer.show_celebration("discovery", f"[?] Discovered: {result['new_area_discovered']}!", duration=3.0)
            duck_sounds.level_up()
        elif result.get("rare_discovery"):
            self.renderer.show_celebration("rare_find", f"* Found: {result['rare_discovery']}!", duration=3.0)
            duck_sounds.level_up()
        else:
            self.renderer.show_message(message, duration=4.0)
        
        # Check achievements
        self._check_exploration_achievements()

        # Update challenge and quest progress for exploration
        self.challenges.update_progress("explore", 1)
        self._process_quest_updates("explore", "any", 1)

        # Update personality for exploration
        self.extended_personality.adjust_trait("curiosity", 2, "Exploring")
        self.extended_personality.update_hidden_trait_progress("adventurer", 0.02)

    def _check_exploration_achievements(self):
        """Check for exploration-related achievements."""
        if len(self.exploration.discovered_areas) >= 3:
            self.achievements.unlock("explorer_3_areas")
        if len(self.exploration.discovered_areas) >= 7:
            self.achievements.unlock("explorer_7_areas")
        if len(self.exploration.discovered_areas) >= 15:
            self.achievements.unlock("explorer_15_areas")
        if self.exploration.total_resources_gathered >= 100:
            self.achievements.unlock("gatherer_100")
        if self.exploration.total_resources_gathered >= 500:
            self.achievements.unlock("gatherer_500")
        if len(self.exploration.rare_items_found) >= 1:
            self.achievements.unlock("first_rare_find")
        if len(self.exploration.rare_items_found) >= 10:
            self.achievements.unlock("treasure_hunter")

    def _show_use_menu(self):
        """Show the use/interact menu for owned items."""
        if not self.duck:
            return

        # Build list of interactable items
        self._use_menu_items = []
        for item_id in self.habitat.owned_items:
            if item_id in ITEM_INTERACTIONS:
                item = get_shop_item(item_id)
                if item:
                    self._use_menu_items.append((item_id, item))

        if not self._use_menu_items:
            self.renderer.show_message(
                "No interactable items owned!\n"
                "Buy toys and decorations from the shop [B]",
                duration=3.0
            )
            return

        # Build menu items
        items = []
        for item_id, item in self._use_menu_items:
            interaction = ITEM_INTERACTIONS.get(item_id, {})
            commands = interaction.get("commands", ["use"])
            cmd_hint = commands[0] if commands else "use"
            items.append({
                'id': item_id,
                'label': item.name,
                'description': f'Command: "{cmd_hint}"',
                'enabled': True,
                'data': (item_id, item)
            })

        self._use_menu.set_items([
            MenuItem(id=item['id'], label=item['label'], description=item['description'],
                     enabled=item['enabled'], data=item.get('data'))
            for item in items
        ])
        self._use_menu.open()
        self._use_menu_selected = 0
        self._use_menu_open = True
        self._update_use_menu_display()

    def _update_use_menu_display(self):
        """Update the use menu display."""
        items = [{'label': item.label, 'description': item.description, 'enabled': item.enabled}
                 for item in self._use_menu.get_items()]
        self.renderer.show_menu(
            "USE ITEM",
            items,
            self._use_menu.get_selected_index(),
            footer="[^v] Navigate  [Enter] Use  [U/ESC] Close"
        )

    def _handle_use_input(self, key_str: str, key_name: str = "", key=None) -> bool:
        """Handle input while use menu is open. Returns True if handled."""
        if not self._use_menu_open:
            return False

        # Handle arrow keys and enter directly (same as shop)
        if key.name == "KEY_UP":
            idx = self._use_menu.get_selected_index()
            if idx > 0:
                self._use_menu.set_selected_index(idx - 1)
                self._update_use_menu_display()
            return True
        if key.name == "KEY_DOWN":
            idx = self._use_menu.get_selected_index()
            items = self._use_menu.get_items()
            if idx < len(items) - 1:
                self._use_menu.set_selected_index(idx + 1)
                self._update_use_menu_display()
            return True
        if key.name == "KEY_ENTER":
            selected = self._use_menu.get_selected_item()
            if selected and selected.data:
                item_id, item = selected.data
                self._use_menu_open = False
                self.renderer.dismiss_message()
                self._execute_item_interaction(item_id)
            return True

        # Close on ESC or U
        if key.name == 'KEY_ESCAPE' or key_str == 'u':
            self._use_menu_open = False
            self.renderer.dismiss_message()
            return True

        return True  # Consume all keys while menu is open

    def _toggle_boombox_music(self):
        """Toggle the boombox music on/off."""
        if self._boombox_playing:
            sound_engine.stop_background_music()
            self._boombox_playing = False
            if self.duck:
                self.duck.set_action_message("*turns off boombox* The music stops...")
            self.renderer.show_message("*click* Boombox off.", duration=2.0, category="duck")
        else:
            sound_engine.play_background_music('main')
            self._boombox_playing = True
            if self.duck:
                self.duck.set_action_message("*turns on boombox* ## MUSIC TIME! ##")
            self.renderer.show_message("## Boombox ON! Let's groove! ##", duration=2.0)
            duck_sounds.quack("happy")

    # ==================== MINI-GAMES SYSTEM ====================

    def _show_minigames_menu(self):
        """Show the mini-games selection menu."""
        if not self.duck:
            return

        # Can't open menu if already in a minigame
        if self._active_minigame:
            return

        games = self.minigames.get_available_games()

        # Build menu items
        items = []

        # Add fishing as first option
        fishing_status = "-o" if not self.fishing.is_fishing else "⏱"
        fishing_desc = "Cast your line and catch fish!"
        if self.fishing.total_catches > 0:
            fishing_desc += f" | Caught: {self.fishing.total_catches}"
        items.append({
            'id': 'fishing',
            'label': f"{fishing_status} Fishing",
            'description': fishing_desc,
            'enabled': not self.fishing.is_fishing,
            'data': {'id': 'fishing', 'name': 'Fishing'}
        })

        for game in games:
            status = "x" if game["can_play"] else "⏱"
            desc = game['description']
            if game["high_score"] not in [0, 999]:
                if game["id"] in ["memory_match", "duck_race"]:
                    desc += f" | Best: {game['high_score']}"
                else:
                    desc += f" | High: {game['high_score']}"
            if not game["can_play"]:
                desc += f" | {game['cooldown_msg']}"

            items.append({
                'id': game['id'],
                'label': f"{status} {game['name']}",
                'description': desc,
                'enabled': game['can_play'],
                'data': game
            })

        self._minigames_menu.set_items([
            MenuItem(id=item['id'], label=item['label'], description=item['description'],
                     enabled=item['enabled'], data=item.get('data'))
            for item in items
        ])
        self._minigames_menu.open()
        self._minigames_menu_open = True
        self._minigames_menu_selected = 0
        self._update_minigames_menu_display()

    def _update_minigames_menu_display(self):
        """Update the minigames menu display."""
        items = [{'label': item.label, 'description': item.description, 'enabled': item.enabled}
                 for item in self._minigames_menu.get_items()]

        footer = f"Coins: {self.minigames.total_coins_earned} | [^v] Navigate  [Enter] Play  [J/ESC] Close"
        self.renderer.show_menu(
            "MINI-GAMES",
            items,
            self._minigames_menu.get_selected_index(),
            footer=footer
        )

    def _handle_minigames_menu_input(self, key_str: str, key_name: str = "", key=None) -> bool:
        """Handle input while minigames menu is open."""
        if not self._minigames_menu_open:
            return False

        # Handle arrow keys and enter directly (same as shop)
        if key.name == "KEY_UP":
            idx = self._minigames_menu.get_selected_index()
            if idx > 0:
                self._minigames_menu.set_selected_index(idx - 1)
                self._update_minigames_menu_display()
            return True
        if key.name == "KEY_DOWN":
            idx = self._minigames_menu.get_selected_index()
            items = self._minigames_menu.get_items()
            if idx < len(items) - 1:
                self._minigames_menu.set_selected_index(idx + 1)
                self._update_minigames_menu_display()
            return True
        if key.name == "KEY_ENTER":
            selected = self._minigames_menu.get_selected_item()
            if selected and selected.data and selected.enabled:
                self._start_minigame(selected.data["id"])
            return True

        # Close on ESC or J
        if key.name == 'KEY_ESCAPE' or key_str == 'j':
            self._minigames_menu_open = False
            self.renderer.dismiss_message()
            return True

        # Number keys for quick select (kept for convenience)
        if key_str.isdigit() and 1 <= int(key_str) <= 4:
            games = self.minigames.get_available_games()
            idx = int(key_str) - 1
            if idx < len(games):
                self._start_minigame(games[idx]["id"])
            return True

        return False  # Let other keys pass through

    def _start_minigame(self, game_id: str):
        """Start a mini-game."""
        # Handle fishing separately
        if game_id == "fishing":
            self._minigames_menu_open = False
            self.renderer.dismiss_message()
            self._start_fishing("pond")
            return

        can_play, msg = self.minigames.can_play(game_id)
        if not can_play:
            self.renderer.show_message(msg, duration=2.0)
            return

        self._minigames_menu_open = False
        self.renderer.dismiss_message()

        # Create game instance
        if game_id == "bread_catch":
            self._active_minigame = BreadCatchGame()
        elif game_id == "bug_chase":
            self._active_minigame = BugChaseGame()
        elif game_id == "memory_match":
            self._active_minigame = MemoryMatchGame()
        elif game_id == "duck_race":
            self._active_minigame = DuckRaceGame()
        else:
            return

        self._minigame_type = game_id
        self._minigame_last_update = time.time()
        self.minigames.start_game(game_id)

        # Show game start message
        game_names = {
            "bread_catch": "Bread Catch",
            "bug_chase": "Bug Chase",
            "memory_match": "Memory Match",
            "duck_race": "Duck Race",
        }
        self.renderer.show_message(f"Starting {game_names.get(game_id, game_id)}!", duration=1.0)
        duck_sounds.quack("happy")

    def _handle_minigame_input(self, key_str: str, key_name: str = "") -> bool:
        """Handle input for active minigame."""
        if not self._active_minigame:
            return False

        game = self._active_minigame

        # Quit game with Q
        if key_str == 'q':
            self._end_minigame(abandoned=True)
            return True

        # Game-specific input
        if isinstance(game, BreadCatchGame):
            if key_name == 'KEY_LEFT':
                game.move_left()
            elif key_name == 'KEY_RIGHT':
                game.move_right()

        elif isinstance(game, BugChaseGame):
            if key_str == ' ' or key_name == 'KEY_ENTER':
                game.catch_bug()

        elif isinstance(game, MemoryMatchGame):
            if key_name == 'KEY_UP':
                game.move_cursor("up")
            elif key_name == 'KEY_DOWN':
                game.move_cursor("down")
            elif key_name == 'KEY_LEFT':
                game.move_cursor("left")
            elif key_name == 'KEY_RIGHT':
                game.move_cursor("right")
            elif key_str == ' ' or key_name == 'KEY_ENTER':
                game.select_card()

        elif isinstance(game, DuckRaceGame):
            if key_str == ' ' or key_name == 'KEY_ENTER':
                game.mash()

        return True

    def _handle_fishing_input(self, key_str: str, key_name: str = "", key=None) -> bool:
        """Handle input while fishing."""
        if not self.fishing.is_fishing:
            return False

        # Cancel fishing with Q or Escape
        if key_str == 'q' or key_name == 'KEY_ESCAPE':
            self.fishing.cancel_fishing()
            self.renderer.show_message("Stopped fishing.", duration=2.0)
            return True

        # Reel in with SPACE or ENTER when a fish is hooked
        is_space = key_str == ' ' or key_name == 'KEY_SPACE' or (key and str(key) == ' ')
        if is_space or key_name == 'KEY_ENTER':
            if self.fishing.hooked_fish:
                success, message, caught_fish = self.fishing.reel_in()

                if success and caught_fish:
                    # Show catch message
                    fish_name = caught_fish.fish_id.replace('_', ' ').title()
                    catch_msg = f"-o Caught: {fish_name}!\n"
                    catch_msg += f"Size: {caught_fish.size} cm"
                    if caught_fish.is_record:
                        catch_msg += "\n[#] NEW RECORD!"

                    self.renderer.show_message(catch_msg, duration=4.0)
                    duck_sounds.quack("happy")

                    # Award XP
                    self.progression.add_xp(20, "fishing")

                    # Update challenges and quests
                    self.challenges.update_progress("fish", 1)
                    self._process_quest_updates("catch", caught_fish.fish_id, 1)

                    # Update personality
                    self.extended_personality.adjust_trait("patience", 1, "Caught a fish")

                    # Check achievements
                    total_fish = self.fishing.total_catches
                    if total_fish == 1:
                        self.achievements.unlock("first_fish")
                    elif total_fish >= 10:
                        self.achievements.unlock("fish_10")
                    elif total_fish >= 50:
                        self.achievements.unlock("fish_master")
                else:
                    self.renderer.show_message(message, duration=2.0)
                    duck_sounds.quack("sad")

                return True
            else:
                # No fish hooked, just waiting
                self.renderer.show_message("Wait for a bite! -o", duration=1.0)
                return True

        return True  # Consume all input while fishing

    def _start_fishing(self, spot: str = "pond"):
        """Start a fishing session."""
        if self.fishing.is_fishing:
            self.renderer.show_message("Already fishing!", duration=2.0)
            return

        # Convert string spot to FishingSpot enum
        spot_map = {
            "pond": FishingSpot.POND,
            "river": FishingSpot.RIVER,
            "lake": FishingSpot.LAKE,
            "ocean": FishingSpot.OCEAN,
            "secret_cove": FishingSpot.SECRET_COVE,
        }
        fishing_spot = spot_map.get(spot.lower(), FishingSpot.POND)

        success, message = self.fishing.start_fishing(fishing_spot)
        if success:
            duck_sounds.play()  # Splash sound
            # The fishing overlay will show controls, just confirm we started
        else:
            self.renderer.show_message(message, duration=2.0)

    def _update_minigame(self):
        """Update the active minigame."""
        if not self._active_minigame:
            return

        current_time = time.time()
        delta_time = current_time - self._minigame_last_update
        self._minigame_last_update = current_time

        game = self._active_minigame

        # Update game based on type
        if isinstance(game, BreadCatchGame):
            game.update()
        elif isinstance(game, BugChaseGame):
            game.update(delta_time)
        elif isinstance(game, MemoryMatchGame):
            game.update()
        elif isinstance(game, DuckRaceGame):
            game.update(delta_time)

        # Check if game is over
        if game.game_over:
            self._end_minigame()

    def _end_minigame(self, abandoned: bool = False):
        """End the current minigame and award rewards."""
        if not self._active_minigame:
            return

        game = self._active_minigame
        game_type = self._minigame_type

        if abandoned:
            self.renderer.show_message("Game abandoned!", duration=2.0)
        else:
            # Get score based on game type
            if isinstance(game, BreadCatchGame):
                score = game.score
                is_time_based = False
            elif isinstance(game, BugChaseGame):
                score = game.score
                is_time_based = False
            elif isinstance(game, MemoryMatchGame):
                score = game.moves
                is_time_based = True  # Lower moves is better
            elif isinstance(game, DuckRaceGame):
                if game.winner == "You":
                    score = int(game.race_time)
                    is_time_based = True  # Lower time is better
                else:
                    score = 999  # Lost the race
                    is_time_based = True
            else:
                score = 0
                is_time_based = False

            # Calculate rewards
            result = self.minigames.finish_game(game_type, score, is_time_based)

            # Apply rewards
            self.habitat.add_currency(result.coins_earned)
            self.progression.add_xp(result.xp_earned, "minigame")

            for item_id in result.items_earned:
                self.inventory.add_item(item_id)

            # Show results
            lines = ["=== GAME OVER ===", ""]
            lines.append(result.message)
            lines.append("")
            lines.append(f"Coins: +{result.coins_earned}")
            lines.append(f"XP: +{result.xp_earned}")
            if result.items_earned:
                lines.append(f"Items: {', '.join(result.items_earned)}")
            if result.high_score:
                lines.append("")
                lines.append("* NEW HIGH SCORE! *")
                duck_sounds.level_up()

            self.renderer.show_message("\n".join(lines), duration=4.0)

            # Check achievements
            self._check_minigame_achievements(game_type, score, result.high_score)

        # Clean up
        self._active_minigame = None
        self._minigame_type = None

    def _check_minigame_achievements(self, game_type: str, score: int, is_high_score: bool):
        """Check for minigame-related achievements."""
        total_played = sum(self.minigames.games_played.values())

        if total_played >= 1:
            self.achievements.unlock("first_minigame")
        if total_played >= 10:
            self.achievements.unlock("minigame_fan")
        if total_played >= 50:
            self.achievements.unlock("minigame_master")

        if is_high_score:
            self.achievements.unlock("high_scorer")

        # Game-specific achievements
        if game_type == "bread_catch" and score >= 500:
            self.achievements.unlock("bread_master")
        if game_type == "bug_chase" and score >= 1000:
            self.achievements.unlock("bug_hunter")
        if game_type == "memory_match" and score <= 16:
            self.achievements.unlock("perfect_memory")
        if game_type == "duck_race" and score <= 10:
            self.achievements.unlock("speed_demon")

    def _render_minigame(self) -> List[str]:
        """Render the current minigame."""
        if not self._active_minigame:
            return []
        return self._active_minigame.render()

    # ==================== DREAMS SYSTEM ====================

    def _start_dream(self):
        """Start a dream sequence when the duck sleeps."""
        if not self.duck:
            return

        # Get recent activities for dream influence
        recent_activities = []
        # Convert deque to list for slicing (deque doesn't support slice notation)
        short_term_list = list(self.duck.memory.short_term)
        for memory in short_term_list[-5:]:
            # Memory objects have a 'type' attribute and 'content'
            if memory.type == "interaction":
                # Extract the interaction type from content (format: "type: details" or just "type")
                activity = memory.content.split(":")[0].strip()
                recent_activities.append(activity)

        # Get visitor names for friend dreams
        visitor_names = []
        if self.atmosphere.current_visitor:
            visitor_names.append(self.atmosphere.current_visitor[0].name)

        # Generate dream
        mood = self.duck.get_mood()
        self._dream_result = self.dreams.start_dream(
            mood_score=mood.score,
            recent_activities=recent_activities,
            visitor_names=visitor_names,
        )

        self._dream_active = True
        self._dream_scene_index = 0
        self._dream_scene_timer = time.time()

        # Set duck to sleeping state for the entire dream duration
        # Calculate total dream duration (3 seconds per scene + 3 second buffer)
        dream_duration = len(self._dream_result.scenes_shown) * 3.0 + 3.0 if self._dream_result else 12.0
        self.renderer.set_duck_state("sleeping", duration=dream_duration)
        self.renderer.show_closeup("sleeping", duration=dream_duration)

        # Notify reaction controller with correct dream duration
        # This prevents weather reactions from overriding sleeping animation
        self.reaction_controller.notify_user_action(dream_duration, time.time())

        # Prevent behavior AI from interrupting sleep
        if self.behavior_ai:
            self.behavior_ai._action_end_time = time.time() + dream_duration

        # Show first dream message
        if self._dream_result and self._dream_result.scenes_shown:
            self._show_dream_scene()

    def _show_dream_scene(self):
        """Show the current dream scene."""
        if not self._dream_result or not self._dream_active:
            return

        scenes = self._dream_result.scenes_shown
        if self._dream_scene_index < len(scenes):
            scene = scenes[self._dream_scene_index]
            # Show dream scene with dreamy formatting
            dream_msg = f"Zzz... {scene}"
            self.renderer.show_message(dream_msg, duration=3.0)
            self._dream_scene_timer = time.time()

    def _update_dream(self):
        """Update the dream sequence."""
        if not self._dream_active or not self._dream_result:
            return

        current_time = time.time()
        # Each scene lasts about 3 seconds
        if current_time - self._dream_scene_timer >= 3.0:
            self._dream_scene_index += 1

            if self._dream_scene_index < len(self._dream_result.scenes_shown):
                self._show_dream_scene()
            else:
                # Dream is over
                self._end_dream()

    def _end_dream(self):
        """End the dream and apply rewards."""
        if not self._dream_result or not self.duck:
            self._dream_active = False
            return

        result = self._dream_result

        # Wake up the duck - clear sleeping visuals
        self.renderer.set_duck_state("idle", duration=0)
        self.renderer.show_closeup("confused", duration=2.0)  # Show groggy wake-up closeup

        # Apply mood effect
        if result.mood_effect != 0:
            self.duck.needs.social = min(100, max(0, self.duck.needs.social + result.mood_effect))

        # Apply XP
        if result.xp_earned > 0:
            self.progression.add_xp(result.xp_earned, "dream")

        # Apply special reward
        if result.special_reward:
            self.inventory.add_item(result.special_reward)
            self.renderer.show_message(
                f"*wakes up* What a dream! Found: {result.special_reward}!",
                duration=3.0
            )
            duck_sounds.level_up()
        else:
            # Normal wake up message
            wake_messages = [
                "*yawn* That was a nice dream...",
                "*stretches* Zzz... huh? Oh, I'm awake!",
                "*blinks* What a journey that was...",
                "*ruffles feathers* Good dreams make good ducks!",
            ]
            self.renderer.show_message(random.choice(wake_messages), duration=2.0)

        # Check dream achievements
        self._check_dream_achievements()

        # Clean up
        self._dream_active = False
        self._dream_result = None
        self._dream_scene_index = 0

    def _check_dream_achievements(self):
        """Check for dream-related achievements."""
        stats = self.dreams.get_dream_stats()

        if stats["total_dreams"] >= 1:
            self.achievements.unlock("first_dream")
        if stats["total_dreams"] >= 10:
            self.achievements.unlock("dreamer")
        if stats["total_dreams"] >= 50:
            self.achievements.unlock("dream_master")

        if len(stats["special_rewards"]) >= 1:
            self.achievements.unlock("dream_treasure")
        if len(stats["special_rewards"]) >= 5:
            self.achievements.unlock("dream_collector")

        # Check for dream variety (all dream types experienced)
        if len(stats["dream_types"]) >= 8:
            self.achievements.unlock("dream_explorer")

    # ==================== BIRTHDAY & FACTS SYSTEM ====================

    def _check_birthday_milestone(self):
        """Check for birthday or milestone messages."""
        if not self.duck:
            return

        birthday_info = get_birthday_info(self.duck.created_at, self.duck.name)

        # Check for birthday
        if birthday_info.is_birthday:
            msg = get_birthday_message(self.duck.name, birthday_info.age_days)
            self.renderer.show_celebration("birthday", msg, duration=5.0)
            duck_sounds.level_up()
            self.achievements.unlock("happy_birthday")

            # Birthday bonus - extra coins!
            bonus_coins = birthday_info.age_days * 5
            self.habitat.add_currency(bonus_coins)
            self.renderer.show_message(f"Birthday bonus: +{bonus_coins} coins!", duration=3.0, category="event")

        # Check for milestone
        elif birthday_info.milestone:
            self.renderer.show_celebration("milestone", birthday_info.milestone, duration=4.0)
            duck_sounds.level_up()

            # Milestone bonuses
            if birthday_info.age_days >= 365:
                self.achievements.unlock("year_together")
            elif birthday_info.age_days >= 100:
                self.achievements.unlock("century_of_love")
            elif birthday_info.age_days >= 30:
                self.achievements.unlock("month_together")
            elif birthday_info.age_days >= 7:
                self.achievements.unlock("week_together")

    def _show_duck_fact(self):
        """Show a random duck fact."""
        fact = get_random_fact()
        self.renderer.show_message(f"Duck Fact: {fact}", duration=5.0)

        # Track facts shown
        self._statistics["facts_shown"] = self._statistics.get("facts_shown", 0) + 1

        if self._statistics["facts_shown"] >= 10:
            self.achievements.unlock("duck_scholar")
        if self._statistics["facts_shown"] >= 50:
            self.achievements.unlock("duck_professor")
    # ==================== QUESTS SYSTEM ====================

    def _show_quests_menu(self):
        """Show the quests menu with arrow-key navigation."""
        if not self.duck:
            return

        # Get available quests
        available = self.quests.get_available_quests(self.progression.level)
        active = list(self.quests.active_quests.values())

        # Build menu items
        items = []

        # Show active quests first
        for aq in active:
            from world.quests import QUESTS
            quest = QUESTS.get(aq.quest_id)
            if quest:
                step = quest.steps[aq.current_step] if aq.current_step < len(quest.steps) else None
                progress = f"Step {aq.current_step + 1}/{len(quest.steps)}"
                items.append(MenuItem(
                    id=aq.quest_id,
                    label=f"[Active] {quest.name}",
                    description=progress,
                    enabled=False,  # Can't start an active quest
                    data={"quest_id": aq.quest_id, "active": True}
                ))

        # Show available quests
        for quest in available:
            difficulty = quest.difficulty.value.title()
            items.append(MenuItem(
                id=quest.id,
                label=quest.name,
                description=f"{difficulty} - {quest.description[:40]}...",
                enabled=True,
                data={"quest_id": quest.id, "active": False}
            ))

        if not items:
            self.renderer.show_message("No quests available!\n\nComplete more activities to unlock quests.", duration=3.0)
            return

        self._quests_menu.set_items(items)
        self._quests_menu_open = True
        self._update_quests_menu_display()

    def _update_quests_menu_display(self):
        """Update the quests menu display."""
        items = self._quests_menu.get_items()
        selected_idx = self._quests_menu.get_selected_index()

        lines = ["=== QUESTS ===", ""]

        for i, item in enumerate(items):
            prefix = "> " if i == selected_idx else "  "
            lines.append(f"{prefix}{item.label}")
            if i == selected_idx and item.description:
                lines.append(f"    {item.description}")

        lines.append("")
        lines.append("[Up/Down] Navigate  [Enter] Start  [ESC/O] Close")

        self.renderer.show_overlay("\n".join(lines), duration=0)

    def _start_selected_quest(self, quest_id: str):
        """Start the selected quest."""
        success, message, dialogue = self.quests.start_quest(quest_id)
        if success:
            self.renderer.show_message(f"Quest started: {message}", duration=3.0)
            if dialogue:
                # Show first dialogue if available
                for line in dialogue[:3]:
                    self.renderer.show_message(line, duration=3.0)
        else:
            self.renderer.show_message(message, duration=3.0)

    # ==================== TRADING SYSTEM ====================

    def _show_trading_menu(self):
        """Show the trading post menu."""
        if not self.duck:
            return
        self._trading_menu_open = True
        self._trading_selected = 0
        self._render_trading_menu()

    def _render_trading_menu(self):
        """Render the trading menu with selection."""
        lines = [
            "+=============================================+",
            "|              TRADING POST                   |",
            "+=============================================+",
        ]
        
        # Get traders from trading system
        traders = list(self.trading.traders.values()) if hasattr(self.trading, 'traders') else []
        
        if traders:
            for i, trader in enumerate(traders[:5]):
                selected = "[>]" if i == self._trading_selected else "   "
                name = trader.name if hasattr(trader, 'name') else f"Trader {i+1}"
                specialty = trader.specialty if hasattr(trader, 'specialty') else "General"
                lines.append(f"| {selected} {name[:20]:20} ({specialty[:15]:15}) |")
        else:
            lines.append("|  No traders available right now...          |")
        
        lines.append("+=============================================+")
        lines.append("")
        lines.append("[^/v] Select  [Enter] Visit  [ESC/Backspace] Close")
        
        self.renderer.show_overlay("\n".join(lines), duration=0)

    def _handle_trading_input(self, key):
        """Handle input for trading menu."""
        key_str = str(key).lower()
        key_name = getattr(key, 'name', None) or ''
        
        # Close with ESC or Backspace
        if key_name == "KEY_ESCAPE" or key_name == "KEY_BACKSPACE":
            self._trading_menu_open = False
            self.renderer.dismiss_overlay()
            return
        
        # Navigate traders
        traders = list(self.trading.traders.values()) if hasattr(self.trading, 'traders') else []
        max_traders = min(5, len(traders))
        
        if key_name == "KEY_UP":
            if self._trading_selected > 0:
                self._trading_selected -= 1
                self._render_trading_menu()
            return
        
        if key_name == "KEY_DOWN":
            if self._trading_selected < max_traders - 1:
                self._trading_selected += 1
                self._render_trading_menu()
            return
        
        # Visit trader with Enter
        if key_name == "KEY_ENTER" and traders:
            trader = traders[self._trading_selected]
            self._trading_menu_open = False
            self.renderer.dismiss_message()
            self._visit_trader(trader)
            return
        
        # Number key quick select
        if key_str.isdigit() and 1 <= int(key_str) <= max_traders:
            self._trading_selected = int(key_str) - 1
            if traders:
                trader = traders[self._trading_selected]
                self._trading_menu_open = False
                self.renderer.dismiss_message()
                self._visit_trader(trader)
            return

    def _visit_trader(self, trader):
        """Visit a trader to see their wares."""
        # Show trader's inventory
        if hasattr(trader, 'get_inventory'):
            items = trader.get_inventory()
            lines = [f"=== {trader.name}'s Wares ===", ""]
            for item in items[:10]:
                name = item.name if hasattr(item, 'name') else str(item)
                price = item.price if hasattr(item, 'price') else 0
                lines.append(f"  {name[:30]:30} - {price} coins")
            lines.append("")
            lines.append("[Press any key to leave]")
            self.renderer.show_overlay("\n".join(lines), duration=0)
        else:
            self.renderer.show_message(f"Visited {trader.name if hasattr(trader, 'name') else 'trader'}!", duration=3.0)

    # ==================== WEATHER ACTIVITIES ====================

    def _show_weather_activities(self):
        """Show weather-specific activities."""
        if not self.duck:
            return

        # Get current weather
        weather = self.atmosphere.current_weather.weather_type.value if self.atmosphere.current_weather else "sunny"
        
        # Get available activities
        activities = self.weather_activities.get_available_activities(weather)
        
        # Build menu items
        from ui.menu_selector import MenuItem
        self._weather_menu.clear_items()
        for i, activity in enumerate(activities):
            desc = f"{activity.description[:35]}... ({activity.duration_seconds}s)"
            self._weather_menu.add_item(MenuItem(
                id=str(i),
                label=activity.name,
                description=desc,
                enabled=True,
                data=activity
            ))
        
        if not activities:
            self._weather_menu.add_item(MenuItem(
                id="none",
                label="No activities available",
                description="Check back when weather changes!",
                enabled=False
            ))
        
        # Show menu
        self._weather_menu_open = True
        self._update_weather_menu_display(weather)

    def _update_weather_menu_display(self, weather: str = None):
        """Update the weather activities menu display with current selection."""
        if weather is None:
            weather = self.atmosphere.current_weather.weather_type.value if self.atmosphere.current_weather else "sunny"
        
        items = [{'label': item.label, 'description': item.description, 'enabled': item.enabled}
                 for item in self._weather_menu.get_items()]
        self.renderer.show_menu(
            f"WEATHER ACTIVITIES ({weather.upper()})",
            items,
            self._weather_menu.get_selected_index(),
            footer="[^v] Navigate  [Enter] Start  [W/ESC] Close"
        )

    def _handle_weather_input_direct(self, key):
        """Handle input while in weather activities menu."""
        key_str = str(key).lower() if not key.is_sequence else str(key)
        
        # Arrow key navigation
        if key.name == "KEY_UP":
            idx = self._weather_menu.get_selected_index()
            if idx > 0:
                self._weather_menu.set_selected_index(idx - 1)
                self._update_weather_menu_display()
            return
        if key.name == "KEY_DOWN":
            idx = self._weather_menu.get_selected_index()
            items = self._weather_menu.get_items()
            if idx < len(items) - 1:
                self._weather_menu.set_selected_index(idx + 1)
                self._update_weather_menu_display()
            return
        
        # Select with Enter
        if key.name == "KEY_ENTER" or key_str == ' ':
            selected = self._weather_menu.get_selected_item()
            if selected and selected.data and selected.enabled:
                activity = selected.data
                weather = self.atmosphere.current_weather.weather_type.value if self.atmosphere.current_weather else "sunny"
                result = self.weather_activities.start_activity(activity.id, weather)
                
                self._weather_menu_open = False
                self.renderer.dismiss_message()
                if result:
                    self.renderer.show_message(f"Started: {result.name}\n{result.description}\nDuration: {result.duration_seconds}s", duration=3)
                else:
                    self.renderer.show_message("Couldn't start activity - already busy!", duration=2)
            return
        
        # Close with ESC, Backspace, W, or B
        if key.name == "KEY_ESCAPE" or key.name == "KEY_BACKSPACE" or key_str in ('w', 'b'):
            self._weather_menu_open = False
            self.renderer.dismiss_message()
            return
        
        # Also support number key selection for backwards compatibility
        if key_str.isdigit() and key_str != '0':
            idx = int(key_str) - 1  # Convert to 0-based index
            items = self._weather_menu.get_items()
            if 0 <= idx < len(items) and items[idx].enabled:
                self._weather_menu.set_selected_index(idx)
                # Trigger selection
                selected = self._weather_menu.get_selected_item()
                if selected and selected.data:
                    activity = selected.data
                    weather = self.atmosphere.current_weather.weather_type.value if self.atmosphere.current_weather else "sunny"
                    result = self.weather_activities.start_activity(activity.id, weather)
                    
                    self._weather_menu_open = False
                    self.renderer.dismiss_message()
                    if result:
                        self.renderer.show_message(f"Started: {result.name}\n{result.description}\nDuration: {result.duration_seconds}s", duration=3)
                    else:
                        self.renderer.show_message("Couldn't start activity - already busy!", duration=2)
            return

    # ==================== WEATHER ACTIVITY COMPLETION ====================

    def _update_weather_activity(self):
        """Check for weather activity completion and apply rewards."""
        if not self.weather_activities.current_activity:
            return
        
        result = self.weather_activities.check_activity_complete()
        if not result:
            return
        
        activity, rewards = result
        
        # Apply rewards
        if self.duck:
            # Add coins
            self.habitat.add_coins(rewards["coins"])
            
            # Add XP
            new_level = self.progression.add_xp(rewards["xp"])
            if new_level:
                self._show_level_up(new_level)
            
            # Apply mood bonus
            self.duck.needs.fun = min(100, self.duck.needs.fun + rewards["mood_bonus"])
            
            # Handle special drops
            if rewards["special_drop"]:
                self.inventory.add_item(rewards["special_drop"])
        
        # Show completion message with animation
        lines = activity.ascii_animation if activity.ascii_animation else []
        lines.extend([
            "",
            f"(!) {rewards['message']}",
            f"+{rewards['coins']} coins  +{rewards['xp']} XP",
        ])
        if rewards["special_drop"]:
            lines.append(f"Found: {rewards['special_drop']}!")
        
        self.renderer.show_message("\n".join(lines), duration=4.0)
        duck_sounds.quack("happy")
        
        # Check for achievements
        if self.weather_activities.total_activities_done >= 10:
            self.achievements.unlock("weather_watcher")
        if self.weather_activities.total_activities_done >= 50:
            self.achievements.unlock("weather_master")

    # ==================== TREASURE HUNTING INTERACTIVE ====================

    def _show_treasure_hunt(self):
        """Show the interactive treasure hunting menu."""
        if not self.duck:
            return
        
        self._treasure_menu_open = True
        self._treasure_menu_selected = 0
        self._update_treasure_menu_display()

    def _update_treasure_menu_display(self):
        """Update the treasure hunting menu display."""
        stats = self.treasure.get_collection_stats()
        
        lines = [
            "+==========================================+",
            "|        [D] TREASURE HUNTING [D]           |",
            "+==========================================+",
            f"| Collection: {stats['found_types']}/{stats['total_types']} ({stats['completion']}%)",
            f"| Total Value: {stats['total_value']:,} coins",
            f"| Digs Today: {self.treasure.dig_attempts_today}/{self.treasure.max_digs_per_day}",
            f"| Maps: {stats['maps_available']} available",
            "+==========================================+",
            "",
        ]
        
        # Build menu items
        menu_items = []
        
        # If currently hunting, show dig option
        if self.treasure.current_hunt_location:
            loc = self.treasure.current_hunt_location.value.title()
            progress = self.treasure.hunt_progress
            progress_bar = "[" + "#" * (progress // 10) + "-" * (10 - progress // 10) + "]"
            lines.append(f"  Currently at: {loc}")
            lines.append(f"  Progress: {progress_bar} {progress}%")
            lines.append("")
            menu_items.append(("dig", "DIG!", "Search for treasure"))
            menu_items.append(("leave", "Leave Area", "Stop hunting here"))
        else:
            # Show location options
            lines.append("  Select a location to hunt:")
            lines.append("")
            for loc in self.treasure.unlocked_locations:
                menu_items.append((f"loc_{loc.value}", loc.value.title(), f"Hunt at {loc.value}"))
        
        # Add map option if available
        unused_maps = [m for m in self.treasure.treasure_maps if not m.found]
        if unused_maps and not self.treasure.current_hunt_location:
            menu_items.append(("use_map", f"Use Map ({len(unused_maps)})", "Follow a treasure map"))
        
        # Add collection view
        menu_items.append(("collection", "View Collection", "See found treasures"))
        
        # Draw menu items with selection
        for i, (item_id, label, desc) in enumerate(menu_items):
            prefix = " >" if i == self._treasure_menu_selected else "  "
            lines.append(f"{prefix} [{i+1}] {label}")
            if i == self._treasure_menu_selected:
                lines.append(f"      {desc}")
        
        lines.extend([
            "",
            "+==========================================+",
            "| [^v] Navigate  [Enter] Select  [ESC] Close |",
            "+==========================================+",
        ])
        
        self._treasure_menu_items = menu_items
        self.renderer.show_overlay("\n".join(lines), duration=0)

    def _handle_treasure_input(self, key):
        """Handle input in treasure hunting menu."""
        key_str = str(key).lower() if not key.is_sequence else str(key)
        key_name = key.name if hasattr(key, 'name') else ''
        
        # Navigate
        if key_name == "KEY_UP":
            if self._treasure_menu_selected > 0:
                self._treasure_menu_selected -= 1
                self._update_treasure_menu_display()
            return
        if key_name == "KEY_DOWN":
            if self._treasure_menu_selected < len(self._treasure_menu_items) - 1:
                self._treasure_menu_selected += 1
                self._update_treasure_menu_display()
            return
        
        # Select
        if key_name == "KEY_ENTER" or key_str == ' ':
            self._treasure_select_current()
            return
        
        # Number keys
        if key_str.isdigit() and key_str != '0':
            idx = int(key_str) - 1
            if 0 <= idx < len(self._treasure_menu_items):
                self._treasure_menu_selected = idx
                self._treasure_select_current()
            return
        
        # Quick dig with D
        if key_str == 'd' and self.treasure.current_hunt_location:
            self._do_treasure_dig()
            return
        
        # Close with ESC, Backspace, or B
        if key_name == "KEY_ESCAPE" or key_name == "KEY_BACKSPACE" or key_str == 'b':
            self._treasure_menu_open = False
            self.renderer.dismiss_message()
            return

    def _treasure_select_current(self):
        """Execute the current treasure menu selection."""
        if not self._treasure_menu_items:
            return
        
        item_id, label, desc = self._treasure_menu_items[self._treasure_menu_selected]
        
        if item_id == "dig":
            self._do_treasure_dig()
        elif item_id == "leave":
            self.treasure.current_hunt_location = None
            self.treasure.hunt_progress = 0
            self.renderer.show_message("Left the hunting area.", duration=2)
            self._treasure_menu_selected = 0
            self._update_treasure_menu_display()
        elif item_id.startswith("loc_"):
            location_str = item_id[4:]
            from world.treasure import TreasureLocation
            try:
                location = TreasureLocation(location_str)
                success, msg = self.treasure.start_hunt(location)
                if success:
                    self._treasure_menu_selected = 0
                    self._update_treasure_menu_display()
                else:
                    self.renderer.show_message(msg, duration=2)
            except ValueError:
                self.renderer.show_message("Invalid location!", duration=2)
        elif item_id == "use_map":
            self._show_treasure_map_selection()
        elif item_id == "collection":
            self._show_treasure_collection()

    def _do_treasure_dig(self):
        """Perform a treasure dig."""
        success, message, found = self.treasure.dig()
        
        if found:
            # Found treasure!
            from world.treasure import TREASURES
            treasure = TREASURES.get(found.treasure_id)
            if treasure:
                # Add rewards
                self.habitat.add_coins(treasure.coin_value)
                new_level = self.progression.add_xp(treasure.xp_value)
                if new_level:
                    self._show_level_up(new_level)
                
                # Show treasure found animation
                lines = [
                    "+==========================================+",
                    "|          [D] TREASURE FOUND! [D]          |",
                    "+==========================================+",
                    "",
                    f"          {treasure.ascii_art}",
                    "",
                    f"   {treasure.name}",
                    f"   {treasure.description}",
                    "",
                    f"   Rarity: {treasure.rarity.value.upper()}",
                    f"   +{treasure.coin_value} coins  +{treasure.xp_value} XP",
                    "",
                    f'   "{treasure.lore}"',
                    "",
                    "+==========================================+",
                    "|     [Press any key to continue]          |",
                    "+==========================================+",
                ]
                self.renderer.show_overlay("\n".join(lines), duration=0)
                duck_sounds.quack("excited")
                
                # Achievements
                if self.treasure.total_treasures_found >= 10:
                    self.achievements.unlock("treasure_hunter")
                if self.treasure.total_treasures_found >= 50:
                    self.achievements.unlock("treasure_master")
        else:
            # Still digging
            progress = self.treasure.hunt_progress
            dig_art = [
                "       d       ",
                "      [_]      ",
                "   *digging*   ",
                f"   Progress: {progress}%",
            ]
            lines = dig_art + ["", message]
            self.renderer.show_message("\n".join(lines), duration=2)
        
        # Update display after a moment
        if not found:
            self._update_treasure_menu_display()

    def _show_treasure_map_selection(self):
        """Show available treasure maps."""
        unused_maps = [m for m in self.treasure.treasure_maps if not m.found]
        if not unused_maps:
            self.renderer.show_message("No treasure maps available!", duration=2)
            return
        
        lines = [
            "+==========================================+",
            "|          TREASURE MAPS                   |",
            "+==========================================+",
        ]
        
        for i, tmap in enumerate(unused_maps[:5], 1):
            from world.treasure import TREASURES
            treasure = TREASURES.get(tmap.treasure_id)
            name = treasure.name if treasure else "???"
            lines.append(f"  [{i}] Map to: {name}")
            lines.append(f"      Location: {tmap.location.value.title()}")
            lines.append(f"      Hint: {tmap.hint}")
            lines.append("")
        
        lines.append("[1-5] Use map  [ESC] Back")
        self.renderer.show_overlay("\n".join(lines), duration=0)

    def _show_treasure_collection(self):
        """Show treasure collection."""
        lines = self.treasure.render_collection()
        lines.append("")
        lines.append("[Press any key to return]")
        self.renderer.show_overlay("\n".join(lines), duration=0)

    # ==================== FESTIVAL ACTIVITIES INTERACTIVE ====================

    def _show_festival_menu(self):
        """Show the interactive festival activities menu."""
        if not self.duck:
            return
        
        self._festival_menu_open = True
        self._festival_menu_selected = 0
        self._update_festival_menu_display()

    def _update_festival_menu_display(self):
        """Update the festival menu display."""
        # Check for active festival
        active = self.festivals.check_active_festival()
        status = self.festivals.get_festival_status()
        
        if not active:
            lines = [
                "+==========================================+",
                "|           (!) FESTIVALS (!)               |",
                "+==========================================+",
                "",
                "  No festival is currently active.",
                "",
                "  Festivals occur during special times",
                "  throughout the year!",
                "",
                "  Check back during:",
                "  - Spring Bloom (March 20-April 3)",
                "  - Summer Splash (June 21-July 5)",
                "  - Autumn Harvest (Sept 22-Oct 6)",
                "  - Winter Wonder (Dec 21-Jan 4)",
                "",
                "+==========================================+",
                "|            [ESC] Close                   |",
                "+==========================================+",
            ]
            self.renderer.show_overlay("\n".join(lines), duration=0)
            self._festival_menu_items = []
            return
        
        from world.festivals import FESTIVALS
        festival = FESTIVALS.get(active.id)
        if not festival:
            self._festival_menu_open = False
            return
        
        lines = [
            "+==========================================+",
            f"|   (!) {festival.name.upper()[:30]:^30} (!)   |",
            "+==========================================+",
            f"| {festival.description[:40]}",
        ]
        
        if status:
            lines.extend([
                f"| Points: {status['points']}",
                f"| Activities Done: {status['activities_done']}",
                f"| Rewards Claimed: {status['rewards_claimed']}",
            ])
        else:
            lines.append("| [Not yet joined - select activity to start!]")
        
        lines.extend([
            "+==========================================+",
            "",
            "  ACTIVITIES:",
        ])
        
        menu_items = []
        for i, activity in enumerate(festival.activities):
            # Check cooldown
            daily_count = 0
            if status:
                daily_count = status.get('daily_activities', {}).get(activity.id, 0)
            
            available = daily_count < activity.max_daily
            status_str = f"({daily_count}/{activity.max_daily})" if not available else ""
            
            menu_items.append((activity.id, activity.name, activity.description, available))
            
            prefix = " >" if i == self._festival_menu_selected else "  "
            avail_mark = "" if available else " [DONE]"
            lines.append(f"{prefix} [{i+1}] {activity.name} +{activity.participation_points}pts{avail_mark}")
        
        # Add rewards section
        if status and status['points'] > 0:
            lines.extend([
                "",
                "  REWARDS:",
            ])
            for i, reward in enumerate(festival.exclusive_rewards):
                required = (i + 1) * 100
                claimed = reward.name in (self.festivals.current_festival_progress.rewards_claimed if self.festivals.current_festival_progress else [])
                if claimed:
                    lines.append(f"    [*] {reward.name} - CLAIMED!")
                elif status['points'] >= required:
                    menu_items.append((f"reward_{i}", f"Claim: {reward.name}", reward.description, True))
                    lines.append(f"    [!] {reward.name} - {required} pts - AVAILABLE!")
                else:
                    lines.append(f"    [ ] {reward.name} - {required} pts needed")
        
        lines.extend([
            "",
            "+==========================================+",
            "| [^v] Navigate  [Enter] Do  [ESC] Close    |",
            "+==========================================+",
        ])
        
        self._festival_menu_items = menu_items
        self.renderer.show_overlay("\n".join(lines), duration=0)

    def _handle_festival_input(self, key):
        """Handle input in festival menu."""
        key_str = str(key).lower() if not key.is_sequence else str(key)
        key_name = key.name if hasattr(key, 'name') else ''
        
        # Navigate
        if key_name == "KEY_UP":
            if self._festival_menu_selected > 0:
                self._festival_menu_selected -= 1
                self._update_festival_menu_display()
            return
        if key_name == "KEY_DOWN":
            if self._festival_menu_selected < len(self._festival_menu_items) - 1:
                self._festival_menu_selected += 1
                self._update_festival_menu_display()
            return
        
        # Select
        if key_name == "KEY_ENTER" or key_str == ' ':
            self._festival_select_current()
            return
        
        # Number keys
        if key_str.isdigit() and key_str != '0':
            idx = int(key_str) - 1
            if 0 <= idx < len(self._festival_menu_items):
                self._festival_menu_selected = idx
                self._festival_select_current()
            return
        
        # Close with ESC, Backspace, or B
        if key_name == "KEY_ESCAPE" or key_name == "KEY_BACKSPACE" or key_str == 'b':
            self._festival_menu_open = False
            self.renderer.dismiss_message()
            return

    def _festival_select_current(self):
        """Execute the current festival menu selection."""
        if not self._festival_menu_items:
            return
        
        item_id, label, desc, available = self._festival_menu_items[self._festival_menu_selected]
        
        if not available:
            self.renderer.show_message("Activity not available right now!", duration=2)
            return
        
        if item_id.startswith("reward_"):
            # Claim reward
            reward_idx = int(item_id[7:])
            success, msg, reward = self.festivals.claim_festival_reward(reward_idx)
            if success:
                if reward:
                    # Add to inventory if applicable
                    if reward.item_type == "cosmetic":
                        self.inventory.add_item(reward.name.lower().replace(" ", "_"))
                    new_level = self.progression.add_xp(reward.xp_value)
                    if new_level:
                        self._show_level_up(new_level)
                self.renderer.show_message(msg, duration=3)
                duck_sounds.quack("excited")
            else:
                self.renderer.show_message(msg, duration=2)
            self._update_festival_menu_display()
        else:
            # Do activity
            success, msg, reward = self.festivals.do_festival_activity(item_id)
            if success:
                # Show activity completion
                lines = [
                    "+==========================================+",
                    "|         (!) ACTIVITY COMPLETE! (!)        |",
                    "+==========================================+",
                    "",
                    f"  {label}",
                    "",
                    msg,
                ]
                if reward:
                    lines.append(f"  Got: {reward.name}!")
                    if reward.item_type in ("consumable", "material"):
                        self.inventory.add_item(reward.name.lower().replace(" ", "_"))
                    new_level = self.progression.add_xp(reward.xp_value)
                    if new_level:
                        self._show_level_up(new_level)
                
                lines.extend([
                    "",
                    "+==========================================+",
                ])
                self.renderer.show_message("\n".join(lines), duration=3)
                duck_sounds.quack("happy")
                
                # Check achievements
                if self.festivals.current_festival_progress:
                    total_done = sum(self.festivals.current_festival_progress.activities_completed.values())
                    if total_done >= 10:
                        self.achievements.unlock("festival_goer")
                    if total_done >= 50:
                        self.achievements.unlock("festival_master")
            else:
                self.renderer.show_message(msg, duration=2)
            
            self._update_festival_menu_display()

    # ==================== DEBUG MENU (HIDDEN) ====================
    
    def _handle_debug_input(self, key):
        """Handle input in the hidden debug menu."""
        key_str = str(key).lower()
        key_name = key.name if hasattr(key, 'name') else ''
        
        # Close with ESC, Backspace, or backtick
        if key_name == "KEY_ESCAPE" or key_name == "KEY_BACKSPACE" or key_str in ('`', '~'):
            if self._debug_submenu:
                self._debug_submenu = None
                self._debug_submenu_selected = 0
                self._debug_submenu_page = 0
                self._show_debug_menu()
            else:
                self._debug_menu_open = False
                self.renderer.dismiss_overlay()
            return
        
        # Page navigation with LEFT/RIGHT in submenus
        if self._debug_submenu and key_name == "KEY_LEFT":
            if self._debug_submenu_page > 0:
                self._debug_submenu_page -= 1
                self._debug_submenu_selected = 0
            self._show_debug_menu()
            return
        if self._debug_submenu and key_name == "KEY_RIGHT":
            all_items = self._get_debug_submenu_items()
            max_pages = (len(all_items) - 1) // self._debug_items_per_page
            if self._debug_submenu_page < max_pages:
                self._debug_submenu_page += 1
                self._debug_submenu_selected = 0
            self._show_debug_menu()
            return
        
        # Navigate with arrows
        if key_name == "KEY_UP":
            if self._debug_submenu:
                self._debug_submenu_selected = max(0, self._debug_submenu_selected - 1)
            else:
                self._debug_menu_selected = max(0, self._debug_menu_selected - 1)
            self._show_debug_menu()
            return
        if key_name == "KEY_DOWN":
            if self._debug_submenu:
                # Get items on current page
                all_items = self._get_debug_submenu_items()
                start_idx = self._debug_submenu_page * self._debug_items_per_page
                page_items = all_items[start_idx:start_idx + self._debug_items_per_page]
                max_idx = len(page_items) - 1
                self._debug_submenu_selected = min(max_idx, self._debug_submenu_selected + 1)
            else:
                self._debug_menu_selected = min(10, self._debug_menu_selected + 1)  # 11 items (0-10)
            self._show_debug_menu()
            return
        
        # Select with Enter or number keys
        if key_name == "KEY_ENTER":
            self._debug_select_current()
            return
        
        # T key for autotest
        if key_str in ('t', 'T') and not self._debug_submenu:
            self._debug_menu_selected = 10  # AutoTest is index 10
            self._debug_select_current()
            return
        
        # Number key shortcuts (select item on current page)
        if key_str.isdigit():
            idx = int(key_str) - 1 if key_str != '0' else 9
            if self._debug_submenu:
                # Select item on current page
                if 0 <= idx < self._debug_items_per_page:
                    all_items = self._get_debug_submenu_items()
                    start_idx = self._debug_submenu_page * self._debug_items_per_page
                    page_items = all_items[start_idx:start_idx + self._debug_items_per_page]
                    if idx < len(page_items):
                        self._debug_submenu_selected = idx
                        self._debug_select_current()
            else:
                if 0 <= idx < 9:
                    self._debug_menu_selected = idx
                    self._debug_select_current()
            return
    
    def _get_debug_submenu_items(self):
        """Get items for current debug submenu."""
        if self._debug_submenu == "weather":
            from world.atmosphere import WeatherType
            return [w.value for w in WeatherType]
        elif self._debug_submenu == "events":
            from world.events import EVENTS
            return list(EVENTS.keys())[:15]  # First 15 events
        elif self._debug_submenu == "visitor":
            return ["adventurous", "scholarly", "artistic", "playful", 
                    "mysterious", "generous", "foodie", "athletic"]
        elif self._debug_submenu == "needs":
            return ["max_all", "hunger_0", "energy_0", "fun_0", "clean_0", "social_0"]
        elif self._debug_submenu == "money":
            return ["+100", "+1000", "+10000", "=0"]
        elif self._debug_submenu == "friendship":
            return ["stranger", "acquaintance", "friend", "close_friend", "best_friend"]
        elif self._debug_submenu == "time":
            return ["advance_1h", "advance_6h", "advance_1d", "set_dawn", "set_noon", "set_dusk", "set_night"]
        elif self._debug_submenu == "misc":
            return ["spawn_treasure", "unlock_all_areas", "max_xp", "trigger_dream", "spawn_rainbow"]
        elif self._debug_submenu == "age":
            return ["egg", "hatchling", "duckling", "juvenile", "young_adult", "adult", "mature", "elder", "legendary", "+1_day", "+7_days", "+30_days"]
        elif self._debug_submenu == "building":
            return ["give_all_materials", "complete_build", "unlock_blueprints", "clear_structures"]
        elif self._debug_submenu == "autotest":
            return ["run_full_test", "run_quick_test", "view_last_report"]
        return []
    
    def _debug_select_current(self):
        """Execute the currently selected debug option."""
        if not self._debug_submenu:
            # Main menu selection
            menus = ["weather", "events", "visitor", "needs", "money", "friendship", "time", "misc", "age", "building", "autotest"]
            if 0 <= self._debug_menu_selected < len(menus):
                self._debug_submenu = menus[self._debug_menu_selected]
                self._debug_submenu_selected = 0
                self._debug_submenu_page = 0  # Reset page on entering submenu
                self._show_debug_menu()
            return
        
        # Submenu selection - account for pagination
        all_items = self._get_debug_submenu_items()
        start_idx = self._debug_submenu_page * self._debug_items_per_page
        actual_idx = start_idx + self._debug_submenu_selected
        
        if not (0 <= actual_idx < len(all_items)):
            return
        
        selected = all_items[actual_idx]
        
        if self._debug_submenu == "weather":
            self._debug_set_weather(selected)
        elif self._debug_submenu == "events":
            self._debug_trigger_event(selected)
        elif self._debug_submenu == "visitor":
            self._debug_spawn_visitor(selected)
        elif self._debug_submenu == "needs":
            self._debug_set_needs(selected)
        elif self._debug_submenu == "money":
            self._debug_set_money(selected)
        elif self._debug_submenu == "friendship":
            self._debug_set_friendship(selected)
        elif self._debug_submenu == "time":
            self._debug_set_time(selected)
        elif self._debug_submenu == "misc":
            self._debug_misc_action(selected)
        elif self._debug_submenu == "age":
            self._debug_set_age(selected)
        elif self._debug_submenu == "building":
            self._debug_building_action(selected)
        elif self._debug_submenu == "autotest":
            self._debug_run_autotest(selected)
    
    def _debug_set_weather(self, weather_type: str):
        """Set weather to specified type."""
        from world.atmosphere import WeatherType, Weather, WEATHER_DATA
        from datetime import datetime
        
        try:
            wtype = WeatherType(weather_type)
            data = WEATHER_DATA.get(wtype, {})
            self.atmosphere.current_weather = Weather(
                weather_type=wtype,
                intensity=1.0,
                duration_hours=2.0,
                start_time=datetime.now().isoformat(),
                mood_modifier=data.get("mood_modifier", 0),
                xp_multiplier=data.get("xp_multiplier", 1.0),
                special_message=data.get("message", f"Weather set to {weather_type}"),
            )
            self.renderer.show_message(f"# DEBUG: Weather set to {weather_type.upper()}", duration=2)
        except:
            self.renderer.show_message(f"# DEBUG: Failed to set weather", duration=2)
        
        self._debug_menu_open = False
        self.renderer.dismiss_overlay()
        self._debug_submenu = None
    
    def _debug_trigger_event(self, event_id: str):
        """Trigger a specific event."""
        from world.events import EVENTS
        
        if event_id in EVENTS and self.duck:
            event = EVENTS[event_id]
            # Apply event effects
            for need, change in event.effects.items():
                if hasattr(self.duck.needs, need):
                    old_val = getattr(self.duck.needs, need)
                    new_val = max(0, min(100, old_val + change))
                    setattr(self.duck.needs, need, new_val)
            
            # Start event animation if available
            if event.has_animation and event_id in ANIMATED_EVENTS:
                self._start_event_animation(event_id)
                self.renderer.show_message(f"# DEBUG: {event.message}", duration=5)
            else:
                self.renderer.show_message(f"# DEBUG: {event.message}", duration=3)
        else:
            self.renderer.show_message(f"# DEBUG: Event '{event_id}' triggered", duration=2)
        
        self._debug_menu_open = False
        self.renderer.dismiss_overlay()
        self._debug_submenu = None
    
    def _debug_spawn_visitor(self, personality: str):
        """Spawn a visitor with specified personality."""
        from world.friends import visitor_animator, DuckPersonalityType, FriendshipLevel, DUCK_NAMES
        import random
        from datetime import datetime
        
        # Create or get a friend with this personality
        name = random.choice(DUCK_NAMES.get(personality, ["Debug Duck"]))
        friend_id = f"debug_{personality}"
        
        friend = self.friends.get_friend_by_id(friend_id)
        if not friend:
            from world.friends import DuckFriend
            friend = DuckFriend(
                id=friend_id,
                name=name,
                personality=DuckPersonalityType(personality),
                friendship_level=FriendshipLevel.FRIEND,
                first_met=datetime.now().isoformat(),
                times_visited=5
            )
            self.friends.friends[friend_id] = friend
        
        # Force a visit
        from world.friends import VisitEvent
        self.friends.current_visit = VisitEvent(
            friend_id=friend_id,
            started_at=datetime.now().isoformat(),
            duration_minutes=30
        )
        
        visitor_animator.set_visitor(
            personality, 
            friend.name,
            "friend",
            friend.times_visited,
            set(),
            duck_ref=self.duck,
            shared_memories=[]
        )
        
        greeting = visitor_animator.get_greeting(self.duck.name if self.duck else "Duck")
        self.renderer.show_message(f"# DEBUG: Spawned {personality} visitor\n{greeting}", duration=4)
        
        self._debug_menu_open = False
        self.renderer.dismiss_overlay()
        self._debug_submenu = None
    
    def _debug_set_needs(self, action: str):
        """Set duck needs."""
        if not self.duck:
            return
        
        if action == "max_all":
            self.duck.needs.hunger = 100
            self.duck.needs.energy = 100
            self.duck.needs.fun = 100
            self.duck.needs.clean = 100
            self.duck.needs.social = 100
            self.renderer.show_message("# DEBUG: All needs set to 100%", duration=2)
        elif action == "hunger_0":
            self.duck.needs.hunger = 0
            self.renderer.show_message("# DEBUG: Hunger set to 0%", duration=2)
        elif action == "energy_0":
            self.duck.needs.energy = 0
            self.renderer.show_message("# DEBUG: Energy set to 0%", duration=2)
        elif action == "fun_0":
            self.duck.needs.fun = 0
            self.renderer.show_message("# DEBUG: Fun set to 0%", duration=2)
        elif action == "clean_0":
            self.duck.needs.clean = 0
            self.renderer.show_message("# DEBUG: Cleanliness set to 0%", duration=2)
        elif action == "social_0":
            self.duck.needs.social = 0
            self.renderer.show_message("# DEBUG: Social set to 0%", duration=2)
        
        self._debug_menu_open = False
        self.renderer.dismiss_overlay()
        self._debug_submenu = None
    
    def _debug_set_money(self, action: str):
        """Set money amount."""
        if not self.duck:
            return

        if action == "+100":
            self.habitat.currency += 100
        elif action == "+1000":
            self.habitat.currency += 1000
        elif action == "+10000":
            self.habitat.currency += 10000
        elif action == "=0":
            self.habitat.currency = 0

        self.renderer.show_message(f"# DEBUG: Coins now ${self.habitat.currency}", duration=2)
        self._debug_menu_open = False
        self.renderer.dismiss_overlay()
        self._debug_submenu = None
    
    def _debug_set_friendship(self, level: str):
        """Set friendship level of current/recent visitor."""
        from world.friends import FriendshipLevel
        
        if self.friends.current_visit:
            friend = self.friends.get_friend_by_id(self.friends.current_visit.friend_id)
            if friend:
                friend.friendship_level = FriendshipLevel(level)
                self.renderer.show_message(f"# DEBUG: {friend.name} friendship set to {level}", duration=2)
            else:
                self.renderer.show_message("# DEBUG: No current visitor to modify", duration=2)
        elif self.friends.known_friends:
            # Modify most recent friend
            friend = self.friends.known_friends[-1]
            friend.friendship_level = FriendshipLevel(level)
            self.renderer.show_message(f"# DEBUG: {friend.name} friendship set to {level}", duration=2)
        else:
            self.renderer.show_message("# DEBUG: No friends to modify", duration=2)
        
        self._debug_menu_open = False
        self.renderer.dismiss_overlay()
        self._debug_submenu = None
    
    def _debug_set_time(self, action: str):
        """Manipulate time for testing."""
        from datetime import datetime, timedelta, date
        
        hours = 0
        if action == "advance_1h":
            hours = 1
        elif action == "advance_6h":
            hours = 6
        elif action == "advance_1d":
            hours = 24
        
        if hours > 0 and self.duck:
            # Convert hours to minutes for duck growth and needs
            minutes_to_add = hours * 60
            
            # Update duck needs (decay based on time passed)
            self.duck.needs.update(minutes_to_add, self.duck.personality)
            
            # Update duck growth progress
            self.duck._update_growth(minutes_to_add)
            
            # Update duck's created_at for age display (it's stored as ISO string)
            if hasattr(self.duck, 'created_at') and self.duck.created_at:
                if isinstance(self.duck.created_at, str):
                    # Parse ISO format string
                    created = datetime.fromisoformat(self.duck.created_at.replace('Z', '+00:00'))
                    if created.tzinfo is not None:
                        created = created.replace(tzinfo=None)
                    new_created = created - timedelta(hours=hours)
                    self.duck.created_at = new_created.isoformat()
                else:
                    new_created = self.duck.created_at - timedelta(hours=hours)
                    self.duck.created_at = new_created.isoformat()
            
            # Update AgingSystem birth_date if advancing by days
            if hours >= 24 and hasattr(self, 'aging') and self.aging and self.aging.birth_date:
                days = hours // 24
                birth = date.fromisoformat(self.aging.birth_date)
                new_birth = birth - timedelta(days=days)
                self.aging.birth_date = new_birth.strftime("%Y-%m-%d")
                new_stage = self.aging.update_stage()
                if new_stage:
                    self.duck.growth_stage = new_stage.value
                    self.duck.growth_progress = 0.0
            
            if hours >= 24:
                self.renderer.show_message(f"# DEBUG: Advanced time by {hours // 24} day(s)", duration=2)
            else:
                self.renderer.show_message(f"# DEBUG: Advanced time by {hours} hour(s)", duration=2)
        elif action == "set_dawn":
            self.renderer.show_message("# DEBUG: Time display simulating dawn (5 AM)", duration=2)
        elif action == "set_noon":
            self.renderer.show_message("# DEBUG: Time display simulating noon", duration=2)
        elif action == "set_dusk":
            self.renderer.show_message("# DEBUG: Time display simulating dusk (7 PM)", duration=2)
        elif action == "set_night":
            self.renderer.show_message("# DEBUG: Time display simulating night (11 PM)", duration=2)
        
        self._debug_menu_open = False
        self.renderer.dismiss_overlay()
        self._debug_submenu = None
    
    def _debug_misc_action(self, action: str):
        """Miscellaneous debug actions."""
        if action == "spawn_treasure":
            self.renderer.show_message("# DEBUG: Spawned treasure nearby!", duration=2)
        elif action == "unlock_all_areas":
            from world.exploration import AREAS
            for biome_areas in AREAS.values():
                for area in biome_areas:
                    area.is_discovered = True
                    self.exploration.discovered_areas[area.name] = area
            # Also max out player level so areas pass the level filter in menu
            self.exploration._player_level = 99
            self.renderer.show_message("# DEBUG: All exploration areas unlocked!", duration=2)
        elif action == "max_xp":
            # Set progression system level (this is what the game actually uses)
            # XP and level must be consistent: 99999 XP = level 99
            self.progression.xp = 99999
            self.progression.level = 99
            self.progression.title = "Legendary Duck Keeper"
            # Also update exploration system's player level for area unlocks
            self.exploration._player_level = 99
            self.renderer.show_message("# DEBUG: XP and level maxed! (Lv.99)", duration=2)
        elif action == "trigger_dream":
            if self.duck:
                self._dream_active = True
                mood = self.duck.get_mood()
                mood_score = int(mood.happiness) if hasattr(mood, 'happiness') else 50
                self._dream_result = self.dreams.generate_dream(mood_score, 50)
            self.renderer.show_message("# DEBUG: Dream triggered!", duration=2)
        elif action == "spawn_rainbow":
            self._debug_set_weather("rainbow")
            return  # Already handles menu close
        
        self._debug_menu_open = False
        self.renderer.dismiss_overlay()
        self._debug_submenu = None

    def _debug_set_age(self, action: str):
        """Set duck age or growth stage."""
        from duck.aging import GrowthStage
        from datetime import datetime, timedelta, date

        if not self.duck:
            self.renderer.show_message("DEBUG: No duck!", duration=2)
            self._debug_menu_open = False
            self.renderer.dismiss_overlay()
            self._debug_submenu = None
            return

        # Check if it's a time advancement
        if action.startswith("+"):
            days = 0
            if action == "+1_day":
                days = 1
            elif action == "+7_days":
                days = 7
            elif action == "+30_days":
                days = 30

            if days > 0:
                # Update the AgingSystem (self.aging) birth_date
                if hasattr(self, 'aging') and self.aging and self.aging.birth_date:
                    birth = date.fromisoformat(self.aging.birth_date)
                    new_birth = birth - timedelta(days=days)
                    self.aging.birth_date = new_birth.strftime("%Y-%m-%d")
                    # Update stage based on new age
                    new_stage = self.aging.update_stage()
                    if new_stage:
                        self.duck.growth_stage = new_stage.value
                        self.duck.growth_progress = 0.0

                # Also update the duck's created_at for display consistency
                if hasattr(self.duck, 'created_at') and self.duck.created_at:
                    if isinstance(self.duck.created_at, str):
                        created = datetime.fromisoformat(self.duck.created_at.replace('Z', '+00:00'))
                        if created.tzinfo is not None:
                            created = created.replace(tzinfo=None)
                        new_created = created - timedelta(days=days)
                        self.duck.created_at = new_created.isoformat()
                    else:
                        new_created = self.duck.created_at - timedelta(days=days)
                        self.duck.created_at = new_created.isoformat()

                # Advance growth_progress by simulating time passing
                minutes_to_add = days * 24 * 60  # Convert days to minutes
                self.duck._update_growth(minutes_to_add)

                self.renderer.show_message(f"DEBUG: Aged duck by {days} day(s)", duration=2)
            else:
                self.renderer.show_message("DEBUG: Invalid days", duration=2)
        else:
            # Set specific growth stage
            try:
                stage = GrowthStage(action)
                # Update the AgingSystem
                if hasattr(self, 'aging') and self.aging:
                    self.aging.current_stage = stage
                # Update duck's growth_stage
                if hasattr(self.duck, 'growth_stage'):
                    self.duck.growth_stage = action
                    self.duck.growth_progress = 0.0
                self.renderer.show_message(f"DEBUG: Set stage to {action}", duration=2)
            except ValueError:
                self.renderer.show_message(f"DEBUG: Unknown stage {action}", duration=2)

        self._debug_menu_open = False
        self.renderer.dismiss_overlay()
        self._debug_submenu = None

    def _debug_building_action(self, action: str):
        """Building-related debug actions."""
        from world.building import BLUEPRINTS, StructureStatus
        from world.materials import MATERIALS

        if action == "give_all_materials":
            # Give 50 of each common building material
            building_mats = [
                "twig", "grass_blade", "leaf", "moss", "feather", "woven_grass",
                "insulation", "shell", "clay_brick", "thatch", "wooden_plank",
                "rope", "stone_block", "sea_glass", "pebble", "smooth_stone",
                "sand", "seed", "wildflower", "garden_flower", "crystal"
            ]
            for mat_id in building_mats:
                if mat_id in MATERIALS:
                    self.materials.add_material(mat_id, 50)
            self.renderer.show_message("# DEBUG: Added 50 of each building material!", duration=2)
        elif action == "complete_build":
            if self.building.current_build:
                structure = self.building.current_build.structure
                bp = structure.blueprint
                if bp:
                    structure.current_stage = bp.stages
                    structure.stage_progress = 1.0
                    structure.status = StructureStatus.COMPLETE
                    self.building.current_build = None
                    self.renderer.show_message(f"# DEBUG: Completed {bp.name}!", duration=2)
                else:
                    self.renderer.show_message("# DEBUG: No blueprint found", duration=2)
            else:
                self.renderer.show_message("# DEBUG: No building in progress", duration=2)
        elif action == "unlock_blueprints":
            # Set player level high enough to unlock all blueprints
            if self.duck:
                self.duck.level = 25
            self.building._player_level = 25
            self.renderer.show_message("# DEBUG: All blueprints unlocked (level 25)!", duration=2)
        elif action == "clear_structures":
            self.building.structures.clear()
            self.building.occupied_cells.clear()
            self.building.current_build = None
            self.renderer.show_message("# DEBUG: Cleared all structures!", duration=2)

        self._debug_menu_open = False
        self.renderer.dismiss_overlay()
        self._debug_submenu = None

    def _debug_run_autotest(self, action: str):
        """Run automated game tests."""
        from core.automated_test import AutomatedGameTester
        import os
        
        self._debug_menu_open = False
        self.renderer.dismiss_overlay()
        self._debug_submenu = None
        
        if action == "run_full_test":
            self.renderer.show_message("# RUNNING FULL AUTOMATED TEST...\nThis may take a minute. Please wait.", duration=0)
            
            # Create tester and run
            tester = AutomatedGameTester(self)
            
            # Progress callback to update display
            def progress_cb(msg, current, total):
                pct = int((current / total) * 100)
                self.renderer.show_message(f"# TESTING ({pct}%)\n{msg}\n\n[{current}/{total}] categories tested", duration=0)
            
            tester.set_progress_callback(progress_cb)
            
            # Run all tests
            report = tester.run_all_tests()
            
            # Save report
            report_path = tester.save_report()
            
            # Show summary
            summary = f"""
# AUTOMATED TEST COMPLETE

Total Tests:  {report.total_tests}
  ✓ Passed:   {report.passed}
  ✗ Failed:   {report.failed}
  ⚠ Warnings: {report.warnings}
  ○ Skipped:  {report.skipped}

Pass Rate: {report.passed / max(1, report.total_tests) * 100:.1f}%

Report saved to:
{os.path.basename(report_path)}

[Press any key to continue]
"""
            self.renderer.show_message(summary, duration=0)
            
        elif action == "run_quick_test":
            self.renderer.show_message("# RUNNING QUICK TEST...", duration=0)
            
            # Quick test - just check core systems exist
            tester = AutomatedGameTester(self)
            
            # Only run critical tests
            tester._test_duck_state()
            tester._test_needs_system()
            tester._test_core_actions()
            tester._test_save_load_system()
            
            tester.report.ended_at = __import__('datetime').datetime.now().isoformat()
            report = tester.report
            
            summary = f"""
# QUICK TEST COMPLETE

Core Systems Tested: {report.total_tests}
  ✓ Passed:   {report.passed}
  ✗ Failed:   {report.failed}

{"✓ Core systems OK!" if report.failed == 0 else "✗ Issues found - run full test for details"}

[Press any key to continue]
"""
            self.renderer.show_message(summary, duration=0)
            
        elif action == "view_last_report":
            # Find and display most recent report
            import glob
            
            game_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            logs_dir = os.path.join(game_dir, "logs")
            reports = sorted(glob.glob(os.path.join(logs_dir, "test_report_*.txt")), reverse=True)
            
            if reports:
                # Read last report
                with open(reports[0], 'r') as f:
                    content = f.read()
                
                # Show first ~40 lines
                lines = content.split('\n')[:40]
                preview = '\n'.join(lines)
                if len(content.split('\n')) > 40:
                    preview += f"\n\n... ({len(content.split(chr(10))) - 40} more lines)"
                    preview += f"\n\nFull report: {os.path.basename(reports[0])}"
                
                self.renderer.show_message(preview, duration=0)
            else:
                self.renderer.show_message("# No test reports found.\n\nRun a test first!", duration=3)

    def _show_debug_menu(self):
        """Render the debug menu overlay."""
        lines = [
            "+===================================+",
            "|     # DEBUG MENU (HIDDEN) #     |",
            "+===================================+",
        ]
        
        if not self._debug_submenu:
            # Main menu
            options = [
                ("1", "Weather", "Set weather type"),
                ("2", "Events", "Trigger events"),
                ("3", "Visitor", "Spawn visitor"),
                ("4", "Needs", "Set duck needs"),
                ("5", "Money", "Add/set coins"),
                ("6", "Friendship", "Set friend level"),
                ("7", "Time", "Manipulate time"),
                ("8", "Misc", "Other debug options"),
                ("9", "Age", "Set duck age/stage"),
                ("0", "Building", "Building debug"),
                ("T", "AutoTest", "Run auto tests"),
            ]
            for i, (key, name, desc) in enumerate(options):
                prefix = ">" if i == self._debug_menu_selected else " "
                lines.append(f"| {prefix} [{key}] {name:<12} {desc:<16} |")
        else:
            # Submenu with pagination
            all_items = self._get_debug_submenu_items()
            total_items = len(all_items)
            total_pages = (total_items - 1) // self._debug_items_per_page + 1
            current_page = self._debug_submenu_page + 1
            
            # Page indicator
            page_str = f"({current_page}/{total_pages})" if total_pages > 1 else ""
            header = f"<< {self._debug_submenu.upper()} {page_str}"
            lines.append(f"|  {header:<32} |")
            lines.append("+===================================+")
            
            # Get items for current page
            start_idx = self._debug_submenu_page * self._debug_items_per_page
            end_idx = start_idx + self._debug_items_per_page
            page_items = all_items[start_idx:end_idx]
            
            for i, item in enumerate(page_items):
                prefix = ">" if i == self._debug_submenu_selected else " "
                key = str(i + 1) if i < 9 else "0" if i == 9 else " "
                display = item[:28] if len(item) > 28 else item
                lines.append(f"| {prefix} [{key}] {display:<28} |")
            
            # Add pagination hint if needed
            if total_pages > 1:
                lines.append("+===================================+")
                lines.append("|  [</>] Prev/Next Page             |")
        
        lines.extend([
            "+===================================+",
            "|  [^v] Navigate  [Enter] Select    |",
            "|  [ESC/`] Back/Close               |",
            "+===================================+",
        ])
        
        # Use show_overlay to avoid adding to chat log
        self.renderer.show_overlay("\n".join(lines), duration=0)

    # ==================== SETTINGS SYSTEM ====================

    def _handle_settings_input(self, key):
        """Handle input while settings menu is open."""
        key_str = str(key).lower()
        key_name = key.name if hasattr(key, 'name') else ''
        
        # Close with ESC or Backspace
        if key_name == "KEY_ESCAPE" or key_name == "KEY_BACKSPACE":
            # Check for unsaved changes
            if self._settings_menu.has_unsaved_changes():
                self._show_save_settings_prompt()
            else:
                self._close_settings_menu()
            return
        
        # Navigate categories (LEFT/RIGHT)
        if key_name == "KEY_LEFT":
            self._settings_menu.navigate_category(-1)
            self._render_settings_menu()
            return
        if key_name == "KEY_RIGHT":
            self._settings_menu.navigate_category(1)
            self._render_settings_menu()
            return
        
        # Navigate items (UP/DOWN)
        if key_name == "KEY_UP":
            self._settings_menu.navigate_item(-1)
            self._render_settings_menu()
            return
        if key_name == "KEY_DOWN":
            self._settings_menu.navigate_item(1)
            self._render_settings_menu()
            return
        
        # Adjust value (for sliders/choices)
        if key_str in ('-', '_', '[') or key_name == "KEY_LEFT":
            self._settings_menu.adjust_value(-1)
            self._render_settings_menu()
            return
        if key_str in ('=', '+', ']') or key_name == "KEY_RIGHT":
            self._settings_menu.adjust_value(1)
            self._render_settings_menu()
            return
        
        # Toggle/Select with Enter or Space
        if key_name == "KEY_ENTER" or key_str == ' ':
            result = self._settings_menu.select_current()
            if result == "save":
                self._save_and_apply_settings()
            elif result == "reset":
                self._show_reset_settings_prompt()
            self._render_settings_menu()
            return
        
        # Quick save with S
        if key_str == 's':
            self._save_and_apply_settings()
            return
        
        # Quick reset with R
        if key_str == 'r':
            self._show_reset_settings_prompt()
            return

    def _open_settings_menu(self):
        """Open the settings menu."""
        self._settings_menu_open = True
        self._settings_menu = settings_menu  # Use global instance
        self._settings_menu.reset_selection()
        self._render_settings_menu()

    def _close_settings_menu(self):
        """Close the settings menu without saving."""
        self._settings_menu_open = False
        self._settings_menu.discard_changes()
        self.renderer.dismiss_message()

    def _render_settings_menu(self):
        """Render the settings menu overlay."""
        lines = self._settings_menu.render()
        self.renderer.show_overlay("\n".join(lines), duration=0)

    def _save_and_apply_settings(self):
        """Save settings and apply them immediately."""
        self._settings_menu.save_changes()
        save_settings()
        self._apply_settings()
        notification_manager.show("Settings saved!", "success", 2.0)
        self._close_settings_menu()

    def _show_save_settings_prompt(self):
        """Show prompt to save unsaved settings changes."""
        self._confirmation_dialog = ConfirmationDialog(
            title="Unsaved Changes",
            message="You have unsaved settings changes.\nSave before closing?",
            on_confirm=self._save_and_apply_settings,
            on_cancel=self._close_settings_menu
        )
        self._confirmation_dialog.is_open = True
        self._render_confirmation_dialog()

    def _show_reset_settings_prompt(self):
        """Show prompt to confirm settings reset."""
        self._confirmation_dialog = ConfirmationDialog(
            title="Reset Settings?",
            message="Reset all settings to defaults?\nThis cannot be undone.",
            dangerous=True,
            on_confirm=self._reset_settings,
            on_cancel=lambda: None
        )
        self._confirmation_dialog.is_open = True
        self._render_confirmation_dialog()

    def _reset_settings(self):
        """Reset all settings to defaults."""
        settings_manager.reset_to_defaults()
        save_settings()
        self._apply_settings()
        self._settings_menu.reload_from_settings()
        notification_manager.show("Settings reset to defaults!", "info", 2.0)
        self._render_settings_menu()

    def _handle_confirmation_input(self, key):
        """Handle input for confirmation dialogs."""
        if not self._confirmation_dialog:
            return
        
        # Save reference before handle_input (callbacks may clear self._confirmation_dialog)
        dialog = self._confirmation_dialog
        
        # Use the dialog's built-in input handler
        from core.menu_controller import MenuResult
        result = self._confirmation_dialog.handle_input(key)
        
        # Check if dialog is still open (use saved reference)
        if dialog.is_open:
            self._render_confirmation_dialog()
        else:
            # Dialog closed (confirmed or cancelled)
            self._confirmation_dialog = None
            if self._settings_menu_open:
                self._render_settings_menu()
            else:
                self.renderer.dismiss_message()

    def _render_confirmation_dialog(self):
        """Render the confirmation dialog overlay."""
        if not self._confirmation_dialog:
            return
        lines = self._confirmation_dialog.get_display_lines()
        self.renderer.show_overlay("\n".join(lines), duration=0)

    # ==================== SCRAPBOOK SYSTEM ====================

    def _show_scrapbook(self):
        """Show the scrapbook/photo album."""
        if not self.duck:
            return

        self._scrapbook_menu_open = True
        self._render_scrapbook()
    
    def _render_scrapbook(self):
        """Render the current scrapbook page."""
        # Get scrapbook page display
        total_pages = len(self.scrapbook.pages) if self.scrapbook.pages else 1
        if self._scrapbook_page >= total_pages:
            self._scrapbook_page = max(0, total_pages - 1)
        
        lines = self.scrapbook.render_album_page(self._scrapbook_page)
        
        # Add navigation info
        lines.append("")
        lines.append(f"Page {self._scrapbook_page + 1}/{total_pages}")
        lines.append("")
        lines.append("[<-/->] Navigate Pages  [F] Toggle Favorite")
        lines.append("[ESC/Backspace] Close")
        
        scrapbook_text = "\n".join(lines)
        self.renderer.show_overlay(scrapbook_text)
    
    def _handle_scrapbook_input(self, key):
        """Handle input for scrapbook menu."""
        key_str = str(key).lower()
        key_name = key.name if hasattr(key, 'name') else ''
        
        # Close with ESC or Backspace
        if key_name == "KEY_ESCAPE" or key_name == "KEY_BACKSPACE":
            self._scrapbook_menu_open = False
            self.renderer.dismiss_overlay()
            return
        
        total_pages = len(self.scrapbook.pages) if self.scrapbook.pages else 1
        
        # Navigate pages
        if key_name == "KEY_LEFT":
            if self._scrapbook_page > 0:
                self._scrapbook_page -= 1
                self._render_scrapbook()
            return
        
        if key_name == "KEY_RIGHT":
            if self._scrapbook_page < total_pages - 1:
                self._scrapbook_page += 1
                self._render_scrapbook()
            return
        
        # Toggle favorite on current page
        if key_str == 'f':
            photos_on_page = self.scrapbook.get_page(self._scrapbook_page)
            if photos_on_page:
                # Toggle first photo on page (could add selection later)
                photo = photos_on_page[0]
                is_fav = self.scrapbook.toggle_favorite(photo.photo_id)
                status = "favorited" if is_fav else "unfavorited"
                self.renderer.show_message(f"Photo {status}!", duration=1.5)
            return

    # ==================== SECRETS BOOK ====================

    def _show_secrets_book(self):
        """Show the secrets and easter eggs book."""
        if not self.duck:
            return
        self._secrets_menu_open = True
        self._secrets_menu_page = 0
        self._render_secrets_menu()

    def _render_secrets_menu(self):
        """Render the secrets book with pagination."""
        all_secrets = self.secrets.render_secrets_book()
        
        # Pagination - show 10 lines per page
        items_per_page = 10
        total_pages = max(1, (len(all_secrets) + items_per_page - 1) // items_per_page)
        start_idx = self._secrets_menu_page * items_per_page
        end_idx = min(start_idx + items_per_page, len(all_secrets))
        page_secrets = all_secrets[start_idx:end_idx]
        
        lines = [
            "+=============================================+",
            f"|  SECRETS & EASTER EGGS (Page {self._secrets_menu_page + 1}/{total_pages})          |",
            "+=============================================+",
        ]
        
        for secret_line in page_secrets:
            lines.append(f"| {secret_line[:43]:43} |")
        
        # Pad to fill page
        while len(lines) < items_per_page + 3:
            lines.append("|                                             |")
        
        lines.append("+=============================================+")
        lines.append("")
        lines.append("[<-/->] Navigate Pages  [ESC/Backspace] Close")
        
        self.renderer.show_overlay("\n".join(lines))

    def _handle_secrets_input(self, key):
        """Handle input for secrets book menu."""
        key_name = getattr(key, 'name', None) or ''
        
        # Close with ESC or Backspace
        if key_name == "KEY_ESCAPE" or key_name == "KEY_BACKSPACE":
            self._secrets_menu_open = False
            self.renderer.dismiss_overlay()
            return
        
        # Navigate pages
        all_secrets = self.secrets.render_secrets_book()
        items_per_page = 10
        total_pages = max(1, (len(all_secrets) + items_per_page - 1) // items_per_page)
        
        if key_name == "KEY_LEFT":
            if self._secrets_menu_page > 0:
                self._secrets_menu_page -= 1
                self._render_secrets_menu()
            return
        
        if key_name == "KEY_RIGHT":
            if self._secrets_menu_page < total_pages - 1:
                self._secrets_menu_page += 1
                self._render_secrets_menu()
            return

    # ==================== PRESTIGE/LEGACY SYSTEM ====================

    def _show_prestige_menu(self):
        """Show the prestige/legacy system menu."""
        if not self.duck:
            return
        self._prestige_menu_open = True
        self._render_prestige_menu()

    def _render_prestige_menu(self):
        """Render the prestige menu."""
        # Get legacy screen display
        lines = self.prestige.render_legacy_screen()
        
        # Add prestige option if eligible
        can_prestige, prestige_msg = self.prestige.can_prestige(
            self.progression.level,
            self.duck.get_age_days()
        )
        
        lines.append("")
        if can_prestige:
            lines.append("+===============================================+")
            lines.append("|  * PRESTIGE AVAILABLE! *                    |")
            lines.append("|  Press [P] to prestige and start fresh!       |")
            lines.append("+===============================================+")
        else:
            lines.append(f"  Prestige: {prestige_msg}")
        
        lines.append("")
        lines.append("[P] Prestige  [T] Change Title  [ESC/Backspace] Close")
        
        prestige_text = "\n".join(lines)
        self.renderer.show_overlay(prestige_text)

    def _handle_prestige_input(self, key):
        """Handle input for prestige menu."""
        key_str = str(key).lower()
        key_name = getattr(key, 'name', None) or ''
        
        # Close with ESC or Backspace
        if key_name == "KEY_ESCAPE" or key_name == "KEY_BACKSPACE":
            self._prestige_menu_open = False
            self.renderer.dismiss_overlay()
            return
        
        # Prestige action
        if key_str == 'p':
            self._prestige_menu_open = False
            self.renderer.dismiss_overlay()
            self._perform_prestige()
            return
        
        # Change title
        if key_str == 't':
            self._prestige_menu_open = False
            self.renderer.dismiss_overlay()
            self._show_titles_menu()
            return

    def _perform_prestige(self):
        """Perform the prestige/rebirth action."""
        if not self.duck:
            return

        can_prestige, msg = self.prestige.can_prestige(
            self.progression.level,
            self.duck.get_age_days()
        )
        
        if not can_prestige:
            self.renderer.show_message(f"Cannot prestige: {msg}", duration=3.0)
            return
        
        # Perform prestige
        achievements_count = self.achievements.get_unlocked_count()
        success, result_msg, result_data = self.prestige.prestige(
            duck_name=self.duck.name,
            duck_level=self.progression.level,
            duck_age_days=self.duck.get_age_days(),
            achievements_earned=achievements_count,
            memorable_moment=f"Lived {self.duck.get_age_days()} wonderful days!"
        )
        
        if success:
            # Show prestige celebration
            self.renderer.show_message(
                f"{result_msg}\n\n"
                f"New Unlocks: {', '.join(result_data.get('new_unlocks', ['None']))}\n\n"
                f"Your legacy continues with a new duck!\n"
                f"Press any key to start fresh...",
                duration=0
            )
            sound_engine.play_sound("level_up")
            duck_sounds.quack("ecstatic")
            
            # Reset for new game but keep prestige data
            self._reset_for_new_game(keep_prestige=True)
        else:
            self.renderer.show_message(result_msg, duration=3.0)

    def _reset_for_new_game(self, keep_prestige: bool = False):
        """Reset game state for a new game (after prestige or new game)."""
        # Store prestige if keeping
        prestige_data = self.prestige.to_dict() if keep_prestige else None
        
        # Reset all systems
        self.duck = None
        self.behavior_ai = None
        self.inventory = Inventory()
        self.progression = ProgressionSystem()
        self.home = DuckHome()
        from world.habitat import Habitat
        self.habitat = Habitat()

        # Update interaction controller with new habitat reference
        self.interaction_controller.set_references(
            habitat=self.habitat,
            renderer=self.renderer,
            duck=self.duck,
            on_effects_applied=self._on_interaction_effects_applied
        )

        self.materials = MaterialInventory()
        self.building = BuildingSystem()
        self.garden = Garden()
        self.fishing = FishingMinigame()
        self.treasure = TreasureHunter()
        self.challenges = ChallengeSystem()
        self.quests = QuestSystem()
        self.scrapbook = Scrapbook()
        self.tricks = TricksSystem()
        self.titles = TitlesSystem()
        self.decorations = DecorationsSystem()
        
        # Restore prestige if keeping
        if prestige_data:
            self.prestige = PrestigeSystem.from_dict(prestige_data)
            # Apply starting bonuses
            bonuses = self.prestige._calculate_starting_bonuses()
            if bonuses.get("starting_coins", 0) > 0:
                self.habitat.add_currency(int(bonuses["starting_coins"]))
        
        # Go to title screen
        self._state = "title"
        self._start_title_music()

    # ==================== GARDEN SYSTEM ====================

    def _show_garden_menu(self):
        """Show the garden management menu."""
        if not self.duck:
            return
        self._garden_menu_open = True
        self._garden_selected_plot = 0
        self._render_garden_menu()

    def _render_garden_menu(self):
        """Render the garden menu with plot selection."""
        lines = [
            "+=============================================+",
            "|              GARDEN                         |",
            "+=============================================+",
        ]
        
        # Get plots
        plots = list(self.garden.plots.items()) if hasattr(self.garden, 'plots') else []
        num_plots = len(plots) if plots else 4  # Default 4 plots
        
        # Show each plot with selection indicator
        for i in range(num_plots):
            plot_id = i + 1
            plot = self.garden.plots.get(plot_id) if hasattr(self.garden, 'plots') else None
            selected = "[>]" if i == self._garden_selected_plot else "   "
            
            if plot and plot.plant:
                status = f"{plot.plant.name} ({plot.plant.growth_stage})"
                if plot.needs_water:
                    status += " [THIRSTY]"
                if plot.is_ready_to_harvest:
                    status += " [READY!]"
            else:
                status = "Empty plot"
            
            lines.append(f"| {selected} Plot {plot_id}: {status[:30]:30} |")
        
        lines.append("+=============================================+")
        
        # Seed inventory
        lines.append("|  SEEDS:                                     |")
        if self.garden.seed_inventory:
            for seed_id, count in list(self.garden.seed_inventory.items())[:3]:
                seed_name = seed_id.replace("_", " ").title()
                lines.append(f"|    {seed_name[:25]:25} x{count:<5}    |")
        else:
            lines.append("|    No seeds! Explore to find some.         |")
        
        lines.append("+=============================================+")
        lines.append("")
        lines.append("[^/v] Select Plot  [P] Plant  [W] Water  [H] Harvest")
        lines.append("[ESC/Backspace] Close")
        
        self.renderer.show_overlay("\n".join(lines), duration=0)

    def _handle_garden_input(self, key):
        """Handle input for garden menu."""
        key_str = str(key).lower()
        key_name = getattr(key, 'name', None) or ''
        
        # Close with ESC or Backspace
        if key_name == "KEY_ESCAPE" or key_name == "KEY_BACKSPACE":
            self._garden_menu_open = False
            self.renderer.dismiss_message()
            return
        
        # Navigate plots
        num_plots = len(self.garden.plots) if hasattr(self.garden, 'plots') else 4
        
        if key_name == "KEY_UP":
            if self._garden_selected_plot > 0:
                self._garden_selected_plot -= 1
                self._render_garden_menu()
            return
        
        if key_name == "KEY_DOWN":
            if self._garden_selected_plot < num_plots - 1:
                self._garden_selected_plot += 1
                self._render_garden_menu()
            return
        
        # Actions on selected plot
        plot_id = self._garden_selected_plot + 1
        
        if key_str == 'p':
            # Plant - use first available seed
            if self.garden.seed_inventory:
                seed_id = list(self.garden.seed_inventory.keys())[0]
                self._garden_plant(plot_id, seed_id)
                self._render_garden_menu()
            else:
                self.renderer.show_message("No seeds to plant!", duration=2.0)
            return
        
        if key_str == 'w':
            self._garden_water(plot_id)
            self._render_garden_menu()
            return
        
        if key_str == 'h':
            self._garden_harvest(plot_id)
            self._render_garden_menu()
            return

    def _plant_seed(self, seed_id: str):
        """Plant a seed in the first available plot (from menu action)."""
        if not self.duck:
            return

        # Find first empty plot
        empty_plot = None
        for plot_id, plot in self.garden.plots.items():
            if plot.plant is None:
                empty_plot = plot_id
                break

        if empty_plot is None:
            self.renderer.show_message("No empty plots available!", duration=2.0)
            return

        self._garden_plant(empty_plot, seed_id)

    def _garden_plant(self, plot_id: int, seed_id: str):
        """Plant a seed in a garden plot."""
        success, msg = self.garden.plant_seed(plot_id, seed_id)
        self.renderer.show_message(msg, duration=3.0)

        if success:
            self.progression.add_xp(5, "gardening")
            duck_sounds.play()

    def _garden_water(self, plot_id: int):
        """Water a plant in a garden plot."""
        success, msg = self.garden.water_plant(plot_id)
        self.renderer.show_message(msg, duration=2.0)
        
        if success:
            self.challenges.update_progress("garden_water", 1)
            duck_sounds.play()

    def _garden_harvest(self, plot_id: int):
        """Harvest a plant from a garden plot."""
        success, msg, rewards = self.garden.harvest_plant(plot_id)
        
        if success:
            # Add rewards to inventory
            for item_id, amount in rewards.items():
                self.materials.add_material(item_id, amount)
            
            xp = self.progression.add_xp(20, "harvest")
            if xp:
                self._on_level_up(xp)
            
            self.challenges.update_progress("harvest", 1)
            self._process_quest_updates("harvest", "any", 1)
            self.achievements.unlock("first_harvest")
            
            # Check for garden achievements
            stats = self.garden.get_garden_stats()
            if stats["total_harvests"] >= 10:
                self.achievements.unlock("harvest_10")
            if stats["total_harvests"] >= 50:
                self.achievements.unlock("green_thumb")
            
            sound_engine.play_sound("collect")
            duck_sounds.quack("happy")
        
        self.renderer.show_message(msg, duration=3.0)

    def _show_garden_view(self):
        """Show the garden overview."""
        self._show_garden_menu()

    def _water_all_plants(self):
        """Water all plants that need water."""
        if not hasattr(self.garden, 'plots'):
            self.renderer.show_message("No garden plots available!", duration=2.0)
            return
        
        watered = 0
        for plot_id, plot in self.garden.plots.items():
            if plot and plot.plant and plot.needs_water:
                success, _ = self.garden.water_plant(plot_id)
                if success:
                    watered += 1
        
        if watered > 0:
            self.renderer.show_message(f"Watered {watered} plant(s)!", duration=2.0, category="action")
            duck_sounds.play()
        else:
            self.renderer.show_message("No plants need water right now.", duration=2.0)

    def _harvest_all_plants(self):
        """Harvest all ready plants."""
        if not hasattr(self.garden, 'plots'):
            self.renderer.show_message("No garden plots available!", duration=2.0)
            return
        
        harvested = 0
        for plot_id, plot in self.garden.plots.items():
            if plot and plot.plant and plot.is_ready_to_harvest:
                success, msg, rewards = self.garden.harvest_plant(plot_id)
                if success:
                    harvested += 1
                    for item_id, amount in rewards.items():
                        self.materials.add_material(item_id, amount)
        
        if harvested > 0:
            xp = self.progression.add_xp(20 * harvested, "harvest")
            if xp:
                self._on_level_up(xp)
            self.renderer.show_message(f"Harvested {harvested} plant(s)!", duration=2.0, category="action")
            sound_engine.play_sound("collect")
        else:
            self.renderer.show_message("No plants ready to harvest.", duration=2.0)

    # ==================== FESTIVAL SYSTEM ====================

    def _check_festival_events(self):
        """Check for active festival and trigger events."""
        active = self.festivals.check_active_festival()
        
        # Track which festival popup we've shown to avoid repeats
        if not hasattr(self, '_last_shown_festival_id'):
            self._last_shown_festival_id = None
        
        if active:
            # Set weather to match festival theme
            self._apply_festival_weather(active)
            
            # Only show popup if this is a different festival than we last showed
            if self._last_shown_festival_id != active.id:
                self._last_shown_festival_id = active.id
                self.renderer.show_message(
                    f"[#] {active.name} has begun! [#]\n\n"
                    f"{active.description}\n\n"
                    f"Press [0] to view festival activities!",
                    duration=5.0
                )
                sound_engine.play_sound("discovery")
        else:
            # No active festival - reset tracker so next festival shows popup
            self._last_shown_festival_id = None

    def _apply_festival_weather(self, festival):
        """Apply weather that matches the festival theme."""
        from world.atmosphere import WeatherType, Weather
        from datetime import datetime
        
        # Map festival types to appropriate weather
        # Using SUNNY for clear night sky events (stargazing works with clear sunny weather in game)
        festival_weather_map = {
            "spring_bloom": WeatherType.SUNNY,
            "summer_splash": WeatherType.SUNNY,
            "autumn_harvest": WeatherType.WINDY,
            "winter_wonder": WeatherType.SNOWY,
            "duck_day": WeatherType.SUNNY,
            "love_festival": WeatherType.SUNNY,
            "starlight": WeatherType.SUNNY,  # Clear skies for stargazing
            "harvest_moon": WeatherType.SUNNY,  # Clear skies for moon viewing
        }
        
        target_weather = festival_weather_map.get(festival.id)
        if not target_weather:
            return
        
        # Only change weather if current doesn't match festival theme
        if self.atmosphere.current_weather:
            current = self.atmosphere.current_weather.weather_type
            # Allow current weather if it's thematically appropriate
            if current == target_weather:
                return
            # Don't interrupt special weather like rainbow
            if current == WeatherType.RAINBOW:
                return
        
        # 30% chance per check to shift weather to festival theme (gradual shift)
        import random
        if random.random() < 0.3:
            # Get weather data for the target type
            from world.atmosphere import WEATHER_DATA
            data = WEATHER_DATA.get(target_weather, {})
            
            self.atmosphere.current_weather = Weather(
                weather_type=target_weather,
                intensity=random.uniform(0.5, 0.8),
                duration_hours=random.uniform(2, 4),
                start_time=datetime.now().isoformat(),
                mood_modifier=data.get("mood_modifier", 0),
                xp_multiplier=data.get("xp_multiplier", 1.0),
                special_message=f"Festival weather: {data.get('message', '')}",
            )

    # ==================== TRICKS SYSTEM ====================

    def _show_tricks_menu(self):
        """Show the tricks management menu."""
        if not self.duck:
            return

        self._tricks_menu_open = True
        self._render_tricks_menu()
    
    def _render_tricks_menu(self):
        """Render the tricks menu with pagination."""
        items_per_page = 5
        
        # Get learned tricks list
        learned_items = list(self.tricks.learned_tricks.items())
        total_learned = len(learned_items)
        total_pages = max(1, (total_learned + items_per_page - 1) // items_per_page)
        
        if self._tricks_menu_page >= total_pages:
            self._tricks_menu_page = max(0, total_pages - 1)
        
        start_idx = self._tricks_menu_page * items_per_page
        end_idx = start_idx + items_per_page
        page_items = learned_items[start_idx:end_idx]
        
        from duck.tricks import TRICKS
        
        lines = [
            "+===============================================+",
            "|            * DUCK TRICKS *                  |",
            "+===============================================+",
            f"|  Learned: {total_learned:2}  |  Performances: {self.tricks.total_performances:5}       |",
            f"|  Perfect: {self.tricks.total_perfect_performances:3}  |  Highest Combo: {self.tricks.highest_combo:2}          |",
            "+===============================================+",
            f"|  LEARNED TRICKS (Page {self._tricks_menu_page + 1}/{total_pages}):                  |",
        ]
        
        for tid, learned in page_items:
            trick = TRICKS.get(tid)
            if trick:
                stars = "*" * learned.mastery_level + "*" * (5 - learned.mastery_level)
                lines.append(f"|   {trick.name[:20]:20} {stars}         |")
        
        if not learned_items:
            lines.append("|   No tricks learned yet!                      |")
        
        # Training status
        status = self.tricks.get_training_status()
        if status["training"]:
            lines.append("+===============================================+")
            lines.append(f"|  Training: {status['trick_name'][:28]:28}   |")
            lines.append(f"|  Progress: {status['progress']}/{status['required']} ({status['percent']:.0f}%)                      |")
        
        # Available to learn
        available = self.tricks.get_available_tricks()
        if available:
            lines.append("+===============================================+")
            lines.append("|  AVAILABLE TO LEARN:                          |")
            for trick in available[:3]:
                diff_icon = {"easy": "O", "medium": "O", "hard": "O", "master": "O", "legendary": "*"}.get(trick.difficulty.value, "o")
                lines.append(f"|   {diff_icon} {trick.name[:33]:33}   |")
        
        lines.append("+===============================================+")
        lines.append("")
        lines.append("[<-/->] Page  [T] Train  [P] Perform  [C] Combo")
        lines.append("[ESC/Backspace] Close")
        
        tricks_text = "\n".join(lines)
        self.renderer.show_overlay(tricks_text)
    
    def _handle_tricks_input(self, key):
        """Handle input for tricks menu."""
        key_str = str(key).lower()
        key_name = key.name if hasattr(key, 'name') else ''
        
        # Close with ESC or Backspace
        if key_name == "KEY_ESCAPE" or key_name == "KEY_BACKSPACE":
            self._tricks_menu_open = False
            self.renderer.dismiss_overlay()
            return
        
        # Navigate pages
        items_per_page = 5
        learned_items = list(self.tricks.learned_tricks.items())
        total_pages = max(1, (len(learned_items) + items_per_page - 1) // items_per_page)
        
        if key_name == "KEY_LEFT":
            if self._tricks_menu_page > 0:
                self._tricks_menu_page -= 1
                self._render_tricks_menu()
            return
        
        if key_name == "KEY_RIGHT":
            if self._tricks_menu_page < total_pages - 1:
                self._tricks_menu_page += 1
                self._render_tricks_menu()
            return

    def _train_trick(self, trick_id: str):
        """Start or continue training a trick."""
        success, msg = self.tricks.start_training(trick_id)
        self.renderer.show_message(msg, duration=3.0)
        
        if success:
            self.progression.add_xp(10, "training")
            duck_sounds.quack("happy")

    def _perform_trick(self, trick_id: str):
        """Have the duck perform a learned trick."""
        success, msg, result = self.tricks.perform_trick(trick_id)
        
        if success:
            # Show trick animation
            anim_lines = self.tricks.render_trick_performance(trick_id)
            self.renderer.show_message("\n".join(anim_lines), duration=2.0)
            
            # Apply rewards
            xp_gain = result.get("xp_reward", 0)
            coin_gain = result.get("coin_reward", 0)
            mood_bonus = result.get("mood_bonus", 0)
            
            if xp_gain:
                new_level = self.progression.add_xp(xp_gain, "tricks")
                if new_level:
                    self._on_level_up(new_level)
            
            if coin_gain:
                self.habitat.add_currency(coin_gain)
            
            if mood_bonus and self.duck:
                self.duck.needs.fun = min(100, self.duck.needs.fun + mood_bonus)
            
            # Check achievements
            if result.get("perfect"):
                self.achievements.unlock("perfect_trick")
            
            if self.tricks.total_performances >= 10:
                self.achievements.unlock("trick_performer")
            
            if len(self.tricks.learned_tricks) >= 5:
                self.achievements.unlock("trick_master")
            
            sound_engine.play_sound("success")
            duck_sounds.quack("ecstatic")
        else:
            self.renderer.show_message(msg, duration=2.0)

    # ==================== TITLES SYSTEM ====================

    def _show_titles_menu(self):
        """Show the titles management menu."""
        if not self.duck:
            return

        # First check for any new titles based on current stats
        stats = self._get_title_stats()
        new_titles = self.titles.check_title_conditions(stats)
        
        for title_id in new_titles:
            self.titles.earn_title(title_id)
            from duck.titles import TITLES
            title = TITLES.get(title_id)
            if title:
                self.renderer.show_message(
                    f"[=] New Title Earned: {title.name}! [=]\n{title.description}",
                    duration=3.0
                )

        self._titles_menu_open = True
        self._render_titles_menu()
    
    def _render_titles_menu(self):
        """Render the titles menu with pagination."""
        from duck.titles import TITLES
        items_per_page = 5
        
        # Get earned titles list
        earned_items = list(self.titles.earned_titles.items())
        total_earned = len(earned_items)
        total_pages = max(1, (total_earned + items_per_page - 1) // items_per_page)
        
        if self._titles_menu_page >= total_pages:
            self._titles_menu_page = max(0, total_pages - 1)
        
        start_idx = self._titles_menu_page * items_per_page
        end_idx = start_idx + items_per_page
        page_items = earned_items[start_idx:end_idx]
        
        lines = [
            "+===============================================+",
            "|            [=] TITLES & NICKNAMES [=]          |",
            "+===============================================+",
            f"|  Duck: {self.titles.duck_nickname:^35}  |",
            f"|  You: {self.titles.owner_nickname:^36}  |",
        ]
        
        display_name = self.titles.get_display_name()
        lines.append(f"|  Display: {display_name:^31}  |")
        
        current = TITLES.get(self.titles.current_title) if self.titles.current_title else None
        if current:
            lines.append(f"|  Current Title: {current.name:^25}  |")
            if current.xp_bonus > 0:
                lines.append(f"|  XP Bonus: +{current.xp_bonus}%                             |")
        
        lines.append("+===============================================+")
        lines.append(f"|  Titles Earned: {self.titles.total_titles_earned:3}/{len(TITLES):<3}  (Page {self._titles_menu_page + 1}/{total_pages})         |")
        lines.append("+===============================================+")
        lines.append("|  YOUR TITLES:                                 |")
        
        for i, (tid, earned) in enumerate(page_items):
            title = TITLES.get(tid)
            if title:
                equipped = "●" if tid == self.titles.current_title else "○"
                fav = "*" if earned.is_favorite else " "
                rarity_icon = {"common": "o", "uncommon": "O", "rare": "O", "epic": "O", "legendary": "O", "mythic": "O"}.get(title.rarity.value, "o")
                num = i + 1
                lines.append(f"|  [{num}]{equipped}{fav} {rarity_icon} {title.name[:28]:28}   |")
        
        if not earned_items:
            lines.append("|   No titles earned yet!                       |")
        
        lines.append("+===============================================+")
        lines.append("")
        lines.append("[<-/->] Page  [1-5] Equip  [N] Nickname")
        lines.append("[ESC/Backspace] Close")
        
        titles_text = "\n".join(lines)
        self.renderer.show_overlay(titles_text)
    
    def _handle_titles_input(self, key):
        """Handle input for titles menu."""
        key_str = str(key).lower()
        key_name = key.name if hasattr(key, 'name') else ''
        
        # Close with ESC or Backspace
        if key_name == "KEY_ESCAPE" or key_name == "KEY_BACKSPACE":
            self._titles_menu_open = False
            self.renderer.dismiss_overlay()
            return
        
        # Navigate pages
        items_per_page = 5
        earned_items = list(self.titles.earned_titles.items())
        total_pages = max(1, (len(earned_items) + items_per_page - 1) // items_per_page)
        
        if key_name == "KEY_LEFT":
            if self._titles_menu_page > 0:
                self._titles_menu_page -= 1
                self._render_titles_menu()
            return
        
        if key_name == "KEY_RIGHT":
            if self._titles_menu_page < total_pages - 1:
                self._titles_menu_page += 1
                self._render_titles_menu()
            return
        
        # Equip title by number
        if key_str.isdigit() and key_str != '0':
            idx = int(key_str) - 1
            start_idx = self._titles_menu_page * items_per_page
            if 0 <= idx < items_per_page and start_idx + idx < len(earned_items):
                title_id = earned_items[start_idx + idx][0]
                self._equip_title(title_id)
                self._render_titles_menu()
            return

    def _get_title_stats(self) -> Dict:
        """Get current stats for title checking."""
        return {
            "login_streak": self.progression.login_streak if hasattr(self.progression, 'login_streak') else 0,
            "fish_caught": self.fishing.total_fish_caught if hasattr(self.fishing, 'total_fish_caught') else 0,
            "plants_harvested": self.garden.total_harvests if hasattr(self.garden, 'total_harvests') else 0,
            "treasures_found": self.treasure.total_treasures_found if hasattr(self.treasure, 'total_treasures_found') else 0,
            "tricks_learned": len(self.tricks.learned_tricks) if self.tricks else 0,
            "perfect_performances": self.tricks.total_perfect_performances if hasattr(self.tricks, 'total_perfect_performances') else 0,
            "total_coins": self.habitat.currency if self.habitat else 0,
            "unique_items": len(self.inventory.items) if self.inventory else 0,
        }

    def _equip_title(self, title_id: str):
        """Equip a title."""
        success, msg = self.titles.equip_title(title_id)
        self.renderer.show_message(msg, duration=2.0)
        
        if success:
            duck_sounds.quack("happy")

    # ==================== MEMORY RECALL FOR DIALOGUE ====================

    def _get_memory_context_for_dialogue(self) -> str:
        """Get memory context to enhance dialogue responses."""
        if not self.duck or not self.duck.memory:
            return ""
        
        context_parts = []
        
        # Get favorite things
        fav_food = self.duck.memory.get_favorite("food")
        fav_toy = self.duck.memory.get_favorite("toy")
        fav_activity = self.duck.memory.get_favorite("activity")
        
        if fav_food:
            context_parts.append(f"Favorite food: {fav_food}")
        if fav_toy:
            context_parts.append(f"Favorite toy: {fav_toy}")
        if fav_activity:
            context_parts.append(f"Favorite activity: {fav_activity}")
        
        # Get recent memory if available
        if hasattr(self.duck.memory, 'recall_memory'):
            memory = self.duck.memory.recall_memory()
            if memory:
                context_parts.append(f"Recent memory: {memory}")
        
        # Get relationship level
        relationship = self.duck.memory.get_relationship_level()
        if relationship and relationship != "stranger":
            context_parts.append(f"Relationship: {relationship}")
        
        # Get mood trend
        if hasattr(self.duck.memory, 'get_mood_trend'):
            trend = self.duck.memory.get_mood_trend()
            if trend:
                context_parts.append(f"Mood trend: {trend}")
        
        return " | ".join(context_parts)

    # ==================== BADGE AWARDING ====================

    def _unlock_achievement(self, achievement_id: str):
        """Unlock an achievement and award any associated badge."""
        result = self.achievements.unlock(achievement_id)
        if result:  # Only award badge if newly unlocked
            self._award_badge_for_achievement(achievement_id)
        return result

    def _award_badge_for_achievement(self, achievement_id: str):
        """Award a badge when an achievement is unlocked."""
        # Map achievements to badges
        badge_mapping = {
            "first_feed": "caretaker",
            "feed_10": "feeder",
            "feed_100": "master_feeder",
            "first_play": "playful",
            "play_100": "entertainer",
            "first_explore": "explorer",
            "explore_all": "world_traveler",
            "first_craft": "crafter",
            "craft_10": "artisan",
            "first_build": "builder",
            "build_5": "architect",
            "first_fish": "angler",
            "fish_50": "master_angler",
            "first_harvest": "farmer",
            "green_thumb": "botanist",
            "perfect_trick": "performer",
            "trick_master": "star",
            "level_10": "dedicated",
            "level_25": "veteran",
            "level_50": "legendary",
            "prestige_1": "legacy",
        }
        
        badge_id = badge_mapping.get(achievement_id)
        if badge_id and hasattr(self.badges, 'award_badge'):
            self.badges.award_badge(badge_id)
    # ==================== ENHANCED DIARY ====================


    def _show_enhanced_diary(self):
        """Show the enhanced diary menu."""
        if not self.duck:
            return
        self._enhanced_diary_open = True
        self._enhanced_diary_tab = "overview"
        self._enhanced_diary_page = 0
        self._render_enhanced_diary()

    def _render_enhanced_diary(self):
        """Render the enhanced diary with current tab and pagination."""
        if not self.duck:
            return

        width = 48
        items_per_page = 4
        lines = []
        
        # Compact header with tab indicator
        tab_names = {"overview": "Overview", "emotions": "Emotions", "photos": "Photos", "dreams": "Dreams", "life": "Life"}
        current_tab_name = tab_names.get(self._enhanced_diary_tab, "Overview")
        
        lines.append("+" + "=" * (width - 2) + "+")
        lines.append("|" + f" DIARY: {current_tab_name} ".center(width - 2) + "|")
        lines.append("+" + "-" * (width - 2) + "+")
        
        if self._enhanced_diary_tab == "overview":
            self._render_diary_overview(lines, width)
        elif self._enhanced_diary_tab == "emotions":
            self._render_diary_emotions(lines, width, items_per_page)
        elif self._enhanced_diary_tab == "photos":
            self._render_diary_photos(lines, width, items_per_page)
        elif self._enhanced_diary_tab == "dreams":
            self._render_diary_dreams(lines, width, items_per_page)
        elif self._enhanced_diary_tab == "life":
            self._render_diary_life(lines, width, items_per_page)
        
        lines.append("+" + "-" * (width - 2) + "+")
        lines.append("| [<-][->] Navigate Tabs    [ESC] Close   |")
        lines.append("+" + "=" * (width - 2) + "+")
        
        self.renderer.show_overlay("\n".join(lines), duration=0)

    def _render_diary_overview(self, lines: list, width: int):
        """Render overview tab with summary stats (compact)."""
        ed = self.enhanced_diary
        analysis = ed.get_emotion_analysis(7)
        dominant = analysis.get("dominant", "calm")
        
        lines.append("|" + f" Emotions: {len(ed.emotion_logs):3}  Photos: {ed.photos_taken:3}"[:width-2].ljust(width - 2) + "|")
        lines.append("|" + f" Dreams: {ed.dreams_recorded:3}    Chapters: {len(ed.life_chapters):3}"[:width-2].ljust(width - 2) + "|")
        lines.append("|" + f" This Week: {dominant} mood"[:width-2].ljust(width - 2) + "|")
        if ed.current_chapter:
            for ch in ed.life_chapters:
                if ch.chapter_id == ed.current_chapter:
                    lines.append("|" + f" Chapter: {ch.title[:25]}"[:width-2].ljust(width - 2) + "|")
                    break
        else:
            lines.append("|" + " No active chapter"[:width-2].ljust(width - 2) + "|")

    def _render_diary_emotions(self, lines: list, width: int, items_per_page: int):
        """Render emotions tab with pagination (compact)."""
        ed = self.enhanced_diary
        logs = list(reversed(ed.emotion_logs))
        total = len(logs)
        total_pages = max(1, (total + items_per_page - 1) // items_per_page)
        page = min(self._enhanced_diary_page, total_pages - 1)
        self._enhanced_diary_page = page
        
        start = page * items_per_page
        page_items = logs[start:start + items_per_page]
        
        lines.append("|" + f" Page {page+1}/{total_pages} ({total} total)"[:width-2].ljust(width - 2) + "|")
        
        if not page_items:
            lines.append("|" + " No emotions logged yet."[:width-2].ljust(width - 2) + "|")
        else:
            emojis = {"joy": ":)", "sadness": ":(", "excitement": ":D", "calm": "~", 
                      "anxiety": ":S", "love": "<3", "curiosity": "?", "contentment": ":)"}
            for log in page_items:
                dt = log.timestamp[5:10] if log.timestamp else "?"
                e = emojis.get(log.emotion.value, "?")
                t = f"({log.trigger})" if log.trigger else ""
                line = f" {e} {log.emotion.value[:8]:8} {log.intensity}/10 {dt} {t}"
                lines.append("|" + line[:width-2].ljust(width - 2) + "|")

    def _render_diary_photos(self, lines: list, width: int, items_per_page: int):
        """Render photos tab with pagination (compact)."""
        ed = self.enhanced_diary
        photos = list(reversed(ed.photos))
        total = len(photos)
        total_pages = max(1, (total + items_per_page - 1) // items_per_page)
        page = min(self._enhanced_diary_page, total_pages - 1)
        self._enhanced_diary_page = page
        
        start = page * items_per_page
        page_items = photos[start:start + items_per_page]
        
        lines.append("|" + f" Page {page+1}/{total_pages} ({total} photos)"[:width-2].ljust(width - 2) + "|")
        
        if not page_items:
            lines.append("|" + " No photos yet! Press [;] to take one."[:width-2].ljust(width - 2) + "|")
        else:
            for photo in page_items:
                dt = photo.date_taken[5:10] if photo.date_taken else "?"
                loc = (photo.location or "?")[:12]
                cap = photo.caption[:18]
                line = f" {dt} {cap} @{loc}"
                lines.append("|" + line[:width-2].ljust(width - 2) + "|")

    def _render_diary_dreams(self, lines: list, width: int, items_per_page: int):
        """Render dreams tab with pagination (compact)."""
        ed = self.enhanced_diary
        dreams = list(reversed(ed.dream_logs))
        total = len(dreams)
        total_pages = max(1, (total + items_per_page - 1) // items_per_page)
        page = min(self._enhanced_diary_page, total_pages - 1)
        self._enhanced_diary_page = page
        
        start = page * items_per_page
        page_items = dreams[start:start + items_per_page]
        
        lines.append("|" + f" Page {page+1}/{total_pages} ({total} dreams)"[:width-2].ljust(width - 2) + "|")
        
        if not page_items:
            lines.append("|" + " No dreams yet. Sleep to dream!"[:width-2].ljust(width - 2) + "|")
        else:
            for dream in page_items:
                dt = dream.date[5:10] if dream.date else "?"
                r = "*" if dream.recurring else ""
                title = dream.title[:28]
                lines.append("|" + f" {r}{dt} {title}"[:width-2].ljust(width - 2) + "|")

    def _render_diary_life(self, lines: list, width: int, items_per_page: int):
        """Render life story tab with pagination (compact)."""
        ed = self.enhanced_diary
        chapters = list(reversed(ed.life_chapters))
        total = len(chapters)
        total_pages = max(1, (total + items_per_page - 1) // items_per_page)
        page = min(self._enhanced_diary_page, total_pages - 1)
        self._enhanced_diary_page = page
        
        start = page * items_per_page
        page_items = chapters[start:start + items_per_page]
        
        lines.append("|" + f" Page {page+1}/{total_pages} ({total} chapters)"[:width-2].ljust(width - 2) + "|")
        
        if not page_items:
            lines.append("|" + " Your story is just beginning..."[:width-2].ljust(width - 2) + "|")
        else:
            for ch in page_items:
                is_current = ch.chapter_id == ed.current_chapter
                marker = "*" if is_current else "-"
                dt = ch.start_date[5:10] if ch.start_date else "?"
                title = ch.title[:25]
                events_count = len(ch.key_events)
                lines.append("|" + f" {marker}{dt} {title} ({events_count}ev)"[:width-2].ljust(width - 2) + "|")

    def _handle_enhanced_diary_input(self, key):
        """Handle input for the enhanced diary menu."""
        if not key:
            return
            
        key_name = getattr(key, 'name', None) or ""
        
        # Close with ESC or Backspace
        if key_name == "KEY_ESCAPE" or key_name == "KEY_BACKSPACE":
            self._enhanced_diary_open = False
            self.renderer.dismiss_message()
            return
        
        # Tab order for arrow navigation
        tabs = ["overview", "emotions", "photos", "dreams", "life"]
        current_idx = tabs.index(self._enhanced_diary_tab) if self._enhanced_diary_tab in tabs else 0
        
        # Navigate tabs with left/right arrows
        if key_name == "KEY_LEFT":
            if current_idx > 0:
                self._enhanced_diary_tab = tabs[current_idx - 1]
                self._render_enhanced_diary()
            return
        
        if key_name == "KEY_RIGHT":
            if current_idx < len(tabs) - 1:
                self._enhanced_diary_tab = tabs[current_idx + 1]
                self._render_enhanced_diary()
            return

    def _record_random_dream(self):
        """Record a random dream when the duck sleeps."""
        if not self.duck:
            return
        
        import random
        
        # Dream themes based on duck's recent activities and mood
        dream_themes = [
            ("Flying Over the Pond", "Dreamt of soaring high above the pond, seeing everything from the sky. The water sparkled below like diamonds."),
            ("The Giant Bread", "Encountered an enormous piece of bread as big as a house! It was warm and smelled wonderful."),
            ("Making New Friends", "Met lots of friendly ducks and birds. They all played together in a beautiful meadow."),
            ("Underwater Adventure", "Dove deep under the pond and discovered a secret underwater garden full of shiny treasures."),
            ("The Cozy Nest", "Found the most comfortable nest ever made, with soft feathers and warm blankets. Slept so peacefully."),
            ("Dancing in the Rain", "Splashed and twirled in a gentle rain shower while rainbows appeared all around."),
            ("Stargazing", "Looked up at the night sky and saw the stars rearrange into funny shapes and patterns."),
            ("The Tasty Garden", "Wandered through a magical garden where every plant grew delicious treats."),
            ("Playing with Shadows", "Chased shadows that came alive and played hide-and-seek in the moonlight."),
            ("The Singing Pond", "The pond started singing a beautiful melody, and all the animals joined in harmony."),
        ]
        
        # Pick a random dream
        title, description = random.choice(dream_themes)
        
        # Add duck's name for personalization
        description = f"{self.duck.name} {description[0].lower()}{description[1:]}"
        
        # Check if this dream is recurring (small chance)
        recurring = random.random() < 0.1
        
        # Record the dream
        dream = self.enhanced_diary.record_dream(title, description, recurring)
        
        if dream:
            # Show brief dream notification
            self.renderer.show_message(f"z {self.duck.name} had a dream... z", duration=3.0)

    def _take_diary_photo(self):
        """Take a photo for the scrapbook."""
        if not self.duck:
            return
        
        from world.scrapbook import PhotoCategory
        
        # Determine photo context
        mood = self.duck.get_mood().state.value
        weather = self.atmosphere.current_weather.weather_type.value if self.atmosphere.current_weather else "sunny"
        location = self.exploration.current_area.name if self.exploration.current_area else "Home Pond"
        duck_age = self.duck.get_age_days() if self.duck else 1
        
        # Choose art key based on mood
        art_keys = {
            "happy": "duck_happy",
            "content": "duck_happy",
            "excited": "duck_celebration",
            "sleepy": "duck_sleeping",
            "hungry": "duck_eating",
            "playful": "duck_playing",
            "curious": "duck_discovery",
        }
        art_key = art_keys.get(mood, "duck_happy")
        
        # Take the photo in scrapbook
        photo = self.scrapbook.take_photo(
            title=f"Snapshot: {mood.title()}",
            description=f"{self.duck.name} at {location} on a {weather} day",
            category=PhotoCategory.DAILY,
            art_key=art_key,
            mood=mood,
            duck_age=duck_age,
            location=location,
            weather=weather,
            tags=["selfie", mood, location.lower().replace(" ", "_")]
        )
        
        if photo:
            self.renderer.show_message(f"[#] Photo saved to scrapbook!", duration=3.0)
            duck_sounds.play()
            
            # Also log to enhanced diary photos
            from dialogue.diary_enhanced import PhotoType
            photo_type_map = {
                "happy": PhotoType.SELFIE,
                "content": PhotoType.COZY,
                "excited": PhotoType.ADVENTURE,
                "sleepy": PhotoType.COZY,
                "hungry": PhotoType.FOOD,
                "playful": PhotoType.SILLY,
                "curious": PhotoType.ADVENTURE,
            }
            diary_photo_type = photo_type_map.get(mood, PhotoType.SELFIE)
            self.enhanced_diary.take_photo(
                photo_type=diary_photo_type,
                caption=f"Snapshot at {location}",
                location=location,
                mood=mood
            )
        else:
            self.renderer.show_message("Could not take photo", duration=2.0)

    # ==================== COLLECTIBLES ALBUM ====================

    def _show_collectibles_album(self):
        """Show the collectibles album."""
        if not self.duck:
            return

        self._collectibles_menu_open = True
        self._render_collectibles_menu()

    def _view_collectible(self, col_id: str):
        """View a collectible's details (from menu action)."""
        if not self.duck:
            return

        from world.collectibles import COLLECTIBLES
        collectible = COLLECTIBLES.get(col_id)
        if not collectible:
            self.renderer.show_message(f"Unknown collectible: {col_id}", duration=2.0)
            return

        # Check if owned
        is_owned = col_id in self.collectibles.owned_collectibles
        is_shiny = col_id in self.collectibles.shiny_collectibles

        if is_owned:
            shiny_text = " (SHINY!)" if is_shiny else ""
            self.renderer.show_message(
                f"=== {collectible.name}{shiny_text} ===\n\n"
                f"{collectible.description}\n\n"
                f"Rarity: {collectible.rarity.value.title()}\n"
                f"Set: {collectible.set_id.replace('_', ' ').title()}",
                duration=5.0
            )
        else:
            self.renderer.show_message(f"{collectible.name} - Not yet found!", duration=2.0)

    def _render_collectibles_menu(self):
        """Render the collectibles album with pagination."""
        from world.collectibles import SETS
        items_per_page = 6
        
        # Get all sets
        all_sets = list(SETS.items())
        total_sets = len(all_sets)
        total_pages = max(1, (total_sets + items_per_page - 1) // items_per_page)
        
        if self._collectibles_menu_page >= total_pages:
            self._collectibles_menu_page = max(0, total_pages - 1)
        
        start_idx = self._collectibles_menu_page * items_per_page
        end_idx = start_idx + items_per_page
        page_sets = all_sets[start_idx:end_idx]
        
        stats = self.collectibles.get_collection_stats()
        
        lines = [
            "+===============================================+",
            "|           [=] COLLECTION ALBUM [=]              |",
            "+===============================================+",
            f"|  Collected: {stats['unique_owned']:3}/{stats['total_possible']:<3} ({stats['completion_percent']:.1f}%)               |",
            f"|  Shiny: {stats['shiny_count']:3}  |  Sets: {stats['sets_completed']}/{stats['total_sets']}                |",
            "+===============================================+",
            f"|  SETS (Page {self._collectibles_menu_page + 1}/{total_pages}):                           |",
        ]
        
        for i, (set_id, set_def) in enumerate(page_sets):
            owned, total, _ = self.collectibles.get_set_progress(set_id)
            completed = "x" if set_id in self.collectibles.completed_sets else " "
            progress = f"{owned}/{total}"
            lines.append(f"|  [{completed}] {set_def.name[:25]:25} {progress:5}   |")
        
        lines.extend([
            "+===============================================+",
            "|  RARITY:                                      |",
        ])
        
        from world.collectibles import CollectibleRarity
        for rarity in CollectibleRarity:
            count = stats['by_rarity'].get(rarity.value, 0)
            icon = {"common": "o", "uncommon": "O", "rare": "O", "epic": "O", "legendary": "O", "mythic": "O"}.get(rarity.value, "o")
            lines.append(f"|    {icon} {rarity.value.title():12}: {count:3}                    |")
        
        lines.append("+===============================================+")
        lines.append("")
        lines.append(f"Collection Progress: {stats['unique_owned']}/{stats['total_possible']} ({stats['completion_percent']:.1f}%)")
        lines.append(f"Packs Available: {stats.get('packs_available', 0)}")
        lines.append("")
        lines.append("[<-/->] Page  [O] Open Pack  [1-9] View Set")
        lines.append("[ESC/Backspace] Close")
        
        album_text = "\n".join(lines)
        self.renderer.show_overlay(album_text)
    
    def _handle_collectibles_input(self, key):
        """Handle input for collectibles menu."""
        key_str = str(key).lower()
        key_name = key.name if hasattr(key, 'name') else ''
        
        # Close with ESC or Backspace
        if key_name == "KEY_ESCAPE" or key_name == "KEY_BACKSPACE":
            self._collectibles_menu_open = False
            self.renderer.dismiss_overlay()
            return
        
        # Navigate pages
        from world.collectibles import SETS
        items_per_page = 6
        total_sets = len(SETS)
        total_pages = max(1, (total_sets + items_per_page - 1) // items_per_page)
        
        if key_name == "KEY_LEFT":
            if self._collectibles_menu_page > 0:
                self._collectibles_menu_page -= 1
                self._render_collectibles_menu()
            return
        
        if key_name == "KEY_RIGHT":
            if self._collectibles_menu_page < total_pages - 1:
                self._collectibles_menu_page += 1
                self._render_collectibles_menu()
            return
        
        # Open pack
        if key_str == 'o':
            self._open_collectible_pack()
            self._render_collectibles_menu()
            return

    def _open_collectible_pack(self, pack_type: str = "standard"):
        """Open a collectible pack."""
        if not self.duck:
            return
        
        success, msg, items = self.collectibles.open_pack(pack_type)
        
        if success and items:
            # Build reveal display
            lines = [
                "+===============================================+",
                "|          [+] PACK OPENED! [+]                   |",
                "+===============================================+",
            ]
            
            for item in items:
                rarity_icon = {"common": "o", "uncommon": "O", "rare": "O", "epic": "O", "legendary": "O"}.get(item.rarity.value if hasattr(item.rarity, 'value') else str(item.rarity), "o")
                new_marker = "*NEW" if not self.collectibles.is_duplicate(item.id) else ""
                lines.append(f"|  {rarity_icon} {item.name[:30]:30} {new_marker:5} |")
            
            lines.append("+===============================================+")
            
            self.renderer.show_message("\n".join(lines), duration=5.0)
            sound_engine.play_sound("collect")
            duck_sounds.quack("happy")
        else:
            self.renderer.show_message(msg, duration=2.0)

    # ==================== DECORATIONS SYSTEM ====================

    def _show_decorations_menu(self):
        """Show the decorations menu for placing/managing room decor."""
        if not self.duck:
            return

        self._decorations_menu_open = True
        self._render_decorations_menu()
    
    def _render_decorations_menu(self):
        """Render the decorations menu with pagination."""
        from world.decorations import DECORATIONS
        items_per_page = 5
        
        # Get owned decorations
        owned = [(did, count) for did, count in self.decorations.owned_decorations.items() if count > 0]
        total_owned = len(owned)
        total_pages = max(1, (total_owned + items_per_page - 1) // items_per_page)
        
        if self._decorations_menu_page >= total_pages:
            self._decorations_menu_page = max(0, total_pages - 1)
        
        start_idx = self._decorations_menu_page * items_per_page
        end_idx = start_idx + items_per_page
        page_items = owned[start_idx:end_idx]
        
        lines = [
            "+===============================================+",
            "|          [=] DECORATIONS [=]                    |",
            "+===============================================+",
            "|  ROOMS:                                       |",
        ]
        
        # List available rooms
        for i, (room_id, room) in enumerate(self.decorations.rooms.items(), 1):
            decor_count = len(room.decorations) if hasattr(room, 'decorations') else 0
            lines.append(f"|   [{i}] {room.name[:25]:25} ({decor_count} items) |")
        
        lines.append("+===============================================+")
        
        # Show owned decorations with pagination
        if owned:
            lines.append(f"|  AVAILABLE TO PLACE (Page {self._decorations_menu_page + 1}/{total_pages}):            |")
            for i, (did, count) in enumerate(page_items):
                decor = DECORATIONS.get(did)
                if decor:
                    lines.append(f"|   {decor.name[:30]:30} x{count:2}    |")
        else:
            lines.append("|  No decorations to place. Buy some at shop!  |")
        
        lines.append("+===============================================+")
        
        # Stats
        lines.append(f"|  Total Beauty: {self.decorations.total_beauty:4}                         |")
        lines.append(f"|  Total Comfort: {self.decorations.total_comfort:4}                        |")
        
        lines.append("+===============================================+")
        lines.append("")
        lines.append("[<-/->] Page  [1-5] View Room  [P] Place  [R] Remove")
        lines.append("[ESC/Backspace] Close")
        
        self.renderer.show_overlay("\n".join(lines), duration=0)
    
    def _handle_decorations_input(self, key):
        """Handle input for decorations menu."""
        key_str = str(key).lower()
        key_name = key.name if hasattr(key, 'name') else ''
        
        # Close with ESC or Backspace
        if key_name == "KEY_ESCAPE" or key_name == "KEY_BACKSPACE":
            self._decorations_menu_open = False
            self.renderer.dismiss_message()
            return
        
        # Navigate pages
        items_per_page = 5
        owned = [(did, count) for did, count in self.decorations.owned_decorations.items() if count > 0]
        total_pages = max(1, (len(owned) + items_per_page - 1) // items_per_page)
        
        if key_name == "KEY_LEFT":
            if self._decorations_menu_page > 0:
                self._decorations_menu_page -= 1
                self._render_decorations_menu()
            return
        
        if key_name == "KEY_RIGHT":
            if self._decorations_menu_page < total_pages - 1:
                self._decorations_menu_page += 1
                self._render_decorations_menu()
            return

    def _place_decoration(self, decor_id: str):
        """Buy or place a decoration (from menu action)."""
        if not self.duck:
            return

        from world.decorations import DECORATIONS
        decoration = DECORATIONS.get(decor_id)
        if not decoration:
            self.renderer.show_message(f"Unknown decoration: {decor_id}", duration=2.0)
            return

        # Check if owned
        owned_count = self.decorations.owned_decorations.get(decor_id, 0)

        if owned_count == 0:
            # Try to buy
            success, msg, new_coins = self.decorations.buy_decoration(decor_id, self.habitat.currency)
            if success:
                self.habitat._currency = new_coins
                self.renderer.show_message(f"Bought {decoration.name}!", duration=2.0)
                duck_sounds.play()
            else:
                self.renderer.show_message(msg, duration=2.0)
        else:
            # Open decorations menu to place it
            self._show_decorations_menu()

    def _place_decoration_in_room(self, decoration_id: str, room_type: str, position: Tuple[int, int] = (0, 0)):
        """Place a decoration in a room."""
        success, msg = self.decorations.place_decoration(decoration_id, room_type, position)

        if success:
            self.renderer.show_message(f"* {msg}", duration=3.0)
            sound_engine.play_sound("build")
        else:
            self.renderer.show_message(msg, duration=2.0)

        return success

    # ==================== SAVE SLOTS SYSTEM ====================

    def _show_save_slots_menu(self):
        """Show the save slots management menu."""
        self._save_slots_menu_open = True
        self._save_slots_selected = 0
        self._render_save_slots_menu()

    def _render_save_slots_menu(self):
        """Render the save slots menu with selection."""
        # Refresh slot info
        self.save_slots.refresh_slots()
        
        lines = []
        lines.append("+===============================================+")
        lines.append("|              SAVE SLOTS                       |")
        lines.append("+===============================================+")
        lines.append("")
        
        for i, slot_id in enumerate(range(1, SaveSlotsSystem.MAX_SLOTS + 1)):
            slot = self.save_slots.slots.get(slot_id)
            selected = "[>]" if i == self._save_slots_selected else "   "
            
            if slot and not slot.is_empty:
                status = f"Lv.{slot.level} | {slot.playtime_minutes}min | {slot.coins} coins"
                if slot.prestige_level > 0:
                    status += f" | P{slot.prestige_level}"
                lines.append(f"  {selected} [{slot_id}] {slot.duck_name:<12} {status}")
            else:
                lines.append(f"  {selected} [{slot_id}] -- Empty Slot --")
        
        lines.append("")
        lines.append(f"  Current: Slot {self.save_slots.current_slot}")
        lines.append("")
        lines.append("[^/v] Select  [Enter] Switch  [N] New  [D] Delete")
        lines.append("[ESC/Backspace] Close")
        
        self.renderer.show_overlay("\n".join(lines), duration=0)

    def _handle_save_slots_input(self, key):
        """Handle input for save slots menu."""
        key_str = str(key).lower()
        key_name = getattr(key, 'name', None) or ''
        
        # Close with ESC or Backspace
        if key_name == "KEY_ESCAPE" or key_name == "KEY_BACKSPACE":
            self._save_slots_menu_open = False
            self.renderer.dismiss_message()
            return
        
        # Navigate slots
        max_slots = SaveSlotsSystem.MAX_SLOTS
        
        if key_name == "KEY_UP":
            if self._save_slots_selected > 0:
                self._save_slots_selected -= 1
                self._render_save_slots_menu()
            return
        
        if key_name == "KEY_DOWN":
            if self._save_slots_selected < max_slots - 1:
                self._save_slots_selected += 1
                self._render_save_slots_menu()
            return
        
        # Switch slot with Enter or number
        slot_id = self._save_slots_selected + 1
        
        if key_name == "KEY_ENTER":
            slot = self.save_slots.slots.get(slot_id)
            if slot and not slot.is_empty:
                self.save_slots.switch_slot(slot_id)
                self._save_slots_menu_open = False
                self.renderer.dismiss_message()
                self._load_game()
            else:
                self.renderer.show_message("Slot is empty! Use [N] to create new game.", duration=2.0)
            return
        
        if key_str.isdigit() and 1 <= int(key_str) <= max_slots:
            self._save_slots_selected = int(key_str) - 1
            self._render_save_slots_menu()
            return
        
        # New game in selected slot
        if key_str == 'n':
            self._save_slots_menu_open = False
            self.renderer.dismiss_message()
            self.save_slots.switch_slot(slot_id)
            self._start_new_game()
            return
        
        # Delete slot
        if key_str == 'd':
            slot = self.save_slots.slots.get(slot_id)
            if slot and not slot.is_empty:
                self.save_slots.delete_slot(slot_id)
                self._render_save_slots_menu()
                self.renderer.show_message(f"Deleted slot {slot_id}", duration=2.0)
            return

    def _get_room_decoration_bonus(self) -> Dict[str, int]:
        """Get the total decoration bonuses affecting the duck."""
        bonuses = {
            "mood": 0,
            "comfort": 0,
            "beauty": 0
        }
        
        # Get bonuses from all rooms
        for room in self.decorations.rooms.values():
            bonuses["mood"] += getattr(room, 'mood_modifier', 0)
            bonuses["comfort"] += getattr(room, 'comfort_level', 0)
        
        bonuses["beauty"] = self.decorations.total_beauty
        
        return bonuses
