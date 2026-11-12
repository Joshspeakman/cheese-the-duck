// Pure geometry samples, also usable by the read-only browser review.
import {GUEST_CAST} from '../client/guest-cast.mjs';
import {CASTLE_SCORES,castlePose} from '../client/castle-care.mjs';
const cast='butterfly_fairy',profile=GUEST_CAST[cast],offset=[...cast].reduce((n,c)=>n+c.charCodeAt(0),0)%19*.17;
export function flightWork(id='castle_start',index=0,react=true){
 const clock=CASTLE_SCORES[id].effects[index][0]*CASTLE_SCORES[id].duration,base={id,stage:'service',clock,ride_elapsed:clock},station=castlePose(base).station;
 return {...base,flight_observer:true,physical_pilot:true,shared_physical:true,events:react?[index]:[],physical:{version:1,actor:'cheese',phase:'hold',station,root:[0,0],target:[0,0],contact_ready:true},shared:{version:1,mode:'flight-observer',attempt:'flight-metrics',source_age:'adult',phase:'operate',operator:{actor:'cheese',adapter:'cheese',source_age:'adult'},observer:{actor:cast,cast,adapter:'rare',token:'metric',motion_token:'metric',location:'Home Pond'},observer_physical:{root:[0,0],stance:[0,0],exit:[0,0],phase:'hold',ready:true}}};
}
export function flightSampleTimes(){
 // Raster changes occur at lift half-cells, reciprocal-fold rounding, and
 // discrete sparkle phases. Include both sides and midpoints of every boundary
 // across a full common sin(4t)/cos(5t) period in actual seeded visitor time.
 const start=offset,end=offset+2*Math.PI,points=[start,end];
 function roots(freq,angles){for(const a of angles)for(let k=-10;k<=20;k++){const t=(a+k*2*Math.PI)/freq;if(t>start&&t<end)points.push(t);}}
 for(const v of [-.5/1.4,.5/1.4]){const a=Math.asin(v);roots(4,[a,Math.PI-a]);}
 for(const fold of [1/1.5,1/2.5]){const a=Math.acos((fold-.35)/.65);roots(5,[a,-a,Math.PI-a,Math.PI+a]);}
 for(let k=Math.floor(start*profile.pace);k<=Math.ceil(end*profile.pace);k++){const t=k/profile.pace;if(t>start&&t<end)points.push(t);}
 points.sort((a,b)=>a-b);const samples=new Set([0]);for(let i=0;i<points.length;i++){const t=points[i];for(const d of [-1e-7,0,1e-7])if(t+d>=start&&t+d<=end)samples.add(t+d-offset);if(i)samples.add((t+points[i-1])/2-offset);}
 return [...samples].sort((a,b)=>a-b);
}
