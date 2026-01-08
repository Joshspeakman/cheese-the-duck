using System.Text;
using Spectre.Console;
using StupidDuck.Core;
using StupidDuck.World;
using DuckEntity = StupidDuck.Duck.Duck;
using GameState = StupidDuck.World.GameState;

namespace StupidDuck.UI;

/// <summary>
/// Box drawing characters matching Python version.
/// </summary>
public static class BoxChars
{
    // Single line box
    public const char TopLeft = '\u250c';      // ┌
    public const char TopRight = '\u2510';     // ┐
    public const char BottomLeft = '\u2514';   // └
    public const char BottomRight = '\u2518';  // ┘
    public const char Horizontal = '\u2500';   // ─
    public const char Vertical = '\u2502';     // │
    public const char TeeRight = '\u251c';     // ├
    public const char TeeLeft = '\u2524';      // ┤
    public const char TeeDown = '\u252c';      // ┬
    public const char TeeUp = '\u2534';        // ┴
    public const char Cross = '\u253c';        // ┼
    
    // Double line box (for header emphasis)
    public const char DoubleTopLeft = '\u2554';     // ╔
    public const char DoubleTopRight = '\u2557';    // ╗
    public const char DoubleBottomLeft = '\u255a';  // ╚
    public const char DoubleBottomRight = '\u255d'; // ╝
    public const char DoubleHorizontal = '\u2550';  // ═
    public const char DoubleVertical = '\u2551';    // ║
}

/// <summary>
/// Progress bar characters matching Python version.
/// </summary>
public static class BarChars
{
    public const char Full = '\u2588';   // █ Full block
    public const char High = '\u2593';   // ▓ Dark shade
    public const char Med = '\u2592';    // ▒ Medium shade
    public const char Low = '\u2591';    // ░ Light shade
    public const char Empty = ' ';
}

/// <summary>
/// Tracks duck position and movement in the playfield.
/// </summary>
public class DuckPosition
{
    private readonly Random _rng = new();
    
    public int FieldWidth { get; set; }
    public int FieldHeight { get; set; }
    public int X { get; set; }
    public int Y { get; set; }
    public int TargetX { get; set; }
    public int TargetY { get; set; }
    public bool FacingRight { get; set; } = true;
    public bool IsMoving { get; set; }
    
    private float _moveTimer;
    private float _idleTimer;
    private string _state = "idle";
    private int _animationFrame;
    private float _stateAnimationTimer;
    private float _stateDuration;
    private DateTime _stateStartTime;

    public DuckPosition(int fieldWidth = 40, int fieldHeight = 12)
    {
        FieldWidth = fieldWidth;
        FieldHeight = fieldHeight;
        X = fieldWidth / 2;
        Y = fieldHeight / 2;
        TargetX = X;
        TargetY = Y;
    }

    public void Update(float deltaTime)
    {
        _moveTimer += deltaTime;
        _idleTimer += deltaTime;
        _stateAnimationTimer += deltaTime;

        // Cycle animation frames for non-idle states
        if (_state is "sleeping" or "eating" or "playing" or "cleaning" or "petting")
        {
            if (_stateAnimationTimer > 0.4f)
            {
                _animationFrame = (_animationFrame + 1) % 2;
                _stateAnimationTimer = 0;
            }

            if (_stateDuration > 0 && (DateTime.Now - _stateStartTime).TotalSeconds > _stateDuration)
            {
                _state = "idle";
                _stateDuration = 0;
            }
            return;
        }

        // Randomly pick new target when idle
        if (_state == "idle" && _idleTimer > _rng.NextSingle() * 5 + 3)
        {
            if (_rng.NextDouble() < 0.6)
            {
                PickNewTarget();
                _idleTimer = 0;
            }
        }

        // Move towards target
        if (X != TargetX || Y != TargetY)
        {
            IsMoving = true;
            _state = "walking";

            if (_moveTimer > 0.15f)
            {
                _moveTimer = 0;
                _animationFrame = (_animationFrame + 1) % 4;

                if (X < TargetX) { X++; FacingRight = true; }
                else if (X > TargetX) { X--; FacingRight = false; }

                if (Y < TargetY) Y++;
                else if (Y > TargetY) Y--;
            }
        }
        else
        {
            IsMoving = false;
            if (_state == "walking")
            {
                _state = "idle";
                _idleTimer = 0;
            }
        }
    }

    private void PickNewTarget()
    {
        const int margin = 3;
        var maxX = Math.Max(margin, FieldWidth - margin - 6);
        var maxY = Math.Max(margin, FieldHeight - margin - 3);
        TargetX = _rng.Next(margin, maxX + 1);
        TargetY = _rng.Next(margin, maxY + 1);
    }

    public void SetState(string state, float duration = 3.0f)
    {
        _state = state;
        _animationFrame = 0;
        _stateAnimationTimer = 0;
        _stateDuration = duration;
        _stateStartTime = DateTime.Now;

        if (state is "sleeping" or "eating" or "playing" or "cleaning" or "petting")
        {
            TargetX = X;
            TargetY = Y;
            IsMoving = false;
        }
    }

    public string GetState() => _state;
    public int GetAnimationFrame() => _animationFrame;
}

