import ROUTINES from './animation/ground-routines.json' with {type:'json'};
export {ROUTINES as GROUND_ROUTINES};
export const GROUND_CONTROLS={u:.5,v:1.1,press:0,sweep:0};
const REST={...GROUND_CONTROLS,x:0,y:0,b:0,w:0,l:0,r:0,reach:0,contact:0,eye:null,mark:''};
const clamp=n=>Math.max(0,Math.min(1,n));
export function groundPose(work,motion=true){
 const spec=ROUTINES[work?.id];if(!spec||work.interrupted)return null;
 const p=clamp(work.elapsed/spec.duration);let a=spec.track[0],b=spec.track.at(-1);
 for(let i=1;i<spec.track.length;i++)if(p<=spec.track[i][0]){a=spec.track[i-1];b=spec.track[i];break;}
 let u=clamp((p-a[0])/Math.max(.001,b[0]-a[0]));u=u*u*(3-2*u);a={...REST,...work.start,...a[1]};b={...REST,...work.start,...b[1]};const pose={...a};
 for(const k in REST)if(typeof REST[k]==='number')pose[k]=a[k]+(b[k]-a[k])*u;
 if(u>.5){pose.eye=b.eye;pose.mark=b.mark;}
 if(!motion){pose.l=pose.r=pose.w=pose.x=pose.y=0;pose.mark='';}
 return {...pose,progress:p,tool:spec.tool,ground:spec.tool!=='none'};
}
export function groundGeometry(home,worker,sx,sy){
 const c=worker.character,pose=groundPose(c.performance.routine,c.performance.motion!==false),unit=sx*home.scale*home.detailScale,hh=unit*1.5,cw=c.scale*sx,ch=cw*1.5;
 const left=home.x*sx-home.width*unit/2,top=home.y*sy-home.art.length*hh,fp=home.anchors.foot,cp=home.anchors.contact;
 const foot={x:left+(fp.x+.5)*unit,y:top+(fp.y+.5)*hh},target={x:left+(cp.x+.5)*unit,y:top+(cp.y+.5)*hh};
 const character={...c,x:c.x+(foot.x/sx-c.x)*worker.inside,y:c.y+(foot.y/sy-c.y)*worker.inside,offsetY:0};
 const grip=c.grip||{x:c.anchorX+5,y:c.groundRow-6},cl=character.x*sx-c.anchorX*cw,ct=character.y*sy-c.groundRow*ch;
 const hand={x:cl+(grip.x+.5)*cw,y:ct+(grip.y+.5)*ch},points=[];let tip=null;
 if(pose.tool!=='none'&&pose.contact>.01&&worker.inside>.01){
  const u=pose.contact*worker.inside;tip={x:hand.x+(target.x-hand.x)*u,y:hand.y+(target.y-hand.y)*u};
  const dx=tip.x-hand.x,dy=tip.y-hand.y,steps=Math.max(1,Math.ceil(Math.max(Math.abs(dx)/cw,Math.abs(dy)/ch)));
  const glyph=Math.abs(dx)>Math.abs(dy)*2?'-':Math.abs(dy)>Math.abs(dx)*2?'|':dx*dy>0?'\\':'/';
  for(let i=0;i<=steps;i++)points.push({x:hand.x+dx*i/steps,y:hand.y+dy*i/steps,glyph,color:pose.tool==='hand'?c.inks?.w||'#d6b18b':'#bfa06d'});
  points.push({x:tip.x,y:tip.y,glyph:pose.tool==='brush'?'###':pose.tool==='cloth'?'~~~':')',color:'#dfc78b'});
 }
 return {character,pose,cw,foot,target,hand,tip,points};
}
export function drawGroundTools(ctx,g){
 ctx.save();ctx.font='600 '+g.cw*1.5+'px Menlo, monospace';ctx.textAlign='center';ctx.textBaseline='middle';ctx.strokeStyle='#172c22';ctx.lineWidth=Math.max(.6,g.cw*.15);
 for(const p of g.points){ctx.fillStyle=p.color;ctx.strokeText(p.glyph,p.x,p.y);ctx.fillText(p.glyph,p.x,p.y);}ctx.restore();
}
