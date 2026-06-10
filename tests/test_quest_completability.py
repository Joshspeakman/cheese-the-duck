"""Regression tests: every quest must be completable with events the game
actually emits.

The emission vocabulary below mirrors the _process_quest_updates() call sites
in core/game.py. If a quest objective requires a (type, target) pair the game
never emits, these tests fail — that is exactly the bug that shipped with
lost_feather (collect/find never emitted) and mysterious_stranger (no choice
UI, find/talk-guardian never emitted).
"""

import pytest

from world.quests import QuestSystem, QUESTS, ObjectiveType


# (objective_type, target) pairs core/game.py can emit, mirroring its
# _process_quest_updates() call sites. Parametric targets (craft item ids,
# biome values, quest discovery items) are expanded explicitly.
EMITTABLE = {
    ("feed", "any"), ("play", "any"), ("clean", "any"), ("pet", "any"), ("sleep", "any"),
    ("talk", "any"), ("talk", "guardian"),
    ("explore", "pond"), ("explore", "forest"), ("explore", "meadow"),
    ("explore", "riverside"), ("explore", "garden"), ("explore", "mountains"),
    ("explore", "beach"), ("explore", "swamp"), ("explore", "urban"),
    ("fish", "any"), ("fish", "rare"),
    ("garden", "plant"), ("garden", "water"), ("garden", "harvest"),
    ("collect", "shiny_object"),
    ("find", "water_token"), ("find", "earth_token"), ("find", "sky_token"),
}
# craft/build targets are open-ended (any recipe/blueprint id)
OPEN_ENDED_TYPES = {"craft", "build"}


def _emit_for(objective):
    """Return an (objective_type, target) emission that satisfies objective."""
    otype = objective.objective_type.value
    target = objective.target
    if otype in OPEN_ENDED_TYPES:
        return (otype, target if target != "any" else "anything")
    if target == "any":
        # any emission of this type matches; find one in the vocabulary
        for et, tt in EMITTABLE:
            if et == otype:
                return (et, tt)
        return None
    return (otype, target) if (otype, target) in EMITTABLE else None


@pytest.mark.parametrize("quest_id", list(QUESTS.keys()))
def test_quest_objectives_are_emittable(quest_id):
    """Every non-choice objective must match something the game can emit."""
    quest = QUESTS[quest_id]
    for step in quest.steps:
        for obj in step.objectives:
            if obj.objective_type == ObjectiveType.CHOICE:
                continue  # satisfied via the quest decision prompt
            assert _emit_for(obj) is not None, (
                f"{quest_id} step {step.step_id} objective {obj.id} requires "
                f"({obj.objective_type.value!r}, {obj.target!r}) which the game never emits"
            )


@pytest.mark.parametrize("quest_id", list(QUESTS.keys()))
def test_quest_is_completable_end_to_end(quest_id):
    """Drive each quest to completion through the public QuestSystem API."""
    system = QuestSystem()
    ok, _, _ = system.start_quest(quest_id)
    assert ok

    quest = QUESTS[quest_id]
    reward_seen = False

    for _ in range(200):  # generous upper bound on steps * objectives
        if quest_id not in system.active_quests:
            break  # completed (or ended)
        active = system.active_quests[quest_id]
        step = next(s for s in quest.steps if s.step_id == active.current_step)

        choice_objs = [o for o in step.objectives if o.objective_type == ObjectiveType.CHOICE]
        if choice_objs or step.choices:
            choices = system.get_pending_choices(quest_id)
            assert choices, f"{quest_id} step {step.step_id} has a choice objective but no choices"
            # Always pick the first option (the "accept" path)
            ok, _, _ = system.make_choice(quest_id, choices[0])
            assert ok
            continue

        if not step.objectives:
            # Steps with no objectives complete via update_progress's sweep
            _, completed = system.update_progress("noop", "noop", 0)
            if completed:
                reward_seen = True
            continue

        for obj in step.objectives:
            emission = _emit_for(obj)
            assert emission is not None
            _, completed = system.update_progress(emission[0], emission[1], obj.required_amount)
            if completed:
                reward_seen = True

    assert quest_id in system.completed_quests, f"{quest_id} could not be completed"
    assert reward_seen, f"{quest_id} completed without surfacing a final reward"


def test_has_active_objective():
    system = QuestSystem()
    system.start_quest("mysterious_stranger")
    # Step 1 is a choice; find objectives not yet active
    assert not system.has_active_objective("find", "water_token")
    choices = system.get_pending_choices("mysterious_stranger")
    system.make_choice("mysterious_stranger", choices[0])
    assert system.has_active_objective("find", "water_token")
    assert system.has_active_objective("find", "earth_token")
    assert system.has_active_objective("find", "sky_token")
    # Completing one token clears only that objective
    system.update_progress("find", "water_token", 1)
    assert not system.has_active_objective("find", "water_token")
    assert system.has_active_objective("find", "sky_token")


def test_no_prereq_quests_are_available():
    """Quests without prerequisites must appear without chain unlocks."""
    system = QuestSystem()
    available = {q.id for q in system.get_available_quests(player_level=99)}
    for quest_id, quest in QUESTS.items():
        if not quest.prerequisite_quests:
            assert quest_id in available, f"{quest_id} has no prereqs but is not offered"


def test_crafted_results_all_route_to_an_inventory():
    """Every crafting recipe result must land in ITEMS, MATERIALS, or tools."""
    from world.crafting import RECIPES, CraftingCategory
    from world.items import ITEMS
    from world.materials import MATERIALS

    for recipe in RECIPES.values():
        routed = (
            recipe.result_id in ITEMS
            or recipe.result_id in MATERIALS
            or recipe.category == CraftingCategory.TOOL
        )
        assert routed, f"recipe {recipe.id} result {recipe.result_id} has no inventory registry"


def test_quest_reward_items_exist():
    """Quest step/final reward item ids must be grantable."""
    from world.items import ITEMS
    from world.materials import MATERIALS

    for quest_id, quest in QUESTS.items():
        rewards = [s.rewards for s in quest.steps if s.rewards] + [quest.final_reward]
        for reward in rewards:
            for item_id in getattr(reward, "items", []) or []:
                assert item_id in ITEMS or item_id in MATERIALS, (
                    f"{quest_id} rewards unknown item {item_id!r}"
                )
