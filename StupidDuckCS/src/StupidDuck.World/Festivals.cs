using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;

namespace StupidDuck.World;

/// <summary>
/// Types of seasonal festivals.
/// </summary>
public enum FestivalType
{
    SpringBloom,
    SummerSplash,
    AutumnHarvest,
    WinterWonder,
    DuckDay,
    LoveFestival,
    Starlight,
    HarvestMoon
}

/// <summary>
/// A reward from participating in a festival.
/// </summary>
public class FestivalReward
{
    public string Name { get; init; } = "";
    public string Description { get; init; } = "";
    public string ItemType { get; init; } = "";  // cosmetic, consumable, decoration, currency
    public string Rarity { get; init; } = "";
    public int XpValue { get; init; }
    public int CoinValue { get; init; }
}

/// <summary>
/// A festival-specific activity.
/// </summary>
public class FestivalActivity
{
    public string Id { get; init; } = "";
    public string Name { get; init; } = "";
    public string Description { get; init; } = "";
    public int ParticipationPoints { get; init; }
    public int CooldownMinutes { get; init; }
    public int MaxDaily { get; init; }
    public List<FestivalReward> Rewards { get; init; } = new();
}

/// <summary>
/// A seasonal festival event.
/// </summary>
public class Festival
{
    public string Id { get; init; } = "";
    public string Name { get; init; } = "";
    public string Description { get; init; } = "";
    public FestivalType Type { get; init; }
    public int StartMonth { get; init; }
    public int StartDay { get; init; }
    public int DurationDays { get; init; }
    public string ThemeColor { get; init; } = "";
    public List<FestivalActivity> Activities { get; init; } = new();
    public List<FestivalReward> ExclusiveRewards { get; init; } = new();
    public List<string> Decorations { get; init; } = new();
    public string? SpecialNpc { get; init; }
    public string? MusicTheme { get; init; }
}

/// <summary>
/// Player's progress in a festival.
/// </summary>
public class FestivalProgress
{
    public string FestivalId { get; set; } = "";
    public int Year { get; set; }
    public int ParticipationPoints { get; set; }
    public Dictionary<string, int> ActivitiesCompleted { get; set; } = new();
    public List<string> RewardsClaimed { get; set; } = new();
    public Dictionary<string, int> DailyActivities { get; set; } = new();
    public string LastActivityDate { get; set; } = "";
}

/// <summary>
/// Seasonal Festivals System - Special holiday events and celebrations.
/// </summary>
public class FestivalSystem
{
    private static readonly Random _random = new();
    
    public Dictionary<string, List<FestivalProgress>> FestivalHistory { get; private set; } = new();
    public FestivalProgress? CurrentFestivalProgress { get; private set; }
    public int TotalFestivalsParticipated { get; private set; }
    public List<string> FestivalRewardsCollected { get; private set; } = new();
    public string? FavoriteFestival { get; set; }
    public string LastFestivalCheck { get; set; } = "";
    
