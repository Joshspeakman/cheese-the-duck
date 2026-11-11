const {app,BrowserWindow,ipcMain}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-footwear-ui-')));
const out=path.join(__dirname,'artifacts/animation-milestone'),frame=JSON.parse(fs.readFileSync(path.join(__dirname,'artifacts/interface-frames.json'))).pond;
frame.scene=JSON.parse(fs.readFileSync(path.join(out,'footwear-journal-scene.json')));frame.ui.modal=null;frame.ui.state='playing';frame.meta.talking=false;
let win;const inputs=[],errors=[],checks=[],pause=ms=>new Promise(r=>setTimeout(r,ms)),check=(v,label)=>{if(!v)throw Error(label);checks.push(label);};
ipcMain.on('hud-test:ready',()=>win.webContents.send('hud-test:frame',frame));ipcMain.on('hud-test:input',(_e,c)=>inputs.push(c));
app.whenReady().then(async()=>{
 win=new BrowserWindow({show:false,width:1500,height:1000,webPreferences:{preload:path.join(__dirname,'tests/hud-preload.cjs'),contextIsolation:true,sandbox:true,backgroundThrottling:false}});
 win.webContents.on('console-message',d=>{if(d.level==='error')errors.push(d.message);});const js=s=>win.webContents.executeJavaScript(s);
 try{
  await win.loadFile(path.join(__dirname,'client/index.html'));await pause(650);await js("document.getElementById('pond').click();document.querySelector('[data-tab=mind]').click()");
  check(await js("!!document.querySelector('[data-hat-material=ice_skates]')"),'actual equipped skates have a care panel');
  check(await js("document.querySelector('[data-hat-material=ice_skates]').textContent.includes('Left: soaked')&&document.querySelector('[data-hat-material=ice_skates]').textContent.includes('Right: damp')"),'each shoe has its own material description');
  check(await js("!document.querySelector('[data-hat-item=ice_skates][data-hat-action=tie_skates]').disabled"),'real loose laces enable care');
  await js("document.querySelector('[data-hat-item=ice_skates][data-hat-action=tie_skates]').click()");await pause(100);
  check(inputs.some(c=>c.type==='pond'&&c.action==='hat_care'&&c.target==='ice_skates'&&c.text==='tie_skates'),'notebook sends exact equipped item and native care');
  frame.scene.duck.hatCare.active={item:'ice_skates',id:'tie_skates',elapsed:2.9,appliedFeet:[0],applied:false,label:'Tighten both skate laces'};
  for(const entry of [frame.scene.duck.hatCare,...frame.scene.duck.hatCare.items])entry.options.forEach(o=>{o.enabled=false;o.reason='Let Cheese finish what he is doing.';});
  frame.scene.duck.apparel.ice_skates.slack_left=.08;win.webContents.send('hud-test:frame',frame);await pause(200);
  check(await js("[...document.querySelectorAll('[data-hat-action]')].every(b=>b.disabled)"),'ongoing pair care cannot be duplicated');
  check(await js("document.querySelector('[data-hat-care=ice_skates]').textContent==='Tighten both skate laces'"),'pair care status updates in place');
  check(await js("!document.querySelector('[data-hat-material=ice_skates]').textContent.split(' · ')[0].includes('loose')&&document.querySelector('[data-hat-material=ice_skates]').textContent.split(' · ')[1].includes('loose')"),'first contact tightens only the left skate in the live panel');
  fs.writeFileSync(path.join(out,'footwear-notebook.png'),(await win.webContents.capturePage()).toPNG());
  frame.scene.duck.apparel.ice_skates.slack_right=.06;frame.scene.duck.hatCare.active=null;win.webContents.send('hud-test:frame',frame);await pause(200);
  check(await js("!document.querySelector('[data-hat-material=ice_skates]').textContent.includes('loose')"),'second contact updates the remaining skate');
  check(!errors.length,'no notebook renderer errors');fs.writeFileSync(path.join(out,'footwear-ui.json'),JSON.stringify({result:'PASS',checks},null,2));console.log(JSON.stringify({result:'PASS',checks:checks.length}));app.exit(0);
 }catch(e){console.error(e,errors);app.exit(1);}
});
