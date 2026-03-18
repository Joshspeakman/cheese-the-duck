"""Tests for dialogue.dialogue_core — DialogueContext, DialogueResponse, DialogueMemory."""
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dialogue.dialogue_core import DialogueContext, DialogueResponse, DialogueMemory, DialogueState


def _make_context(**overrides):
    defaults = dict(
        timestamp=time.time(), player_message="hello",
        conversation_state="active", duck_mood="content", duck_trust=50.0,
        time_of_day="morning", season="spring", weather="sunny",
        current_biome="pond", current_location="pond",
        active_visitor=None, active_event=None,
        recent_topics=[], session_message_count=1,
        triggers=["player_input"],
    )
    defaults.update(overrides)
    return DialogueContext(**defaults)


def _make_response(**overrides):
    defaults = dict(
        text="quack", source="test", confidence=1.0,
        actions=[], mood_hint=None, should_record=True,
    )
    defaults.update(overrides)
    return DialogueResponse(**defaults)


def test_dialogue_context_creation():
    ctx = _make_context()
    assert ctx.player_message == "hello"
    assert ctx.duck_mood == "content"


def test_dialogue_response_creation():
    resp = _make_response()
    assert resp.text == "quack"
    assert resp.source == "test"


def test_memory_record_and_get_recent():
    mem = DialogueMemory()
    ctx = _make_context()
    resp = _make_response()
    mem.record_exchange("hi", "quack", ctx, resp)
    recent = mem.get_recent(5)
    assert len(recent) == 1
    assert recent[0]["player"] == "hi"
    assert recent[0]["duck"] == "quack"


def test_memory_get_topics():
    mem = DialogueMemory()
    ctx = _make_context()
    resp = _make_response()
    mem.record_exchange("tell me about the weather", "it's sunny", ctx, resp)
    topics = mem.get_topics(limit=5)
    assert isinstance(topics, list)


def test_memory_search():
    mem = DialogueMemory()
    ctx = _make_context()
    resp = _make_response()
    mem.record_exchange("banana smoothie", "yum", ctx, resp)
    results = mem.search("banana")
    assert len(results) >= 1


def test_memory_roundtrip():
    mem = DialogueMemory()
    ctx = _make_context()
    resp = _make_response()
    mem.record_exchange("test", "response", ctx, resp)
    data = mem.to_dict()
    mem2 = DialogueMemory.from_dict(data)
    assert len(mem2.get_recent(10)) == len(mem.get_recent(10))


def test_dialogue_state_defaults():
    state = DialogueState()
    assert state.duck_mood == "content"
    assert state.duck_trust == 20.0  # Default trust is 20
