import test from 'node:test';
import assert from 'node:assert/strict';
import {LivingWorld} from '../client/ultra-world.mjs';
import {castleGeometry,sharedCastleRecord,sharedCastleSource} from '../client/castle-care.mjs';
import {carnivalOccupants} from '../client/carnival-routines.mjs';
import {displayCamera,actorPitches} from '../client/actor-projection.mjs';
import {projectCastleWorld} from '../client/castle-projection.mjs';
import METRICS from '../client/animation/castle-guest-metrics.json' with {type:'json'};
import {specialSharedCastleFixture} from './castle-shared-fixtures.mjs';
const bindings=[['traveling_merchant','rare'],['celebrity_duck','rare'],['lost_duckling','rare'],['lost_duckling','story']];
const close=(a,b)=>assert.ok(Math.abs(a-b)<1e-8,`${a} != ${b}`);
function render(s,width,height){const sx=width/240,sy=height/112,world=new LivingWorld(),result=world.render({...s,camera:displayCamera(s.camera,sx,sy)},.1,.1),home=result.objects.find(o=>o.id==='bounce_house');return {result,home,sx,sy};}
test('three exact rare profiles and story Pip preserve nine contacts and real roots in every display mode',()=>{
 for(const [cast,adapter]of bindings)for(const [id,metrics]of Object.entries(METRICS.casts[cast].routines))for(const [index,metric]of metrics.entries())for(const [width,height]of [[1200,800],[1800,800],[900,1100]])for(const motion of [true,false]){
  const s=specialSharedCastleFixture(cast,adapter,id,index,{motion}),before=JSON.stringify(s),{home,sx,sy,result}=render(s,width,height),w=s.living.plan.carnival_work;
  assert.equal(home.carnivalRiders.length,2);const op=home.carnivalRiders.find(m=>m.role==='a'),watch=home.carnivalRiders.find(m=>m.watch),g=castleGeometry(home,op,sx,sy),target=projectCastleWorld(home.physicalCastle,w.physical.target,sx,sy);
  assert.equal(op.actor,w.shared.operator.actor);assert.equal(op.character.id,adapter==='story'?'story:lost_duckling':cast);assert.equal(op.character.profileId,cast);close(op.character.scale,metric.scale);assert(g.reachable&&g.tip);close(g.tip.x,target.x);close(g.tip.y,target.y);
  for(const m of [op,watch]){const geom=castleGeometry(home,m,sx,sy),root=m.watch?w.shared.cheese.root:w.physical.root,p=projectCastleWorld(home.physicalCastle,root,sx,sy),pitch=actorPitches(m.character,sx,sy);close(geom.character.x*sx,p.x);close(geom.character.y*sy,p.y);close(pitch.ch/pitch.cw,1.5);}
  assert.equal(watch.character.grip,null);assert(!result.characters.some(c=>c.id===op.character.id));assert.equal(JSON.stringify(s),before);
 }
});
test('rare and story arrivals and exits retain source walking without early contact',()=>{
 for(const [cast,adapter]of bindings)for(const phase of ['approach','exit'])for(const facing of [true,false]){
  const s=specialSharedCastleFixture(cast,adapter,'castle_door_open',1,{phase}),shared=sharedCastleRecord(s.living.plan.carnival_work);(adapter==='story'?s.storyActor:s.rareVisitor).facing=facing;
  assert(sharedCastleSource(s,shared));const {home,sx,sy}=render(s,1800,800),op=home.carnivalRiders.find(m=>m.role==='a');assert.equal(op.character.action,'walking');assert.equal(op.character.performance,null);assert.equal(castleGeometry(home,op,sx,sy).points.length,0);
 }
});
test('wrong adapters, missing live actors and changed story identities fail closed',()=>{
 const changes=[s=>s.living.plan.carnival_work.shared.operator.cast='friendly_goose',s=>delete s.living.plan.carnival_work.shared.operator.motion_token,s=>s.living.plan.carnival_work.shared.operator.adapter='regular',s=>s.rareVisitor=null];
 for(const change of changes){const s=specialSharedCastleFixture();change(s);assert.deepEqual(carnivalOccupants(s),[]);}
 for(const change of [s=>s.storyActor=null,s=>s.storyActor.id='story:pip',s=>s.storyActor.storyId='frog_choir',s=>s.living.story.step='choice',s=>s.living.story=null,s=>s.living.plan.carnival_work.shared.operator.render_id='story:other']){const s=specialSharedCastleFixture('lost_duckling','story');change(s);assert.deepEqual(carnivalOccupants(s),[]);}
 assert.equal(METRICS.casts['story:pip'],undefined);assert.equal(METRICS.casts['story:lost_duckling'],undefined);
});
