// Bundles client/animation/repertoire/*.json (one per object) into
// client/animation/repertoire.json for the browser. --check fails if stale.
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
const dir=fileURLToPath(new URL('../client/animation/repertoire/',import.meta.url)),target=fileURLToPath(new URL('../client/animation/repertoire.json',import.meta.url));
const objects={},routines={};
for(const f of fs.readdirSync(dir).filter(f=>f.endsWith('.json')).sort()){
 const d=JSON.parse(fs.readFileSync(dir+f,'utf8'));
 objects[d.object]={host:d.host||'placed',anchors:d.anchors||{},fields:d.fields||{},...(d.marks?{marks:d.marks}:{})};
 for(const [k,r] of Object.entries(d.routines)){if(routines[k])throw Error('duplicate routine '+k);routines[k]={...r,object:d.object};}
}
const data=JSON.stringify({objects,routines})+'\n';
if(process.argv.includes('--check')){if(!fs.existsSync(target)||fs.readFileSync(target,'utf8')!==data)throw Error('Repertoire changed: run node engine/scripts/build-repertoire.mjs');}
else fs.writeFileSync(target,data);
console.log(JSON.stringify({objects:Object.keys(objects).length,routines:Object.keys(routines).length}));
