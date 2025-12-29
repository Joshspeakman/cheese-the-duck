using System.Diagnostics;
using Spectre.Console;
using StupidDuck.Core;
using StupidDuck.Duck;
using StupidDuck.UI;
using StupidDuck.Audio;
using StupidDuck.World;
using DuckEntity = StupidDuck.Duck.Duck;

namespace StupidDuck.Game;

/// <summary>
/// Game screen state enumeration.
/// </summary>
public enum ScreenState
{
    Init,
    Title,
    Playing,
    Paused,
    Menu
}

/// <summary>
/// Main game controller - manages game loop and state.
/// </summary>
public class GameController : IDisposable
{
    private readonly Renderer _renderer;
    private readonly InputHandler _inputHandler;
    private readonly SaveManager _saveManager;
    private readonly SoundEngine _soundEngine;
    private readonly World.GameState _gameState;

    private bool _running;
    private ScreenState _screenState = ScreenState.Init;
    private DateTime _lastTick;
    private DateTime _lastSave;
    private Dictionary<string, object> _statistics = new();
    private bool _disposed;

    // Timing constants
    private const float FrameTime = 1.0f / GameConfig.Fps;
    private const float SaveInterval = 30.0f; // Save every 30 seconds
    private const float TickInterval = 1.0f;  // Game tick every second

    public GameController()
    {
        _renderer = new Renderer();
        _inputHandler = new InputHandler();
        _saveManager = new SaveManager();
        _soundEngine = new SoundEngine();
        _gameState = new World.GameState();
        _lastTick = DateTime.Now;
        _lastSave = DateTime.Now;
    }

    /// <summary>
    /// Start the game.
    /// </summary>
    public void Start()
    {
        _running = true;

        // Check for existing save
        if (_saveManager.SaveExists())
        {
            LoadGame();
        }
        else
        {
            _screenState = ScreenState.Title;
        }

        RunGameLoop();
    }

    private void RunGameLoop()
    {
        var stopwatch = new Stopwatch();

        // Set up console - use alternate screen buffer to prevent scroll issues
        Console.Write("\x1b[?1049h");  // Switch to alternate screen buffer
        Console.Write("\x1b[?25l");    // Hide cursor
        Console.Clear();
        Console.CursorVisible = false;
        Console.TreatControlCAsInput = true;

        try
        {
            while (_running)
            {
                stopwatch.Restart();

                // Process input
                ProcessInput();

                // Update game state
                if (_screenState == ScreenState.Playing && _gameState.Duck != null)
                {
                    Update();
                }

                // Render
                Render();

                // Cap frame rate
                var elapsed = (float)stopwatch.Elapsed.TotalSeconds;
                if (elapsed < FrameTime)
                {
                    Thread.Sleep((int)((FrameTime - elapsed) * 1000));
                }
            }
        }
        finally
        {
            // Cleanup - restore normal screen buffer
            Console.Write("\x1b[?25h");    // Show cursor
            Console.Write("\x1b[?1049l");  // Switch back to main screen buffer
            Console.CursorVisible = true;
            Console.Clear();
        }
    }

    private void ProcessInput()
    {
        if (!Console.KeyAvailable)
            return;

        var keyInfo = Console.ReadKey(intercept: true);

        // Handle talk mode
        if (_renderer.IsTalking())
        {
            HandleTalkInput(keyInfo);
            return;
        }

        var action = _inputHandler.ProcessKey(keyInfo);
        HandleAction(action, keyInfo);
    }

    private void HandleTalkInput(ConsoleKeyInfo keyInfo)
    {
        switch (keyInfo.Key)
        {
            case ConsoleKey.Escape:
                _renderer.ToggleTalk();
                break;
            case ConsoleKey.Enter:
                var message = _renderer.GetTalkBuffer();
                if (!string.IsNullOrWhiteSpace(message))
                {
                    ProcessTalkMessage(message);
                }
                _renderer.ToggleTalk();
                _renderer.ClearTalkBuffer();
                break;
            case ConsoleKey.Backspace:
                _renderer.BackspaceTalk();
                break;
            default:
                if (!char.IsControl(keyInfo.KeyChar))
                {
                    _renderer.AddTalkChar(keyInfo.KeyChar);
                }
                break;
        }
    }

    private void HandleAction(GameAction action, ConsoleKeyInfo keyInfo)
    {
        if (_screenState == ScreenState.Title)
        {
            HandleTitleAction(action, keyInfo);
            return;
        }

        if (_screenState != ScreenState.Playing || _gameState.Duck == null)
            return;

        switch (action)
        {
            case GameAction.Feed:
                PerformInteraction("feed");
                break;
            case GameAction.Play:
                PerformInteraction("play");
                break;
            case GameAction.Clean:
                PerformInteraction("clean");
                break;
            case GameAction.Pet:
                PerformInteraction("pet");
                break;
            case GameAction.Sleep:
                PerformInteraction("sleep");
                break;
            case GameAction.Talk:
                _renderer.ToggleTalk();
                break;
            case GameAction.ToggleHelp:
                _renderer.ToggleHelp();
                break;
            case GameAction.ToggleInventory:
                _renderer.ToggleInventory();
                break;
            case GameAction.ToggleStats:
                _renderer.ToggleStats();
                break;
            case GameAction.Quit:
                SaveGame();
                _running = false;
                break;
        }
    }

