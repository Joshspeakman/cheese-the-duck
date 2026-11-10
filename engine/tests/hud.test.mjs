import test from 'node:test';
import assert from 'node:assert/strict';
import {HudLayout,HUD_PANELS,IdleFade} from '../client/hud-layout.mjs';
test('idle HUD fades only after a minute, without pausing the simulation',()=>{
 const idle=new IdleFade(1000);
 assert.equal(idle.update(60999),1);assert.equal(idle.update(61000),1);
 assert.equal(idle.update(61900),.5);assert.equal(idle.update(62800),0);
 idle.wake(70000);assert.equal(idle.update(70000),1);
 assert.equal(idle.update(140000,{eligible:false}),1);
 assert.equal(idle.update(140001),1,'modal dismissal starts a fresh minute');
 assert.equal(idle.update(210000,{enabled:false}),1);
 assert.equal(idle.update(270001,{reducedMotion:true}),0);
});
test('all panels stay reachable after moving, zooming and resizing',()=>{
 const layout=new HudLayout();
 for(const id of Object.keys(HUD_PANELS)){
  layout.move(id,100000,-5000,1440,1000);
  for(const [W,H] of [[920,640],[1440,1000],[2560,1080],[700,500]]){
   const r=layout.rect(id,W,H);assert(r.x>=8&&r.y>=8,id);
   assert(r.x+r.w<=W-8+.001&&r.y+r.h<=H-8+.001,id);
  }
 }
});
test('visibility and positions persist independently, while reset restores defaults',()=>{
 const layout=new HudLayout();layout.show('care',true);layout.show('emotion',false);layout.move('chat',320,410,1440,1000);
 layout.autoFade=false;const restored=new HudLayout(JSON.parse(JSON.stringify(layout.save())));
 assert.deepEqual(restored.rect('chat',1440,1000),layout.rect('chat',1440,1000));
 assert.equal(restored.visible('care'),true);assert.equal(restored.visible('emotion'),false);assert.equal(restored.autoFade,false);
 restored.preset('quiet');assert.deepEqual(Object.keys(HUD_PANELS).filter(id=>restored.visible(id)),['tools','emotion','actions']);
 restored.preset();assert.equal(restored.visible('chat'),true);assert.equal(restored.visible('care'),false);
 assert.deepEqual(restored.rect('chat',1440,1000),new HudLayout().rect('chat',1440,1000));
});
test('corrupt preferences cannot strand panels or inject unknown elements',()=>{
 const layout=new HudLayout({version:1,panels:{chat:{u:Infinity,v:NaN},unknown:{visible:true},pond:{u:999,v:-55}},dialogs:{bad:{u:null,v:null}}});
 assert.equal(layout.visible('unknown'),false);assert(Number.isFinite(layout.rect('chat',1440,1000).x));
 assert.equal(layout.rect('pond',1440,1000).y,8);assert.deepEqual(layout.dialogs,{});
 const saved=layout.save();saved.panels.pond.u=0;assert.equal(layout.panels.pond.u,1);
});
test('movable dialogs clamp to the viewport and bound stored positions',()=>{
 const layout=new HudLayout(),base={x:20,y:20,w:700,h:500};
 for(let i=0;i<40;i++)layout.moveDialog('dialog:'+i,400,300,base,1440,1000);
 assert.equal(Object.keys(layout.dialogs).length,24);
 const r=layout.dialogRect('dialog:39',base,800,600);assert(r.x+r.w<=792&&r.y+r.h<=592);
});
