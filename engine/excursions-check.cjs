const {app,BrowserWindow}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-excursions-')));
app.whenReady().then(async()=>{
 const win=new BrowserWindow({show:false,webPreferences:{backgroundThrottling:false}}),out=path.join(__dirname,'artifacts/animation-milestone');
 try{
  await win.loadFile(path.join(__dirname,'tests/excursions-theatre.html'));
  const images=await win.webContents.executeJavaScript('window.reviewExcursions()');
  const frames=path.join(out,'excursions-frames.json');
  const replay=fs.existsSync(frames)?await win.webContents.executeJavaScript('window.replayExcursions('+fs.readFileSync(frames,'utf8')+')'):null;
  if(replay){Object.assign(images,replay.images);delete replay.images;}
  for(const [n,data]of Object.entries(images))fs.writeFileSync(path.join(out,n+'.png'),Buffer.from(data.split(',')[1],'base64'));
  fs.writeFileSync(path.join(out,'excursions-review.html'),`<!doctype html><meta charset="utf-8"><title>Cheese · Carnival and travel art review</title>
<style>body{margin:32px auto;max-width:1500px;background:#142b23;color:#eadcb9;font:18px/1.5 system-ui}figure{margin:40px 0}img{width:100%;height:auto}a{color:#c4d8b4}figcaption{font-weight:600}nav{display:flex;gap:20px}</style>
<h1>Carnival and travel belongings</h1><p>Ten current Ultra constructions, weather states and actual pond captures. Empty mechanisms use native saved clocks. Riding, character control contacts, shared performances and full individual repertoires remain in development.</p>
<nav><a href="#excursions-objects-0">Construction sheets</a><a href="#excursions-weather">Weather</a><a href="#excursions-live-wheelbarrow-day">In the pond</a></nav>
${Object.keys(images).map(n=>`<figure id="${n}"><figcaption>${n.replaceAll('excursions-','').replaceAll('-',' ').replaceAll('_',' ')}</figcaption><a href="${n}.png"><img loading="lazy" src="${n}.png" alt="${n}"></a></figure>`).join('\n')}`);
  const result={result:'PASS',sheets:Object.keys(images).length,replay};fs.writeFileSync(path.join(out,'excursions-render.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));app.exit(0);
 }catch(e){console.error(e);app.exit(1);}
});
