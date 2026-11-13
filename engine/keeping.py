"""Keeping pond: real caught fish living in a placed koi_pond.

Every kept fish is exactly one real catch record from g.fishing.fish_caught, and a
catch can be kept at most once (released fish return to the wild and cannot be
kept again). Nothing here creates catches, coins or items. Physics run on an hours
scale like the wonders. See overhaul/animation-milestone/keeping-pond-design.md.
"""
import math

HOSTS = {'koi_pond': dict(capacity=320., water='fresh', setup=False),
         # User decision 2026-11-13: a big pool can be set up as a deep saltwater sea tank.
         'pool_large': dict(capacity=800., water='sea', setup=True), 'infinity_pool': dict(capacity=1000., water='sea', setup=True)}
# Freshwater species that physically fit a koi pond, with behaviour traits.
SPECIES = {
    'minnow': dict(active=('any',), dwell='top', school=True, jumpy=.2, whiskers=False, glow=None),
    'goldfish': dict(active=('morning', 'afternoon'), dwell='top', school=False, jumpy=.1, whiskers=False, glow=None),
    'carp': dict(active=('any',), dwell='bottom', school=False, jumpy=.2, whiskers=True, glow=None),
    'bass': dict(active=('morning', 'evening'), dwell='middle', school=False, jumpy=.7, whiskers=False, glow=None),
    'catfish': dict(active=('evening', 'night'), dwell='bottom', school=False, jumpy=.1, whiskers=True, glow=None),
    'trout': dict(active=('morning',), dwell='middle', school=False, jumpy=.8, whiskers=False, glow=None),
    'koi': dict(active=('morning', 'evening'), dwell='top', school=False, jumpy=.2, whiskers=True, glow=None),
    'salmon': dict(active=('morning', 'evening'), dwell='middle', school=False, jumpy=.9, whiskers=False, glow=None),
    'golden_koi': dict(active=('morning',), dwell='top', school=False, jumpy=.2, whiskers=True, glow='dawn'),
    'ghost_fish': dict(active=('night',), dwell='middle', school=False, jumpy=.1, whiskers=False, glow='night'),
}
SEA = {
    'pufferfish': dict(active=('any',), dwell='middle', school=False, jumpy=.1, whiskers=False, glow=None, puffs=True),
    'swordfish': dict(active=('morning', 'evening'), dwell='top', school=False, jumpy=.9, whiskers=False, glow=None),
    'sturgeon': dict(active=('night',), dwell='bottom', school=False, jumpy=.3, whiskers=True, glow=None),
    'ancient_dragon_fish': dict(active=('night',), dwell='middle', school=False, jumpy=.2, whiskers=True, glow='night'),
}
WATER = {**{k: 'fresh' for k in SPECIES}, **{k: 'sea' for k in SEA}}
TRAITS = {**SPECIES, **SEA}
CANNOT = {'pufferfish': 'needs salt water: set up a big pool as a sea tank', 'swordfish': 'too big for a koi pond: set up a big pool as a sea tank',
          'sturgeon': 'too big for a koi pond: set up a big pool as a sea tank', 'ancient_dragon_fish': 'too big for a koi pond: set up a big pool as a sea tank'}
POND = dict(clarity=(.8, 0, 1), algae=(.1, 0, 1), leaves=(0, 0, 1), ice=(0, 0, 1), oxygen=(.9, 0, 1), plants=(.4, 0, 1), flakes=(0, 0, 1), bell=(0, 0, 1))
FISH = dict(hunger=(.3, 0, 1), mood=(.6, 0, 1), health=(.9, 0, 1), trust=(.1, 0, 1), growth=(0, 0, 1))


def finite(v, d=0.):
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) else d


