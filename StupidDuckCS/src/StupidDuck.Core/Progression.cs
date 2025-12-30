using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json.Serialization;

namespace StupidDuck.Core;

/// <summary>
/// Types of rewards players can earn.
/// </summary>
public enum RewardType
{
    Item,
    XP,
    Currency,
    Collectible,
    Cosmetic,
    Title,
    Unlock
}

/// <summary>
/// A reward that can be earned.
/// </summary>
public class Reward
{
    public RewardType Type { get; set; }
    public string Value { get; set; } = "";
    public int Amount { get; set; } = 1;
    public string Description { get; set; } = "";
    public bool IsRare { get; set; }

    public Reward() { }

    public Reward(RewardType type, string value, int amount = 1, string description = "", bool isRare = false)
    {
        Type = type;
        Value = value;
        Amount = amount;
        Description = description;
        IsRare = isRare;
    }
}

/// <summary>
/// A daily challenge/task.
/// </summary>
public class DailyChallenge
{
    public string Id { get; set; } = "";
    public string Name { get; set; } = "";
    public string Description { get; set; } = "";
    public int Target { get; set; }
    public int Progress { get; set; }
    public Reward? Reward { get; set; }
    public DateTime? Expires { get; set; }

    public bool IsComplete => Progress >= Target;
    public float ProgressPercent => Target > 0 ? (float)Progress / Target * 100 : 0;
}

/// <summary>
/// Collectible item data.
/// </summary>
public class CollectibleItem
{
    public string Id { get; set; } = "";
    public string Name { get; set; } = "";
    public string Rarity { get; set; } = "common";
    public string Description { get; set; } = "";
}

/// <summary>
/// Collectible category.
/// </summary>
public class CollectibleCategory
{
    public string Name { get; set; } = "";
    public string Description { get; set; } = "";
    public Dictionary<string, CollectibleItem> Items { get; set; } = new();
}

/// <summary>
/// Progression and engagement mechanics - The Sims/Animal Crossing style.
/// Implements: XP, levels, streaks, daily rewards, collectibles, milestones.
/// </summary>
public class ProgressionSystem
{
    // =============================================================================
    // STREAK MULTIPLIER SYSTEM
    // =============================================================================
    
    private static readonly Dictionary<int, float> StreakXPMultipliers = new()
    {
        { 1, 1.0f },     // Day 1: Normal XP
        { 3, 1.1f },     // 3+ days: 10% bonus
        { 7, 1.25f },    // Week+: 25% bonus
        { 14, 1.5f },    // 2 weeks+: 50% bonus
        { 30, 2.0f },    // Month+: Double XP!
        { 60, 2.5f },    // 2 months+: 2.5x
        { 100, 3.0f },   // 100+ days: Triple XP!
    };

    private static readonly string[] StreakLossMessages = 
    {
        "Oh no! Cheese missed you... Your {0}-day streak ended. 😢",
        "Cheese waited all day yesterday... The {0}-day streak is broken.",
        "The {0}-day streak has ended, but Cheese is happy you're back!",
        "Your {0}-day streak ended... but every journey starts fresh!",
        "Cheese: 'I counted {0} days... where did you go?' 🥺",
    };

    private static readonly Dictionary<int, string> StreakCelebrationMessages = new()
    {
        { 3, "3 days! Cheese is starting to recognize you! 🌟" },
        { 7, "🎉 ONE WEEK STREAK! Cheese does a happy dance! 🦆💃" },
        { 14, "✨ TWO WEEKS! You and Cheese are becoming best friends!" },
        { 21, "🌈 THREE WEEKS! Cheese gave you a special feather!" },
        { 30, "🎊 ONE MONTH! WOW! Cheese is SO HAPPY! 🦆❤️ DOUBLE XP UNLOCKED!" },
        { 50, "⭐ FIFTY DAYS! Cheese made you a tiny crown! 👑" },
        { 100, "🏆 ONE HUNDRED DAYS! LEGENDARY! Cheese will remember this forever! ✨" },
        { 365, "🎆 ONE YEAR WITH CHEESE! Eternal bond formed! 🦆💕" },
    };

