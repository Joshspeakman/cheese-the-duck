import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import {wearableSlots} from './client/wearables.mjs';
const path=fileURLToPath(new URL('./client/animation/wearable-slots.json',import.meta.url)),data=JSON.stringify(wearableSlots,null,2)+'\n';
if(process.argv.includes('--check')){
 if(fs.readFileSync(path,'utf8')!==data)throw Error('Regenerate native wearable slots with node engine/build-wearable-slots.mjs');
}else fs.writeFileSync(path,data);
