namespace StupidDuck.World;

// Extended atmosphere types (separate from AtmosphereWeather.cs and Friends.cs types)

public enum AtmosphereWeatherType { Sunny, Cloudy, Rainy, Stormy, Foggy, Snowy, Windy, Rainbow }
public enum AtmosphereSeason { Spring, Summer, Fall, Winter }
public enum AtmosphereFriendshipLevel { Stranger, Acquaintance, Friend, GoodFriend, BestFriend }

public class AtmosphereWeather
{
    public AtmosphereWeatherType Type { get; set; }
    public float Intensity { get; set; }
    public float DurationHours { get; set; }
    public DateTime StartTime { get; set; }
    public int MoodModifier { get; set; }
    public float XpMultiplier { get; set; } = 1.0f;
    public string SpecialMessage { get; set; } = "";

    public bool IsActive() => (DateTime.Now - StartTime).TotalHours < DurationHours;
}

public class AtmosphereWeatherData
{
    public string Name { get; set; } = "";
    public string Message { get; set; } = "";
    public int MoodModifier { get; set; }
    public float XpMultiplier { get; set; } = 1.0f;
    public List<string> Ascii { get; set; } = new();
    public float SpringProb { get; set; }
    public float SummerProb { get; set; }
    public float FallProb { get; set; }
    public float WinterProb { get; set; }
    public bool TriggersRainbow { get; set; }
    public float RareDropsBonus { get; set; }
    public bool Special { get; set; }
}

public class SeasonalContent
{
    public List<string> ItemsAvailable { get; set; } = new();
    public List<string> Events { get; set; } = new();
    public List<string> Decorations { get; set; } = new();
    public string MoodTheme { get; set; } = "";
    public float XpBonus { get; set; } = 1.0f;
    public List<string> ColorPalette { get; set; } = new();
    public List<string> SpecialActivities { get; set; } = new();
    public List<string> AmbientEffects { get; set; } = new();
    public List<string> GreetingMessages { get; set; } = new();
}

public class SeasonalEvent
{
    public string Id { get; set; } = "";
    public string Name { get; set; } = "";
    public string Description { get; set; } = "";
    public AtmosphereSeason AtmosphereSeason { get; set; }
    public int StartDay { get; set; }
    public int DurationDays { get; set; }
    public float XpBonus { get; set; }
    public List<string> SpecialDrops { get; set; } = new();
    public List<string> Activities { get; set; } = new();
    public List<string> Messages { get; set; } = new();
}

public class DayFortune
{
    public string FortuneType { get; set; } = "normal";
    public float XpMultiplier { get; set; } = 1.0f;
    public float DropRateModifier { get; set; } = 1.0f;
    public string SpecialMessage { get; set; } = "";
    public string Horoscope { get; set; } = "";
}

public class AtmosphereVisitorFriendship
{
    public string VisitorId { get; set; } = "";
    public int VisitCount { get; set; }
    public int FriendshipPoints { get; set; }
    public DateTime? LastVisit { get; set; }
    public List<string> GiftsReceived { get; set; } = new();
    public List<string> SpecialMoments { get; set; } = new();

    public AtmosphereFriendshipLevel Level
    {
        get
        {
            if (FriendshipPoints >= 25) return AtmosphereFriendshipLevel.BestFriend;
            if (FriendshipPoints >= 15) return AtmosphereFriendshipLevel.GoodFriend;
            if (FriendshipPoints >= 8) return AtmosphereFriendshipLevel.Friend;
            if (FriendshipPoints >= 3) return AtmosphereFriendshipLevel.Acquaintance;
            return AtmosphereFriendshipLevel.Stranger;
        }
    }

    public void AddVisit()
    {
        VisitCount++;
        FriendshipPoints += 2;
        LastVisit = DateTime.Now;
    }

    public void AddInteraction(int points = 1) => FriendshipPoints += points;
}

