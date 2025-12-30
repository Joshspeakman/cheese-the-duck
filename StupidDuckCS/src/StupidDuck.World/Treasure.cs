using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;

namespace StupidDuck.World;

/// <summary>
/// Rarity of treasures
/// </summary>
public enum TreasureRarity
{
    Common,
    Uncommon,
    Rare,
    Epic,
    Legendary,
    Mythical
}

/// <summary>
/// Types of treasure locations
/// </summary>
public enum TreasureLocation
{
    Beach,
    Forest,
    Garden,
    Pond,
    Cave,
    Mountain,
    Secret
}

/// <summary>
/// A treasure that can be found
/// </summary>
public class Treasure
{
    public string Id { get; set; } = "";
    public string Name { get; set; } = "";
    public string Description { get; set; } = "";
    public TreasureRarity Rarity { get; set; }
    public List<TreasureLocation> Locations { get; set; } = new();
    public int XpValue { get; set; } = 0;
    public int CoinValue { get; set; } = 0;
    public string AsciiArt { get; set; } = "";
    public string Lore { get; set; } = "";
    public bool IsCollectible { get; set; } = true;
}

/// <summary>
/// A map that reveals treasure location
/// </summary>
public class TreasureMap
{
    public string MapId { get; set; } = "";
    public string TreasureId { get; set; } = "";
    public TreasureLocation Location { get; set; }
    public string Hint { get; set; } = "";
    public bool Found { get; set; } = false;
    public DateTime CreatedAt { get; set; } = DateTime.Now;
}

/// <summary>
/// A treasure that was found
/// </summary>
public class FoundTreasure
{
    public string TreasureId { get; set; } = "";
    public DateTime FoundAt { get; set; } = DateTime.Now;
    public TreasureLocation Location { get; set; }
    public bool WasMapped { get; set; } = false;
}

/// <summary>
/// Treasure hunting system - hunt for treasures in various locations
/// </summary>
public class TreasureHunter
{
    private static readonly Random _random = new();

