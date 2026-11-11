import ROUTINES from './animation/textile-routines.json' with {type:'json'};
export {ROUTINES as TEXTILE_ROUTINES};
const clamp=n=>Math.max(0,Math.min(1,n));
export const TEXTILE_CONTROLS={roll:0,lift:0,press:0,comb:0,spread:.2,tie:1,loft:.6,u:.5,v:1.08};
const REST={x:0,y:0,b:0,w:0,l:0,r:0,reach:0,contact:0,eye:null,mark:'',...TEXTILE_CONTROLS};
function sample(work,p){
 const track=ROUTINES[work.id].track;let a=track[0],b=track.at(-1);
 for(let i=1;i<track.length;i++)if(p<=track[i][0]){a=track[i-1];b=track[i];break;}
 let u=clamp((p-a[0])/Math.max(.001,b[0]-a[0]));u=u*u*(3-2*u);const base={...REST,...work.start};if(work.id==='mat_roll')base.roll=0;if(work.id==='mat_unroll')base.roll=1;a={...base,...a[1]};b={...base,...b[1]};const pose={...a};
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
 return {...pose,...controls,progress,tool:spec.tool,textile:spec.tool!=='none'};
}
export function textileGeometry(home,worker,sx,sy){
 const c=worker.character,pose=textilePose(c.performance.routine,c.performance.motion!==false),unit=sx*home.scale*home.detailScale,hh=unit*1.5,cw=c.scale*sx,ch=cw*1.5;
 const left=home.x*sx-home.width*unit/2,top=home.y*sy-home.art.length*hh;
 const foot={x:left+(home.anchors.foot.x+.5)*unit,y:top+(home.anchors.foot.y+.5)*hh},target={x:left+(home.anchors.contact.x+.5)*unit,y:top+(home.anchors.contact.y+.5)*hh};
 const character={...c,x:c.x+(foot.x/sx-c.x)*worker.inside,y:c.y+(foot.y/sy-c.y)*worker.inside,offsetY:0};
 const grip=c.grip||{x:c.anchorX+5,y:c.groundRow-6},cl=character.x*sx-c.anchorX*cw,ct=character.y*sy-c.groundRow*ch;
 const hand={x:cl+(grip.x+.5)*cw,y:ct+(grip.y+.5)*ch},points=[];let tip=null;
 if(pose.tool!=='none'&&pose.contact>.01&&worker.inside>.01&&c.rig?.species!=='butterfly'){
  const u=pose.contact*worker.inside;tip={x:hand.x+(target.x-hand.x)*u,y:hand.y+(target.y-hand.y)*u};
  const steps=Math.max(1,Math.ceil(Math.max(Math.abs(tip.x-hand.x)/cw,Math.abs(tip.y-hand.y)/ch)));
  for(let i=0;i<=steps;i++)points.push({x:hand.x+(tip.x-hand.x)*i/steps,y:hand.y+(tip.y-hand.y)*i/steps,glyph:pose.tool==='brush'?'|':')',color:pose.tool==='brush'?'#bfa06d':'#d6b18b'});
  points.push({x:tip.x,y:tip.y,glyph:pose.tool==='brush'?'###':')',color:'#dfc78b'});
 }
 return {character,pose,cw,foot,target,hand,tip,points};
}
export function drawTextileTools(ctx,g){
 ctx.save();ctx.font='600 '+g.cw*1.5+'px Menlo, monospace';ctx.textAlign='center';ctx.textBaseline='middle';ctx.strokeStyle='#172c22';ctx.lineWidth=Math.max(.6,g.cw*.15);
 for(const p of g.points){ctx.fillStyle=p.color;ctx.strokeText(p.glyph,p.x,p.y);ctx.fillText(p.glyph,p.x,p.y);}ctx.restore();
}
