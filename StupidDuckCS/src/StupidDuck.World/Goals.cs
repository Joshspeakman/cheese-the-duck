using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;

namespace StupidDuck.World;

/// <summary>
/// A goal/quest the player can complete.
/// </summary>
public class Goal
{
    public string Id { get; set; } = "";
    public string Name { get; set; } = "";
    public string Description { get; set; } = "";
    public string GoalType { get; set; } = "";  // daily, weekly, achievement, secret
    public string Action { get; set; } = "";    // What action progresses this goal
    public int Target { get; set; }             // How many times to complete
    public int Progress { get; set; }
    public bool Completed { get; set; }
    public string? RewardItem { get; set; }
    public string RewardMessage { get; set; } = "";
    public bool Hidden { get; set; }            // Secret goals don't show until unlocked
    
    public Goal Clone()
    {
        return new Goal
        {
            Id = Id,
            Name = Name,
            Description = Description,
            GoalType = GoalType,
            Action = Action,
            Target = Target,
            Progress = Progress,
            Completed = Completed,
            RewardItem = RewardItem,
            RewardMessage = RewardMessage,
            Hidden = Hidden
        };
    }
}

/// <summary>
/// Goals/Quests system - gives players objectives to complete.
/// </summary>
public class GoalSystem
{
    private static readonly Random _random = new();
    
    private List<Goal> _activeGoals = new();
    private List<string> _completedGoals = new();
    private string? _lastDailyReset;
    private string? _lastWeeklyReset;
    private string _lastAction = "";
    private int _actionStreak;
    private double _idleTime;
    
    // Goal templates
    private static readonly List<Goal> DailyGoals = new()
    {
        new Goal
        {
            Id = "feed_duck_daily",
            Name = "Breakfast Time",
            Description = "Feed your duck 3 times today",
            GoalType = "daily",
            Action = "feed",
            Target = 3,
            RewardMessage = "Your duck had a filling day!"
        },
        new Goal
        {
            Id = "play_duck_daily",
            Name = "Playtime!",
            Description = "Play with your duck 2 times",
            GoalType = "daily",
            Action = "play",
            Target = 2,
            RewardMessage = "Fun was had by all!"
        },
        new Goal
        {
            Id = "pet_duck_daily",
            Name = "Affection",
            Description = "Pet your duck 3 times",
            GoalType = "daily",
            Action = "pet",
            Target = 3,
            RewardMessage = "Your duck feels loved!"
        },
        new Goal
        {
            Id = "talk_duck_daily",
            Name = "Chit Chat",
            Description = "Have 2 conversations with your duck",
            GoalType = "daily",
            Action = "talk",
            Target = 2,
            RewardMessage = "Communication is key!"
        },
        new Goal
        {
            Id = "clean_duck_daily",
            Name = "Squeaky Clean",
            Description = "Clean your duck today",
            GoalType = "daily",
            Action = "clean",
            Target = 1,
            RewardMessage = "Fresh as a daisy!"
        }
    };
    
    private static readonly List<Goal> WeeklyGoals = new()
    {
        new Goal
        {
            Id = "feed_duck_weekly",
            Name = "Well Fed",
            Description = "Feed your duck 20 times this week",
            GoalType = "weekly",
            Action = "feed",
            Target = 20,
            RewardItem = "fancy_bread",
            RewardMessage = "Earned: Fancy Artisan Bread!"
        },
        new Goal
        {
            Id = "play_duck_weekly",
            Name = "Party Duck",
            Description = "Play with your duck 15 times this week",
            GoalType = "weekly",
            Action = "play",
            Target = 15,
            RewardItem = "ball",
            RewardMessage = "Earned: Bouncy Ball!"
        },
        new Goal
        {
            Id = "talk_duck_weekly",
            Name = "Best Friends",
            Description = "Have 10 conversations this week",
            GoalType = "weekly",
            Action = "talk",
            Target = 10,
            RewardItem = "mirror",
            RewardMessage = "Earned: Small Mirror!"
        }
    };
    
