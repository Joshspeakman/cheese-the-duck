using System;
using System.Collections.Generic;
using System.Linq;

namespace StupidDuck.World;

/// <summary>
/// Rarity tiers for fish.
/// </summary>
public enum FishRarity
{
    Common,
    Uncommon,
    Rare,
    Epic,
    Legendary,
    Mythical
}

/// <summary>
/// Different locations to fish.
/// </summary>
public enum FishingSpot
{
    Pond,
    River,
    Lake,
    Ocean,
    SecretCove
}

/// <summary>
/// Types of bait that affect catch rates.
/// </summary>
public enum BaitType
{
    Bread,
    Worms,
    Seeds,
    Special,
    Golden
}

/// <summary>
/// A type of fish that can be caught.
/// </summary>
public class Fish
{
    public string Id { get; set; } = "";
    public string Name { get; set; } = "";
    public string Description { get; set; } = "";
    public FishRarity Rarity { get; set; }
    public float MinSize { get; set; }
    public float MaxSize { get; set; }
    public float BaseCatchRate { get; set; }
    public List<FishingSpot> Spots { get; set; } = new();
    public List<BaitType> PreferredBait { get; set; } = new();
    public List<string> TimeOfDay { get; set; } = new() { "any" };
    public List<string> Season { get; set; } = new() { "any" };
    public string AsciiArt { get; set; } = "><>";
    public int XpValue { get; set; }
    public int CoinValue { get; set; }
    public string FunFact { get; set; } = "";
}

/// <summary>
/// A specific fish that was caught.
/// </summary>
public class CaughtFish
{
    public string FishId { get; set; } = "";
    public float Size { get; set; }
    public DateTime CaughtAt { get; set; }
    public FishingSpot Spot { get; set; }
    public BaitType BaitUsed { get; set; }
    public bool IsRecord { get; set; }
}

/// <summary>
/// Information about a fishing spot.
/// </summary>
public class FishingSpotInfo
{
    public string Name { get; set; } = "";
    public string Description { get; set; } = "";
    public int UnlockLevel { get; set; }
    public int Difficulty { get; set; }
    public List<string> Ascii { get; set; } = new();
}

/// <summary>
/// Fishing minigame state and logic.
/// </summary>
public class FishingSystem
{
    // =============================================================================
    // FISH DATABASE
    // =============================================================================

    public static readonly Dictionary<string, Fish> AllFish = new()
    {
        // === COMMON ===
        ["minnow"] = new()
        {
            Id = "minnow",
            Name = "Minnow",
            Description = "A tiny, quick little fish. Good for beginners!",
            Rarity = FishRarity.Common,
            MinSize = 2.0f, MaxSize = 5.0f,
            BaseCatchRate = 0.8f,
            Spots = new() { FishingSpot.Pond, FishingSpot.River, FishingSpot.Lake },
            PreferredBait = new() { BaitType.Bread },
            AsciiArt = "><>",
            XpValue = 5, CoinValue = 2,
            FunFact = "Minnows travel in schools for protection!"
        },
        ["goldfish"] = new()
        {
            Id = "goldfish",
            Name = "Goldfish",
            Description = "A pretty golden fish that sparkles in the sun!",
            Rarity = FishRarity.Common,
            MinSize = 5.0f, MaxSize = 15.0f,
            BaseCatchRate = 0.7f,
            Spots = new() { FishingSpot.Pond, FishingSpot.Lake },
            PreferredBait = new() { BaitType.Bread, BaitType.Seeds },
            TimeOfDay = new() { "morning", "afternoon" },
            AsciiArt = "<º)))><",
            XpValue = 8, CoinValue = 5,
            FunFact = "Goldfish can recognize their owners!"
        },
        ["carp"] = new()
        {
            Id = "carp",
            Name = "Carp",
            Description = "A chunky, reliable fish. Great for learning!",
            Rarity = FishRarity.Common,
            MinSize = 20.0f, MaxSize = 50.0f,
            BaseCatchRate = 0.6f,
            Spots = new() { FishingSpot.River, FishingSpot.Lake },
            PreferredBait = new() { BaitType.Worms },
            AsciiArt = "><(((('>",
            XpValue = 10, CoinValue = 8,
            FunFact = "Carp can live for over 20 years!"
        },
        // === UNCOMMON ===
        ["bass"] = new()
        {
            Id = "bass",
            Name = "Bass",
            Description = "A feisty fish that puts up a good fight!",
            Rarity = FishRarity.Uncommon,
            MinSize = 25.0f, MaxSize = 60.0f,
            BaseCatchRate = 0.5f,
            Spots = new() { FishingSpot.Lake, FishingSpot.River },
            PreferredBait = new() { BaitType.Worms },
            TimeOfDay = new() { "morning", "evening" },
            Season = new() { "spring", "summer", "fall" },
            AsciiArt = "><(((º>",
            XpValue = 20, CoinValue = 15,
            FunFact = "Bass are ambush predators!"
        },
        ["catfish"] = new()
        {
            Id = "catfish",
            Name = "Catfish",
            Description = "A whiskered bottom-dweller. Very chill!",
            Rarity = FishRarity.Uncommon,
            MinSize = 30.0f, MaxSize = 80.0f,
            BaseCatchRate = 0.45f,
            Spots = new() { FishingSpot.River, FishingSpot.Lake },
            PreferredBait = new() { BaitType.Worms, BaitType.Special },
            TimeOfDay = new() { "night", "evening" },
            AsciiArt = "=<º))))><",
            XpValue = 25, CoinValue = 20,
            FunFact = "Catfish can taste with their entire body!"
        },
        ["trout"] = new()
        {
            Id = "trout",
            Name = "Rainbow Trout",
            Description = "Beautiful and colorful! A prized catch!",
            Rarity = FishRarity.Uncommon,
            MinSize = 20.0f, MaxSize = 50.0f,
            BaseCatchRate = 0.4f,
            Spots = new() { FishingSpot.River },
            PreferredBait = new() { BaitType.Worms, BaitType.Special },
            TimeOfDay = new() { "morning" },
            Season = new() { "spring", "summer" },
            AsciiArt = "🌈><º>",
            XpValue = 30, CoinValue = 25,
            FunFact = "Rainbow trout can leap 3 feet out of water!"
        },
        // === RARE ===
        ["koi"] = new()
        {
            Id = "koi",
            Name = "Koi Fish",
            Description = "An elegant, colorful fish. Symbol of luck!",
            Rarity = FishRarity.Rare,
            MinSize = 30.0f, MaxSize = 70.0f,
            BaseCatchRate = 0.25f,
            Spots = new() { FishingSpot.Pond, FishingSpot.SecretCove },
            PreferredBait = new() { BaitType.Special },
            TimeOfDay = new() { "morning", "evening" },
            Season = new() { "spring", "summer" },
            AsciiArt = "🎏><º)))><",
            XpValue = 50, CoinValue = 50,
            FunFact = "Koi can live for over 200 years!"
        },
        ["salmon"] = new()
        {
            Id = "salmon",
            Name = "Salmon",
            Description = "A powerful swimmer! Swims upstream!",
            Rarity = FishRarity.Rare,
            MinSize = 50.0f, MaxSize = 100.0f,
            BaseCatchRate = 0.3f,
            Spots = new() { FishingSpot.River, FishingSpot.Ocean },
            PreferredBait = new() { BaitType.Worms, BaitType.Special },
            TimeOfDay = new() { "morning", "evening" },
            Season = new() { "fall" },
            AsciiArt = "<º)))>><",
            XpValue = 60, CoinValue = 60,
            FunFact = "Salmon return to where they were born to spawn!"
        },
        ["pufferfish"] = new()
        {
            Id = "pufferfish",
            Name = "Pufferfish",
            Description = "Round and spiky! Puffs up when scared!",
            Rarity = FishRarity.Rare,
            MinSize = 10.0f, MaxSize = 30.0f,
            BaseCatchRate = 0.2f,
            Spots = new() { FishingSpot.Ocean, FishingSpot.SecretCove },
            PreferredBait = new() { BaitType.Special },
            Season = new() { "summer" },
            AsciiArt = "<(°o°)>",
            XpValue = 70, CoinValue = 70,
            FunFact = "Pufferfish are one of the most poisonous vertebrates!"
        },
        // === EPIC ===
        ["swordfish"] = new()
        {
            Id = "swordfish",
            Name = "Swordfish",
            Description = "A majestic fish with a sword-like snout!",
            Rarity = FishRarity.Epic,
            MinSize = 100.0f, MaxSize = 300.0f,
            BaseCatchRate = 0.1f,
            Spots = new() { FishingSpot.Ocean },
            PreferredBait = new() { BaitType.Special, BaitType.Golden },
            TimeOfDay = new() { "morning", "evening" },
            Season = new() { "summer", "fall" },
            AsciiArt = "=======>°>",
            XpValue = 150, CoinValue = 150,
            FunFact = "Swordfish can swim up to 60 mph!"
        },
        ["sturgeon"] = new()
        {
            Id = "sturgeon",
            Name = "Sturgeon",
            Description = "An ancient fish, living fossil!",
            Rarity = FishRarity.Epic,
            MinSize = 100.0f, MaxSize = 400.0f,
            BaseCatchRate = 0.08f,
            Spots = new() { FishingSpot.River, FishingSpot.Lake },
            PreferredBait = new() { BaitType.Special, BaitType.Golden },
            TimeOfDay = new() { "night" },
            AsciiArt = "<º≈≈≈≈))))><",
            XpValue = 200, CoinValue = 200,
            FunFact = "Sturgeon can live for over 100 years!"
        },
        // === LEGENDARY ===
        ["golden_koi"] = new()
        {
            Id = "golden_koi",
            Name = "Golden Koi",
            Description = "A mythical golden koi! Extremely rare!",
            Rarity = FishRarity.Legendary,
            MinSize = 50.0f, MaxSize = 100.0f,
            BaseCatchRate = 0.03f,
            Spots = new() { FishingSpot.SecretCove },
            PreferredBait = new() { BaitType.Golden },
            TimeOfDay = new() { "morning" },
            Season = new() { "spring" },
            AsciiArt = "✨><(((°>✨",
            XpValue = 500, CoinValue = 500,
            FunFact = "Legend says seeing a golden koi brings 100 years of luck!"
        },
        ["ghost_fish"] = new()
        {
            Id = "ghost_fish",
            Name = "Ghost Fish",
            Description = "A translucent, ethereal fish from the deep!",
            Rarity = FishRarity.Legendary,
            MinSize = 20.0f, MaxSize = 50.0f,
            BaseCatchRate = 0.02f,
            Spots = new() { FishingSpot.SecretCove, FishingSpot.Lake },
            PreferredBait = new() { BaitType.Golden },
            TimeOfDay = new() { "night" },
            Season = new() { "winter" },
            AsciiArt = "👻><°>👻",
            XpValue = 600, CoinValue = 600,
            FunFact = "Ghost fish can only be seen under moonlight!"
        },
        // === MYTHICAL ===
        ["ancient_dragon_fish"] = new()
        {
            Id = "ancient_dragon_fish",
            Name = "Ancient Dragon Fish",
            Description = "THE legendary fish of myth! Said to grant wishes!",
            Rarity = FishRarity.Mythical,
            MinSize = 200.0f, MaxSize = 500.0f,
            BaseCatchRate = 0.005f,
            Spots = new() { FishingSpot.SecretCove },
            PreferredBait = new() { BaitType.Golden },
            TimeOfDay = new() { "night" },
            AsciiArt = "🐉><(((((º>🐉",
            XpValue = 2000, CoinValue = 2000,
            FunFact = "Only the most patient and skilled fishers ever see this fish!"
        }
    };

