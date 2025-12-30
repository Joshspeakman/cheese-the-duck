using System;
using System.Collections.Generic;
using System.Linq;

namespace StupidDuck.Duck;

/// <summary>
/// Categories of titles.
/// </summary>
public enum TitleCategory
{
    Achievement,
    Relationship,
    Skill,
    Seasonal,
    Special,
    Hidden
}

/// <summary>
/// Rarity of titles.
/// </summary>
public enum TitleRarity
{
    Common,
    Uncommon,
    Rare,
    Epic,
    Legendary,
    Mythic
}

/// <summary>
/// A title that can be earned.
/// </summary>
public class Title
{
    public string Id { get; set; } = "";
    public string Name { get; set; } = "";
    public string Description { get; set; } = "";
    public TitleCategory Category { get; set; }
    public TitleRarity Rarity { get; set; }
    public string? Prefix { get; set; }
    public string? Suffix { get; set; }
    public string Color { get; set; } = "yellow";
    public string UnlockCondition { get; set; } = "";
    public int XpBonus { get; set; }
    public string? SpecialEffect { get; set; }
}

/// <summary>
/// A title the player has earned.
/// </summary>
public class EarnedTitle
{
    public string TitleId { get; set; } = "";
    public DateTime EarnedAt { get; set; }
    public string EarnedFrom { get; set; } = "";
    public int TimesEquipped { get; set; }
    public bool IsFavorite { get; set; }
}

/// <summary>
/// System for managing titles and nicknames.
/// </summary>
public class TitlesSystem
{
    // =============================================================================
    // TITLE DEFINITIONS
    // =============================================================================

