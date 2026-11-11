import test from 'node:test';
import assert from 'node:assert/strict';
import {BOTANICAL_ROUTINES,botanicalPose,botanicalGeometry} from '../client/botanical-routines.mjs';
import {BOTANICAL_BLUEPRINTS} from '../client/botanical-workshop.mjs';
import {itemSprite} from '../client/ultra-items.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {DUCK_AGES} from '../client/duck-rig.mjs';
import {GUEST_CAST} from '../client/guest-cast.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
const cast=[...DUCK_AGES.slice(1).map(a=>({stage:a.id})),...Object.values(GUEST_CAST).map(g=>({id:g.id,castId:g.id,name:g.name,visitor:true}))];
test('all 19 botanical scores move distinctly and freeze with reduced motion',()=>{
 const signatures=new Set();
 for(const [id,s] of Object.entries(BOTANICAL_ROUTINES)){
  const sequence=[0,.2,.4,.6,.8,1].map(f=>botanicalPose({id,elapsed:s.duration*f}));
  assert(new Set(sequence.map(v=>JSON.stringify(v))).size>=5,id);signatures.add(JSON.stringify(sequence));
  assert.deepEqual(botanicalPose({id,elapsed:0},false),botanicalPose({id,elapsed:999},false));
  assert.equal(botanicalPose({id,elapsed:5,interrupted:true}),null);
 }
 assert.equal(signatures.size,19);
});
test('all hatched ages and all 48 guests keep connected tool grips, supported feet and constant scale',()=>{
 let cases=0;
 for(const duck of cast)for(const facing of [true,false])for(const id of Object.keys(BOTANICAL_ROUTINES)){
  const scales=new Set();
  for(const progress of [0,.3,.6,1]){
   const s=BOTANICAL_ROUTINES[id],routine={id,elapsed:s.duration*progress};
   const c={...characterSprite({...duck,facing,state:'idle',performance:{kind:'botanical',routine}},100,duck.visitor),x:88,y:70};
   assert(!c.clipped,JSON.stringify({duck,id,progress}));scales.add(c.scale);
   if(c.identity?.species!=='butterfly'){
    assert(c.grip&&c.workGripRest);assert.notEqual(c.art[Math.round(c.grip.y)][Math.round(c.grip.x)],' ',duck.id+' empty grip');
   }
   const home={...itemSprite('fern',0),x:100,y:70};
   const frozen=JSON.stringify({c,home});const g=botanicalGeometry(home,{character:c,inside:1,slot:facing?0:1},6,9);
   assert.equal(JSON.stringify({c,home}),frozen);
   assert.equal(g.character.scale,c.scale);
   if(s.tool!=='none')assert(Math.abs(g.character.y*9-(g.stool?.top??(home.y*9-(home.art.length-home.anchors.entry.y)*6*home.scale*home.detailScale*1.5)))<.001);
   for(const p of [...g.points,...g.stream,g.hand,g.target])assert(Number.isFinite(p.x)&&Number.isFinite(p.y));
   if(g.pose.contact===1&&['brush','rake','probe'].includes(s.tool))assert.deepEqual(g.tip,g.target);
   if(g.pose.anchor==='leaf'&&g.pose.contact===1){
    const unit=6*home.scale*home.detailScale;
    const px=(g.target.x-home.x*6)/unit+home.width/2,py=(g.target.y-home.y*9)/(unit*1.5)+home.art.length;
    assert(home.fills.some(f=>'gl'.includes(f.tone)&&Math.abs(f.y-py)<=1&&px>=f.x-1&&px<=f.x+f.w),'bristles must follow a real leaf surface');
   }

   cases++;
  }
  assert.equal(scales.size,1);
 }
 assert.equal(cases,56*2*19*4);
});
function scene(){return {biome:'pond',location:'Home Pond',season:'spring',hour:12,weather:'sunny',motion:true,
 camera:{x:0,y:0,w:132,h:42},duck:{x:60,y:24,stage:'hatchling',state:'idle',cosmetics:{}},items:[{id:'fern',x:60,y:24}],structures:[],
 living:{ecology:{insects:0},plan:{kind:'item',target:'fern',plant_care:'water',phase:'act',duration:30,elapsed:15,destination:[60,24],care_routine:{id:'little_water',elapsed:15}},objects:{fern:{}},minds:{gardeners:[]}}};}
test('botanical staging respects actual placed copies, pauses and independent visitor arrivals',()=>{
 const w=new LivingWorld(),s=scene(),original=JSON.stringify(s);
 w.render(s,100,.1);assert.equal(JSON.stringify(s),original);assert.equal(w.objects.find(o=>o.id==='fern').gardeners.length,1);assert(!w.characters.some(c=>c.cheese));
 s.living.plan.paused=true;w.render(s,101,.1);assert(!w.objects.find(o=>o.id==='fern').gardeners);assert(w.characters.some(c=>c.cheese));
 s.living.plan.paused=false;s.living.plan.destination=[10,24];w.render(s,102,.1);assert(!w.objects.find(o=>o.id==='fern').gardeners);
 s.living.plan=null;s.visitor={id:'friend:frida',castId:'friend:frida',name:'Frida',x:59,y:24,state:'idle'};
 s.living.minds.gardeners=[{actor:'friend:frida',id:'fern',destination:[60,24],slot:0,phase:'approach',elapsed:0,routine:{id:'leaf_dust',elapsed:0}}];
 w.render(s,103,.1);assert(!w.objects.find(o=>o.id==='fern').gardeners);
 s.living.minds.gardeners[0].phase='inside';w.render(s,104,.1);assert.equal(w.objects.find(o=>o.id==='fern').gardeners[0].character.id,'friend:frida');
 assert(!w.characters.some(c=>c.id==='friend:frida'));
});

test('watering streams fall from the held spout into the soil for all rooted plants and ages',()=>{
 for(const item of Object.keys(BOTANICAL_BLUEPRINTS).filter(k=>BOTANICAL_BLUEPRINTS[k].rooted))for(const a of DUCK_AGES.slice(1))for(const [id,s]of Object.entries(BOTANICAL_ROUTINES).filter(([,s])=>s.tool==='can'))for(const f of [.28,.4,.55,.7,.8]){
  const character={...characterSprite({stage:a.id,performance:{kind:'botanical',routine:{id,elapsed:s.duration*f}}},0),x:90,y:70};
  const g=botanicalGeometry({...itemSprite(item,0),x:100,y:70},{character,inside:1,slot:0},6,9);
  if(g.stream.length)assert(g.tip.y<=g.target.y,JSON.stringify({item,age:a.id,id,f}));
 }
});
