import test from 'node:test';
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {regions,waterAt,surfaceFitsRegion} from '../client/terrain.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
import {layoutBounds} from '../client/pond-layout.mjs';
import {groundBounds} from '../client/habitat-ground.mjs';
import {itemWorldScale} from '../client/ultra-items.mjs';
import footprints from '../client/animation/object-footprints.json' with {type:'json'};
import {scene} from './scenes.mjs';

const cameras=[{x:0,y:0,w:132,h:42},{x:10,y:2,w:107,h:38},{x:55,y:10,w:44,h:28}];
test('all original areas and every object use the same native/rendered support surface',()=>{
 const root=fileURLToPath(new URL('../../',import.meta.url));
 const code=`import json
from engine.terrain import REGIONS,surface_fits
from engine.pond_layout import FOOTPRINTS,bounds
from world.exploration import AREAS
assert {(a.name,a.biome.value) for group in AREAS.values() for a in group}=={(n,r['biome']) for n,r in REGIONS.items()}
print(json.dumps([surface_fits(item,bounds(item,x,y)['ground'],name,r['biome']) for name,r in REGIONS.items() for item in FOOTPRINTS for x,y in [(4,2),(10,6),(16,9)]]))`;
 const native=JSON.parse(execFileSync(root+'.venv/bin/python',['-c',code],{cwd:root,maxBuffer:2**22}));
 let i=0;
 for(const [location,r]of Object.entries(regions))for(const [item,f]of Object.entries(footprints.items))for(const [x,y]of [[4,2],[10,6],[16,9]]){
  assert.equal(surfaceFitsRegion(item,groundBounds(item,layoutBounds(f,x,y),y),location,r.biome),native[i++],`${location}: ${item} at ${x},${y}`);
 }
 assert.equal(i,21*542*3);
});
test('water masks and scenery anchors follow world positions in all 21 areas',()=>{
 const world=new LivingWorld();
 for(const [location,r]of Object.entries(regions))for(const camera of cameras){
  const s=scene({location,biome:r.biome,camera,motion:false,particles:false,weatherEffects:false});
  const result=world.render(s,0);
  for(let gx=27;gx<215;gx+=9)for(let gy=45;gy<110;gy+=7){
   const wx=camera.x+(gx-24)*camera.w/192,wy=camera.y+(gy-46)*camera.h/47;
   assert.equal(Boolean(world.water[gy*240+gx]),waterAt(location,wx,wy),`${location} ground ${gx},${gy}`);
  }
  for(const feature of r.features){
   const layer=result.scenery.find(l=>l.id===feature.id);
   assert.ok(layer,`${location}: ${feature.id} participates in scenery depth`);
   const [x,y]=world.project(s,(feature.x-24)*132/192,(feature.y-46)*42/47);
   assert.equal(layer.y,y+(feature.kind==='tree'?2:0));
   assert.ok(Number.isFinite(x));
   if(feature.surface!=='either')for(let ix=0;ix<=16;ix++)for(let iy=0;iy<=4;iy++){
    const wx=(feature.x+feature.width*(ix/16-.5)-24)*132/192,wy=(feature.y+feature.depth*(iy/4-.5)-46)*42/47;
    assert.equal(waterAt(location,wx,wy),feature.surface==='water',`${location}: ${feature.id} has appropriate ground`);
   }
  }
 }
});
test('a portable item stays at its saved object anchor with its measured scale',()=>{
 for(const camera of cameras)for(const id of ['toy_ball','tiny_boat','bubble_wand','picture_frame','jump_rope','skateboard']){
  const plan={kind:'item',target:id,location:'Home Pond',phase:'act',elapsed:5,duration:20,portable:{location:'Home Pond',object:[60,25],stance:[55.1875,25]},destination:[55.1875,25]};
  const s=scene({camera,living:{plan,objects:{[id]:{}},ecology:{}}}),world=new LivingWorld();
  const result=world.render(s,0),object=result.objects.find(o=>o.id===id);
  assert.ok(object,`${id} visible`);
  assert.deepEqual([object.x,object.y],world.project(s,60,25));
  assert.equal(object.scale,itemWorldScale(id));
  plan.portable.deployed=true;plan.phase='approach';
  assert.ok(world.render(s,0).objects.some(o=>o.portable),'deployed item remains while Cheese walks back');
  plan.paused=true;
  assert.ok(world.render(s,0).objects.some(o=>o.portable),'paused item remains at its saved location');
  assert.equal(world.render({...s,location:'Sunny Meadow',biome:'meadow'},0).objects.some(o=>o.portable),false,'left-behind prop stays in its own area');
 }
});
