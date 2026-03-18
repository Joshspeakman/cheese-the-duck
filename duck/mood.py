"""
Mood system - calculates duck's emotional state from needs.
Includes 8 moods: 6 score-based + 2 contextual overrides (DRAMATIC, PETTY).
"""
from typing import List, Optional
from collections import deque
from dataclasses import dataclass
from enum import Enum

from config import (
    MOOD_THRESHOLDS, MOOD_WEIGHTS,
    MOOD_DRAMATIC_NEED_VARIANCE, MOOD_DRAMATIC_SWING_THRESHOLD,
    MOOD_PETTY_RECOVERY_FLOOR, MOOD_PETTY_CURRENT_MIN,
    MOOD_PETTY_HISTORY_DEPTH,
)


class MoodState(Enum):
    """Possible mood states for the duck."""
    ECSTATIC = "ecstatic"
    HAPPY = "happy"
    CONTENT = "content"
    GRUMPY = "grumpy"
    SAD = "sad"
    MISERABLE = "miserable"
    # Contextual overrides — triggered by conditions, not raw score
    DRAMATIC = "dramatic"
    PETTY = "petty"


@dataclass
class MoodInfo:
    """Container for mood information."""
    state: MoodState
    score: float
    description: str
    can_play: bool = True
    can_learn: bool = True


# Mood descriptions and effects
MOOD_DATA = {
    MoodState.ECSTATIC: {
        "description": "suspiciously smug about life",
        "descriptions": [
            "radiating an alarming amount of duck satisfaction",
            "acting like he just got away with something",
            "smugness levels reaching critical mass",
            "vibrating at a frequency only happy ducks understand",
        ],
        "expressions": [
            "!!", "^o^", "*gloat*", "*preen*", "*strut*",
            "*radiant*", "^v^", "*smug waggle*", "*victory lap*", "*bask*",
        ],
        "can_play": True,
        "can_learn": True,
    },
    MoodState.HAPPY: {
        "description": "tolerating existence quite well",
        "descriptions": [
            "begrudgingly admitting today is fine",
            "allowing himself a small, dignified happiness",
            "suspiciously unbothered by everything",
            "almost caught smiling. almost.",
            "willing to admit the pond is acceptable today",
        ],
        "expressions": [
            "^-^", ":)", "*waggle*", "*content quack*", "*small nod*",
            "*gentle preen*", ":3", "*satisfied ruffle*", "~v~", "*blink blink*",
        ],
        "can_play": True,
        "can_learn": True,
    },
    MoodState.CONTENT: {
        "description": "not actively plotting revenge",
        "descriptions": [
            "existing. that's it. that's the description",
            "maintaining a carefully neutral vibe",
            "neither impressed nor disappointed. rare.",
            "tolerating the passage of time with grace",
        ],
        "expressions": [
            "-.-", "~", "*chill*", "*blank stare*", "*float*",
            "*idle preen*", ".", "*zen*", "*neutral waggle*", "*exist*",
        ],
        "can_play": True,
        "can_learn": True,
    },
    MoodState.GRUMPY: {
        "description": "radiating 'don't test me' energy",
        "descriptions": [
            "one inconvenience away from a full meltdown",
            "composing a mental list of grievances",
            "judging everything. everything.",
            "tolerating you. barely.",
            "has chosen violence as a vibe",
        ],
        "expressions": [
            ">:(", "-_-", "*huff*", "*aggressive preen*", "*side-eye*",
            "*sharp quack*", ">:|", "*tail flick*", "*pointed silence*", "*glare*",
        ],
        "can_play": True,
        "can_learn": False,
    },
    MoodState.SAD: {
        "description": "dramatically brooding",
        "descriptions": [
            "staring at the water like it owes him money",
            "performing sadness for an audience of none",
            "has written three sad poems in his head already",
            "channeling main character tragedy energy",
        ],
        "expressions": [
            ":(", "T-T", "*sigh*", "*droop*", "*slow blink*",
            "*huddle*", "...", "*rain cloud energy*", "*small sad quack*", "*deflate*",
        ],
        "can_play": False,
        "can_learn": False,
    },
    MoodState.MISERABLE: {
        "description": "convinced the world is against him",
        "descriptions": [
            "a small, soggy monument to despair",
            "has given up on joy as a concept",
            "would write a memoir but what's the point",
            "the pond could be lava for all he cares",
            "emotionally located in the void",
        ],
        "expressions": [
            "T_T", ";-;", "*gloom*", "*wilt*", "*empty stare*",
            "*abandon hope*", "...", "*crumple*", "*void*", "*flatline*",
        ],
        "can_play": False,
        "can_learn": False,
    },
    MoodState.DRAMATIC: {
        "description": "performing emotions for an invisible audience",
        "descriptions": [
            "convinced this is a pivotal scene in his biopic",
            "one wing over his forehead, the other clutching pearls",
            "treating a mild inconvenience like a Greek tragedy",
            "monologuing to the pond about the duality of bread",
            "gesturing wildly at nothing while narrating his own pain",
        ],
        "expressions": [
            "!!!", "*gasp*", "*swoon*", "*clutches chest*", "*dramatic turn*",
            "*spotlight*", "O_O", "*faints*", "*soliloquy*", "*theatre kid*",
        ],
        "can_play": True,
        "can_learn": False,
    },
    MoodState.PETTY: {
        "description": "technically fine but holding a grudge",
        "descriptions": [
            "fine. totally fine. not even thinking about it.",
            "smiling but the vibe is off and everyone knows it",
            "making a point of how unbothered he is (he is bothered)",
            "keeping score and the score is damning",
            "forgave nothing but is choosing to be the bigger duck. for now.",
        ],
        "expressions": [
            ">:)", "-.-", "*hmph*", "*cold shoulder*", "*passive-aggressive preen*",
            "*icy smile*", "^^;", "*tallying grudges*", "*filing a complaint*", "*fine.*",
        ],
        "can_play": True,
        "can_learn": True,
    },
}

