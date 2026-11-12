"""Independent Flutter flight-observer lifecycle checks with disposable state.

The real DesktopGame update dispatch, GuestMotion/StoryMotion and camera transform run;
unrelated base-game timers and ambient brain decisions are isolated. This is
adversarial lifecycle coverage, not the separate flight age/control matrix.
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
os.environ['CHEESE_SAVE_DIR'] = tempfile.mkdtemp(prefix='cheese-flight-lifecycle-')
os.environ['SDL_AUDIODRIVER'] = 'dummy'
os.environ['SDL_VIDEODRIVER'] = 'dummy'

from engine import host, carnival, castle_work, castle_shared, castle_flight, castle_actors, guest_motion, visitor_shelters, excursions
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


def fixture(kind='butterfly_fairy', remaining=None, age='hatchling', site=(9,6)):
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
    mover.actor.update(x=30., y=30., facing=True)
    mover.target = (30., 30.)
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


def request(kind='butterfly_fairy', score='castle_door_open'):
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


def anatomy_review():
    source = r'''
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {characterSprite} from './engine/client/ultra-characters.mjs';
import {performancePose} from './engine/client/performances.mjs';
import {CASTLE_SCORES,castlePose} from './engine/client/castle-care.mjs';
import {DUCK_AGES} from './engine/client/duck-designs.mjs';
import {LivingWorld} from './engine/client/ultra-world.mjs';
import {seedOf} from './engine/client/ultra-grid.mjs';
import {displayCamera} from './engine/client/actor-projection.mjs';
import {itemSprite,itemWorldScale} from './engine/client/ultra-items.mjs';
const metric=JSON.parse(fs.readFileSync('engine/client/animation/castle-flight-metrics.json'));
const baseDuck={id:'butterfly_fairy',castId:'butterfly_fairy',state:'walking'};
let samples=0,wingWidths=new Set(),tops=new Set();
function audit(c){
 assert.equal(c.scale,.4);assert.equal(c.groundRow,39.5);assert.equal(c.profileId,'butterfly_fairy');
 assert(!c.grip&&c.rig.feet.length===0&&!c.clipped,'no invented anatomy or clipped envelope');
 const cells=[];c.art.forEach((r,y)=>[...r].forEach((ch,x)=>{if(ch!==' ')cells.push({x,y,w:1});}));cells.push(...c.fills);
 for(const p of cells)assert(p.x-c.anchorX>=metric.body.x&&p.x+p.w-c.anchorX<=metric.body.x+metric.body.w&&p.y-c.groundRow>=metric.body.y&&p.y+1-c.groundRow<=metric.body.y+metric.body.h,'actual full flight ink escapes envelope');
 const wing=c.fills.filter(f=>f.tone==='p');wingWidths.add(Math.max(...wing.map(f=>f.x+f.w))-Math.min(...wing.map(f=>f.x)));
 tops.add(Math.min(...cells.map(p=>p.y)));samples++;
}
// Incommensurate dense times over many fold/lift/spark cycles, independent of
// the exporter's analytical boundary sampler and its stated period.
for(const facing of [true,false])for(let i=0;i<1600;i++)audit(characterSprite({...baseDuck,facing},i*.03713,true));
assert(wingWidths.size>=3&&tops.size>=3,'audit must exercise actual fold and hover lift');
for(const id of ['castle_start','castle_door_open','castle_hose_stow'])for(const [index,[at]]of CASTLE_SCORES[id].effects.entries()){
 const clock=at*CASTLE_SCORES[id].duration,base={id,stage:'service',clock,ride_elapsed:clock},station=castlePose(base).station;
 for(const consumed of [false,true])for(const facing of [true,false])for(const motion of [true,false]){
  const work={...base,flight_observer:true,physical_pilot:true,shared_physical:true,events:consumed?[index]:[],physical:{version:1,actor:'cheese',phase:'hold',station,root:[0,0],target:[0,0],contact_ready:true},shared:{version:1,mode:'flight-observer',attempt:'independent-flight',source_age:'hatchling',phase:'operate',operator:{actor:'cheese',adapter:'cheese',source_age:'hatchling'},observer:{actor:'butterfly_fairy',cast:'butterfly_fairy',adapter:'rare',token:'visit',motion_token:'motion',location:'Home Pond'},observer_physical:{root:[0,0],stance:[0,0],exit:[0,0],phase:'hold',ready:true}}};
  const performance={kind:'carnival',routine:work,role:'b',watch:true,motion},pose=performancePose(performance),before=JSON.stringify(work);
  assert.equal(pose.surfaceWork,false);assert.equal(pose.contact,0);assert.equal(pose.reach,0);
  assert.equal(pose.eye,consumed?'^':'O','only consumed material events trigger observation');
  for(let i=0;i<25;i++)audit(characterSprite({...baseDuck,facing,performance},i*.27193,true));
  assert.equal(JSON.stringify(work),before,'render/reaction never writes effect authority');
 }
}
let operators=0,scenery=0,items=0;
for(const stage of DUCK_AGES.filter(a=>a.id!=='egg')){
 const envelope=metric.operators[stage.id];assert(envelope&&envelope.appearance==='unequipped');
 const inspect=c=>{
  assert.equal(c.scale,envelope.scale);
  const cells=[];c.art.forEach((r,y)=>[...r].forEach((ch,x)=>{if(ch!==' ')cells.push({x,y,w:1});}));cells.push(...c.fills);
  for(const p of cells)assert(p.x-c.anchorX>=envelope.body.x&&p.x+p.w-c.anchorX<=envelope.body.x+envelope.body.w&&p.y-c.groundRow>=envelope.body.y&&p.y+1-c.groundRow<=envelope.body.y+envelope.body.h,stage.id+' actual head/working wing escapes operator envelope');
 };
 for(const facing of [true,false]){
  for(let phase=0;phase<64;phase++)inspect(characterSprite({stage:stage.id,facing,state:'walking'},phase*.15793));
  for(const id of ['castle_start','castle_door_open','castle_hose_stow'])for(const [at]of CASTLE_SCORES[id].track)for(const motion of [true,false]){
   const clock=at*CASTLE_SCORES[id].duration;
   inspect(characterSprite({stage:stage.id,facing,performance:{kind:'carnival',role:'a',motion,routine:{id,clock,ride_elapsed:clock,stage:'service'}}},0));
  }
 }
 operators++;
}
const sceneryMetrics=JSON.parse(fs.readFileSync('engine/client/animation/castle-scenery-metrics.json'));
for(const time of [0,1.739,8.071]){
 let reference=null;
 for(const [width,height]of [[1120,820],[2240,600],[700,1100]]){
  const camera=displayCamera({x:12,y:8,w:70,h:25},width/240,height/136),world=new LivingWorld();world.scenery=[];
  world.landmarks({location:'Home Pond',biome:'pond',season:'spring',particles:false,camera},time,seedOf('Home Pond'));
  const layers=world.scenery.filter(s=>s.nativeCells);assert.equal(layers.length,3);
  const native=JSON.stringify(layers.map(l=>[l.id,l.nativeCells]));if(reference===null)reference=native;else assert.equal(native,reference,'camera must not change actual native scenery extent');
  for(const layer of layers){
   const b=sceneryMetrics.features.find(f=>f.id===layer.id).bounds;
   for(const [x,y,w,h,ch]of layer.projectedCells)if(ch!==32){
    const wx=(x-24)*camera.w/192+camera.x,wy=(y-46)*camera.h/47+camera.y;
    assert(wx>=b.x-1e-7&&wx+w*camera.w/192<=b.x+b.w+1e-7&&wy>=b.y-1e-7&&wy+h*camera.h/47<=b.y+b.h+1e-7,'actual projected canopy/dock escapes native collision bounds');
   }
   scenery++;
  }
 }
}
const footprints=JSON.parse(fs.readFileSync('engine/client/animation/object-footprints.json')).items;
for(const id of ['tree_oak','grandfather_clock','street_lamp','windmill','wardrobe','castle_tower']){
 const footprint=footprints[id];assert(footprint&&!footprint.floor);
 for(let phase=0;phase<17;phase++){
  const model=itemSprite(id,phase*.713,{interaction:{kind:'item',target:id,phase:'act',progress:phase/16}}),scale=itemWorldScale(id)*(model.detailScale||1);
  model.art.forEach((r,y)=>[...r].forEach((ch,x)=>{if(ch===' ')return;for(const dx of [0,1])for(const dy of [0,1]){
   const py=(y+dy-model.art.length-model.lift)*scale,px=(x+dx-model.width/2+(y+dy-model.art.length)*1.5*model.sway)*scale;
   assert(px>=-footprint.width/2&&px<=footprint.width/2&&py>=-footprint.height&&py<=.65*47/12,id+' transformed tall artwork escapes full placement bounds');
  }}));
 }
 items++;
}
console.log(JSON.stringify({samples,wingWidths:wingWidths.size,lifts:tops.size,operators,scenery,items}));
'''
    result = subprocess.run(['node','--input-type=module'],input=source,text=True,cwd=ROOT,capture_output=True)
    assert result.returncode == 0,result.stderr
    result = json.loads(result.stdout)
    check(result['samples'] == 5000 and result['wingWidths'] >= 3 and result['lifts'] >= 3,
          'independent full-ink flight envelope audit covers real folds/lifts, all effects and both motion modes')
    check(result['operators'] == 8,'all age operator envelopes contain actual head, body, feet and working wings')
    check(result['scenery'] == 27,'actual canopy/dock ink stays in identical native bounds under three aspect ratios')
    check(result['items'] == 6,'representative tall item bounds contain actual animated/sheared artwork')


def assert_interrupted(pond,work,obj,key,before,label,events):
    check(pond.state['plan'] is None and work.get('interrupted') and not pond.minds.carnival_guests,
          label+': shared ownership is fully released')
    check(work['events'] == events and rewards(pond,obj,key) == before,
          label+': applied mechanics survive without completion or learning rewards')


try:
    game._running = True
    game._start_new_game()
    game._flush_pending_save()
    game._state = 'playing'
    sound_engine.enabled = False
    anatomy_review()
    with controlled_clocks():
        pond,iid,obj,key,mover = fixture()
        geometry_plan = {'target':'bounce_house','instance':iid}
        geometry_plan['carnival_work'] = castle_work.make(pond,geometry_plan,'castle_door_open')
        center = castle_work.placement_center(pond,geometry_plan)
        check(castle_flight.flight_clear(pond,geometry_plan,root(mover),center,cheese_root()),
              'independent flight fixture begins outside fabric, scenery and other body envelopes')
        for label,point in (('western willow canopy',[22,26]),('dock lantern',[95,26])):
            check(not castle_flight.flight_clear(pond,geometry_plan,point,center),
                  'actual '+label+' blocks flight beyond its narrow ground reservation')
        grill = castle_work.control_world(center,'grill')
        exhaust_point = [grill[0]+8,grill[1]+10]
        check(obj['castle']['motor']=='off' and not castle_flight.flight_clear(pond,geometry_plan,exhaust_point,center),
              'future blower stream remains reserved before the switch can turn it on')
        check(not castle_flight.flight_clear(pond,geometry_plan,[center[0],12],center),
              'a flight root cannot pass through the actual castle fabric')
        with patch.object(castle_shared.terrain,'water_at',lambda *args:True):
            check(castle_flight.flight_clear(pond,geometry_plan,root(mover),center) and
                  not castle_work.supported(pond,geometry_plan,cheese_root(),center),
                  'flight uses airborne clearance while the real operator still requires dry grounded feet')
        geometry_plan['carnival_work']['source_age'] = 'adult'
        cr = [44,34]
        torso = castle_flight.box(cr,castle_shared.cheese_metric('adult'))
        observer_box = castle_flight.box([0,0],castle_flight.METRIC)
        over_head = [cr[0],torso[1]-.6-observer_box[1]-observer_box[3]]
        check(not castle_flight.overlap(castle_flight.box(over_head,castle_flight.METRIC),torso) and
              castle_flight.flight_clear(pond,geometry_plan,over_head,center) and
              not castle_flight.flight_clear(pond,geometry_plan,over_head,center,cr),
              'Cheese head and working-body envelope block a corridor that the former torso-only box accepted')
        game.habitat.owned_items.append('grandfather_clock')
        game.habitat.placed_items.append(PlacedItem('grandfather_clock',30*20/132,33*12/42))
        check(not castle_flight.flight_clear(pond,geometry_plan,root(mover),center),
              'a tall placed object blocks its complete artwork, not only its ground feet')
        game.habitat.placed_items = game.habitat.placed_items[:1]
        with patch.object(pond.layout,'occupied',lambda **kwargs:[('unmeasured_obstacle',18,10,None)]):
            check(not castle_flight.flight_clear(pond,geometry_plan,root(mover),center),
                  'an unmeasured obstacle cannot silently inherit the default small footprint')

        for wind in (None,'calm',float('nan'),float('inf'),-1):
            pond,iid,obj,key,mover = fixture()
            pond.state['ecology']['wind'] = wind
            before = copy.deepcopy((obj,pond.minds.tasks,pond.minds.model.state,cheese_root(),root(mover),mover.target))
            ok,_ = carnival.request(pond,'bounce_house','castle_door_open',iid,together=True)
            check(not ok and pond.state['plan'] is None and not pond.minds.carnival_guests and
                  (obj,pond.minds.tasks,pond.minds.model.state,cheese_root(),root(mover),mover.target) == before,
                  'malformed/nonfinite/negative wind refuses atomically: '+repr(wind))

        for coordinate in ('30',True,None,float('nan')):
            pond,iid,obj,key,mover = fixture()
            actual = root(mover)
            before = copy.deepcopy((obj,pond.minds.tasks,pond.minds.model.state,mover.target))
            mover.actor['x'] = coordinate
            try:
                ok,_ = carnival.request(pond,'bounce_house','castle_door_open',iid,together=True)
                check(not ok and pond.state['plan'] is None and not pond.minds.carnival_guests and
                      (obj,pond.minds.tasks,pond.minds.model.state,mover.target) == before,
                      'invalid raw Flutter scalar cannot be coerced into a rendered/native reservation: '+repr(coordinate))
            finally:
                mover.actor['x'] = actual[0]

        for refusal in ('unreachable_door','unreachable_hose','egg','wind','rain','departure_budget','third_story','outfit'):
            score = 'castle_hose_stow' if refusal == 'unreachable_hose' else 'castle_door_open'
            pond,iid,obj,key,mover = fixture(site=(9,7) if refusal.startswith('unreachable') else (9,6),
                                           age='egg' if refusal == 'egg' else 'hatchling',
                                           remaining=12 if refusal == 'departure_budget' else None)
            if refusal == 'wind':pond.state['ecology']['wind'] = .5
            if refusal == 'rain':pond.weather_type = 'rain'
            if refusal == 'third_story':pond.state['story'] = {'id':'frog_choir','step':0,'choices':[]}
            if refusal == 'outfit':game.habitat.equipped_cosmetics = {'hat':'hat_wizard'}
            before = copy.deepcopy((obj,pond.minds.tasks,pond.minds.model.state,cheese_root(),root(mover),mover.target))
            ok,message = carnival.request(pond,'bounce_house',score,iid,together=True)
            check(not ok and pond.state['plan'] is None and not pond.minds.carnival_guests,
                  refusal+': flight partnership refuses before acquisition: '+message)
            check((obj,pond.minds.tasks,pond.minds.model.state,cheese_root(),root(mover),mover.target) == before,
                  refusal+': no task, root, mechanical or learning mutation')

        pond,iid,obj,key,mover = fixture()
        game.habitat.equipped_cosmetics = {'hat':None,'body':'','face':False}
        proposal,message = castle_flight.propose(pond,'castle_door_open',iid)
        check(proposal is not None,'empty and false wardrobe slots are not mistaken for an unmeasured outfit: '+message)

        pond,plan,work,obj,key,mover = request()
        chat = carnival.conversation(pond,plan,'cheese'),carnival.conversation(pond,plan,key)
        check(chat[0]['role']=='operator' and chat[1]['role']=='observer' and
              'flying' in chat[1]['body_status'] and carnival.conversation(pond,plan,'unrelated') is None,
              'ordinary conversation identifies actual flight roles without a legacy companion lease lookup')
        initial = cheese_root(),root(mover)
        for _ in range(3):pond._activity(10)
        check((cheese_root(),root(mover)) == initial and work['clock'] == 0 and not work['events'],
              'a timer cannot arrive Flutter or begin Cheese control work before real independent flight')
        until(lambda: not close_points(root(mover),initial[1]),'Flutter starts real approach')
        check(cheese_root() == initial[0] and not work['events'],
              'Flutter approaches first while the actual operator remains held')
        plan['paused'] = True
        game.renderer.duck_pos.set_state_by_name('idle',0)
        roots = cheese_root(),root(mover)
        step()
        check((cheese_root(),root(mover)) == roots and game.renderer.duck_pos.get_state() == 'thinking',
              'plain pause converts idle into a non-wandering held state before the base mover')
        game.duck.current_action = 'feed'
        game.renderer.duck_pos.set_state_by_name('eating',0)
        game.renderer._viewport_width,game.renderer._viewport_height = 70,25
        game.renderer._update_camera(70,25)
        for _ in range(4):step()
        check((cheese_root(),root(mover)) == roots and game.renderer.duck_pos.get_state() == 'eating' and work['clock'] == 0,
              'camera and direct care preserve both independent native roots without flight or service progress')
        plan['paused'] = False
        game.duck.current_action = None
        until(lambda: bool(work['events']),'Cheese reaches real first contact after Flutter arrival')
        frame = snapshot(game,game.renderer)
        physical = frame['living']['plan']['carnival_work']['physical']
        observer = frame['living']['plan']['carnival_work']['shared']['observer_physical']
        check(physical['actor'] == 'cheese' and physical['contact_ready'] is True and
              close_points(physical['root'],cheese_root()) and close_points(observer['root'],root(mover)) and
              close_points([frame['rareVisitor']['x'],frame['rareVisitor']['y']],root(mover)),
              'end-of-host frame has one actual grounded operator and one actual independent airborne observer')
        metric = castle_work.effect_metrics(work)[0]
        check(all(f[1] == 0 for f in metric['feet']) and
              castle_work.reach_distance(cheese_root(),physical['target'],metric['grip'],metric['scale']) <= 3,
              'small Cheese earns contact using current age feet and grip, without an adult fallback')
        chat = carnival.conversation(pond,plan,'cheese'),carnival.conversation(pond,plan,key)
        check(all(c['completed_contacts']==1 and c['door_buckled'] is False for c in chat) and
              'controls' in chat[0]['body_status'] and 'hover' in chat[1]['body_status'],
              'conversation reports applied material state and independent hover without granting Flutter mechanism authority')
        elapsed,events = work['clock'],list(work['events'])
        mover.actor['facing'] = not (cheese_root()[0] >= root(mover)[0])
        castle_flight.advance(pond,plan,5)
        check(work['clock'] == elapsed and work['events'] == events and work['physical']['contact_ready'] is False,
              'an observer facing away cannot earn a watched effect merely from a ready flag')
        before = rewards(pond,obj,key)
        plan['paused'] = True
        pond.state['ecology']['wind'] = .5
        step()
        assert_interrupted(pond,work,obj,key,before,'wind arriving during paused partial work',[0])
        check(obj['castle']['latch'] == 0,'wind interruption does not restore consumed latch')

        for invalidation in ('departure','replacement','growth','malformed_flag','malformed_observer','third_story','outfit'):
            pond,plan,work,obj,key,mover = request()
            until(lambda: bool(work['events']),'first contact before '+invalidation)
            before = rewards(pond,obj,key)
            plan['paused'] = True
            visitor,arrival = game.atmosphere.current_visitor
            if invalidation == 'departure':clock = SimDatetime.fromisoformat(arrival).timestamp()+visitor.stay_duration_hours*3600-5.9
            elif invalidation == 'replacement':game.atmosphere.current_visitor = (visitor,(SimDatetime.now()+timedelta(seconds=1)).isoformat())
            elif invalidation == 'growth':game.duck.growth_stage = 'duckling'
            elif invalidation == 'malformed_flag':work['flight_observer'] = False
            elif invalidation == 'malformed_observer':work['shared']['observer'] = {'actor':'cheese','adapter':'cheese'}
            elif invalidation == 'third_story':pond.state['story'] = {'id':'frog_choir','step':0,'choices':[]}
            else:game.habitat.equipped_cosmetics = {'hat':'hat_wizard'}
            check(carnival.conversation(pond,plan,key) is None,
                  invalidation+': conversation rejects an invalid role contract before any host cleanup')
            step()
            assert_interrupted(pond,work,obj,key,before,invalidation,[0])
            check(mover._shared_motion_owner is None,invalidation+': stale flight target ownership is gone')
            if invalidation == 'departure':check(game.atmosphere.current_visitor[1] == arrival,'Flutter departure never extends the visit')

        for release_case in ('premature_callback','new_destination','malformed_callback'):
            pond,plan,work,obj,key,mover = request()
            start = root(mover)
            until(lambda: not close_points(root(mover),start),'Flutter actual moving cleanup')
            current = root(mover)
            before = rewards(pond,obj,key)
            if release_case == 'premature_callback':
                pond._complete(plan)
                step()
                check(close_points(root(mover),current) and close_points(mover.target,current),
                      'premature completion releases the owned observer target before actual GuestMotion')
            else:
                mover.target = (current[0]-2,current[1])
                destination = mover.target
                if release_case == 'malformed_callback':
                    pond.minds.carnival_guests[key] = 'broken lease'
                    pond._complete(plan)
                    check(mover.target == destination and not pond.minds.carnival_guests,
                          'direct malformed-lease callback removes garbage without claiming an independent target')
                    step()
                else:
                    pond.cancel()
                    check(mover.target == destination,'flight release preserves an independently replaced destination')
            check(not work['events'] and not pond.minds.carnival_guests and mover._shared_motion_owner is None and rewards(pond,obj,key) == before,
                  release_case+': no contact or shared/generic reward')

        for fault in ('new_tall_obstacle','invalid_root','invalid_lease_contract','invalid_lease_row'):
            pond,plan,work,obj,key,mover = request()
            until(lambda: bool(work['events']),'first contact before '+fault)
            before = rewards(pond,obj,key)
            roots = cheese_root(),root(mover)
            if fault == 'new_tall_obstacle':
                game.habitat.owned_items.append('grandfather_clock')
                game.habitat.placed_items.append(PlacedItem('grandfather_clock',roots[1][0]*20/132,(roots[1][1]+3)*12/42))
                step()
                check(close_points(root(mover),roots[1]),'a new flight obstruction interrupts before the real mover takes a step')
            elif fault == 'invalid_root':
                game.renderer.duck_pos.x = None
                check(carnival.conversation(pond,plan,key) is None,'invalid actual operator root cannot publish a valid conversation contract')
                castle_flight.refresh(pond)
                game.renderer.duck_pos.x = roots[0][0]
                pond._activity(0)
            elif fault == 'invalid_lease_contract':
                pond.minds.carnival_guests[key]['contract'] = []
                castle_flight.refresh(pond)
                pond._activity(0)
            else:
                destination = (roots[1][0]+2,roots[1][1])
                mover.target = destination
                pond.minds.carnival_guests[key] = 'broken lease'
                step()
                check(mover.target == destination,
                      'a non-dict lease is removed without claiming or stopping an independently replaced destination')
            assert_interrupted(pond,work,obj,key,before,fault,[0])
            check(mover._shared_motion_owner is None,fault+': actual observer target ownership is released')

        pond,plan,work,obj,key,mover = request()
        until(lambda: bool(work['events']),'first contact before interrupted flight reload')
        before = rewards(pond,obj,key)
        restored = LivingPond(json.loads(json.dumps(pond.save())))
        loaded = restored.state['plan']['carnival_work']
        game.living_pond = restored
        try:
            restored.attach(game,offline=False)
            restored._activity(0)
            loaded_obj = restored.object_state('bounce_house',plan['instance'])
            check(restored.state['plan'] is None and loaded.get('interrupted') and not restored.minds.carnival_guests,
                  'flight reload interrupts both roles rather than resuming solo Cheese behind a saved observer')
            check(loaded['events'] == [0] and loaded_obj['castle']['latch'] == 0 and rewards(restored,loaded_obj,key) == before,
                  'flight reload preserves material effects but no receipt or operator/observer learning')
        finally:
            restored.minds.close()
            game.living_pond = pond

        for change in ('wind','wet_exit'):
            pond,plan,work,obj,key,mover = request(score='castle_hose_stow')
            until(lambda: work['shared']['phase']=='done','both actual exits before '+change+' callback')
            check(not work.get('recorded') and obj['uses']==0,
                  change+': both exits are reached before the outer callback consumes its receipt')
            before = rewards(pond,obj,key)
            consumed = list(work['events'])
            if change == 'wind':
                pond.state['ecology']['wind'] = .5
                check(not carnival.completion_ready(pond,plan),
                      'current flight weather guards direct completion even before host refresh')
                pond._complete(plan)
            else:
                cr = cheese_root()
                metric = castle_work.rig_metric(work)
                bx,by = castle_work.pitches(metric)
                wet = [cr[0]+metric['feet'][0][0]*bx,cr[1]+metric['feet'][0][1]*by]
                water_at = castle_shared.terrain.water_at
                def flooded_exit(location,x,y,biome=None):
                    return abs(x-wet[0])<.01 and abs(y-wet[1])<.01 or water_at(location,x,y,biome)
                with patch.object(castle_shared.terrain,'water_at',flooded_exit):
                    check(castle_work.physical_geometry_ok(pond,plan) and not carnival.completion_ready(pond,plan),
                          'a still-valid saved contact stance cannot hide lost support beneath the actual exit feet')
                    pond._complete(plan)
            check(rewards(pond,obj,key)==before and not work.get('recorded') and work['events']==consumed and
                  obj['castle']['motor']=='off' and obj['castle']['hose']==1 and not pond.minds.carnival_guests,
                  change+': rejected callback retains completed mechanics without awarding any shared/generic receipt')

        pond,plan,work,obj,key,mover = request(score='castle_hose_stow')
        before_counts = copy.deepcopy({actor:pond.minds.model.residents[actor]['counts'] for actor in ('cheese',key)})
        until(lambda: work['shared']['phase'] == 'exit','Cheese finishes grounded work and reaches exit')
        check(work['done'] is True and not castle_flight.completion_ready(pond,plan) and obj['uses'] == 0 and
              all(pond.minds.model.residents[actor]['counts'] == before_counts[actor] for actor in ('cheese',key)),
              'native operator done cannot claim shared completion before Flutter independently exits')
        until(lambda: pond.state['plan'] is None,'Flutter reaches actual flight exit and shared completion')
        check(work.get('recorded') is True and obj['uses'] == 1 and obj['castle']['motor'] == 'off' and obj['castle']['hose'] == 1,
              'all real controls and both exits claim one shared completion')
        for actor,action in (('cheese','practice'),('cheese','share'),(key,'observe'),(key,'share')):
            check(pond.minds.model.residents[actor]['counts'].get(action,0) == before_counts[actor].get(action,0)+1,
                  actor+' learns only the demonstrated '+action+' role once')
        check(pond.minds.model.residents[key]['counts'].get('practice',0) == before_counts[key].get('practice',0) and
              pond.minds.model.residents['cheese']['counts'].get('observe',0) == before_counts['cheese'].get('observe',0),
              'role reversal gives Flutter no operator practice and Cheese no invented observer action')
        before = rewards(pond,obj,key)
        pond._complete(plan)
        check(rewards(pond,obj,key) == before,'duplicate flight callback leaves all rewards unchanged')

    print(json.dumps({'result':'PASS','checks':len(checks),'scope':'independent-flight-lifecycle'}))
finally:
    if game.living_pond:game.living_pond.minds.close()
    if getattr(game,'_save_executor',None):game._save_executor.shutdown(wait=True)
    if getattr(game,'_talk_executor',None):game._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()