def state(obj):
    k = obj.get('keeping')
    if not isinstance(k, dict):
        k = obj['keeping'] = {}
    for f, (d, lo, hi) in POND.items():
        k[f] = max(lo, min(hi, finite(k.get(f), d)))
    fish = []
    for f in k.get('fish', []) if isinstance(k.get('fish'), list) else []:
        if not isinstance(f, dict) or f.get('species') not in TRAITS or not isinstance(f.get('catch'), str):
            continue
        for name, (d, lo, hi) in FISH.items():
            f[name] = max(lo, min(hi, finite(f.get(name), d)))
        f['size'] = max(1., min(500., finite(f.get('size'), 10.)))
        f['name'] = str(f.get('name') or '')[:24]
        f['id'] = str(f.get('id') or f['species'] + '@' + f['catch'])
        fish.append(f)
    k['fish'] = fish
    k['setup'] = bool(k.get('setup'))
    return k


def ledger(pond):
    """Catch keys ('species@caught_at') ever kept, and whether still kept."""
    led = pond.state.get('kept_catches')
    if not isinstance(led, dict):
        led = pond.state['kept_catches'] = {}
    return led


def catches(pond, species):
    return list(getattr(pond.game.fishing, 'fish_caught', {}).get(species, []))


def keepable(pond):
    """Real catch records that could move into a keeping pond now."""
    led = ledger(pond)
    out = []
    for species in TRAITS:
        for c in catches(pond, species):
            key = species + '@' + c.caught_at
            if key not in led:
                out.append(dict(species=species, catch=c.caught_at, size=float(c.size), record=bool(c.is_record), water=WATER[species]))
    return out


def used(k):
    return sum(f['size'] for f in k['fish'])


def keep(pond, item, instance, species, caught_at):
    if item not in HOSTS:
        return False, 'Only a koi pond or a sea tank can keep fish.'
    if species not in TRAITS:
        return False, 'That is not a fish Cheese has caught.'
    host = HOSTS[item]
    if WATER[species] != host['water']:
        return False, ('A ' + species.replace('_', ' ') + ' cannot live in a koi pond: ' + CANNOT[species] + '.') if host['water'] == 'fresh' \
            else 'A sea tank is salt water; the ' + species.replace('_', ' ') + ' needs the koi pond.'
    obj = pond.object_state(item, instance)
    if obj is None or not any(p.instance == instance and p.item_id == item for p in pond.placements):
        return False, 'Place it outside first.'
    if host['setup'] and not state(obj)['setup']:
        return False, 'Set this pool up as a sea tank first.'
    catch = next((c for c in catches(pond, species) if c.caught_at == caught_at), None)
    if catch is None:
        return False, 'There is no such catch in the fishing record.'
    key = species + '@' + caught_at
    led = ledger(pond)
    if key in led:
        return False, 'That catch was already ' + led[key] + '.'
    k = state(obj)
    if used(k) + float(catch.size) > HOSTS[item]['capacity']:
        return False, 'The koi pond is too full for another ' + str(catch.size) + ' cm fish.'
    k['fish'].append(dict(id=key, species=species, catch=caught_at, size=float(catch.size), name='', hunger=.4, mood=.4, health=.85, trust=0., growth=0.))
    led[key] = 'kept'
    home = 'koi pond' if item == 'koi_pond' else 'sea tank'
    pond.remember('keeping', 'A ' + species.replace('_', ' ') + ' (' + str(catch.size) + ' cm) came home to the ' + home + '.', .5, item)
    pond._cache = None
    return True, 'The ' + species.replace('_', ' ') + ' slips into the ' + home + '.'


def setup(pond, item, instance, on):
    """Turn a big pool into a sea tank (or back, only when empty)."""
    if item not in HOSTS or not HOSTS[item]['setup']:
        return False, 'Only a large pool or an infinity pool can become a sea tank.'
    obj = pond.object_state(item, instance)
    if obj is None or not any(p.instance == instance and p.item_id == item for p in pond.placements):
        return False, 'Place the pool outside first.'
    k = state(obj)
    if not on and k['fish']:
        return False, 'Release the fish before turning the sea tank back into a pool.'
    k['setup'] = bool(on)
    pond.remember('keeping', ('The pool became a deep salt sea tank.' if on else 'The sea tank was drained back into a pool.'), .45, item)
    pond._cache = None
    return True, 'Sea tank ready.' if on else 'Back to a swimming pool.'


