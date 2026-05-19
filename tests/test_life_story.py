from __future__ import annotations

from types import SimpleNamespace

from duck.desires import DailyGoal, GoalType, TimeSlot
from world.life_story import LifeStorySystem


class _FakeCollectibles:
    def __init__(self, owned: int = 0, total: int = 20):
        self.owned = {f"c{i}": object() for i in range(owned)}
        self._owned = owned
        self._total = total

    def get_collection_stats(self):
        return {
            "unique_owned": self._owned,
            "total_possible": self._total,
            "completion_percent": (self._owned / self._total * 100) if self._total else 0,
        }


def _game(**overrides):
    goals = overrides.pop("goals", [])
    duck = SimpleNamespace(
        name="Cheese",
        trust=overrides.pop("trust", 20.0),
        growth_stage=overrides.pop("growth_stage", "duckling"),
        desires=SimpleNamespace(goals=goals),
    )
    game = SimpleNamespace(
        duck=duck,
        decorations=SimpleNamespace(total_comfort=0, total_beauty=0),
        habitat=SimpleNamespace(owned_items=[], placed_items=[]),
        building=SimpleNamespace(structures={}),
        collectibles=_FakeCollectibles(),
        exploration=SimpleNamespace(discovered_areas={}),
        tricks=SimpleNamespace(learned_tricks={}),
        garden=SimpleNamespace(total_harvests=0),
        quests=SimpleNamespace(total_quests_completed=0),
    )
    for key, value in overrides.items():
        setattr(game, key, value)
    return game


def test_life_screen_exposes_hidden_duck_agenda():
    goal = DailyGoal(
        goal_type=GoalType.EXPLORE,
        description="wants to inspect the pond",
        priority=1.0,
        time_slot=TimeSlot.MORNING,
        target_location="Home Pond",
        progress=0.5,
    )
    system = LifeStorySystem()

    lines = system.render_life_screen(_game(goals=[goal]))
    text = "\n".join(lines)

    assert "Plans" in text
    assert "Wander" in text
    assert "@ Home Pond" in text
    assert "50%" in text
    assert len(lines) <= 24
    assert max(len(line) for line in lines) <= 54


def test_agenda_completion_records_once_per_day():
    goal = DailyGoal(
        goal_type=GoalType.PLAY,
        description="play",
        priority=1.0,
        time_slot=TimeSlot.MORNING,
        progress=1.0,
        satisfied=True,
    )
    system = LifeStorySystem()
    desires = SimpleNamespace(goals=[goal])

    assert system.record_agenda_status(desires) == [
        "Plan complete. Cheese insists this was coincidence."
    ]
    assert system.record_agenda_status(desires) == []
    assert len(system.perfect_agenda_days) == 1


def test_life_story_persists_memories_and_progress():
    system = LifeStorySystem()
    system.record_travel("Home Pond", "pond")
    system.record_exploration(
        {"success": True, "rare_discovery": "Golden Scale", "resources": {"twig": 2}},
        area_name="Home Pond",
    )

    restored = LifeStorySystem.from_dict(system.to_dict())

    assert restored.visited_locations["Home Pond"] == 1
    assert restored.discovery_counts["rare"] == 1
    assert any(memory.key.startswith("rare:Golden Scale") for memory in restored.memories)


def test_legendary_cheese_arc_completes_when_connected_systems_are_done():
    system = LifeStorySystem()
    system.perfect_agenda_days = ["2026-05-17", "2026-05-18", "2026-05-19"]
    game = _game(
        trust=75.0,
        growth_stage="adult",
        decorations=SimpleNamespace(total_comfort=25, total_beauty=0),
        collectibles=_FakeCollectibles(owned=6, total=20),
        exploration=SimpleNamespace(
            discovered_areas={f"area{i}": object() for i in range(5)}
        ),
        tricks=SimpleNamespace(learned_tricks={f"trick{i}": object() for i in range(3)}),
        garden=SimpleNamespace(total_harvests=5),
        quests=SimpleNamespace(total_quests_completed=3),
    )

    assert all(step.done for step in system.get_long_term_steps(game))
    assert system.record_arc_completion(game) == [
        "Legend status achieved. Cheese remains Cheese. Dangerous."
    ]
    assert system.record_arc_completion(game) == []
