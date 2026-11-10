import { CATALOG } from '../pond-cast/catalog.mjs';
import { characterSprite, drawCharacter } from '../../client/ultra-characters.mjs';
import { DUCK_AGES } from '../../client/duck-rig.mjs';
import { catalog, itemSprite, itemFamily, itemProfile, itemWorldScale, ItemPainter } from '../../client/ultra-items.mjs';
import { wearableSpec, wearableCatalog } from '../../client/wearables.mjs';
import { eventModel, EVENT_ASSETS } from '../../client/event-art.mjs';
import { WILDLIFE } from '../../client/wildlife.mjs';
import { sceneLight } from '../../client/scene-lighting.mjs';
import { guestProfile } from '../../client/visitor-rig.mjs';
import { DATA } from './data.mjs';

const $=id=>document.getElementById(id), title=s=>String(s||'').replaceAll('_',' ').replace(/\b\w/g,c=>c.toUpperCase());
const painter=new ItemPainter(), images={}, boundsCache=new Map(), PAGE_SIZE=24;
let tab='visitors',page=0,filtered=[],cards=[],selected=null,playing=true,time=0,last=0,facing=true;
let notes={};try{notes=JSON.parse(localStorage.getItem('cheese-art-atlas-notes')||'{}');}catch{}
const records=[
  ...DATA.rare.map(r=>({...r,kind:'visitors',id:r.id,original:r.ascii_art,subtype:'Rare visitors',
    personality:r.rigPersonality,description:r.description,representation:r.rigPersonality?'Detailed duck rig':'Event / wildlife sprite',
    movement:'Fixed beside Cheese (+17, +2 in scene coordinates). No independent wandering; remains idle in the live scene.'})),
  ...CATALOG.friends.map(r=>({...r,kind:'visitors',subtype:'Regular duck friends',representation:'Detailed duck rig',
    description:`${title(r.personality)} duck friend. Personality gear and name-seeded feather crest.`,
    movement:'Independent friend animator: arrivals, departures, following Cheese and random wandering.'})),
  ...CATALOG.events.map(r=>({...r,kind:'events',subtype:r.source,animated:DATA.eventFlags[r.id]?.animated??true,
    definition:DATA.eventFlags[r.id]?.definition,description:r.message,
    representation:DATA.eventFlags[r.id]?.animated===false?'Text only':r.source==='animation'?'Animation recipe':'Event sprite'})),
  ...catalog.map(r=>({...r,kind:'items',subtype:r.category,family:itemFamily(r.id),wearable:wearableSpec(r.id),
    representation:'Detailed item sprite'})),
  ...wearableCatalog.map(r=>({...r,kind:'wearables',subtype:wearableSpec(r.id).slot,
    wearable:wearableSpec(r.id),family:wearableSpec(r.id).family,representation:'Fitted wearable'})),
  ...[...new Set([...Object.keys(EVENT_ASSETS),...Object.keys(WILDLIFE)])].map(key=>({
    id:key,asset:key,name:title(key),kind:'sprites',subtype:EVENT_ASSETS[key]?.category||'creatures',
    representation:WILDLIFE[key]?'Wildlife silhouette':'Event art',original:EVENT_ASSETS[key]?.frames,
    description:'Individual sprite used by event scenes. Some events share this artwork.'})),
  ...Object.entries(DATA.stories).map(([id,r])=>({...r,id,name:r.title,kind:'stories',subtype:'Living pond stories',
    description:r.scenes[0].text,representation:'Story actor',movement:'Story actor is placed beside Cheese (+14, +0); no independent path.'})),
];
for(const r of records){
  if(r.kind==='visitors'){
    r.identity=guestProfile(r);r.description=r.identity.bio;r.representation='Named character rig';
    r.movement=`Independent movement with ${r.identity.pace<3?'unhurried':r.identity.pace>4.5?'energetic':'steady'} steps and occupation pauses. ${r.identity.habit}`;
  }
  r.uid=`${r.kind}:${r.id}`;r.search=JSON.stringify(r).toLowerCase();
}
const byUID=new Map(records.map(r=>[r.uid,r])), counts=Object.fromEntries(['visitors','events','items','wearables','sprites','stories'].map(k=>[k,records.filter(r=>r.kind===k).length]));
const familyCounts={};for(const r of records.filter(r=>r.kind==='items'))familyCounts[r.family]=(familyCounts[r.family]||0)+1;
const eventCounts={};for(const r of records.filter(r=>r.kind==='events'&&r.animated)){const key=eventModel({id:r.animation,family:r.animator,art:r.original},0).asset||'fallback';eventCounts[key]=(eventCounts[key]||0)+1;}

