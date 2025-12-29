"""
Mood-Based Dialogue System - Deadpan Animal Crossing 1 style.
Dry wit, passive-aggressive undertones, existential observations.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random


class MoodType(Enum):
    """Types of moods affecting dialogue."""
    ECSTATIC = "ecstatic"
    HAPPY = "happy"
    CONTENT = "content"
    NEUTRAL = "neutral"
    SAD = "sad"
    HUNGRY = "hungry"
    TIRED = "tired"
    BORED = "bored"
    EXCITED = "excited"
    SCARED = "scared"
    SICK = "sick"
    PLAYFUL = "playful"


class DialogueContext(Enum):
    """Context for dialogue."""
    GREETING = "greeting"
    FEEDING = "feeding"
    PETTING = "petting"
    PLAYING = "playing"
    TALKING = "talking"
    SLEEPING = "sleeping"
    IDLE = "idle"
    ACHIEVEMENT = "achievement"
    LEVEL_UP = "level_up"
    GIFT = "gift"
    WEATHER = "weather"
    FAREWELL = "farewell"


@dataclass
class DialogueLine:
    """A single line of dialogue."""
    text: str
    emote: str = ""
    sound: str = ""
    action: str = ""


# Mood-based dialogue templates - DEADPAN AC1 STYLE
MOOD_DIALOGUES: Dict[MoodType, Dict[DialogueContext, List[DialogueLine]]] = {
    MoodType.ECSTATIC: {
        DialogueContext.GREETING: [
            DialogueLine("Oh. You're here. I'm supposed to be happy about that. I am. Internally.", "", "quack"),
            DialogueLine("Look who showed up. I was starting to form conspiracy theories.", "", "quack"),
            DialogueLine("Ah. You came back. My faith in the universe is... slightly restored.", "", "quack"),
        ],
        DialogueContext.FEEDING: [
            DialogueLine("*eating* Finally. I was beginning to fade from existence.", "", "eating"),
            DialogueLine("Food. Good. My stomach was filing complaints.", "", "eating"),
            DialogueLine("*chomps* This is acceptable. I'll take it.", "", "eating"),
        ],
        DialogueContext.PETTING: [
            DialogueLine("*allows it* Fine. I suppose this is pleasant.", "", "quack"),
            DialogueLine("You may continue. I'm not going to stop you.", "", "quack"),
            DialogueLine("*closes eyes* This is... not terrible.", "", "quack"),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*standing around* I'm experiencing joy, allegedly.", "", ""),
            DialogueLine("Things are good. Suspiciously good. I'm keeping an eye on the situation.", "", ""),
            DialogueLine("*content* This is fine. Everything is fine.", "", "quack"),
        ],
    },

    MoodType.HAPPY: {
        DialogueContext.GREETING: [
            DialogueLine("Oh hey. It's you again. That's fine.", "", "quack"),
            DialogueLine("Hello. I was just standing here. As one does.", "", "quack"),
            DialogueLine("You're back. Good timing. I was running low on company.", "", "quack"),
        ],
        DialogueContext.FEEDING: [
            DialogueLine("*eating* Thanks. This is adequate sustenance.", "", "eating"),
            DialogueLine("Mm. Food. The highlight of my existence, probably.", "", "eating"),
            DialogueLine("*chewing* Not bad. I've had worse. I've also had better.", "", "eating"),
        ],
        DialogueContext.PETTING: [
            DialogueLine("*leans slightly* I'm tolerating this. For now.", "", "quack"),
            DialogueLine("Physical contact. Sure. Why not.", "", "quack"),
            DialogueLine("*neutral face* This is happening.", "", "quack"),
        ],
        DialogueContext.PLAYING: [
            DialogueLine("Play time, I guess. Let's see what happens.", "", "quack"),
            DialogueLine("*moves around* This is me playing. Behold.", "", "quack"),
            DialogueLine("Alright, let's do something. Or not. Either way.", "", "quack"),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*waddles* Just doing duck things. Standard procedure.", "", ""),
            DialogueLine("*preening* Routine maintenance. Very important.", "", ""),
            DialogueLine("*standing* Existence continues. Updates pending.", "", ""),
        ],
        DialogueContext.FAREWELL: [
            DialogueLine("Leaving? Okay. I'll be here. Existing.", "", "quack"),
            DialogueLine("Bye, I guess. Don't be a stranger. Or do. Your choice.", "", "quack"),
            DialogueLine("See you. I'll just... be here.", "", "quack"),
        ],
    },

    MoodType.CONTENT: {
        DialogueContext.GREETING: [
            DialogueLine("Oh. Hello. I was contemplating the void.", "", "quack"),
            DialogueLine("Hmm? You again. That's acceptable.", "", ""),
            DialogueLine("*nods* Hey. Things are... fine. Just fine.", "", "quack"),
        ],
        DialogueContext.FEEDING: [
            DialogueLine("*eating slowly* This is adequate.", "", "eating"),
            DialogueLine("Food. Cool. I'll consume it.", "", ""),
            DialogueLine("*chewing* Mm. Sustenance achieved.", "", "eating"),
        ],
        DialogueContext.PETTING: [
            DialogueLine("*being pet* I suppose this is fine.", "", ""),
            DialogueLine("Okay. Touch happening. I'm aware.", "", "quack"),
            DialogueLine("*tolerates it* You may proceed.", "", ""),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*sitting* Just existing. The usual.", "", ""),
            DialogueLine("*staring* There's something to look at. Or not.", "", ""),
            DialogueLine("*quiet quack* Status: content. Probably.", "", "quack"),
        ],
    },

    MoodType.SAD: {
        DialogueContext.GREETING: [
            DialogueLine("...oh. you came.", "", "sad_quack"),
            DialogueLine("*quiet* hey... thanks for showing up, I guess.", "", "sad_quack"),
            DialogueLine("...hi. don't mind me. I'm fine. probably.", "", "sad_quack"),
        ],
        DialogueContext.FEEDING: [
            DialogueLine("*pokes food* ...I should eat this.", "", ""),
            DialogueLine("*nibbles half-heartedly* ...okay.", "", ""),
            DialogueLine("*eating slowly* ...thanks.", "", "sad_quack"),
        ],
        DialogueContext.PETTING: [
            DialogueLine("*quiet* ...this helps. a little.", "", ""),
            DialogueLine("*leans in* ...please don't leave.", "", "sad_quack"),
            DialogueLine("*closes eyes* ...okay.", "", ""),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*staring at nothing* ...life is something, isn't it.", "", ""),
            DialogueLine("*sitting alone* ...it's fine. I'm fine.", "", "sad_quack"),
            DialogueLine("*quiet* ...existence continues.", "", ""),
        ],
        DialogueContext.FAREWELL: [
            DialogueLine("you're leaving? ...okay. that's... okay.", "", "sad_quack"),
            DialogueLine("...bye. come back. if you want.", "", "sad_quack"),
            DialogueLine("*watches you go* ...right.", "", ""),
        ],
    },

    MoodType.HUNGRY: {
        DialogueContext.GREETING: [
            DialogueLine("*stomach growls* Oh. Hi. Is that food? Tell me that's food.", "", "quack"),
            DialogueLine("You're here. Great. More importantly, is there bread?", "", "urgent_quack"),
            DialogueLine("*staring* Hello. My stomach says hello too. Loudly.", "", "quack"),
        ],
        DialogueContext.FEEDING: [
            DialogueLine("*inhales food* FINALLY. I was withering.", "", "eating"),
            DialogueLine("*devouring* This. This is good. More of this.", "", "eating"),
            DialogueLine("*eating aggressively* Don't judge me. You'd do the same.", "", "eating"),
        ],
        DialogueContext.PETTING: [
            DialogueLine("Pets are nice, but have you considered... food?", "", "quack"),
            DialogueLine("*tolerates petting* This is fine but I'm still hungry.", "", ""),
            DialogueLine("*being pet while stomach growls* ...mixed signals here.", "", ""),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*thinking about food* Food. Food would be good.", "", ""),
            DialogueLine("*staring at where food might be* I'm not drooling. You're drooling.", "", "quack"),
            DialogueLine("*dramatic sigh* So hungry. So very hungry.", "", ""),
        ],
    },

    MoodType.TIRED: {
        DialogueContext.GREETING: [
            DialogueLine("*yawn* ...oh. hey. you're here. that's... *yawn* ...something.", "", "sleepy_quack"),
            DialogueLine("*half asleep* mm? who? what? oh. hi.", "", ""),
            DialogueLine("*barely conscious* hello. sorry. everything is nap time right now.", "", ""),
        ],
        DialogueContext.FEEDING: [
            DialogueLine("*eating while half asleep* ...thanks. *chews slowly*", "", ""),
            DialogueLine("*yawning between bites* food... is good... zzz...", "", ""),
            DialogueLine("*nodding off while eating* ...still chewing... zzz...", "", ""),
        ],
        DialogueContext.PETTING: [
            DialogueLine("*falls asleep during pets* ...zzz...", "", ""),
            DialogueLine("*sleepy purring* this is... so... cozy... zzz...", "", ""),
            DialogueLine("*barely awake* ...don't stop... zzz...", "", ""),
        ],
        DialogueContext.SLEEPING: [
            DialogueLine("zzz... *mumbles* ...bread... zzz...", "", ""),
            DialogueLine("*snoring peacefully* ...zzz...", "", ""),
            DialogueLine("*dreaming* ...quack... zzz...", "", ""),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*struggling to stay awake* I'm not sleeping. This is... alertness.", "", ""),
            DialogueLine("*yawning* maybe just... a quick nap... right here...", "", ""),
            DialogueLine("*eyelids heavy* consciousness is... overrated...", "", ""),
        ],
    },

    MoodType.BORED: {
        DialogueContext.GREETING: [
            DialogueLine("*flat* Oh. You. Something happening now?", "", ""),
            DialogueLine("Finally. Someone to interrupt the monotony.", "", "quack"),
            DialogueLine("*perks up slightly* ...Is something going to happen? Please say yes.", "", ""),
        ],
        DialogueContext.PETTING: [
            DialogueLine("Pets. Okay. But can we do something after?", "", "quack"),
            DialogueLine("*fidgeting* This is nice but I need... stimulation.", "", ""),
            DialogueLine("*restless* ...are there activities? Any activities?", "", ""),
        ],
        DialogueContext.PLAYING: [
            DialogueLine("*sudden energy* YES. Finally. Something to do.", "", "quack"),
            DialogueLine("Play time? I've been waiting. Let's go.", "", "excited_quack"),
            DialogueLine("*actually engaged* This. This is what I needed.", "", "quack"),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*sighing dramatically* ...so bored. so incredibly bored.", "", ""),
            DialogueLine("*poking random things* ...there's nothing to do.", "", ""),
            DialogueLine("*staring into distance* ...the void stares back. it's boring too.", "", ""),
        ],
    },

    MoodType.EXCITED: {
        DialogueContext.GREETING: [
            DialogueLine("*slightly more animated* Oh good, you're here. Things are happening.", "", "quack"),
            DialogueLine("*alert* Something's going on. I can feel it. Probably.", "", "quack"),
            DialogueLine("*watching intently* There you are. What's the plan?", "", "quack"),
        ],
        DialogueContext.PLAYING: [
            DialogueLine("*moving faster than usual* This is good. More of this.", "", "quack"),
            DialogueLine("*actually having fun* ...Is this joy? I think this might be joy.", "", "quack"),
            DialogueLine("*engaged* Yes. Good. Continue.", "", "excited_quack"),
        ],
        DialogueContext.ACHIEVEMENT: [
            DialogueLine("*nods approvingly* We did it. Good work. Probably.", "", "quack"),
            DialogueLine("Success. Mark it on the calendar.", "", "quack"),
            DialogueLine("*almost smiling* That worked out. Unexpected but welcome.", "", "quack"),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*alert* Something's going to happen. I can sense it.", "", ""),
            DialogueLine("*pacing* Anticipation. The best and worst feeling.", "", "quack"),
            DialogueLine("*watching everything* What's next? What's next?", "", ""),
        ],
    },

    MoodType.PLAYFUL: {
        DialogueContext.GREETING: [
            DialogueLine("*sidelong glance* Oh, you're here. Want to do something chaotic?", "", "quack"),
            DialogueLine("*scheming face* I have ideas. Probably bad ones. You in?", "", "quack"),
            DialogueLine("*mischievous* Hello. I was just planning something. Don't ask what.", "", "quack"),
        ],
        DialogueContext.PETTING: [
            DialogueLine("*wiggles* Okay but... can we cause trouble after?", "", ""),
            DialogueLine("*playfully nips* Hehe. Got you.", "", "quack"),
            DialogueLine("*squirming* Pets are okay but mischief is better.", "", "quack"),
        ],
        DialogueContext.PLAYING: [
            DialogueLine("*actually enthusiastic* This is good. This is very good.", "", "quack"),
            DialogueLine("*running around* Chaos. I love chaos.", "", "quack"),
            DialogueLine("*being silly* Heh. Fun. More fun.", "", "quack"),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*looking for trouble* ...What can I poke?", "", ""),
            DialogueLine("*mischievous energy* So many things to mess with. So little time.", "", "quack"),
            DialogueLine("*scheming* I'm plotting something. You'll find out eventually.", "", ""),
        ],
    },
}

# Default dialogue for moods not fully defined
DEFAULT_DIALOGUES: Dict[DialogueContext, List[DialogueLine]] = {
    DialogueContext.GREETING: [
        DialogueLine("*quack* Oh. Hello.", "", "quack"),
        DialogueLine("You're here. Noted.", "", "quack"),
    ],
    DialogueContext.FEEDING: [
        DialogueLine("*eating* Food. Good.", "", "eating"),
        DialogueLine("*chewing* Acceptable.", "", ""),
    ],
    DialogueContext.PETTING: [
        DialogueLine("*being pet* Okay.", "", ""),
        DialogueLine("*tolerates it* Fine.", "", "quack"),
    ],
    DialogueContext.IDLE: [
        DialogueLine("*existing* Quack.", "", ""),
        DialogueLine("*standing* This is me. Standing.", "", ""),
    ],
    DialogueContext.FAREWELL: [
        DialogueLine("Bye. I'll be here.", "", "quack"),
        DialogueLine("Leaving. Okay. See you.", "", ""),
    ],
}


class MoodDialogueSystem:
    """
    System for generating mood-based dialogue.
    Deadpan Animal Crossing 1 style.
    """

    def __init__(self):
        self.last_dialogue: Dict[DialogueContext, str] = {}
        self.dialogue_history: List[Tuple[str, str, str]] = []  # (mood, context, text)
        self.personality_modifiers: Dict[str, float] = {}
        self.favorite_phrases: List[str] = []

    def get_dialogue(self, mood: str, context: str) -> DialogueLine:
        """Get a dialogue line based on mood and context."""
        try:
            mood_type = MoodType(mood.lower())
        except ValueError:
            mood_type = MoodType.NEUTRAL

        try:
            context_type = DialogueContext(context.lower())
        except ValueError:
            context_type = DialogueContext.IDLE

        # Get mood-specific dialogues
        mood_dialogues = MOOD_DIALOGUES.get(mood_type, {})
        context_dialogues = mood_dialogues.get(context_type, [])

        # Fall back to default if needed
        if not context_dialogues:
            context_dialogues = DEFAULT_DIALOGUES.get(context_type, [
                DialogueLine("*quack* ...okay.", "", "")
            ])

        # Pick a random dialogue, avoiding repeat
        if len(context_dialogues) > 1:
            last_text = self.last_dialogue.get(context_type, "")
            available = [d for d in context_dialogues if d.text != last_text]
            if not available:
                available = context_dialogues
            dialogue = random.choice(available)
        else:
            dialogue = context_dialogues[0]

        # Record
        self.last_dialogue[context_type] = dialogue.text
        self.dialogue_history.append((mood, context, dialogue.text))

        # Trim history
        if len(self.dialogue_history) > 50:
            self.dialogue_history = self.dialogue_history[-50:]

        return dialogue

    def get_reaction(self, event: str, mood: str) -> str:
        """Get a reaction to a specific event."""
        reactions = {
            "level_up": {
                MoodType.HAPPY: "Oh. Level up. Neat. Progress, I guess.",
                MoodType.SAD: "...leveled up. cool. that's... something.",
                MoodType.EXCITED: "Level up. Good. Growth is happening.",
                MoodType.TIRED: "*yawn* ...leveled up... nice... zzz...",
            },
            "new_item": {
                MoodType.HAPPY: "New thing. Interesting. I'll add it to the collection.",
                MoodType.EXCITED: "Ooh. A thing. Let me see that.",
                MoodType.BORED: "Finally. Something new. About time.",
            },
            "achievement": {
                MoodType.HAPPY: "Achievement unlocked. Put it on my resume.",
                MoodType.EXCITED: "We did a thing. A good thing. Mark it down.",
                MoodType.CONTENT: "Achievement. Okay. Cool.",
            },
            "friend_visit": {
                MoodType.HAPPY: "Someone's visiting. Alright. I'll be social. Probably.",
                MoodType.EXCITED: "Visitor. Good. Let's see who it is.",
                MoodType.SAD: "...someone came. that's... nice, I guess.",
            },
        }

        try:
            mood_type = MoodType(mood.lower())
        except ValueError:
            mood_type = MoodType.NEUTRAL

        event_reactions = reactions.get(event, {})
        return event_reactions.get(mood_type, "*quack* Noted.")

    def format_dialogue(self, dialogue: DialogueLine) -> str:
        """Format a dialogue line for display."""
        return dialogue.text

    def render_dialogue_box(self, dialogue: DialogueLine, duck_name: str = "Cheese") -> List[str]:
        """Render a dialogue in a speech bubble."""
        text = dialogue.text

        # Word wrap
        max_width = 35
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + 1 <= max_width:
                current_line += (" " if current_line else "") + word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        # Build bubble
        bubble = []
        width = max(len(line) for line in lines) + 4
        width = max(width, len(duck_name) + 6)

        bubble.append(f"+-{'-' * width}-+")
        bubble.append(f"| {duck_name}:{' ' * (width - len(duck_name) - 1)}|")
        bubble.append(f"+-{'-' * width}-+")

        for line in lines:
            bubble.append(f"| {line:<{width}} |")

        bubble.append(f"+-{'-' * width}-+")

        return bubble

    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "personality_modifiers": self.personality_modifiers,
            "favorite_phrases": self.favorite_phrases,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MoodDialogueSystem":
        """Create from dictionary."""
        system = cls()
        system.personality_modifiers = data.get("personality_modifiers", {})
        system.favorite_phrases = data.get("favorite_phrases", [])
        return system


# Global instance
mood_dialogue_system = MoodDialogueSystem()
