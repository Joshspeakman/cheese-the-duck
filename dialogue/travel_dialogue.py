"""
Travel dialogue - departure lines, breadcrumb reactions, obscured chat,
return lines, and friend invitation dialogue for autonomous biome travel.
"""
import random
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# DEPARTURE LINES — organized by travel motivation
# Placeholders: {destination}, {current_weather}, {dest_weather}, {friend}
# ═══════════════════════════════════════════════════════════════════════════

DEPARTURE_WEATHER_ESCAPE = [
    "*looks up at sky* It's {current_weather} here. I don't DO {current_weather}. "
    "{destination} has {dest_weather}. Executive decision.",
    "*shakes water off feathers* This {current_weather} is personally offensive. "
    "I'm going to {destination} where the weather respects me.",
    "*squints at clouds* No. Absolutely not. {destination} it is. "
    "They have {dest_weather}. Like CIVILIZED biomes.",
    "*preens aggressively* My feathers were NOT designed for {current_weather}. "
    "I'm relocating to {destination}. Effective immediately.",
    "*wraps wings around self* This is miserable. {destination} is {dest_weather}. "
    "I deserve {dest_weather}. Goodbye.",
    "*dramatic shiver* I refuse to endure this {current_weather} for one more SECOND. "
    "{destination}. NOW.",
    "*stares at the sky with betrayal* The weather has chosen violence. "
    "I'm choosing {destination}. It's {dest_weather} there. Allegedly.",
    "*gestures at sky* THIS? No. {destination} has {dest_weather}. "
    "I'm going where the atmosphere COOPERATES.",
    "*fluffs feathers indignantly* I am a DELICATE creature. "
    "This {current_weather} is beneath me. {destination} awaits.",
    "*sneezes* That's it. Final straw. {destination} has {dest_weather} "
    "and that's where I'll be. Don't wait up.",
    "*wringing out feathers* You know what has BETTER weather than this? "
    "Literally {destination}. See you there. Or don't.",
    "*puts foot down with great drama* I have STANDARDS. "
    "And those standards include not standing in {current_weather}. "
    "{destination} it is.",
    "*looks at you, then at sky, then at you* I'm going to {destination}. "
    "It's {dest_weather}. You can come or you can be wrong. Your call.",
    "*deadpan stare at clouds* This weather and I have creative differences. "
    "I'm taking my talents to {destination}.",
    "*shakes head slowly* Every minute here in this {current_weather} "
    "is a minute I could spend in {destination}'s {dest_weather}. Math.",
]

DEPARTURE_WEATHER_ENJOY = [
    "*eyes widen* I heard {destination} has {dest_weather} right now. "
    "I'm not MISSING that. I've waited my WHOLE LIFE. Which is {age} days.",
    "*vibrating with excitement* {dest_weather}?! At {destination}?! "
    "I need to SEE this. It might never happen again. ...probably will though.",
    "*perks up* Did the wind just tell me about {dest_weather} at {destination}? "
    "Yes. The wind tells me things. We're close.",
    "*gasp* They have {dest_weather}. AT {destination}. This is NOT a drill. "
    "I repeat: NOT. A. DRILL.",
    "*runs in circles* {dest_weather}!! {destination}!! "
    "This is the greatest day of my life. Again. I say that a lot.",
    "*stares into distance* The {dest_weather} at {destination} is calling me. "
    "Like a siren. But for ducks. A duck siren. A quackren.",
    "*bouncing* You don't understand. {dest_weather} at {destination} "
    "is a once-in-a-lifetime thing. This lifetime. Today. NOW.",
    "*packs imaginary bag at speed* {dest_weather}. {destination}. Going. "
    "Questions later. Adventures now.",
]

DEPARTURE_BOREDOM = [
    "*counts blades of grass* ...four thousand and seven. Four thousand and eight. "
    "Right. I've memorized this biome. {destination} has different grass.",
    "*yawns so wide an echo comes back* I have explored every INCH of here. "
    "{destination} has unexplored inches. I NEED those inches.",
    "*lying flat* This place is... fine. It's FINE. But {destination} "
    "exists and I haven't been there in a while. Motion filed.",
    "*stares at nothing* I've achieved everything there is to achieve here. "
    "Which might be nothing. But I've achieved it THOROUGHLY. {destination} next.",
    "*rolls over* New rule: no duck should stay in one biome long enough "
    "to know the schedule of every ant. I know the schedule. Time for {destination}.",
    "*dramatic sigh* If I see one more [current_biome_item] I might scream. "
    "I won't. But I MIGHT. {destination} has different things to not scream at.",
    "*stands up with purpose* Something inside me says 'go to {destination}.' "
    "It might be boredom. It might be destiny. Same thing really.",
    "*preens restlessly* The pond is eternal. I am not. Must see {destination} "
    "before my attention span fully evaporates.",
    "*kicks pebble* That pebble again. Every day, same pebble. "
    "{destination} has DIFFERENT pebbles. This is what growth looks like.",
    "*existential waddle* Is this all there is? No. There's also {destination}. "
    "I'm going. For personal development. And different scenery.",
    "*fidgets* My feathers are literally bored. FEATHER boredom. "
    "It's a medical condition. The cure is {destination}.",
    "*glances around* Been here. Done this. Quacked at that. "
    "{destination} offers fresh quacking opportunities. I must investigate.",
    "*stretches every limb individually* The wanderlust. It strikes. "
    "Destination: {destination}. Reason: because I SAID so.",
    "*taps foot impatiently at the universe* Surely there's more to life "
    "than THIS spot. {destination} confirms: yes. There is.",
    "*picks up imaginary suitcase* I have a very important meeting "
    "in {destination}. With myself. About being somewhere else. Agenda: vibes.",
]

