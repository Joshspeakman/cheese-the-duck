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

During play, Ultra fills the entire client window with the living ASCII world, with no letterboxing or reserved sidebar. Floating pine-and-brass panels, a compact **Pond kit**, and an action belt keep the pond in view. Care meters and the hierarchy expand with **Care & menu**, the lower **Menu** button, or arrow-key navigation; Escape backs out and then collapses them. Window resizing and fullscreen keep the playfield edge to edge, while Text zoom changes the overlay scale.

Ultra includes an animated pond title screen, an ASCII logo, an expression-only emotion panel with animated eyes, brows, a duck bill and reaction marks for eight moods and care actions, care and trust meters, a scroll-following hierarchy, a persistent transcript, and experience/growth/goal readouts. The top-right panel has no head contour, crest, neck or clothing. It follows the original emotion action priority and keeps the time-of-day background. Shop, workshop, settings, exploration, journal, conversation, activity and warning panels have distinct ASCII illustrations and accents. Full menu text is captured before the terminal compositor truncates it, wrapped without losing characters, and wheel-scrollable when needed. Minigames retain their authored playfields inside the new arcade frame. Reduced Motion freezes portrait effects and High Contrast brightens UI labels and frames.

Classic keyboard controls are unchanged. In Ultra, Enter starts in-world chat when the game menu is collapsed. The title choices, hierarchical side menu, lower action bar and panel navigation controls support mouse input. Stale clicks and clicks behind confirmations are rejected on the game thread; a click uses the same Enter handler as keyboard selection. Arrow keys and Enter navigate the complete game menu. Escape goes back; T opens conversation; Page Up/Down scroll conversation history. Display controls provide fullscreen, larger text with scrolling, Vivid/Subtle/Off scene effects, a searchable item art catalog and PNG screenshots. Every dialogue string is drawn as literal glyphs.

## In-world pond chat (2.36.1)

Ultra's bottom-left log is now a live chat window. Press **Enter** while the game
menu is collapsed, **T**, or **Talk** to compose. **Enter** sends; **Escape** returns
to the pond and keeps an unfinished draft. Typing, selecting, pasting and using
clipboard shortcuts never trigger care/menu hotkeys. The simulation keeps running.

**General**, **Conversations** and **World** tabs separate the log without losing
messages. Names, timestamps and channel colors distinguish Cheese, your words,
visitors, nearby conversations and discoveries. Click a speaker's name to whisper.
Use `/s message` for Cheese, `/w Name message` for a present friend, `/r message`
for the last incoming whisper, and `/help` for reminders. `/clear` clears this view,
not saved memories. `//` begins a literal slash. Up/Down recall sent messages.

The **Say ▾** control chooses Cheese or a present visitor without a command.
It preserves the current draft. Use arrow keys and Enter in the recipient menu;
Escape closes the menu before leaving chat. **Tab** completes slash commands and
visitor names (`/w Ad`); repeated Tab or Shift+Tab cycles matching names. Ordinary
text retains normal Tab navigation. Whisper history keeps the listener's name
after they leave; an absent listener never silently redirects a draft to Cheese.

Scroll or use Page Up/Down to read history; new messages leave your place intact,
with **Latest** to return. The live stream keeps 240 entries; recent saved resident
conversations return on load. The grip moves the panel, its lower-right corner
resizes it, and both support arrow keys when focused. Layout persists. Close with
× and recover with Enter or Pond kit. Idle fading waits while you compose.

Chat fades after 14 seconds of silence; reading, typing and waiting for a reply
keep it visible. Incoming speech restores it. The 2.36.1 chat update was built
from the installed baseline on `codex/pond-chat-2.36.1` in the separate
`cheese-the-duck-chat-release` worktree and installed behind the desktop shortcut.
It includes the listener picker, completion, clearer memory attribution and a
bounded retry for wholly recycled replies. Real local conversation, preference
recall and shutdown saving passed; installed saves were preserved.

Host acknowledgments clear only accepted drafts. Busy/absent residents keep the
message editable, duplicate requests do not repeat learning, and a stale session
cannot send into a newly loaded world. Ordinary dialogue (including notebook
chat) never runs item commands merely because an item is mentioned. Replies use
the existing local language model and persistent resident memories; all text,
including profanity, is rendered literally.

Validation: `npm --prefix engine run test:chat` tests real game routing, memory,
whispers, duplicate rejection, Classic mirroring and save/reload. `npm --prefix
engine run visual:chat` checks real keyboard/pointer input, scrollback, drafts,
channel tabs, drag/resize, idle fade and Classic behavior. Packaged smoke exercises
the inline form through IPC, actual local inference and shutdown saving.

