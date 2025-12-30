using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;

namespace StupidDuck.World;

/// <summary>
/// Types of challenges
/// </summary>
public enum ChallengeType
{
    Daily,
    Weekly,
    Special,
    Seasonal
}

/// <summary>
/// Challenge difficulty levels
/// </summary>
public enum ChallengeDifficulty
{
    Easy,
    Medium,
    Hard,
    Extreme
}

/// <summary>
/// A challenge definition template
/// </summary>
public class ChallengeDefinition
{
    public string Id { get; set; } = "";
    public string Name { get; set; } = "";
    public string Description { get; set; } = "";
    public ChallengeType Type { get; set; }
    public ChallengeDifficulty Difficulty { get; set; }
    public string GoalType { get; set; } = "";
    public int GoalAmount { get; set; } = 0;
    public int XpReward { get; set; } = 0;
    public int CoinReward { get; set; } = 0;
    public string? BonusItem { get; set; } = null;
    public int? TimeLimitHours { get; set; } = null;
}

/// <summary>
/// An active challenge being tracked
/// </summary>
public class ActiveChallenge
{
    public string ChallengeId { get; set; } = "";
    public DateTime StartedAt { get; set; } = DateTime.Now;
    public DateTime ExpiresAt { get; set; } = DateTime.Now;
    public int CurrentProgress { get; set; } = 0;
    public int GoalAmount { get; set; } = 0;
    public bool Completed { get; set; } = false;
    public bool Claimed { get; set; } = false;
}

/// <summary>
/// Challenge system - daily and weekly challenges with rewards
/// </summary>
public class ChallengeSystem
{
    private static readonly Random _random = new();

    // Daily challenge definitions
    private static readonly Dictionary<string, ChallengeDefinition> _dailyChallenges = new()
    {
        // Easy
        ["feed_5"] = new ChallengeDefinition
        {
            Id = "feed_5", Name = "Snack Time",
            Description = "Feed your duck 5 times",
            Type = ChallengeType.Daily, Difficulty = ChallengeDifficulty.Easy,
            GoalType = "feed", GoalAmount = 5,
            XpReward = 25, CoinReward = 15
        },
        ["play_3"] = new ChallengeDefinition
        {
            Id = "play_3", Name = "Playtime!",
            Description = "Play with your duck 3 times",
            Type = ChallengeType.Daily, Difficulty = ChallengeDifficulty.Easy,
            GoalType = "play", GoalAmount = 3,
            XpReward = 20, CoinReward = 10
        },
        ["pet_5"] = new ChallengeDefinition
        {
            Id = "pet_5", Name = "Cuddle Time",
            Description = "Pet your duck 5 times",
            Type = ChallengeType.Daily, Difficulty = ChallengeDifficulty.Easy,
            GoalType = "pet", GoalAmount = 5,
            XpReward = 20, CoinReward = 10
        },
        ["talk_3"] = new ChallengeDefinition
        {
            Id = "talk_3", Name = "Chit Chat",
            Description = "Talk to your duck 3 times",
            Type = ChallengeType.Daily, Difficulty = ChallengeDifficulty.Easy,
            GoalType = "talk", GoalAmount = 3,
            XpReward = 15, CoinReward = 10
        },
        // Medium
        ["feed_10"] = new ChallengeDefinition
        {
            Id = "feed_10", Name = "Feast Day",
            Description = "Feed your duck 10 times",
            Type = ChallengeType.Daily, Difficulty = ChallengeDifficulty.Medium,
            GoalType = "feed", GoalAmount = 10,
            XpReward = 50, CoinReward = 30
        },
        ["explore_2"] = new ChallengeDefinition
        {
            Id = "explore_2", Name = "Explorer",
            Description = "Explore 2 different areas",
            Type = ChallengeType.Daily, Difficulty = ChallengeDifficulty.Medium,
            GoalType = "explore", GoalAmount = 2,
            XpReward = 40, CoinReward = 25
        },
        ["minigame_3"] = new ChallengeDefinition
        {
            Id = "minigame_3", Name = "Gamer Duck",
            Description = "Play 3 mini-games",
            Type = ChallengeType.Daily, Difficulty = ChallengeDifficulty.Medium,
            GoalType = "minigame", GoalAmount = 3,
            XpReward = 45, CoinReward = 30
        },
        ["happy_mood"] = new ChallengeDefinition
        {
            Id = "happy_mood", Name = "Keep Smiling",
            Description = "Keep duck happy for 30 minutes",
            Type = ChallengeType.Daily, Difficulty = ChallengeDifficulty.Medium,
            GoalType = "happy_time", GoalAmount = 30,
            XpReward = 60, CoinReward = 40
        },
        // Hard
        ["perfect_care"] = new ChallengeDefinition
        {
            Id = "perfect_care", Name = "Perfect Caretaker",
            Description = "Keep all needs above 80% for 1 hour",
            Type = ChallengeType.Daily, Difficulty = ChallengeDifficulty.Hard,
            GoalType = "perfect_care", GoalAmount = 60,
            XpReward = 100, CoinReward = 75,
            BonusItem = "rare_treat"
        },
        ["all_activities"] = new ChallengeDefinition
        {
            Id = "all_activities", Name = "Variety Day",
            Description = "Do all 5 activity types today",
            Type = ChallengeType.Daily, Difficulty = ChallengeDifficulty.Hard,
            GoalType = "activity_variety", GoalAmount = 5,
            XpReward = 80, CoinReward = 60
        }
    };

