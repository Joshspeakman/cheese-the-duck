using System;
using System.Collections.Generic;
using System.Linq;

namespace StupidDuck.Duck;

/// <summary>
/// Difficulty levels for tricks.
/// </summary>
public enum TrickDifficulty
{
    Easy,
    Medium,
    Hard,
    Master,
    Legendary
}

/// <summary>
/// Categories of tricks.
/// </summary>
public enum TrickCategory
{
    Movement,
    Sound,
    Social,
    Special,
    Combo
}

/// <summary>
/// A trick the duck can learn.
/// </summary>
public class Trick
{
    public string Id { get; set; } = "";
    public string Name { get; set; } = "";
    public string Description { get; set; } = "";
    public TrickCategory Category { get; set; }
    public TrickDifficulty Difficulty { get; set; }
    public int TrainingRequired { get; set; }
    public int XpReward { get; set; }
    public int CoinReward { get; set; }
    public List<string> Animation { get; set; } = new();
    public List<string> PrerequisiteTricks { get; set; } = new();
    public int MoodBonus { get; set; }
    public string? SpecialEffect { get; set; }
}

/// <summary>
/// A trick the duck has learned.
/// </summary>
public class LearnedTrick
{
    public string TrickId { get; set; } = "";
    public DateTime LearnedAt { get; set; }
    public int TrainingProgress { get; set; }
    public int TimesPerformed { get; set; }
    public int MasteryLevel { get; set; } = 1; // 1-5
    public DateTime? LastPerformed { get; set; }
    public int PerfectPerformances { get; set; }
}

/// <summary>
/// Result of performing a trick.
/// </summary>
public class PerformanceResult
{
    public int Quality { get; set; }
    public string Rating { get; set; } = "";
    public int Xp { get; set; }
    public int Coins { get; set; }
    public bool IsPerfect { get; set; }
    public int MasteryLevel { get; set; }
    public int MoodBonus { get; set; }
    public string? SpecialEffect { get; set; }
    public List<string> Animation { get; set; } = new();
}

/// <summary>
/// Result of performing a combo.
/// </summary>
public class ComboResult
{
    public int TotalXp { get; set; }
    public int TotalCoins { get; set; }
    public int TotalMood { get; set; }
    public int ComboSize { get; set; }
    public float ComboMultiplier { get; set; }
    public List<PerformanceResult> TrickResults { get; set; } = new();
}

/// <summary>
/// System for managing duck tricks, training, and performances.
/// </summary>
public class TricksSystem
{
    private static readonly Random _random = new();

    // =============================================================================
    // TRICK DEFINITIONS
    // =============================================================================

