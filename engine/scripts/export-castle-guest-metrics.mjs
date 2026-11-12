// Exact regular visitors only. The export is geometry, not operator adoption.
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import {DUCK_AGES} from '../client/duck-designs.mjs';
import {GUEST_CAST} from '../client/guest-cast.mjs';
import {CASTLE_SCORES,castlePose} from '../client/castle-care.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
export const REGULAR_CAST_IDS=Object.values(GUEST_CAST).filter(p=>p.id.startsWith('friend:')&&!p.rare&&p.species==='duck').map(p=>p.id);
function support(c,mirrored=false){
 if(c.clipped||!c.rig?.feet?.length)throw Error('Missing or clipped guest support: '+c.profileId);
 return {scale:c.scale,anchorX:c.anchorX,groundRow:c.groundRow,feet:c.rig.feet.map(f=>[(mirrored?c.width-1-f.x:f.x)+.5-c.anchorX,f.y+.5-c.groundRow]),body:{x:(mirrored?c.width-c.rig.body.x-c.rig.body.w:c.rig.body.x)-c.anchorX,y:c.rig.body.y-c.groundRow,w:c.rig.body.w,h:c.rig.body.h}};
}
function supportUnion(samples,states){
 const {scale,anchorX,groundRow}=samples[0],left=Math.min(...samples.map(m=>m.body.x)),top=Math.min(...samples.map(m=>m.body.y));
 if(samples.some(m=>m.scale!==scale||m.groundRow!==groundRow))throw Error('Travel changed native rig scale or ground');
 const feet=[...new Map(samples.flatMap(m=>m.feet).map(f=>[JSON.stringify(f),f])).values()];
 return {kind:'support-union',facings:['right','left'],states,samples:samples.length,scale,anchorX,groundRow,feet,body:{x:left,y:top,w:Math.max(...samples.map(m=>m.body.x+m.body.w))-left,h:Math.max(...samples.map(m=>m.body.y+m.body.h))-top}};
}
export function exportCastleGuestMetrics(){
 if(REGULAR_CAST_IDS.length!==40)throw Error('Regular guest export scope changed; review exact identities');
 const casts={};
 for(const cast of REGULAR_CAST_IDS){
  const profile=GUEST_CAST[cast],actor='metric-operator',duck={id:actor,castId:cast,name:profile.name,stage:'adult',state:'idle',facing:true};
  const idle=support(characterSprite(duck,0,true));
  if(JSON.stringify(idle)!==JSON.stringify(support(characterSprite({...duck,motion:false},0,true))))throw Error(cast+' idle support differs in Reduced Motion');
  const travelSamples=[];
  for(const facing of [true,false]){
   travelSamples.push(support(characterSprite({...duck,facing},0,true),!facing));
   for(let phase=0;phase<8;phase++)travelSamples.push(support(characterSprite({...duck,facing,state:'walking'},(phase+.1)*4.5/(profile.pace*5),true),!facing));
  }
  const travel=supportUnion(travelSamples,['idle','walking']),routines={};casts[cast]={idle,travel,routines};
  for(const id of ['castle_start','castle_door_open','castle_hose_stow']){
   const spec=CASTLE_SCORES[id];routines[id]=spec.effects.map(([at,field,value])=>{
    const work={id,stage:'service',clock:at*spec.duration,ride_elapsed:at*spec.duration},station=castlePose(work).station;
    const sample=(motion,native)=>{
     const routine=native?{...work,shared_physical:true,physical_pilot:false,shared:{version:1,attempt:'metric-export',operator:{actor,cast,adapter:'regular',token:'metric-token',location:'Home Pond'},source_age:'adult',phase:'operate',cheese:{root:[0,0],stance:[0,0],exit:[0,0],phase:'hold',ready:true}},physical:{version:1,actor,phase:'hold',station,root:[0,0],target:[0,0],contact_ready:true}}:work;
     const c=characterSprite({...duck,performance:{kind:'carnival',routine,role:'a',motion}},0,true);
     if(c.profileId!==cast||!c.grip)throw Error(cast+' has no exact operator grip');
     const {body,...stance}=support(c),metric={...stance,grip:[c.grip.x+.5-c.anchorX,c.grip.y+.5-c.groundRow]};
     if(![metric.scale,metric.anchorX,metric.groundRow,...metric.grip,...metric.feet.flat()].every(Number.isFinite))throw Error(cast+' nonfinite geometry');
     return metric;
    };
    const actual=sample(true,true);
    for(const [motion,native]of [[false,true],[true,false],[false,false]])if(JSON.stringify(actual)!==JSON.stringify(sample(motion,native)))throw Error(`${cast} ${id} contact differs (motion=${motion}, native=${native})`);
    return {at,field,value,station,...actual};
   });
  }
 }
 const observers={};
 for(const {id:stage,pace}of DUCK_AGES.filter(a=>a.id!=='egg')){
  const idle=support(characterSprite({stage,state:'idle',facing:true},0)),travelSamples=[];
  for(const facing of [true,false]){travelSamples.push(support(characterSprite({stage,state:'idle',facing},0),!facing));for(let phase=0;phase<8;phase++)travelSamples.push(support(characterSprite({stage,state:'walking',facing},(phase+.1)*4.5/(pace*5)),!facing));}
  for(const id of ['castle_start','castle_door_open','castle_hose_stow'])for(const [index,[at]]of CASTLE_SCORES[id].effects.entries())for(const facing of [true,false])for(const motion of [true,false]){
   const duration=CASTLE_SCORES[id].duration,base={id,stage:'service',ride_elapsed:at*duration,clock:at*duration},station=castlePose(base).station;
   const routine={...base,shared_physical:true,events:[index],shared:{version:1,attempt:'observer-metrics',operator:{actor:'metric-operator',cast:REGULAR_CAST_IDS[0],adapter:'regular',token:'metric-token',location:'Home Pond'},source_age:stage,phase:'operate',cheese:{root:[0,0],stance:[0,0],exit:[0,0],phase:'hold',ready:true}},physical:{version:1,actor:'metric-operator',phase:'hold',station,root:[0,0],target:[0,0],contact_ready:true}};
   const c=characterSprite({stage,state:'idle',facing,performance:{kind:'carnival',routine,role:'b',watch:true,motion}},0),posed=support(c,!facing);
   travelSamples.push(posed);
   if(JSON.stringify(support(characterSprite({stage,state:'idle',facing},0),!facing))!==JSON.stringify(posed))throw Error(stage+' observer support differs from ordinary idle');
   if(c.grip)throw Error(stage+' observer acquired operator grip');
  }
  observers[stage]={...idle,travel:supportUnion(travelSamples,['idle','walking','watch'])};
 }
 return {schema_version:1,actor:'guest',adapter:'regular',role:'a',facing:'right',reach_cells:3,casts,observers};
}
if(process.argv[1]===fileURLToPath(import.meta.url)){
 const output=JSON.stringify(exportCastleGuestMetrics(),null,2)+'\n',path=new URL('../client/animation/castle-guest-metrics.json',import.meta.url);
 if(process.argv.includes('--check')){if(fs.readFileSync(path,'utf8')!==output)throw Error('Castle guest metrics are stale');}else fs.writeFileSync(path,output);
 console.log('Castle guest metrics: 40 exact regular profiles × 9 authored contacts + idle support + 8 observer supports validated');
}
