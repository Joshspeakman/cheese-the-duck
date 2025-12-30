using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;

namespace StupidDuck.World;

/// <summary>
/// Rarity tiers for collectibles
/// </summary>
public enum CollectibleRarity
{
    Common,
    Uncommon,
    Rare,
    Epic,
    Legendary,
    Mythic
}

/// <summary>
/// Types of collectibles
/// </summary>
public enum CollectibleType
{
    Card,
    Sticker,
    Stamp,
    Badge
}

/// <summary>
/// A collectible item
/// </summary>
public class Collectible
{
    public string Id { get; set; } = "";
    public string Name { get; set; } = "";
    public CollectibleType Type { get; set; }
    public CollectibleRarity Rarity { get; set; }
    public string SetId { get; set; } = "";
    public int SetPosition { get; set; } = 0;
    public string Description { get; set; } = "";
    public List<string> ImageArt { get; set; } = new();
    public string FlavorText { get; set; } = "";
    public string? SpecialEffect { get; set; } = null;
}

/// <summary>
/// A set/album of collectibles
/// </summary>
public class CollectibleSet
{
    public string Id { get; set; } = "";
    public string Name { get; set; } = "";
    public string Description { get; set; } = "";
    public string Theme { get; set; } = "";
    public int TotalItems { get; set; } = 0;
    public string SetBonus { get; set; } = "";
    public Dictionary<string, int> BonusReward { get; set; } = new();
}

/// <summary>
/// A collectible owned by the player
/// </summary>
public class OwnedCollectible
{
    public string CollectibleId { get; set; } = "";
    public DateTime ObtainedAt { get; set; } = DateTime.Now;
    public string ObtainedFrom { get; set; } = "";
    public bool IsShiny { get; set; } = false;
    public int DuplicateCount { get; set; } = 0;
}

/// <summary>
/// Collectibles system - cards, stickers, stamps, and albums
/// </summary>
public class CollectiblesSystem
{
    private static readonly Random _random = new();

    // Collectible Sets
    private static readonly Dictionary<string, CollectibleSet> _sets = new()
    {
        ["duck_portraits"] = new CollectibleSet
        {
            Id = "duck_portraits",
            Name = "Duck Portraits Collection",
            Description = "Famous ducks throughout history",
            Theme = "historical",
            TotalItems = 8,
            SetBonus = "Historical Duck Title",
            BonusReward = new Dictionary<string, int> { ["xp"] = 500, ["coins"] = 300 }
        },
        ["pond_life"] = new CollectibleSet
        {
            Id = "pond_life",
            Name = "Life at the Pond",
            Description = "Creatures and plants from the pond",
            Theme = "nature",
            TotalItems = 10,
            SetBonus = "Pond Master Badge",
            BonusReward = new Dictionary<string, int> { ["xp"] = 400, ["coins"] = 250 }
        },
        ["weather_wonders"] = new CollectibleSet
        {
            Id = "weather_wonders",
            Name = "Weather Wonders",
            Description = "Weather phenomena and conditions",
            Theme = "weather",
            TotalItems = 6,
            SetBonus = "Weather Wizard Hat",
            BonusReward = new Dictionary<string, int> { ["xp"] = 350, ["coins"] = 200 }
        },
        ["food_feast"] = new CollectibleSet
        {
            Id = "food_feast",
            Name = "Duck's Feast",
            Description = "Delicious foods for ducks",
            Theme = "food",
            TotalItems = 8,
            SetBonus = "Gourmet Chef Apron",
            BonusReward = new Dictionary<string, int> { ["xp"] = 300, ["coins"] = 200 }
        },
        ["emotions"] = new CollectibleSet
        {
            Id = "emotions",
            Name = "Quack Expressions",
            Description = "Different duck moods and emotions",
            Theme = "emotions",
            TotalItems = 6,
            SetBonus = "Emotion Reader Title",
            BonusReward = new Dictionary<string, int> { ["xp"] = 250, ["coins"] = 150 }
        },
        ["seasons"] = new CollectibleSet
        {
            Id = "seasons",
            Name = "Four Seasons",
            Description = "The beauty of each season",
            Theme = "seasons",
            TotalItems = 4,
            SetBonus = "Seasonal Spirit",
            BonusReward = new Dictionary<string, int> { ["xp"] = 600, ["coins"] = 400 }
        },
        ["legendary_ducks"] = new CollectibleSet
        {
            Id = "legendary_ducks",
            Name = "Legendary Ducks",
            Description = "Mythical and legendary duck beings",
            Theme = "mythology",
            TotalItems = 5,
            SetBonus = "Legendary Status",
            BonusReward = new Dictionary<string, int> { ["xp"] = 1000, ["coins"] = 750 }
        }
    };