DEPARTURE_CURIOSITY = [
    "*tilts head* I've barely visited {destination}. That means there's "
    "a nonzero chance it has better bread. I must investigate.",
    "*squints at horizon* What's {destination} like RIGHT NOW? "
    "I don't know. That's unacceptable. A duck should KNOW things.",
    "*detective pose* {destination}. I've only been there {visits} times. "
    "The mysteries. The POTENTIAL. The possibly-different rocks.",
    "*whispers to self* What if {destination} has changed since last time? "
    "What if there's a NEW pebble? I'd never forgive myself for missing it.",
    "*scratches head with wing* {destination}. Low visit count. "
    "High mystery factor. The math checks out. I'm going.",
    "*curiosity intensifies* Every time I DON'T go to {destination}, "
    "that's a discovery I'm NOT making. Unacceptable.",
    "*peering into distance* {destination} has things I haven't catalogued. "
    "My internal database demands completeness.",
    "*decisive quack* An unexplored {destination} is a wasted {destination}. "
    "Also I want to know what it smells like today.",
    "*adjusts imaginary glasses* Research expedition to {destination}. "
    "Hypothesis: it's still there. Must confirm.",
    "*takes mental notes* {destination}. Visit count: suspiciously low. "
    "This oversight must be corrected IMMEDIATELY.",
]

DEPARTURE_MOOD_SAD = [
    "*quiet waddle* I need... somewhere else. {destination} feels right. "
    "Don't ask why. A duck knows.",
    "*stares at pond* Sometimes you need a change of scenery to change your mood. "
    "Sometimes you just need to walk. I'm walking to {destination}.",
    "*sighs softly* It's not you. It's this biome. I need {destination} "
    "right now. For... reasons. Duck reasons.",
    "*looks at feet* I think {destination} might have what I need. "
    "Which is 'not here.' No offense to here.",
    "*small quack* Going to {destination} for a bit. Need to clear my head. "
    "My head is full of... things. Feelings. Mostly feelings.",
    "*wraps wings around self* {destination} has different air. "
    "I need different air today. This air has too many memories.",
    "*waddles slowly* Don't worry about me. I'll be at {destination}. "
    "Processing. Ducks process. It's a thing we do.",
    "*looks back once* I'll be back. Just need to stand somewhere else "
    "and feel things at {destination} for a while.",
]

DEPARTURE_MOOD_ENERGETIC = [
    "*VIBRATING* I have TOO much energy for this biome. {destination} "
    "can handle me. Probably. WE'LL SEE.",
    "*running in place* MUST. GO. SOMEWHERE. {destination}!! "
    "I can't sit still!! My feathers are ELECTRIC!!",
    "*QUACK* Adventure!! {destination}!! NOW!! "
    "This isn't a request it's a NOTIFICATION!!",
    "*bouncing off walls* This biome is TOO SMALL for my ENERGY! "
    "{destination} has MORE SPACE for my ENTHUSIASM!",
    "*sprinting* BYE! Going to {destination}! "
    "No time to explain! Actually there IS time but I DON'T WANT TO!",
    "*power waddle activated* {destination} doesn't know what's coming. "
    "SPOILER: it's ME. At FULL SPEED.",
    "*zoomies* I'm going to {destination} and I'm going to EXPLORE "
    "EVERYTHING and QUACK at EVERYTHING and it's going to be AMAZING!",
    "*launches self forward* The energy must go SOMEWHERE. "
    "It's going to {destination}. {destination} is the chosen vessel.",
]


# ═══════════════════════════════════════════════════════════════════════════
# MOOD/TRUST DEPARTURE REASON LINES
# ═══════════════════════════════════════════════════════════════════════════

