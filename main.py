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
    if not check_dependencies():
        sys.exit(1)

    try:
        from core.game import Game

        print("Starting Cheese the Duck...")
        game = Game()
        game.start()

    except KeyboardInterrupt:
        print("\n\nQuitting Cheese the Duck. Goodbye!")
        sys.exit(0)

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
