using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace StupidDuck.World;

/// <summary>
/// Types of traders that can visit
/// </summary>
public enum TraderType
{
    TravelingMerchant,
    DuckCollector,
    RareItemDealer,
    FoodVendor,
    SeasonalTrader,
    MysteryTrader
}

/// <summary>
/// Rarity of trade offers
/// </summary>
public enum TradeRarity
{
    Common,
    Uncommon,
    Rare,
    Legendary
}

/// <summary>
/// An item that can be traded
/// </summary>
public class TradeItem
{
    public string ItemId { get; set; } = "";
    public string ItemName { get; set; } = "";
    public int Quantity { get; set; } = 1;
    public bool IsSpecial { get; set; } = false;

    public TradeItem() { }

    public TradeItem(string itemId, string itemName, int quantity, bool isSpecial = false)
    {
        ItemId = itemId;
        ItemName = itemName;
        Quantity = quantity;
        IsSpecial = isSpecial;
    }

    public Dictionary<string, object> ToSaveData()
    {
        return new Dictionary<string, object>
        {
            ["item_id"] = ItemId,
            ["item_name"] = ItemName,
            ["quantity"] = Quantity,
            ["is_special"] = IsSpecial
        };
    }

    public static TradeItem FromSaveData(Dictionary<string, object> data)
    {
        return new TradeItem
        {
            ItemId = data.GetValueOrDefault("item_id")?.ToString() ?? "",
            ItemName = data.GetValueOrDefault("item_name")?.ToString() ?? "",
            Quantity = Convert.ToInt32(data.GetValueOrDefault("quantity", 1)),
            IsSpecial = Convert.ToBoolean(data.GetValueOrDefault("is_special", false))
        };
    }
}

/// <summary>
/// A trade offer from a trader
/// </summary>
public class TradeOffer
{
    public string Id { get; set; } = "";
    public string TraderName { get; set; } = "";
    public string Description { get; set; } = "";
    public List<TradeItem> YouGive { get; set; } = new();
    public List<TradeItem> YouGet { get; set; } = new();
    public TradeRarity Rarity { get; set; } = TradeRarity.Common;
    public int FriendshipRequired { get; set; } = 0;
    public int TimesAvailable { get; set; } = 1;
    public string SpecialDialogue { get; set; } = "";
}

/// <summary>
/// A trader who visits the duck
/// </summary>
public class Trader
{
    public string Id { get; set; } = "";
    public string Name { get; set; } = "";
    public TraderType TraderType { get; set; }
    public string Greeting { get; set; } = "";
    public string Farewell { get; set; } = "";
    public List<string> AsciiArt { get; set; } = new();
    public string Personality { get; set; } = "";
    public List<string> FavoriteItems { get; set; } = new();
    public List<DayOfWeek> VisitDays { get; set; } = new();
}

/// <summary>
/// Template for generating trade offers
/// </summary>
public class TradeTemplate
{
    public string TemplateId { get; set; } = "";
    public string Description { get; set; } = "";
    public List<TradeItem> YouGive { get; set; } = new();
    public List<TradeItem> YouGet { get; set; } = new();
    public TradeRarity Rarity { get; set; } = TradeRarity.Common;
    public int FriendshipRequired { get; set; } = 0;
}

/// <summary>
/// Trading system for duck to trade with visiting merchants
/// </summary>
public class TradingSystem
{
    private static readonly Random _random = new();

