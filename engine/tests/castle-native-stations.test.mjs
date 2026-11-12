import test from 'node:test';
import assert from 'node:assert/strict';
import {CASTLE_SCORES,castlePose,castleStation,castleGeometry} from '../client/castle-care.mjs';
import {castleArtWorld,projectCastleWorld} from '../client/castle-projection.mjs';
import {displayCamera} from '../client/actor-projection.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
import {scene} from './scenes.mjs';
import METRICS from '../client/animation/castle-contact-metrics.json' with {type:'json'};
const ids=['castle_door_open','castle_hose_stow'],origin=[63,25];
const close=(a,b)=>assert.ok(Math.abs(a-b)<1e-8,`${a} != ${b}`);
function work(id,at,station,phase='hold'){
 return {id,physical_pilot:true,stage:'service',clock:at*CASTLE_SCORES[id].duration,ride_elapsed:at*CASTLE_SCORES[id].duration,physical:{version:1,actor:'cheese',station,phase,root:[65,25],target:[70,24],contact_ready:true}};
}
test('native arrival selects the authoritative station without a second renderer walk',()=>{
 for(const id of ids){
  const [at,station]=CASTLE_SCORES[id].stations[1],w=work(id,at,station),before=JSON.stringify(w);
  assert.deepEqual(castleStation(w),{name:station,previous:station,travel:1});
  const pose=castlePose(w);assert.equal(pose.l,0);assert.equal(pose.r,0);assert.equal(pose.contact,1);
  // Native station remains authoritative even while the paused score clock is
  // exactly at, or slightly before, its scheduled transfer threshold.
  w.ride_elapsed-=.001;assert.equal(castlePose(w).station,station);
  w.ride_elapsed+=.001;assert.equal(JSON.stringify(w),before);
 }
});
test('all eight hatched ages use their actual effect metrics and only native hold can draw contact',()=>{
 for(const [stage,age]of Object.entries(METRICS.ages))for(const id of Object.keys(age.routines))for(const metric of age.routines[id])for(const [width,height]of [[1440,900],[1800,800],[800,1200]])for(const motion of [true,false]){
  const sx=width/240,sy=height/112,camera=displayCamera({x:10,y:2,w:107,h:38},sx,sy),physicalCastle={origin,camera};
  const at=projectCastleWorld(physicalCastle,origin),home={...itemSprite('bounce_house',0),...at,scale:itemWorldScale('bounce_house'),physicalCastle};
  const anchor=home.anchors.controls[metric.station],target=castleArtWorld(origin,anchor.x,anchor.y,{center:true});
  const w=work(id,metric.at,metric.station);w.physical.source_age=stage;w.physical.target=target;
  w.physical.root=[target[0]-metric.grip[0]*metric.scale*132/192,target[1]-metric.grip[1]*metric.scale*42/47];
  const character={...characterSprite({stage,state:'idle',facing:true,performance:{kind:'carnival',routine:w,role:'a',motion}},0),x:0,y:0,physicalCastleActor:physicalCastle};
  close(character.grip.x+.5-character.anchorX,metric.grip[0]);close(character.grip.y+.5-character.groundRow,metric.grip[1]);
  const expected=projectCastleWorld(physicalCastle,w.physical.root,sx,sy),pixel=projectCastleWorld(physicalCastle,target,sx,sy),before=JSON.stringify(w);
  const g=castleGeometry(home,{character,work:w,role:'a'},sx,sy);
  close(g.character.x*sx,expected.x);close(g.character.y*sy,expected.y);close(g.tip.x,pixel.x);close(g.tip.y,pixel.y);assert.equal(JSON.stringify(w),before);
  for(const phase of ['approach','exit']){const moving=castleGeometry(home,{character,work:{...w,physical:{...w.physical,phase}},role:'a'},sx,sy);assert.equal(moving.points.length,0);close(moving.character.x*sx,expected.x);close(moving.character.y*sy,expected.y);}
  const waiting=castleGeometry(home,{character,work:{...w,physical:{...w.physical,contact_ready:false}},role:'a'},sx,sy);assert.equal(waiting.points.length,0);
 }
});
test('native transfer and exit retain actual walking art, arrival restores the contact performance',()=>{
 for(const stage of Object.keys(METRICS.ages))for(const id of ids)for(const phase of ['approach','hold','exit']){
  const [at,station]=CASTLE_SCORES[id].stations[1],w=work(id,at,station,phase),world=new LivingWorld();
  const s=scene({duck:{x:65,y:25,stage,state:'walking',facing:false},items:[{id:'bounce_house',x:origin[0],y:origin[1],instance:'native-stations'}],living:{objects:{},ecology:{},plan:{kind:'item',target:'bounce_house',instance:'native-stations',phase:'act',destination:origin,carnival_work:w}}});
  const member=world.render(s,.5,.1).objects.find(o=>o.id==='bounce_house').carnivalRiders[0];
  if(phase==='hold'){assert.equal(member.character.performance.kind,'carnival');assert.equal(castlePose(w).travel,1);}
  else {assert.equal(member.character.performance,null);assert.equal(member.character.action,'walking');}
 }
});