    // Individual Collectibles
    private static readonly Dictionary<string, Collectible> _collectibles = new()
    {
        // Duck Portraits Set
        ["portrait_cheese"] = new Collectible
        {
            Id = "portrait_cheese",
            Name = "Cheese Portrait",
            Type = CollectibleType.Card,
            Rarity = CollectibleRarity.Rare,
            SetId = "duck_portraits",
            SetPosition = 1,
            Description = "An elegant portrait of Cheese the Duck",
            ImageArt = new List<string> { "╔══════════╗", "║  .--.    ║", "║ (_ ^ _)  ║", "║  (__)    ║", "╚══════════╝" },
            FlavorText = "The one and only!"
        },
        ["portrait_emperor"] = new Collectible
        {
            Id = "portrait_emperor",
            Name = "Emperor Duck",
            Type = CollectibleType.Card,
            Rarity = CollectibleRarity.Epic,
            SetId = "duck_portraits",
            SetPosition = 2,
            Description = "The legendary Emperor Duck",
            ImageArt = new List<string> { "╔══════════╗", "║  👑      ║", "║ (_ ^ _)  ║", "║  (__)    ║", "╚══════════╝" },
            FlavorText = "Ruler of the Great Pond"
        },
        ["portrait_scholar"] = new Collectible
        {
            Id = "portrait_scholar",
            Name = "Scholar Duck",
            Type = CollectibleType.Card,
            Rarity = CollectibleRarity.Uncommon,
            SetId = "duck_portraits",
            SetPosition = 3,
            Description = "A wise scholar duck with glasses",
            ImageArt = new List<string> { "╔══════════╗", "║  .--.    ║", "║ (o o)    ║", "║  (__)    ║", "╚══════════╝" },
            FlavorText = "Knowledge is power!"
        },
        ["portrait_artist"] = new Collectible
        {
            Id = "portrait_artist",
            Name = "Artist Duck",
            Type = CollectibleType.Card,
            Rarity = CollectibleRarity.Uncommon,
            SetId = "duck_portraits",
            SetPosition = 4,
            Description = "A creative artist duck",
            ImageArt = new List<string> { "╔══════════╗", "║  🎨      ║", "║ (_ ^ _)  ║", "║  (__)    ║", "╚══════════╝" },
            FlavorText = "Every quack is a masterpiece"
        },
        ["portrait_explorer"] = new Collectible
        {
            Id = "portrait_explorer",
            Name = "Explorer Duck",
            Type = CollectibleType.Card,
            Rarity = CollectibleRarity.Rare,
            SetId = "duck_portraits",
            SetPosition = 5,
            Description = "An adventurous explorer",
            ImageArt = new List<string> { "╔══════════╗", "║  ⛏️      ║", "║ (_ ^ _)  ║", "║  (__)    ║", "╚══════════╝" },
            FlavorText = "Adventure awaits!"
        },
        // Pond Life Set
        ["pond_frog"] = new Collectible
        {
            Id = "pond_frog",
            Name = "Friendly Frog",
            Type = CollectibleType.Sticker,
            Rarity = CollectibleRarity.Common,
            SetId = "pond_life",
            SetPosition = 1,
            Description = "A friendly frog from the pond",
            ImageArt = new List<string> { "  @..@  ", " (----)  ", "( >  < ) ", " ^    ^  " },
            FlavorText = "Ribbit!"
        },
        ["pond_lily"] = new Collectible
        {
            Id = "pond_lily",
            Name = "Water Lily",
            Type = CollectibleType.Sticker,
            Rarity = CollectibleRarity.Common,
            SetId = "pond_life",
            SetPosition = 2,
            Description = "A beautiful water lily",
            ImageArt = new List<string> { "  _/\\_  ", " (____)  ", "~~~~~~~" },
            FlavorText = "Peaceful and serene"
        },
        ["pond_dragonfly"] = new Collectible
        {
            Id = "pond_dragonfly",
            Name = "Dragonfly",
            Type = CollectibleType.Sticker,
            Rarity = CollectibleRarity.Uncommon,
            SetId = "pond_life",
            SetPosition = 3,
            Description = "A shimmering dragonfly",
            ImageArt = new List<string> { " \\|/  ", " -o-  ", " /|\\  " },
            FlavorText = "Swift and beautiful"
        },
        ["pond_fish"] = new Collectible
        {
            Id = "pond_fish",
            Name = "Golden Fish",
            Type = CollectibleType.Sticker,
            Rarity = CollectibleRarity.Rare,
            SetId = "pond_life",
            SetPosition = 4,
            Description = "A rare golden fish",
            ImageArt = new List<string> { "  ><>  " },
            FlavorText = "Lucky find!"
        },
        // Weather Wonders Set
        ["weather_sun"] = new Collectible
        {
            Id = "weather_sun",
            Name = "Sunny Day",
            Type = CollectibleType.Stamp,
            Rarity = CollectibleRarity.Common,
            SetId = "weather_wonders",
            SetPosition = 1,
            Description = "A bright sunny day",
            ImageArt = new List<string> { " \\|/  ", "-- ☀ --", " /|\\  " },
            FlavorText = "Perfect weather!"
        },
        ["weather_rain"] = new Collectible
        {
            Id = "weather_rain",
            Name = "Rainy Day",
            Type = CollectibleType.Stamp,
            Rarity = CollectibleRarity.Common,
            SetId = "weather_wonders",
            SetPosition = 2,
            Description = "A cozy rainy day",
            ImageArt = new List<string> { "  ☁️   ", " , , , ", "' ' ' '" },
            FlavorText = "Splish splash!"
        },
        ["weather_rainbow"] = new Collectible
        {
            Id = "weather_rainbow",
            Name = "Rainbow",
            Type = CollectibleType.Stamp,
            Rarity = CollectibleRarity.Epic,
            SetId = "weather_wonders",
            SetPosition = 3,
            Description = "A magical rainbow",
            ImageArt = new List<string> { "  🌈   " },
            FlavorText = "Double rainbow!"
        },
        ["weather_snow"] = new Collectible
        {
            Id = "weather_snow",
            Name = "Snowy Day",
            Type = CollectibleType.Stamp,
            Rarity = CollectibleRarity.Uncommon,
            SetId = "weather_wonders",
            SetPosition = 4,
            Description = "A beautiful snowy day",
            ImageArt = new List<string> { " ❄️ ❄️ ❄️ ", "  ❄️ ❄️  " },
            FlavorText = "Let it snow!"
        },
        // Legendary Ducks Set
        ["legend_phoenix"] = new Collectible
        {
            Id = "legend_phoenix",
            Name = "Phoenix Duck",
            Type = CollectibleType.Card,
            Rarity = CollectibleRarity.Mythic,
            SetId = "legendary_ducks",
            SetPosition = 1,
            Description = "The immortal Phoenix Duck",
            ImageArt = new List<string> { "  🔥🔥🔥  ", " (_ ^ _) ", "  🔥🔥   " },
            FlavorText = "Rises from the ashes",
            SpecialEffect = "Grants rebirth protection once"
        },
        ["legend_dragon"] = new Collectible
        {
            Id = "legend_dragon",
            Name = "Dragon Duck",
            Type = CollectibleType.Card,
            Rarity = CollectibleRarity.Mythic,
            SetId = "legendary_ducks",
            SetPosition = 2,
            Description = "The mighty Dragon Duck",
            ImageArt = new List<string> { "  🐉     ", " (_ ^ _) ", "  ~~~~   " },
            FlavorText = "Breathes fire and wisdom",
            SpecialEffect = "Doubles XP for one hour"
        }
    };

