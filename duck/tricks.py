"""
Duck Tricks System - Learnable tricks, skills, and performances.
Features training progression, combo moves, and performance rewards.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random
import threading


class TrickDifficulty(Enum):
    """Difficulty levels for tricks."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    MASTER = "master"
    LEGENDARY = "legendary"


class TrickCategory(Enum):
    """Categories of tricks."""
    MOVEMENT = "movement"
    SOUND = "sound"
    SOCIAL = "social"
    SPECIAL = "special"
    COMBO = "combo"


@dataclass
class Trick:
    """A trick the duck can learn."""
    id: str
    name: str
    description: str
    category: TrickCategory
    difficulty: TrickDifficulty
    training_required: int  # Number of training sessions needed
    xp_reward: int
    coin_reward: int
    animation: List[str]  # ASCII animation frames
    prerequisite_tricks: List[str] = field(default_factory=list)
    mood_bonus: int = 0
    special_effect: Optional[str] = None


@dataclass
class LearnedTrick:
    """A trick the duck has learned."""
    trick_id: str
    learned_at: str
    training_progress: int
    times_performed: int = 0
    mastery_level: int = 1  # 1-5 mastery
    last_performed: str = ""
    perfect_performances: int = 0


# Trick Definitions
TRICKS: Dict[str, Trick] = {
    # Movement Tricks - Easy
    "waddle_dance": Trick(
        id="waddle_dance",
        name="Waddle Dance",
        description="An adorable side-to-side waddle dance!",
        category=TrickCategory.MOVEMENT,
        difficulty=TrickDifficulty.EASY,
        training_required=3,
        xp_reward=15,
        coin_reward=5,
        animation=[
            "  <(.)  ",
            "   (.)> ",
            "  <(.)  ",
        ],
        mood_bonus=5,
    ),
    "spin": Trick(
        id="spin",
        name="Spin",
        description="Spin around in a circle!",
        category=TrickCategory.MOVEMENT,
        difficulty=TrickDifficulty.EASY,
        training_required=2,
        xp_reward=10,
        coin_reward=3,
        animation=[
            "  (.)  ",
            " .(.)  ",
            " .(..) ",
            "  (.)  ",
        ],
        mood_bonus=3,
    ),
    "hop": Trick(
        id="hop",
        name="Happy Hop",
        description="Jump up and down excitedly!",
        category=TrickCategory.MOVEMENT,
        difficulty=TrickDifficulty.EASY,
        training_required=2,
        xp_reward=10,
        coin_reward=3,
        animation=[
            "       ",
            "  (.)  ",
            "  ^^^  ",
            "  (.)  ",
        ],
        mood_bonus=5,
    ),
    
    # Movement Tricks - Medium
    "backflip": Trick(
        id="backflip",
        name="Backflip",
        description="An impressive backwards somersault!",
        category=TrickCategory.MOVEMENT,
        difficulty=TrickDifficulty.MEDIUM,
        training_required=8,
        xp_reward=35,
        coin_reward=15,
        animation=[
            "   (.)  ",
            "    ^   ",
            "   (')  ",
            "  (.°)  ",
            "   (.)  ",
        ],
        prerequisite_tricks=["hop"],
        mood_bonus=10,
    ),
    "moonwalk": Trick(
        id="moonwalk",
        name="Moonwalk",
        description="Smooth backwards sliding walk!",
        category=TrickCategory.MOVEMENT,
        difficulty=TrickDifficulty.MEDIUM,
        training_required=6,
        xp_reward=30,
        coin_reward=12,
        animation=[
            "(.)    ->",
            " (.)   ->",
            "  (.)  ->",
            "   (.) ->",
        ],
        prerequisite_tricks=["waddle_dance"],
        mood_bonus=8,
    ),
    
    # Movement Tricks - Hard
    "double_flip": Trick(
        id="double_flip",
        name="Double Flip",
        description="Two flips in a row!",
        category=TrickCategory.MOVEMENT,
        difficulty=TrickDifficulty.HARD,
        training_required=15,
        xp_reward=75,
        coin_reward=40,
        animation=[
            "   (.) ",
            "   ^^  ",
            "  (°.) ",
            " (.°)  ",
            "   (.) ",
        ],
        prerequisite_tricks=["backflip"],
        mood_bonus=15,
        special_effect="double_xp_next_action",
    ),
    
    # Sound Tricks
    "quack_song": Trick(
        id="quack_song",
        name="Quack Song",
        description="Sing a beautiful quacking melody!",
        category=TrickCategory.SOUND,
        difficulty=TrickDifficulty.EASY,
        training_required=3,
        xp_reward=12,
        coin_reward=5,
        animation=[
            " (.) # ",
            " (.) # ",
            " (.) ##",
        ],
        mood_bonus=8,
    ),
    "beatbox": Trick(
        id="beatbox",
        name="Duck Beatbox",
        description="Drop some sick beats!",
        category=TrickCategory.SOUND,
        difficulty=TrickDifficulty.MEDIUM,
        training_required=7,
        xp_reward=30,
        coin_reward=15,
        animation=[
            " (.) # ",
            " (•)BOO",
            " (.)TSS",
            " (•)BAP",
        ],
        prerequisite_tricks=["quack_song"],
        mood_bonus=12,
    ),
    "whistle": Trick(
        id="whistle",
        name="Perfect Whistle",
        description="Whistle a tune perfectly!",
        category=TrickCategory.SOUND,
        difficulty=TrickDifficulty.MEDIUM,
        training_required=5,
        xp_reward=25,
        coin_reward=10,
        animation=[
            " (.) ~~~ ",
            " (°) ~~~°",
        ],
        mood_bonus=5,
    ),
    
    # Social Tricks
    "wave": Trick(
        id="wave",
        name="Friendly Wave",
        description="Wave hello to everyone!",
        category=TrickCategory.SOCIAL,
        difficulty=TrickDifficulty.EASY,
        training_required=2,
        xp_reward=10,
        coin_reward=3,
        animation=[
            " (.)/ ",
            " (.)| ",
            " (.)/ ",
        ],
        mood_bonus=5,
    ),
    "bow": Trick(
        id="bow",
        name="Elegant Bow",
        description="Take a graceful bow!",
        category=TrickCategory.SOCIAL,
        difficulty=TrickDifficulty.EASY,
        training_required=3,
        xp_reward=12,
        coin_reward=5,
        animation=[
            "  (.) ",
            "  (°) ",
            " (___)  ",
        ],
        mood_bonus=5,
    ),
    "high_five": Trick(
        id="high_five",
        name="High Five",
        description="Give someone a wing high-five!",
        category=TrickCategory.SOCIAL,
        difficulty=TrickDifficulty.MEDIUM,
        training_required=4,
        xp_reward=20,
        coin_reward=8,
        animation=[
            "    \\|",
            " (.)/ ",
            "    * ",
        ],
        prerequisite_tricks=["wave"],
        mood_bonus=10,
    ),
    
    # Special Tricks
    "play_dead": Trick(
        id="play_dead",
        name="Play Dead",
        description="Dramatically pretend to faint!",
        category=TrickCategory.SPECIAL,
        difficulty=TrickDifficulty.MEDIUM,
        training_required=6,
        xp_reward=25,
        coin_reward=12,
        animation=[
            "  (.) ",
            "  (x) ",
            " ___x ",
        ],
        mood_bonus=3,
    ),
    "peek_a_boo": Trick(
        id="peek_a_boo",
        name="Peek-a-Boo",
        description="Play peek-a-boo with wing covers!",
        category=TrickCategory.SPECIAL,
        difficulty=TrickDifficulty.EASY,
        training_required=3,
        xp_reward=15,
        coin_reward=5,
        animation=[
            " |.| ",
            " |(.)| ",
            " |.| ",
            " (^.^) ",
        ],
        mood_bonus=10,
    ),
    "magic_trick": Trick(
        id="magic_trick",
        name="Magic Trick",
        description="Perform an amazing magic trick!",
        category=TrickCategory.SPECIAL,
        difficulty=TrickDifficulty.HARD,
        training_required=12,
        xp_reward=60,
        coin_reward=35,
        animation=[
            "  (.) ",
            " *(.)* ",
            "  *   ",
            " POOF! ",
        ],
        prerequisite_tricks=["bow", "wave"],
        mood_bonus=20,
        special_effect="bonus_coins",
    ),
    
    # Combo Tricks
    "dance_routine": Trick(
        id="dance_routine",
        name="Full Dance Routine",
        description="A complete choreographed dance!",
        category=TrickCategory.COMBO,
        difficulty=TrickDifficulty.MASTER,
        training_required=20,
        xp_reward=100,
        coin_reward=60,
        animation=[
            "  (.) ",
            " <(.)>",
            "  ^^  ",
            " .(.) ",
            "  (°) ",
        ],
        prerequisite_tricks=["waddle_dance", "spin", "hop"],
        mood_bonus=25,
        special_effect="attract_visitors",
    ),
    "legendary_performance": Trick(
        id="legendary_performance",
        name="Legendary Performance",
        description="The ultimate duck performance!",
        category=TrickCategory.COMBO,
        difficulty=TrickDifficulty.LEGENDARY,
        training_required=50,
        xp_reward=500,
        coin_reward=300,
        animation=[
            "   *   ",
            " *(.)* ",
            "  **  ",
            " *** ",
        ],
        prerequisite_tricks=["dance_routine", "magic_trick", "double_flip"],
        mood_bonus=50,
        special_effect="legendary_reward",
    ),

    # === NEW SOUND TRICKS ===
    "duck_impressions": Trick(
        id="duck_impressions",
        name="Duck Impressions",
        description="Impressions of other birds. they're all just worse ducks.",
        category=TrickCategory.SOUND,
        difficulty=TrickDifficulty.EASY,
        training_required=3,
        xp_reward=12,
        coin_reward=5,
        animation=[
            " (.) caw? ",
            " (.) hoot.",
            " (.) ...  ",
            " (.) quack.",
        ],
        mood_bonus=6,
    ),
    "whistle_melody": Trick(
        id="whistle_melody",
        name="Whistle Concerto",
        description="a 47-second whistled composition. every note deliberate.",
        category=TrickCategory.SOUND,
        difficulty=TrickDifficulty.HARD,
        training_required=14,
        xp_reward=65,
        coin_reward=35,
        animation=[
            " (.) ~~    ",
            " (°) ~~°~  ",
            " (.) ~~~°~ ",
            " (°) ~~~~°~",
            " (.)  ...  ",
        ],
        prerequisite_tricks=["whistle"],
        mood_bonus=15,
        special_effect="mood_boost_nearby",
    ),
    "beatbox_drop": Trick(
        id="beatbox_drop",
        name="Bass Drop",
        description="beatbox but then the bass drops. feathers vibrate.",
        category=TrickCategory.SOUND,
        difficulty=TrickDifficulty.HARD,
        training_required=12,
        xp_reward=60,
        coin_reward=30,
        animation=[
            " (.) ts ts ",
            " (•) bm bm ",
            " (.) BWAAAA",
            " (°)  ...  ",
            " (.)       ",
        ],
        prerequisite_tricks=["beatbox"],
        mood_bonus=14,
    ),
    "quack_harmony": Trick(
        id="quack_harmony",
        name="Quack Harmony",
        description="harmonized quacking. don't ask how one duck does harmony.",
        category=TrickCategory.SOUND,
        difficulty=TrickDifficulty.MEDIUM,
        training_required=6,
        xp_reward=28,
        coin_reward=12,
        animation=[
            " (.) # # ",
            " (.) ## ##",
            " (.) #####",
        ],
        prerequisite_tricks=["quack_song"],
        mood_bonus=10,
    ),

    # === NEW SOCIAL TRICKS ===
    "salute": Trick(
        id="salute",
        name="Wing Salute",
        description="a crisp military salute. for no one in particular.",
        category=TrickCategory.SOCIAL,
        difficulty=TrickDifficulty.EASY,
        training_required=2,
        xp_reward=10,
        coin_reward=4,
        animation=[
            "  (.)7 ",
            "  (.)7 ",
            "  (.)  ",
        ],
        mood_bonus=4,
    ),
    "wing_shake": Trick(
        id="wing_shake",
        name="Wing Shake",
        description="the duck equivalent of a handshake. very professional.",
        category=TrickCategory.SOCIAL,
        difficulty=TrickDifficulty.MEDIUM,
        training_required=5,
        xp_reward=22,
        coin_reward=10,
        animation=[
            "  (.)/ |  ",
            "  (.)/-|  ",
            "  (.)/ |  ",
        ],
        prerequisite_tricks=["wave"],
        mood_bonus=8,
    ),
    "group_cheer": Trick(
        id="group_cheer",
        name="Group Cheer",
        description="rallies the whole pond. reluctantly charismatic.",
        category=TrickCategory.SOCIAL,
        difficulty=TrickDifficulty.HARD,
        training_required=10,
        xp_reward=55,
        coin_reward=28,
        animation=[
            "  (.)/ \\(.)",
            " \\(.)/ (.) ",
            "  (.)/ \\(.)",
            "   * * *   ",
        ],
        prerequisite_tricks=["high_five", "wave"],
        mood_bonus=18,
        special_effect="attract_visitors",
    ),
    "curtsy": Trick(
        id="curtsy",
        name="Fancy Curtsy",
        description="an unnecessarily elegant curtsy. pinky out.",
        category=TrickCategory.SOCIAL,
        difficulty=TrickDifficulty.MEDIUM,
        training_required=5,
        xp_reward=20,
        coin_reward=10,
        animation=[
            "  (.)  ",
            " /(.)  ",
            " /___\\ ",
            "  (.)  ",
        ],
        prerequisite_tricks=["bow"],
        mood_bonus=7,
    ),

    # === NEW SPECIAL TRICKS ===
    "meditation": Trick(
        id="meditation",
        name="Duck Meditation",
        description="absolute stillness. possibly transcending. possibly napping.",
        category=TrickCategory.SPECIAL,
        difficulty=TrickDifficulty.MEDIUM,
        training_required=7,
        xp_reward=30,
        coin_reward=12,
        animation=[
            "  (.)  ",
            " ~(-)~ ",
            " ~(-)~ ",
            "  ommm ",
        ],
        mood_bonus=20,
        special_effect="mood_restore",
    ),
    "disappearing_act": Trick(
        id="disappearing_act",
        name="Disappearing Act",
        description="now you see cheese. now you don't. *still here though*",
        category=TrickCategory.SPECIAL,
        difficulty=TrickDifficulty.HARD,
        training_required=12,
        xp_reward=65,
        coin_reward=35,
        animation=[
            "  (.)  ",
            " *(.)* ",
            "  *.*  ",
            "       ",
            "  (.)  ",
        ],
        prerequisite_tricks=["play_dead"],
        mood_bonus=12,
    ),
    "bread_summoning": Trick(
        id="bread_summoning",
        name="Bread Summoning",
        description="the sacred ritual. calls bread from the beyond. IT IS REAL.",
        category=TrickCategory.SPECIAL,
        difficulty=TrickDifficulty.MASTER,
        training_required=25,
        xp_reward=120,
        coin_reward=70,
        animation=[
            "  (.)   ",
            " *(.)* ~",
            " *\\.//* ",
            "  [==]  ",
            " *BREAD*",
        ],
        prerequisite_tricks=["magic_trick"],
        mood_bonus=35,
        special_effect="bonus_food",
    ),
    "statue_pose": Trick(
        id="statue_pose",
        name="Statue Pose",
        description="perfectly still. a monument to duck. you may weep.",
        category=TrickCategory.SPECIAL,
        difficulty=TrickDifficulty.EASY,
        training_required=3,
        xp_reward=12,
        coin_reward=5,
        animation=[
            "  (.)  ",
            "  (.)  ",
            "  (.)  ",
        ],
        mood_bonus=5,
    ),

    # === NEW COMBO TRICKS ===
    "musical_revue": Trick(
        id="musical_revue",
        name="Musical Revue",
        description="a full musical number. singing. dancing. regret.",
        category=TrickCategory.COMBO,
        difficulty=TrickDifficulty.MASTER,
        training_required=22,
        xp_reward=110,
        coin_reward=65,
        animation=[
            " (.) # # ",
            " (•)BOO# ",
            " (.) ~~~~",
            " <(.)>   ",
            "  * * *  ",
        ],
        prerequisite_tricks=["beatbox", "whistle", "quack_song"],
        mood_bonus=28,
        special_effect="attract_visitors",
    ),
    "social_butterfly": Trick(
        id="social_butterfly",
        name="Social Butterfly",
        description="a charm offensive. every social trick chained. exhausting.",
        category=TrickCategory.COMBO,
        difficulty=TrickDifficulty.MASTER,
        training_required=20,
        xp_reward=100,
        coin_reward=55,
        animation=[
            "  (.)7  ",
            "  (.)/-|",
            " /(.)   ",
            "  (.)/ *",
        ],
        prerequisite_tricks=["salute", "wing_shake", "bow"],
        mood_bonus=25,
        special_effect="relationship_boost",
    ),
    "grand_illusion": Trick(
        id="grand_illusion",
        name="Grand Illusion",
        description="disappears. summons bread. reappears. no one claps. typical.",
        category=TrickCategory.COMBO,
        difficulty=TrickDifficulty.LEGENDARY,
        training_required=45,
        xp_reward=450,
        coin_reward=250,
        animation=[
            "  (.)   ",
            " *(.)* ~",
            "        ",
            " *[==]* ",
            "  (.)   ",
            " * ** * ",
        ],
        prerequisite_tricks=["disappearing_act", "bread_summoning", "magic_trick"],
        mood_bonus=45,
        special_effect="legendary_reward",
    ),
}


