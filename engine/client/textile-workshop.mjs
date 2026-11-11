import {ObjectCanvas} from './object-canvas.mjs';
import BLUEPRINTS from './animation/textiles.json' with {type:'json'};
export {BLUEPRINTS as TEXTILE_BLUEPRINTS};
const clamp=n=>Math.max(0,Math.min(1,n));
export function textilePoint(p,u,v,pose={}){
 const x=(p.w*.13+u*p.w*.74)*(1-v)+(6+u*(p.w-12))*v;
 const raised=(pose.lift||0)*Math.max(0,1-Math.abs(u-.13)*4)*Math.max(0,v-.5)*18;
 const dent=(pose.press||0)*Math.exp(-((u-(pose.u??.5))**2+(v-(pose.v??.6))**2)*40)*1.5;
 return {x,y:12+v*(p.h-26)-raised+dent};
}
function line(c,p,a,b,glyph,tone,v={}){const A=textilePoint(p,...a,v),B=textilePoint(p,...b,v);c.line(A.x,A.y,B.x,B.y,glyph,tone);}
function at(c,p,u,v,text,tone,pose={}){const q=textilePoint(p,u,v,pose);c.put(q.x,q.y,text,tone);}
function plane(c,p,pose,tone,minV=0){
 for(let y=Math.ceil(12+minV*(p.h-26));y<=p.h-14;y++){
  const v=(y-12)/(p.h-26),a=textilePoint(p,0,v,pose),b=textilePoint(p,1,v,pose);
  c.solid(a.x,Math.min(a.y,b.y),b.x-a.x+1,1,tone);
 }
 for(const [a,b] of [[[0,minV],[1,minV]],[[0,minV],[0,1]],[[1,minV],[1,1]],[[0,1],[1,1]]])line(c,p,a,b,null,'f',pose);
}
function diamond(c,p,u,v,w,h,tone,pose){
 const points=[[u-w,v],[u,v-h],[u+w,v],[u,v+h]];
 for(let i=0;i<4;i++)line(c,p,points[i],points[(i+1)%4],null,tone,pose);
}
function border(c,p,pose,inside=.055){
 for(const inset of [inside,inside+.025])for(const [a,b] of [[[inset,inset],[1-inset,inset]],[[inset,1-inset],[1-inset,1-inset]],[[inset,inset],[inset,1-inset]],[[1-inset,inset],[1-inset,1-inset]]])line(c,p,a,b,null,'a',pose);
}
function sod(c,p,v){
 for(let row=0;row<p.h-25;row++){
  const depth=row/(p.h-26),a=textilePoint(p,0,depth,v),b=textilePoint(p,1,depth,v),inset=[2,0,1,3,1,0,2][row%7];
  c.solid(a.x+inset,a.y,b.x-a.x-inset*2,1,'k');
  if(row%3===0){c.put(a.x+inset,a.y,';', 'b');c.put(b.x-inset-1,a.y,':','b');}
 }
 for(let u=.025;u<.98;u+=.025){const q=textilePoint(p,u,1,v),n=Math.round(u*100);c.put(q.x,q.y+(n%3),'~','b');c.put(q.x,q.y+2+(n%2),n%3?'v':':','s');}
}
function grasses(c,p,v,s){
 sod(c,p,v);for(let j=0;j<17;j++)for(let i=0;i<29;i++){
  const x=.025+i*.032+(j%2)*.011,y=.045+j*.055+(i%3)*.007;
  const q=textilePoint(p,x,y,v),n=i*7+j*11,pressed=(v.press||0)>0&&Math.hypot(x-v.u,y-v.v)<.15||((s.textile?.nap??.5)<.4&&n%4===0);
  const glyph=pressed?'__':p.style==='lawn'?(n%3?'|/':'\\|'):n%4===0?'\\|/':n%3===0?'i|':'/|';
  c.put(q.x,q.y-3,glyph,n%3?'l':'g');
  if(p.style==='meadow'&&n%13===0)c.put(q.x,q.y-5,'*','a');
  if((s.wetness||0)>.2&&n%11===0)c.put(q.x+1,q.y-2,'o','w');
 }
}
function moss(c,p,v,s){
 sod(c,p,v);
 for(let j=0;j<11;j++)for(let i=0;i<14;i++){
  const q=textilePoint(p,.04+i*.066+(j%2)*.018,.065+j*.085+(i%3)*.008,v),r=3+(i*3+j)%4;
  const loft=1+(s.textile?.nap??.5)*2+(i+j)%2;
  c.ellipse(q.x,q.y-2,r,loft,'~',(i+j)%2?'l':'g',true);c.put(q.x-1,q.y-3,':;','f');c.put(q.x-2,q.y-1,'vv','l');
  if((i*3+j)%11===0){c.line(q.x+2,q.y-2,q.x+3,q.y-6,'|','b');c.put(q.x+2,q.y-7,'()','a');}
 }
}
function cloth(c,p,v,s){
 const roll=p.type==='scrap'?0:clamp(v.roll||0),cut=roll*.88;
 plane(c,p,v,p.style==='runner'?'q':p.style==='coir'?'b':p.style==='medallion'?'n':'d',cut);
 const back=cut+.02;
 if(p.style==='runner'){
  for(let y=back;y<.98;y+=.06)for(let x=.04;x<.98;x+=.035)at(c,p,x,y,Math.round(x*100+y*100)%2?':':';','s',v);
  for(const u of [.08,.12,.88,.92])line(c,p,[u,back],[u,.98],'|','a',v);
  for(let y=back+.08;y<.9;y+=.16){diamond(c,p,.5,y,.04,.045,'a',v);at(c,p,.49,y,'+','f',v);}
 }else if(p.style==='medallion'){
  border(c,p,v);
  for(let y=Math.max(back,.12);y<.9;y+=.05)for(let x=.09;x<.92;x+=.035)at(c,p,x,y,':','s',v);
  for(let y=Math.max(back,.17);y<.87;y+=.17)for(const u of [.29,.71]){
   const edge=Math.abs(y-.5)/.33*.27;
   if(Math.abs(u-.5)>.3-edge){at(c,p,u-.012,y,'{+}','g',v);at(c,p,u,y+.035,'v','a',v);}
  }
  for(let u=.08;u<.93;u+=.07){if(cut<.03)at(c,p,u,.03,'x','q',v);at(c,p,u,.97,'x','q',v);}
  if(cut<.65){diamond(c,p,.5,.5,.27,.33,'a',v);diamond(c,p,.5,.5,.22,.27,'q',v);diamond(c,p,.5,.5,.15,.19,'f',v);diamond(c,p,.5,.5,.07,.1,'a',v);at(c,p,.48,.5,'(o)','q',v);}
  for(const [u,y] of [[.18,.22],[.82,.22],[.18,.78],[.82,.78]])if(y>cut){diamond(c,p,u,y,.065,.08,'a',v);at(c,p,u-.03,y,'{*}','q',v);}
  for(let u=.08;u<.94;u+=.08){if(cut<.08)at(c,p,u,.07,'<>','g',v);at(c,p,u,.93,'<>','g',v);}
 }else if(p.style==='tatami'||p.style==='braid'){
  for(let y=back;y<.98;y+=.045)for(let x=.025;x<.98;x+=.035)at(c,p,x,y,(Math.round(y*100)%2?'==':'||'),(Math.round(x*100)+Math.round(y*100))%3?'b':'f',v);
  for(const u of [.04,.96]){line(c,p,[u,back],[u,1],'|','g',v);for(let y=back;y<.95;y+=.1)at(c,p,u,y,p.style==='tatami'?'[x]':'(x)','k',v);}
  if(p.style==='braid')for(let y=back;y<1;y+=.06)at(c,p,.48,y,'/\\','a',v);
 }else if(p.style==='coir'){
  for(let y=back;y<.98;y+=.05)for(let x=.035;x<.98;x+=.035)at(c,p,x,y,Math.round(x*99)%2?'u':'n','s',v);
  if(cut<.65){const q=textilePoint(p,.5,.52,v);c.clear(q.x-24,q.y-3,49,8);c.rect(q.x-25,q.y-4,51,10,'k',true);c.put(q.x-20,q.y,'Q U A C K - O M E !','a');c.put(q.x-23,q.y-2,'(o)>','f');c.put(q.x+17,q.y+3,'<3','q');}
  border(c,p,v,.025);
 }else{
  const cols=p.type==='scrap'?3:5,rows=3;
  for(let j=0;j<rows;j++)for(let i=0;i<cols;i++){
   const tone=['q','w','l','n','b'][(i+j*2)%5],lo=Math.max(back,.06+j*.28),hi=.06+(j+1)*.28;
   for(let y=lo;y<hi;y+=.035)for(let x=.05+i*.18;x<.05+(i+1)*.18;x+=.025)at(c,p,x,y,(i+j)%3?'x':'.',tone,v);
   if(hi>cut){line(c,p,[.05+i*.18,Math.max(cut,.06)],[.05+i*.18,.9],':','f',v);line(c,p,[.05,hi],[.95,hi],':','f',v);}
  }
  if(p.type==='scrap'&&v.roll>.02){
   const f=clamp(v.roll),edge=textilePoint(p,.95-.55*f,.2+.35*f,v),corner=textilePoint(p,.95,.9,v),left=textilePoint(p,.45,.9,v);
   for(let y=Math.ceil(edge.y);y<=corner.y;y++){const u=(y-edge.y)/Math.max(1,corner.y-edge.y),x=edge.x+(left.x-edge.x)*u,right=edge.x+(corner.x-edge.x)*u;c.clear(x,y,right-x+1,1);c.solid(x,y,right-x+1,1,'b');}
   c.line(edge.x,edge.y,left.x,left.y,'/','f');c.line(edge.x,edge.y,corner.x,corner.y,'\\','a');
  }
 }
 const crease=1-(s.textile?.nap??.5);
 if(crease>.06)for(const [u,y] of [[.08,.3],[.88,.43],[.17,.81]])if(y>cut+.05){
  const a=textilePoint(p,u,y,v),b=textilePoint(p,u+.045+crease*.035,y+crease*.055,v);
  c.line(a.x,a.y,b.x,b.y,'~','s');c.put(b.x,b.y+1,':','f');
 }
 if(p.style!=='coir')for(let u=.04;u<1;u+=.04){const q=textilePoint(p,u,1,v),lean=(1-(s.textile?.fringe??.5))*(Math.round(u*100)%3-1)*4;c.line(q.x,q.y,q.x+lean,q.y+4+(Math.round(u*100)%2),'|','b');c.put(q.x+lean,q.y+5,'~','f');}
 if(roll>.02){
  const a=textilePoint(p,0,cut,v),b=textilePoint(p,1,cut,v),height=3+roll*5;
  c.clear(0,0,p.w,Math.ceil(a.y-height));c.fills=c.fills.filter(f=>f.y>=Math.ceil(a.y-height));
  c.clear(a.x-2,a.y-height,b.x-a.x+5,height*2+2);c.rect(a.x,a.y-height,b.x-a.x,height*2,'b',true);
  for(let y=a.y-height+2;y<a.y+height;y+=2)c.line(a.x+2,y,b.x-2,y,'=','s');
  for(const x of [a.x,b.x]){c.ellipse(x,a.y,3,height,'o','a',true);c.ellipse(x,a.y,1,Math.max(1,height-2),'o','k');}
 }
}
function rubber(c,p,v,s){
 plane(c,p,v,'k');border(c,p,v,.04);
 for(let y=.12;y<.94;y+=.12)for(let u=.07;u<.96;u+=.09){
  const q=textilePoint(p,u,y,v),pressure=(v.press||0)*Math.max(0,1-Math.hypot(u-v.u,y-v.v)*6);
  c.put(q.x,q.y,pressure>.6?'[__]':'[::]','g');c.put(q.x+1,q.y+2,'oo','d');
  if((s.wetness||0)>.3)c.put(q.x,q.y+1,'~~','w');
 }
 for(let y=.1;y<.95;y+=.15){at(c,p,0,y,'[','f',v);at(c,p,.99,y,']','f',v);}
}
function bundle(c,p,v,s){
 if(p.style==='reeds'){
  for(let i=0;i<30;i++){
   const spread=clamp(v.spread),x=20+i*3.7,top=14+(i*7%9),bottom=p.h-17-(i*11%7),dx=(i-15)*spread*.6;
   c.beam(x,top,x+dx,bottom,3,i%3?'b':'a');c.put(x-1,top,'()','f');c.line(x,top+4,x+dx,bottom-3,':','s');
   for(let y=top+12;y<bottom-6;y+=15)c.put(x+dx*(y-top)/(bottom-top)-1,y,'==','k');
  }
  for(const y of [34,58]){const slack=(1-v.tie)*8;c.line(18,y,132,y+slack,'~','q');c.line(18,y+2,132,y+2+slack,'~','a');c.rows(['\\ /','(x)','/ \\'],70,y-1,'f');}
 }else{
  const loft=clamp(v.loft),base=p.h-13;
  for(let i=3;i>=0;i--){
   const y=base-i*(3+loft*4),x=14+i*2;
   c.rect(x,y-10,p.w-28-i*3,12,'b',true);c.line(x+2,y,p.w-16,y,'~','f');
   for(let k=x+3;k<p.w-18;k+=5)c.put(k,y-3,(k+i)%3?'u':'~','a');
  }
  const top=base-3*(3+loft*4)-10;
  for(let j=0;j<3;j++)for(let i=0;i<9;i++){const x=24+i*10,y=top+2+j*3;c.put(x,y,j%2?'x--x':'| :|','s');}
  c.put(27,top+7,'SOFT / SAVE FOR LATER','a');
 }
}
export function textileSprite(base,item,time,{state={},pose={},context={}}={}){
 const p=BLUEPRINTS[item.id];if(!p)return null;
 const s=state.textile||{},v={roll:s.roll||0,spread:s.spread??.2,tie:s.tie??1,loft:s.loft??.6,lift:0,press:0,comb:0,u:.5,v:1.08,...pose.textile};
 const c=new ObjectCanvas(p.w,p.h);
 if(p.type==='turf')grasses(c,p,v,state);else if(p.type==='moss')moss(c,p,v,state);else if(p.type==='rubber')rubber(c,p,v,state);else if(p.type==='bundle')bundle(c,p,v,state);else cloth(c,p,v,state);
 for(const t of s.tracks||[]){if(t.v<(v.roll||0)*.88)continue;at(c,p,t.u,t.v,'_>','k',v);}
 const mark=(u,w,glyph,tone)=>{const q=textilePoint(p,u,w,v),x=Math.round(q.x),y=Math.round(q.y);if(c.fills.some(f=>f.y===y&&x>=f.x&&x+glyph.length<=f.x+f.w))c.put(x,y,glyph,tone);};
 for(let i=0;i<Math.ceil((state.dirt||0)*20);i++)mark(.1+(i*17%80)/100,.12+(i*23%72)/100,'.:','k');
 for(let i=0;i<Math.ceil((s.frost||0)*35);i++)mark(.06+(i*19%88)/100,.06+(i*29%88)/100,'*','p');
 const inks={b:'#b79f6f',a:'#e1c385',f:'#d8d8a5',s:'#80785a',k:'#334e32',d:'#7d7053',g:'#91b67b',l:'#689650',q:'#ce8390',w:'#79b0c2',n:'#a99bc2',p:'#d9e6de'};
 const panels={b:'#514a30',a:'#685934',f:'#7b7850',s:'#393b28',k:'#142b21',d:'#343c22',g:'#2e5130',l:'#284621',q:'#5c2838',w:'#244651',n:'#352944',p:'#879a91'};
 if(['fall','autumn'].includes(context.season||context.weather?.season)&&p.type==='turf'){inks.l='#8a9351';inks.g='#a5a260';}
 const foot=textilePoint(p,v.u,v.v,v),entry=textilePoint(p,.5,1.08,v),contact=textilePoint(p,clamp(v.u+.1),clamp(v.v-.16),v);
 return {...base,...c.finish(),construction:'textile-v1',detail:true,detailScale:.65,blueprint:item.id,floor:p.type!=='bundle',anchors:{entry,foot,contact},inks,panels,sway:0,lift:0,animated:Boolean(pose.textile),emissive:false};
}