    // =============================================================================
    // TIME-BASED BONUSES
    // =============================================================================

    private static readonly Dictionary<string, (int Start, int End, float Mult, string Message)> TimeBonuses = new()
    {
        { "morning", (6, 9, 1.2f, "🌅 Early bird bonus! +20% XP") },
        { "lunch", (12, 13, 1.15f, "☀️ Lunch break bonus! +15% XP") },
        { "evening", (18, 21, 1.25f, "🌆 Evening chill bonus! +25% XP") },
        { "night_owl", (23, 24, 1.3f, "🦉 Night owl bonus! +30% XP") },
        { "midnight", (0, 2, 1.5f, "🌙 Midnight dedication! +50% XP") },
    };

    // =============================================================================
    // LEVEL TITLES
    // =============================================================================

    private static readonly Dictionary<int, string> LevelTitles = new()
    {
        { 1, "Duckling Watcher" },
        { 5, "Duck Friend" },
        { 10, "Duck Buddy" },
        { 15, "Duck Companion" },
        { 20, "Duck Guardian" },
        { 25, "Duck Whisperer" },
        { 30, "Duck Master" },
        { 40, "Duck Sage" },
        { 50, "Legendary Duck Keeper" },
        { 75, "Eternal Duck Bond" },
        { 100, "One With The Duck" },
    };

    // =============================================================================
    // COLLECTIBLES
    // =============================================================================

    public static readonly Dictionary<string, CollectibleCategory> Collectibles = new()
    {
        ["feathers"] = new CollectibleCategory
        {
            Name = "Feather Collection",
            Description = "Rare feathers shed by Cheese",
            Items = new Dictionary<string, CollectibleItem>
            {
                ["white_feather"] = new() { Id = "white_feather", Name = "White Feather", Rarity = "common", Description = "A soft white feather" },
                ["golden_feather"] = new() { Id = "golden_feather", Name = "Golden Feather", Rarity = "legendary", Description = "Shimmers with mysterious light" },
                ["rainbow_feather"] = new() { Id = "rainbow_feather", Name = "Rainbow Feather", Rarity = "legendary", Description = "Changes color in the light" },
                ["fluffy_down"] = new() { Id = "fluffy_down", Name = "Fluffy Down", Rarity = "common", Description = "Extra soft and warm" },
                ["spotted_feather"] = new() { Id = "spotted_feather", Name = "Spotted Feather", Rarity = "uncommon", Description = "Unique spotted pattern" },
                ["iridescent_feather"] = new() { Id = "iridescent_feather", Name = "Iridescent Feather", Rarity = "rare", Description = "Gleams with oil-slick colors" },
                ["ancient_feather"] = new() { Id = "ancient_feather", Name = "Ancient Feather", Rarity = "legendary", Description = "From the First Duck..." },
            }
        },
        ["badges"] = new CollectibleCategory
        {
            Name = "Badge Collection",
            Description = "Achievements and honors",
            Items = new Dictionary<string, CollectibleItem>
            {
                ["first_friend"] = new() { Id = "first_friend", Name = "First Friend Badge", Rarity = "common", Description = "Made a friend!" },
                ["best_buddy"] = new() { Id = "best_buddy", Name = "Best Buddy Badge", Rarity = "rare", Description = "Reached max friendship" },
                ["bread_master"] = new() { Id = "bread_master", Name = "Bread Master Badge", Rarity = "uncommon", Description = "Fed 100 pieces of bread" },
                ["early_bird"] = new() { Id = "early_bird", Name = "Early Bird Badge", Rarity = "uncommon", Description = "Played at dawn" },
                ["night_owl"] = new() { Id = "night_owl", Name = "Night Owl Badge", Rarity = "uncommon", Description = "Played at midnight" },
                ["dedication"] = new() { Id = "dedication", Name = "Dedication Badge", Rarity = "rare", Description = "30 day streak" },
                ["legendary_keeper"] = new() { Id = "legendary_keeper", Name = "Legendary Keeper", Rarity = "legendary", Description = "100% completion" },
            }
        },
        ["photos"] = new CollectibleCategory
        {
            Name = "Photo Album",
            Description = "Memorable moments captured",
            Items = new Dictionary<string, CollectibleItem>
            {
                ["first_meeting"] = new() { Id = "first_meeting", Name = "First Meeting", Rarity = "common", Description = "The day we met" },
                ["first_bath"] = new() { Id = "first_bath", Name = "Splish Splash", Rarity = "common", Description = "First bath time" },
                ["sleeping_duck"] = new() { Id = "sleeping_duck", Name = "Sleepy Time", Rarity = "common", Description = "Peaceful napping" },
                ["happy_dance"] = new() { Id = "happy_dance", Name = "Happy Dance", Rarity = "uncommon", Description = "Pure joy captured" },
                ["holiday_photo"] = new() { Id = "holiday_photo", Name = "Holiday Memory", Rarity = "rare", Description = "Special holiday moment" },
                ["evolution"] = new() { Id = "evolution", Name = "Growing Up", Rarity = "rare", Description = "Growth milestone" },
                ["best_friends"] = new() { Id = "best_friends", Name = "Best Friends Forever", Rarity = "legendary", Description = "Maximum bond achieved" },
            }
        },
        ["treasures"] = new CollectibleCategory
        {
            Name = "Duck Treasures",
            Description = "Shiny things Cheese found",
            Items = new Dictionary<string, CollectibleItem>
            {
                ["shiny_coin"] = new() { Id = "shiny_coin", Name = "Shiny Coin", Rarity = "common", Description = "Ooh, shiny!" },
                ["pretty_rock"] = new() { Id = "pretty_rock", Name = "Pretty Rock", Rarity = "common", Description = "It's a really nice rock" },
                ["lost_button"] = new() { Id = "lost_button", Name = "Lost Button", Rarity = "common", Description = "Someone's missing this" },
                ["glass_marble"] = new() { Id = "glass_marble", Name = "Glass Marble", Rarity = "uncommon", Description = "Swirly colors inside" },
                ["old_key"] = new() { Id = "old_key", Name = "Mysterious Key", Rarity = "rare", Description = "What does it unlock?" },
                ["crystal_shard"] = new() { Id = "crystal_shard", Name = "Crystal Shard", Rarity = "rare", Description = "Sparkles in sunlight" },
                ["ancient_artifact"] = new() { Id = "ancient_artifact", Name = "Ancient Artifact", Rarity = "legendary", Description = "From a forgotten time" },
            }
        }
    };

