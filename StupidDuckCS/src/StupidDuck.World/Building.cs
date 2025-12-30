using System;
using System.Collections.Generic;
using System.Linq;

namespace StupidDuck.World;

/// <summary>
/// Types of structures that can be built.
/// </summary>
public enum StructureType
{
    Nest,       // Basic shelters
    House,      // Advanced homes
    Workshop,   // Crafting stations
    Storage,    // Item storage
    Garden,     // Growing plants
    Decoration, // Pretty things
    Utility,    // Functional buildings
    Special     // Rare/magical buildings
}

/// <summary>
/// Status of a building project.
/// </summary>
public enum StructureStatus
{
    Planned,      // Not started
    InProgress,   // Being built
    Complete,     // Fully built
    Damaged,      // Needs repair
    Destroyed     // Needs rebuild
}

/// <summary>
/// A blueprint for building a structure.
/// </summary>
public class StructureBlueprint
{
    public string Id { get; set; } = "";
    public string Name { get; set; } = "";
    public string Description { get; set; } = "";
    public StructureType Type { get; set; }
    public Dictionary<string, int> MaterialsRequired { get; set; } = new();
    public int BuildSteps { get; set; } = 5;
    public int UnlockLevel { get; set; } = 1;
    public int BuildingSkillRequired { get; set; } = 1;
    public string? RequiresTool { get; set; }
    public int MaxDurability { get; set; } = 100;
    public bool IsUpgradeOf { get; set; }
    public string? UpgradesFrom { get; set; }
    public Dictionary<string, float> Bonuses { get; set; } = new();
    public string[]? AsciiArt { get; set; }
    public int XpReward { get; set; } = 50;
}

/// <summary>
/// A built structure in the world.
/// </summary>
public class Structure
{
    public string Id { get; set; } = "";
    public string BlueprintId { get; set; } = "";
    public string Name { get; set; } = "";
    public StructureStatus Status { get; set; } = StructureStatus.Planned;
    public int BuildProgress { get; set; }
    public int MaxProgress { get; set; } = 5;
    public int Durability { get; set; } = 100;
    public int MaxDurability { get; set; } = 100;
    public DateTime? CompletedAt { get; set; }
    public DateTime? LastRepair { get; set; }
    public Dictionary<string, float> Bonuses { get; set; } = new();

    public float GetDurabilityPercent() => MaxDurability > 0 ? (float)Durability / MaxDurability * 100f : 0f;

    public bool IsUsable() => Status == StructureStatus.Complete && Durability > 10;
}

/// <summary>
/// System for managing building operations.
/// </summary>
public class BuildingSystem
{
    // =============================================================================
    // BLUEPRINTS
    // =============================================================================

