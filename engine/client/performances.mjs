import {architecturePose} from './architecture-routines.mjs';
import {groundPose} from './ground-routines.mjs';
import {textilePose} from './textile-routines.mjs';
import {musicPose} from './music-performances.mjs';
import {botanicalPose} from './botanical-routines.mjs';
import {lightingPose} from './lighting-routines.mjs';
import {creativePose} from './creative-routines.mjs';
import {keepsakePose} from './keepsake-routines.mjs';
import {nestPose} from './nest-routines.mjs';
import {waterPose} from './water-routines.mjs';
import {seatingPose} from './seating-routines.mjs';
import HOME_COMPANY from './animation/home-company.json' with {type:'json'};
// Authored joint tracks for two residents. Times are fractions of the shared
// simulation-owned scene; A and B deliberately take different turns.
// x/y move the head, b compresses/lifts the torso, w unfolds a wing, l/r step.
const N={x:0,y:0,b:0,w:0,l:0,r:0,eye:null,mark:''};
const K=(at,p={})=>({at,...N,...p});
export const PERFORMANCES={
 ...Object.fromEntries(Object.entries(HOME_COMPANY).map(([key,s])=>[key,{duration:s.duration,a:s.a.map(([at,p])=>K(at,p)),b:s.b.map(([at,p])=>K(at,p))}])),
 greeting:{duration:12,a:[K(0),K(.15,{y:1,b:.3}),K(.3,{w:1,eye:'^'}),K(.45,{w:.35}),K(.6,{w:.9}),K(.8,{y:.5,eye:'^'}),K(1)],b:[K(0),K(.2,{x:-.5,eye:'O'}),K(.35,{y:.7}),K(.5,{w:.8,eye:'^'}),K(.65,{w:.3}),K(.8,{w:1}),K(1)]},
 call_response:{duration:18,a:[K(0),K(.15,{x:.5,y:-.4,mark:'!'}),K(.3,{x:1,mark:'!'}),K(.42),K(.6,{y:.5}),K(.72,{x:.5,eye:'^'}),K(1)],b:[K(0),K(.2,{y:.6}),K(.4,{y:.5,eye:'^'}),K(.55,{x:.7,y:-.6,mark:'!'}),K(.7,{x:1,mark:'!'}),K(.82,{w:.4}),K(1)]},
 wing_bump:{duration:12,a:[K(0),K(.2,{x:.6,w:.4,l:1}),K(.4,{x:1,w:1,b:-.3}),K(.55,{w:1,b:.4,eye:'^',mark:'*'}),K(.7,{w:.4,r:1}),K(1)],b:[K(0),K(.15,{y:.6}),K(.35,{x:1,w:1,r:1}),K(.55,{w:1,b:.4,eye:'^',mark:'*'}),K(.75,{w:.2,l:1}),K(1)]},
 shy_hello:{duration:16,a:[K(0,{x:-.7,y:.7}),K(.2,{y:1,b:.4}),K(.35,{x:.25}),K(.45,{x:-.6}),K(.65,{w:.35,eye:'^'}),K(.85,{y:.6}),K(1)],b:[K(0),K(.2,{y:.5}),K(.4,{x:-.4,w:.5}),K(.6,{w:.8,eye:'^'}),K(.8,{y:.5}),K(1)]},
 pebble_inspection:{duration:22,a:[K(0),K(.15,{x:.7,y:1.4,b:.4}),K(.3,{x:1,y:1.8,w:.4}),K(.43,{x:0,y:-.5,mark:'?'}),K(.65,{y:1.3}),K(.8,{y:.5,eye:'^'}),K(1)],b:[K(0,{y:.3}),K(.2,{x:.5,y:.7}),K(.4,{x:.8,y:1.7,b:.5}),K(.55,{x:1.2,y:1.8,w:.6}),K(.72,{y:-.5,mark:'!'}),K(.88,{y:.5}),K(1)]},
 duet:{duration:24,a:[K(0),K(.12,{y:-.5,w:.5,l:1,mark:'do'}),K(.25,{b:.5,r:1}),K(.38,{y:-1,w:1,mark:'mi'}),K(.5,{b:.5,l:1}),K(.65,{y:-.8,w:.8,mark:'so'}),K(.8,{w:1,b:-.7,eye:'^'}),K(1)],b:[K(0),K(.18,{b:.5,r:1}),K(.3,{y:-.5,w:.7,mark:'re'}),K(.45,{b:.5,l:1}),K(.55,{y:-.7,w:1,mark:'fa'}),K(.7,{b:.5,r:1}),K(.85,{w:.8,b:-.5,eye:'^',mark:'la'}),K(1)]},
 crumb_search:{duration:24,a:[K(0),K(.15,{x:1,y:1.5,b:.4}),K(.25,{x:.7,y:.4}),K(.35,{x:1.2,y:1.7}),K(.45,{x:-.5,y:.2}),K(.6,{y:1.5,r:1}),K(.8,{w:.4,mark:'.'}),K(1)],b:[K(0),K(.2,{x:-.6,y:.7,l:1}),K(.35,{x:.8,y:1.5,b:.5}),K(.5,{y:.2}),K(.62,{x:1.2,y:1.8}),K(.78,{x:.3,mark:'.'}),K(.9,{eye:'^'}),K(1)]},
 puddle_splash:{duration:20,a:[K(0),K(.2,{b:.7,y:.5}),K(.35,{b:-1.3,y:-.5,w:.8,l:1,r:1}),K(.45,{b:.8,mark:'*'}),K(.6,{x:-.6,y:-.5,eye:'O'}),K(.8,{w:.8,eye:'^'}),K(1)],b:[K(0),K(.25,{y:.4}),K(.45,{x:-.8,w:.6,eye:'O'}),K(.6,{b:.6}),K(.72,{b:-1.1,w:1,l:1,r:1}),K(.82,{b:.7,mark:'*',eye:'^'}),K(1)]},
 leaf_chase:{duration:22,a:[K(0),K(.15,{x:1,y:-.5,mark:'?'}),K(.3,{x:1.2,w:.6,l:1}),K(.45,{x:-.7,y:.5,r:1}),K(.6,{b:-.7,w:1,y:-.6}),K(.8,{x:1,y:1.4,mark:'!'}),K(1)],b:[K(0),K(.2,{x:-.7,y:.5}),K(.38,{x:1,y:-.5,w:.5}),K(.55,{x:1.1,y:1.5,l:1}),K(.7,{b:-.5,w:.8}),K(.87,{eye:'^',y:.5}),K(1)]},
 snow_tracks:{duration:24,a:[K(0),K(.15,{l:1,y:1}),K(.3,{r:1,b:.4}),K(.45,{x:.6,y:1.7}),K(.6,{x:1,mark:'!'}),K(.8,{w:.4,eye:'^'}),K(1)],b:[K(0),K(.2,{x:.5,y:1.3}),K(.4,{r:1,b:.3}),K(.55,{l:1,y:1}),K(.7,{x:.8,y:1.5}),K(.88,{y:-.5,eye:'^'}),K(1)]},
 stargaze:{duration:28,a:[K(0),K(.15,{y:-1.2,x:-.2}),K(.35,{y:-1.5,w:.7,mark:'*'}),K(.55,{y:-1.1}),K(.75,{x:.6,y:-.5,eye:'^'}),K(1)],b:[K(0,{y:.5}),K(.25,{y:-1,x:.2}),K(.45,{y:-1.6,mark:'*'}),K(.65,{y:-1.1,w:.4}),K(.85,{y:-.4,eye:'^'}),K(1)]},
 sunbeam_doze:{duration:26,a:[K(0),K(.18,{x:-.4,y:.7,b:.4}),K(.35,{x:-.7,y:1.3,b:.7,eye:'-'}),K(.6,{x:-.7,y:1.2,b:.5,eye:'-',mark:'z'}),K(.78,{w:.8,y:-.4}),K(1)],b:[K(0),K(.25,{y:.6}),K(.42,{x:-.6,y:1.1,b:.7,eye:'-'}),K(.68,{x:-.6,y:1.3,b:.5,eye:'-',mark:'z'}),K(.85,{y:-.5,w:.5}),K(1)]},
};
// Solo joint tracks use the same sampler, but are selected by an actual item
// plan. The item trajectory supplies support/contact; these supply body acting.
export const ITEM_PERFORMANCES={
 watch_build:[K(0),K(.2,{y:.8,x:.3}),K(.4,{y:1.1}),K(.6,{x:.5,y:.4,w:.2}),K(.8,{y:-.4,eye:'^'}),K(1)],
 ball_nudge:[K(0),K(.18,{x:.6,y:1.2,w:.2}),K(.32,{x:1.2,y:1.7,l:1}),K(.44,{x:.4,y:1}),K(.6,{y:-.4,eye:'^'}),K(.8,{w:.3}),K(1)],
 ball_stop:[K(0,{w:.3}),K(.18,{x:.5,y:.7,r:1}),K(.35,{x:.8,y:1.4,b:.3,w:.55}),K(.5,{y:.4,b:.5}),K(.7,{w:.7,eye:'^'}),K(.85,{y:-.4}),K(1)],
 spotter:[K(0),K(.15,{y:-.6}),K(.3,{y:-1.2,w:.4}),K(.45,{w:.8,x:.5,eye:'O'}),K(.6,{y:.5,w:.6}),K(.75,{w:.8,eye:'^'}),K(.9,{y:.3}),K(1)],
 bounce_count:[K(0),K(.14,{y:-.7,mark:'1'}),K(.3,{y:.6}),K(.44,{y:-1,mark:'2',w:.4}),K(.6,{y:.5}),K(.74,{y:-.8,mark:'3',w:.6}),K(.9,{eye:'^',w:.8}),K(1)],
 balance:[K(0),K(.2,{x:-.7,w:.7,l:1}),K(.4,{x:.6,w:1,b:.4}),K(.6,{x:-.6,w:.8,r:1}),K(.8,{y:-.5,eye:'^'}),K(1)],
 slide:[K(0,{y:.4}),K(.15,{w:.4,b:.5}),K(.35,{x:.6,y:-.4,w:1,eye:'O'}),K(.6,{x:.8,w:1,eye:'^',mark:'!'}),K(.85,{b:.7,w:.4}),K(1)],
 splash_steps:[K(0),K(.2,{l:1,y:1}),K(.4,{b:.5,mark:'.'}),K(.6,{r:1,w:.5}),K(.8,{y:.5,eye:'^'}),K(1)],
 climb:[K(0),K(.16,{l:1,x:.6,w:.3}),K(.33,{r:1,y:-.5,w:.5}),K(.5,{l:1,x:.7,w:.4}),K(.66,{r:1,y:-.5}),K(.85,{w:.6}),K(1)],
 bounce:[K(0,{b:.6}),K(.2,{y:-.5,w:.6}),K(.45,{w:1,y:-.8,l:1,r:1,eye:'^'}),K(.7,{w:.7}),K(.9,{b:.7,y:.6}),K(1,{b:.6})],
 rock:[K(0),K(.2,{x:.6,y:-.4,w:.3}),K(.45,{x:-.5,y:.6,b:.3}),K(.7,{x:.6,y:-.5,w:.4,eye:'^'}),K(1)],
 swing_lean:[K(0),K(.25,{x:.8,y:-.4,b:-.2,l:1,r:1}),K(.5,{x:-.7,y:.5,b:.4}),K(.75,{x:.7,y:-.5,eye:'^'}),K(1)],
 dig:[K(0),K(.2,{x:1,y:1.6,b:.5,w:.4}),K(.4,{x:-.6,y:.7,w:.8,mark:'.'}),K(.6,{x:.8,y:1.4,b:.4}),K(.8,{y:-.3,w:.6,eye:'^'}),K(1)],
};
export function performancePose(performance,stage='adult'){
 if(performance?.kind==='architecture'){
  const pose=architecturePose(performance.routine,performance.motion!==false);return pose?scalePose(pose,stage):null;
 }
 if(performance?.kind==='ground'){
  const pose=groundPose(performance.routine,performance.motion!==false);return pose?scalePose(pose,stage):null;
 }
 if(performance?.kind==='textile'){
  const pose=textilePose(performance.routine,performance.motion!==false);return pose?scalePose(pose,stage):null;
 }
 if(performance?.kind==='creative'){
  const pose=creativePose(performance.routine,performance.motion!==false);return pose?scalePose(pose,stage):null;
 }
 if(performance?.kind==='keepsake'){
  const pose=keepsakePose(performance.routine,performance.motion!==false);return pose?scalePose(pose,stage):null;
 }
 if(performance?.kind==='lighting'){
  const pose=lightingPose(performance.routine,performance.motion!==false);return pose?scalePose(pose,stage):null;
 }
 if(performance?.kind==='instrument'){
  const pose=musicPose(performance.item,performance.routine,performance.motion!==false);return pose?scalePose(pose,stage):null;
 }
 if(performance?.kind==='botanical'){
  const pose=botanicalPose(performance.routine,performance.motion!==false);return pose?scalePose(pose,stage):null;
 }
 if(performance?.kind==='seating'){
  const pose=seatingPose(performance.routine,performance.motion!==false);return pose?scalePose(pose,stage):null;
 }
 if(performance?.kind==='water'){
  const pose=waterPose(performance.routine,performance.motion!==false);return pose?scalePose(pose,stage):null;
 }
 if(performance?.kind==='nest'){
  const pose=nestPose(performance.routine,performance.motion!==false);if(!pose)return null;
  return scalePose(pose,stage);
 }
 const solo=ITEM_PERFORMANCES[performance?.kind],spec=PERFORMANCES[performance?.kind]||(solo?{a:solo,b:solo}:null);if(!spec)return null;
 const track=spec[performance.role==='b'?'b':'a'],p=Math.max(0,Math.min(1,performance.progress??0));
 let a=track[0],b=track.at(-1);for(let i=1;i<track.length;i++)if(p<=track[i].at){a=track[i-1];b=track[i];break;}
 let u=(p-a.at)/Math.max(.001,b.at-a.at);u=u*u*(3-2*u);
 const pose={...a};for(const k of ['x','y','b','w','l','r'])pose[k]=a[k]+(b[k]-a[k])*u;
 if(u>.5){pose.eye=b.eye;pose.mark=b.mark;}
 return scalePose(pose,stage);
}
function scalePose(pose,stage){
 const small=['hatchling','duckling'].includes(stage),elder=['elder','legendary'].includes(stage);
 return {...pose,x:Math.round(pose.x*(small?1.4:2.6)),y:Math.round(pose.y*(small?1:1.8)),
  b:Math.round(pose.b*(small?1:elder?1.2:2)),l:Math.round(pose.l),r:Math.round(pose.r)};
}
export function actorPerformance(scene,key){
 const s=scene.living?.minds?.performances?.find(s=>s.phase==='act'&&(s.a===key||s.b===key));
 if(!s)return null;
 return {kind:s.performance,role:s.a===key?'a':'b',progress:scene.motion===false?.5:s.elapsed/s.duration};
}
