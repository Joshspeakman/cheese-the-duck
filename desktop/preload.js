// The launcher page's way into the app: start the game and carry its terminal.
const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('cheese', {
  info: () => ipcRenderer.invoke('cheese:info'),
  play: (cols, rows) => ipcRenderer.invoke('cheese:play', cols, rows),
  input: (data) => ipcRenderer.send('cheese:input', data),
  resize: (cols, rows) => ipcRenderer.send('cheese:resize', cols, rows),
  stop: () => ipcRenderer.invoke('cheese:stop'),
  fullscreen: (on) => ipcRenderer.invoke('cheese:fullscreen', on),
  quit: () => ipcRenderer.invoke('cheese:quit'),
  onOutput: (fn) => ipcRenderer.on('cheese:output', (_e, d) => fn(d)),
  onExit: (fn) => ipcRenderer.on('cheese:exit', (_e, code) => fn(code)),
  onSetup: (fn) => ipcRenderer.on('cheese:setup', (_e, t) => fn(t)),
});