# ============================================================
# Dialogue Pools for Trick System
# ============================================================

TRICK_ATTEMPT_MESSAGES: Dict[str, List[str]] = {
    "easy": [
        "*stretches wing* ...fine. watch.",
        "this one I can do in my sleep. I HAVE done it in my sleep.",
        "*sighs* the things I do for bread.",
        "hold on. let me get into position. ...ok I was already in position.",
        "don't blink. actually, blink. it's not that fast.",
        "*adjusts feathers* presenting.",
        "I've done this literally hundreds of times. the magic is gone.",
    ],
    "medium": [
        "*cracks neck* this one requires FOCUS.",
        "ok. this is a real trick. no more baby stuff.",
        "*takes a breath* don't talk to me for a second.",
        "I need complete silence. ...that means you.",
        "watched a professional duck do this once. how hard can it be.",
        "*shakes out wings* let's see if the training paid off.",
        "this would be easier with bread as motivation. just saying.",
        "*stares at the ground* ...calculating.",
    ],
    "hard": [
        "*long pause* ...I'm not nervous. ducks don't GET nervous.",
        "this trick has a 30 percent failure rate. for OTHER ducks.",
        "if I pull this off, you owe me bread. GOOD bread.",
        "*flexes wings slowly* ok. HERE WE GO.",
        "don't record this. if I fail there can be no evidence.",
        "I trained for this. the montage was very inspiring.",
        "*deep breath* ...the things I do for your entertainment.",
    ],
    "master": [
        "*stares into the distance* few ducks have attempted this.",
        "I need a moment. this is ADVANCED. don't rush art.",
        "*closes eyes* channeling the ancient duck masters.",
        "if something goes wrong, tell the bread I loved it.",
        "this trick cost me three feathers in training. worth it.",
        "*stands perfectly still for ten seconds* ...NOW.",
        "you're about to witness history. or a very funny failure.",
        "*mutters calculations under breath* ok. ready.",
    ],
    "legendary": [
        "*the air gets heavy* ...you sure about this.",
        "this trick exists in THEORY. I am the theory now.",
        "*every feather stands on end* ...witness me.",
        "they said it couldn't be done. they were almost right.",
        "if I don't come back from this, my bread goes to charity.",
        "*the pond goes silent* even the fish are watching.",
        "legends speak of this trick. I AM the legend now. probably.",
        "*vibrating slightly* this is either greatness or a disaster.",
    ],
}

