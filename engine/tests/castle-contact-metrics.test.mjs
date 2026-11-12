import test from 'node:test';
import assert from 'node:assert/strict';
import METRICS from '../client/animation/castle-contact-metrics.json' with {type:'json'};
import {exportCastleContactMetrics} from '../scripts/export-castle-contact-metrics.mjs';
import {CASTLE_SCORES} from '../client/castle-care.mjs';
const ages=['hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'];
test('schema 2 requires explicit hatched age metrics and has no egg or fallback alias',()=>{
 assert.equal(METRICS.schema_version,2);assert.equal(METRICS.actor,'cheese');assert.equal(METRICS.role,'a');assert.equal(METRICS.facing,'right');assert.equal(METRICS.reach_cells,3);
 assert.deepEqual(Object.keys(METRICS.ages),ages);assert.equal(METRICS.routines,undefined);assert.equal(METRICS.ages.egg,undefined);assert.equal(METRICS.ages.teen,undefined);assert.equal(METRICS.ages.unknown,undefined);
 let contacts=0;
 for(const age of ages)for(const [id,records]of Object.entries(METRICS.ages[age].routines)){
  assert.equal(records.length,CASTLE_SCORES[id].effects.length);
  for(const [i,m]of records.entries()){
   assert.deepEqual([m.at,m.field,m.value],CASTLE_SCORES[id].effects[i]);assert.equal(m.feet.length,2);assert(m.feet.every(f=>f[1]===0));
   assert([m.scale,m.anchorX,m.groundRow,...m.grip,...m.feet.flat()].every(Number.isFinite));contacts++;
  }
 }
 assert.equal(contacts,72);
 assert.notDeepEqual(METRICS.ages.hatchling.routines.castle_start[0].grip,METRICS.ages.adult.routines.castle_start[0].grip);
 assert.equal(METRICS.ages.juvenile.routines.castle_start[0].scale,67/(13*7.5));
});
test('committed metrics reproduce actual rigs at full precision for normal/reduced and native/legacy poses',()=>{
 assert.deepEqual(METRICS,exportCastleContactMetrics());
});
