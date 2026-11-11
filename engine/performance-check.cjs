const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-performance-')));
app.whenReady().then(async()=>{const w=new BrowserWindow({show:false,width:1800,height:1150,webPreferences:{backgroundThrottling:false}});const errors=[];w.webContents.on('console-message',m=>{if(m.level==='error')errors.push(m.message);});try{
 await w.loadFile(path.join(__dirname,'tests/performance-gallery.html'));
 for(const [label,id,age,p]of [['adult-duck','friend:marco','adult',.4],['hatchling-toad','grumpy_toad','hatchling',.7],['elder-owl','wise_owl','elder',.55]]){
  await w.webContents.executeJavaScript(`window.paint(${p},${JSON.stringify(id)},${JSON.stringify(age)})`);
  for(const y of [0,950]){await w.webContents.executeJavaScript(`scrollTo(0,${y})`);await new Promise(r=>setTimeout(r,80));fs.writeFileSync(path.join(__dirname,'artifacts/animation-milestone',`performance-${label}-${y}.png`),(await w.webContents.capturePage()).toPNG());}
 }
 if(errors.length)throw Error(errors.join('\n'));
 console.log('PASS: twelve paired timelines rendered in three cast/age combinations');app.exit(0);
 }catch(e){console.error(e);app.exit(1);}});
