// Repertoire engine: bundle and reach table in sync with data; anchors resolve on
// the host drawing; poses sample cleanly and return to rest.
import test from 'node:test';
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {REP_ROUTINES as R,REP_OBJECTS as O,repPose,repAnchor} from '../client/repertoire-routines.mjs';
import {itemSprite} from '../client/ultra-items.mjs';
const cwd=fileURLToPath(new URL('..',import.meta.url));
const SEA=new Set(['pufferfish','swordfish','sturgeon','ancient_dragon_fish']);
const host=oid=>O[oid].host==='keeping'?(SEA.has(oid)?'infinity_pool':'koi_pond'):oid;
test('bundle and reach table match the per-object data',()=>{
 execFileSync(process.execPath,['scripts/build-repertoire.mjs','--check'],{cwd});
 execFileSync(process.execPath,['scripts/export-repertoire-reach.mjs','--check'],{cwd});
});
test('every routine anchor resolves on its host drawing and poses end at rest',()=>{
 for(const [key,r] of Object.entries(R)){
  if(O[r.object].host==='wearable'){const end=repPose({id:key,elapsed:r.duration});for(const k of ['x','y','b','w','contact'])assert.equal(end[k],0,key+' rest');continue;}
  const m=itemSprite(host(r.object),0,{state:{keeping:{setup:true,fish:[]}}});
  for(const [,q] of r.track)if(q.anchor&&!['contact','entry'].includes(q.anchor))assert.ok(repAnchor(m,r.object,q.anchor),key+' anchor '+q.anchor);
  const end=repPose({id:key,elapsed:r.duration});for(const k of ['x','y','b','w','contact'])assert.equal(end[k],0,key+' rest');
 }
});
