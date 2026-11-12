import test from 'node:test';
import assert from 'node:assert/strict';
import FLIGHT from '../client/animation/castle-flight-metrics.json' with {type:'json'};
import METRICS from '../client/animation/castle-contact-metrics.json' with {type:'json'};
import {exportCastleFlightMetrics,flightInkBounds,flightWork} from '../scripts/export-castle-flight-metrics.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
import {displayCamera,actorPitches} from '../client/actor-projection.mjs';
import {projectCastleWorld} from '../client/castle-projection.mjs';
import {castleGeometry,castlePose} from '../client/castle-care.mjs';
import {carnivalOccupants} from '../client/carnival-routines.mjs';
import {flightFixture} from './castle-flight-fixtures.mjs';
const close=(a,b)=>assert(Math.abs(a-b)<1e-8,`${a} != ${b}`);
function render(s,width=1200,height=800,time=0){const sx=width/240,sy=height/112,world=new LivingWorld(),r=world.render({...s,camera:displayCamera(s.camera,sx,sy)},time,.1),home=r.objects.find(o=>o.id==='bounce_house');return {r,home,sx,sy,members:home.carnivalRiders||[]};}
test('Flutter envelope reproduces actual art and encloses independent flight times with no invented ground anatomy',()=>{
 assert.deepEqual(FLIGHT,exportCastleFlightMetrics());assert.equal(FLIGHT.feet,undefined);assert.equal(FLIGHT.grip,undefined);
 for(const facing of [true,false])for(let i=0;i<800;i++)for(const react of [false,true]){
  const c=characterSprite({castId:'butterfly_fairy',facing,performance:{kind:'carnival',routine:flightWork('castle_start',0,react),role:'b',watch:true}},i*.173,true),b=flightInkBounds(c),u=FLIGHT.body;
  assert(b.x>=u.x&&b.x+b.w<=u.x+u.w&&b.y>=u.y&&b.y+b.h<=u.y+u.h);assert.equal(c.grip,null);assert.deepEqual(c.rig.feet,[]);assert.equal(c.scale,FLIGHT.scale);
 }
});
test('all eight Cheese ages operate every authored effect while Flutter keeps its own airborne native root',()=>{
 for(const stage of Object.keys(METRICS.ages))for(const [id,metrics]of Object.entries(METRICS.ages[stage].routines))for(const [index,metric]of metrics.entries())for(const [width,height]of [[1200,800],[1800,800],[900,1100]])for(const motion of [true,false]){
  const s=flightFixture(stage,id,index,{motion}),before=JSON.stringify(s),{home,members,sx,sy}=render(s,width,height,1.23),w=s.living.plan.carnival_work;assert.equal(members.length,2);
  const op=members.find(m=>m.role==='a'),watch=members.find(m=>m.watch);assert.equal(op.actor,'cheese');assert.equal(op.character.rig.stage,stage);assert.equal(op.character.scale,metric.scale);assert.equal(watch.character.profileId,'butterfly_fairy');
  for(const m of members){const g=castleGeometry(home,m,sx,sy),p=projectCastleWorld(home.physicalCastle,m.watch?w.shared.observer_physical.root:w.physical.root,sx,sy),pitch=actorPitches(m.character,sx,sy);assert(g.authoritativeRoot);close(g.character.x*sx,p.x);close(g.character.y*sy,p.y);close(pitch.ch/pitch.cw,1.5);if(m.watch){assert.equal(g.points.length,0);assert.equal(g.pose.contact,0);assert.equal(g.pose.surfaceWork,false);assert.equal(m.character.grip,null);assert.deepEqual(m.character.rig.feet,[]);}else{assert(g.reachable&&g.tip);close(g.tip.x,g.target.x);close(g.tip.y,g.target.y);}}
  assert.equal(JSON.stringify(s),before);
 }
});
test('Flutter attention requires a consumed effect and Reduced Motion freezes flight at its unchanged root',()=>{
 const s=flightFixture('adult','castle_start',0,{react:false}),w=s.living.plan.carnival_work;assert.equal(castlePose(w,'b',true,true).w,0);w.events=[0];assert.equal(castlePose(w,'b',true,true).w,.4);assert.equal(castlePose(w,'b',false,true).w,0);w.ride_elapsed+=2;assert.equal(castlePose(w,'b',true,true).w,0);
 s.motion=false;const a=render(s,1200,800,0).members.find(m=>m.watch).character,b=render(s,1200,800,30).members.find(m=>m.watch).character;assert.deepEqual(a.art,b.art);assert.equal(a.x,b.x);assert.equal(a.y,b.y);
});
test('independent flight phases preserve source motion and malformed identities never reverse roles or fall back',()=>{
 for(const phase of ['approach','hold','exit'])for(const observerPhase of ['approach','hold','exit']){const s=flightFixture('adult','castle_start',0,{phase,observerPhase}),{home,members,sx,sy}=render(s);assert.equal(members.length,2);if(phase!=='hold'||observerPhase!=='hold')for(const m of members)assert.equal(castleGeometry(home,m,sx,sy).points.length,0);}
 for(const change of [s=>s.rareVisitor=null,s=>s.rareVisitor.castId='lost_duckling',s=>s.duck.stage='egg',s=>s.living.plan.carnival_work.flight_observer=false,s=>s.living.plan.carnival_work.shared_physical=false,s=>delete s.living.plan.carnival_work.shared,s=>s.living.plan.carnival_work.physical_pilot=false,s=>s.living.plan.carnival_work.shared.operator.actor='butterfly_fairy',s=>s.living.plan.carnival_work.shared.observer_physical.root=[NaN,0]]){const s=flightFixture();change(s);assert.deepEqual(carnivalOccupants(s),[]);}
});
