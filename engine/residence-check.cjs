const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-residence-')));
app.whenReady().then(async()=>{const w=new BrowserWindow({show:false,webPreferences:{backgroundThrottling:false}});try{
 await w.loadFile(path.join(__dirname,'tests/residence.html'));
 const images=await w.webContents.executeJavaScript('window.checkResidence()');
 for(const [name,data]of Object.entries(images))fs.writeFileSync(path.join(__dirname,'artifacts/animation-milestone',name+'.png'),Buffer.from(data.split(',')[1],'base64'));
 console.log('PASS: shelter occupancy for nine ages, six rides at two ages, bounded image cache');app.exit(0);
 }catch(e){console.error(e);app.exit(1);}});
