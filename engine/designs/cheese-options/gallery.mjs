import { OPTIONS, ORIGINAL, optionSprite } from './options.mjs';
import { drawCharacter } from '../../client/ultra-characters.mjs';

const BG = '#0c1c21';
let selected = OPTIONS[0], pose = 'idle', playing = true, elapsed = 0, last = 0;
const world = document.getElementById('world'), wc = world.getContext('2d');
const cards = [];
function label(ctx, text, x, y, size = 22, color = '#eee5cd') {
  ctx.fillStyle = color; ctx.font = `600 ${size}px Menlo, monospace`;
  ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic'; ctx.fillText(text, x, y);
}
function wrap(ctx, text, x, y, maxWidth) {
  ctx.fillStyle = '#a9c1b8'; ctx.font = '19px system-ui, sans-serif';
  const words = text.split(' '); let line = '';
  for (const word of words) {
    const next = line ? line + ' ' + word : word;
    if (ctx.measureText(next).width > maxWidth && line) {ctx.fillText(line, x, y); y += 25; line = word;}
    else line = next;
  }
  ctx.fillText(line, x, y);
}
function drawCard(ctx, option, time = 0, expression = 'idle', width = 860, height = 400) {
  ctx.fillStyle = BG; ctx.fillRect(0, 0, width, height);
  label(ctx, String(option.id).padStart(2, '0'), 28, 42, 25, '#edb760');
  label(ctx, option.name, 85, 42, 25);
  const sprite = optionSprite(option, time, expression), cell = 17;
  const bob = expression === 'walking' ? Math.sin(time * 12) * 3 : Math.sin(time * 2) * 1;
  drawCharacter(ctx, {...sprite, x: width / 2, y: 328 + bob, scale: cell}, 1, 1, BG);
  wrap(ctx, option.description, 28, 368, width - 56);
}
function select(option) {
  selected = option;
  document.getElementById('selection').textContent = `${String(option.id).padStart(2, '0')} / ${option.name}`;
  document.getElementById('description').textContent = option.description;
  for (const card of cards) card.button.setAttribute('aria-pressed', card.option.id === option.id);
}
for (const option of OPTIONS) {
  const button = document.createElement('button'), canvas = document.createElement('canvas');
  button.className = 'card'; button.setAttribute('aria-label', `Option ${option.id}: ${option.name}`);
  button.onclick = () => select(option); canvas.width = 860; canvas.height = 400;
  button.append(canvas); document.getElementById('options').append(button);
  cards.push({option, button, canvas, ctx:canvas.getContext('2d')});
}
document.getElementById('play').onclick = event => {
  playing = !playing; event.currentTarget.textContent = playing ? 'Pause animation' : 'Play animation';
  event.currentTarget.setAttribute('aria-pressed', playing);
};
for (const button of document.querySelectorAll('.pose')) button.onclick = () => {
  pose = button.dataset.pose;
  for (const other of document.querySelectorAll('.pose')) other.setAttribute('aria-pressed', other === button);
};
const background = new Image();
background.src = SCENE;
await background.decode();
function drawWorld(time) {
  wc.drawImage(background, 0, 0, world.width, world.height);
  const sprite = optionSprite(selected, time, pose);
  const bob = pose === 'walking' ? Math.sin(time * 12) * 3 : Math.sin(time * 2) * .7;
  const cell = 12.3;
  drawCharacter(wc, {...sprite, x: 600, y: 371 + bob, scale: cell}, 1, 1, BG);
}
function render(time) {
  for (const card of cards) drawCard(card.ctx, card.option, time, pose);
  drawWorld(time);
}
function animate(now) {
  if (now - last > 65) {
    if (playing) elapsed += Math.min((now - last) / 1000, .1);
    render(elapsed); last = now;
  }
  requestAnimationFrame(animate);
}
select(selected); render(0); requestAnimationFrame(animate);

// Export an overview at a fixed frame, plus a world view for every candidate.
window.exportOptions = () => {
  const sheet = document.createElement('canvas'); sheet.width = 1800; sheet.height = 2250;
  const ctx = sheet.getContext('2d'); ctx.fillStyle = '#08181c'; ctx.fillRect(0, 0, sheet.width, sheet.height);
  label(ctx, 'CHEESE / TEN CHARACTER OPTIONS', 40, 55, 34);
  label(ctx, 'Different silhouettes. The same little bastard.', 40, 95, 21, '#a9c1b8');
  label(ctx, 'ORIGINAL', 1500, 45, 16, '#a9c1b8');
  const original = {art:ORIGINAL, width:6, anchorX:3, scale:15, x:1640, y:125, body:'#f0d28e', face:'#ffe9b3', accent:'#f3ad56'};
  drawCharacter(ctx, original, 1, 1, '#08181c');
  const images = {};
  for (const [i, option] of OPTIONS.entries()) {
    ctx.save(); ctx.translate(30 + (i % 2) * 890, 150 + Math.floor(i / 2) * 415);
    drawCard(ctx, option); ctx.restore();
    const card = cards[i]; drawCard(card.ctx, option);
    images[`option-${String(option.id).padStart(2, '0')}`] = card.canvas.toDataURL('image/png');
    select(option); drawWorld(0);
    images[`world-${String(option.id).padStart(2, '0')}`] = world.toDataURL('image/png');
  }
  label(ctx, 'Pick a number, or combine your favorite features.', 40, 2233, 19, '#a9c1b8');
  images['ten-cheese-options'] = sheet.toDataURL('image/png');
  select(OPTIONS[0]); render(0);
  return images;
};
window.galleryReady = true;
