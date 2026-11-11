// Chat commands never become gameplay commands. Ordinary text is always dialogue.
export const CHAT_TABS=[['general','General'],['conversation','Conversations'],['world','World']];
export const spoken=row=>['say','whisper','neighbors'].includes(row.channel);
export const inTab=(row,tab)=>tab==='general'||(tab==='conversation'?spoken(row):!spoken(row));
const COMMANDS=['/say','/whisper','/reply','/help','/clear'];
// Completion only edits the prefix before the caret. Never consume message text.
export function chatCompletions(value,caret,targets=[]){
 const prefix=value.slice(0,caret),suffix=value.slice(caret);
 if(/^\/\w*$/.test(prefix)&&!suffix.trim())return COMMANDS.filter(c=>c.startsWith(prefix.toLowerCase())).map(c=>({value:c+' ',caret:c.length+1,label:c}));
 const whisper=prefix.match(/^\/(?:w|whisper|tell)\s+(.*)$/i);
 if(!whisper)return [];
 const query=whisper[1].replace(/^"/,'').replace(/"$/,'').toLocaleLowerCase();
 return targets.filter(t=>t.name.toLocaleLowerCase().startsWith(query)).map(t=>{
  const head='/w '+t.name+' ',tail=suffix.replace(/^\s+/, '');
  return {value:head+tail,caret:head.length,label:t.name};
 });
}
export function parseChat(value,{target='cheese',channel='say',targets=[],lastWhisper=null}={}){
 const text=value.trim();if(!text)return {kind:'empty'};
 const send=(text,target,channel)=>({kind:text?'send':'target',text,target,channel});
 if(text.startsWith('//'))return send(text.slice(1),target,channel);
 if(!text.startsWith('/'))return send(text,target,channel);
 const [,verb,body='']=text.match(/^\/(\S+)\s*([\s\S]*)$/)||[];
 switch(verb?.toLowerCase()){
  case 's':case 'say':return send(body,'cheese','say');
  case 'w':case 'whisper':case 'tell':{
   const input=body.replace(/^"([^"]+)"(?=\s|$)/,'$1'),lower=input.toLocaleLowerCase();
   const named=targets.filter(t=>lower===t.name.toLocaleLowerCase()||lower.startsWith(t.name.toLocaleLowerCase()+' ')).sort((a,b)=>b.name.length-a.name.length);
   if(named.length){const t=named[0];return send(input.slice(t.name.length).trim(),t.id,'whisper');}
   const [first,...rest]=input.split(/\s+/),matches=targets.filter(t=>t.name.split(' ')[0].toLocaleLowerCase()===first.toLocaleLowerCase());
   if(matches.length===1)return send(rest.join(' '),matches[0].id,'whisper');
   return {kind:'error',message:matches.length>1?'Use their full name so the right friend hears you.':'Whisper to someone here: /w Name your message. Click a speaker’s name to choose them.'};
  }
  case 'r':case 'reply':return lastWhisper&&targets.some(t=>t.id===lastWhisper)?send(body,lastWhisper,'whisper'):{kind:'error',message:'No whisper to reply to from someone who is here.'};
  case 'help':return {kind:'help'};
  case 'clear':return {kind:'clear'};
  default:return {kind:'error',message:'Unknown chat command. /s say · /w Name whisper · /r reply · /help. Start with // to say a literal slash.'};
 }
}
export function channelLabel(row,targets=[]){
 if(row.channel==='whisper')return row.speaker==='player'?`To ${row.targetName||targets.find(t=>t.id===row.target)?.name||row.target}`:'Whisper';
 return row.channel==='neighbors'?'Nearby':row.channel==='say'?'Say':row.channel==='loot'?'Discovery':'World';
}
