using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;

namespace StupidDuck.World;

/// <summary>
/// Duck zodiac signs based on birthday.
/// </summary>
public enum DuckZodiacSign
{
    Mallard,         // Jan 20 - Feb 18 (Aquarius)
    Pekin,           // Feb 19 - Mar 20 (Pisces)
    Muscovy,         // Mar 21 - Apr 19 (Aries)
    Runner,          // Apr 20 - May 20 (Taurus)
    Cayuga,          // May 21 - Jun 20 (Gemini)
    Rouen,           // Jun 21 - Jul 22 (Cancer)
    KhakiCampbell,   // Jul 23 - Aug 22 (Leo)
    Swedish,         // Aug 23 - Sep 22 (Virgo)
    Buff,            // Sep 23 - Oct 22 (Libra)
    Magpie,          // Oct 23 - Nov 21 (Scorpio)
    Call,            // Nov 22 - Dec 21 (Sagittarius)
    WelshHarlequin   // Dec 22 - Jan 19 (Capricorn)
}

/// <summary>
/// Categories of fortune predictions.
/// </summary>
public enum FortuneCategory
{
    General,
    Love,
    Luck,
    Adventure,
    Wealth,
    Friendship,
    Health,
    Wisdom
}

/// <summary>
/// Rarity of fortune cookies.
/// </summary>
public enum FortuneRarity
{
    Common,
    Uncommon,
    Rare,
    Legendary
}

/// <summary>
/// Information about a duck zodiac sign.
/// </summary>
public class ZodiacInfo
{
    public DuckZodiacSign Sign { get; init; }
    public string Name { get; init; } = "";
    public string Symbol { get; init; } = "";
    public string Element { get; init; } = "";
    public List<string> Traits { get; init; } = new();
    public List<DuckZodiacSign> CompatibleSigns { get; init; } = new();
    public List<string> LuckyItems { get; init; } = new();
    public List<string> LuckyColors { get; init; } = new();
    public List<int> LuckyNumbers { get; init; } = new();
    public string Description { get; init; } = "";
}

/// <summary>
/// A daily horoscope reading.
/// </summary>
public class DailyHoroscope
{
    public string Date { get; set; } = "";
    public DuckZodiacSign Sign { get; set; }
    public string GeneralFortune { get; set; } = "";
    public string LuckyItem { get; set; } = "";
    public string LuckyColor { get; set; } = "";
    public int LuckyNumber { get; set; }
    public string MoodPrediction { get; set; } = "";
    public string ActivitySuggestion { get; set; } = "";
    public int FortuneLevel { get; set; }  // 1-5 stars
    public string? SpecialMessage { get; set; }
}

/// <summary>
/// A fortune cookie with a message.
/// </summary>
public class FortuneCookie
{
    public string CookieId { get; set; } = "";
    public string Message { get; set; } = "";
    public FortuneCategory Category { get; set; }
    public FortuneRarity Rarity { get; set; }
    public List<int> LuckyNumbers { get; set; } = new();
    public string DateReceived { get; set; } = "";
    public bool IsRevealed { get; set; }
}

/// <summary>
/// Fortune & Horoscope System - Daily fortunes, zodiac signs, and mystical predictions.
/// </summary>
public class FortuneSystem
{
    private static readonly Random _random = new();
    
    public DateTime? DuckBirthday { get; private set; }
    public DuckZodiacSign? ZodiacSign { get; private set; }
    public DateTime? LastHoroscopeDate { get; private set; }
    public List<FortuneCookie> FortuneCookies { get; private set; } = new();
    public List<string> FavoriteFortunes { get; private set; } = new();
    public int DailyLuckStreak { get; private set; }
    public int TotalCookiesOpened { get; private set; }
    public int RareCookiesFound { get; private set; }
    public int LuckyEventsTriggered { get; set; }
    
