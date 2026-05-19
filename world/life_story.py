"""Connected life-story, agenda, and long-term arc tracking for Cheese.

This module intentionally keeps the narrative glue out of ``core.game``.
The game already owns the systems; this class listens to their outputs and
turns them into readable goals, memories, and long-term progress.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


def _value(obj: Any, default: str = "") -> str:
    """Return enum.value when available, otherwise a safe string."""
    if obj is None:
        return default
    value = getattr(obj, "value", None)
    if value is not None:
        return str(value)
    return str(obj)


def _clamp_percent(value: Any) -> int:
    try:
        return max(0, min(100, int(float(value) * 100)))
    except (TypeError, ValueError):
        return 0


def _today_key() -> str:
    return date.today().isoformat()


def _title(text: str) -> str:
    return text.replace("_", " ").title()


@dataclass
class LifeMemory:
    """A durable note for the player's life-story screen."""

    kind: str
    key: str
    title: str
    text: str
    day_key: str
    seen_count: int = 1
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "kind": self.kind,
            "key": self.key,
            "title": self.title,
            "text": self.text,
            "day_key": self.day_key,
            "seen_count": self.seen_count,
            "meta": self.meta,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LifeMemory":
        return cls(
            kind=str(data.get("kind", "note")),
            key=str(data.get("key", "")),
            title=str(data.get("title", "Note")),
            text=str(data.get("text", "")),
            day_key=str(data.get("day_key", _today_key())),
            seen_count=int(data.get("seen_count", 1)),
            meta=dict(data.get("meta", {})),
        )


@dataclass(frozen=True)
class LongTermStep:
    """One visible step in the Legendary Cheese arc."""

    key: str
    label: str
    current: float
    target: float
    note: str

    @property
    def done(self) -> bool:
        return self.current >= self.target

    @property
    def progress_text(self) -> str:
        if self.target <= 1:
            return "done" if self.done else "open"
        current = int(min(self.current, self.target))
        target = int(self.target)
        return f"{current}/{target}"


