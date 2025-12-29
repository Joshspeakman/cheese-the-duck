namespace StupidDuck.Core;

/// <summary>
/// Game configuration and constants for Cheese the Duck.
/// </summary>
public static class GameConfig
{
    // Paths
    public static string GameDir => AppDomain.CurrentDomain.BaseDirectory;
    public static string DataDir => Path.Combine(GameDir, "data");
    public static string SaveDir => Path.Combine(
        Environment.GetFolderPath(Environment.SpecialFolder.UserProfile),
        ".cheese_the_duck"
    );
    public static string SaveFile => Path.Combine(SaveDir, "save.json");

    // Default duck name
    public const string DefaultDuckName = "Cheese";

    // Game timing
    public const int Fps = 30;
    public const float TickRate = 1.0f;  // Seconds between game ticks
    public const float TimeMultiplier = 1.0f;  // Speed up time for testing

    // Need decay rates (per real minute)
    public static readonly Dictionary<string, float> NeedDecayRates = new()
    {
        ["hunger"] = 0.8f,
        ["energy"] = 0.5f,
        ["fun"] = 1.0f,
        ["cleanliness"] = 0.3f,
        ["social"] = 0.6f
    };

    // Need thresholds
    public const float NeedMax = 100f;
    public const float NeedMin = 0f;
    public const float NeedCritical = 20f;
    public const float NeedLow = 40f;

    // Interaction effects
    public static readonly Dictionary<string, Dictionary<string, float>> InteractionEffects = new()
    {
        ["feed"] = new() { ["hunger"] = 35, ["fun"] = 5 },
        ["play"] = new() { ["fun"] = 30, ["energy"] = -10, ["social"] = 10 },
        ["clean"] = new() { ["cleanliness"] = 40, ["fun"] = -5 },
        ["pet"] = new() { ["social"] = 25, ["fun"] = 10 },
        ["sleep"] = new() { ["energy"] = 50, ["hunger"] = -5 }
    };

    // Mood thresholds (based on weighted need average)
    public static readonly Dictionary<string, float> MoodThresholds = new()
    {
        ["ecstatic"] = 90f,
        ["happy"] = 70f,
        ["content"] = 50f,
        ["grumpy"] = 30f,
        ["sad"] = 10f,
        ["miserable"] = 0f
    };

    // Mood weights for need calculation
    public static readonly Dictionary<string, float> MoodWeights = new()
    {
        ["hunger"] = 0.25f,
        ["energy"] = 0.25f,
        ["fun"] = 0.20f,
        ["cleanliness"] = 0.15f,
        ["social"] = 0.15f
    };

    // Growth stages (duration in hours to reach next stage)
    public static readonly Dictionary<string, GrowthStageInfo> GrowthStages = new()
    {
        ["egg"] = new(0.5f, "duckling"),
        ["duckling"] = new(24f, "teen"),
        ["teen"] = new(72f, "adult"),
        ["adult"] = new(168f, "elder"),
        ["elder"] = new(null, null)
    };

    // Personality trait ranges
    public const int PersonalityMin = -100;
    public const int PersonalityMax = 100;

    // Default personality (slightly derpy duck)
    public static readonly Dictionary<string, int> DefaultPersonality = new()
    {
        ["clever_derpy"] = -30,
        ["brave_timid"] = 0,
        ["active_lazy"] = 20,
        ["social_shy"] = 30,
        ["neat_messy"] = -20
    };

    // AI behavior settings
    public const float AiIdleInterval = 5.0f;
    public const float AiRandomness = 0.3f;
    public const float DerpyRandomnessBonus = 0.4f;

    // Offline progression
    public const int MaxOfflineHours = 24;
    public const float OfflineDecayMultiplier = 0.5f;

    // Duck names for random selection
    public static readonly string[] DuckNames =
    {
        "Cheese", "Quackers", "Waddles", "Ducky", "Feathers",
        "Breadcrumb", "Puddles", "Sunny", "Daisy", "Maple"
    };
}

public record GrowthStageInfo(float? DurationHours, string? NextStage);
