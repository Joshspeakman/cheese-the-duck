"""
Mood Visual Effects System - Environment visuals affected by duck mood.
Changes colors, animations, and atmosphere based on mood.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class VisualMood(Enum):
    """Moods that affect visuals."""
    ECSTATIC = "ecstatic"
    HAPPY = "happy"
    CONTENT = "content"
    NEUTRAL = "neutral"
    SAD = "sad"
    ANXIOUS = "anxious"
    TIRED = "tired"
    SICK = "sick"
    EXCITED = "excited"
    ANGRY = "angry"
    SCARED = "scared"
    PLAYFUL = "playful"


@dataclass
class MoodVisualTheme:
    """Visual theme for a mood."""
    mood: VisualMood
    name: str
    description: str
    
    # Colors (for terminals that support it)
    primary_color: str
    secondary_color: str
    accent_color: str
    
    # ASCII decorations
    background_chars: List[str]
    floating_particles: List[str]
    border_style: str
    
    # Animation speed multiplier
    animation_speed: float = 1.0
    
    # Atmosphere effects
    brightness: float = 1.0  # 0.5 to 1.5
    saturation: float = 1.0
    
    # Special effects
    special_effects: List[str] = field(default_factory=list)


# Mood visual themes
MOOD_THEMES: Dict[VisualMood, MoodVisualTheme] = {
    VisualMood.ECSTATIC: MoodVisualTheme(
        mood=VisualMood.ECSTATIC,
        name="Ecstatic Joy",
        description="Everything is wonderful!",
        primary_color="bright_yellow",
        secondary_color="bright_magenta",
        accent_color="bright_cyan",
        background_chars=["✨", "⭐", "🌟", "💫", "✧"],
        floating_particles=["🎉", "🎊", "💖", "✨", "🌈"],
        border_style="double_rainbow",
        animation_speed=1.5,
        brightness=1.4,
        special_effects=["rainbow_border", "sparkle_burst", "bouncing"]
    ),
    
    VisualMood.HAPPY: MoodVisualTheme(
        mood=VisualMood.HAPPY,
        name="Happy",
        description="Life is good!",
        primary_color="yellow",
        secondary_color="green",
        accent_color="cyan",
        background_chars=["~", "·", "✿", "♪"],
        floating_particles=["💕", "🌸", "♫", "☀️"],
        border_style="curved",
        animation_speed=1.2,
        brightness=1.2,
        special_effects=["gentle_glow", "floating_hearts"]
    ),
    
    VisualMood.CONTENT: MoodVisualTheme(
        mood=VisualMood.CONTENT,
        name="Content",
        description="Peaceful and relaxed",
        primary_color="green",
        secondary_color="cyan",
        accent_color="white",
        background_chars=["·", ".", "~"],
        floating_particles=["☁️", "🌿", "💚"],
        border_style="simple",
        animation_speed=0.8,
        brightness=1.0,
        special_effects=["calm_aura"]
    ),
    
    VisualMood.NEUTRAL: MoodVisualTheme(
        mood=VisualMood.NEUTRAL,
        name="Neutral",
        description="Just... existing",
        primary_color="white",
        secondary_color="gray",
        accent_color="cyan",
        background_chars=[".", " "],
        floating_particles=[],
        border_style="simple",
        animation_speed=1.0,
        brightness=1.0,
        special_effects=[]
    ),
    
    VisualMood.SAD: MoodVisualTheme(
        mood=VisualMood.SAD,
        name="Sad",
        description="Feeling blue...",
        primary_color="blue",
        secondary_color="dark_blue",
        accent_color="gray",
        background_chars=[".", ":", "·", "'"],
        floating_particles=["💧", "🥀", "💔"],
        border_style="droopy",
        animation_speed=0.6,
        brightness=0.7,
        special_effects=["rain_tears", "dim_atmosphere", "drooping"]
    ),
    
    VisualMood.ANXIOUS: MoodVisualTheme(
        mood=VisualMood.ANXIOUS,
        name="Anxious",
        description="Something feels wrong...",
        primary_color="magenta",
        secondary_color="red",
        accent_color="yellow",
        background_chars=["~", "!", "?", "·"],
        floating_particles=["❓", "❗", "💦"],
        border_style="wavy",
        animation_speed=1.3,
        brightness=0.9,
        special_effects=["trembling", "flickering"]
    ),
    
    VisualMood.TIRED: MoodVisualTheme(
        mood=VisualMood.TIRED,
        name="Tired",
        description="So sleepy...",
        primary_color="dark_blue",
        secondary_color="black",
        accent_color="white",
        background_chars=["·", ".", "z"],
        floating_particles=["💤", "🌙", "☁️"],
        border_style="simple",
        animation_speed=0.4,
        brightness=0.6,
        special_effects=["drowsy", "slow_blink", "yawning"]
    ),
    
    VisualMood.SICK: MoodVisualTheme(
        mood=VisualMood.SICK,
        name="Sick",
        description="Not feeling well...",
        primary_color="green",
        secondary_color="dark_green",
        accent_color="yellow",
        background_chars=["~", "·"],
        floating_particles=["🤒", "💊", "🌡️"],
        border_style="wobbly",
        animation_speed=0.5,
        brightness=0.7,
        special_effects=["dizzy", "swirl"]
    ),
    
    VisualMood.EXCITED: MoodVisualTheme(
        mood=VisualMood.EXCITED,
        name="Excited",
        description="So much energy!",
        primary_color="yellow",
        secondary_color="orange",
        accent_color="red",
        background_chars=["!", "*", "✦", "·"],
        floating_particles=["⚡", "🔥", "💥", "✨"],
        border_style="zigzag",
        animation_speed=1.8,
        brightness=1.3,
        special_effects=["bouncing", "flashing", "speed_lines"]
    ),
    
    VisualMood.ANGRY: MoodVisualTheme(
        mood=VisualMood.ANGRY,
        name="Angry",
        description="GRRRR!",
        primary_color="red",
        secondary_color="dark_red",
        accent_color="orange",
        background_chars=["#", "!", "@", "*"],
        floating_particles=["💢", "😤", "🔥"],
        border_style="sharp",
        animation_speed=1.4,
        brightness=1.1,
        special_effects=["shake", "steam", "red_tint"]
    ),
    
    VisualMood.SCARED: MoodVisualTheme(
        mood=VisualMood.SCARED,
        name="Scared",
        description="Eep!",
        primary_color="dark_blue",
        secondary_color="black",
        accent_color="white",
        background_chars=["·", ".", " ", "?"],
        floating_particles=["😰", "💦", "👻"],
        border_style="shaky",
        animation_speed=1.2,
        brightness=0.5,
        special_effects=["trembling", "hiding", "dark_corners"]
    ),
    
    VisualMood.PLAYFUL: MoodVisualTheme(
        mood=VisualMood.PLAYFUL,
        name="Playful",
        description="Let's have fun!",
        primary_color="cyan",
        secondary_color="magenta",
        accent_color="yellow",
        background_chars=["~", "♪", "♫", "*"],
        floating_particles=["🎮", "🎪", "🎈", "🌀"],
        border_style="bouncy",
        animation_speed=1.5,
        brightness=1.2,
        special_effects=["bouncing", "silly_dance", "confetti"]
    ),
}


class MoodVisualEffects:
    """
    System for mood-based visual effects.
    """
    
    def __init__(self):
        self.current_mood: VisualMood = VisualMood.NEUTRAL
        self.transition_progress: float = 1.0  # 0.0 to 1.0 for smooth transitions
        self.previous_mood: Optional[VisualMood] = None
        self.effects_enabled: bool = True
        self.particle_density: float = 1.0  # Multiplier for particles
        self.animation_frame: int = 0
    
    def set_mood(self, mood: str):
        """Set the current mood for visual effects."""
        try:
            new_mood = VisualMood(mood.lower())
        except ValueError:
            new_mood = VisualMood.NEUTRAL
        
        if new_mood != self.current_mood:
            self.previous_mood = self.current_mood
            self.current_mood = new_mood
            self.transition_progress = 0.0
    
    def update(self, delta_time: float = 0.016):
        """Update visual effects (call each frame)."""
        # Update transition
        if self.transition_progress < 1.0:
            theme = MOOD_THEMES[self.current_mood]
            self.transition_progress = min(1.0, 
                self.transition_progress + delta_time * theme.animation_speed * 2)
        
        # Update animation frame
        self.animation_frame += 1
    
    def get_current_theme(self) -> MoodVisualTheme:
        """Get the current mood theme."""
        return MOOD_THEMES.get(self.current_mood, MOOD_THEMES[VisualMood.NEUTRAL])
    
    def generate_particles(self) -> List[str]:
        """Generate floating particle decorations."""
        if not self.effects_enabled:
            return []
        
        theme = self.get_current_theme()
        if not theme.floating_particles:
            return []
        
        import random
        num_particles = int(3 * self.particle_density * theme.animation_speed)
        particles = []
        
        for _ in range(num_particles):
            particle = random.choice(theme.floating_particles)
            particles.append(particle)
        
        return particles
    
    def generate_background_decoration(self, width: int = 40, height: int = 10) -> List[str]:
        """Generate background decoration pattern."""
        if not self.effects_enabled:
            return [" " * width for _ in range(height)]
        
        import random
        theme = self.get_current_theme()
        lines = []
        
        for _ in range(height):
            line = ""
            for _ in range(width):
                if random.random() < 0.1 * theme.brightness:
                    char = random.choice(theme.background_chars) if theme.background_chars else " "
                else:
                    char = " "
                line += char
            lines.append(line)
        
        return lines
    
    def get_border_chars(self) -> Dict[str, str]:
        """Get border characters based on current mood."""
        theme = self.get_current_theme()
        
        borders = {
            "simple": {
                "tl": "┌", "tr": "┐", "bl": "└", "br": "┘",
                "h": "─", "v": "│"
            },
            "curved": {
                "tl": "╭", "tr": "╮", "bl": "╰", "br": "╯",
                "h": "─", "v": "│"
            },
            "double_rainbow": {
                "tl": "╔", "tr": "╗", "bl": "╚", "br": "╝",
                "h": "═", "v": "║"
            },
            "wavy": {
                "tl": "~", "tr": "~", "bl": "~", "br": "~",
                "h": "~", "v": "¦"
            },
            "zigzag": {
                "tl": "⌜", "tr": "⌝", "bl": "⌞", "br": "⌟",
                "h": "⌇", "v": "⌇"
            },
            "sharp": {
                "tl": "◢", "tr": "◣", "bl": "◥", "br": "◤",
                "h": "▬", "v": "▐"
            },
            "droopy": {
                "tl": "╭", "tr": "╮", "bl": "⌣", "br": "⌣",
                "h": "─", "v": "│"
            },
            "shaky": {
                "tl": "┌", "tr": "┐", "bl": "└", "br": "┘",
                "h": "~", "v": "¦"
            },
            "bouncy": {
                "tl": "●", "tr": "●", "bl": "●", "br": "●",
                "h": "○", "v": "○"
            },
            "wobbly": {
                "tl": "~", "tr": "~", "bl": "~", "br": "~",
                "h": "≈", "v": "§"
            },
        }
        
        return borders.get(theme.border_style, borders["simple"])
    
    def apply_mood_filter(self, text: str) -> str:
        """Apply mood-based text modifications."""
        if not self.effects_enabled:
            return text
        
        theme = self.get_current_theme()
        
        # Add effects based on mood
        if "trembling" in theme.special_effects:
            # Add shake effect (in a real implementation, this would animate)
            pass
        
        if "bouncing" in theme.special_effects:
            # Could add bounce indicators
            pass
        
        return text
    
    def render_mood_atmosphere(self) -> List[str]:
        """Render the mood atmosphere overlay."""
        theme = self.get_current_theme()
        
        lines = []
        
        # Top particles
        particles = self.generate_particles()
        if particles:
            particle_line = "  ".join(particles[:5])
            lines.append(f"  {particle_line}  ")
        
        return lines
    
    def render_mood_indicator(self) -> List[str]:
        """Render a visual mood indicator."""
        theme = self.get_current_theme()
        
        # Mood face based on mood
        faces = {
            VisualMood.ECSTATIC: ["✧◡✧", "🤩"],
            VisualMood.HAPPY: ["^◡^", "😊"],
            VisualMood.CONTENT: ["◡‿◡", "😌"],
            VisualMood.NEUTRAL: ["•_•", "😐"],
            VisualMood.SAD: ["╥﹏╥", "😢"],
            VisualMood.ANXIOUS: ["◉_◉", "😰"],
            VisualMood.TIRED: ["-_-", "😴"],
            VisualMood.SICK: ["×_×", "🤒"],
            VisualMood.EXCITED: ["◕‿◕", "🤩"],
            VisualMood.ANGRY: ["ಠ_ಠ", "😠"],
            VisualMood.SCARED: ["ఠ_ఠ", "😨"],
            VisualMood.PLAYFUL: ["◕ᴗ◕", "😜"],
        }
        
        face_data = faces.get(self.current_mood, ["•_•", "🦆"])
        
        import random
        particles = theme.floating_particles[:2] if theme.floating_particles else []
        particle_str = " ".join(particles) if particles else ""
        
        return [
            f"  {particle_str}  ",
            f"    {face_data[1]}     ",
            f"   ({face_data[0]})   ",
            f"  Mood: {theme.name}  ",
        ]
    
    def get_duck_expression(self) -> str:
        """Get ASCII expression for duck based on mood."""
        expressions = {
            VisualMood.ECSTATIC: "✧◡✧",
            VisualMood.HAPPY: "^◡^",
            VisualMood.CONTENT: "◡‿◡",
            VisualMood.NEUTRAL: "•_•",
            VisualMood.SAD: "╥﹏╥",
            VisualMood.ANXIOUS: "◉_◉",
            VisualMood.TIRED: "-_-",
            VisualMood.SICK: "×_×",
            VisualMood.EXCITED: "◕‿◕!",
            VisualMood.ANGRY: "ಠ益ಠ",
            VisualMood.SCARED: "°△°",
            VisualMood.PLAYFUL: "◕ᴗ◕",
        }
        
        return expressions.get(self.current_mood, "•_•")
    
    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "current_mood": self.current_mood.value,
            "effects_enabled": self.effects_enabled,
            "particle_density": self.particle_density,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "MoodVisualEffects":
        """Create from dictionary."""
        system = cls()
        
        mood_str = data.get("current_mood", "neutral")
        try:
            system.current_mood = VisualMood(mood_str)
        except ValueError:
            system.current_mood = VisualMood.NEUTRAL
        
        system.effects_enabled = data.get("effects_enabled", True)
        system.particle_density = data.get("particle_density", 1.0)
        
        return system


# Global instance
mood_visual_effects = MoodVisualEffects()
