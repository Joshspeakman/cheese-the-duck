using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;

namespace StupidDuck.World;

/// <summary>
/// Types of secrets that can be discovered
/// </summary>
public enum SecretType
{
    EasterEgg,
    HiddenItem,
    SecretArea,
    SpecialEvent,
    HiddenCommand,
    SecretCombination,
    RareEncounter
}

/// <summary>
/// Rarity of secrets - how hard they are to find
/// </summary>
public enum SecretRarity
{
    Common,      // Easy to find
    Uncommon,    // Moderate effort
    Rare,        // Requires dedication
    Legendary,   // Extremely hard to find
    Mythical     // Almost impossible
}

/// <summary>
/// Definition of a discoverable secret
/// </summary>
public class Secret
{
    public string Id { get; set; } = "";
    public string Name { get; set; } = "";
    public string Description { get; set; } = "";
    public string Hint { get; set; } = "";
    public SecretType SecretType { get; set; }
    public SecretRarity Rarity { get; set; }
    public int CoinsReward { get; set; } = 0;
    public int XpReward { get; set; } = 0;
    public string SpecialReward { get; set; } = "";
    public string UnlockMessage { get; set; } = "";
    public List<string> AsciiArt { get; set; } = new();
}

/// <summary>
/// Record of a discovered secret
/// </summary>
public class DiscoveredSecret
{
    public string SecretId { get; set; } = "";
    public DateTime DiscoveredAt { get; set; } = DateTime.Now;
    public int TimesTriggered { get; set; } = 1;

    public Dictionary<string, object> ToSaveData()
    {
        return new Dictionary<string, object>
        {
            ["secret_id"] = SecretId,
            ["discovered_at"] = DiscoveredAt.ToString("o"),
            ["times_triggered"] = TimesTriggered
        };
    }

    public static DiscoveredSecret FromSaveData(Dictionary<string, object> data)
    {
        return new DiscoveredSecret
        {
            SecretId = data.GetValueOrDefault("secret_id")?.ToString() ?? "",
            DiscoveredAt = DateTime.TryParse(data.GetValueOrDefault("discovered_at")?.ToString(), out var dt) ? dt : DateTime.Now,
            TimesTriggered = Convert.ToInt32(data.GetValueOrDefault("times_triggered", 1))
        };
    }
}

/// <summary>
/// System for managing secrets and easter eggs
/// </summary>
public class SecretsSystem
{
    private static readonly Random _random = new();

