const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-garment-review-')));
app.whenReady().then(async()=>{
 const w=new BrowserWindow({show:false,width:1500,height:1000,webPreferences:{backgroundThrottling:false}}),out=path.join(__dirname,'artifacts/animation-milestone');
 try{
  await w.loadFile(path.join(__dirname,'tests/garments-theatre.html'));
  const result=await w.webContents.executeJavaScript('(()=>{try{return window.reviewGarments('+fs.readFileSync(path.join(out,'garments-frames.json'),'utf8')+','+fs.readFileSync(path.join(out,'garments-care-frames.json'),'utf8')+')}catch(e){return {error:e.stack}}})()');if(result.error)throw Error(result.error);
  for(const [name,data]of Object.entries(result.images))fs.writeFileSync(path.join(out,'garments-'+name+'.png'),Buffer.from(data.split(',')[1],'base64'));
  fs.writeFileSync(path.join(out,'garments-review.html'),`<!doctype html><meta charset="utf-8"><title>Cheese · The wardrobe atelier</title><style>body{margin:32px;background:#132b28;color:#e5d5b5;font:18px/1.5 system-ui}img{width:100%}a{color:#bad9c0}</style><h1>The wardrobe atelier</h1><p>18 constructed garments and compact fitting across the original wardrobes. Material state comes from the native game. <a href="../../tests/garments-theatre.html">Open the interactive age, action and weather preview.</a></p>${Object.keys(result.images).map(n=>`<figure><figcaption>${n}</figcaption><img loading="lazy" src="garments-${n}.png"></figure>`).join('')}`);
  delete result.images;result.result='PASS';fs.writeFileSync(path.join(out,'garments-render.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));app.exit(0);
 }catch(e){console.error(e);app.exit(1);}
});
