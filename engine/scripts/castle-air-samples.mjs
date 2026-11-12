import {CASTLE_SCORES,castlePose,SHARED_RARE_CASTS} from '../client/castle-care.mjs';
import {GUEST_CAST} from '../client/guest-cast.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {castleVisibleEyes} from '../client/castle-air-geometry.mjs';
export {AIR_ATOMICS} from '../client/castle-air-geometry.mjs';
export function visibleEyes(c){
 const eyes=castleVisibleEyes(c);
 if(!eyes.length)throw Error('Observation has no visible eye ink');
 return eyes;
}
export function airMetricSprite({stage,cast,id,index,motion=true,native=true,facing=true,progress}){
 const spec=CASTLE_SCORES[id],at=progress??spec.effects[index][0],clock=at*spec.duration;
 const base={id,stage:'service',clock,ride_elapsed:clock},station=castlePose(base).station;
 let routine=base;
 if(native){
  const actor=cast?(SHARED_RARE_CASTS.includes(cast)?cast:'metric-operator'):'cheese';
  routine={...base,physical_pilot:!cast,physical:{version:1,actor,source_age:stage,phase:'hold',station,root:[0,0],target:[0,0],contact_ready:true}};
  if(cast)Object.assign(routine,{shared_physical:true,shared:{version:1,attempt:'air-metrics',operator:{actor,cast,adapter:SHARED_RARE_CASTS.includes(cast)?'rare':'regular',motion_token:'metric-motion',token:'metric-token',location:'Home Pond'},source_age:'adult',phase:'operate',cheese:{root:[0,0],stance:[0,0],exit:[0,0],phase:'hold',ready:true}}});
 }
 return characterSprite({stage:stage||'adult',...(cast?{id:cast,castId:cast,name:GUEST_CAST[cast].name}:{}),state:'idle',facing,performance:{kind:'carnival',routine,role:'a',motion}},0,Boolean(cast));
}