TRICK_FAILURE_MESSAGES: Dict[str, List[str]] = {
    "easy": [
        "...that wasn't supposed to happen.",
        "*looks at own wings* traitors.",
        "I KNOW how to do this. my body just... disagreed.",
        "the ground was uneven. that's my story.",
        "*walks away* we never speak of this.",
        "blame the wind. there was wind. I felt it.",
        "*blinks* ...I was doing a DIFFERENT trick. on purpose.",
    ],
    "medium": [
        "*lying on ground* ...I'm fine. this is fine.",
        "that was a PRACTICE run. the real one is next.",
        "I'd like to see YOU try it with wings instead of hands.",
        "*dusts self off* gravity is a personal enemy at this point.",
        "the trick worked. you just weren't looking at the right part.",
        "I need more training. and bread. mostly bread.",
        "*stares at sky* the universe conspires against me.",
        "my mentor never warned me about days like this.",
    ],
    "hard": [
        "*face down* ...leave me here.",
        "that was CLOSE. you didn't see how close that was.",
        "I blame the audience. your energy was OFF.",
        "*slowly stands up* we're going to pretend that didn't happen.",
        "the trick requires conditions I cannot control. like luck.",
        "I almost had it. almost counts in bread and horseshoes.",
        "*shaking* that trick owes me a FEATHER.",
    ],
    "master": [
        "*lying very still* ...I have achieved a different kind of mastery.",
        "the ancient duck masters didn't have to deal with this nonsense.",
        "I need a moment. and possibly medical attention.",
        "*covered in pond water* that was the warm-up. clearly.",
        "mastery takes time. today was not the time.",
        "*whispering* the bread gods have forsaken me.",
        "that trick beat me today. ONLY today.",
        "I'll be back. tell the trick I'll be back.",
    ],
}

