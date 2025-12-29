namespace StupidDuck.World;

/// <summary>
/// Random event types.
/// </summary>
public enum EventType
{
    Visitor,
    Weather,
    Gift,
    Discovery,
    Achievement,
    Special
}

/// <summary>
/// A game event.
/// </summary>
public record GameEvent(
    string Id,
    string Title,
    string Description,
    EventType Type,
    Dictionary<string, float>? Effects = null,
    string? RewardItem = null
);

/// <summary>
/// Manages random events in the game.
/// </summary>
public class EventSystem
{
    private static readonly Random Rng = new();
    private readonly List<GameEvent> _eventHistory = new();
    private DateTime _lastEventCheck = DateTime.Now;
    private const float EventCheckInterval = 60f; // Check every minute

    public static readonly Dictionary<string, GameEvent> Events = new()
    {
        // Random positive events
        ["butterfly_visit"] = new GameEvent(
            "butterfly_visit", "Butterfly Visit",
            "A colorful butterfly lands nearby! Your duck watches in wonder.",
            EventType.Visitor, Effects: new() { ["fun"] = 5 }),
        ["find_worm"] = new GameEvent(
            "find_worm", "Found a Worm!",
            "Your duck found a tasty worm while exploring!",
            EventType.Discovery, Effects: new() { ["hunger"] = 10 }),
        ["found_crumb"] = new GameEvent(
            "found_crumb", "Lucky Crumb",
            "A delicious bread crumb appeared out of nowhere!",
            EventType.Discovery, Effects: new() { ["hunger"] = 5 }),
        ["nice_breeze"] = new GameEvent(
            "nice_breeze", "Nice Breeze",
            "A gentle breeze ruffles your duck's feathers. Ahh...",
            EventType.Weather, Effects: new() { ["fun"] = 3 }),
        ["found_shiny"] = new GameEvent(
            "found_shiny", "Shiny Discovery",
            "Your duck found something shiny in the pond!",
            EventType.Discovery, RewardItem: "golden_feather"),
        
        // Neutral events
        ["random_quack"] = new GameEvent(
            "random_quack", "Random Quack",
            "Your duck suddenly quacks for no apparent reason. Quack!",
            EventType.Special),
        ["forgot_something"] = new GameEvent(
            "forgot_something", "Hmm...",
            "Your duck looks confused for a moment, then shrugs it off.",
            EventType.Special),
        ["stare_contest"] = new GameEvent(
            "stare_contest", "Stare Contest",
            "Your duck engages in a staring contest with a frog. It's intense.",
            EventType.Visitor, Effects: new() { ["fun"] = 2 }),
        
        // Weather events
        ["rain_shower"] = new GameEvent(
            "rain_shower", "Rain Shower",
            "A light rain begins to fall. Your duck splashes happily!",
            EventType.Weather, Effects: new() { ["fun"] = 8, ["cleanliness"] = 5 }),
        ["rainbow"] = new GameEvent(
            "rainbow", "Rainbow!",
            "A beautiful rainbow appears across the sky!",
            EventType.Weather, Effects: new() { ["fun"] = 10 }),
        ["golden_hour"] = new GameEvent(
            "golden_hour", "Golden Hour",
            "The sunset paints everything in warm golden light.",
            EventType.Weather, Effects: new() { ["fun"] = 5 }),
        
        // Visitor events
        ["friend_visit"] = new GameEvent(
            "friend_visit", "Friend Visit",
            "Another duck waddles by to say hello!",
            EventType.Visitor, Effects: new() { ["social"] = 15 }),
        ["bird_friend"] = new GameEvent(
            "bird_friend", "Bird Friend",
            "A friendly sparrow chirps a greeting!",
            EventType.Visitor, Effects: new() { ["social"] = 8 }),
        ["frog_friend"] = new GameEvent(
            "frog_friend", "Frog Friend",
            "A frog croaks a tune from a lily pad.",
            EventType.Visitor, Effects: new() { ["social"] = 5, ["fun"] = 3 }),
        
        // Negative events
        ["loud_noise"] = new GameEvent(
            "loud_noise", "Loud Noise!",
            "A sudden loud noise startles your duck!",
            EventType.Special, Effects: new() { ["fun"] = -5 }),
        ["stubbed_toe"] = new GameEvent(
            "stubbed_toe", "Ouch!",
            "Your duck stubbed its webbed foot on a rock.",
            EventType.Special, Effects: new() { ["fun"] = -3 }),
        ["bad_dream"] = new GameEvent(
            "bad_dream", "Bad Dream",
            "Your duck woke up from a weird dream about being a chicken.",
            EventType.Special, Effects: new() { ["energy"] = -2 }),
        
        // Special day events
        ["lazy_sunday"] = new GameEvent(
            "lazy_sunday", "Lazy Sunday",
            "It's Sunday! Everything feels more relaxed.",
            EventType.Special, Effects: new() { ["energy"] = 10 }),
        ["monday_blues"] = new GameEvent(
            "monday_blues", "Monday Blues",
            "It's Monday... even ducks feel it.",
            EventType.Special, Effects: new() { ["fun"] = -2 }),
        ["friday_vibes"] = new GameEvent(
            "friday_vibes", "Friday Vibes!",
            "TGIF! Weekend energy is building!",
            EventType.Special, Effects: new() { ["fun"] = 8 })
    };

    public GameEvent? CheckForEvent()
    {
        var now = DateTime.Now;
        if ((now - _lastEventCheck).TotalSeconds < EventCheckInterval)
            return null;

        _lastEventCheck = now;

        // 10% chance for an event each check
        if (Rng.NextDouble() > 0.1)
            return null;

        var events = Events.Values.ToList();
        var evt = events[Rng.Next(events.Count)];
        _eventHistory.Add(evt);
        return evt;
    }

    public List<GameEvent> GetRecentEvents(int count = 5) =>
        _eventHistory.TakeLast(count).Reverse().ToList();
}
