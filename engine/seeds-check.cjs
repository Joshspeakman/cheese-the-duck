const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-seeds-')));
app.whenReady().then(async()=>{
 const win=new BrowserWindow({show:false,webPreferences:{backgroundThrottling:false}}),out=path.join(os.tmpdir(),'cheese-seeds-review');fs.mkdirSync(out,{recursive:true});
 try{
  await win.loadFile(path.join(__dirname,'tests/seeds-theatre.html'));
  const images=await win.webContents.executeJavaScript('window.reviewSeeds()');
  for(const [name,data]of Object.entries(images))fs.writeFileSync(path.join(out,name+'.png'),Buffer.from(data.split(',')[1],'base64'));
  console.log(JSON.stringify({result:'PASS',objects:19,sheets:Object.keys(images).length,out}));app.exit(0);
 }catch(e){console.error(e);app.exit(1);}
});
