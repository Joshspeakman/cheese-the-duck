import test from 'node:test';
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
const {pondCommand}=createRequire(import.meta.url)('../pond-command.cjs');
test('shared invitation survives the desktop bridge with exact copy and score',()=>{
 const input={type:'pond',action:'carnival_action',target:'bounce_house',text:'castle_door_open',instance:'house-b',together:true};
 assert.deepEqual(pondCommand(input),input);
 assert.deepEqual(pondCommand({...input,together:false}),{...input,together:false});
 const solo={...input};delete solo.together;
 assert.deepEqual(pondCommand(solo),solo);
 for(const together of ['true',1,{},null])assert.equal(pondCommand({...input,together}),null);
});