    public static readonly Dictionary<string, Trick> AllTricks = new()
    {
        // Movement Tricks - Easy
        ["waddle_dance"] = new Trick
        {
            Id = "waddle_dance",
            Name = "Waddle Dance",
            Description = "An adorable side-to-side waddle dance!",
            Category = TrickCategory.Movement,
            Difficulty = TrickDifficulty.Easy,
            TrainingRequired = 3,
            XpReward = 15,
            CoinReward = 5,
            Animation = new() { "  <(.)  ", "   (.)> ", "  <(.)  " },
            MoodBonus = 5
        },
        ["spin"] = new Trick
        {
            Id = "spin",
            Name = "Spin",
            Description = "Spin around in a circle!",
            Category = TrickCategory.Movement,
            Difficulty = TrickDifficulty.Easy,
            TrainingRequired = 2,
            XpReward = 10,
            CoinReward = 3,
            Animation = new() { "  (.)  ", " .(.)  ", " .(..) ", "  (.)  " },
            MoodBonus = 3
        },
        ["hop"] = new Trick
        {
            Id = "hop",
            Name = "Happy Hop",
            Description = "Jump up and down excitedly!",
            Category = TrickCategory.Movement,
            Difficulty = TrickDifficulty.Easy,
            TrainingRequired = 2,
            XpReward = 10,
            CoinReward = 3,
            Animation = new() { "       ", "  (.)  ", "  ↑↑↑  ", "  (.)  " },
            MoodBonus = 5
        },
        // Movement Tricks - Medium
        ["backflip"] = new Trick
        {
            Id = "backflip",
            Name = "Backflip",
            Description = "An impressive backwards somersault!",
            Category = TrickCategory.Movement,
            Difficulty = TrickDifficulty.Medium,
            TrainingRequired = 8,
            XpReward = 35,
            CoinReward = 15,
            Animation = new() { "   (.)  ", "    ↑   ", "   (')  ", "  (.°)  ", "   (.)  " },
            PrerequisiteTricks = new() { "hop" },
            MoodBonus = 10
        },
        ["moonwalk"] = new Trick
        {
            Id = "moonwalk",
            Name = "Moonwalk",
            Description = "Smooth backwards sliding walk!",
            Category = TrickCategory.Movement,
            Difficulty = TrickDifficulty.Medium,
            TrainingRequired = 6,
            XpReward = 30,
            CoinReward = 12,
            Animation = new() { "(.)    →", " (.)   →", "  (.)  →", "   (.) →" },
            PrerequisiteTricks = new() { "waddle_dance" },
            MoodBonus = 8
        },
        // Movement Tricks - Hard
        ["double_flip"] = new Trick
        {
            Id = "double_flip",
            Name = "Double Flip",
            Description = "Two flips in a row!",
            Category = TrickCategory.Movement,
            Difficulty = TrickDifficulty.Hard,
            TrainingRequired = 15,
            XpReward = 75,
            CoinReward = 40,
            Animation = new() { "   (.) ", "   ↑↑  ", "  (°.) ", " (.°)  ", "   (.) " },
            PrerequisiteTricks = new() { "backflip" },
            MoodBonus = 15,
            SpecialEffect = "double_xp_next_action"
        },
        // Sound Tricks
        ["quack_song"] = new Trick
        {
            Id = "quack_song",
            Name = "Quack Song",
            Description = "Sing a beautiful quacking melody!",
            Category = TrickCategory.Sound,
            Difficulty = TrickDifficulty.Easy,
            TrainingRequired = 3,
            XpReward = 12,
            CoinReward = 5,
            Animation = new() { " (.) ♪ ", " (.) ♫ ", " (.) ♪♪" },
            MoodBonus = 8
        },
        ["beatbox"] = new Trick
        {
            Id = "beatbox",
            Name = "Duck Beatbox",
            Description = "Drop some sick beats!",
            Category = TrickCategory.Sound,
            Difficulty = TrickDifficulty.Medium,
            TrainingRequired = 7,
            XpReward = 30,
            CoinReward = 15,
            Animation = new() { " (.) 🎵 ", " (•)BOO", " (.)TSS", " (•)BAP" },
            PrerequisiteTricks = new() { "quack_song" },
            MoodBonus = 12
        },
        ["whistle"] = new Trick
        {
            Id = "whistle",
            Name = "Perfect Whistle",
            Description = "Whistle a tune perfectly!",
            Category = TrickCategory.Sound,
            Difficulty = TrickDifficulty.Medium,
            TrainingRequired = 5,
            XpReward = 25,
            CoinReward = 10,
            Animation = new() { " (.) ~~~ ", " (°) ~~~°" },
            MoodBonus = 5
        },
        // Social Tricks
        ["wave"] = new Trick
        {
            Id = "wave",
            Name = "Friendly Wave",
            Description = "Wave hello to everyone!",
            Category = TrickCategory.Social,
            Difficulty = TrickDifficulty.Easy,
            TrainingRequired = 2,
            XpReward = 10,
            CoinReward = 3,
            Animation = new() { " (.)/ ", " (.)| ", " (.)/ " },
            MoodBonus = 5
        },
        ["bow"] = new Trick
        {
            Id = "bow",
            Name = "Elegant Bow",
            Description = "Take a graceful bow!",
            Category = TrickCategory.Social,
            Difficulty = TrickDifficulty.Easy,
            TrainingRequired = 3,
            XpReward = 12,
            CoinReward = 5,
            Animation = new() { "  (.) ", "  (°) ", " (___)  " },
            MoodBonus = 5
        },
        ["high_five"] = new Trick
        {
            Id = "high_five",
            Name = "High Five",
            Description = "Give someone a wing high-five!",
            Category = TrickCategory.Social,
            Difficulty = TrickDifficulty.Medium,
            TrainingRequired = 4,
            XpReward = 20,
            CoinReward = 8,
            Animation = new() { "    \\|", " (.)/ ", "    * " },
            PrerequisiteTricks = new() { "wave" },
            MoodBonus = 10
        },
        // Special Tricks
        ["play_dead"] = new Trick
        {
            Id = "play_dead",
            Name = "Play Dead",
            Description = "Dramatically pretend to faint!",
            Category = TrickCategory.Special,
            Difficulty = TrickDifficulty.Medium,
            TrainingRequired = 6,
            XpReward = 25,
            CoinReward = 12,
            Animation = new() { "  (.) ", "  (x) ", " ___x " },
            MoodBonus = 3
        },
        ["peek_a_boo"] = new Trick
        {
            Id = "peek_a_boo",
            Name = "Peek-a-Boo",
            Description = "Play peek-a-boo with wing covers!",
            Category = TrickCategory.Special,
            Difficulty = TrickDifficulty.Easy,
            TrainingRequired = 3,
            XpReward = 15,
            CoinReward = 5,
            Animation = new() { " |.| ", " |(.)| ", " |.| ", " (^.^) " },
            MoodBonus = 10
        },
        ["magic_trick"] = new Trick
        {
            Id = "magic_trick",
            Name = "Magic Trick",
            Description = "Perform an amazing magic trick!",
            Category = TrickCategory.Special,
            Difficulty = TrickDifficulty.Hard,
            TrainingRequired = 12,
            XpReward = 60,
            CoinReward = 35,
            Animation = new() { "  (.) ", " *(.)* ", "  ✨   ", " POOF! " },
            PrerequisiteTricks = new() { "bow", "wave" },
            MoodBonus = 20,
            SpecialEffect = "bonus_coins"
        },
        // Combo Tricks
        ["dance_routine"] = new Trick
        {
            Id = "dance_routine",
            Name = "Full Dance Routine",
            Description = "A complete choreographed dance!",
            Category = TrickCategory.Combo,
            Difficulty = TrickDifficulty.Master,
            TrainingRequired = 20,
            XpReward = 100,
            CoinReward = 60,
            Animation = new() { "  (.) ", " <(.)>", "  ↑↑  ", " .(.) ", "  (°) " },
            PrerequisiteTricks = new() { "waddle_dance", "spin", "hop" },
            MoodBonus = 25,
            SpecialEffect = "attract_visitors"
        },
        ["legendary_performance"] = new Trick
        {
            Id = "legendary_performance",
            Name = "Legendary Performance",
            Description = "The ultimate duck performance!",
            Category = TrickCategory.Combo,
            Difficulty = TrickDifficulty.Legendary,
            TrainingRequired = 50,
            XpReward = 500,
            CoinReward = 300,
            Animation = new() { "   ★   ", " ★(.)★ ", "  ✨✨  ", " 👏👏👏 " },
            PrerequisiteTricks = new() { "dance_routine", "magic_trick", "double_flip" },
            MoodBonus = 50,
            SpecialEffect = "legendary_reward"
        }
    };

