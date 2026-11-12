"""Independent four-species anatomy and shared lifecycle checks with disposable state.

The real DesktopGame update dispatch, GuestMotion/StoryMotion and camera transform run;
unrelated base-game timers and ambient brain decisions are isolated. This is
adversarial lifecycle coverage, not the separate species age/control matrix.
"""
import copy
import json
import os
import random
import sys
import subprocess
import tempfile
import time
from datetime import datetime, timedelta
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ['CHEESE_SAVE_DIR'] = tempfile.mkdtemp(prefix='cheese-species-lifecycle-')
os.environ['SDL_AUDIODRIVER'] = 'dummy'
os.environ['SDL_VIDEODRIVER'] = 'dummy'

from engine import host, carnival, castle_work, castle_shared, castle_actors, guest_motion, visitor_shelters, excursions
from engine.scene import snapshot
from engine.living_world import LivingPond
from world.atmosphere import Weather, WeatherType, Season, VISITORS
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


def fixture(kind='friendly_goose', remaining=None, age='hatchling', site=(9,6)):
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
    game.habitat.placed_items = [PlacedItem('bounce_house', *site)]
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


def request(kind='friendly_goose', score='castle_door_open'):
    pond, iid, obj, key, mover = fixture(kind)
    obj['castle']['motor'] = 'off' if score == 'castle_start' else 'on'
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


SPECIES = ('friendly_goose','wise_owl','mysterious_crow','grumpy_toad')


