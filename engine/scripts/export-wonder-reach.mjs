// Measures, for every wonder routine and every hatched age, whether each authored
// contact is physically within Cheese's reach from the ground he actually stands
// on. Writes client/animation/wonder-reach.json; native eligibility reads it, so a
// routine is never offered to an age whose wing (or held tool) cannot reach.
// Reach envelopes come from the measured D10 rig: a bare wing reaches a little
// above the head; a held tool adds about half a body height.
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import {WONDER_ROUTINES as R,wonderGeometry,wonderPose} from '../client/wonder-routines.mjs';
import {WONDER_BLUEPRINTS as B} from '../client/wonder-workshop.mjs';
import {itemSprite} from '../client/ultra-items.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {actorPitches} from '../client/actor-projection.mjs';
const AGES=['hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'];
const sx=7.5,sy=800/112;
const body={};
for(const stage of AGES){
 const c=characterSprite({stage,state:'idle',facing:true},2),top=c.art.findIndex(r=>r.trim());
 const {ch}=actorPitches({...c,x:0,y:0},sx,sy);body[stage]=(c.groundRow-top)*ch;
}
export function envelope(stage,tool){return body[stage]*(tool==='none'?1.05:tool==='wing'?1.1:1.6);}  // none: head or body contact
const out={version:1,units:'pixels at sx 7.5; heights above the object ground line',bodyHeight:body,routines:{}};
for(const [key,r] of Object.entries(R)){
 const m=itemSprite(r.item,0,{}),unit=sx*B[r.item].scale*m.detailScale,hh=unit*1.5,ground=m.anchors.entry.y;
 let high=0,highAnchor=null;
 for(let i=0;i<=40;i++){
  const pose=wonderPose({id:key,elapsed:r.duration*i/40});if(!(pose.contact>.05))continue;
  const model=itemSprite(r.item,0,{pose:{wonder:pose}});
  for(const name of [pose.anchorA,pose.anchorB]){const a=model.anchors[name];if(!a)continue;const h=(ground-a.y)*hh;if(h>high){high=h;highAnchor=name;}}
 }
 const ages=AGES.filter(stage=>(!r.ages||r.ages.includes(stage))&&high<=envelope(stage,r.tool));
 out.routines[key]={contactHeight:Math.round(high),highestAnchor:highAnchor,tool:r.tool,reachableAges:ages};
}
if(process.argv[1]===fileURLToPath(import.meta.url)){
 const target=fileURLToPath(new URL('../client/animation/wonder-reach.json',import.meta.url));
 const data=JSON.stringify(out,null,1)+'\n';
 if(process.argv.includes('--check')){if(fs.readFileSync(target,'utf8')!==data)throw Error('Wonder anchors changed: run node engine/scripts/export-wonder-reach.mjs');}
 else fs.writeFileSync(target,data);
 const rows=Object.entries(out.routines),none=rows.filter(([,v])=>!v.reachableAges.length);
 console.log(JSON.stringify({routines:rows.length,unreachable:none.length,adultOK:rows.filter(([,v])=>v.reachableAges.includes('adult')).length,hatchlingOK:rows.filter(([,v])=>v.reachableAges.includes('hatchling')).length}));
 if(process.argv.includes('--list'))for(const [k,v] of rows)if(!v.reachableAges.includes('adult')&&v.tool!=='none')console.log(k.padEnd(28),v.tool.padEnd(9),String(v.contactHeight).padStart(4),v.highestAnchor);
}
