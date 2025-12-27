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

        self._running = False
        self._state = "init"  # init, title, playing, paused, daily_rewards
        self._last_tick = 0.0
        self._last_save = 0.0
        self._last_event_check = 0.0
        self._last_progression_check = 0.0
        self._statistics = {}
        self._pending_offline_summary = None
        self._pending_daily_rewards = []
        self._sound_enabled = True
        self._show_goals = False

    def start(self):
        """Start the game."""
        self._running = True

        # Check for existing save
        if self.save_manager.save_exists():
            self._load_game()
        else:
            self._state = "title"

        self._game_loop()

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

        # Play quack sound
        mood = self.duck.get_mood().state.value
        duck_sounds.quack(mood)

        # Check goals
        self.goals.update_progress("talk", 1)

    def _handle_action(self, action: GameAction, key=None):
        """Handle a game action."""
        # Check for direct key actions first (S, T, I, G, M) even if action is NONE
        if self._state == "playing" and self.duck and key:
            key_str = str(key).lower()
            if key_str in ['s', 't', 'i', 'g', 'm']:
                self._handle_playing_action(action, key)
                return

        if action == GameAction.NONE:
            return

        # Global actions
        if action == GameAction.QUIT:
            self._quit()
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

            # Sound toggle [M]
            if key_str == 'm':
                self._sound_enabled = sound_engine.toggle()
                status = "ON" if self._sound_enabled else "OFF"
                self.renderer.show_message(f"Sound: {status}")
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

        # Clear any autonomous action
        if self.behavior_ai:
            self.behavior_ai.clear_action()

        # Set duck visual state
        if interaction == "feed":
            self.renderer.set_duck_state("eating")
        elif interaction == "play":
            self.renderer.set_duck_state("playing")
        elif interaction == "sleep":
            self.renderer.set_duck_state("sleeping")
        else:
            self.renderer.set_duck_state("idle")

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

        # Update goals
        self.goals.update_progress(interaction, 1)

        # Update progression system
        self.progression.record_interaction(interaction)
        self.progression.update_challenge_progress(interaction, 1)

        # Check for happy interactions (for challenges)
        if mood.score > 60:
            self.progression.update_challenge_progress("happy", 1)

        # Random collectible chance on interactions
        collectible = self.progression.random_collectible_drop(0.03)
        if collectible:
            self._show_collectible_found(collectible)

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
        elif interaction == "play":
            self.renderer.show_effect("sparkle", 1.0)
            self.renderer.show_closeup("play", 2.0)
        elif interaction == "feed":
            self.renderer.show_closeup("feed", 2.0)
        elif interaction == "sleep":
            self.renderer.show_closeup("sleep", 2.5)
        elif interaction == "clean":
            self.renderer.show_closeup(None, 1.5)

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
        self.renderer.show_message(f"LEVEL UP! You reached Level {new_level}!", duration=4.0)

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

            self.renderer.show_message(f"Found {rarity_prefix}collectible: {name}!", duration=4.0)

    def _show_milestone_achieved(self, category: str, threshold: int, reward: Reward):
        """Show notification for milestone achievement."""
        duck_sounds.level_up()
        self.renderer.show_effect("sparkle", 1.5)
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
        is_new_day, rewards = self.progression.check_login()

        if is_new_day and rewards:
            # Generate daily challenges
            self.progression.generate_daily_challenges()

            # Show streak info
            streak = self.progression.current_streak
            if streak > 1:
                self.renderer.show_message(f"Day {streak} streak! Keep it going!", duration=3.0)
            else:
                self.renderer.show_message("Welcome back! Claim your daily reward!", duration=3.0)

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

            # Update goals (time-based)
            self.goals.update_time(delta_minutes)

            self._last_tick = current_time

        # Check for random events (every 10 seconds)
        if current_time - self._last_event_check >= 10:
            self._check_events()
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

        # Auto-save every 60 seconds
        if current_time - self._last_save >= 60:
            self._save_game()
            self._last_save = current_time

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
            "statistics": self._statistics,
        }

        self.save_manager.save(save_data)

    def _quit(self):
        """Quit the game."""
        if self.duck:
            self._save_game()
            self.renderer.show_message("Saving and quitting...")
            time.sleep(0.5)

        # Stop any playing music
        sound_engine.stop_music()

        self._running = False
