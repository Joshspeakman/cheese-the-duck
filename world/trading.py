"""
Trading System - Item trading between ducks and NPCs.
Includes trade offers, negotiation, and special traders.
"""
from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random


class TraderType(Enum):
    """Types of traders."""
    TRAVELING_MERCHANT = "traveling_merchant"
    DUCK_COLLECTOR = "duck_collector"
    RARE_ITEM_DEALER = "rare_item_dealer"
    FOOD_VENDOR = "food_vendor"
    SEASONAL_TRADER = "seasonal_trader"
    MYSTERY_TRADER = "mystery_trader"


class TradeRarity(Enum):
    """Rarity of trade offers."""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    LEGENDARY = "legendary"


@dataclass
class TradeItem:
    """An item in a trade."""
    item_id: str
    item_name: str
    quantity: int = 1
    is_special: bool = False


@dataclass
class TradeOffer:
    """A trade offer from a trader."""
    id: str
    trader_type: TraderType
    trader_name: str
    description: str
    you_give: List[TradeItem]
    you_get: List[TradeItem]
    rarity: TradeRarity
    expires_at: str  # ISO format
    times_available: int = 1  # How many times can be traded
    friendship_required: int = 0  # 0-100
    special_dialogue: str = ""


@dataclass
class Trader:
    """A trader NPC."""
    id: str
    name: str
    trader_type: TraderType
    greeting: str
    farewell: str
    ascii_art: List[str]
    personality: str
    favorite_items: List[str]
    visit_days: List[int]  # 0=Monday, 6=Sunday


# Define traders
TRADERS: Dict[str, Trader] = {
    "merchant_mallard": Trader(
        id="merchant_mallard",
        name="Merchant Mallard",
        trader_type=TraderType.TRAVELING_MERCHANT,
        greeting="Quack quack! Welcome to my traveling shop!",
        farewell="Safe travels, friend! Come back soon!",
        ascii_art=[
            "    [^]    ",
            "   d [#]   ",
            "  /|  |\\   ",
            " *TRADE*   ",
        ],
        personality="Friendly and enthusiastic",
        favorite_items=["shiny_pebble", "rare_feather"],
        visit_days=[1, 3, 5]  # Tue, Thu, Sat
    ),
    
    "collector_clara": Trader(
        id="collector_clara",
        name="Collector Clara",
        trader_type=TraderType.DUCK_COLLECTOR,
        greeting="Oh my! Do you have any rare items for my collection?",
        farewell="Thank you for the trade! My collection grows!",
        ascii_art=[
            "   (o)      ",
            "  [^]d      ",
            "  ##        ",
            " *examine* ",
        ],
        personality="Meticulous and excited about rarities",
        favorite_items=["golden_feather", "ancient_artifact"],
        visit_days=[0, 6]  # Mon, Sun
    ),
    
    "mysterious_shadow": Trader(
        id="mysterious_shadow",
        name="???",
        trader_type=TraderType.MYSTERY_TRADER,
        greeting="...You seek something special?",
        farewell="...We shall meet again...",
        ascii_art=[
            "    ?       ",
            "   d        ",
            "  ....      ",
            " *mystery* ",
        ],
        personality="Enigmatic and cryptic",
        favorite_items=["mystery_box", "dark_essence"],
        visit_days=[2]  # Only Wednesday (rare)
    ),
    
    "chef_quackers": Trader(
        id="chef_quackers",
        name="Chef Quackers",
        trader_type=TraderType.FOOD_VENDOR,
        greeting="Bon appetit! Looking for gourmet ingredients?",
        farewell="May your meals be delicious!",
        ascii_art=[
            "    [C]     ",
            "   d (o)   ",
            "   ~~~~    ",
            " *sizzle* ",
        ],
        personality="Passionate about food",
        favorite_items=["rare_berry", "golden_wheat"],
        visit_days=[0, 2, 4]  # Mon, Wed, Fri
    ),
    
    "seasonal_sprite": Trader(
        id="seasonal_sprite",
        name="Seasonal Sprite",
        trader_type=TraderType.SEASONAL_TRADER,
        greeting="The season brings special treasures!",
        farewell="Until the seasons change!",
        ascii_art=[
            "   *~      ",
            "    d      ",
            "   ~*~     ",
            " *magical* ",
        ],
        personality="Whimsical and nature-loving",
        favorite_items=["spring_bloom", "autumn_leaf", "winter_crystal", "summer_sun"],
        visit_days=[5, 6]  # Sat, Sun
    ),
}

