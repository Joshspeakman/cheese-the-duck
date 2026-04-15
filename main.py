#!/usr/bin/env python3
"""
Cheese the Duck - A Virtual Pet Game

A terminal-based Tamagotchi-style game featuring a cute but silly duck
with needs, moods, personality, and autonomous behavior.

Run with: python main.py
"""
import sys
import os

# Get the directory where main.py lives
GAME_DIR = os.path.dirname(os.path.abspath(__file__))

# Add the game directory to path for imports
sys.path.insert(0, GAME_DIR)


def _ensure_venv():
    """Re-execute with venv python if not already using it.

    This ensures llama-cpp-python is available for AI conversations.
    """
    venv_python = os.path.join(GAME_DIR, ".venv", "bin", "python")

    # Check if venv exists
    if not os.path.isfile(venv_python):
        return  # No venv, continue with current python

    # Check if we're already running from the venv by looking at sys.prefix
    # When running from venv, sys.prefix points to the venv directory
    venv_dir = os.path.join(GAME_DIR, ".venv")
    if os.path.realpath(sys.prefix) == os.path.realpath(venv_dir):
        return  # Already using venv

    # Re-execute with venv python
    os.execv(venv_python, [venv_python] + sys.argv)


# Ensure we're using the venv for AI support
_ensure_venv()

# Import logger
from game_logger import get_logger, shutdown_logger


# Model configuration - use user-writable location for system installs
def _get_model_dir():
    """Get model directory, using user home for system installs."""
    if GAME_DIR.startswith('/opt/') or GAME_DIR.startswith('/usr/') or GAME_DIR.startswith('/snap/'):
        # System install - use user's home directory
        user_model_dir = os.path.join(os.path.expanduser("~"), ".local", "share", "cheese-the-duck", "models")
        os.makedirs(user_model_dir, exist_ok=True)
        return user_model_dir
    else:
        # Local install - use game directory
        return os.path.join(GAME_DIR, "models")

MODEL_DIR = _get_model_dir()
RECOMMENDED_MODEL = {
    "name": "Llama 3.2 3B",
    "url": "https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q4_K_M.gguf",
    "filename": "Llama-3.2-3B-Instruct-Q4_K_M.gguf",
    "size_mb": 2000,
}


def _check_and_download_model():
    """Check if AI model exists, download if missing."""
    import glob
    import urllib.request

    # Check for any .gguf model
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR, exist_ok=True)

    existing_models = glob.glob(os.path.join(MODEL_DIR, "*.gguf"))
    if existing_models:
        return True  # Model already exists

    # No model found - download the recommended one
    print()
    print("=" * 60)
    print("  AI MODEL REQUIRED")
    print("=" * 60)
    print()
    print(f"  Downloading {RECOMMENDED_MODEL['name']} (~{RECOMMENDED_MODEL['size_mb']}MB)")
    print("  This enables AI-powered conversations with your duck!")
    print()

    filepath = os.path.join(MODEL_DIR, RECOMMENDED_MODEL["filename"])

    try:
        req = urllib.request.Request(
            RECOMMENDED_MODEL["url"],
            headers={"User-Agent": "Mozilla/5.0"}
        )

        with urllib.request.urlopen(req) as response:
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            chunk_size = 1024 * 1024  # 1MB

            with open(filepath, 'wb') as f:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break

                    f.write(chunk)
                    downloaded += len(chunk)

                    if total_size > 0:
                        pct = downloaded / total_size * 100
                        bar_len = 40
                        filled = int(bar_len * downloaded / total_size)
                        bar = "#" * filled + "-" * (bar_len - filled)
                        mb_done = downloaded / (1024 * 1024)
                        mb_total = total_size / (1024 * 1024)
                        sys.stdout.write(f"\r  [{bar}] {pct:5.1f}% ({mb_done:.0f}/{mb_total:.0f}MB)")
                        sys.stdout.flush()

        print()
        print()
        print("  Download complete!")
        print("=" * 60)
        print()
        return True

    except Exception as e:
        print(f"\n  Download failed: {e}")
        print("  The game will use pre-written responses instead.")
        print()
        # Clean up partial download
        if os.path.exists(filepath):
            os.remove(filepath)
        return False


