import ROUTINES from './animation/creative-routines.json' with {type:'json'};
import COMPANY from './animation/creative-company.json' with {type:'json'};
import {scopeEyepiece} from './creative-workshop.mjs';
export {ROUTINES as CREATIVE_ROUTINES,COMPANY as CREATIVE_COMPANY};
const clamp=n=>Math.max(0,Math.min(1,n));
export const CREATIVE_CONTROLS={aim:.35,focus:.5,cap:1,fold:0,cover:0,flight:0,stroke:0};
const REST={x:0,y:0,b:0,w:0,l:0,r:0,reach:0,contact:0,look:0,eye:null,mark:'',anchor:'contact',...CREATIVE_CONTROLS};
function sample(work,p,track=ROUTINES[work.id].track){
 let a=track[0],b=track.at(-1);
 for(let i=1;i<track.length;i++)if(p<=track[i][0]){a=track[i-1];b=track[i];break;}
 let u=clamp((p-a[0])/Math.max(.001,b[0]-a[0]));u=u*u*(3-2*u);
 const defaults={...REST,...work.start};a={...defaults,...a[1]};b={...defaults,...b[1]};const v={...a};
 for(const k of Object.keys(REST))if(typeof REST[k]==='number')v[k]=a[k]+(b[k]-a[k])*u;
 if(work.id==='kite_reel')v.flight*=work.start?.flight||0;
 if(u>.5){v.eye=b.eye;v.mark=b.mark;}
 return {...v,anchorA:a.anchor,anchorB:b.anchor,anchorBlend:u};
}
export function creativePose(work,motion=true){
 const spec=ROUTINES[work?.id];if(!spec||work.interrupted)return null;
 const progress=clamp(work.elapsed/spec.duration),actual=sample(work,progress),pose=motion?actual:sample(work,.5);
 // Reduced motion still shows the real fold, cap and paint. It suppresses
 // incidental acting and wind flutter, never changes the physical state.
 const controls=Object.fromEntries(Object.keys(CREATIVE_CONTROLS).map(k=>[k,actual[k]]));
 const shared=COMPANY[work.company?.id],partner=shared&&work.company.role==='b';
 const acting=partner?sample(work,motion?progress:.5,shared.track):pose,tool=partner?shared.tool:spec.tool;
 // A helper releases a launched kite; it cannot drag the airborne tail back down.
 const contact=partner&&spec.type==='kite'&&controls.flight>.05?0:acting.contact;
 const stepping=!partner&&spec.type==='scope'&&acting.look>0&&acting.look<1?{l:motion?Math.max(0,Math.sin(acting.look*24)):0,r:motion?Math.max(0,-Math.sin(acting.look*24)):0}:{};
 const walking=work.transition?{contact:0,w:.15,reach:0,b:0,x:0,y:0,l:motion?Math.max(0,Math.sin(work.transition.elapsed*10)):0,r:motion?Math.max(0,-Math.sin(work.transition.elapsed*10)):0,eye:null,mark:''}:{};
 return {...acting,...controls,contact,...stepping,...walking,creative:tool!=='none'&&!work.transition,progress,tool,type:spec.type,partner:Boolean(partner),seconds:motion?work.elapsed:0,wind:motion?work.wind||0:0};
}
export function creativeGeometry(home,worker,sx,sy){
 const c=worker.character,pose=creativePose(c.performance.routine,c.performance.motion!==false),unit=sx*home.scale*home.detailScale,uh=unit*1.5,cw=c.scale*sx,ch=cw*1.5;
 const left=home.x*sx-home.width*unit/2,top=home.y*sy-home.art.length*uh,ground=top+home.anchors.entry.y*uh;
 const a=home.anchors[pose.anchorA]||home.anchors.contact,b=home.anchors[pose.anchorB]||home.anchors.contact;
 const target={x:left+(a.x+(b.x-a.x)*pose.anchorBlend+.5)*unit,y:top+(a.y+(b.y-a.y)*pose.anchorBlend+.5)*uh};
 const rest=c.workGripRest||c.grip||{x:c.anchorX+5,y:c.groundRow-6},eye=c.rig?.eye||c.bill||rest,neutralEye=c.rig?.restEye||eye;
 const partner=worker.slot===1,scope=pose.type==='scope'&&!partner,look=scope?pose.look:0,ocular=home.anchors.eye;
 const eyeTarget=ocular?{x:left+(ocular.x+.5)*unit,y:top+(ocular.y+.5)*uh}:target;
 let workX=target.x-3*cw-(rest.x+.5-c.anchorX)*cw,workY=ground;
 const painting=pose.type==='easel'&&pose.tool!=='none'&&!partner;
 const work=c.performance.routine,spec=ROUTINES[work.id],peek=spec.track.find(([,v])=>v.look===1);
 const fixedEye=peek?scopeEyepiece(sample(work,peek[0])):null;
 const platformX=scope&&fixedEye?left+(fixedEye.x+.5)*unit-(neutralEye.x+.5-c.anchorX)*cw:left+home.width*.5*unit;
 // Dimensions come from the prop and neutral anatomy. The platform never moves
 // with the character's head, brush target, current height, or climb progress.
 const step=scope&&fixedEye?Math.max(0,ground-(top+(fixedEye.y+.5)*uh+(c.groundRow-neutralEye.y-.5)*ch)):painting?Math.max(0,ground-(top+home.art.length*.46*uh+(c.groundRow-rest.y-.5)*ch)):0;
 const platformY=ground-step,half=painting?home.width*.5*unit+3*cw:7*cw,platformLeft=platformX-half,platformRight=platformX+half;
 const stairCount=Math.max(1,Math.ceil(step/(2*ch))),rise=step/stairCount,run=2.4*cw;
 const points=[],supports=[];
 const put=(x,y,glyph,color='#d9c49b',array=points)=>array.push({x,y,glyph,color});
 const line=(a,b,glyph,color,array=points)=>{const n=Math.max(1,Math.ceil(Math.max(Math.abs(b.x-a.x)/cw,Math.abs(b.y-a.y)/ch)));for(let i=0;i<=n;i++)put(a.x+(b.x-a.x)*i/n,a.y+(b.y-a.y)*i/n,glyph||((b.x-a.x)*(b.y-a.y)>0?'\\':'/'),color,array);};
 if(step>1){
  for(const x of [platformLeft,platformRight])line({x,y:platformY},{x,y:ground},'|','#af946f',supports);
  line({x:platformLeft,y:platformY},{x:platformRight,y:ground},'\\','#8f8063',supports);
  line({x:platformRight,y:platformY},{x:platformLeft,y:ground},'/','#8f8063',supports);
  line({x:platformLeft-cw,y:platformY},{x:platformRight+cw,y:platformY},'=','#d4b98b',supports);
  line({x:platformLeft-stairCount*run,y:ground},{x:platformLeft,y:platformY},'/','#8f8063',supports);
  for(let n=1;n<=stairCount;n++){
   const x=platformLeft-n*run,y=platformY+n*rise;
   line({x,y},{x:x+run,y},'=','#c6ab80',supports);
   line({x:x+run,y},{x:x+run,y:y-rise},'|','#a18a66',supports);
  }
 }
 // On the staircase the body stands on a real tread; all of the D10 body and
 // short legs retain their original scale. The working deck stays fixed.
 function climb(amount,startX,startY,endX){
  const u=clamp(amount),bottomX=platformLeft-stairCount*run+run*.5;
  if(u<.2){const q=u/.2;return {x:startX+(bottomX-startX)*q,y:startY+(ground-startY)*q};}
  if(u>=.85){const q=(u-.85)/.15;return {x:platformLeft+(endX-platformLeft)*q,y:platformY};}
  const n=Math.max(1,Math.ceil((1-(u-.2)/.65)*stairCount));
  return {x:platformLeft-n*run+run*.5,y:platformY+n*rise};
 }
 let climbing=false;
 if(partner){
  const edge=left+home.width*unit+5*cw-((c.bill?.x??c.anchorX)+.5-c.anchorX)*cw;
  const hold=target.x+3*cw-(rest.x+.5-c.anchorX)*cw;
  workX=edge+(hold-edge)*pose.contact;
  if(c.rig?.species==='butterfly')workY-=5*ch;
 }else if(scope&&peek){
  const viewingX=eyeTarget.x-(eye.x+.5-c.anchorX)*cw;
  if(look>.001){const at=climb(look,workX,ground,viewingX);workX=at.x;workY=at.y;climbing=look<1;}
 }else if(painting){
  workX=Math.max(platformLeft+3*cw,Math.min(platformRight-3*cw,workX));
  const at=climb(worker.inside,c.x*sx,c.y*sy,workX);workX=at.x;workY=at.y;climbing=worker.inside<1;
 }
 const inside=clamp(worker.inside);
 const character={...c,x:painting?workX/sx:c.x+(workX/sx-c.x)*inside,y:painting?workY/sy:c.y+(workY/sy-c.y)*inside,offsetY:0};
 const grip=c.grip||rest,cl=Math.round(character.x*sx-c.anchorX*cw+(c.offsetX||0)*cw),ct=Math.round(character.y*sy-c.groundRow*ch);
 const hand={x:cl+(grip.x+.5)*cw,y:ct+(grip.y+.5)*ch};
 let tip=null;
 if(!climbing&&pose.tool!=='none'&&pose.contact>.01&&worker.inside>.01&&c.rig?.species!=='butterfly'){
  const u=pose.contact*worker.inside,idle={x:hand.x+(partner?-3:3)*cw,y:hand.y-ch};tip={x:idle.x+(target.x-idle.x)*u,y:idle.y+(target.y-idle.y)*u};
  line(hand,tip,null,pose.tool==='brush'?'#bd9668':'#d5bd8b');put(hand.x,hand.y,')','#ead8b5');
  if(pose.tool==='brush'){put(tip.x,tip.y,'#',pose.anchorB==='rinse'?'#8cc9d8':'#a3c3ae');put(tip.x-cw*.6,tip.y-ch*.4,':','#e2d3aa');}
  else if(pose.tool==='cloth')for(let y=-1;y<=1;y++)for(let x=-2;x<=2;x++)put(tip.x+x*cw,tip.y+y*ch,y===0?'~':':','#bfd5ca');
  else put(tip.x,tip.y,scope?'J':')','#edd9ac');
 }
 return {character,pose,cw,ground,hand,tip,target,eyeTarget,step,points,supports,platform:{x:platformX,y:platformY,left:platformLeft,right:platformRight},climbing};
}
export function drawCreativeTools(ctx,staged,behind=false){
 ctx.save();ctx.font='600 '+staged.cw*1.5+'px Menlo, monospace';ctx.textAlign='center';ctx.textBaseline='middle';ctx.strokeStyle='#162b25';ctx.lineWidth=Math.max(.6,staged.cw*.15);
 for(const p of behind?staged.supports:staged.points){ctx.fillStyle=p.color;ctx.strokeText(p.glyph,p.x,p.y);ctx.fillText(p.glyph,p.x,p.y);}ctx.restore();
}
