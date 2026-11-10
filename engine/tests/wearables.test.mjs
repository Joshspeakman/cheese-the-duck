import test from 'node:test';
import assert from 'node:assert/strict';
import {wearableCatalog,wearableSpec,fitWearables,wornItems} from '../client/wearables.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {STAGES,ACTIONS} from '../client/scruffy-sprites.mjs';
import {mirror} from '../client/ultra-art.mjs';

test('all live wearables have fitted art, colors and individual motion descriptions',()=>{
 for(const item of wearableCatalog){const s=wearableSpec(item.id);assert(s,item.id);assert.match(s.color,/^#[0-9a-f]{6}$/);assert(s.motion,item.id);}
 assert.equal(wornItems({old:'hat_red',current:'hat_blue'}).map(i=>i.id).join(','),'hat_blue');
});
test('wearables fit every age and action without clipping or changing input',()=>{
 for(const item of wearableCatalog)for(const {id:stage} of STAGES.slice(1))for(const {id:state} of ACTIONS)for(const time of [0,.45]){
  const duck={stage,state,cosmetics:{item:item.id}},before=JSON.stringify(duck),m=characterSprite(duck,time);
  assert.equal(m.clipped,false,`${item.id}/${stage}/${state}/${time}`);
  assert(m.art.every((row,y)=>row.length===m.tones[y].length&&/^[ -~]*$/.test(row)));
  assert.equal(JSON.stringify(duck),before);
 }
});
test('fitted accessories mirror with the pose and keep independent garment colors',()=>{
 for(const state of ['idle','walking','eating','sleeping','swimming','flapping']){
  const duck={stage:'adult',state,cosmetics:{head:'hat_red',face:'glasses_nerd',neck:'scarf_striped',back:'cape',feet:'rain_boots'}};
  const r=characterSprite(duck,.4),l=characterSprite({...duck,facing:false},.4);
  assert.deepEqual(l.art,mirror(r.art));assert.deepEqual(l.tones,r.tones.map(row=>[...row].reverse().join('')));assert.deepEqual(l.inks,r.inks);
  assert(new Set(Object.values(r.inks)).size>=5);
 }
});
test('head and neck items leave Cheese\'s expression visible at every age',()=>{
 for(const {id:stage} of STAGES.slice(1))for(const state of ['idle','walking','eating','sleeping'])for(const id of ['hat_red','hat_chef','hat_wizard','hat_crown','scarf_red','winter_earmuffs','headphones','bowtie','backpack_tiny']){
  const m=characterSprite({stage,state,cosmetics:{item:id}},.4),e=m.rig.eye;
  assert.equal(m.art[e.y][e.x],e.char,`${id} obscures ${stage}'s eye during ${state}`);
 }
});
test('cloth, wings, hats and held objects animate while their attachment stays on the posed rig',()=>{
 const rig=characterSprite({stage:'adult',state:'idle'},0).rig;
 for(const id of ['hat_party','hat_chef','hat_wizard','hat_beanie','scarf_red','cape','backpack_tiny','wings_fairy','halo','headphones','umbrella','magic_wand']){
  const frames=new Set(Array.from({length:8},(_,i)=>JSON.stringify(fitWearables(rig,{item:id},i/3).layers)));
  assert(frames.size>1,id+' has no bespoke animation');
 }
 const idle=characterSprite({state:'idle'},0),peck=characterSprite({state:'eating'},.7);
 assert.notDeepEqual(idle.rig.head,peck.rig.head);
 for(const {id:stage} of STAGES.slice(1)){
  const m=characterSprite({stage},0);
  for(const foot of m.rig.feet)assert(foot.y-(m.rig.body.y+m.rig.body.h-1)<=1,stage+' legs are too long');
 }
});
