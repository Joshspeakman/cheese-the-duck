// Synthetic rendering contract only; native route/airborne clearance is separate.
import {scene} from './scenes.mjs';
import {flightWork} from '../scripts/castle-flight-samples.mjs';
import METRICS from '../client/animation/castle-contact-metrics.json' with {type:'json'};
import GEOMETRY from '../client/animation/castle-geometry.json' with {type:'json'};
import {castleArtWorld} from '../client/castle-projection.mjs';
export function flightFixture(stage='adult',id='castle_start',index=0,{phase='hold',observerPhase=phase,motion=true,react=true}={}){
 const w=flightWork(id,index,react),metric=METRICS.ages[stage].routines[id][index],origin=[59.4,21],anchor=GEOMETRY.controls[metric.station],target=castleArtWorld(origin,anchor.x,anchor.y,{center:true}),root=[target[0]-metric.grip[0]*metric.scale*132/192,target[1]-metric.grip[1]*metric.scale*42/47],hover=[46.25,24.75];
 Object.assign(w.physical,{root,target,phase,contact_ready:phase==='hold'});w.shared.source_age=w.shared.operator.source_age=stage;w.shared.phase=phase==='hold'?'operate':phase==='exit'?'exit':'waiting';Object.assign(w.shared.observer_physical,{root:hover,stance:hover,exit:[40,24],phase:observerPhase,ready:observerPhase==='hold'});
 return scene({motion,particles:false,weatherEffects:false,duck:{stage,x:root[0],y:root[1],state:phase==='hold'?'idle':'walking',facing:true},visitor:null,rareVisitor:{id:'butterfly_fairy',castId:'butterfly_fairy',name:'Flutter',x:hover[0],y:hover[1],state:observerPhase==='hold'?'idle':'walking',facing:true},items:[{id:'bounce_house',instance:'flight-fixture',x:origin[0],y:origin[1]}],living:{objects:{},ecology:{},plan:{kind:'item',target:'bounce_house',instance:'flight-fixture',destination:origin,phase:phase==='approach'?'approach':'act',carnival_work:w}}});
}
