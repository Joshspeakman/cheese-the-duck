using System;
using System.Collections.Generic;
using System.Linq;

namespace StupidDuck.World;

/// <summary>
/// Categories of craftable items.
/// </summary>
public enum CraftingCategory
{
    Tool,           // Hammers, fishing rods, etc.
    Building,       // Planks, bricks, thatch
    Decoration,     // Pretty things for the nest/house
    Utility,        // Rope, containers, etc.
    Food,           // Prepared food items
    Special         // Rare/magical items
}

/// <summary>
/// A recipe for crafting an item.
/// </summary>
public class CraftingRecipe
{
    public string Id { get; set; } = "";
    public string Name { get; set; } = "";
    public string Description { get; set; } = "";
    public CraftingCategory Category { get; set; }
    public Dictionary<string, int> Ingredients { get; set; } = new();
    public string ResultId { get; set; } = "";
    public int ResultAmount { get; set; } = 1;
    public float CraftingTime { get; set; } = 1.0f;
    public int SkillRequired { get; set; } = 1;
    public int UnlockLevel { get; set; } = 1;
    public int XpReward { get; set; } = 10;
    public string? RequiresTool { get; set; }
    public bool RequiresWorkbench { get; set; }

    public (bool CanCraft, string Reason) CheckCanCraft(MaterialInventory inventory, int skill, int level, bool hasTool = true, bool hasWorkbench = true)
    {
        if (skill < SkillRequired)
            return (false, $"Need crafting skill {SkillRequired} (have {skill})");

        if (level < UnlockLevel)
            return (false, $"Unlock at level {UnlockLevel}");

        if (RequiresWorkbench && !hasWorkbench)
            return (false, "Need a workbench to craft this");

        if (!string.IsNullOrEmpty(RequiresTool) && !hasTool)
            return (false, $"Need {RequiresTool} to craft this");

        foreach (var (matId, amount) in Ingredients)
        {
            var have = inventory.GetCount(matId);
            if (have < amount)
            {
                var matName = Materials.AllMaterials.TryGetValue(matId, out var mat) ? mat.Name : matId;
                return (false, $"Need {amount}x {matName} (have {have})");
            }
        }

        return (true, "Ready to craft!");
    }
}

/// <summary>
/// Tracks an in-progress crafting operation.
/// </summary>
public class CraftingProgress
{
    public string RecipeId { get; set; } = "";
    public DateTime StartTime { get; set; }
    public float Duration { get; set; }

    public float GetProgress()
    {
        var elapsed = (float)(DateTime.UtcNow - StartTime).TotalSeconds;
        return Math.Min(1.0f, elapsed / Duration);
    }

    public bool IsComplete() => GetProgress() >= 1.0f;
}

/// <summary>
/// A crafted tool with durability.
/// </summary>
public class CraftedTool
{
    public string Id { get; set; } = "";
    public string Name { get; set; } = "";
    public int Durability { get; set; } = 100;
    public int MaxDurability { get; set; } = 100;
    public string BonusType { get; set; } = "";
    public float BonusAmount { get; set; }
}

/// <summary>
/// System for managing crafting operations and skill progression.
/// </summary>
public class CraftingSystem
{
    // =============================================================================
    // RECIPE DEFINITIONS
    // =============================================================================

