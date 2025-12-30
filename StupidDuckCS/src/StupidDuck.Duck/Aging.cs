using System;
using System.Collections.Generic;
using System.Linq;

namespace StupidDuck.Duck;

/// <summary>
/// Growth stages of the duck.
/// </summary>
public enum GrowthStage
{
    Egg,
    Hatchling,
    Duckling,
    Juvenile,
    YoungAdult,
    Adult,
    Mature,
    Elder,
    Legendary
}

/// <summary>
/// Information about a growth stage.
/// </summary>
public class StageInfo
{
    public GrowthStage Stage { get; set; }
    public string Name { get; set; } = "";
    public int MinDays { get; set; }
    public int MaxDays { get; set; } // -1 for no upper limit
    public string Description { get; set; } = "";
    public float SizeMultiplier { get; set; } = 1.0f;
    public Dictionary<string, float> StatModifiers { get; set; } = new();
    public List<string> Unlocks { get; set; } = new();
    public List<string> AsciiArt { get; set; } = new();
    public List<string> SpecialAbilities { get; set; } = new();
}

/// <summary>
/// A special event that occurred during the duck's life.
/// </summary>
public class AgeEvent
{
    public string EventType { get; set; } = "";
    public string Description { get; set; } = "";
    public DateTime OccurredAt { get; set; }
    public int AgeDays { get; set; }
}

/// <summary>
/// System for tracking duck age and growth.
/// </summary>
public class AgingSystem
{
    // =============================================================================
    // GROWTH STAGE DEFINITIONS
    // =============================================================================

    public static readonly Dictionary<GrowthStage, StageInfo> GrowthStages = new()
    {
        [GrowthStage.Egg] = new StageInfo
        {
            Stage = GrowthStage.Egg,
            Name = "Egg",
            MinDays = 0,
            MaxDays = 0,
            Description = "A mysterious egg, waiting to hatch...",
            SizeMultiplier = 0.5f,
            StatModifiers = new(),
            Unlocks = new(),
            AsciiArt = new() { "    ___    ", "   /   \\   ", "  |  ?  |  ", "   \\___/   " },
            SpecialAbilities = new()
        },
        [GrowthStage.Hatchling] = new StageInfo
        {
            Stage = GrowthStage.Hatchling,
            Name = "Hatchling",
            MinDays = 0,
            MaxDays = 3,
            Description = "A tiny, adorable freshly-hatched duck!",
            SizeMultiplier = 0.6f,
            StatModifiers = new() { ["hunger_rate"] = 1.5f, ["energy_rate"] = 1.3f, ["happiness_gain"] = 1.5f },
            Unlocks = new() { "basic_care", "feeding", "petting" },
            AsciiArt = new() { "   (\\./)   ", "   (o.o)   ", "    ('>)   ", "   *tiny*  " },
            SpecialAbilities = new() { "extra_cute" }
        },
        [GrowthStage.Duckling] = new StageInfo
        {
            Stage = GrowthStage.Duckling,
            Name = "Duckling",
            MinDays = 3,
            MaxDays = 14,
            Description = "A fluffy duckling learning about the world!",
            SizeMultiplier = 0.7f,
            StatModifiers = new() { ["hunger_rate"] = 1.3f, ["energy_rate"] = 1.2f, ["xp_gain"] = 1.2f },
            Unlocks = new() { "minigames", "exploring" },
            AsciiArt = new() { "    __     ", "  >(o )__  ", "   ( ._>   ", "  *fluffy* " },
            SpecialAbilities = new() { "quick_learner" }
        },
        [GrowthStage.Juvenile] = new StageInfo
        {
            Stage = GrowthStage.Juvenile,
            Name = "Juvenile",
            MinDays = 14,
            MaxDays = 30,
            Description = "A growing duck, full of energy!",
            SizeMultiplier = 0.85f,
            StatModifiers = new() { ["energy_rate"] = 0.9f, ["xp_gain"] = 1.1f },
            Unlocks = new() { "fishing", "basic_tricks" },
            AsciiArt = new() { "     __    ", "  __( o)>  ", " \\_ \\__/   ", "  *growing*" },
            SpecialAbilities = new() { "energetic" }
        },
        [GrowthStage.YoungAdult] = new StageInfo
        {
            Stage = GrowthStage.YoungAdult,
            Name = "Young Adult",
            MinDays = 30,
            MaxDays = 90,
            Description = "A young adult duck, becoming independent!",
            SizeMultiplier = 0.95f,
            StatModifiers = new() { ["coin_gain"] = 1.1f },
            Unlocks = new() { "garden", "treasure_hunting", "intermediate_tricks" },
            AsciiArt = new() { "      _    ", "   __( o)> ", "  \\___\\_/  ", "   *young* " },
            SpecialAbilities = new() { "social_butterfly" }
        },
        [GrowthStage.Adult] = new StageInfo
        {
            Stage = GrowthStage.Adult,
            Name = "Adult",
            MinDays = 90,
            MaxDays = 365,
            Description = "A fully grown adult duck in their prime!",
            SizeMultiplier = 1.0f,
            StatModifiers = new(),
            Unlocks = new() { "advanced_tricks", "trading", "all_locations" },
            AsciiArt = new() { "      __   ", "   __(o )> ", "  \\_____/  ", "   *prime* " },
            SpecialAbilities = new() { "balanced" }
        },
        [GrowthStage.Mature] = new StageInfo
        {
            Stage = GrowthStage.Mature,
            Name = "Mature",
            MinDays = 365,
            MaxDays = 730,
            Description = "A wise and experienced duck!",
            SizeMultiplier = 1.0f,
            StatModifiers = new() { ["coin_gain"] = 1.15f, ["xp_gain"] = 0.9f },
            Unlocks = new() { "master_tricks", "mentoring" },
            AsciiArt = new() { "      __   ", "   __(• )> ", "  \\_____/  ", "   *wise*  " },
            SpecialAbilities = new() { "wise", "mentor" }
        },
        [GrowthStage.Elder] = new StageInfo
        {
            Stage = GrowthStage.Elder,
            Name = "Elder",
            MinDays = 730,
            MaxDays = 1095,
            Description = "A venerable elder duck, respected by all!",
            SizeMultiplier = 1.0f,
            StatModifiers = new() { ["coin_gain"] = 1.25f, ["energy_rate"] = 1.2f, ["happiness_gain"] = 1.2f },
            Unlocks = new() { "elder_wisdom", "legacy_items" },
            AsciiArt = new() { "    👴     ", "   __(◕ )> ", "  \\_____/  ", "  *elder*  " },
            SpecialAbilities = new() { "respected", "storyteller" }
        },
        [GrowthStage.Legendary] = new StageInfo
        {
            Stage = GrowthStage.Legendary,
            Name = "Legendary",
            MinDays = 1095,
            MaxDays = -1,
            Description = "A legendary duck that has transcended time!",
            SizeMultiplier = 1.1f,
            StatModifiers = new() { ["coin_gain"] = 1.5f, ["xp_gain"] = 1.5f, ["happiness_gain"] = 1.5f },
            Unlocks = new() { "legendary_status", "all_abilities" },
            AsciiArt = new() { "    ✨👑    ", "   __(★ )> ", "  \\_____/  ", " *LEGEND*  " },
            SpecialAbilities = new() { "legendary_aura", "time_transcendent" }
        }
    };

