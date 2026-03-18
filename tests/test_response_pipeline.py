"""Tests for dialogue.response_pipeline — ResponsePipeline and ResponseSource."""
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dialogue.dialogue_core import DialogueContext, DialogueResponse, DialogueState
from dialogue.response_pipeline import ResponsePipeline, ResponseSource


def _make_context():
    return DialogueContext(
        timestamp=time.time(), player_message="hello",
        conversation_state="active", duck_mood="content", duck_trust=50.0,
        time_of_day="morning", season="spring", weather="sunny",
        current_biome="pond", current_location="pond",
        active_visitor=None, active_event=None,
        recent_topics=[], session_message_count=1,
        triggers=["player_input"],
    )


class AlwaysSource(ResponseSource):
    @property
    def name(self): return "always"
    def can_handle(self, context, state): return True
    def generate(self, context, state):
        return DialogueResponse(text="always", source="always", confidence=1.0,
                                actions=[], mood_hint=None, should_record=True)
    def is_enabled(self): return True


class NeverSource(ResponseSource):
    @property
    def name(self): return "never"
    def can_handle(self, context, state): return True
    def generate(self, context, state): return None
    def is_enabled(self): return True


class BrokenSource(ResponseSource):
    @property
    def name(self): return "broken"
    def can_handle(self, context, state): return True
    def generate(self, context, state): raise RuntimeError("boom")
    def is_enabled(self): return True


def test_empty_pipeline_returns_fallback():
    pipe = ResponsePipeline()
    ctx = _make_context()
    resp = pipe.generate_response(ctx, DialogueState())
    assert resp is not None
    assert resp.text  # Should have fallback text


def test_pipeline_uses_first_successful_source():
    pipe = ResponsePipeline()
    pipe.register_source(AlwaysSource(), priority=10)
    ctx = _make_context()
    resp = pipe.generate_response(ctx, DialogueState())
    assert resp.text == "always"


def test_none_source_skipped():
    pipe = ResponsePipeline()
    pipe.register_source(NeverSource(), priority=10)
    pipe.register_source(AlwaysSource(), priority=20)
    ctx = _make_context()
    resp = pipe.generate_response(ctx, DialogueState())
    assert resp.text == "always"


def test_broken_source_skipped():
    pipe = ResponsePipeline()
    pipe.register_source(BrokenSource(), priority=10)
    pipe.register_source(AlwaysSource(), priority=20)
    ctx = _make_context()
    resp = pipe.generate_response(ctx, DialogueState())
    assert resp.text == "always"


def test_priority_ordering():
    order = []
    class TrackingSource(ResponseSource):
        def __init__(self, src_name):
            self._name = src_name
        @property
        def name(self): return self._name
        def can_handle(self, context, state): return True
        def generate(self, context, state):
            order.append(self._name)
            return None
        def is_enabled(self): return True

    pipe = ResponsePipeline()
    pipe.register_source(TrackingSource("low"), priority=50)
    pipe.register_source(TrackingSource("high"), priority=10)
    pipe.generate_response(_make_context(), DialogueState())
    assert order[0] == "high"  # Lower priority number = tried first