    // Festival definitions
    private static readonly Dictionary<string, Festival> Festivals = new()
    {
        ["spring_bloom"] = new Festival
        {
            Id = "spring_bloom",
            Name = "🌸 Spring Bloom Festival",
            Description = "Celebrate the return of spring with flowers, butterflies, and new beginnings!",
            Type = FestivalType.SpringBloom,
            StartMonth = 3,
            StartDay = 20,
            DurationDays = 14,
            ThemeColor = "pink",
            Activities = new List<FestivalActivity>
            {
                new FestivalActivity
                {
                    Id = "plant_flower",
                    Name = "Plant a Festival Flower",
                    Description = "Plant special spring flowers in the festival garden",
                    ParticipationPoints = 15,
                    CooldownMinutes = 30,
                    MaxDaily = 5,
                    Rewards = new List<FestivalReward>
                    {
                        new FestivalReward { Name = "Spring Petal", Description = "A delicate spring petal", ItemType = "consumable", Rarity = "common", XpValue = 10 }
                    }
                },
                new FestivalActivity
                {
                    Id = "catch_butterfly",
                    Name = "Butterfly Catching",
                    Description = "Catch beautiful spring butterflies",
                    ParticipationPoints = 20,
                    CooldownMinutes = 45,
                    MaxDaily = 3,
                    Rewards = new List<FestivalReward>
                    {
                        new FestivalReward { Name = "Butterfly Wing", Description = "A shimmering butterfly wing", ItemType = "material", Rarity = "uncommon", XpValue = 20 }
                    }
                },
                new FestivalActivity
                {
                    Id = "flower_crown",
                    Name = "Make a Flower Crown",
                    Description = "Craft a beautiful flower crown",
                    ParticipationPoints = 30,
                    CooldownMinutes = 60,
                    MaxDaily = 2,
                    Rewards = new List<FestivalReward>
                    {
                        new FestivalReward { Name = "Flower Crown", Description = "A wearable flower crown", ItemType = "cosmetic", Rarity = "rare", XpValue = 35 }
                    }
                }
            },
            ExclusiveRewards = new List<FestivalReward>
            {
                new FestivalReward { Name = "Spring Duck Costume", Description = "A flowery spring outfit", ItemType = "cosmetic", Rarity = "epic", XpValue = 100 },
                new FestivalReward { Name = "Cherry Blossom Hat", Description = "A hat with cherry blossoms", ItemType = "cosmetic", Rarity = "rare", XpValue = 50 },
                new FestivalReward { Name = "Spring Spirit Badge", Description = "Proof of spring celebration", ItemType = "achievement", Rarity = "legendary", XpValue = 150 }
            },
            Decorations = new List<string> { "cherry_blossoms", "flower_garlands", "butterfly_lights", "spring_banners" },
            SpecialNpc = "Blossom the Spring Fairy Duck"
        },
        
        ["summer_splash"] = new Festival
        {
            Id = "summer_splash",
            Name = "🏖️ Summer Splash Festival",
            Description = "Dive into summer fun with beach activities and water games!",
            Type = FestivalType.SummerSplash,
            StartMonth = 6,
            StartDay = 21,
            DurationDays = 14,
            ThemeColor = "cyan",
            Activities = new List<FestivalActivity>
            {
                new FestivalActivity
                {
                    Id = "build_sandcastle",
                    Name = "Build a Sandcastle",
                    Description = "Create an epic sandcastle on the beach",
                    ParticipationPoints = 20,
                    CooldownMinutes = 45,
                    MaxDaily = 4,
                    Rewards = new List<FestivalReward>
                    {
                        new FestivalReward { Name = "Seashell", Description = "A beautiful seashell", ItemType = "material", Rarity = "common", XpValue = 10 }
                    }
                },
                new FestivalActivity
                {
                    Id = "splash_contest",
                    Name = "Splash Contest",
                    Description = "Compete to make the biggest splash!",
                    ParticipationPoints = 25,
                    CooldownMinutes = 60,
                    MaxDaily = 3,
                    Rewards = new List<FestivalReward>
                    {
                        new FestivalReward { Name = "Splash Trophy", Description = "Winner of the splash contest", ItemType = "decoration", Rarity = "uncommon", XpValue = 25 }
                    }
                },
                new FestivalActivity
                {
                    Id = "sunset_watch",
                    Name = "Watch the Sunset",
                    Description = "Enjoy a beautiful summer sunset",
                    ParticipationPoints = 15,
                    CooldownMinutes = 120,
                    MaxDaily = 1,
                    Rewards = new List<FestivalReward>
                    {
                        new FestivalReward { Name = "Sunset Photo", Description = "A gorgeous sunset photo", ItemType = "keepsake", Rarity = "rare", XpValue = 40 }
                    }
                }
            },
            ExclusiveRewards = new List<FestivalReward>
            {
                new FestivalReward { Name = "Beach Duck Costume", Description = "Tropical summer outfit", ItemType = "cosmetic", Rarity = "epic", XpValue = 100 },
                new FestivalReward { Name = "Surfboard", Description = "A rad surfboard", ItemType = "cosmetic", Rarity = "rare", XpValue = 60 },
                new FestivalReward { Name = "Summer Spirit Badge", Description = "Proof of summer fun", ItemType = "achievement", Rarity = "legendary", XpValue = 150 }
            },
            Decorations = new List<string> { "palm_trees", "beach_umbrellas", "sand_dunes", "wave_decorations" },
            SpecialNpc = "Sunny the Lifeguard Duck"
        },
        
        ["autumn_harvest"] = new Festival
        {
            Id = "autumn_harvest",
            Name = "🍂 Autumn Harvest Festival",
            Description = "Gather the bounty of fall with harvesting, cooking, and cozy activities!",
            Type = FestivalType.AutumnHarvest,
            StartMonth = 9,
            StartDay = 22,
            DurationDays = 14,
            ThemeColor = "orange",
            Activities = new List<FestivalActivity>
            {
                new FestivalActivity
                {
                    Id = "harvest_pumpkin",
                    Name = "Harvest Pumpkins",
                    Description = "Pick the perfect pumpkin from the patch",
                    ParticipationPoints = 20,
                    CooldownMinutes = 40,
                    MaxDaily = 4,
                    Rewards = new List<FestivalReward>
                    {
                        new FestivalReward { Name = "Pumpkin", Description = "A round orange pumpkin", ItemType = "material", Rarity = "common", XpValue = 15 }
                    }
                },
                new FestivalActivity
                {
                    Id = "apple_picking",
                    Name = "Apple Picking",
                    Description = "Pick fresh apples from the orchard",
                    ParticipationPoints = 15,
                    CooldownMinutes = 30,
                    MaxDaily = 5,
                    Rewards = new List<FestivalReward>
                    {
                        new FestivalReward { Name = "Fresh Apple", Description = "A crisp autumn apple", ItemType = "consumable", Rarity = "common", XpValue = 10 }
                    }
                },
                new FestivalActivity
                {
                    Id = "leaf_pile",
                    Name = "Jump in Leaf Pile",
                    Description = "Jump into a colorful pile of autumn leaves!",
                    ParticipationPoints = 10,
                    CooldownMinutes = 20,
                    MaxDaily = 6,
                    Rewards = new List<FestivalReward>
                    {
                        new FestivalReward { Name = "Autumn Leaf", Description = "A colorful fall leaf", ItemType = "material", Rarity = "common", XpValue = 5 }
                    }
                },
                new FestivalActivity
                {
                    Id = "bake_pie",
                    Name = "Bake a Pie",
                    Description = "Bake a delicious autumn pie",
                    ParticipationPoints = 35,
                    CooldownMinutes = 90,
                    MaxDaily = 2,
                    Rewards = new List<FestivalReward>
                    {
                        new FestivalReward { Name = "Homemade Pie", Description = "A delicious homemade pie", ItemType = "consumable", Rarity = "rare", XpValue = 45 }
                    }
                }
            },
            ExclusiveRewards = new List<FestivalReward>
            {
                new FestivalReward { Name = "Scarecrow Costume", Description = "A festive scarecrow outfit", ItemType = "cosmetic", Rarity = "epic", XpValue = 100 },
                new FestivalReward { Name = "Autumn Wreath Hat", Description = "A hat with autumn leaves", ItemType = "cosmetic", Rarity = "rare", XpValue = 55 },
                new FestivalReward { Name = "Harvest Spirit Badge", Description = "Proof of autumn bounty", ItemType = "achievement", Rarity = "legendary", XpValue = 150 }
            },
            Decorations = new List<string> { "hay_bales", "pumpkin_stacks", "corn_stalks", "autumn_garlands" },
            SpecialNpc = "Maple the Farmer Duck"
        },
        
        ["winter_wonder"] = new Festival
        {
            Id = "winter_wonder",
            Name = "❄️ Winter Wonderland Festival",
            Description = "Experience the magic of winter with snow, gifts, and warm gatherings!",
            Type = FestivalType.WinterWonder,
            StartMonth = 12,
            StartDay = 21,
            DurationDays = 14,
            ThemeColor = "white",
            Activities = new List<FestivalActivity>
            {
                new FestivalActivity
                {
                    Id = "build_snowduck",
                    Name = "Build a Snow Duck",
                    Description = "Build a duck-shaped snowman",
                    ParticipationPoints = 25,
                    CooldownMinutes = 45,
                    MaxDaily = 3,
                    Rewards = new List<FestivalReward>
                    {
                        new FestivalReward { Name = "Snowball", Description = "A perfectly packed snowball", ItemType = "material", Rarity = "common", XpValue = 10 }
                    }
                },
                new FestivalActivity
                {
                    Id = "ice_skating",
                    Name = "Ice Skating",
                    Description = "Glide across the frozen pond",
                    ParticipationPoints = 20,
                    CooldownMinutes = 40,
                    MaxDaily = 4,
                    Rewards = new List<FestivalReward>
                    {
                        new FestivalReward { Name = "Ice Crystal", Description = "A sparkling ice crystal", ItemType = "material", Rarity = "uncommon", XpValue = 20 }
                    }
                },
                new FestivalActivity
                {
                    Id = "hot_cocoa",
                    Name = "Sip Hot Cocoa",
                    Description = "Warm up with delicious hot cocoa",
                    ParticipationPoints = 15,
                    CooldownMinutes = 30,
                    MaxDaily = 5,
                    Rewards = new List<FestivalReward>
                    {
                        new FestivalReward { Name = "Warmth", Description = "A cozy feeling inside", ItemType = "buff", Rarity = "common", XpValue = 10 }
                    }
                },
                new FestivalActivity
                {
                    Id = "gift_exchange",
                    Name = "Gift Exchange",
                    Description = "Exchange presents with friends",
                    ParticipationPoints = 40,
                    CooldownMinutes = 120,
                    MaxDaily = 1,
                    Rewards = new List<FestivalReward>
                    {
                        new FestivalReward { Name = "Mystery Gift", Description = "A wrapped mystery present", ItemType = "mystery", Rarity = "rare", XpValue = 50 }
                    }
                }
            },
            ExclusiveRewards = new List<FestivalReward>
            {
                new FestivalReward { Name = "Winter Coat Costume", Description = "A warm festive winter outfit", ItemType = "cosmetic", Rarity = "epic", XpValue = 100 },
                new FestivalReward { Name = "Snowflake Crown", Description = "A crown of eternal snowflakes", ItemType = "cosmetic", Rarity = "rare", XpValue = 65 },
                new FestivalReward { Name = "Winter Spirit Badge", Description = "Proof of winter magic", ItemType = "achievement", Rarity = "legendary", XpValue = 150 }
            },
            Decorations = new List<string> { "snowflakes", "ice_sculptures", "winter_lights", "evergreen_garlands" },
            SpecialNpc = "Frost the Holiday Duck"
        },
        
        ["duck_day"] = new Festival
        {
            Id = "duck_day",
            Name = "🦆 International Duck Day",
            Description = "Celebrate all things duck! The most special day of the year for Cheese!",
            Type = FestivalType.DuckDay,
            StartMonth = 1,
            StartDay = 13,
            DurationDays = 3,
            ThemeColor = "yellow",
            Activities = new List<FestivalActivity>
            {
                new FestivalActivity
                {
                    Id = "quack_parade",
                    Name = "Quack Parade",
                    Description = "Join the grand quacking parade!",
                    ParticipationPoints = 50,
                    CooldownMinutes = 180,
                    MaxDaily = 1,
                    Rewards = new List<FestivalReward>
                    {
                        new FestivalReward { Name = "Parade Flag", Description = "A Duck Day parade flag", ItemType = "decoration", Rarity = "uncommon", XpValue = 30 }
                    }
                },
                new FestivalActivity
                {
                    Id = "duck_dance",
                    Name = "Duck Dance Contest",
                    Description = "Show off your best duck dance moves!",
                    ParticipationPoints = 35,
                    CooldownMinutes = 60,
                    MaxDaily = 3,
                    Rewards = new List<FestivalReward>
                    {
                        new FestivalReward { Name = "Dance Medal", Description = "For excellent dancing", ItemType = "achievement", Rarity = "rare", XpValue = 40 }
                    }
                }
            },
            ExclusiveRewards = new List<FestivalReward>
            {
                new FestivalReward { Name = "Golden Duck Trophy", Description = "The ultimate duck prize", ItemType = "decoration", Rarity = "legendary", XpValue = 200 },
                new FestivalReward { Name = "Duck Crown", Description = "A crown fit for the finest duck", ItemType = "cosmetic", Rarity = "legendary", XpValue = 175 },
                new FestivalReward { Name = "Duck Day Champion Badge", Description = "Champion of Duck Day", ItemType = "achievement", Rarity = "legendary", XpValue = 250 }
            },
            Decorations = new List<string> { "duck_balloons", "golden_streamers", "duck_banners", "confetti" },
            SpecialNpc = "The Grand Quackmaster"
        },
        
        ["love_festival"] = new Festival
        {
            Id = "love_festival",
            Name = "💕 Festival of Love",
            Description = "Celebrate friendship, love, and the bonds we share!",
            Type = FestivalType.LoveFestival,
            StartMonth = 2,
            StartDay = 14,
            DurationDays = 3,
            ThemeColor = "pink",
            Activities = new List<FestivalActivity>
            {
                new FestivalActivity
                {
                    Id = "make_card",
                    Name = "Make a Friendship Card",
                    Description = "Create a card for someone special",
                    ParticipationPoints = 20,
                    CooldownMinutes = 45,
                    MaxDaily = 3,
                    Rewards = new List<FestivalReward>
                    {
                        new FestivalReward { Name = "Friendship Card", Description = "A handmade card full of love", ItemType = "gift", Rarity = "uncommon", XpValue = 20 }
                    }
                },
                new FestivalActivity
                {
                    Id = "share_treat",
                    Name = "Share a Treat",
                    Description = "Share something sweet with a friend",
                    ParticipationPoints = 25,
                    CooldownMinutes = 60,
                    MaxDaily = 2,
                    Rewards = new List<FestivalReward>
                    {
                        new FestivalReward { Name = "Heart Cookie", Description = "A heart-shaped cookie", ItemType = "consumable", Rarity = "rare", XpValue = 30 }
                    }
                }
            },
            ExclusiveRewards = new List<FestivalReward>
            {
                new FestivalReward { Name = "Heart Hat", Description = "A hat covered in hearts", ItemType = "cosmetic", Rarity = "rare", XpValue = 75 },
                new FestivalReward { Name = "Love Spirit Badge", Description = "Spreader of love and friendship", ItemType = "achievement", Rarity = "legendary", XpValue = 125 }
            },
            Decorations = new List<string> { "heart_garlands", "pink_ribbons", "rose_petals", "love_lanterns" },
            SpecialNpc = "Cupid the Love Duck"
        }
    };
    
