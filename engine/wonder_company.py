"""Visitors at the wonders: joining Cheese, or working a wonder themselves.

company: a present visitor walks over under their own movement and shares Cheese's
         routine clock, reacting at its actual contact moments in a style that
         follows their personality. Bonds, learning and memories are credited only
         after a completed routine they genuinely shared.
operate: an idle visitor works a placed wonder that nobody is using. Their own
         native clock applies the authored contacts to the real object. If Cheese
         is an egg nearby he gets a 'watched' memory, nothing else: an egg never
         walks, turns or learns a skill from someone else's work.
Reservations are transient (never saved) and live in minds.wonder_guests, which
every other company module treats as busy.
"""
import copy
from engine import wonders, shelters, portable_ground


def spec_of(routine):
    """Routine spec from the wonders or the generic repertoire engine."""
    if routine in wonders.ROUTINES:
        return wonders.ROUTINES[routine]
    from engine import repertoire
    return repertoire.ROUTINES[routine]


def plan_work(plan):
    """(work key, work) for a plan Cheese is doing that visitors may join."""
    for key in ('wonder_work', 'rep_work'):
        if plan and plan.get(key):
            return key, plan[key]
    return None, None


def plan_valid(pond, plan, key):
    if key == 'wonder_work':
        return wonders.valid(pond, plan)
    from engine import repertoire
    return repertoire.valid(pond, plan)


def family(item):
    """'wonder' or 'rep' for an object a visitor could work themselves."""
    if item in wonders.ITEMS:
        return 'wonder'
    from engine import repertoire
    return 'rep' if repertoire.OBJECTS.get(item, {}).get('host') == 'placed' else None


def routines_of(item, fam):
    if fam == 'wonder':
        return wonders.BY_ITEM[item]
    from engine import repertoire
    return repertoire.by_object(item)


def state_of(item, obj, fam):
    if fam == 'wonder':
        return wonders.state(item, obj)
    from engine import repertoire
    return repertoire.state(item, obj)


def sheltering(plan, key, routine):
    if key == 'wonder_work':
        return wonders.sheltering(plan['target'], routine)
    r = spec_of(routine)
    return r['tool'] == 'none' and 'wet' in r['when'] and r['duration'] >= 30
from engine.visitor_shelters import distance, departing, profile

HANDED = {'duck', 'goose', 'owl', 'crow', 'toad', 'duckling'}
# Visitors never make Cheese's irreversible or finite choices for him unattended.
VISITOR_SKIP = {'sand_kaiju_stomp', 'genie_make_wish', 'volcano_baking_soda', 'clone_purge', 'printer_make_it_rain'}
LOUD = {'gong_mighty_bong', 'gong_dinner_call', 'gong_cover_ears', 'volcano_baking_soda', 'time_pull_lever', 'weather_catch_spark',
        'transmog_crank', 'transmog_kick', 'sand_kaiju_stomp', 'shrink_zap_pebble', 'growth_zap_dandelion', 'portal_peek_through'}


def busy(minds, key):
    m = minds
    return bool(key in m.carnival_guests or key in m.nest_helpers or key in m.playmates or key in m.structure_helpers or key in m.ground_helpers
                or key in m.textile_helpers or key in m.creators or key in m.housing or key in m.gardening or key in m.furnishings or key in m.musicians
                or key in m.readers or key in m.wonder_guests or m.encounter_for(key))


def style(minds, key, routine):
    t = minds.model.residents[key]['traits']
    if routine in LOUD and t['confidence'] < .45:
        return 'nervous'
    if t['sociability'] > .55 and t['confidence'] > .45:
        return 'cheer'
    if t['care'] > .5 or t['patience'] > .55:
        return 'steady'
    return 'curious'


def ready(minds):
    return minds.game.duck.current_action not in ('feed', 'play', 'clean', 'pet', 'sleep')


def can_operate(minds, key, routine):
    _, species = profile(minds, key)
    if species not in HANDED:
        return False
    body = 'duckling' if species == 'duckling' else 'adult'  # measured duck-sized reach
    spec = spec_of(routine)
    from engine import repertoire
    reach = wonders.REACH.get(routine) if routine in wonders.ROUTINES else repertoire.REACH.get(routine, ())
    return body in (reach or ()) and (not spec.get('ages') or body in spec['ages'])