    public static readonly Dictionary<string, StructureBlueprint> AllBlueprints = new()
    {
        // === NESTS ===
        ["basic_nest"] = new()
        {
            Id = "basic_nest",
            Name = "Basic Nest",
            Description = "A simple nest of grass and twigs.",
            Type = StructureType.Nest,
            MaterialsRequired = new() { ["grass_blade"] = 15, ["twig"] = 10 },
            BuildSteps = 3,
            UnlockLevel = 1,
            BuildingSkillRequired = 1,
            MaxDurability = 50,
            Bonuses = new() { ["rest_bonus"] = 0.1f },
            XpReward = 25,
            AsciiArt = new[]
            {
                "  ___  ",
                " (   ) ",
                "(_____)"
            }
        },
        ["cozy_nest"] = new()
        {
            Id = "cozy_nest",
            Name = "Cozy Nest",
            Description = "A well-padded, comfortable nest.",
            Type = StructureType.Nest,
            MaterialsRequired = new() { ["woven_grass"] = 5, ["twig"] = 8, ["feather"] = 10, ["moss"] = 5 },
            BuildSteps = 5,
            UnlockLevel = 5,
            BuildingSkillRequired = 2,
            MaxDurability = 80,
            IsUpgradeOf = true,
            UpgradesFrom = "basic_nest",
            Bonuses = new() { ["rest_bonus"] = 0.25f, ["comfort"] = 0.15f },
            XpReward = 75,
            AsciiArt = new[]
            {
                "  _____  ",
                " (  o  ) ",
                " (     ) ",
                "(_______)"
            }
        },
        ["deluxe_nest"] = new()
        {
            Id = "deluxe_nest",
            Name = "Deluxe Nest",
            Description = "A luxurious nest with all the comforts!",
            Type = StructureType.Nest,
            MaterialsRequired = new() { ["woven_grass"] = 10, ["insulation"] = 5, ["fabric_scrap"] = 8, ["shell"] = 6 },
            BuildSteps = 8,
            UnlockLevel = 12,
            BuildingSkillRequired = 4,
            MaxDurability = 120,
            IsUpgradeOf = true,
            UpgradesFrom = "cozy_nest",
            Bonuses = new() { ["rest_bonus"] = 0.5f, ["comfort"] = 0.35f, ["happiness_bonus"] = 0.1f },
            XpReward = 150,
            AsciiArt = new[]
            {
                "  _______  ",
                " /  ^ ^  \\ ",
                "(    o    )",
                " \\       / ",
                " (_______)"
            }
        },
        // === HOUSES ===
        ["mud_hut"] = new()
        {
            Id = "mud_hut",
            Name = "Mud Hut",
            Description = "A sturdy mud and clay shelter.",
            Type = StructureType.House,
            MaterialsRequired = new() { ["clay"] = 20, ["twig"] = 15, ["thatch"] = 8 },
            BuildSteps = 8,
            UnlockLevel = 8,
            BuildingSkillRequired = 3,
            RequiresTool = "stone_hammer",
            MaxDurability = 150,
            Bonuses = new() { ["weather_protection"] = 0.5f, ["rest_bonus"] = 0.3f },
            XpReward = 150,
            AsciiArt = new[]
            {
                "    ___    ",
                "   /   \\   ",
                "  /     \\  ",
                " |   o   | ",
                " |___|___| "
            }
        },
        ["wooden_cottage"] = new()
        {
            Id = "wooden_cottage",
            Name = "Wooden Cottage",
            Description = "A cozy wooden home!",
            Type = StructureType.House,
            MaterialsRequired = new() { ["wooden_plank"] = 15, ["thatch"] = 12, ["rope"] = 5, ["clay_brick"] = 10 },
            BuildSteps = 12,
            UnlockLevel = 15,
            BuildingSkillRequired = 5,
            RequiresTool = "stone_hammer",
            MaxDurability = 200,
            IsUpgradeOf = true,
            UpgradesFrom = "mud_hut",
            Bonuses = new() { ["weather_protection"] = 0.8f, ["rest_bonus"] = 0.5f, ["comfort"] = 0.3f },
            XpReward = 300,
            AsciiArt = new[]
            {
                "     /\\     ",
                "    /  \\    ",
                "   /----\\   ",
                "  | [] o |  ",
                "  |______|  "
            }
        },
        ["stone_house"] = new()
        {
            Id = "stone_house",
            Name = "Stone House",
            Description = "A grand stone dwelling!",
            Type = StructureType.House,
            MaterialsRequired = new() { ["stone_block"] = 25, ["wooden_plank"] = 10, ["thatch"] = 15, ["insulation"] = 8 },
            BuildSteps = 20,
            UnlockLevel = 25,
            BuildingSkillRequired = 7,
            RequiresTool = "stone_hammer",
            MaxDurability = 300,
            IsUpgradeOf = true,
            UpgradesFrom = "wooden_cottage",
            Bonuses = new() { ["weather_protection"] = 1.0f, ["rest_bonus"] = 0.75f, ["comfort"] = 0.5f, ["happiness_bonus"] = 0.2f },
            XpReward = 500,
            AsciiArt = new[]
            {
                "      /\\      ",
                "     /  \\     ",
                "    /    \\    ",
                "   |------|   ",
                "   | [] []|   ",
                "   |__  __|   "
            }
        },
        // === WORKSHOPS ===
        ["workbench"] = new()
        {
            Id = "workbench",
            Name = "Workbench",
            Description = "A place for crafting!",
            Type = StructureType.Workshop,
            MaterialsRequired = new() { ["wooden_plank"] = 6, ["rock"] = 4, ["rope"] = 2 },
            BuildSteps = 5,
            UnlockLevel = 6,
            BuildingSkillRequired = 2,
            RequiresTool = "stone_hammer",
            MaxDurability = 100,
            Bonuses = new() { ["crafting_speed"] = 0.2f },
            XpReward = 100,
            AsciiArt = new[]
            {
                " _______ ",
                "|=======|",
                "| |   | |",
                "|_|   |_|"
            }
        },
        ["advanced_workshop"] = new()
        {
            Id = "advanced_workshop",
            Name = "Advanced Workshop",
            Description = "A fully equipped crafting station!",
            Type = StructureType.Workshop,
            MaterialsRequired = new() { ["wooden_plank"] = 15, ["stone_block"] = 8, ["rope"] = 6, ["clay_brick"] = 10 },
            BuildSteps = 12,
            UnlockLevel = 18,
            BuildingSkillRequired = 5,
            RequiresTool = "stone_hammer",
            MaxDurability = 180,
            IsUpgradeOf = true,
            UpgradesFrom = "workbench",
            Bonuses = new() { ["crafting_speed"] = 0.5f, ["crafting_quality"] = 0.2f },
            XpReward = 250,
            AsciiArt = new[]
            {
                "  _______  ",
                " |  ===  | ",
                " |[]   []| ",
                " | _____ | ",
                " |_|   |_| "
            }
        },
        // === STORAGE ===
        ["storage_chest"] = new()
        {
            Id = "storage_chest",
            Name = "Storage Chest",
            Description = "Store your treasures!",
            Type = StructureType.Storage,
            MaterialsRequired = new() { ["wooden_plank"] = 8, ["rope"] = 2 },
            BuildSteps = 4,
            UnlockLevel = 4,
            BuildingSkillRequired = 2,
            MaxDurability = 80,
            Bonuses = new() { ["storage_capacity"] = 50f },
            XpReward = 50,
            AsciiArt = new[]
            {
                " _____ ",
                "|     |",
                "|_____|"
            }
        },
        ["large_storage"] = new()
        {
            Id = "large_storage",
            Name = "Large Storage",
            Description = "A spacious storage area!",
            Type = StructureType.Storage,
            MaterialsRequired = new() { ["wooden_plank"] = 15, ["stone_block"] = 5, ["rope"] = 5 },
            BuildSteps = 8,
            UnlockLevel = 12,
            BuildingSkillRequired = 4,
            RequiresTool = "stone_hammer",
            MaxDurability = 150,
            IsUpgradeOf = true,
            UpgradesFrom = "storage_chest",
            Bonuses = new() { ["storage_capacity"] = 200f },
            XpReward = 150
        },
        // === GARDENS ===
        ["small_garden"] = new()
        {
            Id = "small_garden",
            Name = "Small Garden",
            Description = "A patch for growing plants!",
            Type = StructureType.Garden,
            MaterialsRequired = new() { ["grass_blade"] = 10, ["twig"] = 6, ["pebble"] = 8 },
            BuildSteps = 4,
            UnlockLevel = 3,
            BuildingSkillRequired = 1,
            MaxDurability = 60,
            Bonuses = new() { ["garden_plots"] = 3f },
            XpReward = 40,
            AsciiArt = new[]
            {
                " _______ ",
                "|* * * *|",
                "|_______|"
            }
        },
        ["flower_garden"] = new()
        {
            Id = "flower_garden",
            Name = "Flower Garden",
            Description = "Beautiful flowers bloom here!",
            Type = StructureType.Garden,
            MaterialsRequired = new() { ["wildflower"] = 15, ["seed"] = 10, ["pebble_path"] = 2, ["moss"] = 5 },
            BuildSteps = 6,
            UnlockLevel = 10,
            BuildingSkillRequired = 3,
            MaxDurability = 80,
            Bonuses = new() { ["garden_plots"] = 6f, ["happiness_bonus"] = 0.15f, ["beauty"] = 0.3f },
            XpReward = 100,
            AsciiArt = new[]
            {
                "  * * *  ",
                " *@*@*@* ",
                "|* * * *|",
                "|_______|"
            }
        },
        // === DECORATIONS ===
        ["pond"] = new()
        {
            Id = "pond",
            Name = "Small Pond",
            Description = "A relaxing water feature!",
            Type = StructureType.Decoration,
            MaterialsRequired = new() { ["clay"] = 15, ["pebble"] = 20, ["sand"] = 10 },
            BuildSteps = 6,
            UnlockLevel = 7,
            BuildingSkillRequired = 2,
            MaxDurability = 120,
            Bonuses = new() { ["happiness_bonus"] = 0.2f, ["relaxation"] = 0.3f },
            XpReward = 80,
            AsciiArt = new[]
            {
                "   ~~~   ",
                " ~~~~~~~ ",
                "(~~~~~~~)",
                " ~~~~~~~ "
            }
        },
        ["statue"] = new()
        {
            Id = "statue",
            Name = "Duck Statue",
            Description = "A magnificent duck statue!",
            Type = StructureType.Decoration,
            MaterialsRequired = new() { ["stone_block"] = 10, ["smooth_stone"] = 5 },
            BuildSteps = 10,
            UnlockLevel = 20,
            BuildingSkillRequired = 6,
            RequiresTool = "stone_hammer",
            MaxDurability = 200,
            Bonuses = new() { ["prestige"] = 0.5f, ["beauty"] = 0.5f },
            XpReward = 200,
            AsciiArt = new[]
            {
                "   _   ",
                "  (o)  ",
                "  / \\  ",
                " /   \\ ",
                "[_____]"
            }
        },
        // === UTILITY ===
        ["rain_collector"] = new()
        {
            Id = "rain_collector",
            Name = "Rain Collector",
            Description = "Collects rainwater!",
            Type = StructureType.Utility,
            MaterialsRequired = new() { ["clay"] = 8, ["wooden_plank"] = 4, ["reed"] = 6 },
            BuildSteps = 5,
            UnlockLevel = 8,
            BuildingSkillRequired = 3,
            MaxDurability = 70,
            Bonuses = new() { ["water_gathering"] = 0.5f },
            XpReward = 80
        },
        ["sun_dial"] = new()
        {
            Id = "sun_dial",
            Name = "Sun Dial",
            Description = "Tell time by the sun!",
            Type = StructureType.Utility,
            MaterialsRequired = new() { ["stone_block"] = 5, ["smooth_stone"] = 3 },
            BuildSteps = 4,
            UnlockLevel = 10,
            BuildingSkillRequired = 3,
            MaxDurability = 150,
            Bonuses = new() { ["time_awareness"] = 1.0f },
            XpReward = 60
        },
        // === SPECIAL ===
        ["wishing_well"] = new()
        {
            Id = "wishing_well",
            Name = "Wishing Well",
            Description = "Make wishes come true!",
            Type = StructureType.Special,
            MaterialsRequired = new() { ["stone_block"] = 20, ["clay_brick"] = 15, ["rope"] = 5, ["river_pearl"] = 3 },
            BuildSteps = 15,
            UnlockLevel = 25,
            BuildingSkillRequired = 6,
            RequiresTool = "stone_hammer",
            MaxDurability = 250,
            Bonuses = new() { ["luck"] = 0.3f, ["wish_power"] = 1.0f },
            XpReward = 350,
            AsciiArt = new[]
            {
                "   ___   ",
                "  /_\\  ",
                " || || ",
                "(======)",
                "|      |",
                "(______)"
            }
        },
        ["magic_circle"] = new()
        {
            Id = "magic_circle",
            Name = "Magic Circle",
            Description = "A circle of mystical power!",
            Type = StructureType.Special,
            MaterialsRequired = new() { ["crystal"] = 5, ["fairy_dust"] = 3, ["river_pearl"] = 5, ["magic_acorn"] = 2 },
            BuildSteps = 20,
            UnlockLevel = 30,
            BuildingSkillRequired = 8,
            MaxDurability = 100,
            Bonuses = new() { ["magic_power"] = 0.5f, ["xp_bonus"] = 0.2f },
            XpReward = 500,
            AsciiArt = new[]
            {
                "  * * *  ",
                " *     * ",
                "*  ___  *",
                "*  \\_/  *",
                " *     * ",
                "  * * *  "
            }
        }
    };

