using System;
using System.Collections.Generic;
using System.Linq;

namespace StupidDuck.World
{
    /// <summary>
    /// An achievement that can be unlocked.
    /// </summary>
    public class Achievement
    {
        public string Id { get; set; } = "";
        public string Name { get; set; } = "";
        public string Description { get; set; } = "";
        public string SecretDescription { get; set; } = "";
        public string Category { get; set; } = ""; // interaction, growth, time, secret, legendary
        public string Icon { get; set; } = "";
        public string Rarity { get; set; } = "common"; // common, uncommon, rare, legendary, secret
        public bool Hidden { get; set; }
    }

    /// <summary>
    /// Manages player achievements.
    /// </summary>
    public class AchievementSystem
    {
        // All achievements database
        public static readonly Dictionary<string, Achievement> Achievements = new()
        {
            // ==================== INTERACTION ACHIEVEMENTS ====================
            ["first_feed"] = new Achievement
            {
                Id = "first_feed", Name = "First Meal", Description = "Fed your duck for the first time",
                Category = "interaction", Icon = "[F]", Rarity = "common"
            },
            ["10_feeds"] = new Achievement
            {
                Id = "10_feeds", Name = "Feeder I", Description = "Fed your duck 10 times",
                Category = "interaction", Icon = "[F]", Rarity = "common"
            },
            ["50_feeds"] = new Achievement
            {
                Id = "50_feeds", Name = "Feeder II", Description = "Fed your duck 50 times",
                Category = "interaction", Icon = "[F]", Rarity = "uncommon"
            },
            ["100_feeds"] = new Achievement
            {
                Id = "100_feeds", Name = "Master Feeder", Description = "Fed your duck 100 times",
                Category = "interaction", Icon = "[F]", Rarity = "rare"
            },
            ["10_plays"] = new Achievement
            {
                Id = "10_plays", Name = "Playmate I", Description = "Played with your duck 10 times",
                Category = "interaction", Icon = "[P]", Rarity = "common"
            },
            ["50_plays"] = new Achievement
            {
                Id = "50_plays", Name = "Playmate II", Description = "Played with your duck 50 times",
                Category = "interaction", Icon = "[P]", Rarity = "uncommon"
            },
            ["100_plays"] = new Achievement
            {
                Id = "100_plays", Name = "Best Playmate", Description = "Played with your duck 100 times",
                Category = "interaction", Icon = "[P]", Rarity = "rare"
            },
            ["10_pets"] = new Achievement
            {
                Id = "10_pets", Name = "Affectionate I", Description = "Petted your duck 10 times",
                Category = "interaction", Icon = "[E]", Rarity = "common"
            },
            ["50_pets"] = new Achievement
            {
                Id = "50_pets", Name = "Affectionate II", Description = "Petted your duck 50 times",
                Category = "interaction", Icon = "[E]", Rarity = "uncommon"
            },
            ["100_pets"] = new Achievement
            {
                Id = "100_pets", Name = "Cuddle Expert", Description = "Petted your duck 100 times",
                Category = "interaction", Icon = "[E]", Rarity = "rare"
            },

            // ==================== GROWTH ACHIEVEMENTS ====================
            ["reach_duckling"] = new Achievement
            {
                Id = "reach_duckling", Name = "Born!", Description = "Your duck hatched from an egg",
                Category = "growth", Icon = "[D]", Rarity = "common"
            },
            ["reach_teen"] = new Achievement
            {
                Id = "reach_teen", Name = "Growing Up", Description = "Your duck became a teenager",
                Category = "growth", Icon = "[T]", Rarity = "uncommon"
            },
            ["reach_adult"] = new Achievement
            {
                Id = "reach_adult", Name = "All Grown Up", Description = "Your duck became an adult",
                Category = "growth", Icon = "[A]", Rarity = "rare"
            },
            ["reach_elder"] = new Achievement
            {
                Id = "reach_elder", Name = "Wise One", Description = "Your duck became an elder",
                Category = "growth", Icon = "[E]", Rarity = "legendary"
            },

            // ==================== MOOD ACHIEVEMENTS ====================
            ["first_ecstatic"] = new Achievement
            {
                Id = "first_ecstatic", Name = "Pure Joy", Description = "Made your duck ecstatic for the first time",
                Category = "mood", Icon = "[!]", Rarity = "uncommon"
            },
            ["keep_happy_day"] = new Achievement
            {
                Id = "keep_happy_day", Name = "Good Day", Description = "Kept your duck happy for a full day",
                Category = "mood", Icon = "[^]", Rarity = "rare"
            },

            // ==================== RELATIONSHIP ACHIEVEMENTS ====================
            ["best_friends"] = new Achievement
            {
                Id = "best_friends", Name = "Best Friends Forever", Description = "Reached 'bonded' relationship with your duck",
                Category = "relationship", Icon = "[<3]", Rarity = "legendary"
            },

            // ==================== TIME ACHIEVEMENTS ====================
            ["week_played"] = new Achievement
            {
                Id = "week_played", Name = "Dedicated", Description = "Played for a week",
                Category = "time", Icon = "[7]", Rarity = "uncommon"
            },
            ["month_played"] = new Achievement
            {
                Id = "month_played", Name = "Committed", Description = "Played for a month",
                Category = "time", Icon = "[30]", Rarity = "rare"
            },

            // ==================== SECRET ACHIEVEMENTS ====================
            ["midnight_duck"] = new Achievement
            {
                Id = "midnight_duck", Name = "Night Owl", Description = "Played with your duck at midnight",
                SecretDescription = "???", Category = "secret", Icon = "[?]", Rarity = "secret", Hidden = true
            },
            ["early_bird"] = new Achievement
            {
                Id = "early_bird", Name = "Early Bird", Description = "Played with your duck at 5 AM",
                SecretDescription = "???", Category = "secret", Icon = "[?]", Rarity = "secret", Hidden = true
            },
            ["derp_master"] = new Achievement
            {
                Id = "derp_master", Name = "Derp Master", Description = "Witnessed your duck trip over nothing 10 times",
                SecretDescription = "???", Category = "secret", Icon = "[?]", Rarity = "secret", Hidden = true
            },
            ["golden_discovery"] = new Achievement
            {
                Id = "golden_discovery", Name = "Legendary Find", Description = "Found the Golden Crumb",
                SecretDescription = "???", Category = "secret", Icon = "[G]", Rarity = "legendary", Hidden = true
            },
            ["patient_one"] = new Achievement
            {
                Id = "patient_one", Name = "The Patient One", Description = "Waited 5 minutes without doing anything",
                SecretDescription = "???", Category = "secret", Icon = "[.]", Rarity = "secret", Hidden = true
            },
            ["quack_master"] = new Achievement
            {
                Id = "quack_master", Name = "Quack Master", Description = "Heard your duck quack 50 times",
                SecretDescription = "???", Category = "secret", Icon = "[Q]", Rarity = "secret", Hidden = true
            },
            ["holiday_spirit"] = new Achievement
            {
                Id = "holiday_spirit", Name = "Holiday Spirit", Description = "Played during a special holiday event",
                SecretDescription = "???", Category = "secret", Icon = "[*]", Rarity = "secret", Hidden = true
            },

            // ==================== EXPLORATION ACHIEVEMENTS ====================
            ["first_explore"] = new Achievement
            {
                Id = "first_explore", Name = "Explorer", Description = "Explored your first area",
                Category = "exploration", Icon = "[E]", Rarity = "common"
            },
            ["discover_5_areas"] = new Achievement
            {
                Id = "discover_5_areas", Name = "Adventurer", Description = "Discovered 5 different areas",
                Category = "exploration", Icon = "[E]", Rarity = "uncommon"
            },
            ["discover_10_areas"] = new Achievement
            {
                Id = "discover_10_areas", Name = "World Explorer", Description = "Discovered 10 different areas",
                Category = "exploration", Icon = "[E]", Rarity = "rare"
            },
            ["gathering_master"] = new Achievement
            {
                Id = "gathering_master", Name = "Gathering Master", Description = "Reached gathering skill level 5",
                Category = "exploration", Icon = "[G]", Rarity = "rare"
            },
            ["rare_find"] = new Achievement
            {
                Id = "rare_find", Name = "Rare Find", Description = "Found a rare item while exploring",
                Category = "exploration", Icon = "[R]", Rarity = "uncommon"
            },

            // ==================== CRAFTING ACHIEVEMENTS ====================
            ["first_craft"] = new Achievement
            {
                Id = "first_craft", Name = "Crafter", Description = "Crafted your first item",
                Category = "crafting", Icon = "[C]", Rarity = "common"
            },
            ["craft_10"] = new Achievement
            {
                Id = "craft_10", Name = "Artisan", Description = "Crafted 10 items",
                Category = "crafting", Icon = "[C]", Rarity = "uncommon"
            },
            ["craft_tool"] = new Achievement
            {
                Id = "craft_tool", Name = "Tool Maker", Description = "Crafted your first tool",
                Category = "crafting", Icon = "[T]", Rarity = "uncommon"
            },
            ["crafting_master"] = new Achievement
            {
                Id = "crafting_master", Name = "Crafting Master", Description = "Reached crafting skill level 5",
                Category = "crafting", Icon = "[C]", Rarity = "rare"
            },

            // ==================== BUILDING ACHIEVEMENTS ====================
            ["first_build"] = new Achievement
            {
                Id = "first_build", Name = "Builder", Description = "Built your first structure",
                Category = "building", Icon = "[B]", Rarity = "common"
            },
            ["build_nest"] = new Achievement
            {
                Id = "build_nest", Name = "Homemaker", Description = "Built a cozy nest",
                Category = "building", Icon = "[N]", Rarity = "common"
            },
            ["build_house"] = new Achievement
            {
                Id = "build_house", Name = "Architect", Description = "Built a proper house",
                Category = "building", Icon = "[H]", Rarity = "rare"
            },
            ["build_5"] = new Achievement
            {
                Id = "build_5", Name = "Construction Duck", Description = "Built 5 structures",
                Category = "building", Icon = "[B]", Rarity = "uncommon"
            },
            ["building_master"] = new Achievement
            {
                Id = "building_master", Name = "Master Builder", Description = "Reached building skill level 5",
                Category = "building", Icon = "[B]", Rarity = "rare"
            },

            // ==================== MINIGAME ACHIEVEMENTS ====================
            ["first_minigame"] = new Achievement
            {
                Id = "first_minigame", Name = "Game On!", Description = "Played your first mini-game",
                Category = "minigame", Icon = "[J]", Rarity = "common"
            },
            ["minigame_fan"] = new Achievement
            {
                Id = "minigame_fan", Name = "Game Fan", Description = "Played 10 mini-games",
                Category = "minigame", Icon = "[J]", Rarity = "uncommon"
            },
            ["minigame_master"] = new Achievement
            {
                Id = "minigame_master", Name = "Game Master", Description = "Played 50 mini-games",
                Category = "minigame", Icon = "[J]", Rarity = "rare"
            },
            ["high_scorer"] = new Achievement
            {
                Id = "high_scorer", Name = "High Scorer", Description = "Set a new high score in any mini-game",
                Category = "minigame", Icon = "[H]", Rarity = "uncommon"
            },
            ["bread_master"] = new Achievement
            {
                Id = "bread_master", Name = "Bread Catcher", Description = "Scored 500+ in Bread Catch",
                SecretDescription = "???", Category = "minigame", Icon = "[B]", Rarity = "rare", Hidden = true
            },
            ["bug_hunter"] = new Achievement
            {
                Id = "bug_hunter", Name = "Bug Hunter", Description = "Scored 1000+ in Bug Chase",
                SecretDescription = "???", Category = "minigame", Icon = "[B]", Rarity = "rare", Hidden = true
            },
            ["perfect_memory"] = new Achievement
            {
                Id = "perfect_memory", Name = "Perfect Memory", Description = "Won Memory Match in 16 moves or less",
                SecretDescription = "???", Category = "minigame", Icon = "[M]", Rarity = "legendary", Hidden = true
            },
            ["speed_demon"] = new Achievement
            {
                Id = "speed_demon", Name = "Speed Demon", Description = "Won Duck Race in under 10 seconds",
                SecretDescription = "???", Category = "minigame", Icon = "[R]", Rarity = "legendary", Hidden = true
            },

            // ==================== DREAM ACHIEVEMENTS ====================
            ["first_dream"] = new Achievement
            {
                Id = "first_dream", Name = "Sweet Dreams", Description = "Had your first dream",
                Category = "dreams", Icon = "[Z]", Rarity = "common"
            },
            ["dreamer"] = new Achievement
            {
                Id = "dreamer", Name = "Dreamer", Description = "Had 10 dreams",
                Category = "dreams", Icon = "[Z]", Rarity = "uncommon"
            },
            ["dream_master"] = new Achievement
            {
                Id = "dream_master", Name = "Dream Walker", Description = "Had 50 dreams",
                Category = "dreams", Icon = "[Z]", Rarity = "rare"
            },
            ["dream_treasure"] = new Achievement
            {
                Id = "dream_treasure", Name = "Dream Treasure", Description = "Found an item in a dream",
                SecretDescription = "???", Category = "dreams", Icon = "[D]", Rarity = "uncommon", Hidden = true
            },
            ["dream_collector"] = new Achievement
            {
                Id = "dream_collector", Name = "Dream Collector", Description = "Found 5 items in dreams",
                SecretDescription = "???", Category = "dreams", Icon = "[D]", Rarity = "rare", Hidden = true
            },
            ["dream_explorer"] = new Achievement
            {
                Id = "dream_explorer", Name = "Dream Explorer", Description = "Experienced all types of dreams",
                SecretDescription = "???", Category = "dreams", Icon = "[*]", Rarity = "legendary", Hidden = true
            },

            // ==================== VISITOR ACHIEVEMENTS ====================
            ["first_visitor"] = new Achievement
            {
                Id = "first_visitor", Name = "Host", Description = "Had your first visitor",
                Category = "visitors", Icon = "[V]", Rarity = "common"
            },
            ["social_butterfly"] = new Achievement
            {
                Id = "social_butterfly", Name = "Social Butterfly", Description = "Met 5 different visitors",
                Category = "visitors", Icon = "[V]", Rarity = "uncommon"
            },
            ["popular_duck"] = new Achievement
            {
                Id = "popular_duck", Name = "Popular Duck", Description = "Had 20 total visitor visits",
                Category = "visitors", Icon = "[V]", Rarity = "rare"
            },
            ["best_friend_visitor"] = new Achievement
            {
                Id = "best_friend_visitor", Name = "Best Friends", Description = "Reached best friend status with a visitor",
                SecretDescription = "???", Category = "visitors", Icon = "[<3]", Rarity = "legendary", Hidden = true
            },
            ["met_gerald"] = new Achievement
            {
                Id = "met_gerald", Name = "Goose Friend", Description = "Met Gerald the Goose",
                SecretDescription = "???", Category = "visitors", Icon = "[G]", Rarity = "secret", Hidden = true
            },
            ["met_professor"] = new Achievement
            {
                Id = "met_professor", Name = "Wise Student", Description = "Met Professor Hoot",
                SecretDescription = "???", Category = "visitors", Icon = "[O]", Rarity = "secret", Hidden = true
            },
            ["met_all_visitors"] = new Achievement
            {
                Id = "met_all_visitors", Name = "Social Legend", Description = "Met all possible visitors",
                SecretDescription = "???", Category = "visitors", Icon = "[*]", Rarity = "legendary", Hidden = true
            },

            // ==================== SEASONAL ACHIEVEMENTS ====================
            ["spring_celebration"] = new Achievement
            {
                Id = "spring_celebration", Name = "Spring Has Sprung", Description = "Played during a Spring event",
                Category = "seasonal", Icon = "[S]", Rarity = "uncommon"
            },
            ["summer_fun"] = new Achievement
            {
                Id = "summer_fun", Name = "Summer Vibes", Description = "Played during a Summer event",
                Category = "seasonal", Icon = "[S]", Rarity = "uncommon"
            },
            ["fall_harvest"] = new Achievement
            {
                Id = "fall_harvest", Name = "Harvest Time", Description = "Played during a Fall event",
                Category = "seasonal", Icon = "[S]", Rarity = "uncommon"
            },
            ["winter_wonderland"] = new Achievement
            {
                Id = "winter_wonderland", Name = "Winter Wonderland", Description = "Played during a Winter event",
                Category = "seasonal", Icon = "[S]", Rarity = "uncommon"
            },
            ["all_seasons"] = new Achievement
            {
                Id = "all_seasons", Name = "Season Master", Description = "Experienced all four seasons",
                Category = "seasonal", Icon = "[*]", Rarity = "rare"
            },

            // ==================== MILESTONE ACHIEVEMENTS ====================
            ["happy_birthday"] = new Achievement
            {
                Id = "happy_birthday", Name = "Happy Hatch Day!", Description = "Celebrated your duck's birthday",
                Category = "milestone", Icon = "[B]", Rarity = "rare"
            },
            ["week_together"] = new Achievement
            {
                Id = "week_together", Name = "One Week Friend", Description = "Been together for one week",
                Category = "milestone", Icon = "[7]", Rarity = "common"
            },
            ["month_together"] = new Achievement
            {
                Id = "month_together", Name = "Monthly Bond", Description = "Been together for one month",
                Category = "milestone", Icon = "[30]", Rarity = "uncommon"
            },
            ["century_of_love"] = new Achievement
            {
                Id = "century_of_love", Name = "Century of Love", Description = "Been together for 100 days",
                Category = "milestone", Icon = "[100]", Rarity = "rare"
            },
            ["year_together"] = new Achievement
            {
                Id = "year_together", Name = "Forever Friends", Description = "Been together for one whole year!",
                Category = "milestone", Icon = "[365]", Rarity = "legendary"
            },

            // ==================== KNOWLEDGE ACHIEVEMENTS ====================
            ["duck_scholar"] = new Achievement
            {
                Id = "duck_scholar", Name = "Duck Scholar", Description = "Learned 10 duck facts",
                Category = "knowledge", Icon = "[F]", Rarity = "uncommon"
            },
            ["duck_professor"] = new Achievement
            {
                Id = "duck_professor", Name = "Duck Professor", Description = "Learned 50 duck facts",
                Category = "knowledge", Icon = "[F]", Rarity = "rare"
            }
        };

