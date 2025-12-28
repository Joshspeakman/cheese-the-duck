"""
Secrets and Easter Eggs System - Hidden content and discoveries.
Includes secret areas, hidden items, special events, and easter eggs.
"""
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple, Callable
from enum import Enum
import random
import hashlib


class SecretType(Enum):
    """Types of secrets."""
    EASTER_EGG = "easter_egg"
    HIDDEN_ITEM = "hidden_item"
    SECRET_AREA = "secret_area"
    SPECIAL_EVENT = "special_event"
    HIDDEN_COMMAND = "hidden_command"
    SECRET_COMBINATION = "secret_combination"
    RARE_ENCOUNTER = "rare_encounter"


class SecretRarity(Enum):
    """Rarity of secrets."""
    COMMON = "common"        # Easy to find
    UNCOMMON = "uncommon"    # Moderate effort
    RARE = "rare"            # Requires dedication
    LEGENDARY = "legendary"   # Extremely hard to find
    MYTHICAL = "mythical"    # Almost impossible


@dataclass
class Secret:
    """Definition of a secret."""
    id: str
    name: str
    description: str
    hint: str
    secret_type: SecretType
    rarity: SecretRarity
    coins_reward: int = 0
    xp_reward: int = 0
    special_reward: str = ""
    unlock_message: str = ""
    ascii_art: List[str] = field(default_factory=list)


@dataclass
class DiscoveredSecret:
    """A secret that has been discovered."""
    secret_id: str
    discovered_at: str
    times_triggered: int = 1


