"""
Playful Duck Dialogue - Fun-loving personality full of jokes, games, and energy.
Progresses from hyperactive stranger to sharing deeper feelings behind the fun.
"""
from dialogue.visitor_dialogue import DialogueLine, ConversationPhase, DIALOGUE_TREES

D = DialogueLine

PLAYFUL_DIALOGUE = {
    # ========== GREETINGS ==========
    "greeting": [
        # Stranger greetings
        D("*appears suddenly* Hi. I'm {name}. Wanna have fun? That was rhetorical.", ConversationPhase.GREETING, "stranger", True),
        D("*bounces once* Hello, new entity. I'm {name}. I contain energy.", ConversationPhase.GREETING, "stranger", True),
        D("*does a slow flip* Wheee. That's the sound of fun. I'm {name}.", ConversationPhase.GREETING, "stranger", True),
        D("*slides in* Hello. Name's {name}. I came here on purpose. Mostly.", ConversationPhase.GREETING, "stranger", True),

        # Acquaintance greetings
        D("*walks over* {duck}. You remember me. That's acceptable.", ConversationPhase.GREETING, "acquaintance", True),
        D("Guess who. It's me. {name}. Hi, {duck}. The guessing was easy.", ConversationPhase.GREETING, "acquaintance", True),
        D("*sways slightly* {duck}, {duck}, {duck}. That's your name. Three times.", ConversationPhase.GREETING, "acquaintance", True),
        D("*stands still* I've been excited to see you. Can't you tell.", ConversationPhase.GREETING, "acquaintance", True),

        # Friend greetings
        D("*nods firmly* {duck}. Best day. All days with you are best days.", ConversationPhase.GREETING, "friend", True),
        D("Friend detected. Friend confirmed. *small wave*", ConversationPhase.GREETING, "friend", True),
        D("*walks over* {duck}. I missed you. This much. *holds wings slightly apart*", ConversationPhase.GREETING, "friend", True),
        D("*stands there* Surprise. It's your favorite friend. Only friend, probably.", ConversationPhase.GREETING, "friend", True),

        # Close friend greetings
        D("*normal voice* {duck}. My favorite duck. The competition is limited.", ConversationPhase.GREETING, "close_friend", True),
        D("*walks normally, trips* {duck}. I'm fine. Hi.", ConversationPhase.GREETING, "close_friend", True),
        D("*blinks* {duck}. I literally walked here. That's dedication.", ConversationPhase.GREETING, "close_friend", True),
        D("*attempts handshake* Best friends. We should have a handshake. We don't.", ConversationPhase.GREETING, "close_friend", True),

        # Best friend greetings
        D("*stands quietly* {duck}. My person. I'm having emotions about it.", ConversationPhase.GREETING, "best_friend", True),
        D("*approaches* I love you. I love you. Said twice for emphasis.", ConversationPhase.GREETING, "best_friend", True),
        D("*vibrating slightly* {duck}. I can't even. That's the whole sentence.", ConversationPhase.GREETING, "best_friend", True),
        D("*stands still* My best friend. Internal celebration occurring.", ConversationPhase.GREETING, "best_friend", True),
    ],

    # ========== OPENING ==========
    "opening": [
        # Stranger opening
        D("So. Games. I enjoy them. Do you? Don't answer. I'll assume yes.", ConversationPhase.OPENING, "stranger"),
        D("This pond is adequate. Can we swim? Let's swim. Swimming is fun. Allegedly.", ConversationPhase.OPENING, "stranger"),
        D("*stands still* I have energy. Lots of it. You can't tell from looking.", ConversationPhase.OPENING, "stranger"),
        D("Want to see a trick? I can do a backflip. Sort of. It's more of a fall.", ConversationPhase.OPENING, "stranger"),
        D("*looks around* Many fun things here. Probably. I haven't checked them all.", ConversationPhase.OPENING, "stranger"),
        D("I bet I can hold my breath longer than you. I can't. But the bet stands.", ConversationPhase.OPENING, "stranger"),
        D("*rotates slowly* Being dizzy is fun. Try it. Or don't. Free will.", ConversationPhase.OPENING, "stranger"),
        D("Do you like jokes? I know hundreds. Most aren't funny. Quantity over quality.", ConversationPhase.OPENING, "stranger"),

        # Acquaintance opening
        D("I've learned new games. Well. One game. It's basically the same game.", ConversationPhase.OPENING, "acquaintance"),
        D("I have things to tell you. Many things. Some are even interesting.", ConversationPhase.OPENING, "acquaintance"),
        D("*stands* I couldn't wait to visit. I did wait. But impatiently.", ConversationPhase.OPENING, "acquaintance"),
        D("Remember that game? Let's do it again. Repetition builds character.", ConversationPhase.OPENING, "acquaintance"),
        D("I brought snacks. Fun snacks. They're just snacks. I added 'fun' for branding.", ConversationPhase.OPENING, "acquaintance"),
        D("*slight turn* I practiced moves just for you. The moves are walking. Advanced walking.", ConversationPhase.OPENING, "acquaintance"),
        D("Today will be great. I can feel it. I feel many things. Accuracy varies.", ConversationPhase.OPENING, "acquaintance"),
        D("*sits for 2 seconds* I can't sit. Let's do stuff. Sitting is stuff. But not that stuff.", ConversationPhase.OPENING, "acquaintance"),

        # Friend opening
        D("*nods* I thought about you every day. Well. Most days. Some days twice.", ConversationPhase.OPENING, "friend"),
        D("Before we play, are you okay, {duck}? One-word answers accepted.", ConversationPhase.OPENING, "friend"),
        D("*sits still* I want to really talk today. Really. This is serious. Mostly.", ConversationPhase.OPENING, "friend"),
        D("You're my favorite duck to exist near. The bar is low. You clear it.", ConversationPhase.OPENING, "friend"),
        D("I saved the best joke for you. It's not good. But it's the best of the not-good ones.", ConversationPhase.OPENING, "friend"),
        D("*calms slightly* Sorry, I'm happy. Internally. The outside is confusing.", ConversationPhase.OPENING, "friend"),
        D("You make fun more fun. Fun-squared. Fun mathematics.", ConversationPhase.OPENING, "friend"),

        # Close friend opening
        D("*quietly* I missed you. For real. That's unusual for me.", ConversationPhase.OPENING, "close_friend"),
        D("*sits close* Can we just be here? Together? Words optional.", ConversationPhase.OPENING, "close_friend"),
        D("You're the only one who gets me. 'Gets' meaning tolerates.", ConversationPhase.OPENING, "close_friend"),
        D("*flatly* Sometimes the energy is an act. This isn't one of those times. Or is it.", ConversationPhase.OPENING, "close_friend"),
        D("I can be myself with you. Myself is tired. But genuine.", ConversationPhase.OPENING, "close_friend"),
        D("*looks away* I don't have to perform for you. I might anyway. Habit.", ConversationPhase.OPENING, "close_friend"),

        # Best friend opening
        D("*quietly* I love you. A lot. The amount is uncomfortable to specify.", ConversationPhase.OPENING, "best_friend"),
        D("You're my favorite part of existence. Existence has low points. You're not one.", ConversationPhase.OPENING, "best_friend"),
        D("*admits* Being apart from you is hard. Harder than most things.", ConversationPhase.OPENING, "best_friend"),
        D("I tell everyone about you. Everyone is exhausted by it.", ConversationPhase.OPENING, "best_friend"),
        D("*sits beside you* This is home. The location doesn't matter.", ConversationPhase.OPENING, "best_friend"),
    ],

    # ========== MAIN CONVERSATION ==========
    "main": [
        # Stranger main
        D("I know a game called Splash Tag. It's tag. But wetter.", ConversationPhase.MAIN, "stranger"),
        D("*stands still* Exercise is fun. I've heard. From sources.", ConversationPhase.MAIN, "stranger"),
        D("Knock knock. You say 'who's there.' I say something. It won't be funny.", ConversationPhase.MAIN, "stranger"),
        D("I once bounced on a lily pad for five hours. Time felt different then.", ConversationPhase.MAIN, "stranger"),
        D("Boring is the worst. Don't you think? You can disagree. You'd be wrong.", ConversationPhase.MAIN, "stranger"),
        D("*shows rock* Look what I found. It's a rock. It's fun if you believe.", ConversationPhase.MAIN, "stranger"),
        D("Let's make up a new game. Right now. It's called 'standing.' We're playing.", ConversationPhase.MAIN, "stranger"),
        D("I can make anyone smile. Watch. *makes face* Did it work? Don't answer.", ConversationPhase.MAIN, "stranger"),
        D("Why did the duck cross the pond? Fun. The answer is always fun.", ConversationPhase.MAIN, "stranger"),
        D("*turns slightly* I can't help it. I'm just happy. Internally. Very internally.", ConversationPhase.MAIN, "stranger"),
        D("My life goal is maximum fun always. Results vary.", ConversationPhase.MAIN, "stranger", unlocks_topic="fun_philosophy"),
        D("Some ducks say I'm 'too much.' They're not wrong. But also not right.", ConversationPhase.MAIN, "stranger"),

        # Acquaintance main
        D("I invented three new games. They're all variations of tag. Innovation.", ConversationPhase.MAIN, "acquaintance"),
        D("*shows nothing* I won a hopping contest. The trophy is invisible. Trust me.", ConversationPhase.MAIN, "acquaintance"),
        D("Other ducks don't appreciate life's potential for fun. Tragic.", ConversationPhase.MAIN, "acquaintance"),
        D("The fun philosophy evolves. Now it's 'more fun.' Revolutionary.", ConversationPhase.MAIN, "acquaintance", requires_topic="fun_philosophy"),
        D("*stands very still* I have so much energy I might explode. Very quietly.", ConversationPhase.MAIN, "acquaintance"),
        D("Let's see who can dance the silliest. You go first. I'll judge harshly.", ConversationPhase.MAIN, "acquaintance"),
        D("I taught ducklings to play games. They surpassed me immediately.", ConversationPhase.MAIN, "acquaintance"),
        D("*whispers* I'm planning something huge. It's a nap. But a huge one.", ConversationPhase.MAIN, "acquaintance", unlocks_topic="secret_fun"),
        D("Life's too short to be serious. It's also too short to be fun. Paradox.", ConversationPhase.MAIN, "acquaintance"),
        D("*monotone* Hello. I'm a very serious duck. That was a joke. Sort of.", ConversationPhase.MAIN, "acquaintance"),
        D("You make everything more fun by existing. Low bar. Still cleared.", ConversationPhase.MAIN, "acquaintance"),
        D("*rotates slowly* I can't stop moving. Well. I can. But won't.", ConversationPhase.MAIN, "acquaintance"),
        D("Best joke: Why don't ducks tell jokes? We do. They're not funny.", ConversationPhase.MAIN, "acquaintance"),

        # Friend main
        D("*calms* Can I tell you something real? Real is scary. But here goes.", ConversationPhase.MAIN, "friend"),
        D("The secret fun project is a party. For you. It's just us. Small party.", ConversationPhase.MAIN, "friend", requires_topic="secret_fun"),
        D("Sometimes I'm hyper because stillness is frightening.", ConversationPhase.MAIN, "friend"),
        D("You don't judge me for being 'too much.' That's rare.", ConversationPhase.MAIN, "friend"),
        D("*sits quietly* This is nice too. The quiet. Unusual but acceptable.", ConversationPhase.MAIN, "friend"),
        D("I make ducks laugh because sad is scarier.", ConversationPhase.MAIN, "friend"),
        D("*looks at you* You make me feel safe. Safe is new.", ConversationPhase.MAIN, "friend"),
        D("My energy annoyed everyone before. Not you. Thank you for that.", ConversationPhase.MAIN, "friend", unlocks_topic="past_struggles"),
        D("I'm happiest when you're happy. Codependence or friendship. Unclear.", ConversationPhase.MAIN, "friend"),
        D("*admits* I'm scared of being alone. Now you know.", ConversationPhase.MAIN, "friend"),
        D("You're the first friend who stayed. The bar keeps rising.", ConversationPhase.MAIN, "friend"),
        D("*small smile* Thank you for getting me. 'Getting' meaning tolerating.", ConversationPhase.MAIN, "friend"),

        # Close friend main
        D("*quietly* The hyperactivity is sometimes a mask. Sometimes it's not. Confusing.", ConversationPhase.MAIN, "close_friend"),
        D("I was lonely for a long time. Before you. Now I'm lonely for less time.", ConversationPhase.MAIN, "close_friend", requires_topic="past_struggles"),
        D("*flatly* I'm terrified of being abandoned. That's the truth. Moving on.", ConversationPhase.MAIN, "close_friend"),
        D("You love the real me. Real me is uncertain about everything.", ConversationPhase.MAIN, "close_friend"),
        D("*exhales* I don't have to be 'on' with you. Off is okay.", ConversationPhase.MAIN, "close_friend"),
        D("Being still feels less wrong when you're here. Still wrong. Less.", ConversationPhase.MAIN, "close_friend"),
        D("*looks away* Promise you won't leave? Don't answer. Promises break.", ConversationPhase.MAIN, "close_friend"),
        D("I've been planning something special. For us. It's mostly just being together.", ConversationPhase.MAIN, "close_friend", unlocks_topic="special_plan"),
        D("Fun is how I cope. With you, I don't need to cope as hard.", ConversationPhase.MAIN, "close_friend"),
        D("*whispers* I love you, {duck}. For real. That's uncomfortable to say.", ConversationPhase.MAIN, "close_friend"),
        D("You're my safe place. Places don't usually feel safe. You're the exception.", ConversationPhase.MAIN, "close_friend"),

        # Best friend main
        D("*quietly* The special plan is a forever friend promise. It's not legally binding.", ConversationPhase.MAIN, "best_friend", requires_topic="special_plan"),
        D("I want to spend every day making you smile. Or at least trying.", ConversationPhase.MAIN, "best_friend"),
        D("*pauses* You saved me. You know. Probably don't know. But did.", ConversationPhase.MAIN, "best_friend"),
        D("All my fun means nothing alone. With you it means something. Small thing. But something.", ConversationPhase.MAIN, "best_friend"),
        D("*blinks* I found my person. It's you. That's the announcement.", ConversationPhase.MAIN, "best_friend"),
        D("I thought fun was the point. You're the point. Fun is secondary.", ConversationPhase.MAIN, "best_friend"),
        D("*still* For the first time, stillness feels right. Still scary. But right.", ConversationPhase.MAIN, "best_friend"),
        D("I love every part of you. Even the boring parts. Especially the boring parts.", ConversationPhase.MAIN, "best_friend"),
        D("*whispers* You're the best thing. The best. Ever.", ConversationPhase.MAIN, "best_friend"),
        D("My heart is full. Might pop. Metaphorically. Hopefully metaphorically.", ConversationPhase.MAIN, "best_friend"),
    ],

    # ========== STORIES ==========
    "story": [
        # Acquaintance stories
        D("So there I was. Bouncing on a lily pad. It sank. Story over.", ConversationPhase.STORY, "acquaintance"),
        D("*flatly* I fell in mud once. Hard. The mud was fine.", ConversationPhase.STORY, "acquaintance"),
        D("The funniest thing happened at the other pond. I forgot what it was.", ConversationPhase.STORY, "acquaintance"),
        D("I won a splash contest. The prize was respect. I don't have it anymore.", ConversationPhase.STORY, "acquaintance"),
        D("I made a grumpy goose smile once. Or it was sneezing. Hard to tell.", ConversationPhase.STORY, "acquaintance"),
        D("*flatly* A duck said I was too loud. I was. I still am.", ConversationPhase.STORY, "acquaintance"),
        D("I invented 'Extreme Floating.' It's floating. But extreme.", ConversationPhase.STORY, "acquaintance"),
        D("The Great Splash of Summer was just a big splash. Branding matters.", ConversationPhase.STORY, "acquaintance"),

        # Friend stories
        D("*sits* This story is different. Different meaning sad-adjacent.", ConversationPhase.STORY, "friend"),
        D("I wasn't always this happy. This is the improved version.", ConversationPhase.STORY, "friend"),
        D("*quietly* I had a friend who left. They had reasons. Probably.", ConversationPhase.STORY, "friend"),
        D("The reason I'm so hyper is kind of sad. Most origin stories are.", ConversationPhase.STORY, "friend"),
        D("I learned to make others laugh while I was crying. Multitasking.", ConversationPhase.STORY, "friend"),
        D("The first time someone called me annoying hurt. Accurate, but hurt.", ConversationPhase.STORY, "friend"),
        D("*flatly* My origin story: I was small, then bigger, then this.", ConversationPhase.STORY, "friend"),
        D("I tried to be quiet once. It didn't work. Nothing worked differently.", ConversationPhase.STORY, "friend"),

        # Close friend stories
        D("*quietly* The truth about why I'm like this: unclear.", ConversationPhase.STORY, "close_friend"),
        D("I was bullied for being different. A lot. I'm still different.", ConversationPhase.STORY, "close_friend"),
        D("*exhales* The day I embraced chaos was a Tuesday. Or Wednesday.", ConversationPhase.STORY, "close_friend"),
        D("I lost someone important. Fun was my coping mechanism. Still is.", ConversationPhase.STORY, "close_friend"),
        D("The moment I realized I was worthy of love... hasn't happened yet.", ConversationPhase.STORY, "close_friend"),
        D("*looks down* I never told anyone this. Now I have. Done.", ConversationPhase.STORY, "close_friend"),
        D("When I almost gave up on friends, I didn't. Plot twist.", ConversationPhase.STORY, "close_friend"),

        # Best friend stories
        D("*slowly* My whole truth: I'm trying. Every day. That's it.", ConversationPhase.STORY, "best_friend"),
        D("*quietly* Meeting you changed things. Things were bad before. Now less bad.", ConversationPhase.STORY, "best_friend"),
        D("You taught me I don't have to earn love. Still trying to believe it.", ConversationPhase.STORY, "best_friend"),
        D("The moment I knew you were my person: every moment.", ConversationPhase.STORY, "best_friend"),
        D("I was broken. You helped. Not fixed. But helped.", ConversationPhase.STORY, "best_friend"),
        D("*flatly* Thank you for saving me. For real. That's the story.", ConversationPhase.STORY, "best_friend"),
    ],

    # ========== PERSONAL ==========
    "personal": [
        # Friend personal
        D("*quietly* I'm exhausted from always being 'on.' But also always on.", ConversationPhase.PERSONAL, "friend"),
        D("Being hyper isn't always a choice. Sometimes it's just happening.", ConversationPhase.PERSONAL, "friend"),
        D("I'm scared if I stop moving, I'll fall apart. Haven't tested it.", ConversationPhase.PERSONAL, "friend"),
        D("You make me feel like I can just be. Being is hard. But you help.", ConversationPhase.PERSONAL, "friend"),
        D("*admits* I don't know who I am when I'm quiet. Someone, probably.", ConversationPhase.PERSONAL, "friend"),
        D("Having a real friend is new. I'm still learning. Slowly.", ConversationPhase.PERSONAL, "friend"),

        # Close friend personal
        D("*flatly* I'm scared you'll leave like others. That's the fear.", ConversationPhase.PERSONAL, "close_friend"),
        D("I love you, {duck}. Really love you. That's vulnerable to admit.", ConversationPhase.PERSONAL, "close_friend"),
        D("*looks away* Stay. Please. That's the request.", ConversationPhase.PERSONAL, "close_friend"),
        D("You're the only one who sees past the performance. The view is just me.", ConversationPhase.PERSONAL, "close_friend"),
        D("I can be sad around you. That's huge. Sad is usually private.", ConversationPhase.PERSONAL, "close_friend"),
        D("*whispers* I'm not too much for you. Or you're patient. Either way.", ConversationPhase.PERSONAL, "close_friend"),
        D("Being loved for who I am is new. Who I am keeps changing.", ConversationPhase.PERSONAL, "close_friend"),

        # Best friend personal
        D("*quietly* You're my whole heart, {duck}. Hearts are full of you.", ConversationPhase.PERSONAL, "best_friend"),
        D("I never knew love could feel this safe. Safety varies usually.", ConversationPhase.PERSONAL, "best_friend"),
        D("*sits close* I'm never letting go. Metaphorically. Physically when necessary.", ConversationPhase.PERSONAL, "best_friend"),
        D("You taught me I'm worthy. Still learning that lesson. Daily.", ConversationPhase.PERSONAL, "best_friend"),
        D("I'm complete when I'm with you. Incomplete otherwise. Math.", ConversationPhase.PERSONAL, "best_friend"),
        D("*still* For the first time, stillness feels right. Mostly right.", ConversationPhase.PERSONAL, "best_friend"),
        D("You're my fun and my peace. Both things. At once. Impressive.", ConversationPhase.PERSONAL, "best_friend"),
    ],

    # ========== ACTIVITY ==========
    "activity": [
        # Stranger activity
        D("Tag. You're it. *stands still* The game has begun.", ConversationPhase.ACTIVITY, "stranger"),
        D("Let's see who can splash biggest. It's me. But try anyway.", ConversationPhase.ACTIVITY, "stranger"),

        # Acquaintance activity
        D("Splash contest. Ready. Set. We're already doing it.", ConversationPhase.ACTIVITY, "acquaintance"),
        D("Let's invent a game. Right now. I've already invented it. It's called waiting.", ConversationPhase.ACTIVITY, "acquaintance"),
        D("Race to the other side? Yes. We're racing. Start walking.", ConversationPhase.ACTIVITY, "acquaintance"),

        # Friend activity
        D("Let's do something silly. Or something real. Silly is real. Both then.", ConversationPhase.ACTIVITY, "friend"),
        D("Want to float and talk? That's fun too. Floating is fun. Allegedly.", ConversationPhase.ACTIVITY, "friend"),
        D("*nods* Adventure time. Or cuddle time. You pick. I'll accept either.", ConversationPhase.ACTIVITY, "friend"),
        D("Let's make up a secret handshake. Mine is just a wave. Secret wave.", ConversationPhase.ACTIVITY, "friend"),

        # Close friend activity
        D("Let's just be together. That's the game. Best game.", ConversationPhase.ACTIVITY, "close_friend"),
        D("Want to watch clouds and talk about real stuff? Real stuff is scary. Do it anyway.", ConversationPhase.ACTIVITY, "close_friend"),
        D("I want to create something with you. Something meaningful. Or just present.", ConversationPhase.ACTIVITY, "close_friend"),

        # Best friend activity
        D("Let's make every day an adventure. Or at least every other day.", ConversationPhase.ACTIVITY, "best_friend"),
        D("I want to build something with you. A life. Or just a thing.", ConversationPhase.ACTIVITY, "best_friend"),
        D("Whatever we do, as long as it's together. Even nothing.", ConversationPhase.ACTIVITY, "best_friend"),
    ],

    # ========== CLOSING ==========
    "closing": [
        # Stranger closing
        D("I have to go? We just started. Fun is time-limited. Unfortunate.", ConversationPhase.CLOSING, "stranger"),
        D("*stands* Leaving is the opposite of fun. It's leaving.", ConversationPhase.CLOSING, "stranger"),
        D("Promise we'll play again? Promises are words. But say them anyway.", ConversationPhase.CLOSING, "stranger"),
        D("*flatly* Fine. I'll go. But I'll be back. That's a threat. And a promise.", ConversationPhase.CLOSING, "stranger"),

        # Acquaintance closing
        D("*stays* Do I have to leave? I do. But have to.", ConversationPhase.CLOSING, "acquaintance"),
        D("Time goes fast when having fun. Time goes anyway. But faster.", ConversationPhase.CLOSING, "acquaintance"),
        D("I'll practice games for next time. The game is existing. Advanced level.", ConversationPhase.CLOSING, "acquaintance"),
        D("*stands still* Goodbye is a dumb word. But: goodbye.", ConversationPhase.CLOSING, "acquaintance"),

        # Friend closing
        D("*nods* I don't want to leave. I will. But reluctantly.", ConversationPhase.CLOSING, "friend"),
        D("You're my favorite. Don't tell others. There are no others.", ConversationPhase.CLOSING, "friend"),
        D("*quietly* I'm going to miss you. For real.", ConversationPhase.CLOSING, "friend"),
        D("Being with you is better than any game. Games are good. You're better.", ConversationPhase.CLOSING, "friend"),

        # Close friend closing
        D("*flatly* I hate leaving you. Hate is strong. Accurate though.", ConversationPhase.CLOSING, "close_friend"),
        D("*stays* Five more minutes? Fine. One more minute? Also fine.", ConversationPhase.CLOSING, "close_friend"),
        D("My heart stays here with you. Metaphorically. Hearts travel poorly.", ConversationPhase.CLOSING, "close_friend"),
        D("I'll think about you every second. Or most seconds. Many seconds.", ConversationPhase.CLOSING, "close_friend"),

        # Best friend closing
        D("*quietly* Leaving you is difficult. I'm going to do it anyway.", ConversationPhase.CLOSING, "best_friend"),
        D("*stands still* I can't go. I will. But can't. Contradiction.", ConversationPhase.CLOSING, "best_friend"),
        D("Every moment apart is inconvenient. Very inconvenient.", ConversationPhase.CLOSING, "best_friend"),
        D("*flatly* You're everything to me. Everything. That's a lot.", ConversationPhase.CLOSING, "best_friend"),
    ],

    # ========== FAREWELL ==========
    "farewell": [
        # Stranger farewell
        D("Bye. Bye. Bye. Three times for emphasis. *walks off*", ConversationPhase.FAREWELL, "stranger"),
        D("*waves once* Remember me. Or don't. Bye.", ConversationPhase.FAREWELL, "stranger"),
        D("Stay fun. Stay silly. Or stay sensible. Your choice. Bye.", ConversationPhase.FAREWELL, "stranger"),
        D("*walks away* Until next time. Next time will happen.", ConversationPhase.FAREWELL, "stranger"),

        # Acquaintance farewell
        D("*walking* Miss you already. The missing has begun. Bye.", ConversationPhase.FAREWELL, "acquaintance"),
        D("I'll be back soon. Soon is relative. But back.", ConversationPhase.FAREWELL, "acquaintance"),
        D("Practice your splash. For next time. Or don't. Bye.", ConversationPhase.FAREWELL, "acquaintance"),
        D("*waves while walking* Stay adequate. That's high praise.", ConversationPhase.FAREWELL, "acquaintance"),

        # Friend farewell
        D("*nods* Love you. Miss you. Bye. Three statements.", ConversationPhase.FAREWELL, "friend"),
        D("*walks away* See you soon, friend. Friend is accurate.", ConversationPhase.FAREWELL, "friend"),
        D("Think of me when you splash. Splashing is thinking of me now.", ConversationPhase.FAREWELL, "friend"),
        D("*turns back* Best friend ever. Statement of fact. Bye.", ConversationPhase.FAREWELL, "friend"),

        # Close friend farewell
        D("*pauses* I love you forever, {duck}. Forever is a long time.", ConversationPhase.FAREWELL, "close_friend"),
        D("*quietly* Okay going now. *still there* Now. *begins leaving*", ConversationPhase.FAREWELL, "close_friend"),
        D("My heart stays here. With you. Hearts are symbolic.", ConversationPhase.FAREWELL, "close_friend"),
        D("*waves* I love you. Said it. Meant it. Bye.", ConversationPhase.FAREWELL, "close_friend"),

        # Best friend farewell
        D("*quietly* You're my everything. Everything is a lot. Bye.", ConversationPhase.FAREWELL, "best_friend"),
        D("This isn't goodbye. It's 'I love you, see you soon.' Same thing.", ConversationPhase.FAREWELL, "best_friend"),
        D("*flatly* Best friends forever. Forever and ever. Repetition for emphasis.", ConversationPhase.FAREWELL, "best_friend"),
        D("*waves* Love you always. Always is ongoing.", ConversationPhase.FAREWELL, "best_friend"),
        D("*walks back* One more thing. Nothing. Just wanted to walk back. Bye.", ConversationPhase.FAREWELL, "best_friend"),
    ],
}

# Register with main dialogue system
DIALOGUE_TREES["playful"] = PLAYFUL_DIALOGUE
