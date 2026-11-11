// Presentation of a simulation-owned arrival. Never chooses or advances a plan.
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
export function occupiedGeometry(home,character,inside,sx,sy){
 const unit=sx*home.scale*(home.detailScale||1),ch=unit*1.5;
 // ItemPainter has a one-cell padding around the same native glyph grid.
 const left=home.x*sx-home.width*unit/2,top=home.y*sy-home.art.length*ch;
 const seat=home.anchors.seat,opening=home.anchors.opening;
 const ink=character.art.flatMap((r,y)=>[...r].flatMap((c,x)=>c===' '?[]:[[x,y]]));
 const minX=Math.min(...ink.map(p=>p[0])),maxX=Math.max(...ink.map(p=>p[0]));
 const minY=Math.min(...ink.map(p=>p[1])),maxY=Math.max(...ink.map(p=>p[1]));
 let scale=character.scale;
 if(opening)scale=Math.min(scale,(opening.w-2)*unit/((maxX-minX+1)*sx),(opening.h-1)*ch/((maxY-minY+1)*sx*1.5));
 const restingX=left+seat.x*unit,restingY=top+seat.y*ch;
 const x=(character.x*sx*(1-inside)+restingX*inside)/sx;
 const y=(character.y*sy*(1-inside)+restingY*inside)/sy;
 const clip=opening&&inside>=.99?{x:left+(opening.x+1)*unit,y:top+(opening.y+1)*ch,w:(opening.w-2)*unit,h:(opening.h-1)*ch}:null;
 const rim=home.anchors.rim;
 const front=rim===undefined?null:{...home,id:home.id+':front',occupant:null,
  art:home.art.map((r,y)=>y>=rim?r:' '.repeat(r.length)),fills:home.fills.filter(f=>f.y>=rim)};
 return {character:{...character,x,y,scale:character.scale+(scale-character.scale)*inside},clip,front};
}
