namespace StupidDuck.World;

public enum DecorationSlot { Nest, FloorLeft, FloorRight, WallLeft, WallRight, Ceiling, Water }

public class Decoration
{
    public string Id { get; set; } = "";
    public string Name { get; set; } = "";
    public string Description { get; set; } = "";
    public DecorationSlot Slot { get; set; }
    public List<string> AsciiArt { get; set; } = new();
    public int MoodBonus { get; set; }
    public string Rarity { get; set; } = "common";
    public bool Unlocked { get; set; }
    public string UnlockCondition { get; set; } = "";
}

public class HomeTheme
{
    public string Name { get; set; } = "";
    public string Description { get; set; } = "";
    public char BorderChar { get; set; } = '~';
    public char FloorChar { get; set; } = '.';
    public bool Unlocked { get; set; }
    public string UnlockCondition { get; set; } = "";
}

public class DuckHome
{
    public string Theme { get; set; } = "default";
    public Dictionary<string, string> Decorations { get; private set; } = new() { ["Nest"] = "basic_nest" };
    public List<string> UnlockedDecorations { get; private set; } = new() { "basic_nest", "pebble_collection", "duck_poster" };
    public List<string> UnlockedThemes { get; private set; } = new() { "default" };
    public int TotalMoodBonus { get; private set; }

    public static Dictionary<string, Decoration> DecorationData { get; } = new()
    {
        ["basic_nest"] = new Decoration
        {
            Id = "basic_nest", Name = "Basic Nest", Description = "A simple but cozy nest",
            Slot = DecorationSlot.Nest, AsciiArt = new() { "\\___/" }, MoodBonus = 0, Unlocked = true
        },
        ["cozy_nest"] = new Decoration
        {
            Id = "cozy_nest", Name = "Cozy Nest", Description = "Extra soft with feather lining",
            Slot = DecorationSlot.Nest, AsciiArt = new() { "\\~*~/" }, MoodBonus = 5, Rarity = "uncommon",
            UnlockCondition = "Reach level 5"
        },
        ["luxury_nest"] = new Decoration
        {
            Id = "luxury_nest", Name = "Luxury Nest", Description = "Fit for duck royalty",
            Slot = DecorationSlot.Nest, AsciiArt = new() { "\\***/" }, MoodBonus = 15, Rarity = "rare",
            UnlockCondition = "Reach level 15"
        },
        ["golden_nest"] = new Decoration
        {
            Id = "golden_nest", Name = "Golden Nest", Description = "Made of dreams and sparkles",
            Slot = DecorationSlot.Nest, AsciiArt = new() { "\\@#@/" }, MoodBonus = 30, Rarity = "legendary",
            UnlockCondition = "Reach level 30"
        },
        ["small_pond"] = new Decoration
        {
            Id = "small_pond", Name = "Mini Pond", Description = "A tiny splash zone",
            Slot = DecorationSlot.Water, AsciiArt = new() { "~~~~~", " ~~~ " }, MoodBonus = 10, Rarity = "uncommon",
            UnlockCondition = "Play 50 times"
        },
        ["flower_patch"] = new Decoration
        {
            Id = "flower_patch", Name = "Flower Patch", Description = "Pretty flowers!",
            Slot = DecorationSlot.FloorLeft, AsciiArt = new() { "*,*,*" }, MoodBonus = 5,
            UnlockCondition = "Feed 20 times"
        },
        ["pebble_collection"] = new Decoration
        {
            Id = "pebble_collection", Name = "Pebble Collection", Description = "Shiny rocks arranged nicely",
            Slot = DecorationSlot.FloorRight, AsciiArt = new() { "o.o.o" }, MoodBonus = 3, Unlocked = true
        },
        ["food_bowl"] = new Decoration
        {
            Id = "food_bowl", Name = "Fancy Food Bowl", Description = "Always has snacks nearby",
            Slot = DecorationSlot.FloorLeft, AsciiArt = new() { "(===)" }, MoodBonus = 8, Rarity = "uncommon",
            UnlockCondition = "Feed 100 times"
        },
        ["toy_box"] = new Decoration
        {
            Id = "toy_box", Name = "Toy Box", Description = "Full of fun things!",
            Slot = DecorationSlot.FloorRight, AsciiArt = new() { "[TOY]" }, MoodBonus = 10, Rarity = "uncommon",
            UnlockCondition = "Collect 5 toys"
        },
        ["family_photo"] = new Decoration
        {
            Id = "family_photo", Name = "Family Photo", Description = "A photo of you and Cheese",
            Slot = DecorationSlot.WallLeft, AsciiArt = new() { "[^^]" }, MoodBonus = 15, Rarity = "rare",
            UnlockCondition = "30 day streak"
        },
        ["duck_poster"] = new Decoration
        {
            Id = "duck_poster", Name = "Duck Poster", Description = "'Believe in yourself' - Duck",
            Slot = DecorationSlot.WallRight, AsciiArt = new() { "[DK]" }, MoodBonus = 5, Unlocked = true
        },
        ["achievement_wall"] = new Decoration
        {
            Id = "achievement_wall", Name = "Achievement Wall", Description = "Shows off your badges",
            Slot = DecorationSlot.WallLeft, AsciiArt = new() { "[!!]" }, MoodBonus = 10, Rarity = "uncommon",
            UnlockCondition = "Earn 10 achievements"
        },
        ["window"] = new Decoration
        {
            Id = "window", Name = "Sunny Window", Description = "Lets in natural light",
            Slot = DecorationSlot.WallRight, AsciiArt = new() { "[##]" }, MoodBonus = 8, Rarity = "uncommon",
            UnlockCondition = "Reach level 10"
        },
        ["fairy_lights"] = new Decoration
        {
            Id = "fairy_lights", Name = "Fairy Lights", Description = "Sparkly and magical",
            Slot = DecorationSlot.Ceiling, AsciiArt = new() { "*-*-*-*" }, MoodBonus = 12, Rarity = "rare",
            UnlockCondition = "Find Golden Feather"
        },
        ["mobile"] = new Decoration
        {
            Id = "mobile", Name = "Duck Mobile", Description = "Little ducks spinning around",
            Slot = DecorationSlot.Ceiling, AsciiArt = new() { "o-O-o" }, MoodBonus = 7, Rarity = "uncommon",
            UnlockCondition = "Reach level 7"
        },
        ["chandelier"] = new Decoration
        {
            Id = "chandelier", Name = "Mini Chandelier", Description = "Fancy lighting!",
            Slot = DecorationSlot.Ceiling, AsciiArt = new() { "\\|/" }, MoodBonus = 20, Rarity = "legendary",
            UnlockCondition = "Reach level 40"
        }
    };

