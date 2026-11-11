const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os'),{createHash}=require('node:crypto');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-shared-homes-')));
app.whenReady().then(async()=>{
 const w=new BrowserWindow({show:false,webPreferences:{backgroundThrottling:false}}),out=path.join(__dirname,'artifacts/animation-milestone');
 async function evaluate(expression){
  const result=await w.webContents.executeJavaScript('(()=>{try{return '+expression+'}catch(e){return {error:e.stack}}})()');
  if(result.error)throw Error(result.error);return result;
 }
 try{
  await w.loadFile(path.join(__dirname,'tests/shared-home-theatre.html'));
  const images=await evaluate('window.reviewHomes()');
  for(const [name,data]of Object.entries(images))fs.writeFileSync(path.join(out,name+'.png'),Buffer.from(data.split(',')[1],'base64'));
  const source=fs.readFileSync(path.join(out,'visitor-shelter-frames.json'),'utf8');
  const replay=await evaluate('window.replayHomes('+source+')');
  fs.writeFileSync(path.join(out,'shared-home-live.png'),Buffer.from(replay.image.split(',')[1],'base64'));delete replay.image;
  const companySource=fs.readFileSync(path.join(out,'shelter-company-frames.json'),'utf8');
  const company=await evaluate('window.replayHomes('+companySource+')');
  if(!company.paired)throw Error('Native replay had no shared shelter acting');
  fs.writeFileSync(path.join(out,'shelter-company-live.png'),Buffer.from(company.image.split(',')[1],'base64'));delete company.image;
  const result={result:'PASS',rooms:18,inputSha256:createHash('sha256').update(source).digest('hex'),replay,companyInputSha256:createHash('sha256').update(companySource).digest('hex'),company};
  fs.writeFileSync(path.join(out,'shared-home-render.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));app.exit(0);
 }catch(e){console.error(e);app.exit(1);}
});