    public static readonly Dictionary<string, Title> AllTitles = new()
    {
        // Achievement Titles
        ["new_caretaker"] = new Title
        {
            Id = "new_caretaker",
            Name = "New Caretaker",
            Description = "Just starting your journey",
            Category = TitleCategory.Achievement,
            Rarity = TitleRarity.Common,
            Suffix = "the Beginner",
            UnlockCondition = "Start the game"
        },
        ["dedicated"] = new Title
        {
            Id = "dedicated",
            Name = "Dedicated",
            Description = "Logged in for 7 days in a row",
            Category = TitleCategory.Achievement,
            Rarity = TitleRarity.Uncommon,
            Prefix = "Dedicated",
            UnlockCondition = "7 day login streak",
            XpBonus = 5
        },
        ["devoted"] = new Title
        {
            Id = "devoted",
            Name = "Devoted",
            Description = "Logged in for 30 days in a row",
            Category = TitleCategory.Achievement,
            Rarity = TitleRarity.Rare,
            Prefix = "Devoted",
            UnlockCondition = "30 day login streak",
            XpBonus = 10
        },
        ["eternal_bond"] = new Title
        {
            Id = "eternal_bond",
            Name = "Eternal Bond",
            Description = "100+ day login streak",
            Category = TitleCategory.Achievement,
            Rarity = TitleRarity.Legendary,
            Prefix = "Eternally Bonded",
            UnlockCondition = "100 day login streak",
            XpBonus = 25,
            SpecialEffect = "golden_text"
        },
        ["first_million"] = new Title
        {
            Id = "first_million",
            Name = "Millionaire",
            Description = "Earned 1,000,000 total coins",
            Category = TitleCategory.Achievement,
            Rarity = TitleRarity.Epic,
            Suffix = "the Rich",
            UnlockCondition = "Earn 1,000,000 coins lifetime",
            XpBonus = 15
        },
        // Relationship Titles
        ["acquaintance"] = new Title
        {
            Id = "acquaintance",
            Name = "Acquaintance",
            Description = "Just getting to know each other",
            Category = TitleCategory.Relationship,
            Rarity = TitleRarity.Common,
            Suffix = "'s Acquaintance",
            UnlockCondition = "Reach relationship level 1"
        },
        ["friend"] = new Title
        {
            Id = "friend",
            Name = "Friend",
            Description = "A true friend",
            Category = TitleCategory.Relationship,
            Rarity = TitleRarity.Uncommon,
            Suffix = "'s Friend",
            UnlockCondition = "Reach relationship level 5",
            XpBonus = 5
        },
        ["best_friend"] = new Title
        {
            Id = "best_friend",
            Name = "Best Friend",
            Description = "Best friends forever!",
            Category = TitleCategory.Relationship,
            Rarity = TitleRarity.Rare,
            Suffix = "'s Best Friend",
            UnlockCondition = "Reach relationship level 10",
            XpBonus = 10
        },
        ["soulmate"] = new Title
        {
            Id = "soulmate",
            Name = "Soulmate",
            Description = "An unbreakable bond",
            Category = TitleCategory.Relationship,
            Rarity = TitleRarity.Legendary,
            Prefix = "Soulmate of",
            UnlockCondition = "Reach relationship level 20",
            XpBonus = 20,
            SpecialEffect = "heart_particles"
        },
        ["duck_whisperer"] = new Title
        {
            Id = "duck_whisperer",
            Name = "Duck Whisperer",
            Description = "Understands ducks on a deep level",
            Category = TitleCategory.Relationship,
            Rarity = TitleRarity.Epic,
            Prefix = "The",
            Suffix = "Duck Whisperer",
            UnlockCondition = "Maximum relationship with 3 ducks",
            XpBonus = 15
        },
        // Skill Titles
        ["master_fisher"] = new Title
        {
            Id = "master_fisher",
            Name = "Master Fisher",
            Description = "Caught 100+ fish",
            Category = TitleCategory.Skill,
            Rarity = TitleRarity.Rare,
            Prefix = "Master Fisher",
            UnlockCondition = "Catch 100 fish",
            XpBonus = 10
        },
        ["legendary_angler"] = new Title
        {
            Id = "legendary_angler",
            Name = "Legendary Angler",
            Description = "Caught a legendary fish",
            Category = TitleCategory.Skill,
            Rarity = TitleRarity.Legendary,
            Suffix = "the Legendary Angler",
            UnlockCondition = "Catch a legendary fish",
            XpBonus = 20
        },
        ["green_thumb"] = new Title
        {
            Id = "green_thumb",
            Name = "Green Thumb",
            Description = "Harvested 50+ plants",
            Category = TitleCategory.Skill,
            Rarity = TitleRarity.Uncommon,
            Prefix = "Green Thumb",
            UnlockCondition = "Harvest 50 plants",
            XpBonus = 5
        },
        ["master_gardener"] = new Title
        {
            Id = "master_gardener",
            Name = "Master Gardener",
            Description = "Grew a rare golden flower",
            Category = TitleCategory.Skill,
            Rarity = TitleRarity.Epic,
            Prefix = "Master Gardener",
            UnlockCondition = "Grow a golden flower",
            XpBonus = 15
        },
        ["treasure_hunter"] = new Title
        {
            Id = "treasure_hunter",
            Name = "Treasure Hunter",
            Description = "Found 25+ treasures",
            Category = TitleCategory.Skill,
            Rarity = TitleRarity.Rare,
            Suffix = "the Treasure Hunter",
            UnlockCondition = "Find 25 treasures",
            XpBonus = 10
        },
        ["trick_master"] = new Title
        {
            Id = "trick_master",
            Name = "Trick Master",
            Description = "Learned 10+ tricks",
            Category = TitleCategory.Skill,
            Rarity = TitleRarity.Rare,
            Prefix = "Trick Master",
            UnlockCondition = "Learn 10 tricks",
            XpBonus = 10
        },
        ["performance_star"] = new Title
        {
            Id = "performance_star",
            Name = "Performance Star",
            Description = "50 perfect trick performances",
            Category = TitleCategory.Skill,
            Rarity = TitleRarity.Epic,
            Prefix = "⭐",
            Suffix = "the Star",
            UnlockCondition = "50 perfect performances",
            XpBonus = 15
        },
        // Seasonal Titles
        ["spring_spirit"] = new Title
        {
            Id = "spring_spirit",
            Name = "Spring Spirit",
            Description = "Celebrated the Spring Festival",
            Category = TitleCategory.Seasonal,
            Rarity = TitleRarity.Rare,
            Prefix = "🌸",
            Suffix = "of Spring",
            UnlockCondition = "Complete Spring Festival",
            XpBonus = 5
        },
        ["summer_soul"] = new Title
        {
            Id = "summer_soul",
            Name = "Summer Soul",
            Description = "Celebrated the Summer Festival",
            Category = TitleCategory.Seasonal,
            Rarity = TitleRarity.Rare,
            Prefix = "☀️",
            Suffix = "of Summer",
            UnlockCondition = "Complete Summer Festival",
            XpBonus = 5
        },
        ["autumn_guardian"] = new Title
        {
            Id = "autumn_guardian",
            Name = "Autumn Guardian",
            Description = "Celebrated the Autumn Festival",
            Category = TitleCategory.Seasonal,
            Rarity = TitleRarity.Rare,
            Prefix = "🍂",
            Suffix = "of Autumn",
            UnlockCondition = "Complete Autumn Festival",
            XpBonus = 5
        },
        ["winter_wanderer"] = new Title
        {
            Id = "winter_wanderer",
            Name = "Winter Wanderer",
            Description = "Celebrated the Winter Festival",
            Category = TitleCategory.Seasonal,
            Rarity = TitleRarity.Rare,
            Prefix = "❄️",
            Suffix = "of Winter",
            UnlockCondition = "Complete Winter Festival",
            XpBonus = 5
        },
        ["season_master"] = new Title
        {
            Id = "season_master",
            Name = "Season Master",
            Description = "Completed all seasonal festivals",
            Category = TitleCategory.Seasonal,
            Rarity = TitleRarity.Legendary,
            Prefix = "🌍",
            Suffix = "Master of Seasons",
            UnlockCondition = "Complete all 4 seasonal festivals",
            XpBonus = 25,
            SpecialEffect = "rainbow_text"
        },
        // Special Titles
        ["duck_day_champion"] = new Title
        {
            Id = "duck_day_champion",
            Name = "Duck Day Champion",
            Description = "Won Duck Day competition",
            Category = TitleCategory.Special,
            Rarity = TitleRarity.Legendary,
            Prefix = "🦆 Champion",
            UnlockCondition = "Win Duck Day",
            XpBonus = 30
        },
        ["collector"] = new Title
        {
            Id = "collector",
            Name = "Collector",
            Description = "Collected 50+ unique items",
            Category = TitleCategory.Special,
            Rarity = TitleRarity.Uncommon,
            Suffix = "the Collector",
            UnlockCondition = "Own 50 unique items",
            XpBonus = 5
        },
        ["completionist"] = new Title
        {
            Id = "completionist",
            Name = "Completionist",
            Description = "Unlocked all achievements",
            Category = TitleCategory.Special,
            Rarity = TitleRarity.Mythic,
            Prefix = "✨",
            Suffix = "the Completionist ✨",
            UnlockCondition = "Unlock all achievements",
            XpBonus = 50,
            SpecialEffect = "sparkle_name"
        },
        // Hidden Titles
        ["night_owl"] = new Title
        {
            Id = "night_owl",
            Name = "Night Owl",
            Description = "Play between midnight and 5 AM",
            Category = TitleCategory.Hidden,
            Rarity = TitleRarity.Rare,
            Suffix = "🦉",
            UnlockCondition = "Play at night 10 times",
            XpBonus = 5
        },
        ["early_bird"] = new Title
        {
            Id = "early_bird",
            Name = "Early Bird",
            Description = "Play between 5 AM and 7 AM",
            Category = TitleCategory.Hidden,
            Rarity = TitleRarity.Rare,
            Prefix = "🌅",
            UnlockCondition = "Play early morning 10 times",
            XpBonus = 5
        },
        ["secret_finder"] = new Title
        {
            Id = "secret_finder",
            Name = "Secret Finder",
            Description = "Found a hidden secret",
            Category = TitleCategory.Hidden,
            Rarity = TitleRarity.Epic,
            Suffix = "🔍",
            UnlockCondition = "Discover a hidden secret",
            XpBonus = 15
        },
        ["konami_master"] = new Title
        {
            Id = "konami_master",
            Name = "Konami Master",
            Description = "Entered the secret code",
            Category = TitleCategory.Hidden,
            Rarity = TitleRarity.Legendary,
            Prefix = "⬆️⬆️⬇️⬇️",
            UnlockCondition = "Enter the Konami code",
            XpBonus = 25,
            SpecialEffect = "retro_style"
        }
    };