    public static readonly Dictionary<string, CraftingRecipe> AllRecipes = new()
    {
        // === BUILDING MATERIALS ===
        ["woven_grass"] = new()
        {
            Id = "woven_grass",
            Name = "Woven Grass Mat",
            Description = "Weave grass into a useful mat.",
            Category = CraftingCategory.Building,
            Ingredients = new() { ["grass_blade"] = 10 },
            ResultId = "woven_grass",
            CraftingTime = 2.0f,
            SkillRequired = 1,
            UnlockLevel = 1,
            XpReward = 5
        },
        ["rope"] = new()
        {
            Id = "rope",
            Name = "Rope",
            Description = "Twist fibers into strong rope.",
            Category = CraftingCategory.Utility,
            Ingredients = new() { ["reed"] = 5, ["grass_blade"] = 5 },
            ResultId = "rope",
            CraftingTime = 3.0f,
            SkillRequired = 2,
            UnlockLevel = 2,
            XpReward = 10
        },
        ["thatch"] = new()
        {
            Id = "thatch",
            Name = "Thatch Bundle",
            Description = "Bundle reeds into roofing material.",
            Category = CraftingCategory.Building,
            Ingredients = new() { ["reed"] = 8, ["grass_blade"] = 4 },
            ResultId = "thatch",
            CraftingTime = 2.5f,
            SkillRequired = 2,
            UnlockLevel = 3,
            XpReward = 10
        },
        ["clay_brick"] = new()
        {
            Id = "clay_brick",
            Name = "Clay Brick",
            Description = "Shape and dry clay into a brick.",
            Category = CraftingCategory.Building,
            Ingredients = new() { ["clay"] = 3, ["sand"] = 1 },
            ResultId = "clay_brick",
            CraftingTime = 4.0f,
            SkillRequired = 3,
            UnlockLevel = 5,
            XpReward = 15
        },
        ["wooden_plank"] = new()
        {
            Id = "wooden_plank",
            Name = "Wooden Plank",
            Description = "Carve driftwood into a plank.",
            Category = CraftingCategory.Building,
            Ingredients = new() { ["driftwood"] = 2, ["twig"] = 4 },
            ResultId = "wooden_plank",
            CraftingTime = 5.0f,
            SkillRequired = 3,
            UnlockLevel = 6,
            XpReward = 20,
            RequiresTool = "stone_hammer"
        },
        ["stone_block"] = new()
        {
            Id = "stone_block",
            Name = "Stone Block",
            Description = "Shape rocks into a building block.",
            Category = CraftingCategory.Building,
            Ingredients = new() { ["rock"] = 4, ["pebble"] = 6 },
            ResultId = "stone_block",
            CraftingTime = 6.0f,
            SkillRequired = 4,
            UnlockLevel = 8,
            XpReward = 25,
            RequiresTool = "stone_hammer"
        },
        ["insulation"] = new()
        {
            Id = "insulation",
            Name = "Insulation",
            Description = "Soft materials for warmth.",
            Category = CraftingCategory.Building,
            Ingredients = new() { ["feather"] = 5, ["moss"] = 3, ["leaf"] = 8 },
            ResultId = "insulation",
            CraftingTime = 3.0f,
            SkillRequired = 2,
            UnlockLevel = 4,
            XpReward = 10
        },
        // === TOOLS ===
        ["stone_hammer"] = new()
        {
            Id = "stone_hammer",
            Name = "Stone Hammer",
            Description = "A basic hammer for building.",
            Category = CraftingCategory.Tool,
            Ingredients = new() { ["rock"] = 2, ["twig"] = 3, ["reed"] = 2 },
            ResultId = "stone_hammer",
            CraftingTime = 4.0f,
            SkillRequired = 2,
            UnlockLevel = 3,
            XpReward = 20
        },
        ["fishing_rod"] = new()
        {
            Id = "fishing_rod",
            Name = "Fishing Rod",
            Description = "A simple rod for catching fish.",
            Category = CraftingCategory.Tool,
            Ingredients = new() { ["twig"] = 5, ["string"] = 2, ["worm"] = 1 },
            ResultId = "fishing_rod",
            CraftingTime = 5.0f,
            SkillRequired = 3,
            UnlockLevel = 5,
            XpReward = 25
        },
        ["gathering_bag"] = new()
        {
            Id = "gathering_bag",
            Name = "Gathering Bag",
            Description = "Carry more materials!",
            Category = CraftingCategory.Tool,
            Ingredients = new() { ["fabric_scrap"] = 3, ["string"] = 2, ["leaf"] = 5 },
            ResultId = "gathering_bag",
            CraftingTime = 4.0f,
            SkillRequired = 2,
            UnlockLevel = 4,
            XpReward = 20
        },
        ["digging_stick"] = new()
        {
            Id = "digging_stick",
            Name = "Digging Stick",
            Description = "For digging up treasures.",
            Category = CraftingCategory.Tool,
            Ingredients = new() { ["twig"] = 4, ["smooth_stone"] = 1 },
            ResultId = "digging_stick",
            CraftingTime = 3.0f,
            SkillRequired = 2,
            UnlockLevel = 3,
            XpReward = 15
        },
        // === DECORATIONS ===
        ["flower_wreath"] = new()
        {
            Id = "flower_wreath",
            Name = "Flower Wreath",
            Description = "A pretty wreath of flowers.",
            Category = CraftingCategory.Decoration,
            Ingredients = new() { ["wildflower"] = 6, ["grass_blade"] = 4 },
            ResultId = "flower_wreath",
            CraftingTime = 2.0f,
            SkillRequired = 1,
            UnlockLevel = 2,
            XpReward = 10
        },
        ["shell_mobile"] = new()
        {
            Id = "shell_mobile",
            Name = "Shell Mobile",
            Description = "Shells that clink in the wind.",
            Category = CraftingCategory.Decoration,
            Ingredients = new() { ["shell"] = 5, ["string"] = 1, ["twig"] = 2 },
            ResultId = "shell_mobile",
            CraftingTime = 3.0f,
            SkillRequired = 2,
            UnlockLevel = 4,
            XpReward = 15
        },
        ["pebble_path"] = new()
        {
            Id = "pebble_path",
            Name = "Pebble Path",
            Description = "A decorative path of pebbles.",
            Category = CraftingCategory.Decoration,
            Ingredients = new() { ["pebble"] = 10, ["sand"] = 5 },
            ResultId = "pebble_path",
            CraftingTime = 4.0f,
            SkillRequired = 2,
            UnlockLevel = 5,
            XpReward = 15
        },
        ["moss_carpet"] = new()
        {
            Id = "moss_carpet",
            Name = "Moss Carpet",
            Description = "Soft, cozy floor covering.",
            Category = CraftingCategory.Decoration,
            Ingredients = new() { ["moss"] = 8, ["woven_grass"] = 2 },
            ResultId = "moss_carpet",
            CraftingTime = 3.5f,
            SkillRequired = 3,
            UnlockLevel = 6,
            XpReward = 20
        },
        // === UTILITY ===
        ["storage_basket"] = new()
        {
            Id = "storage_basket",
            Name = "Storage Basket",
            Description = "A woven basket for storage.",
            Category = CraftingCategory.Utility,
            Ingredients = new() { ["reed"] = 10, ["grass_blade"] = 6 },
            ResultId = "storage_basket",
            CraftingTime = 4.0f,
            SkillRequired = 2,
            UnlockLevel = 3,
            XpReward = 15
        },
        ["water_bowl"] = new()
        {
            Id = "water_bowl",
            Name = "Water Bowl",
            Description = "A clay bowl for water.",
            Category = CraftingCategory.Utility,
            Ingredients = new() { ["clay"] = 5, ["pebble"] = 2 },
            ResultId = "water_bowl",
            CraftingTime = 3.5f,
            SkillRequired = 2,
            UnlockLevel = 4,
            XpReward = 15
        },
        ["torch"] = new()
        {
            Id = "torch",
            Name = "Torch",
            Description = "Light the way!",
            Category = CraftingCategory.Utility,
            Ingredients = new() { ["twig"] = 3, ["bark"] = 2, ["fabric_scrap"] = 1 },
            ResultId = "torch",
            CraftingTime = 2.0f,
            SkillRequired = 2,
            UnlockLevel = 5,
            XpReward = 10
        },
        // === FOOD ===
        ["berry_salad"] = new()
        {
            Id = "berry_salad",
            Name = "Berry Salad",
            Description = "A healthy mix of berries.",
            Category = CraftingCategory.Food,
            Ingredients = new() { ["berry"] = 5, ["clover"] = 2 },
            ResultId = "berry_salad",
            CraftingTime = 1.0f,
            SkillRequired = 1,
            UnlockLevel = 2,
            XpReward = 5
        },
        ["honey_bread"] = new()
        {
            Id = "honey_bread",
            Name = "Honey Bread",
            Description = "Sweet honey on bread crumbs!",
            Category = CraftingCategory.Food,
            Ingredients = new() { ["bread_crumb"] = 5, ["honeycomb"] = 1, ["seed"] = 3 },
            ResultId = "honey_bread",
            CraftingTime = 3.0f,
            SkillRequired = 3,
            UnlockLevel = 7,
            XpReward = 20
        },
        // === SPECIAL ===
        ["lucky_charm"] = new()
        {
            Id = "lucky_charm",
            Name = "Lucky Charm",
            Description = "Increases rare find chance!",
            Category = CraftingCategory.Special,
            Ingredients = new() { ["lucky_clover"] = 1, ["butterfly_wing"] = 1, ["river_pearl"] = 1 },
            ResultId = "lucky_charm",
            CraftingTime = 10.0f,
            SkillRequired = 5,
            UnlockLevel = 12,
            XpReward = 75
        },
        ["magic_wand"] = new()
        {
            Id = "magic_wand",
            Name = "Magic Wand",
            Description = "Channel magical energy!",
            Category = CraftingCategory.Special,
            Ingredients = new() { ["magic_acorn"] = 1, ["fairy_dust"] = 2, ["crystal"] = 1, ["eagle_feather"] = 1 },
            ResultId = "magic_wand",
            CraftingTime = 15.0f,
            SkillRequired = 6,
            UnlockLevel = 20,
            XpReward = 200
        }
    };

