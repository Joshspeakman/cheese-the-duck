import { W,H,C,hash } from './ultra-grid.mjs';

export const EFFECT_LEVELS=['vivid','subtle','off'];
export function effectStrength(level){return level==='off'?0:level==='subtle'?.38:1;}
export function luminousPalette(palette,level){
  const amount=effectStrength(level);if(!amount)return palette;
  return palette.map((hex,i)=>{
    if(i===0)return hex;
    const rgb=hex.match(/[a-f\d]{2}/gi).map(v=>parseInt(v,16)),luma=rgb[0]*.21+rgb[1]*.72+rgb[2]*.07;
    return '#'+rgb.map(v=>Math.round(Math.max(0,Math.min(255,luma+(v-luma)*(1+.16*amount)+amount*(i===C.shadow?0:9)))) .toString(16).padStart(2,'0')).join('');
  });
}

export class SceneEffects {
  constructor(){this.level='vivid';this.light=document.createElement('canvas');this.light.width=480;this.light.height=224;this.lc=this.light.getContext('2d');}
  draw(ctx,world,scene,time,sx,sy,objects=[]){
    const strength=effectStrength(this.level);if(!strength)return;
    const t=scene.motion===false?0:time,night=scene.hour<6||scene.hour>=20;
    const underground=world.underground(scene),wet=/rain|storm|drizzle/.test(scene.weather)&&scene.weatherEffects!==false;
    const lc=this.lc;lc.clearRect(0,0,480,224);
    const glow=(x,y,r,color,power)=>{
      const gradient=lc.createRadialGradient(x*2,y*2,0,x*2,y*2,r*2);
      gradient.addColorStop(0,color+Math.round(power*strength*255).toString(16).padStart(2,'0'));gradient.addColorStop(1,color+'00');
      lc.fillStyle=gradient;lc.fillRect((x-r)*2,(y-r)*2,r*4,r*4);
    };
    if(!underground){
      const sunX=night?183:43+(scene.hour-6)*10;
      glow(sunX,13,night?36:52,night?'#8bd7ed':'#ffd197',wet?.1:night?.3:.17);
      // Soft shafts are illumination underneath the sharp character ink.
      lc.save();lc.globalAlpha=(wet?.015:night?.045:.022)*strength;lc.fillStyle=night?'#87cadd':'#ffe4a3';
      for(let i=0;i<4;i++){
        const drift=Math.sin(t*.12+i)*3,x=sunX+i*9;
        lc.beginPath();lc.moveTo(x*2,16);lc.lineTo((x-45+drift)*2,216);lc.lineTo((x-24+drift)*2,216);lc.lineTo((x+2)*2,16);lc.closePath();lc.fill();
      }lc.restore();
    }
    // Selective bloom uses a small light buffer; neither UI nor full-size glyphs
    // are blurred. Emissive objects get warm pools, crystals cool ones.
    for(const object of objects){
      if(object.item&&object.emissive)glow(object.x,object.y-object.art.length*object.scale*.7,12,object.accent,night?.25:.13);
    }
    const grid=world.grid;
    for(let i=0,n=0;i<W*H;i+=3){
      if(grid.chars[i]===32)continue;
      const color=grid.colors[i];
      if((color===C.lamp||color===C.crystal||color===C.glint)&&hash(i,5)>.85&&n++<55)glow(i%W,(i/W)|0,color===C.glint?2.8:5,color===C.lamp?'#ffd08c':'#89e4e0',.15);
    }
    ctx.save();ctx.globalCompositeOperation='screen';ctx.drawImage(this.light,0,0,W*sx,H*sy);ctx.restore();
    if(scene.particles===false)return;
    ctx.save();ctx.textAlign='center';ctx.textBaseline='middle';ctx.font=`600 ${Math.max(7,sy*1.1)}px Menlo, monospace`;
    // Interlocking caustic streaks follow actual water cells, including winter,
    // shorelines and different biomes. A dry meadow never acquires pond ripples.
    for(let i=0;i<42;i++){
      const x=Math.floor(hash(i,11)*W),y=Math.floor(55+hash(i,12)*45);
      if(!world.water[y*W+x]||scene.season==='winter')continue;
      const pulse=.5+.5*Math.sin(t*1.1+i*2.3);
      ctx.globalAlpha=(.08+pulse*.24)*strength;ctx.fillStyle=night?'#a9e2e9':'#e7ebbf';
      ctx.fillText(pulse>.8?'~--~':'-~-',x*sx,y*sy);
      if(wet){
        const phase=(t*.65+hash(i,13))%1;
        ctx.globalAlpha=(1-phase)*.3*strength;
        ctx.fillText(phase<.3?'o':phase<.65?'( . )':'(     )',x*sx,y*sy);
      }
    }
    // Discrete little motes, always ASCII. Wind moves them along repeatable paths.
    if(!wet)for(let i=0;i<(night?22:16);i++){
      const x=(hash(i,41)*W+t*(.6+hash(i,42))+.6*Math.sin(t*.5+i))%W;
      const y=43+hash(i,43)*56+Math.sin(t*.7+i)*1.4;
      ctx.fillStyle=underground?'#bbbcf6':night?'#e7ed9e':/fall|autumn/.test(scene.season)?'#efb373':'#ffe1a5';
      ctx.globalAlpha=(.16+.34*(.5+.5*Math.sin(t*1.4+i)))*strength;
      ctx.fillText(night?(i%4?'*':'+'):/fall|autumn/.test(scene.season)?"'":'.',x*sx,y*sy);
    }
    // A short wake keeps Cheese grounded in water without hiding his silhouette.
    const duck=world.duckPosition;
    if(duck&&!scene.duck.hidden&&!scene.duck.away&&/swim|splash|float/.test(scene.duck.state||'')){
      ctx.fillStyle='#9bdde3';ctx.globalAlpha=.4*strength;
      for(let i=0;i<3;i++)ctx.fillText(i===0?'~---~':'-~-',(duck[0]-8-i*3)*sx,(duck[1]+i)*sy);
    }
    ctx.restore();
  }
}
