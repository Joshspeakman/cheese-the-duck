// Actual application/CSS/controller with real simulation fixtures and isolated preferences.
const {app,BrowserWindow,ipcMain}=require('electron');
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const out=path.join(__dirname,'artifacts/hud');fs.mkdirSync(out,{recursive:true});
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-hud-check-')));
const frames=JSON.parse(fs.readFileSync(path.join(__dirname,'artifacts/interface-frames.json')));
const inputs=[],checks=[],errors=[];let current=frames.pond,win;
ipcMain.on('hud-test:ready',()=>win.webContents.send('hud-test:frame',current));
ipcMain.on('hud-test:input',(_e,c)=>inputs.push(c));
const pause=ms=>new Promise(r=>setTimeout(r,ms));
const js=source=>win.webContents.executeJavaScript(source);
const check=(yes,label)=>{if(!yes)throw Error(label);checks.push(label);};
async function wait(source,label){for(let i=0;i<150;i++){if(await js(source))return;await pause(50);}throw Error(label);}
async function frame(f){current=structuredClone(f);win.webContents.send('hud-test:frame',current);await pause(150);}
async function screenshot(name){await pause(120);fs.writeFileSync(path.join(out,name+'.png'),(await win.webContents.capturePage()).toPNG());}
async function drag(selector,dx,dy){
 const p=await js(`(()=>{const r=document.querySelector(${JSON.stringify(selector)}).getBoundingClientRect();return {x:Math.round(r.x+Math.min(100,r.width/2)),y:Math.round(r.y+Math.min(20,r.height/2))};})()`);
 win.webContents.sendInputEvent({type:'mouseMove',...p});win.webContents.sendInputEvent({type:'mouseDown',button:'left',clickCount:1,...p});await pause(70);
 for(let i=1;i<=6;i++){win.webContents.sendInputEvent({type:'mouseMove',modifiers:['leftButtonDown'],x:Math.round(p.x+dx*i/6),y:Math.round(p.y+dy*i/6)});await pause(30);}
 win.webContents.sendInputEvent({type:'mouseUp',button:'left',clickCount:1,x:p.x+dx,y:p.y+dy});await pause(180);
}
app.whenReady().then(async()=>{
 win=new BrowserWindow({show:true,width:1440,height:1000,webPreferences:{preload:path.join(__dirname,'tests/hud-preload.cjs'),contextIsolation:true,sandbox:true,backgroundThrottling:false}});
 win.webContents.on('console-message',d=>{if(d.level==='error')errors.push(d.message);});
 try{
  await win.loadFile(path.join(__dirname,'client/index.html'));await wait('window.engineStats?.state==="playing"','HUD did not start');
  await screenshot('cozy');
  check(await js("document.querySelectorAll('.hud-handle:not([hidden])').length===4"),'four compact HUD windows');
  const before=await js("window.pondHUD.layout.rect('emotion',window.engineStats.viewWidth,window.engineStats.viewHeight)");
  const count=inputs.length;await drag('[data-panel="emotion"] .hud-grip',-220,120);
  const after=await js("window.pondHUD.layout.rect('emotion',window.engineStats.viewWidth,window.engineStats.viewHeight)");
  check(after.x<before.x-100&&after.y>before.y+80,'pointer drag moves emotion window '+JSON.stringify({before,after}));check(inputs.length===count,'drag does not send gameplay input');
  await js("document.querySelector('[data-panel=emotion] .hud-close').click()");await pause(100);
  check(await js("document.querySelector('[data-panel=emotion].hud-handle').hidden"),'emotion window closes');
  await js("window.pondHUD.toggleKit();document.querySelector('#panel-switches input[data-panel=emotion]').click()");await screenshot('pond-kit');
  await js('window.pondHUD.closeKit()');check(await js("!document.querySelector('[data-panel=emotion].hud-handle').hidden"),'closed window reopens from kit');
  await screenshot('moved');
  await new Promise(resolve=>{win.webContents.once('did-finish-load',resolve);win.webContents.reload();});await wait('window.engineStats?.state==="playing"','reload');
  check(await js(`Math.abs(window.pondHUD.layout.rect('emotion',window.engineStats.viewWidth,window.engineStats.viewHeight).x-${after.x})<1`),'layout persists across reload');
  await js("window.pondHUD.toggleKit();for(const i of document.querySelectorAll('#panel-switches input:checked'))i.click();window.pondHUD.closeKit()");
  check(await js("!document.getElementById('kit-recall').hidden&&document.getElementById('action-belt').hidden&&document.getElementById('game-header').hidden"),'all sections can close with recovery control remaining');
  win.webContents.sendInputEvent({type:'keyDown',keyCode:'F2'});win.webContents.sendInputEvent({type:'keyUp',keyCode:'F2'});await pause(100);
  check(await js('window.pondHUD.open'),'F2 recovers hidden controls');
  await js("document.querySelector('[data-layout-preset=cozy]').click();window.pondHUD.closeKit();window.pondHUD.layout.show('menu',true);window.pondHUD.changed()");
  await drag('[data-panel="menu"] .hud-grip',-280,-220);
  const hit=await js("(()=>{const h=window.interfaceTargets.find(h=>h.command.id==='care'),r=document.getElementById('world').getBoundingClientRect(),s=window.engineStats;return {x:Math.round(r.x+(h.x+h.w/2)/s.viewWidth*r.width),y:Math.round(r.y+(h.y+h.h/2)/s.viewHeight*r.height)};})()");
  win.webContents.sendInputEvent({type:'mouseDown',button:'left',clickCount:1,...hit});win.webContents.sendInputEvent({type:'mouseUp',button:'left',clickCount:1,...hit});await pause(120);
  check(inputs.at(-1)?.id==='care','moved menu retains correct hit targets');
  const prior=inputs.length;
  await js("(()=>{const h=window.pondHUD,i=h.renderer.interface,r=h.layout.rect('menu',i.width,i.height);h.layout.move('chat',r.x,r.y,i.width,i.height);h.changed();})()");
  win.webContents.sendInputEvent({type:'mouseDown',button:'left',clickCount:1,...hit});win.webContents.sendInputEvent({type:'mouseUp',button:'left',clickCount:1,...hit});await pause(100);
  check(inputs.length===prior,'overlapping panel blocks covered menu actions');
  await js("delete window.pondHUD.layout.panels.chat;window.pondHUD.changed()");
  for(const [w,h] of [[920,640],[1800,760],[1440,1000]]){
   win.setSize(w,h);await pause(250);
   check(await js("[...document.querySelectorAll('.hud-handle:not([hidden]),#game-header:not([hidden]),#action-belt:not([hidden])')].every(n=>{const r=n.getBoundingClientRect();return r.left>=-1&&r.top>=-1&&r.right<=innerWidth+1&&r.bottom<=innerHeight+1})"),'panels stay onscreen '+w);
   if(w===920)await screenshot('small-window');
   check(await js("(()=>{const a=document.querySelector('#game-header .brand').getBoundingClientRect(),b=document.getElementById('pond-kit').getBoundingClientRect();return a.right<=b.left+1})()"),'compact kit labels do not overlap '+w);
  }
  await frame(frames.help);await wait("!!document.querySelector('[data-panel=document]:not([hidden])')",'movable game menu');
  const docBefore=await js("document.querySelector('[data-panel=document]').getBoundingClientRect().x");await drag('[data-panel="document"] .hud-grip',50,25);
  check(await js(`document.querySelector('[data-panel=document]').getBoundingClientRect().x>${docBefore+20}`),'game document can be moved');
  await js("document.querySelector('[data-panel=document] .hud-close').click()");await pause(50);check(inputs.at(-1)?.key==='Escape','document close uses original Escape behavior');
  await frame(frames.confirmation);await js('window.pondHUD.fade.lastInput=performance.now()-70000');await pause(100);check(await js('window.pondHUD.fade.opacity===1'),'confirmation never fades');
  await frame(frames.pond);await js("document.getElementById('pond').click()");await pause(120);
  const journal=await js("document.getElementById('pond-journal').getBoundingClientRect().x");await drag('#pond-journal>header',40,20);
  check(await js(`document.getElementById('pond-journal').getBoundingClientRect().x>${journal+15}`),'field notebook can be moved');
  await js('window.pondHUD.fade.lastInput=performance.now()-70000');await pause(100);check(await js('window.pondHUD.fade.opacity===1'),'open notebook keeps controls awake');
  await screenshot('notebook');await js("document.getElementById('pond-journal').close();document.getElementById('item-art').click()");await pause(120);
  await drag('.gallery-head',35,15);check(await js("document.getElementById('item-gallery').style.left!==''"),'item cabinet can be moved');await screenshot('cabinet');
  await js("document.getElementById('item-gallery').close();window.pondHUD.layout.preset();window.pondHUD.changed();window.pondHUD.fade.lastInput=performance.now()-62000");await pause(150);
  check(await js('window.pondHUD.fade.opacity===0'),'HUD fully fades while world continues');await screenshot('quiet');
  const n=inputs.length;win.webContents.sendInputEvent({type:'keyDown',keyCode:'B'});win.webContents.sendInputEvent({type:'keyUp',keyCode:'B'});await pause(400);
  check(await js('window.pondHUD.fade.opacity===1'),'keyboard wakes HUD');check(inputs.length===n,'wake key cannot open a hidden action');
  await js('window.pondHUD.fade.lastInput=performance.now()-62000');await pause(100);
  const f=await js('window.pondHUD.renderer.frames');
  win.webContents.sendInputEvent({type:'mouseDown',button:'left',clickCount:1,x:500,y:500});win.webContents.sendInputEvent({type:'mouseUp',button:'left',clickCount:1,x:500,y:500});await pause(400);
  check(inputs.length===n,'wake click does not reach gameplay');check(await js('window.pondHUD.fade.opacity===1'),'pointer wakes HUD');
  check(await js(`window.pondHUD.renderer.frames>${f}`),'pond continues rendering through idle and waking');
  // One actual minute verifies the production threshold, not just a synthetic clock.
  await js('window.pondHUD.wake()');console.log('Waiting for the real 60-second idle fade…');
  await pause(59000);check(await js('window.pondHUD.fade.opacity===1'),'real idle stays visible before minute');
  await pause(3500);check(await js('window.pondHUD.fade.opacity===0'),'real minute fades all HUD chrome');
  await screenshot('real-idle');check(errors.length===0,'no browser errors: '+errors.join('; '));
  fs.writeFileSync(path.join(out,'checks.json'),JSON.stringify({result:'PASS',checks,inputs:inputs.length},null,2));console.log(JSON.stringify({result:'PASS',checks:checks.length,out}));app.exit(0);
 }catch(error){await screenshot('failure');console.error(error);console.error(errors);app.exit(1);}
});