    // =============================================================================
    // DAILY REWARDS
    // =============================================================================

    private static readonly List<Reward>[] DailyRewards =
    {
        // Day 1
        new List<Reward> { new(RewardType.Item, "bread", 2), new(RewardType.XP, "10") },
        // Day 2
        new List<Reward> { new(RewardType.Item, "seeds", 2), new(RewardType.XP, "15") },
        // Day 3
        new List<Reward> { new(RewardType.Item, "lettuce"), new(RewardType.XP, "20") },
        // Day 4
        new List<Reward> { new(RewardType.Item, "corn", 2), new(RewardType.XP, "25") },
        // Day 5
        new List<Reward> { new(RewardType.Item, "worm"), new(RewardType.XP, "30") },
        // Day 6
        new List<Reward> { new(RewardType.Item, "grapes"), new(RewardType.XP, "35") },
        // Day 7 (weekly bonus!)
        new List<Reward> 
        { 
            new(RewardType.Item, "fancy_bread"), 
            new(RewardType.XP, "100"),
            new(RewardType.Collectible, "treasures:shiny_coin")
        },
    };

    // =============================================================================
    // STATE
    // =============================================================================

    // XP and Level
    public int XP { get; set; }
    public int Level { get; set; } = 1;
    public string Title { get; set; } = "Duckling Watcher";

    // Streaks
    public int CurrentStreak { get; set; }
    public int LongestStreak { get; set; }
    public string? LastLoginDate { get; set; }
    public bool DailyRewardClaimed { get; set; }
    public int DaysPlayed { get; set; }

