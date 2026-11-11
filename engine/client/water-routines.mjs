import {sameInstance} from './physical-objects.mjs';
import ROUTINES from './animation/water-routines.json' with {type:'json'};
export {ROUTINES as WATER_ROUTINES};
const clamp=n=>Math.max(0,Math.min(1,n));
const NEUTRAL={x:0,y:0,b:0,w:0,l:0,r:0,u:0,v:0,splash:0,sip:0,eye:null,mark:'',facing:true};
export function waterPose(routine,motion=true){
 const spec=ROUTINES[routine?.id];if(!spec||routine.interrupted)return null;
 const progress=motion?clamp(routine.elapsed/spec.duration):.5;
 let a=spec.track[0],b=spec.track.at(-1);
 for(let i=1;i<spec.track.length;i++)if(progress<=spec.track[i][0]){a=spec.track[i-1];b=spec.track[i];break;}
 let u=clamp((progress-a[0])/Math.max(.001,b[0]-a[0]));u=u*u*(3-2*u);
 a={...NEUTRAL,...a[1]};b={...NEUTRAL,...b[1]};const pose={...a};
 for(const k of ['x','y','b','w','l','r','u','v','splash','sip'])pose[k]=a[k]+(b[k]-a[k])*u;
 if(u>.5){pose.eye=b.eye;pose.mark=b.mark;pose.facing=b.facing;}
 return {...pose,mode:spec.mode,swimming:['swim','soak'].includes(spec.mode),progress,
  inside:motion?Math.min(clamp(progress/.12),clamp((1-progress)/.12)):1};
}
export function waterStage(plan,objects,character,stage,motion=true){
 if(!plan||plan.kind!=='item'||plan.paused||plan.phase!=='act'||stage==='egg')return null;
 const routine=plan.water_routine,pose=waterPose(routine,motion);if(!pose||routine.done)return null;
 const home=objects.find(o=>o.id===plan.target&&sameInstance(o,plan)&&o.worldPosition?.every((v,i)=>Math.abs(v-plan.destination[i])<1.1));
 if(!home||home.construction!=='waterworks-v1'||!character)return null;
 const a=home.anchors,edge=['edge','sip'].includes(pose.mode),seat={...(edge?a.entry:a.seat)};
 seat.x+=pose.u*(edge?4:a.swimRadius||5);seat.y+=pose.v*(edge?1:3);
 return {home,seat,pose,inside:pose.inside,immersed:['wade','swim','soak'].includes(pose.mode)};
}
export function waterGeometry(home,passenger,sx,sy){
 const c=passenger.character,unit=sx*home.scale*home.detailScale,ch=unit*1.5;
 const left=home.x*sx-home.width*unit/2,top=home.y*sy-home.art.length*ch;
 let x=left+passenger.seat.x*unit,y=top+passenger.seat.y*ch;
 // The bowl is low enough to sip from the bank. Align the contact at the
 // deepest dip; the rest of the gesture returns to the independently reached
 // bank position. The original age-specific bill remains the contact point.
 if(passenger.pose.sip&&c.bill){
  const cu=sx*c.scale,billX=(c.bill.x+.5-c.anchorX+(c.offsetX||0))*cu;
  const billY=(c.bill.y+.5-c.groundRow)*cu*1.5+(c.offsetY||0)*cu;
  const contactX=left+(home.anchors.contact.x+.5)*unit,contactY=top+(home.anchors.contact.y+.5)*ch;
  const sip=passenger.pose.sip;x+=(contactX-billX-x)*sip;y+=(contactY-billY-y)*sip;
 }
 const inside=passenger.inside;
 const character={...c,x:c.x+(x/sx-c.x)*inside,y:c.y+(y/sy-c.y)*inside};
 const rim=home.anchors.rim,front=passenger.immersed&&inside>.99?{...home,id:home.id+':waterfront',bather:null,
  art:home.art.map((row,y)=>y>=rim?row:' '.repeat(home.width)),fills:home.fills.filter(f=>f.y>=rim)}:null;
 return {character,front};
}
