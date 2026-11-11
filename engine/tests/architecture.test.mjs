import test from 'node:test';import assert from 'node:assert/strict';
import {itemSprite,itemWorldScale,itemProfile} from '../client/ultra-items.mjs';
import {ARCHITECTURE_BLUEPRINTS,bridgeDeck} from '../client/architecture-workshop.mjs';
import {ARCHITECTURE_ROUTINES,ARCHITECTURE_CONTROLS,architecturePose,architectureGeometry} from '../client/architecture-routines.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';import {scene} from './scenes.mjs';
const ages=['hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'],items=Object.entries(ARCHITECTURE_BLUEPRINTS);
const work=(id,f)=>({id,elapsed:ARCHITECTURE_ROUTINES[id].duration*f,start:{...ARCHITECTURE_CONTROLS,open:.3,panel:.7,flag:.4,bucket:.8,brake:.5}});
test('thirteen garden structures have bounded material construction in every control position',()=>{
 const seen=new Set();
 for(const [id,p]of items){
  seen.add(itemSprite(id,0).art.join('\n'));assert.equal(itemProfile({id},'unknown').material,p.material);
  for(const season of ['spring','summer','fall','winter'])for(const f of [0,.25,.5,.75,1]){
   const options={state:{architecture:{open:f,panel:f,flag:f,bucket:f,phase:f*Math.PI*2,season},wetness:.8,dirt:.8}},before=JSON.stringify(options),m=itemSprite(id,10,options);
   assert.equal(m.construction,'architecture-v1');assert(!m.clipped,id+' '+season+' '+f);assert(m.art.every(r=>/^[ -~]*$/.test(r)));
   assert(m.fills.every(a=>a.x>=0&&a.y>=0&&a.w>0&&a.x+a.w<=m.width&&a.y<m.art.length),id+' solid bounds');assert.equal(JSON.stringify(options),before);
   assert.deepEqual(itemSprite(id,100,options),m,'renderer does not advance a saved mechanism');
  }
 }
 assert.equal(seen.size,13);
});
test('gate, mailbox, bucket, sails and seasonal vines show their real saved states',()=>{
 for(const [id,a,b]of [['gate',{open:0},{open:1}],['mailbox',{panel:0},{panel:1}],['mailbox',{flag:0},{flag:1}],['wishing_well',{bucket:0},{bucket:1}],['windmill',{phase:0},{phase:.5}],['trellis',{season:'summer'},{season:'winter'}]])assert.notDeepEqual(itemSprite(id,0,{state:{architecture:a}}).art,itemSprite(id,0,{state:{architecture:b}}).art,id);
 assert.deepEqual(itemSprite('windmill',0,{motion:false,state:{architecture:{phase:0}}}).art,itemSprite('windmill',0,{motion:false,state:{architecture:{phase:2}}}).art);
});
test('thirty-six native scores keep all hatched bodies bounded and contacts grounded',()=>{
 let cases=0;
 for(const stage of ages)for(const [id,s]of Object.entries(ARCHITECTURE_ROUTINES))for(const f of [.2,.4,.6,.8]){
  const [item]=items.find(([,p])=>s.types.includes(p.type)),routine=work(id,f),pose=architecturePose(routine),home={...itemSprite(item,0,{pose:{architecture:pose}}),x:100,y:80,scale:itemWorldScale(item)};
  const c={...characterSprite({stage,facing:true,state:'idle',performance:{kind:'architecture',routine}},0),x:100,y:80},before=JSON.stringify({home,c}),g=architectureGeometry(home,{character:c,inside:1},6,9);
  assert(!c.clipped,stage+' '+id);assert.equal(g.character.scale,c.scale);assert(Math.abs(g.character.y*9-g.ground)<1e-9);assert.equal(before,JSON.stringify({home,c}));
  if(pose.contact===1){assert(Math.hypot(g.tip.x-g.target.x,g.tip.y-g.target.y)<1e-9);if(!['hatchling','duckling'].includes(stage)&&pose.tool==='hand')assert(Math.abs(g.hand.y-g.target.y)<6*g.cw*1.5,stage+' '+id+' keeps a short physical reach');}
  for(const k of Object.keys(ARCHITECTURE_CONTROLS))assert.equal(pose[k],architecturePose(routine,false)[k]);cases++;
 }
 assert.equal(cases,1152);
});
test('bridge feet follow the fixed deck and controls attach only to the chosen physical copy',()=>{
 const p=ARCHITECTURE_BLUEPRINTS.bridge,mid=bridgeDeck(p,.5);assert(mid.y<bridgeDeck(p,0).y&&mid.y<bridgeDeck(p,1).y);
 const routine=work('bridge_cross',.5),s=scene({items:[{id:'bridge',instance:'a',x:60,y:24},{id:'bridge',instance:'b',x:95,y:24}],living:{ecology:{},instances:{a:{architecture:{}},b:{architecture:{}}},objects:{},plan:{kind:'item',target:'bridge',instance:'a',phase:'act',progress:.5,elapsed:10,duration:24,destination:[60,24],architecture_work:routine}}}),world=new LivingWorld();
 world.render(s,0,.1);assert.equal(world.objects[0].structureUsers.length,1);assert(!world.objects[1].structureUsers);assert(world.objects[0].front);assert(!world.characters.some(c=>c.cheese));
 s.living.plan.paused=true;world.render(s,1,.1);const art=world.objects[0].structureUsers[0].character.art;world.render(s,100,.1);assert.deepEqual(world.objects[0].structureUsers[0].character.art,art);
 s.items[0].instance='replacement';world.render(s,101,.1);assert(!world.objects[0].structureUsers);assert(world.characters.some(c=>c.cheese));
});
