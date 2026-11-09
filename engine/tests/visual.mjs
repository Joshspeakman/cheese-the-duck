import { SceneCanvas,DisplayRenderer } from '../client/ultra-renderer.mjs';
import { GlyphRenderer } from '../client/renderer.mjs';
import { scene,BIOMES,LOCATIONS } from './scenes.mjs';
const assert=(x,label)=>{if(!x)throw new Error(label);};
const equal=(a,b)=>a.length===b.length&&a.every((v,i)=>v===b[i]);
const pixels=canvas=>canvas.getContext('2d').getImageData(0,0,canvas.width,canvas.height).data;
window.runVisualChecks=frame=>{
 const images={},durations=[];
 const sheet=document.createElement('canvas');sheet.width=1800;sheet.height=1104;
 const ctx=sheet.getContext('2d');ctx.fillStyle='#0c1c21';ctx.fillRect(0,0,1800,1104);
 for(const [i,biome] of BIOMES.entries()){
  const canvas=new SceneCanvas();canvas.resize(1440,672);
  const s=scene({biome,location:LOCATIONS[i],hour:i===6?22:i===7?4:i===3?18:14,season:i===7?'winter':i===1?'fall':'spring',weather:i===6?'foggy':i===7?'snowy':'sunny'});
  if(i===2)s.duck.state='dancing'; if(i===0)s.duck.state='swimming'; if(i===3)s.duck.cosmetics={hat:'party_hat'};
  canvas.draw(s,2,1/30);
  const first=new Uint8ClampedArray(pixels(canvas.canvas));
  for(let n=0;n<30;n++){const start=performance.now();canvas.draw(s,2+n/30,1/30);durations.push(performance.now()-start);}
  assert(!equal(first,pixels(canvas.canvas)),`animation frozen: ${biome}`);
  images[biome]=canvas.canvas.toDataURL('image/png');
  const x=i%3*600,y=Math.floor(i/3)*368;
  ctx.fillStyle='#ebd2a3';ctx.font='18px Menlo';ctx.fillText(`${LOCATIONS[i]} / ${s.season}`,x+14,y+28);
  ctx.drawImage(canvas.canvas,x,y+40,600,280);
 }
 images.gallery=sheet.toDataURL('image/png');
 const classic=new GlyphRenderer(document.createElement('canvas')),display=new DisplayRenderer(document.createElement('canvas'));
 classic.resize(frame.cols,frame.rows,1);classic.draw(frame);
 display.resize(frame.cols,frame.rows,1);display.mode='classic';display.draw(frame,1000);
 assert(equal(pixels(classic.canvas),pixels(display.canvas)),'Classic pixels changed');
 display.mode='ultra';display.draw(frame,1000);
 const o=frame.scene?.overlay;
 assert(o,'smoke frame must include a real dialogue modal');
 const sx=classic.sx,sy=classic.sy,rect=[Math.floor(o.x*sx),Math.floor(o.y*sy),Math.ceil(o.w*sx),Math.ceil(o.h*sy)];
 assert(equal(classic.ctx.getImageData(...rect).data,display.ctx.getImageData(...rect).data),'Ultra overwrote the dialogue overlay');
 display.mode='classic';display.draw(frame,1033);
 assert(equal(pixels(classic.canvas),pixels(display.canvas)),'returning to Classic left Ultra pixels behind');
 durations.sort((a,b)=>a-b);
 return {images,checks:['nine animated biomes','Classic pixel parity','opaque dialogue preservation','return to Classic'],medianMs:durations[Math.floor(durations.length*.5)],p95Ms:durations[Math.floor(durations.length*.95)]};
};
