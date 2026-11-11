import test from 'node:test';import assert from 'node:assert/strict';
import {KEEPSAKE_BLUEPRINTS} from '../client/keepsake-workshop.mjs';
import {KEEPSAKE_ROUTINES,keepsakePose,keepsakeGeometry} from '../client/keepsake-routines.mjs';
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';import {scene} from './scenes.mjs';
const ages=['egg','hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'];
test('all fifteen keepsakes have distinct printable construction and bounded moving parts',()=>{
 const signatures=new Set();
 for(const id of Object.keys(KEEPSAKE_BLUEPRINTS)){
  signatures.add(itemSprite(id,0).art.join('\n'));assert(itemWorldScale(id)>.45);
  for(const [key,spec]of Object.entries(KEEPSAKE_ROUTINES))for(const t of [0,.15,.3,.5,.68,.9,1]){
   const work={id:key,elapsed:spec.duration*t,start_open:0},options={state:{keepsake:{litres:60,page:5,frozen:true},wetness:.8,dirt:.8,condition:.3},pose:{keepsake:keepsakePose(work)}};
   const before=JSON.stringify(options),m=itemSprite(id,0,options);
   assert.equal(m.construction,'keepsake-v1');assert.equal(m.clipped,false,id+' '+key+' '+t);
   assert(m.art.every((s,i)=>s.length===m.width&&m.tones[i].length===m.width&&/^[ -~]*$/.test(s)));
   assert(m.fills.every(f=>Number.isFinite(f.x+f.y+f.w)&&f.x>=0&&f.y>=0&&f.x+f.w<=m.width&&f.y<m.art.length),id+' surface bounds');
   assert.equal(JSON.stringify(options),before,'rendering never changes pages or water');
  }
 }
 assert.equal(signatures.size,15);
});
test('opening, sorting, folding and turning are driven by contact instead of idle timers',()=>{
 for(const id of ['treasure_chest','storage_chest','weekly_chest','storage_basket','rain_barrel','friendship_card','storm_sketch','pirate_map','ancient_tome','duck_photo','sunset_photo','picture_frame']){
  const still=itemSprite(id,0);assert.deepEqual(still,itemSprite(id,500),id+' stays physically still without action');
  const handled=itemSprite(id,0,{pose:{keepsake:{open:1,sort:1,turn:.5,fold:0,wipe:.7}}});
  const closed=itemSprite(id,0,{pose:{keepsake:{open:0,sort:0,turn:0,fold:1,wipe:0}}});
  assert.notDeepEqual(handled.art,closed.art,id+' has an actual changed surface or moving part');
 }
 const open=itemSprite('storm_sketch',0,{state:{keepsake:{open:1}}}),folded=itemSprite('storm_sketch',0,{state:{keepsake:{open:0}}});
 const top=m=>m.art.findIndex(r=>r.trim());assert(top(folded)>top(open)+15,'folded paper physically occupies less space');
 const a=itemSprite('ancient_tome',0,{state:{keepsake:{page:0,open:1}}}),b=itemSprite('ancient_tome',0,{state:{keepsake:{page:3,open:1}}});
 assert.notDeepEqual(a.art,b.art,'saved page selects real chapter content');
});
test('reduced motion freezes gestures without mutating native opening state',()=>{
 for(const [id,spec]of Object.entries(KEEPSAKE_ROUTINES)){
  const work={id,elapsed:spec.duration*.2,start_open:.7},before=JSON.stringify(work);
  assert.deepEqual(keepsakePose(work,false),keepsakePose({...work,elapsed:spec.duration*.9},false));assert.equal(JSON.stringify(work),before);
 }
});
test('every age stays grounded and reading tools meet real page anchors',()=>{
 for(const stage of ages)for(const [id,spec]of Object.entries(KEEPSAKE_ROUTINES)){
  const routine={id,elapsed:spec.duration*.3,start_open:0};
  const home={...itemSprite('ancient_tome',0,{pose:{keepsake:keepsakePose(routine)}}),scale:.52,x:110,y:85};
  const character={...characterSprite({stage,state:'idle',facing:true,performance:{kind:'keepsake',routine,motion:true}},2),x:100,y:85};
  const staged=keepsakeGeometry(home,{character,inside:1},6,8);
  assert(Math.abs(staged.character.y*8-staged.ground)<1e-9,stage+' grounded');
  assert(staged.points.every(p=>Number.isFinite(p.x+p.y)));assert.equal(staged.character.scale,character.scale,'does not stretch a young character to reach');
  if(keepsakePose(routine).contact===1)assert(Math.hypot(staged.tip.x-staged.target.x,staged.tip.y-staged.target.y)<1e-9);
 }
});
test('portable reading stays at the original spot across pausing and camera movement',()=>{
 const s=scene({items:[],structures:[],living:{objects:{ancient_tome:{keepsake:{open:1,page:3}}},ecology:{},plan:{kind:'item',target:'ancient_tome',phase:'act',progress:.5,elapsed:8,duration:16,keepsake_work:{id:'book_leaf',elapsed:14,origin:[60,24],start_open:0}}}});
 const w=new LivingWorld();w.render(s,0,.1);const book=w.objects.find(o=>o.id==='ancient_tome'),actor=book.keepers[0].character;
 assert(book.portable&&book.keepers.length===1);assert(!w.characters.some(c=>c.cheese),'staged Cheese replaces the ordinary sprite');
 s.living.plan.paused=true;s.duck.x+=20;w.render(s,30,.1);const paused=w.objects.find(o=>o.id==='ancient_tome');
 assert.equal(paused.x,book.x,'book does not follow Cheese across the pond');assert.deepEqual(paused.art,book.art);assert.deepEqual(paused.keepers[0].character.art,actor.art);
 w.render({...s,camera:{...s.camera,x:10}},30,.1);assert.notEqual(w.objects.find(o=>o.id==='ancient_tome').x,book.x,'camera moves the whole scene');
 s.living.plan=null;w.render(s,31,.1);assert(!w.objects.some(o=>o.id==='ancient_tome'),'putting away a portable book removes it');
});
test('a physical chest interaction stays with its selected copy',()=>{
 const s=scene({items:[{id:'treasure_chest',instance:'a',x:60,y:24},{id:'treasure_chest',instance:'b',x:90,y:24}],living:{ecology:{},instances:{a:{keepsake:{open:1}},b:{keepsake:{open:0}}},objects:{},plan:{kind:'item',target:'treasure_chest',instance:'a',phase:'act',progress:.5,elapsed:8,duration:16,destination:[60,24],keepsake_work:{id:'coin_inspection',elapsed:12,start_open:0}}}});
 const w=new LivingWorld();w.render(s,0,.1);assert.equal(w.objects[0].keepers.length,1);assert(!w.objects[1].keepers);
 s.items[0].instance='replacement';w.render(s,1,.1);assert(!w.objects[0].keepers);assert(w.characters.some(c=>c.cheese));
});
