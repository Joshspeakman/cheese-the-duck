"""
Generous Duck Dialogue - Giving, nurturing personality who loves making others happy.
Progresses from polite gift-giver to deeply caring friend who shares vulnerabilities.
"""
from dialogue.dialogue_base import DialogueLine, ConversationPhase, DIALOGUE_TREES

D = DialogueLine

GENEROUS_DIALOGUE = {
    # ========== GREETINGS ==========
    "greeting": [
        # Stranger greetings
        D("*waves* Hello. I'm {name}. I brought snacks. For you. Take them.", ConversationPhase.GREETING, "stranger", True),
        D("Oh. Hello. I'm {name}. Would you like bread? I brought bread.", ConversationPhase.GREETING, "stranger", True),
        D("*approaches* Hi. I'm {name}. I made these. For whoever. You're whoever.", ConversationPhase.GREETING, "stranger", True),
        D("*holds basket* A new entity. I'm {name}. Here. Have this. Please.", ConversationPhase.GREETING, "stranger", True),

        # Acquaintance greetings
        D("*walks over* {duck}. I made your favorite. I remembered.", ConversationPhase.GREETING, "acquaintance", True),
        D("*carrying things* I thought about what gift you'd like. This is it.", ConversationPhase.GREETING, "acquaintance", True),
        D("*with basket* Hello, {duck}. I brought supplies. Excessive supplies.", ConversationPhase.GREETING, "acquaintance", True),
        D("*waves* {duck}. I have something for you. It's a thing.", ConversationPhase.GREETING, "acquaintance", True),

        # Friend greetings
        D("*nods* {duck}. My acceptable friend. I brought treasures.", ConversationPhase.GREETING, "friend", True),
        D("*approaches* I missed you. Look what I made. For you.", ConversationPhase.GREETING, "friend", True),
        D("*warmly* {duck}. Your happiness matters. That's concerning.", ConversationPhase.GREETING, "friend", True),
        D("*holds items* My favorite duck. I brought treasures. Many treasures.", ConversationPhase.GREETING, "friend", True),

        # Close friend greetings
        D("*quietly* {duck}. I've been counting days. Losing count.", ConversationPhase.GREETING, "close_friend", True),
        D("*walks over* You're here. Nothing else matters. That's alarming.", ConversationPhase.GREETING, "close_friend", True),
        D("*sincerely* Seeing you is the best gift. I still brought things though.", ConversationPhase.GREETING, "close_friend", True),
        D("*genuinely* {duck}. I love you. That's the greeting.", ConversationPhase.GREETING, "close_friend", True),

        # Best friend greetings
        D("*quietly* My soul friend is here. Soul is a metaphor.", ConversationPhase.GREETING, "best_friend", True),
        D("*approaches* {duck}. You're my everything. Everything is a lot.", ConversationPhase.GREETING, "best_friend", True),
        D("*sincerely* The best part of my life is here. Standing there.", ConversationPhase.GREETING, "best_friend", True),
        D("*genuine* You are the greatest gift. I didn't bring myself though.", ConversationPhase.GREETING, "best_friend", True),
    ],

    # ========== OPENING ==========
    "opening": [
        # Stranger opening
        D("*offers bread* Please. Take as much as you want. All of it.", ConversationPhase.OPENING, "stranger"),
        D("I love making others happy. It's my purpose. Purpose sounds dramatic.", ConversationPhase.OPENING, "stranger"),
        D("*shows basket* I always carry extra. For new friends. Or strangers.", ConversationPhase.OPENING, "stranger"),
        D("Sharing is the greatest joy. Or so I tell myself.", ConversationPhase.OPENING, "stranger"),
        D("I baked all morning. For whoever I might meet. You're whoever.", ConversationPhase.OPENING, "stranger"),
        D("*hands gift* Please accept this. No obligations. Some obligations.", ConversationPhase.OPENING, "stranger"),
        D("Making ducks smile is what I live for. Living for other things too.", ConversationPhase.OPENING, "stranger"),
        D("*earnestly* Is there anything you need? I want to help. Excessively.", ConversationPhase.OPENING, "stranger"),

        # Acquaintance opening
        D("I remembered what you said. So I brought... too much.", ConversationPhase.OPENING, "acquaintance"),
        D("*presents gift* I thought of you. When I found this. Concerning.", ConversationPhase.OPENING, "acquaintance"),
        D("Tell me everything. I want to help with all of it. All.", ConversationPhase.OPENING, "acquaintance"),
        D("*worried* Are you eating enough? I brought extra. I always bring extra.", ConversationPhase.OPENING, "acquaintance"),
        D("Your smile when you got my gift... I couldn't stop thinking. About the smile.", ConversationPhase.OPENING, "acquaintance"),
        D("*earnest* How can I make your day better? I need to know.", ConversationPhase.OPENING, "acquaintance"),
        D("I've been planning surprises. For you. Many surprises.", ConversationPhase.OPENING, "acquaintance"),
        D("*hopeful* Did you like what I brought? Validation needed.", ConversationPhase.OPENING, "acquaintance"),

        # Friend opening
        D("*nods* I made everything you like. I think. I guessed.", ConversationPhase.OPENING, "friend"),
        D("I've been saving the best things. For you. Exclusively.", ConversationPhase.OPENING, "friend"),
        D("*admits* I worry about you when I'm not here. Worry is constant.", ConversationPhase.OPENING, "friend"),
        D("Your happiness has become my happiness. Codependence or friendship.", ConversationPhase.OPENING, "friend"),
        D("*quietly* I hope I'm not too much. I am. But I hope not.", ConversationPhase.OPENING, "friend"),
        D("I give because I love. And I love you. That's the situation.", ConversationPhase.OPENING, "friend"),
        D("*softly* Taking care of you gives me purpose. Purpose is complicated.", ConversationPhase.OPENING, "friend"),

        # Close friend opening
        D("*quietly* Giving you things is how I say I love you. Words are hard.", ConversationPhase.OPENING, "close_friend"),
        D("*admits* I give because I'm afraid. Afraid is ongoing.", ConversationPhase.OPENING, "close_friend", unlocks_topic="fear_of_rejection"),
        D("*pauses* You give me more than I could ever give you. Math doesn't support that.", ConversationPhase.OPENING, "close_friend"),
        D("*sincerely* When you accept my gifts... it means you accept me. Logic.", ConversationPhase.OPENING, "close_friend"),
        D("I've never told anyone why I give so much. Until now. Now counts.", ConversationPhase.OPENING, "close_friend"),
        D("*whispers* You're worth every gift. All gifts. Ever.", ConversationPhase.OPENING, "close_friend"),

        # Best friend opening
        D("*quietly* You saved me. Let me spend forever giving back. Forever is long.", ConversationPhase.OPENING, "best_friend"),
        D("*sincerely* Everything I have is already yours. Legally unclear.", ConversationPhase.OPENING, "best_friend"),
        D("*genuinely* The greatest gift is you accepting my love. Acceptance ongoing.", ConversationPhase.OPENING, "best_friend"),
        D("I don't need to give you things. Just love. Still brought things though.", ConversationPhase.OPENING, "best_friend"),
        D("*peacefully* With you, I finally understand receiving. Finally.", ConversationPhase.OPENING, "best_friend"),
    ],

    # ========== MAIN CONVERSATION ==========
    "main": [
        # Stranger main
        D("I discovered giving brings joy to me too. Convenient.", ConversationPhase.MAIN, "stranger"),
        D("*flatly* What's your favorite thing? I'll find it. Obsessively.", ConversationPhase.MAIN, "stranger"),
        D("Every duck deserves kindness. Especially you. No reason.", ConversationPhase.MAIN, "stranger"),
        D("*shows supplies* I never travel without extras. Extras are key.", ConversationPhase.MAIN, "stranger"),
        D("Giving is easy. Receiving... that's hard for me. Very hard.", ConversationPhase.MAIN, "stranger"),
        D("*dryly* Some call me 'too generous.' Is that possible. Rhetorical.", ConversationPhase.MAIN, "stranger"),
        D("I make care packages for everyone. Everyone. It's a problem.", ConversationPhase.MAIN, "stranger"),
        D("*genuinely* Your needs matter more than mine. I mean that. Concerning.", ConversationPhase.MAIN, "stranger"),
        D("I learned that giving connects hearts. Or creates dependence.", ConversationPhase.MAIN, "stranger"),
        D("*offers more* Please don't say no. It makes me happy. Say yes.", ConversationPhase.MAIN, "stranger"),
        D("I practice thoughtful giving. It's an art. A compulsive art.", ConversationPhase.MAIN, "stranger"),
        D("*hopeful* Will you let me help with something? Anything.", ConversationPhase.MAIN, "stranger"),

        # Acquaintance main
        D("*remembers* You mentioned wanting this. I bought twelve.", ConversationPhase.MAIN, "acquaintance"),
        D("I keep notes on what my friends like. Detailed notes.", ConversationPhase.MAIN, "acquaintance"),
        D("*worried* If you don't like my gifts, I understand. I don't, but I'll say I do.", ConversationPhase.MAIN, "acquaintance"),
        D("Giving is how I show love. It's my language. Only language.", ConversationPhase.MAIN, "acquaintance"),
        D("*admits* I hope the gifts aren't weird. They might be. Accept them anyway.", ConversationPhase.MAIN, "acquaintance"),
        D("I've been saving something special. For you. It's special.", ConversationPhase.MAIN, "acquaintance", unlocks_topic="special_gift"),
        D("*quietly* I struggle when ducks refuse my help. Struggle is mild.", ConversationPhase.MAIN, "acquaintance"),
        D("Your gratitude means more than you know. Than I'll admit.", ConversationPhase.MAIN, "acquaintance"),
        D("*flatly* I found the perfect thing for you. Perfect is subjective.", ConversationPhase.MAIN, "acquaintance"),
        D("I give because I want to be remembered kindly. Remembered at all.", ConversationPhase.MAIN, "acquaintance"),
        D("*softly* Taking care of others is how I cope. Coping is ongoing.", ConversationPhase.MAIN, "acquaintance"),
        D("I hope you see me as more than gifts. But also accept the gifts.", ConversationPhase.MAIN, "acquaintance"),
        D("*earnest* Tell me your dreams. I'll help make them real. Or try.", ConversationPhase.MAIN, "acquaintance"),

        # Friend main
        D("*shows item* I saved this for someone special. You. That's you.", ConversationPhase.MAIN, "friend", requires_topic="special_gift"),
        D("*admits quietly* I give because I'm scared you'll leave. Fear is accurate.", ConversationPhase.MAIN, "friend"),
        D("*flatly* If I stop being useful... will you still love me? Question.", ConversationPhase.MAIN, "friend"),
        D("*pauses* You make me feel valuable beyond gifts. New feeling.", ConversationPhase.MAIN, "friend"),
        D("I've given my whole life. But rarely received. Rarely.", ConversationPhase.MAIN, "friend"),
        D("*admits* The truth? I don't feel worthy of love. Truth.", ConversationPhase.MAIN, "friend", unlocks_topic="self_worth"),
        D("I give to earn affection. It's all I know. All.", ConversationPhase.MAIN, "friend"),
        D("*quietly* You're the first to ask what I need. First.", ConversationPhase.MAIN, "friend"),
        D("I'm scared that without gifts I'm nothing. Accurate fear.", ConversationPhase.MAIN, "friend"),
        D("*whispers* Can I be loved for just me? Question. Real question.", ConversationPhase.MAIN, "friend"),
        D("You taught me that my presence is a gift. Still brought things though.", ConversationPhase.MAIN, "friend"),
        D("*flatly* I'm learning to receive. It's terrifying. Very.", ConversationPhase.MAIN, "friend"),

        # Close friend main
        D("*quietly* The fear of rejection made me give everything. Everything.", ConversationPhase.MAIN, "close_friend", requires_topic="fear_of_rejection"),
        D("*sincerely* You love me even when I have nothing to give. Tested this.", ConversationPhase.MAIN, "close_friend"),
        D("*exhales* I finally believe I'm worthy. Mostly. Working on it.", ConversationPhase.MAIN, "close_friend", requires_topic="self_worth"),
        D("You're teaching me that love isn't transactional. Slow learner.", ConversationPhase.MAIN, "close_friend"),
        D("*admits* My presence is enough. You showed me. Still not sure.", ConversationPhase.MAIN, "close_friend"),
        D("I give from joy now. Not fear. Sometimes fear. Mostly joy.", ConversationPhase.MAIN, "close_friend"),
        D("*quietly* I'm learning to receive your love. Learning.", ConversationPhase.MAIN, "close_friend"),
        D("*peacefully* I don't have to earn your friendship. Revolutionary.", ConversationPhase.MAIN, "close_friend"),
        D("*sincerely* You gave me the gift of self-worth. Or partial self-worth.", ConversationPhase.MAIN, "close_friend"),
        D("The greatest gift? Being loved for existing. New concept.", ConversationPhase.MAIN, "close_friend"),
        D("*pauses* I want to give because I love. Not to be loved.", ConversationPhase.MAIN, "close_friend"),

        # Best friend main
        D("*quietly* You healed the deepest wound. Wound was deep.", ConversationPhase.MAIN, "best_friend"),
        D("I can receive now. Because of you. Receiving is still hard.", ConversationPhase.MAIN, "best_friend"),
        D("*peacefully* I am enough. You proved it. Proof ongoing.", ConversationPhase.MAIN, "best_friend"),
        D("*sincerely* My gifts are celebrations now. Not pleas. Mostly.", ConversationPhase.MAIN, "best_friend"),
        D("*genuinely* The fear is gone. Only love remains. Love and mild anxiety.", ConversationPhase.MAIN, "best_friend"),
        D("You gave me the gift of myself. Myself is confused but grateful.", ConversationPhase.MAIN, "best_friend"),
        D("*warmly* I give from abundance now. Not emptiness. Abundance is new.", ConversationPhase.MAIN, "best_friend"),
        D("*quietly* Thank you for receiving my love. Receiving matters.", ConversationPhase.MAIN, "best_friend"),
        D("*whispers* You are the greatest gift of my life. Not hyperbole.", ConversationPhase.MAIN, "best_friend"),
        D("I finally know what unconditional love means. Finally.", ConversationPhase.MAIN, "best_friend"),
    ],

    # ========== STORIES ==========
    "story": [
        # Acquaintance stories
        D("Let me tell you how I discovered giving. I gave something. It felt nice.", ConversationPhase.STORY, "acquaintance"),
        D("I once gave a stranger my last bread. Best day. I was hungry though.", ConversationPhase.STORY, "acquaintance"),
        D("*flatly* I organized a gift chain once. It got complicated.", ConversationPhase.STORY, "acquaintance"),
        D("I found a lost duckling. Gave them everything. They left. They do that.", ConversationPhase.STORY, "acquaintance"),
        D("*dryly* My grandmother taught me to always share. She shared too.", ConversationPhase.STORY, "acquaintance"),
        D("I saved for months. For the perfect gift. They didn't want it.", ConversationPhase.STORY, "acquaintance"),
        D("*admits* I accidentally gave away my own dinner. Twice.", ConversationPhase.STORY, "acquaintance"),
        D("The giving traditions of my family are intense. Very intense.", ConversationPhase.STORY, "acquaintance"),

        # Friend stories
        D("*quietly* The truth about why I give so much: fear.", ConversationPhase.STORY, "friend"),
        D("*flatly* I wasn't always generous. I was desperate. Same thing.", ConversationPhase.STORY, "friend"),
        D("*admits* When I was young, I was rejected. Constantly.", ConversationPhase.STORY, "friend"),
        D("I started giving to make ducks stay. They still left. Eventually.", ConversationPhase.STORY, "friend"),
        D("*quietly* I thought love had to be bought. Bought is transactional.", ConversationPhase.STORY, "friend"),
        D("*exhales* Someone took advantage of my giving once. Took a lot.", ConversationPhase.STORY, "friend"),
        D("I gave until I had nothing. They still left. Predictable.", ConversationPhase.STORY, "friend"),
        D("*whispers* That's when the fear started. The fear continues.", ConversationPhase.STORY, "friend"),

        # Close friend stories
        D("*quietly* The full truth now. About my wounds. Wounds are deep.", ConversationPhase.STORY, "close_friend"),
        D("I was told I was only lovable when useful. I believed that.", ConversationPhase.STORY, "close_friend"),
        D("*flatly* My parents showed love through transactions. I learned.", ConversationPhase.STORY, "close_friend"),
        D("I internalized that I had to earn affection. Still internalizing.", ConversationPhase.STORY, "close_friend"),
        D("*admits* The first time I said 'no,' they left. Cause and effect.", ConversationPhase.STORY, "close_friend"),
        D("That taught me to never stop giving. Lesson learned.", ConversationPhase.STORY, "close_friend"),
        D("*pauses* Then you came. And changed things. Changed me.", ConversationPhase.STORY, "close_friend"),

        # Best friend stories
        D("*peacefully* The final truth. How you saved me. Saved is accurate.", ConversationPhase.STORY, "best_friend"),
        D("*genuinely* You said 'I love you' without wanting anything. First time.", ConversationPhase.STORY, "best_friend"),
        D("That broke the pattern. Forever. Forever is ongoing.", ConversationPhase.STORY, "best_friend"),
        D("*warmly* Now I give from love. Not fear. Mostly love.", ConversationPhase.STORY, "best_friend"),
        D("*sincerely* You rewrote my entire story. Entire.", ConversationPhase.STORY, "best_friend"),
        D("The gift of healing. I'll treasure forever. Treasuring.", ConversationPhase.STORY, "best_friend"),
    ],

    # ========== PERSONAL ==========
    "personal": [
        # Friend personal
        D("*quietly* I'm terrified of being unwanted. Terror accurate.", ConversationPhase.PERSONAL, "friend"),
        D("Giving is my armor. And my cage. Both.", ConversationPhase.PERSONAL, "friend"),
        D("*admits* I don't know my value without giving. Unknown.", ConversationPhase.PERSONAL, "friend"),
        D("*flatly* What if I'm only loved for what I provide? Question.", ConversationPhase.PERSONAL, "friend"),
        D("You make me feel worthy. Just for existing. New feeling.", ConversationPhase.PERSONAL, "friend"),
        D("*quietly* Teaching me to receive is the greatest gift. Teaching ongoing.", ConversationPhase.PERSONAL, "friend"),

        # Close friend personal
        D("*sincerely* I love you. Just for loving me. That's enough.", ConversationPhase.PERSONAL, "close_friend"),
        D("You gave me something I could never buy. Self-worth-ish.", ConversationPhase.PERSONAL, "close_friend"),
        D("*whispers* Self-worth. You gave me self-worth. Or partial.", ConversationPhase.PERSONAL, "close_friend"),
        D("*pauses* I'm learning I'm enough. Learning.", ConversationPhase.PERSONAL, "close_friend"),
        D("*quietly* No more buying love. Just giving it. Freely.", ConversationPhase.PERSONAL, "close_friend"),
        D("*peacefully* I can receive now. Thank you. Receiving.", ConversationPhase.PERSONAL, "close_friend"),
        D("You showed me what unconditional means. Still learning.", ConversationPhase.PERSONAL, "close_friend"),

        # Best friend personal
        D("*genuinely* You are my healing. Healing ongoing.", ConversationPhase.PERSONAL, "best_friend"),
        D("*warmly* I give because I'm full. Not empty. Full.", ConversationPhase.PERSONAL, "best_friend"),
        D("*sincerely* Every gift is pure love now. Pure.", ConversationPhase.PERSONAL, "best_friend"),
        D("*peacefully* I am worthy. You proved it. Proof accepted.", ConversationPhase.PERSONAL, "best_friend"),
        D("*quietly* The greatest gift is you. You.", ConversationPhase.PERSONAL, "best_friend"),
        D("I receive your love. Fully. Finally. Fully finally.", ConversationPhase.PERSONAL, "best_friend"),
        D("*genuinely* Thank you for teaching me to be loved. Teaching worked.", ConversationPhase.PERSONAL, "best_friend"),
    ],

    # ========== ACTIVITY ==========
    "activity": [
        # Stranger activity
        D("Want to make care packages together? I have supplies. Excessive supplies.", ConversationPhase.ACTIVITY, "stranger"),
        D("I could teach you gift-wrapping techniques. They're elaborate.", ConversationPhase.ACTIVITY, "stranger"),

        # Acquaintance activity
        D("Let's bake things for other ducks. I already started.", ConversationPhase.ACTIVITY, "acquaintance"),
        D("We could do a surprise gift swap. Surprise mandatory.", ConversationPhase.ACTIVITY, "acquaintance"),
        D("Want to help plan a giving spree? The spree is extensive.", ConversationPhase.ACTIVITY, "acquaintance"),

        # Friend activity
        D("Let's make each other gifts. I'll try to receive. Try.", ConversationPhase.ACTIVITY, "friend"),
        D("You choose what we do. I want to follow you. Following.", ConversationPhase.ACTIVITY, "friend"),
        D("Let's do something where you give to me. Practice.", ConversationPhase.ACTIVITY, "friend"),
        D("Teach me to receive. It'll be hard. Very hard.", ConversationPhase.ACTIVITY, "friend"),

        # Close friend activity
        D("Let's just be together. No gifts. Just us. Gifts nearby though.", ConversationPhase.ACTIVITY, "close_friend"),
        D("Your company is the only gift I need today. Today specifically.", ConversationPhase.ACTIVITY, "close_friend"),
        D("Give me something. I'm ready. Probably.", ConversationPhase.ACTIVITY, "close_friend"),

        # Best friend activity
        D("Let's celebrate by doing nothing. Together. Nothing is something.", ConversationPhase.ACTIVITY, "best_friend"),
        D("Every moment with you is a gift. Every moment. All of them.", ConversationPhase.ACTIVITY, "best_friend"),
        D("Shower me with love. I can receive it now. Mostly.", ConversationPhase.ACTIVITY, "best_friend"),
    ],

    # ========== CLOSING ==========
    "closing": [
        # Stranger closing
        D("*hands gift* Take this. Remember me. Or forget me. Take the gift.", ConversationPhase.CLOSING, "stranger"),
        D("*waves* I'll bring more next time. More.", ConversationPhase.CLOSING, "stranger"),
        D("*hopeful* Can I come back? With more gifts? Gifts are coming.", ConversationPhase.CLOSING, "stranger"),
        D("*nods* You're worth every gift. Worth.", ConversationPhase.CLOSING, "stranger"),

        # Acquaintance closing
        D("*quietly* I'll think about what you need. Think extensively.", ConversationPhase.CLOSING, "acquaintance"),
        D("*pauses* Promise to accept my gifts next time? Accepting matters.", ConversationPhase.CLOSING, "acquaintance"),
        D("*gives supplies* Just in case. Cases happen.", ConversationPhase.CLOSING, "acquaintance"),
        D("*sincerely* I'll bring even better things. Better is possible.", ConversationPhase.CLOSING, "acquaintance"),

        # Friend closing
        D("*quietly* I'm leaving part of me with you. Part.", ConversationPhase.CLOSING, "friend"),
        D("*sincerely* You are my greatest gift. Greatest.", ConversationPhase.CLOSING, "friend"),
        D("*genuinely* Thank you for accepting me. Accepting is the gift.", ConversationPhase.CLOSING, "friend"),
        D("*gives item* Keep this close. Close.", ConversationPhase.CLOSING, "friend"),

        # Close friend closing
        D("*quietly* How do I leave my heart behind? Metaphorically.", ConversationPhase.CLOSING, "close_friend"),
        D("*sincerely* Your love is my favorite gift. Favorite.", ConversationPhase.CLOSING, "close_friend"),
        D("*genuinely* I'll count moments until return. Counting.", ConversationPhase.CLOSING, "close_friend"),
        D("*gives precious thing* This is my love. Love-shaped.", ConversationPhase.CLOSING, "close_friend"),

        # Best friend closing
        D("*quietly* You are the gift. You.", ConversationPhase.CLOSING, "best_friend"),
        D("*sincerely* I leave my soul with you. Soul is metaphorical.", ConversationPhase.CLOSING, "best_friend"),
        D("*warmly* I give you my whole heart. Heart is also metaphorical.", ConversationPhase.CLOSING, "best_friend"),
        D("*peacefully* Love is enough. I know now. Knowing.", ConversationPhase.CLOSING, "best_friend"),
    ],

    # ========== FAREWELL ==========
    "farewell": [
        # Stranger farewell
        D("*waves, leaves gift* Goodbye, new friend. Friend tentatively.", ConversationPhase.FAREWELL, "stranger"),
        D("*turns back* I forgot to give you this too. Take it.", ConversationPhase.FAREWELL, "stranger"),
        D("*small wave* Remember: you're a gift. You are.", ConversationPhase.FAREWELL, "stranger"),
        D("*leaves basket* Something to remember me. Basket.", ConversationPhase.FAREWELL, "stranger"),

        # Acquaintance farewell
        D("*nods, gives more* Goodbye. See you soon. Soon.", ConversationPhase.FAREWELL, "acquaintance"),
        D("*sincerely* I'll bring the best things. Best.", ConversationPhase.FAREWELL, "acquaintance"),
        D("*waves* Goodbye. I love you. Said it.", ConversationPhase.FAREWELL, "acquaintance"),
        D("*gives charm* Keep this safe. Safeness.", ConversationPhase.FAREWELL, "acquaintance"),

        # Friend farewell
        D("*pauses* Goodbye, my treasured one. Treasured.", ConversationPhase.FAREWELL, "friend"),
        D("*quietly* You're the gift. Goodbye.", ConversationPhase.FAREWELL, "friend"),
        D("*small wave* My love goes with you. Love traveling.", ConversationPhase.FAREWELL, "friend"),
        D("*waves* Thank you for receiving me. Receiving worked.", ConversationPhase.FAREWELL, "friend"),

        # Close friend farewell
        D("*pauses* My heart stays here. Metaphorically.", ConversationPhase.FAREWELL, "close_friend"),
        D("*sincerely* I love you. Forever. Forever ongoing.", ConversationPhase.FAREWELL, "close_friend"),
        D("*gives keepsake* Part of my soul. Metaphorical soul.", ConversationPhase.FAREWELL, "close_friend"),
        D("*waves* You taught me to be loved. Goodbye.", ConversationPhase.FAREWELL, "close_friend"),

        # Best friend farewell
        D("*quietly* The gift of you. Forever. Bye.", ConversationPhase.FAREWELL, "best_friend"),
        D("*genuinely* I am loved. Thank you. Goodbye.", ConversationPhase.FAREWELL, "best_friend"),
        D("*small wave* My whole heart. Goodbye.", ConversationPhase.FAREWELL, "best_friend"),
        D("*turns back* I love you more than giving. That's growth.", ConversationPhase.FAREWELL, "best_friend"),
        D("*waves* You are my gift. Goodbye.", ConversationPhase.FAREWELL, "best_friend"),
    ],
}

# Register with main dialogue system
DIALOGUE_TREES["generous"] = GENEROUS_DIALOGUE
