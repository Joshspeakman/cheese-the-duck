"""
Visitor Dialogue System - Comprehensive dialogue trees for duck friends.
Each personality has dialogue for each friendship level that progresses naturally.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random


# =============================================================================
# VISITOR WEATHER COMMENTS - Weather-specific comments by personality
# =============================================================================

VISITOR_WEATHER_COMMENTS: Dict[str, Dict[str, List[str]]] = {
    "adventurous": {
        "sunny": [
            "Perfect weather for an adventure! The sun is calling!",
            "*checks compass* Excellent conditions for exploration!",
            "Sunny skies mean new trails to discover!",
        ],
        "rainy": [
            "Rain never stopped a TRUE adventurer! Let's go!",
            "I once crossed a monsoon. This is nothing!",
            "*excited* PUDDLES! Nature's obstacle course!",
        ],
        "stormy": [
            "*eyes wide* Now THIS is weather! EXCITING!",
            "Storms make everything more dramatic!",
            "*watches lightning* The universe is putting on a SHOW!",
        ],
        "snowy": [
            "Snow means winter expeditions! I'm SO ready!",
            "I've trekked through worse blizzards. This is cozy!",
            "*catching snowflakes* Perfect for tracking!",
        ],
        "windy": [
            "The wind guides my adventures! Which way, wind?",
            "*feathers blown back* FREEDOM feels like this!",
            "Wind at our backs! Let's GO!",
        ],
        "foggy": [
            "Mysterious! Could be ANYTHING out there!",
            "Fog makes everything feel like a quest!",
            "*squinting* Adventure awaits beyond the mist!",
        ],
    },
    "scholarly": {
        "sunny": [
            "Optimal photosynthetic conditions. Fascinating.",
            "The sun provides excellent reading light!",
            "*adjusts glasses* Clear skies. Perfect for observations.",
        ],
        "rainy": [
            "Rain increases ambient humidity by... *calculates*",
            "Did you know rain forms around dust particles?",
            "*taking notes* Precipitation patterns are remarkable!",
        ],
        "stormy": [
            "The electrical potential in those clouds is IMMENSE!",
            "Storm systems are nature's most complex phenomena!",
            "*fascinated* Each lightning bolt is 30,000 kelvin!",
        ],
        "snowy": [
            "Each snowflake IS unique. I've verified this.",
            "Snow crystals form in fascinating hexagonal patterns!",
            "*examining snowflake* Six-fold symmetry! Beautiful!",
        ],
        "windy": [
            "Wind is simply differential air pressure. Elegantly simple.",
            "The Coriolis effect influences this breeze!",
            "*hair blown* Aerodynamics in action!",
        ],
        "foggy": [
            "Fog is merely ground-level stratus clouds. Technically.",
            "Visibility reduced to approximately... *squints* ...limited.",
            "Water vapor condensation. Quite poetic, actually.",
        ],
    },
    "artistic": {
        "sunny": [
            "*gestures dramatically* The LIGHT! The SHADOWS! Art!",
            "Golden rays inspire golden creativity!",
            "The sun paints everything in warm tones!",
        ],
        "rainy": [
            "Rain creates the most MELANCHOLIC aesthetic!",
            "*spreading wings* The drama! The romance!",
            "Everything glistens! Nature's rhinestones!",
        ],
        "stormy": [
            "DRAMATIC! INTENSE! INSPIRED!",
            "*poses in wind* The perfect backdrop for art!",
            "Such POWERFUL energy! I must create!",
        ],
        "snowy": [
            "A blank canvas! The world is ART waiting to happen!",
            "*twirling* Pure white beauty! Pristine!",
            "Snow muffles sound... so peaceful... so inspiring...",
        ],
        "windy": [
            "*feathers flowing* I am become SCULPTURE!",
            "The wind creates such dynamic MOVEMENT!",
            "DRAMATIC! The wind is an artist too!",
        ],
        "foggy": [
            "The atmosphere is MOODY! I love it!",
            "*mysterious pose* Ethereal. Haunting. Perfect.",
            "Fog turns everything into impressionism!",
        ],
    },
    "playful": {
        "sunny": [
            "YAY! Sunny! Let's play EVERYTHING!",
            "*bouncing* The sun wants us to have FUN!",
            "Perfect day for shenanigans!",
        ],
        "rainy": [
            "PUDDLES! PUDDLES EVERYWHERE! *splashing*",
            "Rain is just nature's sprinkler system!",
            "*spinning* SPLASHY SPLASH SPLASH!",
        ],
        "stormy": [
            "*hides* The sky is being LOUD. Make it stop?",
            "Thunder is just sky farts. Right? RIGHT?",
            "*nervous but excited* SCARY but also COOL!",
        ],
        "snowy": [
            "SNOWBALL FIGHT! I mean... SNOWBALL CUDDLE!",
            "*diving into snow* I'm a snow duck now!",
            "Let's make snow angels! Or snow DUCKS!",
        ],
        "windy": [
            "*spreads wings* I can ALMOST fly! Almost!",
            "WHEEEEE! The wind is playing with me!",
            "*spinning* I'm a feathery windmill!",
        ],
        "foggy": [
            "Spooky! Let's play hide and seek!",
            "*disappears into fog* Can you find me??",
            "The fog is trying to play! It's hiding everything!",
        ],
    },
    "mysterious": {
        "sunny": [
            "The sun reveals what darkness conceals...",
            "*squints* Too bright. I prefer shadows.",
            "Even light casts darkness somewhere...",
        ],
        "rainy": [
            "The sky weeps. I understand.",
            "Rain washes away secrets... or hides them.",
            "*gazes at puddles* Reflections of other worlds...",
        ],
        "stormy": [
            "The storm and I have an... understanding.",
            "*unfazed by thunder* We've met before.",
            "Such weather reveals true nature...",
        ],
        "snowy": [
            "Snow covers all tracks... how convenient.",
            "*watching snowfall* Each flake carries a secret.",
            "The silence of snow... it speaks volumes.",
        ],
        "windy": [
            "The wind whispers things... dark things...",
            "*listening* Do you hear it too?",
            "Ancient messages on the breeze...",
        ],
        "foggy": [
            "*emerges from fog* My element.",
            "Fog hides many mysteries. Including me.",
            "The veil between worlds is thin today...",
        ],
    },
    "generous": {
        "sunny": [
            "Sunny days deserve extra gifts!",
            "*handing out treats* The sun smiles, so should we!",
            "Perfect weather for sharing joy!",
        ],
        "rainy": [
            "I brought extra! In case you got wet!",
            "*offers umbrella* Rain can't dampen generosity!",
            "Here! Something to warm you up!",
        ],
        "stormy": [
            "Stay safe! Here's something to help!",
            "*worried* Do you need anything? I have extras!",
            "Storms mean we stick together!",
        ],
        "snowy": [
            "*bundled up* I brought you something warm!",
            "Snow days mean hot cocoa gifts!",
            "Here! To keep you cozy!",
        ],
        "windy": [
            "*holding onto things* Don't let the gifts blow away!",
            "Windy days need extra cheer!",
            "I brought something stable. Unlike the weather!",
        ],
        "foggy": [
            "Hard to see, but I found you anyway! With gifts!",
            "*emerges from fog* Surprise! It's gift time!",
            "Fog can't hide my generosity!",
        ],
    },
    "foodie": {
        "sunny": [
            "Perfect weather for a picnic! Did you bring snacks?",
            "The sun makes everything taste better!",
            "*sniffing* I smell... POSSIBILITIES.",
        ],
        "rainy": [
            "Rain means comfort food time!",
            "Wet weather, warm snacks. Perfect combo!",
            "*excited* Raindrops make everything taste fresh!",
        ],
        "stormy": [
            "Storm baking! The BEST kind of baking!",
            "*cozy* Perfect weather for hot soup!",
            "Thunder? That's the universe's tummy rumbling!",
        ],
        "snowy": [
            "Cold weather means hot food! PERFECT!",
            "*making snow cones* Nature provides!",
            "Winter is soup season. All soup. Always.",
        ],
        "windy": [
            "Wind-blown snacks are still snacks!",
            "*chasing leaves* Wait, those aren't food!",
            "The wind brings new smells! New FLAVORS!",
        ],
        "foggy": [
            "Can't see but I can SMELL everything!",
            "Misty mornings, perfect breakfast vibes!",
            "*sniffing* My nose sees through fog!",
        ],
    },
    "athletic": {
        "sunny": [
            "PERFECT training weather! Let's GO!",
            "*stretching* The sun energizes my workout!",
            "Peak conditions for peak performance!",
        ],
        "rainy": [
            "Rain is just nature's sweat! Keep pushing!",
            "*running in rain* REFRESHING!",
            "Wet feathers mean harder workout! GAINS!",
        ],
        "stormy": [
            "*pumped* EXTREME weather! EXTREME training!",
            "Storm drills! Nature's intensity training!",
            "Lightning reflexes! Get it? LIGHTNING?",
        ],
        "snowy": [
            "Cold weather burns MORE calories!",
            "*running in snow* RESISTANCE training!",
            "Snow sports time! Race you to that drift!",
        ],
        "windy": [
            "*running into wind* CARDIO INTENSIFIES!",
            "Wind resistance! Free gym membership!",
            "The wind is my sparring partner today!",
        ],
        "foggy": [
            "Training in limited visibility! SKILL BUILDER!",
            "*jogging* Can't see? Run ANYWAY!",
            "Fog is just the world making training harder!",
        ],
    },
}


# Import base types from dialogue_base to avoid circular imports
from dialogue.dialogue_base import ConversationPhase, DialogueLine, DIALOGUE_TREES


@dataclass 
class ConversationState:
    """Tracks the state of the current conversation."""
    phase: ConversationPhase = ConversationPhase.GREETING
    lines_said: List[str] = field(default_factory=list)
    topics_discussed: List[str] = field(default_factory=list)
    dialogue_index: int = 0
    visit_count: int = 1
    

# Friendship level order for comparisons
FRIENDSHIP_ORDER = ["stranger", "acquaintance", "friend", "close_friend", "best_friend"]


def friendship_meets_minimum(current: str, minimum: str) -> bool:
    """Check if current friendship level meets the minimum requirement."""
    current_idx = FRIENDSHIP_ORDER.index(current) if current in FRIENDSHIP_ORDER else 0
    min_idx = FRIENDSHIP_ORDER.index(minimum) if minimum in FRIENDSHIP_ORDER else 0
    return current_idx >= min_idx


class VisitorDialogueManager:
    """Manages dialogue for a visitor during their visit."""
    
    def __init__(self):
        self.state = ConversationState()
        self.personality: str = "adventurous"
        self.friendship_level: str = "stranger"
        self.friend_name: str = "Friend"
        self.unlocked_topics: set = set()
        self.visit_number: int = 1
        # NEW: Memory for tracking conversation history
        self.conversation_topics: List[str] = []  # What we've discussed before
        self.shared_experiences: List[str] = []  # What we've done together
        self.last_conversation_summary: str = ""  # What we talked about last time
        
    def start_visit(self, personality: str, friendship_level: str, 
                    friend_name: str, visit_number: int, unlocked_topics: set = None,
                    conversation_topics: List[str] = None, shared_experiences: List[str] = None,
                    last_conversation_summary: str = ""):
        """Initialize for a new visit."""
        self.state = ConversationState()
        self.state.phase = ConversationPhase.GREETING
        self.personality = personality.lower()
        self.friendship_level = friendship_level.lower().replace(" ", "_")
        self.friend_name = friend_name
        self.visit_number = visit_number
        self.unlocked_topics = unlocked_topics or set()
        self.state.visit_count = visit_number
        # Store memory
        self.conversation_topics = conversation_topics or []
        self.shared_experiences = shared_experiences or []
        self.last_conversation_summary = last_conversation_summary
        
    def get_next_dialogue(self, duck_name: str = "friend") -> Optional[str]:
        """Get the next line of dialogue based on current state."""
        dialogue_tree = DIALOGUE_TREES.get(self.personality, {})
        
        # Special handling for greetings when we've met before
        if self.state.phase == ConversationPhase.GREETING and self.visit_number > 1:
            returning_greeting = self._get_returning_greeting(duck_name)
            if returning_greeting:
                self.state.lines_said.append(returning_greeting)
                return returning_greeting
        
        phase_dialogue = dialogue_tree.get(self.state.phase.value, [])
        
        # Filter to lines we can say
        available = []
        for line in phase_dialogue:
            # Check friendship requirement
            if not friendship_meets_minimum(self.friendship_level, line.friendship_min):
                continue
            # Check if already said this visit
            if line.once_per_visit and line.text in self.state.lines_said:
                continue
            # Check topic requirements
            if line.requires_topic and line.requires_topic not in self.unlocked_topics:
                continue
            available.append(line)
        
        if not available:
            # Move to next phase
            return self._advance_phase(duck_name)
        
        # Pick a line (weighted toward ones not said yet)
        unsaid = [l for l in available if l.text not in self.state.lines_said]
        if unsaid:
            line = random.choice(unsaid)
        else:
            line = random.choice(available)
        
        # Record that we said it
        self.state.lines_said.append(line.text)
        
        # Handle topic unlocking
        if line.unlocks_topic:
            self.unlocked_topics.add(line.unlocks_topic)
            
        # Format and return
        text = line.text.format(duck=duck_name, name=self.friend_name)
        return f"{self.friend_name}: {text}"
    
    def _advance_phase(self, duck_name: str) -> Optional[str]:
        """Move to the next conversation phase."""
        phase_order = [
            ConversationPhase.GREETING,
            ConversationPhase.OPENING,
            ConversationPhase.MAIN,
            ConversationPhase.STORY,
            ConversationPhase.PERSONAL,
            ConversationPhase.ACTIVITY,
            ConversationPhase.CLOSING,
            ConversationPhase.FAREWELL,
        ]
        
        current_idx = phase_order.index(self.state.phase)
        
        # Skip PERSONAL phase if not close enough friends
        if current_idx < len(phase_order) - 1:
            next_phase = phase_order[current_idx + 1]
            if next_phase == ConversationPhase.PERSONAL:
                if not friendship_meets_minimum(self.friendship_level, "friend"):
                    current_idx += 1  # Skip personal
            if next_phase == ConversationPhase.STORY:
                if not friendship_meets_minimum(self.friendship_level, "acquaintance"):
                    current_idx += 1  # Skip story for strangers
        
        if current_idx >= len(phase_order) - 1:
            return None  # Conversation over
            
        self.state.phase = phase_order[current_idx + 1]
        self.state.dialogue_index = 0
        
        # Get first line of new phase
        return self.get_next_dialogue(duck_name)
    
    def is_conversation_over(self) -> bool:
        """Check if the conversation has ended."""
        return self.state.phase == ConversationPhase.FAREWELL and len(self.state.lines_said) > 5
    
    def _get_returning_greeting(self, duck_name: str) -> Optional[str]:
        """Get a special greeting for returning visitors that references past visits."""
        import random
        
        # Only use this sometimes to add variety
        if random.random() > 0.7:
            return None
        
        greetings = []
        
        # Reference shared experiences
        if self.shared_experiences:
            recent_exp = self.shared_experiences[-1] if self.shared_experiences else None
            exp_greetings = {
                "adventurous": [
                    f"*arrives* {duck_name}! Remember when we {recent_exp}? Still thinking about that.",
                    f"Back again! That {recent_exp} thing we did... I've told everyone.",
                    f"*waves* {duck_name}! So about that {recent_exp}... any more adventures planned?",
                ],
                "scholarly": [
                    f"*adjusts glasses* Ah, {duck_name}! I've been analyzing our {recent_exp} experience.",
                    f"{duck_name}! I documented everything from when we {recent_exp}. Fascinating data.",
                    f"*opens notebook* Our {recent_exp}... I have follow-up questions.",
                ],
                "artistic": [
                    f"*twirls* {duck_name}! That {recent_exp}... it INSPIRED me!",
                    f"There you are! I painted a mural about when we {recent_exp}.",
                    f"*gestures dramatically* {duck_name}! Our {recent_exp} was pure art!",
                ],
                "playful": [
                    f"*bounces* {duck_name}! {duck_name}! That {recent_exp} was SO FUN!",
                    f"HI AGAIN! Remember {recent_exp}? Let's do that AGAIN!",
                    f"*giggles* Our {recent_exp}... best day EVER! Well, second best. Today could be better!",
                ],
                "mysterious": [
                    f"*appears* {duck_name}... The stars aligned again. Like when we {recent_exp}...",
                    f"Our {recent_exp}... the spirits still speak of it.",
                    f"*cryptic nod* Fate brought me back. Perhaps to recreate our {recent_exp}...",
                ],
                "generous": [
                    f"*hugs* {duck_name}! I've thought about our {recent_exp} every day!",
                    f"There's my favorite friend! That {recent_exp}... I brought something to celebrate!",
                    f"*beams* Remember our {recent_exp}? Made me so happy!",
                ],
                "foodie": [
                    f"*sniffs* {duck_name}! That {recent_exp}... but more importantly, what's for lunch?",
                    f"Back for more! That {recent_exp} worked up quite an appetite.",
                    f"*belly rumbles* {duck_name}! After that {recent_exp}, I dreamed about food here.",
                ],
                "athletic": [
                    f"*jogs over* {duck_name}! Ready to top our {recent_exp}?",
                    f"Champion! That {recent_exp}... let's go bigger!",
                    f"*stretches* Our {recent_exp}... good training. Let's level up!",
                ],
            }
            if self.personality in exp_greetings and recent_exp:
                greetings.extend(exp_greetings[self.personality])
        
        # Reference visit count
        if self.visit_number > 3:
            count_greetings = {
                "adventurous": [
                    f"*arrives* Visit number {self.visit_number}. I've been counting. Don't judge me, {duck_name}.",
                    f"{duck_name}! I keep coming back. This place is on all my maps now.",
                ],
                "scholarly": [
                    f"*adjusts glasses* Visit {self.visit_number}, {duck_name}. I'm collecting data.",
                    f"{duck_name}! My studies bring me back. You're a fascinating subject.",
                ],
                "artistic": [
                    f"*dramatically* {duck_name}! My muse calls me back again!",
                    f"Visit {self.visit_number}! Each one more inspiring than the last!",
                ],
                "playful": [
                    f"*spins* {duck_name}! I missed you SO MUCH! Again!",
                    f"HIII! I can't stay away! This is too fun!",
                ],
                "mysterious": [
                    f"*appears* We meet again, {duck_name}. As foretold.",
                    f"The threads of fate keep weaving us together...",
                ],
                "generous": [
                    f"*waves excitedly* My dear {duck_name}! I couldn't stay away!",
                    f"Back again with gifts! You deserve ALL the visits!",
                ],
                "foodie": [
                    f"*sniffs air* {duck_name}! The crumbs here... I dream about them.",
                    f"I keep coming back. Your pond has the BEST food!",
                ],
                "athletic": [
                    f"*runs in* Training partner! Ready for round {self.visit_number}?",
                    f"{duck_name}! Our workouts are the highlight of my week!",
                ],
            }
            if self.personality in count_greetings:
                greetings.extend(count_greetings[self.personality])
        
        # Pick one if we have any
        if greetings:
            text = random.choice(greetings)
            return f"{self.friend_name}: {text}"
        
        return None
    
    def get_weather_comment(self, weather_type: str) -> Optional[str]:
        """Get a weather-specific comment based on personality and current weather."""
        if not weather_type:
            return None
        
        # Normalize weather type to match our comment keys
        weather_key = weather_type.lower()
        
        # Map specific weather types to broader categories for comments
        weather_mapping = {
            # Rain variants
            "drizzle": "rainy",
            "heavy_rain": "rainy", 
            "spring_showers": "rainy",
            "thunderstorm": "stormy",
            "summer_storm": "stormy",
            "storm": "stormy",
            # Snow variants
            "light_snow": "snowy",
            "heavy_snow": "snowy",
            "blizzard": "snowy",
            "snow_flurries": "snowy",
            "frost": "snowy",
            "sleet": "snowy",
            "hail": "stormy",
            "ice_storm": "stormy",
            # Other variants
            "partly_cloudy": "sunny",
            "cloudy": "foggy",
            "overcast": "foggy",
            "misty": "foggy",
            "breezy": "windy",
            "leaf_storm": "windy",
            "warm_breeze": "sunny",
            "crisp": "sunny",
            "golden_hour": "sunny",
            "perfect_day": "sunny",
            "balmy_evening": "sunny",
            "scorching": "sunny",
            "heat_wave": "sunny",
            "humid": "sunny",
            "muggy": "sunny",
            "dewy_morning": "foggy",
            "pollen_drift": "windy",
            "aurora": "snowy",
            "meteor_shower": "sunny",
            "double_rainbow": "rainy",
            "rainbow": "rainy",
        }
        
        # Get the mapped key or use the original
        mapped_key = weather_mapping.get(weather_key, weather_key)
        
        # Get personality comments
        personality_comments = VISITOR_WEATHER_COMMENTS.get(self.personality, {})
        weather_comments = personality_comments.get(mapped_key, [])
        
        if weather_comments:
            comment = random.choice(weather_comments)
            return f"{self.friend_name}: {comment}"
        
        return None
    
    def get_farewell(self, duck_name: str) -> str:
        """Get a farewell message."""
        self.state.phase = ConversationPhase.FAREWELL
        return self.get_next_dialogue(duck_name) or f"{self.friend_name}: Bye, {duck_name}!"


# ============================================================================
# DIALOGUE TREES BY PERSONALITY
# Each personality has dialogue organized by phase and friendship level
# DIALOGUE_TREES is imported from dialogue_base to avoid circular imports
# ============================================================================

# Import personality-specific dialogue - each file populates DIALOGUE_TREES when imported
from dialogue.dialogue_adventurous import ADVENTUROUS_DIALOGUE
from dialogue.dialogue_scholarly import SCHOLARLY_DIALOGUE
from dialogue.dialogue_artistic import ARTISTIC_DIALOGUE
from dialogue.dialogue_playful import PLAYFUL_DIALOGUE
from dialogue.dialogue_mysterious import MYSTERIOUS_DIALOGUE
from dialogue.dialogue_generous import GENEROUS_DIALOGUE
from dialogue.dialogue_foodie import FOODIE_DIALOGUE
from dialogue.dialogue_athletic import ATHLETIC_DIALOGUE


# Verify all personalities are loaded
def get_available_personalities() -> list:
    """Return list of personalities with dialogue trees."""
    return list(DIALOGUE_TREES.keys())


def count_dialogue_lines(personality: str) -> int:
    """Count total dialogue lines for a personality."""
    if personality not in DIALOGUE_TREES:
        return 0
    tree = DIALOGUE_TREES[personality]
    return sum(len(lines) for lines in tree.values())
