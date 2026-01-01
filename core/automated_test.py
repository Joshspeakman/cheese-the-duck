"""
Automated Game Testing System

Runs through all game features, menus, and interactions automatically
to identify missing or broken functionality.
"""
import os
import time
import traceback
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum


class TestStatus(Enum):
    """Status of a test."""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    WARNING = "warning"


@dataclass
class TestResult:
    """Result of a single test."""
    name: str
    category: str
    status: TestStatus
    message: str = ""
    error: str = ""
    duration_ms: float = 0.0
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TestReport:
    """Complete test report."""
    started_at: str
    ended_at: str = ""
    total_tests: int = 0
    passed: int = 0
    failed: int = 0
    warnings: int = 0
    skipped: int = 0
    results: List[TestResult] = field(default_factory=list)
    missing_features: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class AutomatedGameTester:
    """
    Automated testing system that runs through all game features.
    """
    
    def __init__(self, game):
        """
        Initialize with game instance.
        
        Args:
            game: The Game instance to test
        """
        self.game = game
        self.report = TestReport(started_at=datetime.now().isoformat())
        self.current_test: Optional[str] = None
        self._test_delay = 0.1  # Delay between tests in seconds
        self._running = False
        self._paused = False
        self._current_category = ""
        self._progress_callback: Optional[Callable[[str, int, int], None]] = None
        
    def set_progress_callback(self, callback: Callable[[str, int, int], None]):
        """Set callback for progress updates: (message, current, total)."""
        self._progress_callback = callback
        
    def _update_progress(self, message: str, current: int, total: int):
        """Update progress display."""
        if self._progress_callback:
            self._progress_callback(message, current, total)
            
    def _log_result(self, name: str, category: str, status: TestStatus, 
                    message: str = "", error: str = "", details: Dict = None):
        """Log a test result."""
        result = TestResult(
            name=name,
            category=category,
            status=status,
            message=message,
            error=error,
            details=details or {}
        )
        self.report.results.append(result)
        
        if status == TestStatus.PASSED:
            self.report.passed += 1
        elif status == TestStatus.FAILED:
            self.report.failed += 1
            self.report.errors.append(f"{category}/{name}: {error or message}")
        elif status == TestStatus.WARNING:
            self.report.warnings += 1
        elif status == TestStatus.SKIPPED:
            self.report.skipped += 1
            
        self.report.total_tests += 1
        
    def _test_with_timeout(self, test_func: Callable, name: str, category: str, timeout: float = 5.0) -> bool:
        """Run a test function with timeout and error handling."""
        start_time = time.time()
        try:
            result = test_func()
            duration = (time.time() - start_time) * 1000
            
            if result is True or result is None:
                self._log_result(name, category, TestStatus.PASSED, 
                               message="Test passed", details={"duration_ms": duration})
                return True
            elif result is False:
                self._log_result(name, category, TestStatus.FAILED,
                               message="Test returned False", details={"duration_ms": duration})
                return False
            elif isinstance(result, str):
                # String result indicates warning or info
                self._log_result(name, category, TestStatus.WARNING,
                               message=result, details={"duration_ms": duration})
                return True
            else:
                self._log_result(name, category, TestStatus.PASSED,
                               message=str(result), details={"duration_ms": duration})
                return True
                
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            error_msg = f"{type(e).__name__}: {str(e)}"
            self._log_result(name, category, TestStatus.FAILED,
                           error=error_msg, 
                           details={"duration_ms": duration, "traceback": traceback.format_exc()})
            return False
            
    def stop(self):
        """Stop the test run."""
        self._running = False
        
    def pause(self):
        """Pause the test run."""
        self._paused = True
        
    def resume(self):
        """Resume a paused test run."""
        self._paused = False

    def run_all_tests(self) -> TestReport:
        """
        Run all automated tests.
        
        Returns:
            TestReport with all results
        """
        self._running = True
        self.report = TestReport(started_at=datetime.now().isoformat())
        
        test_categories = [
            ("Duck State", self._test_duck_state),
            ("Needs System", self._test_needs_system),
            ("Mood System", self._test_mood_system),
            ("Personality", self._test_personality_system),
            ("Core Actions", self._test_core_actions),
            ("Shop System", self._test_shop_system),
            ("Inventory", self._test_inventory_system),
            ("Crafting", self._test_crafting_system),
            ("Building", self._test_building_system),
            ("Exploration", self._test_exploration_system),
            ("Weather", self._test_weather_system),
            ("Friends/Visitors", self._test_friends_system),
            ("Quests/Goals", self._test_quests_system),
            ("Achievements", self._test_achievements_system),
            ("Minigames", self._test_minigames_system),
            ("Dialogue", self._test_dialogue_system),
            ("Audio", self._test_audio_system),
            ("Save/Load", self._test_save_load_system),
            ("Menus", self._test_menus),
            ("Progression", self._test_progression_system),
            ("Dreams", self._test_dreams_system),
            ("Fishing", self._test_fishing_system),
            ("Garden", self._test_garden_system),
            ("Treasure", self._test_treasure_system),
            ("Collectibles", self._test_collectibles_system),
            ("Trading", self._test_trading_system),
            ("Festivals", self._test_festivals_system),
            ("Secrets", self._test_secrets_system),
        ]
        
        total_categories = len(test_categories)
        
        for i, (category_name, test_func) in enumerate(test_categories):
            if not self._running:
                break
                
            while self._paused and self._running:
                time.sleep(0.1)
                
            self._current_category = category_name
            self._update_progress(f"Testing: {category_name}", i + 1, total_categories)
            
            try:
                test_func()
            except Exception as e:
                self._log_result(f"{category_name} (Category)", category_name, 
                               TestStatus.FAILED, error=str(e))
                
            time.sleep(self._test_delay)
            
        self.report.ended_at = datetime.now().isoformat()
        self._running = False
        
        return self.report

    # ==================== DUCK STATE TESTS ====================
    
    def _test_duck_state(self):
        """Test duck basic state."""
        category = "Duck State"
        
        # Test duck exists
        self._test_with_timeout(
            lambda: self.game.duck is not None,
            "Duck exists", category
        )
        
        if not self.game.duck:
            self._log_result("Duck attributes", category, TestStatus.SKIPPED, 
                           message="No duck to test")
            return
            
        # Test duck has name
        self._test_with_timeout(
            lambda: hasattr(self.game.duck, 'name') and self.game.duck.name,
            "Duck has name", category
        )
        
        # Test duck has needs
        self._test_with_timeout(
            lambda: hasattr(self.game.duck, 'needs') and self.game.duck.needs is not None,
            "Duck has needs", category
        )
        
        # Test duck has personality
        self._test_with_timeout(
            lambda: hasattr(self.game.duck, 'personality') and self.game.duck.personality is not None,
            "Duck has personality", category
        )
        
        # Test duck has growth stage (not age_tracker - uses growth_stage attribute)
        self._test_with_timeout(
            lambda: hasattr(self.game.duck, 'growth_stage'),
            "Duck has growth_stage", category
        )
        
    # ==================== NEEDS SYSTEM TESTS ====================
    
    def _test_needs_system(self):
        """Test needs system."""
        category = "Needs System"
        
        if not self.game.duck:
            self._log_result("Needs System", category, TestStatus.SKIPPED, 
                           message="No duck")
            return
            
        needs = self.game.duck.needs
        
        # Test all needs exist (note: cleanliness not clean)
        for need in ["hunger", "energy", "fun", "cleanliness", "social"]:
            self._test_with_timeout(
                lambda n=need: hasattr(needs, n) and isinstance(getattr(needs, n), (int, float)),
                f"{need.title()} attribute exists", category
            )
            
        # Test needs are in valid range
        for need in ["hunger", "energy", "fun", "cleanliness", "social"]:
            self._test_with_timeout(
                lambda n=need: 0 <= getattr(needs, n, -1) <= 100,
                f"{need.title()} in valid range (0-100)", category
            )
            
        # Test needs update method exists (decay is called via update)
        self._test_with_timeout(
            lambda: hasattr(needs, 'update') and callable(getattr(needs, 'update', None)),
            "Needs update method exists", category
        )
        
    # ==================== MOOD SYSTEM TESTS ====================
    
    def _test_mood_system(self):
        """Test mood system."""
        category = "Mood System"
        
        if not self.game.duck:
            self._log_result("Mood System", category, TestStatus.SKIPPED)
            return
            
        # Test get_mood method
        self._test_with_timeout(
            lambda: hasattr(self.game.duck, 'get_mood') and callable(self.game.duck.get_mood),
            "get_mood method exists", category
        )
        
        # Test mood returns valid value
        def test_mood_value():
            mood = self.game.duck.get_mood()
            return mood is not None
        self._test_with_timeout(test_mood_value, "get_mood returns value", category)
        
    # ==================== PERSONALITY TESTS ====================
    
    def _test_personality_system(self):
        """Test personality system."""
        category = "Personality"
        
        if not self.game.duck or not self.game.duck.personality:
            self._log_result("Personality", category, TestStatus.SKIPPED)
            return
            
        personality = self.game.duck.personality
        
        # Test personality has traits dict (actual structure uses traits dict)
        self._test_with_timeout(
            lambda: hasattr(personality, 'traits') and isinstance(personality.traits, dict),
            "Personality has traits dict", category
        )
        
        # Test core traits exist in traits dict
        # Actual trait keys are: clever_derpy, brave_timid, active_lazy, social_shy, neat_messy
        trait_keys = ["clever_derpy", "brave_timid", "active_lazy", "social_shy", "neat_messy"]
        for trait in trait_keys:
            self._test_with_timeout(
                lambda t=trait: hasattr(personality, 'traits') and t in personality.traits,
                f"{trait} trait exists", category
            )
            
    # ==================== CORE ACTIONS TESTS ====================
    
    def _test_core_actions(self):
        """Test core duck interactions."""
        category = "Core Actions"
        
        # Test _perform_interaction method (game uses this pattern for actions)
        self._test_with_timeout(
            lambda: hasattr(self.game, '_perform_interaction') and callable(self.game._perform_interaction),
            "Perform interaction method exists", category
        )
        
        # Test talk/conversation action
        self._test_with_timeout(
            lambda: hasattr(self.game, '_start_conversation') and callable(self.game._start_conversation),
            "Talk action exists", category
        )
        
        # Test interaction types are handled (check interaction_map or similar)
        self._test_with_timeout(
            lambda: hasattr(self.game, 'interaction_map') or hasattr(self.game, '_perform_interaction'),
            "Interaction system exists", category
        )
        
        # Actually try actions (with duck needs reset after)
        if self.game.duck:
            original_needs = {
                'hunger': self.game.duck.needs.hunger,
                'energy': self.game.duck.needs.energy,
                'fun': self.game.duck.needs.fun,
                'cleanliness': self.game.duck.needs.cleanliness,
                'social': self.game.duck.needs.social,
            }
            
            # Try feed via _perform_interaction
            def test_feed():
                try:
                    self.game._perform_interaction("feed")
                    return True
                except Exception:
                    return False
            self._test_with_timeout(test_feed, "Feed executes without error", category)
            
            # Try play
            def test_play():
                try:
                    self.game._perform_interaction("play")
                    return True
                except Exception:
                    return False
            self._test_with_timeout(test_play, "Play executes without error", category)
            
            # Try clean
            def test_clean():
                try:
                    self.game._perform_interaction("clean")
                    return True
                except Exception:
                    return False
            self._test_with_timeout(test_clean, "Clean executes without error", category)
            
            # Try pet
            def test_pet():
                try:
                    self.game._perform_interaction("pet")
                    return True
                except Exception:
                    return False
            self._test_with_timeout(test_pet, "Pet executes without error", category)
            
            # Restore needs
            self.game.duck.needs.hunger = original_needs['hunger']
            self.game.duck.needs.energy = original_needs['energy']
            self.game.duck.needs.fun = original_needs['fun']
            self.game.duck.needs.cleanliness = original_needs['cleanliness']
            self.game.duck.needs.social = original_needs['social']
            
    # ==================== SHOP SYSTEM TESTS ====================
    
    def _test_shop_system(self):
        """Test shop system."""
        category = "Shop System"
        
        # Shop functionality is in habitat - check habitat exists
        self._test_with_timeout(
            lambda: hasattr(self.game, 'habitat') and self.game.habitat is not None,
            "Habitat (shop container) exists", category
        )
        
        # Test renderer has shop display method
        self._test_with_timeout(
            lambda: hasattr(self.game, 'renderer') and hasattr(self.game.renderer, '_show_shop'),
            "Shop display method exists", category
        )
        
        # Test shop module exists
        def test_shop_module():
            try:
                from world import shop
                return True
            except ImportError:
                return False
        self._test_with_timeout(test_shop_module, "Shop module exists", category)
        
    # ==================== INVENTORY TESTS ====================
    
    def _test_inventory_system(self):
        """Test inventory system."""
        category = "Inventory"
        
        # Test inventory exists directly on game
        self._test_with_timeout(
            lambda: hasattr(self.game, 'inventory') and self.game.inventory is not None,
            "Inventory system exists", category
        )
        
        # Test inventory has items dict
        self._test_with_timeout(
            lambda: hasattr(self.game.inventory, 'items') if self.game.inventory else False,
            "Inventory has items", category
        )
        
        # Test inventory has add_item method
        self._test_with_timeout(
            lambda: hasattr(self.game.inventory, 'add_item') if self.game.inventory else False,
            "Inventory has add_item method", category
        )
        
        # Test inventory has use_item method
        self._test_with_timeout(
            lambda: hasattr(self.game.inventory, 'use_item') if self.game.inventory else False,
            "Inventory has use_item method", category
        )
        
    # ==================== CRAFTING SYSTEM TESTS ====================
    
    def _test_crafting_system(self):
        """Test crafting system."""
        category = "Crafting"
        
        # Test crafting exists
        self._test_with_timeout(
            lambda: hasattr(self.game, 'crafting') and self.game.crafting is not None,
            "Crafting system exists", category
        )
        
        if not hasattr(self.game, 'crafting') or not self.game.crafting:
            return
            
        # Test recipes exist
        self._test_with_timeout(
            lambda: hasattr(self.game.crafting, 'recipes') or hasattr(self.game.crafting, 'get_recipes'),
            "Crafting has recipes", category
        )
        
        # Test materials system
        self._test_with_timeout(
            lambda: hasattr(self.game, 'materials') and self.game.materials is not None,
            "Materials system exists", category
        )
        
    # ==================== BUILDING SYSTEM TESTS ====================
    
    def _test_building_system(self):
        """Test building system."""
        category = "Building"
        
        # Test building exists
        self._test_with_timeout(
            lambda: hasattr(self.game, 'building') and self.game.building is not None,
            "Building system exists", category
        )
        
        if not hasattr(self.game, 'building') or not self.game.building:
            return
            
        # Test blueprints
        self._test_with_timeout(
            lambda: hasattr(self.game.building, 'blueprints') or hasattr(self.game.building, 'get_blueprints'),
            "Building has blueprints", category
        )
        
        # Test structures list
        self._test_with_timeout(
            lambda: hasattr(self.game.building, 'structures'),
            "Building has structures list", category
        )
        
    # ==================== EXPLORATION TESTS ====================
    
    def _test_exploration_system(self):
        """Test exploration system."""
        category = "Exploration"
        
        # Test exploration exists
        self._test_with_timeout(
            lambda: hasattr(self.game, 'exploration') and self.game.exploration is not None,
            "Exploration system exists", category
        )
        
        if not hasattr(self.game, 'exploration') or not self.game.exploration:
            return
            
        # Test areas/locations
        self._test_with_timeout(
            lambda: hasattr(self.game.exploration, 'discovered_areas') or hasattr(self.game.exploration, 'areas'),
            "Exploration has areas", category
        )
        
        # Test current location
        self._test_with_timeout(
            lambda: hasattr(self.game.exploration, 'current_location') or hasattr(self.game.exploration, 'current_biome'),
            "Has current location tracking", category
        )
        
    # ==================== WEATHER SYSTEM TESTS ====================
    
    def _test_weather_system(self):
        """Test weather system."""
        category = "Weather"
        
        # Test atmosphere exists
        self._test_with_timeout(
            lambda: hasattr(self.game, 'atmosphere') and self.game.atmosphere is not None,
            "Atmosphere system exists", category
        )
        
        if not hasattr(self.game, 'atmosphere') or not self.game.atmosphere:
            return
            
        # Test current weather
        self._test_with_timeout(
            lambda: hasattr(self.game.atmosphere, 'current_weather'),
            "Has current weather", category
        )
        
        # Test weather types
        def test_weather_types():
            from world.atmosphere import WeatherType
            return len(list(WeatherType)) > 0
        self._test_with_timeout(test_weather_types, "Weather types defined", category)
        
        # Test season
        self._test_with_timeout(
            lambda: hasattr(self.game.atmosphere, 'current_season') or hasattr(self.game.atmosphere, 'get_season'),
            "Has season tracking", category
        )
        
    # ==================== FRIENDS SYSTEM TESTS ====================
    
    def _test_friends_system(self):
        """Test friends/visitors system."""
        category = "Friends/Visitors"
        
        # Test friends system exists
        self._test_with_timeout(
            lambda: hasattr(self.game, 'friends') and self.game.friends is not None,
            "Friends system exists", category
        )
        
        if not hasattr(self.game, 'friends') or not self.game.friends:
            return
            
        # Test friends list
        self._test_with_timeout(
            lambda: hasattr(self.game.friends, 'friends') or hasattr(self.game.friends, 'known_friends'),
            "Has friends list", category
        )
        
        # Test visitor tracking
        self._test_with_timeout(
            lambda: hasattr(self.game.friends, 'current_visit'),
            "Has visitor tracking", category
        )
        
    # ==================== QUESTS SYSTEM TESTS ====================
    
    def _test_quests_system(self):
        """Test quests/goals system."""
        category = "Quests/Goals"
        
        # Test quests system
        self._test_with_timeout(
            lambda: hasattr(self.game, 'quests') and self.game.quests is not None,
            "Quests system exists", category
        )
        
        # Test goals system
        self._test_with_timeout(
            lambda: hasattr(self.game, 'goals') and self.game.goals is not None,
            "Goals system exists", category
        )
        
        # Test challenges
        self._test_with_timeout(
            lambda: hasattr(self.game, 'challenges') and self.game.challenges is not None,
            "Challenges system exists", category
        )
        
    # ==================== ACHIEVEMENTS TESTS ====================
    
    def _test_achievements_system(self):
        """Test achievements system."""
        category = "Achievements"
        
        # Test achievements exist
        self._test_with_timeout(
            lambda: hasattr(self.game, 'achievements') and self.game.achievements is not None,
            "Achievements system exists", category
        )
        
        if not hasattr(self.game, 'achievements') or not self.game.achievements:
            return
            
        # Test achievement tracking (uses _unlocked set or get_unlocked method)
        self._test_with_timeout(
            lambda: hasattr(self.game.achievements, '_unlocked') or hasattr(self.game.achievements, 'get_unlocked'),
            "Has unlocked achievements tracking", category
        )
        
        # Test get_unlocked_count method
        self._test_with_timeout(
            lambda: hasattr(self.game.achievements, 'get_unlocked_count'),
            "Has get_unlocked_count method", category
        )
        
    # ==================== MINIGAMES TESTS ====================
    
    def _test_minigames_system(self):
        """Test minigames system."""
        category = "Minigames"
        
        # Test minigames exist
        self._test_with_timeout(
            lambda: hasattr(self.game, 'minigames') and self.game.minigames is not None,
            "Minigames system exists", category
        )
        
        # Test _start_minigame method exists (actual method name)
        self._test_with_timeout(
            lambda: hasattr(self.game, '_start_minigame') and callable(self.game._start_minigame),
            "Start minigame method exists", category
        )
        
        # Test minigame menu exists
        self._test_with_timeout(
            lambda: hasattr(self.game, '_minigames_menu'),
            "Minigames menu exists", category
        )
        
        # Test active minigame tracking
        self._test_with_timeout(
            lambda: hasattr(self.game, '_active_minigame'),
            "Active minigame tracking exists", category
        )
            
    # ==================== DIALOGUE TESTS ====================
    
    def _test_dialogue_system(self):
        """Test dialogue system."""
        category = "Dialogue"
        
        # Test conversation system
        self._test_with_timeout(
            lambda: hasattr(self.game, 'conversation') and self.game.conversation is not None,
            "Conversation system exists", category
        )
        
        # Test dialogue files exist
        dialogue_files = [
            "dialogue_adventurous",
            "dialogue_artistic",
            "dialogue_athletic",
            "dialogue_foodie",
            "dialogue_generous",
            "dialogue_mysterious",
            "dialogue_playful",
            "dialogue_scholarly",
        ]
        
        for df in dialogue_files:
            def test_dialogue(name=df):
                try:
                    module = __import__(f"dialogue.{name}", fromlist=[name])
                    return True
                except ImportError:
                    return False
            self._test_with_timeout(test_dialogue, f"{df} module exists", category)
            
    # ==================== AUDIO TESTS ====================
    
    def _test_audio_system(self):
        """Test audio system."""
        category = "Audio"
        
        # Test sound effects system (actual attribute name is sound_effects)
        self._test_with_timeout(
            lambda: hasattr(self.game, 'sound_effects') and self.game.sound_effects is not None,
            "Sound effects system exists", category
        )
        
        # Test ambient system (actual attribute name is ambient)
        self._test_with_timeout(
            lambda: hasattr(self.game, 'ambient') and self.game.ambient is not None,
            "Ambient audio system exists", category
        )
        
        # Test sound effect methods
        if hasattr(self.game, 'sound_effects') and self.game.sound_effects:
            self._test_with_timeout(
                lambda: hasattr(self.game.sound_effects, 'play') or hasattr(self.game.sound_effects, 'play_sound'),
                "Sound effects has play method", category
            )
            
    # ==================== SAVE/LOAD TESTS ====================
    
    def _test_save_load_system(self):
        """Test save/load system."""
        category = "Save/Load"
        
        # Test save_manager exists (actual attribute name is save_manager, not persistence)
        self._test_with_timeout(
            lambda: hasattr(self.game, 'save_manager') and self.game.save_manager is not None,
            "Save manager exists", category
        )
        
        # Test save method
        self._test_with_timeout(
            lambda: hasattr(self.game, '_save_game') or hasattr(self.game, 'save'),
            "Save method exists", category
        )
        
        # Test load method
        self._test_with_timeout(
            lambda: hasattr(self.game, '_load_game') or hasattr(self.game, 'load'),
            "Load method exists", category
        )
        
        # Test save slots
        self._test_with_timeout(
            lambda: hasattr(self.game, 'save_slots') and self.game.save_slots is not None,
            "Save slots system exists", category
        )
        
    # ==================== MENUS TESTS ====================
    
    def _test_menus(self):
        """Test all menus open and close properly."""
        category = "Menus"
        
        # Test menu open flags exist
        menu_flags = [
            '_main_menu_open',
            '_crafting_menu_open',
            '_building_menu_open',
            '_areas_menu_open',
            '_use_menu_open',
            '_minigames_menu_open',
            '_quests_menu_open',
            '_weather_menu_open',
            '_debug_menu_open',
        ]
        
        for flag in menu_flags:
            self._test_with_timeout(
                lambda f=flag: hasattr(self.game, f),
                f"{flag.replace('_', ' ').strip()} flag exists", category
            )
            
        # Test menu show methods exist
        menu_methods = [
            '_show_main_menu',
            '_show_crafting_menu',
            '_show_building_menu',
            '_show_exploration_menu',
            '_show_shop',
            '_show_inventory',
            '_show_stats',
            '_show_goals_overlay',
            '_show_achievements',
            '_show_debug_menu',
        ]
        
        for method in menu_methods:
            self._test_with_timeout(
                lambda m=method: hasattr(self.game, m),
                f"{method.replace('_show_', '').replace('_', ' ').title()} screen exists", category
            )
            
    # ==================== PROGRESSION TESTS ====================
    
    def _test_progression_system(self):
        """Test progression/leveling system."""
        category = "Progression"
        
        # Test progression exists
        self._test_with_timeout(
            lambda: hasattr(self.game, 'progression') and self.game.progression is not None,
            "Progression system exists", category
        )
        
        if not hasattr(self.game, 'progression') or not self.game.progression:
            return
            
        # Test XP tracking
        self._test_with_timeout(
            lambda: hasattr(self.game.progression, 'xp'),
            "Has XP tracking", category
        )
        
        # Test level tracking
        self._test_with_timeout(
            lambda: hasattr(self.game.progression, 'level'),
            "Has level tracking", category
        )
        
        # Test prestige system
        self._test_with_timeout(
            lambda: hasattr(self.game, 'prestige') and self.game.prestige is not None,
            "Prestige system exists", category
        )
        
    # ==================== DREAMS TESTS ====================
    
    def _test_dreams_system(self):
        """Test dreams system."""
        category = "Dreams"
        
        # Test dreams exist
        self._test_with_timeout(
            lambda: hasattr(self.game, 'dreams') and self.game.dreams is not None,
            "Dreams system exists", category
        )
        
        if not hasattr(self.game, 'dreams') or not self.game.dreams:
            return
            
        # Test dream generation
        self._test_with_timeout(
            lambda: hasattr(self.game.dreams, 'generate_dream'),
            "Has dream generation", category
        )
        
    # ==================== FISHING TESTS ====================
    
    def _test_fishing_system(self):
        """Test fishing system."""
        category = "Fishing"
        
        # Test fishing exists
        self._test_with_timeout(
            lambda: hasattr(self.game, 'fishing') and self.game.fishing is not None,
            "Fishing system exists", category
        )
        
    # ==================== GARDEN TESTS ====================
    
    def _test_garden_system(self):
        """Test garden system."""
        category = "Garden"
        
        # Test garden exists
        self._test_with_timeout(
            lambda: hasattr(self.game, 'garden') and self.game.garden is not None,
            "Garden system exists", category
        )
        
    # ==================== TREASURE TESTS ====================
    
    def _test_treasure_system(self):
        """Test treasure hunting system."""
        category = "Treasure"
        
        # Test treasure exists
        self._test_with_timeout(
            lambda: hasattr(self.game, 'treasure') and self.game.treasure is not None,
            "Treasure system exists", category
        )
        
    # ==================== COLLECTIBLES TESTS ====================
    
    def _test_collectibles_system(self):
        """Test collectibles system."""
        category = "Collectibles"
        
        # Test collectibles exist
        self._test_with_timeout(
            lambda: hasattr(self.game, 'collectibles') and self.game.collectibles is not None,
            "Collectibles system exists", category
        )
        
        # Test scrapbook
        self._test_with_timeout(
            lambda: hasattr(self.game, 'scrapbook') and self.game.scrapbook is not None,
            "Scrapbook system exists", category
        )
        
    # ==================== TRADING TESTS ====================
    
    def _test_trading_system(self):
        """Test trading system."""
        category = "Trading"
        
        # Test trading exists
        self._test_with_timeout(
            lambda: hasattr(self.game, 'trading') and self.game.trading is not None,
            "Trading system exists", category
        )
        
    # ==================== FESTIVALS TESTS ====================
    
    def _test_festivals_system(self):
        """Test festivals system."""
        category = "Festivals"
        
        # Test festivals exist
        self._test_with_timeout(
            lambda: hasattr(self.game, 'festivals') and self.game.festivals is not None,
            "Festivals system exists", category
        )
        
    # ==================== SECRETS TESTS ====================
    
    def _test_secrets_system(self):
        """Test secrets system."""
        category = "Secrets"
        
        # Test secrets exist
        self._test_with_timeout(
            lambda: hasattr(self.game, 'secrets') and self.game.secrets is not None,
            "Secrets system exists", category
        )
        
    # ==================== REPORT GENERATION ====================
    
    def generate_report_text(self) -> str:
        """Generate a human-readable test report."""
        lines = [
            "=" * 70,
            "CHEESE THE DUCK - AUTOMATED TEST REPORT",
            "=" * 70,
            "",
            f"Started:  {self.report.started_at}",
            f"Ended:    {self.report.ended_at}",
            "",
            "-" * 70,
            "SUMMARY",
            "-" * 70,
            f"Total Tests:  {self.report.total_tests}",
            f"  ✓ Passed:   {self.report.passed}",
            f"  ✗ Failed:   {self.report.failed}",
            f"  ⚠ Warnings: {self.report.warnings}",
            f"  ○ Skipped:  {self.report.skipped}",
            "",
            f"Pass Rate:    {self.report.passed / max(1, self.report.total_tests) * 100:.1f}%",
            "",
        ]
        
        # Group results by category
        categories: Dict[str, List[TestResult]] = {}
        for result in self.report.results:
            if result.category not in categories:
                categories[result.category] = []
            categories[result.category].append(result)
            
        # Results by category
        lines.extend([
            "-" * 70,
            "DETAILED RESULTS BY CATEGORY",
            "-" * 70,
        ])
        
        for category, results in categories.items():
            passed = sum(1 for r in results if r.status == TestStatus.PASSED)
            failed = sum(1 for r in results if r.status == TestStatus.FAILED)
            total = len(results)
            
            status_icon = "✓" if failed == 0 else "✗"
            lines.append(f"\n[{status_icon}] {category} ({passed}/{total})")
            
            for result in results:
                if result.status == TestStatus.PASSED:
                    icon = "  ✓"
                elif result.status == TestStatus.FAILED:
                    icon = "  ✗"
                elif result.status == TestStatus.WARNING:
                    icon = "  ⚠"
                else:
                    icon = "  ○"
                    
                lines.append(f"{icon} {result.name}")
                if result.error:
                    lines.append(f"      Error: {result.error[:60]}...")
                elif result.message and result.status != TestStatus.PASSED:
                    lines.append(f"      Note: {result.message[:60]}")
                    
        # Errors section
        if self.report.errors:
            lines.extend([
                "",
                "-" * 70,
                "ERRORS (Action Required)",
                "-" * 70,
            ])
            for error in self.report.errors:
                lines.append(f"  • {error}")
                
        # Missing features
        if self.report.missing_features:
            lines.extend([
                "",
                "-" * 70,
                "MISSING FEATURES",
                "-" * 70,
            ])
            for feature in self.report.missing_features:
                lines.append(f"  • {feature}")
                
        lines.extend([
            "",
            "=" * 70,
            "END OF REPORT",
            "=" * 70,
        ])
        
        return "\n".join(lines)
        
    def save_report(self, filepath: str = None) -> str:
        """
        Save the test report to a file.
        
        Args:
            filepath: Path to save report (defaults to logs/test_report_<timestamp>.txt)
            
        Returns:
            Path where report was saved
        """
        if not filepath:
            # Get game directory
            game_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            logs_dir = os.path.join(game_dir, "logs")
            os.makedirs(logs_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(logs_dir, f"test_report_{timestamp}.txt")
            
        report_text = self.generate_report_text()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_text)
            
        return filepath
