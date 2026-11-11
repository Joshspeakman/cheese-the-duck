import test from 'node:test';import assert from 'node:assert/strict';
import {KEEPSAKE_COMPANY,KEEPSAKE_ROUTINES,keepsakePose,keepsakeGeometry} from '../client/keepsake-routines.mjs';
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {GUEST_CAST} from '../client/guest-cast.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';import {scene} from './scenes.mjs';
const ages=['hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'];
const actors=[...ages.map(stage=>({stage})),...Object.values(GUEST_CAST).map(g=>({id:g.id,castId:g.id,name:g.name,visitor:true}))];
test('15 shared reading scores use distinct partner jobs without duplicating object mechanics',()=>{
 assert.equal(Object.keys(KEEPSAKE_COMPANY).length,15);
 const signatures=new Set();
 for(const [id,s]of Object.entries(KEEPSAKE_COMPANY)){
  signatures.add(JSON.stringify(s.track));
  for(const f of [.1,.3,.5,.7,.9]){
   const work={id:'book_leaf',elapsed:36*f,start_open:.3},solo=keepsakePose(work),lead=keepsakePose({...work,company:{id,role:'a'}}),partner=keepsakePose({...work,company:{id,role:'b'}});
   for(const field of ['open','contact','turn','anchorA','anchorB','anchorBlend'])assert.deepEqual(lead[field],solo[field],'the original operator owns '+field);
   assert(partner.reader);assert(s.tool===partner.tool);
   assert.deepEqual(keepsakePose({...work,company:{id,role:'b'}},false),keepsakePose({...work,elapsed:500,company:{id,role:'b'}},false));
  }
 }
 assert.equal(signatures.size,15);
});
test('every hatched age and all 48 visitors fit shared reading without stretching or floating',()=>{
 let cases=0;
 for(const actor of actors)for(const [id,s]of Object.entries(KEEPSAKE_COMPANY))for(const f of [.2,.4,.6,.8]){
  const routine={id:'book_leaf',elapsed:36*f,start_open:0,company:{id,role:'b'}};
  const home={...itemSprite('ancient_tome',0,{pose:{keepsake:keepsakePose(routine)}}),x:100,y:70,scale:itemWorldScale('ancient_tome')};
  const c={...characterSprite({...actor,facing:false,state:'idle',performance:{kind:'keepsake',routine}},10,actor.visitor),x:110,y:70};
  assert(!c.clipped,(actor.id||actor.stage)+' '+id);assert(c.art.every(r=>/^[ -~]*$/.test(r)));
  const before=JSON.stringify({home,c}),posed=keepsakeGeometry(home,{character:c,inside:1,slot:1},6,9);
  assert.equal(before,JSON.stringify({home,c}));assert.equal(posed.character.scale,c.scale);
  assert(posed.points.every(p=>Number.isFinite(p.x+p.y)));
  if(c.rig?.species==='butterfly')assert(posed.character.y*9<posed.ground&&posed.points.length===0,'a butterfly hovers without a tool');
  else assert(Math.abs(posed.character.y*9-posed.ground)<.001,'feet stay at ground level');
  if(posed.pose.contact===1&&posed.pose.tool!=='none'&&c.rig?.species!=='butterfly')assert(Math.hypot(posed.tip.x-posed.target.x,posed.tip.y-posed.target.y)<.001,'pointer ends on the object');
  if(posed.tip)assert(posed.tip.x<posed.hand.x,'a right-hand reader raises the pointer toward the page');
  cases++;
 }
 assert.equal(cases,(8+48)*15*4);
});
test('arrived readers attach to the exact copy and remain selectable independently of Cheese',()=>{
 const work={id:'coin_inspection',elapsed:12,start_open:0,origin:[60,24]},shared={...work,company:{id:'count_the_shine',role:'b'}};
 const s=scene({items:[{id:'treasure_chest',instance:'a',x:60,y:24},{id:'treasure_chest',instance:'b',x:90,y:24}],
  visitor:{id:'friend:frida',castId:'friend:frida',name:'Frida',x:75,y:24,state:'idle'},
  living:{ecology:{},objects:{},instances:{a:{keepsake:{open:1}},b:{keepsake:{open:0}}},
   plan:{kind:'item',target:'treasure_chest',instance:'a',phase:'act',progress:.5,elapsed:10,duration:20,destination:[60,24],keepsake_work:{...work,company:{id:'count_the_shine',role:'a'}}},
   minds:{readers:[{actor:'friend:frida',id:'treasure_chest',instance:'a',destination:[60,24],spot:[69,24],phase:'approach',elapsed:0,routine:shared}]}}});
 const w=new LivingWorld();w.render(s,1,.1);assert.equal(w.objects[0].keepers.length,1);assert(w.characters.some(c=>c.id==='friend:frida'));
 s.living.minds.readers[0].phase='inside';w.render(s,2,.1);assert.equal(w.objects[0].keepers.length,2);assert(!w.objects[1].keepers);assert(!w.characters.some(c=>c.id==='friend:frida'));
 const reader=w.objects[0].keepers[1];assert(reader.character.visitor&&reader.character.id==='friend:frida');
 const state=JSON.stringify(s);s.living.plan.paused=true;w.render(s,10,.1);const held=w.objects[0].keepers[1].character;w.render(s,100,.1);assert.deepEqual(w.objects[0].keepers[1].character.art,held.art);
 assert.equal(JSON.stringify({...s,living:{...s.living,plan:{...s.living.plan,paused:undefined}}}),state);
 s.items[0].instance='replacement';w.render(s,101,.1);assert(!w.objects[0].keepers);assert(w.characters.some(c=>c.id==='friend:frida'));
});
