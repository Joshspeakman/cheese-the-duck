import ROUTINES from './animation/architecture-routines.json' with {type:'json'};
import COMPANY from './animation/architecture-company.json' with {type:'json'};
import {ARCHITECTURE_BLUEPRINTS,bridgeDeck} from './architecture-workshop.mjs';
export {ROUTINES as ARCHITECTURE_ROUTINES};
export {COMPANY as ARCHITECTURE_COMPANY};
export const ARCHITECTURE_CONTROLS={open:0,panel:0,flag:0,bucket:0,brake:0,walk:0};
const REST={...ARCHITECTURE_CONTROLS,u:1.08,v:0,x:0,y:0,b:0,w:0,l:0,r:0,reach:0,contact:0,gape:0,eye:null,mark:''},clamp=n=>Math.max(0,Math.min(1,n));
function sample(work,track,base){
 const p=clamp(work.elapsed/ROUTINES[work.id].duration);let a=track[0],b=track.at(-1);
 for(let i=1;i<track.length;i++)if(p<=track[i][0]){a=track[i-1];b=track[i];break;}
 let u=clamp((p-a[0])/Math.max(.001,b[0]-a[0]));u=u*u*(3-2*u);a={...base,...a[1]};b={...base,...b[1]};const pose={...a};
 for(const k in REST)if(typeof REST[k]==='number')pose[k]=a[k]+(b[k]-a[k])*u;
 if(u>.5){pose.eye=b.eye;pose.mark=b.mark;}return pose;
}
export function architecturePose(work,motion=true){
 const spec=ROUTINES[work?.id];if(!spec||work.interrupted)return null;
 const leader=sample(work,spec.track,{...REST,...work.start}),shared=COMPANY[work.company?.id],partner=Boolean(shared&&work.company.role==='b');
 const pose=partner?sample(work,shared.track,REST):leader,tool=partner?shared.tool:spec.tool,anchor=partner?shared.anchor:spec.anchor;
 // The helper may move and gesture, but never owns the mechanism controls.
 for(const k in ARCHITECTURE_CONTROLS)pose[k]=leader[k];
 if(!motion){pose.x=pose.y=pose.l=pose.r=pose.w=pose.gape=0;pose.mark='';}
 if(work.transition)Object.assign(pose,{contact:0,w:.15,reach:0,b:0,x:0,y:0,gape:0,l:motion?Math.max(0,Math.sin(work.transition.elapsed*10)):0,r:motion?Math.max(0,-Math.sin(work.transition.elapsed*10)):0,eye:null,mark:''});
 return {...pose,partner,actorU:pose.u,actorV:pose.v,anchor,tool,architecture:tool!=='none'&&!work.transition,progress:clamp(work.elapsed/spec.duration)};
}
export function architectureGeometry(home,worker,sx,sy){
 const c=worker.character,pose=architecturePose(c.performance.routine,c.performance.motion!==false),p=ARCHITECTURE_BLUEPRINTS[home.blueprint],unit=sx*home.scale*home.detailScale,uh=unit*1.5,cw=c.scale*sx,ch=cw*1.5;
 const left=home.x*sx-home.width*unit/2,top=home.y*sy-home.art.length*uh,anchor=home.anchors[pose.anchor]||home.anchors.contact;
 const target={x:left+(anchor.x+.5)*unit,y:top+(anchor.y+.5)*uh},rest=c.workGripRest||c.grip||{x:c.anchorX+5,y:c.groundRow-6};
 const deck=pose.partner?{x:p.w*pose.actorU,y:p.h-3+pose.actorV*10}:p.type==='bridge'?bridgeDeck(p,pose.walk):p.type==='compass'&&pose.tool==='none'?{x:p.w/2+Math.sin(pose.walk*Math.PI*2)*57,y:p.h-31-Math.cos(pose.walk*Math.PI*2)*18}:home.anchors.entry,ground=top+deck.y*uh;
 let x=pose.tool==='none'?left+deck.x*unit:target.x+(pose.partner?2:-2)*cw-(rest.x+.5-c.anchorX)*cw,y=ground;
 if(c.rig?.species==='butterfly')y-=5*ch;
 const character={...c,x:c.x+(x/sx-c.x)*worker.inside,y:c.y+(y/sy-c.y)*worker.inside,offsetY:0};
 const grip=c.grip||rest,hand={x:character.x*sx+(grip.x+.5-c.anchorX)*cw,y:character.y*sy+(grip.y+.5-c.groundRow)*ch},points=[];let tip=null;
 if(pose.tool!=='none'&&pose.contact>.01&&worker.inside>.01&&c.rig?.species!=='butterfly'){
  const u=pose.contact*worker.inside;tip={x:hand.x+(target.x-hand.x)*u,y:hand.y+(target.y-hand.y)*u};
  const dx=tip.x-hand.x,dy=tip.y-hand.y,n=Math.max(1,Math.ceil(Math.max(Math.abs(dx)/cw,Math.abs(dy)/ch))),glyph=Math.abs(dx)>Math.abs(dy)*2?'-':Math.abs(dy)>Math.abs(dx)*2?'|':dx*dy>0?'\\':'/';
  for(let i=0;i<=n;i++)points.push({x:hand.x+dx*i/n,y:hand.y+dy*i/n,glyph,color:pose.tool==='hand'?c.inks?.w||'#d9bd8b':'#c4aa7d'});
  points.push({x:tip.x,y:tip.y,glyph:pose.tool==='brush'?'###':')',color:'#e7d3a0'});
 }
 return {character,pose,cw,ground,target,hand,tip,points};
}
export function drawArchitectureTools(ctx,g){
 ctx.save();ctx.font='600 '+g.cw*1.5+'px Menlo, monospace';ctx.textAlign='center';ctx.textBaseline='middle';ctx.strokeStyle='#172c22';ctx.lineWidth=Math.max(.6,g.cw*.15);
 for(const p of g.points){ctx.fillStyle=p.color;ctx.strokeText(p.glyph,p.x,p.y);ctx.fillText(p.glyph,p.x,p.y);}ctx.restore();
}
