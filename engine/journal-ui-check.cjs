// Journal cards for wonders, keeping pond, display shelf, wearables and the
// repertoire chooser drive real native work through IPC (disposable saves).
const {app,BrowserWindow,ipcMain}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const {spawn}=require('node:child_process'),{createInterface}=require('node:readline'),{pondCommand}=require('./pond-command.cjs');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-journal-ui-')));
app.whenReady().then(async()=>{
 let child,stderr='';const checks=[];
 try{
  const w=new BrowserWindow({show:false,width:1440,height:1000,webPreferences:{nodeIntegration:true,contextIsolation:false,backgroundThrottling:false}});
  const js=s=>w.webContents.executeJavaScript(s);
  // Re-find and click until it lands: frames re-render the journal between calls.
  const click=async(finder,label)=>{await until('(()=>{const b='+finder+';if(b&&!b.disabled){b.click();return true}return false})()',label);};
  const until=async(s,label)=>{const start=Date.now();while(!await js(s)){if(Date.now()-start>20000)throw Error(label+' timed out '+stderr.slice(-800));await new Promise(r=>setTimeout(r,30));}checks.push(label);};
  await w.loadFile(path.join(__dirname,'tests/physical-objects-theatre.html'));
  await until('Boolean(window.journal)','notebook initialized');
  ipcMain.on('physical-command',(_,raw)=>{const c=pondCommand(raw);if(c)child.stdin.write(JSON.stringify(c)+'\n');});
  child=spawn(path.join(__dirname,'../.venv/bin/python'),[path.join(__dirname,'ui_fixture.py')],{cwd:path.dirname(__dirname),stdio:['pipe','pipe','pipe']});
  child.stderr.on('data',b=>stderr=(stderr+b).slice(-5000));
  createInterface({input:child.stdout}).on('line',line=>{try{const m=JSON.parse(line);if(m.type==='physical_frame')js('window.receive('+JSON.stringify(m.frame)+')');}catch{}});
  const send=o=>child.stdin.write(JSON.stringify(o)+'\n');
  await until("window.frame?.item==='gong'",'placed gong arrives');
  await js("journal.show('belongings','gong',frame.copies[0])");
  await until("[...journal.body.querySelectorAll('[data-wonder-choice]')].some(b=>b.textContent.startsWith('Tapping the gong'))",'gong card lists its wonder routines');
  await click("[...journal.body.querySelectorAll('[data-wonder-choice]')].find(b=>b.textContent.startsWith('Tapping the gong'))",'gong routine clicked');
  await until("journal.world.plan?.wonder_work?.id==='gong_soft_tap'",'a wonder button starts the real routine');
  send({type:'test_advance',until:'finish'});await until('!journal.world.plan','routine finishes');
  send({type:'test_fixture',item:'koi_pond'});await until("frame.item==='koi_pond'",'koi pond arrives');
  await js("journal.show('belongings','koi_pond',frame.copies[0])");
  await until("[...journal.body.querySelectorAll('button')].some(b=>b.textContent.startsWith('Keep the koi'))",'koi pond offers the real koi catch');
  await click("[...journal.body.querySelectorAll('button')].find(b=>b.textContent.startsWith('Keep the koi'))",'Keep clicked');
  await until("(journal.world.instances[frame.copies[0]].keeping.fish||[]).length===1",'Keep moves the catch into the pond');
  await js("journal.show('belongings','koi_pond',frame.copies[0])");
  await until("[...journal.body.querySelectorAll('.pond-rep-row select')].some(s=>[...s.options].some(o=>o.value==='koi_kiss'))",'the kept koi gets a repertoire chooser');
  await js("{const s=[...journal.body.querySelectorAll('.pond-rep-row select')].find(s=>[...s.options].some(o=>o.value==='koi_scatter_flakes'));s.value='koi_scatter_flakes';s.nextElementSibling.click()}");
  await until("journal.world.plan?.rep_work?.id==='koi_scatter_flakes'",'the chooser starts real repertoire work');
  send({type:'test_advance',until:'finish'});await until("!journal.world.plan&&journal.world.instances[frame.copies[0]].keeping.flakes>0",'flakes actually land in the pond');
  send({type:'test_fixture',item:'trophy_case'});await until("frame.item==='trophy_case'",'trophy case arrives');
  await js("journal.show('belongings','trophy_case',frame.copies[0])");
  await until("[...journal.body.querySelectorAll('button')].some(b=>b.textContent==='Display portrait cheese')",'the owned card can be displayed');
  await click("[...journal.body.querySelectorAll('button')].find(b=>b.textContent==='Display portrait cheese')",'Display clicked');
  await until("(journal.world.instances[frame.copies[0]]?.display?.items||[]).includes('portrait_cheese')",'Display puts the card on the shelf');
  send({type:'test_fixture',item:'scarf_red'});await until("frame.item==='scarf_red'",'owned scarf arrives');
  await js("journal.show('belongings','scarf_red')");
  await until("[...journal.body.querySelectorAll('.pond-rep-row select')].some(s=>[...s.options].some(o=>o.value==='scarf_fluff'))",'the scarf gets a chooser');
  await js("{const s=[...journal.body.querySelectorAll('.pond-rep-row select')].find(s=>[...s.options].some(o=>o.value==='scarf_fluff'));s.value='scarf_fluff';s.nextElementSibling.click()}");
  await until("journal.world.plan?.rep_work?.id==='scarf_fluff'&&!journal.world.plan.instance",'the scarf routine runs in place');
  send({type:'quit'});console.log(JSON.stringify({result:'PASS',checks:checks.length}));app.exit(0);
 }catch(e){console.error("AFTER: "+checks.at(-1));try{console.error("STATE: "+await js("JSON.stringify({plan:journal.world.plan,notice:document.body.innerText.slice(-200),btn:[...journal.body.querySelectorAll('.pond-rep-row button')].map(b=>[b.textContent,b.disabled])})"));}catch(x){}console.error(e.message);try{child?.stdin.write('{"type":"quit"}\n');}catch{}app.exit(1);}
});