    // Zodiac definitions
    private static readonly Dictionary<DuckZodiacSign, ZodiacInfo> ZodiacInfoMap = new()
    {
        [DuckZodiacSign.Mallard] = new ZodiacInfo
        {
            Sign = DuckZodiacSign.Mallard,
            Name = "The Mallard",
            Symbol = "🦆",
            Element = "Air",
            Traits = new List<string> { "Free-spirited", "Social", "Adaptable", "Innovative" },
            CompatibleSigns = new List<DuckZodiacSign> { DuckZodiacSign.Cayuga, DuckZodiacSign.Call, DuckZodiacSign.Buff },
            LuckyItems = new List<string> { "Feather", "Blue ribbon", "Wind chime" },
            LuckyColors = new List<string> { "Iridescent green", "Sky blue" },
            LuckyNumbers = new List<int> { 7, 11, 22 },
            Description = "Mallards are natural leaders with a flair for the unconventional. They swim against the current and inspire others to do the same."
        },
        [DuckZodiacSign.Pekin] = new ZodiacInfo
        {
            Sign = DuckZodiacSign.Pekin,
            Name = "The Pekin",
            Symbol = "🐤",
            Element = "Water",
            Traits = new List<string> { "Dreamy", "Gentle", "Intuitive", "Artistic" },
            CompatibleSigns = new List<DuckZodiacSign> { DuckZodiacSign.Rouen, DuckZodiacSign.Cayuga, DuckZodiacSign.Swedish },
            LuckyItems = new List<string> { "Pearl", "Lily pad", "Moon pendant" },
            LuckyColors = new List<string> { "Pure white", "Pearl pink" },
            LuckyNumbers = new List<int> { 3, 9, 12 },
            Description = "Pekins are the dreamers of the duck world. They have deep emotional intelligence and a natural artistic flair."
        },
        [DuckZodiacSign.Muscovy] = new ZodiacInfo
        {
            Sign = DuckZodiacSign.Muscovy,
            Name = "The Muscovy",
            Symbol = "💪",
            Element = "Fire",
            Traits = new List<string> { "Bold", "Independent", "Courageous", "Pioneering" },
            CompatibleSigns = new List<DuckZodiacSign> { DuckZodiacSign.KhakiCampbell, DuckZodiacSign.Call, DuckZodiacSign.Runner },
            LuckyItems = new List<string> { "Red stone", "Sun medal", "Courage token" },
            LuckyColors = new List<string> { "Crimson", "Orange" },
            LuckyNumbers = new List<int> { 1, 9, 19 },
            Description = "Muscovys charge ahead where others fear to waddle. Natural pioneers who blaze new trails."
        },
        [DuckZodiacSign.Runner] = new ZodiacInfo
        {
            Sign = DuckZodiacSign.Runner,
            Name = "The Runner",
            Symbol = "🏃",
            Element = "Earth",
            Traits = new List<string> { "Determined", "Patient", "Reliable", "Luxurious" },
            CompatibleSigns = new List<DuckZodiacSign> { DuckZodiacSign.Swedish, DuckZodiacSign.WelshHarlequin, DuckZodiacSign.Pekin },
            LuckyItems = new List<string> { "Garden stone", "Copper coin", "Rose petal" },
            LuckyColors = new List<string> { "Emerald", "Earthy brown" },
            LuckyNumbers = new List<int> { 2, 6, 15 },
            Description = "Runners are steady and dependable. They appreciate the finer things and work hard to achieve comfort."
        },
        [DuckZodiacSign.Cayuga] = new ZodiacInfo
        {
            Sign = DuckZodiacSign.Cayuga,
            Name = "The Cayuga",
            Symbol = "🌟",
            Element = "Air",
            Traits = new List<string> { "Curious", "Witty", "Versatile", "Communicative" },
            CompatibleSigns = new List<DuckZodiacSign> { DuckZodiacSign.Mallard, DuckZodiacSign.Buff, DuckZodiacSign.Call },
            LuckyItems = new List<string> { "Twin feathers", "Journal", "Lucky dice" },
            LuckyColors = new List<string> { "Beetle green", "Yellow" },
            LuckyNumbers = new List<int> { 5, 14, 23 },
            Description = "Cayugas are quick-witted and love to learn. They have beautiful iridescent feathers that shift like their moods."
        },
        [DuckZodiacSign.Rouen] = new ZodiacInfo
        {
            Sign = DuckZodiacSign.Rouen,
            Name = "The Rouen",
            Symbol = "🏠",
            Element = "Water",
            Traits = new List<string> { "Nurturing", "Protective", "Emotional", "Home-loving" },
            CompatibleSigns = new List<DuckZodiacSign> { DuckZodiacSign.Pekin, DuckZodiacSign.Magpie, DuckZodiacSign.Swedish },
            LuckyItems = new List<string> { "Shell", "Family photo", "Nest material" },
            LuckyColors = new List<string> { "Silver", "Cream" },
            LuckyNumbers = new List<int> { 2, 7, 11 },
            Description = "Rouens are the nurturers. They create warm, welcoming spaces and protect those they love fiercely."
        },
        [DuckZodiacSign.KhakiCampbell] = new ZodiacInfo
        {
            Sign = DuckZodiacSign.KhakiCampbell,
            Name = "The Khaki Campbell",
            Symbol = "👑",
            Element = "Fire",
            Traits = new List<string> { "Confident", "Generous", "Dramatic", "Warm-hearted" },
            CompatibleSigns = new List<DuckZodiacSign> { DuckZodiacSign.Muscovy, DuckZodiacSign.Call, DuckZodiacSign.Buff },
            LuckyItems = new List<string> { "Gold coin", "Crown charm", "Sunflower" },
            LuckyColors = new List<string> { "Gold", "Khaki" },
            LuckyNumbers = new List<int> { 1, 10, 19 },
            Description = "Khaki Campbells are born performers who love the spotlight. They're generous and warm but demand recognition."
        },
        [DuckZodiacSign.Swedish] = new ZodiacInfo
        {
            Sign = DuckZodiacSign.Swedish,
            Name = "The Swedish",
            Symbol = "📋",
            Element = "Earth",
            Traits = new List<string> { "Analytical", "Practical", "Helpful", "Detail-oriented" },
            CompatibleSigns = new List<DuckZodiacSign> { DuckZodiacSign.Runner, DuckZodiacSign.Rouen, DuckZodiacSign.WelshHarlequin },
            LuckyItems = new List<string> { "Checklist", "Blue flower", "Perfect pebble" },
            LuckyColors = new List<string> { "Blue", "Slate grey" },
            LuckyNumbers = new List<int> { 3, 6, 27 },
            Description = "Swedish ducks are the organizers. They notice every detail and strive for perfection in all they do."
        },
        [DuckZodiacSign.Buff] = new ZodiacInfo
        {
            Sign = DuckZodiacSign.Buff,
            Name = "The Buff",
            Symbol = "⚖️",
            Element = "Air",
            Traits = new List<string> { "Diplomatic", "Charming", "Fair", "Artistic" },
            CompatibleSigns = new List<DuckZodiacSign> { DuckZodiacSign.Cayuga, DuckZodiacSign.Mallard, DuckZodiacSign.KhakiCampbell },
            LuckyItems = new List<string> { "Balance scale", "Rose quartz", "Art brush" },
            LuckyColors = new List<string> { "Buff", "Pastel pink" },
            LuckyNumbers = new List<int> { 4, 13, 22 },
            Description = "Buffs seek harmony in all things. They're natural diplomats with excellent taste and charming personalities."
        },
        [DuckZodiacSign.Magpie] = new ZodiacInfo
        {
            Sign = DuckZodiacSign.Magpie,
            Name = "The Magpie",
            Symbol = "🔮",
            Element = "Water",
            Traits = new List<string> { "Mysterious", "Intense", "Passionate", "Perceptive" },
            CompatibleSigns = new List<DuckZodiacSign> { DuckZodiacSign.Rouen, DuckZodiacSign.Pekin, DuckZodiacSign.WelshHarlequin },
            LuckyItems = new List<string> { "Black pearl", "Mystery box", "Obsidian" },
            LuckyColors = new List<string> { "Black", "Deep purple" },
            LuckyNumbers = new List<int> { 8, 11, 18 },
            Description = "Magpies are drawn to mystery and secrets. They have intense emotions and see through pretense."
        },
        [DuckZodiacSign.Call] = new ZodiacInfo
        {
            Sign = DuckZodiacSign.Call,
            Name = "The Call",
            Symbol = "🏹",
            Element = "Fire",
            Traits = new List<string> { "Adventurous", "Optimistic", "Philosophical", "Honest" },
            CompatibleSigns = new List<DuckZodiacSign> { DuckZodiacSign.Mallard, DuckZodiacSign.Muscovy, DuckZodiacSign.Cayuga },
            LuckyItems = new List<string> { "Map", "Arrow charm", "Lucky horseshoe" },
            LuckyColors = new List<string> { "Purple", "Turquoise" },
            LuckyNumbers = new List<int> { 3, 9, 12 },
            Description = "Calls are the philosophers and adventurers. Their loud voice matches their big dreams and bigger heart."
        },
        [DuckZodiacSign.WelshHarlequin] = new ZodiacInfo
        {
            Sign = DuckZodiacSign.WelshHarlequin,
            Name = "The Welsh Harlequin",
            Symbol = "🏔️",
            Element = "Earth",
            Traits = new List<string> { "Ambitious", "Disciplined", "Patient", "Responsible" },
            CompatibleSigns = new List<DuckZodiacSign> { DuckZodiacSign.Runner, DuckZodiacSign.Swedish, DuckZodiacSign.Magpie },
            LuckyItems = new List<string> { "Mountain crystal", "Clock charm", "Building block" },
            LuckyColors = new List<string> { "Dark brown", "Forest green" },
            LuckyNumbers = new List<int> { 4, 8, 17 },
            Description = "Welsh Harlequins are the builders. Patient and ambitious, they work steadily toward their lofty goals."
        }
    };
    
