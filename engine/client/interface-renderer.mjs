import { characterSprite, drawCharacter } from './ultra-characters.mjs';
import { itemSprite,ItemPainter,selectedItem,rarityColor } from './ultra-items.mjs';
import { emotionPortrait } from './emotion-portrait.mjs';
import { documentRows, documentTitle, themeFor, menuWindow, clamp, plain, cropDocument } from './interface-model.mjs';

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
  constructor(){this.hits=[];this.scroll=0;this.docKey='';this.selectedLine=-1;this.visibleDocument=null;this.cache=new Map();this.panelsOpen=false;this.itemPainter=new ItemPainter();}
  text(ctx,text,x,y,size=16,color=C.ink,align='left',weight=400){
    ctx.font=`${weight} ${size}px Menlo, monospace`;ctx.textAlign=align;ctx.textBaseline='middle';ctx.fillStyle=color;ctx.fillText(String(text),x,y);
  }
  fitText(ctx,text,x,y,width,size=16,color=C.ink){
    const length=Array.from(String(text)).length;
    this.text(ctx,text,x,y,Math.min(size,width/Math.max(1,length)*1.62),color);
  }
  rule(ctx,x,y,w,color=C.line,char='-'){
    const n=Math.max(2,Math.floor(w/9));this.text(ctx,char.repeat(n),x,y,14,color);
  }
  panel(ctx,x,y,w,h,color=C.line,fill=C.panel){
    ctx.fillStyle=fill;ctx.fillRect(x,y,w,h);
    this.rule(ctx,x+8,y+8,w-16,color);this.rule(ctx,x+8,y+h-8,w-16,color);
    for(let py=y+23;py<y+h-14;py+=16){this.text(ctx,':',x+5,py,14,color);this.text(ctx,':',x+w-7,py,14,color);}
    for(const px of [x+5,x+w-7])for(const py of [y+8,y+h-8])this.text(ctx,'+',px,py,14,color);
  }
  art(ctx,lines,x,y,size,color){lines.forEach((line,i)=>this.text(ctx,line,x,y+i*size*1.15,size,color));}
  button(ctx,label,x,y,w,h,selected=false,command=null){
    ctx.fillStyle=selected?'#355247':'#1b3435';ctx.fillRect(x,y,w,h);
    this.text(ctx,selected?'>':'[',x+12,y+h/2,18,selected?C.gold:C.dim);
    this.fitText(ctx,label,x+34,y+h/2,w-64,17,selected?C.gold:C.ink);
    this.text(ctx,selected?'<':']',x+w-22,y+h/2,18,selected?C.gold:C.dim);
    if(command)this.hits.push({x,y,w,h,command});
  }
  begin(ctx,canvas,frame,viewport){
    this.hits=[];this.visibleDocument=null;
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
      this.hud(ctx,frame,clock);
      if(ui.modal)this.document(ctx,ui.modal,ui);
    }else this.fullScreen(ctx,frame,clock);
    ctx.restore();
  }
  portrait(ctx,duck,x,y,size,time){
    const sprite=characterSprite(duck,time);const scale=size/(sprite.width*1.8);
    drawCharacter(ctx,{...sprite,x:x/scale,y:y/scale},scale,scale,C.panel);
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
    this.portrait(ctx,{stage:'adult',state:'idle',facing:true},1040,H*.54,500,time);
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
  hud(ctx,frame,time){
    const {ui,scene:s}=frame,W=this.width,H=this.height;
    const right=W-346,sw=328;
    // The world extends behind every panel. No space is reserved for a sidebar.
    this.panel(ctx,18,78,Math.min(570,right-36),78,C.line,'#102429e8');
    this.text(ctx,s.location.toUpperCase(),36,102,18,C.gold,'left',700);
    this.text(ctx,`$ ${ui.currency}`,Math.min(570,right-36),102,17,C.gold,'right');
    this.fitText(ctx,`${friendly(s.season)} / ${friendly(s.weather)} / ${String(Math.floor(s.hour)).padStart(2,'0')}:${String(Math.floor(s.hour%1*60)).padStart(2,'0')}  ·  ${ui.activity}`,36,133,Math.min(530,right-76),13,C.muted);
    const x=right+18,w=sw-36;
    this.panel(ctx,right,78,sw,228,C.line,'#102429ef');
    this.text(ctx,'// EMOTIONS',x,103,13,C.gold);
    this.text(ctx,ui.age<1?`${Math.floor(ui.age*24)}h old`:`${Math.floor(ui.age)} days`,right+sw-22,103,12,C.muted,'right');
    const closeup=emotionPortrait(s.duck,ui.emotion,time),faceCell=Math.min((w-8)/closeup.width,150/(closeup.art.length*1.5));
    drawCharacter(ctx,{...closeup,x:(right+sw/2)/faceCell,y:264/faceCell},faceCell,faceCell,C.panel);
    this.fitText(ctx,ui.mood,x,281,w,14,C.muted);
    if(this.panelsOpen){
    this.panel(ctx,right,313,sw,216,C.line,'#102429ef');
    this.text(ctx,'CARE & CONNECTION',x,335,13,C.mint);
    const needs=[['Hunger',ui.needs.hunger],['Energy',ui.needs.energy],['Fun',ui.needs.fun],['Clean',ui.needs.cleanliness],['Social',ui.needs.social],['Trust',ui.trust]];
    needs.forEach(([label,value],i)=>{
      const y=364+i*25,low=value<20,color=low?C.rose:i===5?C.gold:C.mint;
      this.text(ctx,label,x,y,14,low?C.rose:C.ink);
      const bars=11,filled=Math.round(clamp(value,0,100)/100*bars);
      this.text(ctx,'['+'='.repeat(filled)+'.'.repeat(bars-filled)+']',x+81,y,13,color);
      this.text(ctx,`${Math.floor(value)}%`,right+sw-20,y,13,color,'right');
    });
    if(ui.attention||ui.trust<20||ui.cold)this.text(ctx,ui.attention?'! NEEDS ATTENTION':ui.cold?'[COLD SHOULDER]':'[DISTANT]',x,514,11,C.rose);
    const my=537,mh=H-155-my;
    this.panel(ctx,right,my,sw,mh,C.line,'#102429ef');
    this.fitText(ctx,(ui.menu.depth?' / ':'// ')+ui.menu.title.toUpperCase(),x,my+24,w,14,C.gold);
    const count=Math.max(3,Math.floor((mh-72)/32)),window=menuWindow(ui.menu,count);
    window.items.forEach((item,i)=>{
      const index=window.start+i,y=my+48+i*32,selected=index===ui.menu.selected;
      if(selected){ctx.fillStyle='#355247';ctx.fillRect(x-4,y-13,w+8,29);}
      this.text(ctx,selected?'>':item.completed?'*':'.',x+3,y+1,15,selected?C.gold:C.dim);
      this.fitText(ctx,item.label,x+24,y+1,w-43,14,!item.enabled?C.dim:selected?C.gold:C.ink);
      if(item.children)this.text(ctx,'>',x+w-10,y+1,14,C.mint);
      if(item.enabled&&!ui.modal&&!ui.minigame)this.hits.push({x:x-4,y:y-13,w:w+8,h:29,command:{type:'choose',target:'menu',id:item.id,context:ui.menu.items.map(v=>v.id).join('|')}});
    });
    this.text(ctx,`${window.start+1}-${window.start+window.items.length} / ${ui.menu.items.length}   [ESC] Back`,x,my+mh-20,11,C.muted);
    }else{
      this.button(ctx,ui.attention?'! Care & menu':'Care & menu',right,314,sw,34,false,ui.modal?null:{type:'panels'});
      this.panel(ctx,right,355,sw,57,C.line,'#102429d9');
      this.wrapText(ctx,ui.action,x,377,w,12,C.ink,2);
    }
    // Transcript remains the original game's visible, scrollable, styled text.
    const chatW=Math.min(920,right-36),chatY=H-324,chatH=169;
    this.panel(ctx,18,chatY,chatW,chatH,C.line,'#102429df');
    this.text(ctx,'POND CHAT',36,chatY+22,12,C.mint);
    this.text(ctx,'[PGUP / PGDN] History',chatW+2,chatY+22,11,C.muted,'right');
    const chat=documentRows(ui.chat,Math.floor((chatW-36)/(12*.61))).filter(row=>row.kind!=='rule');
    const rowH=Math.min(17,104/Math.max(chat.length,1));
    chat.forEach((row,i)=>this.row(ctx,row,36,chatY+44+i*rowH,Math.min(12,rowH*.82),chatW-36));
    this.rule(ctx,36,chatY+chatH-28,chatW-36);
    this.fitText(ctx,`LV ${ui.level}  ${ui.xp}/${ui.xpNeeded} XP  /  ${ui.stage} ${Math.floor(ui.growth)}%  /  GOALS ${ui.goals[0]}/${ui.goals[1]}`,36,chatY+chatH-14,chatW-36,11,C.muted);
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
      this.text(ctx,cell.char,x+offset,y,size,color,'left',selected||cell.flags&1?700:400);
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
    const w=clamp(maxCols*cw+92+previewWidth,preview?990:690,W-96),x=(W-w)/2;
    const top=this.worldFill?78:0,bottom=this.worldFill?145:0,available=H-top-bottom;
    const rowH=size*1.48,maxRows=Math.max(4,Math.floor((available-194)/rowH));
    const count=Math.min(rows.length,maxRows),h=count*rowH+170,y=top+(available-h)/2;
    const key=ui.state+':'+ui.overlay+':'+title;
    const selected=rows.findIndex(row=>row.kind==='selected');
    if(key!==this.docKey){this.scroll=0;this.selectedLine=-1;this.docKey=key;}
    if(selected!==this.selectedLine){
      if(selected>=0&&(selected<this.scroll||selected>=this.scroll+count))this.scroll=clamp(selected-Math.floor(count/2),0,Math.max(0,rows.length-count));
      this.selectedLine=selected;
    }
    this.scroll=clamp(this.scroll,0,Math.max(0,rows.length-count));
    this.visibleDocument={x,y,w,h,total:rows.length,count,scroll:this.scroll,rows,title,preview:preview?.id,textWidth:w-80-previewWidth};
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
  hit(x,y){return this.hits.find(hit=>x>=hit.x&&y>=hit.y&&x<hit.x+hit.w&&y<hit.y+hit.h)?.command;}
  wheel(delta){if(!this.visibleDocument||this.visibleDocument.total<=this.visibleDocument.count)return false;this.scroll=clamp(this.scroll+Math.sign(delta)*3,0,this.visibleDocument.total-this.visibleDocument.count);return true;}
}
