"""Independent air-supply atomic/procedure lifecycle checks with disposable state.

The real DesktopGame update dispatch, VisitorAnimator and camera transform run;
unrelated base-game timers and ambient brain decisions are isolated. This is
adversarial lifecycle coverage, separate from the full actor/context matrix.
"""
import copy
import json
import os
import random
import sys
import subprocess
import math
import tempfile
import time
from datetime import datetime, timedelta
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ['CHEESE_SAVE_DIR'] = tempfile.mkdtemp(prefix='cheese-air-lifecycle-')
os.environ['SDL_AUDIODRIVER'] = 'dummy'
os.environ['SDL_VIDEODRIVER'] = 'dummy'

from engine import host, carnival, castle_work, castle_shared, castle_flight, castle_actors, guest_motion, visitor_shelters, egg_caregiver, excursions
from engine.scene import snapshot
from engine.living_world import LivingPond, PLANS
from world.atmosphere import Weather, WeatherType, Season, VISITORS
from world.friends import visitor_animator, DuckPersonalityType, FriendshipLevel
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


def base_fixture(age='egg', cast='friend:marco',long_visit=False):
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
    game.habitat.equipped_cosmetics = {}
    game.habitat.placed_items = [PlacedItem('bounce_house', 9, 5)]
    game.habitat.stored_items = []
    game.habitat.stored_placements = []
    game.building.structures = []
    for room in game.decorations.rooms.values():
        room.decorations = []
    pos = game.renderer.duck_pos
    pos.cancel_movement()
    pos.x, pos.y = 44, 26
    pos.facing_right = False
    pos.frozen = age == 'egg'
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
    if long_visit:
        friend.friendship_level=FriendshipLevel.BEST_FRIEND
        friend.friendship_points=600
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


def step(dt=.2, after_pond=None):
    global clock
    pond = game.living_pond
    clock += dt

    def base_update(_game):
        pos = game.renderer.duck_pos
        pos._state_start_time -= dt
        pos.update(dt)
        if game.friends.current_visit:visitor_animator.update(clock, pos.x-game.renderer._camera_x, pos.y-game.renderer._camera_y)

    def pond_tick():
        pond.state['elapsed'] += dt
        # LivingPond.advance integrates the environment before activity. An
        # effect consumed below therefore changes the next physical interval.
        if pond.state['plan']:
            obj = pond.object_state('bounce_house', pond.state['plan'])
            excursions.update('bounce_house', obj, dt, True, pond.weather_type, .2, 12,
                              reserved=carnival.owns(pond, 'bounce_house', obj))
        pond._activity(dt)
        if after_pond:after_pond()

    def minds_tick():
        pond.minds.sync()
        carnival.tick(pond.minds, dt)

    with patch.object(host.Game, '_update', base_update), \
            patch.object(pond, 'tick', pond_tick), \
            patch.object(pond.minds, 'tick', minds_tick):
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
                              guest_target=[visitor_animator._target_x, visitor_animator._target_y],
                              rare={k:getattr(game.guest_motion,k,None) for k in ('actor','token','target','_shared_motion_owner','_shared_motion_target')},
                              story={k:getattr(game.story_motion,k,None) for k in ('actor','token','target','_shared_motion_owner','_shared_motion_target')}))


def rewards(pond, obj, key):
    return copy.deepcopy(dict(uses=obj['uses'], routines=obj['carnival_routines'],
                              company=obj['carnival_company'], skills=pond.state['skills'],
                              needs={k: getattr(game.duck.needs, k) for k in ('hunger', 'energy', 'fun', 'cleanliness', 'social')},
                              brains={k: pond.minds.model.residents[k] for k in ('cheese', key)},
                              egg=egg_credit(pond)))



def egg_credit(pond):
    return copy.deepcopy(dict(brain=pond.minds.model.residents['cheese'],
        skills=pond.state['skills'], preferences=pond.state.get('preferences'),
        habits=pond.state.get('habits'), needs=game.duck.needs.to_dict(),
        memory=game.duck.memory.to_dict(), personality=game.duck.personality,
        growth=game.duck.growth_progress, trust=game.duck.trust))


def actual_egg():
    p=game.renderer.duck_pos
    return [p.x,p.y,p.facing_right]


def assert_interrupted(pond,work,obj,key,before,events,label):
    check(pond.state['plan'] is None and work.get('interrupted') and not pond.minds.carnival_guests,
          label+': releases the stationary recipient and exact caregiver')
    check(work['events']==events and rewards(pond,obj,key)==before,
          label+': keeps consumed mechanics without any recipient or caregiver reward')



class SimDatetime(datetime):
    @classmethod
    def now(cls,tz=None):return cls.fromtimestamp(clock,tz)


@contextmanager
def controlled_clocks():
    with patch('datetime.datetime',SimDatetime),patch.object(guest_motion,'datetime',SimDatetime),\
         patch.object(castle_actors,'datetime',SimDatetime,create=True),\
         patch.object(visitor_shelters,'datetime',SimDatetime),\
         patch('engine.guest_motion.time.monotonic',lambda:clock):yield


