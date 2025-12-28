"""
Duck Dreams System - Dreams that play while the duck sleeps.
Dreams are influenced by recent activities, mood, and random chance.
"""
import random
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime


class DreamType(Enum):
    """Types of dreams the duck can have."""
    ADVENTURE = "adventure"
    FLYING = "flying"
    FOOD = "food"
    FRIEND = "friend"
    NIGHTMARE = "nightmare"
    MEMORY = "memory"
    PROPHETIC = "prophetic"
    SILLY = "silly"
    PEACEFUL = "peaceful"


@dataclass
class Dream:
    """A single dream sequence."""
    dream_type: DreamType
    title: str
    scenes: List[str]
    mood_effect: int  # Effect on mood when waking
    special_reward: Optional[str] = None  # Rare item/bonus from dream
    xp_bonus: int = 0
    is_recurring: bool = False


# Dream sequences organized by type
DREAMS = {
    DreamType.ADVENTURE: [
        Dream(
            dream_type=DreamType.ADVENTURE,
            title="The Great Bread Quest",
            scenes=[
                "Cheese dreams of a far-off land...",
                "A mountain of bread loaves rises in the distance!",
                "Cheese waddles bravely through the Butter Valley...",
                "A friendly toast guardian offers guidance...",
                "The legendary Golden Crumb appears!",
                "Cheese reaches the summit! The bread is... delicious!",
            ],
            mood_effect=10,
            xp_bonus=5,
        ),
        Dream(
            dream_type=DreamType.ADVENTURE,
            title="Pirate Duck",
            scenes=[
                "Ahoy! Captain Cheese sets sail!",
                "The sea sparkles with possibilities...",
                "A treasure map appears in the waves!",
                "X marks the spot... under the old willow tree?",
                "Cheese discovers a chest full of shiny pebbles!",
            ],
            mood_effect=8,
            xp_bonus=3,
            special_reward="treasure_map",
        ),
        Dream(
            dream_type=DreamType.ADVENTURE,
            title="Space Duck",
            scenes=[
                "3... 2... 1... BLAST OFF!",
                "Cheese floats among the stars...",
                "A friendly alien duck waves hello!",
                "The Moon Pond reflects the Earth below...",
                "Space bread tastes like stardust!",
            ],
            mood_effect=12,
            xp_bonus=5,
        ),
    ],
    DreamType.FLYING: [
        Dream(
            dream_type=DreamType.FLYING,
            title="Cloud Surfing",
            scenes=[
                "Cheese's wings grow strong and powerful...",
                "WHOOOOSH! Into the clouds!",
                "The world below looks so small!",
                "Other birds wave as Cheese soars past...",
                "A soft cloud makes the perfect rest stop...",
            ],
            mood_effect=15,
            xp_bonus=3,
        ),
        Dream(
            dream_type=DreamType.FLYING,
            title="Rainbow Rider",
            scenes=[
                "A rainbow appears after the storm...",
                "Cheese slides down the colorful arc!",
                "Red! Orange! Yellow! Green! Blue! Purple!",
                "At the rainbow's end... a pot of golden corn!",
            ],
            mood_effect=20,
            xp_bonus=5,
            special_reward="rainbow_feather",
        ),
    ],
    DreamType.FOOD: [
        Dream(
            dream_type=DreamType.FOOD,
            title="Bread Paradise",
            scenes=[
                "Cheese finds themself in a world made of bread...",
                "Baguette trees! Croissant bushes! Pretzel bridges!",
                "The river flows with melted butter...",
                "Every bite is heavenly! NOM NOM NOM!",
                "*happy food coma*",
            ],
            mood_effect=10,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.FOOD,
            title="The Infinite Feast",
            scenes=[
                "A banquet stretches to the horizon...",
                "Every food Cheese has ever loved is here!",
                "The vegetables... wait, even they look tasty?!",
                "Cheese eats and eats but never gets full!",
                "This is the good life...",
            ],
            mood_effect=8,
            xp_bonus=2,
        ),
    ],
    DreamType.FRIEND: [
        Dream(
            dream_type=DreamType.FRIEND,
            title="Best Friends Forever",
            scenes=[
                "Cheese is surrounded by all their friends...",
                "Gerald the Goose tells funny jokes!",
                "Pip the Duckling learns to fly!",
                "Everyone shares snacks and stories...",
                "Cheese feels so loved and happy...",
            ],
            mood_effect=15,
            xp_bonus=3,
        ),
        Dream(
            dream_type=DreamType.FRIEND,
            title="Memory Lane",
            scenes=[
                "Cheese walks down a path of memories...",
                "There's the first toy they ever loved!",
                "And the first friend who visited!",
                "Every happy moment glows warmly...",
                "The past and present blend together beautifully...",
            ],
            mood_effect=12,
            xp_bonus=2,
        ),
    ],
    DreamType.NIGHTMARE: [
        Dream(
            dream_type=DreamType.NIGHTMARE,
            title="The Empty Pond",
            scenes=[
                "Cheese waddles to the pond...",
                "But... where is everyone?",
                "The water is cold and still...",
                "Wait... is that a friend in the distance?",
                "Cheese runs toward them... closer... closer...",
                "OH! *wakes up* Just a dream! Phew!",
            ],
            mood_effect=-5,
            xp_bonus=1,
        ),
        Dream(
            dream_type=DreamType.NIGHTMARE,
            title="Bread Shortage",
            scenes=[
                "The bread... it's all gone!",
                "Every bakery is closed!",
                "Cheese searches everywhere...",
                "Wait... there's one crumb left!",
                "Cheese nibbles it... and more appears!",
                "The nightmare becomes a happy dream!",
            ],
            mood_effect=2,  # Turns positive at the end
            xp_bonus=2,
        ),
    ],
    DreamType.MEMORY: [
        Dream(
            dream_type=DreamType.MEMORY,
            title="First Day Home",
            scenes=[
                "Cheese remembers hatching from their egg...",
                "The world was so big and new!",
                "A kind presence was there from the start...",
                "That first meal tasted like love...",
                "Home has always been where the heart is...",
            ],
            mood_effect=10,
            xp_bonus=3,
        ),
    ],
    DreamType.PROPHETIC: [
        Dream(
            dream_type=DreamType.PROPHETIC,
            title="Vision of Tomorrow",
            scenes=[
                "The dream feels strangely real...",
                "Cheese sees a glimpse of things to come...",
                "A new friend will arrive soon!",
                "Something special waits to be discovered...",
                "The future looks bright and exciting!",
            ],
            mood_effect=8,
            xp_bonus=5,
            special_reward="lucky_charm",
        ),
    ],
    DreamType.SILLY: [
        Dream(
            dream_type=DreamType.SILLY,
            title="Upside Down World",
            scenes=[
                "Wait... why is everything upside down?!",
                "Cheese walks on the ceiling!",
                "The fish are flying! The birds are swimming!",
                "A backwards quack comes out: KCAUQ!",
                "*giggle* This is so weird!",
            ],
            mood_effect=8,
            xp_bonus=1,
        ),
        Dream(
            dream_type=DreamType.SILLY,
            title="Giant Cheese (the Duck)",
            scenes=[
                "Cheese grows... and grows... AND GROWS!",
                "Now they're as tall as a tree!",
                "All the tiny ducks look up in awe!",
                "Cheese gives the smallest leaf a gentle pat...",
                "Being big is fun but being small is cozy!",
            ],
            mood_effect=6,
            xp_bonus=1,
        ),
        Dream(
            dream_type=DreamType.SILLY,
            title="The Talking Hat",
            scenes=[
                "Cheese's favorite hat starts talking!",
                "'Hello! I'm Hat! Nice to meet you!'",
                "Hat knows so many funny jokes!",
                "'Why did the duck cross the road? To prove they weren't chicken!'",
                "*quacking with laughter*",
            ],
            mood_effect=10,
            xp_bonus=2,
        ),
    ],
    DreamType.PEACEFUL: [
        Dream(
            dream_type=DreamType.PEACEFUL,
            title="Sunset Pond",
            scenes=[
                "The sun sets over a beautiful pond...",
                "Warm colors paint the sky...",
                "Cheese floats peacefully on the calm water...",
                "Everything is quiet and serene...",
                "Pure contentment fills the dream...",
            ],
            mood_effect=12,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.PEACEFUL,
            title="Garden Nap",
            scenes=[
                "Cheese rests in a bed of soft flowers...",
                "Butterflies dance overhead...",
                "A gentle breeze carries sweet scents...",
                "Time seems to slow down...",
                "This is perfect peace...",
            ],
            mood_effect=15,
            xp_bonus=2,
        ),
    ],
}