    // Fortune cookie messages
    private static readonly Dictionary<FortuneCategory, Dictionary<FortuneRarity, List<string>>> FortuneMessages = new()
    {
        [FortuneCategory.General] = new Dictionary<FortuneRarity, List<string>>
        {
            [FortuneRarity.Common] = new List<string>
            {
                "Today will be a good day for quacking.",
                "The pond awaits your presence.",
                "A feather in the wind leads to adventure.",
                "Sometimes the best path is the one with the most puddles.",
                "Bread crumbs are a duck's best friend."
            },
            [FortuneRarity.Uncommon] = new List<string>
            {
                "An unexpected visitor brings good tidings.",
                "The next sunset will bring clarity to your thoughts.",
                "Trust your waddle - it knows the way.",
                "A shiny object will catch your attention soon.",
                "The universe quacks in mysterious ways."
            },
            [FortuneRarity.Rare] = new List<string>
            {
                "A golden opportunity lies beneath the surface.",
                "Your feathers will shine with destiny's light.",
                "The stars align in favor of your next adventure.",
                "Something lost shall be found by week's end."
            },
            [FortuneRarity.Legendary] = new List<string>
            {
                "You are destined for greatness, little duck.",
                "The legendary Golden Bread awaits those who seek it.",
                "Your quack echoes through the halls of eternity."
            }
        },
        [FortuneCategory.Love] = new Dictionary<FortuneRarity, List<string>>
        {
            [FortuneRarity.Common] = new List<string>
            {
                "Your human thinks of you fondly right now.",
                "Love is found in simple moments of care.",
                "A pet on the head brings joy to the heart."
            },
            [FortuneRarity.Uncommon] = new List<string>
            {
                "A deep bond will grow stronger this week.",
                "Your affection will be returned tenfold.",
                "The heart knows what the beak cannot say."
            },
            [FortuneRarity.Rare] = new List<string>
            {
                "A soulmate watches over you from afar.",
                "Your love creates ripples across the universe."
            },
            [FortuneRarity.Legendary] = new List<string>
            {
                "You are loved beyond measure - eternally."
            }
        },
        [FortuneCategory.Luck] = new Dictionary<FortuneRarity, List<string>>
        {
            [FortuneRarity.Common] = new List<string>
            {
                "Good luck flows like water today.",
                "Fortune favors the bold duck.",
                "A lucky number will appear soon."
            },
            [FortuneRarity.Uncommon] = new List<string>
            {
                "Unexpected fortune comes your way.",
                "The odds are ever in your favor.",
                "Lucky finds await the patient seeker."
            },
            [FortuneRarity.Rare] = new List<string>
            {
                "A four-leaf clover blooms in your path.",
                "Lady Luck has taken notice of you."
            },
            [FortuneRarity.Legendary] = new List<string>
            {
                "You ARE luck incarnate."
            }
        },
        [FortuneCategory.Adventure] = new Dictionary<FortuneRarity, List<string>>
        {
            [FortuneRarity.Common] = new List<string>
            {
                "A new path opens before you.",
                "Adventure is just a waddle away.",
                "The world is your pond."
            },
            [FortuneRarity.Uncommon] = new List<string>
            {
                "An exciting journey awaits beyond the familiar.",
                "Discovery comes to those who explore.",
                "Uncharted waters call your name."
            },
            [FortuneRarity.Rare] = new List<string>
            {
                "A legendary quest shall present itself.",
                "The greatest adventure of your life approaches."
            },
            [FortuneRarity.Legendary] = new List<string>
            {
                "You shall explore realms yet undreamed of."
            }
        },
        [FortuneCategory.Wealth] = new Dictionary<FortuneRarity, List<string>>
        {
            [FortuneRarity.Common] = new List<string>
            {
                "A small treasure hides nearby.",
                "Wealth comes in many forms - including bread.",
                "Your collection grows steadily."
            },
            [FortuneRarity.Uncommon] = new List<string>
            {
                "A generous gift approaches.",
                "Investment in friendship pays the highest dividends.",
                "Abundance flows to the grateful duck."
            },
            [FortuneRarity.Rare] = new List<string>
            {
                "Riches beyond bread await your discovery.",
                "A fortune in coins shall be yours."
            },
            [FortuneRarity.Legendary] = new List<string>
            {
                "You shall want for nothing, ever."
            }
        },
        [FortuneCategory.Friendship] = new Dictionary<FortuneRarity, List<string>>
        {
            [FortuneRarity.Common] = new List<string>
            {
                "A friend thinks of you today.",
                "Friendship makes the pond brighter.",
                "Share your bread, share your joy."
            },
            [FortuneRarity.Uncommon] = new List<string>
            {
                "A new friend awaits introduction.",
                "Old friends return with happy news.",
                "Your flock grows stronger together."
            },
            [FortuneRarity.Rare] = new List<string>
            {
                "A friendship forged now shall last forever.",
                "You are the friend everyone hopes to find."
            },
            [FortuneRarity.Legendary] = new List<string>
            {
                "Your friendships shape the very stars."
            }
        },
        [FortuneCategory.Health] = new Dictionary<FortuneRarity, List<string>>
        {
            [FortuneRarity.Common] = new List<string>
            {
                "Healthy feathers, happy duck.",
                "A good preen keeps problems at bay.",
                "Rest well to waddle far."
            },
            [FortuneRarity.Uncommon] = new List<string>
            {
                "Vitality surges through your wings.",
                "Your energy shall know no bounds today.",
                "Balance in all things brings wellness."
            },
            [FortuneRarity.Rare] = new List<string>
            {
                "Peak condition is your natural state.",
                "You radiate with vibrant health."
            },
            [FortuneRarity.Legendary] = new List<string>
            {
                "You are blessed with eternal vigor."
            }
        },
        [FortuneCategory.Wisdom] = new Dictionary<FortuneRarity, List<string>>
        {
            [FortuneRarity.Common] = new List<string>
            {
                "The wise duck listens before quacking.",
                "Patience is a virtue, even for ducks.",
                "Learn from yesterday, hope for tomorrow."
            },
            [FortuneRarity.Uncommon] = new List<string>
            {
                "Deep thoughts lead to greater understanding.",
                "The answer you seek lies within.",
                "Wisdom comes to those who observe."
            },
            [FortuneRarity.Rare] = new List<string>
            {
                "You carry knowledge beyond your years.",
                "Others seek your counsel for good reason."
            },
            [FortuneRarity.Legendary] = new List<string>
            {
                "You are a sage among ducks."
            }
        }
    };
    
