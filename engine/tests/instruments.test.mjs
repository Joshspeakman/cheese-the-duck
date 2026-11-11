import test from 'node:test';
import assert from 'node:assert/strict';
import {MUSIC_SCORES,musicNotes,musicPose,musicGeometry} from '../client/music-performances.mjs';
import {INSTRUMENT_BLUEPRINTS as B} from '../client/instrument-workshop.mjs';
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {DUCK_AGES} from '../client/duck-rig.mjs';
import {GUEST_CAST} from '../client/guest-cast.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
const cast=[...DUCK_AGES.slice(1).map(a=>({stage:a.id})),...Object.values(GUEST_CAST).map(g=>({id:g.id,castId:g.id,name:g.name,visitor:true}))];
test('nine instruments expose real bounded contact surfaces and keep complete ASCII masks',()=>{
 assert.equal(Object.keys(B).length,9);
 for(const [item,s]of Object.entries(B))for(const time of [0,1,3,6,13]){
  const model=itemSprite(item,time,{state:{wetness:.8,dirt:.7,condition:.3},context:{living:{ecology:{wind:.9}}}});
  assert.equal(model.construction,'instrument-v1');assert.equal(model.kind,'music');assert(!model.clipped,item);
  assert.equal(model.width,s.w);assert.equal(model.art.length,s.h);assert.equal(itemWorldScale(item),s.scale);
  assert(model.art.every((row,i)=>/^[ -~]*$/.test(row)&&row.length===model.tones[i].length));
  for(const f of model.fills)assert(f.x>=0&&f.y>=0&&f.x+f.w<=model.width&&f.y<model.art.length,item+' fill overflow');
  for(const key of model.anchors.keys)assert(key.x>=0&&key.y>=0&&key.x<model.width&&key.y<model.art.length);
  assert.deepEqual(itemSprite(item,0,{motion:false}),itemSprite(item,999,{motion:false}));
 }
});
test('25 authored phrases press only their currently sounding keys and freeze deterministically',()=>{
 assert.equal(Object.keys(MUSIC_SCORES).length,25);const phrases=new Set();
 for(const [id,s]of Object.entries(MUSIC_SCORES)){
  phrases.add(JSON.stringify(s.notes));assert(s.notes.every((n,i)=>!i||n[0]>=s.notes[i-1][0]));
  for(const [item,p]of Object.entries(B).filter(([,p])=>s.types.includes(p.type))){
   for(const role of s.shared?['a','b']:['']){
    const routine={id,elapsed:0,role},notes=musicNotes(item,routine);
    for(const n of notes){
     const pose=musicPose(item,{...routine,elapsed:n.at+.1});
     assert(pose.hits.some(h=>h.index===n.index),item+' '+id+' missing sounding note');
     assert(pose.hits.every(h=>h.press>=0&&h.press<=1&&pose.time>=h.at&&pose.time<h.at+h.hold));
    }
    assert.deepEqual(musicPose(item,{...routine,elapsed:0},false),musicPose(item,{...routine,elapsed:900},false));
    assert.equal(musicPose(item,{...routine,interrupted:true}),null);
   }
  }
 }
 assert.equal(phrases.size,25);
});
test('playing changes the actual instrument mechanism rather than only the character',()=>{
 const samples={toy_piano:'first_keys',piano:'pond_waltz',drums:'drum_steps',toy_trumpet:'horn_breath',toy_boombox:'cassette_side_a',nook_radio:'evening_station',wind_chimes:'tube_taps',shell_mobile:'shell_ripple',fog_bell:'fog_answer'};
 for(const [item,id]of Object.entries(samples)){
  const note=musicNotes(item,{id})[0],pose=musicPose(item,{id,elapsed:note.at+.12});
  const playing=itemSprite(item,0,{pose:{music:[pose]}}),silent=itemSprite(item,0);
  assert.notDeepEqual(playing.art,silent.art,item);
  if(B[item].type==='piano')assert(playing.anchors.keys[note.key].y>silent.anchors.keys[note.key].y,'the touched key physically depresses');
 }
});
test('all hatched ages and 48 guests retain scale and supported contact through music poses',()=>{
 let cases=0;
 for(const [item,p]of Object.entries(B))for(const [id,s]of Object.entries(MUSIC_SCORES).filter(([,s])=>s.types.includes(p.type)))for(const duck of cast)for(const facing of [true,false]){
  const scales=new Set();
  for(const f of [.1,.3,.6,.9]){
   const routine={id,elapsed:s.duration*f,role:s.shared?(facing?'a':'b'):''};
   const pose=musicPose(item,routine),home={...itemSprite(item,0,{pose:{music:[pose]}}),scale:itemWorldScale(item),x:100,y:70};
   const c={...characterSprite({...duck,facing,state:'idle',performance:{kind:'instrument',item,routine}},100,duck.visitor),x:88,y:70};
   assert(!c.clipped,JSON.stringify({item,id,duck,f}));scales.add(c.scale);
   if(c.identity?.species!=='butterfly')assert(c.grip&&c.bill&&c.art[Math.round(c.grip.y)][Math.round(c.grip.x)]!==' '&&c.art[Math.round(c.bill.y)][Math.round(c.bill.x)]!==' ',duck.id||duck.stage);
   const frozen=JSON.stringify({c,home}),g=musicGeometry(home,{character:c,inside:1,slot:facing?0:1},6,9);
   assert.equal(JSON.stringify({c,home}),frozen);assert.equal(g.character.scale,c.scale);
   for(const point of [...g.points,g.hand,...g.targets])assert(Number.isFinite(point.x)&&Number.isFinite(point.y));
   if(g.stool)assert(Math.abs(g.character.y*9-g.stool.top)<.001);
   for(const contact of g.contacts){
    assert(contact.distance<35,JSON.stringify({item,id,who:duck.id||duck.stage,facing,f,distance:contact.distance}));
    if(contact.press>.1&&pose.type!=='radio'&&pose.gesture!=='brush')assert.deepEqual(contact.tip,{x:contact.x,y:contact.y});
   }
   if(p.type==='horn'&&c.bill){
    const cw=c.scale*6,hh=cw*1.5,unit=home.scale*home.detailScale*6;
    const x=Math.round(g.character.x*6-c.anchorX*cw)+(c.bill.x+.5)*cw;
    const y=Math.round(g.character.y*9-c.groundRow*hh)+(c.bill.y+.5)*hh;
    assert(Math.abs(x-(home.x*6-home.width*unit/2+(home.anchors.mouth.x+.5)*unit))<=.51);
    assert(Math.abs(y-(home.y*9-home.art.length*unit*1.5+(home.anchors.mouth.y+.5)*unit*1.5))<=.51);
   }
   cases++;
  }
  assert.equal(scales.size,1);
 }
 assert.equal(cases,20160);
});
function scene(){return {biome:'pond',location:'Home Pond',season:'spring',hour:12,weather:'sunny',motion:true,
 camera:{x:0,y:0,w:132,h:42},duck:{x:60,y:24,stage:'hatchling',state:'idle',cosmetics:{}},items:[{id:'toy_piano',x:60,y:24},{id:'toy_piano',x:90,y:24}],structures:[],
 living:{ecology:{insects:0},plan:{kind:'item',target:'toy_piano',instrument:{slot:0},phase:'act',duration:30,elapsed:15,destination:[60,24],music_score:{id:'first_keys',elapsed:2.2}},objects:{toy_piano:{}},minds:{musicians:[]}}};}
