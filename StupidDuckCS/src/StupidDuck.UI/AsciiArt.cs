namespace StupidDuck.UI;

/// <summary>
/// ASCII art for duck visuals and UI elements.
/// </summary>
public static class AsciiArt
{
    // Box drawing characters
    public static readonly Dictionary<string, char> Box = new()
    {
        ["tl"] = '┌',
        ["tr"] = '┐',
        ["bl"] = '└',
        ["br"] = '┘',
        ["h"] = '─',
        ["v"] = '│',
        ["cross"] = '┼',
        ["t_down"] = '┬',
        ["t_up"] = '┴',
        ["t_right"] = '├',
        ["t_left"] = '┤'
    };

    // Double line box
    public static readonly Dictionary<string, char> BoxDouble = new()
    {
        ["tl"] = '╔',
        ["tr"] = '╗',
        ["bl"] = '╚',
        ["br"] = '╝',
        ["h"] = '═',
        ["v"] = '║'
    };

    // Basic duck ASCII art (facing right)
    public static readonly string[] DuckIdle = new[]
    {
        @"    __",
        @" __( o)>",
        @" \_____)",
        @"  `---'"
    };

    public static readonly string[] DuckIdleLeft = new[]
    {
        @"  __",
        @"<(o )__",
        @"(_____/",
        @" '---`"
    };

    public static readonly string[] DuckWalking = new[]
    {
        @"    __",
        @" __( o)>",
        @" \_____)",
        @"   / \"
    };

    public static readonly string[] DuckSleeping = new[]
    {
        @"   z z",
        @"  __(-)_",
        @" \______)",
        @"  `----'"
    };

    public static readonly string[] DuckHappy = new[]
    {
        @"    __",
        @" __( ^)>",
        @" \_____)",
        @"  `---'"
    };

    public static readonly string[] DuckSad = new[]
    {
        @"    __",
        @" __( ;)>",
        @" \_____)",
        @"  `---'"
    };

    public static readonly string[] DuckEating = new[]
    {
        @"    __",
        @" __( o)",
        @" \__v__)",
        @"  `---'"
    };

    public static readonly string[] DuckPlaying = new[]
    {
        @"    __  !",
        @" __( ^)>",
        @" \__~__)",
        @"  `~-~'"
    };

    // Close-up duck faces for emotions
    public static readonly Dictionary<string, string[]> CloseupFaces = new()
    {
        ["ecstatic"] = new[]
        {
            @"  ╭───────╮  ",
            @"  │ ^   ^ │  ",
            @"  │   >   │  ",
            @"  │  \_/  │  ",
            @"  ╰───────╯  "
        },
        ["happy"] = new[]
        {
            @"  ╭───────╮  ",
            @"  │ -   - │  ",
            @"  │   >   │  ",
            @"  │  \_/  │  ",
            @"  ╰───────╯  "
        },
        ["content"] = new[]
        {
            @"  ╭───────╮  ",
            @"  │ -   - │  ",
            @"  │   >   │  ",
            @"  │  ---  │  ",
            @"  ╰───────╯  "
        },
        ["grumpy"] = new[]
        {
            @"  ╭───────╮  ",
            @"  │ \   / │  ",
            @"  │   >   │  ",
            @"  │  ~~~  │  ",
            @"  ╰───────╯  "
        },
        ["sad"] = new[]
        {
            @"  ╭───────╮  ",
            @"  │ ;   ; │  ",
            @"  │   >   │  ",
            @"  │  /_\  │  ",
            @"  ╰───────╯  "
        },
        ["miserable"] = new[]
        {
            @"  ╭───────╮  ",
            @"  │ T   T │  ",
            @"  │   >   │  ",
            @"  │  /_\  │  ",
            @"  ╰───────╯  "
        }
    };

