namespace StupidDuck.Data;

/// <summary>
/// Static data and constants shared across the game.
/// </summary>
public static class GameData
{
    /// <summary>
    /// Random duck facts.
    /// </summary>
    public static readonly string[] DuckFacts = new[]
    {
        "Ducks have waterproof feathers!",
        "A group of ducks is called a 'paddling'.",
        "Ducks can sleep with one eye open.",
        "Ducklings can swim within 24 hours of hatching.",
        "Ducks have three eyelids.",
        "A duck's quack doesn't echo (myth or fact? Scientists debate!)",
        "Ducks have been domesticated for over 4,000 years.",
        "Male ducks are called drakes, females are hens.",
        "Ducks can fly up to 50 mph!",
        "Ducks' feet have no nerves or blood vessels, so they don't feel cold.",
        "Some ducks can dive up to 6 feet deep.",
        "Ducks are omnivores and eat plants, insects, and small fish.",
        "Baby ducks imprint on the first thing they see.",
        "Ducks preen for hours to spread oil on their feathers.",
        "Wild ducks can live 5-10 years, domestic ducks up to 20."
    };

    /// <summary>
    /// Seasonal messages.
    /// </summary>
    public static readonly Dictionary<string, string[]> SeasonalMessages = new()
    {
        ["spring"] = new[]
        {
            "Flowers are blooming around the pond!",
            "The weather is getting warmer.",
            "Spring showers keep the pond nice and full.",
            "Butterflies are visiting the garden!"
        },
        ["summer"] = new[]
        {
            "It's a beautiful sunny day!",
            "Perfect weather for swimming.",
            "The pond is warm and lovely.",
            "Fireflies dance at dusk."
        },
        ["autumn"] = new[]
        {
            "Leaves are changing colors.",
            "A cool breeze rustles the reeds.",
            "The harvest moon rises over the pond.",
            "Acorns drop from nearby trees."
        },
        ["winter"] = new[]
        {
            "Frost sparkles on the grass.",
            "Time to stay warm and cozy!",
            "The pond might freeze over soon.",
            "Snowflakes drift down gently."
        }
    };

    /// <summary>
    /// Time of day greetings.
    /// </summary>
    public static readonly Dictionary<string, string[]> TimeGreetings = new()
    {
        ["morning"] = new[] { "Good morning!", "Rise and shine!", "A new day begins!" },
        ["afternoon"] = new[] { "Good afternoon!", "Having a good day?", "Afternoon stretches!" },
        ["evening"] = new[] { "Good evening!", "The sun is setting.", "Winding down..." },
        ["night"] = new[] { "It's getting late.", "Stars are twinkling.", "Time for dreams." }
    };

    /// <summary>
    /// Get a random duck fact.
    /// </summary>
    public static string GetRandomFact()
    {
        var rng = new Random();
        return DuckFacts[rng.Next(DuckFacts.Length)];
    }

    /// <summary>
    /// Get a seasonal message.
    /// </summary>
    public static string GetSeasonalMessage(string season)
    {
        var rng = new Random();
        if (SeasonalMessages.TryGetValue(season, out var messages))
            return messages[rng.Next(messages.Length)];
        return "The weather is pleasant.";
    }

    /// <summary>
    /// Get a time-based greeting.
    /// </summary>
    public static string GetTimeGreeting(string timeOfDay)
    {
        var rng = new Random();
        if (TimeGreetings.TryGetValue(timeOfDay, out var greetings))
            return greetings[rng.Next(greetings.Length)];
        return "Hello!";
    }
}
