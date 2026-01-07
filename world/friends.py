"""
Duck Friends System - Visiting ducks, friendship levels, and social interactions.
Includes visitor events, gift exchanges, and duck personalities.
"""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random
import time


class FriendshipLevel(Enum):
    """Friendship tier with visiting ducks."""
    STRANGER = "stranger"
    ACQUAINTANCE = "acquaintance"
    FRIEND = "friend"
    CLOSE_FRIEND = "close_friend"
    BEST_FRIEND = "best_friend"


class DuckPersonalityType(Enum):
    """Personality archetypes for visitor ducks."""
    ADVENTUROUS = "adventurous"
    SCHOLARLY = "scholarly"
    ARTISTIC = "artistic"
    PLAYFUL = "playful"
    MYSTERIOUS = "mysterious"
    GENEROUS = "generous"
    FOODIE = "foodie"
    ATHLETIC = "athletic"


# Visitor duck appearances
DUCK_APPEARANCES = {
    "adventurous": {"color": "tan", "accessory": "explorer_hat", "scarf": "green"},
    "scholarly": {"color": "gray", "accessory": "glasses", "scarf": "blue"},
    "artistic": {"color": "white", "accessory": "beret", "scarf": "rainbow"},
    "playful": {"color": "yellow", "accessory": "propeller_hat", "scarf": "red"},
    "mysterious": {"color": "black", "accessory": "mask", "scarf": "purple"},
    "generous": {"color": "golden", "accessory": "bow_tie", "scarf": "pink"},
    "foodie": {"color": "orange", "accessory": "chef_hat", "scarf": "white"},
    "athletic": {"color": "brown", "accessory": "headband", "scarf": "orange"},
}

# Visitor NPC ASCII art by personality (facing left, toward Cheese)
# Option A: Cute Round Style
VISITOR_ASCII_ART = {
    "adventurous": {
        "idle": [
            "   /^\\  ",
            "  (o.o) ",
            "  /)_)\\>",
            "   \" \"~]",
        ],
        "waddle": [
            "   /^\\  ",
            "  (o.o) ",
            "  /)_)\\>",
            "  \" \" ~]",
        ],
        "happy": [
            "   /^\\! ",
            "  (^.^) ",
            "  /)_)\\>",
            "   \" \"~]",
        ],
        "gift": [
            "   /^\\  ",
            "  (o.o)[#]",
            "  /)_)\\>",
            "   \" \"~]",
        ],
    },
    "scholarly": {
        "idle": [
            "  .--. ",
            " (O.O) ",
            "  |__|>",
            "   ''  ",
        ],
        "waddle": [
            "  .--. ",
            " (O.O) ",
            "  |__|>",
            "  '' ''",
        ],
        "happy": [
            "  .--. !",
            " (^.^) ",
            "  |__|>",
            "   ''  ",
        ],
        "reading": [
            "  .--. ",
            " (-.-)>",
            "  |__|[=]",
            "   ''  ",
        ],
    },
    "artistic": {
        "idle": [
            "   ~@  ",
            "  (^.^)",
            "  /)~)\\>",
            "   '' ~",
        ],
        "waddle": [
            "   ~@  ",
            "  (o.o)",
            "  /)~)\\>",
            "  '' ''~",
        ],
        "happy": [
            "   ~@ *",
            "  (^o^)*",
            "  /)~)\\>",
            "   '' ~",
        ],
        "painting": [
            "   ~@  ",
            "  (-.o)~",
            "  /)~)\\[=]",
            "   '' ~",
        ],
    },
    "playful": {
        "idle": [
            "   @/  ",
            "  (>.>) ",
            "  /)_)\\>",
            "  d'' b",
        ],
        "waddle": [
            "   @\\  ",
            "  (<.<) ",
            "  /)_)\\>",
            " d'' b ",
        ],
        "happy": [
            "   @/ !",
            "  (>w<)!",
            "  /)_)\\>",
            "  d'' b",
        ],
        "bounce": [
            "   @|  ",
            "  (^o^) ",
            "  /)_)\\>",
            "   \\~/  ",
        ],
    },
    "mysterious": {
        "idle": [
            "  /_\\  ",
            " (?_?) ",
            "  |__|>",
            "   ~~  ",
        ],
        "waddle": [
            "  /_\\  ",
            " (?_?) ",
            "  |__|>",
            "  ~~ ~~",
        ],
        "happy": [
            "  /_\\ .",
            " (^_^)..",
            "  |__|>",
            "   ~~  ",
        ],
        "vanish": [
            "  ._.  ",
            " .?_?. ",
            "  .|.  ",
            "   .   ",
        ],
    },
    "generous": {
        "idle": [
            "  <3   ",
            "  (o.o)",
            "  /)_)\\>[+]",
            "   ''  ",
        ],
        "waddle": [
            "  <3   ",
            "  (o.o)",
            "  /)_)\\>[+]",
            "  '' ''",
        ],
        "happy": [
            " <3 <3 ",
            "  (^.^)",
            "  /)_)\\>[+]",
            "   ''  ",
        ],
        "giving": [
            "  <3   ",
            "  (^.^)[*]->",
            "  /)_)\\>",
            "   ''  ",
        ],
    },
    "foodie": {
        "idle": [
            "  _|=|_",
            "  (o.o)",
            "  /)_)\\>",
            "   ''  ",
        ],
        "waddle": [
            "  _|=|_",
            "  (o.o)",
            "  /)_)\\>",
            "  '' ''",
        ],
        "happy": [
            "  _|=|_!",
            "  (^o^)nom",
            "  /)_)\\>",
            "   ''  ",
        ],
        "eating": [
            "  _|=|_",
            "  (-.-)~@",
            "  /)_)\\>",
            "   '' .",
        ],
    },
    "athletic": {
        "idle": [
            "   ==  ",
            "  (o.o)",
            "  /)_)\\>",
            "   ''  ",
        ],
        "waddle": [
            "   ==  ",
            "  (o.o)",
            "  /)_)\\>",
            "  /  \\ ",
        ],
        "happy": [
            "  \\==/!",
            "  (>.<)!",
            "  /)_)\\>",
            "   ''  ",
        ],
        "exercise": [
            "   == !",
            "  (>.>)",
            " \\/)_)\\/",
            "  /  \\ ",
        ],
    },
}

