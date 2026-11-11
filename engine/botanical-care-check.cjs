const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-garden-render-')));
app.whenReady().then(async()=>{
 const w=new BrowserWindow({show:false,webPreferences:{backgroundThrottling:false}}),out=path.join(__dirname,'artifacts/animation-milestone');
 try{
  await w.loadFile(path.join(__dirname,'tests/botanical-care-theatre.html'));
  const images=await w.webContents.executeJavaScript('window.reviewCare()');
  const replay=await w.webContents.executeJavaScript('window.replayCare('+fs.readFileSync(path.join(out,'botanical-care-frames.json'),'utf8')+')');
  Object.assign(images,replay.images);delete replay.images;
  for(const [name,data]of Object.entries(images))fs.writeFileSync(path.join(out,name+'.png'),Buffer.from(data.split(',')[1],'base64'));
  const result={result:'PASS',sheets:Object.keys(images).length,replay};
  fs.writeFileSync(path.join(out,'botanical-care-render.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));app.exit(0);
 }catch(e){console.error(e);app.exit(1);}
});