def check_dependencies():
    """Check system requirements and offer to install missing packages.

    Returns True if all *required* dependencies are met (after any
    auto-install), False if the game cannot start.
    """
    import shutil
    import importlib
    import subprocess

    # ── Python version ────────────────────────────────────────────
    py_ver = sys.version_info
    if py_ver < (3, 9):
        print(f"\n  Python 3.9+ required (you have {py_ver.major}.{py_ver.minor})")
        print("  Please upgrade Python and try again.\n")
        return False

    # ── Python packages ───────────────────────────────────────────
    # (module_name, pip_name, required?)
    _PACKAGES = [
        ("blessed",         "blessed",          True),
        ("pygame",          "pygame",           True),
        ("markovify",       "markovify",        False),
        ("llama_cpp",       "llama-cpp-python", False),
    ]

    missing_required = []
    missing_optional = []

    for mod_name, pip_name, required in _PACKAGES:
        try:
            importlib.import_module(mod_name)
        except ImportError:
            if required:
                missing_required.append((mod_name, pip_name))
            else:
                missing_optional.append((mod_name, pip_name))

    # ── System tools (informational only) ─────────────────────────
    _TOOLS = [
        ("mpv",     "Radio streaming"),
        ("xclip",   "Clipboard copy (X11)"),
        ("xsel",    "Clipboard copy (X11 fallback)"),
        ("wl-copy", "Clipboard copy (Wayland)"),
        ("git",     "In-game updates"),
    ]

    missing_tools = []
    for tool, purpose in _TOOLS:
        if not shutil.which(tool):
            missing_tools.append((tool, purpose))

    # ── Nothing missing ───────────────────────────────────────────
    if not missing_required and not missing_optional and not missing_tools:
        return True

    # ── Report ────────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("  SYSTEM REQUIREMENTS CHECK")
    print("=" * 60)

    if missing_required:
        print()
        print("  Missing REQUIRED packages:")
        for mod, pip_name in missing_required:
            print(f"    ✗ {pip_name}")

    if missing_optional:
        print()
        print("  Missing optional packages:")
        for mod, pip_name in missing_optional:
            print(f"    - {pip_name}")

    if missing_tools:
        print()
        print("  Missing optional system tools:")
        for tool, purpose in missing_tools:
            print(f"    - {tool}  ({purpose})")

    # ── Offer to install Python packages ──────────────────────────
    all_missing_pip = missing_required + missing_optional
    if all_missing_pip:
        pip_list = " ".join(p for _, p in all_missing_pip)
        print()
        print(f"  Install missing Python packages? ({pip_list})")
        print()
        try:
            answer = input("  [Y] Yes  [N] No  > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            answer = "n"

        if answer in ("y", "yes", ""):
            print()
            pip_cmd = [sys.executable, "-m", "pip", "install"] + [p for _, p in all_missing_pip]
            print(f"  Running: {' '.join(pip_cmd)}")
            print()
            try:
                result = subprocess.run(pip_cmd, timeout=300)
                if result.returncode == 0:
                    print()
                    print("  ✓ Packages installed successfully!")
                    # Re-check required packages after install
                    for mod_name, pip_name in missing_required:
                        try:
                            importlib.import_module(mod_name)
                        except ImportError:
                            print(f"\n  ✗ {pip_name} still not importable after install.")
                            print("    Try manually: pip install " + pip_name)
                            print()
                            return False
                    missing_required = []
                else:
                    print(f"\n  ✗ pip exited with code {result.returncode}")
            except subprocess.TimeoutExpired:
                print("\n  ✗ Install timed out")
            except Exception as e:
                print(f"\n  ✗ Install failed: {e}")

    if missing_tools:
        print()
        print("  Tip: install missing system tools with your package manager")
        print("  e.g. sudo pacman -S mpv xclip git")

    print()
    print("=" * 60)
    print()

    if missing_required:
        print("  Cannot start — required packages are missing.")
        print("  Run:  pip install " + " ".join(p for _, p in missing_required))
        print()
        return False

    return True


def main():
    """Main entry point."""
    logger = None
    game = None

    try:
        # Initialize logger first
        logger = get_logger()
        logger.info("=" * 80)
        logger.info("GAME STARTING")
        logger.info("=" * 80)

        if not check_dependencies():
            logger.error("Missing dependencies")
            sys.exit(1)

        # Check for AI model, download if missing
        _check_and_download_model()

        from core.game import Game

        print("Starting Cheese the Duck...")
        logger.info("Initializing game...")
        game = Game()

        logger.info("Starting game loop...")
        game.start()

        logger.info("Game ended normally")

    except KeyboardInterrupt:
        print("\n\nQuitting Cheese the Duck. Goodbye!")
        if logger:
            logger.info("Game interrupted by user (Ctrl+C)")

    except Exception as e:
        error_msg = f"Fatal error in main: {e}"
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

        if logger:
            logger.critical(error_msg, exc_info=True)
            logger.log_exception(e, "Fatal error in main game loop")

    finally:
        # Clean up resources to prevent leaks
        try:
            from audio.sound import sound_engine
            sound_engine.shutdown()
        except Exception:
            pass
        try:
            from dialogue.llm_behavior import get_behavior_controller
            get_behavior_controller().shutdown()
        except Exception:
            pass
        try:
            if game and hasattr(game, '_talk_executor'):
                game._talk_executor.shutdown(wait=False)
        except Exception:
            pass
        if logger:
            logger.info("Shutting down logger...")
            shutdown_logger()


if __name__ == "__main__":
    main()
