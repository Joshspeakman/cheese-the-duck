using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;

namespace StupidDuck.World;

// Note: WeatherType is already defined in Weather.cs

/// <summary>
/// Types of weather activities.
/// </summary>
public enum WeatherActivityType
{
    Play,
    Explore,
    Collect,
    Special
}

/// <summary>
/// A weather-specific activity.
/// </summary>
public class WeatherActivity
{
    public string Id { get; init; } = "";
    public string Name { get; init; } = "";
    public string Description { get; init; } = "";
    public List<WeatherType> WeatherTypes { get; init; } = new();
    public WeatherActivityType ActivityType { get; init; }
    public int DurationSeconds { get; init; } = 30;
    public int CooldownMinutes { get; init; } = 15;
    public (int min, int max) CoinsReward { get; init; } = (10, 30);
    public (int min, int max) XpReward { get; init; } = (5, 15);
    public List<string> SpecialDrops { get; init; } = new();
    public double DropChance { get; init; } = 0.1;
    public int MoodBonus { get; init; } = 10;
    public List<string> AsciiAnimation { get; init; } = new();
    public List<string> SuccessMessages { get; init; } = new();
}

/// <summary>
/// Progress for an in-progress activity.
/// </summary>
public class ActivityProgress
{
    public string ActivityId { get; set; } = "";
    public string StartedAt { get; set; } = "";
    public int DurationSeconds { get; set; }
    public bool Completed { get; set; }
}

/// <summary>
/// Weather Activities System - Weather-specific interactions and events.
/// </summary>
public class WeatherActivitiesSystem
{
    private static readonly Random _random = new();
    
    public Dictionary<string, string> ActivityCooldowns { get; private set; } = new();
    public ActivityProgress? CurrentActivity { get; private set; }
    public Dictionary<string, int> CompletedActivities { get; private set; } = new();
    public int TotalActivitiesDone { get; private set; }
    public List<string> ItemsCollected { get; private set; } = new();
    