    // Horoscope templates by fortune level
    private static readonly Dictionary<int, List<string>> HoroscopeTemplates = new()
    {
        [1] = new List<string>
        {
            "The stars suggest a day of rest. Stay close to home and avoid unnecessary risks.",
            "A challenging day lies ahead. Find comfort in familiar routines.",
            "The cosmic energies are scrambled. Best to keep expectations low today."
        },
        [2] = new List<string>
        {
            "A slightly bumpy day ahead. Patience will be your greatest ally.",
            "Minor obstacles may appear. Face them with resilience.",
            "The universe tests your resolve today. Stay strong, little duck."
        },
        [3] = new List<string>
        {
            "A balanced day awaits. Neither great nor poor - embrace the ordinary.",
            "The stars shine neutrally. Make of today what you will.",
            "Average energies surround you. A good day for steady progress."
        },
        [4] = new List<string>
        {
            "Good fortune flows your way! Seize opportunities as they appear.",
            "The stars smile upon you today. Take confident action.",
            "Positive energy surrounds you. A wonderful day for new beginnings."
        },
        [5] = new List<string>
        {
            "AMAZING! The stars align perfectly! Today is YOUR day!",
            "Cosmic forces conspire in your favor! Embrace every moment!",
            "A legendary day awaits! Nothing can stop you now!"
        }
    };
    
    private static readonly List<string> MoodPredictions = new()
    {
        "cheerful and energetic",
        "calm and contemplative",
        "playful and mischievous",
        "cuddly and affectionate",
        "adventurous and bold",
        "peaceful and serene",
        "curious and explorative",
        "cozy and content"
    };
    
    private static readonly List<string> ActivitySuggestions = new()
    {
        "take a relaxing swim",
        "explore somewhere new",
        "spend quality time with your human",
        "practice your favorite trick",
        "hunt for hidden treasures",
        "make a new friend",
        "rest and recharge",
        "enjoy a delicious meal",
        "splash in puddles",
        "collect shiny things",
        "preen your feathers extra thoroughly",
        "try something you've never done before"
    };
    
    /// <summary>
    /// Set the duck's birthday and determine zodiac sign.
    /// </summary>
    public void SetDuckBirthday(DateTime birthday)
    {
        DuckBirthday = birthday;
        ZodiacSign = GetZodiacSign(birthday);
    }
    
