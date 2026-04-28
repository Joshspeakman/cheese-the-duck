"""Tests for dialogue.ambient_lines — AmbientLineGenerator storage, parsing, filtering."""
import sys
import time
import sqlite3
from pathlib import Path
from unittest.mock import MagicMock, patch
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dialogue.ambient_lines import (
    AmbientLineGenerator, VALID_CONTEXTS, _LINE_RE,
)


# ── Helpers ──────────────────────────────────────────────────────────

def _make_gen(tmp_path, cooldown=0, max_stored=100):
    """Create a generator using a temp DB path."""
    with patch("dialogue.ambient_lines.DB_PATH", tmp_path / "test_brain.db"):
        gen = AmbientLineGenerator(llm_chat=None, cooldown=cooldown, max_stored=max_stored)
    return gen


def _insert_lines(gen, lines, source="test"):
    """Directly insert parsed lines into the DB."""
    gen._store_lines(lines, source)


# ── Regex parsing ────────────────────────────────────────────────────

class TestLineRegex:
    def test_simple_match(self):
        m = _LINE_RE.match("greeting: Hello there.")
        assert m
        assert m.group("ctx") == "greeting"
        assert m.group("text") == "Hello there."

    def test_idle_match(self):
        m = _LINE_RE.match("idle: *blinks* I was thinking about bread.")
        assert m
        assert m.group("ctx") == "idle"

    def test_dash_prefix(self):
        m = _LINE_RE.match("- feed: Food received.")
        assert m
        assert m.group("ctx") == "feed"

    def test_numbered_prefix(self):
        m = _LINE_RE.match("1. play: *flaps* That was acceptable.")
        assert m
        assert m.group("ctx") == "play"

    def test_case_insensitive(self):
        m = _LINE_RE.match("GREETING: Oh. You.")
        assert m
        assert m.group("ctx") == "GREETING"

    def test_no_match_invalid_context(self):
        m = _LINE_RE.match("dancing: I groove.")
        assert m is None

    def test_no_match_no_colon(self):
        m = _LINE_RE.match("greeting Hello")
        assert m is None

    def test_callback_context(self):
        m = _LINE_RE.match("callback: You mentioned bread earlier.")
        assert m
        assert m.group("ctx") == "callback"

    def test_clean_context(self):
        m = _LINE_RE.match("clean: *shakes feathers* Tolerable.")
        assert m
        assert m.group("ctx") == "clean"

    def test_pet_context(self):
        m = _LINE_RE.match("pet: *tilts head* Acceptable contact.")
        assert m
        assert m.group("ctx") == "pet"


# ── Valid contexts ───────────────────────────────────────────────────

class TestValidContexts:
    def test_all_expected_contexts_present(self):
        expected = {"greeting", "feed", "play", "pet", "clean", "idle", "callback", "chat_response"}
        assert VALID_CONTEXTS == expected


# ── Parse response ───────────────────────────────────────────────────

class TestParseResponse:
    def test_parses_multiple_lines(self, tmp_path):
        gen = _make_gen(tmp_path)
        raw = (
            "greeting: *blinks* Oh. You again.\n"
            "idle: I was staring at the wall. It stared back.\n"
            "feed: Bread. Noted.\n"
        )
        lines = gen._parse_response(raw)
        assert len(lines) == 3
        assert lines[0] == ("greeting", "*blinks* Oh. You again.")
        assert lines[1] == ("idle", "I was staring at the wall. It stared back.")
        assert lines[2] == ("feed", "Bread. Noted.")

    def test_skips_empty_lines(self, tmp_path):
        gen = _make_gen(tmp_path)
        raw = "\n\ngreeting: Hello.\n\n"
        lines = gen._parse_response(raw)
        assert len(lines) == 1

    def test_skips_too_short(self, tmp_path):
        gen = _make_gen(tmp_path)
        raw = "greeting: Hi\n"  # < 5 chars
        lines = gen._parse_response(raw)
        assert len(lines) == 0

    def test_skips_too_long(self, tmp_path):
        gen = _make_gen(tmp_path)
        raw = f"greeting: {'x' * 201}\n"
        lines = gen._parse_response(raw)
        assert len(lines) == 0

    def test_skips_non_matching_lines(self, tmp_path):
        gen = _make_gen(tmp_path)
        raw = (
            "Here are some lines:\n"
            "greeting: *blinks* Hello there.\n"
            "This is just filler text.\n"
        )
        lines = gen._parse_response(raw)
        assert len(lines) == 1
        assert lines[0][0] == "greeting"

    def test_empty_input(self, tmp_path):
        gen = _make_gen(tmp_path)
        assert gen._parse_response("") == []

    def test_whitespace_only(self, tmp_path):
        gen = _make_gen(tmp_path)
        assert gen._parse_response("   \n  \n") == []