    // Rarity drop weights
    private static readonly Dictionary<CollectibleRarity, double> _rarityWeights = new()
    {
        [CollectibleRarity.Common] = 45,
        [CollectibleRarity.Uncommon] = 30,
        [CollectibleRarity.Rare] = 15,
        [CollectibleRarity.Epic] = 7,
        [CollectibleRarity.Legendary] = 2.5,
        [CollectibleRarity.Mythic] = 0.5
    };

    // Instance state
    public Dictionary<string, OwnedCollectible> Owned { get; private set; } = new();
    public List<string> CompletedSets { get; private set; } = new();
    public int TotalCollected { get; private set; } = 0;
    public int ShinyCount { get; private set; } = 0;
    public string? FavoriteCollectible { get; private set; } = null;
    public int PacksOpened { get; private set; } = 0;
    public List<Dictionary<string, object>> TradeHistory { get; private set; } = new();

    public CollectiblesSystem()
    {
    }

    /// <summary>
    /// Open a collectible pack
    /// </summary>
    public (bool success, string message, List<Collectible> results) OpenPack(string packType = "standard")
    {
        var packSizes = new Dictionary<string, int>
        {
            ["standard"] = 3,
            ["premium"] = 5,
            ["mega"] = 8
        };

        int count = packSizes.GetValueOrDefault(packType, 3);
        var results = new List<Collectible>();

        for (int i = 0; i < count; i++)
        {
            // Weighted random rarity
            double roll = _random.NextDouble() * 100;
            double cumulative = 0;
            CollectibleRarity selectedRarity = CollectibleRarity.Common;

            foreach (var kvp in _rarityWeights)
            {
                cumulative += kvp.Value;
                if (roll <= cumulative)
                {
                    selectedRarity = kvp.Key;
                    break;
                }
            }

            // Find collectibles of that rarity
            var matching = _collectibles.Values.Where(c => c.Rarity == selectedRarity).ToList();
            if (!matching.Any())
            {
                matching = _collectibles.Values.ToList();
            }

            var collectible = matching[_random.Next(matching.Count)];
            results.Add(collectible);
            AddCollectible(collectible);
        }

        PacksOpened++;

        string names = string.Join(", ", results.Select(c => c.Name));
        return (true, $"🎴 Pack opened! Got: {names}", results);
    }