    // All treasures
    private static readonly Dictionary<string, Treasure> _treasures = new()
    {
        // Common treasures
        ["old_coin"] = new Treasure
        {
            Id = "old_coin",
            Name = "Old Coin",
            Description = "A worn, old coin. Someone lost this long ago.",
            Rarity = TreasureRarity.Common,
            Locations = new List<TreasureLocation> { TreasureLocation.Beach, TreasureLocation.Garden },
            XpValue = 10, CoinValue = 5,
            AsciiArt = "[◎]",
            Lore = "This coin bears the image of a duck king from centuries past."
        },
        ["pretty_shell"] = new Treasure
        {
            Id = "pretty_shell",
            Name = "Pretty Shell",
            Description = "A beautiful seashell with a pearly interior.",
            Rarity = TreasureRarity.Common,
            Locations = new List<TreasureLocation> { TreasureLocation.Beach, TreasureLocation.Pond },
            XpValue = 8, CoinValue = 3,
            AsciiArt = "🐚",
            Lore = "Hold it to your ear - you can hear the ocean!"
        },
        ["smooth_stone"] = new Treasure
        {
            Id = "smooth_stone",
            Name = "Smooth Stone",
            Description = "A perfectly smooth, palm-sized stone.",
            Rarity = TreasureRarity.Common,
            Locations = new List<TreasureLocation> { TreasureLocation.Forest, TreasureLocation.Pond },
            XpValue = 5, CoinValue = 2,
            AsciiArt = "◐",
            Lore = "Polished by centuries of flowing water."
        },
        // Uncommon treasures
        ["ancient_feather"] = new Treasure
        {
            Id = "ancient_feather",
            Name = "Ancient Feather",
            Description = "A preserved feather from an ancient duck.",
            Rarity = TreasureRarity.Uncommon,
            Locations = new List<TreasureLocation> { TreasureLocation.Cave, TreasureLocation.Forest },
            XpValue = 25, CoinValue = 20,
            AsciiArt = "🪶",
            Lore = "Legend says this belonged to the First Duck."
        },
        ["glass_bottle"] = new Treasure
        {
            Id = "glass_bottle",
            Name = "Message in a Bottle",
            Description = "An old bottle with a mysterious message inside!",
            Rarity = TreasureRarity.Uncommon,
            Locations = new List<TreasureLocation> { TreasureLocation.Beach, TreasureLocation.Pond },
            XpValue = 30, CoinValue = 25,
            AsciiArt = "🍾",
            Lore = "The message reads: 'Bread is the answer to everything.'"
        },
        ["fossil"] = new Treasure
        {
            Id = "fossil",
            Name = "Duck Fossil",
            Description = "A fossilized duck footprint from prehistoric times!",
            Rarity = TreasureRarity.Uncommon,
            Locations = new List<TreasureLocation> { TreasureLocation.Mountain, TreasureLocation.Cave },
            XpValue = 35, CoinValue = 30,
            AsciiArt = "🦶",
            Lore = "Evidence that ducks have been awesome for millions of years."
        },
        // Rare treasures
        ["ruby_gem"] = new Treasure
        {
            Id = "ruby_gem",
            Name = "Ruby Gem",
            Description = "A beautiful red gemstone that catches the light!",
            Rarity = TreasureRarity.Rare,
            Locations = new List<TreasureLocation> { TreasureLocation.Cave, TreasureLocation.Mountain },
            XpValue = 75, CoinValue = 100,
            AsciiArt = "💎",
            Lore = "Some say this gem was formed from crystallized duck joy."
        },
        ["golden_acorn"] = new Treasure
        {
            Id = "golden_acorn",
            Name = "Golden Acorn",
            Description = "A perfectly preserved golden acorn!",
            Rarity = TreasureRarity.Rare,
            Locations = new List<TreasureLocation> { TreasureLocation.Forest },
            XpValue = 60, CoinValue = 75,
            AsciiArt = "🌰",
            Lore = "Grown from the legendary Golden Oak Tree."
        },
        ["pirate_compass"] = new Treasure
        {
            Id = "pirate_compass",
            Name = "Pirate Compass",
            Description = "An old compass that always points to treasure!",
            Rarity = TreasureRarity.Rare,
            Locations = new List<TreasureLocation> { TreasureLocation.Beach, TreasureLocation.Cave },
            XpValue = 80, CoinValue = 90,
            AsciiArt = "🧭",
            Lore = "Once belonged to Captain Quackbeard himself."
        },
        // Epic treasures
        ["ancient_crown"] = new Treasure
        {
            Id = "ancient_crown",
            Name = "Ancient Duck Crown",
            Description = "A crown worn by duck royalty of old!",
            Rarity = TreasureRarity.Epic,
            Locations = new List<TreasureLocation> { TreasureLocation.Cave, TreasureLocation.Secret },
            XpValue = 200, CoinValue = 300,
            AsciiArt = "👑",
            Lore = "This crown has been passed down through 100 duck generations."
        },
        ["mystic_egg"] = new Treasure
        {
            Id = "mystic_egg",
            Name = "Mystic Egg",
            Description = "A mysterious glowing egg with ancient symbols.",
            Rarity = TreasureRarity.Epic,
            Locations = new List<TreasureLocation> { TreasureLocation.Secret, TreasureLocation.Mountain },
            XpValue = 250, CoinValue = 350,
            AsciiArt = "🥚✨",
            Lore = "What could hatch from this egg? Nobody knows..."
        },
        // Legendary treasures
        ["star_fragment"] = new Treasure
        {
            Id = "star_fragment",
            Name = "Star Fragment",
            Description = "A piece of a fallen star! Incredibly rare!",
            Rarity = TreasureRarity.Legendary,
            Locations = new List<TreasureLocation> { TreasureLocation.Secret, TreasureLocation.Mountain },
            XpValue = 500, CoinValue = 750,
            AsciiArt = "⭐",
            Lore = "Whispered wishes to this fragment are said to come true."
        },
        ["ancient_tome"] = new Treasure
        {
            Id = "ancient_tome",
            Name = "Ancient Tome of Quacks",
            Description = "An ancient book of duck wisdom!",
            Rarity = TreasureRarity.Legendary,
            Locations = new List<TreasureLocation> { TreasureLocation.Cave, TreasureLocation.Secret },
            XpValue = 600, CoinValue = 800,
            AsciiArt = "📖",
            Lore = "Contains the sacred knowledge of the Duck Elders."
        },
        // Mythical
        ["heart_of_pond"] = new Treasure
        {
            Id = "heart_of_pond",
            Name = "Heart of the Pond",
            Description = "THE legendary treasure. The soul of all ponds!",
            Rarity = TreasureRarity.Mythical,
            Locations = new List<TreasureLocation> { TreasureLocation.Secret },
            XpValue = 2000, CoinValue = 2500,
            AsciiArt = "💙✨",
            Lore = "Only the most dedicated treasure hunter will ever find this."
        }
    };