/// <summary>
/// Renders the game UI to the terminal using Spectre.Console.
/// </summary>
public class Renderer
{
    private readonly DuckPosition _duckPos;
    private readonly AnimationController _animations = new();
    private readonly List<string> _messageQueue = new();
    private DateTime _messageExpire = DateTime.MinValue;
    private bool _showHelp;
    private bool _showInventory;
    private bool _showStats;
    private bool _showTalk;
    private string _talkBuffer = "";
    private DateTime _lastRenderTime = DateTime.Now;
    
    // Weather particles
    private readonly List<(int x, int y, char c)> _weatherParticles = new();
    private readonly Random _rng = new();

    public Renderer()
    {
        _duckPos = new DuckPosition(50, 15);
    }

    public DuckPosition DuckPosition => _duckPos;
    public AnimationController Animations => _animations;

    public void ShowMessage(string message, int durationMs = 3000)
    {
        _messageQueue.Add(message);
        _messageExpire = DateTime.Now.AddMilliseconds(durationMs);
    }

    public void ToggleHelp() => _showHelp = !_showHelp;
    public void ToggleInventory() => _showInventory = !_showInventory;
    public void ToggleStats() => _showStats = !_showStats;
    public void ToggleTalk() => _showTalk = !_showTalk;
    public bool IsTalking() => _showTalk;

    public string GetTalkBuffer() => _talkBuffer;
    public void AddTalkChar(char c) => _talkBuffer += c;
    public void BackspaceTalk()
    {
        if (_talkBuffer.Length > 0)
            _talkBuffer = _talkBuffer[..^1];
    }
    public void ClearTalkBuffer() => _talkBuffer = "";

    /// <summary>
    /// Update animation state.
    /// </summary>
    public void Update(float deltaTime)
    {
        _duckPos.Update(deltaTime);
        _animations.Update(deltaTime);
        
        // Clean expired messages
        if (DateTime.Now > _messageExpire && _messageQueue.Count > 0)
            _messageQueue.Clear();
    }

    /// <summary>
    /// Render the title screen.
    /// </summary>
    public void RenderTitleScreen()
    {
        Console.Clear();
        Console.CursorVisible = false;

        var panel = new Panel(string.Join('\n', AsciiArt.TitleArt))
            .Border(BoxBorder.None)
            .Expand();

        AnsiConsole.Write(panel);
        
        AnsiConsole.MarkupLine("\n[yellow]Press [bold]N[/] for New Game or [bold]L[/] to Load[/]");
        AnsiConsole.MarkupLine("[dim]Press [bold]Q[/] to Quit[/]");
    }

    /// <summary>
    /// Render the main game screen with full game state.
    /// Uses direct string building like Python for better control.
    /// Buffers all output to prevent flashing.
    /// </summary>
    public void RenderGameWithState(GameState state)
    {
        if (state.Duck == null) return;
        
        Console.CursorVisible = false;
        
        // Get terminal dimensions
        var termWidth = Math.Max(Console.WindowWidth, 80);
        var termHeight = Math.Max(Console.WindowHeight, 24);
        
        // Cap to reasonable maximum like Python
        var width = Math.Min(termWidth, 120);
        var height = Math.Min(termHeight, 40);
        
        // Layout: sidebar = 1/3, playfield = 2/3
        var sidebarWidth = Math.Max(25, Math.Min(35, width / 3));
        var playfieldWidth = width - sidebarWidth;
        var fieldHeight = Math.Max(10, height - 8); // Header(3) + Bottom(3) + Messages(2)
        
        // Update duck position field dimensions
        _duckPos.FieldWidth = playfieldWidth - 2;
        _duckPos.FieldHeight = fieldHeight - 2;
        
        // Build output lines
        var output = new List<string>();
        
        // Header bar (3 lines with double border)
        output.AddRange(BuildHeaderLines(state, width));
        
        // Playfield + Sidebar area
        var playfieldLines = BuildPlayfieldLines(state, playfieldWidth, fieldHeight);
        var sidebarLines = BuildSidebarLines(state, sidebarWidth, fieldHeight);
        
        // Combine playfield and sidebar
        var maxLines = Math.Max(playfieldLines.Count, sidebarLines.Count);
        for (var i = 0; i < maxLines; i++)
        {
            var pfLine = i < playfieldLines.Count ? playfieldLines[i] : new string(' ', playfieldWidth);
            var sbLine = i < sidebarLines.Count ? sidebarLines[i] : new string(' ', sidebarWidth);
            output.Add(pfLine + sbLine);
        }
        
        // Message area (1 line)
        output.Add(BuildMessageLine(width));
        
        // Controls bar (3 lines with border)
        output.AddRange(BuildControlsBar(width));
        
        // Render to screen using buffered output (prevents flashing)
        var buffer = new StringBuilder();
        buffer.Append("\x1b[H");  // Move cursor to home position (0,0)
        
        for (var i = 0; i < height - 1; i++)
        {
            string line;
            if (i < output.Count)
            {
                line = output[i];
                if (line.Length > width) line = line[..width];
                else if (line.Length < width) line = line + new string(' ', width - line.Length);
            }
            else
            {
                line = new string(' ', width);
            }
            
            buffer.Append(line);
            if (i < height - 2) buffer.Append('\n');
        }
        
        // Write entire buffer at once
        Console.Write(buffer.ToString());

        // Render overlays on top
        if (_showHelp)
            RenderHelpOverlay();

        if (_messageQueue.Count > 0 && DateTime.Now < _messageExpire)
            RenderMessage(_messageQueue[^1]);
    }
    
