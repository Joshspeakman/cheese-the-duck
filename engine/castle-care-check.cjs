const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-castle-review-')));
app.whenReady().then(async()=>{
 const win=new BrowserWindow({show:false,webPreferences:{backgroundThrottling:false}}),out=path.join(__dirname,'artifacts/animation-milestone');
 try{
  await win.loadFile(path.join(__dirname,'tests/castle-care-theatre.html'));
  const result=await win.webContents.executeJavaScript('(()=>{try{return window.replayCastle('+fs.readFileSync(path.join(out,'castle-care-frames.json'),'utf8')+')}catch(e){return {error:e.stack}}})()');
  if(result.error)throw Error(result.error);
  for(const [n,data]of Object.entries(result.images))fs.writeFileSync(path.join(out,'castle-'+n+'.png'),Buffer.from(data.split(',')[1],'base64'));
  fs.writeFileSync(path.join(out,'castle-care-review.html'),`<!doctype html><meta charset="utf-8"><title>Cheese · The Wobbly Duck workshop</title><style>body{margin:32px auto;max-width:1500px;background:#142b23;color:#eadcb9;font:18px/1.5 system-ui}figure{margin:40px 0}img{width:100%;height:auto}a{color:#c4d8b4}figcaption{font-weight:600}</style><h1>The Wobbly Duck workshop</h1><p>Native arrivals, low physical controls, shared material work and actual fabric state. Twenty-four control scores and ten ordered care procedures extend the fourteen shared play routines. Procedures physically visit each component, preserve partial work, and complete as one activity. Full per-object repertoire audits remain open.</p>${Object.keys(result.images).map(n=>`<figure><figcaption>${n.replaceAll('-',' ').replaceAll('_',' ')}</figcaption><a href="castle-${n}.png"><img loading="lazy" src="castle-${n}.png" alt="${n}"></a></figure>`).join('')}`);
  delete result.images;result.result='PASS';fs.writeFileSync(path.join(out,'castle-care-render.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));app.exit(0);
 }catch(e){console.error(e);app.exit(1);}
});
