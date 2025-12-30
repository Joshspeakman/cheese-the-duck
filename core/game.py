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
from world.quests import QuestSystem, quest_system
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

from ui.statistics import StatisticsSystem, statistics_system
from ui.day_night import DayNightSystem, day_night_system
from ui.event_animations import (
    EventAnimator, create_event_animator, ANIMATED_EVENTS,
    EventAnimationState, BreezeAnimator
)
from ui.badges import BadgesSystem, badges_system
from ui.mood_visuals import MoodVisualEffects, mood_visual_effects
from ui.reactions import DuckReactionController, init_reaction_controller
from ui.menu_selector import HierarchicalMenuSelector
from ui.menu_structure import build_main_menu_categories, MENU_ACTIONS

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
        self._sound_enabled = True
        self._show_goals = False
        self._reset_confirmation = False  # Flag for reset game confirmation

        # Arrow-key menu selectors
        self._crafting_menu = MenuSelector("CRAFTING", close_keys=['KEY_ESCAPE', 'c'])
        self._building_menu = MenuSelector("BUILDING", close_keys=['KEY_ESCAPE', 'r'])
        self._areas_menu = MenuSelector("AREAS", close_keys=['KEY_ESCAPE', 'a'])
        self._use_menu = MenuSelector("USE ITEM", close_keys=['KEY_ESCAPE', 'u'])
        self._minigames_menu = MenuSelector("MINI-GAMES", close_keys=['KEY_ESCAPE', 'j'])
        self._quests_menu = MenuSelector("QUESTS", close_keys=['KEY_ESCAPE', 'o'])
        self._weather_menu = MenuSelector("WEATHER ACTIVITIES", close_keys=['KEY_ESCAPE', 'w'])

        # Main hierarchical menu (TAB to open)
        self._main_menu = HierarchicalMenuSelector("Main Menu")
        self._main_menu.set_categories(build_main_menu_categories())
        self._main_menu_open = False

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
        
        # Hidden debug menu (accessed with backtick `)
        self._debug_menu_open = False
        self._debug_menu_selected = 0
        self._debug_submenu = None  # Current debug submenu (weather, events, etc.)
        self._debug_submenu_selected = 0

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

        # Check for existing save
        if self.save_manager.save_exists():
            self._load_game()
        else:
            self._state = "title"
            self._start_title_music()

        self._game_loop()

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

                # Cap frame rate
                elapsed = time.time() - loop_start
                if elapsed < frame_time:
                    time.sleep(frame_time - elapsed)

    def _process_input(self):
        """Process keyboard input."""
        key = self.terminal.inkey(timeout=0.05)

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
        if self._main_menu_open:
            self._handle_main_menu_input(key)
            return
        if self._debug_menu_open:
            self._handle_debug_input(key)
            return

        # Handle inventory item selection
        if self.renderer.is_inventory_open() and self.duck:
            key_str = str(key)
            if key_str.isdigit() and key_str != '0':
                self._use_inventory_item(int(key_str) - 1)  # Convert to 0-based index
                return

        action = self.input_handler.process_key(key)
        self._handle_action(action, key)

    def _handle_talk_input(self, key):
        """Handle input while in talk mode."""
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
                self.renderer.show_message("*stares expectantly* ...Well? I'm listening.", duration=3.0)
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

        # Close shop with ESC or B
        if key.name == "KEY_ESCAPE" or key_str == 'b':
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
                self.renderer.show_message(result["message"], duration=3.0)
            return
        # Close with ESC or C
        if key.name == "KEY_ESCAPE" or key_str == 'c':
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
                result = self.building.start_building(bp.id, self.materials)
                self._building_menu_open = False
                if result.get("success"):
                    self._start_building_animation(bp)
                else:
                    self.renderer.show_message(result["message"], duration=3.0)
            return
        if key.name == "KEY_ESCAPE" or key_str == 'r':
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
        if key.name == "KEY_ESCAPE" or key_str == 'a':
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
        if key.name == "KEY_ESCAPE" or key_str == 'u':
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
        if key.name == "KEY_ESCAPE" or key_str == 'j':
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
        if key.name == "KEY_ESCAPE" or key_str == 'o':
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
        self.renderer.show_message("\n".join(lines), duration=0)

    def _execute_menu_action(self, action_id: str):
        """Execute a menu action by its ID."""
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
        if method_name == "_quit_game":
            self._quit()
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
        sound_engine.toggle_sound()
        status = "ON" if sound_engine.sound_enabled else "OFF"
        self.renderer.show_message(f"Sound Effects: {status}")

    def _toggle_music_action(self):
        """Toggle music."""
        from audio.sound import sound_engine
        sound_engine.toggle_music()
        status = "ON" if sound_engine.music_enabled else "OFF"
        self.renderer.show_message(f"Music: {status}")

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
            self.renderer.show_message(result["message"], duration=4.0)

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
        self.renderer.show_message(response, duration=8.0)

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

    def _execute_item_interaction(self, item_id: str):
        """Execute an interaction with a placed item (with animated movement)."""
        if not self.duck:
            return
        
        # Check if we're already in an interaction
        if self._interaction_phase != InteractionPhase.IDLE:
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
        }
        
        # Execute the interaction to get the result
        result = execute_interaction(item_id, duck_state)
        
        if not result or not result.success:
            self.renderer.show_message("*confused quack* I don't know how to do that...")
            return
        
        # Get item's playfield position
        item_pos = self._get_item_playfield_position(item_id)
        
        if item_pos:
            # Animated interaction: waddle to item first
            self._interaction_phase = InteractionPhase.MOVING_TO_TARGET
            self._interaction_target_item = item_id
            self._interaction_target_pos = item_pos
            self._interaction_pending_result = result
            
            # Show anticipation message
            item = get_shop_item(item_id)
            item_name = item.name if item else item_id
            self.renderer.show_message(f"*waddles excitedly toward {item_name}*", duration=2.0)
            
            # Move duck to item with callback
            self.renderer.duck_pos.move_to(
                item_pos[0], item_pos[1],
                callback=self._on_arrived_at_item,
                callback_data={"item_id": item_id, "result": result}
            )
        else:
            # No position found, play animation immediately (fallback)
            self._complete_item_interaction(item_id, result)

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
        }
        
        result = execute_interaction(item_id, duck_state)
        
        if not result or not result.success:
            self.renderer.show_message("*confused quack* I don't know how to do that...")
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
        self.renderer.show_message(result.message, duration=result.duration + 1.0)
    
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
                    self.renderer.dismiss_message()
                return

            # Main menu (TAB key)
            if key_str == '\t' or key_name == 'KEY_TAB':
                self._close_all_overlays()
                self._main_menu.open()
                self._main_menu_open = True
                self._update_main_menu_display()
                return

            # UI keys and interaction keys
            if key_str in ['s', 't', 'i', 'g', 'm', 'b', 'n', 'x', '+', '=', '-', '_', 'e', 'a', 'c', 'r', 'u', 'j', 'k', 'f', 'p', 'l', 'd', 'z', 'h', 'o', 'v', 'w', 'y', 'q', '1', '2', '3', '4', '5', '6', '7']:
                self._handle_playing_action(action, key)
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
        if self._state == "title":
            if action == GameAction.CONFIRM or (key and key.name == "KEY_ENTER"):
                self._start_new_game()
            return

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

            # Goals toggle [G]
            if key_str == 'g':
                self._show_goals = not self._show_goals
                if self._show_goals:
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

            # Sound toggle [M]
            if key_str == 'm':
                self._sound_enabled = sound_engine.toggle()
                status = "ON" if self._sound_enabled else "OFF"
                self.renderer.show_message(f"Sound: {status}")
                return

            # Music mute toggle [N]
            if key_str == 'n':
                muted = sound_engine.toggle_music_mute()
                status = "OFF" if muted else "ON"
                self.renderer.show_message(f"Music: {status}")
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
        """Show the goals overlay."""
        active_goals = self.goals.get_active_goals()
        completed = self.goals.get_completed_count()
        total = self.goals.get_total_count()

        # Build goals text
        lines = [
            f"Goals Completed: {completed}/{total}",
            "-" * 30,
        ]

        for goal in active_goals[:5]:  # Show up to 5 active goals
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
            "Press [G] to close",
        ])

        self.renderer.show_message("\n".join(lines[:2]), duration=5.0)

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

        # Clear any autonomous action
        if self.behavior_ai:
            self.behavior_ai.clear_action()

        # Set duck visual state with appropriate duration
        state_durations = {
            "feed": 4.0,    # Eating animation for 4 seconds
            "play": 3.0,    # Playing animation for 3 seconds
            "sleep": 15.0,  # Sleeping animation for 15 seconds
            "clean": 3.5,   # Cleaning animation for 3.5 seconds
            "pet": 2.5,     # Petting animation for 2.5 seconds
        }
        duration = state_durations.get(interaction, 3.0)
        
        if interaction == "feed":
            self.renderer.set_duck_state("eating", duration)
        elif interaction == "play":
            self.renderer.set_duck_state("playing", duration)
        elif interaction == "sleep":
            self.renderer.set_duck_state("sleeping", duration)
            # Start a dream sequence
            self._start_dream()
        elif interaction == "clean":
            self.renderer.set_duck_state("cleaning", duration)
        elif interaction == "pet":
            self.renderer.set_duck_state("petting", duration)
        else:
            self.renderer.set_duck_state("idle", 1.0)

        # Notify reaction controller that user action is in progress
        # This prevents weather reactions from overriding user-initiated animations
        self.reaction_controller.notify_user_action(duration, time.time())

        # Perform the interaction
        result = self.duck.interact(interaction)

        # Record in memory
        mood = self.duck.get_mood()
        emotional_value = 10 if mood.score > 50 else 5
        self.duck.memory.add_interaction(interaction, "", emotional_value)
        self.duck.memory.total_interactions += 1
        self.duck.memory.record_mood(mood.score)

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
        quest_updates = self.quests.update_progress("interact", interaction, 1)
        for quest_id, objective, completed in quest_updates:
            if completed:
                self.renderer.show_message(f"[=] Quest objective complete!", duration=2.0)

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
            self.renderer.show_message(f"Received: {name} x{reward.amount}!", duration=2.0)

        elif reward.reward_type == RewardType.XP:
            xp = int(reward.value)
            new_level = self.progression.add_xp(xp, "reward")
            self.renderer.show_message(f"+{xp} XP!", duration=2.0)
            if new_level:
                self._on_level_up(new_level)

        elif reward.reward_type == RewardType.COLLECTIBLE:
            if self.progression.add_collectible(reward.value):
                self._show_collectible_found(reward.value)

        elif reward.reward_type == RewardType.TITLE:
            if reward.value not in self.progression.unlocked_titles:
                self.progression.unlocked_titles.append(reward.value)
                self.renderer.show_message(f"Unlocked title: {reward.value}!", duration=3.0)

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
                self.renderer.show_message(fish_msg, duration=2.0)

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
                self._show_message_if_no_menu(build_result.get("message", "Stage complete!"), duration=2.0)
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
                self._show_message_if_no_menu(f"# Your duck has grown to {new_stage.value}!", duration=5.0)

            # Check secret goals for session/mood-based achievements
            self._check_secret_achievements()

            self._last_tick = current_time

        # Update atmosphere (weather, visitors) every 30 seconds
        if current_time - self._last_atmosphere_check >= 30:
            messages = self.atmosphere.update()
            for msg in messages:
                self._show_message_if_no_menu(msg, duration=4.0)

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
                            visitor_animator.set_visitor(
                                personality, 
                                friend.name,
                                friendship_level,
                                friend.times_visited,
                                unlocked_topics,
                                conversation_topics=conversation_topics,
                                shared_experiences=shared_experiences,
                                last_conversation_summary=last_summary,
                            )
                            greeting = visitor_animator.get_greeting(self.duck.name)
                            if greeting:
                                self._show_message_if_no_menu(greeting, duration=6.0)
                            duck_sounds.quack("happy")
                            # Trigger friend arrival reaction animation
                            self.reaction_controller.trigger_friend_reaction("arrival", current_time)
                            # Play happy music for the visit
                            sound_engine.play_event_music(MusicContext.HAPPY, duration=10.0)
                            
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
                self._show_message_if_no_menu(ambient, duration=3.0)

            self._last_event_check = current_time

        # Random contextual duck comments (every ~45 seconds when idle)
        if current_time - self._last_random_comment_time >= self._random_comment_interval:
            if not self._duck_traveling and not self._duck_exploring and not self._duck_building:
                # 25% chance to make a contextual comment
                if random.random() < 0.25:
                    self._make_contextual_comment()
            self._last_random_comment_time = current_time

        # Check for pending visitor reaction comment
        if self._pending_visitor_comment and current_time >= self._pending_visitor_comment_time:
            self._show_message_if_no_menu(self._pending_visitor_comment, duration=4.0)
            duck_sounds.quack("content")
            self._pending_visitor_comment = None

        # Check for pending weather reaction comment
        if self._pending_weather_comment and current_time >= self._pending_weather_comment_time:
            self._show_message_if_no_menu(self._pending_weather_comment, duration=4.0)
            duck_sounds.quack("content")
            self._pending_weather_comment = None

        # Autonomous behavior (skip if duck is busy traveling/exploring/building)
        if self.behavior_ai and not self._duck_traveling and not self._duck_exploring and not self._duck_building:
            # Update behavior AI context with available structures and weather
            available_structures = set()
            for structure in self.building.structures:
                if structure.status.value == "complete":
                    available_structures.add(structure.blueprint_id)
            
            # Check for bad weather
            is_bad_weather = False
            weather_type = None
            if self.atmosphere.current_weather:
                weather_type = self.atmosphere.current_weather.weather_type.value
                is_bad_weather = weather_type in ["rainy", "stormy", "snowy"]
            
            self.behavior_ai.set_context(
                available_structures=available_structures,
                is_bad_weather=is_bad_weather,
                weather_type=weather_type
            )
            
            result = self.behavior_ai.perform_action(self.duck, current_time)
            if result:
                self.duck.set_action_message(result.message)

                # Update visual state based on action
                if result.action.value in ["nap", "sleep", "nap_in_nest"]:
                    self.renderer.set_duck_state("sleeping")
                elif result.action.value in ["waddle", "look_around", "chase_bug"]:
                    self.renderer.set_duck_state("walking")
                elif result.action.value in ["splash", "wiggle", "flap_wings", "use_bird_bath"]:
                    self.renderer.set_duck_state("playing")
                elif result.action.value in ["hide_in_shelter"]:
                    self.renderer.set_duck_state("hiding")

                # Show closeup for emotive actions
                emotive_actions = ["stare_blankly", "trip", "quack", "wiggle", "flap_wings", 
                                   "nap_in_nest", "hide_in_shelter", "use_bird_bath"]
                if result.action.value in emotive_actions:
                    self.renderer.show_closeup(result.action.value, 1.5)
                
                # Play quack sound when duck talks to itself or does vocal actions
                vocal_actions = ["quack", "look_around", "chase_bug", "trip", "wiggle", "splash"]
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
        
        # Get duck's position for visitor to follow/approach
        duck_x = self.renderer.duck_pos.x
        duck_y = self.renderer.duck_pos.y
        
        # Update visitor animation and movement
        frame_changed, _ = visitor_animator.update(current_time, duck_x, duck_y)
        
        # Check for random dialogue
        dialogue = visitor_animator.get_random_dialogue(self.duck.name, current_time)
        if dialogue:
            self.renderer.show_message(dialogue, duration=5.0)
        
        # Comment on items/structures the visitor sees (only once per item)
        if visitor_animator.is_near_duck():
            # Comment on placed items
            for item in self.habitat.placed_items:
                item_id = item.item_id if hasattr(item, 'item_id') else str(item)
                item_name = item.name if hasattr(item, 'name') else item_id
                comment = visitor_animator.get_item_comment(item_id, item_name)
                if comment:
                    self.renderer.show_message(comment, duration=4.0)
                    break  # Only one comment at a time
            
            # Comment on cosmetics
            for slot, cosmetic_id in self.habitat.equipped_cosmetics.items():
                if cosmetic_id:
                    comment = visitor_animator.get_cosmetic_comment(self.duck.name, cosmetic_id)
                    if comment:
                        self.renderer.show_message(comment, duration=4.0)
                        break
            
            # Comment on built structures
            for structure in self.building.structures:
                if structure.status.value == "complete":
                    comment = visitor_animator.get_item_comment(structure.blueprint_id, structure.blueprint_id)
                    if comment:
                        self.renderer.show_message(comment, duration=4.0)
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
                self.renderer.show_message(farewell, duration=5.0)
                duck_sounds.quack("happy")
                # Trigger friend departure reaction animation
                self.reaction_controller.trigger_friend_reaction("departure", time.time())
            
            # Check if off screen (position > 20)
            pos_x, _ = visitor_animator.get_position()
            if pos_x >= 24:
                # End the visit
                self.friends.end_visit()
                self.renderer.show_message(f"*{friend.name} waddles away happily*", duration=3.0)

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
            self.quests.update_progress("craft", item_id, 1)

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
            self.quests.update_progress("build", bp_id, 1)

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
        """Check if duck should interact with nearby placed items."""
        import random
        
        if not self.duck or not hasattr(self, 'habitat') or random.random() > 0.03:
            return
        
        # Get duck position in habitat coordinates
        # Playfield is 44x14, habitat grid is 20x12
        duck_x = int(self.renderer.duck_pos.x * 20 / 44)
        duck_y = int(self.renderer.duck_pos.y * 12 / 14)
        
        # Find nearby items
        nearby = self.habitat.get_nearby_items(duck_x, duck_y, radius=3)
        if not nearby:
            return
        
        # Pick a random nearby item to interact with
        item = random.choice(nearby)
        
        # Check cooldown (don't interact with same item too often)
        if current_time - item.last_interaction < 30:  # 30 second cooldown
            return
        
        # Get item info
        from world.shop import get_item, ItemCategory
        shop_item = get_item(item.item_id)
        if not shop_item:
            return

        # Mark interaction
        self.habitat.mark_interaction(item, current_time)

        # Special handling for boombox - toggle music!
        if item.item_id == "toy_boombox":
            self._toggle_boombox_music()
            return

        # Animate the item based on category
        item_animations = {
            ItemCategory.TOY: "bounce",  # Toys bounce when played with
            ItemCategory.WATER: "shake",  # Water ripples
            ItemCategory.FURNITURE: "shake",  # Furniture wobbles
            ItemCategory.PLANT: "shake",  # Plants sway
            ItemCategory.DECORATION: "bounce",  # Decorations bounce
            ItemCategory.SPECIAL: "bounce",  # Special items bounce
        }
        anim_type = item_animations.get(shop_item.category, "bounce")
        self.habitat.animate_item(item, anim_type)

        # Generate interaction message based on item category
        category_actions = {
            ItemCategory.TOY: [
                f"*plays with {shop_item.name}*",
                f"*bounces around the {shop_item.name}!*",
                f"*has fun with the {shop_item.name}*",
            ],
            ItemCategory.FURNITURE: [
                f"*sits on the {shop_item.name}*",
                f"*inspects the {shop_item.name}*",
                f"*rests near the {shop_item.name}*",
            ],
            ItemCategory.WATER: [
                f"*splashes in the {shop_item.name}!*",
                f"*swims in the {shop_item.name}*",
                f"*enjoys the {shop_item.name}*",
            ],
            ItemCategory.PLANT: [
                f"*sniffs the {shop_item.name}*",
                f"*admires the {shop_item.name}*",
                f"*hides behind the {shop_item.name}*",
            ],
            ItemCategory.DECORATION: [
                f"*stares at the {shop_item.name}*",
                f"*appreciates the {shop_item.name}*",
                f"*quacks at the {shop_item.name}*",
            ],
            ItemCategory.STRUCTURE: [
                f"*explores near the {shop_item.name}*",
                f"*investigates the {shop_item.name}*",
                f"*waddles around the {shop_item.name}*",
            ],
        }
        
        messages = category_actions.get(shop_item.category, [f"*looks at {shop_item.name}*"])
        message = random.choice(messages)
        
        self.duck.set_action_message(message)
        self.renderer.show_message(message, duration=2.5)
        
        # Play animation/effect based on item category
        category_effects = {
            ItemCategory.TOY: "sparkle",
            ItemCategory.WATER: "sparkle", 
            ItemCategory.FURNITURE: "happy",
            ItemCategory.PLANT: "happy",
            ItemCategory.DECORATION: "sparkle",
            ItemCategory.SPECIAL: "hearts",
        }
        effect = category_effects.get(shop_item.category, "happy")
        self.renderer.show_effect(effect, duration=1.5)
        
        # Trigger duck animation based on category
        category_animations = {
            ItemCategory.TOY: "bounce",
            ItemCategory.WATER: "splash",
            ItemCategory.FURNITURE: "wiggle",
            ItemCategory.PLANT: "wiggle",
            ItemCategory.DECORATION: "spin",
            ItemCategory.SPECIAL: "spin",
        }
        anim_name = category_animations.get(shop_item.category, "wiggle")
        self.renderer.duck_pos.set_state(anim_name)
        
        # Give small mood boost based on item category
        mood_boosts = {
            ItemCategory.TOY: ("fun", 3),
            ItemCategory.WATER: ("fun", 4),
            ItemCategory.FURNITURE: ("energy", 2),
            ItemCategory.PLANT: ("fun", 1),
            ItemCategory.DECORATION: ("fun", 1),
        }
        
        if shop_item.category in mood_boosts:
            need, amount = mood_boosts[shop_item.category]
            current = getattr(self.duck.needs, need, 0)
            setattr(self.duck.needs, need, min(100, current + amount))
        
        # Small XP reward for item interaction
        new_level = self.progression.add_xp(1, "item_interaction")
        if new_level:
            self._on_level_up(new_level)

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
            self.renderer.show_message(special_event.message, duration=5.0)
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
                self.renderer.show_message(event.message, duration=5.0)
            else:
                # Show event message immediately for non-animated events
                self.renderer.show_message(event.message, duration=4.0)

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
        """Make a random contextual comment based on current game state."""
        if not self.duck:
            return
        
        # Don't interrupt open menus or overlays
        if self._is_any_menu_open():
            return
        
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
            self.renderer.show_message(comment, duration=4.0)
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
        self.renderer.show_message("*splish splash splosh!*", duration=2.5)
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
        self.renderer.show_message(f"*happy quack* Hi {friend_name}!", duration=2.5)
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
                            # ~0.2% per frame (at 60fps, ~12% chance per second)
                            if random.random() < 0.002:
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
            self.renderer._render_title_screen()
        elif self._state == "offline_summary" and self._pending_offline_summary:
            summary = self._pending_offline_summary
            self.renderer.render_offline_summary(
                summary["name"],
                summary["hours"],
                summary["changes"],
            )
        elif self._state == "playing":
            self.renderer.render_frame(self)

    def _start_new_game(self):
        """Start a new game with a new duck."""
        # Stop title music (both methods to ensure it stops)
        sound_engine.stop_music()
        sound_engine.stop_background_music()
        
        self.duck = Duck.create_new()
        self.behavior_ai = BehaviorAI()
        self.inventory = Inventory()
        self.goals = GoalSystem()
        self.achievements = AchievementSystem()
        self.progression = ProgressionSystem()
        self.home = DuckHome()

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

        # Welcome message
        greeting = self.conversation.get_greeting(self.duck)
        self.renderer.show_message(f"Welcome, {self.duck.name}!")
        self.renderer.show_message(greeting, duration=4.0)

        # Play welcome sound
        duck_sounds.quack("happy")

        # Start main game background music using dynamic system
        music_context = get_music_context(weather="sunny", duck_mood="content")
        sound_engine.update_music(music_context, force=True)

        # First goal
        self.goals.add_daily_goals()

        # Generate daily challenges
        self.progression.generate_daily_challenges()

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
            # ============== END NEW FEATURE SYSTEMS ==============
        }

        self.save_manager.save(save_data)

    def _return_to_title(self):
        """Save the game and return to title screen."""
        if self.duck:
            self._save_game()
            self.renderer.show_message("Saving game...")
            time.sleep(0.5)
        
        # Reset game state
        self.duck = None
        self.behavior_ai = None
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
            self._main_menu_open or
            self._debug_menu_open or
            self.renderer.is_shop_open() or
            self.renderer.is_talking() or
            self.renderer._show_stats or
            self.renderer._show_inventory or
            self.renderer._show_help
        )

    def _show_message_if_no_menu(self, message: str, duration: float = 5.0):
        """Show a message only if no menu is currently open. Used for non-critical duck messages."""
        if not self._is_any_menu_open():
            self.renderer.show_message(message, duration)

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
        self._main_menu_open = False
        self._show_goals = False
        self._debug_menu_open = False
        self._debug_submenu = None

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
        self._main_menu_open = False
        self._show_goals = False
        self._debug_menu_open = False
        self._debug_submenu = None

    def _quit(self):
        """Quit the game."""
        if self.duck:
            self._save_game()
            self.renderer.show_message("Saving and quitting...")
            time.sleep(0.5)

        # Stop any playing music
        sound_engine.stop_music()
        sound_engine.stop_background_music()

        self._running = False

    def _start_reset_confirmation(self):
        """Start the reset game confirmation dialog."""
        self._reset_confirmation = True
        self.renderer.show_message(
            "RESET GAME?\n\n"
            "This will DELETE all progress!\n"
            "Your duck, items, and achievements\n"
            "will be PERMANENTLY lost!\n\n"
            "[Y] Yes, reset everything\n"
            "[N] No, cancel",
            duration=0  # Don't auto-dismiss
        )

    def _confirm_reset(self):
        """Confirm and execute game reset."""
        self._reset_confirmation = False

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
            self.renderer.show_message(
                f"* RARE DISCOVERY! *\n\n"
                f"You found: {item_id.replace('_', ' ').title()}!\n"
                f"Resources: {', '.join(resources_found) if resources_found else 'None'}",
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

        # Normal exploration result
        biome_name = result.get("biome", "area").replace("_", " ").title()
        if resources_found:
            msg = f"~ Explored {biome_name} ~\n\nFound: {', '.join(resources_found)}"
            if result.get("skill_up"):
                msg += f"\n\n* Gathering skill improved!"
                # Check for gathering master achievement
                if self.exploration.gathering_skill >= 5:
                    self._unlock_achievement("gathering_master")
        else:
            msg = f"~ Explored {biome_name} ~\n\nNothing found this time."

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

        # Build menu items
        items = []
        for recipe in all_recipes[:8]:
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

        # Build menu items
        items = []
        for bp in all_blueprints[:6]:
            can_build = bp.id in buildable
            mat_desc = ', '.join(f'{v} {k}' for k, v in bp.required_materials.items())
            items.append({
                'id': bp.id,
                'label': f"{'x' if can_build else ' '} {bp.name}",
                'description': f"Needs: {mat_desc}",
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
                result = self.building.start_building(bp.id, self.materials)
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
        self.quests.update_progress("explore", "any", 1)

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
            self.renderer.show_message("*click* Boombox off.", duration=2.0)
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
                    self.quests.update_progress("catch", caught_fish.fish_id, 1)

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
        for memory in self.duck.memory.short_term[-5:]:
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
            self.renderer.show_message(f"Birthday bonus: +{bonus_coins} coins!", duration=3.0)

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

        self.renderer.show_message("\n".join(lines), duration=0)

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

        # Get trader selection display
        lines = self.trading.render_trader_selection()
        
        trading_text = "\n".join(lines)
        trading_text += "\n\n[1-5] Visit trader  [ESC/V] Close"
        
        self.renderer.show_message(trading_text, duration=0)

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
        self._weather_menu.clear_items()
        for activity in activities:
            desc = f"{activity.description[:35]}... ({activity.duration_seconds}s)"
            self._weather_menu.add_item(activity.name, desc, enabled=True, data=activity)
        
        if not activities:
            self._weather_menu.add_item("No activities available", "Check back when weather changes!", enabled=False)
        
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
        
        # Close with ESC, W, or B
        if key.name == "KEY_ESCAPE" or key_str in ('w', 'b'):
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

    # ==================== DEBUG MENU (HIDDEN) ====================
    
    def _handle_debug_input(self, key):
        """Handle input in the hidden debug menu."""
        key_str = str(key).lower()
        key_name = key.name if hasattr(key, 'name') else ''
        
        # Close with ESC or backtick
        if key_name == "KEY_ESCAPE" or key_str in ('`', '~'):
            if self._debug_submenu:
                self._debug_submenu = None
                self._debug_submenu_selected = 0
                self._show_debug_menu()
            else:
                self._debug_menu_open = False
                self.renderer.dismiss_message()
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
                max_items = len(self._get_debug_submenu_items())
                self._debug_submenu_selected = min(max_items - 1, self._debug_submenu_selected + 1)
            else:
                self._debug_menu_selected = min(9, self._debug_menu_selected + 1)
            self._show_debug_menu()
            return
        
        # Select with Enter or number keys
        if key_name == "KEY_ENTER":
            self._debug_select_current()
            return
        
        # Number key shortcuts
        if key_str.isdigit():
            idx = int(key_str) - 1 if key_str != '0' else 9
            if self._debug_submenu:
                items = self._get_debug_submenu_items()
                if 0 <= idx < len(items):
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
        return []
    
    def _debug_select_current(self):
        """Execute the currently selected debug option."""
        if not self._debug_submenu:
            # Main menu selection
            menus = ["weather", "events", "visitor", "needs", "money", "friendship", "time", "misc", "age", "building"]
            if 0 <= self._debug_menu_selected < len(menus):
                self._debug_submenu = menus[self._debug_menu_selected]
                self._debug_submenu_selected = 0
                self._show_debug_menu()
            return
        
        # Submenu selection
        items = self._get_debug_submenu_items()
        if not (0 <= self._debug_submenu_selected < len(items)):
            return
        
        selected = items[self._debug_submenu_selected]
        
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
            set()
        )
        
        greeting = visitor_animator.get_greeting(self.duck.name if self.duck else "Duck")
        self.renderer.show_message(f"# DEBUG: Spawned {personality} visitor\n{greeting}", duration=4)
        
        self._debug_menu_open = False
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
        self._debug_submenu = None
    
    def _debug_set_time(self, action: str):
        """Manipulate time for testing."""
        from datetime import datetime, timedelta
        
        if action == "advance_1h":
            # Advance all time-based systems by 1 hour
            self.renderer.show_message("# DEBUG: Advanced time by 1 hour (effects limited)", duration=2)
        elif action == "advance_6h":
            self.renderer.show_message("# DEBUG: Advanced time by 6 hours (effects limited)", duration=2)
        elif action == "advance_1d":
            self.renderer.show_message("# DEBUG: Advanced time by 1 day (effects limited)", duration=2)
        elif action == "set_dawn":
            self.renderer.show_message("# DEBUG: Time display simulating dawn (5 AM)", duration=2)
        elif action == "set_noon":
            self.renderer.show_message("# DEBUG: Time display simulating noon", duration=2)
        elif action == "set_dusk":
            self.renderer.show_message("# DEBUG: Time display simulating dusk (7 PM)", duration=2)
        elif action == "set_night":
            self.renderer.show_message("# DEBUG: Time display simulating night (11 PM)", duration=2)
        
        self._debug_menu_open = False
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
        self._debug_submenu = None

    def _debug_set_age(self, action: str):
        """Set duck age or growth stage."""
        from duck.aging import GrowthStage
        from datetime import datetime, timedelta

        if not self.duck:
            self.renderer.show_message("DEBUG: No duck!", duration=2)
            self._debug_menu_open = False
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

            if days > 0 and hasattr(self.duck, 'age_tracker') and self.duck.age_tracker:
                # Advance the birth date backwards to simulate aging
                if self.duck.age_tracker.birth_date:
                    birth = datetime.fromisoformat(self.duck.age_tracker.birth_date + "T00:00:00")
                    new_birth = birth - timedelta(days=days)
                    self.duck.age_tracker.birth_date = new_birth.strftime("%Y-%m-%d")
                    self.duck.age_tracker.update_growth(self.duck.age_tracker.get_age_days())
                    self.renderer.show_message(f"DEBUG: Aged duck by {days} day(s)", duration=2)
                else:
                    self.renderer.show_message("DEBUG: No birth date set", duration=2)
            else:
                self.renderer.show_message("DEBUG: No age tracker", duration=2)
        else:
            # Set specific growth stage
            try:
                stage = GrowthStage(action)
                if hasattr(self.duck, 'age_tracker') and self.duck.age_tracker:
                    self.duck.age_tracker.current_stage = stage
                    self.renderer.show_message(f"DEBUG: Set stage to {action}", duration=2)
                # Also update old growth_stage if it exists
                if hasattr(self.duck, 'growth_stage'):
                    self.duck.growth_stage = action
            except ValueError:
                self.renderer.show_message(f"DEBUG: Unknown stage {action}", duration=2)

        self._debug_menu_open = False
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
        self._debug_submenu = None

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
            ]
            for i, (key, name, desc) in enumerate(options):
                prefix = ">" if i == self._debug_menu_selected else " "
                lines.append(f"| {prefix} [{key}] {name:<12} {desc:<16} |")
        else:
            # Submenu
            lines.append(f"|  << {self._debug_submenu.upper():<29} |")
            lines.append("+===================================+")
            items = self._get_debug_submenu_items()
            for i, item in enumerate(items):
                prefix = ">" if i == self._debug_submenu_selected else " "
                key = str(i + 1) if i < 9 else " "
                display = item[:28] if len(item) > 28 else item
                lines.append(f"| {prefix} [{key}] {display:<28} |")
        
        lines.extend([
            "+===================================+",
            "|  [^v] Navigate  [Enter] Select    |",
            "|  [ESC/`] Back/Close               |",
            "+===================================+",
        ])
        
        self.renderer.show_message("\n".join(lines), duration=0)

    # ==================== SCRAPBOOK SYSTEM ====================

    def _show_scrapbook(self):
        """Show the scrapbook/photo album."""
        if not self.duck:
            return

        # Get scrapbook page display
        lines = self.scrapbook.render_album_page()
        
        scrapbook_text = "\n".join(lines)
        scrapbook_text += "\n\n[</>/F] Navigate/Favorite  [ESC/Y] Close"
        
        self.renderer.show_message(scrapbook_text, duration=0)

    # ==================== TREASURE HUNTING ====================

    def _show_treasure_hunt(self):
        """Show the treasure hunting menu."""
        if not self.duck:
            return

        # Get treasure collection display
        stats = self.treasure.get_collection_stats()
        
        lines = [
            "=== TREASURE HUNTING ===",
            "",
            f"Collection: {stats['found_types']}/{stats['total_types']} ({stats['completion']}%)",
            f"Total Treasures Found: {stats['total_found']}",
            f"Total Value: {stats['total_value']} coins",
            f"Maps Available: {stats['maps_available']}",
            "",
            "Available Locations:",
        ]
        
        for i, loc in enumerate(self.treasure.unlocked_locations, 1):
            lines.append(f"  [{i}] {loc.value.title()}")
        
        lines.extend([
            "",
            "Digs Remaining Today: " + str(max(0, self.treasure.max_digs_per_day - self.treasure.dig_attempts_today)),
            "",
            "[1-9] Hunt location  [C] Collection",
            "[ESC/6] Close"
        ])
        
        treasure_text = "\n".join(lines)
        self.renderer.show_message(treasure_text, duration=0)

    # ==================== SECRETS BOOK ====================

    def _show_secrets_book(self):
        """Show the secrets and easter eggs book."""
        if not self.duck:
            return

        # Get secrets display
        lines = self.secrets.render_secrets_book()
        
        secrets_text = "\n".join(lines)
        secrets_text += "\n\n[</>/] Navigate  [ESC/7] Close"
        
        self.renderer.show_message(secrets_text, duration=0)

    # ==================== PRESTIGE/LEGACY SYSTEM ====================

    def _show_prestige_menu(self):
        """Show the prestige/legacy system menu."""
        if not self.duck:
            return

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
        lines.append("[P] Prestige  [T] Change Title  [ESC/8] Close")
        
        prestige_text = "\n".join(lines)
        self.renderer.show_message(prestige_text, duration=0)

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

        # Get garden display
        lines = self.garden.render_garden()
        
        # Add seed inventory
        lines.append("")
        lines.append("+=======================================+")
        lines.append("|  SEED INVENTORY:                      |")
        
        if self.garden.seed_inventory:
            for seed_id, count in list(self.garden.seed_inventory.items())[:5]:
                seed_name = seed_id.replace("_", " ").title()
                lines.append(f"|   {seed_name[:20]:20} x{count:<5}     |")
        else:
            lines.append("|   No seeds! Explore to find some.    |")
        
        lines.append("+=======================================+")
        lines.append("")
        lines.append("[P] Plant  [W] Water  [H] Harvest  [ESC/9] Close")
        
        garden_text = "\n".join(lines)
        self.renderer.show_message(garden_text, duration=0)

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
            self.quests.update_progress("harvest", "any", 1)
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

    # ==================== FESTIVAL SYSTEM ====================

    def _show_festival_menu(self):
        """Show the festival menu."""
        if not self.duck:
            return

        # Get festival display
        lines = self.festivals.render_festival_screen()
        
        # Add upcoming festivals if none active
        active = self.festivals.check_active_festival()
        if not active:
            upcoming = self.festivals.get_upcoming_festivals()
            if upcoming:
                lines.append("")
                lines.append("  UPCOMING FESTIVALS:")
                for name, days in upcoming[:3]:
                    lines.append(f"    • {name}: {days} days away")
        
        lines.append("")
        if active:
            lines.append("[J] Join/Participate  [A] Activities  [R] Rewards")
        lines.append("[ESC/0] Close")
        
        festival_text = "\n".join(lines)
        self.renderer.show_message(festival_text, duration=0)

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

        # Get tricks display
        lines = self.tricks.render_trick_list()
        
        lines.append("")
        lines.append("[T] Train a trick  [P] Perform  [C] Combo")
        lines.append("[ESC/X] Close")
        
        tricks_text = "\n".join(lines)
        self.renderer.show_message(tricks_text, duration=0)

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

        # Get titles display
        lines = self.titles.render_titles_screen()
        
        lines.append("")
        lines.append("[1-5] Equip title  [N] Set nickname  [ESC/`] Close")
        
        titles_text = "\n".join(lines)
        self.renderer.show_message(titles_text, duration=0)

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
        """Show the enhanced diary with emotions, photos, and dreams."""
        if not self.duck:
            return

        # Build combined diary view
        lines = [
            "+===============================================+",
            "|            [=] DUCK'S DIARY [=]                  |",
            "+===============================================+",
        ]
        
        # Emotion wheel section
        emotion_lines = self.enhanced_diary.render_emotion_wheel(width=40)
        for line in emotion_lines[:6]:
            lines.append(f"| {line:^43} |")
        
        lines.append("+===============================================+")
        lines.append("|  RECENT PHOTOS:                               |")
        
        # Photo album section (mini preview)
        photo_lines = self.enhanced_diary.render_photo_album_page(page=0, photos_per_page=1)
        for line in photo_lines[:4]:
            lines.append(f"|   {line[:40]:40}   |")
        
        lines.append("+===============================================+")
        lines.append("|  DREAM JOURNAL:                               |")
        
        # Dream journal section
        dream_lines = self.enhanced_diary.render_dream_journal(width=40)
        for line in dream_lines[:4]:
            lines.append(f"|   {line[:40]:40}   |")
        
        lines.append("+===============================================+")
        lines.append("")
        lines.append("[E] Emotions  [P] Photos  [D] Dreams  [L] Life Story")
        lines.append("[ESC] Close")
        
        diary_text = "\n".join(lines)
        self.renderer.show_message(diary_text, duration=0)

    def _take_diary_photo(self):
        """Take a photo for the diary."""
        if not self.duck:
            return
        
        from dialogue.diary_enhanced import PhotoType
        
        # Determine photo type based on current activity
        mood = self.duck.get_mood().state.value
        weather = self.atmosphere.current_weather.weather_type.value if self.atmosphere.current_weather else "sunny"
        location = self.exploration.current_area.name if self.exploration.current_area else "Home Pond"
        
        # Create caption
        caption = f"{self.duck.name} at {location} ({weather})"
        
        # Take the photo
        success, msg, photo = self.enhanced_diary.take_photo(
            photo_type=PhotoType.MOOD,
            caption=caption,
            duck_mood=mood,
            weather=weather,
            location=location
        )
        
        if success:
            self.renderer.show_message(f"[#] {msg}", duration=3.0)
            duck_sounds.play()
        else:
            self.renderer.show_message(msg, duration=2.0)

    # ==================== COLLECTIBLES ALBUM ====================

    def _show_collectibles_album(self):
        """Show the collectibles album."""
        if not self.duck:
            return

        # Get collection display
        lines = self.collectibles.render_collection_album()
        
        # Add stats
        stats = self.collectibles.get_collection_stats()
        lines.append("")
        lines.append(f"Collection Progress: {stats['total_owned']}/{stats['total_possible']} ({stats['completion_percent']:.1f}%)")
        lines.append(f"Packs Available: {stats.get('packs_available', 0)}")
        lines.append("")
        lines.append("[O] Open Pack  [1-9] View Set  [ESC] Close")
        
        album_text = "\n".join(lines)
        self.renderer.show_message(album_text, duration=0)

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
        
        # Show owned decorations
        owned = [(did, count) for did, count in self.decorations.owned_decorations.items() if count > 0]
        if owned:
            lines.append("|  AVAILABLE TO PLACE:                          |")
            for did, count in owned[:5]:
                from world.decorations import DECORATIONS
                decor = DECORATIONS.get(did)
                if decor:
                    lines.append(f"|   {decor.name[:30]:30} x{count:2}    |")
            if len(owned) > 5:
                lines.append(f"|   ... and {len(owned) - 5} more                         |")
        else:
            lines.append("|  No decorations to place. Buy some at shop!  |")
        
        lines.append("+===============================================+")
        
        # Stats
        lines.append(f"|  Total Beauty: {self.decorations.total_beauty:4}                         |")
        lines.append(f"|  Total Comfort: {self.decorations.total_comfort:4}                        |")
        
        lines.append("+===============================================+")
        lines.append("")
        lines.append("[1-5] View Room  [P] Place  [R] Remove  [ESC] Close")
        
        self.renderer.show_message("\n".join(lines), duration=0)

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
        # Refresh slot info
        self.save_slots.refresh_slots()
        
        lines = []
        lines.append("+===============================================+")
        lines.append("|              SAVE SLOTS                       |")
        lines.append("+===============================================+")
        lines.append("")
        
        for slot_id in range(1, SaveSlotsSystem.MAX_SLOTS + 1):
            slot = self.save_slots.slots.get(slot_id)
            if slot and not slot.is_empty:
                status = f"Lv.{slot.level} | {slot.playtime_minutes}min | {slot.coins} coins"
                if slot.prestige_level > 0:
                    status += f" | P{slot.prestige_level}"
                lines.append(f"  [{slot_id}] {slot.duck_name:<15} {status}")
            else:
                lines.append(f"  [{slot_id}] -- Empty Slot --")
        
        lines.append("")
        lines.append(f"  Current: Slot {self.save_slots.current_slot}")
        lines.append("")
        lines.append("  [1-5] Switch Slot  [N] New Game in Slot")
        lines.append("  [D] Delete Slot    [ESC] Close")
        
        self.renderer.show_message("\n".join(lines), duration=0)

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