    /// <summary>
    /// Build header bar lines (3 lines with double border).
    /// </summary>
    private List<string> BuildHeaderLines(GameState state, int width)
    {
        var duck = state.Duck!;
        var mood = duck.GetMood();
        var innerWidth = width - 2;
        
        // Mood indicators
        var moodEmoji = mood.State switch
        {
            Duck.MoodState.Ecstatic => "[*o*]",
            Duck.MoodState.Happy => "[^-^]",
            Duck.MoodState.Content => "[-.-]",
            Duck.MoodState.Grumpy => "[>_<]",
            Duck.MoodState.Sad => "[;_;]",
            Duck.MoodState.Miserable => "[T_T]",
            _ => "[-.-]"
        };

        var time = state.Clock.Now;
        var timeStr = time.ToString("HH:mm");
        var timeOfDay = state.Clock.GetTimeOfDay();
        var weatherIcon = state.Weather.GetWeatherIcon();
        var weatherName = state.Weather.CurrentWeather.ToString();
        
        // Time icon
        var timeIcon = timeOfDay switch
        {
            "Dawn" => "☀",
            "Morning" => "☀",
            "Afternoon" => "☀",
            "Evening" => "☁",
            "Night" => "☾",
            _ => "☁"
        };

        // Build left and right with proper spacing
        var leftPart = $" {duck.Name} | {weatherIcon} {weatherName} | {timeIcon} {timeStr} {timeOfDay}";
        var rightPart = $"{moodEmoji} {state.GetPlaytimeDisplay()} ${state.Coins} ";
        
        var padding = Math.Max(1, innerWidth - leftPart.Length - rightPart.Length);
        var content = leftPart + new string(' ', padding) + rightPart;
        if (content.Length > innerWidth) content = content[..innerWidth];
        content = content.PadRight(innerWidth);
        
        return new List<string>
        {
            BoxChars.DoubleTopLeft + new string(BoxChars.DoubleHorizontal, innerWidth) + BoxChars.DoubleTopRight,
            $"{BoxChars.DoubleVertical}{content}{BoxChars.DoubleVertical}",
            BoxChars.DoubleBottomLeft + new string(BoxChars.DoubleHorizontal, innerWidth) + BoxChars.DoubleBottomRight
        };
    }
    
    /// <summary>
    /// Build playfield lines with proper borders.
    /// </summary>
    private List<string> BuildPlayfieldLines(GameState state, int width, int height)
    {
        var innerWidth = width - 2;
        var innerHeight = height - 2;
        var lines = new List<string>();
        
        // Top border with header
        var header = "─ DUCK HABITAT ─";
        var headerPad = (innerWidth - header.Length) / 2;
        var topBorder = BoxChars.TopLeft + 
            new string(BoxChars.Horizontal, headerPad) + header + 
            new string(BoxChars.Horizontal, innerWidth - headerPad - header.Length) + 
            BoxChars.TopRight;
        lines.Add(topBorder);
        
        // Build field content
        var duck = state.Duck!;
        var decorations = state.Decorations.GetRenderPositions();
        var visitor = state.Friends.CurrentVisitor;
        
        // Get duck sprite
        var duckLines = GetDuckSpriteLines(duck);
        var duckHeight = duckLines.Length;
        var duckWidth = duckLines.Max(l => l.Length);
        
        // Generate habitat detail
        for (var y = 0; y < innerHeight; y++)
        {
            var sb = new StringBuilder();
            sb.Append(BoxChars.Vertical);
            
            var x = 0;
            while (x < innerWidth)
            {
                // Check if we're in duck area
                var duckY = y - _duckPos.Y;
                if (duckY >= 0 && duckY < duckHeight && x >= _duckPos.X && x < _duckPos.X + duckWidth)
                {
                    if (x == _duckPos.X)
                    {
                        var duckLine = duckLines[duckY];
                        sb.Append(duckLine);
                        x += duckLine.Length;
                        continue;
                    }
                    x++;
                    continue;
                }
                
                // Check visitor
                if (visitor != null && x == visitor.X && y == visitor.Y)
                {
                    sb.Append(visitor.GetDisplayChar());
                    x++;
                    continue;
                }
                
                // Check decorations
                if (decorations.TryGetValue((x, y), out var deco))
                {
                    sb.Append(deco.ascii);
                    x++;
                    continue;
                }
                
                // Detailed ground pattern with habitat features
                sb.Append(GetDetailedGroundChar(x, y, innerWidth, innerHeight));
                x++;
            }
            
            // Pad to exact width
            var lineContent = sb.ToString();
            if (lineContent.Length < width - 1)
                lineContent += new string(' ', width - 1 - lineContent.Length);
            else if (lineContent.Length > width - 1)
                lineContent = lineContent[..(width - 1)];
            
            lines.Add(lineContent + BoxChars.Vertical);
        }
        
        // Bottom border
        lines.Add(BoxChars.BottomLeft + new string(BoxChars.Horizontal, innerWidth) + BoxChars.BottomRight);
        
        return lines;
    }
    