    // Weekly challenge definitions
    private static readonly Dictionary<string, ChallengeDefinition> _weeklyChallenges = new()
    {
        ["weekly_feed_50"] = new ChallengeDefinition
        {
            Id = "weekly_feed_50", Name = "Weekly Feast",
            Description = "Feed your duck 50 times this week",
            Type = ChallengeType.Weekly, Difficulty = ChallengeDifficulty.Medium,
            GoalType = "feed", GoalAmount = 50,
            XpReward = 200, CoinReward = 150
        },
        ["weekly_play_25"] = new ChallengeDefinition
        {
            Id = "weekly_play_25", Name = "Playful Week",
            Description = "Play 25 times this week",
            Type = ChallengeType.Weekly, Difficulty = ChallengeDifficulty.Medium,
            GoalType = "play", GoalAmount = 25,
            XpReward = 175, CoinReward = 125
        },
        ["weekly_login_7"] = new ChallengeDefinition
        {
            Id = "weekly_login_7", Name = "Dedicated",
            Description = "Log in every day this week",
            Type = ChallengeType.Weekly, Difficulty = ChallengeDifficulty.Medium,
            GoalType = "login", GoalAmount = 7,
            XpReward = 250, CoinReward = 200,
            BonusItem = "weekly_chest"
        },
        ["weekly_explore_10"] = new ChallengeDefinition
        {
            Id = "weekly_explore_10", Name = "Grand Explorer",
            Description = "Complete 10 explorations this week",
            Type = ChallengeType.Weekly, Difficulty = ChallengeDifficulty.Hard,
            GoalType = "explore", GoalAmount = 10,
            XpReward = 300, CoinReward = 250,
            BonusItem = "explorer_badge"
        },
        ["weekly_minigame_20"] = new ChallengeDefinition
        {
            Id = "weekly_minigame_20", Name = "Mini-Game Master",
            Description = "Play 20 mini-games this week",
            Type = ChallengeType.Weekly, Difficulty = ChallengeDifficulty.Hard,
            GoalType = "minigame", GoalAmount = 20,
            XpReward = 350, CoinReward = 275
        },
        ["weekly_master"] = new ChallengeDefinition
        {
            Id = "weekly_master", Name = "Master Caretaker",
            Description = "Complete all other weekly challenges",
            Type = ChallengeType.Weekly, Difficulty = ChallengeDifficulty.Extreme,
            GoalType = "complete_weekly", GoalAmount = 4,
            XpReward = 500, CoinReward = 400,
            BonusItem = "master_trophy"
        }
    };

