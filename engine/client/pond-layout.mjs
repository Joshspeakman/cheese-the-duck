import {SceneCanvas} from './ultra-renderer.mjs';
import {catalog} from './ultra-items.mjs';
import {surfaceFits,itemSurface} from './habitat-ground.mjs';

const names=new Map(catalog.map(i=>[i.id,i.name]));
const name=id=>names.get(id)||String(id).replaceAll('_',' ');
const node=(tag,text,cls)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;};
export function layoutBounds(f,x,y){
 const w=f.width*20/192+.5,h=f.height*12/47;
 return {x:x-w/2,y:y-h,w,h:h+.65,floor:f.floor};
}
export function layoutCheck(layout,id,x,y,instance=null){
 const item=layout?.items.find(i=>i.id===id);
 if(!item)return {ok:false,message:'Choose an owned belonging.'};
 if(instance&&layout.copies&&!layout.copies.some(p=>p.instance===instance&&p.id===id))return {ok:false,message:'That copy is no longer available here. Choose another belonging.'};
 if(!Number.isFinite(x)||!Number.isFinite(y))return {ok:false,message:'Choose a point inside the habitat.'};
 const box=layoutBounds(item.footprint,x,y);
 if(box.x<.2||box.x+box.w>19.8||x>124*20/132||y<1||y>37*12/42)return {ok:false,message:'Leave room around the edge for the whole object.'};
 if(46+y*47/12-item.footprint.height<2)return {ok:false,message:'That tall object needs a spot farther down the bank.'};
 if(!surfaceFits(id,box,y))return {ok:false,message:itemSurface(id)==='water'?'That belongs on the water.':'Keep its feet on the dry bank.'};
 for(const other of [...layout.placed.filter(p=>instance?p.instance!==instance:p.id!==id),...layout.obstacles]){
  const b=other.box;
  if(box.floor===b.floor&&box.x<b.x+b.w&&box.x+box.w>b.x&&box.y<b.y+b.h&&box.y+box.h>b.y)
   return {ok:false,message:'That spot overlaps '+name(other.id)+'.'};
 }
 return {ok:true,message:'There is room here. Place it when you like the preview.'};
}

