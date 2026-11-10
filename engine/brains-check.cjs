// Actual renderer + notebook, isolated from the installed game and its saves.
const {app,BrowserWindow,ipcMain}=require('electron');
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const out=path.join(__dirname,'artifacts/brains'),scene=JSON.parse(fs.readFileSync(path.join(out,'scene.json')));
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-brains-ui-')));
let frame=JSON.parse(fs.readFileSync(path.join(__dirname,'artifacts/interface-frames.json'))).pond;
frame.scene=scene;frame.ui.modal=null;frame.meta.talking=false;
const inputs=[],errors=[],checks=[];let win;
ipcMain.on('hud-test:ready',()=>win.webContents.send('hud-test:frame',frame));
ipcMain.on('hud-test:input',(_e,c)=>inputs.push(c));
const pause=ms=>new Promise(r=>setTimeout(r,ms)),js=s=>win.webContents.executeJavaScript(s);
const check=(x,label)=>{if(!x)throw Error(label);checks.push(label);};
app.whenReady().then(async()=>{
 win=new BrowserWindow({show:false,width:1440,height:1000,webPreferences:{preload:path.join(__dirname,'tests/hud-preload.cjs'),contextIsolation:true,sandbox:true,backgroundThrottling:false}});
 win.webContents.on('console-message',d=>{if(d.level==='error')errors.push(d.message);});
 try{
  await win.loadFile(path.join(__dirname,'client/index.html'));await pause(600);
  await js("document.getElementById('pond').click();document.querySelector('[data-tab=personalities]').click()");await pause(300);
  check(await js("document.querySelectorAll('.resident-picker button').length>=3"),'all known resident brains accessible');
  check(await js("document.querySelector('.resident-thread').textContent.includes('lavender')"),'actual learned conversation visible');
  check(await js("document.querySelector('.resident-portrait').textContent.includes('experiences learned')"),'actual experience count visible');
  await js("document.querySelector('.resident-form textarea').focus();document.querySelector('.resident-form textarea').value='What the fuck, Cheese?';document.querySelector('.resident-form textarea').dispatchEvent(new Event('input'));document.querySelector('.resident-form textarea').dispatchEvent(new KeyboardEvent('keydown',{key:'b',bubbles:true}))");
  const before=inputs.length;
  frame.scene.living.minds.pending='A friend';win.webContents.send('hud-test:frame',frame);await pause(5500);
  check(await js("document.activeElement.tagName==='TEXTAREA'&&document.activeElement.value==='What the fuck, Cheese?'"),'live refresh preserves text and focus');
  check(inputs.length===before,'typing in guest chat never leaks to gameplay');
  frame.scene.living.minds.pending=null;win.webContents.send('hud-test:frame',frame);await pause(250);
  await js("document.querySelector('.resident-form').requestSubmit()");await pause(80);
  check(inputs.at(-1)?.action==='mind_chat'&&inputs.at(-1)?.target==='cheese'&&inputs.at(-1)?.text==='What the fuck, Cheese?','uncensored message sent to selected brain');
  const friend=frame.scene.living.minds.residents.find(r=>r.id!=='cheese'&&r.present);
  await js(`(()=>{const b=[...document.querySelectorAll('.resident-picker button')].find(b=>b.textContent.startsWith(${JSON.stringify(friend.name+' ·')}));b.click()})()`);await pause(150);
  check(await js("document.querySelector('.resident-form textarea').getAttribute('aria-label')")===`Message to ${friend.name}`,'visitor gets their own chat target');
  await js("document.querySelector('.resident-form textarea').value='Let us take a quiet walk.';document.querySelector('.resident-form').requestSubmit()");await pause(70);
  check(inputs.at(-1)?.target===friend.id,'direct visitor chat preserves real persistent ID');
  await js("[...document.querySelectorAll('#pond-journal button')].find(b=>b.textContent==='I liked that').click()");await pause(70);
  check(inputs.at(-1)?.action==='mind_encourage'&&inputs.at(-1)?.target===friend.id,'feedback targets that character');
  frame.scene.living.minds.exchanges.push({id:999999,speaker:friend.id,name:friend.name,listener:'player',heard:'A test',text:'<img src=x onerror=alert(1)> Fuck yes.',source:'local'});
  win.webContents.send('hud-test:frame',frame);await pause(200);
  check(await js("!document.querySelector('.resident-thread img')&&document.querySelector('.resident-thread').textContent.includes('<img')"),'model output renders as literal text');
  frame.scene.living.minds.exchanges.pop();win.webContents.send('hud-test:frame',frame);await pause(200);
  await js("document.querySelector('.pond-body').scrollTop=180");
  fs.writeFileSync(path.join(out,'personalities.png'),(await win.webContents.capturePage()).toPNG());
  for(const [width,height] of [[920,640],[1700,960]]){
   win.setSize(width,height);await pause(200);
   check(await js("(()=>{const d=document.getElementById('pond-journal'),r=d.getBoundingClientRect();return r.left>=0&&r.right<=innerWidth&&r.bottom<=innerHeight&&d.scrollWidth<=d.clientWidth+2})()"),'notebook stays inside '+width+'px window');
  }
  check(!errors.length,'no renderer errors');
  fs.writeFileSync(path.join(out,'ui-checks.json'),JSON.stringify({result:'PASS',checks},null,2));console.log(JSON.stringify({result:'PASS',checks:checks.length}));app.exit(0);
 }catch(e){console.error(e,errors);fs.writeFileSync(path.join(out,'ui-failure.png'),(await win.webContents.capturePage()).toPNG());app.exit(1);}
});
