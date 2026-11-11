import test from 'node:test';import assert from 'node:assert/strict';
import {CREATIVE_COMPANY,CREATIVE_ROUTINES,creativePose,creativeGeometry} from '../client/creative-routines.mjs';
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {GUEST_CAST} from '../client/guest-cast.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';import {scene} from './scenes.mjs';
const ages=['hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'];
const coreFor=id=>id.startsWith('scope')?'scope_focus':id.startsWith('paint')?'paint_ducks':id==='kite_tail_partner'?'kite_tail':id.startsWith('kite')?'kite_launch':'fold_wings';
const itemFor=id=>({scope:'telescope',easel:'easel',kite:'kite',fold:'paper_plane_design'})[CREATIVE_ROUTINES[id].type];
const actors=[...ages.map(stage=>({stage})),...Object.values(GUEST_CAST).map(g=>({id:g.id,castId:g.id,name:g.name,visitor:true}))];
test('13 shared creative scores use distinct partner jobs without duplicating object mechanics',()=>{
 assert.equal(Object.keys(CREATIVE_COMPANY).length,13);
 const signatures=new Set();
 for(const [id,s]of Object.entries(CREATIVE_COMPANY)){
  signatures.add(JSON.stringify(s.track));
  for(const f of [.1,.3,.5,.7,.9]){
   const core=coreFor(id),work={id:core,elapsed:CREATIVE_ROUTINES[core].duration*f,start:{fold:.3}},solo=creativePose(work),lead=creativePose({...work,company:{id,role:'a'}}),partner=creativePose({...work,company:{id,role:'b'}});
   for(const field of ['aim','focus','cap','fold','flight','cover','contact','anchorA','anchorB','anchorBlend'])assert.deepEqual(lead[field],solo[field],'the original operator owns '+field);
   assert(partner.partner);assert(s.tool===partner.tool);
   const quiet=creativePose({...work,company:{id,role:'b'}},false);for(const field of ['aim','focus','cap','fold','flight','cover'])assert.equal(quiet[field],solo[field]);
  }
 }
 assert.equal(signatures.size,13);
});
test('every hatched age and all 48 visitors fit shared creative company without stretching or floating',()=>{
 let cases=0;
 for(const actor of actors)for(const [id,s]of Object.entries(CREATIVE_COMPANY))for(const f of [.2,.4,.6,.8]){
  const core=coreFor(id),item=itemFor(core),routine={id:core,elapsed:CREATIVE_ROUTINES[core].duration*f,start:{fold:0},company:{id,role:'b'}};
  const home={...itemSprite(item,0,{pose:{creative:creativePose(routine)}}),x:100,y:70,scale:itemWorldScale(item)};
  const c={...characterSprite({...actor,facing:false,state:'idle',performance:{kind:'creative',routine}},10,actor.visitor),x:110,y:70};
  assert(!c.clipped,(actor.id||actor.stage)+' '+id);assert(c.art.every(r=>/^[ -~]*$/.test(r)));
  const before=JSON.stringify({home,c}),posed=creativeGeometry(home,{character:c,inside:1,slot:1},6,9);
  assert.equal(before,JSON.stringify({home,c}));assert.equal(posed.character.scale,c.scale);
  assert(posed.points.every(p=>Number.isFinite(p.x+p.y)));
  if(c.rig?.species==='butterfly')assert(posed.character.y*9<posed.ground&&posed.points.length===0,'a butterfly hovers without a tool');
  else assert(Math.abs(posed.character.y*9-posed.ground)<.001,'feet stay at ground level');
  if(posed.pose.contact===1&&posed.pose.tool!=='none'&&c.rig?.species!=='butterfly')assert(Math.hypot(posed.tip.x-posed.target.x,posed.tip.y-posed.target.y)<.001,'hand ends on the object');
  if(posed.tip)assert(posed.tip.x<posed.hand.x,'a right-hand creator reaches toward the shared prop');
  cases++;
 }
 assert.equal(cases,(8+48)*13*4);
});
test('arrived creators attach to the exact copy and remain selectable independently of Cheese',()=>{
 const work={id:'paint_sky',elapsed:12,start:{},origin:[60,24]},shared={...work,company:{id:'paint_proud',role:'b'}};
 const s=scene({items:[{id:'easel',instance:'a',x:60,y:24},{id:'easel',instance:'b',x:90,y:24}],
  visitor:{id:'friend:frida',castId:'friend:frida',name:'Frida',x:75,y:24,state:'idle'},
  living:{ecology:{},objects:{},instances:{a:{creative:{strokes:1}},b:{creative:{strokes:0}}},
   plan:{kind:'item',target:'easel',instance:'a',phase:'act',progress:.5,elapsed:10,duration:20,destination:[60,24],creative_work:{...work,company:{id:'paint_proud',role:'a'}}},
   minds:{creators:[{actor:'friend:frida',id:'easel',instance:'a',destination:[60,24],spot:[69,24],phase:'approach',elapsed:0,routine:shared}]}}});
 const w=new LivingWorld();w.render(s,1,.1);assert.equal(w.objects[0].creators.length,1);assert(w.characters.some(c=>c.id==='friend:frida'));
 s.living.minds.creators[0].phase='inside';w.render(s,2,.1);assert.equal(w.objects[0].creators.length,2);assert(!w.objects[1].creators);assert(!w.characters.some(c=>c.id==='friend:frida'));
 const creator=w.objects[0].creators[1];assert(creator.character.visitor&&creator.character.id==='friend:frida');
 const state=JSON.stringify(s);s.living.plan.paused=true;w.render(s,10,.1);const held=w.objects[0].creators[1].character;w.render(s,100,.1);assert.deepEqual(w.objects[0].creators[1].character.art,held.art);
 assert.equal(JSON.stringify({...s,living:{...s.living,plan:{...s.living.plan,paused:undefined}}}),state);
 s.items[0].instance='replacement';w.render(s,101,.1);assert(!w.objects[0].creators);assert(w.characters.some(c=>c.id==='friend:frida'));
});
