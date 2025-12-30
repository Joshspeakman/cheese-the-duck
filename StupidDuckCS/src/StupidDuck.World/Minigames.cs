using System;
using System.Collections.Generic;
using System.Linq;

namespace StupidDuck.World;

/// <summary>
/// Types of mini-games.
/// </summary>
public enum MiniGameType
{
    BreadCatch,
    BugChase,
    MemoryMatch,
    DuckRace
}

/// <summary>
/// Result of playing a mini-game.
/// </summary>
public class MiniGameResult
{
    public MiniGameType GameType { get; set; }
    public int Score { get; set; }
    public bool IsHighScore { get; set; }
    public int CoinsEarned { get; set; }
    public int XpEarned { get; set; }
    public List<string> ItemsEarned { get; set; } = new();
    public string Message { get; set; } = "";
}

/// <summary>
/// Falling item in Bread Catch game.
/// </summary>
public class FallingItem
{
    public int X { get; set; }
    public int Y { get; set; }
    public string ItemType { get; set; } = "bread";
}

/// <summary>
/// Bread Catch - Catch falling bread crumbs!
/// Player moves left/right to catch bread, avoid rotten food.
/// </summary>
public class BreadCatchGame
{
    public int Width { get; set; } = 20;
    public int Height { get; set; } = 10;
    public int PlayerPos { get; set; } = 10;
    public int Score { get; set; }
    public int Lives { get; set; } = 3;
    public List<FallingItem> FallingItems { get; set; } = new();
    public bool GameOver { get; set; }
    public int Frame { get; set; }

    private static readonly Random _random = new();

    // Item types: bread (good), golden_bread (bonus), rotten (bad), seed (small good)
    private static readonly Dictionary<string, char> ItemChars = new()
    {
        ["bread"] = 'o',
        ["golden_bread"] = '*',
        ["rotten"] = 'x',
        ["seed"] = '.'
    };

    private static readonly Dictionary<string, int> ItemPoints = new()
    {
        ["bread"] = 10,
        ["golden_bread"] = 50,
        ["seed"] = 5,
        ["rotten"] = -20
    };

    public void SpawnItem()
    {
        var x = _random.Next(1, Width - 1);

        // Weighted random item type
        var roll = _random.NextDouble();
        string itemType;
        if (roll < 0.6)
            itemType = "bread";
        else if (roll < 0.75)
            itemType = "seed";
        else if (roll < 0.9)
            itemType = "rotten";
        else
            itemType = "golden_bread";

        FallingItems.Add(new FallingItem { X = x, Y = 0, ItemType = itemType });
    }

    public void Update()
    {
        if (GameOver)
            return;

        Frame++;

        // Spawn new items periodically
        if (Frame % 5 == 0)
            SpawnItem();

        // Move items down
        var newItems = new List<FallingItem>();
        foreach (var item in FallingItems)
        {
            item.Y++;

            // Check if caught by player
            if (item.Y >= Height - 1)
            {
                if (Math.Abs(item.X - PlayerPos) <= 1)
                {
                    // Caught!
                    var points = ItemPoints.GetValueOrDefault(item.ItemType);
                    Score += points;
                    if (item.ItemType == "rotten")
                    {
                        Lives--;
                        if (Lives <= 0)
                            GameOver = true;
                    }
                }
                // Item reached bottom, remove it
                continue;
            }

            newItems.Add(item);
        }

        FallingItems = newItems;
    }

    public void MoveLeft() => PlayerPos = Math.Max(1, PlayerPos - 2);
    public void MoveRight() => PlayerPos = Math.Min(Width - 2, PlayerPos + 2);