public class AtmosphereVisitor
{
    public string Id { get; set; } = "";
    public string Name { get; set; } = "";
    public string Description { get; set; } = "";
    public List<string> AsciiArt { get; set; } = new();
    public string Greeting { get; set; } = "";
    public string Farewell { get; set; } = "";
    public float GiftChance { get; set; }
    public List<string> PossibleGifts { get; set; } = new();
    public float AppearanceChance { get; set; }
    public float StayDurationHours { get; set; }
    public string SpecialInteraction { get; set; } = "";
    public int MoodBoost { get; set; }
    public bool IsRecurring { get; set; } = true;
    public string Personality { get; set; } = "friendly";
    public string? FavoriteWeather { get; set; }
    public string? FavoriteSeason { get; set; }
    public List<string> ReturnGreetings { get; set; } = new();
    public List<string> FriendGreetings { get; set; } = new();
    public List<string> BestFriendGreetings { get; set; } = new();
    public List<string> SpecialGifts { get; set; } = new();
    public List<string> Conversations { get; set; } = new();
    public List<string> Secrets { get; set; } = new();
}

public class ExtendedAtmosphereSystem
{
    private static readonly Random _random = new();
    
    public AtmosphereWeather? CurrentWeather { get; private set; }
    public AtmosphereSeason CurrentSeason { get; private set; }
    public DayFortune? DayFortune { get; private set; }
    public (AtmosphereVisitor AtmosphereVisitor, DateTime Arrival)? CurrentVisitor { get; private set; }
    public DateTime? LastFortuneDate { get; private set; }
    public List<string> VisitorHistory { get; private set; } = new();
    public List<string> WeatherHistory { get; private set; } = new();
    public Dictionary<string, AtmosphereVisitorFriendship> VisitorFriendships { get; private set; } = new();

    public static Dictionary<AtmosphereWeatherType, AtmosphereWeatherData> WeatherDataMap { get; } = new()
    {
        [AtmosphereWeatherType.Sunny] = new AtmosphereWeatherData
        {
            Name = "Sunny", Message = "The sun is shining! Perfect day!",
            MoodModifier = 5, XpMultiplier = 1.1f,
            Ascii = new() { "  \\  |  /", "   \\ | /", " -- ☉ --", "   / | \\", "  /  |  \\" },
            SpringProb = 0.35f, SummerProb = 0.50f, FallProb = 0.25f, WinterProb = 0.15f
        },
        [AtmosphereWeatherType.Cloudy] = new AtmosphereWeatherData
        {
            Name = "Cloudy", Message = "Clouds drift overhead...",
            MoodModifier = 0, XpMultiplier = 1.0f,
            Ascii = new() { "   .-~~~-.", " .-~       ~-.", "{    CLOUD   }", " `-._______.-'" },
            SpringProb = 0.25f, SummerProb = 0.15f, FallProb = 0.30f, WinterProb = 0.30f
        },
        [AtmosphereWeatherType.Rainy] = new AtmosphereWeatherData
        {
            Name = "Rainy", Message = "*pitter patter* Cheese loves splashing in puddles!",
            MoodModifier = -2, XpMultiplier = 1.15f, TriggersRainbow = true,
            Ascii = new() { " , , , , ,", ", , , , , ,", " , , , , ,", "  ~ puddles ~" },
            SpringProb = 0.25f, SummerProb = 0.15f, FallProb = 0.25f, WinterProb = 0.10f
        },
        [AtmosphereWeatherType.Stormy] = new AtmosphereWeatherData
        {
            Name = "Stormy", Message = "*BOOM* Thunder! Cheese hides under a wing...",
            MoodModifier = -5, XpMultiplier = 1.25f,
            Ascii = new() { " \\\\\\|///", "  STORM!!", " ///|\\\\\\", "  * zap *" },
            SpringProb = 0.05f, SummerProb = 0.10f, FallProb = 0.10f, WinterProb = 0.05f
        },
        [AtmosphereWeatherType.Foggy] = new AtmosphereWeatherData
        {
            Name = "Foggy", Message = "Mysterious fog rolls in... spooky!",
            MoodModifier = 0, XpMultiplier = 1.2f, RareDropsBonus = 0.5f,
            Ascii = new() { "~ ~ ~ ~ ~ ~", " ~ ~ ~ ~ ~", "~ ~ ~ ~ ~ ~", " ~ fog ~ ~" },
            SpringProb = 0.05f, SummerProb = 0.02f, FallProb = 0.08f, WinterProb = 0.15f
        },
        [AtmosphereWeatherType.Snowy] = new AtmosphereWeatherData
        {
            Name = "Snowy", Message = "*catches snowflake* So pretty! So cold!",
            MoodModifier = 3, XpMultiplier = 1.2f,
            Ascii = new() { "  *  *  *  ", " *  *  *  *", "  *  *  *  ", "~~~~~~~~~~~~" },
            SpringProb = 0.02f, SummerProb = 0.0f, FallProb = 0.05f, WinterProb = 0.30f
        },
        [AtmosphereWeatherType.Windy] = new AtmosphereWeatherData
        {
            Name = "Windy", Message = "*feathers ruffled* Woooosh!",
            MoodModifier = 2, XpMultiplier = 1.0f,
            Ascii = new() { "  ~~ >>> ~~", " ~~ >>> ~~", "~~ >>> ~~", "  whoooosh" },
            SpringProb = 0.08f, SummerProb = 0.05f, FallProb = 0.12f, WinterProb = 0.10f
        },
        [AtmosphereWeatherType.Rainbow] = new AtmosphereWeatherData
        {
            Name = "Rainbow", Message = "A RAINBOW! Make a wish! This is MAGICAL!",
            MoodModifier = 15, XpMultiplier = 2.0f, Special = true,
            Ascii = new() { "   .--.", " .'    `.", "/  RAINBOW\\", "  colors! " },
            SpringProb = 0.0f, SummerProb = 0.0f, FallProb = 0.0f, WinterProb = 0.0f
        }
    };