    // Location hints
    private static readonly Dictionary<TreasureLocation, List<string>> _locationHints = new()
    {
        [TreasureLocation.Beach] = new List<string>
        {
            "Where the waves kiss the sand...",
            "Near the driftwood at low tide...",
            "Beneath the seagull's watchful gaze..."
        },
        [TreasureLocation.Forest] = new List<string>
        {
            "Under the ancient oak...",
            "Where sunlight filters through leaves...",
            "Near the mushroom circle..."
        },
        [TreasureLocation.Garden] = new List<string>
        {
            "Beside the old sundial...",
            "Where the roses bloom...",
            "Under the bird bath..."
        },
        [TreasureLocation.Pond] = new List<string>
        {
            "At the water's edge...",
            "Near the lily pads...",
            "Where the ducks gather..."
        },
        [TreasureLocation.Cave] = new List<string>
        {
            "In the deepest shadows...",
            "Behind the crystal formations...",
            "Where echoes fade to silence..."
        },
        [TreasureLocation.Mountain] = new List<string>
        {
            "At the summit's peak...",
            "Near the ancient stones...",
            "Where eagles dare not go..."
        },
        [TreasureLocation.Secret] = new List<string>
        {
            "Where dreams meet reality...",
            "In the place between places...",
            "Follow the golden light..."
        }
    };

    // Instance state
    public Dictionary<string, List<FoundTreasure>> FoundTreasures { get; private set; } = new();
    public List<TreasureMap> TreasureMaps { get; private set; } = new();
    public int TotalTreasuresFound { get; private set; } = 0;
    public int TotalValueFound { get; private set; } = 0;
    public List<TreasureLocation> UnlockedLocations { get; private set; } = new()
    {
        TreasureLocation.Beach,
        TreasureLocation.Garden
    };
    public int DigAttemptsToday { get; private set; } = 0;
    public int MaxDigsPerDay { get; } = 10;
    public string LastDigDate { get; private set; } = "";
    public TreasureLocation? CurrentHuntLocation { get; private set; } = null;
    public int HuntProgress { get; private set; } = 0;
    public TreasureMap? ActiveMap { get; private set; } = null;

    public TreasureHunter()
    {
    }

    /// <summary>
    /// Start hunting at a location
    /// </summary>
    public (bool success, string message) StartHunt(TreasureLocation location)
    {
        if (!UnlockedLocations.Contains(location))
        {
            return (false, $"You haven't unlocked {location} yet!");
        }

        // Check daily dig limit
        string today = DateTime.Now.ToString("yyyy-MM-dd");
        if (LastDigDate != today)
        {
            DigAttemptsToday = 0;
            LastDigDate = today;
        }

        if (DigAttemptsToday >= MaxDigsPerDay)
        {
            return (false, "You're tired from digging! Try again tomorrow.");
        }

        CurrentHuntLocation = location;
        HuntProgress = 0;
        return (true, $"Started searching at {location}... 🔍");
    }