    // Skill XP thresholds
    private static readonly int[] SkillThresholds = { 0, 100, 300, 600, 1000, 1500, 2200, 3000, 4000, 5500 };

    // =============================================================================
    // STATE
    // =============================================================================

    public int BuildingSkill { get; set; } = 1;
    public int BuildingXp { get; set; }
    public List<string> BlueprintsUnlocked { get; set; } = new();
    public Dictionary<string, Structure> BuiltStructures { get; set; } = new();
    public Structure? CurrentProject { get; set; }
    private int _playerLevel = 1;
    private readonly Random _random = new();

    public BuildingSystem()
    {
        UnlockStartingBlueprints();
    }

    private void UnlockStartingBlueprints()
    {
        foreach (var (id, bp) in AllBlueprints)
        {
            if (bp.UnlockLevel <= 1 && bp.BuildingSkillRequired <= 1 && !BlueprintsUnlocked.Contains(id))
                BlueprintsUnlocked.Add(id);
        }
    }

    // =============================================================================
    // BLUEPRINT ACCESS
    // =============================================================================

    public List<StructureBlueprint> GetAvailableBlueprints(MaterialInventory inventory, int? playerLevel = null)
    {
        var level = playerLevel ?? _playerLevel;
        var available = new List<StructureBlueprint>();

        foreach (var bpId in BlueprintsUnlocked)
        {
            if (!AllBlueprints.TryGetValue(bpId, out var bp))
                continue;

            // Check if already built (unless upgradeable)
            if (BuiltStructures.ContainsKey(bpId) && !bp.IsUpgradeOf)
                continue;

            // Check upgrade requirement
            if (bp.IsUpgradeOf && !string.IsNullOrEmpty(bp.UpgradesFrom) && !BuiltStructures.ContainsKey(bp.UpgradesFrom))
                continue;

            if (bp.UnlockLevel <= level && bp.BuildingSkillRequired <= BuildingSkill)
                available.Add(bp);
        }

        return available;
    }