class LifeStorySystem:
    """Tracks the visible life layer: agenda, memories, home, and the arc."""

    MEMORY_LIMIT = 80

    _DAILY_EVENTS: Sequence[Tuple[str, str]] = (
        ("pond_check", "The pond is still wet. Bold choice. It works."),
        ("bread_weather", "Forecast says bread. Forecast may be biased."),
        ("feather_count", "Cheese counted his feathers. The number is private."),
        ("still_here", "Main task: remain alive and mildly difficult."),
        ("ignored_work", "Something needed doing. Cheese stared until it left."),
        ("mud_ok", "Mud status: fine. Human standards rejected."),
        ("snack_time", "Snack time has been moved to now. Again."),
    )

    _AGENDA_LINES: Dict[str, Tuple[str, str]] = {
        "explore": ("Wander", "go somewhere like it was on purpose"),
        "socialize": ("Be Seen", "let the human be nearby"),
        "play": ("Mess Around", "have fun, unfortunately"),
        "rest": ("Nap", "recharge by staring"),
        "forage": ("Snack", "find edible evidence"),
        "groom": ("Preen", "fix the feather situation"),
        "adventure": ("Big Wander", "visit a place with opinions"),
        "creative": ("Poke Stuff", "make, inspect, or learn a thing"),
        "acquire": ("Want Thing", "get thing. no questions"),
    }

    _BOND_MILESTONES: Sequence[Tuple[int, str, str]] = (
        (20, "Familiar", "Cheese knows you. That is not praise. Yet."),
        (35, "Friendly", "Cheese lets you stay. Big day for you."),
        (50, "Close", "Cheese trusts you with bread-adjacent matters."),
        (70, "Devoted", "Cheese cares. He is handling it poorly."),
        (90, "Bonded", "Cheese trusts you. He will now deny saying that."),
    )

    _HOME_TIERS: Sequence[Tuple[int, str, str]] = (
        (0, "Bare", "Shelter, technically. A generous word."),
        (10, "Livable", "Floor, but with ambition."),
        (25, "Cozy", "Comfortable enough for better complaints."),
        (50, "Fancy", "This is a residence now. Troubling."),
        (90, "Estate", "Cheese lives like tiny royalty. Fine."),
    )

    def __init__(self) -> None:
        self.day_key: str = _today_key()
        self.daily_event_key: str = ""
        self.daily_event_text: str = ""
        self.daily_event_announced: bool = False
        self.perfect_agenda_days: List[str] = []
        self.activity_counts: Dict[str, int] = {}
        self.visited_locations: Dict[str, int] = {}
        self.discovery_counts: Dict[str, int] = {}
        self.memory_keys_seen: set[str] = set()
        self.bond_milestones_seen: set[str] = set()
        self.collection_milestones_seen: set[str] = set()
        self.growth_stages_seen: set[str] = set()
        self.arc_completed: bool = False
        self.home_tier: str = ""
        self.last_home_score: int = 0
        self.memories: List[LifeMemory] = []

    # ------------------------------------------------------------------
    # Lifecycle and serialization

    def ensure_day(self, game: Any = None, announce: bool = False) -> Optional[str]:
        """Roll daily flavor forward and optionally return the one-shot note."""
        today = _today_key()
        if self.day_key != today:
            self.day_key = today
            self.daily_event_key = ""
            self.daily_event_text = ""
            self.daily_event_announced = False

        if not self.daily_event_text:
            duck_name = getattr(getattr(game, "duck", None), "name", "Cheese")
            seed = sum(ord(ch) for ch in f"{today}:{duck_name}")
            key, text = self._DAILY_EVENTS[seed % len(self._DAILY_EVENTS)]
            self.daily_event_key = key
            self.daily_event_text = text

        if announce and not self.daily_event_announced:
            self.daily_event_announced = True
            return f"Life note: {self.daily_event_text}"
        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "day_key": self.day_key,
            "daily_event_key": self.daily_event_key,
            "daily_event_text": self.daily_event_text,
            "daily_event_announced": self.daily_event_announced,
            "perfect_agenda_days": list(self.perfect_agenda_days),
            "activity_counts": dict(self.activity_counts),
            "visited_locations": dict(self.visited_locations),
            "discovery_counts": dict(self.discovery_counts),
            "memory_keys_seen": sorted(self.memory_keys_seen),
            "bond_milestones_seen": sorted(self.bond_milestones_seen),
            "collection_milestones_seen": sorted(self.collection_milestones_seen),
            "growth_stages_seen": sorted(self.growth_stages_seen),
            "arc_completed": self.arc_completed,
            "home_tier": self.home_tier,
            "last_home_score": self.last_home_score,
            "memories": [m.to_dict() for m in self.memories[-self.MEMORY_LIMIT:]],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LifeStorySystem":
        system = cls()
        system.day_key = str(data.get("day_key", _today_key()))
        system.daily_event_key = str(data.get("daily_event_key", ""))
        system.daily_event_text = str(data.get("daily_event_text", ""))
        system.daily_event_announced = bool(data.get("daily_event_announced", False))
        system.perfect_agenda_days = list(data.get("perfect_agenda_days", []))
        system.activity_counts = {
            str(k): int(v) for k, v in dict(data.get("activity_counts", {})).items()
        }
        system.visited_locations = {
            str(k): int(v) for k, v in dict(data.get("visited_locations", {})).items()
        }
        system.discovery_counts = {
            str(k): int(v) for k, v in dict(data.get("discovery_counts", {})).items()
        }
        system.memory_keys_seen = set(data.get("memory_keys_seen", []))
        system.bond_milestones_seen = set(data.get("bond_milestones_seen", []))
        system.collection_milestones_seen = set(data.get("collection_milestones_seen", []))
        system.growth_stages_seen = set(data.get("growth_stages_seen", []))
        system.arc_completed = bool(data.get("arc_completed", False))
        system.home_tier = str(data.get("home_tier", ""))
        system.last_home_score = int(data.get("last_home_score", 0))
        system.memories = [
            LifeMemory.from_dict(m)
            for m in data.get("memories", [])[-cls.MEMORY_LIMIT:]
        ]
        for memory in system.memories:
            system.memory_keys_seen.add(memory.key)
        return system

    # ------------------------------------------------------------------
    # Event ingestion

    def sync_from_game(self, game: Any, announce_day: bool = False) -> List[str]:
        """Record passive milestones from the current game state."""
        messages: List[str] = []
        day_note = self.ensure_day(game, announce=announce_day)
        if day_note:
            messages.append(day_note)

        duck = getattr(game, "duck", None)
        if duck:
            messages.extend(self.record_growth_stage(getattr(duck, "growth_stage", "")))
            messages.extend(self.record_bond_milestones(duck))

        desires = getattr(duck, "desires", None) if duck else None
        messages.extend(self.record_agenda_status(desires))
        messages.extend(self.record_home_snapshot(game))
        messages.extend(self.record_collection_snapshot(game))
        messages.extend(self.record_arc_completion(game))
        return messages

    def record_activity(self, activity: str, detail: str = "", amount: int = 1) -> List[str]:
        activity = str(activity or "activity")
        self.activity_counts[activity] = self.activity_counts.get(activity, 0) + max(1, amount)

        messages: List[str] = []
        first_key = f"first_activity:{activity}"
        if first_key not in self.memory_keys_seen:
            label = _title(activity)
            text = f"First {label.lower()}. Cheese was there. Barely."
            self._add_memory("activity", first_key, f"First {label}", text, {"detail": detail})
            messages.append(text)
        return messages

    def record_talk(self, message: str = "") -> List[str]:
        detail = message[:40] if message else ""
        return self.record_activity("talk", detail)

    def record_interaction(self, interaction: str, duck: Any = None) -> List[str]:
        messages = self.record_activity(interaction)
        count = self.activity_counts.get(interaction, 0)
        milestone_key = f"interaction:{interaction}:{count}"
        if count in (5, 25, 100) and milestone_key not in self.memory_keys_seen:
            label = _title(interaction)
            text = f"{label} x{count}. Cheese noticed. Do not make it weird."
            self._add_memory("interaction", milestone_key, f"{label} x{count}", text)
            messages.append(text)
        return messages

    def record_travel(
        self,
        area_name: str,
        biome: Optional[str] = None,
        duck: Any = None,
    ) -> List[str]:
        if not area_name:
            return []
        self.visited_locations[area_name] = self.visited_locations.get(area_name, 0) + 1
        messages: List[str] = []

        first_key = f"visit:{area_name}"
        if first_key not in self.memory_keys_seen:
            biome_text = f" ({_title(biome)})" if biome else ""
            text = f"{area_name}{biome_text}. New place. Same duck."
            self._add_memory("travel", first_key, f"First Visit: {area_name}", text)
            messages.append(text)

        visits = self.visited_locations[area_name]
        repeat_key = f"visit:{area_name}:{visits}"
        if visits in (5, 10, 25) and repeat_key not in self.memory_keys_seen:
            text = f"{area_name} x{visits}. It probably recognizes the waddling."
            self._add_memory("travel", repeat_key, f"{area_name} Regular", text)
            messages.append(text)
        return messages

    def record_exploration(
        self,
        result: Dict[str, Any],
        area_name: Optional[str] = None,
    ) -> List[str]:
        if not result or not result.get("success", True):
            return []

        self.activity_counts["explore"] = self.activity_counts.get("explore", 0) + 1
        messages: List[str] = []
        area = area_name or str(result.get("area") or result.get("biome") or "somewhere")

        new_area = result.get("new_area_discovered")
        if new_area:
            self.discovery_counts["areas"] = self.discovery_counts.get("areas", 0) + 1
            key = f"discover_area:{new_area}"
            text = f"Found {new_area}. The world got bigger. Rude."
            if self._add_memory("discovery", key, f"Discovered {new_area}", text):
                messages.append(text)

        rare = result.get("rare_discovery")
        if rare:
            self.discovery_counts["rare"] = self.discovery_counts.get("rare", 0) + 1
            key = f"rare:{rare}:{self.discovery_counts['rare']}"
            text = f"Rare thing found: {rare}. Cheese acted casual. Failed."
            if self._add_memory("discovery", key, f"Rare Find: {_title(str(rare))}", text):
                messages.append(text)

        resources = result.get("resources") or {}
        if resources:
            total = sum(int(v) for v in resources.values() if isinstance(v, (int, float)))
            self.discovery_counts["resources"] = self.discovery_counts.get("resources", 0) + total
            if self.discovery_counts["resources"] >= 50:
                key = "resources:50"
                text = "Fifty things gathered. This is a hoard with nicer lighting."
                if self._add_memory("discovery", key, "Resource Habit", text):
                    messages.append(text)

        first_key = f"explore:{area}"
        if first_key not in self.memory_keys_seen:
            text = f"Explored {area}. Outside still has things in it."
            if self._add_memory("explore", first_key, f"Explored {_title(area)}", text):
                messages.append(text)

        return messages

    def record_garden_harvest(self, rewards: Dict[str, Any]) -> List[str]:
        item = str(rewards.get("item") or "produce")
        messages = self.record_activity("garden_harvest", item)
        count = self.activity_counts.get("garden_harvest", 0)
        if count in (5, 25):
            key = f"garden_harvest:{count}"
            text = f"Harvest x{count}. Dirt paid rent."
            if self._add_memory("garden", key, f"Harvest x{count}", text):
                messages.append(text)
        return messages

    def record_photo(self, title: str = "") -> List[str]:
        messages = self.record_activity("photo", title)
        count = self.activity_counts.get("photo", 0)
        if count in (3, 10):
            key = f"photo:{count}"
            text = f"{count} photos. Cheese remains hard to capture emotionally."
            if self._add_memory("photo", key, f"Photo Archive x{count}", text):
                messages.append(text)
        return messages

    def record_agenda_status(self, desires: Any) -> List[str]:
        goals = list(getattr(desires, "goals", []) or [])
        if not goals:
            return []
        if not all(bool(getattr(goal, "satisfied", False)) for goal in goals):
            return []
        if self.day_key in self.perfect_agenda_days:
            return []
        self.perfect_agenda_days.append(self.day_key)
        text = "Plan complete. Cheese insists this was coincidence."
        self._add_memory("agenda", f"agenda_complete:{self.day_key}", "Plan Complete", text)
        return [text]

    def record_growth_stage(self, stage: Any) -> List[str]:
        stage_value = _value(stage, "").lower()
        if not stage_value:
            return []
        key = f"growth:{stage_value}"
        if key in self.growth_stages_seen:
            return []
        self.growth_stages_seen.add(key)
        text = f"Cheese is now {_title(stage_value)}. Smaller than the attitude."
        self._add_memory("growth", key, f"Stage: {_title(stage_value)}", text)
        return [text]

    def record_bond_milestones(self, duck: Any) -> List[str]:
        trust = float(getattr(duck, "trust", 0) or 0)
        messages: List[str] = []
        for threshold, label, text in self._BOND_MILESTONES:
            key = f"bond:{threshold}"
            if trust >= threshold and key not in self.bond_milestones_seen:
                self.bond_milestones_seen.add(key)
                self._add_memory("bond", key, f"Bond: {label}", text)
                messages.append(text)
        return messages[-1:]

    def record_home_snapshot(self, game: Any) -> List[str]:
        score = self._home_score(game)
        tier_name, tier_text = self._home_tier_for_score(score)
        self.last_home_score = score
        if tier_name == self.home_tier:
            return []
        previous = self.home_tier
        self.home_tier = tier_name
        key = f"home:{tier_name}"
        if previous and self._add_memory("home", key, f"Home: {tier_name}", tier_text, {"score": score}):
            return [tier_text]
        if not previous:
            self._add_memory("home", key, f"Home: {tier_name}", tier_text, {"score": score})
        return []

    def record_collection_snapshot(self, game: Any) -> List[str]:
        owned, total, percent = self._collection_stats(game)
        if total <= 0:
            return []
        messages: List[str] = []
        for threshold in (1, 5, 10, 25, 50, 75, 100):
            if percent >= threshold:
                key = f"collection:{threshold}"
                if key not in self.collection_milestones_seen:
                    self.collection_milestones_seen.add(key)
                    text = f"Collection hit {threshold}%. Stuff is happening."
                    self._add_memory(
                        "collection",
                        key,
                        f"Collection {threshold}%",
                        text,
                        {"owned": owned, "total": total},
                    )
                    messages.append(text)
        return messages[-1:]

    def record_arc_completion(self, game: Any) -> List[str]:
        steps = self.get_long_term_steps(game)
        complete = bool(steps) and all(step.done for step in steps)
        if not complete or self.arc_completed:
            return []
        self.arc_completed = True
        text = "Legend status achieved. Cheese remains Cheese. Dangerous."
        self._add_memory("arc", "legendary_cheese", "Legend Cheese", text)
        return [text]

    # ------------------------------------------------------------------
    # Rendering

    def render_life_screen(self, game: Any, width: int = 54) -> List[str]:
        self.ensure_day(game, announce=False)
        duck = getattr(game, "duck", None)
        name = getattr(duck, "name", "Cheese")

        width = max(36, min(width, 54))
        lines: List[str] = [f"{name}'s Day"]

        lines.extend(self._wrap(f"Today: {self.daily_event_text}", width))
        lines.append("")
        lines.append("Plans")
        lines.extend(self._agenda_lines(getattr(duck, "desires", None), width))

        lines.append("")
        lines.append("Trust / Nest")
        lines.extend(self._bond_home_lines(game, width))

        lines.append("")
        lines.append("Becoming A Problem")
        lines.extend(self._arc_lines(game, width))

        lines.append("")
        lines.append("Notes")
        recent = list(reversed(self.memories[-2:]))
        if not recent:
            lines.append("No notes yet. Suspiciously peaceful.")
        else:
            for memory in recent:
                lines.append(self._ellipsize(f"- {memory.title}: {memory.text}", width))

        lines.append("[Esc/Bksp] Close")
        return lines

    def get_long_term_steps(self, game: Any) -> List[LongTermStep]:
        duck = getattr(game, "duck", None)
        trust = float(getattr(duck, "trust", 0) or 0)

        discovered = 0
        exploration = getattr(game, "exploration", None)
        if exploration is not None:
            discovered = len(getattr(exploration, "discovered_areas", {}) or {})

        owned, total, collection_percent = self._collection_stats(game)
        home_score = self._home_score(game)
        trick_count = len(getattr(getattr(game, "tricks", None), "learned_tricks", {}) or {})
        garden_harvests = int(getattr(getattr(game, "garden", None), "total_harvests", 0) or 0)
        quest_count = int(getattr(getattr(game, "quests", None), "total_quests_completed", 0) or 0)
        agenda_days = len(self.perfect_agenda_days)
        growth_rank = self._growth_rank(getattr(duck, "growth_stage", "")) if duck else 0

        return [
            LongTermStep("bond", "Trust", trust, 70, "earn the side-eye"),
            LongTermStep("agenda", "Plans", agenda_days, 3, "finish tiny demands"),
            LongTermStep("explore", "World", discovered, 5, "outside happened"),
            LongTermStep("home", "Nest", home_score, 25, "less floor, more glory"),
            LongTermStep("collect", "Stuff", collection_percent, 25, f"{owned}/{total} shiny bits"),
            LongTermStep("tricks", "Tricks", trick_count, 3, "skill, allegedly"),
            LongTermStep("garden", "Garden", garden_harvests, 5, "make dirt pay rent"),
            LongTermStep("quests", "Quests", quest_count, 3, "do named chores"),
            LongTermStep("growth", "Grow", growth_rank, 3, "become more duck"),
        ]

    # ------------------------------------------------------------------
    # Internal helpers

    def _add_memory(
        self,
        kind: str,
        key: str,
        title: str,
        text: str,
        meta: Optional[Dict[str, Any]] = None,
    ) -> bool:
        if not key:
            return False
        for memory in self.memories:
            if memory.key == key:
                memory.seen_count += 1
                return False
        self.memory_keys_seen.add(key)
        self.memories.append(
            LifeMemory(
                kind=kind,
                key=key,
                title=title,
                text=text,
                day_key=self.day_key,
                meta=meta or {},
            )
        )
        if len(self.memories) > self.MEMORY_LIMIT:
            self.memories = self.memories[-self.MEMORY_LIMIT:]
            self.memory_keys_seen = {m.key for m in self.memories}
        return True

    def _agenda_lines(self, desires: Any, width: int) -> List[str]:
        goals = list(getattr(desires, "goals", []) or [])
        if not goals:
            return ["No plan yet. Cheese is free-range."]

        lines: List[str] = []
        for index, goal in enumerate(goals, start=1):
            goal_type = _value(getattr(goal, "goal_type", None), "rest")
            slot = _title(_value(getattr(goal, "time_slot", None), "anytime"))
            target = getattr(goal, "target_location", None)
            progress = _clamp_percent(getattr(goal, "progress", 0))
            done = bool(getattr(goal, "satisfied", False))
            title, hint = self._AGENDA_LINES.get(goal_type, (_title(goal_type), "Do the thing. Quietly."))
            marker = "x" if done else " "
            line = f"{index}. [{marker}] {slot} {title} {progress}%"
            if target:
                line += f" @ {target}"
            else:
                line += f": {hint}"
            lines.append(self._ellipsize(line, width))
        return lines

    def _bond_home_lines(self, game: Any, width: int) -> List[str]:
        duck = getattr(game, "duck", None)
        trust = float(getattr(duck, "trust", 0) or 0)
        stage = _title(_value(getattr(duck, "growth_stage", ""), "unknown"))
        score = self._home_score(game)
        self.last_home_score = score
        tier_name, tier_text = self._home_tier_for_score(score)

        return [
            self._ellipsize(f"Trust {trust:.1f}/100 | {stage} | Nest: {tier_name} ({score})", width),
            self._ellipsize(tier_text, width),
        ]

    def _arc_lines(self, game: Any, width: int) -> List[str]:
        steps = self.get_long_term_steps(game)
        complete = all(step.done for step in steps)
        priority = ["bond", "explore", "home", "collect"]
        shown = [step for key in priority for step in steps if step.key == key]
        lines = []
        for step in shown:
            marker = "x" if step.done else " "
            text = f"[{marker}] {step.label} {step.progress_text} - {step.note}"
            lines.append(self._ellipsize(text, width))

        hidden = {step.key: step for step in steps if step not in shown}
        lines.append(
            f"More: Plans {hidden['agenda'].progress_text}, "
            f"Tricks {hidden['tricks'].progress_text}, "
            f"Garden {hidden['garden'].progress_text}"
        )
        lines.append(
            f"      Quests {hidden['quests'].progress_text}, "
            f"Grow {hidden['growth'].progress_text}"
        )

        status = "Legendary. Somehow." if complete else "Not legendary yet. Very loud though."
        lines.append(self._ellipsize(f"Status: {status}", width))
        return lines

    def _home_score(self, game: Any) -> int:
        decorations = getattr(game, "decorations", None)
        score = 0
        if decorations is not None:
            score += int(getattr(decorations, "total_comfort", 0) or 0)
            score += int(getattr(decorations, "total_beauty", 0) or 0)

        habitat = getattr(game, "habitat", None)
        if habitat is not None:
            owned_items = getattr(habitat, "owned_items", []) or []
            placed_items = getattr(habitat, "placed_items", []) or []
            score += min(20, len(owned_items) + len(placed_items))

        building = getattr(game, "building", None)
        if building is not None:
            structures = getattr(building, "structures", {}) or {}
            score += min(20, len(structures) * 3)
        return score

    def _home_tier_for_score(self, score: int) -> Tuple[str, str]:
        tier_name, tier_text = self._HOME_TIERS[0][1], self._HOME_TIERS[0][2]
        for threshold, name, text in self._HOME_TIERS:
            if score >= threshold:
                tier_name, tier_text = name, text
        return tier_name, tier_text

    def _collection_stats(self, game: Any) -> Tuple[int, int, float]:
        collectibles = getattr(game, "collectibles", None)
        if collectibles is None:
            return 0, 0, 0.0
        try:
            stats = collectibles.get_collection_stats()
            owned = int(stats.get("unique_owned", 0))
            total = int(stats.get("total_possible", 0))
            percent = float(stats.get("completion_percent", 0.0))
            return owned, total, percent
        except Exception:
            owned = len(getattr(collectibles, "owned", {}) or {})
            return owned, 0, 0.0

    def _growth_rank(self, stage: Any) -> int:
        stage_value = _value(stage, "").lower()
        ranks = {
            "egg": 0,
            "hatchling": 1,
            "duckling": 1,
            "juvenile": 2,
            "teen": 2,
            "young_adult": 3,
            "adult": 3,
            "mature": 4,
            "elder": 4,
            "legendary": 5,
        }
        return ranks.get(stage_value, 0)

    def _ellipsize(self, text: str, width: int) -> str:
        if width <= 3:
            return text[:width]
        if len(text) <= width:
            return text
        return text[: width - 3].rstrip() + "..."

    def _wrap(self, text: str, width: int) -> List[str]:
        if width <= 0:
            return [text]
        words = text.split()
        if not words:
            return [""]
        lines: List[str] = []
        current = ""
        for word in words:
            if len(word) > width:
                if current:
                    lines.append(current)
                    current = ""
                while len(word) > width:
                    lines.append(word[:width])
                    word = word[width:]
                current = word
                continue
            candidate = word if not current else f"{current} {word}"
            if len(candidate) <= width:
                current = candidate
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines
