const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-wonders-')));
app.whenReady().then(async()=>{
 const win=new BrowserWindow({show:false,webPreferences:{backgroundThrottling:false}}),out=path.join(__dirname,'artifacts/animation-milestone');fs.mkdirSync(out,{recursive:true});
 win.webContents.on('console-message',d=>{if(d.level==='error')console.error(d.message);});
 try{
  await win.loadFile(path.join(__dirname,'tests/wonders-theatre.html'));
  const result=await win.webContents.executeJavaScript('(()=>{try{return window.reviewWonders()}catch(e){return {error:e.stack||String(e)}}})()');
  if(result.error)throw Error(result.error);
  let replay=null;const frames=path.join(out,'wonder-frames.json');
  if(fs.existsSync(frames)){replay=await win.webContents.executeJavaScript('(()=>{try{return window.replayWonders('+fs.readFileSync(frames,'utf8')+')}catch(e){return {error:e.stack||String(e)}}})()');if(replay.error)throw Error(replay.error);Object.assign(result.images,replay.images);delete replay.images;}
  let company=null;const cf=path.join(out,'wonder-company-frames.json');
  if(fs.existsSync(cf)){company=await win.webContents.executeJavaScript('(()=>{try{return window.replayWonderCompany('+fs.readFileSync(cf,'utf8')+')}catch(e){return {error:e.stack||String(e)}}})()');if(company.error)throw Error(company.error);Object.assign(result.images,company.images);delete company.images;}
  let perf=null;const group=path.join(out,'wonder-group-scene.json');
  if(fs.existsSync(group)){perf=await win.webContents.executeJavaScript('(()=>{try{return window.measureWonders('+fs.readFileSync(group,'utf8')+')}catch(e){return {error:e.stack||String(e)}}})()');if(perf.error)throw Error(perf.error);result.images['wonder-group']=perf.image;delete perf.image;}
  for(const [name,data]of Object.entries(result.images))fs.writeFileSync(path.join(out,name+'.png'),Buffer.from(data.split(',')[1],'base64'));
  const report={result:'PASS',objects:32,drawn:result.drawn,sheets:Object.keys(result.images).length,replay,company,perf};fs.writeFileSync(path.join(out,'wonders-render.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));app.exit(0);
 }catch(e){console.error(e);app.exit(1);}
});
