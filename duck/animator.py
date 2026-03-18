"""
Duck animation and movement module.

Extracted from renderer.py's DuckPosition class into a standalone, testable
animation module with no UI/Terminal dependencies (pure logic).

Provides DuckAnimator (full duck state machine) and NPCAnimator (simplified
version for visitor characters).
"""
import random
import time
from enum import Enum
from typing import Optional, Callable, Tuple


class AnimationState(Enum):
    """Animation states for the duck."""
    IDLE = "idle"
    WALKING = "walking"
    EATING = "eating"
    SLEEPING = "sleeping"
    PLAYING = "playing"
    CLEANING = "cleaning"
    SWIMMING = "swimming"
    PETTING = "petting"
    SICK = "sick"
    HIDING = "hiding"
    CUSTOM = "custom"


class DuckAnimator:
    """Tracks duck position, movement, and animation state in the playfield.

    This is a pure-logic state machine extracted from the renderer's DuckPosition
    class.  It handles:
      - Grid-based movement toward a target (one cell per step)
      - Idle wandering with configurable probability and timing
      - Directed movement with completion callbacks
      - State-specific animation frame cycling
      - Motivation-dependent walk speed

    All timing values are ported directly from the original DuckPosition.
    """

    # States that support animation-frame cycling.
    # Only includes states that exist for all growth stages.
    ANIMATABLE_STATES = {
        # User interaction states
        "sleeping", "eating", "playing", "cleaning", "petting",
        # Weather reaction states
        "cold", "hot", "shaking", "scared", "excited", "curious", "hiding",
        # Extended animation states
        "swimming", "diving", "stretching", "yawning", "jumping",
        "thinking", "dancing", "singing", "pecking", "flapping",
        "preening", "napping", "waddle_fast", "dizzy", "proud",
        "sneaking", "splashing", "floating", "hungry", "love",
        "angry", "bored", "waving", "tail_wag", "reminiscing", "wise",
        # Enum-based names (for callers using AnimationState)
        "sick", "custom",
    }

    def __init__(self, x: int = 0, y: int = 0, play_width: int = 40,
                 play_height: int = 12, *, field_width: int = 0,
                 field_height: int = 0) -> None:
        """Initialise the duck animator.

        Args:
            x: Initial x position in playfield coordinates.
            y: Initial y position in playfield coordinates.
            play_width: Playfield width in cells.
            play_height: Playfield height in cells.
            field_width: Alias for play_width (backward compat with DuckPosition).
            field_height: Alias for play_height (backward compat with DuckPosition).
        """
        # Support DuckPosition-style keyword args
        if field_width:
            play_width = field_width
        if field_height:
            play_height = field_height
        if x == 0 and y == 0 and (field_width or field_height):
            x = play_width // 2
            y = play_height // 2
        self.x: int = x
        self.y: int = y
        self.target_x: int = x
        self.target_y: int = y
        self.facing_right: bool = True

        self._play_width: int = play_width
        self._play_height: int = play_height

        # Public readable state
        self.state: AnimationState = AnimationState.IDLE
        self.animation_frame: int = 0

        # Internal state name string -- mirrors the original ``_state`` field
        # which used raw strings like ``"idle"``, ``"walking"``, etc.  We keep
        # a parallel string so that ANIMATABLE_STATES lookup works identically
        # to the original code.
        self._state_str: str = "idle"

        # Timers
        self._move_timer: float = 0.0
        self._idle_timer: float = 0.0
        self._state_animation_timer: float = 0.0
        self._state_duration: float = 0.0
        self._state_start_time: float = 0.0

        # Movement callback support for animated interactions
        self._movement_callback: Optional[Callable] = None
        self._movement_callback_data = None
        self._is_directed_movement: bool = False
        self._original_position: Optional[Tuple[int, int]] = None

        # Motivation affects walk speed (set externally by game loop)
        self.motivation: float = 1.0

        # Tracks whether the animator is currently translating
        self._is_moving: bool = False

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def play_width(self) -> int:
        """Current playfield width."""
        return self._play_width

    @play_width.setter
    def play_width(self, value: int) -> None:
        self._play_width = value

    @property
    def play_height(self) -> int:
        """Current playfield height."""
        return self._play_height

    @play_height.setter
    def play_height(self, value: int) -> None:
        self._play_height = value

    # Backward-compatible aliases for DuckPosition API
    @property
    def field_width(self) -> int:
        return self._play_width

    @field_width.setter
    def field_width(self, value: int) -> None:
        self._play_width = value

    @property
    def field_height(self) -> int:
        return self._play_height

    @field_height.setter
    def field_height(self, value: int) -> None:
        self._play_height = value

    @property
    def is_moving(self) -> bool:
        return self._is_moving

    @is_moving.setter
    def is_moving(self, value: bool) -> None:
        self._is_moving = value

    @property
    def _motivation(self) -> float:
        return self.motivation

    @_motivation.setter
    def _motivation(self, value: float) -> None:
        self.motivation = value

    @property
    def _animation_frame(self) -> int:
        return self.animation_frame

    @_animation_frame.setter
    def _animation_frame(self, value: int) -> None:
        self.animation_frame = value

    # ------------------------------------------------------------------
    # Core update
    # ------------------------------------------------------------------

    def update(self, delta_time: float) -> None:
        """Advance the animation/movement state machine by *delta_time* seconds.

        This replicates the exact logic of the original ``DuckPosition.update``
        method, preserving all timing constants and behavioural quirks.
        """
        self._move_timer += delta_time
        self._idle_timer += delta_time
        self._state_animation_timer += delta_time

        # Walk speed scales with motivation (0.10s at full -> 0.25s at zero).
        # Original formula: ``0.10 + (1.0 - motivation) * 0.15``
        step_interval: float = 0.10 + (1.0 - self.motivation) * 0.15

        # ----- Directed movement (highest priority) -----
        if self._is_directed_movement:
            if self.x != self.target_x or self.y != self.target_y:
                self._is_moving = True
                if self._move_timer > step_interval:
                    self._move_timer = 0.0
                    self.animation_frame = (self.animation_frame + 1) % 4

                    # Move one step toward target
                    if self.x < self.target_x:
                        self.x += 1
                        self.facing_right = True
                    elif self.x > self.target_x:
                        self.x -= 1
                        self.facing_right = False

                    if self.y < self.target_y:
                        self.y += 1
                    elif self.y > self.target_y:
                        self.y -= 1
            else:
                # Reached directed-movement target
                self._is_moving = False
                if self._movement_callback:
                    callback = self._movement_callback
                    callback_data = self._movement_callback_data
                    self._movement_callback = None
                    self._movement_callback_data = None
                    self._is_directed_movement = False
                    callback(callback_data)
                else:
                    self._is_directed_movement = False
            return  # Don't process other movement while directed

        # ----- Animatable-state frame cycling (every 0.25 s) -----
        if self._state_str in self.ANIMATABLE_STATES:
            if self._state_animation_timer > 0.25:
                self.animation_frame = (self.animation_frame + 1) % 2
                self._state_animation_timer = 0.0

            # Check whether the timed state has expired
            if self._state_duration > 0:
                if time.time() - self._state_start_time > self._state_duration:
                    self._state_str = "idle"
                    self.state = AnimationState.IDLE
                    self._state_duration = 0.0
            return  # Don't wander while in a special state

        # ----- Idle wandering -----
        if (self._state_str == "idle"
                and not self._is_directed_movement
                and self._idle_timer > random.uniform(1.5, 4.0)):
            if random.random() < 0.7:  # 70% chance to wander
                self._pick_new_target()
                self._idle_timer = 0.0

        # ----- Normal walk toward target -----
        if self.x != self.target_x or self.y != self.target_y:
            self._is_moving = True
            self._state_str = "walking"
            self.state = AnimationState.WALKING

            if self._move_timer > step_interval:
                self._move_timer = 0.0
                self.animation_frame = (self.animation_frame + 1) % 4

                if self.x < self.target_x:
                    self.x += 1
                    self.facing_right = True
                elif self.x > self.target_x:
                    self.x -= 1
                    self.facing_right = False

                if self.y < self.target_y:
                    self.y += 1
                elif self.y > self.target_y:
                    self.y -= 1
        else:
            # Reached wander target
            self._is_moving = False
            if self._state_str == "walking":
                self._state_str = "idle"
                self.state = AnimationState.IDLE
                self._idle_timer = 0.0

    # ------------------------------------------------------------------
    # Movement commands
    # ------------------------------------------------------------------

    def move_to(
        self,
        target_x: int,
        target_y: int,
        callback: Optional[Callable] = None,
        callback_data=None,
        save_original: bool = True,
    ) -> None:
        """Move the duck to a specific target with an optional arrival callback.

        Args:
            target_x: Target x position in playfield coordinates.
            target_y: Target y position in playfield coordinates.
            callback: Function called when the duck reaches the target.
                      Receives *callback_data* as its sole argument.
            callback_data: Arbitrary data forwarded to *callback*.
            save_original: If ``True``, remember the current position so
                           :meth:`return_to_original` can restore it later.
        """
        margin = 2
        max_x = max(margin, self._play_width - margin - 6)
        max_y = max(margin, self._play_height - margin - 3)
        target_x = max(margin, min(target_x, max_x))
        target_y = max(margin, min(target_y, max_y))

        if save_original and self._original_position is None:
            self._original_position = (self.x, self.y)

        self.target_x = target_x
        self.target_y = target_y
        self._movement_callback = callback
        self._movement_callback_data = callback_data
        self._is_directed_movement = True
        self._state_str = "walking"
        self.state = AnimationState.WALKING
        self._is_moving = True

        self.facing_right = target_x >= self.x

    def return_to_original(
        self,
        callback: Optional[Callable] = None,
        callback_data=None,
    ) -> None:
        """Move the duck back to the position it was at before directed movement.

        If no original position is stored, *callback* is invoked immediately.
        """
        if self._original_position:
            orig_x, orig_y = self._original_position
            self._original_position = None
            self.move_to(orig_x, orig_y, callback, callback_data, save_original=False)
        else:
            if callback:
                callback(callback_data)

    def wander(self) -> None:
        """Pick a random nearby target (same logic as idle wander)."""
        self._pick_new_target()

    def stop(self) -> None:
        """Cancel all movement and return to idle."""
        self._movement_callback = None
        self._movement_callback_data = None
        self._is_directed_movement = False
        self._original_position = None
        self.target_x = self.x
        self.target_y = self.y
        self._is_moving = False
        self._state_str = "idle"
        self.state = AnimationState.IDLE

    def cancel_movement(self) -> None:
        """Cancel any pending directed movement and callbacks.

        Alias retained for backward compatibility with renderer code.
        """
        self.stop()

    # ------------------------------------------------------------------
    # State management
    # ------------------------------------------------------------------

    def set_state(self, state, duration: float = 3.0) -> None:
        """Transition to *state* for *duration* seconds.

        Accepts either an AnimationState enum or a raw string (backward
        compatible with DuckPosition.set_state).

        Args:
            state: The target animation state (AnimationState or str).
            duration: Seconds to remain in this state (0 = indefinite).
        """
        if isinstance(state, str):
            state_str = state
            try:
                self.state = AnimationState(state)
            except ValueError:
                self.state = AnimationState.CUSTOM
        else:
            state_str = state.value if isinstance(state, AnimationState) else str(state)
            self.state = state if isinstance(state, AnimationState) else AnimationState.IDLE
        self._state_str = state_str
        self.animation_frame = 0
        self._state_animation_timer = 0.0
        self._state_duration = duration
        self._state_start_time = time.time()

        # Stop moving during animatable states
        if state_str in self.ANIMATABLE_STATES:
            self.target_x = self.x
            self.target_y = self.y
            self._is_moving = False
            self._is_directed_movement = False
            self._movement_callback = None
            self._movement_callback_data = None

    def set_state_by_name(self, name: str, duration: float = 3.0) -> None:
        """Transition using a raw state name string (e.g. ``"sleeping"``).

        This mirrors the original ``DuckPosition.set_state`` interface which
        accepted arbitrary strings.
        """
        self._state_str = name
        # Try to map to an AnimationState enum; fall back to CUSTOM.
        try:
            self.state = AnimationState(name)
        except ValueError:
            self.state = AnimationState.CUSTOM
        self.animation_frame = 0
        self._state_animation_timer = 0.0
        self._state_duration = duration
        self._state_start_time = time.time()

        if name in self.ANIMATABLE_STATES:
            self.target_x = self.x
            self.target_y = self.y
            self._is_moving = False
            self._is_directed_movement = False
            self._movement_callback = None
            self._movement_callback_data = None

    def get_state(self) -> str:
        """Return the current state as a raw string.

        Returns the string representation for backward compatibility with
        DuckPosition callers (renderer, game.py).
        """
        return self._state_str

    def get_state_name(self) -> str:
        """Alias for get_state() — returns the raw string state name."""
        return self._state_str

    def get_state_enum(self) -> AnimationState:
        """Return the current animation state as an enum."""
        return self.state

    def get_animation_frame(self) -> int:
        """Return the current animation frame index."""
        return self.animation_frame

    # is_moving is defined as a property earlier in the class for
    # backward compatibility with DuckPosition's attribute-style access.

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _pick_new_target(self) -> None:
        """Pick a random target position within the playfield bounds.

        Uses the same margins as the original ``DuckPosition._pick_new_target``.
        """
        margin = 3
        max_x = max(margin, self._play_width - margin - 6)
        max_y = max(margin, self._play_height - margin - 3)
        self.target_x = random.randint(margin, max_x)
        self.target_y = random.randint(margin, max_y)


