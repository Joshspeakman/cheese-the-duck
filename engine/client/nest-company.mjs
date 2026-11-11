import {nestPose} from './nest-routines.mjs';

// An outside helper keeps its own natural body scale and ground contact. The
// short wing-to-rim contact belongs to this actor, never to the nest's occupant.
export function nestHelpGeometry(home,helper,sx,sy){
 const c=helper.character,pose=nestPose(c.performance.routine,c.performance.motion!==false);
 const unit=sx*home.scale*home.detailScale,hh=unit*1.5,cw=c.scale*sx,ch=cw*1.5;
 const left=home.x*sx-home.width*unit/2,top=home.y*sy-home.art.length*hh;
 const anchor=pose.anchor==='left'?home.anchors.workLeft:home.anchors.workRight;
 const target={x:left+(anchor.x+.5)*unit,y:top+(anchor.y+.5)*hh};
 const side=pose.anchor==='left'?1:-1,rest=c.workGripRest||c.grip||{x:c.anchorX+side*5,y:c.groundRow-7};
 const workX=target.x-(rest.x+.5-c.anchorX)*cw-side*1.5*cw;
 const ground=home.y*sy-2*hh,hover=c.rig?.species==='butterfly'?5*ch:0;
 const character={...c,x:c.x+(workX/sx-c.x)*helper.inside,y:c.y+((ground-hover)/sy-c.y)*helper.inside,offsetY:0};
 const cl=Math.round(character.x*sx-c.anchorX*cw+(c.offsetX||0)*cw),ct=Math.round(character.y*sy-c.groundRow*ch);
 const grip=c.grip||rest,hand={x:cl+(grip.x+.5)*cw,y:ct+(grip.y+.5)*ch};
 const points=[];let tip=null;
 if(pose.contact>.01&&helper.inside>.01&&c.rig?.species!=='butterfly'){
  const blend=pose.contact*helper.inside;tip={x:hand.x+(target.x-hand.x)*blend,y:hand.y+(target.y-hand.y)*blend};
  const count=Math.ceil(Math.max(Math.abs(tip.x-hand.x)/cw,Math.abs(tip.y-hand.y)/ch));
  for(let i=1;i<=count;i++){const q=i/count;points.push({x:hand.x+(tip.x-hand.x)*q,y:hand.y+(tip.y-hand.y)*q,glyph:i===count?'v':side>0?'/':'\\'});}
 }
 return {character,pose,cw,ch,ground,hand,tip,target,points};
}
export function drawNestHelp(ctx,staged){
 ctx.save();ctx.font='600 '+staged.cw*1.5+'px Menlo, monospace';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillStyle=staged.character.face;ctx.strokeStyle='#14291f';ctx.lineWidth=Math.max(.6,staged.cw*.15);
 for(const p of staged.points){ctx.strokeText(p.glyph,p.x,p.y);ctx.fillText(p.glyph,p.x,p.y);}ctx.restore();
}
