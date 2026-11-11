import test from 'node:test';
import assert from 'node:assert/strict';
import {HOME_BLUEPRINTS} from '../client/home-workshop.mjs';
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';
import {duckRig,DUCK_AGES} from '../client/duck-rig.mjs';
import {residenceStage,occupiedGeometry} from '../client/residence-stage.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
import {scene} from './scenes.mjs';
test('home geometry, contact anchors and weather details remain within their authored bounds',()=>{
 for(const id of Object.keys(HOME_BLUEPRINTS))for(const season of ['spring','summer','fall','winter'])for(const hour of [5,12,20])for(const t of [0,.4,1.1]){
  const m=itemSprite(id,t,{context:{season,hour,weather:'rain'},interaction:{phase:'act',kind:'rest'},state:{condition:.3,wetness:.8,dirt:.7}});
  assert.equal(m.construction,'workshop-v1');assert.equal(m.clipped,false,id);
  assert(m.art.join('').replace(/ /g,'').length>200,id+' contains constructed detail');
  for(const a of [m.anchors.entry,m.anchors.seat])assert(a.x>=0&&a.x<m.width&&a.y>=0&&a.y<m.art.length,id);
  assert(m.art.every((r,y)=>r.length===m.tones[y].length&&/^[ -~]*$/.test(r)),id);
 }
});
test('occupied homes fit all nine silhouettes without enlarging Cheese or changing his design',()=>{
 for(const id of Object.keys(HOME_BLUEPRINTS))for(const age of DUCK_AGES){
  const home={...itemSprite(id,1),scale:itemWorldScale(id),x:100,y:80},duck={...duckRig({stage:age.id,state:'sleeping'},1),x:100,y:80};
  const g=occupiedGeometry(home,duck,1,6,9);
  assert(g.character.scale>0&&g.character.scale<=duck.scale,id+' '+age.id);assert.equal(g.character.design,'d10');
  if(g.clip)assert(g.clip.w>0&&g.clip.h>0);else assert(g.front&&g.front.art.slice(0,home.anchors.rim).every(r=>!r.trim()),id);
 }
});
test('only a real, arrived, unpaused plan occupies the matching home instance',()=>{
 const plan={kind:'rest',target:'cozy_nest',phase:'act',progress:.5,residence:{destination:[60,24]}};
 const s=scene({items:[{id:'cozy_nest',x:10,y:24},{id:'cozy_nest',x:60,y:24}],living:{ecology:{},plan,objects:{},projects:[],garden:[]}}),w=new LivingWorld();
 let r=w.render(s,1,.03);
 assert.equal(r.objects.filter(o=>o.occupant).length,1);assert.equal(r.objects.find(o=>o.occupant).worldPosition[0],60);
 assert.equal(r.characters.filter(c=>c.cheese).length,0);
 for(const changes of [{phase:'approach'},{paused:true}]){r=w.render({...s,living:{...s.living,plan:{...plan,...changes}}},1,.03);assert(!r.objects.some(o=>o.occupant));assert.equal(r.characters.filter(c=>c.cheese).length,1);}
 assert.equal(residenceStage(plan,[],duckRig({stage:'adult'},0)),null);
});