# Visitor animation states by mood/activity
VISITOR_ANIMATION_STATES = {
    "arriving": ["waddle", "waddle", "idle"],
    "chatting": ["idle", "happy", "idle", "happy"],
    "playing": ["happy", "bounce" if "playful" else "happy", "waddle", "happy"],
    "giving_gift": ["idle", "gift" if "adventurous" else "giving", "happy"],
    "receiving_gift": ["happy", "happy", "idle"],
    "eating": ["eating", "eating", "happy"],
    "leaving": ["waddle", "waddle", "waddle"],
    "idle": ["idle", "idle", "happy", "idle"],
}

# Visitor animation timing
VISITOR_ANIMATION_SPEED = 0.5  # Seconds per frame (faster animation)
VISITOR_DIALOGUE_INTERVAL = 6.0  # Seconds between random dialogue
VISITOR_MOVE_INTERVAL = 1.2  # Seconds between position changes (faster movement)


# Visitor dialogue by personality and situation
VISITOR_GREETINGS = {
    "adventurous": [
        "*waddles in excitedly* Hey {duck}! Ready for adventure?",
        "Ahoy, {duck}! I just got back from the most amazing trip!",
        "*adjusts explorer hat* {duck}! Perfect timing!",
    ],
    "scholarly": [
        "*adjusts glasses* Ah, {duck}! I've been meaning to discuss something!",
        "Greetings, {duck}! Did you know that ducks have waterproof feathers?",
        "*opens book* {duck}, you must hear about my latest research!",
    ],
    "artistic": [
        "*twirls beret* {duck}! This pond is SO inspiring today!",
        "Oh {duck}! The light here is perfect for painting!",
        "*sketches in air* I see art everywhere when I'm with you!",
    ],
    "playful": [
        "*bounces excitedly* {duck}! {duck}! Let's PLAY!",
        "TAG, YOU'RE IT! ...wait, hi {duck}!",
        "*spins around* Best day ever! I get to see {duck}!",
    ],
    "mysterious": [
        "*appears from shadows* ...{duck}. The winds told me to come.",
        "Greetings, {duck}. I sensed... something. Perhaps fate.",
        "*nods mysteriously* We meet again, {duck}...",
    ],
    "generous": [
        "*waves warmly* {duck}! I brought something for you!",
        "Dearest {duck}! Sharing is caring, and I LOVE sharing!",
        "*beams happily* {duck}! You deserve nice things!",
    ],
    "foodie": [
        "*sniffs air* {duck}! Something smells DELICIOUS here!",
        "Ooh, {duck}! Have you tried that new bread recipe?",
        "*stomach growls* Perfect timing! Let's eat, {duck}!",
    ],
    "athletic": [
        "*jogs over* {duck}! Great day for some exercise!",
        "Race you to the pond, {duck}! Oh wait, we're already here!",
        "*stretches* Looking fit, {duck}! Keep up the good work!",
    ],
}

VISITOR_FAREWELLS = {
    "adventurous": [
        "Adventure awaits! See you next time, {duck}!",
        "*tips explorer hat* Until our paths cross again!",
        "The horizon is calling! Bye, {duck}!",
    ],
    "scholarly": [
        "Fascinating visit! I have much to document. Farewell, {duck}!",
        "*closes book* Until our next intellectual exchange!",
        "Knowledge shared is knowledge doubled. Goodbye, {duck}!",
    ],
    "artistic": [
        "*blows kiss* Stay beautiful, {duck}! Ciao!",
        "This visit was pure inspiration! Au revoir!",
        "*dramatic bow* The world awaits my art! Bye, {duck}!",
    ],
    "playful": [
        "*waves frantically* BYE BYE BYE {duck}!!! Miss you already!",
        "That was SO fun! Same time tomorrow? Pleeeease?",
        "*bounces away* WEEEEE! Bye {duck}!",
    ],
    "mysterious": [
        "*fades into shadows* We will meet again... when the stars align...",
        "The mists call me elsewhere. Farewell, {duck}...",
        "*cryptic smile* Until the threads of fate intertwine once more...",
    ],
    "generous": [
        "*big hug* Take care, sweet {duck}! You're the best!",
        "Remember, you're loved! Bye bye!",
        "*leaves a small gift* A little something to remember me by!",
    ],
    "foodie": [
        "*pats belly* What a feast! Thanks, {duck}! Bye!",
        "That was delicious! We MUST do this again!",
        "*waddles away happily* Save me some crumbs next time!",
    ],
    "athletic": [
        "*high-fives* Great workout, {duck}! Stay strong!",
        "Keep training! You're getting better every day!",
        "*jogs away* Race you next time! Bye!",
    ],
}

VISITOR_IDLE_CHAT = {
    "adventurous": [
        "*points at horizon* I wonder what's over there...",
        "Did I tell you about the time I swam upstream for 3 miles?",
        "*checks map* Hmm, there might be treasure nearby!",
        "The Forest Edge has some great foraging spots!",
        "*looks around* This pond has so many unexplored corners!",
    ],
    "scholarly": [
        "*adjusts glasses* According to my research...",
        "Fun fact: Ducks can sleep with one eye open!",
        "*scribbles notes* Fascinating weather patterns today!",
        "Have you ever wondered why the sky is blue?",
        "*reads from book* 'And thus, the duck discovered...'",
    ],
    "artistic": [
        "*gazes dreamily* The ripples in the water are like poetry...",
        "I should paint this scene! It's magnificent!",
        "*hums a tune* Everything inspires a song!",
        "The way the light hits the lily pads... *chef's kiss*",
        "*sketches* Hold still, you're perfect right now!",
    ],
    "playful": [
        "*splashes* Hehe! Gotcha!",
        "Wanna play hide and seek? I'll count!",
        "*makes silly face* Quack quack quack!",
        "I bet I can hold my breath longer than you!",
        "*chases own tail* Almost got it!",
    ],
    "mysterious": [
        "*stares into distance* The shadows whisper secrets...",
        "Do you ever feel like we're being watched?",
        "*traces patterns in water* The signs are everywhere...",
        "I had a vision last night... about you.",
        "*cryptic pause* ...nevermind. You're not ready yet.",
    ],
    "generous": [
        "*offers crumb* Here, you look hungry!",
        "Is there anything you need? I want to help!",
        "*picks flower* This made me think of you!",
        "Your happiness makes me happy!",
        "*beams* I love spending time with you!",
    ],
    "foodie": [
        "*sniffs* What's that delicious smell?",
        "You know what would be perfect right now? Cake.",
        "*daydreams* Bread... crusty, warm bread...",
        "We should try that new spot by the garden!",
        "*nibbles on something* Want some? It's tasty!",
    ],
    "athletic": [
        "*does squats* Gotta stay in shape!",
        "Have you been working out? You look stronger!",
        "*stretches* Ahh, that's the good burn!",
        "We should do laps around the pond!",
        "*shadowboxing* Staying ready!",
    ],
}

