using StupidDuck.Core;

namespace StupidDuck.Duck;

/// <summary>
/// Possible mood states for the duck.
/// </summary>
public enum MoodState
{
    Ecstatic,
    Happy,
    Content,
    Grumpy,
    Sad,
    Miserable
}

/// <summary>
/// Container for mood information.
/// </summary>
public record MoodInfo(
    MoodState State,
    float Score,
    string Description,
    bool CanPlay = true,
    bool CanLearn = true
);

/// <summary>
/// Mood data with descriptions and effects.
/// </summary>
public static class MoodData
{
    public static readonly Dictionary<MoodState, MoodStateData> Data = new()
    {
        [MoodState.Ecstatic] = new(
            "suspiciously smug about life",
            new[] { "!!", "^o^", "*gloat*" },
            true, true
        ),
        [MoodState.Happy] = new(
            "tolerating existence quite well",
            new[] { "^-^", ":)", "*waggle*" },
            true, true
        ),
        [MoodState.Content] = new(
            "not actively plotting revenge",
            new[] { "-.-", "~", "*chill*" },
            true, true
        ),
        [MoodState.Grumpy] = new(
            "radiating 'don't test me' energy",
            new[] { ">:(", "-_-", "*huff*" },
            true, false
        ),
        [MoodState.Sad] = new(
            "dramatically brooding",
            new[] { ":(", "T-T", "*sigh*" },
            false, false
        ),
        [MoodState.Miserable] = new(
            "convinced the world is against him",
            new[] { "T_T", ";-;", "*gloom*" },
            false, false
        )
    };
}

public record MoodStateData(
    string Description,
    string[] Expressions,
    bool CanPlay,
    bool CanLearn
);

/// <summary>
/// Calculates and tracks the duck's mood.
/// </summary>
public class MoodCalculator
{
    private readonly List<float> _history = new();
    private const int MaxHistory = 10;
    private static readonly Random Rng = new();

    /// <summary>
    /// Calculate mood score from weighted needs.
    /// </summary>
    public float CalculateScore(Needs needs)
    {
        var score = 0f;
        score += needs.Hunger * GameConfig.MoodWeights["hunger"];
        score += needs.Energy * GameConfig.MoodWeights["energy"];
        score += needs.Fun * GameConfig.MoodWeights["fun"];
        score += needs.Cleanliness * GameConfig.MoodWeights["cleanliness"];
        score += needs.Social * GameConfig.MoodWeights["social"];
        return MathF.Round(score, 1);
    }

    /// <summary>
    /// Determine mood state from score.
    /// </summary>
    public MoodState GetState(float score)
    {
        if (score >= GameConfig.MoodThresholds["ecstatic"])
            return MoodState.Ecstatic;
        if (score >= GameConfig.MoodThresholds["happy"])
            return MoodState.Happy;
        if (score >= GameConfig.MoodThresholds["content"])
            return MoodState.Content;
        if (score >= GameConfig.MoodThresholds["grumpy"])
            return MoodState.Grumpy;
        if (score >= GameConfig.MoodThresholds["sad"])
            return MoodState.Sad;
        return MoodState.Miserable;
    }

    /// <summary>
    /// Get complete mood information from needs.
    /// </summary>
    public MoodInfo GetMood(Needs needs)
    {
        var score = CalculateScore(needs);
        var state = GetState(score);
        var data = MoodData.Data[state];

        _history.Add(score);
        while (_history.Count > MaxHistory)
            _history.RemoveAt(0);

        return new MoodInfo(
            state,
            score,
            data.Description,
            data.CanPlay,
            data.CanLearn
        );
    }

    /// <summary>
    /// Get mood trend based on history.
    /// </summary>
    public string GetTrend()
    {
        if (_history.Count < 3)
            return "stable";

        var recent = _history.Skip(_history.Count - 3).ToList();
        if (recent[^1] > recent[0] + 5)
            return "improving";
        if (recent[^1] < recent[0] - 5)
            return "declining";
        return "stable";
    }

    /// <summary>
    /// Get a random expression for the mood state.
    /// </summary>
    public string GetExpression(MoodState state)
    {
        var expressions = MoodData.Data[state].Expressions;
        return expressions[Rng.Next(expressions.Length)];
    }

    public List<float> GetHistory() => new(_history);

    public void SetHistory(List<float>? history)
    {
        _history.Clear();
        if (history != null)
        {
            var toAdd = history.Skip(Math.Max(0, history.Count - MaxHistory));
            _history.AddRange(toAdd);
        }
    }

    /// <summary>
    /// Create a visual mood bar.
    /// </summary>
    public string GetMoodBar(float score, int width = 20)
    {
        var filled = (int)((score / 100f) * width);
        var empty = width - filled;

        var ch = score switch
        {
            >= 70 => '*',
            >= 50 => '=',
            >= 30 => '-',
            _ => '.'
        };

        return $"[{new string(ch, filled)}{new string(' ', empty)}]";
    }
}
