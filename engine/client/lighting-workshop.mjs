import {ObjectCanvas} from './object-canvas.mjs';
import BLUEPRINTS from './animation/lighting.json' with {type:'json'};
import {lightOutput} from './lighting-state.mjs';
export {BLUEPRINTS as LIGHTING_BLUEPRINTS};
const mix=(a,b,t)=>'#'+a.slice(1).match(/../g).map((v,i)=>Math.round(parseInt(v,16)*(1-t)+parseInt(b.slice(1+i*2,3+i*2),16)*t).toString(16).padStart(2,'0')).join('');
function bar(c,x,y,xx,yy,w=3,tone='a'){c.beam(x,y,xx,yy,w,tone);}
function disk(c,x,y,rx,ry,tone='b'){c.ellipse(x,y,rx,ry,'_',tone,true);c.ellipse(x,y-1,rx-2,Math.max(1,ry-1),'-','f');}
function board(c,x,y,w,h,tone='b'){
 c.rect(x,y,w,h,tone,true);for(let j=y+3;j<y+h-2;j+=4)c.line(x+2,j,x+w-3,j,'~','s');
 for(const [xx,yy] of [[x+2,y+2],[x+w-3,y+2],[x+2,y+h-3],[x+w-3,y+h-3]])c.put(xx,yy,'o','a');
}
function glaze(c,x,y,rx,ry){
 for(let yy=-ry+2;yy<ry-1;yy+=3){
  const half=rx*Math.sqrt(1-(yy/ry)**2);
  for(let xx=-half+3;xx<half-2;xx+=5)c.put(x+xx,y+yy,xx<0?':':'.',xx<-rx*.5?'a':'s');
 }
 for(const dx of [-rx*.7,-rx*.55])c.line(x+dx,y-ry*.55,x+dx-2,y+ry*.4,':','f');
}
function base(c,p){const x=p.w/2,y=p.h-7;disk(c,x,y,p.w*.29,4,'k');c.line(x-p.w*.24,y+1,x+p.w*.24,y+1,'_','a');return {x,y};}
function plinth(c,p,w=p.w*.57){const x=(p.w-w)/2,y=p.h-17;board(c,x,y,w,11);c.put(x+4,p.h-5,'[__]','k');c.put(x+w-8,p.h-5,'[__]','k');}
function arch(c,p){
 for(const side of [-1,1]){const x=p.w/2+side*(p.w/2-12);bar(c,x,13,x,p.h-6,5,'k');disk(c,x,p.h-5,9,3,'a');c.put(x-1,20,'o','f');c.put(x-1,p.h-17,'o','f');}
 bar(c,12,13,p.w-12,13,3,'k');for(let x=12;x<=p.w-12;x++)c.put(x,12-7*Math.sin((x-12)/(p.w-24)*Math.PI),'_','a');
}
function bulb(c,x,y,r,env){
 c.ellipse(x,y,r,r*.75,'-',env.ink,true);c.put(x-2,y-1,env.on?'(~)':'(-)','f');c.put(x-2,y+r*.7,'[=]','a');
 env.source(x,y,.55);
}
function control(c,p,env,x=p.w-20,y=p.h-16){
 const pressed=env.press;
 c.rect(x-5,y-4,11,8,'k',true);c.rect(x-3,y-2,7,4,'a',true);c.put(x-2,y,pressed>.4?'v':env.on?'I':'O',env.on?'e':'s');
 c.line(x,y+4,x,p.h-7,'|','k');c.put(x-1,y-3,'o','f');
 return {x,y};
}
function flame(c,x,y,size,env){
 const h=Math.max(2,size*(.35+.65*env.level)),bend=env.wind*3+Math.sin(env.t*5+x)*1.6;
 if(env.level<.05){c.put(x-3,y,'__:_','s');return;}
 for(let j=0;j<h;j++){
  const q=j/h,half=Math.sin(q*Math.PI)*size*.42+q*2,cx=x+(1-q)*bend+Math.sin(q*11+env.t*4)*.8;
  c.solid(cx-half,y-h+j,half*2+1,1,q>.7?'e':'p');c.put(cx-half,y-h+j,q<.4?'/':'(','p');c.put(cx+half,y-h+j,q<.4?'\\':')','e');
  if(j%3===0){for(let k=-half+2;k<half-1;k+=4)c.put(cx+k,y-h+j,k<0?'/':':',q>.55?'f':'e');}
  if(j%4===1)c.put(cx+Math.sin(q*10+env.t*3)*half*.55,y-h+j,')','e');
 }
 c.put(x-2,y-2,'vvv','f');env.source(x,y-h*.5,1);
}
function shade(c,p,env){
 const cx=p.w/2,H=p.h;let capY=20,shadeH=25,topR=17,bottomR=32;
 if(p.style==='gooseneck'){
  base(c,p);bar(c,cx-12,H-10,cx-12,35,4,'k');
  const pts=[[cx-12,35],[cx-12,23],[cx-5,14],[cx+9,12],[cx+17,19]];
  for(let i=1;i<pts.length;i++)bar(c,...pts[i-1],...pts[i],4,'a');
  for(let y=40;y<H-18;y+=9)c.put(cx-13,y,'[=]','s');
  const x=cx+14;c.ellipse(x,34,22,13,'_','p',true);c.rect(x-22,34,45,7,'p',true);
  for(let yy=26;yy<35;yy+=3)c.line(x-12,yy,x+12,yy,'=','s');for(const dx of [-17,-11,11,17])c.line(x+dx*.5,24,x+dx,36,'/','a');
  c.line(x-21,39,x+21,39,'_','f');bulb(c,x,42,7,env);
  c.put(x-4,24,'(o)','a');c.line(cx-10,43,cx-10,H-13,':','s');
  return {control:control(c,p,env,cx-12,H-23),contact:{x:cx-12,y:H-23}};
 }
 if(p.style==='ceramic'){
  capY=9;shadeH=23;topR=15;bottomR=30;plinth(c,p,66);
  const y=H-37;c.ellipse(cx,y,15,18,'_','g',true);glaze(c,cx,y,15,18);disk(c,cx,y+15,17,3,'a');
  for(let yy=y-9;yy<y+12;yy+=7){c.put(cx-9,yy,'~\"~\"~\"~','p');c.put(cx-4,yy+3,'<o>','b');c.line(cx+7,yy-2,cx+10,yy+3,'/','p');}
  bar(c,cx,capY+shadeH,cx,y-15,3,'a');
 }else if(p.style==='tripod'){
  for(const sign of [-1,0,1]){bar(c,cx,51,cx+sign*30,H-8,4,'b');c.put(cx+sign*30-3,H-6,'[____]','k');}
  disk(c,cx,55,8,3,'a');c.line(cx-19,H-33,cx+19,H-33,'-','s');
 }else{
  capY=12;shadeH=30;topR=18;bottomR=33;plinth(c,p,66);
  for(let yy=capY+shadeH;yy<H-18;yy+=5)disk(c,cx,yy,8+Math.sin(yy)*2,3,'b');
 }
 bulb(c,cx,capY+shadeH-4,6,env);
 for(let yy=0;yy<shadeH;yy++){
  const radius=topR+(bottomR-topR)*yy/shadeH;c.clear(cx-radius,capY+yy,radius*2+1,1);c.solid(cx-radius,capY+yy,radius*2+1,1,'c');
  c.put(cx-radius,capY+yy,'/','a');c.put(cx+radius,capY+yy,'\\','b');
  for(let k=-3;k<=3;k++)c.put(cx+k*radius/4,capY+yy,yy%4?'|':':',p.style==='cozy'?'p':'s');
  if(yy%3===1)for(let xx=cx-radius+3;xx<cx+radius-2;xx+=5)c.put(xx,capY+yy,yy%2?':':'-','a');
  if(p.style==='cozy'&&yy%7===3)for(let xx=cx-radius+4;xx<cx+radius-3;xx+=8)c.put(xx,capY+yy,'<>','a');
 }
 c.line(cx-bottomR,capY+shadeH,cx+bottomR,capY+shadeH,'_','a');
 for(let x=cx-bottomR+2;x<cx+bottomR-1;x+=5)c.put(x,capY+shadeH+1,p.style==='cozy'?'v':'_','p');
 c.put(cx-2,capY-3,'(o)','a');
 const x=cx+bottomR-5,y=H-23;c.line(x,capY+shadeH,x,y+env.pull-2,':','a');c.put(x-2,y+env.pull,'(o)','a');
 return {control:{x,y},contact:{x,y}};
}
function lantern(c,p,env){
 const cx=p.w/2,fish=p.style==='fish';base(c,p);bar(c,16,p.h-9,16,12,5,'b');bar(c,16,12,cx+9,12,4,'b');
 c.line(cx,13,cx,21,'|','a');c.put(cx-3,19,'(   )','a');
 const y=51,rx=fish?30:27,ry=fish?27:25,sway=Math.sin(env.t*.9)*env.wind*2,x=cx+sway;
 c.ellipse(x,y,rx,ry,'_','c',true);
 for(let yy=-ry+3;yy<ry-1;yy+=4){const half=rx*Math.sqrt(1-(yy/ry)**2);c.line(x-half+1,y+yy,x+half-1,y+yy,'~','p');}
 for(const dx of [-.7,-.35,0,.35,.7])for(let yy=-ry+3;yy<ry-2;yy++)c.put(x+dx*rx*Math.sqrt(1-(yy/ry)**2),y+yy,'|','s');
 if(fish){c.rows(['     .--.',' >==/ o  \\','    \\__<>/','     \/\/'],x-9,y-5,'b');}
 else{c.rows(['  /\\',' /  \\','/____\\','  ||',' /__\\'],x-3,y-8,'a');c.put(x-17,y+7,'*','p');c.put(x+16,y-10,'*','p');}
 c.rect(x-13,y-ry,27,3,'a',true);c.rect(x-13,y+ry-1,27,3,'a',true);
 for(const dx of [-5,0,5]){c.line(x+dx,y+ry+3,x+dx+Math.sin(env.t+dx)*env.wind*2,y+ry+13,'|','p');c.put(x+dx-1,y+ry+14,'v','a');}
 env.source(x,y,1);c.line(18,24,18,p.h-24,':','s');return {control:control(c,p,env,18,p.h-22),contact:{x,y:y+ry-1}};
}
function festoon(c,p,env){
 for(const x of [12,p.w-13]){bar(c,x,17,x,p.h-7,4,'b');disk(c,x,p.h-5,9,3,'k');c.put(x-2,14,'(o)','a');}
 const ys=x=>20+18*Math.sin((x-12)/(p.w-25)*Math.PI);
 for(let x=12;x<p.w-12;x++)c.put(x,ys(x),'_','a');
 for(let i=0;i<7;i++){const x=23+i*(p.w-46)/6,y=ys(x)+4;bar(c,x,y-4,x,y,2,'k');bulb(c,x,y+5,5,{...env,on:env.on&&Math.sin(env.t*.9+i)>.05,ink:env.on?'e':'g'});c.put(x-2,y,'[=]','b');}
 c.line(14,24,14,p.h-22,':','s');return {control:control(c,p,env,14,p.h-20),contact:{x:14,y:p.h-20}};
}
function torch(c,p,env){
 const pair=p.style==='pair',xs=pair?[30,p.w-30]:[p.w/2];
 if(pair){for(const x of [14,p.w-15])board(c,x,22,7,p.h-29);for(const y of [32,72,96])board(c,12,y,p.w-24,5);}
 else base(c,p);
 for(const x of xs){
  const top=pair?40:43,ground=p.h-10;bar(c,x,top+6,x,ground,5,p.style==='woven'?'b':'k');
  if(pair){bar(c,x,71,x+(x<p.w/2?-11:11),57,4,'a');c.put(x-2,73,'(o)','a');}
  if(p.style==='woven'){
   for(let y=52;y<ground;y+=13)c.put(x-3,y,'[===]','a');
   c.ellipse(x,top+5,14,12,'_','b',true);for(let y=top-3;y<top+15;y+=3)c.put(x-10,y,'/X/X/X/X/X/X/X/X/X/X/','a');
   c.line(x-13,top-5,x+13,top-5,'_','f');
  }else{
   c.rect(x-12,top-2,25,21,'k',true);for(let dx=-8;dx<=8;dx+=8)c.line(x+dx,top,x+dx,top+16,'|','a');
   disk(c,x,top+18,16,3,'a');c.line(x-12,top-3,x+12,top-3,'=','f');
  }
  flame(c,x,top+2,24,env);
  if(p.style==='garden'){for(const side of [-1,1]){c.line(x+side*13,top-5,x+side*13,top-27,'|','k');}c.line(x-18,top-27,x+18,top-27,'_','a');}
 }
 return {control:control(c,p,env,xs[0],p.h-24),contact:{x:xs[0]-12,y:pair?55:58}};
}
function candles(c,p,env){
 const cx=p.w/2;base(c,p);bar(c,cx,p.h-10,cx,34,5,'a');
 for(let i=0;i<5;i++){
  const x=17+i*(p.w-34)/4,y=25+Math.abs(i-2)*7;
  for(let q=0;q<=20;q++){const u=q/20;bar(c,cx+(x-cx)*u,67-(67-(y+17))*u*u,cx+(x-cx)*Math.min(1,u+.05),67-(67-(y+17))*Math.min(1,u+.05)**2,2,'a');}
  disk(c,x,y+19,10,3,'a');c.rect(x-3,y,7,18,'c',true);c.put(x-2,y+2,'||','f');c.put(x+2,y+5,'v','s');
  flame(c,x,y,12,env);c.put(x,y-1,'|','k');
 }
 c.rows(['  /\\',' <()>','  \\/'],cx-3,76,'a');return {control:control(c,p,env,cx+19,p.h-18),contact:{x:cx,y:p.h-20}};
}
function chandelier(c,p,env){
 arch(c,p);const cx=p.w/2;c.line(cx,13,cx,27,':','a');disk(c,cx,29,9,4,'a');
 for(let i=0;i<5;i++){
  const x=25+i*(p.w-50)/4,y=43+Math.abs(i-2)*4;c.line(cx,29,x,y,'~','a');bulb(c,x,y+5,5,env);disk(c,x,y+10,10,3,'a');
  for(const dx of [-5,0,5]){const yy=y+18+(dx===0?9:0);c.line(x+dx,y+12,x+dx,yy,'|','a');c.rows([' /\\','<  >',' \\/'],x+dx-2,yy,'g');c.put(x+dx-1,yy+1,env.on?'*':':','f');}
 }
 for(let x=25;x<p.w-25;x++)c.put(x,66+6*Math.sin((x-25)/(p.w-50)*Math.PI),'o','g');
 c.line(p.w-14,18,p.w-14,p.h-22,':','a');return {control:control(c,p,env,p.w-15,p.h-20),contact:{x:p.w-15,y:p.h-20}};
}
function lava(c,p,env){
 const x=p.w/2;plinth(c,p,56);const y=17,h=60;
 for(let j=0;j<h;j++){const r=12+j*.16;c.solid(x-r,y+j,r*2+1,1,'g');c.put(x-r,y+j,'/','a');c.put(x+r,y+j,'\\','a');c.put(x-r+3,y+j,j%3?'|':':','f');}
 for(let i=0;i<4;i++){
  const q=env.on?((env.t*.045+i*.24)%1):.07+i*.035,cy=y+h-8-q*(h-17),cx=x+Math.sin(q*7+i)*6,rx=5+Math.sin(q*5+i)**2*4;
  c.ellipse(cx,cy,rx,5+i%2,'~',env.on?'e':'p',true);c.put(cx-2,cy-2,'~','f');
 }
 c.rect(x-14,y-6,29,8,'a',true);c.line(x-11,y-4,x+11,y-4,'_','f');c.rect(x-25,y+h,51,9,'a',true);c.line(x-23,y+h+6,x+23,y+h+6,'=','k');
 env.source(x,y+33,1);return {control:control(c,p,env,x+21,p.h-15),contact:{x:x+21,y:p.h-15}};
}
const LETTERS={Q:['.---.','|   |','| \\|',"'--\\'"],U:['|   |','|   |','|   |',"'---'"],A:[' .-. ','/   \\','|---|','|   |'],C:['.---.','|    ','|    ',"'---'"],K:['|  /','| / ','|<  ','| \\']};
function neon(c,p,env){
 board(c,9,14,p.w-18,49,'k');for(const x of [23,p.w-24])bar(c,x,63,x,p.h-6,5,'b');
 for(const [i,l] of [...'QUACK'].entries()){
  const x=16+i*23;for(const [y,row] of LETTERS[l].entries())for(const [j,ch] of [...row].entries())if(ch!==' '){
   const xx=x+j*4,yy=25+y*7;c.put(xx,yy,ch,env.ink);if(ch==='|'||ch==='/'||ch==='\\')c.line(xx,yy,xx+(ch==='/'?-2:ch==='\\'?2:0),yy+5,ch,env.ink);else c.line(xx,yy,xx+3,yy,ch,env.ink);
  }
  c.put(x+8,55,'o','a');env.source(x+8,35,.4);
 }
 c.rect(p.w-28,67,16,8,'a',true);c.put(p.w-26,70,'12V','k');return {control:control(c,p,env,22,p.h-13),contact:{x:22,y:p.h-13}};
}
function disco(c,p,env){
 arch(c,p);const x=p.w/2,y=49,rx=30,ry=26;c.line(x,13,x,y-ry,'|','a');c.ellipse(x,y,rx,ry,'_','g',true);
 for(let yy=-ry+3;yy<ry-2;yy+=5){const half=rx*Math.sqrt(1-(yy/ry)**2);for(let xx=-half+2;xx<half-3;xx+=6){const shine=env.on&&Math.sin(xx*.14+yy*.11+env.t*.7)>.55;c.rect(x+xx,y+yy,5,4,shine?'f':'s');if(shine)c.put(x+xx+2,y+yy+1,'*','e');}}
 c.rect(x-8,17,17,7,'k',true);c.put(x-4,20,'<o>','a');
 if(env.on)for(let i=0;i<6;i++){const a=env.t*.28+i*Math.PI/3;c.put(x+Math.cos(a)*40,y+Math.sin(a)*32,i%2?'+':'.','e');}
 env.source(x,y,1);return {control:control(c,p,env,p.w-14,p.h-20),contact:{x:p.w-14,y:p.h-20}};
}
function jar(c,p,env){
 const x=p.w/2,y=50;plinth(c,p,65);
 c.ellipse(x,21,23,16,'_','k');c.ellipse(x,21,20,13,'_','a');c.rect(x-25,27,51,47,'g',true);disk(c,x,74,25,5,'g');
 for(let i=0;i<5;i++){const yy=34+i*7;c.line(x-17,yy,x+17,yy+4,'~','a');c.put(x-18,yy,'o','p');c.put(x+17,yy+4,'o','p');}
 for(let i=0;i<9;i++){const xx=x-17+(i*13%35),yy=34+(i*11%34);c.put(xx,yy,env.on?(Math.sin(env.t*1.7+i)>.3?'*':'+'):'o',env.ink);}
 c.rect(x-28,23,57,7,'a',true);c.line(x-26,25,x+26,25,'=','f');c.put(x-22,46,'|','f');c.put(x+21,58,'|','f');
 c.rows([' .----.',' | LED|'," '----'"],x-3,58,'k');env.source(x,y,1);
 return {control:control(c,p,env,x+26,p.h-15),contact:{x:x+26,y:p.h-15}};
}
function spot(c,p,env){
 const x=p.w/2,y=39;for(const side of [-1,0,1])bar(c,x,67,x+side*29,p.h-7,3,'a');disk(c,x,67,9,3,'k');bar(c,x,59,x,67,4,'a');
 c.rect(22,19,61,39,'k',true);for(let i=0;i<8;i++)c.line(27+i*6,23,27+i*6,54,'|','s');
  for(const xx of [26,75])for(const yy of [23,52])c.put(xx,yy,'o','a');c.rect(34,29,31,15,'a',true);c.put(38,33,'P O N D','k');c.put(39,38,'F O C U S','k');
 disk(c,84,y,15,23,'a');disk(c,86,y,11,18,env.ink);c.ellipse(87,y,6,12,':','f');
 c.rows(['  /____',' /____/'],75,11,'k');c.rows([' \\___','  \\__\\'],75,61,'k');
 bar(c,21,39,21,65,4,'a');bar(c,21,65,70,65,4,'a');bar(c,70,65,70,59,4,'a');disk(c,21,40,6,4,'b');c.put(19,40,'(o)','f');
 c.line(32,57,35,78,'~','k');c.put(34,78,'[=]','a');env.source(88,y,1);return {control:control(c,p,env,35,p.h-16),contact:{x:21,y:40}};
}
function street(c,p,env){
 const x=p.w/2;const {y}=base(c,p);bar(c,x,58,x,y-4,7,'k');for(let yy=68;yy<p.h-14;yy+=14)disk(c,x,yy,7,2,'a');
 c.rect(x-22,26,45,34,'g',true);for(const dx of [-22,0,22])bar(c,x+dx,26,x+dx,60,2,'k');
 for(let yy=28;yy<59;yy++){c.put(x-20,yy,'|','f');if(yy%4===0)c.put(x+13,yy,'/','s');}
  for(const sign of [-1,1]){c.line(x+sign*20,28,x+sign*3,56,'/','s');c.put(x+sign*12,52,'<>','a');}
 for(let yy=0;yy<16;yy++){const half=6+yy*1.5;c.solid(x-half,10+yy,half*2+1,1,'k');c.put(x-half,10+yy,'/','a');c.put(x+half,10+yy,'\\','a');}
 c.line(x-30,26,x+30,26,'_','a');disk(c,x,61,25,4,'k');c.put(x-2,7,'(o)','a');
 for(const dx of [-12,12])bulb(c,x+dx,43,5,env);
 for(const side of [-1,1])c.rows(['  .-.',' (   )',"  '-'"],x+side*27-3,64,'a');
 return {control:control(c,p,env,x,p.h-26),contact:{x,y:p.h-26}};
}
function fire(c,p,env){
 const x=p.w/2,y=p.h-24;
 if(p.style==='eternal'){
  base(c,p);bar(c,x,p.h-11,x,y-6,8,'a');c.ellipse(x,y-8,32,11,'_','a',true);
  for(let i=0;i<7;i++){const xx=x-27+i*9;c.line(xx,y-8,xx+(xx-x)*.12,y-25,'/','b');c.put(xx+(xx-x)*.12,y-26,'<o>','f');}
  c.rect(x-16,p.h-15,33,5,'k',true);c.put(x-11,p.h-13,'S T I L L  H E R E','a');
  for(const dx of [-14,0,14])flame(c,x+dx,y-14,dx===0?45:29,{...env,level:1,ink:'e'});
 }else{
  for(let i=0;i<10;i++){const a=i*Math.PI/5,xx=x+Math.cos(a)*43,yy=y+Math.sin(a)*12;disk(c,xx,yy,10,5,i%3?'s':'k');c.put(xx-3,yy,'.:/','f');}
  for(const [x1,y1,x2,y2]of [[x-26,y-2,x+26,y+8],[x-26,y+7,x+28,y-5],[x-18,y-7,x+10,y+12]]){bar(c,x1,y1,x2,y2,8,'b');disk(c,x1,y1,5,3,'a');c.put(x1-1,y1,'@','k');}
  if(env.mode!=='off')for(const dx of [-15,0,15])flame(c,x+dx,y-1,dx===0?43:27,env);
  else{disk(c,x,y,36,12,'k');for(let xx=x-28;xx<x+30;xx+=7)c.line(xx,y-6,xx+4,y+6,'/','s');c.put(x-33,y+9,'(o)','a');}
  if(env.on&&env.mode!=='off')for(let i=0;i<3;i++)c.put(x+Math.sin(env.t+i)*8,6+((env.t*5+i*12)%19),'.','p');
 }
 return {control:{x:x-31,y:y+9},contact:{x:x-35,y:y+8},warmth:{x,y:y-20}};
}
function fireflies(c,p,env){
 const ground=p.h-6;
 for(let i=0;i<7;i++){
  const x=15+i*(p.w-30)/6,h=12+i%3*7;c.line(x,ground,x+Math.sin(i)*4,ground-h,'|','b');c.line(x,ground-4,x-7,ground-h+7,'/','s');c.put(x-1,ground-h,'(i)','a');
 }
 for(let i=0;i<13;i++){
  const x=14+(i*29%(p.w-28))+(env.on?Math.sin(env.t*.6+i)*4:0),y=env.on?15+(i*17%(p.h-42))+Math.cos(env.t*.8+i)*3:ground-10-i%4*3;
  const blinking=env.on&&Math.sin(env.t*1.4+i*1.9)>.1;c.put(x-1,y,blinking?'.*.':"'o'",blinking?'e':'s');c.put(x,y-1,Math.floor(env.t*8+i)%2?'v':'-','g');
  if(blinking)env.source(x,y,.7);
 }
 return {control:null,contact:{x:p.w/2,y:ground-8},observation:{x:p.w/2,y:35}};
}
function moon(c,p,env){
 const x=p.w/2,y=39,r=30;plinth(c,p,70);c.ellipse(x,y,r,29,'_',env.ink,true);
 for(let yy=-26;yy<=26;yy+=2)for(let xx=-27;xx<=27;xx+=3){
  if((xx/29)**2+(yy/28)**2>=1)continue;
  const mare=((xx+9)/15)**2+((yy-4)/20)**2<1,edge=xx>17||yy>18;
  c.put(x+xx,y+yy,mare?(yy%4===0?':':'.'):edge?':':'.',mare?'s':edge?'a':'g');
 }
 const craters=[[-13,-14,6,4],[12,-7,8,6],[-2,9,10,5],[15,16,5,3],[-17,8,4,5],[1,-21,3,2]];
 for(const [dx,dy,rx,ry]of craters){c.ellipse(x+dx,y+dy,rx,ry,':','s');c.ellipse(x+dx+1,y+dy+1,Math.max(1,rx-2),Math.max(1,ry-1),'.','g');c.put(x+dx-1,y+dy,'..','a');}
 for(let i=0;i<18;i++){const a=i*.71,rr=7+(i*7%22);c.put(x+Math.cos(a)*rr,y+Math.sin(a)*rr,'.','s');}
 for(const side of [-1,1])bar(c,x+side*27,61,x+side*14,p.h-19,4,'b');c.line(x-15,p.h-20,x+15,p.h-20,'_','a');
 env.source(x,y,1);return {control:control(c,p,env,x+26,p.h-15),contact:{x:x+26,y:p.h-15}};
}
function projector(c,p,env){
 const x=p.w/2,y=p.h-27;plinth(c,p,80);c.rect(x-34,y-15,69,21,'k',true);for(let xx=x-28;xx<x+30;xx+=5)c.line(xx,y-10,xx,y-2,'|','s');
 if(p.style==='hologram'){
  disk(c,x,y-15,33,7,'a');disk(c,x,y-16,27,5,env.ink);
  if(env.on){
   const bob=Math.sin(env.t)*1.4;
   c.rows(String.raw`                  .---..__
               .-' .  :   '-.
              / . :   . (o)  \___
              | : . :   .  ____/==>
              \  . : . _.-' '---'
               '--. : (
            __..--' .  |
        _.-' .  : .  :  \
      .' . : . ______   .\
     / .  :  .' : .  '-.  |
    / . :   / . : . :  \ :|
   / : .   /  . : . :   | |
  < . : . | : .  : . :  / |
   \_ : .  \__ . : . _.' :/
     '-. : .  '-----' . :/
        '---. : . : . _.'
             '---.---'
               / | \\
              /  |  \\
           __/   |   \__
          /___>  |  <___\
`.trimEnd().split('\n'),x-20,20+bob,'e');
   for(const side of [-1,1])for(let j=0;j<5;j++)c.put(x+side*(8+j*4),48+j*5,':','g');
   c.ellipse(x,67,22,4,'~','e');
  }
  env.source(x,y-18,1);
 }else if(p.style==='laser'){
  c.rect(x-36,y-29,73,19,'a',true);
  for(let i=0;i<3;i++){
   const xx=x-23+i*23;disk(c,xx,y-21,8,6,'k');disk(c,xx,y-21,4,3,env.ink);
   if(env.on){const end=x+(i-1)*43+Math.sin(env.t*.7+i)*7;c.line(xx,y-29,end,12+i*4,':',i===1?'p':'e');c.put(end,11+i*4,'+','f');}
   env.source(xx,y-21,.5);
  }
  c.line(x-39,y-31,x-39,y+1,'|','k');c.line(x+39,y-31,x+39,y+1,'|','k');
 }else{
  c.ellipse(x,y-22,28,20,'_','a',true);c.rect(x-29,y-22,59,18,'a',true);
  for(let i=0;i<19;i++){const angle=i*2.4+env.t*.08,rr=5+(i*7%20),xx=x+Math.cos(angle)*rr,yy=y-23+Math.sin(angle)*rr*.65;c.put(xx,yy,env.on?'*':'o',env.ink);}
  disk(c,x,y-4,31,4,'k');
  if(env.on)for(let i=0;i<17;i++){const xx=15+(i*37%(p.w-30)),yy=8+(i*11%31);c.put(xx+Math.sin(env.t*.15+i),yy,i%5?'.':'+','e');if(i%5===0)c.line(xx,yy,xx+5,yy+3,'.','g');}
  env.source(x,y-24,1);
 }
 c.rect(x-11,y+7,23,5,'a',true);c.put(x-7,y+9,env.on?'ON  .':'OFF .','k');return {control:control(c,p,env,x+27,p.h-13),contact:{x:x+27,y:p.h-13}};
}
function crystal(c,p,env){
 const x=p.w/2;plinth(c,p,68);
 const shards=[[-18,33,8],[-4,9,13],[18,27,10]];
 for(const [dx,top,r]of shards){const xx=x+dx,bottom=p.h-28;c.line(xx,top,xx-r,top+17,'/','a');c.line(xx,top,xx+r,top+18,'\\','f');
  for(let y=top+1;y<bottom;y++){const half=Math.min(r,(y-top)*r/17);c.solid(xx-half,y,half*2+1,1,'g');c.put(xx-half,y,'|','a');c.put(xx+half,y,'|','f');c.put(xx,y,y%5?':':'+',env.ink);}
  c.line(xx-r,bottom,xx,bottom+9,'\\','a');c.line(xx+r,bottom,xx,bottom+9,'/','a');c.line(xx,top,xx,bottom+9,'|',env.ink);
 }
 disk(c,x,p.h-24,32,5,'a');for(const dx of [-24,-12,0,12,24])c.put(x+dx,p.h-25,'^','k');
 if(!env.on){for(const side of [-1,1]){c.rect(x+side*20-10,38,21,38,'k',true);for(let yy=41;yy<74;yy+=4)c.line(x+side*20-8,yy,x+side*20+8,yy,'=','s');}}
 env.source(x,43,1);return {control:control(c,p,env,x+25,p.h-14),contact:{x:x+25,y:p.h-14}};
}
function glowsticks(c,p,env){
 const x=p.w/2;board(c,18,p.h-33,p.w-36,27,'b');c.rect(27,p.h-43,p.w-54,14,'k');
 for(let i=0;i<5;i++){
  const xx=25+i*12,top=18+i%3*7,tone=env.on?(i%2?'p':'e'):'g';bar(c,xx,top,xx+(i-2)*2,p.h-28,5,tone);
  c.put(xx-2,top-2,'[=]','f');c.put(xx-2,top+9,'::','f');env.source(xx,top+15,.35);
 }
 if(!env.on){board(c,19,p.h-64,p.w-38,38,'k');c.put(x-11,p.h-48,'L I G H T S','a');}
 c.line(23,p.h-18,p.w-24,p.h-18,'~','s');c.put(x-7,p.h-14,'*  *  *','a');return {control:control(c,p,env,p.w-20,p.h-15),contact:{x:p.w-20,y:p.h-15}};
}
const BUILDERS={shade,lantern,festoon,torch,candles,chandelier,lava,neon,disco,jar,spot,street,fire,fireflies,moon,projector,crystal,glowsticks};
export function lightingSprite(base,item,time,{motion=true,state={},context={},pose={}}={}){
 const p=BLUEPRINTS[item.id];if(!p)return null;
 const level=lightOutput(item.id,state,context),sources=[],t=motion?time:0;
 const env={t,level,mode:state.lighting?.mode||'auto',on:level>.08,ink:level>.08?'e':'g',wind:motion?(context.living?.ecology?.wind??.12):0,press:pose.light?.contact||0,pull:pose.light?.pull||0,
  source:(x,y,amount)=>{if(level>.01)sources.push({x,y,color:p.color,radius:p.radius,power:p.power*level*amount});}};
 const c=new ObjectCanvas(p.w,p.h),anchors=BUILDERS[p.type](c,p,env);
 anchors.entry={x:p.w/2,y:p.h-3};
 if(state.dirt>.35)for(const x of [p.w*.35,p.w*.5,p.w*.65])c.put(x,p.h-9,'.:','s');
 if(state.wetness>.45)for(const x of [p.w*.32,p.w*.5,p.w*.68])c.put(x,p.h-11,"'",'w');
 if(state.condition<.45)c.put(p.w*.4,p.h-8,'/','k');
 const inks={b:'#c3a27b',f:'#eee4c5',a:'#d3b77f',s:'#8a9b92',k:'#647e72',c:'#e2d2ad',p:'#d29e91',g:'#9db9b9',e:mix('#8d9d98',p.color,Math.max(.2,level)),w:'#a6cfd5'};
 const panels={b:'#443a2d',f:'#5a5842',a:'#4a412b',s:'#30433b',k:'#142722',c:'#595648',p:'#543b37',g:'#294548',e:mix('#29443f',p.color,level*.4),w:'#254047'};
 if(p.type==='shade'||p.type==='lantern'){
  // The paper/cloth itself warms; the ceramic, wood and ink keep their contrast.
  panels.c=mix('#3d4136',p.color,.1+level*.24);inks.c=mix('#c0b292',p.color,level*.65);
  if(p.style==='ceramic'){panels.g='#304d55';inks.g='#9bc4cf';inks.p='#b4d4cb';}
  if(p.style==='pagoda'){panels.c=mix('#4c302a',p.color,.12+level*.25);inks.p='#e2c198';}
 }
 if(['fire','torch','candles'].includes(p.type)){
  const eternal=p.style==='eternal';inks.p=eternal?'#8ad1df':'#f0b878';inks.f=eternal?'#d9f3ee':'#ffe4ae';
  panels.p=mix(eternal?'#18343d':'#482e23',p.color,.22+level*.26);panels.e=mix(eternal?'#34585c':'#71532f',p.color,level*.52);
  if(p.type==='candles'){panels.a='#384b4a';inks.a='#ced5c7';}
 }
 if(p.type==='moon'){panels.e=mix('#364a48',p.color,level*.33);inks.s='#8faba7';inks.g='#c0cfbc';}
 if(p.type==='crystal'){panels.g=mix('#333c53',p.color,level*.24);inks.g='#b6b7d6';inks.a='#a0b9cb';}
 if(p.type==='neon')inks.e=mix('#777b84','#f6b2d7',level);
 return {...base,...c.finish(),construction:'lighting-v1',detail:true,detailScale:.62,blueprint:item.id,anchors,inks,panels,sway:0,lift:0,
  animated:motion,emissive:level>.01,lightSources:sources,lightLevel:level,active:state.active||false};
}
