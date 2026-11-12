"""Pip has one body across visitor/story paths; disposable game and saves."""
import copy
import json
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ['CHEESE_SAVE_DIR'] = tempfile.mkdtemp(prefix='cheese-presence-')
os.environ['SDL_AUDIODRIVER'] = 'dummy'
os.environ['SDL_VIDEODRIVER'] = 'dummy'
from engine import host, carnival, castle_shared, castle_work, excursions
from engine.pond_stories import STORIES
from engine.scene import snapshot
from world.atmosphere import VISITORS, Season, Weather, WeatherType
from world.habitat import PlacedItem
from audio.sound import sound_engine

sys.stdout = host.WIRE
checks = []


def check(value, label):
    assert value, label
    checks.append(label)


terminal = host.DesktopInput()
game = host.DesktopGame(terminal=terminal, renderer_factory=host.CanvasRenderer)
terminal.game = game
game.renderer.game = game
game.renderer.present = lambda lines: None
try:
    game._running = True
    game._start_new_game()
    game._flush_pending_save()
    game._state = 'playing'
    game.renderer._show_talk = False
    game.duck.growth_stage = 'adult'
    game.duck.current_action = None
    for key in ('hunger', 'energy', 'fun', 'cleanliness', 'social'):
        setattr(game.duck.needs, key, 95)
    game.duck_store.sync_from_duck(game.duck)
    pond = game.living_pond
    pond.state['auto'] = False
    pond.state['elapsed'] = 1000
    pond.state['next_story'] = 0
    pond.state['story'] = None
    game.friends.current_visit = None
    pip = VISITORS['lost_duckling']
    merchant = VISITORS['traveling_merchant']
    arrival = datetime.now().isoformat()
    game.atmosphere.current_visitor = (pip, arrival)
    with patch.dict('engine.living_world.STORIES', {'lost_duckling': STORIES['lost_duckling']}, clear=True):
        pond._stories()
        check(pond.state['story'] is None and game.atmosphere.current_visitor == (pip, arrival),
              'a visiting Pip defers his story without altering his visit')
        game.atmosphere.current_visitor = None
        pond.state['next_story'] = 0
        pond._stories()
    check(pond.state['story']['id'] == 'lost_duckling', 'Pip story can begin after his visit ends')
    story_before = copy.deepcopy(pond.state['story'])
    for step in range(len(STORIES['lost_duckling']['scenes'])):
        pond.state['story']['step'] = step
        game._reconcile_visitor_presence()
        history = copy.deepcopy(game.atmosphere.to_dict())
        with patch.dict('world.atmosphere.VISITORS', {'lost_duckling': pip}, clear=True), \
                patch('world.atmosphere.random.random', return_value=0):
            check(game.atmosphere._check_visitor() is None and game.atmosphere.current_visitor is None,
                  'story step ' + str(step) + ' excludes a duplicate arrival')
        check(game.atmosphere.to_dict() == history, 'excluded arrival has no friendship or history effects')
    pond.state['story'] = story_before
    with patch.dict('world.atmosphere.VISITORS', {'traveling_merchant': merchant}, clear=True), \
            patch('world.atmosphere.random.random', return_value=0):
        game.atmosphere._check_visitor()
    check(game.atmosphere.current_visitor[0].id == 'traveling_merchant', 'other visitors remain eligible during Pip story')
    game._reconcile_visitor_presence()
    check(game.atmosphere.current_visitor[0].id == 'traveling_merchant', 'reconciliation preserves another visitor')
    check('excluded_visitors' not in game.atmosphere.to_dict(), 'presence exclusion is transient, not saved friendship state')

    # An obsolete overlapping source cannot hand a live mechanical lease to the
    # story body. Begin with the real rare visitor, then introduce that conflict.
    pond.state['story'] = None
    game._reconcile_visitor_presence()
    check('lost_duckling' not in game.atmosphere.excluded_visitors, 'ending the story releases its arrival reservation')
    game.renderer._viewport_width = 132
    game.renderer._viewport_height = 42
    game.renderer._update_camera(132, 42)
    game.habitat.owned_items = ['bounce_house']
    game.habitat.placed_items = [PlacedItem('bounce_house', 9, 6)]
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
    game.atmosphere.current_weather = Weather(WeatherType.SUNNY, .5, 1, arrival)
    game.atmosphere.current_visitor = (pip, arrival)
    game.guest_motion.tick(game, 0)
    game.guest_motion.actor.update(x=64., y=24.)
    game.guest_motion.target = (64., 24.)
    pond.sync()
    pond.weather_type, pond.season, pond.hour = 'sunny', 'spring', 12
    pond.state['ecology'].update(wind=.2, temperature=18)
    pond.state['cooldowns'] = {}
    pond.minds.sync()
    pond.minds.model.residents['lost_duckling']['energy'] = .95
    pond.minds.tasks['lost_duckling'] = dict(action='observe', until=1e9)
    iid = next(p.instance for p in pond.placements if p.item_id == 'bounce_house')
    obj = pond.object_state('bounce_house', iid)
    obj.update(last_use=-1000, uses=0, castle={}, excursion={})
    excursions.state('bounce_house', obj)
    castle_work.state(obj).update(motor='on', latch=1)
    ok, reason = carnival.request(pond, 'bounce_house', 'castle_door_open', iid, together=True)
    check(ok, 'real rare Pip starts shared work: ' + reason)
    work = pond.state['plan']['carnival_work']
    clock = 0.
    for _ in range(2000):
        if work['events']:
            break
        clock += .2
        pond.state['elapsed'] += .2
        castle_shared.refresh(pond)
        pos._state_start_time -= .2
        pos.update(.2)
        game.guest_motion.tick(game, clock)
        pond._activity(.2)
    check(work['events'] == [0], 'rare Pip consumes only the real first latch event')
    pond.state['story'] = copy.deepcopy(story_before)
    story_object = pond.state['story']
    history = copy.deepcopy(game.atmosphere.to_dict())
    brains = copy.deepcopy(pond.minds.model.state)
    needs = copy.deepcopy(game.duck.needs.__dict__)
    game._reconcile_visitor_presence()
    check(game.atmosphere.current_visitor is None and work.get('interrupted') and not pond.minds.carnival_guests,
          'existing story owns one body and interrupts the duplicate rare lease')
    check('lost_duckling' not in pond.minds.present and 'lost_duckling' not in pond.minds.presence_tokens,
          'other company routines immediately see the duplicate visitor as absent')
    check(game.guest_motion.target == (game.guest_motion.actor['x'], game.guest_motion.actor['y']),
          'duplicate cleanup releases the old owned destination before its mover runs')
    check(work['events'] == [0] and obj['castle']['latch'] == 0 and obj['uses'] == 0,
          'consumed latch persists without a completion reward or role handoff')
    for _ in range(3):
        game._reconcile_visitor_presence()
    check(pond.state['story'] is story_object and story_object == story_before and
          game.atmosphere.to_dict() == history and pond.minds.model.state == brains and game.duck.needs.__dict__ == needs,
          'idempotent reconciliation preserves story, memories, friendships, history and needs')
    game.guest_motion.tick(game, clock + .2)
    game.story_motion.tick(game, clock + .2)
    pond._activity(.2)
    scene = snapshot(game, game.renderer)
    check(scene['rareVisitor'] is None and scene['storyActor']['id'] == 'story:lost_duckling',
          'the published world contains exactly one Pip body')
    game._save_game()
    game._flush_pending_save()
    game._load_game()
    check(game.living_pond.state['story'] == story_before and 'lost_duckling' in game.atmosphere.excluded_visitors,
          'loading a saved story rebuilds its transient presence reservation')
    print(json.dumps(dict(result='PASS', checks=len(checks), scope='single-Pip-presence')))
finally:
    if game.living_pond:
        game.living_pond.minds.close()
    game._save_executor.shutdown(wait=True)
    if getattr(game, '_talk_executor', None):
        game._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
