const { app, BrowserWindow, Menu, ipcMain } = require('electron');
const { spawn } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');
const readline = require('node:readline');
const os = require('node:os');
const SMOKE = process.argv.includes('--smoke');
const root = path.resolve(__dirname, '..');
const runtime = SMOKE ? fs.mkdtempSync(path.join(os.tmpdir(), 'cheese-ascii-smoke-')) :
  (app.isPackaged ? path.join(app.getPath('appData'), 'Cheese the Duck ASCII Engine') : path.join(__dirname, '.runtime'));
app.setPath('userData', path.join(runtime, 'window'));
app.setName('Cheese the Duck ASCII Engine');
let simulationExit = null;
let win, child, closing = false, latest, queued, awaitingFrame = false, errorTail = '', closeTimer;
const send = (channel, data) => { if (win && !win.isDestroyed()) win.webContents.send(channel, data); };
function input(command) {
  if (child && child.stdin.writable) child.stdin.write(JSON.stringify(command) + '\n');
}
function deliver(frame) {
  latest = frame;
  if (awaitingFrame) { queued = frame; return; }
  awaitingFrame = true; send('engine:frame', frame);
}
function start() {
  simulationExit = null; errorTail = '';
  fs.mkdirSync(runtime, { recursive: true });
  const saveDir = path.join(runtime, 'saves');
  // Copy once; the installed game's saves are never opened for writing.
  if (!SMOKE && !fs.existsSync(saveDir)) {
    const legacy = path.join(os.homedir(), '.cheese_the_duck');
    if (fs.existsSync(legacy)) fs.cpSync(legacy, saveDir, { recursive: true });
  }
  fs.mkdirSync(saveDir, { recursive: true });
  const executable = app.isPackaged ? path.join(process.resourcesPath, 'simulation', 'cheese-simulation') : path.join(root, '.venv', 'bin', 'python');
  const args = app.isPackaged ? [] : ['-u', path.join(__dirname, 'host.py')];
  const env = { ...process.env, CHEESE_SAVE_DIR: saveDir, PYTHONDONTWRITEBYTECODE: '1',
    PYTHONUNBUFFERED: '1', PYGAME_HIDE_SUPPORT_PROMPT: '1', TERM: 'xterm-256color' };
  if (SMOKE && process.env.CHEESE_SMOKE_AUDIO !== 'system') env.SDL_AUDIODRIVER = 'dummy';
  child = spawn(executable, args, { cwd: runtime, env, stdio: ['pipe', 'pipe', 'pipe'] });
  const log = fs.createWriteStream(path.join(runtime, 'engine.log'), { flags: 'a' });
  child.stderr.on('data', d => { log.write(d); errorTail = (errorTail + d).slice(-6000); });
  child.stdin.on('error', () => {});
  child.on('error', err => send('engine:error', `Cannot start Cheese: ${err.message}. See engine/README.md for setup.`));
  readline.createInterface({ input: child.stdout }).on('line', line => {
    try {
      const message = JSON.parse(line);
      if (message.type === 'frame') deliver(message);
      else if (message.type === 'error') send('engine:error', message.message);
    } catch (err) { send('engine:error', `Invalid simulation frame: ${err.message}`); }
  });
  child.on('exit', (code, signal) => {
    simulationExit = { code, signal };
    child = null; log.end();
    if (SMOKE) return;
    if (closing && code === 0 && !signal) { clearTimeout(closeTimer); win.destroy(); app.quit(); }
    else if (code !== 0 || signal) { closing = false; clearTimeout(closeTimer); send('engine:error', `Cheese stopped (${signal || code}). ${errorTail}`); }
    else { closing = true; win.close(); }
  });
}
function shutdown() {
  if (closing) return;
  closing = true;
  if (!child) { win.destroy(); app.quit(); return; }
  input({ type: 'shutdown' });
  closeTimer = setTimeout(() => {
    closing = false;
    send('engine:error', 'Saving is taking longer than expected. The window is staying open; see engine.log for details.');
  }, 15000);
}
ipcMain.on('engine:ready', () => {
  // A reload discards in-flight ACKs. Seed the new renderer with the latest
  // frame and reset backpressure instead of waiting on the old page forever.
  awaitingFrame = false; queued = null;
  if (!child) start();
  else if (latest) deliver(latest);
});
ipcMain.on('engine:ack', () => { awaitingFrame = false; if (queued) { const frame = queued; queued = null; deliver(frame); } });
ipcMain.on('engine:input', (_e, command) => {
  if (!command || closing) return;
  if (command.type === 'action' && typeof command.action === 'string' && command.action.length < 32) input(command);
  if (command.type === 'key' && typeof command.key === 'string' && command.key.length < 32) input(command);
  if (command.type === 'text' && typeof command.text === 'string') input({ type: 'text', text: command.text.slice(0, 1000) });
  if (command.type === 'choose' && ['title','menu'].includes(command.target) && typeof command.context === 'string' && command.context.length < 8192) input(command);
});
ipcMain.handle('engine:fullscreen', () => { win.setFullScreen(!win.isFullScreen()); });
ipcMain.handle('engine:capture', async () => {
  const dir = path.join(runtime, 'screenshots'); fs.mkdirSync(dir, { recursive: true });
  const file = path.join(dir, `cheese-${Date.now()}.png`);
  fs.writeFileSync(file, (await win.webContents.capturePage()).toPNG()); return file;
});
const pause = ms => new Promise(resolve => setTimeout(resolve, ms));
async function waitFor(predicate, label, ms = 30000) {
  const deadline = Date.now() + ms;
  while (Date.now() < deadline) { if (predicate()) return; await pause(100); }
  throw new Error(`Timed out: ${label}\n${errorTail}`);
}
async function smoke() {
  const out = process.env.CHEESE_ARTIFACTS || path.join(__dirname, 'artifacts'); fs.mkdirSync(out, { recursive: true });
  await waitFor(() => latest?.meta.state === 'title', 'title screen'); await pause(300);
  fs.writeFileSync(path.join(out, 'title.png'), (await win.webContents.capturePage()).toPNG());
  const clickChoice = async (target,id=null) => win.webContents.executeJavaScript(`(() => {
    const hit=window.interfaceTargets?.find(h=>h.command.target===${JSON.stringify(target)} && (${JSON.stringify(id)}===null || h.command.id===${JSON.stringify(id)}));
    if(!hit)throw new Error('Missing clickable menu choice');
    const canvas=document.getElementById('world'),r=canvas.getBoundingClientRect(),s=window.engineStats;
    canvas.dispatchEvent(new MouseEvent('click',{bubbles:true,clientX:r.left+(hit.x+hit.w/2)/(s.cols*10)*r.width,clientY:r.top+(hit.y+hit.h/2)/(s.rows*18)*r.height}));
  })()`);
  await clickChoice('title');
  await waitFor(() => latest?.meta.state === 'playing', 'new game'); await pause(4200);
  input({ type: 'key', key: 'Escape' }); await pause(300);
  fs.writeFileSync(path.join(out, 'pond.png'), (await win.webContents.capturePage()).toPNG());
  await clickChoice('menu','care');
  await waitFor(()=>latest?.ui?.menu.depth===1,'mouse opens care submenu');
  input({type:'key',key:'Escape'});
  await waitFor(()=>latest?.ui?.menu.depth===0,'keyboard returns from care submenu');
  await win.webContents.executeJavaScript("document.getElementById('graphics').click()");
  await pause(300);
  fs.writeFileSync(path.join(out, 'classic.png'), (await win.webContents.capturePage()).toPNG());
  if (await win.webContents.executeJavaScript("localStorage.getItem('cheese.graphics')") !== 'classic') throw new Error('Classic preference was not saved');
  await new Promise(resolve => { win.webContents.once('did-finish-load', resolve); win.webContents.reload(); });
  await win.webContents.executeJavaScript(`new Promise((resolve, reject) => {
    const deadline = Date.now() + 5000;
    const poll = () => { if (window.engineStats?.frames > 0) resolve();
      else if (Date.now() > deadline) reject(new Error('Renderer did not resume after reload'));
      else setTimeout(poll, 50); }; poll();
  })`);
  if (await win.webContents.executeJavaScript("window.engineStats?.mode") !== 'classic') throw new Error('Classic preference did not survive reload');
  await win.webContents.executeJavaScript("document.getElementById('graphics').click()");
  await pause(300);
  // Exercise the actual DOM toolbar -> preload -> IPC -> simulation path.
  for (const index of [11, 12, 7, 12, 5]) {
    await win.webContents.executeJavaScript(`document.querySelectorAll('#actions button')[${index}].click()`);
    await pause(300);
  }
  await waitFor(() => latest?.meta.talking, 'talk toolbar action');
  input({ type: 'text', text: 'What the hell, Cheese?' }); await pause(500);
  await waitFor(() => latest?.lines.some(row => row.some(run => run[0].includes('What the hell, Cheese?'))), 'literal dialogue input');
  fs.writeFileSync(path.join(out, 'talk.png'), (await win.webContents.capturePage()).toPNG());
  fs.writeFileSync(path.join(out, 'talk-frame.json'), JSON.stringify(latest));
  input({ type: 'key', key: 'Enter' }); await pause(800);
  fs.writeFileSync(path.join(out, 'frame.json'), JSON.stringify(latest));
  const stats = await win.webContents.executeJavaScript('window.engineStats');
  if (!stats || stats.frames < 10) throw new Error('Canvas did not draw enough frames');
  input({ type: 'shutdown' }); await waitFor(() => !child, 'graceful shutdown');
  if (simulationExit?.code !== 0 || simulationExit?.signal) throw new Error(`Simulation shutdown failed: ${JSON.stringify(simulationExit)}\n${errorTail}`);
  JSON.parse(fs.readFileSync(path.join(runtime, 'saves', 'save.json'), 'utf8'));
  console.log(JSON.stringify({ result: 'PASS', stats, runtime, out }));
}
app.whenReady().then(async () => {
  win = new BrowserWindow({ title: 'Cheese the Duck - ASCII Engine', width: 1500, height: 1020,
    minWidth: 920, minHeight: 640, backgroundColor: '#101b19',
    webPreferences: { preload: path.join(__dirname, 'preload.cjs'), contextIsolation: true, sandbox: true } });
  if (SMOKE) win.webContents.on('console-message', ({ level, message, lineNumber, sourceId }) =>
    console.error('Renderer console:', JSON.stringify({ level, message, lineNumber, sourceId })));
  Menu.setApplicationMenu(Menu.buildFromTemplate([{ role: 'appMenu' }, { role: 'editMenu' }, { label: 'View', submenu: [{ role: 'togglefullscreen' }] }]));
  win.on('close', event => { if (child) { event.preventDefault(); shutdown(); } });
  await win.loadFile(path.join(__dirname, 'client', 'index.html'));
  if (SMOKE) {
    try { await smoke(); } catch (err) {
      console.error(err);
      console.error(JSON.stringify({runtime, focused:win.isFocused(), visible:win.isVisible(), awaitingFrame, queued:queued?.seq, latest:latest?.seq}));
      console.error(await win.webContents.executeJavaScript("JSON.stringify({visibility:document.visibilityState,readyState:document.readyState,mode:document.getElementById('graphics')?.textContent,error:document.getElementById('error')?.textContent,stats:window.engineStats})").catch(String));
      process.exitCode = 1;
    }
    if (child) { input({ type: 'shutdown' }); await waitFor(() => !child, 'shutdown after failure').catch(() => child?.kill()); }
    app.exit(process.exitCode || 0);
  }
});
app.on('before-quit', event => { if (child) { event.preventDefault(); shutdown(); } });
app.on('window-all-closed', () => app.quit());
