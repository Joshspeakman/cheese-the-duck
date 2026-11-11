import test from 'node:test';import assert from 'node:assert/strict';
import {FOOTWEAR_BLUEPRINTS,fittedFootwear,shoeMaterial} from '../client/footwear-workshop.mjs';
import {FOOTWEAR_CARE} from '../client/headwear-care.mjs';
import {itemSprite} from '../client/ultra-items.mjs';import {characterSprite} from '../client/ultra-characters.mjs';
import {STAGES,ACTIONS} from '../client/scruffy-sprites.mjs';
import {GUEST_CAST} from '../client/guest-cast.mjs';
const material={wet_left:.8,wet_right:.2,snow_left:.6,snow_right:0,soil_left:.7,soil_right:.3,slack_left:.8,slack_right:.1,phase:1};
function bounds(m,label){assert(!m.clipped,label+' clipped');assert(m.fills.every(f=>f.x>=0&&f.y>=0&&f.x+f.w<=m.width&&f.y<m.art.length),label+' fills');assert(m.art.every((r,y)=>r.length===m.tones[y].length&&/^[ -~]*$/.test(r)),label+' ASCII');}
test('seven footwear constructions have separate uppers, soles and per-foot material',()=>{
 const signatures=new Set();
 for(const id in FOOTWEAR_BLUEPRINTS){
  const dry=itemSprite(id,0);assert.equal(dry.construction,'footwear-v1');signatures.add(dry.art.join('\n'));bounds(dry,id);
  for(let n=0;n<12;n++){const state={apparel:{...material,phase:n}},before=JSON.stringify(state),a=itemSprite(id,0,{state});bounds(a,id);assert.deepEqual(a,itemSprite(id,99,{state}));assert.equal(JSON.stringify(state),before);assert.deepEqual(itemSprite(id,n,{state,motion:false}),itemSprite(id,99,{state:{apparel:{...state.apparel,phase:99}},motion:false}));}
  assert.notDeepEqual(itemSprite(id,0,{state:{apparel:{soil_left:1}}}).art,itemSprite(id,0,{state:{apparel:{soil_right:1}}}).art,id+' sides have independent dirt');
 }
 assert.equal(signatures.size,7);assert.deepEqual(shoeMaterial({wet_left:NaN,snow_left:-2,soil_left:4,slack_left:Infinity}),{wet:0,snow:0,soil:1,slack:0});
});
test('each shoe follows its own posed foot and never hangs below the sole',()=>{
 for(const {id:stage}of STAGES.slice(1))for(const {id:state}of ACTIONS)for(const id in FOOTWEAR_BLUEPRINTS)for(const time of [.1,.4,.8,1.2]){
  const bare=characterSprite({stage,state},time),r=bare.rig,piece=fittedFootwear(r,id,{material,phase:1}),worn=characterSprite({stage,state,cosmetics:{feet:id},apparel:{[id]:material}},time);
  bounds(worn,id+'/'+stage+'/'+state);bounds(piece.front,id);assert.equal(worn.scale,bare.scale);assert.equal(worn.art[r.eye.y][r.eye.x],bare.art[r.eye.y][r.eye.x]);
  assert.equal(piece.feet.length,r.feet.length);
  if(!r.feet.length)assert(piece.front.art.every(row=>!row.trim()),'tucked or submerged feet have no floating shoes');
  piece.feet.forEach((shoe,i)=>{const f=r.feet[i];assert.equal(shoe.sole.y,f.y);assert.equal(shoe.sole.x,f.x);assert.equal(shoe.bounds.y+shoe.bounds.h-1,f.y);});
  for(const f of piece.front.fills)assert(piece.feet.some(s=>f.y>=s.bounds.y&&f.y<s.bounds.y+s.bounds.h&&f.x>=s.bounds.x&&f.x+f.w<=s.bounds.x+s.bounds.w),id+' fill is attached to a shoe');
 }
 assert.deepEqual(characterSprite({stage:'egg',cosmetics:{feet:'rain_boots'}},0).wearables,[]);
});
test('two-foot care lifts one shoe at a time and reaches each real contact across ages and directions',()=>{
 for(const [id,p]of Object.entries(FOOTWEAR_BLUEPRINTS))for(const [action,spec]of Object.entries(FOOTWEAR_CARE).filter(([,s])=>s.shapes.includes(p.shape)))for(const {id:stage}of STAGES.slice(1))for(const facing of [true,false]){
  const frames=new Set();
  for(const elapsed of [0,spec.contact*.7,spec.contacts[0],spec.duration/2,spec.contacts[1],spec.duration*.94]){
   const data={stage,state:'thinking',facing,cosmetics:{feet:id},apparel:{[id]:material},hatCare:{active:{id:action,item:id,elapsed,appliedFeet:spec.contacts.map((at,i)=>elapsed>=at?i:-1).filter(i=>i>=0)}}},before=JSON.stringify(data),m=characterSprite(data,0);bounds(m,id+'/'+stage+'/'+action);frames.add(m.art.join('\n'));assert.equal(JSON.stringify(data),before);
   const foot=spec.contacts.indexOf(elapsed);if(foot>=0){assert(m.hatContact&&m.hatTarget);assert(Math.hypot(m.hatContact.x-m.hatTarget.x,m.hatContact.y-m.hatTarget.y)<=1.5,id+' reaches '+foot);assert.equal(m.rig.feet[1-foot].y,39,'other foot stays planted');assert.equal(m.rig.feet[foot].y,36,'target foot is raised');}
   assert.deepEqual(characterSprite({...data,motion:false},0).art,characterSprite({...data,motion:false,hatCare:{active:{...data.hatCare.active,elapsed:8}}},0).art);
  }
  assert(frames.size>=4,id+'/'+action+' has approach, both contacts and release');
 }
});
test('new shoe fitting preserves existing visitor identities and combined wardrobes',()=>{
 for(const p of Object.values(GUEST_CAST))for(const state of ['walking','swimming','sleeping','preening'])bounds(characterSprite({castId:p.id,name:p.name,state},.4,true),p.id);
 for(const {id:stage}of STAGES.slice(1))for(const id in FOOTWEAR_BLUEPRINTS){const m=characterSprite({stage,state:'walking',cosmetics:{feet:id,body:'winter_puffy_coat',back:'cape_superhero',neck:'scarf_red',head:'hat_red'}},.8);bounds(m,id+'/'+stage);assert(m.wearables.includes(id));}
});
