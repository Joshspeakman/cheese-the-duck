import test from 'node:test';import assert from 'node:assert/strict';
import {GROUND_BLUEPRINTS,groundPoint} from '../client/ground-workshop.mjs';
import {GROUND_ROUTINES,GROUND_CONTROLS,groundPose,groundGeometry} from '../client/ground-routines.mjs';
import {itemSprite,itemWorldScale,itemProfile} from '../client/ultra-items.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';import {scene} from './scenes.mjs';
const ages=['hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'],items=Object.entries(GROUND_BLUEPRINTS);
const work=(id,f)=>({id,elapsed:GROUND_ROUTINES[id].duration*f,origin:[60,24]});
test('eighteen rebuilt surfaces have bounded printable anatomy and material-specific contact poses',()=>{
 const signatures=new Set();let cases=0;
 for(const [item,p]of items){
  signatures.add(itemSprite(item,0).art.join('\n'));assert.deepEqual(itemSprite(item,0),itemSprite(item,500),item+' cannot advance native material time');
  assert.equal(itemProfile({id:item},'tile').material,p.material);
  for(const [id,spec]of Object.entries(GROUND_ROUTINES).filter(([,s])=>s.types.includes(p.type)))for(const f of [0,.1,.3,.5,.7,.9,1]){
   const options={state:{ground:{powder:.2,phase:7,frost:.8,tracks:[{u:.5,v:.5,life:1}],furrows:[{v:.5,life:1}]},wetness:.8,dirt:.7},pose:{ground:groundPose(work(id,f))}},before=JSON.stringify(options),m=itemSprite(item,100,options);
   assert.equal(m.construction,'ground-v1');assert(!m.clipped,item+' '+id+' '+f);
   assert(m.art.every((row,y)=>/^[ -~]*$/.test(row)&&row.length===m.width&&m.tones[y].length===m.width));
   assert(m.fills.every(a=>a.x>=0&&a.y>=0&&a.w>0&&a.x+a.w<=m.width&&a.y<m.art.length),item+' '+id+' fills');assert.equal(JSON.stringify(options),before);cases++;
  }
 }
 assert.equal(signatures.size,18);assert(cases>700);
});
test('saved footprints, rake lines, powder, frost and native magical phase affect the actual surfaces',()=>{
 for(const [id,a,b]of [['sand_floor',{tracks:[]},{tracks:[{u:.5,v:.6,life:1}]}],['sand_floor',{furrows:[]},{furrows:[{v:.6,life:1}]}],['snow_floor',{powder:.1},{powder:1}],['stone_tiles',{frost:0},{frost:1}],['cloud_floor',{phase:0},{phase:3}],['lava_floor',{phase:0},{phase:3}],['galaxy_floor',{phase:0},{phase:3}]])assert.notDeepEqual(itemSprite(id,0,{state:{ground:a}}).art,itemSprite(id,0,{state:{ground:b}}).art,id);
 for(const id of ['cloud_floor','lava_floor','galaxy_floor'])assert.deepEqual(itemSprite(id,0,{motion:false,state:{ground:{phase:0}}}),itemSprite(id,0,{motion:false,state:{ground:{phase:3}}}),id+' reduced motion freezes decorative movement');
});
test('all hatched bodies keep their original scale and reach the selected physical contact',()=>{
 let count=0;
 for(const stage of ages)for(const [id,spec]of Object.entries(GROUND_ROUTINES))for(const f of [.2,.4,.6,.8]){
  const [item]=items.find(([,p])=>spec.types.includes(p.type)),routine=work(id,f),pose=groundPose(routine),home={...itemSprite(item,0,{pose:{ground:pose}}),x:100,y:85,scale:itemWorldScale(item)};
  const c={...characterSprite({stage,state:'idle',facing:true,performance:{kind:'ground',routine}},0),x:100,y:85},before=JSON.stringify({home,c});
  assert(!c.clipped,stage+' '+id);const g=groundGeometry(home,{character:c,inside:1},6,8);
  assert.equal(g.character.scale,c.scale);assert(Math.abs(g.character.x*6-g.foot.x)<1e-9&&Math.abs(g.character.y*8-g.foot.y)<1e-9);
  assert(g.points.every(a=>Number.isFinite(a.x+a.y)));if(pose.contact===1)assert(Math.hypot(g.tip.x-g.target.x,g.tip.y-g.target.y)<1e-9);
  assert.equal(JSON.stringify({home,c}),before);count++;
 }
 assert.equal(count,1024);
});
test('lava observers stay outside the lip, and path contact points match their authored stones',()=>{
 for(let i=0;i<=100;i++)assert(groundPose(work('lava_edge',i/100)).v>=1.1);
 for(const [id,points]of [['stone_cross',[[.16,.22,.67],[.34,.4,.5],[.55,.6,.62],[.78,.78,.4]]],['winding_walk',[[.14,.13,.67],[.3,.31,.47],[.46,.5,.57],[.62,.69,.39],[.8,.87,.55]]]])for(const [f,u,v]of points){const pose=groundPose(work(id,f));assert(Math.abs(pose.u-u)<1e-9&&Math.abs(pose.v-v)<1e-9);}
 const p=GROUND_BLUEPRINTS.lava_floor;assert(groundPoint(p,.5,1.1).y>groundPoint(p,.5,1).y);
});
test('reduced motion retains physical contact and copy identities survive replacement and pause',()=>{
 for(const id of Object.keys(GROUND_ROUTINES)){
  const w=work(id,.63),full=groundPose(w),quiet=groundPose(w,false);
  for(const key of [...Object.keys(GROUND_CONTROLS),'contact'])assert.equal(full[key],quiet[key]);
 }
 const plan={kind:'item',target:'sand_floor',instance:'a',phase:'act',progress:.5,elapsed:8,duration:24,destination:[60,24],ground_work:work('sand_rake',.6)};
 const s=scene({items:[{id:'sand_floor',instance:'a',x:60,y:24},{id:'sand_floor',instance:'b',x:95,y:24}],living:{ecology:{},instances:{a:{ground:{}},b:{ground:{}}},objects:{},plan}}),world=new LivingWorld();
 world.render(s,0,.1);assert.equal(world.objects[0].groundUsers.length,1);assert(!world.objects[1].groundUsers);assert(!world.characters.some(c=>c.cheese));
 s.items[0].instance='replacement';world.render(s,1,.1);assert(!world.objects[0].groundUsers);assert(world.characters.some(c=>c.cheese));
 s.items=[];s.living.plan={...plan,target:'wooden_plank',instance:null,ground_work:work('wood_grain',.6)};s.living.objects={wooden_plank:{ground:{}}};world.render(s,1,.1);const x=world.objects[0].x;
 s.living.plan.paused=true;s.duck.x+=20;world.render(s,100,.1);assert.equal(world.objects[0].x,x,'crafting plank stays where placed for inspection');
});
