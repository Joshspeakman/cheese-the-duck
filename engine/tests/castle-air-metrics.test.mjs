import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {AIR_ATOMICS,airMetricSprite,exportCastleAirMetrics} from '../scripts/export-castle-air-metrics.mjs';
import {CASTLE_SCORES,castlePose} from '../client/castle-care.mjs';
import {CASTLE_DIAL,CASTLE_FABRIC_OCCLUDERS} from '../client/castle-air-geometry.mjs';
import {ObjectCanvas} from '../client/object-canvas.mjs';
import {softCastle,surfaceState} from '../client/soft-surfaces.mjs';
import {castleState} from '../client/castle-care.mjs';
import {flightInkBounds} from '../scripts/export-castle-flight-metrics.mjs';

test('air metrics reproduce exact eight atomic templates without procedure or egg fallback',()=>{
 const actual=exportCastleAirMetrics(),saved=JSON.parse(fs.readFileSync(new URL('../client/animation/castle-air-metrics.json',import.meta.url)));
 assert.deepEqual(actual,saved);assert.equal(Object.keys(actual.ages).length,8);assert.equal(Object.keys(actual.casts).length,47);assert.equal(actual.ages.egg,undefined);
 for(const group of [actual.ages,actual.casts])for(const actor of Object.values(group)){
  assert.deepEqual(Object.keys(actor.routines),AIR_ATOMICS);
  assert.equal(Object.values(actor.routines).flat().length,19);
  for(const [id,events]of Object.entries(actor.routines))for(const [i,event]of events.entries()){
   assert.deepEqual([event.at,event.field,event.value],CASTLE_SCORES[id].effects[i]);
   const stations=CASTLE_SCORES[id].stations||[[0,CASTLE_SCORES[id].station]];
   assert.equal(event.station_index,stations.findLastIndex(([at])=>at<=event.at));assert.equal(event.station,stations[event.station_index][1]);
   assert.ok(event.feet.length>=2);assert.ok(event.feet.every(([,y])=>y===0));
   assert.equal(Object.hasOwn(event,'grip'),event.kind==='contact');assert.equal(Object.hasOwn(event,'eyes'),event.kind==='observation');
  }
 }
});

test('air full ink envelopes contain independently sampled working poses',()=>{
 const metrics=JSON.parse(fs.readFileSync(new URL('../client/animation/castle-air-metrics.json',import.meta.url)));
 const contains=(a,b)=>a.x<=b.x&&a.y<=b.y&&a.x+a.w>=b.x+b.w&&a.y+a.h>=b.y+b.h;
 for(const [key,group]of [['stage',metrics.ages],['cast',metrics.casts]])for(const [actor,entry]of Object.entries(group))for(const id of AIR_ATOMICS)for(const facing of [true,false])for(const progress of [...[.0271,.1739,.3297,.5163,.6811,.9387],...CASTLE_SCORES[id].track.slice(1).flatMap(([end],i)=>[.25,.5,.75].map(u=>CASTLE_SCORES[id].track[i][0]+u*(end-CASTLE_SCORES[id].track[i][0])))]){
  const c=airMetricSprite({[key]:actor,id,facing,progress}),b=flightInkBounds(c);b.x+=c.offsetX||0;b.y+=(c.offsetY||0)/1.5;
  assert.ok(contains(entry.by_score[id].body,b),`${actor} ${id}`);assert.ok(contains(entry.travel.body,b));
 }
});

test('air raster padding exceeds authored per-sample interpolation displacement',()=>{
 // scalePose uses at most x*2.6, y*1.8 and b*2; working wing reach
 // uses *2, while the ordinary wing gesture uses at most *6. Smoothstep's
 // maximum derivative is 1.5. Track endpoints are sampled explicitly.
 for(const id of AIR_ATOMICS){const track=CASTLE_SCORES[id].track;for(let i=1;i<track.length;i++){
  const [a,p]=track[i-1],[b,q]=track[i],delta=k=>Math.abs((p[k]||0)-(q[k]||0));
  const displacement=1.5*.01/(b-a)*Math.max(2.6*delta('x'),1.8*delta('y')+2*delta('b'),2*delta('reach')+2*delta('b'),6*delta('w'));
  assert.ok(displacement<1,`${id} interval ${i} needs a larger envelope margin`);
 }}
});