def swim_blocked(pond, item, obj):
    """A pool set up as a sea tank is not for swimming."""
    return item in HOSTS and HOSTS[item]['setup'] and isinstance(obj, dict) and bool((obj.get('keeping') or {}).get('setup'))


def release(pond, item, instance, fish_id):
    obj = pond.object_state(item, instance)
    if obj is None or item not in HOSTS:
        return False, 'No koi pond there.'
    k = state(obj)
    fish = next((f for f in k['fish'] if f['id'] == fish_id), None)
    if fish is None:
        return False, 'That fish is not in this pond.'
    k['fish'].remove(fish)
    ledger(pond)[fish_id] = 'released'
    eco = pond.state.get('ecology', {})
    eco['fish'] = min(1., finite(eco.get('fish'), .5) + .01)
    pond.remember('keeping', (fish['name'] or 'The ' + fish['species'].replace('_', ' ')) + ' swam off into the big pond.', .5, item)
    pond._cache = None
    return True, 'Released back to the wild pond.'


def update(pond, item, obj, dt, outdoors, wet=False, temperature=15, wind=.1, weather='sunny', hour=12., season='spring'):
    if item not in HOSTS:
        return
    k = state(obj)
    if HOSTS[item]['setup'] and not k['setup']:
        return
    dt = max(0., min(86400., finite(dt)))
    if dt <= 0:
        return
    slices = max(1, min(2000, math.ceil(dt / 5.)))
    h = dt / slices
    sunny = outdoors and not wet and 7 <= hour < 18
    crowd = used(k) / HOSTS[item]['capacity']
    if HOSTS[item]['water'] == 'sea':
        sunny = False  # a deep covered tank grows little algae
    for _ in range(slices):
        if outdoors:
            k['algae'] = min(1., k['algae'] + h * (.00004 if sunny else .00001) * (1 + crowd))
            k['clarity'] = max(0., min(1., k['clarity'] + h * (-.00003 * (len(k['fish']) + 1) - .00002 * k['algae'] + (.00006 if wet else 0))))
            if season in ('fall', 'autumn'):
                k['leaves'] = min(1., k['leaves'] + h * .00005)
            k['ice'] = max(0., min(1., k['ice'] + h * (.0004 if temperature <= 0 else -.0008)))
            k['oxygen'] = max(0., min(1., k['oxygen'] + h * (-.00004 * (temperature > 24) - .00002 * crowd + .00006 * k['plants'] - .0001 * (k['ice'] > .8) + (.00005 if wind > .3 else 0))))
        k['flakes'] = max(0., k['flakes'] - h * .01)
        k['bell'] = max(0., k['bell'] - h * .00001)
        for f in k['fish']:
            eat = min(k['flakes'], .002 * h)
            k['flakes'] -= eat
            f['hunger'] = max(0., min(1., f['hunger'] + h * .00004 - eat * 8))
            stress = (f['hunger'] > .7) + (k['clarity'] < .3) + (k['oxygen'] < .3) + (crowd > .9)
            f['health'] = max(0., min(1., f['health'] + h * (.00003 if not stress else -.00004 * stress)))
            target = max(0., min(1., .8 - .4 * f['hunger'] - .2 * (k['clarity'] < .4) - .2 * crowd + .2 * f['trust']))
            f['mood'] += (target - f['mood']) * min(1., h * .002)
            if f['hunger'] < .4 and f['health'] > .7:
                f['growth'] = min(1., f['growth'] + h * .000005)
            f['trust'] = max(0., f['trust'] - h * .0000005)


def summary(obj, item='koi_pond'):
    k = state(obj)
    if not k['fish']:
        return 'No fish kept yet. Keep a catch from the fishing record.'
    hungry = [f for f in k['fish'] if f['hunger'] > .6]
    return (str(len(k['fish'])) + ' fish (' + str(round(used(k))) + '/' + str(round(HOSTS[item]['capacity'])) + ' cm) · water '
            + ('clear' if k['clarity'] > .6 else 'murky' if k['clarity'] < .35 else 'fair') + (' · ' + str(len(hungry)) + ' hungry' if hungry else '')
            + (' · iced over' if k['ice'] > .6 else ''))