    // XP thresholds for skill levels
    private static readonly int[] SkillThresholds = { 0, 50, 150, 350, 600, 1000, 1500, 2200, 3000, 4000 };

    // =============================================================================
    // STATE
    // =============================================================================

    public int CraftingSkill { get; set; } = 1;
    public int CraftingXp { get; set; }
    public List<string> RecipesUnlocked { get; set; } = new();
    public CraftingProgress? CurrentCraft { get; set; }
    public Dictionary<string, int> CraftedCount { get; set; } = new();
    public Dictionary<string, CraftedTool> Tools { get; set; } = new();
    private int _playerLevel = 1;

    public CraftingSystem()
    {
        UnlockStartingRecipes();
    }

    private void UnlockStartingRecipes()
    {
        foreach (var (id, recipe) in AllRecipes)
        {
            if (recipe.UnlockLevel <= 1 && recipe.SkillRequired <= 1 && !RecipesUnlocked.Contains(id))
                RecipesUnlocked.Add(id);
        }
    }

    // =============================================================================
    // RECIPE ACCESS
    // =============================================================================

    public List<string> GetAvailableRecipes(MaterialInventory inventory, int? playerLevel = null)
    {
        var level = playerLevel ?? _playerLevel;
        var available = new List<string>();

        foreach (var recipeId in RecipesUnlocked)
        {
            if (!AllRecipes.TryGetValue(recipeId, out var recipe))
                continue;

            var (canCraft, _) = recipe.CheckCanCraft(
                inventory, CraftingSkill, level,
                HasTool(recipe.RequiresTool), true);

            if (canCraft)
                available.Add(recipe.ResultId);
        }

        return available;
    }