    /// <summary>
    /// Attempt to dig for treasure
    /// </summary>
    public (bool found, string message, FoundTreasure? treasure) Dig()
    {
        if (CurrentHuntLocation == null)
        {
            return (false, "Start a treasure hunt first!", null);
        }

        DigAttemptsToday++;
        HuntProgress += _random.Next(15, 36);

        // Check if using a map
        if (ActiveMap != null)
        {
            if (HuntProgress >= 50)
            {
                // Guaranteed find with map
                return FindTreasure(ActiveMap.TreasureId, wasMapped: true);
            }
        }

        // Random find chance
        double findChance = 0.1 + (HuntProgress / 500.0);

        if (_random.NextDouble() < findChance)
        {
            var treasure = SelectTreasure();
            if (treasure != null)
            {
                return FindTreasure(treasure.Id);
            }
        }

        // Progression messages
        if (HuntProgress >= 100)
        {
            HuntProgress = 0;
            return (false, "Nothing here... Try a different spot? 🤔", null);
        }

        string[] messages =
        {
            "Digging... Nothing yet. 🕳️",
            "Keep searching... 🔍",
            "You found a rock! ...Just a rock. 🪨",
            "Something rustles nearby... 🌿",
            "The duck instincts say you're getting closer! 🦆"
        };
        return (false, messages[_random.Next(messages.Length)], null);
    }

    /// <summary>
    /// Select a random treasure based on location and rarity
    /// </summary>
    private Treasure? SelectTreasure()
    {
        if (CurrentHuntLocation == null)
        {
            return null;
        }

        var available = _treasures.Values
            .Where(t => t.Locations.Contains(CurrentHuntLocation.Value))
            .ToList();

        if (!available.Any())
        {
            return null;
        }

        // Weight by rarity
        var weights = new Dictionary<TreasureRarity, int>
        {
            [TreasureRarity.Common] = 500,
            [TreasureRarity.Uncommon] = 250,
            [TreasureRarity.Rare] = 100,
            [TreasureRarity.Epic] = 40,
            [TreasureRarity.Legendary] = 10,
            [TreasureRarity.Mythical] = 1
        };

        var weighted = new List<Treasure>();
        foreach (var t in available)
        {
            int weight = weights.GetValueOrDefault(t.Rarity, 10);
            for (int i = 0; i < weight; i++)
            {
                weighted.Add(t);
            }
        }

        if (weighted.Any())
        {
            return weighted[_random.Next(weighted.Count)];
        }
        return available[_random.Next(available.Count)];
    }

    /// <summary>
    /// Record finding a treasure
    /// </summary>
    private (bool found, string message, FoundTreasure? treasure) FindTreasure(string treasureId, bool wasMapped = false)
    {
        if (!_treasures.TryGetValue(treasureId, out var treasure))
        {
            return (false, "Error: Unknown treasure!", null);
        }

        var found = new FoundTreasure
        {
            TreasureId = treasureId,
            FoundAt = DateTime.Now,
            Location = CurrentHuntLocation!.Value,
            WasMapped = wasMapped
        };

        if (!FoundTreasures.ContainsKey(treasureId))
        {
            FoundTreasures[treasureId] = new List<FoundTreasure>();
        }
        FoundTreasures[treasureId].Add(found);

        TotalTreasuresFound++;
        TotalValueFound += treasure.CoinValue;

        // Clear map if used
        if (wasMapped && ActiveMap != null)
        {
            ActiveMap.Found = true;
            ActiveMap = null;
        }

        // Reset hunt
        CurrentHuntLocation = null;
        HuntProgress = 0;

        var rarityEmoji = treasure.Rarity switch
        {
            TreasureRarity.Common => "✓",
            TreasureRarity.Uncommon => "✦",
            TreasureRarity.Rare => "★",
            TreasureRarity.Epic => "✮",
            TreasureRarity.Legendary => "⭐",
            TreasureRarity.Mythical => "🌟",
            _ => "✓"
        };

        bool firstFind = FoundTreasures[treasureId].Count == 1;
        string newBadge = firstFind ? " 🆕 First Find!" : "";

        return (true, $"{rarityEmoji} TREASURE FOUND! {rarityEmoji}\n{treasure.Name} {treasure.AsciiArt}{newBadge}", found);
    }

