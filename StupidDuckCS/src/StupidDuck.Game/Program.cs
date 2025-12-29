using Spectre.Console;
using StupidDuck.Game;

// Cheese the Duck - A Virtual Pet Game
// Ported from Python to C#

try
{
    AnsiConsole.MarkupLine("[yellow]Starting Cheese the Duck...[/]");
    
    using var game = new GameController();
    game.Start();
}
catch (Exception ex)
{
    AnsiConsole.WriteException(ex);
    Console.WriteLine("\nPress any key to exit...");
    Console.ReadKey();
}
