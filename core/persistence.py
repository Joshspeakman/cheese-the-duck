"""
Save/load system for game persistence using JSON.

Version History:
- 1.0: Original save format
- 2.0: Added duck_brain (player model, conversation memory, questions)
"""
import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from config import SAVE_DIR, SAVE_FILE

# Current save version - increment when save structure changes
SAVE_VERSION = "2.0"


class SaveManager:
    """Handles saving and loading game state to JSON files."""

    def __init__(self, save_path: Optional[Path] = None):
        self.save_path = save_path or SAVE_FILE
        self._ensure_save_dir()

    def _ensure_save_dir(self):
        """Create save directory if it doesn't exist."""
        self.save_path.parent.mkdir(parents=True, exist_ok=True)

    def save_exists(self) -> bool:
        """Check if a save file exists."""
        return self.save_path.exists()

    def save(self, data: dict) -> bool:
        """
        Save game data to JSON file.

        Args:
            data: Game state dictionary to save

        Returns:
            True if save successful, False otherwise
        """
        try:
            # Add metadata
            save_data = {
                "version": SAVE_VERSION,
                "saved_at": datetime.now().isoformat(),
                **data,
            }

            # Write atomically using temp file
            # Resolve paths to absolute to avoid pathlib rename bugs
            save_path_resolved = self.save_path.resolve()
            temp_path = save_path_resolved.with_suffix(".tmp")
            bak_path = save_path_resolved.with_suffix(".bak")

            # Remove existing temp file if crashed save left one behind
            if temp_path.exists():
                temp_path.unlink()

            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)

            # Backup current save before replacing
            if save_path_resolved.exists():
                try:
                    save_path_resolved.replace(bak_path)
                except OSError:
                    pass  # Best-effort backup

            # Rename temp to actual save file (atomic on most systems)
            try:
                temp_path.replace(save_path_resolved)
            except OSError as rename_error:
                # Try to restore backup if rename failed
                if bak_path.exists():
                    try:
                        bak_path.replace(save_path_resolved)
                    except OSError:
                        pass
                print(f"Warning: Could not complete atomic save: {rename_error}")
                # Clean up orphaned temp file
                if temp_path.exists():
                    try:
                        temp_path.unlink()
                    except OSError:
                        pass
                return False
            
            return True

        except (IOError, OSError, TypeError) as e:
            print(f"Save failed: {e}")
            return False

    def load(self) -> Optional[dict]:
        """
        Load game data from JSON file.
        Falls back to .bak if main save is corrupted.
        Cleans up orphaned .tmp files.

        Returns:
            Game state dictionary or None if load fails
        """
        save_path_resolved = self.save_path.resolve()
        temp_path = save_path_resolved.with_suffix(".tmp")
        bak_path = save_path_resolved.with_suffix(".bak")

        # Clean up orphaned temp files from crashed saves
        if temp_path.exists():
            try:
                temp_path.unlink()
            except OSError:
                pass

        # Try main save first
        data = self._try_load_file(self.save_path)
        if data is not None:
            return self._migrate_save(data)

        # Fall back to backup
        if bak_path.exists():
            print("Main save corrupted, loading backup...")
            data = self._try_load_file(bak_path)
            if data is not None:
                return self._migrate_save(data)

        return None

    def _try_load_file(self, path: Path) -> Optional[dict]:
        """Try to load and parse a JSON save file."""
        if not path.exists():
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (IOError, OSError, json.JSONDecodeError) as e:
            print(f"Load failed for {path.name}: {e}")
            return None
    
    def _migrate_save(self, data: dict) -> dict:
        """Migrate old save formats to current version."""
        version = data.get("version", "1.0")
        
        # Migrate from 1.0 to 2.0 (add duck_brain)
        if version == "1.0":
            # Add empty duck_brain structure for migration
            if "duck_brain" not in data:
                data["duck_brain"] = None  # Will be initialized fresh
            
            data["version"] = "2.0"
        
        return data

    def delete_save(self) -> bool:
        """Delete the save file."""
        try:
            if self.save_exists():
                self.save_path.unlink()
            return True
        except OSError:
            return False

    def get_save_info(self) -> Optional[dict]:
        """Get basic info about save without loading full data."""
        data = self.load()
        if not data:
            return None

        duck = data.get("duck", {})
        return {
            "name": duck.get("name", "Unknown"),
            "stage": duck.get("growth_stage", "unknown"),
            "last_played": data.get("last_played", "unknown"),
            "days_alive": data.get("statistics", {}).get("days_alive", 0),
        }


def create_new_save(duck_name: str) -> dict:
    """
    Create a fresh save data structure for a new duck.

    Args:
        duck_name: Name for the new duck

    Returns:
        Complete save data dictionary
    """
    now = datetime.now().isoformat()

    return {
        "version": SAVE_VERSION,
        "duck": {
            "name": duck_name,
            "created_at": now,
            "growth_stage": "hatchling",
            "growth_progress": 0.0,
            "needs": {
                "hunger": 80,
                "energy": 100,
                "fun": 70,
                "cleanliness": 100,
                "social": 60,
            },
            "personality": {
                "clever_derpy": -30,
                "brave_timid": 0,
                "active_lazy": 20,
                "social_shy": 30,
                "neat_messy": -20,
            },
            "current_action": None,
            "mood_history": [],
        },
        "last_played": now,
        "inventory": [],
        "statistics": {
            "days_alive": 0,
            "times_fed": 0,
            "times_played": 0,
            "times_cleaned": 0,
            "times_petted": 0,
            "conversations": 0,
        },
        # New in v2.0: Duck Brain for persistent memory
        "duck_brain": None,  # Will be initialized by game
    }


# Global save manager instance
save_manager = SaveManager()