    // Special challenge definitions
    private static readonly Dictionary<string, ChallengeDefinition> _specialChallenges = new()
    {
        ["first_rainbow"] = new ChallengeDefinition
        {
            Id = "first_rainbow", Name = "Rainbow Hunter",
            Description = "Experience a rainbow event",
            Type = ChallengeType.Special, Difficulty = ChallengeDifficulty.Medium,
            GoalType = "see_rainbow", GoalAmount = 1,
            XpReward = 100, CoinReward = 100,
            BonusItem = "rainbow_charm"
        },
        ["catch_legendary"] = new ChallengeDefinition
        {
            Id = "catch_legendary", Name = "Legend Fisher",
            Description = "Catch a legendary fish",
            Type = ChallengeType.Special, Difficulty = ChallengeDifficulty.Extreme,
            GoalType = "catch_legendary_fish", GoalAmount = 1,
            XpReward = 500, CoinReward = 500,
            BonusItem = "legendary_trophy"
        },
        ["grow_golden"] = new ChallengeDefinition
        {
            Id = "grow_golden", Name = "Golden Gardener",
            Description = "Grow a golden flower",
            Type = ChallengeType.Special, Difficulty = ChallengeDifficulty.Hard,
            GoalType = "grow_golden_flower", GoalAmount = 1,
            XpReward = 300, CoinReward = 300,
            BonusItem = "golden_badge"
        }
    };

    // Instance state
    public List<ActiveChallenge> ActiveDaily { get; private set; } = new();
    public List<ActiveChallenge> ActiveWeekly { get; private set; } = new();
    public List<ActiveChallenge> ActiveSpecial { get; private set; } = new();
    public Dictionary<string, int> CompletedChallenges { get; private set; } = new();
    public string DailyRefreshDate { get; private set; } = "";
    public string WeeklyRefreshDate { get; private set; } = "";
    public int ChallengeStreak { get; private set; } = 0;
    public string LastCompleteDate { get; private set; } = "";
    public int TotalChallengesCompleted { get; private set; } = 0;
    public Dictionary<string, int> TotalRewardsEarned { get; private set; } = new() { ["xp"] = 0, ["coins"] = 0 };

    public ChallengeSystem()
    {
    }

    /// <summary>
    /// Refresh daily challenges if needed
    /// </summary>
    public bool RefreshDailyChallenges(bool force = false)
    {
        string today = DateTime.Now.ToString("yyyy-MM-dd");

        if (DailyRefreshDate == today && !force)
        {
            return false;
        }

        // Select 3 random daily challenges
        var challengePool = _dailyChallenges.Values.ToList();
        var selected = challengePool.OrderBy(_ => _random.Next()).Take(Math.Min(3, challengePool.Count)).ToList();

        var now = DateTime.Now;
        var tomorrow = now.Date.AddDays(1);

        ActiveDaily = selected.Select(c => new ActiveChallenge
        {
            ChallengeId = c.Id,
            StartedAt = now,
            ExpiresAt = tomorrow,
            CurrentProgress = 0,
            GoalAmount = c.GoalAmount
        }).ToList();

        DailyRefreshDate = today;
        return true;
    }

    /// <summary>
    /// Refresh weekly challenges if needed
    /// </summary>
    public bool RefreshWeeklyChallenges(bool force = false)
    {
        var today = DateTime.Now;
        var weekNum = System.Globalization.ISOWeek.GetWeekOfYear(today);
        var weekKey = $"{today.Year}-W{weekNum}";

        if (WeeklyRefreshDate == weekKey && !force)
        {
            return false;
        }

        // Select 4 weekly challenges
        var challengePool = _weeklyChallenges.Values.ToList();
        var selected = challengePool.OrderBy(_ => _random.Next()).Take(Math.Min(4, challengePool.Count)).ToList();

        // Calculate end of week (next Monday)
        int daysUntilMonday = ((int)DayOfWeek.Monday - (int)today.DayOfWeek + 7) % 7;
        if (daysUntilMonday == 0) daysUntilMonday = 7;
        var nextMonday = today.Date.AddDays(daysUntilMonday);

        ActiveWeekly = selected.Select(c => new ActiveChallenge
        {
            ChallengeId = c.Id,
            StartedAt = today,
            ExpiresAt = nextMonday,
            CurrentProgress = 0,
            GoalAmount = c.GoalAmount
        }).ToList();

        WeeklyRefreshDate = weekKey;
        return true;
    }

