# Cheese the Duck — ASCII Engine edition

This branch runs the full Cheese simulation in a custom desktop glyph engine, following Dead West Railway's Electron/custom-renderer architecture. The Python gameplay systems remain authoritative; the desktop frontend draws structured color glyph frames on a cached Canvas atlas. It does not launch a terminal, shell, PTY, or xterm.

Open **Play Cheese ASCII.command** in the repository root, or **engine/dist/mac-arm64/Cheese the Duck ASCII Engine.app**. The bundled macOS ARM64 app includes its Python runtime, gameplay modules, original music and sound effects. It needs no first-launch dependency download. The build has an ad-hoc signature for local use, not an Apple notarization for public distribution.

## What carries over

All original gameplay code and data remain: needs and care, growth, personality, trust and consequences, autonomous behavior, conversation and memory, learning, quests, friends, exploration, crafting, building, inventory and shop, fishing, gardening, weather, festivals, collectibles, decorations, tricks, titles, achievements, prestige, diaries, scrapbook, save slots and minigames. Cheese's authored dialogue, duck sprites, expressions, movement and interaction animations are preserved. The former content gate now passes text through unchanged, including profanity, in dialogue learning and memory.

The **Graphics: Ultra / Classic** button switches instantly and remembers your choice. **Classic** is the original engine presentation, preserved pixel for pixel. **Ultra** is the default: a 240 × 112 ASCII world (26,880 character cells), with layered landscapes, etched tree canopies, willow fronds, water reflections, ripples, lily pads, fish, clouds, birds, butterflies, fireflies, seasonal foliage and animated weather. Daylight and moonlight change the palette. Landmarks distinguish the nine biomes and 21 locations: waterfalls, palms, windmills, flower arches, vegetable rows, cabins, ruins, crystal caverns, a fountain and underground storm-drain arches.

Cheese uses the selected **scruffy option B** design: swept floppy feathers, a round body, a scruffy folded wing and expressive side-eye. All nine growth stages have distinct drawings, from egg and hatchling through mature, elder and legendary. The shared character rig animates planted and lifted feet, body dips, delayed crest motion, wingbeats, pecking and chewing, swimming and diving, hops, preening, quacking, sleep and dancing. Live care and movement states trigger these poses; moods, facing direction, equipped cosmetics and Reduced Motion still apply. The foot anchor keeps the body grounded without adding a second world-space bob or jump. The eight NPC redraws keep the original personalities, faces and signature accessories, adding details such as an explorer compass and pack, glasses and an opening book, beret and paintbrush, spinning propeller, hood and mask, wrapped gift, chef hat and apron, and running shoes. Original NPC animation frames drive facial expressions and prop actions. Characters use clear ASCII contours and open interiors on their own layer above the dense scenery, with readable names and a small color palette. The terrain is restored before each character frame so movement leaves no trails. Growth, facing, movement, cosmetics, placed objects and visitors come from the live simulation. The game still owns every menu action, dialogue string and minigame. Ultra now also provides the desktop interface described below; Classic continues to use the original glyph compositor. Reduced Motion, animation, particle and weather preferences are respected. Worlds use printable ASCII; the original UI retains its extended ASCII/Unicode symbols. High-DPI glyph caching, changed-cell repainting and bounded frame transport keep drawing responsive.

Ultra has presentation art for **all 542 unique items across 11 live registries**, built from 221 hand-drawn ASCII silhouette families plus collectible cards, with material colors and discrete animation. Placed furniture and structures share depth ordering with characters; rugs remain underneath. Fountains, waterfalls, flames, portals, windmills, chimes and plants animate without accumulating trails. Equipped hats, scarves, glasses, headphones, wings, halos and backpacks follow Cheese's pose. Shop, inventory, crafting and building menus display the selected item's full-color preview using the original selection. The desktop shop exposes all ten existing categories, including structure, decoration, lighting and flooring. Prices, unlocks, item effects and purchase/use handlers remain in the original game.

**Item art** opens a searchable, paginated artwork catalog covering every item, including locked content. It is a preview library and never grants items or changes inventory. Category filters, item descriptions, rarity accents and a Pause animation control support inspection; typing in the catalog is isolated from game input. `engine/export_items.py` regenerates metadata directly from the live Python definitions, and a parity test catches registry drift.

**Effects: vivid / subtle / off** controls warm sun shafts, moonlight, selective bloom around emissive glyphs and items, water caustics, rain rings, motes and swimming wakes. Light is drawn before characters and UI so the ASCII ink stays sharp. The preference persists across relaunches. Reduced Motion freezes all effects, props and previews; particle and weather toggles remain respected. A small lighting buffer and bounded sprite caches keep effects inexpensive at Retina resolution.

During play, Ultra fills the entire client window with the living ASCII world, with no letterboxing or reserved sidebar. The emotion close-up and transcript float over the pond. Care meters and the hierarchy expand with **Care & menu**, the lower **Menu** button, or arrow-key navigation; Escape backs out and then collapses them. Window resizing and fullscreen keep the playfield edge to edge, while Text zoom changes the overlay scale.

Ultra includes an animated pond title screen, an ASCII logo, a duck-shaped emotion close-up with a broad bill, swept feathers and a tapered neck with eight moods and care-action expressions, care and trust meters, a scroll-following hierarchy, a persistent transcript, and experience/growth/goal readouts. The top-right emotion panel follows the original close-up action priority rather than the world movement pose. Shop, workshop, settings, exploration, journal, conversation, activity and warning panels have distinct ASCII illustrations and accents. Full menu text is captured before the terminal compositor truncates it, wrapped without losing characters, and wheel-scrollable when needed. Minigames retain their authored playfields inside the new arcade frame. Reduced Motion freezes portrait effects and High Contrast brightens UI labels and frames.

Keyboard controls are unchanged. The title choices, hierarchical side menu, lower action bar and panel navigation controls support mouse input. Stale clicks and clicks behind confirmations are rejected on the game thread; a click uses the same Enter handler as keyboard selection. Arrow keys and Enter navigate the complete game menu. Escape goes back; T opens conversation; Page Up/Down scroll conversation history. Display controls provide fullscreen, larger text with scrolling, Vivid/Subtle/Off scene effects, a searchable item art catalog and PNG screenshots. Every dialogue string is drawn as literal glyphs.

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
