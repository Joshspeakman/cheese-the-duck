"""
Adventurous Duck Dialogue - Explorer personality with deadpan delivery.
Tales of travel delivered with dry wit and matter-of-fact observations.
"""
from dialogue.visitor_dialogue import DialogueLine, ConversationPhase, DIALOGUE_TREES

# D = DialogueLine shorthand
D = DialogueLine

ADVENTUROUS_DIALOGUE = {
    # ========== GREETINGS ==========
    "greeting": [
        # Stranger greetings
        D("*appears from somewhere* Oh. Hello. I'm {name}. I was just... passing through. As one does.", ConversationPhase.GREETING, "stranger", True),
        D("*dusts off feathers* Ah. Another duck. Name's {name}. I've been places. Many places.", ConversationPhase.GREETING, "stranger", True),
        D("*adjusts worn hat* You live here? Interesting. I'm {name}. I don't live anywhere, really.", ConversationPhase.GREETING, "stranger", True),
        D("*emerges from bush* Oh, you saw that. Okay. I'm {name}. I was exploring. Obviously.", ConversationPhase.GREETING, "stranger", True),

        # Acquaintance greetings
        D("*nods* {duck}. Good to see you didn't move. Makes you easy to find.", ConversationPhase.GREETING, "acquaintance", True),
        D("Ah, {duck}. Still here. That's comforting, I suppose.", ConversationPhase.GREETING, "acquaintance", True),
        D("*shows up unannounced* {duck}. I have stories. Whether you want them or not.", ConversationPhase.GREETING, "acquaintance", True),
        D("Back again. {duck}, right? I remember now. My memory for places is better.", ConversationPhase.GREETING, "acquaintance", True),

        # Friend greetings
        D("*waddles over* {duck}. You won't believe what I found. Actually, you might not care. But I'll tell you anyway.", ConversationPhase.GREETING, "friend", True),
        D("{duck}. There you are. I was thinking about coming here while I was somewhere else entirely.", ConversationPhase.GREETING, "friend", True),
        D("*arrives looking disheveled* {duck}. I made it. The journey was... eventful.", ConversationPhase.GREETING, "friend", True),
        D("Hey, {duck}. I brought stories. And possibly mud. Mostly stories.", ConversationPhase.GREETING, "friend", True),

        # Close friend greetings
        D("*slightly out of breath* {duck}. I walked fast to get here. Not running. Walking. Fast.", ConversationPhase.GREETING, "close_friend", True),
        D("{duck}. *genuine relief* Oh good. You're still you. I was worried you'd become someone else.", ConversationPhase.GREETING, "close_friend", True),
        D("*sits down heavily* Finally. {duck}. You're a rest stop for my soul. That sounded dramatic.", ConversationPhase.GREETING, "close_friend", True),
        D("There's my favorite stationary duck. {duck}. You never move. I appreciate that about you.", ConversationPhase.GREETING, "close_friend", True),

        # Best friend greetings
        D("*emotional but hiding it* {duck}. I'm not going to say I missed you. But I thought about you. A lot.", ConversationPhase.GREETING, "best_friend", True),
        D("{duck}. *long pause* ...I rushed here. I don't rush for most things. Make of that what you will.", ConversationPhase.GREETING, "best_friend", True),
        D("*arrives, stops, just looks at you* ...{duck}. Words are failing me. That never happens.", ConversationPhase.GREETING, "best_friend", True),
        D("You know, {duck}, I've seen incredible places. But this? This is where I actually want to be.", ConversationPhase.GREETING, "best_friend", True),
    ],

    # ========== OPENING (Small Talk) ==========
    "opening": [
        # Stranger opening
        D("So. Nice pond. I've seen worse. I've seen better. But this is... fine.", ConversationPhase.OPENING, "stranger"),
        D("I've been traveling. For a while now. Time loses meaning out there.", ConversationPhase.OPENING, "stranger"),
        D("Do you explore? No? That's okay. Someone has to stay home, I suppose.", ConversationPhase.OPENING, "stranger"),
        D("I collect rocks. Interesting ones. Want to see? No? Fair enough.", ConversationPhase.OPENING, "stranger"),
        D("Weather's good for traveling. Or staying. Either, really.", ConversationPhase.OPENING, "stranger"),
        D("Your pond has good... water. Watery water. Very important for ponds.", ConversationPhase.OPENING, "stranger"),
        D("I heard there might be interesting bread around here. Rumors, probably.", ConversationPhase.OPENING, "stranger"),
        D("*looks at sky* Perfect conditions for something. Not sure what.", ConversationPhase.OPENING, "stranger"),

        # Acquaintance opening
        D("Been thinking since we last talked. About maps. And existence. Mostly maps.", ConversationPhase.OPENING, "acquaintance"),
        D("I've traveled far since we met. Probably too far. My feet have opinions.", ConversationPhase.OPENING, "acquaintance"),
        D("Brought my journal. It has sketches. They're... artistic. That's what I tell myself.", ConversationPhase.OPENING, "acquaintance"),
        D("So. Anything happen here? Probably not. That's why I explore. Things happen out there.", ConversationPhase.OPENING, "acquaintance"),
        D("Found something interesting. Made me think of you. Not sure why.", ConversationPhase.OPENING, "acquaintance"),
        D("I mapped three streams since last time. Streams are just indecisive rivers.", ConversationPhase.OPENING, "acquaintance"),
        D("My compass works. Mostly. It disagrees with me sometimes.", ConversationPhase.OPENING, "acquaintance"),
        D("*shows map* See all these X marks? Been there. Some of them on purpose.", ConversationPhase.OPENING, "acquaintance"),

        # Friend opening
        D("Before I start rambling about adventures... how are you? Genuinely asking.", ConversationPhase.OPENING, "friend"),
        D("*sits comfortably* Good friend. Good pond. This is... acceptable.", ConversationPhase.OPENING, "friend"),
        D("Saved the best story for you. It's about getting lost. I get lost a lot.", ConversationPhase.OPENING, "friend"),
        D("Did you try that river diving thing I mentioned? No? Smart choice, honestly.", ConversationPhase.OPENING, "friend"),
        D("I named a rock formation after you. It's sturdy. Reliable. Like you.", ConversationPhase.OPENING, "friend"),
        D("Okay, real talk: how's life here? I need to know if I'm missing something.", ConversationPhase.OPENING, "friend"),
        D("Practiced swimming upstream. Got good at it. Also got very tired.", ConversationPhase.OPENING, "friend"),

        # Close friend opening
        D("*sighs* Being here is... nice. Not that I'll admit that to anyone else.", ConversationPhase.OPENING, "close_friend"),
        D("I talk about you on my travels. To rocks, mostly. They're good listeners.", ConversationPhase.OPENING, "close_friend"),
        D("Other ducks ask why I always come back here. I tell them it's strategic.", ConversationPhase.OPENING, "close_friend"),
        D("Remember when we first met? I was lost. Technically still am. Life-wise.", ConversationPhase.OPENING, "close_friend"),
        D("Saving stories just for you. Like emotional hoarding, but healthy. Probably.", ConversationPhase.OPENING, "close_friend"),
        D("No one gets my adventure stories like you do. Everyone else just looks concerned.", ConversationPhase.OPENING, "close_friend"),

        # Best friend opening
        D("*trying not to be emotional* I walked very fast to get here. That's all I'll say about that.", ConversationPhase.OPENING, "best_friend"),
        D("I have a surprise for later. It's a rock. A really good rock.", ConversationPhase.OPENING, "best_friend"),
        D("My family asks about you now. I show them the spot on my map where you are.", ConversationPhase.OPENING, "best_friend"),
        D("Being away from you is the only bad part of exploring. Everything else is just mildly inconvenient.", ConversationPhase.OPENING, "best_friend"),
        D("*quiet* I'm glad you're here. Not everyone stays in one place. I appreciate that you do.", ConversationPhase.OPENING, "best_friend"),
    ],

    # ========== MAIN CONVERSATION ==========
    "main": [
        # Stranger main
        D("I'm mapping waterways. It's tedious. But someone should do it.", ConversationPhase.MAIN, "stranger"),
        D("Ever wonder what's past the treeline? I stopped wondering. Now I just go.", ConversationPhase.MAIN, "stranger"),
        D("My grandpa told me stories about travel. I believed them. That was my first mistake.", ConversationPhase.MAIN, "stranger"),
        D("*shows worn map* See these X marks? Places I've been. Some by choice.", ConversationPhase.MAIN, "stranger"),
        D("Most ducks think I'm strange for traveling. They're not wrong.", ConversationPhase.MAIN, "stranger"),
        D("Key to adventure: always have snacks. Everything else is secondary.", ConversationPhase.MAIN, "stranger"),
        D("Found a cave with crystals once. Got lost in it. Worth it.", ConversationPhase.MAIN, "stranger"),
        D("Do you get the urge to just... leave? No? That's probably healthier.", ConversationPhase.MAIN, "stranger"),
        D("*points to hat* This hat has seen twelve adventures. It's more experienced than me.", ConversationPhase.MAIN, "stranger"),
        D("Finding new ponds is my thing. Yours is nice. Adequate water content.", ConversationPhase.MAIN, "stranger"),
        D("I keep a journal. Mostly it says 'got lost' and 'found bread.'", ConversationPhase.MAIN, "stranger", unlocks_topic="journal"),
        D("Weather prediction is crucial. I'm bad at it. That's what makes it exciting.", ConversationPhase.MAIN, "stranger"),

        # Acquaintance main
        D("Found a waterfall last week. Stood under it. Felt dramatic. Got wet.", ConversationPhase.MAIN, "acquaintance"),
        D("Tried a new route through the forest. Only got lost twice. Personal best.", ConversationPhase.MAIN, "acquaintance"),
        D("Met other explorer ducks. They're all weird. Takes one to know one, I suppose.", ConversationPhase.MAIN, "acquaintance"),
        D("Map collection's growing. Soon I'll have more maps than actual memories.", ConversationPhase.MAIN, "acquaintance"),
        D("Trick to crossing rapids: confidence. And luck. Mostly luck.", ConversationPhase.MAIN, "acquaintance"),
        D("Working on a theory about migration patterns. The theory is that patterns are confusing.", ConversationPhase.MAIN, "acquaintance"),
        D("*shows sketch* Biggest frog I ever saw. Drew it. It's not a good drawing.", ConversationPhase.MAIN, "acquaintance"),
        D("Planning to explore the Northern Marshes next. Could be dangerous. Could be fine.", ConversationPhase.MAIN, "acquaintance"),
        D("Found this rock. It might be valuable. Or just shiny. Unclear.", ConversationPhase.MAIN, "acquaintance"),
        D("Underground rivers exist. I want to find one. Could be a terrible idea.", ConversationPhase.MAIN, "acquaintance"),
        D("Parents worried at first. Now they just want postcards. Rocks count as postcards.", ConversationPhase.MAIN, "acquaintance"),
        D("Explorer's code: Leave only ripples, take only rocks. I added the rocks part.", ConversationPhase.MAIN, "acquaintance"),
        D("Thinking about writing a travel guide. It would mostly say 'don't do what I did.'", ConversationPhase.MAIN, "acquaintance", unlocks_topic="travel_guide"),

        # Friend main
        D("Real talk: that mountain I climbed? Terrifying. Cried a little. Worth it though.", ConversationPhase.MAIN, "friend"),
        D("Want to show you my favorite sunset spot someday. It's far. Very far.", ConversationPhase.MAIN, "friend"),
        D("Best discoveries happen when completely lost. I'm very good at discoveries.", ConversationPhase.MAIN, "friend"),
        D("Met a wise old turtle. He gave me directions. They were wrong.", ConversationPhase.MAIN, "friend"),
        D("*whispers* Found a hidden pond. Called it {duck} Pond. Don't tell anyone.", ConversationPhase.MAIN, "friend"),
        D("Some nights camping under stars, I think about friends. You specifically.", ConversationPhase.MAIN, "friend"),
        D("The world's bigger than most ducks realize. Also scarier. Also prettier.", ConversationPhase.MAIN, "friend"),
        D("Started teaching young ducks about exploring. Mostly it's 'don't die.'", ConversationPhase.MAIN, "friend"),
        D("Compass broke once. Navigated by moss. It actually worked. Shocked everyone.", ConversationPhase.MAIN, "friend"),
        D("There's a legend about a golden fish. Investigating. Will report back.", ConversationPhase.MAIN, "friend"),
        D("Keep a feather from each friend in my journal. Yours is the nicest.", ConversationPhase.MAIN, "friend", requires_topic="journal"),
        D("*shows journal* This page is about you. It just says 'good friend.' That's enough.", ConversationPhase.MAIN, "friend", requires_topic="journal"),
        D("Travel guide's coming along. Dedicated a chapter to kindness. It's short.", ConversationPhase.MAIN, "friend", requires_topic="travel_guide"),
        D("Want to explore somewhere with you someday. No pressure.", ConversationPhase.MAIN, "friend", unlocks_topic="future_adventure"),

        # Close friend main
        D("Between us? Sometimes exploring is lonely. Don't tell the other explorers.", ConversationPhase.MAIN, "close_friend"),
        D("Found a place perfect for us to visit together. It has good rocks.", ConversationPhase.MAIN, "close_friend"),
        D("*quietly* Don't show my real map to just anyone. You're not just anyone.", ConversationPhase.MAIN, "close_friend"),
        D("There's a legend about a hidden paradise. I think it's real. Want to find out?", ConversationPhase.MAIN, "close_friend", unlocks_topic="hidden_paradise"),
        D("Training for a big expedition. The biggest. Might be ridiculous. Probably is.", ConversationPhase.MAIN, "close_friend"),
        D("When things get scary out there, I think about coming back here. To you.", ConversationPhase.MAIN, "close_friend"),
        D("Never told anyone about almost giving up. You're the first. Don't make it weird.", ConversationPhase.MAIN, "close_friend"),
        D("*shows secret pocket* Keep my most precious things here. Including your feather.", ConversationPhase.MAIN, "close_friend"),
        D("Northern Peaks are calling me. Dangerous. But what isn't, really?", ConversationPhase.MAIN, "close_friend"),
        D("Starting to think the journey matters more than the destination. Profound, right?", ConversationPhase.MAIN, "close_friend"),
        D("You're why I don't just wander forever. Needed something to come back to.", ConversationPhase.MAIN, "close_friend"),
        D("Dream about showing you all my favorite places. Long dream. You'd get tired.", ConversationPhase.MAIN, "close_friend", requires_topic="future_adventure"),

        # Best friend main
        D("*deep breath* Planning something huge. Life-changing. Terrifying. Exciting.", ConversationPhase.MAIN, "best_friend"),
        D("You're first to know: found a map to the Paradise Isles. It might be real.", ConversationPhase.MAIN, "best_friend", requires_topic="hidden_paradise"),
        D("When I write my memoir, you get a whole chapter. Longest one.", ConversationPhase.MAIN, "best_friend"),
        D("Got offered to lead an expedition team. Me. Leading. Terrifying.", ConversationPhase.MAIN, "best_friend"),
        D("*holds wing* Whatever adventures come, you're always home. That's not negotiable.", ConversationPhase.MAIN, "best_friend"),
        D("Explored the world. Best discovery? This friendship. Cheesy but true.", ConversationPhase.MAIN, "best_friend"),
        D("The sunset at the peak... wished you were there. Would've been better.", ConversationPhase.MAIN, "best_friend"),
        D("Going to circumnavigate the Great Lake. Want to see me off? No pressure.", ConversationPhase.MAIN, "best_friend"),
        D("*voice wavering* Adventures mean nothing without someone to share them. That's you.", ConversationPhase.MAIN, "best_friend"),
        D("Greatest treasure is true friendship. Found it. Not letting go.", ConversationPhase.MAIN, "best_friend"),
    ],

    # ========== STORIES ==========
    "story": [
        # Acquaintance stories
        D("Picture this: cliff edge. Me. Windy. Dramatic. Then I sneezed.", ConversationPhase.STORY, "acquaintance"),
        D("Got chased by geese once. Not fun. Don't recommend. Zero stars.", ConversationPhase.STORY, "acquaintance"),
        D("*lowers voice* Let me tell you about the Haunted Hollow. Probably not haunted. Probably.", ConversationPhase.STORY, "acquaintance"),
        D("Swimming upstream, suddenly SPLASH. Fish. Very surprised fish. Very surprised me.", ConversationPhase.STORY, "acquaintance"),
        D("Ever heard of the Moss King legend? No? Good. It's unsettling.", ConversationPhase.STORY, "acquaintance"),
        D("Found an old explorer's camp. Journal still there. Last entry: 'Found something amazing.'", ConversationPhase.STORY, "acquaintance"),
        D("*dramatic pause* ...and that's when the storm hit. I made peace with things.", ConversationPhase.STORY, "acquaintance"),
        D("Stuck in a cave for three days. Talked to rocks. They're good company.", ConversationPhase.STORY, "acquaintance"),

        # Friend stories
        D("This story I've told no one. Until now. Don't interrupt.", ConversationPhase.STORY, "friend"),
        D("Remember the golden fish? Well... *glances around* ...I found it.", ConversationPhase.STORY, "friend"),
        D("*sits closer* Okay. The REAL version of what happened. Not the one I tell others.", ConversationPhase.STORY, "friend"),
        D("Crystal Cave wasn't on any map. Found it by accident. Almost didn't leave.", ConversationPhase.STORY, "friend"),
        D("Befriended a hawk once. He showed me the world from above. Changed everything.", ConversationPhase.STORY, "friend"),
        D("There's a tree that's been growing for a thousand years. I touched it. Felt... old.", ConversationPhase.STORY, "friend"),
        D("The night the sky turned green... I'll never forget it. Didn't understand it either.", ConversationPhase.STORY, "friend"),
        D("Discovered a forgotten pond where ducks lived centuries ago. They left things behind.", ConversationPhase.STORY, "friend"),

        # Close friend stories
        D("*voice drops* The Whispering Marsh... almost didn't make it. But here I am.", ConversationPhase.STORY, "close_friend"),
        D("This is the story I couldn't tell anyone. Until you.", ConversationPhase.STORY, "close_friend"),
        D("Met another explorer out there. She taught me everything. She's gone now.", ConversationPhase.STORY, "close_friend"),
        D("Finding the underground river... changed me. Can't explain how.", ConversationPhase.STORY, "close_friend"),
        D("My mentor disappeared on an expedition. Still looking. Always looking.", ConversationPhase.STORY, "close_friend"),
        D("Midnight Mountain peak at sunrise... stood there and cried. Good tears.", ConversationPhase.STORY, "close_friend"),
        D("Discovered ruins. Ancient duck ruins. No one believed me. But I know.", ConversationPhase.STORY, "close_friend"),

        # Best friend stories
        D("*deep breath* Never told anyone the full truth. Here goes.", ConversationPhase.STORY, "best_friend"),
        D("The reason I became an explorer... starts with loss. Ends with hope.", ConversationPhase.STORY, "best_friend"),
        D("I found it, {duck}. The legendary Sanctuary. It exists. I wept.", ConversationPhase.STORY, "best_friend"),
        D("At my lowest point, almost gave up everything. Then I thought of coming home.", ConversationPhase.STORY, "best_friend"),
        D("Greatest adventure wasn't a place. It was realizing what matters.", ConversationPhase.STORY, "best_friend"),
        D("When I discovered the Paradise Isles... cried for an hour. Beautiful crying.", ConversationPhase.STORY, "best_friend"),
    ],

    # ========== PERSONAL ==========
    "personal": [
        # Friend personal
        D("Can I be honest? Sometimes I'm scared out there. Often, actually.", ConversationPhase.PERSONAL, "friend"),
        D("Wonder if I explore to run away from something. Haven't figured out what.", ConversationPhase.PERSONAL, "friend"),
        D("Family doesn't understand why I do this. Neither do I, sometimes.", ConversationPhase.PERSONAL, "friend"),
        D("You're one of the only ducks who takes me seriously. That matters.", ConversationPhase.PERSONAL, "friend"),
        D("Not as brave as I pretend. The hat is mostly for morale.", ConversationPhase.PERSONAL, "friend"),
        D("Having a friend like you... means more than you know. Probably should say that more.", ConversationPhase.PERSONAL, "friend"),

        # Close friend personal
        D("*quietly* Sometimes wonder if I'll ever settle down. Probably not. Maybe.", ConversationPhase.PERSONAL, "close_friend"),
        D("Truth is... looking for somewhere I belong. Haven't found it on maps.", ConversationPhase.PERSONAL, "close_friend"),
        D("Dreams are too big. Everyone says so. Can't seem to make them smaller.", ConversationPhase.PERSONAL, "close_friend"),
        D("You make me feel like I don't have to prove anything. That's rare.", ConversationPhase.PERSONAL, "close_friend"),
        D("When I'm with you, the wanderlust quiets down. Just a little.", ConversationPhase.PERSONAL, "close_friend"),
        D("Been alone a lot. But not lonely. Not anymore.", ConversationPhase.PERSONAL, "close_friend"),
        D("*looks away* Scared of losing the ducks I care about. That's you, by the way.", ConversationPhase.PERSONAL, "close_friend"),

        # Best friend personal
        D("*emotional but trying not to show it* Never felt so accepted. That's... a lot.", ConversationPhase.PERSONAL, "best_friend"),
        D("You're my home, {duck}. Wherever I roam. Always come back to you.", ConversationPhase.PERSONAL, "best_friend"),
        D("Decided something. Want to build a life here. Near you. If that's okay.", ConversationPhase.PERSONAL, "best_friend"),
        D("Adventures were always about finding something. Found it. It's friendship.", ConversationPhase.PERSONAL, "best_friend"),
        D("*holds wing* Will you always be here when I return? I need to know.", ConversationPhase.PERSONAL, "best_friend"),
        D("I love you, {duck}. Like family. Like home. Like the best parts of everywhere.", ConversationPhase.PERSONAL, "best_friend"),
        D("My greatest discovery wasn't a place. It was you.", ConversationPhase.PERSONAL, "best_friend"),
    ],

    # ========== ACTIVITY ==========
    "activity": [
        # Stranger activity
        D("Want to look at my map collection? No pressure. They're just maps.", ConversationPhase.ACTIVITY, "stranger"),
        D("Could... look at clouds? Imagine they're mountains? No? Fair.", ConversationPhase.ACTIVITY, "stranger"),

        # Acquaintance activity
        D("Short walk around the pond? I'll try not to get lost.", ConversationPhase.ACTIVITY, "acquaintance"),
        D("Want to practice compass reading? I'm... adequate at teaching.", ConversationPhase.ACTIVITY, "acquaintance"),
        D("Could teach you explorer signals. They're mostly waving.", ConversationPhase.ACTIVITY, "acquaintance"),

        # Friend activity
        D("Something fun? Stargazing? Treasure hunt? Both involve looking at things.", ConversationPhase.ACTIVITY, "friend"),
        D("Explore the edge of your territory together? Promise not to go too far.", ConversationPhase.ACTIVITY, "friend"),
        D("Race across the pond? Loser admits they're the loser. Simple.", ConversationPhase.ACTIVITY, "friend"),
        D("Draw a map of your pond together? I'll try to make it accurate.", ConversationPhase.ACTIVITY, "friend"),

        # Close friend activity
        D("One day we HAVE to go on a real adventure together. One day.", ConversationPhase.ACTIVITY, "close_friend"),
        D("Want to see the secret grove? It's secret. But you're invited.", ConversationPhase.ACTIVITY, "close_friend"),
        D("Let's make a pact: someday, the mountains. Together.", ConversationPhase.ACTIVITY, "close_friend"),

        # Best friend activity
        D("Pack your things, {duck}. We're going somewhere. Short trip. Maybe long.", ConversationPhase.ACTIVITY, "best_friend"),
        D("Perfect trip planned. Just us. Minimal danger. Maximum rocks.", ConversationPhase.ACTIVITY, "best_friend"),
        D("Want to discover something amazing together? I have coordinates.", ConversationPhase.ACTIVITY, "best_friend"),
    ],

    # ========== CLOSING ==========
    "closing": [
        # Stranger closing
        D("Should probably get going. Places to be. Allegedly.", ConversationPhase.CLOSING, "stranger"),
        D("Thanks for letting me rest here. Adequate hospitality.", ConversationPhase.CLOSING, "stranger"),
        D("Maybe I'll stop by again. If I can find my way back.", ConversationPhase.CLOSING, "stranger"),
        D("You're nicer than most ducks I meet. Low bar, but still.", ConversationPhase.CLOSING, "stranger"),

        # Acquaintance closing
        D("Time flies when you're talking about getting lost. Ironic.", ConversationPhase.CLOSING, "acquaintance"),
        D("Enjoyed this. We should do it again. If I remember where you are.", ConversationPhase.CLOSING, "acquaintance"),
        D("*stretches* Road calls. But I'll be back. Probably.", ConversationPhase.CLOSING, "acquaintance"),
        D("Same time next week? I'll try to show up. No guarantees.", ConversationPhase.CLOSING, "acquaintance"),

        # Friend closing
        D("Never want these hangouts to end. But they do. That's time for you.", ConversationPhase.CLOSING, "friend"),
        D("*sighs* This was exactly what I needed. Don't tell anyone I said that.", ConversationPhase.CLOSING, "friend"),
        D("Promise you won't forget me between visits? I'll forget things, but not you.", ConversationPhase.CLOSING, "friend"),
        D("Until next time, friend. Stay exactly where you are.", ConversationPhase.CLOSING, "friend"),

        # Close friend closing
        D("Leaving is always the hardest part. Everything else is just walking.", ConversationPhase.CLOSING, "close_friend"),
        D("*unexpected hug* I'm gonna miss you. A lot. Don't make it weird.", ConversationPhase.CLOSING, "close_friend"),
        D("My heart stays here. Rest of me has to go. Logistics.", ConversationPhase.CLOSING, "close_friend"),
        D("Count the days until I'm back. I will be. That's a promise.", ConversationPhase.CLOSING, "close_friend"),

        # Best friend closing
        D("*trying not to be emotional* Every goodbye with you is too soon.", ConversationPhase.CLOSING, "best_friend"),
        D("Carrying this moment everywhere I go. It weighs nothing. Means everything.", ConversationPhase.CLOSING, "best_friend"),
        D("This isn't goodbye. It's 'see you soon.' There's a difference.", ConversationPhase.CLOSING, "best_friend"),
        D("*holds wing* You're my greatest treasure. Better than any rock.", ConversationPhase.CLOSING, "best_friend"),
    ],

    # ========== FAREWELL ==========
    "farewell": [
        # Stranger farewell
        D("Bye. Maybe see you around. Probably not. But maybe.", ConversationPhase.FAREWELL, "stranger"),
        D("*tips hat* Until next time. If there is one.", ConversationPhase.FAREWELL, "stranger"),
        D("Safe waters. Thanks for the chat. It was... adequate.", ConversationPhase.FAREWELL, "stranger"),
        D("Gotta keep moving. That's the explorer way. Also I'm bad at goodbyes.", ConversationPhase.FAREWELL, "stranger"),

        # Acquaintance farewell
        D("*waves* See you, {duck}. Stay where you are.", ConversationPhase.FAREWELL, "acquaintance"),
        D("Adventure awaits. But I'll be back. Probably.", ConversationPhase.FAREWELL, "acquaintance"),
        D("Keep this pond safe for me. I'll need somewhere to rest.", ConversationPhase.FAREWELL, "acquaintance"),
        D("*salutes* Until next adventure. Or next visit. Same thing.", ConversationPhase.FAREWELL, "acquaintance"),

        # Friend farewell
        D("*brief hug* Take care, {duck}. You're one of the good ones.", ConversationPhase.FAREWELL, "friend"),
        D("Bringing you something cool next time. Probably a rock.", ConversationPhase.FAREWELL, "friend"),
        D("Think of me when you see stars. I'll be under them somewhere.", ConversationPhase.FAREWELL, "friend"),
        D("*reluctantly leaving* Bye, buddy. Miss you already. That's inconvenient.", ConversationPhase.FAREWELL, "friend"),

        # Close friend farewell
        D("*long hug* I love you, friend. See you soon. Very soon.", ConversationPhase.FAREWELL, "close_friend"),
        D("*wiping eyes* Okay okay, going now. *doesn't move* ...Now I'm going.", ConversationPhase.FAREWELL, "close_friend"),
        D("Stars will guide me back to you, {duck}. That's not a metaphor. I use stars.", ConversationPhase.FAREWELL, "close_friend"),
        D("*waves from distance* STILL MISS YOU. WILL KEEP MISSING YOU.", ConversationPhase.FAREWELL, "close_friend"),

        # Best friend farewell
        D("*emotional* My soul stays here with you. Only slightly dramatic.", ConversationPhase.FAREWELL, "best_friend"),
        D("Every step away makes me want to turn back. But I'll return. Always.", ConversationPhase.FAREWELL, "best_friend"),
        D("This isn't goodbye. This is 'I love you, see you soon.'", ConversationPhase.FAREWELL, "best_friend"),
        D("*turns back one more time* You're my everything, {duck}. Not exaggerating.", ConversationPhase.FAREWELL, "best_friend"),
        D("*leaving but looking back* Best friends forever. That's not a question.", ConversationPhase.FAREWELL, "best_friend"),
    ],
}

# Register with main dialogue system
DIALOGUE_TREES["adventurous"] = ADVENTUROUS_DIALOGUE
