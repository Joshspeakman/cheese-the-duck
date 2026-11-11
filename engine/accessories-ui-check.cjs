// Actual notebook controls with a native scene; all commands go to a test host.
const {app,BrowserWindow,ipcMain}=require('electron');
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-accessory-ui-')));
const out=path.join(__dirname,'artifacts/animation-milestone');
const frame=JSON.parse(fs.readFileSync(path.join(__dirname,'artifacts/interface-frames.json'))).pond;
frame.scene=JSON.parse(fs.readFileSync(path.join(out,'accessories-journal-scene.json')));frame.ui.modal=null;frame.ui.state='playing';frame.meta.talking=false;
let win;const inputs=[],errors=[],checks=[];
ipcMain.on('hud-test:ready',()=>win.webContents.send('hud-test:frame',frame));
ipcMain.on('hud-test:input',(_e,c)=>inputs.push(c));
const pause=ms=>new Promise(r=>setTimeout(r,ms)),check=(v,label)=>{if(!v)throw Error(label);checks.push(label);};
app.whenReady().then(async()=>{
 win=new BrowserWindow({show:false,width:1500,height:1000,webPreferences:{preload:path.join(__dirname,'tests/hud-preload.cjs'),contextIsolation:true,sandbox:true,backgroundThrottling:false}});
 win.webContents.on('console-message',d=>{if(d.level==='error')errors.push(d.message);});
 const js=s=>win.webContents.executeJavaScript(s);
 try{
  await win.loadFile(path.join(__dirname,'client/index.html'));await pause(650);
  await js("document.getElementById('pond').click();document.querySelector('[data-tab=mind]').click()");
  check(await js("['hat_blue','glasses_nerd','scarf_red','headphones'].every(id=>document.querySelector('[data-hat-material='+id+']'))"),'all four equipped care panels appear in the live plans notebook');
  check(await js("document.querySelector('[data-hat-care=scarf_red]').textContent.includes('Red Scarf')&&!document.querySelector('[data-hat-material=scarf_red]').textContent.includes('lens')"),'the notebook uses the original item name and material-appropriate description');
  check(await js("!document.querySelector('[data-hat-item=glasses_nerd][data-hat-action=wipe_lenses]').disabled"),'actual lens fog enables polishing');
  await js("document.querySelector('[data-hat-item=glasses_nerd][data-hat-action=wipe_lenses]').click()");await pause(100);
  check(inputs.some(c=>c.type==='pond'&&c.action==='hat_care'&&c.target==='glasses_nerd'&&c.text==='wipe_lenses'),'notebook sends the exact original equipped item and care request');
  frame.scene.duck.hatCare.active={item:'glasses_nerd',id:'wipe_lenses',elapsed:2,applied:false,label:'Polish the lenses'};
  for(const entry of [frame.scene.duck.hatCare,...(frame.scene.duck.hatCare.items||[])])entry.options.forEach(o=>{o.enabled=false;o.reason='Let Cheese finish what he is doing.';});
  win.webContents.send('hud-test:frame',frame);await pause(200);
  check(await js("[...document.querySelectorAll('[data-hat-action]')].every(b=>b.disabled)"),'ongoing care disables duplicate requests without replacing the panel');
  check(await js("document.querySelector('[data-hat-care=glasses_nerd]').textContent==='Polish the lenses'"),'native care status updates in place');
  const material=frame.scene.duck.apparel.glasses_nerd;material.snow=0;material.wet=0;material.fog=0;material.soil=0;material.slack=0;
  frame.scene.duck.hatCare.active=null;win.webContents.send('hud-test:frame',frame);await pause(200);
  check(await js("document.querySelector('[data-hat-material=glasses_nerd]').textContent==='Dry'"),'material description reflects the actual current wardrobe state');
  fs.writeFileSync(path.join(out,'accessories-notebook.png'),(await win.webContents.capturePage()).toPNG());
  check(await js("document.querySelector('[data-hat-material=scarf_red]').textContent.includes('Soaked')"),'care on the lenses does not clear a different accessory');
  check(!errors.length,'no notebook renderer errors');
  fs.writeFileSync(path.join(out,'accessories-ui.json'),JSON.stringify({result:'PASS',checks},null,2));console.log(JSON.stringify({result:'PASS',checks:checks.length}));app.exit(0);
 }catch(e){console.error(e,errors);app.exit(1);}
});
