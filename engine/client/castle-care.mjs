import {GUEST_CAST} from './guest-cast.mjs';
import {castleArtFrame,castleActorPitches,projectCastleWorld} from './castle-projection.mjs';
import {castleVisibleEyes,castleActiveWork,castleTransit,AIR_ATOMICS} from './castle-air-geometry.mjs';
import CASTLE_GEOMETRY from './animation/castle-geometry.json' with {type:'json'};
import SCORES from './animation/castle-care.json' with {type:'json'};
export {SCORES as CASTLE_SCORES};
const N={x:0,y:0,b:0,w:0,l:0,r:0,contact:0,reach:0,gape:0,eye:null,mark:''},clamp=(n,a=0,b=1)=>Math.max(a,Math.min(b,Number.isFinite(n)?n:0));
const point=p=>Array.isArray(p)&&p.length===2&&p.every(Number.isFinite);
export const SHARED_RARE_CASTS=['traveling_merchant','celebrity_duck','lost_duckling','friendly_goose','wise_owl','mysterious_crow','grumpy_toad'];
// Exact adapter identities only; a story brain key is distinct from its render ID.
export function flightCastleRecord(work){
 work=castleActiveWork(work);
 const s=work?.shared,p=work?.physical,o=s?.operator,v=s?.observer,a=s?.observer_physical;
 return work?.flight_observer===true&&work.physical_pilot===true&&work.shared_physical===true&&s?.version===1&&s.mode==='flight-observer'&&o?.actor==='cheese'&&o.adapter==='cheese'&&o.source_age===s.source_age&&['hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'].includes(s.source_age)&&s.attempt&&v?.actor==='butterfly_fairy'&&v.cast==='butterfly_fairy'&&v.adapter==='rare'&&v.token!=null&&typeof v.motion_token==='string'&&typeof v.location==='string'&&['waiting','operate','exit','done','interrupted'].includes(s.phase)&&p?.version===1&&p.actor==='cheese'&&point(p.root)&&point(p.target)&&CASTLE_GEOMETRY.controls[p.station]&&['approach','hold','exit'].includes(p.phase)&&point(a?.root)&&point(a.stance)&&point(a.exit)&&['approach','hold','exit'].includes(a.phase)?s:null;
}
export function eggCaregiverRecord(work){
 work=castleActiveWork(work);
 const s=work?.shared,p=work?.physical,o=s?.operator,r=s?.recipient,profile=GUEST_CAST[o?.cast];
 const adapter=o?.adapter==='regular'?profile?.id.startsWith('friend:')&&!profile.rare&&profile.species==='duck':o?.adapter==='rare'?SHARED_RARE_CASTS.includes(o.cast)&&o.actor===o.cast&&typeof o.motion_token==='string':o?.adapter==='story'?o.cast==='lost_duckling'&&o.actor==='story:pip'&&o.render_id==='story:lost_duckling'&&typeof o.motion_token==='string'&&typeof o.story_step==='string':false;
 return work?.egg_caregiver===true&&(castleTransit(work)||[...AIR_ATOMICS,'castle_door_open'].includes(work.id))&&work.shared_physical===true&&work.physical_pilot===false&&!Object.hasOwn(work,'flight_observer')&&s?.version===1&&s.mode==='egg-caregiver'&&point(s.destination)&&point(s.center)&&typeof s.instance==='string'&&s.source_age==='egg'&&s.observer===undefined&&s.cheese===undefined&&s.attempt&&adapter&&typeof o.actor==='string'&&o.actor!=='cheese'&&o.token!=null&&typeof o.location==='string'&&['approach','operate','exit','done','interrupted'].includes(s.phase)&&r?.actor==='cheese'&&r.stage==='egg'&&typeof r.token==='string'&&r.token.length>0&&point(r.root)&&typeof r.facing==='boolean'&&r.phase==='stationary'&&p?.version===1&&p.actor===o.actor&&point(p.center)&&p.center.every((v,i)=>v===s.center[i])&&point(p.root)&&point(p.target)&&CASTLE_GEOMETRY.controls[p.station]&&['approach','hold','exit'].includes(p.phase)?s:null;
}
export function eggCaregiverScene(scene){
 const plan=scene.living?.plan,s=eggCaregiverRecord(plan?.carnival_work),d=scene.duck,r=s?.recipient;
 return s&&plan.kind==='item'&&plan.target==='bounce_house'&&plan.location===scene.location&&d?.stage==='egg'&&d.identity===r.token&&d.facing===r.facing&&d.x===r.root[0]&&d.y===r.root[1]&&scene.location===s.operator.location&&scene.living.plan.instance===s.instance&&point(scene.living.plan.destination)&&scene.living.plan.destination.every((v,i)=>v===s.destination[i])&&sharedCastleSource(scene,s)?s:null;
}
export function sharedCastleRecord(work){
 work=castleActiveWork(work);
 if((work&&Object.hasOwn(work,'egg_caregiver'))||work?.shared?.mode==='egg-caregiver')return eggCaregiverRecord(work);
 if((work&&Object.hasOwn(work,'flight_observer'))||work?.shared?.mode==='flight-observer')return flightCastleRecord(work);
 const s=work?.shared,p=work?.physical,o=s?.operator,profile=GUEST_CAST[o?.cast];
 const adapter=o?.adapter==='regular'?profile?.id.startsWith('friend:')&&!profile.rare&&profile.species==='duck':o?.adapter==='rare'?SHARED_RARE_CASTS.includes(o.cast)&&o.actor===o.cast&&typeof o.motion_token==='string':o?.adapter==='story'?o.cast==='lost_duckling'&&o.actor==='story:pip'&&o.render_id==='story:lost_duckling'&&typeof o.motion_token==='string'&&typeof o.story_step==='string':false;
 return work?.shared_physical===true&&work.physical_pilot!==true&&s?.version===1&&adapter&&typeof o.actor==='string'&&o.actor.length>0&&o.actor!=='cheese'&&['hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'].includes(s.source_age)&&s.attempt&&o.token!=null&&typeof o.location==='string'&&['waiting','operate','exit','done','interrupted'].includes(s.phase)&&p?.version===1&&p.actor===o.actor&&point(p.root)&&point(p.target)&&CASTLE_GEOMETRY.controls[p.station]&&['approach','hold','exit'].includes(p.phase)&&point(s.cheese?.root)&&point(s.cheese?.stance)&&point(s.cheese?.exit)&&['approach','hold','exit'].includes(s.cheese.phase)?s:null;
}
export function sharedCastleVisitorMatches(visitor,shared){
 return Boolean(shared&&visitor?.id===shared.operator.actor&&(visitor.castId?visitor.castId===shared.operator.cast:visitor.name===GUEST_CAST[shared.operator.cast]?.name));
}
export function sharedCastleSource(scene,shared){
 if(!shared)return null;const o=shared.operator;
 if(shared.mode==='flight-observer'){const v=scene.rareVisitor;return v?.id===shared.observer.actor&&v.castId===shared.observer.cast&&Number.isFinite(v.x)&&Number.isFinite(v.y)?v:null;}
 if(o.adapter==='regular')return sharedCastleVisitorMatches(scene.visitor,shared)?scene.visitor:null;
 if(o.adapter==='rare')return sharedCastleVisitorMatches(scene.rareVisitor,shared)?scene.rareVisitor:null;
 const actor=scene.storyActor,story=scene.living?.story;
 return o.adapter==='story'&&actor?.id===o.render_id&&actor.storyId==='lost_duckling'&&story?.id==='lost_duckling'&&String(story.step)===o.story_step&&Number.isFinite(actor.x)&&Number.isFinite(actor.y)?{...actor,castId:o.cast,name:GUEST_CAST[o.cast].name,stage:'duckling'}:null;
}
export function castleActorPhysical(work,role='a'){
 const shared=sharedCastleRecord(work);
 if(work?.shared_physical)return shared?(role==='a'?work.physical:shared.mode==='egg-caregiver'?null:shared.mode==='flight-observer'?shared.observer_physical:shared.cheese):null;
 const p=work?.physical;
 return role==='a'&&p?.version===1&&p.actor==='cheese'&&point(p.root)&&point(p.target)?p:null;
}
export function castleState(raw={}){
 if(!raw||typeof raw!=='object')raw={};const defaults={vent:0,door:0,latch:0,tie_left:.8,tie_right:.8,apron:0,flag:1,hose:0,kink:0,dust:0,mesh_wet:0,roof_water:0,prints:0,spray:0,stroke:0};
 return {...Object.fromEntries(Object.entries(defaults).map(([k,v])=>[k,clamp(raw[k]??v)])),motor:['auto','on','off'].includes(raw.motor)?raw.motor:'auto',powered:raw.powered===true,fan:Number.isFinite(raw.fan)?raw.fan:0,rotor_speed:clamp(raw.rotor_speed),airflow:clamp(raw.airflow),pressure:clamp(raw.pressure)};
}
export function castleStation(work,role='a'){
 work=castleActiveWork(work);if(!work||!SCORES[work.id])return null;
 const spec=SCORES[work.id],physical=work.physical;
 // Native locomotion owns station travel and contact readiness. Its frozen
 // score clock must not restart the legacy two-second crossing on arrival.
 if((sharedCastleRecord(work)||(role==='a'&&physical?.version===1&&physical.actor==='cheese'))&&CASTLE_GEOMETRY.controls[physical.station])return {name:physical.station,previous:physical.station,travel:1};
 const steps=role==='b'?(spec.partnerStations||[[0,spec.partner]]):(spec.stations||[[0,spec.station]]);let name=steps[0][1],previous=name,travel=1;
 for(const [at,target]of steps.slice(1)){if(work.ride_elapsed<at*spec.duration)break;previous=name;name=target;travel=clamp((work.ride_elapsed-at*spec.duration)/2);}
 return {name,previous,travel};
}
export function castlePose(work,role='a',motion=true,watch=false){
 work=castleActiveWork(work);
 if(castleTransit(work))return {...N,station:work.physical?.station,previousStation:work.physical?.station,travel:1,surfaceWork:false,tool:'hand',seated:false};
 const spec=SCORES[work?.id];if(!spec)return null;const progress=clamp(work.ride_elapsed/spec.duration),track=spec.track;
 let a=track[0],b=track.at(-1);for(let i=1;i<track.length;i++)if(progress<=track[i][0]){a=track[i-1];b=track[i];break;}
 let u=clamp((progress-a[0])/Math.max(.001,b[0]-a[0]));u=u*u*(3-2*u);a={...N,...a[1]};b={...N,...b[1]};let p=Object.fromEntries(Object.entries(N).map(([k,v])=>[k,typeof v==='number'?a[k]+(b[k]-a[k])*u:u>.5?b[k]:a[k]]));
 const segment=spec.segments?.find(([start,end])=>progress>=start&&progress<=end);
 const local=segment?clamp((progress-segment[0])/(segment[1]-segment[0])):spec.segments?0:progress;
 if(role==='b')p={...N,contact:watch?0:local>.24&&local<.8?1:0,reach:watch?0:.25+.3*Math.sin(local*Math.PI),b:local>.35&&local<.7?.3:0,w:watch?.5:0,eye:local>.75?'^':'-',mark:local>.8&&local<.87?'!':''};
 const where=castleStation(work,role);
 if(where.travel<1)p={...N,l:Math.max(0,Math.sin(work.ride_elapsed*8)),r:Math.max(0,-Math.sin(work.ride_elapsed*8))};
 if(work.stage!=='service')p={...N,l:work.stage==='service_exit'?Math.max(0,Math.sin(work.clock*8)):0,r:work.stage==='service_exit'?Math.max(0,-Math.sin(work.clock*8)):0};
 if(watch&&work.shared_physical){
  const shared=sharedCastleRecord(work),react=shared?.mode!=='egg-caregiver'&&shared?.phase==='operate'&&(shared.mode==='flight-observer'?shared.observer_physical:shared.cheese).ready===true&&(work.events||[]).some(i=>spec.effects[i]&&work.ride_elapsed-spec.effects[i][0]*spec.duration>=0&&work.ride_elapsed-spec.effects[i][0]*spec.duration<1.5);
  p={...N,y:react?-.4:0,w:react&&shared?.mode==='flight-observer'?.4:0,eye:react?'^':'O',mark:react&&shared?.mode!=='flight-observer'?'!':''};
 }
 if(!motion){p.x=p.y=p.l=p.r=p.w=p.gape=0;p.mark='';}
 return {...p,workLift:work.id==='castle_grill_clean'&&where.name==='grill'?3+2*p.reach:0,station:where.name,previousStation:where.previous,travel:where.travel,surfaceWork:!watch&&work.stage==='service',tool:'hand',seated:false};
}
export function castleGeometry(home,member,sx,sy){
 if(!castleActiveWork(member.work))return {character:member.character,pose:null,tip:null,points:[],inside:0,front:null,authoritativeRoot:false,reachable:false,observation:null};
 const frame=castleArtFrame(home,sx,sy);
 const c=member.character,w=castleActiveWork(member.work),pose=castlePose(w,member.role,c.performance?.motion!==false,member.watch),spec=SCORES[w.id];
 const shared=sharedCastleRecord(w),nativeRecord=castleActorPhysical(w,member.role),nativePhase=Boolean(nativeRecord);
 const inside=nativePhase?(nativeRecord.phase==='hold'?1:0):w.shared_physical?0:w.stage==='service'?clamp(w.clock/(spec.entryDuration??spec.duration*.14)):w.stage==='service_exit'?1-clamp(w.clock/4):0;
 const unit=frame?.unit||sx*home.scale*home.detailScale,uh=frame?.uh||unit*1.5,{cw,ch}=castleActorPitches(c,sx,sy),left=home.x*sx-home.width*unit/2,top=home.y*sy-home.art.length*uh;
 const end=home.anchors.controls[pose.station],start=home.anchors.controls[pose.previousStation],t=tween(pose.travel),anchor={x:start.x+(end.x-start.x)*t,y:start.y+(end.y-start.y)*t},target={x:left+(anchor.x+.5)*unit,y:top+(anchor.y+.5)*uh},ground=top+CASTLE_GEOMETRY.ground_row*uh;
 const rest=c.workGripRest||c.grip||{x:c.anchorX+5,y:c.groundRow-6},x=target.x+(member.role==='a'?-3:3)*cw-(rest.x+.5-c.anchorX)*cw;
 const character={...c,x:c.x+(x/sx-c.x)*inside,y:c.y+(ground/sy-c.y)*inside,offsetX:0,offsetY:0};
 const pilot=w.shared_physical===true||(member.role==='a'&&w.physical_pilot===true);
 const identity=!w.shared_physical||Boolean(shared&&(shared.mode==='flight-observer'?(member.role==='a'?member.actor==='cheese'&&c.cheese&&c.rig?.stage===shared.source_age:member.actor===shared.observer.actor&&c.profileId===shared.observer.cast):member.role==='a'?member.actor===shared.operator.actor&&c.profileId===shared.operator.cast:member.actor==='cheese'&&c.cheese));
 const physical=frame&&identity?nativeRecord:null;
 if(pilot&&!physical){character.x=c.x;character.y=c.y;}
 if(physical){
  const root=projectCastleWorld(home.physicalCastle,physical.root,sx,sy),nativeTarget=projectCastleWorld(home.physicalCastle,w.physical.target,sx,sy);
  character.x=root.x/sx;character.y=root.y/sy;target.x=nativeTarget.x;target.y=nativeTarget.y;
 }
 if(!pilot&&!physical&&c.rig?.species==='butterfly')character.y-=5*ch/sy*inside;
 const grip=c.grip||rest,hand={x:character.x*sx+(grip.x+.5-c.anchorX)*cw,y:character.y*sy+(grip.y+.5-c.groundRow)*ch},points=[];let tip=null;
 const reachable=!member.watch&&(!pilot||Boolean(physical))&&(!physical||Math.hypot((target.x-hand.x)/cw,(target.y-hand.y)/ch)<=3+1e-9);
 const sharedContact=!w.shared_physical||!member.paused&&shared?.phase==='operate'&&(shared.mode==='egg-caregiver'||(shared.mode==='flight-observer'?shared.observer_physical:shared.cheese).ready===true&&(shared.mode==='flight-observer'?shared.observer_physical:shared.cheese).phase==='hold');
 const observationOnly=w.id==='castle_gauge_check';
 if(!observationOnly&&sharedContact&&pose.contact>.01&&inside>.01&&!member.watch&&c.rig?.species!=='butterfly'&&(!physical||physical.contact_ready===true)&&reachable){
  const u=pose.contact*inside;tip={x:hand.x+(target.x-hand.x)*u,y:hand.y+(target.y-hand.y)*u};
  const dx=tip.x-hand.x,dy=tip.y-hand.y,n=Math.max(1,Math.ceil(Math.max(Math.abs(dx)/cw,Math.abs(dy)/ch))),glyph=Math.abs(dx)>Math.abs(dy)*2?'-':Math.abs(dy)>Math.abs(dx)*2?'|':dx*dy>0?'\\':'/';
  for(let i=0;i<=n;i++)points.push({x:hand.x+dx*i/n,y:hand.y+dy*i/n,glyph,color:c.inks?.w||'#d9bd8b'});
  points.push({x:tip.x,y:tip.y,glyph:')',color:'#e7d3a0'});
 }
 const visibleEyes=observationOnly?castleVisibleEyes(character):[];
 const observation=observationOnly&&physical&&point(physical.observation_target)?{
  target:projectCastleWorld(home.physicalCastle,physical.observation_target,sx,sy),
  eyes:visibleEyes.map(([x,y])=>({x:character.x*sx+x*cw,y:character.y*sy+y*ch})),
  ready:visibleEyes.length>0&&!member.watch&&!member.paused&&sharedContact&&physical.phase==='hold'&&physical.observation_ready===true,
 }:null;
 return {character,pose,cw,ground:physical?character.y*sy:ground,target,hand,tip,points,inside,front:null,authoritativeRoot:Boolean(physical),reachable,observation};
}
function tween(t){return t*t*(3-2*t);}
export function castleSummary(state){const s=castleState(state.castle);return `Blower ${s.motor}${s.powered?' · turning':''} · ${Math.round((state.excursion?.inflation??0)*100)}% inflated · mesh ${s.door>.8?'rolled up':s.door<.2?'lowered':'partly open'}${s.latch>.5?' · buckled':''}`;}
