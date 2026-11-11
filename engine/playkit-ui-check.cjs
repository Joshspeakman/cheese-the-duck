const {app,BrowserWindow,ipcMain}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os'),{spawn}=require('node:child_process'),{createInterface}=require('node:readline'),{pondCommand}=require('./pond-command.cjs');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-playkit-ui-')));
app.whenReady().then(async()=>{let child,stderr='';const checks=[],out=path.join(__dirname,'artifacts/animation-milestone');try{
 const w=new BrowserWindow({show:false,width:1440,height:1000,webPreferences:{nodeIntegration:true,contextIsolation:false,backgroundThrottling:false}}),js=s=>w.webContents.executeJavaScript(s),send=c=>child.stdin.write(JSON.stringify(c)+'\n');
 const until=async(s,label)=>{const start=Date.now();while(!await js(s)){if(Date.now()-start>15000)throw Error(label+' timed out '+stderr+' '+await js('JSON.stringify({commands:window.commands,plan:journal.world?.plan,duck:frame.scene.duck,memories:journal.world?.memories?.slice(-3)})'));await new Promise(r=>setTimeout(r,30));}checks.push(label);};
 await w.loadFile(path.join(__dirname,'tests/physical-objects-theatre.html'));await until('Boolean(window.journal)','notebook initialized');
 ipcMain.on('physical-command',(_,raw)=>{const c=pondCommand(raw);if(c)send(c);});child=spawn(path.join(__dirname,'../.venv/bin/python'),[path.join(__dirname,'check_playkit.py'),'--serve'],{cwd:path.dirname(__dirname),stdio:['pipe','pipe','pipe']});child.stderr.on('data',b=>stderr=(stderr+b).slice(-5000));
 createInterface({input:child.stdout}).on('line',line=>{try{const m=JSON.parse(line);if(m.type==='physical_frame')js('window.receive('+JSON.stringify(m.frame)+')');}catch{}});
 await until('Boolean(window.frame)','native toy state arrives');
 for(const [item,choice,field,value]of [['bubble_machine','bubbler_start','power',1],['jump_rope','rope_coil','coil',1],['tiny_boat','boat_sail','sail',1],['surfboard','board_wax','waxes',2]]){
  await js('window.frame=null');send({type:'test_fixture',item});await until("frame?.item==='"+item+"'",item+' fixture arrives');await js("journal.show('belongings',frame.item,frame.copies[0]||null)");
  await until("Boolean(journal.body.querySelector('[data-playkit-choice=\""+choice+"\"]'))",choice+' is offered');await js("journal.body.querySelector('[data-playkit-choice=\""+choice+"\"]').click()");
  await until("journal.world.plan?.playkit_work?.id==='"+choice+"'",choice+' crosses the real command bridge');send({type:'test_advance'});
  await until("!journal.world.plan&&(frame.copies[0]?journal.world.instances[frame.copies[0]]:journal.world.objects[frame.item]).playkit."+field+"==="+value,choice+' changes the actual object');
  if(await js('frame.copies.length>1'))await until("journal.world.instances[frame.copies[1]].playkit."+field+"===0",'second copy remains unchanged');
  await until("journal.body.querySelector('[data-playkit-summary]').textContent.length>10",'live summary is visible');
 }
 fs.writeFileSync(path.join(out,'playkit-inspector.png'),(await w.webContents.capturePage()).toPNG());fs.writeFileSync(path.join(out,'playkit-ui.json'),JSON.stringify({result:'PASS',checks},null,2));console.log(JSON.stringify({result:'PASS',checks:checks.length}));child.stdin.end('{"type":"quit"}\n');await new Promise((res,rej)=>{child.once('exit',code=>code===0?res():rej(Error('Native exit '+code+' '+stderr)));setTimeout(()=>rej(Error('Shutdown timed out')),5000).unref();});app.exit(0);
 }catch(e){console.error(e);if(child)child.stdin.end('{"type":"quit"}\n');app.exit(1);}});