    // Weather activities definitions
    private static readonly Dictionary<string, WeatherActivity> WeatherActivities = new()
    {
        ["sunbathing"] = new WeatherActivity
        {
            Id = "sunbathing",
            Name = "Sunbathing",
            Description = "Cheese relaxes in the warm sunshine!",
            WeatherTypes = new List<WeatherType> { WeatherType.Sunny, WeatherType.Hot },
            ActivityType = WeatherActivityType.Play,
            DurationSeconds = 20,
            CooldownMinutes = 30,
            CoinsReward = (15, 25),
            XpReward = (10, 20),
            MoodBonus = 20,
            AsciiAnimation = new List<string>
            {
                "  ☀️☀️☀️  ",
                "   \\|/   ",
                "  --🦆--  ",
                "   ~~~~   ",
                "  Ahhh... "
            },
            SuccessMessages = new List<string>
            {
                "Cheese soaks up the vitamin D!",
                "What a beautiful day for a duck!",
                "Cheese feels warm and happy!"
            }
        },
        
        ["butterfly_chase"] = new WeatherActivity
        {
            Id = "butterfly_chase",
            Name = "Chase Butterflies",
            Description = "Chase beautiful butterflies through the meadow!",
            WeatherTypes = new List<WeatherType> { WeatherType.Sunny },
            ActivityType = WeatherActivityType.Play,
            DurationSeconds = 25,
            CooldownMinutes = 20,
            CoinsReward = (20, 40),
            XpReward = (15, 25),
            SpecialDrops = new List<string> { "butterfly_wing", "flower_petal" },
            DropChance = 0.3,
            MoodBonus = 15,
            AsciiAnimation = new List<string>
            {
                "  🦋  🦋  ",
                "    🦆    ",
                "   💨→    ",
                " *waddle* "
            },
            SuccessMessages = new List<string>
            {
                "Cheese chased 5 butterflies!",
                "Almost caught one!",
                "So many pretty colors!"
            }
        },
        
        ["puddle_splash"] = new WeatherActivity
        {
            Id = "puddle_splash",
            Name = "Puddle Splashing",
            Description = "Jump and splash in rain puddles!",
            WeatherTypes = new List<WeatherType> { WeatherType.Rainy },
            ActivityType = WeatherActivityType.Play,
            DurationSeconds = 20,
            CooldownMinutes = 15,
            CoinsReward = (15, 30),
            XpReward = (10, 20),
            MoodBonus = 25,
            AsciiAnimation = new List<string>
            {
                "   🌧️🌧️   ",
                "   💦🦆💦  ",
                "  *SPLASH* ",
                "   ~~~~    "
            },
            SuccessMessages = new List<string>
            {
                "SPLASH! Water everywhere!",
                "Puddles are the best!",
                "Cheese is soaking wet and happy!"
            }
        },
        
        ["worm_hunting"] = new WeatherActivity
        {
            Id = "worm_hunting",
            Name = "Worm Hunting",
            Description = "Rain brings worms to the surface!",
            WeatherTypes = new List<WeatherType> { WeatherType.Rainy },
            ActivityType = WeatherActivityType.Collect,
            DurationSeconds = 30,
            CooldownMinutes = 25,
            CoinsReward = (25, 50),
            XpReward = (20, 35),
            SpecialDrops = new List<string> { "juicy_worm", "giant_worm" },
            DropChance = 0.5,
            MoodBonus = 10,
            AsciiAnimation = new List<string>
            {
                "  🌧️      ",
                "  🦆 ?    ",
                " ~🪱~~~   ",
                "  Found!  "
            },
            SuccessMessages = new List<string>
            {
                "Cheese found 3 juicy worms!",
                "Protein snack time!",
                "The early duck gets the worm!"
            }
        },
        
        ["rainbow_watch"] = new WeatherActivity
        {
            Id = "rainbow_watch",
            Name = "Rainbow Watching",
            Description = "Wait for a rainbow after the rain!",
            WeatherTypes = new List<WeatherType> { WeatherType.Rainy, WeatherType.Cloudy },
            ActivityType = WeatherActivityType.Special,
            DurationSeconds = 45,
            CooldownMinutes = 60,
            CoinsReward = (50, 100),
            XpReward = (30, 50),
            SpecialDrops = new List<string> { "rainbow_feather" },
            DropChance = 0.2,
            MoodBonus = 30,
            AsciiAnimation = new List<string>
            {
                "       🌈        ",
                "  ☁️       ☁️   ",
                "      🦆        ",
                "   *amazed*     "
            },
            SuccessMessages = new List<string>
            {
                "A beautiful rainbow appeared!",
                "Cheese made a rainbow wish!",
                "Seven colors of joy!"
            }
        },
        
        ["snowball_play"] = new WeatherActivity
        {
            Id = "snowball_play",
            Name = "Snowball Fun",
            Description = "Roll around and play in the snow!",
            WeatherTypes = new List<WeatherType> { WeatherType.Snowy },
            ActivityType = WeatherActivityType.Play,
            DurationSeconds = 25,
            CooldownMinutes = 20,
            CoinsReward = (20, 40),
            XpReward = (15, 30),
            MoodBonus = 20,
            AsciiAnimation = new List<string>
            {
                "  ❄️ ❄️ ❄️  ",
                "    ⚪🦆   ",
                "   *roll*  ",
                "  ❄️ ❄️ ❄️  "
            },
            SuccessMessages = new List<string>
            {
                "Cheese made a snowball!",
                "Brrr but fun!",
                "Snow duck mode activated!"
            }
        },
        
        ["snow_angel"] = new WeatherActivity
        {
            Id = "snow_angel",
            Name = "Snow Duck Angel",
            Description = "Make a duck-shaped angel in the snow!",
            WeatherTypes = new List<WeatherType> { WeatherType.Snowy },
            ActivityType = WeatherActivityType.Special,
            DurationSeconds = 15,
            CooldownMinutes = 30,
            CoinsReward = (30, 50),
            XpReward = (20, 35),
            MoodBonus = 25,
            AsciiAnimation = new List<string>
            {
                "  ❄️     ❄️  ",
                "    \\🦆/   ",
                "    /  \\   ",
                "  *flap*   "
            },
            SuccessMessages = new List<string>
            {
                "Perfect snow duck angel!",
                "It looks just like Cheese!",
                "Art in the snow!"
            }
        },
        
        ["icicle_collect"] = new WeatherActivity
        {
            Id = "icicle_collect",
            Name = "Icicle Collection",
            Description = "Carefully collect pretty icicles!",
            WeatherTypes = new List<WeatherType> { WeatherType.Snowy, WeatherType.Cold },
            ActivityType = WeatherActivityType.Collect,
            DurationSeconds = 30,
            CooldownMinutes = 25,
            CoinsReward = (25, 45),
            XpReward = (15, 30),
            SpecialDrops = new List<string> { "crystal_icicle", "frozen_dewdrop" },
            DropChance = 0.35,
            AsciiAnimation = new List<string>
            {
                "   🧊🧊🧊   ",
                "     |     ",
                "    🦆     ",
                "  *clink*  "
            },
            SuccessMessages = new List<string>
            {
                "Found some beautiful icicles!",
                "So cold and sparkly!",
                "Nature's crystals!"
            }
        },
        
        ["storm_watch"] = new WeatherActivity
        {
            Id = "storm_watch",
            Name = "Storm Watching",
            Description = "Watch the dramatic storm from safety!",
            WeatherTypes = new List<WeatherType> { WeatherType.Stormy },
            ActivityType = WeatherActivityType.Special,
            DurationSeconds = 40,
            CooldownMinutes = 45,
            CoinsReward = (40, 80),
            XpReward = (25, 45),
            MoodBonus = 10,
            AsciiAnimation = new List<string>
            {
                "  ⚡ ☁️ ⚡   ",
                "   🌧️🌧️    ",
                "  [🦆]     ",
                " *window*  "
            },
            SuccessMessages = new List<string>
            {
                "The storm is intense!",
                "Cheese watches from inside, cozy and dry.",
                "Nature's power is amazing!"
            }
        },
        
        ["thunder_count"] = new WeatherActivity
        {
            Id = "thunder_count",
            Name = "Count Thunder",
            Description = "Count the seconds between lightning and thunder!",
            WeatherTypes = new List<WeatherType> { WeatherType.Stormy },
            ActivityType = WeatherActivityType.Play,
            DurationSeconds = 30,
            CooldownMinutes = 30,
            CoinsReward = (30, 60),
            XpReward = (20, 40),
            SpecialDrops = new List<string> { "static_feather" },
            DropChance = 0.15,
            AsciiAnimation = new List<string>
            {
                "   ⚡     ",
                "  1...2...3",
                "   BOOM!  ",
                "   🦆!    "
            },
            SuccessMessages = new List<string>
            {
                "That was close! Only 3 seconds!",
                "The storm is far away now.",
                "Cheese is getting good at counting!"
            }
        },
        
        ["kite_flying"] = new WeatherActivity
        {
            Id = "kite_flying",
            Name = "Fly a Kite",
            Description = "The wind is perfect for kite flying!",
            WeatherTypes = new List<WeatherType> { WeatherType.Windy },
            ActivityType = WeatherActivityType.Play,
            DurationSeconds = 35,
            CooldownMinutes = 25,
            CoinsReward = (25, 50),
            XpReward = (20, 35),
            MoodBonus = 20,
            AsciiAnimation = new List<string>
            {
                "      🪁   ",
                "     /     ",
                "    /      ",
                "   🦆      "
            },
            SuccessMessages = new List<string>
            {
                "The kite soars high!",
                "Look at it dance in the wind!",
                "Cheese is a master kite flyer!"
            }
        },
        
        ["leaf_catch"] = new WeatherActivity
        {
            Id = "leaf_catch",
            Name = "Catch Leaves",
            Description = "Catch swirling autumn leaves in the wind!",
            WeatherTypes = new List<WeatherType> { WeatherType.Windy },
            ActivityType = WeatherActivityType.Collect,
            DurationSeconds = 25,
            CooldownMinutes = 20,
            CoinsReward = (20, 40),
            XpReward = (15, 30),
            SpecialDrops = new List<string> { "golden_leaf", "red_maple_leaf" },
            DropChance = 0.4,
            AsciiAnimation = new List<string>
            {
                "  🍂 🍁 🍂  ",
                "    💨    ",
                "    🦆    ",
                "  *catch* "
            },
            SuccessMessages = new List<string>
            {
                "Caught 5 colorful leaves!",
                "They're so pretty!",
                "A perfect collection!"
            }
        },
        
        ["fog_explore"] = new WeatherActivity
        {
            Id = "fog_explore",
            Name = "Mysterious Fog Walk",
            Description = "Explore the mysterious foggy landscape!",
            WeatherTypes = new List<WeatherType> { WeatherType.Foggy },
            ActivityType = WeatherActivityType.Explore,
            DurationSeconds = 40,
            CooldownMinutes = 35,
            CoinsReward = (35, 70),
            XpReward = (25, 45),
            SpecialDrops = new List<string> { "mist_crystal", "fog_essence" },
            DropChance = 0.25,
            MoodBonus = 5,
            AsciiAnimation = new List<string>
            {
                "  ░░░░░░  ",
                "  ░🦆░░░  ",
                "  ░░░?░░  ",
                " *spooky* "
            },
            SuccessMessages = new List<string>
            {
                "What was that shadow?",
                "Cheese found something in the mist!",
                "Mysterious and exciting!"
            }
        },
        
        ["cloud_shapes"] = new WeatherActivity
        {
            Id = "cloud_shapes",
            Name = "Cloud Watching",
            Description = "Find fun shapes in the clouds!",
            WeatherTypes = new List<WeatherType> { WeatherType.Cloudy },
            ActivityType = WeatherActivityType.Play,
            DurationSeconds = 30,
            CooldownMinutes = 20,
            CoinsReward = (15, 30),
            XpReward = (10, 25),
            MoodBonus = 15,
            AsciiAnimation = new List<string>
            {
                "  ☁️ ☁️ ☁️  ",
                "   (o o)  ",
                "    🦆    ",
                "  *dream* "
            },
            SuccessMessages = new List<string>
            {
                "That cloud looks like a duck!",
                "Cheese sees a giant bread loaf!",
                "So peaceful and relaxing."
            }
        },
        
        ["pond_swim"] = new WeatherActivity
        {
            Id = "pond_swim",
            Name = "Cool Swim",
            Description = "Take a refreshing swim in the pond!",
            WeatherTypes = new List<WeatherType> { WeatherType.Hot, WeatherType.Sunny },
            ActivityType = WeatherActivityType.Play,
            DurationSeconds = 25,
            CooldownMinutes = 20,
            CoinsReward = (20, 40),
            XpReward = (15, 30),
            MoodBonus = 25,
            AsciiAnimation = new List<string>
            {
                "   ☀️☀️    ",
                "   🦆~    ",
                "  ~~~~   ",
                " *splash* "
            },
            SuccessMessages = new List<string>
            {
                "So refreshing!",
                "Perfect temperature!",
                "Cheese is a natural swimmer!"
            }
        }
    };
    
