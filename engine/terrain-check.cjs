const {app,BrowserWindow}=require('electron');
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-terrain-review-')));
app.whenReady().then(async()=>{
 try{
  const w=new BrowserWindow({show:false,width:1480,height:1000,webPreferences:{backgroundThrottling:false}});
  await w.loadFile(path.join(__dirname,'tests/terrain-theatre.html'));
  const out=path.join(__dirname,'artifacts/animation-milestone'),reviews=JSON.parse(fs.readFileSync(path.join(out,'terrain-review-frames.json'),'utf8'));
  const result=await w.webContents.executeJavaScript('window.check('+JSON.stringify(reviews)+')');
  fs.writeFileSync(path.join(out,'terrain-contact-sheet.png'),Buffer.from(await w.webContents.executeJavaScript('window.capture()'),'base64'));
  for(const location of ['Home Pond','Mushroom Grove','Shipwreck Cove','Waterfall']){
   const frame=reviews.find(r=>r.scene.location===location);
   fs.writeFileSync(path.join(out,'terrain-'+location.toLowerCase().replaceAll(' ','-')+'.png'),Buffer.from(await w.webContents.executeJavaScript('window.review('+JSON.stringify(frame)+')'),'base64'));
  }
  fs.writeFileSync(path.join(out,'terrain-render.json'),JSON.stringify({result:'PASS',...result},null,2));
  console.log(JSON.stringify({result:'PASS',...result}));app.exit(0);
 }catch(e){console.error(e);app.exit(1);}
});
