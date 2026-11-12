import test from 'node:test';
import assert from 'node:assert/strict';
import {exportCastleGuestMetrics,REGULAR_CAST_IDS,SHARED_CAST_IDS} from '../scripts/export-castle-guest-metrics.mjs';
import METRICS from '../client/animation/castle-guest-metrics.json' with {type:'json'};
import {DUCK_AGES} from '../client/duck-designs.mjs';
import {GUEST_CAST} from '../client/guest-cast.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
import {castleGeometry,castlePose,sharedCastleRecord} from '../client/castle-care.mjs';
import {carnivalOccupants} from '../client/carnival-routines.mjs';
import {displayCamera,actorPitches} from '../client/actor-projection.mjs';
import {projectCastleWorld} from '../client/castle-projection.mjs';
import {sharedCastleFixture} from './castle-shared-fixtures.mjs';
const close=(a,b)=>assert.ok(Math.abs(a-b)<1e-8,`${a} != ${b}`);
function render(s,width=1440,height=900){const sx=width/240,sy=height/112,copy={...s,camera:displayCamera(s.camera,sx,sy)},world=new LivingWorld(),result=world.render(copy,0,0),home=result.objects.find(o=>o.id==='bounce_house');return {world,result,home,sx,sy,members:home.carnivalRiders||[]};}
test('43 exact guest exports and 8 actual observer supports match live rigs with no fallback',()=>{
 assert.equal(REGULAR_CAST_IDS.length,40);assert.deepEqual(Object.keys(METRICS.casts),SHARED_CAST_IDS);assert.deepEqual(METRICS,exportCastleGuestMetrics());
 assert.equal(Object.keys(METRICS.observers).length,8);assert.equal(METRICS.observers.egg,undefined);assert.equal(METRICS.casts.friend,undefined);assert.equal(METRICS.casts.friendly_goose,undefined);
 assert.equal(Object.values(METRICS.casts).reduce((n,c)=>n+Object.values(c.routines).flat().length,0),387);
 for(const c of Object.values(METRICS.casts))for(const m of Object.values(c.routines).flat()){assert(m.feet.length===2);assert(m.feet.every(f=>f[1]===0));assert(m.scale>0);}
});
test('every regular profile owns exact native contact while Cheese watches at its own root',()=>{
 for(const cast of REGULAR_CAST_IDS)for(const [id,metrics]of Object.entries(METRICS.casts[cast].routines))for(const [index,metric]of metrics.entries())for(const [width,height]of [[1440,900],[1800,800],[800,1200]]){
  const s=sharedCastleFixture(cast,id,index,{motion:index%2===0}),before=JSON.stringify(s),{home,members,sx,sy}=render(s,width,height),w=s.living.plan.carnival_work;
  assert.equal(members.length,2);const operator=members.find(m=>m.role==='a'),observer=members.find(m=>m.watch);assert.equal(operator.actor,s.visitor.id);assert.equal(operator.character.profileId,cast);assert.equal(observer.actor,'cheese');
  for(const member of members){
   const g=castleGeometry(home,member,sx,sy),root=member.watch?w.shared.cheese.root:w.physical.root,p=projectCastleWorld(home.physicalCastle,root,sx,sy),pitch=actorPitches(member.character,sx,sy);
   assert(g.authoritativeRoot);close(g.character.x*sx,p.x);close(g.character.y*sy,p.y);close(pitch.ch/pitch.cw,1.5);
   if(member.watch){assert.equal(g.points.length,0);assert.equal(g.pose.contact,0);assert.equal(g.pose.surfaceWork,false);assert.equal(member.character.grip,null);}
   else{assert(g.reachable);assert(g.tip);const target=projectCastleWorld(home.physicalCastle,w.physical.target,sx,sy);close(g.tip.x,target.x);close(g.tip.y,target.y);close(member.character.scale,metric.scale);}
  }
  assert.equal(JSON.stringify(s),before);
 }
});
test('both roots and locomotion survive independent arrival, transfer, exit and paused holds',()=>{
 for(const cast of REGULAR_CAST_IDS)for(const phase of ['approach','hold','exit'])for(const cheesePhase of ['approach','hold','exit']){
  const s=sharedCastleFixture(cast,'castle_door_open',1,{phase,cheesePhase,camera:{x:10,y:2,w:107,h:38}});if(phase==='approach')s.living.plan.phase='approach';const {home,members,sx,sy}=render(s),w=s.living.plan.carnival_work;assert.equal(members.length,2);
  for(const member of members){const ownPhase=member.watch?cheesePhase:phase,g=castleGeometry(home,member,sx,sy);if(ownPhase!=='hold'){assert.equal(member.character.performance,null);assert.equal(member.character.action,'walking');assert.equal(g.points.length,0);}if(member.watch||phase!=='hold'||cheesePhase!=='hold')assert.equal(g.points.length,0);}
  s.living.plan.paused=true;const paused=render(s);for(const member of paused.members)assert.equal(castleGeometry(paused.home,member,paused.sx,paused.sy).points.length,0);
  assert(sharedCastleRecord(w));
 }
});
test('malformed or changed identities never substitute Cheese or a fallback guest as operator',()=>{
 const cases=[s=>delete s.living.plan.carnival_work.shared,s=>s.living.plan.carnival_work.shared.operator.cast='unknown',s=>s.visitor.id='replacement',s=>s.visitor.name='Marco impersonator',s=>s.visitor.castId='friend:ada',s=>s.living.plan.carnival_work.physical.actor='cheese',s=>s.duck.stage='egg',s=>s.living.plan.carnival_work.shared.cheese.root=[NaN,4]];
 for(const change of cases){const s=sharedCastleFixture();change(s);assert.deepEqual(carnivalOccupants(s),[]);assert.equal(render(s).members.length,0);}
 const s=sharedCastleFixture();s.visitor.castId='friend:marco';assert.equal(carnivalOccupants(s).length,2);
});
test('observer reaction follows consumed native effects and never becomes material assistance',()=>{
 const s=sharedCastleFixture(),w=s.living.plan.carnival_work;w.events=[];const before=castlePose(w,'b',true,true);assert.equal(before.mark,'');
 w.events=[0];const reaction=castlePose(w,'b',true,true);assert.equal(reaction.mark,'!');assert.equal(reaction.contact,0);assert.equal(reaction.reach,0);assert.equal(reaction.surfaceWork,false);
 w.ride_elapsed+=2;assert.equal(castlePose(w,'b',true,true).mark,'');
});

