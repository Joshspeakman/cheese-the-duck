namespace StupidDuck.World;

public static class DuckFacts
{
    private static readonly Random _random = new();

    public static List<string> Facts { get; } = new()
    {
        "Cheese once forgot which end of the bread to eat. He still hasn't figured it out.",
        "Cheese got lost in a straight hallway. Twice. The same hallway.",
        "Cheese once tried to fight his own reflection. The reflection won.",
        "Cheese thinks the moon is a very large crumb. No one has corrected him.",
        "Cheese once walked into a glass door, apologized to it, then did it again.",
        "Cheese has forgotten his own name mid-introduction. Multiple times.",
        "Cheese once spent three hours trying to befriend a statue. He still waves at it.",
        "Cheese believes he's invisible when he closes his eyes.",
        "Cheese once got scared by his own sneeze and hasn't fully recovered.",
        "Cheese tried to swim in a puddle and got confused when it wasn't deep enough.",
        "Cheese has walked into the same wall seventeen times. He blames the wall.",
        "Cheese once forgot how to sit down halfway through sitting down.",
        "Cheese tried to intimidate a butterfly. The butterfly was not intimidated.",
        "Cheese gets lost going to places he's been a hundred times. Every. Single. Time.",
        "Cheese once mistook a pinecone for a friend. He named it Gerald.",
        "Cheese thinks clouds are just sky bread. He's been disappointed every time.",
        "Cheese believes his reflection is a very rude duck who copies him.",
        "Cheese once tried to fly by just believing really hard. Gravity disagreed.",
        "Cheese has never successfully predicted where his next step will go.",
        "Cheese forgets he can swim. In the middle of swimming. Regularly.",
        "Cheese once chased his own tail for so long he forgot why he started.",
        "Cheese has never successfully caught a bug. The bugs feel bad for him at this point.",
        "Cheese thinks 'Tuesday' is a type of weather.",
        "Cheese regularly walks the wrong direction and calls it 'the scenic route.'",
        "Cheese once forgot what bread was while eating bread.",
        "Cheese has been startled by the same leaf eight days in a row.",
        "Cheese once tried to drink water and forgot how. He eventually remembered.",
        "Cheese thinks he's being sneaky when he waddles loudly while making eye contact.",
        "Cheese has never won a game, but insists he's 'letting everyone else have fun.'",
        "Cheese gets confused by stairs. Not going up them. Just... stairs existing.",
        "Cheese once forgot mid-quack what he was quacking about.",
        "Cheese thinks naps are a competitive sport. He's undefeated at losing.",
        "Cheese tried to make friends with his own shadow. The shadow left.",
        "Cheese regularly forgets he has wings. And feet. And sometimes a head.",
        "Cheese is the reason 'duck-brained' is an insult. He considers it a compliment.",
        "Cheese was born confused and has maintained that energy ever since.",
        "Cheese once asked a rock for directions. He's still waiting for a response.",
        "Cheese believes he invented waddling. He did not.",
        "Cheese once got his head stuck in a bush. He blamed the bush.",
        "Cheese thinks he's a natural leader. He has never successfully led anything.",
        "Cheese once tried to count to ten. He got to seven and celebrated.",
        "Cheese thinks alphabetical order is just a suggestion.",
        "Cheese once forgot what feet were. While standing.",
        "Cheese believes rain is the sky crying because it misses him.",
        "Cheese once tried to high-five a fish. It went as expected.",
        "Cheese thinks echoes are other ducks agreeing with him.",
        "Cheese once tried to read a book upside down for an hour before giving up.",
        "Cheese believes he speaks fluent human. He does not.",
        "Cheese once asked a tree for its opinion. The tree did not respond.",
        "Cheese thinks gravity is a personal attack against him specifically.",
        "Cheese thinks doors are just very polite walls.",
        "Cheese believes wind is just the air showing off.",
        "Cheese thinks cold is just spicy air.",
        "Cheese believes feathers are just fancy fur.",
        "Cheese thinks every day is his birthday. It never is.",
        "Cheese has never remembered a face. Including his own.",
        "Cheese once dreamed he was awake. He was right.",
        "Cheese believes being awake is overrated.",
        "Cheese thinks 'five more minutes' means an hour.",
        "Cheese believes mornings should be illegal.",
        "Cheese thinks rules are just suggestions for other ducks.",
        "Cheese believes he's famous. He is not.",
        "Cheese thinks he's very tall. He is not.",
        "Cheese believes he's intimidating. No one is intimidated.",
        "Cheese thinks he has excellent memory. He forgot that thought.",
        "Cheese is Cheese. That's the most important fact of all."
    };

