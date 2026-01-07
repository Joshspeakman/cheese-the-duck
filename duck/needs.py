"""
Needs system for the duck - hunger, energy, fun, cleanliness, social.
"""
from typing import Dict, Optional
from dataclasses import dataclass, field

from config import (
    NEED_DECAY_RATES,
    NEED_MAX,
    NEED_MIN,
    NEED_CRITICAL,
    NEED_LOW,
    INTERACTION_EFFECTS,
)


@dataclass
class Needs:
    """
    Manages the duck's five core needs.
    Each need is a value from 0-100.
    """

    hunger: float = 50.0
    energy: float = 50.0
    fun: float = 50.0
    cleanliness: float = 50.0
    social: float = 50.0

    def __post_init__(self):
        """Clamp all values to valid range."""
        self._clamp_all()

    def _clamp(self, value: float) -> float:
        """Clamp a value to the valid need range."""
        return max(NEED_MIN, min(NEED_MAX, value))

    def _clamp_all(self):
        """Clamp all needs to valid range."""
        self.hunger = self._clamp(self.hunger)
        self.energy = self._clamp(self.energy)
        self.fun = self._clamp(self.fun)
        self.cleanliness = self._clamp(self.cleanliness)
        self.social = self._clamp(self.social)

    def update(self, delta_minutes: float, personality: Optional[dict] = None):
        """
        Update needs based on time passed.

        Args:
            delta_minutes: Real minutes that passed
            personality: Optional personality dict to modify decay rates
        """
        # Get decay modifiers from personality
        modifiers = self._get_personality_modifiers(personality or {})

        # Apply decay
        self.hunger -= NEED_DECAY_RATES["hunger"] * delta_minutes * modifiers.get("hunger", 1.0)
        self.energy -= NEED_DECAY_RATES["energy"] * delta_minutes * modifiers.get("energy", 1.0)
        self.fun -= NEED_DECAY_RATES["fun"] * delta_minutes * modifiers.get("fun", 1.0)
        self.cleanliness -= NEED_DECAY_RATES["cleanliness"] * delta_minutes * modifiers.get("cleanliness", 1.0)
        self.social -= NEED_DECAY_RATES["social"] * delta_minutes * modifiers.get("social", 1.0)

        self._clamp_all()

    def _get_personality_modifiers(self, personality: dict) -> dict:
        """
        Get need decay modifiers based on personality.

        Personality traits affect decay rates:
        - active_lazy: Active ducks use more energy
        - social_shy: Shy ducks need less social interaction
        - neat_messy: Messy ducks get dirty faster
        """
        modifiers = {}

        # Active ducks burn energy faster, lazy ducks slower
        active_lazy = personality.get("active_lazy", 0)
        modifiers["energy"] = 1.0 + (active_lazy / 200)  # -0.5 to +0.5

        # Social ducks need more interaction, shy ducks less
        social_shy = personality.get("social_shy", 0)
        modifiers["social"] = 1.0 + (social_shy / 200)

        # Messy ducks tolerate dirt better (slower cleanliness decay)
        # Neat ducks notice dirt more (faster cleanliness decay)
        neat_messy = personality.get("neat_messy", 0)
        modifiers["cleanliness"] = 1.0 - (neat_messy / 200)  # Messy = slower decay, neat = faster decay

        return modifiers

    def apply_interaction(self, interaction: str) -> dict:
        """
        Apply the effects of an interaction.

        Args:
            interaction: Name of the interaction (feed, play, etc.)

        Returns:
            Dict of changes applied
        """
        effects = INTERACTION_EFFECTS.get(interaction, {})
        changes = {}

        for need, change in effects.items():
            if hasattr(self, need):
                old_value = getattr(self, need)
                new_value = self._clamp(old_value + change)
                setattr(self, need, new_value)
                changes[need] = new_value - old_value

        return changes

    def get_critical_needs(self) -> list:
        """Get list of needs below critical threshold."""
        critical = []
        for need in ["hunger", "energy", "fun", "cleanliness", "social"]:
            if getattr(self, need) < NEED_CRITICAL:
                critical.append(need)
        return critical

    def get_low_needs(self) -> list:
        """Get list of needs below low threshold."""
        low = []
        for need in ["hunger", "energy", "fun", "cleanliness", "social"]:
            if getattr(self, need) < NEED_LOW:
                low.append(need)
        return low

    def get_urgent_need(self) -> Optional[str]:
        """Get the most urgent need (lowest value below threshold)."""
        critical = self.get_critical_needs()
        if critical:
            return min(critical, key=lambda n: getattr(self, n))

        low = self.get_low_needs()
        if low:
            return min(low, key=lambda n: getattr(self, n))

        return None

    def to_dict(self) -> dict:
        """Convert needs to dictionary for saving."""
        return {
            "hunger": round(self.hunger, 1),
            "energy": round(self.energy, 1),
            "fun": round(self.fun, 1),
            "cleanliness": round(self.cleanliness, 1),
            "social": round(self.social, 1),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Needs":
        """Create Needs from dictionary."""
        return cls(
            hunger=data.get("hunger", 80),
            energy=data.get("energy", 100),
            fun=data.get("fun", 70),
            cleanliness=data.get("cleanliness", 100),
            social=data.get("social", 60),
        )

    def get_status_emoji(self, need: str) -> str:
        """Get a status indicator for a need."""
        value = getattr(self, need, 50)
        if value >= 80:
            return "[###]"
        elif value >= 60:
            return "[## ]"
        elif value >= 40:
            return "[#  ]"
        elif value >= 20:
            return "[!  ]"
        else:
            return "[!!!]"

    def get_all_as_bars(self, width: int = 10) -> dict:
        """Get all needs as progress bar strings."""
        bars = {}
        for need in ["hunger", "energy", "fun", "cleanliness", "social"]:
            value = getattr(self, need)
            filled = int((value / 100) * width)
            empty = width - filled

            # Color coding via markers
            if value < NEED_CRITICAL:
                marker = "!"
            elif value < NEED_LOW:
                marker = "="
            else:
                marker = "#"

            bars[need] = f"[{marker * filled}{' ' * empty}]"
        return bars
