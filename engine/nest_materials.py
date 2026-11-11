"""The lining and loose materials of one physical nest.

These are parts of the furnishing, not inventory resources. Native contact
events move them; drawing and conversation only read copies of this state.
"""
import copy
import math

NESTS = {'basic_nest', 'cozy_nest', 'deluxe_nest', 'nest_premium', 'golden_nest'}
DEFAULTS = dict(left=.22, right=.28, brace=0., mend=0., plump=.5,
                hollow=.2, width=.5, feather=0., leaf=0., twig=1.,
                grit=.6, crumbs=.35, pebble=0., acorn=0., petals=0.,
                snow=0., frost=0., groove=0., braid=.25)
SNOW = {'snow', 'snowy', 'light_snow', 'heavy_snow', 'snow_flurries', 'blizzard', 'sleet'}
WET = {'rain', 'rainy', 'heavy_rain', 'drizzle', 'spring_showers', 'storm',
       'stormy', 'thunderstorm', 'summer_storm', 'sleet', 'hail', 'ice_storm'}


def finite(value, default=0.):
    return value if isinstance(value, (int, float)) and math.isfinite(value) else default


def clamp(value):
    return max(0., min(1., finite(value)))


def state(obj):
    if not isinstance(obj.get('nest'), dict):
        obj['nest'] = {}
    s = obj['nest']
    for key, default in DEFAULTS.items():
        s[key] = clamp(finite(s.get(key), default))
    s['touches'] = max(0, min(999999, int(finite(s.get('touches')))))
    return s


def update(item, obj, dt, outdoors, weather, temperature, wind, intensity, season):
    if item not in NESTS or not outdoors:
        return
    s = state(obj)
    minutes = max(0., finite(dt))/60
    wind, intensity = clamp(wind), clamp(intensity)
    covered = item in {'deluxe_nest', 'nest_premium', 'golden_nest'}
    exposure = .15 if covered else 1.
    # Separate snowfall and real wet freezing from the season's name. A winter
    # afternoon above freezing cannot paint frost onto a dry furnishing.
    s['snow'] = clamp(s['snow'] + minutes*(.025*intensity*exposure if weather in SNOW else -.002*max(0., temperature)))
    s['frost'] = clamp(s['frost'] + minutes*(.008*exposure if temperature <= 0 and (weather in WET | SNOW or obj.get('wetness', 0) > .2) else -.004*max(0., temperature)))
    loosening = 1-math.exp(-minutes*wind*.008)
    for key in ('left', 'right', 'braid'):
        s[key] *= 1-loosening
    s['plump'] += (.35-s['plump'])*(1-math.exp(-minutes*.002))
    s['groove'] *= math.exp(-minutes*wind*.006)
    if season == 'spring':s['petals'] = clamp(s['petals']+minutes*wind*.008*exposure)
    if season == 'fall':s['acorn'] = clamp(s['acorn']+minutes*wind*.004*exposure)
    # Windborne grit is finite bedding debris, never a collectible stone reward.
    s['grit'] = clamp(s['grit']+minutes*wind*.003*exposure)


def contacts(obj, routine, spec, previous, elapsed):
    """Apply each crossed contact exactly once, even after pause/save/large dt."""
    s = state(obj)
    events = spec.get('contacts', [])
    fired = routine.setdefault('contacts', [])
    for index, event in enumerate(events):
        at = event['at']*spec['duration']
        if index in fired or not previous < at <= elapsed:
            continue
        for key, amount in event.get('add', {}).items():s[key] = clamp(s[key]+amount)
        for key, value in event.get('set', {}).items():s[key] = clamp(value)
        for key, factor in event.get('multiply', {}).items():s[key] = clamp(s[key]*factor)
        fired.append(index)
        s['touches'] = min(999999, s['touches']+1)


def facts(obj):
    s = state(copy.deepcopy(obj))
    return dict(lining='fluffed' if s['plump']>.7 else 'pressed flat' if s['plump']<.3 else 'softly settled',
                hollow='deep' if s['hollow']>.65 else 'shallow',
                left_rim='tucked' if s['left']>.7 else 'loose',
                right_rim='tucked' if s['right']>.7 else 'loose',
                twig_brace=s['brace']>.5, repaired_gap=s['mend']>.5,
                feather='tucked into the lining' if s['feather']>.5 else 'loose at the edge',
                leaf='under the bedding' if s['leaf']>.5 else 'at the edge',
                pebble='beside the nest' if s['pebble']>.5 else 'in the lining',
                snow=round(s['snow'], 2), frost=round(s['frost'], 2),
                toe_groove=s['groove']>.5)
