import test from 'node:test';
import assert from 'node:assert/strict';
import { sceneLight,ambientRows,lightBand,ambientSwatches,readableInk,contrastRatio } from '../client/scene-lighting.mjs';
const luma=hex=>{const [r,g,b]=hex.slice(1).match(/../g).map(v=>parseInt(v,16)/255);return .2126*r+.7152*g+.0722*b;};
const pond={location:'Home Pond',biome:'pond',season:'spring',weather:'sunny',hour:12};
test('daylight has rich midtones rather than pale flat fills or night darkness',()=>{
  const day=ambientRows(sceneLight(pond)),night=ambientRows(sceneLight({...pond,hour:23}));
  assert(luma(day.land[15])>.32&&luma(day.land[15])<.6);assert(luma(day.land[85])>.22&&luma(day.land[85])<.5);assert(luma(day.water[85])>.24&&luma(day.water[85])<.5);
  for(const [surface,row] of [['land',15],['land',85],['water',85]])assert(luma(day[surface][row])>luma(night[surface][row])*1.8);
});
test('overcast daytime stays readable, sunsets are distinct, caves stay sheltered',()=>{
  const noon=sceneLight(pond),dusk=sceneLight({...pond,hour:18.5}),rain=sceneLight({...pond,weather:'rainy'});
  assert.notEqual(noon.skyTop,dusk.skyTop);assert(dusk.twilight>.8);
  assert(luma(ambientRows(rain).land[85])>.22);
  const cave=sceneLight({...pond,location:'Crystal Cave'});assert(cave.indoor);assert.equal(cave.sun,0);assert(luma(ambientRows(cave).land[15])<.2);
});
test('world and portrait lighting derive their phase solely from the game hour',()=>{
  const s={...pond,hour:23,duck:{name:'Cheese'}},before=JSON.stringify(s);
  assert.equal(sceneLight(s).hour,23);assert.equal(sceneLight(s).phase,'Night');assert(sceneLight(s).night);
  assert.equal(JSON.stringify(s),before);
  assert.equal(sceneLight({...pond,hour:18+43/60}).hour,18+43/60);
  for(const [hour,phase] of [[2,'Late night'],[6,'Dawn'],[9,'Morning'],[12,'Midday'],[16,'Afternoon'],[18,'Evening'],[20,'Dusk'],[23,'Night']])assert.equal(sceneLight({...pond,hour}).phase,phase);
});
test('directional illumination gives the landscape distinct lit and shaded areas',()=>{
  const light=sceneLight(pond),rows=ambientRows(light),swatches=ambientSwatches(light,rows);
  const bands=new Set();for(let x=0;x<240;x+=10)bands.add(lightBand(light,x,80));
  assert(bands.size>=3);assert.notEqual(swatches.land[0][80],swatches.land[4][80]);
});

test('fine daylight ink retains at least 3.25:1 contrast on sky, ground and water',()=>{
  const rows=ambientRows(sceneLight(pond));
  for(const background of [...rows.land,...rows.water])for(const ink of ['#9bad66','#d8ad9b','#796343','#acd8ce','#426c43']){
    assert(contrastRatio(readableInk(ink,background),background)>=3.25,ink+' on '+background);
  }
});
