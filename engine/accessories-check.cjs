const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-accessory-review-')));
app.whenReady().then(async()=>{
 const w=new BrowserWindow({show:false,width:1500,height:1000,webPreferences:{backgroundThrottling:false}}),out=path.join(__dirname,'artifacts/animation-milestone');
 try{
  await w.loadFile(path.join(__dirname,'tests/accessories-theatre.html'));
  const result=await w.webContents.executeJavaScript('(()=>{try{return window.reviewAccessories('+fs.readFileSync(path.join(out,'accessories-frames.json'),'utf8')+','+fs.readFileSync(path.join(out,'accessories-care-frames.json'),'utf8')+')}catch(e){return {error:e.stack}}})()');if(result.error)throw Error(result.error);
  for(const [name,data]of Object.entries(result.images))fs.writeFileSync(path.join(out,'accessories-'+name+'.png'),Buffer.from(data.split(',')[1],'base64'));
  fs.writeFileSync(path.join(out,'accessories-review.html'),`<!doctype html><meta charset="utf-8"><title>Cheese · The accessory drawer</title><style>body{margin:32px;background:#132b28;color:#e5d5b5;font:18px/1.5 system-ui}img{width:100%}a{color:#bad9c0}</style><h1>The accessory drawer</h1><p>25 constructed accessories and compact fitting across the original wardrobes. Material state comes from the native game. <a href="../../tests/accessories-theatre.html">Open the interactive age, action and weather preview.</a></p>${Object.keys(result.images).map(n=>`<figure><figcaption>${n}</figcaption><img loading="lazy" src="accessories-${n}.png"></figure>`).join('')}`);
  delete result.images;result.result='PASS';fs.writeFileSync(path.join(out,'accessories-render.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));app.exit(0);
 }catch(e){console.error(e);app.exit(1);}
});
