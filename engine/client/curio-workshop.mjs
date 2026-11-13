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
const glint=(c,x,y,f,tone='f',ph=0)=>c.put(x,y,['.','+','*','+'][(f+ph)%4],tone);
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
 if(s.laurel){c.put(cx-12,cy,'(\\\\','h');c.put(cx+11,cy,'//)','h');}
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
  for(let r=0;r<3;r++){const rr=(f+r)%3;for(let i=0;i<20;i++){const a=i/20*TAU;c.put(cx+Math.cos(a)*(5+rr*2.8)*1.2,cy+Math.sin(a)*(5+rr*2.8)/1.5*1.2,rr===0?'o':'.','y');}}
 }
 blob(c,s.shape,cx,cy,R,s.rim,s.rim);blob(c,s.shape,cx,cy,R*.76,s.rim,s.inner);
 if(s.crystal){for(const [dx,dy,ch] of [[-8,-4,'/'],[8,-4,'\\\\'],[-8,4,'\\\\'],[8,4,'/'],[0,-8,'^'],[0,8,'v']])c.put(cx+dx,cy+dy,ch,'w');c.put(cx-5,cy-5,'\\\\','f');}
 emb(c,s.emb,cx,cy,s.tone,s.map||{});
 if(id==='ancient_amulet'){c.put(cx-4,cy+4,'-- ~ --','a');c.put(cx-2,cy-5,'|||','k');}
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
  const tn=['c','l','q','w','x','v'];
  for(let r=0;r<5;r++)for(let a=0;a<=12;a++){const th=Math.PI*(a/12),rr=3+r*2.5;if(r<4||a%2===0)c.put(cx+Math.cos(th)*rr*1.1,19-Math.sin(th)*rr*.9,r%2?')':'(',tn[(r+a+f)%6]);}
  c.solid(cx-9,13,19,6,'l');
  for(let a=0;a<=12;a++){const th=Math.PI*a/12;c.line(cx,19,cx+Math.cos(th)*11,19-Math.sin(th)*13*.7,null,tn[(a+f)%6]);}
  c.put(cx-3,19,'\\\\___/','x');c.put(cx-1,20,'v','x');
  sparks(c,[[cx-9,3],[cx+8,4],[cx,1],[cx+11,12]],f,'f');
 }
 return {entry:{x:cx,y:H-1},contact:{x:cx,y:cy},face:{x:cx,y:cy},tip:{x:cx,y:H-3}};
}

// ------------------------------------------------------------------ entry point
const BUILD={badge,medal,token,charm,coin,scale:scaleItem,card:(c,W,H,s,f,t,id)=>card(c,W,H,s,f,t,id),fish:(c,W,H,s,f,t,id)=>fish(c,W,H,s,f,t,id)};
const SPECS={...FISH,...BADGES,...MEDALS,...TOKENS,...CHARMS};
const GLOWS=new Set(['golden_feather','rainbow_feather','static_feather','magic_acorn','golden_acorn','fairy_dust','warmth','mystery_sound','mystic_egg','heart_of_pond','guardian_blessing','golden_koi','ghost_fish','legend_phoenix','legend_dragon','weather_sun','weather_rainbow','master_trophy','legendary_trophy','golden_duck_trophy','fog_essence','magic_wand','ancient_dragon_fish','rainbow_charm','frozen_dewdrop','golden_badge','duck_crown','snowflake_crown']);
const MEMO=new Map();
function construct(p,item,f,t){
 const k=p.grid||1,W=Math.ceil(p.w/k),H=Math.ceil(p.h/k),c=new ObjectCanvas(W,H);
 const raw=BUILD[p.type](c,W,H,SPECS[item.id]||{},f,t,item.id)||{};
 const anchors={};
 for(const [n,a] of Object.entries({entry:{x:W/2,y:H-1},contact:{x:W/2,y:H/2},...raw}))anchors[n]={x:clamp(Math.round(a.x),0,W-1),y:clamp(Math.round(a.y),0,H-1)};
 const fin=c.finish();fin.fills=mergeFills(fin.fills);
 return {...fin,construction:'curio-v1',detail:true,detailScale:.62,blueprint:item.id,detailGrid:k,anchors,inks:INKS,panels:PANELS,sway:0,lift:0,animated:true,emissive:GLOWS.has(item.id)};
}
export function curioSprite(base,item,time,{motion=true}={}){
 const p=BLUEPRINTS[item?.id];if(!p||!BUILD[p.type])return null;
 const offset=(hash(item.id)%97)/97,f=motion?Math.floor(time*3+offset):0,t=f/3,key=item.id+'|'+f;
 let built=MEMO.get(key);
 if(built){MEMO.delete(key);MEMO.set(key,built);}
 else{built=construct(p,item,f,t);MEMO.set(key,built);if(MEMO.size>384)MEMO.delete(MEMO.keys().next().value);}
 return {...base,...built,anchors:built.anchors};
}