    // Enhanced streak tracking
    public bool StreakLostToday { get; set; }
    public int PreviousStreak { get; set; }
    public int DaysSinceStreakLoss { get; set; }
    public HashSet<int> StreakCelebrationsShown { get; set; } = new();

    // Collectibles: category -> item_id -> owned
    public Dictionary<string, HashSet<string>> OwnedCollectibles { get; set; } = new();

    // Milestone tracking
    public Dictionary<string, int> MilestoneProgress { get; set; } = new()
    {
        ["interactions"] = 0,
        ["days_played"] = 0,
        ["streak"] = 0,
        ["relationship"] = 0,
    };
    public Dictionary<string, List<int>> ClaimedMilestones { get; set; } = new()
    {
        ["interactions"] = new(),
        ["days_played"] = new(),
        ["streak"] = new(),
        ["relationship"] = new(),
    };

    // Daily challenges
    public List<DailyChallenge> DailyChallenges { get; set; } = new();
    public string? LastChallengeRefresh { get; set; }

    // Unlocked titles
    public List<string> UnlockedTitles { get; set; } = new() { "Duckling Watcher" };

    // Statistics
    public Dictionary<string, int> Stats { get; set; } = new()
    {
        ["total_feeds"] = 0,
        ["total_plays"] = 0,
        ["total_cleans"] = 0,
        ["total_pets"] = 0,
        ["total_talks"] = 0,
        ["items_used"] = 0,
        ["collectibles_found"] = 0,
    };

    // Pending rewards
    [JsonIgnore]
    public List<(string Source, Reward Reward)> PendingRewards { get; set; } = new();

    private static readonly Random _random = new();

    // =============================================================================
    // XP AND LEVELING
    // =============================================================================

    /// <summary>
    /// Calculate XP needed to reach a level.
    /// </summary>
    public static int XPForLevel(int level) => (int)(100 * Math.Pow(level, 1.5));

    /// <summary>
    /// Add XP and check for level up.
    /// Returns new level if leveled up, null otherwise.
    /// </summary>
    public int? AddXP(int amount, string source = "")
    {
        // Apply streak multiplier
        var multiplier = GetStreakMultiplier();
        var boostedAmount = (int)(amount * multiplier);
        XP += boostedAmount;
        var oldLevel = Level;

        // Check for level up
        while (XP >= XPForLevel(Level + 1))
        {
            Level++;

            // Check for new title
            if (LevelTitles.TryGetValue(Level, out var newTitle))
            {
                Title = newTitle;
                if (!UnlockedTitles.Contains(newTitle))
                    UnlockedTitles.Add(newTitle);
            }
        }

        if (Level > oldLevel)
            return Level;
        return null;
    }

    /// <summary>
    /// Get the current XP multiplier based on streak.
    /// </summary>
    public float GetStreakMultiplier()
    {
        float multiplier = 1.0f;
        foreach (var (threshold, mult) in StreakXPMultipliers.OrderBy(x => x.Key))
        {
            if (CurrentStreak >= threshold)
                multiplier = mult;
        }
        return multiplier;
    }

    /// <summary>
    /// Get display string for current streak bonus.
    /// </summary>
    public string GetStreakMultiplierDisplay()
    {
        var mult = GetStreakMultiplier();
        return mult > 1.0f ? $"🔥 {mult}x XP" : "";
    }

    /// <summary>
    /// Get current XP progress: (current XP in level, XP needed for next, percentage).
    /// </summary>
    public (int Current, int Needed, float Percent) GetXPProgress()
    {
        var currentLevelXP = XPForLevel(Level);
        var nextLevelXP = XPForLevel(Level + 1);
        var xpInLevel = XP - currentLevelXP;
        var xpNeeded = nextLevelXP - currentLevelXP;
        var percentage = xpNeeded > 0 ? (float)xpInLevel / xpNeeded * 100 : 100;
        return (xpInLevel, xpNeeded, percentage);
    }

    // =============================================================================
    // LOGIN AND STREAKS
    // =============================================================================