    /// <summary>
    /// Check if there's an active festival right now.
    /// </summary>
    public Festival? CheckActiveFestival()
    {
        DateTime today = DateTime.Today;
        
        foreach (var festival in Festivals.Values)
        {
            DateTime start = new DateTime(today.Year, festival.StartMonth, festival.StartDay);
            DateTime end = start.AddDays(festival.DurationDays);
            
            // Handle year wraparound
            if (end.Month < start.Month)
                end = end.AddYears(1);
            
            if (today >= start && today <= end)
                return festival;
            
            // Check previous year for festivals that span year boundary
            DateTime startPrev = start.AddYears(-1);
            DateTime endPrev = startPrev.AddDays(festival.DurationDays);
            if (today >= startPrev && today <= endPrev)
                return festival;
        }
        
        return null;
    }
    
    /// <summary>
    /// Start participating in an active festival.
    /// </summary>
    public (bool success, string message) StartFestivalParticipation(Festival festival)
    {
        int currentYear = DateTime.Today.Year;
        
        // Check if already participating this year
        if (CurrentFestivalProgress != null &&
            CurrentFestivalProgress.FestivalId == festival.Id &&
            CurrentFestivalProgress.Year == currentYear)
        {
            return (false, "Already participating in this festival!");
        }
        
        CurrentFestivalProgress = new FestivalProgress
        {
            FestivalId = festival.Id,
            Year = currentYear
        };
        
        TotalFestivalsParticipated++;
        
        return (true, $"🎉 Welcome to the {festival.Name}!");
    }
    