    public static readonly Dictionary<FishingSpot, FishingSpotInfo> SpotInfo = new()
    {
        [FishingSpot.Pond] = new()
        {
            Name = "Peaceful Pond",
            Description = "A quiet, serene pond perfect for beginners.",
            UnlockLevel = 1, Difficulty = 1,
            Ascii = new() { "  ~~~~~~~~~~~  ", " ~~~~~~~~~~~~~ ", "~~~~~~~~~~~~~~~" }
        },
        [FishingSpot.River] = new()
        {
            Name = "Rushing River",
            Description = "A flowing river with diverse fish!",
            UnlockLevel = 3, Difficulty = 2,
            Ascii = new() { "≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈", "≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈" }
        },
        [FishingSpot.Lake] = new()
        {
            Name = "Crystal Lake",
            Description = "A large, clear lake with big fish!",
            UnlockLevel = 5, Difficulty = 3,
            Ascii = new() { "   ~~~~~~~~~~   ", "  ~~~~~~~~~~~~  ", "~~~~~~~~~~~~~~~~" }
        },
        [FishingSpot.Ocean] = new()
        {
            Name = "Deep Ocean",
            Description = "The vast ocean. Who knows what lurks below?",
            UnlockLevel = 8, Difficulty = 4,
            Ascii = new() { "≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋", "≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋" }
        },
        [FishingSpot.SecretCove] = new()
        {
            Name = "Secret Cove",
            Description = "A hidden spot with legendary fish...",
            UnlockLevel = 12, Difficulty = 5,
            Ascii = new() { "  ✨~~~~~✨  ", " ~~~~~~~~~~~ ", "~~~~~~~~~~~~~" }
        }
    };

