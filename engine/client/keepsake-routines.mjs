import ROUTINES from './animation/keepsake-routines.json' with {type:'json'};
import COMPANY from './animation/keepsake-company.json' with {type:'json'};
export {ROUTINES as KEEPSAKE_ROUTINES,COMPANY as KEEPSAKE_COMPANY};
const clamp=n=>Math.max(0,Math.min(1,n));
const REST={x:0,y:0,b:0,w:0,l:0,r:0,reach:0,contact:0,open:0,sort:0,turn:0,wipe:0,fold:0,pour:0,eye:null,mark:'',anchor:'contact'};
function sample(track,progress,rest){
 let a=track[0],b=track.at(-1);
 for(let i=1;i<track.length;i++)if(progress<=track[i][0]){a=track[i-1];b=track[i];break;}
 let u=clamp((progress-a[0])/Math.max(.001,b[0]-a[0]));u=u*u*(3-2*u);a={...rest,...a[1]};b={...rest,...b[1]};const pose={...a};
 for(const k of Object.keys(rest))if(typeof rest[k]==='number')pose[k]=a[k]+(b[k]-a[k])*u;
 if(u>.5){pose.eye=b.eye;pose.mark=b.mark;}
 // Target interpolation keeps a pointer travelling continuously from one
 // physical feature to another, instead of teleporting between anchor names.
 return {...pose,anchorA:a.anchor,anchorB:b.anchor,anchorBlend:u};
}
export function keepsakePose(work,motion=true){
 const spec=ROUTINES[work?.id];if(!spec||work.interrupted)return null;
 const progress=motion?clamp(work.elapsed/spec.duration):.5,rest={...REST,open:work.start_open||0};
 const base=sample(spec.track,progress,rest),shared=COMPANY[work.company?.id];
 const walking=work.transition?{contact:0,w:.15,reach:0,b:0,x:0,y:0,l:motion?Math.max(0,Math.sin(work.transition.elapsed*10)):0,r:motion?Math.max(0,-Math.sin(work.transition.elapsed*10)):0,eye:null,mark:''}:{};
 if(shared&&work.company.role==='b')return {...sample(shared.track,progress,rest),...walking,keepsake:shared.tool!=='none'&&!work.transition,progress,tool:shared.tool,reader:true};
 // The lead keeps the original mechanical contact and openness. Only the
 // listening expression changes; a companion cannot turn a second page.
 const response=shared?sample(shared.lead,progress,REST):null;
 return {...base,...(response?{eye:response.eye??base.eye,mark:response.mark||base.mark}:{}),...walking,keepsake:!work.transition,progress,tool:spec.tool||'hook'};
}
export function keepsakeGeometry(home,worker,sx,sy){
 const c=worker.character,pose=keepsakePose(c.performance.routine,c.performance.motion!==false),unit=sx*home.scale*home.detailScale,hh=unit*1.5;
 const left=home.x*sx-home.width*unit/2,top=home.y*sy-home.art.length*hh,ground=top+home.anchors.entry.y*hh;
 const A=home.anchors[pose.anchorA]||home.anchors.contact,B=home.anchors[pose.anchorB]||home.anchors.contact;
 const target={x:left+(A.x+(B.x-A.x)*pose.anchorBlend+.5)*unit,y:top+(A.y+(B.y-A.y)*pose.anchorBlend+.5)*hh};
 const cw=c.scale*sx,ch=cw*1.5,rest=c.workGripRest||c.grip||{x:c.anchorX+5,y:c.groundRow-7};
 // Move along the front edge to the part being handled. Staying at one end
 // made every page turn look like a fishing rod reaching across the book.
 const workX=worker.slot===1?left+home.width*unit+6*cw-((c.bill?.x??c.anchorX)+.5-c.anchorX)*cw:target.x-2*cw-(rest.x-c.anchorX)*cw;
 const hovering=c.rig?.species==='butterfly'?ch*5:0;
 const character={...c,x:c.x+(workX/sx-c.x)*worker.inside,y:c.y+((ground-hovering)/sy-c.y)*worker.inside,offsetY:0};
 const grip=c.grip||rest,cl=Math.round(character.x*sx-c.anchorX*cw+(c.offsetX||0)*cw),ct=Math.round(character.y*sy-c.groundRow*ch);
 const hand={x:cl+(grip.x+.5)*cw,y:ct+(grip.y+.5)*ch},points=[];
 const put=(x,y,glyph,color='#d9c49b')=>points.push({x,y,glyph,color});
 let tip=null;
 if(pose.tool!=='none'&&c.rig?.species!=='butterfly'&&pose.contact>.01&&worker.inside>.01){
  const u=pose.contact*worker.inside,idle={x:hand.x+(c.facing===false?-5:5)*cw,y:hand.y-ch*2};tip={x:idle.x+(target.x-idle.x)*u,y:idle.y+(target.y-idle.y)*u};
  const n=Math.max(1,Math.ceil(Math.max(Math.abs(tip.x-hand.x)/cw,Math.abs(tip.y-hand.y)/ch)));
  for(let i=0;i<=n;i++){const q=i/n;put(hand.x+(tip.x-hand.x)*q,hand.y+(tip.y-hand.y)*q,(tip.x-hand.x)*(tip.y-hand.y)>0?'\\':'/');}
  put(hand.x,hand.y,')','#e5d5b2');
  if(pose.tool==='cloth')for(let y=-1;y<=1;y++)for(let x=-2;x<=2;x++)put(tip.x+x*cw,tip.y+y*ch,y===0?'~':':','#bad6ca');
  else put(tip.x,tip.y,pose.tool==='hook'?'J':'.','#e9dfb9');
 }
 return {character,pose,ground,cw,hand,tip,target,points};
}
export function drawKeepsakeTools(ctx,staged){
 ctx.save();ctx.font='600 '+staged.cw*1.5+'px Menlo, monospace';ctx.textAlign='center';ctx.textBaseline='middle';ctx.strokeStyle='#172b24';ctx.lineWidth=Math.max(.6,staged.cw*.15);
 for(const p of staged.points){ctx.fillStyle=p.color;ctx.strokeText(p.glyph,p.x,p.y);ctx.fillText(p.glyph,p.x,p.y);}ctx.restore();
}
