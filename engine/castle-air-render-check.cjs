// Source-pose gallery only. Native command/replay evidence is collected separately.
const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os'),crypto=require('node:crypto');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-air-review-')));
app.whenReady().then(async()=>{try{
 const win=new BrowserWindow({show:false,webPreferences:{backgroundThrottling:false}});
 await win.loadFile(path.join(__dirname,'tests/castle-air-theatre.html'));
 const out=path.join(__dirname,'artifacts/animation-milestone'),at=process.argv.indexOf('--frames'),native=at>=0||process.argv.includes('--native'),file=native?path.resolve(out,at>=0?process.argv[at+1]:'castle-air-frames.json'):null,source=native?fs.readFileSync(file,'utf8'):null,prefix=native?path.basename(file,'.json').replace(/-frames$/,'')+'-native-render':'castle-air-source-poses';
 const expression=native?'window.replayNativeAir('+source+')':'{images:window.reviewAirPoses(),scope:"source-pose-fixtures-only"}',result=await win.webContents.executeJavaScript('(()=>{try{return '+expression+';}catch(e){return {reviewError:e.stack||String(e)};}})()');if(result.reviewError)throw Error(result.reviewError);const images=result.images;
 fs.mkdirSync(out,{recursive:true});for(const [name,data]of Object.entries(images))fs.writeFileSync(path.join(out,prefix+'-'+name+'.png'),Buffer.from(data.split(',')[1],'base64'));
 fs.writeFileSync(path.join(out,prefix+'-review.html'),'<!doctype html><meta charset="utf-8"><title>Air rendering review</title><p>'+result.scope+'. Rendering evidence only; native procedure completion is evaluated separately.</p>'+Object.keys(images).map(n=>'<h2>'+n+'</h2><img style="width:100%" src="'+prefix+'-'+n+'.png">').join(''));
 delete result.images;if(native){result.sourceSha256=crypto.createHash('sha256').update(source).digest('hex');result.source=path.basename(file);}result.result='PASS';fs.writeFileSync(path.join(out,prefix+'.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({...result,coverage:result.coverage?Object.keys(result.coverage).length:undefined}));
 // Electron overrides process.exit; terminate this owned test only after all
 // awaited drawing and synchronous artifact writes have completed.
 process.reallyExit(0);
}catch(e){console.error(e);process.reallyExit(1);}});
