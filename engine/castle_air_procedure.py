"""Occurrence-owned air procedures, independent of movers and reward delivery.

The role controller retains its lease and drives each returned native route. It
must keep the proposal in its transient lease (immutable geometry plus a private
execution journal) and call finish_exit only
after participants have physically left. No child creates a completion receipt.
"""
import copy
import math
import uuid
from engine import castle_air as air, castle_work as castle, castle_shared as shared

PROCEDURES = {
    'castle_pressure_check': (
        ('gauge_before', 'castle_gauge_check'),
        ('seal_valve', 'castle_vent_close'),
        ('straighten_supply', 'castle_hose_straight'),
        ('gauge_after', 'castle_gauge_check'),
    ),
    'castle_dust_service': (
        ('sweep_grille', 'castle_grill_clean'),
        ('straighten_supply', 'castle_hose_straight'),
        ('restore_supply', 'castle_start'),
        ('gauge_after', 'castle_gauge_check'),
    ),
}


def recognizes(work):
    return isinstance(work, dict) and (
        isinstance(work.get('id'), str) and work['id'] in PROCEDURES or 'air_procedure' in work)


def disposition(atomic_id, state, initial):
    """Evaluate real state, never fabricate work for already satisfied controls."""
    if atomic_id == 'castle_gauge_check':
        return 'inspect-only', 'Read the actual pressure needle.'
    if atomic_id == 'castle_vent_close' and state['vent'] <= .001 and state['targets']['vent'] == 0:
        return 'skipped-with-state-reason', 'The air valve is already closed.'
    if atomic_id == 'castle_hose_straight' and all(state[k] <= .001 and state['targets'][k] == 0 for k in ('hose', 'kink')):
        return 'skipped-with-state-reason', 'The connected supply hose is already straight.'
    if atomic_id == 'castle_grill_clean' and state['dust'] <= .01:
        return 'skipped-with-state-reason', 'The grille has no meaningful dust to sweep.'
    if atomic_id == 'castle_start':
        if initial['motor'] == 'off' or initial['power_hold']:
            return 'skipped-with-state-reason', 'The original power policy leaves the supply stopped.'
        if initial['motor'] == 'auto' and state['motor'] == 'auto' and not initial['restart_allowed']:
            return 'skipped-with-state-reason', 'The original automatic policy is already in standby.'
        if state['motor'] == initial['motor'] and state['powered'] and state['rotor_speed'] >= .98:
            return 'skipped-with-state-reason', 'The original supply is already running.'
    return 'execute', 'Perform the authored control contacts.'


def propose(pond, plan, operator, origin, obstacles=(), available_seconds=math.inf):
    """Pure whole-itinerary geometry preflight; acquire no actor and move nothing.

    Routes include every possible child and every forward skip edge. The caller
    also preflights observer approaches/exits and deducts their travel budget.
    """
    work = plan.get('carnival_work', {})
    procedure_id = work.get('id')
    if not isinstance(procedure_id, str) or procedure_id not in PROCEDURES or not shared.point(origin):
        return None, 'Unknown procedure or invalid original root.'
    live = air.operator_state(pond, operator)
    if not live or not shared.near(live['root'], origin, 1e-7):
        return None, 'The original operator is no longer at the proposed root.'
    object_snapshot = copy.deepcopy(pond.object_state('bounce_house', plan))
    state = castle.state(object_snapshot)
    initial = dict(motor=state['motor'], power_hold=state['power_hold'],
                   power_revision=state['power_revision'],
                   restart_allowed=not state['power_hold'] and (state['motor'] == 'on' or state['motor'] == 'auto' and state['powered']))
    occurrences = []
    forecast = copy.deepcopy(state)
    for occurrence_id, atomic_id in PROCEDURES[procedure_id]:
        sites, reason = air.plan_sites(pond, plan, atomic_id, operator, obstacles)
        if not sites:
            return None, reason
        mode, reason = disposition(atomic_id, forecast, initial)
        if atomic_id == 'castle_start' and mode == 'execute' and castle.excursions.finite(object_snapshot.get('condition'), 1.) <= .2:
            return None, 'Repair the house before restoring its air supply.'
        occurrences.append(dict(occurrence_id=occurrence_id, atomic_id=atomic_id,
                                sites=sites, disposition=mode, reason=reason))
        # Predict only the already-authored terminal controls for branch choice.
        # No predicted pressure or observation becomes native state or evidence.
        if mode == 'execute':
            dust_before = forecast['dust']
            for _, field, value in castle.ROUTINES[atomic_id]['effects']:
                if field == 'motor':
                    forecast['motor'] = initial['motor'] if value == 'on' else value
                    forecast['powered'] = forecast['motor'] != 'off' and (forecast['motor'] == 'on' or state['powered'])
                    forecast['rotor_speed'] = float(forecast['powered'])
                elif field in castle.MOVING:
                    forecast[field] = forecast['targets'][field] = value
                elif field == 'dust_fraction':
                    forecast['dust'] = dust_before * value
    # All forward edges allow a satisfied intermediate occurrence to be skipped
    # without silently introducing an unexamined cross-object movement segment.
    nodes = [('origin', list(origin))]
    for occurrence in occurrences:
        nodes.extend((occurrence['occurrence_id'] + ':' + str(site['station_index']), site['stance'])
                     for site in occurrence['sites'])
    nodes.append(('exit', list(origin)))
    routes = {}
    for i, (name, root) in enumerate(nodes[:-1]):
        for target_name, target in nodes[i + 1:]:
            route = air.plan_route(pond, plan, 'castle_gauge_check', operator, root, target, obstacles)
            if route is None:
                return None, 'The full itinerary or a possible skip/exit route is obstructed.'
            routes[name + '>' + target_name] = route
    # Conservative real-time bound uses the role controller's measured movement
    # speed; callers must supply a budget after reserving other actors' travel.
    return dict(version=1, id=procedure_id, attempt=uuid.uuid4().hex,
                instance=plan.get('instance'), center=castle.placement_center(pond, plan),
                operator=copy.deepcopy(operator), origin=list(origin),
                occurrences=occurrences, routes=routes, initial_power=initial,
                available_seconds=available_seconds), ''