## Local voices and learning residents (2.35.0)

Open **Pond kit → Pond journal → Personalities**, choose Cheese or a visitor,
and talk in the notebook. Friends also have a **Talk & get to know** button.
**T** opens the in-world chat in Ultra; Classic retains the original talk screen.
Both use the local voice model and Cheese's original quest/memory hooks.
Enter sends; the notebook additionally supports Shift+Enter for a new line.
The notebook preserves unfinished drafts while the simulation runs.

Every met resident has an independent persistent contextual action model,
core temperament, gradually changing traits, interests, personal intentions,
episodic memories, remembered player statements and directional relationships.
Actual care, completed activities, conversation, shared time and kept/missed
promises supply experiences. The small models update normalized linear weights
online; those predictions affect Cheese's utility planner and visitor routines.
Temperament also influences guests' pace and pauses while they roam freely.
**I liked that / Try a different approach** gives bounded feedback about the
most recent experience. It does not directly award friendship or currency.

Nearby residents can initiate and answer one another, remember the exchange,
and develop relationships. Lingering over a shared interest can teach both
participants; leaving cancels an unfinished shared activity. Familiarity and
feelings influence whom they approach conversationally. Each keeps separate
memories, so telling one character something does not magically tell everyone.
Direct visitor conversations advance the original friendship system once per
visit, without rolling gifts. The notebook shows memories, interests, goals,
relationship changes and the experiences behind gradual personality growth.

One shared **Qwen3-4B Q4_K_M** language model generates their speech using their
individual state and authored voices. Its neural weights are fixed; the small
behavior models, preferences and memories learn as you play. Inference runs on
this Mac through the bundled ARM64/Metal llama.cpp runtime. There is no cloud
API or ongoing model download. Generated speech cannot execute game commands,
change inventory, grant rewards, or become an authoritative game fact. Original
uncensored dialogue remains available if inference is unavailable; that state is
shown in the notebook. New memories live under the optional `living_pond.minds`
save section, preserving original save compatibility. Offline catch-up never
fabricates conversations or trains these models on invented encounters.

For a fresh development machine, run `npm --prefix engine run setup:voice`
before building. This explicit setup downloads and verifies the pinned assets:

