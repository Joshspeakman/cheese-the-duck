import { GlyphRenderer } from './renderer.mjs';
import { LivingWorld } from './ultra-world.mjs';
import { W,H } from './ultra-grid.mjs';

export class SceneCanvas {
  constructor(){
    this.canvas=document.createElement('canvas');this.ctx=this.canvas.getContext('2d',{alpha:false});
    this.world=new LivingWorld();this.atlas=new Map();this.previousChars=new Uint8Array(W*H);this.previousColors=new Uint8Array(W*H);
    this.paletteKey='';this.frames=0;
  }
  resize(width,height){
    width=Math.round(width);height=Math.round(height);
    if(this.canvas.width===width&&this.canvas.height===height)return;
    this.canvas.width=width;this.canvas.height=height;this.sx=width/W;this.sy=height/H;
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
    const {grid,palette}=this.world.render(scene,time,dt),key=palette.join('');
    if(key!==this.paletteKey){this.previousChars.fill(0);this.paletteKey=key;this.atlas.clear();}
    const ctx=this.ctx;
    for(let i=0;i<W*H;i++){
      const char=grid.chars[i],color=grid.colors[i];
      if(char===this.previousChars[i]&&color===this.previousColors[i])continue;
      const x=i%W,y=(i/W)|0,left=Math.round(x*this.sx),top=Math.round(y*this.sy);
      const width=Math.round((x+1)*this.sx)-left,height=Math.round((y+1)*this.sy)-top;
      ctx.fillStyle=palette[0];ctx.fillRect(left,top,width,height);
      if(char!==32)ctx.drawImage(this.tile(char,palette[color]),left,top,width,height);
    }
    this.previousChars.set(grid.chars);this.previousColors.set(grid.colors);this.frames++;
  }
}
export class DisplayRenderer {
  constructor(canvas){
    this.canvas=canvas;this.ctx=canvas.getContext('2d',{alpha:false});
    this.classic=new GlyphRenderer(document.createElement('canvas'));this.scene=new SceneCanvas();
    this.mode='ultra';this.frames=0;this.lastTime=0;this.cost=0;this.peak=0;
  }
  get atlas(){return this.classic.atlas;}
  resize(cols,rows,scale){
    this.classic.resize(cols,rows,scale);
    const c=this.classic.canvas;
    this.canvas.style.width=c.style.width;this.canvas.style.height=c.style.height;
    if(this.canvas.width!==c.width||this.canvas.height!==c.height){this.canvas.width=c.width;this.canvas.height=c.height;}
  }
  draw(frame,time=performance.now()){
    const begin=performance.now();this.classic.draw(frame);
    this.ctx.drawImage(this.classic.canvas,0,0);
    if(this.mode==='ultra'&&frame.scene){
      const s=frame.scene,r=s.rect,sx=this.classic.sx,sy=this.classic.sy;
      const x=Math.round(r.x*sx),y=Math.round(r.y*sy),w=Math.round(r.w*sx),h=Math.round(r.h*sy);
      this.scene.resize(w,h);this.scene.draw(s,time/1000,Math.min(.1,(time-this.lastTime)/1000||1/30));
      this.ctx.drawImage(this.scene.canvas,x,y,w,h);
      // Redraw the complete original modal, including blank cells. No game UI is
      // inferred or replaced: this preserves every menu and minigame action.
      if(s.overlay){
        const o=s.overlay,left=Math.floor(o.x*sx),top=Math.floor(o.y*sy),ow=Math.ceil(o.w*sx),oh=Math.ceil(o.h*sy);
        this.ctx.drawImage(this.classic.canvas,left,top,ow,oh,left,top,ow,oh);
      }
    }
    this.lastTime=time;this.frames++;
    this.cost=performance.now()-begin;this.peak=Math.max(this.peak,this.cost);
  }
}
