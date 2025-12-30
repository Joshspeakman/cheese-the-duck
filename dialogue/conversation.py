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
        ],
        "happy": [
            "Oh, hey. I was just thinking about... actually, I forgot. It's gone now. Thanks for that.",
            "*glances up* Ah. It's you. I suppose you'll want me to be all cheerful and duck-like.",
            "Hello. I've been doing important duck things. Like standing. And also sitting. Very productive.",
            "You're back. Good timing. I was about to have an existential crisis, but this works too.",
        ],
        "content": [
            "Hmm? Oh. Hello. I was just contemplating the void. Standard Tuesday stuff.",
            "*nods slowly* You again. That's fine. I was getting bored of my own company anyway.",
            "Oh, it's you. I'd say I'm surprised, but honestly, nothing surprises me anymore.",
            "Hey. Don't mind me. I'm just here, being a duck. Living the dream, allegedly.",
        ],
        "grumpy": [
            "*stares* What.",
            "Oh good. Company. Just what I wanted. *deadpan* Can you hear my enthusiasm.",
            "...Look, I'm not saying leave, but I'm also not saying stay. Do whatever.",
            "*long pause* ...Is there something you need, or are you just here to watch me suffer?",
        ],
        "sad": [
            "...oh. you came. that's... something, I guess.",
            "*quiet* hey. don't worry about me. I'm fine. everything's fine. *clearly not fine*",
            "...hi. sorry. I'm not great at being cheerful right now. or ever, really.",
            "*stares at ground* ...thanks for showing up. I think.",
        ],
        "miserable": [
            "...oh. it's you. or someone. does it matter.",
            "*hollow stare* existence is a peculiar thing, isn't it.",
            "...quack, I suppose. if I must.",
            "*lying down* ...I'm not ignoring you. I'm just... tired of being conscious.",
        ],
    },

    # Responses to being fed
    "feed": {
        "hungry": [
            "*eating* Oh thank goodness. I was starting to fade. Like a ghost, but with more dramatic quacking.",
            "Food. Finally. I was beginning to think this was some kind of experiment. 'How long can a duck survive on vibes alone?'",
            "*inhales food* Don't judge me. You'd do the same if you'd been standing here, slowly withering.",
            "*chomping* This is acceptable. I mean, it's food. Food is good. That's just science.",
        ],
        "normal": [
            "*takes a bite* Hmm. Not bad. Not amazing. Just... adequate. Like most things in life.",
            "Oh, a snack. Sure. I'll eat it. Not like I have anything else going on.",
            "*chewing thoughtfully* You know, I was going to say something profound, but then... food.",
            "*eating* Thanks, I guess. You're alright. For someone who just watches me eat.",
        ],
        "full": [
            "*stares at food* ...I'm already full. But also, it's right there. This is a moral dilemma.",
            "*pokes food* Listen. I appreciate the gesture. But if I eat any more, I'll become spherical.",
            "I can't possibly... *eats one bite* ...okay maybe just one. For science.",
            "*sighs* You're going to make me fat and immobile. Is that the plan? Am I being sabotaged?",
        ],
    },

    # Responses to playing
    "play": {
        "energetic": [
            "*waddles around* Okay, I'm playing. This is what playing looks like. Are you entertained?",
            "*runs in a small circle* Wheee. So much fun. Can you feel the excitement. I can't.",
            "*chasing nothing* Is this... is this what joy feels like? Unclear. I'll report back.",
            "*bouncing* Look at me go. A picture of athletic excellence. Please clap.",
        ],
        "normal": [
            "*half-hearted waddle* Okay, playtime. Let's see... I could run around, or I could stand here. Decisions.",
            "*moves slightly* There. I played. That counts. Don't fact-check me on that.",
            "*flaps once* That was a power move. You probably didn't even appreciate it.",
            "*looking around* What are we playing? I wasn't briefed on this. I need a memo.",
        ],
        "tired": [
            "*lies down* This is me playing. It's an interpretive game called 'Rest'. Very avant-garde.",
            "*yawns* I'll play... later. Put it on my calendar. Pencil it in. Actually, just erase it.",
            "*barely moves* Running... sounds exhausting just thinking about it. Can we play 'Nap' instead?",
            "*stationary* I'm playing. This is speed: zero. I'm winning by not moving. Strategy.",
        ],
    },

    # Responses to cleaning
    "clean": {
        "dirty": [
            "*in bath* Fine. I'll admit I was getting a bit... atmospheric. Happy now?",
            "*splashes half-heartedly* This is humiliating. Dignified. I meant dignified.",
            "*being cleaned* Yes yes, I know. I looked like a swamp cryptid. Message received.",
            "*shaking off* There. I'm clean. Or cleaner. Let's not set the bar too high.",
        ],
        "normal": [
            "*splish* Ah, bath time. The only socially acceptable time to be wet and miserable.",
            "*preening* I'm not saying I needed this, but I'm also not saying I didn't.",
            "*bathing* You know, some cultures consider this a spiritual experience. I consider it damp.",
            "*shakes off water* There. Hygiene achieved. Put it on my resume.",
        ],
        "clean": [
            "*offended* I JUST bathed. Do I look dirty to you? Don't answer that.",
            "*gestures at self* Behold. A clean duck. Rare. Majestic. Stop trying to wash me.",
            "I'm already pristine. This is unnecessary. But also... the water is kind of nice.",
            "*sighs* You're obsessed with cleanliness. It's a little concerning, honestly.",
        ],
    },

    # Responses to petting
    "pet": {
        "social": [
            "*reluctantly enjoying it* This is... acceptable. Don't tell anyone I said that.",
            "*leans in slightly* Fine. You may continue. I'm not going to stop you.",
            "*closes eyes* Okay. This is happening. I'm not mad about it.",
            "*soft quack* ...Look, I have a reputation to maintain. But also... don't stop.",
        ],
        "normal": [
            "*allows it* Hmm. Physical contact. Sure. Why not.",
            "*being pet* Is this what affection feels like? I'll have to consult my notes.",
            "*tolerates it* You're doing this for you, not for me. Just so we're clear.",
            "*sighs* Fine. Pet me. I don't care. *clearly cares*",
        ],
        "shy": [
            "*freezes* ...What are you doing. What is this. Why.",
            "*tense* I'm not used to this. Fair warning: I might panic. Or not. We'll see.",
            "*nervous* Is... is this normal? Do ducks normally get touched? I need data.",
            "*wary* Okay but if this is a trap, I'm going to be very disappointed.",
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
    ],
    "idle_clever": [
        "*calculating* If I position myself here... the sun will hit me at optimal angles. I'm a genius.",
        "*observing* Interesting. Very interesting. I have no idea what I'm looking at.",
        "You know, I've been thinking about the nature of existence. Then I got hungry and stopped.",
        "*smug* I figured something out today. I won't tell you what. It's need-to-know.",
        "*nodding sagely* They say knowledge is power. I say naps are power. Agree to disagree.",
    ],
    "idle_social": [
        "*staring at you* ...So. Are we just going to stand here, or...?",
        "*waddles closer* Hey. Hey. Hey. Are you ignoring me? You seem like you're ignoring me.",
        "*following* I'm not clingy. I just happen to be wherever you are. Coincidence.",
        "Pay attention to me. I'm right here. I'm reasonably adorable. Work with me.",
    ],
    "idle_shy": [
        "*hiding behind object* You can't see me. I'm invisible. Please respect my invisibility.",
        "*peeking out* ...Is it safe? Are there... others? *suspicious squint*",
        "*from a distance* I'm fine over here. Don't mind me. Pretend I don't exist.",
        "*quietly* I'll just... observe. From afar. Where it's safe. And lonely. But safe.",
    ],
    "idle_active": [
        "*pacing* We should be doing something. Anything. Standing still is a waste of perfectly good legs.",
        "*fidgeting* I have energy and nowhere to put it. This is a crisis. A low-key crisis.",
        "*walking in circles* Motion is life. Stillness is death. I read that somewhere. Or made it up.",
        "*restless* Okay but what if we... did something? Just a thought.",
    ],
    "idle_lazy": [
        "*lying down* I could move. Or I could not. The math checks out on 'not.'",
        "*yawning* Everything is nap time if you believe in yourself.",
        "*barely conscious* I'm resting my eyes. And also the rest of my body. Indefinitely.",
        "*horizontal* Vertical is overrated. Horizontal is where it's at.",
    ],

    # Reactions to events
    "event_scared": [
        "*deadpan* Oh no. Danger. How terrifying. *not moving*",
        "*monotone* I'm scared. Can you tell? I'm expressing fear. This is my fear face.",
        "*flat* Something happened. I should probably react. ...There. Reacted.",
    ],
    "event_curious": [
        "*squinting* What's that. I should investigate. Or not. Let's see how I feel.",
        "*poking thing* Hmm. It's a thing. Interesting thing. Could be dangerous. Only one way to find out.",
        "*staring* This is new. I have questions. Mostly 'can I eat it?' and 'will it hurt me?'",
    ],
    "event_happy": [
        "*slight smile* Oh. That's nice. I'm experiencing a positive emotion. Mark your calendars.",
        "*nods approvingly* Good. Good stuff happening. I approve of this development.",
        "*almost enthusiastic* Hey, that's actually great. I'm... dare I say... pleased.",
    ],

    # Growth stage reactions
    "growth_duckling": [
        "*tiny voice* Why is everything so big? Why am I so small? These are important questions.",
        "*wobbling* Walking is harder than it looks. No one warned me about this.",
        "*confused peeping* I'm new here. Please lower your expectations accordingly.",
    ],
    "growth_teen": [
        "*voice cracking* I'm NOT a baby. I'm practically an adult. I have... responsibilities. Probably.",
        "*sulking* Nobody understands me. Especially me. I don't understand me either.",
        "*dramatic* Everything is SO unfair. Why? I don't know. It just IS.",
    ],
    "growth_adult": [
        "*standing confidently* Behold: a fully formed duck. Impressive? Yes. Humble? Also yes.",
        "*looking around* I'm an adult now. I should probably know what I'm doing. ...I don't.",
        "*posing* These are premium feathers. Look at them. LOOK AT THEM.",
    ],
    "growth_elder": [
        "*wise nod* I've seen things. Many things. Mostly bread. Some water. A few concerning bugs.",
        "*reminiscing* Back in my day, we appreciated things. Like silence. And bread.",
        "*sage* Youth is wasted on the young. Wisdom is wasted on the old. Bread is wasted on no one.",
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
        Uses LLM if available, otherwise falls back to templates.
        
        Args:
            duck: The Duck instance
            player_input: What the player said
            use_llm: Whether to try using LLM
            memory_context: Optional context from duck's memory for richer responses
        """
        # Try LLM first if enabled
        if use_llm:
            try:
                from dialogue.llm_chat import get_llm_chat
                llm = get_llm_chat()
                if llm.is_available():
                    # Pass memory context to LLM for richer responses
                    llm_response = llm.generate_response(duck, player_input, memory_context=memory_context)
                    if llm_response:
                        self.add_to_history(player_input, llm_response)
                        return llm_response
                    # LLM returned None - log for debugging
                    import logging
                    logging.debug(f"LLM returned None. Last error: {llm.get_last_error()}")
            except Exception as e:
                # Log the exception for debugging
                import logging
                logging.debug(f"LLM exception: {e}")

        # Fall back to template-based responses
        input_lower = player_input.lower().strip()

        # Detect intent and respond with personality
        if any(word in input_lower for word in ["hi", "hello", "hey", "greet"]):
            return self.get_greeting(duck)

        if any(word in input_lower for word in ["good", "nice", "love", "cute", "pretty"]):
            responses = [
                "*blinks* Was that a compliment? I'm going to assume it was. Thank you. I think.",
                "Oh. Flattery. I mean, you're not wrong, but still. Suspicious.",
                "*slight head tilt* Are you being nice to me? What's the catch?",
                "That's... unexpectedly kind. I don't know how to process this. Give me a moment.",
            ]
            return random.choice(responses)

        if any(word in input_lower for word in ["bad", "dumb", "stupid", "ugly"]):
            if duck.is_derpy():
                responses = [
                    "*blinks slowly* ...What? I wasn't listening. Could you repeat that? Actually, don't.",
                    "Words are just sounds. I choose not to assign meaning to those particular sounds.",
                    "*tilts head* I don't understand, but I feel like I shouldn't. Moving on.",
                ]
            else:
                responses = [
                    "*stares* Okay. Cool. I'll remember that. Forever. No pressure.",
                    "Noted. Adding you to my list of people who owe me an apology. It's a long list.",
                    "*deadpan* Wow. That hurt. Can you see how hurt I am? *no visible emotion*",
                ]
            return random.choice(responses)

        if any(word in input_lower for word in ["hungry", "food", "eat", "feed"]):
            if duck.needs.hunger < 50:
                return "Food would be nice. I'm not begging. Just... strongly suggesting. With my eyes."
            return "I could eat. I'm always at least 15% hungry. It's a lifestyle."

        if any(word in input_lower for word in ["play", "fun", "game"]):
            return "Play? Sure. I'll move around or whatever. Don't expect cartwheels."

        if any(word in input_lower for word in ["tired", "sleep", "rest"]):
            if duck.needs.energy < 50:
                return "Sleep sounds good. I've been awake for... *checks internal clock* ...too long."
            return "I'm not tired. But I could become tired. It wouldn't take much."

        if any(word in input_lower for word in ["name", "who are you", "called"]):
            return f"I'm {duck.name}. That's my name. I didn't choose it, but I've made my peace with it."

        if "?" in input_lower:
            responses = [
                "*tilts head* That's a question. I heard the question mark. Answer pending.",
                "Hmm. *pretends to think* ...The answer is probably bread. Everything is bread eventually.",
                "*stares* I could tell you, but then I'd have to... actually, I just don't know.",
                "Good question. Wrong duck. Or maybe right duck. I'll get back to you. Maybe.",
            ]
            if duck.is_derpy():
                responses.extend([
                    "*brain.exe has stopped responding* ...What were we talking about?",
                    "I started thinking about that, then I thought about something else. What was it? Gone now.",
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
