// Curios: cards, fish, feathers, badges, trophies, small treasures and tools.
// Every object is constructed from printable ASCII geometry on a coarse grid, one
// builder per type, parametrised by a per-id spec (colour, emblem, shape, text).
// Construction is memoised and motion steps at 3 fps; motion:false is static.
import {ObjectCanvas} from './object-canvas.mjs';
import BLUEPRINTS from './animation/curios.json' with {type:'json'};
export {BLUEPRINTS as CURIO_BLUEPRINTS};
const TAU=Math.PI*2,clamp=(n,a=0,b=1)=>Math.max(a,Math.min(b,Number.isFinite(n)?n:0));
const hash=(...v)=>{let h=2166136261;for(const c of v.join('|')){h^=c.charCodeAt(0);h=Math.imul(h,16777619);}return h>>>0;};
const INKS={b:'#c9a071',a:'#e8c27a',f:'#f6f0d8',s:'#93a39e',k:'#5f6f6a',p:'#e9e3cc',d:'#2c3440',g:'#9ef0a8',q:'#f0a4bc',w:'#8fd7ea',l:'#c4b4f0',e:'#ffb347',y:'#f0d060',v:'#b58cf2',c:'#8ce9f0',h:'#6fb36a',i:'#cdeff6',m:'#8fb86a',n:'#e6cf9a',o:'#e8955a',r:'#e86f6f',t:'#a7b4b8',u:'#6f9fe0',x:'#4fb3a4',j:'#e0609a',z:'#a8794a'};
const PANELS={b:'#4a3a2a',a:'#5a4528',f:'#5e5a4a',s:'#2c3834',k:'#141c1c',p:'#5a5648',d:'#0c1018',g:'#1e4a2a',q:'#5a2a3a',w:'#1e4a5a',l:'#3a3256',e:'#5a3216',y:'#5a4a22',v:'#3a2456',c:'#1a4a50',h:'#1f3f20',i:'#3a5a64',m:'#2a3a1e',n:'#6a5a3a',o:'#5a3220',r:'#5a2020',t:'#36403f',u:'#1c3260',x:'#1c4a44',j:'#5a1e3c',z:'#46301c'};

// ------------------------------------------------------------------ drawing helpers
// Cells are 1 wide by 1.5 tall, so a round thing is rx = 1.5 * ry.
const circ=(c,cx,cy,ry,ch='-',tone='b',fill=false)=>c.ellipse(cx,cy,ry*1.5,ry,ch,tone,fill);
function P(c,rows,x,y,tone='b',map={},fill=false){
 rows.forEach((r,j)=>{
  if(fill){const a=r.search(/\S/),b=r.trimEnd().length;if(a>=0)c.solid(x+a,y+j,b-a,1,typeof fill==='string'?fill:tone);}
  [...r].forEach((ch,i)=>{if(ch!==' ')c.put(x+i,y+j,ch,map[ch]||tone);});
 });
}
const PC=(c,rows,cx,cy,tone,map,fill)=>P(c,rows,Math.round(cx-Math.max(...rows.map(r=>r.length))/2),Math.round(cy-rows.length/2),tone,map,fill);
const text=(c,x,y,s,tone='f')=>c.put(x,y,s,tone);
const ctext=(c,cx,y,s,tone='f')=>c.put(Math.round(cx-s.length/2),y,s,tone);
const dot=(c,x,y,ch,tone)=>{x=Math.round(x);y=Math.round(y);if(x>=0&&y>=0&&x<c.w&&y<c.h)c.put(x,y,ch,tone);};
const glint=(c,x,y,f,tone='f',ph=0)=>dot(c,x,y,['.','+','*','+'][(f+ph)%4],tone);
const sparks=(c,list,f,tone='f')=>list.forEach(([x,y],i)=>glint(c,x,y,f,tone,i));
function mergeFills(fills){
 const grid=new Map();
 for(const f of fills)for(let x=f.x;x<f.x+f.w;x++)grid.set(f.y*4096+x,f.tone+(f.opaque?'!':''));
 const rows=new Map();
 for(const [k,tone] of grid){const y=Math.floor(k/4096),x=k-y*4096;if(!rows.has(y))rows.set(y,[]);rows.get(y).push([x,tone]);}
 const out=[];
 for(const [y,cells] of [...rows].sort((a,b)=>a[0]-b[0])){
  cells.sort((a,b)=>a[0]-b[0]);let run=null;
  for(const [x,tone] of cells){
   if(run&&run.x+run.w===x&&run.key===tone){run.w++;continue;}
   if(run)out.push({x:run.x,y,w:run.w,tone:run.tone,opaque:run.opaque});
   run={x,w:1,key:tone,tone:tone.replace('!',''),opaque:tone.endsWith('!')};
  }
  if(run)out.push({x:run.x,y,w:run.w,tone:run.tone,opaque:run.opaque});
 }
 return out;
}

// ------------------------------------------------------------------ fish
// Side view facing right. A fusiform body is filled column by column; each fish
// differs in profile, tail, fins, colouring and markings (see FISH).
const FISH={
 minnow:{tw:5,hh:2.2,pw:.7,back:'m',side:'t',belly:'f',fin:'t',tail:'fork',th:2.5,dorsal:[.42,.62,2],anal:[.45,.6,1],pat:'stripe',stripe:'k',eyeAt:.12},
 small_fish:{tw:5,hh:3.8,pw:.6,pk:1.05,back:'u',side:'w',belly:'e',fin:'u',tail:'fork',th:3.2,dorsal:[.3,.75,2],anal:[.5,.72,1.6],pat:'cheek',eyeAt:.13},
 goldfish:{tw:9,hh:5,prof:'ball',ped:1.2,back:'e',side:'e',belly:'a',fin:'e',tail:'fan',th:6,dorsal:[.3,.7,3],anal:[.55,.7,2],pat:'scales',eyeAt:.14,big:1,glow:1},
 carp:{tw:8,hh:6,pw:.55,pk:1.2,back:'m',side:'a',belly:'n',fin:'z',tail:'fork',th:5,dorsal:[.1,.7,3],anal:[.58,.72,2],pat:'scales',whisk:2,eyeAt:.13},
 bass:{tw:8,hh:5.6,pw:.6,pk:1.25,back:'h',side:'g',belly:'f',fin:'h',tail:'fork',th:4.5,dorsal:[.18,.62,3],anal:[.58,.74,2],pat:'blotch',stripe:'k',eyeAt:.13,jaw:1,spiny:1},
 catfish:{tw:7,hh:5.2,pw:.5,pk:1.5,back:'k',side:'s',belly:'p',fin:'k',tail:'round',th:4,dorsal:[.52,.64,2],anal:[.25,.6,2],pat:'mottle',whisk:4,eyeAt:.1,flat:1,adip:1},
 trout:{tw:7,hh:4.4,pw:.65,pk:1.15,back:'m',side:'g',belly:'f',fin:'g',tail:'fork',th:3.5,dorsal:[.4,.58,2],anal:[.6,.72,1.4],pat:'trout',stripe:'q',eyeAt:.13},
 koi:{tw:8,hh:5,pw:.6,pk:1.2,back:'f',side:'f',belly:'f',fin:'f',tail:'fan',th:5,dorsal:[.2,.6,3],anal:[.55,.7,1.6],pat:'koi',whisk:2,eyeAt:.12,patches:[['e',.18,.5],['k',.5,.7],['e',.74,.92]]},
 salmon:{tw:9,hh:5.2,pw:.65,pk:1.15,back:'u',side:'t',belly:'f',fin:'u',tail:'hetero',th:5,dorsal:[.38,.55,2],anal:[.6,.72,1.4],pat:'salmon',eyeAt:.12,hook:1,blush:'r'},
 pufferfish:{tw:5,hh:7.2,prof:'ball',ped:1.4,back:'a',side:'y',belly:'f',fin:'a',tail:'round',th:3,dorsal:[.45,.6,1.4],anal:[.5,.62,1.2],pat:'puff',eyeAt:.2,spines:1,pout:1},
 swordfish:{tw:11,hh:5.6,pw:.7,pk:1.1,back:'u',side:'t',belly:'f',fin:'u',tail:'lunate',th:7,dorsal:[.3,.55,5],anal:[.58,.68,2],pat:'stripe',stripe:'u',eyeAt:.1,bill:20,sn:20,sail:1},
 sturgeon:{tw:11,hh:4.6,pw:.5,pk:1.25,back:'s',side:'t',belly:'p',fin:'k',tail:'hetero',th:6,dorsal:[.2,.35,3],anal:[.42,.52,2],pat:'scutes',whisk:3,eyeAt:.1,snout:10,sn:10},
 golden_koi:{tw:9,hh:6,pw:.6,pk:1.2,back:'y',side:'y',belly:'a',fin:'y',tail:'fan',th:6.5,dorsal:[.2,.62,3.4],anal:[.55,.7,2],pat:'scales',whisk:2,eyeAt:.12,glow:1,gold:1},
 ghost_fish:{tw:9,hh:5.4,pw:.6,pk:1.2,back:'c',side:'i',belly:'i',fin:'c',tail:'fan',th:6,dorsal:[.25,.6,3.5],anal:[.55,.7,2],pat:'ghost',eyeAt:.12,ghost:1},
};
function fish(c,W,H,s,f,t,id){
 const tw=s.tw,x0=tw,x1=W-1-(s.sn||0),L=x1-x0,A={},dH=s.pat==='puff'?0:Math.ceil(s.dorsal[2]*(s.sail?1:.9)+.4),aH=Math.ceil(s.anal[2]+.4);
 const hh=Math.min(s.hh,(H-2-dH-aH-1)/2),cy=Math.round(1+dH+hh);s={...s,th:Math.min(s.th,cy,H-1-cy)};
 const prof=u=>{u=clamp(u);if(s.prof==='ball')return Math.sqrt(Math.max(0,1-((u-.5)/.5)**2));return Math.pow(Math.sin(Math.PI*Math.pow(u,s.pk||1.15)),s.pw||.75);};
 const half=u=>Math.max(s.ped??.7,hh*prof(u));
 const top=[],bot=[],flick=[0,1,0,-1][f%4];
 for(let x=x0;x<=x1;x++){const h=half((x-x0)/L);top[x]=Math.round(cy-h);bot[x]=Math.round(cy+h);}
 const fin=s.fin,ghost=s.ghost;
 // tail
 for(let x=0;x<tw;x++){
  const d=(tw-x)/tw,ph=Math.max(.7,s.ped??.7),h=ph+(s.th-ph)*d,sh=Math.round(flick*d*1.2),n=s.tail==='fork'||s.tail==='lunate'?(s.tail==='lunate'?.55:.45)*d*h:0;
  for(let dy=-Math.round(h);dy<=Math.round(h);dy++){
   if(Math.abs(dy)<n)continue;
   if(s.tail==='hetero'&&dy>0&&dy>h*.55)continue;
   if(s.tail==='fan'&&Math.abs(dy)>h-.4*Math.sin(x*1.3))continue;
   if(s.tail==='round'&&Math.abs(dy)>h*Math.sqrt(1-d*d*.5))continue;
   const y=cy+dy+sh,edge=Math.abs(Math.abs(dy)-Math.round(h))<.5||(s.tail!=='round'&&Math.abs(Math.abs(dy)-n)<1);
   const ch=edge?(dy<0?'/':dy>0?'\\':'<'):((x+dy)%2?'-':'=');
   if(!ghost)c.solid(x,y,1,1,fin);
   c.put(x,y,ghost&&!edge?'.':ch,fin);
  }
 }
 // dorsal and anal fins
 const dfin=([u0,u1,h],up)=>{
  const a=Math.round(x0+u0*L),b=Math.round(x0+u1*L);
  for(let x=a;x<=b;x++){
   const k=(x-a)/Math.max(1,b-a),hgt=Math.round(h*(s.sail?1-k*.55:1-k*.8)+.4);
   for(let j=1;j<=hgt;j++){
    const y=up?top[x]-j:bot[x]+j;if(!ghost)c.solid(x,y,1,1,fin);
    c.put(x,y,j===hgt?(s.spiny?'^':up?(k<.5?'/':'\\'):(k<.5?'\\':'/')):(ghost?'.':':'),fin);
   }
  }
 };
 if(s.pat!=='puff')dfin(s.dorsal,true);dfin(s.anal,false);
 if(s.adip){for(let x=x0+Math.round(L*.18);x<x0+Math.round(L*.26);x++){c.solid(x,top[x]-1,1,1,fin);c.put(x,top[x]-1,'~',fin);}}
 // body
 for(let x=x0;x<=x1;x++){
  const u=(x-x0)/L,h=Math.max(.5,(bot[x]-top[x])/2),yc=(bot[x]+top[x])/2;
  for(let y=top[x];y<=bot[x];y++){
   const z=(y-yc)/h;let tone=z<-.35?s.back:z>.45?s.belly:s.side,ch=' ';
   if(s.patches){const q=s.patches.find(p=>u>=p[1]&&u<=p[2]&&z<.55+.2*Math.sin(x));if(q&&z<.6){tone=q[0];ch=((x+y)%3?'@':'o');}}
   if(!s.patches||ch===' '){
    if(y===top[x])ch='_';else if(y===bot[x])ch='~';
    else if(s.pat==='scales'||s.pat==='trout'||s.pat==='salmon'||s.pat==='mottle'||s.pat==='blotch'||s.pat==='cheek'){ch=(x+y*2)%4===0?'(':(x+y*2)%4===2?')':' ';}
    else if(s.pat==='scutes')ch=y===top[x]+1?(x%2?'^':'v'):(z>.3?'.':' ');
    else if(s.pat==='puff')ch=hash(x,y)%4===0?'.':hash(x,y)%7===0?'o':' ';
    else if(s.pat==='ghost')ch=(x%3===0&&z<.6)?'|':'.';
    else ch=(x+y)%5===0?'.':' ';
    if(s.pat==='trout'&&Math.abs(z-.05)<.34)tone=s.stripe,ch=(x%2?'=':'-');
    if(s.pat==='stripe'&&Math.abs(z-.05)<.3&&s.stripe!==s.side)ch=ch===' '?'=':'=',tone=s.stripe;
    if(s.pat==='blotch'&&Math.abs(z)<.45&&(x%6<3)&&u>.1&&u<.85)tone=s.stripe,ch='#';
    if(s.pat==='mottle'&&hash(id,x,y)%5===0)tone='z',ch='o';
    if(s.pat==='cheek'&&Math.abs(u-.82)<.06&&Math.abs(z+.1)<.4)tone='d',ch='@';
    if(s.pat==='salmon'&&z>.1&&u>.55)tone=s.blush,ch=ch===' '?'.':ch;
    if(s.pat==='salmon'&&hash(x,y)%9===0&&z<-.05)tone='k',ch='.';
    if(s.pat==='trout'&&hash(x,y)%6===0&&z<-.45)tone='k',ch='.';
   }
   if(s.gold&&hash(x,y,f%2)%11===0&&ch!==' ')tone='f';
   if(s.glow&&y===top[x]+1&&x%3===0)tone='f',ch='.';
   if(ghost)c.put(x,y,ch===' '?(z>.6?'.':' '):ch,tone);
   else{c.solid(x,y,1,1,tone);if(ch!==' ')c.put(x,y,ch,tone);}
  }
 }
 if(ghost){for(let x=x0+2;x<x1-3;x++)c.put(x,cy,x%2?'=':'-','f');c.put(x1-3,cy-1,'O','c');}
 // head: gill, eye, mouth, special jaws and whiskers
 const ex=x1-Math.round(s.eyeAt*L)-1,ey=Math.round(cy-hh*(s.prof==='ball'?.2:.3));
 c.put(x1-Math.round(L*.27),cy-1,')','k');c.put(x1-Math.round(L*.27),cy,')','k');if(hh>3.5)c.put(x1-Math.round(L*.27),cy+1,')','k');
 c.put(ex,ey,s.ghost?'@':'O',s.ghost?'c':'f');
 const mouthY=Math.round(cy+hh*.12);
 if(s.jaw){c.put(x1-3,mouthY,'<<=','k');c.put(x1-1,mouthY,'=','b');c.put(x1-4,mouthY+1,'\\_','k');}
 else if(s.pout){c.put(x1-1,mouthY,'o','r');c.put(x1,mouthY,')','q');}
 else if(s.hook){c.put(x1-1,mouthY,'-','k');c.put(x1-1,mouthY+1,'v','k');}
 else c.put(x1-1,mouthY,'-','d');
 if(s.bill){for(let x=x1+1;x<W;x++){c.put(x,cy-1,x-x1<s.bill-2?'=':'-','k');c.put(x,cy,x===W-1?'>':'=','t');}}
 if(s.snout){for(let x=x1+1;x<W;x++){c.put(x,cy,'=','k');c.put(x,cy-1,'_','s');}}
 if(s.whisk){for(let i=0;i<s.whisk;i++){const wy=mouthY+(i%2),wx=x1-1,sw=Math.round(Math.sin(f*1.1+i)*.8);const dir=i<s.whisk/2?1:-1;c.line(wx,wy+1,Math.min(W-1,wx+3+i%2),clamp(wy+2+sw+(i%2)*dir,0,H-1),null,'a');}}
 if(s.spines){for(let a=0;a<14;a++){const q=a/14*TAU,x=x0+L/2+Math.cos(q)*(L/2+1.4),y=cy+Math.sin(q)*(hh+.8);if(Math.abs(Math.sin(q))>.2&&Math.abs(Math.cos(q))<.97&&x>=0&&x<W&&y>=0&&y<H)c.put(x,y,'*','k');}}
 // pectoral fin flutter
 if(s.pat!=='ghost'||true){const px=x1-Math.round(L*.34),py=cy+Math.round(hh*.15);c.put(px-1,py,f%2?'(=':'(-','f');c.put(px,py+1,f%2?'`':'\'',s.fin);}
 if(s.gold)sparks(c,[[x0+3,1],[x1-6,H-2],[Math.round(W*.5),0]],f,'f');
 if(s.glow&&!s.gold)glint(c,x1-4,top[x1-4]-2,f,'f');
 if(s.ghost){sparks(c,[[x0+4,2],[x1-8,H-3]],f,'c');}
 A.entry={x:Math.round(W/2),y:H-1};A.contact={x:Math.round(x0+L*.5),y:cy};A.head={x:x1,y:cy};A.tail={x:0,y:cy};A.fin={x:Math.round(x0+L*.5),y:Math.max(0,top[Math.round(x0+L*.5)]-1)};
 return A;
}

