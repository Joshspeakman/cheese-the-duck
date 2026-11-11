import {duckRig,mirrorGlyph} from './duck-rig.mjs';
import {GUEST_CAST} from './guest-cast.mjs';
import {guestDesign,propRows} from './guest-shapes.mjs';
import {performancePose} from './performances.mjs';

export const VISITOR_STYLES=Object.fromEntries(['adventurous','scholarly','artistic','playful','mysterious','generous','foodie','athletic'].map(kind=>{
 const p=Object.values(GUEST_CAST).find(p=>p.archetype===kind);return [kind,{...p,tints:p.palette,gear:kind==='mysterious'?[...p.gear,'masquerade_mask']:p.gear}];
}));
export {GUEST_CAST};
const BY_NAME=new Map(Object.values(GUEST_CAST).map(p=>[p.name.toLowerCase(),p]));
export function guestProfile(duck={}){return GUEST_CAST[duck.castId||duck.id]||BY_NAME.get(String(duck.name||'').toLowerCase())||VISITOR_STYLES[duck.personality]||VISITOR_STYLES.adventurous;}
const W=76,H=48,FLOOR=39,seedOf=s=>[...s].reduce((n,c)=>n+c.charCodeAt(0),0);
const WORK={plane:'flapping',map:'preening',flask:'eating',chalkboard:'preening',abacus:'preening',magnifier:'preening',brush:'preening',pressed_flower:'preening',gears:'preening',lily_brush:'preening',watering_can:'eating',bubble_wand:'quacking',banana:'quacking',ball:'hopping',pinwheel:'quacking',mask:'quacking',puzzle:'preening',quill:'preening',sewing:'preening',tea_cup:'eating',sprout:'preening',first_aid:'preening',letter:'preening',jam:'eating',mushroom_basket:'eating',pepper_mill:'preening',stopwatch:'flapping',laces:'preening',trophy:'preening',clipboard:'preening',rocket:'hopping',bread_bag:'quacking',book:'preening',case:'preening',rose:'preening',buttons:'preening',mug:'eating'};

function canvas(base=null){
 const art=base?base.art.map(r=>[...r]):Array.from({length:H},()=>Array(W).fill(' '));
 const tones=base?base.tones.map(r=>[...r]):art.map(r=>r.map(()=> 'b'));
 const fills=base?base.fills.map(f=>({...f})):[];let clipped=Boolean(base?.clipped);
 function put(str,x,y,tone='b'){x=Math.round(x);y=Math.round(y);for(let i=0;i<str.length;i++){
   const ch=str[i];if(ch===' ')continue;if(x+i<0||x+i>=W||y<0||y>=H){clipped=true;continue;}art[y][x+i]=ch;tones[y][x+i]=tone;
 }}
 function group(rows,x,y,tone='b',solid=false,eyes=false){rows.forEach((line,j)=>{
   const a=line.search(/\S/),b=line.trimEnd().length;if(solid&&a>=0){
     fills.push({x:Math.round(x+a),y:Math.round(y+j),w:b-a,tone});
     for(let k=a;k<b;k++){const xx=Math.round(x+k),yy=Math.round(y+j);if(art[yy]?.[xx]!==undefined)art[yy][xx]=' ';}
   }
   [...line].forEach((ch,i)=>{let ink=tone;if(eyes&&ch==='O')ink='e';else if(/[=:<>]/.test(ch))ink='a';else if(/[.:]/.test(ch))ink='s';else if(i===a||i===b-1)ink='h';put(ch,x+i,y+j,ink);});
 });}
 function finish(facing){if(facing===false){for(let y=0;y<H;y++){art[y].reverse();art[y]=art[y].map(mirrorGlyph);tones[y].reverse();}for(const f of fills)f.x=W-f.x-f.w;}return {art:art.map(r=>r.join('')),tones:tones.map(r=>r.join('')),fills,clipped};}
 return {put,group,finish,art,tones,fills};
}