# ── Store and consume ────────────────────────────────────────────────

class TestStoreAndConsume:
    def test_store_and_consume_single_line(self, tmp_path):
        gen = _make_gen(tmp_path)
        _insert_lines(gen, [("greeting", "Hello there.")], source="test")
        result = gen.consume_line("greeting")
        assert result == "Hello there."

    def test_consume_returns_none_when_empty(self, tmp_path):
        gen = _make_gen(tmp_path)
        assert gen.consume_line("greeting") is None

    def test_consume_marks_as_used(self, tmp_path):
        gen = _make_gen(tmp_path)
        _insert_lines(gen, [("idle", "Thinking about nothing.")])
        gen.consume_line("idle")
        # Second consume should get None (marked as used)
        assert gen.consume_line("idle") is None

    def test_consume_respects_context(self, tmp_path):
        gen = _make_gen(tmp_path)
        _insert_lines(gen, [
            ("greeting", "Hello."),
            ("idle", "Staring at wall."),
        ])
        result = gen.consume_line("idle")
        assert result == "Staring at wall."
        # Greeting still available
        result2 = gen.consume_line("greeting")
        assert result2 == "Hello."

    def test_consume_fifo_order(self, tmp_path):
        gen = _make_gen(tmp_path)
        _insert_lines(gen, [
            ("idle", "First thought."),
            ("idle", "Second thought."),
            ("idle", "Third thought."),
        ])
        assert gen.consume_line("idle") == "First thought."
        assert gen.consume_line("idle") == "Second thought."
        assert gen.consume_line("idle") == "Third thought."
        assert gen.consume_line("idle") is None

    def test_store_with_source_trigger(self, tmp_path):
        gen = _make_gen(tmp_path)
        _insert_lines(gen, [("greeting", "Hi.")], source="chat:my name is Josh")
        row = gen._conn.execute(
            "SELECT source_trigger FROM ambient_lines WHERE context='greeting'"
        ).fetchone()
        assert row[0] == "chat:my name is Josh"


# ── Count unused ─────────────────────────────────────────────────────

class TestCountUnused:
    def test_count_all_unused(self, tmp_path):
        gen = _make_gen(tmp_path)
        _insert_lines(gen, [
            ("greeting", "Hello."),
            ("idle", "Thinking."),
            ("feed", "Food noted."),
        ])
        assert gen.count_unused() == 3

    def test_count_by_context(self, tmp_path):
        gen = _make_gen(tmp_path)
        _insert_lines(gen, [
            ("greeting", "Hello."),
            ("greeting", "Oh. You."),
            ("idle", "Thinking."),
        ])
        assert gen.count_unused("greeting") == 2
        assert gen.count_unused("idle") == 1
        assert gen.count_unused("feed") == 0

    def test_count_decreases_after_consume(self, tmp_path):
        gen = _make_gen(tmp_path)
        _insert_lines(gen, [
            ("idle", "One."),
            ("idle", "Two."),
        ])
        assert gen.count_unused("idle") == 2
        gen.consume_line("idle")
        assert gen.count_unused("idle") == 1


