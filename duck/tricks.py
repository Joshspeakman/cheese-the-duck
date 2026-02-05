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
}


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
    
    def start_training(self, trick_id: str) -> Tuple[bool, str]:
        """Start training a trick."""
        if trick_id in self.learned_tricks:
            return False, "Already learned this trick!"
        
        trick = TRICKS.get(trick_id)
        if not trick:
            return False, "Trick not found!"
        
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
