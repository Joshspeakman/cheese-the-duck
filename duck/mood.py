"""
Mood system - calculates duck's emotional state from needs.
"""
from typing import Optional
from dataclasses import dataclass
from enum import Enum

from config import MOOD_THRESHOLDS, MOOD_WEIGHTS


class MoodState(Enum):
    """Possible mood states for the duck."""
    ECSTATIC = "ecstatic"
    HAPPY = "happy"
    CONTENT = "content"
    GRUMPY = "grumpy"
    SAD = "sad"
    MISERABLE = "miserable"


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
        "expressions": ["!!", "^o^", "*gloat*"],
        "can_play": True,
        "can_learn": True,
    },
    MoodState.HAPPY: {
        "description": "tolerating existence quite well",
        "expressions": ["^-^", ":)", "*waggle*"],
        "can_play": True,
        "can_learn": True,
    },
    MoodState.CONTENT: {
        "description": "not actively plotting revenge",
        "expressions": ["-.-", "~", "*chill*"],
        "can_play": True,
        "can_learn": True,
    },
    MoodState.GRUMPY: {
        "description": "radiating 'don't test me' energy",
        "expressions": [">:(", "-_-", "*huff*"],
        "can_play": True,
        "can_learn": False,
    },
    MoodState.SAD: {
        "description": "dramatically brooding",
        "expressions": [":(", "T-T", "*sigh*"],
        "can_play": False,
        "can_learn": False,
    },
    MoodState.MISERABLE: {
        "description": "convinced the world is against him",
        "expressions": ["T_T", ";-;", "*gloom*"],
        "can_play": False,
        "can_learn": False,
    },
}


class MoodCalculator:
    """Calculates and tracks the duck's mood."""

    def __init__(self):
        self._history: List[float] = []
        self._max_history = 10

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

        Args:
            needs: The duck's current needs

        Returns:
            MoodInfo with state, score, and description
        """
        score = self.calculate_score(needs)
        state = self.get_state(score)
        data = MOOD_DATA[state]

        # Track history
        self._history.append(score)
        if len(self._history) > self._max_history:
            self._history.pop(0)

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

        recent = self._history[-3:]
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
        return self._history.copy()

    def set_history(self, history: List[float]):
        """Set mood history from saved data."""
        self._history = history[-self._max_history:]

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


# Global mood calculator instance
mood_calculator = MoodCalculator()
