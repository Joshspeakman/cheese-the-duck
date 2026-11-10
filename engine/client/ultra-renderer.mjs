import { GlyphRenderer } from './renderer.mjs';
import { LivingWorld } from './ultra-world.mjs';
import { drawCharacter } from './ultra-characters.mjs';
import { ItemPainter } from './ultra-items.mjs';
import { SceneEffects,luminousPalette } from './scene-effects.mjs';
import { W,H } from './ultra-grid.mjs';
import { InterfaceRenderer } from './interface-renderer.mjs';

const TITLE_SCENE={biome:'pond',location:'Home Pond',season:'spring',hour:17,weather:'sunny',intensity:.5,motion:true,particles:true,weatherEffects:true,
  camera:{x:0,y:0,w:132,h:42},duck:{name:'Cheese',x:65,y:24,hidden:true,stage:'adult',state:'idle',cosmetics:{}},items:[],structures:[],visitor:null,interaction:null};

export class SceneCanvas {
  constructor(){
    this.canvas=document.createElement('canvas');this.ctx=this.canvas.getContext('2d',{alpha:false});
    this.terrain=document.createElement('canvas');this.terrainCtx=this.terrain.getContext('2d',{alpha:false});
    this.world=new LivingWorld();this.atlas=new Map();this.previousChars=new Uint8Array(W*H);this.previousColors=new Uint8Array(W*H);
    this.paletteKey='';this.frames=0;this.items=new ItemPainter();this.effects=new SceneEffects();
  }
  resize(width,height){
    width=Math.round(width);height=Math.round(height);
    if(this.canvas.width===width&&this.canvas.height===height)return;
    this.canvas.width=width;this.canvas.height=height;this.terrain.width=width;this.terrain.height=height;this.sx=width/W;this.sy=height/H;
    this.previousChars.fill(0);this.atlas.clear();this.paletteKey='';
  }
  tile(char,color){
    const key=char+':'+color;
    if(this.atlas.has(key))return this.atlas.get(key);
    const tile=document.createElement('canvas');tile.width=Math.ceil(this.sx);tile.height=Math.ceil(this.sy);
    const ctx=tile.getContext('2d');ctx.fillStyle=color;
    ctx.font=`600 ${Math.max(6,this.sy*1.14)}px Menlo, monospace`;
    ctx.textBaseline='middle';ctx.textAlign='center';
    ctx.fillText(String.fromCharCode(char),tile.width/2,tile.height*.52,tile.width);
    this.atlas.set(key,tile);return tile;
  }
  draw(scene,time,dt){
    const result=this.world.render(scene,time,dt),{grid,characters,objects}=result;
    const palette=luminousPalette(result.palette,this.effects.level),key=palette.join('');
    if(key!==this.paletteKey){this.previousChars.fill(0);this.paletteKey=key;this.atlas.clear();}
    const ctx=this.terrainCtx;
    for(let i=0;i<W*H;i++){
      const char=grid.chars[i],color=grid.colors[i];
      if(char===this.previousChars[i]&&color===this.previousColors[i])continue;
      const x=i%W,y=(i/W)|0,left=Math.round(x*this.sx),top=Math.round(y*this.sy);
      const width=Math.round((x+1)*this.sx)-left,height=Math.round((y+1)*this.sy)-top;
      ctx.fillStyle=palette[0];ctx.fillRect(left,top,width,height);
      if(char!==32)ctx.drawImage(this.tile(char,palette[color]),left,top,width,height);
    }
    this.previousChars.set(grid.chars);this.previousColors.set(grid.colors);
    // Copy the cached terrain every frame so walking/hidden actors leave no trail.
    this.ctx.drawImage(this.terrain,0,0);
    this.effects.draw(this.ctx,this.world,scene,time,this.sx,this.sy,objects);
    // Rugs stay under everything; other props and characters share depth order.
    for(const actor of [...objects,...characters].sort((a,b)=>(a.floor?-1000:a.y)-(b.floor?-1000:b.y))){
      if(actor.item)this.items.draw(this.ctx,actor,actor.x*this.sx,actor.y*this.sy,this.sx*actor.scale);
      else drawCharacter(this.ctx,actor,this.sx,this.sy,palette[0]);
    }
    this.frames++;
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
        this.scene.draw({...TITLE_SCENE,motion:frame.ui.motion},time/1000,Math.min(.1,(time-this.lastTime)/1000||1/30));
        this.ctx.drawImage(this.scene.canvas,0,0);
      }
      this.interface.draw(this.ctx,this.canvas,frame,time,this.viewport);
    }
    this.lastTime=time;this.frames++;
    this.cost=performance.now()-begin;this.peak=Math.max(this.peak,this.cost);
  }
}
