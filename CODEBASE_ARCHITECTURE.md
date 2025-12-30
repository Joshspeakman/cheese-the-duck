# Cheese the Duck - Complete Codebase Architecture

> A comprehensive documentation for AI assistants and developers to understand the entire codebase structure, module connections, and function purposes.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Directory Structure](#directory-structure)
3. [Module Dependency Graph](#module-dependency-graph)
4. [Core Modules](#core-modules)
5. [Duck Modules](#duck-modules)
6. [UI Modules](#ui-modules)
7. [World Modules](#world-modules)
8. [Dialogue Modules](#dialogue-modules)
9. [Audio Modules](#audio-modules)
10. [Data Flow](#data-flow)
11. [Save/Load System](#saveload-system)
12. [Key Integration Points](#key-integration-points)

---

## Project Overview

**Cheese the Duck** is a terminal-based virtual pet game written in Python. It features:

- **ASCII art rendering** using the `blessed` terminal library
- **Virtual pet mechanics** (feeding, playing, cleaning, petting, sleeping)
- **Personality system** with traits affecting behavior
- **Growth stages** from egg to legendary
- **Weather and day/night cycles**
- **Exploration, fishing, gardening, crafting, and building systems**
- **Quest and achievement systems**
- **Local LLM integration** for dynamic conversations
- **Chiptune audio** using pygame

### Tech Stack
- **Python 3.13+**
- **blessed** - Terminal rendering and input
- **pygame** - Audio playback
- **llama-cpp-python** (optional) - Local LLM for conversations

### Entry Point
```
main.py → Game.start() → Game._game_loop()
```

---

## Directory Structure

```
stupid_duck/
├── main.py                 # Entry point
├── config.py               # Global configuration constants
├── download_model.py       # LLM model downloader
├── requirements.txt        # Python dependencies
├── run_game.sh            # Shell launcher script
│
├── core/                   # Core game systems
│   ├── game.py            # Main game controller & loop
│   ├── clock.py           # Time management
│   ├── persistence.py     # Save/load system
│   ├── prestige.py        # Rebirth/legacy system
│   ├── progression.py     # XP, levels, streaks
│   └── save_slots.py      # Multi-slot save management
│
├── duck/                   # Duck entity & behavior
│   ├── duck.py            # Main Duck dataclass
│   ├── mood.py            # Mood calculation
│   ├── needs.py           # Hunger, energy, fun, etc.
│   ├── behavior_ai.py     # Autonomous AI behaviors
│   ├── personality.py     # Core personality traits
│   ├── personality_extended.py  # Extended traits/quirks
│   ├── aging.py           # Growth stages
│   ├── cosmetics.py       # Visual cosmetics rendering
│   ├── outfits.py         # Equippable outfit items
│   ├── seasonal_clothing.py    # Season-specific items
│   ├── titles.py          # Unlockable titles
│   └── tricks.py          # Learnable tricks
│
├── ui/                     # User interface & rendering
│   ├── renderer.py        # Main terminal renderer
│   ├── ascii_art.py       # Duck art & closeups
│   ├── animations.py      # Animation controller
│   ├── badges.py          # Badge display system
│   ├── day_night.py       # Time-of-day visuals
│   ├── habitat_art.py     # Item ASCII art
│   ├── habitat_icons.py   # Small item icons
│   ├── input_handler.py   # Keyboard input processing
│   ├── location_art.py    # Location backgrounds
│   ├── mood_visuals.py    # Mood-based visual effects
│   └── statistics.py      # Stats tracking & display
│
├── world/                  # Game world systems
│   ├── achievements.py    # Achievement definitions
│   ├── atmosphere.py      # Weather & seasons
│   ├── building.py        # Structure construction
│   ├── challenges.py      # Daily/weekly challenges
│   ├── collectibles.py    # Trading cards/stickers
│   ├── crafting.py        # Crafting recipes
│   ├── decorations.py     # Room decorations
│   ├── dreams.py          # Dream sequences
│   ├── events.py          # Random events
│   ├── exploration.py     # Biome exploration
│   ├── facts.py           # Fun facts database
│   ├── festivals.py       # Seasonal festivals
│   ├── fishing.py         # Fishing minigame
│   ├── fortune.py         # Horoscopes & fortunes
│   ├── friends.py         # Visiting duck friends
│   ├── garden.py          # Plant growing
│   ├── goals.py           # Quest objectives
│   ├── habitat.py         # Habitat/home management
│   ├── home.py            # Home decorations
│   ├── item_interactions.py   # Item use animations
│   ├── items.py           # Item definitions
│   ├── materials.py       # Crafting materials
│   ├── minigames.py       # Minigame implementations
│   ├── quests.py          # Multi-step quests
│   ├── scrapbook.py       # Photo album
│   ├── secrets.py         # Easter eggs
│   ├── shop.py            # In-game shop
│   ├── trading.py         # NPC traders
│   ├── treasure.py        # Treasure hunting
│   └── weather_activities.py  # Weather-based activities
│
├── dialogue/               # Conversation systems
│   ├── conversation.py    # Main chat system
│   ├── diary.py           # Life journal
│   ├── diary_enhanced.py  # Extended diary features
│   ├── llm_chat.py        # Local LLM integration
│   ├── memory.py          # Duck memory system
│   └── mood_dialogue.py   # Context-aware dialogue
│
├── audio/                  # Sound systems
│   ├── sound.py           # Core audio engine
│   ├── sound_effects.py   # Text-based sound effects
│   └── ambient.py         # Environmental audio
│
├── models/                 # LLM model files
│   └── tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
│
└── data/                   # Game data files
```

---

## Module Dependency Graph

```
                              ┌─────────────────┐
                              │   main.py       │
                              └────────┬────────┘
                                       │
                              ┌────────▼────────┐
                              │    Game         │
                              │  (core/game.py) │
                              └────────┬────────┘
                                       │
    ┌──────────────────────────────────┼──────────────────────────────────┐
    │                                  │                                  │
    ▼                                  ▼                                  ▼
┌───────────────┐            ┌─────────────────┐            ┌─────────────────┐
│    Duck       │            │    Renderer     │            │   World Systems │
│ (duck/duck.py)│            │(ui/renderer.py) │            │   (world/*.py)  │
└───────┬───────┘            └────────┬────────┘            └────────┬────────┘
        │                             │                              │
        │                             │                              │
   ┌────┴────┐                   ┌────┴────┐                    ┌────┴────┐
   ▼         ▼                   ▼         ▼                    ▼         ▼
┌──────┐ ┌──────┐          ┌──────┐  ┌──────┐            ┌──────┐  ┌──────┐
│Needs │ │ Mood │          │ASCII │  │Anim  │            │Shop  │  │Events│
│Pers. │ │ AI   │          │Art   │  │Loc.  │            │Habit │  │Atmos │
└──────┘ └──────┘          └──────┘  └──────┘            └──────┘  └──────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                           Core Systems                                   │
├─────────────────┬─────────────────┬─────────────────┬───────────────────┤
│   GameClock     │   SaveManager   │ ProgressionSys  │   PrestigeSys     │
│  (clock.py)     │ (persistence.py)│ (progression.py)│   (prestige.py)   │
└─────────────────┴─────────────────┴─────────────────┴───────────────────┘
        │                  │                  │                  │
        └──────────────────┴──────────────────┴──────────────────┘
                                    │
                           Used globally by Game
```

---

## Core Modules

### `core/game.py` - Main Game Controller

**Class: `Game`** (2000+ lines)

The central orchestrator that manages the entire game loop and coordinates all subsystems.

#### State Machine
```
"init" → "slot_select" → "playing" → "paused" → "daily_rewards"
                ↑_______________↓
```

#### Key Methods

| Method | Description |
|--------|-------------|
| `start()` | Entry point - checks for saves, shows slot selection, starts game loop |
| `_game_loop()` | Main loop: `input → update → render` at 30 FPS |
| `_handle_action(key)` | Routes keyboard input to appropriate handlers |
| `_handle_playing_action(action)` | Processes game actions (feed, play, clean, pet, sleep) |
| `_load_game(save_data)` | Loads save data and initializes all systems |
| `_update(delta)` | Updates duck state, events, progression, atmosphere |
| `_render()` | Delegates rendering to the Renderer |
| `_save_game()` | Serializes all systems and saves to file |
| `_handle_talk()` | Processes conversation mode with LLM support |
| `_handle_shop_action()` | Shop navigation and purchasing |
| `_run_item_interaction()` | Animated item interactions |

#### Instantiated Systems
```python
self.duck = Duck                      # The pet duck
self.habitat = Habitat                # Home/items
self.inventory = Inventory            # Player inventory
self.friends = FriendsSystem          # Visiting friends
self.atmosphere = AtmosphereSystem    # Weather/seasons
self.material_inventory = MaterialInventory  # Crafting materials
self.fishing = FishingLog             # Fish collection
self.garden = Garden                  # Plants
self.building = BuildingSystem        # Structures
self.secrets = SecretsSystem          # Easter eggs
self.scrapbook = Scrapbook           # Photo album
self.quests = QuestSystem            # Quest tracking
self.trading = TradingSystem         # NPC trading
self.minigames = MinigamesSystem     # Minigame state
self.treasure = TreasureSystem       # Treasure hunting
self.weather_activities = WeatherActivitiesSystem
```

---

### `core/clock.py` - Time Management

**Class: `GameClock`**

Manages real-time and game-time, calculates offline progression.

| Method | Description |
|--------|-------------|
| `tick()` | Returns delta time since last tick (multiplied by time factor) |
| `tick_minutes()` | Converts seconds to game minutes |
| `hours_since(iso_timestamp)` | Calculates offline hours (capped at MAX_OFFLINE_HOURS) |
| `format_offline_time(hours)` | Human-readable format ("3 hours, 15 min") |
| `get_time_of_day()` | Returns "morning", "afternoon", "evening", "night" |
| `set_time_factor(factor)` | Adjusts time speed |

**Global Instance:** `game_clock`

---

### `core/persistence.py` - Save/Load System

**Class: `SaveManager`**

| Method | Description |
|--------|-------------|
| `save(data)` | Atomic save (temp file → rename) |
| `load()` | Load game state dictionary |
| `exists()` | Check if save file exists |
| `delete()` | Remove save file |
| `get_save_info()` | Get metadata (name, stage, days alive) |

**Helper:** `create_default_save_data()` - Creates fresh save structure

**Global Instance:** `save_manager`

---

### `core/progression.py` - XP, Levels & Streaks

**Class: `ProgressionSystem`**

| Method | Description |
|--------|-------------|
| `add_xp(amount, source)` | Adds XP with streak multiplier, handles level-ups |
| `get_streak_multiplier()` | Returns XP multiplier based on streak (up to 3x) |
| `process_daily_login()` | Updates streak, returns rewards & special messages |
| `claim_daily_reward()` | Claims daily reward pack |
| `track_milestone(milestone_type)` | Tracks interactions for milestones |
| `generate_daily_challenges()` | Creates 3 random daily challenges |
| `update_challenge_progress()` | Updates progress on active challenges |
| `get_random_collectible()` | Rolls for random collectible (weighted by rarity) |
| `variable_ratio_reward()` | Variable-ratio reinforcement random rewards |

**Data Managed:**
- `level`, `xp`, `total_xp` - Player progression
- `streak_days`, `last_login` - Login streak
- `collectibles` - Dict of category → item_id → owned
- `milestones` - Progress on interactions/days/streak
- `challenges` - Active daily/weekly challenges

**Global Instance:** `progression_system`

---

### `core/prestige.py` - Legacy/Rebirth System

**Class: `PrestigeSystem`**

| Method | Description |
|--------|-------------|
| `can_prestige()` | Checks requirements (min level 20, min 7 days) |
| `perform_prestige()` | Performs prestige, calculates legacy points |
| `check_new_unlocks()` | Checks for newly unlocked bonuses |
| `get_legacy_multipliers()` | Computes XP/coin/growth multipliers |
| `get_current_tier()` | Returns current PrestigeTier |
| `get_active_bonuses()` | Returns list of active LegacyBonus objects |
| `spend_legacy_points(amount)` | Deducts legacy points for purchases |

**Tiers:** NOVICE → APPRENTICE → JOURNEYMAN → EXPERT → MASTER → GRANDMASTER → LEGENDARY

**Global Instance:** `prestige_system`

---

### `core/save_slots.py` - Multi-Slot Saves

**Class: `SaveSlotsSystem`**

| Method | Description |
|--------|-------------|
| `refresh_slots()` | Scans all slots and parses save data |
| `load_slot(slot_id)` | Loads save data from a slot |
| `save_to_slot(slot_id, data)` | Saves data with automatic backup |
| `delete_slot(slot_id)` | Deletes slot and its backup |
| `copy_slot(from_id, to_id)` | Copies save between slots |
| `restore_from_backup(slot_id)` | Restores from backup |
| `export_save()` / `import_save()` | External file import/export |

**Global Instance:** `save_slots_system`

---

## Duck Modules

### `duck/duck.py` - Main Duck Entity

**Class: `Duck`** (dataclass)

The central pet entity.

| Field | Type | Description |
|-------|------|-------------|
| `name` | str | Duck's name |
| `personality` | Personality | Personality traits |
| `needs` | Needs | Hunger, energy, fun, cleanliness, social |
| `growth_stage` | GrowthStage | Current life stage |
| `growth_progress` | float | Progress to next stage |
| `created_at` | str | ISO timestamp of creation |
| `current_activity` | str | Current action |
| `memory` | DuckMemory | Conversation memory |

| Method | Description |
|--------|-------------|
| `create_new(name)` | Factory method with randomized personality |
| `update(delta)` | Updates needs decay and growth progress |
| `get_mood()` | Returns current MoodInfo based on needs |
| `apply_interaction(action)` | Applies feed/play/clean/pet/sleep |
| `get_personality_trait(name)` | Gets trait value (-100 to +100) |
| `is_derpy()` / `is_clever()` | Personality checks |
| `get_age_days()` | Duck's age in days |
| `get_stage_name()` | Human-readable growth stage |

---

### `duck/needs.py` - Need Management

**Class: `Needs`** (dataclass)

| Field | Range | Description |
|-------|-------|-------------|
| `hunger` | 0-100 | Food level |
| `energy` | 0-100 | Rest level |
| `fun` | 0-100 | Entertainment level |
| `cleanliness` | 0-100 | Hygiene level |
| `social` | 0-100 | Social interaction level |

| Method | Description |
|--------|-------------|
| `decay(delta, personality)` | Decays needs over time with personality modifiers |
| `apply_effect(action, personality)` | Applies interaction effects |
| `critical_needs()` | Returns needs below critical threshold |
| `low_needs()` | Returns needs below low threshold |
| `most_urgent()` | Most urgent need requiring attention |

---

### `duck/mood.py` - Mood System

**Enum: `MoodState`**
```
ECSTATIC > HAPPY > CONTENT > GRUMPY > SAD > MISERABLE
```

**Class: `MoodCalculator`**

| Method | Description |
|--------|-------------|
| `calculate_score(needs)` | Weighted sum of needs → mood score (0-100) |
| `get_state(score)` | Maps score to MoodState enum |
| `get_mood_info(needs)` | Complete MoodInfo with history tracking |
| `get_trend()` | Returns "improving", "declining", or "stable" |
| `get_expression()` | Random ASCII expression for mood |
| `get_mood_bar()` | ASCII visual mood bar |

**Global Instance:** `mood_calculator`

---

### `duck/behavior_ai.py` - Autonomous Behaviors

**Enum: `DuckAction`**
```
IDLE, WADDLE, QUACK, PREEN, NAP, LOOK_AROUND, SPLASH, STARE_BLANKLY,
CHASE_BUG, FLAP_WINGS, WIGGLE, TRIP, NAP_IN_NEST, HIDE_IN_SHELTER, etc.
```

**Class: `BehaviorAI`**

Utility-based AI for autonomous duck behaviors.

| Method | Description |
|--------|-------------|
| `set_context(structures, weather, location)` | Sets context for decisions |
| `should_act()` | Check if it's time for new action |
| `choose_action(needs, personality, mood)` | Utility scoring to pick best action |
| `execute_action(action)` | Execute action, apply effects |
| `score_actions()` | Score all actions based on needs, personality, mood, weather |

**Action Properties:**
- Base utility score
- Need bonuses (e.g., NAP gets bonus when energy low)
- Personality bonuses (e.g., derpy ducks more likely to TRIP)
- Duration and effects

---

### `duck/personality.py` - Personality Traits

**Class: `Personality`**

Five core traits, each ranging from -100 to +100:

| Trait | Low ↔ High |
|-------|------------|
| `clever_derpy` | Derpy ↔ Clever |
| `brave_timid` | Timid ↔ Brave |
| `active_lazy` | Lazy ↔ Active |
| `social_shy` | Shy ↔ Social |
| `neat_messy` | Messy ↔ Neat |

| Method | Description |
|--------|-------------|
| `create_random()` | Factory with random traits (bias toward derpy) |
| `get_trait(name)` | Get trait value |
| `get_dominant_traits()` | Most pronounced traits |
| `get_description()` | Human-readable description |
| `get_quirk()` | Random personality-based quirk message |

---

### `duck/aging.py` - Growth Stages

**Enum: `GrowthStage`**
```
EGG → HATCHLING → DUCKLING → JUVENILE → YOUNG_ADULT → ADULT → MATURE → ELDER → LEGENDARY
```

**Data: `GROWTH_STAGE_INFO`**

Each stage defines:
- Duration (min/max days)
- Size multipliers
- Stat modifiers (hunger_rate, energy_rate, xp_gain)
- Feature unlocks
- Stage-specific ASCII art
- Special abilities

---

### `duck/cosmetics.py` - Visual Cosmetics

**Class: `CosmeticsRenderer`**

Renders duck with equipped cosmetics in the playfield.

**Data: `COSMETIC_ART`**

Mini cosmetics for playfield duck:
- Hats (hat_red, hat_blue, hat_party, hat_chef, hat_wizard, hat_crown)
- Position info (above, y_offset, x_offset)
- Color functions for each element

---

### `duck/outfits.py` - Equippable Items

**Enum: `OutfitSlot`**
```
HAT, FACE, NECK, BODY, WINGS, FEET, HELD, SPECIAL
```

**Data: `OUTFIT_ITEMS`**

200+ outfit items including:
- Hats (santa_hat, witch_hat, bunny_ears, sun_hat)
- Face accessories (sunglasses, monocle, heart_glasses)
- Neck accessories (bowtie, scarf, pearl_necklace)
- Body, wings, feet, held items

---

## UI Modules

### `ui/renderer.py` - Main Renderer

**Class: `Renderer`** (1960+ lines)

The main UI renderer using the `blessed` terminal library.

#### Layout Structure
```
┌────────────────────────────────────────────────────────┐
│                    HEADER BAR                          │
│  Name | Season Weather | Time | Mood Age $Currency     │
├──────────────────────────────┬─────────────────────────┤
│                              │                         │
│        PLAYFIELD             │      SIDE PANEL         │
│   (Duck, items, weather)     │  (Closeup, stats,       │
│                              │   shortcuts)            │
│                              │                         │
├──────────────────────────────┴─────────────────────────┤
│                    MESSAGE AREA                        │
├────────────────────────────────────────────────────────┤
│                    CONTROLS BAR                        │
└────────────────────────────────────────────────────────┘
```

#### Season Display (Header)
The header bar shows the current season alongside weather:
- **Spring** (`~*~`): March, April, May
- **Summer** (`-*-`): June, July, August  
- **Fall** (`{~}`): September, October, November
- **Winter** (`*.*`): December, January, February

| Method | Description |
|--------|-------------|
| `render_frame(game)` | Main render loop - builds complete frame |
| `_render_header_bar()` | Top header with name, season, weather, time, mood |
| `_render_playfield()` | Main duck play area with decorations |
| `_render_side_panel()` | Stats/closeup panel on the right |
| `_render_messages()` | Message queue area |
| `_render_controls_bar()` | Bottom controls hints |
| `_overlay_help/stats/talk/inventory/shop()` | Modal overlay renderers |
| `_generate_ground_pattern()` | Location-specific ground patterns |
| `_update_weather_particles()` | Animates weather effects |
| `queue_message()` | Queues messages for display |
| `show_celebration()` | Triggers celebration overlay |

**Helper Classes:**
- `DuckPosition` - Tracks duck position and wandering behavior

---

### `ui/ascii_art.py` - Duck Art

**Data Structures:**
- `DUCK_ART` - Dict of duck ASCII art by growth stage and emotion
- `EMOTION_CLOSEUPS` - Detailed face closeups
- `BORDER` - Box drawing character set
- `PLAYFIELD_OBJECTS` - Small decorative objects
- `COSMETIC_OVERLAYS` - Art overlays for equipped items

| Function | Description |
|----------|-------------|
| `get_duck_art(stage, emotion)` | Returns appropriate duck art |
| `get_emotion_closeup(mood, action)` | Returns detailed face closeup |
| `create_box(content, title)` | Creates bordered box |
| `get_mini_duck()` | Returns small duck for playfield |

---

### `ui/animations.py` - Animation System

**Class: `AnimationController`**

| Method | Description |
|--------|-------------|
| `play(animation)` | Starts playing an animation |
| `show_effect(effect_name)` | Shows overlay effect |
| `update(delta)` | Updates animation state |
| `spawn_particles()` | Spawns ambient particles |
| `get_particles()` | Returns current particle list |
| `get_effect_overlay()` | Returns current effect overlay art |
| `get_breathing_offset()` | Returns breathing/idle motion offset |

**Effects:**
- Hearts, sparkles, zzz, music notes, stars, flowers

**Global Instance:** `animation_controller`

---

### `ui/location_art.py` - Location Backgrounds

**Data:**
- `LOCATION_GROUND_CHARS` - Ground tile characters by location
- `LOCATION_DECORATIONS` - Weighted decorations by location
- `LOCATION_SCENERY` - Large multi-line scenery pieces

**Locations (15+):**
- Home Pond, Deep End
- Forest Edge, Ancient Oak, Mushroom Grove
- Sunny Meadow, Butterfly Garden
- Pebble Beach, Waterfall
- Vegetable Patch, Tool Shed
- Foothills, Crystal Cave
- Sandy Shore, Shipwreck Cove

| Function | Description |
|----------|-------------|
| `generate_location_ground()` | Generates ground pattern grid |
| `generate_location_decorations()` | Returns decoration positions |
| `generate_location_scenery()` | Returns large scenery placements |
| `get_decoration_color()` | Returns blessed color for character |
| `get_ground_color()` | Returns ground character color |

---

### `ui/input_handler.py` - Input Processing

**Enum: `GameAction`**

All possible input actions mapped from keyboard.

| Function | Description |
|----------|-------------|
| `get_help_text()` | Returns formatted help string |
| `get_action_name(action)` | Returns display name for action |

**Class: `InputHandler`**

| Method | Description |
|--------|-------------|
| `register_action(action, callback)` | Registers action callback |
| `process_key(key)` | Processes key press, returns GameAction |
| `handle_text_input(key)` | Handles text entry mode |
| `start_text_mode()` | Switches to text mode |
| `get_text()` | Returns current text input |
| `is_text_mode()` | Checks if in text entry mode |

---

### `ui/day_night.py` - Time Cycle Visuals

**Enum: `TimePhase`**
```
DAWN → EARLY_MORNING → MORNING → MIDDAY → AFTERNOON → EVENING → NIGHT → LATE_NIGHT
```

**Class: `DayNightSystem`**

| Method | Description |
|--------|-------------|
| `get_current_time()` | Returns current time (real or game) |
| `get_time_of_day()` | Returns current TimeOfDay enum |
| `get_current_phase()` | Returns current TimePhase details |
| `get_moon_phase()` | Calculates current moon phase |
| `get_sky_art()` | Returns ASCII sky representation |

---

### `ui/mood_visuals.py` - Mood Visual Effects

**Enum: `MoodVisual`**
```
ECSTATIC, JOYFUL, HAPPY, CONTENT, NEUTRAL, PENSIVE, SAD, DEPRESSED, ANXIOUS, EXCITED, SLEEPY, HUNGRY
```

**Class: `MoodVisualEffects`**

| Method | Description |
|--------|-------------|
| `set_mood(mood)` | Sets current mood with transition |
| `update(delta)` | Updates effects state |
| `get_current_theme()` | Returns current MoodVisualTheme |
| `get_floating_decorations()` | Generates floating decorations |
| `generate_background()` | Generates mood-based background |

---

## World Modules

### `world/shop.py` - In-Game Shop

**Class: `ShopItem`** (dataclass)

| Field | Description |
|-------|-------------|
| `id` | Unique identifier |
| `name` | Display name |
| `description` | Item description |
| `price` | Cost in coins |
| `category` | ItemCategory enum |
| `rarity` | ItemRarity enum |
| `level_required` | Minimum level to purchase |
| `ascii_art` | Visual representation |
| `duck_dialogue` | Duck's reaction when bought |

**Categories:** COSMETIC, TOY, FURNITURE, WATER, PLANT, STRUCTURE, DECORATION, LIGHTING, FLOORING, SPECIAL

**Functions:**
| Function | Description |
|----------|-------------|
| `register_item(item)` | Register new shop item |
| `get_item(item_id)` | Retrieve item by ID |
| `get_items_by_category(category)` | Get all items in category |

**Data:** 255 purchasable items

---

### `world/habitat.py` - Habitat Management

**Class: `Habitat`**

| Method | Description |
|--------|-------------|
| `buy_item(item_id, inventory)` | Purchase from shop |
| `place_item(item_id, x, y)` | Grid-based placement |
| `equip_cosmetic(item_id)` | Equip duck cosmetic |
| `animate_item_bounce()` | Bounce animation |
| `animate_item_shake()` | Shake animation |
| `get_placed_items()` | Returns all placed items |
| `get_equipped_cosmetics()` | Returns equipped cosmetics list |

---

### `world/atmosphere.py` - Weather & Seasons

**Enum: `WeatherType`** (47 types organized by category)
```
# Common (all seasons)
SUNNY, PARTLY_CLOUDY, CLOUDY, OVERCAST, WINDY, FOGGY, MISTY

# Rain variants
DRIZZLE, RAINY, HEAVY_RAIN, STORMY, THUNDERSTORM

# Snow/ice variants
FROST, LIGHT_SNOW, SNOWY, HEAVY_SNOW, BLIZZARD, SLEET, HAIL, ICE_STORM

# Spring specific
SPRING_SHOWERS, RAINBOW, POLLEN_DRIFT, WARM_BREEZE, DEWY_MORNING

# Summer specific
SCORCHING, HUMID, HEAT_WAVE, SUMMER_STORM, BALMY_EVENING, GOLDEN_HOUR, MUGGY

# Fall specific
CRISP, BREEZY, LEAF_STORM, HARVEST_MOON, FIRST_FROST, AUTUMNAL

# Winter specific
BITTER_COLD, FREEZING, CLEAR_COLD, SNOW_FLURRIES, WINTER_SUN

# Rare/special
AURORA, METEOR_SHOWER, DOUBLE_RAINBOW, PERFECT_DAY
```

**WEATHER_DATA dictionary fields:**
| Field | Description |
|-------|-------------|
| `name` | Display name |
| `message` | Duck announcement message |
| `mood_modifier` | Effect on duck mood (-8 to +25) |
| `xp_multiplier` | XP bonus (1.0 to 3.0) |
| `particle_type` | Renderer particle key (e.g., "rain", "snow", "aurora") |
| `env_effects` | List of environmental effects (puddles, snow_piles, etc.) |
| `spring/summer/fall/winter_prob` | Per-season probability |
| `triggers_rainbow` | Can trigger rainbow after ending |
| `special` | Is rare/special weather |

**Environmental Effects:**
- Puddles, snow piles, leaf piles rendered on playfield
- Frost crystals, icicles, dew drops for atmosphere
- Swaying vegetation for wind effects

**Enum: `Season`**
```
SPRING, SUMMER, FALL, WINTER
```

**Class: `AtmosphereManager`**

| Method | Description |
|--------|-------------|
| `update()` | Updates weather/season, returns change messages |
| `_generate_weather()` | Selects weather based on season probabilities |
| `_maybe_rainbow()` | 20% chance of rainbow after rain, 5% double rainbow |
| `_calculate_season()` | Month-based season determination |
| `get_mood_modifier()` | Weather effect on mood |
| `get_xp_modifier()` | Weather effect on XP gain |

---

### `world/events.py` - Random Events

**Enum: `EventType`**
```
RANDOM, SCHEDULED, TRIGGERED, WEATHER, VISITOR, SPECIAL_DAY
```

**Class: `EventSystem`**

| Method | Description |
|--------|-------------|
| `update(delta)` | Checks for event triggers |
| `trigger_random_event()` | Triggers a random event |
| `get_active_event()` | Returns currently active event |
| `get_event_reactions(personality)` | Personality-based reactions |

**Events:** 20+ including found crumb, butterfly, loud noise, weather changes, visitors

---

### `world/exploration.py` - Biome Exploration

**Enum: `Biome`**
```
POND, FOREST, MEADOW, RIVERSIDE, GARDEN, MOUNTAINS, BEACH
```

**Class: `ExplorationSystem`**

| Method | Description |
|--------|-------------|
| `explore_area(area_id)` | Explore an area |
| `gather_resource(area_id, resource)` | Collect resources |
| `check_resource_regen()` | Check resource regeneration |
| `get_available_areas()` | Areas unlocked by level |
| `get_discovery_chance(area)` | Rare discovery probability |

---

### `world/fishing.py` - Fishing System

**Enum: `FishRarity`**
```
COMMON, UNCOMMON, RARE, EPIC, LEGENDARY, MYTHICAL
```

**Enum: `FishingSpot`**
```
POND, RIVER, LAKE, OCEAN, SECRET_COVE
```

**Class: `FishingSystem`**

| Method | Description |
|--------|-------------|
| `cast_line(spot, bait)` | Start fishing |
| `reel_in()` | Attempt to catch |
| `get_catch_probability()` | Probability based on conditions |
| `get_fish_collection()` | All caught fish |
| `get_records()` | Biggest fish records |

---

### `world/garden.py` - Gardening System

**Enum: `PlantType`**
```
FLOWER, VEGETABLE, FRUIT, HERB, SPECIAL
```

**Enum: `GrowthState`**
```
SEED, SPROUT, GROWING, MATURE, FLOWERING, HARVESTABLE, WITHERED
```

**Class: `Garden`**

| Method | Description |
|--------|-------------|
| `plant(species, plot)` | Plant a seed |
| `water(plot)` | Water a plant |
| `harvest(plot)` | Harvest mature plant |
| `check_growth()` | Update plant growth |
| `get_plants()` | All active plants |

---

### `world/building.py` - Construction System

**Enum: `StructureType`**
```
NEST, HOUSE, WORKSHOP, GARDEN, POND, DECORATION, STORAGE, WATCHTOWER
```

**Class: `BuildingSystem`**

| Method | Description |
|--------|-------------|
| `start_building(blueprint)` | Begin construction |
| `add_materials(structure, materials)` | Add building materials |
| `get_progress(structure)` | Returns 0.0-1.0 completion |
| `take_damage(structure, amount)` | Weather/predator damage |
| `repair(structure)` | Repair damaged structure |
| `get_structure_benefits()` | Active structure bonuses |

---

### `world/crafting.py` - Crafting System

**Class: `CraftingSystem`**

| Method | Description |
|--------|-------------|
| `can_craft(recipe)` | Check materials, skill, level, tool requirements |
| `craft(recipe)` | Perform crafting |
| `get_available_recipes()` | Recipes player can craft |
| `get_skill_level()` | Current crafting skill |

**Recipes:** 20+ including woven grass, rope, thatch, bricks, tools

---

### `world/materials.py` - Resource System

**Enum: `MaterialCategory`**
```
PLANT, WOOD, STONE, EARTH, WATER, FIBER, FOOD, RARE, CRAFTED
```

**Class: `MaterialInventory`**

| Method | Description |
|--------|-------------|
| `add(material, amount)` | Add with stacking |
| `remove(material, amount)` | Remove from stacks |
| `count(material)` | Get material count |
| `has(material, amount)` | Check if has enough |

**Data:** 60+ materials (leaves, twigs, shells, crystals, crafted items)

---

### `world/quests.py` - Quest System

**Class: `Quest`** (dataclass)

Multi-step narrative quests with:
- Steps with dialogue and objectives
- Branching choices
- Prerequisites
- Rewards (XP, coins, items, titles)

**Class: `QuestSystem`**

| Method | Description |
|--------|-------------|
| `start_quest(quest_id)` | Begin a quest |
| `update_progress(objective_type, amount)` | Progress objectives |
| `complete_step()` | Complete current step |
| `get_active_quests()` | Currently active quests |
| `get_available_quests()` | Quests player can start |

---

### `world/minigames.py` - Minigames

**Enum: `MinigameType`**
```
BREAD_CATCH, BUG_CHASE, MEMORY_MATCH, DUCK_RACE
```

**Class: `BreadCatchGame`**

Catch falling bread minigame with:
- Falling bread items
- Player paddle movement
- Score and lives
- ASCII rendering

**Class: `BugChaseGame`**

Quick reaction bug catching with:
- Random bug spawning
- Timed catches
- Combo multipliers

---

### `world/friends.py` - Social System

**Enum: `FriendshipLevel`**
```
STRANGER → ACQUAINTANCE → FRIEND → CLOSE_FRIEND → BEST_FRIEND
```

**Enum: `FriendPersonality`**
```
ADVENTUROUS, SCHOLARLY, ARTISTIC, PLAYFUL, MYSTERIOUS, GENEROUS, FOODIE, ATHLETIC
```

**Class: `FriendsSystem`**

| Method | Description |
|--------|-------------|
| `check_visitor()` | Check for random visitor |
| `interact_with_friend(friend_id)` | Social interaction |
| `give_gift(friend_id, item)` | Gift giving |
| `get_friendship_level(friend_id)` | Current friendship |
| `get_visitor_art(personality)` | ASCII art for visitor |

---

### `world/trading.py` - NPC Trading

**Enum: `TraderType`**
```
TRAVELING_MERCHANT, COLLECTOR, RARE_DEALER, FOOD_VENDOR, SEASONAL, MYSTERY
```

**Class: `TradingSystem`**

| Method | Description |
|--------|-------------|
| `check_trader_visit()` | Check for trader arrival |
| `get_current_trader()` | Active trader NPC |
| `get_available_trades()` | Current trade offers |
| `execute_trade(trade_id)` | Perform trade |
| `get_trader_friendship()` | Trader relationship |

---

### `world/secrets.py` - Easter Eggs

**Enum: `SecretType`**
```
EASTER_EGG, HIDDEN_ITEM, SECRET_AREA, SPECIAL_EVENT, HIDDEN_COMMAND, SECRET_COMBINATION, RARE_ENCOUNTER
```

**Class: `SecretsSystem`**

| Method | Description |
|--------|-------------|
| `check_sequence(key)` | Check for secret key sequences |
| `discover_secret(secret_id)` | Discover a secret |
| `get_discovered_secrets()` | All found secrets |
| `get_hint(secret_id)` | Get hint for secret |

**Secrets:** Konami code, duck song, midnight quacker, golden duck, dev room

---

### `world/achievements.py` - Achievement System

**Data: `ACHIEVEMENTS`**

40+ achievements across categories:
- **Interaction:** Feed/play/pet milestones
- **Growth:** Stage progressions
- **Time:** Playtime milestones
- **Secret:** Hidden achievements
- **Exploration:** Area discoveries
- **Crafting:** Items crafted
- **Building:** Structures built

---

## Dialogue Modules

### `dialogue/conversation.py` - Main Chat System

**Class: `ConversationSystem`**

"Edgy GameCube Animal Crossing" style - snarky, direct dialogue.

| Method | Description |
|--------|-------------|
| `get_greeting(mood)` | Mood-based greeting |
| `get_interaction_response(action, needs)` | Feed/play/clean/pet responses |
| `get_idle_dialogue(personality)` | Personality-based idle chat |
| `get_growth_reaction(stage)` | Growth stage reactions |
| `get_event_reaction(event_type)` | Event reactions |
| `process_player_message(text)` | Process text input (uses LLM if available) |
| `add_to_history(message)` | Track conversation history |

**Global Instance:** `conversation_system`

---

### `dialogue/llm_chat.py` - LLM Integration

**Class: `LLMChat`**

Local LLM integration using GGUF models.

| Method | Description |
|--------|-------------|
| `is_available()` | Check if LLM backend available |
| `get_model_name()` | Current model with [Local]/[Ollama] prefix |
| `generate_response(prompt, personality)` | Generate LLM response |
| `build_system_prompt(personality)` | Build personality-aware prompt |
| `_generate_local()` | Generate via local GGUF model |
| `_generate_ollama()` | Generate via Ollama HTTP API |

**Supported Models:**
- Local: TinyLlama GGUF (bundled)
- Ollama: llama3.2, llama3.1, mistral, phi3, gemma2, qwen2

---

### `dialogue/memory.py` - Memory System

**Class: `DuckMemory`**

Duck remembers interactions and events.

| Method | Description |
|--------|-------------|
| `remember_interaction(type, content)` | Record interaction (short-term) |
| `remember_event(type, content)` | Record significant event |
| `remember_milestone(milestone)` | Record milestone (always long-term) |
| `update_affinity(category, item)` | Update food/toy/activity preference |
| `get_favorite(category)` | Get duck's favorite thing |
| `get_mood_trend()` | improving/declining/stable/consistent |
| `get_relationship()` | stranger/acquaintance/friend/best_friend/bonded |
| `recall_memory()` | Random memory weighted by importance |

---

### `dialogue/diary.py` - Life Journal

**Class: `DuckDiary`**

Sims-style life journal tracking events.

| Method | Description |
|--------|-------------|
| `add_entry(entry)` | Add new diary entry |
| `record_milestone(milestone, details)` | Record growth/achievement |
| `record_relationship_event(event)` | Record relationship changes |
| `record_weather_event(weather, details)` | Record weather events |
| `record_discovery(item)` | Record found items |
| `record_visitor(visitor_name)` | Record visitor interactions |
| `add_relationship_xp(amount)` | Increase relationship score |
| `get_relationship_level()` | Current relationship status |

**Relationship Levels:** Strangers → Soul Bonded (7 levels)

**Global Instance:** `duck_diary`

---

### `dialogue/diary_enhanced.py` - Enhanced Diary

**Class: `EnhancedDiary`**

Extended diary with emotional tracking, photos, dreams.

| Method | Description |
|--------|-------------|
| `log_emotion(emotion, intensity, trigger)` | Log emotional moment |
| `analyze_emotions(period)` | Analyze emotions over period |
| `take_photo(photo_type, subject)` | Take ASCII diary photo |
| `get_writing_prompt()` | Get writing prompt |
| `answer_prompt(prompt_id, response)` | Answer a prompt |
| `start_chapter(title)` | Start new life chapter |
| `record_dream(dream_text)` | Record dream with symbol detection |
| `get_daily_mood_summary()` | Daily mood summary |
| `render_emotion_wheel()` | ASCII emotion wheel |
| `render_photo_album()` | Photo album page |
| `render_dream_journal()` | Dream journal display |

**Global Instance:** `enhanced_diary`

---

### `dialogue/mood_dialogue.py` - Context Dialogue

**Class: `MoodDialogueSystem`**

Context-aware dialogue based on mood.

| Method | Description |
|--------|-------------|
| `get_dialogue(mood, context)` | Get dialogue for mood/context |
| `get_reaction(event)` | Reaction to specific event |
| `format_dialogue(dialogue)` | Format with emote |
| `render_speech_bubble(text)` | Render speech bubble |

**Contexts:** GREETING, FEEDING, PETTING, PLAYING, TALKING, SLEEPING, IDLE, ACHIEVEMENT, LEVEL_UP, GIFT, WEATHER, FAREWELL

**Global Instance:** `mood_dialogue_system`

---

## Audio Modules

### `audio/sound.py` - Core Audio Engine

**Class: `SoundEngine`**

Core sound playback engine with multiple backends.

| Method | Description |
|--------|-------------|
| `play_music(filepath)` | Play background music on loop |
| `stop_music()` | Stop background music |
| `toggle_music_mute()` | Toggle music mute |
| `set_music_volume(volume)` | Set music volume (0.0-1.0) |
| `play_wav(filepath)` | Play WAV file |
| `play_tone(frequency, duration)` | Play single tone |
| `play_effect(sound_type)` | Play sound effect |
| `play_melody(name)` | Play named melody |
| `toggle_sound()` | Toggle sound on/off |
| `set_volume(volume)` | Set volume |
| `volume_up()` / `volume_down()` | Adjust volume |
| `get_volume_bar()` | Volume bar visualization |

**Playback Methods (auto-detected):**
1. WAV files via pygame/aplay/paplay
2. Terminal bell for beeps
3. Beep command for frequency control
4. Silent fallback

**Class: `DuckSounds`**

Duck-specific sound effects.

| Method | Description |
|--------|-------------|
| `quack(mood)` | Play quack based on mood |
| `quack_speak(text)` | Quacks for each syllable |
| `eat()` / `splash()` / `pet()` / `play()` / `sleep()` / `wake()` | Specific sounds |
| `level_up()` | Level up fanfare |
| `notification()` / `achievement()` | Notification sounds |
| `random_quack()` | Random quack variation |

**Global Instances:** `sound_engine`, `duck_sounds`

---

### `audio/ambient.py` - Environmental Audio

**Class: `AmbientSoundSystem`**

Environmental ambient sounds (text-based for terminal).

| Method | Description |
|--------|-------------|
| `set_enabled(enabled)` | Enable/disable ambient sounds |
| `set_master_volume(volume)` | Set master volume |
| `update_active_sounds(weather, time, location)` | Update based on context |
| `get_visualization()` | ASCII visualization of sounds |
| `get_current_mood()` | Overall mood from active sounds |
| `render_settings()` | Settings screen |

**Predefined Sounds:**
- Weather: light_rain, heavy_rain, thunder, wind, snow_falling
- Time: morning_birds, afternoon_buzz, evening_crickets, night_silence
- Location: pond_water, forest_rustle, home_cozy
- Seasonal: spring_bloom, summer_heat, autumn_leaves, winter_chill
- Special: festival_music, sleeping_duck

**Global Instance:** `ambient_system`

---

### `audio/sound_effects.py` - Text Sound Effects

**Data: `SOUND_EFFECTS`**

Text-based sound representations for terminal output.

**Categories:**
- Duck Voice: quack, happy_quack, sad_quack, excited_quack, etc.
- Duck Movement: waddle, splash, flap, hop, slide, plop
- Duck Action: eat, drink, preen, shake, nap_start, snoring
- Environment: rain, thunder, wind, birds_chirping
- UI: menu_open, select, confirm, error, coins, level_up

---

## Data Flow

### Game Loop Flow
```
main.py
    └── Game.start()
        └── Game._game_loop() [30 FPS]
            ├── Input: _handle_action(key)
            │   ├── Check overlays (help, stats, inventory, shop, talk)
            │   ├── Route to appropriate handler
            │   └── Process action (feed, play, clean, pet, sleep)
            │
            ├── Update: _update(delta)
            │   ├── Duck.update(delta)  # Needs decay, growth
            │   ├── BehaviorAI.update() # Autonomous actions
            │   ├── Atmosphere.update() # Weather changes
            │   ├── Events.update()     # Random events
            │   └── Progression.update() # XP/level checks
            │
            └── Render: _render()
                └── Renderer.render_frame(game)
                    ├── Header bar
                    ├── Playfield + Side panel
                    ├── Message area
                    ├── Controls bar
                    └── Overlays (if active)
```

### Save Data Flow
```
Game._save_game()
    ├── duck.to_dict()
    ├── habitat.to_dict()
    ├── progression_system.to_dict()
    ├── prestige_system.to_dict()
    ├── inventory.to_dict()
    ├── friends.to_dict()
    ├── atmosphere.to_dict()
    ├── material_inventory.to_dict()
    ├── fishing.to_dict()
    ├── garden.to_dict()
    ├── building.to_dict()
    ├── secrets.to_dict()
    ├── scrapbook.to_dict()
    ├── quests.to_dict()
    ├── trading.to_dict()
    ├── minigames.to_dict()
    ├── treasure.to_dict()
    ├── weather_activities.to_dict()
    ├── duck_diary.to_dict()
    ├── enhanced_diary.to_dict()
    ├── duck.memory.to_dict()
    └── save_manager.save(data)
```

---

## Save/Load System

### Save File Structure
```json
{
  "version": "1.0",
  "saved_at": "2024-01-01T12:00:00",
  "duck": {
    "name": "Cheese",
    "personality": {...},
    "needs": {...},
    "growth_stage": "adult",
    "growth_progress": 0.5,
    "created_at": "...",
    "current_activity": null
  },
  "habitat": {
    "placed_items": [...],
    "equipped_cosmetics": [...],
    "currency": 1000
  },
  "progression": {
    "level": 10,
    "xp": 500,
    "total_xp": 5000,
    "streak_days": 7,
    "last_login": "...",
    "collectibles": {...},
    "milestones": {...},
    "challenges": [...]
  },
  "prestige": {
    "prestige_count": 0,
    "legacy_points": 0,
    "unlocked_bonuses": [],
    "duck_history": []
  },
  // ... other systems
}
```

### Multi-Slot System
```
data/
├── saves/
│   ├── slot_1.json
│   ├── slot_1.json.backup
│   ├── slot_2.json
│   ├── slot_2.json.backup
│   └── ...
```

---

## Key Integration Points

### 1. Duck ↔ Game
- Game instantiates Duck and calls `update()` each frame
- Game processes interactions via `apply_interaction()`
- Game reads mood via `get_mood()` for UI and events

### 2. Duck ↔ Needs ↔ Mood
- `Needs.decay()` called each frame
- `MoodCalculator.get_mood_info(needs)` calculates mood
- Mood affects AI behavior, dialogue, visuals

### 3. Game ↔ Renderer
- Game calls `render_frame()` each frame
- Renderer reads all game state for display
- Renderer manages UI overlays and animations

### 4. Game ↔ Progression
- Actions call `add_xp()` and `track_milestone()`
- Daily login triggers `process_daily_login()`
- Level-ups trigger celebrations and unlocks

### 5. Game ↔ Atmosphere
- `update()` called each frame for weather changes
- Weather affects duck mood, XP gain, and available activities
- Seasons affect available items, events, and visuals

### 6. Dialogue ↔ LLM
- `ConversationSystem.process_player_message()` checks for LLM
- Falls back to template responses if unavailable
- Personality context passed to LLM for in-character responses

### 7. Memory ↔ Dialogue
- Memory tracks interactions for context
- Relationship level affects dialogue options
- Favorites influence random dialogue selection

### 8. Shop ↔ Habitat
- Shop defines purchasable items
- Habitat manages owned items and placement
- Currency tracked in Habitat

---

## Global Instances

These singleton instances are used throughout the codebase:

```python
# Core
from core.clock import game_clock
from core.persistence import save_manager
from core.progression import progression_system
from core.prestige import prestige_system
from core.save_slots import save_slots_system

# Duck
from duck.mood import mood_calculator

# UI
from ui.animations import animation_controller

# Dialogue
from dialogue.conversation import conversation_system
from dialogue.diary import duck_diary
from dialogue.diary_enhanced import enhanced_diary
from dialogue.mood_dialogue import mood_dialogue_system

# Audio
from audio.sound import sound_engine, duck_sounds
from audio.ambient import ambient_system
```

---

## Configuration (`config.py`)

Key configuration constants:

```python
# Time
TICK_RATE = 30  # FPS
MAX_OFFLINE_HOURS = 24  # Cap for offline progression

# Needs
NEED_DECAY_RATES = {...}  # Per-minute decay rates
NEED_MAX = 100
NEED_MIN = 0
NEED_CRITICAL = 20
NEED_LOW = 40
INTERACTION_EFFECTS = {...}  # Effect of each action

# Mood
MOOD_THRESHOLDS = {...}  # Score ranges for each mood
MOOD_WEIGHTS = {...}  # Weight of each need in mood calculation

# Personality
DEFAULT_PERSONALITY = {...}  # Default trait values

# Growth
GROWTH_STAGES = {...}  # Stage durations and properties

# Colors
COLORS = {...}  # Terminal color definitions

# Paths
SAVE_FILE = "data/save.json"
MODELS_DIR = "models/"
```

---

## Quick Reference: Key Files by Feature

| Feature | Primary Files |
|---------|---------------|
| Game Loop | `core/game.py` |
| Duck State | `duck/duck.py`, `duck/needs.py`, `duck/mood.py` |
| Rendering | `ui/renderer.py`, `ui/ascii_art.py` |
| Input | `ui/input_handler.py`, `core/game.py` |
| Saving | `core/persistence.py`, `core/save_slots.py` |
| Progression | `core/progression.py`, `core/prestige.py` |
| Weather | `world/atmosphere.py`, `world/weather_activities.py` |
| Shop/Items | `world/shop.py`, `world/items.py`, `world/habitat.py` |
| Crafting | `world/crafting.py`, `world/materials.py` |
| Building | `world/building.py` |
| Fishing | `world/fishing.py` |
| Gardening | `world/garden.py` |
| Exploration | `world/exploration.py` |
| Quests | `world/quests.py`, `world/goals.py`, `world/challenges.py` |
| Social | `world/friends.py`, `world/trading.py` |
| Achievements | `world/achievements.py`, `world/secrets.py` |
| Dialogue | `dialogue/conversation.py`, `dialogue/llm_chat.py` |
| Audio | `audio/sound.py`, `audio/ambient.py` |

---

*Last updated: December 2024*
*Document generated for AI assistant reference*