    /// <summary>
    /// Perform a festival activity.
    /// </summary>
    public (bool success, string message, FestivalReward? reward) DoFestivalActivity(string activityId)
    {
        if (CurrentFestivalProgress == null)
            return (false, "Not participating in a festival!", null);
        
        if (!Festivals.TryGetValue(CurrentFestivalProgress.FestivalId, out var festival))
            return (false, "Festival not found!", null);
        
        var activity = festival.Activities.FirstOrDefault(a => a.Id == activityId);
        if (activity == null)
            return (false, "Activity not found!", null);
        
        // Check daily limit
        string today = DateTime.Today.ToString("yyyy-MM-dd");
        if (CurrentFestivalProgress.LastActivityDate != today)
        {
            CurrentFestivalProgress.DailyActivities.Clear();
            CurrentFestivalProgress.LastActivityDate = today;
        }
        
        int dailyCount = CurrentFestivalProgress.DailyActivities.GetValueOrDefault(activityId, 0);
        if (dailyCount >= activity.MaxDaily)
            return (false, $"You've done this activity {activity.MaxDaily} times today!", null);
        
        // Perform activity
        CurrentFestivalProgress.DailyActivities[activityId] = dailyCount + 1;
        CurrentFestivalProgress.ParticipationPoints += activity.ParticipationPoints;
        
        // Track completion
        int totalCompletions = CurrentFestivalProgress.ActivitiesCompleted.GetValueOrDefault(activityId, 0);
        CurrentFestivalProgress.ActivitiesCompleted[activityId] = totalCompletions + 1;
        
        // Get reward
        FestivalReward? reward = activity.Rewards.Any() 
            ? activity.Rewards[_random.Next(activity.Rewards.Count)] 
            : null;
        
        if (reward != null)
        {
            FestivalRewardsCollected.Add(reward.Name);
            return (true, $"🎊 {activity.Name} complete! +{activity.ParticipationPoints} points! Got: {reward.Name}", reward);
        }
        
        return (true, $"🎊 {activity.Name} complete! +{activity.ParticipationPoints} points!", null);
    }
    