    private void HandleTitleAction(GameAction action, ConsoleKeyInfo keyInfo)
    {
        switch (keyInfo.Key)
        {
            case ConsoleKey.N:
                StartNewGame();
                break;
            case ConsoleKey.L:
                if (_saveManager.SaveExists())
                    LoadGame();
                else
                    _renderer.ShowMessage("No save file found!");
                break;
            case ConsoleKey.Q:
                _running = false;
                break;
        }
    }

    private void StartNewGame()
    {
        // Prompt for duck name
        Console.Clear();
        AnsiConsole.MarkupLine("[yellow]Enter a name for your duck (or press Enter for 'Cheese'):[/]");
        Console.Write("> ");
        
        var name = Console.ReadLine();
        if (string.IsNullOrWhiteSpace(name))
            name = GameConfig.DefaultDuckName;

        _gameState.Duck = DuckEntity.CreateNew(name);
        _screenState = ScreenState.Playing;
        
        _renderer.ShowMessage($"Welcome {_gameState.Duck.Name} to the world! ~quack~");
        SaveGame();
    }

    private void LoadGame()
    {
        var data = _saveManager.Load();
        if (data?.Duck == null)
        {
            _renderer.ShowMessage("Failed to load save file!");
            return;
        }

        _gameState.Duck = DuckEntity.FromSaveData(data.Duck);
        _screenState = ScreenState.Playing;

        // Calculate offline progression
        if (data.LastPlayed != null)
        {
            var offline = _gameState.Clock.CalculateOfflineTime(data.LastPlayed);
            if (offline.Hours > 0.01f)
            {
                var offlineMinutes = offline.Minutes * offline.DecayMultiplier;
                _gameState.Duck.Update(offlineMinutes);
                _renderer.ShowMessage($"Welcome back! {_gameState.Duck.Name} missed you for {_gameState.Clock.FormatDuration(offline.Hours)}");
            }
        }
    }

    private void SaveGame()
    {
        if (_gameState.Duck == null)
            return;

        var data = new GameSaveData
        {
            Duck = _gameState.Duck.ToSaveData(),
            LastPlayed = _gameState.Clock.Timestamp,
            Statistics = new GameStatistics()
        };

        if (_saveManager.Save(data))
        {
            _lastSave = DateTime.Now;
        }
    }

    private void PerformInteraction(string interaction)
    {
        if (_gameState.Duck == null)
            return;

        var result = _gameState.Duck.Interact(interaction);
        _renderer.DuckPosition.SetState(interaction, 2.0f);

        var messages = new Dictionary<string, string>
        {
            ["feed"] = $"You fed {_gameState.Duck.Name}! *munch munch*",
            ["play"] = $"You played with {_gameState.Duck.Name}! *wheee!*",
            ["clean"] = $"You cleaned {_gameState.Duck.Name}! *splash*",
            ["pet"] = $"You petted {_gameState.Duck.Name}! *happy quack*",
            ["sleep"] = $"{_gameState.Duck.Name} is taking a nap... *zzz*"
        };

        if (messages.TryGetValue(interaction, out var message))
            _renderer.ShowMessage(message);
    }

    private void ProcessTalkMessage(string message)
    {
        if (_gameState.Duck == null)
            return;

        // Simple response for now (LLM integration can be added)
        var responses = new[]
        {
            "Quack! *tilts head*",
            "Quack quack! *waddles excitedly*",
            "*blinks curiously*",
            "Quaaack! *flaps wings*",
            "*stares at you with beady eyes*"
        };

        var rng = new Random();
        var response = responses[rng.Next(responses.Length)];
        _renderer.ShowMessage($"{_gameState.Duck.Name}: {response}");
    }

    private void Update()
    {
        if (_gameState.Duck == null)
            return;

        var now = DateTime.Now;
        var deltaSeconds = (float)(now - _lastTick).TotalSeconds;
        _lastTick = now;

        // Update duck needs (convert to minutes)
        var deltaMinutes = _gameState.Clock.GetDeltaMinutes(deltaSeconds);
        _gameState.Duck.Update(deltaMinutes);

        // Update game systems
        _gameState.Weather.Update();
        _gameState.Friends.Update(
            _renderer.DuckPosition.X, 
            _renderer.DuckPosition.Y,
            _renderer.DuckPosition.FieldWidth,
            _renderer.DuckPosition.FieldHeight
        );

        // Update renderer animations
        _renderer.Update(deltaSeconds);

        // Check for random events
        var evt = _gameState.Events.CheckForEvent();
        if (evt != null)
        {
            _renderer.ShowMessage($"{evt.Title}: {evt.Description}");
            // Apply event effects
            if (evt.Effects != null)
            {
                foreach (var (need, change) in evt.Effects)
                    _gameState.Duck.Needs.ApplyChange(need, change);
            }
        }

        // Auto-save periodically
        if ((now - _lastSave).TotalSeconds > SaveInterval)
        {
            SaveGame();
        }
    }

    private void Render()
    {
        switch (_screenState)
        {
            case ScreenState.Title:
                _renderer.RenderTitleScreen();
                break;
            case ScreenState.Playing when _gameState.Duck != null:
                _renderer.RenderGameWithState(_gameState);
                break;
        }
    }

    public void Dispose()
    {
        if (_disposed)
            return;

        _disposed = true;
        SaveGame();
        _soundEngine.Dispose();
    }
}
