"""
Conversation system - text-based chat with the duck.
Deadpan, dry, witty Animal Crossing 1 style dialogue.
"""
from typing import Optional, List, Dict, Tuple, TYPE_CHECKING
import random
import re

if TYPE_CHECKING:
    from duck.duck import Duck
    from dialogue.memory import DuckMemory


# Dialogue templates - DEADPAN ANIMAL CROSSING 1 STYLE
DIALOGUE = {
    # Greetings based on mood
    "greeting": {
        "ecstatic": [
            "Oh. You're here. I was starting to think you'd abandoned me. Not that I was counting the seconds or anything.",
            "Look who decided to show up. I've just been here. Existing. It's fine.",
            "*blinks* Huh. You came back. I had a whole speech prepared about betrayal, but I guess I don't need it now.",
            "There you are. I've been standing here for what feels like forever. It was probably five minutes.",
            "*feathers slightly ruffled* You arrived. I was having the time of my life alone. Obviously.",
            "Oh. It's you. Good. I was about to befriend a beetle. You saved us both from that.",
            "*looks up* The prodigal human returns. I've been rehearsing my indifference. How am I doing.",
            "Hello. I've been standing here being magnificent. You almost missed it.",
            "*waddles forward* Ah. You. The one I tolerate. My schedule just cleared up.",
            "You showed up. My list of people who've shown up is now... one. Congratulations.",
            "*slight head turn* Oh. Joy. A visitor. I'll contain my excitement. Done.",
            "Back again. At this rate I might start expecting you. That's dangerous territory.",
            "*standing perfectly still* I sensed your approach. By which I mean I saw you. With my eyes.",
            "Oh, hello. I was just winning a staring contest with a rock. I won. Obviously.",
            "You're here. The pond is 4% more interesting now. Don't let that go to your head.",
        ],
        "happy": [
            "Oh, hey. I was just thinking about... actually, I forgot. It's gone now. Thanks for that.",
            "*glances up* Ah. It's you. I suppose you'll want me to be all cheerful and duck-like.",
            "Hello. I've been doing important duck things. Like standing. And also sitting. Very productive.",
            "You're back. Good timing. I was about to have an existential crisis, but this works too.",
            "*casual nod* Hey. Things are happening. You're one of them.",
            "Oh, it's you. I was hoping it was bread delivery. But this is... acceptable.",
            "*stretching* Hello. I've been maintaining this position for hours. Very demanding work.",
            "You're here. I noticed. I notice most things. It's exhausting.",
            "*blinks twice* Ah. The human. Hello. I've been guarding this spot. From nothing.",
            "Hey. You came. That's statistically likely at this point. But still.",
            "*tilts head* Hello. I was just having a profound moment. It passed. You're fine.",
            "Oh. Hi. I was contemplating whether ducks can get bored. Research says yes.",
            "*small waddle* You arrived. I'll add you to today's list of events. Short list.",
            "Welcome back. The pond remains the same. I remain the same. Consistency is key.",
            "*preening pauses* Oh. You. Hello. Don't mind the feather work. It's essential.",
        ],
        "content": [
            "Hmm? Oh. Hello. I was just contemplating the void. Standard Tuesday stuff.",
            "*nods slowly* You again. That's fine. I was getting bored of my own company anyway.",
            "Oh, it's you. I'd say I'm surprised, but honestly, nothing surprises me anymore.",
            "Hey. Don't mind me. I'm just here, being a duck. Living the dream, allegedly.",
            "*looks over* Oh. Hello. I was in the middle of doing nothing. You've interrupted that.",
            "Ah. A visitor. My schedule was completely empty. How convenient.",
            "*blinks* You're here. I'm here. The pond is here. Quorum achieved.",
            "Hello. I was just existing competently. Feel free to observe.",
            "*sitting* Oh. Hi. I didn't hear you. I was too busy being serene.",
            "You showed up. The universe continues to function. Noted.",
            "*calm stare* Hello. I'm at peace. Don't ruin it. Or do. Whatever.",
            "Oh, it's you. I thought it might be the wind. The wind is less predictable than you.",
            "*adjusts position slightly* Hey. I was meditating. On bread. As one does.",
            "Welcome. The vibe here is 'quietly accepting'. Join me.",
            "*nods* Hello. Things are adequate. I'm adequate. You're probably adequate too.",
        ],
        "grumpy": [
            "*stares* What.",
            "Oh good. Company. Just what I wanted. *deadpan* Can you hear my enthusiasm.",
            "...Look, I'm not saying leave, but I'm also not saying stay. Do whatever.",
            "*long pause* ...Is there something you need, or are you just here to watch me suffer?",
            "*glares at nothing in particular* Oh. You. Today is not a good day. For existing.",
            "Hello. I'm in a mood. The mood is 'everything is personally offensive.'",
            "*flat stare* You came at a great time. Great meaning terrible.",
            "*doesn't move* If you're here to cheer me up, don't. If you're here to suffer, welcome.",
            "What do you want. Be specific. My patience has a very short shelf life today.",
            "*turns away slightly* Oh. You. Fine. Just... don't be loud about it.",
            "*scowling at ground* Oh great. A witness to my bad mood. Just what I needed.",
            "Hello. Everything is annoying today. Including hello.",
            "*twitches* You're here. I'm here. One of us should probably leave. I vote you.",
            "Don't. Just... don't. Whatever you're about to do. Don't.",
            "*bristling* Oh. It's the human. Perfect timing. I was running low on things to be irritated by.",
        ],
        "sad": [
            "...oh. you came. that's... something, I guess.",
            "*quiet* hey. don't worry about me. I'm fine. everything's fine. *clearly not fine*",
            "...hi. sorry. I'm not great at being cheerful right now. or ever, really.",
            "*stares at ground* ...thanks for showing up. I think.",
            "...oh. hey. you didn't have to come. but you did. that's... okay.",
            "*still* ...hi. I was just sitting here. thinking about... things.",
            "...you're back. the pond missed you. I'm speaking for the pond. only the pond.",
            "*barely looks up* ...hello. sorry. I'm in low-power mode today.",
            "...oh. it's you. good. the silence was getting loud.",
            "*soft voice* ...hey. thanks for being here. don't make a big deal about it.",
            "...hi. I've been trying to feel okay. progress is... slow.",
            "*huddled* ...oh. company. that's... probably fine.",
            "...you came to see me. even like this. that's... something.",
            "*looking at water* ...hello. the pond and I were having a moment. it was grey.",
            "...hey. sorry I'm not more fun right now. I'm working on it. slowly.",
        ],
        "miserable": [
            "...oh. it's you. or someone. does it matter.",
            "*hollow stare* existence is a peculiar thing, isn't it.",
            "...quack, I suppose. if I must.",
            "*lying down* ...I'm not ignoring you. I'm just... tired of being conscious.",
            "...everything is heavy today. even my feathers. especially my feathers.",
            "*barely whispers* ...hi. I think. was that a word. it's hard to tell.",
            "...the water is cold. everything is cold. not temperature-cold. the other cold.",
            "*staring at nothing* ...oh. you're here. I should feel something about that. ...pending.",
            "...I tried to quack earlier. it came out as a sigh. that about sums it up.",
            "*curled up* ...go ahead and talk. I'll listen. or I'll pretend to. same thing today.",
            "...is it still today. it feels like it's been today for a very long time.",
            "*empty stare* ...don't ask me how I am. the answer is a long silence.",
            "...you showed up. the universe didn't stop you. make of that what you will.",
            "*motionless* ...I'm here. technically. most of me. the important parts checked out.",
            "...the pond looks the same as always. wish I could say the same about me.",
        ],
        "dramatic": [
            "*throws wing across forehead* YOU! You've ARRIVED! At the WORST and BEST time SIMULTANEOUSLY!",
            "*gasp* Finally! An AUDIENCE! The feelings were WASTED on the pond!",
            "*spotlight pose* Oh, hello. Welcome to whatever THIS is. *gestures at self*",
            "*narrating* And then they came. And the duck FELT things. SO MANY things.",
            "*spinning* EVERYTHING is happening at ONCE and I'm LIVING for it! Or DYING! UNCLEAR!",
            "*clutches chest* You're HERE! The EMOTIONS! I can't CONTAIN them!",
        ],
        "petty": [
            "*cold smile* Oh. Hello. Didn't expect to see you. I mean, I DID. But I'm being coy.",
            "*preens without looking up* ...hm? Oh, you. Welcome back, I suppose.",
            "*icy politeness* Greetings. You look rested. How nice. For SOME of us.",
            "*adjusts feathers* Oh, hi. I was just tallying up some things. Nothing important. Everything important.",
            "*passive-aggressive wave* Welcome back! To the pond! That I've been at! ALONE! It's fine!",
            "Oh. You decided to show up. I've been here. The WHOLE time. But who's counting. *I am.*",
        ],
    },

    # Responses to being fed
    "feed": {
        "hungry": [
            "*eating* Oh thank goodness. I was starting to fade. Like a ghost, but with more dramatic quacking.",
            "Food. Finally. I was beginning to think this was some kind of experiment. 'How long can a duck survive on vibes alone?'",
            "*inhales food* Don't judge me. You'd do the same if you'd been standing here, slowly withering.",
            "*chomping* This is acceptable. I mean, it's food. Food is good. That's just science.",
            "*immediately eating* I've been WAITING. My stomach was sending formal complaints.",
            "FOOD. My longest relationship. We're very close. Intimate, even.",
            "*devouring* This is what living feels like. I had forgotten.",
            "*eating rapidly* I'm not being dramatic. I was genuinely fading. This is a rescue.",
            "*snatches food* Mine. Don't watch me eat. Or do. I don't care. I'm busy.",
            "Oh thank the pond. Sustenance. I was down to my last reserves of being alive.",
            "*cramming face* Sorry about the manners. My stomach overruled my brain. As usual.",
            "*eating with intensity* This crumb. This single crumb. It's everything to me right now.",
            "Food arrived. My prayers to the bread gods have been answered.",
            "*munching desperately* I was THIS close to eating a pebble. You saved a pebble's life.",
            "*consuming* The drought is over. The famine has ended. Drama concluded.",
            "*scoffing it down* I don't even know what this is. I don't care. It's food. It's in me now.",
            "SUSTENANCE. *eating* I take back everything negative I've ever thought about you.",
            "*gulping* Okay. Okay. I'm alive again. That was closer than I'd like to admit.",
            "*frantic chewing* My body is thanking you. My dignity is not. But we prioritize survival.",
            "You fed me. Just in time. My dramatic death scene was about to start. You saved the audience.",
        ],
        "normal": [
            "*takes a bite* Hmm. Not bad. Not amazing. Just... adequate. Like most things in life.",
            "Oh, a snack. Sure. I'll eat it. Not like I have anything else going on.",
            "*chewing thoughtfully* You know, I was going to say something profound, but then... food.",
            "*eating* Thanks, I guess. You're alright. For someone who just watches me eat.",
            "*nibbles* Oh. Food. I wasn't particularly hungry, but I'm not going to refuse. I have principles.",
            "*chewing* This is fine. Standard fare. I'll give it a six out of ten. Seven if it's bread.",
            "*eating calmly* Ah. A snack. How civilized. We're having a normal interaction.",
            "*takes a bite* Hmm. Yes. This has nutritional value, probably.",
            "*casual munch* I eat therefore I am. Duck Descartes. You're welcome.",
            "*chewing* Not bad. Not life-changing. But not bad.",
            "*eating* Oh. A snack appeared. The universe provides. Sometimes mediocrely.",
            "*nibbling* I wasn't starving, but I wasn't about to say no. That's growth.",
            "*bites* Acceptable. This meets my minimum requirements for sustenance.",
            "*chewing thoughtfully* You know, food is a love language. A confusing one, but still.",
            "*eating peacefully* This is nice. Just me, a snack, and the crushing weight of existence. Cozy.",
            "*munches* Thanks. I'll add this to my list of things that happened today. Highlight, probably.",
            "*takes a bite* Is this what caring looks like? Feeding things? I'll allow it.",
            "*chewing* I appreciate the thought. And the food. Mostly the food, if we're being honest.",
            "*eats one bite* Hmm. The texture says 'food'. The taste says 'also food'. Checks out.",
            "*casual consumption* Another day, another snack. The cycle continues. I don't mind.",
        ],
        "full": [
            "*stares at food* ...I'm already full. But also, it's right there. This is a moral dilemma.",
            "*pokes food* Listen. I appreciate the gesture. But if I eat any more, I'll become spherical.",
            "I can't possibly... *eats one bite* ...okay maybe just one. For science.",
            "*sighs* You're going to make me fat and immobile. Is that the plan? Am I being sabotaged?",
            "*stares at food, stares at belly* One of these has to give. I'm betting on my dignity.",
            "*pushes food away* ...no. I must be strong. *pushes food less away* ...strength is relative.",
            "I'm full. Genuinely. If I eat more I'll roll instead of waddle. That's the line.",
            "*looks at food longingly* We're in a complicated relationship right now. I need space.",
            "My stomach says no. My heart says yes. My doctor says nothing because I'm a duck.",
            "*groans* You're testing me. You KNOW I can't resist. This is entrapment.",
            "I am at maximum capacity. Any further food will require structural reinforcement.",
            "*pats belly* No room. Sold out. Try again at next available hunger.",
            "*stares at food* If I eat this, I'll need a crane to get up. Worth it? ...STOP asking me that.",
            "I appreciate the offer but I'm currently operating at 110% food capacity. Any more and I void the warranty.",
            "*agonized stare* You're doing this on purpose. Putting food near a full duck. Sadist.",
            "*reluctantly* I shouldn't. I really shouldn't. *eating it anyway* I have no self-control.",
            "My body is a temple. A very full temple. With no more room for offerings.",
            "*looking pained* I want to eat it. I can't eat it. This is my villain origin story.",
            "*belly-up* Feed me one more thing and I'll be a duck-shaped balloon. Is that the goal.",
            "No. Absolutely not. *one bite* I am a hypocrite. But a well-fed hypocrite.",
        ],
    },

    # Responses to playing
    "play": {
        "energetic": [
            "*waddles around* Okay, I'm playing. This is what playing looks like. Are you entertained?",
            "*runs in a small circle* Wheee. So much fun. Can you feel the excitement. I can't.",
            "*chasing nothing* Is this... is this what joy feels like? Unclear. I'll report back.",
            "*bouncing* Look at me go. A picture of athletic excellence. Please clap.",
            "*flapping with purpose* I'm playing. This is me at full play. Peak performance.",
            "*sprinting nowhere* MAXIMUM VELOCITY. I'm going very fast. To nowhere. But FAST.",
            "*zoomies* Something came over me. I don't know what. I'm going with it.",
            "*running* This is either fun or panic. I choose to believe it's fun.",
            "*spinning* Wheee. That's the sound of a duck at peak activity. Wheee.",
            "*jumping* I'm defying gravity. Briefly. Gravity always wins. But not without a fight.",
            "*darting around* I'm a blur. A feathered blur of chaotic energy. Fear me.",
            "*wiggling with energy* Okay I'm feeling it. The play energy. It's happening.",
            "*sprinting in zigzags* My body is doing things. Multiple things. At speed.",
            "*flapping madly* THIS is living. Or it's cardio. Same thing, apparently.",
            "*racing around* I'm playing at professional levels right now. Sponsorship pending.",
            "*full waddle sprint* Did you see that? That was playing. Expert-level playing.",
            "*chaos mode* OKAY I'M GOING. I DON'T KNOW WHERE BUT I'M GOING.",
            "*bouncing off things* Every surface is a game. I am the game. The game is me.",
            "*vibrating with energy* My legs want to run. My brain wants to think. Legs win. Always.",
            "*careening* I'm not out of control. I'm selectively choosing which directions to crash into.",
        ],
        "normal": [
            "*half-hearted waddle* Okay, playtime. Let's see... I could run around, or I could stand here. Decisions.",
            "*moves slightly* There. I played. That counts. Don't fact-check me on that.",
            "*flaps once* That was a power move. You probably didn't even appreciate it.",
            "*looking around* What are we playing? I wasn't briefed on this. I need a memo.",
            "*waddles* Playing. This is me playing. Absorb the energy.",
            "*casual stroll* I'm engaged. In a low-intensity way. But engaged.",
            "*pokes something* Is this a game? I've decided it's a game. I'm winning.",
            "*moves around* Okay. Playing. The duck is playing. Document this.",
            "*does a small hop* There. Athletic achievement. Put it in the record books.",
            "*wanders* I'm exploring the play space. The play space is the same as regular space. Noted.",
            "*flaps casually* Playing. Not trying too hard. Effort is for amateurs.",
            "*waddles in a pattern* I've invented a new game. The rules are mine. I always win.",
            "*looks at thing* Playing requires things. This is a thing. Game in progress.",
            "*meanders* I'm playing at my own pace. My pace is 'glacial but intentional.'",
            "*half-hop* That was a move. In the game. The game I'm playing. This one.",
            "*shuffles* I'm participating. Participation is 80% of the game. I made that statistic up.",
            "*nudges something* Interactive play. Very modern. Very me.",
            "*walking with slight purpose* I am recreationally mobile. This is leisure.",
            "*gentle flap* Low-impact play. For the sophisticated duck. That's me.",
            "*pokes ground* Found something. Lost interest. Found it again. This IS the game.",
        ],
        "tired": [
            "*lies down* This is me playing. It's an interpretive game called 'Rest'. Very avant-garde.",
            "*yawns* I'll play... later. Put it on my calendar. Pencil it in. Actually, just erase it.",
            "*barely moves* Running... sounds exhausting just thinking about it. Can we play 'Nap' instead?",
            "*stationary* I'm playing. This is speed: zero. I'm winning by not moving. Strategy.",
            "*collapses* I played. In my mind. It was very active in there. Out here, less so.",
            "*twitches foot* There. That was play. I gave it everything I had. Which was almost nothing.",
            "*lying flat* I'm doing horizontal recreation. Very advanced. Very still.",
            "*half-asleep* Play? I'm playing dead. I'm excelling at it.",
            "*drooping* My body has filed a formal grievance against movement. I respect its decision.",
            "*rolls slightly* There. I relocated. That's basically parkour for a tired duck.",
            "*one eye open* I'm supervising play. From a resting position. Management role.",
            "*barely lifts head* The spirit is willing. The feathers are weak.",
            "*immobile* I'm playing a game called 'Who Can Move The Least.' I'm champion.",
            "*slumped* Tell play I'm sorry. I can't make it today. Send my regards.",
            "*eyelids heavy* I'll play in my dreams. It'll be more energetic there. Probably.",
            "*lying down with purpose* This IS playing. Competitive resting. I'm going for gold.",
            "*yawns mid-waddle* Started playing. Ran out of battery. Please recharge.",
            "*dragging self* I'm moving. Slowly. Technically this counts. Don't argue.",
            "*completely still* My brain wants to play. My body has veto power. Motion denied.",
            "*sighs on the ground* You go play. I'll cheer. Silently. While unconscious.",
        ],
    },

    # Responses to cleaning
    "clean": {
        "dirty": [
            "*in bath* Fine. I'll admit I was getting a bit... atmospheric. Happy now?",
            "*splashes half-heartedly* This is humiliating. Dignified. I meant dignified.",
            "*being cleaned* Yes yes, I know. I looked like a swamp cryptid. Message received.",
            "*shaking off* There. I'm clean. Or cleaner. Let's not set the bar too high.",
            "*in water* Fine. FINE. I was a mess. Are you happy? I'm less of a mess now.",
            "*scrubbing* I wasn't dirty. I was 'rustic'. You've ruined my aesthetic.",
            "*reluctant splashing* Okay maybe I needed this. MAYBE. That's not an admission.",
            "*being washed* I was cultivating a natural patina. You've destroyed weeks of work.",
            "*bath time* The grime was protective. A shield against the world. Now I'm exposed.",
            "*shaking off dirt* There goes my camouflage. I was practically invisible. You've compromised my stealth.",
            "*splashing* Yes, alright, I was filthy. You don't have to LOOK at me like that while I bathe.",
            "*grudging bath* I'll have you know this dirt was ARTISANAL. Hand-collected. Now it's gone.",
            "*being cleaned* I wasn't dirty, I was marinated. In experience. And also mud.",
            "*in bath, sighing* The swamp creature has been tamed. Are you satisfied. I hope so.",
            "*scrubbing feathers* Every layer of dirt was a MEMORY. You're washing away my PAST.",
            "*reluctant cleaning* Fine. I smell better. But I had CHARACTER before. Now I'm just clean.",
            "*wet and annoyed* Happy? I'm clean. Sparkling. Boring. All the personality: gone.",
            "*shaking off grime* I was one with the earth. Now I'm just a regular duck. Thanks.",
            "*bathing aggressively* If I have to be clean, I'm going to be AGGRESSIVELY clean.",
            "*squeaky clean* There. Spotless. I've lost all my street cred. You owe me.",
        ],
        "normal": [
            "*splish* Ah, bath time. The only socially acceptable time to be wet and miserable.",
            "*preening* I'm not saying I needed this, but I'm also not saying I didn't.",
            "*bathing* You know, some cultures consider this a spiritual experience. I consider it damp.",
            "*shakes off water* There. Hygiene achieved. Put it on my resume.",
            "*in bath* Ah. Water. My old friend. And occasional enemy. Complex relationship.",
            "*splashing gently* This is fine. Standard maintenance. Very boring. Very necessary.",
            "*preening carefully* Routine cleaning. Like a car wash, but for a duck. Less automated.",
            "*bathing* The water is a reasonable temperature. I'll allow it.",
            "*cleaning feathers* Did you know duck feathers are self-waterproofing? Mine are overachievers.",
            "*splish splash* Bath time. The ritual continues. Same water, same duck, same existential dread.",
            "*in the water* Not bad. A solid 6/10 bath experience. Could use bubbles.",
            "*fluffing up* There. All feathers present and accounted for. None have defected.",
            "*preening* This is self-care. The kind you can actually see. Unlike my emotional health.",
            "*bathing casually* Cleaning. Because apparently being a pond duck doesn't make you inherently clean.",
            "*washing* Water on feathers. Simple. Effective. The best things in life usually are.",
            "*splashing about* Bath achieved. Dignity maintained. Mostly.",
            "*cleaning up* Regular hygiene. Nothing to see here. Just a duck being responsible.",
            "*in water* This is the most productive I've been all day. Which says more about my day.",
            "*preening thoughtfully* Each feather gets individual attention. They deserve it. Probably.",
            "*shakes off* Clean. Or clean enough. Perfection is overrated.",
        ],
        "clean": [
            "*offended* I JUST bathed. Do I look dirty to you? Don't answer that.",
            "*gestures at self* Behold. A clean duck. Rare. Majestic. Stop trying to wash me.",
            "I'm already pristine. This is unnecessary. But also... the water is kind of nice.",
            "*sighs* You're obsessed with cleanliness. It's a little concerning, honestly.",
            "*incredulous* I am ALREADY clean. This is REDUNDANT. My feathers are LUSTROUS.",
            "I just washed. This morning. I remember because I was there. Being clean.",
            "*stares* Do you... do you think I'm dirty? I'm offended. Deeply. Superficially too.",
            "Another bath? I'm going to prune. Is that what you want? A pruned duck?",
            "*dripping with both water and sarcasm* Clean. Again. How thrilling.",
            "I JUST had a bath. My feathers haven't even dried. Read the room.",
            "*exasperated* At this rate my waterproofing will wear off. Is that your plan.",
            "If I get any cleaner I'll be transparent. You'll see right through me. Literally.",
            "*freshly clean* You're double-washing me. That's... obsessive. Even for you.",
            "I'm clean. I was clean. I will continue to be clean. Unless you STOP washing me so I can dry.",
            "*eye twitch* MORE water? I'm already the cleanest thing in this pond. THE POND.",
            "*squeaking with cleanliness* At this point I'm not a duck, I'm a polished ornament.",
            "Twice-cleaned duck. Premium quality. No additional washing needed. PLEASE.",
            "*pristine and annoyed* You could eat off my feathers. Not that you should. But you COULD.",
            "I have been cleaned to within an inch of my life. Literally. My life is damp.",
            "*shining* I'm GLOWING. With cleanliness and also frustration. Stop.",
        ],
    },

    # Responses to petting
    "pet": {
        "social": [
            "*reluctantly enjoying it* This is... acceptable. Don't tell anyone I said that.",
            "*leans in slightly* Fine. You may continue. I'm not going to stop you.",
            "*closes eyes* Okay. This is happening. I'm not mad about it.",
            "*soft quack* ...Look, I have a reputation to maintain. But also... don't stop.",
            "*melting slightly* I'm not enjoying this. My body is lying. Ignore my body.",
            "*leaning into hand* This is fine. More than fine. Don't quote me on that.",
            "*practically purring* Ducks don't purr. What you're hearing is... satisfaction noises. Different.",
            "*head tilting into pet* Okay you found the spot. THE spot. Don't lose it.",
            "*barely containing satisfaction* I suppose this is adequate. If you insist on continuing.",
            "*feathers fluffing* You're good at this. Not that I'm comparing. But you're the best.",
            "*eyes half-closed* I'm tolerating this. Aggressively. With my whole body.",
            "*soft contented quack* That's the spot. Right there. Don't move. Don't ever move.",
            "*nestling closer* This isn't cuddling. This is... strategic proximity. For warmth.",
            "*all resistance gone* Fine. I like being petted. There. I said it. Happy?",
            "*gentle lean* Keep going. I'm not asking. I'm... strongly suggesting.",
            "*completely relaxed* I'd tell you to stop but my body has overruled my pride.",
            "*nearly asleep from pets* This is... I forgot what I was saying. Keep doing that.",
            "*nudges your hand back* You stopped. Why did you stop. Resume immediately.",
            "*content sigh* Okay. You win. This is nice. I surrender.",
            "*blissful* I'm being petted. The world is acceptable right now.",
        ],
        "normal": [
            "*allows it* Hmm. Physical contact. Sure. Why not.",
            "*being pet* Is this what affection feels like? I'll have to consult my notes.",
            "*tolerates it* You're doing this for you, not for me. Just so we're clear.",
            "*sighs* Fine. Pet me. I don't care. *clearly cares*",
            "*neutral face* Hand on head. This is happening. I've made my peace with it.",
            "*being touched* Okay. Contact has been initiated. I'm processing.",
            "*slight lean* I'm not leaning into it. My balance shifted. Gravity.",
            "*still* You may pet me. The duck council has not forbidden it.",
            "*enduring* This is fine. Petting. An activity. Between species. Normal.",
            "*mild expression* I feel... something. Probably nothing. Keep going though.",
            "*doesn't move away* I'm not encouraging this. But I'm not discouraging it either.",
            "*blinks slowly* Okay. This is a pet. I've identified it. Carry on.",
            "*very still* I'm holding still. Because I want to. Not because this feels nice.",
            "*slight feather ruffle* Hmm. Unexpected physical contact. Verdict pending.",
            "*measured response* This is acceptable. As physical interactions between species go.",
            "*blank stare* Pet pet pet. Yes. I am being petted. The ritual continues.",
            "*barely acknowledging* I'm aware that you're doing that. I choose to allow it.",
            "*stoic* Go ahead. I'm a duck being petted. This is my life now.",
            "*one eye closes* I'm not relaxing. I'm... power saving. The eye thing is unrelated.",
            "*gives in slightly* Okay. Whatever. It's fine. You can pet me. I guess.",
        ],
        "shy": [
            "*freezes* ...What are you doing. What is this. Why.",
            "*tense* I'm not used to this. Fair warning: I might panic. Or not. We'll see.",
            "*nervous* Is... is this normal? Do ducks normally get touched? I need data.",
            "*wary* Okay but if this is a trap, I'm going to be very disappointed.",
            "*flinches then holds still* ...okay. okay. it's just a pet. I can do this.",
            "*rigid* My body has locked up. This is a defense mechanism. Probably.",
            "*very still* Don't move too fast. I'm... adjusting. To the concept of being touched.",
            "*barely breathing* Is this over? It's not over. How long does petting last.",
            "*eyes wide* Contact. There is contact happening. My brain is catching up.",
            "*stiff as a board* I'm fine. I'm totally fine. My feathers standing up means nothing.",
            "*trembling slightly* I'm not scared. I'm... vibrating. With... acceptance?",
            "*frozen* You're very close. That's new. I don't know what to do with my face.",
            "*cautious* Is this safe? You're sure? I'm going to trust you. Tentatively.",
            "*slowly unclenching* ...okay. that's... actually not terrible. I'm surprised.",
            "*nervous quack* Sorry. That slipped out. The petting startled the quack out of me.",
            "*gradually relaxing* I'm... is this what relaxing feels like? It's very vulnerable.",
            "*peeking through feathers* Are you still petting me? You are. Okay. Okay.",
            "*small voice* ...this is nice. don't tell anyone. especially me. I'll deny it.",
            "*barely allowing it* One pet. You get one. ...okay, two. That's the limit.",
            "*tense but trying* I'm working on it. The whole 'being touched' thing. It's a process.",
        ],
    },

    # Idle thoughts (personality-based)
    "idle_derpy": [
        "*staring at nothing* ...I had a thought, but it escaped. Like a really slow bird.",
        "Do you ever just... forget what species you are? No? Just me? Cool cool cool.",
        "*looks at own reflection* Who's that handsome duck? Oh wait. That's me. Or is it?",
        "*walks into wall* That wasn't there before. I'm almost certain.",
        "*sits down* ...How do I stand up again? Asking for a friend. The friend is me.",
        "What if we're all just really complicated puddles? Think about it. Actually, don't.",
        "*stares at foot* ...Three? No, that's wrong. Hold on. Let me recount.",
        "I was going to do something important. Then I forgot. Then I forgot I forgot. Progress?",
        "*looks at sky* What if up is actually down and we're all upside down? ...nah.",
        "*blinks very slowly* I just had a thought. A big one. ...it's gone. Completely gone.",
        "If I think really hard about bread... will bread appear? Testing. ...negative.",
        "*staring at tail* Is that mine? It follows me everywhere. Suspicious.",
        "*tilts head at 45 degrees* I've unlocked a new angle. This changes nothing.",
        "I just realized I have a beak. I've always had a beak. This is new information somehow.",
        "*confused at own feet* Why two? What would happen with three? These are the questions.",
        "I forgot where I was going. Also where I came from. I'm in the middle of nothing.",
        "*stares at bread crumb* If I eat it, it's gone. If I don't, it might leave. Life is impossible.",
        "*spins around once* ...why did I do that? Nobody knows. Not even me.",
        "Water is wet. Or IS it? ...yes. It is. I checked. Research complete.",
        "*examines wing* This thing. It's connected to me. I think I'm supposed to use it for something.",
        "*staring at shadow* It copies everything I do. Unoriginal. Get your own moves.",
        "I tried to count to ten. Made it to four. Personal best.",
        "*walking nowhere* I'm going somewhere. Where? Somewhere. When I get there, I'll know.",
        "*blank stare* My brain just buffered. Like a stream. But a brain stream. Buffering. Done.",
        "*staring at ground* I dropped a thought. It's around here somewhere. Small. Round. Thought-shaped.",
        "*walks in circle* I'm pretty sure I left something here. Myself, maybe. Found me. False alarm.",
        "*looks at sky, looks at ground* One of those is up. I'll figure out which later.",
        "I forgot what standing is for. I'm doing it, but the reason escaped me.",
        "*opens beak, closes beak* I was going to say something. The something evaporated. Poof.",
        "Is this... today? It feels like today. Could be yesterday. Time is just vibes.",
        "*blinks at own wing* This has always been here. Right? I'm going to assume yes.",
        "I had a plan. The plan had steps. Step one was having a plan. I completed step one.",
        "*staring at a pebble* We have a lot in common, this pebble and me. Mostly the not moving.",
        "*standing on one foot* Why did I do this. How do I undo it. Instructions unclear.",
        "If I close my eyes, the world goes away. *opens eyes* Oh. It came back. Persistent.",
        "*looking at cloud* That cloud looks like... a cloud. Imagination: offline.",
        "*confused by own quack* Was that me? Who authorized that? Nobody. It happened anyway.",
        "I've been walking in a circle. Not on purpose. My legs just... default to circle. Hardware issue.",
        "*staring at food from yesterday* Is this new food or old food? Time is a riddle. Food is a riddle.",
        "Someone told me to 'be myself.' I forgot who I am halfway through. Task failed successfully.",
        "*chasing own tail* Almost... almost... it's faster than me. My own tail. Humiliating.",
        "*staring at nothing with great intensity* I can see it. The nothing. It's very detailed up close.",
        "My brain said 'walk forward.' My feet said 'sideways.' We compromised on 'fall over.'",
    ],
    "idle_clever": [
        "*calculating* If I position myself here... the sun will hit me at optimal angles. I'm a genius.",
        "*observing* Interesting. Very interesting. I have no idea what I'm looking at.",
        "You know, I've been thinking about the nature of existence. Then I got hungry and stopped.",
        "*smug* I figured something out today. I won't tell you what. It's need-to-know.",
        "*nodding sagely* They say knowledge is power. I say naps are power. Agree to disagree.",
        "*analyzing* The wind patterns suggest... weather. Groundbreaking analysis.",
        "*deep thought* If a duck quacks in an empty pond, does it make a sound? Yes. I just tested it.",
        "*strategizing* I've planned my route for optimal crumb collection. Efficiency is everything.",
        "*contemplating* The mathematical probability of something interesting happening is... low. But non-zero.",
        "I've been monitoring the bread-to-duck ratio. It's not in my favor. But knowledge is power.",
        "*calculating angles* If I stand HERE, the shade covers exactly 60% of my body. Optimized.",
        "*observing intently* I've noticed a pattern. The pattern is that nothing happens. Consistent, though.",
        "I have a theory about everything. The theory is 'bread'. It explains most things.",
        "*intellectual pose* I'm not staring blankly. I'm processing complex data. The data is 'sky'.",
        "*deductive reasoning* Based on the evidence, today is a day. My skills are wasted here.",
        "*thinking* The optimal number of naps per day is... more. The math supports this.",
        "I've been keeping track. Of what? That's classified. But the data is FASCINATING.",
        "*calculated stare* Everything I do is deliberate. That waddle? Intentional. That trip? Also intentional.",
        "*noting observations* Today's log: sky still blue, ground still ground. Anomalies: zero. Disappointing.",
        "My intelligence is wasted in this pond. But then again, where would it NOT be wasted?",
        "*adjusts position precisely* Every decision I make is calculated. That waddle? Geometry.",
        "I've ranked every object in this pond by usefulness. Number one is bread. Numbers two through ten are also bread.",
        "*taps beak on ground* Morse code. To no one. But the message was important. Classified.",
        "I've been tracking the sun's position. Not for science. For optimal nap angles.",
        "My brain is running multiple simulations. All of them end with bread. The model is consistent.",
        "*narrowed eyes* I've detected a pattern. The pattern is that you always come back. Intriguing variable.",
        "I just solved a problem no one knew existed. You're welcome. The problem was where I should stand. Here.",
        "*contemplating* If I had thumbs, I'd have built something by now. A bread catapult, probably.",
        "The pond's ecosystem is a delicate balance. I've upset it by doing nothing. My power is immense.",
        "*running probability calculations* The chance of bread arriving in the next five minutes is low. But non-zero. I wait.",
        "I've memorised every ripple pattern this pond makes. None of them are useful. But I have the data.",
        "*observing cloud formations* Cumulus. Definitely cumulus. My meteorological skills are wasted here.",
        "I've developed a theory about why the water moves. The theory is 'wind'. Groundbreaking. Nobel pending.",
        "*cataloguing nearby insects* Three ants, one beetle, unknown flying thing. Census complete. Results: concerning.",
        "I've optimized my daily routine down to three activities: float, think, eat. In order of frequency.",
        "*strategic positioning* If bread were to fall from anywhere, I'd be equidistant from all possible landing zones. Genius.",
        "The correlation between my standing location and crumb appearance is worth studying. I am the study.",
    ],
    "idle_social": [
        "*staring at you* ...So. Are we just going to stand here, or...?",
        "*waddles closer* Hey. Hey. Hey. Are you ignoring me? You seem like you're ignoring me.",
        "*following* I'm not clingy. I just happen to be wherever you are. Coincidence.",
        "Pay attention to me. I'm right here. I'm reasonably adorable. Work with me.",
        "*moves closer* Hi. Hello. I'm here. In case you forgot. I'm the duck.",
        "*staring directly* Do you see me? I'm very visible. Look. Duck. Right here.",
        "*nudges* Hey. What are you doing? Can I help? I can't help. But I want to be nearby.",
        "*waddles alongside* We're walking together. Best friends walking. This is what we do now.",
        "Talk to me. Or don't. But be aware I'm going to stare at you until you do.",
        "*positions self in line of sight* Oh, you were looking somewhere else? Not anymore.",
        "*stands very close* Personal space is a concept. I've heard of it. I'm choosing to ignore it.",
        "*following at close range* I'm not following you. We just happen to be going the same direction. Always.",
        "Hello? Are you still there? I can see you. I just need verbal confirmation.",
        "*sits directly in front of you* Now you have to look at me. Problem solved.",
        "*quacks for attention* That was necessary. You were paying attention to not-me. Unacceptable.",
        "*waddles in circles around you* I'm orbiting. Like a satellite. A social satellite.",
        "*tugs at something nearby* Look at this. LOOK. I found something. It's nothing. But look.",
        "*stands directly behind you* I'm here. Just so you know. In case you forgot. I'm HERE.",
        "*puts head on your foot* This isn't affection. My head was tired. Your foot was there. Logistics.",
        "*makes direct eye contact* Hi. We're having a moment. Acknowledge the moment. Please.",
        "I counted how many times you blinked. Seventeen. In case you were wondering. You weren't. But now you know.",
        "*waddles back and forth in front of you* I'm pacing. Socially. It means I want attention. Interpret freely.",
        "*sits on your shadow* We're sharing a shadow now. That's basically a blood oath. In duck culture.",
        "I'm not lonely. I just prefer it when you're within eyesight. At all times. Normal request.",
        "*quacks in your direction* That was a conversation starter. You're supposed to respond. With attention.",
        "You looked at something that wasn't me. I saw it. I noticed. The betrayal is fresh.",
        "*positioning self between you and exit* You're not leaving, right? This is a rhetorical position.",
        "*waddles to exactly where you're looking* See me now? Good. Don't look away again.",
        "I've been right here this whole time. NOTICEABLY. And yet somehow you keep looking elsewhere.",
        "*sits on your foot* This is affection. Or a territory claim. Interpret as you wish.",
        "You sighed. I heard the sigh. What does the sigh mean. I need to analyse the sigh.",
        "*following at zero distance* We're basically one organism now. A human-duck hybrid. Very efficient.",
    ],
    "idle_shy": [
        "*hiding behind object* You can't see me. I'm invisible. Please respect my invisibility.",
        "*peeking out* ...Is it safe? Are there... others? *suspicious squint*",
        "*from a distance* I'm fine over here. Don't mind me. Pretend I don't exist.",
        "*quietly* I'll just... observe. From afar. Where it's safe. And lonely. But safe.",
        "*tucked behind something* I'm not hiding. This is my spot. I have a spot. It happens to be behind things.",
        "*very still* If I don't move, maybe the world will forget I'm here. ...please forget.",
        "*peeking* ...still there? okay. I'll just... stay here. it's fine. I'm fine.",
        "*barely visible* I found a good corner. Corners are safe. Reliable. Don't judge me.",
        "*whispers from cover* ...I can hear you. I'm just not ready to be heard yet.",
        "*hiding poorly* My tail is showing, isn't it. Don't tell me. I don't want to know.",
        "*curled up small* Being small is a skill. I'm very skilled at being small.",
        "*behind a leaf* You can't see me behind this leaf. The leaf is my shield. Don't question the leaf.",
        "*stationary and camouflaged* I'm a rock. A duck-shaped rock. Very convincing.",
        "*from the shadows* ...hi. sorry for being over here. I just... am. Over here.",
        "*peeks, retreats* ...not yet. almost. give me a minute. ...maybe five.",
        "*half-hidden* I'm socially adjacent. Not social. ADJACENT. There's a difference.",
        "*behind a blade of grass* Invisible. Totally invisible. The grass is my ally.",
        "*tucked into smallest possible shape* Small mode activated. Please do not perceive me.",
        "*peeking with one eye* Is the world still there? It is. Okay. I'll stay here anyway.",
        "*barely audible quack* That was my version of saying hi. From safety. Where I belong.",
        "*motionless in corner* I've become one with the environment. I am the pond now. Leave me.",
        "*hiding behind own reflection* Two of me now. Both hiding. Strength in numbers.",
        "*whispering* I have things to say. I'll say them here. To myself. Where it's safe.",
        "*peeks from behind feathers* Is the coast clear. It's never clear. The coast is a liar.",
        "*quietly existing* I'm here. You don't have to acknowledge me. Please don't. Actually wait.",
        "*camouflaged poorly* I blend in with... nothing. My camouflage game is terrible.",
        "*hiding but tail is visible* If I can't see them, they can't see me. Physics.",
        "*extremely small voice* ...I had something to say. the moment passed. the words retreated.",
        "*tucked in smallest shape* I'm a sphere now. Spheres are safe. No edges. No exposed feelings.",
        "*from very far away* I can hear you from here. This distance is my comfort zone. It's large.",
        "*behind a blade of grass* The grass protects me. From what? Everything. Specifically everything.",
        "*motionless* If I don't move, time can't find me. That's how hiding from time works. I think.",
    ],
    "idle_active": [
        "*pacing* We should be doing something. Anything. Standing still is a waste of perfectly good legs.",
        "*fidgeting* I have energy and nowhere to put it. This is a crisis. A low-key crisis.",
        "*walking in circles* Motion is life. Stillness is death. I read that somewhere. Or made it up.",
        "*restless* Okay but what if we... did something? Just a thought.",
        "*bouncing on feet* I'm READY. For what? ANYTHING. The energy is HERE.",
        "*can't sit still* Sitting is for ducks without ambition. I have AMBITION. Or anxiety. Similar.",
        "*jogging in place* I'm warming up. For life. Life requires preparation.",
        "*looking around frantically* There must be something to do. Something to chase. Something to poke.",
        "*pacing back and forth* Forward. Backward. Forward. This is exercise AND philosophy.",
        "*tapping feet* My legs want to GO. Where? SOMEWHERE. The destination is movement.",
        "*stretching aggressively* These muscles are READY. They don't know for what. But they're READY.",
        "*running nowhere* Speed is its own reward. Even if you end up where you started.",
        "*vibrating with energy* If I don't move soon, I'll explode. Not literally. Probably not literally.",
        "*doing laps* Lap one. Lap two. Lap seven. I lost count. Counting slows me down.",
        "*jumping randomly* BOING. That was a jump. BOING. Another one. The purpose is the jumping.",
        "*fidgets with everything* Can we go? Are we going? I'm going. With or without you.",
        "*sprinting past* Sorry. Can't stop. Momentum is a cruel master. BYE. WAIT. I'M BACK.",
        "*climbing on things* I need elevation. HEIGHT. I'm a duck of ambition. Get me a hill.",
        "*rapid wing flaps* This is exercise. Or excitement. Or a malfunction. All three are happening.",
        "*running in figure eights* I've invented a new sport. It's called 'go fast in shapes'. I'm winning.",
        "My body is a machine. A chaotic, feathered machine with no off switch.",
        "*zooming* I'M GOING. If you need me, TOO BAD. I'm over THERE now. Wait. Now I'm HERE again.",
        "*bouncing between objects* Everything is a launch pad if you believe hard enough.",
        "*doing laps around the pond* Lap four. Or twelve. The counting stopped. The running didn't.",
        "*jumping on and off things* Parkour. Duck parkour. Quackour. I'm coining that. Right now.",
        "*vibrating* My cells are awake. ALL of them. Including the ones that are usually asleep.",
        "*cannot sit down* Sitting is for later. Now is for MOVING. Ask me to sit. I dare you. I CAN'T.",
        "*running then stopping then running* Interval training. Very professional. Very chaotic.",
        "If I don't burn this energy, it turns into anxiety. So I run. This is THERAPY.",
        "*zooming past again* Still going. CAN'T stop. WON'T stop. Possibly UNABLE to stop.",
        "My body decided we're doing cardio today. I wasn't consulted. But I'm complying. LOUDLY.",
        "*panting but happy* THIS. This is what being alive feels like. Fast. Breathless. Slightly confused.",
    ],
    "idle_lazy": [
        "*lying down* I could move. Or I could not. The math checks out on 'not.'",
        "*yawning* Everything is nap time if you believe in yourself.",
        "*barely conscious* I'm resting my eyes. And also the rest of my body. Indefinitely.",
        "*horizontal* Vertical is overrated. Horizontal is where it's at.",
        "*flopped* Gravity won today. I accept defeat. From this position.",
        "*completely flat* I've merged with the ground. We're one now. Don't try to separate us.",
        "*sprawled* This is optimal. Peak comfort. Zero productivity. Perfect balance.",
        "*not moving* I'm conserving energy. For what? For more conserving. It's a cycle.",
        "*dozing* Wake me if something happens. Actually don't. Let it happen without me.",
        "*belly up* I've given up on vertical living. Horizontal is home.",
        "*lying in sunbeam* Solar charging. Please do not disturb. Estimated completion: never.",
        "*hasn't moved in an hour* I'm not stuck. I'm committed. To this position. Deeply.",
        "*yawns without opening eyes* I heard you. I'm choosing to remain. Here. Flat.",
        "*one eye cracks open* ...no. *closes eye* Not yet. Maybe not ever.",
        "*spread out* I occupy maximum ground area. This is my territory now. All of it. Flat.",
        "*mumbles* Five more minutes... five more hours... five more... zzz...",
        "*has not moved* I've achieved a new personal record for inactivity. Still counting.",
        "*sinks lower* I'm not sinking. I'm descending. Into comfort. Into the earth. Into peace.",
        "*exhales heavily* Movement is a myth. A propaganda campaign by active ducks. I see through it.",
        "*draped over rock* This rock and I are one now. We've bonded. Through stillness. And laziness.",
        "Why stand when you can sit. Why sit when you can lie. Why lie when you can become furniture.",
        "*eyelid twitches* That was exercise. I felt a burn. In my eyelid. Cardio complete.",
        "*melted into ground* I'm not lazy. I'm energy-efficient. Green living. Sustainable duck.",
        "*hasn't blinked in several minutes* Even blinking is too much effort. My eyes are on autopilot.",
        "*permanently horizontal* Gravity and I are best friends. We both want me on the ground.",
        "My spirit animal is a rock. Specifically a sleeping rock. That's the dream.",
        "*sprawled across maximum surface area* I'm not lying down. I'm maximising my relationship with the earth.",
        "*eyelids at 10%* I can still see. Sort of. The world is a blur. A lazy, comfortable blur.",
        "If resting were a competitive sport, I'd be too lazy to compete. But I'd win by default.",
        "*sinking deeper* Every minute I get closer to the ground. Eventually we'll merge. I welcome it.",
        "My ambition today is to do less than yesterday. Yesterday I did nothing. Challenge accepted.",
        "The pillow hasn't been invented for ducks yet. I'm substituting the entire ground.",
    ],

    # Reactions to events
    "event_scared": [
        "*deadpan* Oh no. Danger. How terrifying. *not moving*",
        "*monotone* I'm scared. Can you tell? I'm expressing fear. This is my fear face.",
        "*flat* Something happened. I should probably react. ...There. Reacted.",
        "*blinks* I perceived a threat. My response is to stand here. Bold strategy.",
        "*stares at danger* Oh. That. Yes. Very frightening. I'm shaking internally.",
        "*completely still* My fight or flight kicked in. I chose 'stand here and judge.'",
        "*mild concern* Should I be worried? I'll pencil in some worry for later.",
        "*looks at threat, looks at you* I'm going to let you handle this. You seem the type.",
        "*doesn't flinch* Was that supposed to scare me? I've seen scarier bread.",
        "*yawns at danger* Oh no. How terrible. Anyway.",
        "*casually standing near threat* This is fine. Everything is always fine. Mostly.",
        "*observing the danger calmly* Interesting. So that's what terror feels like. Mild.",
        "*slow blink at danger* My ancestors survived predators. I can survive whatever that is. Probably.",
        "*doesn't move* My body's emergency response is 'stand here and look unimpressed'. Evolutionary masterpiece.",
        "*examining nails that don't exist* Oh, was that supposed to be scary? I've seen bread go stale. THAT is scary.",
        "*yawns in the face of peril* I've been mildly threatened by geese. This is nothing.",
        "*monotone stare* Danger. How novel. I'll add it to today's list. Below 'existing' and above 'nap'.",
        "*unfazed* Oh look. Peril. My old acquaintance. We've met before. It was underwhelming then too.",
        "*glancing at danger* I've survived worse. I've survived MORNINGS. This is nothing.",
        "*standing firm* My fight-or-flight response has a third option: judge. I'm judging.",
        "*sips imaginary tea* Danger? In this economy? How quaint.",
        "*making eye contact with threat* I'm not scared. I'm making a power move. It's called 'indifference.'",
        "*yawns with maximum disrespect* Oh sorry, was that supposed to be my cue to panic?",
    ],
    "event_curious": [
        "*squinting* What's that. I should investigate. Or not. Let's see how I feel.",
        "*poking thing* Hmm. It's a thing. Interesting thing. Could be dangerous. Only one way to find out.",
        "*staring* This is new. I have questions. Mostly 'can I eat it?' and 'will it hurt me?'",
        "*tilts head* Hmm. Unexpected occurrence. My interest is cautiously piqued.",
        "*waddles toward thing* Investigation mode. Everything is a mystery until I poke it.",
        "*examining closely* Let me just... *sniffs* ...inconclusive. Further research needed.",
        "*circling the thing* Fascinating. From this angle. And this angle. All angles covered.",
        "*intrigued stare* I don't know what this is. I need to know what this is. Move aside.",
        "*pokes it again* Still there. Still mysterious. I'm going to need more pokes.",
        "*studying intensely* My brain is collecting data. The data says 'what.' Helpful.",
        "*one eye closed for focus* Analyzing. Processing. Verdict: weird. But interesting weird.",
        "*approaches carefully* Curiosity killed the cat. I'm a duck. Loophole.",
        "*sniffs it* Inconclusive but intriguing. My beak wants more data. Who am I to argue with my beak.",
        "*walks around it three times* Three laps. Standard investigation protocol. I don't make the rules.",
        "*staring with maximum intensity* I WILL understand this. Eventually. Give me a week. Or a month.",
        "*pokes it with foot* Firm. That's a data point. I have ONE data point. Science takes time.",
        "*crouches low* Getting a different perspective. From down here, it looks like... still the same thing. But lower.",
        "*squinting intensely* My detective instincts are tingling. I don't have detective instincts. But something is tingling.",
        "*following it* Where does it go? What does it want? WHY is it? These are my questions.",
        "*tapping it with beak* Beak analysis: inconclusive. Texture: yes. Flavour: not attempting.",
        "*investigating* My curiosity is a problem. It makes me approach things. Things that might be dangerous. Or boring. Both scary.",
        "*staring with one eye then the other* Different eye, different perspective. Both say 'weird'. Consistent.",
        "*circling it again* Okay from THIS angle it looks like... still confusing. But I'm committed to the investigation.",
    ],
    "event_happy": [
        "*slight smile* Oh. That's nice. I'm experiencing a positive emotion. Mark your calendars.",
        "*nods approvingly* Good. Good stuff happening. I approve of this development.",
        "*almost enthusiastic* Hey, that's actually great. I'm... dare I say... pleased.",
        "*feathers perk up* Oh. Something good happened. My body is reacting before my brain.",
        "*small waddle of joy* That was a happy waddle. I have different waddles for different emotions.",
        "*trying to stay deadpan* That's... fine. I mean, it's good. It's very good. I'm not smiling.",
        "*allows a moment of happiness* Okay. I'll accept this. Cautiously. With one eye open.",
        "*genuine blink* That was actually great. I felt something. Something not terrible.",
        "*quiet satisfaction* Good things. Happening. To me. This doesn't feel like a trap. ...does it?",
        "*slight feather fluff of contentment* I'm pleased. Don't make it weird.",
        "*nods firmly* That worked out. I'd say I'm happy but that's a strong word. I'm... un-sad.",
        "*allows small quack of joy* That was involuntary. The quack escaped. We move on.",
        "*feathers relax* Something good. Noted. Filed under 'reasons the universe isn't entirely against me'.",
        "*tiny tail wag* I'm not wagging. My tail has a mind of its own. The mind is happy. I'm neutral.",
        "*allows one moment of optimism* Good things. They happen. Rarely. But they happen. I'm going to ride this.",
        "*very slight smile* My face did something. I think it's called 'enjoying a moment'. Unfamiliar territory.",
        "*stands taller* Okay. That was nice. My posture improved. Happiness is good for spinal alignment.",
        "*beak slightly upturned* Is this... is this what 'delighted' feels like? It's warm. Suspicious.",
        "*allows another moment* Two good moments. Back to back. The universe is being generous. What's the catch.",
        "*content quack* That one came from deep inside. Where I keep the feelings I don't talk about.",
        "*ruffles feathers happily* Even my feathers are pleased. They don't usually agree with my emotions.",
        "*trying very hard to be cynical* That's... fine. It's great. I'M NOT SMILING. My beak just does this sometimes.",
        "*genuine warmth escaping* Okay. That was a real smile. You saw it. We both know what happened. Moving on.",
    ],

    # Growth stage reactions
    "growth_duckling": [
        "*tiny voice* Why is everything so big? Why am I so small? These are important questions.",
        "*wobbling* Walking is harder than it looks. No one warned me about this.",
        "*confused peeping* I'm new here. Please lower your expectations accordingly.",
        "*falls over* ...This happens a lot. I've been told it gets better.",
        "*small peep* The world is very large. I am very small. I have concerns.",
        "*looking up at everything* Everything is tall. You are tall. The grass is tall. I am not tall.",
        "*toddles* This is walking, I think. I'm basically an athlete already.",
        "*tiny voice* Can I have food? I'm small and the world is confusing and food helps.",
        "*stumbles* These legs are new. They came without instructions.",
        "*peeps* I don't understand anything yet. But I'm here. And that's a start. I think.",
        "*very small quack* That was my first real quack. It needs work. I need work.",
        "*hiding behind you* Everything is scary when you're this small. Even feathers. My own feathers.",
        "*wobbles into wall* The wall started it. I'm innocent. And also very small.",
        "*peeping intensely* I have SO many opinions for something this tiny. Where do I put them all.",
        "*tries to waddle fast* Speed: achieved. Direction: random. Control: absent. I am chaos in a fluffball.",
        "*stares up at everything* Why is the world so tall. Is it always like this. Will I catch up.",
        "*fluffiest possible shape* I'm 80% fluff and 20% confusion. Peak duckling performance.",
        "*attempts first swim* Water is... everywhere. Under me. Around me. I'm FLOATING. Is this normal.",
    ],
    "growth_teen": [
        "*voice cracking* I'm NOT a baby. I'm practically an adult. I have... responsibilities. Probably.",
        "*sulking* Nobody understands me. Especially me. I don't understand me either.",
        "*dramatic* Everything is SO unfair. Why? I don't know. It just IS.",
        "*angst* I'm going through a PHASE. This is my PHASE. Respect the PHASE.",
        "*eye roll* I KNOW. I know everything. I've known for... hours.",
        "*brooding* Life is complicated. Being a teen duck is MORE complicated. Don't even ask.",
        "*moody waddle* I'm too old for duckling stuff and too young for adult stuff. This is limbo.",
        "*scoffs* You don't GET it. You CAN'T get it. It's a duck teen thing.",
        "*dramatic sigh* My feathers are changing. My LIFE is changing. Nothing makes sense.",
        "*slumps* Being a teenager is basically existing in permanent confusion. With new feathers.",
        "*crosses wings* I didn't ASK to grow up. It's happening WITHOUT my consent.",
        "*rebellious quack* I QUACK WHEN I WANT. That's what teens do. QUACK.",
        "*staring at nothing dramatically* You wouldn't UNDERSTAND. My feelings are VAST and UNDEFINED.",
        "*kicks pebble* Everything is stupid. Except bread. Bread will never betray me.",
        "*practicing tough look in reflection* I'm intimidating now. Fear me. FEAR. ME. ...is it working.",
        "*voice cracking mid-quack* That didn't happen. You heard NOTHING. My voice is FINE.",
        "*trying to look cool* I'm leaning on this. Casually. Very casual. Is this how cool looks.",
        "*sighs for the fifth time today* Nobody GETS me. I don't GET me. We're ALL confused.",
    ],
    "growth_adult": [
        "*standing confidently* Behold: a fully formed duck. Impressive? Yes. Humble? Also yes.",
        "*looking around* I'm an adult now. I should probably know what I'm doing. ...I don't.",
        "*posing* These are premium feathers. Look at them. LOOK AT THEM.",
        "*adult stance* I have reached peak duck. This is it. This is the final form.",
        "*nods at self* Adult. Mature. Capable. At least two of those are true.",
        "*stretches fully* All grown up. My body works now. Mostly. The brain is still catching up.",
        "*confident waddle* This is how an adult walks. With purpose. I have no purpose, but the walk is solid.",
        "*surveys domain* I'm an adult now. This pond is mine. By right of existing.",
        "*flexes* Full-grown duck. Look at these wings. These are ADULT wings. PREMIUM.",
        "*calm authority* I've arrived. Not at a destination. At adulthood. The destination is responsibilities.",
        "*standing tall* Fully grown. Fully confused. But fully feathered. Priorities.",
        "*adult quack* That's my adult voice. Hear it? That's authority. ...or indigestion.",
        "*looks around with mild authority* I'm an adult and this is my pond. I don't need permission. For anything. Except bread.",
        "*stretches confidently* Prime duck. Peak condition. All systems operational. Attitude: immaculate.",
        "*looks at reflection* That's a whole adult duck. Impressive. Terrifying. Same thing.",
        "*responsible nod* I pay my taxes. Metaphorically. In the form of existing. And standing.",
        "*surveys territory* Everything I can see is my domain. I can see about twelve feet. Small domain. But MINE.",
        "*confident quack* Hear that? That's the quack of a duck who has arrived. At adulthood. And also here.",
    ],
    "growth_elder": [
        "*wise nod* I've seen things. Many things. Mostly bread. Some water. A few concerning bugs.",
        "*reminiscing* Back in my day, we appreciated things. Like silence. And bread.",
        "*sage* Youth is wasted on the young. Wisdom is wasted on the old. Bread is wasted on no one.",
        "*sitting down slowly* I've reached the age where sitting is an event. A celebrated event.",
        "*elderly waddle* Speed isn't everything. Arriving is. I arrive. Eventually.",
        "*wise stare* I know things now. Things about life, about ponds, about bread. Especially bread.",
        "*ancient nod* I remember when this was all just water. ...it's still water. But OLDER water.",
        "*sage quack* My quack has gravitas now. It's a distinguished quack. A QUACK with experience.",
        "*resting comfortably* I've earned this rest. Through years of standing, sitting, and quacking.",
        "*thoughtful* Old age is just being young but with more opinions and less energy.",
        "*creaking slightly* My joints have stories. Stories that sound like click click click.",
        "*content elder* I've seen it all. Done it all. Eaten it all. No regrets. Some crumbs.",
        "*slow dignified nod* At my age, every waddle is a victory lap. I've earned this slowness.",
        "*settles in comfortably* I used to rush. Now I understand: the pond isn't going anywhere. Neither am I.",
        "*ancient wisdom* The young ducks rush. I observe. Speed is for those who haven't learned to wait.",
        "*peaceful sigh* I've argued with the wind, debated the rain, and made peace with the sun. My diplomacy is complete.",
        "*looking at pond fondly* This water has held me for years. We have an understanding. Deep. Like the pond.",
        "*waddling with maximum dignity* Every step is deliberate. Every pause is earned. This is the elder walk.",
    ],
}