    // All discoverable secrets
    private static readonly Dictionary<string, Secret> _secrets = new()
    {
        // Easter Eggs
        ["konami_code"] = new Secret
        {
            Id = "konami_code",
            Name = "Konami Code",
            Description = "The classic cheat code works here!",
            Hint = "↑↑↓↓←→←→BA",
            SecretType = SecretType.EasterEgg,
            Rarity = SecretRarity.Uncommon,
            CoinsReward = 500,
            XpReward = 100,
            UnlockMessage = "30 extra coins! Wait... lives? We don't do that here.",
            AsciiArt = new List<string>
            {
                "  ↑↑↓↓←→←→BA  ",
                "    START!     ",
                "  🎮 CLASSIC 🎮  "
            }
        },
        ["duck_song"] = new Secret
        {
            Id = "duck_song",
            Name = "The Duck Song",
            Description = "Got any grapes?",
            Hint = "Try talking about grapes...",
            SecretType = SecretType.EasterEgg,
            Rarity = SecretRarity.Common,
            CoinsReward = 100,
            XpReward = 50,
            UnlockMessage = "A duck walked up to a lemonade stand...",
            AsciiArt = new List<string>
            {
                "  🍇 🍇 🍇 🍇  ",
                " Got any grapes? ",
                "  🍋 Nope! 🍋    "
            }
        },
        ["midnight_quack"] = new Secret
        {
            Id = "midnight_quack",
            Name = "Midnight Quacker",
            Description = "Something special happens at exactly midnight...",
            Hint = "The clock strikes twelve...",
            SecretType = SecretType.SpecialEvent,
            Rarity = SecretRarity.Rare,
            CoinsReward = 250,
            XpReward = 150,
            SpecialReward = "midnight_hat",
            UnlockMessage = "🌙 The Midnight Duck rises! 🌙"
        },
        ["triple_seven"] = new Secret
        {
            Id = "triple_seven",
            Name = "Lucky 777",
            Description = "When coins align perfectly...",
            Hint = "777 is a lucky number...",
            SecretType = SecretType.SecretCombination,
            Rarity = SecretRarity.Uncommon,
            CoinsReward = 777,
            XpReward = 77,
            UnlockMessage = "JACKPOT! 🎰🎰🎰"
        },
        ["golden_duck"] = new Secret
        {
            Id = "golden_duck",
            Name = "The Golden Duck",
            Description = "A shimmering golden feather appears...",
            Hint = "Feed 1000 times for something special",
            SecretType = SecretType.RareEncounter,
            Rarity = SecretRarity.Legendary,
            CoinsReward = 5000,
            XpReward = 1000,
            SpecialReward = "golden_aura",
            UnlockMessage = "Your duck glows with golden light!",
            AsciiArt = new List<string>
            {
                "     ✨✨✨     ",
                "   ⭐🦆⭐    ",
                "     ✨✨✨     ",
                "  LEGENDARY!   "
            }
        },
        ["rubber_duck"] = new Secret
        {
            Id = "rubber_duck",
            Name = "Rubber Ducky Mode",
            Description = "Squeak squeak!",
            Hint = "Type 'squeak' three times...",
            SecretType = SecretType.HiddenCommand,
            Rarity = SecretRarity.Common,
            CoinsReward = 50,
            XpReward = 25,
            UnlockMessage = "🛁 SQUEAK! You're the one! 🛁"
        },
        ["secret_pond"] = new Secret
        {
            Id = "secret_pond",
            Name = "Hidden Lily Pond",
            Description = "A secret peaceful pond behind the waterfall...",
            Hint = "Explore when it's raining heavily",
            SecretType = SecretType.SecretArea,
            Rarity = SecretRarity.Rare,
            CoinsReward = 300,
            XpReward = 200,
            SpecialReward = "lily_pad_decoration",
            UnlockMessage = "You discovered a hidden sanctuary!"
        },
        ["dev_room"] = new Secret
        {
            Id = "dev_room",
            Name = "Developer's Room",
            Description = "Where the magic happens...",
            Hint = "404... but not really",
            SecretType = SecretType.SecretArea,
            Rarity = SecretRarity.Legendary,
            CoinsReward = 1000,
            XpReward = 500,
            UnlockMessage = "Welcome behind the scenes!",
            AsciiArt = new List<string>
            {
                "  +----------+  ",
                "  | DEV ROOM |  ",
                "  |  🖥️ 🦆   |  ",
                "  | v1.0.0   |  ",
                "  +----------+  "
            }
        },
        ["birthday_duck"] = new Secret
        {
            Id = "birthday_duck",
            Name = "Birthday Duck",
            Description = "Celebrating a special day!",
            Hint = "Play on a very special day...",
            SecretType = SecretType.SpecialEvent,
            Rarity = SecretRarity.Uncommon,
            CoinsReward = 200,
            XpReward = 100,
            SpecialReward = "birthday_hat",
            UnlockMessage = "🎂 Happy Birthday! 🎂"
        },
        ["palindrome"] = new Secret
        {
            Id = "palindrome",
            Name = "Palindrome Duck",
            Description = "Forward and backward, all the same!",
            Hint = "12:21, 23:32, 11:11...",
            SecretType = SecretType.SpecialEvent,
            Rarity = SecretRarity.Common,
            CoinsReward = 111,
            XpReward = 11,
            UnlockMessage = "Time mirrors itself! ⏰"
        },
        ["hundred_pets"] = new Secret
        {
            Id = "hundred_pets",
            Name = "Pet Master",
            Description = "100 pets in one session!",
            Hint = "Pet, pet, pet, pet, pet...",
            SecretType = SecretType.RareEncounter,
            Rarity = SecretRarity.Uncommon,
            CoinsReward = 200,
            XpReward = 100,
            UnlockMessage = "You really love petting! 🫳🦆"
        },
        ["ancient_quack"] = new Secret
        {
            Id = "ancient_quack",
            Name = "Ancient Quack",
            Description = "The primordial duck sound...",
            Hint = "Quack in ancient language",
            SecretType = SecretType.HiddenCommand,
            Rarity = SecretRarity.Rare,
            CoinsReward = 500,
            XpReward = 250,
            UnlockMessage = "QUACKUS MAXIMUS!",
            AsciiArt = new List<string>
            {
                "   📜📜📜📜   ",
                "  QUACKUS    ",
                "   MAXIMUS   ",
                "   📜📜📜📜   "
            }
        },
        ["night_owl_duck"] = new Secret
        {
            Id = "night_owl_duck",
            Name = "Night Owl",
            Description = "Playing in the wee hours...",
            Hint = "3 AM club member",
            SecretType = SecretType.SpecialEvent,
            Rarity = SecretRarity.Uncommon,
            CoinsReward = 150,
            XpReward = 75,
            UnlockMessage = "🦉 Why are you awake? 🦆"
        },
        ["rainbow_duck"] = new Secret
        {
            Id = "rainbow_duck",
            Name = "Rainbow Connection",
            Description = "All colors of the rainbow!",
            Hint = "Have 7 different colored items equipped",
            SecretType = SecretType.SecretCombination,
            Rarity = SecretRarity.Rare,
            CoinsReward = 700,
            XpReward = 350,
            SpecialReward = "rainbow_trail",
            UnlockMessage = "🌈 Somewhere over the rainbow! 🌈"
        },
        ["year_one"] = new Secret
        {
            Id = "year_one",
            Name = "Year One",
            Description = "365 days of duck care!",
            Hint = "A whole year...",
            SecretType = SecretType.RareEncounter,
            Rarity = SecretRarity.Mythical,
            CoinsReward = 10000,
            XpReward = 5000,
            SpecialReward = "eternal_bond_title",
            UnlockMessage = "A bond that transcends time! 🎊",
            AsciiArt = new List<string>
            {
                "   ★ YEAR ONE ★  ",
                "    365 DAYS     ",
                "   🦆💕 FOREVER  ",
                "   💕🦆 FRIENDS  "
            }
        }
    };