    // =============================================================================
    // STATE
    // =============================================================================

    public Dictionary<string, LearnedTrick> LearnedTricks { get; set; } = new();
    public Dictionary<string, int> TrainingProgress { get; set; } = new();
    public int TotalPerformances { get; set; }
    public int TotalPerfectPerformances { get; set; }
    public string? CurrentTraining { get; set; }
    public int TrainingStreak { get; set; }
    public DateTime? LastTrainingDate { get; set; }
    public string? FavoriteTrick { get; set; }
    public int ComboStreak { get; set; }
    public int HighestCombo { get; set; }

    // =============================================================================
    // TRICK AVAILABILITY
    // =============================================================================

    /// <summary>
    /// Get tricks available to learn.
    /// </summary>
    public List<Trick> GetAvailableTricks()
    {
        var available = new List<Trick>();

        foreach (var (trickId, trick) in AllTricks)
        {
            // Skip if already learned
            if (LearnedTricks.ContainsKey(trickId))
                continue;

            // Check prerequisites
            var prereqsMet = trick.PrerequisiteTricks.All(pt => LearnedTricks.ContainsKey(pt));

            if (prereqsMet)
                available.Add(trick);
        }

        return available;
    }

    // =============================================================================
    // TRAINING
    // =============================================================================

    /// <summary>
    /// Start training a trick.
    /// </summary>
    public (bool Success, string Message) StartTraining(string trickId)
    {
        if (LearnedTricks.ContainsKey(trickId))
            return (false, "Already learned this trick!");

        if (!AllTricks.TryGetValue(trickId, out var trick))
            return (false, "Trick not found!");

        // Check prerequisites
        foreach (var prereq in trick.PrerequisiteTricks)
        {
            if (!LearnedTricks.ContainsKey(prereq))
            {
                var prereqName = AllTricks.TryGetValue(prereq, out var pt) ? pt.Name : prereq;
                return (false, $"Need to learn '{prereqName}' first!");
            }
        }

        CurrentTraining = trickId;
        return (true, $"🎓 Started training: {trick.Name}!");
    }

