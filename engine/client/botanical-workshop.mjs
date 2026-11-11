import {ObjectCanvas} from './object-canvas.mjs';
import BLUEPRINTS from './animation/botanical.json' with {type:'json'};
export {BLUEPRINTS as BOTANICAL_BLUEPRINTS};
const clamp=(n,a=0,b=1)=>Math.max(a,Math.min(b,n));
const mix=(a,b,u)=>a+(b-a)*u;
function polygon(c,points,tone='g',fill=true){
 if(fill)for(let y=Math.ceil(Math.min(...points.map(p=>p[1])));y<=Math.floor(Math.max(...points.map(p=>p[1])));y++){
  const crosses=[];
  for(let i=0;i<points.length;i++){
   const a=points[i],b=points[(i+1)%points.length];
   if((a[1]<=y&&b[1]>y)||(b[1]<=y&&a[1]>y))crosses.push(a[0]+(y-a[1])/(b[1]-a[1])*(b[0]-a[0]));
  }
  crosses.sort((a,b)=>a-b);
  for(let i=0;i+1<crosses.length;i+=2){const x=Math.ceil(crosses[i]),w=Math.floor(crosses[i+1])-x+1;c.clear(x,y,w,1).solid(x,y,w,1,tone);}
 }
 for(let i=0;i<points.length;i++)c.line(...points[i],...points[(i+1)%points.length],null,tone);
}
function oval(c,x,y,rx,ry,tone='g',char='~'){
 for(let yy=Math.ceil(y-ry);yy<=Math.floor(y+ry);yy++){
  const half=rx*Math.sqrt(Math.max(0,1-((yy-y)/ry)**2));
  c.clear(Math.ceil(x-half),yy,Math.floor(x+half)-Math.ceil(x-half)+1,1);
 }
 c.ellipse(x,y,rx,ry,char,tone,true);
}
function leaf(c,x,y,tx,ty,width=5,tone='g',serrated=false){
 const dx=tx-x,dy=ty-y,len=Math.hypot(dx,dy)||1,nx=-dy/len,ny=dx/len,a=[],b=[];
 for(let i=0;i<=12;i++){
  const u=i/12,r=Math.sin(Math.PI*u)*width*(serrated&&i%2?.72:1);
  a.push([x+dx*u+nx*r,y+dy*u+ny*r]);b.push([x+dx*u-nx*r,y+dy*u-ny*r]);
 }
 polygon(c,[...a,...b.reverse()],tone);
 c.line(x,y,tx,ty,null,'l');
 for(const u of [.25,.45,.65,.8]){
  const r=Math.sin(Math.PI*(u+.1))*width*.8;
  for(const sign of [-1,1])c.line(x+dx*u,y+dy*u,x+dx*(u+.11)+nx*r*sign,y+dy*(u+.11)+ny*r*sign,null,'s');
 }
}
function soil(c,x,y,rx,ry,wet=.5){
 oval(c,x,y,rx,ry,'d','_');
 for(let yy=-ry+2;yy<ry-1;yy+=2)for(let xx=-rx+3;xx<rx-2;xx+=5){
  if((xx/rx)**2+(yy/ry)**2<.8)c.put(x+xx,y+yy,wet>.6?':':xx%2?"'":'.','b');
 }
}
function pot(c,p,moisture){
 const x=p.w/2,y=p.h-15,rx=Math.min(25,p.w*.25);
 if(p.container==='pot'){
  polygon(c,[[x-rx,y-3],[x+rx,y-3],[x+rx-5,p.h-5],[x-rx+5,p.h-5]],'b');
  for(let xx=-rx+6;xx<rx-5;xx+=7)c.line(x+xx,y,x+xx*.8,p.h-7,'|','s');
  c.line(x-rx+6,p.h-7,x+rx-6,p.h-7,'_','f');soil(c,x,y-3,rx,4,moisture);
  c.line(x-rx,y-1,x+rx,y-1,'=','f');c.line(x-rx,y+1,x+rx,y+1,'-','b');
  c.put(x-6,y+4,'< /\\ >','a');c.ellipse(x,p.h-4,rx-2,2,'_','b');
 }else if(p.container==='dish'){
  polygon(c,[[x-36,y+5],[x+36,y+5],[x+30,p.h-4],[x-30,p.h-4]],'p');
  c.line(x-31,p.h-5,x+31,p.h-5,'=','f');soil(c,x,y+3,35,4,moisture);
  for(const dx of [-26,26])c.put(x+dx-2,p.h-3,'[__]','k');
 }else if(p.container==='bed')soil(c,x,p.h-5,p.w*.39,3,moisture);
}
function stem(c,x,y,tx,ty,bend=0,tone='g',thick=1){
 let last=[x,y];
 for(let i=1;i<=18;i++){
  const u=i/18,next=[mix(x,tx,u)+Math.sin(Math.PI*u)*bend,mix(y,ty,u)];
  if(thick>1)c.beam(...last,...next,thick,tone);else c.line(...last,...next,null,tone);
  last=next;
 }
}
function bloom(c,x,y,kind,size,opening,tone='p',turn=0){
 const rx=size,ry=size*.58,open=clamp(opening);
 if(open<.22){
  polygon(c,[[x,y-ry],[x+rx*.4,y],[x+rx*.2,y+ry],[x-rx*.2,y+ry],[x-rx*.4,y]],tone);
  c.put(x-2,y+ry,'\\|/','g');c.line(x,y-ry+2,x,y+ry-1,':','f');return;
 }
 if(kind==='tulip'){
  const r=rx*(.55+.45*open);
  polygon(c,[[x-r,y-ry],[x-r*.25,y-ry*.5],[x,y-ry*1.2],[x+r*.3,y-ry*.45],[x+r,y-ry],[x+r*.8,y+ry*.45],[x+r*.4,y+ry],[x-rx*.4,y+ry],[x-r*.8,y+ry*.4]],tone);
  for(const side of [-1,1])stem(c,x+side*r*.35,y+ry-1,x+side*r*.55,y-ry+3,-side*2,'f');
  c.line(x,y+ry-1,x,y-ry*.4,'|','a');return;
 }
 if(kind==='rose'){
  const edge=[];
  for(let j=0;j<48;j++){const a=j*Math.PI/24,r=.87+.13*Math.cos(a*7);edge.push([x+Math.cos(a)*rx*r,y+Math.sin(a)*ry*r]);}
  polygon(c,edge,tone);
  // Offset folds spiral inward, ending in rolled lips.
  for(let layer=0;layer<3;layer++)for(let petal=0;petal<5-layer;petal++){
   const r=1-layer*.27,a=petal*Math.PI*2/(5-layer)+layer*.8;
   let prev;
   for(let j=0;j<=14;j++){
    const u=j/14,theta=a+u*1.75,rr=r*(.67+.2*Math.sin(u*Math.PI));
    const next=[x+Math.cos(theta)*rx*rr,y+Math.sin(theta)*ry*rr];
    if(prev)c.line(...prev,...next,null,j<3?'r':'f');prev=next;
   }
   c.line(...prev,prev[0]-Math.cos(a+1.75)*2,prev[1]-Math.sin(a+1.75)*2,null,'r');
  }
  c.put(x-2,y,'(@)','f');return;
 }
 if(kind==='bell'){
  const r=rx*(.25+.75*open);
  polygon(c,[[x-r*.5,y-ry],[x+r*.5,y-ry],[x+r*.7,y+ry*.5],[x+r,y+ry],[x+r*.4,y+ry*.7],[x,y+ry],[x-r*.4,y+ry*.7],[x-r,y+ry],[x-r*.7,y+ry*.5]],tone);
  for(const side of [-1,0,1])stem(c,x+side*r*.25,y-ry+1,x+side*r*.55,y+ry-2,side*r*.1,'f');
  for(const d of [-1,1])c.put(x+d*r*.3,y+ry,'o','a');return;
 }
 const count=kind==='star'?7:kind==='sunflower'?14:10;
 for(let i=0;i<count;i++){
  const a=i*Math.PI*2/count+turn,outer=kind==='star'?1.15:1,inner=.4;
  const tip=[x+Math.cos(a)*rx*outer,y+Math.sin(a)*ry*outer];
  const side=[-Math.sin(a)*rx*.18,Math.cos(a)*ry*.18],base=[x+Math.cos(a)*rx*inner,y+Math.sin(a)*ry*inner];
  polygon(c,[base,[mix(base[0],tip[0],.5)+side[0],mix(base[1],tip[1],.5)+side[1]],tip,[mix(base[0],tip[0],.5)-side[0],mix(base[1],tip[1],.5)-side[1]]],tone==='rainbow'?['p','a','q','l','w','v','r'][i%7]:tone);
  c.line(...base,...tip,null,'f');
 }
 oval(c,x,y,rx*(kind==='sunflower'?.45:.24),ry*(kind==='sunflower'?.47:.3),'a','o');
 if(kind==='sunflower')for(let j=0;j<34;j++){
  const angle=j*2.399,r=Math.sqrt(j/34)*rx*.39;
  c.put(x+Math.cos(angle)*r,y+Math.sin(angle)*r*.58,j%3?'o':'.','k');
 }else c.put(x-1,y,'o','k');
}
function flower(c,p,t,env){
 const W=p.w,H=p.h,base=H-(p.container==='pot'?19:7),cx=W/2;
 let stems;
 const shape=p.shape;
 if(shape==='rose_bush')stems=[[-24,-31,'rose',11],[0,-48,'rose',13],[25,-37,'rose',12],[-10,-22,'rose',8],[15,-16,'rose',7]];
 else if(shape==='tulip_cluster')stems=[[-25,-33,'tulip',9],[-11,-45,'tulip',10],[8,-38,'tulip',10],[25,-29,'tulip',9]];
 else if(shape==='pot_flowers')stems=[[-22,-30,'daisy',12],[-3,-43,'daisy',13],[22,-33,'daisy',11]];
 else if(shape==='lavender_bush'){
  for(let i=0;i<13;i++){
   const dx=(i-6)*5,ty=base-25-(6-Math.abs(i-6))*4,tx=cx+dx+env.breeze;
   stem(c,cx+dx*.5,base,tx,ty,dx*.15);
   leaf(c,cx+dx*.75,base-10,tx+(i%2?8:-8),base-20,2,'g');
   for(let j=0;j<5;j++){const y=ty+j*3,r=1+j*.35;c.put(tx-r,y,'(o)','v');c.put(tx+1,y+1,':','p');}
  }
  return {contact:{x:cx,y:base-12},flower:{x:cx,y:base-40},soil:{x:cx,y:base},entry:{x:cx,y:H-3}};
 }else{
  const kind=shape.includes('tulip')?'tulip':shape.includes('rose')?'rose':shape.includes('sunflower')?'sunflower':shape==='dream_bell'?'bell':shape==='golden_star'?'star':'daisy';
  stems=[[0,-(base-20),kind,kind==='sunflower'?20:kind==='rose'?15:15]];
  if(shape==='double_bloom')stems=[[-15,-31,'rose',12],[12,-43,'daisy',15]];
  if(shape==='wildflower')stems=[[-11,-32,'daisy',10],[11,-43,'daisy',10],[-19,-18,'daisy',6]];
  if(shape==='dream_bell')stems=[[-15,-35,'bell',11],[10,-47,'bell',12],[24,-26,'bell',9]];
 }
 let tip={x:cx,y:20};
 for(const [i,[dx,dy,kind,size]]of stems.entries()){
  const rootX=cx+dx*.32,tx=cx+dx+env.breeze*(1+i*.13),ty=base+dy*(.78+env.growth*.22)+env.droop*Math.abs(dx*.2+5);
  stem(c,rootX,base,tx,ty,dx*.15, 'g',kind==='sunflower'?2:1);
  for(const [u,side]of [[.32,-1],[.57,1]]){
   const x=mix(rootX,tx,u),y=mix(base,ty,u),reach=kind==='sunflower'?17:12;
   leaf(c,x,y,x+side*reach,y-(kind==='tulip'?16:7)+env.droop*5,kind==='tulip'?3:5,'g',kind==='rose');
  }
  if(kind==='rose')for(const u of [.2,.5,.7])c.put(mix(rootX,tx,u)+(u===.5?-2:1),mix(base,ty,u),u===.5?'<':'>','b');
  let open=p.rooted?env.bloom:.85;
  if(shape.includes('tulip'))open*=env.night?.34:1;
  if(shape==='dream_bell')open=env.night?1:.3;
  if(shape==='dandelion'){
   c.ellipse(tx,ty,17,10,'.','c');
   for(let j=0;j<18;j++){const a=j*Math.PI/9;c.line(tx,ty,tx+Math.cos(a)*15,ty+Math.sin(a)*8,':','c');c.put(tx+Math.cos(a)*17,ty+Math.sin(a)*9,'*','c');}
   if(env.wind>.4)for(let j=0;j<3;j++){const u=(t*.13+j*.24)%1;c.put(tx+12+u*13,ty-4-u*6,'+','c');}
   c.put(tx-1,ty,'(o)','b');
  }else bloom(c,tx,ty,kind,size,open,p.color==='rainbow'?'rainbow':p.color==='gold'?'a':p.color==='white'?'c':p.color==='mixed'?['p','q','v'][i%3]:'p',kind==='sunflower'?(env.hour-12)*.018:0);
  if(i===0)tip={x:tx,y:ty};
 }
 if(!p.rooted&&p.container==='none'&&stems.length>1)c.put(cx-3,base,'~==~','b');
 return {contact:{x:cx,y:base-12},flower:tip,soil:{x:cx,y:base},entry:{x:cx,y:H-3}};
}
function canopy(c,x,y,rx,ry,shape,env,tone='g'){
 if(env.winter&&shape!=='world')return;
 const flowering=shape.includes('cherry')&&!env.autumn&&!env.summer&&env.bloom>.25;
 const edge=[];
 for(let j=0;j<64;j++){
  const a=j*Math.PI/32,r=.9+.06*Math.sin(a*9)+.035*Math.cos(a*17);
  edge.push([x+Math.cos(a)*rx*r,y+Math.sin(a)*ry*r]);
 }
 polygon(c,edge,flowering?'p':tone);
 // Fans follow twigs; shaded gaps and scalloped edges break up the crown.
 for(let row=0,yy=-ry+4;yy<ry-3;yy+=5,row++)for(let col=0,xx=-rx+4;xx<rx-4;xx+=8,col++){
  const dx=xx+(row%2)*3,dy=yy+(col%3)-1;
  if((dx/rx)**2+(dy/ry)**2>.65)continue;
  const xx0=x+dx,yy0=y+dy;
  if(flowering){
   c.rows([' .o.','o(@)o'," 'o'"],xx0-2,yy0-1,(row+col)%3?'p':'c');
   c.put(xx0+3,yy0+2,'<','l');
  }else if(shape==='bonsai')c.rows(['\\ | /','-\\|/-',' /|\\'],xx0-2,yy0-1,'l');
  else{
   c.put(xx0-2,yy0-1,shape==='willow'?'// /':'<\\/','l');
   c.put(xx0-2,yy0,shape==='world'?'(<>)/':'/|\\>','g');
   c.put(xx0-1,yy0+1,'\\;>','l');c.put(xx0,yy0+2,'/','s');
  }
  if(shape==='orchard_cherry'&&env.summer&&(row+col)%2===0){
   c.put(xx0+1,yy0+1,'/\\','b');c.put(xx0,yy0+2,'o o','r');
  }
 }
 for(let i=-2;i<=2;i++)c.put(x+i*rx*.29-2,y+ry*(.55-Math.abs(i)*.04),'\\/\\/','s');
 if(env.snow>.15)c.line(x-rx*.55,y-ry+1,x+rx*.55,y-ry+1,'_','c');
}
function tree(c,p,t,env){
 const W=p.w,H=p.h,cx=W/2,base=H-(p.container==='dish'?18:6),small=p.shape==='sapling',bonsai=p.shape==='bonsai',world=p.shape==='world',willow=p.shape==='willow';
 const split=base*(bonsai?.58:.52),trunk=small?4:bonsai?7:world?11:9;
 const curve=bonsai?-12:world?5:0;
 polygon(c,[[cx-trunk,base],[cx-trunk*.6,split+4],[cx+curve-3,split-9],[cx+curve+4,split-9],[cx+trunk*.6,split+4],[cx+trunk,base]],'b');
 for(let i=-1;i<=1;i++)stem(c,cx+i*trunk*.6,base-2,cx+curve+i*2,split-7,2,'s');
 for(let yy=split+12;yy<base-4;yy+=6){
  const u=(yy-split)/(base-split),xx=cx+curve*(1-u);
  c.put(xx-trunk*u*.6,yy,'|:','f');c.put(xx+trunk*u*.4,yy+2,'/)','k');c.put(xx-1,yy+3,'~','b');
 }
 c.rows([' /---\\','( (o) )',' \\___/'],cx-3,base-19,'f');
 for(const [dx,dy]of [[-23,0],[-14,3],[15,2],[25,-1]]){
  c.beam(cx,base-5,cx+dx,base+dy,small?2:3,'b');c.line(cx+dx,base+dy,cx+dx+(dx>0?8:-8),base+dy-2,null,'s');
 }
 let branches;
 if(bonsai)branches=[[-24,-21,21,11],[21,-32,25,12],[-5,-42,21,10]];
 else if(small)branches=[[-19,-31,19,13],[18,-43,21,14],[-5,-56,23,14]];
 else if(willow)branches=[[-43,-42,25,16],[-23,-61,29,18],[16,-66,31,19],[43,-47,24,17]];
 else if(world)branches=[[-47,-43,25,16],[47,-43,25,16],[-30,-69,29,17],[30,-69,29,17],[0,-86,31,17]];
 else if(p.shape==='ornamental_cherry')branches=[[-31,-37,25,17],[26,-40,27,18],[-14,-61,29,19],[17,-65,26,17]];
 else branches=[[-35,-41,26,18],[32,-44,29,19],[-16,-66,31,20],[20,-69,28,18]];
 let high={x:cx,y:split};
 for(const [i,[dx,dy,rx,ry]]of branches.entries()){
  const x=cx+dx+env.breeze*(.7+i*.1),y=base+dy;
  const bx=cx+curve,by=split+8+i*2;
  c.beam(bx,by,x,y+ry*.4,small?2:bonsai?3:4,'b');
  c.line(x,y+ry*.4,x-rx*.6,y-ry*.3,'/','s');c.line(x,y+ry*.4,x+rx*.6,y-ry*.3,'\\','s');
  canopy(c,x,y,rx,ry,p.shape,env);
  if(willow&&!env.winter){
   for(let j=0;j<8;j++){
    const xx=x+(j-3.5)*5,start=y+4,end=Math.min(base-8,start+20+(j%3)*6),bend=Math.sin(t*.8+j+i)*env.wind*4;
    stem(c,xx,start,xx+bend,end,bend,'g');
    for(let yy=start+3;yy<end;yy+=4)c.put(xx+bend*(yy-start)/(end-start)-1,yy,'\\/','l');
   }
  }
  if(y<high.y)high={x,y};
 }
 if(world){
  c.rows(['  /\\',' /<>\\','| /\\ |','| \\/ |',' \\__/'],cx-3,base-35,'a');
  for(const [dx,dy]of [[-38,-23],[34,-28],[-18,-49]]){c.line(cx+dx,base+dy-8,cx+dx,base+dy,'|','q');c.put(cx+dx-2,base+dy,'<*>','a');}
 }
 if(env.winter)for(const [dx,dy]of branches)c.put(cx+dx-3,base+dy+7,'___','c');
 return {contact:{x:cx+trunk,y:base-12},flower:high,soil:{x:cx,y:base},entry:{x:cx,y:H-3}};
}
function frond(c,p,t,env){
 const W=p.w,H=p.h,cx=W/2,base=H-(p.container==='pot'?20:6);
 if(p.shape==='rubber_plant'||p.shape==='mint'){
  const mint=p.shape==='mint';
  for(const [i,dx]of [-18,0,19].entries()){
   const top=base-35-i*7,tx=cx+dx+env.breeze;
   stem(c,cx,base,tx,top,dx*.15);
   for(let j=0;j<3;j++){const u=.3+j*.24,x=mix(cx,tx,u),y=mix(base,top,u);
    leaf(c,x,y,x-17+(j%2)*4,y-9, mint?5:7,'g',mint);
    leaf(c,x,y,x+17-(j%2)*3,y-10,mint?5:7,'l',mint);
   }
  }
 }else if(p.shape==='reed'){
  for(const [dx,height]of [[-20,44],[-6,57],[13,48],[24,36]]){
   const tx=cx+dx+env.breeze;stem(c,cx+dx*.6,base,tx,base-height,env.breeze*.5);
   leaf(c,cx+dx*.7,base-9,tx+12,base-height+9,2,'g');
   oval(c,tx,base-height+5,3,9,'b','|');for(let y=base-height-1;y<base-height+12;y+=3)c.put(tx-1,y,':','a');
  }
 }else if(p.shape==='kelp'||p.shape==='pond_weed'){
  for(let n=0;n<5;n++){
   const height=28+(n%3)*12,x=cx+(n-2)*9;
   let last=[x,base];for(let j=1;j<=12;j++){const u=j/12,next=[x+Math.sin(u*6+t*.7+n)*5,base-height*u];c.beam(...last,...next,p.shape==='kelp'?4:2,'g');if(j%3===0)leaf(c,...next,next[0]+(j%2?9:-9),next[1]-5,3,'l');last=next;}
  }
  c.put(cx-6,base,'\\__|__/','b');
 }else{
  for(const [i,[dx,dy]]of [[-43,-23],[-31,-40],[-14,-53],[6,-58],[26,-45],[43,-29]].entries()){
   const tx=cx+dx+env.breeze,ty=base+dy+env.droop*7;
   stem(c,cx,base,tx,ty,dx*.18,'l');
   for(let n=2;n<10;n++){
    const u=n/10,x=mix(cx,tx,u)+Math.sin(Math.PI*u)*dx*.18,y=mix(base,ty,u);
    const length=Math.hypot(dx,dy),nx=-dy/length,ny=dx/length,pinna=Math.sin(u*Math.PI)*9+1;
    leaf(c,x,y,x+nx*pinna+dx*.05,y+ny*pinna+dy*.04,1.1,'g');
    leaf(c,x,y,x-nx*pinna+dx*.05,y-ny*pinna+dy*.04,1.1,'l');
   }
  }
 }
 return {contact:{x:cx,y:base-13},flower:{x:cx,y:base-32},soil:{x:cx,y:base},entry:{x:cx,y:H-3}};
}
function bamboo(c,p,t,env){
 const base=p.h-7,cx=p.w/2;
 for(const [i,[dx,height]]of [[-35,55],[-23,73],[-9,80],[6,70],[24,83],[37,57]].entries()){
  const x=cx+dx,tip=x+env.breeze*(.7+i*.1);
  c.beam(x,base,tip,base-height,3,'g');
  for(let y=base-6;y>base-height+3;y-=12){
   const xx=mix(x,tip,(base-y)/height);c.put(xx-2,y,'[=]','l');c.put(xx,y-4,':','s');
   if(y<base-18)for(const side of [-1,1])leaf(c,xx,y,xx+side*(9+i%3*2),y-6,1.7,'g');
  }
  c.put(x-4,base,'_/|\\_','b');
 }
 return {contact:{x:cx,y:base-15},flower:{x:cx,y:base-63},soil:{x:cx,y:base},entry:{x:cx,y:p.h-3}};
}
function succulent(c,p,t,env){
 const cx=p.w/2,base=p.h-(p.container==='pot'?20:7),barrel=p.shape==='barrel';
 const cy=barrel?base-18:base-27,rx=barrel?22:11,ry=barrel?20:29;
 if(!barrel)for(const [side,y]of [[-1,base-22],[1,base-36]]){
  const arm=cx+side*23;
  polygon(c,[[cx,y-4],[arm-side*4,y-4],[arm-side*4,y-17],[arm+side*4,y-17],[arm+side*4,y+2],[arm,y+5],[cx,y+4]],'g');
  oval(c,arm,y-17,4,4,'g');
  c.line(cx+side*4,y,arm,y,'-','l');c.line(arm,y,arm,y-17,'|','l');
  for(let yy=y-14;yy<y;yy+=5)c.put(cx+side*23-1,yy,'*','f');
 }
 oval(c,cx,cy,rx,ry,'g');
 for(let dx=-rx+4;dx<rx-2;dx+=5){
  const hh=ry*Math.sqrt(1-(dx/rx)**2);
  c.line(cx+dx,cy-hh+2,cx+dx,cy+hh-2,'|','l');
  for(let y=cy-hh+5;y<cy+hh-3;y+=6)c.put(cx+dx-1,y,'*','c');
 }
 if(barrel||env.summer)bloom(c,cx+3,cy-ry+1,'daisy',8,.8,'a');
 return {contact:{x:cx-rx-3,y:base-5},flower:{x:cx,y:cy-ry},soil:{x:cx,y:base},entry:{x:cx,y:p.h-3}};
}
function trap(c,p,t,env){
 const cx=p.w/2,base=p.h-20;
 for(const [i,[dx,dy]]of [[-25,-22],[0,-37],[25,-24]].entries()){
  const x=cx+dx+env.breeze,y=base+dy;stem(c,cx,base,x,y,dx*.2,'g',2);
  leaf(c,cx,base,cx+dx*1.35,base-7,5,'g');
  const closed=(env.insects>.4&&((t+i*5)%19)>14)?1:0;
  if(closed){
   polygon(c,[[x-13,y],[x-8,y-5],[x+7,y-6],[x+13,y],[x+5,y+3],[x-6,y+3]],'g');c.line(x-11,y,x+11,y,'v','p');
  }else{
   polygon(c,[[x-13,y-8],[x-3,y-7],[x,y],[x-11,y+4],[x-16,y-1]],'p');
   polygon(c,[[x+13,y-8],[x+3,y-7],[x,y],[x+11,y+4],[x+16,y-1]],'p');
   for(const side of [-1,1])for(let j=0;j<5;j++)c.put(x+side*(5+j*2),y-7+j%2,'^','l');
   for(const side of [-1,1]){
    c.line(x+side*3,y,x+side*12,y-3,null,'r');
    for(const yy of [-5,-1,2]){c.put(x+side*8,y+yy,side<0?'>':'<','f');c.put(x+side*5,y+yy+1,':','r');}
    c.line(x+side*14,y-6,x+side*15,y,'|','g');
   }
   c.line(x,y-3,x,y+3,'|','g');
  }
 }
 return {contact:{x:cx-18,y:base-3},flower:{x:cx,y:base-37},soil:{x:cx,y:base},entry:{x:cx,y:p.h-3}};
}
function cap(c,x,y,r,h,tone='p'){
 c.beam(x,y+2,x-2,y+h,5,'c');c.put(x-5,y+h,'(___)','b');
 for(let yy=y+5;yy<y+h;yy+=4){c.put(x-2,yy,'|','b');c.put(x,yy+1,':','f');}
 oval(c,x,y+2,r,4,'b','_');
 for(let i=-r+3;i<r-2;i+=4)c.line(x+i,y+1,x+i*.35,y+4,'/','f');
 for(let yy=-Math.round(r*.65);yy<=0;yy++){
  const half=r*Math.sqrt(Math.max(0,1-(yy/(r*.7))**2));c.clear(x-half,y+yy,half*2+1,1).solid(x-half,y+yy,half*2+1,1,tone);
  c.put(x-half,y+yy,'/','f');c.put(x+half,y+yy,'\\','f');
  if(yy%3===0)for(let xx=-half+3;xx<half-3;xx+=7)c.put(x+xx,y+yy,yy%2?'o':':.','c');
 }
 for(let j=-3;j<=3;j++)stem(c,x+j*r*.22,y-1,x+j*r*.12,y-r*.5,j*.4,'f');
 c.line(x-r,y,x+r,y,'~','f');c.put(x-4,y+7,'(===)','c');
}
function fungus(c,p,t,env){
 if(p.shape==='patch'){
  soil(c,p.w/2,p.h-6,42,3,env.moisture);
  cap(c,30,28,18,27,'r');cap(c,68,20,21,34,'p');cap(c,82,43,13,15,'a');cap(c,16,48,10,10,'b');cap(c,49,42,15,16,'p');
  if(env.wetness>.4)for(const [x,y]of [[30,29],[68,21],[82,44]])c.put(x+4,y+(t*3)%8,"'",'w');
 }else{cap(c,p.w/2,23,23,24,'b');c.put(p.w/2-6,49,'=//==','s');}
 return {contact:{x:p.w/2,y:p.h-13},flower:{x:p.w/2,y:25},soil:{x:p.w/2,y:p.h-6},entry:{x:p.w/2,y:p.h-3}};
}
function hedgeBlock(c,x,y,w,h,env){
 polygon(c,[[x,y],[x+w,y],[x+w-3,y+h],[x+3,y+h]],'g');
 c.line(x+1,y+2,x+w-2,y+2,'_','l');
 for(let yy=4;yy<h-3;yy+=4)for(let xx=4;xx<w-7;xx+=7){
  const offset=(yy%3);c.put(x+xx+offset,y+yy,'<\\/','l');c.put(x+xx+offset+1,y+yy+1,'/;>','g');c.put(x+xx+offset,y+yy+2,'/','s');
 }
 for(let xx=5;xx<w-5;xx+=6)c.put(x+xx,y-1,xx%2?'_,':'._','l');
 c.line(x+3,y+h-1,x+w-4,y+h-1,'~','s');
 if(env.snow>.2)c.line(x+3,y,x+w-3,y,'_','c');
}
function hedge(c,p,t,env){
 const H=p.h,W=p.w;
 if(p.shape==='maze'){
  soil(c,W/2,H-13,W*.43,9,env.moisture);
  hedgeBlock(c,12,17,W-24,18,env);
  hedgeBlock(c,14,29,16,43,env);hedgeBlock(c,W-31,29,16,43,env);
  hedgeBlock(c,41,35,57,17,env);hedgeBlock(c,42,47,15,24,env);
  hedgeBlock(c,75,59,35,15,env);hedgeBlock(c,15,H-22,41,17,env);
  hedgeBlock(c,83,H-22,45,17,env);c.put(63,H-9,'| |','b');
 }else{
  for(const x of [22,51,81])c.beam(x,H-19,x-3,H-4,3,'b');
  hedgeBlock(c,7,15,W-14,H-28,env);
  for(let x=16;x<W-12;x+=17)c.put(x,14-(x%3),'_._','l');
 }
 return {contact:{x:W/2,y:H-18},flower:{x:W/2,y:25},soil:{x:W/2,y:H-5},entry:{x:W/2,y:H-3}};
}
function garden(c,p,t,env,context){
 const W=p.w,H=p.h,base=H-7,top=H-29;
 polygon(c,[[8,top],[W-8,top],[W-12,base],[12,base]],'b');
 c.line(9,top+5,W-9,top+5,'=','f');c.line(13,base-3,W-13,base-3,'~','s');
 for(let y=top+9;y<base-3;y+=4)for(let x=19;x<W-23;x+=24){c.put(x,y,'--~~---','f');c.put(x+9,y,'(=)','s');}
 for(const x of [12,W-16]){c.line(x,top+6,x,base-2,'|','f');c.line(x+3,top+6,x+3,base-2,'|','k');}
 soil(c,W/2,top,W*.42,9,env.moisture);
 if(p.shape==='herbs'){
  for(const [i,label]of ['MINT','THYME','BASIL'].entries()){
   const x=26+i*36;
   c.line(x-17,top-6,x-17,top+6,'|','b');
   for(let j=-2;j<=2;j++){const tx=x+j*5+env.breeze*.5,ty=top-15-Math.abs(j%2)*7;stem(c,x+j*3,top,tx,ty,1);
    for(let n=0;n<3;n++){const yy=ty+4+n*5;if(i===1)c.put(tx-4,yy,'<|>','l');else{leaf(c,tx,yy,tx-7,yy-4,i===0?3:4,'g',i===0);leaf(c,tx,yy,tx+7,yy-5,i===0?3:4,'l',i===0);}}
   }
   c.put(x-7,base-7,'['+label+']','c');
  }
 }else if(p.shape==='flowers'){
  for(const [i,[x,y]]of [[24,top-13],[48,top-24],[72,top-16],[97,top-28],[117,top-13]].entries()){
   stem(c,x,top+2,x+env.breeze,y,3);leaf(c,x,top-4,x+(i%2?11:-11),top-10,3,'g');
   bloom(c,x+env.breeze,y,i%2?'tulip':'daisy',10,env.bloom,['p','a','v','q'][i%4]);
  }
 }else{
  const plots=context.living?.garden||[],slots=Math.max(6,plots.length),cols=Math.min(6,slots),rows=Math.ceil(slots/cols);
  for(let i=0;i<slots;i++){
   const x=23+(i%cols)*(W-46)/(cols-1),y=top-1+Math.floor(i/cols)*5/Math.max(1,rows-1),plot=plots[i];
   c.line(x-7,y+3,x+7,y+3,'~','b');
   if(plot?.plant){
    const stage=plot.stage;
    if(stage==='seed')c.put(x-2,y,' . ','b');
    else if(stage==='withered'){stem(c,x,y,x+3,y-5,3,'q');c.put(x+3,y-3,'v','b');}
    else{
     const grown=['harvestable','mature','flowering'].includes(stage),height=grown?12:stage==='sprout'?4:7;
     stem(c,x,y,x,y-height);leaf(c,x,y-2,x-6,y-height+1,3,'g');leaf(c,x,y-3,x+6,y-height,3,'l');
     if(grown){
      if(['rose','tulip','sunflower','golden_flower'].includes(plot.plant))bloom(c,x,y-height,plot.plant==='golden_flower'?'star':plot.plant,5,.9,'p');
      else if(plot.plant==='mint'){leaf(c,x,y-height+3,x-5,y-height-2,2,'g');leaf(c,x,y-height+3,x+5,y-height-2,2,'l');}
      else if(plot.plant==='carrot')c.put(x-2,y-1,'\\V/','a');
      else if(plot.plant==='crystal_plant')c.rows([' /\\','<  >',' \\/'],x-2,y-height-3,'w');
      else c.put(x-2,y-height-2,'(o)','r');
     }
    }
   }
   else c.put(x-2,y,'...','s');
  }
  c.line(14,top-9,14,top-25,'|','b');c.put(10,top-26,'[GROW]','f');
 }
 for(const x of [13,W-16])for(const y of [top+8,base-6])c.put(x,y,'o','k');
 return {contact:{x:W/2,y:top},flower:{x:W/2,y:top-20},soil:{x:W/2,y:top+3},entry:{x:W/2,y:H-3},
  gardenPlots:p.shape==='plot'?(context.living?.garden||[]).map(plot=>({id:plot.id,plant:plot.plant,stage:plot.stage})):[]};
}
function loose(c,p,t,env){
 const W=p.w,H=p.h,cx=W/2,cy=H/2,shape=p.shape;
 if(shape==='pile'){
  for(const [i,[x,y,a,b]]of [[26,27,15,14],[47,29,59,11],[76,28,95,14],[33,35,55,23],[58,37,79,27],[74,35,95,33],[20,34,39,24]].entries())leaf(c,x,y,a+env.breeze*.3,b,7,['q','p','a'][i%3],true);
 }else if(shape.includes('clover')){
  const four=shape==='four_clover';stem(c,cx-5,H-5,cx,cy-3,4);
  for(let i=0;i<(four?4:3);i++){const a=i*Math.PI*2/(four?4:3)-Math.PI/2,x=cx+Math.cos(a)*12,y=cy-6+Math.sin(a)*9;
   polygon(c,[[cx,cy-3],[x-8,y+2],[x-9,y-3],[x-4,y-6],[x,y-3],[x+4,y-6],[x+9,y-3],[x+8,y+2]],'g');c.line(cx,cy-3,x,y-2,null,'l');
  }
  if(four)c.put(cx+17,cy-8,'*','a');
 }else if(shape==='grass'){
  leaf(c,cx-17,H-7,cx+12,8,3,'g');leaf(c,cx-16,H-7,cx+22,17,2,'l');c.put(cx-20,H-5,'__//','b');
 }else if(shape==='needles'){
  c.beam(10,H-9,W-12,13,2,'b');
  for(let i=0;i<6;i++){const x=19+i*6,y=H-12-i*2.7;c.line(x,y,x-9,y-13,'/','g');c.line(x,y,x+11,y+3,'\\','l');}
 }else if(shape==='moss'){
  oval(c,cx,H-11,34,9,'b');oval(c,cx,H-15,34,9,'g');
  for(let row=0;row<4;row++)for(let col=0;col<9;col++){
   const x=12+col*7+(row%2)*2,y=H-10-row*4;
   if((x+1-cx)**2/1156+(y-(H-15))**2/81<.75){c.put(x,y,'\\|/','l');c.put(x+1,y-1,'|','g');c.put(x,y-2,'v^','l');}
  }
 }else if(shape==='lily'){
  const outline=[[cx,cy]];
  for(let a=1.27;a<=Math.PI*2+.58;a+=.12)outline.push([cx+Math.cos(a)*33,cy+Math.sin(a)*15]);
  polygon(c,outline,'g');
  for(let a=1.4;a<Math.PI*2+.5;a+=.5){
   const tx=cx+Math.cos(a)*29,ty=cy+Math.sin(a)*12;c.line(cx,cy,tx,ty,null,'l');
   c.line(mix(cx,tx,.55),mix(cy,ty,.55),cx+Math.cos(a+.2)*25,cy+Math.sin(a+.2)*11,null,'s');
  }
  oval(c,cx-10,cy-5,2,1,'w','o');
 }else if(shape==='mint_pair'){
  leaf(c,14,H-9,41,7,10,'g',true);leaf(c,27,H-6,65,16,10,'l',true);c.line(10,H-8,31,H-7,'_','b');
 }else if(shape==='maple'||shape==='ginkgo'||shape==='oak_leaf'){
  const x=cx,y=H-10;
  const points=shape==='maple'?[[x,y],[10,cy+4],[23,cy-3],[14,12],[31,17],[x,5],[x+10,17],[W-15,11],[W-23,cy],[W-9,cy+5],[x+8,y-2]]:
   shape==='ginkgo'?[[x,y],[8,20],[18,10],[31,6],[x,12],[x+9,6],[W-18,10],[W-8,20]]:
   [[x-5,y],[13,H-15],[9,H-24],[19,H-27],[14,17],[27,17],[24,9],[x,6],[x+10,9],[x+9,17],[W-13,16],[W-18,27],[W-9,31],[W-15,H-14],[x+5,y]];
  polygon(c,points,'p');c.line(x,H-4,x,9,'|','a');
  for(let i=1;i<points.length-1;i+=2)c.line(x,y-3,...points[i],null,'f');
 }else if(shape.includes('petal')){
  const long=shape==='long_petal',notch=shape==='notched_petal',rx=long?17:22,ry=long?17:12;
  if(shape==='rose_petal')polygon(c,[[cx,cy+13],[cx-23,cy+2],[cx-21,cy-8],[cx-11,cy-13],[cx,cy-8],[cx+10,cy-11],[cx+24,cy-2],[cx+15,cy+7]],'p');
  else if(notch)polygon(c,[[cx,cy+14],[cx-24,cy-2],[cx-15,cy-12],[cx-4,cy-9],[cx,cy-3],[cx+4,cy-9],[cx+17,cy-11],[cx+24,cy]],'p');
  else oval(c,cx,cy,rx,ry,'p');
  for(const dx of [-12,-5,3,11])stem(c,cx,cy+ry-1,cx+dx,cy-ry+4,dx*.3,'f');
  if(p.color==='gold')c.put(cx+8,cy-7,'*','a');
 }else leaf(c,11,H-7,W-11,8,13,'g',true);
 return {contact:{x:cx,y:cy},flower:{x:cx,y:cy},soil:{x:cx,y:H-4},entry:{x:cx,y:H-3}};
}
function food(c,p,t,env){
 const W=p.w,H=p.h,cx=W/2;
 if(p.shape==='lettuce'){
  for(const [dx,dy,width]of [[0,0,17],[-12,6,13],[13,5,13],[-5,11,12],[9,12,11]])leaf(c,cx,H-6,cx+dx,8+dy,width,'g',true);
  c.put(cx-5,H-4,'[===]','c');
 }else if(p.shape==='kernels'){
  for(const [x,y]of [[22,14],[39,11],[53,18],[32,26],[48,28],[15,28]]){
   polygon(c,[[x-7,y-4],[x+5,y-5],[x+8,y],[x+4,y+6],[x-5,y+5],[x-8,y]],'a');
   c.put(x-4,y-2,'(___)','c');c.put(x-5,y,'|: :|','f');c.put(x-3,y+2,'\\ :/','q');c.put(x-2,y+4,'[v]','b');
  }
 }else if(p.shape==='peas'){
  polygon(c,[[9,22],[17,13],[59,12],[70,18],[62,26],[17,29]],'g');
  for(const [x,y]of [[22,20],[35,19],[49,19],[61,32]]){
   oval(c,x,y,6,5,'l','~');c.put(x-3,y-2,".'",'c');c.put(x-2,y+2,"'--",'g');c.put(x+2,y,';','s');
  }
  c.line(17,27,61,25,'~','f');c.put(69,18,'~','g');
 }else if(p.shape==='grape_halves'){
  for(const [x,y]of [[24,18],[53,23]]){
   oval(c,x,y,16,12,'p');oval(c,x,y-1,13,9,'q');
   for(let a=0;a<Math.PI*2;a+=.65)c.line(x+Math.cos(a)*5,y-1+Math.sin(a)*3,x+Math.cos(a)*11,y-1+Math.sin(a)*7,':','f');
   c.put(x-5,y,'(<>)','b');c.put(x+2,y-4,'(<>)','b');c.put(x-9,y-6,".'''",'c');c.put(x+7,y+3,'..','w');
  }
  c.put(39,8,'_/>','b');
 }else{
  const cy=H/2+1;
  polygon(c,[[cx-18,cy-6],[cx-12,cy-12],[cx+10,cy-12],[cx+18,cy-6],[cx+15,cy+4],[cx+7,cy+12],[cx,cy+15],[cx-9,cy+10]],'r');
  for(let row=0;row<5;row++)for(let col=-2;col<=2;col++){
   const dx=col*6+(row%2)*2,dy=-6+row*4;if(Math.abs(dx)<17-row*2)c.put(cx+dx-1,cy+dy,'v','a');
  }
  c.put(cx-12,cy-7,".''",'c');c.put(cx-14,cy-4,':','p');
  for(const dx of [-13,0,13])leaf(c,cx,cy-10,cx+dx,cy-15+Math.abs(dx)*.35,3,'g');
  stem(c,cx,cy-11,cx+3,5,2,'b');
 }
 return {contact:{x:cx,y:H/2},entry:{x:cx,y:H-3}};
}
function bulb(c,p,t,env){
 const cx=p.w/2,cy=p.h*.6;
 polygon(c,[[cx-19,cy+7],[cx-21,cy-2],[cx-13,cy-12],[cx-3,cy-20],[cx+4,cy-18],[cx+17,cy-8],[cx+20,cy+3],[cx+12,cy+10],[cx-10,cy+11]],'b');
 for(const dx of [-10,-4,5,12])stem(c,cx+dx,cy+9,cx,cy-17,dx*.5,'f');
 for(const dx of [-11,-5,3,10])stem(c,cx+dx,cy+10,cx+dx*1.6,p.h-3,dx*.5,'c');
 leaf(c,cx,cy-18,cx+12,5,3,'g');
 return {contact:{x:cx,y:cy},entry:{x:cx,y:p.h-3}};
}
const DRAW={flower,tree,frond,bamboo,succulent,trap,fungus,hedge,garden,loose,food,bulb};
function surfaceWeather(c,p,state){
 // Work on occupied surfaces only. No floating grime, detached droplets or
 // invented "using" animation on a stationary seed, food or picked specimen.
 const surfaces=new Map();
 for(const f of c.fills)for(let x=Math.max(0,f.x);x<Math.min(c.w,f.x+f.w);x++)surfaces.set(f.y*c.w+x,f.tone);
 let spots=[...surfaces].filter(([key,tone])=>{
  const x=key%c.w,y=Math.floor(key/c.w);
  return x>2&&x<c.w-3&&y>2&&y<c.h-3&&surfaces.has(key-1)&&surfaces.has(key+1)&&surfaces.has(key+c.w)&&surfaces.has(key-c.w);
 });
 if(!spots.length)for(let y=3;y<c.h-3;y++)for(let x=3;x<c.w-3;x++){
  if(c.art[y][x]!==' ')spots.push([y*c.w+x,c.tones[y][x]]);
 }
 if(state.wetness>.35){
  const leaves=spots.filter(([,tone])=>'glprva'.includes(tone));
  const pool=leaves.length?leaves:spots;
  for(let n=1;n<=4;n++){const cell=pool[Math.floor(pool.length*n/5)];if(cell)c.put(cell[0]%c.w,Math.floor(cell[0]/c.w),"'",'w');}
 }
 if(state.dirt>.25){
  const low=spots.filter(([key])=>Math.floor(key/c.w)>c.h*.5);
  for(let n=1;n<=6;n++){const cell=low[Math.floor(low.length*n/7)];if(cell)c.put(cell[0]%c.w,Math.floor(cell[0]/c.w),n%2?':':'.','d');}
 }
 if(state.condition<.5){
  if(['pot','dish'].includes(p.container)){
   const x=p.w/2+12,y=p.h-12;c.rows(['\\',' /',' |','/'],x,y,'k');
  }else{
   const cell=spots[Math.floor(spots.length*.78)];
   if(cell)c.put(cell[0]%c.w,Math.floor(cell[0]/c.w),'~','q');
  }
 }
}
export function botanicalSprite(base,item,time,{motion=true,state={},context={},interaction=null}={}){
 const p=BLUEPRINTS[item.id];if(!p)return null;
 const t=motion?time:0,botany=state.botany||{},season=context.season||'spring',hour=context.hour??12,weather=context.weather||'sunny';
 const moisture=botany.moisture??.55,health=botany.health??.9,growth=p.rooted?state.growth??.6:1;
 const env={moisture,health,growth,hour,night:hour<6||hour>=19,summer:season==='summer',winter:season==='winter',autumn:['fall','autumn'].includes(season),
  snow:context.living?.ecology?.snow??(/snow/.test(weather)?.7:0),wetness:state.wetness||0,wind:context.living?.ecology?.wind??(/wind|storm/.test(weather)?.7:.15),
  insects:context.living?.ecology?.insects??.3,bloom:clamp((botany.bloom??.65)*(season==='winter'?.12:1),.05,1)};
 env.breeze=motion?Math.sin(t*.75)*env.wind*2.3:0;env.droop=p.rooted?clamp((.35-moisture)*2+(1-health)*.5):0;
 const c=new ObjectCanvas(p.w,p.h);pot(c,p,moisture);
 const anchors=DRAW[p.type](c,p,t,env,context)||{};
 if(state.wetness>.35||state.dirt>.25||state.condition<.5)surfaceWeather(c,p,state);
 if(p.rooted&&moisture>.75)for(let i=0;i<3;i++)c.put(p.w*.4+i*7,p.h-9+i%2,"'",'w');
 if(p.rooted&&health<.45)c.put(p.w/2-12,p.h-7,'<;>','q');
 const inks={b:'#c59b76',f:'#e6c9a3',s:'#658969',k:'#364d36',g:'#88b16e',l:'#bad69b',p:'#e8a6b2',q:'#d3c46f',a:'#e8c36b',r:'#df7d75',v:'#bba5da',w:'#9fd8d0',c:'#ebe7cb',d:'#6e5b43'};
 const panels={b:'#493a2d',f:'#574635',s:'#2c422e',k:'#1e3325',g:'#28452e',l:'#3c5337',p:'#4e303e',q:'#4b472c',a:'#51452a',r:'#4c2b2b',v:'#3c344b',w:'#29494a',c:'#686a53',d:moisture>.6?'#282a22':'#3b3328'};
 if(p.color==='rose')inks.p='#df8eaa';
 if(p.color==='lavender'){inks.p='#c2a9e2';panels.p='#43344f';}
 if(p.color==='blue'){inks.p='#a7c7e7';panels.p='#2d4556';}
 if(p.color==='gold'){inks.p='#eac775';panels.p='#574829';}
 if(p.color==='red'){inks.p='#e49373';panels.p='#57362d';}
 if(p.color==='autumn'){inks.p='#d5a269';panels.p='#52412e';}
 if(env.autumn&&p.type==='tree'&&!['bonsai','world'].includes(p.shape)){
  Object.assign(inks,{g:'#c29f62',l:'#e0bb7e'});Object.assign(panels,{g:'#4c412c',l:'#5c4b31'});
 }
 if(p.rooted&&moisture<.2)Object.assign(inks,{g:'#a09e65',l:'#c7bb82'});
 return {...base,...c.finish(),inks,panels,
  construction:'botanical-v1',blueprint:item.id,detail:true,detailScale:.62,anchors,botanical:{rooted:p.rooted,shape:p.shape,...env},
  animated:motion,active:Boolean(interaction&&!interaction.paused),sway:0,lift:0};
}
