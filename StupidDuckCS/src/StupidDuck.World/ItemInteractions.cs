namespace StupidDuck.World;

public enum InteractionType { Play, Use, Splash, Ride, Sit, Sleep, Eat, Music, Climb, Hide, Admire }

public class InteractionResult
{
    public bool Success { get; set; }
    public string Message { get; set; } = "";
    public List<List<string>> AnimationFrames { get; set; } = new();
    public float Duration { get; set; }
    public Dictionary<string, int> Effects { get; set; } = new();
    public string? Sound { get; set; }
}

public class ItemInteraction
{
    public List<string> Commands { get; set; } = new();
    public InteractionType Type { get; set; }
    public List<string> Messages { get; set; } = new();
    public Dictionary<string, int> Effects { get; set; } = new();
    public string? Sound { get; set; }
    public Dictionary<string, string> EdgeCases { get; set; } = new();
}

public static class ItemInteractions
{
    private static readonly Random _random = new();

    public static Dictionary<string, ItemInteraction> Interactions { get; } = new()
    {
        ["toy_ball"] = new ItemInteraction
        {
            Commands = new() { "play with ball", "kick ball", "chase ball" },
            Type = InteractionType.Play,
            Messages = new()
            {
                "*pushes ball* Wheee!", "*chases ball around* Come back here!",
                "*kicks ball* GOAL! Wait, there's no goal...", "*nudges ball with beak* Roll roll roll!",
                "*accidentally sits on ball* ...oops"
            },
            Effects = new() { ["fun"] = 15, ["energy"] = -5 },
            Sound = "play",
            EdgeCases = new()
            {
                ["tired"] = "*yawn* Too tired to chase ball... *pushes weakly*",
                ["hungry"] = "*stomach growls* Ball... looks... round like bread?",
                ["sad"] = "*pushes ball* ...it keeps rolling away. Like my happiness."
            }
        },
        ["toy_blocks"] = new ItemInteraction
        {
            Commands = new() { "play with blocks", "stack blocks", "build blocks" },
            Type = InteractionType.Play,
            Messages = new()
            {
                "*stacks blocks carefully* Tower time!", "*KNOCKS OVER BLOCKS* Oops! ...that was on purpose.",
                "*builds elaborate structure* Architectural genius!", "*places block* One more... *falls* NOOO!"
            },
            Effects = new() { ["fun"] = 12 },
            Sound = "play"
        },
        ["toy_trumpet"] = new ItemInteraction
        {
            Commands = new() { "play trumpet", "honk trumpet", "make noise" },
            Type = InteractionType.Music,
            Messages = new()
            {
                "*HONK HONK* This is AMAZING!", "*jazz quacking intensifies*",
                "*plays a tune* I'm basically Mozart!", "*HONNNNNK* ...sorry neighbors!"
            },
            Effects = new() { ["fun"] = 10, ["social"] = 5 },
            Sound = "quack"
        },
        ["toy_skateboard"] = new ItemInteraction
        {
            Commands = new() { "ride skateboard", "skate", "do tricks" },
            Type = InteractionType.Ride,
            Messages = new()
            {
                "*kickflips* ...almost!", "*rolls around* Quack yeah! Radical!",
                "*attempts ollie* *falls off* That was... intentional.", "*cruises by* I'm a skating legend!"
            },
            Effects = new() { ["fun"] = 18, ["energy"] = -8 },
            Sound = "play",
            EdgeCases = new()
            {
                ["clumsy"] = "*immediately faceplants* I'm okay!",
                ["tired"] = "*sits on skateboard* This counts as skating, right?"
            }
        },
        ["toy_piano"] = new ItemInteraction
        {
            Commands = new() { "play piano", "make music", "compose" },
            Type = InteractionType.Music,
            Messages = new()
            {
                "*pecks keys* ♪♫ Masterpiece!", "*composes* This is called 'Bread in D Minor'",
                "*plays dramatic chord* DUN DUN DUNNN", "*gentle melody* So soothing..."
            },
            Effects = new() { ["fun"] = 12, ["social"] = 3 },
            Sound = "play"
        },
        ["toy_trampoline"] = new ItemInteraction
        {
            Commands = new() { "jump on trampoline", "bounce", "trampoline" },
            Type = InteractionType.Play,
            Messages = new()
            {
                "*BOING BOING* THIS IS THE BEST!", "*bouncing intensifies* HIGHER!",
                "*does flip* ...nailed it? Sort of?", "*bounces* I CAN TOUCH THE CLOUDS!"
            },
            Effects = new() { ["fun"] = 20, ["energy"] = -10 },
            Sound = "play",
            EdgeCases = new()
            {
                ["tired"] = "*weak bounce* *flops* I'll just... lie here.",
                ["full_stomach"] = "*bounces* Oh no my bread! *urp*"
            }
        },
        ["toy_slide"] = new ItemInteraction
        {
            Commands = new() { "go down slide", "slide", "climb slide" },
            Type = InteractionType.Climb,
            Messages = new()
            {
                "*slides down* WHEEEEE!", "*climbs up for another turn* Again! Again!",
                "*goes down backwards* I'm an innovator!", "*zooms down* That was SO FAST!"
            },
            Effects = new() { ["fun"] = 15, ["energy"] = -5 },
            Sound = "play"
        },
        ["toy_swing"] = new ItemInteraction
        {
            Commands = new() { "swing", "use swing", "swing set" },
            Type = InteractionType.Play,
            Messages = new()
            {
                "*swinging* Higher! HIGHER!", "*pumps legs* I can touch the clouds!",
                "*swings peacefully* So relaxing...", "*swings wildly* MAXIMUM VELOCITY!"
            },
            Effects = new() { ["fun"] = 15, ["energy"] = -3 },
            Sound = "play"
        },
        ["toy_sandbox"] = new ItemInteraction
        {
            Commands = new() { "play in sandbox", "dig sand", "build sandcastle" },
            Type = InteractionType.Play,
            Messages = new()
            {
                "*digs furiously* TREASURE! ...nope, just more sand.",
                "*makes sand castle* Architectural genius!",
                "*buries self* I am one with the sand.",
                "*digs hole* It's getting deeper! And deeper!"
            },
            Effects = new() { ["fun"] = 12, ["cleanliness"] = -8 },
            Sound = "play"
        },
        ["toy_boombox"] = new ItemInteraction
        {
            Commands = new() { "play boombox", "turn on music", "dance" },
            Type = InteractionType.Music,
            Messages = new()
            {
                "*turns on boombox* ♪♫ MUSIC TIME! ♫♪", "*dances to the beat* This is my JAM!",
                "*breakdances* ...sort of. Duck-style!", "*vibes* This beat is FIRE!"
            },
            Effects = new() { ["fun"] = 15, ["social"] = 5 },
            Sound = "play"
        },
        ["pool_kiddie"] = new ItemInteraction
        {
            Commands = new() { "swim in pool", "splash in pool", "go swimming" },
            Type = InteractionType.Splash,
            Messages = new()
            {
                "*splashes* WATER! GLORIOUS WATER!", "*paddles around* I'm a natural!",
                "*floats on back* This is the life...", "*dives under* Blub blub!"
            },
            Effects = new() { ["fun"] = 20, ["cleanliness"] = 10, ["energy"] = -5 },
            Sound = "splash"
        },
        ["pool_large"] = new ItemInteraction
        {
            Commands = new() { "swim in pool", "dive in pool", "cannonball" },
            Type = InteractionType.Splash,
            Messages = new()
            {
                "*dives in* CANNONBALL!", "*swims laps* I'm an athlete!",
                "*floats majestically* Born for this!", "*does synchronized swimming alone* TA-DA!"
            },
            Effects = new() { ["fun"] = 25, ["cleanliness"] = 15, ["energy"] = -8 },
            Sound = "splash"
        },
        ["fountain_small"] = new ItemInteraction
        {
            Commands = new() { "drink from fountain", "splash in fountain", "use fountain" },
            Type = InteractionType.Splash,
            Messages = new()
            {
                "*drinks from fountain* Refreshing!", "*splashes face* Ahh, so nice!",
                "*watches water* So peaceful...", "*sticks head in* BLOOOP!"
            },
            Effects = new() { ["fun"] = 8, ["hunger"] = 5 },
            Sound = "splash"
        },
        ["pond"] = new ItemInteraction
        {
            Commands = new() { "swim in pond", "float in pond", "go to pond" },
            Type = InteractionType.Splash,
            Messages = new()
            {
                "*happy duck noises* HOME!", "*floats peacefully* This is where I belong...",
                "*dives for imaginary fish* Gotcha! ...nothing.", "*paddles in circles* Round and round!"
            },
            Effects = new() { ["fun"] = 20, ["cleanliness"] = 10, ["energy"] = 5 },
            Sound = "splash"
        },
        ["sprinkler"] = new ItemInteraction
        {
            Commands = new() { "run through sprinkler", "play in sprinkler", "get wet" },
            Type = InteractionType.Splash,
            Messages = new()
            {
                "*runs through sprinkler* WHEEE!", "*gets soaked* Worth it!",
                "*dances in water* LA LA LA!", "*jumps through repeatedly* AGAIN!"
            },
            Effects = new() { ["fun"] = 15, ["cleanliness"] = 8, ["energy"] = -5 },
            Sound = "splash"
        },
        ["hot_tub"] = new ItemInteraction
        {
            Commands = new() { "get in hot tub", "relax in hot tub", "soak" },
            Type = InteractionType.Splash,
            Messages = new()
            {
                "*relaxes* Ahhhh... this is AMAZING!", "*bubbles* The bubbles! SO MANY BUBBLES!",
                "*soaks* I could stay here forever...",
                "*steam rises* I'm like a soup... wait, that's concerning."
            },
            Effects = new() { ["fun"] = 15, ["energy"] = 10, ["cleanliness"] = 5 },
            Sound = "splash"
        },
        ["chair_wood"] = new ItemInteraction
        {
            Commands = new() { "sit on chair", "rest on chair", "sit down" },
            Type = InteractionType.Sit,
            Messages = new()
            {
                "*sits* Ahh, perfect.", "*lounges* This is the life.",
                "*swings legs* La la la~", "*sits regally* Throne acquired."
            },
            Effects = new() { ["energy"] = 5 }
        },
        ["bed"] = new ItemInteraction
        {
            Commands = new() { "sleep in bed", "rest in bed", "take a nap", "lie down" },
            Type = InteractionType.Sleep,
            Messages = new()
            {
                "*flops on bed* SO COMFY!", "*snuggles in* zzz...",
                "*starfishes* Maximum comfort achieved.", "*burrows under covers* Goodnight world!"
            },
            Effects = new() { ["energy"] = 20 },
            Sound = "sleep"
        },
        ["hammock"] = new ItemInteraction
        {
            Commands = new() { "rest in hammock", "swing in hammock", "nap in hammock" },
            Type = InteractionType.Sleep,
            Messages = new()
            {
                "*sways gently* This is paradise...",
                "*falls asleep* zzz... *almost falls out* GAH!",
                "*relaxes* Nothing to do... nowhere to be..."
            },
            Effects = new() { ["energy"] = 15, ["fun"] = 5 }
        },
        ["disco_ball"] = new ItemInteraction
        {
            Commands = new() { "dance under disco ball", "party time" },
            Type = InteractionType.Play,
            Messages = new()
            {
                "*disco dancing* SATURDAY NIGHT FEVER!",
                "*struts* I'm a dancing MACHINE!",
                "*sparkles* Look at those lights!"
            },
            Effects = new() { ["fun"] = 15, ["social"] = 5 }
        },
        ["campfire"] = new ItemInteraction
        {
            Commands = new() { "sit by campfire", "warm up", "roast marshmallows" },
            Type = InteractionType.Sit,
            Messages = new()
            {
                "*warms wings* Cozy~", "*stares at flames* So mesmerizing...",
                "*pretends to roast marshmallow* S'mores time!"
            },
            Effects = new() { ["energy"] = 5, ["fun"] = 8 },
            EdgeCases = new() { ["cold"] = "*hugs fire* WARMTH! PRECIOUS WARMTH!" }
        },
        ["frisbee"] = new ItemInteraction
        {
            Commands = new() { "throw frisbee", "play frisbee", "catch frisbee" },
            Type = InteractionType.Play,
            Messages = new()
            {
                "*throws frisbee* ...and catches it! Wait, how?",
                "*chases frisbee* Got it! Got it! Almost!",
                "*frisbee bonks head* Ow! Worth it!",
                "*does trick throw* I'm a frisbee LEGEND!"
            },
            Effects = new() { ["fun"] = 15, ["energy"] = -8 }
        },
        ["kite"] = new ItemInteraction
        {
            Commands = new() { "fly kite", "play with kite" },
            Type = InteractionType.Play,
            Messages = new()
            {
                "*runs with kite* FLY! FLY!", "*kite soars* I made it FLY!",
                "*kite crashes* ...gravity wins again.", "*watches kite dance* So pretty up there!"
            },
            Effects = new() { ["fun"] = 15, ["energy"] = -5 },
            EdgeCases = new() { ["no_wind"] = "*waves kite sadly* Need more wind..." }
        },
        ["drums"] = new ItemInteraction
        {
            Commands = new() { "play drums", "drum solo" },
            Type = InteractionType.Music,
            Messages = new()
            {
                "*BANG BANG BANG* ROCK AND ROLL!", "*epic drum solo* FEEL THE RHYTHM!",
                "*tap tap tap* Subtle. Artistic.", "*crashes cymbals* WHAT A FINALE!"
            },
            Effects = new() { ["fun"] = 15, ["social"] = 5 }
        },
        ["telescope"] = new ItemInteraction
        {
            Commands = new() { "look through telescope", "stargaze", "use telescope" },
            Type = InteractionType.Use,
            Messages = new()
            {
                "*peers through telescope* I can see the MOON!",
                "*searches sky* Looking for the Bread Galaxy...",
                "*spots star* I'm naming that one 'Quacky'!",
                "*gazes at stars* So many worlds out there..."
            },
            Effects = new() { ["fun"] = 10 },
            EdgeCases = new() { ["day"] = "*looks at sun* OW! Okay don't do that." }
        },
        ["easel"] = new ItemInteraction
        {
            Commands = new() { "paint", "draw", "use easel" },
            Type = InteractionType.Use,
            Messages = new()
            {
                "*paints masterpiece* Art! ART!", "*draws self-portrait* Stunning. Magnificent.",
                "*splashes colors* Abstract expressionism!", "*careful brushstrokes* My magnum opus!"
            },
            Effects = new() { ["fun"] = 12 }
        },
        ["water_slide"] = new ItemInteraction
        {
            Commands = new() { "go down water slide", "slide", "whoosh" },
            Type = InteractionType.Splash,
            Messages = new()
            {
                "*WHOOOOSH* AMAZING!", "*zooms down* FASTER! FASTER!",
                "*splashes at bottom* Perfect landing!", "*slides again* One more time! And again!"
            },
            Effects = new() { ["fun"] = 25, ["cleanliness"] = 5, ["energy"] = -8 }
        },
        ["mirror"] = new ItemInteraction
        {
            Commands = new() { "look in mirror", "admire self" },
            Type = InteractionType.Admire,
            Messages = new()
            {
                "*poses* Looking GOOD!", "*makes faces* Majestic. Stunning.",
                "*preens feathers* Photo ready!", "*winks at reflection* Hey good looking!"
            },
            Effects = new() { ["fun"] = 8 }
        },
        ["chair_throne"] = new ItemInteraction
        {
            Commands = new() { "sit on throne", "be king" },
            Type = InteractionType.Sit,
            Messages = new()
            {
                "*sits majestically* BOW TO ME!", "*adjusts crown* King of the ducks!",
                "*waves regally* Hello, subjects!", "*decrees* More bread for everyone!"
            },
            Effects = new() { ["energy"] = 8, ["fun"] = 10 }
        }
    };

