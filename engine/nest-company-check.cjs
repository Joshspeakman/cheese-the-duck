const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-nest-company-review-')));
app.whenReady().then(async()=>{
 const w=new BrowserWindow({show:false,webPreferences:{backgroundThrottling:false}}),out=path.join(__dirname,'artifacts/animation-milestone');
 try{
  await w.loadFile(path.join(__dirname,'tests/nest-theatre.html'));
  const frames=JSON.parse(fs.readFileSync(path.join(out,'nest-company-frames.json'),'utf8'));
  const result=await w.webContents.executeJavaScript('window.replayNestCompany('+JSON.stringify(frames)+')');
  for(const [name,url]of Object.entries(result.images))fs.writeFileSync(path.join(out,'nest-company-'+name+'.png'),Buffer.from(url.split(',')[1],'base64'));
  delete result.images;fs.writeFileSync(path.join(out,'nest-company-render.json'),JSON.stringify({result:'PASS',...result},null,2));
  console.log(JSON.stringify({result:'PASS',...result}));app.exit(0);
 }catch(e){console.error(e);app.exit(1);}
});