# Trade offer templates
TRADE_TEMPLATES: List[Dict] = [
    # Common trades
    {
        "id": "bread_for_coins",
        "trader_types": [TraderType.FOOD_VENDOR],
        "you_give": [TradeItem("coins", "Coins", 20)],
        "you_get": [TradeItem("premium_bread", "Premium Bread", 3)],
        "rarity": TradeRarity.COMMON,
        "description": "Fresh artisan bread!",
    },
    {
        "id": "pebble_exchange",
        "trader_types": [TraderType.TRAVELING_MERCHANT],
        "you_give": [TradeItem("shiny_pebble", "Shiny Pebble", 5)],
        "you_get": [TradeItem("coins", "Coins", 50)],
        "rarity": TradeRarity.COMMON,
        "description": "I collect these pebbles!",
    },
    {
        "id": "feather_for_decoration",
        "trader_types": [TraderType.DUCK_COLLECTOR],
        "you_give": [TradeItem("colorful_feather", "Colorful Feather", 3)],
        "you_get": [TradeItem("feather_decoration", "Feather Decoration", 1)],
        "rarity": TradeRarity.UNCOMMON,
        "description": "I'll make something beautiful!",
    },
    {
        "id": "mystery_exchange",
        "trader_types": [TraderType.MYSTERY_TRADER],
        "you_give": [TradeItem("coins", "Coins", 100)],
        "you_get": [TradeItem("mystery_box", "Mystery Box", 1)],
        "rarity": TradeRarity.RARE,
        "description": "What's inside? Only luck decides...",
    },
    {
        "id": "seasonal_bundle",
        "trader_types": [TraderType.SEASONAL_TRADER],
        "you_give": [TradeItem("coins", "Coins", 75)],
        "you_get": [TradeItem("seasonal_bundle", "Seasonal Bundle", 1)],
        "rarity": TradeRarity.UNCOMMON,
        "description": "Special items for this season!",
    },
    {
        "id": "rare_recipe",
        "trader_types": [TraderType.FOOD_VENDOR],
        "you_give": [TradeItem("rare_ingredient", "Rare Ingredient", 2)],
        "you_get": [TradeItem("secret_recipe", "Secret Recipe", 1)],
        "rarity": TradeRarity.RARE,
        "description": "My grandmother's secret!",
    },
    {
        "id": "golden_trade",
        "trader_types": [TraderType.DUCK_COLLECTOR, TraderType.RARE_ITEM_DEALER],
        "you_give": [TradeItem("golden_feather", "Golden Feather", 1)],
        "you_get": [TradeItem("coins", "Coins", 500), TradeItem("rare_hat", "Rare Hat", 1)],
        "rarity": TradeRarity.LEGENDARY,
        "description": "A magnificent specimen!",
    },
    {
        "id": "bulk_fish",
        "trader_types": [TraderType.TRAVELING_MERCHANT],
        "you_give": [TradeItem("common_fish", "Common Fish", 10)],
        "you_get": [TradeItem("coins", "Coins", 80), TradeItem("fish_trophy", "Fish Trophy", 1)],
        "rarity": TradeRarity.UNCOMMON,
        "description": "That's a lot of fish!",
    },
]