def fixture(mode='solo',age='adult',material=None,long_visit=False):
    pond,iid,obj,key=base_fixture(age='egg' if mode=='egg' else age,long_visit=long_visit)
    if mode in ('solo','flight'):
        game.friends.current_visit=None
        visitor_animator._mind_motion={}
    if mode=='flight':
        visitor=copy.deepcopy(VISITORS['butterfly_fairy'])
        game.atmosphere.current_visitor=(visitor,SimDatetime.now().isoformat())
        mover=game.guest_motion;mover.actor=mover.token=None;mover.tick(game,clock)
        mover.actor.update(x=30.,y=30.,facing=True);mover.target=(30.,30.);mover.last=clock;mover.rest_until=clock+100
        mover._shared_motion_owner=mover._shared_motion_target=None
        key='butterfly_fairy'
        pond.minds.sync();pond.minds.model.residents[key]['energy']=.95
        pond.minds.tasks[key]=dict(action='observe',until=pond.minds.now+1000,context=pond.minds.context(key))
    castle=castle_work.state(obj)
    castle.update(motor='on',power_hold=False,hose=0.,kink=0.,vent=0.,dust=.8,powered=True,
                  rotor_speed=1.,pressure=.45)
    if material:castle.update(material)
    castle['targets']={k:castle[k] for k in castle_work.MOVING}
    obj['excursion']['inflation']=.45
    return pond,iid,obj,key


def request(score='castle_pressure_check',mode='solo',**kwargs):
    pond,iid,obj,key=fixture(mode=mode,**kwargs)
    ok,message=carnival.request(pond,'bounce_house',score,iid,together=mode!='solo')
    check(ok,mode+' '+score+' public request: '+message)
    plan=pond.state['plan']
    return pond,plan,plan['carnival_work'],obj,key


def mechanism_object(**state):
    obj=dict(condition=1.,excursion={},castle={})
    excursions.state('bounce_house',obj)
    care=castle_work.state(obj)
    care.update(motor='off',power_hold=False,powered=False,rotor_speed=.8,fan=.3,
                hose=0.,kink=.2,vent=0.,dust=.3,pressure=.65)
    care.update(state);care['targets']={k:care[k] for k in castle_work.MOVING}
    obj['excursion']['inflation']=.65
    return obj


def mechanism_tick(obj,dt):
    excursions.update('bounce_house',obj,dt,True,'sunny',.2,12,reserved='service')


