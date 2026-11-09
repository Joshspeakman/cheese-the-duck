import {STAGES,VARIANTS,ACTIONS,scruffySprite} from './sprites.mjs';
import {drawCharacter} from '../../client/ultra-characters.mjs';
const BG='#0c1c21',PAGE='#08181c';
const $=id=>document.getElementById(id);
let selected='A',age='adult',action='walking',playing=!matchMedia('(prefers-reduced-motion: reduce)').matches,facing=true,time=0,speed=1,last=0;
const variantCards=[],ageCards=[],world=$('world'),wc=world.getContext('2d');
function text(ctx,line,x,y,size=22,color='#f0e5cc'){
  ctx.fillStyle=color;ctx.font=`600 ${size}px Menlo,monospace`;ctx.textBaseline='alphabetic';ctx.textAlign='left';ctx.fillText(line,x,y);
}
function wrap(ctx,line,x,y,width,size=18){
  ctx.fillStyle='#a9c0b6';ctx.font=`${size}px system-ui,sans-serif`;ctx.textAlign='left';ctx.textBaseline='alphabetic';let row='';
  for(const word of line.split(' ')){const next=row?row+' '+word:word;if(row&&ctx.measureText(next).width>width){ctx.fillText(row,x,y);y+=24;row=word;}else row=next;}
  ctx.fillText(row,x,y);
}
function figure(ctx,v,s,a,t,x,ground,cell=14,dir=true){
  const sprite=scruffySprite(v,s,a,t,dir);
  drawCharacter(ctx,{...sprite,scale:cell,x:x+sprite.offsetX*cell,y:ground+3.5*cell*1.5+sprite.offsetY*cell},1,1,BG);
}
function variantCard(ctx,v,s='adult',a='idle',t=0,dir=true){
  ctx.fillStyle=BG;ctx.fillRect(0,0,580,430);text(ctx,v.id,24,38,27,'#edb66b');text(ctx,v.name,66,38,24);
  text(ctx,STAGES.find(o=>o.id===s).name+' / '+ACTIONS.find(o=>o.id===a).name,24,69,15,'#a9c0b6');
  figure(ctx,v.id,s,a,t,290,326,17,dir);wrap(ctx,v.note,24,382,532);
}
function ageCard(ctx,s,v='A',a='walking',t=0,dir=true){
  ctx.fillStyle=BG;ctx.fillRect(0,0,480,370);text(ctx,s.name,24,35,24);text(ctx,s.age,24,63,16,'#edb66b');
  figure(ctx,v,s.id,a,t,240,283,14,dir);wrap(ctx,s.note,24,326,432,16);
}
function makeCard(container,option,width,height,onClick){
  const button=document.createElement('button'),canvas=document.createElement('canvas');button.className='card';canvas.width=width;canvas.height=height;
  button.setAttribute('aria-label',option.name);button.onclick=onClick;button.append(canvas);$(container).append(button);return {button,canvas,ctx:canvas.getContext('2d'),option};
}
for(const v of VARIANTS)variantCards.push(makeCard('variants',v,580,430,()=>{selected=v.id;update();render();}));
for(const s of STAGES)ageCards.push(makeCard('ages',s,480,370,()=>{age=s.id;$('age').value=age;time=0;update();render();}));
for(const s of STAGES)$('age').add(new Option(s.name+' · '+s.age,s.id));
for(const a of ACTIONS)$('action').add(new Option(a.name,a.id));
$('age').value=age;$('action').value=action;
$('age').onchange=()=>{age=$('age').value;time=0;update();render();};
$('action').onchange=()=>{action=$('action').value;time=0;update();render();};
function setPlaying(value){playing=value;$('play').textContent=playing?'Pause':'Play';$('play').setAttribute('aria-pressed',playing);}
$('play').onclick=()=>setPlaying(!playing);
$('speed').onchange=()=>{speed=Number($('speed').value);};
$('facing').onclick=()=>{facing=!facing;$('facing').textContent=facing?'Face left':'Face right';$('facing').setAttribute('aria-pressed',!facing);render();};
function ageRate(){return age==='elder'?.72:age==='hatchling'?1.18:1;}
$('timeline').oninput=()=>{setPlaying(false);time=Number($('timeline').value)/1000*ACTIONS.find(a=>a.id===action).duration/ageRate();render();};
$('step').onclick=()=>{setPlaying(false);const a=ACTIONS.find(a=>a.id===action);time+=a.duration/a.frames/ageRate();render();};
function update(){
  const v=VARIANTS.find(v=>v.id===selected),s=STAGES.find(s=>s.id===age),a=ACTIONS.find(a=>a.id===action);
  $('selection').textContent=`${v.id} / ${v.name} · ${s.name}`;
  $('detail').textContent=age==='egg'?'The egg rocks, cracks, and briefly reveals its first scruffy feathers.':a.detail;
  $('age-heading').textContent=`${v.id} / ${v.name} — all nine ages`;
  $('age-note').textContent='Real growth stages from the game. Hatchlings move quicker; elders take slower steps. Click any age to inspect it above.';
  for(const c of variantCards)c.button.setAttribute('aria-pressed',c.option.id===selected);
  for(const c of ageCards)c.button.setAttribute('aria-pressed',c.option.id===age);
}
const background=new Image();background.src=SCENE;await background.decode();
function render(){
  wc.drawImage(background,0,0,world.width,world.height);figure(wc,selected,age,action,time,600,390,15,facing);
  for(const c of variantCards)variantCard(c.ctx,c.option,age,action,time,facing);
  for(const c of ageCards)ageCard(c.ctx,c.option,selected,action,time,facing);
  const model=scruffySprite(selected,age,action,time,facing);$('counter').textContent=`Pose ${model.phase+1} / ${model.frames}`;
  $('timeline').value=Math.floor(model.cycle*999);
}
function tick(now){if(now-last>1000/24){if(playing)time+=Math.min((now-last)/1000,.1)*speed;last=now;render();}requestAnimationFrame(tick);}
setPlaying(playing);update();render();requestAnimationFrame(tick);