        // Instance fields
        private HashSet<string> _unlocked = new();
        private Dictionary<string, string> _unlockTimes = new();
        private Dictionary<string, int> _progress = new();
        private List<Achievement> _pendingNotifications = new();

        /// <summary>
        /// Unlock an achievement.
        /// </summary>
        /// <returns>The achievement if newly unlocked, null if already unlocked.</returns>
        public Achievement? Unlock(string achievementId)
        {
            if (_unlocked.Contains(achievementId))
                return null;

            if (!Achievements.TryGetValue(achievementId, out var achievement))
                return null;

            _unlocked.Add(achievementId);
            _unlockTimes[achievementId] = DateTime.Now.ToString("o");
            _pendingNotifications.Add(achievement);

            return achievement;
        }

        /// <summary>
        /// Check if an achievement is unlocked.
        /// </summary>
        public bool IsUnlocked(string achievementId)
        {
            return _unlocked.Contains(achievementId);
        }

        /// <summary>
        /// Get all unlocked achievements.
        /// </summary>
        public List<Achievement> GetUnlocked()
        {
            return _unlocked
                .Where(aid => Achievements.ContainsKey(aid))
                .Select(aid => Achievements[aid])
                .ToList();
        }

        /// <summary>
        /// Get all locked achievements (non-hidden ones).
        /// </summary>
        public List<Achievement> GetLocked()
        {
            return Achievements.Values
                .Where(ach => !_unlocked.Contains(ach.Id) && !ach.Hidden)
                .ToList();
        }