    /// <summary>
    /// Add a collectible to the collection
    /// </summary>
    private void AddCollectible(Collectible collectible)
    {
        // 5% chance of shiny
        bool isShiny = _random.NextDouble() < 0.05;

        if (Owned.ContainsKey(collectible.Id))
        {
            Owned[collectible.Id].DuplicateCount++;
        }
        else
        {
            Owned[collectible.Id] = new OwnedCollectible
            {
                CollectibleId = collectible.Id,
                ObtainedAt = DateTime.Now,
                ObtainedFrom = "pack",
                IsShiny = isShiny
            };
            TotalCollected++;

            if (isShiny)
            {
                ShinyCount++;
            }
        }

        // Check for set completion
        CheckSetCompletion(collectible.SetId);
    }

    /// <summary>
    /// Check if a set is complete
    /// </summary>
    private bool CheckSetCompletion(string setId)
    {
        if (CompletedSets.Contains(setId))
        {
            return true;
        }

        if (!_sets.TryGetValue(setId, out var setDef))
        {
            return false;
        }

        // Count owned from this set
        int ownedInSet = Owned.Keys
            .Count(cid => _collectibles.TryGetValue(cid, out var c) && c.SetId == setId);

        if (ownedInSet >= setDef.TotalItems)
        {
            CompletedSets.Add(setId);
            return true;
        }

        return false;
    }

