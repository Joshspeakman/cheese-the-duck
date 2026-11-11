import test from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {NEST_ROUTINES,NEST_IDS,nestPose} from '../client/nest-routines.mjs';
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';
import {duckRig,DUCK_AGES} from '../client/duck-rig.mjs';
import {occupiedGeometry,heldNestGeometry} from '../client/residence-stage.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
import {scene} from './scenes.mjs';
const hash=value=>createHash('sha256').update(value).digest('hex');
const plan=(id,key,p)=>({kind:'rest',target:id,phase:'act',progress:.7,residence:{destination:[65,24],routine:{id:key,elapsed:NEST_ROUTINES[key].duration*p}}});

test('authored nest scores have distinct visible character/object motion, printable ink and bounded contacts',()=>{
 for(const id of NEST_IDS){
  const signatures=new Map();
  for(const [key,spec]of Object.entries(NEST_ROUTINES)){
   assert(spec.duration>=10&&spec.duration<=30,key);assert.equal(spec.track[0].at,0);assert.equal(spec.track.at(-1).at,1);
   assert(spec.track.every((k,i)=>!i||k.at>spec.track[i-1].at));
   const frames=[];
   for(let n=0;n<=24;n++){
    const activity=plan(id,key,n/24),routine=activity.residence.routine;
    const m=itemSprite(id,900,{interaction:activity,context:{season:'summer',hour:12}});
    assert.equal(m.clipped,false,id+' '+key+' '+n);
    assert(m.art.every((r,y)=>r.length===m.tones[y].length&&/^[ -~]*$/.test(r)));
    assert(m.anchors.seat.x>0&&m.anchors.seat.x<m.width&&m.anchors.seat.y<m.art.length);
    const d=duckRig({stage:'adult',performance:{kind:'nest',routine}},0);
    assert.equal(d.clipped,false,key);
    frames.push(hash(m.art.join('\n')+(m.held?.art.join('\n')||'')+d.art.join('\n')));
    assert.equal(m.held?.clipped||false,false);
   }
   assert(new Set(frames).size>=5,id+' '+key+' changes actual rendered glyphs');
   const signature=hash(frames.join(':'));
   assert(!signatures.has(signature),`${key} duplicates ${signatures.get(signature)}`);
   signatures.set(signature,key);
  }
 }
});
test('nest acting preserves all age rigs, and front layers occlude only the nest rim and loose materials',()=>{
 for(const age of DUCK_AGES)for(const [key,spec]of Object.entries(NEST_ROUTINES))for(const p of [0,.2,.4,.6,.8,1]){
  const routine={id:key,elapsed:spec.duration*p},d=duckRig({stage:age.id,performance:{kind:'nest',routine}},200);
  assert.equal(d.clipped,false,key+' '+age.id);assert.equal(d.design,'d10');
  if(d.rig){
   const headEnd=d.rig.faceBounds.y+d.rig.faceBounds.h-1,neck=d.rig.neck.y;
   for(let y=headEnd+1;y<neck;y++)assert(d.fills.some(f=>f.y===y&&f.tone==='g'),'connected neck '+age.id+' '+key);
  }
 }
 const activity=plan('cozy_nest','sweep_crumbs',.48),m={...itemSprite('cozy_nest',0,{interaction:activity}),scale:itemWorldScale('cozy_nest'),x:100,y:80};
 const d={...duckRig({stage:'hatchling',performance:{kind:'nest',routine:activity.residence.routine}},0),x:100,y:80};
 const g=occupiedGeometry(m,d,1,6,9);
 assert(g.front.art.some((r,y)=>y<m.anchors.rim&&r.trim()),'swept crumbs are drawn in front of the occupant');
 assert(g.front.fills.every(f=>f.y>=m.anchors.rim),'front backdrop cannot hide the whole duck');
 assert(g.character.scale<=d.scale);
 for(const age of DUCK_AGES.filter(a=>a.id!=='egg')){
  const interaction=plan('basic_nest','lift_loose_twig',.4);
  const home={...itemSprite('basic_nest',0,{interaction}),scale:itemWorldScale('basic_nest'),x:100,y:80};
  const character={...duckRig({stage:age.id,performance:{kind:'nest',routine:interaction.residence.routine}},0),x:100,y:80};
  const staged=occupiedGeometry(home,character,1,6,9),held=heldNestGeometry(home,staged.character,6,9);
  assert(held,'held twig uses a real bill contact for '+age.id);
  assert.deepEqual(held.contact,held.bill,age.id+' twig stays on the posed bill');
  assert.equal(home.foreground,null,'no duplicate twig remains on the nest');
 }
});
test('routine snapshots are deterministic and reduced motion stays still across wall clocks and score phases',()=>{
 for(const id of NEST_IDS)for(const key of Object.keys(NEST_ROUTINES)){
  const a=plan(id,key,.2),b=plan(id,key,.8);
  assert.deepEqual(itemSprite(id,1,{interaction:a,motion:false}),itemSprite(id,100,{interaction:b,motion:false}));
  const duck=r=>duckRig({stage:'hatchling',performance:{kind:'nest',routine:r,motion:false}},80);
  for(const field of ['art','tones','fills','rig'])assert.deepEqual(duck(a.residence.routine)[field],duck(b.residence.routine)[field]);
  const moving=itemSprite(id,1,{interaction:a});
  assert.deepEqual(moving,itemSprite(id,100,{interaction:a}),'wall clock cannot advance a nest routine');
 }
 assert.equal(nestPose({id:'unrecognized'}),null);
});
test('live scenes stage only the arrived matching nest and feed its exact score to Cheese',()=>{
 const activity=plan('cozy_nest','fluff_center',.6),world=new LivingWorld();
 const s=scene({items:[{id:'cozy_nest',x:12,y:24},{id:'cozy_nest',x:65,y:24}],living:{ecology:{},plan:activity,objects:{},projects:[],garden:[]}});
 const r=world.render(s,300,.03),occupied=r.objects.filter(o=>o.occupant);
 assert.equal(occupied.length,1);assert.equal(occupied[0].worldPosition[0],65);
 assert.deepEqual(occupied[0].occupant.character.performance.routine,activity.residence.routine);
 assert.equal(r.objects.find(o=>o.worldPosition?.[0]===12).foreground,null,'another copy must not act out the same routine');
 assert(!r.characters.some(c=>c.cheese));
 const paused=world.render({...s,living:{...s.living,plan:{...activity,paused:true}}},300,.03);
 assert(!paused.objects.some(o=>o.occupant));assert(paused.characters.some(c=>c.cheese));
});