    /// <summary>
    /// Claim an exclusive festival reward based on participation points.
    /// </summary>
    public (bool success, string message, FestivalReward? reward) ClaimFestivalReward(int rewardIndex)
    {
        if (CurrentFestivalProgress == null)
            return (false, "Not participating in a festival!", null);
        
        if (!Festivals.TryGetValue(CurrentFestivalProgress.FestivalId, out var festival))
            return (false, "Festival not found!", null);
        
        if (rewardIndex >= festival.ExclusiveRewards.Count)
            return (false, "Invalid reward!", null);
        
        var reward = festival.ExclusiveRewards[rewardIndex];
        
        if (CurrentFestivalProgress.RewardsClaimed.Contains(reward.Name))
            return (false, "Already claimed this reward!", null);
        
        int requiredPoints = (rewardIndex + 1) * 100;
        if (CurrentFestivalProgress.ParticipationPoints < requiredPoints)
            return (false, $"Need {requiredPoints} points! (Have: {CurrentFestivalProgress.ParticipationPoints})", null);
        
        CurrentFestivalProgress.RewardsClaimed.Add(reward.Name);
        FestivalRewardsCollected.Add(reward.Name);
        
        return (true, $"🏆 Claimed: {reward.Name}!", reward);
    }
    
    /// <summary>
    /// End participation in the current festival.
    /// </summary>
    public (bool success, string message, Dictionary<string, object> summary) EndFestival()
    {
        if (CurrentFestivalProgress == null)
            return (false, "Not participating in a festival!", new Dictionary<string, object>());
        
        string festivalId = CurrentFestivalProgress.FestivalId;
        
        if (!FestivalHistory.ContainsKey(festivalId))
            FestivalHistory[festivalId] = new List<FestivalProgress>();
        
        FestivalHistory[festivalId].Add(CurrentFestivalProgress);
        
        // Keep history manageable
        if (FestivalHistory[festivalId].Count > 20)
            FestivalHistory[festivalId] = FestivalHistory[festivalId].TakeLast(20).ToList();
        
        var summary = new Dictionary<string, object>
        {
            ["festival_id"] = festivalId,
            ["points"] = CurrentFestivalProgress.ParticipationPoints,
            ["activities"] = CurrentFestivalProgress.ActivitiesCompleted.Values.Sum(),
            ["rewards"] = CurrentFestivalProgress.RewardsClaimed.Count
        };
        
        CurrentFestivalProgress = null;
        
        return (true, "🎉 Festival participation ended! See you next year!", summary);
    }
    
