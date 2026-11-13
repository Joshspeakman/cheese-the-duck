// Curios: bespoke art for the 116 cards, fish, feathers, badges, trophies, treasures and tools.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {curioSprite,CURIO_BLUEPRINTS as B} from '../client/curio-workshop.mjs';
const req=JSON.parse(fs.readFileSync(new URL('../overhaul/animation-milestone/requirements.json',import.meta.url),'utf8'));
const pending=req.items.filter(i=>i.art==='pending').map(i=>i.id);
const ids=Object.keys(B);
const draw=(id,time,motion=true)=>curioSprite({},{id},time,{motion});
const TIMES=[0,.34,.71,1.03,1.9,2.6];
test('every pending object has a curio blueprint (and only those)',()=>{
 assert.equal(pending.length,116);
 for(const id of pending)assert.ok(B[id],id+' has no curio blueprint');
 assert.deepEqual([...ids].sort(),[...pending].sort());
 for(const [id,b] of Object.entries(B)){
  assert.ok(b.type&&b.w>0&&b.h>0&&b.scale>0&&b.grid>=1&&b.grid<=3,id+' blueprint fields');
  assert.ok(4.65*b.scale>=2.4,id+' glyphs below 2.4 px at the review camera');
 }
});
test('every curio renders printable, unclipped art with in-bounds anchors at every time, motion on and off',()=>{
 for(const id of ids){
  const b=B[id];
  for(const motion of [true,false])for(const time of TIMES){
   const m=draw(id,time,motion);
   assert.ok(m,id+' did not render');assert.equal(m.construction,'curio-v1');
   assert.ok(!m.clipped,id+' clipped (motion '+motion+', t '+time+')');
   assert.ok(m.art.every(r=>/^[ -~]*$/.test(r)),id+' printable ASCII');
   assert.equal(m.art.length,Math.ceil(b.h/b.grid),id+' rows');assert.equal(m.width,Math.ceil(b.w/b.grid),id+' width');
   assert.ok(m.art.every(r=>r.length===m.width),id+' ragged rows');
   assert.ok(m.tones.every((r,y)=>r.length===m.width&&[...r].every(t=>m.inks[t]&&m.panels[t])),id+' tones');
   assert.ok(m.fills.every(q=>q.x>=0&&q.y>=0&&q.y<m.art.length&&q.x+q.w<=m.width&&m.panels[q.tone]),id+' fills inside the canvas');
   const ink=m.art.join('').replace(/ /g,'').length;assert.ok(ink>=40,id+' is nearly empty ('+ink+' glyphs)');
   const names=Object.keys(m.anchors);assert.ok(names.includes('entry')&&names.includes('contact')&&names.length>=4&&names.length<=8,id+' anchors '+names);
   for(const [a,p] of Object.entries(m.anchors))assert.ok(p.x>=0&&p.x<m.width&&p.y>=0&&p.y<m.art.length,id+' anchor '+a);
  }
 }
});
test('motion:false is deterministic and time-independent; motion steps at 3 fps and is memoised',()=>{
 for(const id of ids){
  const a=draw(id,0,false),b=draw(id,5.5,false);
  assert.equal(a.art.join('\n'),b.art.join('\n'),id+' static art changes with time');assert.equal(a.tones.join('\n'),b.tones.join('\n'),id+' static tones');
  const x=draw(id,1.2,true),y=draw(id,1.2,true);assert.equal(x.art.join('\n'),y.art.join('\n'),id+' same time differs');assert.strictEqual(x.anchors,y.anchors,id+' memo');
 }
});
test('idle motion exists where it should: most curios animate over a few seconds',()=>{
 const still=[];
 for(const id of ids){const seen=new Set();for(let t=0;t<4;t+=1/3)seen.add(draw(id,t,true).art.join('\n'));if(seen.size<2)still.push(id);}
 assert.ok(still.length<=6,'too many curios never move: '+still.join(' '));
});
test('every curio looks different from every other',()=>{
 const seen=new Map();
 for(const id of ids){
  const m=draw(id,0,false),key=m.art.join('\n')+'|'+m.tones.join('\n');
  assert.ok(!seen.has(key),id+' looks identical to '+seen.get(key));seen.set(key,id);
 }
 // and not merely a recolour of a sibling: the glyph layout must differ
 const layouts=new Map();
 for(const id of ids){const k=draw(id,0,false).art.join('\n');assert.ok(!layouts.has(k),id+' has the same glyph layout as '+layouts.get(k));layouts.set(k,id);}
});
test('sizes follow object class: cards ~0.4-0.5 duck, badges ~0.4, fish by size class, watchtower ~2.5 ducks',()=>{
 const ducks=id=>B[id].h/B[id].grid*B[id].scale*.0191;
 for(const id of ids.filter(i=>B[i].type==='card'))assert.ok(ducks(id)>.38&&ducks(id)<.52,id);
 for(const id of ids.filter(i=>B[i].type==='badge'))assert.ok(ducks(id)>.35&&ducks(id)<.5,id);
 assert.ok(ducks('watchtower')>2.3&&ducks('watchtower')<2.8);
 const len=id=>B[id].w/B[id].grid*B[id].scale*.0122;
 assert.ok(len('minnow')<len('goldfish')&&len('goldfish')<len('trout')&&len('trout')<len('catfish')&&len('catfish')<len('swordfish')&&len('swordfish')<len('ancient_dragon_fish'));
 for(const id of ids)assert.ok(ducks(id)<=2.8&&ducks(id)>=.08,id+' size '+ducks(id));
});
