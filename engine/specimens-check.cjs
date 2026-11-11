const {app,BrowserWindow}=require('electron');
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
// Isolated review session: never opens the player's profile or saves.
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-specimens-review-')));
app.whenReady().then(async()=>{
 const w=new BrowserWindow({show:false,width:1450,height:1100,webPreferences:{backgroundThrottling:false}});
 try{
  await w.loadFile(path.join(__dirname,'tests/specimens-theatre.html'));
  const out=fs.mkdtempSync(path.join(os.tmpdir(),'cheese-specimens-art-'));
  for(const wet of [false,true]){
   const r=await w.webContents.executeJavaScript(`window.reviewSpecimens(${wet})`);
   if(r.count!==33)throw Error('Expected 33 specimen studies');
   fs.writeFileSync(path.join(out,wet?'weathered.png':'dry.png'),Buffer.from(r.image.split(',')[1],'base64'));
  }
  console.log(JSON.stringify({result:'PASS',count:33,out}));app.exit(0);
 }catch(error){console.error(error);app.exit(1);}
});