    private static readonly List<Goal> AchievementGoals = new()
    {
        new Goal
        {
            Id = "first_feed",
            Name = "First Meal",
            Description = "Feed your duck for the first time",
            GoalType = "achievement",
            Action = "feed",
            Target = 1,
            RewardMessage = "Your journey begins!"
        },
        new Goal
        {
            Id = "hundred_feeds",
            Name = "Master Chef",
            Description = "Feed your duck 100 times",
            GoalType = "achievement",
            Action = "feed",
            Target = 100,
            RewardItem = "golden_crumb",
            RewardMessage = "LEGENDARY: Golden Crumb!"
        },
        new Goal
        {
            Id = "hundred_pets",
            Name = "Cuddle Master",
            Description = "Pet your duck 100 times",
            GoalType = "achievement",
            Action = "pet",
            Target = 100,
            RewardItem = "lucky_clover",
            RewardMessage = "RARE: Four-Leaf Clover!"
        }
    };
    
    private static readonly List<Goal> SecretGoals = new()
    {
        new Goal
        {
            Id = "midnight_quack",
            Name = "???",
            Description = "Play at midnight",
            GoalType = "secret",
            Action = "midnight_play",
            Target = 1,
            Hidden = true,
            RewardItem = "shiny_pebble",
            RewardMessage = "SECRET: Night Owl achievement!"
        },
        new Goal
        {
            Id = "triple_play",
            Name = "???",
            Description = "Play 3 times in a row",
            GoalType = "secret",
            Action = "triple_play",
            Target = 1,
            Hidden = true,
            RewardMessage = "SECRET: Triple Threat!"
        },
        new Goal
        {
            Id = "patient_one",
            Name = "???",
            Description = "Wait for 5 minutes without doing anything",
            GoalType = "secret",
            Action = "idle_wait",
            Target = 1,
            Hidden = true,
            RewardMessage = "SECRET: The Patient One"
        },
        new Goal
        {
            Id = "early_bird",
            Name = "???",
            Description = "Play before 6 AM",
            GoalType = "secret",
            Action = "early_bird",
            Target = 1,
            Hidden = true,
            RewardItem = "seeds",
            RewardMessage = "SECRET: Early Bird! The duck that gets the worm!"
        },
        new Goal
        {
            Id = "bread_obsessed",
            Name = "???",
            Description = "Feed bread 10 times in one session",
            GoalType = "secret",
            Action = "bread_feast",
            Target = 1,
            Hidden = true,
            RewardItem = "fancy_bread",
            RewardMessage = "SECRET: Bread Obsessed! Carb loading complete!"
        },
        new Goal
        {
            Id = "rainbow_witness",
            Name = "???",
            Description = "See a rainbow",
            GoalType = "secret",
            Action = "saw_rainbow",
            Target = 1,
            Hidden = true,
            RewardItem = "rainbow_crumb",
            RewardMessage = "SECRET: Rainbow Witness! Magical!"
        },
        new Goal
        {
            Id = "visitor_friend",
            Name = "???",
            Description = "Meet 5 different visitors",
            GoalType = "secret",
            Action = "met_visitors",
            Target = 5,
            Hidden = true,
            RewardItem = "glass_marble",
            RewardMessage = "SECRET: Social Butterfly! So many friends!"
        },
        new Goal
        {
            Id = "weather_watcher",
            Name = "???",
            Description = "Experience all weather types",
            GoalType = "secret",
            Action = "all_weather",
            Target = 1,
            Hidden = true,
            RewardMessage = "SECRET: Weather Watcher! Meteorologist duck!"
        },
        new Goal
        {
            Id = "marathon_session",
            Name = "???",
            Description = "Play for 30 minutes straight",
            GoalType = "secret",
            Action = "marathon",
            Target = 1,
            Hidden = true,
            RewardItem = "worm",
            RewardMessage = "SECRET: Marathon Duck! Such dedication!"
        },
        new Goal
        {
            Id = "perfectionist",
            Name = "???",
            Description = "Keep all needs above 80 for 10 minutes",
            GoalType = "secret",
            Action = "perfect_care",
            Target = 1,
            Hidden = true,
            RewardItem = "golden_crumb",
            RewardMessage = "SECRET: Perfectionist! Optimal duck care achieved!"
        },
        new Goal
        {
            Id = "chatterbox",
            Name = "???",
            Description = "Talk to duck 20 times",
            GoalType = "secret",
            Action = "talk",
            Target = 20,
            Hidden = true,
            RewardMessage = "SECRET: Chatterbox! Quack quack indeed!"
        },
        new Goal
        {
            Id = "collector",
            Name = "???",
            Description = "Find 10 collectibles",
            GoalType = "secret",
            Action = "collect_item",
            Target = 10,
            Hidden = true,
            RewardItem = "crystal_shard",
            RewardMessage = "SECRET: Collector! Shiny hoarder!"
        },
        new Goal
        {
            Id = "super_lucky",
            Name = "???",
            Description = "Play on a super lucky day",
            GoalType = "secret",
            Action = "super_lucky_day",
            Target = 1,
            Hidden = true,
            RewardMessage = "SECRET: Fortune's Favorite! The stars aligned!"
        },
        new Goal
        {
            Id = "storm_chaser",
            Name = "???",
            Description = "Play during a storm",
            GoalType = "secret",
            Action = "storm_play",
            Target = 1,
            Hidden = true,
            RewardMessage = "SECRET: Storm Chaser! Brave duck!"
        },
        new Goal
        {
            Id = "zen_master",
            Name = "???",
            Description = "Keep duck at ecstatic mood for 5 minutes",
            GoalType = "secret",
            Action = "zen_master",
            Target = 1,
            Hidden = true,
            RewardItem = "lucky_clover",
            RewardMessage = "SECRET: Zen Master! Maximum happiness achieved!"
        },
        new Goal
        {
            Id = "holiday_spirit",
            Name = "???",
            Description = "Play on a special holiday",
            GoalType = "secret",
            Action = "holiday_play",
            Target = 1,
            Hidden = true,
            RewardMessage = "SECRET: Holiday Spirit! Festive duck!"
        },
        new Goal
        {
            Id = "week_warrior",
            Name = "???",
            Description = "Maintain a 7-day streak",
            GoalType = "secret",
            Action = "week_streak",
            Target = 1,
            Hidden = true,
            RewardItem = "feather",
            RewardMessage = "SECRET: Week Warrior! Consistent friend!"
        },
        new Goal
        {
            Id = "month_master",
            Name = "???",
            Description = "Maintain a 30-day streak",
            GoalType = "secret",
            Action = "month_streak",
            Target = 1,
            Hidden = true,
            RewardItem = "ancient_artifact",
            RewardMessage = "SECRET: Month Master! Legendary dedication!"
        }
    };
    
