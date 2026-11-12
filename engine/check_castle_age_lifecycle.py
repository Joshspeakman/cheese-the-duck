"""Independent age-bound castle lifecycle regressions, with disposable saves.

Run: .venv/bin/python engine/check_castle_age_lifecycle.py
This checks native ownership and rejection paths, not repertoire certification.
"""
import copy
import json
import os
import random
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ['CHEESE_SAVE_DIR'] = tempfile.mkdtemp(prefix='cheese-castle-age-lifecycle-')
os.environ['SDL_AUDIODRIVER'] = 'dummy'
os.environ['SDL_VIDEODRIVER'] = 'dummy'

from engine import host, carnival, castle_work as castle, excursions, terrain
from engine.living_world import LivingPond
from world.habitat import PlacedItem
from world.atmosphere import Weather, WeatherType, Season
from audio.sound import sound_engine

sys.stdout = host.WIRE
random.seed(53)
checks = []


def check(ok, label):
    assert ok, label
    checks.append(label)


terminal = host.DesktopInput()
game = host.DesktopGame(terminal=terminal, renderer_factory=host.CanvasRenderer)
terminal.game = game
game.renderer.game = game
game.renderer.present = lambda lines: None


def fixture(age='adult', placement=(9, 6)):
    pond = game.living_pond
    pond.cancel()
    game.duck.current_action = None
    game.behavior_ai.clear_action()
    game.duck.growth_stage = age
    for name in ('hunger', 'energy', 'fun', 'cleanliness', 'social'):
        setattr(game.duck.needs, name, 95)
    game.duck_store.sync_from_duck(game.duck)
    game.friends.current_visit = None
    game.atmosphere.current_visitor = None
    game.renderer._show_talk = False
    pond.state['story'] = None
    game.habitat.owned_items = ['bounce_house']
    game.habitat.placed_items = [PlacedItem('bounce_house', *placement)]
    game.habitat.stored_items = []
    game.habitat.stored_placements = []
    game.building.structures = []
    for room in game.decorations.rooms.values():
        room.decorations = []
    pos = game.renderer.duck_pos
    pos.cancel_movement()
    pos.x, pos.y = 48, 26
    game.day_night.get_current_hour = lambda: 12
    game.day_night.get_current_minute = lambda: 0
    game.atmosphere.current_season = Season.SPRING
    game.atmosphere.current_weather = Weather(WeatherType.SUNNY, .5, 1, datetime.now().isoformat())
    pond.sync()
    pond.state['auto'] = False
    pond.minds.model.state['next_social'] = 1e9
    pond.weather_type, pond.season, pond.hour = 'sunny', 'spring', 12
    pond.state['ecology'].update(wind=.2, temperature=18)
    pond.state['cooldowns'] = {}
    iid = next(p.instance for p in pond.placements if p.item_id == 'bounce_house')
    obj = pond.object_state('bounce_house', iid)
    obj.update(last_use=-1000, uses=0, dirt=0, wetness=0, condition=1,
               excursion={}, castle={}, carnival_routines={}, carnival_company={})
    excursions.state('bounce_house', obj)
    castle.state(obj).update(motor='off', power_hold=True, latch=1, door=0, hose=0)
    return iid, obj


def request(age='adult', score='castle_door_open', placement=(9, 6)):
    iid, obj = fixture(age, placement)
    ok, message = carnival.request(game.living_pond, 'bounce_house', score, iid)
    check(ok, age + ' production request: ' + message)
    plan = game.living_pond.state['plan']
    return plan, plan['carnival_work'], obj


def step(move=True, dt=.2):
    pond = game.living_pond
    pond.state['elapsed'] += dt
    pos = game.renderer.duck_pos
    if move:
        pos._state_start_time -= dt
        pos.update(dt)
    pond._activity(dt)
    if pond.state['plan']:
        obj = pond.object_state('bounce_house', pond.state['plan'])
        excursions.update('bounce_house', obj, dt, True, pond.weather_type, .2, pond.hour,
                          reserved=carnival.owns(pond, 'bounce_house', obj))


def until(predicate, label):
    for _ in range(1000):
        if predicate():
            return
        step()
    check(False, label)


