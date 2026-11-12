import test from 'node:test';
import assert from 'node:assert/strict';
import {characterSprite} from '../client/ultra-characters.mjs';
import {eggShellGeometry} from '../scripts/egg-shell-samples.mjs';
import {exportEggCaregiverMetrics} from '../scripts/export-egg-caregiver-metrics.mjs';
import METRICS from '../client/animation/egg-caregiver-metrics.json' with {type:'json'};
import GUESTS from '../client/animation/castle-guest-metrics.json' with {type:'json'};
import {GUEST_CAST} from '../client/guest-cast.mjs';
import {flightInkBounds} from '../scripts/export-castle-flight-metrics.mjs';
import {eggCaregiverWork} from '../scripts/egg-caregiver-samples.mjs';
import {CASTLE_SCORES} from '../client/castle-care.mjs';
const contains=(outer,inner)=>assert(inner.x>=outer.x-1e-10&&inner.y>=outer.y-1e-10&&inner.x+inner.w<=outer.x+outer.w+1e-10&&inner.y+inner.h<=outer.y+outer.h+1e-10);
test('egg metric reproduces the original shell with separate bottom-shell support and no invented contacts',()=>{
 assert.deepEqual(METRICS,exportEggCaregiverMetrics());assert.equal(METRICS.feet,undefined);assert.equal(METRICS.grip,undefined);assert.equal(METRICS.bill,undefined);
 for(const facing of [true,false])for(const motion of [true,false])for(let i=0;i<500;i++){
  const source={id:'egg-identity',stage:'egg',state:'idle',facing,motion,x:34.25,y:22.75},before=structuredClone(source),c=characterSprite(source,motion?i*.719:0),actual=eggShellGeometry(c),bound=METRICS.facings[facing?'right':'left'];assert.deepEqual(source,before);assert.equal(c.rig,null);assert.equal(c.grip,null);assert.equal(c.bill,null);assert.equal(c.performance,null);
  for(const key of ['body','shell','shell_base']){contains(METRICS[key],actual[key]);contains(bound[key],actual[key]);}
  const bottom=Math.max(...c.fills.map(f=>f.y));for(const f of c.fills.filter(f=>f.y===bottom)){assert(c.art[f.y].slice(f.x,f.x+f.w).includes('-'),'support derives from actual bottom shell ink');}
 }
});
test('Reduced Motion keeps exact source facing and the ordinary phase-zero shell without equipment or gestures',()=>{
 for(const facing of [true,false]){const a=characterSprite({stage:'egg',state:'idle',facing,motion:false,cosmetics:{head:'hat_red'}},0),b=characterSprite({stage:'egg',state:'idle',facing,motion:false},0);assert.deepEqual(a.art,b.art);assert.deepEqual(a.fills,b.fills);assert.deepEqual(a.wearables,[]);assert.equal(a.facing,facing);assert.equal(a.offsetY,0);assert.equal(a.phase,0);assert.equal(a.rig,null);}
});
test('caregiver collision bounds contain actual full profile ink during independent idle, signature, travel and contact samples',()=>{
 assert.deepEqual(Object.keys(METRICS.caregivers),Object.keys(GUESTS.casts));assert.equal(METRICS.caregivers.butterfly_fairy,undefined);
 for(const cast of Object.keys(GUESTS.casts))for(const facing of [true,false]){
  const box=METRICS.caregivers[cast].body;
  for(const state of ['idle','signature','walking'])for(let i=0;i<80;i++){
   const c=characterSprite({castId:cast,name:GUEST_CAST[cast].name,state,facing},i*.719,true),b=flightInkBounds(c);b.y+=(c.offsetY||0)/1.5;contains(box,b);
  }
  for(const id of Object.keys(CASTLE_SCORES).filter(id=>['castle_start','castle_door_open','castle_hose_stow'].includes(id)))for(const [at]of CASTLE_SCORES[id].effects)for(const motion of [true,false]){
   const c=characterSprite({castId:cast,facing,performance:{kind:'carnival',routine:eggCaregiverWork(cast,id,at*CASTLE_SCORES[id].duration),role:'a',motion}},0,true);contains(box,flightInkBounds(c));
  }
 }
});
