import test from 'node:test';
import assert from 'node:assert/strict';
import {WATER_ROUTINES,waterPose,waterGeometry} from '../client/water-routines.mjs';
import {DUCK_AGES} from '../client/duck-rig.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
import {scene} from './scenes.mjs';
const ITEM={shallow_steps:'pool_kiddie',paddle_loop:'pool_large',lazy_drift:'pool_large',wing_rinse:'bird_bath',bubble_soak:'hot_tub',steam_stretch:'hot_tub_deluxe',watch_koi:'koi_pond',small_sips:'water_bowl',fountain_rings:'fountain_small',catch_spray:'sprinkler',spray_dash:'sprinkler_system',cascade_listen:'waterfall',rain_rings:'pond',moon_reflection:'pond',ripple_watch:'birdbath',ice_inspect:'pond'};
export function fixture(id,stage,progress){
 const target=ITEM[id],spec=WATER_ROUTINES[id];
 return scene({duck:{x:60,y:24,stage,state:'thinking'},items:[{id:target,x:60,y:24}],living:{plan:{kind:'item',target,phase:'act',progress:.7,elapsed:20,duration:30,destination:[60,24],water_routine:{id,elapsed:progress*spec.duration,done:false,label:spec.label}},ecology:{},objects:{},projects:[],garden:[],minds:{}}});
}
test('sixteen water scores articulate every hatched age within bounds and keep contact inside the actual object',()=>{
 const world=new LivingWorld(),signatures=new Set();
 for(const id of Object.keys(WATER_ROUTINES)){
  let signature=[];
  for(const age of DUCK_AGES)for(let n=0;n<=32;n++){
   const s=fixture(id,age.id,n/32),before=JSON.stringify(s),result=world.render(s,n,.03),home=result.objects.find(o=>o.bather);
   if(age.id==='egg'){assert.equal(home,undefined);continue;}
   assert(home,id+' '+age.id);const b=home.bather;assert.equal(b.character.clipped,false,id+' '+age.id+' '+n);
   assert(b.seat.x>=0&&b.seat.x<home.width&&b.seat.y>=0&&b.seat.y<home.art.length,id+' support');
   assert.equal(home.clipped,false);assert.equal(JSON.stringify(s),before);
   assert.equal(result.characters.filter(c=>c.cheese).length,0,'one actual Cheese');
   if(age.id==='adult')signature.push([b.character.art,b.seat,b.pose.splash]);
  }
  signatures.add(JSON.stringify(signature));
 }
 assert.equal(signatures.size,16);
});
test('bathing needs the real matching item and pauses without leaving a duplicate swimmer',()=>{
 const world=new LivingWorld();
 for(const change of [s=>s.items=[],s=>s.living.plan.paused=true,s=>s.living.plan.phase='approach',s=>s.living.plan.water_routine.done=true,s=>s.items[0].x=90]){
  const s=fixture('paddle_loop','adult',.5);change(s);const result=world.render(s,1,.03);
  assert(!result.objects.some(o=>o.bather));assert.equal(result.characters.filter(c=>c.cheese).length,1);
 }
 const s=fixture('paddle_loop','adult',.5);s.items.push({id:'pool_large',x:90,y:24});
 assert.equal(world.render(s,1,.03).objects.filter(o=>o.bather).length,1);
});
test('reduced motion freezes the complete water pose, and each bill reaches the bowl on a sip',()=>{
 const world=new LivingWorld();
 for(const id of Object.keys(WATER_ROUTINES)){
  const models=[.15,.5,.83].map(p=>{const s=fixture(id,'adult',p);s.motion=false;const b=world.render(s,p*100,.03).objects.find(o=>o.bather).bather;const {performance,...character}=b.character;return {...b,character};});
  assert.deepEqual(models[0],models[1]);assert.deepEqual(models[1],models[2]);
 }
 for(const age of DUCK_AGES.filter(a=>a.id!=='egg')){
  const s=fixture('small_sips',age.id,.4),home=world.render(s,1,.03).objects.find(o=>o.bather),c=waterGeometry(home,home.bather,6,9).character;
  const cu=6*c.scale,hu=6*home.scale*home.detailScale;
  const bx=c.x*6+(c.bill.x+.5-c.anchorX+(c.offsetX||0))*cu,by=c.y*9+(c.bill.y+.5-c.groundRow)*cu*1.5+(c.offsetY||0)*cu;
  const tx=home.x*6+(home.anchors.contact.x+.5-home.width/2)*hu,ty=home.y*9+(home.anchors.contact.y+.5-home.art.length)*hu*1.5;
  assert(Math.abs(bx-tx)<.001&&Math.abs(by-ty)<.001,age.id+' bill meets water');
 }
});
