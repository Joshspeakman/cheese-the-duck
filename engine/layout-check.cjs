const {app,BrowserWindow,ipcMain}=require('electron');
const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),{spawn}=require('node:child_process'),{createInterface}=require('node:readline');
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-layout-ui-')));
app.whenReady().then(async()=>{
 let child,w,latest,stderr='',failure;
 const checks=[],out=path.join(__dirname,'artifacts/animation-milestone');
 try{
  w=new BrowserWindow({show:false,width:1440,height:1000,webPreferences:{nodeIntegration:true,contextIsolation:false,backgroundThrottling:false}});
  w.webContents.on('console-message',d=>{if(d.level==='error')console.error(d.message);});
  const js=source=>w.webContents.executeJavaScript(source);
  const until=async(source,label)=>{const start=Date.now();while(!await js(source)){if(Date.now()-start>12000)throw Error(label+' timed out '+stderr.slice(-500));await new Promise(r=>setTimeout(r,30));}checks.push(label);};
  await w.loadFile(path.join(__dirname,'tests/layout-theatre.html'));
  await until('Boolean(window.journal)','notebook initializes');
  ipcMain.on('layout-command',(_,command)=>child.stdin.write(JSON.stringify(command)+'\n'));
  child=spawn(path.join(__dirname,'../.venv/bin/python'),[path.join(__dirname,'check_layout.py'),'--serve'],{cwd:path.dirname(__dirname),stdio:['pipe','pipe','pipe']});
  child.stderr.on('data',b=>{stderr=(stderr+b).slice(-5000);});
  child.on('error',e=>{failure=e;});
  const lines=createInterface({input:child.stdout});
  lines.on('line',line=>{try{const msg=JSON.parse(line);if(msg.type==='layout_frame'){latest=msg.frame;js('window.receive('+JSON.stringify(latest)+')').catch(e=>{failure=e;});}}catch{}});
  await until('Boolean(window.journal.frame)','real simulation frame arrives');
  if(failure)throw failure;
  const cases=fs.readFileSync(path.join(out,'layout-cases.json'),'utf8');
  if(!await js('window.compareCases('+cases+')'))throw Error('Client/native placement rules disagree');
  checks.push('480 native placement decisions agree with preview');
  const grounds=fs.readFileSync(path.join(out,'grounds-cases.json'),'utf8');
  if(!await js('window.compareCases('+grounds+')'))throw Error('Garden/building native placement rules disagree with preview');
  checks.push('garden, project, building and decoration placement decisions agree with preview');
  await js("window.journal.arrangement.canvas.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowLeft',bubbles:true}))");
  if(await js('window.commands.length')!==0)throw Error('Preview wrote to the simulation');
  checks.push('keyboard draft leaves actual habitat unchanged');
  await js("window.journal.arrangement.canvas.scrollIntoView({block:'center'});new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))");
  const point=await js("(()=>{const a=window.journal.arrangement,r=a.canvas.getBoundingClientRect();return {x:Math.round(r.left+r.width*.55),y:Math.round(r.top+r.height*.6)}})()");
  const beforePointer=await js('JSON.stringify(window.journal.arrangement.draft)');
  await w.webContents.sendInputEvent({type:'mouseDown',button:'left',clickCount:1,...point});
  await w.webContents.sendInputEvent({type:'mouseUp',button:'left',clickCount:1,...point});
  await js('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))');
  if(await js('window.commands.length')!==0||await js('JSON.stringify(window.journal.arrangement.draft)')===beforePointer){
   const debug=await js('(()=>{const e=document.elementFromPoint('+point.x+','+point.y+');return {hit:e?.tagName,cls:e?.className,after:window.journal.arrangement.draft,viewport:[innerWidth,innerHeight],rect:window.journal.arrangement.canvas.getBoundingClientRect().toJSON(),commands:window.commands.length}})()');
   throw Error('Mouse must move the draft without changing actual placement '+JSON.stringify({beforePointer,point,...debug}));
  }
  checks.push('real mouse positioning edits only the draft');
  await js('window.journal.arrangement.store.click()');
  await until("!window.journal.arrangement.pending && !window.journal.world.layout.placed.some(p=>p.id==='couch')",'storage reaches actual simulation and acknowledges');
  await js('window.journal.arrangement.auto.click()');
  await until("!window.journal.arrangement.pending && window.journal.world.layout.placed.some(p=>p.id==='couch')",'automatic placement reaches actual simulation');
  // A colliding draft is rejected before sending. Native rejection is covered separately.
  await js("window.journal.arrangement.select('toy_ball');window.journal.arrangement.draft={x:window.journal.world.layout.placed.find(p=>p.id==='couch').x,y:window.journal.world.layout.placed.find(p=>p.id==='couch').y};window.journal.arrangement.update()");
  if(!await js('window.journal.arrangement.place.disabled'))throw Error('Collision draft can be placed');
  checks.push('overlapping draft explains failure and disables placement');
  await js("window.journal.arrangement.select('toy_ball');window.journal.arrangement.update();window.journal.arrangement.place.click()");
  await until('!window.journal.arrangement.pending','explicit coordinates acknowledged by simulation');
  // A renderer refresh cannot throw away the selected draft.
  const draft=await js('JSON.stringify(window.journal.arrangement.draft)');
  await js('window.journal.update(window.journal.frame);window.journal.updateDynamic()');
  if(await js('JSON.stringify(window.journal.arrangement.draft)')!==draft)throw Error('Live frame erased the draft');
  checks.push('live updates preserve draft and focus');
  const geometry=await js('(()=>{try{return window.geometryCheck()}catch(e){return {error:e.stack}}})()');
  if(geometry.error)throw Error(geometry.error);
  checks.push('actual item hit bounds fit reservations at wide, normal and tall aspect ratios');
  await js("window.journal.arrangement.select('couch');window.journal.arrangement.update();window.journal.arrangement.lastPaint=-Infinity;window.journal.paint(performance.now()/1000)");
  await new Promise(r=>setTimeout(r,150));
  fs.writeFileSync(path.join(out,'layout-notebook.png'),(await w.webContents.capturePage()).toPNG());
  const result={result:'PASS',checks,geometry,commands:await js('window.commands'),nativeChecks:JSON.parse(fs.readFileSync(path.join(out,'layout-simulation.json'),'utf8')).checks};
  fs.writeFileSync(path.join(out,'layout-render.json'),JSON.stringify(result,null,2));
  console.log(JSON.stringify(result));
  child.stdin.end('{"type":"quit"}\n');
  await new Promise((resolve,reject)=>{child.once('exit',code=>code===0?resolve():reject(Error('Native shutdown '+code+' '+stderr)));setTimeout(()=>reject(Error('Native shutdown timed out')),5000).unref();});
  app.exit(0);
 }catch(e){console.error(e);if(child)child.kill('SIGTERM');app.exit(1);}
});
