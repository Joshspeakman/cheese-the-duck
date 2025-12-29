namespace StupidDuck.World;

/// <summary>
/// Friendship levels with visitors.
/// </summary>
public enum FriendshipLevel
{
    Stranger,
    Acquaintance,
    Friend,
    CloseFriend,
    BestFriend
}

/// <summary>
/// Visitor personality types.
/// </summary>
public enum VisitorPersonality
{
    Adventurous,
    Scholarly,
    Artistic,
    Playful,
    Mysterious,
    Generous,
    Foodie,
    Athletic
}

/// <summary>
/// A friend duck that can visit.
/// </summary>
public class Friend
{
    private static readonly Random Rng = new();

    public string Id { get; init; } = Guid.NewGuid().ToString()[..8];
    public string Name { get; init; } = "Duck";
    public VisitorPersonality Personality { get; init; }
    public int FriendshipPoints { get; private set; }
    public int VisitCount { get; private set; }
    public DateTime FirstMet { get; init; } = DateTime.Now;
    public DateTime? LastVisit { get; private set; }
    public string Color { get; init; } = "yellow";
    public string Accessory { get; init; } = "";

    public FriendshipLevel Level => FriendshipPoints switch
    {
        >= 600 => FriendshipLevel.BestFriend,
        >= 350 => FriendshipLevel.CloseFriend,
        >= 150 => FriendshipLevel.Friend,
        >= 50 => FriendshipLevel.Acquaintance,
        _ => FriendshipLevel.Stranger
    };

    // Personality-based visual traits
    private static readonly Dictionary<VisitorPersonality, (string color, string accessory)> PersonalityTraits = new()
    {
        [VisitorPersonality.Adventurous] = ("green", "🎒"),
        [VisitorPersonality.Scholarly] = ("blue", "📚"),
        [VisitorPersonality.Artistic] = ("magenta", "🎨"),
        [VisitorPersonality.Playful] = ("yellow", "🎈"),
        [VisitorPersonality.Mysterious] = ("purple", "🔮"),
        [VisitorPersonality.Generous] = ("gold", "🎁"),
        [VisitorPersonality.Foodie] = ("orange", "🍕"),
        [VisitorPersonality.Athletic] = ("red", "⚽")
    };

    // Names per personality
    private static readonly Dictionary<VisitorPersonality, string[]> Names = new()
    {
        [VisitorPersonality.Adventurous] = new[] { "Scout", "Trek", "Journey", "Blaze", "Ranger" },
        [VisitorPersonality.Scholarly] = new[] { "Sage", "Newton", "Darwin", "Plato", "Einstein" },
        [VisitorPersonality.Artistic] = new[] { "Picasso", "Monet", "Doodle", "Canvas", "Palette" },
        [VisitorPersonality.Playful] = new[] { "Bubbles", "Giggles", "Bounce", "Zoom", "Silly" },
        [VisitorPersonality.Mysterious] = new[] { "Shadow", "Enigma", "Whisper", "Phantom", "Riddle" },
        [VisitorPersonality.Generous] = new[] { "Sunny", "Kindred", "Blessing", "Grace", "Hope" },
        [VisitorPersonality.Foodie] = new[] { "Crumbs", "Nibbles", "Muffin", "Cookie", "Biscuit" },
        [VisitorPersonality.Athletic] = new[] { "Dash", "Sprint", "Flex", "Champion", "Victor" }
    };

    public static Friend CreateRandom()
    {
        var personality = (VisitorPersonality)Rng.Next(Enum.GetValues<VisitorPersonality>().Length);
        var traits = PersonalityTraits[personality];
        var names = Names[personality];

        return new Friend
        {
            Personality = personality,
            Name = names[Rng.Next(names.Length)],
            Color = traits.color,
            Accessory = traits.accessory
        };
    }

    public void AddFriendshipPoints(int points)
    {
        FriendshipPoints = Math.Max(0, FriendshipPoints + points);
    }

    public void RecordVisit()
    {
        VisitCount++;
        LastVisit = DateTime.Now;
    }

    public string GetGreeting() => Personality switch
    {
        VisitorPersonality.Adventurous => "Hey friend! Ready for adventure?",
        VisitorPersonality.Scholarly => "Greetings! Did you know...",
        VisitorPersonality.Artistic => "Oh, the light is beautiful today!",
        VisitorPersonality.Playful => "TAG! You're it! Hehe!",
        VisitorPersonality.Mysterious => "The winds whispered your name...",
        VisitorPersonality.Generous => "I brought you a little something!",
        VisitorPersonality.Foodie => "Mmm, something smells delicious!",
        VisitorPersonality.Athletic => "Race you to the pond!",
        _ => "Hello there!"
    };

    public string GetAscii() => $"({Accessory})>";

    public Dictionary<string, object> ToSaveData() => new()
    {
        ["id"] = Id,
        ["name"] = Name,
        ["personality"] = Personality.ToString().ToLower(),
        ["friendship_points"] = FriendshipPoints,
        ["visit_count"] = VisitCount,
        ["first_met"] = FirstMet.ToString("O"),
        ["last_visit"] = LastVisit?.ToString("O") ?? "",
        ["color"] = Color,
        ["accessory"] = Accessory
    };
}

/// <summary>
/// Active visitor in the habitat.
/// </summary>
public class Visitor
{
    public Friend Friend { get; }
    public int X { get; set; }
    public int Y { get; set; }
    public DateTime ArrivalTime { get; } = DateTime.Now;
    public bool FacingRight { get; set; } = true;
    public string CurrentActivity { get; set; } = "visiting";
    public int AnimationFrame { get; set; }