@dataclass
class DreamResult:
    """Result of a dream sequence."""
    dream: Dream
    scenes_shown: List[str]
    mood_effect: int
    xp_earned: int
    special_reward: Optional[str]
    message: str


class DreamSystem:
    """Manages duck dreams during sleep."""

    def __init__(self):
        self.dream_history: List[str] = []  # Track recent dream titles
        self.total_dreams: int = 0
        self.dream_type_counts: Dict[str, int] = {}
        self.special_rewards_found: List[str] = []

    def generate_dream(
        self,
        mood_score: int = 50,
        recent_activities: List[str] = None,
        visitor_names: List[str] = None,
    ) -> Dream:
        """Generate a dream based on current state."""
        recent_activities = recent_activities or []
        visitor_names = visitor_names or []

        # Determine dream type probabilities
        weights = {
            DreamType.ADVENTURE: 20,
            DreamType.FLYING: 15,
            DreamType.FOOD: 20,
            DreamType.FRIEND: 15,
            DreamType.NIGHTMARE: 5,
            DreamType.MEMORY: 10,
            DreamType.PROPHETIC: 3,
            DreamType.SILLY: 15,
            DreamType.PEACEFUL: 15,
        }

        # Adjust weights based on mood
        if mood_score < 30:
            weights[DreamType.NIGHTMARE] += 10
            weights[DreamType.PEACEFUL] -= 5
        elif mood_score > 70:
            weights[DreamType.PEACEFUL] += 10
            weights[DreamType.NIGHTMARE] -= 3
            weights[DreamType.FLYING] += 5

        # Adjust based on recent activities
        if "feed" in recent_activities or "eat" in recent_activities:
            weights[DreamType.FOOD] += 15
        if "play" in recent_activities:
            weights[DreamType.ADVENTURE] += 10
            weights[DreamType.SILLY] += 10
        if visitor_names:
            weights[DreamType.FRIEND] += 15

        # Avoid repeating recent dreams
        for title in self.dream_history[-3:]:
            for dream_type, dreams in DREAMS.items():
                for dream in dreams:
                    if dream.title == title:
                        weights[dream_type] = max(1, weights[dream_type] - 10)

        # Select dream type
        dream_types = list(weights.keys())
        probabilities = [weights[dt] for dt in dream_types]
        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]

        selected_type = random.choices(dream_types, weights=probabilities, k=1)[0]

        # Select specific dream
        available_dreams = DREAMS.get(selected_type, [])
        if not available_dreams:
            # Fallback to peaceful dream
            available_dreams = DREAMS[DreamType.PEACEFUL]

        dream = random.choice(available_dreams)
        return dream

    def start_dream(
        self,
        mood_score: int = 50,
        recent_activities: List[str] = None,
        visitor_names: List[str] = None,
    ) -> DreamResult:
        """Start a dream sequence and return the result."""
        dream = self.generate_dream(mood_score, recent_activities, visitor_names)

        # Track this dream
        self.dream_history.append(dream.title)
        if len(self.dream_history) > 10:
            self.dream_history = self.dream_history[-10:]

        self.total_dreams += 1
        type_key = dream.dream_type.value
        self.dream_type_counts[type_key] = self.dream_type_counts.get(type_key, 0) + 1

        # Check for special reward (not guaranteed even if dream has one)
        special_reward = None
        if dream.special_reward and random.random() < 0.3:  # 30% chance
            special_reward = dream.special_reward
            self.special_rewards_found.append(special_reward)

        # Generate result
        result = DreamResult(
            dream=dream,
            scenes_shown=dream.scenes,
            mood_effect=dream.mood_effect,
            xp_earned=dream.xp_bonus,
            special_reward=special_reward,
            message=f"{dream.title}: A {dream.dream_type.value} dream",
        )

        return result

    def get_dream_stats(self) -> Dict:
        """Get statistics about dreams."""
        return {
            "total_dreams": self.total_dreams,
            "dream_types": self.dream_type_counts,
            "special_rewards": self.special_rewards_found,
            "recent_dreams": self.dream_history[-5:],
        }

    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "dream_history": self.dream_history,
            "total_dreams": self.total_dreams,
            "dream_type_counts": self.dream_type_counts,
            "special_rewards_found": self.special_rewards_found,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DreamSystem":
        """Create from dictionary."""
        system = cls()
        system.dream_history = data.get("dream_history", [])
        system.total_dreams = data.get("total_dreams", 0)
        system.dream_type_counts = data.get("dream_type_counts", {})
        system.special_rewards_found = data.get("special_rewards_found", [])
        return system


# Global instance
dreams = DreamSystem()
