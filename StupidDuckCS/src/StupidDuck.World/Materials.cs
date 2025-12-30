using System;
using System.Collections.Generic;
using System.Linq;

namespace StupidDuck.World;

/// <summary>
/// Categories of materials.
/// </summary>
public enum MaterialCategory
{
    Plant,      // Leaves, grass, flowers, seeds
    Wood,       // Twigs, bark, branches, driftwood
    Stone,      // Pebbles, rocks, crystals
    Earth,      // Clay, sand, mud
    Water,      // Shells, pearls, seaweed
    Fiber,      // String, fabric, reeds
    Food,       // Berries, seeds, fish
    Rare,       // Special/magical items
    Crafted     // Items made from other materials
}

/// <summary>
/// Definition of a gatherable/craftable material.
/// </summary>
public class Material
{
    public string Id { get; set; } = "";
    public string Name { get; set; } = "";
    public string Description { get; set; } = "";
    public MaterialCategory Category { get; set; }
    public int Rarity { get; set; } = 1;        // 1-5, higher = rarer
    public int StackSize { get; set; } = 99;    // Max per stack
    public int Value { get; set; } = 1;         // Base value for trading
    public int Strength { get; set; } = 1;      // For building durability
    public int Warmth { get; set; }             // For insulation
    public int Beauty { get; set; }             // For decoration
    public bool Waterproof { get; set; }
}

/// <summary>
/// A stack of materials in inventory.
/// </summary>
public class MaterialStack
{
    public string MaterialId { get; set; } = "";
    public int Quantity { get; set; }

    public bool CanAdd(int amount)
    {
        if (!Materials.AllMaterials.TryGetValue(MaterialId, out var mat))
            return false;
        return Quantity + amount <= mat.StackSize;
    }

    public int Add(int amount)
    {
        if (!Materials.AllMaterials.TryGetValue(MaterialId, out var mat))
            return amount;

        var canAdd = mat.StackSize - Quantity;
        var actual = Math.Min(amount, canAdd);
        Quantity += actual;
        return amount - actual;
    }

    public int Remove(int amount)
    {
        var actual = Math.Min(amount, Quantity);
        Quantity -= actual;
        return actual;
    }
}

