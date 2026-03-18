"""
Centralized state management for the duck entity.

DuckStore wraps the existing Duck object and provides:
- Validated get/set for all duck state fields
- Automatic clamping (never crash, always clamp)
- Derived-state caching (mood, motivation)
- Circular audit log of all state changes
- Serialization/deserialization with validation
- Event emission via the EventBus on state changes

DuckStore does NOT replace the Duck dataclass — it wraps it.
Use ``sync_from_duck`` / ``sync_to_duck`` to bridge the two.
"""
from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Deque, Dict, List, Optional, TYPE_CHECKING

from config import GROWTH_STAGES, NEED_MAX, NEED_MIN

if TYPE_CHECKING:
    from duck.duck import Duck

# Maximum number of audit log entries retained.
_MAX_AUDIT_LOG: int = 500

# Canonical need names.
NEED_NAMES: List[str] = ["hunger", "energy", "fun", "cleanliness", "social"]

# Valid growth stage identifiers (drawn from config.py).
VALID_GROWTH_STAGES: set = set(GROWTH_STAGES.keys())


# ── Data Classes ─────────────────────────────────────────────────────────────

@dataclass
class DuckState:
    """Immutable snapshot of all duck state in one place.

    This is a *read-only* view — mutating fields here does NOT affect the
    store.  Use the setter methods on ``DuckStore`` instead.
    """

    name: str = "Cheese"
    created_at: float = 0.0
    growth_stage: str = "hatchling"
    growth_progress: float = 0.0
    needs: Dict[str, float] = field(default_factory=lambda: {
        "hunger": 50.0,
        "energy": 50.0,
        "fun": 50.0,
        "cleanliness": 50.0,
        "social": 50.0,
    })
    trust: float = 50.0
    personality: Dict[str, float] = field(default_factory=dict)
    mood: str = "content"
    mood_score: float = 50.0
    motivation: float = 0.5
    is_sick: bool = False
    sick_since: Optional[float] = None
    is_hiding: bool = False
    hiding_coax_visits: int = 0
    cooldown_until: Optional[float] = None
    current_action: Optional[str] = None
    action_start_time: Optional[float] = None


@dataclass
class StateChange:
    """Audit record for a single state mutation."""

    timestamp: float
    field: str
    old_value: Any
    new_value: Any
    reason: str
    source: str  # "decay", "player_action", "consequence", "event", etc.


# ── DuckStore ────────────────────────────────────────────────────────────────

