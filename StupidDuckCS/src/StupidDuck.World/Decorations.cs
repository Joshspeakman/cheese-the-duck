namespace StupidDuck.World;

/// <summary>
/// Decoration categories.
/// </summary>
public enum DecorationType
{
    Furniture,
    Plant,
    Toy,
    Lighting,
    Seasonal,
    Special
}

/// <summary>
/// Decoration rarity.
/// </summary>
public enum DecorationRarity
{
    Common,
    Uncommon,
    Rare,
    Epic,
    Legendary
}

/// <summary>
/// A decoration item definition.
/// </summary>
public record DecorationDef(
    string Id,
    string Name,
    string Ascii,
    DecorationType Type,
    DecorationRarity Rarity,
    int Price,
    float ComfortBonus = 0f,
    string Description = ""
);

/// <summary>
/// A placed decoration in the habitat.
/// </summary>
public class PlacedDecoration
{
    public string DecorationId { get; init; } = "";
    public int X { get; set; }
    public int Y { get; set; }
    public DateTime PlacedAt { get; init; } = DateTime.Now;
}

/// <summary>
/// Manages decorations and items in the habitat.
/// </summary>
public static class Decorations
{
    public static readonly Dictionary<string, DecorationDef> All = new()
    {
        // Plants
        ["lily_pad"] = new("lily_pad", "Lily Pad", "@", DecorationType.Plant, DecorationRarity.Common, 10, 0.5f, "A floating lily pad"),
        ["cattails"] = new("cattails", "Cattails", "|i", DecorationType.Plant, DecorationRarity.Common, 15, 0.3f, "Tall pond reeds"),
        ["flower"] = new("flower", "Flower", "*", DecorationType.Plant, DecorationRarity.Common, 20, 1f, "A pretty flower"),
        ["bonsai"] = new("bonsai", "Bonsai Tree", "🌳", DecorationType.Plant, DecorationRarity.Rare, 150, 3f, "A tiny tree"),
        
        // Toys
        ["rubber_duck"] = new("rubber_duck", "Rubber Duck", "♦", DecorationType.Toy, DecorationRarity.Common, 25, 1f, "A classic friend"),
        ["ball"] = new("ball", "Ball", "●", DecorationType.Toy, DecorationRarity.Common, 15, 0.8f, "Bouncy!"),
        ["plushie"] = new("plushie", "Plushie", "♥", DecorationType.Toy, DecorationRarity.Uncommon, 50, 2f, "Soft and cuddly"),
        
        // Furniture
        ["nest"] = new("nest", "Cozy Nest", "◎", DecorationType.Furniture, DecorationRarity.Common, 30, 2f, "A comfy nest"),
        ["bench"] = new("bench", "Tiny Bench", "═", DecorationType.Furniture, DecorationRarity.Uncommon, 45, 1.5f, "A resting spot"),
        ["umbrella"] = new("umbrella", "Beach Umbrella", "☂", DecorationType.Furniture, DecorationRarity.Uncommon, 60, 1f, "Shade from the sun"),
        
        // Lighting
        ["lantern"] = new("lantern", "Paper Lantern", "◯", DecorationType.Lighting, DecorationRarity.Uncommon, 40, 1.5f, "Soft glow"),
        ["fairy_lights"] = new("fairy_lights", "Fairy Lights", ".:.", DecorationType.Lighting, DecorationRarity.Rare, 100, 3f, "Magical sparkles"),
        
        // Seasonal
        ["pumpkin"] = new("pumpkin", "Pumpkin", "☻", DecorationType.Seasonal, DecorationRarity.Uncommon, 35, 1f, "Spooky season"),
        ["snowman"] = new("snowman", "Snowman", "⛄", DecorationType.Seasonal, DecorationRarity.Uncommon, 35, 1f, "Frosty friend"),
        ["wreath"] = new("wreath", "Holiday Wreath", "❀", DecorationType.Seasonal, DecorationRarity.Rare, 80, 2f, "Festive decoration"),
        
        // Special
        ["fountain"] = new("fountain", "Fountain", "⛲", DecorationType.Special, DecorationRarity.Epic, 500, 5f, "Splashy centerpiece"),
        ["golden_nest"] = new("golden_nest", "Golden Nest", "✦", DecorationType.Special, DecorationRarity.Legendary, 2000, 10f, "Luxurious living"),
        ["rainbow_crystal"] = new("rainbow_crystal", "Rainbow Crystal", "◆", DecorationType.Special, DecorationRarity.Legendary, 1500, 8f, "Prismatic beauty")
    };

    public static DecorationDef? Get(string id) =>
        All.TryGetValue(id, out var def) ? def : null;

    public static IEnumerable<DecorationDef> ByType(DecorationType type) =>
        All.Values.Where(d => d.Type == type);

    public static IEnumerable<DecorationDef> ByRarity(DecorationRarity rarity) =>
        All.Values.Where(d => d.Rarity == rarity);
}

/// <summary>
/// Manages placed decorations in the habitat.
/// </summary>
public class HabitatDecorations
{
    private readonly List<PlacedDecoration> _placed = new();
    private readonly Dictionary<string, int> _inventory = new();
    
    public IReadOnlyList<PlacedDecoration> PlacedItems => _placed;
    public IReadOnlyDictionary<string, int> Inventory => _inventory;

    /// <summary>
    /// Add a decoration to inventory.
    /// </summary>
    public void AddToInventory(string decorationId, int count = 1)
    {
        _inventory.TryGetValue(decorationId, out var current);
        _inventory[decorationId] = current + count;
    }

    /// <summary>
    /// Place a decoration from inventory.
    /// </summary>
    public bool Place(string decorationId, int x, int y)
    {
        if (!_inventory.TryGetValue(decorationId, out var count) || count <= 0)
            return false;

        _placed.Add(new PlacedDecoration
        {
            DecorationId = decorationId,
            X = x,
            Y = y
        });

        _inventory[decorationId] = count - 1;
        if (_inventory[decorationId] <= 0)
            _inventory.Remove(decorationId);

        return true;
    }

    /// <summary>
    /// Get total comfort bonus from all decorations.
    /// </summary>
    public float GetTotalComfort()
    {
        return _placed.Sum(p => 
            Decorations.Get(p.DecorationId)?.ComfortBonus ?? 0f);
    }

    /// <summary>
    /// Get decoration characters at positions for rendering.
    /// </summary>
    public Dictionary<(int x, int y), (string ascii, string color)> GetRenderPositions()
    {
        var result = new Dictionary<(int, int), (string, string)>();
        
        foreach (var placed in _placed)
        {
            var def = Decorations.Get(placed.DecorationId);
            if (def == null) continue;

            var color = def.Rarity switch
            {
                DecorationRarity.Legendary => "gold",
                DecorationRarity.Epic => "magenta",
                DecorationRarity.Rare => "blue",
                DecorationRarity.Uncommon => "green",
                _ => "white"
            };

            result[(placed.X, placed.Y)] = (def.Ascii, color);
        }

        return result;
    }

    public Dictionary<string, object> ToSaveData() => new()
    {
        ["placed"] = _placed.Select(p => new Dictionary<string, object>
        {
            ["id"] = p.DecorationId,
            ["x"] = p.X,
            ["y"] = p.Y,
            ["placed_at"] = p.PlacedAt.ToString("O")
        }).ToList(),
        ["inventory"] = _inventory.ToDictionary(kvp => kvp.Key, kvp => (object)kvp.Value)
    };

    public void LoadSaveData(Dictionary<string, object>? data)
    {
        // TODO: Implement loading
    }
}