# Comments about items and structures
VISITOR_ITEM_COMMENTS = {
    "adventurous": {
        "ball": "Ooh, a ball! Reminds me of coconuts on tropical islands!",
        "fountain": "A fountain! Perfect for dramatic departures!",
        "pond_fountain": "Wow, a fountain! The explorers' rest stop!",
        "basic_nest": "A cozy nest! Good base camp, friend!",
        "cozy_nest": "That nest looks perfect for planning expeditions!",
        "deluxe_nest": "Now THAT'S a headquarters worthy of an adventurer!",
        "mud_hut": "Rustic shelter! Reminds me of jungle camps!",
        "wooden_cottage": "A proper cottage! Very expedition-ready!",
        "stone_house": "Stone walls! This could survive any storm!",
        "watchtower": "A watchtower! Perfect for spotting new horizons!",
        "garden_plot": "Growing your own supplies? Smart explorer!",
        "bird_bath": "A bird bath! Essential for any traveler!",
        "hat": "Nice hat! Very explorer-chic!",
        "bow_tie": "Fancy! Ready for a formal adventure?",
        "_default": "Interesting! I've seen something like this in my travels!",
    },
    "scholarly": {
        "ball": "A sphere! The most mathematically elegant shape!",
        "fountain": "Fascinating water dynamics at play here!",
        "pond_fountain": "The hydraulics here are remarkable!",
        "basic_nest": "Functional architecture! Efficient design!",
        "cozy_nest": "Improved insulation coefficient! Well done!",
        "deluxe_nest": "Magnificent engineering! May I take notes?",
        "workbench": "A workbench! The foundation of innovation!",
        "storage_chest": "Organized storage! A sign of a great mind!",
        "watchtower": "Elevated observation platform! Excellent for research!",
        "glasses": "Excellent eyewear choice! Great for reading!",
        "_default": "Hmm, this warrants further study...",
    },
    "artistic": {
        "ball": "The curves! The shadow! So sculptural!",
        "fountain": "The water's movement is pure performance art!",
        "pond_fountain": "OH! *gasp* The aesthetic! It's perfect!",
        "basic_nest": "Minimalist design! I love it!",
        "cozy_nest": "The textures! So wonderfully rustic!",
        "deluxe_nest": "A MASTERPIECE of architectural art!",
        "flower_bed": "Flowers! Nature's own gallery!",
        "garden_plot": "A living canvas! How creative!",
        "stone_path": "The lines! The symmetry! *chef's kiss*",
        "hat": "Ooh la la! Very fashionable!",
        "bow_tie": "That bow tie is EVERYTHING!",
        "_default": "Oh, how beautiful! This speaks to my soul!",
    },
    "playful": {
        "ball": "A BALL! CAN WE PLAY? PLEASE PLEASE PLEASE!",
        "fountain": "SPLASH TIME! *runs toward it*",
        "pond_fountain": "WATER SHOW! *does a little dance*",
        "basic_nest": "Perfect for hide and seek!",
        "cozy_nest": "Pillow fort vibes! I LOVE IT!",
        "deluxe_nest": "This is the BEST fort ever!",
        "bird_bath": "SPLASH SPLASH! This is the best!",
        "watchtower": "I bet I can jump off that!",
        "party_hat": "PARTY HAT! Is it your birthday?!",
        "_default": "OOOH! That looks FUN!",
    },
    "mysterious": {
        "ball": "*stares* The orb holds many secrets...",
        "fountain": "The water... it shows visions of the future...",
        "pond_fountain": "The spirits of the water dance here...",
        "basic_nest": "A sanctuary from the watching eyes...",
        "cozy_nest": "The shadows here are... comfortable...",
        "deluxe_nest": "Many secrets could be kept here...",
        "watchtower": "From there, one can see the threads of fate...",
        "_default": "Interesting... but what does it MEAN?",
    },
    "generous": {
        "ball": "Oh, a ball! Want me to throw it for you?",
        "fountain": "So pretty! I should get you more decorations!",
        "pond_fountain": "Beautiful! You deserve such nice things!",
        "basic_nest": "A home! Let me help you decorate!",
        "cozy_nest": "So welcoming! You're wonderful, you know?",
        "deluxe_nest": "You've worked so hard! I'm proud of you!",
        "garden_plot": "Growing things for others to enjoy! How lovely!",
        "_default": "How lovely! You deserve nice things!",
    },
    "foodie": {
        "ball": "For a second I thought that was a giant meatball...",
        "fountain": "Is that... drinking water? *licks lips*",
        "pond_fountain": "Fresh water! Great for cooking!",
        "basic_nest": "Nice! But where's the pantry?",
        "garden_plot": "VEGETABLES! Fresh ingredients! *drools*",
        "storage_chest": "Please tell me there's food in there!",
        "_default": "Nice! But have you considered adding a snack bar?",
    },
    "athletic": {
        "ball": "Great for agility training! *kicks it*",
        "fountain": "Perfect for cooling down after a workout!",
        "pond_fountain": "Hydration station! Essential!",
        "basic_nest": "Good recovery spot after training!",
        "watchtower": "I could do pull-ups on that!",
        "stone_path": "Perfect running track!",
        "bird_bath": "Post-workout cooldown! *stretches*",
        "_default": "Nice setup! Good for training!",
    },
}

VISITOR_COSMETIC_COMMENTS = {
    "adventurous": [
        "Love the look, {duck}! Very expedition-ready!",
        "That {item} would survive any adventure!",
        "Looking equipped for anything!",
    ],
    "scholarly": [
        "Interesting fashion choice, {duck}! I should document this!",
        "That {item} is quite distinguished!",
        "Academic chic! I approve!",
    ],
    "artistic": [
        "Oh {duck}, you're SERVING with that {item}!",
        "The aesthetic! *chef's kiss*",
        "You're a work of art, darling!",
    ],
    "playful": [
        "CUTE CUTE CUTE! I love your {item}!",
        "We should trade looks sometime!",
        "You look SO fun!",
    ],
    "mysterious": [
        "That {item}... it suits your aura...",
        "The shadows favor your choice...",
        "*knowing nod*",
    ],
    "generous": [
        "You look wonderful, {duck}!",
        "That {item} is perfect for you!",
        "You deserve to look this good!",
    ],
    "foodie": [
        "Nice {item}! But more importantly, what's for lunch?",
        "Looking good enough to eat! Wait, that came out wrong...",
        "Stylish! Now let's celebrate with snacks!",
    ],
    "athletic": [
        "Looking fit, {duck}! Is that {item} aerodynamic?",
        "Nice gear! Function AND fashion!",
        "That's some champion style!",
    ],
}

