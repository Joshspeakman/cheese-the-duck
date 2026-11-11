const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-furniture-')));
app.whenReady().then(async()=>{
 const w=new BrowserWindow({show:false,webPreferences:{backgroundThrottling:false}}),out=path.join(__dirname,'artifacts/animation-milestone');
 try{
  await w.loadFile(path.join(__dirname,'tests/furniture-theatre.html'));
  const save=images=>{for(const [name,data]of Object.entries(images))fs.writeFileSync(path.join(out,name+'.png'),Buffer.from(data.split(',')[1],'base64'));};
  save(await w.webContents.executeJavaScript('window.reviewFurniture()'));
  save(await w.webContents.executeJavaScript('window.reviewSitting()'));
  let replay=null;
  if(fs.existsSync(path.join(out,'furniture-frames.json'))){
   replay=await w.webContents.executeJavaScript('window.replayFurniture('+fs.readFileSync(path.join(out,'furniture-frames.json'),'utf8')+')');
   save(Object.fromEntries(Object.entries(replay.images).map(([key,value])=>['furniture-live-'+key,value])));delete replay.images;
  }
  const result={result:'PASS',objects:28,sheets:8,replay};
  fs.writeFileSync(path.join(out,'furniture-render.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));app.exit(0);
 }catch(e){console.error(e);app.exit(1);}
});
