// Geometry for atomic air-supply work. Procedure occurrences reuse these exact
// templates; this file does not adopt scores or grant mechanical completion.
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import {DUCK_AGES} from '../client/duck-designs.mjs';
import {CASTLE_SCORES} from '../client/castle-care.mjs';
import {SHARED_CAST_IDS} from './export-castle-guest-metrics.mjs';
import {CASTLE_DIAL,CASTLE_FABRIC_OCCLUDERS} from '../client/castle-air-geometry.mjs';
import {flightInkBounds} from './export-castle-flight-metrics.mjs';
import FLIGHT from '../client/animation/castle-flight-metrics.json' with {type:'json'};
import EGG from '../client/animation/egg-caregiver-metrics.json' with {type:'json'};
import GUEST from '../client/animation/castle-guest-metrics.json' with {type:'json'};

export {AIR_ATOMICS,airMetricSprite,visibleEyes} from './castle-air-samples.mjs';
import {AIR_ATOMICS,airMetricSprite,visibleEyes} from './castle-air-samples.mjs';
function anatomy(c){
 if(c.clipped||!c.rig?.feet?.length)throw Error('Invalid air operator anatomy');
 return {scale:c.scale,anchorX:c.anchorX,groundRow:c.groundRow,feet:c.rig.feet.map(f=>[f.x+.5-c.anchorX,f.y+.5-c.groundRow])};
}
function routines(actor){
 return Object.fromEntries(AIR_ATOMICS.map(id=>{
  const spec=CASTLE_SCORES[id],stations=spec.stations||[[0,spec.station]];
  return [id,spec.effects.map(([at,field,value],index)=>{
   const station_index=stations.findLastIndex(([start])=>start<=at),station=stations[station_index][1],observation=field==='inspection';
   const c=airMetricSprite({...actor,id,index}),metric={at,field,value,station,station_index,kind:observation?'observation':'contact',...anatomy(c)};
   if(observation)metric.eyes={normal:visibleEyes(c),reduced:visibleEyes(airMetricSprite({...actor,id,index,motion:false}))};
   else {if(!c.grip)throw Error(id+' missing actual grip');metric.grip=[c.grip.x+.5-c.anchorX,c.grip.y+.5-c.groundRow];}
   for(const motion of [true,false])for(const native of [true,false]){
    const other=airMetricSprite({...actor,id,index,motion,native});
    if(JSON.stringify(anatomy(c))!==JSON.stringify(anatomy(other)))throw Error(id+' support differs by motion/native mode');
    if(observation){if(JSON.stringify(metric.eyes[motion?'normal':'reduced'])!==JSON.stringify(visibleEyes(other)))throw Error(id+' visible eye differs by native mode');}
    else if(JSON.stringify(metric.grip)!==JSON.stringify([other.grip.x+.5-other.anchorX,other.grip.y+.5-other.groundRow]))throw Error(id+' grip differs by motion/native mode');
   }
   return metric;
  })];
 }));
}
function union(boxes){const x=Math.min(...boxes.map(b=>b.x)),y=Math.min(...boxes.map(b=>b.y));return {x,y,w:Math.max(...boxes.map(b=>b.x+b.w))-x,h:Math.max(...boxes.map(b=>b.y+b.h))-y};}
function envelopes(actor){
 const byScore={},base=actor.cast?EGG.caregivers[actor.cast]:FLIGHT.operators[actor.stage],travel=actor.cast?GUEST.casts[actor.cast].travel:GUEST.observers[actor.stage].travel;
 for(const id of AIR_ATOMICS){
  const boxes=[],feet=[],times=new Set(CASTLE_SCORES[id].track.map(([at])=>at));
  for(let n=0;n<=100;n++)times.add(n/100);
  for(const progress of times)for(const facing of [true,false])for(const motion of [true,false]){
   const c=airMetricSprite({...actor,id,progress,facing,motion}),box=flightInkBounds(c);box.x+=c.offsetX||0;box.y+=(c.offsetY||0)/1.5;boxes.push(box);
   if(c.clipped)throw Error(id+' clipped air pose');
   for(const f of c.rig.feet)feet.push([(facing?f.x:c.width-1-f.x)+.5-c.anchorX,f.y+.5-c.groundRow]);
  }
  const body=union(boxes);
  // Authored smoothstep tracks interpolate bounded sub-cell changes between
  // these samples; one cell encloses raster threshold changes on every side.
  body.x--;body.y--;body.w+=2;body.h+=2;
  byScore[id]={scale:base.scale,body,feet:[...new Map(feet.map(p=>[JSON.stringify(p),p])).values()],facings:['right','left'],motion_modes:['normal','reduced'],raster_margin:1,samples:boxes.length};
 }
 return {by_score:byScore,travel:{scale:base.scale,body:union([base.body,...Object.values(byScore).map(e=>e.body)]),feet:[...new Map([...travel.feet,...Object.values(byScore).flatMap(e=>e.feet)].map(p=>[JSON.stringify(p),p])).values()]}};
}
export function exportCastleAirMetrics(){
 const entry=actor=>({routines:routines(actor),...envelopes(actor)});
 return {schema_version:1,role:'a',facing:'right',reach_cells:3,observation:{units:'object-art-grid',dial:CASTLE_DIAL,occluders:CASTLE_FABRIC_OCCLUDERS},ages:Object.fromEntries(DUCK_AGES.filter(a=>a.id!=='egg').map(({id:stage})=>[stage,entry({stage})])),casts:Object.fromEntries(SHARED_CAST_IDS.map(cast=>[cast,entry({cast})]))};
}
if(process.argv[1]===fileURLToPath(import.meta.url)){
 const output=JSON.stringify(exportCastleAirMetrics(),null,2)+'\n',path=new URL('../client/animation/castle-air-metrics.json',import.meta.url);
 if(process.argv.includes('--check')){if(fs.readFileSync(path,'utf8')!==output)throw Error('Air metrics are stale');}else fs.writeFileSync(path,output);
 console.log('Air metrics: eight atomic templates for eight hatched ages and 47 exact operators');
}
