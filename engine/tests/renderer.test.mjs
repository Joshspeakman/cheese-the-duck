import test from 'node:test';
import assert from 'node:assert/strict';
import { decodeLine } from '../client/renderer.mjs';
test('speech and extended ASCII are passed verbatim without markup interpretation', () => {
 const text = 'What the fuck? <script> │';
 assert.equal(decodeLine([[text, '#fff', '#000', 0]], 100).map(c => c[0]).join(''), text);
});
test('inverse selection, clipping and unicode glyphs occupy independent cells', () => {
 assert.deepEqual(decodeLine([['A😀B', '#abc', '#123', 4]], 2), [['A','#123','#abc',4],['😀','#123','#abc',4]]);
});
