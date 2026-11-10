"""Read the complete original cast/event registries into a preview-only catalog."""
import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from world.friends import DUCK_NAMES, DUCK_APPEARANCES, VISITOR_ASCII_ART
from world.events import EVENTS, ENCOUNTERS, SPECIAL_DAY_EVENTS
from world.expanded_events import EXPANDED_EVENTS, EXPANDED_ENCOUNTERS
from world.area_events import AREA_EVENTS
from ui import sprite_library as sprites
from ui.event_animations import create_event_animator


def export():
    tree = ast.parse((ROOT / 'ui/event_animations.py').read_text())
    factory = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'create_event_animator')
    mappings = {}
    for node in ast.walk(factory):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Dict):
            name = node.targets[0].id
            if name == 'specific':
                mappings[name] = {ast.literal_eval(key): None for key in node.value.keys}
            else:
                mappings[name] = ast.literal_eval(node.value)
    assets = []
    for category in ('CREATURES', 'FOOD', 'OBJECTS', 'HUMANS', 'CELESTIAL', 'PROPS', 'VEHICLES'):
        for key, frames in getattr(sprites, category).items():
            assets.append(dict(id=category.lower() + ':' + key, category=category.lower(), key=key,
                               name=key.replace('_', ' ').title(), frames=frames))
    friends = [dict(id='friend:' + name.lower(), name=name, personality=personality,
                    appearance=DUCK_APPEARANCES[personality], original=VISITOR_ASCII_ART[personality])
               for personality, names in DUCK_NAMES.items() for name in names]
    records = {}
    def record(event, source, animation=None):
        key = event.id
        records[key] = dict(id=key, name=event.name,
                            message=getattr(event, 'message', getattr(event, 'trigger_message', '')),
                            source=source, animation=animation or key)
    for source, events in [('events', EVENTS), ('expanded', EXPANDED_EVENTS), ('encounters', ENCOUNTERS), ('expanded encounters', EXPANDED_ENCOUNTERS)]:
        for event in events.values():
            record(event, source)
    for area, events in AREA_EVENTS.items():
        for event in events:
            record(event, area, event.animation_id if event.has_animation else None)
    def special_walk(value):
        if hasattr(value, 'id') and hasattr(value, 'name'):
            record(value, 'special days')
        elif isinstance(value, dict):
            for child in value.values(): special_walk(child)
        elif isinstance(value, (list, tuple)):
            for child in value: special_walk(child)
    special_walk(SPECIAL_DAY_EVENTS)
    for mapping in mappings.values():
        for key in mapping:
            records.setdefault(key, dict(id=key, name=key.replace('_', ' ').title(), message='', source='animation', animation=key))
    for event in records.values():
        key = event['animation']
        group = next((name for name, entries in mappings.items() if key in entries), 'ambient_events')
        event['group'] = group
        event['recipe'] = mappings.get(group, {}).get(key) or ['sparkle', 'white']
        animator = create_event_animator(key)
        event['animator'] = type(animator).__name__
        event['original'] = animator.get_sprite()
    data = dict(friends=friends, assets=assets, events=list(records.values()))
    target = Path(__file__).with_name('catalog.mjs')
    target.write_text('// Generated from the original registries. Dialogue is copied verbatim.\nexport const CATALOG=' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
    print(json.dumps({'friends': len(friends), 'assets': len(assets), 'events': len(records), 'animator_families': len({e['animator'] for e in records.values()})}))
    return data


if __name__ == '__main__':
    export()
