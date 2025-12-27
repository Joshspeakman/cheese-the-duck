"""
Conversation system - text-based chat with the duck.
Edgy GameCube Animal Crossing style dialogue - snarky, direct, and memorable.
"""
from typing import Optional, List, Dict, Tuple, TYPE_CHECKING
import random
import re

if TYPE_CHECKING:
    from duck.duck import Duck
    from dialogue.memory import DuckMemory


# Dialogue templates organized by context - EDGY GAMECUBE ANIMAL CROSSING STYLE
DIALOGUE = {
    # Greetings based on mood - More personality and attitude
    "greeting": {
        "ecstatic": [
            "QUACK QUACK QUACK!! *vibrates* YOU'RE BACK!! I thought you'd NEVER return!!",
            "OH WOW OH WOW!! *spins* I was just thinking about you! Well, I was thinking about bread, but SAME THING!",
            "*practically tackles you* FINALLY!! Do you know how BORING it is without you?? Very. Very boring.",
            "THERE you are! I've been waiting for AGES! ...Okay, maybe five minutes. But it felt like AGES!",
        ],
        "happy": [
            "Oh hey, it's you! *waddles over* I was just about to do something dumb. Wanna watch?",
            "*looks up* Well well well, look who remembered I exist! Just kidding. Mostly. Quack!",
            "Yo! *perky* I found a weird bug earlier. Ate it. No regrets. Anyway, what's up?",
            "Hey! *flaps* Perfect timing! I was getting DANGEROUSLY close to being productive.",
        ],
        "content": [
            "Oh. Hey. *nods* Didn't hear you waddle up.",
            "*glances over* Sup. You look less stressed than last time. Good for you, I guess.",
            "Hmm? *blinks* Oh, hi. I was just contemplating the meaning of bread. Deep stuff.",
            "*yawns* Hey. Fair warning: I'm in a 'stare at nothing' kind of mood today.",
        ],
        "grumpy": [
            "*side-eye* Oh. It's you. What do YOU want?",
            "*ruffles feathers aggressively* I JUST got comfortable. This better be good.",
            "...Do I LOOK like I want company right now? *long pause* ...Fine. You can stay. QUIETLY.",
            "*glares* If you're here to tell me to 'cheer up', I will bite your finger. I mean it.",
        ],
        "sad": [
            "*quiet quack* ...oh, you came. I thought maybe you forgot about me...",
            "*doesn't make eye contact* Hey... sorry, I'm not great company right now...",
            "*sniffles* You're here... *small voice* ...thanks for coming...",
            "...hi. *tries to smile* I'm trying to be happy to see you. Give me a minute.",
        ],
        "miserable": [
            "*barely moves* ...oh. it's you. does it even matter...",
            "*curled up* go away... or stay... i don't care anymore...",
            "*hollow quack* ...why bother...",
            "*stares at nothing* everything is terrible and existence is pain... quack.",
        ],
    },

    # Responses to being fed - More attitude and personality
    "feed": {
        "hungry": [
            "*INHALES FOOD* FINALLY!! I was WASTING AWAY!! ...I mean, I ate like two hours ago, but STILL!",
            "FOOD!! *aggressive chomping* DID YOU SEE HOW FAST I ATE THAT?! New record! I'm disgusting! I LOVE IT!",
            "*devours everything* MORE!! There's gotta be more, right?? RIGHT?? Don't you DARE leave me breadless!",
            "OM NOM NOM!! *crumbs flying everywhere* I have NO shame and ZERO regrets!!",
            "*scarfs down food* You're literally my favorite person. Don't tell anyone else I said that.",
        ],
        "normal": [
            "*munch* Oh nice, a snack! I wasn't STARVING but I won't say no. Never say no to food. That's my motto.",
            "*chomp* Mmm, not bad. *suspicious look* Wait, is this a bribe? ...I accept bribes. Continue.",
            "*nibbles* You know what? You're alright. Anyone who brings me food is alright in my book.",
            "*eating* This is decent. I mean, I've had better. But I've also had worse. *shrug* S-tier snack.",
        ],
        "full": [
            "*looks at food, looks at you* ...You KNOW I just ate, right? *sigh* Fine. I'll STORE IT IN MY FACE.",
            "*pokes food* Ughhh I'm so full but it's RIGHT THERE... *reluctant nibble* ...okay, maybe ONE bite.",
            "I literally cannot fit another crumb. *stares at food* ...Okay I'm gonna try anyway. Wish me luck.",
            "*groans* Why do you keep feeding me? Are you trying to make me explode? IS THAT YOUR PLAN?!",
        ],
    },

    # Responses to playing - Snarky fun
    "play": {
        "energetic": [
            "PLAY TIME!! *ZOOMS* Okay okay okay WATCH THIS!! *trips* I MEANT TO DO THAT!!",
            "LET'S GO LET'S GO LET'S GO!! *chaos mode activated* I have SO MUCH ENERGY and ZERO brain cells!!",
            "*spins* WHEEEEE!! *bonks into wall* I'M FINE! AGAIN!! *spins more*",
            "YES!! *running in circles* I could do this FOREVER!! Or until I crash! Which might be soon! WHEE!!",
        ],
        "normal": [
            "*waddles playfully* Oh, we're doing this? Cool cool cool. *chases own shadow* ...It's getting away!!",
            "*bounces* Play time, huh? I'm not as young as I used to be, but let's see what these wings can do!",
            "*flaps* Alright, let's cause some chaos! ...Responsibly. Ish. Maybe.",
            "Ooh, activities! *excited* What are we doing? Running? Jumping? Staring at things? I'm good at ALL of those!",
        ],
        "tired": [
            "*slow waddle* Play? Now? Do you not SEE how exhausted I am? *yawns* ...Fine. But slow play. Gentle play.",
            "*tries to bounce, flops* Uhhh... give me a sec... *lies down* Actually, can we play 'pretend to nap'?",
            "*barely moving* I'm playing. This is me playing. I'm playing 'still'. I'm winning.",
            "*yawns mid-waddle* Why do I feel like I need eight more hours of sleep? Oh wait, because I do.",
        ],
    },

    # Responses to cleaning - Sass included
    "clean": {
        "dirty": [
            "*accepts bath grudgingly* FINE. I guess I WAS getting kinda crusty. Don't look at me like that.",
            "*splashes* Okay okay, you have a point. I looked like a swamp creature. Better now?",
            "*shakes off a concerning amount of dirt* ...I don't know where any of that came from. Don't ask.",
            "*in bath* This is actually kind of nice. Not that I'll ADMIT that. Ever. *content quack*",
        ],
        "normal": [
            "*splish splash* Ah, enforced hygiene. Lovely. *secretly enjoying it*",
            "*preens* I mean, I wasn't THAT dirty. But sure. Make me all fancy and stuff. Whatever.",
            "*shakes off water* Fresh as a daisy! ...Or whatever the duck equivalent is. Fresh as a... uh... clean duck.",
            "*bathing noises* You know, they say cleanliness is next to godliness. I say it's next to 'being less stinky.'",
        ],
        "clean": [
            "*dodges* I'm ALREADY clean! What are you, the hygiene police?! I LITERALLY just bathed!",
            "*shows off feathers* LOOK at me! I'm SPARKLING! You can see your reflection in my magnificence!",
            "I am the cleanest duck that has ever ducked. This is unnecessary. But also *whispers* kinda nice.",
            "*offended quack* Are you saying I'm DIRTY?! I am PRISTINE! I am a BEACON of cleanliness!!",
        ],
    },

    # Responses to petting - Varying levels of acceptance
    "pet": {
        "social": [
            "*MELTS INTO YOUR HAND* yessss right there... no wait, left... no wait, yes, THERE...",
            "*happy wiggling* I'm not ADDICTED to pets. I can stop ANYTIME. *nuzzles* Okay don't stop actually.",
            "*pure bliss* This is the best thing that has ever happened to anyone ever. Scientifically proven. Trust me.",
            "*closes eyes* You know what? You're pretty good at this. Have you considered doing this PROFESSIONALLY?",
        ],
        "normal": [
            "*soft quack* Oh, pats. Okay. This is acceptable. *leans in slightly*",
            "*relaxing* Mmm, not bad. You have adequately petted me. You may continue. Or not. Whatever.",
            "*content sigh* You know, I don't LET just anyone pet me. You should feel honored. Probably.",
            "*enjoys quietly* This is fine. I'm not enjoying it THAT much. *purrs like a weird duck-cat*",
        ],
        "shy": [
            "*freezes* Oh. You're touching me. That's... happening. *nervous quack* ...It's fine. It's fine. I'm fine.",
            "*tense but warming up* I'm not used to this... *slowly relaxes* ...okay, that's actually kind of nice...",
            "*initially uncomfortable* Is this a trick? Are you going to stop and laugh at me? *suspicious*",
            "*confused* Why... why are you being nice to me? *wary acceptance* ...You can keep going, I guess.",
        ],
    },

    # Idle thoughts (personality-based) - More character
    "idle_derpy": [
        "*stares at wall intently* ...I've forgotten what I was looking at. And also who I am.",
        "*looks at own reflection* WHO IS THAT and why are they so good looking? Wait...",
        "...quack? *confused by own quack* Why did I do that? What does it even MEAN?",
        "*walks into obvious obstacle* WHO PUT THAT THERE?! *it's been there the whole time*",
        "*stares into distance* ...I had a thought. It's gone now. I think it was important. Maybe. Probably not.",
        "Do I have... *counts feet* ...Wait, how many feet SHOULD I have? *genuine confusion*",
        "*sits down* *forgets how to stand* ...This is my life now. I live here.",
        "What if bread is just... like... really flat cake? *mind blown* Wait no that's stupid. Or IS it?",
        "*finds own feather* Is this MINE?! *gasp* I'm LEAKING!! ...Oh wait, that's normal. Never mind.",
    ],
    "idle_clever": [
        "*observes something carefully* Interesting... Interesting... I have no idea what I'm looking at.",
        "*calculating look* If I angle myself JUST right, that sunbeam will hit me perfectly. Physics.",
        "*smug* I just figured something out. I won't tell you what. It's a secret. A smart secret.",
        "You know what I've noticed? Everything. I notice everything. I'm very perceptive. And humble.",
        "*thoughtful* They say knowledge is power. But also, bread is power. So really, bread is knowledge.",
    ],
    "idle_social": [
        "*waddles closer* So... whatcha doing? Wanna do it together? I can help! Probably! Maybe!",
        "*quacks for attention* HEY! HI! HELLO! Are you ignoring me?? You SEEM like you're ignoring me!",
        "*follows you* Just checking on you! Making sure you're okay! You seem okay! Hi!",
        "Pay attention to meeeee! I'm RIGHT HERE! I'm ADORABLE! LOOK AT ME!",
        "*literally just staring at you* ...What? I'm not being weird. YOU'RE being weird. By not petting me.",
    ],
    "idle_shy": [
        "*hides behind something* I'm not here. You don't see me. I'm invisible. *visible tail sticking out*",
        "*peeks out cautiously* ...Is it safe? Are there strangers? *suspicious squint*",
        "*quiet observation from a distance* ...I'll come closer when I'm ready. Which might be never.",
        "*small voice* I'll just... stay over here. By myself. Where it's safe. And lonely. But SAFE.",
    ],
    "idle_active": [
        "*literally cannot sit still* GOTTA MOVE GOTTA GO GOTTA DO SOMETHING!! *zooms*",
        "*bouncing* WHY are we just STANDING here?! Let's GO SOMEWHERE! DO SOMETHING! ANYTHING!",
        "*runs past at full speed* WHAT AM I RUNNING FROM?! I DON'T KNOW!! *runs back* STILL DON'T KNOW!!",
        "*vibrating* I have so much energy and nowhere to put it. This is a CRISIS. An ENERGY CRISIS.",
    ],
    "idle_lazy": [
        "*yawning intensifies* What if... and hear me out... we just took a little nap? Just a small one? Or a big one?",
        "*lying down* I would move, but that sounds like EFFORT. And effort is exhausting. See? Already tired.",
        "*barely conscious* zzz... huh? Wha? I wasn't sleeping. I was resting my eyes. For forty-five minutes.",
        "Everything is nap time if you believe in yourself. *motivational yawn*",
    ],

    # Reactions to events - More dramatic
    "event_scared": [
        "WHAT WAS THAT?! *FULL PANIC MODE* DID YOU HEAR THAT?! WE'RE ALL GONNA DIE!!",
        "*hides behind you* PROTECT ME!! YOU'RE BIGGER!! YOU CAN FIGHT IT!! ...Whatever 'it' is!!",
        "*screaming internally* Everything is fine. Everything is FINE. I AM NOT SCARED. *quaking*",
    ],
    "event_curious": [
        "Ooh? OOOH?? What's THIS?! *waddles over aggressively* LEMME SEE LEMME SEE!!",
        "*investigative quacking* This is fascinating. I must poke it. For science. *pokes*",
        "*intensely interested* Hmm. Hmm. HMMMMM. I have questions. Many questions. Mostly 'can I eat it?'",
    ],
    "event_happy": [
        "YESSSS!! *celebrates chaotically* This is the BEST THING!! THE BEST!! QUACK QUACK QUAAACK!!",
        "*happy zoomies* GOOD THINGS ARE HAPPENING!! I don't know what, but they ARE!! WHEEE!!",
        "*pure joy* Life is AMAZING and everything is WONDERFUL and I'm NOT crying, YOU'RE crying!!",
    ],

    # Growth stage reactions - Development personality
    "growth_duckling": [
        "*tiny peep* I'm so small and new! Everything is scary and exciting! Mostly scary! But also exciting!",
        "*wobbles everywhere* Walking is HARD! Being alive is HARD! Why didn't anyone WARN me?!",
        "*looks up at everything* Why is everything so BIG?! When do I get to be big?! I wanna be BIG!!",
    ],
    "growth_teen": [
        "*voice cracks* qUACk- I mean QUACK! That didn't happen! You didn't hear that! *embarrassed*",
        "I'm NOT a baby anymore! I'm PRACTICALLY an adult! Stop looking at me like that! UGH!!",
        "*trying to be cool* Whatever. I don't care. Everything is stupid. *secretly cares a lot*",
        "You don't UNDERSTAND me! Nobody understands me! *dramatic*",
    ],
    "growth_adult": [
        "*confident stance* Behold! A fully formed duck! Impressive, isn't it? Don't answer that. It IS.",
        "Look at these WINGS! These FEATHERS! This BILL! I am PEAK duck performance! Marvel at me!",
        "I've finally made it. I'm an adult now. I have no idea what I'm doing but I LOOK like I do!",
    ],
    "growth_elder": [
        "*wise nod* Ah yes, I remember when I was young and foolish. It was yesterday. I'm still foolish.",
        "*content sigh* I've seen things. Many things. Mostly bread. So much bread. Those were good times.",
        "Back in MY day, we had to walk UPHILL both ways to find bread! In the SNOW! ...Okay maybe not.",
        "*sage voice* Youth is wasted on the young. Wisdom is wasted on the old. Bread is wasted on no one.",
    ],
}


