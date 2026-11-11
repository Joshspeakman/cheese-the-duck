"""Simulation-owned nest choreography and bounded, persistent object memories.

The renderer samples the same authored score; rendering never advances a routine
or changes needs. A canceled routine has no completion effect.
"""
import hashlib
import json
from pathlib import Path
from engine import shelters

ROUTINES = json.loads((Path(__file__).parent / 'client/animation/nest-routines.json').read_text())['routines']
NESTS = {'basic_nest', 'cozy_nest', 'deluxe_nest', 'nest_premium', 'golden_nest'}
RAIN = {'rain', 'rainy', 'heavy_rain', 'drizzle', 'spring_showers'}
STORM = {'storm', 'stormy', 'thunderstorm', 'summer_storm', 'ice_storm'}
SNOW = {'snow', 'snowy', 'light_snow', 'heavy_snow', 'snow_flurries', 'blizzard', 'sleet'}
WIND = {'wind', 'windy', 'gusty', 'breezy', 'autumn_wind', 'leaf_storm', 'blizzard'}


def context(pond, plan):
    needs = pond.game.duck.needs
    mood = pond.game.duck.get_mood_state().value
    return dict(season=pond.season, hour=pond.hour, weather=pond.weather_type,
                temperature=pond.state['ecology']['temperature'], snow=pond.state['ecology']['snow'],
                energy=needs.energy, fun=needs.fun, social=needs.social, mood=mood,
                roof=plan['residence']['roof'], stage=pond.game.duck.growth_stage,
                bond=pond.state['objects'].get(plan['target'], {}).get('bond', 0.))


def eligible(spec, ctx):
    if ctx['stage'] == 'egg':
        return False  # An egg cannot pick up twigs or walk into a nest.
    gate = spec['when']
    hour, weather = ctx['hour'], ctx['weather']
    if gate.get('roof') and not ctx['roof']:
        return False
    if gate.get('season') and gate['season'] != ctx['season']:
        return False
    if gate.get('time'):
        period = gate['time']
        if not {'night': hour < 6 or hour >= 19, 'dawn': 5 <= hour < 9,
                'day': 7 <= hour < 19, 'noon': 11 <= hour < 15}.get(period, False):
            return False
    if gate.get('weather'):
        condition = gate['weather']
        if not {'rain': weather in RAIN | STORM, 'storm': weather in STORM,
                'wind': weather in WIND | STORM,
                'clear': not shelters.adverse(weather) and weather not in {'fog', 'foggy', 'misty', 'cloudy', 'overcast'}}.get(condition, False):
            return False
    if gate.get('temperature') == 'cold' and ctx['temperature'] > 8:
        return False
    if gate.get('temperature') == 'hot' and ctx['temperature'] < 25:
        return False
    if gate.get('snow') and ctx['snow'] < .05 and weather not in SNOW:
        return False
    if gate.get('bond', 0.) > ctx['bond']:
        return False
    if gate.get('mood'):
        condition = gate['mood']
        if not {'content': ctx['mood'] in {'happy', 'ecstatic', 'content'} and ctx['fun'] >= 50,
                'grumpy': ctx['mood'] in {'sad', 'miserable', 'angry', 'grumpy'} or ctx['fun'] < 30,
                'bored': ctx['fun'] < 45,
                'shy': ctx['social'] < 40}.get(condition, False):
            return False
    return True


def choose(pond, plan, ctx):
    obj = pond.state['objects'][plan['target']]
    history = obj.get('routines', {})
    recent = obj.get('recent_routines', [])[-4:]
    choices = [key for key, spec in ROUTINES.items() if eligible(spec, ctx)]
    varied = [key for key in choices if key not in recent]
    choices = varied or choices
    if not choices:
        return None
    def rank(key):
        spec = ROUTINES[key]
        salt = f"{pond.state['seed']}:{plan['target']}:{obj.get('routine_visits', 0)}:{key}"
        varied = int(hashlib.sha256(salt.encode()).hexdigest()[:8], 16) / 0xffffffff
        urge = ((100-ctx['energy'])/60 if spec['motive'] == 'rest' else
                obj.get('dirt', 0.)*2 if spec['motive'] == 'care' else (100-ctx['fun'])/100)
        # Contextual actions are favored, but repeated favorites lose priority.
        return varied*2 + urge + min(1.2, len(spec['when'])*.5) - history.get(key, 0)*.3
    return max(choices, key=rank)


def advance(pond, plan, dt):
    residence = plan.get('residence')
    if not residence or plan['target'] not in NESTS or plan['phase'] != 'act':
        return False
    ctx = context(pond, plan)
    current = residence.get('routine')
    if ctx['stage'] == 'egg' or pond.game.duck.needs.hunger <= 15:
        residence.pop('routine', None)
        return False
    if current and current['id'] not in ROUTINES:
        residence.pop('routine', None)
        current = None
    # Finishing a one-off visit does not start another routine. A real storm
    # wait may choose another, while retaining the visit's single reward cap.
    if current and current.get('done'):
        if not (ctx['roof'] and shelters.adverse(ctx['weather'])):
            return False
        current = None
    if current is None:
        key = choose(pond, plan, ctx)
        if not key:
            return False
        current = {'id': key, 'elapsed': 0., 'label': ROUTINES[key]['label'], 'done': False}
        residence['routine'] = current
        return True
    spec = ROUTINES[current['id']]
    # When the front passes or a condition changes, don't keep acting out a
    # vanished storm, heatwave or snow shower. No partial completion is recorded.
    if not eligible(spec, ctx):
        current['done'] = True
        current['interrupted'] = True
        current['elapsed'] = spec['duration']
        return False
    current['elapsed'] = min(spec['duration'], current['elapsed']+dt)
    if current['elapsed'] < spec['duration']:
        return True
    current['done'] = True
    obj = pond.state['objects'][plan['target']]
    history = obj.setdefault('routines', {})
    history[current['id']] = min(9999, history.get(current['id'], 0)+1)
    obj['routine_visits'] = min(999999, obj.get('routine_visits', 0)+1)
    obj['recent_routines'] = (obj.get('recent_routines', []) + [current['id']])[-12:]
    residence['performed'] = (residence.get('performed', []) + [current['id']])[-8:]
    tidied = min(spec['effect'].get('tidiness', 0.), max(0., .06-residence.get('tidied', 0.)))
    if tidied:
        removed = min(obj.get('dirt', 0.), tidied)
        obj['dirt'] = max(0., obj.get('dirt', 0.)-removed)
        residence['tidied'] = residence.get('tidied', 0.)+removed
    pond._cache = None
    return False
