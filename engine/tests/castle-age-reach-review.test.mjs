import test from 'node:test';
import assert from 'node:assert/strict';
import {buildReview,reach,sampleAge} from '../scripts/review-castle-age-reach.mjs';
import ADULT from '../client/animation/castle-contact-metrics.json' with {type:'json'};
const report=buildReview();
test('nine-age read-only review preserves actual anatomy and existing adult contact contract',()=>{
 assert.equal(report.status,'review-only');assert.equal(report.ages.length,9);
 for(const a of report.ages){assert.equal(a.metrics.length,9);for(const m of a.metrics){assert.equal(m.clipped,false);if(a.age==='egg'){assert.equal(m.grip,null);assert.equal(m.feet,null);}else {assert.equal(m.feet.length,2);assert(m.feet.every(f=>f[1]===0));assert(m.scale>0);}}}
 assert.equal(report.ages[0].placements.length,0);
 const adult=report.ages.find(a=>a.age==='adult');
 for(const m of adult.metrics){const expected=ADULT.routines[m.id][m.index];for(const k of ['scale','anchorX','groundRow','grip','feet'])assert.deepEqual(m[k],expected[k],m.id+' '+k);}
});
test('hatchling feasibility remains placement-specific with no invented reach extension',()=>{
 const age=report.ages.find(a=>a.age==='hatchling'),[lower,upper]=age.placements;
 assert.deepEqual(lower.stations.filter(s=>!s.supportedCommonCount).map(s=>[s.id,s.station]),[['castle_door_open','door'],['castle_hose_stow','switch'],['castle_hose_stow','hose']]);
 assert(upper.stations.every(s=>s.supportedCommonCount>0));
 assert(report.ages.filter(a=>!['egg','hatchling'].includes(a.age)).every(a=>a.placements.every(p=>p.stations.every(s=>s.supportedCommonCount>0))));
});
test('every reported common supported stance reaches every authored station effect with the actual age rig',()=>{
 for(const age of report.ages)for(const p of age.placements)for(const station of p.stations){
  if(!station.bestSupported)continue;
  assert(station.bestSupported.root.every(Number.isInteger));assert(station.bestSupported.root[1]>=p.ground);
  for(const index of station.effectIndices){const actual=sampleAge(age.age,station.id,index);assert(reach(actual,station.bestSupported.root,station.target)<=report.reachCap);}
 }
});
