import BLUEPRINTS from './animation/architecture.json' with {type:'json'};
import {ObjectCanvas} from './object-canvas.mjs';
export {BLUEPRINTS as ARCHITECTURE_BLUEPRINTS};
const clamp=n=>Math.max(0,Math.min(1,Number.isFinite(n)?n:0));
function timber(c,x,y,w,h){
 c.rect(x,y,w,h,'b',true);c.line(x+2,y+2,x+2,y+h-3,':','s');
 for(let row=6;row<h-3;row+=11){c.put(x+Math.max(2,w/2-2),y+row,'(o)','s');if(w>10)c.line(x+5,y+row+3,x+w-3,y+row+4,':','a');}
 for(const yy of [y+3,y+h-4])c.put(x+Math.max(2,w/2-1),yy,'o','f');
}
function stonewall(c,x,y,w,h){
 c.rect(x,y,w,h,'s',true);
 for(let row=0;row<h;row+=9){
  c.line(x,y+row,x+w-1,y+row,'_','k');
  for(let col=(row/9%2)*11;col<w;col+=22){const ww=Math.min(20,w-col-1);if(ww<3)continue;
   c.line(x+col,y+row+1,x+col,Math.min(y+h-1,y+row+8),'|','k');
   if(row+2<h)c.line(x+col+2,y+row+2,x+col+ww-1,y+row+2,'-','f');
   if(row+5<h)c.put(x+col+3,y+row+5,': .','a');
   if(row+7<h)c.put(x+col+ww-4,y+row+7,'/','k');
  }
 }
}
function shingleRoof(c,x,y,w,h){
 for(let row=0;row<h;row++){
  const left=x+w*.5*(1-row/h),right=x+w-left+x;
  c.solid(left,y+row,right-left+1,1,'r');c.put(left,y+row,'/','f');c.put(right,y+row,'\\','s');
  if(row%5===0)for(let xx=left+3;xx<right-3;xx+=9)c.put(xx,y+row,'[_]','a');
 }
 c.line(x-2,y+h,x+w+2,y+h,'=','b');c.line(x+w*.5,y-2,x+w*.5+7,y+1,'_','f');
}
function curl(c,x,y,rx=8,ry=8,tone='a'){
 let old=null;for(let i=0;i<=45;i++){const a=i*.14,r=1-i/55,p=[x+Math.cos(a)*rx*r,y+Math.sin(a)*ry*r];if(old)c.line(...old,...p,null,tone);old=p;}
}
function vine(c,x,y,h,season='spring'){
 const bare=season==='winter';let old=[x,y];
 for(let i=1;i<=h;i++){const p=[x+Math.sin(i*.13)*4,y-i];c.line(...old,...p,null,'l');
  if(i%9===0&&!bare){const sign=i%18?1:-1;c.rows(sign>0?[' /\\','<;;>',' \\/']:['/\\','<;;>','\\/'],p[0]+sign*3,p[1]-2,season==='fall'?'a':'l');}
  if(i%23===0&&['spring','summer'].includes(season)){c.rows([' .o.','(o@o)',' \'o\''],p[0]-2,p[1]-2,'q');}old=p;
 }
}
function masonryFoot(c,p){stonewall(c,10,p.h-11,p.w-20,7);}
function fence(c,p,iron=false){
 const H=p.h;
 if(!iron){
  for(const yy of [H-55,H-14]){c.rect(14,yy,p.w-28,6,'b',true);c.line(16,yy+2,p.w-16,yy+2,':','s');}
  for(let i=0;i<9;i++){
   const x=18+i*17,y=25+(i%2)*4;
   timber(c,x,y,10,H-y-8);c.rows(['    /\\','   /  \\','  /    \\',' /      \\','/________\\'],x,y-5,'f',true);
   for(const yy of [H-53,H-12])c.put(x+4,yy,'+','k');
  }
 }else{
  c.line(12,H-17,p.w-12,H-17,'=','b');c.line(12,32,p.w-12,32,'=','b');
  for(let x=18;x<p.w-14;x+=18){c.beam(x,23,x,H-9,3,'i');c.rows([' /\\','<||>',' \\/'],x-2,17,'a');curl(c,x+6,50,7,10);curl(c,x-5,H-30,6,8);c.put(x-1,H-18,'(+)','f');}
 }
 for(const x of [10,p.w-15]){timber(c,x,18,6,H-22);c.ellipse(x+3,16,5,3,'_','f',true);c.put(x-3,H-3,'[_______]','k');}
 return {contact:{x:46,y:H-14}};
}
function arch(c,p,s){
 const H=p.h,cx=p.w/2;
 for(const x of [24,p.w-25]){c.beam(x,42,x,H-9,5,'i');c.beam(x+8,46,x+8,H-9,3,'i');vine(c,x+3,H-13,H-55,s.season);stonewall(c,x-9,H-13,23,9);}
 for(const radius of [54,64]){
  let old=null;for(let i=0;i<=60;i++){const a=Math.PI+i*Math.PI/60,pnt=[cx+Math.cos(a)*radius,49+Math.sin(a)*34];if(old)c.line(...old,...pnt,null,'f');old=pnt;}
 }
 for(let i=0;i<7;i++){const a=Math.PI+i*Math.PI/6,x=cx+Math.cos(a)*59,y=49+Math.sin(a)*28;curl(c,x,y,6,5);}
 c.rows(['  .-.',' (o.o)','  \\_/'],cx-2,8,'a');
 return {contact:{x:35,y:H-24},entry:{x:cx,y:H-3}};
}
export function bridgeDeck(p,u){return {x:18+clamp(u)*(p.w-36),y:p.h-19-Math.sin(clamp(u)*Math.PI)*12};}
function bridge(c,p,front){
 const H=p.h;let previous=null;
 for(let i=0;i<=24;i++){
  const u=i/24,q=bridgeDeck(p,u),q2=bridgeDeck(p,Math.min(1,u+1/24));
  c.solid(q.x,q.y-15,Math.max(1,q2.x-q.x),16,'b');c.line(q.x,q.y-15,q.x,q.y,'|','b');c.line(q.x,q.y,q2.x,q2.y,'_','a');c.put(q.x+1,q.y-7,':','s');c.line(q.x+2,q.y-12,q.x+2,q.y-2,':','a');
  if(i%3===0){c.put(q.x,q.y-12,'o','f');c.put(q.x,q.y-2,'o','f');}
  if(previous){c.line(previous.x,previous.y-17,q.x,q.y-17,'=','f');c.line(previous.x,previous.y+4,q.x,q.y+4,'=','k');}
  previous=q;
 }
 for(let i=0;i<=6;i++){
  const q=bridgeDeck(p,i/6);c.beam(q.x,q.y-37,q.x,q.y-17,3,'b');front.beam(q.x,q.y-19,q.x,q.y+2,3,'b');
  if(i){const a=bridgeDeck(p,(i-1)/6);c.line(a.x,a.y-37,q.x,q.y-37,'=','a');front.line(a.x,a.y-19,q.x,q.y-19,'=','a');}
  c.put(q.x-1,q.y-30,'o','f');front.put(q.x-1,q.y-10,'o','f');
 }
 for(const u of [0,1]){const q=bridgeDeck(p,u);stonewall(c,q.x-9,H-15,18,12);}
 return {contact:{x:24,y:H-28},entry:bridgeDeck(p,0)};
}
function watchtower(c,p){
 const H=p.h,x=35,w=p.w-70;
 for(const xx of [x,x+w-6])timber(c,xx,52,6,H-57);
 c.beam(x+3,80,x+w-3,H-12,4,'b');c.beam(x+w-3,80,x+3,H-12,4,'b');
 c.rect(x-12,65,w+24,8,'a',true);c.line(x-10,68,x+w+10,68,'=','f');
 for(let xx=x-9;xx<x+w+10;xx+=10)c.beam(xx,43,xx,65,2,'b');c.line(x-12,43,x+w+12,43,'=','a');
 for(const xx of [x-10,x+w+10])c.beam(xx,29,xx,43,4,'b');
 shingleRoof(c,x-20,8,w+40,25);
 // Fixed ladder: the observation routines stay below it; they never fake a climb.
 for(const xx of [p.w/2-8,p.w/2+8])c.beam(xx,75,xx,H-8,2,'a');
 for(let y=79;y<H-7;y+=8)c.line(p.w/2-8,y,p.w/2+8,y,'=','f');
 for(const xx of [x-4,x+w-9])stonewall(c,xx,H-10,17,7);
 return {contact:{x:x+10,y:H-23}};
}
function gate(c,p,v){
 const H=p.h,left=30,span=(p.w-65)*(1-.91*clamp(v.open)),rise=clamp(v.open)*10;
 for(const x of [18,p.w-25]){stonewall(c,x,28,14,H-34);c.ellipse(x+7,25,10,5,'_','a',true);}
 c.line(left,45,left+span,45-rise,'=','a');c.line(left,H-19,left+span,H-19-rise,'=','a');
 for(let i=0;i<=7;i++){const x=left+span*i/7,y=rise*i/7;c.beam(x,40-y,x,H-20-y,2,'i');c.put(x-1,39-y,'^','f');if(span>35)curl(c,x+3,65-y,span/23,7);}
 for(const yy of [52,H-13]){c.rect(left-4,yy,8,5,'i',true);c.put(left-1,yy+2,'o','f');}
 const top={x:left+span-4,y:H-29-rise},latch={x:top.x,y:H-10};c.line(top.x,top.y,latch.x,latch.y,':','i');c.put(latch.x-3,latch.y,v.open>.1?'[ / ]':'[===]','f');
 return {contact:latch,latch,hinge:{x:left,y:H-11}};
}
function pergola(c,p,s,trellis=false){
 const H=p.h;
 if(trellis){
  for(const x of [26,p.w-31])timber(c,x,22,6,H-27);
  const left=33,right=p.w-34,top=25,bottom=H-12;
  for(let y=top;y<bottom;y+=14)c.line(left,y,right,Math.min(bottom,y+22),'/','a');
  for(let y=top+20;y<bottom;y+=14)c.line(left,y,right,Math.max(top,y-22),'\\','b');
  for(let x=left;x<right;x+=15)c.line(x,top,x,bottom,':','s');
  for(const x of [42,75,110])vine(c,x,H-12,H-33,s.season);
  c.put(30,H-16,'(x)','f');c.put(p.w-39,H-32,'(x)','f');
 }else{
  for(const x of [24,p.w-31]){timber(c,x,28,8,H-34);stonewall(c,x-5,H-13,19,10);}
  for(let y=23;y<44;y+=9){c.rect(14,y,p.w-28,5,'b',true);c.line(16,y+1,p.w-16,y+1,':','f');}
  for(let x=18;x<p.w-16;x+=15){c.beam(x,15,x+15,47,4,'a');c.put(x,15,'o','f');}
  c.beam(28,54,55,42,4,'b');c.beam(p.w-27,54,p.w-55,42,4,'b');
  vine(c,30,H-17,H-40,s.season);vine(c,p.w-28,H-17,H-41,s.season);
  for(let x=50;x<p.w-40;x+=21)c.rows([' o','/;\\',' ;'],x,45,'l');
 }
 return {contact:{x:35,y:H-26},leaf:{x:42,y:H-31},entry:{x:p.w*.5,y:H-3}};
}
function mailbox(c,p,v){
 const H=p.h,by=49;
 timber(c,55,by+27,10,H-by-32);c.beam(59,H-18,39,H-8,4,'b');c.beam(61,H-18,81,H-8,4,'b');
 c.rect(26,by,73,31,'i',true);c.ellipse(62,by-1,36,13,'_','i',true);c.rect(26,by,73,25,'i',true);
 c.line(31,by+4,94,by+4,'_','f');c.line(31,by+24,94,by+24,':','s');c.put(43,by+10,'QUAIL MAIL','a');
 c.rect(23,by+2,19,29,'k',true);c.line(26,by+5,39,by+5,'_','f');
 const doorY=by+30+v.panel*13;
 if(v.panel<.05){c.rect(23,by+2,19,29,'i',true);c.put(28,by+16,'[=]','f');}
 else{c.line(23,by+30,19,doorY,'/','f');c.line(41,by+30,43,doorY,'\\','f');c.line(19,doorY,43,doorY,'_','a');}
 // Duck-height pull loops operate the door and flag without stretching a wing.
 c.line(26,doorY,21,H-10,':','i');c.put(19,H-10,'(o)','f');
 const flag={x:96,y:by+19-v.flag*25};c.line(96,by+21,flag.x,flag.y,'|','a');c.rect(96,flag.y,14,7,'q',true);c.put(96,by+21,'o','f');
 c.line(96,by+21,104,H-10,':','i');c.put(102,H-10,'(o)','f');c.put(47,H-4,'[________________]','k');
 return {contact:{x:21,y:H-10},door:{x:21,y:H-10},flag:{x:104,y:H-10},entry:{x:32,y:H-3}};
}
function well(c,p,v){
 const H=p.h,cx=p.w/2;
 for(const x of [31,p.w-36])timber(c,x,36,7,H-44);
 shingleRoof(c,14,9,p.w-28,29);
 c.beam(34,H-69,p.w-32,H-69,5,'b');
 c.rect(cx-13,H-74,26,10,'a',true);for(let x=cx-11;x<cx+13;x+=3)c.line(x,H-73,x,H-65,'|','f');
 c.ellipse(cx,H-22,55,15,'_','k',true);
 const by=H-49+v.bucket*32;
 c.line(cx,H-64,cx,Math.min(by,H-17),':','a');
 if(by<H-20){c.ellipse(cx,by,11,4,'_','b',true);c.rect(cx-10,by,21,11,'b',true);for(let x=cx-8;x<cx+10;x+=4)c.line(x,by+2,x,by+9,'|','a');c.line(cx-11,by+3,cx+11,by+3,'=','i');c.line(cx-11,by+9,cx+11,by+9,'=','i');}
 c.clear(26,H-18,p.w-52,13);stonewall(c,26,H-18,p.w-52,13);c.ellipse(cx,H-21,58,6,'_','a');
 const angle=v.crank||0,hub={x:24,y:H-13},crank={x:hub.x+Math.cos(angle)*7,y:hub.y+Math.sin(angle)*4};c.line(34,H-69,hub.x,hub.y,':','i');c.line(hub.x,hub.y,crank.x,crank.y,null,'a');c.put(hub.x-1,hub.y,'o','i');c.put(crank.x-1,crank.y,'[o]','f');
 return {contact:crank,crank,entry:{x:22,y:H-3}};
}
function castle(c,p){
 const H=p.h,cx=p.w/2;stonewall(c,31,29,p.w-62,H-37);
 for(const x of [27,53,79,105])stonewall(c,x,15,20,22);
 c.line(28,36,p.w-28,36,'=','a');c.line(30,H-14,p.w-30,H-14,'=','a');
 for(const [x,y]of [[50,53],[101,67],[73,87]]){c.rect(x,y,5,16,'k',true);c.line(x-3,y+5,x+7,y+5,'-','k');c.put(x+1,y+2,'.','w');}
 c.clear(cx-15,H-51,30,35);c.rect(cx-15,H-45,30,38,'k',true);c.ellipse(cx,H-45,15,8,'_','k',true);
 for(let x=cx-11;x<cx+13;x+=6)c.line(x,H-47,x,H-9,'|','i');c.line(cx-14,H-28,cx+14,H-28,'=','i');
 for(const x of [21,p.w-39])stonewall(c,x,H-58,18,51);
 c.put(24,H-19,'MDCC / Q','a');masonryFoot(c,p);
 return {contact:{x:32,y:H-24}};
}
function windmill(c,p,v){
 const H=p.h,cx=p.w/2;stonewall(c,45,86,p.w-90,H-95);shingleRoof(c,34,63,p.w-68,24);
 c.rect(cx-14,H-43,28,35,'b',true);for(let x=cx-12;x<cx+14;x+=5)c.line(x,H-41,x,H-10,':','s');c.put(cx+6,H-25,'o','f');
 c.rect(56,100,19,19,'k',true);c.line(65,101,65,117,'|','a');c.line(57,109,73,109,'-','a');
 const cy=52,angle=v.phase||0;
 for(let n=0;n<4;n++){
  const a=angle+n*Math.PI/2,co=Math.cos(a),si=Math.sin(a),point=(r,w=0)=>[cx+co*r-si*w,cy+si*r+co*w];
  c.beam(cx,cy,...point(44),3,'b');
  for(let r=14;r<=42;r+=4)c.line(...point(r,-7),...point(r,7),null,r%8?'f':'a');
  c.line(...point(12,-7),...point(43,-7),null,'b');c.line(...point(12,7),...point(43,7),null,'b');
 }
 c.ellipse(cx,cy,6,5,'o','i',true);c.put(cx-1,cy,'(+)','f');
 const brake={x:25+v.brake*13,y:H-10};c.line(37,H-61,37,H-18,':','i');c.line(37,H-18,brake.x,brake.y,null,'a');c.put(brake.x-1,brake.y,'(o)','f');
 c.put(46,H-4,'[____________________________________]','k');
 return {contact:brake,brake};
}
const builders={picket:(c,p)=>fence(c,p),ironfence:(c,p)=>fence(c,p,true),wall:(c,p)=>{stonewall(c,14,30,p.w-28,p.h-37);c.rect(10,23,p.w-20,8,'a',true);for(let x=19;x<p.w-20;x+=23)c.put(x,p.h-16,';,,;','l');return {contact:{x:47,y:p.h-24},moss:{x:42,y:p.h-14}};},arch,bridge,watchtower,gate,pergola,trellis:(c,p,s)=>pergola(c,p,s,true),mailbox,well,castle,windmill};
export function architectureSprite(base,item,t,{state={},pose={},motion=true}={}){
 const p=BLUEPRINTS[item.id];if(!p)return null;
 const v={open:0,panel:0,flag:0,bucket:0,brake:0,phase:0,crank:0,season:'spring',...state.architecture,...pose.architecture};
 if(!motion)v.phase=0;
 const c=new ObjectCanvas(p.w,p.h),front=new ObjectCanvas(p.w,p.h);
 const anchors=builders[p.type](c,p,p.type==='bridge'?front:v)||{};
 const inks={b:'#bc9c6e',a:'#d2bd91',f:'#e8d9b1',s:'#899180',k:'#3a5148',i:'#89a69e',l:'#8fae6f',q:'#d79b9f',r:'#aa815e',w:'#91b7bd'};
 const panels={b:'#4b422f',a:'#655b43',f:'#a99c75',s:'#4e5b51',k:'#102820',i:'#304b46',l:'#35533c',q:'#804e56',r:'#493c31',w:'#365967'};
 if(p.type==='picket'){inks.b='#d5d7be';panels.b='#899480';}
 const cells=[];for(let y=0;y<p.h;y++)for(let x=0;x<p.w;x++)if(c.art[y][x]!==' ')cells.push([x,y]);
 if(state.wetness>.2)for(let n=0;n<Math.ceil(state.wetness*20);n++){const at=cells[n*47%cells.length];if(at)c.put(...at,"'",'w');}
 if(state.dirt>.25)for(let n=0;n<Math.ceil(state.dirt*25);n++){const at=cells[(n*71+19)%cells.length];if(at)c.put(...at,'.','k');}
 // In a catalogue the whole bridge is one drawing. During a crossing the near
 // rail is a separate foreground layer, so the feet stay on the deck behind it.
 if(p.type==='bridge'&&!pose.architecture){c.fills.push(...front.fills);front.art.forEach((row,y)=>row.forEach((glyph,x)=>{if(glyph!==' ')c.put(x,y,glyph,front.tones[y][x]);}));}
 const model={...base,...c.finish(),construction:'architecture-v1',blueprint:item.id,detail:true,detailScale:.62,anchors:{entry:{x:p.w*.35,y:p.h-3},...anchors},inks,panels,sway:0,lift:0,animated:Boolean(pose.architecture)||p.type==='windmill',floor:false,emissive:false};
 if(p.type==='bridge')model.front={...model,...front.finish(),front:null};
 return model;
}
