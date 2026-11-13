// Explicit session-envelope fixtures; native session execution is separate.
import test from 'node:test';
import assert from 'node:assert/strict';
import {sharedCastleFixture} from './castle-shared-fixtures.mjs';
import {eggCaregiverFixture} from './egg-caregiver-fixtures.mjs';
import {flightFixture} from './castle-flight-fixtures.mjs';
import {sharedCastleRecord,castleGeometry} from '../client/castle-care.mjs';
import {carnivalOccupants} from '../client/carnival-routines.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
import {displayCamera} from '../client/actor-projection.mjs';

function sessionFixture(mode,stage){
 const s=mode==='egg-caregiver'?eggCaregiverFixture():mode==='flight-observer'?flightFixture():sharedCastleFixture(),w=s.living.plan.carnival_work,child={id:w.id,occurrence_id:'read-session:0',stage:w.stage,clock:w.clock,ride_elapsed:w.ride_elapsed,events:[...w.events]},active=stage==='operate',initial=stage==='observer_approach';
 w.id='castle_pressure_check';w.shared.mode=mode;w.shared.phase=stage;
 if(mode==='solo'){w.shared_physical=false;w.physical_pilot=true;w.physical.actor='cheese';w.shared.operator={actor:'cheese',adapter:'cheese',source_age:s.duck.stage,token:'source-cheese'};delete w.shared.cheese;Object.assign(s.duck,{x:w.physical.root[0],y:w.physical.root[1]});s.visitor=null;}
 w.source_age=w.shared.source_age;w.shared.attempt='read-session';w.shared.instance=s.living.plan.instance;w.shared.center=[s.items[0].x,s.items[0].y];w.physical.center=[...w.shared.center];w.shared.destination=[...s.living.plan.destination];s.living.plan.location=s.location;
 w.air_procedure={version:1,id:w.id,attempt:'read-session',phase:initial?'approach':active?'hold':'exit',current_occurrence:active?child.occurrence_id:null,cursor:initial?-1:0,occurrences:[{occurrence_id:child.occurrence_id,atomic_id:child.id,status:initial?'pending':active?'active':'finished'}]};
 if(active)w.atomic=child;else delete w.atomic;
 w.physical.phase=stage==='operator_exit'?'exit':'hold';w.physical.contact_ready=active;
 const watcher=w.shared.cheese||w.shared.observer_physical;if(watcher){watcher.phase=initial?'approach':stage==='observer_exit'?'exit':'hold';watcher.ready=watcher.phase==='hold';}
 s.living.plan.phase='act';return s;
}
test('explicit air session stages preserve roots and stationary egg without relaxing atomic role phases',()=>{
 for(const mode of ['visitor-operator','flight-observer','egg-caregiver','solo'])for(const phase of (['egg-caregiver','solo'].includes(mode)?['operate','operator_exit']:['observer_approach','operate','operator_exit','observer_exit'])){
  const s=sessionFixture(mode,phase),before=JSON.stringify(s),w=s.living.plan.carnival_work;
  if(mode!=='solo')assert.ok(sharedCastleRecord(w),mode+' '+phase);assert.equal(carnivalOccupants(s).length,['egg-caregiver','solo'].includes(mode)?1:2);
  const sx=7.5,sy=800/112,out=new LivingWorld().render({...s,camera:displayCamera(s.camera,sx,sy)},0,0),home=out.objects.find(o=>o.id==='bounce_house');
  assert.equal(home.carnivalRiders.length,['egg-caregiver','solo'].includes(mode)?1:2);
  for(const member of home.carnivalRiders){const g=castleGeometry(home,member,sx,sy);assert.ok(g.authoritativeRoot);if(phase!=='operate'||member.watch){assert.equal(g.tip,null);assert.deepEqual(g.points,[]);assert.equal(g.observation,null);}}
  if(mode==='egg-caregiver'){const egg=out.characters.find(c=>c.cheese);assert.ok(egg);assert.equal(egg.performance,null);assert.equal(egg.grip,null);assert.equal(egg.facing,s.duck.facing);}
  assert.equal(JSON.stringify(s),before);
 }
 for(const s of [sharedCastleFixture(),flightFixture(),eggCaregiverFixture()]){s.living.plan.carnival_work.shared.phase='operator_exit';assert.equal(sharedCastleRecord(s.living.plan.carnival_work),null);assert.deepEqual(carnivalOccupants(s),[]);}
});
test('session wrong mode, occurrence and egg destination fail closed',()=>{
 for(const change of [s=>s.living.plan.carnival_work.shared.mode='other',s=>s.living.plan.carnival_work.atomic.occurrence_id='other',s=>s.living.plan.carnival_work.air_procedure.occurrences[0].atomic_id='castle_stop',s=>s.living.plan.carnival_work.shared.attempt='other',s=>s.living.plan.carnival_work.shared.center[0]+=1,s=>s.living.plan.instance='other']){
  const s=sessionFixture('visitor-operator','operate');change(s);assert.deepEqual(carnivalOccupants(s),[]);
 }
 const s=sessionFixture('egg-caregiver','operate');delete s.living.plan.carnival_work.shared.destination;assert.deepEqual(carnivalOccupants(s),[]);
});