def valid(minds, r):
    p = minds.pond
    if r['actor'] not in minds.present or minds.presence_tokens.get(r['actor']) != r['token'] or r['location'] != p.location:
        return False
    if departing(minds, r['actor']) or r['actor'] in minds.housing or shelters.adverse(p.weather_type) and not r.get('shelter'):
        return False
    if not shelters.still_placed(p, dict(id=r['id'], instance=r['instance'], destination=r['destination'])):
        return False
    if r['mode'] == 'company':
        plan = p.state.get('plan')
        return bool(plan and plan.get(r.get('key', 'wonder_work')) is r['work'] and plan_valid(p, plan, r.get('key', 'wonder_work')))
    plan = p.state.get('plan')
    if plan and plan.get('target') == r['id'] and plan.get('instance') == r['instance']:
        return False  # Cheese started on this exact copy: the visitor steps away.
    return r['id'] in p.owned


def release(minds, key, retry=60):
    if minds.wonder_guests.pop(key, None) is not None:
        minds.wonder_retry[key] = minds.now + retry
        minds.pond._cache = None


def tick(minds, dt):
    p = minds.pond
    for key, r in list(minds.wonder_guests.items()):
        if not valid(minds, r) or not ready(minds) and r['mode'] == 'company':
            release(minds, key)
            continue
        plan = p.state.get('plan')
        if r['mode'] == 'company' and plan.get('paused'):
            r['started'] += dt
            continue
        here = distance(minds.present[key], r['spot'])
        if r['phase'] == 'approach':
            if minds.now - r['started'] > 30:
                release(minds, key)
            elif here <= .8:
                r.update(phase='enter', elapsed=0.)
            continue
        if here > 3 and r['phase'] != 'exit':
            release(minds, key)
            continue
        if r['phase'] == 'enter':
            r['elapsed'] += dt
            if r['elapsed'] >= 2:
                r.update(phase='inside', elapsed=0., last_clock=r['work']['elapsed'])
        elif r['phase'] == 'inside' and r['mode'] == 'company':
            clock = r['work']['elapsed']
            r['overlap'] += max(0., clock - r['last_clock'])
            r['last_clock'] = clock
            if r['work'].get('done'):
                r['phase'] = 'finished'
        elif r['phase'] == 'inside':
            operate(minds, key, r, dt)
        elif r['phase'] == 'exit':
            r['elapsed'] += dt
            if r['elapsed'] >= 2:
                release(minds, key, 240)
    invite(minds)
    volunteer(minds)


def invite(minds):
    """At most one visitor joins Cheese, chosen once per routine start."""
    p = minds.pond
    plan = p.state.get('plan')
    wkey, work = plan_work(plan)
    if not work or plan.get('paused') or not ready(minds):
        return
    if work.get('invitation_checked') or work.get('done') or work['elapsed'] > 0 or plan['phase'] not in ('prepare', 'act'):
        return
    work['invitation_checked'] = True
    if any(r['mode'] == 'company' for r in minds.wonder_guests.values()):
        return
    origin = list(plan.get('destination', work['origin']))
    spot = portable_ground.companion_spot(p, plan, origin)
    if spot is None:
        return
    shelter = sheltering(plan, wkey, work['id'])
    options = []
    for key in minds.present:
        if key == 'cheese' or departing(minds, key) or minds.now < minds.wonder_retry.get(key, 0) or busy(minds, key):
            continue
        resident = minds.model.residents[key]
        duet = bool(spec_of(work['id']).get('duo'))  # a duet was chosen because this friend is here: they come over
        if resident['energy'] < .25 or (not shelter and not duet and minds.tasks.get(key, {}).get('action') not in ('observe', 'share', 'restore')):
            continue
        d = distance(minds.present[key], spot)
        if d <= (90 if duet else 24):
            options.append((d - 5 * resident['traits']['sociability'] - 4 * resident['traits']['curiosity'], key))
    if not options:
        return
    _, key = min(options)
    minds.tasks.pop(key, None)
    minds.wonder_guests[key] = dict(actor=key, mode='company', key=wkey, id=plan['target'], instance=plan.get('instance'), destination=origin, spot=spot,
                                    location=p.location, token=minds.presence_tokens[key], phase='approach', elapsed=0., started=minds.now,
                                    style=style(minds, key, work['id']), work=work, overlap=0., last_clock=work['elapsed'], shelter=shelter, duet=bool(spec_of(work['id']).get('duo')),
                                    contexts={k: minds.context(k) for k in ('cheese', key)})
    p._cache = None