    // =============================================================================
    // STATE
    // =============================================================================

    public DateTime? BirthDate { get; set; }
    public GrowthStage CurrentStage { get; set; } = GrowthStage.Hatchling;
    public int DaysInCurrentStage { get; set; }
    public List<AgeEvent> LifeEvents { get; set; } = new();
    public Dictionary<GrowthStage, DateTime> GrowthMilestones { get; set; } = new();
    public HashSet<int> BirthdaysCelebrated { get; set; } = new();
    public bool AgingPaused { get; set; }

    // =============================================================================
    // INITIALIZATION
    // =============================================================================

    /// <summary>
    /// Initialize the aging system for a new duck.
    /// </summary>
    public void Initialize(DateTime? birthDate = null)
    {
        BirthDate = birthDate ?? DateTime.Today;
        CurrentStage = GrowthStage.Hatchling;
        GrowthMilestones[GrowthStage.Hatchling] = DateTime.Now;

        LifeEvents.Add(new AgeEvent
        {
            EventType = "birth",
            Description = "A new duck was born!",
            OccurredAt = DateTime.Now,
            AgeDays = 0
        });
    }

    // =============================================================================
    // AGE CALCULATION
    // =============================================================================

    /// <summary>
    /// Get the duck's age in days.
    /// </summary>
    public int GetAgeDays()
    {
        if (!BirthDate.HasValue)
            return 0;
        return (DateTime.Today - BirthDate.Value.Date).Days;
    }

