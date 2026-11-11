import test from 'node:test';import assert from 'node:assert/strict';
import {CREATIVE_BLUEPRINTS} from '../client/creative-workshop.mjs';
import {CREATIVE_ROUTINES,CREATIVE_CONTROLS,creativePose,creativeGeometry} from '../client/creative-routines.mjs';
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';import {scene} from './scenes.mjs';
const ages=['hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'];
const ids={scope:'telescope',easel:'easel',kite:'kite',fold:'paper_plane_design'};
test('four creative props contain bounded mechanical construction through every score',()=>{
 const unique=new Set();
 for(const id of Object.keys(CREATIVE_BLUEPRINTS)){unique.add(itemSprite(id,0).art.join('\n'));assert.deepEqual(itemSprite(id,0),itemSprite(id,999),id+' never operates from idle wall-clock time');}
 assert.equal(unique.size,4);
 for(const [id,s]of Object.entries(CREATIVE_ROUTINES))for(let i=0;i<=40;i++){
  const routine={id,elapsed:s.duration*i/40,wind:1,start:{...CREATIVE_CONTROLS,flight:.75,cover:1}},pose=creativePose(routine);
  const options={state:{creative:{strokes:12,motif:'winter'},wetness:.8,dirt:.8,condition:.3},pose:{creative:pose}},before=JSON.stringify(options);
  const model=itemSprite(ids[s.type],0,options);assert.equal(model.construction,'creative-v1');assert(!model.clipped,id+' '+i);
  assert(model.art.every((row,y)=>/^[ -~]*$/.test(row)&&row.length===model.width&&model.tones[y].length===model.width));
  assert(model.fills.every(f=>f.x>=0&&f.y>=0&&f.w>0&&f.x+f.w<=model.width&&f.y<model.art.length),id+' material bounds');
  assert.equal(JSON.stringify(options),before,'render cannot paint, focus, fold or grant a flight');
 }
});
test('paint layers, covers, focus and paper folds change real material instead of decorative particles',()=>{
 for(const motif of ['pond','night','winter','autumn']){
  const signatures=new Set();for(let strokes=0;strokes<=12;strokes++)signatures.add(JSON.stringify(itemSprite('easel',0,{state:{creative:{strokes,motif}}})));
  assert.equal(signatures.size,13,'each authored painting layer adds visible content');
 }
 for(const [id,a,b] of [['telescope',{aim:0,focus:0,cap:1},{aim:1,focus:1,cap:0}],['kite',{flight:0},{flight:1}],['paper_plane_design',{fold:0},{fold:1}],['easel',{cover:0},{cover:1}]])assert.notDeepEqual(itemSprite(id,0,{pose:{creative:a}}).art,itemSprite(id,0,{pose:{creative:b}}).art,id);
});
test('reduced motion suppresses flutter while retaining current physical controls',()=>{
 for(const [id,s]of Object.entries(CREATIVE_ROUTINES)){
  const work={id,elapsed:s.duration*.63,wind:.8,start:CREATIVE_CONTROLS},before=JSON.stringify(work),full=creativePose(work),quiet=creativePose(work,false);
  for(const key of Object.keys(CREATIVE_CONTROLS))assert.equal(full[key],quiet[key],id+' '+key);
  assert.equal(quiet.seconds,0);assert.equal(quiet.wind,0);assert.equal(JSON.stringify(work),before);
 }
});
test('all hatched ages keep their bodies intact and tools reach actual controls',()=>{
 let count=0;
 for(const stage of ages)for(const [id,s]of Object.entries(CREATIVE_ROUTINES))for(const f of [.2,.4,.6,.8]){
  const routine={id,elapsed:s.duration*f,wind:.5,start:CREATIVE_CONTROLS},pose=creativePose(routine),item=ids[s.type];
  const home={...itemSprite(item,0,{pose:{creative:pose}}),x:100,y:85,scale:itemWorldScale(item)};
  const c={...characterSprite({stage,state:'idle',facing:true,performance:{kind:'creative',routine}},0),x:90,y:85};
  const before=JSON.stringify({home,c}),staged=creativeGeometry(home,{character:c,inside:1},6,8);
  assert.equal(staged.character.scale,c.scale);assert(!c.clipped,stage+' '+id);assert(staged.points.concat(staged.supports).every(p=>Number.isFinite(p.x+p.y)));
  if(pose.contact===1)assert(Math.hypot(staged.tip.x-staged.target.x,staged.tip.y-staged.target.y)<1e-9);
  if(!['scope','easel'].includes(pose.type))assert.equal(staged.character.y*8,staged.ground);
  if(pose.type==='easel'&&pose.tool!=='none')assert(staged.supports.length&&staged.character.y*8<staged.ground,'painting has a supported working height');
  if(pose.look===1){const e=c.rig.eye;const ex=staged.character.x*6+(e.x+.5-c.anchorX)*staged.cw,ey=staged.character.y*8+(e.y+.5-c.groundRow)*staged.cw*1.5;assert(Math.abs(ex-staged.eyeTarget.x)<1e-8);assert(Math.abs(ey-staged.eyeTarget.y)<1e-8);assert(staged.supports.length,'eyepiece is reached using a visible support');}
  assert.equal(JSON.stringify({home,c}),before);count++;
 }
 assert.equal(count,ages.length*Object.keys(CREATIVE_ROUTINES).length*4);
});
test('placed copy selection and portable folding retain their physical origin',()=>{
 const plan={kind:'item',target:'easel',instance:'a',phase:'act',progress:.5,elapsed:8,duration:24,destination:[60,24],creative_work:{id:'paint_sky',elapsed:15,origin:[35,24],start:CREATIVE_CONTROLS}};
 const s=scene({items:[{id:'easel',instance:'a',x:60,y:24},{id:'easel',instance:'b',x:90,y:24}],living:{ecology:{},instances:{a:{creative:{strokes:3}},b:{creative:{strokes:0}}},objects:{},plan}}),world=new LivingWorld();
 world.render(s,0,.1);assert.equal(world.objects[0].creators.length,1);assert(!world.objects[1].creators);assert(!world.characters.some(c=>c.cheese));
 s.items[0].instance='replacement';world.render(s,1,.1);assert(!world.objects[0].creators);assert(world.characters.some(c=>c.cheese));
 s.items=[];s.living.plan={...plan,target:'paper_plane_design',instance:null,creative_work:{id:'fold_wings',elapsed:18,origin:[60,24],start:CREATIVE_CONTROLS}};
 s.living.objects={paper_plane_design:{creative:{fold:.6}}};world.render(s,0,.1);const paper=world.objects[0];assert(paper.creators.length===1&&paper.portable);
 s.living.plan.paused=true;s.duck.x+=30;world.render(s,99,.1);assert.equal(world.objects[0].x,paper.x);assert.deepEqual(world.objects[0].art,paper.art);
 s.living.plan=null;world.render(s,100,.1);assert(!world.objects.some(x=>x.id==='paper_plane_design'));
});

test('viewing stairs and painting decks remain stationary throughout acting and entry',()=>{
 for(const stage of ages)for(const [id,s]of Object.entries(CREATIVE_ROUTINES).filter(([,s])=>s.type==='scope'||s.type==='easel'&&s.tool!=='none')){
  let reference=null;
  for(const f of [.1,.2,.4,.5,.6,.7,.8,.9]){
   const routine={id,elapsed:s.duration*f,start:CREATIVE_CONTROLS},item=ids[s.type],pose=creativePose(routine);
   const home={...itemSprite(item,0,{pose:{creative:pose}}),x:90,y:85,scale:itemWorldScale(item)};
   const c={...characterSprite({stage,state:'idle',facing:true,performance:{kind:'creative',routine}},0),x:90,y:85};
   for(const inside of [.1,.4,.7,1]){
    const g=creativeGeometry(home,{character:c,inside},6,8),shape=JSON.stringify(g.supports);
    if(reference===null)reference=shape;else assert.equal(shape,reference,stage+' '+id+' fixed support');
    if(g.climbing&&s.type==='scope'&&inside===1)assert(g.character.y*8>=g.platform.y-1e-8&&g.character.y*8<=g.ground+1e-8);
   }
  }
 }
});