    public List<string> Render()
    {
        var lines = new List<string>
        {
            $"  BREAD CATCH!  Score: {Score}  Lives: {new string('♥', Lives)}",
            "+" + new string('-', Width) + "+"
        };

        for (var y = 0; y < Height; y++)
        {
            var row = new char[Width];
            for (var i = 0; i < Width; i++)
                row[i] = ' ';

            // Draw falling items
            foreach (var item in FallingItems)
            {
                if (item.Y == y && item.X >= 0 && item.X < Width)
                    row[item.X] = ItemChars.GetValueOrDefault(item.ItemType, '?');
            }

            // Draw player on bottom row
            if (y == Height - 1)
            {
                for (var dx = -1; dx <= 1; dx++)
                {
                    var px = PlayerPos + dx;
                    if (px >= 0 && px < Width)
                        row[px] = dx == 0 ? 'V' : '=';
                }
            }

            lines.Add("|" + new string(row) + "|");
        }

        lines.Add("+" + new string('-', Width) + "+");
        lines.Add("  [<] Left  [>] Right  [Q] Quit");

        if (GameOver)
        {
            lines.Add("");
            lines.Add($"  GAME OVER! Final Score: {Score}");
        }

        return lines;
    }
}

/// <summary>
/// Bug Chase - Quick reaction game to catch bugs!
/// Bugs appear randomly, player must press key quickly.
/// </summary>
public class BugChaseGame
{
    public int Width { get; set; } = 20;
    public int Height { get; set; } = 8;
    public int Score { get; set; }
    public int BugsCaught { get; set; }
    public int BugsEscaped { get; set; }
    public int MaxEscaped { get; set; } = 5;
    public (int X, int Y)? CurrentBug { get; set; }
    public float BugTimer { get; set; }
    public float BugLifetime { get; set; } = 2.0f;
    public bool GameOver { get; set; }
    public List<float> ReactionTimes { get; set; } = new();
    public DateTime BugSpawnTime { get; set; }
    public bool WaitingForBug { get; set; } = true;

    private static readonly Random _random = new();
    private static readonly char[] BugChars = { '@', '#', '&', '%', '~' };

    public void SpawnBug()
    {
        var x = _random.Next(2, Width - 2);
        var y = _random.Next(1, Height - 1);
        CurrentBug = (x, y);
        BugSpawnTime = DateTime.UtcNow;
        WaitingForBug = false;
    }

    public void Update(float deltaTime)
    {
        if (GameOver)
            return;

        if (WaitingForBug)
        {
            BugTimer += deltaTime;
            if (BugTimer > 0.5f + _random.NextDouble() * 1.5f)
            {
                SpawnBug();
                BugTimer = 0;
            }
        }
        else if (CurrentBug.HasValue)
        {
            var elapsed = (float)(DateTime.UtcNow - BugSpawnTime).TotalSeconds;
            if (elapsed > BugLifetime)
            {
                BugsEscaped++;
                CurrentBug = null;
                WaitingForBug = true;
                if (BugsEscaped >= MaxEscaped)
                    GameOver = true;
            }
        }
    }

    public bool CatchBug()
    {
        if (!CurrentBug.HasValue || WaitingForBug)
            return false;

        var reactionTime = (float)(DateTime.UtcNow - BugSpawnTime).TotalSeconds;
        ReactionTimes.Add(reactionTime);

        // Score based on reaction time
        int points;
        if (reactionTime < 0.3f)
            points = 100;
        else if (reactionTime < 0.6f)
            points = 50;
        else if (reactionTime < 1.0f)
            points = 25;
        else
            points = 10;

        Score += points;
        BugsCaught++;
        CurrentBug = null;
        WaitingForBug = true;
        return true;
    }

    public float GetAverageReaction() =>
        ReactionTimes.Count == 0 ? 0f : ReactionTimes.Average();

