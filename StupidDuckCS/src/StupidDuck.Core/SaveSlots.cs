using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;

namespace StupidDuck.Core;

/// <summary>
/// Information about a save slot.
/// </summary>
public class SaveSlotInfo
{
    public int SlotId { get; set; }
    public bool IsEmpty { get; set; } = true;
    public string DuckName { get; set; } = "";
    public int Level { get; set; } = 1;
    public int PlaytimeMinutes { get; set; }
    public int Coins { get; set; }
    public string CreatedAt { get; set; } = "";
    public string LastPlayed { get; set; } = "";
    public int PrestigeLevel { get; set; }
    public int AchievementsCount { get; set; }
    public string Mood { get; set; } = "happy";
    public List<string> PreviewAscii { get; set; } = new();
}

/// <summary>
/// System for managing multiple save slots.
/// </summary>
public class SaveSlotsSystem
{
    public const int MaxSlots = 5;

    public string SaveDir { get; }
    public int CurrentSlot { get; set; } = 1;
    public Dictionary<int, SaveSlotInfo> Slots { get; set; } = new();

    private static readonly Dictionary<string, string> MoodFaces = new()
    {
        ["happy"] = "^◡^",
        ["excited"] = "✧◡✧",
        ["content"] = "◡‿◡",
        ["sad"] = "╥﹏╥",
        ["hungry"] = "ò﹏ó",
        ["sleepy"] = "-_-",
        ["playful"] = "◕‿◕"
    };