/// <summary>
/// All material definitions.
/// </summary>
public static class Materials
{
    public static readonly Dictionary<string, Material> AllMaterials = new()
    {
        // PLANT materials
        ["leaf"] = new() { Id = "leaf", Name = "Leaf", Description = "A fallen leaf.", Category = MaterialCategory.Plant, Rarity = 1, StackSize = 99, Value = 1, Strength = 1, Warmth = 1, Beauty = 1 },
        ["grass_blade"] = new() { Id = "grass_blade", Name = "Grass Blade", Description = "Long blade of grass.", Category = MaterialCategory.Plant, Rarity = 1, StackSize = 99, Value = 1, Strength = 1, Warmth = 1 },
        ["wildflower"] = new() { Id = "wildflower", Name = "Wildflower", Description = "A pretty flower.", Category = MaterialCategory.Plant, Rarity = 1, StackSize = 50, Value = 2, Beauty = 3 },
        ["clover"] = new() { Id = "clover", Name = "Clover", Description = "A lucky clover.", Category = MaterialCategory.Plant, Rarity = 1, StackSize = 99, Value = 1, Strength = 1, Beauty = 1 },
        ["dandelion"] = new() { Id = "dandelion", Name = "Dandelion", Description = "Fluffy dandelion.", Category = MaterialCategory.Plant, Rarity = 1, StackSize = 99, Value = 1, Beauty = 1 },
        ["moss"] = new() { Id = "moss", Name = "Moss", Description = "Soft green moss.", Category = MaterialCategory.Plant, Rarity = 2, StackSize = 50, Value = 3, Strength = 2, Warmth = 3, Beauty = 2 },
        ["pine_needle"] = new() { Id = "pine_needle", Name = "Pine Needle", Description = "Fragrant pine needle.", Category = MaterialCategory.Plant, Rarity = 1, StackSize = 99, Value = 1, Strength = 1, Warmth = 1, Beauty = 1 },
        ["mushroom"] = new() { Id = "mushroom", Name = "Mushroom", Description = "A forest mushroom.", Category = MaterialCategory.Plant, Rarity = 2, StackSize = 30, Value = 3, Beauty = 1 },
        ["pond_weed"] = new() { Id = "pond_weed", Name = "Pond Weed", Description = "Aquatic plant.", Category = MaterialCategory.Plant, Rarity = 1, StackSize = 99, Value = 1, Strength = 1 },
        ["lily_pad"] = new() { Id = "lily_pad", Name = "Lily Pad", Description = "Floating lily pad.", Category = MaterialCategory.Plant, Rarity = 2, StackSize = 30, Value = 3, Strength = 1, Beauty = 2, Waterproof = true },
        ["garden_flower"] = new() { Id = "garden_flower", Name = "Garden Flower", Description = "Cultivated flower.", Category = MaterialCategory.Plant, Rarity = 2, StackSize = 50, Value = 4, Beauty = 4 },
        
        // WOOD materials
        ["twig"] = new() { Id = "twig", Name = "Twig", Description = "A small twig.", Category = MaterialCategory.Wood, Rarity = 1, StackSize = 99, Value = 1, Strength = 2 },
        ["bark"] = new() { Id = "bark", Name = "Bark", Description = "Tree bark.", Category = MaterialCategory.Wood, Rarity = 2, StackSize = 50, Value = 2, Strength = 3, Warmth = 1 },
        ["acorn"] = new() { Id = "acorn", Name = "Acorn", Description = "A small acorn.", Category = MaterialCategory.Wood, Rarity = 1, StackSize = 99, Value = 2, Strength = 1 },
        ["pine_cone"] = new() { Id = "pine_cone", Name = "Pine Cone", Description = "A pine cone.", Category = MaterialCategory.Wood, Rarity = 1, StackSize = 50, Value = 2, Strength = 2, Beauty = 1 },
        ["driftwood"] = new() { Id = "driftwood", Name = "Driftwood", Description = "Weathered driftwood.", Category = MaterialCategory.Wood, Rarity = 2, StackSize = 30, Value = 4, Strength = 4, Beauty = 2, Waterproof = true },
        
        // STONE materials
        ["pebble"] = new() { Id = "pebble", Name = "Pebble", Description = "A small pebble.", Category = MaterialCategory.Stone, Rarity = 1, StackSize = 99, Value = 1, Strength = 3 },
        ["smooth_stone"] = new() { Id = "smooth_stone", Name = "Smooth Stone", Description = "Polished by water.", Category = MaterialCategory.Stone, Rarity = 2, StackSize = 50, Value = 3, Strength = 4, Beauty = 1 },
        ["rock"] = new() { Id = "rock", Name = "Rock", Description = "A solid rock.", Category = MaterialCategory.Stone, Rarity = 2, StackSize = 30, Value = 4, Strength = 5 },
        ["crystal"] = new() { Id = "crystal", Name = "Crystal", Description = "A sparkling crystal!", Category = MaterialCategory.Rare, Rarity = 4, StackSize = 20, Value = 25, Strength = 3, Beauty = 8 },
        
        // EARTH materials
        ["clay"] = new() { Id = "clay", Name = "Clay", Description = "Moldable clay.", Category = MaterialCategory.Earth, Rarity = 1, StackSize = 50, Value = 2, Strength = 2, Waterproof = true },
        ["pond_clay"] = new() { Id = "pond_clay", Name = "Pond Clay", Description = "Clay from the pond.", Category = MaterialCategory.Earth, Rarity = 1, StackSize = 50, Value = 2, Strength = 2, Waterproof = true },
        ["sand"] = new() { Id = "sand", Name = "Sand", Description = "Fine sand.", Category = MaterialCategory.Earth, Rarity = 1, StackSize = 99, Value = 1, Strength = 1 },
        
        // WATER/SHELL materials
        ["shell"] = new() { Id = "shell", Name = "Shell", Description = "A pretty shell.", Category = MaterialCategory.Water, Rarity = 1, StackSize = 50, Value = 2, Strength = 2, Beauty = 2 },
        ["sea_shell"] = new() { Id = "sea_shell", Name = "Sea Shell", Description = "Ocean shell.", Category = MaterialCategory.Water, Rarity = 1, StackSize = 50, Value = 3, Strength = 3, Beauty = 3 },
        ["sea_glass"] = new() { Id = "sea_glass", Name = "Sea Glass", Description = "Smooth sea glass.", Category = MaterialCategory.Water, Rarity = 2, StackSize = 30, Value = 5, Strength = 2, Beauty = 5 },
        ["seaweed"] = new() { Id = "seaweed", Name = "Seaweed", Description = "Ocean seaweed.", Category = MaterialCategory.Water, Rarity = 1, StackSize = 99, Value = 1, Strength = 1, Waterproof = true },
        ["river_pearl"] = new() { Id = "river_pearl", Name = "River Pearl", Description = "A rare pearl!", Category = MaterialCategory.Rare, Rarity = 4, StackSize = 10, Value = 30, Strength = 1, Beauty = 10 },
        
        // FIBER materials
        ["reed"] = new() { Id = "reed", Name = "Reed", Description = "A sturdy reed.", Category = MaterialCategory.Fiber, Rarity = 1, StackSize = 99, Value = 2, Strength = 2, Waterproof = true },
        ["string"] = new() { Id = "string", Name = "String", Description = "A length of string.", Category = MaterialCategory.Fiber, Rarity = 2, StackSize = 50, Value = 4, Strength = 1 },
        ["fabric_scrap"] = new() { Id = "fabric_scrap", Name = "Fabric Scrap", Description = "Piece of fabric.", Category = MaterialCategory.Fiber, Rarity = 2, StackSize = 30, Value = 5, Strength = 1, Warmth = 3, Beauty = 1 },
        ["feather"] = new() { Id = "feather", Name = "Feather", Description = "A soft feather.", Category = MaterialCategory.Fiber, Rarity = 2, StackSize = 50, Value = 3, Warmth = 2, Beauty = 2 },
        
        // FOOD materials
        ["berry"] = new() { Id = "berry", Name = "Berry", Description = "A tasty berry.", Category = MaterialCategory.Food, Rarity = 1, StackSize = 50, Value = 2, Beauty = 1 },
        ["seed"] = new() { Id = "seed", Name = "Seed", Description = "A plantable seed.", Category = MaterialCategory.Food, Rarity = 1, StackSize = 99, Value = 1 },
        ["vegetable_seed"] = new() { Id = "vegetable_seed", Name = "Vegetable Seed", Description = "Garden vegetable seed.", Category = MaterialCategory.Food, Rarity = 2, StackSize = 50, Value = 3 },
        ["worm"] = new() { Id = "worm", Name = "Worm", Description = "A wiggly worm.", Category = MaterialCategory.Food, Rarity = 1, StackSize = 30, Value = 2 },
        ["small_fish"] = new() { Id = "small_fish", Name = "Small Fish", Description = "A tiny fish.", Category = MaterialCategory.Food, Rarity = 2, StackSize = 20, Value = 5 },
        ["bread_crumb"] = new() { Id = "bread_crumb", Name = "Bread Crumb", Description = "Precious bread!", Category = MaterialCategory.Food, Rarity = 1, StackSize = 99, Value = 2 },
        ["honeycomb"] = new() { Id = "honeycomb", Name = "Honeycomb", Description = "Sweet honeycomb.", Category = MaterialCategory.Food, Rarity = 3, StackSize = 20, Value = 10, Beauty = 2 },
        
        // RARE/SPECIAL materials
        ["butterfly_wing"] = new() { Id = "butterfly_wing", Name = "Butterfly Wing", Description = "A delicate wing.", Category = MaterialCategory.Rare, Rarity = 3, StackSize = 20, Value = 8, Beauty = 6 },
        ["fairy_dust"] = new() { Id = "fairy_dust", Name = "Fairy Dust", Description = "Magical sparkling dust!", Category = MaterialCategory.Rare, Rarity = 5, StackSize = 10, Value = 100, Beauty = 10 },
        ["lucky_clover"] = new() { Id = "lucky_clover", Name = "Lucky Clover", Description = "Four-leaf clover!", Category = MaterialCategory.Rare, Rarity = 3, StackSize = 20, Value = 25, Beauty = 3 },
        ["shiny_button"] = new() { Id = "shiny_button", Name = "Shiny Button", Description = "A shiny button.", Category = MaterialCategory.Rare, Rarity = 2, StackSize = 30, Value = 5, Beauty = 3 },
        ["eagle_feather"] = new() { Id = "eagle_feather", Name = "Eagle Feather", Description = "A majestic eagle feather!", Category = MaterialCategory.Rare, Rarity = 4, StackSize = 10, Value = 20, Warmth = 1, Beauty = 8 },
        ["magic_acorn"] = new() { Id = "magic_acorn", Name = "Magic Acorn", Description = "Glows softly...", Category = MaterialCategory.Rare, Rarity = 4, StackSize = 10, Value = 50, Strength = 3, Warmth = 2, Beauty = 5 },
        
        // CRAFTED materials
        ["woven_grass"] = new() { Id = "woven_grass", Name = "Woven Grass", Description = "Grass woven into a mat.", Category = MaterialCategory.Crafted, Rarity = 2, StackSize = 30, Value = 5, Strength = 3, Warmth = 2, Beauty = 1, Waterproof = true },
        ["rope"] = new() { Id = "rope", Name = "Rope", Description = "Strong woven rope.", Category = MaterialCategory.Crafted, Rarity = 2, StackSize = 30, Value = 8, Strength = 4 },
        ["clay_brick"] = new() { Id = "clay_brick", Name = "Clay Brick", Description = "Hardened clay brick.", Category = MaterialCategory.Crafted, Rarity = 2, StackSize = 50, Value = 6, Strength = 6, Warmth = 1, Waterproof = true },
        ["wooden_plank"] = new() { Id = "wooden_plank", Name = "Wooden Plank", Description = "Carved wooden plank.", Category = MaterialCategory.Crafted, Rarity = 2, StackSize = 30, Value = 10, Strength = 5, Warmth = 1, Beauty = 1 },
        ["stone_block"] = new() { Id = "stone_block", Name = "Stone Block", Description = "Carved stone block.", Category = MaterialCategory.Crafted, Rarity = 3, StackSize = 20, Value = 15, Strength = 8, Beauty = 1 },
        ["insulation"] = new() { Id = "insulation", Name = "Insulation", Description = "Keeps warmth in.", Category = MaterialCategory.Crafted, Rarity = 2, StackSize = 30, Value = 8, Strength = 2, Warmth = 5 },
        ["thatch"] = new() { Id = "thatch", Name = "Thatch", Description = "Woven roof material.", Category = MaterialCategory.Crafted, Rarity = 2, StackSize = 30, Value = 7, Strength = 4, Warmth = 2, Beauty = 1, Waterproof = true }
    };
}