    /// <summary>
    /// Get activities available for current weather.
    /// </summary>
    public List<WeatherActivity> GetAvailableActivities(string weather)
    {
        if (!Enum.TryParse<WeatherType>(weather, true, out var weatherType))
            weatherType = WeatherType.Cloudy;
        
        DateTime now = DateTime.Now;
        var available = new List<WeatherActivity>();
        
        foreach (var activity in WeatherActivities.Values)
        {
            if (!activity.WeatherTypes.Contains(weatherType))
                continue;
            
            // Check cooldown
            if (ActivityCooldowns.TryGetValue(activity.Id, out var lastDoneStr))
            {
                if (DateTime.TryParse(lastDoneStr, out var lastDone))
                {
                    double cooldownSeconds = activity.CooldownMinutes * 60;
                    if ((now - lastDone).TotalSeconds < cooldownSeconds)
                        continue;
                }
            }
            
            available.Add(activity);
        }
        
        return available;
    }
    
    /// <summary>
    /// Start a weather activity.
    /// </summary>
    public WeatherActivity? StartActivity(string activityId, string weather)
    {
        if (CurrentActivity != null)
            return null;
        
        var available = GetAvailableActivities(weather);
        var activity = available.FirstOrDefault(a => a.Id == activityId);
        
        if (activity == null)
            return null;
        
        CurrentActivity = new ActivityProgress
        {
            ActivityId = activityId,
            StartedAt = DateTime.Now.ToString("o"),
            DurationSeconds = activity.DurationSeconds
        };
        
        return activity;
    }
    
