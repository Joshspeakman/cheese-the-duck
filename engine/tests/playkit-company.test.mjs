import test from 'node:test';import assert from 'node:assert/strict';
import {PLAYKIT_COMPANY,PLAYKIT_ROUTINES,PLAYKIT_CONTROLS,playkitPose,playkitGeometry} from '../client/playkit-routines.mjs';
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';import {GUEST_CAST} from '../client/guest-cast.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';import {scene} from './scenes.mjs';
const ages=['hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'];
const actors=[...ages.map(stage=>({stage})),...Object.values(GUEST_CAST).map(g=>({id:g.id,castId:g.id,name:g.name,visitor:true}))];
const work=(id,s,f,role='b')=>({id:s.preview,elapsed:PLAYKIT_ROUTINES[s.preview].duration*f,start:PLAYKIT_CONTROLS,duet:id,company:{id,role}});
test('25 toy company tracks share controls without moving mechanisms twice',()=>{
 const seen=new Set();assert.equal(Object.keys(PLAYKIT_COMPANY).length,25);
 for(const [id,s]of Object.entries(PLAYKIT_COMPANY)){
  seen.add(JSON.stringify(s.track));
  for(const f of [.1,.3,.5,.7,.9]){
   const w=work(id,s,f),helper=playkitPose(w),leader=playkitPose({...w,company:{id,role:'a'}}),quiet=playkitPose(w,false);
   assert(helper.partner);assert.equal(helper.tool,s.tool);assert.equal(helper.actorU,quiet.actorU);assert.equal(helper.actorV,quiet.actorV);
   for(const k in PLAYKIT_CONTROLS){assert.equal(helper[k],leader[k]);assert.equal(helper[k],quiet[k]);}
  }
  for(const [at]of s.events)assert.equal(playkitPose(work(id,s,at)).contact,1,id+' event occurs at physical contact');
 }
 assert.equal(seen.size,25);
 for(const id of ['wand_bubbles','rope_count']){const p=playkitPose(work(id,PLAYKIT_COMPANY[id],.5));assert.equal(p.actorJump,0,'watchers do not inherit Cheese’s jumps');}
});
test('every hatched age and all 48 visitors fit their shared toy roles',()=>{
 let cases=0;
 for(const actor of actors)for(const [id,s]of Object.entries(PLAYKIT_COMPANY))for(const f of new Set([.2,.4,.6,.8,...s.events.map(e=>e[0])])){
  const routine=work(id,s,f),home={...itemSprite(s.item,0,{pose:{playkit:playkitPose({...routine,company:{id,role:'a'}})}}),x:100,y:70,scale:itemWorldScale(s.item)};
  const c={...characterSprite({...actor,facing:false,state:'idle',performance:{kind:'playkit',routine}},10,actor.visitor),x:110,y:70},before=JSON.stringify({home,c}),g=playkitGeometry(home,{character:c,inside:1,slot:1},6,9);
  assert(!c.clipped,(actor.id||actor.stage)+' '+id);assert(c.art.every(r=>/^[ -~]*$/.test(r)));assert.equal(before,JSON.stringify({home,c}));assert.equal(g.character.scale,c.scale);assert(g.points.every(p=>Number.isFinite(p.x+p.y)));
  if(c.rig?.species==='butterfly')assert(g.character.y*9<g.ground&&g.points.length===0,'butterflies hover without manipulating a toy');
  else assert(Math.abs(g.character.y*9-g.ground)<.001,'feet stay on the fixed landing');
  if(g.pose.contact===1&&g.pose.tool!=='none'&&c.rig?.species!=='butterfly'){
   assert(Math.hypot(g.tip.x-g.target.x,g.tip.y-g.target.y)<.001,'real contact point');
   assert(Math.abs(g.hand.x-g.target.x)<=4*g.cw,'short horizontal reach '+(actor.id||actor.stage)+' '+id);
   assert(Math.abs(g.hand.y-g.target.y)<=6*g.cw*1.5,'short vertical reach '+(actor.id||actor.stage)+' '+id+' '+Math.abs(g.hand.y-g.target.y)/(g.cw*1.5));
  }
  cases++;
 }
 assert.equal(cases,actors.length*Object.values(PLAYKIT_COMPANY).reduce((n,s)=>n+new Set([.2,.4,.6,.8,...s.events.map(e=>e[0])]).size,0));
});
test('toy helpers arrive independently and retain exact-copy identity and paused poses',()=>{
 const core=work('disc_finish',PLAYKIT_COMPANY.disc_finish,.7,'a'),shared={...core,company:{id:'disc_finish',role:'b'}};
 const s=scene({items:[{id:'frisbee',instance:'a',x:60,y:24},{id:'frisbee',instance:'b',x:90,y:24}],visitor:{id:'friend:frida',castId:'friend:frida',name:'Frida',x:75,y:24,state:'idle'},living:{ecology:{},objects:{},instances:{a:{playkit:{}},b:{playkit:{}}},plan:{kind:'item',target:'frisbee',instance:'a',phase:'act',progress:.5,elapsed:10,duration:20,destination:[60,24],playkit_work:core},minds:{playmates:[{actor:'friend:frida',id:'frisbee',instance:'a',destination:[60,24],spot:[69,24],phase:'approach',elapsed:0,routine:shared}]}}});
 const w=new LivingWorld();w.render(s,1,.1);assert.equal(w.objects[0].players.length,1);assert(w.characters.some(c=>c.id==='friend:frida'));
 s.living.minds.playmates[0].phase='inside';w.render(s,2,.1);assert.equal(w.objects[0].players.length,2);assert(!w.objects[1].players);assert(!w.characters.some(c=>c.id==='friend:frida'));
 const helper=w.objects[0].players[1];assert(helper.character.visitor&&helper.character.id==='friend:frida');
 s.living.plan.paused=true;const before=JSON.stringify(s);w.render(s,10,.1);const held=w.objects[0].players[1].character;w.render(s,100,.1);assert.deepEqual(w.objects[0].players[1].character.art,held.art);assert.equal(JSON.stringify(s),before);
 s.items[0].instance='replacement';w.render(s,101,.1);assert(!w.objects[0].players);assert(w.characters.some(c=>c.id==='friend:frida'));
});
