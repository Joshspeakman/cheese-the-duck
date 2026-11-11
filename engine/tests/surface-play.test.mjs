import test from 'node:test';import assert from 'node:assert/strict';
import {SURFACE_ROUTINES as scores,surfaceControls,surfaceInside} from '../client/surface-routines.mjs';
import {carnivalPose,carnivalGeometry,CARNIVAL_CHOICES} from '../client/carnival-routines.mjs';
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';import {GUEST_CAST} from '../client/guest-cast.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';import {scene} from './scenes.mjs';
const ages=['hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'];
const actors=[...ages.map(stage=>({stage})),...Object.values(GUEST_CAST).map(g=>({id:g.id,castId:g.id,name:g.name,visitor:true}))];
const work=(id,t)=>({id,stage:'play',clock:t,ride_elapsed:t,factors:{a:.5,b:.75},paired:true});
function home(id,w){return {...itemSprite(id,0,{state:{excursion:{inflation:1,cover:0,surface:{...surfaceControls(w),gate:1,active:true}}}}),x:100,y:80,scale:itemWorldScale(id)};}
test('28 authored spring-floor and carpet programs have distinct two-person acting and physically brief flights',()=>{
 assert.equal(Object.keys(scores).length,28);assert.equal(CARNIVAL_CHOICES.bounce_house.length,14);assert.equal(CARNIVAL_CHOICES.magic_carpet.length,14);
 for(const item of ['bounce_house','magic_carpet']){
  const a=new Set(),b=new Set();
  for(const [id,s]of Object.entries(scores).filter(([,s])=>s.item===item)){
   a.add(JSON.stringify([s.a,s.leaps.a,s.deck]));b.add(JSON.stringify([s.b,s.leaps.b,s.deck]));assert.notDeepEqual(s.a,s.b,id+' has an answer');
   for(const role of ['a','b']){
    let previous=-1;for(const [start,end,height]of s.leaps[role]){assert(start>previous&&end>start&&end<1);assert(height>0&&height<=18);assert((end-start)*s.duration<1.5,'flight stays brief');previous=end;}
    for(let n=0;n<=100;n++){
     const w=work(id,s.duration*n/100),v=surfaceControls(w),p=carnivalPose(w,role);
     assert(['x','y','b','w','l','r'].every(k=>Number.isFinite(p[k])));assert(v[role].jump>=0&&v[role].jump<=18);assert(v.lift>=0&&v.lift<=18);assert(Math.abs(v.tilt)<=.65);
     assert.equal(surfaceInside(w,role),1);
    }
   }
  }
  assert.equal(a.size,14);assert.equal(b.size,14);
 }
});
test('each real age and visitor keeps body scale and contacts a moving surface or the exact native jump height',()=>{
 for(const actor of actors)for(const id of ['bounce_first','bounce_quiet','bounce_together','carpet_first','carpet_banks','carpet_climb'])for(const role of ['a','b']){
  const s=scores[id],leap=s.leaps[role][0],t=leap?leap[0]*s.duration+(leap[1]-leap[0])*s.duration*Math.sqrt(role==='a'?.5:.75)/2:s.duration*.45,w=work(id,t),h=home(s.item,w),watch=actor.id==='butterfly_fairy';
  const c={...characterSprite({...actor,facing:role==='a',state:'idle',performance:{kind:'carnival',routine:w,role,watch}},0,actor.visitor),x:122,y:80};
  const before=JSON.stringify({h,c}),g=carnivalGeometry(h,{character:c,work:w,role,watch},6,9);
  assert(!c.clipped,(actor.id||actor.stage)+' '+id);assert(c.art.every(r=>/^[ -~]*$/.test(r)));assert.equal(g.character.scale,c.scale);assert.equal(JSON.stringify({h,c}),before);
  if(watch){assert.equal(g.inside,0);continue;}
  const contact=g.character.y*9-(c.groundRow-(c.seatContact??c.groundRow))*c.scale*6*1.5*g.seated+(c.offsetY||0)*c.scale*6;
  assert(Math.abs(contact-(g.seatPixel.y-g.jumpPixels))<1e-7,(actor.id||actor.stage)+' native contact '+id);
  assert.equal(g.jumpPixels,h.surfaceState[role].jump*6*h.scale*h.detailScale*1.5);
  assert(h.anchors.slots[0].x<h.anchors.slots[1].x,'independent floor lanes');
 }
});
test('landings compress nearby ribs, carpet elevation and tilt move both seating anchors, and all geometry stays bounded',()=>{
 for(const id of ['bounce_house','magic_carpet']){
  for(const corrupt of [null,'bad',[],{a:null,b:{jump:Infinity,press:NaN},lift:Infinity,tilt:-999}]){
   const m=itemSprite(id,0,{state:{excursion:{surface:corrupt}}});assert(!m.clipped);assert(m.anchors.slots.every(s=>Number.isFinite(s.x+s.y)));
  }
  const idle=itemSprite(id,0,{state:{excursion:{surface:{}}}});
  for(let n=0;n<100;n++){
   const state={excursion:{phase:0,wind_phase:0,wind:.2,inflation:.35+n/100*.65,cover:n/100,surface:{a:{jump:18,press:n/100,u:Math.sin(n),v:Math.cos(n),impact:n/100},b:{jump:8,press:1-n/100,u:-Math.sin(n),v:-Math.cos(n)},lift:n/100*18,tilt:Math.sin(n)*.65,gate:n/100}}},a=itemSprite(id,0,{state});
   assert(!a.clipped,id+' bounded at '+n);assert(a.art.every(r=>/^[ -~]*$/.test(r)));assert(a.fills.every(f=>f.x>=0&&f.y>=0&&f.x+f.w<=a.width&&f.y<a.art.length));
   assert.deepEqual(a,itemSprite(id,900,{state}),'native state prevents renderer clock drift');
  }
  const press=itemSprite(id,0,{state:{excursion:{surface:{a:{press:1}}}}});
  assert(press.anchors.slots[0].y>idle.anchors.slots[0].y+.5,'real local compression');
  assert(press.anchors.slots[1].y-idle.anchors.slots[1].y<.02,'other lane does not bounce from a distant footprint');
  const up=itemSprite(id,0,{state:{excursion:{surface:{lift:18,tilt:.6}}}});
  if(id==='magic_carpet')assert(up.anchors.slots.every((s,i)=>s.y<idle.anchors.slots[i].y-15));
 }
});
test('entry and exit use reversible paths, spectators stay out, and reduced motion preserves physical height',()=>{
 const leap=scores.bounce_together.leaps.b[0],length=(leap[1]-leap[0])*scores.bounce_together.duration*Math.sqrt(.75);
 const observer=work('bounce_together',leap[0]*scores.bounce_together.duration+length/2),pose=carnivalPose(observer,'b',true,true);
 assert(surfaceControls(observer).b.jump>1);assert.equal(pose.l,0);assert.equal(pose.r,0);assert.equal(pose.seated,false,'watchers never adopt a rider jump or seat');
 for(const id of ['bounce_first','carpet_climb'])for(const role of ['a','b']){
  const s=scores[id],w=work(id,s.duration*.4),h=home(s.item,w),c={...characterSprite({stage:'adult',state:'idle'},0),x:122,y:80};
  for(let n=0;n<=40;n++){
   const a={...w,stage:'board_'+role,clock:n/10},b={...w,stage:'unload_'+role,clock:4-n/10};
   const p=carnivalGeometry(h,{character:c,work:a,role},6,9),q=carnivalGeometry(h,{character:c,work:b,role},6,9);
   assert(Math.abs(p.character.x-q.character.x)<1e-8&&Math.abs(p.character.y-q.character.y)<1e-8);
  }
  const quiet={...characterSprite({stage:'adult',state:'idle',performance:{kind:'carnival',routine:w,role}},0,false,false),x:122,y:80};
  const g=carnivalGeometry(h,{character:quiet,work:w,role},6,9);assert.equal(g.jumpPixels,h.surfaceState[role].jump*6*h.scale*h.detailScale*1.5);
 }
});
test('live world binds two performers to one exact carpet and freezes gestures while paused',()=>{
 const w=work('carpet_banks',21);w.companion={actor:'friend:frida',ready:true,mode:'ride'};
 const surface={...surfaceControls(w),gate:1,active:true};
 const s=scene({items:[{id:'magic_carpet',instance:'a',x:50,y:28},{id:'magic_carpet',instance:'b',x:100,y:28}],visitor:{id:'friend:frida',castId:'friend:frida',name:'Frida',x:75,y:28,state:'idle'},living:{ecology:{},objects:{},instances:{a:{excursion:{surface}},b:{excursion:{surface:{}}}},plan:{kind:'item',target:'magic_carpet',instance:'a',phase:'act',progress:.5,elapsed:10,duration:20,destination:[50,28],paused:true,carnival_work:w}}});
 const world=new LivingWorld();world.render(s,0,.1);const h=world.objects.find(o=>o.instance==='a'),art=h.carnivalRiders.map(r=>r.character.art);
 assert.equal(art.length,2);assert(!world.characters.some(c=>c.id==='friend:frida'));assert(!world.objects.find(o=>o.instance==='b').carnivalRiders);
 world.render(s,900,.1);assert.deepEqual(world.objects.find(o=>o.instance==='a').carnivalRiders.map(r=>r.character.art),art);
 s.items[0].instance='new';world.render(s,901,.1);assert(!world.objects.find(o=>o.instance==='new').carnivalRiders);assert(world.characters.some(c=>c.id==='friend:frida'));
});
