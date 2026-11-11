import {renderMinds,refreshConversation} from './minds-notebook.mjs';
import {catalog,itemSprite,itemProfile,itemFamily,ItemPainter} from './ultra-items.mjs';
import {characterSprite,drawCharacter} from './ultra-characters.mjs';
import {eventModel,EVENT_ASSETS} from './event-art.mjs';
import {guestProfile} from './visitor-rig.mjs';
import {storyModel} from './story-art.mjs';
import {PondArrangement} from './pond-layout.mjs';
import LIGHTING from './animation/lighting.json' with {type:'json'};
import KEEPSAKES from './animation/keepsakes.json' with {type:'json'};
import {keepsakeSummary} from './keepsake-state.mjs';
import {keepsakePose} from './keepsake-routines.mjs';
const names=new Map(catalog.map(i=>[i.id,i]));
const pretty=s=>String(s||'').replaceAll('_',' ');
const percent=n=>`${Math.round((n||0)*100)}%`;
const el=(tag,text,cls)=>{const node=document.createElement(tag);if(text!==undefined)node.textContent=text;if(cls)node.className=cls;return node;};
export class PondJournal{
 constructor(){
  this.tab='pond';this.selected=null;this.frame=null;this.painter=new ItemPainter();this.last=0;this.lastRender=0;this.searchQuery='';this.arrangement=new PondArrangement(this);
  this.dialog=el('dialog',undefined,'pond-journal');this.dialog.id='pond-journal';this.dialog.setAttribute('aria-label','Living pond journal');
  const head=el('header');head.append(el('div','CHEESE’S FIELD NOTEBOOK','pond-eyebrow'),el('h1','Notes from the pond.'));
  this.closeButton=el('button','Close ×');this.closeButton.onclick=()=>this.dialog.close();head.append(this.closeButton);
  this.nav=el('nav');this.nav.setAttribute('aria-label','Journal sections');
  for(const [id,label] of [['pond','The pond'],['mind','Cheese’s plans'],['personalities','Personalities'],['belongings','Belongings'],['arrange','Arrange'],['friends','Friends'],['weather','Weather'],['projects','Projects'],['field','Field notes'],['memories','Memories']]){
   const b=el('button',label);b.dataset.tab=id;b.onclick=()=>{this.tab=id;this.selected=null;this.selectedInstance=null;this.render(true);};this.nav.append(b);
  }
  this.body=el('div',undefined,'pond-body');this.status=el('div',undefined,'pond-live-status');this.status.setAttribute('role','status');
  this.dialog.append(head,this.nav,this.status,this.body);document.body.append(this.dialog);
  this.dialog.addEventListener('close',()=>document.getElementById('world').focus());
  this.dialog.addEventListener('keydown',e=>e.stopPropagation());
  const animate=t=>{if(this.open){this.paint(t/1000);if(t-this.last>1000){this.updateDynamic();if(this.tab!=='arrange'&&t-this.lastRender>5000&&!['INPUT','SELECT','TEXTAREA'].includes(document.activeElement.tagName))this.render();this.last=t;}}requestAnimationFrame(animate);};requestAnimationFrame(animate);
 }
 get open(){return this.dialog.open;}
 show(tab='pond',selected=null,instance=null){this.tab=tab;this.selected=selected;this.selectedInstance=instance;if(!this.open)this.dialog.showModal();this.render(true);this.closeButton.focus();}
 update(frame){this.frame=frame;if(this.open)this.updateDynamic();}
 get world(){return this.frame?.scene?.living;}
 command(action,target='',extra={}){window.cheese.input({type:'pond',action,target,...extra});this.status.textContent='Cheese is considering that…';setTimeout(()=>{if(this.open&&this.tab!=='arrange'&&!['INPUT','SELECT','TEXTAREA'].includes(document.activeElement.tagName))this.render();},350);}
 button(text,action,target,disabled=false,extra={}){const b=el('button',text,'pond-action');b.disabled=disabled;b.onclick=()=>this.command(action,target,extra);return b;}
 legacy(text,action){const b=el('button',text,'pond-action');b.onclick=()=>{this.dialog.close();window.cheese.input({type:'action',action});};return b;}
 card(title,description){const c=el('section',undefined,'pond-card');c.append(el('h2',title));if(description)c.append(el('p',description));return c;}
 meter(parent,label,value){const row=el('label',undefined,'pond-meter');const text=el('span',label),m=el('meter');m.min=0;m.max=1;m.value=Math.max(0,Math.min(1,value||0));m.setAttribute('aria-label',label);row.append(text,m,el('span',percent(value)));parent.append(row);}
 preview(parent,kind,id,large=false,instance=''){const canvas=el('canvas',undefined,large?'pond-preview large':'pond-preview');canvas.width=large?720:360;canvas.height=large?390:220;canvas.dataset.kind=kind;canvas.dataset.id=id;canvas.dataset.instance=instance;canvas.setAttribute('aria-label',names.get(id)?.name||pretty(id));parent.append(canvas);}
 updateDynamic(){
  const w=this.world;if(!w)return;
  if(this.tab==='arrange'){this.arrangement.update();return;}
  refreshConversation(this);
  const p=w.plan;this.status.textContent=p?`${p.label} · ${p.paused?'paused':pretty(p.phase)} · ${Math.round(p.progress*100)}%`:'Cheese is free to choose what comes next.';
  for(const bar of this.body.querySelectorAll('[data-progress]'))bar.value=p?.progress||0;
  for(const card of this.body.querySelectorAll('[data-keepsake-id]')){
   const id=card.dataset.keepsakeId,instance=card.dataset.keepsakeInstance,state=instance?w.instances?.[instance]:w.objects[id];if(!state)continue;
   card.querySelector('[data-keepsake-summary]').textContent=keepsakeSummary(id,state);
   const meter=card.querySelector('[aria-label="Rainwater"]');if(meter){meter.value=(state.keepsake?.litres||0)/KEEPSAKES[id].capacity;meter.nextElementSibling.textContent=percent(meter.value);}
  }
  for(const card of this.body.querySelectorAll('[data-light-id]')){
   const id=card.dataset.lightId,instance=card.dataset.lightInstance,light=(instance?w.instances?.[instance]:w.objects[id])?.lighting;
   if(!light)continue;
   const outside=instance?[...(this.frame.scene.items||[]),...(this.frame.scene.structures||[])].some(o=>o.instance===instance):w.placed.includes(id);
   const meter=card.querySelector('[aria-label="Light"]');meter.value=Math.max(0,Math.min(1,light.level||0));meter.nextElementSibling.textContent=percent(light.level);
   card.querySelector('[data-light-summary]').textContent=`${pretty(light.mode)} · ${light.switches} careful adjustments`;
   for(const button of card.querySelectorAll('[data-light-mode]')){button.disabled=Boolean(p)||!outside||light.mode===button.dataset.lightMode;button.setAttribute('aria-pressed',String(light.mode===button.dataset.lightMode));}
  }
  // Keep focused controls and scroll position stable as live frames arrive.
  const signature=[p?.kind,p?.paused,...w.projects.map(p=>p.stage),Object.keys(w.objects).length,w.friends.length,w.rare_guest?.id,w.rare_guest?.last_line,w.story?.id,w.story?.step,w.garden.map(p=>p.plant+':'+p.stage).join(',')].join('|');
  if(this.signature&&signature!==this.signature&&!['INPUT','SELECT','TEXTAREA'].includes(document.activeElement.tagName))this.render();this.signature=signature;
 }
 render(reset=false){
  this.lastRender=performance.now();
  const w=this.world,scroll=this.body.scrollTop,focus=this.body.contains(document.activeElement)?document.activeElement.textContent:null;
  this.body.replaceChildren();for(const b of this.nav.children)b.setAttribute('aria-current',b.dataset.tab===this.tab?'page':'false');
  if(!w){this.body.append(el('p','Start or continue a game to open Cheese’s living journal.'));return;}
  const grid=el('div',undefined,'pond-cards');this.body.append(grid);const busy=Boolean(w.plan);
  if(this.tab==='arrange'){this.arrangement.mount(grid);
  }else if(this.tab==='personalities'){renderMinds(this,grid);
  }else if(this.tab==='pond'){
   if(w.story){const story=w.story,c=this.card(story.title,story.text);c.classList.add('pond-story');this.preview(c,'story',story.id);c.append(el('small',`Chapter ${story.step+1} of ${story.total}`));
    for(const choice of story.choices){const row=el('div',undefined,'pond-choice');row.append(this.button(choice.label,'story_choice',`${story.id}:${story.step}:${choice.id}`,!choice.available));const cost=Object.entries(choice.cost||{}).map(([id,n])=>`${n} ${pretty(id)}`).join(', ');if(cost)row.append(el('p','Uses '+cost));const impact=Object.entries(choice.effect).map(([id,n])=>`${id==='warmth'?'community warmth':pretty(id)} +${n<1?Math.round(n*100)+'%':n}`).join(' · ');row.append(el('small',impact));c.append(row);}grid.append(c);
   }
   const garden=this.card('A growing garden','The real garden plots share the weather. Rain waters them; hot, dry conditions stress thirsty plants.');
   for(const plot of w.garden){const row=el('div',undefined,'pond-forecast');row.append(el('h3',`Plot ${plot.id+1} · ${plot.plant?pretty(plot.plant):'ready to plant'}`));
    if(plot.plant){this.preview(row,'item',plot.plant);row.append(el('p',pretty(plot.stage)));this.meter(row,'Water',plot.water);this.meter(row,'Health',plot.health);row.append(this.button('Water','garden_water',String(plot.id),plot.water>.7),this.button('Harvest','garden_harvest',String(plot.id),plot.stage!=='harvestable'));}
    else{const select=el('select');select.setAttribute('aria-label','Seed for plot '+(plot.id+1));for(const [id,n] of Object.entries(w.seeds).filter(([,n])=>n>0)){const option=el('option',`${pretty(id)} ×${n}`);option.value=id;select.append(option);}const b=el('button','Plant');b.disabled=!select.options.length;b.onclick=()=>this.command('garden_plant',`${plot.id}:${select.value}`);row.append(select,b);}garden.append(row);}
   garden.append(this.legacy('Garden, harvest & supplies','inventory'));grid.append(garden);
   const intro=this.card(w.location,'The water, soil and wildlife respond to weather and to the care you put into this place. Explore, make things, spend time with friends, or simply let Cheese choose.');
   if(w.offline)intro.append(el('p',w.offline,'pond-note'));
   for(const [action,label] of [['forage','Forage the shoreline'],['observe','Watch the wildlife'],['restore','Restore the shallows'],['garden','Tend the garden'],['practice','Practice a tune'],['rest','Find a quiet place'],['wander','Take a little wander']])intro.append(this.button(label,action,'',busy));grid.append(intro);
   const eco=this.card('A connected habitat','Flowering plants feed insects. Insects attract birds; clean, deep water supports fish. Restored reed beds help the pond hold water and filter runoff.');
   for(const [key,label] of [['soil','Living soil'],['water','Pond level'],['clarity','Water clarity'],['flowers','Flowers'],['insects','Insects'],['fish','Fish'],['birds','Birds']])this.meter(eco,label,w.ecology[key]);grid.append(eco);
   const resources=this.card('What grows here','Foraging draws from local patches. Give a picked-over place time to recover or visit another biome.');for(const [id,value] of Object.entries(w.stocks))this.meter(resources,pretty(id),value/12);resources.append(this.legacy('Explore another area','explore'));grid.append(resources);
   const systems=this.card('The rest of Cheese’s world','The original collections, quests, mini-games, fishing, garden, crafting, trading, festivals and stories remain available through the care menu.');
   for(const [label,action] of [['Explore & discover','explore'],['Crafting','craft'],['Building','build'],['Inventory & equipment','inventory'],['Shop','shop'],['Full menu & help','help']])systems.append(this.legacy(label,action));grid.append(systems);
  }else if(this.tab==='mind'){
   const c=this.card('What Cheese is doing',w.plan?.label||'Taking in the world.');this.preview(c,'cheese','Cheese');
   if(w.plan){const progress=el('progress');progress.max=1;progress.value=w.plan.progress;progress.dataset.progress='plan';c.append(progress,el('p',`${w.plan.automatic?'Cheese chose this.':'You suggested this.'} ${pretty(w.plan.phase)}${w.plan.paused?' · paused':''}`));if(w.plan.paused)c.append(this.button('Resume','resume'));c.append(this.button('Set this aside','cancel'));}grid.append(c);
   const meet=el('button','Talk, memories & personality','pond-action');meet.onclick=()=>this.show('personalities','cheese');c.append(meet);
   const intent=this.card('A nudge, not a script','Cheese weighs needs, weather, habits, favorite possessions and who is visiting. Urgent needs still come first.');
   for(const policy of ['balanced','curious','social','homebody']){const b=this.button((policy===w.policy?'✓ ':'')+pretty(policy),'policy',policy);b.setAttribute('aria-pressed',policy===w.policy);intent.append(b);}
   intent.append(this.button(w.auto?'Pause extended routines':'Enable extended routines','autonomy'));for(const d of w.decision)intent.append(el('p',`${pretty(d.kind)} — ${d.reason}.`));grid.append(intent);
   const skills=this.card('Things learned by doing','Skills grow through completed activities. Repeating familiar actions builds habits; trying different objects broadens experience.');for(const [id,xp] of Object.entries(w.skills)){const level=Math.floor(Math.sqrt(xp/12));skills.append(el('p',`${pretty(id)} · level ${level} · ${Math.round(xp)} practice`));}grid.append(skills);
  }else if(this.tab==='belongings'){
   const list=this.card('Well-loved things','Click an object in the world to inspect it here. The catalogue’s “Item art” button still lets you browse everything without granting items.');
   const search=el('input');search.type='search';search.placeholder='Find an owned item';search.setAttribute('aria-label','Find an owned item');search.value=this.searchQuery;list.append(search);
   const entries=el('div',undefined,'pond-item-list');list.append(entries);
   const drawList=()=>{entries.replaceChildren();for(const id of Object.keys(w.objects).filter(id=>(names.get(id)?.name||id).toLowerCase().includes(search.value.toLowerCase())).sort((a,b)=>(names.get(a)?.name||a).localeCompare(names.get(b)?.name||b))){const b=el('button',names.get(id)?.name||pretty(id));b.onclick=()=>{this.selected=id;this.selectedInstance=null;this.render();};b.setAttribute('aria-pressed',id===this.selected);entries.append(b);}};search.oninput=()=>{this.searchQuery=search.value;drawList();};drawList();grid.append(list);
   const id=this.selected||Object.keys(w.objects)[0],item=names.get(id);
   const copies=[...(this.frame.scene.items||[]),...(this.frame.scene.structures||[])].filter(p=>p.id===id&&p.instance);
   if(!this.selectedInstance&&copies.length)this.selectedInstance=copies.at(-1).instance;
   const instance=this.selectedInstance,state=instance?w.instances?.[instance]:w.objects[id],outside=!instance||copies.some(p=>p.instance===instance);
   if(item&&state){const detail=this.card(item.name,item.description);this.preview(detail,'item',id,true,instance||'');
    if(copies.length>1){const picker=el('select');picker.setAttribute('aria-label','Choose a placed copy');copies.forEach((copy,i)=>{const option=el('option',`Copy ${i+1} · ${copy.x<44?'west side':copy.x>88?'east side':'middle of the pond'}`);option.value=copy.instance;picker.append(option);});picker.value=instance;picker.onchange=()=>{this.selectedInstance=picker.value;this.render();};detail.append(picker);}
const p=itemProfile(item,itemFamily(id));detail.append(el('p',`${pretty(p.material)} · ${pretty(p.skill)} · ${state.uses} uses${instance?(outside?' · placed at home':' · put away'):w.placed.includes(id)?' · placed at home':''}`));for(const [key,label] of [['condition','Condition'],['wetness','Wetness'],['dirt','Dirt'],['bond','Familiarity']])this.meter(detail,label,state[key]);
    detail.append(this.button(p.verb,'item',id,busy||!outside||['food','wearable'].includes(p.kind),{instance}),this.button('Brush & polish','clean_item',id,busy||!outside||state.dirt<.05,{instance}),this.button('Repair · 1 twig','repair_item',id,busy||!outside||state.condition>=.95,{instance}));if(['food','wearable'].includes(p.kind))detail.append(this.legacy(p.kind==='food'?'Eat through inventory':'Open wardrobe & items','inventory'));grid.append(detail);
    if(w.layout?.items.some(i=>i.id===id)&&(!instance||w.layout.copies?.some(p=>p.id===id&&p.instance===instance))){const arrange=el('button',w.placed.includes(id)?'Move or store':'Find a place','pond-action');arrange.onclick=()=>this.show('arrange',id,instance);detail.append(arrange);}
    if(state.botany){this.meter(detail,'Soil moisture',state.botany.moisture);this.meter(detail,'Plant health',state.botany.health);detail.append(el('p',state.botany.last_care?'Last care: '+pretty(state.botany.last_care):'Rain waters the roots. Warm, dry air slowly draws moisture out of the soil.'));}
    if(state.keepsake&&KEEPSAKES[id]){
     detail.dataset.keepsakeId=id;detail.dataset.keepsakeInstance=instance||'';
     const summary=el('p',keepsakeSummary(id,state));summary.dataset.keepsakeSummary='';detail.append(summary);
     if(KEEPSAKES[id].type==='barrel'){this.meter(detail,'Rainwater',state.keepsake.litres/KEEPSAKES[id].capacity);detail.append(el('p','Rain collects through the screened cover. Ice holds it still; warm dry air slowly draws it away.'));}
    }
    if(state.lighting&&LIGHTING[id]){
     const light=state.lighting;detail.dataset.lightId=id;detail.dataset.lightInstance=instance||'';this.meter(detail,'Light',light.level);const summary=el('p',`${pretty(light.mode)} · ${light.switches} careful adjustments`);summary.dataset.lightSummary='';detail.append(summary);
     if(LIGHTING[id].control!=='observe')for(const [mode,label] of [['auto','At dusk'],['on','On'],['off','Off']]){
      const button=this.button(label,'lighting_mode',id,busy||!outside||light.mode===mode,{instance,text:mode});button.dataset.lightMode=mode;button.setAttribute('aria-pressed',String(light.mode===mode));detail.append(button);
     }
     detail.append(el('p',id==='firefly_swarm'?'Wild fireflies follow dusk and the seasons.':id==='eternal_flame'?'This flame never goes out.':LIGHTING[id].exposed?'Rain softens exposed firelight. Cheese adjusts the flame when he reaches it.':'Cheese walks over to work the control. At dusk follows the pond clock.'));
    }
   }else if(instance)grid.append(this.card('Put away or moved','This copy is no longer outside. Choose a belonging from the list to see its current home.'));else grid.append(this.card('Make a collection','Find resources, craft things or visit the shop. New belongings appear here as you acquire them.'));
  }else if(this.tab==='friends'){
   if(w.rare_guest){const guest=w.rare_guest,c=this.card(guest.name,guest.bio);this.preview(c,'friend',guest.id);c.append(el('p',guest.habit),el('p',pretty(guest.relationship)));
    if(guest.last_line)c.append(el('p',guest.last_line,'pond-note'));
    const meet=el('button','Talk with '+guest.name,'pond-action');meet.onclick=()=>this.show('personalities',guest.id);c.append(meet);
    c.append(this.button('Say hello','guest_chat',guest.id),this.button('Ask about their adventures','guest_hobby',guest.id),this.button('Keep them company','guest_company',guest.id));grid.append(c);}
   const community=this.card('A welcoming pond','Kindness to visitors and passing strangers is remembered here. A warmer community eases loneliness between visits and makes shared time more restorative.');this.meter(community,'Community warmth',w.community?.warmth||0);community.append(el('p',`${w.community?.gatherings||0} shared gatherings`));grid.append(community);
   if(!w.friends.length)grid.append(this.card('Room for friends','Visitors arrive as you play. Once you meet someone, their routines, memories and shared plans appear here.'));
   for(const friend of w.friends){const identity=guestProfile(friend),c=this.card(friend.name,identity.bio);this.preview(c,'friend',friend.id);c.append(el('p',identity.habit),el('p',`${pretty(friend.personality)} · ${pretty(friend.relationship)} · ${friend.activity} at ${friend.location}`));for(const [key,label] of [['trust','Trust'],['warmth','Warmth'],['reliability','Reliability']])this.meter(c,label,friend[key]);c.append(el('p',`Would enjoy: ${friend.want}.`),this.button('Invite over','invite',friend.id),this.button('Make a promise','promise',friend.id),this.button('Share their favorite activity','share',friend.id,busy));
    for(const promise of w.promises.filter(p=>p.friend===friend.id).slice(-2))c.append(el('p',`${pretty(promise.activity)} · ${promise.status}${promise.status==='promised'?' · '+Math.max(0,Math.ceil((promise.deadline-w.elapsed)/60))+' minutes left':''}`,'pond-note'));
    const meet=el('button','Talk & get to know '+friend.name,'pond-action');meet.onclick=()=>this.show('personalities',friend.id);c.append(meet);
    for(const memory of friend.memories.slice(-2))c.append(el('p',`Remembered ${memory.activity} together in ${pretty(memory.weather)}.`));grid.append(c);}
  }else if(this.tab==='weather'){
   const c=this.card(pretty(w.weather.type).toUpperCase(),'Fronts travel through the seasons. Conditions accumulate: rain soaks objects and gardens, snow settles, water freezes, and sunlight dries surfaces.');
   c.append(el('p',`${Math.round(w.ecology.temperature)}°C · wind ${percent(w.ecology.wind)} · next front in about ${Math.max(0,Math.ceil((w.weather.until-w.elapsed)/60))} minutes`));for(const [key,label] of [['wetness','Ground wetness'],['snow','Snow cover'],['ice','Ice'],['water','Pond level']])this.meter(c,label,w.ecology[key]);grid.append(c);
   const forecast=this.card('On the horizon','These are the next fronts in the current biome. Travel takes you into another local forecast.');for(const [i,f] of (w.weather.forecast||[]).entries()){const section=el('div',undefined,'pond-forecast');section.append(el('h3',`${i+1}. ${pretty(f.type)}`),el('p',`${Math.round(f.duration/60)} minutes · strength ${percent(f.intensity)}`));forecast.append(section);}grid.append(forecast);
   const advice=this.card('Read the conditions',w.ecology.temperature<0?'Cold water holds ice. Look after shelter and wait for a thaw.':w.ecology.wetness>.6?'The ground is soaked. Gardens need less watering; mud and runoff can cloud the shallows.':w.ecology.water<.4?'The pond is low. Reed beds help retain water; let nearby patches recover.':'Good conditions for observing wildlife, working on projects and spending time outside.');advice.append(this.button('Watch the habitat','observe','',busy),this.button('Care for the water','restore','',busy));grid.append(advice);
  }else if(this.tab==='projects'){
   for(const project of w.projects){const c=this.card(project.name,project.description);this.preview(c,'project',project.id);c.append(el('p',`${project.stage}/3 stages · ${project.next}`));let ready=true;for(const [id,amount] of Object.entries(project.cost)){const have=project.have[id];if(have<amount)ready=false;c.append(el('p',`${pretty(id)}: ${have}/${amount}`,have<amount?'pond-missing':'pond-enough'));}c.append(this.button(project.stage===3?'Complete':'Work on this stage','project',project.id,busy||!ready||project.stage===3));grid.append(c);}
  }else if(this.tab==='field'){
   const c=this.card('Field notebook','Quiet observation and encounters build a record of the living world. The local food web influences which animals you notice.');c.append(this.button('Observe quietly','observe','',busy));grid.append(c);
   for(const [id,count] of Object.entries(w.knowledge)){const card=this.card(pretty(id),`${count} observations`);this.preview(card,'wildlife',id);grid.append(card);}
   const sightings=w.journal.filter(e=>e.kind==='encounter');for(const entry of sightings.slice(-12).reverse())grid.append(this.card('A passing encounter',entry.text));
  }else if(this.tab==='memories'){
   for(const entry of [...w.journal].reverse()){const c=this.card(pretty(entry.kind),entry.text);c.append(el('small',`${Math.max(0,Math.floor((w.elapsed-entry.at)/60))} minutes ago`));grid.append(c);}if(!w.journal.length)grid.append(this.card('The first page','Shared experiences, care, weather changes and discoveries will collect here.'));
  }
  this.body.scrollTop=reset?0:scroll;
  if(focus){const b=[...this.body.querySelectorAll('button')].find(b=>b.textContent===focus&&!b.disabled);b?.focus({preventScroll:true});}
  this.paint(performance.now()/1000);
 }
 paint(time){
  const w=this.world;if(!w)return;const motion=this.frame?.scene?.motion!==false;if(!motion)time=0;
  if(this.tab==='arrange'){this.arrangement.paint(performance.now()/1000);return;}
  for(const canvas of this.body.querySelectorAll('canvas[data-kind]')){
   const ctx=canvas.getContext('2d'),{kind,id,instance}=canvas.dataset;ctx.fillStyle='#132721';ctx.fillRect(0,0,canvas.width,canvas.height);
   ctx.fillStyle='#345745';ctx.font='11px Menlo,monospace';for(let x=4;x<canvas.width;x+=13)ctx.fillText(x%3?'\'':'.',x,canvas.height-18-(x%5));
   if(kind==='item'||kind==='project'){
    const project={reed_beds:'reed',orchard:'tree_oak',observatory:'telescope',clubhouse:'basic_nest',workshop:'workbench',trail:'bridge'};
    const interaction=w.plan?.target===id&&(!instance||w.plan.instance===instance)?w.plan:null;
    const model=itemSprite(kind==='project'?project[id]:id,time,{motion,state:instance?w.instances?.[instance]:w.objects[id],interaction,pose:{keepsake:interaction?.keepsake_work?keepsakePose(interaction.keepsake_work,motion):null}});
    const cw=Math.min((canvas.width-30)/(model.width+2),(canvas.height-45)/((model.art.length+2)*1.5))/(model.detailScale||1);
    this.painter.draw(ctx,model,canvas.width/2,canvas.height-22,cw,{surface:'#142a22',outline:'#091d18'});
   }else{
    let model;if(kind==='story'){if(!w.story||w.story.id!==id)continue;model=storyModel(w.story,{state:'signature'},time,motion);model.name='';}else if(kind==='wildlife'){model=eventModel({id,asset:id,family:'',art:EVENT_ASSETS[id]?.frames?.idle},time,motion);}else if(kind==='friend'){const friend=w.friends.find(f=>f.id===id)||(w.rare_guest?.id===id?w.rare_guest:null);if(!friend)continue;model=characterSprite({...friend,state:'signature',activity:'signature',stage:'adult'},time,true);model.name='';}else model=characterSprite({...this.frame.scene.duck,state:w.plan?.kind==='rest'?'sleeping':this.frame.scene.duck.state},time);
    const sx=kind==='story'&&model.profileId==='lost_duckling'?12:kind==='wildlife'?5:6,sy=5;drawCharacter(ctx,{...model,x:canvas.width/2/sx,y:(canvas.height-22)/sy,sun:.7},sx,sy,'#132721');
   }
  }
 }
}
