import {OPTIONS,ACTIONS,optionSprite,drawStudy} from './options.mjs';
const $=id=>document.getElementById(id),world=$('world'),detail=$('detail');
const images={};
for(const [key,url] of Object.entries(SCENES)){const im=new Image();im.src=url;await im.decode();images[key]=im;}
let selected=OPTIONS[0],light='day',action='walking',time=.2,playing=!matchMedia('(prefers-reduced-motion: reduce)').matches,facing=true,last=0;
const cards=[];
for(const [id,name] of ACTIONS)$('action').add(new Option(name,id));$('action').value=action;
function label(ctx,text,x,y,size=18,color='#eee3c3'){ctx.font=`600 ${size}px Menlo,monospace`;ctx.textBaseline='alphabetic';ctx.textAlign='left';ctx.fillStyle=color;ctx.fillText(text,x,y);}
function worldView(ctx,opt,t,mode,pose,dir,comparison=false){
  ctx.drawImage(images[mode],0,0,1200,620);
  if(comparison){ctx.drawImage(images[mode+'Current'],0,0,1200,620);label(ctx,'CURRENT',365,350,13);}
  drawStudy(ctx,opt,t,pose,740,320,optionSprite(opt).cell,dir,mode);
  label(ctx,opt.id+' / '+opt.name.toUpperCase(),645,350,13);
}
function detailView(ctx,opt,t,mode,pose,dir){
  ctx.fillStyle=mode==='day'?'#384c3d':mode==='dusk'?'#34423d':'#213b3f';ctx.fillRect(0,0,400,450);
  label(ctx,opt.id,22,40,25,'#e2bd72');label(ctx,'FEATHER / BILL / SILHOUETTE',22,68,11,'#c0cdb8');
  const m=optionSprite(opt),cw=Math.min(10,345/(m.width-7),260/(opt.art.length*1.5));
  drawStudy(ctx,opt,t,pose,205,360,cw,dir,mode);
  label(ctx,opt.material,22,415,11,'#c0cdb8');
}
function cardView(ctx,opt,t,mode,pose,dir){
  ctx.drawImage(images[mode],440,80,480,300,0,0,400,250);
  drawStudy(ctx,opt,t,pose,215,205,optionSprite(opt).cell*1.75,dir,mode);
  // Scale is deliberately magnified here; the large scene is the size reference.
  label(ctx,opt.id,15,29,22);label(ctx,'DETAIL VIEW',265,27,11,'#e4dcc4');
}
function update(){
  $('selected').textContent=selected.id+' / '+selected.name;
  $('notes').textContent=selected.note+' '+selected.motion;
  $('materials').textContent=selected.material+' · '+Math.round(100*(1-selected.height/108))+'% shorter than current Cheese';
  cards.forEach(c=>c.button.setAttribute('aria-pressed',c.option===selected));render();
}
for(const [i,opt] of OPTIONS.entries()){
  const button=document.createElement('button');button.className='option';button.setAttribute('aria-label',(i+1)+'. '+opt.name);button.setAttribute('aria-pressed','false');
  const canvas=document.createElement('canvas');canvas.width=400;canvas.height=250;
  const name=document.createElement('strong');name.textContent=opt.id+' · '+opt.name;
  const note=document.createElement('small');note.textContent=opt.note;
  button.append(canvas,name,note);button.onclick=()=>{selected=opt;update();};$('options').append(button);cards.push({button,canvas,option:opt});
}
function setPlaying(value){playing=value;$('play').textContent=value?'Pause':'Play';$('play').setAttribute('aria-pressed',value);}
$('play').onclick=()=>setPlaying(!playing);
$('light').onchange=()=>{light=$('light').value;render();};
$('action').onchange=()=>{action=$('action').value;time=0;render();};
$('facing').onclick=()=>{facing=!facing;$('facing').textContent=facing?'Face left':'Face right';$('facing').setAttribute('aria-pressed',!facing);render();};
$('compare').onchange=render;
$('scrub').oninput=()=>{setPlaying(false);time=Number($('scrub').value)/100;render();};
function render(){
  worldView(world.getContext('2d'),selected,time,light,action,facing,$('compare').checked);
  detailView(detail.getContext('2d'),selected,time,light,action,facing);
  cards.forEach(({canvas,option})=>cardView(canvas.getContext('2d'),option,time,light,action,facing));
  $('scrub').value=Math.round(time%5.3*100);
}
function tick(now){if(now-last>=1000/18){if(playing)time+=Math.min(.12,(now-last)/1000);last=now;render();}requestAnimationFrame(tick);}
setPlaying(playing);update();requestAnimationFrame(tick);

function canvas(w,h){const c=document.createElement('canvas');c.width=w;c.height=h;return c;}
function contact(mode='day',t=.2,pose='idle'){
  const c=canvas(2000,1000),ctx=c.getContext('2d');ctx.fillStyle='#13211d';ctx.fillRect(0,0,c.width,c.height);
  label(ctx,'CHEESE / TEN WORLD STUDIES',26,44,28);label(ctx,'A smaller silhouette. Finer feathers. Ten very different ducks. / '+mode.toUpperCase(),26,76,16,'#acbda8');
  OPTIONS.forEach((opt,i)=>{
    const x=i%5*400,y=110+Math.floor(i/5)*440;
    ctx.save();ctx.translate(x,y);cardView(ctx,opt,t,mode,pose,true);
    label(ctx,opt.id+' / '+opt.name,16,281,18);label(ctx,opt.material,16,309,11,'#adbea8');
    const words=opt.note.split(' ');let line='',lineY=339;ctx.font='600 13px Menlo,monospace';
    for(const word of words){const next=line?line+' '+word:word;if(ctx.measureText(next).width>365){label(ctx,line,16,lineY,13,'#c4cbb6');lineY+=20;line=word;}else line=next;}label(ctx,line,16,lineY,13,'#c4cbb6');ctx.restore();
  });return c;
}
window.exportStudies=()=>{
  const result={'ten-world-studies-day':contact().toDataURL(),'ten-world-studies-night':contact('night').toDataURL()};
  for(const opt of OPTIONS){const c=canvas(1600,620),ctx=c.getContext('2d');worldView(ctx,opt,.2,'day','idle',true,true);ctx.save();ctx.translate(1200,0);ctx.fillStyle='#263d30';ctx.fillRect(0,0,400,620);detailView(ctx,opt,.2,'day','idle',true);label(ctx,opt.id+' / '+opt.name,16,494,19);label(ctx,'PROPOSED GAME SIZE: '+opt.height+'px',16,531,13,'#acbda8');ctx.restore();result['option-'+opt.id]=c.toDataURL();}return result;
};
window.animationFrame=index=>{const c=contact('day',index/12,'walking'),small=canvas(1400,700);small.getContext('2d').drawImage(c,0,0,1400,700);return small.toDataURL();};
window.galleryReady=true;
