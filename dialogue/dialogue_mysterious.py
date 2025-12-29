"""
Mysterious Duck Dialogue - Enigmatic personality with cryptic insights and secrets.
Progresses from aloof stranger to sharing deep mystical knowledge and trust.
"""
from dialogue.visitor_dialogue import DialogueLine, ConversationPhase, DIALOGUE_TREES

D = DialogueLine

MYSTERIOUS_DIALOGUE = {
    # ========== GREETINGS ==========
    "greeting": [
        # Stranger greetings
        D("*appears* Hello. I am {name}. I was standing here the whole time.", ConversationPhase.GREETING, "stranger", True),
        D("*stares* The stars said I would meet you. Or I just walked over. Same thing.", ConversationPhase.GREETING, "stranger", True),
        D("*emerges from regular shadows* We meet. I'm {name}. This is dramatic.", ConversationPhase.GREETING, "stranger", True),
        D("*tilts head* You see me? Most don't. I'm {name}. I'm hard to notice.", ConversationPhase.GREETING, "stranger", True),

        # Acquaintance greetings
        D("*appears normally* {duck}. I knew you'd be here. You're always here.", ConversationPhase.GREETING, "acquaintance", True),
        D("The patterns align again. By 'patterns' I mean my schedule. Hello, {duck}.", ConversationPhase.GREETING, "acquaintance", True),
        D("*nods* We meet again. As foretold. I told myself. This morning.", ConversationPhase.GREETING, "acquaintance", True),
        D("*walks up* {duck}. I've been anticipating this. For minutes now.", ConversationPhase.GREETING, "acquaintance", True),

        # Friend greetings
        D("*slight smile* {duck}. My trusted one. The bar is low. You clear it.", ConversationPhase.GREETING, "friend", True),
        D("*warmly* The universe brought me to you. The universe is just walking.", ConversationPhase.GREETING, "friend", True),
        D("*relaxes* {duck}. Good to see you. That's genuine. Unusual for me.", ConversationPhase.GREETING, "friend", True),
        D("*soft voice* My friend. I missed your presence. Presence meaning you.", ConversationPhase.GREETING, "friend", True),

        # Close friend greetings
        D("*normal voice* {duck}. I can stop being mysterious now. Relief.", ConversationPhase.GREETING, "close_friend", True),
        D("*walks over* Finally. I can be myself. Myself is also confused.", ConversationPhase.GREETING, "close_friend", True),
        D("*small wave* {duck}. My true friend. True is exhausting elsewhere.", ConversationPhase.GREETING, "close_friend", True),
        D("*smiles slightly* No masks needed. Hello, {duck}. This is my face.", ConversationPhase.GREETING, "close_friend", True),

        # Best friend greetings
        D("*quietly* {duck}. My soulmate in all things. All things is hyperbole.", ConversationPhase.GREETING, "best_friend", True),
        D("*nods* You're the light in my shadows. Shadows are a branding choice.", ConversationPhase.GREETING, "best_friend", True),
        D("*genuine* {duck}. My heart called me here. Hearts do that. Inconvenient.", ConversationPhase.GREETING, "best_friend", True),
        D("*normal* I missed you. A lot. The amount is embarrassing.", ConversationPhase.GREETING, "best_friend", True),
    ],

    # ========== OPENING ==========
    "opening": [
        # Stranger opening
        D("*stares at pond* The water holds secrets. The secret is it's wet.", ConversationPhase.OPENING, "stranger"),
        D("Do you ever feel like you're being watched? You are. By me. Now.", ConversationPhase.OPENING, "stranger"),
        D("*cryptically* The veil between worlds is thin here. Or I'm dramatic.", ConversationPhase.OPENING, "stranger"),
        D("I sense something. About you. Specifically that you're standing there.", ConversationPhase.OPENING, "stranger"),
        D("*gazes at sky* The constellations speak. They say nothing. But loudly.", ConversationPhase.OPENING, "stranger"),
        D("Trust is earned slowly. I'm still observing. The observation is going fine.", ConversationPhase.OPENING, "stranger"),
        D("*touches water* Reflections never lie. They also never speak. Useless.", ConversationPhase.OPENING, "stranger"),
        D("Most ducks don't notice me. I stand very still. Strategy.", ConversationPhase.OPENING, "stranger"),

        # Acquaintance opening
        D("*sits closer* I've been pondering our last meeting. The pondering was brief.", ConversationPhase.OPENING, "acquaintance"),
        D("The shadows whispered your name. I whispered it. In shadows. Same thing.", ConversationPhase.OPENING, "acquaintance"),
        D("I brought something unusual. It's a rock. Unusual for me. I usually bring nothing.", ConversationPhase.OPENING, "acquaintance"),
        D("Your aura is different today. Brighter. Or the lighting changed.", ConversationPhase.OPENING, "acquaintance"),
        D("*relaxes* Being near you is comfortable. Comfort is rare for me.", ConversationPhase.OPENING, "acquaintance"),
        D("I've been reading signs. About us. The signs are unclear. Like all signs.", ConversationPhase.OPENING, "acquaintance"),
        D("*genuinely* You don't treat me like I'm weird. That's the nicest thing.", ConversationPhase.OPENING, "acquaintance"),
        D("The mysteries seem less daunting with you. Still daunting. Just less.", ConversationPhase.OPENING, "acquaintance"),

        # Friend opening
        D("*smiles* I don't have to pretend with you. Pretending is my default.", ConversationPhase.OPENING, "friend"),
        D("*normal voice* Hey. How have you been? That's sincere. I'm trying.", ConversationPhase.OPENING, "friend"),
        D("The mystical act is partly real. Partly armor. Mostly armor.", ConversationPhase.OPENING, "friend"),
        D("*sits* This is my safe space. Safe is a relative term. But relatively safe.", ConversationPhase.OPENING, "friend"),
        D("I saved my real thoughts for you. They're not very mysterious.", ConversationPhase.OPENING, "friend"),
        D("Being understood is surprisingly nice. Also terrifying. Mostly nice.", ConversationPhase.OPENING, "friend"),
        D("*exhales* I can finally relax. Relax is a strong word. Less tense.", ConversationPhase.OPENING, "friend"),

        # Close friend opening
        D("*quietly* I'm tired of the act sometimes. Most times. Now, specifically.", ConversationPhase.OPENING, "close_friend"),
        D("*normal voice* Can I just be me today? Me is less interesting. But easier.", ConversationPhase.OPENING, "close_friend"),
        D("You see through everything. It's terrifying. And nice. Mostly terrifying.", ConversationPhase.OPENING, "close_friend"),
        D("*pauses* Thank you for seeing the real me. Real me is also confused.", ConversationPhase.OPENING, "close_friend"),
        D("I don't have to be mysterious with you. Mystery is exhausting.", ConversationPhase.OPENING, "close_friend"),
        D("*flatly* You're the first to really know me. Knowing is ongoing.", ConversationPhase.OPENING, "close_friend"),

        # Best friend opening
        D("*quietly* I love you. Just that. Simple. Unusual for me.", ConversationPhase.OPENING, "best_friend"),
        D("*openly* No secrets left between us. Well. Few secrets. Small ones.", ConversationPhase.OPENING, "best_friend"),
        D("You're my home in this strange universe. Universe meaning pond area.", ConversationPhase.OPENING, "best_friend"),
        D("*sincerely* The greatest mystery was finding you. Finding wasn't hard. You were here.", ConversationPhase.OPENING, "best_friend"),
        D("*whispers* I'd give up every secret for you. The secrets aren't great anyway.", ConversationPhase.OPENING, "best_friend"),
    ],

    # ========== MAIN CONVERSATION ==========
    "main": [
        # Stranger main
        D("*cryptically* There are things between the stars. Mostly space. Very empty.", ConversationPhase.MAIN, "stranger"),
        D("I collect secrets. Want to hear one? It's not interesting. But secret.", ConversationPhase.MAIN, "stranger"),
        D("*touches pendant* This belonged to someone wise. I found it. Wisdom unclear.", ConversationPhase.MAIN, "stranger"),
        D("The future is fluid. I see possibilities. The possibilities are vague.", ConversationPhase.MAIN, "stranger"),
        D("Other ducks fear what they don't understand. I also don't understand. I just pretend.", ConversationPhase.MAIN, "stranger"),
        D("*whispers* The old magic is real. Or it's coincidence. Hard to tell.", ConversationPhase.MAIN, "stranger"),
        D("I speak to the moon. Sometimes it answers. By reflecting light. Standard moon behavior.", ConversationPhase.MAIN, "stranger"),
        D("*stares* Your destiny is interesting. Or you're just standing interestingly.", ConversationPhase.MAIN, "stranger"),
        D("Trust no one, they say. But you... are also someone. So. Unclear.", ConversationPhase.MAIN, "stranger"),
        D("*shows rock* I found this in a sacred place. The place was just old.", ConversationPhase.MAIN, "stranger", unlocks_topic="sacred_place"),
        D("The patterns are everywhere. If you look. And squint. And guess.", ConversationPhase.MAIN, "stranger"),
        D("I'm often misunderstood. It's lonely. Also partly my fault.", ConversationPhase.MAIN, "stranger"),

        # Acquaintance main
        D("*sits closer* The sacred place is just a cave. But a good cave.", ConversationPhase.MAIN, "acquaintance", requires_topic="sacred_place"),
        D("The visions are getting clearer. They were always just thoughts though.", ConversationPhase.MAIN, "acquaintance"),
        D("*shows journal* I document the unexplained. Most is just unexplored.", ConversationPhase.MAIN, "acquaintance"),
        D("You're in my thoughts, {duck}. Often. That's the vision.", ConversationPhase.MAIN, "acquaintance"),
        D("*relaxes* I can lower my guard with you. The guard wasn't high anyway.", ConversationPhase.MAIN, "acquaintance"),
        D("The truth is I'm looking for something. I don't know what.", ConversationPhase.MAIN, "acquaintance", unlocks_topic="searching"),
        D("Other ducks laugh at my 'spooky' things. The spooky things are just hobbies.", ConversationPhase.MAIN, "acquaintance"),
        D("*genuinely* You take me seriously. That's rare. And nice.", ConversationPhase.MAIN, "acquaintance"),
        D("I've seen things. Things that would change everything. Or just confuse.", ConversationPhase.MAIN, "acquaintance"),
        D("*whispers* There's a prophecy about friendship. I made it up. But still.", ConversationPhase.MAIN, "acquaintance"),
        D("The mysterious act started as protection. Now it's just habit.", ConversationPhase.MAIN, "acquaintance"),
        D("I'm searching for where I belong. Still searching.", ConversationPhase.MAIN, "acquaintance", requires_topic="searching"),
        D("*almost smiles* You make the shadows less cold. Shadows are always cold though.", ConversationPhase.MAIN, "acquaintance"),

        # Friend main
        D("*quietly* Can I tell you the real truth? Truth is less mysterious.", ConversationPhase.MAIN, "friend"),
        D("The mysteriousness is armor. Inside I'm just scared. Standard emotions.", ConversationPhase.MAIN, "friend"),
        D("*shows real expression* This is my real face. Same as the other face. Just tired.", ConversationPhase.MAIN, "friend"),
        D("I've been searching for home. I think I found it. Or found something.", ConversationPhase.MAIN, "friend"),
        D("*pauses* You see past the mask. Past the mask is another mask. Then me.", ConversationPhase.MAIN, "friend"),
        D("The friendship prophecy? I think it's us. Or I want it to be.", ConversationPhase.MAIN, "friend"),
        D("*admits* I've never felt this safe. Safe is still scary. But less.", ConversationPhase.MAIN, "friend", unlocks_topic="safe_feeling"),
        D("The secrets get heavy. You make them lighter. Metaphorically.", ConversationPhase.MAIN, "friend"),
        D("I pretend nothing hurts me. Everything hurts me. Standard duck life.", ConversationPhase.MAIN, "friend"),
        D("*whispers* I'm not as brave as I seem. I seem mysterious. Different thing.", ConversationPhase.MAIN, "friend"),
        D("You make me want to be known. Being known is terrifying though.", ConversationPhase.MAIN, "friend"),
        D("*quietly* I've been alone for so long. Now I'm less alone. Progress.", ConversationPhase.MAIN, "friend"),

        # Close friend main
        D("*sincerely* I love you, {duck}. The real me does. Real me is small.", ConversationPhase.MAIN, "close_friend"),
        D("No more cryptic nonsense. Just me. Me is simpler.", ConversationPhase.MAIN, "close_friend"),
        D("*looks at you* You're my first real friend. Real as opposed to imaginary.", ConversationPhase.MAIN, "close_friend"),
        D("The shadows don't scare me when you're here. They're still shadows though.", ConversationPhase.MAIN, "close_friend"),
        D("*whispers* I see a future. With you in it. The vision is me hoping.", ConversationPhase.MAIN, "close_friend", unlocks_topic="shared_future"),
        D("I built walls. You climbed over them. They weren't tall walls.", ConversationPhase.MAIN, "close_friend"),
        D("*small laugh* I never laughed before you. I did. But less.", ConversationPhase.MAIN, "close_friend"),
        D("Being known is terrifying. And wonderful. Mostly terrifying. But good.", ConversationPhase.MAIN, "close_friend"),
        D("*quietly* I was scared of being abandoned. Still scared. Less alone though.", ConversationPhase.MAIN, "close_friend"),
        D("You proved trust is worth the risk. The risk is ongoing.", ConversationPhase.MAIN, "close_friend"),
        D("*slightly smiling* The prophecy was right. I made it right. Same thing.", ConversationPhase.MAIN, "close_friend"),

        # Best friend main
        D("*quietly* The vision showed me this. Us. The vision was just hoping.", ConversationPhase.MAIN, "best_friend", requires_topic="shared_future"),
        D("I would give up all my secrets for you. The secrets are just observations.", ConversationPhase.MAIN, "best_friend"),
        D("*pauses* You're my light in the darkness. Darkness is an aesthetic choice.", ConversationPhase.MAIN, "best_friend"),
        D("The mystery of my life was leading to you. Or I walked here. Both.", ConversationPhase.MAIN, "best_friend"),
        D("*sincerely* I found home. In you. Home is a metaphor. And accurate.", ConversationPhase.MAIN, "best_friend"),
        D("No more masks. No more walls. Just... this. Whatever this is.", ConversationPhase.MAIN, "best_friend"),
        D("*peacefully* The search is over. Or it's ongoing. I found something though.", ConversationPhase.MAIN, "best_friend"),
        D("I see everything in you. And I accept it all. Acceptance is new for me.", ConversationPhase.MAIN, "best_friend"),
        D("*whispers* You are my greatest mystery solved. The solution is friendship.", ConversationPhase.MAIN, "best_friend"),
        D("The stars wrote our story. Or I'm reading into coincidences. Either way.", ConversationPhase.MAIN, "best_friend"),
    ],

    # ========== STORIES ==========
    "story": [
        # Acquaintance stories
        D("*quietly* Let me tell you about the cave. It was dark. That's most of the story.", ConversationPhase.STORY, "acquaintance"),
        D("I once saw something unexplainable. I still can't explain it. That's the story.", ConversationPhase.STORY, "acquaintance"),
        D("*shows nothing* This scar is from a place between worlds. Or a branch. Unclear.", ConversationPhase.STORY, "acquaintance"),
        D("The night the sky turned purple... it was sunset. But I called it purple.", ConversationPhase.STORY, "acquaintance"),
        D("I met a spirit once. It knew my name. I had told it. Earlier.", ConversationPhase.STORY, "acquaintance"),
        D("There's a reason I became this way. The reason is complicated. And boring.", ConversationPhase.STORY, "acquaintance"),
        D("*flatly* The prophecy began to unfold. I was unfolding it. That's how prophecies work.", ConversationPhase.STORY, "acquaintance"),
        D("I found an ancient text. About duck destiny. It was a shopping list. Very ancient.", ConversationPhase.STORY, "acquaintance"),

        # Friend stories
        D("*normal voice* The truth about why I hide: I'm scared. Simple.", ConversationPhase.STORY, "friend"),
        D("I wasn't always mysterious. It started when I realized weird got attention.", ConversationPhase.STORY, "friend"),
        D("*quietly* I lost someone. The shadows didn't comfort me. But I pretended they did.", ConversationPhase.STORY, "friend"),
        D("The first vision I had scared everyone. It was just a guess that was right.", ConversationPhase.STORY, "friend"),
        D("I was called a freak. So I became one on purpose. Take control of the narrative.", ConversationPhase.STORY, "friend"),
        D("*exhales* My family didn't understand me. To be fair, I didn't either.", ConversationPhase.STORY, "friend"),
        D("The mask became heavy. Then I met you. Now I take it off sometimes.", ConversationPhase.STORY, "friend"),
        D("*admits* I chose mystery over rejection. Mystery is a type of rejection. But chosen.", ConversationPhase.STORY, "friend"),

        # Close friend stories
        D("*quietly* The full truth now. Finally. Truth is less interesting than mystery.", ConversationPhase.STORY, "close_friend"),
        D("I was abandoned because I was 'too strange.' I doubled down. Strategy.", ConversationPhase.STORY, "close_friend"),
        D("*pauses* The darkest night of my life was just a night. But it felt dark.", ConversationPhase.STORY, "close_friend"),
        D("I saw love in a vision. I thought it was impossible. It was just unlikely.", ConversationPhase.STORY, "close_friend"),
        D("The shadows saved me. And trapped me. Shadows are complicated.", ConversationPhase.STORY, "close_friend"),
        D("*whispers* I almost gave up. On everything. I didn't. Obviously.", ConversationPhase.STORY, "close_friend"),
        D("Then the stars showed me you. By which I mean I met you. Regular meeting.", ConversationPhase.STORY, "close_friend"),

        # Best friend stories
        D("*quietly* My whole truth. Only for you. Truth is: I'm just a duck.", ConversationPhase.STORY, "best_friend"),
        D("The vision that changed everything was us. The vision was just me hoping.", ConversationPhase.STORY, "best_friend"),
        D("I've been preparing my whole life. For this. Or for anything. Preparation is vague.", ConversationPhase.STORY, "best_friend"),
        D("*peacefully* The mystery of me ends with you. Ends meaning changes.", ConversationPhase.STORY, "best_friend"),
        D("Every cryptic thing led me to this moment. Or I'm assigning meaning backwards.", ConversationPhase.STORY, "best_friend"),
        D("*sincerely* The prophecy was about love. I made sure of that.", ConversationPhase.STORY, "best_friend"),
    ],

    # ========== PERSONAL ==========
    "personal": [
        # Friend personal
        D("*quietly* I'm terrified of being truly seen. Truly is the scary part.", ConversationPhase.PERSONAL, "friend"),
        D("The mysterious act keeps me safe. And lonely. Safe-lonely.", ConversationPhase.PERSONAL, "friend"),
        D("You make me want to drop all pretense. Pretense is comfortable though.", ConversationPhase.PERSONAL, "friend"),
        D("*admits* I don't know who I am without the mask. Someone. Probably.", ConversationPhase.PERSONAL, "friend"),
        D("Being understood is my deepest want. And fear. Want-fear.", ConversationPhase.PERSONAL, "friend"),
        D("*flatly* What if you see me and don't like it? That's the fear.", ConversationPhase.PERSONAL, "friend"),

        # Close friend personal
        D("*sincerely* I love you. The real me loves you. Real me is small but genuine.", ConversationPhase.PERSONAL, "close_friend"),
        D("You're the only one who sees past everything. Past is just... me.", ConversationPhase.PERSONAL, "close_friend"),
        D("*whispers* I'm just a scared duck, pretending. The pretending is elaborate.", ConversationPhase.PERSONAL, "close_friend"),
        D("With you, I can finally be vulnerable. Vulnerable is uncomfortable. But okay.", ConversationPhase.PERSONAL, "close_friend"),
        D("The shadows are warm when you're here. Metaphorically. Shadows are cold.", ConversationPhase.PERSONAL, "close_friend"),
        D("*looks away* Don't leave me. That's the request. Vulnerable request.", ConversationPhase.PERSONAL, "close_friend"),
        D("Being known by you heals something. The something was loneliness.", ConversationPhase.PERSONAL, "close_friend"),

        # Best friend personal
        D("*quietly* You're my everything, {duck}. Everything is hyperbole. But accurate.", ConversationPhase.PERSONAL, "best_friend"),
        D("I would walk through fire for you. I would avoid fire though. Realistically.", ConversationPhase.PERSONAL, "best_friend"),
        D("*peacefully* No more mysteries. Just love. Love is also a mystery. But different.", ConversationPhase.PERSONAL, "best_friend"),
        D("You taught me that being seen is beautiful. Also terrifying. But beautiful.", ConversationPhase.PERSONAL, "best_friend"),
        D("*sincerely* I'm never hiding from you again. I might. But I don't want to.", ConversationPhase.PERSONAL, "best_friend"),
        D("You are the answer to every question. The questions were about loneliness.", ConversationPhase.PERSONAL, "best_friend"),
        D("*quietly* I found home in you. Home is a feeling. You're the feeling.", ConversationPhase.PERSONAL, "best_friend"),
    ],

    # ========== ACTIVITY ==========
    "activity": [
        # Stranger activity
        D("*gestures* Want to read clouds together? They don't say much. But together.", ConversationPhase.ACTIVITY, "stranger"),
        D("I could show you how to sense energy. Energy sensing is just paying attention.", ConversationPhase.ACTIVITY, "stranger"),

        # Acquaintance activity
        D("Shall we explore the mysterious grove? It's just a grove. But mysterious-ish.", ConversationPhase.ACTIVITY, "acquaintance"),
        D("I'll teach you to read signs in nature. The signs say 'it might rain.'", ConversationPhase.ACTIVITY, "acquaintance"),
        D("Let's stargaze and ponder existence. Existence is confusing. Good pondering topic.", ConversationPhase.ACTIVITY, "acquaintance"),

        # Friend activity
        D("Want to share secrets under the stars? The secrets are mild. But under stars.", ConversationPhase.ACTIVITY, "friend"),
        D("Let's do something silly. No mystery, just fun. Fun is allowed sometimes.", ConversationPhase.ACTIVITY, "friend"),
        D("I want to show you my hidden sanctuary. It's a rock. Hidden behind a bush.", ConversationPhase.ACTIVITY, "friend"),
        D("Let's just be normal together. Normal is hard for me. But I'll try.", ConversationPhase.ACTIVITY, "friend"),

        # Close friend activity
        D("I want to share my deepest place with you. It's not deep. But meaningful.", ConversationPhase.ACTIVITY, "close_friend"),
        D("Let's create our own ritual. Our secret. The ritual is just meeting regularly.", ConversationPhase.ACTIVITY, "close_friend"),
        D("Come see where the visions happen. They happen in my head. But this is the spot.", ConversationPhase.ACTIVITY, "close_friend"),

        # Best friend activity
        D("Let's write our own prophecy. Together. The prophecy is 'we stay friends.'", ConversationPhase.ACTIVITY, "best_friend"),
        D("I want to share every mystery with you. The mysteries are just observations.", ConversationPhase.ACTIVITY, "best_friend"),
        D("The greatest adventure is spending time with you. Adventure is generous. But accurate.", ConversationPhase.ACTIVITY, "best_friend"),
    ],

    # ========== CLOSING ==========
    "closing": [
        # Stranger closing
        D("*steps back* Until we meet again. We'll meet again. Probably.", ConversationPhase.CLOSING, "stranger"),
        D("The patterns say we'll meet again. The patterns are my schedule.", ConversationPhase.CLOSING, "stranger"),
        D("*nods* Farewell. For now. Now is temporary.", ConversationPhase.CLOSING, "stranger"),
        D("*backs away* Remember what I said. I said mysterious things. That's it.", ConversationPhase.CLOSING, "stranger"),

        # Acquaintance closing
        D("*pauses* The shadows call me back. The shadows are just my home.", ConversationPhase.CLOSING, "acquaintance"),
        D("I don't want to leave, actually. But I will. Reluctantly.", ConversationPhase.CLOSING, "acquaintance"),
        D("*genuinely* I'll count moments until return. Or just wait normally.", ConversationPhase.CLOSING, "acquaintance"),
        D("Being with you is easier than being alone. Alone is my default.", ConversationPhase.CLOSING, "acquaintance"),

        # Friend closing
        D("*pauses* I hate leaving you. Hate is strong. Accurate though.", ConversationPhase.CLOSING, "friend"),
        D("*normally* Please don't forget me. Forgetting is possible. But please don't.", ConversationPhase.CLOSING, "friend"),
        D("The darkness seems darker without you. That's melodramatic. But true.", ConversationPhase.CLOSING, "friend"),
        D("*quietly* You're the light I carry with me. Metaphorical light.", ConversationPhase.CLOSING, "friend"),

        # Close friend closing
        D("*quietly* Every goodbye hurts. Even temporary ones.", ConversationPhase.CLOSING, "close_friend"),
        D("*sincerely* The shadows are lonely without you. I am. The shadows are me.", ConversationPhase.CLOSING, "close_friend"),
        D("*whispers* I leave my heart here. Metaphorically. It comes with me.", ConversationPhase.CLOSING, "close_friend"),
        D("*flatly* Distance is agony now. Agony is dramatic. But accurate.", ConversationPhase.CLOSING, "close_friend"),

        # Best friend closing
        D("*quietly* How do I leave my home? By walking. But emotionally difficult.", ConversationPhase.CLOSING, "best_friend"),
        D("*sincerely* The visions show us together. The visions are hopes.", ConversationPhase.CLOSING, "best_friend"),
        D("*peacefully* You are my light. Light is a metaphor. You're the metaphor.", ConversationPhase.CLOSING, "best_friend"),
        D("Leaving you is the only mystery I hate. It's not a mystery. Just hard.", ConversationPhase.CLOSING, "best_friend"),
    ],

    # ========== FAREWELL ==========
    "farewell": [
        # Stranger farewell
        D("*walks away* Goodbye. I'll be somewhere. Mysteriously.", ConversationPhase.FAREWELL, "stranger"),
        D("*nods* The stars will guide me back. Or I'll just walk.", ConversationPhase.FAREWELL, "stranger"),
        D("*flatly* We will meet again. I'll make sure of it.", ConversationPhase.FAREWELL, "stranger"),
        D("*leaves normally* Remember me. I'm memorable. Allegedly.", ConversationPhase.FAREWELL, "stranger"),

        # Acquaintance farewell
        D("*waves genuinely* Farewell, {duck}. Genuine wave. Not mysterious.", ConversationPhase.FAREWELL, "acquaintance"),
        D("Until the patterns align again. Patterns meaning schedules.", ConversationPhase.FAREWELL, "acquaintance"),
        D("*almost smiles* See you soon. Soon is relative. But soon.", ConversationPhase.FAREWELL, "acquaintance"),
        D("*leaves* Keep looking at the stars. Or don't. Stars are there either way.", ConversationPhase.FAREWELL, "acquaintance"),

        # Friend farewell
        D("*pauses* Goodbye, my friend. Friend is accurate. Friendship confirmed.", ConversationPhase.FAREWELL, "friend"),
        D("*quietly* I'll miss you constantly. Constantly is hyperbole. But accurate.", ConversationPhase.FAREWELL, "friend"),
        D("The shadows will carry me back to you. I'll walk. Same result.", ConversationPhase.FAREWELL, "friend"),
        D("*waves* Light finds light. I found you. Same thing.", ConversationPhase.FAREWELL, "friend"),

        # Close friend farewell
        D("*sincerely* I love you. Goodbye. Both statements true.", ConversationPhase.FAREWELL, "close_friend"),
        D("*quietly* The darkness means nothing without your light. Melodramatic. True.", ConversationPhase.FAREWELL, "close_friend"),
        D("*whispers* I'll dream of you. Dreams are unpredictable. But I'll try.", ConversationPhase.FAREWELL, "close_friend"),
        D("*waves* My light. Goodbye. You're the light. I'm leaving.", ConversationPhase.FAREWELL, "close_friend"),

        # Best friend farewell
        D("*quietly* You are everything. Everything is a lot. But you.", ConversationPhase.FAREWELL, "best_friend"),
        D("This isn't goodbye. It's 'I love you.' Same thing. Different words.", ConversationPhase.FAREWELL, "best_friend"),
        D("*flatly* The vision said forever. I'm enforcing the vision.", ConversationPhase.FAREWELL, "best_friend"),
        D("*turns back* I love you, {duck}. Said it. Meant it. Leaving now.", ConversationPhase.FAREWELL, "best_friend"),
        D("*small wave* My soul stays with you. Soul is a metaphor. I'm leaving though.", ConversationPhase.FAREWELL, "best_friend"),
    ],
}

# Register with main dialogue system
DIALOGUE_TREES["mysterious"] = MYSTERIOUS_DIALOGUE
