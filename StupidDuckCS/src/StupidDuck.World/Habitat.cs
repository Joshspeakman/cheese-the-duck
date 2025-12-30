using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;

namespace StupidDuck.World;

/// <summary>
/// An item that has been placed in the habitat.
/// </summary>
public class PlacedItem
{
    public string ItemId { get; set; } = "";
    public int X { get; set; }
    public int Y { get; set; }
    public double LastInteraction { get; set; }
    
    // Animation state (not saved)
    public double AnimOffsetX { get; set; }
    public double AnimOffsetY { get; set; }
    public double AnimStart { get; set; }
    public bool IsAnimating { get; set; }
    
    /// <summary>
    /// Start an interaction animation.
    /// </summary>
    public void StartAnimation(string animType = "bounce")
    {
        IsAnimating = true;
        AnimStart = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() / 1000.0;
        
        switch (animType)
        {
            case "bounce":
                AnimOffsetY = -1;
                break;
            case "shake":
                AnimOffsetX = 1;
                break;
            case "roll":
                AnimOffsetX = 2;
                break;
        }
    }
    
    /// <summary>
    /// Update animation state. Returns True if still animating.
    /// </summary>
    public bool UpdateAnimation()
    {
        if (!IsAnimating)
            return false;
        
        double now = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() / 1000.0;
        double elapsed = now - AnimStart;
        double duration = 0.5;
        
        if (elapsed >= duration)
        {
            IsAnimating = false;
            AnimOffsetX = 0;
            AnimOffsetY = 0;
            return false;
        }
        
        double progress = elapsed / duration;
        double decay = 1.0 - progress;
        AnimOffsetX *= decay * 0.9;
        AnimOffsetY *= decay * 0.9;
        
        // Add bounce effect
        if (Math.Abs(AnimOffsetY) > 0.1)
        {
            double bounce = Math.Sin(progress * Math.PI * 3) * decay;
            AnimOffsetY = bounce * -1;
        }
        
        return true;
    }
    
    /// <summary>
    /// Get position with animation offset applied.
    /// </summary>
    public (int x, int y) GetDisplayPosition()
    {
        return (X + (int)Math.Round(AnimOffsetX), Y + (int)Math.Round(AnimOffsetY));
    }
    
    public Dictionary<string, object?> ToSaveData()
    {
        return new Dictionary<string, object?>
        {
            ["item_id"] = ItemId,
            ["x"] = X,
            ["y"] = Y,
            ["last_interaction"] = LastInteraction
        };
    }
    
    public static PlacedItem FromSaveData(JsonElement data)
    {
        return new PlacedItem
        {
            ItemId = data.TryGetProperty("item_id", out var idEl) ? idEl.GetString() ?? "" : "",
            X = data.TryGetProperty("x", out var xEl) ? xEl.GetInt32() : 0,
            Y = data.TryGetProperty("y", out var yEl) ? yEl.GetInt32() : 0,
            LastInteraction = data.TryGetProperty("last_interaction", out var liEl) ? liEl.GetDouble() : 0
        };
    }
}

/// <summary>
/// Habitat system - manages owned items and their placement in the duck's home.
/// </summary>
public class Habitat
{
    private static readonly Random _random = new();
    
    public List<string> OwnedItems { get; private set; } = new();
    public List<PlacedItem> PlacedItems { get; private set; } = new();
    public Dictionary<string, string> EquippedCosmetics { get; private set; } = new();
    public int Currency { get; set; } = 100;
    
    // Habitat grid size
    public int Width { get; } = 20;
    public int Height { get; } = 12;
    
    /// <summary>
    /// Add currency.
    /// </summary>
    public void AddCurrency(int amount)
    {
        Currency += amount;
    }
    
    /// <summary>
    /// Check if player can afford an item.
    /// </summary>
    public bool CanAfford(int cost)
    {
        return Currency >= cost;
    }
    
    /// <summary>
    /// Purchase an item if affordable.
    /// </summary>
    public bool PurchaseItem(string itemId, int cost, string category)
    {
        if (!CanAfford(cost))
            return false;
        
        if (OwnedItems.Contains(itemId))
            return false;
        
        Currency -= cost;
        OwnedItems.Add(itemId);
        
        // Auto-equip cosmetics
        if (category == "cosmetic")
        {
            EquipCosmetic(itemId);
        }
        else
        {
            // Auto-place non-cosmetic items in the habitat
            AutoPlaceItem(itemId);
        }
        
        return true;
    }
    
