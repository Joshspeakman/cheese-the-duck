import test from 'node:test';
import assert from 'node:assert/strict';
import {WATER_BLUEPRINTS} from '../client/waterworks.mjs';
import {itemSprite,itemWorldScale,ItemPainter} from '../client/ultra-items.mjs';

test('every water construction has bounded ink, solid geometry, contacts and its own silhouette',()=>{
 const signatures=new Set();
 for(const id of Object.keys(WATER_BLUEPRINTS)){
  const state={condition:.2,dirt:.7},before=JSON.stringify(state);
  for(const season of ['spring','summer','fall','winter'])for(const hour of [3,15])for(let n=0;n<24;n++){
   const m=itemSprite(id,n/3,{state,interaction:{phase:'act'},context:{season,hour,weather:'rain',living:{ecology:{ice:season==='winter'?.7:0,snow:season==='winter'?.3:0}}}});
   assert.equal(m.construction,'waterworks-v1');assert.equal(m.clipped,false,id+' '+n);
   assert(m.art.every((r,y)=>r.length===m.width&&r.length===m.tones[y].length&&/^[ -~]*$/.test(r)),id);
   assert(m.fills.every(f=>f.x>=0&&f.y>=0&&f.x+f.w<=m.width&&f.y<m.art.length),id+' solid bound');
   for(const a of Object.values(m.anchors))if(typeof a==='object'&&a.x!==undefined)assert(a.x>=0&&a.x<m.width&&a.y>=0&&a.y<m.art.length,id+' contact');
   assert(m.art.join('').replace(/ /g,'').length>(['spray','bowl'].includes(WATER_BLUEPRINTS[id].type)?150:250),id+' constructed ink');
  }
  signatures.add(itemSprite(id,1).art.join('\n'));assert.equal(JSON.stringify(state),before);
  assert(itemWorldScale(id)>=.6);
 }
 assert.equal(signatures.size,Object.keys(WATER_BLUEPRINTS).length);
});
test('cached drawings distinguish changed water fills and materials even when glyphs stay the same',()=>{
 const old=globalThis.document,ctx={fillRect(){},strokeText(){},fillText(){}};
 globalThis.document={createElement:()=>({getContext:()=>ctx})};
 try{
  const p=new ItemPainter(),a=itemSprite('pool_kiddie',0),b={...a,panels:{...a.panels,w:'#153441'}},c={...a,fills:a.fills.slice(2)};
  const ia=p.image(a,4),ib=p.image(b,4),ic=p.image(c,4);
  assert.notEqual(ia.canvas,ib.canvas);assert.notEqual(ia.canvas,ic.canvas);assert.equal(p.image(a,4),ia);
 }finally{globalThis.document=old;}
});
test('ambient water moves, cold water freezes, heated tubs stay warm, and the mat is woven fabric',()=>{
 for(const id of Object.keys(WATER_BLUEPRINTS)){
  const options={context:{hour:13,living:{ecology:{ice:.7}}}},a=itemSprite(id,0),b=itemSprite(id,1.3);
  if(id==='pond_mat'){assert.equal(a.animated,false);assert.equal(a.floor,true);assert.deepEqual(a.art,b.art);continue;}
  const phases=[0,.2,.6,1.3,2.1].map(t=>itemSprite(id,t).art.join('\n'));
  assert(new Set(phases).size>1,id+' flow');
  assert.equal(itemSprite(id,1,options).frozen,!WATER_BLUEPRINTS[id].heated,id);
  const reduced=t=>itemSprite(id,t,{motion:false,interaction:{phase:'act'},context:{hour:13,weather:'rain'}});
  assert.deepEqual(reduced(0),reduced(100),id+' reduced motion');
 }
});
