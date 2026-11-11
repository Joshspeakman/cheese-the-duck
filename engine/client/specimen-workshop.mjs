import {ObjectCanvas} from './object-canvas.mjs';
import BLUEPRINTS from './animation/specimens.json' with {type:'json'};
export {BLUEPRINTS as SPECIMEN_BLUEPRINTS};

// Authored geological surfaces: outlines, cleavage planes and growth follow the
// material. No idle motion, random grain, inventory state or new care mechanics.
function path(c,points,glyph=null,tone='f'){
 for(let i=1;i<points.length;i++)c.line(...points[i-1],...points[i],glyph,tone);
}
function polygon(c,points,tone='b',edge='f'){
 const ys=points.map(p=>p[1]);
 for(let y=Math.min(...ys);y<Math.max(...ys);y++){
  const cuts=[];
  for(let i=0;i<points.length;i++){
   const a=points[i],b=points[(i+1)%points.length];
   if(a[1]!==b[1]&&y>=Math.min(a[1],b[1])&&y<Math.max(a[1],b[1]))cuts.push(a[0]+(y-a[1])*(b[0]-a[0])/(b[1]-a[1]));
  }
  cuts.sort((a,b)=>a-b);
  for(let i=0;i+1<cuts.length;i+=2){const x=Math.ceil(cuts[i]),end=Math.floor(cuts[i+1]);if(end>=x)c.solid(x,y,end-x+1,1,tone);}
 }
 path(c,[...points,points[0]],null,edge);
}
function facets(c,p){
 for(let i=0;i<p.outline.length;i++)polygon(c,[p.outline[i],p.outline[(i+1)%p.outline.length],p.hub],['b','a','s','k'][i%4],'s');
 path(c,[...p.outline,p.outline[0]],null,'f');
}
function arc(c,cx,cy,rx,ry,start,end,tone='a',glyph=null){
 let prev;
 for(let n=0;n<=48;n++){const a=start+(end-start)*n/48,next=[cx+Math.cos(a)*rx,cy+Math.sin(a)*ry];if(prev)c.line(...prev,...next,glyph,tone);prev=next;}
}
function spiral(c,p,chambers=false){
 let prev;
 const turns=p.turns||2.4,angle=turns*Math.PI*2;
 for(let n=0;n<=160;n++){
  const u=n/160,a=angle*u,r=.06+.94*u,point=[p.cx+Math.cos(a)*p.rx*r,p.cy+Math.sin(a)*p.ry*r];
  if(prev)c.line(...prev,...point,null,'a');
  if(chambers&&n>54&&n%9===0){const inner=Math.max(.06,r-.94/turns);c.line(p.cx+Math.cos(a-.13)*p.rx*inner,p.cy+Math.sin(a-.13)*p.ry*inner,...point,null,'f');}
  prev=point;
 }
}
function stone(c,p){
 if(p.mark==='plain')c.ellipse(29,22,17,8,'_','f',true);
 else if(p.mark==='polish')c.ellipse(30,21,19,10,'_','f',true);
 else if(p.mark==='band')c.ellipse(31,21,24,11,'_','f',true);
 else if(p.mark==='frost')polygon(c,p.outline,'w');
 else facets(c,p);
 for(const v of p.veins)path(c,v,null,p.mark==='cut'?'f':'a');
 switch(p.mark){
 case 'seal': c.ellipse(31,17,9,7,'_','a');path(c,[[31,11],[23,22],[39,22],[31,11]],null,'f');c.put(27,18,'--+--','a');break;
 case 'mica': for(const [x,y]of [[19,14],[31,12],[40,18],[25,25],[44,26]])c.rows([' /_','/=/'],x,y,'a');break;
 case 'frost': path(c,[[18,17],[23,15],[30,15]],':','f');path(c,[[23,23],[32,25],[40,23]],':','w');break;
 case 'polish': arc(c,30,20,12,7,3.5,4.8,'f');c.put(38,23,'__','a');break;
 case 'metal': c.put(29,14,'/==/','f');c.put(30,22,'[::]','k');break;
 case 'band': arc(c,30,21,20,7,.2,2.8,'s');break;
 case 'strata': path(c,[[12,23],[21,26],[30,24]],'_','s');c.put(37,18,'/::/','k');break;
 case 'ore': for(const [x,y]of [[18,12],[34,14],[40,23],[20,24]])c.rows(['/##/','\\##\\'],x,y,'k');c.put(29,22,'=o=','a');break;
 case 'star': c.put(29,17,'<+>','a');break;
 case 'plain': c.put(26,19,'__','s');break;
 }
}
function crystal(c,p,id){
 for(const points of p.prisms){
  const xs=points.map(a=>a[0]),ys=points.map(a=>a[1]),min=Math.min(...ys),max=Math.max(...ys),cx=(Math.min(...xs)+Math.max(...xs))/2;
  const hub=[Math.round(cx),Math.round(min+(max-min)*.35)];
  for(let i=0;i<points.length;i++)polygon(c,[points[i],points[(i+1)%points.length],hub],['w','b','k','a'][i%4],'s');
  path(c,[...points,points[0]],null,'f');c.line(...hub,cx,max-2,'|','a');
  if(max-min>14)c.line(cx-2,hub[1]+2,cx-2,max-5,':','w');
 }
 if(id==='mist_crystal'){arc(c,30,21,14,5,3.2,6.1,'w',':');arc(c,31,23,10,4,.2,2.8,'w',':');}
 if(id==='ice_crystal'){c.put(29,16,'-+-','f');path(c,[[27,12],[31,16],[35,12]],null,'f');}
 if(id==='crystal_plant')c.rows(['  _/=/\\=\\_',' /__/:|:\\__\\'],24,29,'s');
}
function sediment(c,p){
 polygon(c,p.outline,p.mark==='wetfolds'?'k':'b');
 if(p.mark==='granules'){
  // Nested sediment beds and a few coarse grains, aligned to the sand mound.
  for(const [y,x,w] of [[23,23,17],[26,17,28],[29,12,41]]){
   for(let i=0;i<w;i+=4)c.put(x+i,y,i%8===0?'o':'.','a');
   c.line(x+2,y+1,x+w-2,y+1,':','s');
  }
  c.put(29,20,'..o..','f');
 }else{
  arc(c,30,24,17,5,.2,2.8,'a');arc(c,29,20,12,4,3.2,5.9,'s');
  path(c,[[18,27],[24,24],[30,25],[36,29]],null,'s');
  path(c,[[35,16],[38,20],[45,23]],null,'k');
  if(p.mark==='wetfolds'){c.put(22,17,'~~~','w');c.put(39,27,'~~~','w');}else c.put(22,14,'___','a');
 }
}
function shell(c,p){
 const {cx,cy,rx,ry}=p;
 if(p.kind==='fan'){
  const points=[[cx-5,cy],[cx-8,cy-3]];
  for(let i=0;i<=p.ribs*2;i++){
   const a=Math.PI+i*Math.PI/(p.ribs*2),ridge=i%2===0?1:.94;
   points.push([Math.round(cx+Math.cos(a)*rx*ridge),Math.round(cy-4+Math.sin(a)*ry*ridge)]);
  }
  points.push([cx+8,cy-3],[cx+5,cy]);polygon(c,points,'b');
  for(let i=1;i<p.ribs;i++){
   const a=Math.PI+i*Math.PI/p.ribs;
   c.line(cx,cy-2,cx+Math.cos(a)*(rx-2),cy-4+Math.sin(a)*(ry-2),null,i%2?'a':'f');
  }
  for(const scale of [.5,.75])arc(c,cx,cy-4,rx*scale,ry*scale,Math.PI,Math.PI*2,'s',':');
  c.put(cx-5,cy,'[__|__|__]','a');
 }else if(p.kind==='spiral'){
  c.ellipse(cx,cy,rx,ry,'_','f',true);spiral(c,p);arc(c,43,25,7,5,-1.4,1.8,'f');c.put(39,28,'\\____/','a');
 }else if(p.kind==='spire'){
  polygon(c,[[10,28],[47,5],[50,9],[46,12],[50,15],[46,19],[50,23],[45,30],[30,32]],'b');
  for(const [x,y,r]of [[42,11,4],[37,16,7],[30,22,10]])arc(c,x,y,r,4,-.5,2.6,'a');
  c.ellipse(35,27,9,4,'_','k',true);arc(c,35,27,8,3,2.8,6,'f');
 }else{
  c.ellipse(cx,cy,rx,ry,'_','f',true);arc(c,cx,cy,rx-3,ry-2,.1,6.1,'s',':');
  for(let i=0;i<5;i++){
   const a=-Math.PI/2+i*Math.PI*2/5,tip=[cx+Math.cos(a)*14,cy+Math.sin(a)*8];
   path(c,[[cx+Math.cos(a-.65)*3,cy+Math.sin(a-.65)*2],tip,[cx+Math.cos(a+.65)*3,cy+Math.sin(a+.65)*2]],null,'a');
  }
  c.put(cx-1,cy,'(o)','f');
 }
}
function wood(c,p){
 polygon(c,p.outline,'b');for(const points of p.grain)path(c,points,null,'a');
 for(const [x,y]of p.knots){c.ellipse(x,y,4,2,'_','k');c.put(x-1,y,'(o)','a');}
 if(p.rings){const [x,y,rx,ry]=p.rings;c.ellipse(x,y,rx,ry,'_','f',true);for(const scale of [.7,.4])c.ellipse(x,y,rx*scale,ry*scale,'_','a');c.put(x,y,'.','k');}
}
const INKS={b:'#c0b8a0',f:'#f1e5c5',s:'#868b81',k:'#5e6c6b',a:'#d9bd7b',w:'#a6dfdf'};
const PANELS={b:'#4f5148',f:'#747367',s:'#41483f',k:'#263d3b',a:'#726044',w:'#3e6b72'};
function unit(v,fallback=0){return Number.isFinite(v)?Math.max(0,Math.min(1,v)):fallback;}
export function specimenSprite(base,item,time,{state={},motion=true}={}){
 const p=BLUEPRINTS[item?.id];if(!p)return null;
 const c=new ObjectCanvas(p.w,p.h);
 if(p.type==='stone')stone(c,p);
 else if(p.type==='crystal')crystal(c,p,item.id);
 else if(p.type==='sediment')sediment(c,p);
 else if(p.type==='shell')shell(c,p);
 else if(p.type==='wood')wood(c,p);
 else if(p.type==='fossil'){polygon(c,p.outline,'b');spiral(c,p,true);path(c,[[12,16],[15,13],[19,12]],':','s');path(c,[[42,27],[47,23],[49,21]],':','s');}
 else if(p.type==='pearl'){
  c.ellipse(p.cx,p.cy,p.rx,p.ry,'_','f',true);
  arc(c,p.cx,p.cy,p.rx-3,p.ry-2,-.7,2.8,'s',':');
  arc(c,p.cx-1,p.cy-1,10,7,3.5,5.3,'a');c.put(23,15,'__','f');c.put(23,16,'/  )','f');
  arc(c,p.cx,p.cy,12,8,.6,2.5,'w','_');
 }
 // Read-only, bounded material projection. Keep authored contours intact;
 // wetness darkens the lower surface, dirt settles there, wear dims highlights.
 const wet=unit(state.wetness),dirt=unit(state.dirt),wear=1-unit(state.condition,1);
 for(let y=0;y<p.h;y++)for(let x=0;x<p.w;x++){
  if(c.art[y][x]===' ')continue;
  if(wear>.3&&c.tones[y][x]==='f')c.tones[y][x]='s';
  if(wet>.2&&y>p.h*(1-wet*.5))c.tones[y][x]='w';
  if(dirt>.2&&y>p.h*(1-dirt*.3))c.tones[y][x]='k';
 }
 const inks={...INKS},panels={...PANELS};
 if(p.type==='crystal'||item.id==='sea_glass'){inks.b='#a4d3cf';inks.a='#d1eff0';panels.b='#375e60';panels.a='#446e77';panels.k='#193f51';}
 if(item.id==='ruby_gem'){inks.b='#e79ca5';inks.a='#f1bbc0';panels.b='#783d50';panels.a='#9a5060';}
 if(p.type==='wood'){inks.b='#bf9f70';inks.a='#dac08c';panels.b='#51432d';}
 return {...base,...c.finish(),construction:'specimen-v1',detail:true,detailScale:p.scale,blueprint:item.id,inks,panels,sway:0,lift:0,animated:false,emissive:false};
}
