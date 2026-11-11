import {ChatFade} from './chat-fade.mjs';
import {CHAT_TABS,inTab,parseChat,channelLabel,spoken} from './chat-model.mjs';
const el=(tag,text,cls)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;};
const HELP='Enter / T: chat · Enter: send · Esc: return · ↑ / ↓: sent history · /s: say to Cheese · /w Name: whisper · /r: reply · /clear: clear this view.';
export class PondChat{
 constructor(renderer,hud){
  this.renderer=renderer;this.hud=hud;renderer.interface.chatExternal=true;this.fade=new ChatFade(performance.now());this.hovered=false;
  this.stream=null;this.frame=null;this.editing=false;this.tab='general';this.target='cheese';this.channel='say';this.lastWhisper=null;
  this.rows=[];this.local=[];this.high=0;this.clearThrough=0;this.unread=0;this.badges={general:0,conversation:0,world:0};this.scrolls={};this.follow=true;
  this.sent=[];this.historyIndex=0;this.draft='';this.inflight=null;this.lastPending='';this.lastVoice='';
  this.root=el('section',undefined,'pond-chat');this.root.id='pond-chat';this.root.dataset.hudUi='';this.root.setAttribute('aria-label','Pond chat');this.root.hidden=true;
  const top=el('div',undefined,'chat-heading');this.tabs=el('div',undefined,'chat-tabs');this.tabs.setAttribute('role','tablist');this.tabs.setAttribute('aria-label','Chat channels');
  for(const [id,label] of CHAT_TABS){const b=el('button',label,'chat-tab');b.dataset.chatTab=id;b.setAttribute('role','tab');b.onclick=()=>this.setTab(id);this.tabs.append(b);}
  this.grip=el('button','⠿','chat-grip');this.grip.setAttribute('aria-label','Move pond chat');this.grip.title='Drag to move chat';hud.bindDrag(this.grip,'chat');
  const close=el('button','×','chat-close');close.setAttribute('aria-label','Close pond chat');close.onclick=()=>{this.park();hud.layout.show('chat',false);hud.changed();this.sync();};
  top.append(this.tabs,this.grip,close);
  this.log=el('div',undefined,'chat-scroll');this.log.tabIndex=0;this.log.setAttribute('role','log');this.log.setAttribute('aria-label','Pond conversation history');this.log.setAttribute('aria-live','polite');this.log.setAttribute('aria-relevant','additions');
  this.log.onscroll=()=>{this.follow=this.log.scrollHeight-this.log.scrollTop-this.log.clientHeight<24;if(this.follow){this.unread=0;this.updateUnread();}};
  this.jump=el('button','↓ Latest','chat-latest');this.jump.hidden=true;this.jump.onclick=()=>this.bottom();
  this.form=el('form',undefined,'chat-composer');this.label=el('label','Say to Cheese:','chat-to');this.label.htmlFor='pond-chat-input';
  this.input=el('input',undefined,'chat-input');this.input.id='pond-chat-input';this.input.type='text';this.input.maxLength=1000;this.input.autocomplete='off';this.input.spellcheck=true;this.input.setAttribute('aria-label','Message to Cheese');this.input.placeholder='Press Enter to chat…';
  this.send=el('button','↵','chat-send');this.send.type='submit';this.send.setAttribute('aria-label','Send chat message');this.send.title='Send · Enter';
  this.form.append(this.label,this.input,this.send);this.form.onsubmit=e=>{e.preventDefault();this.submit();};
  this.status=el('div','Enter to chat · /help','chat-status');this.status.setAttribute('role','status');
  this.resize=el('button','◢','chat-resize');this.resize.setAttribute('aria-label','Resize pond chat');this.resize.title='Drag to resize · arrow keys when focused';
  this.root.append(top,this.log,this.jump,this.form,this.status,this.resize);document.body.append(this.root);
  this.root.addEventListener('keydown',e=>this.key(e));this.root.addEventListener('pointerdown',()=>hud.wake());
  this.input.onfocus=()=>{this.editing=true;this.root.classList.add('composing');this.input.placeholder='Say something…';hud.wake();};
  this.input.onblur=()=>{this.editing=false;this.root.classList.remove('composing');this.input.placeholder='Press Enter to chat…';};
  this.input.oninput=()=>{this.draft=this.input.value;this.historyIndex=this.sent.length;this.status.textContent=this.stream?.pending?`${this.stream.pending} is thinking…`:'Enter to send · Esc to return';};
  this.root.addEventListener('wheel',e=>e.stopPropagation(),{passive:true});this.root.addEventListener('paste',e=>e.stopPropagation());
  this.recall=el('button','Chat · Enter','chat-recall');this.recall.id='chat-recall';this.recall.dataset.hudUi='';this.recall.hidden=true;this.recall.setAttribute('aria-label','Open pond chat');this.recall.onclick=()=>this.open();document.body.append(this.recall);
  this.root.addEventListener('pointerenter',()=>{this.hovered=true;this.fade.wake(performance.now());});
  this.root.addEventListener('pointerleave',()=>{this.hovered=false;if(this.fade.opacity>.1)this.fade.wake(performance.now());});
  this.root.addEventListener('keydown',()=>this.fade.wake(performance.now()));
  this.root.addEventListener('wheel',()=>this.fade.wake(performance.now()),{passive:true});
  this.bindResize();
 }
 get active(){return this.editing||Boolean(this.resizeDrag);}
 get available(){return this.renderer.mode==='ultra'&&this.frame?.ui?.state==='playing'&&Boolean(this.frame.scene)&&!this.frame.ui.modal&&!this.frame.ui.minigame&&!this.frame.meta.talking;}
 update(frame){
  this.frame=frame;this.root.classList.toggle('high-contrast',Boolean(frame?.ui?.highContrast));const data=frame?.ui?.chatStream;
  if(data){
   let receiptError='';
   const changed=this.stream?.session!==data.session;
   if(changed){this.fade.wake(performance.now());this.stream=data;this.rows=[];this.local=[];this.high=0;this.clearThrough=0;this.unread=0;this.sent=[];this.historyIndex=0;this.target='cheese';this.channel='say';this.lastWhisper=null;this.badges={general:0,conversation:0,world:0};this.follow=true;this.log.replaceChildren();this.park();this.input.value='';this.input.readOnly=false;this.inflight=null;this.lastPending='';}
   this.stream=data;
   const arrivals=data.entries.filter(r=>r.id>this.high);
   if(arrivals.length){
    if(arrivals.some(spoken))this.fade.spoke(performance.now());
    for(const row of arrivals){
     if(row.channel==='whisper'&&row.speaker!=='player')this.lastWhisper=row.speaker;
     if(!changed)for(const [id] of CHAT_TABS)if(id!==this.tab&&inTab(row,id))this.badges[id]++;
    }
    if(!this.follow&&!changed)this.unread+=arrivals.filter(r=>inTab(r,this.tab)).length;
    this.high=Math.max(this.high,...arrivals.map(r=>r.id));this.rows=data.entries.slice();this.renderLog();
   }
   if(this.inflight){
    const receipt=data.receipts.find(r=>r.id===this.inflight.id);
    if(receipt){
     const pending=this.inflight;this.inflight=null;this.input.readOnly=false;
     if(receipt.accepted){this.sent.push(pending.raw);this.sent=this.sent.slice(-50);this.historyIndex=this.sent.length;this.input.value='';this.draft='';this.park();this.bottom();}
     else{this.input.value=pending.raw;receiptError=receipt.message;if(this.available)this.open();}
    }
   }
   const voice=data.voice?.source||'';
   if(data.pending!==this.lastPending||voice!==this.lastVoice){this.lastPending=data.pending;this.lastVoice=voice;this.status.textContent=data.pending?`${data.pending} is thinking…`:voice==='authored'?'Local voice unavailable · authored dialogue · /help':'Enter to chat · /help';}
   if(receiptError)this.status.textContent=receiptError;
   this.status.title=data.voice?.detail||this.status.textContent;
   this.updateLabels();this.updateUnread();
  }
  this.sync();
 }
 sync(){
  const wasHidden=this.root.hidden,show=this.available&&this.hud.layout.visible('chat');this.root.hidden=!show;
  if(!show){this.hovered=false;if(this.editing)this.park();}
  const i=this.renderer.interface,opacity=this.fade.update(performance.now(),{held:this.active||this.hovered||this.root.contains(document.activeElement)||Boolean(this.stream?.pending)||Boolean(this.inflight)||this.hud.editing,reducedMotion:this.frame?.ui?.motion===false});
  const quiet=opacity<.1;this.root.style.setProperty('--chat-opacity',String(opacity));this.root.dataset.quiet=String(quiet);this.root.inert=quiet;i.chatQuiet=quiet;this.recall.hidden=!show||!quiet;
  if(show){const h=this.log.clientHeight,r=this.hud.layout.rect('chat',i.width,i.height);this.hud.position(this.root,r);this.hud.position(this.recall,{x:r.x,y:r.y+r.h-27,w:120,h:27});if(this.follow&&(wasHidden||h!==this.log.clientHeight))this.bottom();}
 }
 open(prefill=null){
  if(!this.available)return false;
  this.fade.wake(performance.now());this.hud.closeKit();this.hud.layout.show('chat',true);this.hud.changed();this.sync();
  if(prefill!==null){this.input.value=prefill;this.draft=prefill;}
  this.input.focus();this.input.setSelectionRange(this.input.value.length,this.input.value.length);this.hud.wake();return true;
 }
 park(){const owned=this.root.contains(document.activeElement);this.input.blur();this.editing=false;this.root.classList.remove('composing');if(owned)document.getElementById('world').focus();}
 key(e){
  // Native text editing and clipboard shortcuts stay native inside this panel.
  if(e.isComposing||e.keyCode===229){if(e.key==='Enter')e.preventDefault();e.stopPropagation();return;}
  e.stopPropagation();
  if(e.target.matches('[role=tab]')&&['ArrowLeft','ArrowRight','Home','End'].includes(e.key)){
   e.preventDefault();const index=CHAT_TABS.findIndex(([id])=>id===this.tab),next=e.key==='Home'?0:e.key==='End'?CHAT_TABS.length-1:(index+(e.key==='ArrowLeft'?-1:1)+CHAT_TABS.length)%CHAT_TABS.length;
   this.setTab(CHAT_TABS[next][0]);this.tabs.children[next].focus();return;
  }
  if(e.key==='Escape'){e.preventDefault();this.park();return;}
  if(['PageUp','PageDown'].includes(e.key)){e.preventDefault();this.page(e.key==='PageUp'?-1:1);return;}
  if(e.target===this.input&&!e.metaKey&&!e.ctrlKey&&!e.altKey){
   if(e.key==='Enter'){e.preventDefault();this.submit();return;}
   if(['ArrowUp','ArrowDown'].includes(e.key)&&!this.inflight){
    e.preventDefault();if(this.historyIndex===this.sent.length)this.draft=this.input.value;
    this.historyIndex=Math.max(0,Math.min(this.sent.length,this.historyIndex+(e.key==='ArrowUp'?-1:1)));
    this.input.value=this.historyIndex===this.sent.length?this.draft:this.sent[this.historyIndex];
   }
  }
 }
 page(direction){this.log.scrollTop+=direction*Math.max(40,this.log.clientHeight*.8);this.follow=this.log.scrollHeight-this.log.scrollTop-this.log.clientHeight<24;this.updateUnread();}
 setTab(tab){this.scrolls[this.tab]={top:this.log.scrollTop,follow:this.follow};this.tab=tab;this.badges[tab]=0;this.follow=this.scrolls[tab]?.follow??true;this.renderLog();if(!this.follow)this.log.scrollTop=this.scrolls[tab]?.top||0;this.updateUnread();}
 bottom(){this.follow=true;this.unread=0;this.log.scrollTop=this.log.scrollHeight;this.updateUnread();}
 updateUnread(){this.jump.hidden=!this.unread&&!(!this.follow);this.jump.textContent=this.unread?`↓ ${this.unread} new · Latest`:'↓ Latest';for(const [id,label] of CHAT_TABS){const b=this.tabs.querySelector(`[data-chat-tab=${id}]`);b.textContent=label+(this.badges[id]?` (${this.badges[id]})`:'');b.setAttribute('aria-selected',String(this.tab===id));}}
 updateLabels(){const target=this.stream?.targets.find(t=>t.id===this.target);const name=target?.name||this.target;this.label.textContent=this.channel==='whisper'?`To ${name}:`:'Say to Cheese:';this.input.setAttribute('aria-label','Message to '+(this.channel==='whisper'?name:'Cheese'));this.root.dataset.channel=this.channel;this.send.disabled=Boolean(this.inflight)||Boolean(this.stream?.pending);}
 notice(text){this.local.push({id:'local:'+crypto.randomUUID(),text,channel:'world',name:'',time:'',order:this.high+.5});this.local=this.local.slice(-20);this.status.textContent=text;this.renderLog();}
 submit(){
  if(!this.available||this.inflight)return;
  const parsed=parseChat(this.input.value,{target:this.target,channel:this.channel,targets:this.stream?.targets||[],lastWhisper:this.lastWhisper});
  if(parsed.kind==='empty'){this.park();return;}
  if(parsed.kind==='error'){this.status.textContent=parsed.message;return;}
  if(parsed.kind==='help'){this.notice(HELP);this.input.value='';this.draft='';return;}
  if(parsed.kind==='clear'){this.clearThrough=this.high;this.local=[];this.renderLog();this.input.value='';this.draft='';this.bottom();return;}
  this.target=parsed.target;this.channel=parsed.channel;this.updateLabels();
  if(parsed.kind==='target'){this.input.value='';this.draft='';return;}
  if(!this.stream?.targets.some(t=>t.id===parsed.target)){this.status.textContent='That friend has stepped away. Use /s to talk to Cheese.';return;}
  if(this.stream.pending){this.status.textContent=`Let ${this.stream.pending} finish. Your message is still here.`;return;}
  const id=crypto.randomUUID();this.inflight={id,raw:this.input.value};this.input.readOnly=true;this.send.disabled=true;
  window.cheese.input({type:'chat',id,session:this.stream.session,text:parsed.text,target:parsed.target,channel:parsed.channel});
  this.status.textContent='Sending…';
 }
 renderLog(){
  const top=this.log.scrollTop,oldHeight=this.log.scrollHeight;
  const edge=this.log.getBoundingClientRect().top,anchor=this.follow?null:[...this.log.children].find(n=>n.getBoundingClientRect().bottom>edge),anchorTop=anchor?.getBoundingClientRect().top;
  const rows=[...this.rows.filter(r=>r.id>this.clearThrough),...this.local].sort((a,b)=>(a.order??a.id)-(b.order??b.id)).filter(r=>inTab(r,this.tab));
  // Reconcile by stable IDs so selection and scrollback do not jump on updates.
  const desired=new Set(rows.map(r=>String(r.id)));
  for(const node of [...this.log.children])if(!desired.has(node.dataset.entry))node.remove();
  let previous=null;
  for(const row of rows){
   let line=[...this.log.children].find(n=>n.dataset.entry===String(row.id));
   if(!line){
    line=el('p',undefined,'chat-line');line.dataset.entry=String(row.id);line.dataset.channel=row.channel;
    if(row.time)line.append(el('span',`[${row.time}] `,'chat-time'));
    line.append(el('span',`[${channelLabel(row,this.stream?.targets)}] `,'chat-channel'));
    if(row.name){const speaker=el(row.speaker==='player'?'span':'button',`[${row.name}]`,'chat-speaker');
     if(row.speaker!=='player'){speaker.title='Whisper to '+row.name;speaker.onclick=()=>{this.target=row.speaker;this.channel='whisper';this.updateLabels();this.open();};}
     line.append(speaker,document.createTextNode(row.channel==='whisper'?' whispers: ':row.channel==='neighbors'?' says nearby: ':': '));}
    line.append(el('span',row.text,'chat-text'));
   }
   if(previous?previous.nextSibling!==line:this.log.firstChild!==line)this.log.insertBefore(line,previous?previous.nextSibling:this.log.firstChild);
   previous=line;
  }
  if(!rows.length){const tip=el('p','The pond is listening. Press Enter to talk to Cheese.','chat-empty');tip.dataset.entry='empty';this.log.append(tip);}
  if(this.follow)this.log.scrollTop=this.log.scrollHeight;
  else if(anchor?.parentNode===this.log)this.log.scrollTop+=anchor.getBoundingClientRect().top-anchorTop;
  else{const trimmed=this.rows.length>=240&&this.log.scrollHeight<oldHeight;this.log.scrollTop=trimmed?Math.max(0,top-(oldHeight-this.log.scrollHeight)):top;}
 }
 bindResize(){
  this.resize.addEventListener('pointerdown',e=>{if(e.button)return;e.preventDefault();e.stopPropagation();this.hud.wake();const i=this.renderer.interface;this.resizeDrag={point:this.hud.point(e),rect:this.hud.layout.rect('chat',i.width,i.height),pointer:e.pointerId};this.resize.setPointerCapture(e.pointerId);});
  this.resize.addEventListener('pointermove',e=>{if(!this.resizeDrag)return;const p=this.hud.point(e),d=this.resizeDrag,i=this.renderer.interface;this.hud.layout.resize('chat',d.rect.w+p.x-d.point.x,d.rect.h+p.y-d.point.y,i.width,i.height);this.hud.redraw?.();this.hud.sync();this.sync();});
  const finish=()=>{if(!this.resizeDrag)return;this.resizeDrag=null;this.hud.changed();};for(const type of ['pointerup','pointercancel','lostpointercapture'])this.resize.addEventListener(type,finish);
  this.resize.addEventListener('keydown',e=>{if(!e.key.startsWith('Arrow'))return;e.preventDefault();e.stopPropagation();const i=this.renderer.interface,r=this.hud.layout.rect('chat',i.width,i.height),step=e.shiftKey?40:10;this.hud.layout.resize('chat',r.w+(e.key==='ArrowLeft'?-step:e.key==='ArrowRight'?step:0),r.h+(e.key==='ArrowUp'?-step:e.key==='ArrowDown'?step:0),i.width,i.height);this.hud.changed();this.sync();});
 }
}
