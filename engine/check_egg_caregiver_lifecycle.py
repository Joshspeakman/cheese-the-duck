"""Independent stationary-egg caregiver lifecycle checks using disposable state.

The real DesktopGame update dispatch, VisitorAnimator and camera transform run;
unrelated base-game timers and ambient brain decisions are isolated. This is
adversarial lifecycle coverage of exact regular Marco, not a caregiver matrix.
"""
import copy
import json
import os
import random
import sys
import subprocess
import tempfile
import time
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ['CHEESE_SAVE_DIR'] = tempfile.mkdtemp(prefix='cheese-egg-lifecycle-')
os.environ['SDL_AUDIODRIVER'] = 'dummy'
os.environ['SDL_VIDEODRIVER'] = 'dummy'

from engine import host, carnival, castle_work, castle_shared, egg_caregiver, excursions
from engine.scene import snapshot
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


def fixture(age='egg', cast='friend:marco'):
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
    game.habitat.placed_items = [PlacedItem('bounce_house', 9, 6)]
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
    obj['castle']['motor']='off' if score=='castle_start' else 'on'
    ok, message = carnival.request(pond, 'bounce_house', score, iid, together=True)
    check(ok, 'explicit together request: ' + message)
    plan = pond.state['plan']
    return pond, plan, plan['carnival_work'], obj, key


def step(dt=.2, after_pond=None):
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
        if after_pond:after_pond()
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


def drawing_review(frame):
    source=r'''
import assert from 'node:assert/strict';
import {LivingWorld} from './engine/client/ultra-world.mjs';
import {carnivalOccupants} from './engine/client/carnival-routines.mjs';
import {characterSprite} from './engine/client/ultra-characters.mjs';
import {displayCamera} from './engine/client/actor-projection.mjs';
import {projectCastleWorld} from './engine/client/castle-projection.mjs';
const frame=JSON.parse(process.argv[1]),work=frame.living.plan.carnival_work;
const occupants=carnivalOccupants(frame);
assert.equal(occupants.length,1);assert.equal(occupants[0].actor,work.shared.operator.actor);
assert(!occupants.some(r=>r.actor==='cheese'));
let count=0;
for(const motion of [true,false])for(const [width,height]of [[1200,800],[1800,800],[900,1100]])for(const time of [0,.13,1.1,5.8,19.25]){
 const scene=structuredClone(frame),sx=width/240,sy=height/112;
 scene.motion=motion;scene.duck.motion=motion;scene.camera=displayCamera(scene.camera,sx,sy);
 const world=new LivingWorld();world.duckPosition=[200,10];
 const result=world.render(scene,time,.1),egg=result.characters.find(c=>c.cheese);
 assert(egg,'stationary egg remains in ordinary world characters');
 const baseline=characterSprite({...scene.duck,motion,performance:null},motion?time:0);
 for(const key of ['art','fills','offsetY','scale','facing','phase','rig','grip','bill','performance'])assert.deepEqual(egg[key],baseline[key]);
 assert.equal(egg.performance,null);assert.equal(egg.grip,null);assert.equal(egg.rig,null);
 const root=projectCastleWorld({camera:scene.camera},work.shared.recipient.root,sx,sy);
 assert(Math.abs(egg.x*sx-root.x)<1e-8&&Math.abs(egg.y*sy-root.y)<1e-8);
 count++;
}
console.log(JSON.stringify({count}));
'''
    result=subprocess.run(['node','--input-type=module','-e',source,json.dumps(frame)],cwd=ROOT,text=True,capture_output=True)
    assert result.returncode==0,result.stdout+result.stderr
    check(json.loads(result.stdout)['count']==30,
          'actual host egg retains original art and root at 30 motion/time/camera combinations')