    public static Dictionary<string, List<List<string>>> Animations { get; } = new()
    {
        ["toy_ball"] = new()
        {
            new() { "        O  ", "   __  /   ", "  (o )>    ", "  /|\\|     ", " (_) (_)   " },
            new() { "          O", "   __   / ", "  (o )>/  ", "  /|\\|    ", " (_)  (_) " },
            new() { "   __  O", "  (^o)>|", "  /|\\|  ", " (_)(_) " }
        },
        ["pool_kiddie"] = new()
        {
            new() { "   __      ", "  (o )>    ", " /|\\|      ", " (__)  [~] " },
            new() { "   SPLASH! ", "  * (oo) * ", " *  ~~   * ", "  [~~~~~~] " },
            new() { "   __      ", " ~(^o)>~   ", "  [~~~~~~] " }
        },
        ["toy_trampoline"] = new()
        {
            new() { "   __    ", "  (o )>  ", " /|\\|    ", " [====]  ", "  \\  /   " },
            new() { "  (^o)>  ", " /|\\|    ", "  WHEEE! ", "         ", " [====]  " },
            new() { "   __    ", "  (oo)>  ", " [====]  ", "  \\  /   " }
        }
    };

    public static ItemInteraction? GetInteraction(string itemId) =>
        Interactions.TryGetValue(itemId, out var interaction) ? interaction : null;

