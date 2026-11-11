import test from 'node:test';import assert from 'node:assert/strict';
import {GARMENT_BLUEPRINTS,fittedGarment} from '../client/garment-workshop.mjs';
import {GARMENT_CARE} from '../client/headwear-care.mjs';
import {itemSprite} from '../client/ultra-items.mjs';import {characterSprite} from '../client/ultra-characters.mjs';
import {fitWearables} from '../client/wearables.mjs';import {STAGES,ACTIONS} from '../client/scruffy-sprites.mjs';
import {GUEST_CAST} from '../client/guest-cast.mjs';
const choices=id=>Object.entries(GARMENT_CARE).filter(([,s])=>s.shapes.includes(GARMENT_BLUEPRINTS[id].shape));
const inside=(x,y,r)=>r&&x>=r.x&&x<r.x+r.w&&y>=r.y&&y<r.y+r.h;
const onSurface=(m,p)=>Boolean(m.art[p.y]?.[p.x]?.trim())||m.fills.some(f=>f.y===p.y&&p.x>=f.x&&p.x<f.x+f.w);
function bounds(m,label){assert(!m.clipped,label+' glyphs');assert(m.fills.every(f=>f.x>=0&&f.y>=0&&f.x+f.w<=m.width&&f.y<m.art.length),label+' fills');assert(m.art.every((r,y)=>r.length===m.tones[y].length&&/^[ -~]*$/.test(r)),label+' printable ASCII');}
test('18 garment constructions have distinct sewn details and bounded native material projection',()=>{
 const signatures=new Set();
 for(const id in GARMENT_BLUEPRINTS){
  const dry=itemSprite(id,0);assert.equal(dry.construction,'garment-v1');signatures.add(dry.art.join('\n'));
  for(let n=0;n<16;n++){
   const state={apparel:{wet:n/15,snow:1-n/15,wind:1,phase:n,soil:.5,slack:.8,crease:.7}},before=JSON.stringify(state);
   const a=itemSprite(id,0,{state}),b=itemSprite(id,90,{state});bounds(a,id+'/'+n);assert.deepEqual(a,b);assert.equal(JSON.stringify(state),before);
   const paused=t=>itemSprite(id,t,{state:{apparel:{...state.apparel,phase:t}},motion:false});assert.deepEqual(paused(0),paused(9));
  }
 }
 assert.equal(signatures.size,18,'tint alone does not define a new garment');
});
test('garments follow posed feather contours and keep face, wing openings and feet clear',()=>{
 for(const {id:stage}of STAGES.slice(1))for(const {id:state}of ACTIONS)for(const [id,p]of Object.entries(GARMENT_BLUEPRINTS)){
  const bare=characterSprite({stage,state},.7),r=bare.rig,material={wet:.8,snow:.6,wind:1,phase:1,soil:.7,slack:.9,crease:.8};
  const data={stage,state,cosmetics:{garment:id},apparel:{[id]:material}},before=JSON.stringify(data),worn=characterSprite(data,.7);
  bounds(worn,id+'/'+stage+'/'+state);assert.equal(JSON.stringify(data),before);assert.equal(worn.scale,bare.scale);
  assert.equal(worn.art[r.eye.y][r.eye.x],bare.art[r.eye.y][r.eye.x],id+' preserves expression');
  if(worn.bill)assert.equal(worn.art[worn.bill.y][worn.bill.x],bare.art[bare.bill.y][bare.bill.x],id+' preserves bill');
  for(const f of r.feet)assert.equal(worn.art[f.y].slice(f.x,f.x+2),bare.art[f.y].slice(f.x,f.x+2));
  const piece=fittedGarment(r,id,{material,phase:1});bounds(piece.front,id+' front');bounds(piece.back,id+' rear');
  if(p.slot==='back')for(let y=0;y<piece.back.art.length;y++)if(piece.back.art[y].trim())assert(y<=Math.max(r.body.y+r.body.h-1,...r.feet.map(f=>f.y)),id+'/'+stage+'/'+state+' stays above the planted floor');
  if(p.slot!=='back')for(const f of piece.front.fills)for(let x=f.x;x<f.x+f.w;x++){
   assert(r.torso.some(t=>t.y===f.y&&x>=t.x&&x<t.x+t.w),id+' follows torso');assert(!inside(x,f.y,r.faceBounds)&&!inside(x,f.y,r.wing),id+' leaves face and wings open');
  }
  for(const [,spec]of choices(id)){const p=piece.contacts[spec.anchor];assert(p&&(onSurface(piece.front,p)||onSurface(piece.back,p)),id+'/'+stage+'/'+state+'/'+spec.anchor+' contacts visible material');}
 }
 const egg=characterSprite({stage:'egg',cosmetics:{body:'raincoat',back:'cape'}},0);assert.deepEqual(egg.wearables,[]);
});
test('care contacts fitted cloth through all ages and directions, without free rendering effects',()=>{
 for(const id in GARMENT_BLUEPRINTS)for(const [action,spec]of choices(id))for(const {id:stage}of STAGES.slice(1))for(const facing of [true,false]){
  const variants=new Set();
  for(const elapsed of [0,spec.contact*.7,spec.contact,spec.contact+.35,spec.duration*.85]){
   const data={stage,state:'thinking',facing,cosmetics:{garment:id},apparel:{[id]:{snow:.7,wet:.6,phase:1,soil:.4,slack:.6,crease:.7}},hatCare:{active:{id:action,item:id,elapsed,applied:elapsed>=spec.contact}}};
   const before=JSON.stringify(data),m=characterSprite(data,0);bounds(m,id+'/'+stage+'/'+action);assert.equal(JSON.stringify(data),before);variants.add(m.art.join('\n'));
   if(elapsed===spec.contact){assert(m.hatContact&&m.hatTarget,id+'/'+stage+'/'+action+' contact');assert(Math.hypot(m.hatContact.x-m.hatTarget.x,m.hatContact.y-m.hatTarget.y)<=2.1,id+' reaches '+spec.anchor);}
   assert.deepEqual(characterSprite({...data,motion:false},0).art,characterSprite({...data,motion:false,hatCare:{active:{...data.hatCare.active,elapsed:spec.duration*.9}}},0).art);
  }
  assert(variants.size>=3,id+'/'+stage+'/'+action+' anticipation/contact/release');
 }
});
test('Reduced Motion freezes cloth and existing visitors keep their own fitted garments',()=>{
 for(const id in GARMENT_BLUEPRINTS){const rig={...characterSprite({stage:'adult'},0).rig,motion:false},apparel={wet:.8,snow:.5,wind:.9,phase:1,soil:.4,slack:.3,crease:.7};assert.deepEqual(fitWearables(rig,{garment:id},0,{[id]:apparel}),fitWearables(rig,{garment:id},500,{[id]:{...apparel,phase:5}}));}
 let fitted=0;
 for(const p of Object.values(GUEST_CAST))for(const state of ['idle','walking','swimming','sleeping','quacking','preening'])for(const facing of [true,false]){
  const model=characterSprite({castId:p.id,name:p.name,state,facing},.7,true);bounds(model,p.id+'/'+state);
  if(['duck','duckling'].includes(p.species))for(const id of p.gear.filter(id=>GARMENT_BLUEPRINTS[id])){assert(model.wearables.includes(id),p.id+' wears '+id);fitted++;}
 }
 assert(fitted>0);
});
test('rear fabric follows the feather silhouette instead of disappearing inside its empty bounding corners',()=>{
 let checked=0;
 for(const id of ['cape','cape_superhero','backpack_tiny'])for(const stage of ['duckling','adult','legendary']){
  const data={stage,state:'idle'},bare=characterSprite(data,.7),r=bare.rig,material={phase:1,wind:.7},worn=characterSprite({...data,cosmetics:{back:id},apparel:{[id]:material}},.7),piece=fittedGarment(r,id,{material,phase:1});
  for(let y=0;y<48;y++)for(let x=0;x<76;x++)if(piece.back.art[y][x]!==' '&&bare.art[y][x]===' '&&inside(x,y,r.body)&&!inside(x,y,r.faceBounds)&&!r.occlusion.some(f=>f.y===y&&x>=f.x&&x<f.x+f.w)){
   assert.equal(worn.art[y][x],piece.back.art[y][x],id+' retains the cloth connection outside actual feathers');checked++;
  }
 }
 assert(checked>0,'negative space inside a real body bounding box was exercised');
});