    /// <summary>
    /// Check if current activity is complete and return results.
    /// </summary>
    public (WeatherActivity? activity, Dictionary<string, object>? results) CheckActivityComplete()
    {
        if (CurrentActivity == null)
            return (null, null);
        
        if (!DateTime.TryParse(CurrentActivity.StartedAt, out var started))
            return (null, null);
        
        double elapsed = (DateTime.Now - started).TotalSeconds;
        
        if (elapsed < CurrentActivity.DurationSeconds)
            return (null, null);
        
        if (!WeatherActivities.TryGetValue(CurrentActivity.ActivityId, out var activity))
        {
            CurrentActivity = null;
            return (null, null);
        }
        
        // Calculate rewards
        int coins = _random.Next(activity.CoinsReward.min, activity.CoinsReward.max + 1);
        int xp = _random.Next(activity.XpReward.min, activity.XpReward.max + 1);
        
        // Check for special drops
        string? specialDrop = null;
        if (activity.SpecialDrops.Any() && _random.NextDouble() < activity.DropChance)
        {
            specialDrop = activity.SpecialDrops[_random.Next(activity.SpecialDrops.Count)];
            ItemsCollected.Add(specialDrop);
        }
        
        string message = activity.SuccessMessages.Any() 
            ? activity.SuccessMessages[_random.Next(activity.SuccessMessages.Count)]
            : $"Completed {activity.Name}!";
        
        // Update tracking
        ActivityCooldowns[activity.Id] = DateTime.Now.ToString("o");
        CompletedActivities[activity.Id] = CompletedActivities.GetValueOrDefault(activity.Id, 0) + 1;
        TotalActivitiesDone++;
        CurrentActivity = null;
        
        var results = new Dictionary<string, object>
        {
            ["coins"] = coins,
            ["xp"] = xp,
            ["mood_bonus"] = activity.MoodBonus,
            ["special_drop"] = specialDrop ?? (object)"",
            ["message"] = message
        };
        
        return (activity, results);
    }
    