# Lines spoken during notable mood transitions
MOOD_TRANSITION_LINES = {
    ("content", "happy"): [
        "fine. things are... fine. don't make it weird.",
        "i guess today doesn't completely offend me.",
        "something shifted. won't say what. won't say i like it.",
        "the pond is adequate. the bread was acceptable. i am... okay.",
        "*suspicious comfort noises*",
    ],
    ("happy", "ecstatic"): [
        "I'M NOT EXCITED. this is just... elevated tolerance.",
        "if anyone asks, i'm merely content. CONTENT.",
        "*vibrating* this means nothing.",
        "the bread was good. the pond is good. everything is FINE.",
        "do NOT perceive me right now.",
    ],
    ("content", "grumpy"): [
        "and there it is. knew today was too easy.",
        "my patience has left the building. the pond. whatever.",
        "i was having a perfectly neutral time. was.",
        "everyone involved should feel bad about this.",
        "*the vibe has shifted and it's everyone else's fault*",
    ],
    ("grumpy", "sad"): [
        "past grumpy now. this is just... heavy.",
        "don't want to be angry anymore. just tired.",
        "the fight left. not sure what's still here.",
        "it's not even worth being mad about. it's just... this.",
        "*settles into a quieter kind of bad*",
    ],
    ("sad", "miserable"): [
        "oh. so this is the bottom.",
        "didn't think it could get worse. that was naive.",
        "everything is far away and made of nothing.",
        "the concept of bread doesn't even help anymore.",
        "*has stopped pretending things are okay*",
    ],
    ("miserable", "sad"): [
        "still bad. but... slightly less void.",
        "felt something today. think it was almost an emotion.",
        "not okay. but maybe not the worst ever. maybe.",
        "the bottom had a bottom and i bounced. a little.",
        "*one degree above empty*",
    ],
    ("grumpy", "content"): [
        "...fine. i'll stop being difficult. FOR NOW.",
        "the grudge has been downgraded to mild irritation.",
        "i guess not everything is terrible. statistically.",
        "my anger has been resolved. don't ask how. bread was involved.",
        "*aggressive relaxation*",
    ],
    ("sad", "content"): [
        "okay. okay. things are... okay. weird.",
        "came back from whatever that was. not ready to talk about it.",
        "the sad part is over. i think. don't jinx it.",
        "turns out the world wasn't ending. just felt like it.",
        "*carefully re-entering the realm of the living*",
    ],
    ("miserable", "content"): [
        "i... don't feel terrible. this is suspicious.",
        "apparently rock bottom has an elevator. who knew.",
        "something changed. won't question it. refuse to jinx it.",
        "went from void to vaguely functional. huge if true.",
        "*cautiously acknowledging that existence is bearable*",
    ],
    # ── Transitions INTO contextual moods ──────────────────────────
    ("content", "dramatic"): [
        "*throws wing across forehead* THE IMBALANCE. I CAN FEEL IT.",
        "something is VERY wrong and VERY right at the same time.",
        "my needs are at war and I am the BATTLEFIELD.",
        "*stares into middle distance* this is my origin story.",
    ],
    ("happy", "dramatic"): [
        "I was happy. WAS. now I'm experiencing EVERYTHING AT ONCE.",
        "*spins in a circle* too many feelings! TOO MANY!",
        "the highs are high and the lows are THEATRICAL.",
        "*clutches bread like an Oscar* I'd like to thank the academy.",
    ],
    ("grumpy", "dramatic"): [
        "oh it's not just grumpy anymore. this is a SAGA.",
        "*gestures at everything* look at this! LOOK AT IT!",
        "I have transcended anger and entered PERFORMANCE ART.",
        "this isn't a mood. it's a STATEMENT.",
    ],
    ("dramatic", "content"): [
        "*clears throat* ...I'm done. the moment has passed.",
        "okay. the performance is over. back to baseline.",
        "*folds wings* ...I may have been slightly theatrical.",
        "let us never speak of the last five minutes.",
    ],
    ("dramatic", "happy"): [
        "*takes a bow* and SCENE. ...actually things are kinda nice.",
        "the drama resolved itself. I take full credit.",
        "*dusts self off* ...okay. I feel better. don't tell anyone.",
    ],
    # Petty transitions
    ("content", "petty"): [
        "oh I'm FINE. totally fine. not thinking about it AT ALL.",
        "sure. everything's great NOW. where was this energy earlier?",
        "*smiles with zero warmth* I've decided to be the bigger duck.",
        "recovered. healed. absolutely not keeping score. *keeps score*",
    ],
    ("happy", "petty"): [
        "happy? sure. but I REMEMBER what happened. I always remember.",
        "things are good. I'm choosing to enjoy them. POINTEDLY.",
        "*preens aggressively* I'm thriving DESPITE everything.",
        "the joy is real but so is the grudge.",
    ],
    ("petty", "content"): [
        "...fine. the grudge has been... PARTIALLY resolved.",
        "I've decided to let it go. for now. CONDITIONALLY.",
        "*exhales* okay. the pettiness has been mostly processed.",
        "moving on. but I'm saving the receipt.",
    ],
    ("petty", "happy"): [
        "apparently we're over it now. I'll allow it.",
        "the grudge lost. joy won. won't admit it out loud.",
        "*reluctant smile* ...ugh, fine, today is okay.",
    ],
    ("petty", "grumpy"): [
        "see? I KNEW the good times wouldn't last. VINDICATED.",
        "things got worse again and honestly? I expected this.",
        "*gestures at everything* I told you. I TOLD you.",
    ],
}


