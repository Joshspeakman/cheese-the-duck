using StupidDuck.Core;
using StupidDuck.World;
using DuckEntity = StupidDuck.Duck.Duck;

namespace StupidDuck.Game;

/// <summary>
/// Holds all game state and systems.
/// </summary>
public class GameState
{
    public DuckEntity? Duck { get; set; }
    public GameClock Clock { get; } = new();
    public AtmosphereManager Weather { get; } = new();
    public FriendsManager Friends { get; } = new();
    public HabitatDecorations Decorations { get; } = new();
    public EventSystem Events { get; } = new();
    
    // Currency and stats
    public int Coins { get; set; } = 100;
    public TimeSpan TotalPlaytime { get; set; } = TimeSpan.Zero;
    public string CurrentLocation { get; set; } = "Home Pond";
    public string CurrentActivity { get; set; } = "Just vibing...";
    
    // Session tracking
    private DateTime _sessionStart = DateTime.Now;
    
    public void UpdatePlaytime()
    {
        TotalPlaytime += DateTime.Now - _sessionStart;
        _sessionStart = DateTime.Now;
    }
    
    public string GetPlaytimeDisplay()
    {
        var hours = (int)TotalPlaytime.TotalHours;
        return $"{hours}h";
    }

    public void AddCoins(int amount)
    {
        Coins = Math.Max(0, Coins + amount);
    }

    public bool SpendCoins(int amount)
    {
        if (Coins >= amount)
        {
            Coins -= amount;
            return true;
        }
        return false;
    }
}
