# Stupid Duck — Complete Game Systems Inventory

## What `_get_memory_context_for_dialogue()` Currently Sends to the LLM

Located in [core/game.py](core/game.py#L9793-L9968). Builds a `memory_context` string containing:

1. **Current location** — area name + description (default "Home Pond")
2. **Time of day** — hour from `day_night` system
3. **Season** — from `atmosphere`
4. **Weather** — `weather_type` from `atmosphere`
5. **Visiting friend** — name, personality, friendship level, times_visited, favorite_food, favorite_activity, gift_brought, activities_done, active conversation flag
6. **Known friends list** — up to 8 friends with personality + friendship level
7. **Duck mood** — current mood state string
8. **Favorites** — favorite food, toy, activity (from `duck.memory`)
9. **Active quests** — up to 5 quest names
10. **Recent event** — last event description
11. **Relationship level** — with the player (from memory)
12. **Recent memory** — from `duck.memory.recall_memory()`
13. **Mood trend** — from `duck.memory`
14. **Habitat items** — up to 10 placed item names

---

## 1. Duck Entity — `duck/duck.py`

**State tracked:**
- `name` (str) — duck name (default "Cheese")
- `created_at` (datetime) — birth timestamp
- `needs` (Needs) — hunger, energy, fun, cleanliness, social
- `personality` (Dict[str,int]) — 5 traits: clever_derpy, brave_timid, active_lazy, social_shy, neat_messy
- `growth_stage` (str) — current life stage
- `growth_progress` (float) — progress to next stage
- `current_action` (str) — what the duck is doing right now
- `action_start_time` (float) — when current action started
- `trust` (float, 0-100) — trust in player (consequences system)
- `is_sick` (bool), `sick_since` — sickness state
- `hiding` (bool), `hiding_coax_visits` (int) — hiding from player
- `cooldown_until` (float) — interaction cooldown
- `neglect_minutes_at_zero` (int) — neglect tracking
- `_mood_calculator` (MoodCalculator) — mood computation
- `_personality_system` (Personality) — personality trait system
- `_memory` (DuckMemory) — memory instance

**Actions/Methods:**
- `create_new()` — initialize a new duck
- `update()` — tick update for decay/stage progression
- `get_mood()` → MoodInfo — current mood info
- `get_personality_summary()` → str

**LLM-useful:** mood state, personality summary, growth stage, trust level, sickness, current action

---

## 2. Needs System — `duck/needs.py`

**State tracked:**
- 5 floats (0–100): `hunger`, `energy`, `fun`, `cleanliness`, `social`
- Decay rates per config (`NEED_DECAY_RATES`): hunger ~8hr, energy ~14hr, fun ~8hr, cleanliness ~21hr, social ~8hr
- Decay modifiers from personality, aging, sickness, weather, cascade

**Actions/Methods:**
- `update()` — apply decay over time
- `apply_interaction(interaction_type)` — apply effects from config `INTERACTION_EFFECTS`
- `get_critical_needs()` → List — needs below 20
- `get_low_needs()` → List — needs below 40
- `get_urgent_need()` → Optional[str] — single most urgent need

**Interaction effects (from config):**
- `feed` → hunger +18, fun +2
- `play` → fun +15, energy -5, social +5
- `clean` → cleanliness +20, fun -2
- `pet` → social +12, fun +5
- `sleep` → energy +25, hunger -3

**LLM-useful:** all 5 need levels, critical/low needs, which need is urgent

---

## 3. Mood System — `duck/mood.py`

**State tracked:**
- Current `MoodState`: ECSTATIC, HAPPY, CONTENT, GRUMPY, SAD, MISERABLE
- `MoodInfo`: state, score (float), description, can_play (bool), can_learn (bool)
- Mood history for trends

**Key rules:**
- SAD/MISERABLE → `can_play = False`, `can_learn = False`
- Mood score is weighted avg of needs (hunger 25%, energy 25%, fun 20%, cleanliness 15%, social 15%)
- Thresholds: ecstatic ≥90, happy ≥70, content ≥50, grumpy ≥30, sad ≥10, miserable <10

**LLM-useful:** mood state name, score, description, mood transition events, trend

---

## 4. Personality — `duck/personality.py`

**State tracked:**
- 5 trait axes (-100 to +100):
  - `clever_derpy` → affects dialogue_randomness, learning_speed, trip_chance
  - `brave_timid` → affects exploration_willingness
  - `active_lazy` → affects activity level
  - `social_shy` → affects visitor comfort
  - `neat_messy` → affects cleanliness decay

**Actions/Methods:**
- `get_trait(name)`, `set_trait(name, value)`, `adjust_trait(name, delta)`
- `get_effect(effect_name)` → float — personality-derived modifier
- `get_dominant_traits()` → List — strongest traits
- `get_personality_summary()` → str — human-readable summary

**LLM-useful:** dominant traits, personality summary string, specific trait values

---

## 5. Extended Personality — `duck/personality_extended.py`

**State tracked:**
- Additional trait axes beyond the base 5
- `QuirkType` enum — behavioral quirks (e.g., unique habits)
- `PreferenceType` enum — favorites vs dislikes
- Hidden traits (discoverable over time)

**Actions/Methods:**
- `generate_random()` — create random extended personality
- `adjust_trait()`, `check_quirk_trigger()`, `discover_preference()`
- `update_hidden_trait_progress()`, `age_personality()`
- `get_behavior_modifiers()` → modifiers for AI decisions

**LLM-useful:** active quirks, discovered preferences, hidden traits

---

## 6. Aging System — `duck/aging.py`

**State tracked:**
- `birth_date`, `current_stage`, `days_in_current_stage`
- `life_events` (List), `growth_milestones` (List)
- `birthday_celebrated` (bool), `aging_paused` (bool)
- Growth stages: HATCHLING → DUCKLING → JUVENILE → YOUNG_ADULT → ADULT → MATURE → ELDER → ANCIENT
- Stage durations: 3d, 11d, 16d, 60d, 275d, 365d, 365d, ∞

**Actions/Methods:**
- `get_age_days()`, `get_age_string()` — current age
- `update_stage()` — check for stage transitions
- `get_stat_modifier()` — age-based stat modifiers
- `is_birthday()`, `celebrate_birthday()`
- `add_life_event(event)`, `get_unlocked_features()`

**LLM-useful:** age string, growth stage, life events, birthday, unlocked features

---

## 7. Consequences & Trust — `core/consequences.py`

**State tracked:**
- `trust` (0–100), trust levels (stranger → soulmate)
- Sickness, hiding, cooldown, cold shoulder states
- Neglect tracking (minutes at zero needs)
- Cascade modifiers (low needs affect other needs)

**Actions/Methods:**
- `get_trust_level()` → str
- `check_consequences()` — evaluate state for penalties
- `apply_trust_gain()`, `apply_personality_drift()`
- `attempt_coax()` — try to bring duck out of hiding
- `apply_medicine()` — cure sickness
- `thaw_cold_shoulder()`, `is_cold_shoulder_active()`
- `get_cold_shoulder_greeting/idle/interaction()` — special dialogue when cold

**LLM-useful:** trust level, sickness status, cold shoulder state, hiding status

---

## 8. Duck Memory — `dialogue/memory.py`

**State tracked:**
- `interactions` — Dict[str, int] — counts of each interaction type
- `events` — List[Memory] — remembered events with importance + emotional value
- `milestones` — List[Memory] — significant achievements
- `long_term_memories` — List[Memory] — consolidated important memories
- `moods` — List[float] — recent mood scores for trending
- `food_affinity`, `toy_affinity`, `activity_affinity` — Dict[str, int] — preferences
- `relationship_points` (int) — cumulative relationship score

**Actions/Methods:**
- `add_interaction(type, details, emotional_value)`
- `add_event(name, details, importance, emotional_value)`
- `add_milestone(milestone, details)`
- `update_affinity(thing, delta)` — adjust preference for food/toy/activity
- `get_favorite(category)` → str — top-ranked food/toy/activity
- `get_recent_mood_trend()` → "improving" / "declining" / "stable"
- `get_relationship_level()` → "stranger" / "acquaintance" / "friend" / "best_friend" / "soulmate"
- `recall_memory()`, `recall_random_memory()` → Optional[str]

**LLM-useful:** favorites, relationship level, mood trend, recalled memories, interaction counts

---

## 9. Conversation System — `dialogue/conversation.py`

**State tracked:**
- Conversation history (player ↔ duck messages)
- LLM integration for generating responses

**Actions/Methods:**
- `get_greeting(duck)` → str
- `get_interaction_response(duck, interaction)` → str
- `get_idle_thought(duck)` → str
- `get_growth_reaction(duck, new_stage)` → str
- `get_event_reaction(duck, event_type)` → str
- `process_player_input(duck, player_input, use_llm, memory_context)` → str — main chat handler
- `add_to_history(player_msg, duck_response)`

**LLM-useful:** this IS the LLM interface; memory_context is passed through here

---

## 10. Conversation Memory — `dialogue/conversation_memory.py`

**State tracked:**
- `conversations` — List[Conversation] — full conversation logs
- `conversation_summaries` — List[ConversationSummary]
- `notable_quotes`, `learned_facts` — extracted from chats
- Topics: ConversationTopic enum (GREETING, FEELINGS, MEMORIES, PHILOSOPHY, FOOD, WEATHER, GAMES, STORIES, MUSIC, NATURE, FRIENDSHIP, SECRETS, DREAMS, ADVENTURES, DAILY_LIFE, HUMOR, LEARNING, OTHER)

**Actions/Methods:**
- `start_conversation(duck_mood)`, `end_conversation(duck_mood)`
- `add_message(role, content, ...)` — records & auto-detects topics, notable quotes, facts
- `get_recent_context(max_messages)` — for LLM context window
- `search_conversations(query)` — keyword search past conversations
- `get_random_callback()` — retrieve random past moment to reference
- `get_conversation_stats()`, `get_topic_summary()`

**LLM-useful:** recent context, topic distribution, notable quotes, learned facts, callbacks

---

## 11. Duck Brain — `dialogue/duck_brain.py`

**State tracked:**
- `thought_queue` — List[DuckThought] — pending thoughts to share
- `relationship_level` (float 0–1)
- `conversation_count`, `message_count`
- `pending_observations` — queued behavioral observations
- `cold_shoulder_active`, `duck_trust` — proxied from duck state

**Actions/Methods:**
- `start_session(time_since_last)`, `end_session()`
- `process_player_message(message, response, context)` → str
- `process_action(action, context)` → str — duck comments on its own actions
- `get_greeting(time_since_last)`, `get_farewell()`
- `get_idle_thought(duck_mood, ...)`, `get_observation(context)`
- `get_weather_forecast(atmosphere)` — duck predicts weather
- `get_callback()` — reference past conversation
- `get_question(relationship_level, ...)` — duck asks player questions
- `record_question_answer(question_id, answer)` — process player answers
- `build_llm_prompt(memory_context)`, `get_llm_context(max_messages)`

**LLM-useful:** this system drives proactive duck speech; relationship level, thought queue, observations

---

## 12. Player Model — `dialogue/player_model.py`

**State tracked:**
- `traits` — Dict[PlayerTraitAxis, float] — inferred player personality
  - Axes: CARING_NEGLECTFUL, PLAYFUL_SERIOUS, PATIENT_IMPATIENT, GENEROUS_STINGY, ADVENTUROUS_CAUTIOUS, CREATIVE_PRACTICAL, TALKATIVE_QUIET
- `statements` — List[PlayerStatement] — things the player has said
- `facts` — List[PlayerFact] — extracted facts about the player (name, job, pets, etc.)
- `visit_patterns` — VisitPattern (play times, session duration, frequency)
- `behavior_patterns` — BehaviorPattern (interaction preferences, favorite activities)
- `pending_questions` — List — questions the duck wants to ask

**Actions/Methods:**
- `start_session()`, `end_session()` — track visit patterns
- `record_action(action)` — infer traits from player choices
- `record_statement(text, context)` — store + extract facts
- `record_fact(type, value)` — explicit fact storage
- `get_relevant_facts(context)`, `get_relevant_statements(topic)`
- `get_behavioral_observations()` → List[str] — human-readable observations
- `get_trait_description(trait)` → describe player trait
- `get_pending_observation()` — duck notices player patterns

**LLM-useful:** player trait summary, known facts about player, visit patterns, behavioral observations

---

## 13. Ritual Tracker — `dialogue/ritual_tracker.py`

**State tracked:**
- `action_history` — Dict[str, List[ActionTimestamp]] — when player does actions
- `rituals` — Dict[str, RitualPattern] — detected daily routines
- `broken_rituals`, `new_rituals` — tracking changes

**Actions/Methods:**
- `record_interaction(action)` → Optional[str] — track action & return ritual comment
- `check_missed_rituals()` → List[str] — rituals the player is late on
- `get_ritual_summary()` → Dict — active rituals for display

**LLM-useful:** established rituals (e.g., "feeds me every morning at 8am"), missed rituals, new patterns

---

## 14. LLM Chat — `dialogue/llm_chat.py`

**State tracked:**
- Local GGUF model (Llama-3.2-3B-Instruct-Q4_K_M)
- `conversation_history` — message history for context
- GPU layer detection, model loading state

**Actions/Methods:**
- `generate_response(duck, player_input, memory_context)` — main chat generation
- `generate_action_commentary(duck, action, context)` — duck comments on actions
- `generate_visitor_dialogue(duck, visitor_name, visitor_personality, ...)` — visitor speech
- `_build_system_prompt(duck, context)` — constructs the LLM system prompt
- `clear_history()`

**Config:**
- `LLM_CONTEXT_SIZE = 1024`, `LLM_MAX_TOKENS = 80` (actions), `LLM_MAX_TOKENS_CHAT = 120` (chat)
- `LLM_TEMPERATURE = 0.75`, `LLM_ACTION_CHANCE = 0.7`, `LLM_VISITOR_CHANCE = 0.8`

---

## 15. LLM Behavior Controller — `dialogue/llm_behavior.py`

**State tracked:**
- Request queue (RequestType: ACTION_COMMENT, VISITOR_DIALOGUE, IDLE_THOUGHT, SPECIAL_EVENT)
- Response cache (100 entries, 5min TTL)
- Worker thread for background LLM generation

**Classes:**
- `ContextBuilder` — builds structured context for LLM prompts
- `LLMWorker` — background thread processing LLM requests
- `LLMBehaviorController` — orchestrates LLM usage across game

---

## 16. Contextual Dialogue — `dialogue/contextual_dialogue.py`

**State tracked:**
- `ContextComment` — weather/location/time-aware comments
- Large library of context-specific dialogue lines (~1335 lines of data)

**Actions/Methods:**
- `ContextualDialogueSystem` — generates comments based on current weather, season, time, location, mood combinations

**LLM-useful:** provides template-based dialogue when LLM isn't available

---

## 17. Question System — `dialogue/questions.py`

**State tracked:**
- `QuestionCategory`: PERSONAL, PREFERENCES, PHILOSOPHICAL, PLAYFUL, MEMORIES, CREATIVE, HYPOTHETICAL, EMOTIONAL, DAILY_LIFE, DEEP
- `QuestionTiming`: ANY, MORNING, AFTERNOON, EVENING, NIGHT, HIGH_TRUST, LOW_TRUST
- ~2258 lines of question data

**Actions/Methods:**
- `QuestionManager` — selects contextually appropriate questions for the duck to ask the player

---

## 18. Mood Dialogue — `dialogue/mood_dialogue.py`

**State tracked:**
- `MoodType` enum matching mood states
- `DialogueContext` enum (GREETING, IDLE, INTERACTION, EVENT, FAREWELL, etc.)
- ~808 lines of mood-specific dialogue lines

**Actions/Methods:**
- `MoodDialogueSystem` — provides mood-appropriate dialogue templates

---

## 19. Seaman-Style Dialogue — `dialogue/seaman_style.py`

**State tracked:**
- `DialogueTone` (SASSY, PHILOSOPHICAL, CURIOUS, EXCITED, GRUMPY, PLAYFUL, MYSTERIOUS, etc.)
- `DialogueContext` (GREETING, FAREWELL, IDLE, NEED, EVENT, ITEM, WEATHER, etc.)
- Inspired by Sega Dreamcast's "Seaman" game

**Actions/Methods:**
- `SeamanDialogue` — generates quirky, opinionated dialogue in the Seaman style

---

## 20. Visitor Dialogue — `dialogue/visitor_dialogue.py`

**State tracked:**
- `ConversationState` — active visitor conversation state
- `VisitorDialogueManager` — manages multi-turn visitor conversations

---

## 21. Guest Conversations — `dialogue/guest_conversations.py`

**State tracked:**
- `ConversationExchange` — individual exchange in a guest conversation
- `GuestConversation` — full guest conversation log

---

## 22. Diary Systems — `dialogue/diary.py` + `dialogue/diary_enhanced.py`

### Basic Diary (`DuckDiary`):
**State tracked:**
- `DiaryEntryType`: DAILY, EVENT, MILESTONE, MOOD, INTERACTION, DISCOVERY, MEMORY, DREAM, FESTIVAL, QUEST, FRIEND, SEASONAL
- Diary entries with timestamps, content, emotional tone

**Actions/Methods:**
- Auto-generates daily diary entries from game events
- Render diary pages

### Enhanced Diary (`EnhancedDiarySystem`):
**State tracked:**
- `EmotionCategory`, `DiaryPromptType`, `PhotoType` enums
- `EmotionLog` — hourly emotion tracking
- `DiaryPhoto` — snapshot moments
- `DiaryPrompt` — reflective prompts
- `LifeChapter` — grouping life phases
- `DreamLog` — dream journaling

---

## 23. DJ Duck Commentary — `dialogue/dj_duck.py`

**State tracked:**
- `DJDuckCommentary` — generates radio DJ-style commentary about game events and music

---

## 24. Personality Dialogue Modules

8 specialized dialogue files for personality-driven responses:
- `dialogue/dialogue_adventurous.py`
- `dialogue/dialogue_artistic.py`
- `dialogue/dialogue_athletic.py`
- `dialogue/dialogue_base.py`
- `dialogue/dialogue_foodie.py`
- `dialogue/dialogue_generous.py`
- `dialogue/dialogue_mysterious.py`
- `dialogue/dialogue_playful.py`
- `dialogue/dialogue_scholarly.py`

Each provides trait-specific responses for various `ConversationPhase` values.

---

## 25. Exploration System — `world/exploration.py`

**State tracked:**
- `BiomeType` enum — different biome types (pond, forest, meadow, etc.)
- `current_area` — where the duck currently is
- `discovered_areas` — Dict of unlocked BiomeAreas
- `gathering_skill` (int), `exploration_xp` (int)
- `total_resources_gathered`, `rare_items_found`

**Actions/Methods:**
- `travel_to(area)` — move to a different area
- `explore()` → ExplorationResult — explore current location
- `gather()` — gather resources from current area
- `get_available_areas()`, `get_location_dialogue()`
- `check_location_event()` — area-specific random events

**LLM-useful:** current area name/description, discovered areas, gathering skill level

---

## 26. Items & Inventory — `world/items.py`

**State tracked:**
- `ItemType` enum (FOOD, TOY, DECORATION, TOOL, MATERIAL, SPECIAL, KEY, COSMETIC, etc.)
- `Inventory` — list of Item objects, `max_size = 20`

**Actions/Methods:**
- `add_item()`, `remove_item()`, `use_item()`
- `get_items_by_type()`, `get_food_items()`, `get_toy_items()`

**LLM-useful:** what items the player has, item names/descriptions

---

## 27. Item Interactions — `world/item_interactions.py`

**State tracked:**
- `InteractionType` enum — types of item interactions
- ~4983 lines of item-specific interaction data with dialogue strings
- Growth-stage-specific interaction variants

**Actions/Methods:**
- `get_item_interaction(item_id)`, `get_interaction_commands(item_id)`
- `execute_interaction(item_id, duck_state)` → InteractionResult
- `find_matching_item(command, owned_items)`

---

## 28. Materials — `world/materials.py`

**State tracked:**
- `MaterialCategory` enum — categorized resources
- `MaterialInventory` — `max_slots = 50`, material stacks with quantities

**Actions/Methods:**
- `add_material(id, amount)`, `remove_material(id, amount)`
- `get_count(id)`, `has_materials(requirements)` — recipe checking
- `get_by_category(category)`, `get_total_value()`
- `get_slots_used()`, `get_slots_free()`

**LLM-useful:** total materials count, notable materials, slot usage

---

## 29. Habitat — `world/habitat.py`

**State tracked:**
- `owned_items`, `placed_items` (with animations), `stored_items`
- `equipped_cosmetics` — cosmetic equips
- `currency` (int, starts at 100)

**Actions/Methods:**
- `purchase_item()`, `place_item()`, `equip_cosmetic()`
- `get_items_near()`, `mark_interaction()`

**LLM-useful:** placed items (currently sent — up to 10), currency

---

## 30. Duck Home — `world/home.py`

**State tracked:**
- `DecorationSlot` enum — location slots in the home
- Placed decorations, unlocked decorations, themes
- `mood_bonus` — cumulative mood bonus from decorations

**Actions/Methods:**
- `place_decoration(id)`, `remove_decoration(slot)`, `unlock_decoration(id)`
- `set_theme(id)`, `unlock_theme(id)`
- `render_home_preview()` — ASCII art of the home
- `check_unlocks(level, stats, streak, collectibles)` — progression-based unlocks

**LLM-useful:** active theme, placed decorations, mood bonus

---

## 31. Atmosphere (Weather/Season/Visitors) — `world/atmosphere.py`

**State tracked:**
- `WeatherType` enum (SUNNY, CLOUDY, RAINY, STORMY, SNOWY, FOGGY, etc.)
- `Season` enum: SPRING, SUMMER, AUTUMN, WINTER
- `current_season`, `biome_weather` (weather per biome)
- `day_fortune`, `current_visitor`, `visitor_history`, `weather_history`
- `visitor_friendships`

**Actions/Methods:**
- `update()` — advance weather/season
- `set_current_biome()`, `get_biome_weather()`

**LLM-useful:** current weather, season (currently sent), visitor presence

---

## 32. Friends System — `world/friends.py`

**State tracked:**
- `FriendshipLevel` enum — levels of friendship
- `DuckPersonalityType` enum — visitor personality archetypes
- `DuckFriend` — individual friend with personality, friendship level, visit history
- `VisitEvent` — logged visit data

**Actions/Methods:**
- `generate_new_friend()` — create random friend duck
- `start_visit()`, `end_visit()` — manage visits
- `interact_with_visitor()`, `give_gift_to_visitor()`
- `check_for_random_visitor()` — trigger random visits

**LLM-useful:** visiting friend details (currently sent), all known friends (currently sent)

---

## 33. Event System — `world/events.py`

**State tracked:**
- `EventType` enum — categories of events
- `Event`, `Encounter`, `EventChain` classes
- Event cooldowns, active event chains

**Actions/Methods:**
- `check_random_events()`, `check_chain_progress()`
- `start_encounter()`, `try_resolve_encounter()`
- `check_triggered_events()`, `check_special_day_events()`
- `apply_event()` — execute event effects

**LLM-useful:** recent event (currently sent), active event chains

---

## 34. Area Events & Spontaneous Travel — `world/area_events.py`

**State tracked:**
- `AreaEvent` — location-specific events (~1314 lines of event data)
- `SpontaneousTravelSystem` — duck may travel spontaneously
- `AreaEventSystem` — area event checking/application

**Actions/Methods:**
- `check_area_events(area_name)` → Optional[AreaEvent]
- `apply_area_event(duck, event)` → need modifications
- `check_spontaneous_travel()` — duck might wander spontaneously

---

## 35. Crafting System — `world/crafting.py`

**State tracked:**
- `CraftingCategory` enum
- `CraftingRecipe`, `CraftingProgress`, `Tool` classes
- Active crafting progress, tool durability

**Actions/Methods:**
- `get_available_recipes()` — what can be crafted with current materials
- `start_crafting()`, `check_crafting()`, `cancel_crafting()`
- Cancel refunds 50% of materials

**LLM-useful:** what's currently being crafted, available recipes

---

## 36. Building System — `world/building.py`

**State tracked:**
- `StructureType`, `StructureStatus` enums
- `Structure` — built structures with status, level, bonuses
- Building skill level

**Actions/Methods:**
- `start_building()`, `update_building()`, `repair_structure()`
- `apply_weather_damage()` — weather erodes structures
- `get_total_bonuses()` — combined bonuses from all structures
- `has_workbench()` — unlocks advanced crafting

**LLM-useful:** built structures list, structure bonuses, building skill

---

## 37. Garden System — `world/garden.py`

**State tracked:**
- `PlantType`, `GrowthStage` enums
- `PlantedPlant` — individual plants with growth progress
- Unlocked plots (expandable)

**Actions/Methods:**
- `plant_seed()`, `water_plant()`, `update_plants()`, `harvest_plant()`
- `unlock_plot()` — expand garden

**LLM-useful:** planted plants, growth stages, harvest-ready plants

---

## 38. Fishing System — `world/fishing.py`

**State tracked:**
- `FishRarity`, `FishingSpot`, `BaitType` enums
- `CaughtFish` — fish log with rarity, weight
- Unlocked fishing spots

**Actions/Methods:**
- `start_fishing()`, `update()`, `reel_in()`
- `unlock_spot()`, `add_bait()`

**LLM-useful:** fish caught, best catches, fishing skill

---

## 39. Treasure Hunting — `world/treasure.py`

**State tracked:**
- `TreasureRarity`, `TreasureLocation` enums
- `TreasureMap`, `Treasure` classes
- Unlocked locations, found treasures

**Actions/Methods:**
- `start_hunt()`, `dig()`, `use_map()`
- `unlock_location()`

**LLM-useful:** found treasures, active hunts

---

## 40. Quest System — `world/quests.py`

**State tracked:**
- `QuestType`, `QuestDifficulty`, `ObjectiveType` enums
- `Quest`, `ActiveQuest` — quests with objectives, progress, choices

**Actions/Methods:**
- `get_available_quests()`, `start_quest()`, `update_progress()`
- `make_choice()` — branching quest decisions

**LLM-useful:** active quests (currently sent — up to 5 names), quest progress

---

## 41. Festival System — `world/festivals.py`

**State tracked:**
- `FestivalType` enum
- `Festival`, `FestivalActivity` classes
- Festival participation state, rewards

**Actions/Methods:**
- `check_active_festival()`, `start_festival_participation()`
- `do_festival_activity()`, `claim_festival_reward()`

**LLM-useful:** active festival, participation status

---

## 42. Trading System — `world/trading.py`

**State tracked:**
- `TraderType`, `TradeRarity` enums
- `Trader`, `TradeOffer`, `TradeItem` classes
- Available traders and their inventories

**Actions/Methods:**
- `refresh_traders()`, `generate_offers()`, `complete_trade()`

**LLM-useful:** available trades, trader types

---

## 43. Dream System — `world/dreams.py`

**State tracked:**
- `DreamType` enum
- `Dream`, `DreamResult` classes
- Dream history, dream effects on mood/needs

**Actions/Methods:**
- `generate_dream()`, `start_dream()`
- `get_dream_stats()` — dream frequency/types

**LLM-useful:** recent dreams, dream themes

---

## 44. Mini-Games — `world/minigames.py`

**State tracked:**
- `MiniGameType` enum
- 4 games: `BreadCatchGame`, `BugChaseGame`, `MemoryMatchGame`, `DuckRaceGame`
- Scores, play counts

**Actions/Methods:**
- `can_play()`, `start_game()`, `finish_game()`
- `get_available_games()` — which games are unlocked

**LLM-useful:** available games, best scores

---

## 45. Secrets System — `world/secrets.py`

**State tracked:**
- `SecretType`, `SecretRarity` enums
- `Secret` class — hidden discoverable content
- Discovered secrets tracking

**Actions/Methods:**
- `check_input_sequence()` — Konami-code-style inputs
- `check_text_input()` — secret words in chat
- `check_time_secrets()`, `check_date_secrets()` — time-based secrets
- `check_coin_secret()`, `check_action_secrets()`
- `discover_secret()` — reveal a secret

**LLM-useful:** discovered secrets count, secret types found

---

## 46. Collectibles — `world/collectibles.py`

**State tracked:**
- `CollectibleRarity`, `CollectibleType` enums
- `Collectible`, `CollectibleSet` classes
- Collection completion progress

**Actions/Methods:**
- `open_pack()` — gacha-style pack opening
- `trade_duplicates()` — exchange duplicate collectibles
- `get_set_progress()` — completion percentage per set

**LLM-useful:** collection completion %, notable collectibles

---

## 47. Decorations System — `world/decorations.py`

**State tracked:**
- `DecorationCategory`, `DecorationRarity`, `RoomType` enums
- `Decoration`, `Room` classes
- Placed decorations per room, room bonuses

**Actions/Methods:**
- `buy_decoration()`, `place_decoration()`, `remove_decoration()`
- `get_room_bonuses()` — cumulative effects of room decor

**LLM-useful:** room decoration themes, room bonuses

---

## 48. Fortune System — `world/fortune.py`

**State tracked:**
- `DuckZodiacSign`, `FortuneCategory`, `FortuneRarity` enums
- `ZodiacInfo`, `DailyHoroscope`, `FortuneCookie` classes
- Duck's zodiac sign, daily horoscope, lucky items

**Actions/Methods:**
- `set_duck_birthday()`, `generate_daily_horoscope()`
- `get_fortune_cookie()`, `get_compatibility()`
- `get_daily_bonus()` — fortune-based gameplay bonuses

**LLM-useful:** today's horoscope, zodiac sign, fortune cookie message, lucky items

---

## 49. Achievements — `world/achievements.py`

**State tracked:**
- `Achievement` class — name, description, progress, unlocked state

**Actions/Methods:**
- `unlock()`, `is_unlocked()`, `increment_progress()`
- `get_pending_notifications()` — newly unlocked achievements

**LLM-useful:** recently unlocked achievements, total completion

---

## 50. Goals — `world/goals.py`

**State tracked:**
- `Goal` class — daily and weekly goals
- Goal progress tracking

**Actions/Methods:**
- `add_daily_goals()`, `add_weekly_goals()`
- `update_progress()`, `update_time()` — tick-based goal updates

**LLM-useful:** active daily/weekly goals, goal completion

---

## 51. Challenges — `world/challenges.py`

**State tracked:**
- `ChallengeType`, `ChallengeDifficulty` enums
- `ActiveChallenge` — challenges with progress and time limits

**Actions/Methods:**
- `refresh_daily_challenges()`, `refresh_weekly_challenges()`
- `update_progress()`, `claim_reward()`

**LLM-useful:** active challenges, challenge progress

---

## 52. Weather Activities — `world/weather_activities.py`

**State tracked:**
- `WeatherType`, `ActivityType` enums
- `WeatherActivity` — weather-specific activities (e.g., puddle jumping in rain)

**Actions/Methods:**
- `get_available_activities()` — activities for current weather
- `start_activity()`, `check_activity_complete()`

**LLM-useful:** available weather activities, active weather activity

---

## 53. Scrapbook — `world/scrapbook.py`

**State tracked:**
- `PhotoCategory` enum (PORTRAIT, SCENERY, FRIEND, EVENT, MILESTONE, SEASONAL, etc.)
- `ScrapbookPhoto` — ASCII art "photos" with stickers, frames
- Album pages, favorites, unlocked frames/stickers

**Actions/Methods:**
- `take_photo()`, `toggle_favorite()`, `add_sticker()`
- `unlock_frame()`, `unlock_sticker()`
- `get_page()`, `get_photos_by_category()`, `get_favorites()`
- `auto_capture_milestone(milestone_type, duck_name, duck_age, mood)`
- `render_photo()`, `render_album_page()`

**LLM-useful:** photo count, favorite photos, milestone photos

---

## 54. Tricks System — `duck/tricks.py`

**State tracked:**
- `TrickDifficulty`, `TrickCategory` enums
- `Trick`, `LearnedTrick` classes
- Trick mastery levels, combo sequences

**Actions/Methods:**
- `get_available_tricks()`, `start_training()`, `do_training_session()`
- `perform_trick()`, `perform_combo()` — execute tricks for XP/fun

**LLM-useful:** known tricks, trick mastery levels, combos

---

## 55. Titles System — `duck/titles.py`

**State tracked:**
- `TitleCategory`, `TitleRarity` enums
- `Title`, `EarnedTitle` classes
- Equipped title, nickname

**Actions/Methods:**
- `earn_title()`, `equip_title()`, `get_display_name()`
- `set_nickname()`, `check_title_conditions()`

**LLM-useful:** current title/nickname, earned titles

---

## 56. Outfits — `duck/outfits.py`

**State tracked:**
- `OutfitSlot` enum (HAT, SCARF, SHOES, ACCESSORY, etc.)
- `OutfitItem`, `EquippedOutfit`, `SavedOutfit` classes
- Owned items, equipped outfit, saved outfit presets

**Actions/Methods:**
- `purchase_item()`, `equip_item()`, `unequip_slot()`
- `save_outfit()`, `load_outfit()`
- `get_total_mood_bonus()` — outfit mood effects

**LLM-useful:** currently worn outfit, mood bonus from outfit

---

## 57. Seasonal Clothing — `duck/seasonal_clothing.py`

**State tracked:**
- `Season`, `ClothingSlot`, `SeasonalRarity`, `HolidayType` enums
- `SeasonalItem` — season/holiday-specific clothing
- Seasonal shop inventory, unlocked holiday items

**Actions/Methods:**
- `equip_item()`, `auto_equip_for_season()`
- `refresh_seasonal_shop()`, `unlock_holiday()`
- `get_season_bonus()` — bonuses for wearing season-appropriate clothing

**LLM-useful:** current seasonal outfit, season bonus

---

## 58. Cosmetics Renderer — `duck/cosmetics.py`

**Actions/Methods:**
- `render_duck_with_cosmetics()` — render ASCII duck with equipped cosmetics
- `get_cosmetic_preview()`, `get_cosmetic_description()`

(Rendering only — no persistent state beyond equipped items)

---

## 59. Behavior AI — `duck/behavior_ai.py`

**State tracked:**
- `AutonomousAction` enum — many possible autonomous duck actions
- `ActionResult` — outcome of autonomous action
- Utility scores per action

**Actions/Methods:**
- `select_action()` — utility-based AI picks best action
- `perform_action()` — execute chosen autonomous action
- `_calculate_utilities()` — score each possible action
- `should_act()` — check if enough time has passed (15s interval)
- `complete_movement()` — finish movement animation
- Has LLM integration for generating contextual comments on actions

**Config:**
- `AI_IDLE_INTERVAL = 15.0` seconds, `AI_RANDOMNESS = 0.3`, `DERPY_RANDOMNESS_BONUS = 0.4`

**LLM-useful:** current autonomous action, action history

---

## 60. Progression System — `core/progression.py`

**State tracked:**
- `level` (int), `xp` (int), `total_xp` (int)
- `streak` — consecutive day login streak
- `daily_challenges` — List[DailyChallenge]
- `collectibles` — Dict[str, int]
- `milestones` — unlocked milestones
- `reward_history` — past rewards

**Actions/Methods:**
- `add_xp(amount)` — add XP, check level up
- `check_login()` — process daily login, update streak
- `claim_daily_rewards()`, `record_interaction(type)`
- `check_milestones()`, `add_collectible()`
- `generate_daily_challenges()`, `update_challenge_progress()`

**LLM-useful:** player level, streak, daily challenge progress

---

## 61. Prestige System — `core/prestige.py`

**State tracked:**
- `LegacyTier` enum — prestige levels
- `DuckLegacy` — prestige run history
- Legacy points, active bonuses, prestige count

**Actions/Methods:**
- `can_prestige()` — check prerequisites
- `prestige()` — reset and gain legacy rewards
- `spend_legacy_points()`, `get_current_tier()`
- `get_active_bonuses()` — legacy bonuses applied

**LLM-useful:** prestige tier, legacy bonuses, prestige count

---

## 62. Day/Night System — `ui/day_night.py`

**State tracked:**
- `TimeOfDay` enum: DAWN, MORNING, MIDDAY, AFTERNOON, DUSK, EVENING, NIGHT, LATE_NIGHT
- `MoonPhase` enum (8 phases)
- Current real-time hour mapping to game time
- Shooting star chance, energy modifiers, time bonuses

**Actions/Methods:**
- `get_current_hour()`, `get_time_of_day()`, `get_current_phase()`
- `get_moon_phase()`, `get_sky_gradient()`, `get_ambient_modifier()`
- `check_time_bonus()` — bonuses at special times
- `check_shooting_star()` — rare event
- `get_duck_energy_modifier()` — energy decay varies by time

**LLM-useful:** time of day (currently sent), moon phase, time-specific bonuses

---

## 63. Statistics System — `ui/statistics.py`

**State tracked:**
- `StatCategory` enum — stat groupings
- `StatRecord` — per-stat tracking (total, session, daily, weekly, all-time best)
- Tracked stats include: interactions, explorations, crafts, builds, play time, etc.
- Mood distribution tracking
- Session start/end times

**Actions/Methods:**
- `start_session()`, `end_session()`
- `increment_stat(name, amount)` — track any named stat
- `get_stat_summary(name)`, `get_overview_stats()`
- `record_mood(mood)`, `get_mood_distribution()`
- `check_milestones()` — stat-based milestones

**LLM-useful:** total play time, interaction counts, mood distribution

---

## 64. Badges — `ui/badges.py`

**State tracked:**
- `BadgeRarity`, `BadgeCategory` enums
- `Badge`, `EarnedBadge` classes
- Badge showcase (up to N featured badges), favorite badge

**Actions/Methods:**
- `earn_badge(id)`, `has_badge(id)`
- `add_to_showcase()`, `remove_from_showcase()`, `set_favorite()`
- `get_earned_count()`, `get_rarity_count()`
- `render_showcase()`, `render_badge_collection()`

**LLM-useful:** recently earned badges, showcase badges, total badge count

---

## 65. Settings — `core/settings.py`

**State tracked:**
- `TextSpeed` (SLOW, NORMAL, FAST, INSTANT)
- `Difficulty` (EASY, NORMAL, HARD)
- Audio, Display, Accessibility, Gameplay sub-settings
- Key bindings

**Actions/Methods:**
- `SettingsManager` — load/save/reset settings
- `get_difficulty_multiplier()`, `get_text_speed_delay()`
- `should_show_animations()`, `should_show_particles()`

**LLM-useful:** difficulty level (affects need decay multiplier)

---

## 66. Save System — `core/persistence.py` + `core/save_slots.py`

### SaveManager:
- `save()`, `load()`, `delete_save()`, `save_exists()`
- `_migrate_save()` — handles save format upgrades

### SaveSlotsSystem:
- 3+ save slots
- `save_to_slot()`, `load_slot()`, `delete_slot()`
- `copy_slot()`, `restore_backup()`, `export_slot()`, `import_slot()`

---

## 67. Audio Systems — `audio/`

### Sound Effects (`audio/sound_effects.py`):
- `SoundCategory`, `SoundPriority`, `MoodModifier` enums
- `SoundEffect` — ASCII text-based "sound effects" (visual onomatopoeia)
- `SoundEffectSystem` — play/manage sound effects with category volumes, muting

### Ambient Sounds (`audio/ambient.py`):
- `AmbientCategory`, `SoundMood` enums
- `AmbientSound`, `AmbientSoundSystem`
- Location/weather/time-based ambient text effects

### Radio (`audio/radio.py`):
- Background music/radio system (text-based)

(These are **text-based** visual sound effects rendered in the terminal, not actual audio)

---

## 68. Core Game Loop — `core/game.py` (~10,789 lines)

### Game States:
- `_state`: "init", "title", "playing", "paused", "daily_rewards"

### Active Menu Flags (show_*_menu):
crafting, building, areas, use, minigames, quests, weather, treasure, scrapbook, tricks, titles, decorations, collectibles, secrets, garden, prestige, save_slots, trading, enhanced_diary, festival, settings, debug

### Key Game Methods:
- `_perform_interaction(interaction_type)` — processes feed/play/clean/pet/sleep
- `_process_talk()` — handles player chat (routes through LLM)
- `_get_memory_context_for_dialogue()` — builds LLM context (documented at top)
- `_update()` — main game tick
- Many `_handle_*_menu()` methods for each subsystem

---

## Summary: What's NOT Being Sent to the LLM

The following data exists but `_get_memory_context_for_dialogue()` does NOT include:

| Category | Missing Data |
|---|---|
| **Duck State** | Trust level, sickness, growth stage, age, personality traits/summary, needs values, current action, outfit/title |
| **Player Model** | Player facts, player traits, behavioral observations, visit patterns |
| **Rituals** | Established rituals, missed rituals |
| **Conversation Memory** | Notable quotes, learned facts, conversation topics, callbacks |
| **Extended Personality** | Quirks, preferences, hidden traits |
| **World State** | Built structures, garden plants, fish caught, treasures found, dream themes |
| **Progression** | Level, XP, streak, prestige tier, legacy bonuses |
| **Collections** | Collectible completion, badges earned, titles, tricks known |
| **Crafting/Building** | Active crafting, buildings and their bonuses |
| **Fortune** | Daily horoscope, zodiac sign |
| **Statistics** | Play time, interaction distribution, mood history |
| **Challenges/Goals** | Active daily/weekly challenges, goal progress |
| **Festival** | Active festival, participation |
| **Mini-games** | Available games, best scores |
| **Secrets** | Discovered secrets |
| **Diary** | Recent diary entries, life chapters |
| **Moon/Time** | Moon phase, time bonuses |
