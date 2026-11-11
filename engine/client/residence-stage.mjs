// Presentation of a simulation-owned arrival. Never chooses or advances a plan.
import {inkBounds,residentEnvelope} from './resident-envelope.mjs';
const clamp=n=>Math.max(0,Math.min(1,n));
export function residenceStage(plan, objects, character){
 if(!plan?.residence||plan.paused||!['prepare','act','settle'].includes(plan.phase))return null;
 const dest=plan.residence.destination;
 const home=objects.find(o=>o.id===plan.target&&o.worldPosition?.every((n,i)=>Math.abs(n-dest[i])<1.1));
 if(!home?.anchors||!character)return null;
 const progress=plan.progress??plan.elapsed/plan.duration;
 const inside=plan.phase==='act'?1:plan.phase==='prepare'?clamp((progress-.15)/.13):clamp((1-progress)/.1);
 return {home,character,inside};
}
export function occupiedGeometry(home,character,inside,sx,sy,slot=0){
 const unit=sx*home.scale*(home.detailScale||1),ch=unit*1.5;
 // ItemPainter has a one-cell padding around the same native glyph grid.
 const left=home.x*sx-home.width*unit/2,top=home.y*sy-home.art.length*ch;
 const seat=home.anchors.slots?.[slot]||home.anchors.seat,opening=home.anchors.opening;
 const {left:minX,right:maxX,top:minY,bottom:maxY}=home.anchors.slots?residentEnvelope(character):inkBounds(character);
 let scale=character.scale;
 if(home.anchors.slotWidth)scale=Math.min(scale,home.anchors.slotWidth*unit/((maxX-minX+1)*sx));
 if(opening){
  // Fit around the real foot/anchor, not merely the ink rectangle's height.
  // Tall necks and asymmetric bills otherwise cross the ceiling or jamb.
  const ax=character.anchorX??character.width/2,gy=character.groundRow??character.art.length;
  const dx=home.anchors.slots?0:character.offsetX||0,dy=home.anchors.slots?0:(character.offsetY||0)/1.5;
  const limits=[
   [seat.x-opening.x-1,ax-minX-dx,unit/sx],
   [opening.x+opening.w-1-seat.x,maxX+1-ax+dx,unit/sx],
   [seat.y-opening.y-1,gy-minY-dy,ch/(sx*1.5)],
   [opening.y+opening.h-seat.y,maxY+1-gy+dy,ch/(sx*1.5)],
  ];
  for(const [space,extent,factor]of limits)if(extent>0)scale=Math.min(scale,Math.max(.01,space)*factor/extent);
 }
 const restingX=left+seat.x*unit,restingY=top+seat.y*ch;
 const x=(character.x*sx*(1-inside)+restingX*inside)/sx;
 const y=(character.y*sy*(1-inside)+restingY*inside)/sy;
 const clip=opening&&inside>=.99?{x:left+(opening.x+1)*unit,y:top+(opening.y+1)*ch,w:(opening.w-2)*unit,h:(opening.h-1)*ch}:null;
 const rim=home.anchors.rim;
 const foreground=home.foreground;
 const front=rim===undefined?null:{...home,id:home.id+':front',occupant:null,
  art:home.art.map((r,y)=>[...r].map((c,x)=>foreground?.art[y][x]!==' '&&foreground?.art[y][x]!==undefined?foreground.art[y][x]:y>=rim?c:' ').join('')),
  tones:home.tones.map((r,y)=>[...r].map((c,x)=>foreground?.art[y][x]!==' '&&foreground?.art[y][x]!==undefined?foreground.tones[y][x]:c).join('')),
  fills:home.fills.filter(f=>f.y>=rim)};
 return {character:{...character,x,y,scale:character.scale+(scale-character.scale)*inside},clip,front};
}

export function heldNestGeometry(home,character,sx,sy){
 const held=home.held,bill=character.bill;if(!held?.contact||!bill)return null;
 const bodyUnit=sx*character.scale,bodyCh=bodyUnit*1.5;
 const left=Math.round(character.x*sx-character.anchorX*bodyUnit+(character.offsetX||0)*bodyUnit);
 const top=Math.round(character.y*sy-character.groundRow*bodyCh+(character.offsetY||0)*bodyUnit);
 const grip=held.grip,unit=sx*home.scale*(home.detailScale||1),ch=unit*1.5;
 const originX=home.x*sx-home.width*unit/2+(held.contact.x+.5)*unit;
 const originY=home.y*sy-home.art.length*ch+(held.contact.y+.5)*ch;
 const contactX=originX*(1-grip)+(left+(bill.x+.5)*bodyUnit)*grip;
 const contactY=originY*(1-grip)+(top+(bill.y+.5)*bodyCh)*grip;
 const size=1-(character.rig?.small?.3:0)*grip,heldUnit=unit*size;
 const model={...home,...held,id:home.id+':held',occupant:null,held:null,foreground:null,fills:[]};
 return {model,x:contactX+(model.width/2-held.contact.x-.5)*heldUnit,
  y:contactY+(model.art.length-held.contact.y-.5)*heldUnit*1.5,cw:sx*home.scale*size,
  contact:{x:contactX,y:contactY},bill:{x:left+(bill.x+.5)*bodyUnit,y:top+(bill.y+.5)*bodyCh}};
}
