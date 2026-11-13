const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-rep-')));
app.whenReady().then(async()=>{
 const win=new BrowserWindow({show:false,webPreferences:{backgroundThrottling:false}}),out=path.join(__dirname,'artifacts/animation-milestone');
 win.webContents.on('console-message',d=>{if(d.level==='error')console.error(d.message);});
 try{
  await win.loadFile(path.join(__dirname,'tests/rep-theatre.html'));
  const frames=fs.readFileSync(path.join(out,'rep-frames.json'),'utf8');
  const r=await win.webContents.executeJavaScript('(()=>{try{return window.replayRep('+frames+')}catch(e){return {error:e.stack||String(e)}}})()');
  if(r.error)throw Error(r.error);
  if(process.argv.includes('--full')){const f=await win.webContents.executeJavaScript('window.fullFrame('+JSON.stringify(JSON.parse(frames)[0])+')');fs.writeFileSync(path.join(out,'rep-full-0.png'),Buffer.from(f.image.split(',')[1],'base64'));console.log(JSON.stringify({home:f.home,sx:f.sx,sy:f.sy}));}
  for(const [name,data] of Object.entries(r.images))fs.writeFileSync(path.join(out,name+'.png'),Buffer.from(data.split(',')[1],'base64'));
  console.log(JSON.stringify({result:'PASS',frames:r.frames,staged:r.staged,sheets:Object.keys(r.images).length}));app.exit(0);
 }catch(e){console.error(e);app.exit(1);}
});