    // =============================================================================
    // STATE
    // =============================================================================

    public Dictionary<string, EarnedTitle> EarnedTitles { get; set; } = new();
    public string? CurrentTitle { get; set; }
    public string DuckNickname { get; set; } = "Cheese";
    public string OwnerNickname { get; set; } = "Friend";
    public int TotalTitlesEarned { get; set; }
    public List<string> FavoriteTitles { get; set; } = new();
    public string TitleDisplayMode { get; set; } = "prefix"; // prefix, suffix, both

    // =============================================================================
    // TITLE MANAGEMENT
    // =============================================================================

    /// <summary>
    /// Earn a new title.
    /// </summary>
    public (bool Success, string Message) EarnTitle(string titleId, string earnedFrom = "achievement")
    {
        if (EarnedTitles.ContainsKey(titleId))
            return (false, "Already have this title!");

        if (!AllTitles.TryGetValue(titleId, out var title))
            return (false, "Title not found!");

        EarnedTitles[titleId] = new EarnedTitle
        {
            TitleId = titleId,
            EarnedAt = DateTime.Now,
            EarnedFrom = earnedFrom
        };

        TotalTitlesEarned++;

        // Auto-equip if first title
        if (string.IsNullOrEmpty(CurrentTitle))
            CurrentTitle = titleId;

        var rarityEmoji = title.Rarity switch
        {
            TitleRarity.Common => "",
            TitleRarity.Uncommon => "✦",
            TitleRarity.Rare => "★",
            TitleRarity.Epic => "★★",
            TitleRarity.Legendary => "★★★",
            TitleRarity.Mythic => "✨★★★✨",
            _ => ""
        };

        return (true, $"🎖️ New Title Earned: {rarityEmoji} {title.Name}!");
    }