TRICK_MASTERY_MESSAGES: Dict[int, List[str]] = {
    1: [
        "*looks at own wings* ...huh. I can do that now.",
        "learned it. not WELL. but learned.",
        "filed under: things I can technically do.",
        "the journey of a thousand tricks begins with one barely-passable attempt.",
    ],
    2: [
        "getting better at this. don't make it weird.",
        "*nods* ok. that's starting to feel natural.",
        "the muscle memory is forming. or whatever ducks have instead of muscles.",
        "I can do this without thinking now. which is how I prefer to do everything.",
    ],
    3: [
        "*polishes wing* I'm genuinely good at this now.",
        "proficiency achieved. the trick fears me.",
        "this is the part where lesser ducks peak. not me.",
        "I could do this in a storm. I WON'T. but I could.",
    ],
    4: [
        "*adjusts invisible monocle* expert level. obviously.",
        "I've elevated this trick to an art form. you're welcome.",
        "other ducks ask me for tips now. I charge bread.",
        "at this level, the trick does itself. I just show up.",
    ],
    5: [
        "*glowing faintly* ...I have become the trick.",
        "mastery. the trick and I are one. this is either beautiful or concerning.",
        "PEAK. DUCK. PERFORMANCE. *adjusts feathers calmly*",
        "there is nothing more to learn. I am the teacher now.",
    ],
}

