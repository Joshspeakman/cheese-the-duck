"""
Main game controller - manages game loop and state.
Enhanced with progression, daily rewards, collectibles, and addiction mechanics.
"""
import time
import random
from typing import Optional, List, Tuple
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
from audio.sound import sound_engine, duck_sounds
from ui.renderer import Renderer
from ui.animations import animation_controller
from ui.input_handler import InputHandler, GameAction
from ui.menu_selector import MenuSelector, MenuItem

# New feature imports - Phase 2 systems
from world.scrapbook import Scrapbook, scrapbook
from world.fishing import FishingMinigame, fishing_system
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

from audio.ambient import AmbientSoundSystem, ambient_sound_system
from audio.sound_effects import SoundEffectSystem, sound_effects

from ui.statistics import StatisticsSystem, statistics_system
from ui.day_night import DayNightSystem, day_night_system
from ui.badges import BadgesSystem, badges_system
from ui.mood_visuals import MoodVisualEffects, mood_visual_effects


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

        # Backwards compatibility flags (computed from menu state)
        self._crafting_menu_open = False  # Flag for crafting menu
        self._building_menu_open = False  # Flag for building menu
        self._areas_menu_open = False     # Flag for areas menu
        self._use_menu_open = False       # Flag for use/interact menu
        self._use_menu_items = []         # List of items with interactions
        self._use_menu_selected = 0       # Currently selected item in use menu
        self._minigames_menu_open = False # Flag for minigames menu
        self._minigames_menu_selected = 0 # Currently selected minigame

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
        
        # Save Management
        self.save_slots: SaveSlotsSystem = save_slots_system
        # ============== END NEW FEATURE SYSTEMS ==============
        
        # Item interaction animation state
        self._item_interaction_active = False
        self._item_interaction_item = None
        self._item_interaction_frames = []
        self._item_interaction_frame_idx = 0
        self._item_interaction_start = 0.0
        self._item_interaction_duration = 0.0
        self._item_interaction_message = ""
        self._item_interaction_frame_time = 0.5
        
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
        else:
            # Fallback to synthesized music if WAV not available
            sound_engine.play_melody('happy', loop=True)

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
            if message.strip():
                self._process_talk(message)
            self.renderer.toggle_talk()
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
            self.renderer.show_message(f"Purchased {item.name}! ✓")
            # Award XP for shopping
            self.progression.add_xp(5)
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
                self.achievements.unlock("used_legendary")
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

        # Get response from conversation system
        response = self.conversation.process_player_input(self.duck, message)

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

    def _execute_item_interaction(self, item_id: str):
        """Execute an interaction with a placed item."""
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
        
        # Execute the interaction
        result = execute_interaction(item_id, duck_state)
        
        if not result or not result.success:
            self.renderer.show_message("*confused quack* I don't know how to do that...")
            return
        
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
            self.achievements.unlock("playful_duck")
        if self._statistics["item_interactions"] >= 50:
            self.achievements.unlock("item_master")
    
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
            key_str = str(key).lower()
            key_name = getattr(key, 'name', '') or ''

            # Handle ESC to close any overlay
            if key_name == 'KEY_ESCAPE':
                self._close_all_overlays()
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
            self.renderer.toggle_help()
            return

        if action == GameAction.CANCEL:
            self.renderer.hide_overlays()
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
            return

        if self._state == "playing" and self.duck:
            self._handle_playing_action(action, key)

    def _handle_playing_action(self, action: GameAction, key=None):
        """Handle actions while playing."""
        # Handle menu inputs first (if any menu is open)
        if key:
            key_str = str(key).lower()
            key_name = getattr(key, 'name', '') or ''

            # Check for open menus and handle their input
            if self._crafting_menu_open:
                if self._handle_crafting_input(key_str, key_name):
                    return

            if self._building_menu_open:
                if self._handle_building_input(key_str, key_name):
                    return

            if self._areas_menu_open:
                if self._handle_areas_input(key_str, key_name):
                    return

            if self._use_menu_open:
                if self._handle_use_input(key_str, key_name):
                    return

            if self._minigames_menu_open:
                if self._handle_minigames_menu_input(key_str, key_name):
                    return

            # Check if a minigame is active
            if self._active_minigame:
                if self._handle_minigame_input(key_str, key_name):
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
                self.renderer.toggle_stats()
                return

            # Talk toggle [T]
            if key_str == 't':
                self.renderer.toggle_talk()
                return

            # Inventory toggle [I]
            if key_str == 'i':
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

            # Reset game [X] - buried in menu, requires confirmation
            if key_str == 'x':
                self._start_reset_confirmation()
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

            # Trading Post [V] (Visiting merchants)
            if key_str == 'v':
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

            # Secrets Book [7]
            if key_str == '7':
                self._show_secrets_book()
                return

            # Help toggle [H]
            if key_str == 'h':
                self.renderer.toggle_help()
                return

            # Check if any menu/overlay is open that uses number keys
            # If so, don't process number keys as interaction shortcuts
            has_number_key_menu = (
                self._crafting_menu_open or
                self._building_menu_open or
                self._areas_menu_open or
                self._use_menu_open or
                self._minigames_menu_open or
                self.renderer._show_message_overlay or
                self.renderer._show_inventory
            )

            # Duck interaction keys - close any overlays first and perform action
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
            "sleep": 5.0,   # Sleeping animation for 5 seconds
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
            self.achievements.unlock(f"10_{interaction}s")
        elif count == 50:
            self.achievements.unlock(f"50_{interaction}s")
        elif count == 100:
            self.achievements.unlock(f"100_{interaction}s")

        # Check mood-based achievements
        mood = self.duck.get_mood()
        if mood.state.value == "ecstatic":
            self.achievements.unlock("first_ecstatic")

        # Check relationship achievements
        if self.duck.memory.get_relationship_level() == "bonded":
            self.achievements.unlock("best_friends")

    def _on_level_up(self, new_level: int):
        """Handle level up notification."""
        duck_sounds.level_up()
        self.renderer.show_effect("sparkle", 2.0)
        self.renderer.show_celebration(
            "level_up",
            f"Level {new_level}! {self.progression.title}",
            duration=4.0
        )

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
                self.renderer.show_message(build_result.get("message", "Stage complete!"), duration=2.0)
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

            # Check secret goals for session/mood-based achievements
            self._check_secret_achievements()

            self._last_tick = current_time

        # Update atmosphere (weather, visitors) every 30 seconds
        if current_time - self._last_atmosphere_check >= 30:
            messages = self.atmosphere.update()
            for msg in messages:
                self.renderer.show_message(msg, duration=4.0)

            # Track weather for secret goal
            if self.atmosphere.current_weather:
                self._weather_seen.add(self.atmosphere.current_weather.weather_type.value)

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

            self._last_atmosphere_check = current_time

        # Check for random events (every 10 seconds)
        if current_time - self._last_event_check >= 10:
            self._check_events()

            # Chance for ambient event (peaceful atmosphere)
            ambient = self.progression.get_ambient_event(chance=0.02)
            if ambient:
                self.renderer.show_message(ambient, duration=3.0)

            self._last_event_check = current_time

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
                f"✨ Crafting Complete! ✨\n\n"
                f"Created: {item_id.replace('_', ' ').title()} x{quantity}",
                duration=4.0
            )
            sound_engine.play_sound("craft_complete")
            self.progression.add_xp(15, "crafting")

            # Crafting achievements
            self.achievements.unlock("first_craft")
            
            # Check for tool crafting
            from world.crafting import RECIPES, CraftingCategory
            recipe = RECIPES.get(item_id)
            if recipe and recipe.category == CraftingCategory.TOOL:
                self.achievements.unlock("craft_tool")
            
            # Check for crafting milestones
            total_crafted = sum(self.crafting.crafted_count.values())
            if total_crafted >= 10:
                self.achievements.unlock("craft_10")
            
            # Check for crafting master
            if self.crafting.crafting_skill >= 5:
                self.achievements.unlock("crafting_master")

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
                f"🏠 Building Complete! 🏠\n\n"
                f"Built: {name}\n"
                f"Check [R] menu to see your structures!",
                duration=5.0
            )
            sound_engine.play_sound("build_complete")
            self.progression.add_xp(50, "building")

            # Building achievements
            self.achievements.unlock("first_build")
            
            # Check structure type
            from world.building import StructureType
            if bp:
                if bp.structure_type == StructureType.NEST:
                    self.achievements.unlock("build_nest")
                elif bp.structure_type == StructureType.HOUSE:
                    self.achievements.unlock("build_house")
            
            # Check building milestones
            if self.building.structures_built >= 5:
                self.achievements.unlock("build_5")
            
            # Check for building master
            if self.building.building_skill >= 5:
                self.achievements.unlock("building_master")

        elif result.get("stage_completed"):
            stage = result.get("current_stage", 0)
            stage_names = ["Foundation", "Frame", "Walls", "Roof", "Finishing"]
            name = stage_names[min(stage, 4)]
            self.renderer.show_message(f"🔨 {name} complete! Continue building...", duration=2.0)

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
                    f"⚠️ {name} damaged by weather! ({health}%)\n"
                    f"Repair with [R] menu.",
                    duration=3.0
                )
            elif structure.status.value == "destroyed":
                self.renderer.show_message(
                    f"💔 {name} destroyed by weather!",
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
        self.progression.add_xp(1, "item_interaction")

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

            # Show event
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
        self.achievements.unlock(f"reach_{new_stage}")

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
        self._show_goals = False

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
                f"✨ RARE DISCOVERY! ✨\n\n"
                f"You found: {item_id.replace('_', ' ').title()}!\n"
                f"Resources: {', '.join(resources_found) if resources_found else 'None'}",
                duration=5.0
            )
            # Achievement for rare finds
            self.achievements.unlock("rare_find")
            return

        # Handle danger encounters
        if result.get("danger"):
            danger = result["danger"]
            self.renderer.show_message(
                f"⚠️ DANGER! ⚠️\n\n"
                f"{danger['message']}\n"
                f"You escaped but dropped some items!",
                duration=4.0
            )
            return

        # Normal exploration result
        biome_name = result.get("biome", "area").replace("_", " ").title()
        if resources_found:
            msg = f"🌿 Explored {biome_name} 🌿\n\nFound: {', '.join(resources_found)}"
            if result.get("skill_up"):
                msg += f"\n\n⭐ Gathering skill improved!"
                # Check for gathering master achievement
                if self.exploration.gathering_skill >= 5:
                    self.achievements.unlock("gathering_master")
        else:
            msg = f"🌿 Explored {biome_name} 🌿\n\nNothing found this time."

        self.renderer.show_message(msg, duration=3.0)

        # Award some XP for exploring
        self.progression.add_xp(5, "exploration")

        # First exploration achievement
        self.achievements.unlock("first_explore")

        # Check for area discovery achievements
        area_count = len(self.exploration.discovered_areas)
        if area_count >= 5:
            self.achievements.unlock("discover_5_areas")
        if area_count >= 10:
            self.achievements.unlock("discover_10_areas")

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
                    f"🔨 Crafting: {recipe.name} ({pct}%)\n\n[Press ESC or C to close]",
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
                'label': f"{'✓' if can_craft else '✗'} {recipe.name}",
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
                    f"🏗️ Building: {bp.name}\nStage: {current_stage} ({pct}%)\n\n[Press ESC or R to close]",
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
                'label': f"{'✓' if can_build else '✗'} {bp.name}",
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

        available = self.exploration.get_available_areas()
        current_biome = self.exploration._current_biome
        current_name = current_biome.value.replace("_", " ").title() if current_biome else "Unknown"

        if not available:
            self.renderer.show_message(
                f"═══ AREAS ═══\n\nCurrent: {current_name}\n\n"
                "No other areas discovered yet.\nKeep exploring [E] to find new biomes!\n\n"
                f"Gathering skill: Lv.{self.exploration.gathering_skill}\n\n[ESC or A] Close",
                duration=0
            )
            self._areas_menu_open = True
            return

        # Build menu items
        items = []
        for area in available:
            danger = area.danger_level / 5.0
            danger_str = "🟢" if danger < 0.3 else "🟡" if danger < 0.6 else "🔴"
            items.append({
                'id': area.biome.value if hasattr(area, 'biome') else area.name,
                'label': f"{danger_str} {area.name}",
                'description': f"Danger: {'Low' if danger < 0.3 else 'Medium' if danger < 0.6 else 'High'}",
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

    def _handle_crafting_input(self, key_str: str, key_name: str = "") -> bool:
        """Handle input while crafting menu is open. Returns True if handled."""
        if not self._crafting_menu_open:
            return False

        # If crafting in progress, just handle close
        if self.crafting._current_craft:
            if key_name == 'KEY_ESCAPE' or key_str == 'c':
                self._crafting_menu_open = False
                self._crafting_menu.close()
                self.renderer.dismiss_message()
            return True

        # Let menu handle navigation
        if self._crafting_menu.handle_key(key_str, key_name):
            if self._crafting_menu.was_confirmed():
                # Execute crafting
                selected = self._crafting_menu.get_selected_item()
                if selected and selected.data:
                    recipe = selected.data
                    result = self.crafting.start_crafting(recipe.id, self.materials)
                    self._crafting_menu_open = False
                    self.renderer.show_message(result["message"], duration=3.0)
            elif self._crafting_menu.was_cancelled():
                self._crafting_menu_open = False
                self.renderer.dismiss_message()
            else:
                # Just navigating, update display
                self._update_crafting_menu_display()
            return True

        return False

    def _update_crafting_menu_display(self):
        """Update the crafting menu display with current selection."""
        items = [{'label': item.label, 'description': item.description, 'enabled': item.enabled}
                 for item in self._crafting_menu.get_items()]
        self.renderer.show_menu(
            "CRAFTING",
            items,
            self._crafting_menu.get_selected_index(),
            footer="[↑↓] Navigate  [Enter] Craft  [C/ESC] Close"
        )

    def _handle_building_input(self, key_str: str, key_name: str = "") -> bool:
        """Handle input while building menu is open. Returns True if handled."""
        if not self._building_menu_open:
            return False

        # If building in progress, just handle close
        if self.building._current_build:
            if key_name == 'KEY_ESCAPE' or key_str == 'r':
                self._building_menu_open = False
                self._building_menu.close()
                self.renderer.dismiss_message()
            return True

        # Let menu handle navigation
        if self._building_menu.handle_key(key_str, key_name):
            if self._building_menu.was_confirmed():
                # Execute building
                selected = self._building_menu.get_selected_item()
                if selected and selected.data:
                    bp = selected.data
                    result = self.building.start_building(bp.id, self.materials)
                    self._building_menu_open = False

                    if result.get("success"):
                        self._start_building_animation(bp)
                    else:
                        self.renderer.show_message(result["message"], duration=3.0)
            elif self._building_menu.was_cancelled():
                self._building_menu_open = False
                self.renderer.dismiss_message()
            else:
                # Just navigating, update display
                self._update_building_menu_display()
            return True

        return False

    def _update_building_menu_display(self):
        """Update the building menu display with current selection."""
        items = [{'label': item.label, 'description': item.description, 'enabled': item.enabled}
                 for item in self._building_menu.get_items()]
        self.renderer.show_menu(
            "BUILDING",
            items,
            self._building_menu.get_selected_index(),
            footer="[↑↓] Navigate  [Enter] Build  [R/ESC] Close"
        )

    def _start_building_animation(self, blueprint):
        """Start the duck building animation."""
        self._duck_building = True
        self._building_start_time = time.time()
        
        if self.duck:
            self.duck.current_action = "building"
            self.duck.set_action_message(f"*builds {blueprint.name}* 🔨")
        
        self.renderer.show_message(f"🔨 Building {blueprint.name}...", duration=blueprint.build_time)
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
                f"🏠 {bp.name} Complete!",
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

    def _handle_areas_input(self, key_str: str, key_name: str = "") -> bool:
        """Handle input while areas menu is open. Returns True if handled."""
        if not self._areas_menu_open:
            return False

        # If no areas available, just handle close
        available = self.exploration.get_available_areas()
        if not available:
            if key_name == 'KEY_ESCAPE' or key_str == 'a':
                self._areas_menu_open = False
                self._areas_menu.close()
                self.renderer.dismiss_message()
            return True

        # Let menu handle navigation
        if self._areas_menu.handle_key(key_str, key_name):
            if self._areas_menu.was_confirmed():
                # Travel to selected area
                selected = self._areas_menu.get_selected_item()
                if selected and selected.data:
                    area = selected.data
                    self._areas_menu_open = False
                    self.renderer.dismiss_message()
                    self._start_travel_to_area(area)
            elif self._areas_menu.was_cancelled():
                self._areas_menu_open = False
                self.renderer.dismiss_message()
            else:
                # Just navigating, update display
                self._update_areas_menu_display()
            return True

        return False

    def _update_areas_menu_display(self):
        """Update the areas menu display with current selection."""
        current_biome = self.exploration._current_biome
        current_name = current_biome.value.replace("_", " ").title() if current_biome else "Unknown"

        items = [{'label': item.label, 'description': item.description, 'enabled': item.enabled}
                 for item in self._areas_menu.get_items()]
        self.renderer.show_menu(
            f"AREAS (Current: {current_name})",
            items,
            self._areas_menu.get_selected_index(),
            show_numbers=False,
            footer="[↑↓] Navigate  [Enter] Travel  [A/ESC] Close"
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
        
        self.renderer.show_message(f"🦆 Traveling to {area.name}...", duration=self._travel_duration)
        duck_sounds.play()  # Travel sound

    def _complete_travel(self):
        """Complete the travel and start exploring."""
        if not self._travel_destination:
            self._duck_traveling = False
            return
        
        area = self._travel_destination
        result = self.exploration.travel_to(area)
        
        if result.get("success"):
            # Start exploring immediately after arriving
            self._start_exploring()
            self.renderer.show_message(f"📍 Arrived at {area.name}! Exploring...", duration=2.0)
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
            self.progression.add_xp(result["xp_gained"])
        
        # Show results
        message = result.get("message", "Exploration complete!")
        if result.get("new_area_discovered"):
            self.renderer.show_celebration("discovery", f"🗺️ Discovered: {result['new_area_discovered']}!", duration=3.0)
            duck_sounds.level_up()
        elif result.get("rare_discovery"):
            self.renderer.show_celebration("rare_find", f"✨ Found: {result['rare_discovery']}!", duration=3.0)
            duck_sounds.level_up()
        else:
            self.renderer.show_message(message, duration=4.0)
        
        # Check achievements
        self._check_exploration_achievements()

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
            footer="[↑↓] Navigate  [Enter] Use  [U/ESC] Close"
        )

    def _handle_use_input(self, key_str: str, key_name: str = "") -> bool:
        """Handle input while use menu is open. Returns True if handled."""
        if not self._use_menu_open:
            return False

        # Let menu handle navigation
        if self._use_menu.handle_key(key_str, key_name):
            if self._use_menu.was_confirmed():
                # Use selected item
                selected = self._use_menu.get_selected_item()
                if selected and selected.data:
                    item_id, item = selected.data
                    self._use_menu_open = False
                    self.renderer.dismiss_message()
                    self._execute_item_interaction(item_id)
            elif self._use_menu.was_cancelled():
                self._use_menu_open = False
                self.renderer.dismiss_message()
            else:
                # Just navigating, update display
                self._update_use_menu_display()
            return True

        return False  # Let other keys pass through

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
                self.duck.set_action_message("*turns on boombox* ♪♫ MUSIC TIME! ♫♪")
            self.renderer.show_message("♪♫ Boombox ON! Let's groove! ♫♪", duration=2.0)
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
        for game in games:
            status = "✓" if game["can_play"] else "⏱"
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

        footer = f"Coins: {self.minigames.total_coins_earned} | [↑↓] Navigate  [Enter] Play  [J/ESC] Close"
        self.renderer.show_menu(
            "MINI-GAMES",
            items,
            self._minigames_menu.get_selected_index(),
            footer=footer
        )

    def _handle_minigames_menu_input(self, key_str: str, key_name: str = "") -> bool:
        """Handle input while minigames menu is open."""
        if not self._minigames_menu_open:
            return False

        # Let menu handle navigation
        if self._minigames_menu.handle_key(key_str, key_name):
            if self._minigames_menu.was_confirmed():
                # Start selected game
                selected = self._minigames_menu.get_selected_item()
                if selected and selected.data:
                    self._start_minigame(selected.data["id"])
            elif self._minigames_menu.was_cancelled():
                self._minigames_menu_open = False
                self.renderer.dismiss_message()
            else:
                # Just navigating, update display
                self._update_minigames_menu_display()
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
            lines = ["═══ GAME OVER ═══", ""]
            lines.append(result.message)
            lines.append("")
            lines.append(f"Coins: +{result.coins_earned}")
            lines.append(f"XP: +{result.xp_earned}")
            if result.items_earned:
                lines.append(f"Items: {', '.join(result.items_earned)}")
            if result.high_score:
                lines.append("")
                lines.append("★ NEW HIGH SCORE! ★")
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
        """Show the quests menu."""
        if not self.duck:
            return

        # Get quest log display
        lines = self.quests.render_quest_log()
        
        # Add available quests
        available = self.quests.get_available_quests(self.progression.level)
        
        quest_text = "\n".join(lines)
        quest_text += "\n\n[1-9] Start quest  [ESC/O] Close"
        
        self.renderer.show_message(quest_text, duration=0)

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
        weather = self.atmosphere.current_weather.value if self.atmosphere.current_weather else "sunny"
        
        # Get available activities display
        lines = self.weather_activities.render_activity_selection(weather)
        
        activities_text = "\n".join(lines)
        activities_text += "\n\n[1-9] Start activity  [ESC/W] Close"
        
        self.renderer.show_message(activities_text, duration=0)

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
            "═══ TREASURE HUNTING ═══",
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