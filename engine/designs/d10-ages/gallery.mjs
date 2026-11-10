import {AGES,ACTIONS,ageSprite,drawAge} from './ages.mjs';
const $=id=>document.getElementById(id),world=$('world'),detail=$('detail'),adult=AGES.find(a=>a.id==='adult');
const images={};
for(const [key,url] of Object.entries(SCENES)){const im=new Image();im.src=url;await im.decode();images[key]=im;}
let selected=adult,light='day',action='walking',time=.2,playing=!matchMedia('(prefers-reduced-motion: reduce)').matches,facing=true,last=0;
const cards=[];
for(const [id,name] of ACTIONS)$('action').add(new Option(name,id));$('action').value=action;
for(const a of AGES)$('age').add(new Option(a.name,a.id));$('age').value=selected.id;
function label(ctx,text,x,y,size=18,color='#eee3c3'){ctx.font=`600 ${size}px Menlo,monospace`;ctx.textBaseline='alphabetic';ctx.textAlign='left';ctx.fillStyle=color;ctx.fillText(text,x,y);}
function worldView(ctx,age,t,mode,pose,dir,comparison=false){
  ctx.drawImage(images[mode],0,0,1200,620);
  if(comparison){drawAge(ctx,adult,t,pose,420,320,ageSprite(adult).cell,dir,mode);label(ctx,'ADULT D10',365,350,13);}
  drawAge(ctx,age,t,pose,740,320,ageSprite(age).cell,dir,mode);label(ctx,age.name.toUpperCase(),680,350,13);
}
function detailView(ctx,age,t,mode,pose,dir){
  ctx.fillStyle=mode==='day'?'#384c3d':mode==='dusk'?'#34423d':'#213b3f';ctx.fillRect(0,0,400,450);
  label(ctx,age.name,22,40,25,'#e2bd72');label(ctx,age.age,22,68,14,'#c0cdb8');
  const m=ageSprite(age),cw=age.id==='egg'?12:Math.min(10,345/(m.width-7),260/(age.art.length*1.5));
  drawAge(ctx,age,t,pose,205,360,cw,dir,mode);label(ctx,'CHEESE / D10 / ENLARGED',22,415,12,'#c0cdb8');
}
function cardView(ctx,age,t,mode,pose,dir){
  ctx.drawImage(images[mode],420,80,480,300,0,0,600,300);
  drawAge(ctx,age,t,pose,320,264,ageSprite(age).cell*2,dir,mode);
  label(ctx,age.name.toUpperCase(),20,34,23);label(ctx,'2x / SHARED SCALE',387,32,12,'#e4dcc4');
}
function update(){
  $('selected').textContent='Cheese / '+selected.name;$('notes').textContent=selected.note;
  $('materials').textContent=selected.age+' · '+(selected.id==='egg'?'Shell wobble and hatching peek':selected.id==='adult'?'Your selected D10, unchanged':'D10 growth study');
  $('age').value=selected.id;cards.forEach(c=>c.button.setAttribute('aria-pressed',c.age===selected));render();
}
for(const age of AGES){
  const button=document.createElement('button');button.className='option';button.setAttribute('aria-label',age.name+' / '+age.age);
  const canvas=document.createElement('canvas');canvas.width=600;canvas.height=300;
  const name=document.createElement('strong');name.textContent=age.name+' · '+age.age;
  const note=document.createElement('small');note.textContent=age.note;
  button.append(canvas,name,note);button.onclick=()=>{selected=age;update();};$('options').append(button);cards.push({button,canvas,age});
}
function setPlaying(value){playing=value;$('play').textContent=value?'Pause':'Play';$('play').setAttribute('aria-pressed',value);}
$('age').onchange=()=>{selected=AGES.find(a=>a.id===$('age').value);update();};
$('play').onclick=()=>setPlaying(!playing);
$('light').onchange=()=>{light=$('light').value;render();};
$('action').onchange=()=>{action=$('action').value;time=0;render();};
$('facing').onclick=()=>{facing=!facing;$('facing').textContent=facing?'Face left':'Face right';$('facing').setAttribute('aria-pressed',!facing);render();};
$('compare').onchange=render;$('scrub').oninput=()=>{setPlaying(false);time=Number($('scrub').value)/100;render();};
function render(){worldView(world.getContext('2d'),selected,time,light,action,facing,$('compare').checked);detailView(detail.getContext('2d'),selected,time,light,action,facing);cards.forEach(c=>cardView(c.canvas.getContext('2d'),c.age,time,light,action,facing));$('scrub').value=Math.round(time%5.3*100);}
function tick(now){if(now-last>=1000/18){if(playing)time+=Math.min(.12,(now-last)/1000);last=now;render();}requestAnimationFrame(tick);}
setPlaying(playing);update();requestAnimationFrame(tick);
function canvas(w,h){const c=document.createElement('canvas');c.width=w;c.height=h;return c;}
function contact(mode='day',t=.2,pose='idle'){
  const c=canvas(1800,1440),ctx=c.getContext('2d');ctx.fillStyle='#13211d';ctx.fillRect(0,0,c.width,c.height);
  label(ctx,'CHEESE / D10 / ALL NINE AGES',26,44,30);label(ctx,'From egg to Legendary. Same magnification throughout. / '+mode.toUpperCase(),26,79,17,'#acbda8');
  AGES.forEach((age,i)=>{
    ctx.save();ctx.translate(i%3*600,110+Math.floor(i/3)*440);cardView(ctx,age,t,mode,pose,true);
    label(ctx,age.name+' / '+age.age,20,333,19);let line='',lineY=365;ctx.font='600 14px Menlo,monospace';
    for(const word of age.note.split(' ')){const next=line?line+' '+word:word;if(ctx.measureText(next).width>555){label(ctx,line,20,lineY,14,'#b8c5ae');lineY+=22;line=word;}else line=next;}label(ctx,line,20,lineY,14,'#b8c5ae');ctx.restore();
  });return c;
}
function lineup(t=0,pose='idle'){
  const c=canvas(2160,460),ctx=c.getContext('2d');ctx.fillStyle='#172a22';ctx.fillRect(0,0,c.width,c.height);
  label(ctx,'CHEESE / D10 / GROWING UP',25,40,27);label(ctx,'One shared scale. One ground line. Every age.',25,73,16,'#b4c3ab');
  AGES.forEach((age,i)=>{drawAge(ctx,age,t,pose,i*240+120,330,ageSprite(age).cell*1.8,true,'day');label(ctx,age.name,i*240+24,373,18);label(ctx,age.age,i*240+24,405,13,'#b4c3ab');});return c;
}
window.exportStudies=()=>{
  const result={'d10-all-ages-day':contact().toDataURL(),'d10-all-ages-night':contact('night').toDataURL(),'d10-growth-lineup':lineup().toDataURL()};
  for(const age of AGES){const c=canvas(1600,620),ctx=c.getContext('2d');worldView(ctx,age,.2,'day','idle',true,true);ctx.save();ctx.translate(1200,0);ctx.fillStyle='#263d30';ctx.fillRect(0,0,400,620);detailView(ctx,age,.2,'day','idle',true);label(ctx,age.name,18,500,23);label(ctx,age.age,18,535,16,'#b4c3ab');ctx.restore();result['age-'+age.id]=c.toDataURL();}return result;
};
window.animationFrame=index=>{const c=contact('day',index/12,'walking'),small=canvas(1200,960);small.getContext('2d').drawImage(c,0,0,1200,960);return small.toDataURL();};
window.checkAdultParity=()=>{
  const a=canvas(450,400),b=canvas(450,400);
  drawAge(a.getContext('2d'),adult,.4,'walking',220,320,8,true,'day');drawCute(b.getContext('2d'),CUTE_OPTIONS.find(o=>o.id==='D10'),.4,'walking',220,320,8,true,'day');
  if(a.toDataURL()!==b.toDataURL())throw Error('Selected adult D10 changed');return true;
};
window.galleryReady=true;
