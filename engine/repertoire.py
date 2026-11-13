"""Repertoire engine: data-authored, physically checked sequences for any object.

One file per object in client/animation/repertoire/<object>.json (see
overhaul/animation-milestone/repertoire-engine.md). Shares the rule language, world
view and Cheese context with wonders.py. Native code applies every contact effect;
the renderer only reads. Never grants items or coins; never consumes inventory.
Hosts: placed (the object itself), portable (owned inventory object set down),
keeping (a kept fish of this species in a koi pond / sea tank).
"""
import copy
import json
import math
from pathlib import Path
from engine import shelters
from engine.wonders import World, condition, cheese_context, hash_text, finite, COMPARE, YOUNG, ELDER

DIR = Path(__file__).parent / 'client/animation/repertoire'
OBJECTS = {}
ROUTINES = {}
LOAD_ERRORS = []   # a broken file is skipped and reported, never breaks the game
TOOLS = ('none', 'wing', 'twig', 'reed')
OBJ_STATE = ('dirt', 'wetness', 'condition')   # real drawn object state effects may change
_NEEDS_OK = ('fun', 'social', 'energy', 'cleanliness')


def _validate(d):
    assert isinstance(d.get('object'), str) and d.get('host') in ('placed', 'portable', 'keeping', 'display', 'wearable'), 'object/host'
    fields = d.get('fields', {})
    for name, rows in d.get('effects', {}).items():
        for t, op, v in rows:
            assert op in ('set', 'add', 'mul', 'max', 'min', 'wrap'), name + ' op'
            ok = t in fields or (t.startswith('need.') and t[5:] in _NEEDS_OK and op == 'add') or (t.startswith('obj.') and t[4:] in OBJ_STATE) \
                or (d['host'] == 'keeping' and (t.startswith('subject.') or t.startswith('keeping.')))
            assert ok, name + ' target ' + t
    for k, r in d['routines'].items():
        for key in ('label', 'duration', 'track', 'events', 'when', 'prefer', 'tool'):
            assert key in r, k + ' missing ' + key
        assert r['tool'] in TOOLS, k + ' tool ' + r['tool']
        assert all(e[1] in d['effects'] for e in r['events']), k + ' event effect'


for _f in sorted(DIR.glob('*.json')) if DIR.exists() else []:
    try:
        _d = json.loads(_f.read_text())
        _validate(_d)
        assert not any(_k in ROUTINES for _k in _d['routines']), 'duplicate routine id'
    except Exception as _e:
        LOAD_ERRORS.append(_f.name + ': ' + str(_e))
        continue
    OBJECTS[_d['object']] = _d
    for _k, _r in _d['routines'].items():
        ROUTINES[_k] = dict(_r, object=_d['object'])
_REACH_FILE = Path(__file__).parent / 'client/animation/repertoire-reach.json'
REACH = {k: set(v['reachableAges']) for k, v in json.loads(_REACH_FILE.read_text())['routines'].items()} if _REACH_FILE.exists() else {}
CHEESE_TAGS = ('young', 'grown', 'elder', 'tired', 'lonely', 'sad', 'happy', 'grumpy', 'curious')
NEEDS = ('energy', 'fun', 'social', 'hunger', 'cleanliness')


_QUEUE = Path(__file__).parent / 'overhaul/animation-milestone/work-queue.json'
QUEUE = {o['id']: o for o in json.loads((Path(__file__).parent / 'overhaul/animation-milestone/work-queue.json').read_text())['objects']}
DISPLAYABLE = frozenset(o['id'] for o in json.loads(_QUEUE.read_text())['objects'] if o['host'] == 'display') if _QUEUE.exists() else frozenset()


def displayable():
    return set(DISPLAYABLE)


BY_OBJECT = {}
for _k, _r in ROUTINES.items():
    BY_OBJECT.setdefault(_r['object'], []).append(_k)


def by_object(obj_id):
    return BY_OBJECT.get(obj_id, [])