    /// <summary>
    /// Complete a training session.
    /// </summary>
    public (bool Success, string Message, Trick? LearnedTrick) DoTrainingSession()
    {
        if (string.IsNullOrEmpty(CurrentTraining))
            return (false, "Not training any trick!", null);

        if (!AllTricks.TryGetValue(CurrentTraining, out var trick))
        {
            CurrentTraining = null;
            return (false, "Invalid trick!", null);
        }

        // Update progress
        if (!TrainingProgress.ContainsKey(CurrentTraining))
            TrainingProgress[CurrentTraining] = 0;
        TrainingProgress[CurrentTraining]++;

        // Update streak
        var today = DateTime.Today;
        if (LastTrainingDate.HasValue)
        {
            var daysSince = (today - LastTrainingDate.Value.Date).Days;
            if (daysSince == 1)
                TrainingStreak++;
            else if (daysSince > 1)
                TrainingStreak = 1;
        }
        else
        {
            TrainingStreak = 1;
        }
        LastTrainingDate = today;

        // Check if learned
        if (TrainingProgress[CurrentTraining] >= trick.TrainingRequired)
        {
            LearnedTricks[CurrentTraining] = new LearnedTrick
            {
                TrickId = CurrentTraining,
                LearnedAt = DateTime.Now,
                TrainingProgress = trick.TrainingRequired
            };

            var learnedTrick = trick;
            CurrentTraining = null;

            return (true, $"🎉 Learned new trick: {learnedTrick.Name}!", learnedTrick);
        }

        var progress = TrainingProgress[CurrentTraining];
        var remaining = trick.TrainingRequired - progress;

        return (true, $"📚 Training session complete! {remaining} sessions left until learned.", null);
    }

    // =============================================================================
    // PERFORMANCE
    // =============================================================================