# ── Pruning ──────────────────────────────────────────────────────────

class TestPruning:
    def test_prune_caps_at_max_stored(self, tmp_path):
        gen = _make_gen(tmp_path, max_stored=3)
        _insert_lines(gen, [
            ("idle", "Line one."),
            ("idle", "Line two."),
            ("idle", "Line three."),
            ("idle", "Line four."),
            ("idle", "Line five."),
        ])
        # Should have pruned to 3
        assert gen.count_unused() == 3
        # Oldest should be gone; first remaining should be "Line three."
        result = gen.consume_line("idle")
        assert result == "Line three."

    def test_prune_removes_old_used_lines(self, tmp_path):
        gen = _make_gen(tmp_path)
        _insert_lines(gen, [("idle", "Used line.")])
        gen.consume_line("idle")
        # Manually set created_at to 2 hours ago
        gen._conn.execute(
            "UPDATE ambient_lines SET created_at = ?",
            (time.time() - 7200,),
        )
        gen._conn.commit()
        # Prune should remove the old used line
        gen._prune()
        total = gen._conn.execute("SELECT COUNT(*) FROM ambient_lines").fetchone()[0]
        assert total == 0


# ── Filter lines ─────────────────────────────────────────────────────

class TestFilterLines:
    def test_safe_lines_pass_through(self, tmp_path):
        gen = _make_gen(tmp_path)
        lines = [("greeting", "Hello there."), ("idle", "Bread is good.")]
        result = gen._filter_lines(lines)
        assert len(result) == 2

    def test_unsafe_lines_removed(self, tmp_path):
        gen = _make_gen(tmp_path)
        lines = [
            ("greeting", "Hello there."),
            ("idle", "what the fuck"),
        ]
        result = gen._filter_lines(lines)
        assert len(result) == 1
        assert result[0][0] == "greeting"


# ── Pick contexts ───────────────────────────────────────────────────

class TestPickContexts:
    def test_chat_trigger(self, tmp_path):
        gen = _make_gen(tmp_path)
        ctxs = gen._pick_contexts("chat")
        assert "greeting" in ctxs
        assert "idle" in ctxs
        assert "callback" in ctxs

    def test_feed_trigger(self, tmp_path):
        gen = _make_gen(tmp_path)
        ctxs = gen._pick_contexts("feed")
        assert "feed" in ctxs
        assert "idle" in ctxs

    def test_play_trigger(self, tmp_path):
        gen = _make_gen(tmp_path)
        ctxs = gen._pick_contexts("play")
        assert "play" in ctxs

    def test_login_trigger(self, tmp_path):
        gen = _make_gen(tmp_path)
        ctxs = gen._pick_contexts("login")
        assert "greeting" in ctxs
        assert "idle" in ctxs

    def test_unknown_trigger_defaults_to_idle(self, tmp_path):
        gen = _make_gen(tmp_path)
        ctxs = gen._pick_contexts("unknown")
        assert ctxs == ["idle"]


# ── Build prompt ─────────────────────────────────────────────────────