    public static Dictionary<AtmosphereSeason, SeasonalContent> SeasonalContentMap { get; } = new()
    {
        [AtmosphereSeason.Spring] = new SeasonalContent
        {
            ItemsAvailable = new() { "spring_flower", "easter_egg", "cherry_blossom", "butterfly_net", "flower_seeds" },
            Events = new() { "cherry_blossom_festival", "egg_hunt" },
            Decorations = new() { "flower_wreath", "pastel_banner", "bunny_statue", "blossom_tree", "butterfly_garden" },
            MoodTheme = "renewal", XpBonus = 1.1f,
            ColorPalette = new() { "pink", "light_green", "yellow", "lavender" },
            SpecialActivities = new() { "flower_picking", "butterfly_watching", "spring_cleaning" },
            AmbientEffects = new() { "petals_falling", "birds_singing", "gentle_breeze" },
            GreetingMessages = new() { "Spring has sprung! New beginnings await!", "The flowers are blooming just for you!" }
        },
        [AtmosphereSeason.Summer] = new SeasonalContent
        {
            ItemsAvailable = new() { "watermelon", "sunscreen", "beach_ball", "ice_cream", "sunglasses", "seashell" },
            Events = new() { "beach_day", "fireworks_show" },
            Decorations = new() { "beach_umbrella", "sandcastle", "tiki_torch", "palm_tree", "hammock" },
            MoodTheme = "adventure", XpBonus = 1.0f,
            ColorPalette = new() { "bright_blue", "yellow", "orange", "coral" },
            SpecialActivities = new() { "swimming", "sunbathing", "beach_exploring" },
            AmbientEffects = new() { "sun_rays", "heat_shimmer", "waves" },
            GreetingMessages = new() { "Summer vibes! Time for adventure!", "The sun is shining just for you!" }
        },
        [AtmosphereSeason.Fall] = new SeasonalContent
        {
            ItemsAvailable = new() { "pumpkin", "autumn_leaf", "candy_corn", "apple_cider", "acorn", "warm_scarf" },
            Events = new() { "harvest_festival", "spooky_night" },
            Decorations = new() { "scarecrow", "hay_bale", "pumpkin_lantern", "leaf_pile", "harvest_basket" },
            MoodTheme = "cozy", XpBonus = 1.15f,
            ColorPalette = new() { "orange", "red", "brown", "gold" },
            SpecialActivities = new() { "leaf_jumping", "apple_picking", "cozy_napping" },
            AmbientEffects = new() { "leaves_falling", "crisp_air", "warm_glow" },
            GreetingMessages = new() { "Cozy autumn days are here!", "The leaves are changing colors!" }
        },
        [AtmosphereSeason.Winter] = new SeasonalContent
        {
            ItemsAvailable = new() { "hot_cocoa", "snowball", "candy_cane", "wrapped_gift", "mittens", "warm_blanket" },
            Events = new() { "first_snow", "winter_festival", "new_year_countdown" },
            Decorations = new() { "snow_duck", "string_lights", "wreath", "snowman", "ice_sculpture" },
            MoodTheme = "warmth", XpBonus = 1.2f,
            ColorPalette = new() { "white", "blue", "silver", "red", "green" },
            SpecialActivities = new() { "snowball_fights", "ice_skating", "cozy_cuddling" },
            AmbientEffects = new() { "snowfall", "frost", "twinkling_lights" },
            GreetingMessages = new() { "Winter wonderland! Stay warm and cozy!", "The snow makes everything magical!" }
        }
    };

