import {ObjectCanvas} from './object-canvas.mjs';
import {playdatePose} from './playdates.mjs';
export const PLAY_BLUEPRINTS={
 toy_ball:{type:'ball',w:48,h:38,scale:.43,pattern:'panels'},ball:{type:'ball',w:48,h:38,scale:.43,pattern:'stripes'},snowball:{type:'ball',w:44,h:34,scale:.4,pattern:'snow'},
 toy_blocks:{type:'blocks',w:76,h:49,scale:.72},
 toy_trampoline:{type:'trampoline',w:88,h:51,scale:.87,net:true},trampoline:{type:'trampoline',w:74,h:40,scale:.8,net:false},
 toy_slide:{type:'slide',w:100,h:72,scale:.95,style:'wood'},water_slide:{type:'slide',w:108,h:75,scale:.95,style:'pool'},water_slide_mega:{type:'slide',w:116,h:82,scale:1,style:'cascade'},rainbow_slide:{type:'slide',w:110,h:76,scale:.98,style:'rainbow'},
 toy_swing:{type:'swing',w:102,h:75,scale:.95},tire_swing:{type:'tire',w:82,h:75,scale:.9},
 toy_seesaw:{type:'seesaw',w:100,h:43,scale:.9},toy_sandbox:{type:'sandbox',w:96,h:42,scale:.9},
 toy_skateboard:{type:'skateboard',w:70,h:30,scale:.65,style:'fish'},skateboard:{type:'skateboard',w:64,h:29,scale:.6,style:'lightning'},
 toy_car:{type:'car',w:66,h:39,scale:.6},rocking_horse:{type:'horse',w:84,h:62,scale:.82},
 rubber_duck:{type:'duck',w:52,h:38,scale:.5,style:'rubber'},squeaky_toy:{type:'duck',w:48,h:36,scale:.48,style:'squeaker'},
 wind_up_duck:{type:'duck',w:60,h:42,scale:.53,style:'clockwork'},duck_toy:{type:'duck',w:56,h:40,scale:.52,style:'carved'},
 plushie:{type:'plush',w:62,h:48,scale:.6},
};
function wheel(c,x,y,r,turn,tone='k'){
 c.ellipse(x,y,r,r*.55,'=','s',true);c.ellipse(x,y,r-2,Math.max(1,r*.55-1),'-',tone,true);
 c.put(x,y,Math.floor(turn*6)%2?'x':'+','f');for(const sign of [-1,1])c.put(x+sign*r,y,':','k');
}
function ball(c,p,t,active,pose={}){
 const bounce=pose.family==='ball'?-(pose.bally||0):active?Math.abs(Math.sin(t*3.5))*8:0,cy=p.h-15-bounce,rx=17,ry=11-(pose.squash??(active&&bounce<2?2:0)),cx=p.w/2+(pose.ballx||0);
 if(pose.family==='ball')t=pose.spin||0;
 c.ellipse(cx,cy,rx,ry,'_',p.pattern==='snow'?'c':'a',true);
 for(let y=-ry+2;y<ry-1;y++){
  const half=Math.sqrt(1-(y/ry)**2)*(rx-2);
  if(p.pattern==='panels'){
   const seam=cx+Math.sin(y*.2+t*(active?2:0))*8;c.put(seam,cy+y,'|','f');
   if(y===-4||y===5)c.line(cx-half,cy+y,cx+half,cy+y,'-','f');
   if(y%2===0){c.put(seam-2,cy+y,':','q');c.put(seam+2,cy+y,':','q');}
   for(let xx=-half+2;xx<half-1;xx+=5)if(Math.abs(cx+xx-seam)>3)c.put(cx+xx,cy+y,'.','s');
  }
  if(p.pattern==='stripes'&&y%4===0)c.line(cx-half,cy+y,cx+half,cy+y,'~','q');
  if(p.pattern==='snow')for(let x=-half+2;x<half-1;x+=6)c.put(cx+x,cy+y,(Math.round(x+y)%3)?'.':'*','w');
 }
 c.rows([' .---.','(  +  )'," '---'"],cx-4+Math.sin(t)*3,cy-2,'q');
 c.rows([' ..','...'],cx-9,cy-6,'c');c.put(cx+10,cy+5,'(o)','k');
 return {contact:{x:cx+rx,y:cy},top:{x:cx,y:cy-ry}};
}
function blocks(c,p,t,active){
 const lift=active?Math.round(Math.sin(t*3)*3):0;
 const letters={A:[' /\\ ','/  \\','|--|','|  |'],B:['|--.','|__|','|  |',"|__'"],C:[' .--','|   ','|   '," '--"],D:['|--.','|  |','|  |',"|__'"],E:['|---','|__ ','|   ','|___'],F:['|---','|__ ','|   ','|   ']};
 for(const [x,y,w,h,letter,tone]of [[7,29,20,16,'A','a'],[29,29,20,16,'B','w'],[51,29,18,16,'C','q'],[18,14,21,15,'D','q'],[41,14,20,15,'E','a'],[29,3+lift,20,11,'F','w']]){
  c.rect(x,y,w,h,tone,true);c.line(x+2,y+2,x+w-3,y+2,'-','f');c.line(x+w-3,y+2,x+w-3,y+h-3,'|','s');c.rows(letters[letter],x+w/2-2,y+h/2-2,'c');c.put(x+2,y+h-3,'.','f');
  c.line(x+2,y+h-2,x+w-3,y+h-2,'_','s');c.put(x+w-5,y+1,'o','f');
 }
 return {contact:{x:39,y:15+lift},top:{x:39,y:3+lift}};
}
function trampoline(c,p,t,active,pose={}){
 const x=p.w/2,y=p.h-14,dip=pose.dip??(active?Math.max(0,Math.sin(t*4))*4:0);
 for(const sign of [-1,1]){c.line(x+sign*26,y+2,x+sign*29,p.h-3,'|','k');c.line(x+sign*29,p.h-3,x+sign*23,p.h-3,'_','k');}
 c.ellipse(x,y,33,7,'=','f',true);c.ellipse(x,y+dip,27,5,'~','s',true);
 for(let j=-3;j<=3;j++)for(let i=-24;i<=24;i+=3)if((i/26)**2+(j/4)**2<1)c.put(x+i,y+j+dip,(j+i)%2?':':'.','b');
 for(let i=-29;i<30;i+=8)c.put(x+i,y+4,'/\/','k');
 if(p.net){for(const sign of [-1,1]){c.line(x+sign*34,7,x+sign*34,y+2,'|','a');c.put(x+sign*34-1,5,'(o)','a');}c.line(x-34,8,x+34,8,'~','q');for(let xx=x-31;xx<x+33;xx++)for(let yy=10;yy<y-2;yy++)if((xx+yy)%6===0||(xx-yy+90)%6===0)c.put(xx,yy,(xx+yy)%6===0?'/':'\\','q');}
 return {seat:{x,y:y+dip},entry:{x:x+32,y:y+3},spring:{x:x+24,y:y+5}};
}
function slide(c,p,t,active){
 const W=p.w,H=p.h,deckY=19,water=p.style==='pool'||p.style==='cascade',rainbow=p.style==='rainbow';
 c.rect(13,deckY,27,5,'b',true);c.beam(14,deckY+4,14,H-5,3,'b');c.beam(38,deckY+4,38,H-5,3,'b');
 for(const x of [9,27])c.beam(x,deckY+5,x,H-4,3,'k');for(let yy=deckY+7;yy<H-3;yy+=5){c.solid(9,yy,18,1,'k');c.line(9,yy,27,yy,'=','k');}
 c.line(11,deckY+7,11,H-5,'|','s');c.line(25,deckY+7,25,H-5,'|','s');
 c.line(15,H-15,37,deckY+7,'/','b').line(15,deckY+7,37,H-15,'\\','b');
 for(let yy=deckY+9;yy<H-9;yy+=10){c.put(12,yy,'o','f');c.put(24,yy,'o','f');}
 for(const x of [13,39])c.line(x,7,x,deckY,'|','a');c.line(13,7,39,7,'=','a');c.line(13,12,39,12,'-','f');
 const curve=[];for(let i=0;i<=45;i++){const u=i/45,x=37+u*(W-47),y=deckY+3+(H-32)*(u*u*(3-2*u));curve.push([x,y]);}
 for(const [i,[x,y]]of curve.entries()){
  c.solid(x,y,2,7,'s');
  c.line(x,y,x,y+6,'|',rainbow?['a','q','w','g'][Math.floor(i/12)%4]:water?'w':'s');
  c.put(x,y,'_',water?'w':'f');c.put(x,y+6,'_',rainbow?'q':'f');
  if(i%6===0)c.put(x,y+5,'o','k');else if(i%3===0)c.put(x,y+2,'/','c');
  if(water&&i%5===Math.floor(t*7)%5)c.put(x,y+3,'~','c');
 }
 if(p.style==='cascade'){
  c.rect(W-18,8,10,13,'w',true);c.put(W-17,10,'~ ~ ~','c');c.line(W-13,21,W-13,H-21,'|','w');c.line(W-16,22,W-16,H-25,'|','c');
 }
 if(water){c.ellipse(W-28,H-7,23,5,'~','w',true);for(let i=0;i<5;i++)c.put(W-43+i*7,H-7+(i%2),Math.floor(t*4+i)%2?'~~':'--','c');}
 else{c.line(W-23,H-5,W-7,H-5,'_','k');c.put(W-18,H-4,'|___|','s');}
 if(active){const u=(t*.3)%1,[x,y]=curve[Math.round(u*45)];c.put(x,y+2,'*','c');}
 return {entry:{x:18,y:H-4},top:{x:28,y:deckY},seat:{x:40,y:deckY+2},exit:{x:W-13,y:H-9},path:curve};
}
function swing(c,p,t,active){
 const W=p.w,H=p.h,mid=W/2,angle=Math.sin(t*(active?2.4:.8))*(active?14:2),seatY=H-17-Math.abs(angle)*.2;
 if(p.type==='tire'){
  c.rect(9,4,7,H-7,'b',true);for(let y=6;y<H-4;y+=5)c.put(10,y,'|:|','f');c.line(13,9,W-8,5,'=','b');c.line(14,12,W-8,8,'=','f');c.line(mid,8,mid+angle,seatY-9,'|','a');
  c.ellipse(mid+angle,seatY,17,10,'#','s',true);c.ellipse(mid+angle,seatY,9,5,'-','d',true);
  for(const side of [-1,1])for(let yy=-6;yy<=6;yy+=3)c.put(mid+angle+side*14,seatY+yy,'=','k');
 }else{
  for(const x of [12,W-13]){c.beam(x,9,x-7,H-4,3,'b');c.beam(x,9,x+7,H-4,3,'b');c.line(x-5,H-14,x+5,H-14,'-','f');}
  c.rect(7,6,W-14,4,'b',true);for(const x of [12,W-13])c.put(x,7,'o','k');
  for(const sign of [-1,1]){const top=mid+sign*14,bottom=mid+angle+sign*14;c.line(top,10,bottom,seatY,'|','k');for(let y=12;y<seatY;y+=4)c.put(top+(bottom-top)*(y-10)/(seatY-10),y,'o','f');}
  c.rect(mid+angle-17,seatY,34,4,'q',true);c.line(mid+angle-15,seatY+2,mid+angle+14,seatY+2,'-','f');
 }
 return {seat:{x:mid+angle,y:seatY},entry:{x:mid,y:H-4},pivot:{x:mid,y:9}};
}
function seesaw(c,p,t,active,pose={}){
 const cx=p.w/2,cy=23,tilt=pose.tilt??Math.sin(t*(active?2:0))*(active?7:0);
 for(let y=cy+1;y<p.h-3;y++){
  const half=(y-cy)*.53;c.solid(cx-half,y,half*2+1,1,'b');
  c.put(cx-half+1,y,'/','f');c.put(cx+half-1,y,'\\','s');if(y%3===0)c.put(cx-1,y,'|:|','s');
 }
 c.line(cx,cy,cx-9,p.h-3,'/','b').line(cx,cy,cx+9,p.h-3,'\\','b').line(cx-9,p.h-3,cx+9,p.h-3,'=','b');c.put(cx-2,cy,'(o)','k');
 for(let j=0;j<4;j++)c.line(8,cy-tilt+j,p.w-9,cy+tilt+j,'=','a');
 for(let x=13;x<p.w-12;x+=9){const y=cy-tilt+(x-8)/(p.w-17)*tilt*2;c.put(x,y+1,'o','k');c.put(x+2,y+2,'~','s');}
 c.rows(['[--(O)--]',' |:::::|'],cx-4,cy+1,'k');
 const seatTilt=tilt*33/(cx-8);
 for(const sign of [-1,1]){const x=cx+sign*33,y=cy+sign*seatTilt;c.rect(x-7,y-3,14,4,'q',true);c.line(x-5,y-2,x+4,y-2,':','f');c.line(x-sign*7,y-3,x-sign*7,y-10,'|','k');c.put(x-sign*7-3,y-10,'[===]','k');c.put(x-5,y+1,'o','k');c.put(x+4,y+1,'o','k');}
 return {seat:{x:cx-33,y:cy-seatTilt-3},partner:{x:cx+33,y:cy+seatTilt-3},pivot:{x:cx,y:cy}};
}
function sandbox(c,p,t,active,pose={}){
 const W=p.w,H=p.h;c.rect(7,16,W-14,H-20,'b',true);c.line(7,16,16,7,'/','f').line(16,7,W-15,7,'-','f').line(W-15,7,W-8,16,'\\','f');
 for(let y=8;y<17;y++){const left=16-(y-7);c.solid(left,y,W-left*2,1,'v');}
 c.solid(8,17,W-16,H-24,'v');
 for(let y=10;y<H-8;y++)for(let x=17;x<W-16;x+=4)c.put(x,y,(x+y)%3?'.':':','a');
 for(let x=21;x<W-19;x+=14)c.rows([' .__','_.. '],x,10+(x%3),'s');
 c.rect(7,H-8,W-14,4,'b',true);for(let x=10;x<W-9;x+=9)c.put(x,H-7,'o','k');
 if(pose.id==='sandbox_channels'){
  for(const side of [-1,1])for(let n=0;n<Math.round((pose.build||0)*24);n++){
   const x=W/2+side*(24-n),y=23+Math.sin(n*.25)*4;
   c.put(x,y,'.','s');c.put(x,y+1,'~','w');c.put(x,y+2,':','a');
  }
 }else{
  const level=pose.family==='sandbox'?pose.build:1;
  c.ellipse(W/2,27,18,3,'~','a',true);
  const castle=['  |_|_|_|             |_|_|_|','  | . : |             | : . |','  |--.--|             |--.--|','  | : . |_|_|_|_|_|_|_| . : |','  |--.--| . : . : . : |--.--|','  | . : |--.--.--.--.-| : . |','  |--.--|   .-----.   |--.--|','  | : . |  / . . . \\  | . : |','  |--.--| |         | |--.--|','  |_____|_|         |_|____|'];
  const rows=Math.ceil(level*castle.length);c.rows(castle.slice(castle.length-rows),W/2-14,29-rows,'c');
  if(level>.85)c.rows(['|>>','|','|','|'],W/2+7,15,'q');
 }
 c.rows([' .----.','/------\\','|:    :|',' \\____/'],13,H-15,'w');c.rows(['  D','  |','  |',' /_\\'],W-19,H-17,'k');
 if(active)for(let i=0;i<4;i++){
  const origin=pose.family==='sandbox'?(pose.turn==='a'?W*.32:W*.66):W/2,side=pose.turn==='b'?-1:1;
  c.put(origin+side*i*2,19-Math.floor(Math.abs(Math.sin(t*4+i))*4),'.','c');
 }
 return {seat:{x:W/2,y:H-10},entry:{x:W/2,y:H-3},contact:{x:W/2,y:15}};
}
function skateboard(c,p,t,active){
 const W=p.w,y=p.h-12,tilt=active?Math.round(Math.sin(t*3)*2):0;
 c.ellipse(W/2,y,27,6,'=','b',true);c.ellipse(W/2,y-1+tilt,23,4,'~','s',true);
 for(let x=12;x<W-12;x+=4)c.put(x,y-1+tilt,':','f');
 c.put(W/2-5,y-1+tilt,p.style==='fish'?'><((o)>':'/\/\/','a');
 c.line(17,y+5,W-18,y+5,'=','k');for(const x of [18,W-19])wheel(c,x,y+7,5,active?t:0);
 return {seat:{x:W/2,y:y-3+tilt},entry:{x:W/2,y:y+8}};
}
function car(c,p,t,active){
 const y=p.h-13;c.rect(9,y-8,p.w-18,12,'a',true);c.rect(22,y-19,25,12,'q',true);c.rect(25,y-17,9,8,'w',true);c.rect(36,y-17,8,8,'w',true);
 c.line(7,y-3,p.w-8,y-3,'=','f');c.put(11,y,'[o]','c');c.put(p.w-15,y,'[=]','q');c.put(38,y-6,'--','k');
 for(const x of [19,p.w-20])wheel(c,x,y+5,8,active?t:0);
 c.line(p.w-9,y-10,p.w-3,y-10,'-','k');c.put(p.w-7,y-13,active&&Math.floor(t*5)%2?'|':'(o)','k');
 return {contact:{x:p.w-5,y:y-11},top:{x:34,y:y-20}};
}
function horse(c,p,t,active){
 const rock=active?Math.round(Math.sin(t*2.5)*2):0;
 c.ellipse(37,35+rock,23,9,'~','b',true);
 for(let y=19;y<=36;y++){const x=51-Math.max(0,y-27)*.5;c.solid(x,y+rock,10,1,'b');c.put(x,y+rock,'|','f');c.put(x+9,y+rock,'|','s');}
 c.rows(['   /\\     /\\','  / .\\___/ .\\',' / .         \\','( O   ______  \\',' \\  / . . .)__)','  |: |----\'','  |: |','  |: |'],49,7+rock,'b',true);c.put(51,10+rock,'O','e');
 for(let y=15;y<31;y+=2)c.put(48,y+rock,'///','q');
 for(let yy=32;yy<40;yy+=3)for(let xx=19;xx<49;xx+=10)c.put(xx,yy+rock,'(~)','s');
 c.rows(['.------------.','| :  .  .  : |',"'------------'"],26,27+rock,'q');c.line(64,18+rock,39,33+rock,'~','a');c.put(60,17+rock,'(o)','k');
 for(const x of [22,48]){c.line(x,39+rock,x-3,51+rock,'/','b');c.put(x-5,51+rock,'[___]','k');}
 c.rows(['\\\\',' \\\\','  \\'],12,31+rock,'q');for(let x=9;x<70;x++)c.put(x,56-Math.abs(x-39)*.08,'_','f');c.put(7,53,'\\_','f');c.put(69,53,'_/','f');
 return {seat:{x:35,y:27+rock},entry:{x:29,y:54},contact:{x:57,y:25+rock}};
}
function duck(c,p,t,active){
 const W=p.w,H=p.h,squeeze=active&&p.style==='squeaker'?Math.round(Math.sin(t*4)*2):0;
 c.ellipse(W/2,H-14+squeeze,18,9,'~','a',true);c.ellipse(W/2+8,H-27+squeeze,10,7,'_', 'a',true);
 c.rows(['_______','\\_____>'],W/2+14,H-27+squeeze,'q');c.put(W/2+10,H-29+squeeze,'O','e');c.ellipse(W/2-1,H-13+squeeze,10,5,'~','f');
 c.put(5,H-14+squeeze,'<','a');c.line(10,H-7,W-12,H-7,'_','s');
 for(let x=12;x<W-13;x+=4)c.put(x,H-9+squeeze,"'",'s');
 c.rows([' .--.','/ .  \\',"'----'"],W/2-9,H-18+squeeze,'f');
 c.put(W/2+6,H-32+squeeze,'..','c');c.put(W/2+10,H-29+squeeze,'O','e');
 if(p.style==='clockwork'){c.line(5,H-20,15,H-20,'=','k');c.rows(active&&Math.floor(t*5)%2?[' (o)','  |',' (o)']:['(o)-(o)'],2,H-22,'k');wheel(c,22,H-6,5,t);wheel(c,43,H-6,5,t);}
 if(p.style==='carved'){for(let x=16;x<W-15;x+=7)c.put(x,H-17,'(=)','s');wheel(c,19,H-5,5,active?t:0);wheel(c,38,H-5,5,active?t:0);c.put(W-14,H-16,'o','k');}
 if(active&&p.style==='rubber')c.put(W-6,H-34,Math.floor(t*4)%2?'!':'.','c');
 return {contact:{x:W/2,y:H-15},top:{x:W/2+8,y:H-34}};
}
function plush(c,p,t,active){
 const dy=active?Math.round(Math.sin(t*2)*2):0;
 c.ellipse(18,10+dy,6,4,'~','b',true);c.ellipse(43,10+dy,6,4,'~','b',true);c.ellipse(31,20+dy,18,12,'~','b',true);
 c.ellipse(31,35,17,10,'~','q',true);c.ellipse(17,41,9,4,'~','b',true);c.ellipse(46,41,9,4,'~','b',true);
 c.put(23,18+dy,'x','e');c.put(38,18+dy,'o','e');c.put(28,24+dy,'(v)','a');c.put(27,27+dy,"'---'",'f');
 c.line(31,30,31,42,':','f');c.put(23,33,'[X]','a');c.rows(['\\   /',' >o<','/   \\'],27,29,'a');
 c.ellipse(31,35,10,6,':','f');for(let y=14;y<26;y+=3){c.put(18,y+dy,'x','f');c.put(44,y+dy,'x','f');}c.rows([' .---.',' | + |'," '---'"],34,33,'w');
 c.ellipse(9,31+dy,5,7,'~','b',true);c.ellipse(53,31-dy,5,7,'~','b',true);
 return {contact:{x:31,y:30},hug:{x:31,y:24+dy}};
}
const DRAW={ball,blocks,trampoline,slide,swing,tire:swing,seesaw,sandbox,skateboard,car,horse,duck,plush};
export function playgroundSprite(base,item,time,{motion=true,state={},interaction=null,context={},pose={}}={}){
 let p=PLAY_BLUEPRINTS[item.id];if(!p)return null;
 const company=playdatePose(interaction,motion);if(company)pose=company;
 if(p.type==='sandbox'&&!company)pose={id:state.sandwork||'sandbox_castle',family:'sandbox',build:state.sandwork?1:0};
 if(company?.family==='ball')p={...p,w:116};
 const c=new ObjectCanvas(p.w,p.h);
 const active=Boolean(interaction&&!interaction.paused&&['prepare','act','settle'].includes(interaction.phase||'act'));
 const t=motion?(active?(interaction.elapsed??time):time):0;
 const anchors=DRAW[p.type](c,p,t,active,pose);
 if((state.wetness||0)>.2)for(let i=0;i<5;i++)c.put(6+i*(p.w-12)/5,p.h-4-(i%2),Math.floor(t*6+i)%2?"'":'.','w');
 if((state.dirt||0)>.3)c.put(9,p.h-5,':. .:','s');
 if((state.condition??1)<.5)c.rows([' /','<',' \\'],p.w-12,p.h-13,'s');
 if((state.bond||0)>.6)c.put(p.w/2-1,p.h-3,'<3','a');
 if(context.season==='winter'&&['slide','swing','tire','seesaw','trampoline','sandbox'].includes(p.type))for(let x=9;x<p.w-8;x+=9)c.put(x,p.type==='sandbox'?8:5,'_','c');
 const inks={b:base.body,f:base.face,s:'#82948a',a:base.accent,q:'#bb8c8e',w:'#8ac1cf',k:'#b2bab2',c:'#e8e5d4',d:'#152d28',g:'#91b491',e:'#122923'};
 if(['slide','swing','tire','trampoline','seesaw'].includes(p.type))Object.assign(inks,{b:'#c7ad83',f:'#e1d2ae',k:'#d0d5c7',s:'#a4b8b3',w:'#a9dbe0'});
 if(p.type==='horse')Object.assign(inks,{b:'#caa278',f:'#e2c8a0',s:'#9d805e',q:'#99bba5',a:'#e2bc78'});
 if(p.type==='ball')Object.assign(inks,{a:p.pattern==='snow'?'#d8e5dd':'#dbaa6b',f:'#f3d8a5',q:'#8ec7bd',s:'#bf9e6f',k:'#e5c985'});
 if(p.type==='sandbox')Object.assign(inks,{b:'#bc976d',f:'#dfbe86',a:'#cfb37c',s:'#9b8969',v:'#e5c688',c:'#f1d6a1',q:'#d7907b',w:'#88bfc9'});
 if(p.type==='duck')Object.assign(inks,{a:'#e6c273',q:'#d89b6b',f:'#f0dcaa',s:'#a28a60',b:'#c5ab78'});
 if(p.type==='plush')Object.assign(inks,{b:'#bca48e',q:'#ab9a86',f:'#dfcba8',a:'#bf9091'});
 return {...base,...c.finish(),inks,panels:{b:'#3e3527',f:'#3a4937',a:'#51482e',q:'#453039',w:'#26474c',s:'#24342f',k:'#293d3a',c:'#729b9c',d:'#142c27',v:'#53452e'},detail:true,detailScale:.72,animated:true,active,lift:0,sway:0,construction:'playground-v1',anchors,blueprint:item.id};
}
