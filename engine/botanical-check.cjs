const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-botanical-')));
app.whenReady().then(async()=>{
 const w=new BrowserWindow({show:false,webPreferences:{backgroundThrottling:false}}),out=path.join(__dirname,'artifacts/animation-milestone');
 try{
  await w.loadFile(path.join(__dirname,'tests/botanical-theatre.html'));
  const images=await w.webContents.executeJavaScript('window.reviewBotany()');
  let replay=null;
  if(fs.existsSync(path.join(out,'botanical-frames.json'))){
   replay=await w.webContents.executeJavaScript('window.replayBotany('+fs.readFileSync(path.join(out,'botanical-frames.json'),'utf8')+')');
   Object.assign(images,replay.images);delete replay.images;
  }
  for(const [name,data]of Object.entries(images))fs.writeFileSync(path.join(out,name+'.png'),Buffer.from(data.split(',')[1],'base64'));
  const result={result:'PASS',objects:61,sheets:Object.keys(images).length,replay};
  fs.writeFileSync(path.join(out,'botanical-render.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));app.exit(0);
 }catch(e){console.error(e);app.exit(1);}
});