    // Title screen art
    public static readonly string[] TitleArt = new[]
    {
        @"  ╔═══════════════════════════════════════════════════════════╗",
        @"  ║                                                           ║",
        @"  ║      ██████╗██╗  ██╗███████╗███████╗███████╗███████╗      ║",
        @"  ║     ██╔════╝██║  ██║██╔════╝██╔════╝██╔════╝██╔════╝      ║",
        @"  ║     ██║     ███████║█████╗  █████╗  ███████╗█████╗        ║",
        @"  ║     ██║     ██╔══██║██╔══╝  ██╔══╝  ╚════██║██╔══╝        ║",
        @"  ║     ╚██████╗██║  ██║███████╗███████╗███████║███████╗      ║",
        @"  ║      ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚══════╝      ║",
        @"  ║                                                           ║",
        @"  ║            ████████╗██╗  ██╗███████╗                      ║",
        @"  ║               ██║   ██║  ██║██╔════╝                      ║",
        @"  ║               ██║   ███████║█████╗                        ║",
        @"  ║               ██║   ██╔══██║██╔══╝                        ║",
        @"  ║               ██║   ██║  ██║███████╗                      ║",
        @"  ║               ╚═╝   ╚═╝  ╚═╝╚══════╝                      ║",
        @"  ║                                                           ║",
        @"  ║           ██████╗ ██╗   ██╗ ██████╗██╗  ██╗               ║",
        @"  ║           ██╔══██╗██║   ██║██╔════╝██║ ██╔╝               ║",
        @"  ║           ██║  ██║██║   ██║██║     █████╔╝                ║",
        @"  ║           ██║  ██║██║   ██║██║     ██╔═██╗                ║",
        @"  ║           ██████╔╝╚██████╔╝╚██████╗██║  ██╗               ║",
        @"  ║           ╚═════╝  ╚═════╝  ╚═════╝╚═╝  ╚═╝               ║",
        @"  ║                                                           ║",
        @"  ║                       __                                  ║",
        @"  ║                    __( o)>                                ║",
        @"  ║                    \_____) ~quack~                        ║",
        @"  ║                     `---'                                 ║",
        @"  ║                                                           ║",
        @"  ╚═══════════════════════════════════════════════════════════╝"
    };

    // Mini duck for status bar
    public static string GetMiniDuck(bool facingRight = true) =>
        facingRight ? "(o)>" : "<(o)";

    /// <summary>
    /// Create a box around content.
    /// </summary>
    public static string[] CreateBox(string[] content, int width, string? title = null)
    {
        var lines = new List<string>();
        var innerWidth = width - 2;

        // Top border
        var topBorder = title != null
            ? $"{Box["tl"]}─ {title} {new string(Box["h"], innerWidth - title.Length - 3)}{Box["tr"]}"
            : $"{Box["tl"]}{new string(Box["h"], innerWidth)}{Box["tr"]}";
        lines.Add(topBorder);

        // Content
        foreach (var line in content)
        {
            var padded = line.Length > innerWidth
                ? line[..innerWidth]
                : line.PadRight(innerWidth);
            lines.Add($"{Box["v"]}{padded}{Box["v"]}");
        }

        // Bottom border
        lines.Add($"{Box["bl"]}{new string(Box["h"], innerWidth)}{Box["br"]}");

        return lines.ToArray();
    }

    /// <summary>
    /// Get duck art based on state.
    /// </summary>
    public static string[] GetDuckArt(string state, bool facingRight = true) => state switch
    {
        "sleeping" => DuckSleeping,
        "eating" => DuckEating,
        "playing" => DuckPlaying,
        "walking" => facingRight ? DuckWalking : DuckIdleLeft,
        "happy" => DuckHappy,
        "sad" => DuckSad,
        _ => facingRight ? DuckIdle : DuckIdleLeft
    };

    /// <summary>
    /// Get closeup face for mood.
    /// </summary>
    public static string[] GetCloseupFace(string mood)
    {
        var moodLower = mood.ToLower();
        return CloseupFaces.TryGetValue(moodLower, out var face) ? face : CloseupFaces["content"];
    }
}
