import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import {LivingWorld} from '../client/ultra-world.mjs';
import {seedOf} from '../client/ultra-grid.mjs';
import {nativeSceneryBounds} from '../client/scenery-projection.mjs';
// Each moving glyph has x = fixed + amplitude*sin(frequency*t+phase).
// Its y, hash and visibility are time-independent. Solving both extrema for
// every lobe/curtain therefore bounds every rounded glyph position for all t.
export function scenerySampleTimes(){
 const times=new Set([0]);
 for(const [count,frequency,phaseStep]of [[8,.7,1],[29,.75,.3]])for(let n=0;n<count;n++)for(const angle of [Math.PI/2,3*Math.PI/2]){
  let phase=angle-n*phaseStep;while(phase<0)phase+=2*Math.PI;times.add(phase/frequency);
 }
 return [...times].sort((a,b)=>a-b);
}
export function captureHomeScenery(time=0,camera={x:0,y:0,w:132,h:42}){
 const world=new LivingWorld();world.scenery=[];world.landmarks({location:'Home Pond',biome:'pond',season:'spring',particles:false,camera},time,seedOf('Home Pond'));
 return world.scenery.filter(s=>s.nativeCells);
}
export function exportCastleSceneryMetrics(){
 const cells=new Map(),times=scenerySampleTimes();
 for(const time of times)for(const layer of captureHomeScenery(time)){
  if(!cells.has(layer.id))cells.set(layer.id,new Map());const all=cells.get(layer.id);
  for(const c of layer.nativeCells)if(c[2]!==32)all.set(c[0]+','+c[1],c);
 }
 return {schema_version:1,location:'Home Pond',kind:'native-scenery-ink-envelope',sampling:{method:'all-willow-sway-extrema',samples:times.length},features:[...cells].map(([id,ink])=>({id,kind:id.includes('willow')?'willow':'dock-and-lantern',bounds:nativeSceneryBounds([...ink.values()])}))};
}
if(process.argv[1]===fileURLToPath(import.meta.url)){
 const output=JSON.stringify(exportCastleSceneryMetrics(),null,2)+'\n',path=new URL('../client/animation/castle-scenery-metrics.json',import.meta.url);
 if(process.argv.includes('--check')){if(fs.readFileSync(path,'utf8')!==output)throw Error('Scenery metrics stale');}else fs.writeFileSync(path,output);
 console.log('Home Pond physical scenery envelope validated from actual canonical ink');
}