function signature(c,p,t,x,y,active){
 const phase=Math.floor(t*5)%8,rows=propRows(p,t,active);let dx=0,dy=0;
 if(active){
   if(['plane','rose'].includes(p.prop)){dx=[0,1,2,3,4,3,2,1][phase];dy=-Math.floor(dx/2);}
   else if(['ball','apple','rocket'].includes(p.prop))dy=[0,-1,-3,-4,-3,-1,0,0][phase];
   else if(['mug','flask','tea_cup','jam','teapot','mask'].includes(p.prop))dy=phase>2&&phase<6?-2:0;
   else dx=phase>2&&phase<5?1:0;
 }
 c.group(rows,x+dx,y+dy,'p',true);c.put(')~',x-2+dx,y+Math.min(2,rows.length-1)+dy,'w');
 if(active&&p.prop==='bubble_wand')c.put(phase%2?'o':'.',x+5+phase%3,y-1-phase%4,'p');
 if(active&&p.prop==='watering_can')c.group(phase%2?[' . .','  : ']:['  . ',' . .'],x+8,y+4,'p');
 if(active&&p.prop==='pepper_mill'&&phase>4)c.put('*',x-2,y-2,'a');
 if(active&&p.prop==='pinwheel')c.put(phase%2?'~':'-',x-2,y+1,'p');
 if(active&&p.prop==='sewing')c.put(phase%2?'\\':'/',x+4,y-2,'h');
 if(active&&p.prop==='plush')c.put(phase>3?'<3':'.',x+6,y-2,'p');
 if(active&&p.prop==='flasks')c.put(phase%2?'o':'.',x+2+phase%4,y-1-phase%3,'p');
 if(active&&p.prop==='rocket')c.put(phase<5?String(3-Math.floor(phase/2)):'*',x+3,y-3,'a');
}

function duckGuest(duck,p,t,requested,active){
 const state=active?WORK[p.prop]||'idle':requested,spec=guestDesign(p);
 if(duck.performance)duck={...duck,performance:{...duck.performance,young:p.species==='duckling'}};
 const base=duckRig({...duck,facing:true,state,cosmetics:Object.fromEntries(p.gear.map((id,i)=>[i,id]))},t,spec),c=canvas(base),r=base.rig,b=r.body,h=r.head;
 const markings={champion:['\\ /','(o)'],frida:['---'],truffle:['..'],pepper:['/'],ada:['::'],charity:['[X]','|/|'],cookie:['. : .'],sprint:['///'],heart:['<3'],leonardo:['o=o']};
 const mark=markings[p.id.replace('friend:','')];if(mark)c.group(mark,b.x+3,b.y+3,'p');
 if(p.id==='friend:frida')c.put('---',r.eye.x-1,r.eye.y-1,'b');
 if(p.id==='traveling_merchant'){for(let y=b.y+2;y<b.y+b.h-1;y+=2)c.put('| : |',b.x+4,y,'p');c.group(['[o]','[+]'],b.x+1,b.y+3,'a');}
 if(p.id==='celebrity_duck')c.put('[*]',b.x+b.w-7,b.y+2,'a');
 if(!duck.performance&&!/walking|arriving|leaving|swimming|sleeping/.test(requested)){
   const rows=propRows(p,t,active);let x=Math.min(W-Math.max(...rows.map(r=>r.length))-7,b.x+b.w-3),y=Math.min(FLOOR-rows.length-1,b.y+Math.max(3,b.h*.35));
   if(active&&p.prop==='apple'&&Math.floor(t*5)%8<3){x=h.x+1;y=h.y-5;}
   signature(c,p,t,x,y,active);
 }else if(requested!=='sleeping'&&!['botanical','instrument','lighting','keepsake','creative','textile','ground','architecture'].includes(duck.performance?.kind))c.group(['.---.','| : |',"'---'"],b.x+1,b.y+Math.max(2,b.h*.4),'p',true);
 if(/giving/.test(duck.activity||duck.state||''))c.group([' .-+- .',' |+ +|'," '---'"],Math.min(61,b.x+b.w),FLOOR-4,'p',true);
 c.put(r.eye.char,r.eye.x,r.eye.y,'e');
 return {...base,...c.finish(duck.facing),...Object.fromEntries(['bill','grip','workGripRest'].map(k=>[k,base[k]&&{...base[k],x:duck.facing===false?W-1-base[k].x:base[k].x}])),anchorX:duck.facing===false?W-1-base.anchorX:base.anchorX,action:state,profileId:p.id,design:'pond-cast',signature:active,habit:p.habit};
}

