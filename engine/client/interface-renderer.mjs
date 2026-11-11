import { portraitEnvironment } from './portrait-environment.mjs';
import { sceneLight,mixColor } from './scene-lighting.mjs';
import { characterSprite, drawCharacter } from './ultra-characters.mjs';
import { itemSprite,ItemPainter,selectedItem,rarityColor } from './ultra-items.mjs';
import { emotionPortrait } from './emotion-portrait.mjs';
import { documentRows, documentTitle, themeFor, menuWindow, clamp, plain, cropDocument } from './interface-model.mjs';
import { HudLayout } from './hud-layout.mjs';

const C={ink:'#ebe6cf',muted:'#a2b6a2',dim:'#5e7e73',gold:'#f4ce82',mint:'#9bd9b9',blue:'#97cdd8',rose:'#efa997',bg:'#0d1e21',panel:'#13282b',line:'#345654'};
const BASE_COLORS={...C};
const THEMES={
 duck:{label:'LIFE AT THE POND',color:C.gold,art:['   \\|/    ','  (o .o)>  ','  /)___)   ',"   \" \"    "]},
 workshop:{label:'THE POND WORKSHOP',color:C.gold,art:['  /_______\\ ','  | $ | $ | ','  |___|___| ','  [_______] ']},
 settings:{label:'MAKE YOURSELF AT HOME',color:C.blue,art:['   .-|- .   ','  / (o) \\  ','  +--+--+   ','   `-|-`    ']},
 world:{label:'OUT BEYOND THE REEDS',color:C.mint,art:['    /\\     ',' /\\/  \\ /\\','/  / ~  V  \\','  ~~~  ~~~  ']},
 play:{label:'A LITTLE MISCHIEF',color:C.rose,art:['   .----.   ','  / o  o \\ ',' |  .--.  | ','  \\/    \\/ ']},
 journal:{label:'THE STORIES WE KEEP',color:'#c4b1e5',art:['  __ __ __  ',' /__V__V_/| ',' |..|..|.|| ',' |__|__|_|/ ']},
 talk:{label:'A WORD WITH CHEESE',color:C.gold,art:[' .--------. ',' | ... !  | ',' `----. .-` ','       V    ']},
 warning:{label:'TAKE A MOMENT',color:C.rose,art:['     /\\    ','    / !\\   ','   /  ! \\  ','  /______\\ ']},
};
const LOGO=[
'  ____  _   _  _____  _____  ____   _____',
' / ___|| | | || ____|| ____|/ ___| | ____|',
'| |    | |_| ||  _|  |  _|  \\___ \\ |  _|',
'| |___ |  _  || |___ | |___  ___) || |___',
' \\____||_| |_||_____||_____||____/ |_____|',
];
const friendly=value=>String(value||'').replaceAll('_',' ');

