"""Independent shared-control lifecycle checks using disposable game state.

The real DesktopGame update dispatch, VisitorAnimator and camera transform run;
unrelated base-game timers and ambient brain decisions are isolated. This is
adversarial lifecycle coverage, not the separate 40-profile acceptance matrix.
"""
import copy
import json
import os
import random
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ['CHEESE_SAVE_DIR'] = tempfile.mkdtemp(prefix='cheese-shared-lifecycle-')
os.environ['SDL_AUDIODRIVER'] = 'dummy'
os.environ['SDL_VIDEODRIVER'] = 'dummy'

from engine import host, carnival, castle_work, excursions
from engine.living_world import LivingPond, PLANS
from world.atmosphere import Weather, WeatherType, Season
from world.friends import visitor_animator, DuckPersonalityType
from world.guest_cast import PROFILES
from world.habitat import PlacedItem
from audio.sound import sound_engine

sys.stdout = host.WIRE
random.seed(59)
checks = []
clock = time.time()
terminal = host.DesktopInput()
game = host.DesktopGame(terminal=terminal, renderer_factory=host.CanvasRenderer)
terminal.game = game
game.renderer.game = game
game.renderer.present = lambda lines: None


def check(ok, label):
    assert ok, label
    checks.append(label)


def close_points(a, b):
    return len(a) == len(b) and all(abs(x-y) < 1e-9 for x, y in zip(a, b))


def guest_root():
    return [visitor_animator._position_x + game.renderer._camera_x,
            visitor_animator._position_y + game.renderer._camera_y]


def cheese_root():
    return [game.renderer.duck_pos.x, game.renderer.duck_pos.y]


def fixture(age='hatchling', cast='friend:ada'):
    pond = game.living_pond
    pond.cancel()
    for name in ('carnival_retry', 'nest_helpers', 'playmates', 'structure_helpers',
                 'ground_helpers', 'textile_helpers', 'creators', 'readers',
                 'housing', 'furnishings', 'gardening', 'musicians', 'coactivities', 'tasks'):
        getattr(pond.minds, name).clear()
    game.friends.current_visit = None
    game.atmosphere.current_visitor = None
    game.guest_motion.actor = game.story_motion.actor = None
    pond.state['story'] = None
    game.duck.current_action = None
    game.behavior_ai.clear_action()
    game.duck.growth_stage = age
    for need in ('hunger', 'energy', 'fun', 'cleanliness', 'social'):
        setattr(game.duck.needs, need, 95)
    game.duck_store.sync_from_duck(game.duck)
    game.renderer._show_talk = False
    game.habitat.owned_items = ['bounce_house']
    game.habitat.placed_items = [PlacedItem('bounce_house', 9, 7)]
    game.habitat.stored_items = []
    game.habitat.stored_placements = []
    game.building.structures = []
    for room in game.decorations.rooms.values():
        room.decorations = []
    pos = game.renderer.duck_pos
    pos.cancel_movement()
    pos.x, pos.y = 48, 26
    game.renderer._viewport_width, game.renderer._viewport_height = 132, 42
    game.renderer._update_camera(132, 42)
    game.day_night.get_current_hour = lambda: 12
    game.day_night.get_current_minute = lambda: 0
    game.atmosphere.current_season = Season.SPRING
    game.atmosphere.current_weather = Weather(WeatherType.SUNNY, .5, 1, datetime.now().isoformat())
    pond.sync()
    pond.weather_type, pond.season, pond.hour = 'sunny', 'spring', 12
    pond.state['auto'] = False
    pond.state['ecology'].update(wind=.2, temperature=18)
    pond.state['cooldowns'] = {}
    iid = next(p.instance for p in pond.placements if p.item_id == 'bounce_house')
    obj = pond.object_state('bounce_house', iid)
    obj.update(last_use=-1000, uses=0, dirt=0, wetness=0, condition=1,
               excursion={}, castle={}, carnival_routines={}, carnival_company={})
    excursions.state('bounce_house', obj)
    castle_work.state(obj).update(motor='off', power_hold=True, latch=1, door=0, hose=0)
    profile = PROFILES[cast]
    friend = game.friends.generate_new_friend()
    friend.name = profile['name']
    friend.personality = DuckPersonalityType(profile['archetype'])
    ok, message, visit = game.friends.start_visit(friend.id)
    assert ok, message
    visitor_animator.set_visitor(profile['archetype'], profile['name'], duck_ref=game.duck)
    visitor_animator._position_x = 72 - game.renderer._camera_x
    visitor_animator._position_y = 25 - game.renderer._camera_y
    visitor_animator._target_x = visitor_animator._position_x
    visitor_animator._target_y = visitor_animator._position_y
    visitor_animator._last_move_time = clock
    visitor_animator._mind_motion = {}
    pond.minds.sync()
    pond.minds.model.residents[friend.id]['energy'] = .95
    pond.minds.tasks[friend.id] = dict(action='observe', until=pond.minds.now+1000,
                                      context=pond.minds.context(friend.id))
    return pond, iid, obj, friend.id


