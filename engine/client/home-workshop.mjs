import {ObjectCanvas} from './object-canvas.mjs';
import {nestPose,nestForeground,NEST_MARGIN} from './nest-routines.mjs';
// Individual blueprints: roof structure, wall joinery, floor, glazing, entry and
// furnishings belong to each object. These replace the old stretched silhouettes.
export const HOME_BLUEPRINTS={
 dog_house:{w:70,h:43,roof:'shingle',wall:'plank',door:[26,25,19,15],windows:[],props:['bowl','nameplate'],roofInk:'#b57861',shelter:true},
 shed:{w:86,h:53,roof:'corrugated',wall:'board',door:[30,29,23,20],windows:[[12,30,12,10]],props:['tools','barrel'],roofInk:'#87999b',shelter:true},
 mud_hut:{w:82,h:48,roof:'thatch',wall:'clay',door:[30,29,22,15],windows:[[13,29,12,9],[58,29,11,9]],props:['pots','reeds'],roofInk:'#c9b472',shelter:true},
 wooden_cottage:{w:98,h:59,roof:'shingle',wall:'timber',door:[39,33,23,22],windows:[[15,33,17,13],[68,33,16,13]],props:['chimney','flowers','mail'],roofInk:'#839e8f',shelter:true},
 stone_house:{w:96,h:58,roof:'slate',wall:'stone',door:[38,32,24,22],windows:[[15,33,15,12],[68,33,15,12]],props:['chimney','lantern','step'],roofInk:'#9096b2',shelter:true},
 barn:{w:108,h:62,roof:'gambrel',wall:'redboard',door:[35,32,38,26],windows:[[15,36,12,10],[81,36,12,10]],props:['loft','hay','vane'],roofInk:'#9d967b',shelter:true},
 greenhouse:{w:108,h:58,roof:'glass',wall:'glass',door:[44,31,23,23],windows:[],props:['plants','bench','pots'],roofInk:'#a1c3bd',shelter:true},
 gazebo:{w:106,h:54,roof:'pagoda',wall:'posts',door:[34,30,40,20],windows:[],props:['lattice','curtains','flowers'],roofInk:'#ac9687',shelter:true},
 treehouse:{w:104,h:71,roof:'shingle',wall:'timber',door:[40,30,22,21],windows:[[18,31,15,12],[70,31,14,12]],props:['branches','ladder','rope'],roofInk:'#a9ad72',shelter:true},
 birdhouse:{w:62,h:54,roof:'shingle',wall:'plank',door:[23,25,16,12],windows:[],props:['pole','perch'],roofInk:'#a9b77a',shelter:true,maxStage:'duckling'},
 lighthouse:{w:76,h:80,roof:'beacon',wall:'tower',door:[26,56,23,20],windows:[[27,36,19,12]],props:['beacon','stairs','rope'],roofInk:'#a6aeb1',shelter:true},
 basic_nest:{w:66,h:29,nest:'twig',lining:'grass',props:['feather','leaf'],shelter:false},
 cozy_nest:{w:76,h:35,nest:'braid',lining:'wool',props:['pillow','quilt','leaf'],shelter:false},
 deluxe_nest:{w:84,h:43,nest:'willow',lining:'quilt',props:['canopy','pillow','quilt','lantern'],shelter:true},
 nest_premium:{w:88,h:44,nest:'wicker',lining:'velvet',props:['canopy','pillow','quilt','curtains'],shelter:true},
 golden_nest:{w:90,h:44,nest:'gold',lining:'velvet',props:['canopy','pillow','quilt','jewels'],shelter:true},
 bed_small:{w:78,h:40,bed:'pine',lining:'patchwork',props:['pillow','quilt','carving'],shelter:false},
 bed_king:{w:100,h:49,bed:'fourposter',lining:'velvet',props:['pillow','quilt','canopy','curtains'],shelter:false},
 cozy_bed:{w:86,h:43,bed:'round',lining:'wool',props:['pillow','quilt','book'],shelter:false},
};
const has=(p,key)=>p.props.includes(key),hash=s=>[...s].reduce((n,c)=>(Math.imul(n,31)+c.charCodeAt(0))>>>0,7);
function plankWall(c,x,y,w,h,kind){
 c.rect(x,y,w,h,'b',true);
 if(kind==='stone'){
  for(let j=0;j<h;j+=3){c.line(x+1,y+j,x+w-2,y+j,'_','s');for(let i=(j/3)%2?7:2;i<w-2;i+=11){c.line(x+i,y+j,x+i,Math.min(y+j+2,y+h-2),'|','s');c.put(x+i+3,y+j+1,".:'",'f');}}
 }else if(kind==='clay'){
  for(let j=2;j<h-1;j+=3)for(let i=2;i<w-3;i+=8)c.put(x+i,y+j,(j+i)%2?'~._':'_..','s');c.line(x,y+h-2,x+w-1,y+h-2,'=','f');
 }else{
  for(let i=3;i<w-2;i+=5){c.line(x+i,y+1,x+i,y+h-2,'|','s');for(let j=2;j<h-1;j+=7)c.put(x+i-2,y+j,'o','k');}
  for(let j=3;j<h-2;j+=8)for(let i=5;i<w-4;i+=13)c.put(x+i,y+j,'(=)','s');
  if(kind==='timber'){c.line(x,y+1,x+w-1,y+h-2,'\\','f');c.line(x,y+h-2,x+w-1,y+1,'/','f');c.line(x+w/2,y,x+w/2,y+h-1,'|','f');}
  c.line(x,y+h-2,x+w-1,y+h-2,'=','f');
 }
}
function roof(c,p,t,ctx){
 const W=p.w,top=p.roof==='beacon'?3:7,left=7,right=W-8,base=p.roof==='beacon'?12:p.door[1]-4,mid=W/2;
 let edge=[[left,base],[mid,top],[right,base]];
 if(p.roof==='corrugated')edge=[[left,top+5],[right,top+10],[right,base],[left,base]];
 if(p.roof==='gambrel')edge=[[left,base],[mid-26,top+7],[mid,top],[mid+26,top+7],[right,base]];
 if(p.roof==='slate')edge=[[left,base],[mid-11,top+3],[mid+11,top+3],[right,base]];
 if(p.roof==='pagoda')edge=[[left-3,base-3],[left+8,base-1],[mid-16,top+6],[mid,top],[mid+16,top+6],[right-8,base-1],[right+3,base-3],[right+3,base+1],[left-3,base+1]];
 if(p.roof==='thatch')edge=Array.from({length:17},(_,i)=>{const a=Math.PI-i*Math.PI/16;return [mid+Math.cos(a)*(right-left)/2,base-Math.sin(a)*(base-top)];});
 const span=y=>{const xs=[];for(let i=0;i<edge.length;i++){const a=edge[i],b=edge[(i+1)%edge.length];if(y>=Math.min(a[1],b[1])&&y<=Math.max(a[1],b[1])){if(a[1]===b[1])xs.push(a[0],b[0]);else xs.push(a[0]+(b[0]-a[0])*(y-a[1])/(b[1]-a[1]));}}return xs.length?[Math.round(Math.min(...xs)),Math.round(Math.max(...xs))]:null;};
 for(let y=top;y<=base;y++){
  const bounds=span(y);if(!bounds)continue;const [a,b]=bounds;c.solid(a,y,b-a+1,1,'r');c.line(a,y,b,y,p.roof==='thatch'?'/':'_','r');
  for(let x=a+2;x<b-1;x++){
   const n=x+y*3;
   if(p.roof==='thatch')c.put(x,y,'/|/\\'[n%4],n%5?'r':'f');
   else if(p.roof==='corrugated'&&x%4===0)c.put(x,y,'|','f');
   else if(p.roof==='glass'){if(y%4===0||x%7===0)c.put(x,y,'+','f');else if(n%13===0)c.put(x,y,'/','w');}
   else if(y%3===0)c.put(x,y,'_','s');else if((x+(Math.floor(y/3)%2)*3)%6===0)c.put(x,y,'|','s');
  }
  c.put(a,y,'/','f');c.put(b,y,'\\','f');
 }
 c.line(left-2,base+1,right+2,base+1,'=','f');c.line(left-1,base+2,right+1,base+2,'-','s');
 if(p.roof==='gambrel')for(const side of [-1,1])c.line(mid+side*16,top+5,mid+side*27,base-4,side<0?'/':'\\','f');
 if(p.roof==='pagoda'){c.put(left-3,base-1,'\\__','f');c.put(right,base-1,'__/','f');c.put(mid-3,top-3,'_o_','a');}
 if(ctx.season==='winter'){
  for(let i=1;i<edge.length;i++)c.line(edge[i-1][0],edge[i-1][1]-1,edge[i][0],edge[i][1]-1,'_','c');
  for(let x=left+4;x<right;x+=9)c.line(x,base+2,x,base+3+(x%3),'v','w');
 }else if(ctx.season==='fall')for(let x=left+5;x<right-5;x+=11)c.put(x,base-1,'<>','a');
 if(/rain|storm|drizzle|sleet/.test(ctx.weather||''))for(const x of [left-2,right+2]){c.put(x,base+3+Math.floor(t*9)%8,"'",'w');c.put(x-2,p.h-3,'~._~','w');}
}
function window(c,x,y,w,h,night,curtain){
 c.rect(x-1,y-1,w+2,h+2,'f',true);c.rect(x,y,w,h,'d',true);
 c.line(x+w/2,y,x+w/2,y+h-1,'|','f').line(x,y+h/2,x+w-1,y+h/2,'-','f');
 for(let j=1;j<h-1;j++){
  c.put(x+1,y+j,j<h*.5?'//':':','l');c.put(x+w-3,y+j,j<h*.5?'//':':','l');
  if(curtain>0){const k=Math.min(Math.floor(w*.35),Math.ceil(curtain*w*.35));for(let i=0;i<k;i++){c.put(x+1+i,y+j,i%2?':':'|','q');c.put(x+w-2-i,y+j,i%2?':':'|','q');}}
 }
 if(night)c.put(x+Math.floor(w*.5)-2,y+h-3,'(*)','a');
 c.line(x-2,y+h+1,x+w+1,y+h+1,'=','f');
}
function door(c,p,pose,night){
 const [x,y,w,h]=p.door,open=Math.max(0,Math.min(1,pose.door||0));
 c.rect(x-1,y-1,w+2,h+1,'f',true);c.solid(x,y,w,h,'d');c.clear(x,y,w,h);
 for(let j=2;j<h;j+=3)c.line(x+1,y+j,x+w-2,y+j,'_','s');
 c.rows([' .----.',' |____|',' /____\\'],x+w-9,y+h-5,'s');
 if(night)c.put(x+w-5,y+3,'(*)','l');
 const leaf=Math.max(2,Math.round(w*(1-open)));
 if(p.roof==='gambrel'){
  const half=Math.max(2,Math.round(w/2*(1-open)));plankWall(c,x,y,half,h,'board');plankWall(c,x+w-half,y,half,h,'board');c.line(x+1,y+2,x+half-2,y+h-3,'\\','f').line(x+w-half+1,y+h-3,x+w-2,y+2,'/','f');
 }else{
  plankWall(c,x,y,leaf,h,p.wall==='stone'?'board':p.wall==='glass'?'glass':p.wall==='clay'?'board':'plank');
  c.put(x+Math.max(1,leaf-3),y+h*.55,'o','a');
  if(leaf>6){c.rect(x+2,y+2,leaf-4,Math.max(3,h*.3|0),'s');c.rect(x+2,y+(h*.55|0),leaf-4,Math.max(3,h*.3|0),'s');}
 }
 c.line(x-2,y+h,x+w+1,y+h,'=','f');c.line(x-3,y+h+1,x+w+2,y+h+1,'_','s');
}
function planter(c,x,y,season,t){
 c.rows(['\\ : : : /',' [======]','  \\____/'],x,y+3,'b');
 for(let i=0;i<3;i++){const dx=Math.round(Math.sin(t+i)*.5);c.line(x+2+i*2,y+3,x+1+i*2+dx,y-1-i%2,'|','g');c.put(x+i*2+dx,y-i%2,season==='winter'?'v':season==='fall'?'<>':'(*)','a');}
}
function quilt(c,x,y,w,h,pose,p){
 const fold=Math.round((pose.blanket||0)*Math.min(6,h/2));c.rect(x,y+fold,w,h-fold,'q',true);
 for(let j=1;j<h-fold-1;j++)for(let i=1;i<w-1;i++){
  if(j%4===0)c.put(x+i,y+fold+j,'-','f');else if(i%7===0)c.put(x+i,y+fold+j,'|','f');
  else if(j%4===2&&i%7===3)c.put(x+i,y+fold+j,p.lining==='velvet'?'*':p.lining==='wool'?':':'<>','q');
 }
 c.line(x,y+fold,x+w-1,y+fold,'~','f');
 for(let i=1;i<w;i+=3)c.put(x+i,y+h,"'",'f');
}
function nest(c,p,t,pose,ctx){
 const W=p.w,H=p.h,cx=W/2,cy=H-12,rx=W*.42,ry=9,press=Math.round((pose.press||0)*1.5);
 if(has(p,'canopy')){
  c.line(9,5,9,H-8,'|','f').line(W-10,5,W-10,H-8,'|','f');
  for(let y=3;y<11;y++){const inset=Math.abs(y-3)*1.4;c.line(8+inset,y,W-9-inset,y,y%3?'~':'=','q');}
  c.line(9,4,W-10,4,'=','a');
  if(has(p,'curtains'))for(let y=8;y<H-17;y++){c.put(10,y,'|:|','q');c.put(W-14,y,'|:|','q');}
 }
 for(let j=-3;j<=6;j++){
  const r=rx-Math.abs(j)*.65;c.ellipse(cx,cy+j,r,Math.max(2,ry-Math.abs(j)*.7),'~',j>1?'s':'b',true);
  for(let x=Math.round(cx-r+3);x<cx+r-2;x+=3)c.put(x,cy+j,p.nest==='twig'?((x+j)%2?'/':'\\'):p.nest==='gold'?'(o)':p.nest==='wicker'?'#=':'><',j%3?'b':'f');
 }
 c.ellipse(cx,cy-4+press,rx-8,5-press*.4,'-', 'd',true);c.clear(cx-rx+9,cy-7+press,(rx-9)*2,6-press);
 for(let x=cx-rx+10;x<cx+rx-10;x+=4)c.put(x,cy-5+(Math.round(x)%3),p.lining==='grass'?'\\|/':p.lining==='velvet'?'.':':','q');
 if(has(p,'pillow')){const x=cx-17+Math.round((pose.pillow||0)*3);c.rows([' .---------------.','(  :       :      )'," '---------------'"],x,cy-11,'q');}
 if(has(p,'quilt'))quilt(c,cx-12,cy-5,25,8,pose,p);
 if(has(p,'jewels'))for(let x=14;x<W-12;x+=12)c.put(x,cy+3,'<o>','a');
 if(has(p,'leaf'))c.rows(['  .---.',' /; / /'," '---'"],W-16,cy-10,'g');
 if(has(p,'feather'))c.rows(['  /',' /:','//'],12,cy-9,'c');
 if(has(p,'lantern'))c.rows([' _','/o\\','|*|',"'-'"],W-13,11,'l');
 if(p.nest==='twig')for(const side of [-1,1])for(let j=0;j<3;j++)c.line(cx+side*(rx-5),cy+j*2,cx+side*(rx+2),cy-3+j*4,side<0?'/':'\\','f');
 if(pose.straw)for(let i=0;i<5;i++)c.put(cx-10+i*5,cy-2-Math.round(Math.sin(t*4+i)*pose.straw*4),'/','f');
 return {entry:{x:cx,y:cy-4},seat:{x:cx+(pose.u||0)*7,y:cy+press+(pose.v||0)*3},rim:cy+1,capacity:p.nest==='twig'?1:2};
}
function bed(c,p,t,pose,ctx){
 const W=p.w,H=p.h,x=8,y=H-18,w=W-16;
 c.rect(x,y-14,w,15,'b',true);c.line(x+2,y-12,x+w-3,y-12,'=','f');
 for(let i=x+6;i<x+w-5;i+=7){c.line(i,y-11,i,y-2,'|','s');c.put(i-1,y-9,'(o)','f');}
 if(has(p,'carving')){c.put(W/2-9,y-10,'<~ o ~><~ o ~>','a');c.put(W/2-4,y-6,'<><><>','f');}
 if(p.bed==='fourposter'){
  for(const px of [x-1,x+w]){c.line(px,5,px,H-3,'|','f');c.put(px-1,3,'(o)','a');}
  c.line(x,5,x+w,5,'=','q');for(let py=6;py<y-7;py++){c.put(x+1,py,'|:|','q');c.put(x+w-3,py,'|:|','q');}
 }
 c.rect(x-1,y,w+2,12,'s',true);c.ellipse(W/2,y,w/2,3,'~','q',true);
 c.rows([' .-------------.','(  .       .    )'," '-------------'"],x+7+Math.round((pose.pillow||0)*2),y-4,'q');
 quilt(c,x+3,y+1,w-6,10,pose,p);c.line(x-1,y+11,x+w,y+11,'=','f');
 for(const px of [x+2,x+w-3]){c.rows(['|::|','|__|'],px,H-5,'b');}
 if(has(p,'book'))c.rows([' .----.','/ :  /|','+----+/',"'----'"],W-15,H-6,'f');
 return {entry:{x:W/2,y:y+6},seat:{x:W/2,y:y+3},rim:y+9,capacity:p.bed==='fourposter'?2:1};
}
export function homeSprite(base,item,time,{motion=true,state={},interaction=null,context={},pose={}}={}){
 const p=HOME_BLUEPRINTS[item.id];if(!p)return null;
 const routine=interaction?.phase==='act'&&!interaction.paused?interaction.residence?.routine:null;
 const scored=p.nest?nestPose(routine,motion):null;
 const pad=p.nest?NEST_MARGIN:{x:0,y:0},surface=new ObjectCanvas(p.w+pad.x*2,p.h+pad.y),c=surface.view(pad.x,pad.y);
 const t=motion?(scored?routine.elapsed:time):0,night=(context.hour??12)<6||(context.hour??12)>=19;
 const active=Boolean(interaction&&!interaction.paused&&['prepare','act','settle'].includes(interaction.phase||'act'));
 pose={...scored,...pose};const progress=interaction?.progress??((t%6)/6),pulse=motion?Math.sin(progress*Math.PI*2):0;
 if(active){
  if(pose.door===undefined)pose.door=interaction?.kind==='rest'?1:.6+.4*pulse;
  if(pose.blanket===undefined)pose.blanket=.45+.35*pulse;
  if(pose.pillow===undefined)pose.pillow=pulse;
  if(pose.straw===undefined)pose.straw=.5+.5*pulse;
 }
 let anchors;
 if(p.nest)anchors=nest(c,p,t,pose,context);
 else if(p.bed)anchors=bed(c,p,t,pose,context);
 else{
  const x=10,y=p.door[1]-3,w=p.w-20,h=p.door[3]+6;
  if(p.wall==='posts'){
   c.solid(x,y,w,h,'d');c.rect(x,y,w,h,'s');for(const xx of [x,x+7,x+w-8,x+w-1]){c.line(xx,y,xx,y+h-1,'|','f');c.put(xx-1,y+h,'[=]','b');}
  }else if(p.wall==='tower'){
   c.rect(19,22,p.w-38,p.h-26,'b',true);for(let yy=25;yy<p.h-5;yy+=6){c.line(20,yy,p.w-21,yy,'=','r');for(let xx=22;xx<p.w-22;xx+=9)c.put(xx,yy+3,':','s');}
  }else if(p.wall==='glass'){
   c.rect(x,y,w,h,'w',true);for(let xx=x+1;xx<x+w;xx+=8)c.line(xx,y,xx,y+h-1,'|','f');for(let yy=y+1;yy<y+h;yy+=5)c.line(x,yy,x+w-1,yy,'-','f');
   for(let xx=x+4;xx<x+w-5;xx+=12)planter(c,xx,p.h-10,context.season,t);
  }else plankWall(c,x,y,w,h,p.wall);
  roof(c,p,t,context);
  for(const win of p.windows)window(c,...win,night,pose.curtain??(night?.6:0));
  if(p.wall!=='posts')door(c,p,pose,night);
  if(has(p,'chimney')){c.rect(p.w-28,3,10,p.door[1]-10,'s',true);for(let yy=5;yy<p.door[1]-7;yy+=3)c.put(p.w-27,yy,'_|__|_|','b');c.line(p.w-29,3,p.w-18,3,'=','f');if(night||context.season==='winter')c.put(p.w-25+Math.floor(t*2)%2,Math.floor(t*2)%2,'~.','c');}
  if(has(p,'flowers')){planter(c,12,p.door[1]+p.door[3]-4,context.season,t);planter(c,p.w-23,p.door[1]+p.door[3]-4,context.season,t);}
  if(has(p,'nameplate')){c.rect(25,18,21,4,'f',true);c.put(29,19,'C H E E S E','a');}
  if(has(p,'bowl'))c.rows(['.------.',"\\:____:/"],p.w-14,p.h-3,'w');
  if(has(p,'barrel')){c.ellipse(p.w-13,p.h-10,7,3,'=','b',true);c.rect(p.w-20,p.h-10,15,8,'b',true);c.line(p.w-20,p.h-7,p.w-6,p.h-7,'=','k');c.ellipse(p.w-13,p.h-3,7,2,'=','b');}
  if(has(p,'tools')){c.rows(['T    /|','|   / |','|  /  J'],p.w-27,p.h-15,'k');}
  if(has(p,'pots'))c.rows([' _   __','(o) (__)','|:| |::|',"'-' '--'"],p.w-19,p.h-6,'a');
  if(has(p,'reeds')){for(let i=0;i<5;i++){c.line(10+i, p.h-5,9+i*2,p.h-17-i%2,'/','g');c.put(9+i*2,p.h-18-i%2,'!','a');}c.put(11,p.h-9,'===','b');}
  if(has(p,'bench')){c.rect(15,p.h-8,p.w-30,3,'b',true);for(const xx of [18,p.w-20])c.line(xx,p.h-5,xx,p.h-2,'|','f');}
  if(has(p,'lattice'))for(const xx of [11,p.w-32]){c.rect(xx,p.h-14,22,9,'b');for(let j=1;j<8;j++)for(let i=1;i<21;i++)if((i+j)%4===0||(i-j+8)%4===0)c.put(xx+i,p.h-14+j,(i+j)%4===0?'/':'\\','f');}
  if(has(p,'curtains'))for(const side of [-1,1]){
   const xx=side<0?18:p.w-24;
   for(let j=0;j<12;j++){const tuck=j>6?Math.min(3,j-6):0;c.put(xx+side*tuck,p.door[1]+j,'|:|','q');}
   c.put(xx-1+side*3,p.door[1]+10,'-o-','a');
  }
  if(has(p,'loft')){c.rect(p.w/2-9,21,18,7,'d',true);c.line(p.w/2-9,27,p.w/2+8,21,'/','f');}
  if(has(p,'hay'))c.rows([' /||||\\','/|/||/|\\','[======]'],8,p.h-5,'a');
  if(has(p,'vane'))c.rows(['   >','--(o)--','   |'],p.w/2-3,1,'a');
  if(has(p,'branches')){c.line(16,50,9,63,'/','b').line(16,53,28,67,'\\','b').line(p.w-17,49,p.w-8,62,'\\','b');}
  if(has(p,'ladder')){for(const xx of [46,57])c.line(xx,52,xx,p.h-2,'|','b');for(let yy=54;yy<p.h-2;yy+=3)c.line(46,yy,57,yy,'=','f');}
  if(has(p,'pole')){c.rect(28,40,6,p.h-42,'b',true);c.put(24,p.h-2,'__|__|__','s');}
  if(has(p,'perch'))c.line(20,39,43,39,'=','f');
  if(has(p,'lantern'))c.rows(['  |',' .-.',' |*|'," '-'"],p.door[0]-6,p.door[1]+2,'l');
  if(has(p,'beacon')){c.rect(15,13,p.w-30,10,'w',true);c.line(14,23,p.w-15,23,'=','k');c.put(p.w/2-4,17,night?'<<<(*)>>>':' --(o)--','l');}
  if(has(p,'stairs'))for(let j=0;j<3;j++)c.line(p.door[0]-j*2,p.h-4+j,p.door[0]+p.door[2]+j*2,p.h-4+j,'=','s');
  if(has(p,'rope')){const xx=p.w-19,yy=p.h-12;c.line(xx,yy-6,xx,yy,'|','a');c.ellipse(xx,yy+3,6,3,'~','a');c.ellipse(xx,yy+3,3,2,'~','a');}
  if(has(p,'step'))c.rect(p.door[0]-4,p.h-4,p.door[2]+8,3,'s',true);
  if(has(p,'mail'))c.rows([' /__\\',' |o |',' |__|'],p.w-8,p.h-8,'b');
  anchors={entry:{x:p.door[0]+p.door[2]/2,y:p.door[1]+p.door[3]},seat:{x:p.door[0]+p.door[2]/2,y:p.door[1]+p.door[3]-2},opening:{x:p.door[0],y:p.door[1],w:p.door[2],h:p.door[3]},capacity:p.door[2]>30?3:2};
 }
 // Surface wear follows actual object state, with drip trails below the eaves.
 if((state.wetness||0)>.2){for(let i=0;i<6;i++){const x=8+(hash(item.id)+i*13)%(p.w-16),y=(p.nest||p.bed?p.h-12:p.door[1]-1)+Math.floor(t*7+i*3)%7;c.put(x,Math.min(p.h-2,y),"'",'w');}}
 if((state.dirt||0)>.3)for(let i=0;i<8;i++)c.put(9+(hash(item.id)+i*11)%(p.w-18),p.h-4-i%2,'.:','s');
 if((state.condition??1)<.5)c.rows(p.nest?['/ /'," ' "]:[' /','<',' \\'],Math.round(p.w*.27),p.nest?p.h-12:p.door?.[1]+4||p.h-12,'s');
 if((state.bond||0)>.6)c.put(p.w/2-2,p.h-3,'<3','a');
 const loose=scored?nestForeground(p,scored,anchors):null,held=scored?.grip>0?{...loose,grip:scored.grip}:null;
 const foreground=held?null:loose;
 if(foreground)for(let y=0;y<foreground.art.length;y++)for(let x=0;x<foreground.width;x++)if(foreground.art[y][x]!==' ')surface.put(x,y,foreground.art[y][x],foreground.tones[y][x]);
 if(p.nest){for(const key of ['seat','entry'])anchors[key]={x:anchors[key].x+pad.x,y:anchors[key].y+pad.y};anchors.rim+=pad.y;}
 const glyphs=c.finish();glyphs.clipped ||= loose?.clipped||false;
 const body=p.nest==='gold'?'#d8b76a':p.wall==='stone'?'#adb3aa':p.wall==='clay'?'#bc9474':p.wall==='redboard'?'#c58c79':base.body;
 const inks={b:body,f:base.face,s:'#7e8e83',a:base.accent,w:'#a3d2dc',r:p.roofInk||body,q:p.lining==='velvet'?'#ac9dc0':'#c5b99a',d:'#718a83',g:'#8eb798',c:'#e6dfcc',k:'#a2b8b7',l:night?'#f5d98c':'#b2d7db'};
 return {...base,...glyphs,body,inks,panels:{b:'#342e25',r:'#30352e',d:'#112521',q:'#393731',s:'#26332c',w:'#203c3c',f:'#37382d'},detail:true,detailScale:.72,animated:true,active,phase:motion?Math.floor(t*8)%48:0,lift:0,sway:0,construction:'workshop-v1',anchors,foreground,held,shelter:p.shelter,blueprint:item.id,context:{season:context.season||'summer',night}};
}