    // =============================================================================
    // BUILDING
    // =============================================================================

    public (bool Success, string Message) StartBuilding(string blueprintId, MaterialInventory inventory, int? playerLevel = null)
    {
        var level = playerLevel ?? _playerLevel;

        if (CurrentProject != null)
            return (false, $"Already building {CurrentProject.Name}!");

        if (!AllBlueprints.TryGetValue(blueprintId, out var bp))
            return (false, $"Unknown blueprint: {blueprintId}");

        if (!BlueprintsUnlocked.Contains(blueprintId))
            return (false, "Blueprint not unlocked");

        if (bp.UnlockLevel > level)
            return (false, $"Unlock at level {bp.UnlockLevel}");

        if (bp.BuildingSkillRequired > BuildingSkill)
            return (false, $"Need building skill {bp.BuildingSkillRequired}");

        // Check upgrade path
        if (bp.IsUpgradeOf && !string.IsNullOrEmpty(bp.UpgradesFrom) && !BuiltStructures.ContainsKey(bp.UpgradesFrom))
            return (false, $"Must build {AllBlueprints[bp.UpgradesFrom].Name} first");

        // Check materials
        foreach (var (matId, amount) in bp.MaterialsRequired)
        {
            if (inventory.GetCount(matId) < amount)
            {
                var matName = Materials.AllMaterials.TryGetValue(matId, out var mat) ? mat.Name : matId;
                return (false, $"Need {amount}x {matName}");
            }
        }

        // Consume materials
        foreach (var (matId, amount) in bp.MaterialsRequired)
            inventory.RemoveMaterial(matId, amount);

        CurrentProject = new Structure
        {
            Id = blueprintId,
            BlueprintId = blueprintId,
            Name = bp.Name,
            Status = StructureStatus.InProgress,
            BuildProgress = 0,
            MaxProgress = bp.BuildSteps,
            Durability = bp.MaxDurability,
            MaxDurability = bp.MaxDurability,
            Bonuses = new Dictionary<string, float>(bp.Bonuses)
        };

        return (true, $"Started building {bp.Name}!");
    }

