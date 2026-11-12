// A read-only geometric review, not an age adoption or repertoire certificate.
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {DUCK_AGES} from '../client/duck-designs.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {CASTLE_SCORES,castlePose} from '../client/castle-care.mjs';
import {castleArtWorld} from '../client/castle-projection.mjs';
import GEOMETRY from '../client/animation/castle-geometry.json' with {type:'json'};
export const REVIEW_SCORES=['castle_start','castle_door_open','castle_hose_stow'];
export function sampleAge(stage,id,index,motion=true){
 const spec=CASTLE_SCORES[id],[at,field,value]=spec.effects[index],work={id,stage:'service',clock:at*spec.duration,ride_elapsed:at*spec.duration},station=castlePose(work).station;
 const c=characterSprite({stage,state:'idle',facing:true,performance:{kind:'carnival',role:'a',motion,routine:{...work,physical_pilot:true,physical:{version:1,actor:'cheese',phase:'hold',station,root:[0,0],target:[0,0],contact_ready:true}}}},0);
 return {id,index,at,field,value,station,scale:c.scale,anchorX:c.anchorX,groundRow:c.groundRow,grip:c.grip?[c.grip.x+.5-c.anchorX,c.grip.y+.5-c.groundRow]:null,feet:c.rig?.feet.map(f=>[f.x+.5-c.anchorX,f.y+.5-c.groundRow])??null,clipped:c.clipped,art:c.art};
}
export function reach(metric,root,target){const bx=metric.scale*132/192,by=metric.scale*42/47;return Math.hypot((target[0]-root[0])/bx-metric.grip[0],(target[1]-root[1])/by-metric.grip[1]);}
export function buildReview(){
 const requests=[],groups=[],report={status:'review-only',reachCap:3,assumptions:['Right-facing solo poses at authored effect times; native adoption remains adult-only.','Home Pond fixtures at habitat (9,7) and (9,6), with no other placed items.','Native PondLayout checks the existing conservative 6x4 stance footprint; that footprint is not an approved age-specific policy.','Actual age-specific foot coordinates must be dry and on the root ground row.','Integer roots searched across native x=2..124, from ceil(castle ground) through y=37.','A common stance must reach all effects at its station; routes, actors, weather, ownership and lifecycle are not certified.'],ages:[]};
 for(const age of DUCK_AGES){
  const metrics=REVIEW_SCORES.flatMap(id=>CASTLE_SCORES[id].effects.map((_,i)=>sampleAge(age.id,id,i)));
  for(const m of metrics){const reduced=sampleAge(age.id,m.id,m.index,false);for(const key of ['scale','anchorX','groundRow','grip','feet'])if(JSON.stringify(m[key])!==JSON.stringify(reduced[key]))throw Error(age.id+' motion metrics differ: '+key);if(m.clipped)throw Error(age.id+' clipped');}
  const a={age:age.id,role:age.id==='egg'?'observer-only proposal; no implemented participation':'operator geometry review only',metrics:metrics.map(({art,...m})=>m),previewArt:metrics[0].art,placements:[]};report.ages.push(a);
  if(age.id==='egg'){if(metrics.some(m=>m.grip||m.feet))throw Error('Egg acquired operator anatomy');continue;}
  for(const center of [[59.4,24.5],[59.4,21]]){
   const placement={center,ground:castleArtWorld(center,0,GEOMETRY.ground_row)[1],stations:[]};a.placements.push(placement);
   for(const id of REVIEW_SCORES)for(const station of new Set(metrics.filter(m=>m.id===id).map(m=>m.station))){
    const effects=metrics.filter(m=>m.id===id&&m.station===station),control=GEOMETRY.controls[station],target=castleArtWorld(center,control.x,control.y,{center:true}),candidates=[];
    for(let x=2;x<=124;x++)for(let y=Math.ceil(placement.ground);y<=37;y++){const distances=effects.map(m=>reach(m,[x,y],target));candidates.push({root:[x,y],distances,maxReach:Math.max(...distances)});}
    candidates.sort((a,b)=>a.maxReach-b.maxReach||a.root[1]-b.root[1]||a.root[0]-b.root[0]);
    const record={id,station,target,effectIndices:effects.map(m=>m.index),bestGeometric:candidates[0],geometricCommonCount:candidates.filter(c=>c.maxReach<=3).length,effects:effects.map((m,i)=>({index:m.index,minReach:Math.min(...candidates.map(c=>c.distances[i])),geometricCount:candidates.filter(c=>c.distances[i]<=3).length})),supportedCommonCount:0,bestSupported:null};placement.stations.push(record);
    const possible=candidates.filter(c=>c.distances.some(d=>d<=3));
    groups.push({record,possible,effects,offset:requests.length});
    for(const c of possible)for(const m of effects)requests.push({root:c.root,center,metric:m});
   }
  }
 }
 const python=fileURLToPath(new URL('../../.venv/bin/python',import.meta.url)),helper=fileURLToPath(new URL('./review-castle-age-support.py',import.meta.url));
 const result=spawnSync(python,[helper],{input:JSON.stringify(requests),encoding:'utf8',maxBuffer:32*1024*1024});if(result.status!==0)throw Error(result.stderr||'Native support helper failed');const support=JSON.parse(result.stdout);
 if(support.length!==requests.length)throw Error('Native support result count mismatch');
 for(const {record,possible,effects,offset}of groups){
  record.effects.forEach(e=>e.supportedCount=0);record.rejectedReasons={};
  possible.forEach((c,i)=>{const checks=effects.map((_,j)=>support[offset+i*effects.length+j]);checks.forEach((check,j)=>{if(check.supported&&c.distances[j]<=3)record.effects[j].supportedCount++;else if(!check.supported)record.rejectedReasons[check.reason]=(record.rejectedReasons[check.reason]||0)+1;});if(c.maxReach<=3&&checks.every(c=>c.supported)){record.supportedCommonCount++;record.bestSupported??=c;}});
 }
 return report;
}
function html(report){const escape=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');return '<!doctype html><meta charset="utf-8"><title>Castle age reach review</title><style>body{background:#142820;color:#eadbbd;font:15px system-ui;margin:30px}table{border-collapse:collapse}td,th{padding:8px;border:1px solid #587367;text-align:left}pre{font:12px/10.8px monospace;white-space:pre}section{margin:24px 0}.no{color:#ffbd9a}</style><h1>Castle age reach review</h1><p>Read-only feasibility evidence. No new age is adopted or certified. Egg observer participation remains a proposal.</p><ul>'+report.assumptions.map(s=>'<li>'+escape(s)+'</li>').join('')+'</ul>'+report.ages.map(a=>'<section><h2>'+a.age+'</h2><p>'+escape(a.role)+' · scale '+a.metrics[0].scale.toFixed(6)+' · feet '+JSON.stringify(a.metrics[0].feet)+'</p><details><summary>Actual D10 start-contact art</summary><pre>'+escape(a.previewArt.join('\n'))+'</pre></details>'+a.placements.map(p=>'<h3>Native center '+p.center+'; ground '+p.ground.toFixed(4)+'</h3><table><tr><th>Score/station</th><th>Grips by effect</th><th>Best geometric max reach</th><th>Common supported stances</th><th>Best supported root</th></tr>'+p.stations.map(s=>'<tr class="'+(s.supportedCommonCount?'':'no')+'"><td>'+s.id+' / '+s.station+'</td><td>'+s.effectIndices.map(i=>JSON.stringify(a.metrics.find(m=>m.id===s.id&&m.index===i).grip)).join('; ')+'</td><td>'+s.bestGeometric.maxReach.toFixed(3)+'</td><td>'+s.supportedCommonCount+'</td><td>'+JSON.stringify(s.bestSupported?.root??null)+'</td></tr>').join('')+'</table>').join('')+'</section>').join('');}
if(process.argv[1]===fileURLToPath(import.meta.url)){
 const report=buildReview(),out=new URL('../artifacts/animation-milestone/',import.meta.url);fs.mkdirSync(out,{recursive:true});fs.writeFileSync(new URL('castle-age-reach-review.json',out),JSON.stringify(report,null,2)+'\n');fs.writeFileSync(new URL('castle-age-reach-review.html',out),html(report));
 console.log(JSON.stringify(report.ages.map(a=>({age:a.age,scale:a.metrics[0].scale,placements:a.placements.map(p=>({center:p.center,stations:p.stations.map(s=>({id:s.id,station:s.station,min:s.bestGeometric.maxReach,supported:s.supportedCommonCount}))}))})),null,2));
}