def mechanism_review():
    # Identical actual input histories, differing only in frame partitioning.
    for motor in ('off','on'):
        large=mechanism_object(motor=motor);small=copy.deepcopy(large)
        mechanism_tick(large,6.)
        for _ in range(600):mechanism_tick(small,.01)
        ca,cb=large['castle'],small['castle']
        check('rotor_speed' in ca and 'airflow' in ca and 'pressure' in ca,
              'native mechanism publishes rotor speed, delivered airflow and actual pressure')
        phase_error=abs((ca['fan']-cb['fan']+math.pi)%(2*math.pi)-math.pi)
        check(phase_error<2e-4 and abs(ca['rotor_speed']-cb['rotor_speed'])<2e-4 and
              abs(ca['pressure']-cb['pressure'])<2e-4 and
              abs(large['excursion']['inflation']-small['excursion']['inflation'])<2e-4,
              motor+': rotor phase/speed and pressure are independent of frame partition')
    disconnected=mechanism_object(motor='on',rotor_speed=0.,hose=1.,kink=0.,dust=0.)
    before=disconnected['castle']['pressure'];mechanism_tick(disconnected,4)
    check(disconnected['castle']['powered'] and disconnected['castle']['rotor_speed']>0 and
          disconnected['castle']['airflow']==0 and disconnected['castle']['pressure']<before,
          'powered disconnected blower spins while delivering no invented house pressure')
    clean=mechanism_object(motor='on',rotor_speed=1.,dust=0.,kink=0.)
    dusty=mechanism_object(motor='on',rotor_speed=1.,dust=1.,kink=0.)
    for obj in (clean,dusty):mechanism_tick(obj,20)
    check(clean['castle']['airflow']>dusty['castle']['airflow'] and
          clean['castle']['pressure']>dusty['castle']['pressure'],
          'existing dust obstructs intake and changes actual delivered pressure')

    # A folded silhouette is not a pressure source, including at night/in rain.
    for weather,hour in [('sunny',12),('sunny',23),('rain',23)]:
        stopped=mechanism_object(motor='off',rotor_speed=0.,pressure=0.)
        excursions.update('bounce_house',stopped,100.,True,weather,.2,hour,reserved='service')
        check(stopped['castle']['pressure']==0 and stopped['castle']['airflow']==0 and
              stopped['excursion']['inflation']>=0,
              weather+str(hour)+': resting fabric never becomes false gauge pressure')

    # Long updates must have bounded work, and agree with a partitioned history
    # across the dust clamp and the settled-rotor analytic tail.
    offline=mechanism_object(motor='on',rotor_speed=.1,dust=.999,vent=.3)
    partitioned=copy.deepcopy(offline)
    begin=time.perf_counter();mechanism_tick(offline,86400.)
    elapsed=time.perf_counter()-begin
    for _ in range(24):mechanism_tick(partitioned,3600.)
    check(elapsed<2.,'one offline day integrates with bounded cost rather than dt-sized event loops')
    a,b=offline['castle'],partitioned['castle']
    check(abs(a['pressure']-b['pressure'])<2e-4 and abs(a['rotor_speed']-b['rotor_speed'])<2e-4 and
          abs((a['fan']-b['fan']+math.pi)%(2*math.pi)-math.pi)<2e-4,
          'offline analytic tail preserves pressure and phase across dust saturation')

    for powered in (False,True):
        legacy=dict(condition=1.,castle=dict(motor='on' if powered else 'off',powered=powered),
                    excursion=dict(inflation=.73))
        state=castle_work.state(legacy)
        check(state['pressure']==(.73 if powered else 0.) and state['rotor_speed']==float(powered),
              'legacy '+str(powered)+': migration uses electrical state without inventing stopped pressure')
        state['pressure']=.21;state['rotor_speed']=.34
        castle_work.state(legacy)
        check(state['pressure']==.21 and state['rotor_speed']==.34,
              'repeated normalization preserves explicitly persisted mechanism values')

    for duration in (2.878231366,20.01,75.):
        large=mechanism_object(motor='off' if duration<3 else 'on',rotor_speed=1.,
                               hose=.8,kink=.6,vent=.9,dust=.9999)
        large['castle']['targets'].update(hose=0.,kink=0.,vent=0.)
        small=copy.deepcopy(large);mechanism_tick(large,duration)
        parts=math.ceil(duration/.01)
        for _ in range(parts):mechanism_tick(small,duration/parts)
        a,b=large['castle'],small['castle']
        check(abs(a['pressure']-b['pressure'])<2e-4 and abs(a['airflow']-b['airflow'])<2e-4 and
              abs((a['fan']-b['fan']+math.pi)%(2*math.pi)-math.pi)<2e-4,
              str(duration)+': control easing, coast threshold and dust clamp remain partition stable')


def start_test_game():
    game._running=True
    game._start_new_game()
    game._flush_pending_save()
    game._state='playing'
    sound_engine.enabled=False


AIR_ATOMICS=('castle_start','castle_stop','castle_vent_open','castle_vent_close',
             'castle_hose_straight','castle_hose_stow','castle_grill_clean','castle_gauge_check')


def active_execution(work):
    return work.get('atomic',work)


def operator_root(pond,work):
    shared=work.get('shared',{})
    operator=shared.get('operator',{})
    if operator.get('actor') and operator.get('actor')!='cheese':
        live=castle_actors.live(pond,operator)
        return live['root'] if live else None
    return cheese_root()


def atomic_request(score,mode='solo'):
    materials={
        'castle_start':dict(motor='off',power_hold=True,powered=False,rotor_speed=0.,pressure=0.),
        'castle_vent_close':dict(vent=1.),
        'castle_hose_straight':dict(hose=1.,kink=1.),
    }
    return request(score,mode,material=materials.get(score,{}))