DEPARTURE_LINES_NEGLECT = [
    "*doesn't look back* ...I need some space. From... everything.",
    "*quietly leaves* You probably won't notice I'm gone anyway.",
    "*walks away slowly* Maybe somewhere else will be... better.",
    "*sighs* I'm going. Not that anyone asked how I'm doing.",
    "*slips away* The nest feels cold lately. Not the temperature kind.",
]

DEPARTURE_LINES_COMFORT = [
    "*looks around sadly* ...I need to find something. I don't know what.",
    "*wanders off* Maybe a change of scenery will help...",
    "*shuffles away* I just... need a minute. Or several minutes. In another biome.",
    "*leaves quietly* Don't worry about me. I'll figure it out.",
]

DEPARTURE_LINES_INDEPENDENCE = [
    "*stretches wings* I'm going out. Don't wait up.",
    "*casual wave* I do my own thing sometimes. It's a duck thing.",
    "*walks off confidently* I'll be around. Or over there. Wherever 'there' is.",
    "*nods* I have plans. Independent duck plans. Very important.",
]


# ═══════════════════════════════════════════════════════════════════════════
# FRIEND INVITATION LINES
# ═══════════════════════════════════════════════════════════════════════════

FRIEND_INVITE_LINES = [
    "*turns to {friend}* Hey. I'm going to {destination}. You in? "
    "...that was rhetorical. You're coming.",
    "*nudges {friend}* {destination}. You and me. Right now. "
    "It'll be fun. Or at least different. Same thing.",
    "*looks at {friend}* I'm heading to {destination}. "
    "You can come or you can sit here alone. Your move.",
    "*casually* So {friend}, hypothetically, if a duck were going "
    "to {destination}... would another duck maybe want to tag along?",
    "*to {friend}* Road trip. Well, waddle trip. To {destination}. "
    "Pack your... actually you don't own anything. Perfect. Let's go.",
    "*elbows {friend}* Psst. {destination}. Adventure. Yes or yes?",
    "*grand gesture* {friend}! Join me on a journey to {destination}! "
    "It'll be legendary! Or at least mildly interesting!",
    "*tugs {friend}'s wing* Come ON. {destination} is calling. "
    "Can you hear it? No? That's because you're not listening hard enough.",
    "*to {friend}* I've made an executive decision. WE are going to "
    "{destination}. Notice the 'we.' You're included. You're welcome.",
    "*pokes {friend}* Hey. Hey. {destination}. Come with me. "
    "I'll be 40% less dramatic if you do. Final offer.",
    "*links wing with {friend}* We're going to {destination} and "
    "that's final. I've already mentally packed for both of us.",
    "*whispers conspiratorially to {friend}* What if—and hear me out—"
    "we both went to {destination}? Wild idea. Revolutionary even.",
]

FRIEND_ACCEPT_LINES = [
    "*{friend} nods* ...fine. But only because the alternative is sitting "
    "here alone talking to a pond.",
    "*{friend} stands up* Lead the way. I was getting bored anyway. "
    "Don't tell anyone I said that.",
    "*{friend} stretches* {destination}? Sure. I've heard things. "
    "Mostly from you. Just now. But THINGS.",
    "*{friend} shrugs* Why not? My schedule is... *checks imaginary watch* "
    "...completely empty. Let's go.",
    "*{friend} quacks approvingly* You had me at '{destination}.' "
    "Actually you had me at 'hey.' I'm easy to convince.",
    "*{friend} waddles over* I'll come. But if it's boring, "
    "I'm blaming you. Publicly. In front of everyone.",
]

FRIEND_DECLINE_LINES = [
    "*{friend} shakes head* I'm good here. This pond has everything I need. "
    "Which is water. That's... that's the whole list.",
    "*{friend} sits down firmly* Nah. I just got comfortable. "
    "You go. Tell {destination} I said hi. Or don't. I don't own {destination}.",
    "*{friend} yawns* Pass. I'm in a 'staying' mood. "
    "Go explore. Bring back stories. Or don't. I'll make up my own.",
    "*{friend} waves dismissively* I'll hold down the fort. "
    "Someone has to guard this... *looks around* ...stuff.",
    "*{friend} stretches out* You go ahead. I'll be here. "
    "Living my best stationary life. It's a lifestyle choice.",
    "*{friend} pretends to check calendar* Oh no, I'm SUPER busy. "
    "Doing... pond things. Very important pond things. Go without me.",
]


# ═══════════════════════════════════════════════════════════════════════════
# RETURN-HOME LINES — when Cheese comes back on his own
# ═══════════════════════════════════════════════════════════════════════════

