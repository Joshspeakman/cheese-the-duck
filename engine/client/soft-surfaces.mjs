import CASTLE_GEOMETRY from './animation/castle-geometry.json' with {type:'json'};
import {ObjectCanvas} from './object-canvas.mjs';
import {CASTLE_DIAL} from './castle-air-geometry.mjs';
const finite=(v,d=0)=>Number.isFinite(v)?v:d,clamp=(v,a,b)=>Math.max(a,Math.min(b,finite(v)));
export function surfaceState(saved={}){
 if(!saved||typeof saved!=='object')saved={};
 const actor=r=>({jump:clamp(r?.jump,0,18),press:clamp(r?.press,0,1),u:clamp(r?.u,-1,1),v:clamp(r?.v,-1,1),impact:clamp(r?.impact,0,1)});
 return {a:actor(saved.a),b:actor(saved.b),lift:clamp(saved.lift,0,18),tilt:clamp(saved.tilt,-.65,.65),gate:clamp(saved.gate,0,1),active:saved.active===true};
}
function panel(c,x,y,w,h,tone){c.clear(x,y,w,h);return c.rect(x,y,w,h,tone,true);}
function polygon(c,pts,tone){
 const ys=pts.map(p=>p[1]);
 for(let y=Math.ceil(Math.min(...ys));y<Math.max(...ys);y++){
  const cuts=[];for(let n=0;n<pts.length;n++){const a=pts[n],b=pts[(n+1)%pts.length];if(a[1]!==b[1]&&y>=Math.min(a[1],b[1])&&y<Math.max(a[1],b[1]))cuts.push(a[0]+(y-a[1])*(b[0]-a[0])/(b[1]-a[1]));}
  cuts.sort((a,b)=>a-b);for(let n=0;n+1<cuts.length;n+=2){const x=Math.ceil(cuts[n]),w=Math.floor(cuts[n+1])-x+1;if(w>0){c.clear(x,y,w,1);c.solid(x,y,w,1,tone);}}
 }
 pts.forEach((a,i)=>c.line(...a,...pts[(i+1)%pts.length],null,'f'));
}
function stitch(c,x0,y0,x1,y1,tone='a'){const n=Math.ceil(Math.hypot(x1-x0,y1-y0)/3);for(let i=0;i<=n;i++){const u=i/n;c.put(x0+(x1-x0)*u,y0+(y1-y0)*u,'+','s');c.put(x0+(x1-x0)*u+1,y0+(y1-y0)*u,':',tone);}}
function impact(c,seat,v){if(v.impact<.05)return;const r=3+(1-v.impact)*12;c.put(seat.x-r,seat.y-1,'.','a');c.put(seat.x+r,seat.y-1,'.','a');c.put(seat.x-r+2,seat.y+1,'-','f');c.put(seat.x+r-2,seat.y+1,'-','f');}
export function softCarpet(c,p,v){
 const s=v.surface,fold=v.cover*10;
 const dy=x=>-s.lift+(x-87)*s.tilt*.09;
 const pressure=x=>s.a.press*2*Math.exp(-(((x-55)/19)**2))+s.b.press*2*Math.exp(-(((x-119)/19)**2));
 const point=(x,y)=>[x,y+dy(x)+pressure(x)];
 const poly=(pts,tone)=>polygon(c,pts.map(([x,y])=>point(x,y)),tone);
 // Braided edge, nested woven borders and a hand-knotted compass medallion.
 poly([[22,28+fold],[151,24+fold],[164,76],[12,84]],'q');
 poly([[27,32+fold],[146,29+fold],[157,72],[20,78]],'a');
 poly([[33,36+fold],[141,33+fold],[150,68],[28,72]],'w');
 for(let y=37+fold;y<69;y+=2)for(let x=35;x<145;x+=4)c.put(...point(x,y),'~','g');
 for(let x=29;x<148;x+=7){c.put(...point(x,31+fold),'<>','q');c.put(...point(x-2,75),'<>','q');}
 for(let y=41+fold;y<69;y+=5){c.put(...point(24,y),'<>','g');c.put(...point(153,y-1),'<>','g');}
 poly([[87,35+fold],[119,52],[87,70],[55,54]],'q');poly([[87,40+fold],[110,52],[87,64],[65,54]],'a');
 c.rows(['    . /\\ .','  < ( >< ) >','    \\_||_/','      \\/'],80,47+dy(87)+fold*.3,'k');
 for(const [x,y]of [[42,46],[132,42],[40,63],[135,61]]){c.put(...point(x,y),'/\\','g');c.put(...point(x,y+1),'\\/','g');}
 for(let n=0;n<18;n++){
  const u=n/17,x=22-u*10,y=28+fold+u*(56-fold),x2=151+u*13,y2=24+fold+u*(52-fold);
  c.line(...point(x,y),...point(x-7,y+Math.sin(v.wind_phase+n*.25)*v.wind),'~','a');c.put(...point(x-8,y),'o','b');
  c.line(...point(x2,y2),...point(x2+6,y2-Math.sin(v.wind_phase+n*.3)*v.wind),'~','a');
 }
 stitch(c,...point(24,30+fold),...point(149,26+fold),'q');stitch(c,...point(16,82),...point(162,74),'q');
 for(const x of [29,50,72,96,119,142])c.put(...point(x,77),s.lift>3&&v.lights>.5?'*':':',s.lift>3&&v.lights>.5?'a':'b');
 const slots=[{x:55+s.a.u*8,y:58+s.a.v*4},{x:119+s.b.u*8,y:56+s.b.v*4}].map(a=>({...a,y:a.y+dy(a.x)+pressure(a.x)}));
 // The fringe lies in front of seated feet; its narrow strip never masks faces.
 const front=new ObjectCanvas(p.w,p.h);
 for(let x=14;x<163;x++){const y=82-(x-14)*6/149+dy(x)+pressure(x);front.put(x,y,x%3?'~':'+','a');}
 return {entry:{x:87,y:94},contact:{x:28,y:74+dy(28)},surface:'carpet',slots,front:front.finish(),route:[{x:87,y:94},{x:87,y:82+dy(87)}],tassel:{x:12,y:65+dy(12)}};
}
export function softCastle(c,p,v){
 const s=v.surface,care=v.castle,sink=(1-v.inflation)*34;
 const seatX=[CASTLE_GEOMETRY.floor_slots[0].x+s.a.u*10,CASTLE_GEOMETRY.floor_slots[1].x+s.b.u*10],press=x=>s.a.press*3*Math.exp(-(((x-seatX[0])/22)**2))+s.b.press*3*Math.exp(-(((x-seatX[1])/22)**2));
 panel(c,12,119,155,18,'a');
 for(let n=0;n<9;n++)c.ellipse(20+n*17,127,10,9,'_',['q','g','w'][n%3],true);
 polygon(c,[[30,49+sink],[150,49+sink],[154,110],[26,110]],'k');
 for(let y=52+sink,row=0;y<105;y+=3,row++)for(let x=32;x<150;x+=5)c.put(x+row%2*2,y,'/\\','s');
 // Each rib sinks locally under a foot or belly rather than the whole house bobbing.
 for(let x=25;x<=155;x++){
  const y=109+press(x);c.clear(x,y,1,10);c.solid(x,y,1,10,'g');c.put(x,y,'_','f');c.put(x,118+press(x),'=','a');
  if(x%8===0)c.line(x,y+2,x,116+press(x),':','s');
 }
 for(const [x,tone]of [[17,'q'],[162,'g']]){
  const top=24+sink;c.ellipse(x,top,13,12,'_','a',true);panel(c,x-13,top,27,94-sink,tone);c.ellipse(x,118,13,5,'_','a',true);
  for(const dx of [-8,8])c.line(x+dx,top+4,x+dx,114,':','f');
  c.rows(['|_|_|_|_|','| : : : |'],x-8,top-9,'a');c.put(x-6,top+17,'<><>','a');
  for(let yy=top+26;yy<112;yy+=11){c.line(x-10,yy,x+10,yy,':','s');c.put(x-2,yy+3,'<o>','a');}
 }
 polygon(c,[[14,36+sink],[90,8+sink],[166,36+sink]],'q');
 for(let n=0;n<9;n++)c.line(90,10+sink,18+n*18,36+sink,'/',['a','g','w'][n%3]);
 panel(c,28,37+sink,124,11,'a');c.put(45,41+sink,'THE WOBBLY DUCK / BOUNCE CLUB','k');
 stitch(c,18,35+sink,90,12+sink);stitch(c,90,12+sink,161,35+sink);
 const gate=Math.max(s.gate,care.door),top=67+sink*.5,door=22+gate*36;
 // A wide roll-up mesh door reaches the spring floor; no wall is crossed.
 for(const side of [-1,1]){
  const x=90+side*door/2;c.line(x,top,x+side*3,119,'|','g');c.put(x-1,top+2,'[o]','a');
  if(gate<.95)for(let y=top+4;y<114;y+=4)c.put(x-side*4,y,side<0?'/>':'<\\','s');
 }
 c.line(90-door/2,top,90+door/2,top,'=','a');
 if(gate<.1)for(let y=top+4;y<114;y+=4)for(let x=90-door/2+4;x<90+door/2-3;x+=5)c.put(x,y,'/\\','s');
 panel(c,62,129,56,8,'g');c.put(72,132,'SOFT LANDING','a');
 c.rows(['  ___________',' /__________/','[___________]'],73,139-care.apron*7,'a');
 for(let y=0;y<care.apron*6;y++)c.line(74,139-y,86,139-y,'=','g');
 for(let i=0;i<Math.floor(care.prints*8);i++)c.put(67+(i*13)%42,134+(i%2)*2,'v:','s');
 c.line(169,119,175,124,'~','m');panel(c,169,127,10,12,'m');c.put(171,131,'[o]','k');c.put(170,135,'||||||','s');
 c.line(90,7+sink,90,1+sink,'|','m');const flagY=1+sink+(1-care.flag)*(125-sink),flagX=91-(1-care.flag)*63;polygon(c,[[flagX,flagY],[flagX+13,flagY+2],[flagX,flagY+4]],'g');
 c.line(90,8+sink,27,126,':','s');c.line(27,126,27,142,'|','a');c.put(24,140,'[=]','m');
 for(const [side,tie]of [[-1,care.tie_left],[1,care.tie_right]]){
  const x=side<0?17:162,end=side<0?4:167;c.line(x,113,end,131+(1-tie)*10,'~','a');c.line(end,131+(1-tie)*10,end,143,'~','a');c.put(end-2,143,'[+]','m');
 }
 c.line(118,top+3,118,140,'|','a');c.put(116,140,'(o)','a');
 c.put(91,141,care.latch>.5?'[><]':'[> <]','m');
 panel(c,145,131,22,15,'m');c.put(147,133,'AIR / PRESSURE','a');
 c.put(148,141,care.motor==='off'?'[ ]':'[o]','a');c.put(155,141,care.vent>.5?'( / )':'(---)','q');
 const [dialX,dialY]=CASTLE_DIAL.needle_origin;
 c.line(dialX,dialY,dialX+Math.cos(Math.PI-care.pressure*Math.PI)*CASTLE_DIAL.radius_x,dialY-Math.sin(Math.PI-care.pressure*Math.PI)*CASTLE_DIAL.radius_y,null,'a');c.put(157,144,'0  :  1','k');
 c.put(171,131,care.rotor_speed>0?['|','/','-','\\'][v.motion===false?0:((Math.floor(care.fan*2)%4)+4)%4]:'o','a');
 for(let i=0;i<Math.floor(care.dust*7);i++)c.put(170+i%6,134+Math.floor(i/6),':','s');
 c.line(166,139,174,139+care.kink*4,'~','m');
 if(care.hose>.1)for(let i=0;i<Math.ceil(care.hose*3);i++)c.ellipse(174,143-i,4,2,'~','a');
 for(let i=0;i<Math.floor(care.mesh_wet*12);i++)c.put(84+(i*7)%16,86+i*2,"'",'w');
 for(let i=0;i<Math.floor(care.roof_water*16);i++)c.put(52+i*5,34+sink,'~','w');
 c.line(151,48+sink,143,140,':','w');c.put(140,140,'(=)','m');
 if(care.spray>.04)for(let i=0;i<6;i++)c.put(137+i%3*4,126+i*3+care.stroke,"'",'w');
 c.put(40,140,'[::]','s');
 c.line(79,140-care.apron*7,79,141,':','a');c.put(77,141,'(=)','a');
 const slots=[{x:seatX[0],y:116+press(seatX[0])+s.a.v*3},{x:seatX[1],y:116+press(seatX[1])+s.b.v*3}];
 for(const [i,r]of [s.a,s.b].entries())impact(c,slots[i],r);
 const front=new ObjectCanvas(p.w,p.h);
 // Only the low apron is in front of players. Side/back mesh stays behind them.
 for(let x=25;x<=155;x++)front.put(x,120+press(x),'=','a');
 const controls=structuredClone(CASTLE_GEOMETRY.controls);
 return {entry:{...CASTLE_GEOMETRY.entry},contact:{...CASTLE_GEOMETRY.contact},surface:'castle',slots,controls,front:front.finish(),route:structuredClone(CASTLE_GEOMETRY.route),blower:{...CASTLE_GEOMETRY.contact},mesh:{x:43,y:70+sink}};
}