class TradingSystem:
    """
    System for trading with NPCs.
    """
    
    def __init__(self):
        self.active_traders: List[str] = []  # Currently visiting trader IDs
        self.current_offers: List[TradeOffer] = []
        self.completed_trades: int = 0
        self.total_items_traded: int = 0
        self.trader_friendships: Dict[str, int] = {}  # trader_id -> friendship (0-100)
        self.last_trader_refresh: str = ""
        self.trade_history: List[Dict] = []  # Recent trades
        self.lucky_trades: int = 0  # Trades with bonus rewards
    
    def refresh_traders(self) -> List[Trader]:
        """Refresh which traders are visiting today."""
        today = date.today()
        today_str = today.isoformat()
        
        if today_str == self.last_trader_refresh:
            return [TRADERS[tid] for tid in self.active_traders if tid in TRADERS]
        
        self.last_trader_refresh = today_str
        weekday = today.weekday()  # 0=Monday
        
        # Find traders who visit today
        self.active_traders = []
        for trader_id, trader in TRADERS.items():
            if weekday in trader.visit_days:
                self.active_traders.append(trader_id)
        
        # Generate new offers
        self.generate_offers()
        
        return [TRADERS[tid] for tid in self.active_traders if tid in TRADERS]
    
    def generate_offers(self):
        """Generate trade offers from active traders."""
        self.current_offers = []
        
        for trader_id in self.active_traders:
            trader = TRADERS.get(trader_id)
            if not trader:
                continue
            
            # Generate 2-4 offers per trader
            num_offers = random.randint(2, 4)
            suitable_templates = [
                t for t in TRADE_TEMPLATES
                if trader.trader_type in t["trader_types"]
            ]
            
            if not suitable_templates:
                continue
            
            selected = random.sample(
                suitable_templates,
                min(num_offers, len(suitable_templates))
            )
            
            for i, template in enumerate(selected):
                expires = (datetime.now() + timedelta(hours=24)).isoformat()
                
                offer = TradeOffer(
                    id=f"{trader_id}_{template['id']}_{i}",
                    trader_type=trader.trader_type,
                    trader_name=trader.name,
                    description=template["description"],
                    you_give=template["you_give"].copy(),
                    you_get=template["you_get"].copy(),
                    rarity=template["rarity"],
                    expires_at=expires,
                    times_available=random.randint(1, 3),
                    special_dialogue=self.get_trader_dialogue(trader, template["rarity"])
                )
                
                self.current_offers.append(offer)
    
    def get_trader_dialogue(self, trader: Trader, rarity: TradeRarity) -> str:
        """Get appropriate dialogue for a trade."""
        dialogues = {
            TraderType.TRAVELING_MERCHANT: {
                TradeRarity.COMMON: "A fair deal for both of us!",
                TradeRarity.UNCOMMON: "This is a special offer just for you!",
                TradeRarity.RARE: "I don't offer this to just anyone...",
                TradeRarity.LEGENDARY: "Once in a lifetime opportunity!",
            },
            TraderType.DUCK_COLLECTOR: {
                TradeRarity.COMMON: "A fine addition to any collection!",
                TradeRarity.UNCOMMON: "Ooh, this one is quite nice!",
                TradeRarity.RARE: "Magnificent! Simply magnificent!",
                TradeRarity.LEGENDARY: "I've waited years for this!",
            },
            TraderType.MYSTERY_TRADER: {
                TradeRarity.COMMON: "...fate guides this trade...",
                TradeRarity.UNCOMMON: "...the shadows approve...",
                TradeRarity.RARE: "...destiny calls...",
                TradeRarity.LEGENDARY: "...the stars align...",
            },
            TraderType.FOOD_VENDOR: {
                TradeRarity.COMMON: "Fresh and delicious!",
                TradeRarity.UNCOMMON: "Made with love!",
                TradeRarity.RARE: "My special recipe!",
                TradeRarity.LEGENDARY: "The finest in all the land!",
            },
            TraderType.SEASONAL_TRADER: {
                TradeRarity.COMMON: "A gift from nature!",
                TradeRarity.UNCOMMON: "Blessed by the season!",
                TradeRarity.RARE: "Rare seasonal magic!",
                TradeRarity.LEGENDARY: "Pure seasonal essence!",
            },
        }
        
        trader_dialogues = dialogues.get(trader.trader_type, {})
        return trader_dialogues.get(rarity, "A good trade!")
    
    def get_offers_for_trader(self, trader_id: str) -> List[TradeOffer]:
        """Get offers from a specific trader."""
        trader = TRADERS.get(trader_id)
        if not trader:
            return []
        
        return [o for o in self.current_offers if o.trader_name == trader.name and o.times_available > 0]
    
    def can_complete_trade(self, offer: TradeOffer, inventory: Dict[str, int]) -> bool:
        """Check if player can complete a trade."""
        if offer.times_available <= 0:
            return False
        
        # Check friendship requirement
        trader_id = next((tid for tid, t in TRADERS.items() if t.name == offer.trader_name), None)
        if trader_id and offer.friendship_required > 0:
            friendship = self.trader_friendships.get(trader_id, 0)
            if friendship < offer.friendship_required:
                return False
        
        # Check inventory
        for item in offer.you_give:
            if item.item_id == "coins":
                if inventory.get("coins", 0) < item.quantity:
                    return False
            else:
                if inventory.get(item.item_id, 0) < item.quantity:
                    return False
        
        return True
    
    def complete_trade(self, offer: TradeOffer) -> Tuple[List[TradeItem], bool]:
        """
        Complete a trade. Returns (items_received, was_lucky).
        Caller is responsible for updating inventory.
        """
        if offer.times_available <= 0:
            return [], False
        
        offer.times_available -= 1
        self.completed_trades += 1
        
        # Count items traded
        for item in offer.you_give:
            self.total_items_traded += item.quantity
        for item in offer.you_get:
            self.total_items_traded += item.quantity
        
        # Check for lucky bonus (10% chance)
        was_lucky = random.random() < 0.1
        items_received = list(offer.you_get)
        
        if was_lucky:
            self.lucky_trades += 1
            # Add bonus item or increase quantity
            if items_received:
                bonus_item = TradeItem(
                    item_id="lucky_coin",
                    item_name="Lucky Coin",
                    quantity=1,
                    is_special=True
                )
                items_received.append(bonus_item)
        
        # Increase friendship with trader
        trader_id = next((tid for tid, t in TRADERS.items() if t.name == offer.trader_name), None)
        if trader_id:
            current = self.trader_friendships.get(trader_id, 0)
            friendship_gain = {
                TradeRarity.COMMON: 1,
                TradeRarity.UNCOMMON: 2,
                TradeRarity.RARE: 5,
                TradeRarity.LEGENDARY: 10,
            }.get(offer.rarity, 1)
            self.trader_friendships[trader_id] = min(100, current + friendship_gain)
        
        # Record in history
        self.trade_history.append({
            "offer_id": offer.id,
            "trader": offer.trader_name,
            "timestamp": datetime.now().isoformat(),
            "was_lucky": was_lucky,
        })
        
        # Keep history manageable
        if len(self.trade_history) > 50:
            self.trade_history = self.trade_history[-50:]
        
        return items_received, was_lucky
    
    def get_trader_friendship(self, trader_id: str) -> int:
        """Get friendship level with a trader."""
        return self.trader_friendships.get(trader_id, 0)
    
    def render_trader_selection(self) -> List[str]:
        """Render the trader selection screen."""
        lines = [
            "+===============================================+",
            "|            [=] TRADING POST [=]              |",
            "+===============================================+",
        ]
        
        traders = self.refresh_traders()
        
        if not traders:
            lines.append("|  No traders visiting today!                   |")
            lines.append("|  Check back tomorrow.                         |")
            lines.append("|                                               |")
            lines.append("|  Traders visit on different days:             |")
            for trader in TRADERS.values():
                days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                visit_days = [days[d] for d in trader.visit_days]
                lines.append(f"|  - {trader.name}: {', '.join(visit_days):^20}  |")
        else:
            lines.append("|  Today's Visitors:                            |")
            lines.append("|                                               |")
            
            for i, trader in enumerate(traders, 1):
                friendship = self.get_trader_friendship(trader.id)
                heart = "<3" if friendship > 50 else "<"
                offers = len(self.get_offers_for_trader(trader.id))
                
                lines.append(f"|  [{i}] {trader.name:<30} {heart}  |")
                lines.append(f"|      {trader.personality[:35]:<35}  |")
                lines.append(f"|      Offers: {offers}  Friendship: {friendship}/100        |")
                lines.append("|                                               |")
        
        lines.extend([
            "+===============================================+",
            f"|  Total Trades: {self.completed_trades}  Lucky: {self.lucky_trades:^17}  |",
            "+===============================================+",
        ])
        
        return lines
    
    def render_trader_offers(self, trader_id: str) -> List[str]:
        """Render offers from a specific trader."""
        trader = TRADERS.get(trader_id)
        if not trader:
            return ["Trader not found!"]
        
        offers = self.get_offers_for_trader(trader_id)
        friendship = self.get_trader_friendship(trader_id)
        
        lines = [
            "+===============================================+",
            f"|  [=] {trader.name:^38} [=] |",
            "+===============================================+",
        ]
        
        # Trader art and greeting
        for art_line in trader.ascii_art:
            lines.append(f"|  {art_line:^43}  |")
        
        lines.append(f"|  \"{trader.greeting[:40]}\"  |")
        lines.append(f"|  Friendship: {friendship}/100                          |")
        lines.append("+===============================================+")
        
        if not offers:
            lines.append("|  No offers available right now!               |")
        else:
            for i, offer in enumerate(offers, 1):
                rarity_icons = {
                    TradeRarity.COMMON: "o",
                    TradeRarity.UNCOMMON: "+",
                    TradeRarity.RARE: "*",
                    TradeRarity.LEGENDARY: "#",
                }
                icon = rarity_icons.get(offer.rarity, "o")
                
                lines.append(f"|  [{i}] {icon} {offer.rarity.value.upper():<12}           x{offer.times_available} |")
                lines.append(f"|      {offer.description[:40]:<40}  |")
                
                give_str = ", ".join(f"{item.item_name}x{item.quantity}" for item in offer.you_give)[:35]
                get_str = ", ".join(f"{item.item_name}x{item.quantity}" for item in offer.you_get)[:35]
                
                lines.append(f"|      Give: {give_str:<35}  |")
                lines.append(f"|      Get:  {get_str:<35}  |")
                lines.append("|                                               |")
        
        lines.extend([
            "+===============================================+",
            "|  [#] Select trade  [B] Back                   |",
            "+===============================================+",
        ])
        
        return lines
    
    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "completed_trades": self.completed_trades,
            "total_items_traded": self.total_items_traded,
            "trader_friendships": self.trader_friendships,
            "last_trader_refresh": self.last_trader_refresh,
            "trade_history": self.trade_history[-30:],  # Keep last 30
            "lucky_trades": self.lucky_trades,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "TradingSystem":
        """Create from dictionary."""
        system = cls()
        system.completed_trades = data.get("completed_trades", 0)
        system.total_items_traded = data.get("total_items_traded", 0)
        system.trader_friendships = data.get("trader_friendships", {})
        system.last_trader_refresh = data.get("last_trader_refresh", "")
        system.trade_history = data.get("trade_history", [])
        system.lucky_trades = data.get("lucky_trades", 0)
        return system


# Global instance
trading_system = TradingSystem()