    public List<string> Render()
    {
        var lines = new List<string>
        {
            $"  BUG CHASE!  Score: {Score}  Caught: {BugsCaught}",
            $"  Escaped: {BugsEscaped}/{MaxEscaped}",
            "+" + new string('-', Width) + "+"
        };

        for (var y = 0; y < Height; y++)
        {
            var row = new char[Width];
            for (var i = 0; i < Width; i++)
                row[i] = ' ';

            // Draw bug if present
            if (CurrentBug.HasValue && !WaitingForBug)
            {
                var (bx, by) = CurrentBug.Value;
                if (by == y && bx >= 0 && bx < Width)
                    row[bx] = BugChars[_random.Next(BugChars.Length)];
            }

            lines.Add("|" + new string(row) + "|");
        }

        lines.Add("+" + new string('-', Width) + "+");

        if (WaitingForBug && !GameOver)
            lines.Add("  Wait for it...");
        else if (CurrentBug.HasValue)
            lines.Add("  [SPACE] CATCH IT!");

        if (GameOver)
        {
            var avg = GetAverageReaction();
            lines.Add("");
            lines.Add($"  GAME OVER! Bugs caught: {BugsCaught}");
            lines.Add($"  Avg reaction: {avg:F2}s");
        }

        lines.Add("  [Q] Quit");

        return lines;
    }
}

/// <summary>
/// Memory Match - Classic card matching game!
/// Find matching pairs of duck items.
/// </summary>
public class MemoryMatchGame
{
    public int GridSize { get; set; } = 4;
    public List<char> Cards { get; set; } = new();
    public List<bool> Revealed { get; set; } = new();
    public List<bool> Matched { get; set; } = new();
    public int? FirstPick { get; set; }
    public int? SecondPick { get; set; }
    public int Moves { get; set; }
    public int PairsFound { get; set; }
    public bool GameOver { get; set; }
    public int CursorPos { get; set; }
    public bool ShowPicks { get; set; }
    public DateTime ShowTimer { get; set; }

    private static readonly char[] CardSymbols = { '@', '#', '$', '%', '&', '*', '+', '=' };
    private static readonly Random _random = new();

    public MemoryMatchGame()
    {
        SetupGame();
    }

    public void SetupGame()
    {
        var numPairs = (GridSize * GridSize) / 2;
        var symbols = CardSymbols.Take(numPairs).ToList();
        Cards = symbols.Concat(symbols).OrderBy(_ => _random.Next()).Select(c => c).ToList();
        Revealed = Enumerable.Repeat(false, Cards.Count).ToList();
        Matched = Enumerable.Repeat(false, Cards.Count).ToList();
        FirstPick = null;
        SecondPick = null;
        Moves = 0;
        PairsFound = 0;
        GameOver = false;
        CursorPos = 0;
    }

    public bool SelectCard()
    {
        if (Matched[CursorPos] || Revealed[CursorPos])
            return false;

        if (!FirstPick.HasValue)
        {
            FirstPick = CursorPos;
            Revealed[CursorPos] = true;
        }
        else if (!SecondPick.HasValue && CursorPos != FirstPick.Value)
        {
            SecondPick = CursorPos;
            Revealed[CursorPos] = true;
            Moves++;
            ShowPicks = true;
            ShowTimer = DateTime.UtcNow;
        }

        return true;
    }

    public void Update()
    {
        if (ShowPicks && FirstPick.HasValue && SecondPick.HasValue)
        {
            if ((DateTime.UtcNow - ShowTimer).TotalSeconds > 1.0)
            {
                // Check for match
                if (Cards[FirstPick.Value] == Cards[SecondPick.Value])
                {
                    Matched[FirstPick.Value] = true;
                    Matched[SecondPick.Value] = true;
                    PairsFound++;
                }
                else
                {
                    Revealed[FirstPick.Value] = false;
                    Revealed[SecondPick.Value] = false;
                }

                FirstPick = null;
                SecondPick = null;
                ShowPicks = false;

                // Check win
                if (PairsFound >= Cards.Count / 2)
                    GameOver = true;
            }
        }
    }

    public void MoveCursor(string direction)
    {
        var row = CursorPos / GridSize;
        var col = CursorPos % GridSize;

        switch (direction)
        {
            case "up" when row > 0:
                row--;
                break;
            case "down" when row < GridSize - 1:
                row++;
                break;
            case "left" when col > 0:
                col--;
                break;
            case "right" when col < GridSize - 1:
                col++;
                break;
        }

        CursorPos = row * GridSize + col;
    }

