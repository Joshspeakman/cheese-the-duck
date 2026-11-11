import test from 'node:test';import assert from 'node:assert/strict';
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {GUEST_CAST} from '../client/guest-cast.mjs';
import {KEEPSAKE_BLUEPRINTS} from '../client/keepsake-workshop.mjs';
import {keepsakePose,keepsakeGeometry,KEEPSAKE_ROUTINES,KEEPSAKE_COMPANY} from '../client/keepsake-routines.mjs';
import {keepsakeSummary,KEEPSAKE_CHOICES} from '../client/keepsake-state.mjs';
import {weatherGlyphFamily} from '../client/glass-curios.mjs';
const items=['snow_globe','snowglobe','crystal_ball'];
const ages=['egg','hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'];
test('miniatures and oracle retain native physical state and distinct visible saved changes',()=>{
 for(const id of items){
  const state={keepsake:{glass:{energy:.8,phase:1.2,focus:.9,azimuth:1.1,vision:{weather:'snowy',biome:'pond'}}}},before=JSON.stringify(state);
  const a=itemSprite(id,0,{state}),b=itemSprite(id,300,{state});assert.deepEqual(a,b,'wall time cannot invent snow or weather');assert.equal(JSON.stringify(state),before);
  const changed=structuredClone(state);changed.keepsake.glass={energy:0,phase:0,focus:0,azimuth:0,vision:null};
  assert.notDeepEqual(a.art,itemSprite(id,0,{state:changed}).art,id+' shows native changed state');
  assert(!a.clipped);assert(a.art.every(r=>/^[ -~]*$/.test(r)));assert(a.fills.every(f=>f.x>=0&&f.y>=0&&f.x+f.w<=a.width&&f.y<a.art.length));
 }
 assert.notDeepEqual(itemSprite('snow_globe',0).art,itemSprite('snowglobe',0).art,'two authored landscapes');
 for(const id of ['snow_globe','snowglobe']){
  const a=itemSprite(id,0,{motion:false,state:{keepsake:{glass:{energy:.8,phase:0}}}});
  assert.deepEqual(a.art,itemSprite(id,0,{motion:false,state:{keepsake:{glass:{energy:.6,phase:2}}}}).art,'reduced motion holds circulating flakes still');
  assert.deepEqual(itemSprite(id,0,{state:{keepsake:{glass:{energy:.8,phase:0}}}}).art,itemSprite(id,0,{state:{keepsake:{glass:{energy:.8,phase:Math.PI*2}}}}).art,'native phase wraps without teleporting the snow');
 }
});
test('all actual glass controls use short physical reaches at unchanged body scale',()=>{
 let cases=0;
 for(const stage of ages)for(const id of items)for(const [core,spec]of Object.entries(KEEPSAKE_ROUTINES).filter(([,s])=>s.types?.includes(KEEPSAKE_BLUEPRINTS[id].type))){
  if(stage==='egg'||(['hatchling','duckling'].includes(stage)&&spec.tool!=='none'))continue;
  for(const [at]of spec.track){
   const routine={id:core,elapsed:at*spec.duration,start_open:0},pose=keepsakePose(routine),home={...itemSprite(id,0,{pose:{keepsake:pose}}),x:100,y:70,scale:itemWorldScale(id)};
   const c={...characterSprite({stage,facing:true,state:'idle',performance:{kind:'keepsake',routine}},0),x:100,y:70};
   const g=keepsakeGeometry(home,{character:c,inside:1},6,9);
   assert(!c.clipped);assert.equal(g.character.scale,c.scale);assert(Math.abs(g.character.y*9-g.ground)<.001);
   if(g.tip){assert(Math.hypot(g.tip.x-g.hand.x,g.tip.y-g.hand.y)/g.cw<6,stage+' '+id+' '+core+' short wing reach');if(pose.contact===1)assert(Math.hypot(g.tip.x-g.target.x,g.tip.y-g.target.y)<.001);}
   cases++;
  }
 }
 assert(cases>700);
});
test('every visitor observes the real miniature at a fixed physical side, never attached to Cheese',()=>{
 for(const actor of Object.values(GUEST_CAST))for(const [id,s]of Object.entries(KEEPSAKE_COMPANY).filter(([,s])=>s.item))for(const t of [.15,.4,.7,.95]){
  const routine={id:s.preview,elapsed:KEEPSAKE_ROUTINES[s.preview].duration*t,company:{id,role:'b'}},home={...itemSprite(s.item,0),x:100,y:70,scale:itemWorldScale(s.item)};
  const c={...characterSprite({id:actor.id,castId:actor.id,visitor:true,facing:false,state:'idle',performance:{kind:'keepsake',routine}},0,true),x:110,y:70};
  const g=keepsakeGeometry(home,{character:c,slot:1,inside:1},6,9);
  assert(!c.clipped);assert.equal(g.character.scale,c.scale);assert.equal(g.points.length,0,'observers do not conjure tools');
  assert(Number.isFinite(g.character.x+g.character.y));
 }
});
test('notebook exposes actual curio controls and distinguishes a last reading from certainty',()=>{
 for(const id of items)for(const [core]of KEEPSAKE_CHOICES[id])assert(KEEPSAKE_ROUTINES[core].types.includes(KEEPSAKE_BLUEPRINTS[id].type));
 assert.match(keepsakeSummary('snowglobe',{keepsake:{glass:{energy:.2,pumps:3}}}),/Snow settling.*3 pump strokes/);
 assert.match(keepsakeSummary('crystal_ball',{keepsake:{glass:{vision:{weather:'stormy',biome:'pond'},readings:2}}}),/Last reading: stormy.*Forecasts can change/);
});
test('weather readings do not mistake meteor showers, rainbows or falling leaves for rain',()=>{
 for(const [type,family]of Object.entries({meteor_shower:'night',harvest_moon:'night',double_rainbow:'rainbow',rainbow:'rainbow',leaf_storm:'leaves',crisp:'leaves',first_frost:'frost',ice_storm:'snow',spring_showers:'rain',summer_storm:'rain'}))assert.equal(weatherGlyphFamily(type),family);
});
