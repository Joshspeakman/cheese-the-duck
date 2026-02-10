"""
Personality system - defines duck's unique character traits.
"""
from typing import Dict, List, Tuple
from dataclasses import dataclass
import random


@dataclass
class PersonalityTrait:
    """A single personality trait with its effects."""
    name: str
    low_name: str      # Name when trait is negative (e.g., "Derpy")
    high_name: str     # Name when trait is positive (e.g., "Clever")
    value: int         # -100 to +100

    @property
    def display_name(self) -> str:
        """Get the display name based on current value."""
        if self.value < -30:
            return self.low_name
        elif self.value > 30:
            return self.high_name
        return f"Somewhat {self.low_name.lower()}/{self.high_name.lower()}"

    @property
    def intensity(self) -> str:
        """Get intensity descriptor."""
        abs_val = abs(self.value)
        if abs_val >= 80:
            return "Extremely"
        elif abs_val >= 60:
            return "Very"
        elif abs_val >= 40:
            return "Quite"
        elif abs_val >= 20:
            return "Somewhat"
        return "Slightly"


TRAIT_DEFINITIONS = {
    "clever_derpy": {
        "low_name": "Derpy",
        "high_name": "Clever",
        "description": "Affects problem-solving and dialogue coherence",
        "effects": {
            "dialogue_randomness": -0.5,  # Derpy = more random dialogue
            "learning_speed": 0.3,        # Clever = learns faster
            "trip_chance": -0.4,          # Derpy = trips more
        }
    },
    "brave_timid": {
        "low_name": "Timid",
        "high_name": "Brave",
        "description": "Affects reactions to events and new things",
        "effects": {
            "event_fear_response": -0.5,  # Timid = scared of events
            "exploration_bonus": 0.3,      # Brave = explores more
            "hide_chance": -0.4,           # Timid = hides more
        }
    },
    "active_lazy": {
        "low_name": "Lazy",
        "high_name": "Active",
        "description": "Affects energy usage and activity level",
        "effects": {
            "energy_decay": 0.3,          # Active = uses more energy
            "action_frequency": 0.4,       # Active = does more things
            "nap_preference": -0.5,        # Lazy = naps more
        }
    },
    "social_shy": {
        "low_name": "Shy",
        "high_name": "Social",
        "description": "Affects interaction needs and talkativeness",
        "effects": {
            "social_decay": 0.4,          # Social = needs more interaction
            "quack_frequency": 0.5,        # Social = quacks more
            "approach_player": 0.3,        # Social = approaches player
        }
    },
    "neat_messy": {
        "low_name": "Messy",
        "high_name": "Neat",
        "description": "Affects cleanliness decay and preening",
        "effects": {
            "cleanliness_decay": -0.3,    # Messy = gets dirty faster
            "preen_frequency": 0.4,        # Neat = preens more
            "splash_messiness": -0.3,      # Messy = messier splashing
        }
    },
}