        /// <summary>
        /// Get number of unlocked achievements.
        /// </summary>
        public int GetUnlockedCount()
        {
            return _unlocked.Count;
        }

        /// <summary>
        /// Get total number of achievements (excluding hidden).
        /// </summary>
        public int GetTotalCount()
        {
            return Achievements.Values.Count(a => !a.Hidden);
        }

        /// <summary>
        /// Get and clear pending achievement notifications.
        /// </summary>
        public List<Achievement> GetPendingNotifications()
        {
            var pending = new List<Achievement>(_pendingNotifications);
            _pendingNotifications.Clear();
            return pending;
        }

        /// <summary>
        /// Increment progress on a progress-based achievement.
        /// </summary>
        public Achievement? IncrementProgress(string achievementId, int amount = 1)
        {
            _progress[achievementId] = _progress.GetValueOrDefault(achievementId) + amount;
            return null; // Would need targets defined to auto-unlock
        }

        /// <summary>
        /// Get progress for an achievement.
        /// </summary>
        public int GetProgress(string achievementId)
        {
            return _progress.GetValueOrDefault(achievementId);
        }

        /// <summary>
        /// Get achievements by category.
        /// </summary>
        public static List<Achievement> GetByCategory(string category)
        {
            return Achievements.Values.Where(a => a.Category == category).ToList();
        }