    // =============================================================================
    // STATE
    // =============================================================================

    public FishingSpot? CurrentSpot { get; set; }
    public BaitType CurrentBait { get; set; } = BaitType.Bread;
    public bool IsFishing { get; set; }
    public bool WaitingForBite { get; set; }
    public float BiteTimer { get; set; }
    public float ReactionWindow { get; set; }
    public string? HookedFish { get; set; }
    public int AnimationFrame { get; set; }
    public DateTime CastTime { get; set; }

    // Player stats
    public Dictionary<string, List<CaughtFish>> FishCaught { get; set; } = new();
    public int TotalCatches { get; set; }
    public CaughtFish? BiggestCatch { get; set; }
    public Dictionary<string, float> FishRecords { get; set; } = new();
    public List<FishingSpot> UnlockedSpots { get; set; } = new() { FishingSpot.Pond };
    public Dictionary<BaitType, int> BaitInventory { get; set; } = new()
    {
        [BaitType.Bread] = 10,
        [BaitType.Worms] = 0,
        [BaitType.Seeds] = 5,
        [BaitType.Special] = 0,
        [BaitType.Golden] = 0
    };

    private static readonly Random _random = new();

    // =============================================================================
    // FISHING ACTIONS
    // =============================================================================

    public (bool Success, string Message) StartFishing(FishingSpot spot)
    {
        if (!UnlockedSpots.Contains(spot))
            return (false, $"You haven't unlocked {SpotInfo[spot].Name} yet!");

        if (BaitInventory.GetValueOrDefault(CurrentBait) <= 0)
            return (false, $"You're out of {CurrentBait}!");

        CurrentSpot = spot;
        IsFishing = true;
        WaitingForBite = true;
        BiteTimer = 3.0f + (float)_random.NextDouble() * 7.0f;
        CastTime = DateTime.UtcNow;
        HookedFish = null;

        BaitInventory[CurrentBait]--;

        return (true, $"Casting line at {SpotInfo[spot].Name}... 🎣");
    }

    public string? Update(float deltaTime)
    {
        if (!IsFishing)
            return null;

        AnimationFrame = (AnimationFrame + 1) % 4;

        if (WaitingForBite)
        {
            BiteTimer -= deltaTime;

            if (BiteTimer <= 0)
            {
                var fish = SelectFish();
                if (fish != null)
                {
                    HookedFish = fish.Id;
                    WaitingForBite = false;
                    ReactionWindow = 2.0f;
                    return "❗ BITE! Press SPACE to reel in! ❗";
                }
                else
                {
                    BiteTimer = 3.0f + (float)_random.NextDouble() * 5.0f;
                }
            }
        }
        else
        {
            ReactionWindow -= deltaTime;
            if (ReactionWindow <= 0)
            {
                HookedFish = null;
                IsFishing = false;
                return "The fish got away! 😢";
            }
        }

        return null;
    }