    // All available traders
    private static readonly Dictionary<string, Trader> _traders = new()
    {
        ["merchant_mallard"] = new Trader
        {
            Id = "merchant_mallard",
            Name = "Merchant Mallard",
            TraderType = TraderType.TravelingMerchant,
            Greeting = "Welcome, welcome! The finest goods in all the land!",
            Farewell = "Safe travels, friend! Come back soon!",
            AsciiArt = new List<string>
            {
                "  __",
                @" /o \",
                "(  _/)",
                " \\__/"
            },
            Personality = "A friendly traveling merchant with goods from far lands",
            FavoriteItems = new List<string> { "coins", "gems", "rare_feathers" },
            VisitDays = new List<DayOfWeek> { DayOfWeek.Tuesday, DayOfWeek.Thursday, DayOfWeek.Saturday }
        },
        ["collector_clara"] = new Trader
        {
            Id = "collector_clara",
            Name = "Collector Clara",
            TraderType = TraderType.DuckCollector,
            Greeting = "Oh my! What wonderful treasures you have!",
            Farewell = "These will make fine additions to my collection!",
            AsciiArt = new List<string>
            {
                " ♦♦♦",
                "(◕‿◕)",
                " \\=/",
                " / \\"
            },
            Personality = "An eccentric collector seeking rare duck memorabilia",
            FavoriteItems = new List<string> { "feathers", "photos", "collectibles" },
            VisitDays = new List<DayOfWeek> { DayOfWeek.Monday, DayOfWeek.Sunday }
        },
        ["mysterious_shadow"] = new Trader
        {
            Id = "mysterious_shadow",
            Name = "Mysterious Shadow",
            TraderType = TraderType.MysteryTrader,
            Greeting = "...the darkness brings gifts...",
            Farewell = "...until the shadows call again...",
            AsciiArt = new List<string>
            {
                " ????",
                "(•_•)",
                " ▓▓▓",
                " ░░░"
            },
            Personality = "A mysterious figure who appears only at midnight",
            FavoriteItems = new List<string> { "mystery_items", "shadow_essence", "secrets" },
            VisitDays = new List<DayOfWeek> { DayOfWeek.Wednesday }
        },
        ["chef_quackers"] = new Trader
        {
            Id = "chef_quackers",
            Name = "Chef Quackers",
            TraderType = TraderType.FoodVendor,
            Greeting = "Hungry? My recipes are legendary!",
            Farewell = "Bon appétit, mon ami!",
            AsciiArt = new List<string>
            {
                " 👨‍🍳",
                "(^o^)",
                " |[]|",
                " /  \\"
            },
            Personality = "A renowned duck chef with delectable treats",
            FavoriteItems = new List<string> { "bread", "vegetables", "fish" },
            VisitDays = new List<DayOfWeek> { DayOfWeek.Monday, DayOfWeek.Wednesday, DayOfWeek.Friday }
        },
        ["seasonal_sprite"] = new Trader
        {
            Id = "seasonal_sprite",
            Name = "Seasonal Sprite",
            TraderType = TraderType.SeasonalTrader,
            Greeting = "The season's blessings upon you!",
            Farewell = "May nature guide your path!",
            AsciiArt = new List<string>
            {
                " ✨🌸✨",
                " (◠‿◠)",
                "  ~~~",
                "  \\|/"
            },
            Personality = "A magical sprite who brings seasonal treasures",
            FavoriteItems = new List<string> { "flowers", "seasonal_items", "nature_gifts" },
            VisitDays = new List<DayOfWeek> { DayOfWeek.Saturday, DayOfWeek.Sunday }
        }
    };

