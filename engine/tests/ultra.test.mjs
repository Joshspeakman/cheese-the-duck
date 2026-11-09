import test from 'node:test';
import assert from 'node:assert/strict';
import { LivingWorld } from '../client/ultra-world.mjs';
import { W,H,palette } from '../client/ultra-grid.mjs';
import { duckArt,mirror } from '../client/ultra-art.mjs';
import { BIOMES,LOCATIONS,scene } from './scenes.mjs';
const pixels = (world,s,t=2) => {const {grid}=world.render(s,t);return Buffer.concat([Buffer.from(grid.chars),Buffer.from(grid.colors)]);};
test('every biome, season, weather and expression renders printable ASCII with valid palette indices',()=>{
 const world=new LivingWorld();
 const states=['idle','walking','sleeping','eating','playing','quack','happy','sad','cleaning','petting','swimming','diving','stretching','yawning','jumping','scared','thinking','dancing','singing','pecking','flapping','preening','napping','curious','waddle_fast','dizzy','proud','sneaking'];
 const weather=['sunny','cloudy','rainy','stormy','foggy','snowy','windy','rainbow'];
 for(const [i,biome] of BIOMES.entries())for(const season of ['spring','summer','fall','winter'])for(const [j,state] of states.entries()){
  const s=scene({biome,location:LOCATIONS[i],season,hour:j%24,weather:weather[j%8]});s.duck.state=state;
  const {grid,palette}=world.render(s,j*.17);
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
 const a=duckArt('idle',1);assert.notDeepEqual(a,duckArt('sleeping',1));assert.notDeepEqual(a,duckArt('eating',1));
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
