import {projectSceneryCell} from './scenery-projection.mjs';
import {castleActorPhysical,sharedCastleRecord,sharedCastleSource,eggCaregiverScene} from './castle-care.mjs';
import {carnivalOccupants} from './carnival-routines.mjs';
import {playkitPose,PLAYKIT_ROUTINES} from './playkit-routines.mjs';
import {WeatherDrift,wrap} from './weather-wind.mjs';
import {architecturePose,ARCHITECTURE_ROUTINES} from './architecture-routines.mjs';
import {groundPose,GROUND_ROUTINES} from './ground-routines.mjs';
import {textilePose,TEXTILE_ROUTINES} from './textile-routines.mjs';
import {sameInstance,physicalState} from './physical-objects.mjs';
import {musicOccupants,musicPose,MUSIC_SCORES} from './music-performances.mjs';
import {botanicalOccupants,BOTANICAL_ROUTINES} from './botanical-routines.mjs';
import { eventModel } from './event-art.mjs';
import { storyModel } from './story-art.mjs';
import { sceneLight } from './scene-lighting.mjs';
import { Grid,W,H,C,M,hash,seedOf,clamp,lerp,palette } from './ultra-grid.mjs';
import { DOCK,LANTERN } from './ultra-art.mjs';

import { itemSprite,itemWorldScale } from './ultra-items.mjs';
import { characterSprite } from './ultra-characters.mjs';
import {residenceStage} from './residence-stage.mjs';
import {actorPerformance} from './performances.mjs';
import {lightingPose,LIGHTING_ROUTINES} from './lighting-routines.mjs';
import {creativePose,CREATIVE_ROUTINES} from './creative-routines.mjs';
import {keepsakePose,KEEPSAKE_ROUTINES} from './keepsake-routines.mjs';
import {wonderPose,WONDER_ROUTINES} from './wonder-routines.mjs';
import {repPose,REP_ROUTINES,REP_OBJECTS,applyObjectPose} from './repertoire-routines.mjs';
import {playdateStage} from './playdates.mjs';
import {playgroundStage} from './playground-stage.mjs';
import {waterStage} from './water-routines.mjs';
import {seatOccupants} from './seating-routines.mjs';
import {residentEnvelope} from './resident-envelope.mjs';
import {homeScenery} from './habitat-ground.mjs';
import {region,waterAt,bankOnScreen} from './terrain.mjs';
import * as LANDMARK_ART from './ultra-art.mjs';

