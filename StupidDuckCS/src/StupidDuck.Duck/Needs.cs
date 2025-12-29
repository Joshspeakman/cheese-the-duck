using StupidDuck.Core;

namespace StupidDuck.Duck;

/// <summary>
/// Manages the duck's five core needs: hunger, energy, fun, cleanliness, social.
/// </summary>
public class Needs
{
    public float Hunger { get; set; } = 80f;
    public float Energy { get; set; } = 100f;
    public float Fun { get; set; } = 70f;
    public float Cleanliness { get; set; } = 100f;
    public float Social { get; set; } = 60f;

    public Needs()
    {
        ClampAll();
    }

    public Needs(float hunger, float energy, float fun, float cleanliness, float social)
    {
        Hunger = hunger;
        Energy = energy;
        Fun = fun;
        Cleanliness = cleanliness;
        Social = social;
        ClampAll();
    }

    private float Clamp(float value) => Math.Clamp(value, GameConfig.NeedMin, GameConfig.NeedMax);

    private void ClampAll()
    {
        Hunger = Clamp(Hunger);
        Energy = Clamp(Energy);
        Fun = Clamp(Fun);
        Cleanliness = Clamp(Cleanliness);
        Social = Clamp(Social);
    }

    /// <summary>
    /// Update needs based on time passed.
    /// </summary>
    public void Update(float deltaMinutes, Dictionary<string, int>? personality = null)
    {
        var modifiers = GetPersonalityModifiers(personality ?? new());

        Hunger -= GameConfig.NeedDecayRates["hunger"] * deltaMinutes * modifiers.GetValueOrDefault("hunger", 1.0f);
        Energy -= GameConfig.NeedDecayRates["energy"] * deltaMinutes * modifiers.GetValueOrDefault("energy", 1.0f);
        Fun -= GameConfig.NeedDecayRates["fun"] * deltaMinutes * modifiers.GetValueOrDefault("fun", 1.0f);
        Cleanliness -= GameConfig.NeedDecayRates["cleanliness"] * deltaMinutes * modifiers.GetValueOrDefault("cleanliness", 1.0f);
        Social -= GameConfig.NeedDecayRates["social"] * deltaMinutes * modifiers.GetValueOrDefault("social", 1.0f);

        ClampAll();
    }

    private Dictionary<string, float> GetPersonalityModifiers(Dictionary<string, int> personality)
    {
        var modifiers = new Dictionary<string, float>();

        // Active ducks burn energy faster, lazy ducks slower
        var activeLazy = personality.GetValueOrDefault("active_lazy", 0);
        modifiers["energy"] = 1.0f + (activeLazy / 200f);

        // Social ducks need more interaction, shy ducks less
        var socialShy = personality.GetValueOrDefault("social_shy", 0);
        modifiers["social"] = 1.0f + (socialShy / 200f);

        // Messy ducks get dirty faster
        var neatMessy = personality.GetValueOrDefault("neat_messy", 0);
        modifiers["cleanliness"] = 1.0f - (neatMessy / 200f);

        return modifiers;
    }

    /// <summary>
    /// Apply the effects of an interaction.
    /// </summary>
    public Dictionary<string, float> ApplyInteraction(string interaction)
    {
        var changes = new Dictionary<string, float>();
        
        if (!GameConfig.InteractionEffects.TryGetValue(interaction, out var effects))
            return changes;

        foreach (var (need, change) in effects)
        {
            var oldValue = GetNeedValue(need);
            var newValue = Clamp(oldValue + change);
            SetNeedValue(need, newValue);
            changes[need] = newValue - oldValue;
        }

        return changes;
    }

    public float GetNeedValue(string need) => need switch
    {
        "hunger" => Hunger,
        "energy" => Energy,
        "fun" => Fun,
        "cleanliness" => Cleanliness,
        "social" => Social,
        _ => 0
    };

    /// <summary>
    /// Apply a direct change to a need value.
    /// </summary>
    public void ApplyChange(string need, float change)
    {
        var current = GetNeedValue(need);
        SetNeedValue(need, Clamp(current + change));
    }

    private void SetNeedValue(string need, float value)
    {
        switch (need)
        {
            case "hunger": Hunger = value; break;
            case "energy": Energy = value; break;
            case "fun": Fun = value; break;
            case "cleanliness": Cleanliness = value; break;
            case "social": Social = value; break;
        }
    }

    public List<string> GetCriticalNeeds()
    {
        var critical = new List<string>();
        foreach (var need in new[] { "hunger", "energy", "fun", "cleanliness", "social" })
        {
            if (GetNeedValue(need) < GameConfig.NeedCritical)
                critical.Add(need);
        }
        return critical;
    }

    public List<string> GetLowNeeds()
    {
        var low = new List<string>();
        foreach (var need in new[] { "hunger", "energy", "fun", "cleanliness", "social" })
        {
            if (GetNeedValue(need) < GameConfig.NeedLow)
                low.Add(need);
        }
        return low;
    }

    public string? GetUrgentNeed()
    {
        var critical = GetCriticalNeeds();
        if (critical.Count > 0)
            return critical.MinBy(n => GetNeedValue(n));

        var low = GetLowNeeds();
        if (low.Count > 0)
            return low.MinBy(n => GetNeedValue(n));

        return null;
    }

    public NeedsSaveData ToSaveData() => new()
    {
        Hunger = MathF.Round(Hunger, 1),
        Energy = MathF.Round(Energy, 1),
        Fun = MathF.Round(Fun, 1),
        Cleanliness = MathF.Round(Cleanliness, 1),
        Social = MathF.Round(Social, 1)
    };

    public static Needs FromSaveData(NeedsSaveData? data)
    {
        if (data == null)
            return new Needs();

        return new Needs(
            data.Hunger,
            data.Energy,
            data.Fun,
            data.Cleanliness,
            data.Social
        );
    }

    public string GetStatusEmoji(string need)
    {
        var value = GetNeedValue(need);
        return value switch
        {
            >= 80 => "[###]",
            >= 60 => "[## ]",
            >= 40 => "[#  ]",
            >= 20 => "[!  ]",
            _ => "[!!!]"
        };
    }

    public Dictionary<string, string> GetAllAsBars(int width = 10)
    {
        var bars = new Dictionary<string, string>();
        
        foreach (var need in new[] { "hunger", "energy", "fun", "cleanliness", "social" })
        {
            var value = GetNeedValue(need);
            var filled = (int)((value / 100f) * width);
            var empty = width - filled;

            var marker = value switch
            {
                < GameConfig.NeedCritical => '!',
                < GameConfig.NeedLow => '=',
                _ => '#'
            };

            bars[need] = $"[{new string(marker, filled)}{new string(' ', empty)}]";
        }

        return bars;
    }
}
