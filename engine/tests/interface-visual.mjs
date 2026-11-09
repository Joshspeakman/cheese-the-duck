import { DisplayRenderer } from '../client/ultra-renderer.mjs';
import { GlyphRenderer } from '../client/renderer.mjs';
import { plain } from '../client/interface-model.mjs';
import { emotionPortrait } from '../client/emotion-portrait.mjs';
import { drawCharacter } from '../client/ultra-characters.mjs';
const assert=(ok,message)=>{if(!ok)throw new Error(message);};
const pixels=c=>c.getContext('2d').getImageData(0,0,c.width,c.height).data;
const equal=(a,b)=>a.length===b.length&&a.every((v,i)=>v===b[i]);
window.checkInterface=frames=>{
  const images={},durations=[],checks=[];
  const canvas=document.createElement('canvas'),display=new DisplayRenderer(canvas);
  const selected=['title','pond','shop','settings-audio','settings-accessibility','craft','build','help','diary-overview','confirmation','long-talk','bread_catch','offline','loading','title-confirmation'];
  const contact=document.createElement('canvas');contact.width=1920;contact.height=selected.length/3*500;
  const c=contact.getContext('2d');c.fillStyle='#091a1e';c.fillRect(0,0,contact.width,contact.height);
  for(const [name,frame] of Object.entries(frames)){
    assert(frame.ui,`missing UI: ${name}`);
    display.resize(frame.cols,frame.rows,.8);
    const start=performance.now();display.draw(frame,2000);durations.push(performance.now()-start);
    const doc=display.interface.visibleDocument;
    if(doc){
      assert(doc.x>=0&&doc.y>=0&&doc.x+doc.w<=frame.cols*10&&doc.y+doc.h<=frame.rows*18,`panel clipped: ${name}`);
      assert(doc.rows.every(row=>row.cells.length<=108),`line clipped: ${name}`);
      assert(doc.scroll+doc.count<=doc.total,`invalid scroll: ${name}`);
    }
    if(name==='confirmation')assert(doc?.title.includes('Reset'), 'confirmation was obscured by settings');
    if(name==='celebration')assert(doc?.title==='CELEBRATION'&&doc.rows.some(row=>row.text.includes('Cheese reached level 2!')),'custom celebration disappeared');
    if(name==='item-interaction')assert(doc?.title==='INTERACTING'&&doc.rows.some(row=>row.text.includes('Cheese is enjoying the bread.')),'custom interaction disappeared');
    if(name==='long-talk'){
      const text=doc.rows.map(row=>row.text).join('');
      assert(text.includes('What the fuck, Cheese?'), 'speech changed');
      assert(text.includes('Keep every character. '.repeat(9).trim()),'long dialogue clipped');
    }
    if(name==='settings-audio')assert(doc.rows.some(row=>row.text.includes('KEYBINDINGS')),'wide category tabs clipped');
    const i=selected.indexOf(name);
    if(i>=0){
      images[name]=canvas.toDataURL('image/png');
      c.fillStyle='#f4ce82';c.font='18px Menlo';c.fillText(name,i%3*640+16,Math.floor(i/3)*500+26);
      c.drawImage(canvas,i%3*640,Math.floor(i/3)*500+44,640,440);
    }
    checks.push(name);
  }
  // Every row of a long document remains reachable without changing game input.
  const long=structuredClone(frames.help);long.ui.modal.lines=Array.from({length:150},(_,i)=>[[`UNIQUE ROW ${i}`,'#e2dfca','#101b19',0]]);
  display.resize(long.cols,long.rows,.8);display.draw(long,2000);
  const seen=new Set();
  for(let i=0;i<60;i++){
    const d=display.interface.visibleDocument;
    d.rows.slice(d.scroll,d.scroll+d.count).forEach(row=>seen.add(row.text));
    display.interface.wheel(120);display.draw(long,2000);
  }
  assert(seen.size===150,'long menu has unreachable content');
  for(const name of ['pond','shop','title']){
    const f=frames[name],classic=new GlyphRenderer(document.createElement('canvas'));
    classic.resize(f.cols,f.rows,.5);classic.draw(f);
    display.resize(f.cols,f.rows,.5);display.mode='classic';display.draw(f,2000);
    assert(equal(pixels(classic.canvas),pixels(canvas)),`Classic changed: ${name}`);
    display.mode='ultra';display.draw(f,2000);display.mode='classic';display.draw(f,2033);
    assert(equal(pixels(classic.canvas),pixels(canvas)),`Classic toggle trails: ${name}`);
  }
  display.mode='ultra';display.resize(144,55,.8);
  const frozen=structuredClone(frames.pond);frozen.scene.motion=false;frozen.ui.motion=false;
  display.draw(frozen,2000);const before=new Uint8ClampedArray(pixels(canvas));display.draw(frozen,8000);
  assert(equal(before,pixels(canvas)),'reduced motion animated UI');
  images.gallery=contact.toDataURL('image/png');
  // World composition fills every aspect ratio; menu hit boxes follow its UI scale.
  for(const [width,height] of [[920,613],[1500,993],[1920,1080],[1800,760]]){
    const frame=structuredClone(frames.pond),uiScale=Math.min(width/1440,height/1000,1);
    display.resize(frame.cols,frame.rows,.8,{width,height,uiScale});
    display.interface.panelsOpen=false;display.draw(frame,2000);
    assert(display.scene.canvas.width===canvas.width&&display.scene.canvas.height===canvas.height,'world does not fill canvas');
    assert(canvas.style.width===`${width}px`&&canvas.style.height===`${height}px`,'viewport dimensions changed');
    assert(!display.interface.hits.some(hit=>hit.command.target==='menu'),'compact view reserved a menu');
    images[`window-${width}`]=canvas.toDataURL('image/png');
    display.interface.panelsOpen=true;display.draw(frame,2000);
    const hit=display.interface.hits.find(hit=>hit.command.target==='menu');
    assert(hit&&display.interface.hit(hit.x+hit.w/2,hit.y+hit.h/2).id==='care','floating menu click target moved');
    for(const hit of display.interface.hits)assert(hit.x>=0&&hit.y>=0&&hit.x+hit.w<=display.interface.width&&hit.y+hit.h<=display.interface.height,'floating control clipped');
    for(const name of ['help','settings-audio','long-talk']){
      display.draw(frames[name],2000);const d=display.interface.visibleDocument;
      assert(d.y>=78&&d.y+d.h<=display.interface.height-145,'menu overlaps app controls');
      assert(d.rows.every(row=>row.cells.length*(d.rows.length>32?17:19)*.61<=d.w-80),'menu text clipped at this aspect ratio');
    }
  }
  const emotions=document.createElement('canvas');emotions.width=1200;emotions.height=690;
  const ec=emotions.getContext('2d');ec.fillStyle='#13282b';ec.fillRect(0,0,1200,690);
  ['ecstatic','happy','content','grumpy','sad','miserable','dramatic','petty','eating','sleeping','petting','talking'].forEach((mood,i)=>{
    const x=i%4*300,y=Math.floor(i/4)*230,action=i>=8?mood:null;
    drawCharacter(ec,{...emotionPortrait({stage:'adult'},{mood:action?'content':mood,action},.5),x:(x+150)/10,y:(y+185)/10},10,10,'#13282b');
    ec.font='16px Menlo';ec.textAlign='center';ec.fillStyle='#f4ce82';ec.fillText(mood,x+150,y+214);
  });
  images.emotions=emotions.toDataURL('image/png');
  durations.sort((a,b)=>a-b);
  return {checks,medianMs:durations[Math.floor(durations.length*.5)],p95Ms:durations[Math.floor(durations.length*.95)],images};
};