# Lazy import for LLM behavior controller
_llm_controller = None

def _get_llm_controller():
    """Lazy load LLM controller to avoid circular imports."""
    global _llm_controller
    if _llm_controller is None:
        try:
            from dialogue.llm_behavior import get_behavior_controller
            _llm_controller = get_behavior_controller()
        except ImportError:
            pass
    return _llm_controller


class VisitorAnimator:
    """Handles visitor NPC animations during visits."""
    
    def __init__(self):
        self._current_state: str = "idle"
        self._frame_index: int = 0
        self._last_frame_time: float = 0.0
        self._last_dialogue_time: float = 0.0
        self._last_move_time: float = 0.0
        self._personality: str = "adventurous"
        self._friend_name: str = "Friend"
        self._position_x: int = 60  # Absolute screen position
        self._position_y: int = 4
        self._target_x: int = 25
        self._target_y: int = 4
        self._wobble: int = 0
        self._near_duck: bool = False
        self._commented_items: set = set()  # Items we've already commented on
        self._has_greeted: bool = False
        self._is_leaving: bool = False
        self._following_duck: bool = False  # Whether currently following the duck
        self._wander_timer: int = 0  # Time since last wander decision
        
        # New dialogue system
        self._dialogue_manager = None
        self._friendship_level: str = "stranger"
        self._visit_number: int = 1
        self._unlocked_topics: set = set()
        self._conversation_over: bool = False
        
        # LLM integration
        self._shared_memories: List[str] = []  # Memories from Friend dataclass
        self._duck_ref = None  # Reference to player's duck for LLM context
    
    def set_visitor(self, personality: str, friend_name: str = "Friend", 
                     friendship_level: str = "stranger", visit_number: int = 1,
                     unlocked_topics: set = None, conversation_topics: list = None,
                     shared_experiences: list = None, last_conversation_summary: str = "",
                     duck_ref = None, shared_memories: list = None):
        """Set the current visitor's personality for art selection."""
        self._personality = personality.lower() if personality else "adventurous"
        self._friend_name = friend_name
        self._frame_index = 0
        self._current_state = "arriving"
        self._position_x = 60  # Start at right side of screen (absolute)
        self._position_y = 4   # Start near middle height
        self._target_x = 25    # Initial target toward center
        self._target_y = 4
        self._has_greeted = False
        self._is_leaving = False
        self._commented_items = set()
        self._last_dialogue_time = time.time()
        self._last_move_time = time.time()
        self._following_duck = False  # Whether currently following the duck
        self._wander_timer = 0  # Time since last wander decision
        
        # LLM integration references
        self._duck_ref = duck_ref
        self._shared_memories = shared_memories or []
        
        # Setup new dialogue system
        self._friendship_level = friendship_level.lower().replace(" ", "_")
        self._visit_number = visit_number
        self._unlocked_topics = unlocked_topics or set()
        self._conversation_over = False
        
        # Initialize dialogue manager with memory
        try:
            from dialogue.visitor_dialogue import VisitorDialogueManager
            self._dialogue_manager = VisitorDialogueManager()
            self._dialogue_manager.start_visit(
                self._personality, 
                self._friendship_level, 
                self._friend_name,
                self._visit_number,
                self._unlocked_topics,
                conversation_topics=conversation_topics or [],
                shared_experiences=shared_experiences or [],
                last_conversation_summary=last_conversation_summary or "",
            )
        except ImportError:
            self._dialogue_manager = None
    
    def set_state(self, state: str):
        """Set the animation state (arriving, chatting, playing, etc.)."""
        if state in VISITOR_ANIMATION_STATES:
            self._current_state = state
            self._frame_index = 0
    
    def start_leaving(self):
        """Begin the leaving animation."""
        self._is_leaving = True
        self._current_state = "leaving"
        self._target_x = 70  # Move off screen right (absolute position)
    
    def update(self, current_time: float, duck_x: int = 10, duck_y: int = 5) -> Tuple[bool, Optional[str]]:
        """Update animation frame and movement. Returns (frame_changed, dialogue_message)."""
        frame_changed = False
        dialogue = None
        
        # Update animation frame
        if current_time - self._last_frame_time >= VISITOR_ANIMATION_SPEED:
            self._last_frame_time = current_time
            frames = VISITOR_ANIMATION_STATES.get(self._current_state, ["idle"])
            self._frame_index = (self._frame_index + 1) % len(frames)
            
            # Add wobble for movement
            if self._current_state in ["arriving", "leaving", "playing"]:
                self._wobble = 1 if self._wobble == 0 else 0
            else:
                self._wobble = 0
            
            frame_changed = True
        
        # Update position (move toward target)
        if current_time - self._last_move_time >= VISITOR_MOVE_INTERVAL:
            self._last_move_time = current_time
            self._wander_timer += 1
            
            # Move toward target position (can move 1-2 units for more dynamic movement)
            move_speed = 2 if self._is_leaving else 1
            
            if self._position_x < self._target_x:
                self._position_x = min(self._position_x + move_speed, self._target_x)
            elif self._position_x > self._target_x:
                self._position_x = max(self._position_x - move_speed, self._target_x)
            
            if self._position_y < self._target_y:
                self._position_y += 1
            elif self._position_y > self._target_y:
                self._position_y -= 1
            
            # Check if near duck
            dist_to_duck = abs(self._position_x - duck_x) + abs(self._position_y - duck_y)
            self._near_duck = dist_to_duck < 15
            
            # Decide behavior: follow duck, wander, or explore
            if not self._is_leaving:
                # Every few updates, decide what to do
                if self._position_x == self._target_x and self._position_y == self._target_y:
                    behavior = random.random()
                    
                    if behavior < 0.4:  # 40% chance: Follow the duck
                        # Move toward where the duck is
                        offset_x = random.randint(-8, 8)
                        offset_y = random.randint(-2, 2)
                        self._target_x = duck_x + offset_x
                        self._target_y = duck_y + offset_y
                        self._following_duck = True
                        if random.random() < 0.3:
                            self._current_state = "chatting"
                    
                    elif behavior < 0.7:  # 30% chance: Wander around exploring
                        # Pick a random spot on the screen
                        self._target_x = random.randint(5, 55)
                        self._target_y = random.randint(1, 7)
                        self._following_duck = False
                        if random.random() < 0.3:
                            self._current_state = "playing"
                    
                    else:  # 30% chance: Stay near duck
                        # Stay close to the duck
                        self._target_x = duck_x + random.randint(3, 10)
                        self._target_y = duck_y + random.randint(-1, 1)
                        self._following_duck = True
                        if random.random() < 0.5:
                            states = ["idle", "chatting", "happy"]
                            self._current_state = random.choice(states)
                    
                    # Keep in screen bounds
                    self._target_x = max(2, min(self._target_x, 58))
                    self._target_y = max(0, min(self._target_y, 8))
        
        return frame_changed, dialogue
    
    def get_position(self) -> Tuple[int, int]:
        """Get current visitor position offset."""
        return self._position_x, self._position_y
    
    def is_near_duck(self) -> bool:
        """Check if visitor is near the duck."""
        return self._near_duck
    
    def get_greeting(self, duck_name: str) -> str:
        """Get a greeting message for when the visitor arrives."""
        if self._has_greeted:
            return ""
        self._has_greeted = True
        
        # Use new dialogue system if available
        if self._dialogue_manager:
            return self._dialogue_manager.get_next_dialogue(duck_name) or ""
        
        # Fallback to old system
        greetings = VISITOR_GREETINGS.get(self._personality, VISITOR_GREETINGS["adventurous"])
        greeting = random.choice(greetings).format(duck=duck_name)
        return f"{self._friend_name}: {greeting}"
    
    def get_farewell(self, duck_name: str) -> str:
        """Get a farewell message when the visitor leaves."""
        # Use new dialogue system if available
        if self._dialogue_manager:
            return self._dialogue_manager.get_farewell(duck_name)
        
        # Fallback to old system
        farewells = VISITOR_FAREWELLS.get(self._personality, VISITOR_FAREWELLS["adventurous"])
        farewell = random.choice(farewells).format(duck=duck_name)
        return f"{self._friend_name}: {farewell}"
    
    def get_random_dialogue(self, duck_name: str, current_time: float) -> Optional[str]:
        """Get random idle chat if enough time has passed."""
        if current_time - self._last_dialogue_time < VISITOR_DIALOGUE_INTERVAL:
            return None
        
        self._last_dialogue_time = current_time
        
        # Only chat if near duck
        if not self._near_duck:
            return None
        
        # Use new dialogue system if available (primary source)
        if self._dialogue_manager:
            dialogue = self._dialogue_manager.get_next_dialogue(duck_name)
            if dialogue:
                # Check if conversation is over (triggers leaving)
                if self._dialogue_manager.is_conversation_over():
                    self._conversation_over = True
                return dialogue
            else:
                # No more dialogue - conversation over
                self._conversation_over = True
                return None
        
        # Fallback to old system (only if no dialogue manager)
        chat_lines = VISITOR_IDLE_CHAT.get(self._personality, VISITOR_IDLE_CHAT["adventurous"])
        line = random.choice(chat_lines).format(duck=duck_name)
        return f"{self._friend_name}: {line}"
    
    def is_conversation_complete(self) -> bool:
        """Check if the visitor has said everything they wanted to say."""
        return self._conversation_over
    
    def get_unlocked_topics(self) -> set:
        """Get any new topics unlocked during this visit."""
        if self._dialogue_manager:
            return self._dialogue_manager.unlocked_topics
        return set()
    
    def get_item_comment(self, item_id: str, item_name: str) -> Optional[str]:
        """Get a comment about an item the visitor sees."""
        if item_id in self._commented_items:
            return None
        
        # Only comment sometimes
        if random.random() > 0.5:
            return None
        
        self._commented_items.add(item_id)
        
        item_comments = VISITOR_ITEM_COMMENTS.get(self._personality, {})
        if item_id in item_comments:
            comment = item_comments[item_id]
        elif "_default" in item_comments:
            comment = item_comments["_default"]
        else:
            return None
        
        return f"{self._friend_name}: {comment}"
    
    def get_cosmetic_comment(self, duck_name: str, cosmetic_type: str) -> Optional[str]:
        """Get a comment about the duck's cosmetics."""
        key = f"cosmetic_{cosmetic_type}"
        if key in self._commented_items:
            return None
        
        # Only comment sometimes
        if random.random() > 0.4:
            return None
        
        self._commented_items.add(key)
        
        comments = VISITOR_COSMETIC_COMMENTS.get(self._personality, VISITOR_COSMETIC_COMMENTS["adventurous"])
        comment = random.choice(comments).format(duck=duck_name, item=cosmetic_type)
        return f"{self._friend_name}: {comment}"
    
    def get_current_art(self) -> List[str]:
        """Get the current animation frame's ASCII art."""
        frames = VISITOR_ANIMATION_STATES.get(self._current_state, ["idle"])
        frame_name = frames[self._frame_index % len(frames)]
        
        # Get personality-specific art
        personality_art = VISITOR_ASCII_ART.get(self._personality, VISITOR_ASCII_ART["adventurous"])
        art = personality_art.get(frame_name, personality_art.get("idle", ["[DUCK]"]))
        
        # Apply wobble offset
        if self._wobble:
            art = [" " + line[:-1] if len(line) > 1 else line for line in art]
        
        return art
    
    def get_activity_message(self) -> str:
        """Get a message describing what the visitor is doing."""
        messages = {
            "arriving": "*waddles over excitedly*",
            "chatting": "*quacks in conversation*",
            "playing": "*having fun!*",
            "giving_gift": "*offers a gift*",
            "receiving_gift": "*accepts gift happily*",
            "eating": "*om nom nom*",
            "leaving": "*waves goodbye*",
            "idle": "*standing around*",
        }
        return messages.get(self._current_state, "")