# Define all secrets
SECRETS: Dict[str, Secret] = {
    # Easter Eggs
    "konami_code": Secret(
        id="konami_code",
        name="Konami Code",
        description="The classic cheat code works here!",
        hint="↑↑↓↓←→←→BA",
        secret_type=SecretType.EASTER_EGG,
        rarity=SecretRarity.UNCOMMON,
        coins_reward=500,
        xp_reward=100,
        unlock_message="30 extra coins! Wait... lives? We don't do that here.",
        ascii_art=[
            "  ↑↑↓↓←→←→BA  ",
            "    START!     ",
            "  🎮 CLASSIC 🎮  ",
        ]
    ),
    
    "duck_song": Secret(
        id="duck_song",
        name="The Duck Song",
        description="Got any grapes?",
        hint="Try talking about grapes...",
        secret_type=SecretType.EASTER_EGG,
        rarity=SecretRarity.COMMON,
        coins_reward=100,
        xp_reward=50,
        unlock_message="A duck walked up to a lemonade stand...",
        ascii_art=[
            "  🍇 🍇 🍇 🍇  ",
            " Got any grapes? ",
            "  🍋 Nope! 🍋    ",
        ]
    ),
    
    "midnight_quack": Secret(
        id="midnight_quack",
        name="Midnight Quacker",
        description="Something special happens at exactly midnight...",
        hint="The clock strikes twelve...",
        secret_type=SecretType.SPECIAL_EVENT,
        rarity=SecretRarity.RARE,
        coins_reward=250,
        xp_reward=150,
        special_reward="midnight_hat",
        unlock_message="🌙 The Midnight Duck rises! 🌙"
    ),
    
    "triple_seven": Secret(
        id="triple_seven",
        name="Lucky 777",
        description="When coins align perfectly...",
        hint="777 is a lucky number...",
        secret_type=SecretType.SECRET_COMBINATION,
        rarity=SecretRarity.UNCOMMON,
        coins_reward=777,
        xp_reward=77,
        unlock_message="JACKPOT! 🎰🎰🎰"
    ),
    
    "golden_duck": Secret(
        id="golden_duck",
        name="The Golden Duck",
        description="A shimmering golden feather appears...",
        hint="Feed 1000 times for something special",
        secret_type=SecretType.RARE_ENCOUNTER,
        rarity=SecretRarity.LEGENDARY,
        coins_reward=5000,
        xp_reward=1000,
        special_reward="golden_aura",
        unlock_message="Your duck glows with golden light!",
        ascii_art=[
            "     ✨✨✨     ",
            "   ⭐🦆⭐    ",
            "     ✨✨✨     ",
            "  LEGENDARY!   ",
        ]
    ),
    
    "rubber_duck": Secret(
        id="rubber_duck",
        name="Rubber Ducky Mode",
        description="Squeak squeak!",
        hint="Type 'squeak' three times...",
        secret_type=SecretType.HIDDEN_COMMAND,
        rarity=SecretRarity.COMMON,
        coins_reward=50,
        xp_reward=25,
        unlock_message="🛁 SQUEAK! You're the one! 🛁"
    ),
    
    "secret_pond": Secret(
        id="secret_pond",
        name="Hidden Lily Pond",
        description="A secret peaceful pond behind the waterfall...",
        hint="Explore when it's raining heavily",
        secret_type=SecretType.SECRET_AREA,
        rarity=SecretRarity.RARE,
        coins_reward=300,
        xp_reward=200,
        special_reward="lily_pad_decoration",
        unlock_message="You discovered a hidden sanctuary!"
    ),
    
    "dev_room": Secret(
        id="dev_room",
        name="Developer's Room",
        description="Where the magic happens...",
        hint="404... but not really",
        secret_type=SecretType.SECRET_AREA,
        rarity=SecretRarity.LEGENDARY,
        coins_reward=1000,
        xp_reward=500,
        unlock_message="Welcome behind the scenes!",
        ascii_art=[
            "  +----------+  ",
            "  | DEV ROOM |  ",
            "  |  🖥️ 🦆   |  ",
            "  | v1.0.0   |  ",
            "  +----------+  ",
        ]
    ),
    
    "birthday_duck": Secret(
        id="birthday_duck",
        name="Birthday Duck",
        description="Celebrating a special day!",
        hint="Play on a very special day...",
        secret_type=SecretType.SPECIAL_EVENT,
        rarity=SecretRarity.UNCOMMON,
        coins_reward=200,
        xp_reward=100,
        special_reward="birthday_hat",
        unlock_message="🎂 Happy Birthday! 🎂"
    ),
    
    "palindrome": Secret(
        id="palindrome",
        name="Palindrome Duck",
        description="Forward and backward, all the same!",
        hint="12:21, 23:32, 11:11...",
        secret_type=SecretType.SPECIAL_EVENT,
        rarity=SecretRarity.COMMON,
        coins_reward=111,
        xp_reward=11,
        unlock_message="Time mirrors itself! ⏰"
    ),
    
    "hundred_pets": Secret(
        id="hundred_pets",
        name="Pet Master",
        description="100 pets in one session!",
        hint="Pet, pet, pet, pet, pet...",
        secret_type=SecretType.RARE_ENCOUNTER,
        rarity=SecretRarity.UNCOMMON,
        coins_reward=200,
        xp_reward=100,
        unlock_message="You really love petting! 🫳🦆"
    ),
    
    "ancient_quack": Secret(
        id="ancient_quack",
        name="Ancient Quack",
        description="The primordial duck sound...",
        hint="Quack in ancient language",
        secret_type=SecretType.HIDDEN_COMMAND,
        rarity=SecretRarity.RARE,
        coins_reward=500,
        xp_reward=250,
        unlock_message="QUACKUS MAXIMUS!",
        ascii_art=[
            "   📜📜📜📜   ",
            "  QUACKUS    ",
            "   MAXIMUS   ",
            "   📜📜📜📜   ",
        ]
    ),
    
    "night_owl_duck": Secret(
        id="night_owl_duck",
        name="Night Owl",
        description="Playing in the wee hours...",
        hint="3 AM club member",
        secret_type=SecretType.SPECIAL_EVENT,
        rarity=SecretRarity.UNCOMMON,
        coins_reward=150,
        xp_reward=75,
        unlock_message="🦉 Why are you awake? 🦆"
    ),
    
    "rainbow_duck": Secret(
        id="rainbow_duck",
        name="Rainbow Connection",
        description="All colors of the rainbow!",
        hint="Have 7 different colored items equipped",
        secret_type=SecretType.SECRET_COMBINATION,
        rarity=SecretRarity.RARE,
        coins_reward=700,
        xp_reward=350,
        special_reward="rainbow_trail",
        unlock_message="🌈 Somewhere over the rainbow! 🌈"
    ),
    
    "year_one": Secret(
        id="year_one",
        name="Year One",
        description="365 days of duck care!",
        hint="A whole year...",
        secret_type=SecretType.RARE_ENCOUNTER,
        rarity=SecretRarity.MYTHICAL,
        coins_reward=10000,
        xp_reward=5000,
        special_reward="eternal_bond_title",
        unlock_message="A bond that transcends time! 🎊",
        ascii_art=[
            "   ★ YEAR ONE ★  ",
            "    365 DAYS     ",
            "   🦆💕 CHEESE   ",
            "   FOREVER! 💕🦆  ",
        ]
    ),
}