    // Trade templates for generating offers
    private static readonly List<TradeTemplate> _tradeTemplates = new()
    {
        new TradeTemplate
        {
            TemplateId = "bread_for_coins",
            Description = "Trade bread for shiny coins",
            YouGive = new List<TradeItem> { new("bread", "Bread", 3) },
            YouGet = new List<TradeItem> { new("coins", "Coins", 10) },
            Rarity = TradeRarity.Common,
            FriendshipRequired = 0
        },
        new TradeTemplate
        {
            TemplateId = "pebble_exchange",
            Description = "Special pebbles for decorations",
            YouGive = new List<TradeItem> { new("shiny_pebble", "Shiny Pebble", 5) },
            YouGet = new List<TradeItem> { new("garden_gnome", "Garden Gnome", 1) },
            Rarity = TradeRarity.Uncommon,
            FriendshipRequired = 10
        },
        new TradeTemplate
        {
            TemplateId = "feather_for_decoration",
            Description = "Trade rare feathers for pond decorations",
            YouGive = new List<TradeItem> { new("golden_feather", "Golden Feather", 1) },
            YouGet = new List<TradeItem> { new("lily_pad", "Lily Pad", 3), new("flower_patch", "Flower Patch", 2) },
            Rarity = TradeRarity.Rare,
            FriendshipRequired = 25
        },
        new TradeTemplate
        {
            TemplateId = "mystery_exchange",
            Description = "A mysterious trade... who knows what you'll get?",
            YouGive = new List<TradeItem> { new("mystery_box", "Mystery Box", 1) },
            YouGet = new List<TradeItem> { new("???", "???", 1, true) },
            Rarity = TradeRarity.Rare,
            FriendshipRequired = 15
        },
        new TradeTemplate
        {
            TemplateId = "seasonal_bundle",
            Description = "Seasonal items at a special price",
            YouGive = new List<TradeItem> { new("coins", "Coins", 50) },
            YouGet = new List<TradeItem> { new("seasonal_bundle", "Seasonal Bundle", 1, true) },
            Rarity = TradeRarity.Uncommon,
            FriendshipRequired = 5
        },
        new TradeTemplate
        {
            TemplateId = "rare_recipe",
            Description = "A secret recipe from distant lands",
            YouGive = new List<TradeItem> { new("coins", "Coins", 100), new("rare_ingredient", "Rare Ingredient", 3) },
            YouGet = new List<TradeItem> { new("legendary_recipe", "Legendary Recipe", 1, true) },
            Rarity = TradeRarity.Legendary,
            FriendshipRequired = 50
        },
        new TradeTemplate
        {
            TemplateId = "golden_trade",
            Description = "The golden opportunity of a lifetime!",
            YouGive = new List<TradeItem> { new("golden_feather", "Golden Feather", 3) },
            YouGet = new List<TradeItem> { new("golden_crown", "Golden Crown", 1, true) },
            Rarity = TradeRarity.Legendary,
            FriendshipRequired = 75
        },
        new TradeTemplate
        {
            TemplateId = "bulk_fish",
            Description = "Fresh fish in bulk at a discount",
            YouGive = new List<TradeItem> { new("coins", "Coins", 25) },
            YouGet = new List<TradeItem> { new("fish", "Fresh Fish", 5) },
            Rarity = TradeRarity.Common,
            FriendshipRequired = 0
        },
        new TradeTemplate
        {
            TemplateId = "collectible_trade",
            Description = "Rare collectibles exchange",
            YouGive = new List<TradeItem> { new("common_collectible", "Common Collectible", 10) },
            YouGet = new List<TradeItem> { new("rare_collectible", "Rare Collectible", 1, true) },
            Rarity = TradeRarity.Rare,
            FriendshipRequired = 30
        },
        new TradeTemplate
        {
            TemplateId = "gourmet_ingredients",
            Description = "Premium cooking ingredients",
            YouGive = new List<TradeItem> { new("coins", "Coins", 40) },
            YouGet = new List<TradeItem> { new("truffle", "Truffle", 2), new("saffron", "Saffron", 1) },
            Rarity = TradeRarity.Uncommon,
            FriendshipRequired = 20
        }
    };

    // Instance state
    public List<Trader> ActiveTraders { get; private set; } = new();
    public List<TradeOffer> CurrentOffers { get; private set; } = new();
    public int CompletedTrades { get; private set; } = 0;
    public int TotalItemsTraded { get; private set; } = 0;
    public Dictionary<string, int> TraderFriendships { get; private set; } = new();
    public string LastTraderRefresh { get; private set; } = "";
    public List<TradeHistoryEntry> TradeHistory { get; private set; } = new();
    public int LuckyTrades { get; private set; } = 0;

    public TradingSystem()
    {
    }

