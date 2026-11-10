# Cheese the Duck — ASCII Engine edition

This branch runs the full Cheese simulation in a custom desktop glyph engine, following Dead West Railway's Electron/custom-renderer architecture. The Python gameplay systems remain authoritative; the desktop frontend draws structured color glyph frames on a cached Canvas atlas. It does not launch a terminal, shell, PTY, or xterm.

Open **Play Cheese ASCII.command** in the repository root, or **engine/dist/mac-arm64/Cheese the Duck ASCII Engine.app**. The bundled macOS ARM64 app includes its Python runtime, gameplay modules, original music and sound effects. It needs no first-launch dependency download. The build has an ad-hoc signature for local use, not an Apple notarization for public distribution.

## What carries over

All original gameplay code and data remain: needs and care, growth, personality, trust and consequences, autonomous behavior, conversation and memory, learning, quests, friends, exploration, crafting, building, inventory and shop, fishing, gardening, weather, festivals, collectibles, decorations, tricks, titles, achievements, prestige, diaries, scrapbook, save slots and minigames. Cheese's authored dialogue, duck sprites, expressions, movement and interaction animations are preserved. The former content gate now passes text through unchanged, including profanity, in dialogue learning and memory.

The **Graphics: Ultra / Classic** button switches instantly and remembers your choice. **Classic** is the original engine presentation, preserved pixel for pixel. **Ultra** is the default: a 240 × 112 ASCII world (26,880 character cells), with layered landscapes, etched tree canopies, willow fronds, water reflections, ripples, lily pads, fish, clouds, birds, butterflies, fireflies, seasonal foliage and animated weather. Daylight and moonlight change the palette. Landmarks distinguish the nine biomes and 21 locations: waterfalls, palms, windmills, flower arches, vegetable rows, cabins, ruins, crystal caverns, a fountain and underground storm-drain arches.

Cheese now uses the approved **D10** mallard: compact proportions, a curled forelock, jade head, cream collar, warm feathered body and blue folded wing. All nine approved ages are live, with fitted equipment and posed feet, head, wings and bill. Hatchlings, ducklings and juveniles retain their original golden feather brightness, with a close contour and clear eyes. Daytime grass uses deeper greens and subdued ASCII texture so the young birds stand out; the extra contour fades away at night. Walking, swimming, diving, eating, preening, sleeping, hopping, dancing and quacking each animate from the shared rig. Visitors use the same visual language with their original names, eight personalities, plumage and signature accessories. The original event animators now reach Ultra: 737 animation recipes cover the 774 exported event records, including all 131 original event assets; 60 wildlife, human and vehicle silhouettes have new authored art.

Ultra has presentation art for **all 542 unique items across 11 live registries**, built from 221 hand-drawn ASCII silhouette families plus collectible cards, with material colors and discrete animation. Placed furniture and structures share depth ordering with characters; rugs remain underneath. Fountains, waterfalls, flames, portals, windmills, chimes and plants animate without accumulating trails. All 109 wearables from the shop, outfit system and seasonal wardrobe have fitted presentation art. Headwear scales to the age's head and follows pecks and turns; collars attach below the jaw, capes and bags attach at the shoulder, wings fold and beat, and boots and skates follow each foot. Each garment retains its own colors in combined outfits. Soft hats, scarves, capes, wings, pendants, helmet reflections and held props use separate animation patterns. Saved outfit and seasonal equipment now appear in Ultra; a shop selection wins a conflicting visual slot without modifying any wardrobe data. Clothes submerge with Cheese during a dive and freeze with Reduced Motion. Shop, inventory, crafting and building menus display the selected item's full-color preview using the original selection. The desktop shop exposes all ten existing categories, including structure, decoration, lighting and flooring. Prices, unlocks, item effects and purchase/use handlers remain in the original game.

**Item art** opens a searchable, paginated artwork catalog covering every item, including locked content. It is a preview library and never grants items or changes inventory. Category filters, item descriptions, rarity accents and a Pause animation control support inspection; typing in the catalog is isolated from game input. **Preview → Wearables on Cheese** switches the catalog to a fitted try-on view, with all nine ages, ten actions, both facing directions and Pause animation. It shows every wearable without granting or equipping anything. `engine/export_items.py` and `engine/export_wearables.py` regenerate metadata from the live Python definitions; parity tests catch registry drift.

