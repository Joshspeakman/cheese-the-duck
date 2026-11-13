// Source gallery or native matrix replay; native request execution is separate.
const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os'),crypto=require('node:crypto');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-air-review-')));
app.whenReady().then(async()=>{try{
 const win=new BrowserWindow({show:false,webPreferences:{backgroundThrottling:false}});
 await win.loadFile(path.join(__dirname,'tests/castle-air-theatre.html'));
 const out=path.join(__dirname,'artifacts/animation-milestone'),at=process.argv.indexOf('--frames'),mat=process.argv.indexOf('--manifest');
 const manifestFile=mat>=0?path.resolve(out,process.argv[mat+1]):null,manifestSource=manifestFile?fs.readFileSync(manifestFile,'utf8'):null,manifest=manifestSource?JSON.parse(manifestSource):null;
 const native=at>=0||Boolean(manifest)||process.argv.includes('--native'),file=native?path.resolve(out,at>=0?process.argv[at+1]:manifest?.frames_file||'castle-air-frames.json'):null;
 const source=native?fs.readFileSync(file,'utf8'):null,sourceHash=source?crypto.createHash('sha256').update(source).digest('hex'):null,prefix=native?path.basename(file,'.json').replace(/-frames$/,'')+'-native-render':'castle-air-source-poses';
 if(manifest&&(manifest.frames_sha256!==sourceHash||path.basename(manifest.frames_file)!==path.basename(file)))throw Error('Matrix manifest does not bind these exact native frames');
 for(const dependency of manifest?.sources||[])for(const kind of ['manifest','frames']){
  const bytes=fs.readFileSync(path.resolve(out,dependency[kind+'_file']));if(crypto.createHash('sha256').update(bytes).digest('hex')!==dependency[kind+'_sha256'])throw Error('Stale matrix source '+dependency[kind+'_file']);
 }
 const expression=native?'window.replayNativeAir('+source+',{manifest:'+manifestSource+'})':'{images:window.reviewAirPoses(),scope:"source-pose-fixtures-only"}';
 const result=await win.webContents.executeJavaScript('(()=>{try{return '+expression+';}catch(e){return {reviewError:e.stack||String(e)};}})()');if(result.reviewError)throw Error(result.reviewError);const images=result.images;
 fs.mkdirSync(out,{recursive:true});for(const [name,data]of Object.entries(images))fs.writeFileSync(path.join(out,prefix+'-'+name+'.png'),Buffer.from(data.split(',')[1],'base64'));
 const matrixSummary=result.matrix?'<p>Selected supported cases: '+result.matrix.supportedCount+'. Refused cases: '+result.matrix.refusedCount+'. Retained failed setup attempts: '+result.matrix.failedAttemptCount+'. Support applies to the recorded placement and starting roots.</p>':'';
 fs.writeFileSync(path.join(out,prefix+'-review.html'),'<!doctype html><meta charset="utf-8"><title>Air rendering review</title><p>'+result.scope+'. Rendering evidence only; native procedure completion is evaluated separately.</p>'+matrixSummary+Object.keys(images).map(n=>'<h2>'+n+'</h2><img style="width:100%" src="'+prefix+'-'+n+'.png">').join(''));
 delete result.images;if(native){result.sourceSha256=sourceHash;result.source=path.basename(file);if(manifest){result.manifest=path.basename(manifestFile);result.manifestSha256=crypto.createHash('sha256').update(manifestSource).digest('hex');}}result.result='PASS';fs.writeFileSync(path.join(out,prefix+'.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({...result,coverage:result.coverage?Object.keys(result.coverage).length:undefined,matrix:result.matrix?{supported:result.matrix.supportedCount,refused:result.matrix.refusedCount,cases:result.matrix.caseCount}:undefined}));
 // Electron overrides process.exit; terminate this owned test only after all
 // awaited drawing and synchronous artifact writes have completed.
 process.reallyExit(0);
}catch(e){console.error(e);process.reallyExit(1);}});