// ------------------------------------------------------------------ collectible cards
const RANK={common:['s',1],uncommon:['g',2],rare:['w',3],epic:['v',4],mythic:['y',5]};
const HEAD=[[4,',','.','-'],[7,',','.',0],[9,'/','\\',0],[10,'|','|',0],[10,'|','|',0],[10,'|','|',0],[9,'\\','/',0],[7,"'","'",0],[4,"'","'",'_']];
const BODY=[[6,'/','\\'],[9,'/','\\'],[11,'/','\\'],[11,'|','|']];
// Front-facing duck head and shoulders, head rows y0..y0+8; 'bill' colours and body tone are options.
function duckBust(w,cx,y0,f,o={}){
 const body=o.body||'y';
 BODY.forEach(([hw,l,r],i)=>{const y=y0+9+i;w.solid(cx-hw,y,hw*2+1,1,o.shirt||body);w.put(cx-hw,y,l,body);w.put(cx+hw,y,r,body);});
 HEAD.forEach(([hw,l,r,top],i)=>{const y=y0+i;w.solid(cx-hw,y,hw*2+1,1,body);if(top)for(let x=-hw+1;x<hw;x++)w.put(cx+x,y,top,body);w.put(cx-hw,y,l,body);w.put(cx+hw,y,r,body);});
 w.put(cx-4,y0+3,f%6===5?'-':'O','f');w.put(cx+4,y0+3,f%6===5?'-':'O','f');
 w.put(cx-3,y0+4,'.-===-.','e');w.put(cx-3,y0+5,'( === )','e');w.put(cx-2,y0+6,"'---'",'e');
 if(o.blush){w.put(cx-7,y0+5,'**','q');w.put(cx+6,y0+5,'**','q');}
}
const FRAME_SCENES={
 portrait_cheese(w,f){
  duckBust(w,12,2,f,{blush:1});
  P(w,['  /\\  ',' /o \\ ','/__o_\\'],9,0,'y',{o:'a'},true);
  w.put(10,11,'>o<','r');sparks(w,[[2,2],[21,3],[20,9],[3,8]],f,'y');
 },
 portrait_emperor(w,f){
  duckBust(w,12,2,f,{shirt:'r'});
  P(w,[' ^ ^ ^ ^ ',' |/|/|/| ','|_*_*_*_|'],8,0,'y',{'*':'r'},true);
  w.put(7,11,'/~~~~~~~~~\\','f');w.put(11,12,'(O)','y');w.put(7,4,'\\','k');w.put(16,4,'/','k');
  sparks(w,[[2,3],[21,2],[21,9]],f,'y');
 },
 portrait_scholar(w,f){
  duckBust(w,12,2,f);
  w.put(7,5,'(','s');w.put(9,5,')','s');w.put(15,5,'(','s');w.put(17,5,')','s');w.put(10,5,'-----','s');
  P(w,['  _______  ',' /_______\\ ','<=========>'],6,0,'u',{'<':'y','>':'y'},true);w.put(17,3,'|','y');w.put(17,4,'o','y');
  P(w,['[=|=]'],10,11,'l',{},true);w.put(1,4,'E=mc','f');w.put(1,6,'a+b','s');w.put(1,8,'?','y');
 },
 portrait_artist(w,f){
  duckBust(w,12,2,f);
  P(w,['  _.--._  ',' (  @@  ) ',' `-.__.-\' '],7,0,'r',{'@':'f'},true);w.put(16,0,'*','r');
  P(w,['.--.','(o.o)',"'--'"],1,10,'n',{o:'r','.':'u'},true);
  w.line(20,13,22,6,null,'z');w.put(22,5,'v','q');if(f%4<2)w.put(21,3,'.','q');
 },
 portrait_explorer(w,f){
  duckBust(w,12,2,f);
  P(w,['   ___   ','  (___)  ','__/---\\__'],7,0,'a',{},true);w.put(9,1,'=====','z');
  P(w,['(oo)'],10,11,'t',{},true);w.put(8,12,'~~~~~~~~','e');
  P(w,['.-.','(+)',"'-'"],1,10,'p',{'+':'r'},true);w.put(20,11,'x','r');w.put(18,12,'...','a');
 },
 pond_frog(w,f){
  for(let x=0;x<24;x++)if((x+f)%4<2)w.put(x,12,'~','w');w.put(0,13,'~~~~~~~~~~~~~~~~~~~~~~~~','c');
  circ(w,12,11,1.8,'_','g',true);w.ellipse(12,11,11,1.6,'_','g',true);w.put(10,11,'<','h');
  w.ellipse(12,8,6,3,'-','h',true);
  circ(w,6,4,1.2,'o','h',true);circ(w,18,4,1.2,'o','h',true);w.put(5,4,'(O)','f');w.put(17,4,'(O)','f');w.put(6,4,'.','d');
  w.ellipse(12,6,6,2.2,'-','h',true);w.put(8,7,'\\_____ ____/','m');w.put(11,8,f%4<2?'(_)':'(.)','g');w.put(10,9,'. .','m');w.put(14,9,'.','m');
  w.put(3,10,'(_)','h');w.put(19,10,'(_)','h');
  w.put(20,2,'o','c');w.put(2,5,'.','c');if(f%3===0)w.put(21,6,'z','c');
 },
 pond_lily(w,f){
  for(let y=10;y<14;y++)for(let x=0;x<24;x++)if((x*2+y+f)%5<2)w.put(x,y,'~','w');
  w.ellipse(12,11,10,2.2,'_','g',true);w.line(12,11,22,10,'-','h');w.put(9,10,'. .','h');
  P(w,['  \\  |  /  ','\\ \\ \\|/ / /',' -\\_\\|/_/- ','  \\_(*)_/  ','    ~~~    '],6,3,'q',{'*':'y','|':'j','(':'y',')':'y'},true);
  w.put(1,2,'o','q');w.put(21,3,'.','w');glint(w,3,7,f,'q');glint(w,20,7,f,'f',2);
 },
 pond_dragonfly(w,f){
  for(const x of [2,4,19,21]){for(let y=3+(x%2);y<14;y++)w.put(x,y,'|','h');w.put(x,2+(x%2),'O','b');}
  const up=f%2===0;
  for(const sx of [-1,1]){
   w.ellipse(12+sx*6,up?4:6,5,1.4,'=','c',false);w.ellipse(12+sx*6,up?7:8,5.2,1.5,'=','i',false);
   w.put(12+sx*6-1,up?4:6,'. .','c');w.put(12+sx*6-1,up?7:8,'. .','i');
  }
  w.put(12,3,'@','x');w.put(12,2,'v','x');w.put(11,1,'\\ /','x');
  for(let y=4;y<13;y++){w.put(12,y,y<7?'#':(y%2?'=':'-'),y<7?'x':y%3?'c':'x');}
  w.put(12,13,'v','x');sparks(w,[[7,12],[18,11],[8,1]],f,'y');
 },
 pond_fish(w,f){
  for(let y=0;y<14;y++)for(let x=0;x<24;x++)if((x+y*2+f)%7===0)w.put(x,y,'~','w');
  const s={...FISH.goldfish,tw:6,hh:3.4,th:3.6,dorsal:[.3,.7,2],anal:[.55,.7,1.5],gold:1};
  fish(w,24,14,s,f,f/3,'pond_fish');
  w.put(20,2,'o','c');w.put(21,0,'O','c');w.put(2,11,'o','c');
 },
 weather_sun(w,f){
  circ(w,12,6,3,'-','y',true);w.put(10,5,'o  o','a');w.put(11,7,'\\__/','a');
  for(let i=0;i<14;i++){const a=i/14*TAU,r=(i+f)%2;w.put(12+Math.cos(a)*(8.5+r*1.3),6+Math.sin(a)*(5.2+r*.6),'*+'[(i+f)%2],'y');}
  P(w,['  .--.  ',' (    ) ','  `--\'  '],14,10,'f',{},true);
 },
 weather_rain(w,f){
  P(w,['    .--~~--.    ','  .(          ).','(               )',' `--~~~~~~~~--\' '],3,0,'t',{},true);
  for(let i=0;i<9;i++){const x=3+i*2.4,y=5+(i*3+f*2)%7;w.put(x,y,'/','w');w.put(x+1,y+1,'.','w');}
  for(let i=0;i<3;i++){const r=(f+i*2)%4;w.put(12-r*2-1,12+(i%2)*0,'~'.repeat(r*2+2),'w');}
  P(w,[' _.-._ ','/_____\\','   |   '],17,9,'r',{'|':'z'},true);w.put(1,11,'o','c');
 },
 weather_rainbow(w,f){
  const tones=['r','e','y','g','u','v'];
  tones.forEach((t,i)=>{const rx=11.5-i*1.05,ry=rx*.9;for(let k=0;k<=34;k++){const a=Math.PI*k/34;w.put(12-Math.cos(a)*rx,13-Math.sin(a)*ry,(k+f)%3?'=':'#',t);}});
  P(w,['.-~~-.','(     )'],0,11,'f',{},true);P(w,['.-~~-.','(     )'],17,11,'f',{},true);
  sparks(w,[[12,2],[3,4],[21,5]],f,'f');
 },
 weather_snow(w,f){
  w.solid(0,11,24,3,'p');for(let x=0;x<24;x++)w.put(x,11,(x+f)%3?'~':'-','f');
  P(w,['   ^   ','  /^\\  ',' /^^^\\ ','/^^^^^\\','   |   '],1,5,'h',{'|':'z'},true);w.put(3,6,'*','f');w.put(2,8,'~','f');w.put(4,9,'~','f');
  P(w,['.-.','(o)','/:\\','(:)'],17,7,'f',{o:'d',':':'k'},true);w.put(18,6,'_','z');w.put(17,6,'[','d');w.put(19,6,']','d');
  for(let i=0;i<14;i++){const h=hash('sn',i);w.put(h%24,(h>>>6)%10+((f*(1+h%2))%4),'*.+'[h%3],'f');}
 },
 legend_phoenix(w,f){
  for(let sd=-1;sd<=1;sd+=2)for(let i=0;i<6;i++)for(let j=0;j<5-i*.5;j++){
   const x=12+sd*(5+j*1.3+i*.5),y=3+i*1.7+j*.5-(f%2)*(i%2?.5:0),h=hash(f,i,j),tn=h%3===0?'y':h%3===1?'e':'r';
   w.put(x,y,'^~*'[(h>>>3)%3],tn);
  }
  for(let i=0;i<8;i++){const h=hash(f,i,'t'),tn=i%3?'e':'y';w.put(9+i%4*2,12+i%2,'~^'[h%2],tn);}
  duckBust(w,12,2,f,{body:'a',shirt:'e'});
  w.put(10,1,'^',(f%2)?'y':'e');w.put(12,0,'*','r');w.put(14,1,'^',(f%2)?'e':'y');
  sparks(w,[[1,1],[22,2],[2,12],[21,12]],f,'y');
 },
 legend_dragon(w,f){
  for(let sd=-1;sd<=1;sd+=2){w.line(12+sd*5,8,12+sd*11,1,null,'k');w.line(12+sd*11,1,12+sd*10,6,null,'k');w.line(12+sd*10,6,12+sd*8,10,null,'k');for(let k=0;k<5;k++)w.put(12+sd*(6+k),3+Math.abs(k-2)*.6+k*.6,'v','v');}
  duckBust(w,12,2,f,{body:'h',shirt:'m'});w.put(8,1,'/','f');w.put(16,1,'\\','f');w.put(7,0,'/','f');w.put(17,0,'\\','f');
  w.put(8,5,'@','y');w.put(16,5,'@','y');for(let i=0;i<4;i++)w.put(8+i*3,12,'^','m');
  const fl=[['~~~*','e'],['~*~~','r'],['*~~~','y']][f%3];w.put(18,7,fl[0],fl[1]);w.put(20,9,'~*','e');w.put(21,6,'.','y');
  sparks(w,[[1,2],[2,11]],f,'v');
 }
};
const CARDS={
 portrait_cheese:['rare','y','CHEESE'],portrait_emperor:['epic','r','EMPEROR DUCK'],portrait_scholar:['uncommon','u','SCHOLAR DUCK'],portrait_artist:['uncommon','q','ARTIST DUCK'],portrait_explorer:['rare','m','EXPLORER DUCK'],
 pond_frog:['common','c','FRIENDLY FROG'],pond_lily:['common','w','WATER LILY'],pond_dragonfly:['uncommon','g','DRAGONFLY'],pond_fish:['rare','w','GOLDEN FISH'],
 weather_sun:['common','u','SUNNY DAY'],weather_rain:['common','u','RAINY DAY'],weather_rainbow:['epic','w','RAINBOW'],weather_snow:['uncommon','i','SNOWY DAY'],
 legend_phoenix:['mythic','e','PHOENIX DUCK'],legend_dragon:['mythic','v','DRAGON DUCK']};
function blit(c,sub,dx,dy){
 sub.art.forEach((row,y)=>row.forEach((ch,x)=>{if(ch!==' ')c.put(dx+x,dy+y,ch,sub.tones[y][x]);}));
 for(const q of sub.fills){if(q.y<0||q.y>=sub.h)continue;const a=Math.max(0,q.x),b=Math.min(sub.w,q.x+q.w);if(b>a)c.solid(dx+a,dy+q.y,b-a,1,q.tone);}
}
function card(c,W,H,s,f,t,id){
 const [rank,win,name]=CARDS[id],[tone,stars]=RANK[rank];
 c.rect(0,0,W,H,tone,true);c.solid(2,2,26,16,win);c.rect(2,2,26,16,'k',false);
 {const sub=new ObjectCanvas(24,14);FRAME_SCENES[id](sub,f);blit(c,sub,3,3);}
 // window corners re-drawn above the scene
 c.put(2,2,'+','y');c.put(27,2,'+','y');c.put(2,17,'+','y');c.put(27,17,'+','y');
 c.solid(3,19,24,5,'d');c.rect(2,19,26,5,tone,false);
 ctext(c,15,20,name,'f');
 
 for(let i=0;i<5;i++)c.put(11+i*2,22,i<stars?'*':'.',i<stars?'y':'k');
 c.put(1,0,'.','f');if(stars>=4&&f%4<2){c.put(1,1,'*','y');c.put(28,24,'*','y');}
 if(stars>=4)c.put(0,0,'*','y');
 return {entry:{x:15,y:H-1},contact:{x:15,y:10},face:{x:15,y:10},label:{x:15,y:20},rim:{x:15,y:0},emblem:{x:15,y:8}};
}

