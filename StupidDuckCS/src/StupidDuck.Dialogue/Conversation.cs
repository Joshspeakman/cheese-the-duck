using DuckEntity = StupidDuck.Duck.Duck;

namespace StupidDuck.Dialogue;

/// <summary>
/// Handles conversation with the duck.
/// </summary>
public class ConversationSystem
{
    private static readonly Random Rng = new();

    // Simple response templates based on mood and keywords
    private static readonly Dictionary<string, string[]> MoodResponses = new()
    {
        ["ecstatic"] = new[]
        {
            "QUACK! *does a happy dance*",
            "*flaps wings excitedly* Quack quack!",
            "*waddles in circles* This is the BEST!",
            "Quaaaaack! *vibrating with joy*"
        },
        ["happy"] = new[]
        {
            "Quack! *happy tail waggle*",
            "*tilts head cheerfully* Quack~",
            "Quack quack! *waddles closer*",
            "*preens contentedly* Quack!"
        },
        ["content"] = new[]
        {
            "Quack. *nods*",
            "*blinks peacefully* Quack.",
            "Quack quack. *settles down*",
            "*calm stare* Quack."
        },
        ["grumpy"] = new[]
        {
            "*huffs* Quack.",
            "Quack! *turns away slightly*",
            "*ruffles feathers* Quaaack.",
            "*side-eye* Quack."
        },
        ["sad"] = new[]
        {
            "quack... *droops*",
            "*sighs* quack...",
            "*looks up with big sad eyes* quack",
            "...quack. *sniffles*"
        },
        ["miserable"] = new[]
        {
            "*barely audible* quack...",
            "*won't make eye contact* ...",
            "*curls up* quack...",
            "*shivering* q-quack..."
        }
    };

    private static readonly Dictionary<string, string[]> KeywordResponses = new()
    {
        ["hello"] = new[] { "Quack! *perks up*", "*waves wing* Quack!" },
        ["hi"] = new[] { "Quack! *perks up*", "*waves wing* Quack!" },
        ["love"] = new[] { "*blushes* Quack quack!", "*nuzzles* Quaaack~" },
        ["food"] = new[] { "*eyes widen* QUACK?!", "*drools* Quack quack quack!" },
        ["bread"] = new[] { "BREAD?! QUACK QUACK QUACK!", "*INTENSE STARING* QUACK!" },
        ["good"] = new[] { "*puffs up proudly* Quack!", "*happy wiggle* Quack~" },
        ["bad"] = new[] { "*droops* quack...", "*offended* QUACK!" },
        ["cute"] = new[] { "*blushes and hides face* q-quack...", "*proud pose* Quack!" },
        ["name"] = new[] { "Quack! That's me!", "*points to self* QUACK!" },
        ["play"] = new[] { "*bounces excitedly* QUACK QUACK!", "*zooms around* Quaaaack!" }
    };

    /// <summary>
    /// Generate a response to a message.
    /// </summary>
    public string GetResponse(DuckEntity duck, string message)
    {
        var mood = duck.GetMoodState().ToString().ToLower();
        var messageLower = message.ToLower();

        // Check for keyword matches
        foreach (var (keyword, responses) in KeywordResponses)
        {
            if (messageLower.Contains(keyword))
            {
                return responses[Rng.Next(responses.Length)];
            }
        }

        // Fall back to mood-based response
        if (MoodResponses.TryGetValue(mood, out var moodReplies))
        {
            return moodReplies[Rng.Next(moodReplies.Length)];
        }

        return "Quack! *tilts head*";
    }

    /// <summary>
    /// Get a random idle quack.
    /// </summary>
    public string GetIdleQuack(DuckEntity duck)
    {
        var mood = duck.GetMoodState().ToString().ToLower();
        var idleQuacks = new Dictionary<string, string[]>
        {
            ["ecstatic"] = new[] { "~quack~", "*hums happily*", "*does a little dance*" },
            ["happy"] = new[] { "quack!", "*waddles around*", "*looks content*" },
            ["content"] = new[] { "...", "*preens*", "*watches the clouds*" },
            ["grumpy"] = new[] { "*grumbles*", "*huffs*", "*taps foot*" },
            ["sad"] = new[] { "*sighs*", "*stares at ground*", "..." },
            ["miserable"] = new[] { "*shivering*", "*very quiet*", "*hiding*" }
        };

        if (idleQuacks.TryGetValue(mood, out var quacks))
        {
            return quacks[Rng.Next(quacks.Length)];
        }

        return "*blinks*";
    }
}