class SecretsSystem:
    """
    System for managing secrets and easter eggs.
    """
    
    def __init__(self):
        self.discovered_secrets: Dict[str, DiscoveredSecret] = {}
        self.input_buffer: List[str] = []  # For command sequences
        self.session_pet_count: int = 0
        self.session_squeak_count: int = 0
        self.last_check_time: str = ""
        self.special_date_checked: str = ""
        
        # Konami code sequence
        self.konami_sequence = ["up", "up", "down", "down", "left", "right", "left", "right", "b", "a"]
    
    def check_input_sequence(self, input_key: str) -> Optional[Secret]:
        """Check if input sequence triggers a secret."""
        self.input_buffer.append(input_key.lower())
        
        # Keep buffer manageable
        if len(self.input_buffer) > 20:
            self.input_buffer = self.input_buffer[-20:]
        
        # Check Konami Code
        if len(self.input_buffer) >= 10:
            last_10 = self.input_buffer[-10:]
            if last_10 == self.konami_sequence:
                return self.discover_secret("konami_code")
        
        return None
    
    def check_text_input(self, text: str) -> Optional[Secret]:
        """Check text input for secret triggers."""
        text_lower = text.lower()
        
        # Check for grape mentions
        if "grape" in text_lower or "grapes" in text_lower:
            return self.discover_secret("duck_song")
        
        # Check for squeak
        if "squeak" in text_lower:
            self.session_squeak_count += 1
            if self.session_squeak_count >= 3:
                self.session_squeak_count = 0
                return self.discover_secret("rubber_duck")
        
        # Check for ancient quack
        if text_lower in ["quackus", "quackus maximus", "ancient quack"]:
            return self.discover_secret("ancient_quack")
        
        return None
    
    def check_time_secrets(self) -> Optional[Secret]:
        """Check for time-based secrets."""
        now = datetime.now()
        time_str = now.strftime("%H:%M")
        
        # Prevent duplicate checks in same minute
        if time_str == self.last_check_time:
            return None
        self.last_check_time = time_str
        
        # Midnight
        if time_str == "00:00":
            return self.discover_secret("midnight_quack")
        
        # 3 AM
        if time_str == "03:00":
            return self.discover_secret("night_owl_duck")
        
        # Palindrome times
        if time_str == time_str[::-1]:  # e.g., 12:21
            return self.discover_secret("palindrome")
        
        return None
    
    def check_date_secrets(self) -> Optional[Secret]:
        """Check for date-based secrets."""
        today = date.today().isoformat()
        
        if today == self.special_date_checked:
            return None
        self.special_date_checked = today
        
        # This could be customized or read from config
        # For now, let's check for common special dates
        month_day = date.today().strftime("%m-%d")
        
        # April 1st - could be duck birthday
        if month_day == "04-01":
            return self.discover_secret("birthday_duck")
        
        return None
    
    def check_coin_secret(self, coins: int) -> Optional[Secret]:
        """Check for coin-based secrets."""
        if coins == 777 or coins == 7777:
            return self.discover_secret("triple_seven")
        return None
    
    def check_action_secrets(self, action: str, count: int = 0) -> Optional[Secret]:
        """Check for action-based secrets."""
        if action == "pet":
            self.session_pet_count += 1
            if self.session_pet_count >= 100:
                return self.discover_secret("hundred_pets")
        
        if action == "feed" and count >= 1000:
            return self.discover_secret("golden_duck")
        
        return None
    
    def check_exploration_secret(self, weather: str) -> Optional[Secret]:
        """Check for exploration-based secrets."""
        if weather in ["heavy_rain", "storm", "thunderstorm"]:
            # 5% chance during heavy rain
            if random.random() < 0.05:
                return self.discover_secret("secret_pond")
        
        return None
    
    def check_playtime_secret(self, days_played: int) -> Optional[Secret]:
        """Check for playtime-based secrets."""
        if days_played >= 365:
            return self.discover_secret("year_one")
        return None
    
    def discover_secret(self, secret_id: str) -> Optional[Secret]:
        """Discover a secret."""
        if secret_id not in SECRETS:
            return None
        
        secret = SECRETS[secret_id]
        
        if secret_id in self.discovered_secrets:
            # Already discovered, just increment trigger count
            self.discovered_secrets[secret_id].times_triggered += 1
            return None  # Don't reward again
        
        # New discovery!
        self.discovered_secrets[secret_id] = DiscoveredSecret(
            secret_id=secret_id,
            discovered_at=datetime.now().isoformat()
        )
        
        return secret
    
    def get_discovered_count(self) -> Tuple[int, int]:
        """Get count of discovered secrets vs total."""
        return len(self.discovered_secrets), len(SECRETS)
    
    def get_undiscovered_hints(self) -> List[str]:
        """Get hints for undiscovered secrets."""
        hints = []
        for secret_id, secret in SECRETS.items():
            if secret_id not in self.discovered_secrets:
                hints.append(f"[{secret.rarity.value.upper()}] {secret.hint}")
        return hints
    
    def get_rarity_progress(self) -> Dict[SecretRarity, Tuple[int, int]]:
        """Get discovery progress by rarity."""
        progress = {}
        
        for rarity in SecretRarity:
            total = sum(1 for s in SECRETS.values() if s.rarity == rarity)
            discovered = sum(
                1 for sid in self.discovered_secrets 
                if SECRETS[sid].rarity == rarity
            )
            progress[rarity] = (discovered, total)
        
        return progress
    
    def render_secrets_book(self, page: int = 1) -> List[str]:
        """Render the secrets discovery book."""
        lines = [
            "╔═══════════════════════════════════════════════╗",
            "║            🔮 BOOK OF SECRETS 🔮              ║",
            "╠═══════════════════════════════════════════════╣",
        ]
        
        discovered, total = self.get_discovered_count()
        lines.append(f"║  Secrets Found: {discovered}/{total}                         ║")
        lines.append("╠═══════════════════════════════════════════════╣")
        
        # Show discovered secrets
        discovered_list = list(self.discovered_secrets.keys())
        per_page = 5
        start = (page - 1) * per_page
        end = start + per_page
        page_secrets = discovered_list[start:end]
        
        if page_secrets:
            for secret_id in page_secrets:
                secret = SECRETS[secret_id]
                rarity_icon = {
                    SecretRarity.COMMON: "⚪",
                    SecretRarity.UNCOMMON: "🟢",
                    SecretRarity.RARE: "🔵",
                    SecretRarity.LEGENDARY: "🟡",
                    SecretRarity.MYTHICAL: "🔴",
                }.get(secret.rarity, "⚪")
                
                name = secret.name[:30]
                lines.append(f"║  {rarity_icon} {name:<38}  ║")
                lines.append(f"║     {secret.description[:38]:<38}  ║")
        else:
            lines.append("║  No secrets discovered yet!                   ║")
            lines.append("║  Keep exploring and experimenting...          ║")
        
        lines.append("╠═══════════════════════════════════════════════╣")
        
        # Show hints for undiscovered
        lines.append("║  💡 HINTS:                                    ║")
        hints = self.get_undiscovered_hints()[:2]  # Show 2 hints
        for hint in hints:
            hint_text = hint[:40]
            lines.append(f"║  • {hint_text:<40}  ║")
        
        if not hints:
            lines.append("║  You've found all the secrets! 🎉            ║")
        
        total_pages = (len(discovered_list) + per_page - 1) // per_page
        total_pages = max(1, total_pages)
        
        lines.extend([
            "╠═══════════════════════════════════════════════╣",
            f"║  Page {page}/{total_pages}  [←/→ to navigate]                ║",
            "╚═══════════════════════════════════════════════╝",
        ])
        
        return lines
    
    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "discovered_secrets": {
                sid: {
                    "secret_id": d.secret_id,
                    "discovered_at": d.discovered_at,
                    "times_triggered": d.times_triggered,
                }
                for sid, d in self.discovered_secrets.items()
            },
            "special_date_checked": self.special_date_checked,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "SecretsSystem":
        """Create from dictionary."""
        system = cls()
        
        discovered = data.get("discovered_secrets", {})
        for sid, d in discovered.items():
            system.discovered_secrets[sid] = DiscoveredSecret(
                secret_id=d["secret_id"],
                discovered_at=d.get("discovered_at", ""),
                times_triggered=d.get("times_triggered", 1),
            )
        
        system.special_date_checked = data.get("special_date_checked", "")
        
        return system


# Global secrets system instance
secrets_system = SecretsSystem()
