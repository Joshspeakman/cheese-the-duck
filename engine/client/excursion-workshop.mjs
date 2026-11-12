import {softCarpet,softCastle,surfaceState} from './soft-surfaces.mjs';
import {castleState} from './castle-care.mjs';
import {ObjectCanvas} from './object-canvas.mjs';
import BLUEPRINTS from './animation/excursions.json' with {type:'json'};
export {BLUEPRINTS as EXCURSION_BLUEPRINTS};
const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,Number.isFinite(v)?v:0));
const finite=(v,fallback=0)=>Number.isFinite(v)?v:fallback;
const TAU=Math.PI*2;
function panel(c,x,y,w,h,tone){c.clear(x,y,w,h);return c.rect(x,y,w,h,tone,true);}
function opaqueEllipse(c,cx,cy,rx,ry,char,tone){
 for(let y=Math.ceil(cy-ry);y<=Math.floor(cy+ry);y++){
  const half=rx*Math.sqrt(Math.max(0,1-((y-cy)/ry)**2)),left=Math.round(cx-half),right=Math.round(cx+half);
  c.clear(left,y,right-left+1,1);
 }
 return c.ellipse(cx,cy,rx,ry,char,tone,true);
}
function polygon(c,pts,tone,edge='f'){
 const ys=pts.map(p=>p[1]);
 for(let y=Math.ceil(Math.min(...ys));y<Math.max(...ys);y++){
  const cuts=[];
  for(let n=0;n<pts.length;n++){
   const a=pts[n],b=pts[(n+1)%pts.length];
   if(a[1]!==b[1]&&y>=Math.min(a[1],b[1])&&y<Math.max(a[1],b[1]))cuts.push(a[0]+(y-a[1])*(b[0]-a[0])/(b[1]-a[1]));
  }
  cuts.sort((a,b)=>a-b);for(let n=0;n+1<cuts.length;n+=2){const x=Math.ceil(cuts[n]),w=Math.floor(cuts[n+1])-x+1;if(w>0){c.clear(x,y,w,1);c.solid(x,y,w,1,tone);}}
 }
 pts.forEach((a,i)=>c.line(...a,...pts[(i+1)%pts.length],null,edge));
}
function ring(c,x,y,rx,ry,tone='a'){
 opaqueEllipse(c,x,y,rx,ry,'=','k');opaqueEllipse(c,x,y,rx-2,ry-2,'o',tone);
 opaqueEllipse(c,x,y,rx-4,ry-4,'-','w');
 for(let n=0;n<8;n++){const a=n*Math.PI/4;c.put(x+Math.cos(a)*(rx-1),y+Math.sin(a)*(ry-1),'o','f');}
 c.line(x-rx+5,y-1,x-2,y-ry+5,'/','c');c.put(x+2,y+ry-5,'..','g');
}
function wheel(c,x,y,rx,ry,phase){
 c.ellipse(x,y,rx,ry,'#','k',true);c.ellipse(x,y,rx-2,ry-2,'=','m',true);
 for(let n=0;n<8;n++){const a=phase+n*Math.PI/4;c.line(x,y,x+Math.cos(a)*(rx-3),y+Math.sin(a)*(ry-3),null,'s');}
 c.put(x-2,y,'(+)','a');
}
function bolts(c,x0,y0,x1,y1,count=8,tone='a'){for(let n=0;n<=count;n++){const u=n/count;c.put(x0+(x1-x0)*u,y0+(y1-y0)*u,'o',tone);}}
function gauge(c,x,y,label,angle=-.7){
 c.ellipse(x,y,6,5,'-','a',true);c.ellipse(x,y,4,3,'.','p',true);
 c.line(x,y,x+Math.cos(angle)*3,y+Math.sin(angle)*2,null,'k');c.put(x-1,y,'o','k');c.put(x-5,y+6,label,'f');
}
function pennant(c,x,y,phase,tone='q',wind=.4){
 c.line(x,y,x,y+10,'|','m');const dy=Math.sin(phase)*wind*2;
 polygon(c,[[x+1,y],[x+14,y+2+dy],[x+1,y+5]],tone);
}
function stitch(c,x0,y0,x1,y1,tone='a'){
 const n=Math.ceil(Math.hypot(x1-x0,y1-y0)/3);
 for(let i=0;i<=n;i++){const u=i/n;c.put(x0+(x1-x0)*u,y0+(y1-y0)*u,'+','s');c.put(x0+(x1-x0)*u+1,y0+(y1-y0)*u,':',tone);}
}
function barrow(c,p,v){
 wheel(c,25,61,13,12,0);
 c.beam(33,48,113,28,3,'b');c.beam(33,54,117,36,3,'b');
 c.rows(['[=======]',' \\_____'],111,26,'k');c.rows(['[=======]',' \\_____'],115,34,'k');
 for(const x of [73,94]){c.beam(x,47,x-6,72,3,'m');c.line(x-6,72,x+3,72,'_','s');c.put(x-7,73,'[____]','k');}
 polygon(c,[[25,22],[88,13],[107,31],[39,43]],'g');
 polygon(c,[[25,22],[39,43],[47,57],[32,40]],'s');
 polygon(c,[[39,43],[107,31],[99,51],[47,57]],'b');
 c.line(30,23,87,17,'_','f');c.line(87,17,101,31,'\\','f');c.line(42,43,102,33,'=','a');
 for(let n=0;n<6;n++){const x=47+n*8;c.line(x,44-n,x+3,52-n,'|','s');c.put(x+3,48-n,':','a');}
 bolts(c,47,55,98,49,7);c.put(60,48,'POND WORKS','a');
 polygon(c,[[31,24],[86,18],[99,30],[44,38]],'k');
 c.line(34,26,85,20,':','s');c.line(44,35,95,30,'_','g');
 for(const [x,y]of [[49,28],[62,27],[75,25],[53,31],[71,31]])c.put(x,y,'--:','s');
 c.put(65,33,'..::..','b');
 c.line(13,59,38,59,'=','m');c.put(22,60,'[+]','a');
 return {entry:{x:113,y:74},contact:{x:115,y:28},tray:{x:68,y:32},wheel:{x:25,y:61},handles:[{x:116,y:28},{x:120,y:36}]};
}
function pack(c,p,v){
 panel(c,24,20,46,64,'k');
 for(const x of [24,68]){
  c.ellipse(x,30,14,12,'_','m',true);panel(c,x-14,30,29,43,'m');c.ellipse(x,73,14,7,'_','s',true);
  for(const dx of [-10,10])c.line(x+dx,32,x+dx,70,'|',dx<0?'f':'s');
  c.line(x-7,29,x-7,70,':','f');
  for(const y of [38,60]){panel(c,x-15,y,31,4,'a');bolts(c,x-12,y+1,x+12,y+1,4,'k');}
  polygon(c,[[x-9,77],[x+9,77],[x+13,90],[x-13,90]],'k');
  for(let xx=x-8;xx<x+9;xx+=4)c.line(xx,80,xx,88,'|','m');
  c.ellipse(x,90,13,3,'=','m',true);c.ellipse(x,90,8,1,'-','k',true);
  c.put(x-7,48,x<40?'PORT 01':'STBD 02','k');c.put(x-5,53,'// //','f');
  for(const y of [27,34,45,57,68,74])c.put(x+5,y,'::','s');
  c.line(x+7,42,x+7,58,'|','k');c.line(x-9,63,x-9,68,'|','a');
 }
 c.line(29,18,34,8,'/','b');c.line(34,8,61,8,'=','b');c.line(61,8,66,18,'\\','b');
 c.line(32,15,37,12,'/','a');c.line(37,12,59,12,'_','a');
 for(const [x,side]of [[18,-1],[75,1]]){c.line(x,24,x+side*9,42,'|','k');c.line(x+side*9,42,x+side*7,72,'|','k');c.put(x+side*7-2,70,'[=]','a');}
 panel(c,37,42,19,30,'b');gauge(c,46,49,'IDLE',-2.5);c.put(40,64,'[ o o ]','a');
 c.line(29,76,38,81,'~','k');c.line(38,81,54,81,'~','k');c.line(54,81,65,76,'~','k');
 c.line(27,15,27,22,'|','a');c.put(23,14,'--(+)--','q');c.line(68,15,68,22,'|','a');c.put(64,14,'--(+)--','q');
 c.put(32,97,'FLIGHT / IMAGINATION','a');
 return {entry:{x:47,y:105},contact:{x:46,y:65},gauge:{x:46,y:49},strap:{x:14,y:60},nozzles:[{x:24,y:90},{x:68,y:90}]};
}
function sub(c,p,v){
 c.line(79,38,79,15,'|','m');c.line(82,38,82,13,'|','a');panel(c,76,9,22,7,'m');c.put(95,11,'[O]','w');
 c.ellipse(75,39,19,9,'_','s',true);panel(c,57,39,37,10,'a');
 c.ellipse(74,61,57,26,'_','a',true);c.ellipse(74,59,52,21,'_','b',true);
 for(const y of [44,74,80]){const half=50*Math.sqrt(Math.max(0,1-((y-61)/23)**2));c.line(74-half,y,74+half,y,':','s');}
 for(const x of [31,59,88,116]){c.line(x,47,x,72,'|','s');bolts(c,x+2,48,x+2,71,5,'a');}
 for(let n=0;n<38;n++){const a=n*TAU/38;c.put(74+Math.cos(a)*53,61+Math.sin(a)*23,'o','f');}
 for(const x of [45,74,103])ring(c,x,59,12,10,'a');
 c.put(47,78,'P O N D  /  D I V E R','f');c.put(25,55,'[::]','k');
 polygon(c,[[112,73],[139,82],[115,84]],'a');polygon(c,[[115,48],[137,36],[124,60]],'b');
 c.line(127,64,141,64,'=','m');c.ellipse(142,64,3,12,'|','k',true);c.put(140,64,'(+)','a');
 for(const side of [-1,1])c.line(142,64,142+side*3,64+side*11,'|','m');
 c.rect(26,68,15,6,'s');c.put(28,70,'||| |||','k');c.rect(104,69,16,6,'s');c.put(106,71,'||| |||','k');
 c.put(59,85,'DIVE / 03m','k');
 c.ellipse(72,32,11,3,'=','m',true);c.line(72,29,72,35,'|','k');c.line(66,32,78,32,'-','k');
 c.line(29,88,118,88,'~','w');c.line(43,90,106,90,'-','g');c.put(34,89,'~--','c');c.put(111,89,'--~','c');
 return {entry:{x:76,y:93},contact:{x:72,y:32},hatch:{x:72,y:34},window:{x:74,y:59},propeller:{x:142,y:64}};
}
function rocket(c,p,v){
 const cx=56;
 polygon(c,[[cx,5],[cx+20,35],[cx+24,108],[cx-24,108],[cx-20,35]],'m');
 for(let y=18;y<39;y+=4){const w=(y-5)*.67;c.line(cx-w+2,y,cx+w-2,y,':','q');}
 c.line(37,36,75,36,'=','a');c.line(37,40,75,40,'-','s');
 for(const x of [37,75]){c.line(x,45,x,102,'|','s');bolts(c,x+2,44,x+2,100,9,'a');}
 c.line(43,45,43,102,':','f');ring(c,56,57,13,12,'a');
 panel(c,45,77,23,24,'b');c.put(47,81,'POND','f');c.put(47,85,'ORBITAL','a');c.put(48,91,'NO. 01','f');
 c.put(46,97,'[ :: :: ]','k');c.line(33,106,79,106,'=','a');c.line(33,109,79,109,'-','s');
 for(const y of [42,73,103]){c.line(36,y,76,y,'_','s');bolts(c,38,y+1,74,y+1,6,'a');}
 for(const [x,y]of [[38,82],[69,82],[38,94],[70,94]])c.rows(['[||]','[||]'],x,y,'s');
 c.put(48,17,'P / 01','q');c.put(49,69,'* - *','q');c.put(48,75,'NO BREAD','k');
 polygon(c,[[33,84],[14,115],[13,134],[38,112]],'q');polygon(c,[[79,84],[98,115],[99,134],[74,112]],'q');
 c.line(20,117,31,101,'/','f');c.line(92,117,81,101,'\\','f');
 polygon(c,[[43,111],[69,111],[75,129],[37,129]],'k');
 for(let x=42;x<73;x+=5)c.line(x,115,x,127,'|','m');c.ellipse(56,130,19,4,'=','m',true);c.ellipse(56,130,14,2,'-','k',true);
 for(const side of [-1,1]){c.beam(cx+side*22,112,cx+side*31,140,3,'m');c.put(cx+side*31-7,141,'[____________]','k');}
 c.line(80,73,101,73,'_','a');c.line(101,73,101,137,'|','m');
 for(let y=77;y<137;y+=5)c.line(88,y,101,y,'=','m');c.line(88,75,88,137,'|','m');
 c.put(82,68,'GANTRY','a');
 return {entry:{x:99,y:144},contact:{x:88,y:77},hatch:{x:57,y:86},window:{x:56,y:57},gantry:{x:95,y:128}};
}
function balloon(c,p,v){
 const cx=64+Math.sin(v.wind_phase)*v.wind*3,cy=37+(1-v.inflation)*25,rx=46*(.65+v.inflation*.35),ry=36*(.5+v.inflation*.5);
 c.ellipse(cx,cy,rx,ry,'_','q',true);
 for(let y=Math.ceil(cy-ry);y<=Math.floor(cy+ry);y++){
  const half=rx*Math.sqrt(Math.max(0,1-((y-cy)/ry)**2));
  for(let n=-3;n<4;n++){const x=cx+n*half/4;if(n>-3)c.solid(x,y,Math.max(1,half/4),1,['q','a','g','q','a','g'][n+2]||'q');c.put(x,y,Math.abs(y-cy)>ry*.85?'_':'|','f');}
 }
 // Stitched gore joins and the two reinforced horizontal envelope belts.
 for(const u of [-.5,.4]){
  const y=cy+ry*u,half=rx*Math.sqrt(1-u*u);
  c.line(cx-half+3,y,cx+half-3,y,':','a');
  for(let x=cx-half+4;x<cx+half-3;x+=5)c.put(x,y+1,'+','s');
 }
 for(let n=-2;n<=2;n++){
  for(let u=-.7;u<.75;u+=.14){const half=rx*Math.sqrt(1-u*u);c.put(cx+n*half/4+1,cy+ry*u,'=','a');}
 }
 for(let n=-3;n<=3;n++){
  const x=cx+n*11;c.line(x,cy+ry*.7,64+n*3,94,'\\','b');c.put(x-1,cy+ry*.7,'o','a');
 }
 c.ellipse(64,96,12,3,'=','k',true);c.put(58,97,'[ BURNER ]','a');
 for(const x of [42,86])c.line(cx+(x-64)*1.3,cy+ry*.65,x,101,'|','b');
 c.line(42,100,86,100,'=','m');
 for(const x of [42,86]){c.line(x,101,x,130,'|','b');c.line(x+1,101,x+1,130,':','f');}
 panel(c,38,127,52,22,'b');c.ellipse(64,127,26,5,'=','a',true);c.ellipse(64,126,22,3,'_','k',true);
 for(let y=132;y<147;y+=2)for(let x=40;x<88;x+=4)c.put(x+(y%4?1:0),y,y%4?'[]':'==','a');
 for(const x of [45,81]){c.line(x,130,x,147,'|','s');c.put(x-2,134,'[o]','f');}
 c.put(49,141,'BREAD AERONAUTICS','k');
 c.rows([' /==\\ ','(____)',' |::| '],60,113,'a');c.line(64,108,64,112,'|','b');
 for(const [x,end]of [[43,14],[85,114]]){c.line(x,103,end,148,'/','b');c.put(end-3,149,'_[|]_','m');}
 c.line(91,133,99,133,'=','b');c.line(91,140,99,140,'=','b');c.line(99,130,99,148,'|','b');
 return {entry:{x:99,y:151},contact:{x:83,y:130},basket:{x:64,y:126},burner:{x:64,y:97},tether:{x:114,y:148}};
}
function saucer(c,p,v){
 const cx=74,cy=59;
 for(const [x,y]of [[32,75],[116,75],[74,80]]){c.beam(x,y,x+(x-cx)*.15,99,4,'m');c.put(x+(x-cx)*.15-7,100,'[____________]','k');}
 c.ellipse(cx,65,66,21,'_','s',true);c.ellipse(cx,59,66,19,'=','m',true);
 for(let n=0;n<20;n++){const a=n*TAU/20,x=cx+Math.cos(a)*59,y=cy+Math.sin(a)*14;c.ellipse(x,y,3,2,'o',v.lights>.5?'a':'g',true);}
 c.ellipse(cx,52,49,11,'=','a',true);opaqueEllipse(c,cx,45,34,22,'_','w');
 for(let x=47;x<103;x+=10){const dy=20*Math.sqrt(Math.max(0,1-((x-cx)/34)**2));c.line(x,45-dy+3,x,52,'|','g');}
 c.line(47,36,64,27,'/','c');c.put(54,35,'//','c');c.put(90,50,'..','g');
 c.ellipse(cx,53,32,5,'=','m',true);c.put(61,54,'O  O  O  O  O','a');
 for(const [x,y]of [[26,62],[44,68],[97,68],[115,62]]){c.put(x,y,'[::::]','k');c.put(x+1,y+2,'----','f');}
 for(const x of [35,109]){c.line(x,76,x,89,'|','s');c.put(x-2,82,'[o]','a');}
 c.line(74,22,74,8,'|','m');c.ellipse(74,7,9,3,'_','q',true);c.line(74,7,74+Math.cos(v.phase)*7,7+Math.sin(v.phase)*2,null,'f');
 panel(c,61,68,27,13,'k');c.line(64,72,85,72,'=','a');c.put(66,75,'POND / 51','g');
 c.line(64,81,57,95,'/','m');c.line(85,81,92,95,'\\','m');for(let y=83;y<96;y+=3)c.line(63-(y-82)*.4,y,86+(y-82)*.4,y,'=','m');
 return {entry:{x:74,y:102},contact:{x:88,y:76},hatch:{x:74,y:75},dome:{x:74,y:43},scanner:{x:74,y:7}};
}
function gondola(c,x,y,tone,lights,front=false){
 if(!front){
  c.line(x,y-7,x,y-2,'|','m');
  c.line(x-25,y-4,x+25,y-4,'=','a');
  for(const dx of [-25,25]){c.line(x+dx,y-4,x+dx,y+10,'|','m');c.put(x+dx,y-5,lights?'*':'o',lights?'a':'f');}
  panel(c,x-24,y+5,49,5,'b');c.line(x-21,y+6,x+21,y+6,'_','f');
 }
 polygon(c,[[x-26,y+8],[x+26,y+8],[x+23,y+17],[x-23,y+17]],tone);
 c.line(x-26,y+8,x+26,y+8,'=','a');c.line(x-22,y+15,x+22,y+15,'_','s');
 for(const dx of [-19,-12,12,19])c.line(x+dx,y+10,x+dx,y+14,':','f');
 c.put(x-5,y+11,'[ <><> ]','a');c.put(x-23,y+10,'o','a');c.put(x+23,y+10,'o','a');
}
function ferris(c,p,v){
 const cx=92,cy=53,rx=62,ry=41,phase=v.phase;
 for(const side of [-1,1]){c.beam(cx,cy,cx+side*43,123,5,'g');c.line(cx+side*3,cy+8,cx+side*35,118,':','f');c.put(cx+side*43-9,124,'[________________]','k');}
 c.line(61,110,123,110,'=','m');c.line(61,110,110,82,'/','s');c.line(123,110,74,82,'\\','s');
 c.ellipse(cx,cy,rx,ry,'o','a');c.ellipse(cx,cy,rx-3,ry-3,'=','m');
 const cabins=[],fronts=[];
 for(let n=0;n<8;n++){
  const a=phase+n*Math.PI/4,x=cx+Math.cos(a)*rx,y=cy+Math.sin(a)*ry;
  c.line(cx,cy,x,y,null,'m');c.line(cx+2,cy,x+2,y,null,'s');
  const b=a+Math.PI/4;c.line(x,y,cx+Math.cos(b)*rx,cy+Math.sin(b)*ry,null,'g');
  c.put(cx+Math.cos(a)*28,cy+Math.sin(a)*26,'o','a');
  if(n%2===0)cabins.push({x,y:y+7,index:n/2,seat:{x,y:y+13},width:49});
 }
 for(let n=0;n<48;n++){const a=n*TAU/48;c.put(cx+Math.cos(a)*(rx+1),cy+Math.sin(a)*(ry+1),v.lights>.5?'*':'o',v.lights>.5?'a':'m');}
 c.clear(cx-10,cy-7,21,15);c.ellipse(cx,cy,10,7,'=','q',true);c.ellipse(cx,cy,6,4,'o','a',true);c.put(cx-3,cy,'( + )','k');
 cabins.sort((a,b)=>a.y-b.y).forEach(a=>{
  const tone=['q','w','g','a'][a.index];gondola(c,a.x,a.y,tone,v.lights>.5);
  const f=new ObjectCanvas(p.w,p.h);gondola(f,a.x,a.y,tone,v.lights>.5,true);fronts.push({index:a.index,...f.finish()});
 });
 // Low landing deck and broad stairs reach the open cabin at the bottom.
 panel(c,61,119,70,5,'b');c.line(61,119,130,119,'=','a');
 for(let x=64;x<129;x+=8)c.put(x,122,'o','s');
 for(let i=0;i<4;i++){const x=127+i*7,y=123+i*5;panel(c,x,y,14,5,'b');c.line(x,y,x+13,y,'=','a');}
 c.line(135,114,158,133,'\\','m');c.line(134,114,134,123,'|','m');c.line(158,133,158,140,'|','m');
 panel(c,18,122,36,17,'b');c.put(21,125,'POND VIEW','a');c.put(21,129,'FOUR ROOMY CABINS','f');c.put(21,134,'TICKETS [o]','a');
 return {entry:{x:153,y:141},contact:{x:134,y:123},wheel:{x:cx,y:cy},cabins,fronts,platform:{x:92,y:107},route:[{x:153,y:141},{x:139,y:128},{x:124,y:119},{x:92,y:107}]};
}
function carvedDuck(c,x,y,tone,flip=false){
 const rows=['                 _..._','               .\'  o  `.','              /    .---\'===.','             /    /________>','            /    /','  __..-----\'    /',' /  .--------.   \\','(  /  vvvvvv  \\   )',' \\  \\_vvvvv_/   /','  `----._____.--\'','       |     |','     __|     |__'];
 const art=flip?rows.map(r=>[...r.padEnd(30)].reverse().map(a=>({'/':'\\','\\':'/','(' :')',')':'(','<':'>','>':'<'}[a]||a)).join('')):rows;
 c.rows(art,x-15,y-8,tone,true);panel(c,x-9,y-3,20,3,'q');c.put(x-7,y-2,'=<>==<>==<>==<>','a');
}
function carouselRoof(c,v){
 polygon(c,[[12,40],[74,9],[136,40]],'q');
 for(let i=0;i<8;i++){const x=13+i*15.2;polygon(c,[[74,9],[x,40],[x+14,40]],i%2?'a':'g');}
 for(let i=0;i<8;i++){const x=13+i*15.2;stitch(c,74,10,x+7,39);}
 c.ellipse(74,42,65,6,'=','b',true);
 for(let x=16;x<137;x+=12){c.clear(x-6,43,13,8);c.ellipse(x,45,6,5,'_','q',true);c.put(x-3,44,'<o>','a');c.put(x-1,48,v.lights>.5?'*':'o',v.lights>.5?'a':'f');}
 c.put(49,40,'THE QUACK-A-ROUND','a');c.line(74,8,74,2,'|','a');c.put(71,1,'<*>','q');
}
function carousel(c,p,v){
 const cx=74,ground=111;
 c.ellipse(cx,ground,66,12,'=','b',true);c.ellipse(cx,ground-3,62,9,'_','a',true);
 for(let x=20;x<133;x+=9){c.line(x,104,x+2,116,'|','s');c.put(x+1,115,'o','a');c.put(x+4,111,'~','s');}
 c.rect(68,36,13,72,'g',true);c.line(70,38,70,106,':','f');c.line(78,38,78,106,'|','k');
 const rides=[],fronts=[];
 for(let i=0;i<4;i++){const a=v.phase+i*Math.PI/2,y=94+Math.sin(a)*8-Math.sin(a*2)*3,x=cx+Math.cos(a)*46;rides.push({x,y,phase:a,index:i,seat:{x,y:y-3},width:30});}
 for(const r of rides.sort((a,b)=>a.y-b.y)){
  c.line(r.x,43,r.x,r.y+10,'|','a');c.line(r.x+1,44,r.x+1,r.y+10,':','f');
  carvedDuck(c,r.x,r.y,['p','g','q','a'][r.index],Math.sin(r.phase)<0);
  c.put(r.x-4,r.y+10,'[______]','m');
  const f=new ObjectCanvas(p.w,p.h);f.line(r.x+7,r.y-12,r.x+7,r.y+4,'|','a');f.put(r.x+5,r.y-9,'[o]','f');fronts.push({index:r.index,...f.finish()});
 }
 carouselRoof(c,v);const roof=new ObjectCanvas(p.w,p.h);carouselRoof(roof,v);
 c.rows([' _________','/__/__/__/','|__|__|__|'],111,115,'m');
 return {entry:{x:121,y:126},contact:{x:121,y:115},seat:rides.at(-1).seat,pole:{x:74,y:77},rides,fronts,roof:roof.finish(),route:[{x:121,y:126},{x:118,y:114},{x:108,y:104}]};
}
const BUILDERS={barrow,pack,sub,rocket,balloon,saucer,carpet:softCarpet,inflatable:softCastle,wheel:ferris,carousel};
export function excursionSprite(base,item,time,{state={},motion=true,context={}}={}){
 const p=BLUEPRINTS[item.id];if(!p)return null;
 const saved=state.excursion||{},hour=finite(context.hour,12),weather=String(context.weather||'sunny').toLowerCase();
 const wet=weather!=='rainbow'&&/rain|storm|snow|blizzard|drizzle|shower|hail|sleet|tornado|hurricane|gale|freezing/.test(weather);
 const t=motion?time:0;
 // Catalogue previews may animate; real objects use only their native state.
 const quiet=hour<7||hour>=20,wind=clamp(finite(saved.wind,finite(context.living?.ecology?.wind,.35)));
 const v={phase:finite(saved.phase,t*.12),wind_phase:finite(saved.wind_phase,t*.7),wind,inflation:clamp(finite(saved.inflation,wet||quiet||wind>=.8?.35:1)),cover:clamp(finite(saved.cover,wet?1:0)),lights:clamp(finite(saved.lights,Number(!wet&&(hour>=18||hour<6))))};
 // Accessibility must not rewind a real wheel, cabin, cover or inflation state.
 if(!motion){v.wind_phase=0;v.wind=0;}
 v.surface=surfaceState(saved.surface);
 v.motion=motion;
 v.castle=castleState(state.castle);
 const c=new ObjectCanvas(p.w,p.h),anchors=BUILDERS[p.type](c,p,v);
 const cells=[];for(let y=0;y<p.h;y++)for(let x=0;x<p.w;x++)if(c.art[y][x]!==' ')cells.push([x,y]);
 for(const [amount,glyph,tone,step]of [[clamp(state.wetness),"'",'w',37],[clamp(state.dirt),'.','s',59],[1-clamp(finite(state.condition,1)),'/', 'k',83]])if(amount>.2)for(let n=0;n<Math.ceil(amount*18);n++){const at=cells[(n*step+7)%cells.length];if(at)c.put(...at,glyph,tone);}
 const inks={b:'#cda879',m:'#b4c4c1',a:'#e7c578',f:'#e5dbc0',s:'#8b9d8c',k:'#344b42',w:'#8ac6d3',g:'#8cbaa0',q:'#d8949d',p:'#e4d9af',c:'#d9f0df'};
 const panels={b:'#4b3b2b',m:'#465c59',a:'#70572e',f:'#75694c',s:'#304139',k:'#10261f',w:'#214853',g:'#315943',q:'#754250',p:'#b5ad8d',c:'#a0b5aa'};
 return {...base,...c.finish(),construction:'excursion-v1',detail:true,detailScale:.62,blueprint:item.id,anchors,surfaceState:v.surface,inks,panels,animated:p.motion!=='still',emissive:false,floor:false,sway:0,lift:0};
}
