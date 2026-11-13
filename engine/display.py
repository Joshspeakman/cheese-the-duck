"""Display spots: owned collectibles shown on a placed trophy_case or cabinet.

Showing never consumes or creates anything: a displayed thing is a reference to
something Cheese owns, and it leaves the shelf if it stops being owned. Each item
may be shown in one place at a time. User decision 2026-11-13.
"""
import math
HOSTS = {'trophy_case': dict(slots=8), 'cabinet': dict(slots=10)}
CASE = dict(dust=(.1, 0, 1), shine=(.5, 0, 1), arranged=(.5, 0, 1))


def finite(v, d=0.):
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) else d


def state(obj):
    d = obj.get('display')
    if not isinstance(d, dict):
        d = obj['display'] = {}
    for f, (v, lo, hi) in CASE.items():
        d[f] = max(lo, min(hi, finite(d.get(f), v)))
    items = d.get('items') if isinstance(d.get('items'), list) else []
    d['items'] = [i for i in dict.fromkeys(x for x in items if isinstance(x, str))]
    return d


def shown_anywhere(pond):
    out = {}
    for p in pond.placements:
        if p.item_id in HOSTS:
            obj = pond.object_state(p.item_id, p.instance)
            if obj is not None:
                for i in state(obj)['items']:
                    out[i] = (p.item_id, p.instance)
    return out


def reconcile(pond):
    """Things no longer owned leave every shelf (nothing is invented or kept)."""
    for p in pond.placements:
        if p.item_id in HOSTS:
            obj = pond.object_state(p.item_id, p.instance)
            if obj is not None:
                d = state(obj)
                d['items'] = [i for i in d['items'] if i in pond.owned]


def show(pond, item, instance, thing, displayable):
    if item not in HOSTS:
        return False, 'Only a trophy case or cabinet can display things.'
    if thing not in displayable:
        return False, 'That is not something to put on display.'
    if thing not in pond.owned:
        return False, 'Cheese does not own that.'
    obj = pond.object_state(item, instance)
    if obj is None or not any(p.instance == instance and p.item_id == item for p in pond.placements):
        return False, 'Place it outside first.'
    where = shown_anywhere(pond).get(thing)
    if where:
        return False, 'That is already on display.'
    d = state(obj)
    if len(d['items']) >= HOSTS[item]['slots']:
        return False, 'No room left on the shelves.'
    d['items'].append(thing)
    pond.remember('display', 'Put the ' + thing.replace('_', ' ') + ' on display.', .4, item)
    pond._cache = None
    return True, 'On display: ' + thing.replace('_', ' ') + '.'


def take(pond, item, instance, thing):
    obj = pond.object_state(item, instance)
    if obj is None or item not in HOSTS:
        return False, 'Nothing displayed there.'
    d = state(obj)
    if thing not in d['items']:
        return False, 'That is not on these shelves.'
    d['items'].remove(thing)
    pond._cache = None
    return True, 'Taken down: ' + thing.replace('_', ' ') + '.'


def update(pond, item, obj, dt, outdoors):
    if item not in HOSTS:
        return
    d = state(obj)
    dt = max(0., min(86400., finite(dt)))
    d['dust'] = min(1., d['dust'] + dt * (.00003 if outdoors else .00001))
    d['shine'] = max(0., d['shine'] - dt * .00002)
