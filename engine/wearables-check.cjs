const {app,BrowserWindow}=require('electron');
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-wearables-')));
app.whenReady().then(async()=>{
 const win=new BrowserWindow({show:false,width:1500,height:1020,webPreferences:{contextIsolation:true,sandbox:true}});
 try{
  await win.loadFile(path.join(__dirname,'tests/wearables.html'));
  const frames=fs.readFileSync(path.join(__dirname,'artifacts/interface-frames.json'),'utf8');
  const result=await win.webContents.executeJavaScript(`(() => {try{return window.checkWearables(${frames})}catch(e){return {error:e.stack}}})()`);
  if(result.error)throw Error(result.error);
  const out=path.join(__dirname,'artifacts/wearables');fs.mkdirSync(out,{recursive:true});
  for(const [name,data] of Object.entries(result.images))fs.writeFileSync(path.join(out,name+'.png'),Buffer.from(data.split(',')[1],'base64'));
  delete result.images;fs.writeFileSync(path.join(out,'checks.json'),JSON.stringify(result,null,2));console.log(JSON.stringify({result:'PASS',...result,out}));app.exit(0);
 }catch(error){console.error(error);app.exit(1);}
});