    public (bool Complete, string Message, int? XpGained) DoWork()
    {
        if (CurrentProject == null)
            return (false, "No building project started", null);

        CurrentProject.BuildProgress++;

        if (CurrentProject.BuildProgress >= CurrentProject.MaxProgress)
        {
            // Complete the building!
            CurrentProject.Status = StructureStatus.Complete;
            CurrentProject.CompletedAt = DateTime.UtcNow;

            // If this is an upgrade, remove the old structure
            if (AllBlueprints.TryGetValue(CurrentProject.BlueprintId, out var bp))
            {
                if (bp.IsUpgradeOf && !string.IsNullOrEmpty(bp.UpgradesFrom))
                    BuiltStructures.Remove(bp.UpgradesFrom);

                // Award XP
                BuildingXp += bp.XpReward;
                CheckSkillUp();

                // Check for new blueprint unlocks
                CheckBlueprintUnlocks();

                BuiltStructures[CurrentProject.Id] = CurrentProject;

                var finished = CurrentProject;
                CurrentProject = null;

                return (true, $"Completed {finished.Name}! (+{bp.XpReward} XP)", bp.XpReward);
            }

            BuiltStructures[CurrentProject.Id] = CurrentProject;
            var completedName = CurrentProject.Name;
            CurrentProject = null;
            return (true, $"Completed {completedName}!", null);
        }

        var progress = (int)((float)CurrentProject.BuildProgress / CurrentProject.MaxProgress * 100);
        return (false, $"Building {CurrentProject.Name}... {progress}%", null);
    }

