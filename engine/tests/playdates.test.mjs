import test from 'node:test';
import assert from 'node:assert/strict';
import {PLAYDATES,playdatePose} from '../client/playdates.mjs';
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
import {GUEST_CAST} from '../client/visitor-rig.mjs';
import {DUCK_AGES} from '../client/duck-rig.mjs';
import {ridingGeometry} from '../client/playground-stage.mjs';
import {scene} from './scenes.mjs';
const items={seesaw:'toy_seesaw',sandbox:'toy_sandbox',ball:'toy_ball',trampoline:'toy_trampoline'};
function fixture(id,stage='adult',guest='friendly_goose',progress=.5){
 const spec=PLAYDATES[id],item=items[spec.family];
 const plan={kind:'item',target:item,phase:'act',progress:.7,elapsed:20,duration:30,destination:[60,24],company:{id,partner:guest,destination:[60,24],spot:[65,24],phase:'act',elapsed:spec.duration*progress,duration:spec.duration,mass:[stage==='hatchling'?.3:1,1.5],young:['hatchling','duckling','elder','legendary'].includes(stage)}};
 return scene({duck:{x:60,y:24,stage,state:'thinking',cosmetics:{}},visitor:{id:guest,x:65,y:24,state:'idle'},items:[{id:item,x:60,y:24}],living:{plan,ecology:{},objects:{},projects:[],garden:[],minds:{}}});
}
test('each shared toy score has distinct mechanical motion and bounded artwork',()=>{
 const signatures=[];
 for(const [id,spec]of Object.entries(PLAYDATES)){
  const rendered=[];
  for(let i=0;i<=40;i++){
   const s=fixture(id,'adult','friendly_goose',i/40),m=itemSprite(s.living.plan.target,i,{interaction:s.living.plan});
   assert.equal(m.clipped,false,id+' '+i);assert(m.art.every(r=>/^[ -~]*$/.test(r)));
   rendered.push(m.art.join('\n'));
   if(spec.family==='seesaw')assert(Math.abs((m.anchors.seat.y+m.anchors.partner.y)/2-20)<.01);
  }
  assert(new Set(rendered).size>4,id+' visibly changes');signatures.push(rendered.join('\n'));
 }
 assert.equal(new Set(signatures).size,Object.keys(PLAYDATES).length);
});
test('all hatched ages and all 48 visitors ride or help from distinct physical contact anchors',()=>{
 const w=new LivingWorld();
 for(const id of Object.keys(PLAYDATES))for(const age of DUCK_AGES.filter(a=>a.id!=='egg'))for(const guest of Object.keys(GUEST_CAST)){
  const s=fixture(id,age.id,guest),original=JSON.stringify(s),r=w.render(s,1,.03),home=r.objects.find(o=>o.riders);
  assert(home,id+' '+age.id+' '+guest);assert.equal(home.riders.length,2);
  assert(!r.characters.some(c=>c.cheese||c.id===guest));
  const positions=home.riders.map(p=>ridingGeometry(home,p.character,p.seat,p.inside,6,9));
  assert(positions.every(c=>!c.clipped&&Number.isFinite(c.x)&&Number.isFinite(c.y)));
  assert.notEqual(positions[0].x,positions[1].x);assert.equal(JSON.stringify(s),original);
 }
});
test('no partner, paused plans, invitations and removed copies cannot create a phantom shared performance',()=>{
 const w=new LivingWorld(),s=fixture('seesaw_gentle');
 for(const changed of [{...s,visitor:null},{...s,living:{...s.living,plan:{...s.living.plan,paused:true}}},{...s,items:[]},{...s,living:{...s.living,plan:{...s.living.plan,company:{...s.living.plan.company,phase:'approach'}}}}]){
  assert(!w.render(changed,1,.03).objects.some(o=>o.riders));
 }
 const duplicate={...s,items:[{id:'toy_seesaw',x:10,y:24},...s.items]};
 const r=w.render(duplicate,1,.03);assert.equal(r.objects.filter(o=>o.riders).length,1);assert.equal(r.objects.find(o=>o.riders).worldPosition[0],60);
});
test('reduced motion freezes both partners and the machine, while age and mass affect the real motion',()=>{
 const w=new LivingWorld();
 for(const id of Object.keys(PLAYDATES)){
  const a=fixture(id,'hatchling','friendly_goose',.25),b=fixture(id,'hatchling','friendly_goose',.75);
  assert.deepEqual(w.render({...a,motion:false},1,.03).objects,w.render({...b,motion:false},99,.03).objects,id);
 }
 const a=fixture('seesaw_rhythm').living.plan,b=structuredClone(a);b.company.mass=[.3,1.5];b.company.young=true;
 assert.notEqual(playdatePose(a).tilt,playdatePose(b).tilt);
});
