"""Native state and timed contact work for the wonder machines and curiosities.

Every wonder owns bounded, saved fields (melt, pressure, rake pattern...). Weather
physics and contact effects are applied here only; the renderer reads them.
Routine choice follows actual weather, season, time, Cheese's age, needs, mood and
the object's own condition. Nothing here grants inventory, coins or rewards.
"""
import copy
import json
import math
import re
from pathlib import Path
from engine import shelters

DATA = Path(__file__).parent / 'client/animation'
ITEMS = json.loads((DATA / 'wonders.json').read_text())
ROUTINES = json.loads((DATA / 'wonder-routines.json').read_text())
# Measured from the drawn anchors and the D10 rig (scripts/export-wonder-reach.mjs):
# an age is offered a routine only if its wing, head or held tool reaches every contact.
REACH = {k: set(v['reachableAges']) for k, v in json.loads((DATA / 'wonder-reach.json').read_text())['routines'].items()}
LINES = json.loads((DATA / 'wonder-lines.json').read_text())
BY_ITEM = {}
for _key, _spec in ROUTINES.items():
    BY_ITEM.setdefault(_spec['item'], []).append(_key)

YOUNG = ('hatchling', 'duckling')
ELDER = ('mature', 'elder', 'legendary')
WET = ('rain', 'storm', 'shower', 'drizzle', 'sleet', 'snow', 'blizzard', 'hail')
COMPARE = re.compile(r'^([a-z_]+)(<=|>=|<|>)(-?[0-9.]+)$')
# Object-derived flags read from the object's own saved fields.
FLAGS = dict(powered=('power', .5), energized=('energy', .3), open=('aperture', .3), fielded=('field', .4), shielded=('shield', .5),
             tarp=('tarp', .5), oiled=('oil', .3), embered=('embers', .3), warm_egg=('warmth', .5), covered=('covered', .5), snow_on=('snow', .2))


def finite(v, d=0.):
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) else d


def state(item, obj):
    """Finite bounded fields; damaged saves fall back to authored defaults."""
    spec = ITEMS[item]
    s = obj.get('wonder')
    if not isinstance(s, dict):
        s = obj['wonder'] = {}
    for name, (default, low, high) in spec['fields'].items():
        s[name] = max(low, min(high, finite(s.get(name), default)))
    for name in [k for k in s if k not in spec['fields'] and k != 'history']:
        del s[name]
    if not isinstance(s.get('history'), dict):
        s['history'] = {}
    s['history'] = {k: int(max(0, min(9999, finite(v)))) for k, v in s['history'].items() if k in ROUTINES}
    return s


class World:
    """Detached view of the actual environment used by physics and choice."""

    def __init__(self, pond, outdoors=True, wet=None, temperature=None, wind=None, weather=None):
        self.weather = weather if weather is not None else getattr(pond, 'weather_type', 'sunny')
        self.wet = outdoors and (wet if wet is not None else any(w in self.weather for w in WET))
        eco = pond.state.get('ecology', {}) if hasattr(pond, 'state') else {}
        self.temperature = finite(temperature, finite(eco.get('temperature'), 15))
        self.wind = finite(wind, finite(eco.get('wind'), .1)) if outdoors else 0.
        self.hour = finite(getattr(pond, 'hour', 12), 12)
        self.season = str(getattr(pond, 'season', 'spring'))
        self.outdoors = outdoors

    def tag(self, name):
        h = self.hour
        return {
            'always': True, 'wet': self.wet, 'dry': not self.wet, 'snow': self.outdoors and any(w in self.weather for w in ('snow', 'blizzard')),
            'storm': self.outdoors and any(w in self.weather for w in ('storm', 'blizzard', 'gale', 'tornado', 'hurricane')),
            'windy': self.wind > .45, 'calm': self.wind < .25, 'warm': self.temperature > 2, 'cold': self.temperature <= 0,
            'sun': self.outdoors and 7 <= h < 18 and not self.wet and any(w in self.weather for w in ('sun', 'clear', 'heat', 'rainbow')),
            'night': h < 6 or h >= 20, 'day': 7 <= h < 18, 'dawn': 5 <= h < 8, 'dusk': 17 <= h < 20.5, 'night_late': h >= 22 or h < 5,
            'dawn_or_day': 5 <= h < 18, 'clear': not self.wet and not any(w in self.weather for w in ('fog', 'cloud', 'overcast', 'mist')),
            'rainbow_sky': 'rainbow' in self.weather, 'growing': self.season in ('spring', 'summer') and self.temperature > 2,
            'spring': self.season == 'spring', 'summer': self.season == 'summer', 'fall': self.season in ('fall', 'autumn'), 'winter': self.season == 'winter',
        }.get(name)


