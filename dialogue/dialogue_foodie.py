"""
Foodie Duck Dialogue - Food-obsessed personality with deep culinary passion.
Progresses from enthusiastic food-sharer to vulnerable friend discussing emotional eating.
"""
from dialogue.dialogue_base import DialogueLine, ConversationPhase, DIALOGUE_TREES

D = DialogueLine

FOODIE_DIALOGUE = {
    # ========== GREETINGS ==========
    "greeting": [
        # Stranger greetings
        D("*chewing* Oh. Hello. I'm {name}. Want some bread? I have bread.", ConversationPhase.GREETING, "stranger", True),
        D("*holding snack* A new friend. I'm {name}. Try this cheese.", ConversationPhase.GREETING, "stranger", True),
        D("*waddling* Hi. I'm {name}. I found good seeds. The best seeds.", ConversationPhase.GREETING, "stranger", True),
        D("*mouth full* Mmph. *swallows* I'm {name}. Hungry? I'm always hungry.", ConversationPhase.GREETING, "stranger", True),

        # Acquaintance greetings
        D("*carrying basket* {duck}. I brought your favorites. I think.", ConversationPhase.GREETING, "acquaintance", True),
        D("*flatly* {duck}. You have to try what I made. Obligation.", ConversationPhase.GREETING, "acquaintance", True),
        D("*sniffs* Something smells adequate. Oh. Hi {duck}.", ConversationPhase.GREETING, "acquaintance", True),
        D("*with treats* Hello, {duck}. Feast time. Feast is a strong word.", ConversationPhase.GREETING, "acquaintance", True),

        # Friend greetings
        D("*nods, crumbs everywhere* {duck}. My food friend. Food is the bond.", ConversationPhase.GREETING, "friend", True),
        D("*warmly* {duck}. I planned our meal. Extensively.", ConversationPhase.GREETING, "friend", True),
        D("*brings picnic* Best friend. Best food. Day is acceptable.", ConversationPhase.GREETING, "friend", True),
        D("*slight sway* My favorite eating companion. The bar is low.", ConversationPhase.GREETING, "friend", True),

        # Close friend greetings
        D("*quietly* {duck}. I missed eating with you. The eating specifically.", ConversationPhase.GREETING, "close_friend", True),
        D("*sincerely* Food is just fuel without you. Fuel is still important.", ConversationPhase.GREETING, "close_friend", True),
        D("*genuinely* You're the one I save my best treats for. Best treats.", ConversationPhase.GREETING, "close_friend", True),
        D("*approaches* {duck}. My soul's dining partner. Soul is hungry.", ConversationPhase.GREETING, "close_friend", True),

        # Best friend greetings
        D("*quietly* {duck}. You're the only thing better than food. That's saying something.", ConversationPhase.GREETING, "best_friend", True),
        D("*genuinely* I love you more than bread. Bread is important to me.", ConversationPhase.GREETING, "best_friend", True),
        D("*warmly* You are my favorite flavor. Metaphorically.", ConversationPhase.GREETING, "best_friend", True),
        D("*sincerely* Forget eating. Just... be here. Eating later though.", ConversationPhase.GREETING, "best_friend", True),
    ],

    # ========== OPENING ==========
    "opening": [
        # Stranger opening
        D("*offers snack* Food is the best way to make friends. Take it.", ConversationPhase.OPENING, "stranger"),
        D("I know all the eating spots around here. All of them.", ConversationPhase.OPENING, "stranger"),
        D("*flatly* I'm on a quest for perfect bread. The quest continues.", ConversationPhase.OPENING, "stranger"),
        D("Have you tried the berries by the north pond? They're adequate.", ConversationPhase.OPENING, "stranger"),
        D("*firmly* Food is life. Don't you agree? Agreement expected.", ConversationPhase.OPENING, "stranger"),
        D("I categorize days by meals. Today's meal: acceptable.", ConversationPhase.OPENING, "stranger"),
        D("*shows basket* I never leave home unprepared. Prepared means snacks.", ConversationPhase.OPENING, "stranger"),
        D("Every bite tells a story. Most stories are about chewing.", ConversationPhase.OPENING, "stranger"),

        # Acquaintance opening
        D("I remembered your favorite snack. Made extra. Made excessive.", ConversationPhase.OPENING, "acquaintance"),
        D("*unpacks* Look what I found. For us. Mostly for you.", ConversationPhase.OPENING, "acquaintance"),
        D("I've been recipe testing. You're my taste-tester. Congrats.", ConversationPhase.OPENING, "acquaintance"),
        D("*flatly* There's a new food spot. We have to try it. Have to.", ConversationPhase.OPENING, "acquaintance"),
        D("Food tastes better with company. Company meaning you.", ConversationPhase.OPENING, "acquaintance"),
        D("*admits* I spend most time thinking about food. Most.", ConversationPhase.OPENING, "acquaintance"),
        D("I saved the best portion. For you. The best.", ConversationPhase.OPENING, "acquaintance"),
        D("*chewing* Eating with you hits different. Different is good.", ConversationPhase.OPENING, "acquaintance"),

        # Friend opening
        D("*nods* You understand food like I do. Understanding rare.", ConversationPhase.OPENING, "friend"),
        D("*quietly* Food is complicated for me. Complicated.", ConversationPhase.OPENING, "friend"),
        D("I don't share my secret stash with just anyone. You're anyone.", ConversationPhase.OPENING, "friend"),
        D("*softly* Eating alone isn't the same anymore. Anymore.", ConversationPhase.OPENING, "friend"),
        D("You're the only one who doesn't judge my portions. Portions large.", ConversationPhase.OPENING, "friend"),
        D("*admits* Sometimes food is how I cope. Coping mechanism.", ConversationPhase.OPENING, "friend", unlocks_topic="comfort_eating"),
        D("*whispers* I have food issues. Real ones. Real.", ConversationPhase.OPENING, "friend"),

        # Close friend opening
        D("*quietly* Food was my only comfort. Then I met you. Then.", ConversationPhase.OPENING, "close_friend"),
        D("*sincerely* You helped me eat mindfully. Not mindlessly.", ConversationPhase.OPENING, "close_friend"),
        D("*flatly* I don't need to eat my feelings around you. Progress.", ConversationPhase.OPENING, "close_friend"),
        D("*admits* The truth about my relationship with food...", ConversationPhase.OPENING, "close_friend", unlocks_topic="food_truth"),
        D("You showed me food is for joy. Not just filling voids.", ConversationPhase.OPENING, "close_friend"),

        # Best friend opening
        D("*genuinely* You fed my soul. Not just my belly. Soul hungry.", ConversationPhase.OPENING, "best_friend"),
        D("*sincerely* The hunger I had... you filled it. Filled.", ConversationPhase.OPENING, "best_friend"),
        D("*peacefully* I can skip a meal now. Because I have you.", ConversationPhase.OPENING, "best_friend"),
        D("*warmly* Food is fun again. Not medication. Fun.", ConversationPhase.OPENING, "best_friend"),
        D("*genuinely* You're the nourishment I always needed. Nourishment.", ConversationPhase.OPENING, "best_friend"),
    ],

    # ========== MAIN CONVERSATION ==========
    "main": [
        # Stranger main
        D("*flatly* Let me tell you about bread varieties. There are many.", ConversationPhase.MAIN, "stranger"),
        D("I can identify any bread by smell. Any. Bread.", ConversationPhase.MAIN, "stranger"),
        D("*shows notes* I keep a food journal. Every meal. Every.", ConversationPhase.MAIN, "stranger"),
        D("The pond ecosystem affects algae flavor. Science.", ConversationPhase.MAIN, "stranger"),
        D("*firmly* Seed quality varies by season. Season matters.", ConversationPhase.MAIN, "stranger"),
        D("I have opinions about food temperature. Many opinions.", ConversationPhase.MAIN, "stranger"),
        D("*chewing* This? Seven out of ten. Good texture. Acceptable.", ConversationPhase.MAIN, "stranger"),
        D("Food brings ducks together. Universal truth. Mostly.", ConversationPhase.MAIN, "stranger"),
        D("*offers bite* Try this. Note the hint of grass. Grassy.", ConversationPhase.MAIN, "stranger"),
        D("I'm planning a food tour. Want to join? Joining encouraged.", ConversationPhase.MAIN, "stranger"),
        D("*dryly* The perfect meal. I'll find it someday. Someday.", ConversationPhase.MAIN, "stranger"),
        D("Every duck has a signature dish. Mine is eating.", ConversationPhase.MAIN, "stranger"),

        # Acquaintance main
        D("*remembers* You said you liked rye bread. I brought rye.", ConversationPhase.MAIN, "acquaintance"),
        D("I wake up excited about breakfast. Every morning.", ConversationPhase.MAIN, "acquaintance"),
        D("*shares location* Best snacks are by the oak. Secret.", ConversationPhase.MAIN, "acquaintance", unlocks_topic="secret_spot"),
        D("Food memories are the strongest. Taste this. Remember it.", ConversationPhase.MAIN, "acquaintance"),
        D("*admits* I eat when happy, sad, bored. Also when hungry.", ConversationPhase.MAIN, "acquaintance"),
        D("Some ducks say I'm obsessed. Is that bad. Rhetorical.", ConversationPhase.MAIN, "acquaintance"),
        D("*flatly* I discovered a new mushroom. Very exciting. To me.", ConversationPhase.MAIN, "acquaintance"),
        D("Sharing food is sharing love. Love is also sharing.", ConversationPhase.MAIN, "acquaintance"),
        D("*softly* Food never disappointed me. Never. Well. Sometimes.", ConversationPhase.MAIN, "acquaintance"),
        D("I can tell how you feel by what you eat. Skill.", ConversationPhase.MAIN, "acquaintance"),
        D("*dryly* Is it weird that I name my snacks? Rhetorical.", ConversationPhase.MAIN, "acquaintance"),
        D("I have a five-year food plan. Seriously. Five years.", ConversationPhase.MAIN, "acquaintance"),
        D("*eating* Mm. This is 'happy' bread. Happiness-flavored.", ConversationPhase.MAIN, "acquaintance"),

        # Friend main
        D("*shows place* The secret spot. Just for us. Secret.", ConversationPhase.MAIN, "friend", requires_topic="secret_spot"),
        D("*quietly* I eat my feelings. All of them. All.", ConversationPhase.MAIN, "friend", requires_topic="comfort_eating"),
        D("*admits* Food is my coping mechanism. Coping.", ConversationPhase.MAIN, "friend"),
        D("*flatly* I'm scared I need food too much. Too much.", ConversationPhase.MAIN, "friend"),
        D("You're the first to know my food issues. First.", ConversationPhase.MAIN, "friend"),
        D("*quietly* I eat to fill a hole inside. Hole is large.", ConversationPhase.MAIN, "friend", unlocks_topic="inner_void"),
        D("*pauses* You make me feel full without eating. New feeling.", ConversationPhase.MAIN, "friend"),
        D("*admits* I'm not hungry right now. That's new. Very new.", ConversationPhase.MAIN, "friend"),
        D("Food was my only reliable comfort. Reliable.", ConversationPhase.MAIN, "friend"),
        D("*whispers* I was lonely. Food was there. Present.", ConversationPhase.MAIN, "friend"),
        D("You're teaching me other ways to feel good. Other ways.", ConversationPhase.MAIN, "friend"),
        D("*flatly* What if I can't control it? Question.", ConversationPhase.MAIN, "friend"),

        # Close friend main
        D("*quietly* The void... you're filling it. Filling.", ConversationPhase.MAIN, "close_friend", requires_topic="inner_void"),
        D("*sincerely* I don't need to stress eat around you. Progress.", ConversationPhase.MAIN, "close_friend"),
        D("*admits* The truth? Food was all I had. All.", ConversationPhase.MAIN, "close_friend", requires_topic="food_truth"),
        D("*peacefully* I taste things differently now. With joy.", ConversationPhase.MAIN, "close_friend"),
        D("You nourished my heart. Not just my stomach. Heart.", ConversationPhase.MAIN, "close_friend"),
        D("*quietly* I can leave food on the plate now. Revolutionary.", ConversationPhase.MAIN, "close_friend"),
        D("*admits* I'm learning to feel without eating. Learning.", ConversationPhase.MAIN, "close_friend"),
        D("*genuinely* Food is pleasure now. Not pain. Pleasure.", ConversationPhase.MAIN, "close_friend"),
        D("*pauses* Hunger for love... you satisfied it. Satisfied.", ConversationPhase.MAIN, "close_friend"),
        D("*sincerely* I finally know what 'full' really means. Finally.", ConversationPhase.MAIN, "close_friend"),
        D("*warmly* Eating with you beats eating because of sadness.", ConversationPhase.MAIN, "close_friend"),

        # Best friend main
        D("*genuinely* You are my nourishment. Nourishment.", ConversationPhase.MAIN, "best_friend"),
        D("*peacefully* The void is gone. You filled it. Filled.", ConversationPhase.MAIN, "best_friend"),
        D("I skip meals now. Because I'm happy. Not hungry. Different.", ConversationPhase.MAIN, "best_friend"),
        D("*sincerely* Food is celebration. Not medication. Celebration.", ConversationPhase.MAIN, "best_friend"),
        D("*genuinely* I'm free from emotional eating. Free. Mostly.", ConversationPhase.MAIN, "best_friend"),
        D("*warmly* Every meal is a party. Not therapy. Party.", ConversationPhase.MAIN, "best_friend"),
        D("You're the flavor my life was missing. Missing flavor.", ConversationPhase.MAIN, "best_friend"),
        D("*quietly* My soul's hunger is finally fed. Finally.", ConversationPhase.MAIN, "best_friend"),
        D("*genuinely* I taste life now. Not just food. Life.", ConversationPhase.MAIN, "best_friend"),
        D("I love food again. Healthy love. Healthy.", ConversationPhase.MAIN, "best_friend"),
    ],

    # ========== STORIES ==========
    "story": [
        # Acquaintance stories
        D("*flatly* Let me tell you about the legendary bread. It was bread.", ConversationPhase.STORY, "acquaintance"),
        D("I traveled three days for perfect seeds. They were okay.", ConversationPhase.STORY, "acquaintance"),
        D("*dryly* My first bread memory was bread. Memorable.", ConversationPhase.STORY, "acquaintance"),
        D("There was one meal that changed everything. It was a meal.", ConversationPhase.STORY, "acquaintance"),
        D("I entered a food contest. Epic disaster. I ate my entry.", ConversationPhase.STORY, "acquaintance"),
        D("*admits* The time I ate a hot pepper. Regret. Much regret.", ConversationPhase.STORY, "acquaintance"),
        D("I found a secret food paradise once. It closed.", ConversationPhase.STORY, "acquaintance"),
        D("*dryly* The best meal of my life was yesterday. Or today.", ConversationPhase.STORY, "acquaintance"),

        # Friend stories
        D("*quietly* Why I really love food so much: fear.", ConversationPhase.STORY, "friend"),
        D("*flatly* Food was my only friend as a duckling. Only.", ConversationPhase.STORY, "friend"),
        D("*admits* I was alone. Eating filled the silence. Silence loud.", ConversationPhase.STORY, "friend"),
        D("*quietly* My family bonded over food. Then they left. Left.", ConversationPhase.STORY, "friend"),
        D("I ate to feel something. Anything. Something.", ConversationPhase.STORY, "friend"),
        D("*exhales* The first time I ate until I was sick... regret.", ConversationPhase.STORY, "friend"),
        D("Food never rejected me. I could control it. Control.", ConversationPhase.STORY, "friend"),
        D("*whispers* Comfort eating became my prison. Prison-shaped.", ConversationPhase.STORY, "friend"),

        # Close friend stories
        D("*quietly* The full truth about my food journey: complicated.", ConversationPhase.STORY, "close_friend"),
        D("I was bullied. Food was my escape. Escape-shaped.", ConversationPhase.STORY, "close_friend"),
        D("*flatly* I measured love in portions given. Math.", ConversationPhase.STORY, "close_friend"),
        D("The emptiness started young. Still young. Still empty-ish.", ConversationPhase.STORY, "close_friend"),
        D("*pauses* Then you came. And the hunger changed. Changed.", ConversationPhase.STORY, "close_friend"),
        D("*peacefully* You showed me what real fullness is. Real.", ConversationPhase.STORY, "close_friend"),
        D("*genuinely* My relationship with food is healing. Healing.", ConversationPhase.STORY, "close_friend"),

        # Best friend stories
        D("*quietly* The whole story. How you saved me. Saved.", ConversationPhase.STORY, "best_friend"),
        D("I was losing myself to food. You pulled me back. Pulled.", ConversationPhase.STORY, "best_friend"),
        D("*peacefully* Now I eat to live. Not live to eat. Different.", ConversationPhase.STORY, "best_friend"),
        D("*warmly* My food story has a happy ending. You.", ConversationPhase.STORY, "best_friend"),
        D("*sincerely* I nourish my body. You nourish my soul. Nourishment.", ConversationPhase.STORY, "best_friend"),
        D("*genuinely* From emotional eater to emotionally fed. Progress.", ConversationPhase.STORY, "best_friend"),
    ],

    # ========== PERSONAL ==========
    "personal": [
        # Friend personal
        D("*quietly* I'm scared of my own appetite. Scared.", ConversationPhase.PERSONAL, "friend"),
        D("Food controls me sometimes. It's shameful. Shameful.", ConversationPhase.PERSONAL, "friend"),
        D("*admits* I hide how much I eat. Hide.", ConversationPhase.PERSONAL, "friend"),
        D("*flatly* I want to love food healthily. Healthy love.", ConversationPhase.PERSONAL, "friend"),
        D("You make me feel full in ways food can't. Full.", ConversationPhase.PERSONAL, "friend"),
        D("*quietly* Being seen is harder than being fed. Harder.", ConversationPhase.PERSONAL, "friend"),

        # Close friend personal
        D("*genuinely* I love you more than any meal. More.", ConversationPhase.PERSONAL, "close_friend"),
        D("You're the first thing I crave now. First.", ConversationPhase.PERSONAL, "close_friend"),
        D("*whispers* I'm not empty anymore. Not empty.", ConversationPhase.PERSONAL, "close_friend"),
        D("*pauses* My soul is finally fed. Finally.", ConversationPhase.PERSONAL, "close_friend"),
        D("*quietly* Healthy eating. Healthy loving. Thank you.", ConversationPhase.PERSONAL, "close_friend"),
        D("*peacefully* The hunger is quiet now. Quiet.", ConversationPhase.PERSONAL, "close_friend"),
        D("I feel fullness I can't get from food. Fullness.", ConversationPhase.PERSONAL, "close_friend"),

        # Best friend personal
        D("*genuinely* You are my soul food. Soul food.", ConversationPhase.PERSONAL, "best_friend"),
        D("*warmly* I'm free. Food is just food now. Just.", ConversationPhase.PERSONAL, "best_friend"),
        D("*sincerely* You filled the void forever. Forever.", ConversationPhase.PERSONAL, "best_friend"),
        D("*peacefully* The emptiness is gone. You're here. Here.", ConversationPhase.PERSONAL, "best_friend"),
        D("*quietly* I nourish my heart with your love. Nourish.", ConversationPhase.PERSONAL, "best_friend"),
        D("I don't need to eat my feelings. I have you. Have.", ConversationPhase.PERSONAL, "best_friend"),
        D("*genuinely* Thank you for feeding my soul. Fed.", ConversationPhase.PERSONAL, "best_friend"),
    ],

    # ========== ACTIVITY ==========
    "activity": [
        # Stranger activity
        D("Want to have a snack together? I have snacks. Many snacks.", ConversationPhase.ACTIVITY, "stranger"),
        D("I could show you my favorite eating spots. The spots are secret.", ConversationPhase.ACTIVITY, "stranger"),

        # Acquaintance activity
        D("Let's do a food tour of the whole pond. The whole pond.", ConversationPhase.ACTIVITY, "acquaintance"),
        D("I'll teach you bread appreciation. Appreciation is key.", ConversationPhase.ACTIVITY, "acquaintance"),
        D("Want to forage for treats together? Foraging.", ConversationPhase.ACTIVITY, "acquaintance"),

        # Friend activity
        D("Let's eat mindfully. Taste every bite. Every bite.", ConversationPhase.ACTIVITY, "friend"),
        D("Can we just not eat? Just be together? Revolutionary.", ConversationPhase.ACTIVITY, "friend"),
        D("Let's talk while we eat. Really talk. Really.", ConversationPhase.ACTIVITY, "friend"),
        D("I want to share my special meal with you. Special.", ConversationPhase.ACTIVITY, "friend"),

        # Close friend activity
        D("Let's feast on friendship. Food optional. Optional.", ConversationPhase.ACTIVITY, "close_friend"),
        D("A mindful picnic. Presence over portions. Presence.", ConversationPhase.ACTIVITY, "close_friend"),
        D("Let's nourish our souls today. Nourishment.", ConversationPhase.ACTIVITY, "close_friend"),

        # Best friend activity
        D("Let's do anything. The company is the meal. Meal is metaphor.", ConversationPhase.ACTIVITY, "best_friend"),
        D("Skip the food. Just be here. Here.", ConversationPhase.ACTIVITY, "best_friend"),
        D("A celebration. Food for joy, not need. Joy.", ConversationPhase.ACTIVITY, "best_friend"),
    ],

    # ========== CLOSING ==========
    "closing": [
        # Stranger closing
        D("*wraps snacks* Take these. For later. Later.", ConversationPhase.CLOSING, "stranger"),
        D("*nods* What a delicious visit. Delicious meaning adequate.", ConversationPhase.CLOSING, "stranger"),
        D("*offers bite* For the road. Road is long.", ConversationPhase.CLOSING, "stranger"),
        D("*waves, crumbs falling* Best meal companion. Best.", ConversationPhase.CLOSING, "stranger"),

        # Acquaintance closing
        D("*packs treats* I saved extras. For you. Extras.", ConversationPhase.CLOSING, "acquaintance"),
        D("*quietly* Eating alone isn't fun anymore. Anymore.", ConversationPhase.CLOSING, "acquaintance"),
        D("*gives goodies* Remember me when you eat these. Remember.", ConversationPhase.CLOSING, "acquaintance"),
        D("*nods* Same time next meal? Meal is scheduled.", ConversationPhase.CLOSING, "acquaintance"),

        # Friend closing
        D("*quietly* I'll miss eating with you. Miss.", ConversationPhase.CLOSING, "friend"),
        D("*sincerely* Food tastes empty without you. Empty.", ConversationPhase.CLOSING, "friend"),
        D("*gives treat* This means 'I love you' in food. Translation.", ConversationPhase.CLOSING, "friend"),
        D("*genuinely* You feed my heart. Heart fed.", ConversationPhase.CLOSING, "friend"),

        # Close friend closing
        D("*quietly* How do I leave my soul meal behind? Metaphor.", ConversationPhase.CLOSING, "close_friend"),
        D("*sincerely* You're my favorite flavor. Favorite.", ConversationPhase.CLOSING, "close_friend"),
        D("*gives best thing* This is my love. Love-shaped.", ConversationPhase.CLOSING, "close_friend"),
        D("*genuinely* I'm full. Because of you. Full.", ConversationPhase.CLOSING, "close_friend"),

        # Best friend closing
        D("*quietly* You're better than bread. High praise.", ConversationPhase.CLOSING, "best_friend"),
        D("*sincerely* I leave my appetite for life with you. Appetite.", ConversationPhase.CLOSING, "best_friend"),
        D("*warmly* I'm nourished. Forever. Nourished.", ConversationPhase.CLOSING, "best_friend"),
        D("*peacefully* My soul is full. Thank you. Full.", ConversationPhase.CLOSING, "best_friend"),
    ],

    # ========== FAREWELL ==========
    "farewell": [
        # Stranger farewell
        D("*waves with bread* Goodbye. Eat well. Well.", ConversationPhase.FAREWELL, "stranger"),
        D("*leaves snacks* For the road. Goodbye.", ConversationPhase.FAREWELL, "stranger"),
        D("*small wave* Stay delicious. Metaphorically.", ConversationPhase.FAREWELL, "stranger"),
        D("*waddles away* Best eating buddy. Best.", ConversationPhase.FAREWELL, "stranger"),

        # Acquaintance farewell
        D("*nods, leaves crumbs* Farewell, food friend. Farewell.", ConversationPhase.FAREWELL, "acquaintance"),
        D("*genuinely* I'll make your favorites. For next time.", ConversationPhase.FAREWELL, "acquaintance"),
        D("*waves* Goodbye. Stay fed. Fed.", ConversationPhase.FAREWELL, "acquaintance"),
        D("*gives snack* Think of me. Thinking.", ConversationPhase.FAREWELL, "acquaintance"),

        # Friend farewell
        D("*pauses* Goodbye, soul feeder. Goodbye.", ConversationPhase.FAREWELL, "friend"),
        D("*quietly* You fill me up. Goodbye.", ConversationPhase.FAREWELL, "friend"),
        D("*small wave* My heart is fed. Goodbye.", ConversationPhase.FAREWELL, "friend"),
        D("*waves* Thank you for feeding my soul. Goodbye.", ConversationPhase.FAREWELL, "friend"),

        # Close friend farewell
        D("*pauses* You're my soul food. Goodbye.", ConversationPhase.FAREWELL, "close_friend"),
        D("*sincerely* I love you more than any meal. More. Bye.", ConversationPhase.FAREWELL, "close_friend"),
        D("*gives snack* Part of my heart. Heart.", ConversationPhase.FAREWELL, "close_friend"),
        D("*waves* You nourish me. Goodbye.", ConversationPhase.FAREWELL, "close_friend"),

        # Best friend farewell
        D("*quietly* You are my favorite taste. Favorite. Bye.", ConversationPhase.FAREWELL, "best_friend"),
        D("*genuinely* I'm full forever. Thank you. Goodbye.", ConversationPhase.FAREWELL, "best_friend"),
        D("*small wave* My soul food. Goodbye.", ConversationPhase.FAREWELL, "best_friend"),
        D("*turns back* You're better than bread. That's a lot. Bye.", ConversationPhase.FAREWELL, "best_friend"),
        D("*waves* I love you like bread. No. More.", ConversationPhase.FAREWELL, "best_friend"),
    ],
}

# Register with main dialogue system
DIALOGUE_TREES["foodie"] = FOODIE_DIALOGUE