    // Konami code sequence
    private static readonly string[] _konamiSequence = { "up", "up", "down", "down", "left", "right", "left", "right", "b", "a" };

    // Instance state
    public Dictionary<string, DiscoveredSecret> DiscoveredSecrets { get; private set; } = new();
    private List<string> _inputBuffer = new();
    private int _sessionPetCount = 0;
    private int _sessionSqueakCount = 0;
    private string _lastCheckTime = "";
    private string _specialDateChecked = "";

    public SecretsSystem()
    {
    }

    /// <summary>
    /// Check if input sequence triggers a secret (for Konami code)
    /// </summary>
    public Secret? CheckInputSequence(string inputKey)
    {
        _inputBuffer.Add(inputKey.ToLower());

        // Keep buffer manageable
        if (_inputBuffer.Count > 20)
        {
            _inputBuffer = _inputBuffer.Skip(_inputBuffer.Count - 20).ToList();
        }

        // Check Konami Code
        if (_inputBuffer.Count >= 10)
        {
            var last10 = _inputBuffer.Skip(_inputBuffer.Count - 10).ToList();
            if (last10.SequenceEqual(_konamiSequence))
            {
                return DiscoverSecret("konami_code");
            }
        }

        return null;
    }

    /// <summary>
    /// Check text input for secret triggers
    /// </summary>
    public Secret? CheckTextInput(string text)
    {
        string textLower = text.ToLower();

        // Check for grape mentions
        if (textLower.Contains("grape") || textLower.Contains("grapes"))
        {
            return DiscoverSecret("duck_song");
        }

        // Check for squeak
        if (textLower.Contains("squeak"))
        {
            _sessionSqueakCount++;
            if (_sessionSqueakCount >= 3)
            {
                _sessionSqueakCount = 0;
                return DiscoverSecret("rubber_duck");
            }
        }

        // Check for ancient quack
        if (textLower == "quackus" || textLower == "quackus maximus" || textLower == "ancient quack")
        {
            return DiscoverSecret("ancient_quack");
        }

        return null;
    }

    /// <summary>
    /// Check for time-based secrets
    /// </summary>
    public Secret? CheckTimeSecrets()
    {
        var now = DateTime.Now;
        string timeStr = now.ToString("HH:mm");

        // Prevent duplicate checks in same minute
        if (timeStr == _lastCheckTime)
        {
            return null;
        }
        _lastCheckTime = timeStr;

        // Midnight
        if (timeStr == "00:00")
        {
            return DiscoverSecret("midnight_quack");
        }

        // 3 AM
        if (timeStr == "03:00")
        {
            return DiscoverSecret("night_owl_duck");
        }

        // Palindrome times (e.g., 12:21, 13:31)
        char[] chars = timeStr.Replace(":", "").ToCharArray();
        Array.Reverse(chars);
        string reversed = new string(chars);
        if (timeStr.Replace(":", "") == reversed)
        {
            return DiscoverSecret("palindrome");
        }

        return null;
    }

