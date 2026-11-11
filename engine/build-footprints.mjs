// Generate placement bounds from the same drawings used by the live renderer.
// Bounds include the whole authored canvas, including reserved animation space.
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import {catalog,itemSprite,itemWorldScale,itemFamily} from './client/ultra-items.mjs';
import {PLAYDATES} from './client/playdates.mjs';
export function measure(item){
 let width=0,height=0,model;
 const include=(time,interaction)=>{
  model=itemSprite(item.id,time,{interaction});
  const scale=itemWorldScale(item.id)*(model.detailScale||1);
  // Include the painter border, lift and the largest authored shear. This
  // reserves animation space, not just the quiet first frame.
  width=Math.max(width,(model.width+2+(model.art.length+2)*1.5*.065*2)*scale);
  height=Math.max(height,(model.art.length+2+1.2)*scale);
 };
 for(let phase=0;phase<16;phase++)include(phase*.37,phase%2?{kind:'item',target:item.id,phase:'act',progress:phase/16}:null);
 // Shared ball play opens a wider court than the resting drawing. Reserve the
 // whole authored passage so passes cannot roll through roots or over a bank.
 for(const [id,score]of Object.entries(PLAYDATES))if(score.family===itemFamily(item.id)){
  for(const progress of [0,.25,.5,.75,1])include(progress*score.duration,{kind:'item',target:item.id,phase:'act',
   company:{id,phase:'act',elapsed:progress*score.duration,duration:score.duration,mass:[1,1]}});
 }
 return {width:Math.ceil(width*100)/100,height:Math.ceil(height*100)/100,
  floor:Boolean(model.floor),construction:model.construction||'legacy-detail'};
}
const entries={};
for(const item of catalog){
 entries[item.id]=measure(item);
}
const target=fileURLToPath(new URL('./client/animation/object-footprints.json',import.meta.url));
const data=JSON.stringify({version:2,units:'render-grid-cells',items:entries},null,2)+'\n';
if(process.argv.includes('--check')){
 if(fs.readFileSync(target,'utf8')!==data)throw Error('Artwork changed: regenerate object footprints with node engine/build-footprints.mjs');
}else fs.writeFileSync(target,data);
console.log(JSON.stringify({objects:Object.keys(entries).length,target}));