def request(score='castle_door_open', **kwargs):
    pond, iid, obj, key = fixture(**kwargs)
    ok, message = carnival.request(pond, 'bounce_house', score, iid, together=True)
    check(ok, 'explicit together request: ' + message)
    plan = pond.state['plan']
    return pond, plan, plan['carnival_work'], obj, key


def step(dt=.2):
    global clock
    pond = game.living_pond
    clock += dt

    def base_update(_game):
        pos = game.renderer.duck_pos
        pos._state_start_time -= dt
        pos.update(dt)
        visitor_animator.update(clock, pos.x, pos.y)

    def pond_tick():
        pond.state['elapsed'] += dt
        pond._activity(dt)
        if pond.state['plan']:
            obj = pond.object_state('bounce_house', pond.state['plan'])
            excursions.update('bounce_house', obj, dt, True, pond.weather_type, .2, 12,
                              reserved=carnival.owns(pond, 'bounce_house', obj))

    def minds_tick():
        pond.minds.sync()
        carnival.tick(pond.minds, dt)

    with patch.object(host.Game, '_update', base_update), \
            patch.object(pond, 'tick', pond_tick), \
            patch.object(pond.minds, 'tick', minds_tick), \
            patch.object(game.guest_motion, 'tick'), patch.object(game.story_motion, 'tick'):
        game._update()


def until(predicate, label):
    for _ in range(1500):
        if predicate():
            return
        step()
    raise AssertionError(label + ': ' + repr(game.living_pond.state.get('plan')))


def ownership(pond, obj):
    return copy.deepcopy(dict(plan=pond.state['plan'], object=obj, tasks=pond.minds.tasks,
                              leases=pond.minds.carnival_guests, brains=pond.minds.model.state,
                              cheese=cheese_root(), guest=guest_root(),
                              cheese_target=[game.renderer.duck_pos.target_x, game.renderer.duck_pos.target_y],
                              guest_target=[visitor_animator._target_x, visitor_animator._target_y]))


def rewards(pond, obj, key):
    return copy.deepcopy(dict(uses=obj['uses'], routines=obj['carnival_routines'],
                              company=obj['carnival_company'], skills=pond.state['skills'],
                              needs={k: getattr(game.duck.needs, k) for k in ('hunger', 'energy', 'fun', 'cleanliness', 'social')},
                              brains={k: pond.minds.model.residents[k] for k in ('cheese', key)}))


