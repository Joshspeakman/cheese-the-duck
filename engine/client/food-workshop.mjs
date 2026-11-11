import {ObjectCanvas} from './object-canvas.mjs';
import BLUEPRINTS from './animation/foods.json' with {type:'json'};
export {BLUEPRINTS as FOOD_BLUEPRINTS};
const inks={b:'#d8ad6c',f:'#ffe3a0',k:'#92633e',s:'#8d8663',w:'#a6d7e3',r:'#e87e70',g:'#9bbd6f',p:'#deb4db',a:'#efc95f',n:'#a59acc'};
const panels={b:'#8a5734',f:'#b7955e',k:'#3e2a22',s:'#4e4a31',w:'#375f69',r:'#973d40',g:'#406135',p:'#775071',a:'#a7792e',n:'#393353'};
function poly(c,pts,t='b'){
 for(let y=Math.min(...pts.map(p=>p[1]));y<=Math.max(...pts.map(p=>p[1]));y++){
  const cuts=[];for(let i=0;i<pts.length;i++){const a=pts[i],b=pts[(i+1)%pts.length];if(a[1]!==b[1]&&y>=Math.min(a[1],b[1])&&y<Math.max(a[1],b[1]))cuts.push(a[0]+(y-a[1])*(b[0]-a[0])/(b[1]-a[1]));}
  cuts.sort((a,b)=>a-b);for(let i=0;i+1<cuts.length;i+=2)c.solid(Math.ceil(cuts[i]),y,Math.floor(cuts[i+1])-Math.ceil(cuts[i])+1,1,t);
 }
 pts.forEach((a,i)=>c.line(...a,...pts[(i+1)%pts.length],null,t));
}
function pores(c,x,y,rx,ry){for(let yy=-ry+2;yy<ry;yy+=3)for(let xx=-rx+3;xx<rx;xx+=6)if((xx/rx)**2+(yy/ry)**2<.7)c.put(x+xx,y+yy,(xx+yy)%3?'o':'.','f');}
function crumb(c,x,y,r=7,t='b',kind=0){poly(c,[[x-r,y-2],[x-r+3,y-5],[x+2,y-6],[x+r,y-1],[x+r-2,y+4],[x-2,y+5],[x-r,y+2]],t);c.line(x-r+2,y-2,x+1,y-4,'_','f');c.put(x-3,y,'o .','f');c.put(x,y+2,kind?'::':"' o",'k');}
function loaf(c,kind){
 if(kind==='ancient_bread')poly(c,[[8,24],[12,16],[22,12],[38,13],[49,19],[54,27],[46,33],[18,34]],'b');
 else if(kind!=='welcome_bread')c.ellipse(31,23,25,12,'_','b',true);
 if(kind!=='welcome_bread')c.line(10,29,48,29,'_','k');
 if(kind==='fancy_bread'){for(const [x,y] of [[15,19],[25,15],[35,17],[43,21]]){c.line(x,y,x+5,y+5,'/','f');c.line(x+2,y,x+7,y+4,'/','k');}c.put(16,31,'~  ~  ~  ~  ~','f');}
 if(kind==='ancient_bread'){c.line(13,15,25,23,'\\','k');c.line(25,23,20,30,'/','k');c.line(25,23,43,20,'-','k');c.put(34,15,'/\/','f');c.put(34,27,': = :','k');c.put(12,24,'o  o','f');}
 if(kind==='honey_bread'){c.ellipse(29,17,18,5,'~','a',true);for(const [x,n] of [[16,6],[25,10],[38,7]]){c.line(x,18,x,18+n,'|','a');c.put(x-1,19+n,'(_)','a');}c.put(19,15,'~~   ~~~~','f');}
 if(kind==='welcome_bread'){for(let x=12;x<=42;x+=10){c.ellipse(x,22,8,9,'_','b',true);c.line(x-4,19,x+3,24,'/','f');c.line(x-3,25,x+4,20,'\\','k');}c.put(9,32,'\\______________________/','f');}
}
function fruit(c,id){
 if(id==='carrot'){
  for(const [x,y] of [[16,4],[25,3],[34,5]]){c.line(27,14,x,y,'/','g');c.put(x-2,y,'\\|/','g');}poly(c,[[14,13],[40,14],[35,23],[24,35],[20,33]],'b');for(const [x,y] of [[17,17],[24,21],[22,26]])c.put(x,y,'---','k');c.line(23,15,26,28,':','f');return;
 }
 if(id==='watermelon'){poly(c,[[7,12],[53,12],[48,25],[39,32],[22,34],[12,27]],'g');poly(c,[[10,12],[50,12],[45,24],[37,29],[23,31],[15,25]],'f');poly(c,[[13,12],[47,12],[42,22],[35,27],[24,28],[18,23]],'r');for(const [x,y] of [[21,17],[32,17],[42,16],[25,24],[36,23]])c.put(x,y,'()','k');c.line(10,11,51,11,'_','f');return;}
 if(id==='strawberry'){poly(c,[[14,13],[22,9],[39,10],[47,16],[43,25],[31,35],[20,29],[13,21]],'r');for(let y=14;y<29;y+=4)for(let x=20+(y%3);x<42-(y-14)*.4;x+=7)c.put(x,y,':','a');c.rows(['  \\ | /','__\\|/___',' \\ / \\ /'],25,5,'g');return;}
 if(id==='pumpkin'){for(const [x,rx] of [[17,10],[43,10],[24,11],[36,11],[30,8]])c.ellipse(x,24,rx,11,'_','b',true);c.rows(['  ___',' / /',' | |','_| |_'],29,5,'g');for(const x of [23,36])c.line(x,16,x-1,30,':','f');return;}
 const apple=id==='fresh_apple';
 if(apple)poly(c,[[9,18],[15,12],[24,12],[30,15],[37,12],[45,13],[51,20],[48,29],[40,35],[33,34],[28,35],[18,33],[11,27]],'r');
 else c.ellipse(30,24,22,11,'_','r',true);
 c.put(16,18,'(  )','f');c.line(30,15,32,7,'/','k');
 if(apple){poly(c,[[32,9],[37,5],[46,6],[41,10]],'g');c.line(34,9,43,7,'/','f');c.put(27,33,'\\_/','k');}
 else{c.rows(['\\  |  /',' \\ | /','--\\|/--','  / \\'],26,10,'g');c.put(40,25,'..','b');}
}
function build(c,id){
 if(['fancy_bread','ancient_bread','honey_bread','welcome_bread'].includes(id))return loaf(c,id);
 if(['carrot','tomato','fresh_apple','pumpkin','strawberry','watermelon'].includes(id))return fruit(c,id);
 if(id==='bread'){poly(c,[[12,18],[9,15],[10,11],[15,8],[24,8],[30,10],[37,8],[45,9],[50,13],[49,17],[46,19],[46,34],[14,34]],'b');poly(c,[[17,18],[14,15],[15,12],[23,11],[30,13],[38,11],[44,13],[45,16],[41,19],[41,30],[19,30]],'f');pores(c,29,21,14,10);c.put(17,32,'------------------------','k');return;}
 if(id==='oats'){c.ellipse(30,29,23,6,'_','k',true);for(const [x,y] of [[16,24],[27,24],[39,24],[21,20],[33,19],[29,15],[43,28],[12,29],[25,28]]){c.ellipse(x,y,5,2,'_','b',true);c.line(x-2,y,x+2,y,'-','f');}return;}
 if(id==='breadcrumbs'){for(const [x,y,r] of [[14,27,6],[25,20,7],[42,27,8],[38,14,5],[26,31,4]])crumb(c,x,y,r);return;}
 if(id==='bread_crumb'){crumb(c,30,24,17);pores(c,30,23,13,7);c.line(18,29,37,31,'_','k');return;}
 if(id==='golden_crumb'){poly(c,[[17,25],[21,14],[33,10],[45,20],[41,30],[26,33]],'a');c.line(21,14,30,24,'\\','f');c.line(30,24,45,20,'/','f');c.line(30,24,26,33,'/','k');c.put(31,16,'<>','f');return;}
 if(id==='mysterious_crumb'){crumb(c,30,24,17,'p');c.ellipse(30,22,8,5,'~','k',true);c.rows([' .---.',' / . |',' \\__/'],27,20,'p');return;}
 if(id==='rainbow_crumb'){for(const [y,t,r] of [[27,'p',22],[24,'n',19],[21,'g',16],[18,'a',13],[15,'r',10]]){c.ellipse(30,y,r,5,'_',t,true);c.line(30-r+3,y+2,30+r-3,y+2,'~',t);}c.put(25,13,'o  o','f');return;}
 if(id==='void_crumb'){poly(c,[[13,22],[24,12],[42,15],[48,26],[34,34],[18,30]],'n');poly(c,[[21,22],[29,17],[39,20],[39,27],[29,30],[22,26]],'k');c.rows(['  .---.',' / .   |',' |  .--\'','  `--'],24,20,'n');return;}
 if(id==='rare_treat'){poly(c,[[30,9],[35,18],[48,20],[39,26],[40,34],[30,30],[20,34],[21,25],[12,20],[25,18]],'b');c.rows([' .-.','( o )',' `-\''],27,20,'p');c.put(24,17,'::','f');c.put(34,27,'::','f');return;}
 if(id==='honeycomb'){for(const [x,y] of [[19,13],[29,13],[39,13],[14,20],[24,20],[34,20],[44,20],[19,27],[29,27],[39,27]]){poly(c,[[x-4,y-2],[x,y-4],[x+4,y-2],[x+4,y+2],[x,y+4],[x-4,y+2]],'a');c.put(x-2,y,'(_)','k');c.put(x-2,y-2,'__','f');}c.line(33,30,33,35,'|','a');return;}
 if(id==='berry_salad'){for(const [x,y] of [[16,18],[27,15],[39,17],[44,22]])c.rows(['\\ /',' >','/ \\'],x,y,'g');for(const [x,y,t] of [[23,20,'r'],[33,19,'n'],[39,23,'r'],[18,24,'p'],[29,24,'n']]){c.ellipse(x,y,4,3,'o',t,true);c.put(x,y-1,"'",'f');}poly(c,[[7,24],[53,24],[47,32],[39,35],[21,35],[13,31]],'f');c.line(9,25,51,25,'=','b');c.put(18,31,'( )  ( )  ( )','b');return;}
 if(id==='homemade_pie'){c.ellipse(30,28,24,7,'_','k',true);c.ellipse(30,24,25,9,'~','b',true);c.ellipse(30,22,20,6,'_','r',true);for(let x=17;x<=41;x+=8){c.line(x-5,18,x+5,27,'\\','f');c.line(x+5,18,x-5,27,'/','b');}c.put(12,29,'v v v v v v v v v v','f');c.line(13,32,47,32,'_','b');return;}
 if(id==='heart_cookie'){poly(c,[[30,15],[24,9],[15,10],[10,16],[12,24],[30,35],[48,24],[50,16],[45,10],[36,9]],'b');poly(c,[[30,19],[23,13],[17,14],[15,18],[18,24],[30,31],[42,24],[45,18],[42,14],[37,13]],'p');c.rows(['  .  .',' : \\/ :','  \\  /','   \\/'],26,20,'f');for(const [x,y] of [[18,18],[41,19],[23,25],[36,26]])c.put(x,y,'o','r');}
}
// Artwork only: native simulation owns condition; no consumption, timers or inventory here.
export function foodSprite(base,item,time,{state={},motion=1}={}){
 const p=BLUEPRINTS[item?.id];if(!p)return null;
 const c=new ObjectCanvas(p.w,p.h);build(c,item.id);
 const cells=[];for(let y=0;y<c.h;y++)for(let x=0;x<c.w;x++)if(c.art[y][x]!==' ')cells.push([x,y]);
 const amount=v=>Number.isFinite(v)?Math.max(0,Math.min(1,v)):0;
 for(const [value,glyph,tone,stride] of [[amount(state.wetness),"'",'w',17],[amount(state.dirt),'.','s',29],[amount(1-(state.condition??1)),'/','k',41]])for(let i=0;i<Math.floor(value*12);i++){const cell=cells[(i*stride+7)%cells.length];if(cell)c.put(...cell,glyph,tone);}
 const surface=c.finish();
 const bottom=Math.max(...cells.map(([,y])=>y),...surface.fills.map(f=>f.y))+1;
 surface.art=surface.art.slice(0,bottom);surface.tones=surface.tones.slice(0,bottom);surface.groundRow=bottom;
 return {...base,...surface,scale:p.scale,construction:'food-v1',blueprint:item.id,detail:true,detailScale:.68,inks,panels,sway:0,lift:0,animated:false,emissive:false};
}