class DuckStore:
    """Centralized, validated state store for a single duck entity.

    Parameters
    ----------
    duck : Duck, optional
        If provided, the store is initialised by pulling state from this
        existing Duck object via ``sync_from_duck``.
    """

    def __init__(self, duck: Optional["Duck"] = None) -> None:
        # ── Internal state ───────────────────────────────────────────
        self._name: str = "Cheese"
        self._created_at: float = 0.0
        self._growth_stage: str = "hatchling"
        self._growth_progress: float = 0.0
        self._needs: Dict[str, float] = {
            "hunger": 50.0,
            "energy": 50.0,
            "fun": 50.0,
            "cleanliness": 50.0,
            "social": 50.0,
        }
        self._trust: float = 20.0
        self._personality: Dict[str, float] = {}
        self._is_sick: bool = False
        self._sick_since: Optional[float] = None
        self._is_hiding: bool = False
        self._hiding_coax_visits: int = 0
        self._cooldown_until: Optional[float] = None
        self._current_action: Optional[str] = None
        self._action_start_time: Optional[float] = None

        # ── Cached derived state ─────────────────────────────────────
        self._mood: str = "content"
        self._mood_score: float = 50.0
        self._motivation: float = 0.5
        self._mood_dirty: bool = True
        self._motivation_dirty: bool = True

        # ── Audit log (circular buffer) ──────────────────────────────
        self._audit_log: Deque[StateChange] = deque(maxlen=_MAX_AUDIT_LOG)

        # ── Event bus reference (lazy import to avoid circular deps) ─
        self._event_bus = None

        # ── Initialise from existing Duck if provided ────────────────
        if duck is not None:
            self.sync_from_duck(duck)

    # ── Event bus accessor ───────────────────────────────────────────────

    def _get_event_bus(self):
        """Lazily import and cache the event bus singleton."""
        if self._event_bus is None:
            try:
                from core.event_bus import event_bus
                self._event_bus = event_bus
            except ImportError:
                self._event_bus = None
        return self._event_bus

    # ── State snapshot ───────────────────────────────────────────────────

    def get_state(self) -> DuckState:
        """Return a read-only snapshot of the full duck state."""
        return DuckState(
            name=self._name,
            created_at=self._created_at,
            growth_stage=self._growth_stage,
            growth_progress=self._growth_progress,
            needs=dict(self._needs),
            trust=self._trust,
            personality=dict(self._personality),
            mood=self.get_mood(),
            mood_score=self.get_mood_score(),
            motivation=self.get_motivation(),
            is_sick=self._is_sick,
            sick_since=self._sick_since,
            is_hiding=self._is_hiding,
            hiding_coax_visits=self._hiding_coax_visits,
            cooldown_until=self._cooldown_until,
            current_action=self._current_action,
            action_start_time=self._action_start_time,
        )

    # ── Need management ──────────────────────────────────────────────────

    def get_need(self, need: str) -> float:
        """Get the current value of a single need.

        Parameters
        ----------
        need : str
            One of ``"hunger"``, ``"energy"``, ``"fun"``,
            ``"cleanliness"``, ``"social"``.

        Returns
        -------
        float
            The need value (0-100), or 0.0 if the need name is unknown.
        """
        return self._needs.get(need, 0.0)

    def set_need(self, need: str, value: float, reason: str = "") -> None:
        """Set a need to an absolute value (clamped to 0-100).

        Parameters
        ----------
        need : str
            Need name.
        value : float
            Desired value (will be clamped).
        reason : str, optional
            Human-readable reason for the change.
        """
        if need not in self._needs:
            return
        old = self._needs[need]
        new = self._validate_need(need, value)
        if old == new:
            return
        self._needs[need] = new
        self._record_change(f"need.{need}", old, new, reason, "player_action")
        self._emit_need_event(need, old, new, reason)
        self._mood_dirty = True

    def change_need(self, need: str, delta: float, reason: str = "") -> None:
        """Change a need by a relative amount (clamped to 0-100).

        Parameters
        ----------
        need : str
            Need name.
        delta : float
            Amount to add (positive) or subtract (negative).
        reason : str, optional
            Human-readable reason.
        """
        if need not in self._needs:
            return
        self.set_need(need, self._needs[need] + delta, reason)

    def get_all_needs(self) -> Dict[str, float]:
        """Return a copy of all need values."""
        return dict(self._needs)

    def get_critical_needs(self, threshold: float = 20.0) -> List[str]:
        """Return need names whose value is below *threshold*.

        Parameters
        ----------
        threshold : float
            The value below which a need is considered critical.
        """
        return [n for n, v in self._needs.items() if v < threshold]

    # ── Trust management ─────────────────────────────────────────────────

    def get_trust(self) -> float:
        """Return the current trust value (0-100)."""
        return self._trust

    def change_trust(self, delta: float, reason: str = "") -> None:
        """Change trust by *delta* (clamped to 0-100).

        Parameters
        ----------
        delta : float
            Amount to add (positive) or subtract (negative).
        reason : str, optional
            Human-readable reason.
        """
        old = self._trust
        new = self._validate_trust(old + delta)
        if old == new:
            return
        self._trust = new
        self._record_change("trust", old, new, reason, "consequence")
        self._emit_trust_event(old, new, reason)

    # ── Mood (derived, cached) ───────────────────────────────────────────

    def get_mood(self) -> str:
        """Return the current mood label string."""
        if self._mood_dirty:
            self._recalculate_mood()
        return self._mood

    def get_mood_score(self) -> float:
        """Return the current numerical mood score."""
        if self._mood_dirty:
            self._recalculate_mood()
        return self._mood_score

    def _recalculate_mood(self) -> None:
        """Recalculate mood from current needs using MoodCalculator logic.

        Falls back to a simple weighted average if the mood module cannot
        be imported (e.g. during isolated unit tests).
        """
        try:
            from duck.mood import MoodCalculator
            from duck.needs import Needs

            needs_obj = Needs(
                hunger=self._needs.get("hunger", 50.0),
                energy=self._needs.get("energy", 50.0),
                fun=self._needs.get("fun", 50.0),
                cleanliness=self._needs.get("cleanliness", 50.0),
                social=self._needs.get("social", 50.0),
            )
            calc = MoodCalculator()
            mood_info = calc.get_mood(needs_obj)
            old_mood = self._mood
            self._mood = mood_info.state.value
            self._mood_score = mood_info.score
            if old_mood != self._mood:
                self._emit_mood_event(old_mood, self._mood)
                self._motivation_dirty = True
        except ImportError:
            # Fallback: simple weighted average.
            from config import MOOD_WEIGHTS, MOOD_THRESHOLDS

            score = sum(
                self._needs.get(n, 50.0) * w
                for n, w in MOOD_WEIGHTS.items()
            )
            self._mood_score = round(score, 1)
            old_mood = self._mood
            for label in ("ecstatic", "happy", "content", "grumpy", "sad"):
                if score >= MOOD_THRESHOLDS[label]:
                    self._mood = label
                    break
            else:
                self._mood = "miserable"
            if old_mood != self._mood:
                self._motivation_dirty = True

        self._mood_dirty = False

    # ── Motivation (derived, cached) ─────────────────────────────────────

    def get_motivation(self) -> float:
        """Return the current motivation level (0.0-1.0)."""
        if self._motivation_dirty:
            self._recalculate_motivation()
        return self._motivation

    def _recalculate_motivation(self) -> None:
        """Recalculate motivation from mood, needs, and sickness.

        Mirrors the logic in ``DuckDesires.calculate_motivation`` but works
        from store-internal state so that a full Duck object is not required.
        """
        try:
            from duck.desires import MOOD_MOTIVATION_MULT
        except ImportError:
            MOOD_MOTIVATION_MULT = {
                "ecstatic": 1.3, "happy": 1.1, "content": 1.0,
                "grumpy": 0.7, "sad": 0.5, "miserable": 0.2,
                "dramatic": 0.8, "petty": 0.6,
            }

        mood_score = self.get_mood_score()
        mood_label = self.get_mood()
        base = mood_score / 100.0
        mult = MOOD_MOTIVATION_MULT.get(mood_label, 1.0)
        motivation = base * mult

        # Low energy penalty.
        if self._needs.get("energy", 50.0) < 20:
            motivation *= 0.5

        # Sickness penalty.
        if self._is_sick:
            motivation *= 0.3

        self._motivation = max(0.0, min(1.0, motivation))
        self._motivation_dirty = False

    # ── Sickness / hiding ────────────────────────────────────────────────

    def set_sick(self, is_sick: bool, cause: str = "") -> None:
        """Set or clear sickness status.

        Parameters
        ----------
        is_sick : bool
            Whether the duck is now sick.
        cause : str, optional
            Why the duck became sick (or recovered).
        """
        old = self._is_sick
        self._is_sick = is_sick
        if is_sick and not old:
            self._sick_since = time.time()
        elif not is_sick:
            self._sick_since = None
        self._record_change("is_sick", old, is_sick, cause, "consequence")
        self._motivation_dirty = True
        self._emit_sickness_event(is_sick, cause)

    def set_hiding(self, is_hiding: bool) -> None:
        """Set or clear hiding status.

        Parameters
        ----------
        is_hiding : bool
            Whether the duck is now hiding.
        """
        old = self._is_hiding
        self._is_hiding = is_hiding
        if is_hiding and not old:
            self._hiding_coax_visits = 0
        self._record_change("is_hiding", old, is_hiding, "", "consequence")
        self._emit_hiding_event(is_hiding)

    @property
    def is_sick(self) -> bool:
        """Whether the duck is currently sick."""
        return self._is_sick

    @property
    def is_hiding(self) -> bool:
        """Whether the duck is currently hiding."""
        return self._is_hiding

    # ── Validation ───────────────────────────────────────────────────────

    def validate(self) -> List[str]:
        """Validate the entire internal state and return a list of errors.

        An empty list means everything is valid.  This method does NOT
        modify state — it only reports problems.
        """
        errors: List[str] = []

        for need_name in NEED_NAMES:
            val = self._needs.get(need_name, -1)
            if val < NEED_MIN or val > NEED_MAX:
                errors.append(
                    f"Need '{need_name}' out of bounds: {val}"
                )

        if not (0.0 <= self._trust <= 100.0):
            errors.append(f"Trust out of bounds: {self._trust}")

        if self._growth_stage not in VALID_GROWTH_STAGES:
            errors.append(
                f"Invalid growth stage: {self._growth_stage!r}"
            )

        if not (0.0 <= self._growth_progress <= 1.0):
            errors.append(
                f"Growth progress out of bounds: {self._growth_progress}"
            )

        return errors

    def _validate_need(self, need: str, value: float) -> float:
        """Clamp a need value to 0-100.

        Parameters
        ----------
        need : str
            The need name (unused, kept for signature symmetry).
        value : float
            The raw value.

        Returns
        -------
        float
            The clamped value.
        """
        return max(float(NEED_MIN), min(float(NEED_MAX), float(value)))

    def _validate_trust(self, value: float) -> float:
        """Clamp trust to 0-100."""
        return max(0.0, min(100.0, float(value)))

    def _validate_growth_stage(self, stage: str) -> bool:
        """Return True if *stage* is a recognized growth stage."""
        return stage in VALID_GROWTH_STAGES

    # ── Audit log ────────────────────────────────────────────────────────

    def get_recent_changes(self, limit: int = 50) -> List[StateChange]:
        """Return the most recent audit log entries (newest last).

        Parameters
        ----------
        limit : int
            Maximum number of entries to return.
        """
        entries = list(self._audit_log)
        return entries[-limit:]

    def get_changes_for(self, field: str, limit: int = 10) -> List[StateChange]:
        """Return recent changes for a specific field.

        Parameters
        ----------
        field : str
            Field name (e.g. ``"need.hunger"``, ``"trust"``).
        limit : int
            Maximum number of entries to return.
        """
        matching = [c for c in self._audit_log if c.field == field]
        return matching[-limit:]

    def _record_change(
        self,
        field: str,
        old_value: Any,
        new_value: Any,
        reason: str,
        source: str,
    ) -> None:
        """Append a ``StateChange`` to the audit log."""
        self._audit_log.append(StateChange(
            timestamp=time.time(),
            field=field,
            old_value=old_value,
            new_value=new_value,
            reason=reason,
            source=source,
        ))

    # ── Event emission helpers ───────────────────────────────────────────

    def _emit_need_event(
        self, need: str, old: float, new: float, reason: str
    ) -> None:
        """Emit a NeedChangedEvent if the event bus is available."""
        bus = self._get_event_bus()
        if bus is None:
            return
        try:
            from core.event_bus import NeedChangedEvent
            bus.emit(NeedChangedEvent(
                source="duck_store",
                need=need,
                old_value=old,
                new_value=new,
                reason=reason,
            ))
        except Exception:
            pass

    def _emit_trust_event(self, old: float, new: float, reason: str) -> None:
        """Emit a TrustChangedEvent if the event bus is available."""
        bus = self._get_event_bus()
        if bus is None:
            return
        try:
            from core.event_bus import TrustChangedEvent
            bus.emit(TrustChangedEvent(
                source="duck_store",
                old_value=old,
                new_value=new,
                reason=reason,
            ))
        except Exception:
            pass

    def _emit_mood_event(self, old_mood: str, new_mood: str) -> None:
        """Emit a MoodChangedEvent if the event bus is available."""
        bus = self._get_event_bus()
        if bus is None:
            return
        try:
            from core.event_bus import MoodChangedEvent
            bus.emit(MoodChangedEvent(
                source="duck_store",
                old_mood=old_mood,
                new_mood=new_mood,
            ))
        except Exception:
            pass

    def _emit_sickness_event(self, started: bool, cause: str) -> None:
        """Emit a SicknessEvent if the event bus is available."""
        bus = self._get_event_bus()
        if bus is None:
            return
        try:
            from core.event_bus import SicknessEvent
            bus.emit(SicknessEvent(
                source="duck_store",
                started=started,
                cause=cause,
            ))
        except Exception:
            pass

    def _emit_hiding_event(self, started: bool) -> None:
        """Emit a HidingEvent if the event bus is available."""
        bus = self._get_event_bus()
        if bus is None:
            return
        try:
            from core.event_bus import HidingEvent
            bus.emit(HidingEvent(
                source="duck_store",
                started=started,
            ))
        except Exception:
            pass

    # ── Persistence ──────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Serialize the store's state to a plain dict for saving.

        The output format is designed to be forward-compatible with the
        existing ``Duck.to_dict()`` structure so that saves can be shared.
        """
        return {
            "name": self._name,
            "created_at": self._created_at,
            "growth_stage": self._growth_stage,
            "growth_progress": round(self._growth_progress, 3),
            "needs": {n: round(v, 1) for n, v in self._needs.items()},
            "trust": round(self._trust, 2),
            "personality": dict(self._personality),
            "mood": self.get_mood(),
            "mood_score": round(self.get_mood_score(), 1),
            "motivation": round(self.get_motivation(), 3),
            "is_sick": self._is_sick,
            "sick_since": self._sick_since,
            "is_hiding": self._is_hiding,
            "hiding_coax_visits": self._hiding_coax_visits,
            "cooldown_until": self._cooldown_until,
            "current_action": self._current_action,
            "action_start_time": self._action_start_time,
        }

    def from_dict(self, data: dict) -> None:
        """Deserialize state from a plain dict, applying validation.

        Missing keys are filled with sensible defaults.  Invalid values
        are silently clamped rather than raising exceptions.

        Parameters
        ----------
        data : dict
            A dictionary previously produced by ``to_dict()``.
        """
        self._name = data.get("name", "Cheese")

        # created_at may be a float or an ISO string in legacy saves.
        raw_created = data.get("created_at", 0.0)
        if isinstance(raw_created, (int, float)):
            self._created_at = float(raw_created)
        else:
            self._created_at = 0.0

        self._growth_stage = data.get("growth_stage", "hatchling")
        if not self._validate_growth_stage(self._growth_stage):
            self._growth_stage = "hatchling"

        self._growth_progress = max(0.0, min(1.0, float(
            data.get("growth_progress", 0.0)
        )))

        # Needs — restore with validation.
        raw_needs = data.get("needs", {})
        for need_name in NEED_NAMES:
            self._needs[need_name] = self._validate_need(
                need_name, float(raw_needs.get(need_name, 50.0))
            )

        self._trust = self._validate_trust(
            float(data.get("trust", 20.0))
        )

        self._personality = dict(data.get("personality", {}))

        self._is_sick = bool(data.get("is_sick", False))
        self._sick_since = data.get("sick_since")
        self._is_hiding = bool(data.get("is_hiding", False))
        self._hiding_coax_visits = int(data.get("hiding_coax_visits", 0))
        self._cooldown_until = data.get("cooldown_until")
        self._current_action = data.get("current_action")
        self._action_start_time = data.get("action_start_time")

        # Mark derived state as stale.
        self._mood_dirty = True
        self._motivation_dirty = True

    def sync_from_duck(self, duck: "Duck") -> None:
        """Pull all state from an existing Duck object into the store.

        Parameters
        ----------
        duck : Duck
            The source Duck dataclass instance.
        """
        self._name = duck.name

        # created_at is stored as an ISO string on Duck; keep as-is.
        try:
            self._created_at = float(duck.created_at)
        except (ValueError, TypeError):
            self._created_at = 0.0

        self._growth_stage = duck.growth_stage
        self._growth_progress = duck.growth_progress

        # Pull needs.
        self._needs["hunger"] = self._validate_need("hunger", duck.needs.hunger)
        self._needs["energy"] = self._validate_need("energy", duck.needs.energy)
        self._needs["fun"] = self._validate_need("fun", duck.needs.fun)
        self._needs["cleanliness"] = self._validate_need("cleanliness", duck.needs.cleanliness)
        self._needs["social"] = self._validate_need("social", duck.needs.social)

        self._trust = self._validate_trust(duck.trust)
        self._personality = dict(duck.personality)

        self._is_sick = duck.is_sick
        self._sick_since = duck.sick_since
        self._is_hiding = duck.hiding
        self._hiding_coax_visits = duck.hiding_coax_visits
        self._cooldown_until = duck.cooldown_until
        self._current_action = duck.current_action
        self._action_start_time = duck.action_start_time

        # Derived state must be recalculated.
        self._mood_dirty = True
        self._motivation_dirty = True

    def sync_to_duck(self, duck: "Duck") -> None:
        """Push validated state from the store back to a Duck object.

        Parameters
        ----------
        duck : Duck
            The target Duck dataclass instance (modified in-place).
        """
        duck.name = self._name
        duck.growth_stage = self._growth_stage
        duck.growth_progress = self._growth_progress

        # Push needs.
        duck.needs.hunger = self._needs["hunger"]
        duck.needs.energy = self._needs["energy"]
        duck.needs.fun = self._needs["fun"]
        duck.needs.cleanliness = self._needs["cleanliness"]
        duck.needs.social = self._needs["social"]

        duck.trust = self._trust
        duck.personality = dict(self._personality)

        duck.is_sick = self._is_sick
        duck.sick_since = self._sick_since
        duck.hiding = self._is_hiding
        duck.hiding_coax_visits = self._hiding_coax_visits
        duck.cooldown_until = self._cooldown_until
        duck.current_action = self._current_action
        duck.action_start_time = self._action_start_time