def atomic_completion_review(score,mode='solo'):
    pond,plan,work,obj,key=atomic_request(score,mode)
    check(isinstance(work.get('physical'),dict),mode+' '+score+': public request owns real native physical record')
    before_counts=copy.deepcopy({k:pond.minds.model.residents[k]['counts'] for k in ('cheese',key)})
    egg_before=egg_credit(pond) if mode=='egg' else None
    seen=[];closed_eye_frames=0
    apply=castle_work.apply

    def observed_apply(target,execution,index,effect):
        if target is not obj:return apply(target,execution,index,effect)
        state=copy.deepcopy(castle_work.state(obj))
        physical=work['physical']
        record=dict(id=execution['id'],index=index,clock=execution['clock'],effect=effect,
                    root=copy.deepcopy(physical['root']),actual=operator_root(pond,work),
                    phase=physical['phase'],contact=physical.get('contact_ready'),
                    observation=physical.get('observation_ready'),pressure=state['pressure'],
                    inflation=obj['excursion']['inflation'],motor=state['motor'],
                    powered=state['powered'],rotor=state['rotor_speed'])
        result=apply(target,execution,index,effect)
        record['reading']=copy.deepcopy(execution.get('inspection'))
        seen.append(record)
        return result

    with controlled_clocks(),patch.object(castle_work,'apply',observed_apply):
        for _ in range(2200):
            if pond.state.get('plan') is not plan:break
            step()
            if score=='castle_gauge_check' and pond.state.get('plan') is plan:
                execution=active_execution(work)
                progress=execution.get('ride_elapsed',0)/castle_work.ROUTINES[score]['duration']
                if work['physical']['phase']=='hold' and .16<=progress<=.22:
                    closed_eye_frames+=1
                    assert work['physical'].get('observation_ready') is False,'closed drawn eyes published observation readiness'
            if pond.state.get('plan') is plan and not work.get('recorded'):
                assert not obj['carnival_routines'], 'an atomic effect awarded history before complete exit'
                assert {k:pond.minds.model.residents[k]['counts'] for k in ('cheese',key)}==before_counts, 'an atomic effect awarded early learning'
        else:raise AssertionError('atomic did not finish: '+repr(work))
    check(work.get('recorded') is True and not work.get('interrupted'),
          mode+' '+score+': reaches a valid complete exit: '+str(work.get('physical_error')))
    expected=castle_work.ROUTINES[score]['effects']
    check([r['index'] for r in seen]==list(range(len(expected))),
          mode+' '+score+': each authored effect consumes exactly once')
    check(all(r['phase']=='hold' and close_points(r['root'],r['actual']) and
              abs(r['clock']-expected[r['index']][0]*castle_work.ROUTINES[score]['duration'])<1e-8 for r in seen),
          mode+' '+score+': actual rooted hold and exact authored pose precede every effect')
    if score=='castle_gauge_check':
        check(closed_eye_frames>0,mode+': post-host closed-eye preparation never advertises an actual observation')
        check(all(r['observation'] is True and r['contact'] is False and
                  r['reading']['pressure']==round(r['pressure'],3) for r in seen),
              mode+': gaze reads actual pressure without hand-contact authority')
        operator=key if mode in ('shared','egg') else 'cheese'
        counts=pond.minds.model.residents[operator]['counts']
        check(counts['observe']==before_counts[operator]['observe']+1 and
              counts['practice']==before_counts[operator]['practice'],
              mode+': actual gauge reader learns observation, never mechanical practice')
    if score=='castle_grill_clean':
        check(all(r['motor']=='off' and r['powered'] is False and r['rotor']==0
                  for r in seen if r['effect'][1]=='dust_fraction'),
              mode+': wing cleaning begins only after the actual blower rotor stops')
    if mode=='egg':
        check(egg_credit(pond)==egg_before,'stationary egg receives no action or observation learning')
    before=rewards(pond,obj,key)
    pond._complete(plan)
    check(rewards(pond,obj,key)==before,mode+' '+score+': duplicate outer callback awards nothing')


def atomic_review():
    for score in AIR_ATOMICS:
        if '--no-grille' in sys.argv and score=='castle_grill_clean':continue
        atomic_completion_review(score)
    for mode in ('shared','flight','egg'):
        for score in ('castle_gauge_check','castle_grill_clean'):
            if '--no-grille' in sys.argv and score=='castle_grill_clean':continue
            atomic_completion_review(score,mode)


def pure_procedure_run(score,material=None,hour=12):
    """Exercise the real coordinator/executor before production dispatch lands.

    Only the outer motion harness is local: it walks the actual Cheese animator
    along the proposed routes. This is core coverage, not public role adoption.
    """
    from engine import castle_air as air,castle_air_procedure as procedure
    pond,iid,obj,key=fixture(material=material)
    pond.hour=hour
    plan=dict(kind='item',target='bounce_house',instance=iid,location=pond.location,
              phase='act',automatic=False,destination=castle_work.placement_center(pond,dict(instance=iid)))
    work=plan['carnival_work']=castle_work.make(pond,plan,score)
    operator=dict(actor='cheese',adapter='cheese',source_age='adult',token=str(game.duck.created_at))
    before=ownership(pond,obj)
    contract,reason=procedure.propose(pond,plan,operator,cheese_root())
    check(contract is not None,score+': actual geometry admits whole core itinerary: '+reason)
    check(ownership(pond,obj)==before,score+': whole itinerary proposal leaves roots, materials, brains and tasks unchanged')
    check(procedure.begin(work,contract,procedure.budget(contract,1.)),score+': begins one immutable procedure attempt')
    initial_id=work['id'];initial_rewards=rewards(pond,obj,key)
    result=procedure.next_occurrence(pond,plan,contract)
    applications=[];apply=castle_work.apply

    def observed_apply(target,execution,index,effect):
        applications.append((execution['occurrence_id'],index,effect[1],castle_work.state(target)['pressure']))
        return apply(target,execution,index,effect)

    def walk(path):
        pos=game.renderer.duck_pos
        for target in path:
            pos.move_to(*target)
            for _ in range(1500):
                if close_points(cheese_root(),target):break
                pos._state_start_time-=.2;pos.update(.2)
            else:raise AssertionError('pure coordinator native route failed: '+repr((cheese_root(),target)))
        pos.cancel_movement();pos.set_state_by_name('thinking',0);pos.facing_right=True

    with patch.object(castle_work,'apply',observed_apply):
        for _ in range(2500):
            assert work['id']==initial_id,'child execution replaced the outer procedure ID'
            assert rewards(pond,obj,key)==initial_rewards,'core executor/coordinator awarded intermediate rewards'
            if result['status']=='blocked':raise AssertionError('pure procedure blocked: '+repr(result))
            if result['status']=='transfer':
                walk(result['route'])
                site=result['site'];work['physical']=dict(site,phase='hold',root=cheese_root(),center=contract['center'],contact_ready=False,observation_ready=False)
                check(procedure.arrived(work,contract,result['node']),score+': occurrence starts only after actual route arrival')
            elif result['status']=='exit':
                before_exit=copy.deepcopy(work)
                check(procedure.finish_exit(work,contract,False) is None and work==before_exit,
                      score+': no whole receipt while actual participants still owe exit')
                walk(result['route'])
                check(close_points(cheese_root(),contract['origin']),score+': actual animator returns along reserved exit')
                receipt=procedure.finish_exit(work,contract,True)
                check(receipt is not None,score+': one whole receipt follows all real child effects and return')
                check(procedure.finish_exit(work,contract,True) is None,score+': coordinator receipt is exact-once')
                return pond,plan,work,obj,key,contract,receipt,applications
            context=dict(operator=operator,physical=work['physical'],
                         preflight=lambda:procedure.itinerary_clear(pond,plan,contract))
            excursions.update('bounce_house',obj,.2,True,'sunny',.2,hour,reserved='service')
            result=procedure.advance(pond,plan,contract,context,.2)
        raise AssertionError('pure procedure did not terminate: '+repr(work))