    /// <summary>
    /// Use a treasure map
    /// </summary>
    public (bool success, string message) UseMap(string mapId)
    {
        var map = TreasureMaps.FirstOrDefault(m => m.MapId == mapId && !m.Found);
        if (map == null)
        {
            return (false, "Map not found or already used!");
        }

        if (!UnlockedLocations.Contains(map.Location))
        {
            return (false, $"You need to unlock {map.Location} first!");
        }

        ActiveMap = map;
        CurrentHuntLocation = map.Location;
        HuntProgress = 0;

        return (true, $"Following the map... Hint: {map.Hint}");
    }

    /// <summary>
    /// Add a new treasure map
    /// </summary>
    public TreasureMap AddMap(string? treasureId = null)
    {
        var treasure = treasureId != null && _treasures.TryGetValue(treasureId, out var t)
            ? t
            : _treasures.Values.ElementAt(_random.Next(_treasures.Count));

        var location = treasure.Locations[_random.Next(treasure.Locations.Count)];
        var hints = _locationHints.GetValueOrDefault(location, new List<string> { "Look carefully..." });

        var newMap = new TreasureMap
        {
            MapId = $"map_{TreasureMaps.Count + 1}",
            TreasureId = treasure.Id,
            Location = location,
            Hint = hints[_random.Next(hints.Count)],
            CreatedAt = DateTime.Now
        };

        TreasureMaps.Add(newMap);
        return newMap;
    }

    /// <summary>
    /// Unlock a new location
    /// </summary>
    public (bool success, string message) UnlockLocation(TreasureLocation location)
    {
        if (UnlockedLocations.Contains(location))
        {
            return (false, "Location already unlocked!");
        }

        UnlockedLocations.Add(location);
        return (true, $"Unlocked {location} for treasure hunting! 🗺️");
    }

    /// <summary>
    /// Get collection statistics
    /// </summary>
    public Dictionary<string, object> GetCollectionStats()
    {
        int total = _treasures.Count;
        int found = FoundTreasures.Count;

        var byRarity = new Dictionary<string, int>();
        foreach (var tid in FoundTreasures.Keys)
        {
            if (_treasures.TryGetValue(tid, out var treasure))
            {
                string rarity = treasure.Rarity.ToString().ToLower();
                byRarity[rarity] = byRarity.GetValueOrDefault(rarity, 0) + 1;
            }
        }

        return new Dictionary<string, object>
        {
            ["total_types"] = total,
            ["found_types"] = found,
            ["completion"] = Math.Round(found / (double)total * 100, 1),
            ["total_found"] = TotalTreasuresFound,
            ["total_value"] = TotalValueFound,
            ["by_rarity"] = byRarity,
            ["unlocked_locations"] = UnlockedLocations.Count,
            ["maps_available"] = TreasureMaps.Count(m => !m.Found)
        };
    }

    /// <summary>
    /// Get a treasure by ID
    /// </summary>
    public static Treasure? GetTreasure(string treasureId)
    {
        return _treasures.GetValueOrDefault(treasureId);
    }

    /// <summary>
    /// Get all treasures
    /// </summary>
    public static IReadOnlyDictionary<string, Treasure> GetAllTreasures() => _treasures;

    /// <summary>
    /// Render treasure collection
    /// </summary>
    public List<string> RenderCollection()
    {
        var stats = GetCollectionStats();

        var lines = new List<string>
        {
            "╔════════════════════════════════════════╗",
            "║       💎 TREASURE COLLECTION 💎        ║",
            $"║ Found: {stats["found_types"]}/{stats["total_types"]} ({stats["completion"]}%)            ║",
            $"║ Total Value: {stats["total_value"]:N0} coins            ║",
            "╠════════════════════════════════════════╣"
        };

        foreach (var kvp in _treasures)
        {
            if (FoundTreasures.ContainsKey(kvp.Key))
            {
                int count = FoundTreasures[kvp.Key].Count;
                lines.Add($"║ {kvp.Value.AsciiArt} {kvp.Value.Name,-20} x{count} ║");
            }
            else
            {
                lines.Add($"║ ??? {"Unknown Treasure",-20}    ║");
            }
        }

        lines.Add("╚════════════════════════════════════════╝");
        return lines;
    }

