import test from 'node:test';
import assert from 'node:assert/strict';
import { sceneLight,ambientRows,lightingScene,readableInk,contrastRatio } from '../client/scene-lighting.mjs';
const luma=hex=>{const [r,g,b]=hex.slice(1).match(/../g).map(v=>parseInt(v,16)/255);return .2126*r+.7152*g+.0722*b;};
const pond={location:'Home Pond',biome:'pond',season:'spring',weather:'sunny',hour:12};
test('daytime lights the empty sky, land and water instead of only the glyphs',()=>{
  const day=ambientRows(sceneLight(pond)),night=ambientRows(sceneLight({...pond,hour:23}));
  assert(luma(day.land[15])>.6);assert(luma(day.land[85])>.42);assert(luma(day.water[85])>.45);
  for(const [surface,row] of [['land',15],['land',85],['water',85]])assert(luma(day[surface][row])>luma(night[surface][row])*2.1);
});
test('overcast daytime stays readable, sunsets are distinct, caves stay sheltered',()=>{
  const noon=sceneLight(pond),dusk=sceneLight({...pond,hour:18.5}),rain=sceneLight({...pond,weather:'rainy'});
  assert.notEqual(noon.skyTop,dusk.skyTop);assert(dusk.twilight>.8);
  assert(luma(ambientRows(rain).land[85])>.4);
  const cave=sceneLight({...pond,location:'Crystal Cave'});assert(cave.indoor);assert.equal(cave.sun,0);assert(luma(ambientRows(cave).land[15])<.2);
});
test('lighting overrides preserve game time and freeze consistently at any hour',()=>{
  const s={...pond,hour:23,duck:{name:'Cheese'}},before=JSON.stringify(s);
  assert.equal(lightingScene(s,'day').hour,12);assert.equal(lightingScene(s,'night').hour,23);
  assert.equal(lightingScene(s,'dusk').hour,18.5);assert.equal(lightingScene(s,'auto'),s);
  assert.equal(JSON.stringify(s),before);
  for(let hour=0;hour<24;hour+=.25){const light=sceneLight({...pond,hour});assert(light.sun>=0&&light.sun<=1);assert(light.twilight>=0&&light.twilight<=1);}
});

test('fine daylight ink retains at least 3.25:1 contrast on sky, ground and water',()=>{
  const rows=ambientRows(sceneLight(pond));
  for(const background of [...rows.land,...rows.water])for(const ink of ['#9bad66','#d8ad9b','#796343','#acd8ce','#426c43']){
    assert(contrastRatio(readableInk(ink,background),background)>=3.25,ink+' on '+background);
  }
});