    /// <summary>
    /// Check for date-based secrets
    /// </summary>
    public Secret? CheckDateSecrets()
    {
        string today = DateTime.Today.ToString("yyyy-MM-dd");

        if (today == _specialDateChecked)
        {
            return null;
        }
        _specialDateChecked = today;

        // Check for special dates
        string monthDay = DateTime.Today.ToString("MM-dd");

        // April 1st
        if (monthDay == "04-01")
        {
            return DiscoverSecret("birthday_duck");
        }

        return null;
    }

    /// <summary>
    /// Check for coin-based secrets
    /// </summary>
    public Secret? CheckCoinSecret(int coins)
    {
        if (coins == 777 || coins == 7777)
        {
            return DiscoverSecret("triple_seven");
        }
        return null;
    }

    /// <summary>
    /// Check for action-based secrets
    /// </summary>
    public Secret? CheckActionSecrets(string action, int count = 0)
    {
        if (action == "pet")
        {
            _sessionPetCount++;
            if (_sessionPetCount >= 100)
            {
                return DiscoverSecret("hundred_pets");
            }
        }

        if (action == "feed" && count >= 1000)
        {
            return DiscoverSecret("golden_duck");
        }

        return null;
    }

    /// <summary>
    /// Check for exploration-based secrets
    /// </summary>
    public Secret? CheckExplorationSecret(string weather)
    {
        if (weather == "heavy_rain" || weather == "storm" || weather == "thunderstorm")
        {
            // 5% chance during heavy rain
            if (_random.NextDouble() < 0.05)
            {
                return DiscoverSecret("secret_pond");
            }
        }

        return null;
    }

    /// <summary>
    /// Check for playtime-based secrets
    /// </summary>
    public Secret? CheckPlaytimeSecret(int daysPlayed)
    {
        if (daysPlayed >= 365)
        {
            return DiscoverSecret("year_one");
        }
        return null;
    }

    /// <summary>
    /// Discover a secret by ID
    /// </summary>
    public Secret? DiscoverSecret(string secretId)
    {
        if (!_secrets.TryGetValue(secretId, out var secret))
        {
            return null;
        }

        if (DiscoveredSecrets.ContainsKey(secretId))
        {
            // Already discovered, just increment trigger count
            DiscoveredSecrets[secretId].TimesTriggered++;
            return null; // Don't reward again
        }

        // New discovery!
        DiscoveredSecrets[secretId] = new DiscoveredSecret
        {
            SecretId = secretId,
            DiscoveredAt = DateTime.Now
        };

        return secret;
    }

    /// <summary>
    /// Get count of discovered vs total secrets
    /// </summary>
    public (int discovered, int total) GetDiscoveredCount()
    {
        return (DiscoveredSecrets.Count, _secrets.Count);
    }

    /// <summary>
    /// Get hints for undiscovered secrets
    /// </summary>
    public List<string> GetUndiscoveredHints()
    {
        var hints = new List<string>();
        foreach (var kvp in _secrets)
        {
            if (!DiscoveredSecrets.ContainsKey(kvp.Key))
            {
                hints.Add($"[{kvp.Value.Rarity.ToString().ToUpper()}] {kvp.Value.Hint}");
            }
        }
        return hints;
    }

    /// <summary>
    /// Get discovery progress by rarity
    /// </summary>
    public Dictionary<SecretRarity, (int discovered, int total)> GetRarityProgress()
    {
        var progress = new Dictionary<SecretRarity, (int, int)>();

        foreach (SecretRarity rarity in Enum.GetValues<SecretRarity>())
        {
            int total = _secrets.Values.Count(s => s.Rarity == rarity);
            int discovered = DiscoveredSecrets.Keys.Count(sid => _secrets.TryGetValue(sid, out var s) && s.Rarity == rarity);
            progress[rarity] = (discovered, total);
        }

        return progress;
    }

    /// <summary>
    /// Get a secret by ID
    /// </summary>
    public static Secret? GetSecret(string secretId)
    {
        return _secrets.GetValueOrDefault(secretId);
    }

