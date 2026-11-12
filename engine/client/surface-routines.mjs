import {actorPitches} from './actor-projection.mjs';
import {castleArtFrame} from './castle-projection.mjs';
import ROUTINES from './animation/surface-routines.json' with {type:'json'};
export {ROUTINES as SURFACE_ROUTINES};
const N={x:0,y:0,b:0,w:0,l:0,r:0,u:0,v:0,press:0,seated:0,eye:null,mark:''};
const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,Number.isFinite(v)?v:0));
function sample(track,p,base){
 p=clamp(p);let a=track[0],b=track.at(-1);
 for(let i=1;i<track.length;i++)if(p<=track[i][0]){a=track[i-1];b=track[i];break;}
 let u=clamp((p-a[0])/Math.max(.001,b[0]-a[0]));u=u*u*(3-2*u);a={...base,...a[1]};b={...base,...b[1]};
 return Object.fromEntries(Object.entries(base).map(([k,v])=>[k,typeof v==='number'?a[k]+(b[k]-a[k])*u:u>.5?b[k]:a[k]]));
}
export function surfaceControls(work){
 const spec=ROUTINES[work.id],t=work.ride_elapsed||0,p=clamp(t/spec.duration),out={};
 for(const role of ['a','b']){
  const pose=sample(spec[role],p,N),factor=work.factors?.[role]??1;let jump=0,press=pose.press,impact=0;
  for(const [start,end,height]of spec.leaps[role]){
   const a=start*spec.duration,length=(end-start)*spec.duration*Math.sqrt(Math.max(.01,factor)),b=a+length;
   if(a<=t&&t<=b){const u=(t-a)/Math.max(.001,length);jump=Math.max(jump,4*u*(1-u)*height*factor);}
   if(a-.5<=t&&t<a)press=Math.max(press,.55*Math.sin(Math.PI*(t-a+.5)/.5));
   if(b<=t&&t<b+1.2){const age=t-b;impact=Math.max(impact,1-age/1.2);press=Math.max(press,.85*Math.exp(-age*3));}
  }
  out[role]={...pose,jump,press:clamp(press),impact};
 }
 return {...out,...sample(spec.deck,p,{lift:0,tilt:0})};
}
export function surfaceInside(work,role){
 if(work.stage==='board_'+role)return clamp(work.clock/4);
 if(work.stage==='unload_'+role)return 1-clamp(work.clock/4);
 return (role==='a'?['board_b','play','land','unload_b']:['play','land']).includes(work.stage)?1:0;
}
export function surfacePose(work,role='a',motion=true,watch=false){
 const spec=ROUTINES[work?.id];if(!spec)return null;
 const inside=watch?0:surfaceInside(work,role),control=surfaceControls(work)[role];let p={...control};
 if(work.stage!=='play')p={...N};
 if(work.stage==='land'){p.y=.5;p.w=.5;p.eye=work.withdrawal?'O':'^';}
 if(inside>0&&inside<1)p={...N,w:.25,l:Math.max(0,Math.sin(work.clock*8)),r:Math.max(0,-Math.sin(work.clock*8))};
 if(watch&&work.stage==='play')p={...N,y:-.5,w:.4+.4*Math.max(0,Math.sin(work.ride_elapsed*.6)),eye:'^'};
 if(!watch&&work.stage==='play'&&control.jump>1){p.w=Math.max(p.w,.6);p.l=p.r=.5;p.y-=.2;}
 if(!motion)p={...N};
 return {...p,seated:inside>.9&&(spec.item==='magic_carpet'||control.seated>.5)};
}
export function surfaceGeometry(home,member,sx,sy){
 const physical=castleArtFrame(home,sx,sy);
 const c=member.character,w=member.work,inside=member.watch?0:surfaceInside(w,member.role),slot=member.role==='a'?0:1,unit=physical?.unit||sx*home.scale*home.detailScale,uh=physical?.uh||unit*1.5,{cw,ch}=actorPitches(c,sx,sy);
 if(inside===0)return {character:c,front:null,inside,seatIndex:slot};
 const left=home.x*sx-home.width*unit/2,top=home.y*sy-home.art.length*uh,seat=home.anchors.slots[slot],state=home.surfaceState[member.role];
 const pose=surfaceControls(w)[member.role],seated=home.anchors.surface==='carpet'?1:clamp((pose.seated-.5)*2);
 const contact=c.seatContact??c.groundRow,resting={x:left+seat.x*unit-(c.offsetX||0)*cw,y:top+(seat.y-state.jump)*uh+(c.groundRow-contact)*ch*seated-(c.offsetY||0)*ch/1.5};
 const route=[{x:c.x*sx,y:c.y*sy},...home.anchors.route.slice(1).map(p=>({x:left+p.x*unit,y:top+p.y*uh})),resting];
 const t=inside*(route.length-1),i=Math.min(route.length-2,Math.floor(t)),u=t-i,a=route[i],b=route[i+1];
 const character={...c,x:(a.x+(b.x-a.x)*u)/sx,y:(a.y+(b.y-a.y)*u)/sy,offsetY:inside===1?c.offsetY:0};
 const front=inside>.9?{...home,...home.anchors.front,id:home.id+':surface-front',anchors:{},carnivalRiders:null,animated:false}:null;
 return {character,front,inside,seatIndex:slot,seatPixel:{x:left+seat.x*unit,y:top+seat.y*uh},jumpPixels:state.jump*uh,seated};
}
