// Export actual authored contact geometry for each hatched age. Native mechanics
// must select the reserved age explicitly, never substitute an adult rig.
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import {DUCK_AGES} from '../client/duck-designs.mjs';
import {CASTLE_SCORES,castlePose} from '../client/castle-care.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
export function exportCastleContactMetrics(){
 const ages={};
 for(const {id:stage}of DUCK_AGES.filter(a=>a.id!=='egg')){
  const routines={};ages[stage]={routines};
  for(const id of ['castle_start','castle_door_open','castle_hose_stow']){
   const spec=CASTLE_SCORES[id];
   routines[id]=spec.effects.map(([at,field,value])=>{
    const work={id,stage:'service',clock:at*spec.duration,ride_elapsed:at*spec.duration};
    const station=castlePose(work).station;
    const sample=(motion,native)=>{
     const routine=native?{...work,physical_pilot:true,physical:{version:1,actor:'cheese',source_age:stage,phase:'hold',station,root:[0,0],target:[0,0],contact_ready:true}}:work;
     const c=characterSprite({stage,state:'idle',facing:true,performance:{kind:'carnival',routine,role:'a',motion}},0);
     if(c.clipped||!c.grip||c.rig?.feet.length!==2)throw Error(`${stage} ${id}: invalid operator anatomy`);
     const result={grip:[c.grip.x+.5-c.anchorX,c.grip.y+.5-c.groundRow],scale:c.scale,anchorX:c.anchorX,groundRow:c.groundRow,feet:c.rig.feet.map(f=>[f.x+.5-c.anchorX,f.y+.5-c.groundRow])};
     if(![result.scale,result.anchorX,result.groundRow,...result.grip,...result.feet.flat()].every(Number.isFinite)||result.scale<=0)throw Error(`${stage} ${id}: nonfinite contact geometry`);
     return result;
    };
    const actual=sample(true,true);
    for(const [motion,native]of [[false,true],[true,false],[false,false]])if(JSON.stringify(actual)!==JSON.stringify(sample(motion,native)))throw Error(`${stage} ${id}: contact geometry differs (motion=${motion}, native=${native})`);
    return {at,field,value,station,...actual};
   });
  }
 }
 return {schema_version:2,actor:'cheese',role:'a',facing:'right',reach_cells:3,ages};
}
if(process.argv[1]===fileURLToPath(import.meta.url)){
 const metrics=exportCastleContactMetrics(),output=JSON.stringify(metrics,null,2)+'\n',path=new URL('../client/animation/castle-contact-metrics.json',import.meta.url);
 if(process.argv.includes('--check')){if(fs.readFileSync(path,'utf8')!==output)throw Error('Castle contact metrics are stale');}
 else fs.writeFileSync(path,output);
 console.log(`Castle contact metrics: ${Object.keys(metrics.ages).length} hatched ages × 9 authored contacts validated`);
}