// ------------------------------------------------------------------ shapes and emblems
// Visual space: X = column offset, Y = row offset * 1.5 (cells are 1 wide, 1.5 tall).
const SHAPES={
 round:R=>(X,Y)=>X*X+Y*Y<=R*R,
 shield:R=>(X,Y)=>{if(Y<-.9*R||Y>R)return false;const w=Y<.1*R?.95*R:.95*R*Math.sqrt(Math.max(0,1-((Y-.1*R)/(.9*R))**2));return Math.abs(X)<=w;},
 hex:R=>(X,Y)=>Math.abs(Y)<=R*.88&&Math.abs(X)<=R-Math.abs(Y)*.58,
 heart:R=>(X,Y)=>{const x=X/R*1.25,y=-Y/R*1.25+.2;return (x*x+y*y-1)**3-x*x*y**3<=0;},
 rosette:R=>(X,Y)=>{const a=Math.atan2(Y,X);return Math.hypot(X,Y)<=R*(.93+.07*Math.cos(a*14));},
 star:R=>(X,Y)=>{const a=Math.atan2(Y,X)+Math.PI/2,k=((a%(TAU/5))+TAU/5)%(TAU/5)-TAU/10;return Math.hypot(X,Y)*Math.cos(k)*1.0<=R*.62/Math.cos(Math.PI/5)*Math.cos(Math.abs(k)>0?Math.min(Math.abs(k),Math.PI/5):0)*1.0+R*.38*(1-Math.abs(k)/(Math.PI/5));},
 pointy:R=>(X,Y)=>{if(Y<-R||Y>R)return false;const w=R*.8*Math.pow(1-Math.abs(Y/R),.7);return Math.abs(X)<=w+.2;},
};
function blob(c,kind,cx,cy,R,rim,fill,edge=true){
 const inside=SHAPES[kind](R),at=(x,y)=>inside(x-cx,(y-cy)*1.5);
 const rows=Math.ceil(R/1.5)+2,cols=Math.ceil(R)+2;
 for(let y=Math.floor(cy-rows);y<=Math.ceil(cy+rows);y++)for(let x=Math.floor(cx-cols);x<=Math.ceil(cx+cols);x++){
  if(!at(x,y))continue;
  if(fill)c.solid(x,y,1,1,fill);
  if(!edge)continue;
  const l=!at(x-1,y),r=!at(x+1,y),u=!at(x,y-1),d=!at(x,y+1);if(!(l||r||u||d))continue;
  c.put(x,y,u&&(l||r)?'.':d&&l?'`':d&&r?"'":u?'_':d?'-':l?'(':')',rim);
 }
}
// Small row-art emblems; 'tone' is the main ink, 'map' recolours chosen glyphs.
const EMB={
 heart:[".-. .-.","(  V  )"," \\   / ","  \\ /  ","   v   "],
 flower:["  .-.  "," ( * ) ","--\\ /--"," (  \\)  ","  \\|/  ","   |   "],
 sun:[" \\ | / ","  .-.  ","--(@)--","  `-'  "," / | \\ "],
 wheat:["  ,  "," ,|, ","_\\|/_","_\\|/_"," _|_ ","  |  "],
 snow:["  |  ","\\ | /","--*--","/ | \\","  |  "],
 star:["   *   ","  /|\\  ","<--*-->","  \\|/  ","   *   "],
 compass:[" .-N-. ","( \\|/ )","W-(@)-E","( /|\\ )"," `-S-' "],
 sprout:["  \\ /  "," (\\Y/) ","  \\|/  ","   |   ","  _|_  "],
 notes:["  _____"," /|   |"," | |  |"," o_|  o","  (_)  "],
 flag:["|###..##","|.#.##.#","|##..##.","|"],
 duckhead:[" .-\"-. ","( o o )"," \\ = / ","  `-'  "],
 clover:[" _ _ ","(_V_)","(_|_)","  |  "],
 eye:[" .-\"\"-. ","( (@@) )"," `-..-' "],
 wave:["~~~~~~~","\\/\\/\\/\\","~~~~~~~"],
 drop:["  .  "," / \\ ","(   )"," `-' "],
 mountain:["  /\\   "," /  \\/\\","/_ _ _ \\"],
 sprig:["  \\|/  ","   |   ","  /|\\  "],
 cloud:[" .--. ","(    )"," `--' "],
 bolt:[" /| ","/_ |"," /|/","/_/ "],
 laurel:["\\\\ // ","|\\\\//|","|/\\\\/|"," \\  / "],
 rainbow:[".--==--.","/.-==-.\\","| |  | |"],
 bird:["   _   ","  (o)>=","~~~\\_/ ","   /\\  "],
 wing:["<<(V)>>"],
};
const emb=(c,name,cx,cy,tone,map={})=>PC(c,EMB[name],cx,cy,tone,map);
const ribbonV=(c,cx,y0,len,tone,tone2)=>{ // V-shaped neck ribbon dropping to the medal
 for(let i=0;i<len;i++){c.put(cx-8+i*1.2,y0+i,'\\\\',tone);c.put(cx-6+i*1.2,y0+i,'\\\\',tone2);c.put(cx+7-i*1.2,y0+i,'//',tone);c.put(cx+5-i*1.2,y0+i,'//',tone2);}
};

// ------------------------------------------------------------------ badges
const BADGES={
 best_friend_badge:{shape:'round',rim:'q',inner:'l',emb:'heart',map:{V:'f'},tone:'q',bow:'w',sub:'u'},
 spring_spirit_badge:{shape:'round',rim:'g',inner:'h',emb:'flower',tone:'q',map:{'*':'y','|':'g','\\':'g','/':'g'},leaves:'g'},
 summer_spirit_badge:{shape:'shield',rim:'y',inner:'u',emb:'sun',tone:'y',map:{'@':'e'}},
 harvest_spirit_badge:{shape:'hex',rim:'e',inner:'z',emb:'wheat',tone:'y',map:{}},
 winter_spirit_badge:{shape:'rosette',rim:'i',inner:'u',emb:'snow',tone:'f',map:{'*':'w'}},
 love_spirit_badge:{shape:'heart',rim:'r',inner:'j',emb:'heart',tone:'q',map:{V:'f'}},
 duck_day_champion_badge:{shape:'rosette',rim:'y',inner:'r',emb:'duckhead',tone:'y',map:{o:'f'},ribbons:['r','u'],laurel:1},
 explorer_badge:{shape:'pointy',rim:'a',inner:'m',emb:'compass',tone:'y',map:{'@':'r',N:'r'},strap:1},
 golden_badge:{shape:'shield',rim:'y',inner:'a',emb:'sprout',tone:'g',map:{Y:'y'},glow:1},
};
function badge(c,W,H,s,f,t,id){
 const cx=W/2,cy=s.ribbons||s.bow?8:Math.floor(H/2),R={heart:11,pointy:11.5,shield:10.5,hex:10,rosette:10,round:9.5}[s.shape];
 if(s.ribbons)for(let i=0;i<5;i++){c.put(cx-6+i*.5,cy+8+i,'\\\\','r');c.put(cx-3+i*.5,cy+8+i,'\\\\','u');c.put(cx+5-i*.5,cy+8+i,'//','r');c.put(cx+2-i*.5,cy+8+i,'//','u');}
 if(s.bow){const y=cy+8;P(c,['\\\\  //','(\\/ )'],cx-3,y,s.bow);c.put(cx-7,y+1,'~~~','w');c.put(cx+4,y+1,'~~~','w');c.put(cx-5,y+2,'\\\\','w');c.put(cx+4,y+2,'/','w');}
 if(s.strap){c.line(cx,0,cx,2,'|','z');c.put(cx-1,0,'(_)','z');}
 blob(c,s.shape,cx,cy,R,s.rim,s.rim);
 blob(c,s.shape,cx,cy,R*.78,s.tone==='f'?'w':s.rim,s.inner);
 emb(c,s.emb,cx,cy,s.tone,s.map);
 if(s.laurel){c.put(cx-11,cy,'(\\\\','h');c.put(cx+9,cy,'//)','h');}
 if(s.leaves){c.put(cx-11,cy+4,'~\\\\','g');c.put(cx+9,cy+4,'/~','g');}
 sparks(c,[[cx-R*.9,cy-R*.35],[cx+R*.95,cy-R*.4]],f,s.glow?'f':s.rim);
 if(s.glow){sparks(c,[[cx,0],[cx-R,cy+R*.3],[cx+R*.9,cy+R*.5]],f,'y');}
 return {entry:{x:cx,y:H-1},contact:{x:cx,y:cy},emblem:{x:cx,y:cy},rim:{x:cx-R*.8,y:cy},ribbon:{x:cx,y:Math.min(H-1,cy+10)}};
}
const MEDALS={
 racing_medal:{rim:'y',inner:'e',emb:'flag',tone:'f',map:{'.':'d','#':'f','|':'z'},ribbon:['u','f'],shape:'round'},
 dance_medal:{rim:'t',inner:'v',emb:'notes',tone:'q',map:{o:'y'},ribbon:['v','q'],shape:'round'},
};
function medal(c,W,H,s,f,t,id){
 const cx=W/2,cy=18,R=7.8;
 for(let i=0;i<11;i++){const y=i;c.put(cx-8+i*.65,y,'\\\\',s.ribbon[0]);c.put(cx-6+i*.65,y,'\\\\',s.ribbon[1]);c.put(cx+7-i*.65,y,'//',s.ribbon[0]);c.put(cx+4.5-i*.65,y,'//',s.ribbon[1]);}
 c.put(cx-2,10,'[=]','t');
 blob(c,s.shape,cx,cy,R*1.3,s.rim,s.rim);blob(c,s.shape,cx,cy,R*1.3*.75,s.rim,s.inner);
 emb(c,s.emb,cx,cy,s.tone,s.map);
 sparks(c,[[cx-9,cy-7],[cx+9,cy+5]],f,'f');
 return {entry:{x:cx,y:H-1},contact:{x:cx,y:cy},emblem:{x:cx,y:cy},ribbon:{x:cx,y:3},rim:{x:cx-8,y:cy}};
}
// ------------------------------------------------------------------ tokens: ancient stone discs
const TOKENS={
 water_token:{rim:'s',inner:'u',emb:'drop',emb2:'wave',tone:'w',tone2:'c',shape:'round',moss:'h'},
 earth_token:{rim:'b',inner:'z',emb:'mountain',emb2:'sprig',tone:'a',tone2:'g',shape:'hex'},
 sky_token:{rim:'t',inner:'l',emb:'cloud',emb2:'bolt',tone:'f',tone2:'y',shape:'round'},
};
function token(c,W,H,s,f,t,id){
 const cx=W/2,cy=8,R=9.5;
 blob(c,s.shape,cx,cy,R,s.rim,s.rim);blob(c,s.shape,cx,cy,R*.78,s.rim,s.inner);
 for(let i=0;i<12;i++){const a=i/12*TAU;c.put(cx+Math.cos(a)*R*.86,cy+Math.sin(a)*R*.86/1.5,i%2?'.':':',s.tone2);}
 const pulse=f%4;emb(c,s.emb,cx,cy-1,pulse<2?s.tone:'f');c.put(cx-3,cy+3,id==='water_token'?'~ ~ ~':id==='earth_token'?'. : .':'- = -',s.tone2);
 if(s.moss)for(let i=0;i<5;i++)c.put(cx-8+i*4,cy+7-i%2,'"',s.moss);
 if(id==='earth_token'){c.put(cx-9,cy-4,'/\\\\','z');c.put(cx+7,cy+5,'x','k');}
 if(id==='sky_token'){c.put(cx+7,cy-6,pulse%2?'z':'Z','y');c.put(cx-9,cy+4,'/','y');}
 sparks(c,[[cx-R-1,cy-4],[cx+R,cy+3]],f,s.tone);
 return {entry:{x:cx,y:H-1},contact:{x:cx,y:cy},emblem:{x:cx,y:cy},rim:{x:cx-R*.8,y:cy}};
}
// ------------------------------------------------------------------ charms and amulets
const CHARMS={
 ancient_amulet:{shape:'pointy',rim:'n',inner:'z',tone:'y',emb:'eye',cord:'z'},
 lucky_charm:{shape:'hex',rim:'i',inner:'g',tone:'g',emb:'clover',cord:'t',crystal:1},
 magpie_friendship_charm:{shape:'round',rim:'t',inner:'u',tone:'f',emb:'bird',cord:'q',map:{o:'y','=':'y','>':'y','~':'w'}},
 rainbow_charm:{shape:'round',rim:'f',inner:'w',tone:'q',emb:'rainbow',cord:'t',glow:1},
 guardian_blessing:{shape:'round',rim:'y',inner:'d',tone:'y',emb:'wing',cord:null,glow:1},
};
function charm(c,W,H,s,f,t,id){
 const cx=W/2,cy=s.cord?15:12,R=s.shape==='pointy'?11:9;
 if(s.cord){for(let i=0;i<5;i++){c.put(cx-4+i*.4-i*.2,1+i,i%2?'(':'.','z');}c.ellipse(cx,3,4,2.5,'-',s.cord,false);c.put(cx-1,5,'||',s.rim);}
 if(id==='guardian_blessing'){
  for(let r=0;r<3;r++){const rr=(f+r)%3;for(let i=0;i<20;i++){const a=i/20*TAU;dot(c,cx+Math.cos(a)*(5+rr*2.8)*1.2,cy+Math.sin(a)*(5+rr*2.8)/1.5*1.2,rr===0?'o':'.','y');}}
 }
 blob(c,s.shape,cx,cy,R,s.rim,s.rim);blob(c,s.shape,cx,cy,R*.76,s.rim,s.inner);
 if(s.crystal){for(const [dx,dy,ch] of [[-8,-4,'/'],[8,-4,'\\\\'],[-8,4,'\\\\'],[8,4,'/'],[0,-8,'^'],[0,8,'v']])c.put(cx+dx,cy+dy,ch,'w');c.put(cx-5,cy-5,'\\\\','f');}
 emb(c,s.emb,cx,cy,s.tone,s.map||{});
 if(id==='ancient_amulet'){c.put(cx-4,cy+4,'-- ~ --','a');c.put(cx-2,cy-5,'|||','k');c.put(cx-2,cy,f%4<2?'(@@)':'(oo)','y');for(let i=0;i<3;i++)dot(c,cx-5+i*5,cy+6-((f+i)%3),'.','a');}
 if(id==='rainbow_charm'){const tn=['r','e','y','g','u','v'];for(let i=0;i<6;i++)c.put(cx-6+i*2,cy+4,'=',tn[(i+f)%6]);}
 if(id==='guardian_blessing')c.put(cx-4,cy+4,'(  *  )','f');
 sparks(c,[[cx-R-2,cy-4],[cx+R+1,cy+2],[cx+2,cy+R/1.5+2]],f,s.glow?'f':s.tone);
 return {entry:{x:cx,y:H-1},contact:{x:cx,y:cy},emblem:{x:cx,y:cy},cord:{x:cx,y:3},rim:{x:cx-R*.7,y:cy}};
}
// ------------------------------------------------------------------ coins and buttons
function coin(c,W,H,s,f,t,id){
 const cx=W/2,cy=Math.floor(H/2)-0,R=id==='bottle_cap'?9:10;
 if(id==='old_coin'){
  blob(c,'round',cx,cy,R,'z','b');blob(c,'round',cx,cy,R*.78,'z','z');
  P(c,['.-"-.','( o )',' \\=/ '],cx-3,cy-2,'a',{o:'z'});c.put(cx+4,cy-3,'/','k');c.put(cx-6,cy+2,'x','h');c.put(cx+3,cy+3,'.','h');c.put(cx-7,cy-1,'.:','h');glint(c,cx+6,cy-4,f,'f');
 }else if(id==='ancient_coin'){
  blob(c,'round',cx,cy,R+.5,'y','y');blob(c,'round',cx,cy,R*.8,'a','a');
  for(let i=0;i<16;i++){const a=i/16*TAU;c.put(cx+Math.cos(a)*R*.62*1.5/1.2,cy+Math.sin(a)*R*.62/1.2,'o','y');}
  emb(c,'sun',cx,cy,'y',{'@':'f'});sparks(c,[[cx-R-1,cy-4],[cx+R,cy+4],[cx+3,cy-7]],f,'f');
 }else if(id==='shiny_button'){
  blob(c,'round',cx,cy,R,'c','c');blob(c,'round',cx,cy,R*.75,'x','x');
  for(const [dx,dy] of [[-2,-1],[2,-1],[-2,1],[2,1]])c.put(cx+dx*1.5-.5,cy+dy*1.4,'O','f');
  c.put(cx-3.5,cy-1.5,'\\\\','f');c.put(cx+2,cy+.5,'\\\\','f');c.put(cx-3,cy+1.5,'/','f');c.put(cx+2,cy-1.5,'/','f');
  c.put(cx-6,cy-3,'*','f');if(f%4<2)c.put(cx+5,cy-4,'+','f');
 }else{
  blob(c,'rosette',cx,cy,R+1,'t','t');blob(c,'round',cx,cy,R*.7,'s','u');
  P(c,["'.-.'",'|   |',"'-\\''"].slice(0,1),cx-2,cy-1,'f');c.put(cx-2,cy,'(D)','y');c.put(cx-4,cy-3,'*','f');if(f%3===0)c.put(cx+5,cy-3,'+','f');
  c.put(cx-8,cy+2,'.','f');c.put(cx+7,cy+1,'.','f');
 }
 return {entry:{x:cx,y:H-1},contact:{x:cx,y:cy},face:{x:cx,y:cy},rim:{x:cx-R*.9,y:cy}};
}
// ------------------------------------------------------------------ scales
function scaleItem(c,W,H,s,f,t,id){
 const cx=W/2,cy=12;
 if(id==='dragon_scale'){
  const sh=SHAPES.pointy(13);
  blob(c,'pointy',cx,cy+1,12.5,'r','r');blob(c,'pointy',cx,cy+1,10,'e','e');blob(c,'pointy',cx,cy+1,6.8,'o','o');
  for(let k=0;k<4;k++)c.put(cx-5+k,cy-3+k*1.5,'(','r'),c.put(cx+5-k,cy-3+k*1.5,')','r');
  for(let k=1;k<=3;k++)c.put(cx-4,cy-6+k*2.4,'~'.repeat(9),k%2?'y':'e');
  c.put(cx-1,cy-8,'|','r');c.put(cx-1,cy+7,'v','r');
  for(let i=0;i<4;i++){const h=hash('dr',i,f);c.put(cx-4+i*3+(h%2),1+(h>>>3)%3,'^~'[h%2],'e');}
  sparks(c,[[2,6],[W-3,15]],f,'y');
 }else{
  const tn=['c','l','q','w','x','v'],base=H-3;
  // a fan-shaped scale: radial ribs and scalloped bands whose colours shift like mother-of-pearl
  const R=12,at=(x,y)=>{const X=x-cx,Y=(y-base)*1.5;return Y<=0&&Math.hypot(X,Y)<=R*1.0&&Math.abs(X)<=R*.95;};
  for(let y=1;y<=base;y++)for(let x=1;x<W-1;x++){
   if(!at(x,y))continue;const X=x-cx,Y=(y-base)*1.5,r=Math.hypot(X,Y),a=Math.atan2(-Y,X),band=Math.floor(r/3);
   const tone=tn[(band+Math.floor(a*3)+f)%6];c.solid(x,y,1,1,band%2?'l':'v');
   const edge=!at(x-1,y)||!at(x+1,y)||!at(x,y-1);
   c.put(x,y,edge?(!at(x,y-1)?'_':!at(x-1,y)?'(':')'):((band+x)%2?')':'(' ),tone);
  }
  for(let i=1;i<7;i++){const a=Math.PI*i/7;c.line(cx,base,cx+Math.cos(a)*R*.9,base-Math.sin(a)*R*.9/1.5,null,tn[(i+f)%6]);}
  c.put(cx-3,base+1,'\\___/','x');c.put(cx-1,base+2,'v','x');
  c.put(cx-6,3,'\\','f');c.put(cx-8,5,'.','f');
  sparks(c,[[cx-9,3],[cx+8,4],[cx+1,0],[cx+10,12]],f,'f');
 }
 return {entry:{x:cx,y:H-1},contact:{x:cx,y:cy},face:{x:cx,y:cy},tip:{x:cx,y:H-3}};
}

