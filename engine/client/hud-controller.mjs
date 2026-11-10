import {HUD_PANELS,HudLayout,IdleFade} from './hud-layout.mjs';
const KEY='cheese.hud.v1',$=id=>document.getElementById(id);
const inside=(r,x,y)=>x>=r.x&&y>=r.y&&x<=r.x+r.w&&y<=r.y+r.h;
export class HudController{
 constructor(renderer,{redraw,onEscape,blocked}={}){
  this.renderer=renderer;this.redraw=redraw;this.onEscape=onEscape;this.blocked=blocked;
  let saved;try{saved=JSON.parse(localStorage.getItem(KEY));}catch{}
  this.layout=new HudLayout(saved);renderer.interface.layout=this.layout;
  this.fade=new IdleFade(performance.now());this.editing=false;this.drag=null;this.suppressUntil=0;this.nodes=new Map();
  this.layer=document.createElement('div');this.layer.id='hud-handles';this.layer.dataset.hudUi='';document.body.append(this.layer);
  this.checkboxes=new Map();
  for(const [id,def] of Object.entries(HUD_PANELS)){
   const label=document.createElement('label'),input=document.createElement('input');input.type='checkbox';input.checked=this.layout.visible(id);input.dataset.panel=id;
   input.onchange=()=>{this.layout.show(id,input.checked);this.changed();};
   label.append(input,document.createTextNode(def.name));$('panel-switches').append(label);this.checkboxes.set(id,input);
  }
  $('idle-fade').checked=this.layout.autoFade;$('idle-fade').onchange=()=>{this.layout.autoFade=$('idle-fade').checked;this.changed();};
  $('pond-kit').onclick=() =>this.toggleKit();$('kit-recall').onclick=()=>this.toggleKit();$('kit-close').onclick=()=>this.closeKit();
  $('arrange').onclick=()=>{this.editing=!this.editing;this.closeKit();this.changed();};
  document.querySelectorAll('[data-layout-preset]').forEach(b=>b.onclick=()=>{this.layout.preset(b.dataset.layoutPreset);this.changed();});
  $('belt-close').onclick=()=>{this.layout.show('actions',false);this.changed();};
  this.bindDrag($('belt-grip'),'actions');this.bindDrag($('game-header'),'tools');
  $('game-header').tabIndex=0;$('game-header').setAttribute('aria-label','Move pond kit');
  for(const event of ['pointermove','pointerdown','keydown','wheel'])document.addEventListener(event,e=>this.activity(e),{capture:true,passive:false});
  document.addEventListener('click',e=>{if(performance.now()<this.suppressUntil){e.preventDefault();e.stopImmediatePropagation();}},{capture:true});
  document.addEventListener('pointerdown',e=>{if(this.open&&!e.target.closest('#pond-tools-panel,#pond-kit,#kit-recall'))this.closeKit();});
  document.addEventListener('keydown',e=>{
   if(e.key==='F2'&&!e.metaKey&&!e.ctrlKey){e.preventDefault();e.stopImmediatePropagation();this.toggleKit();}
   else if(e.key==='Escape'&&(this.open||this.editing)){e.preventDefault();e.stopImmediatePropagation();this.closeKit();this.editing=false;this.changed();}
  },true);
  window.addEventListener('blur',()=>this.finishDrag());
  window.addEventListener('focus',()=>this.wake());
  window.addEventListener('resize',()=>{this.finishDrag();for(const d of document.querySelectorAll('dialog[open]'))this.placeDialog(d);this.sync();});
  for(const dialog of document.querySelectorAll('dialog'))this.registerDialog(dialog);
  this.refreshControls();
 }
 get open(){return !$('pond-tools-panel').hidden;}
 persist(){try{localStorage.setItem(KEY,JSON.stringify(this.layout.save()));}catch{}}
 wake(){this.fade.wake(performance.now());this.renderer.interface.hudOpacity=1;document.body.style.setProperty('--hud-opacity','1');document.body.dataset.hudAsleep='false';}
 activity(e){
  if(e.type==='pointermove'){
   const key=e.clientX+','+e.clientY;if(key===this.pointer)return;this.pointer=key;
  }
  const asleep=this.fade.opacity<.15;this.wake();
  // Waking must never buy an item, select a hidden action or click through a HUD.
  if(asleep&&e.type!=='pointermove'){
   this.suppressUntil=performance.now()+350;e.preventDefault();e.stopImmediatePropagation();
  }
 }
 update(frame,now=performance.now()){
  this.frame=frame;const world=this.renderer.mode==='ultra'&&Boolean(frame?.scene&&frame?.ui);
  this.world=world;
  const eligible=world&&frame.ui.state==='playing'&&!frame.ui.modal&&!frame.ui.minigame&&!frame.meta.talking&&!this.open&&!this.editing&&!this.drag&&!this.blocked?.()&&$('error').hidden;
  const opacity=this.fade.update(now,{eligible,enabled:this.layout.autoFade,reducedMotion:frame?.ui?.motion===false});
  this.renderer.interface.hudOpacity=opacity;document.body.style.setProperty('--hud-opacity',String(opacity));document.body.dataset.hudAsleep=String(opacity<.15);
  document.body.dataset.arranging=String(this.editing&&world);$('arrange').setAttribute('aria-pressed',String(this.editing));
  if(this.drag&&(!world||Boolean(frame.ui.modal)!==(this.drag.id==='document')))this.finishDrag();
 }
 refreshControls(){for(const [id,input] of this.checkboxes)input.checked=this.layout.visible(id);}
 changed(){this.wake();this.persist();this.refreshControls();this.redraw?.();this.sync();}
 toggleKit(){if(this.open){this.closeKit();return;}this.wake();this.refreshControls();$('pond-tools-panel').hidden=false;$('pond-kit').setAttribute('aria-expanded','true');$('kit-close').focus();}
 closeKit(){if(!this.open)return;$('pond-tools-panel').hidden=true;$('pond-kit').setAttribute('aria-expanded','false');$('world').focus();this.wake();}
 point(e){const c=this.renderer.canvas.getBoundingClientRect(),i=this.renderer.interface;return {x:(e.clientX-c.left)/c.width*i.width,y:(e.clientY-c.top)/c.height*i.height};}
 position(node,r){
  const c=this.renderer.canvas.getBoundingClientRect(),i=this.renderer.interface,sx=c.width/i.width,sy=c.height/i.height;
  Object.assign(node.style,{left:(c.left+r.x*sx)+'px',top:(c.top+r.y*sy)+'px',width:r.w*sx+'px',height:r.h*sy+'px'});
  node.style.setProperty('--panel-scale',String(sx));
 }
 sync(){
  if(!this.frame)return;
  const i=this.renderer.interface,active=this.world&&!this.frame.ui.modal;
  this.layer.hidden=!this.world;this.layer.classList.toggle('modal-handles',Boolean(this.frame.ui.modal));
  const shown=new Set();
  if(active)for(const [order,r] of i.hudRects.entries()){const n=this.handle(r.id,HUD_PANELS[r.id].name);this.position(n,r);n.style.zIndex=String(order);n.hidden=false;shown.add(r.id);}
  const doc=i.visibleDocument;
  if(this.world&&this.frame.ui.modal&&doc?.movable){const n=this.handle('document','Move '+doc.title);this.position(n,doc);n.hidden=false;shown.add('document');}
  for(const [id,n] of this.nodes)n.hidden=!shown.has(id);
  for(const [id,node] of [['tools',$('game-header')],['actions',$('action-belt')]]){
   node.hidden=this.world&&!this.layout.visible(id);
   node.inert=id==='actions'&&this.world&&Boolean(this.frame.ui.modal);
   if(this.world)this.position(node,this.layout.rect(id,i.width,i.height));else node.removeAttribute('style');
  }
  $('kit-recall').hidden=!this.world||this.layout.visible('tools');
  this.refreshControls();
 }
 handle(id,name){
  if(this.nodes.has(id))return this.nodes.get(id);
  const node=document.createElement('div');node.className='hud-handle';node.dataset.panel=id;
  const grip=document.createElement('button');grip.className='hud-grip';grip.setAttribute('aria-label','Move '+name);grip.title='Drag to move · arrow keys when focused';
  const close=document.createElement('button');close.className='hud-close';close.textContent='×';close.setAttribute('aria-label',id==='document'?'Back / close window':'Close '+name);
  close.onclick=()=>{if(id==='document')this.onEscape?.();else{this.layout.show(id,false);this.changed();}};
  node.append(grip,close);this.layer.append(node);this.nodes.set(id,node);this.bindDrag(grip,id);return node;
 }
 bindDrag(handle,id){
  handle.classList.add('movable-grip');
  handle.addEventListener('pointerdown',e=>{
   if(e.button!==0||!this.world||this.open||this.blocked?.()||e.target.closest('button')&&e.target!==handle)return;
   const i=this.renderer.interface,r=id==='document'?i.visibleDocument:this.layout.rect(id,i.width,i.height);
   if(!r)return;e.preventDefault();e.stopPropagation();this.wake();
   const p=this.point(e);this.drag={id,r:{...r},dx:p.x-r.x,dy:p.y-r.y,handle,pointer:e.pointerId,moved:false};handle.setPointerCapture(e.pointerId);
  });
  handle.addEventListener('pointermove',e=>{
   if(this.drag?.handle!==handle||this.drag.pointer!==e.pointerId)return;
   const d=this.drag,p=this.point(e),i=this.renderer.interface;
   if(Math.abs(p.x-d.dx-d.r.x)+Math.abs(p.y-d.dy-d.r.y)>2)d.moved=true;
   if(id==='document')this.layout.moveDialog(d.r.id,p.x-d.dx,p.y-d.dy,d.r,i.width,i.height);
   else this.layout.move(id,p.x-d.dx,p.y-d.dy,i.width,i.height);
   this.redraw?.();this.sync();
  });
  for(const event of ['pointerup','pointercancel','lostpointercapture'])handle.addEventListener(event,()=>{if(this.drag?.handle===handle)this.finishDrag();});
  handle.addEventListener('keydown',e=>{
   if(!this.world||!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key))return;
   e.preventDefault();e.stopPropagation();const i=this.renderer.interface,r=id==='document'?i.visibleDocument:this.layout.rect(id,i.width,i.height),step=e.shiftKey?40:10;
   const x=r.x+(e.key==='ArrowRight'?step:e.key==='ArrowLeft'?-step:0),y=r.y+(e.key==='ArrowDown'?step:e.key==='ArrowUp'?-step:0);
   if(id==='document')this.layout.moveDialog(r.id,x,y,r,i.width,i.height);else this.layout.move(id,x,y,i.width,i.height);this.changed();
  });
 }
 finishDrag(){if(!this.drag)return;const d=this.drag;this.drag=null;if(d.moved)this.suppressUntil=performance.now()+150;this.persist();if(d.handle.hasPointerCapture?.(d.pointer))d.handle.releasePointerCapture(d.pointer);}
 blocks(e){if(!this.world||this.fade.opacity<.15)return false;const p=this.point(e);return this.renderer.interface.hudRects.some(r=>inside(r,p.x,p.y));}
 registerDialog(dialog){
  const handle=dialog.querySelector('header,.gallery-head');if(!handle)return;
  handle.classList.add('dialog-grip');handle.title='Drag this heading to move the window';handle.tabIndex=0;handle.setAttribute('aria-label','Move '+(dialog.getAttribute('aria-label')||'window'));
  let drag;
  const save=()=>{if(!drag)return;const r=dialog.getBoundingClientRect();this.layout.moveDialog('html:'+dialog.id,r.x,r.y,{w:r.width,h:r.height},innerWidth,innerHeight);drag=null;this.persist();};
  handle.addEventListener('pointerdown',e=>{if(e.button||e.target.closest('button,input,select'))return;const r=dialog.getBoundingClientRect();drag={x:e.clientX-r.x,y:e.clientY-r.y};e.preventDefault();handle.setPointerCapture(e.pointerId);});
  handle.addEventListener('pointermove',e=>{if(!drag)return;const r=dialog.getBoundingClientRect();this.moveHtml(dialog,e.clientX-drag.x,e.clientY-drag.y,r);});
  for(const event of ['pointerup','pointercancel','lostpointercapture'])handle.addEventListener(event,save);
  handle.addEventListener('keydown',e=>{if(e.target!==handle||!e.key.startsWith('Arrow'))return;e.preventDefault();e.stopPropagation();const r=dialog.getBoundingClientRect(),d=e.shiftKey?40:10;this.moveHtml(dialog,r.x+(e.key==='ArrowLeft'?-d:e.key==='ArrowRight'?d:0),r.y+(e.key==='ArrowUp'?-d:e.key==='ArrowDown'?d:0),r);drag={};save();});
  new MutationObserver(()=>{if(dialog.open)this.placeDialog(dialog);else save();}).observe(dialog,{attributes:true,attributeFilter:['open']});
 }
 moveHtml(dialog,x,y,r){Object.assign(dialog.style,{position:'fixed',margin:'0',left:Math.max(8,Math.min(innerWidth-r.width-8,x))+'px',top:Math.max(8,Math.min(innerHeight-r.height-8,y))+'px'});}
 placeDialog(dialog){const r=dialog.getBoundingClientRect(),p=this.layout.dialogRect('html:'+dialog.id,{x:(innerWidth-r.width)/2,y:(innerHeight-r.height)/2,w:r.width,h:r.height},innerWidth,innerHeight);this.moveHtml(dialog,p.x,p.y,r);}
}
