// Physical reach for every repertoire routine and hatched age (see
// export-wonder-reach.mjs): contact anchor height above the host's ground line
// against the measured D10 body height. Writes client/animation/repertoire-reach.json.
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import {REP_ROUTINES as R,REP_OBJECTS as O,repPose,repAnchor,repGround} from '../client/repertoire-routines.mjs';
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {actorPitches} from '../client/actor-projection.mjs';
const AGES=['hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'],sx=7.5,sy=800/112,body={};
for(const stage of AGES){const c=characterSprite({stage,state:'idle',facing:true},2),top=c.art.findIndex(r=>r.trim());body[stage]=(c.groundRow-top)*actorPitches({...c,x:0,y:0},sx,sy).ch;}
const SEA=new Set(['pufferfish','swordfish','sturgeon','ancient_dragon_fish']);
export const hostItem=oid=>O[oid].host==='keeping'?(SEA.has(oid)?'infinity_pool':'koi_pond'):O[oid].host==='display'?'trophy_case':oid;
// Worn things: contacts are on Cheese's own body, always within his reach.
const SELF=oid=>O[oid].host==='wearable';
const env=(stage,tool)=>body[stage]*({none:1.05,wing:1.1,twig:1.6,reed:1.6}[tool]??0);  // unknown tools reach nothing
const out={version:1,bodyHeight:body,routines:{}};
for(const [key,r] of Object.entries(R)){
  if(SELF(r.object)){out.routines[key]={contactHeight:0,highestAnchor:null,tool:r.tool,reachableAges:AGES.filter(a=>!r.ages||r.ages.includes(a))};continue;}
 const item=hostItem(r.object),m=itemSprite(item,0,{state:{keeping:{setup:true,fish:[]}}}),hh=sx*itemWorldScale(item)*(m.detailScale||1)*1.5,ground=repGround(m);
 let high=0,anchor=null;
 const samples=[...Array(161).keys()].map(i=>i/160).concat(r.events.map(e=>e[0]),r.track.map(q=>q[0]));
 for(const f of samples){const p=repPose({id:key,elapsed:r.duration*f});if(!(p.contact>.05))continue;for(const n of [p.anchorA,p.anchorB]){const a=repAnchor(m,r.object,n);if(!a)continue;const h=(ground-a.y)*hh;if(h>high){high=h;anchor=n;}}}
 out.routines[key]={contactHeight:Math.round(high),highestAnchor:anchor,tool:r.tool,reachableAges:AGES.filter(a=>(!r.ages||r.ages.includes(a))&&high<=env(a,r.tool))};
}
const target=fileURLToPath(new URL('../client/animation/repertoire-reach.json',import.meta.url)),data=JSON.stringify(out,null,1)+'\n';
if(process.argv.includes('--check')){if(!fs.existsSync(target)||fs.readFileSync(target,'utf8')!==data)throw Error('Repertoire anchors changed: run node engine/scripts/export-repertoire-reach.mjs');}
else fs.writeFileSync(target,data);
const rows=Object.values(out.routines);console.log(JSON.stringify({routines:rows.length,unreachable:rows.filter(v=>!v.reachableAges.length).length}));