    /// <summary>
    /// Update progress on challenges matching the goal type
    /// </summary>
    public List<(string challengeId, bool completed)> UpdateProgress(string goalType, int amount = 1)
    {
        var updates = new List<(string, bool)>();

        var allChallenges = ActiveDaily.Concat(ActiveWeekly).Concat(ActiveSpecial);

        foreach (var challenge in allChallenges)
        {
            if (challenge.Completed)
                continue;

            var definition = GetDefinition(challenge.ChallengeId);
            if (definition == null)
                continue;

            if (definition.GoalType == goalType)
            {
                challenge.CurrentProgress = Math.Min(
                    challenge.CurrentProgress + amount,
                    challenge.GoalAmount
                );

                if (challenge.CurrentProgress >= challenge.GoalAmount)
                {
                    challenge.Completed = true;
                    updates.Add((challenge.ChallengeId, true));
                }
                else
                {
                    updates.Add((challenge.ChallengeId, false));
                }
            }
        }

        return updates;
    }

    /// <summary>
    /// Claim reward for a completed challenge
    /// </summary>
    public (bool success, string message, Dictionary<string, object> rewards) ClaimReward(string challengeId)
    {
        var challenge = FindChallenge(challengeId);
        if (challenge == null)
        {
            return (false, "Challenge not found!", new Dictionary<string, object>());
        }

        if (!challenge.Completed)
        {
            return (false, "Challenge not completed yet!", new Dictionary<string, object>());
        }

        if (challenge.Claimed)
        {
            return (false, "Reward already claimed!", new Dictionary<string, object>());
        }

        var definition = GetDefinition(challengeId);
        if (definition == null)
        {
            return (false, "Challenge definition not found!", new Dictionary<string, object>());
        }

        // Mark as claimed
        challenge.Claimed = true;

        // Update stats
        TotalChallengesCompleted++;
        CompletedChallenges[challengeId] = CompletedChallenges.GetValueOrDefault(challengeId, 0) + 1;
        TotalRewardsEarned["xp"] += definition.XpReward;
        TotalRewardsEarned["coins"] += definition.CoinReward;

        // Update streak
        string today = DateTime.Now.ToString("yyyy-MM-dd");
        if (LastCompleteDate != today)
        {
            string yesterday = DateTime.Now.AddDays(-1).ToString("yyyy-MM-dd");
            if (LastCompleteDate == yesterday)
            {
                ChallengeStreak++;
            }
            else
            {
                ChallengeStreak = 1;
            }
            LastCompleteDate = today;
        }

        // Calculate streak bonus (up to 50%)
        double streakBonus = Math.Min(ChallengeStreak * 0.1, 0.5);
        int bonusXp = (int)(definition.XpReward * streakBonus);
        int bonusCoins = (int)(definition.CoinReward * streakBonus);

        var rewards = new Dictionary<string, object>
        {
            ["xp"] = definition.XpReward + bonusXp,
            ["coins"] = definition.CoinReward + bonusCoins,
            ["streak_bonus"] = streakBonus,
            ["item"] = definition.BonusItem ?? ""
        };

        return (true, $"🎉 Challenge Complete! +{rewards["xp"]} XP, +{rewards["coins"]} coins!", rewards);
    }

    /// <summary>
    /// Find an active challenge by ID
    /// </summary>
    private ActiveChallenge? FindChallenge(string challengeId)
    {
        return ActiveDaily.Concat(ActiveWeekly).Concat(ActiveSpecial)
            .FirstOrDefault(c => c.ChallengeId == challengeId);
    }

    /// <summary>
    /// Get challenge definition by ID
    /// </summary>
    public ChallengeDefinition? GetDefinition(string challengeId)
    {
        if (_dailyChallenges.TryGetValue(challengeId, out var daily))
            return daily;
        if (_weeklyChallenges.TryGetValue(challengeId, out var weekly))
            return weekly;
        if (_specialChallenges.TryGetValue(challengeId, out var special))
            return special;
        return null;
    }