    /// <summary>
    /// Refresh available traders based on current day
    /// </summary>
    public List<Trader> RefreshTraders()
    {
        string today = DateTime.Now.ToString("yyyy-MM-dd");

        // Only refresh once per day
        if (LastTraderRefresh == today)
        {
            return ActiveTraders;
        }

        LastTraderRefresh = today;
        ActiveTraders.Clear();
        CurrentOffers.Clear();

        DayOfWeek currentDay = DateTime.Now.DayOfWeek;

        // Find traders available today
        foreach (var kvp in _traders)
        {
            if (kvp.Value.VisitDays.Contains(currentDay))
            {
                ActiveTraders.Add(kvp.Value);
            }
        }

        // Generate offers for each active trader
        foreach (var trader in ActiveTraders)
        {
            GenerateOffers(trader);
        }

        return ActiveTraders;
    }

    /// <summary>
    /// Generate trade offers for a trader
    /// </summary>
    private void GenerateOffers(Trader trader)
    {
        // Select 2-4 random templates
        int numOffers = _random.Next(2, 5);
        var shuffledTemplates = _tradeTemplates.OrderBy(_ => _random.Next()).ToList();

        foreach (var template in shuffledTemplates.Take(numOffers))
        {
            var offer = new TradeOffer
            {
                Id = Guid.NewGuid().ToString(),
                TraderName = trader.Name,
                Description = template.Description,
                YouGive = template.YouGive.Select(i => new TradeItem(i.ItemId, i.ItemName, i.Quantity, i.IsSpecial)).ToList(),
                YouGet = template.YouGet.Select(i => new TradeItem(i.ItemId, i.ItemName, i.Quantity, i.IsSpecial)).ToList(),
                Rarity = template.Rarity,
                FriendshipRequired = template.FriendshipRequired,
                TimesAvailable = _random.Next(1, 4),
                SpecialDialogue = GetTraderDialogue(trader, template.Rarity)
            };

            CurrentOffers.Add(offer);
        }
    }

    /// <summary>
    /// Get appropriate dialogue for a trade based on rarity
    /// </summary>
    public string GetTraderDialogue(Trader trader, TradeRarity rarity)
    {
        var dialogues = new Dictionary<TraderType, Dictionary<TradeRarity, string>>
        {
            [TraderType.TravelingMerchant] = new()
            {
                [TradeRarity.Common] = "A fair deal for both of us!",
                [TradeRarity.Uncommon] = "This is a special offer just for you!",
                [TradeRarity.Rare] = "I don't offer this to just anyone...",
                [TradeRarity.Legendary] = "Once in a lifetime opportunity!"
            },
            [TraderType.DuckCollector] = new()
            {
                [TradeRarity.Common] = "A fine addition to any collection!",
                [TradeRarity.Uncommon] = "Ooh, this one is quite nice!",
                [TradeRarity.Rare] = "Magnificent! Simply magnificent!",
                [TradeRarity.Legendary] = "I've waited years for this!"
            },
            [TraderType.MysteryTrader] = new()
            {
                [TradeRarity.Common] = "...fate guides this trade...",
                [TradeRarity.Uncommon] = "...the shadows approve...",
                [TradeRarity.Rare] = "...destiny calls...",
                [TradeRarity.Legendary] = "...the stars align..."
            },
            [TraderType.FoodVendor] = new()
            {
                [TradeRarity.Common] = "Fresh and delicious!",
                [TradeRarity.Uncommon] = "Made with love!",
                [TradeRarity.Rare] = "My special recipe!",
                [TradeRarity.Legendary] = "The finest in all the land!"
            },
            [TraderType.SeasonalTrader] = new()
            {
                [TradeRarity.Common] = "A gift from nature!",
                [TradeRarity.Uncommon] = "Blessed by the season!",
                [TradeRarity.Rare] = "Rare seasonal magic!",
                [TradeRarity.Legendary] = "Pure seasonal essence!"
            },
            [TraderType.RareItemDealer] = new()
            {
                [TradeRarity.Common] = "A classic piece!",
                [TradeRarity.Uncommon] = "Quite the find!",
                [TradeRarity.Rare] = "Exceptionally rare!",
                [TradeRarity.Legendary] = "The rarest of the rare!"
            }
        };

        if (dialogues.TryGetValue(trader.TraderType, out var traderDialogues))
        {
            if (traderDialogues.TryGetValue(rarity, out var dialogue))
            {
                return dialogue;
            }
        }

        return "A good trade!";
    }