def need(obj_id):
    """Repertoire sequences an object owes: 48 less the distinct family routines it already has (wonders)."""
    return max(0, 48 - QUEUE.get(obj_id, {}).get('wonder_routines', 0))


def state(oid, obj):
    spec = OBJECTS[oid]
    root = obj.get('rep')
    if not isinstance(root, dict):
        root = obj['rep'] = {}
    s = root.get(oid)
    if not isinstance(s, dict):
        s = root[oid] = {}
    for name, (d, lo, hi) in spec.get('fields', {}).items():
        s[name] = max(lo, min(hi, finite(s.get(name), d)))
    for name in [k for k in s if k not in spec.get('fields', {}) and k != 'history']:
        del s[name]
    h = s.get('history') if isinstance(s.get('history'), dict) else {}
    s['history'] = {k: int(max(0, min(9999, finite(v)))) for k, v in h.items() if k in ROUTINES}
    return s


def apply(s, oid, rows, pond=None, subject=None, host=None, objstate=None):
    fields = OBJECTS[oid].get('fields', {})
    for target, op, value in rows:
        if target.startswith('need.'):
            need = target[5:]
            if pond is not None and need in NEEDS and op == 'add':
                pond.change_need(need, float(value))
            continue
        if target.startswith('obj.'):
            if objstate is None or target[4:] not in OBJ_STATE:
                continue
            store, key, bounds = objstate, target[4:], (0., 1.)
            if key == 'condition':
                store.setdefault('condition', 1.)
        elif target.startswith('keeping.'):
            from engine import keeping
            key = target[8:]
            if host is None or key not in keeping.POND:
                continue
            store, bounds = host, keeping.POND[key][1:]
        elif target.startswith('subject.'):
            if subject is None:
                continue
            store, key, bounds = subject, target[8:], (0., 1.)
            if key not in store or key in ('id', 'species', 'catch', 'name', 'size'):
                continue
        else:
            if target not in fields:
                continue
            store, key, bounds = s, target, fields[target][1:]
        lo, hi = bounds
        if target.startswith('keeping.'):
            key = target[8:]
        old = finite(store.get(key), 1. if key == 'condition' else 0.)
        new = {'set': value, 'add': old + value, 'mul': old * value, 'max': max(old, value), 'min': min(old, value)}.get(op)
        if op == 'wrap':
            span = hi - lo
            new = lo + ((old - lo + value) % span if span > 0 else 0)
        if new is not None:
            store[key] = max(lo, min(hi, new))


def update(pond, item, obj, dt, outdoors, wet=False, temperature=15, wind=.1, weather=None):
    """Physics for every repertoire object whose state lives on this object."""
    root = obj.get('rep') if isinstance(obj, dict) else None
    if not isinstance(root, dict) or not outdoors:
        return
    dt = max(0., min(86400., finite(dt)))
    if dt <= 0:
        return
    world = World(pond, outdoors, wet, temperature, wind, weather)
    for oid in list(root):
        if oid not in OBJECTS:
            continue
        spec = OBJECTS[oid]
        if not spec.get('physics') and not spec.get('triggers'):
            continue
        s = state(oid, obj)
        slices = max(1, min(2000, math.ceil(dt / 5.)))
        h = dt / slices
        for _ in range(slices):
            for field, op, value, when in spec.get('physics', []):
                if field not in spec['fields'] or not condition(when, s, world):
                    continue
                d, lo, hi = spec['fields'][field]
                if op == 'rate':
                    s[field] = max(lo, min(hi, s[field] + value * h))
                elif op == 'decay':
                    s[field] = max(lo, min(hi, value + (s[field] - value) * math.exp(-h * .05)))
                elif op == 'wrap':
                    apply(s, oid, [[field, 'wrap', value * h]])
            for when, rows in spec.get('triggers', []):
                if condition(when, s, world):
                    apply(s, oid, rows)