    private static readonly Random Rng = new();
    private int _moveTimer;
    private int _targetX;
    private int _targetY;

    public Visitor(Friend friend, int x, int y)
    {
        Friend = friend;
        X = x;
        Y = y;
        _targetX = x;
        _targetY = y;
    }

    /// <summary>
    /// Update visitor behavior.
    /// </summary>
    public void Update(int duckX, int duckY, int fieldWidth, int fieldHeight)
    {
        _moveTimer++;
        AnimationFrame = (_moveTimer / 10) % 4;

        // Move towards target
        if (_moveTimer % 5 == 0)
        {
            if (X < _targetX) { X++; FacingRight = true; }
            else if (X > _targetX) { X--; FacingRight = false; }
            if (Y < _targetY) Y++;
            else if (Y > _targetY) Y--;
        }

        // Pick new target occasionally
        if (_moveTimer % 60 == 0 || (X == _targetX && Y == _targetY))
        {
            // 50% chance to move towards duck, 50% random
            if (Rng.NextDouble() < 0.5)
            {
                _targetX = Math.Clamp(duckX + Rng.Next(-5, 6), 2, fieldWidth - 6);
                _targetY = Math.Clamp(duckY + Rng.Next(-2, 3), 2, fieldHeight - 2);
            }
            else
            {
                _targetX = Rng.Next(2, fieldWidth - 6);
                _targetY = Rng.Next(2, fieldHeight - 2);
            }
        }
    }

    public double VisitDuration => (DateTime.Now - ArrivalTime).TotalMinutes;

    public string GetDisplayChar()
    {
        var frames = new[] { "◇", "◆", "◇", "○" };
        return frames[AnimationFrame % frames.Length];
    }
}

/// <summary>
/// Manages friends and visitors.
/// </summary>
public class FriendsManager
{
    private static readonly Random Rng = new();
    
    private readonly List<Friend> _friends = new();
    private Visitor? _currentVisitor;
    private DateTime _lastVisitorCheck = DateTime.Now;
    
    private const double VisitorChance = 0.02; // Per update
    private const double MinVisitMinutes = 5;
    private const double MaxVisitMinutes = 30;

    public IReadOnlyList<Friend> Friends => _friends;
    public Visitor? CurrentVisitor => _currentVisitor;
    public bool HasVisitor => _currentVisitor != null;

    /// <summary>
    /// Update visitors.
    /// </summary>
    public void Update(int duckX, int duckY, int fieldWidth, int fieldHeight)
    {
        // Update current visitor
        if (_currentVisitor != null)
        {
            _currentVisitor.Update(duckX, duckY, fieldWidth, fieldHeight);

            // Check if visit should end
            var maxDuration = MinVisitMinutes + 
                (_currentVisitor.Friend.Level == FriendshipLevel.BestFriend ? MaxVisitMinutes : 
                 _currentVisitor.Friend.Level == FriendshipLevel.CloseFriend ? 20 :
                 _currentVisitor.Friend.Level == FriendshipLevel.Friend ? 15 : 10);

            if (_currentVisitor.VisitDuration >= maxDuration)
            {
                EndVisit();
            }
        }
        else
        {
            // Check for new visitor
            if (Rng.NextDouble() < VisitorChance)
            {
                SpawnVisitor(fieldWidth, fieldHeight);
            }
        }
    }

    private void SpawnVisitor(int fieldWidth, int fieldHeight)
    {
        Friend friend;
        
        // 40% chance existing friend, 60% new
        if (_friends.Count > 0 && Rng.NextDouble() < 0.4)
        {
            friend = _friends[Rng.Next(_friends.Count)];
        }
        else
        {
            friend = Friend.CreateRandom();
            _friends.Add(friend);
        }

        friend.RecordVisit();

        // Spawn at edge
        var edge = Rng.Next(4);
        var (x, y) = edge switch
        {
            0 => (0, Rng.Next(2, fieldHeight - 2)), // Left
            1 => (fieldWidth - 4, Rng.Next(2, fieldHeight - 2)), // Right
            2 => (Rng.Next(2, fieldWidth - 4), 0), // Top
            _ => (Rng.Next(2, fieldWidth - 4), fieldHeight - 1) // Bottom
        };

        _currentVisitor = new Visitor(friend, x, y);
    }

    private void EndVisit()
    {
        if (_currentVisitor != null)
        {
            // Gain friendship points for visit
            _currentVisitor.Friend.AddFriendshipPoints(5 + (int)_currentVisitor.VisitDuration);
            _currentVisitor = null;
        }
    }

    /// <summary>
    /// Interact with current visitor.
    /// </summary>
    public (int points, string message) InteractWithVisitor()
    {
        if (_currentVisitor == null)
            return (0, "No visitor to interact with.");

        var friend = _currentVisitor.Friend;
        var points = 10 + (int)friend.Level * 5;
        friend.AddFriendshipPoints(points);

        var messages = new[]
        {
            $"{friend.Name} quacks happily!",
            $"{friend.Name}: \"{friend.GetGreeting()}\"",
            $"You and {friend.Name} waddle together!",
            $"{friend.Name} does a little dance!",
            $"{friend.Name} shares some gossip about other ducks."
        };

        return (points, messages[Rng.Next(messages.Length)]);
    }

    public Dictionary<string, object> ToSaveData() => new()
    {
        ["friends"] = _friends.Select(f => f.ToSaveData()).ToList()
    };

    public void LoadSaveData(Dictionary<string, object>? data)
    {
        // TODO: Implement friend loading from save data
    }
}
