import test from 'node:test';import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {ACCESSORY_BLUEPRINTS,fittedAccessory} from '../client/accessory-workshop.mjs';
import {ACCESSORY_CARE} from '../client/headwear-care.mjs';
import {itemSprite} from '../client/ultra-items.mjs';import {characterSprite} from '../client/ultra-characters.mjs';
import {fitWearables,wearableSlots} from '../client/wearables.mjs';import {STAGES,ACTIONS} from '../client/scruffy-sprites.mjs';
import {GUEST_CAST} from '../client/guest-cast.mjs';
const choices=id=>Object.entries(ACCESSORY_CARE).filter(([,s])=>s.shapes.includes(ACCESSORY_BLUEPRINTS[id].shape));
const onSurface=(m,p)=>Boolean(m.art[p.y]?.[p.x]?.trim())||m.fills.some(f=>f.y===p.y&&p.x>=f.x&&p.x<f.x+f.w);
function bounds(m,label){assert(!m.clipped,label);assert(m.fills.every(f=>f.x>=0&&f.y>=0&&f.x+f.w<=m.width&&f.y<m.art.length),label+' fills');assert(m.art.every((r,y)=>r.length===m.tones[y].length&&/^[ -~]*$/.test(r)),label+' printable ASCII');}
test('25 detailed accessories have distinct construction and read-only saved material projection',()=>{
 const signatures=new Set();
 for(const id in ACCESSORY_BLUEPRINTS){
  const dry=itemSprite(id,0);assert.equal(dry.construction,'accessory-v1');signatures.add(dry.art.join('\n'));
  for(let n=0;n<16;n++){
   const state={apparel:{wet:n/15,snow:1-n/15,wind:1,phase:n,fog:n/15,soil:.5,slack:.4}},before=JSON.stringify(state);
   const a=itemSprite(id,0,{state}),b=itemSprite(id,90,{state});bounds(a,id+'/'+n);assert.deepEqual(a.art,b.art);assert.equal(JSON.stringify(state),before);
   const paused=t=>itemSprite(id,t,{state:{apparel:{...state.apparel,phase:t}},motion:false});assert.deepEqual(paused(0).art,paused(9).art,'reduced motion stops catalog cloth');
  }
 }
 assert.equal(signatures.size,25,'tint alone is not a new construction');
 assert.deepEqual(wearableSlots,JSON.parse(readFileSync(new URL('../client/animation/wearable-slots.json',import.meta.url))),'native and renderer slot priority agree');
});
test('fitted accessories stay within actual poses and preserve age, expression and bill',()=>{
 for(const {id:stage}of STAGES.slice(1))for(const {id:state}of ACTIONS)for(const id in ACCESSORY_BLUEPRINTS){
  const bare=characterSprite({stage,state},.7),worn=characterSprite({stage,state,cosmetics:{accessory:id}},.7),r=bare.rig;
  bounds(worn,id+'/'+stage+'/'+state);assert.equal(worn.scale,bare.scale);
  assert.equal(worn.art[r.eye.y][r.eye.x],bare.art[r.eye.y][r.eye.x],id+' preserves expression');
  if(worn.bill)assert.equal(worn.art[worn.bill.y][worn.bill.x],bare.art[bare.bill.y][bare.bill.x],id+' preserves the bill');
  const piece=fittedAccessory(r,id,{phase:.7});bounds(piece.front,id+' front');bounds(piece.back,id+' back');
  for(const [,spec]of choices(id)){const p=piece.contacts[spec.anchor];assert(p&&onSurface(piece.front,p)||p&&onSurface(piece.back,p),id+'/'+spec.anchor+'/'+stage+'/'+state+' contact lies on constructed material');}
 }
 const egg=characterSprite({stage:'egg',cosmetics:{neck:'scarf_red',face:'glasses_nerd'}},0);assert.deepEqual(egg.wearables,[]);
});
test('accessory care reaches its posed material at all hatched ages, with distinct contact and release',()=>{
 for(const id in ACCESSORY_BLUEPRINTS)for(const [action,spec]of choices(id))for(const {id:stage}of STAGES.slice(1))for(const facing of [true,false]){
  const variants=new Set();
  for(const elapsed of [0,spec.contact*.7,spec.contact,spec.contact+.35,spec.duration*.85]){
   const data={stage,state:'thinking',facing,cosmetics:{accessory:id},apparel:{[id]:{snow:.7,wet:.6,phase:1,soil:.4,slack:.6}},hatCare:{active:{id:action,item:id,elapsed,applied:elapsed>=spec.contact}}};
   const before=JSON.stringify(data),m=characterSprite(data,0);bounds(m,id+'/'+stage+'/'+action);assert.equal(JSON.stringify(data),before);variants.add(m.art.join('\n'));
   if(elapsed===spec.contact){assert(m.hatContact&&m.hatTarget);assert(Math.hypot(m.hatContact.x-m.hatTarget.x,m.hatContact.y-m.hatTarget.y)<=2.1,id+' reaches '+spec.anchor);}
   assert.deepEqual(characterSprite({...data,motion:false},0).art,characterSprite({...data,motion:false,hatCare:{active:{...data.hatCare.active,elapsed:spec.duration*.9}}},0).art);
  }
  assert(variants.size>=3,id+'/'+stage+'/'+action+' anticipation/contact/release');
 }
});
test('saved cloth freezes under reduced motion, and existing visitor outfits use the same fitted accessories',()=>{
 for(const id in ACCESSORY_BLUEPRINTS){const rig={...characterSprite({stage:'adult'},0).rig,motion:false},apparel={wet:.8,snow:.5,wind:.9,phase:1,soil:.4,slack:.3,fog:.8};assert.deepEqual(fitWearables(rig,{accessory:id},0,{[id]:apparel}),fitWearables(rig,{accessory:id},500,{[id]:{...apparel,phase:5}}));}
 let fitted=0;
 for(const p of Object.values(GUEST_CAST))for(const state of ['idle','walking','swimming','sleeping','quacking','preening'])for(const facing of [true,false]){
  const model=characterSprite({castId:p.id,name:p.name,state,facing},.7,true);bounds(model,p.id+'/'+state);
  if(['duck','duckling'].includes(p.species))for(const id of p.gear.filter(id=>ACCESSORY_BLUEPRINTS[id])){assert(model.wearables.includes(id),p.id+' wears its own '+id);fitted++;}
 }
 assert(fitted>0,'real visitor outfits were exercised');
});
test('loose frames, cloth and cords visibly settle without losing the face or clipping young poses',()=>{
 for(const id of ['glasses_nerd','monocle','bow_tie_blue','scarf_red','pearl_necklace','bell_collar','headphones'])for(const {id:stage}of STAGES.slice(1)){
  const duck={stage,state:'idle',cosmetics:{accessory:id}},loose=characterSprite({...duck,apparel:{[id]:{slack:1,phase:0}}},0),settled=characterSprite({...duck,apparel:{[id]:{slack:0,phase:0}}},0);
  assert.notDeepEqual(loose.art,settled.art,id+'/'+stage+' visibly settles');
 }
 for(const id in ACCESSORY_BLUEPRINTS)for(const {id:stage}of STAGES.slice(1))for(const {id:state}of ACTIONS){
  const m=characterSprite({stage,state,cosmetics:{accessory:id},apparel:{[id]:{slack:1,phase:1,snow:1,wet:1,soil:1,fog:1,wind:1}}},.7);bounds(m,id+'/'+stage+'/'+state+' weathered');
  const e=m.rig.eye;assert.equal(m.art[e.y][e.x],e.char);
 }
});