    public List<CraftingRecipe> GetAllKnownRecipes() =>
        RecipesUnlocked
            .Where(r => AllRecipes.ContainsKey(r))
            .Select(r => AllRecipes[r])
            .ToList();

    private bool HasTool(string? toolId) =>
        string.IsNullOrEmpty(toolId) || (Tools.TryGetValue(toolId, out var tool) && tool.Durability > 0);

    // =============================================================================
    // CRAFTING
    // =============================================================================

    public (bool Success, string Message) StartCrafting(string recipeId, MaterialInventory inventory, int? playerLevel = null)
    {
        var level = playerLevel ?? _playerLevel;

        if (CurrentCraft != null)
            return (false, "Already crafting something!");

        if (!AllRecipes.TryGetValue(recipeId, out var recipe))
            return (false, $"Unknown recipe: {recipeId}");

        if (!RecipesUnlocked.Contains(recipeId))
            return (false, "Recipe not unlocked yet");

        var (canCraft, reason) = recipe.CheckCanCraft(
            inventory, CraftingSkill, level,
            HasTool(recipe.RequiresTool), true);

        if (!canCraft)
            return (false, reason);

        // Consume materials
        foreach (var (matId, amount) in recipe.Ingredients)
            inventory.RemoveMaterial(matId, amount);

        // Start crafting
        CurrentCraft = new CraftingProgress
        {
            RecipeId = recipeId,
            StartTime = DateTime.UtcNow,
            Duration = recipe.CraftingTime
        };

        // Use tool durability
        if (!string.IsNullOrEmpty(recipe.RequiresTool) && Tools.TryGetValue(recipe.RequiresTool, out var tool))
            tool.Durability--;

        return (true, $"Started crafting {recipe.Name}...");
    }

    public CraftingResult CheckCrafting(MaterialInventory? inventory = null)
    {
        if (CurrentCraft == null)
            return new CraftingResult { Completed = false };

        if (!CurrentCraft.IsComplete())
        {
            var progress = (int)(CurrentCraft.GetProgress() * 100);
            return new CraftingResult { Completed = false, Progress = progress, Message = $"Crafting... {progress}%" };
        }

        if (!AllRecipes.TryGetValue(CurrentCraft.RecipeId, out var recipe))
        {
            CurrentCraft = null;
            return new CraftingResult { Completed = false, Message = "Error: Recipe not found" };
        }

        // Track stats
        CraftedCount[recipe.Id] = CraftedCount.GetValueOrDefault(recipe.Id) + 1;

        // Award XP
        CraftingXp += recipe.XpReward;
        CheckSkillUp();

        // Check for new recipe unlocks
        var newUnlocks = CheckRecipeUnlocks();

        // If it's a tool, add to tools
        if (recipe.Category == CraftingCategory.Tool)
            AddTool(recipe.ResultId, recipe.Name);

        var result = new CraftingResult
        {
            Completed = true,
            ResultItem = recipe.ResultId,
            Quantity = recipe.ResultAmount,
            XpGained = recipe.XpReward,
            Message = $"Crafted {recipe.ResultAmount}x {recipe.Name}! (+{recipe.XpReward} XP)",
            NewUnlocks = newUnlocks
        };

        CurrentCraft = null;
        return result;
    }

