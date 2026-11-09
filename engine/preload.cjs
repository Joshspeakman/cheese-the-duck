const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('cheese', {
  ready: () => ipcRenderer.send('engine:ready'), ack: () => ipcRenderer.send('engine:ack'),
  input: command => ipcRenderer.send('engine:input', command),
  frames: callback => ipcRenderer.on('engine:frame', (_event, frame) => callback(frame)),
  errors: callback => ipcRenderer.on('engine:error', (_event, message) => callback(message)),
  fullscreen: () => ipcRenderer.invoke('engine:fullscreen'), capture: () => ipcRenderer.invoke('engine:capture')
});