// ------------------------------------------------------------------ feathers
const FEATHERS={
 feather:{hw:4.6,cols:['x','x','g','q','q'],spine:'f',tip:'f'},
 golden_feather:{hw:4.4,cols:['y','a','y','y','f'],spine:'f',glint:1},
 eagle_feather:{hw:5.2,cols:['f','b','z','b','z','b','n'],band:1,spine:'a'},
 rainbow_feather:{hw:4.6,cols:['r','e','y','g','c','u','v'],spine:'f',cycle:1,glint:1},
 static_feather:{hw:4.4,cols:['w','w','i','w','c'],spine:'y',spark:1},
 snow_feather:{hw:4.8,cols:['f','i','f','f','i'],spine:'w',snow:1},
 ancient_feather:{hw:4.6,cols:['n','n','b','n','s'],spine:'z',age:1},
};
function feather(c,W,H,s,f,t,id){
 const sway=Math.sin(t*2.2)*1.2,top=1,bot=H-5,n=bot-top,cols=s.cols;
 const sx=v=>W*.34+v*W*.3+Math.sin(v*Math.PI)*sway;
 let tip={x:0,y:top};
 for(let i=0;i<=n;i++){
  const v=i/n,y=bot-i,x=Math.round(sx(v));
  const hw=v<.1?0:s.hw*Math.pow(Math.sin(Math.PI*Math.min(1,(v-.06)/.94)),.55);
  const idx=Math.min(cols.length-1,Math.floor(v*cols.length)),tn=s.cycle?cols[(idx+f)%cols.length]:s.band&&i%4<2&&v>.15?'z':cols[idx];
  const l=Math.round(hw),r=Math.round(hw*.72);
  for(let k=1;k<=l;k++){
   if(s.age&&hash(id,i,k)%6===0)continue;
   c.solid(x-k,y,1,1,tn);c.put(x-k,y,k===l?'(':(i+k)%3===0?':':'\\\\',tn);
  }
  for(let k=1;k<=r;k++){
   if(s.age&&hash(id,i,k,1)%6===0)continue;
   c.solid(x+k,y,1,1,tn);c.put(x+k,y,k===r?')':(i+k)%3===0?':':'/',tn);
  }
  c.put(x,y,v<.1?'|':v>.97?'^':'!',v<.1?'p':s.spine);
  if(i===n)tip={x,y};
 }
 const bx=Math.round(sx(0));for(let j=0;j<4;j++)c.put(bx-j*.3,bot+1+j,'|','p');
 if(s.glint)sparks(c,[[W-4,3],[2,9],[W-6,16]],f,'f');
 if(s.spark)for(let i=0;i<4;i++){const h=hash('st',i,f),x=2+h%(W-4),y=3+(h>>>5)%(H-8);c.put(x,y,['/\\\\','~','Z','/'][h%4],'y');}
 if(s.snow)for(let i=0;i<9;i++){const h=hash('sn',i),x=1+h%(W-2),y=(h>>>5)%H+Math.floor(f*.7);c.put(x,(y)%(H-1),'*.+'[h%3],'f');}
 if(s.age){c.put(bx-2,bot+2,'~o~','z');c.put(bx-1,bot+3,'|','z');for(let i=0;i<5;i++){const h=hash('ad',i),y=top+h%n;c.put(W-3-h%3,y,'.','s');}c.put(3,H-3,'.:','s');}
 return {entry:{x:bx,y:H-1},contact:{x:Math.round(sx(.12)),y:bot-1},quill:{x:bx,y:bot+2},tip,vane:{x:Math.round(sx(.5)),y:Math.round(top+n/2)}};
}
// ------------------------------------------------------------------ crowns
const CROWNS={
 tiny_crown:{n:3,tone:'y',h:[5,6,5],gems:['r'],ball:1},
 duck_crown:{n:5,tone:'y',h:[6,9,10,9,6],gems:['r','u','g','u','r'],cap:'r',fur:1,ball:1,duck:1},
 ancient_crown:{n:5,tone:'z',h:[6,8,9,6,5],gems:['h','','g','','h'],patina:1,broken:3,dull:'b'},
 snowflake_crown:{n:5,tone:'i',h:[6,9,10,9,6],gems:['w','c','w','c','w'],flake:1,hi:'f'},
};
function crown(c,W,H,s,f,t,id){
 const bandH=Math.max(3,Math.round(H*.24)),by=H-bandH-1,x0=2,x1=W-3,span=x1-x0,cx=W/2;
 if(s.cap){circ(c,cx,by-3,4,'-',s.cap,true);c.ellipse(cx,by-2,span*.4,4,'~',s.cap,true);}
 // points rise from the band
 for(let i=0;i<s.n;i++){
  const px=x0+2+i*(span-4)/(s.n-1),h=s.h[i]*Math.min(H/20,(by-3)/Math.max(...s.h)),top=by-h;
  if(s.broken===i)continue;
  const hw=Math.max(2,span/s.n/2-1);
  for(let y=Math.round(top);y<by;y++){const k=(y-top)/h,w=Math.round(1+k*hw);c.solid(px-w,y,w*2+1,1,s.tone);c.put(px-w,y,'/',s.tone);c.put(px+w,y,'\\\\',s.tone);if(s.hi&&(y+i)%3===0)c.put(px,y,'*',s.hi);else if(k>.3)c.put(px,y,'|',s.tone);}
  if(s.flake){c.put(px-1,top-1,'\\\\|/',s.tone);c.put(px-1,top,'-*-',s.hi);c.put(px-1,top+1,'/|\\\\',s.tone);}
  else if(s.ball)c.put(px,top-1,'o',i===(s.n>>1)&&s.duck?'r':'f');
  else c.put(px,top,'^',s.tone);
 }
 if(s.broken!==undefined){const px=x0+2+s.broken*(span-4)/(s.n-1);c.put(px-1,by-2,'/\\\\_','z');c.put(px-1,by-1,'/_',s.tone);}
 // band
 c.solid(x0,by,span+1,bandH,s.tone);c.rect(x0,by,span+1,bandH,s.dull||'a',false);
 for(let i=0;i<s.n;i++){const gx=x0+2+i*(span-4)/(s.n-1);if(s.gems[i])c.put(gx-1,by+Math.floor(bandH/2),'<'+'>',s.gems[i]);}
 for(let x=x0+2;x<x1-1;x+=2)if(!s.gems.some((g,i)=>g&&Math.abs(x0+2+i*(span-4)/(s.n-1)-x)<3))c.put(x,by+Math.floor(bandH/2),'.',s.hi||'f');
 if(s.fur){for(let x=x0;x<=x1;x++)c.put(x,H-1,(x+f)%2?'~':'~','f');}
 if(s.duck){P(c,['(o>'],cx-1,by-s.h[2]*(H/20)-3,'y');}
 if(s.patina){for(let i=0;i<7;i++){const h=hash('pa',i);c.put(x0+h%span,by+h%bandH,'"','h');}c.put(x0+4,by+bandH-1,'x','k');c.put(cx+3,by-3,'.','s');}
 sparks(c,[[2,2],[W-3,3],[cx,0]],f,s.hi||'f');
 return {entry:{x:cx,y:H-1},contact:{x:cx,y:by+1},rim:{x:cx,y:by},gem:{x:cx,y:by+1},tip:{x:cx,y:Math.max(0,by-s.h[s.n>>1]*Math.min(H/20,(by-3)/Math.max(...s.h)))}};
}
// ------------------------------------------------------------------ hats and wreaths
function floral(c,x,y,kind,tone,mid,f){
 if(kind==='blossom'){c.put(x-1,y-1,'.@.',tone);c.put(x-1,y,'@'+'*'+'@',tone);c.put(x,y,'*',mid);c.put(x-1,y+1,"'@'",tone);}
 else if(kind==='daisy'){c.put(x-1,y-1,'\\\\|/','f');c.put(x-1,y,'-'+'o'+'-',tone);c.put(x,y,'o',mid);c.put(x-1,y+1,'/|\\\\','f');}
 else if(kind==='tulip'){c.put(x-1,y-1,'\\\\|/',tone);c.put(x-1,y,'(_)',tone);c.put(x,y+1,'|','h');}
 else{c.put(x-1,y,'(@)',tone);c.put(x,y,'@',mid);}
}
const HATS={
 heart_hat:{dome:'q',brim:'r',deco:'hearts',tone:'r',tone2:'f'},
 cherry_blossom_hat:{dome:'n',brim:'a',deco:'blossom',tone:'q',tone2:'y'},
 autumn_wreath_hat:{dome:'z',brim:'b',deco:'leaves',tone:'e',tone2:'r'},
};
function hat(c,W,H,s,f,t,id){
 const cx=W/2,cy=12;
 c.ellipse(cx,cy+6,17,2.2,'_',s.brim,true);
 c.ellipse(cx,cy+1,11,7,'-',s.dome,true);
 c.line(cx-11,cy+5,cx+11,cy+5,'=',s.brim);
 if(s.deco==='hearts'){
  for(const [dx,dy,tn] of [[-8,0,'r'],[-3,-4,'f'],[3,-1,'r'],[8,1,'f'],[-5,3,'f'],[0,2,'r'],[6,-4,'r']])c.put(cx+dx-1,cy+dy,'<3',tn);
  c.put(cx-12,cy+8,'`~~',s.brim);c.put(cx+9,cy+8,'~~\'',s.brim);
 }else if(s.deco==='blossom'){
  c.line(cx-12,cy+4,cx+11,cy+4,'~','z');
  [[-9,3],[-4,-4],[2,-5],[7,0],[-1,2],[10,4],[-12,5]].forEach(([dx,dy],i)=>floral(c,cx+dx,cy+dy,'blossom','q','y',f));
  for(let i=0;i<4;i++){const h=hash('pt',i),x=2+h%(W-4),y=(h>>>4)%8+((f+i*2)%6);c.put(x,Math.min(H-1,y+2),'~','q');}
 }else{
  for(let i=0;i<9;i++){const a=Math.PI*(1.05+i*.11),x=cx+Math.cos(a)*11.5,y=cy+1+Math.sin(a)*8.2;c.put(x-1,y,i%2?'<@>':'>@<',['e','r','y','o'][i%4]);}
  c.put(cx+7,cy-6,'(o)','a');c.put(cx+7,cy-7,'/','z');P(c,['\\\\ /','>@<'],cx-12,cy-6,'r');
  c.put(cx-14,cy+9,'<',(f%3)?'e':'y');
 }
 sparks(c,[[2,3],[W-3,5]],f,s.tone);
 return {entry:{x:cx,y:H-1},contact:{x:cx,y:cy+5},rim:{x:cx,y:cy+6},emblem:{x:cx,y:cy-2},brim:{x:cx-12,y:cy+6}};
}
const WREATHS={
 flower_wreath:{kinds:['daisy','blossom','tulip','daisy'],tones:['y','q','r','w','l','o'],mids:['a','y','f','y','y','f'],ribbon:0},
 spring_wreath:{kinds:['tulip','blossom','blossom','tulip'],tones:['q','f','l','y','w','q'],mids:['y','y','a','f','y','a'],ribbon:'w',eggs:1},
};
function wreath(c,W,H,s,f,t,id){
 const cx=W/2,cy=H/2-1,rx=15,ry=9;
 for(let i=0;i<60;i++){const a=i/60*TAU;const x=cx+Math.cos(a)*rx,y=cy+Math.sin(a)*ry;c.put(x,y,';:"\''[i%4],i%3?'h':'m');c.put(cx+Math.cos(a)*(rx-2),cy+Math.sin(a)*(ry-1.4),'"~'[i%2],'h');}
 for(let i=0;i<10;i++){const a=i/10*TAU+.3;floral(c,Math.round(cx+Math.cos(a)*rx),Math.round(cy+Math.sin(a)*ry),s.kinds[i%s.kinds.length],s.tones[i%s.tones.length],s.mids[i%s.mids.length],f);}
 if(s.eggs)for(const [dx,dy,tn] of [[-4,8,'q'],[5,8,'l']])c.put(cx+dx,cy+dy,'(_)',tn);
 if(s.ribbon){P(c,['\\\\\\\\  //','(\\\\/ )'],cx-3,cy+ry,s.ribbon);c.put(cx-6,cy+ry+2,'~~~',s.ribbon);c.put(cx+4,cy+ry+2,'~~~',s.ribbon);}
 sparks(c,[[cx,cy-1],[cx-6,cy+2],[cx+7,cy-2]],f,'f');
 return {entry:{x:cx,y:H-1},contact:{x:cx,y:cy+ry},rim:{x:cx,y:cy-ry},emblem:{x:cx,y:cy},ribbon:{x:cx,y:cy+ry}};
}