def core_review():
    from engine import castle_air as air,castle_air_procedure as procedure
    check(not air.ray_clear([0.,0.],[1.,0.],[[.09,-1.,.02,2.]]),
          'gauge sightline rejects a thin blocker between former sample points')
    check(not air.ray_clear([0.,0.],[1.,1.],[[.5,.5,.001,.001]]) and
          air.ray_clear([0.,0.],[1.,0.],[[.4,.2,.2,.2]]),
          'gauge sightline uses exact intersection without rejecting a clear nearby object')
    for score,material,hour in (
        ('castle_pressure_check',dict(vent=.8,hose=.6,kink=.8),12),
        ('castle_pressure_check',dict(motor='off',power_hold=True,powered=False,rotor_speed=0.,pressure=.5),12),
        ('castle_dust_service',dict(motor='off',power_hold=True,powered=False,rotor_speed=0.),12),
        ('castle_dust_service',dict(motor='auto',power_hold=False,powered=True,rotor_speed=1.),12),
        ('castle_dust_service',dict(motor='auto',power_hold=False,powered=False,rotor_speed=0.,pressure=0.),23),
    ):
        if '--pressure-core' in sys.argv and score!='castle_pressure_check':continue
        pond,plan,work,obj,key,contract,receipt,applications=pure_procedure_run(score,material,hour)
        p=work['air_procedure']
        expected=['gauge_before','gauge_after'] if score=='castle_pressure_check' else ['gauge_after']
        check([r['occurrence_id'] for r in receipt['observations']]==expected,
              score+': observations retain each occurrence, including repeated same-station reads')
        check(len({(occurrence,index) for occurrence,index,_,_ in applications})==len(applications),
              score+': repeated atomics have independent exact-once event identities')
        for reading in receipt['observations']:
            expected_pressure=next(value for occurrence,_,field,value in applications
                                   if occurrence==reading['occurrence_id'] and field=='inspection')
            check(reading['pressure']==round(expected_pressure,3),score+': receipt keeps the actual pressure at each observed beat')
        check(obj['castle']['power_revision']==contract['initial_power']['power_revision'] and
              obj['castle']['power_hold']==contract['initial_power']['power_hold'] and
              obj['castle']['motor']==contract['initial_power']['motor'],
              score+': internal shutdown/start preserves original user intent and automatic/on policy '+
              repr((hour,{k:obj['castle'][k] for k in ('motor','power_hold','power_revision')},contract['initial_power'])))
        if material.get('power_hold'):
            check(receipt['outcome']=='supply-stopped' and obj['castle']['motor']=='off',
                  score+': initial manual shutdown remains stopped without an invented repair outcome')
        if hour==23:
            check(not contract['initial_power']['restart_allowed'] and any(
                o['atomic_id']=='castle_start' and o['status']=='finished' for o in p['occurrences']) and
                obj['castle']['powered'] is False and obj['castle']['rotor_speed']==0,
                'nighttime automatic policy is restored by a real switch contact without energizing the blower')

        # These invalid records must be rejected even if a caller erroneously
        # presents a late completion callback with an otherwise valid lease.
        for fault in ('observation','mechanical_count','archive_events','status','phase','boolean_version'):
            forged=copy.deepcopy(work);fp=forged['air_procedure']
            if fault=='observation':fp['observations'][0]['pressure']=.123456789
            elif fault=='mechanical_count':fp['mechanical_contacts']+=50
            elif fault=='archive_events':next(o for o in fp['occurrences'] if o['status']=='finished')['execution']['events']=[]
            elif fault=='status':fp['occurrences'][-1]['status']='pending'
            elif fault=='phase':fp['phase']='invented'
            else:fp['version']=True
            check(not procedure.validate(forged,contract),score+': malformed '+fault+' cannot satisfy outer lifecycle')
        previous=copy.deepcopy(work)
        result=procedure.next_occurrence(pond,plan,contract)
        check(result['status']=='blocked' and work==previous,
              score+': finished receipt cannot reopen an earlier occurrence or exit')