    public static Dictionary<string, AtmosphereVisitor> Visitors { get; } = new()
    {
        ["friendly_goose"] = new AtmosphereVisitor
        {
            Id = "friendly_goose", Name = "Gerald the Goose",
            Description = "A surprisingly friendly goose waddles by!",
            AsciiArt = new() { "   __", " >(o )___", "  ( ._> /", "   `---'" },
            Greeting = "*HONK* Oh, a fellow waterfowl! Gerald has arrived!",
            Farewell = "*HONK* Gerald must go. Keep being awesome, friend!",
            GiftChance = 0.7f, PossibleGifts = new() { "bread", "shiny_pebble", "feather" },
            AppearanceChance = 0.25f, StayDurationHours = 0.05f,
            SpecialInteraction = "chat", MoodBoost = 15,
            Personality = "boisterous", FavoriteWeather = "sunny", FavoriteSeason = "summer",
            ReturnGreetings = new() { "*HONK* Gerald is back! Did you miss the honks?", "*happy honk* Cheese! My favorite duck!" },
            FriendGreetings = new() { "*affectionate honk* Cheese, my dear friend!" },
            BestFriendGreetings = new() { "*gentle honk* Best friend Cheese! Gerald missed you so much!" },
            SpecialGifts = new() { "golden_feather", "goose_down_pillow", "honorary_goose_badge" },
            Conversations = new() { "Gerald once flew across three lakes in one day! *proud honk*", "Did you know geese can remember faces?" },
            Secrets = new() { "Gerald is actually afraid of butterflies... don't tell anyone!" }
        },
        ["wise_owl"] = new AtmosphereVisitor
        {
            Id = "wise_owl", Name = "Professor Hoot",
            Description = "A wise owl visits under moonlight!",
            AsciiArt = new() { "  ,___,", "  (O,O)", "  /)_)", "   \" \"" },
            Greeting = "*hoo hoo* Greetings, young duck. I bring wisdom!",
            Farewell = "*hoo* Remember: knowledge is the greatest treasure. Farewell!",
            GiftChance = 0.9f, PossibleGifts = new() { "mysterious_crumb", "old_key", "crystal_shard" },
            AppearanceChance = 0.20f, StayDurationHours = 0.035f,
            SpecialInteraction = "learn", MoodBoost = 20,
            Personality = "scholarly", FavoriteWeather = "foggy", FavoriteSeason = "fall",
            SpecialGifts = new() { "ancient_tome", "wisdom_crystal", "star_chart" },
            Secrets = new() { "I once failed a flying test. Even professors make mistakes!" }
        },
        ["lost_duckling"] = new AtmosphereVisitor
        {
            Id = "lost_duckling", Name = "Pip the Duckling",
            Description = "A tiny lost duckling needs help!",
            AsciiArt = new() { " __", "(o>", " V" },
            Greeting = "*peep peep* I'm lost! Can I stay here for a bit?",
            Farewell = "*happy peep* Thank you for helping me! You're the best!",
            GiftChance = 1.0f, PossibleGifts = new() { "fluffy_down", "lucky_clover" },
            AppearanceChance = 0.15f, StayDurationHours = 0.08f,
            SpecialInteraction = "comfort", MoodBoost = 25,
            Personality = "shy", FavoriteWeather = "sunny", FavoriteSeason = "spring",
            SpecialGifts = new() { "friendship_bracelet", "tiny_flower_crown", "drawn_picture" },
            Secrets = new() { "I'm not really lost anymore. I just like visiting you!" }
        },
        ["traveling_merchant"] = new AtmosphereVisitor
        {
            Id = "traveling_merchant", Name = "Marco the Merchant",
            Description = "A traveling merchant duck appears with wares!",
            AsciiArt = new() { "   ,__,", "  (o.o)", " /|##|\\", "  d  b" },
            Greeting = "*quack* Greetings! Marco has exotic items from far lands!",
            Farewell = "*quack* Marco must continue the journey. Until next time!",
            GiftChance = 0.5f, PossibleGifts = new() { "fancy_bread", "glass_marble", "rainbow_crumb" },
            AppearanceChance = 0.12f, StayDurationHours = 0.05f,
            SpecialInteraction = "trade", MoodBoost = 10,
            Personality = "entrepreneurial", FavoriteWeather = "windy", FavoriteSeason = "fall",
            SpecialGifts = new() { "exotic_spices", "treasure_map", "enchanted_compass" }
        },
        ["celebrity_duck"] = new AtmosphereVisitor
        {
            Id = "celebrity_duck", Name = "Sir Quackington III",
            Description = "A famous noble duck graces you with their presence!",
            AsciiArt = new() { "  /\\  ", " (@@)", " /||\\", "  ''" },
            Greeting = "*regal quack* One has heard of your establishment. Impressive!",
            Farewell = "*noble nod* One shall speak well of this place. Farewell!",
            GiftChance = 0.8f, PossibleGifts = new() { "golden_crumb", "crown", "ancient_artifact" },
            AppearanceChance = 0.08f, StayDurationHours = 0.035f,
            SpecialInteraction = "impress", MoodBoost = 30,
            Personality = "regal", FavoriteWeather = "sunny", FavoriteSeason = "spring",
            SpecialGifts = new() { "royal_decree", "diamond_crumb", "noble_title" },
            Secrets = new() { "I actually prefer common bread over fancy crumpets!" }
        },
        ["mysterious_crow"] = new AtmosphereVisitor
        {
            Id = "mysterious_crow", Name = "Corvus the Crow",
            Description = "A cryptic crow appears with secrets...",
            AsciiArt = new() { "   ___", " /'o o'\\", " \\ V  /", "  ^^^" },
            Greeting = "*caw* I know things... secret things...",
            Farewell = "*caw* We will meet again when the stars align...",
            GiftChance = 0.6f, PossibleGifts = new() { "old_key", "crystal_shard", "ancient_artifact" },
            AppearanceChance = 0.10f, StayDurationHours = 0.035f,
            SpecialInteraction = "mystery", MoodBoost = 5,
            Personality = "mysterious", FavoriteWeather = "foggy", FavoriteSeason = "winter",
            SpecialGifts = new() { "shadow_feather", "prophecy_scroll", "void_crystal" },
            Secrets = new() { "I'm not actually mysterious. I just have social anxiety." }
        },
        ["butterfly_fairy"] = new AtmosphereVisitor
        {
            Id = "butterfly_fairy", Name = "Flutter",
            Description = "A magical butterfly with gossamer wings appears!",
            AsciiArt = new() { "  \\  /", "  (oo)", "  /  \\", "  ~~~~" },
            Greeting = "*sparkle* Hello little duck! I'm Flutter! *twirl*",
            Farewell = "*shimmer* May flowers bloom wherever you waddle!",
            GiftChance = 0.9f, PossibleGifts = new() { "flower_petal", "fairy_dust", "rainbow_scale" },
            AppearanceChance = 0.12f, StayDurationHours = 0.05f,
            SpecialInteraction = "wish", MoodBoost = 20,
            Personality = "whimsical", FavoriteWeather = "sunny", FavoriteSeason = "spring",
            SpecialGifts = new() { "enchanted_pollen", "rainbow_wing_scale", "eternal_bloom" },
            Secrets = new() { "I'm 300 years old! Butterflies live long in the magic meadows!" }
        },
        ["grumpy_toad"] = new AtmosphereVisitor
        {
            Id = "grumpy_toad", Name = "Grumble the Toad",
            Description = "A grumpy toad hops by, looking annoyed!",
            AsciiArt = new() { "  @..@", " (---)", " (---)", "  \\_/" },
            Greeting = "*ribbit* What? I'm just passing through. Don't get excited.",
            Farewell = "*grumble* Fine, this was... acceptable. Don't expect me back.",
            GiftChance = 0.4f, PossibleGifts = new() { "pond_lily", "lucky_stone", "mud_cake" },
            AppearanceChance = 0.15f, StayDurationHours = 0.035f,
            SpecialInteraction = "listen", MoodBoost = 5,
            Personality = "grumpy", FavoriteWeather = "rainy", FavoriteSeason = "fall",
            SpecialGifts = new() { "rare_swamp_crystal", "ancient_tadpole_fossil", "grumble_cookie" },
            Secrets = new() { "I write poetry. It's all about friendship. Tell no one." }
        }
    };