function model(r,t,detail=false){
  const state=detail?$('pose').value:'idle',age=detail?$('age').value:'adult',right=detail?facing:true;
  if(r.kind==='visitors')return characterSprite({...r,state,stage:'adult',facing:right},t,true);
  if(r.kind==='wearables')return characterSprite({stage:age,state,facing:right,cosmetics:{preview:r.id}},t);
  if(r.kind==='items'){
    if(detail&&$('use').value==='worn'&&r.wearable)return characterSprite({stage:age,state,facing:right,cosmetics:{preview:r.id}},t);
    return itemSprite(r.id,t,{motion:true,state:{condition:1},interaction:detail&&$('use').value==='active'?{progress:(t%4)/4}:null});
  }
  if(r.kind==='events'&&!r.animated)return null;
  return eventModel(r.kind==='events'?{id:r.animation,family:r.animator,art:r.original}:
    r.kind==='sprites'?{id:`asset:${r.id}`,asset:r.asset}:
    {id:r.id,asset:r.asset,art:r.ascii_art},t,true);
}
function fitBounds(r,detail){
  const key=[r.uid,detail?$('pose').value:'idle',detail?$('use').value:'idle',detail?$('age').value:'adult',detail?facing:true].join('|');
  if(boundsCache.has(key))return boundsCache.get(key);
  let x0=Infinity,y0=Infinity,x1=-Infinity,y1=-Infinity;
  for(let i=0;i<12;i++){
    const m=model(r,i*.7,detail);if(!m)break;
    m.art.forEach((row,y)=>{for(let x=0;x<row.length;x++)if(row[x]!==' '){x0=Math.min(x0,x);y0=Math.min(y0,y);x1=Math.max(x1,x+1);y1=Math.max(y1,y+1);}});
  }
  const b=Number.isFinite(x0)?{x:x0,y:y0,w:x1-x0,h:y1-y0,cx:(x1+x0)/2,cy:(y1+y0)/2}:{x:0,y:0,w:1,h:1,cx:.5,cy:.5};
  if(boundsCache.size>500)boundsCache.clear();boundsCache.set(key,b);return b;
}
function lighting(){return sceneLight({hour:({studio:12,day:12,dusk:18.5,night:23})[$('backdrop').value],season:'fall',biome:'pond',weather:'sunny'});}
function textOnly(ctx,w,h){ctx.fillStyle='#a6bbb4';ctx.textAlign='center';ctx.font='15px Menlo, monospace';ctx.fillText('[ dialogue / notification ]',w/2,h/2-7);ctx.font='12px Menlo, monospace';ctx.fillText('No separate on-screen sprite',w/2,h/2+20);}
function backdrop(ctx,w,h,world=false){
  const key=$('backdrop').value,light=lighting();ctx.fillStyle='#102125';ctx.fillRect(0,0,w,h);
  if(world)ctx.drawImage(images[key==='studio'?'day':key],0,0,w,h);
  else if(key!=='studio'){
    // Crop the actual ground, at full brightness, rather than tinting the artwork.
    ctx.drawImage(images[key],390,280,440,240,0,0,w,h);
  }else{
    ctx.strokeStyle='#21383a';ctx.lineWidth=1;for(let x=16;x<w;x+=24){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,h);ctx.stroke();}for(let y=16;y<h;y+=24){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(w,y);ctx.stroke();}
  }
  return {...light,surface:key==='studio'&&!world?'#102125':light.groundNear};
}
function drawFitted(canvas,r,t,detail=false){
  const ctx=canvas.getContext('2d'),w=canvas.width,h=canvas.height,light=backdrop(ctx,w,h),m=model(r,t,detail);
  if(!m){textOnly(ctx,w,h);return;}
  const b=fitBounds(r,detail),cw=Math.min(detail?17:10,(w-40)/(b.w+4),(h-40)/((b.h+4)*1.5));
  if(r.kind==='items'&&!(detail&&$('use').value==='worn'&&r.wearable)){
    const centerX=(m.width+2)/2;
    const x=w/2+(centerX-1-b.cx)*cw,y=h/2+(m.art.length-b.cy)*cw*1.5;
    painter.draw(ctx,m,x,y,cw/(m.detailScale||1),{shadow:false,surface:light.surface,outline:light.outline});
  }else drawCharacter(ctx,{...m,name:'',scale:1,sun:light.sun,outline:light.outline,
    x:w/2/cw+(m.anchorX??m.width/2)-b.cx,
    y:h/2/cw+((m.groundRow??m.art.length)-b.cy)*1.5},cw,cw,light.surface);
}
function drawWorld(r,t){
  const c=$('world'),ctx=c.getContext('2d'),light=backdrop(ctx,c.width,c.height,true),sx=c.width/240,sy=c.height/112;
  const cheese=characterSprite({stage:$('age').value,state:'idle',facing:true,cosmetics:{}},t);
  drawCharacter(ctx,{...cheese,x:80,y:64,sun:light.sun,outline:light.outline},sx,sy,light.surface);
  const m=model(r,t,true);
  if(m){
    if(r.kind==='items'&&!($('use').value==='worn'&&r.wearable))painter.draw(ctx,m,150*sx,64*sy,sx*itemWorldScale(r.id),{surface:light.surface,outline:light.outline});
    else drawCharacter(ctx,{...m,name:'',x:150,y:64,sun:light.sun,outline:light.outline},sx,sy,light.surface);
  }
  ctx.font='14px Menlo,monospace';ctx.textAlign='center';
  for(const [x,label] of [[80,`Cheese · ${title($('age').value)}`],[150,m?r.name:'Text-only event']]){
    const width=Math.min(420,ctx.measureText(label).width+20);ctx.fillStyle='#0d191ce8';ctx.fillRect(x*sx-width/2,64*sy+18,width,30);ctx.fillStyle='#ead7a5';ctx.fillText(label,x*sx,64*sy+38,400);
  }
}
function node(tag,text,cls){const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;}
function badge(text,warn=false){return node('span',text,`tag${warn?' warning':''}`);}
function groupOptions(){
  $('filter').replaceChildren(new Option('All '+tab,'all'));
  if(tab==='visitors'){for(const v of ['Rare visitors','Regular duck friends'])$('filter').add(new Option(v,v));for(const p of [...new Set(CATALOG.friends.map(r=>r.personality))])$('filter').add(new Option(title(p),p));}
  else if(tab==='events'){
    for(const [label,value] of [['With sprites','animated'],['Text only','text'],['Generic fallback sparkle','fallback']])$('filter').add(new Option(label,value));
    for(const s of [...new Set(records.filter(r=>r.kind===tab).map(r=>r.subtype))])$('filter').add(new Option(title(s),s));
  }else{
    if(tab==='items')$('filter').add(new Option('Wearables / try-on','wearables'));
    for(const s of [...new Set(records.filter(r=>r.kind===tab).map(r=>r.subtype))].sort())$('filter').add(new Option(title(s),s));
  }
}
function selectTab(next){tab=next;page=0;$('search').value='';groupOptions();document.querySelectorAll('[data-tab]').forEach(b=>b.setAttribute('aria-selected',String(b.dataset.tab===tab)));renderGrid();}
function matches(r){
  const q=$('search').value.trim().toLowerCase(),f=$('filter').value;
  return r.kind===tab&&(!q||q.split(/\s+/).every(word=>r.search.includes(word)))&&(f==='all'||r.subtype===f||r.personality===f||f==='wearables'&&r.wearable||f==='animated'&&r.animated||f==='text'&&r.animated===false||f==='fallback'&&r.animated&&eventModel({id:r.animation,family:r.animator},0).asset==='sparkle');
}
const observer=new IntersectionObserver(entries=>entries.forEach(e=>{e.target.dataset.visible=String(e.isIntersecting);}),{rootMargin:'80px'});
function renderGrid(){
  filtered=records.filter(matches);page=Math.max(0,Math.min(page,Math.ceil(filtered.length/PAGE_SIZE)-1));observer.disconnect();cards=[];$('grid').replaceChildren();
  const slice=filtered.slice(page*PAGE_SIZE,(page+1)*PAGE_SIZE);
  for(const r of slice){
    const card=node('article',undefined,'card'),b=node('button',undefined,'open-card');b.setAttribute('aria-label',`Inspect ${r.name}`);b.dataset.uid=r.uid;
    const canvas=document.createElement('canvas');canvas.width=440;canvas.height=266;canvas.setAttribute('aria-hidden','true');
    const body=node('div',undefined,'card-text');body.append(node('h2',r.name),badge(r.kind==='items'?title(r.subtype):r.kind==='events'?r.representation:r.subtype));
    if(r.kind==='visitors')body.append(badge(title(r.identity.species)));
    if(r.wearable)body.append(badge('Try it on'));
    body.append(node('p',r.kind==='items'?`${title(r.family)} design · ${familyCounts[r.family]} items share this family`:r.kind==='wearables'?`${title(r.family)} · fitted on Cheese`:r.kind==='visitors'?r.identity.habit:r.kind==='events'?title(r.source)+' · '+title(r.group):r.representation));
    body.append(node('div',r.id,'id'));b.append(canvas,body);card.append(b);$('grid').append(card);b.onclick=()=>openDetail(r);observer.observe(card);card.dataset.visible='true';cards.push({r,canvas,card});drawFitted(canvas,r,time);
  }
  if(!slice.length)$('grid').append(node('div','No matches. Try another name, ID or category.','empty'));
  $('count').textContent=`${filtered.length.toLocaleString()} of ${counts[tab].toLocaleString()} ${tab==='sprites'?'event sprites':tab} · ${slice.length?'click any card to inspect':'adjust your filters'}`;
  $('page').textContent=`${page+1} / ${Math.max(1,Math.ceil(filtered.length/PAGE_SIZE))}`;$('prev').disabled=page===0;$('next').disabled=(page+1)*PAGE_SIZE>=filtered.length;
}
function field(dl,label,value){if(value===undefined||value===null||value==='')return;dl.append(node('dt',label),node('dd',String(value)));}
function fold(parent,label,value){if(!value)return;const d=node('details'),pre=node('pre',typeof value==='string'?value:JSON.stringify(value,null,2));d.append(node('summary',label),pre);parent.append(d);return d;}
function openDetail(r){
  selected=r;$('pose').value='idle';$('use').value='idle';facing=true;$('facing').textContent='Face left';
  const duck=r.kind==='visitors'||r.kind==='wearables',wearable=Boolean(r.wearable);$('pose').disabled=!duck;$('facing').disabled=!duck;$('use-label').hidden=r.kind!=='items';$('use').options[2].disabled=!wearable;
  for(const option of $('pose').options)option.disabled=r.kind==='visitors'&&!['duck','duckling'].includes(r.identity.species)&&['swimming','preening','dancing','eating'].includes(option.value);
  $('detail-title').textContent=r.name;$('detail-id').textContent=r.uid;
  const info=$('info');info.replaceChildren();info.append(badge(r.representation,r.kind==='events'&&r.animated===false),node('p',r.description||'Current production artwork.'));
  const dl=node('dl'),m=model(r,0,true);field(dl,'Artwork',r.kind==='items'?`${r.family} family (${familyCounts[r.family]} catalog entries)`:r.kind==='wearables'?`${r.family} fitted to the D10 rig`:r.kind==='visitors'?`${title(r.identity.species)} · ${r.identity.shape} silhouette · ${title(r.identity.prop)}`:m?m.asset||r.asset:'No separate sprite');
  if(r.kind==='events'&&m)field(dl,'Shared artwork',`${eventCounts[m.asset||'fallback']} event records resolve to this asset (${m.asset||'fallback'})`);
  field(dl,'Movement',r.movement||(r.kind==='events'&&r.animated?`${r.animator}. This view previews the sprite, not its path or particle emitter.`:undefined));
  if(r.kind==='visitors'){field(dl,'Signature habit',r.identity.habit);field(dl,'Live pose','Movement and interaction choose the live pose. Select Signature habit to see the occupation loop.');}
  if(r.kind==='items'){const p=itemProfile(r,r.family);field(dl,'Interaction',`${p.verb} · ${p.kind} · ${p.material}`);field(dl,'Rarity / sources',`${r.rarity} / ${(r.sources||[]).join(', ')}`);if(r.wearable)field(dl,'Fitted wearable',`${r.wearable.slot} · ${r.wearable.family}`);}
  if(r.kind==='wearables'){field(dl,'Attachment / animation',`${r.wearable.slot} · ${r.wearable.motion}`);field(dl,'Catalog overlap',catalog.some(i=>i.id===r.id)?'Also listed in Items; this view shows its fitted appearance.':'Wardrobe-only definition, outside the main item catalog.');}
  field(dl,'Animation recipe',r.animator);field(dl,'Source',r.source||r.subtype);info.append(dl);
  if(r.identity)info.append(node('div','In their own words','section-label'),node('p',r.identity.voice.greeting,'quote'),node('p',r.identity.voice.main,'quote'));
  else if(r.greeting)info.append(node('div','Greeting','section-label'),node('p',r.greeting,'quote'));
  if(r.identity)fold(info,'Named voice, stories and friendship dialogue',r.identity.voice);
  if(r.kind==='stories')for(const [i,s] of r.scenes.entries()){
    const d=node('details');d.append(node('summary',`Scene ${i+1}`),node('p',s.text,'quote'));
    for(const choice of s.choices)d.append(node('p',choice.label),node('p',choice.reply,'quote'));info.append(d);
  }
  fold(info,'Original / legacy artwork',r.original);const frame=fold(info,'Current ASCII frame (copyable)',m?.art.join('\n'));if(frame)frame.querySelector('pre').id='current-frame';
  if(r.kind==='visitors'&&r.subtype==='Rare visitors')fold(info,'Additional original dialogue & friendship secrets',{greeting:r.greeting,farewell:r.farewell,conversations:r.conversations,return_greetings:r.return_greetings,friend_greetings:r.friend_greetings,best_friend_greetings:r.best_friend_greetings,secrets:r.secrets});
  fold(info,'Definition / metadata',r.definition||(r.kind==='items'?catalog.find(i=>i.id===r.id):r.kind==='wearables'?r.wearable:r.kind==='stories'?DATA.stories[r.id]:undefined));
  info.append(node('div','Review notes','section-label'));const note=node('textarea',undefined,'review');note.id='review-note';note.setAttribute('aria-label','Review notes for '+r.name);note.placeholder='What should change about this artwork?';note.value=notes[r.uid]?.text||'';
  const status=node('p','Notes are only for this atlas; they do not change the game.','note');
  note.oninput=()=>{notes[r.uid]={name:r.name,text:note.value};try{localStorage.setItem('cheese-art-atlas-notes',JSON.stringify(notes));status.textContent='Saved in this browser. Export notes to keep a portable copy.';}catch{status.textContent='Stored for this session only. Export notes before closing.';}};
  const actions=node('div',undefined,'review-actions'),copy=node('button','Copy ID'),download=node('button','Export notes');copy.onclick=async()=>{try{await navigator.clipboard.writeText(r.uid);toast('Copied '+r.uid);}catch{toast(r.uid);}};download.onclick=exportNotes;actions.append(copy,download);info.append(note,status,actions);
  $('large-caption').textContent=r.kind==='events'&&r.animated===false?'This event delivers text. The game does not attach a separate sprite.':r.kind==='items'?'Enlarged item art. Switch to Interacting to inspect the existing interaction animation; fitted wearables also support try-on.':'Enlarged production sprite. Animation playback does not imply independent movement.';
  if(!$('detail').open)$('detail').showModal();$('detail').scrollTop=0;drawDetail();
}
function drawDetail(){if(!selected||!$('detail').open)return;drawFitted($('large'),selected,time,true);drawWorld(selected,time);$('time').textContent=`${time.toFixed(1)} s`;$('scrub').value=Math.round((time%12)*10);
  if($('current-frame'))$('current-frame').textContent=model(selected,time,true).art.join('\n');
  if(selected.kind==='items'||selected.kind==='wearables')$('large-caption').textContent=$('use').value==='worn'||selected.kind==='wearables'?$('age').value==='egg'?'Egg stage: the current rig has no wearable attachment points. Clothing appears after hatching.':'Current fitted wearable on Cheese. Change his age or pose to inspect the fit.':$('use').value==='active'?'Current item interaction animation, looping through its four-second preview.':'Enlarged item art. Switch to Interacting for the current interaction animation, or try on a fitted wearable.';
}
function setPlaying(value){playing=value;$('play').textContent=value?'Pause animation':'Play animation';$('play').setAttribute('aria-pressed',String(value));$('detail-play').textContent=value?'Pause':'Play';}
function toast(message){$('toast').textContent=message;$('toast').style.display='block';setTimeout(()=>$('toast').style.display='none',2500);}
function exportNotes(){
  const entries=Object.entries(notes).filter(([,n])=>n.text.trim()),payload={build:DATA.build,notes:Object.fromEntries(entries)};
  const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='Cheese - Art Review Notes.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),5000);toast(`Exported ${entries.length} review notes`);
}

