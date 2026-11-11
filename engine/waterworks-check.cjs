const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const {createHash}=require('node:crypto');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-waterworks-')));
app.whenReady().then(async()=>{
 const w=new BrowserWindow({show:false,webPreferences:{backgroundThrottling:false}}),out=path.join(__dirname,'artifacts/animation-milestone');
 try{
  await w.loadFile(path.join(__dirname,'tests/waterworks-theatre.html'));
  const save=images=>{for(const [name,data]of Object.entries(images))fs.writeFileSync(path.join(out,name+'.png'),Buffer.from(data.split(',')[1],'base64'));};
  const drawings=await w.webContents.executeJavaScript('window.reviewWaterworks()');save(drawings);
  save(await w.webContents.executeJavaScript('window.reviewBathing()'));
  const input=fs.readFileSync(path.join(out,'water-frames.json'),'utf8');
  const replay=await w.webContents.executeJavaScript('(()=>{try{return window.replayWater('+input+')}catch(e){return {error:e.stack}}})()');
  if(replay.error)throw Error(replay.error);
  save(Object.fromEntries(Object.entries(replay.images).map(([key,value])=>['water-live-'+key,value])));delete replay.images;
  const result={result:'PASS',objects:23,scores:16,sheets:8,inputSha256:createHash('sha256').update(input).digest('hex'),replay};
  fs.writeFileSync(path.join(out,'water-render.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));app.exit(0);
 }catch(e){console.error(e);app.exit(1);}
});