    /// <summary>
    /// Get detailed ground char with habitat features like Python.
    /// </summary>
    private char GetDetailedGroundChar(int x, int y, int fieldWidth, int fieldHeight)
    {
        // Pond in center-left
        var pondX = fieldWidth / 3;
        var pondY = fieldHeight / 2;
        var distFromPond = Math.Sqrt(Math.Pow(x - pondX, 2) + Math.Pow(y - pondY, 2));
        
        if (distFromPond < 4)
        {
            // Pond water
            var hash = (x + y) % 3;
            return hash switch { 0 => '~', 1 => '≈', _ => '~' };
        }
        if (distFromPond < 5)
        {
            // Pond edge
            return '·';
        }
        
        // Nest area bottom-right
        if (x > fieldWidth - 10 && y > fieldHeight - 4)
        {
            var hash = (x + y) % 4;
            return hash switch { 0 => '(', 1 => ')', 2 => '_', _ => ' ' };
        }
        
        // Food bowl area top-left
        if (x < 8 && y < 3)
        {
            var hash = (x + y) % 5;
            return hash switch { 0 => 'o', 1 => '°', 2 => '.', _ => ' ' };
        }
        
        // Grass patches
        var grassHash = (x * 17 + y * 31) % 50;
        if (grassHash < 4)
        {
            return grassHash switch { 0 => '"', 1 => '\'', 2 => '.', _ => ',' };
        }
        
        // Rocks scattered
        var rockHash = (x * 7 + y * 13) % 80;
        if (rockHash == 0) return 'o';
        if (rockHash == 1) return '°';
        
        return ' ';
    }
    
    /// <summary>
    /// Build sidebar lines with proper borders.
    /// </summary>
    private List<string> BuildSidebarLines(GameState state, int width, int height)
    {
        var innerWidth = width - 2;
        var lines = new List<string>();
        var duck = state.Duck!;
        var mood = duck.GetMood();
        
        // Top border
        lines.Add(BoxChars.TopLeft + new string(BoxChars.Horizontal, innerWidth) + BoxChars.TopRight);
        
        // Duck face closeup (5 lines)
        var faceLines = GetEmotionCloseup(mood.State);
        foreach (var line in faceLines)
        {
            var padded = CenterString(line, innerWidth);
            lines.Add($"{BoxChars.Vertical}{padded}{BoxChars.Vertical}");
        }
        
        // Divider
        lines.Add($"{BoxChars.TeeRight}{new string(BoxChars.Horizontal, innerWidth)}{BoxChars.TeeLeft}");
        
        // Needs bars
        var needs = duck.Needs;
        lines.Add($"{BoxChars.Vertical}{BuildNeedBarPlain("HUN", needs.Hunger, innerWidth)}{BoxChars.Vertical}");
        lines.Add($"{BoxChars.Vertical}{BuildNeedBarPlain("ENG", needs.Energy, innerWidth)}{BoxChars.Vertical}");
        lines.Add($"{BoxChars.Vertical}{BuildNeedBarPlain("FUN", needs.Fun, innerWidth)}{BoxChars.Vertical}");
        lines.Add($"{BoxChars.Vertical}{BuildNeedBarPlain("CLN", needs.Cleanliness, innerWidth)}{BoxChars.Vertical}");
        lines.Add($"{BoxChars.Vertical}{BuildNeedBarPlain("SOC", needs.Social, innerWidth)}{BoxChars.Vertical}");
        
        // Divider
        lines.Add($"{BoxChars.TeeRight}{new string(BoxChars.Horizontal, innerWidth)}{BoxChars.TeeLeft}");
        
        // Shortcuts header
        lines.Add($"{BoxChars.Vertical}{CenterString("─── SHORTCUTS ───", innerWidth)}{BoxChars.Vertical}");
        lines.Add($"{BoxChars.Vertical}{CenterString("[F] Feed   [P] Play", innerWidth)}{BoxChars.Vertical}");
        lines.Add($"{BoxChars.Vertical}{CenterString("[L] Clean  [D] Pet", innerWidth)}{BoxChars.Vertical}");
        lines.Add($"{BoxChars.Vertical}{CenterString("[Z] Sleep  [T] Talk", innerWidth)}{BoxChars.Vertical}");
        lines.Add($"{BoxChars.Vertical}{new string(' ', innerWidth)}{BoxChars.Vertical}");
        lines.Add($"{BoxChars.Vertical}{CenterString("[E] Explore [A] Areas", innerWidth)}{BoxChars.Vertical}");
        lines.Add($"{BoxChars.Vertical}{CenterString("[C] Craft  [R] Build", innerWidth)}{BoxChars.Vertical}");
        lines.Add($"{BoxChars.Vertical}{new string(' ', innerWidth)}{BoxChars.Vertical}");
        lines.Add($"{BoxChars.Vertical}{CenterString("[I] Items  [B] Shop", innerWidth)}{BoxChars.Vertical}");
        lines.Add($"{BoxChars.Vertical}{CenterString("[G] Goals  [S] Stats", innerWidth)}{BoxChars.Vertical}");
        lines.Add($"{BoxChars.Vertical}{CenterString("[H] Help   [Q] Quit", innerWidth)}{BoxChars.Vertical}");
        
        // Divider
        lines.Add($"{BoxChars.TeeRight}{new string(BoxChars.Horizontal, innerWidth)}{BoxChars.TeeLeft}");
        
        // Activity status
        var stateDisplay = _duckPos.GetState() switch
        {
            "sleeping" => "Sleeping Zzz",
            "eating" => "Eating nom",
            "playing" => "Playing!",
            "cleaning" => "Bathing",
            "petting" => "Being petted!",
            "walking" => "Wandering",
            _ => "Chilling"
        };
        lines.Add($"{BoxChars.Vertical}{CenterString(stateDisplay, innerWidth)}{BoxChars.Vertical}");
        lines.Add($"{BoxChars.Vertical}{CenterString(state.CurrentActivity, innerWidth)}{BoxChars.Vertical}");
        lines.Add($"{BoxChars.Vertical}{CenterString($"@ {state.CurrentLocation}", innerWidth)}{BoxChars.Vertical}");
        
        // Fill remaining height
        while (lines.Count < height - 1)
        {
            lines.Add($"{BoxChars.Vertical}{new string(' ', innerWidth)}{BoxChars.Vertical}");
        }
        
        // Bottom border
        lines.Add(BoxChars.BottomLeft + new string(BoxChars.Horizontal, innerWidth) + BoxChars.BottomRight);
        
        return lines;
    }
    
