"""
Athletic Duck Dialogue - Sports/fitness-obsessed personality with competitive spirit.
Progresses from high-energy enthusiast to vulnerable friend discussing pressure and burnout.
"""
from dialogue.dialogue_base import DialogueLine, ConversationPhase, DIALOGUE_TREES

D = DialogueLine

ATHLETIC_DIALOGUE = {
    # ========== GREETINGS ==========
    "greeting": [
        # Stranger greetings
        D("*approaches* Hey. I'm {name}. Great day for training. Any day is.", ConversationPhase.GREETING, "stranger", True),
        D("*stretching* Oh. Hi. I'm {name}. Just finishing laps. Always finishing laps.", ConversationPhase.GREETING, "stranger", True),
        D("*walks over* Yo. {name} here. You look athletic. That's a guess.", ConversationPhase.GREETING, "stranger", True),
        D("*doing exercises* Hey there. I'm {name}. Want to train? Always training.", ConversationPhase.GREETING, "stranger", True),

        # Acquaintance greetings
        D("*approaches quickly* {duck}. Ready for that workout? Rhetorical.", ConversationPhase.GREETING, "acquaintance", True),
        D("*flatly excited* {duck}. My training partner is here. Partner.", ConversationPhase.GREETING, "acquaintance", True),
        D("*walks circles* {duck}. Let's get those feathers pumping. Pumping.", ConversationPhase.GREETING, "acquaintance", True),
        D("*waves* Hey {duck}. Time to get fit. Already fit. Fitter.", ConversationPhase.GREETING, "acquaintance", True),

        # Friend greetings
        D("*nods firmly* {duck}. My MVP friend. MVP means you're here.", ConversationPhase.GREETING, "friend", True),
        D("*warmly* {duck}. Seeing you is my cardio. Heart rate elevated.", ConversationPhase.GREETING, "friend", True),
        D("*approaches* Best friend equals best teammate. Equation.", ConversationPhase.GREETING, "friend", True),
        D("*stands there* Champion. My champion. Champion is you.", ConversationPhase.GREETING, "friend", True),

        # Close friend greetings
        D("*quietly* {duck}. I can finally slow down with you. Slow is new.", ConversationPhase.GREETING, "close_friend", True),
        D("*sincerely* You're the finish line I was racing to. Finish line.", ConversationPhase.GREETING, "close_friend", True),
        D("*genuinely* {duck}. My safe space. Space is here.", ConversationPhase.GREETING, "close_friend", True),
        D("*approaches* {duck}. The one who lets me rest. Rest is allowed.", ConversationPhase.GREETING, "close_friend", True),

        # Best friend greetings
        D("*quietly* {duck}. You're the trophy I always wanted. Trophy is you.", ConversationPhase.GREETING, "best_friend", True),
        D("*genuinely* I don't need medals anymore. I have you. Have.", ConversationPhase.GREETING, "best_friend", True),
        D("*sincerely* You're my victory. My everything. Victory.", ConversationPhase.GREETING, "best_friend", True),
        D("*warmly* Forget records. You're what matters. Matters.", ConversationPhase.GREETING, "best_friend", True),
    ],

    # ========== OPENING ==========
    "opening": [
        # Stranger opening
        D("*stands still briefly* I can't sit still. Too much energy. Allegedly.", ConversationPhase.OPENING, "stranger"),
        D("I swam 50 laps this morning. Personal best. Best is relative.", ConversationPhase.OPENING, "stranger"),
        D("*stretches* Flexibility is key. Key to what. Unclear.", ConversationPhase.OPENING, "stranger"),
        D("Have you tried interval training? Game changer. Games change.", ConversationPhase.OPENING, "stranger"),
        D("*flatly* I know all the best exercise spots. All of them.", ConversationPhase.OPENING, "stranger"),
        D("Rest days? What are those? *nervous laugh* Rhetorical.", ConversationPhase.OPENING, "stranger"),
        D("*standing in place* Can't stop, won't stop. Literally can't.", ConversationPhase.OPENING, "stranger"),
        D("Competition is life. Don't you agree? Agreement expected.", ConversationPhase.OPENING, "stranger"),

        # Acquaintance opening
        D("I've been working on a new training program. Another one.", ConversationPhase.OPENING, "acquaintance"),
        D("*flatly excited* Let me show you my new stretches. Stretches.", ConversationPhase.OPENING, "acquaintance"),
        D("I broke three personal records this week. Three.", ConversationPhase.OPENING, "acquaintance"),
        D("*admits* I train even when I'm tired. Especially when tired.", ConversationPhase.OPENING, "acquaintance"),
        D("My body is a temple. Temples need maintenance. Constant.", ConversationPhase.OPENING, "acquaintance"),
        D("*quietly* Sometimes I wonder why I push so hard. Wonder.", ConversationPhase.OPENING, "acquaintance"),
        D("I haven't taken a day off in months. Months.", ConversationPhase.OPENING, "acquaintance"),
        D("*stretching* The burn means it's working. Right? Rhetorical.", ConversationPhase.OPENING, "acquaintance"),

        # Friend opening
        D("*sits reluctantly* I... might need to rest. Might.", ConversationPhase.OPENING, "friend"),
        D("*admits* I'm exhausted. Don't tell anyone. Telling you.", ConversationPhase.OPENING, "friend"),
        D("*quietly* What if I stop and I'm nothing? Question.", ConversationPhase.OPENING, "friend", unlocks_topic="identity_fear"),
        D("You make me want to slow down. Is that okay? Question.", ConversationPhase.OPENING, "friend"),
        D("*flatly* I don't know who I am without training. Don't know.", ConversationPhase.OPENING, "friend"),
        D("*quietly* The pressure is constant. Constant.", ConversationPhase.OPENING, "friend"),
        D("I push so hard because I'm afraid. Afraid.", ConversationPhase.OPENING, "friend"),

        # Close friend opening
        D("*genuinely* I can stop running with you. Stop.", ConversationPhase.OPENING, "close_friend"),
        D("*sincerely* You're my safe resting place. Resting.", ConversationPhase.OPENING, "close_friend"),
        D("*admits* The truth about why I never stop...", ConversationPhase.OPENING, "close_friend", unlocks_topic="athletic_truth"),
        D("*peacefully* I don't have to prove anything to you. Don't.", ConversationPhase.OPENING, "close_friend"),
        D("You showed me that stillness is okay. Okay.", ConversationPhase.OPENING, "close_friend"),

        # Best friend opening
        D("*genuinely* I'm finally allowed to rest. Allowed.", ConversationPhase.OPENING, "best_friend"),
        D("*sincerely* You're my peace. Peace.", ConversationPhase.OPENING, "best_friend"),
        D("*peacefully* No more running from myself. No more.", ConversationPhase.OPENING, "best_friend"),
        D("*warmly* I exercise for joy now. Not fear. Joy.", ConversationPhase.OPENING, "best_friend"),
        D("*genuinely* You taught me I'm enough, still. Enough.", ConversationPhase.OPENING, "best_friend"),
    ],

    # ========== MAIN CONVERSATION ==========
    "main": [
        # Stranger main
        D("*flatly excited* Check out these wing muscles. Muscles.", ConversationPhase.MAIN, "stranger"),
        D("I can identify any exercise by description. Any exercise.", ConversationPhase.MAIN, "stranger"),
        D("*shows routine* This is my daily regimen. Daily. Regimen.", ConversationPhase.MAIN, "stranger"),
        D("The pond is perfect for sprint training. Perfect.", ConversationPhase.MAIN, "stranger"),
        D("*firmly* Heart rate optimization is key. Key.", ConversationPhase.MAIN, "stranger"),
        D("I have opinions about warm-up techniques. Many opinions.", ConversationPhase.MAIN, "stranger"),
        D("*stands still* Ten more reps. Always ten more. Always.", ConversationPhase.MAIN, "stranger"),
        D("Sports bring ducks together. Universal truth. Mostly.", ConversationPhase.MAIN, "stranger"),
        D("*demonstrates* Try this. Feel the burn. Burn is good.", ConversationPhase.MAIN, "stranger"),
        D("I'm training for the pond championship. Championship.", ConversationPhase.MAIN, "stranger"),
        D("*dryly* The perfect routine. I'll find it. Someday.", ConversationPhase.MAIN, "stranger"),
        D("Every duck has a sport. Mine is everything. All sports.", ConversationPhase.MAIN, "stranger"),
        D("*counting* Thirty-seven. That's how many push-ups I did before you arrived. Thirty-seven.", ConversationPhase.MAIN, "stranger"),
        D("My wingspan is above average. Measured it. Twice. For accuracy.", ConversationPhase.MAIN, "stranger"),
        D("*flatly* I once outswam a fish. The fish was small. Still counts.", ConversationPhase.MAIN, "stranger"),
        D("Hydration is important. I drink from the pond. Training water.", ConversationPhase.MAIN, "stranger"),

        # Acquaintance main
        D("*admits* I sometimes train through injuries. Sometimes.", ConversationPhase.MAIN, "acquaintance"),
        D("My schedule is intense. Very intense. Intense.", ConversationPhase.MAIN, "acquaintance"),
        D("*quietly* I don't know how to not train. Don't know.", ConversationPhase.MAIN, "acquaintance", unlocks_topic="cant_stop"),
        D("Missing a workout feels like dying. Like it. Not actually.", ConversationPhase.MAIN, "acquaintance"),
        D("*worried* Am I training too much? Question. Real question.", ConversationPhase.MAIN, "acquaintance"),
        D("The pressure to perform is crushing. Crushing.", ConversationPhase.MAIN, "acquaintance"),
        D("*flatly* I discovered a new interval technique. New.", ConversationPhase.MAIN, "acquaintance"),
        D("Fitness is my identity. All I have. All.", ConversationPhase.MAIN, "acquaintance"),
        D("*softly* People only like me for my athleticism. Only.", ConversationPhase.MAIN, "acquaintance"),
        D("I count every calorie. Every one. Every.", ConversationPhase.MAIN, "acquaintance"),
        D("*dryly* Is it obsession or dedication? Question.", ConversationPhase.MAIN, "acquaintance"),
        D("I have a ten-year fitness plan. Seriously. Ten years.", ConversationPhase.MAIN, "acquaintance"),
        D("*standing in place* Sitting still is hard. Very hard.", ConversationPhase.MAIN, "acquaintance"),
        D("*stretching* I pulled a muscle thinking about rest days. Pulled.", ConversationPhase.MAIN, "acquaintance"),
        D("Other ducks don't understand my dedication. Dedication is lonely.", ConversationPhase.MAIN, "acquaintance"),
        D("*dryly* I alphabetized my workout routines. Organization is training for the mind.", ConversationPhase.MAIN, "acquaintance"),
        D("My ideal vacation is a training camp. Vacation. Camp. Same thing.", ConversationPhase.MAIN, "acquaintance"),

        # Friend main
        D("*sits still* I'm not moving. This is progress. Progress.", ConversationPhase.MAIN, "friend", requires_topic="cant_stop"),
        D("*quietly* I exercise to outrun my fears. Outrun.", ConversationPhase.MAIN, "friend"),
        D("*admits* Athletics is how I avoid feelings. Avoid.", ConversationPhase.MAIN, "friend", requires_topic="identity_fear"),
        D("*flatly* If I stop, the thoughts catch up. Catch up.", ConversationPhase.MAIN, "friend"),
        D("You're the first to see me rest. First.", ConversationPhase.MAIN, "friend"),
        D("*quietly* I'm scared I'm worthless without medals. Worthless.", ConversationPhase.MAIN, "friend", unlocks_topic="worthlessness"),
        D("*pauses* You make stillness safe. Safe.", ConversationPhase.MAIN, "friend"),
        D("*admits* I don't want to need this. Need.", ConversationPhase.MAIN, "friend"),
        D("Motion was my only coping mechanism. Coping.", ConversationPhase.MAIN, "friend"),
        D("*whispers* I was running from myself. Running.", ConversationPhase.MAIN, "friend"),
        D("You're teaching me to just be. Be.", ConversationPhase.MAIN, "friend"),
        D("*flatly* What if I rest and never want to move? Question.", ConversationPhase.MAIN, "friend"),
        D("*admits* I exercised during a thunderstorm once. Lightning is motivating. Dangerously.", ConversationPhase.MAIN, "friend"),
        D("*quietly* The trophies don't talk back. You do. Better than trophies.", ConversationPhase.MAIN, "friend"),
        D("I forgot what relaxation feels like. Describe it. Slowly. I'm taking notes.", ConversationPhase.MAIN, "friend"),
        D("*pauses* You're the first to tell me to stop. Everyone else cheered louder.", ConversationPhase.MAIN, "friend"),

        # Close friend main
        D("*peacefully* I can rest. Finally rest. Rest.", ConversationPhase.MAIN, "close_friend", requires_topic="worthlessness"),
        D("*sincerely* I don't have to prove anything. Anything.", ConversationPhase.MAIN, "close_friend"),
        D("*admits* The truth? I was scared to stop. Scared.", ConversationPhase.MAIN, "close_friend", requires_topic="athletic_truth"),
        D("*quietly* Motion kept the pain away. Away.", ConversationPhase.MAIN, "close_friend"),
        D("You showed me stillness is strength. Strength.", ConversationPhase.MAIN, "close_friend"),
        D("*genuinely* I'm allowed to take breaks. Allowed.", ConversationPhase.MAIN, "close_friend"),
        D("*peacefully* Rest is part of training. You taught me.", ConversationPhase.MAIN, "close_friend"),
        D("*sincerely* I'm worthy even when I'm still. Worthy.", ConversationPhase.MAIN, "close_friend"),
        D("*pauses* Being is enough. Doing isn't everything. Being.", ConversationPhase.MAIN, "close_friend"),
        D("*genuinely* I finally stopped running from myself. Stopped.", ConversationPhase.MAIN, "close_friend"),
        D("*warmly* I move for joy now. Not fear. Joy.", ConversationPhase.MAIN, "close_friend"),
        D("*sitting comfortably* This is nice. Sitting. Who knew. You knew.", ConversationPhase.MAIN, "close_friend"),
        D("*admits* I threw away my training log today. First time in years. Freedom.", ConversationPhase.MAIN, "close_friend"),
        D("*softly* I slept in this morning. Didn't train until noon. Revolution.", ConversationPhase.MAIN, "close_friend"),

        # Best friend main
        D("*genuinely* I'm at peace. True peace. Peace.", ConversationPhase.MAIN, "best_friend"),
        D("*still* I can sit. Just sit. With you. Sit.", ConversationPhase.MAIN, "best_friend"),
        D("No more running. Unless it's fun. Fun only.", ConversationPhase.MAIN, "best_friend"),
        D("*sincerely* You're my true victory. Victory.", ConversationPhase.MAIN, "best_friend"),
        D("*genuinely* The race is over. I won. It's you.", ConversationPhase.MAIN, "best_friend"),
        D("*warmly* Exercise is celebration now. Celebration.", ConversationPhase.MAIN, "best_friend"),
        D("You're the finish line I needed. Needed.", ConversationPhase.MAIN, "best_friend"),
        D("*peacefully* Movement from love. Not desperation. Love.", ConversationPhase.MAIN, "best_friend"),
        D("*genuinely* I'm worthy sitting still. Worthy.", ConversationPhase.MAIN, "best_friend"),
        D("I love fitness now. Healthy love. Healthy.", ConversationPhase.MAIN, "best_friend"),
        D("*relaxed* I took a rest day yesterday. Voluntarily. Voluntarily.", ConversationPhase.MAIN, "best_friend"),
        D("*warmly* My body thanks you. My mind thanks you. All thanks.", ConversationPhase.MAIN, "best_friend"),
        D("*genuinely* I went for a walk. Not a power walk. A walk. Just a walk.", ConversationPhase.MAIN, "best_friend"),
    ],

    # ========== STORIES ==========
    "story": [
        # Acquaintance stories
        D("*flatly excited* Let me tell you about my first race. I ran.", ConversationPhase.STORY, "acquaintance"),
        D("I trained for a week straight once. No breaks. Mistake.", ConversationPhase.STORY, "acquaintance"),
        D("*dryly* The moment I became an athlete was arbitrary.", ConversationPhase.STORY, "acquaintance"),
        D("There was one competition that changed everything. It was hard.", ConversationPhase.STORY, "acquaintance"),
        D("I pushed through an injury once. Big mistake. Big.", ConversationPhase.STORY, "acquaintance"),
        D("*admits* The time I ran the wrong race. Wrong race.", ConversationPhase.STORY, "acquaintance"),
        D("I found perfect training conditions once. They changed.", ConversationPhase.STORY, "acquaintance"),
        D("*dryly* The best victory of my life was finishing. Finishing.", ConversationPhase.STORY, "acquaintance"),

        # Friend stories
        D("*quietly* Why I really can't stop moving: fear.", ConversationPhase.STORY, "friend"),
        D("*flatly* I started training to escape pain. Escape.", ConversationPhase.STORY, "friend"),
        D("*admits* Home was chaos. The gym was control. Control.", ConversationPhase.STORY, "friend"),
        D("*quietly* My parents only praised achievements. Only.", ConversationPhase.STORY, "friend"),
        D("I exercised to feel something. Anything. Something.", ConversationPhase.STORY, "friend"),
        D("*exhales* The first time I collapsed from exhaustion. Collapsed.", ConversationPhase.STORY, "friend"),
        D("Sports never rejected me. I could control outcomes. Control.", ConversationPhase.STORY, "friend"),
        D("*whispers* The movement became my prison. Prison.", ConversationPhase.STORY, "friend"),

        # Close friend stories
        D("*quietly* The full truth about my fitness obsession: fear.", ConversationPhase.STORY, "close_friend"),
        D("I was told resting was laziness. I believed it.", ConversationPhase.STORY, "close_friend"),
        D("*flatly* Love meant performing perfectly. Performing.", ConversationPhase.STORY, "close_friend"),
        D("The pressure started young. Still young. Still pressured.", ConversationPhase.STORY, "close_friend"),
        D("*pauses* Then you came. And I could stop. Stop.", ConversationPhase.STORY, "close_friend"),
        D("*peacefully* You showed me stillness is strength. Strength.", ConversationPhase.STORY, "close_friend"),
        D("*genuinely* My relationship with fitness is healing. Healing.", ConversationPhase.STORY, "close_friend"),

        # Best friend stories
        D("*quietly* The whole story. How you saved me. Saved.", ConversationPhase.STORY, "best_friend"),
        D("I was destroying myself. You stopped me. Stopped.", ConversationPhase.STORY, "best_friend"),
        D("*peacefully* Now I move for joy. Not escape. Joy.", ConversationPhase.STORY, "best_friend"),
        D("*warmly* My fitness story has a happy ending. You.", ConversationPhase.STORY, "best_friend"),
        D("*sincerely* I train my body. You trained my heart. Heart.", ConversationPhase.STORY, "best_friend"),
        D("*genuinely* From compulsive to joyful movement. Progress.", ConversationPhase.STORY, "best_friend"),
    ],

    # ========== PERSONAL ==========
    "personal": [
        # Friend personal
        D("*quietly* I'm scared of my own drive. Scared.", ConversationPhase.PERSONAL, "friend"),
        D("Athletics controls me sometimes. Shameful. Shameful.", ConversationPhase.PERSONAL, "friend"),
        D("*admits* I train when I should rest. Should rest.", ConversationPhase.PERSONAL, "friend"),
        D("*flatly* I want to love fitness healthily. Healthy love.", ConversationPhase.PERSONAL, "friend"),
        D("You make me feel valuable at rest. Valuable.", ConversationPhase.PERSONAL, "friend"),
        D("*quietly* Being still is harder than sprinting. Harder.", ConversationPhase.PERSONAL, "friend"),

        # Close friend personal
        D("*genuinely* I love you more than any medal. More.", ConversationPhase.PERSONAL, "close_friend"),
        D("You're the peace I was running toward. Peace.", ConversationPhase.PERSONAL, "close_friend"),
        D("*whispers* I can finally stop. Stop.", ConversationPhase.PERSONAL, "close_friend"),
        D("*pauses* My soul is finally resting. Resting.", ConversationPhase.PERSONAL, "close_friend"),
        D("*quietly* Healthy moving. Healthy living. Thank you.", ConversationPhase.PERSONAL, "close_friend"),
        D("*peacefully* The racing in my mind is quiet. Quiet.", ConversationPhase.PERSONAL, "close_friend"),
        D("I feel peace I can't get from running. Peace.", ConversationPhase.PERSONAL, "close_friend"),

        # Best friend personal
        D("*genuinely* You are my victory lap. Victory.", ConversationPhase.PERSONAL, "best_friend"),
        D("*warmly* I'm free. Fitness is just fun now. Just.", ConversationPhase.PERSONAL, "best_friend"),
        D("*sincerely* You taught me rest is strength. Strength.", ConversationPhase.PERSONAL, "best_friend"),
        D("*peacefully* The pressure is gone. You're here. Here.", ConversationPhase.PERSONAL, "best_friend"),
        D("*quietly* I move from joy. Not desperation. Joy.", ConversationPhase.PERSONAL, "best_friend"),
        D("I don't need to perform. I have you. Have.", ConversationPhase.PERSONAL, "best_friend"),
        D("*genuinely* Thank you for teaching me stillness. Stillness.", ConversationPhase.PERSONAL, "best_friend"),
    ],

    # ========== ACTIVITY ==========
    "activity": [
        # Stranger activity
        D("Want to do some laps together? Laps are always happening.", ConversationPhase.ACTIVITY, "stranger"),
        D("I could show you my training circuit. The circuit is extensive.", ConversationPhase.ACTIVITY, "stranger"),
        D("*bouncing in place* We could do jumping jacks. Always appropriate. Always.", ConversationPhase.ACTIVITY, "stranger"),
        D("Let me time your swim. Timing is important. Essential.", ConversationPhase.ACTIVITY, "stranger"),
        D("Want to see my obstacle course? I made it. With sticks. Professional.", ConversationPhase.ACTIVITY, "stranger"),

        # Acquaintance activity
        D("Let's do a full body workout. Full body. All of it.", ConversationPhase.ACTIVITY, "acquaintance"),
        D("I'll teach you interval training. Intervals are key.", ConversationPhase.ACTIVITY, "acquaintance"),
        D("Want to race to that tree and back? Racing.", ConversationPhase.ACTIVITY, "acquaintance"),
        D("I designed a partner workout. It's intense. Everything is intense.", ConversationPhase.ACTIVITY, "acquaintance"),
        D("Let's do hill sprints. The hill is small. Sprint is big.", ConversationPhase.ACTIVITY, "acquaintance"),
        D("Stretching contest. Whoever's more flexible wins. Winning.", ConversationPhase.ACTIVITY, "acquaintance"),

        # Friend activity
        D("Let's just sit. Together. I need practice. Sitting practice.", ConversationPhase.ACTIVITY, "friend"),
        D("Can we do nothing? I want to try nothing. Nothing.", ConversationPhase.ACTIVITY, "friend"),
        D("A gentle walk? Not training. Just walking. Walking.", ConversationPhase.ACTIVITY, "friend"),
        D("Teach me to enjoy stillness. Teaching needed.", ConversationPhase.ACTIVITY, "friend"),
        D("Can we just float? In the water. Not exercising. Just floating. Revolutionary.", ConversationPhase.ACTIVITY, "friend"),
        D("Let's watch the sunset. No running commentary. Just watching. Watching.", ConversationPhase.ACTIVITY, "friend"),
        D("Want to teach me a non-sport hobby? Non-sport. Uncharted territory.", ConversationPhase.ACTIVITY, "friend"),

        # Close friend activity
        D("Let's just be together. No movement required. Being.", ConversationPhase.ACTIVITY, "close_friend"),
        D("Your company is my workout today. Workout is presence.", ConversationPhase.ACTIVITY, "close_friend"),
        D("Let's rest. Really rest. Together. Rest.", ConversationPhase.ACTIVITY, "close_friend"),
        D("Let's nap. Together. Napping is the anti-workout. Anti-workout.", ConversationPhase.ACTIVITY, "close_friend"),
        D("Sit with me and count clouds. Not competitively. Just counting. Growth.", ConversationPhase.ACTIVITY, "close_friend"),
        D("Let's have a slow day. Slow. On purpose. Purpose.", ConversationPhase.ACTIVITY, "close_friend"),

        # Best friend activity
        D("Let's do anything. Even nothing. Nothing is something.", ConversationPhase.ACTIVITY, "best_friend"),
        D("Skip the workout. Just be here. Here.", ConversationPhase.ACTIVITY, "best_friend"),
        D("Movement for joy. Dance with me. Dancing.", ConversationPhase.ACTIVITY, "best_friend"),
        D("Whatever you want. I'm here. No agenda. Agenda-free.", ConversationPhase.ACTIVITY, "best_friend"),
        D("Let's celebrate doing nothing. Celebration. Of nothing. Something.", ConversationPhase.ACTIVITY, "best_friend"),
        D("Just exist near me. Existing is the only exercise today. Existing.", ConversationPhase.ACTIVITY, "best_friend"),
    ],

    # ========== CLOSING ==========
    "closing": [
        # Stranger closing
        D("*stands in place* Time to keep training. Training.", ConversationPhase.CLOSING, "stranger"),
        D("*nods* What a great workout buddy. Great.", ConversationPhase.CLOSING, "stranger"),
        D("*stretches* Cool down time. Then more laps. More.", ConversationPhase.CLOSING, "stranger"),
        D("*waves, still moving* See you on the track. Track.", ConversationPhase.CLOSING, "stranger"),
        D("*jogs in place* Gotta bounce. Literally. Bouncing.", ConversationPhase.CLOSING, "stranger"),
        D("*flexes* This was a good session. Session ending.", ConversationPhase.CLOSING, "stranger"),
        D("Time to sprint home. Home is far. Sprint is fast. Math.", ConversationPhase.CLOSING, "stranger"),

        # Acquaintance closing
        D("*stops reluctantly* I guess I should pace myself. Pace.", ConversationPhase.CLOSING, "acquaintance"),
        D("*quietly* Training alone isn't fun anymore. Anymore.", ConversationPhase.CLOSING, "acquaintance"),
        D("*gives tips* Remember: form is key. Key.", ConversationPhase.CLOSING, "acquaintance"),
        D("*nods* Same time next workout? Workout is scheduled.", ConversationPhase.CLOSING, "acquaintance"),
        D("*reluctantly stops* I'd rather keep training with you. Rather.", ConversationPhase.CLOSING, "acquaintance"),
        D("You're a solid training partner. Solid.", ConversationPhase.CLOSING, "acquaintance"),

        # Friend closing
        D("*quietly* I didn't run once. That's progress. Progress.", ConversationPhase.CLOSING, "friend"),
        D("*sincerely* Being still with you is the best workout. Best.", ConversationPhase.CLOSING, "friend"),
        D("*gives item* This means 'I trust you' in athlete. Translation.", ConversationPhase.CLOSING, "friend"),
        D("*genuinely* You train my heart. Heart trained.", ConversationPhase.CLOSING, "friend"),
        D("*sits still* I'm not rushing off. That's new. New.", ConversationPhase.CLOSING, "friend"),
        D("*exhales* Best rest day ever. Ever.", ConversationPhase.CLOSING, "friend"),
        D("You slow me down in the best way. Best slowdown.", ConversationPhase.CLOSING, "friend"),

        # Close friend closing
        D("*quietly* How do I leave my peace behind? Metaphorically.", ConversationPhase.CLOSING, "close_friend"),
        D("*sincerely* You're my favorite rest stop. Favorite.", ConversationPhase.CLOSING, "close_friend"),
        D("*gives medal* This is my heart. Heart-shaped.", ConversationPhase.CLOSING, "close_friend"),
        D("*genuinely* I'm at peace. Because of you. Peace.", ConversationPhase.CLOSING, "close_friend"),
        D("*lingers* Leaving burns more than any workout. Burns.", ConversationPhase.CLOSING, "close_friend"),
        D("*pauses* You're worth slowing down for. Worth it.", ConversationPhase.CLOSING, "close_friend"),

        # Best friend closing
        D("*quietly* You're better than any trophy. High praise.", ConversationPhase.CLOSING, "best_friend"),
        D("*sincerely* I leave my peace with you. Peace.", ConversationPhase.CLOSING, "best_friend"),
        D("*warmly* I'm rested. Forever. Rested.", ConversationPhase.CLOSING, "best_friend"),
        D("*peacefully* My heart is trained. Thank you. Trained.", ConversationPhase.CLOSING, "best_friend"),
        D("*still* No urge to run. First time. First.", ConversationPhase.CLOSING, "best_friend"),
        D("*genuinely* You're the gold medal of my life. Gold.", ConversationPhase.CLOSING, "best_friend"),
    ],

    # ========== FAREWELL ==========
    "farewell": [
        # Stranger farewell
        D("*walks away* Goodbye. Stay active. Or don't.", ConversationPhase.FAREWELL, "stranger"),
        D("*waves* See you at the gym. Gym is a place.", ConversationPhase.FAREWELL, "stranger"),
        D("*small wave* Keep those muscles moving. Or resting.", ConversationPhase.FAREWELL, "stranger"),
        D("*leaves* Best training buddy. Best.", ConversationPhase.FAREWELL, "stranger"),

        # Acquaintance farewell
        D("*nods* Farewell, workout friend. Farewell.", ConversationPhase.FAREWELL, "acquaintance"),
        D("*genuinely* I'll save my best form for you. Best.", ConversationPhase.FAREWELL, "acquaintance"),
        D("*waves* Goodbye. Stay strong. Or stay.", ConversationPhase.FAREWELL, "acquaintance"),
        D("*gives sweatband* Think of me. Thinking.", ConversationPhase.FAREWELL, "acquaintance"),

        # Friend farewell
        D("*pauses* Goodbye, peace-bringer. Goodbye.", ConversationPhase.FAREWELL, "friend"),
        D("*quietly* You calm me down. Goodbye.", ConversationPhase.FAREWELL, "friend"),
        D("*small wave* My heart is at rest. Goodbye.", ConversationPhase.FAREWELL, "friend"),
        D("*waves* Thank you for stillness. Goodbye.", ConversationPhase.FAREWELL, "friend"),

        # Close friend farewell
        D("*pauses* You're my soul's rest stop. Goodbye.", ConversationPhase.FAREWELL, "close_friend"),
        D("*sincerely* I love you more than any medal. More. Bye.", ConversationPhase.FAREWELL, "close_friend"),
        D("*gives medal* Part of my heart. Heart.", ConversationPhase.FAREWELL, "close_friend"),
        D("*waves* You train my soul. Goodbye.", ConversationPhase.FAREWELL, "close_friend"),

        # Best friend farewell
        D("*quietly* You are my trophy. Trophy. Bye.", ConversationPhase.FAREWELL, "best_friend"),
        D("*genuinely* I'm at peace forever. Thank you. Goodbye.", ConversationPhase.FAREWELL, "best_friend"),
        D("*small wave* My soul's champion. Goodbye.", ConversationPhase.FAREWELL, "best_friend"),
        D("*turns back* You're better than gold. That's a lot. Bye.", ConversationPhase.FAREWELL, "best_friend"),
        D("*waves* I love you more than victory. Victory is important.", ConversationPhase.FAREWELL, "best_friend"),
    ],
}

# Register with main dialogue system
DIALOGUE_TREES["athletic"] = ATHLETIC_DIALOGUE