    /// <summary>
    /// Get offers from a specific trader
    /// </summary>
    public List<TradeOffer> GetOffersForTrader(string traderId)
    {
        if (!_traders.TryGetValue(traderId, out var trader))
        {
            return new List<TradeOffer>();
        }

        return CurrentOffers
            .Where(o => o.TraderName == trader.Name && o.TimesAvailable > 0)
            .ToList();
    }

    /// <summary>
    /// Check if player can complete a trade
    /// </summary>
    public bool CanCompleteTrade(TradeOffer offer, Dictionary<string, int> inventory)
    {
        if (offer.TimesAvailable <= 0)
        {
            return false;
        }

        // Check friendship requirement
        var traderId = _traders.FirstOrDefault(kvp => kvp.Value.Name == offer.TraderName).Key;
        if (!string.IsNullOrEmpty(traderId) && offer.FriendshipRequired > 0)
        {
            int friendship = TraderFriendships.GetValueOrDefault(traderId, 0);
            if (friendship < offer.FriendshipRequired)
            {
                return false;
            }
        }

        // Check inventory
        foreach (var item in offer.YouGive)
        {
            if (!inventory.TryGetValue(item.ItemId, out int quantity) || quantity < item.Quantity)
            {
                return false;
            }
        }

        return true;
    }

    /// <summary>
    /// Complete a trade. Returns items received and whether it was lucky.
    /// Caller is responsible for updating inventory.
    /// </summary>
    public (List<TradeItem> itemsReceived, bool wasLucky) CompleteTrade(TradeOffer offer)
    {
        if (offer.TimesAvailable <= 0)
        {
            return (new List<TradeItem>(), false);
        }

        offer.TimesAvailable--;
        CompletedTrades++;

        // Count items traded
        foreach (var item in offer.YouGive)
        {
            TotalItemsTraded += item.Quantity;
        }
        foreach (var item in offer.YouGet)
        {
            TotalItemsTraded += item.Quantity;
        }

        // Check for lucky bonus (10% chance)
        bool wasLucky = _random.NextDouble() < 0.1;
        var itemsReceived = offer.YouGet.Select(i => new TradeItem(i.ItemId, i.ItemName, i.Quantity, i.IsSpecial)).ToList();

        if (wasLucky)
        {
            LuckyTrades++;
            // Add bonus lucky coin
            itemsReceived.Add(new TradeItem("lucky_coin", "Lucky Coin", 1, true));
        }

        // Increase friendship with trader
        var traderId = _traders.FirstOrDefault(kvp => kvp.Value.Name == offer.TraderName).Key;
        if (!string.IsNullOrEmpty(traderId))
        {
            int current = TraderFriendships.GetValueOrDefault(traderId, 0);
            int friendshipGain = offer.Rarity switch
            {
                TradeRarity.Common => 1,
                TradeRarity.Uncommon => 2,
                TradeRarity.Rare => 5,
                TradeRarity.Legendary => 10,
                _ => 1
            };
            TraderFriendships[traderId] = Math.Min(100, current + friendshipGain);
        }

        // Record in history
        TradeHistory.Add(new TradeHistoryEntry
        {
            OfferId = offer.Id,
            TraderName = offer.TraderName,
            Timestamp = DateTime.Now,
            WasLucky = wasLucky
        });

        // Keep history manageable
        if (TradeHistory.Count > 50)
        {
            TradeHistory = TradeHistory.Skip(TradeHistory.Count - 50).ToList();
        }

        return (itemsReceived, wasLucky);
    }

    /// <summary>
    /// Get friendship level with a trader
    /// </summary>
    public int GetTraderFriendship(string traderId)
    {
        return TraderFriendships.GetValueOrDefault(traderId, 0);
    }

