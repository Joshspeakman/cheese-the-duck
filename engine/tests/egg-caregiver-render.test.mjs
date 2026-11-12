import test from 'node:test';
import assert from 'node:assert/strict';
import {LivingWorld} from '../client/ultra-world.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {displayCamera} from '../client/actor-projection.mjs';
import {castleGeometry,eggCaregiverScene} from '../client/castle-care.mjs';
import {carnivalOccupants} from '../client/carnival-routines.mjs';
import {projectCastleWorld} from '../client/castle-projection.mjs';
import GUESTS from '../client/animation/castle-guest-metrics.json' with {type:'json'};
import {eggCaregiverFixture} from './egg-caregiver-fixtures.mjs';
import NATIVE_CONTACT from './egg-caregiver-native-contact.json' with {type:'json'};
const near=(a,b)=>assert(Math.abs(a-b)<1e-8,`${a} != ${b}`);
function render(s,width=1200,height=800,time=0,world=new LivingWorld()){const sx=width/240,sy=height/112,display={...s,camera:displayCamera(s.camera,sx,sy)},result=world.render(display,time,.1),home=result.objects.find(o=>o.id==='bounce_house');return {world,result,home,sx,sy,display};}
test('every exact caregiver owns control contacts while the original egg remains outside mechanical staging',()=>{
 for(const cast of Object.keys(GUESTS.casts))for(const [id,metrics]of Object.entries(GUESTS.casts[cast].routines))for(const [index]of metrics.entries()){
  const adapter=cast.startsWith('friend:')?'regular':'rare',s=eggCaregiverFixture(cast,adapter,id,index),before=JSON.stringify(s),time=3.14,{home,result,sx,sy,display}=render(s,1800,800,time),members=home.carnivalRiders;assert.equal(members.length,1);const op=members[0],g=castleGeometry(home,op,sx,sy);assert.equal(op.role,'a');assert.equal(op.character.profileId,cast);assert(g.tip&&g.reachable);near(g.tip.x,g.target.x);near(g.tip.y,g.target.y);
  const egg=result.characters.find(c=>c.cheese),expected=characterSprite({...s.duck,motion:true,performance:null},time),p=projectCastleWorld({camera:display.camera},[s.duck.x,s.duck.y],sx,sy);assert(egg);near(egg.x*sx,p.x);near(egg.y*sy,p.y);for(const key of ['art','fills','offsetY','scale','facing','phase','rig','grip','bill','performance'])assert.deepEqual(egg[key],expected[key]);assert.equal(egg.physicalCastleActor,undefined);assert.equal(JSON.stringify(s),before);
 }
});
test('egg root and facing remain source-owned across caregiver phases, cameras, pause and Reduced Motion',()=>{
 for(const adapter of ['rare','story'])for(const facing of [true,false])for(const phase of ['approach','hold','exit'])for(const motion of [true,false])for(const [width,height]of [[1200,800],[1800,800],[900,1100]]){
  const s=eggCaregiverFixture('lost_duckling',adapter,'castle_door_open',1,{phase,motion,facing}),world=new LivingWorld();world.duckPosition=[200,10];s.living.minds={performances:[{phase:'act',a:'cheese',b:'other',performance:'wing_bump',elapsed:5,duration:12}]};
  const {result,home,sx,sy,display}=render(s,width,height,motion?2.7:0,world),egg=result.characters.find(c=>c.cheese),p=projectCastleWorld({camera:display.camera},s.living.plan.carnival_work.shared.recipient.root,sx,sy);near(egg.x*sx,p.x);near(egg.y*sy,p.y);assert.equal(egg.facing,facing);assert.equal(egg.performance,null);assert.equal(egg.rig,null);assert.equal(home.carnivalRiders.length,1);
  s.living.plan.paused=true;const paused=render(s,width,height,2.7);assert.equal(castleGeometry(paused.home,paused.home.carnivalRiders[0],paused.sx,paused.sy).points.length,0);
 }
});
test('changed age, egg identity, root, facing and malformed caregiver markers reject old bindings without fallback',()=>{
 for(const change of [s=>s.living.plan.kind='practice',s=>s.living.plan.target='other-copy',s=>s.living.plan.location='Elsewhere',s=>s.duck.stage='hatchling',s=>s.duck.identity='new-egg',s=>s.duck.x+=.01,s=>s.duck.y+=.01,s=>s.duck.facing=false,s=>s.visitor.id='new-visitor',s=>s.living.plan.carnival_work.egg_caregiver=false,s=>s.living.plan.carnival_work.shared_physical=false,s=>s.living.plan.carnival_work.physical_pilot=true,s=>delete s.living.plan.carnival_work.shared,s=>s.living.plan.carnival_work.shared.observer={},s=>s.living.plan.carnival_work.shared.recipient.phase='approach']){
  const s=eggCaregiverFixture();change(s);assert.equal(eggCaregiverScene(s),null);assert.deepEqual(carnivalOccupants(s),[]);
 }
});
test('published native caregiver binds its exact castle while the egg keeps its separate stationary root',()=>{
 const s=structuredClone(NATIVE_CONTACT),before=JSON.stringify(s),w=s.living.plan.carnival_work;
 assert.deepEqual(s.living.plan.destination,w.shared.destination);assert.notDeepEqual(s.living.plan.destination,w.physical.center);assert.notDeepEqual(s.living.plan.destination,w.shared.recipient.root);
 const {home,result,sx,sy}=render(s,900,1100,1.7);assert.equal(home.instance,s.living.plan.instance);assert.deepEqual(home.worldPosition,w.physical.center);assert.equal(home.carnivalRiders.length,1);assert(result.characters.some(c=>c.cheese));
 const g=castleGeometry(home,home.carnivalRiders[0],sx,sy);assert(g.tip&&g.reachable);near(g.tip.x,g.target.x);near(g.tip.y,g.target.y);assert.equal(JSON.stringify(s),before);
 s.living.plan.destination=[...w.shared.recipient.root];assert.deepEqual(carnivalOccupants(s),[]);s.living.plan.destination=[...w.shared.destination];s.living.plan.instance='different-copy';assert.deepEqual(carnivalOccupants(s),[]);
});
