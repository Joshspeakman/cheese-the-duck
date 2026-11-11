"""Simulation-owned nest choreography and bounded, persistent object memories.

The renderer samples the same authored score; rendering never advances a routine
or changes needs. A canceled routine has no completion effect.
"""
import hashlib
import json
from pathlib import Path
from engine import shelters, nest_materials

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
                bond=(pond.object_state(plan['target'],plan) or {}).get('bond', 0.),
                material=nest_materials.state(pond.object_state(plan['target'],plan)))


def eligible(spec, ctx, material_required=True):
    if ctx['stage'] == 'egg':
        return False  # An egg cannot pick up twigs or walk into a nest.
    gate = spec['when']
    if material_required and gate.get('material') and ctx.get('material', {}).get(gate['material'], 0) <= .02:
        return False
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
    obj = pond.object_state(plan['target'],plan)
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
    from engine.shelter_company import for_actor
    if for_actor(pond.minds, 'cheese'):
        return False  # Shared conversation owns the body until it finishes.
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
        current['quiet_elapsed']=current.get('quiet_elapsed',0.)+max(0.,dt)
        if current['quiet_elapsed'] < 8:
            return False  # Leave a real opening for a sheltered friend's reply.
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
    if not eligible(spec, ctx, material_required=not current.get('contacts')):
        current['done'] = True
        current['interrupted'] = True
        current['elapsed'] = spec['duration']
        return False
    previous = current['elapsed']
    current['elapsed'] = min(spec['duration'], current['elapsed']+max(0., dt))
    obj = pond.object_state(plan['target'],plan)
    nest_materials.contacts(obj, current, spec, previous, current['elapsed'])
    pond._cache = None
    if current['elapsed'] < spec['duration']:
        return True
    current['done'] = True
    current['finished_at'] = pond.state['elapsed']
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


# Visitors have their own temperament/needs and reserved seat. These actions
# don't borrow Cheese's tools or move a prop through another resident's body.
# Detailed material work remains the occupant's separate maintenance activity.
VISITOR_ROUTINES = {
    'bowl_test', 'circle_settle', 'tamp_floor', 'curl_sleep', 'one_eye_guard',
    'dream_paddle', 'startled_awake', 'long_yawn', 'stretch_wing', 'foot_tuck',
    'tail_wriggle', 'chin_on_rim', 'satisfied_sigh', 'shy_hide', 'proud_inspect',
    'rain_listen', 'drip_watch', 'thunder_duck', 'cold_huddle', 'heat_fan',
    'dawn_lookout', 'noon_doze', 'bedtime_tuck', 'sniff_lining',
    'toe_trace',
}

def visitor_choices(species):
    if species=='butterfly':
        return {'rain_listen','drip_watch','dawn_lookout','noon_doze','shy_hide','proud_inspect','cold_huddle'}
    if species=='toad':
        return VISITOR_ROUTINES-{'curl_sleep','stretch_wing','heat_fan','bedtime_tuck'}
    return VISITOR_ROUTINES


def visitor_advance(minds, key, residence, dt):
    if residence['id'] not in NESTS or residence['phase'] != 'inside':return
    from engine.shelter_company import for_actor
    if for_actor(minds, key):return
    pond = minds.pond
    obj = pond.object_state(residence['id'], residence)
    if obj is None:return
    actor = minds.model.residents[key]
    from world.guest_cast import guest_profile
    species=(guest_profile(actor['cast']) or {}).get('species','duck')
    ctx = dict(season=pond.season, hour=pond.hour, weather=pond.weather_type,
               temperature=pond.state['ecology']['temperature'], snow=pond.state['ecology']['snow'],
               roof=True, stage='duckling' if key=='story:pip' else 'adult',
               energy=actor['energy']*100, fun=actor['mood']*100,
               social=actor['social']*100, mood='content' if actor['mood']>=.45 else 'sad',
               bond=obj.get('bond',0), material=nest_materials.state(obj))
    current = residence.get('routine')
    if current and current.get('done'):
        if minds.now < current.get('finished_at', minds.now)+8:return
        current = None
    if not current:
        recent = residence.get('nest_recent', [])[-3:]
        history = obj.setdefault('guest_routines', {})
        choices = [k for k in visitor_choices(species) if eligible(ROUTINES[k],ctx) and k not in recent]
        if not choices:return
        def rank(k):
            spec=ROUTINES[k]
            salt=f"{pond.state['seed']}:{key}:{residence['id']}:{residence.get('nest_turn',0)}:{k}"
            variety=int(hashlib.sha256(salt.encode()).hexdigest()[:8],16)/0xffffffff
            urge=(1-actor['energy'])*3 if spec['motive']=='rest' else actor['traits']['curiosity']
            if k=='shy_hide':urge+=1-actor['traits']['confidence']
            if k in ('rain_listen','drip_watch'):urge+=actor['traits']['patience']*.5
            return variety+urge+len(spec['when'])*.3-history.get(k,0)*.08
        name=max(sorted(choices),key=rank)
        label=ROUTINES[name]['label'].replace('his ', 'the ').replace('himself','themselves')
        if species=='butterfly':
            label={'cold_huddle':'Folding wings close beneath the canopy',
                   'shy_hide':'Peeking out from behind the nest rim',
                   'noon_doze':'Resting folded wings in the sheltered hollow'}.get(name,label)
        residence['routine']=dict(id=name,elapsed=0.,done=False,label=label)
        pond._cache=None
        return
    spec = ROUTINES.get(current['id'])
    if not spec or not eligible(spec,ctx):
        current.update(done=True,interrupted=True,finished_at=minds.now)
        return
    previous=current['elapsed'];current['elapsed']=min(spec['duration'],previous+max(0.,dt))
    nest_materials.contacts(obj,current,spec,previous,current['elapsed'])
    pond._cache=None
    if current['elapsed']<spec['duration']:return
    current.update(done=True,finished_at=minds.now)
    history=obj.setdefault('guest_routines',{})
    history[current['id']]=min(9999,history.get(current['id'],0)+1)
    residence['nest_recent']=(residence.get('nest_recent',[])+[current['id']])[-6:]
    residence['nest_turn']=residence.get('nest_turn',0)+1
    # One genuine settling experience per stay, independent of how many quiet
    # routines play while a storm lasts. No item uses, currency or XP are paid.
    if not residence.get('nest_learned'):
        note=current['label']+' in the '+residence['id'].replace('_',' ')+'.'
        minds.model.learn(key,'rest',residence['context'],.12,minds.now,note)
        residence['nest_learned']=True