    /// <summary>
    /// Find a random empty spot and place an item.
    /// </summary>
    private void AutoPlaceItem(string itemId)
    {
        int maxAttempts = 50;
        for (int i = 0; i < maxAttempts; i++)
        {
            int x = _random.Next(1, Width - 1);
            int y = _random.Next(1, Height - 1);
            
            // Avoid the center area where duck typically is
            if (x >= 7 && x <= 12 && y >= 4 && y <= 8)
                continue;
            
            if (GetItemAt(x, y) == null)
            {
                PlaceItem(itemId, x, y);
                return;
            }
        }
        
        // If all attempts failed, place at first available spot
        for (int y = 1; y < Height - 1; y++)
        {
            for (int x = 1; x < Width - 1; x++)
            {
                if (GetItemAt(x, y) == null)
                {
                    PlaceItem(itemId, x, y);
                    return;
                }
            }
        }
    }
    
    /// <summary>
    /// Check if player owns an item.
    /// </summary>
    public bool OwnsItem(string itemId)
    {
        return OwnedItems.Contains(itemId);
    }
    
    /// <summary>
    /// Place an owned item in the habitat.
    /// </summary>
    public bool PlaceItem(string itemId, int x, int y)
    {
        if (!OwnsItem(itemId))
            return false;
        
        if (x < 0 || x >= Width || y < 0 || y >= Height)
            return false;
        
        if (GetItemAt(x, y) != null)
            return false;
        
        PlacedItems.Add(new PlacedItem { ItemId = itemId, X = x, Y = y });
        return true;
    }
    
    /// <summary>
    /// Remove an item from a position.
    /// </summary>
    public bool RemoveItemAt(int x, int y)
    {
        var item = GetItemAt(x, y);
        if (item != null)
        {
            PlacedItems.Remove(item);
            return true;
        }
        return false;
    }
    
    /// <summary>
    /// Get the item at a position.
    /// </summary>
    public PlacedItem? GetItemAt(int x, int y)
    {
        return PlacedItems.FirstOrDefault(i => i.X == x && i.Y == y);
    }
    
    /// <summary>
    /// Update all item animations.
    /// </summary>
    public void UpdateAnimations()
    {
        foreach (var item in PlacedItems)
        {
            item.UpdateAnimation();
        }
    }
    
    /// <summary>
    /// Start an animation on a placed item.
    /// </summary>
    public void AnimateItem(PlacedItem placedItem, string animType = "bounce")
    {
        placedItem.StartAnimation(animType);
    }
    
    /// <summary>
    /// Get items near a position.
    /// </summary>
    public List<PlacedItem> GetItemsNear(int x, int y, int radius = 3)
    {
        var nearby = new List<PlacedItem>();
        foreach (var item in PlacedItems)
        {
            int dx = Math.Abs(item.X - x);
            int dy = Math.Abs(item.Y - y);
            if (dx <= radius && dy <= radius)
                nearby.Add(item);
        }
        return nearby;
    }
    
    /// <summary>
    /// Get all placed items of a category.
    /// </summary>
    public List<PlacedItem> GetPlacedItemsByCategory(string category)
    {
        // Note: Requires ShopSystem integration to look up item categories
        // For now, returns all items
        return PlacedItems.ToList();
    }
    
    /// <summary>
    /// Equip a cosmetic item.
    /// </summary>
    public void EquipCosmetic(string itemId)
    {
        string slot = GetCosmeticSlot(itemId);
        EquippedCosmetics[slot] = itemId;
    }
    
    /// <summary>
    /// Remove a cosmetic from a slot.
    /// </summary>
    public void UnequipCosmetic(string slot)
    {
        EquippedCosmetics.Remove(slot);
    }
    
    /// <summary>
    /// Determine which slot a cosmetic goes in.
    /// </summary>
    private string GetCosmeticSlot(string itemId)
    {
        // Hats and head items
        string[] headItems = { "hat_", "cap_", "beanie", "crown", "helmet", "wizard", "pirate", "viking",
            "party_hat", "flower_crown", "tiara", "graduation", "nurse", "pilot",
            "detective", "cat_ears", "bunny_ears", "antenna", "propeller", "jester" };
        
        foreach (var h in headItems)
        {
            if (itemId.Contains(h))
                return "head";
        }
        
        // Glasses and face items
        if (itemId.Contains("glasses_") || itemId.Contains("sunglasses") || itemId.Contains("monocle"))
            return "eyes";
        
        // Neck accessories
        if (itemId.Contains("bowtie") || itemId.Contains("bow_tie") || itemId.Contains("scarf_") || itemId.Contains("bandana"))
            return "neck";
        
        // Back items
        if (itemId.Contains("cape") || itemId.Contains("wings_") || itemId.Contains("backpack"))
            return "back";
        
        // Above head (floating)
        if (itemId.Contains("halo") || itemId.Contains("devil_horns") || itemId.Contains("headphones"))
            return "above";
        
        return "head"; // Default to head slot
    }
    