def condition(text, s, world, cheese=None):
    """'a&b&!c', comparisons on saved fields, world tags, object flags, and
    (for choice only) Cheese's age, needs and mood tags."""
    for token in text.split('&'):
        neg = token.startswith('!')
        token = token[1:] if neg else token
        m = COMPARE.match(token)
        if m:
            field, op, value = m.group(1), m.group(2), float(m.group(3))
            have = finite(s.get(field))
            ok = {'<': have < value, '>': have > value, '<=': have <= value, '>=': have >= value}[op]
        elif token in FLAGS:
            field, threshold = FLAGS[token]
            ok = finite(s.get(field)) > threshold
        elif token == 'dry_axle':
            ok = finite(s.get('oil')) < .25
        elif token == 'far_year':
            ok = int(finite(s.get('year'), 2026)) != 2026
        elif cheese is not None and token in cheese:
            ok = cheese[token]
        else:
            ok = world.tag(token)
            if ok is None:
                return False  # Unknown tags never pass silently.
        if bool(ok) == neg:
            return False
    return True


def apply(s, item, effect_rows):
    spec = ITEMS[item]['fields']
    for field, op, value in effect_rows:
        default, low, high = spec[field]
        old = finite(s.get(field), default)
        if op == 'set':
            new = value
        elif op == 'add':
            new = old + value
        elif op == 'mul':
            new = old * value
        elif op == 'max':
            new = max(old, value)
        elif op == 'min':
            new = min(old, value)
        elif op == 'wrap':
            span = high - low
            new = low + ((old - low + value) % span if span > 0 else 0)
        else:
            continue
        s[field] = max(low, min(high, new))


def update(pond, item, obj, dt, outdoors, wet=False, temperature=15, wind=.1, weather=None):
    """Weather and time physics. Stored wonders hold still; placed ones age."""
    if item not in ITEMS:
        return
    s = state(item, obj)
    dt = max(0., min(86400., finite(dt)))
    if not outdoors or dt <= 0:
        return
    world = World(pond, outdoors, wet, temperature, wind, weather)
    spec = ITEMS[item]
    # Rules interact (embers keep the egg warm, warmth drives incubation), so a
    # long catch-up interval is integrated in short slices: the outcome must not
    # depend on rule order or on how coarsely time was delivered.
    slices = max(1, min(2000, math.ceil(dt / 5.)))
    h = dt / slices
    for _ in range(slices):
        for field, op, value, when in spec['physics']:
            if not condition(when, s, world):
                continue
            default, low, high = spec['fields'][field]
            if op == 'rate':
                s[field] = max(low, min(high, s[field] + value * h))
            elif op == 'decay':
                s[field] = value + (s[field] - value) * math.exp(-h * .05)
                s[field] = max(low, min(high, s[field]))
            elif op == 'wrap':
                apply(s, item, [[field, 'wrap', value * h]])
        for when, rows in spec['triggers']:
            if condition(when, s, world):
                apply(s, item, rows)


def cheese_context(pond):
    g = pond.game
    duck = g.duck
    n = duck.needs
    age = duck.growth_stage
    try:
        mood = duck.get_mood_state().value
    except Exception:
        mood = 'content'
    traits = getattr(duck, 'personality', {}) or {}
    return dict(young=age in YOUNG, grown=age not in YOUNG, elder=age in ELDER, tired=n.energy < 35, lonely=n.social < 40,
                sad=mood in ('sad', 'miserable', 'dramatic') or n.fun < 30, happy=mood in ('ecstatic', 'happy'),
                grumpy=mood in ('grumpy', 'petty'), curious=finite(traits.get('brave_timid')) >= 0 or finite(traits.get('clever_derpy')) > 15)


def eligible(pond, item, obj, world=None, cheese=None):
    """Routines whose every condition holds for this exact object now."""
    s = state(item, obj)
    world = world or World(pond)
    cheese = cheese if cheese is not None else cheese_context(pond)
    age = pond.game.duck.growth_stage
    storm = world.tag('storm')
    out = []
    for key in BY_ITEM.get(item, ()):
        spec = ROUTINES[key]
        if spec['ages'] and age not in spec['ages']:
            continue
        if age not in REACH.get(key, ()):
            continue
        if storm and not sheltering(item, key):
            continue
        if all(condition(w, s, world, cheese) for w in spec['when']):
            out.append(key)
    return out