    /// <summary>
    /// Convert to save data
    /// </summary>
    public Dictionary<string, object> ToSaveData()
    {
        var foundData = new Dictionary<string, object>();
        foreach (var kvp in FoundTreasures)
        {
            foundData[kvp.Key] = kvp.Value.Select(f => new Dictionary<string, object>
            {
                ["treasure_id"] = f.TreasureId,
                ["found_at"] = f.FoundAt.ToString("o"),
                ["location"] = f.Location.ToString().ToLower(),
                ["was_mapped"] = f.WasMapped
            }).ToList();
        }

        return new Dictionary<string, object>
        {
            ["found_treasures"] = foundData,
            ["treasure_maps"] = TreasureMaps.Select(m => new Dictionary<string, object>
            {
                ["map_id"] = m.MapId,
                ["treasure_id"] = m.TreasureId,
                ["location"] = m.Location.ToString().ToLower(),
                ["hint"] = m.Hint,
                ["found"] = m.Found,
                ["created_at"] = m.CreatedAt.ToString("o")
            }).ToList(),
            ["total_treasures_found"] = TotalTreasuresFound,
            ["total_value_found"] = TotalValueFound,
            ["unlocked_locations"] = UnlockedLocations.Select(l => l.ToString().ToLower()).ToList(),
            ["dig_attempts_today"] = DigAttemptsToday,
            ["last_dig_date"] = LastDigDate
        };
    }

    /// <summary>
    /// Load from save data
    /// </summary>
    public static TreasureHunter FromSaveData(Dictionary<string, object> data)
    {
        var hunter = new TreasureHunter();

        if (data.TryGetValue("found_treasures", out var foundObj) && foundObj is JsonElement foundElement)
        {
            foreach (var prop in foundElement.EnumerateObject())
            {
                var list = new List<FoundTreasure>();
                foreach (var item in prop.Value.EnumerateArray())
                {
                    list.Add(new FoundTreasure
                    {
                        TreasureId = item.GetProperty("treasure_id").GetString() ?? "",
                        FoundAt = DateTime.Parse(item.GetProperty("found_at").GetString() ?? DateTime.Now.ToString()),
                        Location = Enum.TryParse<TreasureLocation>(item.GetProperty("location").GetString(), true, out var loc) ? loc : TreasureLocation.Beach,
                        WasMapped = item.GetProperty("was_mapped").GetBoolean()
                    });
                }
                hunter.FoundTreasures[prop.Name] = list;
            }
        }

        if (data.TryGetValue("treasure_maps", out var mapsObj) && mapsObj is JsonElement mapsElement)
        {
            foreach (var item in mapsElement.EnumerateArray())
            {
                hunter.TreasureMaps.Add(new TreasureMap
                {
                    MapId = item.GetProperty("map_id").GetString() ?? "",
                    TreasureId = item.GetProperty("treasure_id").GetString() ?? "",
                    Location = Enum.TryParse<TreasureLocation>(item.GetProperty("location").GetString(), true, out var loc) ? loc : TreasureLocation.Beach,
                    Hint = item.GetProperty("hint").GetString() ?? "",
                    Found = item.GetProperty("found").GetBoolean(),
                    CreatedAt = DateTime.TryParse(item.TryGetProperty("created_at", out var ca) ? ca.GetString() : null, out var dt) ? dt : DateTime.Now
                });
            }
        }

        hunter.TotalTreasuresFound = Convert.ToInt32(data.GetValueOrDefault("total_treasures_found", 0));
        hunter.TotalValueFound = Convert.ToInt32(data.GetValueOrDefault("total_value_found", 0));
        hunter.DigAttemptsToday = Convert.ToInt32(data.GetValueOrDefault("dig_attempts_today", 0));
        hunter.LastDigDate = data.GetValueOrDefault("last_dig_date")?.ToString() ?? "";

        if (data.TryGetValue("unlocked_locations", out var locObj) && locObj is JsonElement locElement)
        {
            hunter.UnlockedLocations.Clear();
            foreach (var item in locElement.EnumerateArray())
            {
                if (Enum.TryParse<TreasureLocation>(item.GetString(), true, out var loc))
                {
                    hunter.UnlockedLocations.Add(loc);
                }
            }
        }

        return hunter;
    }
}