def volunteer(minds):
    """An idle visitor may work a free wonder themselves (one at a time)."""
    p = minds.pond
    if any(r['mode'] == 'operate' for r in minds.wonder_guests.values()) or p.location != 'Home Pond' or shelters.adverse(p.weather_type):
        return
    if minds.now < getattr(minds, 'wonder_next', 0):
        return
    minds.wonder_next = minds.now + 20
    plan = p.state.get('plan')
    world = wonders.World(p)
    for placed in p.placements:
        item, iid = placed.item_id, placed.instance
        fam = family(item)
        if fam is None or (plan and plan.get('target') == item and plan.get('instance') == iid):
            continue
        if any(r['instance'] == iid for r in minds.wonder_guests.values()):
            continue
        obj = p.object_state(item, iid)
        if obj is None:
            continue
        s = state_of(item, obj, fam)
        destination = shelters.position(placed)
        spot = portable_ground.companion_spot(p, dict(instance=iid), destination)
        if spot is None:
            continue
        for key in minds.present:
            if key == 'cheese' or departing(minds, key) or minds.now < minds.wonder_retry.get(key, 0) or busy(minds, key):
                continue
            resident = minds.model.residents[key]
            if resident['energy'] < .3 or minds.tasks.get(key, {}).get('action') not in ('observe', 'share', 'restore') or distance(minds.present[key], spot) > 70:
                continue
            keys = [k for k in routines_of(item, fam) if k not in VISITOR_SKIP and spec_of(k)['events'] and can_operate(minds, key, k)
                    and all(wonders.condition(w, s, world, {}) for w in spec_of(k)['when'] if not w.lstrip('!') in ('young', 'grown', 'elder', 'tired', 'lonely', 'sad', 'happy', 'grumpy', 'curious'))]
            if not keys:
                continue
            seed = wonders.hash_text(key + item + str(int(minds.now / 60)))
            routine = keys[seed % len(keys)]
            minds.tasks.pop(key, None)
            egg = minds.game.duck.growth_stage == 'egg'
            minds.wonder_guests[key] = dict(actor=key, mode='operate', id=item, instance=iid, destination=destination, spot=spot, location=p.location,
                                            token=minds.presence_tokens[key], phase='approach', elapsed=0., started=minds.now, style='operator',
                                            work=dict(id=routine, elapsed=0., events=[], done=False), egg_watching=egg, family=fam,
                                            contexts={key: minds.context(key)})
            p._cache = None
            return


def operate(minds, key, r, dt):
    """The visitor's own native clock: contacts land on the real object."""
    p = minds.pond
    work = r['work']
    spec = spec_of(work['id'])
    fam = r.get('family', 'wonder')
    obj = p.object_state(r['id'], r['instance'])
    s = state_of(r['id'], obj, fam)
    work['elapsed'] = min(spec['duration'], work['elapsed'] + dt)
    for i, (at, name) in enumerate(spec['events']):
        if work['elapsed'] >= at * spec['duration'] and i not in work['events']:
            work['events'].append(i)
            if fam == 'wonder':
                wonders.apply(s, r['id'], wonders.ITEMS[r['id']]['effects'][name])
            else:
                from engine import repertoire
                # Visitors change the object, never Cheese's needs.
                repertoire.apply(s, r['id'], [row for row in repertoire.OBJECTS[r['id']]['effects'][name] if not row[0].startswith('need.')])
    p._cache = None
    if work['elapsed'] >= spec['duration'] and not work['done']:
        work['done'] = True
        r.update(phase='exit', elapsed=0.)
        name = minds.model.residents[key]['name']
        # Visitor runs are kept apart from Cheese's own history (which drives his novelty).
        runs = obj.setdefault('wonder_visitor_routines', {})
        runs[work['id']] = min(9999, runs.get(work['id'], 0) + 1)
        obj.setdefault('wonder_visitors', {})
        obj['wonder_visitors'][key] = min(9999, obj['wonder_visitors'].get(key, 0) + 1)
        note = name + ': ' + spec['label'] + '.'
        minds.model.learn(key, 'restore', r['contexts'][key], .2, minds.now, note)
        p.remember('neighbors', name + ' had a go at the ' + r['id'].replace('_', ' ') + ': ' + spec['label'].lower() + '.', .45, key)
        if r.get('egg_watching') and minds.game.duck.growth_stage == 'egg' and distance(minds.present.get('cheese', r['spot']), r['spot']) <= 40:
            # Observation only: no skill, need, facing or position change for the egg.
            p.remember('egg', 'From inside the shell, Cheese heard ' + name + ' at the ' + r['id'].replace('_', ' ') + '.', .4, key)


