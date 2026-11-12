// Actual notebook controls and production IPC serializer, using native scene data.
const {app,BrowserWindow}=require('electron');
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const assert=require('node:assert/strict');
const {pondCommand}=require('./pond-command.cjs');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-shared-ui-')));
app.whenReady().then(async()=>{
 let win;
 try{
  const out=path.join(__dirname,'artifacts/animation-milestone');
  const scene=JSON.parse(fs.readFileSync(path.join(out,'castle-shared-frames.json')))[0];
  const instance=scene.living.plan.instance;scene.living.plan=null;
  win=new BrowserWindow({show:false,webPreferences:{nodeIntegration:true,contextIsolation:false,backgroundThrottling:false}});
  await win.loadFile(path.join(__dirname,'tests/physical-objects-theatre.html'));
  const js=s=>win.webContents.executeJavaScript(s);
  await js('window.receive('+JSON.stringify({scene,item:'bounce_house',copies:[instance]})+')');
  const scores=['castle_start','castle_door_open','castle_hose_stow'];
  assert.deepEqual(await js("[...journal.body.querySelectorAll('[data-carnival-together]')].map(b=>b.dataset.carnivalTogether).sort()"),[...scores].sort());
  for(const score of scores){
   await js(`journal.body.querySelector('[data-carnival-together="${score}"]').click()`);
   const command=await js('window.commands.at(-1)');
   assert.deepEqual(pondCommand(command),{type:'pond',action:'carnival_action',target:'bounce_house',instance,text:score,together:true});
  }
  await js("journal.world.plan={label:'Busy',phase:'act',progress:0};journal.updateDynamic()");
  assert.equal(await js("[...journal.body.querySelectorAll('[data-carnival-together]')].every(b=>b.disabled)"),true);
  await js('journal.world.plan=null;journal.updateDynamic()');
  assert.equal(await js("[...journal.body.querySelectorAll('[data-carnival-together]')].every(b=>!b.disabled)"),true);
  await js('journal.world.layout.copies=[];journal.updateDynamic()');
  assert.equal(await js("[...journal.body.querySelectorAll('[data-carnival-together]')].every(b=>b.disabled)"),true);
  const result={result:'PASS',checks:7,scope:'notebook shared invitation, exact copy IPC, busy and stored state'};
  fs.writeFileSync(path.join(out,'castle-shared-ui.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result));
  win.destroy();app.exit(0);setTimeout(()=>process.exit(0),500).unref();
 }catch(error){console.error(error);win?.destroy();app.exit(1);setTimeout(()=>process.exit(1),500).unref();}
});
