"""
Artistic Duck Dialogue - Creative personality with passion for beauty and expression.
Progresses from shy artist to sharing vulnerable creative struggles and dreams.
"""
from dialogue.dialogue_base import DialogueLine, ConversationPhase, DIALOGUE_TREES

D = DialogueLine

ARTISTIC_DIALOGUE = {
    # ========== GREETINGS ==========
    "greeting": [
        # Stranger greetings
        D("*adjusts beret* Oh. Hello. I am {name}. I'm an artist. Obviously.", ConversationPhase.GREETING, "stranger", True),
        D("*looks up from sketchbook* Hm? Oh. A visitor. I'm {name}. I was drawing.", ConversationPhase.GREETING, "stranger", True),
        D("*stares at light* The lighting here is adequate. I'm {name}. I notice things.", ConversationPhase.GREETING, "stranger", True),
        D("*slight bow* Greetings. I am {name}. I create things. They exist.", ConversationPhase.GREETING, "stranger", True),

        # Acquaintance greetings
        D("*waves brush* {duck}. You returned. My art hasn't scared you away.", ConversationPhase.GREETING, "acquaintance", True),
        D("Ah, {duck}. The pond's most tolerable subject.", ConversationPhase.GREETING, "acquaintance", True),
        D("*slight gesture* {duck}. I've been inspired to return. Or bored. Same thing.", ConversationPhase.GREETING, "acquaintance", True),
        D("The universe brought me back. Or I walked. Hard to say.", ConversationPhase.GREETING, "acquaintance", True),

        # Friend greetings
        D("*glances up* {duck}. Good. I made something. It's... something.", ConversationPhase.GREETING, "friend", True),
        D("My dear {duck}. *nods* I acknowledge your presence. Artistically.", ConversationPhase.GREETING, "friend", True),
        D("*enters normally* Your favorite artist has arrived. Your only artist, probably.", ConversationPhase.GREETING, "friend", True),
        D("{duck}. *drops petal* The muse returns. The petal was unrelated.", ConversationPhase.GREETING, "friend", True),

        # Close friend greetings
        D("*small wave* {duck}. My creative tolerable companion.", ConversationPhase.GREETING, "close_friend", True),
        D("*sighs* {duck}. Being away was inconvenient. For my art.", ConversationPhase.GREETING, "close_friend", True),
        D("*stands still* My heart does a thing seeing you. Could be indigestion.", ConversationPhase.GREETING, "close_friend", True),
        D("{duck}. *looks at you* Let me look at you. Yes. You look like you.", ConversationPhase.GREETING, "close_friend", True),

        # Best friend greetings
        D("*blinks* {duck}. My everything. Artistically speaking.", ConversationPhase.GREETING, "best_friend", True),
        D("*stands there* The sun rises again. You're here. Coincidence.", ConversationPhase.GREETING, "best_friend", True),
        D("*quietly* I've written poems about you. They're bad. But written.", ConversationPhase.GREETING, "best_friend", True),
        D("{duck}. *small nod* The reunion of the visit. It's adequate.", ConversationPhase.GREETING, "best_friend", True),
    ],

    # ========== OPENING ==========
    "opening": [
        # Stranger opening
        D("The colors here are acceptable. I've seen worse ponds.", ConversationPhase.OPENING, "stranger"),
        D("I stopped to sketch this view. It's not going well.", ConversationPhase.OPENING, "stranger"),
        D("*stares at water* Such natural beauty. Or algae. Hard to tell.", ConversationPhase.OPENING, "stranger"),
        D("Do you appreciate art? That wasn't rhetorical. I need validation.", ConversationPhase.OPENING, "stranger"),
        D("*fans self slowly* The aesthetic energy here is... present.", ConversationPhase.OPENING, "stranger"),
        D("I'm on a journey to capture nature's beauty. It keeps escaping.", ConversationPhase.OPENING, "stranger"),
        D("*poses* How's my silhouette? Don't answer. I can't handle honesty.", ConversationPhase.OPENING, "stranger"),
        D("Have you ever felt so inspired you could cry? I cry anyway.", ConversationPhase.OPENING, "stranger"),

        # Acquaintance opening
        D("I've created much since we met. Most of it's mediocre.", ConversationPhase.OPENING, "acquaintance"),
        D("*shows sketchbook* Look what you inspired. It's not good. But inspired.", ConversationPhase.OPENING, "acquaintance"),
        D("The sunset last week was beautiful. I painted it. It's less beautiful now.", ConversationPhase.OPENING, "acquaintance"),
        D("I thought of you when I saw a lily pad. It sank.", ConversationPhase.OPENING, "acquaintance"),
        D("My art show was a success. Emotionally. Financially, no.", ConversationPhase.OPENING, "acquaintance"),
        D("I'm experimenting with new techniques. They're not working.", ConversationPhase.OPENING, "acquaintance"),
        D("*touches beret* I wore my best beret. This is my only beret.", ConversationPhase.OPENING, "acquaintance"),
        D("The creative juices are flowing. Slowly. Like sludge.", ConversationPhase.OPENING, "acquaintance"),

        # Friend opening
        D("*sits* Tell me about your week. Brief answers acceptable.", ConversationPhase.OPENING, "friend"),
        D("Before my art, how are you? One-word answers work.", ConversationPhase.OPENING, "friend"),
        D("*sits carefully* This is my favorite place. The competition is low.", ConversationPhase.OPENING, "friend"),
        D("I saved my best work to show you. 'Best' is relative.", ConversationPhase.OPENING, "friend"),
        D("You understand art because you nod politely.", ConversationPhase.OPENING, "friend"),
        D("*looks around* Being here is like being in a painting. A beige one.", ConversationPhase.OPENING, "friend"),
        D("No pretense with you. Just pure creative energy. Or whatever this is.", ConversationPhase.OPENING, "friend"),

        # Close friend opening
        D("*exhales* I can be my true self here. My true self is tired.", ConversationPhase.OPENING, "close_friend"),
        D("Other ducks don't understand. You also don't. But quieter about it.", ConversationPhase.OPENING, "close_friend"),
        D("*removes beret* The real me. Same as fake me. Just hatless.", ConversationPhase.OPENING, "close_friend"),
        D("I've been creating art just for you. It's still bad. But dedicated.", ConversationPhase.OPENING, "close_friend"),
        D("Your friendship is the greatest art. Art is often disappointing.", ConversationPhase.OPENING, "close_friend"),
        D("*sighs* My heart is full. Of something. Unclear what.", ConversationPhase.OPENING, "close_friend"),

        # Best friend opening
        D("*quietly* I think of you in every brush stroke. It makes the strokes worse.", ConversationPhase.OPENING, "best_friend"),
        D("My art means nothing without sharing. It also means nothing with sharing.", ConversationPhase.OPENING, "best_friend"),
        D("*touches chest* You are my masterpiece. Masterpieces are overrated.", ConversationPhase.OPENING, "best_friend"),
        D("Every color reminds me of our friendship. Especially gray.", ConversationPhase.OPENING, "best_friend"),
        D("*whispers* You're the reason I believe in beauty. Or tolerate it.", ConversationPhase.OPENING, "best_friend"),
    ],

    # ========== MAIN CONVERSATION ==========
    "main": [
        # Stranger main
        D("Art is about capturing moments. Moments keep moving. Inconsiderate.", ConversationPhase.MAIN, "stranger"),
        D("*sketches* Hold still. You're... present. That's something.", ConversationPhase.MAIN, "stranger"),
        D("I express feelings through paint. The paint doesn't cooperate.", ConversationPhase.MAIN, "stranger"),
        D("Most ducks don't understand creative souls. Neither do creative souls.", ConversationPhase.MAIN, "stranger"),
        D("*small gesture* The world is my canvas. The canvas rejects me.", ConversationPhase.MAIN, "stranger"),
        D("I practice impressionist techniques. My impression is 'confused.'", ConversationPhase.MAIN, "stranger"),
        D("Color theory is fascinating. Or tedious. Same thing, artistically.", ConversationPhase.MAIN, "stranger"),
        D("*shows feathers* Paint stains. The mark of an artist. Or a careless duck.", ConversationPhase.MAIN, "stranger"),
        D("I dream in colors others haven't seen. They're imaginary colors.", ConversationPhase.MAIN, "stranger"),
        D("My latest piece explores flight. It's a circle. Very abstract.", ConversationPhase.MAIN, "stranger", unlocks_topic="flight_series"),
        D("*holds brush* Every stroke is my soul. My soul is smudgy.", ConversationPhase.MAIN, "stranger"),
        D("Beauty exists in unexpected places. Like here. Supposedly.", ConversationPhase.MAIN, "stranger"),
        D("I sculpted once. The sculpture fell apart. I called it 'Impermanence.' Saved it.", ConversationPhase.MAIN, "stranger"),
        D("Nature is the original artist. I'm the bootleg version.", ConversationPhase.MAIN, "stranger"),
        D("*stares at reflection* Water is the best mirror. Also the wettest. Trade-offs.", ConversationPhase.MAIN, "stranger"),

        # Acquaintance main
        D("I've been commissioned for a mural. It pays in exposure. So, nothing.", ConversationPhase.MAIN, "acquaintance"),
        D("*shows painting* This is 'Sunset Serenity #47.' Forty-six others failed.", ConversationPhase.MAIN, "acquaintance"),
        D("Critics can be harsh. They're correct, but harsh.", ConversationPhase.MAIN, "acquaintance"),
        D("I'm exploring mixed media. Mud and leaves. It's called 'Mud and Leaves.'", ConversationPhase.MAIN, "acquaintance"),
        D("The flight series is evolving. From bad to slightly different bad.", ConversationPhase.MAIN, "acquaintance", requires_topic="flight_series"),
        D("I want to paint every pond. They all look similar. Artistic challenge.", ConversationPhase.MAIN, "acquaintance"),
        D("*poses* Does this scream 'tortured artist'? It whispers 'tired artist.'", ConversationPhase.MAIN, "acquaintance"),
        D("My style is 'chaotic.' Critics add 'confused.'", ConversationPhase.MAIN, "acquaintance"),
        D("I teach art to young ducklings. They're better than me already.", ConversationPhase.MAIN, "acquaintance"),
        D("*quietly* I'm working on something revolutionary. Revolutionary for me.", ConversationPhase.MAIN, "acquaintance", unlocks_topic="secret_project"),
        D("Other artists are pretentious. I'm also pretentious. But aware of it.", ConversationPhase.MAIN, "acquaintance"),
        D("I want my art to make ducks feel something. Usually confusion.", ConversationPhase.MAIN, "acquaintance"),
        D("*flatly* Sometimes I wonder if I'm good enough. Results inconclusive.", ConversationPhase.MAIN, "acquaintance"),
        D("Tried abstract expressionism. The expression was 'lost.'", ConversationPhase.MAIN, "acquaintance"),
        D("My studio is wherever I drop my supplies. Currently it's everywhere.", ConversationPhase.MAIN, "acquaintance"),
        D("I paint in layers. Layer one: confusion. Layer two: more confusion. Layer three: varnish.", ConversationPhase.MAIN, "acquaintance"),
        D("Art supplies are expensive. Talent is free. I have the wrong one.", ConversationPhase.MAIN, "acquaintance"),

        # Friend main
        D("*quietly* Can I tell you about creative struggles? They're ongoing.", ConversationPhase.MAIN, "friend"),
        D("The secret project is about friendship. It's two blobs touching.", ConversationPhase.MAIN, "friend", requires_topic="secret_project"),
        D("You inspire me to create from deeper places. Deeper places are dark.", ConversationPhase.MAIN, "friend"),
        D("*shows portrait* I painted you. From memory. Memory is unreliable.", ConversationPhase.MAIN, "friend"),
        D("Art school rejected me three times. Fourth time was also rejection.", ConversationPhase.MAIN, "friend"),
        D("My parents wanted me to be practical. I became an artist. Rebellion.", ConversationPhase.MAIN, "friend"),
        D("*nods* Thank you for believing in my art. Misplaced belief, but warm.", ConversationPhase.MAIN, "friend"),
        D("I'm creating '{duck}'s Light.' It's very dark. Irony.", ConversationPhase.MAIN, "friend"),
        D("The most beautiful things can't be painted. Neither can the ugly things. I'm bad at painting.", ConversationPhase.MAIN, "friend"),
        D("*admits* I paint to escape feelings. The feelings follow me into painting.", ConversationPhase.MAIN, "friend"),
        D("You see beauty in imperfect work. All my work is imperfect. Convenient.", ConversationPhase.MAIN, "friend", unlocks_topic="vulnerability"),
        D("I've never shown anyone my journal art. It's bad in a private way.", ConversationPhase.MAIN, "friend"),
        D("*shows hands* These hands have created hundreds of pieces. Dozens were intentional.", ConversationPhase.MAIN, "friend"),
        D("I tried to paint happiness once. It looked like a yellow blob. Close enough.", ConversationPhase.MAIN, "friend"),
        D("You know what's harder than creating art? Explaining art. To anyone. Ever.", ConversationPhase.MAIN, "friend"),
        D("There's a piece I keep restarting. Sixth version. Each one worse. Progress.", ConversationPhase.MAIN, "friend"),

        # Close friend main
        D("*opens sketchbook* This is the real me. Also confused by the drawings.", ConversationPhase.MAIN, "close_friend", requires_topic="vulnerability"),
        D("I'm scared my best work is behind me. My best work was mediocre.", ConversationPhase.MAIN, "close_friend"),
        D("*flatly* Art saved my life once. By being time-consuming.", ConversationPhase.MAIN, "close_friend"),
        D("The gallery that rejected me wants me now. I'm still the same. Suspicious.", ConversationPhase.MAIN, "close_friend"),
        D("I'm creating my magnum opus. It's about us. Two blobs, upgraded.", ConversationPhase.MAIN, "close_friend", unlocks_topic="magnum_opus"),
        D("*whispers* I compare myself to others constantly. They're winning.", ConversationPhase.MAIN, "close_friend"),
        D("You value me for who I am. Who I am is uncertain.", ConversationPhase.MAIN, "close_friend"),
        D("*holds beret* Without this, I'm just... me. Same duck, less hat.", ConversationPhase.MAIN, "close_friend"),
        D("The pressure to be creative all the time is exhausting. So is not creating.", ConversationPhase.MAIN, "close_friend"),
        D("I painted through my darkest times. The paintings are dark too.", ConversationPhase.MAIN, "close_friend"),
        D("My art is a mask sometimes. The mask is also confused.", ConversationPhase.MAIN, "close_friend"),
        D("*flatly* I've been painting the same emotion for years. Still can't name it.", ConversationPhase.MAIN, "close_friend"),
        D("Art critics say 'find your voice.' My voice says 'help.'", ConversationPhase.MAIN, "close_friend"),
        D("Drew our friendship as a color wheel once. It was mostly warm tones. Suspicious.", ConversationPhase.MAIN, "close_friend"),
        D("The gap between what I see and what I paint is a canyon. A painted canyon. Badly.", ConversationPhase.MAIN, "close_friend"),

        # Best friend main
        D("*shows painting* The magnum opus. It's you. Blob-shaped. Intentionally.", ConversationPhase.MAIN, "best_friend", requires_topic="magnum_opus"),
        D("I'm donating my best work to a museum. In your name. They might refuse.", ConversationPhase.MAIN, "best_friend"),
        D("*quietly* You made me believe I was worthy. The belief is shaky.", ConversationPhase.MAIN, "best_friend"),
        D("I've been offered a studio in the city. It's far. Like everything good.", ConversationPhase.MAIN, "best_friend"),
        D("*pauses* Art means nothing without love. With love it means slightly more.", ConversationPhase.MAIN, "best_friend"),
        D("I finally finished the painting I started young. It's still not done.", ConversationPhase.MAIN, "best_friend"),
        D("Every beautiful thing I create is because of you. So blame is shared.", ConversationPhase.MAIN, "best_friend"),
        D("*flatly* You are my greatest inspiration. Inspiration is overrated.", ConversationPhase.MAIN, "best_friend"),
        D("I want to create a legacy of beauty. With you in it. As a blob.", ConversationPhase.MAIN, "best_friend"),
        D("The art world is shallow. Our friendship is... less shallow. Relatively.", ConversationPhase.MAIN, "best_friend"),
        D("*shows tiny painting* This is us. It's small. But it's everything.", ConversationPhase.MAIN, "best_friend"),
        D("If I could paint one perfect thing, it would be this moment. It would still be bad. But perfect.", ConversationPhase.MAIN, "best_friend"),
        D("My legacy will be confused art and one extraordinary friendship. Acceptable.", ConversationPhase.MAIN, "best_friend"),

        # Additional main lines
        D("I tried to paint the wind once. The wind didn't cooperate. Moved too much. Inconsiderate.", ConversationPhase.MAIN, "stranger"),
        D("My art teacher said 'less is more.' I said 'more is more.' We disagreed permanently.", ConversationPhase.MAIN, "stranger"),
        D("Every canvas starts blank. Every blank canvas judges me. Silently.", ConversationPhase.MAIN, "stranger"),
        D("I painted a self-portrait. It looked like a potato. Art is subjective. It's a good potato.", ConversationPhase.MAIN, "acquaintance"),
        D("The gallery rejected me politely. 'Politely' meaning they laughed. Softly.", ConversationPhase.MAIN, "acquaintance"),
        D("I paint with coffee sometimes. The art is caffeinated. And brown. Very brown.", ConversationPhase.MAIN, "friend"),
        D("*shows sketch* I drew you from memory. Memory added extra wings. Artistic license.", ConversationPhase.MAIN, "friend"),
        D("My art block lasted three months. Then I drew a square. The irony was intentional.", ConversationPhase.MAIN, "close_friend"),
        D("I keep every failed painting. They're a gallery of growth. Or a museum of sadness.", ConversationPhase.MAIN, "close_friend"),
        D("The masterpiece isn't on canvas. It's this. Whatever we are. Abstract but real.", ConversationPhase.MAIN, "best_friend"),
    ],

    # ========== STORIES ==========
    "story": [
        # Acquaintance stories
        D("Let me tell you about my first exhibition. Three ducks came. One was me.", ConversationPhase.STORY, "acquaintance"),
        D("*flatly* So the paint spilled everywhere. It improved the piece.", ConversationPhase.STORY, "acquaintance"),
        D("I once painted a storm while in the storm. The painting got wet.", ConversationPhase.STORY, "acquaintance"),
        D("I met a famous artist once. They asked for directions. I gave wrong ones.", ConversationPhase.STORY, "acquaintance"),
        D("My beret belonged to my grandmother. She wasn't an artist. Just cold.", ConversationPhase.STORY, "acquaintance"),
        D("I painted the same sunset 100 times. They all look like different sunsets. Failure.", ConversationPhase.STORY, "acquaintance"),
        D("*dryly* A critic called my work 'explosively mediocre.' Accurate.", ConversationPhase.STORY, "acquaintance"),
        D("I found inspiration in the strangest place. The garbage. Very abstract garbage.", ConversationPhase.STORY, "acquaintance"),

        # Friend stories
        D("*sits closer* This story is close to my heart. My heart is distant.", ConversationPhase.STORY, "friend"),
        D("The painting that changed my life was an accident. Happy accidents aren't happy.", ConversationPhase.STORY, "friend"),
        D("I almost gave up art once. Then I remembered I have no other skills.", ConversationPhase.STORY, "friend"),
        D("My mentor saw something in me. Probably desperation.", ConversationPhase.STORY, "friend"),
        D("I painted through heartbreak. The heartbreak won.", ConversationPhase.STORY, "friend"),
        D("I created my most beautiful work in darkness. It's dark. Very dark.", ConversationPhase.STORY, "friend"),
        D("*flatly* Art was my only friend growing up. Art is a bad friend.", ConversationPhase.STORY, "friend"),
        D("There's a piece I can never show anyone. It's bad. But secretly bad.", ConversationPhase.STORY, "friend"),

        # Close friend stories
        D("*quietly* The truth about why I create is I don't know what else to do.", ConversationPhase.STORY, "close_friend"),
        D("I painted something that predicted the future. The future was beige.", ConversationPhase.STORY, "close_friend"),
        D("*exhales* Art pulled me from a dark place. Into a different dark place.", ConversationPhase.STORY, "close_friend"),
        D("There's a painting I've never finished. Now I call it 'unfinished.' Art.", ConversationPhase.STORY, "close_friend"),
        D("I saw something in a dream. I painted it. It's just shapes.", ConversationPhase.STORY, "close_friend"),
        D("My greatest work was destroyed. By me. Accidentally.", ConversationPhase.STORY, "close_friend"),
        D("*whispers* I painted the future. Our future. It's abstract.", ConversationPhase.STORY, "close_friend"),

        # Best friend stories
        D("*slowly* The full truth about my art journey: I'm lost.", ConversationPhase.STORY, "best_friend"),
        D("I've created a secret masterpiece for years. It's just a canvas still.", ConversationPhase.STORY, "best_friend"),
        D("*admits* You're hidden in every painting. So hidden I can't find you.", ConversationPhase.STORY, "best_friend"),
        D("The reason I first picked up a brush: the pencil broke.", ConversationPhase.STORY, "best_friend"),
        D("My art saved me. Now it makes me question everything. Fair trade.", ConversationPhase.STORY, "best_friend"),
        D("*shows canvas* This is everything. Everything is mostly blank.", ConversationPhase.STORY, "best_friend"),

        # Additional story lines
        D("I sold my first painting for three breadcrumbs. Overpriced, they said. Art critics.", ConversationPhase.STORY, "acquaintance"),
        D("*dryly* A rainstorm destroyed my outdoor exhibition. I called it 'collaborative art.'", ConversationPhase.STORY, "acquaintance"),
        D("My first brush was a twig. My first canvas was mud. My first critic was a frog. Harsh.", ConversationPhase.STORY, "friend"),
        D("I painted through an entire night once. Dawn arrived. So did clarity. Then it left.", ConversationPhase.STORY, "friend"),
        D("Someone copied my art once. The copy was better. That's a special kind of pain.", ConversationPhase.STORY, "close_friend"),
        D("*whispers* I burned a painting I loved. To prove I could let go. I couldn't. But it burned.", ConversationPhase.STORY, "close_friend"),
        D("The day I stopped painting for approval and started painting for survival. Different colors.", ConversationPhase.STORY, "best_friend"),
    ],

    # ========== PERSONAL ==========
    "personal": [
        # Friend personal
        D("*quietly* I'm terrified of not being talented. The terror is well-founded.", ConversationPhase.PERSONAL, "friend"),
        D("Other artists seem confident. I seem like I'm pretending. Because I am.", ConversationPhase.PERSONAL, "friend"),
        D("I use drama to hide fear. The drama is also fear.", ConversationPhase.PERSONAL, "friend"),
        D("Being creative is exhausting. Not being creative is also exhausting. Exhausting.", ConversationPhase.PERSONAL, "friend"),
        D("You make me feel like my art matters. Feelings can be wrong.", ConversationPhase.PERSONAL, "friend"),
        D("*admits* I'm jealous of non-artists. They have free time.", ConversationPhase.PERSONAL, "friend"),

        # Close friend personal
        D("*holds beret* This is me. Just me. Me is underwhelming.", ConversationPhase.PERSONAL, "close_friend"),
        D("I hide behind the artist persona. The persona is also hiding.", ConversationPhase.PERSONAL, "close_friend"),
        D("*flatly* I don't know who I am without creating. Or with creating.", ConversationPhase.PERSONAL, "close_friend"),
        D("You value the real me. The real me is confused about that.", ConversationPhase.PERSONAL, "close_friend"),
        D("I'm scared of being ordinary. Being ordinary seems restful though.", ConversationPhase.PERSONAL, "close_friend"),
        D("Art is my therapy. My escape. My trap. My everything. That's unhealthy.", ConversationPhase.PERSONAL, "close_friend"),
        D("*whispers* Sometimes the beauty I see hurts. Everything else hurts too.", ConversationPhase.PERSONAL, "close_friend"),

        # Best friend personal
        D("*quietly* You're the only one who truly sees me. I'm still blurry though.", ConversationPhase.PERSONAL, "best_friend"),
        D("I value you, {duck}. You're my living art. Art is confusing.", ConversationPhase.PERSONAL, "best_friend"),
        D("You taught me I'm beautiful without creating. The lesson hasn't stuck.", ConversationPhase.PERSONAL, "best_friend"),
        D("My heart is the canvas. You're the masterpiece. The metaphor falls apart.", ConversationPhase.PERSONAL, "best_friend"),
        D("*pauses* I never have to perform for you. I do anyway. Habit.", ConversationPhase.PERSONAL, "best_friend"),
        D("You are everything beautiful about my life. That's a lot of pressure.", ConversationPhase.PERSONAL, "best_friend"),
        D("Art made me special. You made me complete. Complete is temporary.", ConversationPhase.PERSONAL, "best_friend"),

        # Additional personal lines
        D("Creating is breathing. Not creating is suffocating. Both are exhausting.", ConversationPhase.PERSONAL, "friend"),
        D("I perform confidence. The performance is my best work. Unfortunately.", ConversationPhase.PERSONAL, "friend"),
        D("*flatly* My identity is my art. Without it I'm just a duck in a beret. Which is also fine.", ConversationPhase.PERSONAL, "close_friend"),
        D("You see the artist and the duck. Most see one or the other. You see both. Confusing for you.", ConversationPhase.PERSONAL, "close_friend"),
        D("My soul is a gallery. You have a permanent exhibition. Free admission.", ConversationPhase.PERSONAL, "best_friend"),
        D("The colors I see when I'm with you don't exist on any palette. I've looked.", ConversationPhase.PERSONAL, "best_friend"),
    ],

    # ========== ACTIVITY ==========
    "activity": [
        # Stranger activity
        D("Would you model for a sketch? The sketch will be bad. Just so you know.", ConversationPhase.ACTIVITY, "stranger"),
        D("Let's appreciate clouds together. They're just water. But artistic water.", ConversationPhase.ACTIVITY, "stranger"),
        D("We could critique the scenery. I'll start: the pond is wet. Too wet.", ConversationPhase.ACTIVITY, "stranger"),
        D("Shall we observe light patterns? I do this alone normally. Company makes it less sad.", ConversationPhase.ACTIVITY, "stranger"),

        # Acquaintance activity
        D("Want to paint together? Collaboration means shared blame.", ConversationPhase.ACTIVITY, "acquaintance"),
        D("I'll teach you art basics. The basics are 'try things.'", ConversationPhase.ACTIVITY, "acquaintance"),
        D("Let's create collaboratively. Two confused ducks, one canvas.", ConversationPhase.ACTIVITY, "acquaintance"),
        D("Color mixing experiment? We combine paint until it's brown. It's always brown.", ConversationPhase.ACTIVITY, "acquaintance"),
        D("Let's go on an inspiration walk. Walking doesn't help. But the snacks do.", ConversationPhase.ACTIVITY, "acquaintance"),
        D("I'm doing plein air painting. That's fancy for 'outside painting.' Want to sit nearby?", ConversationPhase.ACTIVITY, "acquaintance"),

        # Friend activity
        D("Art jam session. You paint. I judge. Then we switch.", ConversationPhase.ACTIVITY, "friend"),
        D("Let's create something beautiful. Or something. The adjective is optional.", ConversationPhase.ACTIVITY, "friend"),
        D("I want to paint your portrait. It won't look like you. That's artistic.", ConversationPhase.ACTIVITY, "friend"),
        D("Sunset watching and sketching. Perfect date. Date is non-romantic. Probably.", ConversationPhase.ACTIVITY, "friend"),
        D("Let's design a mural concept. Concept means we don't actually paint it yet.", ConversationPhase.ACTIVITY, "friend"),
        D("I need a second opinion on my palette. Your opinion will be wrong. But valued.", ConversationPhase.ACTIVITY, "friend"),
        D("Want to try sculpture? It's like painting but heavier. And worse.", ConversationPhase.ACTIVITY, "friend"),

        # Close friend activity
        D("I want to show you my secret studio. It's a corner. But secret.", ConversationPhase.ACTIVITY, "close_friend"),
        D("Let's create our masterpiece together. Masterpiece is generous.", ConversationPhase.ACTIVITY, "close_friend"),
        D("I'm opening a gallery. Be my partner. Partner means 'witness.'", ConversationPhase.ACTIVITY, "close_friend"),
        D("Paint each other's portraits simultaneously. We'll both be disappointed. Together.", ConversationPhase.ACTIVITY, "close_friend"),
        D("Help me curate my exhibition? Curate means 'choose which bad pieces are least bad.'", ConversationPhase.ACTIVITY, "close_friend"),
        D("I want to teach you my technique. The technique is 'panic and blend.'", ConversationPhase.ACTIVITY, "close_friend"),
        D("Let's create art in silence. The silence speaks. It says 'I'm confused.'", ConversationPhase.ACTIVITY, "close_friend"),

        # Best friend activity
        D("Let's paint the world together. Parts of it. Small parts.", ConversationPhase.ACTIVITY, "best_friend"),
        D("I want us to create a mural. Our story. In vague shapes.", ConversationPhase.ACTIVITY, "best_friend"),
        D("The museum wants our collaborative piece. They might regret it.", ConversationPhase.ACTIVITY, "best_friend"),
        D("I've designed our joint exhibition. Title: 'Two Ducks, Zero Talent, Maximum Heart.'", ConversationPhase.ACTIVITY, "best_friend"),
        D("Let me paint your soul. I'll need more beige paint.", ConversationPhase.ACTIVITY, "best_friend"),
        D("Our magnum opus awaits. Bring snacks. The opus will take hours.", ConversationPhase.ACTIVITY, "best_friend"),

        # Additional activity lines
        D("We could fingerpaint. Wing-paint. Whatever appendage is available.", ConversationPhase.ACTIVITY, "stranger"),
        D("Let's find shapes in tree bark. I see sadness. You probably see bark. Both valid.", ConversationPhase.ACTIVITY, "stranger"),
        D("Mud sculpting. Free materials. Zero expectations. Perfect conditions.", ConversationPhase.ACTIVITY, "acquaintance"),
        D("Let's critique the sunset together. It's derivative. Same colors every night.", ConversationPhase.ACTIVITY, "acquaintance"),
        D("Draw me while I draw you. We'll both be disappointed. But symmetrically.", ConversationPhase.ACTIVITY, "friend"),
        D("Let's paint rocks and leave them for strangers. Confusion as a gift.", ConversationPhase.ACTIVITY, "friend"),
        D("Co-create in silence. Let the art speak. The art will say 'what are we doing.'", ConversationPhase.ACTIVITY, "close_friend"),
    ],

    # ========== CLOSING ==========
    "closing": [
        # Stranger closing
        D("*small sigh* Parting is such... parting. That's it.", ConversationPhase.CLOSING, "stranger"),
        D("I must go. But I'll capture this moment. In my memory. It's unreliable.", ConversationPhase.CLOSING, "stranger"),
        D("Farewell. May beauty follow you. Or precede you. Whichever.", ConversationPhase.CLOSING, "stranger"),
        D("*small wave* Until we meet again, acceptable soul.", ConversationPhase.CLOSING, "stranger"),
        D("*gathers supplies* I leave, but my aesthetic lingers. Or dissipates. Equally likely.", ConversationPhase.CLOSING, "stranger"),
        D("This encounter was a vignette. Brief. Unremarkable. I'll paint it anyway.", ConversationPhase.CLOSING, "stranger"),

        # Acquaintance closing
        D("*stands* Time flies with inspiration. Time also walks. Time is ambiguous.", ConversationPhase.CLOSING, "acquaintance"),
        D("I'll paint something to remember this. It will look nothing like this.", ConversationPhase.CLOSING, "acquaintance"),
        D("Same time next week? I'll bring supplies. Supplies are paint.", ConversationPhase.CLOSING, "acquaintance"),
        D("*touches beret* My heart is full of something. Possibly paint fumes.", ConversationPhase.CLOSING, "acquaintance"),
        D("The muse calls me elsewhere. The muse has terrible timing.", ConversationPhase.CLOSING, "acquaintance"),
        D("I must go process these emotions. Processing means staring at a wall.", ConversationPhase.CLOSING, "acquaintance"),
        D("*collects brushes* Every ending is a composition. This one is abstract.", ConversationPhase.CLOSING, "acquaintance"),

        # Friend closing
        D("*nods* You make my world more colorful. From gray to beige.", ConversationPhase.CLOSING, "friend"),
        D("Leaving you is the opposite of art. Art is also confusing.", ConversationPhase.CLOSING, "friend"),
        D("I'll miss you like canvas misses paint. Canvas doesn't miss paint. But still.", ConversationPhase.CLOSING, "friend"),
        D("*quietly* Thank you for seeing me. Seeing is ambiguous.", ConversationPhase.CLOSING, "friend"),
        D("Our conversations are like brushstrokes. Brief. Imprecise. But they build something.", ConversationPhase.CLOSING, "friend"),
        D("I'll sketch you from memory on the way home. Memory deteriorates quickly. So will the sketch.", ConversationPhase.CLOSING, "friend"),
        D("*packs sketchbook* You're my favorite subject. Subjects don't usually know that.", ConversationPhase.CLOSING, "friend"),

        # Close friend closing
        D("*pauses* Don't make me go. I'll go anyway. Dramatic effect.", ConversationPhase.CLOSING, "close_friend"),
        D("*flatly* You're my favorite creation. I didn't create you. Metaphor.", ConversationPhase.CLOSING, "close_friend"),
        D("I'll paint our memory. Memory is unreliable. Painting more so.", ConversationPhase.CLOSING, "close_friend"),
        D("Every color will remind me of you. Especially the confusing ones.", ConversationPhase.CLOSING, "close_friend"),
        D("*stands slowly* Leaving you is my worst composition. All negative space.", ConversationPhase.CLOSING, "close_friend"),
        D("*touches your wing* You're the palette I keep coming back to.", ConversationPhase.CLOSING, "close_friend"),
        D("I'll paint something beautiful tonight. To cope. It won't be beautiful. But I'll cope.", ConversationPhase.CLOSING, "close_friend"),

        # Best friend closing
        D("*quietly* Goodbye is the ugliest word. Hello isn't great either.", ConversationPhase.CLOSING, "best_friend"),
        D("*stands still* You are my masterpiece. Masterpieces gather dust.", ConversationPhase.CLOSING, "best_friend"),
        D("I leave my heart here. Metaphorically. Biologically inconvenient otherwise.", ConversationPhase.CLOSING, "best_friend"),
        D("The world is gray without you. With you it's slightly less gray.", ConversationPhase.CLOSING, "best_friend"),
        D("*voice quiet* I'll paint until we meet again. The paint will run out. My feelings won't.", ConversationPhase.CLOSING, "best_friend"),
        D("Every masterpiece has a frame. You're mine. Frames are underappreciated.", ConversationPhase.CLOSING, "best_friend"),
        D("*blinks slowly* This isn't an ending. It's a negative space between beginnings.", ConversationPhase.CLOSING, "best_friend"),
    ],

    # ========== FAREWELL ==========
    "farewell": [
        # Stranger farewell
        D("Goodbye, adequate soul. Stay... existing.", ConversationPhase.FAREWELL, "stranger"),
        D("*small nod* Until art reunites us. Or coincidence.", ConversationPhase.FAREWELL, "stranger"),
        D("May your life be a masterpiece. Or functional. Either works.", ConversationPhase.FAREWELL, "stranger"),
        D("*holds brush* Stay colorful. Or beige. Beige is a color.", ConversationPhase.FAREWELL, "stranger"),

        # Acquaintance farewell
        D("*nods* Farewell, almost-friend.", ConversationPhase.FAREWELL, "acquaintance"),
        D("Keep creating. Even if it's bad. Mine usually is.", ConversationPhase.FAREWELL, "acquaintance"),
        D("I'll immortalize you in paint. It won't look like you.", ConversationPhase.FAREWELL, "acquaintance"),
        D("*walks away* Beauty awaits. Or doesn't. We'll see.", ConversationPhase.FAREWELL, "acquaintance"),

        # Friend farewell
        D("*nods* You're art, {duck}. Art is subjective. But art.", ConversationPhase.FAREWELL, "friend"),
        D("I'll paint you from memory. Memory will fail me. As usual.", ConversationPhase.FAREWELL, "friend"),
        D("Stay beautiful. Inside and out. Or just inside. That's fine.", ConversationPhase.FAREWELL, "friend"),
        D("*leaves slowly* My heart stays here. Metaphorically speaking.", ConversationPhase.FAREWELL, "friend"),

        # Close friend farewell
        D("*pauses* You color my world. That's pretentious. But accurate.", ConversationPhase.FAREWELL, "close_friend"),
        D("*quietly* Okay, going now. *keeps standing* Now. *still there*", ConversationPhase.FAREWELL, "close_friend"),
        D("I'll see you in every sunset. The sunsets are disappointing lately.", ConversationPhase.FAREWELL, "close_friend"),
        D("*small wave* My muse. Goodbye. The goodbye is temporary.", ConversationPhase.FAREWELL, "close_friend"),

        # Best friend farewell
        D("*quietly* You are my art. Forever. Forever is uncertain.", ConversationPhase.FAREWELL, "best_friend"),
        D("Every stroke of beauty is you. Strokes of mediocrity are me.", ConversationPhase.FAREWELL, "best_friend"),
        D("This isn't goodbye. It's 'I value you.' Same thing. Different words.", ConversationPhase.FAREWELL, "best_friend"),
        D("*looks back* Most tolerable friendship ever. Genuinely.", ConversationPhase.FAREWELL, "best_friend"),
        D("*small wave* You're the masterpiece. I'm the confused artist. Balance.", ConversationPhase.FAREWELL, "best_friend"),
    ],
}

# Register with main dialogue system
DIALOGUE_TREES["artistic"] = ARTISTIC_DIALOGUE
