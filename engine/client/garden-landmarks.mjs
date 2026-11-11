// Authored landmark anatomy. Motion comes from native saved weather/controls.
const clamp=n=>Math.max(0,Math.min(1,n||0));
function slab(c,x,y,w,h,t='s'){
 c.rect(x,y,w,h,t,true);c.line(x+2,y+2,x+w-3,y+2,'_','f');c.line(x+2,y+h-3,x+w-3,y+h-3,':','k');
 for(let xx=x+5;xx<x+w-4;xx+=11){c.put(xx,y+Math.min(h-4,5),'.','a');if(h>9)c.put(xx+3,y+h-5,"'",'k');}
}
function stitch(c,x,y,w,h,t='q'){
 c.rect(x,y,w,h,t,true);for(let yy=y+2;yy<y+h-1;yy+=3){c.put(x+1,yy,'x','f');c.put(x+w-2,yy,'x','f');}for(let xx=x+3;xx<x+w-2;xx+=4){c.put(xx,y+1,'x','f');c.put(xx,y+h-2,'x','f');}
}
function gnome(c,p){
 const H=p.h,cx=p.w/2;
 for(const x of [cx-28,cx+4]){c.ellipse(x+13,H-12,17,8,'_','i',true);c.line(x+1,H-9,x+26,H-9,'=','k');c.rows([' /\\','/  \\'],x+3,H-20,'a');}
 c.ellipse(cx,H-42,29,29,'_','q',true);c.rect(cx-23,H-58,46,35,'q',true);c.line(cx,H-55,cx,H-19,'|','a');
 for(const yy of [H-52,H-41,H-30])c.put(cx-2,yy,'(o)','a');stitch(c,cx-23,H-38,13,11,'r');stitch(c,cx+11,H-38,13,11,'r');
 for(let y=H-54;y<H-22;y+=5)for(const side of [-1,1])c.put(cx+side*18,y,'v','f');
 for(const x of [cx-30,cx+23]){c.ellipse(x,H-46,7,15,'_','q',true);c.ellipse(x,H-32,6,5,'o','a',true);}
 c.ellipse(cx,H-83,23,21,'_','a',true);
 for(const x of [cx-12,cx+12]){c.ellipse(x,H-84,5,4,'_','f',true);c.ellipse(x+1,H-84,2,3,'o','k',true);c.put(x,H-86,'.','f');c.line(x-4,H-91,x+3,H-92,'_','r');}
 c.put(cx-20,H-77,'::','q');c.put(cx+17,H-77,'::','q');c.ellipse(cx,H-76,7,6,'o','r',true);
 for(let row=0;row<28;row++){const half=22*(1-row/32);c.solid(cx-half,H-71+row,half*2+1,1,'f');for(let x=cx-half+2;x<cx+half-1;x+=5)c.put(x,H-71+row,row%3?'|':':','s');}
 for(let row=0;row<36;row++){const half=4+row*.62;c.solid(cx-half+Math.sin(row*.08)*5,H-137+row,half*2+1,1,'q');c.put(cx-half,H-137+row,'/','r');c.put(cx+half,H-137+row,'\\','f');if(row%4===0){c.put(cx+row*.15,H-137+row,'x','a');c.put(cx-half+4,H-137+row,':','f');}}
 c.ellipse(cx,H-100,29,5,'_','q',true);c.line(cx-25,H-99,cx+25,H-99,'=','r');c.put(cx-8,H-121,'*  +','f');
 return {contact:{x:cx-21,y:H-11},company:{x:cx+26,y:H-10}};
}
function statue(c,p){
 const H=p.h,cx=p.w*.53;
 slab(c,19,H-27,p.w-38,23);slab(c,14,H-32,p.w-28,7,'i');c.rect(cx-24,H-20,49,12,'i',true);c.put(cx-20,H-14,'KEEP IT QUACK','a');
 c.ellipse(cx,H-57,40,24,'_','i',true);c.ellipse(cx-12,H-63,26,14,':','l');
 for(let row=0;row<5;row++)for(let col=0;col<7-row;col++)c.put(cx-36+col*8+row*3,H-65+row*4,'\\v/','a');
 for(let y=H-75;y<H-43;y+=7)c.line(cx-29,y,cx-36,y+5,'/','f');
 c.beam(cx+21,H-73,cx+23,H-91,14,'i');c.ellipse(cx+23,H-98,18,16,'_','i',true);c.ellipse(cx+28,H-101,3,3,'o','k',true);c.put(cx+27,H-102,'.','f');
 c.ellipse(cx+43,H-97,13,5,'_','a',true);c.line(cx+34,H-96,cx+55,H-96,'=','r');c.put(cx+43,H-100,'o','k');c.rows([' /|','/ |','--+'],cx-48,H-63,'i');
 for(const x of [cx-7,cx+14]){c.beam(x,H-36,x,H-30,3,'a');c.put(x-4,H-30,'/___\\','a');}
 for(const [x,y]of [[cx-24,H-48],[cx+15,H-80],[cx+18,H-108]])c.put(x,y,';::;','l');
 return {contact:{x:cx-18,y:H-13},company:{x:cx+31,y:H-9}};
}
function scarecrow(c,p,s){
 const H=p.h,cx=p.w/2,sway=Math.sin(s.phase||0)*(s.wind||0)*4;
 c.beam(cx,H-12,cx,39,5,'b');c.beam(26,70,p.w-26,70,4,'b');c.line(cx-4,H-6,cx+12,H-6,'_','k');
 for(const side of [-1,1]){const x=cx+side*24;c.rect(x-10,H-62,18,42,'i',true);stitch(c,x-8,H-48,14,15,'q');for(let n=0;n<7;n++)c.line(x-8+n*3,H-22,x-13+n*4,H-8-(n%2)*4,null,'a');}
 c.rect(cx-28,65,56,45,'r',true);for(let y=69;y<106;y+=7){c.line(cx-25,y,cx+25,y,':','q');c.line(cx-25,y+1,cx+25,y+1,'-','a');}for(let x=cx-24;x<cx+25;x+=10)c.line(x,68,x,107,'|','b');
 c.line(cx,67,cx,108,'|','a');for(let y=73;y<107;y+=11)c.put(cx-2,y,'(+)','a');stitch(c,cx+9,79,16,17,'q');
 for(const side of [-1,1]){const x=cx+side*36;c.rect(x-16,66,32,14,'r',true);c.line(x-13,70,x+13,70,':','q');for(let n=0;n<6;n++)c.line(cx+side*55,68+n*2,cx+side*(67+n%2*4),64+n*3,null,'a');}
 c.ellipse(cx,45,23,21,'_','a',true);for(const x of [cx-9,cx+9]){c.ellipse(x,42,4,3,'o','k',true);c.put(x-1,42,'x','f');c.line(x-3,36,x+3,35,'_','r');}c.line(cx-12,52,cx+12,54,'_','k');for(let x=cx-10;x<cx+12;x+=4)c.put(x,53,'|','b');c.rows([' /\\','/  \\','----'],cx-2,43,'r');
 for(const side of [-1,1])for(let y=38;y<58;y+=4)c.put(cx+side*18,y,'x','f');
 c.ellipse(cx,24,34,5,'_','b',true);c.rect(cx-19,8,38,17,'b',true);for(let y=10;y<24;y+=4)c.line(cx-16,y,cx+16,y,':','a');stitch(c,cx+4,10,11,10,'q');
 c.rect(cx-24,61,48,7,'q',true);for(let y=68;y<99;y++){const x=cx+19+Math.sin(y*.15+(s.phase||0))*sway;c.solid(x,y,9,1,'q');if(y%4===0)c.put(x+2,y,'+','f');}
 return {contact:{x:cx-25,y:H-10},company:{x:cx+25,y:H-10}};
}
function totem(c,p){
 const H=p.h,cx=p.w/2;slab(c,22,H-13,p.w-44,10,'b');c.rect(cx-25,12,50,H-25,'b',true);
 for(let x=cx-23;x<cx+24;x+=7)for(let y=15;y<H-16;y+=13){c.line(x,y,x+Math.sin(y)*2,y+9,':','s');c.line(x+2,y,x+2+Math.sin(y)*2,y+9,'|','a');}
 for(const [n,y]of [H-44,H-94,H-145].entries()){
  c.ellipse(cx,y,29,22,'_','a',true);c.ellipse(cx,y,25,18,':','b',true);
  if(n===0){for(const x of [cx-16,cx+16]){c.ellipse(x,y-10,8,7,'o','l',true);c.put(x-2,y-11,'(o)','k');}c.line(cx-17,y+7,cx+17,y+7,'_','a');c.put(cx-12,y+10,'/ V V V \\','s');}
  if(n===1){for(const x of [cx-11,cx+11])c.put(x-2,y-4,'(o)','f');c.rows(['  __________',' /==========>',' \\_________/'],cx-11,y+2,'a',true);for(let x=cx-18;x<cx+19;x+=6)c.put(x,y+14,'v','s');}
  if(n===2){for(const x of [cx-12,cx+12]){c.ellipse(x,y-3,10,9,'o','f');c.put(x-2,y-3,'(@)','k');}c.rows([' /\\',' \\/'],cx-1,y+6,'a');c.rows(['/\\      /\\','  \\____/'],cx-21,y-24,'b');}
  for(let x=cx-16;x<cx+20;x+=7)c.put(x,y+17,'V','a');
  for(const side of [-1,1])for(let j=0;j<3;j++)c.line(cx+side*30,y-7+j*5,cx+side*(43-j*4),y-1+j*5,null,'a');
 }
 c.put(cx-19,H-19,'POND / ROOT / SKY','f');c.put(cx-22,H-9,'(o)  .:::.  (o)','a');
 return {contact:{x:cx-21,y:H-13},company:{x:cx+23,y:H-9}};
}
function sundial(c,p,s){
 const H=p.h,cx=p.w/2,cy=H-29;slab(c,26,H-20,p.w-52,17);c.ellipse(cx,cy+5,66,21,'_','s',true);c.ellipse(cx,cy,68,22,'_','a',true);c.ellipse(cx,cy,60,18,':','i');
 for(let n=0;n<24;n++){const a=n*Math.PI/12;c.line(cx+Math.cos(a)*52,cy+Math.sin(a)*15,cx+Math.cos(a)*60,cy+Math.sin(a)*18,null,'k');}
 for(const [label,x,y]of [['VI',cx-54,cy],['IX',cx-36,cy-12],['XII',cx-4,cy-17],['III',cx+32,cy-12],['VI',cx+51,cy]])c.put(x,y,label,'f');
 c.put(cx-20,cy+13,'TEMPUS / QUACK','k');
 for(let n=0;n<18;n++){const a=n*Math.PI/9;c.put(cx+Math.cos(a)*44,cy+Math.sin(a)*12,'+','f');}
 if(s.sun>.1){const a=s.shadow_angle||0,L=46*(s.shadow_length||.7),tip={x:cx+Math.sin(a)*L,y:cy-Math.cos(a)*L*.32};c.beam(cx,cy,tip.x,tip.y,3,'k');c.line(cx,cy,tip.x,tip.y,':','s');}
 for(let y=0;y<22;y++)c.line(cx-2,cy-y,cx+Math.max(0,14-y*.65),cy,'/','b');c.line(cx-2,cy-22,cx-2,cy,'|','f');c.put(cx-3,cy,'[=]','a');
 return {contact:{x:cx-25,y:H-12},company:{x:cx+31,y:H-10},entry:{x:cx-53,y:H-3}};
}
function vane(c,p,s){
 const H=p.h,cx=p.w/2,a=s.bearing||0,dx=Math.cos(a)*48,dy=Math.sin(a)*9;
 slab(c,cx-21,H-14,42,11,'s');c.beam(cx,H-15,cx,32,4,'i');c.line(cx-1,40,cx-1,H-19,':','a');
 c.line(cx-38,65,cx+38,65,'=','i');c.line(cx-22,77,cx+22,53,'/','i');for(const [x,y,t]of [[cx-43,65,'W'],[cx+40,65,'E'],[cx+24,50,'N'],[cx-27,78,'S']])c.put(x,y,t,'f');
 c.beam(cx-dx,35-dy,cx+dx,35+dy,2,'a');c.put(cx+dx-1,35+dy,Math.cos(a)>0?'>':'<','f');c.ellipse(cx-dx,35-dy,8,6,'_','i');c.line(cx-dx-5,35-dy-4,cx-dx+5,35-dy+4,'/','l');
 c.ellipse(cx,25,17,8,'_','i',true);c.ellipse(cx+10,15,7,6,'_','a',true);c.put(cx+11,14,'o','k');c.put(cx+16,17,'==>','f');c.rows([' /|','/ |','--+'],cx-22,25,'i');c.put(cx-4,34,'/___\\','a');c.ellipse(cx,39,6,3,'o','i',true);
 for(const x of [cx-13,cx+13])c.put(x-2,H-9,'(+)','f');
 return {contact:{x:cx-13,y:H-9},company:{x:cx+13,y:H-9}};
}
function compass(c,p){
 const H=p.h,cx=p.w/2,cy=H-35;c.ellipse(cx,cy+3,74,29,'_','s',true);c.ellipse(cx,cy,73,28,'_','i',true);c.ellipse(cx,cy,66,24,':','a');
 for(let i=0;i<16;i++){const a=i*Math.PI/8,rx=i%2?43:57,ry=i%2?15:21,x=cx+Math.sin(a)*rx,y=cy-Math.cos(a)*ry;c.line(cx,cy,x,y,null,i%2?'s':'f');c.line(cx+Math.cos(a)*6,cy+Math.sin(a)*3,x,y,null,i%2?'b':'a');}
 for(let n=0;n<24;n++){const a=n*Math.PI/12;c.put(cx+Math.cos(a)*70,cy+Math.sin(a)*26,'+','k');}
 for(let n=0;n<32;n++){const a=n*Math.PI/16;c.put(cx+Math.cos(a)*63,cy+Math.sin(a)*22,'[]',n%2?'s':'a');}
 for(const [text,x,y]of [['N',cx-1,cy-25],['S',cx-1,cy+24],['W',cx-66,cy],['E',cx+64,cy]])c.put(x,y,text,'f');c.ellipse(cx,cy,8,4,'o','b',true);c.put(cx-3,cy,'(o)>','a');
 return {contact:{x:cx-30,y:H-12},company:{x:cx+38,y:H-10},entry:{x:cx-55,y:H-3}};
}
function flag(c,p,s){
 const H=p.h,mast=38,hoist=clamp(s.flag),fy=H-53-hoist*(H-72),phase=s.phase||0;
 slab(c,mast-18,H-15,38,12,'s');c.beam(mast,12,mast,H-16,4,'i');c.line(mast-1,15,mast-1,H-16,'|','f');c.ellipse(mast,9,6,5,'o','a',true);
 c.line(mast+7,16,mast+7,H-12,':','a');c.line(mast+10,16,mast+10,H-12,':','s');c.put(mast+5,H-11,'[===]','f');
 const cols=68,rows=34;
 for(let x=0;x<cols;x++){const offset=Math.sin(x*.12-phase)*(s.wind||0)*5;for(let y=0;y<rows;y++){const yy=fy+y+offset;c.put(mast+10+x,yy,y===0||y===rows-1?'_':x===cols-1?'|':(x+y)%7===0?':':' ',y===0?'f':'w');if(y>0&&y<rows-1)c.solid(mast+10+x,yy,1,1,'w');}
  if(x%4===0){c.put(mast+10+x,fy+2+offset,'+','a');c.put(mast+10+x,fy+rows-3+offset,'+','a');}}
 const wave=Math.sin(35*.12-phase)*(s.wind||0)*5;c.rows(['      __','     (o)>',' ___ / _)',' \\~~~~/','  \\__/'],mast+33,fy+10+wave,'f');c.put(mast+16,fy+27,'P O N D   P R I D E','a');
 for(const y of [fy+3,fy+rows-4]){c.put(mast+5,y,'(o)','a');c.line(mast+8,y,mast+12,y,'-','i');}
 return {contact:{x:mast+8,y:H-11},company:{x:mast-10,y:H-9},entry:{x:mast-15,y:H-3}};
}
export const LANDMARK_BUILDERS={gnome,statue,scarecrow,totem,sundial,vane,compass,flag};
// Material-specific ink and quiet underpaint keep the cut glyphs legible in
// daylight without bleaching the world or making every ornament the same color.
export const LANDMARK_COLORS={
 gnome:{inks:{q:'#ffb5a8',r:'#e7b884',a:'#f5d6a4',f:'#fff1c8',i:'#99c8b1'},panels:{q:'#8d3833',r:'#6f4934',a:'#a07d54',f:'#917f5b',i:'#244c42'}},
 statue:{inks:{i:'#8cdbc4',a:'#edc88c',f:'#dcf0cd',l:'#84b5a0',s:'#c0c2ab'},panels:{i:'#245344',a:'#896d3a',l:'#376f5a',s:'#36463d'}},
 scarecrow:{inks:{q:'#f4b46a',a:'#f0d395',f:'#fff0c2',b:'#d3ac77',r:'#efbcb2',i:'#9fc6ca'},panels:{q:'#9e502c',a:'#8b7448',b:'#493721',r:'#62463a',i:'#2e5360'}},
 totem:{inks:{b:'#b88d5c',a:'#efd3a1',f:'#ffe8b9',s:'#d0a870',l:'#85d9a2'},panels:{b:'#3b3024',a:'#6f5232',l:'#315d3e'}},
 sundial:{inks:{a:'#ead2a3',i:'#acc7b6',s:'#c0ccba',f:'#fff0cc'},panels:{a:'#64543d',s:'#3e4c43'}},
 vane:{inks:{i:'#8bcab5',a:'#eac488',f:'#e9eac3',l:'#76b598'},panels:{i:'#2f594d',a:'#7b5b30'}},
 compass:{inks:{i:'#a6d1bf',a:'#edbe7a',f:'#f5e0ad',s:'#c3c9ae'},panels:{i:'#294b45',s:'#43574b',b:'#735a36'}},
 flag:{inks:{w:'#94cfda',a:'#e9c789',f:'#fff0b8',i:'#a4c3ae'},panels:{w:'#285f76',i:'#345b4f',s:'#435249'}}
};