**Lighting follows the actual game clock**, with a read-only time-of-day label in the toolbar. Daytime separates a clear blue sky, deep green grass and earthy paths, deep blue water with cool ripples, and shaded green or autumn-orange tree canopies. Trunks have their own brown shading, and a warm bank edge against a cool waterline defines the shoreline. Tree surfaces follow their ASCII silhouettes and restore cleanly as branches sway or the camera moves. Directional sunlight and dappled shade retain those material colors through weather, dusk and night. Weather, seasons and biomes tint the ambient light; caves retain their sheltered lighting. Dawn and dusk have warm horizons, and night shifts to cool moonlight. The emotion close-up and title portrait use the same clock and environment palette, with ASCII clouds, sun or moon and stars. Character interiors clear busy terrain ink using the local sky, land or water background instead of a fixed dark backing. Foreground daylight ink adapts for contrast, while grass texture keeps its quieter natural colors instead of being boosted toward cream. Highlights have narrow outlines, and bloom and shafts remain restrained to preserve detail. Ambient lighting stays active with Effects off. The former forced-time preference is retired and cleared on launch; rendering never advances time or changes gameplay.

**Effects: vivid / subtle / off** controls warm sun shafts, moonlight, selective bloom around emissive glyphs and items, water caustics, rain rings, motes and swimming wakes. Light is drawn before characters and UI so the ASCII ink stays sharp. The preference persists across relaunches. Reduced Motion freezes all effects, props and previews; particle and weather toggles remain respected. A small lighting buffer and bounded sprite caches keep effects inexpensive at Retina resolution.

During play, Ultra fills the entire client window with the living ASCII world, with no letterboxing or reserved sidebar. The emotion close-up and transcript float over the pond. Care meters and the hierarchy expand with **Care & menu**, the lower **Menu** button, or arrow-key navigation; Escape backs out and then collapses them. Window resizing and fullscreen keep the playfield edge to edge, while Text zoom changes the overlay scale.

Ultra includes an animated pond title screen, an ASCII logo, an expression-only emotion panel with animated eyes, brows, a duck bill and reaction marks for eight moods and care actions, care and trust meters, a scroll-following hierarchy, a persistent transcript, and experience/growth/goal readouts. The top-right panel has no head contour, crest, neck or clothing. It follows the original emotion action priority and keeps the time-of-day background. Shop, workshop, settings, exploration, journal, conversation, activity and warning panels have distinct ASCII illustrations and accents. Full menu text is captured before the terminal compositor truncates it, wrapped without losing characters, and wheel-scrollable when needed. Minigames retain their authored playfields inside the new arcade frame. Reduced Motion freezes portrait effects and High Contrast brightens UI labels and frames.

Keyboard controls are unchanged. The title choices, hierarchical side menu, lower action bar and panel navigation controls support mouse input. Stale clicks and clicks behind confirmations are rejected on the game thread; a click uses the same Enter handler as keyboard selection. Arrow keys and Enter navigate the complete game menu. Escape goes back; T opens conversation; Page Up/Down scroll conversation history. Display controls provide fullscreen, larger text with scrolling, Vivid/Subtle/Off scene effects, a searchable item art catalog and PNG screenshots. Every dialogue string is drawn as literal glyphs.

## The named guest cast (2.32.0)

All 40 regular friends and eight rare visitors have individual Ultra silhouettes,
plumage, proportions, fitted belongings, signature props and animated habits.
Named ducks use eleven head shapes and seven body constructions in individually
chosen combinations. Gerald, Professor Hoot, Corvus, Flutter and Grumble have
species-specific articulated rigs; Pip, the merchant and Sir Quackington have
their own duck designs. Rare visitors no longer use small event-sprite fallbacks.

The shared cast registry in `world/guest_cast.py` contains 432 authored lines:
greetings, returning greetings, topics, stories, personal confidences, activity
responses, gift responses and farewells. Existing conversation trees, friendship
gates, memories and rewards continue alongside the named voices. Run that module
to regenerate `client/guest-cast.mjs`; body/prop art is in `guest-shapes.mjs` and
animation is in `visitor-rig.mjs`. Cheese's approved D10 art and speech are unchanged.

Friends walk at individual speeds and pause for their habits. Rare guests wander
independently, face Cheese when acknowledged and walk away before departure.
Click a rare guest, or open Pond journal → Friends, to say hello, ask about their
adventures or keep them company. These use the existing friendship ledger, with
an eight-second interaction cooldown and no repeat gift rolls. Movement staging
is transient; friendship progress uses the original save system.