    /// <summary>
    /// Perform a learned trick.
    /// </summary>
    public (bool Success, string Message, PerformanceResult? Result) PerformTrick(string trickId)
    {
        if (!LearnedTricks.TryGetValue(trickId, out var learned))
            return (false, "Haven't learned this trick!", null);

        if (!AllTricks.TryGetValue(trickId, out var trick))
            return (false, "Trick not found!", null);

        // Calculate performance quality
        var baseQuality = 70;
        var masteryBonus = learned.MasteryLevel * 5;
        var experienceBonus = Math.Min(learned.TimesPerformed, 20);
        var randomMod = _random.Next(-10, 11);

        var quality = Math.Clamp(baseQuality + masteryBonus + experienceBonus + randomMod, 50, 100);

        // Perfect performance?
        var isPerfect = quality >= 95;

        // Calculate rewards
        var xp = trick.XpReward;
        var coins = trick.CoinReward;

        if (isPerfect)
        {
            xp = (int)(xp * 1.5f);
            coins = (int)(coins * 1.5f);
            learned.PerfectPerformances++;
            TotalPerfectPerformances++;
        }

        var qualityMultiplier = quality / 100f;
        xp = (int)(xp * qualityMultiplier);
        coins = (int)(coins * qualityMultiplier);

        // Update stats
        learned.TimesPerformed++;
        learned.LastPerformed = DateTime.Now;
        TotalPerformances++;

        // Check for mastery level up
        int[] masteryThresholds = { 5, 15, 30, 50, 100 };
        if (learned.MasteryLevel < 5)
        {
            if (learned.TimesPerformed >= masteryThresholds[learned.MasteryLevel - 1])
                learned.MasteryLevel++;
        }

        // Performance rating
        var rating = quality switch
        {
            >= 95 => "⭐⭐⭐ PERFECT!",
            >= 85 => "⭐⭐ Excellent!",
            >= 70 => "⭐ Good!",
            _ => "Nice try!"
        };

        var result = new PerformanceResult
        {
            Quality = quality,
            Rating = rating,
            Xp = xp,
            Coins = coins,
            IsPerfect = isPerfect,
            MasteryLevel = learned.MasteryLevel,
            MoodBonus = trick.MoodBonus,
            SpecialEffect = isPerfect ? trick.SpecialEffect : null,
            Animation = trick.Animation
        };

        return (true, $"🎭 {trick.Name} - {rating}", result);
    }

    /// <summary>
    /// Perform multiple tricks in a combo.
    /// </summary>
    public (bool Success, string Message, ComboResult? Result) PerformCombo(List<string> trickIds)
    {
        if (trickIds.Count < 2)
            return (false, "Combos need at least 2 tricks!", null);

        // Verify all tricks are learned
        foreach (var tid in trickIds)
        {
            if (!LearnedTricks.ContainsKey(tid))
                return (false, $"Haven't learned {tid}!", null);
        }

        var totalXp = 0;
        var totalCoins = 0;
        var totalMood = 0;
        var comboMultiplier = 1.0f + (trickIds.Count - 1) * 0.25f;

        var results = new List<PerformanceResult>();
        foreach (var tid in trickIds)
        {
            var (success, _, result) = PerformTrick(tid);
            if (success && result != null)
            {
                results.Add(result);
                totalXp += result.Xp;
                totalCoins += result.Coins;
                totalMood += result.MoodBonus;
            }
        }

        // Apply combo multiplier
        totalXp = (int)(totalXp * comboMultiplier);
        totalCoins = (int)(totalCoins * comboMultiplier);

        ComboStreak = trickIds.Count;
        if (ComboStreak > HighestCombo)
            HighestCombo = ComboStreak;

        var comboResult = new ComboResult
        {
            TotalXp = totalXp,
            TotalCoins = totalCoins,
            TotalMood = totalMood,
            ComboSize = trickIds.Count,
            ComboMultiplier = comboMultiplier,
            TrickResults = results
        };

        return (true, $"🔥 {trickIds.Count}-Hit Combo! ({comboMultiplier:P0} bonus)", comboResult);
    }

    // =============================================================================
    // TRAINING STATUS
    // =============================================================================

