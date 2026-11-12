import {actorPitches} from './actor-projection.mjs';
import ROUTINES from './animation/playkit-routines.json' with {type:'json'};
import COMPANY from './animation/playkit-company.json' with {type:'json'};
export {COMPANY as PLAYKIT_COMPANY};
import {PLAYKIT_BLUEPRINTS} from './playkit-workshop.mjs';
export {ROUTINES as PLAYKIT_ROUTINES};
export const PLAYKIT_CONTROLS={travel:0,lift:0,turn:0,coil:0,power:0,dip:0,blow:0,walk:0,tilt:0,jump:0,drop:1,held:0,wide:0,sail:0};
const REST={...PLAYKIT_CONTROLS,u:1.08,v:0,x:0,y:0,b:0,w:0,l:0,r:0,reach:0,contact:0,eye:null,mark:''},clamp=n=>Math.max(0,Math.min(1,n));
function sample(work,track,base){
 const p=clamp(work.elapsed/ROUTINES[work.id].duration);let a=track[0],b=track.at(-1);
 for(let i=1;i<track.length;i++)if(p<=track[i][0]){a=track[i-1];b=track[i];break;}
 let u=clamp((p-a[0])/Math.max(.001,b[0]-a[0]));u=u*u*(3-2*u);a={...base,...a[1]};b={...base,...b[1]};const pose={...a};
 for(const k in REST)if(typeof REST[k]==='number')pose[k]=a[k]+(b[k]-a[k])*u;
 if(u>.5){pose.eye=b.eye;pose.mark=b.mark;}return pose;
}
export function playkitPose(work,motion=true){
 const spec=ROUTINES[work?.id];if(!spec||work.interrupted)return null;
 const leader=sample(work,spec.track,{...REST,...work.start}),shared=COMPANY[work.company?.id],partner=Boolean(shared&&work.company.role==='b');
 const pose=partner?sample(work,shared.track,REST):leader,tool=partner?shared.tool:spec.tool,anchor=partner?shared.anchor:spec.anchor;
 const actorJump=pose.jump;
 // Mechanisms follow the one native control clock. The partner has a separate
 // articulated pose and does not inherit Cheese's jumps or locomotion.
 for(const k in PLAYKIT_CONTROLS)pose[k]=leader[k];
 if(!partner)pose.x+=pose.tilt*.8;
 if(!motion){pose.x=pose.y=pose.l=pose.r=pose.w=0;pose.mark='';}
 if(work.transition)Object.assign(pose,{contact:0,w:.1,reach:0,b:0,x:0,y:0,l:motion?Math.max(0,Math.sin(work.transition.elapsed*10)):0,r:motion?Math.max(0,-Math.sin(work.transition.elapsed*10)):0,eye:null,mark:''});
 return {...pose,partner,actorU:pose.u,actorV:pose.v,actorJump,playkit:tool!=='none'&&!work.transition,tool,anchor,type:spec.type,progress:clamp(work.elapsed/spec.duration)};
}
export function playkitGeometry(home,worker,sx,sy){
 const c=worker.character,pose=playkitPose(c.performance.routine,c.performance.motion!==false),p=PLAYKIT_BLUEPRINTS[home.blueprint],unit=sx*home.scale*home.detailScale,uh=unit*1.5,{cw,ch}=actorPitches(c,sx,sy);
 const left=home.x*sx-home.width*unit/2,top=home.y*sy-home.art.length*uh,ground=top+home.anchors.entry.y*uh,anchor=home.anchors[pose.anchor]||home.anchors.contact;
 const target={x:left+(anchor.x+.5)*unit,y:top+(anchor.y+.5)*uh},rest=c.workGripRest||c.grip||{x:c.anchorX+5,y:c.groundRow-6},grip=c.grip||rest;
 const range=p.type==='boat'?65:p.type==='yoyo'?45:83;
 const idleX=pose.partner?left+p.w*pose.actorU*unit:left+(home.anchors.entry.x+pose.walk*range)*unit-(['rope','board'].includes(p.type)?0:(rest.x+.5-c.anchorX)*cw+3*cw),holdX=target.x+(pose.partner?2:-2)*cw-(rest.x+.5-c.anchorX)*cw;
 let x=pose.tool==='none'||pose.tool==='string'?idleX:idleX+(holdX-idleX)*pose.contact,y=ground+(pose.partner&&c.rig?.species==='butterfly'?pose.actorV*10*uh:0);
 if(!pose.partner&&p.type==='board'&&pose.tool==='none'&&pose.walk>.01){x=left+home.anchors.deck.x*unit;y=ground+(top+home.anchors.deck.y*uh-ground)*clamp(pose.walk/.15);}
 if(p.type==='rope')y-=pose.actorJump*2.2*ch;
 if(c.rig?.species==='butterfly')y-=5*ch;
 const character={...c,x:c.x+(x/sx-c.x)*worker.inside,y:c.y+(y/sy-c.y)*worker.inside,offsetY:0};
 const hand={x:character.x*sx+(grip.x+.5-c.anchorX)*cw,y:character.y*sy+(grip.y+.5-c.groundRow)*ch},points=[];
 const put=(x,y,glyph,color='#e2c99c')=>points.push({x,y,glyph,color});
 const line=(a,b,glyph,color)=>{const n=Math.max(1,Math.ceil(Math.max(Math.abs(b.x-a.x)/cw,Math.abs(b.y-a.y)/ch)));for(let i=0;i<=n;i++)put(a.x+(b.x-a.x)*i/n,a.y+(b.y-a.y)*i/n,glyph||((b.x-a.x)*(b.y-a.y)>0?'\\':'/'),color);};
 let tip=null;
 if(pose.contact>.01&&worker.inside>.01&&pose.tool!=='none'&&c.rig?.species!=='butterfly'){
  const u=pose.contact*worker.inside,restTip={x:hand.x+2*cw,y:hand.y};tip={x:restTip.x+(target.x-restTip.x)*u,y:restTip.y+(target.y-restTip.y)*u};
  if(pose.tool==='string'){
   const a=home.anchors.axle;tip={x:left+a.x*unit,y:top+a.y*uh};line(hand,tip,':','#eee1be');
  }else if(pose.tool==='wand'&&pose.held>.05){
   const bill=c.bill||c.rig?.eye||rest;tip={x:character.x*sx+(bill.x+3.5-c.anchorX)*cw,y:character.y*sy+(bill.y+.5-c.groundRow)*ch};
   line(hand,{x:tip.x,y:tip.y+2*ch},null,'#ebc979');
   for(const [i,row]of [' .-. ','(   )'," '-' "].entries())for(const [j,g]of [...row].entries())if(g!==' ')put(tip.x+(j-2)*cw,tip.y+(i-1)*ch,g,'#d9dcbc');
   if(pose.blow>.5)put(tip.x+3*cw,tip.y,'.','#a0dae1');
  }else{
   line(hand,tip,null,'#c6ad80');put(hand.x,hand.y,')');
   if(pose.tool==='cloth')for(let yy=-1;yy<=1;yy++)for(let xx=-2;xx<=2;xx++)put(tip.x+xx*cw*.65,tip.y+yy*ch*.6,yy===0?'~':':','#c6d8c0');else put(tip.x,tip.y,')');
  }
 }
 if(p.type==='wand'&&!pose.partner){
  // The real native particle age determines drift. Its source is the held loop
  // beside this character's bill, rather than the bottle on the ground.
  const bill=c.bill||c.rig?.eye||rest,origin={x:holdX+(bill.x+3.5-c.anchorX)*cw,y:ground+(bill.y+.5-c.groundRow)*ch};
  for(const b of home.playkitState?.bubbles||[]){
   const x=origin.x+(2+b.age*(1.4+b.lane*.12))*cw,y=origin.y-b.age*1.15*ch,rx=(1.1+b.size*.9)*cw,ry=(.7+b.size*.45)*ch;
   for(let n=0;n<16;n++){const a=n*Math.PI/8;put(x+Math.cos(a)*rx,y+Math.sin(a)*ry,n%4===0?'o':'.',n<8?'#91d2dc':'#d5b5da');}
   put(x-rx*.4,y-ry*.35,'/','#e8e1c6');
  }
 }
 return {character,pose,cw,ground,hand,tip,target,points};
}
export function drawPlaykitTools(ctx,staged){ctx.save();ctx.font='600 '+staged.cw*1.5+'px Menlo, monospace';ctx.textAlign='center';ctx.textBaseline='middle';ctx.strokeStyle='#172f27';ctx.lineWidth=Math.max(.6,staged.cw*.15);for(const p of staged.points){ctx.fillStyle=p.color;ctx.strokeText(p.glyph,p.x,p.y);ctx.fillText(p.glyph,p.x,p.y);}ctx.restore();}
