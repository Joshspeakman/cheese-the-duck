import {ObjectCanvas} from './object-canvas.mjs';
import BLUEPRINTS from './animation/creative-props.json' with {type:'json'};
export {BLUEPRINTS as CREATIVE_BLUEPRINTS};
const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
function polygon(c,points,tone){
 const ys=points.map(p=>p[1]);
 for(let y=Math.ceil(Math.min(...ys));y<=Math.floor(Math.max(...ys));y++){
  const cuts=[];
  for(let i=0;i<points.length;i++){
   const a=points[i],b=points[(i+1)%points.length];
   if(a[1]!==b[1]&&y>=Math.min(a[1],b[1])&&y<Math.max(a[1],b[1]))cuts.push(a[0]+(y-a[1])/(b[1]-a[1])*(b[0]-a[0]));
  }
  cuts.sort((a,b)=>a-b);for(let i=0;i+1<cuts.length;i+=2){const x=Math.ceil(cuts[i]),w=Math.max(1,Math.floor(cuts[i+1])-x+1);c.clear(x,y,w,1);c.solid(x,y,w,1,tone);}
 }
 for(let i=0;i<points.length;i++){const a=points[i],b=points[(i+1)%points.length];c.line(...a,...b,null,'f');}
}
function timber(c,x0,y0,x1,y1,w=5){
 c.beam(x0,y0,x1,y1,w,'b');c.line(x0,y0,x1,y1,':','s');
 c.put(x0-1,y0+2,'(o)','a');c.put(x1-1,y1-2,'(o)','a');
}
function scope(c,p,v){
 const H=p.h,cx=71,cy=49,angle=-.08-clamp(v.aim)*.5,co=Math.cos(angle),si=Math.sin(angle);
 const point=(u,w=0)=>[cx+co*u-si*w,cy+si*u+co*w];
 // Surveyor tripod: spread feet, sliding braces, toothed altitude circle.
 timber(c,cx,66,cx-35,H-8,6);timber(c,cx+1,66,cx+34,H-8,6);timber(c,cx,67,cx+3,H-5,4);
 c.line(cx-24,H-23,cx+25,H-23,'_','a');c.line(cx,H-46,cx-24,H-23,'/','k');c.line(cx,H-46,cx+25,H-23,'\\','k');
 for(const x of [cx-35,cx+34,cx+3])c.put(x-4,H-5,'[_______]','k');
 c.ellipse(cx,cy+11,10,10,'o','a',true);c.ellipse(cx,cy+11,7,7,':','k',true);c.put(cx-2,cy+11,'(+)','f');
 for(let i=0;i<12;i++){const a=i*Math.PI/6;c.put(cx+Math.cos(a)*8,cy+11+Math.sin(a)*8,'+','b');}
 c.beam(cx,cy+11,cx+18,cy+19,3,'a');c.put(cx+15,cy+20,'[===]','k');
 polygon(c,[point(-36,-6),point(39,-6),point(39,6),point(-36,6)],'a');
 for(const w of [-4,0,4])c.line(...point(-32,w),...point(35,w),w===0?':':'_','s');
 for(const u of [-20,13,31]){polygon(c,[point(u-2,-8),point(u+2,-8),point(u+2,8),point(u-2,8)],'b');c.put(...point(u,0),'o','f');}
 const focus=-38-clamp(v.focus)*7;
 polygon(c,[point(focus-10,-3),point(-34,-3),point(-34,3),point(focus-10,3)],'k');
 c.line(...point(focus-10,-4),...point(focus-10,4),'|','f');
 c.ellipse(...point(-28,10),4,4,'o','a',true);c.put(...point(-30,10),v.focus>.5?'[|]':'[-]','k');
 polygon(c,[point(37,-10),point(44,-10),point(44,10),point(37,10)],'k');
 c.line(...point(42,-8),...point(42,8),'|',v.cap>.5?'b':'w');
 if(v.cap<.5){for(let n=-6;n<=6;n+=3)c.put(...point(42,n),n<0?'/':'.','w');}
 c.line(...point(-10,-11),...point(16,-11),'=','k');c.put(...point(-10,-12),'[o]','w');
 c.put(cx-23,H-17,'N  .  E  .  S  .  W','a');
 const eye=point(focus-10,0),knob=point(-28,10);
 return {entry:{x:cx,y:H-3},contact:{x:knob[0],y:knob[1]},eye:{x:eye[0],y:eye[1]},aim:{x:cx+18,y:cy+19},lens:{x:point(42)[0],y:point(42)[1]}};
}
function painting(c,x,y,w,h,progress,motif){
 const n=Math.floor(clamp(progress)*12),night=motif==='night',winter=motif==='winter',autumn=motif==='autumn';
 if(n>=1)for(let yy=0;yy<h*.5;yy++)c.solid(x,y+yy,w,1,night?'n':'g');
 if(n>=2)for(let yy=Math.floor(h*.5);yy<h;yy++)c.solid(x,y+yy,w,1,winter?'p':autumn?'b':'l');
 if(n>=3)c.ellipse(x+w*.7,y+10,6,5,night?'o':'*',night?'p':'a',true);
 if(n>=4)for(let xx=0;xx<w;xx++)c.put(x+xx,y+h*.5+Math.sin(xx*.17)*2,'^','k');
 if(n>=5)for(let yy=h*.63;yy<h-3;yy++)c.solid(x+4,y+yy,w-9,1,'w');
 if(n>=6)for(let yy=h*.65;yy<h-3;yy+=3)c.line(x+5,y+yy,x+w-7,y+yy,'~','g');
 if(n>=7)for(const xx of [x+8,x+w-12]){c.line(xx,y+h*.65,xx,y+13,'|','b');c.rows(['  /\\',' /||\\','//||\\\\'],xx-3,y+9,'l');}
 if(n>=8)c.rows(['  _',' (o)=',' /_)',' ~~~'],x+w*.36,y+h*.68,'a');
 if(n>=9)c.rows(['  _',' (o)=',' /_)',' ~~~'],x+w*.62,y+h*.65,'q');
 if(n>=10){if(winter)for(let i=0;i<16;i++)c.put(x+3+i*3,y+2+(i*7%25),'*','p');else for(let i=0;i<10;i++)c.put(x+3+i*4,y+3+i%7,night?'+':'.','p');}
 if(n>=11)c.put(x+6,y+h-5,'~ ~  ~ ~  ~ ~','g');
 if(n>=12)c.put(x+w-20,y+h-2,'C. / QUACK','d');
}
function easel(c,p,v,s){
 const H=p.h,x=24,y=17,w=73,h=63;
 timber(c,60,8,60,H-8,6);timber(c,42,68,23,H-5,6);timber(c,79,68,98,H-5,6);timber(c,62,35,107,H-12,4);
 c.clear(x-3,y-3,w+6,h+6);c.rect(x-3,y-3,w+6,h+6,'b',true);c.rect(x,y,w,h,'p',true);
 for(let yy=y+3;yy<y+h-2;yy+=4)for(let xx=x+3;xx<x+w-2;xx+=6)c.put(xx,yy,':','s');
 painting(c,x+4,y+4,w-8,h-8,(s.creative?.strokes||0)/12,s.creative?.motif||'pond');
 if(v.cover>.01){const height=Math.max(1,Math.round(h*clamp(v.cover)));c.clear(x,y,w,height);c.rect(x,y,w,height,'k',true);for(let yy=y+3;yy<y+height-2;yy+=4)c.line(x+2,yy,x+w-3,yy,':','s');c.put(x+15,y+Math.max(1,height-3),'KEEP THE GOOD BITS DRY','a');}
 c.rect(x-5,y+h+4,w+10,5,'a',true);c.line(x-3,y+h+5,x+w+2,y+h+5,'_','f');
 c.rows([' _|_|_','[=====]'],58,y-6,'a');c.ellipse(67,y+h+11,4,3,'o','k',true);c.put(65,y+h+11,'(+)','a');
 c.ellipse(101,H-16,16,8,'_','b',true);c.ellipse(109,H-18,3,2,'o','k',true);
 for(const [dx,dy,t] of [[-10,-1,'q'],[-4,-4,'w'],[3,-4,'a'],[-7,4,'l'],[2,4,'p']])c.ellipse(101+dx,H-16+dy,2,1,'o',t,true);
 c.rect(5,H-19,12,15,'g',true);c.line(7,H-15,15,H-15,'~','w');
 for(const xx of [8,12,16]){c.line(xx,H-19,xx-2,H-33,'/','b');c.put(xx-3,H-34,'#','a');}
 for(const xx of [20,94])c.put(xx,H-3,'[______]','k');
 return {entry:{x:60,y:H-2},contact:{x:45,y:48},canvas:{x:x+7+clamp(v.stroke)*55,y:y+20+Math.sin(clamp(v.stroke)*Math.PI*3)*14},palette:{x:94,y:H-17},rinse:{x:10,y:H-17},clamp:{x:61,y:y-5}};
}
function kite(c,p,v){
 const flight=clamp(v.flight),wind=clamp(v.wind||0),clock=v.seconds||0,cx=75+Math.sin(clock*.8)*wind*5,cy=78-flight*48,rx=27,ry=22;
 // Four stitched panels, exposed bamboo spars and a separate balancing tail.
 const top=[cx,cy-ry],left=[cx-rx,cy],right=[cx+rx,cy],bottom=[cx,cy+ry];
 polygon(c,[top,left,[cx,cy]],'q');polygon(c,[top,right,[cx,cy]],'w');polygon(c,[bottom,left,[cx,cy]],'a');polygon(c,[bottom,right,[cx,cy]],'l');
 for(let yy=-ry+3;yy<ry-2;yy+=3){const half=rx*(1-Math.abs(yy)/ry)-3;for(let xx=-half;xx<half;xx+=4)c.put(cx+xx,cy+yy,yy%2?':':"'",'s');}
 c.rows(['  _   ',' (o)= ',' /_)  ',' ~~~  '],cx-15,cy-3,'p');c.rows([' .--. ','(____)','  / / '],cx+5,cy-7,'g');
 c.line(...top,...bottom,'|','b');c.line(...left,...right,'-','b');c.put(cx-1,cy,'(x)','k');
 for(let k=1;k<9;k++){const u=k/10;c.put(cx-rx*u,cy-ry*(1-u),':','p');c.put(cx+rx*u,cy+ry*(1-u),':','p');}
 const length=8+flight*23;
 let previous=bottom;
 for(let n=1;n<=length;n++){const next=[cx+Math.sin(n*.3+clock)*wind*4,cy+ry+n*.55];c.line(...previous,...next,null,'q');if(n%7===0)c.put(next[0]-3,next[1],'><><','q');previous=next;}
 const spool={x:22,y:p.h-10};let point=[cx,cy+3];
 for(let i=1;i<=26;i++){const u=i/26,next=[cx+(spool.x-cx)*u,cy+3+(spool.y-cy-3)*u+(1-flight)*Math.sin(Math.PI*u)*8];c.line(...point,...next,'.','p');point=next;}
 c.rect(spool.x-10,spool.y-6,20,12,'b',true);for(let y=spool.y-5;y<spool.y+6;y+=2)c.line(spool.x-8,y,spool.x+8,y,'=','p');
 for(const xx of [spool.x-12,spool.x+10])c.rect(xx,spool.y-8,3,16,'a',true);
 c.put(spool.x-2,spool.y,'(+)','k');
 return {entry:{x:38,y:p.h-2},contact:spool,spool,bridle:{x:cx,y:cy+3},tail:{x:previous[0],y:previous[1]}};
}
function fold(c,p,v){
 const x=16,y=p.h-64,w=96,h=60,f=clamp(v.fold);
 if(f<.95){
  polygon(c,[[x+f*20,y+f*8],[x+w-f*20,y+f*8],[x+w,y+h],[x,y+h]],'p');
  c.line(x+w/2,y,x+w/2,y+h,':','d');c.put(x+8,y+7,'POND AIR / FOLDING NOTES','d');
  c.put(x+8,y+13,'1. NOSE   2. SPINE   3. WINGS','d');
  c.rows(['    /\\         /\\        __/\\__','   / :\\       /||\\       \\ || /','  /__: \\     /_||_\\       \\||/','     |:|        ||          \\/'],x+9,y+21,'d');
  c.put(x+9,y+44,'NO ENGINES. ONLY ATTITUDE.','d');
  if(f>.05){polygon(c,[[x,y],[x+w/2,y+f*38],[x,y+f*45]],'g');polygon(c,[[x+w,y],[x+w/2,y+f*38],[x+w,y+f*45]],'p');}
 }
 if(f>.5){
  const u=(f-.5)*2,cx=p.w/2,tip=[cx+u*37,y+9],tail=[cx-39,y+24];
  polygon(c,[tip,tail,[cx-9,y+34]],'p');polygon(c,[tip,[cx+5,y+58],[cx-9,y+34]],'g');
  c.line(...tip,cx-9,y+34,'/','d');c.line(cx-9,y+34,cx-4,y+49,'|','d');c.put(cx-25,y+24,'POND AIR','d');c.put(cx-22,y+27,'NO. 01','d');
  c.line(cx+1,y+39,cx+4,y+51,':','s');c.line(cx-27,y+24,cx-13,y+31,':','d');
 }
 if(v.cover>.5){c.clear(26,y+2,76,56);c.rect(26,y+2,76,56,'k',true);for(let yy=y+6;yy<y+54;yy+=5)c.line(28,yy,99,yy,':','s');c.put(43,y+28,'POND AIR / KEEP DRY','a');}
 c.put(24,12,'FOLD / UNFOLD / TRY AGAIN','a');
 return {entry:{x:p.w/2,y:p.h-2},contact:{x:p.w/2,y:y+35},crease:{x:p.w/2,y:y+14+f*30},corner:{x:x+w,y:y+4},wing:{x:p.w/2+10,y:y+49}};
}
const BUILDERS={scope,easel,kite,fold};
export function creativeSprite(base,item,time,{state={},pose={}}={}){
 const p=BLUEPRINTS[item.id];if(!p)return null;
 const saved=state.creative||{},v={aim:saved.aim??.35,focus:saved.focus??.5,cap:saved.cap??1,fold:saved.fold??0,cover:saved.cover??0,flight:0,wind:0,stroke:0,seconds:0,...pose.creative};
 const c=new ObjectCanvas(p.w,p.h),anchors=BUILDERS[p.type](c,p,v,state);
 // Marks sit on existing material, never in the surrounding air.
 const cells=[];for(let y=0;y<p.h;y++)for(let x=0;x<p.w;x++)if(c.art[y][x]!==' ')cells.push([x,y]);
 for(const [amount,glyph,tone,stride] of [[state.wetness||0,"'",'w',37],[state.dirt||0,'.','s',53],[1-(state.condition??1),'/', 'k',71]])if(amount>.2)for(let n=0;n<Math.ceil(amount*14);n++){const at=cells[(n*stride+19)%cells.length];if(at)c.put(...at,glyph,tone);}
 const inks={b:'#d2b88c',a:'#e1c88a',f:'#e8ddbc',s:'#8d9483',k:'#667c71',p:'#ddcba1',d:'#334637',g:'#91c8be',w:'#88c6d7',q:'#dd9eab',l:'#83af75',n:'#7a85ac'};
 const panels={b:'#493e2c',a:'#6b5936',f:'#77664b',s:'#384735',k:'#12271f',p:'#b9ac82',d:'#293f32',g:'#527c7a',w:'#2d5567',q:'#754556',l:'#36503a',n:'#26364e'};
 return {...base,...c.finish(),construction:'creative-v1',detail:true,detailScale:.62,blueprint:item.id,anchors,inks,panels,sway:0,lift:0,animated:Boolean(pose.creative),emissive:false};
}
