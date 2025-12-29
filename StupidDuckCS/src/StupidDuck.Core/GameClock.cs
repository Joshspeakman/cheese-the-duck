namespace StupidDuck.Core;

/// <summary>
/// Game clock and time management for real-time and offline progression.
/// </summary>
public class GameClock
{
    private DateTime _lastTick;
    private DateTime? _lastSaveTime;
    private float _accumulatedDelta;
    private float _timeMultiplier;

    public GameClock()
    {
        _lastTick = DateTime.Now;
        _lastSaveTime = null;
        _accumulatedDelta = 0.0f;
        _timeMultiplier = GameConfig.TimeMultiplier;
    }

    public DateTime Now => DateTime.Now;
    public string Timestamp => Now.ToString("o");

    /// <summary>
    /// Calculate delta time since last tick.
    /// </summary>
    public float Tick()
    {
        var current = DateTime.Now;
        var delta = (float)(current - _lastTick).TotalSeconds;
        _lastTick = current;
        return delta * _timeMultiplier;
    }

    /// <summary>
    /// Convert delta seconds to minutes for need calculations.
    /// </summary>
    public float GetDeltaMinutes(float deltaSeconds) => deltaSeconds / 60.0f;

    /// <summary>
    /// Calculate how much time passed while offline.
    /// </summary>
    public OfflineTimeResult CalculateOfflineTime(string lastPlayedIso)
    {
        if (!DateTime.TryParse(lastPlayedIso, out var lastPlayed))
        {
            return new OfflineTimeResult(0, 0, 0, false, 1.0f);
        }

        var delta = Now - lastPlayed;
        var rawHours = (float)delta.TotalHours;
        var capped = rawHours > GameConfig.MaxOfflineHours;
        var hours = Math.Min(rawHours, GameConfig.MaxOfflineHours);

        return new OfflineTimeResult(
            hours,
            hours * 60,
            rawHours,
            capped,
            GameConfig.OfflineDecayMultiplier
        );
    }

    /// <summary>
    /// Format a duration in hours as a human-readable string.
    /// </summary>
    public string FormatDuration(float hours)
    {
        if (hours < 1f / 60f)
            return "just now";
        
        if (hours < 1)
        {
            var minutes = (int)(hours * 60);
            return $"{minutes} minute{(minutes != 1 ? "s" : "")}";
        }
        
        if (hours < 24)
        {
            var h = (int)hours;
            var m = (int)((hours - h) * 60);
            if (m > 0)
                return $"{h} hour{(h != 1 ? "s" : "")}, {m} min";
            return $"{h} hour{(h != 1 ? "s" : "")}";
        }

        var days = (int)(hours / 24);
        var remainingHours = (int)(hours % 24);
        if (remainingHours > 0)
            return $"{days} day{(days != 1 ? "s" : "")}, {remainingHours} hr";
        return $"{days} day{(days != 1 ? "s" : "")}";
    }

    public void SetTimeMultiplier(float multiplier)
    {
        _timeMultiplier = Math.Clamp(multiplier, 0.1f, 100.0f);
    }

    public string GetTimeOfDay()
    {
        var hour = Now.Hour;
        return hour switch
        {
            >= 5 and < 12 => "morning",
            >= 12 and < 17 => "afternoon",
            >= 17 and < 21 => "evening",
            _ => "night"
        };
    }
}

public record OfflineTimeResult(
    float Hours,
    float Minutes,
    float RawHours,
    bool Capped,
    float DecayMultiplier
);