    public SaveSlotsSystem(string? saveDir = null)
    {
        SaveDir = saveDir ?? Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.UserProfile),
            ".cheese_the_duck");

        Directory.CreateDirectory(SaveDir);
        RefreshSlots();
    }

    public string GetSavePath(int slotId) =>
        slotId == 1
            ? Path.Combine(SaveDir, "save.json")
            : Path.Combine(SaveDir, $"save_slot_{slotId}.json");

    public string GetBackupPath(int slotId) =>
        Path.Combine(SaveDir, $"save_slot_{slotId}.backup.json");

    public void RefreshSlots()
    {
        Slots.Clear();

        for (var slotId = 1; slotId <= MaxSlots; slotId++)
        {
            var savePath = GetSavePath(slotId);

            if (File.Exists(savePath))
            {
                try
                {
                    var json = File.ReadAllText(savePath);
                    using var doc = JsonDocument.Parse(json);
                    var data = doc.RootElement;
                    Slots[slotId] = ParseSaveData(slotId, data);
                }
                catch
                {
                    Slots[slotId] = new SaveSlotInfo
                    {
                        SlotId = slotId,
                        IsEmpty = false,
                        DuckName = "CORRUPTED"
                    };
                }
            }
            else
            {
                Slots[slotId] = new SaveSlotInfo
                {
                    SlotId = slotId,
                    IsEmpty = true
                };
            }
        }
    }

    private SaveSlotInfo ParseSaveData(int slotId, JsonElement data)
    {
        var duckData = data.TryGetProperty("duck", out var d) ? d : default;
        var progressionData = data.TryGetProperty("progression", out var p) ? p : default;
        var prestigeData = data.TryGetProperty("prestige", out var pr) ? pr : default;
        var achievementsData = data.TryGetProperty("achievements", out var a) ? a : default;
        var statsData = data.TryGetProperty("statistics", out var s) ? s : default;

        var duckName = TryGetString(duckData, "name") ?? "Cheese";
        var level = TryGetInt(progressionData, "level") ?? 1;
        var coins = TryGetInt(progressionData, "coins") ?? 0;
        var prestigeLevel = TryGetInt(prestigeData, "prestige_level") ?? 0;
        var playtime = TryGetInt(statsData, "total_playtime_minutes") ?? 0;
        var firstPlayed = TryGetString(statsData, "first_played") ?? "Unknown";
        var lastPlayed = TryGetString(statsData, "last_played") ?? "Unknown";

        // Get mood
        var moodData = duckData.ValueKind == JsonValueKind.Object && duckData.TryGetProperty("mood", out var m) ? m : default;
        var currentMood = TryGetString(moodData, "current_mood") ?? "happy";

        // Count achievements
        var achievementsCount = 0;
        if (achievementsData.ValueKind == JsonValueKind.Object &&
            achievementsData.TryGetProperty("unlocked", out var unlocked) &&
            unlocked.ValueKind == JsonValueKind.Array)
        {
            achievementsCount = unlocked.GetArrayLength();
        }

        var preview = GeneratePreview(level, prestigeLevel, currentMood);

        return new SaveSlotInfo
        {
            SlotId = slotId,
            IsEmpty = false,
            DuckName = duckName,
            Level = level,
            PlaytimeMinutes = playtime,
            Coins = coins,
            CreatedAt = firstPlayed,
            LastPlayed = lastPlayed,
            PrestigeLevel = prestigeLevel,
            AchievementsCount = achievementsCount,
            Mood = currentMood,
            PreviewAscii = preview
        };
    }

    private static string? TryGetString(JsonElement element, string property)
    {
        if (element.ValueKind == JsonValueKind.Object &&
            element.TryGetProperty(property, out var val) &&
            val.ValueKind == JsonValueKind.String)
            return val.GetString();
        return null;
    }

    private static int? TryGetInt(JsonElement element, string property)
    {
        if (element.ValueKind == JsonValueKind.Object &&
            element.TryGetProperty(property, out var val) &&
            val.ValueKind == JsonValueKind.Number)
            return val.GetInt32();
        return null;
    }

    private List<string> GeneratePreview(int level, int prestige, string mood)
    {
        var face = MoodFaces.GetValueOrDefault(mood, "^◡^");

        if (prestige > 0)
        {
            return new List<string>
            {
                "  ✨👑✨   ",
                $"   ({face})  ",
                "  >🦆<    ",
                $"  P{prestige} Lv{level} "
            };
        }
        else if (level >= 50)
        {
            return new List<string>
            {
                "    ⭐     ",
                $"   ({face})  ",
                "   🦆      ",
                $"   Lv{level}   "
            };
        }
        else
        {
            return new List<string>
            {
                $"   ({face})  ",
                "   🦆      ",
                $"   Lv{level}   "
            };
        }
    }

    public string FormatPlaytime(int minutes)
    {
        var hours = minutes / 60;
        var mins = minutes % 60;

        if (hours > 24)
        {
            var days = hours / 24;
            hours %= 24;
            return $"{days}d {hours}h";
        }
        else if (hours > 0)
        {
            return $"{hours}h {mins}m";
        }
        else
        {
            return $"{mins}m";
        }
    }

    public SaveSlotInfo? GetSlot(int slotId) =>
        Slots.GetValueOrDefault(slotId);

    public string? LoadSlot(int slotId)
    {
        if (slotId < 1 || slotId > MaxSlots)
            return null;

        var savePath = GetSavePath(slotId);
        if (!File.Exists(savePath))
            return null;

        try
        {
            return File.ReadAllText(savePath);
        }
        catch
        {
            return null;
        }
    }

    public bool SaveToSlot(int slotId, string jsonData)
    {
        if (slotId < 1 || slotId > MaxSlots)
            return false;

        var savePath = GetSavePath(slotId);
        var backupPath = GetBackupPath(slotId);

        try
        {
            // Create backup of existing save
            if (File.Exists(savePath))
                File.Copy(savePath, backupPath, overwrite: true);

            // Save new data
            File.WriteAllText(savePath, jsonData);

            RefreshSlots();
            return true;
        }
        catch
        {
            return false;
        }
    }

    public bool DeleteSlot(int slotId)
    {
        if (slotId < 1 || slotId > MaxSlots)
            return false;

        var savePath = GetSavePath(slotId);
        var backupPath = GetBackupPath(slotId);

        try
        {
            if (File.Exists(savePath))
                File.Delete(savePath);
            if (File.Exists(backupPath))
                File.Delete(backupPath);

            RefreshSlots();
            return true;
        }
        catch
        {
            return false;
        }
    }

    public bool CopySlot(int fromSlot, int toSlot)
    {
        var data = LoadSlot(fromSlot);
        if (data == null)
            return false;

        return SaveToSlot(toSlot, data);
    }

    public bool RestoreBackup(int slotId)
    {
        var backupPath = GetBackupPath(slotId);
        var savePath = GetSavePath(slotId);

        if (!File.Exists(backupPath))
            return false;

        try
        {
            File.Copy(backupPath, savePath, overwrite: true);
            RefreshSlots();
            return true;
        }
        catch
        {
            return false;
        }
    }

    public bool HasBackup(int slotId) =>
        File.Exists(GetBackupPath(slotId));

    public bool ExportSlot(int slotId, string exportPath)
    {
        var data = LoadSlot(slotId);
        if (data == null)
            return false;

        try
        {
            File.WriteAllText(exportPath, data);
            return true;
        }
        catch
        {
            return false;
        }
    }

    public bool ImportSlot(int slotId, string importPath)
    {
        try
        {
            var data = File.ReadAllText(importPath);
            // Validate JSON
            using var _ = JsonDocument.Parse(data);
            return SaveToSlot(slotId, data);
        }
        catch
        {
            return false;
        }
    }

    public List<string> RenderSlotSelection(bool showDetails = true)
    {
        var lines = new List<string>
        {
            "╔═══════════════════════════════════════════════╗",
            "║           💾 SAVE SLOTS 💾                    ║",
            "╠═══════════════════════════════════════════════╣"
        };

        for (var slotId = 1; slotId <= MaxSlots; slotId++)
        {
            var slot = Slots.GetValueOrDefault(slotId);

            if (slot == null || slot.IsEmpty)
            {
                lines.Add($"║  [{slotId}] ─── EMPTY SLOT ───                   ║");
                lines.Add("║      Start a new adventure!                   ║");
                lines.Add("║                                               ║");
            }
            else
            {
                var active = slotId == CurrentSlot ? " ◀" : "  ";
                var name = slot.DuckName.PadRight(25);
                if (name.Length > 25) name = name.Substring(0, 25);
                lines.Add($"║  [{slotId}] {name} {active}      ║");

                if (showDetails)
                {
                    foreach (var previewLine in slot.PreviewAscii)
                    {
                        var padded = previewLine.PadRight(39);
                        if (padded.Length > 39) padded = padded.Substring(0, 39);
                        lines.Add($"║      {padded}  ║");
                    }

                    var playtime = FormatPlaytime(slot.PlaytimeMinutes);
                    lines.Add($"║      💰 {slot.Coins,-8}  ⏱️ {playtime,-15}  ║");
                    lines.Add($"║      🏆 {slot.AchievementsCount} achievements                    ║");

                    if (!string.IsNullOrEmpty(slot.LastPlayed) && slot.LastPlayed != "Unknown")
                    {
                        var lastStr = slot.LastPlayed.Length > 16 ? slot.LastPlayed.Substring(0, 16) : slot.LastPlayed;
                        if (DateTime.TryParse(slot.LastPlayed, out var dt))
                            lastStr = dt.ToString("yyyy-MM-dd HH:mm");
                        lines.Add($"║      Last: {lastStr.PadRight(30)}  ║");
                    }
                }

                lines.Add("║                                               ║");
            }
        }

        lines.Add("╠═══════════════════════════════════════════════╣");
        lines.Add("║  [1-5] Select  [D] Delete  [C] Copy           ║");
        lines.Add("║  [E] Export    [I] Import  [B] Back           ║");
        lines.Add("╚═══════════════════════════════════════════════╝");

        return lines;
    }

    public List<string> RenderSlotDetails(int slotId)
    {
        var slot = Slots.GetValueOrDefault(slotId);

        var lines = new List<string>
        {
            "╔═══════════════════════════════════════════════╗",
            $"║           💾 SLOT {slotId} DETAILS                   ║",
            "╠═══════════════════════════════════════════════╣"
        };

        if (slot == null || slot.IsEmpty)
        {
            lines.Add("║                                               ║");
            lines.Add("║              Empty Save Slot                  ║");
            lines.Add("║                                               ║");
            lines.Add("║         Start a new adventure?                ║");
            lines.Add("║                                               ║");
        }
        else
        {
            lines.Add("║                                               ║");
            foreach (var previewLine in slot.PreviewAscii)
            {
                var centered = previewLine.PadLeft((43 + previewLine.Length) / 2).PadRight(43);
                if (centered.Length > 43) centered = centered.Substring(0, 43);
                lines.Add($"║  {centered}  ║");
            }

            lines.Add("║                                               ║");
            lines.Add($"║  Duck Name: {slot.DuckName.PadRight(32)}  ║");
            lines.Add($"║  Level: {slot.Level.ToString().PadRight(36)}  ║");

            if (slot.PrestigeLevel > 0)
                lines.Add($"║  Prestige: {slot.PrestigeLevel.ToString().PadRight(33)}  ║");

            lines.Add($"║  Coins: {slot.Coins.ToString().PadRight(36)}  ║");
            lines.Add($"║  Playtime: {FormatPlaytime(slot.PlaytimeMinutes).PadRight(33)}  ║");
            lines.Add($"║  Achievements: {slot.AchievementsCount.ToString().PadRight(28)}  ║");
            lines.Add($"║  Current Mood: {slot.Mood.PadRight(28)}  ║");

            lines.Add("║                                               ║");

            if (!string.IsNullOrEmpty(slot.CreatedAt) && slot.CreatedAt != "Unknown")
            {
                var created = slot.CreatedAt.Length > 10 ? slot.CreatedAt.Substring(0, 10) : slot.CreatedAt;
                if (DateTime.TryParse(slot.CreatedAt, out var dt))
                    created = dt.ToString("yyyy-MM-dd");
                lines.Add($"║  Created: {created.PadRight(34)}  ║");
            }

            if (!string.IsNullOrEmpty(slot.LastPlayed) && slot.LastPlayed != "Unknown")
            {
                var last = slot.LastPlayed.Length > 16 ? slot.LastPlayed.Substring(0, 16) : slot.LastPlayed;
                if (DateTime.TryParse(slot.LastPlayed, out var dt))
                    last = dt.ToString("yyyy-MM-dd HH:mm");
                lines.Add($"║  Last Played: {last.PadRight(30)}  ║");
            }

            var backupStr = HasBackup(slotId) ? "Yes" : "No";
            lines.Add($"║  Backup Available: {backupStr.PadRight(25)}  ║");
        }

        lines.Add("╠═══════════════════════════════════════════════╣");
        lines.Add("║  [L] Load  [D] Delete  [R] Restore Backup     ║");
        lines.Add("║  [E] Export  [B] Back                         ║");
        lines.Add("╚═══════════════════════════════════════════════╝");

        return lines;
    }

    // =============================================================================
    // SERIALIZATION
    // =============================================================================

    public SaveSlotsSaveData ToSaveData() => new()
    {
        CurrentSlot = CurrentSlot
    };

    public static SaveSlotsSystem FromSaveData(SaveSlotsSaveData data, string? saveDir = null)
    {
        var system = new SaveSlotsSystem(saveDir)
        {
            CurrentSlot = data.CurrentSlot > 0 ? data.CurrentSlot : 1
        };
        return system;
    }
}

public class SaveSlotsSaveData
{
    public int CurrentSlot { get; set; } = 1;
}