// ------------------------------------------------------------------ costume tokens (an outfit on a hanger)
const COSTUMES={
 spring_duck_costume:{rows:['  .-.      .-. ',' / " \\.--./ " \\','|  *  (  )  *  |',' \\  \\ |  | /  / ','  \\__\\|  |/__/  ','   ( ~ ** ~ )    ','  (  *  ~  * )   ','  ( ~   *   ~ )  ',' (  *  ~~~  *  ) ','(~  ~ *  * ~  ~ )','`----------------\''],tone:'q',map:{'*':'y','~':'g','"':'f'},sub:'g',tag:'SPRING'},
 beach_duck_costume:{rows:['  _/\\_    _/\\_  ',' /  \\ \\--/ /  \\ ','|  o  \\    /  o  |',' \\__/|  /\\  |\\__/ ','     | (oo) |     ','     |  \\/  |     ','     | *  * |     ','     |  **  |     ','     | *  * |     ','     |______|     '],tone:'c',map:{o:'f','*':'e'},sub:'e',tag:'BEACH',lei:1},
 scarecrow_costume:{rows:['  ______________ ',' /  ,  ,  ,  ,  \\','|_,___,___,___,__|','  | []  ||  [] |  ','  |__/\\__||__/\\_|  ','  |   ||      |   ','  |  ,||,  [] |   ',' /|__/||\\__ __|\\  ','/,,,|  ||  |,,,\\\\ '],tone:'u',map:{',':'a','[':'y',']':'y'},sub:'a',tag:'HARVEST'},
 winter_coat_costume:{rows:['  ~~~~~~~~~~~~  ',' /@@@@@@@@@@@@\\ ','/@=|=====|=====\\','|@ |  o  |  o  |','|@ |  o  |  o  |','|@ |     |     |','|~~|  o  |  o  |','|  |_____|_____|','|  |/////|/////|'],tone:'r',map:{'@':'f','~':'f','=':'w',o:'y'},sub:'w',tag:'WINTER'},
};
function costume(c,W,H,s,f,t,id){
 const cx=W/2,tag=s.tag,w=Math.max(...s.rows.map(r=>r.length)),ox=Math.round(cx-w/2),oy=7;
 // hanger
 c.put(cx-1,0,'_o_','t');c.put(cx,1,'|','t');c.put(cx-5,2,'.-\'','t');c.put(cx+3,2,"'-.",'t');c.line(cx-8,4,cx+8,4,'_','t');
 P(c,s.rows,ox,oy-1,s.tone,s.map,true);
 if(s.lei){for(let i=0;i<8;i++)c.put(cx-6+i*1.6,oy+4+Math.abs(i-3.5)*.5,'o',['e','r','y','q'][i%4]);}
 if(id==='scarecrow_costume'){for(let i=0;i<4;i++){c.put(ox+1+i,oy+9,',','a');c.put(ox+w-5+i,oy+9,',','a');}c.put(cx-2,oy-3,'/\\\\/\\\\','a');}
 if(id==='spring_duck_costume'){c.put(cx+9,oy-1,'(@)','q');c.put(cx+10,oy,'*','y');}
 if(id==='winter_coat_costume'){c.put(cx-6,oy+10,'* * *','f');}
 const tx=cx-4;c.solid(tx,H-6,tag.length+2,3,'d');c.rect(tx-1,H-6,tag.length+4,3,s.sub,false);c.put(tx+1,H-5,tag,'f');
 sparks(c,[[2,6],[W-3,10]],f,s.sub);
 return {entry:{x:cx,y:H-1},contact:{x:cx,y:oy+3},hanger:{x:cx,y:1},body:{x:cx,y:oy+5},label:{x:cx,y:H-5}};
}
// ------------------------------------------------------------------ trophies
const TROPHIES={
 memory_trophy:{tone:'t',hi:'f',emb:'bulb',plate:'MEMORY',base:'z',handle:'ring'},
 splash_trophy:{tone:'u',hi:'w',emb:'splash',plate:'SPLASH',base:'b',handle:'wave'},
 golden_duck_trophy:{tone:'y',hi:'f',emb:'duck',plate:'1ST',base:'z',noCup:1},
 fish_trophy:{tone:'a',hi:'y',emb:'fish',plate:'FISH',base:'z',noCup:1},
 master_trophy:{tone:'y',hi:'f',emb:'star',plate:'MASTER',base:'z',handle:'ring',big:1},
 legendary_trophy:{tone:'y',hi:'f',emb:'gem',plate:'LEGEND',base:'k',handle:'fish',big:1,glow:1},
};
function trophy(c,W,H,s,f,t,id){
 const cx=W/2,baseY=H-9;
 // pedestal
 c.solid(cx-9,baseY+5,19,4,s.base);c.rect(cx-9,baseY+5,19,4,'a',false);c.solid(cx-6,baseY+3,13,2,s.base);c.line(cx-6,baseY+3,cx+6,baseY+3,'_','a');
 c.put(cx-Math.floor(s.plate.length/2),baseY+7,s.plate,'f');
 if(s.noCup){
  c.solid(cx-7,baseY,15,3,s.tone);c.line(cx-7,baseY,cx+7,baseY,'=',s.hi);
  if(s.emb==='duck'){
   P(c,['      .--.     ','     / o  >==  ','     \\_  _/    ','   .-\'  `-.   ',' .\'  ~~~~  \\ ','/  ~~~~~~~~  >','\\_          /  ','  `-._____.-\'  '],cx-7,baseY-8,s.tone,{o:'f','=':'e','>':'e','~':s.hi},true);
   sparks(c,[[cx-10,baseY-9],[cx+9,baseY-5],[cx+5,baseY-11]],f,'f');
  }else{
   c.solid(cx-9,baseY-12,19,12,'z');c.rect(cx-9,baseY-12,19,12,'a',false);
   const sf={...FISH.trout,tw:5,hh:3,th:3,dorsal:[.4,.58,1.5],anal:[.6,.72,1],sn:0};
   const sub=new ObjectCanvas(17,10);fish(sub,17,10,sf,f,f/3,'ft');blit(c,sub,cx-8,baseY-11);
   c.put(cx-9,baseY-13,'o','y');c.put(cx+9,baseY-13,'o','y');
  }
 }else{
  const w=s.big?19:17,bowl=s.big?12:10,top=baseY-bowl-4,x=Math.round(cx-w/2),hw=(w-1)/2;
  for(let r=0;r<bowl;r++){
   const ind=Math.floor(r*r/(bowl*1.6)),ww=w-ind*2,y=top+r;
   c.solid(x+ind,y,ww,1,s.tone);
   if(r===0){c.put(x,y,'.'+'-'.repeat(w-2)+'.',s.hi);}
   else if(r<bowl-1){c.put(x+ind,y,r<bowl*.4?'|':'\\',s.tone);c.put(x+ind+ww-1,y,r<bowl*.4?'|':'/',s.tone);}
   else c.put(x+ind,y,"'"+'-'.repeat(ww-2)+"'",s.tone);
  }
  c.put(x+2,top+2,'|',s.hi);c.put(x+2,top+3,'|',s.hi);
  const sy=top+bowl;c.solid(cx-1,sy,3,3,s.tone);c.put(cx-1,sy,'| |',s.tone);c.put(cx-1,sy+1,'(_)','a');c.put(cx-1,sy+2,'| |',s.tone);c.put(cx-4,sy+3,'_/___\\_',s.tone);
  const hy=top+1;
  if(s.handle==='ring'){c.ellipse(x-1,hy+2,2.5,2.2,'o',s.tone,false);c.ellipse(x+w,hy+2,2.5,2.2,'o',s.tone,false);}
  else if(s.handle==='wave'){c.put(x-3,hy,'~(',s.hi);c.put(x+w+1,hy,')~',s.hi);c.put(x-3,hy+2,'~(',s.hi);c.put(x+w+1,hy+2,')~',s.hi);}
  else{c.put(x-3,hy,'<>',s.hi);c.put(x+w+1,hy,'><',s.hi);c.put(x-2,hy+1,'(',s.tone);c.put(x+w,hy+1,')',s.tone);}
  const bw=hw,ey=top+2;
  if(s.emb==='bulb'){P(c,[' .-. ','( o )',"'-u-'"],cx-2,ey,'y',{o:'f'});c.put(cx-3,ey+1,'\\\\','y');c.put(cx+3,ey+1,'/','y');}
  else if(s.emb==='splash'){P(c,['\\\\ | /','- (~) -','~ ~~~ ~'],cx-3,ey,'w');c.put(cx-6,top-2,'o','w');c.put(cx+5,top-3,'o','c');c.put(cx,top-2-(f%3),'*','f');c.put(cx-3,top-1,'~ ~',s.hi);}
  else if(s.emb==='star'){P(c,['  /\\  ','<-**->','  \\/  '].map(r=>r),cx-3,ey,'r',{'*':'y'});}
  else {P(c,['  /\\  ',' /<>\\ ',' \\<>/ ','  \\/  '],cx-3,ey-1,'w',{'<':'f','>':'f'});}
  if(s.big)c.put(cx-2,top-1,'* * *','y');
  sparks(c,[[2,top],[W-3,top+6],[cx+4,Math.max(0,top-3)]],f,s.hi);
  if(s.glow)for(let i=0;i<8;i++){const a=i/8*TAU+f*.5;dot(c,cx+Math.cos(a)*12.5,top+7+Math.sin(a)*8/1.5,'.','w');}
 }
 return {entry:{x:cx,y:H-1},contact:{x:cx,y:baseY},cup:{x:cx,y:baseY-8},plate:{x:cx,y:baseY+7},handle:{x:cx-12,y:baseY-12},emblem:{x:cx,y:baseY-12}};
}
// ------------------------------------------------------------------ acorns and cones
const ACORNS={acorn:{nut:'z',lit:'a',cap:'b',capHi:'n',stem:'z'},magic_acorn:{nut:'v',lit:'l',cap:'u',capHi:'w',stem:'c',glow:1},golden_acorn:{nut:'y',lit:'f',cap:'a',capHi:'y',stem:'a',gold:1}};
function acorn(c,W,H,s,f,t,id){
 const cx=W/2,oy=2;
 const hw=[4,5,5,5,5,4,3,1];
 hw.forEach((h,i)=>{const y=oy+5+i;c.solid(cx-h,y,h*2+1,1,s.nut);c.put(cx-h,y,i<5?'(':i<7?'\\':'\\',s.nut);c.put(cx+h,y,i<5?')':'/',s.nut);if(i===7)c.put(cx,y,'v',s.nut);});
 P(c,['    \\|     ','  .-----.  ',' (#+#+#+#) ','  \\#+#+#/  '],Math.round(cx-5.5),oy-1,s.cap,{'#':s.capHi,'+':s.capHi},true);
 c.put(cx-3,oy+7,'\\',s.nut==='z'?'a':'f');c.put(cx-3,oy+8,'|',s.lit);c.put(cx-2,oy+10,'.',s.lit);c.put(cx+2,oy+9,'.',s.lit);
 glint(c,cx+4,oy+6,f,'f');
 if(s.glow){for(let i=0;i<6;i++){const a=i/6*TAU+f*.7;c.put(cx+Math.cos(a)*7,6+Math.sin(a)*5,'*.'[i%2],'c');}c.put(cx,oy+8,'*','f');}
 if(s.gold)sparks(c,[[1,3],[W-2,8],[cx+3,5]],f,'f');
 return {entry:{x:cx,y:H-1},contact:{x:cx,y:oy+6},cap:{x:cx,y:oy+1},nut:{x:cx,y:oy+8},stem:{x:cx,y:oy-1}};
}
function cone(c,W,H,s,f,t){
 const cx=W/2;
 for(let r=0;r<14;r++){
  const y=4+r,hw=Math.round(1.5+Math.sin(Math.PI*Math.min(1,(r+1.8)/15.5))*5.6);
  c.solid(cx-hw,y,hw*2+1,1,r%2?'z':'b');
  for(let k=-hw;k<=hw-1;k+=2){const px=cx+k+(r%2);c.put(px,y,'<>',(r+k)%3?'b':'n');}
  c.put(cx-hw,y,'(',r%2?'z':'b');c.put(cx+hw,y,')',r%2?'z':'b');
 }
 c.put(cx-1,18,"\\|/",'z');c.put(cx,19,'v','z');
 c.put(cx,3,'|','z');c.put(cx-4,2,'\\|/ /','h');c.put(cx+1,2,'\\ |/','m');c.put(cx-6,1,'/ / /','h');c.put(cx+3,1,'\\ \\','m');
 if(f%4===0)c.put(cx+7,6,'*','f');
 return {entry:{x:cx,y:H-1},contact:{x:cx,y:11},stem:{x:cx,y:3},scales:{x:cx,y:9}};
}