    /// <summary>
    /// Get progress on a specific set
    /// </summary>
    public (int owned, int total, List<string> ownedIds) GetSetProgress(string setId)
    {
        if (!_sets.TryGetValue(setId, out var setDef))
        {
            return (0, 0, new List<string>());
        }

        var ownedIds = Owned.Keys
            .Where(cid => _collectibles.TryGetValue(cid, out var c) && c.SetId == setId)
            .ToList();

        return (ownedIds.Count, setDef.TotalItems, ownedIds);
    }

    /// <summary>
    /// Get overall collection statistics
    /// </summary>
    public Dictionary<string, object> GetCollectionStats()
    {
        int totalPossible = _collectibles.Count;
        int uniqueOwned = Owned.Count;
        int duplicates = Owned.Values.Sum(c => c.DuplicateCount);

        var byRarity = new Dictionary<string, int>();
        foreach (var cid in Owned.Keys)
        {
            if (_collectibles.TryGetValue(cid, out var collectible))
            {
                string rarity = collectible.Rarity.ToString().ToLower();
                byRarity[rarity] = byRarity.GetValueOrDefault(rarity, 0) + 1;
            }
        }

        return new Dictionary<string, object>
        {
            ["unique_owned"] = uniqueOwned,
            ["total_possible"] = totalPossible,
            ["completion_percent"] = totalPossible > 0 ? Math.Round(uniqueOwned / (double)totalPossible * 100, 1) : 0,
            ["duplicates"] = duplicates,
            ["shiny_count"] = ShinyCount,
            ["sets_completed"] = CompletedSets.Count,
            ["total_sets"] = _sets.Count,
            ["by_rarity"] = byRarity
        };
    }

    /// <summary>
    /// Trade duplicate collectibles for a random new one
    /// </summary>
    public (bool success, string message, Collectible? result) TradeDuplicates(List<string> collectibleIds)
    {
        if (collectibleIds.Count < 3)
        {
            return (false, "Need at least 3 duplicates to trade!", null);
        }

        // Verify all are duplicates
        foreach (var cid in collectibleIds)
        {
            if (!Owned.TryGetValue(cid, out var owned) || owned.DuplicateCount < 1)
            {
                return (false, $"Not enough duplicates of {cid}!", null);
            }
        }

        // Remove duplicates
        foreach (var cid in collectibleIds)
        {
            Owned[cid].DuplicateCount--;
        }

        // Calculate trade value for rarity
        double avgRarityValue = 0;
        foreach (var cid in collectibleIds)
        {
            if (_collectibles.TryGetValue(cid, out var collectible))
            {
                int rarityValue = collectible.Rarity switch
                {
                    CollectibleRarity.Common => 1,
                    CollectibleRarity.Uncommon => 2,
                    CollectibleRarity.Rare => 4,
                    CollectibleRarity.Epic => 8,
                    CollectibleRarity.Legendary => 16,
                    CollectibleRarity.Mythic => 32,
                    _ => 1
                };
                avgRarityValue += rarityValue;
            }
        }
        avgRarityValue /= collectibleIds.Count;

        // Better chance of higher rarity based on trade value
        CollectibleRarity targetRarity = CollectibleRarity.Common;
        if (avgRarityValue >= 8) targetRarity = CollectibleRarity.Epic;
        else if (avgRarityValue >= 4) targetRarity = CollectibleRarity.Rare;
        else if (avgRarityValue >= 2) targetRarity = CollectibleRarity.Uncommon;

        // Get collectible of appropriate rarity
        var candidates = _collectibles.Values.Where(c => c.Rarity == targetRarity).ToList();
        if (!candidates.Any())
        {
            candidates = _collectibles.Values.ToList();
        }

        var newCollectible = candidates[_random.Next(candidates.Count)];
        AddCollectible(newCollectible);

        // Record trade
        TradeHistory.Add(new Dictionary<string, object>
        {
            ["traded"] = collectibleIds,
            ["received"] = newCollectible.Id,
            ["timestamp"] = DateTime.Now.ToString("o")
        });

        // Keep history manageable
        if (TradeHistory.Count > 100)
        {
            TradeHistory = TradeHistory.TakeLast(100).ToList();
        }

        return (true, $"🔄 Trade successful! Got: {newCollectible.Name}!", newCollectible);
    }