try:
    game._running = True
    game._start_new_game()
    game._flush_pending_save()
    game._state = 'playing'
    sound_engine.enabled = False
    game.renderer._viewport_width = 132
    game.renderer._viewport_height = 42
    game.renderer._update_camera(132, 42)

    # The buckle is reachable here; the later door grip is not. Refusal must
    # precede that otherwise-valid first material contact and any actual walk.
    iid, obj = fixture('hatchling', (9, 7))
    pos = game.renderer.duck_pos
    root = [pos.x, pos.y]
    ok, message = carnival.request(game.living_pond, 'bounce_house', 'castle_door_open', iid)
    check(not ok and game.living_pond.state['plan'] is None,
          'unreachable future door station rejects the entire request: ' + message)
    check(obj['castle']['latch'] == 1 and obj['castle']['targets']['door'] == 0 and obj['uses'] == 0,
          'future-station refusal does not first unlatch, roll, or reward')
    check([pos.x, pos.y] == root and not pos._is_directed_movement,
          'failed preflight leaves no route or root movement')

    for age in ('unknown-age', 'egg'):
        iid, obj = fixture(age)
        ok, _ = carnival.request(game.living_pond, 'bounce_house', 'castle_start', iid)
        check(not ok and game.living_pond.state['plan'] is None and obj['castle']['motor'] == 'off',
              age + ' cannot fall back to adult or legacy operation')

    plan, work, obj = request('teen', 'castle_start')
    check(work['source_age'] == 'juvenile' and work['physical']['source_age'] == 'juvenile',
          'legacy teen explicitly binds the juvenile rig')
    game.duck.growth_stage = 'juvenile'
    step(move=False)
    check(game.living_pond.state['plan'] is plan and not work.get('interrupted'),
          'canonical alias normalization is not mistaken for physical growth')

    for window in ('transfer', 'paused', 'settling'):
        plan, work, obj = request()
        if window == 'settling':
            until(lambda: bool(work.get('done')), 'reach the completed exit')
            check(game.living_pond.state['plan'] is plan and obj['uses'] == 0,
                  'settling fixture precedes the generic completion reward')
        else:
            until(lambda: work['physical']['station_index'] == 1, 'reach second-leg departure')
            check(work['events'] == [0] and obj['castle']['latch'] == 0,
                  window + ': fixture has an actual consumed unlatch')
            if window == 'paused':
                plan['paused'] = True
                game.living_pond._activity(0)
        events = list(work['events'])
        targets = copy.deepcopy(obj['castle']['targets'])
        game.duck.growth_stage = 'mature'
        step(move=False)
        check(game.living_pond.state['plan'] is None and work.get('interrupted'),
              window + ': age change releases the old reservation before further work')
        check(work['events'] == events and obj['castle']['latch'] == 0 and obj['castle']['targets'] == targets,
              window + ': growth retains exactly the already-consumed material work')
        check(obj['uses'] == 0 and not obj['carnival_routines'],
              window + ': growth never receives completion credit from old geometry')

    # Native exit completion precedes outer-plan settling. Its actual animator
    # must stay at the reached exit even when the next pond tick is delayed.
    plan, work, obj = request('elder', 'castle_door_open')
    until(lambda: bool(work.get('done')), 'reach a completed exit before settling')
    pond = game.living_pond
    pos = game.renderer.duck_pos
    root = [pos.x, pos.y]
    check(pond.state['plan'] is plan and plan['phase'] == 'settle' and obj['uses'] == 0,
          'held-exit fixture still awaits the outer completion callback')
    check(root == work['physical']['root'] == work['physical']['exit'],
          'completed exit records the actual elder root')
    # Force an idle animator's normal wander decision to succeed; retain its
    # real target selection and movement, rather than mocking position writes.
    with patch('duck.animator.random.random', return_value=0), \
            patch.object(pos, '_pick_new_target', wraps=pos._pick_new_target) as wander:
        for _ in range(50):
            pos._state_start_time -= .2
            pos.update(.2)
        check(wander.call_count == 0 and [pos.x, pos.y] == root,
              'done native exit cannot wander while the outer plan still owns its root')
        check(pond.state['plan'] is plan and not work.get('recorded') and obj['uses'] == 0,
              'animator-only settling cannot consume completion or award use')
        settling_roots = []
        while pond.state['plan'] is plan and len(settling_roots) < 100:
            step()
            settling_roots.append([pos.x, pos.y])
    check(bool(settling_roots) and all(point == root for point in settling_roots),
          'actual root stays at the reached exit through outer-plan consumption')
    check(pond.state['plan'] is None and work.get('recorded') is True and
          obj['uses'] == 1 and obj['carnival_routines'] == {'castle_door_open': 1},
          'held exit completes and awards exactly one routine and one generic use')

    # Both recorded age fields can agree yet disagree with the real loaded duck.
    plan, work, obj = request()
    until(lambda: work['events'] == [0], 'reach a press before age-mismatched reload')
    saved = game.living_pond.save()
    original = game.living_pond
    for invalid in ('mature', None, 'unknown-age'):
        forged = copy.deepcopy(saved)
        fw = forged['plan']['carnival_work']
        fw['source_age'] = fw['physical']['source_age'] = invalid
        restored = LivingPond(json.loads(json.dumps(forged)))
        restored_work = restored.state['plan']['carnival_work']
        game.living_pond = restored
        try:
            restored.attach(game, offline=False)
            check(restored_work.get('interrupted') or restored.state['plan'] is None,
                  'reload rejects source age ' + repr(invalid))
            loaded_obj = restored.object_state('bounce_house', plan['instance'])
            check(restored_work['events'] == [0] and loaded_obj['castle']['latch'] == 0 and loaded_obj['uses'] == 0,
                  'rejected age reload preserves consumed effects without credit')
        finally:
            restored.minds.close()
            game.living_pond = original
            original.attach(game, offline=False)

    # Deny water support at the mature rig's actual right foot, which is farther
    # from its root than the old adult constant. Observe production terrain calls.
    plan, work, obj = request('mature', 'castle_start')
    until(lambda: work['stage'] == 'service', 'mature Cheese reaches its stance')
    check(not work['events'], 'wet-foot fixture precedes the switch press')
    root = [game.renderer.duck_pos.x, game.renderer.duck_pos.y]
    foot = [root[0] + 3.5 * (85 / (16 * 7.5)) * 132 / 192, root[1]]
    seen = []
    original_water = terrain.water_at

    def water_at(location, x, y, biome='pond'):
        if abs(x - foot[0]) < 1e-9 and abs(y - foot[1]) < 1e-9:
            seen.append([x, y])
            return True
        return original_water(location, x, y, biome)

    with patch('engine.terrain.water_at', side_effect=water_at):
        step(move=False)
    check(bool(seen), 'support queries the mature drawing\'s actual right foot')
    check(game.living_pond.state['plan'] is None and not work['events'] and obj['castle']['motor'] == 'off',
          'a wet mature foot interrupts before pressing the switch')

    # Being outside the wall by three cells is insufficient for mature feet:
    # each extends 3.5 cells. Reject before moving a foot out through the fabric.
    for side in ('left', 'right'):
        iid, obj = fixture('mature')
        pond = game.living_pond
        center = castle.placement_center(pond, {'instance': iid})
        ground = castle.art_world(center, 0, castle.GEOMETRY['ground_row'])[1]
        left = castle.art_world(center, 0, 0)[0]
        right = castle.art_world(center, castle.GEOMETRY['width'], 0)[0]
        bx = (85 / (16 * 7.5)) * 132 / 192
        pos = game.renderer.duck_pos
        pos.x = left - 3.25 * bx if side == 'left' else right + 3.25 * bx
        pos.y = ground - .2
        root = [pos.x, pos.y]
        ok, _ = carnival.request(pond, 'bounce_house', 'castle_start', iid)
        check(not ok and pond.state['plan'] is None,
              side + ': actual mature foot overlap with castle fabric rejects the route')
        check([pos.x, pos.y] == root and not pos._is_directed_movement and
              obj['castle']['motor'] == 'off' and obj['uses'] == 0,
              side + ': rejected foot overlap neither moves nor presses nor rewards')

    print(json.dumps({'result': 'PASS', 'checks': len(checks), 'scope': 'native-age-lifecycle'}))
finally:
    if game.living_pond:
        game.living_pond.minds.close()
    if getattr(game, '_save_executor', None):
        game._save_executor.shutdown(wait=True)
    if getattr(game, '_talk_executor', None):
        game._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