# ---------------------------------------------------------------- hosts
def host_of(pond, oid, instance=None):
    """(host item, instance, subject or None) where this object can be worked now."""
    spec = OBJECTS[oid]
    kind = spec.get('host', 'placed')
    if kind == 'placed':
        for p in pond.placements:
            if p.item_id == oid and (instance is None or p.instance == instance):
                return oid, p.instance, None
        # Garden beds and community works stand on the ground as installations.
        for p in pond.grounds.installations():
            if p['id'] == oid and (instance is None or p['instance'] == instance):
                return oid, p['instance'], None
        return None
    if kind == 'portable':
        return (oid, None, None) if oid in pond.owned else None
    if kind == 'wearable':
        return (oid, None, None) if worn(pond, oid) else None
    if kind == 'display':
        from engine import display
        where = display.shown_anywhere(pond).get(oid)
        if where and (instance is None or where[1] == instance):
            return where[0], where[1], None
        return None
    if kind == 'keeping':
        from engine import keeping
        for p in pond.placements:
            if p.item_id not in keeping.HOSTS or (instance is not None and p.instance != instance):
                continue
            k = keeping.state(pond.object_state(p.item_id, p.instance))
            fish = [f for f in k['fish'] if f['species'] == oid]
            if fish:
                return p.item_id, p.instance, fish
        return None
    return None


def worn(pond, oid):
    """Wearable routines are about the thing on Cheese's body: it must be worn."""
    g = pond.game
    on = set((getattr(g.habitat, 'equipped_cosmetics', {}) or {}).values())
    eq = getattr(getattr(g, 'outfits', None), 'current_outfit', None)
    if eq is not None:
        on |= {v for v in vars(eq).values() if isinstance(v, str)}
    return oid in on


def subject_of(pond, work, plan):
    if not work.get('subject'):
        return None
    from engine import keeping
    obj = pond.object_state(plan['target'], plan)
    if obj is None:
        return None
    return next((f for f in keeping.state(obj)['fish'] if f['id'] == work['subject']), None)


def store(pond, plan, work):
    """The object state dict holding this repertoire object's fields."""
    if OBJECTS.get(work.get('object'), {}).get('host') == 'wearable':
        objs = pond.state['objects']
        if not isinstance(objs.get(work['object']), dict):
            objs[work['object']] = {}
        return objs[work['object']]
    return pond.object_state(plan['target'], plan)


# ---------------------------------------------------------------- choice
def view(oid, obj):
    """Fields conditions may read: the object's own, plus fish_<f> (best kept fish of
    this species) and pond_<f> (keeping pond) for keeping objects."""
    s = state(oid, obj)
    # Gates may read the object's real drawn wear (obj_dirt, obj_wetness, obj_condition).
    v = dict(s)
    v.update({'obj_' + k: finite(obj.get(k), 1. if k == 'condition' else 0.) for k in OBJ_STATE})
    v['history'] = s['history']
    if OBJECTS[oid].get('host') != 'keeping':
        return v
    from engine import keeping
    k = keeping.state(obj)
    v.update({'pond_' + f: k[f] for f in keeping.POND})
    fish = [f for f in k['fish'] if f['species'] == oid]
    for f in keeping.FISH:
        v['fish_' + f] = max((x[f] for x in fish), default=0.)
    v['fish_count'] = float(len(fish))
    return v


def eligible(pond, oid, obj, world=None, cheese=None):
    s = view(oid, obj)
    world = world or World(pond)
    cheese = cheese if cheese is not None else cheese_context(pond)
    age = pond.game.duck.growth_stage
    storm = world.tag('storm')
    out = []
    for key in by_object(oid):
        r = ROUTINES[key]
        if r.get('ages') and age not in r['ages']:
            continue
        if REACH and age not in REACH.get(key, ()):
            continue
        if storm and not (r['tool'] == 'none' and 'wet' in r['when'] and r['duration'] >= 30):
            continue
        if all(condition(w, s, world, cheese) for w in r['when']):
            out.append(key)
    return out


