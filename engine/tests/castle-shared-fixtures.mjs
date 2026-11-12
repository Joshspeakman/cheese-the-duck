// Renderer contract fixtures only; they do not certify native routes/support.
import {scene} from './scenes.mjs';
import METRICS from '../client/animation/castle-guest-metrics.json' with {type:'json'};
import {GUEST_CAST} from '../client/guest-cast.mjs';
import {CASTLE_SCORES} from '../client/castle-care.mjs';
import {castleArtWorld} from '../client/castle-projection.mjs';
import GEOMETRY from '../client/animation/castle-geometry.json' with {type:'json'};
export function sharedCastleFixture(cast='friend:marco',id='castle_start',index=0,{phase='hold',cheesePhase=phase,stage='adult',motion=true,camera={x:0,y:0,w:132,h:42}}={}){
 const metric=METRICS.casts[cast].routines[id][index],anchor=GEOMETRY.controls[metric.station],origin=[59.4,24.5],target=castleArtWorld(origin,anchor.x,anchor.y,{center:true});
 const root=[target[0]-metric.grip[0]*metric.scale*132/192,target[1]-metric.grip[1]*metric.scale*42/47],watchRoot=[48.25,26.5],actor='live-visitor:'+cast.slice(7),profile=GUEST_CAST[cast];
 const elapsed=metric.at*CASTLE_SCORES[id].duration,work={id,stage:phase==='exit'?'service_exit':'service',clock:elapsed,ride_elapsed:elapsed,shared_physical:true,physical_pilot:false,events:Array.from({length:index+1},(_,i)=>i),physical:{version:1,actor,root,target,station:metric.station,phase,contact_ready:phase==='hold'},shared:{version:1,attempt:'renderer-fixture:'+id,operator:{actor,cast,adapter:'regular',token:'visit-token',location:'Home Pond'},source_age:stage,phase:phase==='hold'?'operate':phase==='exit'?'exit':'waiting',cheese:{root:watchRoot,stance:[48,27],exit:[46,27],phase:cheesePhase,ready:cheesePhase==='hold'}}};
 return scene({camera,motion,particles:false,weatherEffects:false,duck:{x:watchRoot[0],y:watchRoot[1],stage,state:cheesePhase==='hold'?'idle':'walking',facing:true},visitor:{id:actor,name:profile.name,x:root[0],y:root[1],state:phase==='hold'?'idle':'walking',facing:phase==='hold',personality:profile.archetype},items:[{id:'bounce_house',instance:'shared-castle-fixture',x:origin[0],y:origin[1]}],living:{objects:{},ecology:{},plan:{kind:'item',target:'bounce_house',instance:'shared-castle-fixture',destination:origin,phase:'act',carnival_work:work}}});
}
