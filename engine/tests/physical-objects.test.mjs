import test from 'node:test';
import assert from 'node:assert/strict';
import {LivingWorld} from '../client/ultra-world.mjs';
import {scene} from './scenes.mjs';
import {layoutBounds,layoutCheck,PondArrangement} from '../client/pond-layout.mjs';
import footprints from '../client/animation/object-footprints.json' with {type:'json'};

test('two plants render their own persistent biology without changing snapshots',()=>{
 const living={ecology:{insects:0},objects:{fern:{growth:.5}},instances:{
  a:{growth:.4,condition:.5,dirt:.8,botany:{health:.4,moisture:.05,bloom:0}},
  b:{growth:.9,condition:1,dirt:0,botany:{health:1,moisture:.8,bloom:1}}}};
 const s=scene({items:[{id:'fern',instance:'a',x:30,y:20},{id:'fern',instance:'b',x:100,y:20}],living});
 const before=JSON.stringify(s),world=new LivingWorld();world.render(s,0,.1);
 assert.equal(JSON.stringify(s),before);
 const [a,b]=world.objects;assert.notDeepEqual(a.art,b.art);
 living.instances.a.botany.health=1;world.render(s,0,.1);
 assert.deepEqual(world.objects[1].art,b.art,'care for one plant cannot change its twin');
});

test('same-position replacement cannot inherit Cheese or a visitor performance',()=>{
 const s=scene({items:[{id:'toy_piano',instance:'new',x:60,y:24}],living:{ecology:{insects:0},instances:{new:{}},objects:{toy_piano:{}},
  plan:{kind:'item',target:'toy_piano',instance:'old',instrument:{slot:0,instance:'old'},phase:'act',duration:30,elapsed:15,destination:[60,24],music_score:{id:'first_keys',elapsed:2.2}},minds:{musicians:[]}}});
 const world=new LivingWorld();world.render(s,0,.1);
 assert.equal(world.objects.length,1,'removed copy is not conjured beside Cheese');
 assert(!world.objects[0].active&&!world.objects[0].musicians);assert(world.characters.some(c=>c.cheese));
 s.living.plan.instance='new';world.render(s,1,.1);assert.equal(world.objects[0].musicians.length,1);
 s.living.plan=null;s.visitor={id:'friend:frida',castId:'friend:frida',name:'Frida',x:59,y:24,state:'idle'};
 s.living.minds.musicians=[{actor:'friend:frida',id:'toy_piano',instance:'old',destination:[60,24],slot:0,phase:'inside',elapsed:0,score:{id:'first_keys',elapsed:2.1}}];
 world.render(s,2,.1);assert(!world.objects[0].musicians);assert(world.characters.some(c=>c.id==='friend:frida'));
 s.living.minds.musicians[0].instance='new';world.render(s,3,.1);assert.equal(world.objects[0].musicians[0].character.id,'friend:frida');
});

test('layout preview excludes only the moved copy from collision checks',()=>{
 const footprint=footprints.items.fern;
 const layout={items:[{id:'fern',footprint}],placed:[{id:'fern',instance:'a',x:5,y:3,box:layoutBounds(footprint,5,3)},
  {id:'fern',instance:'b',x:15,y:3,box:layoutBounds(footprint,15,3)}],obstacles:[]};
 assert(layoutCheck(layout,'fern',5,3,'a').ok);
 assert(!layoutCheck(layout,'fern',15,3,'a').ok,'same catalogue id still occupies space');
 assert(layoutCheck(layout,'fern',15,3,'b').ok);
 layout.copies=layout.placed.map(p=>({id:p.id,instance:p.instance,placed:true}));
 assert(!layoutCheck(layout,'fern',5,3,'gone').ok,'stale copy never substitutes an owned sibling');
 const arrangement=Object.create(PondArrangement.prototype);
 arrangement.journal={world:{layout}};
 arrangement.select('fern','gone');
 assert.equal(arrangement.instance,'gone','selection cannot silently retarget another copy');
 assert(!arrangement.verdict.ok);
});