    /// <summary>
    /// Render the secrets discovery book
    /// </summary>
    public List<string> RenderSecretsBook(int page = 1)
    {
        var lines = new List<string>
        {
            "╔═══════════════════════════════════════════════╗",
            "║            🔮 BOOK OF SECRETS 🔮              ║",
            "╠═══════════════════════════════════════════════╣"
        };

        var (discovered, total) = GetDiscoveredCount();
        lines.Add($"║  Secrets Found: {discovered}/{total}                         ║");
        lines.Add("╠═══════════════════════════════════════════════╣");

        // Show discovered secrets
        var discoveredList = DiscoveredSecrets.Keys.ToList();
        int perPage = 5;
        int start = (page - 1) * perPage;
        var pageSecrets = discoveredList.Skip(start).Take(perPage).ToList();

        if (pageSecrets.Any())
        {
            foreach (var secretId in pageSecrets)
            {
                if (!_secrets.TryGetValue(secretId, out var secret))
                    continue;

                string rarityIcon = secret.Rarity switch
                {
                    SecretRarity.Common => "⚪",
                    SecretRarity.Uncommon => "🟢",
                    SecretRarity.Rare => "🔵",
                    SecretRarity.Legendary => "🟡",
                    SecretRarity.Mythical => "🔴",
                    _ => "⚪"
                };

                string name = secret.Name.Length > 30 ? secret.Name[..30] : secret.Name;
                lines.Add($"║  {rarityIcon} {name,-38}  ║");
                
                string desc = secret.Description.Length > 38 ? secret.Description[..38] : secret.Description;
                lines.Add($"║     {desc,-38}  ║");
            }
        }
        else
        {
            lines.Add("║  No secrets discovered yet!                   ║");
            lines.Add("║  Keep exploring and experimenting...          ║");
        }

        lines.Add("╠═══════════════════════════════════════════════╣");

        // Show hints for undiscovered
        lines.Add("║  💡 HINTS:                                    ║");
        var hints = GetUndiscoveredHints().Take(2).ToList();
        foreach (var hint in hints)
        {
            string hintText = hint.Length > 40 ? hint[..40] : hint;
            lines.Add($"║  • {hintText,-40}  ║");
        }

        if (!hints.Any())
        {
            lines.Add("║  You've found all the secrets! 🎉            ║");
        }

        int totalPages = Math.Max(1, (discoveredList.Count + perPage - 1) / perPage);

        lines.Add("╠═══════════════════════════════════════════════╣");
        lines.Add($"║  Page {page}/{totalPages}  [←/→ to navigate]                ║");
        lines.Add("╚═══════════════════════════════════════════════╝");

        return lines;
    }

    /// <summary>
    /// Convert to save data
    /// </summary>
    public Dictionary<string, object> ToSaveData()
    {
        var secretsData = new Dictionary<string, object>();
        foreach (var kvp in DiscoveredSecrets)
        {
            secretsData[kvp.Key] = kvp.Value.ToSaveData();
        }

        return new Dictionary<string, object>
        {
            ["discovered_secrets"] = secretsData,
            ["special_date_checked"] = _specialDateChecked
        };
    }

    /// <summary>
    /// Load from save data
    /// </summary>
    public static SecretsSystem FromSaveData(Dictionary<string, object> data)
    {
        var system = new SecretsSystem();

        if (data.TryGetValue("discovered_secrets", out var discovered))
        {
            if (discovered is JsonElement element && element.ValueKind == JsonValueKind.Object)
            {
                foreach (var prop in element.EnumerateObject())
                {
                    var secretData = new Dictionary<string, object>();
                    foreach (var innerProp in prop.Value.EnumerateObject())
                    {
                        secretData[innerProp.Name] = innerProp.Value.ValueKind switch
                        {
                            JsonValueKind.String => innerProp.Value.GetString() ?? "",
                            JsonValueKind.Number => innerProp.Value.GetInt32(),
                            _ => innerProp.Value.ToString()
                        };
                    }
                    system.DiscoveredSecrets[prop.Name] = DiscoveredSecret.FromSaveData(secretData);
                }
            }
            else if (discovered is Dictionary<string, object> dict)
            {
                foreach (var kvp in dict)
                {
                    if (kvp.Value is Dictionary<string, object> secretDict)
                    {
                        system.DiscoveredSecrets[kvp.Key] = DiscoveredSecret.FromSaveData(secretDict);
                    }
                }
            }
        }

        system._specialDateChecked = data.GetValueOrDefault("special_date_checked")?.ToString() ?? "";

        return system;
    }
}
