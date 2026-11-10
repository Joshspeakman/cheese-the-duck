import test from 'node:test';
import assert from 'node:assert/strict';
import {GUEST_CAST,guestProfile,visitorRig} from '../client/visitor-rig.mjs';
import {mirrorGlyph} from '../client/duck-rig.mjs';
import {WEARABLE_CATALOG} from '../client/wearable-catalog.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
import {scene} from './scenes.mjs';
const cast=Object.values(GUEST_CAST);
test('all 48 named guests have distinct silhouettes, belongings and voices',()=>{
 assert.equal(cast.length,48);assert.equal(cast.filter(p=>p.rare).length,8);
 const shapes=new Set(),greetings=new Set();
 for(const p of cast){
  const m=visitorRig({id:p.id,state:'walking'},0);
  shapes.add(m.art.map(r=>r.replace(/[^ ]/g,'#')).join('\n'));
  greetings.add(p.voice.greeting);
  for(const gear of p.gear)assert(WEARABLE_CATALOG[gear],p.name+': '+gear);
  assert.equal(Object.keys(p.voice).length,9);assert(p.bio&&p.habit);
  assert.equal(guestProfile({name:p.name}).id,p.id);
 }
 assert.equal(shapes.size,48);assert.equal(greetings.size,48);
 assert.notEqual(guestProfile({name:'Marco'}).id,guestProfile({id:'traveling_merchant'}).id);
});
test('every guest animates, mirrors exactly and stays within the glyph canvas',()=>{
 for(const p of cast){
  const input={id:p.id,name:p.name},before=JSON.stringify(input),signatures=new Set();
  for(const state of ['idle','signature','walking','quacking','sleeping','giving_gift'])for(let i=0;i<24;i++){
   const right=visitorRig({...input,state,facing:true},i*.19),left=visitorRig({...input,state,facing:false},i*.19);
   assert(!right.clipped&&!left.clipped,p.name+' '+state+' '+i);
   assert(right.art.every((r,y)=>/^[ -~]{76}$/.test(r)&&r.length===right.tones[y].length),p.name);
   assert.deepEqual(left.art,right.art.map(r=>[...r].reverse().map(mirrorGlyph).join('')));
   assert.equal(right.profileId,p.id);
   if(state==='signature')signatures.add(right.art.join('\n'));
  }
  assert(signatures.size>=3,p.name+' signature gesture');assert.equal(JSON.stringify(input),before);
 }
});
test('all rare guests use their full character rigs at simulation coordinates',()=>{
 const world=new LivingWorld();
 for(const p of cast.filter(p=>p.rare)){
  const s=scene({rareVisitor:{id:p.id,name:p.name,x:83,y:22,state:'walking'},motion:false});
  const before=JSON.stringify(s),a=world.render(s,1).characters.find(c=>c.id===p.id);
  assert(a&&a.visitor&&!a.event,p.id);assert.equal(a.design,'pond-cast');
  assert.deepEqual([a.x,a.y],world.project(s,83,22));
  assert.deepEqual(world.render(s,1).characters,world.render(s,50).characters);
  assert.equal(JSON.stringify(s),before);
 }
});
