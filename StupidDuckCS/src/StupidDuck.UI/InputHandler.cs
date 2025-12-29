namespace StupidDuck.UI;

/// <summary>
/// Game actions triggered by keyboard input.
/// </summary>
public enum GameAction
{
    None,
    Feed,
    Play,
    Clean,
    Pet,
    Sleep,
    Talk,
    Quit,
    ToggleHelp,
    ToggleInventory,
    ToggleStats,
    ToggleShop,
    ToggleCrafting,
    ToggleBuilding,
    ToggleAreas,
    ToggleGoals,
    ToggleMinigames,
    ToggleQuests,
    ToggleWeather,
    ToggleDebug,
    NavigateUp,
    NavigateDown,
    NavigateLeft,
    NavigateRight,
    Select,
    Cancel,
    Escape,
    Confirm
}

/// <summary>
/// Handles keyboard input and maps to game actions.
/// </summary>
public class InputHandler
{
    private static readonly Dictionary<ConsoleKey, GameAction> KeyMappings = new()
    {
        [ConsoleKey.F] = GameAction.Feed,
        [ConsoleKey.P] = GameAction.Play,
        [ConsoleKey.C] = GameAction.Clean,
        [ConsoleKey.E] = GameAction.Pet,
        [ConsoleKey.Z] = GameAction.Sleep,
        [ConsoleKey.T] = GameAction.Talk,
        [ConsoleKey.Q] = GameAction.Quit,
        [ConsoleKey.H] = GameAction.ToggleHelp,
        [ConsoleKey.I] = GameAction.ToggleInventory,
        [ConsoleKey.S] = GameAction.ToggleStats,
        [ConsoleKey.B] = GameAction.ToggleShop,
        [ConsoleKey.G] = GameAction.ToggleGoals,
        [ConsoleKey.M] = GameAction.ToggleMinigames,
        [ConsoleKey.O] = GameAction.ToggleQuests,
        [ConsoleKey.W] = GameAction.ToggleWeather,
        [ConsoleKey.UpArrow] = GameAction.NavigateUp,
        [ConsoleKey.DownArrow] = GameAction.NavigateDown,
        [ConsoleKey.LeftArrow] = GameAction.NavigateLeft,
        [ConsoleKey.RightArrow] = GameAction.NavigateRight,
        [ConsoleKey.Enter] = GameAction.Select,
        [ConsoleKey.Escape] = GameAction.Escape,
        [ConsoleKey.Spacebar] = GameAction.Confirm
    };

    /// <summary>
    /// Process a key press and return the corresponding action.
    /// </summary>
    public GameAction ProcessKey(ConsoleKeyInfo keyInfo)
    {
        if (KeyMappings.TryGetValue(keyInfo.Key, out var action))
            return action;

        // Check for letter keys with shift/ctrl modifiers
        if (keyInfo.Key == ConsoleKey.Oem3) // Backtick
            return GameAction.ToggleDebug;

        return GameAction.None;
    }

    /// <summary>
    /// Get help text for available controls.
    /// Note: Brackets escaped for Spectre.Console markup compatibility.
    /// </summary>
    public static string[] GetHelpText() => new[]
    {
        "═══════════ CONTROLS ═══════════",
        "",
        "[[F]] Feed     - Give bread to duck",
        "[[P]] Play     - Play with duck",
        "[[C]] Clean    - Clean the duck",
        "[[E]] Pet      - Pet the duck",
        "[[Z]] Sleep    - Put duck to bed",
        "[[T]] Talk     - Chat with duck",
        "",
        "[[I]] Inventory",
        "[[S]] Stats",
        "[[B]] Shop",
        "[[G]] Goals",
        "[[H]] Help     - Toggle this menu",
        "[[Q]] Quit     - Save and exit",
        "",
        "[[↑↓]] Navigate menus",
        "[[Enter]] Select",
        "[[Esc]] Close menu",
        "",
        "════════════════════════════════"
    };
}
