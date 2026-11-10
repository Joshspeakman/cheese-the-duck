// Own a single localhost inference process for this window's simulation.
const {spawn}=require('node:child_process');
const fs=require('node:fs'),path=require('node:path'),net=require('node:net'),crypto=require('node:crypto');
async function startVoice({packaged,resources,engine,runtime,enabled=true}){
 const model=path.join(require('node:os').homedir(),'Library/Application Support/Cheese the Duck ASCII Engine/local-ai/Qwen3-4B-Q4_K_M.gguf');
 const bin=packaged?path.join(resources,'local-ai','llama-server'):path.join(engine,'build/local-ai/runtime/llama-b12255/llama-server');
 if(!enabled||!fs.existsSync(bin)||!fs.existsSync(model))return {env:{},stop(){}};
 const port=await new Promise((resolve,reject)=>{const s=net.createServer();s.once('error',reject);s.listen(0,'127.0.0.1',()=>{const p=s.address().port;s.close(()=>resolve(p));});});
 const token=crypto.randomBytes(24).toString('hex');
 const logfile=fs.openSync(path.join(runtime,'local-voice.log'),'w');
 const child=spawn(bin,['-m',model,'--host','127.0.0.1','--port',String(port),'--api-key',token,
  '-c','4096','-np','1','-t','4','-tb','4','-ngl','99','--reasoning','off','--chat-template-kwargs','{"enable_thinking":false}',
  '--no-webui'],{stdio:['ignore',logfile,logfile]});
 fs.closeSync(logfile);
 let stopped=false;
 const stop=()=>{if(stopped)return;stopped=true;if(child.exitCode===null){child.kill('SIGTERM');const timer=setTimeout(()=>{if(child.exitCode===null)child.kill('SIGKILL');},1500);timer.unref();}};
 child.on('error',err=>{stopped=true;fs.appendFileSync(path.join(runtime,'local-voice.log'),'Local voice failed to start: '+err.message+'\n');});
 child.on('exit',(code,signal)=>{fs.appendFileSync(path.join(runtime,'local-voice.log'),`Local voice stopped: ${signal||code}\n`);});
 return {env:{CHEESE_SPEECH_PORT:String(port),CHEESE_SPEECH_TOKEN:token},stop,pid:child.pid};
}
module.exports={startVoice};