    /// <summary>
    /// Add random daily goals.
    /// </summary>
    public void AddDailyGoals()
    {
        // Clear old daily goals
        _activeGoals = _activeGoals.Where(g => g.GoalType != "daily").ToList();
        
        // Add 3 random daily goals
        var selected = DailyGoals.OrderBy(_ => _random.Next()).Take(Math.Min(3, DailyGoals.Count));
        foreach (var template in selected)
        {
            _activeGoals.Add(template.Clone());
        }
        
        _lastDailyReset = DateTime.Now.ToString("yyyy-MM-dd");
    }
    
    /// <summary>
    /// Add weekly goals.
    /// </summary>
    public void AddWeeklyGoals()
    {
        _activeGoals = _activeGoals.Where(g => g.GoalType != "weekly").ToList();
        
        foreach (var template in WeeklyGoals)
        {
            _activeGoals.Add(template.Clone());
        }
        
        _lastWeeklyReset = DateTime.Now.ToString("yyyy-'W'WW");
    }
    
    /// <summary>
    /// Add achievement goals that weren't completed yet.
    /// </summary>
    public void AddAchievementGoals()
    {
        foreach (var template in AchievementGoals)
        {
            if (!_completedGoals.Contains(template.Id))
            {
                bool exists = _activeGoals.Any(g => g.Id == template.Id);
                if (!exists)
                {
                    _activeGoals.Add(template.Clone());
                }
            }
        }
    }
    
    /// <summary>
    /// Update progress on goals that match the action.
    /// Returns list of newly completed goals.
    /// </summary>
    public List<Goal> UpdateProgress(string action, int amount = 1)
    {
        var completed = new List<Goal>();
        
        // Track action streak for secret goals
        if (action == _lastAction)
            _actionStreak++;
        else
        {
            _actionStreak = 1;
            _lastAction = action;
        }
        
        // Reset idle timer on action
        _idleTime = 0;
        
        // Check for triple action secret
        if (_actionStreak >= 3 && action == "play")
            CheckSecretGoal("triple_play");
        
        // Check midnight play secret
        if (action == "play")
        {
            int hour = DateTime.Now.Hour;
            if (hour == 0 || hour == 23)
                CheckSecretGoal("midnight_play");
        }
        
        foreach (var goal in _activeGoals)
        {
            if (goal.Completed) continue;
            
            if (goal.Action == action)
            {
                goal.Progress += amount;
                if (goal.Progress >= goal.Target)
                {
                    goal.Completed = true;
                    _completedGoals.Add(goal.Id);
                    completed.Add(goal);
                }
            }
        }
        
        return completed;
    }
    
