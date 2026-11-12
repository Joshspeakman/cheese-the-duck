import test from 'node:test';
import assert from 'node:assert/strict';
import {sharedCastleFixture,specialSharedCastleFixture} from './castle-shared-fixtures.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
import {displayCamera} from '../client/actor-projection.mjs';
import {castleGeometry,CASTLE_SCORES} from '../client/castle-care.mjs';
import {projectCastleWorld,castleArtWorld} from '../client/castle-projection.mjs';
import METRICS from '../client/animation/castle-air-metrics.json' with {type:'json'};
import {ObjectCanvas} from '../client/object-canvas.mjs';
import {softCastle,surfaceState} from '../client/soft-surfaces.mjs';
import {castleState} from '../client/castle-care.mjs';
import {castlePose} from '../client/castle-care.mjs';
import {castleActiveWork} from '../client/castle-air-geometry.mjs';
import {carnivalOccupants} from '../client/carnival-routines.mjs';

test('synthetic gauge observation projects actual eye ink and native target without a mechanical bridge',()=>{
 for(const cast of Object.keys(METRICS.casts))for(const motion of [true,false])for(const [width,height]of [[1800,800],[900,1100]]){
  const s=cast.startsWith('friend:')?sharedCastleFixture(cast):specialSharedCastleFixture(cast),w=s.living.plan.carnival_work;
  s.motion=motion;w.id='castle_gauge_check';w.clock=w.ride_elapsed=CASTLE_SCORES[w.id].duration*.52;w.physical.station='gauge';w.events=[0];
  w.physical.observation_target=castleArtWorld([59.4,24.5],161,139,{center:true});w.physical.observation_ready=true;
  // Deliberately stale hand-ready data must not create a mechanical connection.
  w.physical.contact_ready=true;
  const before=JSON.stringify(s),sx=width/240,sy=height/112,world=new LivingWorld(),out=world.render({...s,camera:displayCamera(s.camera,sx,sy)},0,0),home=out.objects.find(o=>o.id==='bounce_house'),member=home.carnivalRiders.find(m=>m.role==='a'),g=castleGeometry(home,member,sx,sy);
  assert.equal(g.tip,null);assert.deepEqual(g.points,[]);assert.ok(g.observation.ready);assert.ok(g.observation.eyes.length);
  assert.deepEqual(g.observation.target,projectCastleWorld(home.physicalCastle,w.physical.observation_target,sx,sy));
  assert.equal(JSON.stringify(s),before);
  const paused=castleGeometry(home,{...member,paused:true},sx,sy);assert.equal(paused.observation.ready,false);
  w.physical.observation_ready=false;assert.equal(castleGeometry(home,member,sx,sy).observation.ready,false);
 }
});