for(const key of ['day','dusk','night']){images[key]=new Image();images[key].src=DATA.backgrounds[key];await images[key].decode();}
for(const kind of Object.keys(counts)){const b=node('button',`${title(kind==='sprites'?'event sprites':kind)}  ${counts[kind]}`);b.dataset.tab=kind;b.setAttribute('aria-selected',String(kind===tab));b.onclick=()=>selectTab(kind);$('tabs').append(b);}
for(const age of DUCK_AGES)$('age').add(new Option(age.name||title(age.id),age.id));$('age').value='adult';
$('build').textContent=`v${DATA.build.version} · ${DATA.build.commit} · ${DATA.build.date} · ${records.length.toLocaleString()} entries · fully offline`;
$('search').oninput=()=>{page=0;renderGrid();};$('filter').onchange=()=>{page=0;renderGrid();};
$('prev').onclick=()=>{page--;renderGrid();$('grid').scrollIntoView({block:'start'});};$('next').onclick=()=>{page++;renderGrid();$('grid').scrollIntoView({block:'start'});};
$('backdrop').onchange=()=>{$('detail-backdrop').value=$('backdrop').value;cards.forEach(({r,canvas})=>drawFitted(canvas,r,time));drawDetail();};
$('detail-backdrop').onchange=()=>{$('backdrop').value=$('detail-backdrop').value;$('backdrop').dispatchEvent(new Event('change'));};
$('play').onclick=()=>setPlaying(!playing);$('detail-play').onclick=()=>setPlaying(!playing);$('close').onclick=()=>$('detail').close();
$('detail').addEventListener('click',e=>{if(e.target===$('detail')&&e.offsetX<0)$('detail').close();});
$('scrub').oninput=()=>{setPlaying(false);time=Number($('scrub').value)/10;drawDetail();};
for(const id of ['pose','age','use'])$(id).onchange=()=>{
  if(id==='use'){const canPose=Boolean(selected?.personality)||$('use').value==='worn';$('pose').disabled=!canPose;$('facing').disabled=!canPose;}
  drawDetail();
};
$('facing').onclick=()=>{facing=!facing;$('facing').textContent=facing?'Face left':'Face right';drawDetail();};$('export-notes').onclick=exportNotes;
if(matchMedia('(prefers-reduced-motion: reduce)').matches)setPlaying(false);
selectTab('visitors');
let lastDraw=0;
function tick(now){const dt=last?Math.min(.2,(now-last)/1000):0;last=now;if(playing)time=(time+dt)%12;
  if(playing&&now-lastDraw>=100){lastDraw=now;if($('detail').open)drawDetail();else cards.filter(v=>v.card.dataset.visible==='true').forEach(({r,canvas})=>drawFitted(canvas,r,time));}
  requestAnimationFrame(tick);
}
requestAnimationFrame(tick);
// Read-only hooks used by the exporter to audit the delivered standalone file.
window.atlas={counts,records,selectTab,open:uid=>openDetail(byUID.get(uid)),model,drawFitted,setTime:t=>{time=t;drawDetail();},setPlaying};
window.galleryReady=true;