# Global visitor animator instance
visitor_animator = VisitorAnimator()

# Duck names by personality
DUCK_NAMES = {
    "adventurous": ["Marco", "Amelia", "Columbus", "Vasco", "Marina"],
    "scholarly": ["Einstein", "Newton", "Ada", "Darwin", "Curie"],
    "artistic": ["Picasso", "Frida", "Leonardo", "Monet", "Georgia"],
    "playful": ["Bubbles", "Giggles", "Zippy", "Bouncy", "Sunny"],
    "mysterious": ["Shadow", "Phantom", "Enigma", "Whisper", "Raven"],
    "generous": ["Charity", "Grace", "Blessing", "Angel", "Heart"],
    "foodie": ["Cookie", "Biscuit", "Truffle", "Pepper", "Ginger"],
    "athletic": ["Dash", "Sprint", "Champion", "Victor", "Rocket"],
}


@dataclass
class DuckFriend:
    """A friend duck that can visit."""
    id: str
    name: str
    personality: DuckPersonalityType
    friendship_level: FriendshipLevel
    friendship_points: int = 0
    times_visited: int = 0
    gifts_given: int = 0
    gifts_received: int = 0
    favorite_food: str = "bread"
    favorite_activity: str = "chat"
    first_met: str = ""
    last_visit: str = ""
    special_memories: List[str] = field(default_factory=list)
    unlocked_dialogue: List[str] = field(default_factory=list)
    # NEW: Conversation memory to prevent repetitive introductions
    conversation_topics: List[str] = field(default_factory=list)  # Topics we've discussed
    shared_experiences: List[str] = field(default_factory=list)  # Activities done together
    gifts_exchanged_history: List[str] = field(default_factory=list)  # What gifts we've exchanged
    last_conversation_summary: str = ""  # Brief summary of last talk