    /// <summary>
    /// Build plain text need bar (no markup).
    /// </summary>
    private string BuildNeedBarPlain(string name, float value, int width)
    {
        var barWidth = 8;
        var filled = (int)((value / 100f) * barWidth);
        var bar = new string('█', filled) + new string(' ', barWidth - filled);
        var result = $"{name}[{bar}] {(int)value}%";
        return result.PadRight(width);
    }
    
    /// <summary>
    /// Center a string within a given width.
    /// </summary>
    private string CenterString(string s, int width)
    {
        if (s.Length >= width) return s[..width];
        var pad = (width - s.Length) / 2;
        return new string(' ', pad) + s + new string(' ', width - pad - s.Length);
    }
    
    /// <summary>
    /// Build message line.
    /// </summary>
    private string BuildMessageLine(int width)
    {
        var innerWidth = width - 2;
        string msg = _messageQueue.Count > 0 && DateTime.Now < _messageExpire 
            ? _messageQueue[^1] 
            : "Press [H] for help";
        var content = CenterString(msg, innerWidth);
        return BoxChars.Vertical + content + BoxChars.Vertical;
    }
    
    /// <summary>
    /// Build controls bar (3 lines with border).
    /// </summary>
    private List<string> BuildControlsBar(int width)
    {
        var innerWidth = width - 2;
        var controls = "[H]elp for shortcuts • [M]ute • [+/-] Volume";
        var content = CenterString(controls, innerWidth);
        
        return new List<string>
        {
            BoxChars.TopLeft + new string(BoxChars.Horizontal, innerWidth) + BoxChars.TopRight,
            $"{BoxChars.Vertical}{content}{BoxChars.Vertical}",
            BoxChars.BottomLeft + new string(BoxChars.Horizontal, innerWidth) + BoxChars.BottomRight
        };
    }
    
    // Keep the old BuildHeaderContent for reference but it's no longer used
    private string BuildHeaderContentOld(GameState state)
    {
        var duck = state.Duck!;
        var mood = duck.GetMood();
        
        // Mood indicators matching Python exactly - escape brackets for Spectre
        var moodEmoji = mood.State switch
        {
            Duck.MoodState.Ecstatic => "[[*o*]]",
            Duck.MoodState.Happy => "[[^-^]]",
            Duck.MoodState.Content => "[[-.-]]",
            Duck.MoodState.Grumpy => "[[>_<]]",
            Duck.MoodState.Sad => "[[;_;]]",
            Duck.MoodState.Miserable => "[[T_T]]",
            _ => "[[-.-]]"
        };

        var time = state.Clock.Now;
        var timeStr = time.ToString("HH:mm");
        var timeOfDay = state.Clock.GetTimeOfDay();
        var weatherIcon = state.Weather.GetWeatherIcon();
        var weatherName = state.Weather.CurrentWeather.ToString();
        
        // Get time-of-day icon
        var timeIcon = timeOfDay switch
        {
            "Dawn" => "☀",
            "Morning" => "☀",
            "Afternoon" => "☀",
            "Evening" => "☁",
            "Night" => "☾",
            _ => "☁"
        };

        // Build content with colors
        return $"[yellow]{Markup.Escape(duck.Name)}[/] | {Markup.Escape(weatherIcon)}{weatherName} | {Markup.Escape(timeIcon)}{timeStr} {timeOfDay}                    {moodEmoji} {state.GetPlaytimeDisplay()} [green]${state.Coins}[/]";
    }

    private string BuildPlayfield(DuckEntity duck)
    {
        var sb = new StringBuilder();
        
        // Draw ground
        for (var y = 0; y < _duckPos.FieldHeight; y++)
        {
            for (var x = 0; x < _duckPos.FieldWidth; x++)
            {
                // Draw duck at position
                if (x == _duckPos.X && y == _duckPos.Y)
                {
                    sb.Append(_duckPos.FacingRight ? "(o)>" : "<(o)");
                    x += 3; // Skip duck width
                }
                else
                {
                    // Ground pattern
                    sb.Append(GetGroundChar(x, y));
                }
            }
            sb.AppendLine();
        }

        return sb.ToString();
    }