    /// <summary>
    /// Determine zodiac sign from birthday.
    /// </summary>
    public static DuckZodiacSign GetZodiacSign(DateTime birthday)
    {
        int month = birthday.Month;
        int day = birthday.Day;
        
        if ((month == 1 && day >= 20) || (month == 2 && day <= 18))
            return DuckZodiacSign.Mallard;
        if ((month == 2 && day >= 19) || (month == 3 && day <= 20))
            return DuckZodiacSign.Pekin;
        if ((month == 3 && day >= 21) || (month == 4 && day <= 19))
            return DuckZodiacSign.Muscovy;
        if ((month == 4 && day >= 20) || (month == 5 && day <= 20))
            return DuckZodiacSign.Runner;
        if ((month == 5 && day >= 21) || (month == 6 && day <= 20))
            return DuckZodiacSign.Cayuga;
        if ((month == 6 && day >= 21) || (month == 7 && day <= 22))
            return DuckZodiacSign.Rouen;
        if ((month == 7 && day >= 23) || (month == 8 && day <= 22))
            return DuckZodiacSign.KhakiCampbell;
        if ((month == 8 && day >= 23) || (month == 9 && day <= 22))
            return DuckZodiacSign.Swedish;
        if ((month == 9 && day >= 23) || (month == 10 && day <= 22))
            return DuckZodiacSign.Buff;
        if ((month == 10 && day >= 23) || (month == 11 && day <= 21))
            return DuckZodiacSign.Magpie;
        if ((month == 11 && day >= 22) || (month == 12 && day <= 21))
            return DuckZodiacSign.Call;
        
        return DuckZodiacSign.WelshHarlequin;
    }
    
    /// <summary>
    /// Get the duck's zodiac information.
    /// </summary>
    public ZodiacInfo? GetZodiacInfo()
    {
        return ZodiacSign.HasValue ? ZodiacInfoMap.GetValueOrDefault(ZodiacSign.Value) : null;
    }
    
    /// <summary>
    /// Generate a deterministic seed for daily fortune based on date and sign.
    /// </summary>
    private static int GenerateDailySeed(DateTime date, DuckZodiacSign sign)
    {
        string seedString = $"{date:yyyy-MM-dd}-{sign}";
        using var md5 = MD5.Create();
        byte[] hash = md5.ComputeHash(Encoding.UTF8.GetBytes(seedString));
        return BitConverter.ToInt32(hash, 0);
    }
    
    /// <summary>
    /// Generate a daily horoscope for the duck.
    /// </summary>
    public DailyHoroscope? GenerateDailyHoroscope(DateTime? forDate = null)
    {
        if (!ZodiacSign.HasValue) return null;
        
        DateTime targetDate = forDate ?? DateTime.Today;
        int seed = GenerateDailySeed(targetDate, ZodiacSign.Value);
        var rng = new Random(seed);
        
        var zodiacInfo = ZodiacInfoMap[ZodiacSign.Value];
        
        // Determine fortune level (1-5 stars)
        double[] fortuneWeights = { 0.1, 0.2, 0.3, 0.25, 0.15 };
        double roll = rng.NextDouble();
        double cumulative = 0;
        int fortuneLevel = 1;
        for (int i = 0; i < fortuneWeights.Length; i++)
        {
            cumulative += fortuneWeights[i];
            if (roll < cumulative)
            {
                fortuneLevel = i + 1;
                break;
            }
        }
        
        // Generate horoscope content
        string generalFortune = HoroscopeTemplates[fortuneLevel][rng.Next(HoroscopeTemplates[fortuneLevel].Count)];
        string luckyItem = zodiacInfo.LuckyItems[rng.Next(zodiacInfo.LuckyItems.Count)];
        string luckyColor = zodiacInfo.LuckyColors[rng.Next(zodiacInfo.LuckyColors.Count)];
        int luckyNumber = zodiacInfo.LuckyNumbers[rng.Next(zodiacInfo.LuckyNumbers.Count)];
        string moodPrediction = MoodPredictions[rng.Next(MoodPredictions.Count)];
        string activitySuggestion = ActivitySuggestions[rng.Next(ActivitySuggestions.Count)];
        
        // Special message on certain days
        string? specialMessage = null;
        int dayOfYear = targetDate.DayOfYear;
        
        if (DuckBirthday.HasValue && 
            targetDate.Month == DuckBirthday.Value.Month && 
            targetDate.Day == DuckBirthday.Value.Day)
        {
            specialMessage = "🎂 HAPPY BIRTHDAY! The stars shower you with extra blessings today! 🎂";
            fortuneLevel = 5;
        }
        else if (dayOfYear % 7 == 0)
        {
            specialMessage = "✨ Weekly fortune boost! Something special may happen! ✨";
        }
        else if (fortuneLevel == 5)
        {
            specialMessage = "🌟 A truly LEGENDARY day! Make it count! 🌟";
        }
        
        var horoscope = new DailyHoroscope
        {
            Date = targetDate.ToString("yyyy-MM-dd"),
            Sign = ZodiacSign.Value,
            GeneralFortune = generalFortune,
            LuckyItem = luckyItem,
            LuckyColor = luckyColor,
            LuckyNumber = luckyNumber,
            MoodPrediction = moodPrediction,
            ActivitySuggestion = activitySuggestion,
            FortuneLevel = fortuneLevel,
            SpecialMessage = specialMessage
        };
        
        LastHoroscopeDate = targetDate;
        
        // Track luck streak
        if (fortuneLevel >= 4)
            DailyLuckStreak++;
        else
            DailyLuckStreak = 0;
        
        return horoscope;
    }
    