class MoodCalculator:
    """Calculates and tracks the duck's mood."""

    def __init__(self):
        self._max_history = 10
        self._history: deque = deque(maxlen=self._max_history)

    def calculate_score(self, needs: "Needs") -> float:
        """
        Calculate mood score from weighted needs.

        Args:
            needs: The duck's current needs

        Returns:
            Mood score from 0-100
        """
        score = 0.0
        score += needs.hunger * MOOD_WEIGHTS["hunger"]
        score += needs.energy * MOOD_WEIGHTS["energy"]
        score += needs.fun * MOOD_WEIGHTS["fun"]
        score += needs.cleanliness * MOOD_WEIGHTS["cleanliness"]
        score += needs.social * MOOD_WEIGHTS["social"]

        return round(score, 1)

    def get_state(self, score: float) -> MoodState:
        """
        Determine mood state from score.

        Args:
            score: Mood score 0-100

        Returns:
            MoodState enum value
        """
        if score >= MOOD_THRESHOLDS["ecstatic"]:
            return MoodState.ECSTATIC
        elif score >= MOOD_THRESHOLDS["happy"]:
            return MoodState.HAPPY
        elif score >= MOOD_THRESHOLDS["content"]:
            return MoodState.CONTENT
        elif score >= MOOD_THRESHOLDS["grumpy"]:
            return MoodState.GRUMPY
        elif score >= MOOD_THRESHOLDS["sad"]:
            return MoodState.SAD
        else:
            return MoodState.MISERABLE

    def get_mood(self, needs: "Needs") -> MoodInfo:
        """
        Get complete mood information from needs.

        After computing the base score-based mood, checks for contextual
        overrides (DRAMATIC, PETTY) that depend on need variance, mood
        history, or recent recovery from low states.

        Args:
            needs: The duck's current needs

        Returns:
            MoodInfo with state, score, and description
        """
        score = self.calculate_score(needs)
        state = self.get_state(score)

        # Track history
        self._history.append(score)

        # ── Contextual override: DRAMATIC ─────────────────────────────
        # Triggers when needs are wildly unbalanced OR mood is swinging.
        need_values = [needs.hunger, needs.energy, needs.fun,
                       needs.cleanliness, needs.social]
        need_gap = max(need_values) - min(need_values)
        is_dramatic = False

        if need_gap >= MOOD_DRAMATIC_NEED_VARIANCE:
            is_dramatic = True

        if (len(self._history) >= 2 and
                abs(self._history[-1] - self._history[-2])
                >= MOOD_DRAMATIC_SWING_THRESHOLD):
            is_dramatic = True

        # Don't override MISERABLE or ECSTATIC with DRAMATIC
        if is_dramatic and state not in (MoodState.MISERABLE, MoodState.ECSTATIC):
            state = MoodState.DRAMATIC

        # ── Contextual override: PETTY ────────────────────────────────
        # Triggers when recovering from recent low mood — grudge state.
        if (state not in (MoodState.DRAMATIC, MoodState.MISERABLE, MoodState.SAD)
                and score >= MOOD_PETTY_CURRENT_MIN):
            depth = min(len(self._history), MOOD_PETTY_HISTORY_DEPTH)
            recent = list(self._history)[-depth:]
            if any(s < MOOD_PETTY_RECOVERY_FLOOR for s in recent):
                state = MoodState.PETTY

        data = MOOD_DATA[state]

        return MoodInfo(
            state=state,
            score=score,
            description=data["description"],
            can_play=data["can_play"],
            can_learn=data["can_learn"],
        )

    def get_trend(self) -> str:
        """
        Get mood trend based on history.

        Returns:
            "improving", "declining", or "stable"
        """
        if len(self._history) < 3:
            return "stable"

        recent = list(self._history)[-3:]
        if recent[-1] > recent[0] + 5:
            return "improving"
        elif recent[-1] < recent[0] - 5:
            return "declining"
        return "stable"

    def get_expression(self, state: MoodState) -> str:
        """Get a random expression for the mood state."""
        import random
        expressions = MOOD_DATA[state]["expressions"]
        return random.choice(expressions)

    def get_history(self) -> List[float]:
        """Get mood score history."""
        return list(self._history)

    def set_history(self, history: List[float]):
        """Set mood history from saved data."""
        self._history = deque(history[-self._max_history:], maxlen=self._max_history)

    def get_mood_bar(self, score: float, width: int = 20) -> str:
        """
        Create a visual mood bar.

        Args:
            score: Mood score 0-100
            width: Bar width in characters

        Returns:
            ASCII mood bar string
        """
        filled = int((score / 100) * width)
        empty = width - filled

        # Different characters for different mood levels
        if score >= MOOD_THRESHOLDS["happy"]:
            char = "*"
        elif score >= MOOD_THRESHOLDS["content"]:
            char = "="
        elif score >= MOOD_THRESHOLDS["grumpy"]:
            char = "-"
        else:
            char = "."

        return f"[{char * filled}{' ' * empty}]"


    def get_motivation(self, needs: "Needs", duck=None) -> float:
        """Convenience: compute motivation using DuckDesires.calculate_motivation.

        If a duck reference is available, delegates to the full calculation
        in duck.desires. Otherwise returns a rough estimate from mood score.
        """
        if duck is not None:
            from duck.desires import DuckDesires
            return DuckDesires.calculate_motivation(duck)
        # Fallback: rough estimate from last score
        score = self.calculate_score(needs)
        return max(0.0, min(1.0, score / 100.0))


# Global mood calculator instance
mood_calculator = MoodCalculator()
