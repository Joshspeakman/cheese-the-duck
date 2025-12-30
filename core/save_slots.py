"""
Save Slots System - Multiple save file management.
Allows players to have multiple save files with different ducks.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import json
import os
import shutil


@dataclass
class SaveSlotInfo:
    """Information about a save slot."""
    slot_id: int
    is_empty: bool = True
    duck_name: str = ""
    level: int = 1
    playtime_minutes: int = 0
    coins: int = 0
    created_at: str = ""
    last_played: str = ""
    prestige_level: int = 0
    achievements_count: int = 0
    mood: str = "happy"
    preview_ascii: List[str] = field(default_factory=list)


class SaveSlotsSystem:
    """
    System for managing multiple save slots.
    """
    
    MAX_SLOTS = 5
    
    def __init__(self, save_dir: str = "~/.cheese_the_duck"):
        self.save_dir = Path(save_dir).expanduser()
        self.save_dir.mkdir(parents=True, exist_ok=True)
        
        self.current_slot: int = 1
        self.slots: Dict[int, SaveSlotInfo] = {}
        
        # Initialize slot info
        self.refresh_slots()
    
    def get_save_path(self, slot_id: int) -> Path:
        """Get the save file path for a slot."""
        if slot_id == 1:
            return self.save_dir / "save.json"  # Legacy default
        return self.save_dir / f"save_slot_{slot_id}.json"
    
    def get_backup_path(self, slot_id: int) -> Path:
        """Get the backup file path for a slot."""
        return self.save_dir / f"save_slot_{slot_id}.backup.json"
    
    def refresh_slots(self):
        """Refresh information about all save slots."""
        self.slots = {}
        
        for slot_id in range(1, self.MAX_SLOTS + 1):
            save_path = self.get_save_path(slot_id)
            
            if save_path.exists():
                try:
                    with open(save_path, 'r') as f:
                        data = json.load(f)
                    
                    self.slots[slot_id] = self._parse_save_data(slot_id, data)
                except (json.JSONDecodeError, KeyError, IOError):
                    self.slots[slot_id] = SaveSlotInfo(
                        slot_id=slot_id,
                        is_empty=False,
                        duck_name="CORRUPTED",
                    )
            else:
                self.slots[slot_id] = SaveSlotInfo(
                    slot_id=slot_id,
                    is_empty=True,
                )
    
    def _parse_save_data(self, slot_id: int, data: dict) -> SaveSlotInfo:
        """Parse save data into slot info."""
        duck_data = data.get("duck", {})
        progression_data = data.get("progression", {})
        prestige_data = data.get("prestige", {})
        achievements_data = data.get("achievements", {})
        stats_data = data.get("statistics", {})
        
        # Get duck mood for preview
        mood_data = duck_data.get("mood", {})
        current_mood = mood_data.get("current_mood", "happy")
        
        # Create preview ASCII based on level/prestige
        level = progression_data.get("level", 1)
        prestige = prestige_data.get("prestige_level", 0)
        
        preview = self._generate_preview(level, prestige, current_mood)
        
        return SaveSlotInfo(
            slot_id=slot_id,
            is_empty=False,
            duck_name=duck_data.get("name", "Cheese"),
            level=level,
            playtime_minutes=stats_data.get("total_playtime_minutes", 0),
            coins=progression_data.get("coins", 0),
            created_at=stats_data.get("first_played", "Unknown"),
            last_played=stats_data.get("last_played", "Unknown"),
            prestige_level=prestige,
            achievements_count=len(achievements_data.get("unlocked", [])),
            mood=current_mood,
            preview_ascii=preview,
        )
    
    def _generate_preview(self, level: int, prestige: int, mood: str) -> List[str]:
        """Generate ASCII preview for a save slot."""
        # Mood faces
        mood_faces = {
            "happy": "^◡^",
            "excited": "*◡*",
            "content": "◡‿◡",
            "sad": "╥﹏╥",
            "hungry": "ò﹏ó",
            "sleepy": "-_-",
            "playful": "◕‿◕",
        }
        face = mood_faces.get(mood, "^◡^")
        
        # Base duck
        if prestige > 0:
            # Prestige duck with crown/aura
            return [
                f"  *^*   ",
                f"   ({face})  ",
                f"  >d<    ",
                f"  P{prestige} Lv{level} ",
            ]
        elif level >= 50:
            return [
                f"    *     ",
                f"   ({face})  ",
                f"   d      ",
                f"   Lv{level}   ",
            ]
        else:
            return [
                f"   ({face})  ",
                f"   d      ",
                f"   Lv{level}   ",
            ]
    
    def format_playtime(self, minutes: int) -> str:
        """Format playtime as human-readable string."""
        hours = minutes // 60
        mins = minutes % 60
        
        if hours > 24:
            days = hours // 24
            hours = hours % 24
            return f"{days}d {hours}h"
        elif hours > 0:
            return f"{hours}h {mins}m"
        else:
            return f"{mins}m"
    
    def get_slot(self, slot_id: int) -> Optional[SaveSlotInfo]:
        """Get info for a specific slot."""
        return self.slots.get(slot_id)
    
    def load_slot(self, slot_id: int) -> Optional[dict]:
        """Load save data from a slot."""
        if slot_id not in range(1, self.MAX_SLOTS + 1):
            return None
        
        save_path = self.get_save_path(slot_id)
        if not save_path.exists():
            return None
        
        try:
            with open(save_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    def save_to_slot(self, slot_id: int, data: dict) -> bool:
        """Save data to a slot."""
        if slot_id not in range(1, self.MAX_SLOTS + 1):
            return False
        
        save_path = self.get_save_path(slot_id)
        backup_path = self.get_backup_path(slot_id)
        
        try:
            # Create backup of existing save
            if save_path.exists():
                shutil.copy2(save_path, backup_path)
            
            # Save new data
            with open(save_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            # Refresh slot info
            self.refresh_slots()
            return True
            
        except IOError:
            return False
    
    def delete_slot(self, slot_id: int) -> bool:
        """Delete a save slot."""
        if slot_id not in range(1, self.MAX_SLOTS + 1):
            return False
        
        save_path = self.get_save_path(slot_id)
        backup_path = self.get_backup_path(slot_id)
        
        try:
            if save_path.exists():
                save_path.unlink()
            if backup_path.exists():
                backup_path.unlink()
            
            self.refresh_slots()
            return True
            
        except IOError:
            return False
    
    def copy_slot(self, from_slot: int, to_slot: int) -> bool:
        """Copy save from one slot to another."""
        data = self.load_slot(from_slot)
        if data is None:
            return False
        
        return self.save_to_slot(to_slot, data)
    
    def restore_backup(self, slot_id: int) -> bool:
        """Restore a slot from its backup."""
        backup_path = self.get_backup_path(slot_id)
        save_path = self.get_save_path(slot_id)
        
        if not backup_path.exists():
            return False
        
        try:
            shutil.copy2(backup_path, save_path)
            self.refresh_slots()
            return True
        except IOError:
            return False
    
    def has_backup(self, slot_id: int) -> bool:
        """Check if a slot has a backup file."""
        return self.get_backup_path(slot_id).exists()
    
    def export_slot(self, slot_id: int, export_path: str) -> bool:
        """Export a save slot to an external file."""
        data = self.load_slot(slot_id)
        if data is None:
            return False
        
        try:
            with open(export_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except IOError:
            return False
    
    def import_slot(self, slot_id: int, import_path: str) -> bool:
        """Import a save file into a slot."""
        try:
            with open(import_path, 'r') as f:
                data = json.load(f)
            return self.save_to_slot(slot_id, data)
        except (json.JSONDecodeError, IOError):
            return False
    
    def render_slot_selection(self, show_details: bool = True) -> List[str]:
        """Render the save slot selection screen."""
        lines = [
            "+===============================================+",
            "|           [=] SAVE SLOTS [=]                    |",
            "+===============================================+",
        ]
        
        for slot_id in range(1, self.MAX_SLOTS + 1):
            slot = self.slots.get(slot_id)
            
            if slot is None or slot.is_empty:
                lines.append(f"|  [{slot_id}] --- EMPTY SLOT ---                   |")
                lines.append("|      Start a new adventure!                   |")
                lines.append("|                                               |")
            else:
                # Active indicator
                active = " <" if slot_id == self.current_slot else "  "
                
                lines.append(f"|  [{slot_id}] {slot.duck_name:<25} {active}      |")
                
                if show_details:
                    # Show preview ASCII
                    for preview_line in slot.preview_ascii:
                        lines.append(f"|      {preview_line:<39}  |")
                    
                    # Stats
                    playtime = self.format_playtime(slot.playtime_minutes)
                    lines.append(f"|      $ {slot.coins:<8}  ⏱️ {playtime:<15}  |")
                    lines.append(f"|      [#] {slot.achievements_count} achievements                    |")
                    
                    # Last played
                    if slot.last_played and slot.last_played != "Unknown":
                        try:
                            dt = datetime.fromisoformat(slot.last_played)
                            last_str = dt.strftime("%Y-%m-%d %H:%M")
                        except ValueError:
                            last_str = slot.last_played[:16]
                        lines.append(f"|      Last: {last_str:<30}  |")
                
                lines.append("|                                               |")
        
        lines.extend([
            "+===============================================+",
            "|  [1-5] Select  [D] Delete  [C] Copy           |",
            "|  [E] Export    [I] Import  [B] Back           |",
            "+===============================================+",
        ])
        
        return lines
    
    def render_slot_details(self, slot_id: int) -> List[str]:
        """Render detailed view of a single slot."""
        slot = self.slots.get(slot_id)
        
        lines = [
            "+===============================================+",
            f"|           [=] SLOT {slot_id} DETAILS                   |",
            "+===============================================+",
        ]
        
        if slot is None or slot.is_empty:
            lines.append("|                                               |")
            lines.append("|              Empty Save Slot                  |")
            lines.append("|                                               |")
            lines.append("|         Start a new adventure?                |")
            lines.append("|                                               |")
        else:
            # Duck preview centered
            lines.append("|                                               |")
            for preview_line in slot.preview_ascii:
                lines.append(f"|  {preview_line:^43}  |")
            
            lines.append("|                                               |")
            lines.append(f"|  Duck Name: {slot.duck_name:<32}  |")
            lines.append(f"|  Level: {slot.level:<36}  |")
            
            if slot.prestige_level > 0:
                lines.append(f"|  Prestige: {slot.prestige_level:<33}  |")
            
            lines.append(f"|  Coins: {slot.coins:<36}  |")
            lines.append(f"|  Playtime: {self.format_playtime(slot.playtime_minutes):<33}  |")
            lines.append(f"|  Achievements: {slot.achievements_count:<28}  |")
            lines.append(f"|  Current Mood: {slot.mood:<28}  |")
            
            lines.append("|                                               |")
            
            if slot.created_at and slot.created_at != "Unknown":
                try:
                    dt = datetime.fromisoformat(slot.created_at)
                    created = dt.strftime("%Y-%m-%d")
                except ValueError:
                    created = slot.created_at[:10]
                lines.append(f"|  Created: {created:<34}  |")
            
            if slot.last_played and slot.last_played != "Unknown":
                try:
                    dt = datetime.fromisoformat(slot.last_played)
                    last = dt.strftime("%Y-%m-%d %H:%M")
                except ValueError:
                    last = slot.last_played[:16]
                lines.append(f"|  Last Played: {last:<30}  |")
            
            has_backup = self.has_backup(slot_id)
            backup_str = "Yes" if has_backup else "No"
            lines.append(f"|  Backup Available: {backup_str:<25}  |")
        
        lines.extend([
            "+===============================================+",
            "|  [L] Load  [D] Delete  [R] Restore Backup     |",
            "|  [E] Export  [B] Back                         |",
            "+===============================================+",
        ])
        
        return lines
    
    def to_dict(self) -> dict:
        """Convert to dictionary for meta-save (which slot was last used)."""
        return {
            "current_slot": self.current_slot,
        }
    
    @classmethod
    def from_dict(cls, data: dict, save_dir: str = "~/.cheese_the_duck") -> "SaveSlotsSystem":
        """Create from dictionary."""
        system = cls(save_dir)
        system.current_slot = data.get("current_slot", 1)
        return system


# Global instance
save_slots_system = SaveSlotsSystem()
