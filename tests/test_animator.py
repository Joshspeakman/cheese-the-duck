"""Tests for duck.animator — DuckAnimator state machine."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from duck.animator import DuckAnimator, AnimationState


def test_initial_position():
    d = DuckAnimator(x=10, y=5, play_width=40, play_height=12)
    assert d.x == 10
    assert d.y == 5
    assert d.get_state() == "idle"


def test_backward_compat_constructor():
    d = DuckAnimator(field_width=44, field_height=14)
    assert d.field_width == 44
    assert d.field_height == 14
    assert d.x == 22
    assert d.y == 7


def test_set_state_with_string():
    d = DuckAnimator(x=5, y=5, play_width=20, play_height=10)
    d.set_state("sleeping", 3.0)
    assert d.get_state() == "sleeping"


def test_set_state_with_enum():
    d = DuckAnimator(x=5, y=5, play_width=20, play_height=10)
    d.set_state(AnimationState.EATING, 2.0)
    assert d.get_state() == "eating"


def test_move_to_and_update():
    d = DuckAnimator(x=5, y=5, play_width=40, play_height=12)
    d.move_to(8, 5)
    assert d._is_directed_movement
    # After enough updates, should have moved toward target
    for _ in range(50):
        d.update(0.15)
    # Duck should have reached target and then may wander further
    # Just verify it moved from the start position
    assert d.x != 5 or d.y != 5


def test_cancel_movement():
    d = DuckAnimator(x=5, y=5, play_width=40, play_height=12)
    d.move_to(20, 5)
    d.cancel_movement()
    assert d.get_state() == "idle"
    assert not d.is_moving


def test_is_moving_property():
    d = DuckAnimator(x=5, y=5, play_width=40, play_height=12)
    assert d.is_moving == False
    d.is_moving = True
    assert d.is_moving == True


def test_motivation_compat():
    d = DuckAnimator(x=5, y=5, play_width=40, play_height=12)
    d._motivation = 0.5
    assert d.motivation == 0.5


def test_animation_frame():
    d = DuckAnimator(x=5, y=5, play_width=40, play_height=12)
    assert d.get_animation_frame() == 0
    d._animation_frame = 2
    assert d.get_animation_frame() == 2
