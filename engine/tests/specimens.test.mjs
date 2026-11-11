import test from 'node:test';
import assert from 'node:assert/strict';
import {SPECIMEN_BLUEPRINTS as B,specimenSprite} from '../client/specimen-workshop.mjs';
const ids='philosophers_stone glitter_rock crystal sea_glass crystal_shard crystal_icicle mist_crystal ice_crystal crystal_plant ruby_gem star_fragment shiny_pebble shiny_object pebble smooth_stone rock iron_ore clay pond_clay sand seashell shell sea_shell sand_dollar pretty_shell cool_stick digging_stick twig bark driftwood driftwood_large fossil river_pearl'.split(' ');
const sprite=(id,time=0,options={})=>specimenSprite({scale:1},{id},time,options);
function bounds(s,id){
 assert.equal(s.clipped,false,id);
 assert.equal(s.width,64);assert.equal(s.art.length,36);
 assert(s.art.every((r,y)=>r.length===s.width&&r.length===s.tones[y].length&&/^[ -~]+$/.test(r)),id+' printable, aligned rows');
 assert(s.fills.every(f=>f.x>=0&&f.y>=0&&f.w>0&&f.x+f.w<=s.width&&f.y<s.art.length&&s.panels[f.tone]),id+' bounded material');
 assert(s.tones.every(r=>[...r].every(t=>s.inks[t])),id+' mapped ink');
 assert(s.anchorX>=0&&s.anchorX<s.width);assert.equal(s.groundRow,s.art.length);
}
test('33 authored specimen forms are bounded and have distinct geometry',()=>{
 assert.deepEqual(Object.keys(B).sort(),ids.slice().sort());
 const forms=new Set();
 for(const id of ids){const s=sprite(id);bounds(s,id);assert.equal(s.construction,'specimen-v1');assert(s.detail);assert(s.fills.length>10);assert(s.art.join('').replace(/ /g,'').length>60,id+' structural ink');forms.add(s.art.join('\n'));}
 assert.equal(forms.size,33);assert.equal(sprite('unknown'),null);
});
test('stationary materials are deterministic and Reduced Motion is stable',()=>{
 for(const id of ids)for(const state of [{},{condition:.1,dirt:1,wetness:1},{condition:.6,dirt:.4,wetness:.8}]){
  const first=sprite(id,0,{state});bounds(first,id);
  assert.deepEqual(first,sprite(id,10000,{state}));
  assert.deepEqual(first,sprite(id,20000,{state,motion:false}));
  assert.equal(first.animated,false);assert.equal(first.sway,0);assert.equal(first.lift,0);
 }
});
test('native surface projection preserves silhouettes and never mutates inputs',()=>{
 const beforeB=JSON.stringify(B);
 for(const id of ids){
  const base=Object.freeze({scale:1,art:Object.freeze(['old']),inks:Object.freeze({b:'old'})}),item=Object.freeze({id}),state=Object.freeze({condition:.2,dirt:.8,wetness:.9}),before=JSON.stringify({base,item,state});
  const s=specimenSprite(base,item,3,{state});
  assert.equal(JSON.stringify({base,item,state}),before);
  assert.deepEqual(s.art,sprite(id).art,id+' weather preserves contours');
  assert.notDeepEqual(s.tones,sprite(id).tones,id+' surface readback');
  assert.deepEqual(sprite(id,0,{state:{condition:NaN,dirt:Infinity,wetness:-2}}),sprite(id),id+' invalid native values safely normalized');
 }
 assert.equal(JSON.stringify(B),beforeB);
});
