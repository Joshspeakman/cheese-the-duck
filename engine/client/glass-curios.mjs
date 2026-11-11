// Sealed miniature scenes. Their snow and readings come only from native state.
const clamp=n=>Math.max(0,Math.min(1,Number.isFinite(n)?n:0));
function fir(c,x,y,size=1){
 for(let tier=0;tier<4;tier++){
  const yy=y+tier*4*size,half=(3+tier*2)*size;
  c.line(x,yy-5*size,x-half,yy+3*size,'/','g');c.line(x,yy-5*size,x+half,yy+3*size,'\\','g');
  c.line(x-half,yy+3*size,x+half,yy+3*size,'_','f');
  for(let i=-tier;i<=tier;i++)c.put(x+i*2*size,yy+size,':','s');
 }
 c.line(x,y+14*size,x,y+20*size,'|','b');
}
function cottage(c,x,y,w,h,chimney=false){
 c.clear(x-2,y-10,w+4,h+11);c.rect(x,y,w,h,'p',true);
 for(let row=0;row<10;row++){
  const over=2-row*.45;c.solid(x-over,y-row,w+over*2,1,'q');
  c.put(x-over,y-row,'/','f');c.put(x+w+over-1,y-row,'\\','q');
  if(row%3===0)c.line(x-over+3,y-row,x+w+over-4,y-row,'=','q');
 }
 c.line(x+3,y-9,x+w-5,y-9,'_','f');
 for(let row=2;row<9;row+=3)for(let xx=x+5;xx<x+w-4;xx+=6)c.put(xx+(row%2)*2,y-row,'|','b');
 if(chimney){c.rect(x+w-8,y-17,5,9,'b',true);c.put(x+w-10,y-18,'_______','f');}
 for(const xx of [x+3,x+w-8]){
  c.rect(xx,y+4,5,6,'a',true);c.put(xx+2,y+5,'|','f');c.put(xx+1,y+7,'-+-','f');
  c.put(xx-1,y+11,'_______','b');
 }
 c.rect(x+w/2-3,y+h-10,7,10,'b',true);c.put(x+w/2+1,y+h-5,'o','a');
 for(let yy=y+3;yy<y+h;yy+=5)c.put(x+1,yy,':','b');
 for(let yy=y+14;yy<y+h-2;yy+=4){c.put(x+2,yy,'--','b');c.put(x+w-5,yy,'--','b');}
 c.line(x-2,y+h,x+w+1,y+h,'_','f');
}
function tinyDuck(c,x,y){
 c.rows(['   ,-.','  (o )=',' /\'--|','(__/_)','  vv'],x,y,'p');c.put(x+6,y+1,'=','a');c.put(x+1,y+3,'/','g');
}
function pedestal(c,p,v,oracle=false){
 const W=p.w,H=p.h,cx=W/2,rx=W*.39;
 c.ellipse(cx,H-23,rx,6,'_','b',true);c.rect(cx-rx,H-23,rx*2+1,16,'b',true);
 for(let x=cx-rx+5;x<cx+rx-4;x+=8){c.put(x,H-19,oracle?'(*)':'<*>','a');c.put(x+1,H-15,oracle?'|':':','s');}
 c.line(cx-rx+2,H-9,cx+rx-2,H-9,'=','a');c.ellipse(cx,H-7,rx,4,'_','k',true);c.line(cx-rx+3,H-5,cx+rx-3,H-5,'_','a');
 c.clear(cx-20,H-22,41,9);c.rect(cx-20,H-22,41,9,'k',true);
 c.put(cx-p.caption.length/2,H-18,p.caption,'a');
 const pump={x:cx-rx+7,y:H-12};
 c.rect(pump.x-5,pump.y-4,11,7,'a',true);c.put(pump.x-3,pump.y-3+Math.round(clamp(v.open)*2),'[===]','f');
 c.put(pump.x-2,pump.y+1,oracle?'(*)':'~~~','k');
 const ring={x:cx+rx-9,y:H-10};
 c.ellipse(ring.x,ring.y,5,4,'_','a',true);
 c.line(ring.x,ring.y,ring.x+Math.cos(v.azimuth||0)*4,ring.y+Math.sin(v.azimuth||0)*3,null,'f');
 return {entry:{x:cx,y:H-3},contact:pump,pump,ring,rim:{x:cx,y:H-10},
  left:{x:cx-rx+3,y:H-10},right:{x:cx+rx-3,y:H-10},window:{x:cx,y:H-26}};
}
function dome(c,cx,cy,rx,ry){
 c.ellipse(cx,cy,rx,ry,'_','g',true);
 c.ellipse(cx,cy,rx-2,ry-2,'.','w');
 // Two curved reflected panes leave the miniature readable through the glass.
 for(let i=0;i<25;i++){
  const a=3.5+i*.026,x=cx+Math.cos(a)*(rx-5),y=cy+Math.sin(a)*(ry-5);
  c.put(x,y,'/','f');if(i%3===0)c.put(x+3,y+1,':','w');
 }
 for(let i=0;i<18;i++){const a=.1+i*.025;c.put(cx+Math.cos(a)*(rx-5),cy+Math.sin(a)*(ry-5),'|','w');}
}
export function globe(c,p,v,state){
 const W=p.w,H=p.h,cx=W/2,cy=(H-36)/2+3,rx=W*.44,ry=(H-36)/2;
 dome(c,cx,cy,rx,ry);
 const floor=H-39;
 // Rolling snow banks and the tiny frozen pond are shaped, not rectangular.
 c.ellipse(cx,floor-13,rx*.79,21,'_','p',true);
 for(let i=0;i<5;i++)c.line(cx-rx*.55+i*4,floor-22+i*4,cx+rx*.5-i*3,floor-22+i*4,'~','f');
 c.ellipse(cx+rx*.12,floor-2,rx*.5,6,'~','w',true);
 for(let i=0;i<5;i++)c.line(cx-rx*.28+i*2,floor-4+i*2,cx+rx*.4-i*3,floor-4+i*2,'_','f');
 if(p.style==='village'){
  fir(c,35,floor-56,1.2);fir(c,W-34,floor-60,1.1);fir(c,W-61,floor-72,.8);
  cottage(c,cx-47,floor-40,29,28,true);cottage(c,cx+1,floor-50,31,30,true);cottage(c,cx+35,floor-30,25,22);
  // A shallow bridge has a visible arch, plank walkway and five balusters.
  for(let i=0;i<39;i++){const x=cx-37+i,y=floor-8-Math.sin(i/38*Math.PI)*7;c.put(x,y,'_','b');c.put(x,y-7,'_','a');if(i%8===0)c.line(x,y-6,x,y,'|','b');}
  c.line(cx-33,floor-5,cx-3,floor-5,'_','s');tinyDuck(c,cx+17,floor-8);
  c.rows([' _|_','  |',' / \\'],cx-63,floor-19,'a');
 }else{
  fir(c,cx+37,floor-46,1);c.put(cx+34,floor-51,'_,','f');
  cottage(c,cx-23,floor-43,35,29,true);
  for(let i=0;i<12;i++){const x=cx-5+Math.sin(i*.25)*13;c.put(x,floor-14+i,'..','b');}
  c.rows(['_|__|__|_',' |  |  | '],cx-41,floor-12,'b');tinyDuck(c,cx+21,floor-7);
  c.put(cx-31,floor-20,'(*)','q');
 }
 const glass=state.keepsake?.glass||{},energy=v.motion===false?(glass.energy>.03?.5:0):clamp(glass.energy),phase=v.motion===false?0:Number(glass.phase)||0;
 // Each flake returns to its own bank as native circulation loses energy.
 for(let i=0;i<(p.style==='village'?105:65);i++){
  const seed=(i*.61803398875)%1,lift=Math.pow(energy,.65),cycle=.5+.5*Math.sin(phase+seed*Math.PI*2),a=i*2.399+phase;
  const y=floor-3-lift*(.18+.82*cycle)*(floor-14),q=Math.max(0,1-((y-cy)/(ry-6))**2);
  const x=cx+Math.sin(a)*(rx-8)*Math.sqrt(q)*(.2+.75*((i*.371)%1));
  c.put(x,y,i%9===0?'*':i%3===0?'+':'.','f');
 }
 const anchors=pedestal(c,p,{...v,azimuth:0});
 if(v.wipe>.05){const x=cx-rx*.65+clamp(v.wipe)*rx*1.3;c.line(x,H-17,x+3,H-11,'/','f');}
 return anchors;
}
export function weatherGlyphFamily(type){
 if(/rainbow/.test(type))return 'rainbow';
 if(/aurora|star|meteor|night|moon|evening/.test(type))return 'night';
 if(/leaf|autumn|crisp/.test(type))return 'leaves';
 if(/pollen/.test(type))return 'pollen';
 if(/frost|cold|freez/.test(type))return 'frost';
 if(/snow|blizzard|sleet|ice_storm/.test(type))return 'snow';
 if(/rain|storm|drizzle|shower|hail/.test(type))return 'rain';
 if(/cloud|overcast|fog|mist/.test(type))return 'cloud';
 if(/wind|breez|dust/.test(type))return 'wind';
 return 'sun';
}
function weatherPicture(c,x,y,type){
 const family=weatherGlyphFamily(type),snow=family==='snow',rain=family==='rain',cloud=family==='cloud';
 if(family==='rainbow'){
  for(let band=0;band<(type==='double_rainbow'?5:3);band++)for(let i=0;i<28;i++){
   const a=Math.PI+i/27*Math.PI;c.put(x+12+Math.cos(a)*(12-band*2),y+15+Math.sin(a)*(11-band*1.6),'_',['q','a','g','w','l'][band]);
  }
  c.put(x,y+17,'~~~                ~~~','f');
 }else if(family==='frost'){
  for(const [dx,dy]of [[10,8],[20,18]]){c.line(x+dx-6,y+dy,x+dx+6,y+dy,'-','w');c.line(x+dx,y+dy-6,x+dx,y+dy+6,'|','f');c.line(x+dx-4,y+dy-4,x+dx+4,y+dy+4,'\\','w');c.line(x+dx-4,y+dy+4,x+dx+4,y+dy-4,'/','w');c.put(x+dx-1,y+dy,'(*)','f');}
 }else if(family==='leaves'){
  c.rows(['    __','   / /','  /_/     __','   |     /  /','         /_/','          |','   __','  / /',' /_/'],x+5,y+3,'a');c.put(x+19,y+16,'~','q');
 }else if(family==='pollen'){
  c.rows([' .      *       .','      .   .','   .      *','       .     .','     (*)','    --|--','      |','  ~~~~~~~~~~~'],x+4,y+2,'a');
 }else if(snow||rain||cloud){
  c.rows(['        .---.','    .--(     )--.','  _(             )_',' (_____.____.______)'],x,y,'f');
  if(snow)for(let i=0;i<12;i++)c.put(x+3+i%4*5,y+7+Math.floor(i/4)*4,i%2?'*':'+','w');
  else if(rain)for(let i=0;i<12;i++)c.put(x+4+i%4*5,y+6+Math.floor(i/4)*4,/hail/.test(type)?'o':'/','w');
  else for(let i=0;i<3;i++)c.put(x-1,y+7+i*3,'~~  ~~~~   ~~~~~  ~~','w');
  if(/storm/.test(type))c.rows(['__',' /','/___','   /','  /'],x+12,y+5,'a');
 }else if(family==='night'){
  c.rows(['  *            .','       .---.','    . (   __)    +','       \`--\'',' +           *','     .    /','         /','    *   .'],x+2,y,'l');
 }else if(family==='wind'){
  c.rows(['        __','  _____/  )','          \`','        ___',' ______/   )','          /','   ______/','  (___'],x+1,y+2,'w');
 }else{
  c.rows(['       \\ | /','        .-.','   --- ( @ ) ---','        \`-\'','       / | \\'],x+1,y+4,'a');
  if(/heat|scorch|muggy|humid/.test(type))c.rows([' ~   ~   ~','  ~   ~   ~'],x+5,y+13,'q');
 }
}
export function oracle(c,p,v,state){
 const W=p.w,H=p.h,cx=W/2,cy=H*.39,rx=W*.34,ry=H*.33,glass=state.keepsake?.glass||{};
 const azimuth=Number(glass.azimuth)||0,focus=clamp(glass.focus),vision=glass.vision;
 // Three claw feet hold the sphere above a carved equatorial cradle.
 for(const sign of [-1,1]){c.beam(cx+sign*31,H-26,cx+sign*47,H-58,5,'b');c.rows(sign>0?[' _/','/ /','|/']:['\\_','\\ \\',' \\|'],cx+sign*48-1,H-63,'a');}
 dome(c,cx,cy,rx,ry);
 for(let i=0;i<42;i++){
  const a=i/42*Math.PI*2+azimuth,r=rx*(.42+.12*Math.sin(i*.6));
  c.put(cx+Math.cos(a)*r,cy+Math.sin(a)*ry*.69,i%7===0?'*':i%2?':':'.',focus>.3?'l':'s');
 }
 if(vision?.weather){weatherPicture(c,cx-12,cy-13,vision.weather);const text=vision.weather.replaceAll('_',' ').toUpperCase();c.put(cx-text.length/2,cy+17,text,'f');}
 else{c.rows(['       .','    .     .','   .   ?   .','    .     .','       .'],cx-7,cy-3,'l');c.put(cx-8,cy+14,'TOUCH TO CONSULT','s');}
 // Engraved orbital marks physically follow the saved dial bearing.
 for(let i=0;i<12;i++){
  const a=i*Math.PI/6+azimuth,x=cx+Math.cos(a)*(rx+4),y=cy+Math.sin(a)*(ry+3);
  c.put(x-1,y,['(*)','o','+','.'][i%4],i%3===0?'a':'s');
 }
 c.line(cx-rx+6,H-30,cx+rx-6,H-30,'=','a');
 return pedestal(c,p,{...v,azimuth},true);
}
export const GLASS_INKS={g:'#79afa9',w:'#b3d7dd',f:'#e5ece3',p:'#dfd9bf',q:'#b97378',a:'#dfbf79',l:'#b9aee4',s:'#7f9d9d',b:'#ad9473'};
export const GLASS_PANELS={g:'#163539',w:'#29565e',p:'#a2afa0',q:'#563741',b:'#39362e',a:'#6a5841',k:'#152a29'};
