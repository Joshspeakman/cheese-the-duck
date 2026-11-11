import test from 'node:test';
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import footprints from '../client/animation/object-footprints.json' with {type:'json'};
import {homeShore,homeBankOnScreen,surfaceFits,homeScenery} from '../client/habitat-ground.mjs';
import {layoutBounds,layoutCheck} from '../client/pond-layout.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
import {scene} from './scenes.mjs';
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';
import {PLAYDATES} from '../client/playdates.mjs';

test('placement measurements stay current with all actual item drawings',()=>{
 execFileSync(process.execPath,[fileURLToPath(new URL('../build-footprints.mjs',import.meta.url)),'--check'],{stdio:'pipe'});
 assert.equal(Object.keys(footprints.items).length,542);
});
test('shared ball passages fit their reserved ground, including the expanded court',()=>{
 for(const id of ['toy_ball','ball'])for(const [score,spec]of Object.entries(PLAYDATES).filter(([,s])=>s.family==='ball')){
  for(const fraction of [0,.2,.5,.8,1]){
   const model=itemSprite(id,0,{interaction:{kind:'item',target:id,phase:'act',company:{id:score,phase:'act',elapsed:fraction*spec.duration,duration:spec.duration}}});
   const width=(model.width+2)*itemWorldScale(id)*model.detailScale;
   assert.ok(width<=footprints.items[id].width,`${id}: ${score} must not outgrow its bank reservation`);
  }
 }
});
test('scenery roots and dock reject placement; world anchors follow the same camera as items',()=>{
 const layout={items:[{id:'toy_ball',footprint:footprints.items.toy_ball},{id:'tiny_boat',footprint:footprints.items.tiny_boat}],placed:[],obstacles:[]};
 for(const f of homeScenery)assert.ok(!layoutCheck(layout,f.kind==='dock'?'tiny_boat':'toy_ball',f.x,f.y).ok);
 for(const camera of [{x:0,y:0,w:132,h:42},{x:10,y:2,w:107,h:38},{x:55,y:10,w:44,h:28}]){
  const world=new LivingWorld(),s=scene({camera}),result=world.render(s,0);
  for(const f of homeScenery){
   const layer=result.scenery.find(l=>l.id===f.id),[x,y]=world.project(s,f.x*132/20,f.y*42/12);
   assert.equal(layer.y,y+(f.kind==='dock'?3:2));
   assert.ok(Number.isFinite(x));
  }
 }
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