    /// <summary>
    /// Get all traders (for UI display purposes)
    /// </summary>
    public static IReadOnlyDictionary<string, Trader> GetAllTraders() => _traders;

    /// <summary>
    /// Get all trade templates (for debug/testing)
    /// </summary>
    public static IReadOnlyList<TradeTemplate> GetAllTemplates() => _tradeTemplates;

    /// <summary>
    /// Render trader selection screen
    /// </summary>
    public List<string> RenderTraderSelection()
    {
        var lines = new List<string>
        {
            "╔═══════════════════════════════════════════════╗",
            "║            🛒 TRADING POST 🛒                 ║",
            "╠═══════════════════════════════════════════════╣"
        };

        var traders = RefreshTraders();

        if (!traders.Any())
        {
            lines.Add("║  No traders visiting today!                   ║");
            lines.Add("║  Check back tomorrow.                         ║");
            lines.Add("║                                               ║");
            lines.Add("║  Traders visit on different days:             ║");
            
            string[] days = { "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat" };
            foreach (var trader in _traders.Values)
            {
                var visitDays = trader.VisitDays.Select(d => days[(int)d]);
                string daysStr = string.Join(", ", visitDays).PadLeft(20).PadRight(20);
                lines.Add($"║  • {trader.Name}: {daysStr}  ║");
            }
        }
        else
        {
            lines.Add("║  Today's Visitors:                            ║");
            lines.Add("║                                               ║");

            int i = 1;
            foreach (var trader in traders)
            {
                int friendship = GetTraderFriendship(trader.Id);
                string heart = friendship > 50 ? "❤️" : "🤍";
                int offers = GetOffersForTrader(trader.Id).Count;

                lines.Add($"║  [{i}] {trader.Name,-30} {heart}  ║");
                lines.Add($"║      {trader.Personality[..Math.Min(35, trader.Personality.Length)],-35}  ║");
                lines.Add($"║      Offers: {offers}  Friendship: {friendship}/100        ║");
                lines.Add("║                                               ║");
                i++;
            }
        }

        lines.Add("╠═══════════════════════════════════════════════╣");
        lines.Add($"║  Total Trades: {CompletedTrades}  Lucky: {LuckyTrades,-17}  ║");
        lines.Add("╚═══════════════════════════════════════════════╝");

        return lines;
    }

    /// <summary>
    /// Render offers from a specific trader
    /// </summary>
    public List<string> RenderTraderOffers(string traderId)
    {
        if (!_traders.TryGetValue(traderId, out var trader))
        {
            return new List<string> { "Trader not found!" };
        }

        var offers = GetOffersForTrader(traderId);
        int friendship = GetTraderFriendship(traderId);

        var lines = new List<string>
        {
            "╔═══════════════════════════════════════════════╗",
            $"║  🛒 {trader.Name,38} 🛒 ║",
            "╠═══════════════════════════════════════════════╣"
        };

        // Trader art and greeting
        foreach (var artLine in trader.AsciiArt)
        {
            string centered = artLine.PadLeft((43 + artLine.Length) / 2).PadRight(43);
            lines.Add($"║  {centered}  ║");
        }

        string greeting = trader.Greeting.Length > 40 ? trader.Greeting[..40] : trader.Greeting;
        lines.Add($"║  \"{greeting}\"  ║");
        lines.Add($"║  Friendship: {friendship}/100                          ║");
        lines.Add("╠═══════════════════════════════════════════════╣");

        if (!offers.Any())
        {
            lines.Add("║  No offers available right now!               ║");
        }
        else
        {
            int i = 1;
            foreach (var offer in offers)
            {
                string icon = offer.Rarity switch
                {
                    TradeRarity.Common => "⚪",
                    TradeRarity.Uncommon => "🟢",
                    TradeRarity.Rare => "🔵",
                    TradeRarity.Legendary => "🟡",
                    _ => "⚪"
                };

                string rarityName = offer.Rarity.ToString().ToUpper();
                lines.Add($"║  [{i}] {icon} {rarityName,-12}           x{offer.TimesAvailable} ║");
                
                string desc = offer.Description.Length > 40 ? offer.Description[..40] : offer.Description;
                lines.Add($"║      {desc,-40}  ║");

                string giveStr = string.Join(", ", offer.YouGive.Select(item => $"{item.ItemName}x{item.Quantity}"));
                if (giveStr.Length > 35) giveStr = giveStr[..35];
                
                string getStr = string.Join(", ", offer.YouGet.Select(item => $"{item.ItemName}x{item.Quantity}"));
                if (getStr.Length > 35) getStr = getStr[..35];

                lines.Add($"║      Give: {giveStr,-35}  ║");
                lines.Add($"║      Get:  {getStr,-35}  ║");
                lines.Add("║                                               ║");
                i++;
            }
        }

        lines.Add("╠═══════════════════════════════════════════════╣");
        lines.Add("║  [#] Select trade  [B] Back                   ║");
        lines.Add("╚═══════════════════════════════════════════════╝");

        return lines;
    }