    /// <summary>
    /// Update time-based goals.
    /// </summary>
    public void UpdateTime(double deltaMinutes)
    {
        _idleTime += deltaMinutes;
        
        // Check for patient one secret (5 minutes idle)
        if (_idleTime >= 5)
            CheckSecretGoal("idle_wait");
        
        // Check for daily/weekly resets
        string today = DateTime.Now.ToString("yyyy-MM-dd");
        string week = DateTime.Now.ToString("yyyy-'W'WW");
        
        if (_lastDailyReset != today)
            AddDailyGoals();
        
        if (_lastWeeklyReset != week)
            AddWeeklyGoals();
    }
    
    /// <summary>
    /// Check and potentially unlock a secret goal.
    /// </summary>
    private Goal? CheckSecretGoal(string action)
    {
        foreach (var template in SecretGoals)
        {
            if (template.Action == action && !_completedGoals.Contains(template.Id))
            {
                // Add and complete the secret goal
                var goal = template.Clone();
                goal.Name = template.Description;
                goal.Progress = template.Target;
                goal.Completed = true;
                goal.Hidden = false;
                
                _activeGoals.Add(goal);
                _completedGoals.Add(goal.Id);
                return goal;
            }
        }
        return null;
    }
    
    /// <summary>
    /// Trigger a secret goal by action name.
    /// </summary>
    public Goal? TriggerSecretGoal(string action)
    {
        return CheckSecretGoal(action);
    }
    
    /// <summary>
    /// Get all active, non-completed goals.
    /// </summary>
    public List<Goal> GetActiveGoals()
    {
        return _activeGoals.Where(g => !g.Completed && !g.Hidden).ToList();
    }
    
    /// <summary>
    /// Get number of completed goals.
    /// </summary>
    public int GetCompletedCount()
    {
        return _completedGoals.Count;
    }
    
    /// <summary>
    /// Get total number of goals (including hidden ones once discovered).
    /// </summary>
    public int GetTotalCount()
    {
        return _activeGoals.Count;
    }
    
    /// <summary>
    /// Render goals display.
    /// </summary>
    public List<string> RenderGoals(int width = 60)
    {
        var lines = new List<string>();
        var activeGoals = GetActiveGoals();
        
        lines.Add("╔" + new string('═', width - 2) + "╗");
        lines.Add("║" + " 🎯 GOALS & QUESTS 🎯 ".PadLeft((width + 20) / 2).PadRight(width - 2) + "║");
        lines.Add("╠" + new string('═', width - 2) + "╣");
        
        // Group by type
        var dailyGoals = activeGoals.Where(g => g.GoalType == "daily").ToList();
        var weeklyGoals = activeGoals.Where(g => g.GoalType == "weekly").ToList();
        var achievementGoals = activeGoals.Where(g => g.GoalType == "achievement").ToList();
        
        if (dailyGoals.Any())
        {
            lines.Add("║" + " ☀️ Daily Goals ".PadRight(width - 2) + "║");
            foreach (var goal in dailyGoals)
            {
                string progressBar = $"[{goal.Progress}/{goal.Target}]";
                lines.Add("║" + $"   • {goal.Name}: {goal.Description}".PadRight(width - 12).Substring(0, width - 12) + progressBar.PadLeft(10) + "║");
            }
            lines.Add("║" + new string(' ', width - 2) + "║");
        }
        
        if (weeklyGoals.Any())
        {
            lines.Add("║" + " 📅 Weekly Goals ".PadRight(width - 2) + "║");
            foreach (var goal in weeklyGoals)
            {
                string progressBar = $"[{goal.Progress}/{goal.Target}]";
                lines.Add("║" + $"   • {goal.Name}: {goal.Description}".PadRight(width - 12).Substring(0, width - 12) + progressBar.PadLeft(10) + "║");
            }
            lines.Add("║" + new string(' ', width - 2) + "║");
        }
        
        if (achievementGoals.Any())
        {
            lines.Add("║" + " 🏆 Achievements ".PadRight(width - 2) + "║");
            foreach (var goal in achievementGoals.Take(3))
            {
                string progressBar = $"[{goal.Progress}/{goal.Target}]";
                lines.Add("║" + $"   • {goal.Name}: {goal.Description}".PadRight(width - 12).Substring(0, width - 12) + progressBar.PadLeft(10) + "║");
            }
        }
        
        lines.Add("╠" + new string('─', width - 2) + "╣");
        lines.Add("║" + $" Completed: {_completedGoals.Count} goals ".PadRight(width - 2) + "║");
        lines.Add("╚" + new string('═', width - 2) + "╝");
        
        return lines;
    }
    
