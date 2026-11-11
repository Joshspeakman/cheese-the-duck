import ROUTINES from './animation/seating-routines.json' with {type:'json'};
export {ROUTINES as SEATING_ROUTINES};
const clamp=n=>Math.max(0,Math.min(1,n));
const N={x:0,y:0,b:0,w:0,l:0,r:0,press:0,sway:0,leaf:0,eye:null,mark:''};
export function seatingPose(routine,motion=true){
 const spec=ROUTINES[routine?.id];if(!spec||routine.interrupted)return null;
 const track=routine.role==='b'&&spec.reply?spec.reply:spec.track;
 const progress=motion?clamp(routine.elapsed/spec.duration):.5;
 let a=track[0],b=track.at(-1);
 for(let i=1;i<track.length;i++)if(progress<=track[i][0]){a=track[i-1];b=track[i];break;}
 let u=clamp((progress-a[0])/Math.max(.001,b[0]-a[0]));u=u*u*(3-2*u);
 a={...N,...a[1]};b={...N,...b[1]};const pose={...a};
 for(const k of ['x','y','b','w','l','r','press','sway','leaf'])pose[k]=a[k]+(b[k]-a[k])*u;
 if(u>.5){pose.eye=b.eye;pose.mark=b.mark;}
 return {...pose,progress,seated:true};
}
export function seatOccupants(scene){
 const p=scene.living?.plan,records=[...(scene.living?.minds?.seats||[])];
 if(p?.seating&&!p.paused&&['prepare','act','settle'].includes(p.phase)){
  const progress=p.progress??p.elapsed/p.duration;
  records.push({...p.seating,actor:'cheese',phase:p.phase==='act'?'inside':p.phase==='prepare'?'enter':'exit',
   elapsed:p.phase==='prepare'?clamp((progress-.15)/.13)*3:p.phase==='settle'?clamp((progress-.9)/.1)*3:0,
   routine:p.seat_routine});
 }
 return records;
}
export function seatingGeometry(home,passenger,sx,sy){
 const c=passenger.character,unit=sx*home.scale*home.detailScale,ch=unit*1.5;
 const left=home.x*sx-home.width*unit/2,top=home.y*sy-home.art.length*ch;
 const seat=home.anchors.slots[passenger.slot]||home.anchors.seat,inside=passenger.inside;
 // Fit the complete repertoire once, preserving scale throughout each rest.
 const bounds=passenger.envelope,fit=Math.min(c.scale,home.anchors.seatWidth*unit/((bounds.right-bounds.left+1)*sx));
 const scale=c.scale+(fit-c.scale)*inside;
 // Seated feet fold beneath the body. The rig exposes its belly contact so
 // cushions support the resident rather than leaving a gap under it.
 const ground=c.seatContact??c.groundRow;
 const restingY=top+seat.y*ch+(c.groundRow-ground)*fit*sx*1.5-(c.offsetY||0)*fit*sx;
 const restingX=left+seat.x*unit-(c.offsetX||0)*fit*sx;
 const character={...c,scale,x:c.x+(restingX/sx-c.x)*inside,y:c.y+(restingY/sy-c.y)*inside};
 const rim=home.anchors.front;
 const front=inside>.99?{...home,id:home.id+':seat-front',sitters:null,
  art:home.art.map((row,y)=>y>=rim?row:' '.repeat(home.width)),fills:home.fills.filter(f=>f.y>=rim)}:null;
 return {character,front};
}
