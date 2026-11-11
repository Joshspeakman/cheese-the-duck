const {app,BrowserWindow,ipcMain}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const {spawn}=require('node:child_process'),{createInterface}=require('node:readline'),{pondCommand}=require('./pond-command.cjs');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-nest-ui-')));
app.whenReady().then(async()=>{
 let child,stderr='';const checks=[],out=path.join(__dirname,'artifacts/animation-milestone');
 try{
  const w=new BrowserWindow({show:false,width:1440,height:1000,webPreferences:{nodeIntegration:true,contextIsolation:false,backgroundThrottling:false}});
  const js=s=>w.webContents.executeJavaScript(s);
  const until=async(s,label)=>{const start=Date.now();while(!await js(s)){if(Date.now()-start>30000)throw Error(label+' timed out '+stderr+' '+JSON.stringify(await js('({reply:window.frame?.reply,plan:window.journal?.world?.plan,commands:window.commands,buttons:[...document.querySelectorAll("[data-nest-choice]")].map(b=>[b.textContent,b.disabled])})')));await new Promise(r=>setTimeout(r,30));}checks.push(label);};
  const send=c=>child.stdin.write(JSON.stringify(c)+'\n');
  await w.loadFile(path.join(__dirname,'tests/physical-objects-theatre.html'));await until('Boolean(window.journal)','notebook initialized');
  ipcMain.on('physical-command',(_,raw)=>{const command=pondCommand(raw);if(command)send(command);});
  child=spawn(path.join(__dirname,'../.venv/bin/python'),[path.join(__dirname,'check_nest_company.py'),'--serve'],{cwd:path.dirname(__dirname),stdio:['pipe','pipe','pipe']});
  child.stderr.on('data',b=>stderr=(stderr+b).slice(-5000));
  createInterface({input:child.stdout}).on('line',line=>{try{const m=JSON.parse(line);if(m.type==='physical_frame')js('window.receive('+JSON.stringify(m.frame)+')');}catch{}});
  await until('Boolean(window.frame)','actual native nests arrive');
  await until('window.hitCopies()','both nests have separate click bounds');
  await until("journal.body.querySelectorAll('[data-nest-choice]').length===7",'seven reachable nest actions appear');
  await js("window.selected=frame.copies[0];window.twin=frame.copies[1];button('Tuck the left edge').click()");
  await until("journal.world.plan?.instance===selected&&journal.world.plan.residence.requested==='tuck_left_edge'",'selected nest and exact requested action survive desktop IPC');
  await until("[...journal.body.querySelectorAll('[data-nest-choice]')].every(b=>b.disabled)",'controls disable during the active visit');
  send({type:'test_advance',until:'waiting'});
  await until("journal.world.plan?.label.startsWith('Waiting at the nest for ')&&journal.world.plan.residence.routine.elapsed===0",'waiting status describes the real approaching helper');
  await js('window.before=structuredClone(journal.world.instances[twin]);window.leftBefore=journal.world.instances[selected].nest.left');
  send({type:'test_advance',until:'contact'});
  await until("journal.world.instances[selected].nest.left>leftBefore",'physical tuck changes only after real contact');
  await until("JSON.stringify(journal.world.instances[twin])===JSON.stringify(before)",'the second nest remains untouched');
  await js("journal.command('cancel')");
  await until("!journal.world.plan&&!journal.world.minds.nest_helpers.length&&!button('Tuck the left edge').disabled&&journal.world.instances[selected].uses===0",'cancel releases the helper and restores controls without a completed visit');
  await js("button('Weave the rim').click()");await until("journal.world.plan?.residence.requested==='weave_rim'",'another chosen action can follow a cancellation');
  send({type:'test_advance',until:'finish'});
  await until("!journal.world.plan&&journal.world.instances[selected].uses===1&&journal.world.instances[selected].routines.weave_rim===1",'one finished weave records one original rest visit');
  for(const item of ['cozy_nest','deluxe_nest','nest_premium','golden_nest']){
   send({type:'test_fixture',item});await until('frame.item==='+JSON.stringify(item),item+' fixture arrives');
   await js("journal.show('belongings',frame.item,frame.copies[1]);window.selected=frame.copies[1];button('Fluff the lining').click()");
   await until("journal.world.plan?.instance===selected&&journal.world.plan.residence.requested==='fluff_center'",item+' uses its second physical copy');
   await js("journal.command('cancel')");await until('!journal.world.plan',item+' cancels normally');
  }
  send({type:'test_store',instance:await js('selected')});await until('!frame.copies.includes(selected)','stored copy leaves the world');
  await js("journal.show('belongings',frame.item,selected)");
  await until("[...journal.body.querySelectorAll('[data-nest-choice]')].every(b=>b.disabled)",'stored nest actions stay disabled');
  await js("journal.command('nest_action',frame.item,{instance:selected,text:'fluff_center'})");
  await until("!journal.world.plan&&frame.reply?.includes('Place that nest')",'native command also refuses an unplaced copy');
  await js('new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))');
  fs.writeFileSync(path.join(out,'nest-notebook.png'),(await w.webContents.capturePage()).toPNG());
  const result={result:'PASS',checks,commands:await js('window.commands')};fs.writeFileSync(path.join(out,'nest-ui.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));
  child.stdin.end('{"type":"quit"}\n');
  await new Promise((resolve,reject)=>{child.once('exit',code=>code===0?resolve():reject(Error('Native exit '+code+' '+stderr)));setTimeout(()=>reject(Error('Shutdown timed out')),5000).unref();});app.exit(0);
 }catch(e){console.error(e);if(child)child.stdin.end('{"type":"quit"}\n');app.exit(1);}
});
