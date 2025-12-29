"""
Visitor Dialogue System - Comprehensive dialogue trees for duck friends.
Each personality has dialogue for each friendship level that progresses naturally.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random


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
        
    def start_visit(self, personality: str, friendship_level: str, 
                    friend_name: str, visit_number: int, unlocked_topics: set = None):
        """Initialize for a new visit."""
        self.state = ConversationState()
        self.state.phase = ConversationPhase.GREETING
        self.personality = personality.lower()
        self.friendship_level = friendship_level.lower().replace(" ", "_")
        self.friend_name = friend_name
        self.visit_number = visit_number
        self.unlocked_topics = unlocked_topics or set()
        
    def get_next_dialogue(self, duck_name: str = "friend") -> Optional[str]:
        """Get the next line of dialogue based on current state."""
        dialogue_tree = DIALOGUE_TREES.get(self.personality, {})
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
    
    def get_farewell(self, duck_name: str) -> str:
        """Get a farewell message."""
        self.state.phase = ConversationPhase.FAREWELL
        return self.get_next_dialogue(duck_name) or f"{self.friend_name}: Bye, {duck_name}!"


# ============================================================================
# DIALOGUE TREES BY PERSONALITY
# Each personality has dialogue organized by phase and friendship level
# ============================================================================

DIALOGUE_TREES: Dict[str, Dict[str, List[DialogueLine]]] = {}

# Import personality-specific dialogue - each file registers its dialogue in DIALOGUE_TREES
# Note: Imports must come after DIALOGUE_TREES is defined since they reference it
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
