"""
Interaction Animation System - Displays duck+item animation scenes in the playfield.
Manages multi-frame animations that overlay on the playfield during interactions.
"""
from typing import List, Optional, Tuple, Dict, Any
from dataclasses import dataclass, field
import time


@dataclass
class AnimationFrame:
    """A single frame of an animation."""
    lines: List[str]  # ASCII art lines for this frame
    duration: float = 0.4  # How long to show this frame
    duck_visible: bool = True  # Whether to show normal duck alongside


@dataclass
class AnimationScene:
    """A complete multi-frame animation scene."""
    item_id: str
    frames: List[AnimationFrame]
    position: Tuple[int, int]  # Where to render in playfield
    item_color: Optional[Any] = None  # Color function for the item
    current_frame_idx: int = 0
    start_time: float = 0.0
    frame_start_time: float = 0.0
    completed: bool = False
    on_complete: Optional[Any] = None  # Callback when animation ends

    def get_current_frame(self) -> Optional[AnimationFrame]:
        """Get the current animation frame."""
        if 0 <= self.current_frame_idx < len(self.frames):
            return self.frames[self.current_frame_idx]
        return None

    def update(self) -> bool:
        """
        Update animation state.
        Returns True if still playing, False if completed.
        """
        if self.completed:
            return False

        current = time.time()
        frame = self.get_current_frame()

        if not frame:
            self.completed = True
            return False

        # Check if current frame duration has elapsed
        if current - self.frame_start_time >= frame.duration:
            self.current_frame_idx += 1
            self.frame_start_time = current

            if self.current_frame_idx >= len(self.frames):
                self.completed = True
                return False

        return True

    def get_elapsed_time(self) -> float:
        """Get total elapsed time since animation started."""
        return time.time() - self.start_time


