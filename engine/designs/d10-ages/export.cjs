// Builds a self-contained, offline design gallery using the actual game terrain.
// Never loads the simulation or changes the installed game.
const {app,BrowserWindow}=require('electron');
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const {pathToFileURL}=require('node:url');
const {execFileSync}=require('node:child_process');
const engine=path.resolve(__dirname,'../..'),out=path.join(engine,'artifacts/d10-ages');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-d10-ages-')));
app.whenReady().then(async()=>{
  const win=new BrowserWindow({show:false,width:1500,height:1100,webPreferences:{contextIsolation:true,sandbox:true,backgroundThrottling:false}});
  try{
    const {AGES:OPTIONS,ageSprite:optionSprite}=await import(pathToFileURL(path.join(__dirname,'ages.mjs')));
    if(OPTIONS.length!==9||new Set(OPTIONS.map(o=>o.art.join('\n'))).size!==9)throw Error('Expected all nine distinct ages');
    let poses=0;
    for(const o of OPTIONS)for(const action of ['idle','walking','ruffle','quack'])for(const facing of [true,false])for(let i=0;i<32;i++){
      const m=optionSprite(o,i*.18,action,facing);poses++;
      if(m.art.some((r,y)=>!/^[\x20-\x7e]*$/.test(r)||r.length!==m.tones[y].length))throw Error('Invalid ASCII: '+o.id);
      if(m.art.some(r=>r[0]!==' '||r.at(-1)!==' ')||m.art[0].trim()||m.art.at(-1).trim())throw Error('Clipped pose: '+o.id);
      if(o.height>=90)throw Error('Study is not smaller: '+o.id);
    }
    await win.loadFile(path.join(__dirname,'template.html'));
    const rendererURL=pathToFileURL(path.join(engine,'client/ultra-renderer.mjs')).href,sceneURL=pathToFileURL(path.join(engine,'tests/scenes.mjs')).href;
    const scenes=await win.webContents.executeJavaScript(`(async()=>{
      const {SceneCanvas}=await import(${JSON.stringify(rendererURL)}),{scene}=await import(${JSON.stringify(sceneURL)});

      const result={};
      for(const [key,hour] of [['day',12],['dusk',18.5],['night',23]]){
        const c=new SceneCanvas();c.resize(1200,620);const s=scene({hour,motion:false,particles:false,weatherEffects:false,season:'fall'});s.duck.hidden=true;
        c.draw(s,2,1/30);result[key]=c.canvas.toDataURL();

      }return result;
    })()`);
    const template=fs.readFileSync(path.join(__dirname,'template.html'),'utf8'),cute=fs.readFileSync(path.join(__dirname,'../cute-mallards/options.mjs'),'utf8').replace(/^export /gm,''),ages=fs.readFileSync(path.join(__dirname,'ages.mjs'),'utf8').replace(/^import .*;\n/gm,'').replace(/^export /gm,''),gallery=fs.readFileSync(path.join(__dirname,'gallery.mjs'),'utf8').replace(/^import .*;\n/gm,'');
    const options=`const {OPTIONS:CUTE_OPTIONS,optionSprite:cuteSprite,drawStudy:drawCute}=(()=>{${cute}\nreturn {OPTIONS,optionSprite,drawStudy};})();\n${ages}`;
    const script=`(async()=>{const SCENES=${JSON.stringify(scenes)};\n${options}\n${gallery}\n})();`;
    fs.mkdirSync(out,{recursive:true});const file=path.join(out,'Cheese - D10 All Ages.html');
    fs.writeFileSync(file,template.replace('<!-- GALLERY_SCRIPT -->',`<script>${script}</script>`));
    await win.loadFile(file);
    await win.webContents.executeJavaScript(`new Promise((resolve,reject)=>{const end=Date.now()+12000;function poll(){if(window.galleryReady)resolve();else if(Date.now()>end)reject(Error('Gallery failed to load'));else setTimeout(poll,40)}poll()})`);
    await win.webContents.executeJavaScript(`(()=>{
      const $=id=>document.getElementById(id),buttons=[...document.querySelectorAll('.option')];
      if(buttons.length!==9||$('age').options.length!==9)throw Error('Missing ages');
      for(const [i,b] of buttons.entries()){b.click();if($('age').selectedIndex!==i)throw Error('Age selection failed');}
      $('play').click();if($('play').getAttribute('aria-pressed')!=='false')throw Error('Pause failed');
      const frame=$('world').toDataURL();$('facing').click();if(frame===$('world').toDataURL())throw Error('Facing failed');$('facing').click();
      for(const mode of ['day','dusk','night']){$('light').value=mode;$('light').dispatchEvent(new Event('change'));}
      for(const action of ['idle','walking','ruffle','quack']){$('action').value=action;$('action').dispatchEvent(new Event('change'));}
      $('scrub').value=270;$('scrub').dispatchEvent(new Event('input'));if($('play').getAttribute('aria-pressed')!=='false')throw Error('Scrub did not pause');
      $('light').value='day';$('light').dispatchEvent(new Event('change'));$('action').value='walking';$('action').dispatchEvent(new Event('change'));buttons[5].click();window.checkAdultParity();
    })()`);
    const exports=await win.webContents.executeJavaScript('window.exportStudies()');
    for(const [name,data] of Object.entries(exports))fs.writeFileSync(path.join(out,name+'.png'),Buffer.from(data.split(',')[1],'base64'));
    fs.writeFileSync(path.join(out,'gallery.png'),(await win.webContents.capturePage()).toPNG());
    if(!process.argv.includes('--stills-only')){
      const frames=path.join(out,'frames');fs.mkdirSync(frames,{recursive:true});
      for(let i=0;i<72;i++){const data=await win.webContents.executeJavaScript(`window.animationFrame(${i})`);fs.writeFileSync(path.join(frames,`frame-${String(i).padStart(3,'0')}.png`),Buffer.from(data.split(',')[1],'base64'));}
      execFileSync('/opt/homebrew/bin/ffmpeg',['-y','-loglevel','error','-framerate','12','-i',path.join(frames,'frame-%03d.png'),'-filter_complex','[0:v]split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=none','-loop','0',path.join(out,'d10-all-ages-waddling.gif')],{timeout:60000});
    }
    const result={result:'PASS',ages:9,poses,checks:['ASCII and bounds','all ages selectable','adult D10 pixel parity','pause','facing','three lighting scenes','four motions','frame scrub'],gallery:file};fs.writeFileSync(path.join(out,'checks.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));app.exit(0);
  }catch(error){console.error(error);app.exit(1);}
});