TRICK_AUDIENCE_REACTIONS: List[str] = [
    "*a visitor claps politely* ...that's more than I usually get.",
    "someone in the back yelled encore. I choose to believe they meant it.",
    "*scattered applause* the crowd goes mild.",
    "a child pointed at me and said 'funny bird.' close enough to praise.",
    "*one person takes a photo* I better not end up on the internet.",
    "the silence after the trick was... respectful. I'll take it.",
    "*a visitor throws bread* NOW we're talking. best review I've ever gotten.",
    "someone whispered 'is that duck ok.' I'm MORE than ok.",
    "*two visitors debate whether that was impressive* it WAS. case closed.",
    "a very small child cried. from JOY. probably.",
    "*a visitor nods slowly* they understand. they GET it.",
    "someone said 'my dog can do that.' your dog is a LIAR.",
]


class TricksSystem:
    """
    Manages duck tricks, training, and performances.
    """
    
    def __init__(self):
        self.learned_tricks: Dict[str, LearnedTrick] = {}
        self.training_progress: Dict[str, int] = {}  # trick_id -> sessions completed
        self.total_performances: int = 0
        self.total_perfect_performances: int = 0
        self.current_training: Optional[str] = None
        self.training_streak: int = 0
        self.last_training_date: str = ""
        self.favorite_trick: Optional[str] = None
        self.combo_streak: int = 0
        self.highest_combo: int = 0
    
    def get_available_tricks(self) -> List[Trick]:
        """Get tricks available to learn."""
        available = []
        
        for trick_id, trick in TRICKS.items():
            # Already learned
            if trick_id in self.learned_tricks:
                continue
            
            # Check prerequisites
            prereqs_met = all(
                pt in self.learned_tricks
                for pt in trick.prerequisite_tricks
            )
            
            if prereqs_met:
                available.append(trick)
        
        return available
    
    def start_training(self, trick_id: str, duck_trust: float = 100.0) -> Tuple[bool, str]:
        """Start training a trick.
        
        Args:
            trick_id: The trick to start training
            duck_trust: Current trust level (0-100). Higher-difficulty tricks
                require more trust — the duck won't learn from someone it
                doesn't trust yet.
        """
        if trick_id in self.learned_tricks:
            return False, "Already learned this trick!"
        
        trick = TRICKS.get(trick_id)
        if not trick:
            return False, "Trick not found!"
        
        # Trust thresholds per difficulty
        trust_required = {
            TrickDifficulty.EASY: 0,
            TrickDifficulty.MEDIUM: 30,
            TrickDifficulty.HARD: 50,
            TrickDifficulty.MASTER: 70,
            TrickDifficulty.LEGENDARY: 85,
        }
        required = trust_required.get(trick.difficulty, 0)
        if duck_trust < required:
            return False, f"*stares* ...I don't trust you enough for that yet. (Need trust: {required}%)"
        
        # Check prerequisites
        for prereq in trick.prerequisite_tricks:
            if prereq not in self.learned_tricks:
                prereq_trick = TRICKS.get(prereq)
                prereq_name = prereq_trick.name if prereq_trick else prereq
                return False, f"Need to learn '{prereq_name}' first!"
        
        self.current_training = trick_id
        
        return True, f"^ Started training: {trick.name}!"
    
    def do_training_session(self) -> Tuple[bool, str, Optional[Trick]]:
        """Complete a training session."""
        if not self.current_training:
            return False, "Not training any trick!", None
        
        trick = TRICKS.get(self.current_training)
        if not trick:
            self.current_training = None
            return False, "Invalid trick!", None
        
        # Update progress
        current = self.training_progress.get(self.current_training, 0)
        self.training_progress[self.current_training] = current + 1
        
        # Update streak
        today = datetime.now().strftime("%Y-%m-%d")
        if self.last_training_date == today:
            pass  # Same day
        elif self.last_training_date:
            try:
                last_date = datetime.fromisoformat(self.last_training_date).date()
                days_since_last_training = datetime.now().date().toordinal() - last_date.toordinal()
                if days_since_last_training == 1:
                    self.training_streak += 1
                else:
                    self.training_streak = 1
            except ValueError:
                self.training_streak = 1  # Reset on parse error
        else:
            self.training_streak = 1
        
        self.last_training_date = today
        
        # Check if learned
        if self.training_progress[self.current_training] >= trick.training_required:
            # Learn the trick!
            self.learned_tricks[self.current_training] = LearnedTrick(
                trick_id=self.current_training,
                learned_at=datetime.now().isoformat(),
                training_progress=trick.training_required,
            )
            
            learned_trick = trick
            self.current_training = None
            
            return True, f"* Learned new trick: {learned_trick.name}!", learned_trick
        
        progress = self.training_progress[self.current_training]
        remaining = trick.training_required - progress
        
        return True, f"[=] Training session complete! {remaining} sessions left until learned.", None
    
    def perform_trick(self, trick_id: str) -> Tuple[bool, str, Dict]:
        """Perform a learned trick."""
        if trick_id not in self.learned_tricks:
            return False, "Haven't learned this trick!", {}
        
        trick = TRICKS.get(trick_id)
        if not trick:
            return False, "Trick not found!", {}
        
        learned = self.learned_tricks[trick_id]
        
        # Calculate performance quality
        base_quality = 70
        mastery_bonus = learned.mastery_level * 5
        experience_bonus = min(learned.times_performed, 20)
        
        quality = base_quality + mastery_bonus + experience_bonus + random.randint(-10, 10)
        quality = max(50, min(100, quality))
        
        # Perfect performance?
        is_perfect = quality >= 95
        
        # Calculate rewards
        xp = trick.xp_reward
        coins = trick.coin_reward
        
        if is_perfect:
            xp = int(xp * 1.5)
            coins = int(coins * 1.5)
            learned.perfect_performances += 1
            self.total_perfect_performances += 1
        
        quality_multiplier = quality / 100
        xp = int(xp * quality_multiplier)
        coins = int(coins * quality_multiplier)
        
        # Update stats
        learned.times_performed += 1
        learned.last_performed = datetime.now().isoformat()
        self.total_performances += 1
        
        # Check for mastery level up
        mastery_thresholds = [5, 15, 30, 50, 100]
        if learned.mastery_level < 5:
            if learned.times_performed >= mastery_thresholds[learned.mastery_level - 1]:
                learned.mastery_level += 1
        
        # Performance rating
        if quality >= 95:
            rating = "*** PERFECT!"
        elif quality >= 85:
            rating = "** Excellent!"
        elif quality >= 70:
            rating = "* Good!"
        else:
            rating = "Nice try!"
        
        results = {
            "quality": quality,
            "rating": rating,
            "xp": xp,
            "coins": coins,
            "is_perfect": is_perfect,
            "mastery_level": learned.mastery_level,
            "mood_bonus": trick.mood_bonus,
            "special_effect": trick.special_effect if is_perfect else None,
            "animation": trick.animation,
        }
        
        return True, f"* {trick.name} - {rating}", results
    
    def perform_combo(self, trick_ids: List[str]) -> Tuple[bool, str, Dict]:
        """Perform multiple tricks in a combo."""
        if len(trick_ids) < 2:
            return False, "Combos need at least 2 tricks!", {}
        
        # Verify all tricks are learned
        for tid in trick_ids:
            if tid not in self.learned_tricks:
                return False, f"Haven't learned {tid}!", {}
        
        total_xp = 0
        total_coins = 0
        total_mood = 0
        combo_multiplier = 1.0 + (len(trick_ids) - 1) * 0.25  # 25% bonus per additional trick
        
        results = []
        for tid in trick_ids:
            success, msg, result = self.perform_trick(tid)
            if success:
                results.append(result)
                total_xp += result["xp"]
                total_coins += result["coins"]
                total_mood += result["mood_bonus"]
        
        # Apply combo multiplier
        total_xp = int(total_xp * combo_multiplier)
        total_coins = int(total_coins * combo_multiplier)
        
        self.combo_streak = len(trick_ids)
        if self.combo_streak > self.highest_combo:
            self.highest_combo = self.combo_streak
        
        return True, f"^ {len(trick_ids)}-Hit Combo! ({combo_multiplier:.0%} bonus)", {
            "total_xp": total_xp,
            "total_coins": total_coins,
            "total_mood": total_mood,
            "combo_size": len(trick_ids),
            "combo_multiplier": combo_multiplier,
            "trick_results": results,
        }
    
    def get_training_status(self) -> Dict:
        """Get current training status."""
        if not self.current_training:
            return {"training": False}
        
        trick = TRICKS.get(self.current_training)
        if not trick:
            return {"training": False}
        
        progress = self.training_progress.get(self.current_training, 0)
        
        return {
            "training": True,
            "trick_name": trick.name,
            "progress": progress,
            "required": trick.training_required,
            "percent": (progress / trick.training_required) * 100,
        }
    
    def render_trick_list(self) -> List[str]:
        """Render the list of tricks."""
        lines = [
            "+===============================================+",
            "|            * DUCK TRICKS *                  |",
            "+===============================================+",
            f"|  Learned: {len(self.learned_tricks):2}  |  Performances: {self.total_performances:5}       |",
            f"|  Perfect: {self.total_perfect_performances:3}  |  Highest Combo: {self.highest_combo:2}          |",
            "+===============================================+",
            "|  LEARNED TRICKS:                              |",
        ]
        
        for tid, learned in list(self.learned_tricks.items())[:5]:
            trick = TRICKS.get(tid)
            if trick:
                stars = "*" * learned.mastery_level + "*" * (5 - learned.mastery_level)
                lines.append(f"|   {trick.name[:20]:20} {stars}         |")
        
        if not self.learned_tricks:
            lines.append("|   No tricks learned yet!                      |")
        
        # Training status
        status = self.get_training_status()
        if status["training"]:
            lines.append("+===============================================+")
            lines.append(f"|  Training: {status['trick_name'][:28]:28}   |")
            lines.append(f"|  Progress: {status['progress']}/{status['required']} ({status['percent']:.0f}%)                      |")
        
        # Available to learn
        available = self.get_available_tricks()
        if available:
            lines.append("+===============================================+")
            lines.append("|  AVAILABLE TO LEARN:                          |")
            for trick in available[:3]:
                diff_icon = {"easy": "O", "medium": "O", "hard": "O", "master": "O", "legendary": "*"}.get(trick.difficulty.value, "o")
                lines.append(f"|   {diff_icon} {trick.name[:33]:33}   |")
        
        lines.append("+===============================================+")
        
        return lines
    
    def render_trick_performance(self, trick_id: str) -> List[str]:
        """Render trick performance animation."""
        trick = TRICKS.get(trick_id)
        if not trick:
            return ["Trick not found!"]
        
        lines = [
            "+===============================================+",
            f"|        * {trick.name:^28} *        |",
            "+===============================================+",
        ]
        
        for frame in trick.animation:
            lines.append(f"|           {frame:^30}          |")
        
        lines.append("+===============================================+")
        
        return lines
    
    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "learned_tricks": {
                tid: {
                    "trick_id": lt.trick_id,
                    "learned_at": lt.learned_at,
                    "training_progress": lt.training_progress,
                    "times_performed": lt.times_performed,
                    "mastery_level": lt.mastery_level,
                    "last_performed": lt.last_performed,
                    "perfect_performances": lt.perfect_performances,
                }
                for tid, lt in self.learned_tricks.items()
            },
            "training_progress": self.training_progress,
            "total_performances": self.total_performances,
            "total_perfect_performances": self.total_perfect_performances,
            "current_training": self.current_training,
            "training_streak": self.training_streak,
            "last_training_date": self.last_training_date,
            "favorite_trick": self.favorite_trick,
            "combo_streak": self.combo_streak,
            "highest_combo": self.highest_combo,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "TricksSystem":
        """Create from dictionary."""
        system = cls()
        
        for tid, tdata in data.get("learned_tricks", {}).items():
            system.learned_tricks[tid] = LearnedTrick(
                trick_id=tdata["trick_id"],
                learned_at=tdata["learned_at"],
                training_progress=tdata.get("training_progress", 0),
                times_performed=tdata.get("times_performed", 0),
                mastery_level=tdata.get("mastery_level", 1),
                last_performed=tdata.get("last_performed", ""),
                perfect_performances=tdata.get("perfect_performances", 0),
            )
        
        system.training_progress = data.get("training_progress", {})
        system.total_performances = data.get("total_performances", 0)
        system.total_perfect_performances = data.get("total_perfect_performances", 0)
        system.current_training = data.get("current_training")
        system.training_streak = data.get("training_streak", 0)
        system.last_training_date = data.get("last_training_date", "")
        system.favorite_trick = data.get("favorite_trick")
        system.combo_streak = data.get("combo_streak", 0)
        system.highest_combo = data.get("highest_combo", 0)
        
        return system


# Lazy singleton pattern with thread-safe initialization
_tricks_system: Optional[TricksSystem] = None
_tricks_system_lock = threading.Lock()


def get_tricks_system() -> TricksSystem:
    """Get the global tricks system instance (lazy initialization). Thread-safe."""
    global _tricks_system
    if _tricks_system is None:
        with _tricks_system_lock:
            if _tricks_system is None:
                _tricks_system = TricksSystem()
    return _tricks_system


# Module-level accessor for backwards compatibility (uses singleton)
tricks_system = get_tricks_system()
