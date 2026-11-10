// Resident notebook: memories, change over time, and conversations with anyone here.
const el=(tag,text,cls)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;};
const pretty=s=>String(s||'').replaceAll('_',' ');
export function refreshConversation(journal){
 const minds=journal.world?.minds,root=journal.body.querySelector('.resident-conversation');if(!minds||!root)return;
 const key=root.dataset.resident,thread=root.querySelector('.resident-thread');
 const rows=minds.exchanges.filter(e=>e.speaker===key||e.listener===key).slice(-10);
 const signature=rows.map(e=>e.id).join(',');
 if(thread.dataset.signature!==signature){
  const atEnd=thread.scrollHeight-thread.scrollTop-thread.clientHeight<60;
  thread.replaceChildren();
  for(const row of rows){
   if(row.listener==='player')thread.append(el('p',`You: ${row.heard}`,'resident-player'));
   const listener=row.listener==='player'?'':` → ${minds.residents.find(r=>r.id===row.listener)?.name||'a friend'}`;
   thread.append(el('p',`${row.name}${listener}: ${row.text}`,'resident-reply'));
  }
  if(!rows.length)thread.append(el('p','A conversation can start with something small. What did you notice today?','resident-empty'));
  thread.dataset.signature=signature;if(atEnd)thread.scrollTop=thread.scrollHeight;
 }
 root.querySelector('.resident-pending').textContent=minds.pending?`${minds.pending} is thinking…`:minds.feedback||'';
 const resident=minds.residents.find(r=>r.id===key);
 root.querySelector('button[type=submit]').disabled=!resident?.present||Boolean(minds.pending);
 const voice=root.querySelector('.resident-voice');
 voice.textContent=minds.voice.source==='local'?'Conversation stays on this Mac.':minds.voice.detail;
}
export function renderMinds(journal,grid){
 const data=journal.world.minds;if(!data?.residents?.length){grid.append(journal.card('A first impression','Personalities begin to unfold as you play.'));return;}
 const chosen=data.residents.find(r=>r.id===journal.selected)||data.residents[0];journal.selected=chosen.id;
 const list=journal.card('The lives around you','Time together leaves a mark. Each resident keeps their own memories, interests and relationships.');list.classList.add('resident-picker');
 for(const r of [...data.residents].sort((a,b)=>Number(b.present)-Number(a.present))){
  const b=el('button',`${r.name} · ${r.present?'here':'away'}`,'pond-action');b.setAttribute('aria-pressed',r.id===chosen.id);b.onclick=()=>{journal.selected=r.id;journal.render(true);};list.append(b);
 }
 grid.append(list);
 const c=journal.card(chosen.name,chosen.present?'Here at the pond.':'Away on their own adventures. Memories will be here when they return.');
 c.classList.add('resident-portrait');
 if(chosen.id==='cheese')journal.preview(c,'cheese','Cheese');
 else if(journal.world.friends.some(f=>f.id===chosen.id)||journal.world.rare_guest?.id===chosen.id)journal.preview(c,'friend',chosen.id);
 c.append(el('p',`${chosen.experiences} experiences learned from`,'resident-caption'));
 for(const trait of chosen.traits){journal.meter(c,pretty(trait.name),trait.value);if(Math.abs(trait.change)>=.004)c.append(el('small',`${trait.change>0?'Growing more':'Growing less'} ${pretty(trait.name)} · ${Math.abs(trait.change*100).toFixed(1)} points since you met`,'resident-growth'));}
 grid.append(c);
 const conversation=journal.card('Pull up a reed','Speak directly to this resident. They remember what you tell them and answer in their own voice.');conversation.classList.add('resident-conversation');conversation.dataset.resident=chosen.id;
 const thread=el('div',undefined,'resident-thread');thread.setAttribute('role','log');thread.setAttribute('aria-label','Conversation with '+chosen.name);thread.setAttribute('aria-live','polite');
 const form=el('form',undefined,'resident-form'),input=el('textarea');input.rows=3;input.maxLength=1000;input.placeholder=`Say something to ${chosen.name}…`;input.setAttribute('aria-label','Message to '+chosen.name);
 journal.mindDrafts??={};input.value=journal.mindDrafts[chosen.id]||'';input.oninput=()=>{journal.mindDrafts[chosen.id]=input.value;};input.disabled=!chosen.present;
 const submit=el('button','Say it','pond-action');submit.type='submit';
 form.onsubmit=e=>{e.preventDefault();const text=input.value.trim();if(!text||submit.disabled)return;window.cheese.input({type:'pond',action:'mind_chat',target:chosen.id,text});journal.mindDrafts[chosen.id]='';input.value='';submit.disabled=true;conversation.querySelector('.resident-pending').textContent=chosen.name+' is listening…';};
 input.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();form.requestSubmit();}});
 form.append(input,submit);conversation.append(thread,form,el('p','','resident-pending'),el('small','','resident-voice'));
 grid.append(conversation);
 const favorites=journal.card('A little more themselves','Their preferences develop through experiences. Encouragement applies to their most recent activity or conversation.');
 for(const interest of chosen.interests)favorites.append(el('p',`${interest.value>.2?'♥':interest.value<-.2?'~':'·'} ${interest.name}`));
 favorites.append(el('h3','A personal intention'),el('p',`${chosen.goal.label} · ${chosen.goal.done}/${chosen.goal.target} good experiences`));
 if(chosen.last_action)favorites.append(el('p',chosen.last_action.note,'pond-note'));
 favorites.append(journal.button('I liked that','mind_encourage',chosen.id,!chosen.present||!chosen.last_action),journal.button('Try a different approach','mind_redirect',chosen.id,!chosen.present||!chosen.last_action));grid.append(favorites);
 const changes=journal.card('How they are changing',chosen.changes.length?'Small moments, lasting impressions.':'Give them time. Growth comes from lived experience.');
 for(const change of [...chosen.changes].reverse())changes.append(el('h3',change.text),el('p',change.reason));
 for(const rel of chosen.relationships){const note=el('div',undefined,'resident-bond');note.append(el('h3',rel.name));journal.meter(note,'Trust',rel.trust);journal.meter(note,'Warmth',rel.warmth);journal.meter(note,'Familiarity',rel.familiarity);if(rel.friction>.04)journal.meter(note,'Unsettled feelings',rel.friction);changes.append(note);}grid.append(changes);
 const memories=journal.card('Things that stayed','Each resident recalls their own experiences. Your words are remembered as things you told them.');
 for(const fact of chosen.facts)memories.append(el('p',fact.text,'resident-keepsake'));
 for(const m of [...chosen.memories].reverse())memories.append(el('p',m.text,'pond-note'));
 grid.append(memories);refreshConversation(journal);
}
