const {app,BrowserWindow}=require('electron');
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const out=path.join(__dirname,'artifacts/overhaul');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-overhaul-visual-')));
app.whenReady().then(async()=>{
 const win=new BrowserWindow({show:false,width:1440,height:1000,webPreferences:{contextIsolation:true,sandbox:true,backgroundThrottling:false}}),errors=[];
 win.webContents.on('console-message',(_e,...args)=>{if(args[0]>=2)errors.push(args[1]);});
 try{
  await win.loadFile(path.join(__dirname,'tests/overhaul.html'));
  const scene=JSON.parse(fs.readFileSync(path.join(out,'scene.json')));
  const result=await win.webContents.executeJavaScript(`window.runOverhaul(${JSON.stringify(scene)})`);
  for(const [key,data] of Object.entries(result.images))fs.writeFileSync(path.join(out,key+'.png'),Buffer.from(data.split(',')[1],'base64'));
  delete result.images;
  const tabs=['pond','mind','belongings','friends','weather','projects','field','memories'];
  for(const tab of tabs){await win.webContents.executeJavaScript(`window.journal.show('${tab}')`);await new Promise(r=>setTimeout(r,100));fs.writeFileSync(path.join(out,'journal-'+tab+'.png'),(await win.webContents.capturePage()).toPNG());}
  const ui=await win.webContents.executeJavaScript(`(()=>{const j=window.journal;j.show('mind');const b=[...j.body.querySelectorAll('button')].find(b=>b.textContent.includes('curious'));b.click();const command=window.lastCommand;j.show('belongings');const search=j.body.querySelector('input');search.value='ball';search.dispatchEvent(new Event('input'));return {command,filtered:[...j.body.querySelectorAll('.pond-item-list button')].map(b=>b.textContent),width:j.dialog.scrollWidth,clientWidth:j.dialog.clientWidth};})()`);
  if(ui.command.action!=='policy'||ui.command.target!=='curious'||ui.width>ui.clientWidth+1)throw Error(JSON.stringify(ui));
  if(result.errors.length||errors.length)throw Error(JSON.stringify({result,errors}));
  fs.writeFileSync(path.join(out,'visual-checks.json'),JSON.stringify({...result,ui,tabs},null,2));console.log(JSON.stringify({result:'PASS',...result,tabs:tabs.length,ui}));app.exit(0);
 }catch(e){console.error(e);app.exit(1);}
});
