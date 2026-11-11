const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-reading-review-')));
app.whenReady().then(async()=>{
 const win=new BrowserWindow({show:false,webPreferences:{backgroundThrottling:false}}),out=path.join(__dirname,'artifacts/animation-milestone');
 win.webContents.on('console-message',({message})=>console.error(message));
 try{
  await win.loadFile(path.join(__dirname,'tests/keepsake-company-theatre.html'));
  const images=await win.webContents.executeJavaScript('window.reviewCompany()');
  const replay=await win.webContents.executeJavaScript('window.replayCompany('+fs.readFileSync(path.join(out,'keepsake-company-frames.json'),'utf8')+')');
  Object.assign(images,replay.images);delete replay.images;
  for(const [name,data]of Object.entries(images))fs.writeFileSync(path.join(out,name+'.png'),Buffer.from(data.split(',')[1],'base64'));
  const result={result:'PASS',sheets:Object.keys(images).length,...replay};fs.writeFileSync(path.join(out,'keepsake-company-render.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));app.exit(0);
 }catch(e){console.error(e);app.exit(1);}
});
