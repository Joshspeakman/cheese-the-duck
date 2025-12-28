"""
Titles System - Earned nicknames, titles, and relationship levels.
Features title unlocking, display options, and special titles.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum


class TitleCategory(Enum):
    """Categories of titles."""
    ACHIEVEMENT = "achievement"
    RELATIONSHIP = "relationship"
    SKILL = "skill"
    SEASONAL = "seasonal"
    SPECIAL = "special"
    HIDDEN = "hidden"


class TitleRarity(Enum):
    """Rarity of titles."""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    MYTHIC = "mythic"


@dataclass
class Title:
    """A title that can be earned."""
    id: str
    name: str
    description: str
    category: TitleCategory
    rarity: TitleRarity
    prefix: Optional[str] = None  # Goes before name
    suffix: Optional[str] = None  # Goes after name
    color: str = "yellow"  # Display color
    unlock_condition: str = ""
    xp_bonus: int = 0  # Bonus XP while equipped
    special_effect: Optional[str] = None


@dataclass
class EarnedTitle:
    """A title the player has earned."""
    title_id: str
    earned_at: str
    earned_from: str
    times_equipped: int = 0
    is_favorite: bool = False


# Title Definitions
TITLES: Dict[str, Title] = {
    # Achievement Titles
    "new_caretaker": Title(
        id="new_caretaker",
        name="New Caretaker",
        description="Just starting your journey",
        category=TitleCategory.ACHIEVEMENT,
        rarity=TitleRarity.COMMON,
        suffix="the Beginner",
        unlock_condition="Start the game",
    ),
    "dedicated": Title(
        id="dedicated",
        name="Dedicated",
        description="Logged in for 7 days in a row",
        category=TitleCategory.ACHIEVEMENT,
        rarity=TitleRarity.UNCOMMON,
        prefix="Dedicated",
        unlock_condition="7 day login streak",
        xp_bonus=5,
    ),
    "devoted": Title(
        id="devoted",
        name="Devoted",
        description="Logged in for 30 days in a row",
        category=TitleCategory.ACHIEVEMENT,
        rarity=TitleRarity.RARE,
        prefix="Devoted",
        unlock_condition="30 day login streak",
        xp_bonus=10,
    ),
    "eternal_bond": Title(
        id="eternal_bond",
        name="Eternal Bond",
        description="100+ day login streak",
        category=TitleCategory.ACHIEVEMENT,
        rarity=TitleRarity.LEGENDARY,
        prefix="Eternally Bonded",
        unlock_condition="100 day login streak",
        xp_bonus=25,
        special_effect="golden_text",
    ),
    "first_million": Title(
        id="first_million",
        name="Millionaire",
        description="Earned 1,000,000 total coins",
        category=TitleCategory.ACHIEVEMENT,
        rarity=TitleRarity.EPIC,
        suffix="the Rich",
        unlock_condition="Earn 1,000,000 coins lifetime",
        xp_bonus=15,
    ),
    
    # Relationship Titles
    "acquaintance": Title(
        id="acquaintance",
        name="Acquaintance",
        description="Just getting to know each other",
        category=TitleCategory.RELATIONSHIP,
        rarity=TitleRarity.COMMON,
        suffix="'s Acquaintance",
        unlock_condition="Reach relationship level 1",
    ),
    "friend": Title(
        id="friend",
        name="Friend",
        description="A true friend",
        category=TitleCategory.RELATIONSHIP,
        rarity=TitleRarity.UNCOMMON,
        suffix="'s Friend",
        unlock_condition="Reach relationship level 5",
        xp_bonus=5,
    ),
    "best_friend": Title(
        id="best_friend",
        name="Best Friend",
        description="Best friends forever!",
        category=TitleCategory.RELATIONSHIP,
        rarity=TitleRarity.RARE,
        suffix="'s Best Friend",
        unlock_condition="Reach relationship level 10",
        xp_bonus=10,
    ),
    "soulmate": Title(
        id="soulmate",
        name="Soulmate",
        description="An unbreakable bond",
        category=TitleCategory.RELATIONSHIP,
        rarity=TitleRarity.LEGENDARY,
        prefix="Soulmate of",
        unlock_condition="Reach relationship level 20",
        xp_bonus=20,
        special_effect="heart_particles",
    ),
    "duck_whisperer": Title(
        id="duck_whisperer",
        name="Duck Whisperer",
        description="Understands ducks on a deep level",
        category=TitleCategory.RELATIONSHIP,
        rarity=TitleRarity.EPIC,
        prefix="The",
        suffix="Duck Whisperer",
        unlock_condition="Maximum relationship with 3 ducks",
        xp_bonus=15,
    ),
    
    # Skill Titles
    "master_fisher": Title(
        id="master_fisher",
        name="Master Fisher",
        description="Caught 100+ fish",
        category=TitleCategory.SKILL,
        rarity=TitleRarity.RARE,
        prefix="Master Fisher",
        unlock_condition="Catch 100 fish",
        xp_bonus=10,
    ),
    "legendary_angler": Title(
        id="legendary_angler",
        name="Legendary Angler",
        description="Caught a legendary fish",
        category=TitleCategory.SKILL,
        rarity=TitleRarity.LEGENDARY,
        suffix="the Legendary Angler",
        unlock_condition="Catch a legendary fish",
        xp_bonus=20,
    ),
    "green_thumb": Title(
        id="green_thumb",
        name="Green Thumb",
        description="Harvested 50+ plants",
        category=TitleCategory.SKILL,
        rarity=TitleRarity.UNCOMMON,
        prefix="Green Thumb",
        unlock_condition="Harvest 50 plants",
        xp_bonus=5,
    ),
    "master_gardener": Title(
        id="master_gardener",
        name="Master Gardener",
        description="Grew a rare golden flower",
        category=TitleCategory.SKILL,
        rarity=TitleRarity.EPIC,
        prefix="Master Gardener",
        unlock_condition="Grow a golden flower",
        xp_bonus=15,
    ),
    "treasure_hunter": Title(
        id="treasure_hunter",
        name="Treasure Hunter",
        description="Found 25+ treasures",
        category=TitleCategory.SKILL,
        rarity=TitleRarity.RARE,
        suffix="the Treasure Hunter",
        unlock_condition="Find 25 treasures",
        xp_bonus=10,
    ),
    "trick_master": Title(
        id="trick_master",
        name="Trick Master",
        description="Learned 10+ tricks",
        category=TitleCategory.SKILL,
        rarity=TitleRarity.RARE,
        prefix="Trick Master",
        unlock_condition="Learn 10 tricks",
        xp_bonus=10,
    ),
    "performance_star": Title(
        id="performance_star",
        name="Performance Star",
        description="50 perfect trick performances",
        category=TitleCategory.SKILL,
        rarity=TitleRarity.EPIC,
        prefix="⭐",
        suffix="the Star",
        unlock_condition="50 perfect performances",
        xp_bonus=15,
    ),
    
    # Seasonal Titles
    "spring_spirit": Title(
        id="spring_spirit",
        name="Spring Spirit",
        description="Celebrated the Spring Festival",
        category=TitleCategory.SEASONAL,
        rarity=TitleRarity.RARE,
        prefix="🌸",
        suffix="of Spring",
        unlock_condition="Complete Spring Festival",
        xp_bonus=5,
    ),
    "summer_soul": Title(
        id="summer_soul",
        name="Summer Soul",
        description="Celebrated the Summer Festival",
        category=TitleCategory.SEASONAL,
        rarity=TitleRarity.RARE,
        prefix="☀️",
        suffix="of Summer",
        unlock_condition="Complete Summer Festival",
        xp_bonus=5,
    ),
    "autumn_guardian": Title(
        id="autumn_guardian",
        name="Autumn Guardian",
        description="Celebrated the Autumn Festival",
        category=TitleCategory.SEASONAL,
        rarity=TitleRarity.RARE,
        prefix="🍂",
        suffix="of Autumn",
        unlock_condition="Complete Autumn Festival",
        xp_bonus=5,
    ),
    "winter_wanderer": Title(
        id="winter_wanderer",
        name="Winter Wanderer",
        description="Celebrated the Winter Festival",
        category=TitleCategory.SEASONAL,
        rarity=TitleRarity.RARE,
        prefix="❄️",
        suffix="of Winter",
        unlock_condition="Complete Winter Festival",
        xp_bonus=5,
    ),
    "season_master": Title(
        id="season_master",
        name="Season Master",
        description="Completed all seasonal festivals",
        category=TitleCategory.SEASONAL,
        rarity=TitleRarity.LEGENDARY,
        prefix="🌍",
        suffix="Master of Seasons",
        unlock_condition="Complete all 4 seasonal festivals",
        xp_bonus=25,
        special_effect="rainbow_text",
    ),
    
    # Special Titles
    "duck_day_champion": Title(
        id="duck_day_champion",
        name="Duck Day Champion",
        description="Won Duck Day competition",
        category=TitleCategory.SPECIAL,
        rarity=TitleRarity.LEGENDARY,
        prefix="🦆 Champion",
        unlock_condition="Win Duck Day",
        xp_bonus=30,
    ),
    "collector": Title(
        id="collector",
        name="Collector",
        description="Collected 50+ unique items",
        category=TitleCategory.SPECIAL,
        rarity=TitleRarity.UNCOMMON,
        suffix="the Collector",
        unlock_condition="Own 50 unique items",
        xp_bonus=5,
    ),
    "completionist": Title(
        id="completionist",
        name="Completionist",
        description="Unlocked all achievements",
        category=TitleCategory.SPECIAL,
        rarity=TitleRarity.MYTHIC,
        prefix="✨",
        suffix="the Completionist ✨",
        unlock_condition="Unlock all achievements",
        xp_bonus=50,
        special_effect="sparkle_name",
    ),
    
    # Hidden Titles
    "night_owl": Title(
        id="night_owl",
        name="Night Owl",
        description="Play between midnight and 5 AM",
        category=TitleCategory.HIDDEN,
        rarity=TitleRarity.RARE,
        suffix="🦉",
        unlock_condition="Play at night 10 times",
        xp_bonus=5,
    ),
    "early_bird": Title(
        id="early_bird",
        name="Early Bird",
        description="Play between 5 AM and 7 AM",
        category=TitleCategory.HIDDEN,
        rarity=TitleRarity.RARE,
        prefix="🌅",
        unlock_condition="Play early morning 10 times",
        xp_bonus=5,
    ),
    "secret_finder": Title(
        id="secret_finder",
        name="Secret Finder",
        description="Found a hidden secret",
        category=TitleCategory.HIDDEN,
        rarity=TitleRarity.EPIC,
        suffix="🔍",
        unlock_condition="Discover a hidden secret",
        xp_bonus=15,
    ),
    "konami_master": Title(
        id="konami_master",
        name="Konami Master",
        description="Entered the secret code",
        category=TitleCategory.HIDDEN,
        rarity=TitleRarity.LEGENDARY,
        prefix="⬆️⬆️⬇️⬇️",
        unlock_condition="Enter the Konami code",
        xp_bonus=25,
        special_effect="retro_style",
    ),
}


class TitlesSystem:
    """
    Manages earned titles and nicknames.
    """
    
    def __init__(self):
        self.earned_titles: Dict[str, EarnedTitle] = {}
        self.current_title: Optional[str] = None
        self.duck_nickname: str = "Cheese"
        self.owner_nickname: str = "Friend"
        self.total_titles_earned: int = 0
        self.favorite_titles: List[str] = []
        self.title_display_mode: str = "prefix"  # prefix, suffix, both
    
    def earn_title(self, title_id: str, earned_from: str = "achievement") -> Tuple[bool, str]:
        """Earn a new title."""
        if title_id in self.earned_titles:
            return False, "Already have this title!"
        
        title = TITLES.get(title_id)
        if not title:
            return False, "Title not found!"
        
        self.earned_titles[title_id] = EarnedTitle(
            title_id=title_id,
            earned_at=datetime.now().isoformat(),
            earned_from=earned_from,
        )
        
        self.total_titles_earned += 1
        
        # Auto-equip if first title
        if not self.current_title:
            self.current_title = title_id
        
        rarity_emoji = {
            TitleRarity.COMMON: "",
            TitleRarity.UNCOMMON: "✦",
            TitleRarity.RARE: "★",
            TitleRarity.EPIC: "★★",
            TitleRarity.LEGENDARY: "★★★",
            TitleRarity.MYTHIC: "✨★★★✨",
        }
        
        emoji = rarity_emoji.get(title.rarity, "")
        return True, f"🎖️ New Title Earned: {emoji} {title.name}!"
    
    def equip_title(self, title_id: str) -> Tuple[bool, str]:
        """Equip a title."""
        if title_id not in self.earned_titles:
            return False, "You haven't earned this title!"
        
        self.current_title = title_id
        self.earned_titles[title_id].times_equipped += 1
        
        title = TITLES.get(title_id)
        name = title.name if title else title_id
        
        return True, f"🏷️ Equipped title: {name}"
    
    def unequip_title(self) -> Tuple[bool, str]:
        """Remove current title."""
        if not self.current_title:
            return False, "No title equipped!"
        
        self.current_title = None
        return True, "🏷️ Title removed"
    
    def get_display_name(self, base_name: Optional[str] = None) -> str:
        """Get the full display name with title."""
        name = base_name or self.duck_nickname
        
        if not self.current_title:
            return name
        
        title = TITLES.get(self.current_title)
        if not title:
            return name
        
        if self.title_display_mode == "prefix" and title.prefix:
            return f"{title.prefix} {name}"
        elif self.title_display_mode == "suffix" and title.suffix:
            return f"{name} {title.suffix}"
        elif self.title_display_mode == "both":
            if title.prefix and title.suffix:
                return f"{title.prefix} {name} {title.suffix}"
            elif title.prefix:
                return f"{title.prefix} {name}"
            elif title.suffix:
                return f"{name} {title.suffix}"
        
        return name
    
    def get_xp_bonus(self) -> int:
        """Get XP bonus from current title."""
        if not self.current_title:
            return 0
        
        title = TITLES.get(self.current_title)
        return title.xp_bonus if title else 0
    
    def set_nickname(self, nickname: str, is_duck: bool = True) -> Tuple[bool, str]:
        """Set a custom nickname."""
        if len(nickname) < 1 or len(nickname) > 20:
            return False, "Nickname must be 1-20 characters!"
        
        if is_duck:
            self.duck_nickname = nickname
            return True, f"🦆 Duck is now called: {nickname}"
        else:
            self.owner_nickname = nickname
            return True, f"👤 You are now known as: {nickname}"
    
    def toggle_favorite(self, title_id: str) -> Tuple[bool, str]:
        """Toggle a title as favorite."""
        if title_id not in self.earned_titles:
            return False, "You haven't earned this title!"
        
        earned = self.earned_titles[title_id]
        earned.is_favorite = not earned.is_favorite
        
        if earned.is_favorite:
            if title_id not in self.favorite_titles:
                self.favorite_titles.append(title_id)
            return True, "⭐ Added to favorites!"
        else:
            if title_id in self.favorite_titles:
                self.favorite_titles.remove(title_id)
            return True, "Removed from favorites"
    
    def get_titles_by_category(self, category: TitleCategory) -> List[Tuple[Title, bool]]:
        """Get all titles in a category with ownership status."""
        result = []
        for title_id, title in TITLES.items():
            if title.category == category:
                owned = title_id in self.earned_titles
                result.append((title, owned))
        return result
    
    def check_title_conditions(self, stats: Dict) -> List[str]:
        """Check if any new titles should be earned based on stats."""
        earned = []
        
        # Login streak titles
        if stats.get("login_streak", 0) >= 7 and "dedicated" not in self.earned_titles:
            earned.append("dedicated")
        if stats.get("login_streak", 0) >= 30 and "devoted" not in self.earned_titles:
            earned.append("devoted")
        if stats.get("login_streak", 0) >= 100 and "eternal_bond" not in self.earned_titles:
            earned.append("eternal_bond")
        
        # Skill titles
        if stats.get("fish_caught", 0) >= 100 and "master_fisher" not in self.earned_titles:
            earned.append("master_fisher")
        if stats.get("plants_harvested", 0) >= 50 and "green_thumb" not in self.earned_titles:
            earned.append("green_thumb")
        if stats.get("treasures_found", 0) >= 25 and "treasure_hunter" not in self.earned_titles:
            earned.append("treasure_hunter")
        if stats.get("tricks_learned", 0) >= 10 and "trick_master" not in self.earned_titles:
            earned.append("trick_master")
        if stats.get("perfect_performances", 0) >= 50 and "performance_star" not in self.earned_titles:
            earned.append("performance_star")
        
        # Achievement titles
        if stats.get("total_coins", 0) >= 1000000 and "first_million" not in self.earned_titles:
            earned.append("first_million")
        if stats.get("unique_items", 0) >= 50 and "collector" not in self.earned_titles:
            earned.append("collector")
        
        return earned
    
    def render_titles_screen(self) -> List[str]:
        """Render the titles management screen."""
        lines = [
            "╔═══════════════════════════════════════════════╗",
            "║            🏷️ TITLES & NICKNAMES 🏷️          ║",
            "╠═══════════════════════════════════════════════╣",
            f"║  Duck: {self.duck_nickname:^35}  ║",
            f"║  You: {self.owner_nickname:^36}  ║",
        ]
        
        display_name = self.get_display_name()
        lines.append(f"║  Display: {display_name:^31}  ║")
        
        current = TITLES.get(self.current_title) if self.current_title else None
        if current:
            lines.append(f"║  Current Title: {current.name:^25}  ║")
            if current.xp_bonus > 0:
                lines.append(f"║  XP Bonus: +{current.xp_bonus}%                             ║")
        
        lines.append("╠═══════════════════════════════════════════════╣")
        lines.append(f"║  Titles Earned: {self.total_titles_earned:3}/{len(TITLES):<3}                       ║")
        lines.append("╠═══════════════════════════════════════════════╣")
        lines.append("║  YOUR TITLES:                                 ║")
        
        for tid, earned in list(self.earned_titles.items())[:5]:
            title = TITLES.get(tid)
            if title:
                equipped = "●" if tid == self.current_title else "○"
                fav = "★" if earned.is_favorite else " "
                rarity_icon = {"common": "⚪", "uncommon": "🟢", "rare": "🔵", "epic": "🟣", "legendary": "🟡", "mythic": "🔴"}.get(title.rarity.value, "⚪")
                lines.append(f"║  {equipped}{fav} {rarity_icon} {title.name[:30]:30}   ║")
        
        if not self.earned_titles:
            lines.append("║   No titles earned yet!                       ║")
        
        lines.append("╚═══════════════════════════════════════════════╝")
        
        return lines
    
    def render_title_detail(self, title_id: str) -> List[str]:
        """Render detailed view of a title."""
        title = TITLES.get(title_id)
        if not title:
            return ["Title not found!"]
        
        owned = title_id in self.earned_titles
        earned = self.earned_titles.get(title_id)
        
        rarity_colors = {
            TitleRarity.COMMON: "⚪ Common",
            TitleRarity.UNCOMMON: "🟢 Uncommon",
            TitleRarity.RARE: "🔵 Rare",
            TitleRarity.EPIC: "🟣 Epic",
            TitleRarity.LEGENDARY: "🟡 Legendary",
            TitleRarity.MYTHIC: "🔴 Mythic",
        }
        
        lines = [
            "╔════════════════════════════════════╗",
            f"║  {title.name:^32}  ║",
            f"║  {rarity_colors.get(title.rarity, 'Unknown'):^32}  ║",
            "╠════════════════════════════════════╣",
        ]
        
        # Description
        desc = title.description
        while desc:
            lines.append(f"║  {desc[:32]:32}  ║")
            desc = desc[32:]
        
        lines.append("╠════════════════════════════════════╣")
        
        if title.prefix:
            lines.append(f"║  Prefix: {title.prefix:^23}  ║")
        if title.suffix:
            lines.append(f"║  Suffix: {title.suffix:^23}  ║")
        if title.xp_bonus > 0:
            lines.append(f"║  XP Bonus: +{title.xp_bonus}%                     ║")
        
        lines.append("╠════════════════════════════════════╣")
        
        if owned and earned:
            lines.append("║  ✓ OWNED                           ║")
            lines.append(f"║  Equipped {earned.times_equipped} times                 ║")
        else:
            lines.append("║  ✗ NOT OWNED                       ║")
            lines.append(f"║  Unlock: {title.unlock_condition[:23]:23}  ║")
        
        lines.append("╚════════════════════════════════════╝")
        
        return lines
    
    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "earned_titles": {
                tid: {
                    "title_id": et.title_id,
                    "earned_at": et.earned_at,
                    "earned_from": et.earned_from,
                    "times_equipped": et.times_equipped,
                    "is_favorite": et.is_favorite,
                }
                for tid, et in self.earned_titles.items()
            },
            "current_title": self.current_title,
            "duck_nickname": self.duck_nickname,
            "owner_nickname": self.owner_nickname,
            "total_titles_earned": self.total_titles_earned,
            "favorite_titles": self.favorite_titles,
            "title_display_mode": self.title_display_mode,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "TitlesSystem":
        """Create from dictionary."""
        system = cls()
        
        for tid, tdata in data.get("earned_titles", {}).items():
            system.earned_titles[tid] = EarnedTitle(
                title_id=tdata["title_id"],
                earned_at=tdata["earned_at"],
                earned_from=tdata.get("earned_from", "unknown"),
                times_equipped=tdata.get("times_equipped", 0),
                is_favorite=tdata.get("is_favorite", False),
            )
        
        system.current_title = data.get("current_title")
        system.duck_nickname = data.get("duck_nickname", "Cheese")
        system.owner_nickname = data.get("owner_nickname", "Friend")
        system.total_titles_earned = data.get("total_titles_earned", 0)
        system.favorite_titles = data.get("favorite_titles", [])
        system.title_display_mode = data.get("title_display_mode", "prefix")
        
        return system


# Global titles system instance
titles_system = TitlesSystem()
