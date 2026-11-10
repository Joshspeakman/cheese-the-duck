const {app,BrowserWindow}=require('electron');
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const out=path.join(__dirname,'artifacts/guests');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-guests-visual-')));
app.whenReady().then(async()=>{
 const win=new BrowserWindow({show:false,width:1440,height:1000,webPreferences:{contextIsolation:true,sandbox:true,backgroundThrottling:false}}),errors=[];
 win.webContents.on('console-message',d=>{if(d.level==='error')errors.push(d.message);});
 try{
  await win.loadFile(path.join(__dirname,'tests/overhaul.html'));
  const scenes=JSON.parse(fs.readFileSync(path.join(out,'scenes.json')));
  const result=await win.webContents.executeJavaScript(`(async()=>{
   const {SceneCanvas}=await import('../client/ultra-renderer.mjs');
   const {PondJournal}=await import('../client/pond-journal.mjs');
   const assert=(v,m)=>{if(!v)throw Error(m);},images={},checks=[];
   const journal=new PondJournal();window.guestJournal=journal;
   for(const s of ${JSON.stringify(scenes)}){
    const id=s.rareVisitor.id;s.hour=12;s.weather='sunny';s.season='spring';s.duck.hidden=false;s.duck.stage='adult';s.motion=true;
    s.rareVisitor.x=84;s.rareVisitor.y=24;s.rareVisitor.state='signature';s.rareVisitor.activity='signature';
    const canvas=new SceneCanvas();canvas.resize(1440,820);canvas.draw(s,1.2,1/30);
    assert(canvas.hits.some(h=>h.id===id&&h.kind==='friend'),id+' clickable guest');
    images[id]=canvas.canvas.toDataURL();
    journal.update({scene:s});journal.show('friends',id);
    assert(journal.body.textContent.includes(s.living.rare_guest.bio),id+' identity');
    assert(journal.body.querySelector('canvas[data-id="'+id+'"]'),id+' animated portrait');
    for(const [label,action] of [['Say hello','guest_chat'],['Ask about their adventures','guest_hobby'],['Keep them company','guest_company']]){
     [...journal.body.querySelectorAll('button')].find(b=>b.textContent===label).click();
     assert(window.lastCommand.action===action&&window.lastCommand.target===id,id+' '+action);
    }
    assert(journal.dialog.scrollWidth<=journal.dialog.clientWidth+1,id+' no horizontal overflow');
    checks.push(id);
   }
   return {images,checks};
  })()`);
  for(const [id,data] of Object.entries(result.images))fs.writeFileSync(path.join(out,id+'.png'),Buffer.from(data.split(',')[1],'base64'));
  delete result.images;
  fs.writeFileSync(path.join(out,'guest-journal.png'),(await win.webContents.capturePage()).toPNG());
  if(errors.length)throw Error(errors.join('\n'));
  fs.writeFileSync(path.join(out,'visual-checks.json'),JSON.stringify({result:'PASS',...result},null,2));
  console.log(JSON.stringify({result:'PASS',...result}));app.exit(0);
 }catch(e){console.error(e);app.exit(1);}
});
