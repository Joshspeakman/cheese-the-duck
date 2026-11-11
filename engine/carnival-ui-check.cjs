const {app,BrowserWindow,ipcMain}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const {spawn}=require('node:child_process'),{createInterface}=require('node:readline'),{pondCommand}=require('./pond-command.cjs');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-carnival-ui-')));
app.whenReady().then(async()=>{
 let child,stderr='';const checks=[],out=path.join(__dirname,'artifacts/animation-milestone');
 try{
  const w=new BrowserWindow({show:false,width:1440,height:1000,webPreferences:{nodeIntegration:true,contextIsolation:false,backgroundThrottling:false}}),js=s=>w.webContents.executeJavaScript(s);
  const until=async(s,label)=>{const start=Date.now();while(!await js(s)){if(Date.now()-start>15000)throw Error(label+' timed out '+stderr);await new Promise(r=>setTimeout(r,30));}checks.push(label);};
  await w.loadFile(path.join(__dirname,'tests/physical-objects-theatre.html'));await until('Boolean(window.journal)','notebook initializes');
  ipcMain.on('physical-command',(_,raw)=>{const c=pondCommand(raw);if(c)child.stdin.write(JSON.stringify(c)+'\n');});
  child=spawn(path.join(__dirname,'../.venv/bin/python'),[path.join(__dirname,'check_carnival.py'),'--serve'],{cwd:path.dirname(__dirname),stdio:['pipe','pipe','pipe']});
  child.stderr.on('data',b=>stderr=(stderr+b).slice(-5000));
  createInterface({input:child.stdout}).on('line',line=>{try{const m=JSON.parse(line);if(m.type==='physical_frame')js('window.receive('+JSON.stringify(m.frame)+');journal.render()');}catch{}});
  await until('Boolean(window.frame)','real ride reaches notebook');
  await until("journal.body.querySelectorAll('[data-carnival-choice]').length===6&&[...journal.body.querySelectorAll('[data-carnival-choice]')].every(b=>!b.disabled)",'six authored ride choices available');
  await js("journal.body.querySelector('[data-carnival-choice=wheel_clouds]').click()");
  await until("journal.world.plan?.carnival_work?.id==='wheel_clouds'&&journal.world.plan.instance===frame.copies[0]&&journal.world.plan.phase==='approach'",'choice crosses production command validator to selected native ride');
  await until("[...journal.body.querySelectorAll('[data-carnival-choice]')].every(b=>b.disabled)",'ride choices become busy during approach');
  child.stdin.write('{"type":"test_advance","until":"ride"}\n');
  await until("journal.world.plan?.carnival_work?.stage==='ride'&&journal.world.instances[frame.copies[0]].uses===0",'boarding reaches native riding without early reward');
  child.stdin.write('{"type":"test_advance","until":"finish"}\n');
  await until("!journal.world.plan&&journal.world.instances[frame.copies[0]].uses===1&&journal.world.instances[frame.copies[0]].carnival_routines.wheel_clouds===1",'complete ride records one actual use');
  await until("[...journal.body.querySelectorAll('[data-carnival-choice]')].every(b=>!b.disabled)",'notebook enables another ride after getting off');
  fs.writeFileSync(path.join(out,'carnival-notebook.png'),(await w.webContents.capturePage()).toPNG());
  const result={result:'PASS',checks,commands:await js('window.commands')};fs.writeFileSync(path.join(out,'carnival-ui.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));
  child.stdin.end('{"type":"quit"}\n');await new Promise((resolve,reject)=>{child.once('exit',code=>code===0?resolve():reject(Error('Native exit '+code+' '+stderr)));setTimeout(()=>reject(Error('Shutdown timed out')),5000).unref();});app.exit(0);
 }catch(e){console.error(e);if(child)child.stdin.end('{"type":"quit"}\n');app.exit(1);}
});