    public (bool Success, string Message, CaughtFish? Caught) ReelIn()
    {
        if (HookedFish == null)
            return (false, "No fish on the line!", null);

        if (!AllFish.TryGetValue(HookedFish, out var fish))
        {
            IsFishing = false;
            return (false, "The fish escaped!", null);
        }

        var difficulty = CurrentSpot.HasValue && SpotInfo.TryGetValue(CurrentSpot.Value, out var spotInfo)
            ? spotInfo.Difficulty : 1;
        var baseSuccess = fish.BaseCatchRate;

        // Bait bonus
        if (fish.PreferredBait.Contains(CurrentBait))
            baseSuccess *= 1.5f;

        // Difficulty modifier
        baseSuccess /= (difficulty * 0.5f);

        if (_random.NextDouble() < Math.Min(0.95, baseSuccess))
        {
            // Caught it!
            var size = (float)Math.Round(fish.MinSize + _random.NextDouble() * (fish.MaxSize - fish.MinSize), 1);
            var isRecord = size > FishRecords.GetValueOrDefault(fish.Id);

            if (isRecord)
                FishRecords[fish.Id] = size;

            var caught = new CaughtFish
            {
                FishId = fish.Id,
                Size = size,
                CaughtAt = DateTime.UtcNow,
                Spot = CurrentSpot ?? FishingSpot.Pond,
                BaitUsed = CurrentBait,
                IsRecord = isRecord
            };

            if (!FishCaught.ContainsKey(fish.Id))
                FishCaught[fish.Id] = new();
            FishCaught[fish.Id].Add(caught);
            TotalCatches++;

            if (BiggestCatch == null || size > BiggestCatch.Size)
                BiggestCatch = caught;

            IsFishing = false;
            HookedFish = null;

            var recordText = isRecord ? " 🏆 NEW RECORD!" : "";
            return (true, $"Caught a {fish.Name}! {size}cm!{recordText} {fish.AsciiArt}", caught);
        }
        else
        {
            IsFishing = false;
            HookedFish = null;
            return (false, $"The {fish.Name} got away... 😢", null);
        }
    }

    private Fish? SelectFish()
    {
        if (!CurrentSpot.HasValue)
            return null;

        // Get current time of day
        var hour = DateTime.Now.Hour;
        string timeOfDay;
        if (hour >= 5 && hour < 12)
            timeOfDay = "morning";
        else if (hour >= 12 && hour < 17)
            timeOfDay = "afternoon";
        else if (hour >= 17 && hour < 21)
            timeOfDay = "evening";
        else
            timeOfDay = "night";

        // Get current season
        var month = DateTime.Now.Month;
        string season;
        if (month >= 3 && month <= 5)
            season = "spring";
        else if (month >= 6 && month <= 8)
            season = "summer";
        else if (month >= 9 && month <= 11)
            season = "fall";
        else
            season = "winter";

        // Filter available fish
        var available = new List<Fish>();
        foreach (var fish in AllFish.Values)
        {
            if (!fish.Spots.Contains(CurrentSpot.Value))
                continue;
            if (!fish.TimeOfDay.Contains("any") && !fish.TimeOfDay.Contains(timeOfDay))
                continue;
            if (!fish.Season.Contains("any") && !fish.Season.Contains(season))
                continue;

            var weight = fish.BaseCatchRate;
            if (fish.PreferredBait.Contains(CurrentBait))
                weight *= 2;

            for (var i = 0; i < (int)(weight * 100); i++)
                available.Add(fish);
        }

        if (!available.Any())
            return AllFish.Values.First();

        return available[_random.Next(available.Count)];
    }

    public void CancelFishing()
    {
        IsFishing = false;
        WaitingForBite = false;
        HookedFish = null;
    }

    public void UnlockSpot(FishingSpot spot)
    {
        if (!UnlockedSpots.Contains(spot))
            UnlockedSpots.Add(spot);
    }