class InteractionAnimator:
    """
    Manages active interaction animations in the playfield.

    This system overlays animations on top of the playfield during
    duck-item interactions to show rich visual feedback.
    """

    def __init__(self):
        self._active_scene: Optional[AnimationScene] = None
        self._duck_hidden: bool = False  # Hide normal duck during animation
        self._animations_db: Dict[str, List[AnimationFrame]] = {}
        self._load_animation_frames()

    def _load_animation_frames(self):
        """Load pre-defined animation frames for each item type."""
        # Ball bouncing animation
        self._animations_db["toy_ball"] = [
            AnimationFrame([
                "     O    ",
                "    /|\\   ",
                "   / | \\  ",
                "  (o_o)   ",
                "   /|\\    ",
                "   / \\    ",
            ], duration=0.4),
            AnimationFrame([
                "          ",
                "      O   ",
                "     /    ",
                "  (^o^)   ",
                "   \\|/    ",
                "   / \\    ",
            ], duration=0.3),
            AnimationFrame([
                "          ",
                "          ",
                "        O ",
                "  (^o^)/  ",
                "   /|     ",
                "   / \\    ",
            ], duration=0.3),
            AnimationFrame([
                "          ",
                "       O  ",
                "      /   ",
                "  (o_o)   ",
                "   /|\\    ",
                "   / \\    ",
            ], duration=0.3),
            AnimationFrame([
                "     O    ",
                "    /     ",
                "          ",
                "  (^-^)   ",
                "   /|\\    ",
                "   / \\    ",
            ], duration=0.4),
        ]

        # Birdbath splashing animation
        self._animations_db["birdbath"] = [
            AnimationFrame([
                "   ~~~    ",
                " [~~~~~]  ",
                "  \\   /   ",
                "   | |    ",
                " (o_o)    ",
                "  /|\\     ",
            ], duration=0.3),
            AnimationFrame([
                " * ~~~ *  ",
                " [~~~~~]  ",
                "  \\(o)/   ",
                "   |_|    ",
                "          ",
                "   / \\    ",
            ], duration=0.3),
            AnimationFrame([
                "* * ~ * * ",
                " [~~~~~]  ",
                "  \\(^)/   ",
                "   |_|    ",
                "          ",
                "   / \\    ",
            ], duration=0.4),
            AnimationFrame([
                " *     *  ",
                "  * ~ *   ",
                " [~~~~~]  ",
                "  \\(^)/   ",
                "   |_|    ",
                "   / \\    ",
            ], duration=0.4),
            AnimationFrame([
                "          ",
                "   ~~~    ",
                " [~~~~~]  ",
                "  \\(-)/   ",
                "   |_|    ",
                "   / \\    ",
            ], duration=0.3),
        ]

        # Pool splashing animation
        self._animations_db["pool_kiddie"] = [
            AnimationFrame([
                " ╔═════╗  ",
                " ║~~~~~║  ",
                " ║~~~~~║  ",
                " ╚═════╝  ",
                "  (o_o)   ",
                "   /|\\    ",
            ], duration=0.3),
            AnimationFrame([
                " ╔═════╗  ",
                " ║~~*~~║  ",
                " ║(o_o)║  ",
                " ╚═════╝  ",
                "          ",
                "   / \\    ",
            ], duration=0.4),
            AnimationFrame([
                "    * *   ",
                " ╔═════╗  ",
                " ║~*~*~║  ",
                " ║(^-^)║  ",
                " ╚═════╝  ",
                "          ",
            ], duration=0.4),
            AnimationFrame([
                "  *   *   ",
                "    *     ",
                " ╔═════╗  ",
                " ║~~~~~║  ",
                " ║(^o^)║  ",
                " ╚═════╝  ",
            ], duration=0.4),
            AnimationFrame([
                "          ",
                " ╔═════╗  ",
                " ║~~~~~║  ",
                " ║(o_o)║  ",
                " ╚═════╝  ",
                "   / \\    ",
            ], duration=0.3),
        ]

        # Trampoline bouncing animation
        self._animations_db["toy_trampoline"] = [
            AnimationFrame([
                "          ",
                "  (o_o)   ",
                "   /|\\    ",
                "   / \\    ",
                " ╱╲╱╲╱╲   ",
                " ══════   ",
            ], duration=0.3),
            AnimationFrame([
                "          ",
                "          ",
                "  (^o^)   ",
                "   \\|/    ",
                " ╱╲╱╲╱╲   ",
                " ══════   ",
            ], duration=0.2),
            AnimationFrame([
                "  (^o^)   ",
                "   \\|/    ",
                "          ",
                "          ",
                " ╱╲╱╲╱╲   ",
                " ══════   ",
            ], duration=0.3),
            AnimationFrame([
                "          ",
                "  (^-^)   ",
                "   /|\\    ",
                "          ",
                " ╱╲╱╲╱╲   ",
                " ══════   ",
            ], duration=0.2),
            AnimationFrame([
                "          ",
                "          ",
                "  (o_o)   ",
                "   /|\\    ",
                " ╱╲╱╲╱╲   ",
                " ══════   ",
            ], duration=0.3),
        ]

        # Swing animation
        self._animations_db["toy_swing"] = [
            AnimationFrame([
                "   ╔═╗    ",
                "   ║ ║    ",
                "  (o_o)   ",
                "   ╚═╝    ",
                "          ",
                "          ",
            ], duration=0.4),
            AnimationFrame([
                "   ╔═╗    ",
                "  /║ ║    ",
                " (^o^)    ",
                "   ╚═╝    ",
                "          ",
                "          ",
            ], duration=0.3),
            AnimationFrame([
                "   ╔═╗    ",
                "   ║ ║\\   ",
                "    (^o^) ",
                "   ╚═╝    ",
                "          ",
                "          ",
            ], duration=0.3),
            AnimationFrame([
                "   ╔═╗    ",
                "   ║ ║    ",
                "  (^-^)   ",
                "   ╚═╝    ",
                "          ",
                "          ",
            ], duration=0.4),
        ]

        # Hammock relaxing animation
        self._animations_db["hammock"] = [
            AnimationFrame([
                " \\       /",
                "  \\     / ",
                "   \\   /  ",
                "   (o_o)  ",
                "   /~~~\\  ",
                "          ",
            ], duration=0.5),
            AnimationFrame([
                " \\       /",
                "  \\     / ",
                "   \\   /  ",
                "   (-_-)  ",
                "   /~~~\\  ",
                "    z z   ",
            ], duration=0.6),
            AnimationFrame([
                " \\       /",
                "  \\     / ",
                "   \\   /  ",
                "   (-_-)  ",
                "   /~~~\\  ",
                "   z Z z  ",
            ], duration=0.6),
        ]

        # Piano playing animation
        self._animations_db["toy_piano"] = [
            AnimationFrame([
                "          ",
                " ┌─────┐  ",
                " │█▒█▒█│  ",
                " └─────┘  ",
                "  (o_o)   ",
                "   /|\\    ",
            ], duration=0.3),
            AnimationFrame([
                "    ♪     ",
                " ┌─────┐  ",
                " │█▒█▒█│  ",
                " └─────┘  ",
                "  (^o^)/  ",
                "   /|     ",
            ], duration=0.3),
            AnimationFrame([
                "  ♪   ♫   ",
                " ┌─────┐  ",
                " │█▒█▒█│  ",
                " └─────┘  ",
                " \\(^o^)   ",
                "     |\\   ",
            ], duration=0.3),
            AnimationFrame([
                " ♫  ♪  ♫  ",
                " ┌─────┐  ",
                " │█▒█▒█│  ",
                " └─────┘  ",
                "  (^o^)   ",
                "   \\|/    ",
            ], duration=0.4),
        ]

        # Generic furniture resting
        self._animations_db["furniture_rest"] = [
            AnimationFrame([
                " ╔═══════╗",
                " ║       ║",
                " ║ (o_o) ║",
                " ║  /|\\  ║",
                " ╚═══════╝",
                "          ",
            ], duration=0.5),
            AnimationFrame([
                " ╔═══════╗",
                " ║       ║",
                " ║ (-_-) ║",
                " ║  /|\\  ║",
                " ╚═══════╝",
                "    z     ",
            ], duration=0.6),
            AnimationFrame([
                " ╔═══════╗",
                " ║       ║",
                " ║ (-_-) ║",
                " ║  /|\\  ║",
                " ╚═══════╝",
                "   z Z    ",
            ], duration=0.6),
        ]

    def get_animation_frames(self, item_id: str) -> List[AnimationFrame]:
        """Get animation frames for an item, with fallbacks."""
        # Direct match
        if item_id in self._animations_db:
            return self._animations_db[item_id]

        # Category-based fallbacks
        if "ball" in item_id or "toy" in item_id:
            return self._animations_db.get("toy_ball", [])
        if "bath" in item_id or "fountain" in item_id:
            return self._animations_db.get("birdbath", [])
        if "pool" in item_id or "water" in item_id:
            return self._animations_db.get("pool_kiddie", [])
        if "trampoline" in item_id:
            return self._animations_db.get("toy_trampoline", [])
        if "swing" in item_id:
            return self._animations_db.get("toy_swing", [])
        if "hammock" in item_id:
            return self._animations_db.get("hammock", [])
        if "piano" in item_id:
            return self._animations_db.get("toy_piano", [])
        if "bed" in item_id or "couch" in item_id or "chair" in item_id:
            return self._animations_db.get("furniture_rest", [])

        # Default empty
        return []

    def get_animation_frames_with_stage(self, item_id: str, growth_stage: str = "adult") -> List[AnimationFrame]:
        """
        Get animation frames for an item with life-stage support.
        Uses animations from world/item_interactions.py with stage-specific variants.
        
        Args:
            item_id: The item being interacted with
            growth_stage: The duck's current growth stage
            
        Returns:
            List of AnimationFrame objects
        """
        from world.item_interactions import (
            INTERACTION_ANIMATIONS, ITEM_INTERACTIONS,
            get_stage_group, InteractionType
        )
        
        # Get the animation data from world/item_interactions
        animation_data = INTERACTION_ANIMATIONS.get(item_id, {})
        if not animation_data:
            # Fall back to legacy animations
            return self.get_animation_frames(item_id)
        
        # Get interaction type for this item
        interaction = ITEM_INTERACTIONS.get(item_id, {})
        interaction_type = interaction.get("type", InteractionType.USE)
        animation_key = interaction_type.value
        
        # Determine stage group and try stage-specific animation first
        stage_group = get_stage_group(growth_stage)
        stage_animation_key = f"{animation_key}_{stage_group}"
        
        # Priority: stage-specific > generic
        raw_frames = animation_data.get(stage_animation_key, [])
        if not raw_frames:
            raw_frames = animation_data.get(animation_key, [])
        
        if not raw_frames:
            # Fall back to legacy animations
            return self.get_animation_frames(item_id)
        
        # Convert raw frame lists to AnimationFrame objects
        frames = []
        for frame_lines in raw_frames:
            frames.append(AnimationFrame(
                lines=frame_lines,
                duration=0.4,
                duck_visible=False  # Duck is part of the animation
            ))
        
        return frames

    def start_animation(self, item_id: str, position: Tuple[int, int],
                       on_complete: Optional[Any] = None,
                       growth_stage: str = "adult") -> bool:
        """
        Start a new interaction animation.

        Args:
            item_id: The item being interacted with
            position: Where to render in playfield coordinates
            on_complete: Optional callback when animation finishes
            growth_stage: The duck's current growth stage (for stage-specific animations)

        Returns:
            True if animation started, False if no animation available
        """
        # Try stage-specific animations first, fall back to legacy
        frames = self.get_animation_frames_with_stage(item_id, growth_stage)
        if not frames:
            return False

        # Get item color for coloring the animation
        from ui.habitat_art import get_item_color
        item_color = get_item_color(item_id)

        self._active_scene = AnimationScene(
            item_id=item_id,
            frames=frames,
            position=position,
            item_color=item_color,
            start_time=time.time(),
            frame_start_time=time.time(),
            on_complete=on_complete
        )
        self._duck_hidden = True
        return True

    def update(self) -> bool:
        """
        Update animation state.
        Returns True if an animation is active.
        """
        if not self._active_scene:
            return False

        still_playing = self._active_scene.update()

        if not still_playing:
            # Animation completed
            if self._active_scene.on_complete:
                self._active_scene.on_complete()
            self._active_scene = None
            self._duck_hidden = False
            return False

        return True

    def get_render_data(self) -> Optional[Tuple[List[str], Tuple[int, int], bool, Optional[Any]]]:
        """
        Get data needed to render the current animation.

        Returns:
            Tuple of (frame_lines, position, show_duck, item_color) or None if no animation
        """
        if not self._active_scene:
            return None

        frame = self._active_scene.get_current_frame()
        if not frame:
            return None

        return (
            frame.lines,
            self._active_scene.position,
            frame.duck_visible,
            self._active_scene.item_color
        )

    def should_hide_duck(self) -> bool:
        """Whether the normal duck sprite should be hidden."""
        return self._duck_hidden

    def is_animating(self) -> bool:
        """Check if an animation is currently playing."""
        return self._active_scene is not None

    def get_animating_item_id(self) -> Optional[str]:
        """Get the item_id of the item currently being animated, or None."""
        if self._active_scene:
            return self._active_scene.item_id
        return None

    def cancel_animation(self):
        """Cancel the current animation."""
        self._active_scene = None
        self._duck_hidden = False

    def get_animation_progress(self) -> float:
        """Get progress of current animation (0.0 to 1.0)."""
        if not self._active_scene:
            return 0.0

        total_frames = len(self._active_scene.frames)
        if total_frames == 0:
            return 0.0

        return self._active_scene.current_frame_idx / total_frames