    /// <summary>
    /// Check daily login, update streak, return daily rewards if applicable.
    /// Returns (is_new_day, rewards_list, special_message).
    /// </summary>
    public (bool IsNewDay, List<Reward> Rewards, string? SpecialMessage) CheckLogin()
    {
        var today = DateTime.Now.ToString("yyyy-MM-dd");

        if (LastLoginDate == today)
            return (false, new List<Reward>(), null);

        // It's a new day!
        var isFirstLogin = LastLoginDate == null;
        var rewards = new List<Reward>();
        string? specialMessage = null;
        StreakLostToday = false;

        if (!isFirstLogin)
        {
            // Check if streak continues
            var yesterday = DateTime.Now.AddDays(-1).ToString("yyyy-MM-dd");
            if (LastLoginDate == yesterday)
            {
                CurrentStreak++;
                DaysSinceStreakLoss = 0;
            }
            else
            {
                // Streak broken!
                if (CurrentStreak > 1)
                {
                    StreakLostToday = true;
                    PreviousStreak = CurrentStreak;
                    var msgTemplate = StreakLossMessages[_random.Next(StreakLossMessages.Length)];
                    specialMessage = string.Format(msgTemplate, PreviousStreak);
                }
                CurrentStreak = 1;
                DaysSinceStreakLoss++;
            }
        }
        else
        {
            CurrentStreak = 1;
        }

        // Update longest streak
        if (CurrentStreak > LongestStreak)
            LongestStreak = CurrentStreak;

        // Check for streak celebration milestone
        if (StreakCelebrationMessages.TryGetValue(CurrentStreak, out var celebrationMsg))
        {
            if (!StreakCelebrationsShown.Contains(CurrentStreak))
            {
                specialMessage = celebrationMsg;
                StreakCelebrationsShown.Add(CurrentStreak);
            }
        }

        // Increment days played
        DaysPlayed++;

        // Get daily rewards based on streak (cycles through week)
        var rewardDay = (CurrentStreak - 1) % 7;
        rewards.AddRange(DailyRewards[rewardDay]);

        // Bonus for long streaks
        if (CurrentStreak >= 30 && CurrentStreak % 30 == 0)
        {
            rewards.Add(new Reward(RewardType.Collectible, "feathers:iridescent_feather",
                description: "30 day streak bonus!"));
        }
        else if (CurrentStreak >= 7 && CurrentStreak % 7 == 0)
        {
            rewards.Add(new Reward(RewardType.XP, "50", description: "Weekly streak bonus!"));
        }

        // Recovery bonus
        if (DaysSinceStreakLoss > 0 && DaysSinceStreakLoss <= 3 && !StreakLostToday)
        {
            rewards.Add(new Reward(RewardType.XP, "25", description: "Welcome back bonus!"));
        }

        LastLoginDate = today;
        DailyRewardClaimed = false;

        // Update milestone progress
        MilestoneProgress["streak"] = CurrentStreak;
        MilestoneProgress["days_played"] = DaysPlayed;

        return (true, rewards, specialMessage);
    }

    /// <summary>
    /// Get time-based bonus if applicable.
    /// </summary>
    public (float Multiplier, string? Message) GetTimeBonus()
    {
        var hour = DateTime.Now.Hour;
        foreach (var (_, bonus) in TimeBonuses)
        {
            if (hour >= bonus.Start && hour < bonus.End)
                return (bonus.Mult, bonus.Message);
        }
        return (1.0f, null);
    }

    // =============================================================================
    // COLLECTIBLES
    // =============================================================================

    /// <summary>
    /// Add a collectible. Returns true if newly added.
    /// </summary>
    public bool AddCollectible(string categoryAndItem)
    {
        var parts = categoryAndItem.Split(':');
        if (parts.Length != 2) return false;

        var category = parts[0];
        var itemId = parts[1];

        if (!OwnedCollectibles.ContainsKey(category))
            OwnedCollectibles[category] = new HashSet<string>();

        if (OwnedCollectibles[category].Contains(itemId))
            return false;

        OwnedCollectibles[category].Add(itemId);
        Stats["collectibles_found"]++;
        return true;
    }

