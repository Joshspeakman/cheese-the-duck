"""
Main game controller - manages game loop and state.
Enhanced with progression, daily rewards, collectibles, and addiction mechanics.
"""
import time
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
from dialogue.diary import DuckDiary, duck_diary, DiaryEntryType
from audio.sound import sound_engine, duck_sounds
from ui.renderer import Renderer
from ui.animations import animation_controller
from ui.input_handler import InputHandler, GameAction


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

        self._running = False
        self._state = "init"  # init, title, playing, paused, daily_rewards
        self._last_tick = 0.0
        self._last_save = 0.0
        self._last_event_check = 0.0
        self._last_progression_check = 0.0
        self._last_atmosphere_check = 0.0
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
        if key.name == "KEY_ESCAPE":
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

        # Purchase item
        key_str = str(key).lower()
        if key_str == 'b':
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

    def _handle_action(self, action: GameAction, key=None):
        """Handle a game action."""
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

        # Check for direct key actions first (S, T, I, G, M, B, N, X, +, -) even if action is NONE
        if self._state == "playing" and self.duck and key:
            key_str = str(key).lower()
            if key_str in ['s', 't', 'i', 'g', 'm', 'b', 'n', 'x', '+', '=', '-', '_']:
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
        # Check for direct key-based actions first (to avoid conflicts)
        if key:
            key_str = str(key).lower()

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

        # Interaction actions (from GameAction enum)
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

        # Autonomous behavior
        if self.behavior_ai:
            result = self.behavior_ai.perform_action(self.duck, current_time)
            if result:
                self.duck.set_action_message(result.message)

                # Update visual state based on action
                if result.action.value in ["nap", "sleep"]:
                    self.renderer.set_duck_state("sleeping")
                elif result.action.value in ["waddle", "look_around", "chase_bug"]:
                    self.renderer.set_duck_state("walking")
                elif result.action.value in ["splash", "wiggle", "flap_wings"]:
                    self.renderer.set_duck_state("playing")

                # Show closeup for emotive actions
                emotive_actions = ["stare_blankly", "trip", "quack", "wiggle", "flap_wings"]
                if result.action.value in emotive_actions:
                    self.renderer.show_closeup(result.action.value, 1.5)
                
                # Play quack sound when duck talks to itself or does vocal actions
                vocal_actions = ["quack", "look_around", "chase_bug", "trip", "wiggle", "splash"]
                if result.action.value in vocal_actions:
                    mood = self.duck.get_mood().state.value
                    duck_sounds.quack(mood)

        # Duck interacts with nearby habitat items (10% chance per update)
        self._check_item_interaction(current_time)

        # Auto-save every 60 seconds
        if current_time - self._last_save >= 60:
            self._save_game()
            self._last_save = current_time

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

        # Load weather history for secret goal
        self._weather_seen = set(data.get("weather_seen", []))

        # Check daily login and streak
        self._check_daily_login()

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
            "statistics": self._statistics,
            "weather_seen": list(self._weather_seen),
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
