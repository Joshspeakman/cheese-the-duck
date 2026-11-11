import test from 'node:test';import assert from 'node:assert/strict';
import {GROUND_COMPANY,GROUND_ROUTINES,groundPose,groundGeometry} from '../client/ground-routines.mjs';
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {GUEST_CAST} from '../client/guest-cast.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';import {scene} from './scenes.mjs';
const ages=['hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'];
const actors=[...ages.map(stage=>({stage})),...Object.values(GUEST_CAST).map(g=>({id:g.id,castId:g.id,name:g.name,visitor:true}))];
const work=(id,s,f,role='b')=>({id:s.preview,elapsed:GROUND_ROUTINES[s.preview].duration*f,duet:id,company:{id,role}});
test('27 ground companion roles keep exact native contact points and separate working lanes',()=>{
 assert.equal(Object.keys(GROUND_COMPANY).length,27);const signatures=new Set();
 for(const [id,s]of Object.entries(GROUND_COMPANY)){
  signatures.add(JSON.stringify(s.track));
  for(const f of [.1,.3,.5,.7,.9]){
   const w=work(id,s,f),leader=groundPose({...w,company:{id,role:'a'}}),helper=groundPose(w),quiet=groundPose(w,false);
   assert(helper.partner);assert.equal(helper.tool,s.tool);assert.equal(helper.u,leader.u);assert.equal(helper.v,leader.v);
   for(const key of ['u','v','actorU','actorV','actorPress','contact'])assert.equal(helper[key],quiet[key]);
   if(s.layout==='lanes')assert(leader.u<.5&&helper.actorU>.65,id+' leaves separate lanes');
  }
  for(const [at,event]of s.events){const p=groundPose(work(id,s,at));assert(event==='foot'?p.actorPress>=.9:p.contact>=.9,id+' event is at real contact');}
 }
 assert.equal(signatures.size,27);
 for(let i=0;i<=100;i++){
  const s=GROUND_COMPANY.lava_edge_pair,w=work('lava_edge_pair',s,i/100),a=groundPose({...w,company:{id:'lava_edge_pair',role:'a'}}),b=groundPose(w);
  assert(a.actorV>=1.1&&b.actorV>=1.15,'both lava observers stay outside the lip');
 }
 for(const [f,u,v]of [[.2,.1,.625],[.42,.3,.375],[.64,.1,.625]]){const p=groundPose(work('checker_echo',GROUND_COMPANY.checker_echo,f,'a'));assert(Math.abs(p.u-u)<1e-8&&Math.abs(p.v-v)<1e-8,'paired checker footing remains in actual square centers');}
});
test('all 48 visitor profiles and hatched ages keep fitted bodies through ground activities',()=>{
 let cases=0;
 for(const actor of actors)for(const [id,s]of Object.entries(GROUND_COMPANY))for(const f of [.2,.4,.6,.8]){
  const routine=work(id,s,f),home={...itemSprite(s.item,0,{pose:{ground:groundPose({...routine,company:{id,role:'a'}})}}),x:100,y:70,scale:itemWorldScale(s.item)};
  const c={...characterSprite({...actor,facing:false,state:'idle',performance:{kind:'ground',routine}},10,actor.visitor),x:110,y:70};
  assert(!c.clipped,(actor.id||actor.stage)+' '+id);assert(c.art.every(r=>/^[ -~]*$/.test(r)));
  const before=JSON.stringify({home,c}),g=groundGeometry(home,{character:c,inside:1,slot:1},6,9);
  assert.equal(before,JSON.stringify({home,c}));assert.equal(g.character.scale,c.scale);assert(g.points.every(p=>Number.isFinite(p.x+p.y)));
  if(c.rig?.species==='butterfly')assert(g.character.y*9<g.ground&&g.points.length===0,'flying guests hover without wielding tools');
  else assert(Math.abs(g.character.y*9-g.ground)<.001,'feet remain on the real surface plane');
  if(g.pose.contact===1&&g.pose.tool!=='none'&&c.rig?.species!=='butterfly'){
   assert(Math.hypot(g.tip.x-g.target.x,g.tip.y-g.target.y)<.001,'wing or held tool reaches the native contact');
   assert(Math.abs(g.hand.x-g.target.x)<=4*g.cw,'short reach '+(actor.id||actor.stage)+' '+id+' '+f+' distance '+Math.abs(g.hand.x-g.target.x)/g.cw);
  }
  cases++;
 }
 assert.equal(cases,6048);
});
test('visitor prints and each author’s furrows are visible without changing physical state',()=>{
 const shapes=['webbed','small','talon','toad'],signatures=new Set();
 for(const shape of shapes){const state={ground:{tracks:[{u:.7,v:.7,life:1,shape,by:'guest'}]}},before=JSON.stringify(state);signatures.add(itemSprite('sand_floor',0,{state}).art.join('\n'));assert.equal(JSON.stringify(state),before);}
 assert.equal(signatures.size,4);
 const left={ground:{furrows:[{u0:.258,u1:.45,v:.5,life:1,by:'cheese'}]}},right={ground:{furrows:[{u0:.64,u1:.86,v:.5,life:1,by:'friend'}]}};
 assert.notDeepEqual(itemSprite('sand_floor',0,{state:left}).art,itemSprite('sand_floor',0,{state:right}).art);
 const worn=structuredClone(right);worn.ground.furrows[0].life=.2;
 assert.notDeepEqual(itemSprite('sand_floor',0,{state:right}).art,itemSprite('sand_floor',0,{state:worn}).art,'native weathering softens the raised sand edge');
});
test('arrived surface companions keep their identity and attach only to the actual selected copy',()=>{
 const core=work('sand_rake_pair',GROUND_COMPANY.sand_rake_pair,.4,'a'),shared={...core,company:{id:'sand_rake_pair',role:'b'}};
 const s=scene({items:[{id:'sand_floor',instance:'a',x:60,y:24},{id:'sand_floor',instance:'b',x:90,y:24}],visitor:{id:'friend:frida',castId:'friend:frida',name:'Frida',x:75,y:24,state:'idle'},living:{ecology:{},objects:{},instances:{a:{ground:{}},b:{ground:{}}},plan:{kind:'item',target:'sand_floor',instance:'a',phase:'act',progress:.5,elapsed:10,duration:20,destination:[60,24],ground_work:core},minds:{ground_helpers:[{actor:'friend:frida',id:'sand_floor',instance:'a',destination:[60,24],spot:[69,24],phase:'approach',elapsed:0,routine:shared}]}}});
 const w=new LivingWorld();w.render(s,1,.1);assert.equal(w.objects[0].groundUsers.length,1);assert(w.characters.some(c=>c.id==='friend:frida'));
 s.living.minds.ground_helpers[0].phase='inside';w.render(s,2,.1);assert.equal(w.objects[0].groundUsers.length,2);assert(!w.objects[1].groundUsers);assert(!w.characters.some(c=>c.id==='friend:frida'));
 const helper=w.objects[0].groundUsers[1];assert(helper.character.visitor&&helper.character.id==='friend:frida');
 s.living.plan.paused=true;const before=JSON.stringify(s);w.render(s,10,.1);const held=w.objects[0].groundUsers[1].character;w.render(s,100,.1);assert.deepEqual(w.objects[0].groundUsers[1].character.art,held.art);assert.equal(JSON.stringify(s),before);
 s.items[0].instance='replacement';w.render(s,101,.1);assert(!w.objects[0].groundUsers);assert(w.characters.some(c=>c.id==='friend:frida'));
});
