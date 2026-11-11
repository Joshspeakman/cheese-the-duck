import test from 'node:test';
import assert from 'node:assert/strict';
import {LIGHTING_BLUEPRINTS} from '../client/lighting-workshop.mjs';
import {itemSprite,itemWorldScale,itemProfile,itemFamily,catalog} from '../client/ultra-items.mjs';
import {lightOutput,objectLightSources} from '../client/lighting-state.mjs';
import {LIGHTING_ROUTINES,lightingGeometry,lightingPose} from '../client/lighting-routines.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
import {scene} from './scenes.mjs';
import {createRequire} from 'node:module';
const {pondCommand}=createRequire(import.meta.url)('../pond-command.cjs');
const ages=['egg','hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'];

test('27 reconstructed lights stay inside their measured silhouettes across weather and operation',()=>{
 const signatures=new Set();
 for(const id of Object.keys(LIGHTING_BLUEPRINTS)){
  for(const time of [0,1.3,5,19])for(const level of [0,.2,1]){
   const opts={state:{lighting:{level,mode:level?'on':'off'},wetness:.8,dirt:.8,condition:.3},context:{hour:23,living:{ecology:{wind:1}}}};
   const before=JSON.stringify(opts),m=itemSprite(id,time,opts);
   assert.equal(m.construction,'lighting-v1');assert.equal(m.clipped,false,id);
   assert(m.art.every((r,y)=>r.length===m.width&&m.tones[y].length===m.width&&/^[ -~]*$/.test(r)));
   assert(m.fills.every(f=>Number.isFinite(f.x+f.y+f.w)&&f.x>=0&&f.y>=0&&f.x+f.w<=m.width&&f.y<m.art.length),id+' surface bounds');
   assert(m.lightSources.every(s=>s.x>=0&&s.x<m.width&&s.y>=0&&s.y<m.art.length&&s.power>=0&&s.power<=1),id+' source bounds');
   if(!level)assert.equal(m.lightSources.length,0,id+' off does not bloom');
   assert.equal(JSON.stringify(opts),before,'drawing does not change a setting');assert(m.anchors.contact&&m.anchors.entry);
  }
  signatures.add(itemSprite(id,2).art.join('\n'));assert(itemWorldScale(id)>.6);
  assert.equal(itemProfile(catalog.find(i=>i.id===id),itemFamily(id)).kind,'light');
  const options={motion:false,state:{lighting:{level:1}},context:{living:{ecology:{wind:1}}}};
  assert.deepEqual(itemSprite(id,0,options),itemSprite(id,500,options),id+' reduced motion');
 }
 assert.equal(signatures.size,27,'each item has a distinct construction');
});
test('dusk, switches and exposed flames change actual output; fixed lights keep their nature',()=>{
 assert.equal(lightOutput('table_lamp',{}, {hour:12}),0);assert.equal(lightOutput('table_lamp',{}, {hour:21}),1);
 assert.equal(lightOutput('table_lamp',{lighting:{mode:'on'}},{hour:12}),1);
 assert.equal(lightOutput('table_lamp',{lighting:{mode:'off'}},{hour:21}),0);
 assert.equal(lightOutput('eternal_flame',{lighting:{mode:'off'}},{hour:12,weather:'stormy'}),1);
 assert(lightOutput('torch',{lighting:{mode:'on'}},{weather:'rain',intensity:1})<.1);
 assert.equal(lightOutput('fairy_lamp',{lighting:{mode:'on'}},{weather:'rain',intensity:1}),1,'glass protects the fake fireflies');
 assert.equal(lightOutput('firefly_swarm',{lighting:{mode:'on'}},{hour:12}),0,'wild insects are not remote controlled');
 assert.equal(lightOutput('firefly_swarm',{}, {hour:21,season:'winter'}),.12);
 assert.equal(lightOutput('lamp',{lighting:{level:.25,mode:'off'}},{hour:12}),.25,'native transition state wins over preview inference');
});
test('light mechanisms follow native contact and warm only their own luminous materials',()=>{
 const still={state:{lighting:{level:1,mode:'on'}}},rest=itemSprite('table_lamp',0,still);
 assert.deepEqual(rest.art,itemSprite('table_lamp',12,still).art,'a stationary lamp does not work itself from a timer');
 const tug={...still,pose:{light:{contact:1,pull:2}}};
 assert.notDeepEqual(rest.art,itemSprite('table_lamp',0,tug).art,'the actual pull moves its hanging chain');
 const off=itemSprite('table_lamp',0,{state:{lighting:{level:0,mode:'off'}}});
 assert.notEqual(rest.panels.c,off.panels.c,'cloth glows locally');assert.equal(rest.panels.g,off.panels.g,'glazed ceramic stays a solid material');
 assert.equal(rest.panels.b,off.panels.b,'the wood base is not bleached by the bulb');
 const flame=itemSprite('campfire',2,still),eternal=itemSprite('eternal_flame',2,still);
 assert.notEqual(flame.panels.p,eternal.panels.p,'wood fire and the blue eternal flame retain different colors');
});
test('light pools match the exact scaled bulb position and remain restrained by day',()=>{
 const m={...itemSprite('table_lamp',0,{state:{lighting:{level:1}}}),item:true,x:100,y:80,scale:.4};
 for(const [sx,sy] of [[6,8],[4,10],[8,5]]){
  const n=objectLightSources(m,sx,sy,true),d=objectLightSources(m,sx,sy,false),unit=sx*m.scale*m.detailScale;
  const s=m.lightSources[0];assert(Math.abs(n[0].x-(m.x-m.width*unit/(2*sx)+(s.x+.5)*unit/sx))<1e-9);
  assert(Math.abs(n[0].y-(m.y-m.art.length*unit*1.5/sy+(s.y+.5)*unit*1.5/sy))<1e-9);
  assert(d[0].power<n[0].power*.21&&d[0].power<.05,'daylight leaves fine ink visible');
 }
 assert.deepEqual(objectLightSources({...m,lightSources:[]},6,8,true),[]);
});
test('control tools meet physical anchors while all Cheese ages keep their feet grounded',()=>{
 for(const age of ages)for(const [id,spec] of Object.entries(LIGHTING_ROUTINES)){
  const elapsed=spec.duration*.4,routine={id,elapsed},home={...itemSprite('table_lamp',0),scale:.76,x:110,y:85};
  const character={...characterSprite({stage:age,state:'idle',facing:true,performance:{kind:'lighting',routine,motion:true}},2),x:100,y:85};
  const staged=lightingGeometry(home,{character,inside:1},6,8);
  assert(Math.abs(staged.character.y*8-staged.ground)<1e-9,age+' grounded');
  assert(staged.points.every(p=>Number.isFinite(p.x+p.y)),id+' finite held tools');
  if(!spec.observe&&lightingPose(routine).contact===1)assert(Math.hypot(staged.tip.x-staged.target.x,staged.tip.y-staged.target.y)<1e-9,id+' makes contact');
 }
});
test('production IPC preserves selected physical copy and layout coordinates',()=>{
 const raw={type:'pond',action:'lighting_mode',target:'lamp',text:'off',instance:'copy-b',secret:'not-forwarded'};
 assert.deepEqual(pondCommand(raw),{type:'pond',action:'lighting_mode',target:'lamp',text:'off',instance:'copy-b'});
 assert.deepEqual(pondCommand({type:'pond',action:'layout_place',target:'lamp',instance:'copy-b',x:14,y:9}),{type:'pond',action:'layout_place',target:'lamp',instance:'copy-b',x:14,y:9,text:''});
 for(const data of [{instance:{}},{instance:'x'.repeat(129)},{x:NaN},{y:Infinity},{x:'14'},{target:12}])assert.equal(pondCommand({...raw,...data}),null);
});
test('a held light action stays with its exact lamp and freezes its pose when paused',()=>{
 const s=scene({items:[{id:'table_lamp',instance:'a',x:60,y:24},{id:'table_lamp',instance:'b',x:90,y:24}],living:{ecology:{insects:0},instances:{a:{lighting:{level:1}},b:{lighting:{level:0}}},objects:{},plan:{kind:'item',target:'table_lamp',instance:'a',phase:'act',progress:.5,duration:16,elapsed:8,destination:[60,24],light_work:{id:'pull_chain',elapsed:5.5}}}});
 const world=new LivingWorld(),before=JSON.stringify(s);world.render(s,0,.1);
 assert.equal(JSON.stringify(s),before);assert.equal(world.objects[0].lightWorkers.length,1);assert(!world.objects[1].lightWorkers);assert.equal(world.objects[1].lightSources.length,0);
 const held=world.objects[0].lightWorkers[0].character,chain=world.objects[0].art;
 s.living.plan.paused=true;world.render(s,30,.1);
 assert.deepEqual(world.objects[0].lightWorkers[0].character,held,'pause does not unstow Cheese or jump his tool');assert.deepEqual(world.objects[0].art,chain,'the chain stays where his grip holds it');
 s.items[0].instance='replacement';world.render(s,31,.1);
 assert(!world.objects[0].lightWorkers);assert(world.characters.some(c=>c.cheese),'same-position replacement releases the visual performance');
});
