import test from 'node:test';import assert from 'node:assert/strict';
import {TEXTILE_COMPANY,TEXTILE_ROUTINES,TEXTILE_CONTROLS,textilePose,textileGeometry} from '../client/textile-routines.mjs';
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {GUEST_CAST} from '../client/guest-cast.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';import {scene} from './scenes.mjs';
const ages=['hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'];
const actors=[...ages.map(stage=>({stage})),...Object.values(GUEST_CAST).map(g=>({id:g.id,castId:g.id,name:g.name,visitor:true}))];
const items={mat_unroll:'carpet_red',fringe_comb:'persian_rug',lint_brush:'rug',corner_smooth:'tatami_mat',medallion_trace:'persian_rug',young_steps:'carpet_red',night_listen:'woven_grass',moss_pat:'moss_carpet',grass_dew:'grass_patch',grass_tracks:'grass_floor',rubber_drain:'rubber_mat',welcome_wipe:'welcome_mat',reed_sort:'thatch',batting_fluff:'insulation',scrap_fold:'fabric_scrap',weave_tighten:'woven_grass'};
test('18 textile helper jobs keep the owner’s mechanical clock and use distinct contact tracks',()=>{
 assert.equal(Object.keys(TEXTILE_COMPANY).length,18);const signatures=new Set();
 for(const [id,s]of Object.entries(TEXTILE_COMPANY)){
  signatures.add(JSON.stringify(s.track));
  for(const f of [.1,.3,.5,.7,.9]){
   const work={id:s.preview,elapsed:TEXTILE_ROUTINES[s.preview].duration*f,start:{...TEXTILE_CONTROLS,roll:.7}},solo=textilePose(work),lead=textilePose({...work,company:{id,role:'a'}}),partner=textilePose({...work,company:{id,role:'b'}});
   for(const field of Object.keys(TEXTILE_CONTROLS))assert.equal(lead[field],solo[field]);
   for(const field of ['contact','actorU','actorV','tool'])assert.equal(lead[field],solo[field]);
   assert(partner.partner);assert.equal(partner.tool,s.tool);
   const quiet=textilePose({...work,company:{id,role:'b'}},false);
   for(const field of Object.keys(TEXTILE_CONTROLS)){assert.equal(partner[field],solo[field]);assert.equal(quiet[field],solo[field]);}
  }
  for(const [at]of s.events){const p=textilePose({id:s.preview,elapsed:TEXTILE_ROUTINES[s.preview].duration*at,start:TEXTILE_CONTROLS,company:{id,role:'b'}});assert(p.contact>=.9,id+' native contact event meets the surface');}
 }
 assert.equal(signatures.size,18);
});
test('all 48 visitor profiles and hatched ages meet the textile edge without stretching',()=>{
 let cases=0;
 for(const actor of actors)for(const [id,s]of Object.entries(TEXTILE_COMPANY))for(const f of [.2,.4,.6,.8]){
  const item=items[s.preview],routine={id:s.preview,elapsed:TEXTILE_ROUTINES[s.preview].duration*f,start:TEXTILE_CONTROLS,company:{id,role:'b'}};
  const home={...itemSprite(item,0,{pose:{textile:textilePose(routine)}}),x:100,y:70,scale:itemWorldScale(item)};
  const c={...characterSprite({...actor,facing:false,state:'idle',performance:{kind:'textile',routine}},10,actor.visitor),x:110,y:70};
  assert(!c.clipped,(actor.id||actor.stage)+' '+id);assert(c.art.every(r=>/^[ -~]*$/.test(r)));
  const before=JSON.stringify({home,c}),g=textileGeometry(home,{character:c,inside:1,slot:1},6,9);
  assert.equal(before,JSON.stringify({home,c}));assert.equal(g.character.scale,c.scale);assert(g.points.every(p=>Number.isFinite(p.x+p.y)));
  if(c.rig?.species==='butterfly')assert(g.character.y*9<g.ground&&g.points.length===0,'butterflies hover without tools');
  else assert(Math.abs(g.character.y*9-g.ground)<.001,'feet remain supported at the edge');
  if(g.pose.contact===1&&g.pose.tool!=='none'&&c.rig?.species!=='butterfly')assert(Math.hypot(g.tip.x-g.target.x,g.tip.y-g.target.y)<.001,'held tool reaches the real surface');
  if(g.pose.contact===1&&g.pose.tool!=='none'&&c.rig?.species!=='butterfly')assert(Math.abs(g.hand.x-g.target.x)<=4*g.cw,'a helper steps close for a short wing reach');
  cases++;
 }
 assert.equal(cases,4032);
});
test('arrived textile visitors attach only to the selected copy and keep their identity',()=>{
 const work={id:'fringe_comb',elapsed:12,start:TEXTILE_CONTROLS,origin:[60,24]},shared={...work,company:{id:'fringe_pair',role:'b'}};
 const s=scene({items:[{id:'persian_rug',instance:'a',x:60,y:24},{id:'persian_rug',instance:'b',x:90,y:24}],visitor:{id:'friend:frida',castId:'friend:frida',name:'Frida',x:75,y:24,state:'idle'},living:{ecology:{},objects:{},instances:{a:{textile:{}},b:{textile:{}}},plan:{kind:'item',target:'persian_rug',instance:'a',phase:'act',progress:.5,elapsed:10,duration:20,destination:[60,24],textile_work:{...work,company:{id:'fringe_pair',role:'a'}}},minds:{textile_helpers:[{actor:'friend:frida',id:'persian_rug',instance:'a',destination:[60,24],spot:[69,24],phase:'approach',elapsed:0,routine:shared}]}}});
 const w=new LivingWorld();w.render(s,1,.1);assert.equal(w.objects[0].textileUsers.length,1);assert(w.characters.some(c=>c.id==='friend:frida'));
 s.living.minds.textile_helpers[0].phase='inside';w.render(s,2,.1);assert.equal(w.objects[0].textileUsers.length,2);assert(!w.objects[1].textileUsers);assert(!w.characters.some(c=>c.id==='friend:frida'));
 const helper=w.objects[0].textileUsers[1];assert(helper.character.visitor&&helper.character.id==='friend:frida');
 s.living.plan.paused=true;const before=JSON.stringify(s);w.render(s,10,.1);const held=w.objects[0].textileUsers[1].character;w.render(s,100,.1);assert.deepEqual(w.objects[0].textileUsers[1].character.art,held.art);assert.equal(JSON.stringify(s),before);
 s.items[0].instance='replacement';w.render(s,101,.1);assert(!w.objects[0].textileUsers);assert(w.characters.some(c=>c.id==='friend:frida'));
});
