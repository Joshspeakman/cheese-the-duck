import { sceneLight,ambientRows,ambientSwatches,lightBand,readableInk,mixColor } from './scene-lighting.mjs';
import { GlyphRenderer } from './renderer.mjs';
import { LivingWorld } from './ultra-world.mjs';
import { drawCharacter } from './ultra-characters.mjs';
import { ItemPainter } from './ultra-items.mjs';
import {occupiedGeometry,heldNestGeometry} from './residence-stage.mjs';
import {ridingGeometry} from './playground-stage.mjs';
import { SceneEffects,luminousPalette } from './scene-effects.mjs';
import { W,H,C,M } from './ultra-grid.mjs';
import { InterfaceRenderer } from './interface-renderer.mjs';

const TITLE_SCENE={biome:'pond',location:'Home Pond',season:'spring',hour:12,weather:'sunny',intensity:.5,motion:true,particles:true,weatherEffects:true,
  camera:{x:0,y:0,w:132,h:42},duck:{name:'Cheese',x:65,y:24,hidden:true,stage:'adult',state:'idle',cosmetics:{}},items:[],structures:[],visitor:null,interaction:null};

export class SceneCanvas {
  constructor(){
    this.canvas=document.createElement('canvas');this.ctx=this.canvas.getContext('2d',{alpha:false});
    this.terrain=document.createElement('canvas');this.terrainCtx=this.terrain.getContext('2d',{alpha:false});
    this.world=new LivingWorld();this.atlas=new Map();this.previousChars=new Uint8Array(W*H);this.previousColors=new Uint8Array(W*H);this.previousWater=new Uint8Array(W*H);
    this.previousMaterials=new Uint8Array(W*H);
    this.paletteKey='';this.frames=0;this.items=new ItemPainter();this.effects=new SceneEffects();
  }
  resize(width,height){
    width=Math.round(width);height=Math.round(height);
    if(this.canvas.width===width&&this.canvas.height===height)return;
    this.canvas.width=width;this.canvas.height=height;this.terrain.width=width;this.terrain.height=height;this.sx=width/W;this.sy=height/H;
    this.previousChars.fill(0);this.atlas.clear();this.paletteKey='';
  }
  tile(char,color,outline=null){
    const key=char+':'+color+':'+outline;
    if(this.atlas.has(key))return this.atlas.get(key);
    const tile=document.createElement('canvas');tile.width=Math.ceil(this.sx);tile.height=Math.ceil(this.sy);
    const ctx=tile.getContext('2d');ctx.fillStyle=color;
    ctx.font=`600 ${Math.max(6,this.sy*1.14)}px Menlo, monospace`;
    ctx.textBaseline='middle';ctx.textAlign='center';
    if(outline){ctx.strokeStyle=outline;ctx.lineWidth=Math.max(.9,this.sy*.095);ctx.strokeText(String.fromCharCode(char),tile.width/2,tile.height*.52,tile.width);}
    ctx.fillText(String.fromCharCode(char),tile.width/2,tile.height*.52,tile.width);
    if(this.atlas.size>=4096)this.atlas.delete(this.atlas.keys().next().value);
    this.atlas.set(key,tile);return tile;
  }
  draw(scene,time,dt){
    const light=sceneLight(scene);this.light=light;
    const result=this.world.render(scene,time,dt),{grid,characters,objects}=result;
    const palette=luminousPalette(result.palette,this.effects.level),key=palette.join('')+JSON.stringify(light);
    if(key!==this.paletteKey){
      this.previousChars.fill(0);this.paletteKey=key;this.atlas.clear();this.ambient=ambientRows(light,H);
      const highlights=new Set([C.cloud,C.glint,C.waterLight,C.lamp,C.star,C.goldLight,C.white]);
      const grassInk=new Set([C.groundDark,C.ground,C.grass]);
      this.swatches=ambientSwatches(light,this.ambient);this.ink={};this.outlines={};
      this.bands=Uint8Array.from({length:W*H},(_,i)=>lightBand(light,i%W,(i/W)|0));
      for(const surface of Object.keys(this.swatches)){
        const rows=this.swatches[surface];
        this.ink[surface]=rows.map(band=>Array.from({length:Math.ceil(H/8)},(_,y)=>palette.map((ink,i)=>{
          const background=band[Math.min(H-1,y*8+4)];
          // Decorative grass texture should not receive the contrast boost used
          // for readable foreground ink: that turned whole fields cream-white.
          if(surface==='land'&&light.grassy&&grassInk.has(i))return mixColor(readableInk(ink,background,1.6),ink,Math.min(1,light.sun*1.5));
          return highlights.has(i)?ink:readableInk(ink,background,i===C.sky?1.55:i===C.far||i===C.hill?2:1.6+light.sun*1.65);
        })));
        this.outlines[surface]=rows.map(band=>Array.from({length:Math.ceil(H/8)},(_,y)=>palette.map((ink,i)=>highlights.has(i)?readableInk(light.outline,band[Math.min(H-1,y*8+4)],3.5):null)));
      }
    }
    const ctx=this.terrainCtx;
    for(let i=0;i<W*H;i++){
      const char=grid.chars[i],color=grid.colors[i];
      if(char===this.previousChars[i]&&color===this.previousColors[i]&&this.world.water[i]===this.previousWater[i]&&grid.materials[i]===this.previousMaterials[i])continue;
      const x=i%W,y=(i/W)|0,left=Math.round(x*this.sx),top=Math.round(y*this.sy);
      const width=Math.round((x+1)*this.sx)-left,height=Math.round((y+1)*this.sy)-top;
      const surface=this.surfaceAt(i),band=this.bands[i],inkRow=y>>3;
      ctx.fillStyle=this.swatches[surface][band][y];ctx.fillRect(left,top,width,height);
      if(char!==32)ctx.drawImage(this.tile(char,this.ink[surface][band][inkRow][color],this.outlines[surface][band][inkRow][color]),left,top,width,height);
    }
    this.previousChars.set(grid.chars);this.previousColors.set(grid.colors);this.previousWater.set(this.world.water);
    this.previousMaterials.set(grid.materials);
    // Copy the cached terrain every frame so walking/hidden actors leave no trail.
    this.ctx.drawImage(this.terrain,0,0);
    this.effects.draw(this.ctx,this.world,scene,time,this.sx,this.sy,objects);
    // Rugs stay under everything; other props and characters share depth order.
    for(const actor of [...objects,...characters].sort((a,b)=>(a.floor?-1000:a.y)-(b.floor?-1000:b.y))){
      const surface=this.backdropAt(actor.x*this.sx,actor.y*this.sy);
      if(actor.item){
        this.items.draw(this.ctx,actor,actor.x*this.sx,actor.y*this.sy,this.sx*actor.scale,{surface,outline:light.outline});
        if(actor.occupant){
          const staged=occupiedGeometry(actor,actor.occupant.character,actor.occupant.inside,this.sx,this.sy);
          this.ctx.save();
          if(staged.clip){const r=staged.clip;this.ctx.beginPath();this.ctx.rect(r.x,r.y,r.w,r.h);this.ctx.clip();}
          drawCharacter(this.ctx,{...staged.character,sun:light.sun*.7,outline:light.outline},this.sx,this.sy,'#112521');
          this.ctx.restore();
          if(staged.front)this.items.draw(this.ctx,staged.front,actor.x*this.sx,actor.y*this.sy,this.sx*actor.scale,{shadow:false,surface,outline:light.outline});
          const held=heldNestGeometry(actor,staged.character,this.sx,this.sy);
          if(held)this.items.draw(this.ctx,held.model,held.x,held.y,held.cw,{shadow:false,surface,outline:light.outline});
        }
        if(actor.rider){
          const rider=ridingGeometry(actor,actor.rider.character,actor.rider.seat,actor.rider.inside,this.sx,this.sy);
          drawCharacter(this.ctx,{...rider,sun:light.sun,outline:light.outline},this.sx,this.sy,surface);
        }
      }
      else drawCharacter(this.ctx,{...actor,sun:light.sun,outline:light.outline,backdrop:(x,y)=>this.backdropAt(x,y)},this.sx,this.sy,surface);
    }
    this.hits=[...objects,...characters].filter(a=>a.item||a.visitor||a.story).map(a=>{
      const unit=this.sx*a.scale*(a.detailScale||1),width=a.width*unit,height=a.art.length*unit*1.5;
      return {id:a.id||scene.visitor?.id,kind:a.story?'story':a.visitor?'friend':'item',x:a.x*this.sx-width/2,y:a.y*this.sy-height,w:width,h:height};
    });
    this.frames++;
  }
  hit(nx,ny){const x=nx*this.canvas.width,y=ny*this.canvas.height;return [...(this.hits||[])].reverse().find(r=>x>=r.x&&x<=r.x+r.w&&y>=r.y&&y<=r.y+r.h);}
  surfaceAt(i){
    const material=this.world.grid.materials[i];
    return material===M.foliage?'foliage':material===M.wood?'wood':this.world.water[i]?'water':'land';
  }
  backdropAt(px,py){
    const x=Math.max(0,Math.min(W-1,Math.floor(px/this.sx))),y=Math.max(0,Math.min(H-1,Math.floor(py/this.sy))),i=y*W+x;
    return this.swatches[this.surfaceAt(i)][this.bands[i]][y];
  }
}
export class DisplayRenderer {
  constructor(canvas){
    this.canvas=canvas;this.ctx=canvas.getContext('2d',{alpha:false});
    this.classic=new GlyphRenderer(document.createElement('canvas'));this.scene=new SceneCanvas();
    this.interface=new InterfaceRenderer();
    this.mode='ultra';this.frames=0;this.lastTime=0;this.cost=0;this.peak=0;
  }
  get atlas(){return this.classic.atlas;}
  resize(cols,rows,scale,viewport=null){
    this.classic.resize(cols,rows,scale);
    this.viewport=viewport;
    const c=this.classic.canvas;
    const dpr=window.devicePixelRatio||1;
    const width=viewport?Math.round(viewport.width*dpr):c.width,height=viewport?Math.round(viewport.height*dpr):c.height;
    this.canvas.style.width=viewport?`${viewport.width}px`:c.style.width;this.canvas.style.height=viewport?`${viewport.height}px`:c.style.height;
    if(this.canvas.width!==width||this.canvas.height!==height){this.canvas.width=width;this.canvas.height=height;}
  }
  draw(frame,time=performance.now()){
    const begin=performance.now();this.classic.draw(frame);
    this.ctx.drawImage(this.classic.canvas,0,0);
    if(this.mode==='ultra'&&frame.scene){
      const s=frame.scene,r=s.rect,sx=this.classic.sx,sy=this.classic.sy;
      const full=Boolean(frame.ui);
      const x=full?0:Math.round(r.x*sx),y=full?0:Math.round(r.y*sy),w=full?this.canvas.width:Math.round(r.w*sx),h=full?this.canvas.height:Math.round(r.h*sy);
      this.scene.resize(w,h);this.scene.draw(s,time/1000,Math.min(.1,(time-this.lastTime)/1000||1/30));
      this.ctx.drawImage(this.scene.canvas,x,y,w,h);
      // Redraw the complete original modal, including blank cells. No game UI is
      // inferred or replaced: this preserves every menu and minigame action.
      if(s.overlay&&!frame.ui){
        const o=s.overlay,left=Math.floor(o.x*sx),top=Math.floor(o.y*sy),ow=Math.ceil(o.w*sx),oh=Math.ceil(o.h*sy);
        this.ctx.drawImage(this.classic.canvas,left,top,ow,oh,left,top,ow,oh);
      }
    }
    if(this.mode==='ultra'&&frame.ui){
      if(frame.ui.state==='title'){
        this.scene.resize(this.canvas.width,this.canvas.height);
        this.scene.draw({...TITLE_SCENE,hour:frame.ui.hour??12,motion:frame.ui.motion},time/1000,Math.min(.1,(time-this.lastTime)/1000||1/30));
        this.ctx.drawImage(this.scene.canvas,0,0);
      }
      this.interface.draw(this.ctx,this.canvas,frame,time,this.viewport);
    }
    this.lastTime=time;this.frames++;
    this.cost=performance.now()-begin;this.peak=Math.max(this.peak,this.cost);
  }
}
