"""Transient all-role ownership for complete native air procedures.

The private session is never saved or sent to the renderer. Existing animators
remain the only root writers; the occurrence coordinator alone owns child time.
"""
import copy
import math
from engine import castle_air as air, castle_air_procedure as core, castle_air_roles as roles
from engine import castle_work as castle, castle_shared as shared, castle_actors as actors
from engine import castle_flight as flight, egg_caregiver as egg, shelters

CARE = ('feed', 'play', 'clean', 'pet', 'sleep')


def session(pond, plan=None):
    owner = getattr(pond, '_castle_air_session', None)
    if not isinstance(owner, Session):
        return None
    if plan is not None and owner.plan is not plan:
        return None
    return owner


def available(pond):
    return pond.scene_available()


def ready_for_acquisition(pond):
    duck = pond.game.duck
    return bool(available(pond) and duck and duck.current_action not in CARE
                and duck.needs.energy >= 10 and duck.needs.hunger >= 15)


def start(pond, score, instance=None, together=False, automatic=False):
    if pond.state.get('plan') or not ready_for_acquisition(pond):
        return False, 'Finish the current activity before beginning this procedure.'
    pond.sync()
    if instance is None:
        placed = pond.placed.get('bounce_house')
        instance = placed.instance if placed else None
    proposal, reason = roles.propose(pond, score, instance, together)
    if not proposal:
        return False, reason
    if pond.state['elapsed'] < pond.state['cooldowns'].get('item:' + str(instance), -1):
        return False, 'Give this house a little time before another procedure.'
    owner = Session(pond, proposal, automatic)
    if not owner.acquire():
        return False, 'The participants or working scene changed before the procedure began.'
    return True, owner.work['label'] + '.'


