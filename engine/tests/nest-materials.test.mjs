import test from 'node:test';
import assert from 'node:assert/strict';
import {nestMaterials} from '../client/nest-materials.mjs';
import {NEST_ROUTINES,NEST_IDS} from '../client/nest-routines.mjs';
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {GUEST_CAST} from '../client/visitor-rig.mjs';
import {DUCK_AGES} from '../client/duck-rig.mjs';
import {occupiedGeometry} from '../client/residence-stage.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
import {scene} from './scenes.mjs';

test('each physical bedding change is visible without a running performance',()=>{
 for(const id of NEST_IDS){
  const defaults=nestMaterials(),before=itemSprite(id,0,{state:{nest:defaults}});
  for(const [key,value]of Object.entries(defaults)){
   const state={nest:{...defaults,[key]:value<.5?1:0}},copy=structuredClone(state);
   const model=itemSprite(id,0,{state});
   assert.notDeepEqual([model.art,model.tones],[before.art,before.tones],id+' '+key+' remains visible after leaving');
   assert.equal(model.clipped,false,id+' '+key);
   assert.deepEqual(state,copy,'drawing does not change '+key);
   assert.deepEqual(model,itemSprite(id,90,{state}),'native bedding does not animate from wall time');
  }
 }
});

test('contact events refer to actual bedding and are ordered within an authored routine',()=>{
 const keys=new Set(Object.keys(nestMaterials()));
 for(const [id,spec]of Object.entries(NEST_ROUTINES)){
  let last=0;
  for(const event of spec.contacts||[]){
   assert(event.at>last&&event.at<1,id);last=event.at;
   for(const kind of ['set','add','multiply'])for(const [key,v]of Object.entries(event[kind]||{})){
    assert(keys.has(key),id+' '+key);assert(Number.isFinite(v),id);
   }
   assert(spec.track.some(k=>k.at===event.at),id+' contact corresponds to a physical keyframe');
  }
 }
});

test('guest bodies keep their own pose clock, nest copy and seat while Cheese is elsewhere',()=>{
 const id='deluxe_nest',guest={id:'friendly_goose',x:65,y:24,state:'idle'};
 const routine={id:'rain_listen',elapsed:9,done:false};
 const r={actor:guest.id,id,instance:'occupied',destination:[65,24],slot:0,capacity:2,phase:'inside',elapsed:12,routine};
 const s=scene({visitor:guest,items:[{id,instance:'empty',x:12,y:24},{id,instance:'occupied',x:65,y:24}],living:{ecology:{},objects:{},projects:[],garden:[],minds:{residences:[r]}}});
 const copy=structuredClone(s),world=new LivingWorld(),result=world.render(s,1,.1);
 const home=result.objects.find(o=>o.instance==='occupied'),other=result.objects.find(o=>o.instance==='empty');
 assert.equal(home.occupants.length,1);
 assert.deepEqual(home.occupants[0].character.performance.routine,routine);
 assert(home.foreground.art.some(row=>row.trim()),'the guest’s rain observation has its own foreground');
 assert.equal(other.foreground,null);assert(!other.occupants);
 assert.deepEqual(s,copy,'presentation never changes simulation clocks');
 const reduced={...s,motion:false};
 const first=new LivingWorld().render(reduced,1,.1).objects;
 const changed=structuredClone(reduced);changed.living.minds.residences[0].routine.elapsed=19;
 const second=new LivingWorld().render(changed,50,.1).objects;
 for(let i=0;i<first.length;i++){
  for(const field of ['art','tones','fills','anchors','foreground'])assert.deepEqual(first[i][field],second[i][field],'reduced motion freezes '+field);
  for(const field of ['art','tones','fills','rig','x','y'])assert.deepEqual(first[i].occupants?.[0].character[field],second[i].occupants?.[0].character[field],'reduced motion freezes guest '+field);
 }
});

test('every visitor and every Cheese age fits a steady nest seat through the full score repertoire',()=>{
 const home={...itemSprite('deluxe_nest',0,{interaction:{shared:true}}),x:100,y:80,scale:itemWorldScale('deluxe_nest')};
 for(const source of [...DUCK_AGES.map(a=>({stage:a.id})),...Object.keys(GUEST_CAST).map(id=>({id}))]){
  const scales=new Set();
  for(const [id,spec]of Object.entries(NEST_ROUTINES))for(const phase of [.25,.5,.75]){
   const character={...characterSprite({...source,facing:true,performance:{kind:'nest',routine:{id,elapsed:spec.duration*phase}}},0,Boolean(source.id)),x:100,y:80,cheese:!source.id};
   assert.equal(character.clipped,false,(source.id||source.stage)+' '+id);
   const staged=occupiedGeometry(home,character,1,6,9,0);
   scales.add(staged.character.scale);
   assert(staged.character.scale>0&&staged.character.scale<=character.scale);
   assert(Number.isFinite(staged.character.x)&&Number.isFinite(staged.character.y));
  }
  assert.equal(scales.size,1,(source.id||source.stage)+' does not change size during gestures');
 }
});

test('all visitor nest details obey the native clock and Reduced Motion',()=>{
 for(const id of Object.keys(GUEST_CAST))for(const kind of ['rain_listen','cold_huddle','noon_doze']){
  const performance={kind:'nest',routine:{id:kind,elapsed:8}};
  const a=characterSprite({id,performance},1,true),b=characterSprite({id,performance},29,true);
  for(const field of ['art','tones','fills','bill','phase'])assert.deepEqual(a[field],b[field],id+' '+kind+' '+field+' uses native elapsed time');
  const reduced=elapsed=>characterSprite({id,performance:{...performance,motion:false,routine:{id:kind,elapsed}}},elapsed*7,true);
  for(const field of ['art','tones','fills','bill','phase'])assert.deepEqual(reduced(3)[field],reduced(19)[field],id+' Reduced Motion '+field);
 }
});
