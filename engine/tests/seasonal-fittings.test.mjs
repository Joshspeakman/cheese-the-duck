import test from 'node:test';
import assert from 'node:assert/strict';
import {SEASONAL_FITTINGS,fittedSeasonalPiece} from '../client/seasonal-fittings.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {fitWearables} from '../client/wearables.mjs';
import {STAGES,ACTIONS} from '../client/scruffy-sprites.mjs';
import {CASTLE_SCORES} from '../client/castle-care.mjs';
import {HAT_CARE} from '../client/headwear-care.mjs';
import {mirror} from '../client/ultra-art.mjs';
const ids=Object.keys(SEASONAL_FITTINGS);
test('both pieces fit hatched ages, actions and mirrored directions without moving anatomy',()=>{
 for(const {id:stage}of STAGES.slice(1))for(const {id:state}of ACTIONS)for(const id of ids)for(const t of [0,.4,.9]){
  const bare=characterSprite({stage,state,facing:true},t),input={stage,state,facing:true,cosmetics:{item:id}},before=JSON.stringify(input),c=characterSprite(input,t),piece=fittedSeasonalPiece(bare.rig,id,{phase:t});
  assert(!c.clipped&&!piece.front.clipped&&!piece.back.clipped,id+'/'+stage+'/'+state);assert(c.art.every(r=>/^[ -~]*$/.test(r)));assert.equal(JSON.stringify(input),before);assert.equal(c.scale,bare.scale);assert.deepEqual(c.rig.feet,bare.rig.feet);assert.deepEqual(c.grip,bare.grip);
  const e=bare.rig.eye;assert.equal(c.art[e.y][e.x],bare.art[e.y][e.x],id+' eye');
  for(const f of bare.rig.feet)assert.equal(c.art[f.y].slice(f.x,f.x+2),bare.art[f.y].slice(f.x,f.x+2),id+' feet');
  assert.deepEqual(characterSprite({...input,facing:false},t).art,mirror(c.art));assert(c.wearables.includes(id));
  if(id==='winter_mittens'){
   assert.deepEqual(piece.contacts.hands,bare.rig.handContacts);if(!piece.contacts.hands.length)assert(piece.front.art.every(r=>!r.trim()),'submerged or hidden hands have no floating mittens');
   for(let y=0;y<48;y++)for(let x=0;x<76;x++)if(piece.front.art[y][x]!==' ')assert(piece.contacts.hands.some(h=>Math.abs(x-h.x)<=2&&Math.abs(y-h.y)<=1),'mitten paints beyond hand');
  }else {assert(piece.front.art.some(r=>r.trim()));assert(piece.back.art.some(r=>r.trim()));assert(piece.contacts.waist.y<39);}
 }
 for(const id of ids)assert.deepEqual(characterSprite({stage:'egg',cosmetics:{item:id}},0).wearables,[]);
});
test('mittens preserve exact working grips and hat-care contacts instead of returning to folded wings',()=>{
 for(const {id:stage}of STAGES.slice(1))for(const facing of [true,false]){
  for(const id of ['castle_start','castle_door_open','castle_hose_stow'])for(const [at]of CASTLE_SCORES[id].effects){
   const elapsed=at*CASTLE_SCORES[id].duration,performance={kind:'carnival',role:'a',routine:{id,stage:'service',clock:elapsed,ride_elapsed:elapsed}},input={stage,state:'idle',facing,performance};
   const bare=characterSprite(input,0),c=characterSprite({...input,cosmetics:{hands:'winter_mittens'}},0);
   assert.deepEqual(c.grip,bare.grip);assert.deepEqual(c.workGripRest,bare.workGripRest);assert.deepEqual(c.rig.handContacts,bare.rig.handContacts);assert(c.rig.handContacts.some(h=>h.x===(facing?c.grip.x:75-c.grip.x)&&h.y===c.grip.y),'working hand published');assert(!c.clipped);
   assert.notEqual(c.tones[c.grip.y][c.grip.x],bare.tones[bare.grip.y][bare.grip.x],'actual grip wears knitted palm');
   const ring=characterSprite({...input,cosmetics:{waist:'summer_swim_ring'}},0);assert.deepEqual(ring.grip,bare.grip);assert.equal(ring.art[ring.grip.y][ring.grip.x],bare.art[bare.grip.y][bare.grip.x],'swim ring leaves working contact visible');assert.equal(ring.tones[ring.grip.y][ring.grip.x],bare.tones[bare.grip.y][bare.grip.x]);
  }
  for(const elapsed of [1,HAT_CARE.brush_snow.contact,5]){
   const input={stage,state:'thinking',facing,cosmetics:{head:'hat_red'},apparel:{hat_red:{snow:.7}},hatCare:{active:{id:'brush_snow',item:'hat_red',elapsed}}},bare=characterSprite(input,0),c=characterSprite({...input,cosmetics:{...input.cosmetics,hands:'winter_mittens'}},0);
   assert.deepEqual(c.hatContact,bare.hatContact);assert.deepEqual(c.hatTarget,bare.hatTarget);assert.deepEqual(c.grip,bare.grip);assert(!c.clipped);
   if(c.hatContact){assert(c.rig.handContacts.some(h=>h.x===(facing?c.hatContact.x:75-c.hatContact.x)&&h.y===c.hatContact.y));assert.notEqual(c.tones[c.hatContact.y][c.hatContact.x],bare.tones[bare.hatContact.y][bare.hatContact.x],'hat-care tip wears glove');}
  }
 }
});
test('Reduced Motion fixes decorative geometry and native apparel input remains read-only',()=>{
 for(const {id:stage}of STAGES.slice(1))for(const id of ids){
  const rig={...characterSprite({stage,state:'idle'},0).rig,motion:false},input={item:id},apparel={[id]:{phase:1}},before=JSON.stringify({rig,input,apparel});
  assert.deepEqual(fittedSeasonalPiece(rig,id,{phase:0}),fittedSeasonalPiece(rig,id,{phase:100}));
  assert.deepEqual(fitWearables(rig,input,0,apparel).layers,fitWearables(rig,input,100,{[id]:{phase:100}}).layers);assert.equal(JSON.stringify({rig,input,apparel}),before);
 }
});