    /// <summary>
    /// Equip a title.
    /// </summary>
    public (bool Success, string Message) EquipTitle(string titleId)
    {
        if (!EarnedTitles.TryGetValue(titleId, out var earned))
            return (false, "You haven't earned this title!");

        CurrentTitle = titleId;
        earned.TimesEquipped++;

        var name = AllTitles.TryGetValue(titleId, out var title) ? title.Name : titleId;

        return (true, $"🏷️ Equipped title: {name}");
    }

    /// <summary>
    /// Remove current title.
    /// </summary>
    public (bool Success, string Message) UnequipTitle()
    {
        if (string.IsNullOrEmpty(CurrentTitle))
            return (false, "No title equipped!");

        CurrentTitle = null;
        return (true, "🏷️ Title removed");
    }

    /// <summary>
    /// Get the full display name with title.
    /// </summary>
    public string GetDisplayName(string? baseName = null)
    {
        var name = baseName ?? DuckNickname;

        if (string.IsNullOrEmpty(CurrentTitle))
            return name;

        if (!AllTitles.TryGetValue(CurrentTitle, out var title))
            return name;

        return TitleDisplayMode switch
        {
            "prefix" when !string.IsNullOrEmpty(title.Prefix) => $"{title.Prefix} {name}",
            "suffix" when !string.IsNullOrEmpty(title.Suffix) => $"{name} {title.Suffix}",
            "both" => GetBothDisplayName(name, title),
            _ => name
        };
    }

