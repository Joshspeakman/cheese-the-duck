# Comprehensive UI Rendering Audit Report

**Project:** Stupid Duck (Terminal game using `blessed` library)  
**Files Audited:** All 17 files in `ui/`  
**Scope:** UI Layout Consistency · ASCII Art Completeness · Statistics Display

---

## Table of Contents

1. [UI Layout Consistency](#1-ui-layout-consistency)
   - [1.1 Border / Box-Drawing Styles](#11-border--box-drawing-styles)
   - [1.2 Navigation Hint Inconsistencies](#12-navigation-hint-inconsistencies)
   - [1.3 Color System Usage](#13-color-system-usage)
   - [1.4 Panel & Overlay Layout](#14-panel--overlay-layout)
2. [ASCII Art Completeness](#2-ascii-art-completeness)
   - [2.1 Duck Art (ascii_art.py)](#21-duck-art-ascii_artpy)
   - [2.2 Habitat Art (habitat_art.py / habitat_icons.py)](#22-habitat-art)
   - [2.3 Location Art (location_art.py)](#23-location-art-location_artpy)
   - [2.4 Event Animations (event_animations.py)](#24-event-animations-event_animationspy)
   - [2.5 Interaction Animations (interaction_animations.py)](#25-interaction-animations)
   - [2.6 Badges (badges.py)](#26-badges-badgespy)
   - [2.7 Day/Night (day_night.py)](#27-daynight-day_nightpy)
   - [2.8 Mood Visuals (mood_visuals.py)](#28-mood-visuals-mood_visualspy)
   - [2.9 Animations (animations.py)](#29-animations-animationspy)
   - [2.10 Reactions (reactions.py)](#210-reactions-reactionspy)
3. [Statistics / Stats Display](#3-statistics--stats-display)
4. [Rendering Bugs & Issues](#4-rendering-bugs--issues)
5. [Summary of Critical Findings](#summary-of-critical-findings)

---

## 1. UI Layout Consistency

### 1.1 Border / Box-Drawing Styles

The codebase uses **five distinct border drawing styles**. This is the primary layout inconsistency.

| Style | Characters | Used In |
|-------|-----------|---------|
| **BOX (single-line)** | `┌ ┐ └ ┘ ─ │ ├ ┤ ┬ ┴ ┼` | Playfield frame, side panel, progress bars, controls bar |
| **BOX_DOUBLE (double-line)** | `╔ ╗ ╚ ╝ ═ ║` | Header bar, `_overlay_box` (shared by help/stats/talk/fishing/inventory/menu/message overlays), offline summary |
| **Custom cyan `+`/`=`/`\|`** | `+ = \|` | `_overlay_item_interaction` — uses `term.cyan("+" + "=" * n + "+")` with pipe sides |
| **Custom `+`/`=`/`-`/`\|`** | `+ = - \|` | Title screen — uses `+======...+` top/bottom and `\|` sides |
| **BORDER dict (ascii_art.py)** | `+ - \|` | `create_box()` helper in ascii_art.py |
| **No border at all** | (none) | `_overlay_celebration` — content rendered directly with no frame |

**Impact:** Five different framing conventions means overlays look visually distinct from each other, even though they serve the same purpose (modal popups over the playfield).

**Specific issues:**
- `_overlay_item_interaction` (renderer.py ~L3207) uses a cyan ASCII `+/=/|` border instead of `BOX_DOUBLE` like every other overlay that goes through `_overlay_box`.
- `_overlay_celebration` (renderer.py ~L3120) has **no border at all** — content floats unframed over the playfield.
- Title screen (renderer.py ~L2600) uses its own `+======+` / `|...|` border style.
- `badges.py` `render_showcase` / `render_badge_collection` use `+=====...=+` ASCII borders (never displayed through the renderer's `_overlay_box`).
- `day_night.py` `render_time_display` uses `+=====...=+` ASCII borders.
- `statistics.py` `render_stats_screen` uses `+=====...=+` ASCII borders.
- `settings_menu.py` `get_display_lines` uses `╔═╗ ║ ╚═╝` — matches BOX_DOUBLE visually but is independently constructed, not via `_overlay_box`.

**Recommendation:** Funnel all overlay/modal rendering through `_overlay_box` (or a shared box-builder that uses `BOX_DOUBLE` consistently), and either give `_overlay_celebration` and `_overlay_item_interaction` matching borders or explicitly document them as intentionally different.

---

### 1.2 Navigation Hint Inconsistencies

Every overlay/menu has its own navigation hint footer. The formats, key names, and separators are inconsistent:

| Overlay / Context | Navigation Hint | Issues |
|---|---|---|
| **Controls bar** (bottom of main screen) | `[Arrows] Nav \| [Enter] Select \| [Bksp] Back \| [M]usic [N]oise \| [H]elp` | Uses `\|` separator, `[Arrows]`, partial key names `[M]usic [N]oise` |
| **Chat log / messages area** | `[TAB] Menu \| [H] Help \| [Q] Quit` | Uses `\|` separator, different set of keys |
| **Help overlay** | `Press [H] to close` | Uses `Press ... to close` style |
| **Stats overlay** | `[^] Up \| [v] Down \| [ESC] Close` | Uses arrow symbols `^` `v`, `\|` separator |
| **Talk overlay** | `Press ESC to cancel` | No brackets on `ESC`, uses "Press ... to cancel" style |
| **Fishing overlay** | `[Q] or [ESC] to stop fishing` | Uses `or`, "to stop fishing" instead of "to close" |
| **Inventory overlay** | `[1-9] Use item \| [</>] Page \| [I] Close` | Uses `\|`, `[</>]` for pages, item-specific close key `[I]` |
| **Shop overlay** | `<- -> : Category \| ^ v : Select \| [B]uy \| [T]oggle \| [ESC]` | Uses `:` separator plus `\|`, raw arrow chars, partial key names |
| **Menu overlay** (`show_menu`) | `[^v] Navigate  [Enter] Select  [ESC] Close` | Uses double-space separator, `[^v]` combined |
| **Settings menu** (editing) | `←/→ to adjust, ENTER to confirm` | Uses Unicode arrows, comma separator, unbracketed `ENTER` |
| **Settings menu** (normal) | `←/→ Category  ↑/↓ Navigate  ENTER Edit  ESC Close` | Unicode arrows, double-space separator, unbracketed keys |
| **HierarchicalMenuSelector** (level 0) | `[^v] Navigate  [Enter/->] Open  [TAB] Close` | `[Enter/->]`, `[TAB]` close |
| **HierarchicalMenuSelector** (level 1) | `[^v] Navigate  [Enter] Select  [<-/ESC] Back` | `[<-/ESC]` for back |
| **MenuSelector** (all) | `[^v] Navigate  [Enter] Select  [ESC] Close` | Same for both paginated and non-paginated |
| **Badge collection** | `Page {n}/{m}  [<-/->] Navigate  [S] Showcase` | `[<-/->]` for pages |
| **Statistics (own renderer)** | `Page {n}/5  [<-/-> to navigate]` | `[<-/-> to navigate]` mixed bracket/text style |
| **Celebration overlay** | `Press any key to continue...` | Completely different format |
| **Input handler help text** | Full multi-line block with section headers | Uses `[KEY] Action` format |

**Summary of inconsistencies:**
1. **Separator style:** `|` vs `  ` (double-space) vs `:` vs `,` — no single convention.
2. **Key bracket style:** `[ESC]` vs `ESC` vs `[<-/ESC]` — sometimes keys have brackets, sometimes not.
3. **Arrow key representation:** `[^v]` vs `[^] [v]` vs `^ v` vs `↑/↓` vs `[Arrows]` vs `<- ->` — at least six different styles.
4. **Close/cancel wording:** "Close" vs "cancel" vs "to stop fishing" vs "to close" vs "to continue" — inconsistent verbs.
5. **Close key varies:** `[ESC]` vs `[H]` vs `[I]` vs `[TAB]` vs `[Q]` — different keys close different overlays.

**Recommendation:** Establish a standard hint format, e.g., `[↑↓] Navigate | [Enter] Select | [Esc] Close` and apply it uniformly. Use a shared `_format_nav_hints()` helper to generate footers.

---

### 1.3 Color System Usage

- **renderer.py:** Uses `self.term.color_rgb(r, g, b)` for cross-platform color consistency. Defines named color constants and applies them via the `blessed` terminal.
- **habitat_art.py:** Uses `ItemColors` class wrapping `term.yellow`, `term.blue`, etc. (named terminal colors), not RGB.
- **habitat_icons.py:** Also uses `ItemColors` with named terminal colors.
- **mood_visuals.py:** Defines `MoodVisualTheme` with `primary_color` and `secondary_color` as string names (e.g., `"yellow"`, `"cyan"`), plus `particles` and `background_chars`. **However, this system is defined but not used by the renderer** — see §4.
- **settings_menu.py:** No color applied — generates plain string lines (expects renderer to colorize).
- **badges.py / day_night.py / statistics.py:** Generate plain text ASCII art with no color application.

**Issues:**
- Mixed color systems: Some files use RGB, others use named terminal colors.
- `mood_visuals.py` defines a comprehensive mood-based theming system (12 moods with colors, particles, borders, animation speeds) that is **never referenced** by `renderer.py`.

---

### 1.4 Panel & Overlay Layout

**Main screen layout** (renderer.py `render_frame`):

```
╔═════════════── Header Bar (BOX_DOUBLE) ══════════════╗
║ Duck name | mood | coins | location | time | weather  ║
╚══════════════════════════════════════════════════════╝
┌─── Playfield (BOX single) ───┬─── Side Panel (BOX) ──┐
│ sky, weather particles,      │ Closeup face           │
│ scenery, decorations,        │ Needs bars             │
│ visitors, duck sprite,       │ Master menu tree       │
│ habitat items,               │ Activity / Location    │
│ chat log                     │ Status area            │
└──────────────────────────────┴────────────────────────┘
┌──────── Progress Bars (BOX single) ──────────────────┐
│ Level XP bar | Growth bar | Goals completion          │
└──────────────────────────────────────────────────────┘
┌──────── Controls Bar (BOX single) ───────────────────┐
│ [Arrows] Nav | [Enter] Select | [Bksp] Back | ...    │
└──────────────────────────────────────────────────────┘
```

**Overlay priority chain** (checked in `render_frame`):
1. `_overlay_celebration` — no border
2. `_overlay_item_interaction` — cyan `+/=` border (NOT BOX_DOUBLE)
3. `_overlay_fishing` — BOX_DOUBLE via `_overlay_box`
4. `_overlay_help` — BOX_DOUBLE via `_overlay_box`
5. `_overlay_stats` — BOX_DOUBLE via `_overlay_box`
6. `_overlay_talk` — BOX_DOUBLE via `_overlay_box`
7. `_overlay_inventory` — BOX_DOUBLE via `_overlay_box`
8. `_overlay_shop` — BOX_DOUBLE via `_overlay_box`
9. `_overlay_menu` — BOX_DOUBLE via `_overlay_box`
10. `_overlay_message` — BOX_DOUBLE via `_overlay_box`

**Issue:** Items 1 and 2 break the consistent `_overlay_box` pattern.

---

## 2. ASCII Art Completeness

### 2.1 Duck Art (ascii_art.py)

**Large Duck Art (`DUCK_ART` dict):**

| Stage | States Available | Count |
|-------|-----------------|-------|
| **Duckling** | normal, happy, sad, sleeping, eating | 5 |
| **Teen** | normal, happy, sad, sleeping, eating, grumpy | 6 |
| **Adult** | normal, happy, ecstatic, sad, miserable, sleeping, eating, grumpy, quack, splash, preen, stare, trip, flap, waddle_left, waddle_right | 16 |
| **Elder** | normal, happy, sleeping, sad | 4 |

**⚠ Gap:** Elder and duckling stages have far fewer expression states than adult. States like `ecstatic`, `grumpy`, `quack`, `splash`, `preen`, `stare`, `trip`, `flap`, `waddle_left`, `waddle_right` exist only for adults. If the renderer requests a state that doesn't exist for a given stage, it must fall back to `normal`.

**Emotion Closeups (`EMOTION_CLOSEUPS`):** 18 emotions — normal, happy, ecstatic, sad, miserable, grumpy, content, eating, sleeping, excited, confused, love, derpy, playing, cleaning, petting, thinking, singing.  
✅ Good coverage. Stage-independent (used in the side panel).

**Mini Duck Sprites (`MINI_DUCK`):** 7 growth stages with extensive state sets:

| Stage | States Count | Notes |
|-------|-------------|-------|
| **Egg** | ~6 | idle, wobble, crack, hatch + frame2 variants |
| **Hatchling** | ~40+ | Full state set |
| **Duckling** | ~40+ | Full state set |
| **Teen** | ~40+ | Full state set |
| **Adult** | ~40+ | Full state set |
| **Elder** | ~40+ | Full state set |
| **Legendary** | ~40+ | Full state set |

✅ Mini duck sprites are comprehensive across all stages.

**`STAGE_SPRITE_MAP`:** Maps all growth stage names correctly: egg, hatchling, duckling, juvenile→teen, young_adult→adult, adult, mature→elder, elder, legendary. ✅

**Celebration Art (`CELEBRATION_ART`):** 7 types:
- `level_up` — 4-frame animation ✅
- `streak_milestone` — static ✅
- `collectible_found` — static ✅
- `achievement` — static ✅
- `surprise_gift` — static ✅
- `jackpot` — static ✅
- `new_record` — static ✅

**Playfield Objects (`PLAYFIELD_OBJECTS`):** 11 objects: flower, grass, rock, mushroom, puddle, leaf, acorn, stick, butterfly, worm, nest. ✅

---

### 2.2 Habitat Art (habitat_art.py / habitat_icons.py)

**habitat_art.py (`HABITAT_ITEM_ART`):** ~150+ items with multi-line ASCII art across categories: toys, furniture, water features, plants, structures, decorations, lighting, flooring, special items, built structures (14 building types).

**habitat_icons.py (`HABITAT_ICONS`):** ~200+ items as `(char, color_func)` tuples for playfield mini-display.

**⚠ Cross-reference gap — Items with icons but NO art:**

Many items in `HABITAT_ICONS` do **not** have corresponding entries in `HABITAT_ITEM_ART`. These items display as a single character on the playfield but have no larger ASCII art for preview/interaction screens:

- **Water features:** `wave_pool`, `lazy_river`, `aquarium_large`, `hot_tub_deluxe`, `waterfall_wall`, `infinity_pool`
- **Plants:** `bonsai_tree`, `bamboo_grove`, `cherry_blossom`, `lavender_field`, `moss_garden`, `carnivorous_plants`, `herb_spiral`, `aquatic_garden`, `sunflower_row`, `cactus_garden`, `orchid_collection`, `topiary_animal`, `fairy_garden`, `zen_sand_garden`, `living_wall`
- **Decorations:** `wind_chimes_crystal`, `garden_gnome`, `bird_feeder_deluxe`, `butterfly_house`, `weather_vane`, `sundial`, `mini_lighthouse`, `gazing_ball`, `garden_arch`, `stone_lantern`, `wind_spinner`, `rain_chain`, `copper_fountain`
- **Outdoor items:** `treehouse`, `gazebo`, `pergola`, `fire_pit`, `outdoor_kitchen`, `telescope`, `hammock_deluxe`, `zip_line`, `climbing_wall`, `rope_bridge`
- **Special/legendary:** `golden_pond`, `enchanted_tree`, `crystal_cave`, `rainbow_bridge`, `floating_island`, `starlight_fountain`, `aurora_curtain`, `time_sundial`, `wishing_well_gold`, `phoenix_perch`, `dragon_egg_nest`, `cloud_walkway`, `moonstone_arch`

Total: **~50+ items with icons but no art.**

---

### 2.3 Location Art (location_art.py)

**All 21 locations have complete art definitions** — ground characters, decorations, scenery elements, and location-specific colors:

Home Pond ✅ · Deep End ✅ · Forest Edge ✅ · Ancient Oak ✅ · Mushroom Grove ✅ · Sunny Meadow ✅ · Butterfly Garden ✅ · Pebble Beach ✅ · Waterfall ✅ · Vegetable Patch ✅ · Tool Shed ✅ · Foothills ✅ · Crystal Cave ✅ · Sandy Shore ✅ · Shipwreck Cove ✅ · Misty Marsh ✅ · Cypress Hollow ✅ · Sunken Ruins ✅ · Park Fountain ✅ · Rooftop Garden ✅ · Storm Drain ✅

✅ **No gaps.** Two locations (Home Pond, Forest Edge) have dynamic scenery generators for additional variety.

---

### 2.4 Event Animations (event_animations.py)

**15 animated event types with complete sprite sets:**

| Event ID | Animator Class | Sprite Frames | Color |
|----------|---------------|---------------|-------|
| `butterfly` | ButterflyAnimator | fly×3, idle×2, land×2 (7) | Cycling magenta/cyan/yellow/blue |
| `bird_friend` | BirdAnimator | fly×4, hop×2, idle×2, chirp×2, peck×2 (12) | Yellow |
| `another_duck` | DuckVisitorAnimator | waddle×3, idle×2, quack×2, happy×2, gift×2, wave×2 (13) | Yellow |
| `found_shiny` | ShinyObjectAnimator | appear×3, shine×3, pickup×2 (8) | Cycling yellow/white/cyan |
| `nice_breeze` | BreezeAnimator | Particle-based (~50 particles) | Cyan |
| `found_crumb` | CrumbAnimator | crumbs×3, eating×2, gone (6) | Yellow |
| `loud_noise` | LoudNoiseAnimator | bang×3, shake×2 (5) | Red→Yellow |
| `bad_dream` | DreamCloudAnimator | cloud×2, bad×2 (4) | Red or Cyan |
| `lily_pad` | LilyPadAnimator | pad×4 (4) | Green |
| `ripple` | RippleAnimator | ripple×7 (7) | Cyan |
| `frog_hop` | FrogAnimator | hop×2, sit×2, croak×2 (6) | Green |
| `dragonfly` | DragonflyAnimator | fly×3, hover×2 (5) | Blue |
| `bubbles` | BubblesAnimator | Particle-based (~15) | Cyan |
| `falling_object` | FallingObjectAnimator | fall×3, impact×2 (5) | Yellow→Red |
| `squirrel` | SquirrelAnimator | run×2, sit×2, panic×2 (6) | Yellow→Red |

✅ All event animations are complete. Factory function `create_event_animator()` and `ANIMATED_EVENTS` list both match.

---

### 2.5 Interaction Animations (interaction_animations.py)

**8 item-specific animation sets defined:**

| Item | Frames | Description |
|------|--------|-------------|
| `toy_ball` | 5 | Ball bouncing with duck catching |
| `birdbath` | 5 | Duck splashing in birdbath |
| `pool_kiddie` | 5 | Duck swimming in pool |
| `toy_trampoline` | 5 | Duck bouncing on trampoline |
| `toy_swing` | 4 | Duck swinging |
| `hammock` | 3 | Duck relaxing in hammock |
| `toy_piano` | 4 | Duck playing piano with notes |
| `furniture_rest` | 3 | Generic resting on furniture |

**Fallback system:** `get_animation_frames()` uses keyword matching ("ball"→toy_ball, "bath"→birdbath, "pool"→pool_kiddie, etc.).

**⚠ Gap:** With 150+ habitat items defined, only 8 have specific animations. Many interactive items (telescope, zip_line, climbing_wall, fire_pit, etc.) will get no animation or only a vague keyword fallback.

**Stage-specific support:** `get_animation_frames_with_stage()` integrates with `world/item_interactions.py` for life-stage variants — falls back to legacy animations if none found.

---

### 2.6 Badges (badges.py)

**33 badges** across 9 categories (care, activities, exploration, social, collection, mastery, secret, seasonal, special).

**⚠ Art issue:** Badge ASCII art is placeholder-level — each badge only has a 1–3 character string:
```
[B]  [X]  [[C]]  [*]  [<3]  [[>]]  ...
```
No multi-line badge icons exist.

**⚠ Duplicate icon issue:** Several badges share the same icon:
- `*` used by 7 badges (petting_pro, first_friend, level_10, level_25, level_50, fashionista, summer_sun)
- `[+]` used by popular_duck and generous_giver
- `[#]` used by game_master, collector, completionist

**Border style:** `render_showcase`/`render_badge_collection` use `+=====...=+` borders — yet another border style not matched by the overlay system.

---

### 2.7 Day/Night (day_night.py)

**8 time phases** (dawn, morning, midday, afternoon, evening, dusk, night, late_night):
- ✅ Sky gradient art (2 lines each)
- ✅ Duck visual art (4 lines each)
- ✅ Moon phase icons (8 phases)
- ✅ Time display renderer
- ✅ Mini time widget for HUD

**Border style:** `render_time_display` uses `+=====...=+` borders (same standalone style as badges and statistics).

---

### 2.8 Mood Visuals (mood_visuals.py)

**12 mood themes** with comprehensive parameters:

ECSTATIC · HAPPY · CONTENT · NEUTRAL · SAD · ANXIOUS · TIRED · SICK · EXCITED · ANGRY · SCARED · PLAYFUL

Each defines: primary/secondary colors, particles, background chars, border style character, animation speed, brightness modifier, special effect name.

**⚠ CRITICAL ISSUE:** This entire 478-line module appears to be **dead code**. `renderer.py` does not import or reference `mood_visuals.py`. The renderer handles mood-based visuals through its own hardcoded logic. The `MoodVisualEffects` class with its transition system, particle generation, border decoration, and background effects is fully implemented but never called.

---

### 2.9 Animations (animations.py)

**20 animation types** via `AnimationType` enum.  
**17 effect overlays** (heart, hearts, sparkle, exclaim, question, angry, zzz, music, sweat, happy, sad, splash, bounce, play, comfy, sniff, admire).  
**5 particle types** (dust, water, sparkle, leaves, crumbs).  
**4 animation factory functions** (waddle, bounce, shake, spin).

✅ Complete and well-structured.

---

### 2.10 Reactions (reactions.py)

**7 weather reaction types** mapping weather→duck states+effects.  
**14 event reaction types** mapping events→duck states+effects+sounds.  
**DuckReactionController** class with priority system (user actions > event reactions > weather reactions).

✅ Complete and well-structured.

---

## 3. Statistics / Stats Display

### 3.1 Statistics System (statistics.py)

`StatisticsSystem` tracks **60+ metrics** across categories:

| Category | Metrics | Tracking Type |
|----------|---------|---------------|
| General | playtime, sessions, streaks | Raw ints |
| Care | fed, played, petted, talked, cleaned, sleep | `StatRecord` (daily/weekly/monthly) |
| Activities | minigames, fish, plants, treasures, tricks | Mixed `StatRecord` + ints |
| Economy | coins earned/spent, items bought/sold | Mixed |
| XP | xp earned, levels | Mixed |
| Social | friends, gifts, visitors | Raw ints only |
| Exploration | areas, explorations, secrets | Raw ints only |
| Quests | completed, failed, chains | Raw ints only |
| Challenges | daily, weekly, best streak | Raw ints only |
| Festivals | participated, rewards | Raw ints only |
| Collections | collectibles, sets, shiny | Raw ints only |
| Duck | age, stages, moods, titles, outfits | Mixed |

### 3.2 Dual Stats Rendering

There are **two independent stat rendering paths**:

**Path A — `renderer.py._overlay_stats`:**
- Dynamically generates content from `game._statistics` and `duck.memory`
- Uses `_overlay_box` for consistent BOX_DOUBLE borders
- Has pagination via `stats_page` state variable
- Navigation: `[^] Up | [v] Down | [ESC] Close`
- **This is the one actually displayed to users.**

**Path B — `statistics.py.render_stats_screen`:**
- Self-contained 5-page renderer
- Uses its own `+=====+` borders
- Navigation: `Page {n}/5  [<-/-> to navigate]`
- **This is never called from the rendering pipeline** (dead code).

### 3.3 Stats Formatting Bugs (in statistics.py)

Even though `render_stats_screen` appears to be dead code, it has formatting issues:

1. **Inconsistent center-pad widths:** Lines use `{:^24}`, `{:^30}`, `{:^25}`, `{:^26}`, `{:^27}`, `{:^29}`, `{:^22}`, `{:^23}`, `{:^21}`, `{:^20}` — all different center-pad widths against a fixed 47-character interior. Many lines won't align to the `|` border.

2. **Mixed formatting on Page 2:**
   ```python
   f"|  Fed: {val}  Played: {val}  Pet: {val:^16}  |"
   ```
   Only the last value is center-padded; first two float free, total width will vary.

3. **Asymmetric formatting on Page 4:**
   ```python
   f"|  Today: +{earned_today} / -{spent_today:^26}  |"
   ```

---

## 4. Rendering Bugs & Issues

### 4.1 Dead Code: mood_visuals.py
478 lines defining a complete visual theming system. Never imported or used by `renderer.py`.

### 4.2 Dead Code: statistics.py `render_stats_screen`
Standalone renderer with own borders and formatting. Never called from the overlay system.

### 4.3 Dead Code: badges.py render methods
`render_showcase()` and `render_badge_collection()` generate standalone formatted output with own border styles. Not called from the overlay system.

### 4.4 Dead Code: day_night.py render methods
`render_time_display()` generates standalone formatted output with own borders. Not used by the overlay system.

### 4.5 Inconsistent Overlay Borders
- `_overlay_item_interaction`: Cyan `+/=/|` border instead of BOX_DOUBLE
- `_overlay_celebration`: No border at all
- Title screen: `+/=/|` border

### 4.6 Settings Menu Independent Construction
`settings_menu.py` generates its own `╔═╗║╚═╝` borders (matching BOX_DOUBLE visually but independently constructed). Doesn't use `_overlay_box`.

### 4.7 Habitat Art/Icon Mismatch
~50+ items exist in `HABITAT_ICONS` without corresponding `HABITAT_ITEM_ART` entries.

### 4.8 Badge Icon Duplicates
7+ badges share the `*` icon. Within the showcase display, these are indistinguishable.

### 4.9 Large Art Stage Coverage Gap

| Stage | Large Art States | Mini Sprite States |
|-------|-----------------|-------------------|
| Duckling | 5 | ~40+ |
| Teen | 6 | ~40+ |
| Adult | 16 | ~40+ |
| Elder | 4 | ~40+ |

### 4.10 Help Text Discrepancy

The help overlay in `renderer.py` (`_overlay_help`) lists different keys than `input_handler.py`'s `get_help_text()`:

| Feature | renderer.py help | input_handler.py help |
|---------|-----------------|----------------------|
| Use Items | `[U] Use Item` | `[U] Use Items` |
| Quests | `[O] Quests` | Not listed |
| Weather | `[W] Weather Activities` | Not listed |
| Trading | `[V] Trading` | `[<] Trading` |
| Secrets | `[7] Secrets` | `[\\] Secrets` |
| Volume | `[+]/[-] Volume` | `[+/-] Vol` |
| Reset | `[X] Reset Game` | Not listed |
| Diary | Not listed | `[=] Diary` |
| Photo | Not listed | `[;] Photo` |
| Titles | Not listed | `[~] Titles` |
| Prestige | Not listed | `[8] Prestige` |
| Collectibles | Not listed | `['] Collectibles` |

---

## Summary of Critical Findings

| # | Severity | Finding |
|---|----------|---------|
| 1 | **High** | 5+ different border/box styles across the UI — overlays, title screen, item interaction, standalone renderers, celebration |
| 2 | **High** | Navigation hints use ~6 different formats with inconsistent separators, key names, arrow representations, and close keys |
| 3 | **High** | `mood_visuals.py` (478 lines) is completely dead code — never imported by renderer |
| 4 | **Medium** | Help text in renderer vs input_handler shows different key bindings for the same actions |
| 5 | **Medium** | ~50+ habitat items have playfield icons but no ASCII art for preview screens |
| 6 | **Medium** | Elder/duckling large art has 4–5 states vs adult's 16 — severe imbalance |
| 7 | **Medium** | statistics.py, badges.py, day_night.py have standalone render methods that bypass the overlay system (dead code) |
| 8 | **Low** | 7+ badges share the same `*` icon, making them visually indistinguishable |
| 9 | **Low** | statistics.py `render_stats_screen` has inconsistent line widths — formatting will break alignment |
| 10 | **Low** | Settings menu constructs its own BOX_DOUBLE border independently rather than using shared helpers |
