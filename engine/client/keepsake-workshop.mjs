import {ObjectCanvas} from './object-canvas.mjs';
import BLUEPRINTS from './animation/keepsakes.json' with {type:'json'};
export {BLUEPRINTS as KEEPSAKE_BLUEPRINTS};
const clamp=n=>Math.max(0,Math.min(1,n));
function wood(c,x,y,w,h,vertical=false,tone='b'){
 c.clear(x,y,w,h);c.rect(x,y,w,h,tone,true);
 if(vertical)for(let xx=x+4;xx<x+w-3;xx+=7){c.line(xx,y+1,xx,y+h-2,'|','s');c.put(xx-2,y+5+(xx%9),'(=)','a');}
 else for(let yy=y+3;yy<y+h-2;yy+=4){c.line(x+2,yy,x+w-3,yy,'~','s');for(let xx=x+7;xx<x+w-5;xx+=23)c.put(xx,yy,'(~)','a');}
 c.line(x+1,y+1,x+w-2,y+1,'_','f');
}
function rivet(c,x,y){c.put(x-1,y,'(o)','a');}
function edge(c,x,y,w,h){
 c.rect(x,y,w,h,'a');c.rect(x+2,y+2,w-4,h-4,'f');
 for(const [xx,yy] of [[x+3,y+3],[x+w-4,y+3],[x+3,y+h-4],[x+w-4,y+h-4]])rivet(c,xx,yy);
}
function feet(c,p){for(const x of [18,p.w-24]){wood(c,x,p.h-12,7,8,true);c.put(x-1,p.h-4,'[_______]','k');}}
function paper(c,x,y,w,h,tone='p'){
 c.clear(x,y,w,h);c.rect(x,y,w,h,tone,true);c.line(x+2,y+1,x+w-3,y+1,'_','f');
 for(let yy=y+5;yy<y+h-2;yy+=7)for(let xx=x+3;xx<x+w-3;xx+=11)c.put(xx+(yy%3),yy,'.','d');
}
function duck(c,x,y,small=false){
 const art=small?[' .--.','(o  )=',' /  \\','(_/__)','  vv']:['       .--.','    .-(o  )==','   /  .---\'',' _/  /','/ .--.\\','|/ :  |',' \\___/','  _|_|_'];
 c.rows(art,x,y,'g');c.put(x+(small?5:11),y+1,small?'=':'==','a');
}
function chest(c,p,v){
 const W=p.w,H=p.h,x=12,w=W-24,front=H-36,open=clamp(v.open),lift=Math.round(open*31);
 feet(c,p);wood(c,x,front,w,25);
 if(p.style==='joinery')for(let yy=front+2;yy<front+23;yy+=4)for(const xx of [x,x+w-4])c.put(xx,yy,'[=]','a');
 else for(const xx of [x+11,x+w-15]){wood(c,xx,front,5,25,false,'k');for(let yy=front+3;yy<front+24;yy+=7)rivet(c,xx+2,yy);}
 c.ellipse(x+3,front+13,4,5,'_','k');c.ellipse(x+w-4,front+13,4,5,'_','k');
 if(open>.08){
  c.clear(x+3,front-13,w-6,14);c.rect(x+3,front-13,w-6,14,'k',true);
  if(p.style==='pirate'){
   for(let yy=front-10;yy<front-2;yy+=3)for(let xx=x+9;xx<x+w-9;xx+=7)c.put(xx+(yy%2)*2,yy,'(o)','a');
   c.rows([' /\\','<  >',' \\/'],x+w-23,front-13,'q');
  }else if(p.style==='joinery'){
   for(let i=0;i<3;i++){c.rect(x+6+i*(w-12)/3,front-12,(w-15)/3,11,'a');c.put(x+12+i*(w-12)/3,front-7,['TWIG','REED','ODDS'][i],'s');}
  }else{
   c.rows(['   _______','  /  *   /',' /______/'],W/2-7,front-12,'p');c.put(x+9,front-6,'[o]','g');c.put(x+w-18,front-6,'[o]','g');
  }
 }
 const lidTop=front-16-lift,lidH=16+Math.round(open*12);
 wood(c,x,lidTop,w,lidH);
 if(p.style==='pirate'){
  for(let xx=x;xx<x+w;xx++){const bow=Math.round(Math.sin((xx-x)/(w-1)*Math.PI)*5);c.put(xx,lidTop-bow,'_','a');if(bow)c.solid(xx,lidTop-bow+1,1,bow-1,'b');}
  for(const xx of [x+12,x+w-16]){c.rect(xx,lidTop-2,5,lidH+2,'k',true);for(let yy=lidTop;yy<lidTop+lidH;yy+=6)rivet(c,xx+2,yy);}
  c.rows([' .---.','( o o )',' | ^ |',' /===\\'],W/2-4,lidTop+3,'a');
 }else if(p.style==='weekly'){
  c.rect(W/2-3,lidTop,7,lidH,'q',true);c.line(x+2,lidTop+7,x+w-3,lidTop+7,'=','q');
  c.rows([' /\\ /\\','(  X  )',' \\/ \\/'],W/2-4,lidTop+2,'q');
  c.put(x+9,front+13,'1  2  3  4  5  6  7','f');c.put(x+11,front+18,'*  *  *  *  *  *  *','q');
 }else{edge(c,x+4,lidTop+2,w-8,lidH-4);c.put(W/2-9,lidTop+lidH/2,'DUCK  THINGS','f');}
 for(const xx of [x+7,x+w-11]){c.rect(xx,front-2,5,4,'k',true);rivet(c,xx+2,front-1);}
 const latch={x:W/2,y:front+6};c.rect(latch.x-4,latch.y-4,9,11,'a',true);c.put(latch.x-1,latch.y-2,open>.1?'U':'o','k');c.put(latch.x,latch.y+2,'|','k');
 return {contact:latch,lid:{x:W/2,y:lidTop+lidH-1},inside:{x:W/2,y:front-5},entry:{x:W/2,y:H-3}};
}
function basket(c,p,v){
 const x=p.w/2,y=p.h-24,rx=40,ry=13;
 for(const offset of [-2,0,2])for(let k=0;k<=60;k++){const a=Math.PI+k*Math.PI/60;c.put(x+Math.cos(a)*(rx-10)+offset,43+Math.sin(a)*28,'o',offset?'b':'a');}
 c.ellipse(x,49,rx,12,'_','k',true);
 for(let i=0;i<4;i++){c.line(x-29+i*20,46,x-24+i*18,54,'/','b');c.put(x-25+i*17,49,'~','p');}
 for(let yy=49;yy<y+9;yy++){
  const half=rx-(yy-49)*.13;c.solid(x-half,yy,half*2,1,'b');c.put(x-half,yy,'(','a');c.put(x+half,yy,')','s');
  if(yy%3===0)for(let xx=x-half+2;xx<x+half-2;xx+=5)c.put(xx,yy,((xx+yy)%2)?'/X/':'\\X\\','a');
  else for(let xx=x-half+4;xx<x+half-3;xx+=10)c.put(xx,yy,'|','s');
 }
 c.ellipse(x,y+8,35,5,'_','b');c.line(x-38,52,x+38,52,'=','f');
 for(const xx of [x-rx+2,x+rx-2])c.rows(['|||','(o)','|||'],xx-1,46,'a');
 c.rect(x-14,y-5,29,10,'p',true);c.put(x-11,y-1,'VERY ORGANIZED','d');c.put(x-8,y+2,'(mostly)','d');
 if(v.sort>.15){c.rows([' .----.',' | ~~ |'," '----'"],x-10+v.sort*8,42-v.sort*9,'p');c.put(x+15,44-v.sort*5,'/\\','g');}
 return {contact:{x:x-24,y:51},inside:{x,y:45},lid:{x,y:43},entry:{x,y:p.h-3}};
}
function barrel(c,p,v,state){
 const x=45,top=27,bottom=p.h-18,rx=30,water=clamp((state.keepsake?.litres??0)/60);
 for(const xx of [x-26,x+20])wood(c,xx,bottom,6,14,true);wood(c,x-32,bottom+9,64,5);
 for(let y=top;y<bottom;y++){
  const half=rx-4+Math.sin((y-top)/(bottom-top)*Math.PI)*5;c.solid(x-half,y,half*2+1,1,'b');c.put(x-half,y,'(','a');c.put(x+half,y,')','s');
  for(const dx of [-20,-10,0,10,20]){c.put(x+dx,y,'|','s');if(y%14===0)c.put(x+dx-2,y,'(~)','a');}
 }
 c.ellipse(x,bottom,27,5,'_','b',true);
 for(const y of [top+7,top+30,bottom-4]){c.clear(x-31,y,63,4);c.rect(x-31,y,63,4,'k',true);c.line(x-29,y+1,x+29,y+1,'=','s');for(const xx of [x-25,x,x+25])rivet(c,xx,y+1);}
 c.ellipse(x,top,29,8,'_','k',true);c.ellipse(x,top-1,25,5,'~',water>.05?'w':'k',true);
 const lidY=top-3-v.open*14;c.ellipse(x,lidY,28,5,'_','b',true);for(let dx=-20;dx<=20;dx+=8)c.line(x+dx,lidY-3,x+dx,lidY+3,'|','s');
 c.rows([' .---.',' |:::|'," '---'"],x-2,lidY-4,'a');
 c.rect(x-4,top+14,9,29,'g',true);const levelY=top+40-water*23;c.solid(x-2,levelY,5,top+42-levelY,'w');
 for(let y=top+17;y<top+42;y+=5)c.put(x-7,y,'--','f');c.put(x-2,top+45,String(Math.round(water*60)).padStart(2,'0')+'L','p');
 const tap={x:x+24,y:bottom-12};c.line(tap.x-3,tap.y,tap.x+13,tap.y,'=','a');c.line(tap.x+13,tap.y,tap.x+13,tap.y+5,'|','a');c.put(tap.x+3,tap.y-3,v.turn>.4?'|':'-+-','f');
 const bx=94,by=p.h-6;c.rect(bx-10,by-13,19,13,'g',true);c.line(bx-7,by-17,bx+5,by-17,'_','a');c.line(bx-9,by-15,bx-9,by-11,'|','a');c.line(bx+8,by-15,bx+8,by-11,'|','a');c.ellipse(bx-1,by,9,2,'_','a');
 if(v.pour>.1&&water>0)c.line(tap.x+13,tap.y+6,bx-2,by-5,':','w');
 if(state.keepsake?.frozen)for(let yy=top+17;yy<top+42;yy+=5)c.put(x-2,yy,'/X/','f');
 return {contact:{x:x-22,y:top+6},lid:{x,y:lidY},gauge:{x,y:top+29},tap,inside:{x,y:top},entry:{x:p.w/2,y:p.h-2}};
}
function frame(c,p,v){
 const x=12,y=12,w=p.w-24,h=p.h-30;
 c.beam(p.w*.57,y+h-8,p.w*.76,p.h-4,4,'b');c.line(p.w*.76,p.h-4,p.w*.36,p.h-4,'_','a');
 c.rect(x,y,w,h,'b',true);edge(c,x,y,w,h);c.rect(x+5,y+5,w-10,h-10,'g',true);
 for(let j=y+5;j<y+h-5;j+=4)for(const xx of [x+3,x+w-4])c.put(xx,j,p.style==='empty'?'<':':','a');
 const px=x+9,py=y+9,pw=w-18,ph=h-18;paper(c,px,py,pw,ph,'p');
 if(p.style==='friends'){
  c.rect(px+3,py+3,pw-6,ph-12,'g',true);for(let yy=py+ph*.55;yy<py+ph-10;yy+=3)c.line(px+5,yy,px+pw-6,yy,'~','w');
  duck(c,px+8,py+19);c.rows(['  ___',' / . \\','(  -  )',' /| |\\','/ | | \\','  | |',' _| |_'],px+pw-21,py+15,'q');
  c.put(px+5,py+ph-6,p.caption,'d');
 }else if(p.style==='sunset'){
  c.rect(px+2,py+2,pw-4,ph-10,'q',true);c.ellipse(px+pw*.65,py+ph*.32,9,7,'*','a',true);
  for(let yy=py+ph*.5;yy<py+ph-9;yy+=3){c.line(px+3,yy,px+pw-4,yy,'~','w');c.line(px+pw*.58,yy,px+pw*.72,yy,'-','a');}
  for(const xx of [px+5,px+11,px+pw-7]){c.line(xx,py+ph-12,xx-3,py+ph-27,'/','s');c.put(xx-4,py+ph-28,'(i)','b');}
  c.put(px+9,py+ph-5,p.caption,'d');
 }else{
  c.rect(px+4,py+4,pw-8,ph-8,'p');
  for(const [xx,yy,s] of [[px+4,py+4,1],[px+pw-9,py+4,-1],[px+4,py+ph-9,1],[px+pw-9,py+ph-9,-1]])c.rows(s>0?['|\\','|_\\']:['/|','/_|'],xx,yy,'d');
  c.put(px+pw/2-12,py+ph/2-2,p.caption[0],'d');c.put(px+pw/2-12,py+ph/2+2,p.caption[1],'d');
 }
 if(v.wipe>.1)c.line(px+3+v.wipe*(pw-12),py+5,px+9+v.wipe*(pw-12),py+ph-9,'/','f');
 return {contact:{x:20,y:p.h-23},glass:{x:p.w*.5,y:p.h*.45},corner:{x:16,y:16},inside:{x:p.w*.5,y:p.h*.5},entry:{x:p.w*.5,y:p.h-3}};
}
function loosePaper(c,p,v){
 const x=11,w=p.w-22,open=clamp(v.open),h=p.h-30,y=18;
 if(p.style==='card'){
  const half=w/2,cx=p.w/2-half*.5*(1-open);
  if(open>.05)paper(c,cx-half*open,y,half*open,h,'p');
  paper(c,cx,y,half,h,'p');c.line(cx,y,cx,y+h-1,':','d');
  if(open>.75){
   c.put(cx-half*open+6,y+13,p.reading.greeting[0],'d');c.put(cx-half*open+6,y+17,p.reading.greeting[1],'d');
   c.rows(p.reading.message,cx-half*open+6,y+28,'d');
   c.put(cx-half*open+6,y+h-14,'<3','q');
  }
  c.rows(['   .----.  .----.','  /      \\/      \\',' (                )','  \\              /','   \\            /','    \\          /','     \\        /','      \\      /','       \\    /','        \\  /','         \\/'],cx+half/2-9,y+14,'q');
  for(let yy=y+3;yy<y+h-2;yy+=5)c.put(cx+half-3,yy,':','q');
  c.put(cx+7,y+h-8,open>.75?p.reading.signature:p.reading.cover,'d');
  for(const yy of [y+5,y+h-5])for(let xx=cx+5;xx<cx+half-5;xx+=5)c.put(xx,yy,'x','q');
 }else{
  const fold=clamp(v.fold),foldedY=y+fold*h*.5,foldedH=h*(1-fold*.5);
  paper(c,x,foldedY,w,foldedH);
  if(fold>.7){c.line(x+3,foldedY+2,x+w-4,foldedY+2,'~','a');c.put(x+w/2-10,foldedY+foldedH*.4,'STORM / STUDY','d');c.put(x+w/2-8,foldedY+foldedH*.65,'KEEP DRY.','d');}
  else{
  c.put(x+5,y+4,p.caption,'d');
  c.rows([
   '               ___..------..___',
   '          _..-\' :   . :  .   : \`-.._',
   '      .--\' .  _..---.    .---.._  .  \`--.',
   '   .-\' :  .--\' . :  \`--\'  : .  \`-.  :  \`.',
   '  ( :  . (  . : .   :  . :   . :   )  .  : )',
   '   \`--.  \`--..___..--.  .--..___..-\' .  .-\'',
   '       \`-..__ : .   . \`\' : .  : __..--\'',
   '             \`---..___..---..--\''
  ],x+8,y+11,'d');
  c.rows(['     /','    /','   /','  /___','     /','    /','   /__','     /','    /','   /'],x+w-26,y+23,'d');
  for(let i=0;i<25;i++)c.put(x+8+(i*17%(w-18)),y+28+(i*7%15),'/','d');
  for(let yy=y+h-17;yy<y+h-7;yy+=3)c.line(x+6,yy,x+w-7,yy,'~','d');
  c.put(x+w-25,y+h-5,'C. / QUACK','d');
  if(fold>.1){const yy=y+h-fold*h*.5;paper(c,x+2,yy,w-4,fold*h*.5-1);c.line(x+2,yy,x+w-3,yy,'~','a');}
  }
 }
 c.put(x+2,p.h-10,'<__>','k');c.put(p.w-20,p.h-11,'<__>','k');
 return {contact:{x:p.w*.35,y:p.h-25},inside:{x:p.w*.5,y:p.h*.5},corner:{x:p.w-15,y:20},entry:{x:p.w/2,y:p.h-3}};
}
function map(c,p,v){
 const cx=p.w/2,half=12+clamp(v.open)*43,y=21,h=53;
 paper(c,cx-half,y,half*2,h);
 for(const sign of [-1,1]){const x=cx+sign*half;c.ellipse(x,y+h/2,5,h/2+3,'_','p',true);c.line(x-sign*2,y+2,x-sign*2,y+h-2,'|','d');c.ellipse(x,y-1,5,3,'_','a');c.put(x-1,y-1,'@','d');}
 if(half>34){
  c.put(cx-half+8,y+5,p.caption,'d');
  c.rows([
   '             __..----..___',
   '       _..--\'  :  :  :    \`---.._',
   '    .-\'  .---.    /\\     /\\    \\',
   '   /  .-\'     \`-. /  \\___/  \\   |',
   '  (  (  ~~ ~~   )  /\\    /\\   .-\'',
   '   \\  \`-.____.-\'  /  \\__/  \\  |',
   '    |  :  :  :    _..----.._  /',
   '    / /|\\ /|\\   /  ~~ ~~  \\ \\',
   '   /   |   |   (   ~  ~   ) |',
   '  ( /|\\ /|\\    \\___..___/  /',
   '   \\ |   |  :  :   :   : .-\'',
   '    \`-.   :   .--.   : .-\'',
   '       \`-..__ ( @@ ) _.-\'',
   '             \`--..--\''
  ],cx-half+7,y+12,'d');
  c.rows(['       N','       ^','     . | .','   .   |   .',' W<----+---->E','   \`   |   \'','     \` | \'','       v','       S'],cx+24,y+4,'d');
  for(let i=0;i<20;i++)c.put(cx-22+i*2.1,y+29+Math.sin(i*.5)*4,'.','d');c.put(cx+20,y+27,'X','q');
  c.rows(['    |\\','    | \\','   /|  \\','  /_|___\\','    | |',' ___|_|____',' \\ . . . /','~~\\_____/~~'],cx+17,y+34,'d');c.put(cx-36,y+h-7,p.question,'d');
 }
 return {contact:{x:cx-half,y:y+h-5},inside:{x:cx-5,y:y+30},route:{x:cx-22+clamp(v.turn)*40,y:y+29+Math.sin(clamp(v.turn)*9.5)*4},corner:{x:cx+half,y:y+2},entry:{x:cx,y:p.h-3}};
}
function book(c,p,v,state){
 const cx=p.w/2,H=p.h,open=clamp(v.open),spread=35+open*21,top=H-49,bottom=H-10,page=p.chapters[(state.keepsake?.page||0)%p.pages];
 c.rect(cx-spread-4,top+4,spread*2+9,bottom-top+4,'k',true);
 for(let yy=bottom-3;yy<=bottom+4;yy+=2)c.line(cx-spread,yy,cx+spread,yy,'_','d');
 if(open>.08){
  paper(c,cx-spread,top,spread,bottom-top);paper(c,cx,top,spread,bottom-top);c.line(cx,top,cx,bottom,'|','d');
  for(let i=0;i<4;i++){c.line(cx-spread+3,top+3+i,cx-3,top+i,'~','a');c.line(cx+3,top+i,cx+spread-3,top+3+i,'~','a');}
  if(open>.5){
   c.put(cx-spread+8,top+10,page[0],'d');c.put(cx-spread+7,top+17,page[1],'d');c.put(cx-spread+7,top+21,page[2],'d');
   for(let yy=top+29;yy<bottom-7;yy+=4){c.put(cx-spread+7,yy,'-: :--:  :--','d');c.put(cx+10,yy,':--: --: :--','d');}
   duck(c,cx+15,top+10);c.put(cx+spread-8,bottom-4,String((state.keepsake?.page||0)+1),'d');
  }
  if(v.turn>.01&&v.turn<.99){
   const xx=cx+Math.cos(v.turn*Math.PI)*(spread-4),arch=6*Math.sin(v.turn*Math.PI);
   for(let yy=top+4;yy<bottom-2;yy++){
    const edge=xx+Math.sin((yy-top)/(bottom-top)*Math.PI)*arch,lo=Math.min(cx,edge),hi=Math.max(cx,edge);
    if(hi-lo<1)continue;c.clear(lo,yy,hi-lo+1,1);c.solid(lo,yy,hi-lo+1,1,'p');c.put(edge,yy,'|','f');
    if(yy%5===0&&hi-lo>16)c.line(lo+5,yy,hi-6,yy,':','d');
   }
   c.line(cx,top+4,xx,top-arch,'_','f');c.line(xx,bottom-2,cx,bottom,'_','f');
  }
  c.line(cx+5,top+4,cx+8,bottom+8,'|','q');c.put(cx+6,bottom+9,'\/','q');
 }else{
  c.rect(cx-35,top-1,71,bottom-top+3,'l',true);edge(c,cx-33,top+1,67,bottom-top-1);
  for(let yy=top+7;yy<bottom-4;yy+=4)for(let xx=cx-29;xx<cx+31;xx+=5)c.put(xx,yy,yy%3?':':'.','s');
  c.rect(cx-19,top+13,39,25,'k',true);duck(c,cx-8,top+19);c.put(cx-25,top+9,'THE ELDER QUACKS','a');
  for(const yy of [top+7,top+19,top+35,bottom-6])c.put(cx-38,yy,'[===]','a');c.rect(cx+27,top+25,13,8,'a',true);c.put(cx+31,top+28,'(o)','k');
 }
 return {contact:{x:cx+spread-5,y:bottom-4},inside:{x:cx-18,y:bottom-4},corner:{x:cx+spread-3,y:bottom-3},lid:{x:cx+35,y:bottom-5},entry:{x:cx,y:H-2}};
}
const BUILDERS={chest,basket,barrel,frame,paper:loosePaper,map,book};
export function keepsakeSprite(base,item,time,{state={},pose={}}={}){
 const p=BLUEPRINTS[item.id];if(!p)return null;
 const saved=state.keepsake||{},v={open:saved.open??(p.style==='charcoal'?1:0),sort:0,turn:0,wipe:0,fold:p.style==='charcoal'?1-(saved.open??1):0,pour:0,...pose.keepsake};
 const c=new ObjectCanvas(p.w,p.h),anchors=BUILDERS[p.type](c,p,v,state);
 if(state.dirt>.35)for(const x of [p.w*.3,p.w*.5,p.w*.7])c.put(x,p.h-13,'.:','s');
 if(state.wetness>.45)for(const x of [p.w*.3,p.w*.5,p.w*.7])c.put(x,p.h-15,"'",'w');
 if(state.condition<.45)c.put(p.w*.4,p.h-12,'/','k');
 const inks={b:'#d9b88b',a:'#dec58e',f:'#e9ddbc',s:'#9aab9b',k:'#687f70',p:'#e1cba1',d:'#342a20',g:'#95c8c1',q:'#df999e',w:'#9bced9',l:'#adacb8'};
 if(['paper','map','book'].includes(p.type))inks.q='#7b3547';
 if(p.type==='book')inks.g='#285954';
 const panels={b:'#493d2e',a:'#665334',f:'#6e6650',s:'#2b3b32',k:'#142820',p:'#b6a77c',d:'#493c2d',g:'#2c4c4c',q:'#59464f',w:'#2e5965',l:'#353843'};
 return {...base,...c.finish(),construction:'keepsake-v1',detail:true,detailScale:.62,blueprint:item.id,anchors,inks,panels,sway:0,lift:0,animated:Boolean(pose.keepsake),emissive:false};
}
