import test from 'node:test';
import assert from 'node:assert/strict';
import {NEST_ROUTINES,NEST_COMPANY,nestPose} from '../client/nest-routines.mjs';
import {nestHelpGeometry} from '../client/nest-company.mjs';
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {GUEST_CAST} from '../client/visitor-rig.mjs';
import {DUCK_AGES} from '../client/duck-rig.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
import {scene} from './scenes.mjs';

test('all ages retain Cheese’s physical nest action while a companion responds',()=>{
 for(const [name,spec]of Object.entries(NEST_COMPANY))for(const core of spec.cores.length?spec.cores:['weave_rim'])for(const age of DUCK_AGES)for(const phase of [.15,.3,.5,.7,.9]){
  const base={id:core,elapsed:phase*NEST_ROUTINES[core].duration},work={...base,company:{id:name,role:'a'}};
  const a=nestPose(base),b=nestPose(work);
  for(const key of ['px','py','press','grip','u','v','show','turn'])assert.equal(a[key],b[key],name+' must not operate the same material twice');
  const character=characterSprite({stage:age.id,performance:{kind:'nest',routine:work}},0);
  assert.equal(character.clipped,false,age.id+' '+name);
 }
});

test('all 48 visitors fit their nest helper roles with short, connected rim contact',()=>{
 for(const [name,spec]of Object.entries(NEST_COMPANY))for(const [id,profile]of Object.entries(GUEST_CAST)){
  if(['butterfly','toad','duckling'].includes(profile.species)&&spec.track.some(p=>p.contact))continue;
  const core=spec.cores[0]||'weave_rim',left=spec.anchor==='left';
  for(const progress of [0,.15,.3,.5,.7,.9,1]){
   const routine={id:core,elapsed:progress*NEST_ROUTINES[core].duration,company:{id:name,role:'b'}};
   const source={id,facing:left,performance:{kind:'nest',routine}},character={...characterSprite(source,0,true),x:100,y:80};
   assert.equal(character.clipped,false,id+' '+name+' '+progress);
   if(spec.track.some(p=>p.contact))assert(character.grip&&character.workGripRest,id+' has a real articulated contact hand');
   else assert(!character.grip,id+' fans or observes without the extended holding pose');
   const home={...itemSprite('basic_nest',0),x:100,y:80,scale:itemWorldScale('basic_nest')};
   const staged=nestHelpGeometry(home,{character,inside:1},6,9);
   assert.equal(staged.character.scale,character.scale,'helper body is never resized to fit a prop');
   assert.equal(staged.character.y*9+(profile.species==='butterfly'?5*staged.ch:0),staged.ground,'feet remain on their own ground plane');
   if(staged.tip){
    assert(Math.hypot((staged.tip.x-staged.hand.x)/staged.cw,(staged.tip.y-staged.hand.y)/staged.ch)<7,id+' '+name+' has a short reach');
    if(staged.pose.contact===1)assert.deepEqual(staged.tip,staged.target,'wing touches the actual rim');
   }
   const later=characterSprite(source,100,true);
   for(const field of ['art','tones','fills'])assert.deepEqual(character[field],later[field],id+' helper uses only native time');
  }
 }
});

test('only arrived helpers are staged at the exact nest copy and Reduced Motion remains still',()=>{
 const core='weave_rim',routine={id:core,elapsed:8,company:{id:'weave_tension',role:'b'}};
 const r={actor:'friendly_goose',id:'basic_nest',instance:'chosen',destination:[65,24],spot:[75,25],phase:'inside',elapsed:3,routine};
 const s=scene({visitor:{id:r.actor,x:75,y:25,state:'idle'},items:[{id:r.id,instance:'other',x:12,y:24},{id:r.id,instance:'chosen',x:65,y:24}],living:{ecology:{},objects:{},projects:[],garden:[],minds:{nest_helpers:[r]}}});
 const w=new LivingWorld(),before=structuredClone(s),result=w.render(s,1,.1),home=result.objects.find(o=>o.instance==='chosen');
 assert.equal(home.nestHelpers.length,1);assert.equal(home.nestHelpers[0].character.performance.routine.company.role,'b');
 assert(!result.objects.find(o=>o.instance==='other').nestHelpers);assert(!result.characters.some(c=>c.id===r.actor));assert.deepEqual(s,before);
 for(const change of [{phase:'approach'},{instance:'missing'},{destination:[40,24]},{actor:'absent'}]){
  const changed=structuredClone(s);Object.assign(changed.living.minds.nest_helpers[0],change);
  assert(!new LivingWorld().render(changed,1,.1).objects.some(o=>o.nestHelpers));
 }
 const paused=structuredClone(s);paused.living.plan={paused:true};
 const resting=new LivingWorld().render(paused,1,.1);
 assert(!resting.objects.some(o=>o.nestHelpers),'a pause releases both actors from the contact presentation');
 assert(resting.characters.some(c=>c.id===r.actor),'paused helper remains at its own native world position');
 for(const id of Object.keys(GUEST_CAST)){
  const source=elapsed=>characterSprite({id,performance:{kind:'nest',routine:{...routine,elapsed},motion:false}},elapsed,true);
  for(const field of ['art','tones','fills','grip'])assert.deepEqual(source(3)[field],source(18)[field],id+' helper respects Reduced Motion');
 }
});