test('travel support encloses actual mirrored feet and body through all walking phases without mutating fitter coordinates',()=>{
 const subjects=[...SHARED_CAST_IDS.map(cast=>({data:{id:'live',castId:cast,name:GUEST_CAST[cast].name},pace:GUEST_CAST[cast].pace,visitor:true,metric:METRICS.casts[cast].travel})),...DUCK_AGES.filter(a=>a.id!=='egg').map(a=>({data:{stage:a.id},pace:a.pace,visitor:false,metric:METRICS.observers[a.id].travel}))];
 for(const {data,pace,visitor,metric}of subjects)for(const facing of [true,false])for(let phase=0;phase<8;phase++){
  assert.equal(metric.kind,'support-union');const c=characterSprite({...data,state:'walking',facing},(phase+.1)*4.5/(pace*5),visitor),before=JSON.stringify(c.rig.feet);
  for(const foot of c.rig.feet){const expected=[(facing?foot.x:c.width-1-foot.x)+.5-c.anchorX,foot.y+.5-c.groundRow];assert(metric.feet.some(f=>f.every((v,i)=>v===expected[i])),'missing actually drawn mirrored foot');}
  const b=c.rig.body,x=(facing?b.x:c.width-b.x-b.w)-c.anchorX,y=b.y-c.groundRow;
  assert(x>=metric.body.x&&x+b.w<=metric.body.x+metric.body.w);assert(y>=metric.body.y&&y+b.h<=metric.body.y+metric.body.h);assert.equal(JSON.stringify(c.rig.feet),before);
 }
});

test('every hatched Cheese observer retains its own age rig and native root through shared phases',()=>{
 for(const stage of Object.keys(METRICS.observers))for(const phase of ['approach','hold','exit']){
  const s=sharedCastleFixture('friend:ada','castle_hose_stow',2,{stage,phase}),{home,members,sx,sy}=render(s,800,1200),watch=members.find(m=>m.watch),g=castleGeometry(home,watch,sx,sy),expected=projectCastleWorld(home.physicalCastle,s.living.plan.carnival_work.shared.cheese.root,sx,sy);
  assert.equal(watch.character.rig.stage,stage);close(watch.character.scale,METRICS.observers[stage].scale);close(g.character.x*sx,expected.x);close(g.character.y*sy,expected.y);assert.equal(g.points.length,0);assert.equal(watch.character.grip,null);
 }
});