const WATER_BIOMES=new Set(['pond','riverside','beach','swamp']);
const choice=(s,n)=>s[Math.floor(n*s.length)%s.length];
export class LivingWorld {
  constructor(){this.grid=new Grid();this.water=new Uint8Array(W*H);this.shore=new Int16Array(W);this.duckPosition=null;this.lastLocation='';this.lastTime=0;this.wind=new WeatherDrift();}
  project(scene,x,y){const c=scene.camera||{x:0,y:0,w:132,h:42};return [24+(x-c.x)/c.w*(W-48),46+(y-c.y)/c.h*47];}
  sceneryLayer(id,y,draw){
    // Keep the composite for reflections/cache, and retain exact ink cells for
    // painter-order occlusion. Transparent gaps never erase an actor behind it.
    const base=this.grid,layer=new Grid(),touched=new Set();layer.clear();
    const put=layer.put.bind(layer);
    layer.put=(x,y,...rest)=>{put(x,y,...rest);x=Math.round(x);y=Math.round(y);if(x>=0&&y>=0&&x<W&&y<H)touched.add(y*W+x);};
    this.grid=layer;
    try{draw();}finally{this.grid=base;}
    const cells=[...touched].map(i=>[i,layer.chars[i],layer.colors[i],layer.materials[i]]);
    for(const [i,ch,color,material] of cells){base.chars[i]=ch;base.colors[i]=color;base.materials[i]=material;}
    const record={id,y,scenery:true,cells};
    (this.scenery||=[]).push(record);
    return record;
  }
  physicalSceneryLayer(scene,id,depth,draw){
    // Capture canonical ink without viewport clipping; offscreen branches must
    // retain their real extent when a wider display camera reveals them.
    const base=this.grid,layer=new Grid(),ink=new Map();
    layer.put=(x,y,ch,color,material=M.ambient)=>{x=Math.round(x);y=Math.round(y);const c=typeof ch==='number'?ch:ch.charCodeAt(0);ink.set(x+','+y,[x,y,c>=32&&c<=126?c:63,color,material]);};
    this.grid=layer;try{draw();}finally{this.grid=base;}
    const nativeCells=[...ink.values()],projectedCells=[],composite=new Map();
    for(const [x,y,ch,color,material]of nativeCells){
      const r=projectSceneryCell(scene.camera,x,y);projectedCells.push([r.x,r.y,r.w,r.h,ch,color,material]);
      for(let py=Math.max(0,Math.floor(r.y));py<Math.min(H,Math.ceil(r.y+r.h));py++)for(let px=Math.max(0,Math.floor(r.x));px<Math.min(W,Math.ceil(r.x+r.w));px++)composite.set(py*W+px,[py*W+px,ch,color,material]);
    }
    const cells=[...composite.values()];for(const [i,ch,color,material]of cells){base.chars[i]=ch;base.colors[i]=color;base.materials[i]=material;}
    const record={id,y:projectSceneryCell(scene.camera,0,depth).y,scenery:true,cells,nativeCells,projectedCells};(this.scenery||=[]).push(record);return record;
  }
  sky(s,t,seed){
    const g=this.grid,light=sceneLight(s),night=light.night;
    for(let y=0;y<45;y++)for(let x=0;x<W;x++){
      const r=hash(x,y,seed);
      if(r<.025+y*.0018)g.put(x,y,choice('.`:',r*31),C.sky);
      if(night&&y<30&&r>.997)g.put(x,y,Math.sin(t*1.8+x)>0?'+':'.',C.star);
    }
    const sunX=light.sunX;
    if(!/storm|rain|fog/.test(s.weather)){
      g.ellipse(sunX,13,9,5,night?'.':'*',night?C.cloud:C.goldDark);
      g.ellipse(sunX-1,12,7,4,night?'o':'#',night?C.white:C.goldLight);
      if(night)g.ellipse(sunX+3,10,7,4,' ',C.bg);
      else for(let k=0;k<14;k++){const a=k*Math.PI/7;g.put(sunX+Math.cos(a)*13,13+Math.sin(a)*7,'.',C.lamp);}
    }
    // Layered, slowly drifting cloud banks; density comes from characters alone.
    for(let n=0;n<6;n++){
      const cx=((n*57+t*(.45+n*.025)+hash(n,1,seed)*30)%(W+70))-35, cy=6+hash(n,2,seed)*17;
      for(let y=-5;y<=5;y++)for(let x=-29;x<=29;x++){
        const edge=1-(x/30)**2-(y/5)**2;
        if(edge>hash(x+n*9,y,seed)*.45){
          const c=edge>.55?'~':edge>.25?'-':'.';
          g.put(cx+x,cy+y,c,y>1?C.sky:C.cloud);
        }
      }
    }
    if(s.particles!==false&&!/storm|snow/.test(s.weather))for(let i=0;i<5;i++){
      const x=(t*(2+i*.3)+i*49)%(W+10)-5,y=15+i*2+Math.sin(t*.7+i);
      g.text(x,y,Math.sin(t*5+i)>0?'v v':'- -',night?C.sky:C.cloud);
    }
  }
  hills(s,t,seed){
    const g=this.grid,mountain=s.biome==='mountains',cave=/cave/i.test(s.location);
    for(let layer=0;layer<3;layer++)for(let x=0;x<W;x++){
      const offset=(s.camera?.x||0)*(.12+layer*.12);
      const u=x+offset, ridge=(mountain?29:33)+layer*6-Math.sin(u*.027+seed+layer)*5-Math.sin(u*.071+layer)*3;
      const peak=mountain?Math.abs(Math.sin(u*.029+layer))*17:0;
      for(let y=Math.floor(ridge-peak);y<50+layer*4;y++){
        const r=hash(x,y,seed+layer),d=y-ridge+peak;
        g.put(x,y,choice(layer===0?' .:':'.,:;i',r),layer===0?C.far:layer===1?C.hill:C.leafDark);
        if(mountain&&d<3&&r>.3)g.put(x,y,choice('/^.`',r),C.ice);
      }
    }
    // Fine distant conifer line gives the horizon a readable silhouette.
    for(let n=0;n<36;n++){
      const x=n*7+hash(n,4,seed)*4,h=4+hash(n,9,seed)*8,y=44+Math.sin(x*.045)*3;
      for(let j=0;j<h;j++)g.text(x-j*.28,y-h+j,'/'.padEnd(1+Math.floor(j*.6),':')+'\\',C.hill);
    }
    if(cave){
      for(let x=0;x<W;x++){
        const depth=10+hash(x>>2,4,seed)*17;
        for(let y=0;y<depth;y++)g.put(x,y,choice(' /|:;',hash(x,y,seed)),y<depth-3?C.shadow:C.far);
      }
    }
  }
  terrain(s,t,seed){
    const g=this.grid,b=s.biome;
    this.water.fill(0);
    for(let x=0;x<W;x++){
      const camera=s.camera||{x:0,y:0,w:132,h:42},wx=camera.x+(x-24)/192*camera.w;
      const bank=bankOnScreen(s.location,x,camera);
      this.shore[x]=bank;
      for(let y=43;y<H;y++){
        const r=hash(x,y,seed),r2=hash(x>>2,y>>1,seed),depth=(y-43)/69;
        const wy=camera.y+(y-46)/47*camera.h;
        const wet=waterAt(s.location,wx,wy,b);
        if(wet){
          this.water[y*W+x]=1;
          const wave=Math.sin(x*.19+t*1.6+y*.6)+Math.sin(x*.049-y*.42+t*.8);
          const glitter=wave>1.45&&r>.38;
          g.put(x,y,glitter?'=':wave>.2?'~':r>.75?'-':'.',glitter?C.waterLight:wave>.2?C.water:C.waterDark);
          if(Math.abs(x-(45+(s.hour-6)*10))<5+(y-bank)*.4&&r>.52)g.put(x,y,'-',C.glint);
          if(y===Math.ceil(bank))g.put(x,y,'~',C.waterLight);
        }else{
          const path=(b==='garden'||b==='urban')&&Math.abs(x-(W/2+Math.sin(y*.08)*12))<5+depth*19;
          const ch=path?choice(' .:_',r):choice(depth>.5?' .,:;\'`':' .,:',r);
          g.put(x,y,ch,path?C.bark:r2>.65?C.ground:C.groundDark);
          if(r>.96&&!path){const breeze=Math.sin(t*1.5+x*.1+y*.03);g.put(x,y,b==='beach'?'.':b==='mountains'?'^':breeze>.2?'/':breeze<-.2?'\\':'|',C.grass);}
          if(r>.997&&b!=='mountains'&&b!=='urban')g.put(x,y,'*',s.season==='winter'?C.white:C.flower);
          if(WATER_BIOMES.has(b)&&y===Math.floor(bank))g.put(x,y,'_',C.barkLight);
        }
      }
    }
  }
  tree(x,base,height,kind,t,seed,foreground=false,id='tree'){
    this.sceneryLayer(id,base+2,()=>this.drawTree(x,base,height,kind,t,seed,foreground));
  }
  drawTree(x,base,height,kind,t,seed,foreground=false){
    const g=this.grid,top=base-height,wide=kind==='pine'?height*.22:height*.38;
    const bark=foreground?C.bark:C.barkDark,leaf=foreground?C.leaf:C.leafDark;
    // Tapered trunks with roots, knotholes, branching and bark hatching.
    for(let y=top+height*.3;y<=base;y++){
      const trunk=2+(y-top)/height*2;
      for(let dx=-trunk;dx<=trunk;dx++)g.put(x+dx,y,choice('|:;/ ',hash(dx,y,seed)),dx<0?bark:C.barkDark,M.wood);
    }
    for(let n=0;n<5;n++){
      const bx=x+(n-2)*wide*.5,by=top+height*(.3+hash(n,6,seed)*.28);
      g.line(x,base-height*.25,bx,by,n<2?'/':'\\',bark,M.wood);
      g.line(x,base-2,x+(n-2)*5,base+2,'_',bark,M.wood);
    }
    g.text(x-1,base-height*.25,'(@)',bark,M.wood);
    if(kind==='pine'){
      for(let y=0;y<height*.76;y++){
        const w=2+y*.34+(y%8)*.25;
        for(let dx=-w;dx<=w;dx++)if(hash(dx,y,seed)>.14)g.put(x+dx,top+y,choice('/\\;:^',hash(dx,y,seed)),dx<0?C.leaf:leaf,M.foliage);
      }
    }else{
      // Overlapping lobes produce a broad, hand-etched canopy silhouette.
      for(let n=0;n<8;n++){
        const cx=x+(hash(n,3,seed)-.5)*wide*1.4,cy=top+hash(n,4,seed)*height*.32+7;
        const rx=wide*(.5+hash(n,5,seed)*.35),ry=height*.16;
        const sway=Math.sin(t*.7+n)*.6;
        for(let dy=-ry;dy<=ry;dy++)for(let dx=-rx;dx<=rx;dx++){
          const d=(dx/rx)**2+(dy/ry)**2,r=hash(dx+n*27,dy,seed);
          if(d<1&&r>.1){
            const color=r>.83&&dy<0?C.leafLight:r>.45?C.leaf:leaf;
            g.put(cx+dx+sway,cy+dy,choice('.,:;o*',r),color,M.foliage);
          }
        }
      }
      if(kind==='willow')for(let n=0;n<29;n++){
        const u=(n/28-.5)*wide*1.9,bend=Math.sin(t*.75+n*.3)*1.4;
        const start=top+height*.3, length=height*(.2+hash(n,8,seed)*.42);
        for(let j=0;j<length;j++)g.put(x+u+bend*(j/length),start+j,j%3===0?';':j%3===1?'|':',',j>length-3?C.leafLight:leaf,M.foliage);
      }
    }
  }
  reflected(t){
    const g=this.grid;
    for(let x=0;x<W;x++)for(let y=this.shore[x]+1;y<H;y++){
      if(!this.water[y*W+x])continue;
      const sourceY=Math.floor(this.shore[x]-(y-this.shore[x])*.7),sourceX=clamp(Math.round(x+Math.sin(t*1.4+y*.6)*2),0,W-1);
      if(sourceY<0)continue;
      const idx=sourceY*W+sourceX,ch=g.chars[idx],col=g.colors[idx];
      if(col>=C.leafDark&&col<=C.barkLight&&ch!==32&&hash(x,y)>.36)g.put(x,y,y%3===0?'~':ch,col===C.leafLight?C.water:C.waterDark);
    }
  }
  palm(x,base,height,t,seed){
    const g=this.grid,top=base-height;
    for(let y=0;y<height;y++){
      const lean=Math.sin(y/height*1.5)*7;
      g.text(x+lean,base-y,y%3===0?'[==]':'|::|',y%3===0?C.barkLight:C.bark,M.wood);
    }
    const crown=x+7;
    for(let n=0;n<9;n++){
      const side=n%2?-1:1,reach=13+hash(n,1,seed)*15,drop=-7+hash(n,2,seed)*20;
      for(let j=0;j<reach;j++){
        const u=j/reach,px=crown+side*j,py=top+drop*u-9*Math.sin(u*2.2)+Math.sin(t*.7+n)*u;
        g.put(px,py,side<0?'/':'\\',C.leafLight,M.foliage);
        if(j%2===0){g.put(px,py+1,'|',C.leaf,M.foliage);g.put(px-side,py+2,side<0?'\\':'/',C.leaf,M.foliage);}
      }
    }
    g.text(crown-2,top+1,'(o)(o)',C.barkLight,M.wood);
  }
  waterfall(x,y,height,t){
    const g=this.grid;
    for(let j=0;j<height;j++)for(let i=-7;i<=7;i++){
      const edge=Math.abs(i)>5;
      g.put(x+i,y+j,edge?choice(':;#',hash(i,j)):choice('|!: .',hash(i,Math.floor(j-t*16))),
        edge?C.barkDark:i%3===0?C.glint:C.waterLight);
    }
    for(let n=0;n<15;n++){
      const a=n*.5+t,r=5+(t*4+n)%8;
      g.put(x+Math.cos(a)*r,y+height+Math.sin(a)*3,n%3?'o':'.',C.mist);
    }
    this.ripples(x,y+height,t,C.water);
  }
  pondLife(s,t,seed){
    const g=this.grid;
    if(['pond','swamp'].includes(s.biome))for(let n=0;n<12;n++){
      const x=15+hash(n,31,seed)*(W-30),bank=this.shore[x|0],y=bank+3+hash(n,32,seed)*Math.max(0,H-bank-7);
      g.text(x,y,Math.sin(t+n)>.1?'(__,)':'(,,_)',C.leaf);
      if(n%4===0){g.put(x+2,y-1,'*',s.biome==='swamp'?C.crystal:C.flower);g.put(x+2,y,'.',C.goldLight);}
    }
    if(s.particles!==false&&WATER_BIOMES.has(s.biome)&&s.season!=='winter')for(let n=0;n<3;n++){
      const x=(n*87+t*3)%(W-30)+10,y=88+n*7+Math.sin(t*.5+n)*2;
      if(this.water[(y|0)*W+(x|0)])g.text(x,y,Math.sin(t*1.3+n)>0?'><>':'><=',C.water);
    }
  }
  regionFeature(s,f,t,seed){
    const [x,y]=this.project(s,(f.x-24)*132/192,(f.y-46)*42/47);
    if(f.kind==='tree'){this.tree(x,y,f.height,f.tree,t,seed+(f.seed||0),f.foreground!==false,f.id);return;}
    this.sceneryLayer(f.id,y,()=>{
      const g=this.grid,color=C[f.color]??C.barkLight;
      if(f.kind==='palm'){this.palm(x,y,f.height,t,seed+(f.seed||0));return;}
      if(f.kind==='waterfall'){this.waterfall(x,y-f.height,f.height,t);return;}
      if(f.kind==='fountain'){
        for(let n=0;n<8;n++)for(let j=0;j<18;j++){
          const u=j/17;g.put(x+(n-3.5)*u*3,y-6-12*Math.sin(u*Math.PI),choice('|:.',hash(n,Math.floor(j+t*10))),C.waterLight);
        }
        g.text(x-10,y-1,'(___________________)',C.barkLight);g.text(x-8,y,'\\_______________/',C.bark);return;
      }
      const left=x-f.drawWidth/2,top=y-f.drawHeight+1;
      const ink=f.art==='ARCH'?ch=>ch==='*'?C.flower:ch==='o'?C.goldLight:color:
        f.art==='FLOWERS'?ch=>ch==='@'?C.goldLight:'()'.includes(ch)?C.flower:C.grass:
        f.art==='MUSHROOM'?ch=>ch==='o'?C.white:color:color;
      g.art(left,top,LANDMARK_ART[f.art],ink);
      if(f.kind==='mill'){
        const mx=left+13,my=top+4;
        for(let n=0;n<4;n++)for(let r=1;r<15;r++){
          const a=t*.25+n*Math.PI/2,px=mx+Math.cos(a)*r,py=my+Math.sin(a)*r*.55;
          g.put(px,py,Math.abs(Math.sin(a))>.7?'|':'=',C.barkLight);
          if(r>7)g.put(px+Math.sin(a)*2,py-Math.cos(a),'#',C.bark);
        }
        g.put(mx,my,'@',C.goldLight);
      }
      if(f.kind==='dock'){
        g.art(left+18,top-9,LANTERN,ch=>ch==='*'?C.lamp:C.barkLight);
        g.line(left+26,top-2,left+26,top+1,'|',C.barkLight,M.wood);
      }
    });
  }
  landmarks(s,t,seed){
    const g=this.grid,b=s.biome,features=region(s.location,s.biome).features;
    if(s.location==='Home Pond'){
      for(const f of homeScenery.filter(f=>f.kind==='willow')){
        const x=24+f.x*192/20,y=46+f.y*47/12;
        this.physicalSceneryLayer(s,f.id,y+2,()=>this.drawTree(x,y,f.height,'willow',t,seed+(f.id==='east_willow'?13:0),true));
      }
    }
    for(const f of features.filter(f=>f.kind==='tree'||f.kind==='palm'))this.regionFeature(s,f,t,seed);
    this.reflected(t);this.pondLife(s,t,seed);
    if(s.location==='Home Pond'){
      const f=homeScenery.find(f=>f.kind==='dock'),x=24+f.x*192/20,y=46+f.y*47/12;
      this.physicalSceneryLayer(s,'pond_dock',y+3,()=>{
        this.grid.art(x-18,y-4,DOCK,(ch,x,y)=>y<4?C.barkLight:C.bark);
        this.grid.art(x,y-13,LANTERN,ch=>ch==='*'?C.lamp:C.barkLight);
        this.grid.line(x+8,y-6,x+8,y-3,'|',C.barkLight,M.wood);
      });
    }
    for(const f of features.filter(f=>f.kind!=='tree'&&f.kind!=='palm'))this.regionFeature(s,f,t,seed);
    const detail=(x,y,text,color)=>{const [px,py]=this.project(s,(x-24)*132/192,(y-46)*42/47);g.text(px,py,text,color);};
    if(b==='garden')for(let n=0;n<5;n++)for(let j=0;j<5;j++)detail(66+n*8,66+j*6,'{v}',j%2?C.leafLight:C.leaf);
    if(b==='riverside'&&s.location!=='Waterfall')for(let n=0;n<20;n++)detail(12+hash(n,1,seed)*210,57+hash(n,2,seed)*13,'(._)',C.barkLight);
    if(b==='beach')for(let n=0;n<16;n++)detail(n*16+hash(n,4,seed)*8,58+hash(n,3,seed)*14,'(@)',C.barkLight);
    if(s.location==='Rooftop Garden')for(let x=5;x<W-5;x++)detail(x,65,x%7?'_':'|',C.barkLight);
    // Seasonal details around the banks and paths, rooted in stable coordinates.
    for(let n=0;n<14;n++){
      const [x,y]=this.project(s,(hash(n,88,seed)*W-24)*132/192,(55+hash(n,87,seed)*43-46)*42/47);
      if(!this.water[(y|0)*W+(x|0)]){
        if(s.season==='winter')g.text(x,y,'_*_',C.white);
        else if(s.season==='fall')g.text(x,y,hash(n,5)>.5?'{}':'<>',C.barkLight);
      }
    }
  }
  ripples(x,y,t,color=C.waterLight){
    for(let n=0;n<3;n++){
      const r=(t*8+n*9)%27;
      for(let a=0;a<Math.PI*2;a+=.15){
        const px=x+Math.cos(a)*r,py=y+Math.sin(a)*r*.2;
        if(hash(a*100|0,n)>.25)this.grid.put(px,py,'~',color);
      }
    }
  }
  actor(s,t,x,y,duck,visitor=false){
    if(duck.away||duck.hidden)return;
    const state=duck.state||'idle';
    if(/swim|float|splash|diving/.test(state))this.ripples(x,y,t);
    const performance=!visitor&&eggCaregiverScene(s)?null:actorPerformance(s,visitor?duck.id:'cheese');
    const sprite=characterSprite({...duck,motion:s.motion!==false,performance,...(performance?{facing:performance.role==='a'}:{})},t,visitor);
    this.characters.push({...sprite,x,y,cheese:!visitor});
  }
  actors(s,t,dt){
    const g=this.grid,actors=[],seated=seatOccupants(s),musicians=musicOccupants(s);
    for(const item of [...(s.structures||[]),...(s.items||[])]){
      const [x,y]=this.project(s,item.x,item.y);
      actors.push({y,draw:()=>{
        const plan=s.living?.plan,destination=plan?.residence?.destination||plan?.destination;
        const matches=dest=>dest&&Math.abs(item.x-dest[0])+Math.abs(item.y-dest[1])<2;
        const occupants=(s.living?.minds?.residences||[]).filter(r=>r.id===item.id&&sameInstance(item,r)&&matches(r.destination));
        const owned=plan?.target===item.id&&sameInstance(item,plan)&&(!destination||matches(destination));
        let interaction=owned?plan:null;
        if(occupants.some(r=>r.phase!=='approach'))interaction=interaction||{phase:'act',kind:'rest'};
        if(interaction&&occupants.length+(owned&&plan.residence?1:0)>1)interaction={...interaction,shared:true};
        if(interaction&&occupants.length)interaction={...interaction,nest_visitors:occupants.filter(r=>r.phase==='inside'&&r.routine&&!r.routine.done)};
        const sitters=seated.filter(r=>r.id===item.id&&sameInstance(item,r)&&matches(r.destination)&&r.phase!=='approach');
        if(sitters.length)interaction={...(interaction||{phase:'act'}),seat_occupants:sitters};
        const music=musicians.filter(r=>r.id===item.id&&sameInstance(item,r)&&matches(r.destination)&&r.phase==='inside').map(r=>{const p=musicPose(r.id,r.score,s.motion!==false);return p&&{...p,slot:r.slot};}).filter(Boolean);
        const light=owned&&plan.light_work?lightingPose(plan.light_work,s.motion!==false):null;
        const playkit=owned&&plan.playkit_work&&plan.phase!=='approach'?playkitPose(plan.playkit_work,s.motion!==false):null;
        const architecture=owned&&plan.architecture_work&&plan.phase!=='approach'?architecturePose(plan.architecture_work,s.motion!==false):null;
        const ground=owned&&plan.ground_work&&plan.phase!=='approach'?groundPose(plan.ground_work,s.motion!==false):null;
        const textile=owned&&plan.textile_work&&plan.phase!=='approach'?textilePose(plan.textile_work,s.motion!==false):null;
        const creative=owned&&plan.creative_work&&plan.phase!=='approach'?creativePose(plan.creative_work,s.motion!==false):null;
        const keepsake=owned&&plan.keepsake_work?keepsakePose(plan.keepsake_work,s.motion!==false):null;
        const wonder=owned&&plan.wonder_work&&plan.phase!=='approach'?wonderPose(plan.wonder_work,s.motion!==false):null;
        const rep=owned&&plan.rep_work&&plan.phase==='act'?repPose(plan.rep_work,s.motion!==false):null;
        this.objects.push(applyObjectPose({...itemSprite(item.id,t,{pose:{music,light,keepsake,wonder,creative,textile,ground,architecture,playkit},motion:s.motion!==false,context:s,originalArt:item.art,state:physicalState(s,item),interaction}),item:true,instance:item.instance,x,y,worldPosition:[item.x,item.y],...(item.id==='bounce_house'?{physicalCastle:{origin:[item.x,item.y],camera:{...(s.camera||{x:0,y:0,w:132,h:42})}}}:{}),scale:itemWorldScale(item.id)},rep));
      }});
    }
    if(s.visitor){const [x,y]=this.project(s,s.visitor.x,s.visitor.y);actors.push({y,draw:()=>this.actor(s,t+2,x,y,{stage:'adult',state:'idle',facing:false,...s.visitor},true)});}
    for(const event of s.events||[]){
      const [x,y]=this.project(s,event.x,event.y);
      if(event.art?.length)this.characters.push({...eventModel(event,t,s.motion!==false),x,y});
      for(const [px,py,char] of event.particles||[]){const [xx,yy]=this.project(s,px,py);g.put(xx,yy,/[\x20-\x7e]/.test(char)?char:'*',C.goldLight);}
    }
    if(s.rareVisitor){const visitor=s.rareVisitor,[x,y]=this.project(s,visitor.x,visitor.y);this.actor(s,t,x,y,{stage:'adult',state:'idle',...visitor},true);}
    const living=s.living;
    if(living&&s.location==='Home Pond'){
      const species=living.ecology.insects>.6?'dragonfly':living.ecology.birds>.55?'robin':living.ecology.fish>.65?'fish':null;
      if(species){const x=30+Math.sin(t*.1)*8,y=species==='fish'?78:68;this.characters.push({...eventModel({id:species,asset:species},t,s.motion!==false),x,y,scale:.55});}
      for(const place of living.installations||[]){
        const [x,y]=this.project(s,place.x,place.y);
        const plot=place.role==='garden'?(living.garden||[]).find(p=>'garden:'+p.id===place.instance):null;
        const project=place.role==='project'?(living.projects||[]).find(p=>'project:'+p.id===place.instance):null;
        const state=plot?{wetness:plot.water,growth:plot.health}:{active:project?.stage===3};
        this.objects.push({...itemSprite(place.id,t,{motion:s.motion!==false,context:s,state}),item:true,
          x,y,worldPosition:[place.x,place.y],instance:place.instance,scale:itemWorldScale(place.id)*place.scale,
          installation:true,project:project?.id});
        if(plot?.plant)this.sceneryLayer(place.instance+':soil',-1000,()=>this.grid.art(x-6,y-1,
          ['.------------.',"'------------'"],C.bark));
        if(project&&project.stage<3)g.art(x-5,y+1,['[ '+project.stage+' / 3 ]'],C.barkLight);
      }
      if(living.story){
        const actor=s.storyActor?.storyId===living.story.id?s.storyActor:{x:48,y:24,state:'signature'};
        const performance=actorPerformance(s,'story:pip');
        const [x,y]=this.project(s,actor.x,actor.y),model=storyModel(living.story,{...actor,performance,...(performance?{facing:performance.role==='a'}:{})},t,s.motion!==false);
        this.characters.push({...model,x,y});
        g.put(x,y-13,'!',C.goldLight);
      }
    }
    const target=this.project(s,s.duck.x,s.duck.y);
    const cameraKey=JSON.stringify(s.camera||null);
    if(s.motion===false||s.living?.plan?.carnival_work?.physical_pilot||eggCaregiverScene(s)||!this.duckPosition||s.location!==this.lastLocation||cameraKey!==this.duckCameraKey)this.duckPosition=target;
    else this.duckPosition=this.duckPosition.map((v,i)=>lerp(v,target[i],clamp(dt*12,0,1)));
    this.duckCameraKey=cameraKey;
    const [x,y]=this.duckPosition;
    let state=s.duck.state;
    const plan=s.living?.plan;
    if(plan&&!plan.paused&&plan.phase==='act'){const poses={rest:'sleeping',forage:'eating',practice:'dancing',restore:'preening',garden:'preening',observe:'idle',project:'preening',share:'quacking'};state=poses[plan.kind]||state;}
    if(Math.abs(x-target[0])+Math.abs(y-target[1])>.7&&state==='idle')state='walking';
    if(plan&&!plan.in_place&&(plan.location??s.location)===s.location&&!plan.instance&&(!plan.paused||plan.portable||plan.keepsake_work||plan.creative_work||plan.textile_work||plan.ground_work||plan.playkit_work)&&(['prepare','act','settle'].includes(plan.phase)||plan.portable?.deployed)&&plan.kind==='item'&&![...(s.items||[]),...(s.structures||[])].some(i=>i.id===plan.target&&sameInstance(i,plan))){
      const playkit=plan.playkit_work?playkitPose(plan.playkit_work,s.motion!==false):null;
      const ground=plan.ground_work?groundPose(plan.ground_work,s.motion!==false):null;
      const textile=plan.textile_work?textilePose(plan.textile_work,s.motion!==false):null,keepsake=plan.keepsake_work?keepsakePose(plan.keepsake_work,s.motion!==false):null,creative=plan.creative_work?creativePose(plan.creative_work,s.motion!==false):null,origin=plan.playkit_work?.origin||plan.keepsake_work?.origin||plan.creative_work?.origin||plan.textile_work?.origin||plan.ground_work?.origin;
      const [ox,oy]=plan.portable?.object?this.project(s,...plan.portable.object):origin?this.project(s,...origin):[x,y];
      this.objects.push({...itemSprite(plan.target,t,{pose:{keepsake,creative,textile,ground,playkit},motion:s.motion!==false,context:s,state:s.living.objects[plan.target],interaction:plan}),item:true,x:ox+(plan.portable?0:7),y:oy,worldPosition:plan.portable?.object,scale:itemWorldScale(plan.target),portable:true});
    }
    actors.push({y,draw:()=>this.actor(s,t,x,y,{...s.duck,state})});
    actors.sort((a,b)=>a.y-b.y).forEach(a=>a.draw());
    const cheese=this.characters.find(c=>c.cheese),residence=residenceStage(plan?.rep_work?null:plan,this.objects,cheese);
    const bathing=waterStage(plan?.rep_work?null:plan,this.objects,cheese,s.duck.stage,s.motion!==false);
    if(bathing){
      const performance={kind:'water',routine:plan.water_routine,motion:s.motion!==false};
      const character={...characterSprite({...s.duck,state:'idle',facing:bathing.pose.facing,performance},t),x:cheese.x,y:cheese.y,cheese:true};
      bathing.home.bather={character,seat:bathing.seat,inside:bathing.inside,pose:bathing.pose,immersed:bathing.immersed};
      this.characters=this.characters.filter(c=>c!==cheese);
    }
    if(residence){
      const routine=plan.phase==='act'&&!plan.residence.routine?.done?plan.residence.routine:null;
      const resident=routine?{...characterSprite({...s.duck,state:'idle',facing:true,performance:{kind:'nest',routine,motion:s.motion!==false}},t),x:cheese.x,y:cheese.y,cheese:true}:residence.inside<.99?{...characterSprite({...s.duck,state:'walking'},t),x:cheese.x,y:cheese.y,cheese:true}:cheese;
      residence.home.occupant={character:resident,inside:residence.inside,slot:plan.residence.slot||0,key:'cheese'};
      residence.home.occupants=[residence.home.occupant];
      this.characters=this.characters.filter(c=>c!==cheese);
    }
    for(const r of living?.minds?.residences||[]){
      if(r.phase==='approach')continue;
      const actorId=r.actor==='story:pip'?'story:lost_duckling':r.actor;
      const original=this.characters.find(c=>c.id===actorId);
      const home=this.objects.find(o=>o.id===r.id&&sameInstance(o,r)&&o.worldPosition?.every((n,i)=>Math.abs(n-r.destination[i])<1.1));
      if(!home?.anchors||!original)continue;
      const source=s.visitor?.id===actorId?s.visitor:s.rareVisitor?.id===actorId?s.rareVisitor:{...s.storyActor,id:actorId,castId:'lost_duckling',name:'Pip',stage:'duckling'};
      const routine=r.phase==='inside'&&!r.routine?.done?r.routine:null;
      const character=routine?{...characterSprite({...source,state:'idle',facing:r.slot===0,performance:{kind:'nest',routine,motion:s.motion!==false}},t,true),x:original.x,y:original.y,story:original.story}:original;
      const inside=r.phase==='inside'?1:r.phase==='enter'?clamp(r.elapsed/3,0,1):clamp(1-r.elapsed/3,0,1);
      (home.occupants||=[]).push({character,inside,slot:r.slot,key:r.actor});
      this.characters=this.characters.filter(c=>c!==original);
    }
    for(const r of seated){
      if(r.phase==='approach')continue;
      const actorId=r.actor==='story:pip'?'story:lost_duckling':r.actor;
      const original=this.characters.find(c=>r.actor==='cheese'?c.cheese:c.id===actorId);
      const home=this.objects.find(o=>o.id===r.id&&sameInstance(o,r)&&o.construction==='furniture-v1'&&o.worldPosition?.every((v,i)=>Math.abs(v-r.destination[i])<1.1));
      if(!original||!home?.anchors?.slots)continue;
      const source=r.actor==='cheese'?s.duck:s.visitor?.id===actorId?s.visitor:s.rareVisitor?.id===actorId?s.rareVisitor:{...s.storyActor,id:actorId,castId:'lost_duckling',name:'Pip',stage:'duckling'};
      const inside=r.phase==='inside'?1:r.phase==='enter'?clamp(r.elapsed/3,0,1):clamp(1-r.elapsed/3,0,1);
      const performance={kind:'seating',routine:r.routine||{id:'perch_watch',elapsed:0},motion:s.motion!==false};
      const character={...characterSprite({...source,state:'idle',facing:r.slot===0,performance},t,r.actor!=='cheese'),x:original.x,y:original.y,cheese:r.actor==='cheese',story:original.story};
      (home.sitters||=[]).push({character,inside,slot:r.slot,envelope:residentEnvelope(character,'seating')});
      this.characters=this.characters.filter(c=>c!==original);
    }
    for(const r of living?.minds?.nest_helpers||[]){
      if(r.phase==='approach'||plan?.paused)continue;
      const actorId=r.actor==='story:pip'?'story:lost_duckling':r.actor;
      const original=this.characters.find(c=>c.id===actorId);
      const home=this.objects.find(o=>o.id===r.id&&sameInstance(o,r)&&o.anchors?.workLeft&&o.worldPosition?.every((n,i)=>Math.abs(n-r.destination[i])<1.1));
      if(!original||!home)continue;
      const source=s.visitor?.id===actorId?s.visitor:s.rareVisitor?.id===actorId?s.rareVisitor:{...s.storyActor,id:actorId,castId:'lost_duckling',name:'Pip',stage:'duckling'};
      const performance={kind:'nest',routine:r.routine,motion:s.motion!==false};
      const character={...characterSprite({...source,state:'idle',facing:r.spot[0]<r.destination[0],performance},t,true),x:original.x,y:original.y,story:original.story};
      (home.nestHelpers||=[]).push({character,inside:r.phase==='enter'?clamp(r.elapsed/2,0,1):1});
      this.characters=this.characters.filter(c=>c!==original);
    }
    for(const r of botanicalOccupants(s)){
      if(r.phase==='approach'||r.routine?.interrupted||!BOTANICAL_ROUTINES[r.routine?.id])continue;
      const actorId=r.actor==='story:pip'?'story:lost_duckling':r.actor;
      const original=this.characters.find(c=>r.actor==='cheese'?c.cheese:c.id===actorId);
      const home=this.objects.find(o=>o.id===r.id&&sameInstance(o,r)&&o.construction==='botanical-v1'&&o.worldPosition?.every((v,i)=>Math.abs(v-r.destination?.[i])<1.1));
      if(!original||!home?.anchors?.entry)continue;
      const source=r.actor==='cheese'?s.duck:s.visitor?.id===actorId?s.visitor:s.rareVisitor?.id===actorId?s.rareVisitor:{...s.storyActor,id:actorId,castId:'lost_duckling',name:'Pip',stage:'duckling'};
      const inside=r.phase==='inside'?1:r.phase==='enter'?clamp(r.elapsed/3,0,1):clamp(1-r.elapsed/3,0,1);
      const performance={kind:'botanical',routine:r.routine,motion:s.motion!==false};
      const character={...characterSprite({...source,state:'idle',facing:r.slot===0,performance},t,r.actor!=='cheese'),x:original.x,y:original.y,cheese:r.actor==='cheese',story:original.story};
      (home.gardeners||=[]).push({character,inside,slot:r.slot});
      this.characters=this.characters.filter(c=>c!==original);
    }
    for(const r of carnivalOccupants(s)){
      const actorId=r.actor==='story:pip'?'story:lost_duckling':r.actor;
      const original=this.characters.find(c=>r.actor==='cheese'?c.cheese:c.id===actorId);
      const home=this.objects.find(o=>o.id===plan.target&&sameInstance(o,plan)&&o.construction==='excursion-v1'&&o.worldPosition?.every((v,i)=>Math.abs(v-(r.work.shared?.mode==='egg-caregiver'?r.work.shared.center:plan.destination)?.[i])<1.1));
      if(!original||!home)continue;
      const source=r.actor==='cheese'?s.duck:r.work.shared_physical?sharedCastleSource(s,sharedCastleRecord(r.work)):s.visitor?.id===actorId?s.visitor:s.rareVisitor?.id===actorId?s.rareVisitor:{...s.storyActor,id:actorId,castId:'lost_duckling',name:'Pip',stage:'duckling'};
      if(!source)continue;
      const actorPhysical=castleActorPhysical(r.work,r.role),shared=r.work.shared_physical===true;
      const walkingPhysical=(shared||r.actor==='cheese'&&r.work.physical_pilot)&&actorPhysical?.phase!=='hold';
      const ownPose=walkingPhysical||(shared&&(plan.paused||r.actor==='cheese'&&source.hatCare?.active));
      const performance=ownPose?null:{kind:'carnival',routine:r.work,role:r.role,watch:r.watch,motion:s.motion!==false};
      const character={...characterSprite({...source,...(shared&&r.actor!=='cheese'?{castId:r.work.shared.mode==='flight-observer'?r.work.shared.observer.cast:r.work.shared.operator.cast}:{}),state:ownPose?(source.state||'walking'):'idle',facing:ownPose||shared&&r.watch?source.facing:r.role==='a',performance},t,r.actor!=='cheese'),x:original.x,y:original.y,cheese:r.actor==='cheese',story:original.story};
      if(home.physicalCastle&&actorPhysical)character.physicalCastleActor=home.physicalCastle;
      (home.carnivalRiders||=[]).push({...r,character});this.characters=this.characters.filter(c=>c!==original);
    }
    if(plan?.playkit_work&&!plan.playkit_work.interrupted&&PLAYKIT_ROUTINES[plan.playkit_work.id]&&['prepare','act','settle'].includes(plan.phase)){
      const original=this.characters.find(c=>c.cheese),home=this.objects.find(o=>o.id===plan.target&&sameInstance(o,plan)&&o.construction==='playkit-v1'&&(o.portable||o.worldPosition?.every((v,i)=>Math.abs(v-plan.destination?.[i])<1.1)));
      if(original&&home){
        const progress=plan.progress??plan.elapsed/plan.duration,inside=plan.phase==='act'?1:plan.phase==='prepare'?clamp((progress-.15)/.13,0,1):clamp(1-(progress-.9)/.1,0,1);
        const performance={kind:'playkit',routine:plan.playkit_work,motion:s.motion!==false};
        const character={...characterSprite({...s.duck,state:'idle',facing:true,performance},t),x:original.x,y:original.y,cheese:true};
        home.players=[{character,inside,slot:0}];this.characters=this.characters.filter(c=>c!==original);
      }
    }
    if(plan?.architecture_work&&!plan.architecture_work.interrupted&&ARCHITECTURE_ROUTINES[plan.architecture_work.id]&&['prepare','act','settle'].includes(plan.phase)){
      const original=this.characters.find(c=>c.cheese),home=this.objects.find(o=>o.id===plan.target&&sameInstance(o,plan)&&o.construction==='architecture-v1'&&(o.portable||o.worldPosition?.every((v,i)=>Math.abs(v-plan.destination?.[i])<1.1)));
      if(original&&home){
        const progress=plan.progress??plan.elapsed/plan.duration,inside=plan.phase==='act'?1:plan.phase==='prepare'?clamp((progress-.15)/.13,0,1):clamp(1-(progress-.9)/.1,0,1);
        const performance={kind:'architecture',routine:plan.architecture_work,motion:s.motion!==false};
        const character={...characterSprite({...s.duck,state:'idle',facing:true,performance},t),x:original.x,y:original.y,cheese:true};
        home.structureUsers=[{character,inside,slot:0}];this.characters=this.characters.filter(c=>c!==original);
      }
    }
    if(plan?.ground_work&&!plan.ground_work.interrupted&&GROUND_ROUTINES[plan.ground_work.id]&&['prepare','act','settle'].includes(plan.phase)){
      const original=this.characters.find(c=>c.cheese),home=this.objects.find(o=>o.id===plan.target&&sameInstance(o,plan)&&o.construction==='ground-v1'&&(o.portable||o.worldPosition?.every((v,i)=>Math.abs(v-plan.destination?.[i])<1.1)));
      if(original&&home){
        const progress=plan.progress??plan.elapsed/plan.duration,inside=plan.phase==='act'?1:plan.phase==='prepare'?clamp((progress-.15)/.13,0,1):clamp(1-(progress-.9)/.1,0,1);
        const performance={kind:'ground',routine:plan.ground_work,motion:s.motion!==false};
        const character={...characterSprite({...s.duck,state:'idle',facing:true,performance},t),x:original.x,y:original.y,cheese:true};
        home.groundUsers=[{character,inside,slot:0}];this.characters=this.characters.filter(c=>c!==original);
      }
    }
    if(plan?.textile_work&&!plan.textile_work.interrupted&&TEXTILE_ROUTINES[plan.textile_work.id]&&['prepare','act','settle'].includes(plan.phase)){
      const original=this.characters.find(c=>c.cheese),home=this.objects.find(o=>o.id===plan.target&&sameInstance(o,plan)&&o.construction==='textile-v1'&&(o.portable||o.worldPosition?.every((v,i)=>Math.abs(v-plan.destination?.[i])<1.1)));
      if(original&&home){
        const progress=plan.progress??plan.elapsed/plan.duration,inside=plan.phase==='act'?1:plan.phase==='prepare'?clamp((progress-.15)/.13,0,1):clamp(1-(progress-.9)/.1,0,1);
        const performance={kind:'textile',routine:plan.textile_work,motion:s.motion!==false};
        const character={...characterSprite({...s.duck,state:'idle',facing:true,performance},t),x:original.x,y:original.y,cheese:true};
        home.textileUsers=[{character,inside,slot:0}];this.characters=this.characters.filter(c=>c!==original);
      }
    }
    if(plan?.creative_work&&!plan.creative_work.interrupted&&CREATIVE_ROUTINES[plan.creative_work.id]&&['prepare','act','settle'].includes(plan.phase)){
      const original=this.characters.find(c=>c.cheese),home=this.objects.find(o=>o.id===plan.target&&sameInstance(o,plan)&&o.construction==='creative-v1'&&(o.portable||o.worldPosition?.every((v,i)=>Math.abs(v-plan.destination?.[i])<1.1)));
      if(original&&home){
        const progress=plan.progress??plan.elapsed/plan.duration,inside=plan.phase==='act'?1:plan.phase==='prepare'?clamp((progress-.15)/.13,0,1):clamp(1-(progress-.9)/.1,0,1);
        const performance={kind:'creative',routine:plan.creative_work,motion:s.motion!==false};
        const character={...characterSprite({...s.duck,state:'idle',facing:true,performance},t),x:original.x,y:original.y,cheese:true};
        home.creators=[{character,inside,slot:0}];this.characters=this.characters.filter(c=>c!==original);
      }
    }
    if(plan?.keepsake_work&&!plan.keepsake_work.interrupted&&KEEPSAKE_ROUTINES[plan.keepsake_work.id]&&['prepare','act','settle'].includes(plan.phase)){
      const original=this.characters.find(c=>c.cheese),home=this.objects.find(o=>o.id===plan.target&&sameInstance(o,plan)&&o.construction==='keepsake-v1'&&(o.portable||o.worldPosition?.every((v,i)=>Math.abs(v-plan.destination?.[i])<1.1)));
      if(original&&home){
        const progress=plan.progress??plan.elapsed/plan.duration,inside=plan.phase==='act'?1:plan.phase==='prepare'?clamp((progress-.15)/.13,0,1):clamp(1-(progress-.9)/.1,0,1);
        const performance={kind:'keepsake',routine:plan.keepsake_work,motion:s.motion!==false};
        const character={...characterSprite({...s.duck,state:'idle',facing:true,performance},t),x:original.x,y:original.y,cheese:true};
        home.keepers=[{character,inside,slot:0}];this.characters=this.characters.filter(c=>c!==original);
      }
    }
    if(plan?.rep_work&&!plan.rep_work.interrupted&&REP_ROUTINES[plan.rep_work.id]&&['prepare','act','settle'].includes(plan.phase)){
      const original=this.characters.find(c=>c.cheese),home=this.objects.find(o=>o.id===plan.target&&(plan.instance?sameInstance(o,plan):true)&&(o.portable||!plan.instance||o.worldPosition?.every((v,i)=>Math.abs(v-plan.destination?.[i])<1.1)));
      if(original&&home){
        const progress=plan.progress??plan.elapsed/plan.duration,inside=plan.phase==='act'?1:plan.phase==='prepare'?clamp((progress-.15)/.13,0,1):clamp(1-(progress-.9)/.1,0,1);
        const performance={kind:'rep',routine:plan.rep_work,motion:s.motion!==false};
        const character={...characterSprite({...s.duck,state:'idle',facing:true,performance},t),x:original.x,y:original.y,cheese:true};
        home.repWorkers=[{character,inside,slot:0}];this.characters=this.characters.filter(c=>c!==original);
      }else if(original&&!home&&REP_OBJECTS[plan.rep_work.object]?.host==='wearable'){
        // Worn or held things: the routine plays on Cheese himself, where he stands.
        const performance={kind:'rep',routine:plan.rep_work,motion:s.motion!==false};
        const i=this.characters.indexOf(original);
        this.characters[i]={...original,...characterSprite({...s.duck,state:'idle',facing:true,performance},t),x:original.x,y:original.y,cheese:true};
      }
    }
    if(plan?.wonder_work&&!plan.wonder_work.interrupted&&WONDER_ROUTINES[plan.wonder_work.id]&&['prepare','act','settle'].includes(plan.phase)){
      const original=this.characters.find(c=>c.cheese),home=this.objects.find(o=>o.id===plan.target&&sameInstance(o,plan)&&o.construction==='wonder-v1'&&o.worldPosition?.every((v,i)=>Math.abs(v-plan.destination?.[i])<1.1));
      if(original&&home){
        const progress=plan.progress??plan.elapsed/plan.duration,inside=plan.phase==='act'?1:plan.phase==='prepare'?clamp((progress-.15)/.13,0,1):clamp(1-(progress-.9)/.1,0,1);
        const performance={kind:'wonder',routine:plan.wonder_work,motion:s.motion!==false};
        const character={...characterSprite({...s.duck,state:'idle',facing:true,performance},t),x:original.x,y:original.y,cheese:true};
        home.wonderWorkers=[{character,inside,slot:0}];this.characters=this.characters.filter(c=>c!==original);
      }
    }
    for(const r of s.living?.minds?.wonderGuests||[]){
      if(r.phase==='approach'||!(WONDER_ROUTINES[r.routine?.id]||REP_ROUTINES[r.routine?.id]))continue;
      const original=this.characters.find(c=>c.id===r.actor);
      const home=this.objects.find(o=>o.id===r.id&&sameInstance(o,r)&&(o.construction==='wonder-v1'||REP_ROUTINES[r.routine.id])&&o.worldPosition?.every((v,i)=>Math.abs(v-r.destination?.[i])<1.1));
      if(!original||!home)continue;
      const source=s.visitor?.id===r.actor?s.visitor:s.rareVisitor?.id===r.actor?s.rareVisitor:{...s.storyActor,id:r.actor,castId:'lost_duckling',name:'Pip',stage:'duckling'};
      const inside=r.phase==='enter'?clamp(r.elapsed/2,0,1):r.phase==='exit'?clamp(1-r.elapsed/2,0,1):1,performance={kind:REP_ROUTINES[r.routine.id]?'rep':'wonder',routine:r.routine,motion:s.motion!==false};
      const character={...characterSprite({...source,state:'idle',facing:r.spot[0]<r.destination[0],performance},t,true),x:original.x,y:original.y,story:original.story};
      (REP_ROUTINES[r.routine.id]?(home.repWorkers||=[]):(home.wonderWorkers||=[])).push({character,inside,slot:r.mode==='company'?1:0});this.characters=this.characters.filter(c=>c!==original);
    }
    for(const r of s.living?.minds?.playmates||[]){
      if(r.phase==='approach'||r.routine?.interrupted||!PLAYKIT_ROUTINES[r.routine?.id])continue;
      const actorId=r.actor==='story:pip'?'story:lost_duckling':r.actor,original=this.characters.find(c=>c.id===actorId);
      const home=this.objects.find(o=>o.id===r.id&&sameInstance(o,r)&&o.construction==='playkit-v1'&&(o.portable||o.worldPosition?.every((v,i)=>Math.abs(v-r.destination?.[i])<1.1)));
      if(!original||!home)continue;
      const source=s.visitor?.id===actorId?s.visitor:s.rareVisitor?.id===actorId?s.rareVisitor:{...s.storyActor,id:actorId,castId:'lost_duckling',name:'Pip',stage:'duckling'};
      const inside=r.phase==='enter'?clamp(r.elapsed/2,0,1):r.phase==='exit'?clamp(1-r.elapsed/2,0,1):1,performance={kind:'playkit',routine:r.routine,motion:s.motion!==false};
      const character={...characterSprite({...source,state:'idle',facing:false,performance},t,true),x:original.x,y:original.y,story:original.story};
      (home.players||=[]).push({character,inside,slot:1});this.characters=this.characters.filter(c=>c!==original);
    }
    for(const r of s.living?.minds?.structure_helpers||[]){
      if(r.phase==='approach'||r.routine?.interrupted||!ARCHITECTURE_ROUTINES[r.routine?.id])continue;
      const actorId=r.actor==='story:pip'?'story:lost_duckling':r.actor,original=this.characters.find(c=>c.id===actorId);
      const home=this.objects.find(o=>o.id===r.id&&sameInstance(o,r)&&o.construction==='architecture-v1'&&(o.portable||o.worldPosition?.every((v,i)=>Math.abs(v-r.destination?.[i])<1.1)));
      if(!original||!home)continue;
      const source=s.visitor?.id===actorId?s.visitor:s.rareVisitor?.id===actorId?s.rareVisitor:{...s.storyActor,id:actorId,castId:'lost_duckling',name:'Pip',stage:'duckling'};
      const inside=r.phase==='enter'?clamp(r.elapsed/2,0,1):r.phase==='exit'?clamp(1-r.elapsed/2,0,1):1,performance={kind:'architecture',routine:r.routine,motion:s.motion!==false};
      const character={...characterSprite({...source,state:'idle',facing:false,performance},t,true),x:original.x,y:original.y,story:original.story};
      (home.structureUsers||=[]).push({character,inside,slot:1});this.characters=this.characters.filter(c=>c!==original);
    }
    for(const r of s.living?.minds?.ground_helpers||[]){
      if(r.phase==='approach'||r.routine?.interrupted||!GROUND_ROUTINES[r.routine?.id])continue;
      const actorId=r.actor==='story:pip'?'story:lost_duckling':r.actor,original=this.characters.find(c=>c.id===actorId);
      const home=this.objects.find(o=>o.id===r.id&&sameInstance(o,r)&&o.construction==='ground-v1'&&(o.portable||o.worldPosition?.every((v,i)=>Math.abs(v-r.destination?.[i])<1.1)));
      if(!original||!home)continue;
      const source=s.visitor?.id===actorId?s.visitor:s.rareVisitor?.id===actorId?s.rareVisitor:{...s.storyActor,id:actorId,castId:'lost_duckling',name:'Pip',stage:'duckling'};
      const inside=r.phase==='enter'?clamp(r.elapsed/2,0,1):r.phase==='exit'?clamp(1-r.elapsed/2,0,1):1,performance={kind:'ground',routine:r.routine,motion:s.motion!==false};
      const character={...characterSprite({...source,state:'idle',facing:false,performance},t,true),x:original.x,y:original.y,story:original.story};
      (home.groundUsers||=[]).push({character,inside,slot:1});this.characters=this.characters.filter(c=>c!==original);
    }
    for(const r of s.living?.minds?.textile_helpers||[]){
      if(r.phase==='approach'||r.routine?.interrupted||!TEXTILE_ROUTINES[r.routine?.id])continue;
      const actorId=r.actor==='story:pip'?'story:lost_duckling':r.actor,original=this.characters.find(c=>c.id===actorId);
      const home=this.objects.find(o=>o.id===r.id&&sameInstance(o,r)&&o.construction==='textile-v1'&&(o.portable||o.worldPosition?.every((v,i)=>Math.abs(v-r.destination?.[i])<1.1)));
      if(!original||!home)continue;
      const source=s.visitor?.id===actorId?s.visitor:s.rareVisitor?.id===actorId?s.rareVisitor:{...s.storyActor,id:actorId,castId:'lost_duckling',name:'Pip',stage:'duckling'};
      const inside=r.phase==='enter'?clamp(r.elapsed/2,0,1):r.phase==='exit'?clamp(1-r.elapsed/2,0,1):1,performance={kind:'textile',routine:r.routine,motion:s.motion!==false};
      const character={...characterSprite({...source,state:'idle',facing:false,performance},t,true),x:original.x,y:original.y,story:original.story};
      (home.textileUsers||=[]).push({character,inside,slot:1});this.characters=this.characters.filter(c=>c!==original);
    }
    for(const r of s.living?.minds?.creators||[]){
      if(r.phase==='approach'||r.routine?.interrupted||!CREATIVE_ROUTINES[r.routine?.id])continue;
      const actorId=r.actor==='story:pip'?'story:lost_duckling':r.actor,original=this.characters.find(c=>c.id===actorId);
      const home=this.objects.find(o=>o.id===r.id&&sameInstance(o,r)&&o.construction==='creative-v1'&&(o.portable||o.worldPosition?.every((v,i)=>Math.abs(v-r.destination?.[i])<1.1)));
      if(!original||!home)continue;
      const source=s.visitor?.id===actorId?s.visitor:s.rareVisitor?.id===actorId?s.rareVisitor:{...s.storyActor,id:actorId,castId:'lost_duckling',name:'Pip',stage:'duckling'};
      const inside=r.phase==='enter'?clamp(r.elapsed/2,0,1):r.phase==='exit'?clamp(1-r.elapsed/2,0,1):1,performance={kind:'creative',routine:r.routine,motion:s.motion!==false};
      const character={...characterSprite({...source,state:'idle',facing:false,performance},t,true),x:original.x,y:original.y,story:original.story};
      (home.creators||=[]).push({character,inside,slot:1});this.characters=this.characters.filter(c=>c!==original);
    }
    for(const r of s.living?.minds?.readers||[]){
      if(r.phase==='approach'||r.routine?.interrupted||!KEEPSAKE_ROUTINES[r.routine?.id])continue;
      const actorId=r.actor==='story:pip'?'story:lost_duckling':r.actor,original=this.characters.find(c=>c.id===actorId);
      const home=this.objects.find(o=>o.id===r.id&&sameInstance(o,r)&&o.construction==='keepsake-v1'&&(o.portable||o.worldPosition?.every((v,i)=>Math.abs(v-r.destination?.[i])<1.1)));
      if(!original||!home)continue;
      const source=s.visitor?.id===actorId?s.visitor:s.rareVisitor?.id===actorId?s.rareVisitor:{...s.storyActor,id:actorId,castId:'lost_duckling',name:'Pip',stage:'duckling'};
      const inside=r.phase==='enter'?clamp(r.elapsed/2,0,1):r.phase==='exit'?clamp(1-r.elapsed/2,0,1):1,performance={kind:'keepsake',routine:r.routine,motion:s.motion!==false};
      const character={...characterSprite({...source,state:'idle',facing:false,performance},t,true),x:original.x,y:original.y,story:original.story};
      (home.keepers||=[]).push({character,inside,slot:1});this.characters=this.characters.filter(c=>c!==original);
    }
    if(plan?.light_work&&!plan.light_work.interrupted&&LIGHTING_ROUTINES[plan.light_work.id]&&['prepare','act','settle'].includes(plan.phase)){
      const original=this.characters.find(c=>c.cheese),home=this.objects.find(o=>o.id===plan.target&&sameInstance(o,plan)&&o.construction==='lighting-v1'&&o.worldPosition?.every((v,i)=>Math.abs(v-plan.destination?.[i])<1.1));
      if(original&&home){
        const progress=plan.progress??plan.elapsed/plan.duration,inside=plan.phase==='act'?1:plan.phase==='prepare'?clamp((progress-.15)/.13,0,1):clamp(1-(progress-.9)/.1,0,1);
        const performance={kind:'lighting',routine:plan.light_work,motion:s.motion!==false};
        const character={...characterSprite({...s.duck,state:'idle',facing:true,performance},t),x:original.x,y:original.y,cheese:true};
        home.lightWorkers=[{character,inside}];this.characters=this.characters.filter(c=>c!==original);
      }
    }
    for(const r of musicians){
      if(r.phase==='approach'||r.score?.interrupted||!MUSIC_SCORES[r.score?.id])continue;
      const actorId=r.actor==='story:pip'?'story:lost_duckling':r.actor;
      const original=this.characters.find(c=>r.actor==='cheese'?c.cheese:c.id===actorId);
      const home=this.objects.find(o=>o.id===r.id&&sameInstance(o,r)&&o.construction==='instrument-v1'&&o.worldPosition?.every((v,i)=>Math.abs(v-r.destination?.[i])<1.1));
      if(!original||!home?.anchors?.entry)continue;
      const source=r.actor==='cheese'?s.duck:s.visitor?.id===actorId?s.visitor:s.rareVisitor?.id===actorId?s.rareVisitor:{...s.storyActor,id:actorId,castId:'lost_duckling',name:'Pip',stage:'duckling'};
      const inside=r.phase==='inside'?1:r.phase==='enter'?clamp(r.elapsed/3,0,1):clamp(1-r.elapsed/3,0,1);
      const performance={kind:'instrument',item:r.id,routine:r.score,motion:s.motion!==false};
      const character={...characterSprite({...source,state:'idle',facing:r.slot===0,performance},t,r.actor!=='cheese'),x:original.x,y:original.y,cheese:r.actor==='cheese',story:original.story};
      (home.musicians||=[]).push({character,inside,slot:r.slot});
      this.characters=this.characters.filter(c=>c!==original);
    }
    const partnerId=plan?.company?.partner==='story:pip'?'story:lost_duckling':plan?.company?.partner;
    const partner=this.characters.find(c=>c.id===partnerId),shared=!residence&&playdateStage(plan,this.objects,cheese,partner,s.motion!==false);
    if(shared){
      const source=s.visitor?.id===partnerId?s.visitor:s.rareVisitor?.id===partnerId?s.rareVisitor:{...s.storyActor,id:partnerId,castId:'lost_duckling',name:'Pip',stage:'duckling'};
      const members=[{model:cheese,source:s.duck,role:'a',visitor:false},{model:partner,source,role:'b',visitor:true}];
      shared.home.riders=members.map(({model,source,role,visitor},i)=>{
        const pose=shared.pose,walking=plan.company.phase!=='act';
        const beat=pose.family==='ball'?(pose.turn===role?pose.beat:0):role==='a'?pose.beat:(pose.beat+.5)%1;
        const kind=pose.family==='sandbox'&&pose.turn!==role?'watch_build':pose[role];
        const performance=walking?null:{kind,role,progress:beat};
        const character={...characterSprite({...source,state:walking?'walking':'idle',facing:role==='a',performance},t,visitor),x:model.x,y:model.y,cheese:!visitor};
        return {character,seat:shared.seats[i],inside:shared.inside};
      });
      this.characters=this.characters.filter(c=>c!==cheese&&c!==partner);
    }
    const ride=!residence&&!shared&&!plan?.company&&playgroundStage(plan?.rep_work?null:plan,this.objects,cheese,s.duck.stage,s.motion!==false);
    if(ride){
      const performance={kind:ride.gesture,role:'a',progress:s.motion===false?.5:ride.beat};
      const rider={...characterSprite({...s.duck,state:plan.phase==='settle'?'walking':'idle',performance:plan.phase==='settle'?null:performance},t),x:cheese.x,y:cheese.y,cheese:true};
      ride.home.rider={character:rider,seat:ride.seat,inside:ride.inside};
      this.characters=this.characters.filter(c=>c!==cheese);
    }
    for(const performance of living?.minds?.performances||[]){
      if(performance.phase!=='act')continue;
      const a=performance.spots?.[performance.a],b=performance.spots?.[performance.b];
      if(!a||!b)continue;
      const [px,py]=this.project(s,(a[0]+b[0])/2,(a[1]+b[1])/2),p=s.motion===false?.5:performance.elapsed/performance.duration;
      if(performance.performance==='pebble_inspection')g.art(px-3,py-2,[' .---.','( . : )',"'-----'"],C.barkLight);
      if(performance.performance==='crumb_search'){g.text(px-3,py,'. o .',C.goldDark);if(p>.45)g.put(px+2,py-1,'.',C.goldLight);}
      if(performance.performance==='puddle_splash'){
        g.ellipse(px,py+1,13,2,'~',C.waterLight);
        for(const beat of [.45,.82]){const age=p-beat;if(age>=0&&age<.16){const spread=age*55;for(const sign of [-1,1])g.put(px+sign*(3+spread),py-4-Math.sin(age/.16*Math.PI)*4,'.',C.waterLight);}}
      }
      if(performance.performance==='leaf_chase'){const drift=Math.sin(p*Math.PI*3)*5;g.art(px+drift,py-5-Math.sin(p*Math.PI)*5,[' /;>',"'/'"],C.goldDark);}
      if(performance.performance==='snow_tracks'){for(let n=0;n<Math.ceil(p*4);n++)g.text(px-6+n*4,py+1+(n%2),n%2?'v':'^',C.ice);}
    }
    if(s.interaction){const [ix,iy]=this.project(s,s.interaction.x,s.interaction.y);g.art(ix-6,iy-s.interaction.art.length,s.interaction.art,C.goldLight);}
  }
  foreground(s,t,seed){
    const g=this.grid;
    for(let n=0;n<35;n++){
      const x=n<17?n*2:W-(n-17)*2,y=H-1-hash(n,7,seed)*5,h=6+hash(n,8,seed)*12;
      const sway=Math.sin(t*1.3+n)*(.6+this.wind.vector.strength*1.4)+this.wind.vector.x*2;
      for(let j=0;j<h;j++)g.put(x+sway*(j/h),y-j,j===h-1?'!':j%4===0?'/':'|',n%3?C.leafDark:C.leaf);
    }
    if(s.particles===false)return;
    const night=sceneLight(s).night;
    if(night||s.biome==='swamp'||/cave/i.test(s.location))for(let n=0;n<22;n++){
      const x=(hash(n,9,seed)*W+Math.sin(t*.7+n)*7),y=45+hash(n,10,seed)*53+Math.sin(t+n)*3;
      const bright=Math.sin(t*2+n*2)>.4;
      g.put(x,y,bright?'*':'.',bright?C.lamp:C.grass);
      if(bright&&n%3===0){g.put(x-1,y,'.',C.leaf);g.put(x+1,y,'.',C.leaf);}
    }
    if(!night&&['meadow','garden','pond'].includes(s.biome))for(let n=0;n<6;n++){
      const x=(n*41+t*(2+n*.1))%W,y=55+Math.sin(t*.8+n)*7+n*3;
      g.text(x,y,Math.sin(t*12+n)>0?'x':'><',n%2?C.flower:C.goldLight);
    }
    if(s.season==='fall'&&!/snow/.test(s.weather))for(let n=0;n<15;n++){
      g.put(wrap(n*29+this.wind.x*12+Math.sin(t+n)*4,W),wrap(t*2+n*9+this.wind.y*4,H),choice('~,/;',hash(n,0)),n%2?C.barkLight:C.flower);
    }
  }
  weather(s,t,seed){
    if(s.weatherEffects===false)return;
    const g=this.grid,w=s.weather||'',intensity=clamp(s.intensity||.5,.15,1);
    if(/rain|storm|drizzle/.test(w)){
      const count=Math.floor((/storm/.test(w)?230:100)*intensity);
      for(let n=0;n<count;n++){
        const x=wrap(hash(n,1,seed)*W+this.wind.x*32,W+15)-8,y=wrap(hash(n,2,seed)*H+t*(42+n%12)+this.wind.y*4,H);
        const dx=this.wind.vector.x,drop=Math.abs(dx)<.06?'|':dx<0?'/':'\\';
        g.put(x,y,drop,n%3?C.water:C.waterLight);
        if(/storm/.test(w))g.put(x-(Math.abs(dx)<.06?0:Math.sign(dx)),y-1,drop,C.waterDark);
      }
      for(let n=0;n<20;n++){
        const x=hash(n,7,seed)*W,y=70+hash(n,8,seed)*38,phase=(t*3+n)%2;
        if(phase<.8)g.text(x,y,phase<.4?'v':'-~-',C.waterLight);
      }
    }
    if(/snow|blizzard/.test(w))for(let n=0;n<160*intensity;n++){
      const x=wrap(hash(n,3,seed)*W+Math.sin(t*.5+n)*4+this.wind.x*19,W),y=wrap(hash(n,4,seed)*H+t*(3+n%5)+this.wind.y*5,H);
      g.put(x,y,n%4===0?'*':'.',n%3?C.ice:C.white);
    }
    if(/fog|mist/.test(w)||s.biome==='swamp')for(let n=0;n<4;n++){
      const y=48+n*14;
      for(let x=0;x<W;x++)if(hash(x,n,seed)>.5)g.put(x,y+Math.sin(x*.05+t*.3+n)*2,choice(' .-~',hash(x,n)),C.mist);
    }
    if(/wind/.test(w))for(let n=0;n<10;n++)g.text(wrap(this.wind.x*30+n*28,W),36+wrap(n*6+this.wind.y*9,60),this.wind.vector.x<0?'~..-':'-..~',C.cloud);
    if(/rainbow/.test(w))for(let band=0;band<4;band++)for(let x=20;x<220;x++){
      const y=43-Math.sqrt(Math.max(0,1-((x-120)/105)**2))*29+band;
      g.put(x,y,'.',[C.flower,C.gold,C.grass,C.crystal][band]);
    }
  }
  underground(s){return /cave|drain/i.test(s.location);}
  cavern(s,t,seed){
    const g=this.grid,drain=s.location==='Storm Drain';
    for(let x=0;x<W;x++){
      const edge=Math.abs(x-W/2)/(W/2),ceiling=7+edge**3*48+hash(x>>2,7,seed)*7;
      for(let y=0;y<ceiling;y++){
        const r=hash(x,y,seed),rim=y>ceiling-3;
        g.put(x,y,drain?(y%7===0?'_':x%13===0?'|':'.'):choice(' .:/|',r),rim?C.hill:r>.7?C.far:C.shadow);
      }
      if(!drain&&x%13===0){
        const length=5+hash(x,3,seed)*15;
        for(let y=0;y<length;y++)g.text(x-y*.09,ceiling+y,y<length-3?'\\|/':'v',C.far);
      }
    }
    if(drain){
      for(let n=0;n<4;n++){
        const rx=24+n*19,ry=20+n*8;
        for(let a=Math.PI;a<Math.PI*2;a+=.025)g.put(W/2+Math.cos(a)*rx,61+Math.sin(a)*ry,'#',n%2?C.hill:C.far);
      }
      g.text(100,58,'| | | | | | | | | |',C.bark);
      g.text(100,59,'|_|_|_|_|_|_|_|_|_|',C.barkLight);
    }
  }
  render(scene,time,dt=1/30){
    const s={hour:12,season:'spring',weather:'sunny',biome:'pond',location:'Home Pond',...scene};
    const t=s.motion===false?0:time,seed=seedOf(s.location);
    this.wind.update(s,dt,!this.underground(s));
    this.grid.clear();this.characters=[];this.objects=[];this.scenery=[];
    if(this.underground(s))this.cavern(s,t,seed);
    else {this.sky(s,t,seed);this.hills(s,t,seed);}
    this.terrain(s,t,seed);
    this.landmarks(s,t,seed);this.actors(s,t,dt);this.foreground(s,t,seed);
    if(!this.underground(s))this.sceneryLayer('weather',Infinity,()=>this.weather(s,t,seed)).overlay=true;
    this.lastLocation=s.location;this.lastTime=t;
    return {grid:this.grid,palette:palette(s),characters:this.characters,objects:this.objects,scenery:this.scenery};
  }
}
