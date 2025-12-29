#!/usr/bin/env python3
"""
Cheese the Duck - A Virtual Pet Game

A terminal-based Tamagotchi-style game featuring a cute but silly duck
with needs, moods, personality, and autonomous behavior.

Run with: python main.py
"""
import sys
import os

# Add the game directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import logger
from game_logger import get_logger, shutdown_logger


def check_dependencies():
    """Check that required dependencies are installed."""
    try:
        import blessed
        return True
    except ImportError:
        print("Missing required dependency: blessed")
        print("")
        print("Install it with:")
        print("  pip install blessed")
        print("")
        print("Or install all requirements:")
        print("  pip install -r requirements.txt")
        return False


def main():
    """Main entry point."""
    logger = None

    try:
        # Initialize logger first
        logger = get_logger()
        logger.info("=" * 80)
        logger.info("GAME STARTING")
        logger.info("=" * 80)

        if not check_dependencies():
            logger.error("Missing dependencies")
            sys.exit(1)

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
        sys.exit(0)

    except Exception as e:
        error_msg = f"Fatal error in main: {e}"
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

        if logger:
            logger.critical(error_msg, exc_info=True)
            logger.log_exception(e, "Fatal error in main game loop")

        sys.exit(1)

    finally:
        # Always shutdown logger
        if logger:
            logger.info("Shutting down logger...")
            shutdown_logger()


if __name__ == "__main__":
    main()
