const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-carnival-review-')));
app.whenReady().then(async()=>{
 const win=new BrowserWindow({show:false,webPreferences:{backgroundThrottling:false}}),out=path.join(__dirname,'artifacts/animation-milestone');
 try{
  await win.loadFile(path.join(__dirname,'tests/carnival-theatre.html'));
  const result=await win.webContents.executeJavaScript('window.replayCarnival('+fs.readFileSync(path.join(out,'carnival-frames.json'),'utf8')+')');
  for(const [n,data]of Object.entries(result.images))fs.writeFileSync(path.join(out,'carnival-'+n+'.png'),Buffer.from(data.split(',')[1],'base64'));
  fs.writeFileSync(path.join(out,'carnival-review.html'),`<!doctype html><meta charset="utf-8"><title>Cheese · Shared carnival rides</title><style>body{margin:32px auto;max-width:1500px;background:#142b23;color:#eadcb9;font:18px/1.5 system-ui}figure{margin:40px 0}img{width:100%;height:auto}a{color:#c4d8b4}figcaption{font-weight:600}</style><h1>Shared carnival rides</h1><p>Actual native boarding, shared riding and disembarking snapshots. These are twelve initial performance scores for two objects; the complete individual repertoires remain in development.</p>${Object.keys(result.images).map(n=>`<figure><figcaption>${n.replaceAll('-',' ').replaceAll('_',' ')}</figcaption><a href="carnival-${n}.png"><img loading="lazy" src="carnival-${n}.png" alt="${n}"></a></figure>`).join('')}`);
  delete result.images;result.result='PASS';fs.writeFileSync(path.join(out,'carnival-render.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));app.exit(0);
 }catch(e){console.error(e);app.exit(1);}
});
