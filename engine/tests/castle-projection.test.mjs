import test from 'node:test';
import assert from 'node:assert/strict';
import {castleArtWorld,castleArtFrame,projectCastleWorld,castleActorPitches,CASTLE_UNIT} from '../client/castle-projection.mjs';
import {castleGeometry,CASTLE_SCORES} from '../client/castle-care.mjs';
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
import {scene} from './scenes.mjs';
import {W,H} from '../client/ultra-grid.mjs';
const origin=[63,25],cameras=[{x:0,y:0,w:132,h:42},{x:10,y:2,w:107,h:38},{x:40,y:9,w:60,h:28}],windows=[[1440,900],[2400,700],[800,1200]];
function home(camera){const physicalCastle={origin,camera},at=projectCastleWorld(physicalCastle,origin);return {...itemSprite('bounce_house',0),...at,scale:itemWorldScale('bounce_house'),physicalCastle};}
const close=(a,b)=>assert.ok(Math.abs(a-b)<1e-8,`${a} != ${b}`);
test('fixed native castle cells, controls and support project identically across aspect/camera',()=>{
 close(CASTLE_UNIT,.4092);
 for(const camera of cameras)for(const [w,h]of windows){
  const sx=w/W,sy=h/H,house=home(camera),frame=castleArtFrame(house,sx,sy);
  for(const anchor of Object.values(house.anchors.controls)){
   const world=castleArtWorld(origin,anchor.x,anchor.y,{center:true}),pixel=projectCastleWorld(house.physicalCastle,world,sx,sy);
   close(pixel.x,frame.left+(anchor.x+.5)*frame.unit);close(pixel.y,frame.top+(anchor.y+.5)*frame.uh);
  }
  const ground=projectCastleWorld(house.physicalCastle,castleArtWorld(origin,90,147),sx,sy);close(ground.y,frame.ground);
 }
});
test('pilot body root remains saved native position with no renderer approach/exit interpolation',()=>{
 for(const camera of cameras)for(const [width,height]of windows)for(const phase of ['approach','hold','exit'])for(const motion of [false,true]){
  const sx=width/W,sy=height/H,h=home(camera),target=castleArtWorld(origin,149,142,{center:true}),root=[target[0]-2,target[1]+1];
  const work={id:'castle_start',stage:'service',clock:10,ride_elapsed:CASTLE_SCORES.castle_start.duration*.5,physical:{version:1,actor:'cheese',root,target,phase,station:'switch',contact_ready:false}};
  const c={...characterSprite({stage:'adult',state:'idle',performance:{kind:'carnival',routine:work,role:'a',motion}},0),x:0,y:0,physicalCastleActor:h.physicalCastle};
  const before=JSON.stringify({h,c,work}),g=castleGeometry(h,{character:c,work,role:'a'},sx,sy),expected=projectCastleWorld(h.physicalCastle,root,sx,sy);
  assert.equal(g.authoritativeRoot,true);close(g.character.x*sx,expected.x);close(g.character.y*sy,expected.y);assert.equal(g.points.length,0);assert.equal(JSON.stringify({h,c,work}),before);
  const pitches=castleActorPitches(c,sx,sy);close(pitches.cw,c.scale*132/camera.w*sx);close(pitches.ch,c.scale*42/camera.h*sy);
 }
});
test('legacy care controls follow physical art while retaining their explicitly nonauthoritative staging',()=>{
 for(const camera of cameras)for(const [width,height]of windows){
  const h=home(camera),sx=width/W,sy=height/H,work={id:'castle_start',stage:'service',clock:20,ride_elapsed:CASTLE_SCORES.castle_start.duration*.5};
  const c={...characterSprite({stage:'adult',state:'idle',performance:{kind:'carnival',routine:work,role:'a'}},0),x:100,y:80};
  const g=castleGeometry(h,{character:c,work,role:'a'},sx,sy),expected=projectCastleWorld(h.physicalCastle,castleArtWorld(origin,149,142,{center:true}),sx,sy);
  close(g.target.x,expected.x);close(g.target.y,expected.y);assert.equal(g.authoritativeRoot,false);
 }
});
test('world carries physical projection continuously while catalogue sprites retain their existing dimensions',()=>{
 const world=new LivingWorld();
 for(const camera of cameras){const s=scene({camera,items:[{id:'bounce_house',x:origin[0],y:origin[1],instance:'projection-test'}]}),before=JSON.stringify(s),h=world.render(s,0).objects.find(o=>o.id==='bounce_house');assert.deepEqual(h.physicalCastle,{origin,camera});assert.equal(JSON.stringify(s),before);}
 assert.equal(itemSprite('bounce_house',0).physicalCastle,undefined);
});

test('native contact readiness cannot draw beyond the three-cell grip ellipse or move the root',()=>{
 for(const camera of cameras)for(const [width,height]of windows){
  const h=home(camera),sx=width/W,sy=height/H,target=castleArtWorld(origin,149,142,{center:true});
  const root=[target[0]-15.5*.675*132/192,target[1]+4*.675*42/47];
  const w={id:'castle_start',stage:'service',clock:30,ride_elapsed:CASTLE_SCORES.castle_start.duration*.5,physical:{version:1,actor:'cheese',root,target,phase:'hold',station:'switch',contact_ready:true}};
  const c={...characterSprite({stage:'adult',state:'idle',performance:{kind:'carnival',routine:w,role:'a'}},0),scale:.675,grip:{x:51,y:35},x:100,y:80,physicalCastleActor:h.physicalCastle};
  const g=castleGeometry(h,{character:c,work:w,role:'a'},sx,sy);assert.equal(g.reachable,true);assert.ok(g.points.length);
  const distant={...w,physical:{...w.physical,root:[root[0]-20,root[1]]}},bad=castleGeometry(h,{character:c,work:distant,role:'a'},sx,sy);
  assert.equal(bad.reachable,false);assert.equal(bad.points.length,0);const expected=projectCastleWorld(h.physicalCastle,distant.physical.root,sx,sy);close(bad.character.x*sx,expected.x);close(bad.character.y*sy,expected.y);
 }
});

test('malformed restored pilot cannot fall back to renderer-owned movement or contact',()=>{
 const h=home(cameras[0]),w={id:'castle_start',stage:'service',clock:30,ride_elapsed:CASTLE_SCORES.castle_start.duration*.5,physical_pilot:true};
 const c={...characterSprite({stage:'adult',state:'idle',performance:{kind:'carnival',routine:w,role:'a'}},0),x:77,y:65};
 for(const physical of [undefined,{}, {version:1,actor:'cheese',root:[NaN,2],target:[1,2],contact_ready:true}]){
  const g=castleGeometry(h,{character:c,work:{...w,physical},role:'a'},6,9);assert.equal(g.character.x,c.x);assert.equal(g.character.y,c.y);assert.equal(g.points.length,0);assert.equal(g.reachable,false);
 }
});
