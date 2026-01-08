"""
Memory system - duck remembers interactions and events.
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque
import random


# Memory limits
MAX_SHORT_TERM = 10
MAX_LONG_TERM = 50
MAX_MOOD_HISTORY = 20
MAX_AFFINITY_ITEMS = 100


@dataclass
class Memory:
    """A single memory entry."""
    type: str              # interaction, event, milestone
    content: str           # What happened
    timestamp: str         # When it happened
    emotional_value: int   # -100 to +100 (negative = bad memory)
    importance: int        # 1-10 scale


class DuckMemory:
    """
    Manages the duck's memories of interactions and events.
    Uses deques for O(1) memory limit enforcement.
    """

    def __init__(self):
        self.short_term: deque = deque(maxlen=MAX_SHORT_TERM)  # Last 10 interactions
        self.long_term: List[Memory] = []   # Important memories (max 50, sorted by importance)
        self.player_name: Optional[str] = None
        self.favorite_things: Dict[str, int] = {}  # thing -> affinity score
        self.disliked_things: Dict[str, int] = {}
        self.interaction_counts: Dict[str, int] = {}
        self.total_interactions: int = 0
        self.first_meeting: Optional[str] = None
        self.mood_history: deque = deque(maxlen=MAX_MOOD_HISTORY)

    def add_interaction(self, interaction_type: str, details: str = "", emotional_value: int = 0):
        """Record an interaction."""
        memory = Memory(
            type="interaction",
            content=f"{interaction_type}: {details}" if details else interaction_type,
            timestamp=datetime.now().isoformat(),
            emotional_value=emotional_value,
            importance=3 if emotional_value != 0 else 1,
        )

        # Add to short term (deque auto-removes oldest when full)
        self.short_term.append(memory)

        # Track counts (with limit to prevent unbounded growth)
        self.interaction_counts[interaction_type] = self.interaction_counts.get(interaction_type, 0) + 1
        self._limit_interaction_counts()
        self.total_interactions += 1

        # Very positive or negative interactions go to long term
        if abs(emotional_value) >= 50:
            self._add_long_term(memory)
    
    def _limit_interaction_counts(self):
        """Limit interaction counts dict size to prevent unbounded growth."""
        if len(self.interaction_counts) > MAX_AFFINITY_ITEMS:
            # Keep only the most frequent interactions
            sorted_counts = sorted(self.interaction_counts.items(), key=lambda x: x[1], reverse=True)
            self.interaction_counts = dict(sorted_counts[:MAX_AFFINITY_ITEMS])

    def add_event(self, event_name: str, details: str, importance: int = 5, emotional_value: int = 0):
        """Record a significant event."""
        memory = Memory(
            type="event",
            content=f"{event_name}: {details}",
            timestamp=datetime.now().isoformat(),
            emotional_value=emotional_value,
            importance=importance,
        )

        # Add to short term (deque auto-removes oldest when full)
        self.short_term.append(memory)

        if importance >= 5:
            self._add_long_term(memory)

    def add_milestone(self, milestone: str, details: str = ""):
        """Record a milestone (growth stage, achievement, etc.)."""
        memory = Memory(
            type="milestone",
            content=f"{milestone}: {details}" if details else milestone,
            timestamp=datetime.now().isoformat(),
            emotional_value=50,
            importance=8,
        )
        self._add_long_term(memory)

    def _add_long_term(self, memory: Memory):
        """Add a memory to long-term storage."""
        self.long_term.append(memory)
        # Keep only most important if over limit
        if len(self.long_term) > MAX_LONG_TERM:
            self.long_term.sort(key=lambda m: m.importance, reverse=True)
            self.long_term = self.long_term[:MAX_LONG_TERM]

    def update_affinity(self, thing: str, delta: int):
        """Update affinity for something (food, toy, activity)."""
        current = self.favorite_things.get(thing, 0)
        new_value = current + delta

        if new_value > 20:
            self.favorite_things[thing] = new_value
            self.disliked_things.pop(thing, None)
        elif new_value < -20:
            self.disliked_things[thing] = new_value
            self.favorite_things.pop(thing, None)
        else:
            self.favorite_things[thing] = new_value

    def get_favorite(self, category: str = None) -> Optional[str]:
        """Get the duck's favorite thing (optionally in a category)."""
        if not self.favorite_things:
            return None
        return max(self.favorite_things.keys(), key=lambda k: self.favorite_things[k])

    def get_recent_mood_trend(self) -> str:
        """Get recent mood trend description."""
        if len(self.mood_history) < 3:
            return "uncertain"

        recent = self.mood_history[-5:]
        avg_recent = sum(recent) / len(recent)

        if len(self.mood_history) >= 10:
            older = self.mood_history[-10:-5]
            avg_older = sum(older) / len(older)

            if avg_recent > avg_older + 10:
                return "improving"
            elif avg_recent < avg_older - 10:
                return "declining"

        if avg_recent >= 70:
            return "consistently happy"
        elif avg_recent <= 30:
            return "consistently sad"
        return "stable"

    def record_mood(self, mood_score: float):
        """Record a mood score for history (deque auto-evicts oldest when full)."""
        self.mood_history.append(int(mood_score))

    def get_relationship_level(self) -> str:
        """Get the relationship level with the player."""
        if self.total_interactions < 10:
            return "stranger"
        elif self.total_interactions < 50:
            return "acquaintance"
        elif self.total_interactions < 150:
            return "friend"
        elif self.total_interactions < 500:
            return "best_friend"
        else:
            return "bonded"

    def get_relationship_description(self) -> str:
        """Get a description of the relationship."""
        level = self.get_relationship_level()
        descriptions = {
            "stranger": "still getting to know you",
            "acquaintance": "starting to recognize you",
            "friend": "considers you a friend",
            "best_friend": "loves spending time with you",
            "bonded": "deeply bonded with you",
        }
        return descriptions.get(level, "exists")

    def recall_random_memory(self) -> Optional[str]:
        """Recall a random memory (for dialogue)."""
        all_memories = list(self.short_term) + self.long_term
        if not all_memories:
            return None

        # Weight toward more important/emotional memories
        weights = [m.importance + abs(m.emotional_value) / 20 for m in all_memories]
        memory = random.choices(all_memories, weights=weights)[0]
        return memory.content

    def recall_memory(self) -> Optional[str]:
        """Alias for recall_random_memory for API compatibility."""
        return self.recall_random_memory()

    def get_mood_trend(self) -> str:
        """Get the overall mood trend description."""
        return self.get_recent_mood_trend()

    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "short_term": [
                {
                    "type": m.type,
                    "content": m.content,
                    "timestamp": m.timestamp,
                    "emotional_value": m.emotional_value,
                    "importance": m.importance,
                }
                for m in self.short_term
            ],
            "long_term": [
                {
                    "type": m.type,
                    "content": m.content,
                    "timestamp": m.timestamp,
                    "emotional_value": m.emotional_value,
                    "importance": m.importance,
                }
                for m in self.long_term
            ],
            "player_name": self.player_name,
            "favorite_things": self.favorite_things,
            "disliked_things": self.disliked_things,
            "interaction_counts": self.interaction_counts,
            "total_interactions": self.total_interactions,
            "first_meeting": self.first_meeting,
            "mood_history": list(self.mood_history),  # Convert deque to list for JSON
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DuckMemory":
        """Create from dictionary."""
        memory = cls()

        for m_data in data.get("short_term", []):
            memory.short_term.append(Memory(
                type=m_data["type"],
                content=m_data["content"],
                timestamp=m_data["timestamp"],
                emotional_value=m_data["emotional_value"],
                importance=m_data["importance"],
            ))

        for m_data in data.get("long_term", []):
            memory.long_term.append(Memory(
                type=m_data["type"],
                content=m_data["content"],
                timestamp=m_data["timestamp"],
                emotional_value=m_data["emotional_value"],
                importance=m_data["importance"],
            ))

        memory.player_name = data.get("player_name")
        memory.favorite_things = data.get("favorite_things", {})
        memory.disliked_things = data.get("disliked_things", {})
        memory.interaction_counts = data.get("interaction_counts", {})
        memory.total_interactions = data.get("total_interactions", 0)
        memory.first_meeting = data.get("first_meeting")
        memory.mood_history = data.get("mood_history", [])

        return memory
