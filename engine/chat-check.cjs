// Real renderer/input events, isolated preferences, deterministic host acknowledgments.
const {app,BrowserWindow,ipcMain}=require('electron');
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const out=path.join(__dirname,'artifacts/chat');fs.mkdirSync(out,{recursive:true});
app.setPath('userData',fs.mkdtempSync(path.join(os.tmpdir(),'cheese-chat-ui-')));
let frame=JSON.parse(fs.readFileSync(path.join(__dirname,'artifacts/interface-frames.json'))).pond;
frame.ui.modal=null;frame.meta.talking=false;
frame.ui.chatStream={session:'test-pond',entries:[],receipts:[],targets:[{id:'cheese',name:'Cheese'},{id:'moss',name:'Moss'}],pending:null};
const stream=frame.ui.chatStream;let sequence=0;
function row(text,channel='say',speaker='cheese',name='Cheese',target='player'){stream.entries.push({id:++sequence,text,channel,speaker,name,target,time:'12:05'});stream.entries=stream.entries.slice(-240);}
row('The light is catching the reeds.','world','','');row('Morning, Cheese. How is pond life treating you?','say','player','You','cheese');
row('*surveys his kingdom* Damp. Full of freeloaders. Honestly? Pretty fucking great.');
row('I found the quiet corner you told me about. Saved you a spot.','whisper','moss','Moss');
const inputs=[],errors=[],checks=[];let win;
ipcMain.on('hud-test:ready',()=>win.webContents.send('hud-test:frame',frame));ipcMain.on('hud-test:input',(_e,c)=>inputs.push(c));
const pause=ms=>new Promise(r=>setTimeout(r,ms)),js=s=>win.webContents.executeJavaScript(s);
const check=(x,label)=>{if(!x)throw Error(label);checks.push(label);};
async function publish(){win.webContents.send('hud-test:frame',frame);await pause(140);}
async function key(keyCode,modifiers=[]){win.webContents.sendInputEvent({type:'keyDown',keyCode,modifiers});win.webContents.sendInputEvent({type:'keyUp',keyCode,modifiers});await pause(70);}
async function text(value){await js(`document.getElementById('pond-chat-input').value=${JSON.stringify(value)}`);}
async function drag(selector,dx,dy){const p=await js(`(()=>{const r=document.querySelector(${JSON.stringify(selector)}).getBoundingClientRect();return {x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2)}})()`);win.webContents.sendInputEvent({type:'mouseMove',...p});win.webContents.sendInputEvent({type:'mouseDown',button:'left',clickCount:1,...p});await pause(50);win.webContents.sendInputEvent({type:'mouseMove',modifiers:['leftButtonDown'],x:p.x+dx,y:p.y+dy});await pause(70);win.webContents.sendInputEvent({type:'mouseUp',button:'left',clickCount:1,x:p.x+dx,y:p.y+dy});await pause(100);}
app.whenReady().then(async()=>{
 win=new BrowserWindow({show:true,width:1440,height:1000,webPreferences:{preload:path.join(__dirname,'tests/hud-preload.cjs'),contextIsolation:true,sandbox:true,backgroundThrottling:false}});
 win.webContents.on('console-message',d=>{if(d.level==='error')errors.push(d.message);});
 try{
 await win.loadFile(path.join(__dirname,'client/index.html'));await pause(650);
 check(await js("!document.getElementById('pond-chat').hidden&&document.querySelectorAll('.chat-line').length===4"),'existing bottom-left log becomes readable structured chat');
 const before=inputs.length;await key('Enter');check(await js("document.activeElement.id==='pond-chat-input'"),'Enter focuses inline chat');
 for(const k of ['F','B','T','J'])await key(k);
 check(inputs.length===before,'typing action hotkeys never reaches gameplay');
 await text('What the fuck, Cheese?');await js("document.getElementById('pond-chat-input').dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',isComposing:true,bubbles:true,cancelable:true}))");
 check(inputs.length===before,'IME composition does not submit');
 await key('Escape');check(await js("document.activeElement.id==='world'&&document.getElementById('pond-chat-input').value==='What the fuck, Cheese?'"),'Escape returns to world and preserves draft');
 await key('Enter');await key('Enter');
 const request=inputs.at(-1);check(request?.type==='chat'&&request.text==='What the fuck, Cheese?'&&request.session===stream.session&&request.target==='cheese','Enter submits natural uncensored dialogue through IPC');
 row(request.text,'say','player','You','cheese');stream.receipts.push({id:request.id,accepted:true});stream.pending='Cheese';await publish();
 check(await js("document.getElementById('pond-chat-input').value===''&&!window.pondChat.active&&document.querySelector('.chat-status').textContent.includes('Cheese')"),'host acknowledgment clears only accepted draft and shows thinking');
 await key('Enter');await key('Up');check(await js("document.getElementById('pond-chat-input').value==='What the fuck, Cheese?'"),'Up recalls sent message');await key('Down');
 await text('A second thought');await key('Enter');check(inputs.at(-1)===request,'busy reply preserves next draft instead of losing it');
 stream.pending=null;stream.voice={source:'authored',detail:'test transport'};row('A magnificent question. The pond remains suspicious.');await publish();
 await key('Enter');const rejected=inputs.at(-1);stream.receipts.push({id:rejected.id,accepted:false,message:'Give them a moment to answer.'});await publish();
 check(await js("document.getElementById('pond-chat-input').value==='A second thought'&&!document.getElementById('pond-chat-input').readOnly"),'rejected message stays editable');await publish();check(await js("document.querySelector('.chat-status').textContent==='Give them a moment to answer.'"),'rejection explanation survives live refresh');
 await text('/w Moss That sounds lovely.');await key('Enter');const whisper=inputs.at(-1);check(whisper.target==='moss'&&whisper.channel==='whisper','whisper addresses independent visitor brain');
 stream.receipts.push({id:whisper.id,accepted:true});row(whisper.text,'whisper','player','You','moss');await publish();
 await key('Enter');await text('/r Save me a seat.');await key('Enter');check(inputs.at(-1).target==='moss','reply resolves last incoming whisper');
 stream.receipts.push({id:inputs.at(-1).id,accepted:true});await publish();
 await js("document.querySelector('[data-chat-tab=world]').click()");check(await js("[...document.querySelectorAll('.chat-line')].every(n=>n.dataset.channel==='world')"),'World tab filters speech');
 await js("document.querySelector('[data-chat-tab=conversation]').click()");check(await js("[...document.querySelectorAll('.chat-line')].every(n=>n.dataset.channel!=='world')"),'Conversations tab filters events');
 await js("document.querySelector('[data-chat-tab=general]').click()");
 for(let i=0;i<90;i++)row('A remembered pond conversation number '+i+'. '+('The reeds rustle softly. ').repeat(2));await publish();
 await js('window.pondChat.log.scrollTop=0');await pause(100);const top=await js('window.pondChat.log.scrollTop');row('A new arrival while you read.');await publish();
 check(await js(`Math.abs(window.pondChat.log.scrollTop-${top})<2&&!document.querySelector('.chat-latest').hidden`),'incoming lines preserve scrollback and show unread indicator');
 await js("document.querySelector('.chat-latest').click()");check(await js('window.pondChat.follow'),'Latest returns to live conversation');
 row('<img src=x onerror=alert(1)> Fuck yes.');await publish();check(await js("!document.querySelector('#pond-chat img')&&document.querySelector('.chat-scroll').textContent.includes('<img')"),'model text is literal and never interpreted as HTML');
 await js("document.querySelectorAll('button.chat-speaker')[0].click()");check(await js("window.pondChat.channel==='whisper'&&window.pondChat.active"),'speaker names open a whisper');await key('Escape');
 const bounds=await js("document.getElementById('pond-chat').getBoundingClientRect().toJSON()");await drag('.chat-grip',90,-60);const moved=await js("document.getElementById('pond-chat').getBoundingClientRect().toJSON()");check(moved.x>bounds.x+50&&moved.y<bounds.y-30,'chat moves independently with pointer drag');
 await drag('.chat-resize',90,-35);check(await js(`document.getElementById('pond-chat').getBoundingClientRect().width>${moved.width+50}`),'chat resizes and keeps anchor');
 await js("document.querySelector('.chat-close').click()");check(await js("document.getElementById('pond-chat').hidden"),'chat can close');await key('Enter');check(await js("!document.getElementById('pond-chat').hidden&&window.pondChat.active"),'Enter reopens closed chat');
 await js('window.pondHUD.fade.lastInput=performance.now()-65000');await pause(160);check(await js('window.pondHUD.fade.opacity===1'),'composing never fades while thinking about a message');await key('Escape');
 await js('window.pondHUD.fade.lastInput=performance.now()-65000');await pause(150);check(await js("window.pondHUD.fade.opacity===0&&getComputedStyle(document.getElementById('pond-chat')).opacity==='0'"),'chat fades with rest of HUD at idle');await js('window.pondHUD.wake()');
 for(const [width,height] of [[920,640],[1700,960],[1440,1000]]){win.setSize(width,height);await pause(220);check(await js("(()=>{const n=document.getElementById('pond-chat'),r=n.getBoundingClientRect();return r.left>=0&&r.right<=innerWidth&&r.bottom<=innerHeight&&n.scrollWidth<=n.clientWidth+2})()"),'chat stays inside '+width+'px window');}
 const saved=await js("JSON.stringify(window.pondHUD.layout.panels.chat)");await new Promise(r=>{win.webContents.once('did-finish-load',r);win.webContents.reload()});await pause(500);check(await js("JSON.stringify(window.pondHUD.layout.panels.chat)")===saved,'size and location persist across renderer reload');
 frame.ui.modal={title:'SHOP',lines:[]};await publish();check(await js("document.getElementById('pond-chat').hidden"),'game modal hides chat and retains original controls');frame.ui.modal=null;await publish();
 await js("document.getElementById('graphics').click()");await key('Enter');check(inputs.at(-1)?.type==='key'&&inputs.at(-1)?.key==='Enter','Classic keeps original keyboard behavior');await js("document.getElementById('graphics').click()");
 // A clean example for visual inspection, not the test's intentionally crowded history.
 stream.session='preview';stream.entries=[];sequence=0;row('The light is catching the reeds.','world','','');row('Morning, Cheese. How is pond life treating you?','say','player','You','cheese');row('*surveys his kingdom* Damp. Full of freeloaders. Honestly? Pretty fucking great.');row('I found that quiet corner. Saved you a spot.','whisper','moss','Moss');await publish();
 await js('window.pondHUD.layout.preset();window.pondHUD.changed();window.pondChat.open()');await text('What should we do today?');
 fs.writeFileSync(path.join(out,'in-world-chat.png'),(await win.webContents.capturePage()).toPNG());
 const rect=await js("(()=>{const r=document.getElementById('pond-chat').getBoundingClientRect();return {x:Math.floor(r.x),y:Math.floor(r.y),width:Math.ceil(r.width),height:Math.ceil(r.height)}})()");fs.writeFileSync(path.join(out,'chat-closeup.png'),(await win.webContents.capturePage(rect)).toPNG());
 check(!errors.length,'no renderer errors');fs.writeFileSync(path.join(out,'ui-checks.json'),JSON.stringify({result:'PASS',checks},null,2));console.log(JSON.stringify({result:'PASS',checks:checks.length}));app.exit(0);
 }catch(e){console.error(e,errors);fs.writeFileSync(path.join(out,'ui-failure.png'),(await win.webContents.capturePage()).toPNG());app.exit(1);}
});