- Model: [official Qwen3-4B GGUF](https://huggingface.co/Qwen/Qwen3-4B-GGUF),
  revision `bc640142c66e1fdd12af0bd68f40445458f3869b`, Apache 2.0.
- Runtime: [llama.cpp b12255](https://github.com/ggml-org/llama.cpp/releases/tag/b12255),
  official macOS ARM64 release, MIT.
- Weights: `~/Library/Application Support/Cheese the Duck ASCII Engine/local-ai/`
  (2.50 GB decimal), retained across application updates.
- Runtime build assets: ignored `engine/build/local-ai/`; the executable and
  libraries are copied into the signed app. License texts are in `engine/licenses`.

`setup_voice.py` pins both SHA-256 checksums, verifies existing downloads, and
extracts native code atomically to fresh files. It does not replace running
signed executables in place. The application starts an authenticated loopback
server on an ephemeral port and stops it with the simulation. One inference
request per character conversation is outstanding; stale replies are discarded.
Long responses are bounded and all output is rendered as literal text.

Validation: `npm --prefix engine run test:brains` exercises learning differences,
actual care and plan completion, neighbor exchanges, individual memory, original
friendship credit, anti-farming guards, save/reload and unavailable-model fallback.
`engine/brains-check.cjs` checks the actual notebook, draft preservation, keyboard
isolation, target IDs, literal output, feedback and resize. `CHEESE_SMOKE_AI=1`
extends the regular packaged smoke test with genuine local inference through
both talk controls, learned preference persistence, and clean shutdown. Test
saves and evidence are isolated under temporary directories / `engine/artifacts`.

## Independent visitors and shaped clothes (2.34.0)

The duckling in **A very small visitor** now uses the detailed, articulated guest
rig, with fitted scarf and toy, in both the world and the journal. Click the story
participant to open its encounter. Story actors have simulation-owned world
positions: living participants explore and pause; objects stay at their encounter
sites. Moving Cheese no longer drags the encounter along. Regular and rare guests
choose routes across the habitat, with occasional social stops. Unfinished story
chapters now restore correctly after loading.

The two sweaters and two Hawaiian shirts follow each age's posed torso contours.
Fabric has its own color and shading, shaped necklines and hems, knit or floral
details, and exposed wings. The cut follows walking, pecking, swimming, sleeping
and flapping; raised feet remain visible instead of disappearing under the hem.

`../.venv/bin/python check_guests.py` exercises independent movement, story staging,
removal and actual save/load, then exports disposable scenes for `npm run test:stories`.
The latter checks world click targets, story portraits and original choice commands.
`electron wearables-check.cjs` includes a focused shirt/knit sheet alongside the
complete wardrobe, motion and restoration checks.

## A quieter, movable interface (2.33.0)

After 60 seconds without mouse or keyboard activity, Ultra's controls fade over
1.8 seconds while the pond keeps running and animating. Move the mouse or press a
key to bring them back; a waking click or key is consumed so it cannot activate a
hidden action. Conversations, confirmations, minigames, open journals and artwork
catalogs remain visible. Reduced Motion makes the transition instant.

Drag panel titles to move them, and use their **×** to close individual sections.
The action belt has a grip at its top; the small Cheese heading moves the Pond kit.
**Pond kit**, or **F2**, opens switches for all eight sections, layout presets and
the idle-fade preference. A small recovery button remains available if the kit
itself is closed. **Reset layout** restores the starting arrangement. Positions
and visibility survive relaunches, with positions clamped inside resized windows.
Focused drag handles also support arrow keys; Shift increases the movement step.

Game windows, the parchment field notebook and the item-art cabinet can be moved
by their headings. Original keyboard navigation, gameplay commands and literal
dialogue are preserved. Classic retains its original rendering.

The HUD harness runs the real frontend against disposable simulation snapshots:
`npm run test:hud` (after `../.venv/bin/python capture_interface.py`). It checks
dragging, independent visibility, reopening, layout persistence, resizing,
overlapping hit targets, dialog input protection, wake handling, continued world
animation and an actual one-minute idle interval. Reports and screenshots are in
`artifacts/hud/`.

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

Resident speech uses the local Qwen3 model and llama.cpp runtime described above. On a fresh development machine, run `npm --prefix engine run setup:voice` before building. Model weights stay in Application Support across application updates; they are not committed to the repository. Actual local inference, conversation memory and shutdown saving have been exercised through the desktop chat. Authored dialogue remains available when the local model is unavailable. Radio still requires its original external stream/tools.

The next animation milestone is in development on this branch and has **not**
replaced the installed game; the separate chat update is installed as 2.36.1. Its tracker is
`overhaul/animation-milestone/requirements.json`: 219 of 542 object drawings have
been reconstructed, with 323 remaining. The full 48 bespoke sequences per object
and all guest/age/context coverage remain unfinished.

The lighting work adds 27 distinct constructions, from pleated lanterns and
glazed lamps to mirrored disco balls and carved crystal lights. Each placed copy
keeps its own **At dusk / On / Off** setting. Click it, open Belongings, and choose
a mode; Cheese must walk over and work its control. Cancelling before contact
leaves the switch alone. Cancelling after contact keeps the physical change but
does not award a completed use. Storage preserves the setting. Fireflies follow
their own dusk/season rhythm, the eternal flame stays lit, and rain dampens exposed
flames. Young Cheese watches open flames without operating their controls.

The ten initial light routines and fitted contact tools are foundations for the
larger repertoire. Visitor light participation, physical tool pickup/put-away
and the full per-object repertoire are still pending. Illumination follows the
actual bulb locations underneath sharp ASCII; cloth warms locally without
bleaching ceramic, wood or daytime terrain. The light meter updates during use.

Lighting validation uses `.venv/bin/python engine/check_lighting.py`,
`engine/node_modules/.bin/electron engine/lighting-check.cjs` and
`engine/node_modules/.bin/electron engine/lighting-ui-check.cjs`. The UI check
routes real notebook controls through the production command validator into an
isolated game process, including duplicate selection, cancellation and storage.

The keepsake work reconstructs twelve storage, reading and display objects. Chest
lids, woven baskets, glass frames, folded cards, rolled maps and the eight-page
**Elder Quacks** book have material surfaces and native contact poses. A page
turn persists when it happens; cancelling afterward keeps the page without
awarding a finished reading session. Bookmarks, careful sorts, collected
rainwater and frozen water survive saves. Duplicate chests retain independent
histories. The Belongings notebook shows live pages and rainwater levels.

Natural conversation receives the actual open chapter or card words from the
same definitions used to draw them. Cheese cannot read through a closed cover or
inspect a barrel before arriving. These descriptions never grant treasure or
invent a photograph's history. Nineteen shared reading/sorting cores are an
initial repertoire. Fifteen additional shared scenes let an independently moving
friend join Cheese for a page, map, card, photograph, chest or rain-gauge study.
Cheese waits briefly for arrival. Pausing holds both poses; a missed invitation,
interruption, moved object or replaced visit cannot award shared learning.
Completed sessions teach both residents and retain words they actually had time
to read. Visitors remain clickable at their drawn positions and return to their
own routines afterward. Young, older and nighttime readers choose different
scenes; butterflies hover instead of using a pointer.

These shared cores are not 48 bespoke sequences per object. Construction-specific
repertoires, personality-specific visitor acting, guest-to-guest keepsake sessions,
physical tool pickup/put-away, portable physical-copy handling and the complete
per-object sequence audits remain unfinished.

Keepsake checks: `.venv/bin/python engine/check_keepsakes.py`,
`engine/node_modules/.bin/electron engine/keepsakes-check.cjs` and
`engine/node_modules/.bin/electron engine/keepsakes-ui-check.cjs`. They use
isolated saves and exercise real notebook commands, contact timing, cancellation,
copy identity, weather, save/load and conversation context.
Shared reading uses `.venv/bin/python engine/check_keepsake_company.py` and
`engine/node_modules/.bin/electron engine/keepsake-company-check.cjs`, with
actual regular, rare and story movement, all-cast pose sheets, native replays,
selectable visitor bounds and interrupted/paused/cancelled sessions.

The creative props now reconstruct the brass telescope, painting easel, stitched
kite and actual paper-plane design. Twenty-seven native action cores handle
focusing, cap checks, progressive painting, launch/low arcs/gusts/reel-in, tail
care and paper creases. The easel accumulates twelve saved painting layers rather
than looping a decorative animation. Each physical copy has its own controls and
history; stopping midway keeps actual brush marks without a completion reward.
A weather change brings an airborne kite down from its current height. Canvas and
paper covers are removed by another physical action when dry weather returns.
The paper-plane design stays the original material; practising never creates or
consumes inventory. Belongings and natural chat receive the actual state.

Creative company now adds thirteen complementary tracks: a visitor walks to a
fixed meeting point, then poses beside the easel, helps with a kite or paper
fold, or watches the telescope session. Confidence, young/elder company, wind
and night change their role. Butterfly visitors observe without handling tools.
Cheese retains ownership of every physical control; a helper never duplicates
inventory, rewards or item uses. Both brains remember only completed shared time
and observations that actually occurred. Natural conversation reports whether
the partner is still approaching, working, paused or finished. Cancellation,
departure, replacement visits, moved objects and weather withdrawal release the
visitor back to independent movement. Reservations do not survive save/load.

Viewing stairs and painting decks are fixed to the prop and neutral body size.
Cheese walks onto their actual treads; they no longer follow his current height
or brush target. Bodies and short legs keep their original scale. Creative
visitors remain independently selectable at their rendered position.

These are initial repertoires, not 48 sequences per object. Personal visitor
choreography, guest-to-guest invitations, telescope handoffs, physical tool
pickup/put-away, unfolded practice-paper handling, full mood/season variants and
the individual sequence audits remain open. Tests use
`.venv/bin/python engine/check_creative.py`,
`.venv/bin/python engine/check_creative_company.py`,
`engine/node_modules/.bin/electron engine/creative-check.cjs`,
`engine/node_modules/.bin/electron engine/creative-company-check.cjs` and
`engine/node_modules/.bin/electron engine/creative-ui-check.cjs`. The last routes
actual notebook actions through the command validator into a disposable game.

The textile work reconstructs thirteen mats, rugs, living ground patches and
fibre materials. Knotted borders, tatami grain, coir loops, rubber drainage,
patchwork seams, moss cushions, layered batting and tied reeds have separate
ASCII constructions. Twenty-eight initial native action cores handle rolling,
unfolding, fringe combing, brushing, stepping, resting, wiping feet, draining,
checking frost and sorting fibres. Folds, impressions and contact changes are
saved on the physical copy. Cancelling preserves work already done without
awarding a completed use; rain protection starts from the actual rolled edge.

Young Cheese takes small steps, elders settle gently, and darkness, moisture,
frost and dirt affect what he chooses. Handling fabric or thatch keeps the
original inventory and never claims a crafting or building repair occurred.
Belongings updates the current material state while natural chat receives only
what Cheese can actually inspect. Eggs cannot operate these materials.

Eighteen complementary company tracks let an independently arriving visitor
steady a roll, separate fringe, brush lint, hold reeds, guide small steps or
settle beside the mat. Confidence changes how a visitor reacts to rug patterns;
young and elder company gets a patient guide, while butterflies hover without
tools. Helpers step close to the seam and keep their original body size. Brush
and fringe contacts affect the selected copy when they occur, including if the
session is later cancelled. Completed shared time teaches both residents once;
missed invitations, new visits, departures, direct care and bad weather do not.

Natural conversation receives the actual shared activity and material state only
after arrival. Visitors can remember the welcome mat greeting after seeing it,
not while walking toward it. Paused work freezes both characters. Loading a save
retains material changes and releases old visitor reservations. Visitors remain
clickable and return to independent movement afterward.

These are initial shared cores. Individual visitor/material-specific repertoires,
guest-to-guest sessions, physical tool pickup/put-away, all mood/season variants
and the 48-sequence audit for every object remain open. Textile checks use
`.venv/bin/python engine/check_textiles.py`,
`engine/node_modules/.bin/electron engine/textiles-check.cjs` and
`engine/node_modules/.bin/electron engine/textiles-ui-check.cjs`. They exercise
real game state and notebook commands with disposable saves, plus native-frame
replays and fixed-scale contact poses across all eight hatched ages.
Shared textile validation uses `.venv/bin/python engine/check_textile_company.py`
and `engine/node_modules/.bin/electron engine/textile-company-check.cjs`, with
actual regular/rare/story arrivals, contact timing, both brains, native replay
and all 48 visitor rigs.

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

Open **Pond journal** (or **J** while outside a conversation), or click a placed object to inspect it. The journal has ten sections: habitat, Cheese’s plans, personalities, belongings, arrangement, friends, weather, projects, field notes and memories. Classic remains available, and all original menus and progression systems remain playable.

Every one of the 542 catalogue items now has denser character-space construction, material detail and operating animations. Owned possessions retain condition, dirt, wetness, familiarity and use history. Objects must be reached before use; operations have preparation, activity and settling phases. Repairs require a twig and restore real crafted-tool durability. Food consumption and equipment changes continue through the original inventory/wardrobe so quantities and equipment stay authoritative. The 109 fitted wearables follow the new rig, including its tucked sleeping head.

Cheese’s extended planner weighs needs, weather, familiar and novel objects, learned routines and visitors. You can suggest an activity, choose a general preference, pause routines or cancel/resume a task. Thirteen practice skills, remembered experiences, friend schedules, trust/warmth/reliability and explicit promises persist. Recent lived experience is supplied to the existing conversation system. No external service or model download is required.

Seasonal, biome-weighted fronts have three-front forecasts. Rain waters the actual garden and wets outdoor items; heat stresses thirsty plants. Ground wetness, snow and ice linger. Soil, water level, clarity, flowers, insects, fish and birds interact. Fishing activity responds to habitat quality; catches, gardening and crafting feed memories and skills. Foraging depletes local patches that replenish over time in all nine biomes.

Six community projects each have three stages with validated material costs: reed beds, orchard, observatory, clubhouse, repair workshop and nature trail. Reed beds, the orchard and trail change habitat recovery. The observatory extends the forecast to five fronts and doubles field notes; the workshop speeds repairs and restores more real tool durability; the clubhouse improves shared social recovery. Kindness toward strangers builds persistent community warmth, reducing loneliness between visits. Eight branching stories introduce consequential choices: a lost duckling, frog choir, storm preparations, repair fair, migration, fireflies, picnic and an old bottle. Choice costs and effects are visible before selecting; stale clicks cannot repeat rewards. Cheese’s original dialogue is unchanged and uncensored.

The optional `living_pond` section is saved atomically with the original 59 sections. Old saves acquire defaults without losing existing data. In-progress activities pause on reload. Offline catch-up is capped at 48 hours and 192 environmental steps; it never manufactures inventory or action rewards. Journals and friend memories are bounded.

Validation: `node --test engine/tests/*.test.mjs`, `.venv/bin/python engine/check_living.py`, `.venv/bin/python engine/check_game.py`, and `cd engine && npm run smoke`. The new integration harness uses disposable saves, exercises ownership, arrival, cooldowns, project costs, original garden/tool/friend systems, all stories, save migration and a deterministic 72-hour habitat simulation. `cd engine && ./node_modules/.bin/electron overhaul-check.cjs` checks all event recipes and captures the cast, items, weather scenes and eight journal tabs under `engine/artifacts/overhaul/`.
