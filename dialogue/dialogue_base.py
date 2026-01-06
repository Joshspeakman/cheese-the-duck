"""
Base dialogue types - shared classes to avoid circular imports.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum


class ConversationPhase(Enum):
    """Phases of a visit conversation."""
    GREETING = "greeting"
    OPENING = "opening"  # Initial small talk
    MAIN = "main"  # Main conversation topics
    STORY = "story"  # Longer stories/anecdotes
    PERSONAL = "personal"  # Personal revelations (higher friendship)
    ACTIVITY = "activity"  # Suggesting activities together
    CLOSING = "closing"  # Wrapping up
    FAREWELL = "farewell"


@dataclass
class DialogueLine:
    """A single line of dialogue."""
    text: str
    phase: ConversationPhase
    friendship_min: str = "stranger"  # Minimum friendship level required
    once_per_visit: bool = False  # Can only be said once per visit
    unlocks_topic: Optional[str] = None  # Unlocks a new topic for future visits
    requires_topic: Optional[str] = None  # Requires a topic to be unlocked


# Global registry for dialogue trees by personality
# Dialogue modules populate this when imported
DIALOGUE_TREES: Dict[str, Dict[str, List[DialogueLine]]] = {}
