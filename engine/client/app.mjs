import { CELL_W, CELL_H } from './renderer.mjs';
import { DisplayRenderer } from './ultra-renderer.mjs';
const $ = id => document.getElementById(id), renderer = new DisplayRenderer($('world'));
let pending, last, zoom = 0, lastPaint = 0, lastAnnouncement = '';
renderer.mode = localStorage.getItem('cheese.graphics') === 'classic' ? 'classic' : 'ultra';
function graphicsLabel(){ const label = renderer.mode === 'ultra' ? 'Ultra' : 'Classic'; document.body.dataset.graphics=renderer.mode; $('graphics').textContent = `Graphics: ${label}`; $('graphics').setAttribute('aria-label', `Graphics mode: ${label}`); }
graphicsLabel();
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
}
function size(frame) {
  const view = $('viewport'), fit = Math.min((view.clientWidth - 24) / (frame.cols * CELL_W), (view.clientHeight - 16) / (frame.rows * CELL_H));
  renderer.resize(frame.cols, frame.rows, sizes[zoom] || fit);
}
window.cheese.frames(frame => { pending = frame; });
window.cheese.errors(message => { $('error').hidden = false; $('error').textContent = message; $('loading').hidden = true; });
function animate(now) {
  if (pending) {
    const frame = pending; pending = null; last = frame;
    size(frame); renderer.draw(frame, now); lastDraw = now; window.cheese.ack(); $('loading').hidden = true;
    $('place').textContent = frame.meta.location || 'Cheese the Duck';
    for (const b of $('actions').children) b.disabled = frame.meta.state !== 'playing';
    $('hint').textContent = frame.meta.talking ? 'Type to talk · Enter to send · Esc to return' : 'Arrow keys + Enter to choose · PgUp/PgDn chat · Esc menu';
    const plain = (frame.ui?.modal?.lines || frame.lines).map(line => line.map(run => run[0]).join('')).join('\n');
    if (plain !== lastAnnouncement && now - lastPaint > 1000) { $('announcement').textContent = plain; lastAnnouncement = plain; lastPaint = now; }
    window.engineStats = { frames: renderer.frames, glyphs: renderer.atlas.size, state: frame.meta.state, cols: frame.cols, rows: frame.rows, mode: renderer.mode, ultraFrames: renderer.scene.frames, renderMs: renderer.cost, peakMs: renderer.peak };
    window.interfaceTargets = renderer.mode === 'ultra' ? renderer.interface.hits : [];
    $('performance').textContent = renderer.mode === 'ultra' ? 'ULTRA ASCII' : `CLASSIC · ${frame.cols} × ${frame.rows}`;
  }
  if (!pending && (last?.scene || last?.ui?.state==='title') && renderer.mode === 'ultra' && now-lastDraw >= 1000/30) { renderer.draw(last, now); lastDraw=now; }
  requestAnimationFrame(animate);
}
new ResizeObserver(() => { if (last) { size(last); renderer.draw(last); } }).observe($('viewport'));
document.addEventListener('keydown', event => {
  if (event.metaKey || event.ctrlKey || event.altKey) return;
  if (event.key === 'F11') { event.preventDefault(); window.cheese.fullscreen(); return; }
  if (event.target.tagName === 'BUTTON' && ['Enter', ' '].includes(event.key)) return;
  if (event.key.length === 1 || ['Enter','Escape','Backspace','Tab','ArrowUp','ArrowDown','ArrowLeft','ArrowRight','PageUp','PageDown','Home','End','Delete'].includes(event.key)) {
    event.preventDefault(); window.cheese.input({ type: 'key', key: event.key });
  }
});
document.addEventListener('paste', event => { if (!last?.meta.talking) return; event.preventDefault(); window.cheese.input({ type: 'text', text: event.clipboardData.getData('text') }); });
$('graphics').onclick = () => { renderer.mode = renderer.mode === 'ultra' ? 'classic' : 'ultra'; localStorage.setItem('cheese.graphics',renderer.mode); graphicsLabel(); if(last)renderer.draw(last); $('world').focus(); };
$('zoom').onclick = () => { zoom = (zoom + 1) % sizes.length; $('zoom').textContent = `Text: ${zoom ? ['','large','larger','largest'][zoom] : 'fit'}`; if (last) { size(last); renderer.draw(last); } };
$('motion').onclick = () => { const on = $('world').classList.toggle('glow'); $('motion').textContent = `Soft glow: ${on ? 'on' : 'off'}`; $('motion').setAttribute('aria-pressed', on); };
$('capture').onclick = async () => { $('hint').textContent = `Photo saved: ${await window.cheese.capture()}`; };
$('fullscreen').onclick = () => window.cheese.fullscreen();
function point(event){const r=$('world').getBoundingClientRect();return [(event.clientX-r.left)/r.width*last.cols*10,(event.clientY-r.top)/r.height*last.rows*18];}
$('world').addEventListener('click',event=>{if(!last||renderer.mode!=='ultra')return;const command=renderer.interface.hit(...point(event));if(command)window.cheese.input(command);$('world').focus();});
$('world').addEventListener('mousemove',event=>{$('world').style.cursor=last&&renderer.mode==='ultra'&&renderer.interface.hit(...point(event))?'pointer':'default';});
$('world').addEventListener('wheel',event=>{if(renderer.mode==='ultra'&&renderer.interface.wheel(event.deltaY)){event.preventDefault();renderer.draw(last);}}, {passive:false});
requestAnimationFrame(animate); window.cheese.ready(); $('world').focus();
