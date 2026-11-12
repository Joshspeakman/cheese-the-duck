import test from 'node:test';
import assert from 'node:assert/strict';
import {COSTUME_ATTACHMENTS,fittedCostumeAttachment} from '../client/costume-attachments.mjs';
import {fitWearables,wornItems} from '../client/wearables.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {STAGES,ACTIONS} from '../client/scruffy-sprites.mjs';
import {mirror} from '../client/ultra-art.mjs';
const ids=Object.keys(COSTUME_ATTACHMENTS);
test('eight costume constructions remain distinct and use only native equipped IDs',()=>{
 assert.equal(ids.length,8);const rig=characterSprite({stage:'adult',state:'idle'},0).rig,patterns=new Set();
 for(const id of ids){const p=fittedCostumeAttachment(rig,id);patterns.add(p.back.art.join('\n'));assert(p.back.art.some(r=>r.trim()));assert(p.front.art.every(r=>!r.trim()));assert(!p.back.clipped);assert(COSTUME_ATTACHMENTS[id].motion);}
 assert.equal(patterns.size,8);assert.deepEqual(wornItems({invented:'flight_engine'}),[]);
 for(const id of ids)assert.deepEqual(characterSprite({stage:'egg',cosmetics:{item:id}},0).wearables,[]);
});
test('costume pieces stay fitted and leave all existing feather, face and feet ink intact across ages, actions and directions',()=>{
 for(const {id:stage}of STAGES.slice(1))for(const {id:state}of ACTIONS)for(const id of ids)for(const time of [0,.45,1.1]){
  const input={stage,state,facing:true,cosmetics:{item:id}},before=JSON.stringify(input),bare=characterSprite({stage,state,facing:true},time),worn=characterSprite(input,time),piece=fittedCostumeAttachment(bare.rig,id,{phase:time});
  assert(!worn.clipped&& !piece.back.clipped,`${id}/${stage}/${state}/${time} clipped`);assert(worn.art.every(r=>/^[ -~]*$/.test(r)));assert.equal(worn.scale,bare.scale);assert.equal(JSON.stringify(input),before);
  for(let y=0;y<bare.art.length;y++)for(let x=0;x<bare.art[y].length;x++)if(bare.art[y][x]!==' ')assert.equal(worn.art[y][x],bare.art[y][x],`${id} overwrites natural ink ${stage}/${state} at${x},${y}`);
  const left=characterSprite({...input,facing:false},time);assert.deepEqual(left.art,mirror(worn.art));assert.deepEqual(left.tones,worn.tones.map(r=>[...r].reverse().join('')));
  assert(worn.wearables.includes(id));
 }
});
test('tip and rim motion preserves fitted anchors and Reduced Motion fixes costume geometry',()=>{
 for(const {id:stage}of STAGES.slice(1))for(const state of ['idle','walking'])for(const id of ids){
  const rig=characterSprite({stage,state},0).rig,frames=new Set(),anchors=new Set();
  for(const time of [0,.5,1,1.5,2]){const p=fittedCostumeAttachment(rig,id,{phase:time});frames.add(p.back.art.join('\n'));anchors.add(JSON.stringify(p.contacts));}
  assert(frames.size>1,id+' static '+stage+'/'+state);assert.equal(anchors.size,1,id+' detached anchor');
  const still={...rig,motion:false};assert.deepEqual(fittedCostumeAttachment(still,id,{phase:0}),fittedCostumeAttachment(still,id,{phase:100}));
  assert.deepEqual(fitWearables(still,{item:id},0).layers,fitWearables(still,{item:id},100).layers);
 }
});
test('combined native wardrobe keeps costume and existing held pieces selected without granting capabilities',()=>{
 for(const {id:stage}of STAGES.slice(1))for(const id of ids){
  const cosmetics={wings:id,head:'hat_red',neck:'scarf_red',body:'winter_puffy_coat',feet:'rain_boots',held:'magic_wand'},input={stage,state:'walking',cosmetics,motion:false},before=JSON.stringify(input),c=characterSprite(input,.5);
  assert(!c.clipped,id+'/'+stage);assert(c.wearables.includes(id));assert(c.wearables.includes('magic_wand'));assert.equal(c.action,'walking');assert.equal(JSON.stringify(input),before);
 }
});
