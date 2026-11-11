import test from 'node:test';
import assert from 'node:assert/strict';
import {PLAY_BLUEPRINTS} from '../client/playground-workshop.mjs';
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';
import {playgroundStage,ridingGeometry} from '../client/playground-stage.mjs';
import {duckRig} from '../client/duck-rig.mjs';
test('new playground constructions keep moving parts and contact points inside their bounds',()=>{
 for(const id of Object.keys(PLAY_BLUEPRINTS))for(let n=0;n<64;n++){
  const m=itemSprite(id,n/8,{interaction:{phase:'act'},state:{condition:.3,wetness:.8,dirt:.7},context:{season:'winter'}});
  assert.equal(m.construction,'playground-v1');assert.equal(m.clipped,false,id+' '+n);
  assert(m.art.join('').replace(/ /g,'').length>50,id);
  for(const a of Object.values(m.anchors))if(!Array.isArray(a))assert(a.x>=0&&a.x<m.width&&a.y>=0&&a.y<m.art.length,id+' contact');
  assert(m.art.every((r,y)=>r.length===m.tones[y].length&&/^[ -~]*$/.test(r)),id);
  assert(itemWorldScale(id)>0&&itemWorldScale(id)<=1);
 }
});
test('riding follows real item plans and young Cheese plays at the foot of tall slides',()=>{
 const id='toy_slide',plan={kind:'item',target:id,phase:'act',progress:.5,elapsed:12,duration:24,destination:[60,24]};
 const m={...itemSprite(id,1,{interaction:plan}),x:100,y:80,scale:itemWorldScale(id),worldPosition:[60,24]};
 const duck={...duckRig({stage:'adult'},1),x:100,y:80};
 const adult=playgroundStage(plan,[m],duck,'adult'),young=playgroundStage(plan,[m],duck,'hatchling');
 assert(adult.seat.y<young.seat.y);assert.equal(young.gesture,'splash_steps');
 assert.equal(playgroundStage({...plan,paused:true},[m],duck,'adult'),null);
 assert.equal(playgroundStage({...plan,phase:'approach'},[m],duck,'adult'),null);
 assert.equal(playgroundStage({...plan,target:'unknown'},[m],duck,'adult'),null);
 const placed=ridingGeometry(m,duck,adult.seat,1,6,9);assert(placed.y<duck.y);assert.equal(placed.scale,duck.scale);
 assert.deepEqual(ridingGeometry(m,duck,adult.seat,0,6,9),duck);
});
test('seesaw seats move in opposition and swing seats remain attached to suspension',()=>{
 const anchors=id=>[.2,.5,.9,1.3].map(t=>itemSprite(id,t,{interaction:{phase:'act'}}).anchors);
 const saw=anchors('toy_seesaw');assert(new Set(saw.map(a=>a.seat.y)).size>2);
 for(const a of saw)assert(Math.abs((a.seat.y+a.partner.y)/2-20)<.01);
 const swing=anchors('toy_swing');assert(new Set(swing.map(a=>a.seat.x)).size>2);assert(swing.every(a=>a.pivot.x===51&&a.pivot.y===9&&a.seat.y>a.pivot.y));
});
test('each slide has a continuous authored run from platform to exit',()=>{
 for(const id of ['toy_slide','water_slide','water_slide_mega','rainbow_slide']){
  const a=itemSprite(id,1).anchors;assert.equal(a.path.length,46);
  for(let n=1;n<a.path.length;n++){const prev=a.path[n-1],next=a.path[n];assert(next[0]>prev[0]&&next[1]>=prev[1]);assert(Math.hypot(next[0]-prev[0],next[1]-prev[1])<3);}
  assert(a.path.at(-1)[1]>a.top.y+25);
 }
});
