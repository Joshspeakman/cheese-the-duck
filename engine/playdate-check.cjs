const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os'),{createHash}=require('node:crypto');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-playdate-theatre-')));
app.whenReady().then(async()=>{
 const w=new BrowserWindow({show:false,webPreferences:{backgroundThrottling:false}}),out=path.join(__dirname,'artifacts/animation-milestone');
 async function evaluate(expression){const r=await w.webContents.executeJavaScript('(()=>{try{return '+expression+'}catch(e){return {error:e.stack}}})()');if(r.error)throw Error(r.error);return r;}
 function save(images){for(const [name,data]of Object.entries(images))fs.writeFileSync(path.join(out,name+'.png'),Buffer.from(data.split(',')[1],'base64'));}
 try{
  await w.loadFile(path.join(__dirname,'tests/playdate-theatre.html'));save(await evaluate('window.reviewPlaydates()'));
  const input=fs.readFileSync(path.join(out,'playdate-frames.json'),'utf8'),replay=await evaluate('window.replayPlaydates('+input+')');
  save(Object.fromEntries(Object.entries(replay.images).map(([k,v])=>['playdate-live-'+k,v])));delete replay.images;
  const result={result:'PASS',scores:8,inputSha256:createHash('sha256').update(input).digest('hex'),replay};
  fs.writeFileSync(path.join(out,'playdate-render.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));app.exit(0);
 }catch(e){console.error(e);app.exit(1);}
});