    /// <summary>
    /// Get a human-readable age string.
    /// </summary>
    public string GetAgeString()
    {
        var days = GetAgeDays();

        if (days < 7)
            return $"{days} days old";
        if (days < 30)
        {
            var weeks = days / 7;
            return $"{weeks} week{(weeks > 1 ? "s" : "")} old";
        }
        if (days < 365)
        {
            var months = days / 30;
            return $"{months} month{(months > 1 ? "s" : "")} old";
        }

        var years = days / 365;
        var remainingMonths = (days % 365) / 30;
        if (remainingMonths > 0)
            return $"{years} year{(years > 1 ? "s" : "")}, {remainingMonths} month{(remainingMonths > 1 ? "s" : "")} old";
        return $"{years} year{(years > 1 ? "s" : "")} old";
    }

    // =============================================================================
    // STAGE MANAGEMENT
    // =============================================================================

    /// <summary>
    /// Update growth stage based on age. Returns new stage if changed.
    /// </summary>
    public GrowthStage? UpdateStage()
    {
        if (AgingPaused)
            return null;

        var days = GetAgeDays();
        GrowthStage? newStage = null;

        // Find appropriate stage
        foreach (var stage in Enum.GetValues<GrowthStage>())
        {
            var stageInfo = GrowthStages[stage];
            if (days >= stageInfo.MinDays)
            {
                if (stageInfo.MaxDays == -1 || days <= stageInfo.MaxDays)
                    newStage = stage;
            }
        }

        if (newStage.HasValue && newStage.Value != CurrentStage)
        {
            var oldStage = CurrentStage;
            CurrentStage = newStage.Value;
            DaysInCurrentStage = 0;
            GrowthMilestones[newStage.Value] = DateTime.Now;

            LifeEvents.Add(new AgeEvent
            {
                EventType = "growth",
                Description = $"Grew from {oldStage} to {newStage.Value}!",
                OccurredAt = DateTime.Now,
                AgeDays = days
            });

            return newStage.Value;
        }

        return null;
    }

    /// <summary>
    /// Get information about the current growth stage.
    /// </summary>
    public StageInfo GetCurrentStageInfo() => GrowthStages[CurrentStage];

    /// <summary>
    /// Get the modifier for a specific stat based on current stage.
    /// </summary>
    public float GetStatModifier(string stat)
    {
        var stageInfo = GrowthStages[CurrentStage];
        return stageInfo.StatModifiers.TryGetValue(stat, out var modifier) ? modifier : 1.0f;
    }

    // =============================================================================
    // BIRTHDAY
    // =============================================================================

    /// <summary>
    /// Check if today is the duck's birthday. Returns (is_birthday, years).
    /// </summary>
    public (bool IsBirthday, int Years) CheckBirthday()
    {
        if (!BirthDate.HasValue)
            return (false, 0);

        var birth = BirthDate.Value;
        var today = DateTime.Today;

        if (birth.Month == today.Month && birth.Day == today.Day)
        {
            var years = today.Year - birth.Year;
            if (years > 0 && !BirthdaysCelebrated.Contains(years))
                return (true, years);
        }

        return (false, 0);
    }

    /// <summary>
    /// Mark a birthday as celebrated.
    /// </summary>
    public void CelebrateBirthday(int years)
    {
        BirthdaysCelebrated.Add(years);

        LifeEvents.Add(new AgeEvent
        {
            EventType = "birthday",
            Description = $"Celebrated {years} year{(years > 1 ? "s" : "")} birthday!",
            OccurredAt = DateTime.Now,
            AgeDays = GetAgeDays()
        });
    }

    // =============================================================================
    // LIFE EVENTS
    // =============================================================================

    /// <summary>
    /// Add a custom life event.
    /// </summary>
    public void AddLifeEvent(string eventType, string description)
    {
        LifeEvents.Add(new AgeEvent
        {
            EventType = eventType,
            Description = description,
            OccurredAt = DateTime.Now,
            AgeDays = GetAgeDays()
        });
    }

    /// <summary>
    /// Get all features unlocked up to current stage.
    /// </summary>
    public List<string> GetUnlockedFeatures()
    {
        var unlocked = new List<string>();
        var stageOrder = Enum.GetValues<GrowthStage>().ToList();
        var currentIndex = stageOrder.IndexOf(CurrentStage);

        for (var i = 0; i <= currentIndex; i++)
        {
            var stageInfo = GrowthStages[stageOrder[i]];
            unlocked.AddRange(stageInfo.Unlocks);
        }

        return unlocked;
    }

    /// <summary>
    /// Get all special abilities for current stage and below.
    /// </summary>
    public List<string> GetSpecialAbilities()
    {
        var abilities = new List<string>();
        var stageOrder = Enum.GetValues<GrowthStage>().ToList();
        var currentIndex = stageOrder.IndexOf(CurrentStage);

        for (var i = 0; i <= currentIndex; i++)
        {
            var stageInfo = GrowthStages[stageOrder[i]];
            abilities.AddRange(stageInfo.SpecialAbilities);
        }

        return abilities;
    }