    /// <summary>
    /// Open a fortune cookie and get a message.
    /// </summary>
    public FortuneCookie GetFortuneCookie()
    {
        // Determine rarity
        double rarityRoll = _random.NextDouble();
        FortuneRarity rarity;
        
        if (rarityRoll < 0.02)
        {
            rarity = FortuneRarity.Legendary;
            RareCookiesFound++;
        }
        else if (rarityRoll < 0.12)
        {
            rarity = FortuneRarity.Rare;
            RareCookiesFound++;
        }
        else if (rarityRoll < 0.37)
        {
            rarity = FortuneRarity.Uncommon;
        }
        else
        {
            rarity = FortuneRarity.Common;
        }
        
        // Pick random category
        var categories = Enum.GetValues<FortuneCategory>();
        var category = categories[_random.Next(categories.Length)];
        
        // Get message
        var messages = FortuneMessages[category][rarity];
        string message = messages[_random.Next(messages.Count)];
        
        // Generate lucky numbers
        var luckyNumbers = Enumerable.Range(1, 49)
            .OrderBy(_ => _random.Next())
            .Take(3)
            .OrderBy(n => n)
            .ToList();
        
        var cookie = new FortuneCookie
        {
            CookieId = $"cookie_{TotalCookiesOpened + 1}",
            Message = message,
            Category = category,
            Rarity = rarity,
            LuckyNumbers = luckyNumbers,
            DateReceived = DateTime.Now.ToString("o"),
            IsRevealed = true
        };
        
        FortuneCookies.Add(cookie);
        TotalCookiesOpened++;
        
        // Keep cookie list manageable
        if (FortuneCookies.Count > 100)
            FortuneCookies = FortuneCookies.Skip(FortuneCookies.Count - 100).ToList();
        
        return cookie;
    }
    
    /// <summary>
    /// Add a fortune to favorites.
    /// </summary>
    public void AddFavoriteFortune(string cookieId)
    {
        if (!FavoriteFortunes.Contains(cookieId))
            FavoriteFortunes.Add(cookieId);
    }
    
    /// <summary>
    /// Remove a fortune from favorites.
    /// </summary>
    public void RemoveFavoriteFortune(string cookieId)
    {
        FavoriteFortunes.Remove(cookieId);
    }
    
    /// <summary>
    /// Check compatibility with another zodiac sign.
    /// </summary>
    public (int compatibility, string message) GetCompatibility(DuckZodiacSign otherSign)
    {
        if (!ZodiacSign.HasValue)
            return (0, "Unknown");
        
        var myInfo = ZodiacInfoMap[ZodiacSign.Value];
        
        if (myInfo.CompatibleSigns.Contains(otherSign))
            return (100, "Perfect Match! 💕");
        
        var otherInfo = ZodiacInfoMap[otherSign];
        if (myInfo.Element == otherInfo.Element)
            return (75, "Great compatibility! 🌟");
        
        var compatibleElements = new Dictionary<string, List<string>>
        {
            ["Fire"] = new List<string> { "Air" },
            ["Air"] = new List<string> { "Fire" },
            ["Water"] = new List<string> { "Earth" },
            ["Earth"] = new List<string> { "Water" }
        };
        
        if (compatibleElements.TryGetValue(myInfo.Element, out var compatible) && 
            compatible.Contains(otherInfo.Element))
            return (60, "Good potential! ✨");
        
        return (40, "Challenging but possible 🤔");
    }
    
    /// <summary>
    /// Get today's horoscope-based bonuses.
    /// </summary>
    public Dictionary<string, double> GetDailyBonus()
    {
        if (!ZodiacSign.HasValue)
            return new Dictionary<string, double>();
        
        var todayHoroscope = GenerateDailyHoroscope();
        if (todayHoroscope == null)
            return new Dictionary<string, double>();
        
        int fortuneLevel = todayHoroscope.FortuneLevel;
        
        var bonuses = new Dictionary<string, double>
        {
            ["luck_multiplier"] = 0.8 + (fortuneLevel * 0.1),
            ["coin_bonus"] = (fortuneLevel - 3) * 0.05,
            ["xp_bonus"] = (fortuneLevel - 3) * 0.05,
            ["find_chance_bonus"] = (fortuneLevel - 3) * 0.02
        };
        
        // Streak bonus
        if (DailyLuckStreak >= 3)
            bonuses["luck_multiplier"] += 0.05;
        if (DailyLuckStreak >= 7)
            bonuses["coin_bonus"] += 0.05;
        
        return bonuses;
    }
    
