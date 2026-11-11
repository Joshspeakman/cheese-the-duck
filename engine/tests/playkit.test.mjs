import test from 'node:test';import assert from 'node:assert/strict';
import {PLAYKIT_BLUEPRINTS} from '../client/playkit-workshop.mjs';
import {PLAYKIT_ROUTINES,PLAYKIT_CONTROLS,playkitPose,playkitGeometry} from '../client/playkit-routines.mjs';
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';import {characterSprite} from '../client/ultra-characters.mjs';import {GUEST_CAST} from '../client/guest-cast.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';import {scene} from './scenes.mjs';
const ages=['hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'],entries=Object.entries(PLAYKIT_BLUEPRINTS);
const work=(id,f)=>({id,elapsed:PLAYKIT_ROUTINES[id].duration*f,start:PLAYKIT_CONTROLS});
test('eight playthings have bounded distinct construction and native control states',()=>{
 const signatures=new Set();for(const [id]of entries){const m=itemSprite(id,0);signatures.add(m.art.join('\n'));assert.equal(m.construction,'playkit-v1');assert.deepEqual(m,itemSprite(id,1000),'catalogue previews cannot operate an owned toy');}
 assert.equal(signatures.size,8);
 for(const [id,s]of Object.entries(PLAYKIT_ROUTINES))for(let n=0;n<=40;n++){
  const item=entries.find(([,p])=>p.type===s.type)[0],w=work(id,n/40),pose=playkitPose(w),opts={pose:{playkit:pose},state:{playkit:{bubbles:[{age:4,lane:3,size:1.7}],waxes:4,phase:1.5}}},before=JSON.stringify(opts),m=itemSprite(item,0,opts);
  assert(!m.clipped,id+' '+n);assert(m.art.every((row,y)=>/^[ -~]*$/.test(row)&&row.length===m.width&&m.tones[y].length===m.width));assert(m.fills.every(f=>f.x>=0&&f.y>=0&&f.w>0&&f.x+f.w<=m.width&&f.y<m.art.length));assert.equal(JSON.stringify(opts),before);
  for(const k in PLAYKIT_CONTROLS)assert.equal(pose[k],playkitPose(w,false)[k],id+' reduced motion retains actual mechanics');
 }
});
test('hatched ages and all visitor rigs preserve body scale and physical toy contact',()=>{
 const actors=[...ages.map(stage=>({stage})),...Object.values(GUEST_CAST).map(p=>({id:p.id,castId:p.id,visitor:true}))];let cases=0;
 for(const actor of actors)for(const [id,s]of Object.entries(PLAYKIT_ROUTINES))for(const f of [.2,.4,.6,.8]){
  const item=entries.find(([,p])=>p.type===s.type)[0],routine=work(id,f),pose=playkitPose(routine),home={...itemSprite(item,0,{pose:{playkit:pose}}),x:100,y:80,scale:itemWorldScale(item)},c={...characterSprite({...actor,state:'idle',facing:true,performance:{kind:'playkit',routine}},0,actor.visitor),x:95,y:80};
  const before=JSON.stringify({home,c}),g=playkitGeometry(home,{character:c,inside:1},6,9);assert.equal(g.character.scale,c.scale);assert(!c.clipped,id+' '+(actor.stage||actor.id));assert(g.points.every(p=>Number.isFinite(p.x+p.y)));
  if(pose.contact===1&&['hand','cloth'].includes(pose.tool)&&c.rig?.species!=='butterfly'){
   assert(Math.hypot(g.tip.x-g.target.x,g.tip.y-g.target.y)<1e-8,id+' contact');assert(Math.abs(g.hand.x-g.target.x)<=4*g.cw,id+' horizontal reach');assert(Math.abs(g.hand.y-g.target.y)<=8*g.cw*1.5,id+' vertical reach '+(actor.stage||actor.id));
  }
  assert.equal(JSON.stringify({home,c}),before);cases++;
 }
 assert.equal(cases,9408);
});
test('paused portable play remains at its put-down position and twin copies stay distinct',()=>{
 const plan={kind:'item',target:'yo_yo',instance:'a',phase:'act',progress:.5,elapsed:10,duration:24,destination:[60,24],playkit_work:work('yoyo_walk',.5)};
 const s=scene({items:[{id:'yo_yo',instance:'a',x:60,y:24},{id:'yo_yo',instance:'b',x:90,y:24}],living:{ecology:{},objects:{},instances:{a:{playkit:{}},b:{playkit:{}}},plan}}),w=new LivingWorld();w.render(s,0,.1);assert.equal(w.objects[0].players.length,1);assert(!w.objects[1].players);assert(!w.characters.some(c=>c.cheese));
 s.items[0].instance='replacement';w.render(s,1,.1);assert(!w.objects[0].players);assert(w.characters.some(c=>c.cheese));
 s.items=[];s.living.plan={...plan,target:'bubble_wand',instance:null,playkit_work:{...work('wand_breath',.5),origin:[50,24]}};s.living.objects={bubble_wand:{playkit:{}}};w.render(s,2,.1);const first=w.objects[0];assert(first.portable&&first.players.length);
 s.living.plan.paused=true;s.duck.x+=30;w.render(s,100,.1);assert.equal(w.objects[0].x,first.x);assert.deepEqual(w.objects[0].art,first.art);assert.deepEqual(w.objects[0].players[0].character.art,first.players[0].character.art);
 s.living.plan=null;w.render(s,101,.1);assert(!w.objects.some(o=>o.id==='bubble_wand'));
});
