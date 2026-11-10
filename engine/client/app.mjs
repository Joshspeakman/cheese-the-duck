import {PondJournal} from './pond-journal.mjs';
import {HudController} from './hud-controller.mjs';
import { sceneLight } from './scene-lighting.mjs';
import { ItemGallery } from './item-gallery.mjs';
import { CELL_W, CELL_H } from './renderer.mjs';
import { DisplayRenderer } from './ultra-renderer.mjs';
const $ = id => document.getElementById(id), renderer = new DisplayRenderer($('world'));
let pending, last, zoom = 0, lastPaint = 0, lastAnnouncement = '';
const gallery=new ItemGallery(()=>last?.ui?.motion!==false);
$('item-art').onclick=()=>{hud.closeKit();gallery.show();};
const pond=new PondJournal();$('pond').onclick=()=>{hud.closeKit();pond.show();};
renderer.mode = localStorage.getItem('cheese.graphics') === 'classic' ? 'classic' : 'ultra';
function graphicsLabel(){ const label = renderer.mode === 'ultra' ? 'Ultra' : 'Classic'; document.body.dataset.graphics=renderer.mode; $('graphics').textContent = `Graphics: ${label}`; $('graphics').setAttribute('aria-label', `Graphics mode: ${label}`); }
graphicsLabel();
const effectLevels=['vivid','subtle','off'];
renderer.scene.effects.level=effectLevels.includes(localStorage.getItem('cheese.effects'))?localStorage.getItem('cheese.effects'):'vivid';
function effectsLabel(){const value=renderer.scene.effects.level;$('motion').textContent=`Effects: ${value}`;$('motion').setAttribute('aria-label',`Scene effects: ${value}`);}
effectsLabel();
const hud=new HudController(renderer,{
 redraw:()=>{if(last){renderer.draw(last);window.interfaceTargets=renderer.interface.hits;}},
 onEscape:()=>window.cheese.input({type:'key',key:'Escape'}),blocked:()=>gallery.open||pond.open,
});
window.pondHUD=hud;
// Retire the previous forced-time preference; the environment follows game time.
localStorage.removeItem('cheese.lighting');
function lightingLabel(frame){const hour=frame.scene?.hour??frame.ui?.hour??12;$('lighting').textContent=sceneLight({hour}).phase;$('lighting').title='Lighting follows the game clock';}
let lastDraw = 0;
const sizes = [0, .9, 1.15, 1.4];
const actionIDs = { f:'feed', p:'play', l:'clean', d:'pet', z:'sleep', t:'talk', e:'explore', b:'shop', c:'craft', r:'build', i:'inventory', h:'help' };
const actionKeys = [['f','Feed'],['p','Play'],['l','Clean'],['d','Pet'],['z','Sleep'],['t','Talk'],['e','Explore'],['b','Shop'],['c','Craft'],['r','Build'],['i','Items'],['h','Help'],['Escape','Menu']];
for (const [key, label] of actionKeys) {
  const button = document.createElement('button'), kbd = document.createElement('kbd'), icon=document.createElement('span');
  const icons=['(=)','*o*','~*~','<3','zZ','...','/\\','$','/T','|^|','[+]','(?)',':::'];
  icon.className='action-icon';icon.setAttribute('aria-hidden','true');icon.textContent=icons[$('actions').children.length];
  kbd.textContent = key === 'Escape' ? 'Esc' : key.toUpperCase(); button.append(icon,kbd, label);
  button.addEventListener('click', () => { window.cheese.input(actionIDs[key] ? { type: 'action', action: actionIDs[key] } : { type: 'key', key }); $('world').focus(); }); $('actions').append(button);
  if(key==='Escape')button.onclick=()=>{ if(last?.scene&&!last.ui?.modal&&(!renderer.interface.panelsOpen||last.ui.menu.depth===0))togglePanels(); };
}
function size(frame) {
  const full=renderer.mode==='ultra'&&Boolean(frame.scene&&frame.ui);
  document.body.dataset.layout=full?'world':'framed';
  const view = $('viewport'), fit = Math.min((view.clientWidth - 24) / (frame.cols * CELL_W), (view.clientHeight - 16) / (frame.rows * CELL_H));
  const uiScale=Math.min(Math.min(view.clientWidth/1440,view.clientHeight/1000,1)*[1,1.1,1.2,1.3][zoom],view.clientWidth/1100,view.clientHeight/850);
  renderer.resize(frame.cols, frame.rows, sizes[zoom] || fit,full?{width:view.clientWidth,height:view.clientHeight,uiScale}:null);
}
function togglePanels(){renderer.interface.panelsOpen=!renderer.interface.panelsOpen;syncPanels();hud.changed();}
function syncPanels(){$('panels').textContent=renderer.interface.panelsOpen?'Hide panels':'Care & menu';$('panels').setAttribute('aria-pressed',renderer.interface.panelsOpen);}
window.cheese.frames(frame => { pending = frame; });
window.cheese.errors(message => { hud.wake();$('error').hidden = false; $('error').textContent = message; $('loading').hidden = true; });
function animate(now) {
  if (pending) {
    const frame = pending; pending = null; last = frame; pond.update(frame);
    size(frame);hud.update(frame,now);renderer.draw(frame, now);hud.sync();lightingLabel(frame); lastDraw = now; window.cheese.ack(); $('loading').hidden = true;
    $('place').textContent = frame.meta.location || 'Cheese the Duck';
    for (const b of $('actions').children) b.disabled = frame.meta.state !== 'playing';
    $('panels').disabled=Boolean(frame.ui?.modal);syncPanels();
    $('hint').textContent = frame.meta.talking ? 'Type to talk · Enter to send · Esc to return' : 'Arrow keys + Enter to choose · PgUp/PgDn chat · Esc menu';
    const plain = (frame.ui?.modal?.lines || frame.lines).map(line => line.map(run => run[0]).join('')).join('\n');
    if (plain !== lastAnnouncement && now - lastPaint > 1000) { $('announcement').textContent = plain; lastAnnouncement = plain; lastPaint = now; }
    window.engineStats = { frames: renderer.frames, glyphs: renderer.atlas.size, state: frame.meta.state, cols: frame.cols, rows: frame.rows, viewWidth:renderer.interface.width, viewHeight:renderer.interface.height, mode: renderer.mode, worldHour:renderer.scene.light?.hour, portraitHour:renderer.interface.emotionHour, ultraFrames: renderer.scene.frames, renderMs: renderer.cost, peakMs: renderer.peak };
    window.interfaceTargets = renderer.mode === 'ultra' ? renderer.interface.hits : [];
    $('performance').textContent = renderer.mode === 'ultra' ? 'ULTRA ASCII' : `CLASSIC · ${frame.cols} × ${frame.rows}`;
  }
  hud.update(last,now);
  if (!pending && (last?.scene || last?.ui?.state==='title') && renderer.mode === 'ultra' && now-lastDraw >= 1000/30) { renderer.draw(last, now);hud.sync();window.interfaceTargets=renderer.interface.hits; lastDraw=now; }
  requestAnimationFrame(animate);
}
new ResizeObserver(() => { if (last) { size(last); renderer.draw(last); } }).observe($('viewport'));
document.addEventListener('keydown', event => {
  if(event.defaultPrevented||hud.open||event.target.closest('[data-hud-ui],dialog'))return;
  if(gallery.open||pond.open)return;
  if (event.metaKey || event.ctrlKey || event.altKey) return;
  if(event.key.toLowerCase()==='j'&&!last?.meta.talking&&!last?.ui?.modal){event.preventDefault();pond.show();return;}
  if (event.key === 'F11') { event.preventDefault(); window.cheese.fullscreen(); return; }
  if (event.target.tagName === 'BUTTON' && ['Enter', ' '].includes(event.key)) return;
  if (event.key.length === 1 || ['Enter','Escape','Backspace','Tab','ArrowUp','ArrowDown','ArrowLeft','ArrowRight','PageUp','PageDown','Home','End','Delete'].includes(event.key)) {
    if(renderer.mode==='ultra'&&last?.scene&&!last.ui?.modal){
      if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Enter'].includes(event.key)){renderer.interface.panelsOpen=true;syncPanels();hud.changed();}
      else if(event.key==='Escape'&&(!renderer.interface.panelsOpen||last.ui.menu.depth===0))togglePanels();
    }
    event.preventDefault(); window.cheese.input({ type: 'key', key: event.key });
  }
});
document.addEventListener('paste', event => { if (gallery.open||pond.open||!last?.meta.talking) return; event.preventDefault(); window.cheese.input({ type: 'text', text: event.clipboardData.getData('text') }); });
$('graphics').onclick = () => { renderer.mode = renderer.mode === 'ultra' ? 'classic' : 'ultra'; localStorage.setItem('cheese.graphics',renderer.mode); graphicsLabel(); if(last){size(last);hud.update(last);renderer.draw(last);hud.sync();} $('world').focus(); };
$('zoom').onclick = () => { zoom = (zoom + 1) % sizes.length; $('zoom').textContent = `Text: ${zoom ? ['','large','larger','largest'][zoom] : 'fit'}`; if (last) { size(last); renderer.draw(last); } };
$('motion').onclick=()=>{renderer.scene.effects.level=effectLevels[(effectLevels.indexOf(renderer.scene.effects.level)+1)%effectLevels.length];localStorage.setItem('cheese.effects',renderer.scene.effects.level);effectsLabel();if(last)renderer.draw(last);$('world').focus();};
$('capture').onclick = async () => { $('hint').textContent = `Photo saved: ${await window.cheese.capture()}`; };
$('fullscreen').onclick = () => window.cheese.fullscreen();
$('panels').onclick=()=>{togglePanels();$('world').focus();};
function point(event){const r=$('world').getBoundingClientRect();return [(event.clientX-r.left)/r.width*renderer.interface.width,(event.clientY-r.top)/r.height*renderer.interface.height];}
$('world').addEventListener('click',event=>{if(!last||renderer.mode!=='ultra')return;const command=renderer.interface.hit(...point(event));if(command?.type==='panels')togglePanels();else if(command)window.cheese.input(command);else if(!hud.blocks(event)&&!last.ui?.modal&&!pond.open){const r=$('world').getBoundingClientRect(),x=(event.clientX-r.left)/r.width,y=(event.clientY-r.top)/r.height;const hit=renderer.scene.hit(x,y);if(hit)pond.show(hit.kind==='friend'?'friends':'belongings',hit.id);}if(!pond.open)$('world').focus();});
$('world').addEventListener('mousemove',event=>{$('world').style.cursor=last&&renderer.mode==='ultra'&&renderer.interface.hit(...point(event))?'pointer':'default';});
$('world').addEventListener('wheel',event=>{if(renderer.mode==='ultra'&&renderer.interface.wheel(event.deltaY)){event.preventDefault();renderer.draw(last);}}, {passive:false});
requestAnimationFrame(animate); window.cheese.ready(); $('world').focus();