    /// <summary>
    /// Convert to save data.
    /// </summary>
    public Dictionary<string, object?> ToSaveData()
    {
        return new Dictionary<string, object?>
        {
            ["active_goals"] = _activeGoals.Select(g => new Dictionary<string, object?>
            {
                ["id"] = g.Id,
                ["name"] = g.Name,
                ["description"] = g.Description,
                ["goal_type"] = g.GoalType,
                ["action"] = g.Action,
                ["target"] = g.Target,
                ["progress"] = g.Progress,
                ["completed"] = g.Completed,
                ["reward_item"] = g.RewardItem,
                ["reward_message"] = g.RewardMessage,
                ["hidden"] = g.Hidden
            }).ToList(),
            ["completed_goals"] = _completedGoals,
            ["last_daily_reset"] = _lastDailyReset,
            ["last_weekly_reset"] = _lastWeeklyReset
        };
    }
    
    /// <summary>
    /// Load from save data.
    /// </summary>
    public static GoalSystem FromSaveData(Dictionary<string, JsonElement> data)
    {
        var system = new GoalSystem();
        
        if (data.TryGetValue("completed_goals", out var compEl) && compEl.ValueKind == JsonValueKind.Array)
            system._completedGoals = compEl.EnumerateArray().Select(e => e.GetString() ?? "").ToList();
        
        if (data.TryGetValue("last_daily_reset", out var dailyEl) && dailyEl.ValueKind == JsonValueKind.String)
            system._lastDailyReset = dailyEl.GetString();
        
        if (data.TryGetValue("last_weekly_reset", out var weeklyEl) && weeklyEl.ValueKind == JsonValueKind.String)
            system._lastWeeklyReset = weeklyEl.GetString();
        
        if (data.TryGetValue("active_goals", out var goalsEl) && goalsEl.ValueKind == JsonValueKind.Array)
        {
            foreach (var gEl in goalsEl.EnumerateArray())
            {
                var goal = new Goal
                {
                    Id = gEl.TryGetProperty("id", out var idEl) ? idEl.GetString() ?? "" : "",
                    Name = gEl.TryGetProperty("name", out var nameEl) ? nameEl.GetString() ?? "" : "",
                    Description = gEl.TryGetProperty("description", out var descEl) ? descEl.GetString() ?? "" : "",
                    GoalType = gEl.TryGetProperty("goal_type", out var typeEl) ? typeEl.GetString() ?? "" : "",
                    Action = gEl.TryGetProperty("action", out var actEl) ? actEl.GetString() ?? "" : "",
                    Target = gEl.TryGetProperty("target", out var targEl) ? targEl.GetInt32() : 1,
                    Progress = gEl.TryGetProperty("progress", out var progEl) ? progEl.GetInt32() : 0,
                    Completed = gEl.TryGetProperty("completed", out var compGoalEl) && compGoalEl.GetBoolean(),
                    RewardItem = gEl.TryGetProperty("reward_item", out var rewEl) && rewEl.ValueKind == JsonValueKind.String ? rewEl.GetString() : null,
                    RewardMessage = gEl.TryGetProperty("reward_message", out var rmEl) ? rmEl.GetString() ?? "" : "",
                    Hidden = gEl.TryGetProperty("hidden", out var hidEl) && hidEl.GetBoolean()
                };
                system._activeGoals.Add(goal);
            }
        }
        
        return system;
    }
}