    /// <summary>
    /// Render the zodiac sign information display.
    /// </summary>
    public List<string> RenderZodiacDisplay(int width = 60)
    {
        var lines = new List<string>();
        
        if (!ZodiacSign.HasValue)
        {
            lines.Add("╔" + new string('═', width - 2) + "╗");
            lines.Add("║" + " No birthday set! ".PadLeft((width + 16) / 2).PadRight(width - 2) + "║");
            lines.Add("╚" + new string('═', width - 2) + "╝");
            return lines;
        }
        
        var info = ZodiacInfoMap[ZodiacSign.Value];
        
        lines.Add("╔" + new string('═', width - 2) + "╗");
        lines.Add("║" + $" {info.Symbol} {info.Name} {info.Symbol} ".PadLeft((width + info.Name.Length + 6) / 2).PadRight(width - 2) + "║");
        lines.Add("║" + $" Element: {info.Element} ".PadLeft((width + 10 + info.Element.Length) / 2).PadRight(width - 2) + "║");
        lines.Add("╠" + new string('═', width - 2) + "╣");
        
        lines.Add("║" + " Traits: ".PadRight(width - 2) + "║");
        string traitsStr = string.Join(", ", info.Traits);
        lines.Add("║" + $"  {traitsStr}".PadRight(width - 2).Substring(0, width - 2) + "║");
        
        lines.Add("╠" + new string('─', width - 2) + "╣");
        
        lines.Add("║" + " Lucky Items: ".PadRight(width - 2) + "║");
        foreach (var item in info.LuckyItems)
        {
            lines.Add("║" + $"  • {item}".PadRight(width - 2).Substring(0, width - 2) + "║");
        }
        
        lines.Add("╠" + new string('─', width - 2) + "╣");
        
        string colorsStr = string.Join(", ", info.LuckyColors);
        lines.Add("║" + $" Lucky Colors: {colorsStr}".PadRight(width - 2).Substring(0, width - 2) + "║");
        
        string numbersStr = string.Join(", ", info.LuckyNumbers);
        lines.Add("║" + $" Lucky Numbers: {numbersStr}".PadRight(width - 2).Substring(0, width - 2) + "║");
        
        lines.Add("╠" + new string('─', width - 2) + "╣");
        
        lines.Add("║" + " Compatible Signs: ".PadRight(width - 2) + "║");
        foreach (var sign in info.CompatibleSigns)
        {
            var compatInfo = ZodiacInfoMap[sign];
            lines.Add("║" + $"  {compatInfo.Symbol} {compatInfo.Name}".PadRight(width - 2).Substring(0, width - 2) + "║");
        }
        
        lines.Add("╠" + new string('─', width - 2) + "╣");
        
        // Wrap description
        string desc = info.Description;
        while (desc.Length > 0)
        {
            int takeLen = Math.Min(width - 4, desc.Length);
            lines.Add("║ " + desc.Substring(0, takeLen).PadRight(width - 3) + "║");
            desc = desc.Length > takeLen ? desc.Substring(takeLen) : "";
        }
        
        lines.Add("╚" + new string('═', width - 2) + "╝");
        
        return lines;
    }
    
    /// <summary>
    /// Render a daily horoscope display.
    /// </summary>
    public List<string> RenderHoroscopeDisplay(DailyHoroscope horoscope, int width = 60)
    {
        var lines = new List<string>();
        var info = ZodiacInfoMap[horoscope.Sign];
        string stars = new string('⭐', horoscope.FortuneLevel) + new string('☆', 5 - horoscope.FortuneLevel);
        
        lines.Add("╔" + new string('═', width - 2) + "╗");
        lines.Add("║" + $" {info.Symbol} Daily Horoscope {info.Symbol} ".PadLeft((width + 20) / 2).PadRight(width - 2) + "║");
        lines.Add("║" + $" {horoscope.Date} ".PadLeft((width + horoscope.Date.Length + 2) / 2).PadRight(width - 2) + "║");
        lines.Add("╠" + new string('═', width - 2) + "╣");
        
        lines.Add("║" + $" Fortune: {stars} ".PadLeft((width + 12 + stars.Length) / 2).PadRight(width - 2) + "║");
        
        if (!string.IsNullOrEmpty(horoscope.SpecialMessage))
        {
            lines.Add("╠" + new string('─', width - 2) + "╣");
            lines.Add("║" + horoscope.SpecialMessage.PadLeft((width + horoscope.SpecialMessage.Length) / 2).PadRight(width - 2).Substring(0, width - 2) + "║");
        }
        
        lines.Add("╠" + new string('─', width - 2) + "╣");
        
        // Wrap general fortune
        string fortune = horoscope.GeneralFortune;
        while (fortune.Length > 0)
        {
            int takeLen = Math.Min(width - 4, fortune.Length);
            lines.Add("║ " + fortune.Substring(0, takeLen).PadRight(width - 3) + "║");
            fortune = fortune.Length > takeLen ? fortune.Substring(takeLen) : "";
        }
        
        lines.Add("╠" + new string('─', width - 2) + "╣");
        
        lines.Add("║" + $" 🎨 Lucky Color: {horoscope.LuckyColor}".PadRight(width - 2).Substring(0, width - 2) + "║");
        lines.Add("║" + $" 🎁 Lucky Item: {horoscope.LuckyItem}".PadRight(width - 2).Substring(0, width - 2) + "║");
        lines.Add("║" + $" 🔢 Lucky Number: {horoscope.LuckyNumber}".PadRight(width - 2).Substring(0, width - 2) + "║");
        
        lines.Add("╠" + new string('─', width - 2) + "╣");
        
        lines.Add("║" + $" Mood: {horoscope.MoodPrediction}".PadRight(width - 2).Substring(0, width - 2) + "║");
        lines.Add("║" + $" Suggestion: {horoscope.ActivitySuggestion}".PadRight(width - 2).Substring(0, width - 2) + "║");
        
        lines.Add("╚" + new string('═', width - 2) + "╝");
        
        return lines;
    }
    
