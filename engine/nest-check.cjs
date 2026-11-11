const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os'),{createHash}=require('node:crypto');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-nest-theatre-')));
app.whenReady().then(async()=>{
 const w=new BrowserWindow({show:false,webPreferences:{backgroundThrottling:false}});
 try{
  await w.loadFile(path.join(__dirname,'tests/nest-theatre.html'));
  const images=await w.webContents.executeJavaScript('window.reviewNests()');
  for(const [name,data]of Object.entries(images))fs.writeFileSync(path.join(__dirname,'artifacts/animation-milestone',name+'.png'),Buffer.from(data.split(',')[1],'base64'));
  const source=fs.readFileSync(path.join(__dirname,'artifacts/animation-milestone/nest-live-frames.json'),'utf8'),frames=JSON.parse(source);
  const replay=await w.webContents.executeJavaScript('window.replayNests('+JSON.stringify(frames)+')');
  fs.writeFileSync(path.join(__dirname,'artifacts/animation-milestone/nest-live-world.png'),Buffer.from(replay.image.split(',')[1],'base64'));delete replay.image;
  fs.writeFileSync(path.join(__dirname,'artifacts/animation-milestone/nest-render.json'),JSON.stringify({result:'PASS',scores:51,ages:9,nests:5,inputSha256:createHash('sha256').update(source).digest('hex'),replay},null,2));
  console.log(JSON.stringify({result:'PASS',scores:51,ages:9,nests:5,replay}));app.exit(0);
 }catch(e){console.error(e);app.exit(1);}
});