    /// <summary>
    /// Get items near a position (for duck interaction).
    /// </summary>
    public List<PlacedItem> GetNearbyItems(int x, int y, int radius = 2)
    {
        return GetItemsNear(x, y, radius);
    }
    
    /// <summary>
    /// Mark that the duck interacted with an item.
    /// </summary>
    public void MarkInteraction(PlacedItem placedItem, double timestamp)
    {
        placedItem.LastInteraction = timestamp;
    }
    
    /// <summary>
    /// Get habitat statistics.
    /// </summary>
    public Dictionary<string, int> GetStats()
    {
        return new Dictionary<string, int>
        {
            ["owned_items"] = OwnedItems.Count,
            ["placed_items"] = PlacedItems.Count,
            ["currency"] = Currency,
            ["cosmetics_equipped"] = EquippedCosmetics.Count
        };
    }
    
    /// <summary>
    /// Render habitat display.
    /// </summary>
    public List<string> RenderHabitat()
    {
        var lines = new List<string>();
        
        // Create grid
        var grid = new char[Height, Width];
        for (int y = 0; y < Height; y++)
        {
            for (int x = 0; x < Width; x++)
            {
                if (y == 0 || y == Height - 1)
                    grid[y, x] = '═';
                else if (x == 0 || x == Width - 1)
                    grid[y, x] = '║';
                else
                    grid[y, x] = ' ';
            }
        }
        
        // Place items
        foreach (var item in PlacedItems)
        {
            var (dx, dy) = item.GetDisplayPosition();
            if (dx >= 0 && dx < Width && dy >= 0 && dy < Height)
            {
                grid[dy, dx] = '▪';
            }
        }
        
        // Corners
        grid[0, 0] = '╔';
        grid[0, Width - 1] = '╗';
        grid[Height - 1, 0] = '╚';
        grid[Height - 1, Width - 1] = '╝';
        
        // Convert to strings
        for (int y = 0; y < Height; y++)
        {
            var row = new char[Width];
            for (int x = 0; x < Width; x++)
                row[x] = grid[y, x];
            lines.Add(new string(row));
        }
        
        return lines;
    }
    
    /// <summary>
    /// Convert to save data.
    /// </summary>
    public Dictionary<string, object?> ToSaveData()
    {
        return new Dictionary<string, object?>
        {
            ["owned_items"] = OwnedItems,
            ["placed_items"] = PlacedItems.Select(i => i.ToSaveData()).ToList(),
            ["equipped_cosmetics"] = EquippedCosmetics,
            ["currency"] = Currency
        };
    }
    
    /// <summary>
    /// Load from save data.
    /// </summary>
    public static Habitat FromSaveData(Dictionary<string, JsonElement> data)
    {
        var habitat = new Habitat();
        
        if (data.TryGetValue("owned_items", out var ownedEl) && ownedEl.ValueKind == JsonValueKind.Array)
            habitat.OwnedItems = ownedEl.EnumerateArray().Select(e => e.GetString() ?? "").ToList();
        
        if (data.TryGetValue("placed_items", out var placedEl) && placedEl.ValueKind == JsonValueKind.Array)
            habitat.PlacedItems = placedEl.EnumerateArray().Select(PlacedItem.FromSaveData).ToList();
        
        if (data.TryGetValue("equipped_cosmetics", out var equippedEl) && equippedEl.ValueKind == JsonValueKind.Object)
        {
            foreach (var prop in equippedEl.EnumerateObject())
            {
                habitat.EquippedCosmetics[prop.Name] = prop.Value.GetString() ?? "";
            }
        }
        
        if (data.TryGetValue("currency", out var currEl))
            habitat.Currency = currEl.GetInt32();
        
        return habitat;
    }
    
    /// <summary>
    /// Load from save data dictionary.
    /// </summary>
    public void LoadFromData(Dictionary<string, JsonElement> data)
    {
        var loaded = FromSaveData(data);
        OwnedItems = loaded.OwnedItems;
        PlacedItems = loaded.PlacedItems;
        EquippedCosmetics = loaded.EquippedCosmetics;
        Currency = loaded.Currency;
    }
}