Validation: `npm test`, `../.venv/bin/python check_guests.py`,
`electron guests-visual.cjs`, the existing simulation parity/living-world checks,
and `npm run smoke`. The guest checks use disposable saves; visual checks exercise
all eight guest hit targets and journal actions against real simulation snapshots.
The complete offline review atlas can be rebuilt using
`electron designs/art-atlas/export.cjs`.

## Isolation and saves

- Worktree: `/Volumes/Expansion Pak/Projects/cheese-the-duck-ascii-engine`
- Branch: `codex/ascii-engine-port`, based on `aa5993f` from `nightly`.
- Development runtime: `engine/.runtime/`.
- Packaged app runtime: `~/Library/Application Support/Cheese the Duck ASCII Engine/`.
- Each runtime stores its own `saves/`, `screenshots/` and logs.
- On first normal launch, the existing `~/.cheese_the_duck` directory is copied into the new runtime if one exists. Later launches do not overwrite the copy. The original installation and saves are left intact.
- Tests always use disposable save directories. Original saves are never used by smoke tests.
- Loading and quitting now wait for queued saves. Writes capture their destination slot before entering the queue. Save failures are surfaced instead of silently closing.
- The terminal self-updater is disabled in this edition so it cannot overwrite the isolated engine branch.

## Development and build

From the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r engine/requirements-build.txt
npm --prefix engine ci
npm --prefix engine start
npm --prefix engine run dist
```

Local LLM support is optional, as in the original game. There is no GGUF model in this repository or the bundled app. Handwritten dialogue and the existing fallbacks run without it. To build with local inference, install `requirements-ai.txt` in `.venv`, supply a model through the existing model setup, and rebuild; the bundler detects and collects `llama_cpp`. Local-model inference itself has not been tested in this port because no model is installed. Radio still requires its original external stream/tools.

## Validation

```sh
CHEESE_SAVE_DIR="$PWD/engine/artifacts/test-saves" SDL_AUDIODRIVER=dummy .venv/bin/python -m pytest -q
.venv/bin/python engine/check_game.py
npm --prefix engine test
npm --prefix engine run smoke
npm --prefix engine run visual
.venv/bin/python engine/capture_interface.py
(cd engine && ./node_modules/.bin/electron interface-check.cjs)
CHEESE_ARTIFACTS="$PWD/engine/artifacts/packaged" \
  'engine/dist/mac-arm64/Cheese the Duck ASCII Engine.app/Contents/MacOS/Cheese the Duck ASCII Engine' --smoke
