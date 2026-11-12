"""Focused adult-solo castle lifecycle regressions, using disposable saves.

Run from the repository root: .venv/bin/python engine/check_castle_lifecycle.py
This covers pause ownership, invalid saved progress, and a new DesktopGame's
real disk load. It does not certify the other castle scores, ages, or visitors.
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
SAVE_DIR = Path(tempfile.mkdtemp(prefix='cheese-castle-lifecycle-'))
os.environ['CHEESE_SAVE_DIR'] = str(SAVE_DIR)
os.environ['SDL_AUDIODRIVER'] = 'dummy'
os.environ['SDL_VIDEODRIVER'] = 'dummy'

from engine import host, carnival, castle_work as castle, excursions
from engine.living_world import LivingPond
from engine.scene import snapshot
from world.habitat import PlacedItem
from world.atmosphere import Weather, WeatherType, Season
from audio.sound import sound_engine

sys.stdout = host.WIRE
random.seed(49)
checks = []
games = []


def check(ok, label):
    assert ok, label
    checks.append(label)


def new_game(start=False):
    terminal = host.DesktopInput()
    game = host.DesktopGame(terminal=terminal, renderer_factory=host.CanvasRenderer)
    games.append(game)
    terminal.game = game
    game.renderer.game = game
    game.renderer.present = lambda lines: None
    game._running = True
    if start:
        game._start_new_game()
        game._flush_pending_save()
    game._state = 'playing'
    game.renderer._show_talk = False
    game.renderer._viewport_width = 132
    game.renderer._viewport_height = 42
    game.renderer._update_camera(132, 42)
    sound_engine.enabled = False
    return game


def conditions(game):
    pond = game.living_pond
    pond.state['auto'] = False
    pond.minds.model.state['next_social'] = 1e9
    game.day_night.get_current_hour = lambda: 12
    game.day_night.get_current_minute = lambda: 0
    game.atmosphere.current_season = Season.SPRING
    game.atmosphere.current_weather = Weather(WeatherType.SUNNY, .5, 1, datetime.now().isoformat())
    pond.sync()
    pond.weather_type = 'sunny'
    pond.season = 'spring'
    pond.hour = 12
    pond.state['ecology'].update(wind=.2, temperature=18)


def reset(game, placement=(9, 7)):
    pond = game.living_pond
    pond.cancel()
    game.duck.current_action = None
    game.behavior_ai.clear_action()
    game.duck.growth_stage = 'adult'
    for name in ('energy', 'hunger', 'fun', 'cleanliness', 'social'):
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
    pos.x, pos.y = 48, 24
    conditions(game)
    pond.state['cooldowns'] = {}
    iid = next(p.instance for p in pond.placements if p.item_id == 'bounce_house')
    obj = pond.object_state('bounce_house', iid)
    obj.update(last_use=-1000, uses=0, dirt=0, wetness=0, condition=1,
               excursion={}, castle={}, carnival_routines={}, carnival_company={})
    excursions.state('bounce_house', obj)
    castle.state(obj).update(motor='off', power_hold=True)
    ok, message = carnival.request(pond, 'bounce_house', 'castle_start', iid)
    check(ok, 'production request succeeds: ' + message)
    plan = pond.state['plan']
    return plan, plan['carnival_work'], obj


def step(game, move=True, dt=.2):
    pond = game.living_pond
    pond.state['elapsed'] += dt
    pos = game.renderer.duck_pos
    if move:
        pos._state_start_time -= dt
        pos.update(dt)
    pond._activity(dt)
    plan = pond.state['plan']
    if plan:
        obj = pond.object_state('bounce_house', plan)
        excursions.update('bounce_house', obj, dt, True, pond.weather_type, .2, pond.hour,
                          reserved=carnival.owns(pond, 'bounce_house', obj))


def until(game, predicate, label, limit=900):
    for _ in range(limit):
        if predicate():
            return
        step(game)
    check(False, label)


def animator_only(game, updates=30):
    """Force the old idle-wander trigger between simulation activity ticks."""
    pos = game.renderer.duck_pos
    pos._idle_timer = 10
    with patch('duck.animator.random.random', return_value=0), \
            patch('duck.animator.random.randint', side_effect=lambda low, high: int(high)):
        for _ in range(updates):
            pos._state_start_time -= .2
            pos.update(.2)


def reject_saved(game, saved, label):
    original = game.living_pond
    restored = LivingPond(json.loads(json.dumps(saved)))
    game.living_pond = restored
    try:
        restored.attach(game, offline=False)
        plan = restored.state['plan']
        work = plan['carnival_work']
        obj = restored.object_state('bounce_house', plan)
        check(work.get('interrupted'), label + ': attach rejects the record without crashing')
        restored.command({'action': 'resume'})
        until(game, lambda: restored.state['plan'] is None, label + ': rejected plan releases')
        check(obj['uses'] == 0 and not obj['carnival_routines'], label + ': no completion credit')
        check(not work['events'] and obj['castle']['motor'] == 'off', label + ': no invented contact')
    finally:
        restored.minds.close()
        game.living_pond = original
        original.attach(game, offline=False)


try:
    game = new_game(start=True)
    for reason in ('paused', 'unavailable', 'direct_care'):
        plan, work, obj = reset(game)
        pos = game.renderer.duck_pos
        if reason == 'paused':
            plan['paused'] = True
        elif reason == 'unavailable':
            game.renderer._show_talk = True
        else:
            game.duck.current_action = 'feed'
            pos.set_state_by_name('eating', 3)
        game.living_pond._activity(.2)
        root = [pos.x, pos.y]
        animator_only(game)
        check([pos.x, pos.y] == root and not pos._is_directed_movement,
              reason + ': old idle timer cannot move Cheese between activity ticks')
        check(work['clock'] == 0 and not work['events'] and obj['uses'] == 0,
              reason + ': paused movement earns no contact or completion')
        if reason == 'direct_care':
            check(pos.get_state_name() == 'eating' and game.duck.current_action == 'feed',
                  'direct care keeps its own animation while travel is suspended')
        game.renderer._show_talk = False
        game.duck.current_action = None
        game.living_pond.command({'action': 'resume'})
        game.living_pond._activity(.2)
        check([pos.x, pos.y] == root and pos._is_directed_movement,
              reason + ': resume reissues walking without teleporting')

    plan, work, _ = reset(game)
    saved = game.living_pond.save()
    bad_exit = copy.deepcopy(saved)
    bad_exit['plan']['carnival_work']['physical']['phase'] = 'exit'
    reject_saved(game, bad_exit, 'premature saved exit')
    bad_id = copy.deepcopy(saved)
    bad_id['plan']['carnival_work']['id'] = []
    reject_saved(game, bad_id, 'unhashable saved pilot ID')

    # The full game does not serialize animator position. Place the house so the
    # fresh animator's default root has a valid exterior route to reacquire.
    plan, work, obj = reset(game, placement=(9, 6))
    until(game, lambda: bool(work['events']), 'original game reaches the switch')
    check(work['events'] == [0] and obj['castle']['motor'] == 'on' and obj['uses'] == 0,
          'disk fixture saves an actual consumed press before completion')
    saved_root = [game.renderer.duck_pos.x, game.renderer.duck_pos.y]
    iid = plan['instance']
    game._save_game()
    game._flush_pending_save()
    check(game.save_manager.save_path.resolve().is_relative_to(SAVE_DIR.resolve()),
          'full-game save is confined to the disposable directory')
    disk = json.loads(game.save_manager.save_path.read_text())
    check(disk['living_pond']['plan']['carnival_work']['events'] == [0],
          'production serializer writes the consumed contact')

    fresh = new_game()
    fresh_pos = fresh.renderer.duck_pos
    fresh_root = [fresh_pos.x, fresh_pos.y]
    check(fresh_pos is not game.renderer.duck_pos and fresh_root != saved_root,
          'reload uses a distinct game and animator at a different actual root')
    fresh._load_game()
    fresh._state = 'playing'
    conditions(fresh)
    loaded = fresh.living_pond
    loaded_plan = loaded.state['plan']
    loaded_work = loaded_plan['carnival_work']
    loaded_obj = loaded.object_state('bounce_house', loaded_plan)
    check(loaded_plan['instance'] == iid and loaded_plan['paused'] and
          [fresh_pos.x, fresh_pos.y] == fresh_root and not loaded_work.get('interrupted'),
          'fresh full-game load preserves exact copy and actual root, paused')
    check(loaded_work['events'] == [0] and loaded_obj['castle']['motor'] == 'on' and loaded_obj['uses'] == 0,
          'fresh full-game load retains the press without completion credit')
    check(loaded_work['physical']['phase'] == 'approach' and
          loaded_work['physical']['contact_ready'] is False,
          'fresh load must reacquire native support and arrival')
    animator_only(fresh)
    check([fresh_pos.x, fresh_pos.y] == fresh_root,
          'freshly restored pause remains stationary between native ticks')
    loaded.command({'action': 'resume'})
    until(fresh, lambda: loaded.state['plan'] is None, 'freshly loaded pilot completes')
    check(loaded_work['events'] == [0] and loaded_obj['uses'] == 1 and
          loaded_obj['carnival_routines'].get('castle_start') == 1,
          'fresh load resumes actual walking and completes once without replaying contact')
    frame = snapshot(fresh, fresh.renderer)
    check(frame['living']['plan'] is None, 'completed fresh-game snapshot releases its activity')
    print(json.dumps({'result': 'PASS', 'checks': len(checks),
                      'pilot': 'adult-solo-castle_start', 'freshGameDiskLoad': True}))
finally:
    for game in reversed(games):
        if game.living_pond:
            game.living_pond.minds.close()
        if getattr(game, '_save_executor', None):
            game._save_executor.shutdown(wait=True)
        if getattr(game, '_talk_executor', None):
            game._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