    /// <summary>
    /// Add a special/seasonal challenge
    /// </summary>
    public void AddSpecialChallenge(string challengeId, int durationHours = 24)
    {
        if (!_specialChallenges.TryGetValue(challengeId, out var definition))
            return;

        var now = DateTime.Now;
        var expires = now.AddHours(durationHours);

        ActiveSpecial.Add(new ActiveChallenge
        {
            ChallengeId = challengeId,
            StartedAt = now,
            ExpiresAt = expires,
            CurrentProgress = 0,
            GoalAmount = definition.GoalAmount
        });
    }

    /// <summary>
    /// Get daily progress summary
    /// </summary>
    public Dictionary<string, object> GetDailyProgress()
    {
        int completed = ActiveDaily.Count(c => c.Completed);

        return new Dictionary<string, object>
        {
            ["completed"] = completed,
            ["total"] = ActiveDaily.Count,
            ["challenges"] = ActiveDaily.Select(c => new Dictionary<string, object>
            {
                ["id"] = c.ChallengeId,
                ["progress"] = c.CurrentProgress,
                ["goal"] = c.GoalAmount,
                ["completed"] = c.Completed,
                ["claimed"] = c.Claimed
            }).ToList()
        };
    }

    /// <summary>
    /// Render challenges display
    /// </summary>
    public List<string> RenderChallenges()
    {
        var lines = new List<string>
        {
            "╔═══════════════════════════════════════════════╗",
            "║          📋 CHALLENGES 📋                     ║",
            $"║  Streak: {ChallengeStreak} days 🔥                          ║",
            "╠═══════════════════════════════════════════════╣",
            "║  📅 DAILY CHALLENGES:                         ║"
        };

        foreach (var challenge in ActiveDaily)
        {
            var definition = GetDefinition(challenge.ChallengeId);
            if (definition != null)
            {
                string status = challenge.Completed ? "✅" : $"{challenge.CurrentProgress}/{challenge.GoalAmount}";
                string claimed = challenge.Claimed ? " 🎁" : "";
                string name = definition.Name.Length > 20 ? definition.Name[..20] : definition.Name;
                lines.Add($"║   {status} {name,-20}{claimed}    ║");
            }
        }

        lines.Add("╠═══════════════════════════════════════════════╣");
        lines.Add("║  📆 WEEKLY CHALLENGES:                        ║");

        foreach (var challenge in ActiveWeekly)
        {
            var definition = GetDefinition(challenge.ChallengeId);
            if (definition != null)
            {
                string status = challenge.Completed ? "✅" : $"{challenge.CurrentProgress}/{challenge.GoalAmount}";
                string claimed = challenge.Claimed ? " 🎁" : "";
                string name = definition.Name.Length > 20 ? definition.Name[..20] : definition.Name;
                lines.Add($"║   {status} {name,-20}{claimed}    ║");
            }
        }

        if (ActiveSpecial.Any())
        {
            lines.Add("╠═══════════════════════════════════════════════╣");
            lines.Add("║  ⭐ SPECIAL CHALLENGES:                       ║");
            foreach (var challenge in ActiveSpecial)
            {
                var definition = GetDefinition(challenge.ChallengeId);
                if (definition != null)
                {
                    string status = challenge.Completed ? "✅" : $"{challenge.CurrentProgress}/{challenge.GoalAmount}";
                    string name = definition.Name.Length > 20 ? definition.Name[..20] : definition.Name;
                    lines.Add($"║   {status} {name,-20}        ║");
                }
            }
        }

        lines.Add("╠═══════════════════════════════════════════════╣");
        lines.Add($"║  Total Completed: {TotalChallengesCompleted,5}                      ║");
        lines.Add("╚═══════════════════════════════════════════════╝");

        return lines;
    }

