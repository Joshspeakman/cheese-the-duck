namespace StupidDuck.World;

/// <summary>
/// Weather types in the game.
/// </summary>
public enum WeatherType
{
    Sunny,
    Cloudy,
    Rainy,
    Stormy,
    Foggy,
    Snowy,
    Windy,
    Hot,
    Cold
}

/// <summary>
/// Manages weather and atmosphere in the game.
/// </summary>
public class AtmosphereManager
{
    private static readonly Random Rng = new();
    
    public WeatherType CurrentWeather { get; private set; } = WeatherType.Sunny;
    public float Temperature { get; private set; } = 20f;
    public string Season { get; private set; } = "spring";

    public AtmosphereManager()
    {
        UpdateSeason();
        UpdateWeather();
    }

    public void Update()
    {
        // Occasionally change weather
        if (Rng.NextDouble() < 0.01)
        {
            UpdateWeather();
        }
    }

    private void UpdateSeason()
    {
        var month = DateTime.Now.Month;
        Season = month switch
        {
            >= 3 and <= 5 => "spring",
            >= 6 and <= 8 => "summer",
            >= 9 and <= 11 => "autumn",
            _ => "winter"
        };
    }

    private void UpdateWeather()
    {
        var weights = Season switch
        {
            "spring" => new[] { 0.3f, 0.25f, 0.25f, 0.05f, 0.1f, 0.0f, 0.05f },
            "summer" => new[] { 0.5f, 0.2f, 0.1f, 0.1f, 0.05f, 0.0f, 0.05f },
            "autumn" => new[] { 0.2f, 0.3f, 0.25f, 0.1f, 0.1f, 0.0f, 0.05f },
            "winter" => new[] { 0.2f, 0.25f, 0.15f, 0.1f, 0.1f, 0.15f, 0.05f },
            _ => new[] { 0.4f, 0.2f, 0.15f, 0.1f, 0.1f, 0.0f, 0.05f }
        };

        var roll = (float)Rng.NextDouble();
        var cumulative = 0f;
        var weathers = Enum.GetValues<WeatherType>();

        for (var i = 0; i < weights.Length; i++)
        {
            cumulative += weights[i];
            if (roll <= cumulative)
            {
                CurrentWeather = weathers[i];
                break;
            }
        }

        UpdateTemperature();
    }

    private void UpdateTemperature()
    {
        var baseTemp = Season switch
        {
            "spring" => 15f,
            "summer" => 25f,
            "autumn" => 12f,
            "winter" => 3f,
            _ => 18f
        };

        var weatherMod = CurrentWeather switch
        {
            WeatherType.Sunny => 5f,
            WeatherType.Stormy => -3f,
            WeatherType.Snowy => -8f,
            WeatherType.Rainy => -2f,
            _ => 0f
        };

        Temperature = baseTemp + weatherMod + (float)(Rng.NextDouble() * 6 - 3);
    }

    public string GetWeatherDescription() => CurrentWeather switch
    {
        WeatherType.Sunny => "The sun is shining brightly!",
        WeatherType.Cloudy => "Clouds drift lazily overhead.",
        WeatherType.Rainy => "Gentle rain patters on the pond.",
        WeatherType.Stormy => "Thunder rumbles in the distance!",
        WeatherType.Foggy => "A mysterious fog blankets the area.",
        WeatherType.Snowy => "Snowflakes fall softly from the sky.",
        WeatherType.Windy => "A brisk wind rustles the reeds.",
        _ => "Pleasant weather today."
    };

    public string GetWeatherEmoji() => CurrentWeather switch
    {
        WeatherType.Sunny => "☀️",
        WeatherType.Cloudy => "☁️",
        WeatherType.Rainy => "🌧️",
        WeatherType.Stormy => "⛈️",
        WeatherType.Foggy => "🌫️",
        WeatherType.Snowy => "❄️",
        WeatherType.Windy => "💨",
        WeatherType.Hot => "🔥",
        WeatherType.Cold => "🥶",
        _ => "🌤️"
    };

    /// <summary>
    /// Get weather icon (single char for compact display).
    /// </summary>
    public string GetWeatherIcon() => CurrentWeather switch
    {
        WeatherType.Sunny => "☀",
        WeatherType.Cloudy => "☁",
        WeatherType.Rainy => "🌧",
        WeatherType.Stormy => "⛈",
        WeatherType.Foggy => "≈",
        WeatherType.Snowy => "❄",
        WeatherType.Windy => "~",
        WeatherType.Hot => "♨",
        WeatherType.Cold => "❆",
        _ => "☀"
    };

    /// <summary>
    /// Get particle characters for weather effects.
    /// </summary>
    public char[] GetParticles() => CurrentWeather switch
    {
        WeatherType.Rainy => new[] { '\'', '.', ',' },
        WeatherType.Stormy => new[] { '\'', '/', '\\', '|' },
        WeatherType.Snowy => new[] { '*', '·', '°', '.' },
        WeatherType.Foggy => new[] { '~', '-', '=' },
        WeatherType.Windy => new[] { '~', '-', '>' },
        _ => Array.Empty<char>()
    };
}
