import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import {characterSprite} from '../client/ultra-characters.mjs';
import {eggShellSampleTimes,eggShellGeometry} from './egg-shell-samples.mjs';
import {GUEST_CAST} from '../client/guest-cast.mjs';
import {CASTLE_SCORES} from '../client/castle-care.mjs';
import {SHARED_CAST_IDS,guestWalkingTime} from './export-castle-guest-metrics.mjs';
import {flightInkBounds} from './export-castle-flight-metrics.mjs';
import {eggCaregiverWork,caregiverSignatureTimes} from './egg-caregiver-samples.mjs';
function union(boxes){const x=Math.min(...boxes.map(b=>b.x)),y=Math.min(...boxes.map(b=>b.y));return {x,y,w:Math.max(...boxes.map(b=>b.x+b.w))-x,h:Math.max(...boxes.map(b=>b.y+b.h))-y};}
export function exportEggCaregiverMetrics(){
 const times=eggShellSampleTimes(),facings={},all=[];
 for(const facing of [true,false]){
  const poses=[];
  for(const motion of [true,false])for(const time of times){
   const source={stage:'egg',state:'idle',facing,motion},before=JSON.stringify(source),c=characterSprite(source,motion?time:0);if(JSON.stringify(source)!==before)throw Error('Egg source mutated');poses.push(eggShellGeometry(c));
  }
  const value=Object.fromEntries(['body','shell','shell_base'].map(key=>[key,union(poses.map(p=>p[key]))]));facings[facing?'right':'left']={anchorX:facing?36:39,...value};all.push(...poses);
 }
 return {schema_version:1,actor:'cheese',stage:'egg',kind:'stationary-shell-envelope',scale:.66,groundRow:39.5,appearance:'original-egg',motion_modes:['normal','reduced'],sampling:{method:'all-eight-shell-phases-and-analytic-idle-offset-extrema',time_samples:times.length,offset_divisor:1.5},facings,...Object.fromEntries(['body','shell','shell_base'].map(key=>[key,union(all.map(p=>p[key]))])),caregivers:exportCaregiverEnvelopes()};
}
export function exportCaregiverEnvelopes(){
 const caregivers={};
 for(const cast of SHARED_CAST_IDS){
  const profile=GUEST_CAST[cast],poses=[],base=characterSprite({castId:cast,state:'idle'},0,true);
  function sample(c,idle=false){if(c.clipped||c.profileId!==cast||c.scale!==base.scale)throw Error('Invalid caregiver anatomy '+cast);const b=flightInkBounds(c);if(idle){b.y-=.1/1.5;b.h+=.2/1.5;}else b.y+=(c.offsetY||0)/1.5;poses.push(b);}
  for(const facing of [true,false]){
   sample(characterSprite({castId:cast,state:'idle',facing},0,true),true);
   for(const t of caregiverSignatureTimes(profile))sample(characterSprite({castId:cast,state:'signature',facing},t,true),true);
   for(let phase=0;phase<8;phase++)sample(characterSprite({castId:cast,state:'walking',facing},guestWalkingTime(profile,phase),true));
   for(const motion of [true,false])for(const id of ['castle_start','castle_door_open','castle_hose_stow'])for(let step=0;step<=100;step++)sample(characterSprite({castId:cast,facing,performance:{kind:'carnival',routine:eggCaregiverWork(cast,id,step/100*CASTLE_SCORES[id].duration),role:'a',motion}},0,true));
  }
  caregivers[cast]={scale:base.scale,body:union(poses),samples:poses.length,states:['idle','signature','walking','working'],facings:['right','left'],appearance:'authored-visitor-profile'};
 }
 return caregivers;
}
if(process.argv[1]===fileURLToPath(import.meta.url)){
 const output=JSON.stringify(exportEggCaregiverMetrics(),null,2)+'\n',path=new URL('../client/animation/egg-caregiver-metrics.json',import.meta.url);
 if(process.argv.includes('--check')){if(fs.readFileSync(path,'utf8')!==output)throw Error('Egg caregiver metrics stale');}else fs.writeFileSync(path,output);
 console.log('Original egg full-shell and bottom-shell support validated; no invented rig contacts');
}
