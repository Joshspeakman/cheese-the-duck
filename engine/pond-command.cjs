// Preserve physical-copy identity and layout coordinates across the production
// desktop bridge. Only bounded command data crosses into the simulation.
function pondCommand(command){
 if(!command||command.type!=='pond'||typeof command.action!=='string'||command.action.length>=32)return null;
 if(command.target!==undefined&&(typeof command.target!=='string'||command.target.length>128))return null;
 const out={type:'pond',action:command.action,target:command.target||'',text:typeof command.text==='string'?command.text.slice(0,1000):''};
 if(command.instance!=null){if(typeof command.instance!=='string'||command.instance.length>128)return null;out.instance=command.instance;}
 for(const key of ['x','y'])if(command[key]!==undefined){if(typeof command[key]!=='number'||!Number.isFinite(command[key]))return null;out[key]=command[key];}
 return out;
}
module.exports={pondCommand};
