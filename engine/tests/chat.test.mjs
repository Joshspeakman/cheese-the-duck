import test from 'node:test';
import assert from 'node:assert/strict';
import {parseChat,inTab,channelLabel,chatCompletions} from '../client/chat-model.mjs';
import {HudLayout} from '../client/hud-layout.mjs';
const targets=[{id:'cheese',name:'Cheese'},{id:'ada',name:'Ada Feather'},{id:'ada2',name:'Ada Moss'},{id:'moss',name:'Moss'}];
const parse=(text,extra={})=>parseChat(text,{targets,...extra});
test('ordinary conversation and escaped slash remain literal and uncensored',()=>{
 assert.deepEqual(parse('What the fuck, Cheese? <img>'),{kind:'send',text:'What the fuck, Cheese? <img>',target:'cheese',channel:'say'});
 assert.equal(parse('//feed Cheese').text,'/feed Cheese');
 assert.equal(parse('/feed').kind,'error');assert.equal(parse('  ').kind,'empty');
});
test('whispers resolve exact, quoted and unique names and reject ambiguity',()=>{
 for(const text of ['/w Ada Feather hello','/tell "Ada Feather" hello','/WHISPER ada feather hello'])assert.deepEqual(parse(text),{kind:'send',text:'hello',target:'ada',channel:'whisper'});
 assert.equal(parse('/w Ada hello').kind,'error');assert.equal(parse('/w nobody hello').kind,'error');
 assert.equal(parse('/w Moss').kind,'target');assert.equal(parse('/w').kind,'error');
 assert.equal(parse('/r hello',{lastWhisper:'moss'}).target,'moss');
 assert.equal(parse('/r hello',{lastWhisper:'departed'}).kind,'error');
 assert.deepEqual(parse('/s hi',{target:'moss',channel:'whisper'}),{kind:'send',text:'hi',target:'cheese',channel:'say'});
 assert.equal(parse('/help').kind,'help');assert.equal(parse('/clear').kind,'clear');
});
test('channel filters separate speech, nearby conversations and world events',()=>{
 for(const channel of ['say','whisper','neighbors']){assert.ok(inTab({channel},'general'));assert.ok(inTab({channel},'conversation'));assert.ok(!inTab({channel},'world'));}
 for(const channel of ['world','loot'])assert.ok(inTab({channel},'world')&&!inTab({channel},'conversation'));
 assert.equal(channelLabel({channel:'whisper',speaker:'player',target:'ada'},targets),'To Ada Feather');
 assert.equal(channelLabel({channel:'whisper',speaker:'player',target:'ada',targetName:'Ada Feather'},[]),'To Ada Feather');
});
test('Tab completion resolves present listeners without overwriting the message',()=>{
 const choices=chatCompletions('/w Ad',5,targets);
 assert.deepEqual(choices.map(c=>c.label),['Ada Feather','Ada Moss']);
 assert.equal(parse(choices[0].value+'Nice to meet you.').target,'ada');
 assert.equal(parse(choices[1].value+'Nice to meet you.').target,'ada2');
 const caret='/w "Ada F'.length,choice=chatCompletions('/w "Ada F How is your day?',caret,targets)[0];
 assert.equal(choice.value,'/w Ada Feather How is your day?');
 assert.equal(choice.caret,'/w Ada Feather '.length);
 for(const s of ['Hello Moss','/w Absent','/w Moss hello','//w Moss'])assert.deepEqual(chatCompletions(s,s.length,targets),[]);
 assert.equal(chatCompletions('/w ',3,targets).length,targets.length);
 assert.equal(chatCompletions('/he',3,targets)[0].value,'/help ');
 assert.deepEqual(chatCompletions('/s Something important',2,targets),[]);
});
test('chat resize preserves its anchor, persists, and clamps after window changes',()=>{
 const h=new HudLayout(),r=h.rect('chat',1440,1000);h.resize('chat',810,400,1440,1000);
 assert.equal(h.rect('chat',1440,1000).x,r.x);assert.ok(h.rect('chat',1440,1000).y<=r.y);
 const restored=new HudLayout(h.save());assert.equal(restored.rect('chat',1440,1000).w,810);
 restored.resize('chat',999999,999999,500,320);const small=restored.rect('chat',500,320);
 assert.ok(small.x>=8&&small.y>=8&&small.x+small.w<=492&&small.y+small.h<=312);
 restored.resize('chat',NaN,NaN,500,320);assert.ok(Number.isFinite(restored.rect('chat',500,320).w));
});