test('dial uses actual needle ink and fabric construction bounds leave its low panel clear',()=>{
 const inBox=(b,x,y)=>x>=b.x&&x<b.x+b.w&&y>=b.y&&y<b.y+b.h;
 assert.ok(!CASTLE_FABRIC_OCCLUDERS.some(b=>inBox(b,...CASTLE_DIAL.needle_center)));
 for(let i=0;i<=40;i++){
  const inflation=i/40,c=new ObjectCanvas(180,150);
  softCastle(c,{w:180,h:150},{inflation,surface:surfaceState({a:{press:1,u:.3},b:{press:1,u:-.2}}),castle:castleState({apron:inflation,flag:1-inflation,door:inflation})});
  const [x,y]=CASTLE_DIAL.needle_origin;assert.notEqual(c.art[y][x],' ');assert.equal(c.tones[y][x],'a');
  for(const fill of c.fills.filter(f=>f.tone!=='m'))for(let x=fill.x;x<fill.x+fill.w;x++)assert.ok(CASTLE_FABRIC_OCCLUDERS.some(b=>inBox(b,x,fill.y)),`unbounded fabric ${x},${fill.y}`);
 }
});

test('gauge observation eyes are actual open visible ink in each motion mode',()=>{
 const metrics=JSON.parse(fs.readFileSync(new URL('../client/animation/castle-air-metrics.json',import.meta.url)));
 for(const [key,group]of [['stage',metrics.ages],['cast',metrics.casts]])for(const [actor,value]of Object.entries(group))for(const motion of [true,false]){
  const request={[key]:actor,id:'castle_gauge_check',index:0,motion},before=structuredClone(request),c=airMetricSprite(request),m=value.routines.castle_gauge_check[0];
  assert.deepEqual(request,before);
  const expected=[];for(let y=0;y<c.art.length;y++)for(let x=0;x<c.art[y].length;x++)if(c.tones[y][x]==='e'&&![' ','-','_'].includes(c.art[y][x]))expected.push([x+.5-c.anchorX+(c.offsetX||0),y+.5-c.groundRow+(c.offsetY||0)/1.5]);
  assert.ok(expected.length);assert.deepEqual(m.eyes[motion?'normal':'reduced'],expected);assert.equal(m.grip,undefined);
 }
});

test('grille sweep raises the actual attached wing tip while every support pad remains grounded',()=>{
 const metrics=JSON.parse(fs.readFileSync(new URL('../client/animation/castle-air-metrics.json',import.meta.url)));
 for(const [key,group]of [['stage',metrics.ages],['cast',metrics.casts]])for(const [actor,entry]of Object.entries(group))for(const [index,m]of entry.routines.castle_grill_clean.entries())for(const motion of [true,false]){
  const c=airMetricSprite({[key]:actor,id:'castle_grill_clean',index,motion}),pose=castlePose({id:'castle_grill_clean',stage:'service',ride_elapsed:m.at*CASTLE_SCORES.castle_grill_clean.duration});
  assert.equal(c.art[c.grip.y][c.grip.x],')');assert.equal(c.tones[c.grip.y][c.grip.x],'w');
  assert.ok(c.rig.feet.every(f=>f.y+.5-c.groundRow===0));assert.equal(c.scale,m.scale);
  assert.equal(pose.workLift>0,m.station==='grill');if(m.station==='grill')assert.ok(pose.workLift>=3&&pose.workLift<=5);
  assert.deepEqual(m.grip,[c.grip.x+.5-c.anchorX,c.grip.y+.5-c.groundRow]);
 }
});