    /// <summary>
    /// Get current training status.
    /// </summary>
    public (bool IsTraining, string? TrickName, int Progress, int Required, float Percent) GetTrainingStatus()
    {
        if (string.IsNullOrEmpty(CurrentTraining))
            return (false, null, 0, 0, 0);

        if (!AllTricks.TryGetValue(CurrentTraining, out var trick))
            return (false, null, 0, 0, 0);

        var progress = TrainingProgress.GetValueOrDefault(CurrentTraining, 0);
        var percent = (float)progress / trick.TrainingRequired * 100f;

        return (true, trick.Name, progress, trick.TrainingRequired, percent);
    }

    // =============================================================================
    // DISPLAY
    // =============================================================================

    /// <summary>
    /// Render the list of tricks.
    /// </summary>
    public List<string> RenderTrickList()
    {
        var lines = new List<string>
        {
            "╔═══════════════════════════════════════════════╗",
            "║            🎭 DUCK TRICKS 🎭                  ║",
            "╠═══════════════════════════════════════════════╣",
            $"║  Learned: {LearnedTricks.Count,2}  |  Performances: {TotalPerformances,5}       ║",
            $"║  Perfect: {TotalPerfectPerformances,3}  |  Highest Combo: {HighestCombo,2}          ║",
            "╠═══════════════════════════════════════════════╣",
            "║  LEARNED TRICKS:                              ║"
        };

        foreach (var (tid, learned) in LearnedTricks.Take(5))
        {
            if (AllTricks.TryGetValue(tid, out var trick))
            {
                var stars = new string('★', learned.MasteryLevel) + new string('☆', 5 - learned.MasteryLevel);
                var name = trick.Name.Length > 20 ? trick.Name[..20] : trick.Name;
                lines.Add($"║   {name,-20} {stars}         ║");
            }
        }

        if (LearnedTricks.Count == 0)
            lines.Add("║   No tricks learned yet!                      ║");

        // Training status
        var (isTraining, trickName, progress, required, percent) = GetTrainingStatus();
        if (isTraining && trickName != null)
        {
            lines.Add("╠═══════════════════════════════════════════════╣");
            var truncName = trickName.Length > 28 ? trickName[..28] : trickName;
            lines.Add($"║  Training: {truncName,-28}   ║");
            lines.Add($"║  Progress: {progress}/{required} ({percent:F0}%)                      ║");
        }

        // Available to learn
        var available = GetAvailableTricks();
        if (available.Count > 0)
        {
            lines.Add("╠═══════════════════════════════════════════════╣");
            lines.Add("║  AVAILABLE TO LEARN:                          ║");
            foreach (var trick in available.Take(3))
            {
                var diffIcon = trick.Difficulty switch
                {
                    TrickDifficulty.Easy => "🟢",
                    TrickDifficulty.Medium => "🟡",
                    TrickDifficulty.Hard => "🟠",
                    TrickDifficulty.Master => "🔴",
                    TrickDifficulty.Legendary => "💎",
                    _ => "⚪"
                };
                var name = trick.Name.Length > 33 ? trick.Name[..33] : trick.Name;
                lines.Add($"║   {diffIcon} {name,-33}   ║");
            }
        }

        lines.Add("╚═══════════════════════════════════════════════╝");

        return lines;
    }

    /// <summary>
    /// Render trick performance animation.
    /// </summary>
    public List<string> RenderTrickPerformance(string trickId)
    {
        if (!AllTricks.TryGetValue(trickId, out var trick))
            return new List<string> { "Trick not found!" };

        var lines = new List<string>
        {
            "╔═══════════════════════════════════════════════╗",
            $"║        🎭 {trick.Name,28} 🎭        ║",
            "╠═══════════════════════════════════════════════╣"
        };

        foreach (var frame in trick.Animation)
        {
            var paddedFrame = frame.Length > 30 ? frame[..30] : frame;
            lines.Add($"║           {paddedFrame,-30}          ║");
        }

        lines.Add("╚═══════════════════════════════════════════════╝");

        return lines;
    }

