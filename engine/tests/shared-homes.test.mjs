import test from 'node:test';
import assert from 'node:assert/strict';
import ROOMS from '../client/animation/home-rooms.json' with {type:'json'};
import {itemSprite,itemWorldScale} from '../client/ultra-items.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {GUEST_CAST} from '../client/visitor-rig.mjs';
import {DUCK_AGES} from '../client/duck-rig.mjs';
import {occupiedGeometry} from '../client/residence-stage.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
import {scene} from './scenes.mjs';
import COMPANY from '../client/animation/home-company.json' with {type:'json'};

test('furnished shared rooms preserve their bounds and provide separate fitting places for the whole cast',()=>{
 const residents=[...DUCK_AGES.map(a=>characterSprite({stage:a.id,state:'sleeping'},0)),...Object.keys(GUEST_CAST).map(id=>characterSprite({id,state:'sleeping'},0,true))];
 for(const [id,room] of Object.entries(ROOMS)){
  const home={...itemSprite(id,1,{interaction:{phase:'act',kind:'rest',shared:true},context:{season:'winter',hour:22,weather:'rainy'}}),x:100,y:80,scale:itemWorldScale(id)};
  assert.equal(home.clipped,false,id);assert.equal(home.anchors.slots.length,room.capacity,id);
  const before=JSON.stringify(home);
  for(const c of residents)for(let slot=0;slot<room.capacity;slot++){
   const g=occupiedGeometry(home,{...c,x:100,y:80},1,6,9,slot);
   assert(g.character.scale>0&&g.character.scale<=c.scale,id+' '+c.profileId);
   assert(Number.isFinite(g.character.x)&&Number.isFinite(g.character.y));
   if(g.clip){
    const unit=6*g.character.scale,ch=unit*1.5;
    const left=g.character.x*6-c.anchorX*unit+(c.offsetX||0)*unit,top=g.character.y*9-c.groundRow*ch+(c.offsetY||0)*unit;
    for(let y=0;y<c.art.length;y++)for(let x=0;x<c.art[y].length;x++)if(c.art[y][x]!==' '){
     assert(left+x*unit>=g.clip.x-.01&&left+(x+1)*unit<=g.clip.x+g.clip.w+.01,id+' horizontal ink fit '+c.profileId);
     assert(top+y*ch>=g.clip.y-.01&&top+(y+1)*ch<=g.clip.y+g.clip.h+.01,id+' vertical ink fit '+c.profileId);
    }
   }
   if(slot){const previous=occupiedGeometry(home,{...c,x:100,y:80},1,6,9,slot-1);assert(g.character.x>previous.character.x,id);}
  }
  assert.equal(JSON.stringify(home),before,'staging cannot mutate the room');
 }
});

test('shared room acting keeps a constant body scale through gestures and head turns',()=>{
 const home={...itemSprite('mud_hut',0,{interaction:{shared:true}}),x:100,y:80,scale:itemWorldScale('mud_hut')};
 for(const source of [...DUCK_AGES.map(a=>({stage:a.id})),...Object.keys(GUEST_CAST).map(id=>({id}))])for(const role of ['a','b']){
  const scales=new Set();
  for(const kind of Object.keys(COMPANY))for(let i=0;i<=20;i++){
   const character={...characterSprite({...source,facing:role==='a',performance:{kind,role,progress:i/20}},i*.4,Boolean(source.id)),x:100,y:80};
   const g=occupiedGeometry(home,character,1,6,9,role==='a'?0:1);
   scales.add(g.character.scale);
   assert(g.character.scale<=character.scale);
  }
  assert.equal(scales.size,1,JSON.stringify(source)+' '+role+' must not pulse in size');
 }
});

test('visitor residence stages only entered visitors in the actual matching item instance',()=>{
 const guest={id:'friendly_goose',name:'Goose',x:62,y:24,state:'sleeping'};
 const residence={actor:guest.id,id:'barn',destination:[60,24],slot:1,capacity:3,phase:'inside',elapsed:10};
 const base=scene({visitor:guest,items:[{id:'barn',x:10,y:24},{id:'barn',x:60,y:24}],living:{ecology:{},objects:{},projects:[],garden:[],minds:{residences:[residence]}}});
 const w=new LivingWorld();let result=w.render(base,1,.03);
 assert.equal(result.objects.filter(o=>o.occupants?.length).length,1);
 assert.equal(result.objects.find(o=>o.occupants?.length).worldPosition[0],60);
 assert(!result.characters.some(c=>c.id===guest.id));
 for(const change of [{phase:'approach'},{destination:[40,24]},{actor:'absent'}]){
  result=w.render({...base,living:{...base.living,minds:{residences:[{...residence,...change}]}}},1,.03);
  assert(!result.objects.some(o=>o.occupants?.length));assert(result.characters.some(c=>c.id===guest.id));
 }
});

test('shared shelter acting freezes under reduced motion without moving the actual occupants',()=>{
 const plan={kind:'rest',target:'barn',phase:'act',progress:.5,residence:{destination:[60,24],slot:0,inside:true}};
 const performance={a:'cheese',b:'friendly_goose',home:'barn',performance:'roof_rhythm',phase:'act',elapsed:8,duration:26};
 const residence={actor:'friendly_goose',id:'barn',destination:[60,24],slot:1,capacity:3,phase:'inside',elapsed:10};
 const s=scene({motion:false,visitor:{id:'friendly_goose',x:60,y:24,state:'idle'},items:[{id:'barn',x:60,y:24}],living:{plan,ecology:{},objects:{},projects:[],garden:[],minds:{residences:[residence],performances:[performance]}}});
 const w=new LivingWorld(),before=JSON.stringify(s),first=w.render(s,1,.1).objects;
 const next=w.render({...s,living:{...s.living,minds:{...s.living.minds,performances:[{...performance,elapsed:22}]}}},15,.1).objects;
 assert.deepEqual(first,next);assert.equal(JSON.stringify(s),before);
 assert.equal(first[0].occupants.length,2);
});
