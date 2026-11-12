import {ObjectCanvas} from './object-canvas.mjs';
import BLUEPRINTS from './animation/seasonal-fittings.json' with {type:'json'};
export {BLUEPRINTS as SEASONAL_FITTINGS};
export function seasonalColors(p){return {b:p.color,a:p.trim,s:p.shade,k:'#537679'};}
export function fittedSeasonalPiece(rig,id,{phase=0}={}){
 const p=BLUEPRINTS[id];if(!p||!rig)return null;
 const front=new ObjectCanvas(76,48),back=new ObjectCanvas(76,48),contacts={};
 const t=rig.motion===false?0:phase,b=rig.body;
 if(p.shape==='mittens'){
  // Published by the character painter from the actual visible wing poses.
  // Never guess a work grip or move it to accommodate the garment.
  contacts.hands=(rig.handContacts||[]).map(h=>({...h}));
  for(const hand of contacts.hands){
   const x=Math.round(hand.x),y=Math.round(hand.y),sign=hand.direction===-1?-1:1;
   const cuff=x-sign*2;
   front.line(cuff,y-1,cuff,y+1,'=','a');
   front.put(x-sign,y-1,'.','b');front.put(x,y-1,'-','b');front.put(x+sign,y,sign===1?')':'(','b');
   front.put(x-sign,y+1,'~','s');front.put(x,y+1,"'",'b');
   front.put(x-sign,y,Math.sin(t)>.5?':':'x','a');
   // The contact center remains the visible front of the knitted palm.
   front.put(x,y,')','a');
  }
  // Raised hands may pass in front of the head. Preserve all face ink except
  // the already-painted hand center, and never cover a planted foot.
  const face=rig.faceBounds||rig.head;
  for(let y=0;y<48;y++)for(let x=0;x<76;x++)if(front.art[y][x]!==' '&&x>=face.x&&x<face.x+face.w&&y>=face.y&&y<face.y+face.h&&!contacts.hands.some(h=>h.x===x&&h.y===y))front.clear(x,y,1,1);
  for(const foot of rig.feet||[])front.clear(foot.x,foot.y,2,1);
 }else{
  const cx=Math.round(b.x+(b.w-1)/2),rx=Math.max(4,Math.ceil(b.w/2)+2);
  const feet=rig.feet||[],floor=feet.length?Math.min(...feet.map(f=>f.y)):39;
  const cy=Math.min(floor-3,Math.round(b.y+b.h-3));
  contacts.waist={x:cx,y:cy};
  // Back arc is occluded by the real torso; the front arc sits below its wings.
  back.solid(cx-Math.round(rx*.65),cy-2,Math.round(rx*.65)*2+1,1,'b');
  back.line(cx-Math.round(rx*.65),cy-2,cx+Math.round(rx*.65),cy-2,'~','a');
  back.put(cx-rx+1,cy-1,".'",'b');back.put(cx+rx-2,cy-1,"'.",'b');
  back.put(cx-rx,cy-1,'(','b');back.put(cx+rx,cy-1,')','b');
  // Sample the lower half of a shallow ellipse. Its rounded tips, sloping
  // shoulders and low central arc avoid a flat belt edge or boxed panels.
  for(let x=cx-rx;x<=cx+rx;x++){
   const u=(x-cx)/rx,depth=Math.round(3*Math.sqrt(Math.max(0,1-u*u))),y=cy-1+depth;
   const outer=(Math.abs(x-cx)+1)/rx,previous=Math.round(3*Math.sqrt(Math.max(0,1-outer*outer)));
   const edge=depth===0?(u<0?'(':')'):depth!==previous?(u<0?'\\':'/'):'_';
   front.solid(x,y,1,1,'b');front.put(x,y,edge,'b');
   if(depth>1){front.solid(x,y-1,1,1,'b');front.put(x,y-1,'.','s');}
  }
  // Only two curved cream seams cross the tube, with no repeating uprights.
  front.put(cx-Math.round(rx*.45),cy+1,'/','a');
  front.put(cx+Math.round(rx*.35),cy+1,'\\','a');
  const valveX=cx+Math.round(rx*.7),valveY=cy+Math.round(2*Math.sqrt(1-.7*.7))-1;
  front.put(valveX,valveY,'o','k');front.put(valveX+1,valveY,"'",'a');
  front.put(cx-Math.round(rx*.15),cy+1,Math.sin(t)>.4?"'":'.','a');
  // A low juvenile working wing can cross the tube. Keep its actual hand
  // in front of the ring, including its grip cell and immediate outline.
  const hands=rig.handContacts||[],overHand=(x,y)=>hands.some(h=>Math.abs(x-h.x)<=1&&Math.abs(y-h.y)<=1);
  for(const h of hands)front.clear(h.x-1,h.y-1,3,3);
  front.fills=front.fills.flatMap(f=>Array.from({length:f.w},(_,i)=>({...f,x:f.x+i,w:1}))).filter(f=>!overHand(f.x,f.y));
 }
 return {front:front.finish(),back:back.finish(),contacts,construction:'seasonal-fitting-v1'};
}