    /// <summary>
    /// Render a fortune cookie display.
    /// </summary>
    public List<string> RenderFortuneCookieDisplay(FortuneCookie cookie, int width = 50)
    {
        var lines = new List<string>();
        
        var raritySymbols = new Dictionary<FortuneRarity, string>
        {
            [FortuneRarity.Common] = "🥠",
            [FortuneRarity.Uncommon] = "🥠✨",
            [FortuneRarity.Rare] = "🥠🌟",
            [FortuneRarity.Legendary] = "🥠👑"
        };
        
        string rarityStr = raritySymbols.GetValueOrDefault(cookie.Rarity, "🥠");
        
        lines.Add("╔" + new string('═', width - 2) + "╗");
        lines.Add("║" + $" {rarityStr} Fortune Cookie {rarityStr} ".PadLeft((width + 20) / 2).PadRight(width - 2) + "║");
        lines.Add("║" + $" [{cookie.Rarity.ToString().ToUpper()}] ".PadLeft((width + cookie.Rarity.ToString().Length + 4) / 2).PadRight(width - 2) + "║");
        lines.Add("╠" + new string('═', width - 2) + "╣");
        
        // Wrap message
        string message = cookie.Message;
        while (message.Length > 0)
        {
            int takeLen = Math.Min(width - 4, message.Length);
            lines.Add("║ " + message.Substring(0, takeLen).PadRight(width - 3) + "║");
            message = message.Length > takeLen ? message.Substring(takeLen) : "";
        }
        
        lines.Add("╠" + new string('─', width - 2) + "╣");
        
        string numbersStr = string.Join(" - ", cookie.LuckyNumbers);
        lines.Add("║" + $" Lucky Numbers: {numbersStr} ".PadLeft((width + 18 + numbersStr.Length) / 2).PadRight(width - 2) + "║");
        
        lines.Add("╚" + new string('═', width - 2) + "╝");
        
        return lines;
    }
    
    /// <summary>
    /// Convert to save data.
    /// </summary>
    public Dictionary<string, object?> ToSaveData()
    {
        return new Dictionary<string, object?>
        {
            ["duck_birthday"] = DuckBirthday?.ToString("yyyy-MM-dd"),
            ["zodiac_sign"] = ZodiacSign?.ToString(),
            ["last_horoscope_date"] = LastHoroscopeDate?.ToString("yyyy-MM-dd"),
            ["fortune_cookies"] = FortuneCookies.TakeLast(50).Select(c => new Dictionary<string, object?>
            {
                ["cookie_id"] = c.CookieId,
                ["message"] = c.Message,
                ["category"] = c.Category.ToString(),
                ["rarity"] = c.Rarity.ToString(),
                ["lucky_numbers"] = c.LuckyNumbers,
                ["date_received"] = c.DateReceived,
                ["is_revealed"] = c.IsRevealed
            }).ToList(),
            ["favorite_fortunes"] = FavoriteFortunes,
            ["daily_luck_streak"] = DailyLuckStreak,
            ["total_cookies_opened"] = TotalCookiesOpened,
            ["rare_cookies_found"] = RareCookiesFound,
            ["lucky_events_triggered"] = LuckyEventsTriggered
        };
    }
    
    /// <summary>
    /// Load from save data.
    /// </summary>
    public static FortuneSystem FromSaveData(Dictionary<string, JsonElement> data)
    {
        var system = new FortuneSystem();
        
        if (data.TryGetValue("duck_birthday", out var birthdayEl) && birthdayEl.ValueKind == JsonValueKind.String)
        {
            if (DateTime.TryParse(birthdayEl.GetString(), out var birthday))
                system.DuckBirthday = birthday;
        }
        
        if (data.TryGetValue("zodiac_sign", out var signEl) && signEl.ValueKind == JsonValueKind.String)
        {
            if (Enum.TryParse<DuckZodiacSign>(signEl.GetString(), out var sign))
                system.ZodiacSign = sign;
        }
        
        if (data.TryGetValue("last_horoscope_date", out var lastDateEl) && lastDateEl.ValueKind == JsonValueKind.String)
        {
            if (DateTime.TryParse(lastDateEl.GetString(), out var lastDate))
                system.LastHoroscopeDate = lastDate;
        }
        
        if (data.TryGetValue("fortune_cookies", out var cookiesEl) && cookiesEl.ValueKind == JsonValueKind.Array)
        {
            foreach (var cEl in cookiesEl.EnumerateArray())
            {
                var cookie = new FortuneCookie
                {
                    CookieId = cEl.TryGetProperty("cookie_id", out var cidEl) ? cidEl.GetString() ?? "" : "",
                    Message = cEl.TryGetProperty("message", out var msgEl) ? msgEl.GetString() ?? "" : "",
                    DateReceived = cEl.TryGetProperty("date_received", out var drEl) ? drEl.GetString() ?? "" : "",
                    IsRevealed = cEl.TryGetProperty("is_revealed", out var revEl) && revEl.GetBoolean()
                };
                
                if (cEl.TryGetProperty("category", out var catEl) && Enum.TryParse<FortuneCategory>(catEl.GetString(), out var cat))
                    cookie.Category = cat;
                if (cEl.TryGetProperty("rarity", out var rarEl) && Enum.TryParse<FortuneRarity>(rarEl.GetString(), out var rar))
                    cookie.Rarity = rar;
                if (cEl.TryGetProperty("lucky_numbers", out var lnEl) && lnEl.ValueKind == JsonValueKind.Array)
                    cookie.LuckyNumbers = lnEl.EnumerateArray().Select(n => n.GetInt32()).ToList();
                
                system.FortuneCookies.Add(cookie);
            }
        }
        
        if (data.TryGetValue("favorite_fortunes", out var favEl) && favEl.ValueKind == JsonValueKind.Array)
            system.FavoriteFortunes = favEl.EnumerateArray().Select(f => f.GetString() ?? "").ToList();
        
        if (data.TryGetValue("daily_luck_streak", out var streakEl))
            system.DailyLuckStreak = streakEl.GetInt32();
        if (data.TryGetValue("total_cookies_opened", out var totalEl))
            system.TotalCookiesOpened = totalEl.GetInt32();
        if (data.TryGetValue("rare_cookies_found", out var rareEl))
            system.RareCookiesFound = rareEl.GetInt32();
        if (data.TryGetValue("lucky_events_triggered", out var luckyEl))
            system.LuckyEventsTriggered = luckyEl.GetInt32();
        
        return system;
    }
}
