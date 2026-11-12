import {CASTLE_SCORES,castlePose} from '../client/castle-care.mjs';
export function eggCaregiverWork(cast,id='castle_start',clock=0){
 const adapter=cast.startsWith('friend:')?'regular':'rare',actor=adapter==='regular'?'metric-visitor':cast,base={id,stage:'service',clock,ride_elapsed:clock},station=castlePose(base).station;
 return {...base,egg_caregiver:true,shared_physical:true,physical_pilot:false,events:[],physical:{version:1,actor,center:[0,0],phase:'hold',station,root:[0,0],target:[0,0],contact_ready:true},shared:{version:1,mode:'egg-caregiver',destination:[0,0],center:[0,0],instance:'metric-instance',attempt:'metric-caregiver',source_age:'egg',phase:'operate',operator:{actor,cast,adapter,token:'metric-visit',motion_token:'metric-motion',location:'Home Pond'},recipient:{actor:'cheese',stage:'egg',token:'metric-egg',root:[0,0],facing:true,phase:'stationary'}}};
}
export function caregiverSignatureTimes(profile){
 const offset=[...profile.id].reduce((n,c)=>n+c.charCodeAt(0),0)%19*.17,duck=['duck','duckling'].includes(profile.species),rate=duck?profile.pace*5/4.5:profile.pace;
 // All authored body/prop phase pairs within a common 720-second period for
 // the current decimal-tenth paces. Keep one actual time per distinct pair.
 const cuts=[offset];for(const hz of [rate,5])for(let k=Math.floor(offset*hz)+1;k/hz<offset+720;k++)cuts.push(k/hz);cuts.push(offset+720);cuts.sort((a,b)=>a-b);
 const pairs=new Map();for(let i=1;i<cuts.length;i++){const t=(cuts[i]+cuts[i-1])/2,key=Math.floor(t*rate)%8+':'+Math.floor(t*5)%8;if(!pairs.has(key))pairs.set(key,t-offset);}
 return [...pairs.values()];
}
