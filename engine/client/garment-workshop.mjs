import {ObjectCanvas} from './object-canvas.mjs';
import BLUEPRINTS from './animation/garments.json' with {type:'json'};
export {BLUEPRINTS as GARMENT_BLUEPRINTS};
const clamp=v=>Math.max(0,Math.min(1,Number.isFinite(v)?v:0));
export function garmentMaterial(raw={}){return {...Object.fromEntries(['wet','snow','wind','soil','slack','crease'].map(k=>[k,clamp(raw[k])])),phase:Number.isFinite(raw.phase)?raw.phase:0};}
const shade=(hex,n)=>'#'+hex.slice(1).match(/../g).map(s=>Math.max(0,Math.min(255,Math.round(parseInt(s,16)*n))).toString(16).padStart(2,'0')).join('');
export function garmentColors(p,raw={}){const v=garmentMaterial(raw);return {b:shade(p.color,1-v.wet*.18),a:p.trim,f:'#e7dfbf',s:shade(p.color,.68),k:'#263d38',g:'#8fa979',q:'#a2c2c5',p:'#d2a293'};}
const inside=(x,y,r)=>r&&x>=r.x&&x<r.x+r.w&&y>=r.y&&y<r.y+r.h;
function polygon(c,points,tone='b',edge='a'){
 for(let y=Math.ceil(Math.min(...points.map(p=>p[1])));y<=Math.floor(Math.max(...points.map(p=>p[1])));y++){
  const cuts=[];for(let i=0;i<points.length;i++){const a=points[i],b=points[(i+1)%points.length];if((a[1]<=y&&b[1]>y)||(b[1]<=y&&a[1]>y))cuts.push(a[0]+(b[0]-a[0])*(y-a[1])/(b[1]-a[1]));}
  cuts.sort((a,b)=>a-b);for(let i=0;i+1<cuts.length;i+=2)c.solid(Math.ceil(cuts[i]),y,Math.max(1,Math.floor(cuts[i+1])-Math.ceil(cuts[i])+1),1,tone);
 }
 points.forEach((a,i)=>c.line(...a,...points[(i+1)%points.length],null,edge));
}
function line(c,pts,ch=':',tone='a'){for(let i=1;i<pts.length;i++)c.line(...pts[i-1],...pts[i],ch,tone);}
function patch(c,x,y,kind){
 if(kind==='palm')c.rows([' \\|/','--+--',' /|\\','  |  ',' /   '],x,y,'g');
 else if(kind==='hibiscus')c.rows([' .o. ','o(*)o'," 'o' "],x,y,'a');
 else if(kind==='star')c.rows(['  |  ','-<*>-','  |  '],x,y,'a');
}
function pocket(c,x,y,w,h,{flap=true}={}){c.rect(x,y,w,h,'s');c.line(x+1,y+1,x+w-2,y+1,':','a');if(flap){polygon(c,[[x,y],[x+w-1,y],[x+w-2,y+3],[x+1,y+3]],'b');c.put(x+w/2,y+2,'o','f');}c.line(x+1,y+h-2,x+w-2,y+h-2,':','a');}
function largeGarment(c,p,v,phase){
 const contacts={},sway=Math.sin(phase)*(1+v.wind*2)*(1-v.wet*.65),shape=p.shape;
 if(shape==='cape'){
  const hem=60+v.slack*2,dx=sway*2;
  polygon(c,[[39,12],[48,16],[57,12],[66,29],[77+dx,hem],[62,hem-2],[48+dx*.5,hem+3],[34,hem-1],[19+dx,hem],[30,29]],'b');
  line(c,[[34,23],[29+dx*.3,42],[24+dx,hem-3]],':','s');line(c,[[61,23],[67+dx*.3,44],[72+dx,hem-3]],':','s');
  for(let i=0;i<4;i++)line(c,[[38+i*7,19],[34+i*9,40],[31+i*11+dx,hem-4]],i%2?'|':':','s');
  c.rows([' .--o--. ',"'-------'"],44,16,'a');
  if(p.style==='shield'){polygon(c,[[36,29],[60,29],[58,44],[48,51],[38,44]],'a','f');patch(c,46,35,'star');c.put(46,43,'==','b');}
  else if(p.style==='lightning')polygon(c,[[49,27],[40,41],[48,40],[43,52],[59,35],[50,36],[55,27]],'a','f');
  else {line(c,[[32,51],[37,44],[42,48],[49,37],[57,45],[63,40]],'^','g');for(let i=0;i<5;i++)c.put(33+i*7,56,'.o.','a');}
  contacts.hem={x:Math.round(48+dx*.5),y:Math.round(hem+3)};contacts.shoulder={x:48,y:17};contacts.front={x:48,y:38};contacts.seam={x:30,y:39};
 }else if(shape==='bag'){
  c.rows(['  .--------.  ',' / .------. \\',' | |      | |'],40,8,'s');
  for(const side of [-1,1]){polygon(c,[[48+side*14,17],[48+side*24,21],[48+side*26,58],[48+side*21,64],[48+side*17,58]],'s');c.line(48+side*22,26,48+side*23,54,':','a');}
  polygon(c,[[30,17],[66,17],[69,26],[68,59],[61,65],[35,65],[28,59],[27,26]],'b');
  for(let y=25;y<59;y+=4)c.line(32,y,63,y,'.','s');
  const flap=25+Math.sin(phase)*v.slack*2;
  polygon(c,[[28,18],[68,18],[65,flap+5],[55,flap+9],[39,flap+9],[30,flap+5]],'b');line(c,[[30,20],[33,flap+3],[40,flap+6],[54,flap+6],[62,flap+3],[66,20]],':','a');
  for(const x of [36,57]){c.rect(x,24,4,19,'s',true);c.rect(x-1,32,6,5,'a');c.put(x+1,34,'+','f');}
  pocket(c,34,46,13,14);pocket(c,51,46,11,12);
  contacts.shoulder={x:42,y:18};contacts.pocket={x:40,y:53};contacts.seam={x:29,y:44};contacts.hem={x:48,y:65};contacts.front={x:48,y:38};
 }else if(shape==='sash'){
  polygon(c,[[61,12],[71,18],[37+sway,64],[24+sway,61]],'b');
  line(c,[[62,17],[30+sway,60]],':','a');line(c,[[67,19],[35+sway,60]],':','a');
  for(let i=0;i<4;i++)patch(c,56-i*6,23+i*9,'star');
  c.ellipse(61,23,8,6,'*','a',true);c.ellipse(61,23,4,3,'o','b',true);c.put(60,23,'+','f');
  contacts.front={x:61,y:23};contacts.shoulder={x:64,y:16};contacts.hem={x:31,y:61};contacts.seam={x:45,y:43};
 }else{
  const hem={knit:57,shirt:54,tuxedo:62,robe:66,suit:62,raincoat:61,coat:61,pumpkin:61,ghost:65,elf:61}[shape],dx=sway*(shape==='ghost'?1.5:.4);
  if(['raincoat','coat'].includes(shape)){c.ellipse(48,16,13,10,'~','b',true);c.ellipse(48,15,9,6,'_','k',true);}
  const outlines={
   knit:[[40,13],[29,17],[17,22],[17,33],[28,32],[26,44],[29,hem-4],[35,hem],[61,hem],[67,hem-4],[70,44],[68,32],[79,33],[79,22],[67,17],[56,13],[54,20],[42,20]],
   shirt:[[40,13],[28,18],[14,24],[20,35],[29,31],[28,hem],[68,hem],[67,31],[76,35],[82,24],[68,18],[56,13],[53,19],[43,19]],
   tuxedo:[[40,13],[30,17],[19,22],[20,34],[29,30],[29,hem-4],[40,hem],[48,hem-9],[56,hem],[67,hem-4],[67,30],[76,34],[77,22],[66,17],[56,13],[53,19],[43,19]],
   robe:[[40,13],[30,18],[18,24],[12,42],[29,36],[22,hem],[74,hem],[67,36],[84,42],[78,24],[66,18],[56,13],[53,19],[43,19]],
   pumpkin:[[39,15],[29,18],[20,27],[17,38],[20,50],[28,58],[39,hem],[57,hem],[68,58],[76,50],[79,38],[76,27],[67,18],[57,15],[54,20],[42,20]],
   ghost:[[39,13],[29,18],[21,30],[15+dx,hem-5],[26+dx,hem],[39+dx,hem-3],[50+dx,hem],[63+dx,hem-3],[78+dx,hem],[73,30],[67,18],[57,13],[54,20],[42,20]],
   coat:[[40,13],[29,17],[17,23],[18,34],[28,32],[26,40],[29,44],[26,49],[29,54],[31,hem],[65,hem],[67,54],[70,49],[67,44],[70,40],[68,32],[78,34],[79,23],[67,17],[56,13],[53,19],[43,19]]
  };
  polygon(c,outlines[shape]||[[40,13],[30,17],[17,22],[19,32],[29,30],[28,hem-8],[34+dx,hem],[61+dx,hem],[68,hem-8],[67,30],[77,32],[79,22],[66,17],[56,13],[53,19],[43,19]],'b');
  const spans=c.fills.filter(f=>f.tone==='b'&&f.y>=21&&f.y<hem-2);
  for(const f of spans)for(let x=f.x+2;x<f.x+f.w-2;x++){
   const y=f.y;if(x<30||x>66)continue;
   if(shape==='knit'){
    if(p.style==='cable'&&x%8===0)c.put(x,y,y%4<2?'(':')','a');
    else if(p.style==='fair_isle'&&y%10<3)c.put(x,y,(x+y)%4===0?'X':'.','a');
    else if(x%3===y%2&&y%2===0)c.put(x,y,'v','s');
   }else if(shape==='coat'){if(y%7===0)c.put(x,y,'=','a');else if(y%7===3&&x%9===0)c.put(x,y,'.','f');}
   else if(shape==='ghost'&&x%9===0)c.put(x+Math.round(Math.sin(y*.22+phase)),y,'|','s');
   else if(shape==='pumpkin'&&x%8===0)c.put(x,y,'(','a');
   else if(y%5===0&&x%5===0)c.put(x,y,'.','s');
  }
  for(const side of [-1,1]){line(c,[[48+side*10,19],[48+side*17,26],[48+side*16,hem-7]],':','s');c.line(48+side*23,27,48+side*27,29,'=','a');}
  if(shape==='knit'){c.line(34,hem-2,61,hem-2,'=','a');for(let x=36;x<61;x+=3)c.put(x,hem-1,'|','f');c.line(42,20,54,20,'v','a');}
  if(shape==='shirt'){
   polygon(c,[[40,14],[48,23],[38,27],[32,18]],'a');polygon(c,[[56,14],[48,23],[58,27],[64,18]],'a');
   for(const [x,y]of [[34,31],[55,33],[35,44],[55,46]])patch(c,x,y,p.style);
   c.line(48,25,48,hem-2,':','s');for(let y=28;y<hem-2;y+=7)c.put(48,y,'o','f');pocket(c,55,26,8,9,{flap:false});
  }else if(shape==='tuxedo'){
   polygon(c,[[42,19],[54,19],[50,45],[46,45]],'f','a');polygon(c,[[36,17],[47,43],[39,37],[34,24]],'s','f');polygon(c,[[60,17],[49,43],[57,37],[62,24]],'s','f');
   c.rows(['>o<'],47,22,'a');for(let y=28;y<44;y+=5)c.put(48,y,'o','k');pocket(c,55,30,9,5,{flap:false});c.rows([' /\\'],57,27,'f');c.line(48,46,48,hem-1,'|','s');
  }else if(shape==='robe'){
   for(const [x,y]of [[36,27],[55,35],[35,49]])patch(c,x,y,'star');c.rows([' .-.','(   '," '-'"] ,55,49,'a');
   c.line(48,21,48,hem-2,'|','a');c.line(31,43,65,43,'=','s');c.rows(['[o]',' |:',' |:'],46,42,'a');
  }else if(shape==='suit'){
   c.line(48,21,48,hem-1,'~','f');for(const x of [47,49])c.line(x,21,x,hem-1,':','a');
   c.line(30,45,66,45,'=','k');c.line(30,46,66,46,'=','k');c.rect(44,43,9,6,'a');c.put(48,45,'+','f');c.line(34,hem-1,61,hem-1,'o','f');
  }else if(['raincoat','coat'].includes(shape)){
   c.rect(47,21,4,hem-24,'s',true);for(let y=24;y<hem-3;y+=6)c.put(49,y,'o','a');
   pocket(c,33,42,10,12);pocket(c,55,42,10,12);
   if(p.style==='petal_seams'){patch(c,34,28,'hibiscus');line(c,[[32,36],[39,38],[44,36]],'~','a');}
   else c.line(34,29,44,29,'=','a');
  }else if(shape==='pumpkin'){
   for(const side of [-1,1])polygon(c,[[48+side*6,30],[48+side*12,35],[48+side*4,35]],'k','s');
   c.rows([' \\__  __/ ','    \\_/   '],43,44,'k');for(let x=38;x<59;x+=4)c.put(x,20,'v','g');
  }else if(shape==='ghost'){
   for(let x=34;x<62;x+=6)c.rows([' | '," '~'"],x,hem-2,'a');c.rows(['.o.'],45,23,'a');
   line(c,[[37,25],[34,38],[36,54]],':','a');line(c,[[59,25],[62,38],[59,54]],':','a');
  }else if(shape==='elf'){
   for(let x=34;x<63;x+=7){polygon(c,[[x,hem-5],[x+6,hem-5],[x+3,hem+2]],'b','a');c.put(x+3,hem+3,'o','a');}
   c.line(31,42,65,42,'=','s');c.rect(44,40,9,5,'a');for(let x=39;x<57;x+=6)c.put(x,21,'v','a');
  }
  contacts.shoulder={x:35,y:20};contacts.front={x:60,y:34};contacts.hem={x:39,y:hem-1};contacts.seam={x:29,y:40};contacts.pocket={x:60,y:48};
 }
 if(v.crease>.18){const a=contacts.front;line(c,[[a.x-5,a.y-2],[a.x,a.y+2],[a.x+4,a.y]],'~','s');}
 if(v.soil>.15){const a=contacts.hem;c.rows(['.: :.', ' :: '],a.x-2,a.y-3,'k');}
 if(v.wet>.15){const a=contacts.seam;c.put(a.x,a.y+2,"'",'q');c.put(a.x+3,a.y+5,':','q');}
 if(v.snow>.15){const a=contacts.shoulder;c.put(a.x-2,a.y-1,'*..*','f');}
 return contacts;
}
export function garmentSprite(base,item,time,{state={},motion=true}={}){
 const p=BLUEPRINTS[item.id];if(!p)return null;
 const raw=state.apparel||state,v=garmentMaterial(raw),phase=motion?(Number.isFinite(raw.phase)?v.phase:time*1.2):0,c=new ObjectCanvas(p.w,p.h),anchors=largeGarment(c,p,v,phase),colors=garmentColors(p,v);
 return {...base,...c.finish(),inks:colors,panels:{...colors,k:'#142c28',s:shade(colors.b,.6)},blueprint:item.id,construction:'garment-v1',detail:true,detailScale:p.detailScale,anchors,animated:false,emissive:false,floor:false,sway:0,lift:0};
}
// Compact patterns are cut to each posed torso, not scaled down from a plate.
export function fittedGarment(rig,id,{material={},phase=0}={}){
 const p=BLUEPRINTS[id];if(!p)return null;
 const v=garmentMaterial(material),front=new ObjectCanvas(76,48),back=new ObjectCanvas(76,48),b=rig.body,h=rig.faceBounds||rig.head,wing=rig.wing,contactCandidates=[];
 const allowable=(x,y)=>!inside(x,y,h)&&!inside(x,y,wing)&&!rig.feet.some(f=>y===f.y&&x>=f.x&&x<f.x+2);
 const shoulderSpan=rig.torso.find(r=>r.w>=Math.min(6,b.w)&&r.y>=b.y+1)||rig.torso[0];
 const shoulder={x:shoulderSpan.x,y:shoulderSpan.y};
 if(p.slot==='back'){
  const compact=rig.small||b.h<5,anchor={x:shoulder.x,y:shoulder.y},width=compact?3:5,sway=Math.round(Math.sin(phase)*(v.wind+.65)*(1-v.wet*.7)),length=Math.max(0,Math.min(rig.action==='sleeping'?3:7,b.y+b.h-1-anchor.y));
  if(p.shape==='cape'){
   if(length<2){
    // A tucked/swimming body carries the cloth along its back, above the waterline.
    polygon(back,[[anchor.x,anchor.y],[anchor.x-2,anchor.y-1],[b.x-width,anchor.y-1],[b.x-width-1+sway,anchor.y],[anchor.x,anchor.y]],'b');
    back.put(b.x-width+1,anchor.y,p.style==='shield'?'*':p.style==='lightning'?'/':':','a');
   }else{
   polygon(back,[[anchor.x,anchor.y],[anchor.x+2,anchor.y+1],[b.x-1+sway,anchor.y+length-1],[b.x-width+sway,anchor.y+length],[b.x-width+1,anchor.y+length-2]],'b');
   line(back,[[anchor.x-1,anchor.y+1],[b.x-2+sway,anchor.y+length-1]],':','a');
   back.put(b.x-width+2+sway,anchor.y+length-2,p.style==='shield'?'*':p.style==='lightning'?'/':':','a');
   }
  }else{
   const x=b.x-width+1,height=compact?3:5,y=Math.min(anchor.y+1+Math.round(v.slack),b.y+b.h-height);
   back.rows(compact?['._.',Math.sin(phase)>.5?'|+|':'|o|','\'~\'']:[' .---.','/____|',Math.sin(phase)>.5?'|[+] |':'|[o] |','|_|__|',"'----'"],x,y,'b',true);
   line(back,[[x+width,y],[anchor.x-1,Math.min(anchor.y+1,b.y+b.h-1)]],'/','s');back.put(x+1,y+height-2,v.soil>.2?':':'=','a');
  }
  // A visible fastening joins the rear panel to the actual shoulder contour.
  front.put(anchor.x,anchor.y,v.slack>.3?'o':'@','a');front.fills.push({x:anchor.x,y:anchor.y,w:1,tone:'b',opaque:true});
 }else{
  for(const [j,span]of rig.torso.entries())for(let x=span.x+(span.w>10?2:0);x<span.x+span.w;x++){
   const y=span.y;if(!allowable(x,y))continue;
   const q=x-span.x,edge=x===span.x+(span.w>10?2:0)||x===span.x+span.w-1,first=j===0,last=j===rig.torso.length-1;
   if(p.shape==='sash'&&Math.abs(x-(span.x+span.w-2-Math.floor(j*.7)))>1)continue;
   let ch=' ',tone='b';
   if(first){ch=v.slack>.3?'~':p.shape==='knit'?'=':p.shape==='shirt'?'v':'_';tone='a';}
   else if(last){ch=p.shape==='elf'?'v':p.shape==='ghost'?'~':p.shape==='knit'?'=':'_';tone='a';}
   else if(edge){ch=x<span.x+span.w/2?'/':'\\';tone='s';}
   else if(p.shape==='knit'){ch=p.style==='cable'?(q%4===0?j%2?'(':')':(q+j)%3===0?'v':' '):(j%3===0?'X':q%3===0?'.':' ');tone='a';}
   else if(p.shape==='shirt'){ch=(q+j*2)%7===0?'*':(q+j*2)%7===1?p.style==='palm'?'|':'/':' ';tone=(q+j*2)%7===0?'a':'g';}
   else if(p.shape==='tuxedo'){ch=x>span.x+span.w-4?j%2?'o':'|':'/';tone=x>span.x+span.w-4?'f':'s';}
   else if(p.shape==='robe'){ch=(q+j)%5===0?'*':q%4===0?':':' ';tone='a';}
   else if(p.shape==='suit'){ch=q%6===0?'~':j===Math.floor(b.h*.6)?'=':' ';tone=q%6===0?'f':'k';}
   else if(p.shape==='raincoat'){ch=q%5===0?'o':(q+j)%4===0?'|':' ';tone=q%5===0?'a':'s';}
   else if(p.shape==='coat'){ch=j%2===0?'=':q%4===0?'.':' ';tone=j%2===0?'a':'s';}
   else if(p.shape==='pumpkin'){ch=q%4===0?'(':j===2?'v':' ';tone='a';}
   else if(p.shape==='ghost'){ch=q%4===0?'|':(q+j)%5===0?'.':' ';tone='s';}
   else if(p.shape==='elf'){ch=q%5===0?'o':j===Math.floor(b.h*.6)?'=':' ';tone='a';}
   else if(p.shape==='sash'){ch=j===1?'*':'/';tone='a';}
   if(v.crease>.2&&!first&&!last&&(q+j)%4===0){ch='~';tone='s';}
   if(v.soil>.2&&j>rig.torso.length*.5&&q%3===0){ch=':';tone='k';}
   if(v.snow>.2&&first&&q%2===0){ch='*';tone='f';}
   if(v.wet>.2&&!first&&!last&&(q+j)%7===0){ch="'";tone='q';}
   if(rig.hatCare?.id==='wring_hem'&&last&&Math.abs(rig.hatCare.sweep)>.3)ch=':';
   front.solid(x,y,1,1,'b');if(ch!==' ')front.put(x,y,ch,tone);
  }
 }
 // Only choose targets from cloth that remains visible after depth masking.
 const underFeathers=(x,y)=>(rig.occlusion||rig.torso)?.some(f=>f.y===y&&x>=f.x&&x<f.x+f.w)??inside(x,y,b);
 for(const [c,rear]of [[front,false],[back,true]])for(const f of c.fills)for(let x=f.x;x<f.x+f.w;x++){
  if(inside(x,f.y,h)||rear&&underFeathers(x,f.y))continue;contactCandidates.push({x,y:f.y});
 }
 for(let y=0;y<48;y++)for(let x=0;x<76;x++)if(back.art[y][x]!==' '&&!underFeathers(x,y)&&!inside(x,y,h))contactCandidates.push({x,y});
 const closest=target=>contactCandidates.reduce((best,p)=>!best||Math.hypot(p.x-target.x,p.y-target.y)<Math.hypot(best.x-target.x,best.y-target.y)?p:best,null);
 const contacts={shoulder:closest(shoulder),front:closest({x:b.x+b.w-3,y:b.y+2}),seam:closest({x:p.slot==='back'?b.x-2:b.x+b.w-2,y:b.y+b.h*.55}),hem:closest({x:p.slot==='back'?b.x-3:b.x+b.w*.65,y:b.y+b.h-1}),pocket:closest({x:p.slot==='back'?b.x-2:b.x+b.w-3,y:b.y+b.h*.65})};
 return {front:front.finish(),back:back.finish(),contacts};
}
export function garmentSummary(raw={}){const v=garmentMaterial(raw);return [v.wet>.6?'Soaked':v.wet>.2?'Damp':'Dry',v.snow>.15?'snow on the cloth':'',v.soil>.18?'mud on the seams':'',v.slack>.18?'needs settling':'',v.crease>.2?'rumpled':''].filter(Boolean).join(' · ');}