def gauge_lifecycle_review():
    for mode in ('solo','shared','flight','egg'):
        with controlled_clocks():
            pond,plan,work,obj,key=atomic_request('castle_gauge_check',mode)
            until(lambda:work['physical']['phase']=='hold' and work['clock']>2,
                  mode+' gauge held preparation')
            before=rewards(pond,obj,key);old_clock=work['clock'];old_events=list(work['events'])
            actual=copy.deepcopy(operator_root(pond,work));recipient=cheese_root()
            plan['paused']=True
            game.duck.current_action='feed';game.renderer.duck_pos.set_state_by_name('eating',0)
            for _ in range(4):step()
            check(work['clock']==old_clock and work['events']==old_events and
                  close_points(operator_root(pond,work),actual) and close_points(cheese_root(),recipient) and
                  work['physical'].get('observation_ready') is False,
                  mode+': pause plus direct care holds actual roots and never consumes a gauge observation')
            check(game.renderer.duck_pos.get_state()=='eating',mode+': gauge pause preserves the independent care pose')
            game.duck.growth_stage='hatchling' if mode=='egg' else 'elder'
            game.duck.current_action=None
            step(0)
            check(work.get('interrupted') and not pond.minds.carnival_guests and
                  work['events']==old_events and rewards(pond,obj,key)==before,
                  mode+': growth while paused interrupts without a reading or reward')

            pond,plan,work,obj,key=atomic_request('castle_gauge_check',mode)
            step(.2)
            before=rewards(pond,obj,key)
            pond._complete(plan)
            check(work.get('interrupted') and not work.get('recorded') and not pond.minds.carnival_guests and
                  rewards(pond,obj,key)==before and not work['events'],
                  mode+': premature gauge callback releases only its attempt and awards no observation')
            step(0)

    # Preserve an actual completed exit while corrupting the reported reading.
    # The callback must reject it even though all route and score data are valid.
    for malformed in (False,float('nan'),None,-.1,1.1):
        pond,plan,work,obj,key=atomic_request('castle_gauge_check')
        callback=pond._complete
        with patch.object(pond,'_complete',lambda _plan:None):
            until(lambda:pond.state.get('plan') is None,'actual gauge exit before malformed reading callback')
        before=rewards(pond,obj,key)
        work['inspection']['pressure']=malformed
        callback(plan)
        check(not work.get('recorded') and rewards(pond,obj,key)==before,
              repr(malformed)+': malformed gauge reading cannot create observation credit after real exit')


