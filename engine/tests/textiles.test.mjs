import test from 'node:test';import assert from 'node:assert/strict';
import {TEXTILE_BLUEPRINTS} from '../client/textile-workshop.mjs';
import {TEXTILE_ROUTINES,TEXTILE_CONTROLS,textilePose,textileGeometry} from '../client/textile-routines.mjs';
import {itemSprite,itemWorldScale,itemProfile} from '../client/ultra-items.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';import {scene} from './scenes.mjs';
const ages=['hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'];
const items=Object.entries(TEXTILE_BLUEPRINTS);
function work(id,f){return {id,elapsed:TEXTILE_ROUTINES[id].duration*f,start:{...TEXTILE_CONTROLS,roll:id==='mat_unroll'?1:.35},origin:[60,24]};}
test('thirteen distinct textile constructions stay bounded through their complete material motions',()=>{
 const signatures=new Set();let count=0;
 for(const [item,p]of items){
  signatures.add(itemSprite(item,0).art.join('\n'));assert.deepEqual(itemSprite(item,0),itemSprite(item,500),item+' does not operate from wall-clock time');
  assert.notEqual(itemProfile({id:item},'rug').material,'ceramic');
  for(const [id,spec]of Object.entries(TEXTILE_ROUTINES).filter(([,s])=>s.types.includes(p.type)))for(const f of [0,.1,.3,.5,.7,.9,1]){
   const options={state:{textile:{nap:.3,fringe:.2,tracks:[{u:.5,v:.6}],frost:.8},wetness:.8,dirt:.7},pose:{textile:textilePose(work(id,f))}},before=JSON.stringify(options),m=itemSprite(item,100,options);
   assert.equal(m.construction,'textile-v1');assert(!m.clipped,item+' '+id+' '+f);assert(m.art.every((row,y)=>/^[ -~]*$/.test(row)&&row.length===m.width&&m.tones[y].length===m.width));
   assert(m.fills.every(a=>a.x>=0&&a.y>=0&&a.w>0&&a.x+a.w<=m.width&&a.y<m.art.length),item+' '+id+' fill bounds');assert.equal(JSON.stringify(options),before);count++;
  }
 }
 assert.equal(signatures.size,13);assert(count>600);
});
test('persistent rolls, ties, loft, frost and impressions change real surfaces',()=>{
 for(const [id,a,b]of [['persian_rug',{roll:0},{roll:1}],['fabric_scrap',{roll:0},{roll:.7}],['thatch',{tie:0,spread:1},{tie:1,spread:.2}],['insulation',{loft:.1},{loft:1}],['grass_patch',{frost:0},{frost:1}],['grass_patch',{nap:.2},{nap:.8}],['moss_carpet',{nap:.1},{nap:1}],['persian_rug',{nap:.1},{nap:1}],['moss_carpet',{tracks:[]},{tracks:[{u:.5,v:.6}]}]])assert.notDeepEqual(itemSprite(id,0,{state:{textile:a}}).art,itemSprite(id,0,{state:{textile:b}}).art,id);
 for(const id of ['mat_roll','mat_unroll'])for(const initial of [0,.25,.75,1]){
  const w={id,elapsed:0,start:{roll:initial}};assert.equal(textilePose(w).roll,initial,'folding starts at the actual roll, without a jump');
  w.elapsed=TEXTILE_ROUTINES[id].duration;assert.equal(textilePose(w).roll,id==='mat_roll'?1:0);
 }
});
test('all hatched ages keep their own bodies and feet on the actual textile surface',()=>{
 let count=0;
 for(const stage of ages)for(const [id,s]of Object.entries(TEXTILE_ROUTINES))for(const f of [.2,.4,.6,.8]){
  const [item,p]=items.find(([,p])=>s.types.includes(p.type)),routine=work(id,f),pose=textilePose(routine),home={...itemSprite(item,0,{pose:{textile:pose}}),x:100,y:85,scale:itemWorldScale(item)};
  const c={...characterSprite({stage,state:'idle',facing:true,performance:{kind:'textile',routine}},0),x:100,y:85},before=JSON.stringify({home,c});
  assert(!c.clipped,stage+' '+id);const g=textileGeometry(home,{character:c,inside:1},6,8);
  assert.equal(g.character.scale,c.scale);assert(Math.abs(g.character.x*6-g.foot.x)<1e-9&&Math.abs(g.character.y*8-g.foot.y)<1e-9);
  assert(g.points.every(a=>Number.isFinite(a.x+a.y)));if(pose.contact===1)assert(Math.hypot(g.tip.x-g.target.x,g.tip.y-g.target.y)<1e-9);
  assert.equal(JSON.stringify({home,c}),before);count++;
 }
 assert.equal(count,896);
});
test('reduced motion retains actual material state and never acts on a different copy',()=>{
 for(const id of Object.keys(TEXTILE_ROUTINES)){
  const w=work(id,.63),full=textilePose(w),quiet=textilePose(w,false);
  for(const key of Object.keys(TEXTILE_CONTROLS))assert.equal(full[key],quiet[key]);
 }
 const plan={kind:'item',target:'persian_rug',instance:'a',phase:'act',progress:.5,elapsed:8,duration:24,destination:[60,24],textile_work:work('fringe_comb',.6)};
 const s=scene({items:[{id:'persian_rug',instance:'a',x:60,y:24},{id:'persian_rug',instance:'b',x:95,y:24}],living:{ecology:{},instances:{a:{textile:{}},b:{textile:{}}},objects:{},plan}}),world=new LivingWorld();
 world.render(s,0,.1);assert.equal(world.objects[0].textileUsers.length,1);assert(!world.objects[1].textileUsers);assert(!world.characters.some(c=>c.cheese));
 s.items[0].instance='replacement';world.render(s,1,.1);assert(!world.objects[0].textileUsers);assert(world.characters.some(c=>c.cheese));
 s.items=[];s.living.plan={...plan,target:'fabric_scrap',instance:null,textile_work:work('scrap_fold',.6)};s.living.objects={fabric_scrap:{textile:{}}};world.render(s,1,.1);const x=world.objects[0].x;
 s.living.plan.paused=true;s.duck.x+=20;world.render(s,100,.1);assert.equal(world.objects[0].x,x,'portable material remains where it was put down');
});
