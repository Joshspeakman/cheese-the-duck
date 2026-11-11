import ROUTINES from './animation/creative-routines.json' with {type:'json'};
export {ROUTINES as CREATIVE_ROUTINES};
const clamp=n=>Math.max(0,Math.min(1,n));
export const CREATIVE_CONTROLS={aim:.35,focus:.5,cap:1,fold:0,cover:0,flight:0,stroke:0};
const REST={x:0,y:0,b:0,w:0,l:0,r:0,reach:0,contact:0,look:0,eye:null,mark:'',anchor:'contact',...CREATIVE_CONTROLS};
function sample(work,p){
 const track=ROUTINES[work.id].track;let a=track[0],b=track.at(-1);
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
 return {...pose,...controls,creative:spec.tool!=='none',progress,tool:spec.tool,type:spec.type,seconds:motion?work.elapsed:0,wind:motion?work.wind||0:0};
}
export function creativeGeometry(home,worker,sx,sy){
 const c=worker.character,pose=creativePose(c.performance.routine,c.performance.motion!==false),unit=sx*home.scale*home.detailScale,uh=unit*1.5,cw=c.scale*sx,ch=cw*1.5;
 const left=home.x*sx-home.width*unit/2,top=home.y*sy-home.art.length*uh,ground=top+home.anchors.entry.y*uh;
 const a=home.anchors[pose.anchorA]||home.anchors.contact,b=home.anchors[pose.anchorB]||home.anchors.contact;
 const target={x:left+(a.x+(b.x-a.x)*pose.anchorBlend+.5)*unit,y:top+(a.y+(b.y-a.y)*pose.anchorBlend+.5)*uh};
 const rest=c.workGripRest||c.grip||{x:c.anchorX+5,y:c.groundRow-6},eye=c.rig?.eye||c.bill||rest;
 const scope=pose.type==='scope',look=scope?pose.look:0,ocular=home.anchors.eye;
 const eyeTarget=ocular?{x:left+(ocular.x+.5)*unit,y:top+(ocular.y+.5)*uh}:target;
 let workX=target.x-3*cw-(rest.x+.5-c.anchorX)*cw;
 let workY=ground;
 // A broad viewing step supports little bodies at the real eyepiece. The
 // character is translated as a whole; no neck, leg or wing gets stretched.
 const painting=pose.type==='easel'&&pose.tool!=='none';
 const step=scope?Math.max(0,ground-(eyeTarget.y+(c.groundRow-eye.y-.5)*ch)):painting?Math.max(0,ground-(top+home.art.length*.46*uh+(c.groundRow-rest.y-.5)*ch)):0;
 const viewingX=eyeTarget.x-(eye.x+.5-c.anchorX)*cw;
 workX+=(viewingX-workX)*look;workY-=step*(scope?look:1);
 const character={...c,x:c.x+(workX/sx-c.x)*worker.inside,y:c.y+(workY/sy-c.y)*worker.inside,offsetY:0};
 const grip=c.grip||rest,cl=Math.round(character.x*sx-c.anchorX*cw+(c.offsetX||0)*cw),ct=Math.round(character.y*sy-c.groundRow*ch);
 const hand={x:cl+(grip.x+.5)*cw,y:ct+(grip.y+.5)*ch},points=[],supports=[];
 const put=(x,y,glyph,color='#d9c49b',array=points)=>array.push({x,y,glyph,color});
 const line=(a,b,glyph,color,array=points)=>{const n=Math.max(1,Math.ceil(Math.max(Math.abs(b.x-a.x)/cw,Math.abs(b.y-a.y)/ch)));for(let i=0;i<=n;i++)put(a.x+(b.x-a.x)*i/n,a.y+(b.y-a.y)*i/n,glyph||((b.x-a.x)*(b.y-a.y)>0?'\\':'/'),color,array);};
 if(step>1&&(look>.02||painting)&&worker.inside>.01){
  const x=character.x*sx,y=character.y*sy;
  // Braced wooden working steps are visible below the feet.
  line({x:x-6*cw,y},{x:x+6*cw,y:ground},'\\','#8f8063',supports);
  line({x:x+6*cw,y},{x:x-6*cw,y:ground},'/','#8f8063',supports);
  for(const dx of [-6,6])line({x:x+dx*cw,y},{x:x+dx*cw,y:ground},'|','#af946f',supports);
  line({x:x-7*cw,y},{x:x+7*cw,y},'=','#d4b98b',supports);
  for(let yy=y+ch*2;yy<ground;yy+=ch*2)line({x:x-6*cw,y:yy},{x:x+6*cw,y:yy},'-','#8f8063',supports);
 }
 let tip=null;
 if(pose.tool!=='none'&&pose.contact>.01&&worker.inside>.01&&c.rig?.species!=='butterfly'){
  const u=pose.contact*worker.inside,idle={x:hand.x+3*cw,y:hand.y-ch};tip={x:idle.x+(target.x-idle.x)*u,y:idle.y+(target.y-idle.y)*u};
  line(hand,tip,null,pose.tool==='brush'?'#bd9668':'#d5bd8b');put(hand.x,hand.y,')','#ead8b5');
  if(pose.tool==='brush'){put(tip.x,tip.y,'#',pose.anchorB==='rinse'?'#8cc9d8':'#a3c3ae');put(tip.x-cw*.6,tip.y-ch*.4,':','#e2d3aa');}
  else if(pose.tool==='cloth')for(let y=-1;y<=1;y++)for(let x=-2;x<=2;x++)put(tip.x+x*cw,tip.y+y*ch,y===0?'~':':','#bfd5ca');
  else put(tip.x,tip.y,scope?'J':')','#edd9ac');
 }
 return {character,pose,cw,ground,hand,tip,target,eyeTarget,step,points,supports};
}
export function drawCreativeTools(ctx,staged,behind=false){
 ctx.save();ctx.font='600 '+staged.cw*1.5+'px Menlo, monospace';ctx.textAlign='center';ctx.textBaseline='middle';ctx.strokeStyle='#162b25';ctx.lineWidth=Math.max(.6,staged.cw*.15);
 for(const p of behind?staged.supports:staged.points){ctx.fillStyle=p.color;ctx.strokeText(p.glyph,p.x,p.y);ctx.fillText(p.glyph,p.x,p.y);}ctx.restore();
}
