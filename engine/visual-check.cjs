// Standalone renderer verification: no simulation, network or player saves.
const { app,BrowserWindow }=require('electron');
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-visual-')));
app.whenReady().then(async()=>{
 const win=new BrowserWindow({show:false,width:1500,height:1020,webPreferences:{contextIsolation:true,sandbox:true}});
 try{
  await win.loadFile(path.join(__dirname,'tests','visual.html'));
  const frame=JSON.parse(fs.readFileSync(path.join(__dirname,'artifacts','talk-frame.json')));
  const result=await win.webContents.executeJavaScript(`(() => { try { return window.runVisualChecks(${JSON.stringify(frame)}); } catch(e) { return {error:e.stack}; } })()`);
  if(result.error)throw new Error(result.error);
  const dir=path.join(__dirname,'artifacts','ultra');fs.mkdirSync(dir,{recursive:true});
  for(const [name,data] of Object.entries(result.images))fs.writeFileSync(path.join(dir,name+'.png'),Buffer.from(data.split(',')[1],'base64'));
  delete result.images;fs.writeFileSync(path.join(dir,'visual.json'),JSON.stringify(result,null,2));
  console.log(JSON.stringify({result:'PASS',...result,out:dir}));app.exit(0);
 }catch(err){console.error(err);app.exit(1);}
});
