"""Independent rare/story shared-control lifecycle checks with disposable state.

The real DesktopGame update dispatch, GuestMotion/StoryMotion and camera transform run;
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
from datetime import datetime, timedelta
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ['CHEESE_SAVE_DIR'] = tempfile.mkdtemp(prefix='cheese-special-lifecycle-')
os.environ['SDL_AUDIODRIVER'] = 'dummy'
os.environ['SDL_VIDEODRIVER'] = 'dummy'

from engine import host, carnival, castle_work, castle_shared, castle_actors, guest_motion, visitor_shelters, excursions
from engine.scene import snapshot
from engine.living_world import LivingPond, PLANS
from world.atmosphere import Weather, WeatherType, Season, VISITORS
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


def cheese_root():
    return [game.renderer.duck_pos.x, game.renderer.duck_pos.y]


def fixture(kind='traveling_merchant', remaining=None, age='hatchling'):
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
    game.habitat.placed_items = [PlacedItem('bounce_house', 9, 6)]
    game.habitat.stored_items = []
    game.habitat.stored_placements = []
    game.building.structures = []
    for room in game.decorations.rooms.values():
        room.decorations = []
    pos = game.renderer.duck_pos
    pos.cancel_movement()
    pos.x, pos.y = 44, 26
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
    if kind == 'story:pip':
        pond.state['story'] = {'id': 'lost_duckling', 'step': 0, 'choices': []}
        mover = game.story_motion
        mover.token = mover.actor = None
        mover.tick(game, clock)
        key = kind
    else:
        visitor = copy.deepcopy(VISITORS[kind])
        age_seconds = 0 if remaining is None else visitor.stay_duration_hours*3600-remaining
        arrival = (SimDatetime.now()-timedelta(seconds=age_seconds)).isoformat()
        game.atmosphere.current_visitor = (visitor, arrival)
        mover = game.guest_motion
        mover.token = mover.actor = None
        mover.tick(game, clock)
        key = kind
    mover.actor.update(x=64., y=24., facing=True)
    mover.target = (64., 24.)
    mover.last = clock
    mover.rest_until = clock+100
    mover._shared_motion_owner = mover._shared_motion_target = None
    pond.minds.sync()
    pond.minds.model.residents[key]['energy'] = .95
    pond.minds.tasks[key] = dict(action='observe', until=pond.minds.now+1000,
                                context=pond.minds.context(key))
    return pond, iid, obj, key, mover


class SimDatetime(datetime):
    @classmethod
    def now(cls, tz=None):
        return cls.fromtimestamp(clock, tz)


@contextmanager
def controlled_clocks():
    with patch('datetime.datetime', SimDatetime), \
            patch.object(guest_motion, 'datetime', SimDatetime), \
            patch.object(castle_actors, 'datetime', SimDatetime, create=True), \
            patch.object(visitor_shelters, 'datetime', SimDatetime), \
            patch('engine.guest_motion.time.monotonic', lambda: clock):
        yield


def root(mover):
    return [mover.actor['x'], mover.actor['y']]


def request(kind='traveling_merchant', score='castle_door_open'):
    pond, iid, obj, key, mover = fixture(kind)
    ok, message = carnival.request(pond, 'bounce_house', score, iid, together=True)
    check(ok, kind + ' explicit shared request: ' + message)
    plan = pond.state['plan']
    return pond, plan, plan['carnival_work'], obj, key, mover


def step(dt=.2, after_pond=None):
    global clock
    clock += dt
    pond = game.living_pond

    def base_update(_game):
        pos = game.renderer.duck_pos
        pos._state_start_time -= dt
        pos.update(dt)

    def pond_tick():
        pond.state['elapsed'] += dt
        pond._activity(dt)
        if pond.state['plan']:
            obj = pond.object_state('bounce_house', pond.state['plan'])
            excursions.update('bounce_house', obj, dt, True, pond.weather_type, .2, 12,
                              reserved=carnival.owns(pond, 'bounce_house', obj))
        if after_pond:
            after_pond()

    def minds_tick():
        pond.minds.sync()
        carnival.tick(pond.minds, dt)

    with patch.object(host.Game, '_update', base_update), \
            patch.object(pond, 'tick', pond_tick), patch.object(pond.minds, 'tick', minds_tick):
        game._update()  # Both real special movers run in their production order.


def until(predicate, label):
    for _ in range(1500):
        if predicate():return
        step()
    raise AssertionError(label + ': ' + repr(game.living_pond.state.get('plan')))


def rewards(pond, obj, key):
    return copy.deepcopy(dict(uses=obj['uses'], routines=obj['carnival_routines'],
                              company=obj['carnival_company'], skills=pond.state['skills'],
                              needs={k:getattr(game.duck.needs,k) for k in ('hunger','energy','fun','cleanliness','social')},
                              brains={k:pond.minds.model.residents[k] for k in ('cheese',key)}))


try:
    game._running = True
    game._start_new_game()
    game._flush_pending_save()
    game._state = 'playing'
    sound_engine.enabled = False
    with controlled_clocks():
        for kind in ('traveling_merchant','celebrity_duck','lost_duckling'):
            for remaining in (5.9,12.):
                pond,iid,obj,key,mover = fixture(kind,remaining)
                before = copy.deepcopy((obj,pond.minds.tasks,pond.minds.model.state,root(mover),mover.target))
                ok,_ = carnival.request(pond,'bounce_house','castle_door_open',iid,together=True)
                check(not ok and pond.state['plan'] is None and not pond.minds.carnival_guests,
                      kind + ': insufficient remaining visit time refuses before acquisition')
                check((obj,pond.minds.tasks,pond.minds.model.state,root(mover),mover.target) == before,
                      kind + ': departure-budget refusal changes no materials, brains, tasks or movement')

            pond,iid,obj,key,mover = fixture(kind)
            proposal,reason = castle_shared.propose(pond,'castle_door_open',iid)
            assert proposal,reason
            needed = proposal['required_seconds']
            check(needed > castle_work.ROUTINES['castle_door_open']['duration']+12,
                  kind + ': budget includes actual sequential routes beyond score and departure margin')
            pond,iid,obj,key,mover = fixture(kind,needed-.5)
            ok,_ = carnival.request(pond,'bounce_house','castle_door_open',iid,together=True)
            check(not ok and pond.state['plan'] is None and obj['castle']['latch'] == 1,
                  kind + ': a visit shorter than the full itinerary cannot consume its first contact')

        for kind in ('traveling_merchant','celebrity_duck','lost_duckling','story:pip'):
            pond,plan,work,obj,key,mover = request(kind)
            initial_story = copy.deepcopy(pond.state['story'])
            until(lambda: bool(work['events']), kind + ' reaches a real contact')
            frame = snapshot(game,game.renderer)
            physical = frame['living']['plan']['carnival_work']['physical']
            source = frame['storyActor'] if kind == 'story:pip' else frame['rareVisitor']
            check(physical['contact_ready'] is True and close_points(physical['root'],root(mover)) and
                  close_points([source['x'],source['y']],root(mover)),
                  kind + ': full host update leaves truthful ready contact and one actual source root')
            check(pond.state['story'] == initial_story,
                  kind + ': material contact does not advance a story choice')
            roots = cheese_root(),root(mover)
            progress = work['clock'],list(work['events'])
            plan['paused'] = True
            game.duck.current_action = 'feed'
            game.renderer.duck_pos.set_state_by_name('eating',0)
            game.renderer._viewport_width,game.renderer._viewport_height = 70,25
            game.renderer._update_camera(70,25)
            for _ in range(4):step()
            check(close_points(cheese_root(),roots[0]) and close_points(root(mover),roots[1]) and
                  (work['clock'],work['events']) == progress and game.renderer.duck_pos.get_state() == 'eating',
                  kind + ': actual host pause/care/camera update holds both native roots and clock')
            check(snapshot(game,game.renderer)['living']['plan']['carnival_work']['physical']['contact_ready'] is False,
                  kind + ': paused end-of-host snapshot cannot claim a ready material contact')
            before = rewards(pond,obj,key)
            if kind == 'story:pip':
                expected = copy.deepcopy(pond.state['story'])
                expected['step'] += 1
                expected['choices'].append('external-choice')
                def change_step():
                    pond.state['story']['step'] += 1
                    pond.state['story']['choices'].append('external-choice')
                step(after_pond=change_step)
                check(work.get('interrupted') and not pond.minds.carnival_guests and
                      close_points(root(mover),roots[1]) and pond.state['story'] == expected,
                      'story change after pond activity releases before the actual StoryMotion update')
                step()
                check(pond.state['plan'] is None and pond.state['story'] == expected,
                      'the next activity tick consumes the interrupted story plan without another choice')
            else:
                visitor,arrival = game.atmosphere.current_visitor
                clock = SimDatetime.fromisoformat(arrival).timestamp()+visitor.stay_duration_hours*3600-5.9
                step()
                check(pond.state['plan'] is None and mover.actor['state'] == 'leaving' and
                      game.atmosphere.current_visitor[1] == arrival,
                      kind + ': final six seconds interrupt even a paused hold without extending the visit')
            check(work.get('interrupted') and work['events'] == [0] and obj['castle']['latch'] == 0 and
                  not pond.minds.carnival_guests and rewards(pond,obj,key) == before,
                  kind + ': interruption retains the applied latch with no shared or generic rewards')

        for kind in ('traveling_merchant','story:pip'):
            pond,plan,work,obj,key,mover = request(kind)
            initial = root(mover)
            until(lambda: not close_points(root(mover),initial),kind + ' starts actual approach')
            before = rewards(pond,obj,key)
            old_owner = mover._shared_motion_owner
            if kind == 'story:pip':
                pond.state['story'] = copy.deepcopy(pond.state['story'])
                expected_story = copy.deepcopy(pond.state['story'])
            else:
                visitor,_ = game.atmosphere.current_visitor
                game.atmosphere.current_visitor = (visitor,(SimDatetime.now()+timedelta(seconds=1)).isoformat())
                expected_story = None
            step()
            check(pond.state['plan'] is None and not pond.minds.carnival_guests and
                  mover._shared_motion_owner != old_owner and not work['events'],
                  kind + ': replacement identity cannot inherit the old approach or contact owner')
            check(rewards(pond,obj,key) == before and pond.state['story'] == expected_story,
                  kind + ': replacement itself adds no story progression or shared rewards')

        for invalidation in ('growth','new_duck_identity','reload'):
            pond,plan,work,obj,key,mover = request('story:pip')
            until(lambda: bool(work['events']),'Pip reaches contact before '+invalidation)
            before = rewards(pond,obj,key)
            story_before = copy.deepcopy(pond.state['story'])
            if invalidation == 'reload':
                restored = LivingPond(json.loads(json.dumps(pond.save())))
                loaded_work = restored.state['plan']['carnival_work']
                game.living_pond = restored
                try:
                    restored.attach(game,offline=False)
                    restored._activity(0)
                    loaded_obj = restored.object_state('bounce_house',plan['instance'])
                    check(restored.state['plan'] is None and loaded_work.get('interrupted') and not restored.minds.carnival_guests,
                          'story reload never resurrects its process-local actor lease')
                    check(loaded_work['events'] == [0] and loaded_obj['castle']['latch'] == 0 and
                          restored.state['story'] == story_before and rewards(restored,loaded_obj,key) == before,
                          'story reload preserves mechanics and choices without completion reward')
                finally:
                    restored.minds.close()
                    game.living_pond = pond
            else:
                plan['paused'] = True
                old_duck = game.duck
                if invalidation == 'growth':game.duck.growth_stage = 'duckling'
                else:game.duck = copy.deepcopy(game.duck)
                step()
                check(pond.state['plan'] is None and work.get('interrupted') and not pond.minds.carnival_guests,
                      invalidation + ': paused story contract cannot cross an age or duck-identity change')
                check(work['events'] == [0] and obj['castle']['latch'] == 0 and pond.state['story'] == story_before and
                      rewards(pond,obj,key) == before,
                      invalidation + ': applied contact remains, without story choice or reward')
                if invalidation == 'new_duck_identity':
                    game.duck = old_duck
                    game._ensure_living_pond()

        for kind in ('traveling_merchant','story:pip'):
            for release_case in ('premature_callback','new_destination','forged_source'):
                pond,plan,work,obj,key,mover = request(kind)
                initial = root(mover)
                until(lambda: not close_points(root(mover),initial),'moving '+kind+' cleanup')
                current = root(mover)
                before = rewards(pond,obj,key)
                if release_case == 'new_destination':
                    mover.target = (current[0]+2,current[1])
                    destination = mover.target
                    pond.cancel()
                    check(mover.target == destination and mover._shared_motion_owner is None,
                          kind + ': release leaves an independently replaced destination intact')
                elif release_case == 'premature_callback':
                    pond._complete(plan)
                    step()
                    check(close_points(root(mover),current) and close_points(mover.target,current) and pond.state['plan'] is None,
                          kind + ': premature callback stops only its old destination before the real mover runs')
                else:
                    mover.actor['storyId' if kind == 'story:pip' else 'castId'] = 'wrong-source'
                    step()
                    check(pond.state['plan'] is None and work.get('interrupted') and not pond.minds.carnival_guests,
                          kind + ': mismatched actual source identity cannot inherit a control pose')
                check(not work['events'] and rewards(pond,obj,key) == before,
                      kind + ' ' + release_case + ': no contact, completion or learning reward')

        pond,iid,obj,key,mover = fixture('story:pip',age='egg')
        initial = cheese_root()
        # The public invitation now has a dedicated stationary egg caregiver.
        # This legacy walking-observer adapter must still reject an egg outright.
        proposal,_ = castle_shared.propose(pond,'castle_door_open',iid)
        check(proposal is None and pond.state['plan'] is None and cheese_root() == initial and obj['castle']['latch'] == 1,
              'an unhatched Cheese cannot enter the walking observer adapter')
        game.duck.growth_stage = 'hatchling'
        check(pond.state['plan'] is None and not pond.minds.carnival_guests,
              'hatching does not revive the refused egg request or acquire a story helper')

        pond,plan,work,obj,key,mover = request('story:pip')
        story_before = copy.deepcopy(pond.state['story'])
        until(lambda: pond.state['plan'] is None,'story operator completes independently of story choices')
        check(work.get('recorded') is True and obj['uses'] == 1 and pond.state['story'] == story_before,
              'completed story operator work records one use without choosing or finishing a story')
        before = rewards(pond,obj,key)
        pond._complete(plan)
        check(rewards(pond,obj,key) == before and pond.state['story'] == story_before,
              'duplicate story completion preserves every reward and story choice')

    print(json.dumps({'result':'PASS','checks':len(checks),'scope':'independent-special-lifecycle'}))
finally:
    if game.living_pond:game.living_pond.minds.close()
    if getattr(game,'_save_executor',None):game._save_executor.shutdown(wait=True)
    if getattr(game,'_talk_executor',None):game._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