    public ExtendedAtmosphereSystem()
    {
        CurrentSeason = CalculateSeason();
        GenerateWeather();
        GenerateFortune();
    }

    private AtmosphereSeason CalculateSeason()
    {
        var month = DateTime.Now.Month;
        return month switch
        {
            >= 3 and <= 5 => AtmosphereSeason.Spring,
            >= 6 and <= 8 => AtmosphereSeason.Summer,
            >= 9 and <= 11 => AtmosphereSeason.Fall,
            _ => AtmosphereSeason.Winter
        };
    }

    private void GenerateWeather()
    {
        var seasonKey = CurrentSeason;
        var weatherOptions = new List<AtmosphereWeatherType>();

        foreach (var (weatherType, data) in WeatherDataMap)
        {
            if (data.Special) continue;
            var prob = seasonKey switch
            {
                AtmosphereSeason.Spring => data.SpringProb,
                AtmosphereSeason.Summer => data.SummerProb,
                AtmosphereSeason.Fall => data.FallProb,
                AtmosphereSeason.Winter => data.WinterProb,
                _ => 0.1f
            };
            var weight = Math.Max(1, (int)(prob * 100));
            for (int i = 0; i < weight; i++) weatherOptions.Add(weatherType);
        }

        var chosenType = weatherOptions[_random.Next(weatherOptions.Count)];
        var weatherData = WeatherDataMap[chosenType];

        CurrentWeather = new AtmosphereWeather
        {
            Type = chosenType,
            Intensity = (float)(_random.NextDouble() * 0.7 + 0.3),
            DurationHours = (float)(_random.NextDouble() * 5 + 1),
            StartTime = DateTime.Now,
            MoodModifier = weatherData.MoodModifier,
            XpMultiplier = weatherData.XpMultiplier,
            SpecialMessage = weatherData.Message
        };

        WeatherHistory.Add(chosenType.ToString());
        if (WeatherHistory.Count > 10) WeatherHistory.RemoveAt(0);
    }