    /// <summary>
    /// Convert to save data
    /// </summary>
    public Dictionary<string, object> ToSaveData()
    {
        return new Dictionary<string, object>
        {
            ["completed_trades"] = CompletedTrades,
            ["total_items_traded"] = TotalItemsTraded,
            ["trader_friendships"] = TraderFriendships,
            ["last_trader_refresh"] = LastTraderRefresh,
            ["trade_history"] = TradeHistory.TakeLast(30).Select(h => h.ToSaveData()).ToList(),
            ["lucky_trades"] = LuckyTrades
        };
    }

    /// <summary>
    /// Load from save data
    /// </summary>
    public static TradingSystem FromSaveData(Dictionary<string, object> data)
    {
        var system = new TradingSystem
        {
            CompletedTrades = Convert.ToInt32(data.GetValueOrDefault("completed_trades", 0)),
            TotalItemsTraded = Convert.ToInt32(data.GetValueOrDefault("total_items_traded", 0)),
            LastTraderRefresh = data.GetValueOrDefault("last_trader_refresh")?.ToString() ?? "",
            LuckyTrades = Convert.ToInt32(data.GetValueOrDefault("lucky_trades", 0))
        };

        if (data.TryGetValue("trader_friendships", out var friendships) && friendships is JsonElement friendshipsElement)
        {
            foreach (var prop in friendshipsElement.EnumerateObject())
            {
                system.TraderFriendships[prop.Name] = prop.Value.GetInt32();
            }
        }
        else if (friendships is Dictionary<string, object> friendshipsDict)
        {
            foreach (var kvp in friendshipsDict)
            {
                system.TraderFriendships[kvp.Key] = Convert.ToInt32(kvp.Value);
            }
        }

        if (data.TryGetValue("trade_history", out var history) && history is JsonElement historyElement)
        {
            foreach (var item in historyElement.EnumerateArray())
            {
                var entry = new TradeHistoryEntry
                {
                    OfferId = item.GetProperty("offer_id").GetString() ?? "",
                    TraderName = item.GetProperty("trader").GetString() ?? "",
                    Timestamp = DateTime.Parse(item.GetProperty("timestamp").GetString() ?? DateTime.Now.ToString()),
                    WasLucky = item.GetProperty("was_lucky").GetBoolean()
                };
                system.TradeHistory.Add(entry);
            }
        }

        return system;
    }
}

/// <summary>
/// Record of a completed trade
/// </summary>
public class TradeHistoryEntry
{
    public string OfferId { get; set; } = "";
    public string TraderName { get; set; } = "";
    public DateTime Timestamp { get; set; } = DateTime.Now;
    public bool WasLucky { get; set; } = false;

    public Dictionary<string, object> ToSaveData()
    {
        return new Dictionary<string, object>
        {
            ["offer_id"] = OfferId,
            ["trader"] = TraderName,
            ["timestamp"] = Timestamp.ToString("o"),
            ["was_lucky"] = WasLucky
        };
    }
}
