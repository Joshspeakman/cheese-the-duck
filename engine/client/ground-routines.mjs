import {actorPitches} from './actor-projection.mjs';
import COMPANY from './animation/ground-company.json' with {type:'json'};
import {GROUND_BLUEPRINTS,groundPoint} from './ground-workshop.mjs';
export {COMPANY as GROUND_COMPANY};
import ROUTINES from './animation/ground-routines.json' with {type:'json'};
export {ROUTINES as GROUND_ROUTINES};
export const GROUND_CONTROLS={u:.5,v:1.1,press:0,sweep:0};
const REST={...GROUND_CONTROLS,x:0,y:0,b:0,w:0,l:0,r:0,reach:0,contact:0,eye:null,mark:''};
const clamp=n=>Math.max(0,Math.min(1,n));
function sample(work,track,base){
 const p=clamp(work.elapsed/ROUTINES[work.id].duration);let a=track[0],b=track.at(-1);
 for(let i=1;i<track.length;i++)if(p<=track[i][0]){a=track[i-1];b=track[i];break;}
 let u=clamp((p-a[0])/Math.max(.001,b[0]-a[0]));u=u*u*(3-2*u);a={...base,...a[1]};b={...base,...b[1]};const pose={...a};
 for(const k in REST)if(typeof REST[k]==='number')pose[k]=a[k]+(b[k]-a[k])*u;
 if(u>.5){pose.eye=b.eye;pose.mark=b.mark;}return pose;
}
export function groundPose(work,motion=true){
 const spec=ROUTINES[work?.id];if(!spec||work.interrupted)return null;
 const duet=COMPANY[work.duet],leader=sample(work,duet?.lead||spec.track,{...REST,...work.start});
 if(duet?.layout==='lanes')leader.u=.08+.4*leader.u;
 const shared=COMPANY[work.company?.id],partner=Boolean(shared&&work.company.role==='b');
 const actor=partner?sample(work,shared.track,{...REST,u:1.12,v:1.06}):leader,tool=partner?shared.tool:spec.tool;
 const controls=Object.fromEntries(Object.keys(GROUND_CONTROLS).map(k=>[k,leader[k]]));
 if(partner&&motion&&actor.press<.3){
  const before=sample({...work,elapsed:Math.max(0,work.elapsed-.05)},shared.track,{...REST,u:1.12,v:1.06});
  if(Math.abs(before.u-actor.u)+Math.abs(before.v-actor.v)>.00001){actor.l=Math.max(actor.l,Math.sin(work.elapsed*9),0);actor.r=Math.max(actor.r,-Math.sin(work.elapsed*9),0);}
 }
 if(!motion){actor.l=actor.r=actor.w=actor.x=actor.y=0;actor.mark='';}
 const transition=work.transition?{contact:0,w:.15,reach:0,b:0,x:0,y:0,l:motion?Math.max(0,Math.sin(work.transition.elapsed*10)):0,r:motion?Math.max(0,-Math.sin(work.transition.elapsed*10)):0,eye:null,mark:''}:{};
 return {...actor,...controls,...transition,actorU:actor.u,actorV:actor.v,actorPress:actor.press,partner,progress:clamp(work.elapsed/spec.duration),tool,ground:tool!=='none'&&!work.transition};
}
export function groundGeometry(home,worker,sx,sy){
 const c=worker.character,pose=groundPose(c.performance.routine,c.performance.motion!==false),unit=sx*home.scale*home.detailScale,hh=unit*1.5,{cw,ch}=actorPitches(c,sx,sy);
 const left=home.x*sx-home.width*unit/2,top=home.y*sy-home.art.length*hh,p=GROUND_BLUEPRINTS[home.blueprint];
 const fp=groundPoint(p,pose.actorU,pose.actorV),cp=groundPoint(p,clamp(pose.actorU+(pose.partner?-.09:.09)),clamp(pose.actorV-.12));
 const foot={x:left+(fp.x+.5)*unit,y:top+(fp.y+.5)*hh},target={x:left+(cp.x+.5)*unit,y:top+(cp.y+.5)*hh};
 const ground=foot.y;
 if(pose.partner&&pose.tool!=='none'&&c.rig?.species!=='butterfly'){
  const rest=c.workGripRest||c.grip||{x:c.anchorX-5,y:c.groundRow-6},near=target.x+2*cw-(rest.x+.5-c.anchorX)*cw;
  foot.x+=(near-foot.x)*pose.contact;
 }
 if(c.rig?.species==='butterfly')foot.y-=5*ch;
 const character={...c,x:c.x+(foot.x/sx-c.x)*worker.inside,y:c.y+(foot.y/sy-c.y)*worker.inside,offsetY:0};
 const grip=c.grip||{x:c.anchorX+5,y:c.groundRow-6},cl=character.x*sx-c.anchorX*cw,ct=character.y*sy-c.groundRow*ch;
 const hand={x:cl+(grip.x+.5)*cw,y:ct+(grip.y+.5)*ch},points=[];let tip=null;
 if(pose.tool!=='none'&&pose.contact>.01&&worker.inside>.01&&c.rig?.species!=='butterfly'){
  const u=pose.contact*worker.inside;tip={x:hand.x+(target.x-hand.x)*u,y:hand.y+(target.y-hand.y)*u};
  const dx=tip.x-hand.x,dy=tip.y-hand.y,steps=Math.max(1,Math.ceil(Math.max(Math.abs(dx)/cw,Math.abs(dy)/ch)));
  const glyph=Math.abs(dx)>Math.abs(dy)*2?'-':Math.abs(dy)>Math.abs(dx)*2?'|':dx*dy>0?'\\':'/';
  for(let i=0;i<=steps;i++)points.push({x:hand.x+dx*i/steps,y:hand.y+dy*i/steps,glyph,color:pose.tool==='hand'?c.inks?.w||'#d6b18b':'#bfa06d'});
  points.push({x:tip.x,y:tip.y,glyph:pose.tool==='brush'?'###':pose.tool==='cloth'?'~~~':')',color:'#dfc78b'});
 }
 return {character,pose,cw,foot,ground,target,hand,tip,points};
}
export function drawGroundTools(ctx,g){
 ctx.save();ctx.font='600 '+g.cw*1.5+'px Menlo, monospace';ctx.textAlign='center';ctx.textBaseline='middle';ctx.strokeStyle='#172c22';ctx.lineWidth=Math.max(.6,g.cw*.15);
 for(const p of g.points){ctx.fillStyle=p.color;ctx.strokeText(p.glyph,p.x,p.y);ctx.fillText(p.glyph,p.x,p.y);}ctx.restore();
}