    private void GenerateFortune()
    {
        var today = DateTime.Now.Date;
        if (LastFortuneDate == today && DayFortune != null) return;

        var roll = _random.NextDouble();
        string fortuneType;
        float xpMult, dropMult;

        if (roll < 0.02) { fortuneType = "super_lucky"; xpMult = 2.0f; dropMult = 3.0f; }
        else if (roll < 0.17) { fortuneType = "lucky"; xpMult = 1.3f; dropMult = 1.5f; }
        else if (roll < 0.87) { fortuneType = "normal"; xpMult = 1.0f; dropMult = 1.0f; }
        else { fortuneType = "unlucky"; xpMult = 0.9f; dropMult = 0.7f; }

        DayFortune = new DayFortune
        {
            FortuneType = fortuneType,
            XpMultiplier = xpMult,
            DropRateModifier = dropMult,
            SpecialMessage = GetFortuneMessage(fortuneType),
            Horoscope = GetHoroscope(fortuneType)
        };
        LastFortuneDate = today;
    }

    private string GetFortuneMessage(string type) => type switch
    {
        "super_lucky" => "The stars align! SUPER LUCKY DAY!",
        "lucky" => "Feeling lucky today! Good things are coming!",
        "unlucky" => "Not the luckiest day, but that makes the good days better!",
        _ => "A pleasant, ordinary day!"
    };

    private string GetHoroscope(string type) => type switch
    {
        "super_lucky" => "Today, even the bread crumbs lead to treasure!",
        "lucky" => "Fortune favors the bold duck today!",
        "unlucky" => "Even unlucky days teach valuable lessons!",
        _ => "Balance in all things today!"
    };