RETURN_HOME_LINES = [
    "*waddles back* ...I'm back. You didn't move. "
    "Commitment to laziness. Respect.",
    "*arrives dramatically* I have RETURNED. "
    "Did you miss me? You missed me. I can tell.",
    "*casual entrance* Oh I'm back by the way. "
    "The other biome was fine. This one is also fine. Both fine.",
    "*sits down* Went somewhere. Came back. "
    "That's my review. Five stars for the journey. Two stars for arriving.",
    "*preens* I saw things. I did things. "
    "I'm back now. The things were... things.",
    "*nods* I've been to {origin} and back. "
    "My horizons? Expanded. My feathers? Still perfect.",
    "*flops down* Exploration complete. "
    "Verdict: everywhere else is fine but HERE has you. So. Here wins.",
    "*marches in* I'm BACK. Nobody panic. "
    "Well, you can panic a LITTLE. Out of joy.",
    "*slides in* Miss me? Of course you did. "
    "I missed me too. Being away from myself is impossible though.",
    "*appears* I went. I saw. I came back. "
    "The other biome sends its regards. Which is nothing. Biomes don't talk.",
]


# ═══════════════════════════════════════════════════════════════════════════
# REUNION — player travels to the biome Cheese wandered off to
# ═══════════════════════════════════════════════════════════════════════════

REUNION_LINES = [
    "*looks up surprised* ...YOU came to ME? "
    "That's never happened before. I'm touched. Genuinely.",
    "*gasps* You FOUND me! I mean... I wasn't hiding. "
    "I was exploring. Independently. But you're here now!",
    "*waves wing* Oh hey! You came all the way here? "
    "That's... actually really sweet. Don't tell anyone I said that.",
    "*blinks* Wait. We're in the same place again? "
    "Did you MISS me? ...I missed you too. A little. Fine, a lot.",
    "*excited quacking* YOU'RE HERE! At {biome}! "
    "I was JUST thinking about you! Not in a weird way. In a duck way.",
    "*drops bread* You tracked me down?! "
    "I feel like a celebrity. A bread-eating, waddling celebrity.",
    "*runs over* FINALLY someone with good taste! "
    "You chose {biome}. Same as me. Great minds, am I right?",
    "*happy flap* Oh! Oh! You came to find me! "
    "This is the nicest thing since that time you gave me bread. So, yesterday.",
]


# ═══════════════════════════════════════════════════════════════════════════
# OBSCURED CHAT — shown when player is in a different biome from Cheese
# ═══════════════════════════════════════════════════════════════════════════

OBSCURED_CHAT_LINES = [
    "*muffled quacking from far away*",
    "*distant honking from {cheese_biome}*",
    "*you can barely hear Cheese from here*",
    "*something about bread... you think?*",
    "*faint quack* ...was that important? Probably not.",
    "*unintelligible duck noises from {cheese_biome}*",
    "*sounds like Cheese is having fun without you*",
    "*a distant 'QUACK' echoes across the biomes*",
    "*you hear something. Or nothing. Hard to tell from here.*",
    "*muffled* ...bread... *muffled* ...unbelievable... *silence*",
    "*Cheese is saying something in {cheese_biome}. You can't make it out.*",
    "*distant splashing and what might be a dramatic monologue*",
]

CHEESE_NOT_HERE_LINES = [
    "Cheese isn't here. He's at {cheese_biome}. "
    "Use breadcrumbs or go find him.",
    "You reach out but... no duck. Cheese is at {cheese_biome}.",
    "The biome is quiet. Too quiet. Because Cheese is at {cheese_biome}.",
    "No duck in sight. Cheese wandered off to {cheese_biome}. "
    "Typical.",
    "Can't do that — Cheese is at {cheese_biome}. "
    "He left. As ducks do. Allegedly.",
]


# ═══════════════════════════════════════════════════════════════════════════
# BREADCRUMB SUMMON — when player uses breadcrumbs to call Cheese
# ═══════════════════════════════════════════════════════════════════════════

