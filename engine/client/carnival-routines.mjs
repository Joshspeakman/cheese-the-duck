import {actorPitches} from './actor-projection.mjs';
import {SURFACE_ROUTINES,surfacePose,surfaceGeometry} from './surface-routines.mjs';
import {CASTLE_SCORES,castlePose,castleGeometry,sharedCastleRecord,sharedCastleSource,eggCaregiverScene} from './castle-care.mjs';
import ROUTINES from './animation/carnival-routines.json' with {type:'json'};
export {ROUTINES as CARNIVAL_ROUTINES};
const PROGRAMS={...ROUTINES,...SURFACE_ROUTINES,...CASTLE_SCORES};
const N={x:0,y:0,b:0,w:0,l:0,r:0,eye:null,mark:''};
const clamp=v=>Math.max(0,Math.min(1,Number.isFinite(v)?v:0));
export const CARNIVAL_CHOICES=Object.fromEntries(['ferris_wheel','carousel','bounce_house','magic_carpet'].map(id=>[id,Object.entries(PROGRAMS).filter(([,s])=>s.item===id).map(([key,s])=>[key,s.label])]));
export function boarding(work,role='a'){
 const name=work.stage,u=clamp(work.clock/6);
 if(name==='board_'+role)return u;
 if(name==='unload_'+role)return 1-u;
 const aboard=role==='a'?['index_b','board_b','ride','weather_return','unload_b','return_a']:['ride','weather_return'];
 return aboard.includes(name)?1:0;
}
export function carnivalPose(work,role='a',motion=true,watch=false){
 if(CASTLE_SCORES[work?.id])return castlePose(work,role,motion,watch);
 if(SURFACE_ROUTINES[work?.id])return surfacePose(work,role,motion,watch);
 const spec=ROUTINES[work?.id];if(!spec)return null;
 const track=spec[role],p=clamp(work.ride_elapsed/spec.duration);let a=track[0],b=track.at(-1);
 for(let i=1;i<track.length;i++)if(p<=track[i][0]){a=track[i-1];b=track[i];break;}
 let u=clamp((p-a[0])/Math.max(.001,b[0]-a[0]));u=u*u*(3-2*u);a={...N,...a[1]};b={...N,...b[1]};const pose={...a};
 for(const k of ['x','y','b','w','l','r'])pose[k]=a[k]+(b[k]-a[k])*u;
 if(u>.5){pose.eye=b.eye;pose.mark=b.mark;}
 const inside=watch?0:boarding(work,role),walking=inside>0&&inside<1;
 if(work.stage!=='ride')Object.assign(pose,N,{y:walking?.2:0,w:walking?.25:0,l:walking?Math.max(0,Math.sin(work.clock*7)):0,r:walking?Math.max(0,-Math.sin(work.clock*7)):0});
 if(watch&&work.stage==='ride'){pose.y=-.6;pose.w=.4+.4*Math.max(0,Math.sin(work.ride_elapsed*.4));}
 if(work.withdrawal&&inside>.9){const returning=Math.max(0,(work.elapsed||0)-(work.withdrawal_at||0));Object.assign(pose,{x:-.4,y:.5,w:.55,b:.2,eye:returning<3?'O':'-',mark:returning<2?'!':'',l:0,r:0});}
 if(!motion)Object.assign(pose,N);
 return {...pose,seated:inside>.9};
}
export function carnivalOccupants(scene){
 const plan=scene.living?.plan,w=plan?.carnival_work;
 if(w&&(Object.hasOwn(w,'flight_observer')||Object.hasOwn(w,'egg_caregiver')||['flight-observer','egg-caregiver'].includes(w.shared?.mode))&&!sharedCastleRecord(w))return [];
 if(!w||w.interrupted||!PROGRAMS[w.id]||!(w.shared_physical?['approach','prepare','act','settle']:['prepare','act','settle']).includes(plan.phase))return [];
 if(w.shared_physical){
  const shared=sharedCastleRecord(w),visitor=sharedCastleSource(scene,shared);
  if(!visitor||scene.location!==(shared.mode==='flight-observer'?shared.observer.location:shared.operator.location)||(scene.duck?.stage==='teen'?'juvenile':scene.duck?.stage)!==shared.source_age)return [];
  if(shared.mode==='egg-caregiver')return eggCaregiverScene(scene)?[{actor:shared.operator.actor,role:'a',work:w,paused:plan.paused===true}]:[];
  if(shared.mode==='flight-observer')return [{actor:'cheese',role:'a',work:w,paused:plan.paused===true},{actor:shared.observer.actor,role:'b',work:w,watch:true,paused:plan.paused===true}];
  return [{actor:shared.operator.actor,role:'a',work:w,paused:plan.paused===true},{actor:'cheese',role:'b',work:w,watch:true,paused:plan.paused===true}];
 }
 const records=[{actor:'cheese',role:'a',work:w}];
 if(w.companion?.ready)records.push({actor:w.companion.actor,role:'b',work:w,watch:w.companion.mode==='watch'});
 return records;
}
export function carnivalGeometry(home,member,sx,sy){
 if(CASTLE_SCORES[member.work?.id])return castleGeometry(home,member,sx,sy);
 if(home.anchors.surface)return surfaceGeometry(home,member,sx,sy);
 const c=member.character,w=member.work,inside=member.watch?0:boarding(w,member.role),unit=sx*home.scale*home.detailScale,uh=unit*1.5,{cw,ch}=actorPitches(c,sx,sy);
 const left=home.x*sx-home.width*unit/2,top=home.y*sy-home.art.length*uh;
 const cabins=home.anchors.cabins||home.anchors.rides,seatIndex=w['seat_'+member.role]??0,seat=cabins.find(s=>s.index===seatIndex);
 if(!seat||inside===0)return {character:c,front:null,inside,seatIndex};
 const ground=c.seatContact??c.groundRow;
 const resting={x:left+seat.seat.x*unit-(c.offsetX||0)*cw,y:top+seat.seat.y*uh+(c.groundRow-ground)*ch-(c.offsetY||0)*ch/1.5};
 const route=[{x:c.x*sx,y:c.y*sy},...home.anchors.route.slice(1).map(p=>({x:left+p.x*unit,y:top+p.y*uh})),resting];
 const t=inside*(route.length-1),index=Math.min(route.length-2,Math.floor(t)),u=t-index,a=route[index],b=route[index+1];
 const character={...c,x:(a.x+(b.x-a.x)*u)/sx,y:(a.y+(b.y-a.y)*u)/sy,offsetY:inside===1?c.offsetY:0};
 const layer=home.anchors.fronts.find(f=>f.index===seatIndex);
 const front=inside>.9&&layer?{...home,...layer,id:home.id+':cabin-front:'+seatIndex,carnivalRiders:null,anchors:{},animated:false}:null;
 return {character,front,inside,seatIndex,seatPixel:{x:left+seat.seat.x*unit,y:top+seat.seat.y*uh},bodyWidth:(c.rig?.body?.w||0)*cw,seatWidth:seat.width*unit};
}
