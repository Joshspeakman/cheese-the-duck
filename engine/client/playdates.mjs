import SCORES from './animation/playdates.json' with {type:'json'};
export {SCORES as PLAYDATES};
const clamp=n=>Math.max(0,Math.min(1,n));
export function playdatePose(plan,motion=true){
 const scene=plan?.company,spec=SCORES[scene?.id];
 if(!spec||plan.paused||scene.done||!['enter','act','exit'].includes(scene.phase))return null;
 const progress=motion?(scene.phase==='enter'?0:scene.phase==='exit'?1:clamp(scene.elapsed/scene.duration)):.5;
 const track=spec.track;let a=track[0],b=track.at(-1);
 for(let i=1;i<track.length;i++)if(progress<=track[i][0]){a=track[i-1];b=track[i];break;}
 let u=clamp((progress-a[0])/Math.max(.001,b[0]-a[0]));const linear=u;u=u*u*(3-2*u);
 const value=a[1]+(b[1]-a[1])*u,mass=scene.mass||[1,1],imbalance=(mass[1]-mass[0])/(mass[0]+mass[1]);
 const pose={id:scene.id,family:spec.family,progress,value,inside:scene.phase==='enter'?clamp(scene.elapsed/3):scene.phase==='exit'?1-clamp(scene.elapsed/3):1,
  a:spec.a,b:spec.b,young:scene.young,beat:motion?(progress*(spec.family==='trampoline'?6:4))%1:.5};
 if(spec.family==='seesaw')pose.tilt=value*(scene.young?3:7)+imbalance*2;
 if(spec.family==='ball'){
  pose.ballx=value*25;pose.bally=scene.id==='ball_bounce'&&a[1]!==b[1]?-Math.sin(linear*Math.PI)*10:0;
  pose.spin=(value+1)*2;pose.squash=scene.id==='ball_bounce'&&a[1]!==b[1]&&linear>.87?Math.sin((linear-.87)/.13*Math.PI):0;
  pose.turn=value<-.8?'a':value>.8?'b':null;
  pose.beat=motion?linear:.5;
 }
 if(spec.family==='sandbox'){pose.build=value;pose.turn=Math.floor(progress*8)%2?'b':'a';}
 if(spec.family==='trampoline'){
  const cycle=pose.beat*Math.PI*2;pose.dip=Math.max(0,Math.sin(cycle))*3*value;
  pose.jump=Math.max(0,-Math.sin(cycle))*value*(scene.young?4:12);
 }
 return pose;
}
export function playdateStage(plan,objects,cheese,partner,motion=true){
 const pose=playdatePose(plan,motion);if(!pose||!cheese||!partner)return null;
 const home=objects.find(o=>o.id===plan.target&&o.worldPosition?.every((n,i)=>Math.abs(n-plan.company.destination[i])<1.1));
 if(!home?.anchors)return null;const a=home.anchors;
 let seats;
 if(pose.family==='seesaw')seats=[a.seat,a.partner];
 else if(pose.family==='sandbox')seats=[{x:17,y:a.seat.y},{x:home.width-17,y:a.seat.y}];
 else if(pose.family==='ball')seats=[{x:12,y:home.art.length-3},{x:home.width-12,y:home.art.length-3}];
 else seats=[{x:a.seat.x,y:a.seat.y-pose.jump},{x:home.width-5,y:home.art.length-3}];
 return {home,pose,seats,inside:pose.inside};
}