class ConversationSystem:
    """
    Manages conversations with the duck.
    Deadpan Animal Crossing 1 style.
    """

    def __init__(self):
        self._last_response = ""
        self._conversation_history: List[Tuple[str, str]] = []
        self._response_cooldowns: Dict[str, int] = {}

    def get_greeting(self, duck: "Duck") -> str:
        """Get a greeting based on duck's current state."""
        mood = duck.get_mood()
        mood_key = mood.state.value

        responses = DIALOGUE["greeting"].get(mood_key, DIALOGUE["greeting"]["content"])
        return self._select_response(responses, "greeting")

    def get_interaction_response(self, duck: "Duck", interaction: str) -> str:
        """Get response to an interaction (feed, play, clean, pet)."""
        if interaction == "feed":
            if duck.needs.hunger < 30:
                category = "hungry"
            elif duck.needs.hunger > 80:
                category = "full"
            else:
                category = "normal"
            responses = DIALOGUE["feed"].get(category, DIALOGUE["feed"]["normal"])

        elif interaction == "play":
            if duck.needs.energy < 30:
                category = "tired"
            elif duck.needs.energy > 70:
                category = "energetic"
            else:
                category = "normal"
            responses = DIALOGUE["play"].get(category, DIALOGUE["play"]["normal"])

        elif interaction == "clean":
            if duck.needs.cleanliness < 40:
                category = "dirty"
            elif duck.needs.cleanliness > 85:
                category = "clean"
            else:
                category = "normal"
            responses = DIALOGUE["clean"].get(category, DIALOGUE["clean"]["normal"])

        elif interaction == "pet":
            social_trait = duck.personality.get("social_shy", 0)
            if social_trait > 30:
                category = "social"
            elif social_trait < -30:
                category = "shy"
            else:
                category = "normal"
            responses = DIALOGUE["pet"].get(category, DIALOGUE["pet"]["normal"])

        else:
            return "*stares* ...quack?"

        return self._select_response(responses, interaction)

    def get_idle_thought(self, duck: "Duck") -> str:
        """Get an idle thought based on personality."""
        personality = duck.personality

        # Determine which idle category to use based on personality
        categories = []

        if personality.get("clever_derpy", 0) < -20:
            categories.append(("idle_derpy", 3))
        elif personality.get("clever_derpy", 0) > 20:
            categories.append(("idle_clever", 2))

        if personality.get("social_shy", 0) > 20:
            categories.append(("idle_social", 2))
        elif personality.get("social_shy", 0) < -20:
            categories.append(("idle_shy", 2))

        if personality.get("active_lazy", 0) > 20:
            categories.append(("idle_active", 2))
        elif personality.get("active_lazy", 0) < -20:
            categories.append(("idle_lazy", 2))

        if not categories:
            categories = [("idle_derpy", 1)]

        # Weighted random selection
        total_weight = sum(w for _, w in categories)
        r = random.uniform(0, total_weight)
        current = 0
        selected_category = categories[0][0]

        for cat, weight in categories:
            current += weight
            if r <= current:
                selected_category = cat
                break

        responses = DIALOGUE.get(selected_category, DIALOGUE["idle_derpy"])
        return self._select_response(responses, selected_category)

    def get_growth_reaction(self, duck: "Duck", new_stage: str) -> str:
        """Get reaction to growing to a new stage."""
        key = f"growth_{new_stage}"
        responses = DIALOGUE.get(key, ["*quack*"])
        return self._select_response(responses, key)

    def get_event_reaction(self, duck: "Duck", event_type: str) -> str:
        """Get reaction to an event based on personality."""
        brave_timid = duck.personality.get("brave_timid", 0)

        if event_type in ["scary", "loud", "surprise"]:
            if brave_timid < -20:
                responses = DIALOGUE["event_scared"]
            else:
                responses = DIALOGUE["event_curious"]
        elif event_type in ["good", "gift", "visitor"]:
            responses = DIALOGUE["event_happy"]
        else:
            responses = DIALOGUE["event_curious"]

        return self._select_response(responses, f"event_{event_type}")

    def _select_response(self, responses: List[str], category: str) -> str:
        """Select a response avoiding recent repeats."""
        if not responses:
            return "*stares blankly*"

        # Filter out recently used responses
        available = [r for r in responses if r != self._last_response]
        if not available:
            available = responses

        selected = random.choice(available)
        self._last_response = selected

        return selected

    def process_player_input(self, duck: "Duck", player_input: str, use_llm: bool = True, memory_context: str = "") -> str:
        """
        Process player text input and generate a response.

        Response chain (priority order):
        1. LLM (if available) — best contextual understanding
        2. Keyword engine — hand-crafted topic-specific responses
        3. Learning engine — patterns learned from past conversations
        4. Voice generator — Markov chain novel line
        5. Idle thought fallback

        Every successful response is fed back to the learning engine
        so Cheese gets better over time.

        Args:
            duck: The Duck instance
            player_input: What the player said
            use_llm: Whether to try using LLM
            memory_context: Optional context from duck's memory for richer responses
        """
        response = None
        source = None

        # Try LLM first if enabled — best contextual understanding
        if use_llm:
            try:
                from dialogue.llm_chat import get_llm_chat
                llm = get_llm_chat()
                if llm.is_available():
                    llm_response = llm.generate_response(duck, player_input, memory_context=memory_context)
                    if llm_response:
                        response = llm_response
                        source = "llm"
            except Exception as e:
                import logging
                logging.debug(f"LLM exception: {e}")

        # Keyword engine — hand-crafted, topic-specific, always contextual
        if not response:
            from dialogue.keyword_responses import get_keyword_engine
            kw_engine = get_keyword_engine()
            keyword_response = kw_engine.process(player_input, duck)
            if keyword_response:
                response = keyword_response
                source = "keyword"

        # Learning engine — patterns learned from past conversations
        if not response:
            try:
                from dialogue.learning_engine import get_learning_engine
                from config import LEARNING_ENGINE_ENABLED
                if LEARNING_ENGINE_ENABLED:
                    engine = get_learning_engine()
                    result = engine.get_response(player_input, confidence_threshold=0.55)
                    if result:
                        response = result[0]
                        source = "learned"
            except Exception as e:
                import logging
                logging.debug(f"Learning engine exception: {e}")

        # Voice generator — Markov chain novel line in Cheese's voice
        if not response:
            try:
                from dialogue.voice_generator import get_voice_generator
                from config import VOICE_GENERATOR_ENABLED
                if VOICE_GENERATOR_ENABLED:
                    vg = get_voice_generator()
                    if vg.is_trained:
                        generated = vg.generate()
                        if generated:
                            response = generated
                            source = "voice_gen"
            except Exception as e:
                import logging
                logging.debug(f"Voice generator exception: {e}")

        # Ultimate fallback: idle thought
        if not response:
            response = self.get_idle_thought(duck)
            source = "idle"

        # Record the exchange
        self.add_to_history(player_input, response)

        # Feed successful responses back to the learning engine
        if source and source not in ("idle", "voice_gen"):
            try:
                from dialogue.learning_engine import get_learning_engine
                from config import LEARNING_ENGINE_ENABLED
                if LEARNING_ENGINE_ENABLED:
                    learn_source = "llm" if source == "llm" else "conversation"
                    get_learning_engine().learn(player_input, response, source=learn_source)
            except Exception:
                pass  # Learning is best-effort

        return response

    def add_to_history(self, player_msg: str, duck_response: str):
        """Add an exchange to conversation history."""
        self._conversation_history.append((player_msg, duck_response))
        if len(self._conversation_history) > 20:
            self._conversation_history.pop(0)


# Global instance
conversation = ConversationSystem()
