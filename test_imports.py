import sys
import importlib
sys.path.insert(0, '.')

files = [
    'main', 'config', 'game_logger',
    'core.game', 'core.clock', 'core.persistence', 'core.progression', 'core.prestige', 'core.save_slots',
    'duck.duck', 'duck.needs', 'duck.mood', 'duck.behavior_ai', 'duck.personality', 'duck.aging',
    'world.shop', 'world.habitat', 'world.building', 'world.atmosphere', 'world.events',
    'world.crafting', 'world.materials', 'world.exploration',
    'dialogue.conversation', 'dialogue.llm_chat', 'dialogue.memory',
]

issues = []
for mod in files:
    try:
        importlib.import_module(mod)
        print(f'OK: {mod}')
    except Exception as e:
        issues.append(f'{mod}: {type(e).__name__}: {e}')
        print(f'FAIL: {mod}: {e}')

print()
print(f'Total issues: {len(issues)}')
for i in issues:
    print(f'  - {i}')
