import test from 'node:test';
import assert from 'node:assert/strict';
import { characterSprite } from '../client/ultra-characters.mjs';
import { STAGES,ACTIONS,scruffySprite } from '../client/scruffy-sprites.mjs';
import {DUCK_AGES,duckRig} from '../client/duck-rig.mjs';
import { mirror } from '../client/ultra-art.mjs';
import { LivingWorld } from '../client/ultra-world.mjs';
import { scene } from './scenes.mjs';

test('live Cheese uses approved compact D10 art at every canonical age',()=>{
  const distinct=new Set();
  for(const stage of STAGES){
    const live=characterSprite({stage:stage.id,state:'idle'},0);
    assert.deepEqual(live.art,duckRig({stage:stage.id,state:'idle'},0).art,stage.id);
    assert.equal(live.design,'d10');assert.equal(live.groundRow,39.5);
    distinct.add(live.art.join('\n'));
  }
  assert.equal(distinct.size,9);
  assert.deepEqual(characterSprite({stage:'teen'},0),characterSprite({stage:'juvenile'},0));
  assert.deepEqual(characterSprite({stage:'unknown'},0),characterSprite({stage:'adult'},0));
});
test('real care, movement and custom states drive the selected animation cycles',()=>{
  const routes={idle:'idle',walking:'walking',waddle_fast:'walking',sneaking:'walking',playing:'dancing',
    petting:'idle',cleaning:'preening',eating:'eating',sleeping:'sleeping',swimming:'swimming',
    diving:'swimming',jumping:'hopping',flapping:'flapping',stretching:'flapping',quack:'quacking',
    singing:'quacking',napping:'sleeping',dancing:'dancing',splashing:'swimming',pecking:'eating'};
  for(const [state,action] of Object.entries(routes))assert.equal(characterSprite({state},.3).action,action,state);
  assert.notDeepEqual(characterSprite({state:'waddle_fast'},.3).art,characterSprite({state:'walking'},.3).art);
  assert.notDeepEqual(characterSprite({state:'diving'},.7).art,characterSprite({state:'swimming'},.7).art);
});
test('mood, love and cosmetics stay visible on the moving D10 character',()=>{
  const base={stage:'adult',state:'idle'},neutral=characterSprite(base,0).art;
  for(const mood of ['happy','sad','miserable','dramatic'])assert.notDeepEqual(characterSprite({...base,mood},0).art,neutral,mood);
  assert.ok(characterSprite({...base,state:'petting'},0).art.join('').includes('<3'));
  for(const cosmetics of [{hat:'hat_party'},{hat:'hat_crown'},{hat:'hat_chef'},{face:'glasses_nerd'},
    {neck:'scarf_red'},{body:'cape_superhero'},{hat:'hat_tophat',face:'glasses_cool',neck:'bowtie'}]){
    assert.notDeepEqual(characterSprite({...base,cosmetics},0).art,neutral);
    const right=characterSprite({...base,state:'walking',cosmetics},.3);
    const left=characterSprite({...base,state:'walking',cosmetics,facing:false},.3);
    assert.deepEqual(left.art,mirror(right.art));
    assert.deepEqual(left.tones,right.tones.map(row=>[...row].reverse().join('')));
    assert.equal(left.anchorX,right.width-1-right.anchorX);
  }
});
test('every age and action fits the sprite grid with combined cosmetics in both directions',()=>{
  for(const {id:stage} of STAGES)for(const action of ACTIONS)for(let frame=0;frame<action.frames;frame++)for(const facing of [true,false]){
    const duck={stage,state:action.id,facing,cosmetics:{hat:'hat_party',face:'glasses_nerd',neck:'scarf_red'}};
    const before=JSON.stringify(duck),model=characterSprite(duck,frame*action.duration/action.frames);
    assert.equal(model.clipped,false,`${stage}/${action.id}/${frame}`);
    assert.ok(model.art.every((row,y)=>row.length===model.tones[y].length&&/^[ -~]*$/.test(row)));
    assert.equal(JSON.stringify(duck),before);
  }
});
test('world anchoring leaves hops and foot placement to the character rig',()=>{
  const world=new LivingWorld(),s=scene();s.duck.state='jumping';
  const [,y]=world.project(s,s.duck.x,s.duck.y);
  const {characters}=world.render(s,.5);
  assert.equal(characters[0].y,y,'do not apply a second world-space jump');
  const reduced={...s,motion:false};
  assert.deepEqual(world.render(reduced,1).characters,world.render(reduced,40).characters);
});