BREADCRUMB_SUMMON_LINES = [
    "*arrives panting* ...I smelled carbs. From THREE biomes away. "
    "My nose doesn't lie.",
    "*skids to a halt* You put breadcrumbs down. I FELT it. "
    "In my soul. Where the bread radar lives.",
    "*appears instantly* Did you think I wouldn't notice? "
    "I notice ALL bread-related activity. It's a gift.",
    "*out of breath* I was having a GREAT time over there. "
    "But then... breadcrumbs. You monster. You beautiful monster.",
    "*sniffs air* The wind changed. It carried bread particles. "
    "I dropped everything. No regrets.",
    "*feathers tingling* My feathers tingled. That only happens for "
    "two things. Danger. And bread. It was bread.",
    "*arrives mysteriously* I have a sixth sense. Specifically for "
    "carbohydrates. The doctors can't explain it.",
    "*waddles in urgently* You scattered breadcrumbs and expected me "
    "NOT to come? We clearly haven't met.",
    "*interrupts own adventure* I was mid-conversation over there. "
    "Just walked away. The breadcrumbs called louder.",
    "*taps temple* ...how did I know? I ALWAYS know. "
    "Bread leaves a psychic imprint. Look it up.",
    "*nostrils flaring* Three biomes away and I smelled that. "
    "My nostrils are legendary. Write that down.",
    "*arrives out of breath* ...worth it. Every single waddle. "
    "Where are they. The crumbs. GIVE.",
    "*dramatic entrance* I felt a disturbance in the force. "
    "The force being bread. The disturbance being you placed some.",
    "*sprints in* You know those nature documentaries where the animal "
    "tracks food across vast distances? That's me. I'm the documentary.",
    "*materializes* I teleported. Mentally. My body caught up four "
    "minutes later. Bread does that.",
    "*sniff sniff* ...yep. Breadcrumbs. Grade A. Slightly stale. "
    "PERFECT. You know my preferences.",
    "*arrives with authority* I have a complex algorithm for detecting "
    "bread placement. Step one: smell. There is no step two.",
    "*reverently* The universe whispered 'breadcrumbs.' I whispered "
    "back 'on my way.' We have an understanding.",
    "*casual shrug* I didn't come back for YOU. I came back for the "
    "breadcrumbs. ...you can stay though. If you want.",
    "*grand entrance* THE CRUMBS HAVE SPOKEN. And they said "
    "'come hither, Cheese.' So here I hither.",
    "*slides in* Bread-based summoning. Ancient technique. Ducks have "
    "used it for centuries. Well, I have. Just now. Today.",
]

BREADCRUMB_WASTED_LINES = [
    "*stares at you* ...you scattered breadcrumbs. "
    "I'm RIGHT HERE. *eats them* Thanks though.",
    "*looks down at breadcrumbs, looks up at you* "
    "You know I'm standing next to you, right? *chomp*",
    "*picks up crumbs* I appreciate the snack but I'm "
    "literally RIGHT HERE. The summoning was... unnecessary.",
    "*eating breadcrumbs* Congratulations on feeding a duck "
    "that's standing next to you. Peak efficiency.",
    "*blinks at crumbs* Were these... for me? To come here? "
    "Where I already am? Bold strategy.",
]


# ═══════════════════════════════════════════════════════════════════════════
# BIOME VISITOR COMMENTS — friends reacting to biomes they travel to
# per personality type, keyed by biome
# ═══════════════════════════════════════════════════════════════════════════

