// Wonder machines: artwork invariants, routine/anchor binding and part ownership.
import test from 'node:test';
import assert from 'node:assert/strict';
import {wonderSprite,WONDER_BLUEPRINTS as B} from '../client/wonder-workshop.mjs';
import {WONDER_ROUTINES as R,wonderPose,sampleTrack} from '../client/wonder-routines.mjs';
import {WONDER_CHOICES,wonderSummary} from '../client/wonder-state.mjs';
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';
import {ITEM_CATALOG} from '../client/item-catalog.mjs';
const states=id=>{const out=[];for(let k=0;k<10;k++){const s={};for(const [f,[d,lo,hi]] of Object.entries(B[id].fields))s[f]=k===0?d:k===1?lo:k===2?hi:lo+(hi-lo)*((k*37)%11)/10;out.push(s);}return out;};
test('all 32 shop wonders route to bespoke construction at their blueprint scale',()=>{
 assert.equal(Object.keys(B).length,32);
 for(const id of Object.keys(B)){
  assert.ok(ITEM_CATALOG[id]?.sources.some(s=>s.startsWith('shop')),id+' is a shop item');
  const m=itemSprite(id,1.2,{state:{wonder:{}}});
  assert.equal(m.construction,'wonder-v1',id);assert.equal(itemWorldScale(id),B[id].scale);
 }
});
test('every saved state and routine moment draws printable, unclipped art with in-bounds anchors',()=>{
 for(const id of Object.keys(B))for(const [k,st] of states(id).entries()){
  const keys=Object.keys(R).filter(r=>R[r].item===id),key=keys[k%keys.length],work={id:key,elapsed:R[key].duration*k/9};
  const m=wonderSprite({},{id},k*.7,{state:{wonder:st},pose:{wonder:wonderPose(work)}});
  assert.ok(!m.clipped,id+' clipped');assert.ok(m.art.every(r=>/^[ -~]*$/.test(r)),id+' printable');
  const gk=B[id].grid||1;assert.equal(m.art.length,Math.ceil(B[id].h/gk));assert.equal(m.width,Math.ceil(B[id].w/gk));
  for(const [a,p] of Object.entries(m.anchors))assert.ok(p.x>=0&&p.x<m.width&&p.y>=0&&p.y<m.art.length,id+' '+a);
  for(const [,q] of R[key].track)if(q.anchor)assert.ok(m.anchors[q.anchor],key+' needs anchor '+q.anchor);
 }
});
test('saved native state visibly changes the drawing',()=>{
 const draw=(id,w)=>wonderSprite({},{id},0,{state:{wonder:w},motion:false}).art.join('\n');
 assert.notEqual(draw('volcano',{eruption:0}),draw('volcano',{eruption:1}));
 assert.notEqual(draw('ice_sculpture',{melt:0}),draw('ice_sculpture',{melt:.8}));
 assert.notEqual(draw('sand_castle',{towers:4}),draw('sand_castle',{towers:0}));
 assert.notEqual(draw('zen_garden',{pattern:0}),draw('zen_garden',{pattern:2}));
 assert.notEqual(draw('time_machine',{year:2026}),draw('time_machine',{year:1885}));
 assert.notEqual(draw('dragon_egg',{incubation:.1}),draw('dragon_egg',{incubation:1}));
});
test('a routine overrides only the object parts it animates',()=>{
 const pose=wonderPose({id:'time_polish_brass',elapsed:5});
 assert.deepEqual(Object.keys(pose.object),['cloth']);
 const open=wonderSprite({},{id:'time_machine'},0,{state:{wonder:{door:1}},pose:{wonder:pose},motion:false});
 const shut=wonderSprite({},{id:'time_machine'},0,{state:{wonder:{door:0}},pose:{wonder:pose},motion:false});
 assert.notEqual(open.art.join(''),shut.art.join(''),'saved door state survives an unrelated routine');
 const lever=wonderPose({id:'time_pull_lever',elapsed:R.time_pull_lever.duration*.32});
 assert.ok(lever.object.lever>.9&&lever.object.door<.1,'lever pulled with the door shut at the contact');
});
test('track sampling is continuous and ends at rest',()=>{
 for(const [key,spec] of Object.entries(R)){
  const end=sampleTrack(spec.track,1,['x','y','b','w','contact']);
  for(const k of ['x','y','b','w','contact'])assert.equal(end[k],0,key+' returns to rest');
  let prev=sampleTrack(spec.track,0,['contact']).contact;
  for(let i=1;i<=50;i++){const v=sampleTrack(spec.track,i/50,['contact']).contact;assert.ok(Math.abs(v-prev)<=.6,key+' contact jumps');prev=v;}
 }
});
test('the journal offers every authored routine with a readable summary',()=>{
 assert.equal(Object.values(WONDER_CHOICES).flat().length,Object.keys(R).length);
 for(const id of Object.keys(B)){assert.ok(WONDER_CHOICES[id].length>=4,id);assert.ok(wonderSummary(id,{wonder:{}}).length>8,id);}
 assert.match(wonderSummary('money_printer',{wonder:{stack:.5}}),/not real money/);
});
test('every routine is physically reachable by the ages it is offered to, and the reach table matches the art',async()=>{
 const {execFileSync}=await import('node:child_process');
 const {fileURLToPath}=await import('node:url');execFileSync(process.execPath,['scripts/export-wonder-reach.mjs','--check'],{cwd:fileURLToPath(new URL('..',import.meta.url))});
 const {default:reach}=await import('../client/animation/wonder-reach.json',{with:{type:'json'}});
 for(const [key,r] of Object.entries(R)){
  assert.ok(reach.routines[key].reachableAges.length,key+' reachable by some age');
  if(r.ages)for(const a of reach.routines[key].reachableAges)assert.ok(r.ages.includes(a),key+' never widens authored ages');
 }
});
test('every routine mark and eye glyph is drawn whole by the D10 rig at every age',async()=>{
 const {characterSprite}=await import('../client/ultra-characters.mjs');
 for(const [key,r] of Object.entries(R))for(const [at,p] of r.track){if(!p.mark&&!p.eye)continue;
  for(const stage of ['hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary']){
   const art=characterSprite({stage,state:'idle',facing:true,performance:{kind:'wonder',routine:{id:key,elapsed:r.duration*at}}},2).art.join('\n');
   if(p.mark)assert.ok(art.includes(p.mark),key+' '+stage+' mark '+p.mark);if(p.eye)assert.ok(art.includes(p.eye),key+' '+stage+' eye '+p.eye);
  }}
});
test('a visitor keeping Cheese company reacts exactly at the routine contacts, never holds a tool, and personality changes the reaction',async()=>{
 const {companyTrack}=await import('../client/wonder-routines.mjs');
 for(const [key,r] of Object.entries(R)){
  const tracks=['cheer','nervous','steady','curious'].map(st=>companyTrack(key,st));
  for(const t of tracks){
   assert.equal(t.tool,'none',key);
   const times=t.track.map(k=>k[0]);assert.deepEqual(times,[...times].sort((a,b)=>a-b),key+' ordered');
   const shelter=r.tool==='none'&&r.when.includes('wet')&&r.duration>=30;  // visitors share the shelter by sitting close
   if(!shelter)for(const [at] of r.events)assert.ok(times.includes(at)||times.some(x=>Math.abs(x-at)<1e-9),key+' reacts at contact '+at);
   const pose=wonderPose({id:key,elapsed:r.duration*.5,company:{mode:'company',style:'cheer'}});assert.deepEqual(pose.object,{},key+' company moves no object part');
  }
  if(r.events.length&&!(r.tool==='none'&&r.when.includes('wet')))assert.notDeepEqual(tracks[0].track,tracks[1].track,key+' cheer differs from nervous');
 }
});
