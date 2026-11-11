import {PLAYKIT_BLUEPRINTS} from '../client/playkit-workshop.mjs';
import {GROUND_BLUEPRINTS} from '../client/ground-workshop.mjs';
import {ARCHITECTURE_BLUEPRINTS} from '../client/architecture-workshop.mjs';
import test from 'node:test';
import assert from 'node:assert/strict';
import { catalog,itemFamily,itemSprite,selectedItem } from '../client/ultra-items.mjs';
import { LivingWorld } from '../client/ultra-world.mjs';
import { luminousPalette } from '../client/scene-effects.mjs';
import { palette } from '../client/ultra-grid.mjs';
import { scene } from './scenes.mjs';
import {TEXTILE_BLUEPRINTS} from '../client/textile-workshop.mjs';
import {INSTRUMENT_BLUEPRINTS} from '../client/instrument-workshop.mjs';
import {BOTANICAL_BLUEPRINTS} from '../client/botanical-workshop.mjs';
import {LIGHTING_BLUEPRINTS} from '../client/lighting-workshop.mjs';
import {CREATIVE_BLUEPRINTS} from '../client/creative-workshop.mjs';
import {KEEPSAKE_BLUEPRINTS} from '../client/keepsake-workshop.mjs';

test('every live item has readable authored ASCII with matching color masks',()=>{
  assert.equal(catalog.length,542);
  const families=new Set();
  for(const item of catalog){
    const model=itemSprite(item.id,1);families.add(itemFamily(item.id));
    assert(itemFamily(item.id),item.id);assert(model.art.length>=3,item.id);
    assert(model.art.every((row,i)=>/^[ -~]*$/.test(row)&&row.length===model.tones[i].length),item.id);
    assert(!model.art.join('').includes('[?]'),item.id);
    assert.equal(model.detail,true);assert(model.width>=5&&model.width<=(PLAYKIT_BLUEPRINTS[item.id]?.w||ARCHITECTURE_BLUEPRINTS[item.id]?.w||GROUND_BLUEPRINTS[item.id]?.w||TEXTILE_BLUEPRINTS[item.id]?.w||CREATIVE_BLUEPRINTS[item.id]?.w||KEEPSAKE_BLUEPRINTS[item.id]?.w||LIGHTING_BLUEPRINTS[item.id]?.w||BOTANICAL_BLUEPRINTS[item.id]?.w||INSTRUMENT_BLUEPRINTS[item.id]?.w||128),item.id);
    assert.deepEqual(itemSprite(item.id,1,{motion:false}),itemSprite(item.id,83,{motion:false}),item.id);
  }
  assert(families.size>200);
});
test('water, fire, magical objects and vegetation animate without mutating catalog data',()=>{
  const original=JSON.stringify(catalog);
  for(const id of ['fountain_grand','waterfall','campfire','portal','firefly_swarm','cherry_tree']){
    assert.notDeepEqual(itemSprite(id,.1),itemSprite(id,.6),id);
  }
  assert.equal(JSON.stringify(catalog),original);
});
test('menu previews follow authoritative selections, with guarded name matching for other item menus',()=>{
  const row={kind:'selected',text:'> [3] Fresh Lettuce x4'};
  assert.equal(selectedItem({modal:{title:'INVENTORY'}},[row]).id,'lettuce');
  assert.equal(selectedItem({modal:{title:'SHOP'},itemPreview:'hat_blue'},[row]).id,'hat_blue');
  assert.equal(selectedItem({modal:{title:'TALK'}},[row]),null);
  assert.equal(selectedItem({modal:{title:'INVENTORY'}},[{kind:'selected',text:'> Costly lettuceware'}]),null);
});
test('props follow the camera and disappear when removed without changing the simulation',()=>{
  const world=new LivingWorld(),s=scene({items:[{id:'fountain_grand',x:40,y:20}],structures:[{id:'wooden_cottage',x:70,y:35}]});
  const original=JSON.stringify(s),a=world.render(s,2,.033).objects;
  assert.equal(a.length,2);assert(a.every(v=>v.item));
  const b=world.render({...s,camera:{...s.camera,x:10}},2,.033).objects;
  assert(a.every((item,i)=>item.x!==b[i].x&&item.y===b[i].y));
  assert.equal(world.render({...s,items:[],structures:[]},2,.033).objects.length,0);
  assert.equal(JSON.stringify(s),original);
});
test('effects off retains the base palette and vivid stays inside RGB bounds',()=>{
  const base=palette(scene());assert.deepEqual(luminousPalette(base,'off'),base);
  const vivid=luminousPalette(base,'vivid');assert.notDeepEqual(vivid,base);assert(vivid.every(c=>/^#[a-f0-9]{6}$/.test(c)));
});