    /// <summary>
    /// Get progress of current activity (0.0 to 1.0).
    /// </summary>
    public (double progress, WeatherActivity? activity) GetActivityProgress()
    {
        if (CurrentActivity == null)
            return (0, null);
        
        if (!WeatherActivities.TryGetValue(CurrentActivity.ActivityId, out var activity))
            return (0, null);
        
        if (!DateTime.TryParse(CurrentActivity.StartedAt, out var started))
            return (0, null);
        
        double elapsed = (DateTime.Now - started).TotalSeconds;
        double progress = Math.Min(1.0, elapsed / CurrentActivity.DurationSeconds);
        
        return (progress, activity);
    }
    
    /// <summary>
    /// Render available activities for selection.
    /// </summary>
    public List<string> RenderActivitySelection(string weather)
    {
        var lines = new List<string>
        {
            "╔═══════════════════════════════════════════════╗",
            $"║      🌤️ WEATHER ACTIVITIES ({weather.ToUpper()})        ║",
            "╠═══════════════════════════════════════════════╣"
        };
        
        var activities = GetAvailableActivities(weather);
        
        if (!activities.Any())
        {
            lines.Add("║  No activities available right now!           ║");
            lines.Add("║  Check back when the weather changes,         ║");
            lines.Add("║  or wait for cooldowns to reset.              ║");
        }
        else
        {
            int i = 1;
            foreach (var activity in activities)
            {
                lines.Add($"║  [{i}] {activity.Name,-35}  ║");
                string desc = activity.Description.Length > 40 
                    ? activity.Description.Substring(0, 40) 
                    : activity.Description;
                lines.Add($"║      {desc,-41}  ║");
                lines.Add($"║      ⏱️ {activity.DurationSeconds}s  💰 {activity.CoinsReward.min}-{activity.CoinsReward.max}  ✨ {activity.XpReward.min}-{activity.XpReward.max} XP ║");
                lines.Add("║                                               ║");
                i++;
            }
        }
        
        lines.Add("╠═══════════════════════════════════════════════╣");
        lines.Add("║  Select an activity number or [B] to go back  ║");
        lines.Add("╚═══════════════════════════════════════════════╝");
        
        return lines;
    }
    