    public List<string> Render()
    {
        var lines = new List<string>
        {
            $"  MEMORY MATCH!  Pairs: {PairsFound}/{Cards.Count / 2}  Moves: {Moves}",
            ""
        };

        for (var row = 0; row < GridSize; row++)
        {
            var rowStr = "    ";
            for (var col = 0; col < GridSize; col++)
            {
                var idx = row * GridSize + col;

                string card;
                if (Matched[idx])
                    card = "  ";
                else if (Revealed[idx])
                    card = $" {Cards[idx]}";
                else
                    card = " ?";

                if (idx == CursorPos)
                    card = $"[{card.Trim()}]";
                else
                    card = $" {card} ";

                rowStr += card;
            }
            lines.Add(rowStr);
        }

        lines.Add("");
        lines.Add("  [Arrows] Move  [SPACE/ENTER] Select  [Q] Quit");

        if (GameOver)
        {
            lines.Add("");
            lines.Add($"  YOU WIN! Completed in {Moves} moves!");
        }

        return lines;
    }
}

/// <summary>
/// Duck Race - Mash keys to race your duck!
/// Compete against AI ducks in a waddle race.
/// </summary>
public class DuckRaceGame
{
    public int TrackLength { get; set; } = 30;
    public float PlayerPos { get; set; }
    public List<float> AiPositions { get; set; } = new();
    public List<float> AiSpeeds { get; set; } = new();
    public float PlayerStamina { get; set; } = 100f;
    public bool GameOver { get; set; }
    public string? Winner { get; set; }
    public float RaceTime { get; set; }
    public int Mashes { get; set; }

    private static readonly string[] AiNames = { "Quackers", "Waddles", "Feathers", "Bread Boy", "Splash" };
    private static readonly Random _random = new();

    public DuckRaceGame()
    {
        SetupRace();
    }

    public void SetupRace()
    {
        const int numAi = 3;
        AiPositions = Enumerable.Range(0, numAi).Select(_ => 0f).ToList();
        AiSpeeds = Enumerable.Range(0, numAi).Select(_ => 0.3f + (float)_random.NextDouble() * 0.4f).ToList();
        PlayerPos = 0;
        PlayerStamina = 100;
        GameOver = false;
        Winner = null;
        RaceTime = 0;
        Mashes = 0;
    }

    public void Mash()
    {
        if (GameOver || PlayerStamina <= 0)
            return;

        Mashes++;
        var speed = PlayerStamina > 50 ? 0.8f : 0.4f;
        PlayerPos += speed;
        PlayerStamina -= 2;
    }

    public void Update(float deltaTime)
    {
        if (GameOver)
            return;

        RaceTime += deltaTime;

        // Recover stamina slowly
        PlayerStamina = Math.Min(100, PlayerStamina + deltaTime * 5);

        // Move AI ducks
        for (var i = 0; i < AiPositions.Count; i++)
        {
            var speed = AiSpeeds[i] + (float)(_random.NextDouble() - 0.5) * 0.2f;
            AiPositions[i] += speed * deltaTime * 10;
        }

        // Check for winner
        if (PlayerPos >= TrackLength)
        {
            GameOver = true;
            Winner = "You";
        }
        else
        {
            for (var i = 0; i < AiPositions.Count; i++)
            {
                if (AiPositions[i] >= TrackLength)
                {
                    GameOver = true;
                    Winner = AiNames[i];
                    break;
                }
            }
        }
    }

