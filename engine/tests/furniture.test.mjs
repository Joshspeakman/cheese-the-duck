import test from 'node:test';
import assert from 'node:assert/strict';
import {FURNITURE_BLUEPRINTS} from '../client/furniture-workshop.mjs';
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';
import {SEATING_ROUTINES,seatingPose,seatingGeometry} from '../client/seating-routines.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
import {DUCK_AGES} from '../client/duck-rig.mjs';
import {GUEST_CAST} from '../client/visitor-rig.mjs';
import {scene} from './scenes.mjs';
test('all 28 furniture constructions remain within their authored bounds',()=>{
 const signatures=new Set();
 for(const [id,bp] of Object.entries(FURNITURE_BLUEPRINTS)){
  for(let frame=0;frame<48;frame++){
   const m=itemSprite(id,frame/5,{context:{hour:15.25,season:'fall'},state:{dirt:.7,condition:.3,wetness:.7},interaction:{phase:'act'}});
   assert.equal(m.construction,'furniture-v1');assert.equal(m.clipped,false,id+' '+frame);
   assert(m.art.every((row,y)=>row.length===m.width&&m.tones[y].length===m.width&&/^[ -~]*$/.test(row)));
   assert(m.fills.every(f=>Number.isFinite(f.x+f.y+f.w)&&f.x>=0&&f.y>=0&&f.x+f.w<=m.width&&f.y<m.art.length),id+' solid bounds');
   if(bp.seat){assert.equal(m.anchors.slots.length,bp.capacity);assert(m.anchors.seatWidth>20);}
  }
  signatures.add(itemSprite(id,0).art.join('\n'));assert(itemWorldScale(id)>.6);
  const opts={motion:false,context:{hour:13.5},interaction:{phase:'act'}};
  assert.deepEqual(itemSprite(id,0,opts),itemSprite(id,50,opts),id+' reduced motion');
 }
 assert.equal(signatures.size,28);
});
test('clock faces follow game time and trophy cases show earned objects only',()=>{
 for(const id of ['clock','grandfather_clock']){
  assert.notDeepEqual(itemSprite(id,0,{context:{hour:3.25}}).art,itemSprite(id,0,{context:{hour:7.75}}).art);
  const m=itemSprite(id,0,{context:{hour:0}});
  assert(!m.art[20].includes('(=)'),id+' grain must not bleed through the clock face');
 }
 const empty=itemSprite('trophy_case',0),awarded=itemSprite('trophy_case',0,{context:{living:{objects:{toy_ball:{},gold_trophy:{},fishing_medal:{}}}}});
 assert.deepEqual(empty.anchors.displayed,[]);assert.deepEqual(awarded.anchors.displayed,['gold_trophy','fishing_medal']);
 assert.notDeepEqual(empty.art,awarded.art);
 const hammock=t=>itemSprite('hammock',t);
 assert.deepEqual(hammock(0).art,hammock(10).art,'an empty hammock must not perform an invented occupant routine');
});
function fixture(id,age='adult',guest=null,progress=.5,item='couch'){
 const routine={id,elapsed:SEATING_ROUTINES[id].duration*progress,done:false};
 return scene({duck:{x:60,y:24,stage:age,state:'idle',cosmetics:{}},visitor:guest?{id:guest,castId:guest,x:60,y:24,state:'idle'}:null,
  items:[{id:item,x:60,y:24}],living:{plan:{kind:'item',target:item,phase:'act',duration:24,elapsed:15,destination:[60,24],seating:{id:item,destination:[60,24],slot:0,capacity:2},seat_routine:routine},
  ecology:{},objects:{},garden:[],projects:[],minds:{seats:guest?[{actor:guest,id:item,destination:[60,24],slot:1,capacity:2,phase:'inside',elapsed:0,routine:{...routine,role:'b'}}]:[]}}});
}
test('seating supports every hatched age and every cast member without clipping or fluctuating body scale',()=>{
 const world=new LivingWorld(),sources=[...DUCK_AGES.filter(a=>a.id!=='egg').map(a=>({age:a.id})),...Object.keys(GUEST_CAST).map(guest=>({age:'adult',guest}))];
 for(const source of sources)for(const [id,spec] of Object.entries(SEATING_ROUTINES)){
  let previousScale=null;
  for(const progress of [0,.18,.36,.55,.76,.9,1]){
   const s=fixture(id,source.age,source.guest,progress),before=JSON.stringify(s),w=world.render(s,1,.1),home=w.objects.find(o=>o.sitters);
   assert.equal(JSON.stringify(s),before);assert(home,id);
   const sitter=home.sitters.at(-1),body=sitter.character;
   assert.equal(body.clipped,false,(source.guest||source.age)+' '+id+' '+progress);
   assert(body.seatContact>0);assert(body.art.every(row=>/^[ -~]*$/.test(row)));
   const drawn=seatingGeometry(home,sitter,6,9);
   assert(Number.isFinite(drawn.character.x+drawn.character.y+drawn.character.scale));
   if(previousScale!==null)assert.equal(drawn.character.scale,previousScale,'fit remains constant '+source.guest+' '+id);
   previousScale=drawn.character.scale;
   const unit=6*home.scale*home.detailScale,ch=unit*1.5,top=home.y*9-home.art.length*ch;
   const bellyY=drawn.character.y*9+(body.seatContact-body.groundRow)*drawn.character.scale*9+(body.offsetY||0)*drawn.character.scale*6;
   assert(Math.abs(bellyY-(top+home.anchors.slots[sitter.slot].y*ch))<.001,'belly touches the actual cushion');
   assert.equal(w.characters.filter(c=>source.guest?c.id===source.guest:c.cheese).length,0,'no duplicate on the ground');
  }
 }
});
test('seating follows the exact placed copy, independent arrivals, pausing and reduced motion',()=>{
 const w=new LivingWorld(),s=fixture('bench_gossip','hatchling','friendly_goose');
 let r=w.render(s,0,.1);assert.equal(r.objects[0].sitters.length,2);
 s.items[0].x=90;r=w.render(s,1,.1);assert.equal(r.objects[0].sitters,undefined,'wrong physical copy is never staged');
 s.items[0].x=60;s.living.plan.paused=true;s.living.minds.seats[0].phase='approach';
 r=w.render(s,2,.1);assert.equal(r.objects[0].sitters,undefined);assert(r.characters.some(c=>c.cheese));
 s.living.plan.paused=false;s.living.minds.seats[0].phase='inside';s.motion=false;
 const first=w.render(s,1,.1).objects[0].sitters.map(c=>c.character.art);
 assert.deepEqual(w.render(s,50,.1).objects[0].sitters.map(c=>c.character.art),first);
 for(const [id,spec] of Object.entries(SEATING_ROUTINES)){
  const signatures=new Set([0,.2,.4,.6,.8,1].map(p=>JSON.stringify(seatingPose({id,elapsed:p*spec.duration}))));
  assert(signatures.size>4,id+' must contain articulated beats');
 }
});