    /// <summary>
    /// Get current festival participation status.
    /// </summary>
    public Dictionary<string, object>? GetFestivalStatus()
    {
        if (CurrentFestivalProgress == null)
            return null;
        
        if (!Festivals.TryGetValue(CurrentFestivalProgress.FestivalId, out var festival))
            return null;
        
        return new Dictionary<string, object>
        {
            ["festival_name"] = festival.Name,
            ["points"] = CurrentFestivalProgress.ParticipationPoints,
            ["activities_done"] = CurrentFestivalProgress.ActivitiesCompleted,
            ["rewards_claimed"] = CurrentFestivalProgress.RewardsClaimed,
            ["available_rewards"] = festival.ExclusiveRewards.Select((r, i) => new Dictionary<string, object>
            {
                ["name"] = r.Name,
                ["required_points"] = (i + 1) * 100,
                ["claimed"] = CurrentFestivalProgress.RewardsClaimed.Contains(r.Name)
            }).ToList()
        };
    }
    
    /// <summary>
    /// Render the festival interface.
    /// </summary>
    public List<string> RenderFestivalScreen()
    {
        var active = CheckActiveFestival();
        
        if (active == null)
        {
            return new List<string>
            {
                "╔═══════════════════════════════════════════════╗",
                "║            🎪 FESTIVALS 🎪                    ║",
                "╠═══════════════════════════════════════════════╣",
                "║                                               ║",
                "║       No festival is currently active.        ║",
                "║                                               ║",
                "║    Check back during seasonal celebrations!   ║",
                "║                                               ║",
                $"║    Festivals participated: {TotalFestivalsParticipated,3}               ║",
                "║                                               ║",
                "╚═══════════════════════════════════════════════╝"
            };
        }
        
        var lines = new List<string>
        {
            "╔═══════════════════════════════════════════════╗",
            $"║  {active.Name,-41}  ║",
            "╠═══════════════════════════════════════════════╣"
        };
        
        string desc = active.Description.Length > 40 ? active.Description.Substring(0, 40) : active.Description;
        lines.Add($"║  {desc,-43}  ║");
        lines.Add("║                                               ║");
        
        if (CurrentFestivalProgress != null)
        {
            int points = CurrentFestivalProgress.ParticipationPoints;
            lines.Add($"║  🌟 Participation Points: {points,5}              ║");
            lines.Add("╠═══════════════════════════════════════════════╣");
            lines.Add("║  ACTIVITIES:                                  ║");
            
            foreach (var activity in active.Activities.Take(4))
            {
                int done = CurrentFestivalProgress.ActivitiesCompleted.GetValueOrDefault(activity.Id, 0);
                int daily = CurrentFestivalProgress.DailyActivities.GetValueOrDefault(activity.Id, 0);
                string actName = activity.Name.Length > 25 ? activity.Name.Substring(0, 25) : activity.Name;
                lines.Add($"║   • {actName,-25} [{daily}/{activity.MaxDaily}]   ║");
            }
            
            lines.Add("╠═══════════════════════════════════════════════╣");
            lines.Add("║  REWARDS:                                     ║");
            
            foreach (var (reward, i) in active.ExclusiveRewards.Take(3).Select((r, i) => (r, i)))
            {
                int req = (i + 1) * 100;
                string claimed = CurrentFestivalProgress.RewardsClaimed.Contains(reward.Name) ? "✓" : "○";
                string rewName = reward.Name.Length > 25 ? reward.Name.Substring(0, 25) : reward.Name;
                lines.Add($"║   {claimed} {rewName,-25} ({req}pts)  ║");
            }
        }
        else
        {
            lines.Add("║                                               ║");
            lines.Add("║     Press [J]oin to participate!              ║");
            lines.Add("║                                               ║");
        }
        
        lines.Add("╚═══════════════════════════════════════════════╝");
        
        return lines;
    }
    