        /// <summary>
        /// Get achievements by rarity.
        /// </summary>
        public static List<Achievement> GetByRarity(string rarity)
        {
            return Achievements.Values.Where(a => a.Rarity == rarity).ToList();
        }

        /// <summary>
        /// Render the achievements display.
        /// </summary>
        public List<string> RenderAchievements()
        {
            var lines = new List<string>
            {
                "╔═══════════════════════════════════════╗",
                "║        🏆 ACHIEVEMENTS 🏆             ║",
                $"║  Unlocked: {GetUnlockedCount()}/{GetTotalCount()}                      ║",
                "╠═══════════════════════════════════════╣"
            };

            var unlocked = GetUnlocked().Take(8);
            foreach (var ach in unlocked)
            {
                lines.Add($"║ {ach.Icon} {ach.Name,-25}  ✓    ║");
            }

            if (!unlocked.Any())
            {
                lines.Add("║  No achievements yet!                ║");
            }

            lines.Add("╚═══════════════════════════════════════╝");

            return lines;
        }

        /// <summary>
        /// Convert to dictionary for saving.
        /// </summary>
        public Dictionary<string, object> ToSaveData()
        {
            return new Dictionary<string, object>
            {
                ["unlocked"] = _unlocked.ToList(),
                ["unlock_times"] = new Dictionary<string, string>(_unlockTimes),
                ["progress"] = new Dictionary<string, int>(_progress)
            };
        }

        /// <summary>
        /// Create from dictionary.
        /// </summary>
        public static AchievementSystem FromSaveData(Dictionary<string, object> data)
        {
            var system = new AchievementSystem();

            if (data.TryGetValue("unlocked", out var unlockedObj) && unlockedObj is List<string> unlocked)
                system._unlocked = new HashSet<string>(unlocked);

            if (data.TryGetValue("unlock_times", out var timesObj) && timesObj is Dictionary<string, string> times)
                system._unlockTimes = new Dictionary<string, string>(times);

            if (data.TryGetValue("progress", out var progressObj) && progressObj is Dictionary<string, int> progress)
                system._progress = new Dictionary<string, int>(progress);

            return system;
        }
    }
}