    public string CancelBuilding(MaterialInventory inventory)
    {
        if (CurrentProject == null)
            return "Not building anything";

        if (AllBlueprints.TryGetValue(CurrentProject.BlueprintId, out var bp))
        {
            // Refund based on progress
            var refundRatio = 1.0f - (float)CurrentProject.BuildProgress / CurrentProject.MaxProgress;
            foreach (var (matId, amount) in bp.MaterialsRequired)
            {
                var refund = (int)(amount * refundRatio * 0.5f);
                if (refund > 0)
                    inventory.AddMaterial(matId, refund);
            }
        }

        CurrentProject = null;
        return "Building cancelled. Partial materials refunded.";
    }

    // =============================================================================
    // MAINTENANCE
    // =============================================================================

    public void ApplyWeatherDamage(string weather)
    {
        var damageByWeather = new Dictionary<string, int>
        {
            ["storm"] = 15,
            ["heavy_rain"] = 8,
            ["rain"] = 3,
            ["snow"] = 5,
            ["hail"] = 20
        };

        if (!damageByWeather.TryGetValue(weather.ToLower(), out var baseDamage))
            return;

        foreach (var structure in BuiltStructures.Values)
        {
            if (structure.Status != StructureStatus.Complete)
                continue;

            // Weather protection reduces damage
            var protection = structure.Bonuses.GetValueOrDefault("weather_protection");
            var damage = (int)(baseDamage * (1 - protection));

            if (damage > 0)
            {
                structure.Durability = Math.Max(0, structure.Durability - damage);

                if (structure.Durability <= 0)
                    structure.Status = StructureStatus.Destroyed;
                else if (structure.Durability < structure.MaxDurability * 0.3f)
                    structure.Status = StructureStatus.Damaged;
            }
        }
    }

