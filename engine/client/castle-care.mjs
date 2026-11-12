import {castleArtFrame,castleActorPitches,projectCastleWorld} from './castle-projection.mjs';
import CASTLE_GEOMETRY from './animation/castle-geometry.json' with {type:'json'};
import SCORES from './animation/castle-care.json' with {type:'json'};
export {SCORES as CASTLE_SCORES};
const N={x:0,y:0,b:0,w:0,l:0,r:0,contact:0,reach:0,gape:0,eye:null,mark:''},clamp=(n,a=0,b=1)=>Math.max(a,Math.min(b,Number.isFinite(n)?n:0));
export function castleState(raw={}){
 if(!raw||typeof raw!=='object')raw={};const defaults={vent:0,door:0,latch:0,tie_left:.8,tie_right:.8,apron:0,flag:1,hose:0,kink:0,dust:0,mesh_wet:0,roof_water:0,prints:0,spray:0,stroke:0};
 return {...Object.fromEntries(Object.entries(defaults).map(([k,v])=>[k,clamp(raw[k]??v)])),motor:['auto','on','off'].includes(raw.motor)?raw.motor:'auto',powered:raw.powered===true,fan:Number.isFinite(raw.fan)?raw.fan:0};
}
export function castleStation(work,role='a'){
 const spec=SCORES[work.id];
 const steps=role==='b'?(spec.partnerStations||[[0,spec.partner]]):(spec.stations||[[0,spec.station]]);let name=steps[0][1],previous=name,travel=1;
 for(const [at,target]of steps.slice(1)){if(work.ride_elapsed<at*spec.duration)break;previous=name;name=target;travel=clamp((work.ride_elapsed-at*spec.duration)/2);}
 return {name,previous,travel};
}
export function castlePose(work,role='a',motion=true,watch=false){
 const spec=SCORES[work?.id];if(!spec)return null;const progress=clamp(work.ride_elapsed/spec.duration),track=spec.track;
 let a=track[0],b=track.at(-1);for(let i=1;i<track.length;i++)if(progress<=track[i][0]){a=track[i-1];b=track[i];break;}
 let u=clamp((progress-a[0])/Math.max(.001,b[0]-a[0]));u=u*u*(3-2*u);a={...N,...a[1]};b={...N,...b[1]};let p=Object.fromEntries(Object.entries(N).map(([k,v])=>[k,typeof v==='number'?a[k]+(b[k]-a[k])*u:u>.5?b[k]:a[k]]));
 const segment=spec.segments?.find(([start,end])=>progress>=start&&progress<=end);
 const local=segment?clamp((progress-segment[0])/(segment[1]-segment[0])):spec.segments?0:progress;
 if(role==='b')p={...N,contact:watch?0:local>.24&&local<.8?1:0,reach:watch?0:.25+.3*Math.sin(local*Math.PI),b:local>.35&&local<.7?.3:0,w:watch?.5:0,eye:local>.75?'^':'-',mark:local>.8&&local<.87?'!':''};
 const where=castleStation(work,role);
 if(where.travel<1)p={...N,l:Math.max(0,Math.sin(work.ride_elapsed*8)),r:Math.max(0,-Math.sin(work.ride_elapsed*8))};
 if(work.stage!=='service')p={...N,l:work.stage==='service_exit'?Math.max(0,Math.sin(work.clock*8)):0,r:work.stage==='service_exit'?Math.max(0,-Math.sin(work.clock*8)):0};
 if(!motion){p.x=p.y=p.l=p.r=p.w=p.gape=0;p.mark='';}
 return {...p,station:where.name,previousStation:where.previous,travel:where.travel,surfaceWork:!watch&&work.stage==='service',tool:'hand',seated:false};
}
export function castleGeometry(home,member,sx,sy){
 const frame=castleArtFrame(home,sx,sy);
 const c=member.character,w=member.work,pose=castlePose(w,member.role,c.performance?.motion!==false,member.watch),spec=SCORES[w.id];
 const inside=w.stage==='service'?clamp(w.clock/(spec.entryDuration??spec.duration*.14)):w.stage==='service_exit'?1-clamp(w.clock/4):0;
 const unit=frame?.unit||sx*home.scale*home.detailScale,uh=frame?.uh||unit*1.5,{cw,ch}=castleActorPitches(c,sx,sy),left=home.x*sx-home.width*unit/2,top=home.y*sy-home.art.length*uh;
 const end=home.anchors.controls[pose.station],start=home.anchors.controls[pose.previousStation],t=tween(pose.travel),anchor={x:start.x+(end.x-start.x)*t,y:start.y+(end.y-start.y)*t},target={x:left+(anchor.x+.5)*unit,y:top+(anchor.y+.5)*uh},ground=top+CASTLE_GEOMETRY.ground_row*uh;
 const rest=c.workGripRest||c.grip||{x:c.anchorX+5,y:c.groundRow-6},x=target.x+(member.role==='a'?-3:3)*cw-(rest.x+.5-c.anchorX)*cw;
 const character={...c,x:c.x+(x/sx-c.x)*inside,y:c.y+(ground/sy-c.y)*inside,offsetX:0,offsetY:0};
 const point=p=>Array.isArray(p)&&p.length===2&&p.every(Number.isFinite);
 const pilot=member.role==='a'&&w.physical_pilot===true;
 const physical=frame&&member.role==='a'&&w.physical?.version===1&&w.physical.actor==='cheese'&&point(w.physical.root)&&point(w.physical.target)?w.physical:null;
 if(pilot&&!physical){character.x=c.x;character.y=c.y;}
 if(physical){
  const root=projectCastleWorld(home.physicalCastle,physical.root,sx,sy),nativeTarget=projectCastleWorld(home.physicalCastle,physical.target,sx,sy);
  character.x=root.x/sx;character.y=root.y/sy;target.x=nativeTarget.x;target.y=nativeTarget.y;
 }
 if(!pilot&&!physical&&c.rig?.species==='butterfly')character.y-=5*ch/sy*inside;
 const grip=c.grip||rest,hand={x:character.x*sx+(grip.x+.5-c.anchorX)*cw,y:character.y*sy+(grip.y+.5-c.groundRow)*ch},points=[];let tip=null;
 const reachable=(!pilot||Boolean(physical))&&(!physical||Math.hypot((target.x-hand.x)/cw,(target.y-hand.y)/ch)<=3+1e-9);
 if(pose.contact>.01&&inside>.01&&!member.watch&&c.rig?.species!=='butterfly'&&(!physical||physical.contact_ready===true)&&reachable){
  const u=pose.contact*inside;tip={x:hand.x+(target.x-hand.x)*u,y:hand.y+(target.y-hand.y)*u};
  const dx=tip.x-hand.x,dy=tip.y-hand.y,n=Math.max(1,Math.ceil(Math.max(Math.abs(dx)/cw,Math.abs(dy)/ch))),glyph=Math.abs(dx)>Math.abs(dy)*2?'-':Math.abs(dy)>Math.abs(dx)*2?'|':dx*dy>0?'\\':'/';
  for(let i=0;i<=n;i++)points.push({x:hand.x+dx*i/n,y:hand.y+dy*i/n,glyph,color:c.inks?.w||'#d9bd8b'});
  points.push({x:tip.x,y:tip.y,glyph:')',color:'#e7d3a0'});
 }
 return {character,pose,cw,ground:physical?character.y*sy:ground,target,hand,tip,points,inside,front:null,authoritativeRoot:Boolean(physical),reachable};
}
function tween(t){return t*t*(3-2*t);}
export function castleSummary(state){const s=castleState(state.castle);return `Blower ${s.motor}${s.powered?' · turning':''} · ${Math.round((state.excursion?.inflation??0)*100)}% inflated · mesh ${s.door>.8?'rolled up':s.door<.2?'lowered':'partly open'}${s.latch>.5?' · buckled':''}`;}
