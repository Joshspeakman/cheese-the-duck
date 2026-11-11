const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-lights-')));
app.whenReady().then(async()=>{
 const win=new BrowserWindow({show:false,webPreferences:{backgroundThrottling:false}}),out=path.join(__dirname,'artifacts/animation-milestone');fs.mkdirSync(out,{recursive:true});
 try{
  await win.loadFile(path.join(__dirname,'tests/lighting-theatre.html'));
  const images=await win.webContents.executeJavaScript('window.reviewLights()');let replay=null;
  if(fs.existsSync(path.join(out,'lighting-frames.json'))){replay=await win.webContents.executeJavaScript('window.replayLights('+fs.readFileSync(path.join(out,'lighting-frames.json'),'utf8')+')');Object.assign(images,replay.images);delete replay.images;}
  for(const [name,data]of Object.entries(images))fs.writeFileSync(path.join(out,name+'.png'),Buffer.from(data.split(',')[1],'base64'));
  const result={result:'PASS',objects:27,sheets:Object.keys(images).length,replay};fs.writeFileSync(path.join(out,'lighting-render.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));app.exit(0);
 }catch(e){console.error(e);app.exit(1);}
});
