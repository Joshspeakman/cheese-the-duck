import {actorPitches} from './actor-projection.mjs';
import ROUTINES from './animation/textile-routines.json' with {type:'json'};
import COMPANY from './animation/textile-company.json' with {type:'json'};
import {TEXTILE_BLUEPRINTS,textilePoint} from './textile-workshop.mjs';
export {ROUTINES as TEXTILE_ROUTINES,COMPANY as TEXTILE_COMPANY};
const clamp=n=>Math.max(0,Math.min(1,n));
export const TEXTILE_CONTROLS={roll:0,lift:0,press:0,comb:0,spread:.2,tie:1,loft:.6,u:.5,v:1.08};
const REST={x:0,y:0,b:0,w:0,l:0,r:0,reach:0,contact:0,eye:null,mark:'',...TEXTILE_CONTROLS};
function sample(work,p,track=ROUTINES[work.id].track,partner=false){
 let a=track[0],b=track.at(-1);
 for(let i=1;i<track.length;i++)if(p<=track[i][0]){a=track[i-1];b=track[i];break;}
 let u=clamp((p-a[0])/Math.max(.001,b[0]-a[0]));u=u*u*(3-2*u);const base={...REST,...work.start,...(partner?{u:1.12,v:.95}:null)};if(work.id==='mat_roll')base.roll=0;if(work.id==='mat_unroll')base.roll=1;a={...base,...a[1]};b={...base,...b[1]};const pose={...a};
 for(const k of Object.keys(REST))if(typeof REST[k]==='number')pose[k]=a[k]+(b[k]-a[k])*u;
 if(u>.5){pose.eye=b.eye;pose.mark=b.mark;}
 if(work.id==='mat_roll')pose.roll=(work.start?.roll||0)+(1-(work.start?.roll||0))*pose.roll;
 if(work.id==='mat_unroll')pose.roll*=work.start?.roll||0;
 return pose;
}
export function textilePose(work,motion=true){
 const spec=ROUTINES[work?.id];if(!spec||work.interrupted)return null;
 const progress=clamp(work.elapsed/spec.duration),actual=sample(work,progress),pose=motion?actual:sample(work,.5);
 const controls=Object.fromEntries(Object.keys(TEXTILE_CONTROLS).map(k=>[k,actual[k]]));
 const shared=COMPANY[work.company?.id],partner=Boolean(shared&&work.company.role==='b');
 const acting=partner?sample(work,motion?progress:.5,shared.track,true):pose,tool=partner?shared.tool:spec.tool;
 const before=partner?sample(work,Math.max(0,progress-.01),shared.track,true):acting;
 const moving=partner&&motion&&(Math.abs(before.v-acting.v)>.0001||Math.abs(before.contact-acting.contact)>.001);
 const steps=moving?{l:Math.max(0,Math.sin(work.elapsed*9)),r:Math.max(0,-Math.sin(work.elapsed*9))}:{};
 const walking=work.transition?{contact:0,w:.15,reach:0,b:0,x:0,y:0,l:motion?Math.max(0,Math.sin(work.transition.elapsed*10)):0,r:motion?Math.max(0,-Math.sin(work.transition.elapsed*10)):0,eye:null,mark:''}:{};
 return {...acting,...controls,...steps,...walking,actorU:acting.u,actorV:acting.v,partner,progress,tool,textile:tool!=='none'&&!work.transition};
}
export function textileGeometry(home,worker,sx,sy){
 const c=worker.character,pose=textilePose(c.performance.routine,c.performance.motion!==false),unit=sx*home.scale*home.detailScale,hh=unit*1.5,{cw,ch}=actorPitches(c,sx,sy);
 const left=home.x*sx-home.width*unit/2,top=home.y*sy-home.art.length*hh;
 const p=TEXTILE_BLUEPRINTS[home.blueprint],partner=worker.slot===1;
 const fp=partner?textilePoint(p,pose.actorU,pose.actorV,pose):home.anchors.foot;
 const cp=partner?textilePoint(p,.97,c.performance.routine.id==='mat_unroll'?pose.roll*.88:clamp(pose.actorV-.16),pose):home.anchors.contact;
 const foot={x:left+(fp.x+.5)*unit,y:top+(fp.y+.5)*hh},target={x:left+(cp.x+.5)*unit,y:top+(cp.y+.5)*hh};
 const rest=c.workGripRest||c.grip||{x:c.anchorX-5,y:c.groundRow-6};
 // Step close enough to the outer seam for a short wing reach. A small visitor
 // must not grow a long chain of hand glyphs to bridge the width of the mat.
 if(partner&&pose.tool!=='none'&&c.rig?.species!=='butterfly'){
  const near=target.x+2*cw-(rest.x+.5-c.anchorX)*cw;
  foot.x+=(near-foot.x)*pose.contact;
 }
 const ground=foot.y;if(c.rig?.species==='butterfly')foot.y-=5*ch;
 const character={...c,x:c.x+(foot.x/sx-c.x)*worker.inside,y:c.y+(foot.y/sy-c.y)*worker.inside,offsetY:0};
 const grip=c.grip||{x:c.anchorX+5,y:c.groundRow-6},cl=character.x*sx-c.anchorX*cw,ct=character.y*sy-c.groundRow*ch;
 const hand={x:cl+(grip.x+.5)*cw,y:ct+(grip.y+.5)*ch},points=[];let tip=null;
 if(pose.tool!=='none'&&pose.contact>.01&&worker.inside>.01&&c.rig?.species!=='butterfly'){
  const u=pose.contact*worker.inside;tip={x:hand.x+(target.x-hand.x)*u,y:hand.y+(target.y-hand.y)*u};
  const steps=Math.max(1,Math.ceil(Math.max(Math.abs(tip.x-hand.x)/cw,Math.abs(tip.y-hand.y)/ch)));
  const dx=tip.x-hand.x,dy=tip.y-hand.y,glyph=Math.abs(dx)>Math.abs(dy)*2?'-':Math.abs(dy)>Math.abs(dx)*2?'|':dx*dy>0?'\\':'/';
  for(let i=0;i<=steps;i++)points.push({x:hand.x+dx*i/steps,y:hand.y+dy*i/steps,glyph,color:pose.tool==='brush'?'#bfa06d':c.inks?.w||'#d6b18b'});
  points.push({x:tip.x,y:tip.y,glyph:pose.tool==='brush'?'###':')',color:'#dfc78b'});
 }
 return {character,pose,cw,foot,ground,target,hand,tip,points};
}
export function drawTextileTools(ctx,g){
 ctx.save();ctx.font='600 '+g.cw*1.5+'px Menlo, monospace';ctx.textAlign='center';ctx.textBaseline='middle';ctx.strokeStyle='#172c22';ctx.lineWidth=Math.max(.6,g.cw*.15);
 for(const p of g.points){ctx.fillStyle=p.color;ctx.strokeText(p.glyph,p.x,p.y);ctx.fillText(p.glyph,p.x,p.y);}ctx.restore();
}