    /// <summary>
    /// Render current activity in progress.
    /// </summary>
    public List<string> RenderActivityProgress()
    {
        var (progress, activity) = GetActivityProgress();
        if (activity == null)
            return new List<string>();
        
        // Progress bar
        int barWidth = 30;
        int filled = (int)(progress * barWidth);
        string bar = new string('█', filled) + new string('░', barWidth - filled);
        
        var lines = new List<string>
        {
            "╔═══════════════════════════════════════════════╗",
            $"║      🎯 {activity.Name.ToUpper(),-30}  ║",
            "╠═══════════════════════════════════════════════╣"
        };
        
        // Add animation
        foreach (var animLine in activity.AsciiAnimation)
        {
            string paddedLine = animLine.Length > 43 
                ? animLine.Substring(0, 43) 
                : animLine.PadLeft((43 + animLine.Length) / 2).PadRight(43);
            lines.Add($"║  {paddedLine}  ║");
        }
        
        lines.Add("║                                               ║");
        lines.Add($"║  [{bar}]  ║");
        lines.Add($"║  {(int)(progress * 100),42}%  ║");
        lines.Add("╚═══════════════════════════════════════════════╝");
        
        return lines;
    }
    
    /// <summary>
    /// Convert to save data.
    /// </summary>
    public Dictionary<string, object?> ToSaveData()
    {
        return new Dictionary<string, object?>
        {
            ["activity_cooldowns"] = ActivityCooldowns,
            ["completed_activities"] = CompletedActivities,
            ["total_activities_done"] = TotalActivitiesDone,
            ["items_collected"] = ItemsCollected.TakeLast(50).ToList()
        };
    }
    
    /// <summary>
    /// Load from save data.
    /// </summary>
    public static WeatherActivitiesSystem FromSaveData(Dictionary<string, JsonElement> data)
    {
        var system = new WeatherActivitiesSystem();
        
        if (data.TryGetValue("activity_cooldowns", out var cooldownsEl) && cooldownsEl.ValueKind == JsonValueKind.Object)
        {
            foreach (var prop in cooldownsEl.EnumerateObject())
                system.ActivityCooldowns[prop.Name] = prop.Value.GetString() ?? "";
        }
        
        if (data.TryGetValue("completed_activities", out var compEl) && compEl.ValueKind == JsonValueKind.Object)
        {
            foreach (var prop in compEl.EnumerateObject())
                system.CompletedActivities[prop.Name] = prop.Value.GetInt32();
        }
        
        if (data.TryGetValue("total_activities_done", out var totalEl))
            system.TotalActivitiesDone = totalEl.GetInt32();
        
        if (data.TryGetValue("items_collected", out var itemsEl) && itemsEl.ValueKind == JsonValueKind.Array)
            system.ItemsCollected = itemsEl.EnumerateArray().Select(e => e.GetString() ?? "").ToList();
        
        return system;
    }
}