    public string CancelCrafting(MaterialInventory inventory)
    {
        if (CurrentCraft == null)
            return "Not crafting anything";

        if (AllRecipes.TryGetValue(CurrentCraft.RecipeId, out var recipe))
        {
            // Refund 50% of materials
            foreach (var (matId, amount) in recipe.Ingredients)
            {
                var refund = Math.Max(1, amount / 2);
                inventory.AddMaterial(matId, refund);
            }
        }

        CurrentCraft = null;
        return "Crafting cancelled. 50% materials refunded.";
    }

    private void AddTool(string toolId, string name)
    {
        var toolProps = new Dictionary<string, (string BonusType, float BonusAmount)>
        {
            ["stone_hammer"] = ("building", 0.2f),
            ["fishing_rod"] = ("fishing", 0.5f),
            ["gathering_bag"] = ("gathering", 0.3f),
            ["digging_stick"] = ("digging", 0.4f)
        };

        var (bonusType, bonusAmount) = toolProps.GetValueOrDefault(toolId, ("", 0f));

        Tools[toolId] = new CraftedTool
        {
            Id = toolId,
            Name = name,
            Durability = 100,
            MaxDurability = 100,
            BonusType = bonusType,
            BonusAmount = bonusAmount
        };
    }

    private void CheckSkillUp()
    {
        for (var level = 0; level < SkillThresholds.Length; level++)
        {
            if (CraftingXp >= SkillThresholds[level])
                CraftingSkill = Math.Max(CraftingSkill, level + 1);
        }
    }

    private List<string> CheckRecipeUnlocks()
    {
        var newUnlocks = new List<string>();
        foreach (var (recipeId, recipe) in AllRecipes)
        {
            if (!RecipesUnlocked.Contains(recipeId) && recipe.SkillRequired <= CraftingSkill)
            {
                RecipesUnlocked.Add(recipeId);
                newUnlocks.Add(recipe.Name);
            }
        }
        return newUnlocks;
    }

    public string GetCraftingStatus()
    {
        if (CurrentCraft == null)
            return "Not crafting";

        if (!AllRecipes.TryGetValue(CurrentCraft.RecipeId, out var recipe))
            return "Unknown craft";

        var progress = (int)(CurrentCraft.GetProgress() * 100);
        return $"Crafting {recipe.Name}... {progress}%";
    }

    // =============================================================================
    // SERIALIZATION
    // =============================================================================

    public CraftingSaveData ToSaveData() => new()
    {
        Skill = CraftingSkill,
        Xp = CraftingXp,
        Unlocked = RecipesUnlocked,
        CraftedCount = CraftedCount,
        Tools = Tools.ToDictionary(
            kvp => kvp.Key,
            kvp => new CraftedToolSaveData { Name = kvp.Value.Name, Durability = kvp.Value.Durability })
    };

    public static CraftingSystem FromSaveData(CraftingSaveData data)
    {
        var system = new CraftingSystem
        {
            CraftingSkill = data.Skill > 0 ? data.Skill : 1,
            CraftingXp = data.Xp,
            RecipesUnlocked = data.Unlocked ?? new(),
            CraftedCount = data.CraftedCount ?? new()
        };

        if (data.Tools != null)
        {
            foreach (var (toolId, toolData) in data.Tools)
            {
                system.Tools[toolId] = new CraftedTool
                {
                    Id = toolId,
                    Name = toolData.Name ?? toolId,
                    Durability = toolData.Durability
                };
            }
        }

        system.UnlockStartingRecipes();
        return system;
    }
}

public class CraftingResult
{
    public bool Completed { get; set; }
    public int Progress { get; set; }
    public string? ResultItem { get; set; }
    public int Quantity { get; set; }
    public int XpGained { get; set; }
    public string Message { get; set; } = "";
    public List<string> NewUnlocks { get; set; } = new();
}

public class CraftedToolSaveData
{
    public string? Name { get; set; }
    public int Durability { get; set; }
}

public class CraftingSaveData
{
    public int Skill { get; set; }
    public int Xp { get; set; }
    public List<string>? Unlocked { get; set; }
    public Dictionary<string, int>? CraftedCount { get; set; }
    public Dictionary<string, CraftedToolSaveData>? Tools { get; set; }
}