// ------------------------------------------------------------------ bottles and jars
const BOTTLES={
 glass_bottle:{shape:'wine',glass:'h',liquid:null,cork:'z',content:'scroll',label:null,algae:1,wax:'r'},
 message_bottle:{shape:'wine',glass:'c',liquid:null,cork:'a',content:'scroll',ribbon:'q',sand:1},
 medicine:{shape:'flask',glass:'z',liquid:'g',cork:'b',content:'bubbles',label:'+'},
 fog_essence:{shape:'vial',glass:'i',liquid:null,cork:'k',content:'fog'},
 rare_bug_jar:{shape:'jar',glass:'c',liquid:null,cork:'a',content:'bug'},
};
function bottle(c,W,H,s,f,t,id){
 const cx=W/2;let outline=[],y0=0,neckTop;
 if(s.shape==='jar'){y0=6;for(let r=0;r<17;r++)outline.push([r<1||r>15?5:7]);}
 else if(s.shape==='flask'){y0=3;[2,2,2,3,4,5,6,7,7,7,7,7,6,6,6,5].forEach(h=>outline.push([h]));}
 else if(s.shape==='vial'){y0=6;[2,2,2,3,4,5,5,6,6,6,6,6,6,6,6,5,4].forEach(h=>outline.push([h]));}
 else{y0=3;[1,1,1,1,2,2,3,4,5,5,5,5,5,5,5,5,5,5,5,5,5,4].forEach(h=>outline.push([h]));}
 // glass body
 outline.forEach(([h],r)=>{
  const y=y0+r,last=r===outline.length-1;
  c.solid(cx-h,y,h*2+1,1,s.glass);
  c.put(cx-h,y,last?'`':'(',s.glass==='z'?'a':'f');c.put(cx+h,y,last?"'":')',s.glass==='z'?'a':'f');
  if(last)c.line(cx-h+1,y,cx+h-1,y,'_','f');
 });
 const bodyTop=s.shape==='jar'?y0+1:y0+outline.findIndex(([h])=>h>=4);
 const bodyH=y0+outline.length-1-bodyTop;
 // liquid / sand
 if(s.liquid){for(let y=bodyTop+3;y<y0+outline.length-1;y++){const h=outline[y-y0][0]-1;c.solid(cx-h,y,h*2+1,1,s.liquid);if((y+f)%3===0)c.put(cx-h+1,y,'~',s.liquid);}}
 if(s.sand)for(let y=y0+outline.length-4;y<y0+outline.length-1;y++){const h=outline[y-y0][0]-1;c.solid(cx-h,y,h*2+1,1,'n');c.put(cx-h+1,y,'.:.:.:.:.:'.slice(0,h*2-1),'a');}
 // rim, cork, neck
 if(s.shape==='jar'){c.solid(cx-6,y0-3,13,3,'t');c.rect(cx-6,y0-3,13,3,'s',false);c.put(cx-4,y0-2,'=======','f');c.put(cx-6,y0+3,'|','f');}
 else{c.solid(cx-2,y0-1,5,1,s.cork);c.solid(cx-2,y0-2,5,1,s.cork);c.put(cx-2,y0-2,'#####','a');c.put(cx-1,y0-1,'\\\\_/',s.cork);}
 // contents
 if(s.content==='scroll'){
  const sy=bodyTop+(s.shape==='wine'?1:2);P(c,['.-------.','|  ~ ~  |','| ~~ ~~ |','`-------\''],cx-4,sy+2,'p',{'~':'k'},true);
  if(s.ribbon)c.put(cx-4,sy+3,'===o===','q');
  if(s.algae){c.put(cx-4,sy,'~\\\\','h');c.put(cx+3,sy+7,'/~','h');c.put(cx-4,sy+9,'"','m');}
  if(s.wax)c.put(cx-1,y0-1,'(@)',s.wax);
  c.put(cx-4,y0+16,f%2?'~ ~ ~':' ~ ~ ',s.sand?'w':'f');glint(c,cx+4,y0+8,f,'f');
 }else if(s.content==='bubbles'){
  for(let i=0;i<5;i++){const h=hash('bb',i),x=cx-4+h%8,y=y0+outline.length-3-((h>>>3)+f*(1+i%2))%9;c.put(x,y,'o.'[i%2],'g');}
  P(c,['.---.','| + |',"'---'"],cx-2,y0+9,'p',{'+':'r'},true);c.put(cx-3,y0-3,'*','g');
 }else if(s.content==='fog'){
  for(let r=0;r<7;r++){const x=cx-4+((r*3+f)%3)+Math.sin(r+f*.9)*1.6,y=y0+6+r*1.6;c.put(x,y,r%2?'~~~~~~':'~~~~~','f');c.put(x+1,y+.5,'.:.','i');}
  c.put(cx-2,y0-4,'. ~ .','i');c.put(cx+1,y0-5,'~','i');
  sparks(c,[[cx-6,y0+5],[cx+5,y0+12]],f,'f');
 }else if(s.content==='bug'){
  const bx=cx-2+Math.round(Math.sin(t*1.7)*2),by=y0+9;P(c,['\\\\o/','(##)',"/'\\\\"],bx-1,by,'r',{'#':'d',o:'f'});c.put(bx-1,by+1,'(','r');c.put(bx+2,by+1,')','r');
  c.put(cx-3,y0+14,'/\\\\','h');c.put(cx+2,y0+13,'\\\\/','h');c.put(cx-5,y0+3,'.','f');c.put(cx+3,y0+5,'.','f');
  c.put(cx-4,y0-1,'+','y');
 }
 if(s.label==='+'){P(c,['.---.','| + |',"'---'"],cx-2,y0+8,'p',{'+':'r'},true);}
 // glint
 c.put(cx-s.glassGlint||cx-4,y0+6,'|','f');c.put(cx-4,y0+7,'|','f');
 return {entry:{x:cx,y:H-1},contact:{x:cx,y:y0+10},cork:{x:cx,y:Math.max(0,y0-2)},body:{x:cx,y:y0+10},label:{x:cx,y:y0+9}};
}
// ------------------------------------------------------------------ eggs
SHAPES.egg=R=>(X,Y)=>{const y=-Y/R,k=y>0?1-.14*y:1;return (X/(R*.75*k))**2+y*y<=1;};
const EGGS={
 mystery_egg:{tone:'f',spot:'k',rune:'?',hue:'y'},
 mystic_egg:{tone:'v',spot:'l',rune:'*',hue:'c',glow:1},
};
function egg(c,W,H,s,f,t,id){
 const cx=W/2,cy=H/2-.5,R=12.5;
 blob(c,'egg',cx,cy,R,s.tone,s.tone);blob(c,'egg',cx,cy,R*.88,s.tone,id==='mystic_egg'?'d':'n');
 for(let i=0;i<60;i++){const h=hash(id,i),x=cx-8+h%17,y=cy-8+(h>>>5)%17;if(SHAPES.egg(R*.82)(x-cx,(y-cy)*1.5))c.put(x,y,id==='mystery_egg'?'o.:'[h%3]:'.+'[h%2],s.spot);}
 if(id==='mystery_egg'){c.put(cx-1,cy-1,'(?)','y');c.put(cx-4,cy+3,'.o.','b');c.put(cx+3,cy-4,'o','b');}
 else{
  const rn=['/\\\\','|-','<>','~~','^v','+|'];for(let i=0;i<6;i++){const a=i/6*TAU+.3;c.put(cx+Math.cos(a)*6.2-1,cy+Math.sin(a)*4.1,rn[i],(i+f)%3===0?'f':'c');}
  c.put(cx-1,cy,f%2?'(*)':'(+)','f');for(let i=0;i<8;i++){const a=i/8*TAU+f*.4;c.put(cx+Math.cos(a)*(R*.9),cy+Math.sin(a)*(R*.62),'.','c');}
 }
 c.put(cx-5,cy-6,'\\\\','f');c.put(cx-6,cy-4,'|','f');
 sparks(c,[[2,3],[W-3,6],[cx+4,0]],f,s.hue);
 return {entry:{x:cx,y:H-1},contact:{x:cx,y:cy},shell:{x:cx,y:cy-4},emblem:{x:cx,y:cy}};
}
// ------------------------------------------------------------------ tools
function toolHammer(c,W,H,f){
 c.line(5,H-3,W-10,8,null,'z');c.line(6,H-3,W-9,8,null,'b');c.line(4,H-3,W-11,8,null,'a');
 for(let i=0;i<3;i++)c.put(4+i,H-3+0,'=','z');c.put(2,H-2,'(_)','z');
 const x=W-17,y=3;c.solid(x,y,15,6,'s');c.rect(x,y,15,6,'t',false);
 for(const [dx,dy] of [[3,2],[7,3],[11,2],[5,4],[9,4]])c.put(x+dx,y+dy,'.:'[(dx+dy)%2],'k');c.put(x+2,y+1,'/','f');c.put(x+13,y+3,'|','k');
 P(c,['#####','#####'],W-13,y+2,'z',{},false);c.put(W-14,y+3,'~~','a');c.put(W-10,y+3,'~~','a');
 c.put(W-6,y+1,'+','f');if(f%3===0)c.put(2,2,'*','f');
 return {entry:{x:5,y:H-1},contact:{x:W-9,y:8},handle:{x:8,y:H-5},head:{x:W-10,y:y+3},wrap:{x:W-10,y:y+3}};
}
function toolRod(c,W,H,s,f,t){
 const g=s.master,tip=[W-6,3],base=[5,H-5];
 c.line(base[0],base[1],tip[0],tip[1],null,g?'k':'z');c.line(base[0],base[1]-1,tip[0],tip[1]-1,null,g?'s':'b');
 for(let i=0;i<6;i++)c.put(base[0]+i*2,base[1]-i*1.1,'#',g?'y':'a');
 c.rect(1,H-5,6,3,g?'y':'a',true);c.put(2,H-4,'(@)',g?'f':'t');
 for(let i=1;i<=5;i++){const p=i/6;c.put(base[0]+(tip[0]-base[0])*(.3+p*.7)-1,base[1]+(tip[1]-base[1])*(.3+p*.7)-2,'o',g?'y':'t');}
 if(g)for(let i=0;i<5;i++)c.put(base[0]+6+i*8,base[1]-5-i*5,'=',i%2?'f':'y');
 const sway=Math.round(Math.sin(t*2)*1);
 const lx=tip[0]+sway,ly=tip[1];c.line(tip[0],tip[1],lx,ly+16,'|','f');
 c.put(lx-1,ly+16,'(O)',g?'y':'r');c.put(lx,ly+17,'|','f');c.put(lx-1,ly+19,'J','t');
 c.put(lx-6,H-1,'~ ~ ~ ~','w');c.put(lx-8,H-3,'. ~ . ~','c');
 if(g){c.put(2,H-8,'<>','r');sparks(c,[[W-4,1],[lx+3,ly+14],[12,H-10]],f,'f');c.put(base[0]+14,base[1]-14,'<>','y');}
 return {entry:{x:6,y:H-1},contact:{x:8,y:H-6},handle:{x:6,y:H-5},tip:{x:tip[0],y:tip[1]},line:{x:lx,y:ly+10},bobber:{x:lx,y:ly+16}};
}
function toolWand(c,W,H,s,f,t){
 c.line(3,H-2,W-9,9,null,'z');c.line(4,H-2,W-8,9,null,'b');
 for(let i=0;i<9;i++){c.put(5+i*2.1,H-4-i*1.3,i%2?'~':'S',i%2?'a':'z');}
 c.put(W-12,10,'/','z');c.put(W-13,12,'o','h');c.put(8,H-6,'o','h');
 const tx=W-9,ty=8;c.put(tx-2,ty-3,'\\\\ | /','y');c.put(tx-3,ty-2,'--(*)--',f%2?'f':'y');c.put(tx-2,ty-1,'/ | \\\\','y');
 for(let i=0;i<7;i++){const a=i/7*TAU+f*.8;dot(c,tx+Math.cos(a)*7,ty-2+Math.sin(a)*4,'.*+'[i%3],['v','l','c','y'][i%4]);}
 return {entry:{x:5,y:H-1},contact:{x:12,y:H-6},handle:{x:5,y:H-3},tip:{x:tx,y:ty},star:{x:tx,y:ty-2}};
}
function toolKey(c,W,H,s,f,t){
 const bx=7,by=8;
 c.ellipse(bx,by-2.5,3,2.5,'o','y',false);c.ellipse(bx+3,by+1,3,2.5,'o','y',false);c.ellipse(bx-3,by+1,3,2.5,'o','y',false);
 c.solid(bx-2,by-2,5,5,'y');c.put(bx-1,by,'(*)','r');c.put(bx-1,by+3,'`|\'','a');
 c.solid(bx+2,by,W-bx-4,2,'y');c.line(bx+2,by,W-3,by,'=','a');c.line(bx+2,by+1,W-3,by+1,'-','y');
 for(const [x,h] of [[W-4,3],[W-7,2],[W-10,3],[W-13,1]]){c.solid(x,by+2,2,h,'y');c.put(x,by+2,'||','a');}
 c.put(bx+5,by+2,'o','a');c.put(bx+8,by+2,'o','a');
 sparks(c,[[bx-5,by-5],[W-4,by-3],[bx+10,by+6]],f,'f');
 return {entry:{x:bx,y:H-1},contact:{x:bx,y:by},bow:{x:bx,y:by},shaft:{x:W/2,y:by},teeth:{x:W-8,y:by+3}};
}
const TOOLS={stone_hammer:{k:'hammer'},fishing_rod:{k:'rod'},master_fishing_rod:{k:'rod',master:1},magic_wand:{k:'wand'},treasure_key:{k:'key'}};
function tool(c,W,H,s,f,t,id){
 return s.k==='hammer'?toolHammer(c,W,H,f):s.k==='rod'?toolRod(c,W,H,s,f,t):s.k==='wand'?toolWand(c,W,H,s,f,t):toolKey(c,W,H,s,f,t);
}
// ------------------------------------------------------------------ blocks and fibre
const BLOCKS={
 clay_brick:{front:'o',top:'a',edge:'r',dots:'z',holes:1},
 stone_block:{front:'s',top:'t',edge:'k',dots:'k',moss:1},
};
function block(c,W,H,s,f,t,id){
 const x=3,y=Math.round(H*.32),w=W-10,h=H-y-3,d=Math.round(h*.45);
 // top face (parallelogram), front face, right face
 for(let i=0;i<d;i++){c.solid(x+d*1.2-i*1.2,y+i,w,1,s.top);c.put(x+d*1.2-i*1.2,y+i,'/',s.edge);c.put(x+d*1.2-i*1.2+w-1,y+i,'/',s.edge);}
 c.line(x+d*1.2-d*1.2,y+d,x+w-1,y+d,'_',s.edge);
 c.solid(x,y+d,w,h-d+1,s.front);c.rect(x,y+d,w,h-d+1,s.edge,false);
 for(let i=0;i<d+1;i++){c.solid(x+w+i*1.2-1,y+d-i,2,h-d+1,s.edge);c.put(x+w+i*1.2-1,y+d-i,'/',s.edge);}
 c.put(x+w-1,y+h,'.','k');
 for(let i=0;i<24;i++){const hh=hash(id,i);c.put(x+2+hh%(w-4),y+d+1+(hh>>>5)%(h-d-1),'.:,'[hh%3],s.dots);}
 if(s.holes){for(let i=0;i<3;i++)c.put(x+4+i*(w/3.2),y+d+(h-d)/2,'(__)','z');c.put(x+2,y+d+1,'/','f');}
 if(s.moss){c.put(x+3,y+h-1,'"%"','h');c.put(x+w-8,y+d+1,'"~"','m');c.line(x+w*.55,y+d+1,x+w*.62,y+h-1,'/','k');c.put(x+3,y+d+2,'/','f');c.put(x+8,y+d+3,'x','k');}
 for(let i=0;i<d;i++)c.put(x+d*1.2-i*1.2+(w>>1),y+i,(i+hash(id)%3)%2?'.':',','f');
 glint(c,x+3,y+d-1,f,'f');glint(c,x+w-3,y+h-2,f,'f',2);
 return {entry:{x:W/2,y:H-1},contact:{x:x+w/2,y:y+d+(h-d)/2},top:{x:x+w/2+d*.6,y:y+d/2},front:{x:x+w/2,y:y+d+(h-d)/2}};
}
function fiber(c,W,H,s,f,t,id){
 const cx=W/2,cy=H/2;
 if(id==='rope'){
  for(let r=0;r<3;r++){const rx=11-r*3.4,ry=7-r*2.2;for(let i=0;i<(34-r*8);i++){const a=i/(34-r*8)*TAU;c.put(cx+Math.cos(a)*rx,cy+Math.sin(a)*ry*.9+ (3-r)*.5,i%2?'/':'\\\\',r%2?'z':'n');}}
  c.solid(cx-3,cy-1,7,3,'z');c.put(cx-3,cy,'(  (  )',  'b');
  c.put(cx+10,cy+4,'\\\\_',"n");c.line(cx+10,cy+5,W-2-(f%3),H-3,null,'n');c.put(W-4-(f%3),H-3,'~;;,','n');c.put(W-3,H-2,f%2?"'`":'.,','b');
  c.put(cx-12,cy-6,'=','a');c.put(cx-3,cy-8,'$','a');
  P(c,["'\\\\|/'"],cx-2,2,'n');
 }else{
  c.ellipse(cx,cy,8,6.4,'o','p',true);
  for(let i=-8;i<=8;i+=2){c.line(cx+i,cy-5,cx+i*1.1,cy+5,i%4?'/':'\\\\',i%3?'f':'p');}
  for(let i=-5;i<=5;i+=2)c.put(cx-6,cy+i*.8,i%4?'~~~~~~~~~~':'~-~-~-~-~-',i%3?'f':'p');
  c.put(cx+7,cy+4,'S','f');c.line(cx+7,cy+5,W-2-(f%3),H-3,'~','f');c.put(W-5-(f%3),H-3,'~o','p');c.put(cx-3,2,'|','p');c.put(cx-2,1,'.','f');
 }
 return {entry:{x:cx,y:H-1},contact:{x:cx,y:cy},coil:{x:cx,y:cy},end:{x:W-3,y:H-3}};
}
// ------------------------------------------------------------------ essences and wisps
function essence(c,W,H,s,f,t,id){
 const cx=W/2,cy=H/2;
 if(id==='dandelion_fluff'){
  c.line(cx-4,H-1,cx-1,cy+2,'|','h');c.put(cx-3,H-3,'\\\\','m');c.put(cx-6,H-2,'/_','h');
  for(let i=0;i<22;i++){const a=i/22*TAU,r=6.5;const x=cx+Math.cos(a)*r*1.4,y=cy-1+Math.sin(a)*r*.8;c.line(cx,cy-1,x,y,i%2?'/':'\\\\','f');c.put(x,y,'*','f');}
  c.put(cx-1,cy-1,'(@)','y');
  for(let i=0;i<4;i++){const h=hash('fl',i),x=1+(h+f*2)%(W-2),y=((h>>>4)%8+f)%H;c.put(x,Math.min(H-2,y),'*\'.'[i%3],'f');}
 }else if(id==='fairy_dust'){
  P(c,['  .---.  ',' /  _  \\ ','(  (_)  )',' \\_____/ ',' {_____} '],cx-4,H-6,'l',{'_':'v'},true);c.put(cx-3,H-8,'\\\\~~/','y');
  const tn=['q','l','w','y','c'];for(let i=0;i<30;i++){const h=hash('fd',i),a=(h%628)/100,r=(h>>>5)%9,x=cx+Math.cos(a)*r*1.4+(f%2),y=cy-3-Math.abs(Math.sin(a))*r*.7+(i%4);dot(c,x,y,'.*+'[(h+f)%3],tn[(h+f)%5]);}
 }else if(id==='frozen_dewdrop'){
  c.line(1,H-2,W-2,H-6,'_','h');c.line(2,H-3,W-3,H-7,'-','m');
  c.ellipse(cx,cy,3.6,3.6,'-','i',true);c.put(cx-2,cy-3,'/\\\\','f');c.put(cx-3,cy-1,'( .\\\\','f');c.put(cx+1,cy,'+','w');c.put(cx-1,cy+2,'`-\'','w');c.put(cx,cy-5,'^','i');
  for(let i=0;i<6;i++){const a=i/6*TAU;c.put(cx+Math.cos(a)*7,cy+Math.sin(a)*4.6,'*+'[i%2],'f');}
  glint(c,cx+4,cy-4,f,'f');
 }else if(id==='warmth'){
  circ(c,cx,cy+1,5,'-','e',true);c.put(cx-2,cy-3,'.-"-.','a');
  const fl=[[' ) ','(  )','( ^ )'],[' ( ','(  )',') ^ ('],[' ) ','(^ )','( ^ )']][f%3];P(c,fl,cx-2,cy-1,'y',{},false);c.put(cx-1,cy+2,'<3','r');
  for(let i=0;i<3;i++)c.put(cx-3+i*3,((f+i*2)%5)+0,'~','o');
  c.put(2,cy+4,'.','y');c.put(W-3,cy,'.','y');c.put(cx-6,H-2,'_____','z');
 }else{
  circ(c,cx,cy,6.5,'-','l',true);c.put(cx-6,cy-4,'\\\\','f');c.put(cx-7,cy-3,'.','f');
  PC(c,[' _____',' |   |',' |  )',' o_|  ','  (_)'].slice(0,0).length?[]:[],cx,cy,'f');
  P(c,['  ,---.',' /|  _|','| | (_|','o_|  o '],cx-3,cy-3,'f',{},false);
  for(let k=0;k<3;k++){const p=(f+k)%3;dot(c,cx+7+k*2,cy-1,')',p===0?'f':'l');dot(c,cx-8-k*2,cy-1,'(',p===0?'f':'l');}
  c.put(cx+8,cy-5,'?','y');c.put(cx-9,cy+4,'?','y');sparks(c,[[2,2],[W-3,H-3]],f,'f');
 }
 return {entry:{x:cx,y:H-1},contact:{x:cx,y:cy},core:{x:cx,y:cy},wisp:{x:cx,y:Math.max(0,cy-5)}};
}