// Draft positions stay in this notebook until the simulation accepts a command.
// The same full-world camera and native renderer show the actual artwork scale.
export class PondArrangement{
 constructor(journal){this.journal=journal;this.renderer=new SceneCanvas();this.id=null;this.draft=null;this.pending=null;this.lastPaint=-Infinity;}
 select(id,instance=null){
  const copy=this.choices.find(p=>p.id===id&&(!instance||p.instance===instance));
  this.id=id;this.instance=instance||copy?.instance||null;this.journal.selected=id;this.journal.selectedInstance=this.instance;
  const placed=this.layout?.placed.find(p=>p.id===id&&(!this.instance||p.instance===this.instance));
  this.draft=placed?{x:placed.x,y:placed.y}:{x:10,y:5};
  this.feedback='';this.lastPaint=-Infinity;
 }
 get layout(){return this.journal.world?.layout;}
 get choices(){
  const l=this.layout;if(!l)return [];
  return l.items.flatMap(item=>{const copies=l.copies?.filter(p=>p.id===item.id)||[];return copies.length?copies.map((p,i)=>({...p,label:name(p.id)+(copies.length>1?` · copy ${i+1}`:'')})):[{...item,label:name(item.id)}];});
 }
 options(){
  const choices=this.choices,keys=choices.map(p=>p.instance||p.id).sort().join('|');
  if([...this.selectControl.options].map(p=>p.value).sort().join('|')!==keys){
   this.selectControl.replaceChildren();
   for(const c of [...choices].sort((a,b)=>a.label.localeCompare(b.label))){const option=node('option');option.value=c.instance||c.id;this.selectControl.append(option);}
  }
  for(const option of this.selectControl.options){const c=choices.find(p=>(p.instance||p.id)===option.value);option.textContent=c.label+(c.placed?' · placed':' · stored');}
  this.selectControl.value=this.instance||this.id||'';
 }
 get home(){return this.journal.world?.location==='Home Pond';}
 get verdict(){return layoutCheck(this.layout,this.id,this.draft?.x,this.draft?.y,this.instance);}
 mount(grid){
  const j=this.journal,l=this.layout;
  if(!l){grid.append(j.card('Arrange the habitat','Continue your game to arrange your belongings.'));return;}
  if(this.id!==(j.selected||l.items[0]?.id)||this.instance!==(j.selectedInstance||null))this.select(j.selected||l.items[0]?.id,j.selectedInstance);
  const c=j.card('Make a place for your things','Choose a belonging, then click or drag in the preview. Arrow keys make small adjustments. Place here commits the move; closing the notebook leaves a preview untouched.');
  c.classList.add('pond-arrangement');
  const toolbar=node('div',undefined,'arrange-toolbar');
  this.selectControl=node('select');this.selectControl.setAttribute('aria-label','Belonging to arrange');
  this.options();this.selectControl.onchange=()=>{const c=this.choices.find(p=>(p.instance||p.id)===this.selectControl.value);this.select(c.id,c.instance);this.update();};
  toolbar.append(this.selectControl);c.append(toolbar);
  this.canvas=node('canvas',undefined,'arrange-preview');this.canvas.width=1000;this.canvas.height=520;
  this.canvas.tabIndex=0;this.canvas.setAttribute('role','group');this.canvas.setAttribute('aria-label','Habitat arrangement preview. Click to position the selected item, or use arrow keys. Press Enter to place.');
  c.append(this.canvas);
  const position=e=>{
   if(!this.home||this.pending||!this.draft)return;
   const r=this.canvas.getBoundingClientRect(),gx=(e.clientX-r.left)/r.width*240,gy=(e.clientY-r.top)/r.height*110;
   this.draft={x:Math.max(.5,Math.min(19.5,Math.round((gx-24)/192*20*4)/4)),y:Math.max(1,Math.min(11,Math.round((gy-46)/47*12*4)/4))};
   this.feedback='';this.lastPaint=-Infinity;this.update();
  };
  this.canvas.onpointerdown=e=>{if(e.button!==0)return;this.canvas.focus();this.canvas.setPointerCapture(e.pointerId);position(e);};
  this.canvas.onpointermove=e=>{if(this.canvas.hasPointerCapture(e.pointerId))position(e);};
  this.canvas.onpointerup=e=>{if(this.canvas.hasPointerCapture(e.pointerId))this.canvas.releasePointerCapture(e.pointerId);};
  this.canvas.onkeydown=e=>{
   const direction={ArrowLeft:[-1,0],ArrowRight:[1,0],ArrowUp:[0,-1],ArrowDown:[0,1]}[e.key];
   if(direction){e.preventDefault();if(!this.home||this.pending||!this.draft)return;
    const step=e.shiftKey?1:.25;
    this.draft={x:Math.max(.5,Math.min(19.5,this.draft.x+direction[0]*step)),y:Math.max(1,Math.min(11,this.draft.y+direction[1]*step))};
    this.feedback='';this.lastPaint=-Infinity;this.update();
   }else if(e.key==='Enter'){e.preventDefault();if(!this.place.disabled)this.send('layout_place');}
  };
  this.description=node('p',undefined,'arrange-description');this.description.setAttribute('role','status');c.insertBefore(this.description,this.canvas);
  const actions=node('div',undefined,'arrange-actions');
  this.place=node('button','Place here');this.place.onclick=()=>this.send('layout_place');
  this.auto=node('button','Find a free spot');this.auto.onclick=()=>this.send('layout_auto');
  this.store=node('button','Put in storage');this.store.onclick=()=>this.send('layout_store');
  actions.append(this.place,this.auto,this.store);toolbar.append(actions);
  c.append(node('small','The outline reserves room for the whole drawing and its movement. Rugs may sit beneath furniture. A full habitat never costs you an item: keep it in storage and swap things around.'));
  grid.append(c);this.update();
 }
 send(action){
  if(this.pending||!this.home||!this.id||(action==='layout_place'&&!this.verdict.ok))return;
  this.pending={sequence:this.layout.reply?.sequence||0,action,id:this.id};
  this.journal.command(action,this.id,{...(action==='layout_place'?this.draft:{}),instance:this.instance});
  this.update();
 }
 update(){
  if(!this.canvas?.isConnected)return;
  const l=this.layout,reply=l?.reply;
  if(this.pending&&reply&&reply.sequence>this.pending.sequence&&reply.target===this.pending.id){
   this.pending=null;this.feedback=reply.message;
   if(reply.ok){const placed=l.placed.find(p=>p.id===this.id&&(!this.instance||p.instance===this.instance));if(placed){this.draft={x:placed.x,y:placed.y};this.instance=placed.instance||null;this.journal.selectedInstance=this.instance;}}
   this.lastPaint=-Infinity;
  }
  const verdict=this.verdict,placed=l?.placed.some(p=>p.id===this.id&&(!this.instance||p.instance===this.instance));
  this.place.disabled=!this.home||!!this.pending||!verdict.ok;
  this.auto.disabled=!this.home||!!this.pending||!this.id||!!this.instance&&!this.choices.some(p=>p.id===this.id&&p.instance===this.instance);
  this.store.disabled=!this.home||!!this.pending||!placed;
  this.selectControl.disabled=!!this.pending||!l?.items.length;
  this.options();
  this.description.textContent=!this.home?'Come back to Home Pond to arrange your belongings.':this.pending?'Finding a place…':this.feedback||(!this.id?'Your placeable belongings will appear here.':name(this.id)+' · Preview · '+verdict.message);
  this.description.dataset.valid=String(verdict.ok);
  this.journal.status.textContent=this.pending?'Arranging your habitat…':'Arrange · '+(this.home?'Home Pond':'Return home to place things');
 }
 paint(time){
  if(!this.canvas?.isConnected||time-this.lastPaint<.12)return;
  const source=this.journal.frame?.scene;if(!source)return;
  this.lastPaint=time;
  const draft=this.home&&this.id&&this.draft&&this.choices.some(i=>i.id===this.id&&(!this.instance||i.instance===this.instance));
  const items=[...(source.items||[])].filter(i=>!draft||i.id!==this.id||(this.instance&&i.instance!==this.instance));
  if(draft)items.push({id:this.id,instance:this.instance,x:this.draft.x*132/20,y:this.draft.y*42/12});
  const scene={...source,camera:{x:0,y:0,w:132,h:42},items,particles:false,weatherEffects:false,
   living:{...source.living,plan:source.living?.plan?.target===this.id&&(!this.instance||source.living.plan.instance===this.instance)?null:source.living?.plan}};
  this.renderer.resize(this.canvas.width,this.canvas.height);this.renderer.draw(scene,time,.12);
  const ctx=this.canvas.getContext('2d');ctx.drawImage(this.renderer.canvas,0,0);
  if(draft){
   const footprint=this.layout.items.find(i=>i.id===this.id).footprint,box=layoutBounds(footprint,this.draft.x,this.draft.y);
   const sx=this.canvas.width/240,sy=this.canvas.height/110;
   const x=(24+box.x/20*192)*sx,y=(46+box.y/12*47)*sy,w=box.w/20*192*sx,h=box.h/12*47*sy;
   ctx.strokeStyle=this.verdict.ok?'#ffe7a0':'#ff9a8c';ctx.lineWidth=2;ctx.setLineDash([6,5]);ctx.strokeRect(x,y,w,h);ctx.setLineDash([]);
   const px=(24+this.draft.x/20*192)*sx,py=(46+this.draft.y/12*47)*sy;
   ctx.beginPath();ctx.moveTo(px-7,py);ctx.lineTo(px+7,py);ctx.moveTo(px,py-7);ctx.lineTo(px,py+7);ctx.stroke();
  }
 }
}