    /// <summary>
    /// Get a collectible by ID
    /// </summary>
    public static Collectible? GetCollectible(string collectibleId)
    {
        return _collectibles.GetValueOrDefault(collectibleId);
    }

    /// <summary>
    /// Get all sets
    /// </summary>
    public static IReadOnlyDictionary<string, CollectibleSet> GetAllSets() => _sets;

    /// <summary>
    /// Render the collection album view
    /// </summary>
    public List<string> RenderCollectionAlbum()
    {
        var stats = GetCollectionStats();

        var lines = new List<string>
        {
            "╔═══════════════════════════════════════════════╗",
            "║           🎴 COLLECTION ALBUM 🎴              ║",
            "╠═══════════════════════════════════════════════╣",
            $"║  Collected: {stats["unique_owned"],3}/{stats["total_possible"],-3} ({stats["completion_percent"]:F1}%)               ║",
            $"║  Shiny: {stats["shiny_count"],3}  |  Sets: {stats["sets_completed"]}/{stats["total_sets"]}                ║",
            "╠═══════════════════════════════════════════════╣",
            "║  SETS:                                        ║"
        };

        foreach (var kvp in _sets.Take(5))
        {
            var (owned, total, _) = GetSetProgress(kvp.Key);
            string completed = CompletedSets.Contains(kvp.Key) ? "✓" : " ";
            string progress = $"{owned}/{total}";
            string name = kvp.Value.Name.Length > 25 ? kvp.Value.Name[..25] : kvp.Value.Name;
            lines.Add($"║  [{completed}] {name,-25} {progress,5}   ║");
        }

        lines.Add("╠═══════════════════════════════════════════════╣");
        lines.Add("║  RARITY:                                      ║");

        var byRarity = stats["by_rarity"] as Dictionary<string, int> ?? new();
        foreach (CollectibleRarity rarity in Enum.GetValues<CollectibleRarity>())
        {
            int count = byRarity.GetValueOrDefault(rarity.ToString().ToLower(), 0);
            string icon = rarity switch
            {
                CollectibleRarity.Common => "⚪",
                CollectibleRarity.Uncommon => "🟢",
                CollectibleRarity.Rare => "🔵",
                CollectibleRarity.Epic => "🟣",
                CollectibleRarity.Legendary => "🟡",
                CollectibleRarity.Mythic => "🔴",
                _ => "⚪"
            };
            string name = rarity.ToString();
            lines.Add($"║    {icon} {name,-12}: {count,3}                    ║");
        }

        lines.Add("╚═══════════════════════════════════════════════╝");

        return lines;
    }