class Session:
    def __init__(self, pond, proposal, automatic):
        self.pond = pond
        self.proposal = copy.deepcopy(proposal)
        self.contract = self.proposal['procedure']
        self.plan = self.proposal['plan']
        self.plan.update(kind='item', location=pond.location, phase='act', elapsed=0.,
                         duration=proposal['required_seconds'], paused=False, automatic=automatic)
        self.work = self.plan['carnival_work']
        self.plan['label'] = self.work['label']
        self.mode = proposal['mode']
        self.operator = self.proposal['operator']
        self.observer = self.proposal['observer']
        self.recipient = self.proposal['recipient']
        self.phase = 'observer_approach' if self.observer else 'operate'
        self.completed = False
        self.receipt = None
        self.node = 'origin'
        self.contexts = {}
        self.guest_key = None
        self.op = dict(version=1, actor=self.operator['actor'], root=list(self.contract['origin']),
                       center=self.contract['center'], phase='hold', route=[self.contract['origin']],
                       waypoint=0, stance=self.contract['origin'], exit=self.contract['origin'],
                       station='gauge', station_index=0, target=air.observation_target(self.contract['center']),
                       contact_ready=False, observation_ready=False)
        self.watch = None
        formation = self.proposal['formation']
        if self.observer:
            flying = self.mode == 'flight-observer'
            origin = formation['roots']['observer' if flying else 'cheese']
            self.watch = dict(root=list(origin), stance=formation['hover' if flying else 'watch'],
                              exit=formation['flight_exit' if flying else 'cheese_exit'],
                              route=formation['flight_route' if flying else 'cheese_route'],
                              waypoint=0, phase='approach', ready=False)
        self.work.update(physical=self.op, shared_physical=self.mode != 'solo',
                         physical_pilot=self.operator['adapter'] == 'cheese',
                         source_age=castle.canonical_age(self.proposal['source_age']) or 'egg', paired=self.mode != 'solo',
                         invitation_checked=True)
        self.work['shared'] = dict(version=1, mode=self.mode, operator=copy.deepcopy(self.operator),
                                   source_age=self.work['source_age'], destination=list(self.plan['destination']), attempt=self.contract['attempt'],
                                   instance=self.contract['instance'], center=self.contract['center'])
        if self.mode == 'flight-observer':
            self.work.update(flight_observer=True)
            self.work['shared'].update(observer=copy.deepcopy(self.observer), observer_physical=self.watch)
        elif self.mode == 'visitor-operator':
            self.work['shared']['cheese'] = self.watch
        elif self.mode == 'egg-caregiver':
            self.work['egg_caregiver'] = True
            self.work['shared']['recipient'] = copy.deepcopy(self.recipient)
        self.motion_snapshot = None
        self.roles_snapshot = None
        self.plan_identity = copy.deepcopy({k: self.plan[k] for k in ('kind', 'target', 'instance', 'location', 'destination', 'phase', 'duration')})
        self.wire_identity = copy.deepcopy({k: self.work[k] for k in ('id', 'source_age', 'physical_pilot', 'shared_physical', 'invitation_checked', 'castle_care')})

    def actual(self, identity):
        if identity is None:
            return None
        if identity.get('cast') == 'butterfly_fairy':
            live = actors.flight(self.pond)
            return live if live and actors.identity(live) == identity else None
        return air.operator_state(self.pond, identity)

    def remember_motion(self):
        self.work['shared']['phase'] = self.phase
        self.motion_snapshot = copy.deepcopy((self.op, self.watch))
        self.roles_snapshot = copy.deepcopy({k: v for k, v in self.work['shared'].items()
                                            if k not in ('cheese', 'observer_physical')})

    def acquire(self):
        p = self.pond
        if p.state.get('plan') or session(p) or not ready_for_acquisition(p) or not self.actual(self.operator):
            return False
        if not shared.near(self.actual(self.operator)['root'], self.contract['origin']):
            return False
        if self.observer and (not self.actual(self.observer) or not shared.near(self.actual(self.observer)['root'], self.watch['root'])):
            return False
        participants = [self.operator] + ([self.observer] if self.observer else [])
        if any(a['adapter'] != 'cheese' and roles.remaining_seconds(p, a) < self.proposal['required_seconds'] for a in participants):
            return False
        if not core.begin(self.work, self.contract, self.proposal['required_seconds']):
            return False
        if not self.scene_ok() or not core.itinerary_clear(p, self.plan, self.contract, self.proposal['obstacles']):
            return False
        self.contexts = {a['actor']: p.minds.context(a['actor']) for a in participants}
        guest = next((a for a in participants if a['adapter'] != 'cheese'), None)
        if guest:
            self.guest_key = guest['actor']
            if self.guest_key in p.minds.carnival_guests:
                return False
            p.minds.carnival_guests[self.guest_key] = dict(
                actor=self.guest_key, work=self.work, attempt=self.contract['attempt'],
                shared=True, flight=self.mode == 'flight-observer', token=guest['token'],
                target=list(self.actual(guest)['root']), spot=list(self.actual(guest)['root']),
                phase='approach', contexts=self.contexts,
                contract=dict(operator=copy.deepcopy(self.operator)))
            p.minds.tasks.pop(self.guest_key, None)
            self.work['companion'] = dict(actor=self.guest_key,
                mode='observer' if self.mode == 'flight-observer' else 'caregiver' if self.recipient else 'operator', ready=False)
        p._castle_air_session = self
        p.state['plan'] = self.plan
        self.remember_motion()
        if not self.observer:
            self.handle(core.next_occurrence(p, self.plan, self.contract))
        self.refresh()
        if self.work.get('interrupted') and p.state.get('plan') is self.plan:
            p.state['plan'] = None
        return not self.work.get('interrupted')

    def scene_ok(self):
        p = self.pond
        if (p.location != self.plan['location'] or str(p.game.duck.created_at) != self.proposal['cheese_identity']
            or p.game.duck.growth_stage != self.proposal['source_age'] or flight.outfitted(p)
            or roles.present_count(p) > (0 if self.mode == 'solo' else 1)
            or castle.placement_center(p, self.plan) != self.contract['center']):
            return False
        if not shelters.still_placed(p, dict(id='bounce_house', instance=self.plan['instance'], destination=self.plan['destination'])):
            return False
        if self.recipient and (egg.recipient(p) != self.recipient or not egg.shell_safe(p, self.plan, self.recipient, self.contract['center'])):
            return False
        if self.mode == 'flight-observer' and not flight.weather_ok(p):
            return False
        wind = p.state.get('ecology', {}).get('wind')
        if type(wind) not in (int, float) or not math.isfinite(wind) or wind < 0 or not castle.allowed(p, self.work['id']):
            return False
        if not self.actual(self.operator) or self.observer and not self.actual(self.observer):
            return False
        for actor in (self.operator, self.observer):
            if actor and actor['adapter'] != 'cheese' and roles.remaining_seconds(p, actor) <= 0:
                return False
        return True

    def valid(self):
        try:
            if (session(self.pond) is not self or self.pond.state.get('plan') is not self.plan and not (self.phase == 'done' and self.pond.state.get('plan') is None)
                or not core._same({k: self.plan.get(k) for k in self.plan_identity}, self.plan_identity)
                or not core._same({k: self.work.get(k) for k in self.wire_identity}, self.wire_identity)
                or self.work is not self.plan.get('carnival_work') or self.work.get('interrupted')
                or self.work.get('recorded') or not core.validate(self.work, self.contract)
                or self.work.get('physical') is not self.op
                or not core._same((self.op, self.watch), self.motion_snapshot)
                or not core._same({k: v for k, v in self.work['shared'].items() if k not in ('cheese', 'observer_physical')}, self.roles_snapshot)
                or not self.scene_ok()):
                return False
            if self.mode == 'flight-observer' and self.work['shared'].get('observer_physical') is not self.watch:
                return False
            if self.mode == 'visitor-operator' and self.work['shared'].get('cheese') is not self.watch:
                return False
            if self.guest_key:
                lease = self.pond.minds.carnival_guests.get(self.guest_key)
                if not isinstance(lease, dict) or lease.get('work') is not self.work or lease.get('attempt') != self.contract['attempt']:
                    return False
            return True
        except (KeyError, TypeError, ValueError, AttributeError):
            return False

    def stopped(self):
        return bool(self.plan.get('paused') or not available(self.pond) or self.pond.game.duck.current_action in CARE)

    def obstacles(self):
        if self.recipient:
            return [egg.box(self.recipient['root'], egg.metric(self.recipient))]
        if self.observer:
            root = self.actual(self.observer)['root']
            metric = flight.METRIC if self.mode == 'flight-observer' else shared.cheese_metric(self.observer['source_age'])
            return [air.box(root, metric)]
        return []

    def segment(self, identity, a, b):
        if identity is self.operator:
            return air.segment_clear(self.pond, self.plan, 'castle_gauge_check', identity, a, b, self.obstacles())
        other = self.actual(self.operator)['root']
        if self.mode == 'flight-observer':
            return flight.flight_segment(self.pond, self.plan, a, b, self.contract['center'], other)
        metric = shared.cheese_metric(self.observer['source_age'])
        return all(shared.support(self.pond, self.plan, r, metric, self.contract['center'])
                   and not air.overlap(air.box(r, metric), air.box(other, air.travel_metric(self.operator)))
                   for r in shared.samples(a, b))

    def command(self, identity, record, target, facing):
        if identity['adapter'] == 'cheese':
            pos = self.pond.game.renderer.duck_pos
            if shared.near([pos.x, pos.y], target, .51):
                current = pos._state_str
                pos.cancel_movement()
                pos.set_state_by_name(current if self.pond.game.duck.current_action in CARE and current in pos.ANIMATABLE_STATES else 'thinking', 0)
                if not self.stopped():
                    pos.facing_right = facing
            elif not pos._is_directed_movement or [pos.target_x, pos.target_y] != target:
                pos.move_to(*target)
        else:
            lease = self.pond.minds.carnival_guests[identity['actor']]
            lease.update(target=list(target), spot=list(target), phase=record['phase'], facing=facing)

    def refresh(self):
        if not self.valid():
            return self.interrupt('The procedure actor, placement or ownership changed.')
        for identity, record in ((self.operator, self.op), (self.observer, self.watch)):
            if not identity:
                continue
            live = self.actual(identity)
            if not self.segment(identity, record['root'], live['root']):
                return self.interrupt('An actual movement segment lost its clear supported corridor.')
            record['root'] = list(live['root'])
        if self.pond.game.duck.needs.energy < 10 or self.pond.game.duck.needs.hunger < 15:
            return self.interrupt('Urgent care interrupted the procedure.')
        if self.phase == 'operate' and self.observer and not shared.near(self.actual(self.observer)['root'], self.watch['stance'], .51 if self.observer['adapter'] == 'cheese' else 1e-7):
            return self.interrupt('The observer left its reserved watching position.')
        if not self.visit_budget_ok():
            return self.interrupt('The visitor no longer has time for the remaining work and exits.')
        stop = self.stopped() or self.phase == 'done'
        for identity, record in ((self.operator, self.op), (self.observer, self.watch)):
            if not identity:
                continue
            moving = not stop and (identity is self.operator and self.phase in ('operate', 'operator_exit')
                                  or identity is self.observer and self.phase in ('observer_approach', 'observer_exit')) and record['phase'] != 'hold'
            target = record['route'][record['waypoint']] if moving else record['root']
            if not self.segment(identity, record['root'], target):
                return self.interrupt('The next reserved movement segment is blocked.')
            facing = True if identity is self.operator else self.op['root'][0] >= record['root'][0]
            self.command(identity, record, target, facing)
        self.op.update(contact_ready=False, observation_ready=False)
        if not stop and self.phase == 'operate' and self.op['phase'] == 'hold' and self.work.get('atomic'):
            air.station_ready(self.pond, self.plan, self.operator, self.op, self.work['atomic']['id'], self.obstacles())
        self.remember_motion()
        self.pond._cache = None
        return True

    def handle(self, result):
        if result['status'] == 'blocked':
            return self.interrupt(result['reason'])
        if result['status'] == 'transfer':
            self.node = result['node']
            self.op.update(result['site'])
            self.op.update(phase='approach', route=result['route'], waypoint=0,
                           contact_ready=False, observation_ready=False)
            if 'observation_target' not in result['site']:
                self.op.pop('observation_target', None)
        elif result['status'] == 'exit':
            self.phase = 'operator_exit'
            self.op.update(phase='exit', route=result['route'], waypoint=0,
                           contact_ready=False, observation_ready=False)
            self.work['stage'] = 'service_exit'
        self.remember_motion()
        return True

    def advance(self, dt):
        if not self.refresh() or self.stopped():
            return
        if self.phase == 'observer_approach':
            if shared.arrived(self.watch, self.actual(self.observer)['root'], .51 if self.observer['adapter'] == 'cheese' else 1e-7):
                self.watch.update(phase='hold', ready=True)
                self.phase = 'operate'
                self.handle(core.next_occurrence(self.pond, self.plan, self.contract))
            self.remember_motion()
            return
        if self.phase in ('operator_exit', 'observer_exit'):
            record, identity = (self.op, self.operator) if self.phase == 'operator_exit' else (self.watch, self.observer)
            if shared.arrived(record, self.actual(identity)['root'], .51 if identity['adapter'] == 'cheese' else 1e-7):
                record.update(phase='hold', exited=True)
                if self.phase == 'operator_exit' and self.observer:
                    self.phase = 'observer_exit'
                    formation = self.proposal['formation']
                    self.watch.update(phase='exit', route=formation['flight_exit_route' if self.mode == 'flight-observer' else 'cheese_exit_route'], waypoint=0)
                else:
                    self.phase = 'done'
                    self.work.update(done=True, stage='done')
            self.remember_motion()
            return
        if self.phase != 'operate':
            return
        if self.op['phase'] == 'approach':
            if not shared.arrived(self.op, self.actual(self.operator)['root'], .51 if self.operator['adapter'] == 'cheese' else 1e-7):
                self.remember_motion()
                return
            self.op['phase'] = 'hold'
            if not core.arrived(self.work, self.contract, self.node):
                return self.interrupt('The actual station occurrence no longer matches its owner.')
        self.remember_motion()
        self.refresh()
        if self.work.get('interrupted'):
            return
        if self.observer and self.actual(self.observer)['facing'] != (self.op['root'][0] >= self.watch['root'][0]):
            return
        context = dict(operator=self.operator, physical=self.op, obstacles=self.obstacles,
                       preflight=lambda: self.visit_budget_ok() and core.itinerary_clear(self.pond, self.plan, self.contract, self.obstacles()))
        self.work['stage'] = 'service'
        self.handle(core.advance(self.pond, self.plan, self.contract, context, dt))

    def interrupt(self, reason):
        self.work.update(interrupted=True, done=True, physical_error=reason)
        self.op.update(contact_ready=False, observation_ready=False)
        self.release()
        return False

    def release(self):
        p = self.pond
        if self.guest_key:
            lease = p.minds.carnival_guests.get(self.guest_key)
            if isinstance(lease, dict) and lease.get('work') is self.work:
                p.minds.carnival_guests.pop(self.guest_key, None)
                self.release_guest(lease)
            elif not isinstance(lease, dict) or not isinstance(lease.get('work'), dict):
                # A malformed row proves no ownership of an actor's target.
                p.minds.carnival_guests.pop(self.guest_key, None)
        if p.state.get('plan') is self.plan:
            if self.operator['adapter'] == 'cheese' or self.observer and self.observer['adapter'] == 'cheese':
                p.game.renderer.duck_pos.cancel_movement()
            castle.clear(p, dict(self.plan, target='bounce_house', instance=self.contract['instance']))
        if session(p) is self:
            p._castle_air_session = None
        p._cache = None

    def release_guest(self, lease):
        if self.operator['adapter'] == 'regular':
            from world.friends import visitor_animator
            meeting = getattr(visitor_animator, '_mind_motion', {}).get('meeting', {})
            actual_target = [visitor_animator._target_x + self.pond.game.renderer._camera_x,
                             visitor_animator._target_y + self.pond.game.renderer._camera_y]
            if not isinstance(meeting, dict) or meeting.get('owner') != self.contract['attempt'] or not shared.near(actual_target, lease.get('target')):
                return
        actors.release_owned(self.pond, self.guest_key, lease)

    def remaining_budget(self):
        if self.phase == 'done':
            return 0.
        op_speed = roles.minimum_speed(self.operator)
        watch_speed = roles.minimum_speed(self.observer) if self.observer else 1.
        formation = self.proposal['formation']
        watch_exit = formation['flight_exit_route' if self.mode == 'flight-observer' else 'cheese_exit_route'] if self.observer else []
        def leg(root, path, speed):
            return roles.travel_seconds(root, path, speed)
        if self.phase == 'observer_exit':
            return leg(self.actual(self.observer)['root'], self.watch['route'][self.watch['waypoint']:], watch_speed)
        observer_tail = leg(self.watch['stance'], watch_exit, watch_speed) if self.observer else 0.
        if self.phase == 'operator_exit':
            return leg(self.actual(self.operator)['root'], self.op['route'][self.op['waypoint']:], op_speed) + observer_tail
        if self.phase == 'observer_approach':
            return core.budget(self.contract, op_speed) + observer_tail + leg(self.actual(self.observer)['root'], self.watch['route'][self.watch['waypoint']:], watch_speed)
        metadata = self.work['air_procedure']
        seconds = observer_tail
        root = self.actual(self.operator)['root']
        node = metadata['node']
        for occurrence in metadata['occurrences']:
            if occurrence['status'] in ('finished', 'skipped'):
                continue
            if occurrence['disposition'] == 'skipped-with-state-reason':
                continue
            child = self.work.get('atomic') if occurrence['status'] == 'active' else None
            if child:
                if self.op['phase'] == 'approach':
                    path = self.op['route'][self.op['waypoint']:]
                    seconds += leg(root, path, op_speed)
                    root, node = path[-1], self.node
                seconds += max(0., castle.ROUTINES[child['id']]['duration'] - child['clock']) + 12.
                sites = occurrence['sites'][self.op['station_index'] + 1:]
            else:
                seconds += castle.ROUTINES[occurrence['atomic_id']]['duration'] + 12.
                sites = occurrence['sites']
            for site in sites:
                target = occurrence['occurrence_id'] + ':' + str(site['station_index'])
                path = self.contract['routes'][node + '>' + target]
                seconds += leg(root, path, op_speed)
                root, node = path[-1], target
        return seconds + leg(root, self.contract['routes'][node + '>exit'], op_speed)

    def visit_budget_ok(self):
        if not self.guest_key:
            return True
        guest = self.observer if self.mode == 'flight-observer' else self.operator
        return roles.remaining_seconds(self.pond, guest) >= self.remaining_budget()

    def completion_ready(self):
        if not self.valid() or self.phase != 'done' or self.completed or self.stopped():
            return False
        for identity in (self.operator, self.observer):
            if identity and not self.segment(identity, self.actual(identity)['root'], self.actual(identity)['root']):
                return False
        if not self.visit_budget_ok():
            return False
        if not shared.near(self.actual(self.operator)['root'], self.contract['origin'], .51 if self.operator['adapter'] == 'cheese' else 1e-7):
            return False
        if self.observer and not shared.near(self.actual(self.observer)['root'], self.watch['exit'], .51 if self.observer['adapter'] == 'cheese' else 1e-7):
            return False
        state = castle.state(self.pond.object_state('bounce_house', self.plan))
        initial = self.contract['initial_power']
        if state['power_revision'] != initial['power_revision'] or state['power_hold'] != initial['power_hold']:
            return False
        # Only final writes to a field define the procedure's final condition;
        # an earlier cleaning stop is intentionally superseded by restore-auto.
        expected = {}
        for occurrence in self.work['air_procedure']['occurrences']:
            execution = occurrence.get('execution')
            if not execution:
                continue
            for _, field, value in castle.ROUTINES[execution['id']]['effects']:
                if field == 'motor':
                    expected['motor'] = execution.get('restore_motor', value) if value == 'on' else value
                elif field in castle.MOVING:
                    expected[field] = value
        if any(state[field] != value if field == 'motor' else abs(state[field] - value) > .001 or state['targets'][field] != value for field, value in expected.items()):
            return False
        for occurrence in self.contract['occurrences']:
            if occurrence['disposition'] == 'skipped-with-state-reason' and core.disposition(occurrence['atomic_id'], state, initial)[0] != 'skipped-with-state-reason':
                return False
        if state['motor'] == 'off' and (state['powered'] or state['rotor_speed'] != 0):
            return False
        for occurrence in reversed(self.work['air_procedure']['occurrences']):
            execution = occurrence.get('execution')
            if execution and any(effect[1] == 'motor' for effect in castle.ROUTINES[execution['id']]['effects']):
                if execution['id'] == 'castle_start' and air.terminal_ready(self.pond, self.plan, execution, {})['status'] != 'ready':
                    return False
                break
        return all(isinstance(context, dict) and actor in self.pond.minds.model.residents
                   for actor, context in self.contexts.items())

    def complete(self):
        if not self.completion_ready():
            return False
        receipt = core.finish_exit(self.work, self.contract, True)
        if receipt is None:
            return self.interrupt('The whole procedure has no valid completion receipt.')
        self.receipt = receipt
        self.completed = True
        self.work['recorded'] = True
        p = self.pond
        minds = p.minds
        reader = self.operator['actor']
        name = minds.model.residents[reader]['name']
        for reading in receipt['observations']:
            note = name + ' read the pressure dial at ' + str(reading['pressure']) + ' during ' + self.work['label'] + '.'
            minds.model.learn(reader, 'observe', self.contexts[reader], .25, minds.now, note, None)
        if receipt['mechanical_contacts']:
            minds.model.learn(reader, 'practice', self.contexts[reader], .25, minds.now,
                              name + ' completed the actual control work: ' + self.work['label'] + '.', None)
        if self.observer:
            watcher = self.observer['actor']
            note = minds.model.residents[watcher]['name'] + ' watched ' + name + ' complete ' + self.work['label'] + '.'
            minds.model.learn(watcher, 'observe', self.contexts[watcher], .2, minds.now, note, reader)
            for actor, other in ((reader, watcher), (watcher, reader)):
                minds.model.learn(actor, 'share', self.contexts[actor], .25, minds.now, note, other)
        elif self.recipient:
            minds.model.learn(reader, 'share', self.contexts[reader], .25, minds.now,
                              name + ' cared for the house beside the stationary egg.', 'cheese')
        obj = p.object_state('bounce_house', self.plan)
        ledger = obj.setdefault('carnival_routines', {})
        ledger[self.work['id']] = min(9999, ledger.get(self.work['id'], 0) + 1)
        if self.guest_key:
            ledger = obj.setdefault('carnival_company', {})
            ledger[self.guest_key] = min(9999, ledger.get(self.guest_key, 0) + 1)
        if self.recipient:
            ledger = obj.setdefault('egg_caregiving', {})
            ledger[reader] = min(9999, ledger.get(reader, 0) + 1)
        obj['active'] = False
        self.release()
        return True


