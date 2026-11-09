// Preview-only export. No simulation, saves, or installed app are modified.
const {app,BrowserWindow}=require('electron');
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const {pathToFileURL}=require('node:url');
const {execFileSync}=require('node:child_process');
const engine=path.resolve(__dirname,'../..'),out=path.join(engine,'artifacts','scruffy-cheese');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-scruffy-')));
app.whenReady().then(async()=>{
  const win=new BrowserWindow({show:false,webPreferences:{contextIsolation:true,sandbox:true,backgroundThrottling:false}});
  win.webContents.on('console-message',({level,message})=>{if(level==='error')console.error(message);});
  try{
    await win.loadFile(path.join(__dirname,'template.html'));
    const rendererURL=pathToFileURL(path.join(engine,'client','ultra-renderer.mjs')).href;
    const sceneURL=pathToFileURL(path.join(engine,'tests','scenes.mjs')).href;
    const background=await win.webContents.executeJavaScript(`(async()=>{
      const {SceneCanvas}=await import(${JSON.stringify(rendererURL)});
      const {scene}=await import(${JSON.stringify(sceneURL)});
      const canvas=new SceneCanvas();canvas.resize(1200,560);const s=scene({motion:false});s.duck.hidden=true;
      canvas.draw(s,2,1/30);return canvas.canvas.toDataURL('image/png');
    })()`);
    const template=fs.readFileSync(path.join(__dirname,'template.html'),'utf8');
    const sprites=fs.readFileSync(path.join(engine,'client','scruffy-sprites.mjs'),'utf8').replace(/^export /gm,'');
    const draw=fs.readFileSync(path.join(engine,'client','ultra-characters.mjs'),'utf8').split('export function drawCharacter')[1];
    const gallery=fs.readFileSync(path.join(__dirname,'gallery.mjs'),'utf8').replace(/^import .*;\n/gm,'');
    const script=`(async()=>{const SCENE=${JSON.stringify(background)};\n${sprites}\nfunction drawCharacter${draw}\n${gallery}\n})();`;
    fs.mkdirSync(out,{recursive:true});
    const file=path.join(out,'Cheese - Scruffy family and all ages.html');
    fs.writeFileSync(file,template.replace('<!-- GALLERY_SCRIPT -->',`<script>${script}</script>`));
    await win.loadFile(file);
    await win.webContents.executeJavaScript(`new Promise((resolve,reject)=>{
      const deadline=Date.now()+5000;const poll=()=>window.galleryReady?resolve():Date.now()>deadline?reject(Error('Gallery failed')):setTimeout(poll,25);poll();
    })`);
    await win.webContents.executeJavaScript(`(()=>{
      for(const [i,button] of [...document.querySelectorAll('#variants button')].entries()){
        button.click();if(!document.getElementById('selection').textContent.startsWith('ABCDEF'[i]))throw Error('Design selection failed');
      }
      const age=document.getElementById('age');if(age.options.length!==9)throw Error('Missing age');
      for(const option of age.options){age.value=option.value;age.dispatchEvent(new Event('change'));}
      const action=document.getElementById('action');if(action.options.length!==10)throw Error('Missing action');
      for(const option of action.options){action.value=option.value;action.dispatchEvent(new Event('change'));}
      age.value='adult';age.dispatchEvent(new Event('change'));action.value='walking';action.dispatchEvent(new Event('change'));
      const world=document.getElementById('world'),before=world.toDataURL();
      document.getElementById('facing').click();if(world.toDataURL()===before)throw Error('Facing did not mirror');
      document.getElementById('facing').click();document.getElementById('step').click();
      if(document.getElementById('play').getAttribute('aria-pressed')!=='false')throw Error('Frame step did not pause');
      const slider=document.getElementById('timeline');slider.value=600;slider.dispatchEvent(new Event('input'));
      if(!document.getElementById('counter').textContent.includes('5'))throw Error('Timeline did not select pose');
      document.querySelector('#variants button').click();
    })()`);
    const images=await win.webContents.executeJavaScript('window.exportSheets()');
    for(const [name,data] of Object.entries(images))fs.writeFileSync(path.join(out,name+'.png'),Buffer.from(data.split(',')[1],'base64'));
    console.log(JSON.stringify({result:'PASS',sheets:Object.keys(images).length,gallery:file}));
    if(!process.argv.includes('--stills-only')){
      for(const [kind,count,name] of [['ages',24,'all-ages-waddle'],['variants',240,'scruffy-animation-reel']]){
        const frameDir=path.join(out,kind+'-frames');fs.mkdirSync(frameDir,{recursive:true});
        for(let i=0;i<count;i++){
          const data=await win.webContents.executeJavaScript(`window.animationFrame(${JSON.stringify(kind)},${i})`);
          fs.writeFileSync(path.join(frameDir,`frame-${String(i).padStart(3,'0')}.png`),Buffer.from(data.split(',')[1],'base64'));
        }
        execFileSync('/opt/homebrew/bin/ffmpeg',['-y','-loglevel','error','-framerate','12','-i',path.join(frameDir,'frame-%03d.png'),
          '-filter_complex','[0:v]split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse=dither=none','-loop','0',path.join(out,name+'.gif')],{timeout:60000});
        console.log(JSON.stringify({animation:name,frames:count}));
      }
    }
    app.exit(0);
  }catch(error){console.error(error);app.exit(1);}
});