function canvas(width,height){const c=document.createElement('canvas');c.width=width;c.height=height;return c;}
function agesSheet(v='A',a='idle',t=0,small=false){
  const c=canvas(1500,1260),ctx=c.getContext('2d');ctx.fillStyle=PAGE;ctx.fillRect(0,0,c.width,c.height);
  const variant=VARIANTS.find(o=>o.id===v);
  text(ctx,`${v} / ${variant.name.toUpperCase()} — EVERY AGE`,30,44,30);
  text(ctx,`${ACTIONS.find(o=>o.id===a).name} · Nine stages, one scruffy little bastard.`,30,78,18,'#a9c0b6');
  for(const [i,s] of STAGES.entries()){ctx.save();ctx.translate(15+i%3*500,108+Math.floor(i/3)*380);ageCard(ctx,s,v,a,t);ctx.restore();}
  if(small){const tiny=canvas(1200,1008);tiny.getContext('2d').drawImage(c,0,0,1200,1008);return tiny;}
  return c;
}
function variantsSheet(a='idle',t=0,small=false){
  const c=canvas(1800,1000),ctx=c.getContext('2d');ctx.fillStyle=PAGE;ctx.fillRect(0,0,c.width,c.height);
  text(ctx,'SCRUFFY CHEESE / SIX RELATED DESIGNS',30,46,32);text(ctx,`Adult / ${ACTIONS.find(o=>o.id===a).name} · A stays closest to option 08.`,30,80,19,'#a9c0b6');
  for(const [i,v] of VARIANTS.entries()){ctx.save();ctx.translate(10+i%3*600,110+Math.floor(i/3)*440);variantCard(ctx,v,'adult',a,t);ctx.restore();}
  if(small){const tiny=canvas(1440,800);tiny.getContext('2d').drawImage(c,0,0,1440,800);return tiny;}
  return c;
}
window.exportSheets=()=>{
  const images={'six-scruffy-designs':variantsSheet().toDataURL()};
  for(const v of VARIANTS)images[`all-ages-${v.id}`]=agesSheet(v.id).toDataURL();
  for(const a of ACTIONS){
    const c=canvas(1600,740),ctx=c.getContext('2d');ctx.fillStyle=PAGE;ctx.fillRect(0,0,c.width,c.height);
    text(ctx,`A / ORIGINAL MENACE — ${a.name.toUpperCase()}`,25,42,27);
    text(ctx,a.detail,25,76,15,'#a9c0b6');
    for(let i=0;i<a.frames;i++){ctx.save();ctx.translate(i%4*400,110+Math.floor(i/4)*310);text(ctx,String(i+1).padStart(2,'0'),22,28,19,'#edb66b');figure(ctx,'A','adult',a.id,(i+.2)*a.duration/a.frames,200,266,13);ctx.restore();}
    images[`poses-${a.id}`]=c.toDataURL();
  }
  return images;
};
window.animationFrame=(kind,index)=>{
  const t=index/12;
  if(kind==='ages')return agesSheet('A','walking',t,true).toDataURL();
  const actions=ACTIONS.map(a=>a.id);
  const a=actions[Math.floor(index/24)%actions.length];
  return variantsSheet(a,(index%24)/12,true).toDataURL();
};
window.galleryReady=true;
