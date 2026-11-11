// Generate placement bounds from the same drawings used by the live renderer.
// Bounds include the whole authored canvas, including reserved animation space.
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import {catalog,itemSprite,itemWorldScale} from './client/ultra-items.mjs';
export function measure(item){
 let width=0,height=0,model;
 for(let phase=0;phase<16;phase++){
  model=itemSprite(item.id,phase*.37,{interaction:phase%2?{kind:'item',target:item.id,phase:'act',progress:phase/16}:null});
  const scale=itemWorldScale(item.id)*(model.detailScale||1);
  // Include the painter border, lift and the largest authored shear. This
  // reserves animation space, not just the quiet first frame.
  width=Math.max(width,(model.width+2+(model.art.length+2)*1.5*.065*2)*scale);
  height=Math.max(height,(model.art.length+2+1.2)*scale);
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