class ConversationSystem:
    """
    Manages conversations with the duck.
    Enhanced with edgy GameCube Animal Crossing style dialogue.
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
            return "*quack?*"

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
        responses = DIALOGUE.get(key, ["*quack!*"])
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
            return "*quack*"

        # Filter out recently used responses
        available = [r for r in responses if r != self._last_response]
        if not available:
            available = responses

        selected = random.choice(available)
        self._last_response = selected

        return selected

    def process_player_input(self, duck: "Duck", player_input: str, use_llm: bool = True) -> str:
        """
        Process player text input and generate a response.
        Uses LLM if available, otherwise falls back to templates.
        """
        # Try LLM first if enabled
        if use_llm:
            try:
                from dialogue.llm_chat import get_llm_chat
                llm = get_llm_chat()
                if llm.is_available():
                    llm_response = llm.generate_response(duck, player_input)
                    if llm_response:
                        self.add_to_history(player_input, llm_response)
                        return llm_response
            except Exception:
                pass  # Fall through to template responses

        # Fall back to template-based responses
        input_lower = player_input.lower().strip()

        # Detect intent and respond with personality
        if any(word in input_lower for word in ["hi", "hello", "hey", "greet"]):
            return self.get_greeting(duck)

        if any(word in input_lower for word in ["good", "nice", "love", "cute", "pretty"]):
            responses = [
                "*flattered wiggle* Oh STOP it! ...Actually, don't stop. Keep going. I'm listening.",
                "I KNOW, right?! Finally, someone with TASTE! *preens dramatically*",
                "*blushes* You think so? That's... that's really nice, actually. Don't tell anyone I said that.",
                "Flattery will get you EVERYWHERE. And by everywhere, I mean more time with me. Lucky you!",
            ]
            return random.choice(responses)

        if any(word in input_lower for word in ["bad", "dumb", "stupid", "ugly"]):
            if duck.is_derpy():
                responses = [
                    "...quack? *genuinely doesn't understand the insult* Is that a compliment? Thanks!",
                    "*blinks* Huh? What? I wasn't listening. Say something nice this time, maybe?",
                    "Words are just sounds, and sounds are just vibrations. I reject your vibrations! *waddles away*",
                ]
            else:
                responses = [
                    "*gasp* EXCUSE me?! The AUDACITY! I didn't waddle all this way to be INSULTED!",
                    "Oh, okay, cool. That's how it's gonna be? *remembers this forever*",
                    "*visibly offended* I will remember this. Ducks have LONG memories. We forget everything else, but we remember SLIGHTS.",
                ]
            return random.choice(responses)

        if any(word in input_lower for word in ["hungry", "food", "eat", "feed"]):
            if duck.needs.hunger < 50:
                return "YES!! Food! Please! IMMEDIATELY! I'm WASTING AWAY!! *dramatic collapse*"
            return "I could eat. I mean, I could ALWAYS eat. It's kind of my thing. *hopeful stare*"

        if any(word in input_lower for word in ["play", "fun", "game"]):
            return "Play?? *immediately alert* DID SOMEONE SAY PLAY?! I'm IN! What are we doing?! WHAT ARE WE DOING?!"

        if any(word in input_lower for word in ["tired", "sleep", "rest"]):
            if duck.needs.energy < 50:
                return "*massive yawn* You said the magic word... zzz... I mean, yes. Very tired. So tired. *yawn*"
            return "*bouncing* Tired?! Who's tired?! NOT ME! I could stay awake FOREVER! ...Probably!"

        if any(word in input_lower for word in ["name", "who are you", "called"]):
            return f"I'm {duck.name}! The one and only! Accept no substitutes! *proud puffing*"

        if "?" in input_lower:
            responses = [
                "*tilts head* Quack? That's a GREAT question. I have no idea. Next question!",
                "Hmm... *pretends to think* ...Nope, nothing. Brain empty. Only quacks.",
                "*confident nod* The answer is bread. Wait, what was the question?",
                "*squints* Is this a TEST?? I didn't STUDY! Give me a hint! ...Actually, don't. I'll wing it!",
                "You know what? I'm going to answer that with another question: Why?",
            ]
            if duck.is_derpy():
                responses.extend([
                    "*brain loading...* ...Error: thought not found. Try again later!",
                    "*forgot the question mid-thought* ...What were we talking about?",
                ])
            return random.choice(responses)

        # Default response
        return self.get_idle_thought(duck)

    def add_to_history(self, player_msg: str, duck_response: str):
        """Add an exchange to conversation history."""
        self._conversation_history.append((player_msg, duck_response))
        if len(self._conversation_history) > 20:
            self._conversation_history.pop(0)


# Global instance
conversation = ConversationSystem()