/// <summary>
/// Material inventory system.
/// </summary>
public class MaterialInventory
{
    public int MaxSlots { get; set; } = 50;
    public List<MaterialStack> Stacks { get; set; } = new();

    public (int Added, string Message) AddMaterial(string materialId, int amount = 1)
    {
        if (!Materials.AllMaterials.TryGetValue(materialId, out var material))
            return (0, $"Unknown material: {materialId}");

        var remaining = amount;

        // Add to existing stacks first
        foreach (var stack in Stacks.Where(s => s.MaterialId == materialId && s.CanAdd(1)))
        {
            remaining = stack.Add(remaining);
            if (remaining == 0) break;
        }

        // Create new stacks if needed
        while (remaining > 0 && Stacks.Count < MaxSlots)
        {
            var newStack = new MaterialStack { MaterialId = materialId };
            remaining = newStack.Add(remaining);
            Stacks.Add(newStack);
        }

        var added = amount - remaining;
        return added > 0 
            ? (added, $"Added {added}x {material.Name}") 
            : (0, "Inventory full!");
    }

    public int RemoveMaterial(string materialId, int amount)
    {
        var remaining = amount;
        var toRemove = new List<MaterialStack>();

        foreach (var stack in Stacks.Where(s => s.MaterialId == materialId))
        {
            var removed = stack.Remove(remaining);
            remaining -= removed;
            if (stack.Quantity == 0)
                toRemove.Add(stack);
            if (remaining == 0) break;
        }

        foreach (var stack in toRemove)
            Stacks.Remove(stack);

        return amount - remaining;
    }

    public int GetCount(string materialId) => 
        Stacks.Where(s => s.MaterialId == materialId).Sum(s => s.Quantity);

    public bool HasMaterial(string materialId, int amount) => GetCount(materialId) >= amount;

    public MaterialInventorySaveData ToSaveData() => new()
    {
        MaxSlots = MaxSlots,
        Stacks = Stacks.Select(s => new MaterialStackSaveData
        {
            MaterialId = s.MaterialId,
            Quantity = s.Quantity
        }).ToList()
    };

    public static MaterialInventory FromSaveData(MaterialInventorySaveData data)
    {
        var inv = new MaterialInventory { MaxSlots = data.MaxSlots };
        if (data.Stacks != null)
        {
            foreach (var s in data.Stacks)
            {
                inv.Stacks.Add(new MaterialStack
                {
                    MaterialId = s.MaterialId ?? "",
                    Quantity = s.Quantity
                });
            }
        }
        return inv;
    }
}

public class MaterialStackSaveData
{
    public string? MaterialId { get; set; }
    public int Quantity { get; set; }
}

public class MaterialInventorySaveData
{
    public int MaxSlots { get; set; }
    public List<MaterialStackSaveData>? Stacks { get; set; }
}
