"""
Prestige/Legacy System - Long-term progression with rebirth mechanics.
Features prestige levels, legacy bonuses, and generational unlocks.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
import threading


class LegacyTier(Enum):
    """Tiers of legacy progression."""
    NEWCOMER = "newcomer"
    FAMILIAR = "familiar"
    ESTABLISHED = "established"
    HONORED = "honored"
    LEGENDARY = "legendary"
    MYTHICAL = "mythical"
    ETERNAL = "eternal"


@dataclass
class LegacyBonus:
    """A permanent bonus from legacy progression."""
    id: str
    name: str
    description: str
    tier: LegacyTier
    prestige_requirement: int
    bonus_type: str  # xp_mult, coin_mult, unlock, cosmetic, ability
    bonus_value: float
    icon: str


@dataclass
class PrestigeReward:
    """Reward for prestiging."""
    prestige_level: int
    legacy_points: int
    special_unlock: Optional[str]
    title: str
    cosmetic_id: Optional[str]


@dataclass
class DuckLegacy:
    """Legacy information from a previous duck."""
    duck_name: str
    days_lived: int
    max_level: int
    achievements_earned: int
    prestige_date: str
    memorable_moment: str


# Legacy bonuses that can be unlocked
LEGACY_BONUSES: Dict[str, LegacyBonus] = {
    # Newcomer tier (0-1 prestige)
    "xp_bonus_1": LegacyBonus(
        id="xp_bonus_1",
        name="Experience Boost I",
        description="+5% XP from all sources",
        tier=LegacyTier.NEWCOMER,
        prestige_requirement=1,
        bonus_type="xp_mult",
        bonus_value=1.05,
        icon="^",
    ),
    "starting_coins": LegacyBonus(
        id="starting_coins",
        name="Inheritance",
        description="Start with 100 bonus coins",
        tier=LegacyTier.NEWCOMER,
        prestige_requirement=1,
        bonus_type="starting_bonus",
        bonus_value=100,
        icon="$",
    ),
    
    # Familiar tier (2-4 prestige)
    "xp_bonus_2": LegacyBonus(
        id="xp_bonus_2",
        name="Experience Boost II",
        description="+10% XP from all sources",
        tier=LegacyTier.FAMILIAR,
        prestige_requirement=2,
        bonus_type="xp_mult",
        bonus_value=1.10,
        icon="^",
    ),
    "coin_bonus_1": LegacyBonus(
        id="coin_bonus_1",
        name="Coin Collector I",
        description="+5% coins from all sources",
        tier=LegacyTier.FAMILIAR,
        prestige_requirement=3,
        bonus_type="coin_mult",
        bonus_value=1.05,
        icon="c",
    ),
    "unlock_legacy_hat": LegacyBonus(
        id="unlock_legacy_hat",
        name="Legacy Crown",
        description="Unlock the Legacy Crown cosmetic",
        tier=LegacyTier.FAMILIAR,
        prestige_requirement=4,
        bonus_type="cosmetic",
        bonus_value=0,
        icon="^",
    ),
    
    # Established tier (5-9 prestige)
    "xp_bonus_3": LegacyBonus(
        id="xp_bonus_3",
        name="Experience Boost III",
        description="+15% XP from all sources",
        tier=LegacyTier.ESTABLISHED,
        prestige_requirement=5,
        bonus_type="xp_mult",
        bonus_value=1.15,
        icon="^",
    ),
    "faster_growth": LegacyBonus(
        id="faster_growth",
        name="Accelerated Growth",
        description="Duck grows 10% faster",
        tier=LegacyTier.ESTABLISHED,
        prestige_requirement=6,
        bonus_type="growth_mult",
        bonus_value=1.10,
        icon="i",
    ),
    "bonus_daily_rewards": LegacyBonus(
        id="bonus_daily_rewards",
        name="Daily Devotion",
        description="+1 bonus item in daily rewards",
        tier=LegacyTier.ESTABLISHED,
        prestige_requirement=7,
        bonus_type="daily_bonus",
        bonus_value=1,
        icon="[+]",
    ),
    
    # Honored tier (10-14 prestige)
    "xp_bonus_4": LegacyBonus(
        id="xp_bonus_4",
        name="Experience Boost IV",
        description="+25% XP from all sources",
        tier=LegacyTier.HONORED,
        prestige_requirement=10,
        bonus_type="xp_mult",
        bonus_value=1.25,
        icon="^",
    ),
    "coin_bonus_2": LegacyBonus(
        id="coin_bonus_2",
        name="Coin Collector II",
        description="+15% coins from all sources",
        tier=LegacyTier.HONORED,
        prestige_requirement=11,
        bonus_type="coin_mult",
        bonus_value=1.15,
        icon="c",
    ),
    "unlock_golden_aura": LegacyBonus(
        id="unlock_golden_aura",
        name="Golden Aura",
        description="Unlock the Golden Aura effect",
        tier=LegacyTier.HONORED,
        prestige_requirement=12,
        bonus_type="cosmetic",
        bonus_value=0,
        icon="*",
    ),
    
    # Legendary tier (15-24 prestige)
    "xp_bonus_5": LegacyBonus(
        id="xp_bonus_5",
        name="Experience Boost V",
        description="+50% XP from all sources",
        tier=LegacyTier.LEGENDARY,
        prestige_requirement=15,
        bonus_type="xp_mult",
        bonus_value=1.50,
        icon="^",
    ),
    "lucky_drops": LegacyBonus(
        id="lucky_drops",
        name="Legacy Luck",
        description="+10% rare item drop chance",
        tier=LegacyTier.LEGENDARY,
        prestige_requirement=18,
        bonus_type="luck_mult",
        bonus_value=1.10,
        icon="+",
    ),
    "unlock_legend_wings": LegacyBonus(
        id="unlock_legend_wings",
        name="Legendary Wings",
        description="Unlock the Legendary Wings cosmetic",
        tier=LegacyTier.LEGENDARY,
        prestige_requirement=20,
        bonus_type="cosmetic",
        bonus_value=0,
        icon="w",
    ),
    
    # Mythical tier (25-49 prestige)
    "double_daily": LegacyBonus(
        id="double_daily",
        name="Mythical Devotion",
        description="Double daily login rewards",
        tier=LegacyTier.MYTHICAL,
        prestige_requirement=25,
        bonus_type="daily_mult",
        bonus_value=2.0,
        icon="[+]",
    ),
    "xp_bonus_6": LegacyBonus(
        id="xp_bonus_6",
        name="Experience Boost VI",
        description="+100% XP from all sources",
        tier=LegacyTier.MYTHICAL,
        prestige_requirement=30,
        bonus_type="xp_mult",
        bonus_value=2.0,
        icon="^",
    ),
    
    # Eternal tier (50+ prestige)
    "eternal_blessing": LegacyBonus(
        id="eternal_blessing",
        name="Eternal Blessing",
        description="All bonuses increased by 25%",
        tier=LegacyTier.ETERNAL,
        prestige_requirement=50,
        bonus_type="global_mult",
        bonus_value=1.25,
        icon="*",
    ),
    "unlock_eternal_crown": LegacyBonus(
        id="unlock_eternal_crown",
        name="Eternal Crown",
        description="Unlock the Eternal Crown (ultimate cosmetic)",
        tier=LegacyTier.ETERNAL,
        prestige_requirement=50,
        bonus_type="cosmetic",
        bonus_value=0,
        icon="*",
    ),
}

# Prestige rewards for each level
PRESTIGE_REWARDS = {
    1: PrestigeReward(1, 100, "legacy_frame_bronze", "Reborn", "legacy_badge_1"),
    2: PrestigeReward(2, 150, None, "Experienced", "legacy_badge_2"),
    3: PrestigeReward(3, 200, "legacy_frame_silver", "Seasoned", "legacy_badge_3"),
    5: PrestigeReward(5, 300, "legacy_title_veteran", "Veteran", "legacy_badge_5"),
    10: PrestigeReward(10, 500, "legacy_frame_gold", "Honored", "legacy_badge_10"),
    15: PrestigeReward(15, 750, "legacy_title_legend", "Legend", "legacy_badge_15"),
    25: PrestigeReward(25, 1000, "legacy_frame_platinum", "Mythical", "legacy_badge_25"),
    50: PrestigeReward(50, 2000, "legacy_ultimate", "Eternal", "legacy_badge_50"),
}


class PrestigeSystem:
    """
    Manages prestige/legacy progression.
    """
    
    def __init__(self):
        self.prestige_level: int = 0
        self.legacy_points: int = 0
        self.total_legacy_points: int = 0
        self.unlocked_bonuses: List[str] = []
        self.legacy_history: List[DuckLegacy] = []
        self.titles_earned: List[str] = ["Newcomer"]
        self.current_title: str = "Newcomer"
        self.cosmetics_unlocked: List[str] = []
        self.total_ducks_raised: int = 1
        self.total_days_played: int = 0
        self.lifetime_xp: int = 0
        self.lifetime_coins: int = 0
    
    def can_prestige(self, duck_level: int, duck_age_days: int) -> Tuple[bool, str]:
        """Check if player can prestige."""
        min_level = 20  # Minimum level to prestige
        min_days = 7    # Minimum days played
        
        if duck_level < min_level:
            return False, f"Reach level {min_level} to prestige (currently {duck_level})"
        
        if duck_age_days < min_days:
            return False, f"Play for {min_days} days to prestige (currently {duck_age_days})"
        
        return True, "Ready to prestige!"
    
    def prestige(
        self,
        duck_name: str,
        duck_level: int,
        duck_age_days: int,
        achievements_earned: int,
        memorable_moment: str = ""
    ) -> Tuple[bool, str, Dict]:
        """Perform prestige - resets progress with bonuses."""
        can_do, message = self.can_prestige(duck_level, duck_age_days)
        if not can_do:
            return False, message, {}
        
        # Calculate legacy points earned
        base_points = 50
        level_bonus = duck_level * 5
        age_bonus = duck_age_days * 2
        achievement_bonus = achievements_earned * 3
        
        points_earned = base_points + level_bonus + age_bonus + achievement_bonus
        
        # Record legacy
        legacy = DuckLegacy(
            duck_name=duck_name,
            days_lived=duck_age_days,
            max_level=duck_level,
            achievements_earned=achievements_earned,
            prestige_date=datetime.now().isoformat(),
            memorable_moment=memorable_moment or f"{duck_name} lived a wonderful life!",
        )
        self.legacy_history.append(legacy)
        
        # Update stats
        self.prestige_level += 1
        self.legacy_points += points_earned
        self.total_legacy_points += points_earned
        self.total_ducks_raised += 1
        self.total_days_played += duck_age_days
        
        # Check for new unlocks
        new_unlocks = self._check_unlocks()
        
        # Get prestige reward
        reward = PRESTIGE_REWARDS.get(self.prestige_level)
        if reward:
            self.legacy_points += reward.legacy_points
            if reward.title not in self.titles_earned:
                self.titles_earned.append(reward.title)
            if reward.cosmetic_id:
                self.cosmetics_unlocked.append(reward.cosmetic_id)
            if reward.special_unlock:
                new_unlocks.append(reward.special_unlock)
        
        # Calculate starting bonuses for new duck
        starting_bonuses = self._calculate_starting_bonuses()
        
        return True, f"* PRESTIGE {self.prestige_level}! *\nEarned {points_earned} Legacy Points!", {
            "prestige_level": self.prestige_level,
            "points_earned": points_earned,
            "new_unlocks": new_unlocks,
            "starting_bonuses": starting_bonuses,
            "title": reward.title if reward else self.current_title,
        }
    
    def _check_unlocks(self) -> List[str]:
        """Check for new bonus unlocks."""
        new_unlocks = []
        
        for bonus_id, bonus in LEGACY_BONUSES.items():
            if bonus_id not in self.unlocked_bonuses:
                if self.prestige_level >= bonus.prestige_requirement:
                    self.unlocked_bonuses.append(bonus_id)
                    new_unlocks.append(f"{bonus.icon} {bonus.name}")
        
        return new_unlocks
    
    def _calculate_starting_bonuses(self) -> Dict:
        """Calculate bonuses for a new duck."""
        bonuses = {
            "xp_multiplier": 1.0,
            "coin_multiplier": 1.0,
            "starting_coins": 0,
            "growth_multiplier": 1.0,
            "luck_multiplier": 1.0,
            "daily_multiplier": 1.0,
        }
        
        for bonus_id in self.unlocked_bonuses:
            bonus = LEGACY_BONUSES.get(bonus_id)
            if not bonus:
                continue
            
            if bonus.bonus_type == "xp_mult":
                # Take the highest XP multiplier
                bonuses["xp_multiplier"] = max(bonuses["xp_multiplier"], bonus.bonus_value)
            elif bonus.bonus_type == "coin_mult":
                bonuses["coin_multiplier"] = max(bonuses["coin_multiplier"], bonus.bonus_value)
            elif bonus.bonus_type == "starting_bonus":
                bonuses["starting_coins"] += bonus.bonus_value
            elif bonus.bonus_type == "growth_mult":
                bonuses["growth_multiplier"] = max(bonuses["growth_multiplier"], bonus.bonus_value)
            elif bonus.bonus_type == "luck_mult":
                bonuses["luck_multiplier"] = max(bonuses["luck_multiplier"], bonus.bonus_value)
            elif bonus.bonus_type == "daily_mult":
                bonuses["daily_multiplier"] = max(bonuses["daily_multiplier"], bonus.bonus_value)
        
        # Apply global multiplier if unlocked
        if "eternal_blessing" in self.unlocked_bonuses:
            for key in ["xp_multiplier", "coin_multiplier", "luck_multiplier"]:
                bonuses[key] *= 1.25
        
        return bonuses
    
    def spend_legacy_points(self, amount: int) -> Tuple[bool, str]:
        """Spend legacy points on something."""
        if self.legacy_points < amount:
            return False, f"Need {amount - self.legacy_points} more Legacy Points!"
        
        self.legacy_points -= amount
        return True, f"Spent {amount} Legacy Points!"
    
    def get_current_tier(self) -> LegacyTier:
        """Get current legacy tier."""
        if self.prestige_level >= 50:
            return LegacyTier.ETERNAL
        elif self.prestige_level >= 25:
            return LegacyTier.MYTHICAL
        elif self.prestige_level >= 15:
            return LegacyTier.LEGENDARY
        elif self.prestige_level >= 10:
            return LegacyTier.HONORED
        elif self.prestige_level >= 5:
            return LegacyTier.ESTABLISHED
        elif self.prestige_level >= 2:
            return LegacyTier.FAMILIAR
        else:
            return LegacyTier.NEWCOMER
    
    def get_active_bonuses(self) -> List[LegacyBonus]:
        """Get list of active bonuses."""
        return [LEGACY_BONUSES[bid] for bid in self.unlocked_bonuses if bid in LEGACY_BONUSES]
    
    def render_legacy_screen(self) -> List[str]:
        """Render the legacy/prestige screen."""
        tier = self.get_current_tier()
        bonuses = self._calculate_starting_bonuses()
        
        lines = [
            "+==============================================+",
            "|            * LEGACY SYSTEM *               |",
            f"|  Prestige Level: {self.prestige_level:3}                        |",
            f"|  Tier: {tier.value.capitalize():15}                   |",
            f"|  Legacy Points: {self.legacy_points:5}                      |",
            f"|  Title: {self.current_title:20}              |",
            "+==============================================+",
            "|  Active Bonuses:                             |",
            f"|    XP: x{bonuses['xp_multiplier']:.2f}  Coins: x{bonuses['coin_multiplier']:.2f}           |",
            f"|    Growth: x{bonuses['growth_multiplier']:.2f}  Luck: x{bonuses['luck_multiplier']:.2f}         |",
            "+==============================================+",
            "|  Legacy History:                             |",
        ]
        
        for legacy in self.legacy_history[-3:]:  # Show last 3
            lines.append(f"|    d {legacy.duck_name[:12]:12} - {legacy.days_lived}d, Lv{legacy.max_level}       |")
        
        if not self.legacy_history:
            lines.append("|    No previous ducks yet!                    |")
        
        lines.append("+==============================================+")
        lines.append(f"|  Ducks Raised: {self.total_ducks_raised:3}  Total Days: {self.total_days_played:5}      |")
        lines.append("+==============================================+")
        
        return lines
    
    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "prestige_level": self.prestige_level,
            "legacy_points": self.legacy_points,
            "total_legacy_points": self.total_legacy_points,
            "unlocked_bonuses": self.unlocked_bonuses,
            "legacy_history": [
                {
                    "duck_name": l.duck_name,
                    "days_lived": l.days_lived,
                    "max_level": l.max_level,
                    "achievements_earned": l.achievements_earned,
                    "prestige_date": l.prestige_date,
                    "memorable_moment": l.memorable_moment,
                }
                for l in self.legacy_history
            ],
            "titles_earned": self.titles_earned,
            "current_title": self.current_title,
            "cosmetics_unlocked": self.cosmetics_unlocked,
            "total_ducks_raised": self.total_ducks_raised,
            "total_days_played": self.total_days_played,
            "lifetime_xp": self.lifetime_xp,
            "lifetime_coins": self.lifetime_coins,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "PrestigeSystem":
        """Create from dictionary."""
        system = cls()
        
        system.prestige_level = data.get("prestige_level", 0)
        system.legacy_points = data.get("legacy_points", 0)
        system.total_legacy_points = data.get("total_legacy_points", 0)
        system.unlocked_bonuses = data.get("unlocked_bonuses", [])
        
        system.legacy_history = [
            DuckLegacy(
                duck_name=l["duck_name"],
                days_lived=l["days_lived"],
                max_level=l["max_level"],
                achievements_earned=l["achievements_earned"],
                prestige_date=l["prestige_date"],
                memorable_moment=l.get("memorable_moment", ""),
            )
            for l in data.get("legacy_history", [])
        ]
        
        system.titles_earned = data.get("titles_earned", ["Newcomer"])
        system.current_title = data.get("current_title", "Newcomer")
        system.cosmetics_unlocked = data.get("cosmetics_unlocked", [])
        system.total_ducks_raised = data.get("total_ducks_raised", 1)
        system.total_days_played = data.get("total_days_played", 0)
        system.lifetime_xp = data.get("lifetime_xp", 0)
        system.lifetime_coins = data.get("lifetime_coins", 0)
        
        return system


# Lazy singleton pattern with thread-safe initialization
_prestige_system: Optional[PrestigeSystem] = None
_prestige_system_lock = threading.Lock()


def get_prestige_system() -> PrestigeSystem:
    """Get the global prestige system instance (lazy initialization). Thread-safe."""
    global _prestige_system
    if _prestige_system is None:
        with _prestige_system_lock:
            if _prestige_system is None:
                _prestige_system = PrestigeSystem()
    return _prestige_system


# Direct instance for backwards compatibility
prestige_system = PrestigeSystem()
