// Export actual adult authored contact grips; native mechanics never guess a rig pose.
import fs from 'node:fs';
import {CASTLE_SCORES,castlePose} from '../client/castle-care.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
const routines={};
for(const id of ['castle_start','castle_door_open','castle_hose_stow']){
 const spec=CASTLE_SCORES[id];
 routines[id]=spec.effects.map(([at,field,value])=>{
  const work={id,stage:'service',clock:at*spec.duration,ride_elapsed:at*spec.duration};
  const station=castlePose(work).station;
  const sample=(motion,native=true)=>{const c=characterSprite({stage:'adult',state:'idle',facing:true,performance:{kind:'carnival',routine:native?{...work,physical_pilot:true,physical:{version:1,actor:'cheese',phase:'hold',station,root:[0,0],target:[0,0],contact_ready:true}}:work,role:'a',motion}},0);return {grip:[c.grip.x+.5-c.anchorX,c.grip.y+.5-c.groundRow],scale:c.scale,anchorX:c.anchorX,groundRow:c.groundRow,feet:c.rig.feet.map(f=>[f.x+.5-c.anchorX,f.y+.5-c.groundRow])};};
  const actual=sample(true);if(JSON.stringify(actual)!==JSON.stringify(sample(false)))throw Error(id+' Reduced Motion grip differs');
  if(JSON.stringify(actual)!==JSON.stringify(sample(true,false)))throw Error(id+' native and legacy contact geometry differs');
  return {at,field,value,station,...actual};
 });
}
const output=JSON.stringify({schema_version:1,actor:'adult-cheese',role:'a',facing:'right',reach_cells:3,routines},null,2)+'\n';
const path=new URL('../client/animation/castle-contact-metrics.json',import.meta.url);
if(process.argv.includes('--check')){if(fs.readFileSync(path,'utf8')!==output)throw Error('Castle contact metrics are stale');}
else fs.writeFileSync(path,output);
console.log('Castle contact metrics: 9 authored contacts validated');
