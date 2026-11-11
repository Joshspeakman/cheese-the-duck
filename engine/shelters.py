"""Physical resting places. Ownership and placement always come from the game."""
import json
from pathlib import Path
ROOMS = json.loads((Path(__file__).parent/'client/animation/home-rooms.json').read_text())
AGES = ('egg', 'hatchling', 'duckling', 'juvenile', 'young_adult', 'adult', 'mature', 'elder', 'legendary')
HOMES = {
    'dog_house': (True, 'hatchling'), 'shed': (True, 'hatchling'),
    'mud_hut': (True, 'hatchling'), 'wooden_cottage': (True, 'hatchling'),
    'stone_house': (True, 'hatchling'), 'barn': (True, 'hatchling'),
    'greenhouse': (True, 'hatchling'), 'gazebo': (True, 'hatchling'),
    'treehouse': (True, 'juvenile'), 'lighthouse': (True, 'juvenile'),
    'basic_nest': (False, 'hatchling'), 'cozy_nest': (False, 'hatchling'),
    'deluxe_nest': (True, 'hatchling'), 'nest_premium': (True, 'hatchling'),
    'golden_nest': (True, 'hatchling'), 'bed_small': (False, 'hatchling'),
    'bed_king': (False, 'hatchling'), 'cozy_bed': (False, 'hatchling'),
}
# Birdhouses are wildlife shelters on poles: a grounded duck cannot enter them.
def adverse(weather):
    return weather in {'rain', 'rainy', 'heavy_rain', 'drizzle', 'spring_showers',
                       'storm', 'stormy', 'thunderstorm', 'summer_storm', 'ice_storm',
                       'snow', 'light_snow', 'snowy', 'heavy_snow', 'snow_flurries',
                       'blizzard', 'sleet', 'hail', 'bitter_cold', 'freezing'}

def position(placement):
    x, y = placement.get_display_position()
    return [round(x * 132 / 20), round(y * 42 / 12)]

def reservations(pond, key, destination, exclude=''):
    result=[]
    plan=pond.state.get('plan')
    if exclude!='cheese' and plan and plan.get('residence'):
        r=plan['residence']
        if r['id']==key and r['destination']==destination:result.append(r.get('slot',0))
    minds=getattr(pond,'minds',None)
    for actor,r in getattr(minds,'housing',{}).items():
        if actor!=exclude and r['id']==key and r['destination']==destination:
            result.append(r['slot'])
    return result


def candidates(pond, target='', actor='cheese', stage=None, position_at=None, species='duck'):
    if pond.location != 'Home Pond' or not pond.game:
        return []
    stage = stage or pond.game.duck.growth_stage
    age = AGES.index(stage) if stage in AGES else AGES.index('adult')
    wet = adverse(pond.weather_type)
    pos = pond.game.renderer.duck_pos
    choices = []
    for placed in getattr(pond, 'placements', []):
        key = placed.item_id
        if key not in HOMES or key not in pond.owned or (target and key != target):
            continue
        roof, youngest = HOMES[key]
        if age < AGES.index(youngest) or (wet and not roof) or (ROOMS[key]['elevated'] and species=='toad'):
            continue
        destination = position(placed)
        right = max(2, getattr(pos, '_play_width', 132)-8)
        bottom = max(2, getattr(pos, '_play_height', 42)-5)
        if not (2 <= destination[0] <= right and 2 <= destination[1] <= bottom):
            continue
        capacity=ROOMS[key]['capacity']
        used=reservations(pond,key,destination,actor)
        slots=[i for i in range(capacity) if i not in used]
        if not slots:continue
        px,py=position_at or (pos.x,pos.y)
        distance = abs(px-destination[0]) + abs(py-destination[1])
        comfort = 8 if 'nest' in key or 'bed' in key else 0
        choices.append({'id': key, 'destination': destination, 'roof': roof,
                        'score': distance-comfort, 'weather': pond.weather_type,
                        'slot':slots[0], 'capacity':capacity})
    return sorted(choices, key=lambda c: c['score'])

def still_placed(pond, residence):
    return residence['id'] in pond.owned and any(
        p.item_id == residence['id'] and position(p) == residence['destination']
        for p in getattr(pond, 'placements', []))