    public void AddBait(BaitType baitType, int amount)
    {
        BaitInventory[baitType] = BaitInventory.GetValueOrDefault(baitType) + amount;
    }

    public FishingStats GetCollectionStats()
    {
        var byRarity = new Dictionary<FishRarity, int>();
        foreach (var fishId in FishCaught.Keys)
        {
            if (AllFish.TryGetValue(fishId, out var fish))
            {
                byRarity[fish.Rarity] = byRarity.GetValueOrDefault(fish.Rarity) + 1;
            }
        }

        return new FishingStats
        {
            TotalSpecies = AllFish.Count,
            CaughtSpecies = FishCaught.Count,
            CompletionPercent = Math.Round((float)FishCaught.Count / AllFish.Count * 100, 1),
            TotalCatches = TotalCatches,
            ByRarity = byRarity,
            BiggestCatch = BiggestCatch
        };
    }

    // =============================================================================
    // SERIALIZATION
    // =============================================================================

    public FishingSaveData ToSaveData() => new()
    {
        FishCaught = FishCaught.ToDictionary(
            kvp => kvp.Key,
            kvp => kvp.Value.Select(c => new CaughtFishSaveData
            {
                FishId = c.FishId,
                Size = c.Size,
                CaughtAt = c.CaughtAt.ToString("o"),
                Spot = c.Spot.ToString(),
                BaitUsed = c.BaitUsed.ToString(),
                IsRecord = c.IsRecord
            }).ToList()),
        TotalCatches = TotalCatches,
        FishRecords = FishRecords,
        UnlockedSpots = UnlockedSpots.Select(s => s.ToString()).ToList(),
        BaitInventory = BaitInventory.ToDictionary(kvp => kvp.Key.ToString(), kvp => kvp.Value)
    };

    public static FishingSystem FromSaveData(FishingSaveData data)
    {
        var system = new FishingSystem
        {
            TotalCatches = data.TotalCatches,
            FishRecords = data.FishRecords ?? new()
        };

        if (data.UnlockedSpots != null)
        {
            system.UnlockedSpots = data.UnlockedSpots
                .Where(s => Enum.TryParse<FishingSpot>(s, out _))
                .Select(s => Enum.Parse<FishingSpot>(s))
                .ToList();
        }

        if (data.BaitInventory != null)
        {
            foreach (var (key, value) in data.BaitInventory)
            {
                if (Enum.TryParse<BaitType>(key, out var bait))
                    system.BaitInventory[bait] = value;
            }
        }

        if (data.FishCaught != null)
        {
            foreach (var (fishId, catches) in data.FishCaught)
            {
                system.FishCaught[fishId] = catches.Select(c =>
                {
                    Enum.TryParse<FishingSpot>(c.Spot, out var spot);
                    Enum.TryParse<BaitType>(c.BaitUsed, out var bait);
                    DateTime.TryParse(c.CaughtAt, out var caught);

                    return new CaughtFish
                    {
                        FishId = c.FishId ?? fishId,
                        Size = c.Size,
                        CaughtAt = caught,
                        Spot = spot,
                        BaitUsed = bait,
                        IsRecord = c.IsRecord
                    };
                }).ToList();
            }
        }

        return system;
    }
}

public class FishingStats
{
    public int TotalSpecies { get; set; }
    public int CaughtSpecies { get; set; }
    public double CompletionPercent { get; set; }
    public int TotalCatches { get; set; }
    public Dictionary<FishRarity, int> ByRarity { get; set; } = new();
    public CaughtFish? BiggestCatch { get; set; }
}

public class CaughtFishSaveData
{
    public string? FishId { get; set; }
    public float Size { get; set; }
    public string? CaughtAt { get; set; }
    public string? Spot { get; set; }
    public string? BaitUsed { get; set; }
    public bool IsRecord { get; set; }
}

public class FishingSaveData
{
    public Dictionary<string, List<CaughtFishSaveData>>? FishCaught { get; set; }
    public int TotalCatches { get; set; }
    public Dictionary<string, float>? FishRecords { get; set; }
    public List<string>? UnlockedSpots { get; set; }
    public Dictionary<string, int>? BaitInventory { get; set; }
}