    public List<string> Update()
    {
        var messages = new List<string>();

        var newSeason = CalculateSeason();
        if (newSeason != CurrentSeason)
        {
            CurrentSeason = newSeason;
            var content = SeasonalContentMap[newSeason];
            messages.Add($"AtmosphereSeason changed to {newSeason}! {content.MoodTheme} vibes!");
        }

        if (CurrentWeather != null && !CurrentWeather.IsActive())
        {
            if (CurrentWeather.Type == AtmosphereWeatherType.Rainy && _random.NextDouble() < 0.2)
            {
                var rainbowData = WeatherDataMap[AtmosphereWeatherType.Rainbow];
                CurrentWeather = new AtmosphereWeather
                {
                    Type = AtmosphereWeatherType.Rainbow, Intensity = 1.0f, DurationHours = 0.5f,
                    StartTime = DateTime.Now, MoodModifier = rainbowData.MoodModifier,
                    XpMultiplier = rainbowData.XpMultiplier, SpecialMessage = rainbowData.Message
                };
            }
            else
            {
                GenerateWeather();
                messages.Add($"AtmosphereWeather changed: {CurrentWeather.SpecialMessage}");
            }
        }

        var today = DateTime.Now.Date;
        if (LastFortuneDate != today)
        {
            GenerateFortune();
            messages.Add($"Today's fortune: {DayFortune?.Horoscope}");
        }

        var visitorMsg = CheckVisitor();
        if (visitorMsg != null) messages.Add(visitorMsg);

        return messages;
    }

    private string? CheckVisitor()
    {
        if (CurrentVisitor != null)
        {
            var (visitor, arrival) = CurrentVisitor.Value;
            if ((DateTime.Now - arrival).TotalHours >= visitor.StayDurationHours)
            {
                CurrentVisitor = null;
                return visitor.Farewell;
            }
        }

        if (CurrentVisitor == null && _random.NextDouble() < 0.01)
        {
            var candidates = new List<string>();
            foreach (var (visitorId, visitor) in Visitors)
            {
                var chance = visitor.AppearanceChance;
                if (VisitorFriendships.TryGetValue(visitorId, out var friendship))
                {
                    chance *= friendship.Level switch
                    {
                        AtmosphereFriendshipLevel.BestFriend => 3.0f,
                        AtmosphereFriendshipLevel.GoodFriend => 2.5f,
                        AtmosphereFriendshipLevel.Friend => 2.0f,
                        AtmosphereFriendshipLevel.Acquaintance => 1.5f,
                        _ => 1.0f
                    };
                }

                if (CurrentWeather != null && visitor.FavoriteWeather == CurrentWeather.Type.ToString().ToLower())
                    chance *= 1.5f;
                if (visitor.FavoriteSeason == CurrentSeason.ToString().ToLower())
                    chance *= 1.3f;

                if (_random.NextDouble() < chance) candidates.Add(visitorId);
            }

            if (candidates.Count > 0)
            {
                var visitorId = candidates[_random.Next(candidates.Count)];
                var visitor = Visitors[visitorId];
                CurrentVisitor = (visitor, DateTime.Now);
                VisitorHistory.Add(visitorId);
                if (VisitorHistory.Count > 50) VisitorHistory.RemoveAt(0);

                if (!VisitorFriendships.ContainsKey(visitorId))
                    VisitorFriendships[visitorId] = new AtmosphereVisitorFriendship { VisitorId = visitorId };
                VisitorFriendships[visitorId].AddVisit();

                return GetVisitorGreeting(visitor, visitorId);
            }
        }

        return null;
    }

    private string GetVisitorGreeting(AtmosphereVisitor visitor, string visitorId)
    {
        if (!VisitorFriendships.TryGetValue(visitorId, out var friendship) || friendship.VisitCount <= 1)
            return visitor.Greeting;

        return friendship.Level switch
        {
            AtmosphereFriendshipLevel.BestFriend when visitor.BestFriendGreetings.Count > 0 
                => visitor.BestFriendGreetings[_random.Next(visitor.BestFriendGreetings.Count)],
            AtmosphereFriendshipLevel.GoodFriend or AtmosphereFriendshipLevel.Friend when visitor.FriendGreetings.Count > 0 
                => visitor.FriendGreetings[_random.Next(visitor.FriendGreetings.Count)],
            _ when visitor.ReturnGreetings.Count > 0 
                => visitor.ReturnGreetings[_random.Next(visitor.ReturnGreetings.Count)],
            _ => visitor.Greeting
        };
    }

    public float GetTotalXpMultiplier()
    {
        float mult = 1.0f;
        if (SeasonalContentMap.TryGetValue(CurrentSeason, out var content)) mult *= content.XpBonus;
        if (CurrentWeather != null) mult *= CurrentWeather.XpMultiplier;
        if (DayFortune != null) mult *= DayFortune.XpMultiplier;
        return mult;
    }