def budget(proposal, speed, other_seconds=0., response_seconds=12.):
    """Conservative duration including settling and slow vertical travel.

    speed is the adapter's minimum horizontal speed, including mind pacing.
    The 2.5 vertical factor bounds regular, rare and story mover metrics.
    """
    if not isinstance(speed, (int, float)) or not math.isfinite(speed) or speed <= 0:
        return math.inf
    seconds = other_seconds
    previous = 'origin'
    root = proposal['origin']
    for occurrence in proposal['occurrences']:
        # A planned skipped branch is an explicit state precondition, checked
        # throughout the itinerary. It cannot later grow into unbudgeted work.
        if occurrence['disposition'] == 'skipped-with-state-reason':
            continue
        seconds += castle.ROUTINES[occurrence['atomic_id']]['duration'] + response_seconds
        for site in occurrence['sites']:
            name = occurrence['occurrence_id'] + ':' + str(site['station_index'])
            route = proposal['routes'][previous + '>' + name]
            for point in route:
                seconds += math.hypot(point[0] - root[0], 2.5 * (point[1] - root[1])) / speed
                root = point
            previous = name
    for point in proposal['routes'][previous + '>exit']:
        seconds += math.hypot(point[0] - root[0], 2.5 * (point[1] - root[1])) / speed
        root = point
    return seconds


def begin(work, proposal, required_seconds):
    available = proposal.get('available_seconds')
    if (type(required_seconds) not in (int, float) or not math.isfinite(required_seconds) or required_seconds < 0
        or type(available) not in (int, float) or math.isnan(available) or available < 0
        or work.get('id') != proposal['id'] or required_seconds > available
        or '_journal' in proposal or 'air_procedure' in work):
        return False
    work['air_procedure'] = dict(
        version=1, id=proposal['id'], attempt=proposal['attempt'], phase='approach',
        current_occurrence=None, occurrences=[dict(o, status='pending') for o in copy.deepcopy(proposal['occurrences'])],
        observations=[], initial_power=copy.deepcopy(proposal['initial_power']),
        cursor=-1, node='origin', mechanical_contacts=0, outcome=None, receipt=False)
    work.pop('atomic', None)
    _checkpoint(work, proposal)
    return True


def _checkpoint(work, contract):
    # This journal belongs to the transient lease, never the serialized plan.
    # Reload cannot resurrect it, and mutating a work record cannot forge the
    # history of native transitions or already delivered receipts.
    contract['_journal'] = copy.deepcopy({k: work[k] for k in ('air_procedure', 'atomic') if k in work})


def _same(left, right):
    # Python treats False == 0 and True == 1; wire validation must not.
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(_same(left[k], right[k]) for k in left)
    if isinstance(left, (list, tuple)):
        return len(left) == len(right) and all(_same(a, b) for a, b in zip(left, right))
    return left == right


