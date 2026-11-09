import assert from 'node:assert/strict';
import {STAGES,VARIANTS,ACTIONS,scruffySprite} from './sprites.mjs';
assert.deepEqual(STAGES.map(s=>s.id),['egg','hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary']);
assert.equal(VARIANTS.length,6);
let count=0;
for(const v of VARIANTS){
  const ages=new Set(STAGES.map(s=>scruffySprite(v.id,s.id).art.join('\n')));
  assert.equal(ages.size,9,`${v.id}: each age needs its own silhouette`);
  for(const s of STAGES)for(const a of ACTIONS){
    const poses=new Set();
    const rate=s.id==='elder'?.72:s.id==='hatchling'?1.18:1;
    for(let i=0;i<24;i++)for(const facing of [true,false]){
      const f=scruffySprite(v.id,s.id,a.id,i*a.duration/24/rate,facing);
      assert.equal(f.clipped,false,`${v.id}/${s.id}/${a.id}/${i}: clipped drawing`);
      assert.ok(f.art.every((row,y)=>row.length===40&&row.length===f.tones[y].length&&/^[\x20-\x7e]*$/.test(row)), 'ASCII-only aligned palette');
      if(facing)poses.add(f.art.join('\n'));count++;
    }
    if(s.id!=='egg'){
      const minimum={walking:5,flapping:4,eating:5,hopping:6,preening:4,quacking:3,sleeping:3,swimming:6,dancing:5,idle:3}[a.id];
      assert.ok(poses.size>=minimum,`${v.id}/${s.id}/${a.id}: only ${poses.size} drawn poses`);
    }
  }
}
const adults=new Set(VARIANTS.map(v=>scruffySprite(v.id,'adult').art.join('\n')));
assert.equal(adults.size,6);
console.log(JSON.stringify({result:'PASS',variants:6,ages:9,actions:10,validatedFrames:count}));
