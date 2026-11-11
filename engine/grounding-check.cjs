const {app,BrowserWindow}=require('electron');
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-grounding-')));
app.whenReady().then(async()=>{
 try{
  const w=new BrowserWindow({show:false,width:1480,height:1020,webPreferences:{backgroundThrottling:false}});
  await w.loadFile(path.join(__dirname,'tests/grounding-theatre.html'));
  const result=await w.webContents.executeJavaScript('window.depthCheck()');
  const out=path.join(__dirname,'artifacts/animation-milestone');
  const frame=JSON.parse(fs.readFileSync(path.join(out,'grounding-frame.json'),'utf8'));
  await w.webContents.executeJavaScript('window.review('+JSON.stringify(frame)+')');
  fs.writeFileSync(path.join(out,'grounding-review.png'),Buffer.from(await w.webContents.executeJavaScript('window.capture()'),'base64'));
  fs.writeFileSync(path.join(out,'grounding-render.json'),JSON.stringify({result:'PASS',depth:result},null,2));
  console.log(JSON.stringify({result:'PASS',depth:result}));app.exit(0);
 }catch(e){console.error(e);app.exit(1);}
});