    /// <summary>
    /// Check if collectible is owned.
    /// </summary>
    public bool HasCollectible(string categoryAndItem)
    {
        var parts = categoryAndItem.Split(':');
        if (parts.Length != 2) return false;

        var category = parts[0];
        var itemId = parts[1];

        return OwnedCollectibles.TryGetValue(category, out var items) && items.Contains(itemId);
    }

    /// <summary>
    /// Get collection completion percentage for a category.
    /// </summary>
    public float GetCategoryCompletion(string category)
    {
        if (!Collectibles.TryGetValue(category, out var cat)) return 0;
        if (!OwnedCollectibles.TryGetValue(category, out var owned)) return 0;

        var total = cat.Items.Count;
        var collected = owned.Count;
        return total > 0 ? (float)collected / total * 100 : 0;
    }

    /// <summary>
    /// Get overall collection completion.
    /// </summary>
    public float GetOverallCompletion()
    {
        int total = 0, collected = 0;
        foreach (var (catName, cat) in Collectibles)
        {
            total += cat.Items.Count;
            if (OwnedCollectibles.TryGetValue(catName, out var owned))
                collected += owned.Count;
        }
        return total > 0 ? (float)collected / total * 100 : 0;
    }

    // =============================================================================
    // DAILY CHALLENGES
    // =============================================================================

    /// <summary>
    /// Generate new daily challenges.
    /// </summary>
    public void GenerateDailyChallenges()
    {
        DailyChallenges.Clear();
        var today = DateTime.Now;
        var expires = today.Date.AddDays(1);

        var challengePool = new List<(string Id, string Name, string Desc, int Target)>
        {
            ("feed_5", "Snack Time", "Feed Cheese 5 times", 5),
            ("play_3", "Fun Times", "Play with Cheese 3 times", 3),
            ("pet_5", "Affection", "Pet Cheese 5 times", 5),
            ("clean_2", "Squeaky Clean", "Clean Cheese 2 times", 2),
            ("talk_3", "Chatterbox", "Talk to Cheese 3 times", 3),
            ("explore_2", "Adventurer", "Explore 2 times", 2),
            ("craft_1", "Crafty Duck", "Craft 1 item", 1),
        };

        // Pick 3 random challenges
        var selected = challengePool.OrderBy(_ => _random.Next()).Take(3).ToList();

        foreach (var (id, name, desc, target) in selected)
        {
            DailyChallenges.Add(new DailyChallenge
            {
                Id = id,
                Name = name,
                Description = desc,
                Target = target,
                Progress = 0,
                Expires = expires,
                Reward = new Reward(RewardType.XP, (_random.Next(15, 35)).ToString(), 
                    description: $"Daily challenge: {name}")
            });
        }

        LastChallengeRefresh = today.ToString("yyyy-MM-dd");
    }

    /// <summary>
    /// Update challenge progress.
    /// </summary>
    public List<DailyChallenge> UpdateChallengeProgress(string challengeType, int amount = 1)
    {
        var completed = new List<DailyChallenge>();
        
        foreach (var challenge in DailyChallenges)
        {
            if (challenge.IsComplete) continue;
            if (!challenge.Id.StartsWith(challengeType)) continue;

            var wasComplete = challenge.IsComplete;
            challenge.Progress += amount;

            if (challenge.IsComplete && !wasComplete)
            {
                completed.Add(challenge);
                if (challenge.Reward != null)
                {
                    PendingRewards.Add((challenge.Name, challenge.Reward));
                }
            }
        }

        return completed;
    }

    // =============================================================================
    // STATISTICS
    // =============================================================================

    /// <summary>
    /// Track an interaction.
    /// </summary>
    public void TrackInteraction(string type)
    {
        var key = $"total_{type}s";
        if (Stats.ContainsKey(key))
            Stats[key]++;

        MilestoneProgress["interactions"]++;
    }

    /// <summary>
    /// Update relationship milestone.
    /// </summary>
    public void UpdateRelationship(int relationshipLevel)
    {
        MilestoneProgress["relationship"] = relationshipLevel;
    }

    // =============================================================================
    // SERIALIZATION
    // =============================================================================

