import {ObjectCanvas} from './object-canvas.mjs';
import BLUEPRINTS from './animation/headwear.json' with {type:'json'};
export {BLUEPRINTS as HEADWEAR_BLUEPRINTS};
const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,Number.isFinite(v)?v:0));
export function hatMaterial(raw={}){
 return {wet:clamp(raw.wet),snow:clamp(raw.snow),wind:clamp(raw.wind),phase:Number.isFinite(raw.phase)?raw.phase:0,fog:clamp(raw.fog)};
}
function polygon(c,points,tone='b',edge='f'){
 const ys=points.map(p=>p[1]);
 for(let y=Math.ceil(Math.min(...ys));y<=Math.floor(Math.max(...ys));y++){
  const cuts=[];
  for(let i=0;i<points.length;i++){const a=points[i],b=points[(i+1)%points.length];if((a[1]<=y&&b[1]>y)||(b[1]<=y&&a[1]>y))cuts.push(a[0]+(b[0]-a[0])*(y-a[1])/(b[1]-a[1]));}
  cuts.sort((a,b)=>a-b);for(let i=0;i+1<cuts.length;i+=2)c.solid(Math.ceil(cuts[i]),y,Math.max(1,Math.floor(cuts[i+1])-Math.ceil(cuts[i])+1),1,tone);
 }
 for(let i=0;i<points.length;i++)c.line(...points[i],...points[(i+1)%points.length],null,edge);
}
function band(c,x,y,w,h=2){c.rect(x,y-h+1,w,h,'a',true);if(w>16)c.line(x+2,y-1,x+w-3,y-1,':','f');}
function badge(c,x,y,motif,large){
 if(large){c.ellipse(x,y,5,3,'-','a',true);c.put(x-Math.floor(motif.length/2),y,motif||'*','k');}
 else c.put(x-Math.floor(motif.length/2),y,motif||'*','a');
}
function stem(c,x,y,dx,dy,bend,tone='a'){
 let prev=[x,y];for(let i=1;i<=10;i++){const t=i/10,next=[x+dx*t+bend*Math.sin(t*Math.PI),y+dy*t];c.line(...prev,...next,null,tone);prev=next;}
}
function dome(c,cx,y,rx,ry,tone='b'){
 const points=Array.from({length:25},(_,i)=>{const a=Math.PI+i*Math.PI/24;return [cx+Math.cos(a)*rx,y+Math.sin(a)*ry];});polygon(c,points,tone);
}
// A second construction at character resolution: every glyph is drawn at its
// native cell size. Large catalogue art is never resampled onto the duck.
export function drawHat(c,p,{cx,bandY,w,large=false,material={},phase=0}={}){
 const v=hatMaterial(material),sway=Math.sin(phase)*p.flutter*(1.6+v.wind*2)*(1-v.wet*.65),x=cx-w/2,y=bandY;
 const tall=large?1:.8,h=Math.max(3,w*.65*tall),top=y-h,unit=large?2:1;
 const seam=(xx,yy,ww,hh,grain=':')=>{if(large)for(let row=yy+2;row<yy+hh-1;row+=3)for(let col=xx+2;col<xx+ww-2;col+=4)c.put(col+(row%2),row,grain,'s');};
 switch(p.shape){
 case 'cap':{
  const crown=h*.7,apex=x+w*(p.style==='club'?.48:.42),tip=x+w+(p.style==='mesh'?w*.27:w*.4);
  polygon(c,[[x,y-1],[x+1,y-crown*.65],[apex,y-crown],[x+w*.84,y-crown*.8],[x+w,y-1]],'b');
  for(let i=1;i<p.panels;i++){const end=x+w*i/p.panels;c.line(apex,y-crown+1,end,y-2,null,'s');if(large)c.put(end,y-4,'o','a');}
  polygon(c,[[x+w*.35,y-1],[x+w,y-2],[tip,y-1],[tip-2,y+1],[x+w*.55,y+1]],'a');
  if(large)c.line(x+w*.65,y,tip-3,y,':','k');
  if(p.style==='mesh')for(let yy=y-crown*.6;yy<y-3;yy+=2)c.line(x+2,yy,apex-1,yy,':','s');
  if(p.style==='club')c.line(x+2,y-3,x+w*.6,y-3,'=','a');
  badge(c,x+w*.72,y-crown*.47,p.motif,large);break;
 }
 case 'party':{
  const apex=[cx+sway*unit,y-h*1.2];polygon(c,[[x,y],[...apex],[x+w,y]],'b');
  if(large)for(let yy=top+2;yy<y-2;yy+=4){const half=(yy-apex[1])/(y-apex[1])*w/2-2;for(let xx=cx-half;xx<cx+half;xx+=5)c.put(xx,yy,p.style==='spiral'?'~':p.style==='foil'?'+':'*','a');}
  else c.put(cx,y-2,p.motif,'a');
  if(p.style==='spiral')for(let i=1;i<4;i++)c.line(cx-w*i/9,y-h+i*h/4,cx+w*i/9,y-h+(i+1)*h/4,'~','a');
  c.put(apex[0]-1,apex[1]-1,phase%5<2?'\\|/':'-o-','a');band(c,x,y,w,unit);break;
 }
 case 'chef':{
  const radius=w*.27,puff=Math.sin(phase)*.8*(1-v.wet*.7);for(let i=0;i<3;i++)c.ellipse(x+w*(.2+i*.3),top+2+(i===1?-1-puff:0),radius,h*.35+Math.max(0,puff)*.2,'~','b',true);
  polygon(c,[[x,top+3],[x+w,top+3],[x+w*.85,y-2],[x+w*.15,y-2]],'b');
  for(let i=1;i<p.panels;i++)c.line(x+w*i/p.panels,top+4,x+w*.15+w*.7*i/p.panels,y-3,'|','s');band(c,x+w*.15,y,w*.7,large?4:2);break;
 }
 case 'wizard':{
  const bent=['moonbend','crooked','web'].includes(p.style),height=h*(p.style==='starfall'?1.25:1.1),tip=cx+(bent?w*.33:0)+sway*unit;
  polygon(c,[[x,y-1],[cx-w*.15,y-height*.64],[tip,y-height],[tip+w*.14,y-height+.5],[cx+w*.27,y-height*.5],[x+w,y-1]],'b');
  c.ellipse(cx,y,w*.72,large?3:1,'_','a',true);band(c,x,y-1,w,unit);
  if(large){c.put(cx-5,y-height*.43,p.style==='moonbend'?'( )':p.style==='web'?'/|\\':p.style==='crooked'?'[x]':'*  +','a');c.put(cx-2,y-height*.69,p.motif,'f');}
  else c.put(cx,y-3,p.motif.length>1?'*':p.motif,'a');
  if(p.style==='web')for(let j=1;j<=3;j++)c.line(cx+2,y-height*.5,cx+w*.5,y-j*2,':','s');break;
 }
 case 'crown':{
  const height=h*.65;let pts=[[x,y]];for(let i=0;i<p.panels;i++)pts.push([x+w*i/(p.panels-1),y-height-(i===Math.floor(p.panels/2)?unit:0)],[x+w*(i+.5)/(p.panels-1),y-height*.45]);pts=pts.slice(0,-1);pts.push([x+w,y]);polygon(c,pts,'b','a');
  if(p.style==='arches')for(const side of [-1,1])stem(c,cx+side*w*.45,y-height*.4,-side*w*.45,-height,side*w*.1,'f');
  band(c,x,y,w,large?4:2);for(let i=1;i<p.panels;i++)c.put(x+w*(i-.5)/(p.panels-1),y-1,p.style==='paper'?'*':large?'<>':'o','q');break;
 }
 case 'viking':{
  dome(c,cx,y-1,w*.48,h);band(c,x,y,w,unit);
  c.line(cx,top-1,cx,y-2,'=','a');
  for(const side of [-1,1]){
   polygon(c,[[cx+side*w*.37,y-h*.55],[cx+side*w*.62,y-h*.65],[cx+side*w*.76,y-h],[cx+side*w*.85,y-h*.6],[cx+side*w*.6,y-h*.2],[cx+side*w*.4,y-h*.22]],'p','f');
   if(p.style==='braided'){stem(c,cx+side*w*.35,y-1,side*1,-h*.5,side,'a');c.put(cx+side*w*.25,y-2,'@','a');}
  }
  if(large)for(let i=1;i<7;i++)c.put(x+w*i/7,y-1,'o','k');break;
 }
 case 'pirate':{
  polygon(c,[[x-w*.25,y],[x-w*.2,y-h*.65],[x+w*.2,y-h*.3],[cx,y-h],[x+w*.8,y-h*.3],[x+w*1.2,y-h*.65],[x+w*1.25,y],[cx,y-2]],'b');
  c.line(x-w*.18,y-1,cx,y-4,'_','a');c.line(cx,y-4,x+w*1.18,y-1,'_','a');badge(c,cx,y-h*.42,p.style==='feather'?'o':large?'x_x':'X',large);
  if(p.style==='feather'){stem(c,x+2,y-h*.4,-w*.2,-h*.5,sway*unit,'p');c.put(x-w*.2,y-h*.9,'///','p');}break;
 }
 case 'cowboy':{
  const crown=y-h*.72;
  polygon(c,[[x,y-2],[x+w*.12,crown+1],[x+w*.32,crown],[cx,crown+1],[x+w*.68,crown],[x+w*.88,crown+1],[x+w,y-2]],'b');
  if(large){c.line(x+w*.2,crown+3,x+w*.38,crown+2,':','s');c.line(x+w*.62,crown+2,x+w*.8,crown+3,':','s');}
  band(c,x,y-1,w,unit);stem(c,x-w*.4,y-3,w*1.8,0,w*.05,'a');c.ellipse(cx,y-1,w*.8,large?3:1,'_','b');badge(c,cx,y-2,'=',large);seam(x,top+2,w,h-5,"'");break;
 }
 case 'tophat':{
  const ww=p.style==='pilgrim'?w*.86:w,hh=p.style==='pilgrim'?h*.8:h;
  polygon(c,[[cx-ww/2,y-1],[x, y-hh],[x+w,y-hh],[cx+ww/2,y-1]],'b');
  c.ellipse(cx,y-hh,w*.5,large?2:1,'_','b');c.ellipse(cx,y,w*.75,large?2:1,'_','a',true);band(c,cx-ww/2,y-2,ww,large?4:2);
  if(p.style==='silk'){
   c.line(x+2,y-hh+2,x+2,y-5,'|','f');
   if(large){for(let yy=y-hh+4;yy<y-7;yy+=3){c.put(x+4,yy,':','a');c.put(x+w-5,yy,'|','s');}c.line(x+6,y-hh+4,x+6,y-8,':','f');}
  }else if(large){c.line(x+w-4,y-hh+3,cx+ww/2-3,y-7,':','s');c.line(cx-ww/2+2,y-7,cx+ww/2-2,y-7,'=','a');}
  badge(c,cx,y-3,'[]',large);break;
 }
 case 'beret':{
  c.ellipse(cx-w*.12,y-h*.33,w*.69,h*.48,'~','b',true);if(large){c.line(cx-w*.55,y-h*.35,cx+w*.4,y-h*.5,':','s');c.put(cx-w*.55,y-3,'/ /','s');for(let i=0;i<6;i++)c.put(cx-w*.55+i*w*.15,y-h*.55-Math.sin(i*.6)*2,"'",'a');c.line(x+4,y-3,cx+w*.3,y-3,':','a');}
  stem(c,cx,y-h*.8,1+sway*unit,-unit,1,'a');band(c,x,y,w,unit);break;
 }
 case 'beanie':{
  dome(c,cx,y-1,w*.5,h*.92);
  if(large)for(let yy=top+2;yy<y-2;yy+=2){const half=w*.45*Math.sqrt(Math.max(0,1-((yy-(y-h*.32))/(h*.62))**2));for(let xx=cx-half+2;xx<cx+half-1;xx+=3)c.put(xx,yy,p.style==='stripe'?(Math.round(yy)%4?'=':'-'):'v','a');}
  else c.put(x+1,y-2,p.style==='stripe'?'===':'v:v','a');
  band(c,x,y,w,large?4:2);c.ellipse(cx+sway*unit,top-1,large?4:1,large?2:1,'*','p',true);break;
 }
 case 'sunhat':{
  const broad=p.style==='embroidered'?1.75:p.style==='openweave'?1.5:1.35;
  c.ellipse(cx,y,w*broad/2,large?6:2,'~','b',true);
  if(large)for(let row=-3;row<=3;row+=2)c.line(cx-w*broad*.42,y+row,cx+w*broad*.42,y+row,p.style==='embroidered'?'v':':','a');
  polygon(c,[[x,y-2],[x+w*.1,top+2],[x+w*.3,top],[x+w*.7,top],[x+w*.9,top+2],[x+w,y-2]],'b');
  seam(x,top,w,h-2,p.style==='openweave'?'o':':');band(c,x,y-2,w,unit);
  if(p.style==='garden')c.put(x+1,y-3,large?'/\\/':'/','g');
  else if(p.style==='ribbon')c.put(x-1,y-2,large?'>o<':'>','p');break;
 }
 case 'flowers':{
  c.ellipse(cx,y-1,w*.6,large?3:1,'~','g');
  for(let i=0;i<p.panels;i++){
   const xx=x+w*i/(p.panels-1),yy=y-2-(i%2)*unit;
   if(p.style==='leaves')polygon(c,[[xx-2,yy],[xx-1,yy-3],[xx+2,yy-1],[xx,yy+1]],'a');
   else if(p.style==='crystals'){c.put(xx,yy,'+','p');c.line(xx-2,yy-1,xx+2,yy-1,'*','q');}
   else if(large){c.ellipse(xx,yy,3,2,'o','p');c.put(xx,yy,p.motif,'a');}
   else c.put(xx,yy,(i%2&&p.style==='blossoms')?'o':'*','p');
   if(large)c.put(xx-1,yy+2,'\\/','g');
  }break;
 }
 case 'santa':{
  const tip=cx+w*.66+sway*unit,drop=p.style==='stocking'?h*.5:h*.27;
  polygon(c,[[x,y-2],[cx-w*.22,top+2],[cx+w*.13,top],[tip,top+drop],[tip-2,top+drop+2],[cx+w*.2,top+3],[x+w,y-2]],'b');
  seam(x+2,top+4,w*.6,h-7);band(c,x,y,w,large?4:2);c.ellipse(tip,top+drop+2,large?4:1,large?3:1,'*','p',true);break;
 }
 case 'ears':{
  c.ellipse(cx,y,w*.55,1,'~','a');
  for(const side of [-1,1]){const xx=cx+side*w*.26,lean=(side===1&&p.style==='folded'?-.3:side*.12)+sway*.12;
   polygon(c,[[xx-2,y-1],[xx-2+lean*w,top-h*.3],[xx+1+lean*w,top-h*.4],[xx+2+lean*w,top-h*.2],[xx+2,y-1]],'p');c.line(xx,y-2,xx+lean*w,top,'|','a');}
  if(p.style==='folded')c.put(cx+w*.26-w*.3,top,'~','a');break;
 }
 case 'antlers':{
  c.ellipse(cx,y,w*.52,1,'~','a');for(const side of [-1,1]){const xx=cx+side*w*.24;stem(c,xx,y,side*w*.2,-h*1.15,-side*unit,'b');for(let i=1;i<4;i++){const yy=y-h*i/4;c.line(xx+side*w*i*.05,yy,xx+side*w*(i*.05+.17),yy-unit*2,null,'a');}c.put(xx+sway*unit,y-2,'o','p');}break;
 }
 case 'headband':{
  c.ellipse(cx,y,w*.52,1,'~','b');for(const side of [-1,1]){const xx=cx+side*w*.3;stem(c,xx,y,side*sway*unit,-h*.6,side,'a');c.put(xx+side*sway*unit-1,y-h*.7,'<3','p');}break;
 }
 case 'icecream':{
  polygon(c,[[x,y-h*.5],[x+w,y-h*.5],[cx,y]],'a');
  if(large)for(let i=1;i<5;i++){c.line(x+w*i/5,y-h*.5,cx,y-i*.8,':','k');c.line(x+w*i/5,y-h*.5,cx,y-i*.8+2,'/','k');}
  c.ellipse(cx+sway,y-h*.65,w*.58,h*.43,'~','p',true);c.put(cx,y-h*1.02,large?'(o)':'o','a');if(large)c.put(cx-5,top+4,'_  .  _','f');break;
 }
 case 'earmuffs':{
  let previous;for(let i=0;i<=24;i++){const a=Math.PI+i*Math.PI/24,next=[cx+Math.cos(a)*w*.7,y-2+Math.sin(a)*h*.8];if(previous)c.line(...previous,...next,null,'a');previous=next;}
  for(const side of [-1,1]){c.ellipse(cx+side*w*.65,y-1,w*.2,h*.35,'~','b',true);if(large)c.ellipse(cx+side*w*.65,y-1,w*.12,h*.22,':','p');}break;
 }
 case 'helmet':{
  c.ellipse(cx,y-h*.5,w*.7,h*.78,'_','b',true);c.ellipse(cx+1,y-h*.5,w*.54,h*.62,'_','q',true);
  c.line(cx-w*.37,y-h*.85,cx-w*.22,y-h*.95,'/','f');band(c,x-w*.14,y,w*1.28,large?5:2);
  if(large){c.put(x+1,y-2,'AIR [o]  ::','k');c.put(cx+w*.47,y-h*.65,'[+]','a');if(v.fog>.2)c.put(cx-w*.4,y-h*.3,': :','f');}break;
 }
 }
 // Weather rests on the constructed surface. The same top edge supplies the
 // brushing contact; different crown heights never share an imaginary plane.
 const left=Math.max(0,Math.ceil(cx-w*.4)),right=Math.min(c.w-1,Math.floor(cx+w*.4)),tops=new Map();
 for(const f of c.fills)for(let xx=Math.max(left,f.x);xx<=Math.min(right,f.x+f.w-1);xx++)if(f.y<(tops.get(xx)??Infinity))tops.set(xx,f.y);
 for(let yy=0;yy<Math.min(c.h,y+1);yy++)for(let xx=left;xx<=right;xx++)if(c.art[yy][xx]!==' '&&yy<(tops.get(xx)??Infinity))tops.set(xx,yy);
 const surface=[...tops].sort((a,b)=>a[0]-b[0]),crown=surface.slice().sort((a,b)=>Math.abs(a[0]-cx)-Math.abs(b[0]-cx))[0]||[cx,top];
 if(v.snow>.12&&surface.length){const count=Math.ceil(v.snow*(large?12:3));for(let i=0;i<count;i++){const [xx,yy]=surface[Math.round(i*(surface.length-1)/Math.max(1,count-1))];c.put(xx,yy-1,'*','p');}}
 if(v.wet>.05&&surface.length){const count=Math.ceil(v.wet*(large?8:2));for(let i=0;i<count;i++){const [xx,yy]=surface[Math.round(i*(surface.length-1)/Math.max(1,count-1))];c.put(xx,yy+1,"'",'q');}}
 return {band:{x,y,w},crown:{x:crown[0],y:crown[1]},brim:{x:x+w,y},decoration:{x:cx,y:top-1}};
}
export function headwearSprite(base,item,time,{state={},motion=true}={}){
 const p=BLUEPRINTS[item.id];if(!p)return null;
 const c=new ObjectCanvas(p.w,p.h),material=hatMaterial(state.apparel||state),phase=motion?(Number.isFinite((state.apparel||state).phase)?material.phase:time*.9):0;
 const anchors=drawHat(c,p,{cx:46,bandY:57,w:43,large:true,material,phase});
 return {...base,...c.finish(),inks:{b:p.color,f:'#e9dfbf',a:'#d1b979',s:'#7e8986',k:'#343d3e',p:'#e4c9bd',q:'#92bfc9',g:'#85ad83'},panels:{b:p.color,a:'#8f7f59',p:'#b9a29c',q:'#577980',g:'#5d785b'},
  blueprint:item.id,construction:'headwear-v1',detail:true,detailScale:p.detailScale,anchors,animated:false,emissive:false,floor:false,sway:0,lift:0};
}

