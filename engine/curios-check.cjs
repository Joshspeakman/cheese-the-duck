const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-curios-')));
// Usage: electron curios-check.cjs [id,id,...] [frame]   (no ids = all sheets)
app.whenReady().then(async()=>{
 const win=new BrowserWindow({show:false,webPreferences:{backgroundThrottling:false}}),out=path.join(__dirname,'artifacts/animation-milestone');fs.mkdirSync(out,{recursive:true});
 win.webContents.on('console-message',d=>{if(d.level==='error')console.error(d.message);});
 const args=process.argv.slice(app.isPackaged?1:2).filter(a=>!a.startsWith('-')),only=args[0]?JSON.stringify(args[0].split(',')):'null',frame=Number(args[1]||0);
 try{
  await win.loadFile(path.join(__dirname,'tests/curios-theatre.html'));
  const run=src=>win.webContents.executeJavaScript('(()=>{try{return '+src+'}catch(e){return {error:e.stack||String(e)}}})()');
  const result=await run(`window.reviewCurios(${only},${frame})`);if(result.error)throw Error(result.error);
  const images={...result.images};
  if(only==='null'){const scale=await run('window.reviewCurioScale()');if(scale.error)throw Error(scale.error);images['curios-scale']=scale.image;}
  const prefix=only==='null'?'':'.';
  for(const [name,data]of Object.entries(images))fs.writeFileSync(path.join(out,(only==='null'?name:'curios-one-'+name.slice(7))+'.png'),Buffer.from(data.split(',')[1],'base64'));
  const report={result:'PASS',objects:result.drawn,sheets:Object.keys(images).length};console.log(JSON.stringify(report));app.exit(0);
 }catch(e){console.error(e);app.exit(1);}
});