```

The parity harness checks 42 static menu actions, 21 locations, six diary tabs, four minigame lifecycles, uncensored keyboard editing, mouse-action routing, and save/reload of the complete 59-section save. It uses real game handlers and the new frame compositor. The Electron smoke tests exercise startup, a new game, input, drawing, screenshots, graceful shutdown and persisted JSON, in both source and frozen app builds. These checks do not simulate months of progression or every random event.

The visual harness checks nine animated biomes, pixel-identical Classic rendering, opaque dialogue preservation and switching back from Ultra. It also checks distinct NPC appearances and restoration of terrain after characters leave. It writes an original-versus-enhanced comparison, a Bedhead Bandit age sheet, character sheets, a gallery and individual world captures under `engine/artifacts/ultra/`. JavaScript tests exercise all seasons, weather, 28 expression/action states, growth, cosmetic/visitor visibility and reduced motion. Bedhead regression checks compare the live character against approved option B at all nine ages, check action routing, moods, mirrored cosmetics and stable foot placement, and validate every age/action combination with multiple equipped accessories. The design previews and the live game use the same sprite rig. The integration harness checks that all 21 real locations produce serializable live scene snapshots.

The November 9 native audio crash was caused by a sound worker using `pygame.Sound.play()` while the main thread closed the SDL mixer. Shutdown now blocks new mixer workers, cancels their waits, joins them, then closes SDL. Tests force that exact overlap and run 20 repeated shutdowns during SFX, WAV playback and crossfades. The desktop smoke test now fails on a nonzero subprocess exit or a termination signal, and checks that graphics preferences survive a renderer reload. Reload also resets frame acknowledgements and resends the current frame so transport cannot stall on an acknowledgement from the old page. Set `CHEESE_SMOKE_AUDIO=system` to exercise the system audio driver instead of the default silent dummy driver.

Testing also exposed and fixed the original diary's stale references to photos (now read from the scrapbook) and a load-versus-background-save race. Regression tests cover these fixes.

Reports and screenshots are generated in `engine/artifacts/`. Build products, runtime data, dependencies and test artifacts are ignored by Git.

The interface harness captures 77 real screens, including all ten shop categories, every static menu route, six settings categories, six diary tabs, confirmations, long dialogue, loading/offline summaries, celebration and item-interaction popups, and four minigames. It checks panel bounds, complete long text, scroll reachability, Reduced Motion, and Classic pixel parity. Screenshots and the contact sheet are in `engine/artifacts/interface/`. The smoke test also clicks the actual canvas title and care-menu choices through preload and IPC, then verifies keyboard navigation, dialogue, save JSON and clean simulation shutdown.

The item harness (`cd engine && ./node_modules/.bin/electron items-check.cjs`) renders all 542 artworks into contact sheets, checks live selected-item previews at three window sizes, verifies prop removal without trails and Reduced Motion, and measures a 100-prop scene. Artifacts are in `engine/artifacts/items/`. The smoke test also verifies catalog search/input isolation and persisted scene effects.

The wearable harness (`cd engine && ./node_modules/.bin/electron wearables-check.cjs`) generates all 109 fitted contact sheets, six combined outfits across eight actions, all ages and expression-only previews. Tests check clipping, age fit, eye visibility, independent garment colors, mirroring, animation, Reduced Motion and clean unequipping. The desktop smoke also exercises try-on controls and confirms they do not change equipment. Artifacts are in `engine/artifacts/wearables/`.


## Living pond overhaul

Open **Pond journal** (or **J** while outside a conversation), or click a placed object to inspect it. The journal has eight sections: habitat, Cheese’s plans, belongings, friends, weather, projects, field notes and memories. Classic remains available, and all original menus and progression systems remain playable.

Every one of the 542 catalogue items now has denser character-space construction, material detail and operating animations. Owned possessions retain condition, dirt, wetness, familiarity and use history. Objects must be reached before use; operations have preparation, activity and settling phases. Repairs require a twig and restore real crafted-tool durability. Food consumption and equipment changes continue through the original inventory/wardrobe so quantities and equipment stay authoritative. The 109 fitted wearables follow the new rig, including its tucked sleeping head.

Cheese’s extended planner weighs needs, weather, familiar and novel objects, learned routines and visitors. You can suggest an activity, choose a general preference, pause routines or cancel/resume a task. Thirteen practice skills, remembered experiences, friend schedules, trust/warmth/reliability and explicit promises persist. Recent lived experience is supplied to the existing conversation system. No external service or model download is required.

Seasonal, biome-weighted fronts have three-front forecasts. Rain waters the actual garden and wets outdoor items; heat stresses thirsty plants. Ground wetness, snow and ice linger. Soil, water level, clarity, flowers, insects, fish and birds interact. Fishing activity responds to habitat quality; catches, gardening and crafting feed memories and skills. Foraging depletes local patches that replenish over time in all nine biomes.

Six community projects each have three stages with validated material costs: reed beds, orchard, observatory, clubhouse, repair workshop and nature trail. Reed beds, the orchard and trail change habitat recovery. The observatory extends the forecast to five fronts and doubles field notes; the workshop speeds repairs and restores more real tool durability; the clubhouse improves shared social recovery. Kindness toward strangers builds persistent community warmth, reducing loneliness between visits. Eight branching stories introduce consequential choices: a lost duckling, frog choir, storm preparations, repair fair, migration, fireflies, picnic and an old bottle. Choice costs and effects are visible before selecting; stale clicks cannot repeat rewards. Cheese’s original dialogue is unchanged and uncensored.

The optional `living_pond` section is saved atomically with the original 59 sections. Old saves acquire defaults without losing existing data. In-progress activities pause on reload. Offline catch-up is capped at 48 hours and 192 environmental steps; it never manufactures inventory or action rewards. Journals and friend memories are bounded.

Validation: `node --test engine/tests/*.test.mjs`, `.venv/bin/python engine/check_living.py`, `.venv/bin/python engine/check_game.py`, and `cd engine && npm run smoke`. The new integration harness uses disposable saves, exercises ownership, arrival, cooldowns, project costs, original garden/tool/friend systems, all stories, save migration and a deterministic 72-hour habitat simulation. `cd engine && ./node_modules/.bin/electron overhaul-check.cjs` checks all event recipes and captures the cast, items, weather scenes and eight journal tabs under `engine/artifacts/overhaul/`.
