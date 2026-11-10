import { catalog,itemSprite,ItemPainter } from '../client/ultra-items.mjs';
import { DisplayRenderer } from '../client/ultra-renderer.mjs';
const assert=(ok,text)=>{if(!ok)throw Error(text);};
const pixels=c=>new Uint8Array(c.getContext('2d').getImageData(0,0,c.width,c.height).data);
const eq=(a,b)=>a.every((v,i)=>v===b[i]);
window.checkItems=frames=>{
  const images={},painter=new ItemPainter(),count=30;
  for(let start=0;start<catalog.length;start+=count){
    const canvas=document.createElement('canvas');canvas.width=1800;canvas.height=1500;const ctx=canvas.getContext('2d');ctx.fillStyle='#0b1d23';ctx.fillRect(0,0,1800,1500);
    catalog.slice(start,start+count).forEach((item,i)=>{
      const x=i%6*300,y=Math.floor(i/6)*300,model=itemSprite(item.id,2),cw=Math.min(10,260/(model.width+2),170/((model.art.length+2)*1.5));
      ctx.fillStyle='#132b30';ctx.fillRect(x+8,y+8,284,284);
      painter.draw(ctx,model,x+150,y+204,cw);
      ctx.fillStyle=model.rarity;ctx.textAlign='center';ctx.font='14px Menlo';ctx.fillText(item.name,x+150,y+240,270);
      ctx.fillStyle='#8ba5a2';ctx.font='11px Menlo';ctx.fillText(item.id,x+150,y+266,270);
    });
    images['catalog-'+String(start/count+1).padStart(2,'0')]=canvas.toDataURL();
  }
  const canvas=document.createElement('canvas'),display=new DisplayRenderer(canvas),s=structuredClone(frames.pond);
  s.scene.items=[['tree_cherry',15,19],['fountain_grand',30,29],['toy_skateboard',55,30],['chair_throne',88,34],['tiki_torch',98,24],['portal',117,30]].map(([id,x,y])=>({id,x,y}));
  s.scene.structures=[{id:'wooden_cottage',x:107,y:16}];
  s.scene.duck.x=62;s.scene.duck.y=30;s.ui.modal=null;
  display.resize(s.cols,s.rows,.8,{width:1500,height:993,uiScale:.993});
  const portraits={};
  for(const [label,hour,weather] of [['dawn',6,'sunny'],['day',12,'sunny'],['dusk',18.5,'sunny'],['night',23,'sunny'],['rain',16,'rainy']]){
    s.scene.hour=hour;s.scene.weather=weather;display.scene.effects.level='vivid';display.draw(s,2000);images['world-'+label]=canvas.toDataURL();
    assert(display.scene.light.hour===hour&&display.interface.emotionHour===hour,`${label} world/portrait time does not match the simulation`);
    const portrait=document.createElement('canvas');portrait.width=608;portrait.height=298;
    const ux=canvas.width/display.interface.width,uy=canvas.height/display.interface.height;
    portrait.getContext('2d').drawImage(canvas,(display.interface.width-334)*ux,117*uy,304*ux,149*uy,0,0,608,298);
    portraits[label]=pixels(portrait);images['portrait-'+label]=portrait.toDataURL();
  }
  assert(!eq(portraits.day,portraits.night)&&!eq(portraits.day,portraits.dusk)&&!eq(portraits.day,portraits.dawn),'emotion portrait background did not change with the game clock');
  s.scene.motion=false;s.ui.motion=false;display.draw(s,1000);const first=pixels(canvas);display.draw(s,9000);assert(eq(first,pixels(canvas)),'reduced motion changed props or light');
  display.scene.effects.level='off';display.draw(s,1000);assert(!eq(first,pixels(canvas)),'effects switch did not change output');images['world-effects-off']=canvas.toDataURL();
  const withItems=pixels(canvas);s.scene.items=[];s.scene.structures=[];display.draw(s,1000);assert(!eq(withItems,pixels(canvas)),'placed items did not render');
  const fresh=new DisplayRenderer(document.createElement('canvas'));fresh.resize(s.cols,s.rows,.8,{width:1500,height:993,uiScale:.993});fresh.scene.effects.level='off';fresh.draw(s,1000);assert(eq(pixels(fresh.canvas),pixels(canvas)),'removed props leave trails');
  const previewChecks=[];
  for(const width of [920,1500,1920]){
    display.resize(s.cols,s.rows,.8,{width,height:993,uiScale:Math.min(width/1440,.993)});
    for(const name of ['shop','inventory','craft','build']){
      const frame=frames[name];display.draw(frame,2000);const d=display.interface.visibleDocument;
      assert(d&&d.x>=0&&d.x+d.w<=display.interface.width,`${name} preview out of bounds`);
      if(['shop','craft','build'].includes(name))assert(d.preview,`${name} missing preview`);
      assert(d.rows.every(row=>row.cells.length*(d.rows.length>32?17:19)*.61<=d.textWidth),`${name} preview overlaps text`);
      if(width===1500)images['menu-'+name]=canvas.toDataURL();previewChecks.push([name,width,d.preview]);
    }
  }
  const actualHour=s.scene.hour;s.scene.motion=false;s.ui.motion=false;
  s.scene.hour=12;const snapshot=JSON.stringify(s);display.draw(s,2000);
  const daylight=pixels(display.scene.canvas);
  assert(JSON.stringify(s)===snapshot,'rendering changed the game clock or snapshot');
  assert(display.interface.emotionHour===12&&display.scene.light.hour===12,'portrait and world clocks differ at noon');
  s.scene.hour=23;display.draw(s,2000);
  assert(display.interface.emotionHour===23&&display.scene.light.hour===23,'portrait and world clocks differ at night');
  const nightlight=pixels(display.scene.canvas);
  const luminance=data=>{let total=0;for(let i=0;i<data.length;i+=4)total+=.2126*data[i]+.7152*data[i+1]+.0722*data[i+2];return total/(data.length/4);};
  const dayBrightness=luminance(daylight),nightBrightness=luminance(nightlight);
  assert(dayBrightness>nightBrightness*2.1,'daytime still reads like night');
  let clipped=0;for(let i=0;i<daylight.length;i+=4)if(daylight[i]>248&&daylight[i+1]>248&&daylight[i+2]>248)clipped++;
  assert(clipped/(daylight.length/4)<.01,'daylight blows out the scene highlights');
  assert(display.scene.atlas.size<=4096,'contrast-adjusted glyph cache unbounded');
  s.scene.hour=actualHour;
  // Full catalog in one scene stresses sorting and bounded caches without saving.
  s.scene.items=catalog.slice(0,100).map((item,i)=>({id:item.id,x:(i%20)*6,y:8+Math.floor(i/20)*6}));
  display.resize(s.cols,s.rows,.8,{width:1500,height:993,uiScale:.993});
  const times=[];for(let n=0;n<30;n++){const t=performance.now();display.draw(s,1000+n*33);times.push(performance.now()-t);}times.sort((a,b)=>a-b);
  assert(display.scene.items.cache.size<=384,'sprite cache unbounded');
  return {images,items:catalog.length,previewChecks,dayBrightness,nightBrightness,median100PropsMs:times[15],p95Ms:times[28]};
};