def anatomy_review():
    # Inspect the production drawings independently of the exporter's sampler.
    # Dense real-time sampling covers the actual species phase function, then
    # authored track knots exercise translated heads and compressed/lifted feet.
    source = r'''
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {characterSprite} from './engine/client/ultra-characters.mjs';
import {GUEST_CAST} from './engine/client/guest-cast.mjs';
import {CASTLE_SCORES,castlePose} from './engine/client/castle-care.mjs';
import {performancePose} from './engine/client/performances.mjs';
const data=JSON.parse(fs.readFileSync('engine/client/animation/castle-guest-metrics.json'));
const cases={friendly_goose:{feet:[-4.5,8.5],top:15,dy:[0,0,-1,-1,0,0,-1,-1]},wise_owl:{feet:[-7.5,2.5],top:12,dy:[0,0,-1,-1,0,0,-1,-1]},mysterious_crow:{feet:[-6.5,2.5],top:17,dy:[0,-1,-3,-2,0,0,-2,-1]},grumpy_toad:{feet:[-12.5,-9.5,6.5,9.5],top:21,dy:[0,1,-2,-3,-1,0,0,0]}};
const result=[];
for(const [id,spec]of Object.entries(cases)){
 const profile=GUEST_CAST[id],entry=data.casts[id],union=entry.travel,duck={id,castId:id,state:'idle',facing:true};
 let walkSamples=0,contacts=0,bodySamples=0;const phases=new Set();
 const audit=(c,facing,inside=true)=>{
  assert.equal(c.scale,profile.height/((40-spec.top)*7.5),id+' keeps authored species scale');
  assert.equal(c.groundRow,39.5,id+' keeps native ground');
  assert.equal(c.rig.feet.length,spec.feet.length,id+' actual pad count');
  for(const f of c.rig.feet){
   const x=facing?f.x:c.width-1-f.x,offset=[x+.5-c.anchorX,f.y+.5-c.groundRow];
   assert.equal(c.art[f.y]?.[x],'_',id+' annotated pad must still be drawn ink');
   if(inside)assert(union.feet.some(p=>p[0]===offset[0]&&p[1]===offset[1]),id+' actual pad missing from travel/hold union');
  }
  if(inside)for(const f of c.fills.filter(f=>['b','g'].includes(f.tone))){
   assert(f.x-c.anchorX>=union.body.x-1e-9&&f.x+f.w-c.anchorX<=union.body.x+union.body.w+1e-9&&f.y-c.groundRow>=union.body.y-1e-9&&f.y+1-c.groundRow<=union.body.y+union.body.h+1e-9,id+' drawn head/torso escapes conservative envelope');
  }
  bodySamples++;
 };
 for(const facing of [true,false])for(let j=0;j<128;j++){
  const c=characterSprite({...duck,facing,state:'walking'},j/16/profile.pace,true);audit(c,facing);phases.add(c.phase);walkSamples++;
  for(const f of c.rig.feet){const lift=((c.phase<4)===(f.foot===0))?1:0;assert.equal(f.y,39+spec.dy[c.phase]-lift,id+' preserves actual hop/stride foot row');}
 }
 assert.deepEqual([...phases].sort(),[0,1,2,3,4,5,6,7],id+' samples every actual species phase');
 for(const score of ['castle_start','castle_door_open','castle_hose_stow']){
  const s=CASTLE_SCORES[score];
  const sample=(at,facing,motion)=>{
   const clock=at*s.duration,base={id:score,stage:'service',clock,ride_elapsed:clock},station=castlePose(base).station;
   const routine={...base,shared_physical:true,physical_pilot:false,shared:{version:1,attempt:'independent-anatomy',operator:{actor:id,cast:id,adapter:'rare',token:'visit',motion_token:'motion',location:'Home Pond'},source_age:'hatchling',phase:'operate',cheese:{root:[0,0],stance:[0,0],exit:[0,0],phase:'hold',ready:true}},physical:{version:1,actor:id,phase:'hold',station,root:[0,0],target:[0,0],contact_ready:true}};
   return characterSprite({...duck,facing,performance:{kind:'carnival',routine,role:'a',motion}},0,true);
  };
  for(const [index,[at]]of s.effects.entries())for(const motion of [true,false]){
   const c=sample(at,true,motion),metric=entry.routines[score][index];audit(c,true);
   assert.deepEqual(c.rig.feet.map(f=>[f.x+.5-c.anchorX,f.y+.5-c.groundRow]),spec.feet.map(x=>[x,0]),id+' each actual contact is grounded');
   assert.deepEqual(metric.feet,spec.feet.map(x=>[x,0]));
   assert.deepEqual(metric.grip,[c.grip.x+.5-c.anchorX,c.grip.y+.5-c.groundRow]);
   assert.equal(c.art[c.grip.y]?.[c.grip.x],')',id+' authored working grip is drawn');contacts++;
  }
  for(const [at]of s.track)for(const facing of [true,false])for(const motion of [true,false])audit(sample(at,facing,motion),facing);
 }
 for(const progress of [.2,.35,.45])for(const facing of [true,false]){
  const performance={kind:'puddle_splash',role:'a',progress},pose=performancePose(performance),c=characterSprite({...duck,facing,performance},0,true);audit(c,facing,false);
  for(const f of c.rig.feet)assert.equal(f.y,Math.round(39-(f.foot?pose.r:pose.l)-Math.max(0,pose.b)+pose.b),id+' annotation follows wrapped positive/negative body translation');
 }
 result.push({id,walkSamples,contacts,bodySamples});
}
assert.equal(data.casts.butterfly_fairy,undefined,'Flutter is not an operator fallback');
console.log(JSON.stringify(result));
'''
    result = subprocess.run(['node','--input-type=module'], input=source, text=True,
                            cwd=ROOT, capture_output=True)
    assert result.returncode == 0, result.stderr
    rows = json.loads(result.stdout)
    for row in rows:
        check(row['walkSamples'] == 256 and row['contacts'] == 18,
              row['id']+': independent actual-ink, true-phase, transformed-body and grounded-contact audit')