    public static List<string> GetInteractionCommands(string itemId) =>
        Interactions.TryGetValue(itemId, out var interaction) ? interaction.Commands : new();

    public static Dictionary<string, List<string>> GetAllInteractionCommands() =>
        Interactions.ToDictionary(kv => kv.Key, kv => kv.Value.Commands);

    public static InteractionResult? ExecuteInteraction(string itemId, Dictionary<string, int>? duckState = null)
    {
        if (!Interactions.TryGetValue(itemId, out var interaction)) return null;

        duckState ??= new();
        string? message = null;

        // Check edge cases
        if (duckState.GetValueOrDefault("energy") < 20 && interaction.EdgeCases.TryGetValue("tired", out var tired))
            message = tired;
        else if (duckState.GetValueOrDefault("hunger") < 20 && interaction.EdgeCases.TryGetValue("hungry", out var hungry))
            message = hungry;
        else if (duckState.GetValueOrDefault("fun") < 20 && interaction.EdgeCases.TryGetValue("sad", out var sad))
            message = sad;
        else if (duckState.GetValueOrDefault("social") < 20 && interaction.EdgeCases.TryGetValue("lonely", out var lonely))
            message = lonely;

        message ??= interaction.Messages[_random.Next(interaction.Messages.Count)];

        var animationFrames = Animations.TryGetValue(itemId, out var anim) 
            ? anim 
            : new List<List<string>> { new() { "   (o_)  ", "   /|\\|  " }, new() { "   (^o)  ", "   /|\\|  " } };

        return new InteractionResult
        {
            Success = true,
            Message = message,
            AnimationFrames = animationFrames,
            Duration = animationFrames.Count * 0.5f,
            Effects = interaction.Effects,
            Sound = interaction.Sound
        };
    }

    public static string? FindMatchingItem(string command, List<string> ownedItems)
    {
        var commandLower = command.ToLower().Trim();

        foreach (var itemId in ownedItems)
        {
            if (!Interactions.TryGetValue(itemId, out var interaction)) continue;

            foreach (var cmd in interaction.Commands)
                if (cmd.ToLower().Contains(commandLower) || commandLower.Contains(cmd.ToLower()))
                    return itemId;
        }

        // Partial name matching
        foreach (var itemId in ownedItems)
        {
            if (Interactions.ContainsKey(itemId) && commandLower.Contains(itemId.Replace("_", " ")))
                return itemId;
        }

        return null;
    }
}
