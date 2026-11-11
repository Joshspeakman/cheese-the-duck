import test from 'node:test';
import assert from 'node:assert/strict';
import {catalog,itemSprite} from '../client/ultra-items.mjs';
import {EVENT_CATALOG,EVENT_ASSETS,eventModel} from '../client/event-art.mjs';
import {WILDLIFE} from '../client/wildlife.mjs';
import {DUCK_AGES,duckRig} from '../client/duck-rig.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
import {scene} from './scenes.mjs';
test('all items have an operating animation, physical weather state and immutable input',()=>{
 for(const item of catalog){
  const state={condition:.3,dirt:.8,wetness:.8,bond:.8},before=JSON.stringify(state);
  const frames=new Set([.05,.23,.45,.7,1.05].map(time=>itemSprite(item.id,time,{state,interaction:{phase:'act',progress:time%1}}).art.join('\n')));
  assert(frames.size>1,item.id+' operation must visibly animate');
  assert.notDeepEqual(itemSprite(item.id,0).art,itemSprite(item.id,0,{state}).art,item.id+' shows wear');
  assert.deepEqual(itemSprite(item.id,1,{motion:false,state,interaction:{progress:.5}}),itemSprite(item.id,40,{motion:false,state,interaction:{progress:.5}}));
  assert.equal(JSON.stringify(state),before);
 }
});
test('all event recipes and 131 original assets have printable bounded renderings',()=>{
 assert.equal(Object.keys(EVENT_ASSETS).length,131);assert(Object.keys(EVENT_CATALOG).length>700);assert(Object.keys(WILDLIFE).length>=59);
 for(const [id,e] of Object.entries(EVENT_CATALOG))for(const time of [0,.6,1.4]){
  const m=eventModel({id,family:e.animator,art:e.original},time);assert(m.art.length>0,id);assert(m.art.every((r,y)=>/^[ -~]*$/.test(r)&&r.length===m.tones[y].length),id);
 }
});
test('approved D10 keeps its nine silhouettes, footprint, visible eye and palette',()=>{
 for(const spec of DUCK_AGES){const m=duckRig({stage:spec.id},0);assert(m.fills.length);assert.equal(m.design,'d10');if(m.rig){const e=m.rig.eye;assert.equal(m.art[e.y][e.x],e.char);assert.equal(m.inks.b,spec.tints?.[0]||'#cba27c');}assert(m.scale*spec.art.length*7.5<90);}
});
test('events, story actors and project art travel with camera and respect reduced motion',()=>{
 const s=scene({events:[{id:'butterfly',family:'ButterflyAnimator',art:['<o>'],x:80,y:16,particles:[]}],living:{ecology:{},projects:[],garden:[],story:{id:'lost_duckling',asset:'baby_duck'}}});
 const w=new LivingWorld(),a=w.render(s,1,.03).characters;
 assert.equal(a.filter(x=>x.event).length,2);
 const b=w.render({...s,camera:{...s.camera,x:10}},1,.03).characters;assert.notEqual(a[0].x,b[0].x);
 assert.deepEqual(w.render({...s,motion:false},1,.03).characters,w.render({...s,motion:false},50,.03).characters);
});