    // =============================================================================
    // SERIALIZATION
    // =============================================================================

    public TricksSaveData ToSaveData() => new()
    {
        LearnedTricks = LearnedTricks.ToDictionary(
            kvp => kvp.Key,
            kvp => new LearnedTrickSaveData
            {
                TrickId = kvp.Value.TrickId,
                LearnedAt = kvp.Value.LearnedAt.ToString("O"),
                TrainingProgress = kvp.Value.TrainingProgress,
                TimesPerformed = kvp.Value.TimesPerformed,
                MasteryLevel = kvp.Value.MasteryLevel,
                LastPerformed = kvp.Value.LastPerformed?.ToString("O"),
                PerfectPerformances = kvp.Value.PerfectPerformances
            }),
        TrainingProgress = TrainingProgress,
        TotalPerformances = TotalPerformances,
        TotalPerfectPerformances = TotalPerfectPerformances,
        CurrentTraining = CurrentTraining,
        TrainingStreak = TrainingStreak,
        LastTrainingDate = LastTrainingDate?.ToString("O"),
        FavoriteTrick = FavoriteTrick,
        ComboStreak = ComboStreak,
        HighestCombo = HighestCombo
    };

    public static TricksSystem FromSaveData(TricksSaveData data)
    {
        var system = new TricksSystem
        {
            TrainingProgress = data.TrainingProgress ?? new(),
            TotalPerformances = data.TotalPerformances,
            TotalPerfectPerformances = data.TotalPerfectPerformances,
            CurrentTraining = data.CurrentTraining,
            TrainingStreak = data.TrainingStreak,
            FavoriteTrick = data.FavoriteTrick,
            ComboStreak = data.ComboStreak,
            HighestCombo = data.HighestCombo
        };

        if (!string.IsNullOrEmpty(data.LastTrainingDate))
            system.LastTrainingDate = DateTime.Parse(data.LastTrainingDate);

        if (data.LearnedTricks != null)
        {
            foreach (var (tid, tdata) in data.LearnedTricks)
            {
                system.LearnedTricks[tid] = new LearnedTrick
                {
                    TrickId = tdata.TrickId ?? tid,
                    LearnedAt = string.IsNullOrEmpty(tdata.LearnedAt) ? DateTime.Now : DateTime.Parse(tdata.LearnedAt),
                    TrainingProgress = tdata.TrainingProgress,
                    TimesPerformed = tdata.TimesPerformed,
                    MasteryLevel = tdata.MasteryLevel > 0 ? tdata.MasteryLevel : 1,
                    LastPerformed = string.IsNullOrEmpty(tdata.LastPerformed) ? null : DateTime.Parse(tdata.LastPerformed),
                    PerfectPerformances = tdata.PerfectPerformances
                };
            }
        }

        return system;
    }
}

/// <summary>
/// Save data for a learned trick.
/// </summary>
public class LearnedTrickSaveData
{
    public string? TrickId { get; set; }
    public string? LearnedAt { get; set; }
    public int TrainingProgress { get; set; }
    public int TimesPerformed { get; set; }
    public int MasteryLevel { get; set; }
    public string? LastPerformed { get; set; }
    public int PerfectPerformances { get; set; }
}

/// <summary>
/// Save data for tricks system.
/// </summary>
public class TricksSaveData
{
    public Dictionary<string, LearnedTrickSaveData>? LearnedTricks { get; set; }
    public Dictionary<string, int>? TrainingProgress { get; set; }
    public int TotalPerformances { get; set; }
    public int TotalPerfectPerformances { get; set; }
    public string? CurrentTraining { get; set; }
    public int TrainingStreak { get; set; }
    public string? LastTrainingDate { get; set; }
    public string? FavoriteTrick { get; set; }
    public int ComboStreak { get; set; }
    public int HighestCombo { get; set; }
}