    public float GetDropRateModifier()
    {
        float mod = DayFortune?.DropRateModifier ?? 1.0f;
        if (CurrentWeather?.Type == AtmosphereWeatherType.Foggy) mod *= 1.5f;
        return mod;
    }

    public int GetMoodModifier()
    {
        int mood = CurrentWeather?.MoodModifier ?? 0;
        if (CurrentVisitor != null) mood += CurrentVisitor.Value.AtmosphereVisitor.MoodBoost;
        return mood;
    }

    public (string Message, string? Gift)? InteractWithVisitor()
    {
        if (CurrentVisitor == null) return null;

        var (visitor, _) = CurrentVisitor.Value;
        if (VisitorFriendships.TryGetValue(visitor.Id, out var friendship))
            friendship.AddInteraction(1);

        var level = friendship?.Level ?? AtmosphereFriendshipLevel.Stranger;
        var giftChance = visitor.GiftChance;
        giftChance += level switch
        {
            AtmosphereFriendshipLevel.BestFriend => 0.3f,
            AtmosphereFriendshipLevel.GoodFriend => 0.2f,
            AtmosphereFriendshipLevel.Friend => 0.1f,
            _ => 0
        };

        string? gift = null;
        string message;

        if (_random.NextDouble() < Math.Min(1.0, giftChance))
        {
            if (level == AtmosphereFriendshipLevel.BestFriend && visitor.SpecialGifts.Count > 0)
            {
                gift = visitor.SpecialGifts[_random.Next(visitor.SpecialGifts.Count)];
                message = $"{visitor.Name}: *gives you something special* For my best friend!";
            }
            else if (visitor.PossibleGifts.Count > 0)
            {
                gift = visitor.PossibleGifts[_random.Next(visitor.PossibleGifts.Count)];
                message = $"{visitor.Name}: *gives you something* Here, take this!";
            }
            else
            {
                message = $"{visitor.Name}: I wish I had something to give you!";
            }
        }
        else
        {
            message = visitor.Conversations.Count > 0 
                ? $"{visitor.Name}: {visitor.Conversations[_random.Next(visitor.Conversations.Count)]}"
                : $"{visitor.Name}: *quacks happily* Nice to meet you!";
        }

        if (gift != null && friendship != null) friendship.GiftsReceived.Add(gift);
        return (message, gift);
    }

    public Dictionary<string, object> ToSaveData() => new()
    {
        ["current_season"] = CurrentSeason.ToString(),
        ["current_weather"] = CurrentWeather != null ? new Dictionary<string, object>
        {
            ["type"] = CurrentWeather.Type.ToString(),
            ["intensity"] = CurrentWeather.Intensity,
            ["duration"] = CurrentWeather.DurationHours,
            ["start"] = CurrentWeather.StartTime.ToString("o")
        } : null!,
        ["day_fortune"] = DayFortune != null ? new Dictionary<string, object>
        {
            ["type"] = DayFortune.FortuneType,
            ["xp_mult"] = DayFortune.XpMultiplier,
            ["drop_mult"] = DayFortune.DropRateModifier
        } : null!,
        ["last_fortune_date"] = LastFortuneDate?.ToString("o") ?? "",
        ["visitor_history"] = VisitorHistory.TakeLast(20).ToList(),
        ["weather_history"] = WeatherHistory,
        ["visitor_friendships"] = VisitorFriendships.ToDictionary(
            kv => kv.Key,
            kv => new Dictionary<string, object>
            {
                ["visit_count"] = kv.Value.VisitCount,
                ["friendship_points"] = kv.Value.FriendshipPoints,
                ["gifts_received"] = kv.Value.GiftsReceived.TakeLast(20).ToList()
            })
    };

    public static ExtendedAtmosphereSystem FromSaveData(Dictionary<string, object> data)
    {
        var atm = new ExtendedAtmosphereSystem();
        if (data.TryGetValue("current_season", out var s) && Enum.TryParse<AtmosphereSeason>(s.ToString(), out var season))
            atm.CurrentSeason = season;
        if (data.TryGetValue("last_fortune_date", out var d) && DateTime.TryParse(d.ToString(), out var date))
            atm.LastFortuneDate = date;
        return atm;
    }
}