try:
    game._running = True
    game._start_new_game()
    game._flush_pending_save()
    game._state = 'playing'
    sound_engine.enabled = False
    anatomy_review()
    with controlled_clocks():
        for kind in SPECIES:
            pond,iid,obj,key,mover = fixture(kind,remaining=12)
            before = copy.deepcopy((obj,pond.minds.tasks,pond.minds.model.state,root(mover),mover.target))
            ok,_ = carnival.request(pond,'bounce_house','castle_door_open',iid,together=True)
            check(not ok and pond.state['plan'] is None and not pond.minds.carnival_guests,
                  kind+': insufficient visit budget refuses before shared acquisition')
            check((obj,pond.minds.tasks,pond.minds.model.state,root(mover),mover.target) == before,
                  kind+': budget refusal leaves mechanics, brains and actual movement unchanged')

            pond,plan,work,obj,key,mover = request(kind)
            until(lambda: bool(work['events']),kind+' reaches grounded first contact')
            frame = snapshot(game,game.renderer)
            physical = frame['living']['plan']['carnival_work']['physical']
            metric = castle_shared.operator_metrics(kind,work['id'])[0]
            check(physical['contact_ready'] is True and close_points(physical['root'],root(mover)) and
                  close_points([frame['rareVisitor']['x'],frame['rareVisitor']['y']],root(mover)) and
                  all(f[1] == 0 for f in metric['feet']),
                  kind+': end-of-host ready contact has actual native root and grounded authored feet')
            check(physical['target'] == castle_work.control_world(work['shared']['center'],physical['station']) and
                  castle_work.reach_distance(root(mover),physical['target'],metric['grip'],metric['scale']) <= 3,
                  kind+': unchanged native hardware is reached with this species scale and grip')
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
                  kind+': real host pause, direct care and camera update hold both roots and the service clock')
            check(snapshot(game,game.renderer)['living']['plan']['carnival_work']['physical']['contact_ready'] is False,
                  kind+': paused snapshot grants no active contact')
            before = rewards(pond,obj,key)
            visitor,arrival = game.atmosphere.current_visitor
            if kind == 'friendly_goose':
                clock = SimDatetime.fromisoformat(arrival).timestamp()+visitor.stay_duration_hours*3600-5.9
            elif kind == 'wise_owl':
                game.atmosphere.current_visitor = (visitor,(SimDatetime.now()+timedelta(seconds=1)).isoformat())
            elif kind == 'mysterious_crow':
                mover.actor['castId'] = 'friendly_goose'
            else:
                game.duck.growth_stage = 'duckling'
            step()
            check(pond.state['plan'] is None and work.get('interrupted') and not pond.minds.carnival_guests and
                  mover._shared_motion_owner is None,
                  kind+': paused departure/replacement/forged anatomy/growth invalidates actual ownership')
            check(work['events'] == [0] and obj['castle']['latch'] == 0 and rewards(pond,obj,key) == before,
                  kind+': interruption preserves consumed latch without completion or learning')
            if kind == 'friendly_goose':
                check(mover.actor['state'] == 'leaving' and game.atmosphere.current_visitor[1] == arrival,
                      'Gerald departure is never delayed to finish control work')

        for score in ('castle_door_open','castle_hose_stow'):
            pond,iid,obj,key,mover = fixture('grumpy_toad',site=(9,7))
            obj['castle']['motor'] = 'on'
            before = copy.deepcopy((obj,pond.minds.tasks,pond.minds.model.state,root(mover),mover.target,cheese_root()))
            ok,message = carnival.request(pond,'bounce_house',score,iid,together=True)
            check(not ok and pond.state['plan'] is None and not pond.minds.carnival_guests,
                  'Grumble at (9,7) refuses unreachable later '+score+' station: '+message)
            check((obj,pond.minds.tasks,pond.minds.model.state,root(mover),mover.target,cheese_root()) == before,
                  'Grumble failing site cannot consume reachable buckle or stop the blower before refusal')

        pond,plan,work,obj,key,mover = request('grumpy_toad')
        until(lambda: bool(work['events']),'Grumble releases buckle at supported (9,6) site')
        before = rewards(pond,obj,key)
        metric = castle_shared.METRICS[key]['travel']
        foot = max(metric['feet'],key=lambda f:(f[1],f[0]))
        check(foot[1] == 1 and len({f[0] for f in metric['feet']}) >= 4,
              'Grumble keeps four drawn toe pads and the actual downward stride phase')
        future = work['shared']['sites'][1]['stance']
        bx,by = castle_work.pitches(metric)
        wet = [future[0]+foot[0]*bx,future[1]+foot[1]*by]
        water_at = castle_shared.terrain.water_at
        def flooded_pad(location,x,y,biome=None):
            return abs(x-wet[0]) < .01 and abs(y-wet[1]) < .01 or water_at(location,x,y,biome)
        with patch.object(castle_shared.terrain,'water_at',flooded_pad):
            check(not castle_shared.support(pond,plan,future,metric,work['shared']['center']),
                  'water under the real lowered toe invalidates support even when the root itself stays dry')
            until(lambda: pond.state['plan'] is None,'new water invalidates Grumble remaining route')
        check(work.get('interrupted') and work['events'] == [0] and obj['castle']['latch'] == 0 and
              rewards(pond,obj,key) == before,
              'future hop-foot obstruction interrupts after the consumed buckle without false door work or rewards')

        for kind in ('wise_owl','mysterious_crow'):
            pond,plan,work,obj,key,mover = request(kind)
            initial = root(mover)
            until(lambda: not close_points(root(mover),initial),kind+' begins real shuffled/hopping approach')
            current = root(mover)
            before = rewards(pond,obj,key)
            if kind == 'wise_owl':
                pond._complete(plan)
                step()
                check(close_points(root(mover),current) and close_points(mover.target,current),
                      'premature owl completion releases the actual owned destination before its mover')
            else:
                mover.target = (current[0]-2,current[1])
                destination = mover.target
                pond.cancel()
                check(mover.target == destination,
                      'crow cleanup preserves a new independently owned destination')
            check(not work['events'] and not pond.minds.carnival_guests and
                  mover._shared_motion_owner is None and rewards(pond,obj,key) == before,
                  kind+': approach cleanup earns no material, shared or generic completion reward')

        pond,plan,work,obj,key,mover = request('mysterious_crow')
        until(lambda: bool(work['events']),'crow partial contact before reload')
        before = rewards(pond,obj,key)
        restored = LivingPond(json.loads(json.dumps(pond.save())))
        loaded_work = restored.state['plan']['carnival_work']
        game.living_pond = restored
        try:
            restored.attach(game,offline=False)
            restored._activity(0)
            loaded_obj = restored.object_state('bounce_house',plan['instance'])
            check(restored.state['plan'] is None and loaded_work.get('interrupted') and not restored.minds.carnival_guests,
                  'species reload cannot recreate a transient operator lease')
            check(loaded_work['events'] == [0] and loaded_obj['castle']['latch'] == 0 and
                  rewards(restored,loaded_obj,key) == before,
                  'species reload retains material work without completion reward')
        finally:
            restored.minds.close()
            game.living_pond = pond

        pond,plan,work,obj,key,mover = request('grumpy_toad','castle_hose_stow')
        check(obj['castle']['motor'] == 'on' and obj['castle']['hose'] == 0,
              'Grumble hose fixture begins with real blower work still required')
        until(lambda: bool(work['events']),'Grumble actually shuts down the blower')
        check(work['events'] == [0] and obj['castle']['motor'] == 'off' and obj['castle']['hose'] == 0,
              'actual shutdown contact precedes every hose manipulation')
        until(lambda: pond.state['plan'] is None,'Grumble completes reachable (9,6) hose work')
        check(work.get('recorded') and obj['uses'] == 1 and obj['castle']['motor'] == 'off' and obj['castle']['hose'] == 1,
              'reachable Grumble hose work completes once through real exits')
        before = rewards(pond,obj,key)
        pond._complete(plan)
        check(rewards(pond,obj,key) == before,'duplicate species completion cannot repeat any reward')

    print(json.dumps({'result':'PASS','checks':len(checks),'scope':'independent-species-lifecycle'}))
finally:
    if game.living_pond:game.living_pond.minds.close()
    if getattr(game,'_save_executor',None):game._save_executor.shutdown(wait=True)
    if getattr(game,'_talk_executor',None):game._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()