def appeal(pond, item, obj, key):
    """Score one eligible routine: matching context, the object's own needs, and
    novelty. Deterministic for a given saved state and clock."""
    s = state(item, obj)
    world = World(pond)
    cheese = cheese_context(pond)
    spec = ROUTINES[key]
    score = 10 + 9 * sum(condition(p, s, world, cheese) for p in spec['prefer'])
    # A routine gated on the actual context (rain, night, a melting swan...) is
    # more fitting right now than one that could happen any time.
    for token in spec['when']:
        name = token.lstrip('!')
        if COMPARE.match(name) or name in FLAGS or name in ('dry_axle', 'far_year'):
            score += 4
        elif not token.startswith('!'):
            score += 6
    score -= 4 * min(5, s['history'].get(key, 0))
    if world.wet and sheltering(item, key):
        score += 40  # Rain: a reachable dome, booth or hedge becomes a shelter.
    return score


def choose(pond, item, ref):
    obj = pond.object_state(item, ref)
    keys = eligible(pond, item, obj)
    if not keys:
        return None
    clock = int(finite(pond.state.get('elapsed')) / 40)
    best = max(keys, key=lambda k: (appeal(pond, item, obj, k), (hash_text(k) + clock) % 97))
    return make(pond, best)


def hash_text(text):
    v = 7
    for c in text:
        v = (v * 31 + ord(c)) & 0xffffffff
    return v


def make(pond, key):
    pos = pond.game.renderer.duck_pos
    spec = ROUTINES[key]
    return dict(id=key, elapsed=0., done=False, events=[], origin=[pos.x, pos.y], label=spec['label'], say=spec.get('say'))


def sheltering(item, key):
    """A long, tool-free routine on a roofed or domed wonder keeps Cheese dry."""
    spec = ROUTINES[key]
    return ITEMS[item]['shelter'] and spec['tool'] in ('none', 'wing') and 'wet' in spec['when'] and spec['duration'] >= 30


def blocked(pond, item, key=None):
    """Plain-language refusal for an unavailable routine, or None."""
    if key is not None and key not in BY_ITEM.get(item, ()):
        return 'Choose something to do with this wonder.'
    if World(pond).tag('storm') and (key is None or not sheltering(item, key)):
        return 'Cheese leaves the machinery alone until the storm passes.'
    return None


def best(pond, item, obj):
    """(routine, appeal, reason) for autonomous choice, or None."""
    keys = eligible(pond, item, obj)
    if not keys:
        return None
    scored = sorted(((appeal(pond, item, obj, k), k) for k in keys), reverse=True)
    score, key = scored[0]
    world = World(pond)
    reason = 'a dry spot under the ' + item.replace('_', ' ') if world.wet and sheltering(item, key) else \
        'the ' + item.replace('_', ' ') + ' needs looking after' if ROUTINES[key]['events'] and score >= 19 else \
        'the ' + item.replace('_', ' ') + ' is a wonder worth a visit'
    return key, score, reason


def valid(pond, plan):
    item = plan['target']
    work = plan.get('wonder_work', {})
    if item not in ITEMS or item not in pond.owned or work.get('id') not in ROUTINES or ROUTINES[work['id']]['item'] != item:
        return False
    if pond.object_state(item, plan) is None:
        return False
    if not plan.get('instance'):
        return False
    if World(pond).tag('storm') and not sheltering(item, work['id']):
        return False  # A storm arriving mid-routine interrupts work on machinery.
    return shelters.still_placed(pond, dict(id=item, instance=plan['instance'], destination=plan.get('destination')))


def pose_value(work, name, default=0.):
    """Native copy of the renderer's smoothstep track sampling for one part."""
    spec = ROUTINES[work['id']]
    progress = max(0., min(1., work['elapsed'] / spec['duration']))
    track = spec['track']
    a, b = track[0], track[-1]
    for i in range(1, len(track)):
        if progress <= track[i][0]:
            a, b = track[i - 1], track[i]
            break
    u = max(0., min(1., (progress - a[0]) / max(.001, b[0] - a[0])))
    u = u * u * (3 - 2 * u)
    va, vb = a[1].get(name, default), b[1].get(name, default)
    return va + (vb - va) * u


