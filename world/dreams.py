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
                "Cheese is in a desert. It's made of bread. Sure.",
                "A mountain of sourdough loaves blocks the path.",
                "Cheese climbs it anyway. Takes about three hours.",
                "At the summit: more bread. Cheese is not surprised.",
                "Eats some. It's fine. Tastes like bread.",
                "Quest complete. Nothing has fundamentally changed.",
            ],
            mood_effect=10,
            xp_bonus=5,
        ),
        Dream(
            dream_type=DreamType.ADVENTURE,
            title="Pirate Duck",
            scenes=[
                "Cheese is on a boat. Cheese did not ask for this.",
                "The ocean is suspiciously calm. Too calm.",
                "A treasure map appears. The X is where Cheese is standing.",
                "Cheese digs. Finds a smaller boat. Okay.",
                "The smaller boat also has a treasure map.",
                "This is going to take a while.",
            ],
            mood_effect=8,
            xp_bonus=3,
            special_reward="treasure_map",
        ),
        Dream(
            dream_type=DreamType.ADVENTURE,
            title="Space Duck",
            scenes=[
                "Cheese is in space now. Nobody explained how.",
                "There are stars. They're just... there.",
                "An alien duck waves. Cheese waves back. Professional courtesy.",
                "The moon is closer than expected. Smells like cheese.",
                "Not the duck. The other cheese. Dairy cheese.",
                "Cheese wakes up confused about identity.",
            ],
            mood_effect=12,
            xp_bonus=5,
        ),
        Dream(
            dream_type=DreamType.ADVENTURE,
            title="The Cave",
            scenes=[
                "There's a cave. Cheese enters. Standard procedure.",
                "It's dark. Cheese can still see somehow. Dream logic.",
                "A dragon appears. It's the size of a potato.",
                "The dragon asks for directions. Cheese doesn't know any.",
                "They sit in awkward silence for a while.",
                "Cheese leaves. The dragon stays. Life goes on.",
            ],
            mood_effect=7,
            xp_bonus=3,
        ),
    ],
    DreamType.FLYING: [
        Dream(
            dream_type=DreamType.FLYING,
            title="Cloud Surfing",
            scenes=[
                "Cheese's wings work now. They usually don't. Suspicious.",
                "Flying is exactly as advertised. You go up.",
                "A cloud passes by. Cheese sits on it. It holds.",
                "Other birds fly past. They seem busy.",
                "Cheese is not busy. Cheese is sitting on a cloud.",
                "This is fine.",
            ],
            mood_effect=15,
            xp_bonus=3,
        ),
        Dream(
            dream_type=DreamType.FLYING,
            title="Rainbow Rider",
            scenes=[
                "A rainbow appears. Cheese gets on it. As one does.",
                "It's a slide now. Cheese didn't consent to this.",
                "The colors blur together. Everything is briefly purple.",
                "At the bottom: a pot of corn. Not gold. Corn.",
                "Cheese eats some. It's fine.",
            ],
            mood_effect=20,
            xp_bonus=5,
            special_reward="rainbow_feather",
        ),
        Dream(
            dream_type=DreamType.FLYING,
            title="Just Falling",
            scenes=[
                "Cheese is falling. Not flying. Just falling.",
                "The ground approaches. Then recedes. Then approaches again.",
                "This has been happening for some time now.",
                "A passing bird asks if Cheese needs help.",
                "Cheese says no. Pride is important.",
                "Still falling. Might be falling forever. It's fine.",
            ],
            mood_effect=5,
            xp_bonus=2,
        ),
    ],
    DreamType.FOOD: [
        Dream(
            dream_type=DreamType.FOOD,
            title="Bread Paradise",
            scenes=[
                "Everything is bread. The ground. The sky. Cheese.",
                "Wait, Cheese is not bread. False alarm.",
                "The trees are baguettes. They're just standing there.",
                "Cheese eats a doorknob. It's a croissant. Of course it is.",
                "Wakes up hungry. Dreams don't count as eating.",
            ],
            mood_effect=10,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.FOOD,
            title="The Infinite Feast",
            scenes=[
                "A table stretches to infinity. Standard dream stuff.",
                "Every food exists here. Even the weird ones.",
                "Cheese eats. Then eats more. Then continues eating.",
                "Still not full. Concerning but not unpleasant.",
                "A waiter appears. Asks if everything is okay.",
                "Cheese nods. The waiter vanishes. Cheese keeps eating.",
            ],
            mood_effect=8,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.FOOD,
            title="The Last Crumb",
            scenes=[
                "There is one crumb. Just one. In the whole world.",
                "Cheese approaches. The crumb doesn't move. It's a crumb.",
                "Dramatic music plays from nowhere.",
                "Cheese eats it. It's a crumb. It tastes like crumb.",
                "More crumbs appear. Crisis averted.",
                "Cheese wakes up feeling accomplished.",
            ],
            mood_effect=6,
            xp_bonus=1,
        ),
    ],
    DreamType.FRIEND: [
        Dream(
            dream_type=DreamType.FRIEND,
            title="Best Friends Forever",
            scenes=[
                "All of Cheese's friends are here. Even the imaginary ones.",
                "Everyone is talking at once. Cheese hears none of it.",
                "Gerald tells a joke. Nobody laughs. It wasn't funny.",
                "They all agree it wasn't funny. Friendship prevails.",
                "Everyone shares snacks. Cheese takes too many.",
                "No one mentions it. True friendship.",
            ],
            mood_effect=15,
            xp_bonus=3,
        ),
        Dream(
            dream_type=DreamType.FRIEND,
            title="Memory Lane",
            scenes=[
                "There's a road. It's made of memories. Somehow.",
                "Cheese steps on a birthday. It squishes.",
                "There's the first friend. They wave. Cheese waves.",
                "This continues for several memories.",
                "At the end: another road. Memory Boulevard, probably.",
                "Cheese turns back. That's enough nostalgia.",
            ],
            mood_effect=12,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.FRIEND,
            title="The Reunion",
            scenes=[
                "Everyone Cheese has ever met is in one room.",
                "It's very crowded. Fire hazard, probably.",
                "Nobody knows why they're here. Standard reunion.",
                "Someone brought a casserole. Nobody eats it.",
                "Cheese stands near the snack table. Strategy.",
                "The dream ends. The casserole remains uneaten.",
            ],
            mood_effect=10,
            xp_bonus=2,
        ),
    ],
    DreamType.NIGHTMARE: [
        Dream(
            dream_type=DreamType.NIGHTMARE,
            title="The Empty Pond",
            scenes=[
                "The pond is empty. Not of water. Of everyone.",
                "Cheese walks around. Footsteps echo. Dramatic.",
                "A shape appears in the distance. Hope rises.",
                "It's a rock. Hope sits back down.",
                "Cheese wakes up. The pond is fine. Everyone is there.",
                "Cheese checks anyway. Just in case.",
            ],
            mood_effect=-5,
            xp_bonus=1,
        ),
        Dream(
            dream_type=DreamType.NIGHTMARE,
            title="Bread Shortage",
            scenes=[
                "No bread. Anywhere. This is serious.",
                "Cheese checks everywhere. Under rocks. In clouds.",
                "The bakery is closed. The baker is also missing.",
                "One crumb appears. Cheese guards it with their life.",
                "More bread appears. The shortage is over.",
                "Cheese is relieved. Also hungry.",
            ],
            mood_effect=2,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.NIGHTMARE,
            title="The Endless Meeting",
            scenes=[
                "Cheese is in a meeting. It has no agenda.",
                "Someone is talking about synergy. Cheese tunes out.",
                "The clock doesn't move. It never moves.",
                "There's no door. There was one earlier. Gone now.",
                "Coffee appears. It's decaf. The horror.",
                "Cheese wakes up grateful for consciousness.",
            ],
            mood_effect=-3,
            xp_bonus=1,
        ),
    ],
    DreamType.MEMORY: [
        Dream(
            dream_type=DreamType.MEMORY,
            title="First Day Home",
            scenes=[
                "Cheese remembers hatching. It was Tuesday.",
                "The world was big. It still is. That hasn't changed.",
                "Someone offered food. Cheese accepted. Good start.",
                "Everything was new. Now some things are old.",
                "Home was here then. Home is here now. Consistent.",
                "Cheese appreciates the lack of surprises.",
            ],
            mood_effect=10,
            xp_bonus=3,
        ),
        Dream(
            dream_type=DreamType.MEMORY,
            title="Yesterday",
            scenes=[
                "Cheese remembers yesterday. It was yesterday.",
                "Things happened. Cheese was there for most of them.",
                "There was food. It was eaten. Standard procedure.",
                "Someone said hello. Cheese said it back.",
                "Then it was night. Now it's this dream.",
                "Tomorrow will probably also happen.",
            ],
            mood_effect=5,
            xp_bonus=1,
        ),
    ],
    DreamType.PROPHETIC: [
        Dream(
            dream_type=DreamType.PROPHETIC,
            title="Vision of Tomorrow",
            scenes=[
                "The dream feels different. More... prophetic.",
                "Cheese sees the future. It looks a lot like the present.",
                "A friend will arrive. Or maybe a package. Hard to tell.",
                "Something will be discovered. Could be anything.",
                "The future is bright. There's adequate lighting.",
                "Cheese will remember none of this. Classic prophecy.",
            ],
            mood_effect=8,
            xp_bonus=5,
            special_reward="lucky_charm",
        ),
        Dream(
            dream_type=DreamType.PROPHETIC,
            title="The Warning",
            scenes=[
                "A mysterious voice speaks. It says 'beware.'",
                "Beware of what? The voice doesn't specify.",
                "Cheese waits for more information. None comes.",
                "The voice clears its throat. Still no details.",
                "'Just... beware in general,' it finally says.",
                "Cheese will try. No promises.",
            ],
            mood_effect=6,
            xp_bonus=3,
        ),
    ],
    DreamType.SILLY: [
        Dream(
            dream_type=DreamType.SILLY,
            title="Upside Down World",
            scenes=[
                "Gravity reversed. Cheese is on the ceiling now.",
                "The furniture doesn't care. It's on the ceiling too.",
                "Walking is the same but in the other direction.",
                "A fish swims by. Through the air. It doesn't explain.",
                "Cheese quacks. It comes out backwards. 'Kcauq.'",
                "Normal enough. Cheese goes back to sleep.",
            ],
            mood_effect=8,
            xp_bonus=1,
        ),
        Dream(
            dream_type=DreamType.SILLY,
            title="Giant Cheese (the Duck)",
            scenes=[
                "Cheese is growing. This wasn't planned.",
                "Now Cheese is taller than a tree. Inconvenient.",
                "The tiny ducks below look up. They seem concerned.",
                "Cheese tries to reassure them. Voice is too loud.",
                "Everyone just nods and walks away slowly.",
                "Cheese shrinks back. Nobody mentions it again.",
            ],
            mood_effect=6,
            xp_bonus=1,
        ),
        Dream(
            dream_type=DreamType.SILLY,
            title="The Talking Hat",
            scenes=[
                "The hat is talking. It hasn't before. Odd.",
                "'I've been watching,' it says. Cheese is uncomfortable.",
                "The hat tells a joke. It's about ducks. It's mediocre.",
                "Cheese laughs politely. The hat seems satisfied.",
                "'Same time tomorrow?' the hat asks.",
                "Cheese pretends not to hear. Wakes up.",
            ],
            mood_effect=10,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.SILLY,
            title="Tax Season",
            scenes=[
                "Cheese is filing taxes. In the dream.",
                "This is unprecedented. Ducks don't pay taxes.",
                "The forms are blank. All of them. Every box.",
                "Cheese signs them anyway. Compliance.",
                "A stamp appears. It says 'APPROVED.'",
                "Cheese wakes up feeling oddly responsible.",
            ],
            mood_effect=4,
            xp_bonus=1,
        ),
    ],
    DreamType.PEACEFUL: [
        Dream(
            dream_type=DreamType.PEACEFUL,
            title="Sunset Pond",
            scenes=[
                "The sun is setting. It does that.",
                "The pond is calm. Nothing is happening.",
                "Cheese floats. The water is the correct temperature.",
                "A bird flies overhead. It doesn't stop.",
                "Time passes. Not too fast. Not too slow.",
                "This is fine. This is exactly fine.",
            ],
            mood_effect=12,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.PEACEFUL,
            title="Garden Nap",
            scenes=[
                "There are flowers. Cheese is among them.",
                "A butterfly exists nearby. It minds its business.",
                "The breeze is gentle. Not too breezy. Just right.",
                "Nothing urgent is happening. Nothing at all.",
                "Cheese lies there. Could be minutes. Could be hours.",
                "Perfect. Absolutely adequate in every way.",
            ],
            mood_effect=15,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.PEACEFUL,
            title="Waiting Room",
            scenes=[
                "Cheese is in a waiting room. There's nothing to wait for.",
                "The chairs are comfortable. The magazines are current.",
                "No one else is here. No one is coming.",
                "The clock ticks. It's not annoying. It's fine.",
                "Cheese waits. For nothing. Contentedly.",
                "This is the whole dream. Cheese wakes up rested.",
            ],
            mood_effect=10,
            xp_bonus=1,
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
