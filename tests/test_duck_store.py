"""
Comprehensive tests for core.duck_store.DuckStore.

Covers need management, trust, derived state (mood/motivation),
sickness/hiding, validation, audit logging, and persistence.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import pytest

# Ensure project root is on sys.path.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from core.duck_store import DuckState, DuckStore, StateChange, NEED_NAMES


# ═══════════════════════════════════════════════════════════════════════════
# Need management
# ═══════════════════════════════════════════════════════════════════════════

class TestNeedManagement:
    """Tests for get/set/change need operations."""

    def test_set_need_valid(self, duck_store: DuckStore) -> None:
        """Setting a valid need value stores it correctly."""
        duck_store.set_need("hunger", 75.0, reason="test")
        assert duck_store.get_need("hunger") == 75.0

    def test_set_need_clamps_to_bounds(self, duck_store: DuckStore) -> None:
        """Values outside 0-100 are silently clamped."""
        duck_store.set_need("hunger", 150.0, reason="over max")
        assert duck_store.get_need("hunger") == 100.0

        duck_store.set_need("energy", -20.0, reason="below min")
        assert duck_store.get_need("energy") == 0.0

    def test_change_need_relative(self, duck_store: DuckStore) -> None:
        """Delta changes are applied relative to current value."""
        duck_store.set_need("fun", 40.0, reason="baseline")
        duck_store.change_need("fun", 25.0, reason="played")
        assert duck_store.get_need("fun") == 65.0

        duck_store.change_need("fun", -10.0, reason="bored")
        assert duck_store.get_need("fun") == 55.0

    def test_change_need_clamps(self, duck_store: DuckStore) -> None:
        """Delta changes that exceed bounds are clamped."""
        duck_store.set_need("cleanliness", 90.0)
        duck_store.change_need("cleanliness", 50.0)
        assert duck_store.get_need("cleanliness") == 100.0

        duck_store.set_need("social", 5.0)
        duck_store.change_need("social", -20.0)
        assert duck_store.get_need("social") == 0.0

    def test_get_critical_needs(self, duck_store: DuckStore) -> None:
        """Needs below the threshold are reported as critical."""
        duck_store.set_need("hunger", 15.0, reason="starving")
        duck_store.set_need("energy", 10.0, reason="exhausted")
        duck_store.set_need("fun", 50.0, reason="fine")

        critical = duck_store.get_critical_needs(threshold=20.0)
        assert "hunger" in critical
        assert "energy" in critical
        assert "fun" not in critical

    def test_get_critical_needs_custom_threshold(self, duck_store: DuckStore) -> None:
        """Custom threshold is respected."""
        duck_store.set_need("hunger", 35.0)
        assert "hunger" not in duck_store.get_critical_needs(threshold=20.0)
        assert "hunger" in duck_store.get_critical_needs(threshold=40.0)

    def test_get_all_needs(self, duck_store: DuckStore) -> None:
        """get_all_needs returns a copy of all five needs."""
        needs = duck_store.get_all_needs()
        assert set(needs.keys()) == set(NEED_NAMES)
        # Mutating the returned dict does not affect the store.
        needs["hunger"] = 999.0
        assert duck_store.get_need("hunger") != 999.0

    def test_set_unknown_need_is_noop(self, duck_store: DuckStore) -> None:
        """Setting an unknown need name does nothing (no crash)."""
        duck_store.set_need("nonexistent", 50.0)
        assert duck_store.get_need("nonexistent") == 0.0

    def test_need_change_records_audit(self, duck_store: DuckStore) -> None:
        """Every need change creates an audit log entry."""
        duck_store.set_need("hunger", 80.0, reason="fed")
        changes = duck_store.get_changes_for("need.hunger")
        assert len(changes) >= 1
        last = changes[-1]
        assert last.field == "need.hunger"
        assert last.new_value == 80.0
        assert last.reason == "fed"


# ═══════════════════════════════════════════════════════════════════════════
# Trust management
# ═══════════════════════════════════════════════════════════════════════════

class TestTrustManagement:
    """Tests for trust get/change operations."""

    def test_trust_change(self, duck_store: DuckStore) -> None:
        """Basic trust change works."""
        initial = duck_store.get_trust()
        duck_store.change_trust(5.0, reason="petted")
        assert duck_store.get_trust() == initial + 5.0

    def test_trust_clamps(self, duck_store: DuckStore) -> None:
        """Trust is clamped to 0-100."""
        duck_store.change_trust(200.0, reason="absurd")
        assert duck_store.get_trust() == 100.0

        duck_store.change_trust(-300.0, reason="also absurd")
        assert duck_store.get_trust() == 0.0

    def test_trust_change_audit(self, duck_store: DuckStore) -> None:
        """Trust changes are recorded in the audit log."""
        duck_store.change_trust(3.0, reason="good care")
        changes = duck_store.get_changes_for("trust")
        assert len(changes) >= 1
        last = changes[-1]
        assert last.field == "trust"
        assert last.reason == "good care"

    def test_trust_no_change_no_audit(self, duck_store: DuckStore) -> None:
        """A zero-delta trust change does not produce an audit entry."""
        before_count = len(duck_store.get_changes_for("trust"))
        duck_store.change_trust(0.0, reason="nothing happened")
        after_count = len(duck_store.get_changes_for("trust"))
        assert after_count == before_count


# ═══════════════════════════════════════════════════════════════════════════
# Derived state (mood, motivation)
# ═══════════════════════════════════════════════════════════════════════════

class TestDerivedState:
    """Tests for mood and motivation recalculation."""

    def test_mood_recalculated_on_need_change(self, duck_store: DuckStore) -> None:
        """Mood updates when needs change significantly."""
        # Set all needs high -> should produce a happy/ecstatic mood.
        for need in NEED_NAMES:
            duck_store.set_need(need, 95.0, reason="max out")
        mood_high = duck_store.get_mood_score()

        # Set all needs low -> mood score should drop.
        for need in NEED_NAMES:
            duck_store.set_need(need, 5.0, reason="neglect")
        mood_low = duck_store.get_mood_score()

        assert mood_low < mood_high

    def test_motivation_derived_from_mood(self, duck_store: DuckStore) -> None:
        """Motivation changes when mood changes."""
        for need in NEED_NAMES:
            duck_store.set_need(need, 80.0, reason="happy")
        motivation_high = duck_store.get_motivation()

        for need in NEED_NAMES:
            duck_store.set_need(need, 0.0, reason="neglect")
        motivation_low = duck_store.get_motivation()

        # With all needs at 0 the duck is miserable → very low motivation.
        assert motivation_low <= motivation_high
        # At least one end should be meaningfully different.
        assert motivation_high > 0.0 or motivation_low < 1.0

    def test_mood_is_string(self, duck_store: DuckStore) -> None:
        """get_mood() always returns a string."""
        assert isinstance(duck_store.get_mood(), str)

    def test_motivation_bounds(self, duck_store: DuckStore) -> None:
        """Motivation is always between 0.0 and 1.0."""
        for need in NEED_NAMES:
            duck_store.set_need(need, 0.0)
        assert 0.0 <= duck_store.get_motivation() <= 1.0

        for need in NEED_NAMES:
            duck_store.set_need(need, 100.0)
        assert 0.0 <= duck_store.get_motivation() <= 1.0


# ═══════════════════════════════════════════════════════════════════════════
# Sickness / hiding
# ═══════════════════════════════════════════════════════════════════════════

class TestSicknessHiding:
    """Tests for sickness and hiding status."""

    def test_set_sick(self, duck_store: DuckStore) -> None:
        """Setting sick=True records the state and timestamp."""
        duck_store.set_sick(True, cause="prolonged neglect")
        assert duck_store.is_sick is True
        state = duck_store.get_state()
        assert state.is_sick is True
        assert state.sick_since is not None

    def test_clear_sick(self, duck_store: DuckStore) -> None:
        """Setting sick=False clears the state and timestamp."""
        duck_store.set_sick(True, cause="test")
        duck_store.set_sick(False, cause="medicine")
        assert duck_store.is_sick is False
        state = duck_store.get_state()
        assert state.sick_since is None

    def test_set_hiding(self, duck_store: DuckStore) -> None:
        """Setting hiding=True records the state and resets coax visits."""
        duck_store.set_hiding(True)
        assert duck_store.is_hiding is True
        state = duck_store.get_state()
        assert state.is_hiding is True
        assert state.hiding_coax_visits == 0

    def test_clear_hiding(self, duck_store: DuckStore) -> None:
        """Setting hiding=False clears the state."""
        duck_store.set_hiding(True)
        duck_store.set_hiding(False)
        assert duck_store.is_hiding is False

    def test_sickness_affects_motivation(self, duck_store: DuckStore) -> None:
        """Sickness should reduce motivation."""
        for need in NEED_NAMES:
            duck_store.set_need(need, 80.0)
        motivation_healthy = duck_store.get_motivation()

        duck_store.set_sick(True, cause="test")
        motivation_sick = duck_store.get_motivation()

        assert motivation_sick < motivation_healthy


# ═══════════════════════════════════════════════════════════════════════════
# Validation
# ═══════════════════════════════════════════════════════════════════════════

class TestValidation:
    """Tests for state validation."""

    def test_validate_clean_state(self, duck_store: DuckStore) -> None:
        """A freshly created store has no validation errors."""
        errors = duck_store.validate()
        assert errors == []

    def test_validate_catches_out_of_bounds(self) -> None:
        """Deliberately corrupted state is caught by validate().

        Note: We bypass the setters to inject invalid values, since the
        setters clamp automatically.
        """
        store = DuckStore()
        # Manually corrupt internal state.
        store._needs["hunger"] = -5.0
        store._trust = 150.0

        errors = store.validate()
        assert any("hunger" in e for e in errors)
        assert any("Trust" in e or "trust" in e.lower() for e in errors)

    def test_validate_invalid_growth_stage(self) -> None:
        """An unrecognized growth stage is flagged."""
        store = DuckStore()
        store._growth_stage = "mega_duck"
        errors = store.validate()
        assert any("growth stage" in e.lower() for e in errors)


# ═══════════════════════════════════════════════════════════════════════════
# Audit log
# ═══════════════════════════════════════════════════════════════════════════

class TestAuditLog:
    """Tests for the audit log circular buffer."""

    def test_recent_changes_limit(self, duck_store: DuckStore) -> None:
        """get_recent_changes respects the limit parameter."""
        for i in range(10):
            duck_store.set_need("hunger", float(i * 10), reason=f"step {i}")
        changes = duck_store.get_recent_changes(limit=3)
        assert len(changes) <= 3

    def test_audit_log_circular_buffer(self) -> None:
        """Audit log does not grow beyond _MAX_AUDIT_LOG entries."""
        from core.duck_store import _MAX_AUDIT_LOG

        store = DuckStore()
        # Generate more than _MAX_AUDIT_LOG changes.
        for i in range(_MAX_AUDIT_LOG + 100):
            val = float(i % 100)
            store.set_need("hunger", val, reason=f"iter {i}")

        # The internal deque enforces the limit.
        assert len(store._audit_log) <= _MAX_AUDIT_LOG

    def test_get_changes_for_filters(self, duck_store: DuckStore) -> None:
        """get_changes_for only returns changes matching the field."""
        duck_store.set_need("hunger", 70.0, reason="fed")
        duck_store.set_need("energy", 80.0, reason="slept")
        duck_store.change_trust(5.0, reason="petted")

        hunger_changes = duck_store.get_changes_for("need.hunger")
        for change in hunger_changes:
            assert change.field == "need.hunger"


# ═══════════════════════════════════════════════════════════════════════════
# Persistence
# ═══════════════════════════════════════════════════════════════════════════

class TestPersistence:
    """Tests for to_dict / from_dict and Duck sync."""

    def test_to_dict_from_dict_roundtrip(self, duck_store: DuckStore) -> None:
        """Serialize -> deserialize preserves all state."""
        duck_store.set_need("hunger", 73.0, reason="test")
        duck_store.set_need("energy", 88.0, reason="test")
        duck_store.change_trust(15.0, reason="test")
        duck_store.set_sick(True, cause="test sickness")

        data = duck_store.to_dict()

        restored = DuckStore()
        restored.from_dict(data)

        assert restored.get_need("hunger") == pytest.approx(73.0, abs=0.2)
        assert restored.get_need("energy") == pytest.approx(88.0, abs=0.2)
        assert restored.get_trust() == pytest.approx(duck_store.get_trust(), abs=0.1)
        assert restored.is_sick is True

    def test_from_dict_with_missing_fields(self) -> None:
        """Missing fields in the dict are filled with defaults."""
        store = DuckStore()
        store.from_dict({"name": "TestDuck"})

        assert store._name == "TestDuck"
        # Needs should fall back to 50.0 default.
        assert store.get_need("hunger") == 50.0
        assert store.get_trust() == 20.0
        assert store.is_sick is False

    def test_from_dict_with_empty_dict(self) -> None:
        """An empty dict produces a valid default state."""
        store = DuckStore()
        store.from_dict({})
        errors = store.validate()
        assert errors == []

    def test_sync_from_duck(self, sample_duck) -> None:
        """sync_from_duck pulls state from a real Duck object."""
        store = DuckStore()
        store.sync_from_duck(sample_duck)

        assert store._name == sample_duck.name
        assert store.get_need("hunger") == pytest.approx(
            sample_duck.needs.hunger, abs=0.1
        )
        assert store.get_trust() == pytest.approx(sample_duck.trust, abs=0.1)

    def test_sync_to_duck(self, sample_duck) -> None:
        """sync_to_duck pushes store state back to a Duck object."""
        store = DuckStore()
        store.sync_from_duck(sample_duck)

        # Modify state in the store.
        store.set_need("hunger", 99.0, reason="gorged")
        store.change_trust(10.0, reason="bonding")

        # Push back.
        store.sync_to_duck(sample_duck)

        assert sample_duck.needs.hunger == pytest.approx(99.0, abs=0.1)
        assert sample_duck.trust == pytest.approx(store.get_trust(), abs=0.1)

    def test_sync_roundtrip(self, sample_duck) -> None:
        """sync_from -> mutate -> sync_to -> sync_from preserves changes."""
        store = DuckStore()
        store.sync_from_duck(sample_duck)

        store.set_need("fun", 12.0, reason="bored")
        store.sync_to_duck(sample_duck)

        # Create a fresh store and sync from the updated duck.
        store2 = DuckStore()
        store2.sync_from_duck(sample_duck)
        assert store2.get_need("fun") == pytest.approx(12.0, abs=0.1)


# ═══════════════════════════════════════════════════════════════════════════
# State snapshot
# ═══════════════════════════════════════════════════════════════════════════

class TestGetState:
    """Tests for the get_state() snapshot method."""

    def test_get_state_returns_duck_state(self, duck_store: DuckStore) -> None:
        """get_state returns a DuckState dataclass."""
        state = duck_store.get_state()
        assert isinstance(state, DuckState)

    def test_get_state_reflects_changes(self, duck_store: DuckStore) -> None:
        """get_state reflects mutations made through setters."""
        duck_store.set_need("hunger", 77.0, reason="fed")
        duck_store.set_sick(True, cause="test")
        state = duck_store.get_state()
        assert state.needs["hunger"] == 77.0
        assert state.is_sick is True