try:
    game._running = True
    game._start_new_game()
    game._flush_pending_save()
    game._state = 'playing'
    sound_engine.enabled = False

    for invalid in ('wet_route', 'reserved', 'animator_identity'):
        pond, iid, obj, key = fixture()
        if invalid == 'reserved':
            pond.minds.readers[key] = {'owner': 'independent-reader'}
        elif invalid == 'animator_identity':
            visitor_animator._friend_name = 'Previous visitor'
        before = ownership(pond, obj)
        if invalid == 'wet_route':
            with patch('engine.terrain.water_at', return_value=True):
                ok, _ = carnival.request(pond, 'bounce_house', 'castle_door_open', iid, together=True)
        else:
            ok, _ = carnival.request(pond, 'bounce_house', 'castle_door_open', iid, together=True)
        check(not ok, invalid + ' rejects before shared acquisition')
        check(ownership(pond, obj) == before,
              invalid + ' leaves materials, brains, tasks, leases, positions and targets unchanged')

    pond, iid, obj, key = fixture()
    ok, message = carnival.request(pond, 'bounce_house', 'castle_start', iid)
    check(ok, 'existing solo plan fixture: ' + message)
    before = ownership(pond, obj)
    ok, _ = carnival.request(pond, 'bounce_house', 'castle_door_open', iid, together=True)
    check(not ok and ownership(pond, obj) == before,
          'shared request cannot replace a prior plan, route, task or reservation')

    for replacement in ('old_owned_target', 'new_target'):
        pond, plan, work, obj, key = request()
        initial_guest = guest_root()
        until(lambda: not close_points(guest_root(), initial_guest), 'reach moving helper replacement')
        root = guest_root()
        target = [visitor_animator._target_x + game.renderer._camera_x,
                  visitor_animator._target_y + game.renderer._camera_y]
        assert not close_points(root, target), 'replacement fixture must still be moving'
        if replacement == 'new_target':
            target = [root[0] + 2, root[1]]
            visitor_animator._target_x = target[0] - game.renderer._camera_x
            visitor_animator._target_y = target[1] - game.renderer._camera_y
        game.friends.current_visit.started_at = 'replacement-during-approach'
        step()
        current_target = [visitor_animator._target_x + game.renderer._camera_x,
                          visitor_animator._target_y + game.renderer._camera_y]
        check(pond.state['plan'] is None and not pond.minds.carnival_guests and
              not work['events'] and obj['uses'] == 0,
              replacement + ': moving visit replacement releases before a contact or reward')
        if replacement == 'old_owned_target':
            check(close_points(guest_root(), root) and close_points(current_target, root),
                  'replacement visit cannot take one last step toward the old owned destination')
        else:
            check(close_points(current_target, target) and not close_points(guest_root(), root),
                  'release preserves a replacement visit destination that the old attempt does not own')

    pond, plan, work, obj, key = request()
    initial_guest = guest_root()
    until(lambda: not close_points(guest_root(), initial_guest), 'reach a premature moving completion callback')
    root = guest_root()
    before = rewards(pond, obj, key)
    pond._complete(plan)
    check(rewards(pond, obj, key) == before and not pond.minds.carnival_guests,
          'premature shared callback releases its lease without any generic or social reward')
    step()
    target = [visitor_animator._target_x + game.renderer._camera_x,
              visitor_animator._target_y + game.renderer._camera_y]
    check(close_points(guest_root(), root) and close_points(target, root) and
          pond.state['plan'] is None and work.get('interrupted') and not work['events'] and
          rewards(pond, obj, key) == before,
          'premature callback releases the owned moving destination before the next host update')

    pond, plan, work, obj, key = request()
    before = rewards(pond, obj, key)
    initial_guest = guest_root()
    check(carnival.conversation(pond, plan, 'cheese')['role'] == 'observer' and
          carnival.conversation(pond, plan, key)['role'] == 'operator',
          'natural chat describes the actual shared operator and observer without legacy lease fields')
    check(carnival.conversation(pond, plan, 'unrelated-visitor') is None,
          'natural chat does not assign the activity to an unrelated visitor')
    until(lambda: not close_points(guest_root(), initial_guest), 'helper begins its own approach')
    check(not work['events'] and rewards(pond, obj, key) == before,
          'independent approach consumes no contact or shared reward')
    plan['paused'] = True
    game.duck.current_action = 'feed'
    game.renderer.duck_pos.set_state_by_name('eating', 0)
    roots = cheese_root(), guest_root()
    progress = work['clock'], list(work['events'])
    step()
    check(close_points(cheese_root(), roots[0]) and close_points(guest_root(), roots[1]),
          'pause before the host update holds both actual roots before base movement')
    camera = game.renderer._camera_x, game.renderer._camera_y
    game.renderer._viewport_width, game.renderer._viewport_height = 70, 25
    game.renderer._update_camera(70, 25)
    check(camera != (game.renderer._camera_x, game.renderer._camera_y),
          'camera fixture scrolls through the real CanvasRenderer transform')
    for _ in range(6):
        step()
    check(close_points(cheese_root(), roots[0]) and close_points(guest_root(), roots[1]) and
          (work['clock'], work['events']) == progress,
          'paused camera scroll preserves native roots and consumes no score time')
    check(game.renderer.duck_pos.get_state() == 'eating',
          'shared pause preserves current direct-care art')
    game._state = 'menu'
    for _ in range(3):
        step()
    check(close_points(cheese_root(), roots[0]) and close_points(guest_root(), roots[1]),
          'nonplaying host updates retain shared holds instead of restoring wandering')
    game._state = 'playing'
    plan['paused'] = False
    game.duck.current_action = None
    until(lambda: bool(work['events']), 'real helper consumes its first contact')
    check(work['events'] == [0] and obj['castle']['latch'] == 0,
          'independent helper reaches the actual first mechanical event')
    from engine.scene import snapshot
    published = snapshot(game, game.renderer)['living']['plan']['carnival_work']
    check(published['physical']['contact_ready'] and published['events'] == [0],
          'completed host update publishes the real held contact after minds refresh')
    check(game.renderer.duck_pos.facing_right == (guest_root()[0] >= cheese_root()[0]),
          'actual observer faces the independently arrived operator at its first contact')
    after_contact = rewards(pond, obj, key)
    game.friends.current_visit.started_at = 'replacement-visit'
    step()
    check(pond.state['plan'] is None and work.get('interrupted') and not pond.minds.carnival_guests,
          'replacement visit interrupts and releases the shared attempt')
    check(work['events'] == [0] and obj['castle']['latch'] == 0 and rewards(pond, obj, key) == after_contact,
          'visit replacement retains the consumed latch without completion or social reward')

    pond, plan, work, obj, key = request('castle_door_open')
    before = rewards(pond, obj, key)
    until(lambda: pond.state['plan'] is None, 'shared control completes through both exits')
    check(work.get('recorded') and not work.get('interrupted') and obj['uses'] == 1 and
          obj['carnival_routines'] == {'castle_door_open': 1},
          'shared success claims one mechanical routine and one object use')
    after = rewards(pond, obj, key)
    old_counts = before['brains']['cheese']['counts']
    counts = after['brains']['cheese']['counts']
    check(counts['item'] == old_counts['item'] and counts['observe'] > old_counts['observe'] and
          counts['share'] > old_counts['share'],
          'Cheese learns completed observation and sharing without false operator learning')
    observation_skill = PLANS['observe'][2]
    check(after['skills'][observation_skill] > before['skills'][observation_skill] and
          all(after['skills'][k] == value for k, value in before['skills'].items() if k != observation_skill),
          'observer Cheese receives no unrelated operator skill gain')
    pond._complete(plan)
    pond._complete(plan)
    check(rewards(pond, obj, key) == after,
          'duplicate shared callbacks award no item, need, skill, bond or learning changes')

    pond, plan, work, obj, key = request()
    until(lambda: bool(work['events']), 'reach a consumed contact before paused growth')
    before = rewards(pond, obj, key)
    plan['paused'] = True
    game.duck.growth_stage = 'duckling'
    step()
    check(pond.state['plan'] is None and work.get('interrupted') and not pond.minds.carnival_guests,
          'growth during pause invalidates both shared roles before movement resumes')
    check(work['events'] == [0] and obj['castle']['latch'] == 0 and rewards(pond, obj, key) == before,
          'paused growth retains consumed material without completing the shared scene')

    pond, plan, work, obj, key = request()
    until(lambda: bool(work['events']), 'reach a consumed contact before shared reload')
    saved = json.loads(json.dumps(pond.save()))
    restored = LivingPond(saved)
    saved_work = restored.state['plan']['carnival_work']
    before = rewards(pond, obj, key)
    game.living_pond = restored
    try:
        restored.attach(game, offline=False)
        restored._activity(0)
        loaded_obj = restored.object_state('bounce_house', plan['instance'])
        check(restored.state['plan'] is None and saved_work.get('interrupted') and not restored.minds.carnival_guests,
              'reload interrupts the saved attempt without reviving a visitor lease')
        check(saved_work['events'] == [0] and loaded_obj['castle']['latch'] == 0 and
              rewards(restored, loaded_obj, key) == before,
              'shared reload keeps the applied contact and no completion reward')
    finally:
        restored.minds.close()
        game.living_pond = pond

    for malformed in ('shared_list', 'operator_list', 'actor_list', 'route_point', 'flag_false', 'flag_missing', 'flag_string'):
        pond, plan, work, obj, key = request()
        before = rewards(pond, obj, key)
        if malformed == 'shared_list':work['shared'] = []
        elif malformed == 'operator_list':work['shared']['operator'] = []
        elif malformed == 'actor_list':work['shared']['operator']['actor'] = []
        elif malformed == 'route_point':work['physical']['route'][0] = [None, 0]
        elif malformed == 'flag_false':work['shared_physical'] = False
        elif malformed == 'flag_missing':work.pop('shared_physical')
        else:work['shared_physical'] = 'true'
        step()
        check(pond.state['plan'] is None and not pond.minds.carnival_guests and obj['castle']['latch'] == 1,
              malformed + ' fails closed and releases the exact attempt without a contact')
        check(rewards(pond, obj, key) == before,
              malformed + ' earns no completion or learning reward')

    print(json.dumps({'result': 'PASS', 'checks': len(checks), 'scope': 'independent-shared-lifecycle'}))
finally:
    if game.living_pond:
        game.living_pond.minds.close()
    if getattr(game, '_save_executor', None):
        game._save_executor.shutdown(wait=True)
    if getattr(game, '_talk_executor', None):
        game._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