    private static string GetBothDisplayName(string name, Title title)
    {
        if (!string.IsNullOrEmpty(title.Prefix) && !string.IsNullOrEmpty(title.Suffix))
            return $"{title.Prefix} {name} {title.Suffix}";
        if (!string.IsNullOrEmpty(title.Prefix))
            return $"{title.Prefix} {name}";
        if (!string.IsNullOrEmpty(title.Suffix))
            return $"{name} {title.Suffix}";
        return name;
    }

    /// <summary>
    /// Get XP bonus from current title.
    /// </summary>
    public int GetXpBonus()
    {
        if (string.IsNullOrEmpty(CurrentTitle))
            return 0;

        return AllTitles.TryGetValue(CurrentTitle, out var title) ? title.XpBonus : 0;
    }

    /// <summary>
    /// Set a custom nickname.
    /// </summary>
    public (bool Success, string Message) SetNickname(string nickname, bool isDuck = true)
    {
        if (nickname.Length < 1 || nickname.Length > 20)
            return (false, "Nickname must be 1-20 characters!");

        if (isDuck)
        {
            DuckNickname = nickname;
            return (true, $"🦆 Duck is now called: {nickname}");
        }
        else
        {
            OwnerNickname = nickname;
            return (true, $"👤 You are now known as: {nickname}");
        }
    }

    /// <summary>
    /// Toggle a title as favorite.
    /// </summary>
    public (bool Success, string Message) ToggleFavorite(string titleId)
    {
        if (!EarnedTitles.TryGetValue(titleId, out var earned))
            return (false, "You haven't earned this title!");

        earned.IsFavorite = !earned.IsFavorite;

        if (earned.IsFavorite)
        {
            if (!FavoriteTitles.Contains(titleId))
                FavoriteTitles.Add(titleId);
            return (true, "⭐ Added to favorites!");
        }
        else
        {
            FavoriteTitles.Remove(titleId);
            return (true, "Removed from favorites");
        }
    }

    /// <summary>
    /// Get all titles in a category with ownership status.
    /// </summary>
    public List<(Title Title, bool Owned)> GetTitlesByCategory(TitleCategory category)
    {
        return AllTitles.Values
            .Where(t => t.Category == category)
            .Select(t => (t, EarnedTitles.ContainsKey(t.Id)))
            .ToList();
    }

    /// <summary>
    /// Check if any new titles should be earned based on stats.
    /// </summary>
    public List<string> CheckTitleConditions(Dictionary<string, int> stats)
    {
        var earned = new List<string>();

        // Login streak titles
        if (stats.GetValueOrDefault("login_streak", 0) >= 7 && !EarnedTitles.ContainsKey("dedicated"))
            earned.Add("dedicated");
        if (stats.GetValueOrDefault("login_streak", 0) >= 30 && !EarnedTitles.ContainsKey("devoted"))
            earned.Add("devoted");
        if (stats.GetValueOrDefault("login_streak", 0) >= 100 && !EarnedTitles.ContainsKey("eternal_bond"))
            earned.Add("eternal_bond");

        // Skill titles
        if (stats.GetValueOrDefault("fish_caught", 0) >= 100 && !EarnedTitles.ContainsKey("master_fisher"))
            earned.Add("master_fisher");
        if (stats.GetValueOrDefault("plants_harvested", 0) >= 50 && !EarnedTitles.ContainsKey("green_thumb"))
            earned.Add("green_thumb");
        if (stats.GetValueOrDefault("treasures_found", 0) >= 25 && !EarnedTitles.ContainsKey("treasure_hunter"))
            earned.Add("treasure_hunter");
        if (stats.GetValueOrDefault("tricks_learned", 0) >= 10 && !EarnedTitles.ContainsKey("trick_master"))
            earned.Add("trick_master");
        if (stats.GetValueOrDefault("perfect_performances", 0) >= 50 && !EarnedTitles.ContainsKey("performance_star"))
            earned.Add("performance_star");

        // Achievement titles
        if (stats.GetValueOrDefault("total_coins", 0) >= 1000000 && !EarnedTitles.ContainsKey("first_million"))
            earned.Add("first_million");
        if (stats.GetValueOrDefault("unique_items", 0) >= 50 && !EarnedTitles.ContainsKey("collector"))
            earned.Add("collector");

        return earned;
    }

