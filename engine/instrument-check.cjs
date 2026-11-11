const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-music-render-')));
app.whenReady().then(async()=>{
 const w=new BrowserWindow({show:false,webPreferences:{backgroundThrottling:false}}),out=path.join(__dirname,'artifacts/animation-milestone');
 try{
  await w.loadFile(path.join(__dirname,'tests/instrument-theatre.html'));
  const images=await w.webContents.executeJavaScript('({...window.reviewMusic(),...window.reviewPhrases()})');
  let replay={};
  if(!process.argv.includes('--art-only')){
   replay=await w.webContents.executeJavaScript('window.replayMusic('+fs.readFileSync(path.join(out,'instrument-frames.json'),'utf8')+')');
   Object.assign(images,replay.images);delete replay.images;
  }
  for(const [name,data]of Object.entries(images))fs.writeFileSync(path.join(out,name+'.png'),Buffer.from(data.split(',')[1],'base64'));
  const result={result:'PASS',sheets:Object.keys(images).length,replay};
  fs.writeFileSync(path.join(out,'instrument-render.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));app.exit(0);
 }catch(e){console.error(e);app.exit(1);}
});
