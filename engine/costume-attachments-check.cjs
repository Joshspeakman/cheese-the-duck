const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-costume-attachments-')));
app.whenReady().then(async()=>{let win;try{
 win=new BrowserWindow({show:false,webPreferences:{backgroundThrottling:false}});await win.loadFile(path.join(__dirname,'tests/costume-attachments-theatre.html'));
 const result=await win.webContents.executeJavaScript('window.reviewCostumeAttachments()'),out=path.join(__dirname,'artifacts/animation-milestone');fs.mkdirSync(out,{recursive:true});
 for(const [name,data]of Object.entries(result.images))fs.writeFileSync(path.join(out,'costume-attachments-'+name+'.png'),Buffer.from(data.split(',')[1],'base64'));
 fs.writeFileSync(path.join(out,'costume-attachments-review.html'),'<!doctype html><meta charset="utf-8"><title>Costume fitting review</title><style>body{background:#142820;color:#eddec2;font:18px system-ui;margin:24px}img{width:100%}a{color:#c0dfbb}</style><h1>Eight costume attachments</h1><p>Worn artwork review only. Native equipped IDs remain authoritative; no flight, material simulation, or repertoire completion is added. Egg remains undecorated.</p><p><a href="../../tests/costume-attachments-theatre.html">Interactive age, action and direction preview</a></p>'+Object.keys(result.images).map(n=>'<h2>'+n+'</h2><img src="costume-attachments-'+n+'.png">').join(''));
 delete result.images;result.result='PASS';fs.writeFileSync(path.join(out,'costume-attachments-render.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result));win.destroy();app.exit(0);setTimeout(()=>process.exit(0),500).unref();
}catch(e){console.error(e);win?.destroy();app.exit(1);setTimeout(()=>process.exit(1),500).unref();}});
