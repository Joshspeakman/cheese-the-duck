# Cheese the Duck — ASCII Engine edition

This branch runs the full Cheese simulation in a custom desktop glyph engine, following Dead West Railway's Electron/custom-renderer architecture. The Python gameplay systems remain authoritative; the desktop frontend draws structured color glyph frames on a cached Canvas atlas. It does not launch a terminal, shell, PTY, or xterm.

Open **Play Cheese ASCII.command** in the repository root, or **engine/dist/mac-arm64/Cheese the Duck ASCII Engine.app**. The bundled macOS ARM64 app includes its Python runtime, gameplay modules, original music and sound effects. It needs no first-launch dependency download. The build has an ad-hoc signature for local use, not an Apple notarization for public distribution.

## What carries over

All original gameplay code and data remain: needs and care, growth, personality, trust and consequences, autonomous behavior, conversation and memory, learning, quests, friends, exploration, crafting, building, inventory and shop, fishing, gardening, weather, festivals, collectibles, decorations, tricks, titles, achievements, prestige, diaries, scrapbook, save slots and minigames. Cheese's authored dialogue, duck sprites, expressions, movement and interaction animations are preserved. The former content gate now passes text through unchanged, including profanity, in dialogue learning and memory.

The new renderer adds world-space terrain, animated water and grass, clouds, willows, pines, docks, ruins, flowers and boats across nine biomes. Original location scenery, items, actors, visitors and weather draw above this layer. It uses a larger character viewport, high-DPI glyph caching, changed-cell repainting, and a bounded latest-frame transport. It retains the original extended ASCII/Unicode borders and symbols.

Keyboard controls are unchanged. The lower action bar supports mouse input. Arrow keys and Enter navigate the complete game menu. Escape goes back; T opens conversation; Page Up/Down scroll conversation history. Display controls provide fullscreen, larger text with scrolling, optional glow and PNG screenshots. Every dialogue string is drawn as literal glyphs.

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
CHEESE_ARTIFACTS="$PWD/engine/artifacts/packaged" \
  'engine/dist/mac-arm64/Cheese the Duck ASCII Engine.app/Contents/MacOS/Cheese the Duck ASCII Engine' --smoke
```

The parity harness checks 42 static menu actions, 21 locations, six diary tabs, four minigame lifecycles, uncensored keyboard editing, mouse-action routing, and save/reload of the complete 59-section save. It uses real game handlers and the new frame compositor. The Electron smoke tests exercise startup, a new game, input, drawing, screenshots, graceful shutdown and persisted JSON, in both source and frozen app builds. These checks do not simulate months of progression or every random event.

Testing also exposed and fixed the original diary's stale references to photos (now read from the scrapbook) and a load-versus-background-save race. Regression tests cover these fixes.

Reports and screenshots are generated in `engine/artifacts/`. Build products, runtime data, dependencies and test artifacts are ignored by Git.
