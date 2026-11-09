// Cheese the Duck on the desktop. The game is a terminal program: this runs it in a real terminal inside the window, with its
// own Python environment (made on first launch in the app's data folder). Saves stay where the game keeps them, ~/.cheese_the_duck.
const { app, BrowserWindow, Menu, ipcMain } = require('electron');
const { spawn, execFileSync } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const pty = require('node-pty');

const GAME_DIR = app.isPackaged ? path.join(process.resourcesPath, 'game') : path.join(__dirname, 'game');
const SMOKE = process.argv.includes('--smoke');
let win = null, game = null, settingsCache = null, setupRunning = null;

const settingsPath = () => path.join(app.getPath('userData'), 'settings.json');
function settings() {
  if (settingsCache) return settingsCache;
  try { settingsCache = JSON.parse(fs.readFileSync(settingsPath(), 'utf8')); } catch { settingsCache = {}; }
  return settingsCache;
}
function saveSettings(change) { Object.assign(settings(), change); fs.writeFileSync(settingsPath(), JSON.stringify(settingsCache, null, 2)); }
const venvDir = () => path.join(app.getPath('userData'), 'python');
const venvPython = () => path.join(venvDir(), 'bin/python');
const stampPath = () => path.join(venvDir(), '.requirements');
const send = (ch, v) => { if (win && !win.isDestroyed()) win.webContents.send(ch, v); };

function findPython() {
  for (const p of ['/opt/homebrew/bin/python3', '/usr/local/bin/python3', '/usr/bin/python3']) {
    if (!fs.existsSync(p)) continue;
    try { const v = execFileSync(p, ['-c', 'import sys; print(sys.version_info[0]*100+sys.version_info[1])'], { stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim(); if (Number(v) >= 309) return p; } catch { /* the macOS stub without developer tools */ }
  }
  return null;
}
function run(cmd, args, label) {
  return new Promise((resolve, reject) => {
    send('cheese:setup', label);
    const p = spawn(cmd, args, { stdio: ['ignore', 'pipe', 'pipe'] });
    let tail = '';
    const take = (d) => { tail = (tail + d).slice(-1200); };
    p.stdout.on('data', take); p.stderr.on('data', take);
    p.on('error', reject);
    p.on('close', (code) => (code === 0 ? resolve() : reject(new Error(tail || `${label} failed`))));
  });
}
/** The Python environment for this version of the game's requirements: made once, and again if they change. */
function ensurePython() {
  if (setupRunning) return setupRunning;
  setupRunning = (async () => {
    const wanted = fs.readFileSync(path.join(GAME_DIR, 'requirements.txt'), 'utf8');
    if (fs.existsSync(venvPython()) && fs.existsSync(stampPath()) && fs.readFileSync(stampPath(), 'utf8') === wanted) return;
    const python = findPython();
    if (!python) throw new Error('Cheese needs Python 3.9 or newer. Install it with: xcode-select --install');
    fs.rmSync(venvDir(), { recursive: true, force: true });
    await run(python, ['-m', 'venv', venvDir()], 'Building Cheese a pond (first launch only)...');
    await run(venvPython(), ['-m', 'pip', 'install', '--disable-pip-version-check', '-q', '-r', path.join(GAME_DIR, 'requirements.txt')], 'Fetching bread and sound effects...');
    fs.writeFileSync(stampPath(), wanted);
  })().finally(() => { setupRunning = null; });
  return setupRunning;
}
function stopGame() { if (game) { const g = game; game = null; try { g.kill(); } catch { /* already gone */ } } }
async function play(cols, rows) {
  stopGame();
  await ensurePython();
  const env = { ...process.env, TERM: 'xterm-256color', COLORTERM: 'truecolor', LANG: process.env.LANG || 'en_US.UTF-8', PYTHONDONTWRITEBYTECODE: '1', PYGAME_HIDE_SUPPORT_PROMPT: '1' };
  const p = pty.spawn(venvPython(), [path.join(GAME_DIR, 'main.py')], { name: 'xterm-256color', cols, rows, cwd: app.getPath('userData'), env });
  game = p;
  p.onData((d) => { if (game === p) send('cheese:output', d); });
  p.onExit(({ exitCode }) => { if (game === p) { game = null; send('cheese:exit', exitCode); } });
  return true;
}
function ipc() {
  ipcMain.handle('cheese:info', () => ({ version: app.getVersion(), fullscreen: !!settings().fullscreen }));
  ipcMain.handle('cheese:play', async (_e, c, r) => { try { await play(c, r); return {}; } catch (err) { return { error: String(err.message || err) }; } });
  ipcMain.on('cheese:input', (_e, d) => { if (game) game.write(d); });
  ipcMain.on('cheese:resize', (_e, c, r) => { if (game && c > 0 && r > 0) game.resize(c, r); });
  ipcMain.handle('cheese:stop', () => stopGame());
  ipcMain.handle('cheese:fullscreen', (_e, on) => { saveSettings({ fullscreen: !!on }); win.setFullScreen(!!on); return !!on; });
  ipcMain.handle('cheese:quit', () => app.quit());
}
function createWindow() {
  win = new BrowserWindow({ width: 1180, height: 780, minWidth: 900, minHeight: 620, backgroundColor: '#14120c', fullscreen: !!settings().fullscreen, title: 'Cheese the Duck',
    webPreferences: { preload: path.join(__dirname, 'preload.js'), contextIsolation: true, sandbox: false } });
  win.loadFile(path.join(__dirname, 'launcher.html'));
  win.on('closed', () => { win = null; });
}
async function smoke() {
  const dir = process.env.SMOKE_OUT || os.tmpdir();
  await new Promise((r) => win.webContents.once('did-finish-load', r));
  await new Promise((r) => setTimeout(r, 700));
  fs.writeFileSync(path.join(dir, 'launcher.png'), (await win.webContents.capturePage()).toPNG());
  await win.webContents.executeJavaScript("document.getElementById('play').click()");
  const deadline = Date.now() + 240000;
  const failed = () => win.webContents.executeJavaScript("document.getElementById('msg').className==='err'");
  while (!game && Date.now() < deadline && !(await failed())) await new Promise((r) => setTimeout(r, 300));
  if (!game) throw new Error(`the game did not start: ${await win.webContents.executeJavaScript("document.getElementById('msg').textContent")}`);
  await new Promise((r) => setTimeout(r, 9000));
  fs.writeFileSync(path.join(dir, 'game.png'), (await win.webContents.capturePage()).toPNG());
  if (!game) throw new Error('the game exited right after starting');
  console.log('smoke: ok, the game is running in the window');
  stopGame();
}
app.setName('Cheese the Duck');
app.whenReady().then(async () => {
  ipc();
  Menu.setApplicationMenu(Menu.buildFromTemplate([{ role: 'appMenu' }, { role: 'editMenu' }, { label: 'View', submenu: [{ role: 'togglefullscreen' }] }]));
  createWindow();
  if (SMOKE) { try { await smoke(); } catch (e) { console.error('smoke: FAILED', e); process.exitCode = 1; } app.quit(); }
});
app.on('before-quit', stopGame);
app.on('window-all-closed', () => app.quit());