def response_callback_review():
    for mode,changed_back in (('solo',False),('solo',True),('shared',False),('flight',False),('egg',False)):
        with controlled_clocks():
            pond,plan,work,obj,key=atomic_request('castle_stop',mode)
            callback=pond._complete
            before=[]
            def changed_input_callback(consumed_plan):
                before.append(rewards(pond,obj,key))
                # The callback stays synchronous with production host order;
                # no artificial orphan lease is left for the next guest mover.
                external=dict(id='castle_start',events=[],automatic=False)
                castle_work.apply(obj,external,0,(0.,'motor','on'))
                if changed_back:
                    external=dict(id='castle_stop',events=[],automatic=False)
                    castle_work.apply(obj,external,0,(0.,'motor','off'))
                callback(consumed_plan)
            with patch.object(pond,'_complete',changed_input_callback):
                until(lambda:pond.state.get('plan') is None,mode+' actual stop exit before changed input')
            check(before and not work.get('recorded') and rewards(pond,obj,key)==before[0] and
                  not pond.minds.carnival_guests,
                  mode+': delayed stop callback rejects '+('a newer intent even with matching final state' if changed_back else 'an actual restarted blower'))

    for mode in ('shared','flight','egg'):
        with controlled_clocks():
            pond,plan,work,obj,key=atomic_request('castle_gauge_check',mode)
            callback=pond._complete;before=[]
            def malformed_read_callback(consumed_plan):
                before.append(rewards(pond,obj,key))
                work['inspection']['pressure']=False
                callback(consumed_plan)
            with patch.object(pond,'_complete',malformed_read_callback):
                until(lambda:pond.state.get('plan') is None,mode+' malformed reading at real callback')
            check(before and not work.get('recorded') and not pond.minds.carnival_guests and
                  rewards(pond,obj,key)==before[0],
                  mode+': rejected gauge receipt releases owned motion before the same host frame advances guests')

    for mode in ('solo','shared','flight','egg'):
        with controlled_clocks():
            pond,old_plan,old_work,obj,key=atomic_request('castle_gauge_check',mode)
            iid=old_plan['instance']
            pond.cancel()
            if mode!='solo':
                # The independent brain has chosen to observe again after the
                # old lease ended; acquisition consumes this new willingness.
                pond.minds.tasks[key]=dict(action='observe',until=pond.minds.now+1000,
                                          context=pond.minds.context(key))
            ok,reason=carnival.request(pond,'bounce_house','castle_stop',iid,together=mode!='solo')
            check(ok,mode+': replacement has its own actual movement/lease: '+reason)
            new_plan=pond.state['plan'];step(0)
            before=ownership(pond,obj)
            old_work['inspection']=dict(kind='pressure',pressure=False)
            pond._complete(old_plan)
            check(pond.state['plan'] is new_plan and ownership(pond,obj)==before,
                  mode+': stale malformed gauge callback preserves the different plan, roots, targets and leases')
            pond.cancel()
            if mode=='solo':
                pos=game.renderer.duck_pos;pos.move_to(38,31)
                before=(pos.x,pos.y,pos.target_x,pos.target_y,pos._is_directed_movement,pos.get_state())
                pond._complete(old_plan)
                check((pos.x,pos.y,pos.target_x,pos.target_y,pos._is_directed_movement,pos.get_state())==before,
                      'stale gauge callback with no plan preserves independent native wandering intent')


def role_preflight_review():
    from engine import castle_air_roles as roles,castle_air_procedure as procedure
    for score in ('castle_pressure_check','castle_dust_service'):
        for mode in ('solo','shared','egg','flight'):
            with controlled_clocks():
                pond,iid,obj,key=fixture(mode,long_visit=mode in ('shared','egg'))
                before=ownership(pond,obj);budgets=[];real_budget=procedure.budget
                def measured_budget(*args,**kwargs):
                    value=real_budget(*args,**kwargs);budgets.append(value);return value
                with patch.object(procedure,'budget',measured_budget):
                    proposal,reason=roles.propose(pond,score,iid,together=mode!='solo')
                check(ownership(pond,obj)==before,mode+' '+score+': whole-role proposal is atomic and changes no ownership or material state')
                if mode=='flight':
                    check(budgets and ((proposal is None and budgets[-1]>180 and 'departure' in reason) or
                          (proposal is not None and proposal['required_seconds']<=180)),
                          score+': real Flutter visit budget admits only a fully budgeted itinerary')
                else:
                    check(proposal is not None,mode+' '+score+': complete role geometry has a valid proposal: '+reason+' '+repr(budgets))
                    check('_journal' not in proposal['procedure'] and 'air_procedure' not in proposal['plan']['carnival_work'] and
                          proposal['required_seconds']==budgets[-1],
                          mode+': pure proposal creates no private execution history or adopted child work')

    for outfit,allowed in (({},True),({'hat':False},True),({'hat':''},True),({'hat':'sun_hat'},False)):
        pond,iid,obj,key=fixture()
        game.habitat.equipped_cosmetics=outfit
        before=ownership(pond,obj)
        proposal,reason=roles.propose(pond,'castle_pressure_check',iid)
        check(bool(proposal)==allowed and ownership(pond,obj)==before,
              repr(outfit)+': outfit clearance rejects only an actually equipped unmeasured garment')

    pond,iid,obj,key=fixture('shared')
    pond.state['story']=dict(id='lost_duckling',step=0)
    before=ownership(pond,obj)
    proposal,reason=roles.propose(pond,'castle_pressure_check',iid,together=True)
    check(proposal is None and 'unreserved' in reason and ownership(pond,obj)==before,
          'unreserved third source refuses the entire procedure before any acquisition')

    pond,iid,obj,key=fixture('shared',long_visit=True)
    visit=game.friends.current_visit
    visit.started_at=(datetime.now()-timedelta(seconds=visit.duration_minutes*60-5)).isoformat()
    before=ownership(pond,obj)
    proposal,reason=roles.propose(pond,'castle_pressure_check',iid,together=True)
    check(proposal is None and 'departure' in reason and ownership(pond,obj)==before,
          'real regular visit with five seconds remaining refuses without extending stay or acquiring targets')

    # A nearby Cheese can finish two actual reads during Flutter's normal visit;
    # that does not authorize adding valve/hose work after the branch was planned.
    with controlled_clocks():
        pond,iid,obj,key=fixture('flight',material=dict(vent=0.,hose=0.,kink=0.,dust=0.))
        game.renderer.duck_pos.x,game.renderer.duck_pos.y=60.,26.
        before=ownership(pond,obj)
        clean,reason=roles.propose(pond,'castle_pressure_check',iid,together=True)
        check(clean is not None and clean['required_seconds']<=180 and ownership(pond,obj)==before,
              'short inspect-only Flutter formation fits the real unchanged visit: '+reason)
        obj['castle'].update(vent=.8,hose=.6,kink=.8)
        obj['castle']['targets'].update(vent=.8,hose=.6,kink=.8)
        before=ownership(pond,obj);budgets=[];real_budget=procedure.budget
        def budget_dirty(*args,**kwargs):
            value=real_budget(*args,**kwargs);budgets.append(value);return value
        with patch.object(procedure,'budget',budget_dirty):dirty,reason=roles.propose(pond,'castle_pressure_check',iid,together=True)
        check(dirty is None and budgets[-1]>clean['required_seconds'] and budgets[-1]>180 and
              ownership(pond,obj)==before,
              'dirty full itinerary cannot borrow the short inspection budget or extend Flutter stay')

    pond,iid,obj,key=fixture(material=dict(vent=0.,hose=0.,kink=0.,dust=0.))
    proposal,reason=roles.propose(pond,'castle_pressure_check',iid)
    check(proposal is not None,'skipped-control regression has an actual feasible itinerary: '+reason)
    plan=proposal['plan'];work=plan['carnival_work'];contract=proposal['procedure']
    check(procedure.begin(work,contract,proposal['required_seconds']) and
          procedure.itinerary_clear(pond,plan,contract),
          'fixed short-visit branch initially has real clear routes and actual gauge sightlines')
    before=copy.deepcopy(work)
    obj['castle']['vent']=obj['castle']['targets']['vent']=.8
    check(not procedure.itinerary_clear(pond,plan,contract) and work==before,
          'changed initially satisfied valve rejects the unbudgeted branch before the first observation/effect')
    obj['castle']['vent']=obj['castle']['targets']['vent']=0.
    with patch('engine.castle_air.sightline',lambda *args,**kwargs:False):
        check(not procedure.itinerary_clear(pond,plan,contract) and work==before,
              'future blocked gauge sightline invalidates the whole itinerary despite unchanged dry routes')


