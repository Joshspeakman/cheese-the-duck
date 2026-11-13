"""Physical-copy histories with a backwards-compatible catalogue view.

`objects` is the view used by inventory cards and older save readers. `instances`
owns placed belongings. The catalogue view aliases one representative record in
memory; physical actions always resolve their explicit saved identity.
"""
import copy
from engine.placements import physical_belongings


def fresh():
    return dict(condition=1., wetness=0., dirt=0., bond=0., uses=0,
                last_use=-1000., growth=.35, active=False)


def sync(pond):
    s = pond.state
    physical = list(physical_belongings(pond.game))
    instances = s['instances']
    known = {v['_item'] for v in instances.values() if '_item' in v}
    # The old renderer used the last placed copy for a catalogue item. Keep its
    # accumulated history there; additional copies start with their own record.
    for source, item, identity in reversed(physical):
        if identity not in instances:
            old = s['objects'].get(item) if item not in known else None
            instances[identity] = copy.deepcopy(old) if old else fresh()
            instances[identity].update(_item=item, _source=source, active=False)
            if old:
                for key, until in list(s['cooldowns'].items()):
                    if key.endswith(':'+item):s['cooldowns'][key[:-len(item)]+identity]=until
            known.add(item)
        for key, value in fresh().items():
            instances[identity].setdefault(key, value)
    return physical


def catalogue(pond, physical):
    for _, item, identity in physical:
        pond.state['objects'][item] = pond.state['instances'][identity]
    # Visible copy takes precedence over storage and interior rooms in cards.
    for p in pond.placements:
        pond.state['objects'][p.item_id] = pond.state['instances'][p.instance]


def resolve(pond, item, ref=None):
    identity = ref if isinstance(ref, str) else (ref or {}).get('instance')
    if identity:
        obj = pond.state['instances'].get(identity)
        return obj if obj and obj.get('_item') == item else None
    destination = (ref or {}).get('destination')
    if destination and not (ref or {}).get('portable'):
        from engine.shelters import position
        copies = [p for p in pond.placements if p.item_id == item and position(p) == destination]
        if len(copies) == 1:
            return pond.state['instances'].get(copies[0].instance)
        return None
    return pond.state['objects'].get(item)


def records(pond):
    """Visit each record once, even though catalogue entries alias physical ones."""
    placed = {p.instance for p in getattr(pond, 'placements', [])}
    seen = set()
    for identity, obj in pond.state['instances'].items():
        seen.add(id(obj))
        yield obj['_item'], obj, identity in placed
    for item, obj in pond.state['objects'].items():
        if id(obj) not in seen:
            yield item, obj, False


def bind_legacy_plan(pond):
    plan = pond.state.get('plan')
    if not plan or plan.get('instance') or plan.get('portable') or plan.get('in_place') or not plan.get('destination'):
        return  # in-place (worn/held) repertoire plans are not legacy reservations
    from engine.shelters import position
    copies = [p for p in pond.placements if p.item_id == plan['target'] and position(p) == plan['destination']]
    if len(copies) != 1:
        if plan['kind'] in ('item','clean_item','repair_item') or plan.get('residence'):
            # No identity was saved. If the location no longer identifies one
            # object, there is no honest way to resume this old reservation.
            pond.state['plan']=None
            pond._cache=None
        return
    plan['instance'] = copies[0].instance
    for field in ('residence', 'seating', 'instrument'):
        if plan.get(field):
            plan[field]['instance'] = copies[0].instance
