const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-keepsakes-')));
app.whenReady().then(async()=>{
 const win=new BrowserWindow({show:false,webPreferences:{backgroundThrottling:false}}),out=path.join(__dirname,'artifacts/animation-milestone');fs.mkdirSync(out,{recursive:true});
 try{
  await win.loadFile(path.join(__dirname,'tests/keepsakes-theatre.html'));
  const images=await win.webContents.executeJavaScript('window.reviewKeepsakes()');let replay=null;
  if(fs.existsSync(path.join(out,'keepsake-frames.json'))){replay=await win.webContents.executeJavaScript('window.replayKeepsakes('+fs.readFileSync(path.join(out,'keepsake-frames.json'),'utf8')+')');Object.assign(images,replay.images);delete replay.images;}
  let glass=null;if(fs.existsSync(path.join(out,'glass-curios-frames.json'))){glass=await win.webContents.executeJavaScript('window.replayKeepsakes('+fs.readFileSync(path.join(out,'glass-curios-frames.json'),'utf8')+')');Object.assign(images,glass.images);delete glass.images;}
  let weather=null;if(fs.existsSync(path.join(out,'glass-curios-weathers.json'))){weather=await win.webContents.executeJavaScript('window.reviewGlassWeather('+fs.readFileSync(path.join(out,'glass-curios-weathers.json'),'utf8')+')');Object.assign(images,weather.images);delete weather.images;}
  for(const [name,data]of Object.entries(images))fs.writeFileSync(path.join(out,name+'.png'),Buffer.from(data.split(',')[1],'base64'));
  const result={result:'PASS',objects:15,sheets:Object.keys(images).length,replay,glass,weather};fs.writeFileSync(path.join(out,'keepsake-render.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));app.exit(0);
 }catch(e){console.error(e);app.exit(1);}
});