def complete(minds, plan):
    """Called once when Cheese's routine completes; credits a genuinely shared one."""
    for key, r in list(minds.wonder_guests.items()):
        if r['mode'] != 'company' or r['work'] is not plan.get(r.get('key', 'wonder_work')) or r.get('recorded'):
            continue
        work = r['work']
        duration = spec_of(work['id'])['duration']
        if r['phase'] not in ('inside', 'finished') or not work.get('done') or work.get('interrupted') or not work.get('recorded') \
                or r['overlap'] < max(4, duration * .45) or distance(minds.present[key], r['spot']) > 3:
            continue
        r['recorded'] = True
        name = minds.model.residents[key]['name']
        label = spec_of(work['id'])['label']
        note = {'cheer': name + ' cheered Cheese on: ', 'nervous': name + ' watched from a careful step back: ',
                'steady': name + ' kept Cheese company: ', 'curious': name + ' leaned in to see: '}[r['style']] + label.lower() + '.'
        for actor, other in (('cheese', key), (key, 'cheese')):
            minds.model.learn(actor, 'share', r['contexts'][actor], .25, minds.now, note, other)
            minds.model.bond(actor, other, .16, minds.now, note)
        obj = minds.pond.object_state(plan['target'], plan) if r.get('key', 'wonder_work') == 'wonder_work' else __import__('engine.repertoire', fromlist=['store']).store(minds.pond, plan, work)
        obj.setdefault('wonder_company', {})
        obj['wonder_company'][r['style']] = min(9999, obj['wonder_company'].get(r['style'], 0) + 1)
        minds.pond.remember('neighbors', note, .55, key)
        r.update(phase='exit', elapsed=0.)


def motion(minds, key):
    r = minds.wonder_guests.get(key)
    if not r:
        return None
    return dict(target=list(r['spot']), facing=False, phase=r['phase'], gesture='idle')


def snapshot(minds):
    out = []
    for r in minds.wonder_guests.values():
        if not valid(minds, r) and r['phase'] != 'exit':
            continue
        rec = {k: copy.deepcopy(r[k]) for k in ('actor', 'mode', 'id', 'instance', 'destination', 'spot', 'phase', 'elapsed', 'style')}
        rec['routine'] = dict(id=r['work']['id'], elapsed=r['work']['elapsed'], company=dict(style=r['style'], mode=r['mode']))
        out.append(rec)
    return out


def conversation(minds, key):
    r = minds.wonder_guests.get(key) if key != 'cheese' else next((x for x in minds.wonder_guests.values() if x['mode'] == 'company'), None)
    if not r:
        return None
    partner = r['actor'] if key == 'cheese' else 'cheese'
    label = spec_of(r['work']['id'])['label']
    status = 'walking over' if r['phase'] == 'approach' else 'settling in' if r['phase'] == 'enter' else 'leaving' if r['phase'] == 'exit' else 'doing it now'
    if r['mode'] == 'operate':
        return dict(activity=label + ' (on their own)', object=r['id'].replace('_', ' '), status=status)
    return dict(with_name=minds.model.residents[partner]['name'], activity=label, object=r['id'].replace('_', ' '), status=status, style=r['style'])