class TestBuildPrompt:
    def test_prompt_contains_system_section(self, tmp_path):
        gen = _make_gen(tmp_path)
        prompt = gen._build_prompt(
            "chat", "hello", "Hi.", "Josh", "content", "", "",
            ["greeting", "idle"],
        )
        assert "[SYSTEM]" in prompt
        assert "[USER]" in prompt
        assert "Cheese" in prompt

    def test_prompt_includes_player_name(self, tmp_path):
        gen = _make_gen(tmp_path)
        prompt = gen._build_prompt(
            "chat", "hi", "Hello.", "Josh", "content", "", "",
            ["greeting"],
        )
        assert "Josh" in prompt

    def test_prompt_includes_player_input(self, tmp_path):
        gen = _make_gen(tmp_path)
        prompt = gen._build_prompt(
            "chat", "my name is Josh", "Noted.", "", "content", "", "",
            ["greeting"],
        )
        assert "my name is Josh" in prompt

    def test_prompt_includes_context_types(self, tmp_path):
        gen = _make_gen(tmp_path)
        prompt = gen._build_prompt(
            "chat", "", "", "", "content", "", "",
            ["feed", "idle"],
        )
        assert "feed:" in prompt
        assert "idle:" in prompt

    def test_prompt_includes_location(self, tmp_path):
        gen = _make_gen(tmp_path)
        prompt = gen._build_prompt(
            "chat", "", "", "", "content", "the pond", "",
            ["idle"],
        )
        assert "the pond" in prompt

    def test_prompt_includes_weather(self, tmp_path):
        gen = _make_gen(tmp_path)
        prompt = gen._build_prompt(
            "chat", "", "", "", "content", "", "rainy",
            ["idle"],
        )
        assert "rainy" in prompt

    def test_action_trigger_description(self, tmp_path):
        gen = _make_gen(tmp_path)
        prompt = gen._build_prompt(
            "feed", "", "", "", "content", "", "",
            ["feed"],
        )
        assert "feed" in prompt.lower()


# ── Request gating ───────────────────────────────────────────────────

class TestRequestGating:
    def test_default_cooldown_starts_in_cooldown(self, tmp_path):
        with patch("dialogue.ambient_lines.DB_PATH", tmp_path / "test_brain.db"):
            gen = AmbientLineGenerator(llm_chat=None, cooldown=120)
        try:
            assert time.time() - gen._last_generation_time < 1
        finally:
            gen.shutdown()

    def test_no_llm_drops_request(self, tmp_path):
        gen = _make_gen(tmp_path)
        gen._llm_chat = None
        gen.request_lines("chat", "hello", "hi")
        assert not gen._busy

    def test_busy_drops_request(self, tmp_path):
        gen = _make_gen(tmp_path, cooldown=0)
        gen._llm_chat = MagicMock()
        gen._llm_chat.is_available.return_value = True
        gen._busy = True
        gen.request_lines("chat", "hello", "hi")
        # Still busy (didn't re-submit)
        assert gen._busy

    def test_cooldown_drops_request(self, tmp_path):
        gen = _make_gen(tmp_path, cooldown=9999)
        gen._llm_chat = MagicMock()
        gen._llm_chat.is_available.return_value = True
        gen._last_generation_time = time.time()
        gen.request_lines("chat", "hello", "hi")
        assert not gen._busy

    def test_llm_unavailable_drops_request(self, tmp_path):
        gen = _make_gen(tmp_path, cooldown=0)
        gen._llm_chat = MagicMock()
        gen._llm_chat.is_available.return_value = False
        gen.request_lines("chat", "hello", "hi")
        assert not gen._busy


# ── Shutdown ─────────────────────────────────────────────────────────

class TestShutdown:
    def test_shutdown_does_not_raise(self, tmp_path):
        gen = _make_gen(tmp_path)
        gen.shutdown()

    def test_consume_after_shutdown_returns_none(self, tmp_path):
        gen = _make_gen(tmp_path)
        _insert_lines(gen, [("idle", "Still here.")])
        gen.shutdown()
        # Connection closed, should handle gracefully
        # (may return None or raise — we just confirm no crash)
        try:
            gen.consume_line("idle")
        except Exception:
            pass


# ── DB initialisation ────────────────────────────────────────────────

class TestDbInit:
    def test_creates_table(self, tmp_path):
        gen = _make_gen(tmp_path)
        # Check table exists
        row = gen._conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='ambient_lines'"
        ).fetchone()
        assert row is not None

    def test_db_has_correct_columns(self, tmp_path):
        gen = _make_gen(tmp_path)
        cursor = gen._conn.execute("PRAGMA table_info(ambient_lines)")
        columns = {row[1] for row in cursor.fetchall()}
        assert columns == {"id", "context", "text", "created_at", "used", "source_trigger", "topics"}