    public static Dictionary<string, HomeTheme> ThemeData { get; } = new()
    {
        ["default"] = new HomeTheme { Name = "Classic Pond", Description = "A simple, cozy pond home", BorderChar = '~', FloorChar = '.', Unlocked = true },
        ["forest"] = new HomeTheme { Name = "Forest Hideaway", Description = "Surrounded by trees", BorderChar = '|', FloorChar = ',', UnlockCondition = "Reach level 10" },
        ["beach"] = new HomeTheme { Name = "Beach Paradise", Description = "Sandy and sunny", BorderChar = '~', FloorChar = ':', UnlockCondition = "7 day streak" },
        ["space"] = new HomeTheme { Name = "Space Station", Description = "Duck in spaaaaace!", BorderChar = '*', FloorChar = ' ', UnlockCondition = "Reach level 25" },
        ["castle"] = new HomeTheme { Name = "Duck Castle", Description = "Royal accommodations", BorderChar = '#', FloorChar = '_', UnlockCondition = "Reach level 50" }
    };

    public DuckHome() => CalculateMoodBonus();

    private void CalculateMoodBonus()
    {
        TotalMoodBonus = 0;
        foreach (var decId in Decorations.Values)
            if (DecorationData.TryGetValue(decId, out var dec))
                TotalMoodBonus += dec.MoodBonus;
    }

    public bool PlaceDecoration(string decorationId)
    {
        if (!UnlockedDecorations.Contains(decorationId)) return false;
        if (!DecorationData.TryGetValue(decorationId, out var dec)) return false;

        Decorations[dec.Slot.ToString()] = decorationId;
        CalculateMoodBonus();
        return true;
    }

    public bool RemoveDecoration(string slot)
    {
        if (!Decorations.ContainsKey(slot)) return false;
        Decorations.Remove(slot);
        CalculateMoodBonus();
        return true;
    }

    public bool UnlockDecoration(string decorationId)
    {
        if (UnlockedDecorations.Contains(decorationId)) return false;
        if (!DecorationData.ContainsKey(decorationId)) return false;
        UnlockedDecorations.Add(decorationId);
        return true;
    }

    public bool SetTheme(string themeId)
    {
        if (!UnlockedThemes.Contains(themeId)) return false;
        if (!ThemeData.ContainsKey(themeId)) return false;
        Theme = themeId;
        return true;
    }

    public bool UnlockTheme(string themeId)
    {
        if (UnlockedThemes.Contains(themeId)) return false;
        if (!ThemeData.ContainsKey(themeId)) return false;
        UnlockedThemes.Add(themeId);
        return true;
    }

    public Decoration? GetDecorationAt(string slot) =>
        Decorations.TryGetValue(slot, out var decId) && DecorationData.TryGetValue(decId, out var dec) ? dec : null;

    public List<Decoration> GetAvailableDecorations(DecorationSlot slot) =>
        UnlockedDecorations
            .Where(id => DecorationData.TryGetValue(id, out var dec) && dec.Slot == slot)
            .Select(id => DecorationData[id])
            .ToList();

