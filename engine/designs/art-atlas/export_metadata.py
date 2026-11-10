"""Read definition registries only. No Game instance, audio, or save access."""
import ast
from dataclasses import asdict, is_dataclass
from enum import Enum
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from world.atmosphere import VISITORS
from world.events import EVENTS, ENCOUNTERS, SPECIAL_DAY_EVENTS
from world.expanded_events import EXPANDED_EVENTS, EXPANDED_ENCOUNTERS
from world.area_events import AREA_EVENTS
from ui.event_animations import ANIMATED_EVENTS
from engine.pond_stories import STORIES


def plain(value):
    if is_dataclass(value):
        return plain(asdict(value))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(k): plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [plain(v) for v in value]
    return value


def export():
    flags = {}
    def record(event, area=False, encounter=False):
        animated = False if encounter else (bool(event.has_animation and event.animation_id) if area
                    else bool(event.has_animation and event.id in ANIMATED_EVENTS))
        flags[event.id] = dict(animated=animated, definition=plain(event),
                               kind='encounter' if encounter else 'area event' if area else 'event')
    for registry in (EVENTS, EXPANDED_EVENTS):
        for event in registry.values():
            record(event)
    for registry in (ENCOUNTERS, EXPANDED_ENCOUNTERS):
        for event in registry.values():
            record(event, encounter=True)
    for events in AREA_EVENTS.values():
        for event in events:
            record(event, area=True)
    def walk(value):
        if hasattr(value, 'has_animation'):
            record(value)
        elif isinstance(value, dict):
            for child in value.values():
                walk(child)
        elif isinstance(value, (list, tuple)):
            for child in value:
                walk(child)
    walk(SPECIAL_DAY_EVENTS)

    # Read the renderer's actual rare-visitor mapping instead of inventing one.
    tree = ast.parse((ROOT / 'engine/scene.py').read_text())
    species = next(ast.literal_eval(n.value) for n in ast.walk(tree)
                   if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'species' for t in n.targets))
    personalities = next(ast.literal_eval(n) for n in ast.walk(tree)
                         if isinstance(n, ast.Dict) and any(isinstance(k, ast.Constant) and k.value == 'celebrity_duck' for k in n.keys)
                         and len(n.keys) == 2)
    rare = [dict(**plain(visitor), asset=species.get(key, 'bird_flying'), rigPersonality=personalities.get(key))
            for key, visitor in VISITORS.items()]
    return dict(eventFlags=flags, rare=rare, stories=plain(STORIES))


if __name__ == '__main__':
    print(json.dumps(export(), ensure_ascii=False))
