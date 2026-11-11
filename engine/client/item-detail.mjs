import INSTRUMENTS from './animation/instruments.json' with {type:'json'};
// Detail is constructed in character space: contours, joinery, stitched seams,
// moving parts and wear stay crisp at every zoom. All gameplay state is supplied
// by the simulation; inspecting a catalogue never mutates an owned object.
import BOTANICAL from './animation/botanical.json' with {type:'json'};
const hash=s=>[...s].reduce((n,c)=>(n*33+c.charCodeAt(0))>>>0,17);
const has=(family,words)=>words.split(' ').includes(family);
export function itemProfile(item,family){
 if(INSTRUMENTS[item.id]){const p=INSTRUMENTS[item.id];return {kind:'music',material:p.type==='horn'||p.type==='chimes'?'metal':'wood',skill:'music',verb:p.type==='radio'?'Listen to':'Play',need:'fun',duration:24};}
 if(item.category==='food')return {kind:'food',material:'food',skill:'cooking',verb:'Taste',need:'hunger',duration:10};
 if(BOTANICAL[item.id]&&!BOTANICAL[item.id].rooted)return {kind:'keepsake',material:'leaf',skill:'observation',verb:'Inspect',need:'fun',duration:14};
 if(item.id==='pond_mat')return {kind:'comfort',material:'fabric',skill:'care',verb:'Settle on',need:'energy',duration:24};
 let kind='keepsake',material='ceramic',skill='observation',verb='Examine',need='fun';
 if(has(family,'rose tulip sunflower tree cherry willow cactus bamboo bonsai flytrap fern flowerpot mushroom hedge garden clover corn peas grapes reed leaf')){kind='plant';material='leaf';skill='gardening';verb='Tend';}
 else if(has(family,'pool fountain waterfall sprinkler birdbath bowl pond')){kind='water';material='stone';skill='stewardship';verb='Splash';need='cleanliness';}
 else if(item.category==='food'||has(family,'bread crumbs seeds salad pie cookie honey carrot tomato pumpkin strawberry watermelon')){kind='food';material='food';skill='cooking';verb='Taste';need='hunger';}
 else if(has(family,'bed nest hammock couch sofa cushion bench chair throne')){kind='comfort';material='fabric';skill='care';verb='Settle in';need='energy';}
 else if(has(family,'house barn treehouse greenhouse tower lighthouse bridge shelter workbench')){kind='structure';material='wood';skill='building';verb='Improve';}
 else if(has(family,'robot machine ray ufo rocket submarine jetpack telescope radio tv clock compass vane windmill infinity dna')){kind='machine';material='metal';skill='engineering';verb='Operate';}
 else if(has(family,'piano trumpet drum guitar chimes')){kind='music';material='wood';skill='music';verb='Play a tune';need='social';}
 else if(has(family,'torch fire lantern lamp lava_lamp chandelier lights neon disco spotlight streetlamp moon projector aurora portal blackhole rainbow orb gem wand genie')){kind='light';material='glass';skill='discovery';verb='Activate';}
 else if(item.category==='cosmetic'||item.category==='clothing'){kind='wearable';material='fabric';skill='style';verb='Fit';need='social';}
 else if(item.category==='toy'||has(family,'ball blocks skateboard trampoline slide swing seesaw sandbox car duck frisbee yoyo kite balloon wheel carousel bouncehouse')){kind='toy';material='paint';skill='agility';verb='Play';}
 else if(has(family,'book map paper card frame')){kind='study';material='paper';skill='observation';verb='Study';}
 else if(has(family,'chest cabinet shelf basket barrel')){kind='storage';material='wood';skill='organization';verb='Sort';}
 else if(item.category==='tool'||has(family,'hammer rod')){kind='tool';material='metal';skill='crafting';verb='Practice';}
 else if(item.category==='material'){kind='material';material=/stone|rock|gem|brick|ore/.test(family)?'stone':'wood';skill='crafting';verb='Inspect grain';}
 return {kind,material,skill,verb,need,duration:{comfort:24,study:18,plant:16,structure:24,machine:16,music:18,food:10}[kind]||12};
}
const textures={wood:[':',"'",'-','.'],metal:['.',':','+',':'],fabric:[':',"'",':','.'],leaf:[';',':',"'",'.'],stone:['.',':',"'",'.'],food:['.',"'",':','.'],glass:['.',':',"'",'.'],paper:['-',':','.',"'"],paint:['.',':','.',"'"]};
export function detailItem(base,item,family,time,{motion=true,state={},interaction=null}={}){
 const profile=itemProfile(item||{},family),seed=hash(item?.id||family||''),phase=motion?Math.floor(time*6)%12:0;
 const source=base.art,w=Math.max(...source.map(r=>r.length)),scaleX=1.6,scaleY=1.5;
 const W=Math.ceil(w*scaleX)+6,H=Math.ceil(source.length*scaleY)+6;
 const cells=Array.from({length:H},()=>Array(W).fill(' ')),tones=cells.map(r=>r.map(()=> 'b'));
 const put=(x,y,c,t='b')=>{x=Math.round(x);y=Math.round(y);if(c!==' '&&cells[y]?.[x]!==undefined){cells[y][x]=c;tones[y][x]=t;}};
 const active=Boolean(interaction||state.active),progress=interaction?.progress??((phase+1)/12),working=active&&motion;
 const tint=(c,x,y)=>/[=+#]/.test(c)?'s':/[oO@*<>]/.test(c)?'a':x<w*.25||y<2?'f':'b';
 source.forEach((line,y)=>{
  const left=line.search(/\S/),right=line.trimEnd().length-1;if(left<0)return;
  for(let x=0;x<line.length;x++){
   const c=line[x];if(c===' ')continue;
   const xx=3+Math.round(x*scaleX),yy=3+Math.round(y*scaleY);
   put(xx,yy,c,tint(c,x,y));
   if(x<right&&line[x+1]!==' '&&/[-_=~]/.test(c))put(xx+1,yy,c,tint(c,x,y));
   if(y+1<source.length&&/[|/\\]/.test(c)){
    const next=source[y+1],nx=c==='/'?x-1:c==='\\'?x+1:x;
    if(next[nx]===c&&Math.round((y+1)*scaleY)-Math.round(y*scaleY)>1)put(xx+(c==='/'?-1:c==='\\'?1:0),yy+1,c,tint(c,x,y));
   }
  }
  // Only add material detail inside enclosed original surfaces; open spaces
  // between tree branches, blades or legs remain transparent.
  if(right-left>=5&&/[|(/\\[]/.test(line[left])&&/[|)\]\\/]/.test(line[right])){
   const yy=3+Math.round(y*scaleY);
   for(let x=left+1;x<right;x++)if(line[x]===' '){
    const xx=3+Math.round(x*scaleX),n=(x*19+y*29+seed)%17;
    if(n<4)put(xx,yy,(textures[profile.material]||textures.stone)[n],'s');
    if(Math.round((y+1)*scaleY)-Math.round(y*scaleY)>1&&n===6)put(xx,yy+1,profile.material==='fabric'?':':'.','s');
   }
  }
 });
 // Join adjacent outline marks across the denser grid. This adds new
 // construction cells rather than stretching glyphs or leaving broken edges.
 const contour=c=>Boolean(c&&/[-_=~|/\\().']/ .test(c));
 for(let y=0;y<source.length;y++)for(let x=0;x<source[y].length;x++){
  const c=source[y][x];if(!contour(c))continue;
  for(const [dx,dy] of [[1,0],[0,1],[1,1],[-1,1]]){
   const other=source[y+dy]?.[x+dx];if(!contour(other))continue;
   if(dx&&dy&&(!/[\\/().' ]/.test(c)||!/[\\/().' ]/.test(other)))continue;
   const ax=3+Math.round(x*scaleX),ay=3+Math.round(y*scaleY),bx=3+Math.round((x+dx)*scaleX),by=3+Math.round((y+dy)*scaleY),n=Math.max(Math.abs(bx-ax),Math.abs(by-ay));
   for(let k=1;k<n;k++){const xx=Math.round(ax+(bx-ax)*k/n),yy=Math.round(ay+(by-ay)*k/n);if(cells[yy][xx]===' ')put(xx,yy,dy?(dx<0?'/':dx>0?'\\':'|'):(c==='='?'=':c==='~'?'~':'-'),tint(c,x,y));}
  }
 }
 const fills=[];
 for(let y=0;y<source.length;y++){
  const r=source[y],a=r.search(/\S/),b=r.trimEnd().length-1;
  if(b-a<5||!/[|(/\\[]/.test(r[a])||!/[|)\]\\/]/.test(r[b]))continue;
  const y0=3+Math.round(y*scaleY),y1=Math.min(H-3,3+Math.round((y+1)*scaleY));
  for(let yy=y0;yy<y1;yy++){
   const left=3+Math.round(a*scaleX),right=3+Math.round(b*scaleX);fills.push({x:left,y:yy,w:right-left+1});
   for(let xx=left+1;xx<right;xx++)if(cells[yy][xx]===' '){
    const n=(xx*13+yy*7+seed)%23;if(n<5)put(xx,yy,(textures[profile.material]||textures.stone)[n%4],'s');
   }
  }
 }
 const cx=Math.floor(W/2),bottom=H-3,top=3;
 // Separate mechanical constructions; every family retains its own contour.
 if(working){
  if(profile.kind==='water')for(let k=0;k<8;k++)put(cx+Math.sin(k*2+phase)*k,top+((k+phase)%Math.max(2,H-4)),k%2?'|':':','w');
  else if(profile.kind==='plant'){for(let k=0;k<4;k++)put(cx+4+k,top+((phase+k)%5),'\'', 'w');put(cx,bottom-2,';', 'f');}
  else if(profile.kind==='music'){put(cx-4,top-1-(phase%2),'d','a');put(cx+5,top-2+phase%3,'b','a');}
  else if(profile.kind==='machine'){put(cx,Math.floor(H*.55),'|/-\\'[phase%4],'a');for(let k=0;k<3;k++)put(cx+k*2-2,bottom-3,(phase+k)%3?'o':'*','a');}
  else if(profile.kind==='storage'){for(let x=4;x<W-4;x++)put(x,top-1-Math.round(Math.sin(progress*Math.PI)*2),'-','f');put(cx,top-2,'o','a');}
  else if(profile.kind==='light'){for(let k=0;k<6;k++)put(cx+Math.cos(k+phase)*Math.min(8,W/3),H/2+Math.sin(k+phase)*H/3,k%2?'*':'+','a');}
  else if(profile.kind==='food'){for(let k=0;k<5;k++)put(cx+4+k,bottom-1-(phase+k)%3,'.','a');}
  else if(profile.kind==='comfort'){put(cx+2,top-1-(phase%3),'z','a');}
  else if(profile.kind==='structure'||profile.kind==='tool'){put(W-5,Math.floor(H*.4)+phase%3,'T','a');put(W-4,Math.floor(H*.4)+2,'*','f');}
  else if(profile.kind==='study'){for(let x=5;x<W-5;x+=4)put(x,H/2+Math.sin(phase/3+x)*2,'~','f');}
  else if(profile.kind==='wearable'){for(let x=4;x<W-4;x+=4)put(x,bottom-2,phase%2?':':"'",'a');}
  else{const scan=3+Math.floor(phase/11*(W-7));put(scan,Math.max(1,top-1),'o','a');put(scan+1,top,'/','f');put(cx+4,top-2,phase%2?'+':'.','a');}
 }
 // Weathering, repairs and affectionate repeated use are visible in the object.
 if((state.wetness||0)>.2)for(let k=0;k<Math.ceil(state.wetness*8);k++)put(3+(seed+k*7)%(W-6),3+(phase+k*3)%(H-4),"'",'w');
 if((state.dirt||0)>.3)for(let k=0;k<Math.ceil(state.dirt*8);k++)put(3+(seed+k*5)%(W-6),bottom-1,'.','s');
 if((state.condition??1)<.5)put(cx,bottom-3,'/','s');
 if(state.bond>.6)put(cx-1,Math.max(3,bottom-2),'*','a');
 const art=cells.map(r=>r.join('')),out={...base,...profile,art,tones:tones.map(r=>r.join('')),width:W,groundRow:H,anchorX:W/2,detailScale:1/scaleX,detail:true,fills,
  sway:working&&['toy','plant','comfort','wearable'].includes(profile.kind)?Math.sin(phase*Math.PI/6)*.065:base.sway,
  lift:working&&profile.kind==='toy'?Math.abs(Math.sin(phase*Math.PI/6))*1.2:base.lift,active,phase};
 return out;
}