    public (bool Success, string Message) RepairStructure(string structureId, MaterialInventory inventory)
    {
        if (!BuiltStructures.TryGetValue(structureId, out var structure))
            return (false, "Structure not found");

        if (structure.Durability >= structure.MaxDurability)
            return (false, "Structure doesn't need repair");

        if (!AllBlueprints.TryGetValue(structure.BlueprintId, out var bp))
            return (false, "Unknown blueprint");

        // Repair costs 25% of original materials
        var missingPercent = 1.0f - (float)structure.Durability / structure.MaxDurability;
        var matCost = new Dictionary<string, int>();

        foreach (var (matId, amount) in bp.MaterialsRequired)
        {
            var cost = Math.Max(1, (int)(amount * 0.25f * missingPercent));
            matCost[matId] = cost;
        }

        // Check materials
        foreach (var (matId, amount) in matCost)
        {
            if (inventory.GetCount(matId) < amount)
            {
                var matName = Materials.AllMaterials.TryGetValue(matId, out var mat) ? mat.Name : matId;
                return (false, $"Need {amount}x {matName} for repair");
            }
        }

        // Consume and repair
        foreach (var (matId, amount) in matCost)
            inventory.RemoveMaterial(matId, amount);

        structure.Durability = structure.MaxDurability;
        structure.Status = StructureStatus.Complete;
        structure.LastRepair = DateTime.UtcNow;

        BuildingXp += 10;
        CheckSkillUp();

        return (true, $"Repaired {structure.Name}!");
    }

    // =============================================================================
    // BONUSES
    // =============================================================================

    public Dictionary<string, float> GetTotalBonuses()
    {
        var totals = new Dictionary<string, float>();

        foreach (var structure in BuiltStructures.Values)
        {
            if (!structure.IsUsable())
                continue;

            // Scale bonus by durability
            var durabilityScale = structure.GetDurabilityPercent() / 100f;

            foreach (var (bonusType, amount) in structure.Bonuses)
            {
                var scaled = amount * durabilityScale;
                totals[bonusType] = totals.GetValueOrDefault(bonusType) + scaled;
            }
        }

        return totals;
    }

    public float GetBonus(string bonusType) => GetTotalBonuses().GetValueOrDefault(bonusType);

    public bool HasWorkbench() =>
        BuiltStructures.ContainsKey("workbench") || BuiltStructures.ContainsKey("advanced_workshop");

    public bool HasHome() =>
        BuiltStructures.Any(s => AllBlueprints.TryGetValue(s.Key, out var bp) &&
            (bp.Type == StructureType.Nest || bp.Type == StructureType.House) &&
            s.Value.IsUsable());

    public Structure? GetHome() =>
        BuiltStructures.Values
            .Where(s => AllBlueprints.TryGetValue(s.BlueprintId, out var bp) &&
                (bp.Type == StructureType.Nest || bp.Type == StructureType.House) &&
                s.IsUsable())
            .OrderByDescending(s => AllBlueprints.TryGetValue(s.BlueprintId, out var bp) ? bp.XpReward : 0)
            .FirstOrDefault();

