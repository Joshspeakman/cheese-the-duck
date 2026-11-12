// Airborne geometry only. Flutter has no ground pads or operating grip.
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import {DUCK_AGES} from '../client/duck-designs.mjs';
import {CASTLE_SCORES,castlePose} from '../client/castle-care.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
const cast='butterfly_fairy';
import {flightWork,flightSampleTimes} from './castle-flight-samples.mjs';
export {flightWork,flightSampleTimes};
export function flightInkBounds(c){
 const cells=[];c.art.forEach((row,y)=>[...row].forEach((ch,x)=>{if(ch!==' ')cells.push({x,y,w:1});}));cells.push(...c.fills);
 const x=Math.min(...cells.map(p=>p.x))-c.anchorX,y=Math.min(...cells.map(p=>p.y))-c.groundRow;
 return {x,y,w:Math.max(...cells.map(p=>p.x+p.w))-c.anchorX-x,h:Math.max(...cells.map(p=>p.y+1))-c.groundRow-y};
}
function union(bounds){const x=Math.min(...bounds.map(b=>b.x)),y=Math.min(...bounds.map(b=>b.y));return {x,y,w:Math.max(...bounds.map(b=>b.x+b.w))-x,h:Math.max(...bounds.map(b=>b.y+b.h))-y};}
export function flightOperatorMetrics(){
 const operators={};
 for(const {id:stage,pace}of DUCK_AGES.filter(a=>a.id!=='egg')){
  const samples=[],base=characterSprite({stage,state:'idle'},0);
  for(const facing of [true,false]){
   samples.push(flightInkBounds(characterSprite({stage,state:'idle',facing},0)));
   for(let phase=0;phase<8;phase++)samples.push(flightInkBounds(characterSprite({stage,state:'walking',facing},(phase+.1)*4.5/(pace*5))));
   for(const motion of [true,false])for(const id of ['castle_start','castle_door_open','castle_hose_stow'])for(let step=0;step<=100;step++){
    const routine=flightWork(id);routine.shared.source_age=routine.shared.operator.source_age=stage;routine.clock=routine.ride_elapsed=step/100*CASTLE_SCORES[id].duration;routine.physical.station=castlePose({id,stage:'service',clock:routine.clock,ride_elapsed:routine.clock}).station;
    const c=characterSprite({stage,facing,performance:{kind:'carnival',routine,role:'a',motion}},0);if(c.clipped||c.scale!==base.scale)throw Error('Invalid flight operator geometry');samples.push(flightInkBounds(c));
   }
  }
  operators[stage]={scale:base.scale,anchorX:base.anchorX,groundRow:base.groundRow,body:union(samples),samples:samples.length,appearance:'unequipped'};
 }
 return operators;
}
export function exportCastleFlightMetrics(){
 const times=flightSampleTimes(),bounds=[];let samples=0,scale,anchorX,groundRow;
 const performances=[null,...[false,true].map(react=>({kind:'carnival',routine:flightWork('castle_start',0,react),role:'b',watch:true}))];
 for(const facing of [true,false])for(const motion of [true,false])for(const performance of performances)for(const time of times){
  const c=characterSprite({id:cast,castId:cast,state:'walking',facing,performance:performance&&{...performance,motion}},motion?time:0,true);
  if(c.profileId!==cast||c.grip||c.rig.feet.length||c.clipped)throw Error('Invalid Flutter flight anatomy');
  scale??=c.scale;anchorX??=c.anchorX;groundRow??=c.groundRow;if(c.scale!==scale||c.groundRow!==groundRow)throw Error('Flight changes scale/root');bounds.push(flightInkBounds(c));samples++;
 }
 const x=Math.min(...bounds.map(b=>b.x)),y=Math.min(...bounds.map(b=>b.y));
 return {schema_version:1,operators:flightOperatorMetrics(),kind:'airborne-envelope',actor:cast,cast,scale,anchorX,groundRow,facings:['right','left'],states:['flight','watch','consumed-effect-attention'],motion_modes:['normal','reduced'],sampling:{method:'raster-boundaries-and-intervals',period:2*Math.PI,time_samples:times.length,samples},body:{x,y,w:Math.max(...bounds.map(b=>b.x+b.w))-x,h:Math.max(...bounds.map(b=>b.y+b.h))-y}};
}
if(process.argv[1]===fileURLToPath(import.meta.url)){
 const output=JSON.stringify(exportCastleFlightMetrics(),null,2)+'\n',path=new URL('../client/animation/castle-flight-metrics.json',import.meta.url);
 if(process.argv.includes('--check')){if(fs.readFileSync(path,'utf8')!==output)throw Error('Flight metrics stale');}else fs.writeFileSync(path,output);
 console.log('Flutter actual airborne envelope validated; no feet or operator grip');
}