def validate(pond, plan):
    owner = session(pond, plan)
    return bool(owner and owner.valid())


def refresh(pond):
    owner = session(pond, pond.state.get('plan'))
    if owner:
        owner.refresh()


def advance(pond, plan, dt):
    owner = session(pond, plan)
    if not owner:
        return False
    owner.advance(dt)
    return not owner.work.get('interrupted') and owner.phase != 'done'


def interrupt(pond, plan, reason):
    owner = session(pond, plan)
    if owner:
        return owner.interrupt(reason)
    return False


def cancel(pond, plan):
    return interrupt(pond, plan, 'The procedure was set aside.')


def completion_ready(pond, plan):
    owner = session(pond, plan)
    return bool(owner and owner.completion_ready())


def complete(pond, plan):
    owner = session(pond, plan)
    if not owner:
        return False
    if owner.complete():
        return True
    if not owner.completed:
        owner.interrupt('The procedure callback arrived without valid completed exits.')
    return False


def tick(pond, dt):
    plan = pond.state.get('plan')
    owner = session(pond, plan)
    if not owner:
        if plan:
            pond.cancel()
        return
    owner.advance(dt)
    if owner.work.get('interrupted'):
        if pond.state.get('plan') is plan:
            pond.state['plan'] = None
        return
    if owner.phase == 'done':
        if owner.stopped():return
        if not owner.complete():
            owner.interrupt('The final roles or mechanical response changed before completion.')
        if pond.state.get('plan') is plan:
            pond.state['plan'] = None
        pond.state['cooldowns']['item:' + str(plan['instance'])] = pond.state['elapsed'] + 30
    pond._cache = None