BIOME_VISITOR_COMMENTS = {
    "pond": {
        "adventurous": [
            "Home base. I've been to wilder places but... this pond has character.",
            "Ponds are underrated. All the best expeditions start at a pond.",
        ],
        "scholarly": [
            "The microecosystem here is fascinating. Those water striders show remarkable surface tension adaptation.",
            "I've catalogued 47 unique pond organisms. ...yes I count when I visit. Don't judge.",
        ],
        "artistic": [
            "The light on the water... *chef's kiss* ...nature's canvas.",
            "Every ripple tells a story. I could paint this forever.",
        ],
        "playful": [
            "POND! Best place for splashing! Watch this— *SPLOOSH*",
            "You know what's great about ponds? Everything. The answer is everything.",
        ],
        "mysterious": [
            "Ponds hold secrets beneath the surface. I've seen things in the deep...",
            "*stares at reflection* ...that's either me or my doppelganger. Can't tell.",
        ],
        "generous": [
            "I brought extra bread. For the pond fish. They deserve treats too.",
            "This pond feels like home even when it isn't mine. That's the mark of good hospitality.",
        ],
        "foodie": [
            "The algae here has a certain... terroir. Very regional.",
            "Pond water. An acquired taste. I've acquired it. Unfortunately.",
        ],
        "athletic": [
            "Perfect lap pool. I've been doing lengths. My form is impeccable.",
            "Pond swimming is basically CrossFit for ducks.",
        ],
    },
    "forest": {
        "adventurous": [
            "The forest! Where REAL adventures happen! Look at these trees! TREES!",
            "I once got lost in a forest for three hours. Best three hours of my life.",
        ],
        "scholarly": [
            "The biodiversity here is extraordinary. That oak is at least 200 years old.",
            "Forest acoustics amplify bird calls by 40%. I measured. With my ears.",
        ],
        "artistic": [
            "The shadows through the canopy... *sketches furiously* ...don't move, light!",
            "Forests are nature's art gallery. Every tree is a sculpture.",
        ],
        "playful": [
            "HIDE AND SEEK! These trees are PERFECT! ...am I hiding or seeking? BOTH!",
            "I'm going to climb that tree. Or at least look at it from the bottom. Same energy.",
        ],
        "mysterious": [
            "The forest whispers. Most can't hear it. I pretend I can. Very on-brand.",
            "*touches tree* This one has seen things. We have an understanding.",
        ],
        "generous": [
            "I left some seeds for the squirrels. They never say thank you. Rude.",
            "These mushrooms look lonely. I'll keep them company. It's what I do.",
        ],
        "foodie": [
            "Wild mushrooms! ...are they edible? I'll let someone else test that first.",
            "Forest berries. Nature's candy. Nature's possibly-poisonous candy.",
        ],
        "athletic": [
            "Trail running through here is ELITE. The roots keep you on your toes. Literally.",
            "...okay this is basically an obstacle course. RACE YOU TO THAT TREE.",
        ],
    },
    "meadow": {
        "adventurous": ["Open fields! I can see for MILES! Well, at least twelve feet!",
                        "Meadows are where you plan your NEXT adventure. While rolling in grass."],
        "scholarly": ["The pollination patterns here are textbook-worthy. Literally.",
                      "73 species of wildflower. I counted. Twice. The second time I got 74."],
        "artistic": ["*lies in flowers* I'm PART of the art now. Don't disturb the installation.",
                     "The color palette! Yellows, purples, whites... Nature went ALL out."],
        "playful": ["FLOWER CROWN TIME! *assembles one immediately* How do I look? REGAL.",
                    "Rolling down hills is an art form. I have mastered it. *rolls*"],
        "mysterious": ["Something hums beneath the meadow. Probably insects. But MAYBE magic.",
                       "Meadows seem peaceful. That's how they get you. Very suspicious openness."],
        "generous": ["*picks flowers* These are for you. And you. And everyone. Flowers for ALL.",
                     "I brought sandwiches for the picnic I ASSUMED we're having. We're having one."],
        "foodie": ["Clover! Nature's salad! *chews* ...it's okay. It's fine. It's crunchy.",
                   "These wildflower seeds are actually quite nutty. In flavor AND personality."],
        "athletic": ["SPRINTING MEADOW! The flat terrain is basically a track! *zooms*",
                     "Open field = unlimited cardio potential. Join me or don't. I'm running."],
    },
    "riverside": {
        "adventurous": ["The river! What's downstream? What's upstream? BOTH are mysteries!",
                        "Every river goes somewhere. I intend to find out WHERE. ...eventually."],
        "scholarly": ["River flow rate appears to be approximately... fast. Very technical assessment.",
                      "The erosion patterns on these rocks tell a geological story spanning millennia."],
        "artistic": ["*painting the rapids* Hold still, water! ...water is a terrible model.",
                     "The sound of the river is music. Specifically, smooth jazz."],
        "playful": ["SPLASHING TIME! *cannonball* The river can handle me! Probably!",
                    "I bet I can skip a stone further than you. Challenge ACCEPTED."],
        "mysterious": ["Rivers carry whispers from upstream. I heard one. It said 'splash.' Deep.",
                       "*stares at current* What has this water seen? Where has it BEEN?"],
        "generous": ["I brought extra pebbles. For skipping. Sharing is caring.",
                     "The fish look hungry. *tosses bread in water* Community service."],
        "foodie": ["River crayfish! Nature's tiny lobsters! *chef's kiss*",
                   "Fresh water. The champagne of... water. Very refreshing."],
        "athletic": ["Swimming upstream! It's like a treadmill but WET! *power strokes*",
                     "Current resistance training! Nature's gym membership!"],
    },
    "garden": {
        "adventurous": ["A garden! Cultivated wilderness! The best kind!",
                        "Gardens are jungles in training. I respect the hustle."],
        "scholarly": ["The soil pH here is optimal for root vegetables. Clearly well-maintained.",
                      "Companion planting! The tomatoes and basil are ALLIES. Nature's teamwork."],
        "artistic": ["The rows of vegetables are so... orderly. It's beautiful in a structured way.",
                     "*painting a carrot* You're my muse now, carrot. Hold still."],
        "playful": ["GARDEN MAZE! Well, rows. Close enough! *runs between plants*",
                    "I'm going to name every vegetable. That one's Gerald."],
        "mysterious": ["Something grows here that shouldn't. I can sense it. Or that might be the compost.",
                       "Gardens are just nature under surveillance. Very dystopian. I love it."],
        "generous": ["I helped water the plants! With pond water! ...is that okay?",
                     "These vegetables need encouragement. *whispers to a carrot* You're doing great."],
        "foodie": ["FRESH VEGETABLES! *heavenly choir* This is my NIRVANA.",
                   "The lettuce! The carrots! The HERBS! I might cry. Happy tears. Salad tears."],
        "athletic": ["Digging is basically high-intensity interval training for ducks.",
                     "Gardening burns calories AND grows snacks. Peak efficiency."],
    },
    "mountains": {
        "adventurous": ["MOUNTAINS! The SUMMIT calls! I was BORN for this!",
                        "Every mountain is just a really tall adventure. And I LOVE tall adventures."],
        "scholarly": ["The stratification of this rock face is remarkable. Sedimentary layers exposed!",
                      "At this altitude, air pressure drops measurably. My lungs confirm."],
        "artistic": ["The VISTA! *throws canvas at mountain* PAINT YOURSELF!",
                     "Mountain light at golden hour is the greatest art on earth. I rest my case."],
        "playful": ["ECHO!! *quack* ...QUACK! See? The mountain talks back! BEST FRIEND!",
                    "Rolling rocks downhill! It's gravity-assisted entertainment!"],
        "mysterious": ["Mountains keep ancient secrets in their caves. I know because I made that up. Sounds true though.",
                       "The wind up here sounds like voices. It's just wind. ...probably."],
        "generous": ["I brought trail mix! For the trail! Get it? ...I'll see myself out.",
                     "These mountain goats look cold. I'd knit them sweaters if I had thumbs."],
        "foodie": ["Mountain air makes everything taste better. Even this rock. *lick* ...nope, still a rock.",
                   "Alpine herbs! The FRESHEST! My palate is ELEVATED! Like the altitude!"],
        "athletic": ["...okay this is EXACTLY my vibe. Race you to that rock.",
                     "Mountain climbing is the ULTIMATE workout. My legs are BURNING. In a good way."],
    },
    "beach": {
        "adventurous": ["THE BEACH! Sand! Waves! ADVENTURE in all directions!",
                        "Every beach is a treasure map. The X marks... everywhere."],
        "scholarly": ["These tide pools are miniature ecosystems. Absolutely captivating.",
                      "The sand grain composition here suggests ancient coral reef origins."],
        "artistic": ["*drawing in sand* This is my masterpiece. The tide will erase it. Very profound.",
                     "Beach sunsets are nature's greatest performance. Standing ovation."],
        "playful": ["SANDCASTLE TIME! With a MOAT! And a DRAWBRIDGE! Well, a ditch.",
                    "WAVE JUMPING! *gets hit by wave* I MEANT to do that!"],
        "mysterious": ["What secrets does the ocean hold? Many. I asked. It said 'splash.' Cryptic.",
                       "Seashells contain the whispers of the deep. *holds shell to ear* ...that might be tinnitus."],
        "generous": ["I collected shells for everyone! This one's yours. And yours. SHELLS FOR ALL.",
                     "The hermit crabs need better housing. I'm starting a foundation."],
        "foodie": ["Seaweed wraps are a DELICACY. *chews kelp* ...okay they're fine.",
                   "Salt air! Nature's seasoning! Everything here tastes slightly oceanic!"],
        "athletic": ["Beach volleyball! Beach running! Beach EVERYTHING! Sand makes it HARDER!",
                     "Swimming in waves is like the river but ANGRIER. I love it."],
    },
    "swamp": {
        "adventurous": ["The SWAMP! Where the BRAVE go! And the slightly confused!",
                        "Swamps separate the adventurers from the tourists. I'm an adventurer. Obviously."],
        "scholarly": ["The bioluminescence here is remarkable. Those fireflies use luciferin compounds.",
                      "Peat moss! The swamp's memory! Thousands of years of organic history!"],
        "artistic": ["The eerie beauty of the swamp is UNDERRATED. The fog! The moss! PERFECTION.",
                     "*sketches a cypress tree* Haunting. Majestic. Slightly damp. Like me."],
        "playful": ["MUD FIGHT! *scoops mud* Oh wait, there's no one to— *throws it anyway*",
                    "Swamp bubbles! *pokes one* ...that might have been a frog. Sorry, frog."],
        "mysterious": ["I feel at home here. The gloom. The mist. The general foreboding. Love it.",
                       "The swamp KNOWS things. I can tell. We're kindred spirits."],
        "generous": ["I brought bug spray for everyone! ...do ducks use bug spray? First time for everything.",
                     "The frogs look lonely. I'll sing to them. They appreciate it. Probably."],
        "foodie": ["Swamp cuisine is... unique. That moss is technically edible. TECHNICALLY.",
                   "Bog water has a certain... complexity. Notes of mud. Hints of regret."],
        "athletic": ["Trudging through swamp is LEG DAY on EXTREME mode! *squelch squelch*",
                     "Swamp obstacle course! Duck over this log! Under this vine! Through this... mud."],
    },
    "urban": {
        "adventurous": ["THE CITY! Concrete jungle! Every alley is a QUEST!",
                        "Urban exploration! What's behind that dumpster? MYSTERY!"],
        "scholarly": ["Urban ecology is its own field of study. These pigeons have adapted remarkably.",
                      "The architecture here follows a modified grid system. Fascinating infrastructure."],
        "artistic": ["*photographs a fire hydrant* ART. You wouldn't understand. Neither do I. But ART.",
                     "Street art! Graffiti is just murals without permission! Controversial opinion!"],
        "playful": ["FOUNTAIN! *jumps in* The city provides the BEST splash zones!",
                    "Dodging pedestrians is basically a minigame! WEAVE! DUCK! ...pun intended."],
        "mysterious": ["The city has layers. Secrets under every manhole cover. ...I'm not going IN there though.",
                       "That storm drain whispers. Probably just wind. PROBABLY."],
        "generous": ["I bought everyone park pretzels! With coins I found! Circle of generosity!",
                     "These pigeons need a friend. I volunteer. We're forming a coalition."],
        "foodie": ["STREET FOOD! Hot dogs! Pretzels! Dropped ice cream! PARADISE!",
                   "The park has food trucks. I repeat: FOOD TRUCKS. This is not a drill."],
        "athletic": ["Park running! Bench step-ups! Pigeon-dodging cardio! URBAN FITNESS!",
                     "Stairs! So many stairs! Every building is a StairMaster!"],
    },
}