    /// <summary>
    /// Build the enhanced playfield with decorations and visitors.
    /// Matches Python's colored ground, decorations, and duck rendering.
    /// </summary>
    private string BuildEnhancedPlayfield(GameState state)
    {
        var sb = new StringBuilder();
        var duck = state.Duck!;
        var decorations = state.Decorations.GetRenderPositions();
        var visitor = state.Friends.CurrentVisitor;
        var weatherParticles = state.Weather.GetParticles();
        
        // Generate weather particles positions (reduced count)
        UpdateWeatherParticles(weatherParticles);
        
        // Get multi-line duck sprite
        var duckLines = GetDuckSpriteLines(duck);
        var duckWidth = duckLines.Max(l => l.Length);
        var duckHeight = duckLines.Length;

        // Create a 2D grid for more sophisticated rendering
        for (var y = 0; y < _duckPos.FieldHeight; y++)
        {
            var x = 0;
            while (x < _duckPos.FieldWidth)
            {
                // Check if we're rendering part of the duck (multi-line sprite)
                var duckLineIdx = y - _duckPos.Y;
                if (duckLineIdx >= 0 && duckLineIdx < duckHeight &&
                    x >= _duckPos.X && x < _duckPos.X + duckWidth)
                {
                    // We're in the duck area - render the whole duck line at once
                    if (x == _duckPos.X)
                    {
                        var duckLine = duckLines[duckLineIdx];
                        sb.Append($"[yellow]{Markup.Escape(duckLine)}[/]");
                        x += duckLine.Length;
                        continue;
                    }
                    // Skip - already rendered as part of duck line
                    x++;
                    continue;
                }

                // Check for visitor
                if (visitor != null && x == visitor.X && y == visitor.Y)
                {
                    var visitorChar = visitor.GetDisplayChar();
                    sb.Append($"[magenta]{Markup.Escape(visitorChar)}[/]");
                    x++;
                    continue;
                }

                // Check for decorations
                if (decorations.TryGetValue((x, y), out var deco))
                {
                    sb.Append($"[{deco.color}]{Markup.Escape(deco.ascii)}[/]");
                    x++;
                    continue;
                }

                // Check for weather particles
                var particle = _weatherParticles.FirstOrDefault(p => p.x == x && p.y == y);
                if (particle.c != '\0')
                {
                    var particleColor = state.Weather.CurrentWeather switch
                    {
                        WeatherType.Rainy or WeatherType.Stormy => "blue",
                        WeatherType.Snowy => "white",
                        WeatherType.Foggy => "grey",
                        WeatherType.Windy => "cyan",
                        _ => "white"
                    };
                    sb.Append($"[{particleColor}]{particle.c}[/]");
                    x++;
                    continue;
                }

                // Ground pattern with pond and grass like Python
                var (groundChar, groundColor) = GetColoredGroundChar(x, y);
                if (groundColor != null)
                {
                    sb.Append($"[{groundColor}]{groundChar}[/]");
                }
                else
                {
                    sb.Append(groundChar);
                }
                x++;
            }
            sb.AppendLine();
        }

        return sb.ToString();
    }

    /// <summary>
    /// Get duck sprite lines with proper appearance (3 lines like Python).
    /// Returns array of lines for the duck.
    /// </summary>
    private string[] GetDuckSpriteLines(DuckEntity duck)
    {
        var state = _duckPos.GetState();
        var frame = _duckPos.GetAnimationFrame();
        
        return state switch
        {
            "sleeping" => frame == 0 
                ? new[] { " __z", "(-~)", "~~~)" }
                : new[] { " __Z", "(~-)", "~~~)" },
            "eating" => frame == 0 
                ? new[] { " __°", "(o>)", "°'\\)" }
                : new[] { " __ ", "(o>°", "/'\\)" },
            "playing" => frame == 0 
                ? new[] { "\\__/", "(^>)", " '\\)" }
                : new[] { " __ ", "(^>)!", " /')" },
            "cleaning" => frame == 0 
                ? new[] { "~__~", "(o>)", "~~~)" }
                : new[] { " __~", "~o>)", "~'\\)" },
            "petting" => frame == 0
                ? new[] { " __♥", "(^>)", "/'\\)" }
                : new[] { "♥__ ", "(^>)", "~'\\)" },
            _ => _duckPos.FacingRight 
                ? new[] { " __ ", "(^>)", "/'\\)" }
                : new[] { " __ ", "(<^)", "(/'\\ " }
        };
    }

    /// <summary>
    /// Get ground character with color - cleaner pattern like Python.
    /// </summary>
    private (char ch, string? color) GetColoredGroundChar(int x, int y)
    {
        // Create a pond area in the center-left (matching Python's location rendering)
        var centerX = _duckPos.FieldWidth / 2 - 5;
        var centerY = _duckPos.FieldHeight / 2;
        var distFromPond = Math.Sqrt(Math.Pow(x - centerX, 2) + Math.Pow(y - centerY, 2));
        
        // Pond - circular water area (smaller, cleaner)
        if (distFromPond < 3)
        {
            var hash = (x * 31 + y * 17) % 3;  // Remove time-based animation for stability
            var ch = hash switch
            {
                0 => '~',
                1 => '≈',
                _ => '~'
            };
            return (ch, "blue");
        }
        
        // Pond edge - subtle
        if (distFromPond < 4)
        {
            return ('.', "cyan");
        }
        
        // Sparse grass - much less dense
        var grassHash = (x * 13 + y * 29) % 80;
        if (grassHash < 3)
        {
            var grassChar = grassHash switch
            {
                0 => '.',
                1 => ',',
                _ => '\''
            };
            return (grassChar, "green");
        }
        
        // Mostly empty for clean look (like Python)
        return (' ', null);
    }