const GOOSE_BODY=['         .---==---.',"     _.-' . . . .  '-.",'  __/ . /vvvvvvvv\\ .  \\','<( . . ( [======] ) .  |',"  \\ . . \\vvvvvvvv/ . . |",'   | . . . . . . . .  /',"    \\ . . . . . . . /","     '---.______..-'"];
const GOOSE_HEAD=['     .---.','   .\' . . \\','  ( O   ___)====>',"   \\  .__.'",'    | . |'];
const OWL_HEAD=['  /\\             /\\',' / .\\__..---..__/ .\\','| . / . . . . . \\ . |','|  | .---. .---. |  |','(  |( O )( O )|  )',' \\  \\___/V\\___/  /','  | . .  \\/  . . |',"   \\ . . . . . ./","    '----..----' "];
const OWL_BODY=['    .-------.',"  .'vvv/vvvv '.",' /v/v/v/v/v/vv \\','( v/ [====] /v )','| v/v/v/v/v/vv |','| /v/v/v/v/v/v |','| v/v/v/v/v/vv |',' \\ v/v/v/v/v /','  \\ /v/v/v/ /',"   '---..---'",'    /v/v/v\\',"     '---'"];
const CROW_HEAD=['      /|/|','    _/ . |','  .\' . .  \\',' ( O   ____)===>',"  \\ .___./",'   | . |'];
const CROW_BODY=['       .---==-.','    .-\' . /v/v\\','  _/ . . /v/v/v|','<( . .  ([====])','  \\ . . \\v/v/v|','   | . .  \\v/v/','   \\ . . . \\/',"    '---.___.'",'      \\|\\|\\'];
const TOAD_HEAD=['   _.._          _.._','  / -- \\________/ -- \\',' (  O  / . . .  \\  O  )','  \\__/ . . . . .\\__/',' /  . . __________ .  \\','( . . /____________\\ . )'," \\ . '----.__.----' . /","  '---..________..---' "];
const TOAD_BODY=['    .---.____.---.','  ./ . /|::::|\\ . \\.',' / . .| |:vv:| |. . \\','| . . | |:vv:| | . .|',' \\ . .|_|____|_|. . /',"  '---\\       /---'",'    __/       \\__'];
const BUTTERFLY_WING=['  .----.',' / .:::.\\','/ .:(o):.\\','| :/\/\\: |','| .:(o): |',' \\ :..: /',"  '.__./",'  /:o:.\\',' / .::. |',' \\ :o:/',"  '--' "];

