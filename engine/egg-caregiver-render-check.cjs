const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os'),crypto=require('node:crypto');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-egg-review-')));
app.whenReady().then(async()=>{try{
 const win=new BrowserWindow({show:false,webPreferences:{backgroundThrottling:false}});await win.loadFile(path.join(__dirname,'tests/egg-caregiver-theatre.html'));
 const all=process.argv.includes('--all'),native=all||process.argv.includes('--native'),out=path.join(__dirname,'artifacts/animation-milestone'),prefix=all?'egg-caregiver-all-native-render':native?'egg-caregiver-native-render':'egg-caregiver-render',source=native?fs.readFileSync(path.join(out,all?'egg-caregiver-all-frames.json':'egg-caregiver-frames.json'),'utf8'):null;
 const expression=native?'window.replayNativeEggCaregiver('+source+')':'window.reviewEggCaregiver()',result=await win.webContents.executeJavaScript('(()=>{try{return '+expression+';}catch(e){return {reviewError:e.stack||String(e)};}})()');if(result.reviewError)throw Error(result.reviewError);fs.mkdirSync(out,{recursive:true});
 for(const [name,data]of Object.entries(result.images))fs.writeFileSync(path.join(out,prefix+'-'+name+'.png'),Buffer.from(data.split(',')[1],'base64'));
 fs.writeFileSync(path.join(out,prefix+'-review.html'),'<!doctype html><meta charset="utf-8"><title>Egg caregiver rendering review</title><style>body{background:#142820;color:#eddec2;font:18px system-ui;margin:24px}img{width:100%}</style><h1>Egg caregiver rendering review</h1><p>Rendering evidence only; source scope recorded in JSON. Egg retains its original drawing and source root. No egg mechanical skill, attention or hatching reward is implied.</p>'+Object.keys(result.images).map(n=>'<h2>'+n+'</h2><img src="'+prefix+'-'+n+'.png">').join(''));
 delete result.images;if(native)result.sourceSha256=crypto.createHash('sha256').update(source).digest('hex');result.result='PASS';fs.writeFileSync(path.join(out,prefix+'.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result));
 // Electron redirects process.exit to app.exit; leave only after all awaited
 // capture work and synchronous artifact writes, using Node's terminal exit.
 process.reallyExit(0);
}catch(e){console.error(e);process.reallyExit(1);}});
