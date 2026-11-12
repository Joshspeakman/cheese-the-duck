import test from 'node:test';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import {captureHomeScenery,exportCastleSceneryMetrics,scenerySampleTimes} from '../scripts/export-castle-scenery-metrics.mjs';
import METRICS from '../client/animation/castle-scenery-metrics.json' with {type:'json'};
import {canonicalSceneryPoint} from '../client/scenery-projection.mjs';
import {displayCamera} from '../client/actor-projection.mjs';
const near=(a,b)=>assert(Math.abs(a-b)<1e-8,`${a} != ${b}`);
test('canonical physical scenery preserves the approved clipped ink and painter order exactly',()=>{
 const hashes={west_willow:['4c8c6c3dac1575962cd22c58ab686774e865862bae53f1e16761b56156d51fbf','260e043d93c68a468909d6be53024ad655824d961aa604ae4c9e0744cc8c7b13','697866b5854ee3ec008a7333fce89d79247e625065efd974bb36bd137dac7489'],east_willow:['9e9a789346ff2a1508ce692877360b7324f5a4350bcb4827759e1e7c68520872','81a1646a8dc5f72e58f421bd96a7a59164ad8dce4757185f397791971f09425e','b25c0f78425148cb5975e4c3461d690c26cf7901202cd3937b0b035a85dd9132'],pond_dock:Array(3).fill('5a4c5d2378fe516f88858c1e96e47a079a64fa03eeb00286b4bba7c050d65385')};
 for(const [i,time]of [0,1.25,4.7].entries())for(const layer of captureHomeScenery(time)){
  const digest=crypto.createHash('sha256').update(JSON.stringify([...layer.cells].sort((a,b)=>a[0]-b[0]))).digest('hex');assert.equal(digest,hashes[layer.id][i]);
  for(const [x,y,w,h]of layer.projectedCells){assert(Number.isInteger(x)&&Number.isInteger(y));assert.equal(w,1);assert.equal(h,1);}
 }
});
test('every projected scenery glyph retains native extent inside exported full sway bounds across cameras',()=>{
 assert.deepEqual(METRICS,exportCastleSceneryMetrics());
 const cameras=[[1200,800,{x:0,y:0,w:132,h:42}],[1800,800,{x:0,y:0,w:132,h:42}],[900,1100,{x:0,y:0,w:132,h:42}],[1800,800,{x:17,y:-3,w:80,h:30}],[900,1100,{x:-22,y:5,w:170,h:50}]].map(([w,h,c])=>displayCamera(c,w/240,h/112));
 for(const camera of cameras)for(const time of [...scenerySampleTimes(),31.17,90.31,221.789])for(const layer of captureHomeScenery(time,camera)){
  const box=METRICS.features.find(f=>f.id===layer.id).bounds;assert.equal(layer.nativeCells.length,layer.projectedCells.length);
  for(const [i,[x,y,ch]]of layer.nativeCells.entries()){
   const [wx,wy]=canonicalSceneryPoint(x,y),[gx,gy,gw,gh]=layer.projectedCells[i];near(camera.x+(gx-24)*camera.w/192,wx);near(camera.y+(gy-46)*camera.h/47,wy);near(gw*camera.w/192,132/192);near(gh*camera.h/47,42/47);
   if(ch!==32){assert(wx>=box.x-1e-8&&wx+132/192<=box.x+box.w+1e-8,layer.id+' horizontal extent');assert(wy>=box.y-1e-8&&wy+42/47<=box.y+box.h+1e-8,layer.id+' vertical extent');}
  }
  assert(layer.cells.every(([i])=>i>=0&&i<240*112));
 }
});