    // =============================================================================
    // DISPLAY
    // =============================================================================

    /// <summary>
    /// Render the titles management screen.
    /// </summary>
    public List<string> RenderTitlesScreen()
    {
        var lines = new List<string>
        {
            "╔═══════════════════════════════════════════════╗",
            "║            🏷️ TITLES & NICKNAMES 🏷️          ║",
            "╠═══════════════════════════════════════════════╣",
            $"║  Duck: {DuckNickname,35}  ║",
            $"║  You: {OwnerNickname,36}  ║"
        };

        var displayName = GetDisplayName();
        lines.Add($"║  Display: {displayName.PadLeft(31)}  ║");

        if (!string.IsNullOrEmpty(CurrentTitle) && AllTitles.TryGetValue(CurrentTitle, out var current))
        {
            var titleName = current.Name.PadLeft(25);
            lines.Add($"║  Current Title: {titleName}  ║");
            if (current.XpBonus > 0)
                lines.Add($"║  XP Bonus: +{current.XpBonus}%                             ║");
        }

        lines.Add("╠═══════════════════════════════════════════════╣");
        lines.Add($"║  Titles Earned: {TotalTitlesEarned,3}/{AllTitles.Count,-3}                       ║");
        lines.Add("╠═══════════════════════════════════════════════╣");
        lines.Add("║  YOUR TITLES:                                 ║");

        foreach (var (tid, earned) in EarnedTitles.Take(5))
        {
            if (AllTitles.TryGetValue(tid, out var title))
            {
                var equipped = tid == CurrentTitle ? "●" : "○";
                var fav = earned.IsFavorite ? "★" : " ";
                var rarityIcon = title.Rarity switch
                {
                    TitleRarity.Common => "⚪",
                    TitleRarity.Uncommon => "🟢",
                    TitleRarity.Rare => "🔵",
                    TitleRarity.Epic => "🟣",
                    TitleRarity.Legendary => "🟡",
                    TitleRarity.Mythic => "🔴",
                    _ => "⚪"
                };
                var name = title.Name.Length > 30 ? title.Name[..30] : title.Name;
                lines.Add($"║  {equipped}{fav} {rarityIcon} {name,-30}   ║");
            }
        }

        if (EarnedTitles.Count == 0)
            lines.Add("║   No titles earned yet!                       ║");

        lines.Add("╚═══════════════════════════════════════════════╝");

        return lines;
    }

    /// <summary>
    /// Render detailed view of a title.
    /// </summary>
    public List<string> RenderTitleDetail(string titleId)
    {
        if (!AllTitles.TryGetValue(titleId, out var title))
            return new List<string> { "Title not found!" };

        var owned = EarnedTitles.ContainsKey(titleId);
        var earned = EarnedTitles.GetValueOrDefault(titleId);

        var rarityColors = new Dictionary<TitleRarity, string>
        {
            [TitleRarity.Common] = "⚪ Common",
            [TitleRarity.Uncommon] = "🟢 Uncommon",
            [TitleRarity.Rare] = "🔵 Rare",
            [TitleRarity.Epic] = "🟣 Epic",
            [TitleRarity.Legendary] = "🟡 Legendary",
            [TitleRarity.Mythic] = "🔴 Mythic"
        };

        var lines = new List<string>
        {
            "╔════════════════════════════════════╗",
            $"║  {title.Name.PadLeft(16).PadRight(32)}  ║",
            $"║  {rarityColors.GetValueOrDefault(title.Rarity, "Unknown").PadLeft(16).PadRight(32)}  ║",
            "╠════════════════════════════════════╣"
        };

        // Description
        var desc = title.Description;
        while (desc.Length > 0)
        {
            var chunk = desc.Length > 32 ? desc[..32] : desc;
            lines.Add($"║  {chunk,-32}  ║");
            desc = desc.Length > 32 ? desc[32..] : "";
        }

        lines.Add("╠════════════════════════════════════╣");

        if (!string.IsNullOrEmpty(title.Prefix))
        {
            var prefixPad = title.Prefix.PadLeft(11 + title.Prefix.Length / 2).PadRight(23);
            lines.Add($"║  Prefix: {prefixPad}  ║");
        }
        if (!string.IsNullOrEmpty(title.Suffix))
        {
            var suffixPad = title.Suffix.PadLeft(11 + title.Suffix.Length / 2).PadRight(23);
            lines.Add($"║  Suffix: {suffixPad}  ║");
        }
        if (title.XpBonus > 0)
            lines.Add($"║  XP Bonus: +{title.XpBonus}%                     ║");

        lines.Add("╠════════════════════════════════════╣");

        if (owned && earned != null)
        {
            lines.Add("║  ✓ OWNED                           ║");
            lines.Add($"║  Equipped {earned.TimesEquipped} times                 ║");
        }
        else
        {
            lines.Add("║  ✗ NOT OWNED                       ║");
            var unlock = title.UnlockCondition.Length > 23 ? title.UnlockCondition[..23] : title.UnlockCondition;
            lines.Add($"║  Unlock: {unlock,-23}  ║");
        }

        lines.Add("╚════════════════════════════════════╝");

        return lines;
    }

