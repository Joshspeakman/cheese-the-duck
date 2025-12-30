namespace StupidDuck.World;

/// <summary>
/// Represents an item in the game.
/// </summary>
public record Item(
    string Id,
    string Name,
    string Description,
    ItemCategory Category,
    ItemRarity Rarity = ItemRarity.Common,
    Dictionary<string, float>? Effects = null
);

public enum ItemCategory
{
    Food,
    Toy,
    Cosmetic,
    Furniture,
    Material,
    Special,
    Water,
    Plant,
    Structure,
    Decoration,
    Flooring,
    Lighting
}

public enum ItemRarity
{
    Common,
    Uncommon,
    Rare,
    Epic,
    Legendary
}

/// <summary>
/// Item definitions for the game.
/// </summary>
public static class ItemData
{
    public static readonly Dictionary<string, Item> Items = new()
    {
        ["bread"] = new Item("bread", "Bread", "A tasty slice of bread.", ItemCategory.Food, 
            Effects: new() { ["hunger"] = 20 }),
        ["premium_bread"] = new Item("premium_bread", "Premium Bread", "Artisan sourdough.", ItemCategory.Food, ItemRarity.Uncommon,
            Effects: new() { ["hunger"] = 35, ["fun"] = 5 }),
        ["rubber_duck"] = new Item("rubber_duck", "Rubber Duck", "A squeaky friend.", ItemCategory.Toy, ItemRarity.Common,
            Effects: new() { ["fun"] = 15 }),
        ["tiny_hat"] = new Item("tiny_hat", "Tiny Hat", "A fashionable tiny hat.", ItemCategory.Cosmetic, ItemRarity.Uncommon),
        ["pond_plant"] = new Item("pond_plant", "Pond Plant", "A decorative water plant.", ItemCategory.Furniture, ItemRarity.Common),
        ["golden_feather"] = new Item("golden_feather", "Golden Feather", "A rare golden feather.", ItemCategory.Special, ItemRarity.Legendary)
    };

    public static Item? GetItem(string id) => Items.TryGetValue(id, out var item) ? item : null;

    public static Item GetRandomItem()
    {
        var rng = new Random();
        var items = Items.Values.ToList();
        return items[rng.Next(items.Count)];
    }
}

/// <summary>
/// Player inventory management.
/// </summary>
public class Inventory
{
    private readonly Dictionary<string, int> _items = new();
    public int Capacity { get; set; } = 50;

    public int Count => _items.Values.Sum();

    public bool Add(string itemId, int quantity = 1)
    {
        if (Count + quantity > Capacity)
            return false;

        _items[itemId] = _items.GetValueOrDefault(itemId, 0) + quantity;
        return true;
    }

    public bool Remove(string itemId, int quantity = 1)
    {
        if (!_items.TryGetValue(itemId, out var current) || current < quantity)
            return false;

        _items[itemId] = current - quantity;
        if (_items[itemId] <= 0)
            _items.Remove(itemId);
        return true;
    }

    public int GetQuantity(string itemId) => _items.GetValueOrDefault(itemId, 0);

    public bool Has(string itemId, int quantity = 1) => GetQuantity(itemId) >= quantity;

    public IEnumerable<(string Id, int Quantity)> GetAll() => 
        _items.Select(kv => (kv.Key, kv.Value));

    public List<string> ToList()
    {
        var list = new List<string>();
        foreach (var (id, qty) in _items)
        {
            for (var i = 0; i < qty; i++)
                list.Add(id);
        }
        return list;
    }
}
