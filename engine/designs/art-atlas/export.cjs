// Build and exercise a portable, offline atlas from the current game renderer.
// Run: engine/node_modules/.bin/electron engine/designs/art-atlas/export.cjs
const {app,BrowserWindow}=require('electron');
const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),crypto=require('node:crypto');
const {execFileSync}=require('node:child_process');
const {pathToFileURL}=require('node:url');
const root=path.resolve(__dirname,'../../..'),engine=path.join(root,'engine'),out=path.join(engine,'artifacts/art-atlas');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-art-atlas-')));

function bundle(entry,data){
  const imports={},sources={},seen=new Set(),virtual=path.join(__dirname,'data.mjs');
  const id=file=>'cheese/'+path.relative(root,file).split(path.sep).join('/');
  function visit(file){
    if(seen.has(file))return id(file);seen.add(file);
    if(!file.startsWith(root+path.sep))throw Error('Unexpected module outside repo: '+file);
    let source=file===virtual?`export const DATA=${JSON.stringify(data)};`:fs.readFileSync(file,'utf8');
    sources[path.relative(root,file)]=crypto.createHash('sha256').update(source).digest('hex');
    source=source.replace(/^((?:import|export)\s[^;]*?\bfrom\s*)(['"])(\.[^'"]+)\2/gm,(_,prefix,quote,relative)=>{
      return prefix+quote+visit(path.resolve(path.dirname(file),relative))+quote;
    });
    imports[id(file)]='data:text/javascript;base64,'+Buffer.from(source).toString('base64');return id(file);
  }
  const main=visit(entry);
  return {script:`<script type="importmap">${JSON.stringify({imports}).replaceAll('<','\\u003c')}</script>\n<script type="module">import ${JSON.stringify(main)};</script>`,sources};
}

app.whenReady().then(async()=>{
  const win=new BrowserWindow({show:false,width:1480,height:1080,webPreferences:{contextIsolation:true,sandbox:true,backgroundThrottling:false}});
  const errors=[];win.webContents.on('console-message',details=>{if(details.level==='error')errors.push(details.message);});
  try{
    fs.mkdirSync(out,{recursive:true});
    const metadata=JSON.parse(execFileSync(path.join(root,'.venv/bin/python'),[path.join(__dirname,'export_metadata.py')],{
      cwd:root,encoding:'utf8',maxBuffer:8*1024*1024,env:{...process.env,PYGAME_HIDE_SUPPORT_PROMPT:'1',CHEESE_SAVE_DIR:fs.mkdtempSync(path.join(os.tmpdir(),'cheese-atlas-definitions-'))}
    }));
    const build={version:JSON.parse(fs.readFileSync(path.join(engine,'package.json'))).version,
      commit:execFileSync('git',['rev-parse','--short','HEAD'],{cwd:root,encoding:'utf8'}).trim(),date:new Date().toISOString().slice(0,10)};
    await win.loadFile(path.join(__dirname,'template.html'));
    const backgrounds=await win.webContents.executeJavaScript(`(async()=>{
      const {SceneCanvas}=await import(${JSON.stringify(pathToFileURL(path.join(engine,'client/ultra-renderer.mjs')).href)});
      const {scene}=await import(${JSON.stringify(pathToFileURL(path.join(engine,'tests/scenes.mjs')).href)});
      const result={};for(const [key,hour] of [['day',12],['dusk',18.5],['night',23]]){
        const c=new SceneCanvas();c.resize(1200,620);const s=scene({hour,motion:false,particles:false,weatherEffects:false,season:'fall'});s.duck.hidden=true;
        c.draw(s,2,1/30);result[key]=c.canvas.toDataURL();
      }return result;
    })()`);
    const {script,sources}=bundle(path.join(__dirname,'gallery.mjs'),{...metadata,build,backgrounds});
    const file=path.join(out,'Cheese - Complete Art Atlas.html');
    fs.writeFileSync(file,fs.readFileSync(path.join(__dirname,'template.html'),'utf8').replace('<!-- ATLAS_SCRIPT -->',script));
    // The delivered file must run with every external request blocked.
    const external=[];win.webContents.session.webRequest.onBeforeRequest((details,callback)=>{
      const blocked=/^https?:/.test(details.url);if(blocked)external.push(details.url);callback({cancel:blocked});
    });
    await win.loadFile(file);
    await win.webContents.executeJavaScript(`new Promise((resolve,reject)=>{const end=Date.now()+20000;const check=()=>window.galleryReady?resolve():Date.now()>end?reject(Error('Atlas startup timeout')):setTimeout(check,50);check();})`);
    const checks=await win.webContents.executeJavaScript(`(async()=>{
      const a=window.atlas,$=id=>document.getElementById(id),assert=(yes,msg)=>{if(!yes)throw Error(msg);};
      a.setPlaying(false);const expected={visitors:48,events:774,items:542,wearables:109,sprites:132,stories:8};
      for(const [k,n] of Object.entries(expected))assert(a.counts[k]===n,k+' count');
      assert(new Set(a.records.map(r=>r.uid)).size===a.records.length,'Duplicate IDs');
      const c=document.createElement('canvas');c.width=440;c.height=266;let rendered=0,textOnly=0;
      for(const r of a.records){
        if(r.kind==='events'&&r.animated===false){assert(a.model(r,0)===null,'Text event must not fabricate art');textOnly++;continue;}
        for(const t of [0,.7,2.1,5.6]){
          const m=a.model(r,t);assert(m.art.length>0&&m.art.some(row=>row.trim()),'Empty art: '+r.uid);
          assert(m.art.every(row=>typeof row==='string'),'Invalid art: '+r.uid);
          a.drawFitted(c,r,t);rendered++;
        }
        if(rendered%80===0)await new Promise(resolve=>setTimeout(resolve,0));
      }
      a.selectTab('visitors');$('filter').value='Rare visitors';$('filter').dispatchEvent(new Event('change'));assert(document.querySelectorAll('.card').length===8,'Rare filter');
      $('filter').value='all';$('search').value='wise_owl';$('search').dispatchEvent(new Event('input'));assert(document.querySelectorAll('.card').length===1,'Search');
      a.selectTab('visitors');const first=document.querySelector('.open-card').dataset.uid;$('next').click();assert(document.querySelector('.open-card').dataset.uid!==first,'Pagination');$('prev').click();
      a.open('visitors:wise_owl');assert($('pose').disabled,'Rare visitor should not offer invented walking');assert($('detail').open,'Detail dialog');
      for(const mode of ['studio','day','dusk','night']){$('backdrop').value=mode;$('backdrop').dispatchEvent(new Event('change'));}
      a.open(a.records.find(r=>r.kind==='visitors'&&r.subtype==='Regular duck friends').uid);
      assert(!$('pose').disabled,'Friend animation controls');$('pose').value='walking';$('pose').dispatchEvent(new Event('change'));a.setTime(.7);const before=$('large').toDataURL();$('facing').click();assert(before!==$('large').toDataURL(),'Facing control');
      const wearable=a.records.find(r=>r.kind==='items'&&r.wearable);a.open(wearable.uid);$('use').value='worn';$('use').dispatchEvent(new Event('change'));
      for(const option of $('age').options){$('age').value=option.value;$('age').dispatchEvent(new Event('change'));const m=a.model(wearable,1,true);assert(option.value==='egg'?m.rig===null:m.rig.stage===option.value,'Wearable age '+option.value);}
      assert($('age').options.length===9,'All ages');
      $('scrub').value=37;$('scrub').dispatchEvent(new Event('input'));assert($('time').textContent==='3.7 s','Scrub');
      const text=a.records.find(r=>r.animated===false);a.open(text.uid);assert($('large-caption').textContent.includes('does not attach'),'Text-only explanation');
      a.selectTab('events');$('filter').value='text';$('filter').dispatchEvent(new Event('change'));assert($('count').textContent.startsWith(textOnly+' '),'Text-only filter');
      a.selectTab('items');$('filter').value='wearables';$('filter').dispatchEvent(new Event('change'));assert($('count').textContent.startsWith('42 '),'Item / wardrobe overlap');
      a.selectTab('wearables');assert($('count').textContent.startsWith('109 '),'All fitted wearables');
      $('detail').close();a.selectTab('visitors');$('filter').value='Rare visitors';$('filter').dispatchEvent(new Event('change'));$('backdrop').value='studio';$('backdrop').dispatchEvent(new Event('change'));
      return {counts:a.counts,renderedFrames:rendered,textOnlyEvents:textOnly,wearables:109,ages:9,checks:['all entries render','text-only events stay text-only','search','filters','pagination','detail dialog','rare guest movement labels','friend poses and facing','all-age try-on','day/dusk/night','frame scrub','offline startup']};
    })()`);
    if(errors.length)throw Error(errors.join('\n'));if(external.length)throw Error('Atlas attempted external requests');
    const settle=()=>win.webContents.executeJavaScript('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))');
    await win.webContents.executeJavaScript('window.scrollTo(0,0)');await settle();
    fs.writeFileSync(path.join(out,'visitors.png'),(await win.webContents.capturePage()).toPNG());
    await win.webContents.executeJavaScript(`window.atlas.open('visitors:wise_owl')`);await settle();
    fs.writeFileSync(path.join(out,'rare-visitor.png'),(await win.webContents.capturePage()).toPNG());
    await win.webContents.executeJavaScript(`window.atlas.open('wearables:santa_hat');document.getElementById('age').value='adult';document.getElementById('age').dispatchEvent(new Event('change'));`);
    await settle();
    fs.writeFileSync(path.join(out,'wearable.png'),(await win.webContents.capturePage()).toPNG());
    const result={result:'PASS',build,...checks,externalRequests:external.length,bytes:fs.statSync(file).size,file,sources};
    fs.writeFileSync(path.join(out,'checks.json'),JSON.stringify(result,null,2));console.log(JSON.stringify({...result,sources:Object.keys(sources).length}));app.exit(0);
  }catch(error){console.error(error.stack||error);app.exit(1);}
});
