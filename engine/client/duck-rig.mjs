import {DUCK_AGES} from './duck-designs.mjs';
import {fitWearables,paintWearables} from './wearables.mjs';
export {DUCK_AGES};
export const mirrorGlyph=c=>({'/':'\\','\\':'/','(' :')',')':'(','<':'>','>':'<','[':']',']':'['}[c]||c);
const W=76,H=48,CX=36,FLOOR=39;
const PHASE=[0,-1,-1,0,0,-1,-1,0];
export function actionFor(state='idle'){
 if(/sleep|nap/.test(state))return 'sleeping';if(/swim|float|splash|div/.test(state))return 'swimming';
 if(/eat|peck|hungry/.test(state))return 'eating';if(/hop|jump/.test(state))return 'hopping';
 if(/danc|playing|excited/.test(state))return 'dancing';if(/flap|wav|stretch/.test(state))return 'flapping';
 if(/clean|preen|shake|ruffle/.test(state))return 'preening';if(/quack|sing|yawn/.test(state))return 'quacking';
 if(/walk|waddle|sneak|arriv|leav|exercise/.test(state))return 'walking';return 'idle';
}
export function duckRig(duck,t=0,design=null){
 const requested=duck.stage==='teen'?'juvenile':duck.stage||'adult',spec=design||DUCK_AGES.find(a=>a.id===requested)||DUCK_AGES[5];
 const stage=design?'adult':spec.id,small=['hatchling','duckling'].includes(stage),action=actionFor(duck.state);
 const rate=spec.pace/4.5,speed=duck.state==='waddle_fast'?1.6:duck.state==='sneaking'?.65:1;
 const cycle=t*rate*speed,phase=Math.floor(cycle*5)%8;
 const cells=Array.from({length:H},()=>Array(W).fill(' ')),tones=cells.map(r=>r.map(()=> 'b')),fills=[];
 let clipped=false,rig=null,plan={items:[],inks:{}};
 const put=(str,x,y,tone='b')=>{x=Math.round(x);y=Math.round(y);for(let i=0;i<str.length;i++){if(str[i]===' ')continue;if(x+i<0||x+i>=W||y<0||y>=H){clipped=true;continue;}cells[y][x+i]=str[i];tones[y][x+i]=tone;}};
 const group=(rows,x,y,tone)=>rows.forEach((r,j)=>put(r,x,y+j,tone));
 const ink={b:spec.tints?.[0]||'#cba27c',g:spec.tints?.[1]||'#8fc5aa',j:'#65a58d',h:'#b1dcc4',s:'#937152',a:'#efc46a',w:'#dbbfa0',c:'#f0ead2',p:spec.tints?.[2]||'#94c6e4',e:'#172b25',...spec.inkOverrides};
 if(stage==='egg'){
  const dx=[0,0,-1,0,1,0,-1,0][phase],x=CX-7+dx,y=FLOOR-spec.art.length;
  group(spec.art,x,y,'c');if(phase>=3&&phase<=6)put(phase<5?'/':'/\\',CX-1+dx,y+2,'s');if(phase>=5&&phase<=6)put(',~.',CX-2+dx,y-1,'a');
  spec.art.forEach((r,j)=>{const a=r.search(/\S/),b=r.trimEnd().length;if(a>=0)fills.push({x:x+a,y:y+j,w:b-a,tone:'c'});});
 }else{
  const L=spec.art.length,baseX=CX-(spec.feet[0]+spec.feet[1])/2-1,baseY=FLOOR-(L-1);
  let bodyDY=0,headDX=0,headDY=0,jump=0,eye=duck.eye||'O';
  const mood=duck.mood||duck.state||'';
  if(/happy|ecstatic|proud|petting|danc/.test(mood))eye='^';else if(/sad|miserable|sick/.test(mood))eye=';';else if(/angry|grumpy|petty/.test(mood))eye='>';else if(/dramatic/.test(mood))eye='@';else if(/scared|surpris/.test(mood))eye='O';
  if(action==='walking'||action==='dancing'){bodyDY=PHASE[phase];headDY=PHASE[(phase+7)%8];headDX=[0,1,1,0,0,-1,-1,0][phase];}
  if(action==='eating'){headDX=[0,1,2,3,3,2,1,0][phase];headDY=[0,1,2,3,3,2,1,0][phase];bodyDY=phase>1&&phase<6?1:0;}
  if(action==='preening'){headDX=[0,-1,-3,-4,-3,-2,-1,0][phase];headDY=[0,1,2,3,2,1,1,0][phase];}
  if(action==='hopping'){jump=[0,1,-1,-4,-5,-3,1,0][phase];bodyDY=headDY=jump;}
  if(action==='sleeping'){bodyDY=1;headDX=-2;headDY=3;eye='-';}
  if(action==='swimming'){bodyDY=headDY=1;}
  if(action==='dancing'){eye='^';bodyDY--;headDY--;}
  if(cycle%5.3>5||action==='sleeping')eye='-';
  let eyePos=null,headBounds=null,bodyBounds=null,wingBounds=null;
  function extend(bounds,x,y,w){return bounds?{x:Math.min(bounds.x,x),y:Math.min(bounds.y,y),w:Math.max(bounds.x+bounds.w,x+w)-Math.min(bounds.x,x),h:Math.max(bounds.y+bounds.h,y+1)-Math.min(bounds.y,y)}:{x,y,w,h:1};}
  // Torso first, then face: a peck or preen can overlap the folded wing.
  const rows=[...Array(L-1).keys()].sort((a,b)=>(a<spec.collar)-(b<spec.collar));
  for(const y of rows){
   const row=spec.art[y],head=y<spec.collar,crest=y<(spec.crest||0),dx=head?headDX:0,dy=head?headDY:bodyDY;
   const x0=Math.round(baseX+dx+(crest?[0,0,1,1,0,-1,-1,0][phase]:0)),y0=baseY+y+dy;
   const first=row.search(/\S/),end=row.trimEnd().length;
   if(first<0)continue;
   if(action==='swimming'&&y>L-4)continue;
   if(!crest){fills.push({x:x0+first,y:y0,w:end-first,tone:head?'g':'b'});if(head)headBounds=extend(headBounds,x0+first,y0,end-first);else bodyBounds=extend(bodyBounds,x0+first,y0,end-first);}
   const beak=row.indexOf(')==')>=0?row.indexOf(')==')+1:row.indexOf(')>')>=0?row.indexOf(')>')+1:100;
   const wing=row.indexOf('['),wingEnd=row.indexOf(']');
   if(!head&&wing>=0)wingBounds={x:x0+wing-1,y:y0-1,w:wingEnd-wing+3,h:3};
   else if(!head&&!wingBounds&&row.includes('(vv)'))wingBounds={x:x0+row.indexOf('(vv)'),y:y0,w:4,h:1};
   for(let x=0;x<row.length;x++){
    let c=row[x];if(c===' ')continue;
    const isEye=head&&'oO'.includes(c);let tone=head?'g':'b';
    if(isEye){c=eye;eyePos={x:x0+x,y:y0,char:c};}
    if(':.'.includes(c))tone=head?'j':(x+y)%3?'s':'b';
    if(!head&&'/v'.includes(c)&&x>first+3&&x<end-2)tone='w';
    if(x===first||x===end-1||c==="'")tone=head?'h':'b';
    if(y===spec.collar)tone='c';if(wing>=0&&x>=wing&&x<=wingEnd)tone='p';if(isEye)tone='e';if(head&&x>=beak)tone='a';
    put(c,x0+x,y0,tone);
   }
   if(head&&beak<100&&['quacking','eating'].includes(action)&&phase>=2&&phase<=5)put('\\_',x0+beak,y0+1,'a');
  }
  const footPositions=[];
  if(!['swimming','sleeping'].includes(action))for(const [i,fx] of spec.feet.entries()){
   const lift=action==='walking'&&((phase<4&&i===0)||(phase>=4&&i===1))?1:0;
   const stride=action==='walking'?[0,i?-1:1,0,0,0,i?1:-1,0,0][phase]:0;
   const x=Math.round(baseX+fx+stride),y=FLOOR+jump-lift;
   put(i?'>_':'_>',x,y,'a');footPositions.push({x,y});
  }
  const h=headBounds||{x:CX,y:baseY+2,w:8,h:4},b=bodyBounds||{x:CX-8,y:FLOOR-6,w:16,h:6},e=eyePos||{x:h.x+2,y:h.y+1,char:eye};
  rig={small,stage,action,phase,head:{...h,w:Math.max(4,h.w-4)},faceBounds:h,eye:e,crest:{x:h.x,y:baseY+headDY,w:h.w},neck:{x:Math.round(baseX+spec.art[spec.collar].search(/\S/)),y:baseY+spec.collar+bodyDY,w:small?2:3},body:b,feet:footPositions};
  rig.torso=fills.filter(f=>f.tone==='b').map(f=>({...f}));rig.wing=wingBounds;
  if(['flapping','dancing'].includes(action)){
   const open=phase>=2&&phase<=5,wing=open?['  /)/)',' / / /','/ / /','\\__/']:['  /)',' / /',' \\/'];
   group(wing,b.x-2,b.y-(open?3:0),'w');if(open)group(wing.map(r=>[...r].reverse().map(mirrorGlyph).join('')),b.x+b.w-2,b.y-2,'w');
  }
  if(duck.state==='petting')put('<3',h.x+h.w+2,h.y-1-Math.floor(phase/3),'a');
  if(action==='eating'&&phase>1&&phase<6)put(phase%2?'. :':'. .',h.x+h.w+2,h.y+h.h,'a');
  if(action==='sleeping')put(phase%2?'z':'Z',h.x+h.w+2,h.y-1-Math.floor(phase/3),'c');
  if(action==='quacking'&&phase>=2&&phase<=5)put('!',h.x+h.w+3,h.y,'a');
  if(action==='swimming')put(phase%2?'~~~   ~~~~   ~~~':' ~~~~  ~~~~  ~~~',CX-9,FLOOR+1,'p');
  plan=fitWearables(rig,duck.cosmetics,t);clipped=paintWearables(cells,tones,rig,plan)||clipped;
  fills.push(...(plan.fills||[]));
  put(e.char,e.x,e.y,'e');
  if(duck.state==='diving'&&phase>=2&&phase<=5){cells.forEach(r=>r.fill(' '));fills.length=0;group([' \\ /','  /\\',' (__)'],CX-2,FLOOR-3,'a');put('~~~  ~~~~~',CX-5,FLOOR+1,'p');}
 }
 const facing=duck.facing!==false;
 if(!facing){for(let y=0;y<H;y++){cells[y].reverse();cells[y]=cells[y].map(mirrorGlyph);tones[y].reverse();}for(const f of fills)f.x=W-f.x-f.w;}
 return {art:cells.map(r=>r.join('')),tones:tones.map(r=>r.join('')),fills,inks:{...ink,...plan.inks},width:W,anchorX:facing?CX:W-1-CX,groundRow:FLOOR+.5,
  scale:stage==='egg'?.66:spec.height/(spec.art.length*7.5),body:ink.b,face:ink.g,accent:ink.a,shade:ink.s,name:'',rig,wearables:plan.items.map(i=>i.id),
  design:'d10',material:'feathers',phase,frames:8,cycle:phase/8,clipped,action,offsetY:action==='idle'?Math.sin(cycle*2)*.1:0};
}
