import test from 'node:test';
import assert from 'node:assert/strict';
import {displayCamera,actorPitches} from '../client/actor-projection.mjs';
import {castleArtFrame,castleArtWorld,projectCastleWorld} from '../client/castle-projection.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
import {regions,waterAt} from '../client/terrain.mjs';
import {scene} from './scenes.mjs';
import {W,H} from '../client/ultra-grid.mjs';
const cameras=[{x:0,y:0,w:132,h:42},{x:10,y:2,w:107,h:38},{x:40,y:9,w:60,h:28}];
const windows=[[1440,900],[1800,800],[800,1200]];
const close=(a,b)=>assert.ok(Math.abs(a-b)<1e-8,`${a} != ${b}`);
test('display camera expands about native center and preserves rig proportions and castle contacts',()=>{
 for(const base of cameras)for(const [width,height]of windows){
  const before=JSON.stringify(base),sx=width/W,sy=height/H,camera=displayCamera(base,sx,sy);
  assert.equal(JSON.stringify(base),before);assert.ok(camera.w>=base.w&&camera.h>=base.h);
  close(camera.x+camera.w/2,base.x+base.w/2);close(camera.y+camera.h/2,base.y+base.h/2);
  const p=actorPitches({scale:.675,physicalActorProjection:{camera}},sx,sy);close(p.ch/p.cw,1.5);
  const origin=[63,25],physicalCastle={origin,camera},f=castleArtFrame({physicalCastle},sx,sy);close(f.uh/f.unit,1.5);
  const target=castleArtWorld(origin,149,142,{center:true}),pixel=projectCastleWorld(physicalCastle,target,sx,sy);
  close(pixel.x,f.left+149.5*f.unit);close(pixel.y,f.top+142.5*f.uh);
  const root=[target[0]-15.5*.675*132/192,target[1]+4*.675*42/47],r=projectCastleWorld(physicalCastle,root,sx,sy);
  close(r.x+15.5*p.cw,pixel.x);close(r.y-4*p.ch,pixel.y);
 }
});
test('display camera terrain inverse and world roots agree across regions and viewport edges',()=>{
 const world=new LivingWorld();
 for(const [location,r]of Object.entries(regions))for(const base of cameras)for(const [width,height]of windows){
  const camera=displayCamera(base,width/W,height/H),s=scene({location,biome:r.biome,camera,motion:false,particles:false,weatherEffects:false});
  world.render(s,0);
  for(const gx of [0,24,120,215,239])for(const gy of [43,46,69,93,111]){
   const wx=camera.x+(gx-24)*camera.w/192,wy=camera.y+(gy-46)*camera.h/47;
   const [x,y]=world.project(s,wx,wy);close(x,gx);close(y,gy);
   assert.equal(Boolean(world.water[gy*W+gx]),waterAt(location,wx,wy,r.biome),`${location} ${width}x${height} ${gx},${gy}`);
  }
 }
});

test('camera changes reproject the current native root without interpolating from old screen coordinates',()=>{
 const world=new LivingWorld();
 for(const base of cameras)for(const [width,height]of windows){
  const camera=displayCamera(base,width/W,height/H),s=scene({camera,motion:true,duck:{x:65,y:24,stage:'adult',state:'idle'}});
  const result=world.render(s,0,0),cheese=result.characters.find(c=>c.cheese),expected=world.project(s,65,24);
  close(cheese.x,expected[0]);close(cheese.y,expected[1]);
 }
});

test('native control approach never interpolates the actor away from its actual root at high frame rates',()=>{
 const world=new LivingWorld(),camera=displayCamera({x:0,y:0,w:132,h:42},6,8);
 for(const x of [60,61,62,63]){
  const s=scene({camera,motion:true,duck:{x,y:24,stage:'adult',state:'walking'},living:{ecology:{},plan:{carnival_work:{physical_pilot:true}}}});
  const result=world.render(s,0,1/60),cheese=result.characters.find(c=>c.cheese),expected=world.project(s,x,24);
  close(cheese.x,expected[0]);close(cheese.y,expected[1]);
 }
});
