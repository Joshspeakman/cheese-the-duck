import test from 'node:test';
import assert from 'node:assert/strict';
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';
import {FOOD_BLUEPRINTS} from '../client/food-workshop.mjs';
import {SPECIMEN_BLUEPRINTS} from '../client/specimen-workshop.mjs';
import {SEED_BLUEPRINTS} from '../client/seed-workshop.mjs';
import footprints from '../client/animation/object-footprints.json' with {type:'json'};
import {LivingWorld} from '../client/ultra-world.mjs';
import {surfaceFitsRegion} from '../client/terrain.mjs';
import {layoutBounds} from '../client/pond-layout.mjs';
import {groundBounds} from '../client/habitat-ground.mjs';
import {scene} from './scenes.mjs';
export const batches={'food-v1':FOOD_BLUEPRINTS,'specimen-v1':SPECIMEN_BLUEPRINTS,'seed-v1':SEED_BLUEPRINTS};
export function safePosition(id){for(let y=28;y>=10;y-=2)for(let x=40;x<100;x+=3)if(surfaceFitsRegion(id,groundBounds(id,layoutBounds(footprints.items[id],x,y),y),'Sunny Meadow','meadow'))return {x,y};throw Error('No safe position for '+id);}
test('all 75 food, specimen, and seed inventory items use production artwork and measured footprints',()=>{
 let count=0;
 for(const [construction,blueprints]of Object.entries(batches))for(const id of Object.keys(blueprints)){
  count++;const m=itemSprite(id,0),f=footprints.items[id],scale=itemWorldScale(id);
  assert.equal(m.construction,construction,id);assert.equal(f.construction,construction,id);assert.equal(m.clipped,false,id);
  assert.ok(scale>=.3&&scale<=.55,id);assert.ok(f.width>10&&f.width<60,id);assert.equal(m.groundRow,m.art.length,id);
  assert.ok(m.art.at(-1).trim()||m.fills.some(f=>f.y===m.groundRow-1),id);
  assert.deepEqual(itemSprite(id,0,{motion:false}),itemSprite(id,100,{motion:false}),id);
 }
 assert.equal(count,75);
});
test('all 75 production world objects retain safe saved anchors at day/night and multiple cameras',()=>{
 const world=new LivingWorld();let checks=0;
 for(const blueprints of Object.values(batches))for(const id of Object.keys(blueprints))for(const hour of [14,23])for(const camera of [{x:0,y:0,w:132,h:42},{x:10,y:2,w:107,h:38}]){
  const position=safePosition(id),state={condition:.3,dirt:.8,wetness:.6};
  const s=scene({location:'Sunny Meadow',biome:'meadow',hour,camera,motion:false,items:[{id,...position,instance:'review'}],living:{objects:{[id]:state},ecology:{}}}),before=JSON.stringify(s);
  const o=world.render(s,0).objects.find(o=>o.id===id);assert.ok(o,id);assert.deepEqual([o.x,o.y],world.project(s,position.x,position.y),id);assert.equal(o.scale,itemWorldScale(id),id);assert.equal(o.lift,0,id);assert.equal(JSON.stringify(s),before);checks++;
 }
 assert.equal(checks,300);
});