export class InterfaceRenderer {
  constructor(){this.hits=[];this.scroll=0;this.docKey='';this.selectedLine=-1;this.visibleDocument=null;this.cache=new Map();this.layout=new HudLayout();this.hudOpacity=1;this.hudRects=[];this.itemPainter=new ItemPainter();}
  get panelsOpen(){return this.layout.visible('menu');}
  set panelsOpen(value){this.layout.show('menu',value);this.layout.show('care',value);}
  text(ctx,text,x,y,size=16,color=C.ink,align='left',weight=400,font='"Avenir Next", sans-serif'){
    ctx.font=`${weight} ${size}px ${font}`;ctx.textAlign=align;ctx.textBaseline='middle';ctx.fillStyle=color;ctx.fillText(String(text),x,y);
  }
  fitText(ctx,text,x,y,width,size=16,color=C.ink){
    const length=Array.from(String(text)).length;
    this.text(ctx,text,x,y,Math.min(size,width/Math.max(1,length)*1.62),color);
  }
  rule(ctx,x,y,w,color=C.line,char='-'){
    ctx.save();ctx.strokeStyle=color;ctx.lineWidth=char==='='?2:1;ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x+w,y);ctx.stroke();ctx.restore();
  }
  panel(ctx,x,y,w,h,color=C.line,fill=C.panel){
    ctx.save();ctx.shadowColor='#020e12a0';ctx.shadowBlur=18;ctx.shadowOffsetY=5;
    ctx.fillStyle=fill;ctx.beginPath();ctx.roundRect(x,y,w,h,14);ctx.fill();ctx.shadowColor='transparent';
    ctx.strokeStyle=color;ctx.lineWidth=1;ctx.stroke();
    ctx.strokeStyle='#e6ce9625';ctx.beginPath();ctx.roundRect(x+4,y+4,w-8,h-8,10);ctx.stroke();
    ctx.fillStyle='#e7cc9320';for(const px of [x+11,x+w-11]){ctx.beginPath();ctx.arc(px,y+12,1.5,0,Math.PI*2);ctx.fill();}
    ctx.restore();
  }
  art(ctx,lines,x,y,size,color){lines.forEach((line,i)=>this.text(ctx,line,x,y+i*size*1.15,size,color,'left',400,'Menlo, monospace'));}
  button(ctx,label,x,y,w,h,selected=false,command=null){
    ctx.fillStyle=selected?'#405943':'#203933';ctx.beginPath();ctx.roundRect(x,y,w,h,9);ctx.fill();
    this.text(ctx,selected?'◆':'·',x+12,y+h/2,15,selected?C.gold:C.dim);
    this.fitText(ctx,label,x+34,y+h/2,w-64,17,selected?C.gold:C.ink);
    if(selected)this.text(ctx,'›',x+w-22,y+h/2,22,C.gold);
    if(command)this.hits.push({x,y,w,h,command});
  }
  begin(ctx,canvas,frame,viewport){
    this.hits=[];this.hudRects=[];this.visibleDocument=null;
    this.width=viewport?viewport.width/viewport.uiScale:frame.cols*10;
    this.height=viewport?viewport.height/viewport.uiScale:frame.rows*18;
    this.worldFill=Boolean(frame.scene);
    ctx.save();ctx.scale(canvas.width/this.width,canvas.height/this.height);
  }
  draw(ctx,canvas,frame,time,viewport=null){
    if(!frame.ui)return;
    Object.assign(C,BASE_COLORS,frame.ui.highContrast?{ink:'#fffbea',muted:'#d4dfcd',dim:'#a7c5bb',line:'#789b95',panel:'#061619'}:{});
    this.begin(ctx,canvas,frame,viewport);
    const ui=frame.ui,clock=ui.motion===false?0:time/1000;this.time=clock;
    if(ui.state==='title')this.title(ctx,frame,clock);
    else if(frame.scene){
      ctx.save();ctx.globalAlpha*=this.hudOpacity;
      this.hud(ctx,frame,clock);
      ctx.restore();
      if(this.hudOpacity<.15||ui.modal)this.hits=[];
      if(ui.modal)this.document(ctx,ui.modal,ui);
    }else this.fullScreen(ctx,frame,clock);
    ctx.restore();
  }
  portrait(ctx,duck,x,y,size,time,environment=null){
    const sprite=characterSprite(duck,time);const scale=size/(sprite.width*1.8);
    drawCharacter(ctx,{...sprite,x:x/scale,y:y/scale,backdrop:environment?.background,outline:environment?.light.outline},scale,scale,C.panel);
  }
  title(ctx,frame,time){
    const {ui}=frame,W=this.width,H=this.height;
    // The scene behind this is the same living ASCII pond used in play.
    ctx.fillStyle='#071719aa';ctx.fillRect(0,0,W,H);
    this.panel(ctx,42,40,W-84,H-80,C.dim,'#0b1c20d9');
    this.text(ctx,'~  A SMALL DUCK. A VERY LARGE WORLD.  ~',W/2,91,15,C.mint,'center');
    this.art(ctx,LOGO,98,168,24,C.gold);
    this.text(ctx,'T H E   D U C K',395,330,27,C.ink,'center');
    this.rule(ctx,103,375,590,C.dim,'=');
    this.text(ctx,'YOUR POND. HIS RULES.',395,411,16,C.muted,'center');
    const title=ui.title||{options:['New Game','Check for Updates','Quit'],selected:0};
    const y=H*.51,step=57;
    title.options.forEach((label,i)=>this.button(ctx,label,142,y+i*step,505,45,i===title.selected,
      {type:'choose',target:'title',index:i,context:title.options.join('|')}));
    this.panel(ctx,785,150,515,H-340,C.line,'#13282be8');
    this.text(ctx,'// RESIDENT TROUBLEMAKER',820,186,14,C.muted);
    const environment=portraitEnvironment(ctx,{hour:ui.hour??12,season:'spring',weather:'sunny',motion:ui.motion},805,213,475,H*.34,time);
    this.portrait(ctx,{stage:'adult',state:'idle',facing:true},1040,H*.54,450,time,environment);
    this.text(ctx,'CHEESE',1040,H*.59,24,C.gold,'center',700);
    this.text(ctx,'A DUCK WITH OPINIONS.',1040,H*.59+33,14,C.muted,'center');
    this.rule(ctx,820,H*.59+66,438);
    this.text(ctx,'POND NOTES',820,H*.59+97,13,C.mint);
    this.wrapText(ctx,ui.fact||'There is always something happening at the pond.',820,H*.59+126,435,16,C.ink,5);
    const status=title.status||'';
    if(status){const danger=/ERASE|\[Y\/N\]/.test(status);this.panel(ctx,101,H-155,1238,65,danger?C.rose:C.line);this.fitText(ctx,status,123,H-122,1190,16,danger?C.rose:C.muted);}
    this.text(ctx,'[UP / DOWN] Choose     [ENTER] Select     Click a choice to begin',W/2,H-65,14,C.muted,'center');
  }
  wrapText(ctx,value,x,y,width,size,color,maxRows=Infinity){
    const words=String(value).split(' '),lines=[];let line='';
    const limit=Math.floor(width/(size*.61));
    for(const word of words){if(line.length+word.length+1>limit){lines.push(line);line='';}line+=(line?' ':'')+word;}if(line)lines.push(line);
    lines.slice(0,maxRows).forEach((row,i)=>this.text(ctx,row,x,y+i*size*1.45,size,color));
  }
  hudWindow(ctx,id,title){
    if(!this.layout.visible(id))return null;
    const r=this.layout.rect(id,this.width,this.height);this.hudRects.push({id,...r});
    this.panel(ctx,r.x,r.y,r.w,r.h,'#667259','#142a25ee');
    this.fitText(ctx,title,r.x+18,r.y+20,r.w-68,14,C.gold);
    this.rule(ctx,r.x+16,r.y+35,r.w-32,'#60705255');
    return r;
  }
  hud(ctx,frame,time){
    const {ui,scene:s}=frame;
    let r=this.hudWindow(ctx,'pond',s.location);
    if(r){
      const clock=String(Math.floor(s.hour)).padStart(2,'0')+':'+String(Math.floor(s.hour%1*60)).padStart(2,'0');
      this.text(ctx,clock+'  ·  '+friendly(s.season)+'  ·  '+friendly(s.weather),r.x+18,r.y+52,13,C.ink);
      this.fitText(ctx,ui.activity,r.x+18,r.y+71,r.w-110,12,C.muted);
      this.text(ctx,'$ '+ui.currency,r.x+r.w-18,r.y+70,14,C.gold,'right',600);
    }
    const light=sceneLight(s);this.emotionHour=light.hour;
    r=this.hudWindow(ctx,'emotion','Cheese');
    if(r){
      const closeup=emotionPortrait(s.duck,ui.emotion,time),cw=Math.min((r.w-32)/closeup.width,126/(closeup.art.length*1.5));
      const environment=portraitEnvironment(ctx,s,r.x+12,r.y+42,r.w-24,126,time);
      drawCharacter(ctx,{...closeup,x:(r.x+r.w/2)/cw,y:(r.y+168)/cw,backdrop:environment.background,outline:environment.light.outline},cw,cw,'#142a25');
      this.fitText(ctx,ui.mood,r.x+18,r.y+184,r.w-36,12,C.ink);
      this.text(ctx,ui.age<1?Math.floor(ui.age*24)+' hours old':Math.floor(ui.age)+' days together',r.x+18,r.y+201,10,C.muted);
    }
    r=this.hudWindow(ctx,'care','Care & connection');
    if(r){
      const needs=[['Hunger',ui.needs.hunger],['Energy',ui.needs.energy],['Fun',ui.needs.fun],['Clean',ui.needs.cleanliness],['Social',ui.needs.social],['Trust',ui.trust]];
      needs.forEach(([label,value],i)=>{
        const y=r.y+54+i*25,color=value<20?C.rose:i===5?C.gold:C.mint;
        this.text(ctx,label,r.x+18,y,13,C.ink);
        const x=r.x+93,w=r.w-150;ctx.fillStyle='#091b18';ctx.beginPath();ctx.roundRect(x,y-5,w,10,5);ctx.fill();
        ctx.fillStyle=color;ctx.beginPath();ctx.roundRect(x,y-5,Math.max(2,w*clamp(value,0,100)/100),10,5);ctx.fill();
        this.text(ctx,Math.floor(value)+'%',r.x+r.w-17,y,12,color,'right');
      });
      if(ui.attention||ui.trust<20||ui.cold)this.text(ctx,ui.attention?'Cheese needs a little care':ui.cold?'Giving you the cold shoulder':'A little distant today',r.x+18,r.y+r.h-16,11,C.rose);
    }
    r=this.hudWindow(ctx,'menu',ui.menu.depth?ui.menu.title:'What shall we do?');
    if(r){
      const count=Math.max(3,Math.floor((r.h-70)/30)),view=menuWindow(ui.menu,count);
      view.items.forEach((item,i)=>{
        const y=r.y+46+i*30,selected=view.start+i===ui.menu.selected;
        if(selected){ctx.fillStyle='#43583d';ctx.beginPath();ctx.roundRect(r.x+10,y-3,r.w-20,28,7);ctx.fill();}
        this.text(ctx,selected?'◆':item.completed?'✓':'·',r.x+19,y+11,12,selected?C.gold:C.dim);
        this.fitText(ctx,item.label,r.x+39,y+11,r.w-70,14,!item.enabled?C.dim:selected?C.gold:C.ink);
        if(item.children)this.text(ctx,'›',r.x+r.w-24,y+11,18,C.mint);
        if(item.enabled&&!ui.modal&&!ui.minigame)this.hits.push({panel:'menu',x:r.x+10,y:y-3,w:r.w-20,h:28,command:{type:'choose',target:'menu',id:item.id,context:ui.menu.items.map(v=>v.id).join('|')}});
      });
      this.text(ctx,(view.start+1)+'–'+(view.start+view.items.length)+' of '+ui.menu.items.length+'   ·   Esc to go back',r.x+18,r.y+r.h-15,10,C.muted);
    }
    if(this.chatExternal&&!this.chatQuiet&&this.layout.visible('chat'))this.hudRects.push({id:'chat',...this.layout.rect('chat',this.width,this.height)});
    r=this.chatExternal?null:this.hudWindow(ctx,'chat','Around the pond');
    if(r){
      const chat=documentRows(ui.chat,Math.floor((r.w-36)/(12*.61))).filter(row=>row.kind!=='rule');
      const rowH=Math.min(18,106/Math.max(chat.length,1));
      chat.forEach((row,i)=>this.row(ctx,row,r.x+18,r.y+51+i*rowH,Math.min(12,rowH*.82),r.w-36));
      this.text(ctx,'PgUp / PgDn to revisit the conversation',r.x+18,r.y+r.h-13,10,C.muted);
    }
    r=this.hudWindow(ctx,'progress','A little more grown');
    if(r){
      this.fitText(ctx,'Level '+ui.level+'  ·  '+ui.xp+'/'+ui.xpNeeded+' XP  ·  '+ui.stage,r.x+18,r.y+49,r.w-36,12,C.muted);
      this.text(ctx,Math.floor(ui.growth)+'% grown  ·  '+ui.goals[0]+'/'+ui.goals[1]+' goals',r.x+18,r.y+67,11,C.muted);
      const x=r.x+165,w=r.w-218;ctx.fillStyle='#0b1e1a';ctx.fillRect(x,r.y+18,w,4);ctx.fillStyle=C.gold;ctx.fillRect(x,r.y+18,w*clamp(ui.xp/Math.max(1,ui.xpNeeded),0,1),4);
    }
  }
  row(ctx,row,x,y,size,width){
    const cw=size*.61;
    if(row.kind==='rule'){this.rule(ctx,x,y,width,C.line);return;}
    const selected=row.kind==='selected';
    if(selected){ctx.fillStyle='#35483e';ctx.fillRect(x-8,y-size*.7,width+16,size*1.45);}
    let offset=0;
    // Batch equal styles; fixed cell positions preserve original ASCII alignment.
    for(const cell of row.cells){
      let color=selected?C.gold:row.kind==='heading'?C.mint:cell.fg;
      if(color==='#e2dfca'||color==='#dfded0')color=C.ink;
      if(/^[─═│║┌┐└┘╔╗╚╝╠╣┤├]$/u.test(cell.char))color=C.dim;
      if(cell.flags&4){ctx.fillStyle=C.gold;ctx.fillRect(x+offset,y-size*.65,cw,size*1.3);color=C.bg;}
      this.text(ctx,cell.char,x+offset,y,size,color,'left',selected||cell.flags&1?700:400,'Menlo, monospace');
      offset+=cw;
    }
  }
  document(ctx,modal,ui={},full=false){
    const W=this.width,H=this.height,title=documentTitle(modal);
    const theme=THEMES[ui.dangerous?'warning':themeFor(title)];
    const preview=selectedItem(ui,documentRows(modal.lines,108)),previewWidth=preview?300:0;
    const columns=Math.min(108,Math.max(40,Math.floor((W-192-previewWidth)/(19*.61))));
    const cacheKey=columns+JSON.stringify(modal);
    let rows=this.cache.get(cacheKey);
    if(!rows){rows=documentRows(modal.lines,columns,modal.preserveArt);if(this.cache.size>24)this.cache.clear();this.cache.set(cacheKey,rows);}
    const size=rows.length>32?17:19,cw=size*.61;
    const maxCols=Math.max(40,...rows.map(row=>row.cells.length));
    const w=clamp(maxCols*cw+92+previewWidth,preview?990:690,W-96);
    const top=this.worldFill?78:0,bottom=this.worldFill?145:0,available=H-top-bottom;
    const rowH=size*1.48,maxRows=Math.max(4,Math.floor((available-194)/rowH));
    const count=Math.min(rows.length,maxRows),h=count*rowH+170;
    const key=ui.state+':'+ui.overlay+':'+title;
    const position=full?{x:(W-w)/2,y:top+(available-h)/2}:this.layout.dialogRect(key,{x:(W-w)/2,y:top+(available-h)/2,w,h},W,H);
    const {x,y}=position;
    const selected=rows.findIndex(row=>row.kind==='selected');
    if(key!==this.docKey){this.scroll=0;this.selectedLine=-1;this.docKey=key;}
    if(selected!==this.selectedLine){
      if(selected>=0&&(selected<this.scroll||selected>=this.scroll+count))this.scroll=clamp(selected-Math.floor(count/2),0,Math.max(0,rows.length-count));
      this.selectedLine=selected;
    }
    this.scroll=clamp(this.scroll,0,Math.max(0,rows.length-count));
    this.visibleDocument={id:key,movable:!full,x,y,w,h,total:rows.length,count,scroll:this.scroll,rows,title,preview:preview?.id,textWidth:w-80-previewWidth};
    ctx.fillStyle=full?'#0c1d21':'#051316cf';ctx.fillRect(0,0,W,H);
    // Offset ink shadow and a double ASCII border give every menu a tactile frame.
    this.panel(ctx,x+9,y+10,w,h,'#152b2c','#061417');
    this.panel(ctx,x,y,w,h,theme.color,C.panel);
    this.art(ctx,theme.art,x+24,y+29,13,theme.color);
    this.text(ctx,theme.label,x+150,y+31,11,C.muted);
    this.fitText(ctx,title,x+150,y+65,w-180,25,theme.color);
    this.rule(ctx,x+24,y+101,w-48,theme.color,'=');
    rows.slice(this.scroll,this.scroll+count).forEach((row,i)=>this.row(ctx,row,x+40,y+128+i*rowH,size,w-80-previewWidth));
    if(preview)this.itemPreview(ctx,preview,x+w-previewWidth+2,y+115,previewWidth-24,h-167,ui.motion!==false);
    this.rule(ctx,x+24,y+h-43,w-48);
    if(rows.length>count){
      this.text(ctx,`SCROLL ${this.scroll+1}-${this.scroll+count} / ${rows.length}`,x+30,y+h-24,11,C.muted);
      for(let i=0;i<count;i++)this.text(ctx,i>=this.scroll/rows.length*count&&i<(this.scroll+count)/rows.length*count?'#':':',x+w-17,y+128+i*rowH,13,theme.color);
    }else this.text(ctx,'CHEESE THE DUCK',x+30,y+h-24,11,C.dim);
    // These are the same original keys, including Escape's confirmation behavior.
    let bx=x+w-334;
    for(const [label,key] of [['<','ArrowLeft'],['^','ArrowUp'],['v','ArrowDown'],['>','ArrowRight'],['ENTER','Enter'],['ESC','Escape']]){
      const bw=label.length>1?70:35;
      ctx.fillStyle='#203b3c';ctx.fillRect(bx,y+h-35,bw,24);
      this.text(ctx,label,bx+bw/2,y+h-23,11,C.muted,'center');
      this.hits.push({x:bx,y:y+h-35,w:bw,h:24,command:{type:'key',key}});bx+=bw+5;
    }
  }
  itemPreview(ctx,item,x,y,w,h,motion){
    const color=rarityColor(item.rarity),model=itemSprite(item.id,this.time,{motion});
    this.panel(ctx,x,y,w,h,C.line,'#0c2025');
    this.text(ctx,'// '+String(item.rarity).toUpperCase(),x+17,y+24,11,color);
    const artHeight=Math.min(182,h*.43),artTop=y+43;
    const cw=Math.min((w-38)/(model.width+2),artHeight/((model.art.length+2)*1.5));
    ctx.save();ctx.beginPath();ctx.rect(x+12,y+36,w-24,artHeight+10);ctx.clip();
    if(model.emissive){const light=ctx.createRadialGradient(x+w/2,artTop+artHeight/2,0,x+w/2,artTop+artHeight/2,w*.42);light.addColorStop(0,model.accent+'25');light.addColorStop(1,model.accent+'00');ctx.fillStyle=light;ctx.fillRect(x+12,artTop,w-24,artHeight);}
    this.itemPainter.draw(ctx,model,x+w/2,artTop+artHeight,cw);ctx.restore();
    const nameY=artTop+artHeight+23;
    this.wrapText(ctx,item.name,x+18,nameY,w-36,16,C.gold,2);
    const descY=nameY+48,rows=Math.max(0,Math.floor((y+h-40-descY)/18));
    this.wrapText(ctx,item.description,x+18,descY,w-36,12,C.muted,rows);
    this.text(ctx,String(item.category).toUpperCase(),x+18,y+h-22,10,C.mint);
  }
  fullScreen(ctx,frame,time){
    const W=this.width,H=this.height;
    ctx.fillStyle=C.bg;ctx.fillRect(0,0,W,H);
    for(let y=22;y<H;y+=32)for(let x=28;x<W;x+=36)this.text(ctx,(x+y)%5===0?'+':'.',x,y,9,'#1b3637');
    const names={offline_summary:'Welcome back',ai_loading:'Waking up the pond',loading:'Waking up the pond'};
    const lines=cropDocument(frame.lines);
    const heading=lines.map(plain).find(line=>line.trim());
    const title=names[frame.ui.state]||(heading?.replace(/^[\s=]+|[\s=]+$/g,'') || 'Pond arcade');
    this.document(ctx,{title,lines,preserveArt:frame.ui.minigame},frame.ui,true);
  }
  hit(x,y){
    const inside=r=>x>=r.x&&y>=r.y&&x<r.x+r.w&&y<r.y+r.h;
    const hit=[...this.hits].reverse().find(inside),top=[...this.hudRects].reverse().find(inside);
    return hit?.panel&&top?.id!==hit.panel?null:hit?.command;
  }
  wheel(delta){if(!this.visibleDocument||this.visibleDocument.total<=this.visibleDocument.count)return false;this.scroll=clamp(this.scroll+Math.sign(delta)*3,0,this.visibleDocument.total-this.visibleDocument.count);return true;}
}
