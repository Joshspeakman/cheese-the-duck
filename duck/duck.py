"""
Duck entity - the main character of the game.
"""
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
import random
import time

from config import DEFAULT_PERSONALITY, DUCK_NAMES, GROWTH_STAGES, DEFAULT_DUCK_NAME
from duck.needs import Needs
from duck.mood import MoodCalculator, MoodState, MoodInfo
from duck.personality import Personality
from dialogue.memory import DuckMemory


@dataclass
class Duck:
    """
    The duck entity with all its state.
    """
    name: str
    created_at: str
    needs: Needs = field(default_factory=Needs)
    personality: Dict[str, int] = field(default_factory=lambda: DEFAULT_PERSONALITY.copy())
    growth_stage: str = "hatchling"
    growth_progress: float = 0.0
    current_action: Optional[str] = None
    action_start_time: Optional[float] = None
    _mood_calculator: MoodCalculator = field(default_factory=MoodCalculator, repr=False)
    _personality_system: Personality = field(default=None, repr=False)
    _memory: DuckMemory = field(default=None, repr=False)

    def __post_init__(self):
        """Initialize calculated properties."""
        self._last_autonomous_action = 0.0
        self._action_message = ""
        self._action_message_expire = 0.0  # Time when message expires
        self._action_end_time = 0.0  # Time when current_action should auto-clear
        if self._personality_system is None:
            self._personality_system = Personality(self.personality)
        if self._memory is None:
            self._memory = DuckMemory()
            self._memory.first_meeting = datetime.now().isoformat()

    @classmethod
    def create_new(cls, name: Optional[str] = None) -> "Duck":
        """Create a new duck with random personality variations."""
        if name is None:
            name = DEFAULT_DUCK_NAME  # Default to "Cheese"

        # Randomize personality a bit from defaults
        personality = {}
        for trait, default_value in DEFAULT_PERSONALITY.items():
            variation = random.randint(-20, 20)
            personality[trait] = max(-100, min(100, default_value + variation))

        return cls(
            name=name,
            created_at=datetime.now().isoformat(),
            personality=personality,
        )

    @classmethod
    def from_dict(cls, data: dict) -> "Duck":
        """Create Duck from save data dictionary."""
        personality_data = data.get("personality", DEFAULT_PERSONALITY.copy())

        duck = cls(
            name=data.get("name", DEFAULT_DUCK_NAME),
            created_at=data.get("created_at", datetime.now().isoformat()),
            needs=Needs.from_dict(data.get("needs", {})),
            personality=personality_data,
            growth_stage=data.get("growth_stage", "duckling"),
            growth_progress=data.get("growth_progress", 0.0),
            current_action=data.get("current_action"),
        )

        # Restore mood history if present
        if "mood_history" in data:
            duck._mood_calculator.set_history(data["mood_history"])

        # Restore memory if present
        if "memory" in data and data["memory"]:
            duck._memory = DuckMemory.from_dict(data["memory"])

        # Restore personality system
        duck._personality_system = Personality(personality_data)

        return duck

    def to_dict(self) -> dict:
        """Convert duck to dictionary for saving."""
        return {
            "name": self.name,
            "created_at": self.created_at,
            "needs": self.needs.to_dict(),
            "personality": self.personality,
            "growth_stage": self.growth_stage,
            "growth_progress": round(self.growth_progress, 3),
            "current_action": self.current_action,
            "mood_history": self._mood_calculator.get_history(),
            "memory": self._memory.to_dict() if self._memory else {},
        }

    @property
    def memory(self) -> DuckMemory:
        """Get the duck's memory system."""
        return self._memory

    @property
    def personality_system(self) -> Personality:
        """Get the personality system."""
        return self._personality_system

    def get_personality_summary(self) -> str:
        """Get a description of the duck's personality."""
        return self._personality_system.get_personality_summary()

    def update(self, delta_minutes: float, aging_modifiers: Optional[dict] = None):
        """
        Update the duck's state based on time passed.

        Args:
            delta_minutes: Real minutes that passed
            aging_modifiers: Optional aging stat modifiers from AgingSystem
        """
        # Update needs with personality and aging modifiers
        self.needs.update(delta_minutes, self.personality, aging_modifiers)

        # Update growth progress
        self._update_growth(delta_minutes)

    def _update_growth(self, delta_minutes: float):
        """Update growth stage progress."""
        stage_info = GROWTH_STAGES.get(self.growth_stage)
        if not stage_info or stage_info["duration_hours"] is None:
            return  # Already at final stage

        # Convert minutes to progress (0.0 to 1.0)
        hours_for_stage = stage_info["duration_hours"]
        progress_per_minute = 1.0 / (hours_for_stage * 60)

        self.growth_progress += delta_minutes * progress_per_minute

        # Check for stage advancement
        if self.growth_progress >= 1.0:
            self.growth_progress = 0.0
            if stage_info["next"]:
                self.growth_stage = stage_info["next"]

    def get_mood(self) -> MoodInfo:
        """Get the duck's current mood."""
        return self._mood_calculator.get_mood(self.needs)

    def get_mood_state(self) -> MoodState:
        """Get just the mood state enum."""
        return self.get_mood().state

    def interact(self, interaction: str) -> dict:
        """
        Perform an interaction with the duck.

        Args:
            interaction: Type of interaction (feed, play, clean, pet, sleep)

        Returns:
            Dict with results of the interaction
        """
        # Apply need changes
        changes = self.needs.apply_interaction(interaction)

        # Get mood after interaction
        mood = self.get_mood()

        # Set current action briefly for animation
        self.current_action = interaction

        return {
            "interaction": interaction,
            "changes": changes,
            "mood_after": mood.state.value,
            "mood_score": mood.score,
        }

    def get_personality_trait(self, trait: str) -> int:
        """Get a personality trait value."""
        return self.personality.get(trait, 0)

    def is_derpy(self) -> bool:
        """Check if duck is notably derpy."""
        return self.get_personality_trait("clever_derpy") < -20

    def is_active(self) -> bool:
        """Check if duck is notably active."""
        return self.get_personality_trait("active_lazy") > 20

    def is_social(self) -> bool:
        """Check if duck is notably social."""
        return self.get_personality_trait("social_shy") > 20

    def get_status_summary(self) -> str:
        """Get a brief status summary."""
        mood = self.get_mood()
        urgent = self.needs.get_urgent_need()

        summary = f"{self.name} is {mood.description}"
        if urgent:
            summary += f" (needs: {urgent})"

        return summary

    def get_age_days(self) -> float:
        """Get duck's age in days."""
        try:
            created = datetime.fromisoformat(self.created_at)
            delta = datetime.now() - created
            return delta.total_seconds() / 86400
        except (ValueError, TypeError):
            return 0.0

    @property
    def age_days(self) -> int:
        """Integer number of days since the duck was created."""
        return int(self.get_age_days())

    def get_growth_stage_display(self) -> str:
        """Get display name for current growth stage."""
        stage_names = {
            "egg": "Egg",
            "hatchling": "Hatchling",
            "duckling": "Duckling",
            "juvenile": "Juvenile",
            "teen": "Teen Duck",
            "young_adult": "Young Adult",
            "adult": "Adult Duck",
            "mature": "Mature Duck",
            "elder": "Elder Duck",
            "legendary": "Legendary Duck",
        }
        return stage_names.get(self.growth_stage, self.growth_stage.title())

    def set_action_message(self, message: str, duration: float = 5.0):
        """Set a temporary action message to display.
        
        Args:
            message: The message to display
            duration: How long to show the message in seconds (default 5s)
        """
        self._action_message = message
        self._action_message_expire = time.time() + duration

    def get_action_message(self) -> str:
        """Get the current action message (returns empty if expired)."""
        if time.time() > self._action_message_expire:
            return ""
        return self._action_message

    def clear_action(self):
        """Clear the current action."""
        self.current_action = None
        self.action_start_time = None