    // =============================================================================
    // SERIALIZATION
    // =============================================================================

    public TitlesSaveData ToSaveData() => new()
    {
        EarnedTitles = EarnedTitles.ToDictionary(
            kvp => kvp.Key,
            kvp => new EarnedTitleSaveData
            {
                TitleId = kvp.Value.TitleId,
                EarnedAt = kvp.Value.EarnedAt.ToString("O"),
                EarnedFrom = kvp.Value.EarnedFrom,
                TimesEquipped = kvp.Value.TimesEquipped,
                IsFavorite = kvp.Value.IsFavorite
            }),
        CurrentTitle = CurrentTitle,
        DuckNickname = DuckNickname,
        OwnerNickname = OwnerNickname,
        TotalTitlesEarned = TotalTitlesEarned,
        FavoriteTitles = FavoriteTitles,
        TitleDisplayMode = TitleDisplayMode
    };

    public static TitlesSystem FromSaveData(TitlesSaveData data)
    {
        var system = new TitlesSystem
        {
            CurrentTitle = data.CurrentTitle,
            DuckNickname = data.DuckNickname ?? "Cheese",
            OwnerNickname = data.OwnerNickname ?? "Friend",
            TotalTitlesEarned = data.TotalTitlesEarned,
            FavoriteTitles = data.FavoriteTitles ?? new(),
            TitleDisplayMode = data.TitleDisplayMode ?? "prefix"
        };

        if (data.EarnedTitles != null)
        {
            foreach (var (tid, tdata) in data.EarnedTitles)
            {
                system.EarnedTitles[tid] = new EarnedTitle
                {
                    TitleId = tdata.TitleId ?? tid,
                    EarnedAt = string.IsNullOrEmpty(tdata.EarnedAt) ? DateTime.Now : DateTime.Parse(tdata.EarnedAt),
                    EarnedFrom = tdata.EarnedFrom ?? "unknown",
                    TimesEquipped = tdata.TimesEquipped,
                    IsFavorite = tdata.IsFavorite
                };
            }
        }

        return system;
    }
}

/// <summary>
/// Save data for an earned title.
/// </summary>
public class EarnedTitleSaveData
{
    public string? TitleId { get; set; }
    public string? EarnedAt { get; set; }
    public string? EarnedFrom { get; set; }
    public int TimesEquipped { get; set; }
    public bool IsFavorite { get; set; }
}

/// <summary>
/// Save data for titles system.
/// </summary>
public class TitlesSaveData
{
    public Dictionary<string, EarnedTitleSaveData>? EarnedTitles { get; set; }
    public string? CurrentTitle { get; set; }
    public string? DuckNickname { get; set; }
    public string? OwnerNickname { get; set; }
    public int TotalTitlesEarned { get; set; }
    public List<string>? FavoriteTitles { get; set; }
    public string? TitleDisplayMode { get; set; }
}
