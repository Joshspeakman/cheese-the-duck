import test from 'node:test';
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import footprints from '../client/animation/object-footprints.json' with {type:'json'};
import {homeShore,homeBankOnScreen,surfaceFits} from '../client/habitat-ground.mjs';
import {layoutBounds,layoutCheck} from '../client/pond-layout.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
import {scene} from './scenes.mjs';

test('placement measurements stay current with all actual item drawings',()=>{
 execFileSync(process.execPath,[fileURLToPath(new URL('../build-footprints.mjs',import.meta.url)),'--check'],{stdio:'pipe'});
 assert.equal(Object.keys(footprints.items).length,542);
});
test('Home Pond water and dry ground follow world positions across camera movement',()=>{
 const world=new LivingWorld();
 for(const camera of [{x:0,y:0,w:132,h:42},{x:10,y:2,w:107,h:38},{x:55,y:10,w:44,h:28}]){
  world.terrain(scene({camera}),0,123);
  for(let x=30;x<210;x+=7){
   const bank=homeBankOnScreen(x,camera),wx=camera.x+(x-24)/192*camera.w;
   const expected=46+(homeShore(wx*20/132)*42/12-camera.y)/camera.h*47;
   assert.ok(Math.abs(bank-expected)<1e-7);
   for(const [y,water] of [[Math.floor(bank)-1,0],[Math.ceil(bank)+1,1]])
    if(y>=43&&y<110)assert.equal(world.water[y*240+x],water);
  }
 }
});
test('preview rejects wet furniture, dry boats, overlap and invalid coordinates; allows rugs under chairs',()=>{
 const couch=footprints.items.couch,boat=footprints.items.tiny_boat;
 const layout={items:[{id:'couch',footprint:couch},{id:'tiny_boat',footprint:boat}],placed:[],obstacles:[]};
 assert.ok(!layoutCheck(layout,'couch',10,11).ok);
 assert.ok(!layoutCheck(layout,'tiny_boat',10,2).ok);
 assert.ok(!layoutCheck(layout,'couch',NaN,3).ok);
 assert.ok(!layoutCheck(layout,'couch',false,3).ok);
 assert.ok(!layoutCheck(layout,'couch',-20,3).ok);
 assert.ok(layoutCheck(layout,'couch',10,4).ok);
 layout.placed.push({id:'garden_bench',box:layoutBounds(footprints.items.garden_bench,10,4)});
 assert.ok(!layoutCheck(layout,'couch',10,4).ok);
 layout.placed=[{id:'grass_patch',box:layoutBounds(footprints.items.grass_patch,10,4)}];
 assert.ok(layoutCheck(layout,'couch',10,4).ok);
 assert.ok(surfaceFits('bridge',layoutBounds(footprints.items.bridge,10,8),8));
});