    /// <summary>
    /// Render a single collectible card
    /// </summary>
    public List<string> RenderCollectibleCard(string collectibleId)
    {
        if (!_collectibles.TryGetValue(collectibleId, out var collectible))
        {
            return new List<string> { "Collectible not found!" };
        }

        Owned.TryGetValue(collectibleId, out var owned);

        string rarityIcon = collectible.Rarity switch
        {
            CollectibleRarity.Common => "⚪",
            CollectibleRarity.Uncommon => "🟢",
            CollectibleRarity.Rare => "🔵",
            CollectibleRarity.Epic => "🟣",
            CollectibleRarity.Legendary => "🟡",
            CollectibleRarity.Mythic => "🔴",
            _ => "⚪"
        };

        string shiny = owned?.IsShiny == true ? "✨" : "";

        var lines = new List<string>
        {
            "╔════════════════════════════════════╗",
            $"║ {shiny}{collectible.Name.PadLeft(16).PadRight(32)}{shiny} ║",
            $"║  {rarityIcon} {collectible.Rarity.ToString().PadLeft(14).PadRight(29)}  ║",
            "╠════════════════════════════════════╣"
        };

        foreach (var artLine in collectible.ImageArt)
        {
            string centered = artLine.PadLeft((32 + artLine.Length) / 2).PadRight(32);
            lines.Add($"║  {centered}  ║");
        }

        lines.Add("╠════════════════════════════════════╣");

        string desc = collectible.Description;
        while (desc.Length > 0)
        {
            string chunk = desc.Length > 32 ? desc[..32] : desc;
            lines.Add($"║  {chunk,-32}  ║");
            desc = desc.Length > 32 ? desc[32..] : "";
        }

        if (!string.IsNullOrEmpty(collectible.FlavorText))
        {
            string flavor = collectible.FlavorText.Length > 28 ? collectible.FlavorText[..28] : collectible.FlavorText;
            lines.Add($"║  \"{flavor,-28}\"  ║");
        }

        if (owned != null)
        {
            string dupe = owned.DuplicateCount > 0 ? $"+{owned.DuplicateCount}" : "";
            lines.Add($"║  Owned {dupe.PadLeft(13).PadRight(27)}  ║");
        }
        else
        {
            lines.Add("║  ??? Not Owned ???                 ║");
        }

        lines.Add("╚════════════════════════════════════╝");

        return lines;
    }

    /// <summary>
    /// Convert to save data
    /// </summary>
    public Dictionary<string, object> ToSaveData()
    {
        var ownedData = new Dictionary<string, object>();
        foreach (var kvp in Owned)
        {
            ownedData[kvp.Key] = new Dictionary<string, object>
            {
                ["collectible_id"] = kvp.Value.CollectibleId,
                ["obtained_at"] = kvp.Value.ObtainedAt.ToString("o"),
                ["obtained_from"] = kvp.Value.ObtainedFrom,
                ["is_shiny"] = kvp.Value.IsShiny,
                ["duplicate_count"] = kvp.Value.DuplicateCount
            };
        }

        return new Dictionary<string, object>
        {
            ["owned"] = ownedData,
            ["completed_sets"] = CompletedSets,
            ["total_collected"] = TotalCollected,
            ["shiny_count"] = ShinyCount,
            ["favorite_collectible"] = FavoriteCollectible ?? "",
            ["packs_opened"] = PacksOpened,
            ["trade_history"] = TradeHistory
        };
    }

    /// <summary>
    /// Load from save data
    /// </summary>
    public static CollectiblesSystem FromSaveData(Dictionary<string, object> data)
    {
        var system = new CollectiblesSystem();

        if (data.TryGetValue("owned", out var ownedObj) && ownedObj is JsonElement ownedElement)
        {
            foreach (var prop in ownedElement.EnumerateObject())
            {
                system.Owned[prop.Name] = new OwnedCollectible
                {
                    CollectibleId = prop.Value.GetProperty("collectible_id").GetString() ?? "",
                    ObtainedAt = DateTime.Parse(prop.Value.GetProperty("obtained_at").GetString() ?? DateTime.Now.ToString()),
                    ObtainedFrom = prop.Value.TryGetProperty("obtained_from", out var of) ? of.GetString() ?? "" : "",
                    IsShiny = prop.Value.TryGetProperty("is_shiny", out var sh) && sh.GetBoolean(),
                    DuplicateCount = prop.Value.TryGetProperty("duplicate_count", out var dc) ? dc.GetInt32() : 0
                };
            }
        }

        if (data.TryGetValue("completed_sets", out var setsObj) && setsObj is JsonElement setsElement)
        {
            foreach (var item in setsElement.EnumerateArray())
            {
                system.CompletedSets.Add(item.GetString() ?? "");
            }
        }

        system.TotalCollected = Convert.ToInt32(data.GetValueOrDefault("total_collected", 0));
        system.ShinyCount = Convert.ToInt32(data.GetValueOrDefault("shiny_count", 0));
        system.FavoriteCollectible = data.GetValueOrDefault("favorite_collectible")?.ToString();
        system.PacksOpened = Convert.ToInt32(data.GetValueOrDefault("packs_opened", 0));

        return system;
    }
}