def motion(minds, key):
    owner = session(minds.pond, minds.pond.state.get('plan'))
    lease = minds.carnival_guests.get(key)
    if not owner or not owner.valid() or not isinstance(lease, dict) or lease.get('work') is not owner.work:
        return None
    return dict(target=list(lease['target']), phase=lease['phase'], facing=lease.get('facing', True),
                gesture='idle', owner=owner.contract['attempt'])


def view(pond, plan):
    owner = session(pond, plan)
    if not owner or not owner.valid():
        return dict(id=plan.get('carnival_work', {}).get('id'), air_procedure=None)
    result = copy.deepcopy(owner.work)
    operator_root = owner.actual(owner.operator)['root']
    changed = result['physical']['root'] != operator_root
    result['physical']['root'] = list(operator_root)
    if owner.observer:
        observer_root = owner.actual(owner.observer)['root']
        record = result['shared']['observer_physical' if owner.mode == 'flight-observer' else 'cheese']
        changed = changed or record['root'] != observer_root
        record['root'] = list(observer_root)
    if changed:
        result['physical'].update(contact_ready=False, observation_ready=False)
    return result


def conversation(pond, plan, key='cheese'):
    owner = session(pond, plan)
    if not owner or not owner.valid() or key not in owner.contexts:
        return None
    state = castle.state(pond.object_state('bounce_house', plan))
    is_reader = key == owner.operator['actor']
    readings = [dict(occurrence=r['occurrence_id'], pressure=r['pressure'])
                for r in owner.work['air_procedure']['observations']] if is_reader else []
    child = owner.work.get('atomic')
    if is_reader and child and child.get('inspection'):
        readings.append(dict(occurrence=child['occurrence_id'], pressure=child['inspection']['pressure']))
    return dict(object='bounce house', activity=owner.work['label'], stage=owner.phase,
                role='operator' if is_reader else 'observer',
                current_occurrence=owner.work['air_procedure']['current_occurrence'],
                paused=owner.stopped(), last_read_pressure=readings[-1]['pressure'] if readings else None,
                motor=state['motor'], fan_turning=state['rotor_speed'] > 0, observations=readings,
                perspective='Uses the controls and can describe actual dial readings.' if is_reader
                else 'Watches the operator from a separate spot; has not read or operated the controls.')
