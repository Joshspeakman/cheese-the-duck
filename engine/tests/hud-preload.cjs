const {contextBridge,ipcRenderer}=require('electron');
contextBridge.exposeInMainWorld('cheese',{
 frames:callback=>ipcRenderer.on('hud-test:frame',(_e,frame)=>callback(frame)),
 errors:callback=>ipcRenderer.on('hud-test:error',(_e,message)=>callback(message)),
 input:command=>ipcRenderer.send('hud-test:input',command),
 ready:()=>ipcRenderer.send('hud-test:ready'),ack:()=>{},
 fullscreen:()=>{},capture:async()=>'/tmp/cheese-hud-preview.png',
});