test('procedure projects only its bound atomic occurrence and never its flattened outer clock',()=>{
 const s=sharedCastleFixture(),outer=s.living.plan.carnival_work,child={id:'castle_gauge_check',occurrence_id:'reading-after',clock:15.6,ride_elapsed:15.6,events:[0],stage:'service'};
 Object.assign(outer,{id:'castle_pressure_check',clock:1e6,ride_elapsed:1e6,atomic:child,air_procedure:{version:1,id:'castle_pressure_check',attempt:'actual-attempt',current_occurrence:'reading-after',cursor:0,occurrences:[{occurrence_id:'reading-after',atomic_id:'castle_gauge_check',status:'active'}]}});outer.physical.station='gauge';
 const before=structuredClone(outer),resolved=castleActiveWork(outer);
 assert.equal(resolved.physical,outer.physical);assert.equal(resolved.shared,outer.shared);assert.equal(resolved.id,child.id);assert.equal(outer.id,'castle_pressure_check');
 const standalone={...outer,...child};delete standalone.air_procedure;delete standalone.atomic;assert.deepEqual(castlePose(outer),castlePose(standalone));
 assert.equal(carnivalOccupants(s).length,2);assert.deepEqual(outer,before);
 for(const change of [w=>w.atomic.occurrence_id='stale-reading',w=>delete w.atomic,w=>w.atomic.id='castle_dust_service',w=>w.air_procedure.id='castle_dust_service',w=>delete w.atomic.ride_elapsed,w=>w.air_procedure.occurrences[0].atomic_id='castle_start']){
  const bad=structuredClone(s);change(bad.living.plan.carnival_work);assert.deepEqual(carnivalOccupants(bad),[]);assert.equal(castlePose(bad.living.plan.carnival_work),null);
 }
 const exit=structuredClone(s),w=exit.living.plan.carnival_work;delete w.atomic;w.air_procedure.current_occurrence=null;w.air_procedure.phase='exit';w.air_procedure.occurrences[0].status='finished';w.physical.phase='exit';w.shared.phase='exit';w.shared.cheese.phase='exit';w.shared.cheese.ready=false;
 assert.equal(carnivalOccupants(exit).length,2);assert.equal(castlePose(w).surfaceWork,false);assert.equal(castlePose(w).contact,0);
 const sx=1800/240,sy=800/112,out=new LivingWorld().render({...exit,camera:displayCamera(exit.camera,sx,sy)},0,0),home=out.objects.find(o=>o.id==='bounce_house');
 for(const member of home.carnivalRiders){const g=castleGeometry(home,member,sx,sy);assert.ok(g.authoritativeRoot);assert.equal(g.tip,null);assert.deepEqual(g.points,[]);assert.equal(g.observation,null);}
});

test('gauge needle reads physical pressure independently of passive visual fill',()=>{
 for(const inflation of [0,.35,1]){
  const c=new ObjectCanvas(180,150);softCastle(c,{w:180,h:150},{inflation,surface:surfaceState(),castle:castleState({pressure:.5}),motion:true});
  assert.equal(c.art[136][161],'|');assert.equal(c.tones[136][161],'a');
 }
});

test('stale observation-ready flags cannot certify closed authored eyes',()=>{
 for(const progress of [.18,.85])for(const motion of [true,false]){
  const s=sharedCastleFixture(),w=s.living.plan.carnival_work;s.motion=motion;w.id='castle_gauge_check';w.clock=w.ride_elapsed=30*progress;w.physical.station='gauge';w.physical.observation_target=castleArtWorld([59.4,24.5],161,139,{center:true});w.physical.observation_ready=true;w.physical.contact_ready=true;
  const sx=6,sy=9,out=new LivingWorld().render({...s,camera:displayCamera(s.camera,sx,sy)},0,0),home=out.objects.find(o=>o.id==='bounce_house'),member=home.carnivalRiders.find(m=>m.role==='a'),g=castleGeometry(home,member,sx,sy);
  assert.deepEqual(g.observation.eyes,[]);assert.equal(g.observation.ready,false);assert.equal(g.tip,null);
 }
});

test('fan displays published coasting angle without electrical power; reduced motion preserves mechanics',()=>{
 for(const fan of [0,.5,1,1.5,2])for(const motion of [true,false]){
  const raw={powered:false,motor:'off',rotor_speed:.35,airflow:.21,fan},before=structuredClone(raw),care=castleState(raw),c=new ObjectCanvas(180,150);
  softCastle(c,{w:180,h:150},{inflation:.5,surface:surfaceState(),castle:care,motion});
  assert.equal(c.art[131][171],motion?['|','/','-','\\'][Math.floor(fan*2)%4]:'|');assert.deepEqual(raw,before);assert.equal(care.rotor_speed,.35);assert.equal(care.airflow,.21);assert.equal(care.fan,fan);
 }
 const c=new ObjectCanvas(180,150);softCastle(c,{w:180,h:150},{inflation:0,surface:surfaceState(),castle:castleState({powered:true,rotor_speed:0,fan:1}),motion:true});assert.equal(c.art[131][171],'o');
});
