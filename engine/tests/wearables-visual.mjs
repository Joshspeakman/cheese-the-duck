import {wearableCatalog,wearableSpec} from '../client/wearables.mjs';
import {characterSprite,drawCharacter} from '../client/ultra-characters.mjs';
import {emotionPortrait} from '../client/emotion-portrait.mjs';
import {STAGES} from '../client/scruffy-sprites.mjs';
import {DisplayRenderer} from '../client/ultra-renderer.mjs';
const assert=(ok,msg)=>{if(!ok)throw Error(msg);};
const pixels=c=>new Uint8Array(c.getContext('2d').getImageData(0,0,c.width,c.height).data);
const equal=(a,b)=>a.length===b.length&&a.every((v,i)=>v===b[i]);
function sheet(w,h){const c=document.createElement('canvas');c.width=w;c.height=h;c.getContext('2d').fillStyle='#10262c';c.getContext('2d').fillRect(0,0,w,h);return c;}
function duck(ctx,data,x,y,cw,time){const m=characterSprite(data,time);drawCharacter(ctx,{...m,scale:1,x:x/cw,y:y/cw},cw,cw,'#10262c');return m;}
window.checkWearables=frames=>{
 const images={};
 for(let start=0;start<wearableCatalog.length;start+=24){
  const c=sheet(1600,1320),ctx=c.getContext('2d');
  wearableCatalog.slice(start,start+24).forEach((item,i)=>{
   const x=i%4*400,y=Math.floor(i/4)*220;
   duck(ctx,{stage:'adult',state:'walking',cosmetics:{item:item.id}},x+200,y+180,7.5,.3);
   ctx.font='14px Menlo';ctx.textAlign='center';ctx.fillStyle=wearableSpec(item.id).color;ctx.fillText(item.name,x+200,y+208,380);
  });images['wardrobe-'+(start/24+1)]=c.toDataURL();
 }
 const outfits=[{head:'hat_red',neck:'scarf_red',back:'backpack_tiny'},
  {head:'hat_wizard',body:'wizard_robe',held:'magic_wand'},
  {head:'hat_crown',face:'monocle',neck:'bow_tie_blue',body:'tuxedo'},
  {head:'hat_party',back:'cape_superhero',feet:'rain_boots'},
  {head:'flower_crown',wings:'wings_fairy'},
  {head:'space_helmet',neck:'scarf_striped'}];
 const poses=['idle','walking','eating','swimming','hopping','sleeping','flapping','dancing'];
 const animation=sheet(1760,outfits.length*245),ctx=animation.getContext('2d');
 outfits.forEach((cosmetics,row)=>poses.forEach((state,col)=>{
  duck(ctx,{stage:'adult',state,cosmetics},col*220+110,row*245+205,7,.45);
  ctx.font='12px Menlo';ctx.textAlign='center';ctx.fillStyle='#cdd5bd';ctx.fillText(state,col*220+110,row*245+232);
 }));images['outfits-in-motion']=animation.toDataURL();
 const clothes=sheet(1800,1160),cl=clothes.getContext('2d');
 ['sweater_cozy','autumn_cozy_sweater','hawaiian_shirt','summer_hawaiian_shirt'].forEach((id,row)=>
  [['hatchling','idle'],['duckling','walking'],['adult','idle'],['adult','eating'],['adult','sleeping'],['adult','flapping']].forEach(([stage,state],col)=>{
   duck(cl,{stage,state,cosmetics:{body:id}},col*300+150,row*290+220,8.5,.6);
   cl.font='13px Menlo';cl.textAlign='center';cl.fillStyle=wearableSpec(id).color;cl.fillText(wearableSpec(id).name,col*300+150,row*290+246,285);
   cl.fillStyle='#cdd5bd';cl.fillText(stage+' · '+state,col*300+150,row*290+267);
  }));images['shaped-shirts-and-knits']=clothes.toDataURL();
 const ages=sheet(1440,960),ac=ages.getContext('2d');
 STAGES.forEach(({id,name},i)=>{
  duck(ac,{stage:id,state:'idle',cosmetics:{head:'hat_red',neck:'scarf_red',back:'backpack_tiny'}},i%3*480+240,Math.floor(i/3)*320+258,12,0);
  ac.font='18px Menlo';ac.textAlign='center';ac.fillStyle='#e7d5a2';ac.fillText(name,i%3*480+240,Math.floor(i/3)*320+298);
 });images['fitted-all-ages']=ages.toDataURL();
 const emotions=sheet(1200,660),ec=emotions.getContext('2d');
 ['happy','content','grumpy','sad','miserable','dramatic','petty','ecstatic'].forEach((mood,i)=>{
  const m=emotionPortrait({stage:'adult'},{mood},.5),x=i%4*300,y=Math.floor(i/4)*330;
  drawCharacter(ec,{...m,x:(x+150)/8,y:(y+245)/8},8,8,'#10262c');ec.font='16px Menlo';ec.textAlign='center';ec.fillStyle='#f4ce82';ec.fillText(mood,x+150,y+290);
 });images['expressions-only']=emotions.toDataURL();
 const frame=structuredClone(frames.pond);frame.scene.duck.cosmetics=outfits[0];frame.scene.duck.state='walking';frame.scene.hour=12;frame.ui.modal=null;
 const canvas=document.createElement('canvas'),display=new DisplayRenderer(canvas);display.resize(frame.cols,frame.rows,.8,{width:1500,height:993,uiScale:.993});display.draw(frame,450);images['fitted-in-game']=canvas.toDataURL();
 frame.scene.motion=false;frame.ui.motion=false;display.draw(frame,1000);const frozen=pixels(canvas);display.draw(frame,9000);assert(equal(frozen,pixels(canvas)),'reduced motion animates worn accessories');
 frame.scene.duck.cosmetics={};display.draw(frame,1000);const fresh=new DisplayRenderer(document.createElement('canvas'));fresh.resize(frame.cols,frame.rows,.8,{width:1500,height:993,uiScale:.993});fresh.draw(frame,1000);assert(equal(pixels(canvas),pixels(fresh.canvas)),'unequipping leaves old clothing on Cheese');
 return {images,items:wearableCatalog.length,checks:['all wearable contact sheets','six combined outfits across eight actions','all nine ages','expression-only panel','reduced motion','unequip restoration']};
};
