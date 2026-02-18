"""
Badges Display System - Visual achievement showcase.
Displays earned achievements as collectible badges.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum


class BadgeRarity(Enum):
    """Rarity of badges."""
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    DIAMOND = "diamond"
    LEGENDARY = "legendary"


class BadgeCategory(Enum):
    """Categories of badges."""
    CARE = "care"
    ACTIVITIES = "activities"
    EXPLORATION = "exploration"
    SOCIAL = "social"
    COLLECTION = "collection"
    MASTERY = "mastery"
    SECRET = "secret"
    SEASONAL = "seasonal"
    SPECIAL = "special"


@dataclass
class Badge:
    """Definition of a badge."""
    id: str
    name: str
    description: str
    category: BadgeCategory
    rarity: BadgeRarity
    icon: str  # Emoji or ASCII
    ascii_art: List[str]
    requirement: str
    points: int = 10
    secret: bool = False


@dataclass
class EarnedBadge:
    """A badge that has been earned."""
    badge_id: str
    earned_at: str
    showcase_position: Optional[int] = None  # Position in showcase (1-6)


# Define all badges
BADGES: Dict[str, Badge] = {
    # Care badges
    "first_feeding": Badge(
        id="first_feeding",
        name="First Meal",
        description="Feed your duck for the first time",
        category=BadgeCategory.CARE,
        rarity=BadgeRarity.BRONZE,
        icon="B",
        ascii_art=["[B]"],
        requirement="Feed once",
        points=5
    ),
    "dedicated_feeder": Badge(
        id="dedicated_feeder",
        name="Dedicated Feeder",
        description="Feed your duck 100 times",
        category=BadgeCategory.CARE,
        rarity=BadgeRarity.SILVER,
        icon="X",
        ascii_art=["[X]"],
        requirement="Feed 100 times",
        points=25
    ),
    "master_chef": Badge(
        id="master_chef",
        name="Master Chef",
        description="Feed your duck 1000 times",
        category=BadgeCategory.CARE,
        rarity=BadgeRarity.GOLD,
        icon="[C]",
        ascii_art=["[[C]]"],
        requirement="Feed 1000 times",
        points=100
    ),
    "petting_pro": Badge(
        id="petting_pro",
        name="Petting Pro",
        description="Pet your duck 500 times",
        category=BadgeCategory.CARE,
        rarity=BadgeRarity.SILVER,
        icon="*",
        ascii_art=["[*]"],
        requirement="Pet 500 times",
        points=30
    ),
    "best_friend": Badge(
        id="best_friend",
        name="Best Friend",
        description="Maintain maximum happiness for 7 days",
        category=BadgeCategory.CARE,
        rarity=BadgeRarity.GOLD,
        icon="<3",
        ascii_art=["[<3]"],
        requirement="Max happiness 7 days",
        points=75
    ),
    
    # Activity badges
    "first_game": Badge(
        id="first_game",
        name="Player One",
        description="Play your first minigame",
        category=BadgeCategory.ACTIVITIES,
        rarity=BadgeRarity.BRONZE,
        icon="[>]",
        ascii_art=["[[>]]"],
        requirement="Play 1 minigame",
        points=5
    ),
    "game_master": Badge(
        id="game_master",
        name="Game Master",
        description="Win 100 minigames",
        category=BadgeCategory.ACTIVITIES,
        rarity=BadgeRarity.GOLD,
        icon="[#]",
        ascii_art=["[[#]]"],
        requirement="Win 100 minigames",
        points=100
    ),
    "angler": Badge(
        id="angler",
        name="Expert Angler",
        description="Catch 50 fish",
        category=BadgeCategory.ACTIVITIES,
        rarity=BadgeRarity.SILVER,
        icon="><>",
        ascii_art=["[><>]"],
        requirement="Catch 50 fish",
        points=35
    ),
    "legendary_fisher": Badge(
        id="legendary_fisher",
        name="Legendary Fisher",
        description="Catch a legendary fish",
        category=BadgeCategory.ACTIVITIES,
        rarity=BadgeRarity.PLATINUM,
        icon="><>",
        ascii_art=["[><>*]"],
        requirement="Catch legendary fish",
        points=150
    ),
    "green_thumb": Badge(
        id="green_thumb",
        name="Green Thumb",
        description="Grow 25 plants",
        category=BadgeCategory.ACTIVITIES,
        rarity=BadgeRarity.SILVER,
        icon="i",
        ascii_art=["[i]"],
        requirement="Grow 25 plants",
        points=30
    ),
    "trick_master": Badge(
        id="trick_master",
        name="Trick Master",
        description="Learn all basic tricks",
        category=BadgeCategory.ACTIVITIES,
        rarity=BadgeRarity.GOLD,
        icon="(!)",
        ascii_art=["[(!)]"],
        requirement="Learn all basic tricks",
        points=80
    ),
    
    # Exploration badges
    "explorer": Badge(
        id="explorer",
        name="Explorer",
        description="Discover 5 new areas",
        category=BadgeCategory.EXPLORATION,
        rarity=BadgeRarity.BRONZE,
        icon="[?]",
        ascii_art=["[[?]]"],
        requirement="Discover 5 areas",
        points=20
    ),
    "treasure_hunter": Badge(
        id="treasure_hunter",
        name="Treasure Hunter",
        description="Find 10 treasures",
        category=BadgeCategory.EXPLORATION,
        rarity=BadgeRarity.SILVER,
        icon="[D]",
        ascii_art=["[[D]]"],
        requirement="Find 10 treasures",
        points=40
    ),
    "world_traveler": Badge(
        id="world_traveler",
        name="World Traveler",
        description="Visit every location",
        category=BadgeCategory.EXPLORATION,
        rarity=BadgeRarity.PLATINUM,
        icon="O",
        ascii_art=["[O]"],
        requirement="Visit all locations",
        points=200
    ),
    
    # Social badges
    "first_friend": Badge(
        id="first_friend",
        name="First Friend",
        description="Make your first duck friend",
        category=BadgeCategory.SOCIAL,
        rarity=BadgeRarity.BRONZE,
        icon="*",
        ascii_art=["[*]"],
        requirement="Make 1 friend",
        points=15
    ),
    "popular_duck": Badge(
        id="popular_duck",
        name="Popular Duck",
        description="Have 10 duck friends",
        category=BadgeCategory.SOCIAL,
        rarity=BadgeRarity.GOLD,
        icon="[+]",
        ascii_art=["[[+]]"],
        requirement="Have 10 friends",
        points=75
    ),
    "generous_giver": Badge(
        id="generous_giver",
        name="Generous Giver",
        description="Give 50 gifts",
        category=BadgeCategory.SOCIAL,
        rarity=BadgeRarity.SILVER,
        icon="[+]",
        ascii_art=["[[+]]"],
        requirement="Give 50 gifts",
        points=35
    ),
    "quest_hero": Badge(
        id="quest_hero",
        name="Quest Hero",
        description="Complete 10 quests",
        category=BadgeCategory.SOCIAL,
        rarity=BadgeRarity.GOLD,
        icon="[=]",
        ascii_art=["[[=]]"],
        requirement="Complete 10 quests",
        points=80
    ),
    
    # Collection badges
    "collector": Badge(
        id="collector",
        name="Collector",
        description="Collect 25 unique items",
        category=BadgeCategory.COLLECTION,
        rarity=BadgeRarity.SILVER,
        icon="[#]",
        ascii_art=["[[#]]"],
        requirement="Collect 25 items",
        points=30
    ),
    "fashionista": Badge(
        id="fashionista",
        name="Fashionista",
        description="Own 20 outfits",
        category=BadgeCategory.COLLECTION,
        rarity=BadgeRarity.GOLD,
        icon="*",
        ascii_art=["[*]"],
        requirement="Own 20 outfits",
        points=60
    ),
    "completionist": Badge(
        id="completionist",
        name="Completionist",
        description="Complete a collectible set",
        category=BadgeCategory.COLLECTION,
        rarity=BadgeRarity.PLATINUM,
        icon="[#]",
        ascii_art=["[[#]]"],
        requirement="Complete 1 set",
        points=100
    ),
    
    # Mastery badges
    "level_10": Badge(
        id="level_10",
        name="Rising Star",
        description="Reach level 10",
        category=BadgeCategory.MASTERY,
        rarity=BadgeRarity.BRONZE,
        icon="*",
        ascii_art=["[*]"],
        requirement="Reach level 10",
        points=20
    ),
    "level_25": Badge(
        id="level_25",
        name="Expert",
        description="Reach level 25",
        category=BadgeCategory.MASTERY,
        rarity=BadgeRarity.SILVER,
        icon="*",
        ascii_art=["[*]"],
        requirement="Reach level 25",
        points=50
    ),
    "level_50": Badge(
        id="level_50",
        name="Master",
        description="Reach level 50",
        category=BadgeCategory.MASTERY,
        rarity=BadgeRarity.GOLD,
        icon="*",
        ascii_art=["[*]"],
        requirement="Reach level 50",
        points=100
    ),
    "level_100": Badge(
        id="level_100",
        name="Legend",
        description="Reach level 100",
        category=BadgeCategory.MASTERY,
        rarity=BadgeRarity.DIAMOND,
        icon="!",
        ascii_art=["[!]"],
        requirement="Reach level 100",
        points=500
    ),
    "prestige_1": Badge(
        id="prestige_1",
        name="Prestige I",
        description="Prestige for the first time",
        category=BadgeCategory.MASTERY,
        rarity=BadgeRarity.PLATINUM,
        icon="^",
        ascii_art=["[^]"],
        requirement="Prestige once",
        points=250
    ),
    
    # Secret badges
    "easter_egg": Badge(
        id="easter_egg",
        name="Easter Egg Hunter",
        description="Find a hidden secret",
        category=BadgeCategory.SECRET,
        rarity=BadgeRarity.GOLD,
        icon="o",
        ascii_art=["[o]"],
        requirement="???",
        points=50,
        secret=True
    ),
    "midnight_duck": Badge(
        id="midnight_duck",
        name="Midnight Duck",
        description="Play at midnight",
        category=BadgeCategory.SECRET,
        rarity=BadgeRarity.SILVER,
        icon=")",
        ascii_art=["[)]"],
        requirement="???",
        points=30,
        secret=True
    ),
    "year_veteran": Badge(
        id="year_veteran",
        name="Year Veteran",
        description="Play for a full year",
        category=BadgeCategory.SECRET,
        rarity=BadgeRarity.LEGENDARY,
        icon="[*]",
        ascii_art=["[[*]]"],
        requirement="???",
        points=1000,
        secret=True
    ),
    
    # Seasonal badges
    "spring_spirit": Badge(
        id="spring_spirit",
        name="Spring Spirit",
        description="Participate in Spring Festival",
        category=BadgeCategory.SEASONAL,
        rarity=BadgeRarity.SILVER,
        icon="~",
        ascii_art=["[~]"],
        requirement="Spring Festival",
        points=40
    ),
    "summer_sun": Badge(
        id="summer_sun",
        name="Summer Sun",
        description="Participate in Summer Festival",
        category=BadgeCategory.SEASONAL,
        rarity=BadgeRarity.SILVER,
        icon="*",
        ascii_art=["[*]"],
        requirement="Summer Festival",
        points=40
    ),
    "autumn_leaf": Badge(
        id="autumn_leaf",
        name="Autumn Leaf",
        description="Participate in Harvest Festival",
        category=BadgeCategory.SEASONAL,
        rarity=BadgeRarity.SILVER,
        icon="~",
        ascii_art=["[~]"],
        requirement="Harvest Festival",
        points=40
    ),
    "winter_wonder": Badge(
        id="winter_wonder",
        name="Winter Wonder",
        description="Participate in Winter Festival",
        category=BadgeCategory.SEASONAL,
        rarity=BadgeRarity.SILVER,
        icon="*️",
        ascii_art=["[*️]"],
        requirement="Winter Festival",
        points=40
    ),
}


class BadgesSystem:
    """
    System for displaying and managing achievement badges.
    """
    
    SHOWCASE_SIZE = 6  # Number of badges in showcase
    
    def __init__(self):
        self.earned_badges: Dict[str, EarnedBadge] = {}
        self.showcase: List[str] = []  # Badge IDs in showcase order
        self.total_points: int = 0
        self.favorite_badge: Optional[str] = None
    
    # Alias for backwards compat — game.py calls award_badge
    def award_badge(self, badge_id: str) -> Optional[Badge]:
        """Alias for earn_badge (backwards compat)."""
        return self.earn_badge(badge_id)

    def earn_badge(self, badge_id: str) -> Optional[Badge]:
        """Earn a badge. Returns the badge if newly earned, None if already had."""
        if badge_id not in BADGES:
            return None
        
        if badge_id in self.earned_badges:
            return None  # Already earned
        
        badge = BADGES[badge_id]
        
        self.earned_badges[badge_id] = EarnedBadge(
            badge_id=badge_id,
            earned_at=datetime.now().isoformat()
        )
        
        self.total_points += badge.points
        
        return badge
    
    def has_badge(self, badge_id: str) -> bool:
        """Check if a badge has been earned."""
        return badge_id in self.earned_badges
    
    def get_earned_count(self) -> Tuple[int, int]:
        """Get count of earned badges vs total."""
        # Don't count secret badges in total unless earned
        visible_total = sum(1 for b in BADGES.values() if not b.secret)
        earned_secrets = sum(1 for bid in self.earned_badges if BADGES.get(bid, Badge("", "", "", BadgeCategory.CARE, BadgeRarity.BRONZE, "", [], "")).secret)
        
        return len(self.earned_badges), visible_total + earned_secrets
    
    def get_badges_by_category(self, category: BadgeCategory) -> List[Tuple[Badge, bool]]:
        """Get badges in a category with earned status."""
        badges = []
        for badge in BADGES.values():
            if badge.category != category:
                continue
            if badge.secret and badge.id not in self.earned_badges:
                continue  # Hide unearned secrets
            badges.append((badge, badge.id in self.earned_badges))
        return badges
    
    def add_to_showcase(self, badge_id: str) -> bool:
        """Add a badge to the showcase."""
        if badge_id not in self.earned_badges:
            return False
        
        if badge_id in self.showcase:
            return False  # Already in showcase
        
        if len(self.showcase) >= self.SHOWCASE_SIZE:
            return False  # Showcase full
        
        self.showcase.append(badge_id)
        return True
    
    def remove_from_showcase(self, badge_id: str) -> bool:
        """Remove a badge from the showcase."""
        if badge_id not in self.showcase:
            return False
        
        self.showcase.remove(badge_id)
        return True
    
    def set_favorite(self, badge_id: str) -> bool:
        """Set a badge as favorite."""
        if badge_id not in self.earned_badges:
            return False
        
        self.favorite_badge = badge_id
        return True
    
    def get_rarity_count(self) -> Dict[BadgeRarity, Tuple[int, int]]:
        """Get earned count by rarity."""
        counts = {}
        
        for rarity in BadgeRarity:
            total = sum(1 for b in BADGES.values() if b.rarity == rarity and not b.secret)
            earned = sum(1 for bid in self.earned_badges if BADGES.get(bid) and BADGES[bid].rarity == rarity)
            counts[rarity] = (earned, total)
        
        return counts
    
    def render_showcase(self) -> List[str]:
        """Render the badge showcase."""
        lines = [
            "+===============================================+",
            "|            [*] BADGE SHOWCASE [*]               |",
            "+===============================================+",
        ]
        
        if not self.showcase:
            lines.append("|  Your showcase is empty!                      |")
            lines.append("|  Add badges to show off your achievements!    |")
        else:
            # Display showcase badges in a grid
            row = "|  "
            for i, badge_id in enumerate(self.showcase):
                badge = BADGES.get(badge_id)
                if badge:
                    row += f" {badge.icon} "
                if (i + 1) % 3 == 0:
                    row += "                       |"
                    lines.append(row)
                    row = "|  "
            
            if len(self.showcase) % 3 != 0:
                row += " " * (3 - (len(self.showcase) % 3)) * 4
                row += "                       |"
                lines.append(row)
            
            # Badge names
            lines.append("|                                               |")
            for badge_id in self.showcase:
                badge = BADGES.get(badge_id)
                if badge:
                    lines.append(f"|  - {badge.name:<40}  |")
        
        earned, total = self.get_earned_count()
        lines.extend([
            "+===============================================+",
            f"|  Badges: {earned}/{total}  Points: {self.total_points:^20}  |",
            "+===============================================+",
        ])
        
        return lines
    
    def render_badge_collection(self, category: Optional[BadgeCategory] = None, page: int = 1) -> List[str]:
        """Render the full badge collection."""
        lines = [
            "+===============================================+",
            "|          [#] BADGE COLLECTION [#]               |",
            "+===============================================+",
        ]
        
        # Filter badges
        if category:
            badges = self.get_badges_by_category(category)
            cat_name = category.value.upper()
            lines.append(f"|  Category: {cat_name:<32}  |")
        else:
            badges = [(b, b.id in self.earned_badges) for b in BADGES.values() if not b.secret or b.id in self.earned_badges]
        
        lines.append("+===============================================+")
        
        # Paginate
        per_page = 6
        start = (page - 1) * per_page
        end = start + per_page
        page_badges = badges[start:end]
        
        rarity_colors = {
            BadgeRarity.BRONZE: "[B]",
            BadgeRarity.SILVER: "[S]",
            BadgeRarity.GOLD: "[G]",
            BadgeRarity.PLATINUM: "[P]",
            BadgeRarity.DIAMOND: "[D]",
            BadgeRarity.LEGENDARY: "[L]",
        }
        
        for badge, earned in page_badges:
            status = "[x]" if earned else "[ ]"
            rarity_icon = rarity_colors.get(badge.rarity, "[S]")
            
            lines.append(f"|  {status} {badge.icon} {badge.name:<28} {rarity_icon}  |")
            
            if earned:
                lines.append(f"|      {badge.description[:38]:<38}  |")
            else:
                lines.append(f"|      Requirement: {badge.requirement:<24}  |")
            
            lines.append(f"|      Points: {badge.points:<30}  |")
            lines.append("|                                               |")
        
        total_pages = (len(badges) + per_page - 1) // per_page
        total_pages = max(1, total_pages)
        
        lines.extend([
            "+===============================================+",
            f"|  Page {page}/{total_pages}  [<-/->] Navigate  [S] Showcase    |",
            "+===============================================+",
        ])
        
        return lines
    
    def render_mini_showcase(self) -> str:
        """Render a compact showcase for the HUD."""
        if not self.showcase:
            return "[*] [ - - - ]"
        
        icons = ""
        for badge_id in self.showcase[:3]:  # Show first 3
            badge = BADGES.get(badge_id)
            if badge:
                icons += badge.icon
        
        return f"[*] [{icons}]"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "earned_badges": {
                bid: {
                    "badge_id": eb.badge_id,
                    "earned_at": eb.earned_at,
                    "showcase_position": eb.showcase_position,
                }
                for bid, eb in self.earned_badges.items()
            },
            "showcase": self.showcase,
            "total_points": self.total_points,
            "favorite_badge": self.favorite_badge,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "BadgesSystem":
        """Create from dictionary."""
        system = cls()
        
        earned = data.get("earned_badges", {})
        for bid, eb_data in earned.items():
            system.earned_badges[bid] = EarnedBadge(
                badge_id=eb_data["badge_id"],
                earned_at=eb_data.get("earned_at", ""),
                showcase_position=eb_data.get("showcase_position"),
            )
        
        system.showcase = data.get("showcase", [])
        system.total_points = data.get("total_points", 0)
        system.favorite_badge = data.get("favorite_badge")
        
        return system


# Global instance
badges_system = BadgesSystem()