function speciesGuest(duck,p,t,state,active){
 const c=canvas(),phase=Math.floor(t*p.pace)%8,walking=/walk|arriv|leav|hopp/.test(state),asleep=/sleep/.test(state);
 const performance=performancePose(duck.performance);let grip=null,workGripRest=null,bill=null;
 if(performance){
  const group=c.group,put=c.put;
  c.group=(rows,x,y,tone='b',solid=false,eyes=false)=>group(rows,x+(tone==='g'?performance.x:0),y+performance.b+(tone==='g'?performance.y:0),tone,solid,eyes);
  c.put=(text,x,y,tone='b')=>put(text,x+(tone==='e'?performance.x:0),y+performance.b+(tone==='e'?performance.y:0),tone);
 }
 const dy=walking?({goose:[0,0,-1,-1,0,0,-1,-1],crow:[0,-1,-3,-2,0,0,-2,-1],toad:[0,1,-2,-3,-1,0,0,0]}[p.species]||[0,0,-1,-1,0,0,-1,-1])[phase]:0;
 const blink=asleep||t%5.7>5.4,eye=performance?.eye||(blink?'-':duck.mood==='happy'?'^':'O'),eyes=rows=>rows.map(r=>r.replaceAll('O',eye));
 let top=12,head={x:30,y:17,w:18,h:8},body={x:20,y:29,w:28,h:9},feet=[25,38];
 if(p.species==='goose'){
   top=15;c.group(GOOSE_BODY,21,30+dy,'b',true);
   for(let y=20;y<31;y++)c.group([y<25?'| . |':'|: .|'],38+(active&&phase>3&&y<25?1:0),y+dy,'g',true);
   c.group(['\\=====/', ' \\::/','  \\|'],36,24+dy,'p',true);
   c.group(eyes(GOOSE_HEAD),34+(active&&phase>3?1:0),16+dy,'g',true,true);c.put(eye,38+(active&&phase>3?1:0),18+dy,'e');
   if(active){c.put(phase>3?'\\_':'==',49,19+dy,'a');c.put(phase>3?'!':'.',54,16+dy,'p');}
   head={x:37,y:16+dy,w:16,h:7};body={x:24,y:30+dy,w:30,h:8};feet=[31,43];
 }else if(p.species==='owl'){
   top=12;const turn=active?[0,0,1,2,2,1,0,-1][phase]:0;
   c.group(OWL_BODY,22,26+dy,'b',true);
   c.group(eyes(OWL_HEAD),19+turn,17+dy,'g',true,true);
   c.put(eye,25+turn,21+dy,'e');c.put(eye,30+turn,21+dy,'e');c.put('V',28+turn,22+dy,'a');
   c.group([' .-------.','/|  ___  |',' |__| |__|','    :'],24+turn,14+dy,'p');
   if(active)c.group(phase>3?['/))',' /)']:['/||',' ||'],19,29+dy,'h');
   head={x:20+turn,y:17+dy,w:22,h:9};body={x:24,y:26+dy,w:19,h:12};feet=[28,37];
 }else if(p.species==='crow'){
   top=17;c.group(CROW_BODY,17,29+dy,'b',true);c.group([' |. |',' /v |','/v/v|','|v/v|'],32,25+dy,'b',true);
   c.group(eyes(CROW_HEAD),30,19+dy,'g',true,true);c.put(eye,33,22+dy,'e');
   c.group(['\\ * /',' \\o/'],32,27+dy,'p');c.group([' /|','/ /','\\/'],16,32+dy,'b');
   head={x:31,y:19+dy,w:19,h:7};body={x:19,y:29+dy,w:27,h:9};feet=[29,37];
 }else if(p.species==='toad'){
   top=21;c.group(TOAD_BODY,21,32+dy,'b',true);c.group([' .---::::---.'],25,31+dy,'b',true);
   c.group(eyes(TOAD_HEAD),19,23+dy,'g',true,true);c.put(eye,23,25+dy,'e');c.put(eye,38,25+dy,'e');
   c.group(['  /','_/__'],17,35+dy,'b');c.group(['\\',' \\__'],46,35+dy,'b');if(active&&phase>3)c.put('  ___  ',28,28+dy,'a');
   head={x:21,y:23+dy,w:29,h:8};body={x:23,y:32+dy,w:23,h:7};feet=[23,42];
 }else if(p.species==='butterfly'){
   top=18;const lift=Math.sin(t*4)*1.4,fold=performance?.w>.2?.35+.65*(1-performance.w*.65):.35+.65*Math.abs(Math.cos(t*5));
   for(const side of [-1,1])BUTTERFLY_WING.forEach((row,y)=>{
     const line=[...row].map(ch=>side<0?mirrorGlyph(ch):ch);if(side<0)line.reverse();
     const visible=line.filter((_,x)=>x%Math.max(1,Math.round(1/fold))===0).join('');c.group([visible],side<0?35-visible.length:39,21+y+lift,'p',true);
   });
   c.group([' @.    .@','   \\  /','   .--.','  (O  O)','   \\v/','   |::|','   |::|','   \\:/','    V'],32,18+lift,'g',true,true);
   c.put(eye,35,21+lift,'e');c.put(eye,38,21+lift,'e');c.put(phase%2?'*':'.',23+phase,21+lift,'a');c.put(phase%2?'.':'*',47-phase%3,29+lift,'h');
   head={x:34,y:20+lift,w:7,h:4};body={x:35,y:24+lift,w:4,h:5};feet=[];
 }
 if(!performance?.seated)for(const [i,x] of feet.entries()){const lift=performance?(i?performance.r:performance.l):walking&&((phase<4)===(i===0))?1:0;c.put(p.species==='toad'?'_\\/_':i?'>_':'_>',x,FLOOR+dy-lift-(performance?Math.max(0,performance.b):0),'a');}
 if(p.species!=='butterfly'&&!walking&&!asleep&&!performance){const x=p.species==='owl'?24:p.species==='toad'?43:p.species==='goose'?43:40;signature(c,p,t,x,p.species==='owl'?31:33,active);}
 if((performance?.botanical||performance?.instrument||performance?.lighting||performance?.keepsake||performance?.creative||performance?.textile||performance?.architecture||performance?.ground||performance?.w>.2)&&p.species!=='butterfly'){
   // A gesture grows from the shoulder. The previous feather patch floated
   // above tall bodies when its upward motion exceeded its own height.
   const shoulderY=Math.round(body.y+body.h*.4),row=shoulderY+performance.b;
   const feathers=c.fills.filter(f=>f.tone==='b'&&f.y===row).sort((a,b)=>b.w-a.w)[0];
   const shoulder={x:Math.round(feathers?feathers.x+feathers.w*.6:body.x+body.w*.4),y:shoulderY};
   const tip=(performance.botanical||performance.instrument||performance.lighting||performance.keepsake||performance.creative||performance.textile||performance.architecture||performance.ground)?{x:Math.min(W-4,Math.round(body.x+body.w+2+performance.reach*2)),y:shoulder.y+1}:{x:shoulder.x+Math.round(4+performance.w*5),y:shoulder.y-Math.round(performance.w*5)};
   if(performance.botanical||performance.instrument||performance.lighting||performance.keepsake||performance.creative||performance.textile||performance.architecture||performance.ground){grip={x:tip.x,y:tip.y+performance.b};workGripRest={x:Math.round(body.x+body.w+2),y:tip.y};}
   const n=Math.max(Math.abs(tip.x-shoulder.x),Math.abs(tip.y-shoulder.y));
   for(let i=0;i<=n;i++){
     const u=i/n,x=shoulder.x+(tip.x-shoulder.x)*u,y=shoulder.y+(tip.y-shoulder.y)*u;
     c.put('/',x,y,'w');if(p.species!=='toad')c.put('/',x+2,y+1,'w');
   }
   if(performance.botanical||performance.instrument||performance.lighting||performance.keepsake||performance.creative||performance.textile||performance.architecture||performance.ground)c.put(')',tip.x,tip.y,'w');
   else c.group(p.species==='toad'?[' /','/_)']:[' /)/)','/ / /','\\__/'],tip.x-1,tip.y-2,'w',true);
 }
 if(performance?.mark)c.put(performance.mark,head.x+head.w+2,head.y-2,'a');
 if(asleep)c.put('z',head.x+head.w+2,head.y-1,'p');
 if(p.species!=='butterfly'){
  const mouth={goose:[34+GOOSE_HEAD[2].length-1,18],crow:[30+CROW_HEAD[3].length-1,22],owl:[28,22],toad:[42,28]}[p.species];
  if(mouth)bill={x:mouth[0]+(performance?.x||0),y:mouth[1]+dy+(performance?.b||0)+(performance?.y||0)};
 }
 if(duck.facing===false)for(const point of [grip,workGripRest,bill])if(point)point.x=W-1-point.x;
 return {...c.finish(duck.facing),grip,workGripRest,bill,performance:duck.performance||null,width:W,anchorX:duck.facing===false?39:36,groundRow:39.5,scale:p.height/((40-top)*7.5),body:p.palette[0],face:p.palette[1],accent:p.palette[2],shade:'#778b7b',
   inks:{b:p.palette[0],g:p.palette[1],p:p.palette[2],h:'#e8dfc7',s:'#7c8e81',a:'#e1b26e',w:p.palette[1],e:'#152c29'},rig:{stage:'adult',species:p.species,head,body},seatContact:performance?.seated?body.y+body.h+performance.b-.3:null,material:'feathers',action:state,phase,frames:8,profileId:p.id,design:'pond-cast',signature:active,habit:p.habit,name:'',offsetY:0};
}

export function visitorRig(duck,time=0){
 if(['botanical','seating','instrument','lighting','keepsake','creative','textile','ground','architecture'].includes(duck.performance?.kind))time=duck.performance.motion===false?0:duck.performance.routine?.elapsed||0;
 const p=guestProfile(duck),seed=seedOf(p.id),t=time+seed%19*.17,raw=duck.activity||duck.state||'idle';
 const requested=/reading|painting|giving/.test(raw)?'signature':/bounce|happy|exercise/.test(raw)?'dancing':/chat|greet/.test(raw)?'quacking':raw;
 const active=!duck.performance&&(requested==='signature'||requested==='working'||requested==='idle'&&(t%(10+seed%5))>5&&(t%(10+seed%5))<8.5),state=duck.performance?'idle':requested==='signature'||requested==='working'?'idle':requested;
 const model=['duck','duckling'].includes(p.species)?duckGuest(duck,p,t,state,active):speciesGuest(duck,p,t,state,active);
 return {...model,personality:p.archetype,profileId:p.id,identity:p,habit:p.habit};
}
