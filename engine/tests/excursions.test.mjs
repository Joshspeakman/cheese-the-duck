import test from 'node:test';
import assert from 'node:assert/strict';
import {EXCURSION_BLUEPRINTS as BLUEPRINTS} from '../client/excursion-workshop.mjs';
import {itemSprite,itemWorldScale,catalog} from '../client/ultra-items.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
import {scene} from './scenes.mjs';

const state=(phase=1)=>({excursion:{phase,wind_phase:phase*2,wind:.5,inflation:.75,cover:.4,lights:1}});
test('ten distinct carnival and travel constructions retain printable ink and bounded fills throughout their mechanisms',()=>{
 const signatures=new Set();
 for(const [id,p]of Object.entries(BLUEPRINTS)){
  assert(catalog.some(i=>i.id===id),'original catalogue identity '+id);
  assert.equal(itemWorldScale(id),p.scale);
  signatures.add(itemSprite(id,0).art.join('\n'));
  for(let n=0;n<120;n++){
   const options={state:{excursion:{phase:n/120*Math.PI*2,wind_phase:n/8,wind:1,inflation:n/119*.65+.35,cover:n/119,lights:n%2}},context:{weather:'stormy',hour:23}},before=JSON.stringify(options),m=itemSprite(id,n,options);
   assert.equal(m.construction,'excursion-v1');assert(!m.clipped,id+' phase '+n);
   assert(m.art.every((r,y)=>r.length===m.width&&m.tones[y].length===m.width&&/^[ -~]*$/.test(r)));
   assert(m.fills.every(f=>f.x>=0&&f.y>=0&&f.w>0&&f.x+f.w<=m.width&&f.y<m.art.length),id+' bounded solid panels');
   for(const anchor of Object.values(m.anchors).flat())assert(anchor.x>=0&&anchor.x<m.width&&anchor.y>=0&&anchor.y<m.art.length,id+' usable anchor');
   assert.equal(JSON.stringify(options),before,'rendering cannot change saved state');
  }
 }
 assert.equal(signatures.size,10);
});
test('native clocks determine actual moving parts, with no renderer drift or accessibility rewind',()=>{
 for(const id in BLUEPRINTS){
  const saved=state(),a=itemSprite(id,0,{state:saved}),b=itemSprite(id,900,{state:saved});
  assert.deepEqual(a,b,id+' frozen native clock');
  const quiet=itemSprite(id,0,{motion:false,state:saved}),later=itemSprite(id,900,{motion:false,state:saved});
  assert.deepEqual(quiet,later,id+' reduced motion');
  if(['ferris_wheel','carousel','ufo'].includes(id))assert.deepEqual(quiet.art,a.art,id+' keeps real mechanism position');
 }
 for(const id of ['ferris_wheel','carousel','ufo'])assert.notDeepEqual(itemSprite(id,0,{state:state(.2)}).art,itemSprite(id,0,{state:state(1.1)}).art,id+' visible mechanical travel');
 for(const id of ['hot_air_balloon','bounce_house','magic_carpet']){
  const dry=state(),wet=state();dry.excursion.inflation=1;dry.excursion.cover=0;wet.excursion.inflation=.35;wet.excursion.cover=1;
  assert.notDeepEqual(itemSprite(id,0,{state:dry}).art,itemSprite(id,0,{state:wet}).art,id+' actual fabric change');
 }
});
test('optional invalid saved mechanisms cannot make malformed geometry or unbounded dirt loops',()=>{
 for(const id in BLUEPRINTS){
  const m=itemSprite(id,0,{state:{wetness:Infinity,dirt:Infinity,condition:NaN,excursion:{phase:Infinity,wind_phase:NaN,wind:200,inflation:100,cover:-200,lights:null}}});
  assert(!m.clipped,id);assert(m.fills.every(f=>Number.isFinite(f.x+f.y+f.w)));
 }
});
test('gondolas remain upright while mounted around the full wheel and carousel ducks orbit their own poles',()=>{
 for(let n=0;n<100;n++){
  const a=itemSprite('ferris_wheel',0,{state:state(n/100*Math.PI*2)});
  assert.equal(a.anchors.cabins.length,8);
  for(const p of a.anchors.cabins)assert(Math.abs(((p.x-82)/62)**2+((p.y-7-55)/41)**2-1)<1e-9,'cabins stay on rim');
  const b=itemSprite('carousel',0,{state:state(n/100*Math.PI*2)});
  assert.equal(b.anchors.rides.length,6);
  for(const p of b.anchors.rides)assert(Math.abs(((p.x-74)/48)**2+((p.y-94)/8)**2-1)<1e-9,'carved mounts orbit central column');
 }
});
test('the live world binds mechanics to each physical copy and never follows Cheese',()=>{
 const s=scene({items:[{id:'ferris_wheel',instance:'a',x:35,y:28},{id:'ferris_wheel',instance:'b',x:90,y:28}],living:{ecology:{},objects:{ferris_wheel:state(5)},instances:{a:state(.1),b:state(1.2)}}});
 const w=new LivingWorld(),before=JSON.stringify(s);w.render(s,0,.1);
 const [a,b]=w.objects.filter(o=>o.id==='ferris_wheel');assert(a&&b);
 assert.notDeepEqual(a.art,b.art,'two real mechanism phases');assert.deepEqual(a.art,itemSprite('ferris_wheel',0,{state:s.living.instances.a}).art);
 assert.equal(JSON.stringify(s),before);
 s.duck.x+=30;w.render(s,500,.1);const moved=w.objects.filter(o=>o.id==='ferris_wheel');
 assert.deepEqual(moved.map(o=>[o.x,o.y,o.art]),[a,b].map(o=>[o.x,o.y,o.art]));
});
