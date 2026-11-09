import test from 'node:test';
import assert from 'node:assert/strict';
import { documentRows,documentTitle,cropDocument,menuWindow } from '../client/interface-model.mjs';
import { emotionPortrait } from '../client/emotion-portrait.mjs';
const line=(text,flags=0)=>[[text,'#e2dfca','#101b19',flags]];
test('long styled speech wraps without losing any content',()=>{
 const speech='> What the fuck, Cheese? '+'Feathers, bread & trouble. '.repeat(40);
 const rows=documentRows([line(speech.trimEnd(),1)],57);
 assert.equal(rows.map(row=>row.text).join(''),speech.trimEnd());
 assert(rows.every(row=>row.cells.length<=57&&row.cells.every(cell=>cell.flags===1)));
});
test('box spacers stay blank and do not become horizontal rules',()=>{
 const rows=documentRows([line('║ A ║'),line('║     ║'),line('╠═════╣'),line('║ B ║')]);
 assert.deepEqual(rows.map(row=>row.kind),['text','blank','rule','text']);
 assert.equal(documentTitle({title:'MENU',lines:[line('╔══════════╗'),line('║ SETTINGS ║')]}),'SETTINGS');
});
test('arcade art keeps its walls and whitespace after a common margin is removed',()=>{
 const rows=documentRows(cropDocument([line('    +----+'),line('    |    |'),line('    | a  |'),line('    +----+')]),108,true);
 assert.deepEqual(rows.map(row=>row.text),['+----+','|    |','| a  |','+----+']);
});
test('long hierarchy always includes the selected last item',()=>{
 const items=Array.from({length:40},(_,id)=>({id}));
 const view=menuWindow({items,selected:39},7);
 assert.equal(view.start,33);assert.equal(view.items.at(-1).id,39);
});
test('the close-up shows eight distinct emotions independently of the world walking pose',()=>{
 const moods=['ecstatic','happy','content','grumpy','sad','miserable','dramatic','petty'];
 const faces=moods.map(mood=>emotionPortrait({stage:'adult',state:'walking'},{mood},0).art.join('\n'));
 assert.equal(new Set(faces).size,8);
 for(const action of ['eating','sleeping','petting','cleaning','playing','talking']){
   const first=emotionPortrait({stage:'adult'},{mood:'content',action},0).art.join('\n');
   const next=emotionPortrait({stage:'adult'},{mood:'content',action},.5).art.join('\n');
   assert.notEqual(first,next,action);
 }
});
