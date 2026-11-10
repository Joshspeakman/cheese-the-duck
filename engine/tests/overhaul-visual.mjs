import {SceneCanvas} from '../client/ultra-renderer.mjs';
import {characterSprite,drawCharacter} from '../client/ultra-characters.mjs';
import {DUCK_AGES} from '../client/duck-rig.mjs';
import {VISITOR_STYLES} from '../client/visitor-rig.mjs';
import {itemSprite,ItemPainter,catalog} from '../client/ultra-items.mjs';
import {WILDLIFE} from '../client/wildlife.mjs';
import {eventModel,EVENT_CATALOG,EVENT_ASSETS} from '../client/event-art.mjs';
import {PondJournal} from '../client/pond-journal.mjs';
window.cheese={input:command=>window.lastCommand=command};
window.runOverhaul=async function(s){
 const images={},errors=[];const make=(w,h)=>{const c=document.createElement('canvas');c.width=w;c.height=h;c.getContext('2d').fillStyle='#14251f';c.getContext('2d').fillRect(0,0,w,h);return c;};
 for(const [name,hour,weather] of [['day',12,'sunny'],['night',23,'clear_cold'],['rain',14,'heavy_rain'],['snow',10,'snowy']]){
  const c=new SceneCanvas();c.resize(1440,800);const scene=structuredClone(s);scene.hour=hour;scene.weather=weather;scene.season=name==='snow'?'winter':'spring';scene.living.ecology.snow=name==='snow'?.65:0;scene.living.ecology.wetness=name==='rain'?.8:.2;
  scene.visitor={id:'scholar',name:'Ada',personality:'scholarly',state:'reading',x:85,y:24};scene.duck.x=65;scene.duck.y=24;
  c.draw(scene,1.8,1/30);images[name]=c.canvas.toDataURL();
 }
 const cast=make(1440,1100),cc=cast.getContext('2d');
 [...DUCK_AGES.map(a=>({stage:a.id,name:a.name||a.id})),...Object.keys(VISITOR_STYLES).map(personality=>({personality,name:personality,stage:'adult'}))].forEach((duck,i)=>{
  const x=(i%5)*288,y=Math.floor(i/5)*270;cc.save();cc.translate(x,y);const m=characterSprite(duck,1,!!duck.personality);drawCharacter(cc,{...m,name:'',x:18,y:28},8,8,'#14251f');cc.fillStyle='#ebce94';cc.font='14px Menlo';cc.fillText(duck.name,24,245);cc.restore();
 });images.cast=cast.toDataURL();
 const wild=make(1500,Math.ceil(Object.keys(WILDLIFE).length/6)*170),wc=wild.getContext('2d');Object.keys(WILDLIFE).forEach((asset,i)=>{wc.save();wc.translate(i%6*250,Math.floor(i/6)*170);const m=eventModel({id:asset,asset},1,true);drawCharacter(wc,{...m,x:22,y:24},5,5,'#14251f');wc.fillStyle='#ebce94';wc.font='12px Menlo';wc.fillText(asset,10,155);wc.restore();});images.wildlife=wild.toDataURL();
 const ids=['toy_ball','fountain_grand','cherry_tree','robot_butler','toy_piano','wooden_cottage','portal','hat_chef','basic_nest','stone_hammer','wind_chimes','treasure_chest'],sheet=make(1500,1100),ic=sheet.getContext('2d'),painter=new ItemPainter();
 ids.forEach((id,i)=>{ic.save();ic.translate(i%4*375,Math.floor(i/4)*360);const m=itemSprite(id,1.2,{state:{wetness:.3,bond:.8},interaction:{progress:.5}});painter.draw(ic,m,185,285,Math.min(9,320/(m.width*m.detailScale)),{surface:'#14251f'});ic.fillStyle='#ebce94';ic.font='14px Menlo';ic.fillText(catalog.find(i=>i.id===id)?.name||id,18,325);ic.restore();});images.items=sheet.toDataURL();
 for(const [id,e] of Object.entries(EVENT_CATALOG))for(const t of [0,.3,.7]){const m=eventModel({id,family:e.animator,art:e.original},t);if(m.art.some((r,y)=>/[^ -~]/.test(r)||r.length!==m.tones[y].length))errors.push(id);}
 const journal=new PondJournal();journal.update({scene:s});journal.show();window.journal=journal;
 return {images,errors,events:Object.keys(EVENT_CATALOG).length,assets:Object.keys(EVENT_ASSETS).length,wildlife:Object.keys(WILDLIFE).length};
};
