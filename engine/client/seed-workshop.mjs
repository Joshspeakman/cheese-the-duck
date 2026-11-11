import {ObjectCanvas} from './object-canvas.mjs';
import BLUEPRINTS from './animation/seeds.json' with {type:'json'};
export {BLUEPRINTS as SEED_BLUEPRINTS};
const inks={b:'#d8b17c',f:'#f5dfac',k:'#807052',s:'#90816c',w:'#9acbd4',r:'#df8c87',g:'#9abb77',a:'#efcf69',n:'#b7a8db',c:'#b7e1e0'};
const panels={b:'#84633e',f:'#b79b6b',k:'#38362a',s:'#62503b',w:'#446b76',r:'#8e5252',g:'#4c6540',a:'#9c7837',n:'#514566',c:'#4c8089'};
function poly(c,pts,t='b'){
 for(let y=Math.min(...pts.map(p=>p[1]));y<=Math.max(...pts.map(p=>p[1]));y++){
  const cuts=[];pts.forEach((a,i)=>{const b=pts[(i+1)%pts.length];if(a[1]!==b[1]&&y>=Math.min(a[1],b[1])&&y<Math.max(a[1],b[1]))cuts.push(a[0]+(y-a[1])*(b[0]-a[0])/(b[1]-a[1]));});
  cuts.sort((a,b)=>a-b);for(let i=0;i+1<cuts.length;i+=2)c.solid(Math.ceil(cuts[i]),y,Math.floor(cuts[i+1])-Math.ceil(cuts[i])+1,1,t);
 }
 pts.forEach((a,i)=>c.line(...a,...pts[(i+1)%pts.length],null,t));
}
function grain(c,x,y,rx=7,ry=4,t='b'){
 poly(c,[[x-rx,y],[x-rx+3,y-ry],[x+rx-3,y-ry+1],[x+rx,y],[x+rx-3,y+ry],[x-rx+2,y+ry-1]],t);
 c.line(x-rx+3,y,x+rx-3,y,'-','f');c.put(x-rx+2,y+1,"'",'k');
}
function almond(c,x,y,rx=6,ry=10,t='b'){
 poly(c,[[x,y-ry],[x+rx,y-2],[x+rx-1,y+ry-3],[x,y+ry],[x-rx,y+ry-3],[x-rx,y-2]],t);
 c.line(x,y-ry+3,x+1,y+ry-3,':','f');
}
function flower(c,x,y,kind){
 c.line(x,y,x,y+10,'|','g');c.rows(['<\\|','  |/>'],x-2,y+5,'g');
 if(kind==='tulip')c.rows(['\\ /\\ /',' \\  /','  \\/'],x-3,y-3,'r');
 if(kind==='rose'){c.ellipse(x,y,6,4,'~','r',true);c.rows([' /~\\','( @ )',' \\_/'],x-2,y-1,'f');}
 if(kind==='mint'){for(const [dx,dy]of [[-5,1],[4,4],[-5,7]]){poly(c,[[x,y+dy],[x+dx,y+dy-3],[x+dx*1.5,y+dy],[x+dx,y+dy+2]],'g');c.line(x,y+dy,x+dx,y+dy,':','f');}}
}
function packet(c,id){
 // A sealed paper seed envelope: folds and printed crop artwork, never a growing plant.
 const long=id==='carrot_seeds',left=long?19:12,right=long?45:52,top=long?4:7;
 poly(c,[[left,top+5],[left+5,top],[right-4,top],[right,top+5],[right-1,38],[left+1,38]],'f');
 c.line(left+1,top+6,right-1,top+6,'_','b');c.line(left+5,top,left+12,top+6,'\\','b');c.line(right-4,top,right-12,top+6,'/','b');
 c.line(left+2,35,right-2,35,'_','b');c.line(left+2,36,left+8,33,'/','b');c.line(right-2,36,right-8,33,'\\','b');
 if(id==='tulip_seeds'){flower(c,30,20,'tulip');c.put(18,15,'TULIP','k');c.put(39,29,'o','b');c.put(42,31,'o','b');}
 if(id==='rose_seeds'){c.put(19,15,'ROSE','k');flower(c,31,22,'rose');c.put(19,30,'<>','b');c.put(42,31,'<>','b');}
 if(id==='carrot_seeds'){c.rows(['\\ | /',' \\|/'],29,14,'g');poly(c,[[25,18],[38,18],[29,31]],'b');c.put(27,22,'--','k');c.put(28,26,'-','k');c.put(23,12,'CARROT','k');}
 if(id==='tomato_seeds'){c.put(17,15,'TOMATO','k');c.ellipse(32,25,10,6,'_','r',true);c.rows(['\\|/','/|\\'],31,19,'g');c.put(26,24,"'",'f');}
 if(id==='strawberry_seeds'){c.put(17,15,'BERRY','k');poly(c,[[24,21],[39,21],[41,25],[32,33],[23,26]],'r');c.put(28,20,'\\|/','g');for(const [x,y]of [[27,24],[34,24],[30,28],[36,27]])c.put(x,y,':','a');}
 if(id==='mint_seeds'){c.put(20,15,'MINT','k');flower(c,32,21,'mint');c.put(18,30,'. :','b');}
}
function worm(c,id){
 const giant=id==='giant_worm',juicy=id==='juicy_worm';
 const points=giant?[[8,31],[12,23],[23,20],[35,25],[47,24],[54,15],[48,10],[40,12]]:juicy?[[9,30],[17,26],[25,29],[34,31],[44,26],[49,20],[43,16]]:[[12,32],[19,28],[26,28],[33,32],[41,31],[49,25]];
 const r=giant?5:juicy?4:2;
 // Build one continuous body first; then place dorsal annuli and a broad clitellum.
 for(let i=1;i<points.length;i++){
  const a=points[i-1],b=points[i],steps=Math.ceil(Math.hypot(b[0]-a[0],b[1]-a[1]));
  for(let j=0;j<=steps;j++){const u=j/steps;c.ellipse(a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u,r,r,'_','r',true);}
 }
 // Retain only the union contour, avoiding overlapping circle ink inside the body.
 const occupied=new Set();for(const f of c.fills)for(let x=f.x;x<f.x+f.w;x++)occupied.add(`${x},${f.y}`);
 c.clear(0,0,c.w,c.h);
 for(const cell of occupied){const [x,y]=cell.split(',').map(Number);
  if(!occupied.has(`${x},${y-1}`)||!occupied.has(`${x},${y+1}`))c.put(x,y,'_','r');
  else if(!occupied.has(`${x-1},${y}`)||!occupied.has(`${x+1},${y}`))c.put(x,y,'|','r');
 }
 for(let i=1;i<points.length;i++){
  const a=points[i-1],b=points[i],dx=b[0]-a[0],dy=b[1]-a[1],length=Math.hypot(dx,dy),steps=Math.floor(length/3);
  for(let j=0;j<steps;j++){const u=j/steps,x=a[0]+dx*u,y=a[1]+dy*u;c.line(x-dy/length*(r-1),y+dx/length*(r-1),x+dy/length*(r-1),y-dx/length*(r-1),'|','b');}
 }
 const [x,y]=points.at(-2);c.ellipse(x,y,r+1,r,'_','b',true);c.line(x-1,y-r+1,x-1,y+r-1,'|','f');
 const [hx,hy]=points.at(-1);c.put(hx,hy,')','k');
}
function build(c,id){
 if(['tulip_seeds','rose_seeds','carrot_seeds','tomato_seeds','strawberry_seeds','mint_seeds'].includes(id))return packet(c,id);
 if(id.endsWith('worm'))return worm(c,id);
 if(id==='seed'){almond(c,32,25,13,12);c.ellipse(27,29,3,2,'_','k',true);c.put(27,28,'o','f');return;}
 if(id==='vegetable_seed'){poly(c,[[14,23],[22,16],[37,16],[47,23],[42,33],[31,36],[19,32]],'b');c.ellipse(31,25,9,6,'_','k',true);c.ellipse(34,24,7,4,'_','b',true);c.put(25,27,'(o)','f');c.line(20,21,29,19,':','f');return;}
 if(id==='seeds'){for(const [x,y,rx,ry]of [[15,30,8,3],[29,28,6,4],[43,31,9,3],[22,21,7,3],[38,20,5,4]])grain(c,x,y,rx,ry);return;}
 if(id==='sunflower_seeds'){for(const [x,y,r]of [[16,26,9],[31,21,12],[47,27,9]]){almond(c,x,y,6,r,'k');for(const dx of [-3,2])c.line(x+dx,y-r+5,x+dx,y+r-3,'|','f');}return;}
 if(id==='pumpkin_seeds'){for(const [x,y]of [[18,29],[33,18],[47,29]]){c.ellipse(x,y,9,7,'_','f',true);c.ellipse(x,y,6,5,'_','b',true);c.line(x-3,y-2,x+3,y+2,'/','f');}return;}
 if(id==='watermelon_seeds'){for(const [x,y]of [[17,28],[32,19],[46,28]]){almond(c,x,y,7,8,'k');c.line(x-3,y-2,x-2,y+3,'|','b');c.put(x-1,y-4,"'",'f');}return;}
 if(id==='enchanted_seeds'){for(const [x,y]of [[18,28],[32,18],[46,29]]){almond(c,x,y,8,8,'n');c.rows([' /\\','< + >',' \\/'],x-2,y-1,'f');}return;}
 if(id==='golden_seeds'){for(const [x,y]of [[20,28],[38,22]]){poly(c,[[x,y-12],[x+10,y-4],[x+9,y+6],[x,y+11],[x-9,y+5],[x-10,y-4]],'a');c.line(x,y-9,x,y+8,'|','f');c.line(x-7,y-2,x+7,y-2,'_','b');c.put(x-4,y+2,'\\ /','f');}return;}
 if(id==='crystal_seeds'){for(const [x,y,size]of [[16,29,7],[32,21,12],[49,29,7]]){poly(c,[[x,y-size],[x+6,y-3],[x+5,y+size-1],[x-4,y+size],[x-6,y-2]],'c');c.line(x,y-size,x+1,y+size-2,'|','f');c.line(x-5,y-2,x+5,y-3,'/','w');c.line(x+1,y+size-2,x+5,y-3,'/','w');}return;}
 if(id==='better_bait'){// A compact pressed groundbait cake; no extra hooks, fish or reward objects.
  poly(c,[[13,23],[20,16],[41,16],[50,23],[46,34],[21,36],[12,30]],'b');
  c.line(15,25,47,25,'_','k');c.line(22,18,20,33,'/','f');
  for(const [x,y]of [[27,20],[38,20],[29,29],[40,30],[17,28]]){c.put(x,y,'o','f');c.put(x+2,y+2,':','k');}c.put(33,23,'~=','r');
 }
}
export function seedSprite(base,item,time,{state={}}={}){
 const p=BLUEPRINTS[item?.id];if(!p)return null;
 const c=new ObjectCanvas(p.w,p.h);build(c,item.id);
 const cells=[];for(let y=0;y<c.h;y++)for(let x=0;x<c.w;x++)if(c.art[y][x]!==' ')cells.push([x,y]);
 const amount=v=>Number.isFinite(v)?Math.max(0,Math.min(1,v)):0;
 for(const [v,g,t,stride]of [[amount(state.wetness),"'",'w',17],[amount(state.dirt),'.','s',31],[amount(1-(state.condition??1)),'/','k',43]])for(let i=0;i<Math.floor(v*10);i++){const a=cells[(i*stride+9)%cells.length];if(a)c.put(...a,g,t);}
 const surface=c.finish(),bottom=Math.max(...cells.map(([,y])=>y),...surface.fills.map(f=>f.y))+1;
 surface.art=surface.art.slice(0,bottom);surface.tones=surface.tones.slice(0,bottom);surface.groundRow=bottom;
 return {...base,...surface,construction:'seed-v1',blueprint:item.id,scale:p.scale,detail:true,detailScale:.68,inks,panels,sway:0,lift:0,animated:false,emissive:false};
}
