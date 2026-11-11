import {ObjectCanvas} from './object-canvas.mjs';
import BLUEPRINTS from './animation/instruments.json' with {type:'json'};
export {BLUEPRINTS as INSTRUMENT_BLUEPRINTS};
const clamp=n=>Math.max(0,Math.min(1,n));
function wood(c,x,y,w,h,tone='b'){
 c.clear(x,y,w,h).rect(x,y,w,h,tone,true);
 for(let yy=y+3;yy<y+h-2;yy+=4){c.line(x+2,yy,x+w-3,yy,'~','s');for(let xx=x+6;xx<x+w-6;xx+=19)c.put(xx,yy,'(=)','s');}
 for(let yy=y+2;yy<y+h-2;yy+=2)for(let xx=x+4+(yy%4)*2;xx<x+w-3;xx+=11)c.put(xx,yy,yy%4?'::':"'-",'b');
 c.line(x+1,y+1,x+w-2,y+1,'_','f');
}
function tube(c,x,y,tx,ty,w=3,tone='a'){
 c.beam(x,y,tx,ty,w,tone);c.line(x,y,tx,ty,null,'f');
}
function disk(c,x,y,rx,ry,tone='k',fill=true){
 for(let yy=Math.ceil(y-ry);yy<=y+ry;yy++){const half=rx*Math.sqrt(Math.max(0,1-((yy-y)/ry)**2));c.clear(x-half,yy,half*2+1,1);}
 c.ellipse(x,y,rx,ry,'_',tone,fill);
}
function bolts(c,x,y,w,h){for(const [xx,yy] of [[x+2,y+2],[x+w-3,y+2],[x+2,y+h-3],[x+w-3,y+h-3]])c.put(xx,yy,'o','k');}
function leg(c,x,y,length){tube(c,x,y,x-2,y+length,4,'b');c.put(x-5,y+length,'[_____]','k');}
function ring(poses,key){return poses.reduce((v,p)=>v+(p.ringing||[]).filter(h=>h.key===key).reduce((n,h)=>n+h.amount,0),0);}
function active(poses,key){return Math.max(0,...poses.map(p=>p.hits?.filter(h=>h.key===key).reduce((n,h)=>Math.max(n,h.press),0)||0));}
function piano(c,p,poses){
 const toy=p.style==='toy',W=p.w,H=p.h,cx=W/2,keyboard=H-29,count=toy?10:18,start=12,span=W-24,kw=span/count;
 leg(c,17,H-24,19);leg(c,W-17,H-24,19);
 wood(c,8,17,W-16,keyboard-12);wood(c,5,keyboard-5,W-10,5);
 if(toy){
  for(let x=13;x<W-12;x++){const y=16-Math.sin((x-13)/(W-26)*Math.PI)*8;c.solid(x,y,1,17-y,'p');c.put(x,y,'~','f');}
  c.rows(['  .--.',' (o  )>',' /|__|\\','  ^  ^'],cx-5,20,'a');
  for(const sign of [-1,1])c.put(cx+sign*27,25,'*','p');
 }else{
  wood(c,5,10,W-10,7);c.rect(15,23,W-30,30,'k',true);
  // Visible soundboard, individually bridged strings, hammer pivots and felt.
  for(let i=0;i<28;i++){
   const x=19+i*(W-38)/28;c.put(x,26,'o','a');c.line(x,27,x-2,48-i%4,'|',i%3?'a':'f');c.put(x-2,49-i%4,'v','p');
  }
  c.line(18,45,W-20,39,'/','b');c.line(18,48,W-20,42,'/','b');
  c.rect(cx-20,54,40,10,'b',true);c.rows([' .------------.','| : : | : : : |','| . . | . . . |',"'-----+-------'"],cx-8,55,'c');
  c.put(13,20,'o','a');c.put(W-15,20,'o','a');
 }
 const keys=[];
 for(let i=0;i<count;i++){
  const x=start+i*kw,press=active(poses,i),dy=Math.round(press*2);
  c.rect(x,keyboard+dy,Math.ceil(kw),9-dy,'c',true);c.line(x+1,keyboard+dy+1,x+kw-2,keyboard+dy+1,'_','f');
  if(![2,6].includes(i%7)){c.rect(x+kw-2,keyboard,3,5,'k',true);c.line(x+kw-1,keyboard+1,x+kw-1,keyboard+3,'|','s');}
  keys.push({x:x+kw*.45,y:keyboard+7+dy});
 }
 wood(c,8,keyboard+10,W-16,7);
 if(toy)for(const [i,n] of ['C','D','E','F','G','A','B','C','D','E'].entries())c.put(start+i*kw+2,keyboard+13,n,'p');
 else{
  for(const dx of [-11,0,11]){tube(c,cx+dx,H-15,cx+dx-3,H-5,3,'a');c.put(cx+dx-5,H-4,'[___]','f');}
  c.put(cx-11,keyboard+13,'P O N D  &  S O N S','a');
 }
 return {keys,contact:keys[Math.floor(count/2)],entry:{x:cx,y:H-3},keyboard,slots:[{x:cx-span*.2,y:H-3},{x:cx+span*.2,y:H-3}],front:keyboard+10};
}
function drum(c,x,y,rx,depth,press=0,tone='p'){
 c.rect(x-rx,y,rx*2,depth,tone,true);c.line(x-rx+1,y+depth-3,x+rx-2,y+depth-3,'=','a');
 for(let dx=-rx+4;dx<rx-3;dx+=7){tube(c,x+dx,y+3,x+dx,y+depth-4,2,'k');c.put(x+dx-1,y+depth-4,'[o]','a');}
 disk(c,x,y+depth-1,rx,3,'b');disk(c,x,y,rx,Math.max(2,5-press),'c');
 c.ellipse(x,y,rx-3,3,'-','f');
 for(let dx=-rx+5;dx<rx-4;dx+=4)c.put(x+dx,y,':','s');
 c.ellipse(x,y,rx*.45,1,'~','s');
 if(press>.1)c.ellipse(x,y,rx*.65,2,'~','a');
}
function stand(c,x,y,h){tube(c,x,y,x,y+h,2,'a');for(const side of [-1,1]){c.line(x,y+h-6,x+side*9,y+h,'/','k');c.put(x+side*9-1,y+h,'[_]','k');}}
function drums(c,p,poses){
 const W=p.w,H=p.h,cx=W/2;
 stand(c,23,26,65);stand(c,W-23,35,56);
 const sway=ring(poses,3);
 for(const [x,y,r]of [[23,26,19],[W-23,35,18]]){
  disk(c,x,y+sway*2,r,4,'a');c.ellipse(x,y+sway*2,r-4,2,'~','f');c.put(x-3,y-2+sway*2,'(o)','b');c.put(x,y-5,'|','k');
 }
 // Bass shell and transparent-looking rim are separate from the kick pedal.
 c.rect(cx-26,55,52,31,'p',true);disk(c,cx,68,28,21,'k');disk(c,cx,68,25,19,'c');
 c.ellipse(cx,68,22,16,':','s');c.ellipse(cx,68,18,13,':','s');
 for(let yy=54;yy<84;yy+=3)for(let xx=cx-19;xx<cx+20;xx+=4)if(((xx-cx)/22)**2+((yy-68)/16)**2<1)c.put(xx,yy,'.','s');
 for(let a=0;a<Math.PI*2;a+=Math.PI/6)c.put(cx+Math.cos(a)*26,68+Math.sin(a)*20,'o','a');
 c.rows(['   __',' >(o )___','  ( ._> /',"   '---'"],cx-8,63,'b');c.put(cx-12,78,'P O N D B E A T','s');
 for(const side of [-1,1]){tube(c,cx+side*25,79,cx+side*31,92,3,'a');c.put(cx+side*31-2,93,'[__]','k');}
 stand(c,37,58,34);stand(c,103,55,36);tube(c,cx,53,cx,35,3,'a');
 drum(c,52,40,17,15,active(poses,0));drum(c,87,38,17,15,active(poses,1),'q');
 drum(c,36,65,18,14,active(poses,2),'b');drum(c,109,63,18,23,active(poses,4),'q');
 c.rows(['  /|',' / |','[==]','|::|','[__]'],cx-3,88,'a');
 return {keys:[{x:52,y:40},{x:87,y:38},{x:36,y:65},{x:W-23,y:35+sway*2},{x:109,y:63},{x:cx,y:70}],contact:{x:cx,y:52},entry:{x:cx,y:H-3},slots:[{x:cx-24,y:H-3},{x:cx+24,y:H-3}]};
}
function horn(c,p,poses){
 const W=p.w,H=p.h,press=poses[0]?.hits||[];
 wood(c,12,H-13,W-24,7,'k');c.put(20,H-7,'[__]','b');c.put(W-25,H-7,'[__]','b');
 // Folded tubing joins the mouthpiece, valve block, tuning slide and flare.
 tube(c,11,25,62,25,4);tube(c,62,25,62,44,4);tube(c,62,44,25,44,4);tube(c,25,44,25,34,4);tube(c,25,34,66,34,4);
 for(let i=0;i<3;i++){
  const x=25+i*4,dy=Math.round((press.find(h=>h.key===i)?.press||0)*3);
  tube(c,x,25,x,39,3,'b');c.put(x-1,28,'[=]','f');c.put(x-1,35,'[=]','f');tube(c,x,24,x,17+dy,1,'a');c.put(x-1,16+dy,'[=]','p');
 }
 c.rows([' _','( )',' |'],25,12,'a');tube(c,27,15,30,15,3);tube(c,30,15,30,25,3);c.put(18,41,'(o)','f');
 for(let x=66;x<88;x++){
  const r=3+((x-66)/22)**2*15;c.solid(x,32-r,1,r*2+1,'a');c.put(x,32-r,'/','f');c.put(x,32+r,'\\','b');
 }
 disk(c,89,32,8,18,'b');disk(c,89,32,5,14,'k');c.ellipse(89,32,7,17,'~','f');
 if(poses.some(p=>p.hits.length)){c.put(99,27,"'",'f');c.put(100,32,'>','a');c.put(99,37,'.','f');}
 c.put(28,47,'(O)','p');
 return {keys:[0,1,2].map(i=>({x:25+i*4,y:16+Math.round((press.find(h=>h.key===i)?.press||0)*3)})),mouth:{x:26,y:13},bell:{x:91,y:32},contact:{x:38,y:19},entry:{x:W/2,y:H-3},slots:[{x:10,y:H-3}]};
}
function speaker(c,x,y,r){
 disk(c,x,y,r,r*.68,'k');disk(c,x,y,r-3,r*.68-2,'b');
 for(let yy=-Math.floor(r*.5);yy<=r*.5;yy+=2)for(let xx=-r+4;xx<r-3;xx+=3)if((xx/(r-3))**2+(yy/(r*.6))**2<1)c.put(x+xx,y+yy,(xx+yy)%2?':':'.','s');
 disk(c,x,y,Math.max(3,r*.25),Math.max(2,r*.17),'k');c.put(x-1,y,'o','f');
}
function radio(c,p,t,poses,env){
 const W=p.w,H=p.h,cx=W/2,wooden=p.style==='wood',playing=poses.some(p=>p.playing),turn=poses.find(p=>p.slot===1)?.dial||0;
 if(playing)t=poses[0].time;
 const top=wooden?16:22,bottom=H-8;
 if(wooden){
  wood(c,10,top,W-20,bottom-top);for(let x=10;x<W-10;x++){const y=top-Math.sin((x-10)/(W-20)*Math.PI)*10;c.solid(x,y,1,top-y,'b');c.put(x,y,'~','f');}
  c.rect(18,25,W-36,26,'k',true);for(let yy=27;yy<49;yy+=3)for(let xx=20;xx<W-20;xx+=3)c.put(xx,yy,(xx+yy)%2?'x':'+','s');
  c.rect(21,55,W-42,9,'c',true);for(let x=24;x<W-24;x+=6)c.put(x,57,'|','b');
  c.put(26+turn*(W-55),58,'^','p');c.put(27,61,'P O N D  F M','b');
 }else{
  c.rect(22,7,W-44,13,'k');c.solid(23,8,W-46,4,'s');c.solid(23,12,5,10,'k');c.solid(W-28,12,5,10,'k');c.line(28,11,W-29,11,'_','f');
  c.rect(7,top,W-14,bottom-top,'s',true);bolts(c,7,top,W-14,bottom-top);
  speaker(c,28,44,17);speaker(c,W-28,44,17);
  c.rect(cx-19,31,38,23,'k',true);c.rect(cx-16,34,32,15,'p',true);
  for(const dx of [-9,9]){disk(c,cx+dx,41,5,4,'k');c.put(cx+dx-2,41,playing?(Math.floor(t*6)%2?'X':'=='):'(o)','f');}
  c.line(cx-8,42,cx+8,42,'-','s');c.put(cx-10,47,'SIDE A  001','c');
  for(let i=0;i<5;i++){c.rect(cx-18+i*8,55,6,4,i===2&&playing?'p':'a',true);c.put(cx-17+i*8,56,['>','|','<','>','o'][i],'k');}
  c.rect(cx-18,24,36,5,'k',true);c.put(cx-15,26,'[ . | . | . | . ]','a');
 }
 for(const [i,x] of [18,W-18].entries()){const knob=poses.find(p=>(p.slot||0)===i)?.dial||0;disk(c,x,bottom-7,5,4,'k');c.line(x,bottom-7,x+Math.sin(knob*5)*3,bottom-10,'/','f');}
 tube(c,W-14,top,W-28,3,2,'a');c.put(W-29,2,'o','f');
 for(const x of [15,W-23])c.rows(['[______]',' |____|'],x,H-7,'k');
 if(playing)c.put(cx-1,wooden?21:25,'*','p');
 return {keys:[{x:18,y:bottom-7},{x:W-18,y:bottom-7},{x:cx,y:wooden?59:56}],dial:{x:W-18,y:bottom-7},contact:{x:cx,y:wooden?59:56},entry:{x:cx,y:H-3},slots:[{x:cx-18,y:H-3},{x:cx+18,y:H-3}]};
}
function chimes(c,p,t,poses,env){
 const W=p.w,H=p.h,cx=W/2,wind=env.wind,keys=[];
 wood(c,8,H-10,W-16,7);wood(c,11,8,6,H-17);wood(c,W-17,8,6,H-17);wood(c,8,5,W-16,7);
 for(const x of [16,W-17]){c.line(x,14,x+(x<cx?12:-12),26,'/','f');c.put(x-1,11,'(o)','a');}
 if(p.style==='bell'){
  const swing=Math.sin(t*1.1)*wind*2+ring(poses,0)*3,x=cx+swing,y=28;
  tube(c,cx,11,x,y-5,3,'k');c.rows(['  .---.',' / . . \\','| (o) |'," '---'"],x-3,y-9,'a');
  for(let yy=0;yy<39;yy++){
   const half=8+yy*.12+Math.max(0,yy-21)**1.5*.2;c.solid(x-half,y+yy,half*2+1,1,'a');c.put(x-half,y+yy,'/','f');c.put(x+half,y+yy,'\\','b');
   if(yy%5===0)c.line(x-half+3,y+yy,x+half-3,y+yy,'~','b');
  }
  tube(c,x,y-6,x,y,5,'a');
  disk(c,x,y+39,25,5,'b');c.ellipse(x,y+38,25,4,'_','f');c.rows(['   |','  (O)'],x-2,y+34,'k');
  c.line(x,y+40,x+Math.sin(t)*wind*3,y+54,'|','c');c.put(x-3,y+54,'(O)','c');keys.push({x:x+17,y:y+25});
  c.put(x-8,y+17,'F O G','f');c.put(x-13,y+23,'-  P O N D  -','b');
 }else{
  const shells=p.style==='shells',count=shells?5:7;
  for(let i=0;i<count;i++){
   const xx=24+i*(W-48)/(count-1),length=(shells?[29,44,56,40,27]:[40,49,58,64,56,44,35])[i];
   const shake=Math.sin(t*1.6+i*.8)*wind*2+ring(poses,i)*2,tip={x:xx+shake,y:20+length};
   c.line(xx,13,tip.x,20,'|','c');
   if(shells){
    c.line(tip.x,20,tip.x,tip.y-8,'|','c');
    const r=8;for(let y=0;y<9;y++){const half=Math.sin(y/10*Math.PI*.85)*r;c.solid(tip.x-half,tip.y-8+y,half*2+1,1,i%2?'p':'c');c.put(tip.x-half,tip.y-8+y,'/','f');c.put(tip.x+half,tip.y-8+y,'\\','b');}
    for(let j=-2;j<=2;j++)c.line(tip.x,tip.y-8,tip.x+j*3,tip.y-1,null,'a');c.put(tip.x-7,tip.y,'vvvvvvv','f');
   }else{
    tube(c,xx+shake,20,tip.x,tip.y,5,i%2?'a':'p');c.put(xx+shake-3,20,'[===]','f');c.put(tip.x-3,tip.y,'[___]','k');c.line(tip.x-1,23,tip.x-1,tip.y-3,'|','f');
   }
   keys.push({x:tip.x,y:shells?tip.y-3:tip.y-7});
  }
  const dy=H-20;c.line(cx,12,cx+Math.sin(t)*wind*2,dy,'|','c');disk(c,cx+Math.sin(t)*wind*2,dy,7,4,'b');c.put(cx-3,dy,'<o>','f');
 }
 return {keys,contact:keys[Math.floor(keys.length/2)],entry:{x:cx,y:H-3},slots:[{x:cx-18,y:H-3},{x:cx+18,y:H-3}]};
}
export function instrumentSprite(base,item,time,{motion=true,state={},context={},pose={}}={}){
 const p=BLUEPRINTS[item.id];if(!p)return null;
 const poses=pose.music||[],t=motion?time:0,env={wind:motion?(context.living?.ecology?.wind??.15):0};
 const c=new ObjectCanvas(p.w,p.h),anchors=({piano,drums,horn,radio,chimes})[p.type](c,p,...(p.type==='radio'||p.type==='chimes'?[t,poses,env]:[poses]));
 if(state.dirt>.35){for(const x of [16,p.w/2,p.w-18])c.put(x,p.h-11,'.:','s');}
 if(state.condition<.5)c.put(p.w/2-9,p.h-9,'/','k');
 if(state.wetness>.5)for(const x of [15,p.w/2,p.w-18])c.put(x,p.h-8,"'",'w');
 const inks={b:'#caa37d',f:'#eedabd',s:'#80928a',k:'#41554d',a:'#e4c576',c:'#e9e2c9',p:'#b0cad0',q:'#c8a3bd',w:'#b3dddd'};
 const panels={b:'#483b2f',f:'#635443',s:'#31413b',k:'#142722',a:'#594b2b',c:'#6a6b59',p:'#364e53',q:'#4c3749',w:'#36514c'};
 return {...base,...c.finish(),construction:'instrument-v1',detail:true,detailScale:.62,blueprint:item.id,anchors,inks,panels,sway:0,lift:0,animated:motion,active:poses.length>0};
}
