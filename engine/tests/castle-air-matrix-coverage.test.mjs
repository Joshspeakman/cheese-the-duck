import test from 'node:test';
import assert from 'node:assert/strict';
import {AirMatrixCoverage,airFrameIdentity} from './castle-air-matrix-coverage.mjs';
import {sharedCastleFixture,specialSharedCastleFixture} from './castle-shared-fixtures.mjs';
const variants=['wide-normal','portrait-reduced'];
function fixture(adapter='regular'){
 const s=adapter==='regular'?sharedCastleFixture():specialSharedCastleFixture('lost_duckling',adapter),w=s.living.plan.carnival_work;
 s._airMatrixCase=adapter+'/start';w.physical.center=[59.4,24.5];
 return s;
}
function descriptor(s){return {id:s._airMatrixCase,...airFrameIdentity(s),placement:[9,7],center:[59.4,24.5],status:'supported'};}
function manifest(cases){return {schema_version:1,scope:'synthetic-coverage-test-only',frames_file:'fixtures.json',frames_sha256:'a'.repeat(64),cases};}
function cover(coverage,s,variant,{effect=true,exit=true}={}){
 for(const phase of ['approach','hold',...(exit?['exit']:[])]){const frame=structuredClone(s);frame.living.plan.carnival_work.physical.phase=phase;if(phase==='hold'&&effect)frame._physicalEvent=0;coverage.record(frame,variant);}
}
test('matrix coverage keeps supported cases and factual native refusals separate',()=>{
 const s=fixture(),refused={...descriptor(s),id:'regular/grille',score:'castle_grill_clean',status:'refused',reason:'No supported stance',attempts:[{placement:[9,6],reason:'Foot support failed'}]},m=manifest([descriptor(s),refused]),before=structuredClone(m),coverage=new AirMatrixCoverage(m);
 for(const variant of variants)cover(coverage,s,variant);
 const result=coverage.finish(variants);assert.equal(result.supportedCount,1);assert.equal(result.refusedCount,1);assert.equal(result.caseCount,2);assert.equal(result.refused[0].reason,refused.reason);assert.deepEqual(m,before);
 const bad=structuredClone(s);bad._airMatrixCase=refused.id;assert.throws(()=>coverage.record(bad,variants[0]),/Refused matrix case emitted/);
});
test('missing effect, variant or native exit cannot pass by borrowing another case coverage',()=>{
 const s=fixture();for(const omission of ['effect','variant','exit']){
  const c=new AirMatrixCoverage(manifest([descriptor(s)]));for(const variant of variants){if(omission==='variant'&&variant===variants[1])continue;cover(c,s,variant,{effect:omission!=='effect'||variant===variants[0],exit:omission!=='exit'||variant===variants[0]});}
  assert.throws(()=>c.finish(variants),/missing (authored effect|rendered variant|exit)/);
 }
});
test('rare and story Pip bind separate adapter cases and exact selected placement',()=>{
 const rare=fixture('rare'),story=fixture('story'),c=new AirMatrixCoverage(manifest([descriptor(rare),descriptor(story)]));
 for(const variant of variants){cover(c,rare,variant);cover(c,story,variant);}assert.equal(c.finish(variants).supportedCount,2);
 const stolen=structuredClone(story);stolen._airMatrixCase=rare._airMatrixCase;assert.throws(()=>c.record(stolen,variants[0]),/changed adapter/);
 const moved=structuredClone(rare);moved.living.plan.carnival_work.physical.center[1]+=.1;assert.throws(()=>c.record(moved,variants[0]),/changed native placement/);
});
test('duplicate IDs, unnamed refusals and absent supported cases fail closed',()=>{
 const s=fixture(),d=descriptor(s);assert.throws(()=>new AirMatrixCoverage(manifest([d,d])),/Duplicate/);
 assert.throws(()=>new AirMatrixCoverage(manifest([{...d,status:'refused',attempts:[]}])) ,/reason/);
 assert.throws(()=>new AirMatrixCoverage(manifest([d])).finish(variants),/missing rendered variant/);
 const refusal={...d,status:'refused',reason:'Unsupported terrain',attempts:[{placement:[9,6],reason:'Unsupported terrain'}]};const onlyRefused=new AirMatrixCoverage(manifest([refusal])).finish(variants);assert.equal(onlyRefused.supportedCount,0);assert.equal(onlyRefused.refusedCount,1);
});
test('a later safe fixture origin retains the failed setup and binds actual approach roots',()=>{
 const s=fixture(),w=s.living.plan.carnival_work,d={...descriptor(s),origin:{operator:[...w.physical.root],cheese:[...w.shared.cheese.root]},attempts:[{placement:[9,7],operator_root:[72,25],cheese_root:[44,26],accepted:false,reason:'Unsupported exterior root'},{placement:[9,7],operator_root:[...w.physical.root],cheese_root:[...w.shared.cheese.root],accepted:true,reason:'Supported'}]},c=new AirMatrixCoverage(manifest([d]));
 for(const variant of variants)cover(c,s,variant);const result=c.finish(variants);assert.equal(result.supportedCount,1);assert.equal(result.refusedCount,0);assert.equal(result.failedAttemptCount,1);assert.equal(result.supportedCasesWithPriorRefusals,1);assert.deepEqual(result.failedAttempts[0].operator_root,[72,25]);
 const moved=structuredClone(s);moved.living.plan.carnival_work.physical.root[0]+=.5;moved.living.plan.carnival_work.physical.phase='approach';assert.throws(()=>new AirMatrixCoverage(manifest([d])).record(moved,variants[0]),/changed selected operator origin/);
});
