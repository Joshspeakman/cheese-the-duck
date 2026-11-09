const {app,BrowserWindow}=require('electron');
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-interface-')));
app.whenReady().then(async()=>{
  const win=new BrowserWindow({show:false,width:1500,height:1020,webPreferences:{contextIsolation:true,sandbox:true}});
  try{
    await win.loadFile(path.join(__dirname,'tests/interface.html'));
    const frames=fs.readFileSync(path.join(__dirname,'artifacts/interface-frames.json'),'utf8');
    const result=await win.webContents.executeJavaScript(`(() => {try{return window.checkInterface(${frames})}catch(e){return {error:e.stack}}})()`);
    if(result.error)throw new Error(result.error);
    const dir=path.join(__dirname,'artifacts/interface');fs.mkdirSync(dir,{recursive:true});
    for(const [name,data] of Object.entries(result.images))fs.writeFileSync(path.join(dir,name+'.png'),Buffer.from(data.split(',')[1],'base64'));
    delete result.images;fs.writeFileSync(path.join(dir,'checks.json'),JSON.stringify(result,null,2));
    console.log(JSON.stringify({result:'PASS',screens:result.checks.length,medianMs:result.medianMs,p95Ms:result.p95Ms,out:dir}));app.exit(0);
  }catch(error){console.error(error);app.exit(1);}
});
