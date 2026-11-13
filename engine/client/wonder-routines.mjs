// Timed wonder work: D10 rig joints plus the object parts each routine moves.
// Native wonders.py owns the clock and every material effect; this module only
// samples the authored track the same way (smoothstep between keyframes).
import {actorPitches} from './actor-projection.mjs';
import ROUTINES from './animation/wonder-routines.json' with {type:'json'};
export {ROUTINES as WONDER_ROUTINES};
const clamp=n=>Math.max(0,Math.min(1,n));
const JOINTS={x:0,y:0,b:0,w:0,l:0,r:0,reach:0,contact:0};
const PARTS=Object.fromEntries(Object.entries(ROUTINES).map(([key,s])=>[key,[...new Set(s.track.flatMap(([,p])=>Object.keys(p)).filter(k=>!(k in JOINTS)&&!['eye','mark','anchor'].includes(k)))]]));
// A keyframe without an anchor holds the nearest authored one (previous, else
// next), so a wing easing off a part does not slide toward the object's middle.
function heldAnchors(track){
 const out=track.map(([,p])=>p.anchor||null);let last=null;
 for(let i=0;i<out.length;i++){if(out[i])last=out[i];else out[i]=last;}
 let next=null;for(let i=out.length-1;i>=0;i--){if(track[i][1].anchor)next=track[i][1].anchor;if(!out[i])out[i]=next;}
 return out.map(a=>a||'contact');
}
export function sampleTrack(track,progress,keys){
 let ia=0,ib=track.length-1;
 for(let i=1;i<track.length;i++)if(progress<=track[i][0]){ia=i-1;ib=i;break;}
 const a=track[ia],b=track[ib],held=heldAnchors(track);
 let u=clamp((progress-a[0])/Math.max(.001,b[0]-a[0]));u=u*u*(3-2*u);
 const out={};for(const k of keys){const va=a[1][k]??0,vb=b[1][k]??0;out[k]=va+(vb-va)*u;}
 out.eye=u>.5?b[1].eye??null:a[1].eye??null;out.mark=u>.5?b[1].mark??'':a[1].mark??'';
 out.anchorA=held[ia];out.anchorB=held[ib];out.anchorBlend=u;
 return out;
}
// A visitor keeping Cheese company reacts at the routine's actual contact
// moments, in a style chosen natively from their personality; a shelter routine
// is shared by sitting close. Derived from the authored events, never invented.
const REACT={cheer:{w:1,b:-.4,eye:'^',mark:'yay!'},nervous:{x:-.7,b:.4,eye:'O',mark:'!'},steady:{y:.3,eye:'-',mark:'mm'},curious:{x:.6,y:.2,eye:'o',mark:'?'}};
const LEAN={cheer:{x:.3,eye:'o'},nervous:{x:-.3,eye:'o'},steady:{eye:'o'},curious:{x:.5,y:.2,eye:'o'}};
const COMPANY=new Map();
export function companyTrack(key,style){
 const id=key+'|'+style;if(COMPANY.has(id))return COMPANY.get(id);
 const spec=ROUTINES[key],keys=[[0,{}]];
 if(spec.tool==='none'&&spec.when.includes('wet')&&spec.duration>=30)keys.push([.15,{y:.8,b:.6,eye:'o'}],[.5,{y:1,b:.8,eye:'-',mark:'~'}],[.85,{y:.8,b:.6,eye:'^'}]);
 else if(!spec.events.length)keys.push([.25,{...LEAN[style]}],[.5,{...REACT[style]}],[.75,{...LEAN[style]}]);
 else for(const [at] of spec.events){if(at-.06>keys.at(-1)[0])keys.push([at-.06,{...LEAN[style]}]);if(at>keys.at(-1)[0])keys.push([at,{...REACT[style]}]);if(at+.08<1&&at+.08>keys.at(-1)[0])keys.push([at+.08,{}]);}
 keys.push([1,{}]);const out={...spec,track:keys,tool:'none'};COMPANY.set(id,out);return out;
}
export function wonderPose(work,motion=true){
 const base=ROUTINES[work?.id];if(!base||work.interrupted)return null;
 const spec=work.company?.mode==='company'?companyTrack(work.id,work.company.style):base;
 const progress=motion?clamp(work.elapsed/spec.duration):.5,parts=work.company?.mode==='company'?[]:PARTS[work.id];
 const pose=sampleTrack(spec.track,progress,[...Object.keys(JOINTS),...parts]);
 // Only parts this routine actually animates override saved object state.
 const object=Object.fromEntries(parts.map(k=>[k,pose[k]]));
 return {...pose,object,wonder:spec.tool!=='none'&&!work.transition,tool:spec.tool,progress,item:spec.item};
}
export function wonderGeometry(home,worker,sx,sy){
 const c=worker.character,pose=wonderPose(c.performance.routine,c.performance.motion!==false),unit=sx*home.scale*home.detailScale,hh=unit*1.5;
 const left=home.x*sx-home.width*unit/2,top=home.y*sy-home.art.length*hh,anchors=home.anchors||{};
 const entry=anchors.entry||{x:home.width/2,y:home.art.length-1},ground=top+entry.y*hh;
 const A=anchors[pose.anchorA]||anchors.contact||entry,B=anchors[pose.anchorB]||anchors.contact||entry;
 const target={x:left+(A.x+(B.x-A.x)*pose.anchorBlend+.5)*unit,y:top+(A.y+(B.y-A.y)*pose.anchorBlend+.5)*hh};
 const {cw,ch}=actorPitches(c,sx,sy),rest=c.workGripRest||c.grip||{x:c.anchorX+5,y:c.groundRow-7};
 // Stand at the object's front edge beside the part being handled; a shelter
 // routine with no tool tucks Cheese in front of the object's centre instead.
 const workX=worker.slot===1?c.x*sx:pose.tool==='none'?left+home.width*unit*.5-(c.anchorX*.2)*cw:target.x-2*cw-(rest.x-c.anchorX)*cw;
 const hovering=c.rig?.species==='butterfly'?ch*5:0;
 // Company (slot 1) stays at its own native root; only the worker is staged at the part.
 const character=worker.slot===1?{...c,offsetY:0}:{...c,x:c.x+(workX/sx-c.x)*worker.inside,y:c.y+((ground-hovering)/sy-c.y)*worker.inside,offsetY:0};
 const grip=c.grip||rest,cl=Math.round(character.x*sx-c.anchorX*cw+(c.offsetX||0)*cw),ct=Math.round(character.y*sy-c.groundRow*ch);
 const hand={x:cl+(grip.x+.5)*cw,y:ct+(grip.y+.5)*ch},points=[];
 const put=(x,y,glyph,color='#d9c49b')=>points.push({x,y,glyph,color});
 let tip=null;
 if(pose.tool!=='none'&&c.rig?.species!=='butterfly'&&pose.contact>.01&&worker.inside>.01){
  const u=pose.contact*worker.inside,idle={x:hand.x+(c.facing===false?-5:5)*cw,y:hand.y-ch*2};tip={x:idle.x+(target.x-idle.x)*u,y:idle.y+(target.y-idle.y)*u};
  const n=Math.max(1,Math.ceil(Math.max(Math.abs(tip.x-hand.x)/cw,Math.abs(tip.y-hand.y)/ch)));
  // A held tool draws its shaft; a bare wing is drawn stretched out to the part
  // (the native reach check already bounds how far that may be), never a tip
  // glyph floating in the air.
  if(pose.tool!=='wing')for(let i=0;i<=n;i++){const q=i/n;put(hand.x+(tip.x-hand.x)*q,hand.y+(tip.y-hand.y)*q,(tip.x-hand.x)*(tip.y-hand.y)>0?'\\':'/');}
  else for(let i=1;i<n;i++){const q=i/n;put(hand.x+(tip.x-hand.x)*q,hand.y+(tip.y-hand.y)*q,q<.5?'=':'~','#f2e3b5');}
  put(hand.x,hand.y,')','#e5d5b2');
  const head={shears:['X','#cfd8d6'],can:['U','#8fc2c9'],chisel:['>','#dfe8ea'],cloth:['~','#bad6ca'],rake:['E','#c9a46a'],broom:['W','#c9a46a'],bucket:['U','#e6a35a'],spade:['D','#c7c2a8'],
   flagstick:['P','#e86f6f'],mallet:['T','#b9875a'],wrench:['Y','#c7d3d6'],jug:['8','#efe6c4'],stick:['/','#9c6f4a'],brush:['m','#d6b97c'],wing:['>','#f2e3b5']}[pose.tool]||['.','#e9dfb9'];
  put(tip.x,tip.y,head[0],head[1]);
 }
 return {character,pose,ground,cw,hand,tip,target,points};
}
export function drawWonderTools(ctx,staged){
 ctx.save();ctx.font='600 '+staged.cw*1.5+'px Menlo, monospace';ctx.textAlign='center';ctx.textBaseline='middle';ctx.strokeStyle='#172b24';ctx.lineWidth=Math.max(.6,staged.cw*.15);
 for(const p of staged.points){ctx.fillStyle=p.color;ctx.strokeText(p.glyph,p.x,p.y);ctx.fillText(p.glyph,p.x,p.y);}ctx.restore();
}