    public ProgressionSaveData ToSaveData() => new()
    {
        XP = XP,
        Level = Level,
        Title = Title,
        CurrentStreak = CurrentStreak,
        LongestStreak = LongestStreak,
        LastLoginDate = LastLoginDate,
        DailyRewardClaimed = DailyRewardClaimed,
        DaysPlayed = DaysPlayed,
        StreakLostToday = StreakLostToday,
        PreviousStreak = PreviousStreak,
        DaysSinceStreakLoss = DaysSinceStreakLoss,
        StreakCelebrationsShown = StreakCelebrationsShown.ToList(),
        OwnedCollectibles = OwnedCollectibles.ToDictionary(
            kvp => kvp.Key, 
            kvp => kvp.Value.ToList()),
        MilestoneProgress = MilestoneProgress,
        ClaimedMilestones = ClaimedMilestones,
        DailyChallenges = DailyChallenges,
        LastChallengeRefresh = LastChallengeRefresh,
        UnlockedTitles = UnlockedTitles,
        Stats = Stats,
    };

    public static ProgressionSystem FromSaveData(ProgressionSaveData data)
    {
        return new ProgressionSystem
        {
            XP = data.XP,
            Level = data.Level,
            Title = data.Title ?? "Duckling Watcher",
            CurrentStreak = data.CurrentStreak,
            LongestStreak = data.LongestStreak,
            LastLoginDate = data.LastLoginDate,
            DailyRewardClaimed = data.DailyRewardClaimed,
            DaysPlayed = data.DaysPlayed,
            StreakLostToday = data.StreakLostToday,
            PreviousStreak = data.PreviousStreak,
            DaysSinceStreakLoss = data.DaysSinceStreakLoss,
            StreakCelebrationsShown = data.StreakCelebrationsShown?.ToHashSet() ?? new(),
            OwnedCollectibles = data.OwnedCollectibles?.ToDictionary(
                kvp => kvp.Key,
                kvp => kvp.Value.ToHashSet()) ?? new(),
            MilestoneProgress = data.MilestoneProgress ?? new()
            {
                ["interactions"] = 0,
                ["days_played"] = 0,
                ["streak"] = 0,
                ["relationship"] = 0,
            },
            ClaimedMilestones = data.ClaimedMilestones ?? new()
            {
                ["interactions"] = new(),
                ["days_played"] = new(),
                ["streak"] = new(),
                ["relationship"] = new(),
            },
            DailyChallenges = data.DailyChallenges ?? new(),
            LastChallengeRefresh = data.LastChallengeRefresh,
            UnlockedTitles = data.UnlockedTitles ?? new() { "Duckling Watcher" },
            Stats = data.Stats ?? new()
            {
                ["total_feeds"] = 0,
                ["total_plays"] = 0,
                ["total_cleans"] = 0,
                ["total_pets"] = 0,
                ["total_talks"] = 0,
                ["items_used"] = 0,
                ["collectibles_found"] = 0,
            },
        };
    }
}

/// <summary>
/// Save data for progression system.
/// </summary>
public class ProgressionSaveData
{
    public int XP { get; set; }
    public int Level { get; set; }
    public string? Title { get; set; }
    public int CurrentStreak { get; set; }
    public int LongestStreak { get; set; }
    public string? LastLoginDate { get; set; }
    public bool DailyRewardClaimed { get; set; }
    public int DaysPlayed { get; set; }
    public bool StreakLostToday { get; set; }
    public int PreviousStreak { get; set; }
    public int DaysSinceStreakLoss { get; set; }
    public List<int>? StreakCelebrationsShown { get; set; }
    public Dictionary<string, List<string>>? OwnedCollectibles { get; set; }
    public Dictionary<string, int>? MilestoneProgress { get; set; }
    public Dictionary<string, List<int>>? ClaimedMilestones { get; set; }
    public List<DailyChallenge>? DailyChallenges { get; set; }
    public string? LastChallengeRefresh { get; set; }
    public List<string>? UnlockedTitles { get; set; }
    public Dictionary<string, int>? Stats { get; set; }
}