    private void UpdateWeatherParticles(char[] chars)
    {
        // Remove old particles and add new ones
        _weatherParticles.Clear();
        
        if (chars.Length == 0) return;

        // Add sparse particles - much fewer for cleaner look
        var count = _rng.Next(2, 6);
        for (var i = 0; i < count; i++)
        {
            _weatherParticles.Add((
                _rng.Next(0, _duckPos.FieldWidth),
                _rng.Next(0, _duckPos.FieldHeight),
                chars[_rng.Next(chars.Length)]
            ));
        }
    }

    /// <summary>
    /// Build the enhanced sidebar matching Python UI.
    /// </summary>
    private Markup BuildEnhancedSidebar(GameState state)
    {
        var duck = state.Duck!;
        var mood = duck.GetMood();
        var sb = new StringBuilder();

        // Duck closeup face art (matching Python)
        var faceLines = GetEmotionCloseup(mood.State);
        foreach (var line in faceLines)
        {
            sb.AppendLine($"[yellow]{Markup.Escape(line)}[/]");
        }
        
        // Divider
        sb.AppendLine($"[dim]{BoxChars.TeeRight}{new string(BoxChars.Horizontal, 18)}{BoxChars.TeeLeft}[/]");

        // Needs with color-coded bars (Python style: value >= 70 green, >= 40 yellow, else red)
        var needs = duck.Needs;
        sb.AppendLine(BuildNeedLine("HUN", needs.Hunger));
        sb.AppendLine(BuildNeedLine("ENG", needs.Energy));
        sb.AppendLine(BuildNeedLine("FUN", needs.Fun));
        sb.AppendLine(BuildNeedLine("CLN", needs.Cleanliness));
        sb.AppendLine(BuildNeedLine("SOC", needs.Social));

        // Divider
        sb.AppendLine($"[dim]{BoxChars.TeeRight}{new string(BoxChars.Horizontal, 18)}{BoxChars.TeeLeft}[/]");
        
        // Shortcuts section header - escape [ and ] as [[ and ]] for Spectre.Console
        sb.AppendLine("[dim]─── SHORTCUTS ───[/]");
        sb.AppendLine("[[F]] Feed   [[P]] Play");
        sb.AppendLine("[[L]] Clean  [[D]] Pet");
        sb.AppendLine("[[Z]] Sleep  [[T]] Talk");
        sb.AppendLine();
        sb.AppendLine("[[E]] Explore [[A]] Areas");
        sb.AppendLine("[[C]] Craft  [[R]] Build");
        sb.AppendLine();
        sb.AppendLine("[[I]] Items  [[B]] Shop");
        sb.AppendLine("[[G]] Goals  [[S]] Stats");
        sb.AppendLine("[[H]] Help   [[Q]] Quit");
        
        // Divider
        sb.AppendLine($"[dim]{BoxChars.TeeRight}{new string(BoxChars.Horizontal, 18)}{BoxChars.TeeLeft}[/]");

        // Current activity status
        var stateDisplay = _duckPos.GetState() switch
        {
            "sleeping" => "Sleeping Zzz",
            "eating" => "Eating nom",
            "playing" => "Playing!",
            "cleaning" => "Bathing",
            "petting" => "Being petted!",
            "walking" => "Wandering",
            _ => "Chilling"
        };
        sb.AppendLine($"[bold]{stateDisplay}[/]");
        sb.AppendLine($"[dim]{Markup.Escape(state.CurrentActivity)}[/]");
        sb.AppendLine($"[dim]@ {Markup.Escape(state.CurrentLocation)}[/]");

        return new Markup(sb.ToString());
    }

    /// <summary>
    /// Get emotion closeup face for sidebar (matching Python's 5-line format).
    /// </summary>
    private string[] GetEmotionCloseup(Duck.MoodState mood)
    {
        return mood switch
        {
            Duck.MoodState.Ecstatic => new[] {
                "           !! ",
                "  (★      ★)  ",
                "              ",
                "      >       ",
                "              "
            },
            Duck.MoodState.Happy => new[] {
                "              ",
                "  (^      ^)  ",
                "              ",
                "      >       ",
                "              "
            },
            Duck.MoodState.Content => new[] {
                "            ~ ",
                "  (-      -)  ",
                "              ",
                "      >       ",
                "              "
            },
            Duck.MoodState.Grumpy => new[] {
                "         hmph ",
                "  (>      <)  ",
                "              ",
                "      >       ",
                "              "
            },
            Duck.MoodState.Sad => new[] {
                "            · ",
                "  (;      ;)  ",
                "              ",
                "      >       ",
                "              "
            },
            Duck.MoodState.Miserable => new[] {
                "          · · ",
                "  (T      T)  ",
                "              ",
                "      >       ",
                "              "
            },
            _ => new[] {
                "              ",
                "  (o      o)  ",
                "              ",
                "      >       ",
                "              "
            }
        };
    }

