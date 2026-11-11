import test from 'node:test';
import assert from 'node:assert/strict';
import {seedSprite,SEED_BLUEPRINTS} from '../client/seed-workshop.mjs';
const ids='seeds seed vegetable_seed sunflower_seeds better_bait enchanted_seeds tulip_seeds rose_seeds carrot_seeds tomato_seeds pumpkin_seeds strawberry_seeds watermelon_seeds mint_seeds golden_seeds crystal_seeds worm juicy_worm giant_worm'.split(' ');
test('all 19 seeds and bait have bounded printable constructions and grounded occupied material',()=>{
 assert.deepEqual(Object.keys(SEED_BLUEPRINTS),ids);
 const signatures=new Set();
 for(const id of ids){
  const s=seedSprite({}, {id}, 0);assert.equal(s.clipped,false,id);assert.equal(s.construction,'seed-v1');
  assert.equal(s.art.length,s.tones.length);assert.equal(s.groundRow,s.art.length);assert.ok(s.scale>0&&s.scale<1);
  for(const [y,row] of s.art.entries()){assert.equal(row.length,s.width,id);assert.match(row,/^[ -~]+$/);assert.equal(s.tones[y].length,s.width);}
  for(const f of s.fills){assert.ok(f.x>=0&&f.y>=0&&f.x+f.w<=s.width&&f.y<s.art.length,id);assert.ok(s.panels[f.tone]);}
  assert.ok(s.art.at(-1).trim()||s.fills.some(f=>f.y===s.art.length-1),id);
  signatures.add(JSON.stringify([s.art,s.fills.map(({x,y,w})=>[x,y,w])]));
 }
 assert.equal(signatures.size,19,'not merely palette variants');
 assert.equal(seedSprite({}, {id:'unregistered_food'},0),null);
});
test('native condition projection is deterministic, bounded, and does not mutate inputs',()=>{
 for(const id of ids){
  const base={id,lift:9,sway:9},item={id},state={condition:.2,wetness:.8,dirt:.6};
  const before=JSON.stringify([base,item,state]);
  const a=seedSprite(base,item,0,{state}),b=seedSprite(base,item,987,{state,motion:0});
  assert.deepEqual(a,b,id);assert.equal(JSON.stringify([base,item,state]),before);assert.equal(a.lift,0);assert.equal(a.sway,0);assert.equal(a.animated,false);
  assert.notDeepEqual(a.art,seedSprite(base,item,0).art,id);
  assert.deepEqual(a.fills,seedSprite(base,item,0).fills,'condition must not invent lost material');
 }
});
test('reduced motion and ordinary time leave resting seeds and worms still',()=>{
 for(const id of ids)assert.deepEqual(seedSprite({}, {id},0,{motion:0}),seedSprite({}, {id},500,{motion:1}));
});
