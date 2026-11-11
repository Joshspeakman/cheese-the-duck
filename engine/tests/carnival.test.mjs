import test from 'node:test';import assert from 'node:assert/strict';
import {CARNIVAL_ROUTINES,boarding,carnivalPose,carnivalGeometry} from '../client/carnival-routines.mjs';
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';import {GUEST_CAST} from '../client/guest-cast.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';import {scene} from './scenes.mjs';
const ages=['hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'];
const actors=[...ages.map(stage=>({stage})),...Object.values(GUEST_CAST).map(g=>({id:g.id,castId:g.id,name:g.name,visitor:true}))];
function routine(id,f=.5){return {id,stage:'ride',clock:f*CARNIVAL_ROUTINES[id].duration,ride_elapsed:f*CARNIVAL_ROUTINES[id].duration,seat_a:0,seat_b:3,paired:true};}
test('twelve separate carnival scores contain distinct two-way acting and finite poses',()=>{
 assert.equal(Object.keys(CARNIVAL_ROUTINES).length,12);const a=new Set(),b=new Set();
 for(const [id,s]of Object.entries(CARNIVAL_ROUTINES)){
  a.add(JSON.stringify(s.a));b.add(JSON.stringify(s.b));assert.notDeepEqual(s.a,s.b,id+' partner has a reply');
  for(const role of ['a','b'])for(let n=0;n<=100;n++){
   const w=routine(id,n/100),pose=carnivalPose(w,role);assert(['x','y','b','w','l','r'].every(k=>Number.isFinite(pose[k])));assert(pose.seated);
   assert.equal(boarding(w,role),1);assert(carnivalPose(w,role,false).seated);
  }
 }
 assert.equal(a.size,12);assert.equal(b.size,12);
});
test('every hatched age and all visitors preserve body scale and contact a real seat',()=>{
 for(const actor of actors)for(const [id,s]of Object.entries(CARNIVAL_ROUTINES))for(const f of [.1,.35,.6,.9])for(const role of ['a','b']){
  const work=routine(id,f),home={...itemSprite(s.item,0,{state:{excursion:{phase:f*Math.PI*2}}}),x:100,y:80,scale:itemWorldScale(s.item)};
  const watch=actor.id==='butterfly_fairy';const c={...characterSprite({...actor,facing:role==='a',state:'idle',performance:{kind:'carnival',routine:work,role,watch}},0,actor.visitor),x:120,y:80};
  const before=JSON.stringify({home,c}),g=carnivalGeometry(home,{character:c,work,role,watch},6,9);
  assert(!c.clipped,(actor.id||actor.stage)+' '+id);assert(c.art.every(r=>/^[ -~]*$/.test(r)));assert.equal(g.character.scale,c.scale,'never shrink the body to fit');
  assert.equal(JSON.stringify({home,c}),before,'projection cannot advance the mechanism');
  assert(Number.isFinite(g.character.x+g.character.y));
  if(watch){assert.equal(g.inside,0);assert.equal(g.front,null);continue;}
  const actual=g.character.y*9-(c.groundRow-(c.seatContact??c.groundRow))*c.scale*6*1.5+(c.offsetY||0)*c.scale*6;
  assert(Math.abs(actual-g.seatPixel.y)<1e-6,'belly on seat '+(actor.id||actor.stage)+' '+id);
  if(s.item==='ferris_wheel')assert(g.bodyWidth<=g.seatWidth+.001,'roomy cabin fits '+(actor.id||actor.stage)+' '+g.bodyWidth+'/'+g.seatWidth);
 }
});
test('boarding paths reach the stationary seat and reverse for disembarking',()=>{
 for(const id of ['wheel_first','carousel_first'])for(const role of ['a','b']){
  const item=CARNIVAL_ROUTINES[id].item,home={...itemSprite(item,0,{state:{excursion:{phase:Math.PI/2}}}),x:100,y:80,scale:itemWorldScale(item)};
  const c={...characterSprite({stage:'adult',state:'idle'},0),x:122,y:80};
  for(let n=0;n<=60;n++){
   const a={...routine(id),stage:'board_'+role,clock:n/10},b={...a,stage:'unload_'+role,clock:6-n/10};
   const p=carnivalGeometry(home,{character:c,work:a,role},6,9),q=carnivalGeometry(home,{character:c,work:b,role},6,9);
   assert(Math.abs(p.character.x-q.character.x)<1e-8&&Math.abs(p.character.y-q.character.y)<1e-8);
  }
 }
});
test('real world uses the exact copy, retains a paused pose and never duplicates the guest',()=>{
 const work={...routine('wheel_clouds'),companion:{actor:'friend:frida',ready:false,mode:'ride'}};
 const s=scene({items:[{id:'ferris_wheel',instance:'a',x:50,y:28},{id:'ferris_wheel',instance:'b',x:100,y:28}],visitor:{id:'friend:frida',castId:'friend:frida',name:'Frida',x:75,y:28,state:'idle'},living:{ecology:{},objects:{},instances:{a:{excursion:{phase:2}},b:{excursion:{phase:.2}}},plan:{kind:'item',target:'ferris_wheel',instance:'a',phase:'act',progress:.5,elapsed:10,duration:20,destination:[50,28],carnival_work:work}}});
 const w=new LivingWorld();w.render(s,0,.1);assert.equal(w.objects[0].carnivalRiders.length,1);assert(w.characters.some(c=>c.id==='friend:frida'));assert(!w.objects[1].carnivalRiders);
 work.companion.ready=true;s.living.plan.paused=true;w.render(s,10,.1);const art=w.objects[0].carnivalRiders.map(r=>r.character.art);assert.equal(art.length,2);assert(!w.characters.some(c=>c.id==='friend:frida'));
 w.render(s,900,.1);assert.deepEqual(w.objects[0].carnivalRiders.map(r=>r.character.art),art);
 s.items[0].instance='replacement';w.render(s,901,.1);assert(!w.objects[0].carnivalRiders);assert(w.characters.some(c=>c.id==='friend:frida'));
});
