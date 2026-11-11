import test from 'node:test';import assert from 'node:assert/strict';
import {HEADWEAR_BLUEPRINTS,fittedHat} from '../client/headwear-workshop.mjs';
import {itemSprite} from '../client/ultra-items.mjs';import {characterSprite} from '../client/ultra-characters.mjs';
import {fitWearables} from '../client/wearables.mjs';import {STAGES,ACTIONS} from '../client/scruffy-sprites.mjs';
import {hatCareChoices,HAT_CARE} from '../client/headwear-care.mjs';
test('41 authored hats have distinct new construction, bounded materials and no stale preview time in saved motion',()=>{
 const signatures=new Set();
 for(const id in HEADWEAR_BLUEPRINTS){
  const dry=itemSprite(id,0);assert.equal(dry.construction,'headwear-v1');signatures.add(dry.art.join('\n'));
  for(let n=0;n<24;n++){
   const state={apparel:{wet:n/23,snow:(23-n)/23,wind:1,phase:n,fog:n/23}},before=JSON.stringify(state),a=itemSprite(id,0,{state}),b=itemSprite(id,90,{state});
   assert(!a.clipped,id+' / '+n);assert.deepEqual(a.art,b.art,'native material phase owns motion');assert.equal(JSON.stringify(state),before);
   assert(a.art.every((r,y)=>r.length===a.tones[y].length&&/^[ -~]*$/.test(r)));
   assert(a.fills.every(f=>f.x>=0&&f.y>=0&&f.x+f.w<=a.width&&f.y<a.art.length),id+' fill bounds');
  }
 }
 assert.equal(signatures.size,41,'variants differ in construction, not just tint');
});
test('native hat care reaches fitted cloth and visor across hatched ages and both directions',()=>{
 for(const [id,p]of Object.entries(HEADWEAR_BLUEPRINTS))for(const [action,spec]of hatCareChoices(p))for(const {id:stage}of STAGES.slice(1))for(const facing of [true,false]){
  const variants=new Set();
  for(const elapsed of [0,spec.contact*.7,spec.contact,spec.contact+.35,spec.duration*.85]){
   const data={stage,state:'thinking',facing,cosmetics:{head:id},apparel:{[id]:{snow:.7,wet:.6,phase:1}},hatCare:{active:{id:action,item:id,elapsed,applied:elapsed>=spec.contact}}};
   const before=JSON.stringify(data),m=characterSprite(data,0);assert(!m.clipped,id+'/'+stage+'/'+action);assert.equal(JSON.stringify(data),before);variants.add(m.art.join('\n'));
   if(elapsed===spec.contact&&action!=='shed_rain'){
    assert(m.hatContact&&m.hatTarget,id+' contact');assert(Math.hypot(m.hatContact.x-m.hatTarget.x,m.hatContact.y-m.hatTarget.y)<=2.1,id+' reaches its actual anchor');
   }
   assert.deepEqual(characterSprite({...data,motion:false},0).art,characterSprite({...data,motion:false,hatCare:{active:{...data.hatCare.active,elapsed:spec.duration*.9}}},0).art,'reduced motion holds the care gesture');
  }
  assert(variants.size>=3,id+'/'+stage+'/'+action+' has anticipation, contact and release');
 }
 const d={stage:'egg',cosmetics:{head:'hat_red'},hatCare:{active:{id:'brush_snow',item:'hat_red',elapsed:3}}};assert.equal(characterSprite(d,0).hatContact,null);
});
test('headwear fits actual posed heads through every age and action, preserving face and body scale',()=>{
 for(const {id:stage}of STAGES.slice(1))for(const {id:state}of ACTIONS)for(const id in HEADWEAR_BLUEPRINTS){
  const bare=characterSprite({stage,state},.7),worn=characterSprite({stage,state,cosmetics:{head:id}},.7),r=bare.rig;
  assert(!worn.clipped,id+'/'+stage+'/'+state);assert.equal(worn.scale,bare.scale);
  assert.equal(worn.art[r.eye.y][r.eye.x],bare.art[r.eye.y][r.eye.x],id+' preserves expression');
  const plan=fitWearables(r,{head:id},.7),hat=fittedHat(r,id);
  const crown=hat.contacts.crown,xx=crown.x-hat.x,yy=crown.y-hat.y;
  assert(hat.art[yy]?.[xx]!==' '||hat.fills.some(f=>f.y===yy&&xx>=f.x&&xx<f.x+f.w),id+' brush anchor lies on its constructed surface');
  assert.equal(hat.bandY,r.head.y,'band sits on the posed head');
  for(const f of plan.fills)assert(f.y<=r.head.y,id+' fabric may not cover the face');
  if(worn.bill)assert.equal(worn.art[worn.bill.y][worn.bill.x],bare.art[bare.bill.y][bare.bill.x],id+' leaves bill visible');
 }
});
test('native wet fabric, snow and helmet fog render without inventing time or overriding reduced motion',()=>{
 for(const id of ['hat_beanie','hat_wizard','hat_party','space_helmet']){
  const duck={stage:'adult',state:'idle',cosmetics:{head:id},apparel:{[id]:{wet:.8,snow:.5,wind:.9,phase:1,fog:.8}}};
  const a=characterSprite(duck,0),b=characterSprite(duck,0);assert.deepEqual(a.art,b.art);
  const rig={...a.rig,motion:false};assert.deepEqual(fitWearables(rig,duck.cosmetics,0,duck.apparel),fitWearables(rig,duck.cosmetics,500,{[id]:{...duck.apparel[id],phase:5}}));
  assert.notDeepEqual(itemSprite(id,0,{state:{apparel:duck.apparel[id]}}).art,itemSprite(id,0).art,id+' has actual weather marks');
 }
 const egg=characterSprite({stage:'egg',cosmetics:{head:'hat_red'}},0);assert.deepEqual(egg.wearables,[],'unhatched Cheese has no cosmetic head');
});
