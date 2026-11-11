const {app,BrowserWindow,ipcMain}=require('electron'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const {spawn}=require('node:child_process'),{createInterface}=require('node:readline'),{pondCommand}=require('./pond-command.cjs');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-architecture-ui-')));
app.whenReady().then(async()=>{
 let child,stderr='';const checks=[],out=path.join(__dirname,'artifacts/animation-milestone');
 try{
  const w=new BrowserWindow({show:false,width:1440,height:1000,webPreferences:{nodeIntegration:true,contextIsolation:false,backgroundThrottling:false}});
  const js=s=>w.webContents.executeJavaScript(s),send=c=>child.stdin.write(JSON.stringify(c)+'\n');
  const until=async(s,label)=>{const start=Date.now();while(!await js(s)){if(Date.now()-start>15000)throw Error(label+' timed out '+stderr+' '+await js("JSON.stringify({selected:journal.selected,instance:journal.selectedInstance,plan:journal.world?.plan,summary:journal.body.querySelector('[data-architecture-summary]')?.textContent,weather:frame.scene.weather})"));await new Promise(r=>setTimeout(r,30));}checks.push(label);};
  await w.loadFile(path.join(__dirname,'tests/physical-objects-theatre.html'));
  await until('Boolean(window.journal)','notebook initialized');
  ipcMain.on('physical-command',(_,raw)=>{const c=pondCommand(raw);if(c)send(c);});
  child=spawn(path.join(__dirname,'../.venv/bin/python'),[path.join(__dirname,'check_architecture.py'),'--serve'],{cwd:path.dirname(__dirname),stdio:['pipe','pipe','pipe']});
  child.stderr.on('data',b=>stderr=(stderr+b).slice(-5000));
  createInterface({input:child.stdout}).on('line',line=>{try{const m=JSON.parse(line);if(m.type==='physical_frame')js('window.receive('+JSON.stringify(m.frame)+')');}catch{}});
  await until('Boolean(window.frame)','native gates arrive');
  await until('window.hitCopies()','two gates retain distinct clickable bounds');
  await js("button('Open gate').click()");
  await until("journal.world.plan?.instance===frame.copies[0]&&journal.world.instances[frame.copies[0]].architecture.open===0",'open command walks to the selected closed gate');
  send({type:'test_advance',until:'contact'});
  await until("journal.world.instances[frame.copies[0]].architecture.open>0&&journal.world.instances[frame.copies[0]].architecture.open<1",'latch contact starts real continuous movement');
  await until("journal.world.instances[frame.copies[1]].architecture.open===0",'other gate remains closed');
  await js("journal.command('cancel')");
  await until("!journal.world.plan&&journal.world.instances[frame.copies[0]].uses===0&&journal.body.querySelector('[data-architecture-summary]').textContent.includes('partway')",'cancel retains the partially opened gate without a reward');
  await js("button('Close gate').click()");
  await until("journal.world.plan?.architecture_work.id==='gate_close'",'close button acts on the same physical gate');
  send({type:'test_advance',until:'finish'});
  await until("!journal.world.plan&&journal.body.querySelector('[data-architecture-summary]').textContent.includes('closed')",'gate closes visibly in the notebook');
  for(const [item,label,field]of [['mailbox','Raise flag','flag'],['wishing_well','Lower bucket','bucket'],['windmill','Apply brake','brake']]){
   send({type:'test_fixture',item});await until("frame.item==='"+item+"'",item+' fixture arrives');
   await js("journal.show('belongings',frame.item,frame.copies[0]);button('"+label+"').click()");
   await until("journal.world.plan?.target==='"+item+"'",label+' reaches native simulation');
   send({type:'test_advance',until:'finish'});
   await until("!journal.world.plan&&journal.world.instances[frame.copies[0]].architecture."+field+"===1&&journal.world.instances[frame.copies[1]].architecture."+field+"===0",label+' updates only selected copy');
  }
  await js('new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))');
  fs.writeFileSync(path.join(out,'architecture-inspector.png'),(await w.webContents.capturePage()).toPNG());
  const result={result:'PASS',checks,commands:await js('window.commands')};fs.writeFileSync(path.join(out,'architecture-ui.json'),JSON.stringify(result,null,2));console.log(JSON.stringify({result:'PASS',checks:checks.length}));
  child.stdin.end('{"type":"quit"}\n');
  await new Promise((resolve,reject)=>{child.once('exit',code=>code===0?resolve():reject(Error('Native exit '+code+' '+stderr)));setTimeout(()=>reject(Error('Shutdown timed out')),5000).unref();});app.exit(0);
 }catch(e){console.error(e);if(child)child.stdin.end('{"type":"quit"}\n');app.exit(1);}
});