class Personality:
    """
    Manages the duck's personality traits.
    """

    def __init__(self, traits: Dict[str, int] = None):
        """Initialize personality with trait values."""
        self.traits: Dict[str, PersonalityTrait] = {}

        for trait_id, definition in TRAIT_DEFINITIONS.items():
            value = (traits or {}).get(trait_id, 0)
            self.traits[trait_id] = PersonalityTrait(
                name=trait_id,
                low_name=definition["low_name"],
                high_name=definition["high_name"],
                value=value,
            )

    @classmethod
    def generate_random(cls) -> "Personality":
        """Generate a random personality with bias toward being derpy."""
        traits = {}
        for trait_id in TRAIT_DEFINITIONS:
            if trait_id == "clever_derpy":
                # Bias toward derpy (-30 to +10)
                traits[trait_id] = random.randint(-70, 20)
            else:
                # Normal distribution around 0
                traits[trait_id] = random.randint(-50, 50)
        return cls(traits)

    def get_trait(self, trait_id: str) -> int:
        """Get a trait value."""
        if trait_id in self.traits:
            return self.traits[trait_id].value
        return 0

    def set_trait(self, trait_id: str, value: int):
        """Set a trait value (clamped to -100 to +100)."""
        if trait_id in self.traits:
            self.traits[trait_id].value = max(-100, min(100, value))

    def adjust_trait(self, trait_id: str, delta: int):
        """Adjust a trait by a delta amount."""
        if trait_id in self.traits:
            current = self.traits[trait_id].value
            self.set_trait(trait_id, current + delta)

    def get_effect(self, effect_name: str) -> float:
        """
        Get the combined effect value from all traits.

        Returns a value typically between -1.0 and +1.0
        """
        total = 0.0
        for trait_id, definition in TRAIT_DEFINITIONS.items():
            effects = definition.get("effects", {})
            if effect_name in effects:
                trait_value = self.get_trait(trait_id)
                effect_weight = effects[effect_name]
                # Normalize trait to -1 to +1 and multiply by weight
                total += (trait_value / 100) * effect_weight
        return total

    def get_dominant_traits(self, count: int = 2) -> List[Tuple[str, PersonalityTrait]]:
        """Get the most pronounced personality traits."""
        sorted_traits = sorted(
            self.traits.items(),
            key=lambda x: abs(x[1].value),
            reverse=True
        )
        return sorted_traits[:count]

    def get_personality_summary(self) -> str:
        """Get a human-readable personality summary."""
        dominant = self.get_dominant_traits(2)

        if not dominant:
            return "a fairly average duck"

        descriptions = []
        for trait_id, trait in dominant:
            if abs(trait.value) >= 20:
                descriptions.append(f"{trait.intensity.lower()} {trait.display_name.lower()}")

        if not descriptions:
            return "a fairly balanced duck"
        elif len(descriptions) == 1:
            return f"a {descriptions[0]} duck"
        else:
            return f"a {descriptions[0]} and {descriptions[1]} duck"

    def to_dict(self) -> Dict[str, int]:
        """Convert to dictionary for saving."""
        return {trait_id: trait.value for trait_id, trait in self.traits.items()}

    @classmethod
    def from_dict(cls, data: Dict[str, int]) -> "Personality":
        """Create from dictionary."""
        return cls(data)

    def get_quirk(self) -> str:
        """Get a random personality-based quirk description."""
        quirks = []

        if self.get_trait("clever_derpy") < -30:
            quirks.extend([
                "stares at things that aren't there",
                "forgets what it was doing mid-action",
                "gets confused by simple things",
                "has moments of profound blankness",
                "walked into a wall. again. same wall.",
                "tried to eat his own reflection. it did not go well.",
                "forgot the pond was wet. seemed genuinely surprised.",
                "stared at a leaf for nine minutes. learned nothing.",
                "got lost in a straight line",
                "had a thought. it left.",
            ])
        elif self.get_trait("clever_derpy") > 30:
            quirks.extend([
                "seems to understand more than expected",
                "has surprisingly clever moments",
                "figures things out quickly",
                "solved a problem you didn't know existed",
                "gave you a look that said 'i know what you did'",
                "is quietly judging your life choices. correctly.",
                "learned something on the first try. smug about it.",
                "made a decision that was... actually smart",
                "knows things. won't say how.",
                "outsmarted the bread. don't ask.",
            ])

        if self.get_trait("brave_timid") < -30:
            quirks.extend([
                "gets startled easily",
                "hides from loud noises",
                "is cautious about new things",
                "flinched at his own shadow. then apologized to it.",
                "treats every new object like it might explode",
                "hid behind a single blade of grass. felt safe.",
                "heard a sound. froze. the sound was himself.",
                "refused to cross the pond. it looked different today.",
                "is watching the sky like it's up to something",
                "whispered a quack. in case.",
            ])
        elif self.get_trait("brave_timid") > 30:
            quirks.extend([
                "isn't afraid of anything",
                "approaches everything boldly",
                "is fearless (maybe too fearless)",
                "challenged a rock. the rock didn't respond. he claimed victory.",
                "walked toward the danger. on purpose.",
                "stared down a leaf in the wind. didn't blink.",
                "has no survival instincts. only vibes.",
                "confronted the unknown. the unknown left.",
                "picked a fight with the concept of fear. won.",
                "fears nothing. this is not a compliment.",
            ])

        if self.get_trait("active_lazy") < -30:
            quirks.extend([
                "hasn't moved in a while. might be decorative.",
                "considered doing something. decided against it.",
                "watched an opportunity pass. from a sitting position.",
                "napped through something important. no regrets.",
                "is conserving energy. for what, nobody knows.",
                "achieved a new personal record for stillness",
                "blinked once. that's his cardio for today.",
                "found the optimal resting position. refuses to leave it.",
                "yawned so hard he almost fell over",
                "the pond came to him. he waited.",
            ])
        elif self.get_trait("active_lazy") > 30:
            quirks.extend([
                "has already done three laps of the pond. it's been two minutes.",
                "can't sit still. literally. he's tried.",
                "vibrating with unspent energy",
                "ran somewhere. came back. forgot why.",
                "preened, splashed, circled, and preened again. needs more.",
                "treats standing still as a personal challenge",
                "found a stick. carried it everywhere. put it back. found another.",
                "did a lap of the pond just to feel something",
                "paced back and forth. with purpose. undefined purpose.",
                "exhausting to watch. he doesn't care.",
            ])

        if self.get_trait("social_shy") < -30:
            quirks.extend([
                "turned away when you looked at him",
                "pretended not to hear you. you were right there.",
                "found the most distant corner and committed to it",
                "made eye contact by accident. panicked.",
                "is over there. on purpose. alone. it's fine.",
                "would rather the pond swallow him than make conversation",
                "hid behind himself somehow",
                "quacked under his breath. hoped nobody heard.",
                "is present but emotionally unlisted",
                "ghosted you while standing three feet away",
            ])
        elif self.get_trait("social_shy") > 30:
            quirks.extend([
                "always wants attention",
                "quacks to get your attention",
                "follows you around",
                "made eye contact and will NOT break it",
                "quacked at you. then again. and again. he has news.",
                "is standing unreasonably close. on purpose.",
                "needs you to witness every single thing he does",
                "narrated his own day. to you. in quacks.",
                "won't stop looking at you until you acknowledge him",
                "brought you a leaf. you didn't ask. he doesn't care.",
            ])

        if self.get_trait("neat_messy") < -30:
            quirks.extend([
                "feathers going in nine directions. he doesn't notice.",
                "rolled in something. won't say what.",
                "the concept of grooming is optional and he's opted out",
                "achieved a new level of disheveled",
                "looks like he lost a fight with the pond. and the pond won.",
                "his reflection doesn't even recognize him",
                "splashed everywhere. cleaned nothing.",
                "has mud in places mud shouldn't be",
                "preening is for ducks who care. he does not.",
                "is a mess. a confident, unbothered mess.",
            ])
        elif self.get_trait("neat_messy") > 30:
            quirks.extend([
                "preened for the third time today. still not satisfied.",
                "found a speck of dirt. this is now his whole personality.",
                "reorganized the pond. mentally.",
                "his feathers are immaculate. it took forty minutes.",
                "spotted a smudge. the day is ruined.",
                "aligned every feather. then checked. then checked again.",
                "the water is dirty and it's EVERYONE'S problem",
                "performed a full self-inspection. results: acceptable. barely.",
                "refuses to sit where another duck sat. standards.",
                "groomed himself to perfection. looked at you. sighed.",
            ])

        if quirks:
            return random.choice(quirks)

        # Fallback pool for when no traits are particularly strong
        generic_quirks = [
            "is just being a duck",
            "stared at the pond. the pond stared back. nobody won.",
            "did a small quack. for no reason. moved on.",
            "exists in the pond. has no further comment.",
            "looked at you. looked away. that's it. that's the update.",
            "had a moment. it passed.",
            "found a spot. sat in it. this is the whole story.",
            "bobbed gently. with intent.",
            "is here. that's his contribution.",
            "did something. won't say what. probably nothing.",
            "preened once. briefly. without enthusiasm.",
            "contemplated the water. reached no conclusions.",
        ]
        return random.choice(generic_quirks)