    public static List<string> BirthdayMessages { get; } = new()
    {
        "Happy Hatch Day, {name}! You've been the best friend for {age} days!",
        "{name}'s Hatch Day! {age} days of wonderful memories together!",
        "Celebrate good times! It's {name}'s {age}-day Hatch Day anniversary!",
        "Happy {age} days, {name}! Here's to many more adventures!",
        "{age} days of quacking good times! Happy Hatch Day, {name}!"
    };

    public static Dictionary<int, string> WeeklyMilestones { get; } = new()
    {
        [7] = "One week together! {name} loves having you around!",
        [14] = "Two weeks of friendship! {name} is so happy!",
        [21] = "Three weeks! {name} has learned so much from you!",
        [28] = "Four weeks! That's almost a month of memories!",
        [30] = "One whole month together! {name} is honored!",
        [60] = "Two months! {name} considers you family now!",
        [90] = "Three months! Quarter-year of quacking joy!",
        [100] = "100 days! A century of love and care!",
        [180] = "Half a year! {name} can't imagine life without you!",
        [365] = "ONE WHOLE YEAR! {name} is the luckiest duck ever!"
    };

    public static List<string> HappyResponses { get; } = new()
    {
        "*wiggles smugly* Yeah, life's pretty good. For once.",
        "*does a little dance* Don't stare. Or DO stare. I'm fabulous.",
        "*preens feathers* Lookin' good and I KNOW it.",
        "*splashes aggressively* WHEEE! Get SOAKED, world!",
        "*content but suspicious duck noises* This is too good. What's the catch?",
        "*quacks triumphantly* Another day of being PEAK duck!",
        "*stretches wings* Today doesn't suck. Shocking, I know.",
        "*happy nibble* This is as good as it gets. Which is pretty good, actually."
    };

    public static List<string> HungryResponses { get; } = new()
    {
        "*stomach rumbles LOUDLY* Is it snack time or am I DYING?!",
        "*eyes you with accusation* You're holding out on me. I can TELL.",
        "*stomach sounds like a war cry* QUACK?! FOOD?! NOW?!",
        "*stares intensely* You know what would be nice? BREAD. Immediately.",
        "*drools dramatically* Bread? Bread?! I'm WASTING AWAY here!",
        "*wistful yet aggressive quack* Remember when I wasn't starving? Good times."
    };

    public static List<string> TiredResponses { get; } = new()
    {
        "*yawns aggressively* So... sleepy... leave me ALONE...",
        "*droopy eyes* Just five more hours... I mean minutes...",
        "*slow blink* zzz... huh? I wasn't sleeping. I was resting my EYES.",
        "*rests head on wing* Wake me when something interesting happens. So... never.",
        "*drowsy, irritated quack* What do you WANT?",
        "*nods off* Oops. Don't care. Bye."
    };

    public static List<string> LonelyResponses { get; } = new()
    {
        "*looks around* ...Where IS everyone? Not that I CARE.",
        "*quiet, bitter quack* Oh sure, just LEAVE. Everyone does.",
        "*waddles closer* ...Fine. You can stay. I GUESS.",
        "*grumpy peep* About TIME you showed up.",
        "*trying not to look relieved* Oh. It's you. ...Whatever."
    };

    public static List<string> PlayfulResponses { get; } = new()
    {
        "*bounces chaotically* PLAY TIME! FINALLY! LET'S CAUSE PROBLEMS!",
        "*chases own tail* I'M GONNA CATCH IT THIS TIME! ...Okay maybe not.",
        "*zooms dangerously* WHEEEEE! OUTTA MY WAY!",
        "*aggressive quack* Tag! You're it! NO TAG-BACKS!",
        "*brings you something weird* Play? Play! Don't ask where I found this!"
    };

