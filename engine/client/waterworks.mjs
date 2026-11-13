import {ObjectCanvas} from './object-canvas.mjs';
import BLUEPRINTS from './animation/waterworks.json' with {type:'json'};
import {waterPose} from './water-routines.mjs';
export {BLUEPRINTS as WATER_BLUEPRINTS};
const clamp=n=>Math.max(0,Math.min(1,n));
const night=ctx=>ctx.hour<6||ctx.hour>=19;
// Real kept fish (engine/keeping.py): species glyph and length from the catch,
// depth by species, resting outside their active hours, glow, hungry surfacing.
const FISHART={minnow:['>','<'],goldfish:['><>','<><'],carp:['><=((>','<))=><'],bass:['><((*>','<*))><'],catfish:['=<((:>','<:))>='],trout:['><--*>','<*--><'],
 koi:['><((o>','<o))><'],salmon:['><==)>','<(==><'],golden_koi:['><((@>','<@))><'],ghost_fish:['>:.:>','<:.:<']};
const DWELL={minnow:-2,goldfish:-2,koi:-2,golden_koi:-2,bass:0,trout:0,salmon:0,ghost_fish:0,carp:2,catfish:2};
const ACTIVE={goldfish:[6,16],trout:[5,11],catfish:[17,30],ghost_fish:[19,29],golden_koi:[5,10]};
function keptFish(c,fish,cx,cy,rx,t,ctx){
 const h=ctx.hour??12;
 fish.forEach((f,i)=>{
  const seed=[...f.id].reduce((n,ch)=>(n*31+ch.charCodeAt(0))>>>0,7),win=ACTIVE[f.species],hh=h<5?h+24:h;
  const awake=!win||(hh>=win[0]&&hh<win[1]),speed=awake?.25+(seed%7)/20:.03,a=t*speed+seed%628/100;
  const dir=Math.cos(a)>0?0:1,x=cx+Math.sin(a)*rx*(.35+(seed%40)/100),y=cy+DWELL[f.species]+Math.cos(a*1.3)*1.5+(f.hunger>.65&&awake?-2:0);
  let glyph=FISHART[f.species][dir];if(f.size>45)glyph=glyph.replace(/[(=:-]/g,m=>m+m);
  const glow=(f.species==='ghost_fish'&&(h<6||h>=19))||(f.species==='golden_koi'&&h>=5&&h<9);
  c.put(x-glyph.length/2,y,glyph,glow?'f':f.species.includes('koi')?'a':f.species==='goldfish'?'p':'c');
  if(f.hunger>.65&&awake)c.put(x+(dir?-1:1)*(glyph.length/2+1),y-1,'o','c');
  if(glow)for(const d of [-1,1])c.put(x+d*(glyph.length/2+1),y,'.','f');
  if(!awake)c.put(x,y-1,'z','s');
 });
}

function masonry(c,x,y,w,h,stone='b'){
 c.rect(x,y,w,h,stone,true);
 for(let yy=2;yy<h-1;yy+=4){
  c.line(x+1,y+yy,x+w-2,y+yy,'_','s');
  for(let xx=2+((yy-2)/4%2)*6;xx<w-2;xx+=12){c.line(x+xx,y+yy,x+xx,Math.min(y+h-2,y+yy+3),'|','s');if(xx+5<w-2)c.put(x+xx+2,y+yy+2,'.:','f');}
 }
 c.line(x+1,y+1,x+w-2,y+1,'=','f');
}
function boulder(c,x,y,w,h){
 const edge=[[.16,0],[.72,0],[1,.2],[.92,.8],[.7,1],[.13,.94],[0,.7],[.04,.2]].map(([a,b])=>[x+a*w,y+b*h]);
 for(let yy=y;yy<=y+h;yy++){
  const hits=[];
  for(let i=0;i<edge.length;i++){
   const a=edge[i],b=edge[(i+1)%edge.length];
   if(a[1]!==b[1]&&yy>=Math.min(a[1],b[1])&&yy<=Math.max(a[1],b[1]))hits.push(a[0]+(b[0]-a[0])*(yy-a[1])/(b[1]-a[1]));
  }
  if(!hits.length)continue;const left=Math.ceil(Math.min(...hits)),right=Math.floor(Math.max(...hits));
  c.clear(left,yy,right-left+1,1);c.solid(left,yy,right-left+1,1,'b');
  if((yy-y)%4===2)c.line(left+2,yy,right-2,yy,'~','s');
  if((yy-y)%5===0&&right-left>8)c.put(left+4,yy,'.:','f');
 }
 for(let i=0;i<edge.length;i++)c.line(...edge[i],...edge[(i+1)%edge.length],null,i<4?'s':'f');
 c.line(x+w*.7,y+3,x+w*.5,y+h*.5,'/','s');c.line(x+w*.5,y+h*.5,x+w*.6,y+h-3,'|','s');
}
function water(c,x,y,rx,ry,t,{frozen=false,bubbles=false,active=false}={}){
 for(let yy=-Math.floor(ry);yy<=ry;yy++){
  const half=Math.floor(rx*Math.sqrt(Math.max(0,1-(yy/ry)**2)));
  c.clear(Math.round(x)-half,Math.round(y)+yy,half*2+1,1);
 }
 c.ellipse(x,y,rx,ry,'~','w',true);
 for(let yy=-Math.floor(ry)+1;yy<ry;yy+=2){
  const half=rx*Math.sqrt(Math.max(0,1-(yy/ry)**2));
  for(let xx=-half+3;xx<half-4;xx+=9){
   const phase=Math.floor(t*3+xx*.2+yy),text=frozen?(Math.round(xx+yy)%3?'_/':'\\/_'):bubbles?['.o.','(o)','o .',' . '][((phase%4)+4)%4]:['~--','--~','._.','~~~'][((phase%4)+4)%4];
   c.put(x+xx,y+yy,text,frozen?'i':(Math.round(xx+yy)%3?'w':'c'));
  }
 }
 if(active&&!frozen)for(const sign of [-1,1]){
  const r=3+((t*4)%7);c.put(x+sign*r,y+1,sign<0?'(':')','c');c.put(x+sign*(r+2),y+2,'~','w');
 }
}
function stoneRing(c,cx,cy,rx,ry,tone='b'){
 c.ellipse(cx,cy+3,rx+3,ry+2,'_','s',true);c.ellipse(cx,cy,rx+3,ry+2,'=','f',true);
 for(let a=0;a<Math.PI*2;a+=Math.PI/12){const x=cx+Math.cos(a)*(rx+1),y=cy+Math.sin(a)*(ry+1);c.put(x,y,a<Math.PI?'/':'|',tone);}
}
function stream(c,x0,y0,x1,y1,rise,t,{frozen=false,wide=1}={}){
 const points=[];
 for(let n=0;n<=28;n++){
  const u=n/28,x=x0+(x1-x0)*u,y=y0+(y1-y0)*u-Math.sin(Math.PI*u)*rise;
  points.push([x,y]);if(frozen||n%4!==Math.floor(t*8)%4)for(let k=0;k<wide;k++)c.put(x+k,y,frozen?'|':n%3?'|':':',frozen?'i':n%3?'w':'c');
 }
 if(!frozen){c.put(x1-2,y1,'~._~','c');c.put(x1+(Math.floor(t*5)%2?2:-2),y1-1,"'",'w');}
 return points;
}
function lily(c,x,y,flower=true){c.rows([' .----.','( . /  )'," '----'"],x-4,y-1,'g',true);if(flower)c.put(x-1,y-2,'{*}','p');}
function reeds(c,x,y,height=10){for(const d of [-3,0,3]){c.line(x+d,y,x+d+d*.7,y-height+Math.abs(d),'|','g');c.put(x+d+d*.7,y-height+Math.abs(d)-1,'#','a');}c.put(x-4,y,'\\|/\\|/','g');}
function ladder(c,x,y,depth){
 for(const dx of [-3,6]){c.rows([' .-.','/   |','    |'],x+dx-3,y,'k');c.line(x+dx+1,y+3,x+dx+1,y+depth,'|','k');}
 for(let yy=4;yy<=depth;yy+=3)c.line(x-2,y+yy,x+7,y+yy,'=','k');
}
function pool(c,p,t,ctx,state,active,frozen){
 const W=p.w,H=p.h,cx=W/2,cy=H-(p.heated?24:20),rx=W/2-12,ry=11,wood=p.style==='cedar',spa=p.style==='spa',natural=['natural','koi'].includes(p.style);
 if(wood||spa){
  c.ellipse(cx,cy+12,rx,9,'_','b',true);
  for(let y=cy;y<cy+13;y++){c.solid(cx-rx,y,rx*2,1,'b');c.put(cx-rx,y,'|','f');c.put(cx+rx,y,'|','s');}
  if(wood){for(let x=cx-rx+3;x<cx+rx-2;x+=6){c.line(x,cy+1,x,cy+17,'|','s');c.put(x+2,cy+9,'(=)','f');}for(const y of [cy+5,cy+13]){c.line(cx-rx+1,y,cx+rx-1,y,'=','k');for(let x=cx-rx+6;x<cx+rx-4;x+=12)c.put(x,y,'o','k');}}
  else{for(let y=cy+4;y<cy+17;y+=3)for(let x=cx-rx+4;x<cx+rx-2;x+=5)c.put(x,y,'[.]','q');c.rows(['[ o : o ]','[ - + ~ ]'],W-26,cy+6,'k');}
  stoneRing(c,cx,cy,rx,ry,wood?'b':'q');
  water(c,cx,cy,rx-4,ry-3,t,{frozen,bubbles:true,active});
  for(const side of [-1,1])c.ellipse(cx+side*(rx-12),cy-6,8,2,'-','q',true);
  for(let i=0;i<3;i++){
   const x=cx-21+i*20+Math.sin(t*.8+i)*2,y=cy-14-(Math.floor(t*2+i*3)%8);
   c.put(x,y,'~','c');c.put(x+1,y-2,'.','c');
  }
  c.rect(9,H-9,20,6,'b',true);c.line(10,H-8,27,H-8,'_','f');c.rect(14,H-12,15,4,'b',true);
  if(spa){c.rect(W-22,H-13,14,8,'q',true);c.rows(['=======',' : : : ','======='],W-21,H-13,'c');}
 }else if(p.style==='inflatable'){
  for(let j=4;j>=0;j-=2)c.ellipse(cx,cy+j,rx,ry,'=','a',true);
  for(let x=cx-rx+6;x<cx+rx-4;x+=8)c.line(x,cy+ry-2,x+2,cy+ry+3,':','p');
  water(c,cx,cy-1,rx-5,ry-4,t,{frozen,active});
  for(let a=.1;a<Math.PI;a+=.28)c.put(cx+Math.cos(a)*(rx-2),cy+Math.sin(a)*(ry-1),'(o)','p');
  c.rows(['.---.','| + |',"'---'"],W-20,cy+ry-2,'f');c.put(12,cy+ry,'(o)','k');
 }else if(natural){
  for(let a=0;a<Math.PI*2;a+=.25){const x=cx+Math.cos(a)*(rx+1),y=cy+Math.sin(a)*(ry+2);c.ellipse(x,y,5+Math.sin(a*3),2, '_','b',true);c.put(x-2,y,'.:','f');}
  water(c,cx,cy,rx-3,ry-1,t,{frozen,active});
  reeds(c,12,H-12,15);reeds(c,W-12,cy-3,13);lily(c,cx+rx*.45,cy+1);lily(c,cx-rx*.4,cy-4,ctx.season!=='winter');
  if(p.style==='koi'){
   const kept=state.keeping?.fish||[];
   if(kept.length&&!frozen)keptFish(c,kept,cx,cy,rx,t,ctx);
   else if(!kept.length)for(const [i,tone]of [[0,'a'],[1,'p'],[2,'c']]){const x=cx+Math.sin(t*.22+i*2)*rx*.5,y=cy+Math.cos(t*.22+i*2)*4;c.put(x-3,y,i%2?'<o))><':'><((o>',tone);}
   for(let x=18;x<46;x++){const y=cy-12-Math.sin((x-18)/28*Math.PI)*4;c.put(x,y,'=','b');c.put(x,y-5,'~','f');if(x%5===0)c.line(x,y-4,x,y,'|','f');}
  }else{c.rows(['  ___',' /:  \\','/_.___\\'],W-28,cy-17,'b',true);c.put(W-22,cy-18,'\\|/','g');}
 }else{
  const x=8,y=cy-13,w=W-16,h=29;masonry(c,x,y,w,h,'b');
  c.clear(x+4,y+3,w-8,h-7);c.rect(x+4,y+3,w-8,h-7,'q',true);c.rect(x+7,y+5,w-14,h-11,'w',true);
  for(let xx=x+6;xx<x+w-5;xx+=6)c.put(xx,y+2,'[]','q');
  for(let yy=y+7;yy<y+h-7;yy+=3)for(let xx=x+10;xx<x+w-11;xx+=8)c.put(xx,yy,frozen?'_/__':((Math.floor(t*4)+xx+yy)%3?'~--':'._~'),frozen?'i':'w');
  if(p.style==='lap'){
   for(let xx=x+12;xx<x+w-10;xx+=4)c.put(xx,cy,'.','q');c.line(x+12,cy+7,x+w-12,cy+7,'_','s');c.put(x+16,cy+6,'[3]','f');
   ladder(c,W-23,cy-12,21);c.rect(13,y-7,21,5,'q',true);c.line(17,y-3,17,y,'|','k');
  }else{
   for(let xx=15;xx<W-15;xx+=2)stream(c,xx,cy+9,xx,cy+17,0,t,{frozen});
   c.line(12,cy+18,W-13,cy+18,'~','w');c.rect(14,cy-19,20,4,'b',true);c.rect(W-37,cy-19,20,4,'b',true);
   c.put(19,cy-18,' : : : : ','f');c.put(W-32,cy-18,' : : : : ','f');
  }
 }
 return {seat:{x:cx,y:cy+2},entry:{x:cx-rx+5,y:cy+10},contact:{x:cx-rx+8,y:cy},water:{x:cx-rx+6,y:cy-6,w:rx*2-12,h:14},rim:cy+8,swimRadius:Math.max(6,rx-22)};
}
function fountain(c,p,t,ctx,state,active,frozen){
 const W=p.w,H=p.h,cx=W/2,cy=H-14,rx=W/2-10;
 masonry(c,9,H-15,W-18,11);stoneRing(c,cx,cy-2,rx-3,7);water(c,cx,cy-3,rx-7,4,t,{frozen,active});
 let lip={x:cx,y:cy-14};
 if(p.style==='tiered'){
  masonry(c,cx-6,18,13,H-38);c.ellipse(cx,14,4,3,'*','a',true);
  for(const [y,r]of [[27,17],[47,28]]){
   c.ellipse(cx,y+3,r-4,4,'_','b',true);stoneRing(c,cx,y,r,4);water(c,cx,y,r-3,2,t,{frozen});
   for(const side of [-1,1])stream(c,cx+side*(r-2),y+2,cx+side*(r+7),y+19,2,t,{frozen});
   c.put(cx-3,y+6,'{o}','a');
  }
  stream(c,cx,14,cx-11,26,9,t,{frozen});stream(c,cx+1,14,cx+11,26,9,t+.4,{frozen});lip={x:cx-28,y:49};
 }else if(p.style==='shell'){
  masonry(c,cx-5,28,11,H-43);c.ellipse(cx,26,24,11,'~','f',true);
  for(let a=Math.PI;a<Math.PI*2;a+=.24)c.line(cx,34,cx+Math.cos(a)*22,27+Math.sin(a)*10,'/','s');
  water(c,cx,34,18,3,t,{frozen});stream(c,cx-15,34,cx-17,cy-4,0,t,{frozen});stream(c,cx+14,34,cx+18,cy-4,0,t+.4,{frozen});lip={x:cx-15,y:34};
 }else if(p.style==='urn'){
  masonry(c,cx-12,cy-7,25,8);c.ellipse(cx+3,24,15,13,'_','p',true);c.ellipse(cx-10,17,7,5,'=','f',true);
  for(let y=17;y<34;y+=4)c.put(cx-2,y,'<><><><>','a');c.ellipse(cx+18,24,5,7,'~','k');
  stream(c,cx-15,18,cx-24,cy-4,1,t,{frozen,wide:2});lip={x:cx-15,y:18};
 }else if(p.style==='pump'){
  masonry(c,cx-10,cy-7,21,9);c.rect(cx-4,16,9,cy-22,'k',true);c.ellipse(cx,16,7,3,'=','k',true);
  c.rect(cx-18,23,17,5,'k',true);c.line(cx-18,25,cx-18,31,'|','f');c.line(cx+6,18,cx+20,12,'/','k');c.line(cx+20,12,cx+24,27,'|','k');c.put(cx+22,27,'[=]','b');
  for(let y=23;y<cy-9;y+=5)c.put(cx-2,y,'[o]','f');stream(c,cx-17,31,cx-17,cy-4,0,t,{frozen,wide:2});lip={x:cx-17,y:31};
 }else if(p.style==='wishing'){
  masonry(c,cx-8,25,17,cy-27);c.ellipse(cx,24,23,6,'=','a',true);water(c,cx,23,19,3,t,{frozen});
  for(const side of [-1,1]){c.line(cx+side*30,11,cx+side*30,cy-6,'|','k');c.rows([' .-.','/___\\','| * |',"'---'"],cx+side*30-2,12,night(ctx)?'a':'f',true);stream(c,cx+side*20,25,cx+side*25,cy-4,2,t+side,{frozen});}
  for(let x=14;x<W-16;x+=11)c.put(x,cy-4+(x%3),'(o)','a');c.rows([' .-*- .','/  |  \\',"'--+--'"],cx-3,8,'a');lip={x:cx-20,y:25};
 }else if(p.style==='heron'){
  masonry(c,cx-11,cy-9,24,10);c.line(cx-2,36,cx-2,cy-10,'|','f');c.line(cx+7,38,cx+3,cy-10,'/','f');
  c.ellipse(cx,35,13,7,'~','b',true);c.rows(['  __',' / .\\___','(  O____>',' |  |',' |  |',' |  |',' |  |',' |  |',' |  |','/   |','|   |','|   |'],cx+7,10,'f',true);
  for(let y=21;y<=34;y++){c.solid(cx+8,y,5,1,'b');c.put(cx+8,y,'|','f');c.put(cx+12,y,'|','s');}
  for(let n=0;n<5;n++)c.put(cx-7+n*3,33+n%2,'\\v','s');stream(c,cx+16,13,cx+29,cy-5,1,t,{frozen});lip={x:cx+16,y:13};
 }else{
  masonry(c,cx-13,cy-11,28,12);c.ellipse(cx,cy-23,19,9,'~','b',true);c.ellipse(cx+12,cy-36,11,8,'_','b',true);
  c.rows(['_________','\\_______>'],cx+18,cy-37,'a');c.put(cx+16,cy-39,'O','k');c.ellipse(cx-2,cy-23,10,5,'~','f');c.put(cx-21,cy-23,'<','b');
  for(const x of [cx-8,cx+5]){c.line(x,cy-15,x,cy-11,'|','a');c.put(x-3,cy-11,'<___>','a');}
  for(let j=0;j<3;j++)c.put(cx-9+j*5,cy-25+j,'vv','s');stream(c,cx+27,cy-36,cx+30,cy-4,2,t,{frozen});lip={x:cx+27,y:cy-36};
 }
 return {seat:{x:cx-17,y:cy-3},entry:{x:cx-20,y:H-3},contact:lip,water:{x:cx-rx+8,y:cy-6,w:rx*2-16,h:7},rim:cy+2,swimRadius:5};
}
function cascade(c,p,t,ctx,state,active,frozen){
 const W=p.w,H=p.h,cx=W/2,cy=H-10;
 stoneRing(c,cx,cy-2,W/2-10,6);water(c,cx,cy-3,W/2-16,4,t,{frozen,active});
 if(p.style==='cliff'){
  for(const [x,y,w,h]of [[12,43,34,27],[59,39,37,30],[23,23,34,25],[54,13,33,28],[34,5,35,21]]){
   boulder(c,x,y,w,h);
   for(let xx=x+4;xx<x+w-5;xx+=7)c.put(xx,y+h-1,'\\|/','g');
  }
  for(const [x,y,x2,y2,width]of [[51,19,53,35,8],[53,37,46,53,12],[46,55,52,cy-4,16]]){
   c.line(x-3,y,x+width+1,y,'~','c');for(let k=0;k<width;k+=2)stream(c,x+k,y+1,x2+k,y2,0,t+k*.13,{frozen});
   c.ellipse(x2+width/2,y2,width/2+2,2,'~','w');
  }
  reeds(c,18,cy-2,14);c.put(88,36,'\\|/','g');
 }else{
  for(const [x,y,rx,ry]of [[57,17,16,10],[33,34,18,10],[53,51,20,9]]){
   c.ellipse(x,y+2,rx,ry,'_','p',true);for(let yy=-ry+4;yy<ry-2;yy+=4)c.line(x-rx+5,y+yy,x+rx-5,y+yy,'~','a');
   water(c,x,y-6,rx-2,3,t,{frozen});c.put(x-rx+2,y-6,'[','f');
  }
  stream(c,43,12,25,27,1,t,{frozen,wide:2});stream(c,47,28,62,44,1,t+.5,{frozen,wide:2});stream(c,37,46,32,cy-3,1,t+1,{frozen,wide:2});
  c.rows(['  ||','\\ || /',' \\||/',' /||\\'],13,19,'g');
 }
 return {seat:{x:cx-15,y:cy-2},entry:{x:cx-22,y:H-2},contact:{x:cx,y:cy-4},water:{x:12,y:cy-6,w:W-24,h:7},rim:cy+2,swimRadius:8};
}
function bath(c,p,t,ctx,state,active,frozen){
 const W=p.w,H=p.h,cx=W/2,cy=p.style==='log'?15:18,rx=W/2-12;
 if(p.style==='log'){
  c.rect(10,cy+3,W-20,17,'b',true);for(let y=cy+5;y<cy+19;y+=4)c.line(12,y,W-13,y,'~','s');
  c.ellipse(12,cy+10,7,10,'_','b',true);c.ellipse(12,cy+10,4,7,'~','f');c.put(11,cy+10,'o','s');c.rows([' |\\','/||\\'],W-19,cy+12,'g');
 }else{
  c.ellipse(cx,H-8,20,5,'=','b',true);c.rect(cx-7,cy+5,15,H-cy-15,'b',true);
  for(let x=cx-5;x<=cx+5;x+=5)c.line(x,cy+7,x,H-12,'|','f');
  if(p.style==='vine')for(let y=cy+6;y<H-10;y+=3){const x=cx+Math.sin(y*.35)*7;c.put(x,y,'~','g');c.put(x+2,y,'<>','g');if(y%2)c.put(x-3,y,'(*)','p');}
  else for(let y=cy+9;y<H-12;y+=7)c.put(cx-3,y,'{o}','a');
 }
 stoneRing(c,cx,cy,rx,6);water(c,cx,cy-1,rx-4,4,t,{frozen,active});
 if(p.style==='vine'){c.rows([' .-.','(o )>','/  _\\','\\_/'],W-20,cy-12,'b',true);c.put(W-20,cy-8,'vv','a');}
 return {seat:{x:cx,y:cy},entry:{x:cx-rx+3,y:H-4},contact:{x:cx-rx+5,y:cy-1},water:{x:cx-rx+6,y:cy-4,w:rx*2-12,h:7},rim:cy+4,swimRadius:7};
}
function bowl(c,p,t,ctx,state,active,frozen){
 const cx=p.w/2,cy=13,rx=24;
 for(let j=5;j>=0;j--)c.ellipse(cx,cy+j,rx-j*.3,6,'_','b',true);
 c.ellipse(cx,cy,rx,6,'=','f',true);water(c,cx,cy-1,rx-4,4,t,{frozen,active});
 for(let x=15;x<p.w-15;x+=8){c.put(x,cy+7,'<>','s');c.put(x+2,cy+5,'.','f');}
 c.put(cx-3,cy+7,'(v)','a');
 return {seat:{x:cx-12,y:cy},entry:{x:cx-20,y:p.h-4},contact:{x:cx-rx+6,y:cy},water:{x:cx-rx+6,y:cy-4,w:rx*2-12,h:7},rim:cy+4,swimRadius:3};
}
function spray(c,p,t,ctx,state,active,frozen){
 const W=p.w,H=p.h,cx=W/2,cy=H-13,rotary=p.style==='rotary';
 c.ellipse(cx,cy+5,18,4,'=','k',true);c.rect(cx-7,cy-2,15,7,'k',true);c.put(cx-4,cy+1,'( O )','f');
 for(const side of [-1,1]){c.put(cx+side*13-1,cy+5,'[o]','a');c.line(cx+side*12,cy+5,cx+side*20,cy+9,'/','k');}
 c.ellipse(19,cy+5,9,3,'~','g');c.ellipse(19,cy+5,6,2,'~','g');c.put(cx-4,cy+3,'-+-','a');
 const arm=rotary?Math.sin(t*1.4)*14:24;
 c.line(cx-arm,cy-4,cx+arm,cy-4,'=','f');c.line(cx,cy-4,cx,cy+1,'|','k');
 for(let x=9;x<cx-10;x++)c.put(x,cy+6+Math.sin(x*.18)*2,'~','g');c.put(cx-12,cy+5,'[=]','a');
 if(rotary){for(const sign of [-1,1])stream(c,cx+sign*arm,cy-4,cx+sign*(35+Math.sin(t)*3),cy+6,17,t,{frozen});}
 else for(let i=-4;i<=4;i++){const x=cx+i*5;c.put(x,cy-4,'o','a');stream(c,x,cy-5,x+Math.sin(t*.8)*15,cy+7,25+Math.cos(i)*2,t+i*.2,{frozen});}
 return {seat:{x:cx-25,y:cy+6},entry:{x:cx-31,y:H-3},contact:{x:cx-25,y:cy-8},water:{x:8,y:cy-10,w:W-16,h:17},rim:H,swimRadius:12};
}
function mat(c,p,t,ctx,state,active){
 const W=p.w,H=p.h;c.ellipse(W/2,H/2,W/2-7,H/2-5,'=','q',true);
 for(let y=5;y<H-5;y++){
  const half=(W/2-9)*Math.sqrt(Math.max(0,1-((y-H/2)/(H/2-5))**2));
  for(let x=Math.ceil(W/2-half);x<W/2+half;x++)c.put(x,y,(x+y)%2?'~':':',y%4?'w':'q');
 }
 lily(c,W/2+15,H/2);c.rows([' .-.','(o )>','/___\\'],W/2-18,H/2-3,'a');
 for(let x=20;x<W-20;x+=4)c.put(x,H-4,"'",'f');
 if(active){const fold=W/2+Math.sin(t*2)*12;for(let y=9;y<H-8;y++){c.clear(fold+(y-H/2)*.2,y,2,1);c.put(fold+(y-H/2)*.2,y,'/','f');}}
 if((state.dirt||0)>.3)c.put(21,H-10,':..::','s');
 if((state.condition??1)<.5)c.rows([' /','/','|'],W-22,H-9,'s');
 return {contact:{x:W/2,y:H/2}};
}
const DRAW={pool,fountain,cascade,bath,bowl,spray,mat};
export function waterworksSprite(base,item,time,{motion=true,state={},interaction=null,context={}}={}){
 const p=BLUEPRINTS[item.id];if(!p)return null;
 const c=new ObjectCanvas(p.w,p.h),active=Boolean(interaction&&!interaction.paused&&interaction.phase==='act');
 const ecology=context.living?.ecology||{},frozen=!p.heated&&p.type!=='mat'&&(ecology.ice||0)>.3;
 const t=motion?time:0,anchors=DRAW[p.type](c,p,t,context,state,active,frozen);
 const pose=interaction&&!interaction.paused&&interaction.phase==='act'?waterPose(interaction.water_routine,motion):null;
 if(pose?.splash>.1&&!frozen){
  const x=anchors.seat.x+pose.u*(anchors.swimRadius||5),y=anchors.seat.y;
  for(const side of [-1,1]){c.put(x+side*(4+pose.splash*7),y-2-pose.splash*5,"'",'c');c.put(x+side*(6+pose.splash*9),y-1-pose.splash*3,'.','w');}
 }
 if(p.type!=='mat'){
  if((state.dirt||0)>.3)c.put(14,p.h-8,':..:','s');
  if((state.condition??1)<.5)c.rows([' /','<',' \\'],p.w-18,p.h-12,'s');
  if(context.season==='fall')c.put(p.w*.64,p.h-14,'<;>','a');
  if((ecology.snow||0)>.1)for(let x=14;x<p.w-12;x+=12)c.put(x,p.h-9,'___','i');
  if(/rain|shower|drizzle/.test(context.weather||''))for(let n=0;n<4;n++){const x=anchors.water.x+6+n*(anchors.water.w-12)/4,y=anchors.water.y+2+(Math.floor(t*4+n)%3);c.put(x,y,Math.floor(t*6+n)%2?'(.)':' . ','c');}
 }
 const inks={b:'#c4baa1',f:'#e3d5b6',s:'#899d8c',k:'#bacdcc',q:'#83b8bd',p:'#d59e91',g:'#86b58a',w:'#91cfd6',c:'#cfebe5',i:'#cee4e9',a:'#dfbd7e'};
 if(p.style==='cedar')Object.assign(inks,{b:'#c89b70',f:'#e0be90',s:'#967752'});
 if(p.style==='inflatable')Object.assign(inks,{a:'#dbb16c',p:'#a9caaa'});
 return {...base,...c.finish(),inks,panels:{b:'#343b31',f:'#405044',s:'#283a31',k:'#253c39',q:'#2a4b4a',p:'#513e32',g:'#263d27',w:frozen?'#3b6568':night(context)?'#163b48':'#204d59',i:'#50767a',a:'#51412a'},
  detail:true,detailScale:.68,construction:'waterworks-v1',blueprint:item.id,anchors,frozen,active,animated:p.type!=='mat',floor:p.type==='mat',lift:0,sway:0};
}