    /// <summary>
    /// Build a need line with color-coded bar matching Python.
    /// </summary>
    private string BuildNeedLine(string name, float value)
    {
        var bar = BuildColoredNeedBar(value, 8);
        var pct = $"{(int)value}%";
        return $"{name}{bar} {pct}";
    }

    /// <summary>
    /// Build color-coded progress bar matching Python's style.
    /// Value >= 70: green (full block)
    /// Value >= 40: yellow (dark shade)
    /// Value >= 20: bright red (medium shade)
    /// Value &lt; 20: red (light shade)
    /// </summary>
    private string BuildColoredNeedBar(float value, int width)
    {
        var filled = (int)((value / 100f) * width);
        var empty = width - filled;
        
        char barChar;
        string color;
        
        if (value >= 70)
        {
            barChar = BarChars.Full;
            color = "green";
        }
        else if (value >= 40)
        {
            barChar = BarChars.High;
            color = "yellow";
        }
        else if (value >= 20)
        {
            barChar = BarChars.Med;
            color = "red";
        }
        else
        {
            barChar = BarChars.Low;
            color = "red";
        }
        
        var barContent = new string(barChar, filled) + new string(' ', empty);
        // Use [[ and ]] to escape literal brackets, color markup is inside
        return $"[[[{color}]{Markup.Escape(barContent)}[/]]]";
    }

    private string BuildNeedBar(float value, string color)
    {
        const int barWidth = 8;
        var filled = (int)((value / 100f) * barWidth);
        var empty = barWidth - filled;
        // Use pipe characters instead of brackets to avoid escaping issues
        return $"|[{color}]{new string('█', filled)}[/]{new string(' ', empty)}|";
    }

    private void RenderEnhancedBottomBar()
    {
        var y = Console.WindowHeight - 2;
        if (y < 0) y = 0;
        Console.SetCursorPosition(0, y);
        AnsiConsole.MarkupLine("[dim]                    Press (H) for help                    [/]");
    }

    private char GetGroundChar(int x, int y)
    {
        var chars = new[] { '.', ',', '\'', '`', ' ', ' ', ' ' };
        var hash = (x * 31 + y * 17) % chars.Length;
        return chars[hash];
    }

    private Markup BuildSidebar(DuckEntity duck, GameClock clock)
    {
        var mood = duck.GetMood();
        var needBars = duck.Needs.GetAllAsBars(8);

        var sb = new StringBuilder();
        
        // Face closeup
        var face = AsciiArt.GetCloseupFace(mood.State.ToString());
        foreach (var line in face)
            sb.AppendLine($"[yellow]{Markup.Escape(line)}[/]");

        sb.AppendLine();
        sb.AppendLine($"[bold]Mood:[/] {mood.State}");
        sb.AppendLine($"[dim]{Markup.Escape(mood.Description)}[/]");
        sb.AppendLine();
        
        // Needs bars
        sb.AppendLine("[bold]Needs:[/]");
        sb.AppendLine($"  Hunger:  [green]{Markup.Escape(needBars["hunger"])}[/]");
        sb.AppendLine($"  Energy:  [blue]{Markup.Escape(needBars["energy"])}[/]");
        sb.AppendLine($"  Fun:     [magenta]{Markup.Escape(needBars["fun"])}[/]");
        sb.AppendLine($"  Clean:   [cyan]{Markup.Escape(needBars["cleanliness"])}[/]");
        sb.AppendLine($"  Social:  [yellow]{Markup.Escape(needBars["social"])}[/]");
        
        sb.AppendLine();
        sb.AppendLine($"[dim]Stage: {duck.GetGrowthStageDisplay()}[/]");
        sb.AppendLine($"[dim]Age: {duck.GetAgeDays():F1} days[/]");
        sb.AppendLine($"[dim]Time: {clock.GetTimeOfDay()}[/]");

        return new Markup(sb.ToString());
    }

    /// <summary>
    /// Render the main game screen (legacy method for compatibility).
    /// </summary>
    public void RenderGame(DuckEntity duck, GameClock clock)
    {
        // Create a temporary GameState for backwards compatibility
        var tempState = new GameState { Duck = duck };
        RenderGameWithState(tempState);
    }

    private void RenderBottomBar(DuckEntity duck)
    {
        var y = Console.WindowHeight - 2;
        Console.SetCursorPosition(0, y);
        
        var controls = "(F)eed (P)lay (C)lean (E) Pet (Z) Sleep (T)alk | (H)elp (I)nventory (Q)uit";
        AnsiConsole.MarkupLine($"[dim]{controls}[/]");
    }

    private void RenderHelpOverlay()
    {
        var helpText = InputHandler.GetHelpText();
        var panel = new Panel(string.Join('\n', helpText))
            .Header("[bold yellow]Help[/]")
            .Border(BoxBorder.Double)
            .BorderColor(Color.Yellow);

        // Center the panel
        var x = (Console.WindowWidth - 40) / 2;
        var y = (Console.WindowHeight - helpText.Length - 4) / 2;

        Console.SetCursorPosition(x, y);
        AnsiConsole.Write(panel);
    }

    private void RenderMessage(string message)
    {
        var y = Console.WindowHeight - 4;
        Console.SetCursorPosition(0, y);
        AnsiConsole.MarkupLine($"[bold green]>>> {Markup.Escape(message)}[/]");
    }
}