    public static List<string> DirtyResponses { get; } = new()
    {
        "*looks at muddy feathers* Yeah? And? I'm a DUCK.",
        "*defiant quack* I may have gotten messy. WORTH IT.",
        "*shakes feathers at you* Mud is basically a spa treatment. Look it up.",
        "*covered in who-knows-what* What are you, the hygiene police? Back off."
    };

    public static Dictionary<string, string> ItemDescriptions { get; } = new()
    {
        ["toy_ball"] = "A bouncy ball that never stops rolling! Perfect for duck soccer.",
        ["toy_boombox"] = "A retro boombox that plays funky tunes. Very groovy!",
        ["toy_rubber_duck"] = "It's a duck! Wait... is this like a duck action figure?",
        ["toy_squeaky"] = "SQUEAK! The most satisfying sound in the universe.",
        ["toy_feather_wand"] = "Wave it around and watch Cheese go wild!",
        ["hat_bow"] = "A cute bow that sits perfectly on a duck head.",
        ["hat_crown"] = "For the royal duck in your life. Quack quack, your majesty!",
        ["hat_party"] = "Every day is a party when you're a duck!",
        ["hat_wizard"] = "Grants +10 to magical quacking abilities.",
        ["hat_pirate"] = "Arrr! Captain Cheese reporting for duty!",
        ["bread"] = "The classic. The legend. The one and only BREAD.",
        ["premium_bread"] = "Artisan bread, baked with love and extra crumbs.",
        ["cake"] = "For special occasions! Or any occasion, really.",
        ["treats"] = "Yummy duck treats! Cheese's eyes light up!",
        ["nest_basic"] = "A cozy nest for afternoon naps.",
        ["nest_deluxe"] = "Extra fluffy! Five-star duck accommodation.",
        ["pond_mini"] = "A tiny pond for tiny splashes.",
        ["fountain"] = "So fancy! The water sparkles beautifully.",
        ["golden_crumb"] = "Legendary! They say it grants good luck!",
        ["treasure_map"] = "X marks the spot... but where?",
        ["lucky_charm"] = "A four-leaf clover encased in crystal.",
        ["rainbow_feather"] = "Shimmers with all the colors of the rainbow!"
    };

    public static string GetRandomFact() => Facts[_random.Next(Facts.Count)];

    public static BirthdayInfo GetBirthdayInfo(DateTime createdAt, string name = "Cheese")
    {
        var ageDays = (DateTime.Now - createdAt).Days;
        var isBirthday = DateTime.Now.Month == createdAt.Month && DateTime.Now.Day == createdAt.Day;

        string? milestone = null;
        if (WeeklyMilestones.TryGetValue(ageDays, out var m))
            milestone = m.Replace("{name}", name);

        int nextMilestone = 0;
        foreach (var days in WeeklyMilestones.Keys.OrderBy(k => k))
        {
            if (days > ageDays) { nextMilestone = days - ageDays; break; }
        }

        return new BirthdayInfo(ageDays, isBirthday, milestone, nextMilestone);
    }

    public static string GetBirthdayMessage(string name, int ageDays)
    {
        var msg = BirthdayMessages[_random.Next(BirthdayMessages.Count)];
        return msg.Replace("{name}", name).Replace("{age}", ageDays.ToString());
    }

    public static string GetMoodResponse(string moodState)
    {
        var responses = moodState.ToLower() switch
        {
            "ecstatic" or "happy" => HappyResponses,
            "hungry" => HungryResponses,
            "tired" => TiredResponses,
            "lonely" => LonelyResponses,
            "playful" => PlayfulResponses,
            "dirty" => DirtyResponses,
            "content" => new List<string> { "*gentle quack*", "*peaceful vibes*", "*content sigh*" },
            "neutral" => new List<string> { "*looks around*", "*mild quack*", "*casual waddle*" },
            "sad" => new List<string> { "*droopy*", "*quiet peep*", "*needs comfort*" },
            _ => new List<string> { "*quack*" }
        };
        return responses[_random.Next(responses.Count)];
    }

    public static string GetItemDescription(string itemId) =>
        ItemDescriptions.TryGetValue(itemId, out var desc) ? desc : "A mysterious item with unknown powers!";
}

public record BirthdayInfo(int AgeDays, bool IsBirthday, string? Milestone, int NextMilestoneDays);