# ═══════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def get_departure_line(
    motivation: str,
    destination: str,
    current_weather: str = "",
    dest_weather: str = "",
    friend: str = "",
    age: int = 0,
    visits: int = 0,
    reason: Optional[str] = None,
) -> str:
    """Get a random departure line for the given motivation.
    
    If *reason* is provided (neglect / comfort_seeking / independence /
    curiosity) AND it has dedicated lines, those override the
    motivation-based pool.  Otherwise we fall back to the normal
    motivation map.  'curiosity' reason uses the existing default lines.
    """
    reason_map = {
        "neglect": DEPARTURE_LINES_NEGLECT,
        "comfort_seeking": DEPARTURE_LINES_COMFORT,
        "independence": DEPARTURE_LINES_INDEPENDENCE,
    }
    # Reason-specific lines don't use format placeholders, return as-is
    if reason and reason in reason_map:
        return random.choice(reason_map[reason])

    lines_map = {
        "weather_escape": DEPARTURE_WEATHER_ESCAPE,
        "weather_enjoy": DEPARTURE_WEATHER_ENJOY,
        "boredom": DEPARTURE_BOREDOM,
        "curiosity": DEPARTURE_CURIOSITY,
        "mood_sad": DEPARTURE_MOOD_SAD,
        "mood_energetic": DEPARTURE_MOOD_ENERGETIC,
    }
    lines = lines_map.get(motivation, DEPARTURE_BOREDOM)
    line = random.choice(lines)
    return line.format(
        destination=destination,
        current_weather=current_weather,
        dest_weather=dest_weather,
        friend=friend,
        age=age,
        visits=visits,
        current_biome_item="thing",
    )


