import test from 'node:test';
import assert from 'node:assert/strict';
import {WeatherDrift,windVector,wrap} from '../client/weather-wind.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
import {itemSprite} from '../client/ultra-items.mjs';
import {scene} from './scenes.mjs';
const weather=(heading,strength=.7,extra={})=>scene({living:{ecology:{wind_heading:heading,wind:strength}},weather:'rainy',...extra});
test('precipitation travels downwind, opposite the native vane bearing',()=>{
 for(const [heading,x,y]of [[0,-1,0],[.25,0,-1],[.5,1,0],[.75,0,1]]){
  const s=weather(heading),before=JSON.stringify(s),v=windVector(s);
  assert(Math.abs(v.x-x*.7)<1e-9);assert(Math.abs(v.y-y*.7)<1e-9);assert.equal(JSON.stringify(s),before);
 }
 assert.deepEqual(windVector(weather(1.5)),windVector(weather(.5)));
 assert.equal(windVector(weather(NaN,Infinity)).strength,.2);
 assert.equal(windVector(weather(0,-1)).strength,0);
 for(const x of [-800,-1,0,800])assert(wrap(x,240)>=0&&wrap(x,240)<240);
});
test('drift stays continuous through wind changes, independent of frame rate',()=>{
 const a=new WeatherDrift(),b=new WeatherDrift(),s=weather(.13),before=JSON.stringify(s);
 for(let n=0;n<300;n++)a.update(s,1/30);
 for(let n=0;n<1200;n++)b.update(s,1/120);
 assert(Math.abs(a.x-b.x)<1e-9&&Math.abs(a.y-b.y)<1e-9);
 const previous={x:a.x,y:a.y};a.update(weather(.63),1/60);
 assert(Math.hypot(a.x-previous.x,a.y-previous.y)<.012,'changed weather moves existing particles a small step');
 const held={x:a.x,y:a.y};a.update({...s,motion:false},1000);assert.equal(a.x,held.x);assert.equal(a.y,held.y);
 a.update(s,1000);assert(Math.hypot(a.x-held.x,a.y-held.y)<=.17500001,'resume skips the long hidden interval');
 a.update({...s,location:'Crystal Cave'},1,false);assert.equal(a.x,0);assert.equal(a.y,0);assert.equal(a.vector.strength,0);
 assert.equal(JSON.stringify(s),before);
});
test('actual weather glyphs lean with wind, while calm rain falls vertically',()=>{
 for(const [heading,strength,glyph]of [[0,.8,'/'],[.5,.8,'\\'],[.2,0,'|']]){
  const s=weather(heading,strength),w=new LivingWorld();w.wind.update(s,.1);w.grid.clear();w.weather(s,2,1);
  assert([...w.grid.chars].filter(c=>c===glyph.charCodeAt(0)).length>20);
  const before=Buffer.from(w.grid.chars);w.grid.clear();w.weather({...s,weatherEffects:false},2,1);assert(w.grid.chars.every(c=>c===32));
  if(strength){w.grid.clear();w.wind.update(s,.2);w.weather(s,2,1);assert.notDeepEqual(Buffer.from(w.grid.chars),before);}
 }
 for(const type of ['snowy','windy']){
  const a=new LivingWorld(),b=new LivingWorld(),s=weather(0,.9,{weather:type}),other=weather(.5,.9,{weather:type});
  for(let n=0;n<30;n++){a.wind.update(s,.1);b.wind.update(other,.1);}
  a.weather(s,3,1);b.weather(other,3,1);assert.notDeepEqual(a.grid.chars,b.grid.chars,type+' follows native direction');
 }
});
test('pennants fly away from the vane bearing and stay bounded through every turn',()=>{
 const variants=new Set();
 for(let n=0;n<32;n++)for(const flag of [0,.5,1]){
  const state={architecture:{bearing:n*Math.PI/16,flag,phase:1.3,wind:.85}},before=JSON.stringify(state),m=itemSprite('flag_pole',0,{state});
  assert(!m.clipped,'bearing '+n+' hoist '+flag);
  assert(m.fills.every(f=>f.x>=0&&f.x+f.w<=m.width&&f.y>=0&&f.y<m.art.length));
  assert.equal(JSON.stringify(state),before);assert.deepEqual(itemSprite('flag_pole',100,{state}),m);variants.add(m.art.join('\n'));
 }
 assert(variants.size>24);
 for(const [bearing,side]of [[0,-1],[Math.PI,1]]){
  const m=itemSprite('flag_pole',0,{state:{architecture:{bearing,flag:1,wind:0}}}),cloth=m.fills.filter(f=>f.tone==='w');
  assert(cloth.length);assert(cloth.every(f=>side*(f.x-m.width/2)>0),'cloth flies downwind');
 }
});