    // =============================================================================
    // SKILL PROGRESSION
    // =============================================================================

    private void CheckSkillUp()
    {
        for (var level = 0; level < SkillThresholds.Length; level++)
        {
            if (BuildingXp >= SkillThresholds[level])
                BuildingSkill = Math.Max(BuildingSkill, level + 1);
        }
    }

    private void CheckBlueprintUnlocks()
    {
        foreach (var (bpId, bp) in AllBlueprints)
        {
            if (!BlueprintsUnlocked.Contains(bpId) && bp.BuildingSkillRequired <= BuildingSkill)
                BlueprintsUnlocked.Add(bpId);
        }
    }

    // =============================================================================
    // STATUS
    // =============================================================================

    public string GetBuildingStatus()
    {
        if (CurrentProject == null)
            return "No active project";

        var progress = (int)((float)CurrentProject.BuildProgress / CurrentProject.MaxProgress * 100);
        return $"Building {CurrentProject.Name}: {progress}%";
    }

    public List<Structure> GetAllStructures() => BuiltStructures.Values.ToList();

    public List<Structure> GetStructuresNeedingRepair() =>
        BuiltStructures.Values
            .Where(s => s.Status == StructureStatus.Damaged || s.Durability < s.MaxDurability * 0.5f)
            .ToList();

    // =============================================================================
    // SERIALIZATION
    // =============================================================================

    public BuildingSaveData ToSaveData() => new()
    {
        Skill = BuildingSkill,
        Xp = BuildingXp,
        Unlocked = BlueprintsUnlocked,
        Structures = BuiltStructures.ToDictionary(
            kvp => kvp.Key,
            kvp => new StructureSaveData
            {
                BlueprintId = kvp.Value.BlueprintId,
                Name = kvp.Value.Name,
                Status = kvp.Value.Status.ToString(),
                Durability = kvp.Value.Durability,
                MaxDurability = kvp.Value.MaxDurability,
                CompletedAt = kvp.Value.CompletedAt?.ToString("o")
            })
    };

    public static BuildingSystem FromSaveData(BuildingSaveData data)
    {
        var system = new BuildingSystem
        {
            BuildingSkill = data.Skill > 0 ? data.Skill : 1,
            BuildingXp = data.Xp,
            BlueprintsUnlocked = data.Unlocked ?? new()
        };

        if (data.Structures != null)
        {
            foreach (var (structId, sData) in data.Structures)
            {
                Enum.TryParse<StructureStatus>(sData.Status, out var status);

                var structure = new Structure
                {
                    Id = structId,
                    BlueprintId = sData.BlueprintId ?? structId,
                    Name = sData.Name ?? structId,
                    Status = status,
                    Durability = sData.Durability,
                    MaxDurability = sData.MaxDurability > 0 ? sData.MaxDurability : 100,
                    BuildProgress = status == StructureStatus.Complete ? 1 : 0,
                    MaxProgress = 1
                };

                if (!string.IsNullOrEmpty(sData.CompletedAt) && DateTime.TryParse(sData.CompletedAt, out var completed))
                    structure.CompletedAt = completed;

                // Restore bonuses from blueprint
                if (AllBlueprints.TryGetValue(structure.BlueprintId, out var bp))
                    structure.Bonuses = new Dictionary<string, float>(bp.Bonuses);

                system.BuiltStructures[structId] = structure;
            }
        }

        system.UnlockStartingBlueprints();
        return system;
    }
}

public class StructureSaveData
{
    public string? BlueprintId { get; set; }
    public string? Name { get; set; }
    public string? Status { get; set; }
    public int Durability { get; set; }
    public int MaxDurability { get; set; }
    public string? CompletedAt { get; set; }
}

public class BuildingSaveData
{
    public int Skill { get; set; }
    public int Xp { get; set; }
    public List<string>? Unlocked { get; set; }
    public Dictionary<string, StructureSaveData>? Structures { get; set; }
}
