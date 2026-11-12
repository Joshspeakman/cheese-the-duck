// Synthetic renderer contracts only; native shell/support/route evidence is separate.
import {sharedCastleFixture,specialSharedCastleFixture} from './castle-shared-fixtures.mjs';
export function eggCaregiverFixture(cast='friend:marco',adapter='regular',id='castle_start',index=0,{phase='hold',motion=true,facing=true}={}){
 const s=adapter==='regular'?sharedCastleFixture(cast,id,index,{phase,motion}):specialSharedCastleFixture(cast,adapter,id,index,{phase,motion}),w=s.living.plan.carnival_work;
 w.shared.center=[s.items[0].x,s.items[0].y];w.shared.destination=w.shared.center.map(v=>{const n=Math.floor(v);return v-n===.5?n+(n%2===0?0:1):Math.round(v);});w.shared.instance=s.living.plan.instance;w.physical.center=[...w.shared.center];
 s.living.plan.location=s.location;w.egg_caregiver=true;w.physical_pilot=false;w.shared.mode='egg-caregiver';w.shared.source_age='egg';w.shared.phase=phase==='hold'?'operate':phase==='exit'?'exit':'approach';delete w.shared.cheese;
 w.shared.recipient={actor:'cheese',stage:'egg',token:'egg-created-at-fixture',root:[45.125,26.875],facing,phase:'stationary'};
 s.living.plan.destination=[...w.shared.destination];
 Object.assign(s.duck,{stage:'egg',identity:w.shared.recipient.token,x:45.125,y:26.875,facing,state:'idle'});
 return s;
}
