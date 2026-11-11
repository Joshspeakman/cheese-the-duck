import test from 'node:test';import assert from 'node:assert/strict';
import {ChatFade} from '../client/chat-fade.mjs';
test('silence fades chat independently of other HUD activity',()=>{const f=new ChatFade(0);assert.equal(f.update(13999),1);assert.ok(f.update(14800)>.4&&f.opacity<.6);assert.equal(f.update(16000),0);f.spoke(16010);assert.equal(f.update(16010),1);});
test('reading, typing, dragging and waiting for a reply hold chat visible',()=>{const f=new ChatFade(0);for(const now of [30000,60000,120000])assert.equal(f.update(now,{held:true}),1);assert.equal(f.update(120100),1);assert.equal(f.update(136000),0);});
test('reduced motion hides at the silence threshold without animated fading',()=>{const f=new ChatFade(0);assert.equal(f.update(14000,{reducedMotion:true}),1);assert.equal(f.update(14001,{reducedMotion:true}),0);f.wake(14002);assert.equal(f.update(14002,{reducedMotion:true}),1);});