    /// <summary>
    /// Convert to save data
    /// </summary>
    public Dictionary<string, object> ToSaveData()
    {
        Func<ActiveChallenge, Dictionary<string, object>> serializeChallenge = c => new Dictionary<string, object>
        {
            ["challenge_id"] = c.ChallengeId,
            ["started_at"] = c.StartedAt.ToString("o"),
            ["expires_at"] = c.ExpiresAt.ToString("o"),
            ["current_progress"] = c.CurrentProgress,
            ["goal_amount"] = c.GoalAmount,
            ["completed"] = c.Completed,
            ["claimed"] = c.Claimed
        };

        return new Dictionary<string, object>
        {
            ["active_daily"] = ActiveDaily.Select(serializeChallenge).ToList(),
            ["active_weekly"] = ActiveWeekly.Select(serializeChallenge).ToList(),
            ["active_special"] = ActiveSpecial.Select(serializeChallenge).ToList(),
            ["completed_challenges"] = CompletedChallenges,
            ["daily_refresh_date"] = DailyRefreshDate,
            ["weekly_refresh_date"] = WeeklyRefreshDate,
            ["challenge_streak"] = ChallengeStreak,
            ["last_complete_date"] = LastCompleteDate,
            ["total_challenges_completed"] = TotalChallengesCompleted,
            ["total_rewards_earned"] = TotalRewardsEarned
        };
    }

    /// <summary>
    /// Load from save data
    /// </summary>
    public static ChallengeSystem FromSaveData(Dictionary<string, object> data)
    {
        var system = new ChallengeSystem();

        Func<JsonElement, ActiveChallenge> deserializeChallenge = elem => new ActiveChallenge
        {
            ChallengeId = elem.GetProperty("challenge_id").GetString() ?? "",
            StartedAt = DateTime.Parse(elem.GetProperty("started_at").GetString() ?? DateTime.Now.ToString()),
            ExpiresAt = DateTime.Parse(elem.GetProperty("expires_at").GetString() ?? DateTime.Now.ToString()),
            CurrentProgress = elem.GetProperty("current_progress").GetInt32(),
            GoalAmount = elem.GetProperty("goal_amount").GetInt32(),
            Completed = elem.TryGetProperty("completed", out var comp) && comp.GetBoolean(),
            Claimed = elem.TryGetProperty("claimed", out var claim) && claim.GetBoolean()
        };

        if (data.TryGetValue("active_daily", out var dailyObj) && dailyObj is JsonElement dailyElem)
        {
            system.ActiveDaily = dailyElem.EnumerateArray().Select(deserializeChallenge).ToList();
        }

        if (data.TryGetValue("active_weekly", out var weeklyObj) && weeklyObj is JsonElement weeklyElem)
        {
            system.ActiveWeekly = weeklyElem.EnumerateArray().Select(deserializeChallenge).ToList();
        }

        if (data.TryGetValue("active_special", out var specialObj) && specialObj is JsonElement specialElem)
        {
            system.ActiveSpecial = specialElem.EnumerateArray().Select(deserializeChallenge).ToList();
        }

        if (data.TryGetValue("completed_challenges", out var compObj) && compObj is JsonElement compElem)
        {
            foreach (var prop in compElem.EnumerateObject())
            {
                system.CompletedChallenges[prop.Name] = prop.Value.GetInt32();
            }
        }

        system.DailyRefreshDate = data.GetValueOrDefault("daily_refresh_date")?.ToString() ?? "";
        system.WeeklyRefreshDate = data.GetValueOrDefault("weekly_refresh_date")?.ToString() ?? "";
        system.ChallengeStreak = Convert.ToInt32(data.GetValueOrDefault("challenge_streak", 0));
        system.LastCompleteDate = data.GetValueOrDefault("last_complete_date")?.ToString() ?? "";
        system.TotalChallengesCompleted = Convert.ToInt32(data.GetValueOrDefault("total_challenges_completed", 0));

        if (data.TryGetValue("total_rewards_earned", out var rewardsObj) && rewardsObj is JsonElement rewardsElem)
        {
            system.TotalRewardsEarned["xp"] = rewardsElem.TryGetProperty("xp", out var xp) ? xp.GetInt32() : 0;
            system.TotalRewardsEarned["coins"] = rewardsElem.TryGetProperty("coins", out var coins) ? coins.GetInt32() : 0;
        }

        return system;
    }
}