    // =============================================================================
    // DISPLAY
    // =============================================================================

    /// <summary>
    /// Render the age and growth display.
    /// </summary>
    public List<string> RenderAgeDisplay()
    {
        var stageInfo = GetCurrentStageInfo();
        var ageStr = GetAgeString();

        var lines = new List<string>
        {
            "╔═══════════════════════════════════════════════╗",
            "║            🦆 DUCK GROWTH 🦆                  ║",
            "╠═══════════════════════════════════════════════╣",
        };

        // ASCII art
        foreach (var artLine in stageInfo.AsciiArt)
        {
            var paddedLine = artLine.PadLeft(22 + artLine.Length / 2).PadRight(43);
            lines.Add($"║  {paddedLine}  ║");
        }

        lines.Add("║                                               ║");
        lines.Add($"║  Stage: {stageInfo.Name,-35}  ║");
        lines.Add($"║  Age: {ageStr,-37}  ║");
        lines.Add($"║  {stageInfo.Description,-43}  ║");
        lines.Add("║                                               ║");

        // Unlocks
        if (stageInfo.Unlocks.Count > 0)
        {
            var unlockStr = string.Join(", ", stageInfo.Unlocks.Take(3));
            lines.Add($"║  Unlocks: {unlockStr,-33}  ║");
        }

        // Special abilities
        if (stageInfo.SpecialAbilities.Count > 0)
        {
            var abilityStr = string.Join(", ", stageInfo.SpecialAbilities);
            lines.Add($"║  Abilities: {abilityStr,-31}  ║");
        }

        lines.Add("╚═══════════════════════════════════════════════╝");

        return lines;
    }

    // =============================================================================
    // SERIALIZATION
    // =============================================================================

    public AgingSaveData ToSaveData() => new()
    {
        BirthDate = BirthDate?.ToString("O"),
        CurrentStage = CurrentStage.ToString(),
        DaysInCurrentStage = DaysInCurrentStage,
        LifeEvents = LifeEvents.Select(e => new AgeEventSaveData
        {
            EventType = e.EventType,
            Description = e.Description,
            OccurredAt = e.OccurredAt.ToString("O"),
            AgeDays = e.AgeDays
        }).ToList(),
        GrowthMilestones = GrowthMilestones.ToDictionary(
            kvp => kvp.Key.ToString(),
            kvp => kvp.Value.ToString("O")),
        BirthdaysCelebrated = BirthdaysCelebrated.ToList(),
        AgingPaused = AgingPaused
    };

    public static AgingSystem FromSaveData(AgingSaveData data)
    {
        var system = new AgingSystem();

        if (!string.IsNullOrEmpty(data.BirthDate))
            system.BirthDate = DateTime.Parse(data.BirthDate);

        if (Enum.TryParse<GrowthStage>(data.CurrentStage, out var stage))
            system.CurrentStage = stage;

        system.DaysInCurrentStage = data.DaysInCurrentStage;
        system.AgingPaused = data.AgingPaused;
        system.BirthdaysCelebrated = data.BirthdaysCelebrated?.ToHashSet() ?? new();

        if (data.LifeEvents != null)
        {
            system.LifeEvents = data.LifeEvents.Select(e => new AgeEvent
            {
                EventType = e.EventType ?? "",
                Description = e.Description ?? "",
                OccurredAt = string.IsNullOrEmpty(e.OccurredAt) ? DateTime.Now : DateTime.Parse(e.OccurredAt),
                AgeDays = e.AgeDays
            }).ToList();
        }

        if (data.GrowthMilestones != null)
        {
            foreach (var (stageStr, dateStr) in data.GrowthMilestones)
            {
                if (Enum.TryParse<GrowthStage>(stageStr, out var s))
                    system.GrowthMilestones[s] = DateTime.Parse(dateStr);
            }
        }

        return system;
    }
}

/// <summary>
/// Save data for age events.
/// </summary>
public class AgeEventSaveData
{
    public string? EventType { get; set; }
    public string? Description { get; set; }
    public string? OccurredAt { get; set; }
    public int AgeDays { get; set; }
}

/// <summary>
/// Save data for aging system.
/// </summary>
public class AgingSaveData
{
    public string? BirthDate { get; set; }
    public string? CurrentStage { get; set; }
    public int DaysInCurrentStage { get; set; }
    public List<AgeEventSaveData>? LifeEvents { get; set; }
    public Dictionary<string, string>? GrowthMilestones { get; set; }
    public List<int>? BirthdaysCelebrated { get; set; }
    public bool AgingPaused { get; set; }
}
