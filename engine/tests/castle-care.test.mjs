import test from 'node:test';import assert from 'node:assert/strict';
import {CASTLE_SCORES as scores,castlePose,castleGeometry,castleStation} from '../client/castle-care.mjs';
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';import {characterSprite} from '../client/ultra-characters.mjs';import {GUEST_CAST} from '../client/guest-cast.mjs';
const boundProcedures=new Set(['castle_pressure_check','castle_dust_service']);
const ages=['hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'];
const actors=[...ages.map(stage=>({stage})),...Object.values(GUEST_CAST).map(g=>({id:g.id,castId:g.id,name:g.name,visitor:true}))];
const work=(id,p=.5)=>({id,castle_care:true,stage:'service',clock:scores[id].duration*p,ride_elapsed:scores[id].duration*p});
const home=(state={})=>({...itemSprite('bounce_house',0,{state}),x:100,y:80,scale:itemWorldScale('bounce_house')});
test('source control templates retain station geometry; adopted procedures require a bound occurrence',()=>{
 assert.equal(Object.keys(scores).length,34);const signatures=new Set();
 for(const [id,s]of Object.entries(scores)){
  signatures.add(JSON.stringify([s.station,s.track,s.effects]));assert(home().anchors.controls[s.station]);assert(home().anchors.controls[s.partner]);
  if(boundProcedures.has(id)){assert.equal(castlePose(work(id)),null);continue;}
  for(const [at,field,value]of s.effects){const w=work(id,at),pose=castlePose(w),where=castleStation(w);assert(pose.contact>=1-1e-9,id+' effect at contact '+pose.contact);assert.equal(where.travel,1,'no control turns while crossing between stations');const station={motor:'switch',vent:'valve',door:'door',latch:'buckle',flag:'flag_rope',hose:'hose',kink:'hose',dust_fraction:'grill',mesh_fraction:'door',roof_fraction:'drain',prints_fraction:'apron',inspection:value==='pressure'?'gauge':'seam'}[field]||field;assert.equal(where.name,station,id+' touches the actual '+field);}
  for(let n=0;n<=100;n++)for(const role of ['a','b']){const pose=castlePose(work(id,n/100),role);assert(['x','y','w','b','reach','contact'].every(k=>Number.isFinite(pose[k])));assert(!pose.seated);}
 }
 assert.equal(signatures.size,34);
});
test('source rigs retain scale and wing continuity; gauge inspection never creates a mechanical bridge',()=>{
 for(const actor of actors)for(const id of Object.keys(scores).filter(id=>!boundProcedures.has(id)))for(const role of ['a','b']){
  const w=work(id,.5),h=home(),watch=actor.id==='butterfly_fairy';
  const c={...characterSprite({...actor,facing:role==='a',state:'idle',performance:{kind:'carnival',routine:w,role,watch}},0,actor.visitor),x:122,y:80};
  const saved=JSON.stringify({w,h,c}),g=castleGeometry(h,{character:c,work:w,role,watch},6,9);
  assert(!c.clipped,(actor.id||actor.stage)+' '+id);assert(c.art.every(r=>/^[ -~]*$/.test(r)));assert.equal(g.character.scale,c.scale);assert.equal(JSON.stringify({w,h,c}),saved);
  assert(Number.isFinite(g.character.x+g.character.y));
  if(watch){assert.equal(g.points.length,0);assert(g.character.y*9<g.ground);continue;}
  assert(Math.abs(g.character.y*9-g.ground)<1e-7,'feet stay on the ground');
  if(id==='castle_gauge_check'){assert.equal(g.tip,null);assert.deepEqual(g.points,[]);}
  else if(g.pose.contact>=1-1e-99){assert(g.tip);assert(Math.hypot(g.tip.x-g.target.x,g.tip.y-g.target.y)<1e-7,'wing ends at actual low component');}
  if(g.points.length)assert(Math.hypot(g.points[0].x-g.hand.x,g.points[0].y-g.hand.y)<1e-7,'contact grows out of the wing');
 }
});
test('persistent controls visibly move separate mechanisms and stay bounded in extreme material states',()=>{
 const idle=home({castle:{powered:false,fan:0}});
 for(const [key,value]of Object.entries({door:1,latch:1,vent:1,tie_left:0,tie_right:0,apron:1,flag:0,hose:1,kink:1,dust:1,mesh_wet:1,roof_water:1,prints:1})){
  assert.notDeepEqual(home({castle:{[key]:value}}).art,idle.art,key+' has distinct physical art');
 }
 for(let n=0;n<100;n++){
  const state={castle:{door:n/99,latch:n%2,vent:n/99,tie_left:n/99,tie_right:1-n/99,apron:n/99,flag:1-n/99,hose:n/99,kink:n/99,dust:1,mesh_wet:1,roof_water:1,prints:1,powered:true,fan:n,spray:1,stroke:n/99},excursion:{phase:0,wind_phase:0,wind:.4,inflation:n/99*.85+.15,surface:{}}},m=home(state);
  assert(!m.clipped,'material range '+n);assert(m.art.every(r=>/^[ -~]*$/.test(r)));assert(m.fills.every(f=>f.x>=0&&f.y>=0&&f.x+f.w<=m.width&&f.y<m.art.length));
  assert.deepEqual(m.art,itemSprite('bounce_house',900,{state}).art,'saved fan/material state owns animation');
 }
});
test('work exits reverse their entrance without resizing, and accessibility leaves the contact intact',()=>{
 for(const id of Object.keys(scores).filter(id=>!boundProcedures.has(id))){
  const w=work(id,.4),h=home(),c={...characterSprite({stage:'adult',state:'idle',performance:{kind:'carnival',routine:w,role:'a'}},0),x:122,y:80};
  const p=castlePose(w,'a',false);assert.equal(p.contact,castlePose(w).contact);assert.equal(p.x,0);
  for(let n=0;n<=20;n++){
   const entry={...w,clock:n/20*(scores[id].entryDuration??scores[id].duration*.14)},exit={...w,stage:'service_exit',clock:(1-n/20)*4};
   const a=castleGeometry(h,{character:c,work:entry,role:'a'},6,9),b=castleGeometry(h,{character:c,work:exit,role:'a'},6,9);
   assert(Math.abs(a.character.x-b.character.x)+Math.abs(a.character.y-b.character.y)<1e-7);
  }
 }
});