export function fittedHat(rig,id,{material={},phase=0}={}){
 const p=BLUEPRINTS[id];if(!p)return null;
 const h=rig.head,face=rig.faceBounds||h,w=h.w,W=Math.ceil(w*2.3)+12,H=Math.ceil(w*1.8)+12;
 const c=new ObjectCanvas(W,H),cx=Math.floor(W/2),bandY=H-4;
 const anchors=drawHat(c,p,{cx,bandY,w,material,phase});
 const x=Math.round(h.x+(w-1)/2-cx),y=h.y-bandY;
 const contacts={band:{x:h.x,y:h.y},brim:{x:h.x-1,y:h.y},crown:{x:Math.round(x+anchors.crown.x),y:Math.round(y+anchors.crown.y)},visor:{x:face.x-2,y:Math.round(face.y+face.h*.45)}};
 const m=c.finish();
 // A compact brim ends above the face. The helmet gets an open visor around
 // the actual bill/eye bounds instead of painting a glass disc over Cheese.
 if(p.shape==='helmet'){
  const visor=new ObjectCanvas(W,H+face.h+5);
  const left=h.x-x-2,right=face.x+face.w-x+1;
  // One continuous canopy around the real face, not a second glass hat stacked
  // above it. The open interior preserves the bill and expression at every age.
  visor.line(left,bandY,left+1,bandY-2,'/','a');visor.line(left+1,bandY-2,left+3,bandY-3,'/','a');
  visor.line(left+3,bandY-3,right-3,bandY-3,'_','a');visor.line(right-3,bandY-3,right,bandY,'\\','a');
  visor.put(left+3,bandY-2,'/','f');visor.put(left-1,bandY+1,'o','q');
  for(let row=0;row<face.h;row++){visor.put(left,bandY+row,'(','a');visor.put(right,bandY+row,')','a');}
  visor.line(left+1,bandY+face.h,right-1,bandY+face.h,'_','a');
  visor.put(left+1,bandY,hatMaterial(material).fog>.3?':':"'",'f');
  if(hatMaterial(material).snow>.12)visor.put(Math.round((left+right)/2),bandY-4,'*','p');
  if(hatMaterial(material).wet>.05)visor.put(right-1,bandY-1,"'",'q');
  contacts.crown={x:Math.round(x+(left+right)/2),y:y+bandY-3};
  const result=visor.finish();return {...result,x,y,bandY:rig.head.y,contacts};
 }
 m.art=m.art.map((r,row)=>row>bandY?' '.repeat(W):r);m.fills=m.fills.filter(f=>f.y<=bandY);
 return {...m,x,y,bandY:rig.head.y,contacts};
}
export function hatSummary(raw){const s=hatMaterial(raw);return [s.wet>.6?'Soaked':s.wet>.2?'Damp':s.wet>.05?'A few raindrops':'Dry',s.snow>.1?'snow caught on top':'',s.fog>.2?'mist around the visor rim':''].filter(Boolean).join(' · ');}
