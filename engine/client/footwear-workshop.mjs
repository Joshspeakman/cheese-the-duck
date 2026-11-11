import {ObjectCanvas} from './object-canvas.mjs';
import BLUEPRINTS from './animation/footwear.json' with {type:'json'};
export {BLUEPRINTS as FOOTWEAR_BLUEPRINTS};
const clamp=v=>Math.max(0,Math.min(1,Number.isFinite(v)?v:0));
export function shoeMaterial(raw={},index=0){const side=index?'right':'left';return Object.fromEntries(['wet','snow','soil','slack'].map(k=>[k,clamp(raw[k+'_'+side]??raw[k])]));}
export function footwearColors(p){return {b:p.color,a:p.trim,f:'#e7dfc7',s:'#697774',k:'#283c36',q:'#9dc6cd',g:'#90ad7c',p:'#d8959d'};}
function polygon(c,points,tone='b',edge='a'){
 for(let y=Math.ceil(Math.min(...points.map(p=>p[1])));y<=Math.floor(Math.max(...points.map(p=>p[1])));y++){
  const cuts=[];for(let i=0;i<points.length;i++){const a=points[i],b=points[(i+1)%points.length];if((a[1]<=y&&b[1]>y)||(b[1]<=y&&a[1]>y))cuts.push(a[0]+(b[0]-a[0])*(y-a[1])/(b[1]-a[1]));}
  cuts.sort((a,b)=>a-b);for(let i=0;i+1<cuts.length;i+=2)c.solid(Math.ceil(cuts[i]),y,Math.floor(cuts[i+1])-Math.ceil(cuts[i])+1,1,tone);
 }
 points.forEach((a,i)=>c.line(...a,...points[(i+1)%points.length],null,edge));
}
function shoe(c,p,v,phase){
 if(p.shape==='boot'||p.shape==='skate'){
  const cuff=p.style==='quilt'?13:p.shape==='skate'?18:9;
  polygon(c,[[6,cuff],[23,cuff],[24,34],[28,40],[37,43],[40,49],[37,54],[6,54],[3,50],[4,36]],'b');
  c.ellipse(14.5,cuff,8.5,3,'=','a',true);c.ellipse(14.5,cuff,5.5,1,'_','k',true);
  c.line(7,cuff+4,6,42,':','s');c.line(8,49,35,49,':','a');
  c.line(5,54,38,54,'=','s');c.line(5,56,37,56,'_','k');
  for(let x=7;x<37;x+=4)c.put(x,55,'|','a');
  c.line(7,45,12,38,'/','s');c.line(12,38,29,42,'~','s');
  if(p.style==='rubber'){c.rect(9,20,10,6,'a');c.rows(['~~~',' v '],12,22,'f');c.line(22,15,22,34,'|','f');c.rows([' /~~.'],27,44,'f');}
  if(p.style==='daisy'){for(const [x,y]of [[10,18],[15,31],[29,44]])c.rows([' .o.','o(*)o'," 'o'"],x,y,'a');c.line(15,23,13,28,'/','g');}
  if(p.style==='leather'||p.shape==='skate'){
   for(let y=cuff+6;y<39;y+=4){c.put(10,y,'o','s');c.put(20,y,'o','s');c.line(11,y,19,y+3,'/','a');c.line(11,y+3,19,y,'\\','a');}
   const dx=Math.round(Math.sin(phase)*v.slack*2);c.rows(['><','| \\'],14+dx,cuff+4,'f');
   c.line(25,42,33,45,':','a');if(p.style==='leather')c.rect(5,34,7,5,'s');
  }
  if(p.style==='quilt'){for(let y=cuff+6;y<39;y+=5)c.line(6,y,22,y,'=','s');c.line(5,cuff,24,cuff,'~','f');c.line(6,cuff+2,23,cuff+2,'o','f');c.rect(10,31,11,5,'s');c.put(15,33,'+','a');}
  if(p.shape==='skate'){c.line(10,57,10,61,'|','s');c.line(29,57,29,61,'|','s');c.line(4,62,36,62,'=','q');c.line(4,63,39,63,'_','f');c.rows([' /','/'],38,60,'q');c.put(35,64,"'",'s');}
 }else if(p.shape==='slipper'){
  c.ellipse(21,45,18,10,'~','b',true);c.ellipse(12,40,8,6,'~','f',true);c.ellipse(12,40,5,3,'_','k',true);
  c.ellipse(29,42,8,7,'~','b',true);c.ellipse(25,30,3,9,'~','b',true);c.ellipse(33,29+Math.sin(phase)*2,3,10,'~','b',true);
  c.line(25,24,25,32,':','p');c.line(33,22,33,31,':','p');c.put(26,41,'o   o','k');c.put(29,43,'v','p');c.put(25,45,'--+--','f');
  c.line(6,54,34,54,'=','s');for(let y=44;y<52;y+=3)c.put(8,y,'v :','a');
 }else{
  c.ellipse(21,46,18,11,'_','s',true);c.ellipse(21,44,16,10,'_','b',true);
  for(let y=38;y<52;y+=3)c.line(10,y,30,y,'.','a');
  c.line(8,48,23,36,'/','a');c.line(9,49,24,37,'/','f');c.line(23,36,33,48,'\\','a');c.line(24,37,34,49,'\\','f');
  c.put(23,37,'o','k');for(let x=12;x<32;x+=4)c.put(x,55,':','a');
 }
 if(v.soil>.18){c.rows(['.: :.:',' :: .'],26,50,'k');}
 if(v.wet>.2){c.put(31,47,"'",'q');c.put(34,49,':','q');}
 if(v.snow>.15)c.put(23,p.shape==='sandal'?37:p.shape==='slipper'?37:43,'*..*','f');
 if(v.slack>.3&&p.shape==='sandal')c.line(23,36,33,46,'~','a');
}
export function footwearSprite(base,item,time,{state={},motion=true}={}){
 const p=BLUEPRINTS[item.id];if(!p)return null;const raw=state.apparel||state,phase=motion?(Number.isFinite(raw.phase)?raw.phase:time*1.2):0,c=new ObjectCanvas(p.w,p.h);
 shoe(c.view(5,1),p,shoeMaterial(raw,0),phase);shoe(c.view(54,7),p,shoeMaterial(raw,1),phase+.8);
 const colors=footwearColors(p);return {...base,...c.finish(),inks:colors,panels:{...colors,k:'#142b27',s:'#253d36'},construction:'footwear-v1',blueprint:item.id,detail:true,detailScale:p.detailScale,animated:false,emissive:false,floor:false,sway:0,lift:0};
}
export function fittedFootwear(rig,id,{material={},phase=0}={}){
 const p=BLUEPRINTS[id];if(!p)return null;const front=new ObjectCanvas(76,48),back=new ObjectCanvas(76,48),feet=[],small=rig.small;
 for(const [i,foot]of rig.feet.entries()){
  const v=shoeMaterial(material,i),x=foot.x-1,y=foot.y;
  let rows;
  if(p.shape==='boot'){
   rows=small?['[~]',p.style==='daisy'?'|*>':p.style==='quilt'?'|=>':p.style==='leather'?'|x>':'|_>']:['[~]',p.style==='daisy'?'|*|':p.style==='quilt'?'|=|':p.style==='leather'?'|x|':'|:|','|__>'];
  }else if(p.shape==='slipper')rows=small?[Math.sin(phase+i)>.4?'|/':'||','(o>']:[Math.sin(phase+i)>.4?'| /':'| |','(o >',"'~~>"];
  else if(p.shape==='skate')rows=small?['[x]','|_>','===']:['[xx]','|__>','===='];
  else rows=small?[' /\\','(__']:[' /\\','(__>'];
  const top=y-rows.length+1;front.rows(rows,x,top,'b',true);
  const width=Math.max(...rows.map(r=>r.length));
  if(p.shape==='skate')front.line(x,y,x+width-1,y,'=','q');
  else if(p.shape!=='slipper'){front.line(x,y,x+width-2,y,'_','s');front.put(x+width-1,y,'>','a');}
  if(v.soil>.2)front.put(x+1,y,':','k');
  if(v.wet>.2)front.put(x+width-1,y-1,"'",'q');
  if(v.snow>.2)front.put(x+width-2,top,'*','f');
  if(v.slack>.3)front.put(x+1,top,p.shape==='skate'?'~':p.shape==='sandal'?'/':'o','a');
  feet.push({sole:{x:x+1,y},cuff:{x:x+1,y:top},toe:{x:x+width-1,y:y-1},bounds:{x,y:top,w:width,h:rows.length}});
 }
 const target=feet[rig.hatCare?.footIndex||0]||{};
 return {front:front.finish(),back:back.finish(),contacts:target,feet};
}
export function footwearSummary(raw={}){
 const description=i=>{const v=shoeMaterial(raw,i);return [v.wet>.6?'soaked':v.wet>.2?'damp':'dry',v.snow>.15?'snowy':'',v.soil>.18?'muddy':'',v.slack>.18?'loose':''].filter(Boolean).join(', ');};
 return 'Left: '+description(0)+' · Right: '+description(1);
}
