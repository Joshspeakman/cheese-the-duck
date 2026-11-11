import test from 'node:test';
import assert from 'node:assert/strict';
import {BOTANICAL_BLUEPRINTS} from '../client/botanical-workshop.mjs';
import {itemSprite,itemWorldScale,itemProfile,itemFamily,catalog} from '../client/ultra-items.mjs';

test('61 botanical drawings stay bounded across season, age of plant, wind, wetness and light',()=>{
 const signatures=new Set();
 for(const [id,p] of Object.entries(BOTANICAL_BLUEPRINTS)){
  for(const season of ['spring','summer','fall','winter'])for(const hour of [3,12,21])for(const healthy of [false,true]){
   const opts={state:{growth:healthy?1:0,wetness:1,dirt:.7,condition:.3,botany:{moisture:healthy?.8:.02,health:healthy?1:.15,bloom:healthy?1:.1}},context:{season,hour,living:{ecology:{wind:1,snow:.8,insects:1}}}};
   const before=JSON.stringify(opts),m=itemSprite(id,hour/4,opts);
   assert.equal(m.construction,'botanical-v1');assert.equal(m.clipped,false,id+' '+season+' '+hour);
   assert(m.art.every((r,y)=>r.length===m.width&&m.tones[y].length===m.width&&/^[ -~]*$/.test(r)));
   assert(m.fills.every(f=>Number.isFinite(f.x+f.y+f.w)&&f.x>=0&&f.y>=0&&f.x+f.w<=m.width&&f.y<m.art.length),id+' fill bounds');
   assert.equal(JSON.stringify(opts),before,'drawing never mutates plant state');
   assert(m.anchors.contact&&m.anchors.entry,id+' actual contact points');
  }
  signatures.add(itemSprite(id,0).art.join('\n'));assert(itemWorldScale(id)>.6);
  const opts={motion:false,state:{wetness:.9},context:{season:'summer',living:{ecology:{wind:1,insects:1}}}};
  assert.deepEqual(itemSprite(id,0,opts),itemSprite(id,120,opts),id+' reduced motion');
 }
 assert.equal(signatures.size,61,'individual object silhouettes');
});
test('flowers and trees reflect real time, season, soil and health',()=>{
 for(const id of ['flower_tulip','dream_flower']){
  assert.notDeepEqual(itemSprite(id,0,{context:{hour:12}}).art,itemSprite(id,0,{context:{hour:23}}).art,id+' opens and closes');
 }
 assert.notDeepEqual(itemSprite('tree_oak',0,{context:{season:'spring'}}).art,itemSprite('tree_oak',0,{context:{season:'winter'}}).art,'deciduous winter branches');
 assert.notDeepEqual(itemSprite('fern',0,{state:{botany:{moisture:.02,health:.2}}}).art,itemSprite('fern',0,{state:{botany:{moisture:.8,health:1}}}).art,'thirst changes frond posture');
 const spring=itemSprite('tree_cherry',0,{context:{season:'spring'}}),summer=itemSprite('tree_cherry',0,{context:{season:'summer'}});
 assert(spring.fills.some(f=>f.tone==='p'));assert(!summer.fills.some(f=>f.tone==='p'),'summer crown is leaves rather than spring blossoms');
 assert.notEqual(itemSprite('golden_petal',0).panels.p,itemSprite('rose_petal',0).panels.p,'gold petal flesh is gold too');
});
test('lily pad has a genuine transparent notch and ingredient profiles do not grow or grant free food',()=>{
 const m=itemSprite('lily_pad',0),x=Math.round(m.width/2+18),y=Math.round(m.art.length/2+10);
 assert(!m.fills.some(f=>f.y===y&&f.x<=x&&f.x+f.w>x),'water remains visible through the notch');
 for(const id of Object.keys(BOTANICAL_BLUEPRINTS)){
  const item=catalog.find(i=>i.id===id),profile=itemProfile(item,itemFamily(id));
  if(item.category==='food')assert.equal(profile.kind,'food',id);
  else assert.equal(profile.kind,BOTANICAL_BLUEPRINTS[id].rooted?'plant':'keepsake',id);
 }
});
test('still ingredients do not perform fake operating loops and surface wear follows actual state',()=>{
 for(const id of ['corn','peas','grapes','leaf','berry','tulip_bulb']){
  assert.deepEqual(itemSprite(id,0).art,itemSprite(id,20).art,id+' idle specimen is still');
  const clean=itemSprite(id,0),wet=itemSprite(id,0,{state:{wetness:.8}}),dirty=itemSprite(id,0,{state:{dirt:.8}});
  assert.notDeepEqual(clean.art,wet.art,id+' surface dew');assert.notDeepEqual(clean.art,dirty.art,id+' actual dirt');
 }
 const healthy=itemSprite('fern',0),cracked=itemSprite('fern',0,{state:{condition:.3}});
 assert.notDeepEqual(healthy.art,cracked.art,'damage belongs to the pot');
});
test('garden model reflects current crop slots without inventing additional plants',()=>{
 const empty=itemSprite('garden_plot',0,{context:{living:{garden:[]}}});
 const state={garden:[{id:0,plant:'tomato',stage:'harvestable'},{id:1,plant:null,stage:'empty'}]};
 const planted=itemSprite('garden_plot',0,{context:{living:state}});
 assert.notDeepEqual(empty.art,planted.art);
 assert.equal(planted.art.join('\n').split('(o)').length-1,1,'one crop marker for one mature slot');
 const stages=['seed','sprout','growing','mature','withered'].map(stage=>itemSprite('garden_plot',0,{context:{living:{garden:[{id:0,plant:'mint',stage}]}}}));
 assert.equal(new Set(stages.map(s=>s.art.join('\n'))).size,5,'real seed, sprout, growth and withering states');
 assert.deepEqual(planted.anchors.gardenPlots,state.garden);
});
