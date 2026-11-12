"""Whole-procedure role preflight, before any mover or lease is acquired.

The existing one-control formations supply candidate observer positions. Every
procedure control and skip/exit corridor is then independently measured with the
full air-control body envelope. This module does not run or award a procedure.
"""
import math
from datetime import datetime
from engine import castle_air as air, castle_air_procedure as procedure
from engine import castle_work as castle, castle_shared as shared
from engine import castle_actors as actors, castle_flight as flight, egg_caregiver as egg
from world.guest_cast import guest_profile


def minimum_speed(operator):
    if operator['adapter'] == 'cheese':
        return 1.
    if operator['adapter'] == 'story':
        return 3.5
    pace = guest_profile(operator['cast'])['pace']
    return pace * (.7 if operator['adapter'] == 'regular' else .72) * .8


def remaining_seconds(pond, operator):
    if operator['adapter'] == 'cheese':
        return math.inf
    if operator.get('cast') == 'butterfly_fairy':
        live = actors.flight(pond)
        if not live or actors.identity(live) != operator:
            return 0.
    else:
        live = air.operator_state(pond, operator)
    if not live:
        return 0.
    if operator['adapter'] == 'regular':
        visit = pond.game.friends.current_visit
        try:
            if str(visit.started_at) != operator['token'] or type(visit.duration_minutes) not in (int, float):
                return 0.
            started = datetime.fromisoformat(visit.started_at)
            remaining = visit.duration_minutes * 60 - (datetime.now(started.tzinfo) - started).total_seconds()
            return max(0., remaining) if math.isfinite(remaining) else 0.
        except (TypeError, ValueError, AttributeError):
            return 0.
    return live.get('remaining_seconds', math.inf)


def travel_seconds(origin, route, speed):
    return sum(math.hypot(b[0] - a[0], 2.5 * (b[1] - a[1])) / speed
               for a, b in zip([origin] + route, route))


def present_count(pond):
    return sum(bool(v) for v in (pond.game.friends.current_visit,
               pond.game.atmosphere.current_visitor, pond.state.get('story')))


def propose(pond, score, instance, together=False):
    if not isinstance(score, str) or score not in procedure.PROCEDURES:
        return None, 'Choose an authored air procedure.'
    if pond.state.get('plan') or not pond.scene_available():
        return None, 'Finish the current activity before beginning this procedure.'
    if flight.outfitted(pond):
        return None, 'This procedure needs measured clearance for the equipped outfit.'
    count = present_count(pond)
    if count > (1 if together else 0):
        return None, 'Another visitor occupies an unreserved part of the working scene.'
    age = castle.canonical_age(pond.game.duck.growth_stage)
    plan = dict(target='bounce_house', instance=instance, automatic=False)
    plan['carnival_work'] = castle.make(pond, plan, score)
    center = castle.placement_center(pond, plan)
    if not shared.point(center) or 'bounce_house' not in pond.owned:
        return None, 'That exact house must be placed here.'
    plan['destination'] = [round(v) for v in center]
    first_atomic = procedure.PROCEDURES[score][0][1]
    formation = None
    observer = None
    recipient = None
    obstacles = []
    other_seconds = 0.
    available_seconds = math.inf
    if pond.game.duck.growth_stage == 'egg':
        if not together:
            return None, 'The resting egg needs an arrived caregiver for this procedure.'
        formation, reason = egg.propose(pond, first_atomic, instance)
        if not formation:
            return None, reason
        mode = 'egg-caregiver'
        operator = formation['operator']
        origin = formation['origin']
        recipient = formation['recipient']
        obstacles = [egg.box(recipient['root'], egg.metric(recipient))]
        available_seconds = remaining_seconds(pond, operator)
    elif not age:
        return None, 'This age has no measured operator or observer anatomy.'
    elif together:
        if actors.flight(pond):
            formation, reason = flight.propose(pond, first_atomic, instance)
            if not formation:
                return None, reason
            mode = 'flight-observer'
            operator = dict(actor='cheese', adapter='cheese', source_age=age,
                            token=str(pond.game.duck.created_at))
            origin = formation['roots']['cheese']
            observer = formation['observer']
            obstacles = [flight.box(formation['hover'], flight.METRIC)]
            # The new procedure exits at its actual original root, unlike the
            # old one-control exit. Recheck Flutter's exit against that root.
            previous = formation['hover']
            for target in formation['flight_exit_route']:
                if not flight.flight_segment(pond, plan, previous, target, center, origin):
                    return None, 'Flutter cannot leave past the final actual operator root.'
                previous = target
            speed = minimum_speed(observer)
            other_seconds = travel_seconds(formation['roots']['observer'], formation['flight_route'], speed)
            other_seconds += travel_seconds(formation['hover'], formation['flight_exit_route'], speed)
            available_seconds = formation['remaining_seconds']
        else:
            formation, reason = shared.propose(pond, first_atomic, instance)
            if not formation:
                return None, reason
            mode = 'visitor-operator'
            operator = formation['operator']
            origin = formation['roots']['operator']
            observer = dict(actor='cheese', adapter='cheese', source_age=age,
                            token=str(pond.game.duck.created_at))
            obstacles = [air.box(formation['watch'], shared.cheese_metric(age))]
            other_seconds = travel_seconds(formation['roots']['cheese'], formation['cheese_route'], 1.)
            other_seconds += travel_seconds(formation['watch'], formation['cheese_exit_route'], 1.)
            available_seconds = remaining_seconds(pond, operator)
    else:
        mode = 'solo'
        operator = dict(actor='cheese', adapter='cheese', source_age=age,
                        token=str(pond.game.duck.created_at))
        origin = shared.cheese_root(pond)
    contract, reason = procedure.propose(pond, plan, operator, origin, obstacles,
                                         available_seconds=available_seconds)
    if contract is None:
        return None, reason
    required = procedure.budget(contract, minimum_speed(operator), other_seconds)
    if required > available_seconds:
        return None, 'This visitor cannot finish the whole procedure and both exits before departure.'
    return dict(mode=mode, plan=plan, procedure=contract, formation=formation,
                operator=operator, observer=observer, recipient=recipient,
                obstacles=obstacles, required_seconds=required,
                cheese_identity=str(pond.game.duck.created_at), source_age=pond.game.duck.growth_stage), ''