def advance(pond, plan, dt):
    work = plan.get('wonder_work')
    if not work or work.get('done') or plan['phase'] != 'act':
        return False
    if not valid(pond, plan):
        work.update(interrupted=True, done=True)
        return False
    pos = pond.game.renderer.duck_pos
    destination = plan.get('destination', work['origin'])
    if abs(pos.x - destination[0]) + abs(pos.y - destination[1]) > 3:
        work.update(interrupted=True, done=True)
        return False
    spec = ROUTINES[work['id']]
    work['elapsed'] = min(spec['duration'], work['elapsed'] + max(0., finite(dt)))
    obj = pond.object_state(plan['target'], plan)
    s = state(plan['target'], obj)
    for i, (at, name) in enumerate(spec['events']):
        if work['elapsed'] < at * spec['duration'] or i in work['events']:
            continue
        work['events'].append(i)
        apply(s, plan['target'], ITEMS[plan['target']]['effects'][name])
    first_moment = work['events'] if spec['events'] else work['elapsed'] >= spec['duration'] * .35
    if spec.get('say') in LINES and first_moment and not work.get('said'):
        work['said'] = True
        say(pond, LINES[spec['say']][s['history'].get(work['id'], 0) % len(LINES[spec['say']])])
    work['done'] = work['elapsed'] >= spec['duration']
    pond._cache = None
    return not work['done']


def say(pond, line):
    """Cheese says an authored line aloud: chat log (bottom left) and speech
    bubble. Not a conversation memory; never censored."""
    minds = getattr(pond, 'minds', None)
    if not minds or pond.game.duck.growth_stage == 'egg':
        return
    minds.utterances['cheese'] = {'text': line, 'until': minds.now + 8}
    chat = getattr(pond.game.renderer, 'chat', None)
    if chat is not None:
        from datetime import datetime
        chat.reply('cheese', minds.model.residents.get('cheese', {}).get('name', 'Cheese'), 'player', line, 'say', 'authored', datetime.now().strftime('%H:%M'))
    pond._cache = None


def complete(pond, plan):
    work = plan.get('wonder_work')
    if not work or not work.get('done') or work.get('interrupted') or work.get('recorded') or not valid(pond, plan):
        return
    spec = ROUTINES[work['id']]
    if len(work['events']) != len(spec['events']):
        return  # Every authored contact must actually have happened.
    work['recorded'] = True
    obj = pond.object_state(plan['target'], plan)
    s = state(plan['target'], obj)
    s['history'][work['id']] = min(9999, s['history'].get(work['id'], 0) + 1)
    pond.remember('wonder', spec['label'] + '.', .5, plan['target'])


def request(pond, item, choice, instance=None):
    if not isinstance(item, str) or not isinstance(choice, str) or item not in ITEMS or choice not in BY_ITEM.get(item, ()):
        return False, 'Choose something to do with this wonder.'
    reason = blocked(pond, item, choice)
    if reason:
        return False, reason
    target = instance or next((p.instance for p in pond.placements if p.item_id == item), None)
    if not target:
        return False, 'Place that wonder outside first.'
    obj = pond.object_state(item, target)
    if obj is None:
        return False, 'Place that wonder outside first.'
    if choice not in eligible(pond, item, obj):
        spec = ROUTINES[choice]
        if spec['ages'] and pond.game.duck.growth_stage not in spec['ages']:
            return False, 'Cheese is a bit too little for that one yet.' if pond.game.duck.growth_stage in YOUNG else 'That one is for little Cheese.'
        if pond.game.duck.growth_stage not in REACH.get(choice, ()):
            return False, 'Cheese can\'t reach that part from the ground yet.'
        return False, 'That doesn\'t make sense right now: ' + spec['label'].lower() + ' needs different weather, time or condition.'
    ok, message = pond.start('item', item, instance=target)
    if not ok:
        return ok, message
    plan = pond.state['plan']
    plan['wonder_work'] = make(pond, choice)
    plan['label'] = ROUTINES[choice]['label']
    pond._cache = None
    return True, ROUTINES[choice]['label']


def conversation(pond, plan):
    """Read-only facts for speech about the exact wonder Cheese is using."""
    if not plan or not plan.get('wonder_work') or not valid(pond, plan):
        return None
    item = plan['target']
    s = copy.deepcopy(pond.object_state(item, plan).get('wonder', {}))
    s.pop('history', None)
    spec = ROUTINES[plan['wonder_work']['id']]
    return dict(object=item.replace('_', ' '), activity=spec['label'], phase=plan['phase'], paused=bool(plan.get('paused')),
                cue=spec.get('say'), state={k: (round(v, 2) if isinstance(v, float) else v) for k, v in s.items()},
                note='Decorative wonder with real saved state; it never grants items, coins or rewards.')


def summary(item, obj):
    s = state(item, obj)
    shown = [k for k in ITEMS[item]['fields'] if not k.endswith('s') or k in ('towers', 'ribbons', 'floaters', 'feathers', 'wishes')]
    return ', '.join(f'{k} {round(s[k], 2) if isinstance(s[k], float) else s[k]}' for k in shown[:4])