    public List<string> RenderHomePreview(int width = 30)
    {
        var theme = ThemeData.TryGetValue(Theme, out var t) ? t : ThemeData["default"];
        var border = theme.BorderChar;
        var floor = theme.FloorChar;
        var lines = new List<string>();

        // Ceiling
        var ceiling = GetDecorationAt(DecorationSlot.Ceiling.ToString());
        var ceilingArt = ceiling?.AsciiArt.FirstOrDefault() ?? "";
        lines.Add($"{border}{ceilingArt.PadLeft((width - 2 + ceilingArt.Length) / 2).PadRight(width - 2)}{border}");

        // Walls
        var wallL = GetDecorationAt(DecorationSlot.WallLeft.ToString());
        var wallR = GetDecorationAt(DecorationSlot.WallRight.ToString());
        var leftArt = wallL?.AsciiArt.FirstOrDefault() ?? "    ";
        var rightArt = wallR?.AsciiArt.FirstOrDefault() ?? "    ";
        var wallPad = new string(' ', width - 2 - leftArt.Length - rightArt.Length);
        lines.Add($"{border}{leftArt}{wallPad}{rightArt}{border}");

        // Middle
        lines.Add($"{border}{new string(' ', width - 2)}{border}");
        lines.Add($"{border}{new string(' ', width - 2)}{border}");

        // Nest
        var nest = GetDecorationAt(DecorationSlot.Nest.ToString());
        var nestArt = nest?.AsciiArt.FirstOrDefault() ?? "\\___/";
        lines.Add($"{border}{nestArt.PadLeft((width - 2 + nestArt.Length) / 2).PadRight(width - 2)}{border}");

        // Floor
        var floorL = GetDecorationAt(DecorationSlot.FloorLeft.ToString());
        var floorR = GetDecorationAt(DecorationSlot.FloorRight.ToString());
        var flLeftArt = floorL?.AsciiArt.FirstOrDefault() ?? new string(floor, 5);
        var flRightArt = floorR?.AsciiArt.FirstOrDefault() ?? new string(floor, 5);
        var floorFill = new string(floor, width - 2 - flLeftArt.Length - flRightArt.Length);
        lines.Add($"{border}{flLeftArt}{floorFill}{flRightArt}{border}");

        // Water
        var water = GetDecorationAt(DecorationSlot.Water.ToString());
        if (water != null)
        {
            var waterArt = water.AsciiArt.FirstOrDefault() ?? "~~~~~";
            lines.Add($"{border}{waterArt.PadLeft((width - 2 + waterArt.Length) / 2).PadRight(width - 2)}{border}");
        }

        lines.Add(new string(border, width));
        return lines;
    }

    public List<string> CheckUnlocks(int level, Dictionary<string, int> stats, int streak)
    {
        var newUnlocks = new List<string>();

        foreach (var (decId, dec) in DecorationData)
        {
            if (UnlockedDecorations.Contains(decId)) continue;
            if (string.IsNullOrEmpty(dec.UnlockCondition)) continue;

            var cond = dec.UnlockCondition.ToLower();
            if (cond.Contains("level") && int.TryParse(System.Text.RegularExpressions.Regex.Match(cond, @"\d+").Value, out var lvl) && level >= lvl)
                newUnlocks.Add(decId);
            else if (cond.Contains("streak") && int.TryParse(System.Text.RegularExpressions.Regex.Match(cond, @"\d+").Value, out var strk) && streak >= strk)
                newUnlocks.Add(decId);
            else if (cond.Contains("feed") && int.TryParse(System.Text.RegularExpressions.Regex.Match(cond, @"\d+").Value, out var feeds) && stats.GetValueOrDefault("total_feeds") >= feeds)
                newUnlocks.Add(decId);
            else if (cond.Contains("play") && int.TryParse(System.Text.RegularExpressions.Regex.Match(cond, @"\d+").Value, out var plays) && stats.GetValueOrDefault("total_plays") >= plays)
                newUnlocks.Add(decId);
        }

        foreach (var (themeId, theme) in ThemeData)
        {
            if (UnlockedThemes.Contains(themeId)) continue;
            if (string.IsNullOrEmpty(theme.UnlockCondition)) continue;

            var cond = theme.UnlockCondition.ToLower();
            if (cond.Contains("level") && int.TryParse(System.Text.RegularExpressions.Regex.Match(cond, @"\d+").Value, out var lvl) && level >= lvl)
                newUnlocks.Add($"theme:{themeId}");
            else if (cond.Contains("streak") && int.TryParse(System.Text.RegularExpressions.Regex.Match(cond, @"\d+").Value, out var strk) && streak >= strk)
                newUnlocks.Add($"theme:{themeId}");
        }

        return newUnlocks;
    }

    public Dictionary<string, object> ToSaveData() => new()
    {
        ["theme"] = Theme,
        ["decorations"] = Decorations,
        ["unlocked_decorations"] = UnlockedDecorations,
        ["unlocked_themes"] = UnlockedThemes
    };

    public static DuckHome FromSaveData(Dictionary<string, object> data)
    {
        var home = new DuckHome();
        if (data.TryGetValue("theme", out var t)) home.Theme = t.ToString() ?? "default";
        if (data.TryGetValue("unlocked_themes", out var ut) && ut is IEnumerable<object> themes)
            home.UnlockedThemes = themes.Select(x => x.ToString()!).ToList();
        if (data.TryGetValue("unlocked_decorations", out var ud) && ud is IEnumerable<object> decs)
            home.UnlockedDecorations = decs.Select(x => x.ToString()!).ToList();
        home.CalculateMoodBonus();
        return home;
    }
}
