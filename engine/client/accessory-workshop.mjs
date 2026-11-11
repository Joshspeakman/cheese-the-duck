import {ObjectCanvas} from './object-canvas.mjs';
import BLUEPRINTS from './animation/accessories.json' with {type:'json'};
export {BLUEPRINTS as ACCESSORY_BLUEPRINTS};
const clamp=v=>Math.max(0,Math.min(1,Number.isFinite(v)?v:0));
export function accessoryMaterial(raw={}){
 return {...Object.fromEntries(['wet','snow','fog','wind','soil','slack'].map(k=>[k,clamp(raw[k])])),phase:Number.isFinite(raw.phase)?raw.phase:0};
}
export function accessoryColors(p){return {b:p.color,a:p.trim,f:'#e6debf',s:'#768e87',k:'#354b49',p:'#d0b2b1',q:'#a3cdcd',g:'#99b88f'};}
function polygon(c,points,tone='b',edge='a'){
 const ys=points.map(p=>p[1]);
 for(let y=Math.ceil(Math.min(...ys));y<=Math.floor(Math.max(...ys));y++){
  const cuts=[];for(let i=0;i<points.length;i++){const a=points[i],b=points[(i+1)%points.length];if((a[1]<=y&&b[1]>y)||(b[1]<=y&&a[1]>y))cuts.push(a[0]+(b[0]-a[0])*(y-a[1])/(b[1]-a[1]));}
  cuts.sort((a,b)=>a-b);for(let i=0;i+1<cuts.length;i+=2)c.solid(Math.ceil(cuts[i]),y,Math.floor(cuts[i+1])-Math.ceil(cuts[i])+1,1,tone);
 }
 points.forEach((a,i)=>c.line(...a,...points[(i+1)%points.length],null,edge));
}
function curve(c,points,char=':',tone='a'){
 for(let i=1;i<points.length;i++)c.line(...points[i-1],...points[i],char,tone);
}
function lens(c,p,x,y,rx,ry,large,v,phase){
 if(p.style==='heart'){
  const pts=[[x-rx,y-ry*.4],[x-rx*.7,y-ry],[x,y-ry*.55],[x+rx*.7,y-ry],[x+rx,y-ry*.4],[x+rx*.8,y+ry*.2],[x,y+ry],[x-rx*.8,y+ry*.2]];
  polygon(c,pts,'q','b');
 }else if(p.style==='aviator'){
  polygon(c,[[x-rx,y-ry*.6],[x-rx*.5,y-ry],[x+rx*.6,y-ry],[x+rx,y-ry*.4],[x+rx*.7,y+ry*.75],[x+rx*.2,y+ry],[x-rx*.65,y+ry*.5]],'q','b');
 }else if(p.style==='wayfarer'||p.style==='cat_eye'){
  const flare=p.style==='cat_eye'?rx*.3:0;
  polygon(c,[[x-rx-flare,y-ry],[x+rx+flare,y-ry],[x+rx*.7,y+ry*.65],[x+rx*.3,y+ry],[x-rx*.55,y+ry]],'q','b');
  c.line(x-rx-flare,y-ry,x+rx+flare,y-ry,'=','b');
 }else if(p.style==='star'){
  polygon(c,Array.from({length:10},(_,i)=>{const a=i*Math.PI/5-Math.PI/2,r=i%2?.55:1;return [x+Math.cos(a)*rx*r,y+Math.sin(a)*ry*r];}),'q','b');
 }else{
  if(large)c.ellipse(x,y,rx,ry,'_','q',true);
  c.ellipse(x,y,rx,ry,'_','b');
 }
 if(large){
  if(['round','engraved','oval'].includes(p.style))c.ellipse(x,y,rx-1,ry-1,'.','a');
  c.line(x-rx*.45,y-ry*.45,x-rx*.2,y-ry*.65,'/','f');
  c.line(x+rx*.25,y+ry*.4,x+rx*.5,y+ry*.1,'/','a');
  if(v.fog>.12)for(let j=-ry+3;j<ry-2;j+=3)for(let i=-rx+3;i<rx-2;i+=4)c.put(x+i,y+j,v.fog>.5?':':'.','s');
  if(v.soil>.15)c.put(x+rx*.5,y+ry*.6,':.','k');
 }else{
  // Only the rim is drawn on the face. The posed eye is restored by the rig.
  c.put(x-rx,y-1,v.fog>.2?':':phase%5<1?'/':"'",'f');
 }
 if(v.wet>.15)c.put(x+rx,y+Math.min(ry,1),"'",'q');
}
function ribbon(c,p,x,y,w,len,phase,v,large,folded=false){
 const sway=(folded?.2:1)*Math.sin(phase)*p.flutter*(1+v.wind*1.5)*(1-v.wet*.7),rows=[];
 for(let j=0;j<len;j++){
  const bend=sway*Math.sin(j/Math.max(1,len-1)*2.2)*(large?4:.6),xx=x+bend;
  c.solid(xx,y+j,w,1,'b');c.put(xx,y+j,j%3?'|':'/','a');c.put(xx+w-1,y+j,j%3?'|':'\\','s');
  if(large){
   if(p.style==='stripe'&&j%8<3)c.line(xx+1,y+j,xx+w-2,y+j,'=','p');
   else if(p.style==='plaid')for(let i=2;i<w-2;i+=4)c.put(xx+i,y+j,j%4?'|':'+','p');
   else if(p.style==='cable')c.put(xx+w/2-1,y+j,j%4<2?'()':')(','a');
   else if(p.style==='fleece')for(let i=2;i<w-2;i+=3)c.put(xx+i,y+j,(j+i)%2?'~':'.','f');
   else if(j%2===0)c.line(xx+2,y+j,xx+w-3,y+j,'v','a');
  }else if(w>2)c.put(xx+1,y+j,p.style==='cable'?')':p.style==='plaid'?'+':p.style==='stripe'?'=':p.style==='fleece'?'~':'v','a');
  rows.push([xx,y+j]);
 }
 const [xx,yy]=rows.at(-1);
 for(let i=0;i<w;i+=large?2:1)c.line(xx+i,yy+1,xx+i+sway*.4,yy+(large?4:1),i%3?'|':':','a');
 return {x:Math.round(xx+w/2),y:Math.round(yy)};
}
function bow(c,p,x,y,w,phase,large,folded,slack=0){
 const half=w/2,knot=large?3:1,height=large?w*.22:1,flutter=Math.sin(phase)*(folded?.2:1)*(large?2:1);
 for(const side of [-1,1]){
  const end=x+side*half,dy=side*flutter+(side<0?slack*(large?4:1):0);
  if(p.style==='butterfly'){
   c.ellipse(x+side*half*.55,y-height*.35+dy,half*.48,height,'~','b',true);
   c.ellipse(x+side*half*.5,y+height*.65+dy,half*.35,height*.65,'o','b',true);
  }else polygon(c,[[x+side*knot,y-1],[end,y-height+dy],[end-side*(p.style==='scallop'?2:0),y+height+dy],[x+side*knot,y+1]],'b');
  if(large){
   for(let j=-1;j<=1;j++)c.line(x+side*(knot+2),y,end-side*3,y+j*height*.7+dy,p.style==='pleated'?'=':':','s');
   if(p.style==='diamond')c.rows([' /\\ ','<  >',' \\/ '],x+side*half*.6-2,y-1+dy,'f');
   else if(p.style==='scallop')for(let j=0;j<3;j++)c.put(end-side*5,y-height+3+j*4+dy,'o','f');
   else if(p.style==='butterfly')c.put(end-side*5,y-height*.4+dy,'(@)','p');
   else c.line(end-side*2,y-height+2+dy,end-side*2,y+height-2+dy,"'",'a');
   polygon(c,[[x+side*2,y+3],[x+side*11,y+17],[x+side*7,y+14],[x+side*2,y+18],[x-side*2,y+4]],'b');
  }
 }
 c.ellipse(x,y,knot,large?5:1,'=','a',true);
 if(large)c.line(x,y-3,x,y+3,'|','f');
 return {x,y};
}
function necklace(c,p,x,y,w,phase,large,slack=0){
 const rx=w/2,drop=large?15+slack*4:1+Math.round(slack),swing=Math.sin(phase)*(large?2:1),points=[];
 for(let i=0;i<=20;i++){const u=i/20;points.push([x-rx+u*w,y+Math.sin(u*Math.PI)*drop]);}
 curve(c,points,p.shape==='bell'?'=':':','b');
 if(p.shape==='pearls'||p.shape==='lei')for(let i=0;i<=8;i++){
  const u=i/8,xx=x-rx+u*w,yy=y+Math.sin(u*Math.PI)*drop;
  if(large){
   if(p.shape==='lei'){c.rows([' .o. ','o(*)o'," 'o' "],xx-2,yy-1,i%2?'a':'b',true);c.put(xx,yy,'*','f');c.put(xx+2,yy+2,'/','g');}
   else {const r=2+Math.sin(u*Math.PI);c.ellipse(xx,yy,r,r*.75,'_','b',true);c.put(xx-1,yy-1,"'",'f');c.put(xx+1,yy+1,'.','s');}
  }
  else if(i%2===0)c.put(xx,yy,p.shape==='lei'?'*':'o',i%4?'b':'f');
 }
 const px=x+swing,py=y+drop+(large?5:1);
 if(large)c.line(x,y+drop,px,py,':','a');
 if(p.shape==='bell'){
  if(large){c.rows([' .---. ','/     \\','|  |  |','|  |  |','\\_____/','   o   '],px-3,py,'a',true);c.put(px-1,py+1,"'/",'f');c.rect(x-rx+2,y-2,7,4,'a');c.put(x-rx+5,y,'+','f');}
  else c.put(px-1,py,'(o)','a');
 }else if(p.shape==='acorn'){
  if(large){c.ellipse(px,py+4,5,6,'v','b',true);c.ellipse(px,py,6,2,'#','a',true);c.put(px-1,py-3,'/','g');for(let j=0;j<3;j++)c.put(px-2+j*2,py,'x','s');c.line(px-2,py+3,px-1,py+7,'|','f');}
  else c.put(px-1,py,'(@)','a');
 }else if(large)c.rows([' .-. ','( o )'," '-' "],px-2,py,p.shape==='pearls'?'f':'g');
 if(!large&&['pearls','lei'].includes(p.shape))return {x:Math.round(x),y:Math.round(y+drop)};
 return {x:Math.round(px),y:Math.round(py+(large?['pearls','lei'].includes(p.shape)?1:3:0))};
}
function build(c,back,p,{cx,cy,w,large,phase,v,rig}){
 const contacts={},sleeping=rig?.action==='sleeping',swimming=rig?.action==='swimming';
 if(p.shape==='frames'){
  if(large){const rx=p.style==='oval'?14:12,ry=p.style==='round'?11:p.style==='aviator'?10:8;
   lens(c,p,cx-17,cy,rx,ry,true,v,phase);lens(c,p,cx+17,cy,rx,ry,true,v,phase);
   c.line(cx-5,cy-2,cx+5,cy-2,'_','a');if(p.style==='aviator')c.line(cx-7,cy-7,cx+7,cy-7,'=','f');
   for(const side of [-1,1]){c.line(cx+side*29,cy-5,cx+side*36,cy-13,null,'b');c.put(cx+side*29,cy-4,'o','f');c.line(cx+side*36,cy-13,cx+side*40,cy-10,null,'a');}
  }else{lens(c,p,cx,cy,2,1,false,v,phase);c.line(cx-4,cy-1,cx-2,cy-1,'-','b');c.put(cx+2,cy,'-','a');}
  contacts.lens={x:cx-2,y:cy};contacts.bridge={x:cx+2,y:cy};
 }else if(p.shape==='monocle'){
  const rx=large?15:2,ry=large?12:1;lens(c,p,cx,cy,rx,ry,large,v,phase);
  const chain=[];for(let i=0;i<=12;i++){const u=i/12;chain.push([cx-rx+Math.sin(u*Math.PI)*(large?13:1)+Math.sin(phase)*u,cy+u*(large?31:3)]);}
  curve(c,chain,large?'o':':','a');const tip=chain.at(-1);c.put(tip[0]-1,tip[1],large?'(+)':'o','f');
  if(large)for(let i=0;i<16;i++){const a=i*Math.PI/8;c.put(cx+Math.cos(a)*(rx+1),cy+Math.sin(a)*(ry+1),i%2?'.':':','a');}
  contacts.lens={x:cx-2,y:cy};contacts.bridge={x:cx-2,y:cy};
 }else if(p.shape==='mask'){
  if(large){
   polygon(c,[[cx-34,cy-10],[cx-22,cy-5],[cx-10,cy-11],[cx,cy-5],[cx+10,cy-11],[cx+22,cy-5],[cx+34,cy-10],[cx+27,cy+10],[cx+13,cy+7],[cx,cy+12],[cx-13,cy+7],[cx-27,cy+10]],'b');
   for(const side of [-1,1]){c.ellipse(cx+side*15,cy,8,4,'_','k',true);c.ellipse(cx+side*15,cy,8,4,'~','a');for(let i=0;i<5;i++)c.put(cx+side*(10+i*4),cy-7+(i%2),'o','p');}
   for(let i=0;i<5;i++){const a=cx-29+i*3,top=cy-15-i%2*5;c.line(cx-27,cy-4,a,top,'/','g');c.line(a-2,top+2,a+2,top-1,'/','a');}
  }else{c.put(cx-2,cy,'<','b');c.put(cx+1,cy,'>','a');c.put(cx-3,cy-1,'/','g');c.put(cx-3,cy-2,phase%4<2?'~':'/','p');}
  contacts.lens={x:cx-2,y:cy};contacts.bridge={x:cx+1,y:cy};
 }else if(p.shape==='bow')contacts.knot=bow(c,p,cx,cy,w,phase,large,sleeping,v.slack);
 else if(p.shape==='bandana'){
  const height=large?28:3,sway=Math.sin(phase)*(large?3:1)*(1-v.wet*.7);
  polygon(c,[[cx-w/2,cy],[cx+w/2,cy],[cx+sway,cy+height]],'b');
  c.line(cx-w/2,cy,cx+w/2,cy,'=','a');
  if(large){for(let i=-2;i<=2;i++)c.put(cx+i*7,cy+5,'(@)','p');c.line(cx-w/2+5,cy+4,cx+sway,cy+height-5,':','f');c.line(cx+w/2-5,cy+4,cx+sway,cy+height-5,':','f');c.put(cx-2,cy+14,'<~>','a');}
  else c.put(cx,cy+1,':','a');
  contacts.knot={x:cx,y:cy};contacts.fringe={x:Math.round(cx+sway),y:cy+height-1};
 }else if(p.shape==='scarf'){
  if(large){
   contacts.fringe=ribbon(back,p,cx-12,cy+7,14,30,phase,v,true,sleeping);
   ribbon(back,p,cx+5,cy+5,13,25,phase+1,v,true,sleeping);
   c.ellipse(cx,cy,w/2,10,'~','b',true);c.ellipse(cx,cy-3,w/2-5,4,'_','k',true);c.ellipse(cx,cy-3,w/2-5,4,'_','s');
   for(let i=-3;i<=3;i++)c.line(cx+i*5,cy+2,cx+i*5-2,cy+6,'v','a');
   if(p.style==='plaid')c.put(cx+14,cy+4,'<v>','g');
  }else{
   // The free end falls from the neck onto the breast. Hanging it outside
   // the rear body required a horizontal strip that read as a floating pole.
   const length=Math.min(sleeping||swimming?2:5,Math.max(1,rig.body.h-2)),x=cx-1,y=cy+1;
   const pinch=rig.hatCare?.id==='wring_scarf'&&Math.abs(rig.hatCare.sweep)>.4?1:0;
   contacts.fringe=ribbon(c,p,x,y,(rig.small?2:3)-pinch,length,phase,v,false,sleeping);
   c.line(cx-w/2-Math.round(v.slack),cy,cx+w/2,cy,'~','b');c.put(cx-1,cy,'(=)','a');
  }
  contacts.knot={x:cx,y:cy};
 }else if(['pearls','lei','bell','acorn'].includes(p.shape))contacts.pendant=necklace(c,p,cx,cy,w,phase,large,v.slack);
 else if(p.shape==='headphones'){
  const rx=large?28:w/2+1,ry=large?24:Math.max(3,rig.head.h+1),top=cy-ry;
  const band=Array.from({length:25},(_,i)=>{const a=Math.PI+i*Math.PI/24;return [cx+Math.cos(a)*rx,cy+Math.sin(a)*ry];});curve(c,band,'=','b');
  if(large){curve(c,band.map(([x,y])=>[x,y+2]),':','a');for(const side of [-1,1]){
   c.rect(cx+side*rx-3,cy-9,7,14,'a');for(let j=0;j<3;j++)c.put(cx+side*rx,cy-7+j*3,'o','f');
   const compression=(.5+.5*Math.sin(phase*1.7))*.8;
   c.ellipse(cx+side*rx,cy+5,7,13,'=','b',true);c.ellipse(cx+side*rx,cy+5,4+compression,9-compression,':','s',true);
   for(let j=-2;j<=2;j++)c.line(cx+side*rx-2,cy+5+j*3,cx+side*rx+2,cy+5+j*3,'.','a');
  }}else{c.put(cx-rx-1,cy,Math.sin(phase*1.7)>.4?'[=]':'(=)','b');c.put(cx+rx,cy,']','a');}
  contacts.pad={x:Math.round(cx-rx),y:cy};contacts.headband={x:cx,y:Math.round(top)};
 }
 const anchor=contacts.knot||contacts.bridge||contacts.pendant||contacts.pad;
 if(anchor){if(v.snow>.16)c.put(anchor.x-(large?5:1),anchor.y-1,'*','f');if(v.wet>.15)c.put(anchor.x+(large?7:1),anchor.y+1,"'",'q');if(v.soil>.18&&p.slot!=='face')c.put(anchor.x-1,anchor.y,':','s');}
 return contacts;
}
export function accessorySprite(base,item,time,{state={},motion=true}={}){
 const p=BLUEPRINTS[item.id];if(!p)return null;
 const c=new ObjectCanvas(p.w,p.h),back=new ObjectCanvas(p.w,p.h),v=accessoryMaterial(state.apparel||state),phase=motion?(Number.isFinite((state.apparel||state).phase)?v.phase:time*1.2):0;
 const contacts=build(c,back,p,{cx:48,cy:p.shape==='headphones'?35:p.shape==='scarf'?19:25,w:50,large:true,phase,v});
 for(const f of c.fills)back.fills.push(f);
 back.clipped||=c.clipped;
 c.art.forEach((r,y)=>r.forEach((ch,x)=>{if(ch!==' ')back.put(x,y,ch,c.tones[y][x]);}));
 return {...base,...back.finish(),inks:accessoryColors(p),panels:{b:p.color,a:p.trim,q:'#304d50',s:'#304239',k:'#142e2b'},
  blueprint:item.id,construction:'accessory-v1',detail:true,detailScale:p.detailScale,anchors:contacts,animated:false,emissive:false,floor:false,sway:0,lift:0};
}
export function fittedAccessory(rig,id,{material={},phase=0}={}){
 const p=BLUEPRINTS[id];if(!p)return null;
 const c=new ObjectCanvas(76,48),back=new ObjectCanvas(76,48),v=accessoryMaterial(material),h=rig.head,n=rig.neck,e=rig.eye;
 const cx=p.slot==='face'?e.x:p.slot==='neck'?Math.round(n.x+n.w/2):Math.round(h.x+h.w/2);
 const sag=v.slack>.35?1:0;
 const cy=p.slot==='face'?e.y+sag:p.slot==='neck'?n.y:Math.round(h.y+h.h*.5)+sag,w=p.slot==='neck'?(rig.small?5:7):h.w;
 const contacts=build(c,back,p,{cx,cy,w,large:false,phase,v,rig});
 return {front:c.finish(),back:back.finish(),x:0,y:0,contacts};
}
export function accessorySummary(raw={},id=null){
 const s=accessoryMaterial(raw);return [s.wet>.6?'Soaked':s.wet>.2?'Damp':'Dry',s.fog>.16&&(!id||BLUEPRINTS[id]?.fog)?'mist on the lens':'',s.snow>.14?'caught snow':'',s.soil>.16?'a little grubby':'',s.slack>.15?'needs settling':''].filter(Boolean).join(' · ');
}