def validate(work, contract):
    try:
        p = work['air_procedure']
        if not _same(contract.get('_journal'), {k: work[k] for k in ('air_procedure', 'atomic') if k in work}):
            return False
        if not isinstance(p, dict) or work['id'] != contract['id'] or p['id'] != contract['id'] or p['attempt'] != contract['attempt'] or p['version'] != 1:
            return False
        if p['initial_power'] != contract['initial_power'] or len(p['occurrences']) != len(contract['occurrences']):
            return False
        if type(p['cursor']) is not int or not -1 <= p['cursor'] < len(p['occurrences']):
            return False
        for index, (actual, expected) in enumerate(zip(p['occurrences'], contract['occurrences'])):
            if any(actual[k] != expected[k] for k in ('occurrence_id', 'atomic_id', 'sites')):
                return False
            if index < p['cursor'] and actual['status'] not in ('finished', 'skipped'):
                return False
            if index > p['cursor'] and actual['status'] != 'pending':
                return False
        if p['current_occurrence'] is not None:
            child = work['atomic']; occurrence = p['occurrences'][p['cursor']]
            if child['occurrence_id'] != p['current_occurrence'] or child['occurrence_id'] != occurrence['occurrence_id'] or child['id'] != occurrence['atomic_id']:
                return False
        elif 'atomic' in work:
            return False
        return True
    except (KeyError, TypeError, IndexError, RecursionError):
        return False


def next_occurrence(pond, plan, contract):
    work = plan['carnival_work']
    if not validate(work, contract):
        return air.result('blocked', 'The procedure occurrence contract changed.')
    p = work['air_procedure']
    if p['phase'] in ('exit', 'done') or p['receipt']:
        return air.result('blocked', 'The itinerary has already ended.')
    if p['current_occurrence'] is not None:
        return air.result('blocked', 'The current occurrence must finish before the next begins.')
    state = castle.state(pond.object_state('bounce_house', plan))
    if state['power_revision'] != p['initial_power']['power_revision'] or state['power_hold'] != p['initial_power']['power_hold']:
        return air.result('blocked', 'The player changed the power policy during this procedure.')
    while p['cursor'] + 1 < len(p['occurrences']):
        next_cursor = p['cursor'] + 1
        occurrence = p['occurrences'][next_cursor]
        mode, reason = disposition(occurrence['atomic_id'], state, p['initial_power'])
        if (contract['occurrences'][next_cursor]['disposition'] == 'skipped-with-state-reason'
            and mode != 'skipped-with-state-reason'):
            return air.result('blocked', 'A satisfied control changed; this visit has no budget for new work.')
        p['cursor'] = next_cursor
        occurrence.update(disposition=mode, reason=reason)
        if mode == 'skipped-with-state-reason':
            occurrence['status'] = 'skipped'
            continue
        occurrence['status'] = 'active'
        p['current_occurrence'] = occurrence['occurrence_id']
        work['atomic'] = air.make_execution(occurrence['atomic_id'], occurrence['occurrence_id'], 'procedure')
        if occurrence['atomic_id'] == 'castle_start':
            work['atomic']['restore_motor'] = p['initial_power']['motor']
            if p['initial_power']['motor'] == 'auto':
                work['atomic']['label'] = 'Restore automatic air supply'
        p['phase'] = 'approach'
        site = occurrence['sites'][0]
        node = occurrence['occurrence_id'] + ':0'
        _checkpoint(work, contract)
        return air.result('transfer', site=copy.deepcopy(site), route=copy.deepcopy(contract['routes'][p['node'] + '>' + node]), node=node)
    p['phase'] = 'exit'
    _checkpoint(work, contract)
    return air.result('exit', route=copy.deepcopy(contract['routes'][p['node'] + '>exit']))


def arrived(work, contract, node):
    """Caller confirms actual root/stance through its native motion controller."""
    if not validate(work, contract):
        return False
    p = work['air_procedure']
    if not isinstance(node, str) or not node.startswith(str(p['current_occurrence']) + ':'):
        return False
    occurrence = p['occurrences'][p['cursor']]
    if node not in [occurrence['occurrence_id'] + ':' + str(s['station_index']) for s in occurrence['sites']]:
        return False
    p.update(node=node, phase='hold')
    _checkpoint(work, contract)
    return True


def advance(pond, plan, contract, context, dt):
    work = plan['carnival_work']
    if not validate(work, contract):
        return air.result('blocked', 'The procedure occurrence contract changed.')
    p = work['air_procedure']; child = work.get('atomic')
    state = castle.state(pond.object_state('bounce_house', plan))
    if state['power_revision'] != p['initial_power']['power_revision'] or state['power_hold'] != p['initial_power']['power_hold']:
        return air.result('blocked', 'The original power policy changed.')
    if p['phase'] != 'hold' or not child:
        return air.result('blocked', 'No child is at its real station.')
    result = air.advance_atomic(pond, plan, child, context, dt)
    p['mechanical_contacts'] += sum(air.event_metric(context['operator'], child['id'], i)['kind'] == 'contact' for i in result.get('new_events', []))
    occurrence = p['occurrences'][p['cursor']]
    if result['status'] == 'transfer':
        site = occurrence['sites'][result['station_index'] + 1]
        node = occurrence['occurrence_id'] + ':' + str(site['station_index'])
        p['phase'] = 'approach'
        _checkpoint(work, contract)
        return dict(result, site=copy.deepcopy(site), route=copy.deepcopy(contract['routes'][p['node'] + '>' + node]), node=node)
    if result['status'] == 'finished':
        if result.get('observation') is not None:
            p['observations'].append(dict(occurrence_id=child['occurrence_id'], reader=copy.deepcopy(context['operator']), **result['observation']))
        occurrence.update(status='finished', execution=copy.deepcopy(child))
        p['current_occurrence'] = None
        work.pop('atomic')
        _checkpoint(work, contract)
        # Discard leftover dt. A new occurrence always requires actual arrival.
        return next_occurrence(pond, plan, contract)
    _checkpoint(work, contract)
    return result


