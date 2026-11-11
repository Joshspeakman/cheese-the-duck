import {ObjectCanvas} from './object-canvas.mjs';
import BLUEPRINTS from './animation/furniture.json' with {type:'json'};
import {seatingPose} from './seating-routines.mjs';
export {BLUEPRINTS as FURNITURE_BLUEPRINTS};
const clamp=n=>Math.max(0,Math.min(1,n));
function timber(c,x,y,w,h,tone='b',vertical=false){
 c.clear(x,y,w,h);c.rect(x,y,w,h,tone,true);
 if(vertical){
  for(let xx=3;xx<w-2;xx+=5){c.line(x+xx,y+1,x+xx,y+h-2,'|','s');for(let yy=5;yy<h-3;yy+=10)c.put(x+xx-1,y+yy,'(=)','s');}
 }else{
  for(let yy=3;yy<h-1;yy+=4){c.line(x+2,y+yy,x+w-3,y+yy,'~','s');for(let xx=6;xx<w-5;xx+=19)c.put(x+xx,y+yy-1,'(=)','f');}
 }
 c.line(x+1,y+1,x+w-2,y+1,'_','f');
 for(const [xx,yy]of [[x+2,y+2],[x+w-3,y+2],[x+2,y+h-3],[x+w-3,y+h-3]])if(h>4)c.put(xx,yy,'o','k');
}
function leg(c,x,y,h,turned=false){
 c.solid(x-2,y,5,h,'b');c.line(x-2,y,x-2,y+h-1,'|','f');c.line(x+2,y,x+2,y+h-1,'|','s');
 if(turned)for(let yy=y+2;yy<y+h-2;yy+=5)c.put(x-3,yy,'(===)','b');
 c.put(x-3,y+h-1,'[___]','k');
}
function pad(c,x,y,w,h,kind='plain',press=0,tone='q'){
 const dy=Math.round(press*2);c.clear(x,y+dy,w,h-dy);c.rect(x,y+dy,w,h-dy,tone,true);
 c.line(x+2,y+dy+1,x+w-3,y+dy+1,':','f');c.line(x+2,y+h-2,x+w-3,y+h-2,':','f');
 for(let yy=y+dy+2;yy<y+h-2;yy++){
  if(kind==='tufted')for(let xx=x+3;xx<x+w-3;xx++){if((xx-x+yy-y)%10===0)c.put(xx,yy,'/','s');if((xx-x-yy+y+100)%10===0)c.put(xx,yy,'\\','s');if((xx-x)%10===5&&(yy-y)%5===0)c.put(xx,yy,'o','a');}
  if(kind==='patchwork'){if((yy-y)%5===0)c.line(x+2,yy,x+w-3,yy,'-','p');else for(let xx=x+6;xx<x+w-2;xx+=8){c.put(xx,yy,'|','p');if((yy-y)%5===2)c.put(xx-4,yy,'<>','a');}}
  if(kind==='ribbed'&&(yy-y)%3===0)c.line(x+2,yy,x+w-3,yy,'~','p');
 }
}
function scroll(c,x,y,sign=1,tone='k'){c.rows(sign>0?[' .---.','( .-\\ )',' \\_/|/','    |']:[' .---.','( /-. )',' \\|\\_/','  |'],x,y,tone);}
function book(c,x,y,w,h,i=0,open=false){
 if(open){c.rows([' .----------.----------.','/ : : : : : | : : : : : \\','| : : : : : | : : : : : |','| . . . . . | . . . . . |',"'-----------+-----------'"],x,y,'f',true);return;}
 const tone=['q','p','g','a'][i%4];c.rect(x,y,w,h,tone,true);c.line(x+1,y+2,x+w-2,y+2,'-','f');c.line(x+1,y+h-3,x+w-2,y+h-3,'-','f');
 if(w>=6){c.put(x+2,y+4,['I','II','V','X'][i%4],'a');if(h>12)c.put(x+2,y+7,':','f');}
}
function wheel(c,x,y){c.ellipse(x,y,5,3,'#','k',true);c.put(x-1,y,'(o)','f');c.line(x,y-6,x,y-3,'|','k');}
function cleanEllipse(c,cx,cy,rx,ry){
 for(let y=Math.ceil(cy-ry);y<=Math.floor(cy+ry);y++){const half=rx*Math.sqrt(Math.max(0,1-((y-cy)/ry)**2));c.clear(Math.round(cx-half),y,Math.round(half*2)+1,1);}
}
function drawer(c,x,y,w,h,open=0){
 const pull=Math.round(open*5);timber(c,x,y+pull,w,h,'b');if(pull){c.rect(x+1,y,w-2,pull,'d',true);c.put(x+4,y+1,': : :','s');}
 const cx=x+w/2;c.put(cx-3,y+pull+h/2,'[ o ]','k');c.line(cx-2,y+pull+h/2+1,cx+2,y+pull+h/2+1,'_','f');
}
function bottle(c,x,y,style=0){c.rows(['  __','  ||',' /  \\','|    |','|[==]|','|    |',"'----'"],x,y,style?'g':'p',true);c.put(x+2,y+4,style?'*':'o','a');}
function chair(c,p,t,pose){
 const W=p.w,H=p.h,cx=W/2,seatY=H-21,royal=p.style!=='ladder';
 leg(c,12,seatY,18,royal);leg(c,W-13,seatY,18,royal);leg(c,20,seatY-2,14);leg(c,W-21,seatY-2,14);
 c.line(13,H-11,W-14,H-11,'=','b');
 timber(c,12,royal?13:8,5,seatY-(royal?13:8),'b',true);timber(c,W-17,royal?13:8,5,seatY-(royal?13:8),'b',true);
 if(!royal){for(let y=10;y<seatY-3;y+=8)timber(c,14,y,W-28,5);timber(c,9,seatY,W-18,6);for(let x=15;x<W-13;x+=8)c.line(x,seatY+1,x,seatY+4,'|','s');}
 else{
  const top=p.style==='gold'?15:18;pad(c,18,top,W-36,seatY-top+4,'tufted',0,p.style==='gold'?'p':'q');
  for(let x=15;x<W-14;x++){const y=top-3-Math.sin((x-15)/(W-30)*Math.PI)*7;c.solid(x,y,1,top-y,'b');c.put(x,y,'~','a');}
  c.line(cx,8,cx,top-10,'|','a');
  for(const sign of [-1,1]){c.line(cx+sign*(W/2-13),top-7,cx+sign*(W/2-13),13,'|','b');c.put(cx+sign*(W/2-13)-2,top-9,'(o)','a');scroll(c,cx+sign*(W/2-12)-3,seatY-8,sign);c.line(cx+sign*(W/2-12),seatY-4,cx+sign*(W/2-12),seatY+2,'|','k');}
  c.rows(p.style==='gold'?[' /\\  /\\  /\\','/o \\/o \\/o \\','[==========]']:['   _o_',' /\\ | /\\','/  \\|/  \\','[=======]'],cx-6,4,'a',true);
  timber(c,10,seatY+3,W-20,6);pad(c,17,seatY-1,W-34,7,'plain',pose.press);
  if(p.style==='gold')for(let x=22;x<W-19;x+=11)c.put(x,seatY+7,'<o>','a');
 }
 return {seat:{x:cx,y:seatY+2},slots:[{x:cx,y:seatY+2}],seatWidth:W-32,entry:{x:cx,y:H-3},front:seatY+5,back:{x:cx,y:seatY-12},arm:{x:W-14,y:seatY-6}};
}
function sofa(c,p,t,pose){
 const W=p.w,H=p.h,cx=W/2,seatY=H-24,fancy=p.style==='velvet';
 for(const x of [16,W-17])leg(c,x,H-13,10,true);
 timber(c,12,seatY+10,W-24,6);pad(c,11,12,W-22,seatY-7,fancy?'tufted':'patchwork');
 if(fancy)for(let x=9;x<W-9;x++)c.put(x,11-Math.sin((x-9)/(W-18)*Math.PI)*6,'~','a');
 for(let i=0;i<2;i++)pad(c,19+i*(W-38)/2,seatY,(W-40)/2,11,fancy?'plain':'ribbed',pose.press*(i===pose.slot?1:.2));
 for(const side of [-1,1]){const x=side<0?8:W-20;c.rect(x,seatY-4,13,19,'q',true);c.ellipse(x+6,seatY-4,7,4,'~','p',true);scroll(c,x+1,seatY-3,side,'f');c.line(x+2,seatY+5,x+2,seatY+13,':','f');}
 pad(c,21,seatY-8,18,9,'patchwork',0,'p');pad(c,W-40,seatY-8,18,9,'tufted',0,'g');
 if(fancy)for(let x=22;x<W-20;x+=3)c.put(x,seatY+16,"'",'a');
 return {seat:{x:cx,y:seatY+5},slots:[{x:W*.32,y:seatY+5},{x:W*.68,y:seatY+5}],seatWidth:(W-42)/2,entry:{x:cx,y:H-3},front:seatY+11,back:{x:cx,y:20},arm:{x:W-14,y:seatY-4}};
}
function cushion(c,p,t,pose){
 const W=p.w,H=p.h,cx=W/2,cy=H-14,press=pose.press*3;
 if(p.style==='beanbag'){
  for(let y=8;y<H-5;y++){const u=(y-8)/(H-14),half=12+Math.sin(u*Math.PI*.83)*25;c.solid(cx-half,y,half*2+1,1,'q');c.put(cx-half,y,'(','f');c.put(cx+half,y,')','s');}
  c.ellipse(cx,cy+5,33,5,'_','q',true);
  for(const side of [-1,1])c.line(cx+side*8,9,cx+side*22,cy+6,':','f');
  c.line(cx-26,cy+3,cx+25,cy+3,'~','p');c.rows(['|||','[o]','|||'],W-23,cy-2,'k');
  c.ellipse(cx,cy-5+press,18,5,':','p',true);c.put(cx-8,cy-4+press,'~  .  ~','s');
 }else{c.ellipse(cx,cy,25,10,'~','p',true);pad(c,11,cy-7,46,14,'patchwork',pose.press);for(const x of [9,W-10])for(let y=cy-4;y<cy+6;y+=3)c.put(x,y,':','a');}
 return {seat:{x:cx,y:cy-2+press},slots:[{x:cx,y:cy-2+press}],seatWidth:44,entry:{x:cx,y:H-3},front:cy+5,back:{x:cx,y:cy-7},arm:{x:W-19,y:cy}};
}
function bench(c,p,t,pose){
 const W=p.w,H=p.h,seatY=H-23;
 for(const x of [16,W-17]){scroll(c,x-5,seatY-12,1);c.line(x,seatY-8,x,H-7,'|','k');c.line(x,H-7,x-6,H-3,'/','k');c.line(x,H-7,x+7,H-3,'\\','k');c.put(x-8,H-3,'[__]','k');c.put(x+5,H-3,'[__]','k');}
 for(const y of [12,20,28])timber(c,13,y,W-26,6);
 for(let j=0;j<3;j++)timber(c,10,seatY+j*3,W-20,3);
 for(const x of [11,W-12]){c.line(x,seatY-5,x,seatY+9,'|','k');c.put(x-4,seatY-6,'[=======]','k');}
 c.put(W/2-7,22,'[ POND ]','a');
 return {seat:{x:W/2,y:seatY+3},slots:[{x:W*.31,y:seatY+3},{x:W*.69,y:seatY+3}],seatWidth:36,entry:{x:W/2,y:H-3},front:seatY+7,back:{x:W/2,y:20},arm:{x:W-12,y:seatY-6}};
}
function hammock(c,p,t,pose){
 const W=p.w,H=p.h,cx=W/2,swing=pose.sway||0;
 for(const x of [12,W-13]){c.beam(x,10,x-5,H-5,4,'b');c.beam(x,10,x+7,H-5,4,'b');c.put(x-2,11,'(o)','k');c.line(x-6,H-6,x+8,H-6,'_','b');}
 c.beam(18,H-8,W-19,H-8,3,'b');
 const cy=H-24+pose.press*3;
 for(let n=0;n<=78;n++){
  const u=n/78,x=23+u*(W-46)+Math.sin(Math.PI*u)*swing,y=15+Math.sin(Math.PI*u)*(cy-15);
  c.solid(x,y,2,7,'q');c.put(x,y,'~','f');c.put(x,y+7,'~','f');
  for(let j=1;j<7;j++)c.put(x,y+j,(n+j)%3?'\\':'/','p');if(n%4===0)c.put(x,y+9,"'",'a');
 }
 c.line(12,12,24,17,'~','k');c.line(W-13,12,W-24,17,'~','k');
 pad(c,cx-22+swing,cy-3,17,6,'ribbed',0,'g');
 return {seat:{x:cx+swing,y:cy+2},slots:[{x:cx+swing,y:cy+2}],seatWidth:46,entry:{x:cx,y:H-3},front:cy+6,back:{x:cx-12+swing,y:cy-2},arm:{x:W-24,y:17}};
}
function table(c,p,t,pose){
 const W=p.w,H=p.h,cx=W/2,top=p.style==='cart'?18:12;
 if(p.style==='round'){
  for(const x of [cx-21,cx+21])leg(c,x,top+4,H-top-8,true);
  leg(c,cx,top+8,H-top-12,true);c.ellipse(cx,top+3,W/2-7,9,'_','b',true);c.ellipse(cx,top,W/2-7,9,'=','b',true);
  for(let y=-5;y<=5;y+=3)c.line(15,top+y,W-16,top+y,'~','s');c.put(cx-8,top,'(~)  .  (~)','f');c.ellipse(cx,top,9,4,':','q');
 }else if(p.style==='folding'){
  for(const offset of [0,9]){c.line(15+offset,top+3,W-16-offset,H-4,'\\','b');c.line(W-16-offset,top+3,15+offset,H-4,'/','b');c.put(cx,top+12,'o','k');}
  timber(c,7,top,W-14,7);c.line(12,top+3,W-13,top+3,':','f');
 }else{
  for(const x of [12,W-13])leg(c,x,top+4,H-top-(p.style==='cart'?12:8));
  timber(c,8,H-19,W-16,5);timber(c,7,top,W-14,7);
  if(p.style==='cart'){
   for(const x of [14,W-15])wheel(c,x,H-5);
   c.line(W-12,top+1,W-12,8,'|','k');c.line(W-12,8,W-4,8,'=','k');c.line(W-4,8,W-4,17,'|','k');
   for(const [x,y]of [[15,top-7],[30,top-7],[20,H-26],[37,H-26]])bottle(c,x,y,x%2);
   c.rows(['\\___/','  |',' _|_'],50,top-3,'f');c.put(51,H-17,'(==) (==)','k');
  }else{
   book(c,18,top-4,12,3,0,true);for(let i=0;i<3;i++)book(c,17+i*12,H-25,10,6,i);
   c.rows([' .---.','(  ~  )','|_____|',' \\___/'],W-27,top-5,'p',true);
  }
 }
 return {contact:{x:cx,y:top},entry:{x:cx,y:H-3},surface:top};
}
function shelf(c,p,t,pose,ctx){
 const W=p.w,H=p.h,trophies=p.style==='trophies';
 timber(c,8,8,W-16,H-13,'b',true);c.clear(15,15,W-30,H-26);c.solid(15,15,W-30,H-26,'d');c.line(12,12,W-13,12,'=','f');
 const levels=[H-16,H-35,H-54];
 const owned=Object.keys(ctx.living?.objects||{}).filter(id=>/trophy|medal|badge/.test(id));
 for(const [n,y]of levels.entries()){
  timber(c,12,y,W-24,4);if(y<12)continue;
  if(trophies){
   for(let i=0;i<3;i++){const x=22+i*26;c.put(x-3,y-2,'[____]','k');if(owned[n*3+i]){c.rows(['\\     /','(  *  )',' \\___/','   |',' __|__'],x-3,y-8,'a',true);c.put(x-1,y-1,'==','f');}}
  }else{
   let x=17,index=n*5;while(x<W-23){const width=6+(index%3)*2,height=10+(index%3)*2;book(c,x,y-height,width,height,index);x+=width+2;index++;}
   if(p.style==='staggered'&&n===1){c.clear(W-37,y-15,20,15);c.solid(W-37,y-15,20,15,'d');c.rows(['  _',' /o\\','/___\\','  |',' _|_'],W-33,y-5,'p',true);}
  }
 }
 if(p.style==='library'){c.line(W-29,19,W-15,H-5,'/','k');c.line(W-18,19,W-4,H-5,'/','k');for(let y=23;y<H-6;y+=7){const x=W-29+(y-19)/(H-24)*14;c.line(x,y,x+11,y,'=','k');}}
 if(trophies){c.rect(13,14,W-26,H-30,'k');c.line(W/2,14,W/2,H-17,'|','k');for(const x of [24,W-34])c.rows(['   /','  /',' /'],x,21,'w');c.put(W/2-5,H/2,'o | o','k');}
 return {contact:{x:W/2,y:levels[1]-6},entry:{x:W/2,y:H-3},shelves:levels,displayed:trophies?owned.slice(0,9):[]};
}
function desk(c,p,t,pose){
 const W=p.w,H=p.h,top=H-27,work=p.style==='workshop';
 for(const x of [12,W-13])leg(c,x,top+5,22);
 timber(c,7,top,W-14,6);timber(c,13,H-11,W-26,4);
 if(work){
  timber(c,13,7,W-26,top-10,'b',true);
  for(let y=12;y<top-6;y+=4)for(let x=18;x<W-17;x+=5)c.put(x,y,'o','s');
  c.rows([' __','|__|','  |','  |','  |'],22,12,'k');c.rows([' /\\',' ||',' ||',' ||','[__]'],42,12,'k');c.rows([' .----.','/ / / /','\\____/','  ||'],64,12,'k');
  c.rect(W-30,top-4,19,8,'k',true);c.line(W-26,top-1,W-13,top-1,'=','f');c.put(W-25,top+2,'(o)===','k');
  c.line(W-18,top+4,W-18,top+12,'|','k');c.put(W-21,top+12,'[===]','k');c.put(20,top-1,'[_______]','b');
 }else{
  drawer(c,W-34,top+7,24,9,pose.drawer);drawer(c,W-34,top+17,24,7,0);
  if(p.style==='secretary'){
   timber(c,14,10,W-28,top-13);for(let i=0;i<4;i++){c.rect(18+i*18,15,15,12,'d',true);c.put(21+i*18,22,'|||','f');}
   c.line(15,top-4,W-16,top-4,'=','k');c.put(W-28,top-7,'[o]','a');
  }
  book(c,20,top-5,0,0,0,true);c.put(48,top-2,'(o)','p');c.line(50,top-3,57,top-13,'/','f');c.rows(['  /',' ///','///',' /'],55,top-15,'c');
  if(pose.page>.1)c.line(33,top-5,33+pose.page*12,top-11*pose.page,'/','f');
 }
 return {contact:{x:W/2-14,y:top-3},entry:{x:W/2,y:H-3},surface:top};
}
function cabinet(c,p,t,pose){
 const W=p.w,H=p.h;for(const x of [16,W-17])leg(c,x,H-10,7,true);timber(c,8,9,W-16,H-17,'b',true);timber(c,5,6,W-10,5);
 if(p.style==='drawers'){for(let n=0;n<3;n++)drawer(c,14,15+n*13,W-28,11,n===1?pose.drawer:0);}
 else{
  c.clear(15,15,W-30,H-32);c.solid(15,15,W-30,H-32,'d');
  if(p.style==='glass'){
   for(let i=0;i<2;i++){const y=H-24-i*21;timber(c,16,y,W-32,4);bottle(c,24,y-7,i);c.rows([' .---.','/ : : \\','\\_____/' ],W-39,y-5,'p',true);}
   c.rect(15,15,W-30,H-32,'k');c.line(W/2,15,W/2,H-18,'|','k');c.rows(['  /',' /','/'],23,22,'w');c.rows(['  /',' /','/'],W-28,40,'w');
  }else{
   c.line(18,19,W-19,19,'=','k');
   for(const [i,x]of [27,46,66].entries()){
    c.rows(['   ?','  /\\',' /__\\'],x,20,'k');
    c.rows([' /|  |\\','/ |::| \\','  |::|','  |::|','  |::|','  |::|','  |::|','  |::|','  |__|'],x-1,23,i%2?'p':'q',true);
   }
   timber(c,17,H-26,W-34,4);for(const x of [24,48,72])c.rows(['  __',' /__\\','|____|'],x,H-29,'p',true);
   const leaf=Math.max(4,Math.round((W-30)/2*(1-pose.door)));timber(c,15,15,leaf,H-32,'b',true);timber(c,W-15-leaf,15,leaf,H-32,'b',true);
  }
  if(p.style==='glass')c.put(W/2-6,H/2,'(o) (o)','k');
  else{const leaf=Math.max(4,Math.round((W-30)/2*(1-pose.door)));c.put(15+leaf-4,H/2,'o','k');c.put(W-15-leaf+2,H/2,'o','k');}
 }
 return {contact:{x:W/2,y:H/2},entry:{x:W/2,y:H-3}};
}
function mirror(c,p,t,pose){
 const W=p.w,H=p.h,cx=W/2,cy=H/2-6,rx=W/2-13,ry=H/2-15;
 for(const x of [11,W-12]){leg(c,x,H-29,24,true);c.line(x,H-30,x,21,'|','b');c.put(x-1,21,'(o)','k');}
 c.line(12,H-13,W-13,H-13,'=','b');c.ellipse(cx,cy,rx+3,ry+3,'~','a',true);c.ellipse(cx,cy,rx,ry,'|','w',true);
 for(let y=cy-ry+3;y<cy+ry-3;y+=4){const half=rx*Math.sqrt(1-((y-cy)/ry)**2);c.line(cx-half+2,y,cx+half-2,y,'-','s');}
 for(const d of [-8,8])c.line(cx+d+5,cy-ry+7,cx+d-7,cy+ry-7,'/','c');
 if(p.style==='tilting'){c.put(cx-5,H-7,'/___\\','b');c.ellipse(cx,H-5,19,3,'=','b');}
 if(pose.polish>.1){const x=cx+Math.sin(t*2)*rx*.4,y=cy+Math.cos(t*2)*ry*.5;c.put(x,y,'*','c');c.put(x-2,y+1,'...','c');}
 return {contact:{x:cx,y:cy},entry:{x:cx,y:H-3},glass:{x:cx-rx,y:cy-ry,w:rx*2,h:ry*2}};
}
function dial(c,cx,cy,rx,ry,hour){
 cleanEllipse(c,cx,cy,rx,ry);
 c.ellipse(cx,cy,rx,ry,'=','a',true);c.ellipse(cx,cy,rx-2,ry-2,'-','c',true);
 for(let i=0;i<12;i++){const a=i*Math.PI/6-Math.PI/2;c.put(cx+Math.cos(a)*(rx-4),cy+Math.sin(a)*(ry-3),i%3?'.':['XII','III','VI','IX'][i/3],'k');}
 const minute=(hour%1)*Math.PI*2-Math.PI/2,h=hour/12*Math.PI*2-Math.PI/2;
 c.line(cx,cy,cx+Math.cos(minute)*(rx-6),cy+Math.sin(minute)*(ry-4),null,'k');c.line(cx,cy,cx+Math.cos(h)*(rx-9),cy+Math.sin(h)*(ry-6),null,'p');c.put(cx-1,cy,'(o)','k');
}
function clock(c,p,t,pose,ctx){
 const W=p.w,H=p.h,cx=W/2;
 if(p.style==='pendulum'){
  timber(c,13,20,W-26,H-26,'b',true);c.rows(['      ____','   .-\\____/-.','  /  .----.  \\',' /__/      \\__\\'],cx-9,3,'b',true);
  c.clear(20,46,W-40,H-58);c.rect(20,46,W-40,H-58,'d',true);c.line(21,48,W-22,48,'=','k');
  const swing=Math.sin(t*2.2)*6;c.line(cx,49,cx+swing,H-24,'|','a');c.ellipse(cx+swing,H-21,8,5,'=','a',true);
  for(const x of [25,W-26])c.line(x,48,x,H-27,'|','k');c.put(23,H-27,'[o]','k');c.put(W-28,H-27,'[o]','k');
  c.line(cx-7,6,cx-7,15,'|','b');c.line(cx+7,6,cx+7,15,'|','b');dial(c,cx,29,21,15,ctx.hour||0);timber(c,10,H-11,W-20,7);
 }else{
  c.ellipse(cx,H/2,27,21,'~','b',true);c.rows(['     __','  __/o \\___',' /   ____  >',' \\__/    \\_\\'],cx-9,1,'a',true);
  dial(c,cx,H/2+1,23,17,ctx.hour||0);c.put(cx-8,H-6,'<___> <___>','a');
 }
 return {contact:{x:cx,y:p.style==='pendulum'?29:H/2},entry:{x:cx,y:H-3}};
}
function hearth(c,p,t,pose){
 const W=p.w,H=p.h,cx=W/2;
 c.rect(13,14,W-26,H-23,'b',true);
 for(let y=17;y<H-11;y+=5){c.line(14,y,W-15,y,'_','s');for(let x=17+((y-17)/5%2)*8;x<W-17;x+=17){c.line(x,y,x,y+4,'|','s');c.put(x+3,y+2,'.:','f');}}
 c.rect(32,33,W-64,H-46,'d',true);c.clear(33,34,W-66,H-48);
 for(let i=0;i<3;i++){const x=cx-15+i*14,y=H-20;c.rows(['/======\\','| (~)  |','\\======/'],x-5,y,'b',true);}
 for(let i=0;i<7;i++){
  const x=cx-18+i*6,h=8+Math.sin(t*4+i)*4;
  for(let y=H-22-h;y<H-20;y++){const dx=Math.sin((y+t*5+i)*.7);c.put(x+dx,y,Math.floor(y+t*4)%3?'|':':',i%2?'p':'a');}
 }
 for(let x=32;x<W-31;x+=7)c.line(x,H-22,x,H-15,'|','k');c.line(30,H-15,W-31,H-15,'=','k');
 timber(c,7,12,W-14,6);timber(c,9,H-10,W-18,6);c.rows(['  .-.',' /   \\','|  |  |','|__|__|'],W-25,H-37,'k');c.line(W-21,H-31,W-21,H-13,'|','k');
 c.rows(['   _','  /o\\',' /___\\','   |',' __|__'],18,7,'p',true);c.put(cx-5,11,'[ HOME ]','a');
 return {contact:{x:cx,y:H-23},entry:{x:cx,y:H-3},warmth:{x:cx,y:H-3}};
}
function media(c,p,t,pose){
 const W=p.w,H=p.h;for(const x of [15,W-16])leg(c,x,H-10,7);timber(c,8,H-27,W-16,19);timber(c,5,H-30,W-10,5);
 for(const [x,w]of [[14,25],[45,26],[77,19]]){c.rect(x,H-22,w,10,'d',true);c.put(x+3,H-16,'||||||','p');}
 c.rect(15,10,W-30,H-45,'k',true);c.rect(20,14,W-48,H-53,'d',true);c.clear(21,15,W-50,H-55);
 c.rows(['   /\\        /\\','__/  \\______/  \\__','  ~~~   ~~~~   ~~~',' ~~   ~~~~    ~~','    ~~~  ~~  ~~~'],23,24,'w');
 const x=35+Math.sin(t*.4)*10;c.rows([' .-.','(o )>','/___\\'],x,31,'a',true);
 for(const y of [19,26,33])c.put(W-26,y,'(o)','f');c.line(W/2,10,W/2-13,2,'/','k');c.line(W/2,10,W/2+13,2,'\\','k');
 c.line(W/2-6,H-36,W/2-6,H-31,'|','k');c.line(W/2+6,H-36,W/2+6,H-31,'|','k');c.put(W/2-8,H-31,'|__|    |__|','k');
 return {contact:{x:W/2,y:H-32},entry:{x:W/2,y:H-3},screen:{x:20,y:14,w:W-48,h:H-53}};
}
const DRAW={chair,sofa,cushion,bench,hammock,table,shelf,desk,cabinet,mirror,clock,hearth,media};
export function furnitureSprite(base,item,time,{motion=true,state={},interaction=null,context={},pose={}}={}){
 const p=BLUEPRINTS[item.id];if(!p)return null;const c=new ObjectCanvas(p.w,p.h),active=Boolean(interaction&&!interaction.paused&&interaction.phase==='act'),t=motion?time:0;
 pose={press:0,sway:0,drawer:0,door:0,page:0,polish:0,slot:0,...(active?{press:.5+.3*Math.sin(t),sway:Math.sin(t*.8)*3,drawer:(Math.sin(t*.8)+1)/2,door:(Math.sin(t*.6)+1)/2,page:(Math.sin(t*1.2)+1)/2,polish:1}:{}),...pose};
 if(p.seat){
  // Cushions and hammock ropes follow actual occupants, never an idle timer.
  const seated=interaction?.seat_occupants||[],actor=seated.find(r=>r.phase==='inside')||seated[0];
  const sampled=actor?seatingPose(actor.routine,motion):null;
  pose={...pose,press:actor?.phase==='inside'?.5:0,sway:0,...sampled,slot:actor?.slot||0};
 }
 const anchors=DRAW[p.type](c,p,t,pose,context);
 if((state.dirt||0)>.3)c.put(16,p.h-8,':..:','s');
 if((state.condition??1)<.5)c.rows([' /','<',' \\'],p.w-20,p.h-13,'s');
 if((state.wetness||0)>.3)for(let i=0;i<4;i++)c.put(12+i*(p.w-25)/4,p.h-6-(Math.floor(t*4+i)%3),"'",'w');
 if(['fall','autumn'].includes(context.season)&&p.type==='bench'&&(pose.leaf||0)<1)c.put(p.w-32+(pose.leaf||0)*12,p.h-20+(pose.leaf||0)*6,'<;>','a');
 const inks={b:'#c7a177',f:'#e1c99f',s:'#958568',k:'#bccac1',q:'#92b5a3',p:'#c59c9c',g:'#a3b78a',a:'#e4c37d',w:'#9bc8ce',c:'#e6e0c8',d:'#15281f'};
 if(p.style==='velvet')Object.assign(inks,{q:'#b38fa9',p:'#d2a5af',b:'#b79a70'});
 if(p.style==='gold')Object.assign(inks,{b:'#d4b267',f:'#f0d58e',a:'#f1d994',q:'#a797b8',p:'#a78bb0'});
 return {...base,...c.finish(),inks,panels:{b:'#443a2b',f:'#514833',s:'#33392d',k:'#2c3b37',q:p.style==='velvet'?'#433140':'#29423a',p:'#493a39',g:'#35412c',a:'#54452b',w:'#294850',c:'#706b52',d:'#10251f'},
  construction:'furniture-v1',blueprint:item.id,detail:true,detailScale:.68,anchors,active,animated:active||['clock','hearth','media'].includes(p.type),lift:0,sway:0};
}