    /// <summary>
    /// Get list of upcoming festivals and days until they start.
    /// </summary>
    public List<(string name, int daysUntil)> GetUpcomingFestivals()
    {
        DateTime today = DateTime.Today;
        var upcoming = new List<(string, int)>();
        
        foreach (var festival in Festivals.Values)
        {
            DateTime start = new DateTime(today.Year, festival.StartMonth, festival.StartDay);
            
            if (start < today)
                start = start.AddYears(1);
            
            int daysUntil = (start - today).Days;
            upcoming.Add((festival.Name, daysUntil));
        }
        
        return upcoming.OrderBy(x => x.Item2).ToList();
    }
    
    /// <summary>
    /// Convert to save data.
    /// </summary>
    public Dictionary<string, object?> ToSaveData()
    {
        return new Dictionary<string, object?>
        {
            ["festival_history"] = FestivalHistory.ToDictionary(
                kvp => kvp.Key,
                kvp => kvp.Value.Select(p => new Dictionary<string, object?>
                {
                    ["festival_id"] = p.FestivalId,
                    ["year"] = p.Year,
                    ["participation_points"] = p.ParticipationPoints,
                    ["activities_completed"] = p.ActivitiesCompleted,
                    ["rewards_claimed"] = p.RewardsClaimed,
                    ["daily_activities"] = p.DailyActivities,
                    ["last_activity_date"] = p.LastActivityDate
                }).ToList() as object
            ),
            ["current_festival_progress"] = CurrentFestivalProgress != null ? new Dictionary<string, object?>
            {
                ["festival_id"] = CurrentFestivalProgress.FestivalId,
                ["year"] = CurrentFestivalProgress.Year,
                ["participation_points"] = CurrentFestivalProgress.ParticipationPoints,
                ["activities_completed"] = CurrentFestivalProgress.ActivitiesCompleted,
                ["rewards_claimed"] = CurrentFestivalProgress.RewardsClaimed,
                ["daily_activities"] = CurrentFestivalProgress.DailyActivities,
                ["last_activity_date"] = CurrentFestivalProgress.LastActivityDate
            } : null,
            ["total_festivals_participated"] = TotalFestivalsParticipated,
            ["festival_rewards_collected"] = FestivalRewardsCollected,
            ["favorite_festival"] = FavoriteFestival,
            ["last_festival_check"] = LastFestivalCheck
        };
    }
    
