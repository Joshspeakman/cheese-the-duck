// Exercise the live application against real story snapshots, without player saves.
const {app,BrowserWindow,ipcMain}=require('electron');
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const out=path.join(__dirname,'artifacts/stories');fs.mkdirSync(out,{recursive:true});
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-story-check-')));
const scenes=JSON.parse(fs.readFileSync(path.join(__dirname,'artifacts/guests/story-scenes.json')));
const base=JSON.parse(fs.readFileSync(path.join(__dirname,'artifacts/interface-frames.json'))).pond;
const inputs=[],checks=[],errors=[];let current=base,win;
ipcMain.on('hud-test:ready',()=>win.webContents.send('hud-test:frame',current));
ipcMain.on('hud-test:input',(_e,c)=>inputs.push(c));
const pause=ms=>new Promise(r=>setTimeout(r,ms)),js=s=>win.webContents.executeJavaScript(s);
const check=(v,m)=>{if(!v)throw Error(m);checks.push(m);};
app.whenReady().then(async()=>{
 win=new BrowserWindow({show:false,width:1440,height:1000,webPreferences:{preload:path.join(__dirname,'tests/hud-preload.cjs'),contextIsolation:true,sandbox:true,backgroundThrottling:false}});
 win.webContents.on('console-message',d=>{if(d.level==='error')errors.push(d.message);});
 try{
  await win.loadFile(path.join(__dirname,'client/index.html'));
  for(let i=0;i<100&&!await js('Boolean(window.engineStats)');i++)await pause(50);
  for(const scene of scenes){
   const id=scene.living.story.id;
   current=structuredClone(base);current.scene=scene;current.scene.storyActor.x=85;current.scene.storyActor.y=20;
   current.scene.storyActor.state=current.scene.storyActor.activity='signature';
   current.scene.hour=12;current.scene.season='fall';current.scene.weather='sunny';
   current.scene.duck.hidden=false;current.scene.duck.stage='hatchling';current.scene.duck.x=55;current.scene.duck.y=23;
   current.ui.modal=null;current.meta.talking=false;
   win.webContents.send('hud-test:frame',current);await pause(250);
   const result=await js(`(()=>{
    const s=window.pondHUD.renderer.scene,m=s.world.characters.find(m=>m.story),h=s.hits.find(h=>h.kind==='story');
    if(!h||!m)return null;
    const c=document.getElementById('world'),r=c.getBoundingClientRect();
    c.dispatchEvent(new MouseEvent('click',{bubbles:true,clientX:r.left+(h.x+h.w*.5)/s.canvas.width*r.width,clientY:r.top+(h.y+h.h*.85)/s.canvas.height*r.height}));
    return {design:m.design,profile:m.profileId,fills:m.fills?.length};
   })()`);
   check(result,id+' has a world hit target');await pause(160);
   check(await js("document.getElementById('pond-journal').open&&Boolean(document.querySelector('.pond-story canvas[data-kind=story]'))"),id+' click opens story journal and upgraded preview');
   if(id==='lost_duckling'){
    check(result.design==='pond-cast'&&result.profile==='lost_duckling'&&result.fills>8,'story duckling uses full feather and accessory rig');
    fs.writeFileSync(path.join(out,'duckling-journal.png'),(await win.webContents.capturePage()).toPNG());
   }
   await js("document.querySelector('.pond-story .pond-choice button:not(:disabled)').click()");await pause(50);
   check(inputs.at(-1)?.action==='story_choice'&&inputs.at(-1)?.target.startsWith(id+':1:'),id+' sends original guarded story choice');
   await js("document.getElementById('pond-journal').close()");await pause(120);
   if(id==='lost_duckling')fs.writeFileSync(path.join(out,'duckling-world.png'),(await win.webContents.capturePage()).toPNG());
  }
  check(!errors.length,'no browser errors: '+errors.join('; '));
  fs.writeFileSync(path.join(out,'checks.json'),JSON.stringify({result:'PASS',checks},null,2));
  console.log(JSON.stringify({result:'PASS',checks:checks.length,out}));app.exit(0);
 }catch(e){fs.writeFileSync(path.join(out,'failure.png'),(await win.webContents.capturePage()).toPNG());console.error(e,errors);app.exit(1);}
});
