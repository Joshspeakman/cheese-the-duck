import test from 'node:test';
import assert from 'node:assert/strict';
import {storyModel} from '../client/story-art.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
import {scene} from './scenes.mjs';

const story={id:'lost_duckling',asset:'baby_duck'};
test('the story duckling uses the full guest rig with feather fills and articulated poses',()=>{
 const poses=new Set();
 for(const state of ['walking','signature','quacking','sleeping'])for(const facing of [true,false])for(const t of [0,.3,.6,1.1]){
  const m=storyModel(story,{state,facing},t);
  assert.equal(m.design,'pond-cast');assert.equal(m.profileId,'lost_duckling');
  assert(m.fills.length>=8&&!m.clipped);assert(m.story&&!m.visitor);
  assert.equal(m.id,'story:lost_duckling');poses.add(m.art.join('\n'));
 }
 assert(poses.size>10);
 assert.deepEqual(storyModel(story,{state:'signature'},1,false),storyModel(story,{state:'signature'},40,false));
});
test('story world positions come from simulation and never follow Cheese during rendering',()=>{
 const s=scene({living:{ecology:{},projects:[],garden:[],story},storyActor:{storyId:story.id,x:33,y:19,state:'walking'}});
 const w=new LivingWorld(),before=JSON.stringify(s),get=s=>w.render(s,1,.03).characters.find(a=>a.story);
 const first=get(s),after=get({...s,duck:{...s.duck,x:100,y:39}});
 assert.deepEqual([first.x,first.y],w.project(s,33,19));assert.deepEqual([after.x,after.y],[first.x,first.y]);
 const moved=get({...s,storyActor:{...s.storyActor,x:43,y:25}});
 assert.deepEqual([moved.x,moved.y],w.project(s,43,25));
 assert.equal(JSON.stringify(s),before);
 const fallback=get({...s,storyActor:null}),other=get({...s,storyActor:null,duck:{...s.duck,x:2}});
 assert.deepEqual([fallback.x,fallback.y],[other.x,other.y]);
});
