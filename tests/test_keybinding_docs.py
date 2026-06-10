"""Guard against drift between documented keys and actual handlers.

KEY_REFERENCE in ui/input_handler.py is the single source of truth for the
in-game help. Most keys are handled directly in core/game.py's key handler;
this test scans that source so a documented key can't silently lose its
handler (e.g. the old '=' diary key that was shadowed by volume-up).
"""

from pathlib import Path

from ui.input_handler import KEY_REFERENCE, KEY_BINDINGS, get_help_text

GAME_SRC = (Path(__file__).parent.parent / "core" / "game.py").read_text()


def _documented_single_keys():
    """Yield (key, label) for entries that are a single dispatchable key."""
    for _section, keys in KEY_REFERENCE:
        for key, label in keys:
            if len(key) == 1:
                yield key, label


def test_documented_keys_have_handlers():
    for key, label in _documented_single_keys():
        lowered = key.lower()
        in_bindings = key in KEY_BINDINGS or lowered in KEY_BINDINGS
        # game.py compares against lowercase key_str with either quote style;
        # the backslash key appears escaped in source ('\\')
        candidates = [lowered, key, lowered.replace("\\", "\\\\"), key.replace("\\", "\\\\")]
        handled = any(
            f"key_str == '{c}'" in GAME_SRC or f'key_str == "{c}"' in GAME_SRC
            for c in candidates
        ) or (f"'{lowered}'" in GAME_SRC and "key_str in" in GAME_SRC)  # list-style checks
        assert in_bindings or handled, (
            f"Help documents [{key}] {label} but no handler was found in "
            f"KEY_BINDINGS or core/game.py"
        )


def test_diary_key_not_shadowed_by_volume():
    """'=' must reach the diary handler; volume-up may only claim '+'."""
    assert "key_str in ['+', '=']" not in GAME_SRC
    assert "key_str == '='" in GAME_SRC


def test_help_text_generated_from_reference():
    help_text = get_help_text()
    for section, keys in KEY_REFERENCE:
        assert section in help_text
        for key, label in keys:
            assert label in help_text