    public List<string> Render()
    {
        var lines = new List<string>
        {
            $"  DUCK RACE!  Time: {RaceTime:F1}s  Stamina: {(int)PlayerStamina}%",
            ""
        };

        // Draw track for player
        var track = new char[TrackLength];
        for (var i = 0; i < TrackLength; i++)
            track[i] = '-';
        var playerIdx = Math.Min((int)PlayerPos, TrackLength - 1);
        track[playerIdx] = '>';
        lines.Add($"  You:      |{new string(track)}| FINISH");

        // Draw tracks for AI
        for (var i = 0; i < AiPositions.Count; i++)
        {
            var aiTrack = new char[TrackLength];
            for (var j = 0; j < TrackLength; j++)
                aiTrack[j] = '-';
            var aiIdx = Math.Min((int)AiPositions[i], TrackLength - 1);
            aiTrack[aiIdx] = '@';
            var name = AiNames[i].PadRight(8).Substring(0, 8);
            lines.Add($"  {name}  |{new string(aiTrack)}|");
        }

        lines.Add("");
        lines.Add("  [SPACE] Mash to waddle faster!");
        lines.Add("  [Q] Quit race");

        if (GameOver)
        {
            lines.Add("");
            if (Winner == "You")
                lines.Add($"  YOU WIN! Time: {RaceTime:F1}s  Mashes: {Mashes}");
            else
                lines.Add($"  {Winner} wins! Better luck next time!");
        }

        return lines;
    }
}

/// <summary>
/// Manages mini-games and rewards.
/// </summary>
public class MiniGameSystem
{
    public Dictionary<string, int> HighScores { get; set; } = new()
    {
        ["bread_catch"] = 0,
        ["bug_chase"] = 0,
        ["memory_match"] = 999,
        ["duck_race"] = 999
    };

    public Dictionary<string, int> GamesPlayed { get; set; } = new()
    {
        ["bread_catch"] = 0,
        ["bug_chase"] = 0,
        ["memory_match"] = 0,
        ["duck_race"] = 0
    };

    public int TotalCoinsEarned { get; set; }
    public string? CurrentGame { get; set; }
    public Dictionary<string, DateTime> Cooldowns { get; set; } = new();
    public float CooldownDuration { get; set; } = 60.0f;

    private static readonly Random _random = new();

    public (bool CanPlay, string Message) CanPlay(string gameType)
    {
        if (Cooldowns.TryGetValue(gameType, out var cooldownStart))
        {
            var elapsed = (DateTime.UtcNow - cooldownStart).TotalSeconds;
            if (elapsed < CooldownDuration)
            {
                var remaining = (int)(CooldownDuration - elapsed);
                return (false, $"Wait {remaining}s before playing again!");
            }
        }
        return (true, "");
    }

    public void StartGame(string gameType)
    {
        CurrentGame = gameType;
        Cooldowns[gameType] = DateTime.UtcNow;
    }

    public MiniGameResult FinishGame(string gameType, int score, bool isTimeBased = false)
    {
        GamesPlayed[gameType] = GamesPlayed.GetValueOrDefault(gameType) + 1;

        // Check high score
        var currentHigh = HighScores.GetValueOrDefault(gameType);
        bool isHighScore;

        if (isTimeBased)
        {
            // Lower is better for time-based games
            isHighScore = score < currentHigh || currentHigh == 0;
            if (isHighScore)
                HighScores[gameType] = score;
        }
        else
        {
            isHighScore = score > currentHigh;
            if (isHighScore)
                HighScores[gameType] = score;
        }

        // Calculate rewards
        var coins = CalculateCoins(gameType, score);
        var xp = CalculateXp(gameType, score);
        var items = CalculateItems(gameType, score);

        TotalCoinsEarned += coins;

        var message = isHighScore ? $"NEW HIGH SCORE! {score}" : $"Score: {score}";

        return new MiniGameResult
        {
            GameType = gameType switch
            {
                "bread_catch" => MiniGameType.BreadCatch,
                "bug_chase" => MiniGameType.BugChase,
                "memory_match" => MiniGameType.MemoryMatch,
                "duck_race" => MiniGameType.DuckRace,
                _ => MiniGameType.BreadCatch
            },
            Score = score,
            IsHighScore = isHighScore,
            CoinsEarned = coins,
            XpEarned = xp,
            ItemsEarned = items,
            Message = message
        };
    }

    private int CalculateCoins(string gameType, int score)
    {
        return gameType switch
        {
            "bread_catch" => score / 5,
            "bug_chase" => score / 10,
            "memory_match" => Math.Max(10, 100 - score * 3),
            "duck_race" => Math.Max(10, 100 - score * 2),
            _ => 10
        };
    }

