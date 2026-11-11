import ROUTINES from './animation/lighting-routines.json' with {type:'json'};
export {ROUTINES as LIGHTING_ROUTINES};
const clamp=n=>Math.max(0,Math.min(1,n));
const REST={x:0,y:0,b:0,w:0,l:0,r:0,reach:0,contact:0,pull:0,turn:0,pump:0,eye:null,mark:''};
export function lightingPose(routine,motion=true){
 const spec=ROUTINES[routine?.id];if(!spec||routine.interrupted)return null;
 const progress=motion?clamp(routine.elapsed/spec.duration):.5,track=spec.track;
 let a=track[0],b=track.at(-1);
 for(let i=1;i<track.length;i++)if(progress<=track[i][0]){a=track[i-1];b=track[i];break;}
 let u=clamp((progress-a[0])/Math.max(.001,b[0]-a[0]));u=u*u*(3-2*u);a={...REST,...a[1]};b={...REST,...b[1]};const pose={...a};
 for(const k of Object.keys(REST))if(typeof REST[k]==='number')pose[k]=a[k]+(b[k]-a[k])*u;
 if(u>.5){pose.eye=b.eye;pose.mark=b.mark;}
 return {...pose,lighting:!spec.observe,observe:!!spec.observe,progress,tool:spec.tool};
}
export function lightingGeometry(home,worker,sx,sy){
 const c=worker.character,pose=lightingPose(c.performance.routine,c.performance.motion!==false);
 const unit=sx*home.scale*home.detailScale,ch=unit*1.5,cw=c.scale*sx,hh=cw*1.5;
 const left=home.x*sx-home.width*unit/2,top=home.y*sy-home.art.length*ch;
 const anchor=home.anchors.control||home.anchors.contact,ground=top+home.anchors.entry.y*ch;
 const target={x:left+(anchor.x+.5)*unit,y:top+(anchor.y+.5+pose.pull)*ch};
 const rest=c.workGripRest||c.grip||{x:c.anchorX+5,y:c.groundRow-6};
 const workX=left+anchor.x*unit-(pose.observe?20:12)*cw-(rest.x-c.anchorX)*cw;
 const character={...c,x:c.x+(workX/sx-c.x)*worker.inside,y:c.y+(ground/sy-c.y)*worker.inside,offsetY:0};
 const grip=c.grip||rest,cl=Math.round(character.x*sx-c.anchorX*cw+(c.offsetX||0)*cw),ct=Math.round(character.y*sy-c.groundRow*hh);
 const hand={x:cl+(grip.x+.5)*cw,y:ct+(grip.y+.5)*hh},points=[];
 const put=(x,y,glyph,color='#d8bf8b')=>points.push({x,y,glyph,color});
 const line=(a,b,glyph=null,color='#c9af7c')=>{const n=Math.max(1,Math.ceil(Math.max(Math.abs(a.x-b.x)/cw,Math.abs(a.y-b.y)/hh)));for(let i=0;i<=n;i++){const f=i/n;put(a.x+(b.x-a.x)*f,a.y+(b.y-a.y)*f,glyph||((b.x-a.x)*(b.y-a.y)>0?'\\':'/'),color);}};
 let tip=null;
 if(!pose.observe&&worker.inside>.01){
  const idle={x:hand.x+7*cw,y:hand.y-3*hh},contact=pose.contact*worker.inside;
  tip={x:idle.x+(target.x-idle.x)*contact,y:idle.y+(target.y-idle.y)*contact};
  // A held lamp-lighter reaches the real chain/knob; wings stay attached and
  // feet stay on the ground for every age. No stretching a hatchling's body.
  line(hand,tip);put(hand.x,hand.y,')','#e1cc9d');
  if(pose.tool==='bellows'){
   const spread=1.5+(1-pose.pump)*2.5;
   line({x:hand.x+cw,y:hand.y-spread*hh},{x:hand.x+5*cw,y:hand.y},'/','#bd9668');
   line({x:hand.x+cw,y:hand.y+spread*hh},{x:hand.x+5*cw,y:hand.y},'\\','#bd9668');
   line({x:hand.x+cw,y:hand.y-spread*hh},{x:hand.x+cw,y:hand.y+spread*hh},':','#d2b68b');put(tip.x,tip.y,'>','#dcc599');
   if(pose.pump>.8&&contact>.9)put(tip.x+cw*2,tip.y,'.','#e9d1a5');
  }else{
   put(tip.x,tip.y,pose.tool==='rod'?(pose.turn>0?'/':'\\'):'J','#e7cc94');
   if(contact>.95)put(tip.x+cw,tip.y,'o','#d9ceb2');
  }
 }
 return {character,pose,cw,hand,tip,target,ground,points};
}
export function drawLightingTools(ctx,staged){
 ctx.save();ctx.font='600 '+staged.cw*1.5+'px Menlo, monospace';ctx.textAlign='center';ctx.textBaseline='middle';ctx.strokeStyle='#162b25';ctx.lineWidth=Math.max(.7,staged.cw*.15);
 for(const p of staged.points){ctx.fillStyle=p.color;ctx.strokeText(p.glyph,p.x,p.y);ctx.fillText(p.glyph,p.x,p.y);}ctx.restore();
}
