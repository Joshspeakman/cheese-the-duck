import test from 'node:test';
import assert from 'node:assert/strict';
import { LivingWorld } from '../client/ultra-world.mjs';
import { W,H,palette } from '../client/ultra-grid.mjs';
import { mirror } from '../client/ultra-art.mjs';
import { characterSprite,VISITOR_ART } from '../client/ultra-characters.mjs';
import { BIOMES,LOCATIONS,scene } from './scenes.mjs';
const pixels = (world,s,t=2) => {const {grid,characters}=world.render(s,t);return Buffer.concat([Buffer.from(grid.chars),Buffer.from(grid.colors),Buffer.from(JSON.stringify(characters))]);};
test('every biome, season, weather and expression renders printable ASCII with valid palette indices',()=>{
 const world=new LivingWorld();
 const states=['idle','walking','sleeping','eating','playing','quack','happy','sad','cleaning','petting','swimming','diving','stretching','yawning','jumping','scared','thinking','dancing','singing','pecking','flapping','preening','napping','curious','waddle_fast','dizzy','proud','sneaking'];
 const weather=['sunny','cloudy','rainy','stormy','foggy','snowy','windy','rainbow'];
 for(const [i,biome] of BIOMES.entries())for(const season of ['spring','summer','fall','winter'])for(const [j,state] of states.entries()){
  const s=scene({biome,location:LOCATIONS[i],season,hour:j%24,weather:weather[j%8]});s.duck.state=state;
  const {grid,palette,characters}=world.render(s,j*.17);
  assert.ok(characters.every(c=>c.art.every(line=>/^[ -~]*$/.test(line))));
  assert.equal(grid.chars.length,W*H);assert.equal(palette.length,32);
  assert.ok(grid.chars.every(c=>c>=32&&c<=126));assert.ok(grid.colors.every(c=>c<palette.length));
 }
});
test('worlds are reproducible, visibly distinct, and do not mutate simulation snapshots',()=>{
 const signatures=new Set();
 for(const [i,biome] of BIOMES.entries()){
  const s=scene({biome,location:LOCATIONS[i]}); const before=JSON.stringify(s);
  const a=pixels(new LivingWorld(),s),b=pixels(new LivingWorld(),s);
  assert.deepEqual(a,b);assert.equal(JSON.stringify(s),before);signatures.add(a.toString('base64'));
 }
 assert.equal(signatures.size,9);
});
test('reduced motion freezes all ambient and character effects; animated mode changes',()=>{
 const world=new LivingWorld(),s=scene({motion:false,season:'fall',weather:'stormy',hour:23});s.duck.state='dancing';
 assert.deepEqual(pixels(world,s,1),pixels(world,s,99));
 s.motion=true; assert.notDeepEqual(pixels(world,s,1),pixels(world,s,99));
});
test('night lighting, seasons and accessibility effect flags alter the scene',()=>{
 const s=scene(),base=pixels(new LivingWorld(),s);
 assert.notDeepEqual(palette(s),palette({...s,hour:23}));
 assert.notDeepEqual(palette(s),palette({...s,season:'winter'}));
 assert.notDeepEqual(base,pixels(new LivingWorld(),{...s,particles:false}));
 assert.notDeepEqual(pixels(new LivingWorld(),{...s,weather:'stormy'}),pixels(new LivingWorld(),{...s,weather:'stormy',weatherEffects:false}));
});
test('Cheese retains expressions, directional mirroring, growth and visible cosmetics',()=>{
 const a=characterSprite(scene().duck,1).art;
 assert.notDeepEqual(a,characterSprite({...scene().duck,state:'sleeping'},1).art);
 assert.notDeepEqual(a,characterSprite({...scene().duck,state:'eating'},0).art);
 assert.deepEqual(mirror(mirror(a)),a.map(l=>l.padEnd(Math.max(...a.map(l=>l.length)))));
 const s=scene(),base=pixels(new LivingWorld(),s);
 for(const stage of ['egg','duckling','teen','elder'])assert.notDeepEqual(base,pixels(new LivingWorld(),{...s,duck:{...s.duck,stage}}));
 for(const change of [{hidden:true},{away:true},{facing:false},{cosmetics:{hat:'party_hat'}},{state:'swimming'}])assert.notDeepEqual(base,pixels(new LivingWorld(),{...s,duck:{...s.duck,...change}}));
});
test('placed objects and visitors remain tied to simulation coordinates',()=>{
 const s=scene(),base=pixels(new LivingWorld(),s);
 assert.notDeepEqual(base,pixels(new LivingWorld(),{...s,items:[{id:'nest',x:80,y:20,art:['(_)']}]}));
 assert.notDeepEqual(base,pixels(new LivingWorld(),{...s,visitor:{name:'Friend',x:80,y:20}}));
 const world=new LivingWorld();assert.notDeepEqual(world.project(s,40,10),world.project({...s,camera:{...s.camera,x:10}},40,10));
});

test('enhanced drawings retain original faces and accessories with more contour detail',()=>{
 const body=characterSprite(scene().duck,1);
 assert.ok(body.art.length>=7);assert.ok(body.width>=12);assert.ok(body.scale>1);
 assert.equal(body.design,'bedhead-bandit');assert.ok(body.art.join('').includes('>'));
 const faces=new Set();
 for(const [personality,art] of Object.entries(VISITOR_ART)){
  const sprite=characterSprite({name:personality,personality,art},1,true);
  assert.ok(sprite.art.length>art.length);assert.ok(sprite.scale>1);
  assert.ok(sprite.art.every((row,i)=>row.length===sprite.tones[i].length));
  faces.add(sprite.art.join('\n'));
 }
 assert.equal(faces.size,8);
 const scholar=characterSprite({personality:'scholarly',art:VISITOR_ART.scholarly},1,true);
 assert.ok(scholar.art.some(row=>row.includes('[O]-[O]')),'scholar keeps glasses');
 const mystery=characterSprite({personality:'mysterious',art:VISITOR_ART.mysterious},1,true);
 assert.ok(mystery.art.some(row=>row.includes('? _ ?')),'masked eyes stay recognizable');
 const gift=characterSprite({personality:'generous',art:['(o.o)[#]']},1,true);
 assert.ok(gift.art.some(row=>row.includes('#')),'gift action retains its prop');
 const happy=characterSprite({personality:'adventurous',art:['(^.^)']},1,true);
 assert.ok(happy.art.some(row=>row.includes('^ . ^')),'original expression drives the redraw');
});
test('enhanced character animation includes wing, step, swim and prop frames',()=>{
 for(const state of ['walking','dancing','flapping','swimming','eating','sleeping']){
  const duck={...scene().duck,state};
  assert.notDeepEqual(characterSprite(duck,.05),characterSprite(duck,.55),state);
 }
 const scholar={personality:'scholarly',art:VISITOR_ART.scholarly};
 assert.notDeepEqual(characterSprite(scholar,.05,true),characterSprite(scholar,.55,true));
});