# ---------------------------------------------------------------------------
# NPCAnimator -- simplified version for visitor characters
# ---------------------------------------------------------------------------

class NPCState(Enum):
    """Animation states for NPC visitors."""
    IDLE = "idle"
    WALKING = "walking"
    TALKING = "talking"


class NPCAnimator:
    """Simplified movement and animation for visitor NPCs.

    Shares the same grid-based movement approach as :class:`DuckAnimator` but
    only supports three states: idle, walking, and talking.  No eating,
    sleeping, or weather-reaction animations.
    """

    def __init__(self, x: int, y: int, play_width: int, play_height: int) -> None:
        """Initialise the NPC animator.

        Args:
            x: Initial x position.
            y: Initial y position.
            play_width: Playfield width in cells.
            play_height: Playfield height in cells.
        """
        self.x: int = x
        self.y: int = y
        self.target_x: int = x
        self.target_y: int = y
        self.facing_right: bool = True
        self.state: NPCState = NPCState.IDLE
        self.animation_frame: int = 0

        self._play_width: int = play_width
        self._play_height: int = play_height

        self._move_timer: float = 0.0
        self._idle_timer: float = 0.0
        self._state_animation_timer: float = 0.0
        self._state_duration: float = 0.0
        self._state_start_time: float = 0.0

        self._movement_callback: Optional[Callable] = None
        self._movement_callback_data = None
        self._is_directed_movement: bool = False
        self._is_moving: bool = False

        # NPCs walk a bit slower than the duck
        self._step_interval: float = 0.14

    # ------------------------------------------------------------------
    # Core update
    # ------------------------------------------------------------------

    def update(self, delta_time: float) -> None:
        """Advance the NPC's state machine by *delta_time* seconds."""
        self._move_timer += delta_time
        self._idle_timer += delta_time
        self._state_animation_timer += delta_time

        # --- Directed movement ---
        if self._is_directed_movement:
            if self.x != self.target_x or self.y != self.target_y:
                self._is_moving = True
                if self._move_timer > self._step_interval:
                    self._move_timer = 0.0
                    self.animation_frame = (self.animation_frame + 1) % 4

                    if self.x < self.target_x:
                        self.x += 1
                        self.facing_right = True
                    elif self.x > self.target_x:
                        self.x -= 1
                        self.facing_right = False

                    if self.y < self.target_y:
                        self.y += 1
                    elif self.y > self.target_y:
                        self.y -= 1
            else:
                self._is_moving = False
                if self._movement_callback:
                    callback = self._movement_callback
                    callback_data = self._movement_callback_data
                    self._movement_callback = None
                    self._movement_callback_data = None
                    self._is_directed_movement = False
                    callback(callback_data)
                else:
                    self._is_directed_movement = False
            return

        # --- Talking state (frame cycle every 0.25 s) ---
        if self.state == NPCState.TALKING:
            if self._state_animation_timer > 0.25:
                self.animation_frame = (self.animation_frame + 1) % 2
                self._state_animation_timer = 0.0
            if self._state_duration > 0:
                if time.time() - self._state_start_time > self._state_duration:
                    self.state = NPCState.IDLE
                    self._state_duration = 0.0
            return

        # --- Idle wandering (less frequent than duck) ---
        if (self.state == NPCState.IDLE
                and not self._is_directed_movement
                and self._idle_timer > random.uniform(3.0, 7.0)):
            if random.random() < 0.5:
                self._pick_new_target()
                self._idle_timer = 0.0

        # --- Normal walk ---
        if self.x != self.target_x or self.y != self.target_y:
            self._is_moving = True
            self.state = NPCState.WALKING

            if self._move_timer > self._step_interval:
                self._move_timer = 0.0
                self.animation_frame = (self.animation_frame + 1) % 4

                if self.x < self.target_x:
                    self.x += 1
                    self.facing_right = True
                elif self.x > self.target_x:
                    self.x -= 1
                    self.facing_right = False

                if self.y < self.target_y:
                    self.y += 1
                elif self.y > self.target_y:
                    self.y -= 1
        else:
            self._is_moving = False
            if self.state == NPCState.WALKING:
                self.state = NPCState.IDLE
                self._idle_timer = 0.0

    # ------------------------------------------------------------------
    # Movement commands
    # ------------------------------------------------------------------

    def move_to(
        self,
        target_x: int,
        target_y: int,
        callback: Optional[Callable] = None,
        callback_data=None,
    ) -> None:
        """Move the NPC to a specific position with an optional callback."""
        margin = 2
        max_x = max(margin, self._play_width - margin - 6)
        max_y = max(margin, self._play_height - margin - 3)
        target_x = max(margin, min(target_x, max_x))
        target_y = max(margin, min(target_y, max_y))

        self.target_x = target_x
        self.target_y = target_y
        self._movement_callback = callback
        self._movement_callback_data = callback_data
        self._is_directed_movement = True
        self.state = NPCState.WALKING
        self._is_moving = True
        self.facing_right = target_x >= self.x

    def wander(self) -> None:
        """Pick a random nearby target."""
        self._pick_new_target()

    def stop(self) -> None:
        """Cancel all movement and return to idle."""
        self._movement_callback = None
        self._movement_callback_data = None
        self._is_directed_movement = False
        self.target_x = self.x
        self.target_y = self.y
        self._is_moving = False
        self.state = NPCState.IDLE

    # ------------------------------------------------------------------
    # State management
    # ------------------------------------------------------------------

    def set_state(self, state: NPCState, duration: float = 0.0) -> None:
        """Transition to *state* for *duration* seconds."""
        self.state = state
        self.animation_frame = 0
        self._state_animation_timer = 0.0
        self._state_duration = duration
        self._state_start_time = time.time()

        if state == NPCState.TALKING:
            self.target_x = self.x
            self.target_y = self.y
            self._is_moving = False
            self._is_directed_movement = False

    def get_state(self) -> NPCState:
        """Return the current NPC state."""
        return self.state

    def get_animation_frame(self) -> int:
        """Return the current animation frame index."""
        return self.animation_frame

    def is_moving(self) -> bool:
        """Return ``True`` if the NPC is currently translating."""
        return self._is_moving

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _pick_new_target(self) -> None:
        """Pick a random target within playfield bounds."""
        margin = 3
        max_x = max(margin, self._play_width - margin - 6)
        max_y = max(margin, self._play_height - margin - 3)
        self.target_x = random.randint(margin, max_x)
        self.target_y = random.randint(margin, max_y)