def unbound_procedure_review():
    for score in ('castle_pressure_check','castle_dust_service'):
        for mode in ('solo','shared','flight','egg'):
            pond,iid,obj,key=fixture(mode)
            before=ownership(pond,obj)
            ok,reason=carnival.request(pond,'bounce_house',score,iid,together=mode!='solo')
            check(not ok and ownership(pond,obj)==before,
                  mode+' '+score+': unbound public procedure refuses before any movement or reservation')
            ok,reason=pond.start('item','bounce_house',instance=iid,carnival_choice=score)
            check(not ok and ownership(pond,obj)==before,
                  mode+' '+score+': direct start cannot bypass the missing runtime owner')

        for marker in ('missing',False,'pretend-bound'):
            pond,iid,obj,key=fixture()
            plan=dict(kind='item',target='bounce_house',instance=iid,location=pond.location,
                      phase='act',automatic=False,label=castle_work.ROUTINES[score]['label'],
                      destination=[round(v) for v in castle_work.placement_center(pond,dict(instance=iid))])
            work=plan['carnival_work']=castle_work.make(pond,plan,score)
            work.update(stage='service',clock=0.,ride_elapsed=0.,start=copy.deepcopy(obj['castle']))
            if marker!='missing':work['air_procedure']=marker
            pond.state['plan']=plan
            before=rewards(pond,obj,key);materials=copy.deepcopy(obj['castle']);root=cheese_root()
            check(not carnival.valid(pond,plan),score+': saved/unbound marker '+repr(marker)+' is not a live activity')
            castle_work.advance(pond,plan,300,None)
            check(work.get('interrupted') and not work['events'] and obj['castle']==materials,
                  score+': legacy flattened clock cannot consume unbound mechanical effects')
            pond._complete(plan);pond._activity(0)
            check(rewards(pond,obj,key)==before and not pond.minds.carnival_guests and close_points(cheese_root(),root),
                  score+': unbound legacy cleanup cannot grant a generic reward or move an actor')


if __name__=='__main__':
    try:
        start_test_game()
        mechanism_review()
        selected=set(sys.argv[1:]) or {'--atomics','--core','--boundaries','--callbacks','--roles','--unbound'}
        if '--atomics' in selected:atomic_review()
        if '--core' in selected or '--pressure-core' in selected:core_review()
        if '--boundaries' in selected:gauge_lifecycle_review()
        if '--callbacks' in selected:response_callback_review()
        if '--roles' in selected:role_preflight_review()
        if '--unbound' in selected:unbound_procedure_review()
        print('PASS castle air lifecycle: '+str(len(checks))+' checks')
    finally:
        game.living_pond.minds.close()
        if getattr(game,'_save_executor',None):game._save_executor.shutdown(wait=True)