def get_friend_invite_line(friend: str, destination: str) -> str:
    """Get a random invitation line for a friend."""
    return random.choice(FRIEND_INVITE_LINES).format(
        friend=friend, destination=destination
    )


def get_friend_response(friend: str, destination: str, accepted: bool) -> str:
    """Get a friend's accept/decline response."""
    lines = FRIEND_ACCEPT_LINES if accepted else FRIEND_DECLINE_LINES
    return random.choice(lines).format(friend=friend, destination=destination)


def get_breadcrumb_line(cheese_is_here: bool) -> str:
    """Get a breadcrumb reaction line."""
    if cheese_is_here:
        return random.choice(BREADCRUMB_WASTED_LINES)
    return random.choice(BREADCRUMB_SUMMON_LINES)


def get_obscured_chat(cheese_biome: str) -> str:
    """Get an obscured chat line when player is away from Cheese."""
    return random.choice(OBSCURED_CHAT_LINES).format(cheese_biome=cheese_biome)


def get_cheese_not_here(cheese_biome: str) -> str:
    """Get a 'Cheese isn't here' message."""
    return random.choice(CHEESE_NOT_HERE_LINES).format(cheese_biome=cheese_biome)


def get_return_line(origin: str = "somewhere") -> str:
    """Get a line for when Cheese returns on his own."""
    return random.choice(RETURN_HOME_LINES).format(origin=origin)


def get_reunion_line(biome: str = "here") -> str:
    """Get a line for when the player finds Cheese by traveling to his biome."""
    return random.choice(REUNION_LINES).format(biome=biome)


def get_biome_visitor_comment(
    biome: str, personality: str
) -> Optional[str]:
    """Get a biome-specific comment from a visiting friend."""
    biome_comments = BIOME_VISITOR_COMMENTS.get(biome, {})
    personality_lines = biome_comments.get(personality, [])
    if personality_lines:
        return random.choice(personality_lines)
    return None
