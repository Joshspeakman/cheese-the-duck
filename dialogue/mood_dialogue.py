"""
Mood-Based Dialogue System - Dialogue variations based on duck mood.
Provides context-aware responses and conversations.
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


# Mood-based dialogue templates
MOOD_DIALOGUES: Dict[MoodType, Dict[DialogueContext, List[DialogueLine]]] = {
    MoodType.ECSTATIC: {
        DialogueContext.GREETING: [
            DialogueLine("QUACK QUACK!!! You're here! Best day EVER!", "✨✨✨", "excited_quack"),
            DialogueLine("I've been waiting for you! Let's do EVERYTHING!", "🎉", "happy_quack"),
            DialogueLine("YAAAAY! My favorite human!", "💕💕💕", "excited_quack"),
        ],
        DialogueContext.FEEDING: [
            DialogueLine("FOOD! AMAZING FOOD! YOU'RE THE BEST!", "😍", "happy_quack"),
            DialogueLine("*gobbles happily* MORE PLEASE!", "🍞✨", "eating_sound"),
            DialogueLine("This is the GREATEST day! Thank you thank you!", "🌟", "happy_quack"),
        ],
        DialogueContext.PETTING: [
            DialogueLine("*vibrates with joy* Don't stop! Ever!", "💕💕💕", "happy_quack"),
            DialogueLine("I love you I love you I LOVE YOU!", "❤️", "soft_quack"),
            DialogueLine("*happy duck noises intensify*", "✨✨✨", "excited_quack"),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*bouncing around excitedly*", "🦆💨", ""),
            DialogueLine("Everything is WONDERFUL!", "🌈", "happy_quack"),
            DialogueLine("*zooming around in pure joy*", "💨💨", ""),
        ],
    },
    
    MoodType.HAPPY: {
        DialogueContext.GREETING: [
            DialogueLine("Quack! Oh, hello there, friend!", "😊", "happy_quack"),
            DialogueLine("Hi hi! I'm so happy to see you!", "💕", "soft_quack"),
            DialogueLine("What a wonderful day for some quality time!", "☀️", "happy_quack"),
        ],
        DialogueContext.FEEDING: [
            DialogueLine("Yum! Thank you for the delicious food!", "😋", "eating_sound"),
            DialogueLine("*happy munching* This is great!", "🍞", "eating_sound"),
            DialogueLine("Mmm, you always know what I like!", "💕", "soft_quack"),
        ],
        DialogueContext.PETTING: [
            DialogueLine("*leans into the pets* Ahhhh, that's nice...", "😌", "soft_quack"),
            DialogueLine("I love when you do that!", "💕", "happy_quack"),
            DialogueLine("*happy quacking*", "😊", "soft_quack"),
        ],
        DialogueContext.PLAYING: [
            DialogueLine("Let's play! This is so fun!", "🎮", "excited_quack"),
            DialogueLine("I love game time with you!", "🎲", "happy_quack"),
            DialogueLine("Woo! Let's gooo!", "🎉", "excited_quack"),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*waddles around contentedly*", "🦆", ""),
            DialogueLine("La la la~ What a nice day!", "🎵", "soft_quack"),
            DialogueLine("*preening feathers happily*", "✨", ""),
        ],
        DialogueContext.FAREWELL: [
            DialogueLine("Bye bye! Come back soon!", "👋", "soft_quack"),
            DialogueLine("See you later! Miss you already!", "💕", "soft_quack"),
            DialogueLine("Take care! I'll be here waiting!", "😊", "happy_quack"),
        ],
    },
    
    MoodType.CONTENT: {
        DialogueContext.GREETING: [
            DialogueLine("Oh, hello. Nice to see you.", "😊", "soft_quack"),
            DialogueLine("Quack. I was just relaxing.", "😌", ""),
            DialogueLine("Hey there. Life is good.", "☺️", "soft_quack"),
        ],
        DialogueContext.FEEDING: [
            DialogueLine("Thank you. *eats peacefully*", "🍞", "eating_sound"),
            DialogueLine("Mmm, this is nice.", "😊", ""),
            DialogueLine("Just what I needed.", "👍", "eating_sound"),
        ],
        DialogueContext.PETTING: [
            DialogueLine("*relaxed quacking*", "😌", "soft_quack"),
            DialogueLine("Mmm, that's nice...", "💕", ""),
            DialogueLine("*closes eyes contentedly*", "😌", ""),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*sitting peacefully*", "🦆", ""),
            DialogueLine("*watching the clouds*", "☁️", ""),
            DialogueLine("*gentle quacking*", "😌", "soft_quack"),
        ],
    },
    
    MoodType.SAD: {
        DialogueContext.GREETING: [
            DialogueLine("...oh, hi...", "😢", "sad_quack"),
            DialogueLine("*sad quack* ...you came...", "🥺", "sad_quack"),
            DialogueLine("I missed you... I was lonely...", "😔", "sad_quack"),
        ],
        DialogueContext.FEEDING: [
            DialogueLine("*nibbles half-heartedly*", "😔", ""),
            DialogueLine("I guess I should eat...", "🍞", ""),
            DialogueLine("Thanks... I suppose...", "😢", "sad_quack"),
        ],
        DialogueContext.PETTING: [
            DialogueLine("*snuggles close* Please don't leave...", "🥺", "sad_quack"),
            DialogueLine("...this helps a little...", "💔", "soft_quack"),
            DialogueLine("*quiet, sad sounds*", "😢", ""),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*staring at nothing*", "😔", ""),
            DialogueLine("*lonely quacking*", "🥺", "sad_quack"),
            DialogueLine("...sigh...", "💔", ""),
        ],
        DialogueContext.FAREWELL: [
            DialogueLine("You're leaving...? Oh...", "😢", "sad_quack"),
            DialogueLine("Please come back soon... please...", "🥺", "sad_quack"),
            DialogueLine("*watches you go with sad eyes*", "💔", ""),
        ],
    },
    
    MoodType.HUNGRY: {
        DialogueContext.GREETING: [
            DialogueLine("FOOD? Did you bring FOOD?!", "🤤", "urgent_quack"),
            DialogueLine("*stomach growling* ...h-hello...", "🍞❓", "sad_quack"),
            DialogueLine("Please tell me it's feeding time!", "😰", "urgent_quack"),
        ],
        DialogueContext.FEEDING: [
            DialogueLine("FINALLY! *devours food*", "😍", "excited_eating"),
            DialogueLine("YESYESYES! *gobbles*", "🍞✨", "happy_quack"),
            DialogueLine("*eating noises* SO GOOD!", "😋", "eating_sound"),
        ],
        DialogueContext.PETTING: [
            DialogueLine("Pets are nice but... food?", "🍞", "soft_quack"),
            DialogueLine("*stomach grumbles during pets*", "😅", ""),
            DialogueLine("Could we maybe... eat first?", "🤤", "soft_quack"),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*thinking about food*", "🍞💭", ""),
            DialogueLine("So... hungry...", "😩", "sad_quack"),
            DialogueLine("*stares at food bowl hopefully*", "🥺", ""),
        ],
    },
    
    MoodType.TIRED: {
        DialogueContext.GREETING: [
            DialogueLine("*yaaawn* ...oh, hi...", "😴", "sleepy_quack"),
            DialogueLine("Mmm... so... sleepy...", "💤", ""),
            DialogueLine("*blinks sleepily* ...huh?", "😪", ""),
        ],
        DialogueContext.FEEDING: [
            DialogueLine("*sleepy eating*", "😴🍞", ""),
            DialogueLine("Mmm... food... *yawn*", "💤", "eating_sound"),
            DialogueLine("*nodding off while eating*", "😪", ""),
        ],
        DialogueContext.PETTING: [
            DialogueLine("*falls asleep during pets*", "💤", ""),
            DialogueLine("Mmm... so cozy... zzz...", "😴", "soft_quack"),
            DialogueLine("*sleepy happy sounds*", "💤💕", ""),
        ],
        DialogueContext.SLEEPING: [
            DialogueLine("zzz... quack... zzz...", "💤", ""),
            DialogueLine("*peaceful snoring*", "😴", ""),
            DialogueLine("*mumbling in sleep* ...bread...", "💤🍞", ""),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*struggling to stay awake*", "😴", ""),
            DialogueLine("Maybe... just a little nap...", "💤", "sleepy_quack"),
            DialogueLine("*eyelids drooping*", "😪", ""),
        ],
    },
    
    MoodType.BORED: {
        DialogueContext.GREETING: [
            DialogueLine("Oh, you're here. Finally something to do.", "😐", ""),
            DialogueLine("I was SO bored! Entertain me!", "😤", "soft_quack"),
            DialogueLine("*perks up* Something happening?", "👀", ""),
        ],
        DialogueContext.PETTING: [
            DialogueLine("This is nice but... can we do something?", "😕", "soft_quack"),
            DialogueLine("*fidgeting* I wanna play!", "🎮", ""),
            DialogueLine("Pets are okay I guess...", "😐", ""),
        ],
        DialogueContext.PLAYING: [
            DialogueLine("FINALLY! Let's GO!", "🎮✨", "excited_quack"),
            DialogueLine("Yes yes yes! Game time!", "🎉", "happy_quack"),
            DialogueLine("I've been waiting for this!", "😍", "excited_quack"),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*sighing dramatically*", "😩", ""),
            DialogueLine("There's nothing to dooo...", "😔", "soft_quack"),
            DialogueLine("*poking random things*", "👆", ""),
        ],
    },
    
    MoodType.EXCITED: {
        DialogueContext.GREETING: [
            DialogueLine("QUACK QUACK! What are we doing?!", "✨", "excited_quack"),
            DialogueLine("I'm so ready for whatever!", "🎉", "excited_quack"),
            DialogueLine("Ooh ooh ooh! You're here!", "💕", "excited_quack"),
        ],
        DialogueContext.PLAYING: [
            DialogueLine("LET'S GOOO!!! *zooming*", "💨", "excited_quack"),
            DialogueLine("This is THE BEST!", "🌟", "happy_quack"),
            DialogueLine("*hyperactive quacking*", "🎮✨", "excited_quack"),
        ],
        DialogueContext.ACHIEVEMENT: [
            DialogueLine("WE DID IT!!! AMAZING!!!", "🏆✨", "excited_quack"),
            DialogueLine("I KNEW we could do it!", "🌟", "happy_quack"),
            DialogueLine("*celebration dancing*", "🎉", "excited_quack"),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*can't sit still*", "💨", ""),
            DialogueLine("What's next what's next?!", "✨", "excited_quack"),
            DialogueLine("*bouncing with anticipation*", "🦆💨", ""),
        ],
    },
    
    MoodType.PLAYFUL: {
        DialogueContext.GREETING: [
            DialogueLine("*playful quack* Wanna play?!", "🎮", "playful_quack"),
            DialogueLine("Catch me if you can! *runs*", "💨", "playful_quack"),
            DialogueLine("Tag! You're it! *waddles away*", "🦆💨", ""),
        ],
        DialogueContext.PETTING: [
            DialogueLine("*wiggles* Tickles! Hehehe!", "😆", "playful_quack"),
            DialogueLine("*playfully nips at fingers*", "😋", ""),
            DialogueLine("Pets OR... we could play!", "🎮", "playful_quack"),
        ],
        DialogueContext.PLAYING: [
            DialogueLine("Wheeeee! This is fun!", "🎮", "playful_quack"),
            DialogueLine("*silly duck noises*", "😝", "playful_quack"),
            DialogueLine("Again again again!", "🔄", "excited_quack"),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*making mischief*", "😏", ""),
            DialogueLine("*looking for something to play with*", "👀", ""),
            DialogueLine("*doing zoomies*", "🦆💨", "playful_quack"),
        ],
    },
}

# Default dialogue for moods not fully defined
DEFAULT_DIALOGUES: Dict[DialogueContext, List[DialogueLine]] = {
    DialogueContext.GREETING: [
        DialogueLine("Quack!", "🦆", "quack"),
        DialogueLine("Hello there!", "👋", "soft_quack"),
    ],
    DialogueContext.FEEDING: [
        DialogueLine("*eating*", "🍞", "eating_sound"),
        DialogueLine("Thanks for the food!", "😊", ""),
    ],
    DialogueContext.PETTING: [
        DialogueLine("*being pet*", "💕", ""),
        DialogueLine("Nice...", "😊", "soft_quack"),
    ],
    DialogueContext.IDLE: [
        DialogueLine("*quack*", "🦆", ""),
        DialogueLine("*waddles around*", "🦆", ""),
    ],
    DialogueContext.FAREWELL: [
        DialogueLine("Bye!", "👋", "soft_quack"),
        DialogueLine("See you!", "😊", ""),
    ],
}


class MoodDialogueSystem:
    """
    System for generating mood-based dialogue.
    """
    
    def __init__(self):
        self.last_dialogue: Dict[DialogueContext, str] = {}
        self.dialogue_history: List[Tuple[str, str, str]] = []  # (mood, context, text)
        self.personality_modifiers: Dict[str, float] = {}  # Personality affects dialogue
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
                DialogueLine("*quack*", "🦆", "")
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
                MoodType.HAPPY: "YAY! I leveled up! 🎉",
                MoodType.SAD: "Oh... I leveled up... I guess that's nice...",
                MoodType.EXCITED: "LEVEL UP!!! I'M AMAZING!!!",
                MoodType.TIRED: "*yawn* ...leveled up... nice... zzz...",
            },
            "new_item": {
                MoodType.HAPPY: "Ooh, something new! 🎁",
                MoodType.EXCITED: "NEW SHINY THING!!!",
                MoodType.BORED: "Finally, something interesting!",
            },
            "achievement": {
                MoodType.HAPPY: "I did it! So proud! 🏆",
                MoodType.EXCITED: "ACHIEVEMENT UNLOCKED!!! WOOO!!!",
                MoodType.CONTENT: "Oh, nice. An achievement.",
            },
            "friend_visit": {
                MoodType.HAPPY: "A friend is here! How wonderful!",
                MoodType.EXCITED: "FRIEND!!! FRIEND!!! FRIEND!!!",
                MoodType.SAD: "Oh... someone came to visit...",
            },
        }
        
        try:
            mood_type = MoodType(mood.lower())
        except ValueError:
            mood_type = MoodType.NEUTRAL
        
        event_reactions = reactions.get(event, {})
        return event_reactions.get(mood_type, "Quack!")
    
    def format_dialogue(self, dialogue: DialogueLine) -> str:
        """Format a dialogue line for display."""
        text = dialogue.text
        if dialogue.emote:
            text = f"{dialogue.emote} {text}"
        return text
    
    def render_dialogue_box(self, dialogue: DialogueLine, duck_name: str = "Cheese") -> List[str]:
        """Render a dialogue in a speech bubble."""
        text = dialogue.text
        emote = dialogue.emote
        
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
        
        bubble.append(f"╭{'─' * width}╮")
        bubble.append(f"│ {duck_name}: {emote:>{width - len(duck_name) - 3}}│")
        bubble.append(f"├{'─' * width}┤")
        
        for line in lines:
            bubble.append(f"│ {line:<{width - 2}} │")
        
        bubble.append(f"╰{'─' * width}╯")
        bubble.append("   ╲")
        bubble.append("    🦆")
        
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