def appeal(pond, oid, obj, key, world=None, cheese=None, s=None, low=None):
    s = s or view(oid, obj)
    world = world or World(pond)
    cheese = cheese if cheese is not None else cheese_context(pond)
    r = ROUTINES[key]
    score = 10 + 9 * sum(condition(p, s, world, cheese) for p in r['prefer'])
    for token in r['when']:
        name = token.lstrip('!')
        score += 4 if COMPARE.match(name) else 0 if token.startswith('!') else 6
    # Least-used rotation: the novelty penalty is relative and uncapped, so gated
    # favourites cannot strand the rest of the 48.
    if low is None:
        low = min([s['history'].get(k, 0) for k in by_object(oid)] or [0])
    score -= 12 * (s['history'].get(key, 0) - low)
    return score


def best(pond, oid, obj, world=None, cheese=None):
    world = world or World(pond)
    cheese = cheese if cheese is not None else cheese_context(pond)
    keys = eligible(pond, oid, obj, world, cheese)
    if not keys:
        return None
    s = view(oid, obj)
    low = min([s['history'].get(k, 0) for k in by_object(oid)] or [0])
    clock = int(finite(pond.state.get('elapsed')) / 40)
    scored = {k: appeal(pond, oid, obj, k, world, cheese, s, low) for k in keys}
    key = max(keys, key=lambda k: (scored[k], (hash_text(k) + clock) % 97))
    return key, scored[key]


def make(pond, key, subject=None):
    pos = pond.game.renderer.duck_pos
    r = ROUTINES[key]
    return dict(id=key, object=r['object'], elapsed=0., done=False, events=[], origin=[pos.x, pos.y], label=r['label'],
                subject=subject, said=False)


# ---------------------------------------------------------------- lifecycle
def valid(pond, plan):
    work = plan.get('rep_work') or {}
    key = work.get('id')
    if key not in ROUTINES or ROUTINES[key]['object'] != work.get('object'):
        return False
    oid = work['object']
    kind = OBJECTS[oid].get('host', 'placed')
    target = plan['target']
    if kind == 'portable':
        if oid not in pond.owned:
            return False
    elif kind == 'wearable':
        if not worn(pond, oid):
            return False  # taken off mid-routine
    elif target not in pond.owned or not plan.get('instance'):
        return False
    if store(pond, plan, work) is None:
        return False
    if kind == 'keeping' and subject_of(pond, work, plan) is None:
        return False
    if kind == 'display' and host_of(pond, oid, plan.get('instance')) is None:
        return False  # taken down or no longer owned
    if World(pond).tag('storm') and not (ROUTINES[key]['tool'] == 'none' and 'wet' in ROUTINES[key]['when']):
        return False
    if plan.get('instance'):
        return shelters.still_placed(pond, dict(id=target, instance=plan['instance'], destination=plan.get('destination')))
    return True


def advance(pond, plan, dt):
    work = plan.get('rep_work')
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
    r = ROUTINES[work['id']]
    oid = work['object']
    work['elapsed'] = min(r['duration'], work['elapsed'] + max(0., finite(dt)))
    obj = store(pond, plan, work)
    s = state(oid, obj)
    subject = subject_of(pond, work, plan)
    from engine import keeping
    host = keeping.state(obj) if OBJECTS[oid].get('host') == 'keeping' else None
    effects = OBJECTS[oid]['effects']
    for i, (at, name) in enumerate(r['events']):
        if work['elapsed'] >= at * r['duration'] and i not in work['events']:
            work['events'].append(i)
            apply(s, oid, effects[name], pond, subject, host, obj)
    first = work['events'] if r['events'] else work['elapsed'] >= r['duration'] * .35
    if r.get('say') and first and not work.get('said'):
        work['said'] = True
        lines = OBJECTS[oid].get('lines', {}).get(r['say'])
        if lines:
            from engine import wonders
            wonders.say(pond, lines[s['history'].get(work['id'], 0) % len(lines)])
    work['done'] = work['elapsed'] >= r['duration']
    pond._cache = None
    return not work['done']


