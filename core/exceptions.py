"""
Custom exception hierarchy for Cheese the Duck.

Provides structured, specific exception types for each game subsystem so that
callers can catch narrowly and logging can include machine-readable context.
"""
from typing import Any, Dict, Optional


class GameError(Exception):
    """Base exception for all game-related errors.

    Parameters
    ----------
    message : str, optional
        Human-readable description of the error.
    details : dict, optional
        Arbitrary key/value context (logged, never shown to the player).
    """

    def __init__(
        self,
        message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.message: str = message or self.__class__.__name__
        self.details: Dict[str, Any] = details or {}
        super().__init__(self.message)

    def __repr__(self) -> str:
        if self.details:
            return f"{self.__class__.__name__}({self.message!r}, details={self.details!r})"
        return f"{self.__class__.__name__}({self.message!r})"


class SaveError(GameError):
    """Raised when persisting game state fails (file I/O, serialisation)."""


class LoadError(GameError):
    """Raised when loading or migrating a save file fails."""


class ValidationError(GameError):
    """Raised when game-state validation detects an inconsistency."""


class AudioError(GameError):
    """Raised when the sound/music subsystem encounters an error."""


class DialogueError(GameError):
    """Raised when the conversation or dialogue system fails."""


class RenderError(GameError):
    """Raised when the rendering pipeline encounters an error."""


class EventError(GameError):
    """Raised when the event bus encounters an error (e.g. recursion limit)."""
