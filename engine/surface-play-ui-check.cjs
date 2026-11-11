const {app,BrowserWindow,ipcMain}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const {spawn}=require('node:child_process'),{createInterface}=require('node:readline'),{pondCommand}=require('./pond-command.cjs');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-surface-ui-')));
app.whenReady().then(async()=>{
 let child,stderr='';const checks=[],out=path.join(__dirname,'artifacts/animation-milestone');
 try{
  const w=new BrowserWindow({show:false,width:1440,height:1000,webPreferences:{nodeIntegration:true,contextIsolation:false,backgroundThrottling:false}}),js=s=>w.webContents.executeJavaScript(s);
  const until=async(s,label)=>{const start=Date.now();while(!await js(s)){if(Date.now()-start>15000)throw Error(label+' timed out '+stderr);await new Promise(r=>setTimeout(r,30));}checks.push(label);};
  ipcMain.on('physical-command',(_,raw)=>{const c=pondCommand(raw);if(c)child.stdin.write(JSON.stringify(c)+'\n');});
  for(const [item,choice]of [['bounce_house','bounce_together'],['magic_carpet','carpet_climb']]){
   await w.loadFile(path.join(__dirname,'tests/physical-objects-theatre.html'));await until('Boolean(window.journal)',item+' notebook initializes');
   child=spawn(path.join(__dirname,'../.venv/bin/python'),[path.join(__dirname,'check_surface_play.py'),'--serve',item],{cwd:path.dirname(__dirname),stdio:['pipe','pipe','pipe']});
   child.stderr.on('data',b=>stderr=(stderr+b).slice(-5000));
   createInterface({input:child.stdout}).on('line',line=>{try{const m=JSON.parse(line);if(m.type==='physical_frame')js('window.receive('+JSON.stringify(m.frame)+');journal.render()');}catch{}});
   await until('Boolean(window.frame)',item+' actual placed surface reaches notebook');
   await until("journal.body.querySelectorAll('[data-carnival-choice]').length===14&&[...journal.body.querySelectorAll('[data-carnival-choice]')].every(b=>!b.disabled)",item+' fourteen authored choices available');
   await js("journal.body.querySelector('[data-carnival-choice="+choice+"]').click()");
   await until("journal.world.plan?.carnival_work?.id==='"+choice+"'&&journal.world.plan.instance===frame.copies[0]&&journal.world.plan.phase==='approach'",item+' choice crosses production validator into exact native copy');
   await until("[...journal.body.querySelectorAll('[data-carnival-choice]')].every(b=>b.disabled)",item+' controls become busy while approaching');
   child.stdin.write('{"type":"test_advance","until":"play"}\n');
   await until("journal.world.plan?.carnival_work?.stage==='play'&&journal.world.instances[frame.copies[0]].uses===0",item+' actual entry starts play without early reward');
   child.stdin.write('{"type":"test_advance","seconds":15}\n');
   await until("journal.world.plan?.carnival_work?.clock>14.9&&journal.world.instances[frame.copies[0]].excursion.surface.active",item+' native shared surface runs');
   if(item==='magic_carpet')await until("journal.world.instances[frame.copies[0]].excursion.surface.lift>5",item+' selected hover really raises the occupied carpet');
   fs.writeFileSync(path.join(out,'surface-'+item+'-notebook.png'),(await w.webContents.capturePage()).toPNG());
   child.stdin.write('{"type":"test_advance","until":"finish"}\n');
   await until("!journal.world.plan&&journal.world.instances[frame.copies[0]].uses===1&&journal.world.instances[frame.copies[0]].carnival_routines['"+choice+"']===1",item+' exit records one original use');
   await until("[...journal.body.querySelectorAll('[data-carnival-choice]')].every(b=>!b.disabled)",item+' controls reopen after getting off');
   child.stdin.end('{"type":"quit"}\n');await new Promise((resolve,reject)=>{child.once('exit',code=>code===0?resolve():reject(Error('Native exit '+code+' '+stderr)));setTimeout(()=>reject(Error('Shutdown timed out')),5000).unref();});child=null;
  }
  const result={result:'PASS',checks};fs.writeFileSync(path.join(out,'surface-play-ui.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));app.exit(0);
 }catch(e){console.error(e);if(child)child.stdin.end('{"type":"quit"}\n');app.exit(1);}
});
