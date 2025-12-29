using StupidDuck.Core;

namespace StupidDuck.Duck;

/// <summary>
/// The duck entity with all its state.
/// </summary>
public class Duck
{
    public string Name { get; set; }
    public string CreatedAt { get; set; }
    public Needs Needs { get; set; }
    public Dictionary<string, int> PersonalityValues { get; set; }
    public string GrowthStage { get; set; }
    public float GrowthProgress { get; set; }
    public string? CurrentAction { get; set; }
    public float? ActionStartTime { get; set; }

    private readonly MoodCalculator _moodCalculator;
    private Personality _personalitySystem;
    private DuckMemory _memory;
    private float _lastAutonomousAction;
    private string _actionMessage = "";

    public Duck(string name, string? createdAt = null)
    {
        Name = name;
        CreatedAt = createdAt ?? DateTime.Now.ToString("o");
        Needs = new Needs();
        PersonalityValues = new Dictionary<string, int>(GameConfig.DefaultPersonality);
        GrowthStage = "duckling";
        GrowthProgress = 0f;
        _moodCalculator = new MoodCalculator();
        _personalitySystem = new Personality(PersonalityValues);
        _memory = new DuckMemory { FirstMeeting = DateTime.Now.ToString("o") };
    }

    /// <summary>
    /// Create a new duck with random personality variations.
    /// </summary>
    public static Duck CreateNew(string? name = null)
    {
        var rng = new Random();
        name ??= GameConfig.DefaultDuckName;

        var personality = new Dictionary<string, int>();
        foreach (var (trait, defaultValue) in GameConfig.DefaultPersonality)
        {
            var variation = rng.Next(-20, 21);
            personality[trait] = Math.Clamp(defaultValue + variation, -100, 100);
        }

        var duck = new Duck(name)
        {
            PersonalityValues = personality
        };
        duck._personalitySystem = new Personality(personality);
        return duck;
    }

    /// <summary>
    /// Create Duck from save data.
    /// </summary>
    public static Duck FromSaveData(DuckSaveData data)
    {
        var duck = new Duck(data.Name, data.CreatedAt)
        {
            Needs = Needs.FromSaveData(data.Needs),
            PersonalityValues = data.Personality ?? new Dictionary<string, int>(GameConfig.DefaultPersonality),
            GrowthStage = data.GrowthStage,
            GrowthProgress = data.GrowthProgress,
            CurrentAction = data.CurrentAction
        };

        if (data.MoodHistory != null)
            duck._moodCalculator.SetHistory(data.MoodHistory);

        // Memory is handled by extension data in Python save, initialize fresh
        duck._memory = new DuckMemory { FirstMeeting = data.CreatedAt };

        duck._personalitySystem = new Personality(duck.PersonalityValues);
        return duck;
    }

    /// <summary>
    /// Convert duck to save data.
    /// </summary>
    public DuckSaveData ToSaveData() => new()
    {
        Name = Name,
        CreatedAt = CreatedAt,
        Needs = Needs.ToSaveData(),
        Personality = PersonalityValues,
        GrowthStage = GrowthStage,
        GrowthProgress = MathF.Round(GrowthProgress, 3),
        CurrentAction = CurrentAction,
        MoodHistory = _moodCalculator.GetHistory()
    };

    public DuckMemory Memory => _memory;
    public Personality PersonalitySystem => _personalitySystem;

    public string GetPersonalitySummary() => _personalitySystem.GetPersonalitySummary();

    /// <summary>
    /// Update the duck's state based on time passed.
    /// </summary>
    public void Update(float deltaMinutes)
    {
        Needs.Update(deltaMinutes, PersonalityValues);
        UpdateGrowth(deltaMinutes);
    }

    private void UpdateGrowth(float deltaMinutes)
    {
        if (!GameConfig.GrowthStages.TryGetValue(GrowthStage, out var stageInfo))
            return;

        if (stageInfo.DurationHours == null)
            return; // Already at final stage

        var hoursForStage = stageInfo.DurationHours.Value;
        var progressPerMinute = 1.0f / (hoursForStage * 60);
        GrowthProgress += deltaMinutes * progressPerMinute;

        if (GrowthProgress >= 1.0f)
        {
            GrowthProgress = 0f;
            if (stageInfo.NextStage != null)
                GrowthStage = stageInfo.NextStage;
        }
    }

    public MoodInfo GetMood() => _moodCalculator.GetMood(Needs);
    public MoodState GetMoodState() => GetMood().State;

    /// <summary>
    /// Perform an interaction with the duck.
    /// </summary>
    public InteractionResult Interact(string interaction)
    {
        var changes = Needs.ApplyInteraction(interaction);
        var mood = GetMood();
        CurrentAction = interaction;

        return new InteractionResult(
            interaction,
            changes,
            mood.State.ToString().ToLower(),
            mood.Score
        );
    }

    public int GetPersonalityTrait(string trait) => PersonalityValues.GetValueOrDefault(trait, 0);
    public bool IsDerpy() => GetPersonalityTrait("clever_derpy") < -20;
    public bool IsActive() => GetPersonalityTrait("active_lazy") > 20;
    public bool IsSocial() => GetPersonalityTrait("social_shy") > 20;

    public string GetStatusSummary()
    {
        var mood = GetMood();
        var urgent = Needs.GetUrgentNeed();

        var summary = $"{Name} is {mood.Description}";
        if (urgent != null)
            summary += $" (needs: {urgent})";

        return summary;
    }

    public float GetAgeDays()
    {
        if (!DateTime.TryParse(CreatedAt, out var created))
            return 0f;

        var delta = DateTime.Now - created;
        return (float)delta.TotalDays;
    }

    public string GetGrowthStageDisplay() => GrowthStage switch
    {
        "egg" => "Egg",
        "duckling" => "Duckling",
        "teen" => "Teen Duck",
        "adult" => "Adult Duck",
        "elder" => "Elder Duck",
        _ => char.ToUpper(GrowthStage[0]) + GrowthStage[1..].ToLower()
    };

    public void SetActionMessage(string message) => _actionMessage = message;

    public string GetActionMessage()
    {
        var msg = _actionMessage;
        _actionMessage = "";
        return msg;
    }

    public void ClearAction()
    {
        CurrentAction = null;
        ActionStartTime = null;
    }
}

public record InteractionResult(
    string Interaction,
    Dictionary<string, float> Changes,
    string MoodAfter,
    float MoodScore
);

/// <summary>
/// Duck's memory for past events and relationships.
/// </summary>
public class DuckMemory
{
    public string? FirstMeeting { get; set; }
    public List<string> Conversations { get; set; } = new();
    public Dictionary<string, int> Relationships { get; set; } = new();

    public MemorySaveData ToSaveData() => new()
    {
        FirstMeeting = FirstMeeting,
        Conversations = Conversations,
        Relationships = Relationships
    };

    public static DuckMemory FromSaveData(MemorySaveData data) => new()
    {
        FirstMeeting = data.FirstMeeting,
        Conversations = data.Conversations ?? new List<string>(),
        Relationships = data.Relationships ?? new Dictionary<string, int>()
    };
}
