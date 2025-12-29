using System.Text.Json;
using System.Text.Json.Serialization;

namespace StupidDuck.Core;

/// <summary>
/// Handles saving and loading game state to JSON files.
/// </summary>
public class SaveManager
{
    private readonly string _savePath;
    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        WriteIndented = true,
        PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull,
        PropertyNameCaseInsensitive = true,
        NumberHandling = JsonNumberHandling.AllowReadingFromString
    };

    public SaveManager(string? savePath = null)
    {
        _savePath = savePath ?? GameConfig.SaveFile;
        EnsureSaveDir();
    }

    private void EnsureSaveDir()
    {
        var dir = Path.GetDirectoryName(_savePath);
        if (!string.IsNullOrEmpty(dir) && !Directory.Exists(dir))
        {
            Directory.CreateDirectory(dir);
        }
    }

    public bool SaveExists() => File.Exists(_savePath);

    /// <summary>
    /// Save game data to JSON file.
    /// </summary>
    public bool Save(GameSaveData data)
    {
        try
        {
            data.Version = "1.0";
            data.SavedAt = DateTime.Now.ToString("o");

            var tempPath = _savePath + ".tmp";
            var json = JsonSerializer.Serialize(data, JsonOptions);
            File.WriteAllText(tempPath, json);
            
            // Atomic rename
            File.Move(tempPath, _savePath, overwrite: true);
            return true;
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"Save failed: {ex.Message}");
            return false;
        }
    }

    /// <summary>
    /// Load game data from JSON file.
    /// </summary>
    public GameSaveData? Load()
    {
        if (!SaveExists())
            return null;

        try
        {
            var json = File.ReadAllText(_savePath);
            
            // Try to deserialize with relaxed options
            var options = new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true,
                PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
                NumberHandling = JsonNumberHandling.AllowReadingFromString,
                UnknownTypeHandling = JsonUnknownTypeHandling.JsonElement
            };
            
            return JsonSerializer.Deserialize<GameSaveData>(json, options);
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"Load failed: {ex.Message}");
            // Return null to trigger new game
            return null;
        }
    }

    public bool DeleteSave()
    {
        try
        {
            if (SaveExists())
                File.Delete(_savePath);
            return true;
        }
        catch
        {
            return false;
        }
    }

    public SaveInfo? GetSaveInfo()
    {
        var data = Load();
        if (data == null)
            return null;

        return new SaveInfo(
            data.Duck?.Name ?? "Unknown",
            data.Duck?.GrowthStage ?? "unknown",
            data.LastPlayed ?? "unknown",
            data.Statistics?.DaysAlive ?? 0
        );
    }
}

public record SaveInfo(string Name, string Stage, string LastPlayed, int DaysAlive);

/// <summary>
/// Complete save data structure.
/// </summary>
public class GameSaveData
{
    public string? Version { get; set; }
    public string? SavedAt { get; set; }
    public string? LastPlayed { get; set; }
    public DuckSaveData? Duck { get; set; }
    
    [JsonExtensionData]
    public Dictionary<string, JsonElement>? ExtensionData { get; set; }
    
    public GameStatistics? Statistics { get; set; }
}

public class DuckSaveData
{
    public string Name { get; set; } = GameConfig.DefaultDuckName;
    public string? CreatedAt { get; set; }
    public string GrowthStage { get; set; } = "duckling";
    public float GrowthProgress { get; set; }
    public NeedsSaveData? Needs { get; set; }
    public Dictionary<string, int>? Personality { get; set; }
    public string? CurrentAction { get; set; }
    public List<float>? MoodHistory { get; set; }
    
    [JsonExtensionData]
    public Dictionary<string, JsonElement>? ExtensionData { get; set; }
}

public class NeedsSaveData
{
    public float Hunger { get; set; } = 80;
    public float Energy { get; set; } = 100;
    public float Fun { get; set; } = 70;
    public float Cleanliness { get; set; } = 100;
    public float Social { get; set; } = 60;
}

public class MemorySaveData
{
    public string? FirstMeeting { get; set; }
    public List<string>? Conversations { get; set; }
    public Dictionary<string, int>? Relationships { get; set; }
}

public class GameStatistics
{
    public int DaysAlive { get; set; }
    public int TimesFed { get; set; }
    public int TimesPlayed { get; set; }
    public int TimesCleaned { get; set; }
    public int TimesPetted { get; set; }
    public int Conversations { get; set; }
}

/// <summary>
/// Factory for creating new save data.
/// </summary>
public static class SaveDataFactory
{
    public static GameSaveData CreateNew(string duckName)
    {
        var now = DateTime.Now.ToString("o");
        
        return new GameSaveData
        {
            Duck = new DuckSaveData
            {
                Name = duckName,
                CreatedAt = now,
                GrowthStage = "duckling",
                GrowthProgress = 0,
                Needs = new NeedsSaveData(),
                Personality = new Dictionary<string, int>(GameConfig.DefaultPersonality),
                MoodHistory = new List<float>()
            },
            LastPlayed = now,
            Statistics = new GameStatistics()
        };
    }
}