// ------------------------------------------------------------------ singular props
const PROPS={};
PROPS.gathering_bag=(c,W,H,f)=>{
 const cx=W/2;
 c.ellipse(cx,17,11,7.5,'-','n',true);c.solid(cx-9,11,19,10,'n');
 for(let y=10;y<24;y++){const hw=Math.round(11*Math.sqrt(Math.max(0,1-((y-17)/7.6)**2)));c.put(cx-hw,y,y<17?'(':'\\\\','z');c.put(cx+hw,y,y<17?')':'/','z');}
 c.line(cx-8,24,cx+8,24,'_','z');
 // gathered neck with drawstring
 c.solid(cx-6,8,13,3,'z');c.put(cx-7,8,'\\\\_/\\\\_/\\\\_/\\\\_/','a');c.put(cx-6,10,'=o=======o=','y');c.put(cx-8,11,'~~','y');c.put(cx+7,11,'~~','y');
 // peeking materials
 c.put(cx-5,4,'\\\\|/ ','h');c.put(cx-4,5,'(o)','z');c.put(cx+1,5,'/ \\\\','b');c.put(cx+3,3,'|','b');c.put(cx+1,4,"'/\\\\'",'g');
 c.put(cx-5,2,'/_','h');
 // patch, stitches, strap
 P(c,['.---.','|+ +|',"'---'"],cx-8,15,'a',{'+':'y'},true);c.put(cx+3,18,'- - -','z');c.put(cx+2,14,'/','f');
 c.line(cx+9,10,cx+13,3,null,'z');c.put(cx+12,2,'(_)','z');
 if(f%4<2)c.put(cx+8,16,'*','f');
 return {entry:{x:cx,y:H-1},contact:{x:cx,y:15},mouth:{x:cx,y:7},strap:{x:cx+12,y:3},patch:{x:cx-6,y:16}};
};
PROPS.watchtower=(c,W,H,f,t)=>{
 const cx=W/2,floor=H-6;
 // stone footing
 for(let i=0;i<2;i++)c.solid(cx-18+i*0,floor+i*2,37,2,i?'k':'s');c.rect(cx-18,floor,37,5,'t',false);for(let x=cx-16;x<cx+16;x+=5)c.put(x,floor+2,'[__]','s');
 // legs and bracing (four posts, front pair with X braces)
 const top=38,L=cx-13,R=cx+13;
 for(const [x,tn] of [[L,'z'],[L+2,'b'],[R-2,'b'],[R,'z']])c.line(x,top,x+(x<cx?-3:3)*0,floor-1,'|',tn);
 for(const y0 of [top+2,top+13,top+24]){const y1=y0+11;c.line(L,y0,R,y1,'\\\\','b');c.line(R,y0,L,y1,'/','b');c.line(L,y1,R,y1,'=','z');}
 // ladder at right side
 c.line(R+4,top+4,R+4,floor-1,'|','a');c.line(R+8,top+4,R+8,floor-1,'|','a');for(let y=top+6;y<floor-1;y+=3)c.put(R+5,y,'---','a');
 // platform + cabin
 c.solid(L-3,top-1,R-L+7,3,'z');c.rect(L-3,top-1,R-L+7,3,'a',false);
 c.solid(L-2,top-15,R-L+5,14,'b');c.rect(L-2,top-15,R-L+5,14,'a',false);
 for(let x=L-1;x<R+2;x+=3)c.line(x,top-14,x,top-2,'|','z');
 const lit=(Math.floor(t*1.2)%2===0);P(c,['.------.','|      |','|  /\\  |',"'------'"],cx-4,top-12,'y',{},false);c.solid(cx-3,top-11,7,3,lit?'y':'e');
 c.put(cx-2,top-10,lit?'(##)':' () ','f');
 // railings
 c.line(L-3,top-4,L-3,top-1,'|','a');c.line(R+3,top-4,R+3,top-1,'|','a');
 // roof
 for(let i=0;i<12;i++){const y=top-16-i,hw=Math.round(18-i*1.4);c.solid(cx-hw,y,hw*2+1,1,i%2?'r':'o');c.put(cx-hw,y,'/','a');c.put(cx+hw,y,'\\\\','a');if(i%3===0)c.put(cx-hw+2,y,'=-=-=-=-=-=-=-=-=-=-='.slice(0,Math.max(0,hw*2-3)),'a');}
 c.line(cx,top-28,cx,top-34,'|','f');
 // flag
 const fw=[0,1,2,1][f%4];for(let i=0;i<9;i++){const y=top-34+(i<5?i:9-i)*0;c.put(cx+1,top-34+Math.floor(i/3),'~'.repeat(4+ (i%3)+fw),'r');}
 c.put(cx-1,top-35,'*','y');
 // spyglass peeking
 c.put(cx+14,top-8,'==o','t');c.put(cx-17,top-10,'o','y');
 for(const [x,y] of [[8,8],[W-8,12],[10,floor-8]])glint(c,x,y,f,'f',x);
 return {entry:{x:cx,y:H-1},contact:{x:cx,y:floor},ladder:{x:R+6,y:floor-4},window:{x:cx,y:top-9},flag:{x:cx+4,y:top-34},platform:{x:cx,y:top}};
};
PROPS.butterfly_wing=(c,W,H,f,t)=>{
 const cx=W/2-2,cy=H/2,flap=Math.sin(t*3)*.12,tn=['q','l','w','v'];
 const inside=(X,Y)=>{const a=Math.atan2(Y,X);const r=Math.hypot(X,Y);return X>-14&&r<(16+3*Math.cos(a*2+.4)+flap*8)&&Y<7&&Y>-17;};
 blob(c,'round',cx,cy,1,'q',null,false);
 for(let y=1;y<H-1;y++)for(let x=1;x<W-1;x++){
  const X=x-(cx-6),Y=(y-cy)*1.5; const u=X/13,v=Y/14;
  const ins=(u*u*.9+(v+.1)**2*1.1<1)&&X>-3;
  if(!ins)continue;
  const edge=!(((X+1)/13)**2*.9+(v+.1)**2*1.1<1)||!(((X-1)/13)**2*.9+(v+.1)**2*1.1<1)||!((u*u*.9+((Y+1.5)/14+.1)**2*1.1)<1)||!((u*u*.9+((Y-1.5)/14+.1)**2*1.1)<1);
  const tone=tn[(Math.floor(Math.hypot(X,Y)/3.5)+f)%4];
  c.solid(x,y,1,1,u<.15?'v':'l');c.put(x,y,edge?'o':((x+y)%2?'.':' '),edge?'d':tone);
  if(edge)c.put(x,y,'o','q');
 }
 for(let i=0;i<6;i++){const a=-.9+i*.38;c.line(cx-6,cy,cx-6+Math.cos(a)*13,cy+Math.sin(a)*8,null,'f');}
 P(c,['.-.','(@)',"'-'"],cx+1,cy-5,'y',{'@':'r'},false);P(c,['.-.','(o)',"'-'"],cx+3,cy+2,'w',{o:'v'},false);
 c.put(cx-9,cy-1,'||','z');c.put(cx-10,cy,'(','z');
 sparks(c,[[2,3],[W-3,5],[W-5,H-3]],f,'f');
 return {entry:{x:cx-6,y:H-1},contact:{x:cx-6,y:cy},base:{x:cx-9,y:cy},eyespot:{x:cx+2,y:cy-4},tip:{x:cx+8,y:cy-8}};
};
PROPS.mud_sculpture=(c,W,H,f)=>{
 const cx=W/2;
 c.solid(cx-11,H-4,23,3,'n');c.rect(cx-11,H-4,23,3,'a',false);c.put(cx-3,H-3,'~ MUD ~','z');
 c.ellipse(cx,H-8,8,4,'-','z',true);c.solid(cx-6,H-10,13,5,'z');
 P(c,['  .--.  ',' ( o  \\==',' (_   _/ ','  \\__/  '],cx-1,H-15,'z',{o:'f','=':'a'},true);
 for(const [dx,dy] of [[-6,-7],[-3,-6],[1,-6],[4,-7],[-5,-9],[2,-9]])c.put(cx+dx,H+dy,'~','b');
 for(let i=0;i<5;i++)c.put(cx-5+i*2,H-7+(i%2),'.:'[i%2],'a');
 c.put(cx+3,H-14,'/\\\\','z');c.put(cx+8,H-8,'(@)','b');c.put(cx-9,H-9,'x','h');
 c.line(cx+8,H-5,cx+10,H-14,null,'a');c.put(cx+10,H-15,'*','y');
 for(let i=0;i<4;i++){const h=hash('mf',i),a=f*.7+i*1.6;c.put(cx+Math.cos(a)*9,4+Math.sin(a)*2+i%2,'.','s');}
 sparks(c,[[2,5]],f,'f');
 return {entry:{x:cx,y:H-1},contact:{x:cx,y:H-9},board:{x:cx,y:H-3},head:{x:cx+3,y:H-14},hand:{x:cx+8,y:H-8}};
};
PROPS.mystery_gift=(c,W,H,f,t)=>{
 const cx=W/2,y0=8;
 c.solid(2,y0,20,12,'r');c.rect(2,y0,20,12,'y',false);
 for(let i=0;i<14;i++){const h=hash('gf',i);c.put(3+h%18,y0+1+(h>>>4)%10,'*.o'[h%3],['y','w','f','g'][h%4]);}
 c.solid(cx-1,y0,3,12,'y');c.put(cx-1,y0+3,'|||','a');c.line(2,y0+5,21,y0+5,'=','y');
 c.solid(1,y0-3,22,3,'r');c.rect(1,y0-3,22,4,'y',false);c.solid(cx-1,y0-3,3,3,'y');
 const wob=f%2;P(c,['  _____  ','/  _ _  \\','\\ ( \\ ) /','  `-v-\'  '].map(r=>r),cx-4-wob*0,y0-8,'y',{},false);c.put(cx-6,y0-5,'(@)','y');c.put(cx+4,y0-5,'(@)','y');c.put(cx-1,y0-5,'@','a');
 c.put(cx+2,y0-8,'~','y');c.put(cx-4,y0-8,'~','y');
 P(c,['.----.','| ?  |',"'----'"],cx+4,y0+4,'p',{'?':'r'},true);c.line(cx+4,y0+4,cx+1,y0+2,'-','y');
 sparks(c,[[1,2],[W-2,3],[W-3,y0+8]],f,'f');
 return {entry:{x:cx,y:H-1},contact:{x:cx,y:y0+6},bow:{x:cx,y:y0-5},lid:{x:cx,y:y0-2},tag:{x:cx+6,y:y0+5}};
};
PROPS.parade_flag=(c,W,H,f,t)=>{
 c.line(4,2,4,H-1,'|','z');c.put(3,1,'(o)','y');c.put(2,H-2,'/_|_\\\\','a');
 const rows=13,left=5;
 for(let r=0;r<rows;r++){
  const wave=Math.round(Math.sin(t*3+r*.35)*1.3),len=(r<rows-3?W-9:W-9-(r-rows+3)*3);
  const y=4+r;for(let i=0;i<len;i++){const w2=Math.round(Math.sin(t*3+i*.4)*1.3);const x=left+i,yy=y+w2;
   if(yy<0||yy>=H)continue;c.solid(x,yy,1,1,i<2||r<1||r>rows-2?'r':'y');c.put(x,yy,r<1||r>rows-2?'=':i<2?'|':' ',i<2?'y':'r');}
 }
 const ex=Math.round(W/2),wv=Math.round(Math.sin(t*3+4)*1.2);
 P(c,['.-.','(o>',' \\\\_/'].map(r=>r),ex-4,7+wv,'r',{o:'f','>':'e'},false);
 P(c,['<>  <>'],left+3,6,'r');c.put(W-9,13+wv,'* * *','r');
 c.put(left+1,H-3,'~~~~~~','r');
 sparks(c,[[W-3,2],[2,10]],f,'y');
 return {entry:{x:4,y:H-1},contact:{x:4,y:H-6},pole:{x:4,y:12},cloth:{x:ex,y:10},tip:{x:W-5,y:7}};
};
PROPS.frog_spawn=(c,W,H,f,t)=>{
 for(let y=0;y<H;y++)for(let x=0;x<W;x++)if((x*3+y*5+f)%11===0&&y>1)c.put(x,y,'~','w');
 const pts=[[5,6],[9,4],[13,6],[17,4],[8,9],[12,10],[16,9],[4,11],[20,8],[10,13],[14,13],[6,14],[19,12],[2,8],[21,5]];
 pts.forEach(([x,y],i)=>{const b=Math.round(Math.sin(t*1.5+i)*.4);c.ellipse(x,y+b,2.2,1.6,'o','c',true);c.put(x-1,y+b-1,'.','f');c.put(x,y+b,i%4===0?'@':'o','d');if(i%4===0)c.put(x,y+b,'@','k');});
 c.put(x0(W),2,'','f');
 // a tiny tadpole wriggling out
 const tx=W-7,ty=H-4+(f%2);P(c,['o~~~~~'],tx-1,ty,'k');c.put(tx-1,ty,'@','x');c.put(tx+5,ty,'~','x');
 c.put(2,H-2,'"|"','h');c.put(W-4,H-2,'"|"','h');
 sparks(c,[[W-4,2]],f,'f');
 return {entry:{x:W/2,y:H-1},contact:{x:W/2,y:8},clump:{x:W/2,y:8},tadpole:{x:tx,y:ty}};
};
const x0=W=>W-1;
PROPS.pirate_compass=(c,W,H,f,t)=>{
 const cx=W/2,cy=H/2+.5;
 blob(c,'round',cx,cy,9,'y','a');blob(c,'round',cx,cy,7.3,'y','d');
 c.put(cx-1,1,'(o)','y');c.put(cx-1,0,'_','y');
 c.put(cx-1,cy-5,'N','r');c.put(cx-1,cy+5,'S','f');c.put(cx-8,cy,'W','f');c.put(cx+7,cy,'E','f');
 for(let i=0;i<8;i++){const a=i/8*TAU;c.put(cx+Math.cos(a)*5.6,cy+Math.sin(a)*3.6,i%2?'.':'+','y');}
 const a=-0.9+Math.sin(t*1.4)*.12;const nx=Math.cos(a)*5,ny=Math.sin(a)*3.4;
 c.line(cx,cy,cx+nx,cy+ny,null,'r');c.line(cx,cy,cx-nx,cy-ny,null,'f');c.put(cx-1,cy,'(@)','y');
 c.put(cx+nx+1,cy+ny-1,'X','r');
 c.put(cx-5,cy-4,'/','f');c.put(cx-7,cy-2,'|','f');
 c.put(cx+7,cy+4,'<','a');
 sparks(c,[[2,3],[W-3,H-3]],f,'f');
 return {entry:{x:cx,y:H-1},contact:{x:cx,y:cy},dial:{x:cx,y:cy},needle:{x:cx+nx,y:cy+ny},ring:{x:cx,y:1}};
};
PROPS.heart_of_pond=(c,W,H,f,t)=>{
 const cx=W/2,cy=10;
 for(let r=0;r<3;r++){const rr=8+((f+r)%3)*2.2;for(let i=0;i<26;i++){const a=i/26*TAU;dot(c,cx+Math.cos(a)*(rr*.8+5),H-4+Math.sin(a)*(rr+1)/3,(i+r)%2?'~':'-','w');}}
 blob(c,'heart',cx,cy,10.5,'c','c');blob(c,'heart',cx,cy,8.3,'x','x');blob(c,'heart',cx,cy,5.2,'w','c');
 for(const [x0,y0,x1,y1] of [[cx-8,cy-4,cx,cy+3],[cx+8,cy-4,cx,cy+3],[cx,cy-6,cx,cy+3],[cx-8,cy-4,cx,cy-6],[cx+8,cy-4,cx,cy-6]])c.line(x0,y0,x1,y1,null,'f');
 c.put(cx-6,cy-6,'\\\\','f');c.put(cx-5,cy-5,'.','f');c.put(cx-2,cy,'<3',f%2?'f':'q');
 c.put(2,H-3,'(_)','g');c.put(W-5,H-2,'(_)','g');c.put(4,H-4,'.','f');
 for(let i=0;i<8;i++){const a=i/8*TAU+f*.5;dot(c,cx+Math.cos(a)*13,cy+Math.sin(a)*7.5,'.*+'[i%3],'c');}
 sparks(c,[[cx,0],[2,5],[W-3,8]],f,'f');
 return {entry:{x:cx,y:H-1},contact:{x:cx,y:cy},core:{x:cx,y:cy},ripple:{x:cx,y:H-5}};
};
PROPS.fish_treat=(c,W,H,f,t)=>{
 c.line(1,1,W-2,1,'~','z');c.put(1,2,'(','z');c.put(W-2,2,')','z');
 [[6,3,'a'],[13,4,'n'],[20,3,'a']].forEach(([x,y,tn],i)=>{
  c.line(x+3,1,x+3,y,'|','z');
  const sw=(f+i)%4===0?1:0;
  P(c,['  ,',' /@>==<','\\\\_~_\\\\/'].map(r=>r),x-3+sw,y,tn,{'@':'f','=':'b','~':'b'},true);
  c.put(x+1+sw,y+2,'^^^',tn);
 });
 return {entry:{x:W/2,y:H-1},contact:{x:W/2,y:5},string:{x:W/2,y:1},fish:{x:13,y:5}};
};
// Standalone drawings of six worn pieces (shop, wardrobe, journal); on Cheese they are fitted by wearables.mjs.
PROPS.umbrella=(c,W,H,f)=>{
 const cx=Math.round(W/2),x=cx-11;
 P(c,['         _.-^-._        ',"      .-'/  |  \\'-.     ","    .'  /   |   \\  '.   ",'   /___/____|____\\___\\  ','   v   v    v    v   v  '],x,1,'r',{'/':'z','\\':'z','|':'z','^':'f',_:'r',v:'y'},true);
 c.solid(x+6,2,4,2,'y');c.solid(x+15,2,3,2,'y');
 P(c,['|','|','|','|','|'],cx+1,6,'k');
 P(c,['  |','\\_/'],cx-1,11,'z');
 if(f%4<2)c.put(x+7,3,'*','f');
 return {entry:{x:cx,y:H-1},contact:{x:cx+1,y:9},canopy:{x:cx,y:3},tip:{x:cx,y:1},handle:{x:cx,y:12},rib:{x:x+4,y:4}};
};
PROPS.bouquet=(c,W,H,f)=>{
 const cx=Math.round(W/2),sway=f%4<2?0:1;
 P(c,['  @   *   @  ',' (q) (y) (r) ','@  (f) (q)  @',' (r) (l) (y) ','  \\ \\|/ /   '],cx-6+sway,1,'g',{'@':'q','*':'y','q':'q','y':'y','r':'r','f':'f','l':'l','(':'h',')':'h'});
 P(c,['   \\|||/   ','    |||    ','   \\|||/   ','    |||    '],cx-5,6,'h');
 P(c,['  .=====.  ',' /  ~~~  \\ ','|  ~ * ~  |',' \\  ~~~  / ',"  '-----'  "],cx-5,10,'u',{'~':'f','*':'y'},true);
 P(c,['   |   |   ','   |___|   '],cx-5,15,'h');
 c.put(cx-6,13,'~<',"q");c.put(cx+5,13,'>~','q');
 return {entry:{x:cx,y:H-1},contact:{x:cx,y:12},blooms:{x:cx,y:3},wrap:{x:cx,y:11},stems:{x:cx,y:16},ribbon:{x:cx-5,y:13}};
};
PROPS.easter_egg_basket=(c,W,H,f)=>{
 const cx=Math.round(W/2),x=cx-11;
 P(c,['        .-------.        ',"      .'         '.      ",'     /             \\     ','    /               \\    '],x,1,'z');
 P(c,['     (=)(~)(o)(=)(~)    '],x,5,'q',{'(':'k',')':'k','=':'y','~':'w',o:'r'},false);
 c.solid(x+6,5,3,1,'q');c.solid(x+9,5,3,1,'w');c.solid(x+12,5,3,1,'y');c.solid(x+15,5,3,1,'l');c.solid(x+18,5,3,1,'g');
 P(c,['   \\vVvVvVvVvVvVvVvVvV/  ','   |^v^v^v^v^v^v^v^v^v|  ','    \\#=#=#=#=#=#=#=#=/   ',"     '----------------'   "],x,6,'b',{'#':'z','=':'a',v:'h',V:'h','^':'h'},true);
 if(f%4===1)c.put(cx,4,'*','f');
 return {entry:{x:cx,y:H-1},contact:{x:cx,y:8},handle:{x:cx,y:1},eggs:{x:cx,y:5},weave:{x:cx,y:8},grass:{x:cx-6,y:6}};
};
PROPS.sparkle_aura=(c,W,H,f)=>{
 const cx=Math.round(W/2),x=cx-8;
 P(c,['      .  *  .     ',"   +    ' '    +  ",'  .   .-*-.    .  ',' *   (  @  )   *  ',"  .   '-*-'    .  ",'   +    . .    +  ','      .  *  .     '],x,1,'l',{'*':'y','+':'c','@':'f','(':'v',')':'v','-':'v'},false);
 [[x+6,1],[x+15,3],[x+16,4],[x+1,4],[x+3,2],[x+11,7]].forEach(([a,b],i)=>glint(c,a,b,f,i%2?'y':'c',i));
 P(c,['.===.','|___|'],cx-2,H-3,'s',{},true);
 return {entry:{x:cx,y:H-1},contact:{x:cx-2,y:4},heart:{x:cx-2,y:4},halo:{x:cx-2,y:1},stand:{x:cx,y:H-2}};
};
PROPS.rainbow_trail=(c,W,H,f)=>{
 const x=Math.round(W/2)-15;
 P(c,['          __.--==--.__          ',"      _.-'            '-._      ","    .'                    '.    ",'   /                        \\   ','  /                          \\  '],x,1,'r');
 P(c,['            .-~~~~-.            ',"        _.-'        '-._        ","      .'                '.      ",'     /                    \\     '],x,3,'y');
 P(c,['              .==.              ',"          _.-'    '-._          ","        .'            '.        "],x,5,'u');
 P(c,[' .oO.                      .Oo. ',' (__)                      (__) '],x,7,'f',{},true);
 sparks(c,[[x+7,1],[x+25,2],[x+15,9]],f,'y');
 return {entry:{x:W/2,y:H-1},contact:{x:x+3,y:8},arc:{x:x+16,y:1},cloud_left:{x:x+3,y:8},cloud_right:{x:x+28,y:8}};
};
PROPS.heart_bubbles=(c,W,H,f)=>{
 const x=Math.round(W/2)-9,bob=f%2;
 P(c,['    .---.         ','   /     \\   .--. ','  | <3 <3 | / <3 \\',"   \\     /  \\    /","    '---'    '--' "],x,1+bob,'i',{'<':'j','3':'j'},false);
 P(c,['   .-.     o      ','  ( <3)           ',"   '-'    o       ",'        o         '],x,6,'i',{'<':'q','3':'q'},false);
 P(c,['       \\ | /      ','       ( O )      ',"       '---'      "],x,10,'w',{O:'f'},false);
 return {entry:{x:W/2,y:H-1},contact:{x:x+9,y:11},bubble_big:{x:x+6,y:3},bubble_low:{x:x+4,y:7},wand_ring:{x:x+9,y:11}};
};
function prop(c,W,H,s,f,t,id){return PROPS[id](c,W,H,f,t);}