@dataclass
class VisitEvent:
    """An active visit from a friend duck."""
    friend_id: str
    started_at: str
    duration_minutes: int
    activities_done: List[str] = field(default_factory=list)
    mood: str = "happy"
    gift_brought: Optional[str] = None
    waiting_for_gift: bool = False


# Friendship point thresholds
FRIENDSHIP_THRESHOLDS = {
    FriendshipLevel.STRANGER: 0,
    FriendshipLevel.ACQUAINTANCE: 50,
    FriendshipLevel.FRIEND: 150,
    FriendshipLevel.CLOSE_FRIEND: 350,
    FriendshipLevel.BEST_FRIEND: 600,
}

# Gift preferences by personality
GIFT_PREFERENCES = {
    "adventurous": ["map", "compass", "binoculars", "hiking_boots"],
    "scholarly": ["book", "quill", "scroll", "telescope"],
    "artistic": ["paintbrush", "canvas", "palette", "sketchbook"],
    "playful": ["ball", "toy", "balloon", "party_hat"],
    "mysterious": ["crystal", "candle", "tarot_deck", "incense"],
    "generous": ["flowers", "chocolate", "ribbon", "heart_charm"],
    "foodie": ["bread", "cake", "cheese", "apple"],
    "athletic": ["dumbbell", "whistle", "medal", "energy_drink"],
}

# Gifts that visitors can bring
VISITOR_GIFTS = {
    "adventurous": ["exotic_feather", "rare_shell", "ancient_coin", "treasure_map"],
    "scholarly": ["rare_book", "fossil", "star_chart", "potion_recipe"],
    "artistic": ["painting", "sculpture", "poem", "melody"],
    "playful": ["toy", "joke_item", "party_favor", "fun_hat"],
    "mysterious": ["mystery_box", "crystal_ball", "shadow_stone", "prophecy"],
    "generous": ["gold_coins", "rare_seed", "blessing_charm", "wish_token"],
    "foodie": ["gourmet_bread", "secret_recipe", "rare_fruit", "magic_ingredient"],
    "athletic": ["trophy", "energy_boost", "speed_shoes", "champion_medal"],
}