    /// <summary>
    /// Load from save data.
    /// </summary>
    public static FestivalSystem FromSaveData(Dictionary<string, JsonElement> data)
    {
        var system = new FestivalSystem();
        
        if (data.TryGetValue("festival_history", out var histEl) && histEl.ValueKind == JsonValueKind.Object)
        {
            foreach (var prop in histEl.EnumerateObject())
            {
                if (prop.Value.ValueKind == JsonValueKind.Array)
                {
                    system.FestivalHistory[prop.Name] = prop.Value.EnumerateArray().Select(pEl =>
                    {
                        var progress = new FestivalProgress
                        {
                            FestivalId = pEl.TryGetProperty("festival_id", out var fidEl) ? fidEl.GetString() ?? "" : "",
                            Year = pEl.TryGetProperty("year", out var yearEl) ? yearEl.GetInt32() : 0,
                            ParticipationPoints = pEl.TryGetProperty("participation_points", out var ppEl) ? ppEl.GetInt32() : 0,
                            LastActivityDate = pEl.TryGetProperty("last_activity_date", out var ladEl) ? ladEl.GetString() ?? "" : ""
                        };
                        
                        if (pEl.TryGetProperty("activities_completed", out var acEl) && acEl.ValueKind == JsonValueKind.Object)
                        {
                            foreach (var acProp in acEl.EnumerateObject())
                                progress.ActivitiesCompleted[acProp.Name] = acProp.Value.GetInt32();
                        }
                        
                        if (pEl.TryGetProperty("rewards_claimed", out var rcEl) && rcEl.ValueKind == JsonValueKind.Array)
                            progress.RewardsClaimed = rcEl.EnumerateArray().Select(e => e.GetString() ?? "").ToList();
                        
                        if (pEl.TryGetProperty("daily_activities", out var daEl) && daEl.ValueKind == JsonValueKind.Object)
                        {
                            foreach (var daProp in daEl.EnumerateObject())
                                progress.DailyActivities[daProp.Name] = daProp.Value.GetInt32();
                        }
                        
                        return progress;
                    }).ToList();
                }
            }
        }
        
        if (data.TryGetValue("current_festival_progress", out var curEl) && curEl.ValueKind == JsonValueKind.Object)
        {
            system.CurrentFestivalProgress = new FestivalProgress
            {
                FestivalId = curEl.TryGetProperty("festival_id", out var fidEl) ? fidEl.GetString() ?? "" : "",
                Year = curEl.TryGetProperty("year", out var yearEl) ? yearEl.GetInt32() : 0,
                ParticipationPoints = curEl.TryGetProperty("participation_points", out var ppEl) ? ppEl.GetInt32() : 0,
                LastActivityDate = curEl.TryGetProperty("last_activity_date", out var ladEl) ? ladEl.GetString() ?? "" : ""
            };
            
            if (curEl.TryGetProperty("activities_completed", out var acEl) && acEl.ValueKind == JsonValueKind.Object)
            {
                foreach (var prop in acEl.EnumerateObject())
                    system.CurrentFestivalProgress.ActivitiesCompleted[prop.Name] = prop.Value.GetInt32();
            }
            
            if (curEl.TryGetProperty("rewards_claimed", out var rcEl) && rcEl.ValueKind == JsonValueKind.Array)
                system.CurrentFestivalProgress.RewardsClaimed = rcEl.EnumerateArray().Select(e => e.GetString() ?? "").ToList();
            
            if (curEl.TryGetProperty("daily_activities", out var daEl) && daEl.ValueKind == JsonValueKind.Object)
            {
                foreach (var prop in daEl.EnumerateObject())
                    system.CurrentFestivalProgress.DailyActivities[prop.Name] = prop.Value.GetInt32();
            }
        }
        
        if (data.TryGetValue("total_festivals_participated", out var totalEl))
            system.TotalFestivalsParticipated = totalEl.GetInt32();
        
        if (data.TryGetValue("festival_rewards_collected", out var rewEl) && rewEl.ValueKind == JsonValueKind.Array)
            system.FestivalRewardsCollected = rewEl.EnumerateArray().Select(e => e.GetString() ?? "").ToList();
        
        if (data.TryGetValue("favorite_festival", out var favEl) && favEl.ValueKind == JsonValueKind.String)
            system.FavoriteFestival = favEl.GetString();
        
        if (data.TryGetValue("last_festival_check", out var lfcEl) && lfcEl.ValueKind == JsonValueKind.String)
            system.LastFestivalCheck = lfcEl.GetString() ?? "";
        
        return system;
    }
}