// ------------------------------------------------------------------ the ancient dragon fish: a long wish-granting serpent
function serpent(c,W,H,s,f,t,id){
 const cy=Math.floor(H/2)+1,xh=W-22,ph=t*2.1;
 const yc=x=>cy+Math.sin(x*.115-ph)*(3.5+4*(1-Math.min(1,x/xh)));
 const th=x=>1.3+2.4*Math.pow(Math.min(1,x/xh),.8);
 let prev=yc(2);
 for(let x=2;x<=xh;x++){
  const y=yc(x),h=th(x),a=Math.floor(Math.min(y,prev)-h),b=Math.ceil(Math.max(y,prev)+h);prev=y;
  for(let yy=a;yy<=b;yy++){
   const z=(yy-y)/(h+.01),belly=z>.35,tone=belly?'y':'x',ch=yy===a?'_':yy===b?'-':belly?'=':((x+yy)%3===0?'<':(x+yy)%3===1?'(':' ');
   c.solid(x,yy,1,1,tone);if(ch!==' ')c.put(x,yy,ch,belly?'a':(x%6<3?'c':'x'));
  }
  if(x%3===0)c.put(x,Math.floor(y-h)-1,(x+f)%2?'^':'/',x%6?'e':'y');
  if(x%9===4){c.put(x,Math.ceil(y+h)+1,'\\\\','x');}
 }
 // tail flame fin
 for(let i=0;i<6;i++){const y=yc(2);c.put(2-1+0,y+(i-3)*1.2,'<',i%2?'e':'y');}
 for(let i=0;i<4;i++)c.put(0+i%2,yc(2)+(i-2)*1.4,'~',i%2?'e':'y');
 // head
 const hy=yc(xh)-.5,hx=xh+9;
 c.ellipse(hx,hy,11,5,'-','x',true);c.solid(hx-8,hy+3,18,2,'y');
 c.put(hx-9,hy+3,'(==',"a");c.line(hx-8,hy+3,hx+9,hy+3,'=','a');
 c.put(hx+6,hy+1,'==<','y');c.put(hx+8,hy-1,'>','e');c.put(hx+4,hy+3,'VvV','f');
 c.put(hx+1,hy-2,'O','y');c.put(hx,hy-2,'(','k');c.put(hx+3,hy-3,'^^','e');
 c.put(hx+10,hy+3,'o',f%2?'f':'c');c.put(hx+11,hy+3,')','c');
 // horns
 c.line(hx-3,hy-5,hx-9,hy-10,'/','f');c.line(hx-1,hy-5,hx-5,hy-11,'/','f');c.put(hx-10,hy-11,'^','f');c.put(hx-5,hy-12,'^','f');
 // flowing whiskers
 for(let k=0;k<2;k++)for(let i=0;i<16;i++){const x=hx+8-i*1.0-k*1,y=hy+2+(k?5:4)+Math.sin(i*.55+ph)*2.2*(k?-1:1);if(x>=0)c.put(x,y,i%3?'~':'-',k?'y':'e');}
 // mane and glints
 for(let i=0;i<5;i++)c.put(hx-8+i*2,hy-6-(i%2)+((f+i)%2?0:-1),'^~*'[i%3],i%2?'e':'r');
 sparks(c,[[W-5,3],[W-14,H-4],[Math.round(W*.45),2],[8,H-3]],f,'y');
 return {entry:{x:W/2,y:H-1},contact:{x:Math.round(W*.45),y:Math.round(yc(W*.45))},head:{x:hx,y:hy},tail:{x:2,y:yc(2)},pearl:{x:hx+10,y:hy+3},whisker:{x:hx-6,y:hy+7}};
}

// ------------------------------------------------------------------ entry point
const BUILD={serpent,prop,bottle,egg,tool,block,fiber,essence,costume,trophy,acorn,cone,feather,crown,hat,wreath,badge,medal,token,charm,coin,scale:scaleItem,card:(c,W,H,s,f,t,id)=>card(c,W,H,s,f,t,id),fish:(c,W,H,s,f,t,id)=>fish(c,W,H,s,f,t,id)};
const SPECS={...FISH,...BOTTLES,...EGGS,...TOOLS,...BLOCKS,...COSTUMES,...TROPHIES,...ACORNS,...FEATHERS,...CROWNS,...HATS,...WREATHS,...BADGES,...MEDALS,...TOKENS,...CHARMS};
const GLOWS=new Set(['sparkle_aura','golden_feather','rainbow_feather','static_feather','magic_acorn','golden_acorn','fairy_dust','warmth','mystery_sound','mystic_egg','heart_of_pond','guardian_blessing','golden_koi','ghost_fish','legend_phoenix','legend_dragon','weather_sun','weather_rainbow','master_trophy','legendary_trophy','golden_duck_trophy','fog_essence','magic_wand','ancient_dragon_fish','rainbow_charm','frozen_dewdrop','golden_badge','duck_crown','snowflake_crown']);
const MEMO=new Map();
function construct(p,item,f,t){
 const k=p.grid||1,W=Math.ceil(p.w/k),H=Math.ceil(p.h/k),c=new ObjectCanvas(W,H);
 const raw=BUILD[p.type](c,W,H,SPECS[item.id]||{},f,t,item.id)||{};
 const anchors={};
 for(const [n,a] of Object.entries({entry:{x:W/2,y:H-1},contact:{x:W/2,y:H/2},...raw}))anchors[n]={x:clamp(Math.round(a.x),0,W-1),y:clamp(Math.round(a.y),0,H-1)};
 const fin=c.finish();fin.fills=mergeFills(fin.fills);
 return {...fin,construction:'curio-v1',detail:true,detailScale:.62,blueprint:item.id,detailGrid:k,anchors,inks:INKS,panels:PANELS,sway:0,lift:0,animated:true,emissive:GLOWS.has(item.id)};
}
// Saved wear (dirt, damage, wetness) is drawn over the art: a muddy badge looks muddy.
function wear(built,state){
 const dirt=state.dirt>.35,crack=(state.condition??1)<.45,wet=state.wetness>.45;
 if(!dirt&&!crack&&!wet)return built;
 const art=built.art.map(r=>[...r]),tones=built.tones.map(r=>[...r]),H=art.length,W=art[0]?.length||0;
 const mark=(x,y,ch,tone)=>{if(y>=0&&y<H&&x>=0&&x<W&&art[y][x]!==' '){art[y][x]=ch;tones[y][x]=tone;}};
 // Marks land only on ink, spread deterministically over the drawing.
 const ink=[];for(let y=0;y<H;y++)for(let x=0;x<W;x++)if(art[y][x]!==' ')ink.push([x,y]);
 const every=Math.max(2,Math.floor(ink.length/12));
 ink.forEach(([x,y],i)=>{if(dirt&&i%every===0)mark(x,y,':','z');else if(wet&&i%every===Math.floor(every/2))mark(x,y,"'",'w');else if(crack&&i%every===1)mark(x,y,'/','k');});
 return {...built,art:art.map(r=>r.join('')),tones:tones.map(r=>r.join(''))};
}
export function curioSprite(base,item,time,{motion=true,state={}}={}){
 const p=BLUEPRINTS[item?.id];if(!p||!BUILD[p.type])return null;
 const offset=(hash(item.id)%97)/97,f=motion?Math.floor(time*3+offset):0,t=f/3,key=item.id+'|'+f;
 let built=MEMO.get(key);
 if(built){MEMO.delete(key);MEMO.set(key,built);}
 else{built=construct(p,item,f,t);MEMO.set(key,built);if(MEMO.size>384)MEMO.delete(MEMO.keys().next().value);}
 const worn=wear(built,state||{});
 return {...base,...worn,anchors:built.anchors};
}
