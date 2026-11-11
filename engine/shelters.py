"""Physical resting places. Ownership and placement always come from the game."""
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

def candidates(pond, target=''):
    if pond.location != 'Home Pond' or not pond.game:
        return []
    stage = pond.game.duck.growth_stage
    age = AGES.index(stage) if stage in AGES else AGES.index('adult')
    wet = adverse(pond.weather_type)
    pos = pond.game.renderer.duck_pos
    choices = []
    for placed in getattr(pond, 'placements', []):
        key = placed.item_id
        if key not in HOMES or key not in pond.owned or (target and key != target):
            continue
        roof, youngest = HOMES[key]
        if age < AGES.index(youngest) or (wet and not roof):
            continue
        destination = position(placed)
        right = max(2, getattr(pos, '_play_width', 132)-8)
        bottom = max(2, getattr(pos, '_play_height', 42)-5)
        if not (2 <= destination[0] <= right and 2 <= destination[1] <= bottom):
            continue
        distance = abs(pos.x-destination[0]) + abs(pos.y-destination[1])
        comfort = 8 if 'nest' in key or 'bed' in key else 0
        choices.append({'id': key, 'destination': destination, 'roof': roof,
                        'score': distance-comfort, 'weather': pond.weather_type})
    return sorted(choices, key=lambda c: c['score'])

def still_placed(pond, residence):
    return residence['id'] in pond.owned and any(
        p.item_id == residence['id'] and position(p) == residence['destination']
        for p in getattr(pond, 'placements', []))
