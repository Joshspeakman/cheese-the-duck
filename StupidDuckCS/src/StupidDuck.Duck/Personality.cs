using StupidDuck.Core;

namespace StupidDuck.Duck;

/// <summary>
/// A single personality trait with its effects.
/// </summary>
public class PersonalityTrait
{
    public string Name { get; }
    public string LowName { get; }
    public string HighName { get; }
    public int Value { get; set; }

    public PersonalityTrait(string name, string lowName, string highName, int value)
    {
        Name = name;
        LowName = lowName;
        HighName = highName;
        Value = value;
    }

    public string DisplayName => Value switch
    {
        < -30 => LowName,
        > 30 => HighName,
        _ => $"Somewhat {LowName.ToLower()}/{HighName.ToLower()}"
    };

    public string Intensity => Math.Abs(Value) switch
    {
        >= 80 => "Extremely",
        >= 60 => "Very",
        >= 40 => "Quite",
        >= 20 => "Somewhat",
        _ => "Slightly"
    };
}

/// <summary>
/// Definitions for all personality traits.
/// </summary>
public static class TraitDefinitions
{
    public static readonly Dictionary<string, TraitDef> All = new()
    {
        ["clever_derpy"] = new TraitDef(
            "Derpy", "Clever",
            "Affects problem-solving and dialogue coherence",
            new Dictionary<string, float>
            {
                ["dialogue_randomness"] = -0.5f,
                ["learning_speed"] = 0.3f,
                ["trip_chance"] = -0.4f
            }
        ),
        ["brave_timid"] = new TraitDef(
            "Timid", "Brave",
            "Affects reactions to events and new things",
            new Dictionary<string, float>
            {
                ["event_fear_response"] = -0.5f,
                ["exploration_bonus"] = 0.3f,
                ["hide_chance"] = -0.4f
            }
        ),
        ["active_lazy"] = new TraitDef(
            "Lazy", "Active",
            "Affects energy usage and activity level",
            new Dictionary<string, float>
            {
                ["energy_decay"] = 0.3f,
                ["action_frequency"] = 0.4f,
                ["nap_preference"] = -0.5f
            }
        ),
        ["social_shy"] = new TraitDef(
            "Shy", "Social",
            "Affects interaction needs and talkativeness",
            new Dictionary<string, float>
            {
                ["social_decay"] = 0.4f,
                ["quack_frequency"] = 0.5f,
                ["approach_player"] = 0.3f
            }
        ),
        ["neat_messy"] = new TraitDef(
            "Messy", "Neat",
            "Affects cleanliness decay and preening",
            new Dictionary<string, float>
            {
                ["cleanliness_decay"] = -0.3f,
                ["preen_frequency"] = 0.4f,
                ["splash_messiness"] = -0.3f
            }
        )
    };
}

public record TraitDef(
    string LowName,
    string HighName,
    string Description,
    Dictionary<string, float> Effects
);

/// <summary>
/// Manages the duck's personality traits.
/// </summary>
public class Personality
{
    private readonly Dictionary<string, PersonalityTrait> _traits = new();
    private static readonly Random Rng = new();

    public Personality(Dictionary<string, int>? traits = null)
    {
        foreach (var (traitId, definition) in TraitDefinitions.All)
        {
            var value = traits?.GetValueOrDefault(traitId, 0) ?? 0;
            _traits[traitId] = new PersonalityTrait(
                traitId,
                definition.LowName,
                definition.HighName,
                value
            );
        }
    }

    public static Personality GenerateRandom()
    {
        var traits = new Dictionary<string, int>();
        foreach (var traitId in TraitDefinitions.All.Keys)
        {
            if (traitId == "clever_derpy")
            {
                // Bias toward derpy
                traits[traitId] = Rng.Next(-70, 21);
            }
            else
            {
                traits[traitId] = Rng.Next(-50, 51);
            }
        }
        return new Personality(traits);
    }

    public int GetTrait(string traitId) =>
        _traits.TryGetValue(traitId, out var trait) ? trait.Value : 0;

    public void SetTrait(string traitId, int value)
    {
        if (_traits.TryGetValue(traitId, out var trait))
            trait.Value = Math.Clamp(value, -100, 100);
    }

    public void AdjustTrait(string traitId, int delta)
    {
        if (_traits.TryGetValue(traitId, out var trait))
            SetTrait(traitId, trait.Value + delta);
    }

    /// <summary>
    /// Get the combined effect value from all traits.
    /// </summary>
    public float GetEffect(string effectName)
    {
        var total = 0f;
        foreach (var (traitId, definition) in TraitDefinitions.All)
        {
            if (definition.Effects.TryGetValue(effectName, out var effectWeight))
            {
                var traitValue = GetTrait(traitId);
                total += (traitValue / 100f) * effectWeight;
            }
        }
        return total;
    }

    /// <summary>
    /// Get the most pronounced personality traits.
    /// </summary>
    public List<(string Id, PersonalityTrait Trait)> GetDominantTraits(int count = 2)
    {
        return _traits
            .OrderByDescending(kv => Math.Abs(kv.Value.Value))
            .Take(count)
            .Select(kv => (kv.Key, kv.Value))
            .ToList();
    }

    /// <summary>
    /// Get a human-readable personality summary.
    /// </summary>
    public string GetPersonalitySummary()
    {
        var dominant = GetDominantTraits(2);

        if (dominant.Count == 0)
            return "a fairly average duck";

        var descriptions = dominant
            .Where(d => Math.Abs(d.Trait.Value) >= 20)
            .Select(d => $"{d.Trait.Intensity.ToLower()} {d.Trait.DisplayName.ToLower()}")
            .ToList();

        if (descriptions.Count == 0)
            return "a fairly balanced duck";
        if (descriptions.Count == 1)
            return $"a {descriptions[0]} duck";
        return $"a {descriptions[0]} and {descriptions[1]} duck";
    }

    public Dictionary<string, int> ToDict() =>
        _traits.ToDictionary(kv => kv.Key, kv => kv.Value.Value);

    public static Personality FromDict(Dictionary<string, int> data) => new(data);
}
