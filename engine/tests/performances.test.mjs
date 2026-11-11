import test from 'node:test';
import assert from 'node:assert/strict';
import {PERFORMANCES,ITEM_PERFORMANCES} from '../client/performances.mjs';
import {duckRig,DUCK_AGES} from '../client/duck-rig.mjs';
import {visitorRig,GUEST_CAST} from '../client/visitor-rig.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
import {scene} from './scenes.mjs';
test('paired tracks articulate every approved age and all 48 guest identities without clipping',()=>{
 for(const kind of Object.keys(PERFORMANCES))for(const role of ['a','b']){
  for(const age of DUCK_AGES){
   const frames=new Set();
   for(let n=0;n<=20;n++){const m=duckRig({stage:age.id,performance:{kind,role,progress:n/20}},1);assert(!m.clipped,`${age.id} ${kind} ${role} ${n}`);assert.equal(m.design,'d10');frames.add(m.art.join('\n'));}
   if(age.id!=='egg')assert(frames.size>=3,age.id+' '+kind);
  }
  for(const profile of Object.values(GUEST_CAST)){
   const frames=new Set();
   for(let n=0;n<=20;n++){const m=visitorRig({castId:profile.id,performance:{kind,role,progress:n/20}},1);assert(!m.clipped,`${profile.id} ${kind} ${role} ${n}`);assert.equal(m.profileId,profile.id);frames.add(m.art.join('\n'));}
   assert(frames.size>=3,profile.id+' '+kind);
  }
 }
});
test('each paired performance has a distinct rendered movement track, not a renamed clip',()=>{
 for(const role of ['a','b']){
  const tracks=Object.keys(PERFORMANCES).map(kind=>[...Array(21)].map((_,i)=>duckRig({stage:'adult',performance:{kind,role,progress:i/20}},1).art.join('\n')).join('\n---\n'));
  assert.equal(new Set(tracks).size,Object.keys(PERFORMANCES).length);
 }
});
test('item gestures preserve every age silhouette through each articulated track',()=>{
 for(const kind of Object.keys(ITEM_PERFORMANCES))for(const age of DUCK_AGES)for(let n=0;n<=20;n++){
  const m=duckRig({stage:age.id,performance:{kind,progress:n/20}},1);
  assert(!m.clipped,kind+' '+age.id+' '+n);assert.equal(m.design,'d10');
 }
});
test('coordinated performances never move actors in the renderer and freeze under reduced motion',()=>{
 const plan={a:'cheese',b:'friend:test',performance:'duet',phase:'act',elapsed:8,duration:24};
 const s=scene({visitor:{id:'friend:test',castId:'friend:frida',name:'Frida',x:75,y:24},living:{ecology:{},minds:{performances:[plan]}}});
 const w=new LivingWorld();const first=w.render(s,1,.03).characters;
 const second=w.render({...s,living:{...s.living,minds:{performances:[{...plan,elapsed:15}]}}},1,.03).characters;
 assert.deepEqual(first.map(c=>[c.x,c.y]),second.map(c=>[c.x,c.y]));assert.notDeepEqual(first.map(c=>c.art),second.map(c=>c.art));
 assert.deepEqual(w.render({...s,motion:false},1,.03).characters,w.render({...s,motion:false},50,.03).characters);
});