class FriendsSystem:
    """
    Manages duck friends, visits, and social interactions.
    """
    
    def __init__(self):
        self.friends: Dict[str, DuckFriend] = {}
        self.current_visit: Optional[VisitEvent] = None
        self.total_visits: int = 0
        self.total_gifts_exchanged: int = 0
        self.last_visitor_time: str = ""
        self.friend_count_by_level: Dict[str, int] = {}
        self.best_friend_id: Optional[str] = None
        self.pending_invitations: List[str] = []
    
    def generate_new_friend(self) -> DuckFriend:
        """Generate a new random friend duck."""
        personality = random.choice(list(DuckPersonalityType))
        names = DUCK_NAMES[personality.value]
        name = random.choice(names)
        
        # Ensure unique name
        existing_names = {f.name for f in self.friends.values()}
        while name in existing_names and len(existing_names) < len(names):
            name = random.choice(names)
        
        friend_id = f"friend_{len(self.friends)}_{random.randint(1000, 9999)}"
        
        # Random favorite food and activity
        foods = ["bread", "seeds", "berries", "worms", "algae", "fish"]
        activities = ["chat", "play", "swim", "explore", "nap", "eat"]
        
        friend = DuckFriend(
            id=friend_id,
            name=name,
            personality=personality,
            friendship_level=FriendshipLevel.STRANGER,
            favorite_food=random.choice(foods),
            favorite_activity=random.choice(activities),
            first_met=datetime.now().isoformat(),
        )
        
        self.friends[friend_id] = friend
        return friend
    
    def get_friend_by_id(self, friend_id: str) -> Optional[DuckFriend]:
        """Get a friend by their ID."""
        return self.friends.get(friend_id)
    
    def start_visit(self, friend_id: Optional[str] = None) -> Tuple[bool, str, Optional[VisitEvent]]:
        """Start a visit from a friend duck."""
        if self.current_visit:
            return False, "A friend is already visiting!", None
        
        # Get or generate friend
        if friend_id and friend_id in self.friends:
            friend = self.friends[friend_id]
        elif self.friends:
            # Random friend visits
            friend = random.choice(list(self.friends.values()))
        else:
            # Generate new friend
            friend = self.generate_new_friend()
        
        # Determine visit duration based on friendship level (in minutes)
        # Keep visits short so they don't overstay their welcome
        duration_map = {
            FriendshipLevel.STRANGER: 2,
            FriendshipLevel.ACQUAINTANCE: 3,
            FriendshipLevel.FRIEND: 4,
            FriendshipLevel.CLOSE_FRIEND: 5,
            FriendshipLevel.BEST_FRIEND: 6,
        }
        
        duration = duration_map.get(friend.friendship_level, 3)
        
        # Determine if they brought a gift
        gift_chance = 0.2 + (friend.friendship_points / 1000)
        brought_gift = random.random() < gift_chance
        gift = None
        if brought_gift:
            gifts = VISITOR_GIFTS.get(friend.personality.value, ["surprise_gift"])
            gift = random.choice(gifts)
        
        self.current_visit = VisitEvent(
            friend_id=friend.id,
            started_at=datetime.now().isoformat(),
            duration_minutes=duration,
            gift_brought=gift,
        )
        
        friend.times_visited += 1
        friend.last_visit = datetime.now().isoformat()
        self.total_visits += 1
        self.last_visitor_time = datetime.now().isoformat()
        
        gift_msg = f" They brought you a {gift}!" if gift else ""
        return True, f"d {friend.name} is visiting!{gift_msg}", self.current_visit
    
    def interact_with_visitor(self, activity: str) -> Tuple[bool, str, int]:
        """Do an activity with the visiting friend."""
        if not self.current_visit:
            return False, "No one is visiting right now!", 0
        
        friend = self.friends.get(self.current_visit.friend_id)
        if not friend:
            return False, "Friend not found!", 0
        
        # Calculate friendship points earned
        base_points = 10
        
        # Bonus for favorite activity
        if activity == friend.favorite_activity:
            base_points += 15
            message = f"{friend.name} loves this! +{base_points} friendship points!"
        else:
            message = f"You and {friend.name} enjoyed {activity}. +{base_points} friendship points!"
        
        # Record activity
        self.current_visit.activities_done.append(activity)
        
        # Add to shared experiences memory (for returning visitor context)
        if activity not in friend.shared_experiences:
            friend.shared_experiences.append(activity)
        # Keep only last 10 experiences
        if len(friend.shared_experiences) > 10:
            friend.shared_experiences = friend.shared_experiences[-10:]
        
        # Add friendship points
        friend.friendship_points += base_points
        
        # Check for level up
        old_level = friend.friendship_level
        new_level = self._calculate_level(friend.friendship_points)
        
        if new_level != old_level:
            friend.friendship_level = new_level
            message += f"\n(!) Friendship level up! {friend.name} is now your {new_level.value.replace('_', ' ')}!"
            
            # Add special memory
            friend.special_memories.append(
                f"Became {new_level.value.replace('_', ' ')} on {datetime.now().strftime('%Y-%m-%d')}"
            )
        
        return True, message, base_points
    
    def give_gift_to_visitor(self, item: str) -> Tuple[bool, str, int]:
        """Give a gift to the visiting friend."""
        if not self.current_visit:
            return False, "No one is visiting right now!", 0
        
        friend = self.friends.get(self.current_visit.friend_id)
        if not friend:
            return False, "Friend not found!", 0
        
        # Check if it's their preferred gift type
        preferred = GIFT_PREFERENCES.get(friend.personality.value, [])
        
        if item in preferred:
            points = 30
            reaction = f":D {friend.name} LOVES this gift!"
        elif item == friend.favorite_food:
            points = 25
            reaction = f":) {friend.name}'s favorite food! They're so happy!"
        else:
            points = 15
            reaction = f":) {friend.name} appreciates the gift!"
        
        friend.friendship_points += points
        friend.gifts_received += 1
        self.total_gifts_exchanged += 1
        
        # Record gift in memory for context-aware conversations
        gift_memory = f"received {item} as gift"
        if gift_memory not in friend.gifts_exchanged_history:
            friend.gifts_exchanged_history.append(gift_memory)
        if len(friend.gifts_exchanged_history) > 10:
            friend.gifts_exchanged_history = friend.gifts_exchanged_history[-10:]
        
        return True, f"{reaction} +{points} friendship points!", points
    
    def receive_gift(self) -> Tuple[bool, str, Optional[str]]:
        """Receive the gift brought by a visitor."""
        if not self.current_visit or not self.current_visit.gift_brought:
            return False, "No gift to receive!", None
        
        gift = self.current_visit.gift_brought
        self.current_visit.gift_brought = None
        
        friend = self.friends.get(self.current_visit.friend_id)
        if friend:
            friend.gifts_given += 1
            # Record gift in memory
            gift_memory = f"gave {gift}"
            if gift_memory not in friend.gifts_exchanged_history:
                friend.gifts_exchanged_history.append(gift_memory)
            if len(friend.gifts_exchanged_history) > 10:
                friend.gifts_exchanged_history = friend.gifts_exchanged_history[-10:]
        
        self.total_gifts_exchanged += 1
        
        return True, f"[+] You received: {gift}!", gift
    
    def end_visit(self) -> Tuple[bool, str, Dict]:
        """End the current visit."""
        if not self.current_visit:
            return False, "No active visit to end!", {}
        
        friend = self.friends.get(self.current_visit.friend_id)
        if not friend:
            self.current_visit = None
            return False, "Friend not found!", {}
        
        activities = len(self.current_visit.activities_done)
        summary = {
            "friend_name": friend.name,
            "activities_done": activities,
            "friendship_points": friend.friendship_points,
            "friendship_level": friend.friendship_level.value,
        }
        
        farewell_messages = [
            f"* {friend.name} waves goodbye! Come back soon!",
            f"d {friend.name} quacks a cheerful farewell!",
            f"! {friend.name} waddles away happily!",
        ]
        
        self.current_visit = None
        
        return True, random.choice(farewell_messages), summary
    
    def _calculate_level(self, points: int) -> FriendshipLevel:
        """Calculate friendship level based on points."""
        if points >= FRIENDSHIP_THRESHOLDS[FriendshipLevel.BEST_FRIEND]:
            return FriendshipLevel.BEST_FRIEND
        elif points >= FRIENDSHIP_THRESHOLDS[FriendshipLevel.CLOSE_FRIEND]:
            return FriendshipLevel.CLOSE_FRIEND
        elif points >= FRIENDSHIP_THRESHOLDS[FriendshipLevel.FRIEND]:
            return FriendshipLevel.FRIEND
        elif points >= FRIENDSHIP_THRESHOLDS[FriendshipLevel.ACQUAINTANCE]:
            return FriendshipLevel.ACQUAINTANCE
        else:
            return FriendshipLevel.STRANGER
    
    def check_for_random_visitor(self, hour: int) -> Tuple[bool, Optional[str]]:
        """Check if a random visitor should appear."""
        if self.current_visit:
            return False, None
        
        # More likely during day hours - but kept rare to feel special
        if 8 <= hour <= 18:
            chance = 0.02  # 2% chance per check during day (was 12%)
        else:
            chance = 0.005  # 0.5% chance at night (was 5%)
        
        # More friends = more chances (up to +3%)
        chance += min(len(self.friends) * 0.005, 0.03)
        
        if random.random() < chance:
            _, message, _ = self.start_visit()
            return True, message
        
        return False, None
    
    def get_friend_list(self) -> List[Dict]:
        """Get list of all friends with their info."""
        return [
            {
                "id": f.id,
                "name": f.name,
                "personality": f.personality.value,
                "level": f.friendship_level.value,
                "points": f.friendship_points,
                "visits": f.times_visited,
            }
            for f in sorted(
                self.friends.values(),
                key=lambda x: x.friendship_points,
                reverse=True
            )
        ]
    
    def render_friend_card(self, friend_id: str) -> List[str]:
        """Render a friend's info card."""
        friend = self.friends.get(friend_id)
        if not friend:
            return ["Friend not found!"]
        
        appearance = DUCK_APPEARANCES.get(friend.personality.value, {})
        
        level_stars = {
            FriendshipLevel.STRANGER: "*****",
            FriendshipLevel.ACQUAINTANCE: "*****",
            FriendshipLevel.FRIEND: "*****",
            FriendshipLevel.CLOSE_FRIEND: "*****",
            FriendshipLevel.BEST_FRIEND: "*****",
        }
        
        next_level_points = 0
        levels = list(FRIENDSHIP_THRESHOLDS.items())
        for i, (level, threshold) in enumerate(levels):
            if level == friend.friendship_level and i < len(levels) - 1:
                next_level_points = levels[i + 1][1]
                break
        
        progress = ""
        if next_level_points > 0:
            progress_pct = friend.friendship_points / next_level_points
            filled = int(progress_pct * 10)
            progress = f"[{'#' * filled}{'.' * (10 - filled)}] {friend.friendship_points}/{next_level_points}"
        
        lines = [
            "+====================================+",
            f"|  d {friend.name:^28} |",
            f"|  {appearance.get('color', 'yellow'):^32} |",
            "+====================================+",
            f"|  Personality: {friend.personality.value:^17} |",
            f"|  {level_stars.get(friend.friendship_level, '*****'):^32} |",
            f"|  {friend.friendship_level.value.replace('_', ' ').title():^32} |",
            "+====================================+",
            f"|  Visits: {friend.times_visited:^23} |",
            f"|  Gifts Given: {friend.gifts_given:^18} |",
            f"|  Gifts Received: {friend.gifts_received:^15} |",
            "+====================================+",
            f"|  Likes: {friend.favorite_food}, {friend.favorite_activity:^15} |",
        ]
        
        if progress:
            lines.append(f"|  {progress:^32} |")
        
        lines.append("+====================================+")
        
        return lines
    
    def render_visit_screen(self) -> List[str]:
        """Render the current visit screen."""
        if not self.current_visit:
            return ["No visitor right now!"]
        
        friend = self.friends.get(self.current_visit.friend_id)
        if not friend:
            return ["Visitor not found!"]
        
        lines = [
            "+===============================================+",
            f"|  d VISITOR: {friend.name:^28}  |",
            f"|  {friend.personality.value.title():^41}  |",
            "+===============================================+",
            f"|  Friendship: {friend.friendship_level.value.replace('_', ' ').title():^28}  |",
            "|                                               |",
            "|       .--.                                    |",
            "|      (_ ^ _)                                  |",
            "|      /`    '\\                                 |",
            "|     (__)(____)                                |",
            "|                                               |",
            "+===============================================+",
            "|  Activities:                                  |",
        ]
        
        activities = self.current_visit.activities_done or ["None yet"]
        for activity in activities[-4:]:  # Show last 4 activities
            lines.append(f"|    - {activity:^37}  |")
        
        if self.current_visit.gift_brought:
            lines.append("+===============================================+")
            lines.append(f"|  [+] Gift: {self.current_visit.gift_brought:^31}  |")
        
        lines.extend([
            "+===============================================+",
            "|  [C]hat  [P]lay  [G]ive Gift  [B]ye          |",
            "+===============================================+",
        ])
        
        return lines
    
    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "friends": {
                fid: {
                    "id": f.id,
                    "name": f.name,
                    "personality": f.personality.value,
                    "friendship_level": f.friendship_level.value,
                    "friendship_points": f.friendship_points,
                    "times_visited": f.times_visited,
                    "gifts_given": f.gifts_given,
                    "gifts_received": f.gifts_received,
                    "favorite_food": f.favorite_food,
                    "favorite_activity": f.favorite_activity,
                    "first_met": f.first_met,
                    "last_visit": f.last_visit,
                    "special_memories": f.special_memories,
                    "unlocked_dialogue": f.unlocked_dialogue,
                    "conversation_topics": f.conversation_topics,
                    "shared_experiences": f.shared_experiences,
                    "gifts_exchanged_history": f.gifts_exchanged_history,
                    "last_conversation_summary": f.last_conversation_summary,
                }
                for fid, f in self.friends.items()
            },
            "current_visit": {
                "friend_id": self.current_visit.friend_id,
                "started_at": self.current_visit.started_at,
                "duration_minutes": self.current_visit.duration_minutes,
                "activities_done": self.current_visit.activities_done,
                "mood": self.current_visit.mood,
                "gift_brought": self.current_visit.gift_brought,
                "waiting_for_gift": self.current_visit.waiting_for_gift,
            } if self.current_visit else None,
            "total_visits": self.total_visits,
            "total_gifts_exchanged": self.total_gifts_exchanged,
            "last_visitor_time": self.last_visitor_time,
            "best_friend_id": self.best_friend_id,
            "pending_invitations": self.pending_invitations,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "FriendsSystem":
        """Create from dictionary."""
        system = cls()
        
        for fid, fdata in data.get("friends", {}).items():
            system.friends[fid] = DuckFriend(
                id=fdata["id"],
                name=fdata["name"],
                personality=DuckPersonalityType(fdata["personality"]),
                friendship_level=FriendshipLevel(fdata["friendship_level"]),
                friendship_points=fdata.get("friendship_points", 0),
                times_visited=fdata.get("times_visited", 0),
                gifts_given=fdata.get("gifts_given", 0),
                gifts_received=fdata.get("gifts_received", 0),
                favorite_food=fdata.get("favorite_food", "bread"),
                favorite_activity=fdata.get("favorite_activity", "chat"),
                first_met=fdata.get("first_met", ""),
                last_visit=fdata.get("last_visit", ""),
                special_memories=fdata.get("special_memories", []),
                unlocked_dialogue=fdata.get("unlocked_dialogue", []),
                conversation_topics=fdata.get("conversation_topics", []),
                shared_experiences=fdata.get("shared_experiences", []),
                gifts_exchanged_history=fdata.get("gifts_exchanged_history", []),
                last_conversation_summary=fdata.get("last_conversation_summary", ""),
            )
        
        visit_data = data.get("current_visit")
        if visit_data:
            system.current_visit = VisitEvent(
                friend_id=visit_data["friend_id"],
                started_at=visit_data["started_at"],
                duration_minutes=visit_data["duration_minutes"],
                activities_done=visit_data.get("activities_done", []),
                mood=visit_data.get("mood", "happy"),
                gift_brought=visit_data.get("gift_brought"),
                waiting_for_gift=visit_data.get("waiting_for_gift", False),
            )
        
        system.total_visits = data.get("total_visits", 0)
        system.total_gifts_exchanged = data.get("total_gifts_exchanged", 0)
        system.last_visitor_time = data.get("last_visitor_time", "")
        system.best_friend_id = data.get("best_friend_id")
        system.pending_invitations = data.get("pending_invitations", [])
        
        return system


# Global friends system instance
friends_system = FriendsSystem()