def finish_exit(work, contract, participants_exited):
    if not validate(work, contract) or participants_exited is not True:
        return None
    p = work['air_procedure']
    if p['phase'] != 'exit' or p['receipt'] or any(o['status'] not in ('finished', 'skipped') for o in p['occurrences']):
        return None
    reads = p['observations']
    if len(reads) != (2 if p['id'] == 'castle_pressure_check' else 1):
        return None
    outcome = 'observed'
    if not p['initial_power']['restart_allowed']:
        outcome = 'supply-stopped'
    elif p['id'] == 'castle_pressure_check':
        delta = reads[-1]['pressure'] - reads[0]['pressure']
        outcome = 'improved' if delta > .005 else 'worse' if delta < -.005 else 'unchanged'
    else:
        outcome = 'serviced' if p['mechanical_contacts'] else 'inspected'
    p.update(phase='done', outcome=outcome, receipt=True)
    _checkpoint(work, contract)
    return dict(attempt=p['attempt'], id=p['id'], outcome=outcome,
                mechanical_contacts=p['mechanical_contacts'], observations=copy.deepcopy(reads))


def itinerary_clear(pond, plan, contract, obstacles=()):
    """Recheck the entire retained corridor before an irreversible child beat.

    The role owner supplies current observer/body boxes and separately verifies
    their identities, stationary pose, departure budget and approach/exit lease.
    This never acquires a new participant or adjusts a planned stance.
    """
    try:
        work = plan['carnival_work']
        # The atomic executor may already have advanced its private child
        # clock when invoking preflight. The outer journal must still match.
        if (work.get('id') != contract['id'] or plan.get('instance') != contract['instance']
            or not _same(work.get('air_procedure'), contract.get('_journal', {}).get('air_procedure'))):
            return False
        if castle.placement_center(pond, plan) != contract['center']:
            return False
        operator = contract['operator']
        live = air.operator_state(pond, operator)
        if not live or not air.supported(pond, plan, 'castle_gauge_check', operator, live['root'], obstacles):
            return False
        state = castle.state(pond.object_state('bounce_house', plan))
        initial = contract['initial_power']
        if state['power_revision'] != initial['power_revision'] or state['power_hold'] != initial['power_hold']:
            return False
        nodes = {'origin': contract['origin'], 'exit': contract['origin']}
        for occurrence in contract['occurrences']:
            if (occurrence['disposition'] == 'skipped-with-state-reason'
                and disposition(occurrence['atomic_id'], state, initial)[0] != 'skipped-with-state-reason'):
                return False
            if not castle.allowed(pond, occurrence['atomic_id']):
                return False
            for site in occurrence['sites']:
                nodes[occurrence['occurrence_id'] + ':' + str(site['station_index'])] = site['stance']
                # A still-walkable route is insufficient when new scenery or
                # another body blocks the later dial reading or control reach.
                rows = [m for m in air.metrics(operator, occurrence['atomic_id'])
                        if m['station_index'] == site['station_index']]
                if not rows or site['target'] != castle.control_world(contract['center'], site['station']):
                    return False
                for metric in rows:
                    if metric['kind'] == 'observation':
                        if (site.get('observation_target') != air.observation_target(contract['center'])
                            or not air.sightline(pond, plan, site['stance'], True, metric, contract['center'], obstacles)):
                            return False
                    elif castle.reach_distance(site['stance'], site['target'], metric['grip'], metric['scale']) > 3:
                        return False
        for edge, path in contract['routes'].items():
            start_name, end_name = edge.split('>')
            if not path or path[-1] != nodes[end_name]:
                return False
            previous = nodes[start_name]
            for target in path:
                if not air.segment_clear(pond, plan, 'castle_gauge_check', operator, previous, target, obstacles):
                    return False
                previous = target
        return True
    except (KeyError, TypeError, ValueError, IndexError, AttributeError):
        return False