test('music follows the played physical copy, real visitor arrivals and paused clocks',()=>{
 const w=new LivingWorld(),s=scene(),original=JSON.stringify(s);w.render(s,100,.1);assert.equal(JSON.stringify(s),original);
 assert.equal(w.objects.filter(o=>o.musicians).length,1);assert(!w.characters.some(c=>c.cheese));
 assert(w.objects[0].active);assert(!w.objects[1].active);
 s.living.plan.paused=true;w.render(s,101,.1);assert(w.objects.every(o=>!o.musicians&&!o.active));assert(w.characters.some(c=>c.cheese));
 s.living.plan=null;s.visitor={id:'friend:frida',castId:'friend:frida',name:'Frida',x:59,y:24,state:'idle'};
 s.living.minds.musicians=[{actor:'friend:frida',id:'toy_piano',destination:[60,24],slot:0,phase:'approach',elapsed:0,score:{id:'first_keys',elapsed:0}}];
 w.render(s,103,.1);assert(w.objects.every(o=>!o.musicians));
 s.living.minds.musicians[0].phase='inside';w.render(s,104,.1);assert.equal(w.objects[0].musicians[0].character.id,'friend:frida');assert(!w.characters.some(c=>c.id==='friend:frida'));
 s.living.minds.musicians[0].destination=[10,24];w.render(s,105,.1);assert(w.objects.every(o=>!o.musicians));
});

test('players cross between notes continuously instead of jumping when the active hand changes',()=>{
 for(const [item,p]of Object.entries(B))for(const [id,s]of Object.entries(MUSIC_SCORES).filter(([,s])=>s.types.includes(p.type)))for(const role of s.shared?['a','b']:['']){
  for(const note of musicNotes(item,{id,role})){
   const poses=[-.0001,.0001].map(delta=>{
    const routine={id,role,elapsed:note.at+delta},pose=musicPose(item,routine);
    const home={...itemSprite(item,0,{pose:{music:[pose]}}),scale:itemWorldScale(item),x:100,y:70};
    const c={...characterSprite({stage:'adult',facing:role!=='b',performance:{kind:'instrument',item,routine}},0),x:88,y:70};
    return musicGeometry(home,{character:c,inside:1,slot:role==='b'?1:0},6,9).character;
   });
   const [a,b]=poses;
   assert(Math.hypot((b.x-a.x)*6,(b.y-a.y)*9)<=a.scale*6*2+1,JSON.stringify({item,id,at:note.at,a:[a.x,a.y],b:[b.x,b.y]}));
  }
 }
});
