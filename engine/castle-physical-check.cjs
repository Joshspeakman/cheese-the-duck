const {app,BrowserWindow}=require('electron');
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-native-castle-')));
app.whenReady().then(async()=>{
 const win=new BrowserWindow({show:false,webPreferences:{backgroundThrottling:false}});
 const out=path.join(__dirname,'artifacts/animation-milestone');
 try{
  const frames=JSON.parse(fs.readFileSync(path.join(out,'castle-physical-frames.json'),'utf8'));
  await win.loadFile(path.join(__dirname,'tests/castle-physical-theatre.html'));
  const result=await win.webContents.executeJavaScript('(()=>{try{return window.replayPhysicalCastle('+JSON.stringify(frames)+')}catch(error){return {error:error.stack}}})()');
  if(result.error)throw Error(result.error);
  for(const [name,data]of Object.entries(result.images))fs.writeFileSync(path.join(out,'castle-physical-'+name+'.png'),Buffer.from(data.split(',')[1],'base64'));
  const names=Object.keys(result.images);delete result.images;result.result='PASS';
  fs.writeFileSync(path.join(out,'castle-physical-render.json'),JSON.stringify(result,null,2));
  fs.writeFileSync(path.join(out,'castle-physical-review.html'),'<!doctype html><meta charset="utf-8"><title>Native castle contact review</title><style>body{max-width:1500px;margin:30px auto;background:#142b23;color:#eadcb9;font:18px system-ui}img{max-width:100%}</style><h1>Native castle contact review</h1><p>Production simulation frames projected at three window sizes and two camera positions. This is partial contact evidence, not full repertoire certification.</p>'+names.map(n=>'<figure><figcaption>'+n+'</figcaption><img loading="lazy" src="castle-physical-'+n+'.png"></figure>').join(''));
  console.log(JSON.stringify(result));win.destroy();app.exit(0);
 }catch(e){console.error(e);win.destroy();app.exit(1);}
});