try:
    game._running=True
    game._start_new_game()
    game._flush_pending_save()
    game._state='playing'
    sound_engine.enabled=False

    pond,iid,obj,key=fixture()
    p=game.renderer.duck_pos
    p.frozen=False
    callbacks=[]
    p.move_to(50,30,lambda _:callbacks.append('stale'))
    p.facing_right=False
    original=actual_egg()
    step(3)
    check(actual_egg()==original and p.frozen and not callbacks and p._movement_callback is None,
          'real host freezes an egg before a stale directed target or arrival callback can run')
    check((p.target_x,p.target_y)==tuple(original[:2]) and not p._is_directed_movement,
          'host frozen update removes the stale destination rather than postponing it')
    game.duck.growth_stage='hatchling'
    step(.1)
    check(actual_egg()==original and not callbacks and not p.frozen,
          'hatching cannot resume a discarded egg destination')

    for fault in ('shell_water','reserved','third_actor','inside_castle','head_overlap'):
        pond,iid,obj,key=fixture()
        if fault=='reserved':pond.minds.readers[key]={'owner':'independent-reader'}
        elif fault=='third_actor':pond.state['story']={'id':'lost_duckling','step':0,'choices':[]}
        elif fault=='inside_castle':
            center=castle_work.placement_center(pond,dict(target='bounce_house',instance=iid))
            p.x,p.y=castle_work.art_world(center,20,20)
        elif fault=='head_overlap':
            # Full caregiver head, not merely its old torso or root distance.
            visitor_animator._position_x=p.x-game.renderer._camera_x
            visitor_animator._position_y=p.y+5-game.renderer._camera_y
            visitor_animator._target_x=visitor_animator._position_x
            visitor_animator._target_y=visitor_animator._position_y
            r=egg_caregiver.recipient(pond)
            center=castle_work.placement_center(pond,dict(target='bounce_house',instance=iid))
            check(egg_caregiver.shell_safe(pond,dict(instance=iid),r,center) and
                  not egg_caregiver.separated(guest_root(),'friend:marco',r),
                  'head overlap fixture has a safe original shell but intersecting full caregiver ink')
        before=ownership(pond,obj)
        if fault=='shell_water':
            r=egg_caregiver.recipient(pond);base=egg_caregiver.box(r['root'],egg_caregiver.metric(r),'shell_base')
            real=egg_caregiver.terrain.water_at
            def water(location,x,y,biome=None):
                return base[0]<=x<=base[0]+base[2] and base[1]<=y<=base[1]+base[3] or real(location,x,y,biome)
            with patch('engine.terrain.water_at',water):
                ok,_=carnival.request(pond,'bounce_house','castle_door_open',iid,together=True)
        else:ok,_=carnival.request(pond,'bounce_house','castle_door_open',iid,together=True)
        check(not ok,fault+': rejects caregiver preflight')
        check(ownership(pond,obj)==before,fault+': does not relocate egg or change materials/tasks/leases/targets')

    pond,plan,work,obj,key=request()
    original=actual_egg();credit=egg_credit(pond)
    until(lambda:bool(work['events']),'first caregiver contact')
    check(work['events']==[0] and obj['castle']['latch']==0 and actual_egg()==original,
          'independently arrived caregiver unlatches while egg root and facing stay exact')
    frame=snapshot(game,game.renderer)
    rendered=frame['living']['plan']['carnival_work']
    check(rendered['physical']['contact_ready'] and close_points(rendered['physical']['root'],guest_root()) and
          rendered['physical']['actor']==key and rendered['shared']['recipient']['root']==original[:2],
          'end-of-host snapshot publishes actual caregiver contact and stationary egg identity')
    drawing_review(frame)
    check(carnival.conversation(pond,plan,'cheese') is None and carnival.conversation(pond,plan,'not-present') is None,
          'egg and unrelated actor receive no invented caregiver conversation')
    chat=carnival.conversation(pond,plan,key)
    check(chat and chat['company_status']=='stationary recipient',
          'caregiver conversation truthfully describes a stationary recipient: '+repr((chat,carnival.valid(pond,plan),egg_caregiver.validate(pond,plan),plan['destination'],work['shared']['center'])))
    check(not pond.minds.ask('cheese','Hello')[0],
          'ordinary egg conversation gate remains intact')
    pond.sync()
    pond.minds.model.state['next_social']=1e30
    pond.minds.next_tick=-1;pond.minds.last_at=pond.minds.now
    before_brain=copy.deepcopy(pond.minds.model.residents[key]['counts'])
    pond.minds.tick()
    activity=pond.state['friends'][key]['activity']
    check('egg' in activity.lower() and 'boarding' not in activity.lower(),
          'real brain tick publishes caregiver status from the held control role: '+activity)
    check(pond.minds.model.residents[key]['counts']==before_brain and egg_credit(pond)==credit,
          'ordinary reserved brain tick awards no caregiver or egg experience before completion')

    hold=guest_root();elapsed=work['ride_elapsed'];events=list(work['events'])
    plan['paused']=True
    game.duck.current_action='feed'
    p.set_state_by_name('eating',0)
    for width,height in ((80,34),(160,50),(132,42)):
        game.renderer._viewport_width,game.renderer._viewport_height=width,height
        game.renderer._update_camera(width,height)
        step(2)
        check(actual_egg()==original and close_points(guest_root(),hold) and work['ride_elapsed']==elapsed and work['events']==events,
              'pause/direct care/camera change holds independent roots and control clock')
        check(p.get_state()=='eating','caregiver pause preserves direct-care art without changing shell position')
    check(egg_credit(pond)==credit,'contacts and paused company award no egg learning, needs, skill, memory or preference')
    game.duck.current_action=None
    plan['paused']=False;game._state='menu'
    step(3)
    check(actual_egg()==original and close_points(guest_root(),hold) and work['ride_elapsed']==elapsed and work['events']==events,
          'nonplaying host holds caregiver and stationary egg without accumulating control time')
    game._state='playing'

    pond,plan,work,obj,key=request()
    until(lambda:bool(work['events']),'first contact before explicit cancellation')
    before=rewards(pond,obj,key);original=actual_egg()
    pond.cancel()
    assert_interrupted(pond,work,obj,key,before,[0],'explicit caregiver cancellation')
    check(actual_egg()==original,'cancelling the caregiver neither turns nor relocates the egg')

    for fault in ('growth','identity','root','facing','visit','leaving','malformed_recipient','malformed_lease',
                  'missing_flag','false_flag','string_flag','raw_guest_bool','raw_guest_none','raw_egg_string','wind_none','wind_nan'):
        pond,plan,work,obj,key=request()
        until(lambda:bool(work['events']),'first contact before '+fault)
        before=rewards(pond,obj,key)
        plan['paused']=True
        if fault=='growth':game.duck.growth_stage='hatchling'
        elif fault=='identity':game.duck.created_at='replacement-egg'
        elif fault=='root':p.x+=.01
        elif fault=='facing':p.facing_right=not p.facing_right
        elif fault=='visit':game.friends.current_visit.started_at='replacement-visit'
        elif fault=='leaving':visitor_animator._is_leaving=True
        elif fault=='malformed_recipient':work['shared']['recipient']='broken'
        elif fault=='malformed_lease':pond.minds.carnival_guests[key]='broken'
        elif fault=='missing_flag':work.pop('egg_caregiver')
        elif fault=='false_flag':work['egg_caregiver']=False
        elif fault=='string_flag':work['egg_caregiver']='egg'
        elif fault=='raw_guest_bool':visitor_animator._position_x=True
        elif fault=='raw_guest_none':visitor_animator._position_x=None
        elif fault=='raw_egg_string':p.x=str(p.x)
        elif fault=='wind_none':pond.state['ecology']['wind']=None
        elif fault=='wind_nan':pond.state['ecology']['wind']=float('nan')
        # Corrupt native scalars are rejected before their unrelated base mover
        # can do arithmetic; all valid-scalar cases use the complete host order.
        if fault.startswith('raw_'):
            egg_caregiver.refresh(pond);pond._activity(0)
            p.x=44
            visitor_animator._position_x=72-game.renderer._camera_x
        else:step()
        assert_interrupted(pond,work,obj,key,before,[0],fault)

    pond,plan,work,obj,key=request()
    until(lambda:work['physical']['phase']=='hold','first station before later-foot obstruction')
    assert not work['events']
    s=work['shared'];m=castle_shared.METRICS['friend:marco']['travel'];bx,by=castle_work.pitches(m)
    later=s['sites'][-1]['stance']
    points=[[later[0]+f[0]*bx,later[1]+f[1]*by] for f in m['feet']]
    current=s['sites'][0]['stance']
    now_points=[[current[0]+f[0]*bx,current[1]+f[1]*by] for f in m['feet']]
    puddle=next(q for q in points if all(not close_points(q,t) for t in now_points))
    real=egg_caregiver.terrain.water_at
    def later_water(location,x,y,biome=None):
        return abs(x-puddle[0])<.04 and abs(y-puddle[1])<.04 or real(location,x,y,biome)
    before=rewards(pond,obj,key)
    with patch('engine.terrain.water_at',later_water):
        check(castle_shared.support(pond,plan,current,m,s['center']) and
              not castle_shared.support(pond,plan,later,m,s['center']),
              'later obstruction fixture preserves current stance and removes future real foot support')
        until(lambda:pond.state['plan'] is None,'future station refusal before first irreversible effect')
    assert_interrupted(pond,work,obj,key,before,[],'new later-station puddle')

    for fault in ('premature','replacement_destination','malformed_lease'):
        pond,plan,work,obj,key=request()
        origin=guest_root()
        until(lambda:not close_points(guest_root(),origin),'moving caregiver before callback')
        held=guest_root();before=rewards(pond,obj,key)
        destination=[held[0]+2,held[1]]
        if fault!='premature':
            visitor_animator._target_x=destination[0]-game.renderer._camera_x
            visitor_animator._target_y=destination[1]-game.renderer._camera_y
            game.friends.current_visit.started_at='new-destination-owner'
        if fault=='malformed_lease':pond.minds.carnival_guests[key]='broken'
        pond._complete(plan)
        check(not pond.minds.carnival_guests and rewards(pond,obj,key)==before,
              fault+': direct rejected callback releases ownership without reward')
        step()
        target=[visitor_animator._target_x+game.renderer._camera_x,visitor_animator._target_y+game.renderer._camera_y]
        check(close_points(target,held if fault=='premature' else destination),
              fault+': rejection drops only an owned old caregiver destination')
        assert_interrupted(pond,work,obj,key,before,[],fault)

    pond,old_plan,old_work,obj,key=request()
    pond.cancel()
    pond,plan,work,obj,key=request()
    until(lambda:bool(work['events']),'new owner before stale callback')
    before=ownership(pond,obj)
    pond._complete(old_plan)
    check(ownership(pond,obj)==before,'an older rejected callback preserves the new scene plan, active material state and lease')

    pond,plan,work,obj,key=request()
    until(lambda:bool(work['events']),'first contact before caregiver reload')
    before=rewards(pond,obj,key);original=actual_egg()
    restored=LivingPond(json.loads(json.dumps(pond.save())))
    loaded=restored.state['plan']['carnival_work']
    game.living_pond=restored
    try:
        restored.attach(game,offline=False)
        restored._activity(0)
        loaded_obj=restored.object_state('bounce_house',plan['instance'])
        check(restored.state['plan'] is None and loaded.get('interrupted') and not restored.minds.carnival_guests,
              'reload drops transient caregiver reservation rather than reviving it')
        check(loaded['events']==[0] and loaded_obj['castle']['latch']==0 and rewards(restored,loaded_obj,key)==before and actual_egg()==original,
              'reload preserves consumed material state and stationary egg without completion credit')
    finally:
        restored.minds.close();game.living_pond=pond

    for fault in ('growth_after_exit','shell_water_after_exit','caregiver_departure_after_exit'):
        pond,plan,work,obj,key=request('castle_hose_stow')
        callback=pond._complete
        with patch.object(pond,'_complete') as intercepted:
            until(lambda:pond.state['plan'] is None,'actual caregiver exit before '+fault)
            check(intercepted.call_count==1 and work['shared']['phase']=='done' and not work.get('recorded'),
                  fault+': fixture reaches real exit before the completion callback')
        before=rewards(pond,obj,key);events=list(work['events'])
        if fault=='growth_after_exit':game.duck.growth_stage='hatchling'
        elif fault=='caregiver_departure_after_exit':visitor_animator._is_leaving=True
        if fault=='shell_water_after_exit':
            r=egg_caregiver.recipient(pond);base=egg_caregiver.box(r['root'],egg_caregiver.metric(r),'shell_base')
            real=egg_caregiver.terrain.water_at
            def shell_water(location,x,y,biome=None):
                return base[0]<=x<=base[0]+base[2] and base[1]<=y<=base[1]+base[3] or real(location,x,y,biome)
            with patch('engine.terrain.water_at',shell_water):callback(plan)
        else:callback(plan)
        assert_interrupted(pond,work,obj,key,before,events,fault)

    for score in ('castle_start','castle_door_open','castle_hose_stow'):
        pond,plan,work,obj,key=request(score)
        original=actual_egg();credit=egg_credit(pond)
        learned=copy.deepcopy(pond.minds.model.residents[key]['counts'])
        until(lambda:pond.state['plan'] is None,score+' caregiver completion')
        check(work.get('recorded') and not work.get('interrupted') and work['shared']['phase']=='done' and
              work['physical']['exited'] and close_points(guest_root(),work['shared']['operator_exit']),
              score+': complete only after real caregiver controls and independent exit')
        check(actual_egg()==original and egg_credit(pond)==credit and obj['uses']==0,
              score+': completion gives no generic use or egg action/skill/need/memory/preference credit')
        check(obj['egg_caregiving'][key]==1 and obj['carnival_company'][key]==1 and obj['carnival_routines'][score]==1,
              score+': records one caregiver receipt after completion')
        delta={name:count-learned[name] for name,count in pond.minds.model.residents[key]['counts'].items()}
        check(delta['practice']==1 and delta['share']==1 and all(v==0 for k,v in delta.items() if k not in ('practice','share')),
              'caregiver receives exactly one demonstrated practice and share experience')
        before=rewards(pond,obj,key)
        pond._complete(plan)
        check(rewards(pond,obj,key)==before,'duplicate caregiver completion callback changes no reward')

    pond,plan,work,obj,key=request(age='hatchling')
    until(lambda:bool(work['events']),'normal shared held contact for role-status compatibility')
    pond.sync();pond.minds.model.state['next_social']=1e30
    pond.minds.next_tick=-1;pond.minds.last_at=pond.minds.now
    before=copy.deepcopy({k:pond.minds.model.residents[k]['counts'] for k in ('cheese',key)})
    pond.minds.tick()
    check(pond.state['friends'][key]['activity']==work['label'] and
          {k:pond.minds.model.residents[k]['counts'] for k in ('cheese',key)}==before,
          'ordinary shared operator retains truthful held status and gains no early brain credit')

    pond,plan,work,obj,key=request()
    until(lambda:bool(work['events']),'first contact before fresh DesktopGame disk reload')
    saved_root=actual_egg()
    game._save_game();game._flush_pending_save()
    original_game=game
    fresh_terminal=host.DesktopInput()
    fresh=host.DesktopGame(terminal=fresh_terminal,renderer_factory=host.CanvasRenderer)
    fresh_terminal.game=fresh;fresh.renderer.game=fresh;fresh.renderer.present=lambda lines:None
    fresh_root=[fresh.renderer.duck_pos.x,fresh.renderer.duck_pos.y,fresh.renderer.duck_pos.facing_right]
    try:
        check(fresh.renderer.duck_pos is not p and fresh_root!=saved_root,
              'disk reload fixture creates a different animator with its own initial root')
        fresh._load_game();fresh._state='playing';game=fresh
        loaded=fresh.living_pond
        loaded_work=loaded.state['plan']['carnival_work']
        loaded_obj=loaded.object_state('bounce_house',plan['instance'])
        step(0)
        check(loaded.state['plan'] is None and loaded_work.get('interrupted') and not loaded.minds.carnival_guests,
              'fresh game disk reload discards caregiver ownership and cannot replay its live reservation')
        check(actual_egg()==fresh_root and fresh.renderer.duck_pos.frozen and loaded_work['events']==[0] and
              loaded_obj['castle']['latch']==0 and not loaded_obj['carnival_routines'] and loaded_obj['uses']==0,
              'fresh animator is never snapped to a saved egg root; applied latch persists without credit')
    finally:
        fresh.living_pond.minds.close()
        if getattr(fresh,'_save_executor',None):fresh._save_executor.shutdown(wait=True)
        game=original_game

    print('PASS egg caregiver lifecycle: '+str(len(checks))+' checks')
finally:
    game.living_pond.minds.close()
    if getattr(game,'_save_executor',None):game._save_executor.shutdown(wait=True)