    private int CalculateXp(string gameType, int score)
    {
        const int baseXp = 10;
        return gameType switch
        {
            "bread_catch" => baseXp + score / 20,
            "bug_chase" => baseXp + score / 25,
            "memory_match" => baseXp + Math.Max(0, 20 - score),
            "duck_race" => baseXp + Math.Max(0, 30 - score),
            _ => baseXp
        };
    }

    private List<string> CalculateItems(string gameType, int score)
    {
        var items = new List<string>();

        // Chance for rare items on high scores
        if (gameType == "bread_catch" && score >= 200 && _random.NextDouble() < 0.3)
            items.Add("golden_crumb");
        else if (gameType == "bug_chase" && score >= 500 && _random.NextDouble() < 0.2)
            items.Add("rare_bug_jar");
        else if (gameType == "memory_match" && score <= 20 && _random.NextDouble() < 0.25)
            items.Add("memory_trophy");
        else if (gameType == "duck_race" && score <= 15 && _random.NextDouble() < 0.2)
            items.Add("racing_medal");

        return items;
    }

    public List<MiniGameInfo> GetAvailableGames()
    {
        var games = new List<MiniGameInfo>
        {
            new()
            {
                Id = "bread_catch",
                Name = "Bread Catch",
                Description = "Catch falling bread crumbs!",
                HighScore = HighScores.GetValueOrDefault("bread_catch"),
                TimesPlayed = GamesPlayed.GetValueOrDefault("bread_catch")
            },
            new()
            {
                Id = "bug_chase",
                Name = "Bug Chase",
                Description = "Quick reactions to catch bugs!",
                HighScore = HighScores.GetValueOrDefault("bug_chase"),
                TimesPlayed = GamesPlayed.GetValueOrDefault("bug_chase")
            },
            new()
            {
                Id = "memory_match",
                Name = "Memory Match",
                Description = "Find matching pairs!",
                HighScore = HighScores.GetValueOrDefault("memory_match", 999),
                TimesPlayed = GamesPlayed.GetValueOrDefault("memory_match")
            },
            new()
            {
                Id = "duck_race",
                Name = "Duck Race",
                Description = "Mash to win the race!",
                HighScore = HighScores.GetValueOrDefault("duck_race", 999),
                TimesPlayed = GamesPlayed.GetValueOrDefault("duck_race")
            }
        };

        // Add cooldown status
        foreach (var game in games)
        {
            var (canPlay, msg) = CanPlay(game.Id);
            game.CanPlay = canPlay;
            game.CooldownMessage = msg;
        }

        return games;
    }

    // =============================================================================
    // SERIALIZATION
    // =============================================================================

    public MiniGameSaveData ToSaveData() => new()
    {
        HighScores = HighScores,
        GamesPlayed = GamesPlayed,
        TotalCoinsEarned = TotalCoinsEarned
    };

    public static MiniGameSystem FromSaveData(MiniGameSaveData data)
    {
        var system = new MiniGameSystem
        {
            TotalCoinsEarned = data.TotalCoinsEarned
        };

        if (data.HighScores != null)
        {
            foreach (var (key, value) in data.HighScores)
                system.HighScores[key] = value;
        }

        if (data.GamesPlayed != null)
        {
            foreach (var (key, value) in data.GamesPlayed)
                system.GamesPlayed[key] = value;
        }

        return system;
    }
}

public class MiniGameInfo
{
    public string Id { get; set; } = "";
    public string Name { get; set; } = "";
    public string Description { get; set; } = "";
    public int HighScore { get; set; }
    public int TimesPlayed { get; set; }
    public bool CanPlay { get; set; } = true;
    public string CooldownMessage { get; set; } = "";
}

public class MiniGameSaveData
{
    public Dictionary<string, int>? HighScores { get; set; }
    public Dictionary<string, int>? GamesPlayed { get; set; }
    public int TotalCoinsEarned { get; set; }
}
