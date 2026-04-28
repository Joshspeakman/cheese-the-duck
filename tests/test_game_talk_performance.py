"""Tests for first-chat hot-path behavior."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.game import Game


class _FakeConversation:
    def __init__(self, needs_context: bool):
        self.needs_context = needs_context
        self.received_context = None

    def needs_memory_context(self) -> bool:
        return self.needs_context

    def process_player_input(self, duck, message, use_llm=True, memory_context="") -> str:
        self.received_context = memory_context
        return f"reply:{message}"


def test_generate_talk_response_skips_context_when_pipeline_does_not_need_it():
    game = Game.__new__(Game)
    game.duck = object()
    game.conversation = _FakeConversation(needs_context=False)
    game._get_memory_context_for_dialogue = lambda: (_ for _ in ()).throw(AssertionError("context built"))

    assert game._generate_talk_response("hello") == "reply:hello"
    assert game.conversation.received_context == ""


def test_generate_talk_response_builds_context_for_direct_llm_pipeline():
    game = Game.__new__(Game)
    game.duck = object()
    game.conversation = _FakeConversation(needs_context=True)
    game._get_memory_context_for_dialogue = lambda: "rich context"

    assert game._generate_talk_response("hello") == "reply:hello"
    assert game.conversation.received_context == "rich context"
