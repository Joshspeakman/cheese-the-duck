"""Tests for core/exceptions.py — custom exception hierarchy."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from core.exceptions import (
    GameError,
    SaveError,
    LoadError,
    ValidationError,
    AudioError,
    DialogueError,
    RenderError,
    EventError,
)


# ═══════════════════════════════════════════════════════════════════════════
# GameError base class
# ═══════════════════════════════════════════════════════════════════════════

class TestGameError:
    """Tests for the GameError base exception."""

    def test_default_message(self) -> None:
        """With no arguments, message defaults to the class name."""
        err = GameError()
        assert err.message == "GameError"
        assert str(err) == "GameError"
        assert err.details == {}

    def test_custom_message(self) -> None:
        """A custom message is stored and used as the str()."""
        err = GameError("something broke")
        assert err.message == "something broke"
        assert str(err) == "something broke"

    def test_details_dict(self) -> None:
        """Arbitrary details are stored for logging."""
        details = {"file": "save.json", "errno": 13}
        err = GameError("oops", details=details)
        assert err.details == details

    def test_repr_with_details(self) -> None:
        """repr includes the class name and details when present."""
        err = GameError("fail", details={"x": 1})
        r = repr(err)
        assert "GameError" in r
        assert "'fail'" in r
        assert "'x'" in r

    def test_repr_without_details(self) -> None:
        """repr omits details when the dict is empty."""
        err = GameError("fail")
        r = repr(err)
        assert "GameError" in r
        assert "details" not in r

    def test_is_exception(self) -> None:
        """GameError is a proper Exception subclass."""
        err = GameError("test")
        assert isinstance(err, Exception)
        with pytest.raises(GameError):
            raise err


# ═══════════════════════════════════════════════════════════════════════════
# Subclass hierarchy
# ═══════════════════════════════════════════════════════════════════════════

class TestSubclasses:
    """Tests for the concrete exception subclasses."""

    @pytest.mark.parametrize("cls,name", [
        (SaveError, "SaveError"),
        (LoadError, "LoadError"),
        (ValidationError, "ValidationError"),
        (AudioError, "AudioError"),
        (DialogueError, "DialogueError"),
        (RenderError, "RenderError"),
        (EventError, "EventError"),
    ])
    def test_subclass_is_game_error(self, cls, name) -> None:
        """Every subclass inherits from GameError."""
        err = cls()
        assert isinstance(err, GameError)
        assert isinstance(err, Exception)
        assert err.message == name

    @pytest.mark.parametrize("cls", [
        SaveError, LoadError, ValidationError,
        AudioError, DialogueError, RenderError, EventError,
    ])
    def test_subclass_with_message_and_details(self, cls) -> None:
        """Subclasses accept message and details like the base class."""
        err = cls("broken", details={"key": "val"})
        assert err.message == "broken"
        assert err.details == {"key": "val"}

    def test_catch_specific_subclass(self) -> None:
        """A specific subclass can be caught without catching others."""
        with pytest.raises(SaveError):
            raise SaveError("disk full")

        # Catching GameError also catches SaveError
        with pytest.raises(GameError):
            raise SaveError("disk full")

    def test_catch_base_does_not_catch_unrelated(self) -> None:
        """Catching SaveError does not catch LoadError."""
        with pytest.raises(LoadError):
            raise LoadError("corrupt file")

        # But GameError catches both
        try:
            raise LoadError("corrupt")
        except GameError:
            pass  # expected

    def test_distinct_types(self) -> None:
        """Each subclass is a distinct type."""
        assert SaveError is not LoadError
        assert AudioError is not RenderError
        assert type(SaveError()) is not type(LoadError())