def choices(pond):
    """Autonomous candidates: (target, instance, score, reason, routine, subject)."""
    out = []
    world, cheese = World(pond), cheese_context(pond)
    for oid, spec in OBJECTS.items():
        host = host_of(pond, oid)
        if host is None:
            continue
        item, inst, fish = host
        if OBJECTS[oid].get('host') == 'wearable':
            obj = pond.state['objects'].get(oid)
        else:
            obj = pond.object_state(item, inst)
        if obj is None:
            if OBJECTS[oid].get('host') not in ('portable', 'wearable'):
                continue
            obj = {}  # never used yet: score with fresh state; starting the routine creates the real record
        if pond.state['elapsed'] - obj.get('last_use', -1e9) < 120:
            continue
        pick = best(pond, oid, obj, world, cheese)
        if not pick:
            continue
        subject = max(fish, key=lambda x: x['hunger'])['id'] if fish else None
        out.append((item, inst, pick[1], 'the ' + oid.replace('_', ' ') + ' could use some attention', pick[0], subject))
    return out


def complete(pond, plan):
    work = plan.get('rep_work')
    if not work or not work.get('done') or work.get('interrupted') or work.get('recorded') or not valid(pond, plan):
        return
    r = ROUTINES[work['id']]
    if len(work['events']) != len(r['events']):
        return
    work['recorded'] = True
    s = state(work['object'], store(pond, plan, work))
    s['history'][work['id']] = min(9999, s['history'].get(work['id'], 0) + 1)
    pond.remember('repertoire', r['label'] + '.', .5, work['object'])


def request(pond, oid, choice, instance=None):
    if oid not in OBJECTS or choice not in ROUTINES or ROUTINES[choice]['object'] != oid:
        return False, 'Choose something to do with that.'
    host = host_of(pond, oid, instance)
    if host is None:
        kind = OBJECTS[oid].get('host', 'placed')
        return False, {'placed': 'Place it outside first.', 'portable': 'Cheese does not have one.',
                       'keeping': 'Keep one in a koi pond or sea tank first.', 'wearable': 'Cheese needs to be wearing it first.', 'display': 'Put it on display in a trophy case or cabinet first.'}.get(kind, 'Not available right now.')
    item, inst, fish = host
    obj = pond.object_state(item, inst)
    if obj is None:
        return False, 'Place it outside first.'
    if choice not in eligible(pond, oid, obj):
        r = ROUTINES[choice]
        age = pond.game.duck.growth_stage
        if r.get('ages') and age not in r['ages']:
            return False, 'Cheese is a bit too little for that one yet.' if age in YOUNG else 'That one is for little Cheese.'
        if REACH and age not in REACH.get(choice, ()):
            return False, "Cheese can't reach that part from the ground yet."
        return False, "That doesn't make sense right now: " + r['label'].lower() + ' needs different weather, time or condition.'
    subject = None
    if fish:
        pick = ROUTINES[choice].get('pick', 'hungriest')
        f = max(fish, key=lambda x: x['hunger']) if pick == 'hungriest' else min(fish, key=lambda x: x['trust']) if pick == 'shyest' else fish[0]
        subject = f['id']
    ok, message = pond.start('item', item, instance=inst, rep_work=make(pond, choice, subject))
    if not ok:
        return ok, message
    return True, ROUTINES[choice]['label']


def conversation(pond, plan):
    if not plan or not plan.get('rep_work') or not valid(pond, plan):
        return None
    work = plan['rep_work']
    s = copy.deepcopy(state(work['object'], store(pond, plan, work)))
    s.pop('history', None)
    return dict(object=work['object'].replace('_', ' '), activity=ROUTINES[work['id']]['label'], phase=plan['phase'],
                state={k: (round(v, 2) if isinstance(v, float) else v) for k, v in s.items()},
                note='Real saved object state; repertoire routines never grant items, coins or rewards.')
